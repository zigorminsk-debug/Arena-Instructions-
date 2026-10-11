/* Сервер защиты для Cloudflare Workers (бесплатный тариф + Workers KV).
   Развёртывание: см. docs/ЗАЩИТА.md (вариант «Cloudflare Workers»).
   Нужно: привязка KV с именем ARENA_KV (см. wrangler.toml).
   Переменные: USERS_URL, APP_ORIGIN (см. wrangler.toml / настройки Worker).

   Внимание: на бесплатном тарифе Cloudflare лимит CPU 10 мс на запрос, а
   PBKDF2 на 600000 итераций может его превысить. Если увидите ошибку 1102 —
   либо перейдите на платный тариф ($5/мес), либо снизьте «iter» в
   auth/users.json (пересоберите: python3 arena_manual/build_secure.py --iter 100000). */
import { checkAccess, corsHeaders, parseBody, usersLoader } from "./arena_core.mjs";

const DEFAULT_USERS_URL =
  "https://raw.githubusercontent.com/zigorminsk-debug/Arena-Instructions-/main/auth/users.json";

let loader = null, loaderUrl = null;

function json(obj, status = 200, origin = "*", extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8",
               "Cache-Control": "no-store", ...corsHeaders(origin), ...extra }
  });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const origin = env.APP_ORIGIN || "*";
    const usersUrl = env.USERS_URL || DEFAULT_USERS_URL;
    if (!loader || loaderUrl !== usersUrl) { loader = usersLoader(usersUrl); loaderUrl = usersUrl; }

    if (req.method === "OPTIONS") return json({}, 200, origin);
    if (url.pathname === "/api/ping") {
      try {
        const auth = await loader();
        return json({ ok: true, service: "arena-protect", users: Object.keys(auth.users).length }, 200, origin);
      } catch (e) {
        return json({ ok: false, error: String(e) }, 500, origin);
      }
    }
    if (url.pathname === "/api/check" && req.method === "POST") {
      const body = parseBody(await req.text());
      const ip = req.headers.get("cf-connecting-ip") || "-";
      const store = {
        get: (k) => env.ARENA_KV.get(k, "json"),
        set: (k, v) => env.ARENA_KV.put(k, JSON.stringify(v))
      };
      try {
        const auth = await loader();
        const { status, json: out } = await checkAccess({
          auth, store, user: body.user, pass: body.pass, ip
        });
        return json(out, status, origin);
      } catch (e) {
        return json({ ok: false, error: "users unavailable" }, 503, origin);
      }
    }
    return json({ ok: true, service: "arena-protect", hint: "POST /api/check" }, 200, origin);
  }
};
