/* Ядро сервера защиты (общее для Deno Deploy, Cloudflare Workers и Node).
   Ничего не знает о среде: получает auth/users.json и маленькое хранилище
   счётчиков (store) с интерфейсом get(key) -> object|null, set(key, object). */

export const MAX_FAILS = 8;              // неверных попыток на пользователя
export const LOCK_MS = 15 * 60 * 1000;   // блокировка после них
export const IP_FAILS = 40;              // суммарно неверных попыток с адреса
export const IP_WINDOW_MS = 10 * 60 * 1000;

/* ---------- PBKDF2 и сравнение ---------- */
export async function pbkdf2(password, salt, iterations) {
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations }, key, 256);
  return new Uint8Array(bits);
}

export function b64d(s) {
  if (typeof atob === "function") {
    const bin = atob(s), out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  return Uint8Array.from(Buffer.from(s, "base64"));   // Node
}

export function ctEq(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

/* ---------- разбор запроса ---------- */
export function parseBody(text) {
  try { return JSON.parse(text || "{}"); } catch { return {}; }
}

/* ---------- основная проверка ----------
   auth  — содержимое auth/users.json
   store — { get(key), set(key, value) }  (счётчики; ключи: "u:<логин>", "ip:<адрес>")
   Возвращает { json, status }                                     */
export async function checkAccess({ auth, store, user, pass, ip = "-", now = Date.now() }) {
  user = String(user || "").trim();
  pass = String(pass || "");
  if (!user || !pass) return { status: 200, json: { ok: false } };

  const rec = auth && auth.users ? auth.users[user] : null;

  const uKey = "u:" + user, ipKey = "ip:" + ip;
  const u = (await store.get(uKey)) || {};
  if (u.lock && u.lock > now) {
    return { status: 200, json: { ok: false, wait: u.lock - now } };
  }
  let iprec = (await store.get(ipKey)) || {};
  if (!iprec.ts || iprec.ts < now - IP_WINDOW_MS) iprec = {};
  if (iprec.f >= IP_FAILS) {
    return { status: 200, json: { ok: false, wait: IP_WINDOW_MS } };
  }

  let ok = !!rec;
  if (ok) {
    const verifier = await pbkdf2(pass, b64d(rec.salt_v), auth.iter);
    ok = ctEq(verifier, b64d(rec.verifier));
  }

  if (!ok) {
    u.f = (u.f || 0) + 1;
    if (u.f >= MAX_FAILS) { u.lock = now + LOCK_MS; u.f = 0; }
    await store.set(uKey, u);
    iprec.f = (iprec.f || 0) + 1; iprec.ts = now;
    await store.set(ipKey, iprec);
    return { status: 200, json: { ok: false } };
  }

  u.f = 0;
  const n = u.v || 0;
  const unlimited = rec.max === null || rec.max === undefined;
  if (!unlimited && n >= rec.max) {
    await store.set(uKey, u);
    return { status: 200, json: { ok: false, limit: true } };
  }
  u.v = n + 1;
  await store.set(uKey, u);
  await store.set(ipKey, { f: 0, ts: now });

  return {
    status: 200,
    json: {
      ok: true,
      role: rec.role || "user",
      iter: auth.iter,
      salt_k: rec.salt_k,
      wrapped_ck: rec.wrapped_ck,
      max: rec.max === undefined ? null : rec.max,
      unlimited,
      left: unlimited ? null : rec.max - u.v
    }
  };
}

/* ---------- CORS ---------- */
export function corsHeaders(origin = "*") {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Max-Age": "86400"
  };
}

/* ---------- загрузка auth/users.json с GitHub (кэш 5 минут) ---------- */
export function usersLoader(url, ttlMs = 300000) {
  let cache = null, at = 0;
  return async function loadUsers() {
    if (cache && Date.now() - at < ttlMs) return cache;
    const r = await fetch(url, { cf: { cacheTtl: 60 } });
    if (!r.ok) throw new Error("users.json: HTTP " + r.status);
    cache = await r.json();
    at = Date.now();
    return cache;
  };
}
