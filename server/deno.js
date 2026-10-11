/* Сервер защиты для Deno Deploy (вход через GitHub, бесплатный тариф).
   Развёртывание: см. docs/ЗАЩИТА.md (вариант «Deno Deploy»).
   Переменные окружения:
     USERS_URL  — ссылка на auth/users.json (по умолчанию raw этого репозитория)
     APP_ORIGIN — откуда приходит браузер (по умолчанию *)
   Счётчики просмотров хранятся в Deno KV. */
import { checkAccess, corsHeaders, parseBody, usersLoader } from "./arena_core.mjs";

const USERS_URL = Deno.env.get("USERS_URL") ||
  "https://raw.githubusercontent.com/zigorminsk-debug/Arena-Instructions-/main/auth/users.json";
const APP_ORIGIN = Deno.env.get("APP_ORIGIN") || "*";

const loadUsers = usersLoader(USERS_URL);
const kv = await Deno.openKv();
const store = {
  get: async (k) => (await kv.get(["arena", k])).value ?? null,
  set: (k, v) => kv.set(["arena", k], v)
};

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8",
               "Cache-Control": "no-store", ...corsHeaders(APP_ORIGIN), ...extra }
  });
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  if (req.method === "OPTIONS") return json({});
  if (url.pathname === "/api/ping") {
    try {
      const auth = await loadUsers();
      return json({ ok: true, service: "arena-protect", users: Object.keys(auth.users).length });
    } catch (e) {
      return json({ ok: false, error: String(e) }, 500);
    }
  }
  if (url.pathname === "/api/check" && req.method === "POST") {
    const body = parseBody(await req.text());
    const ip = req.headers.get("x-forwarded-for") || "-";
    try {
      const auth = await loadUsers();
      const { status, json: out } = await checkAccess({
        auth, store, user: body.user, pass: body.pass, ip
      });
      return json(out, status);
    } catch (e) {
      return json({ ok: false, error: "users unavailable" }, 503);
    }
  }
  return json({ ok: true, service: "arena-protect", hint: "POST /api/check" });
});
