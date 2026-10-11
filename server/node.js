/* Сервер защиты для Node.js 20+ (свой VPS, домашний сервер, Docker).
   Отдаёт приложение И /api/check, счётчики — в server/state/views.json.

   Запуск:  node server/node.js            # порт 8000
            node server/node.js 8080
   Переменные: ARENA_ORIGIN (CORS, по умолчанию *), ARENA_ROOT */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { checkAccess, corsHeaders, parseBody } from "./arena_core.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.ARENA_ROOT || path.dirname(HERE);
const STATE = path.join(HERE, "state", "views.json");
const AUTH = path.join(ROOT, "auth", "users.json");
const PORT = Number(process.argv[2] || process.env.PORT || 8000);
const ORIGIN = process.env.ARENA_ORIGIN || "*";
const MIME = { ".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".bin": "application/octet-stream", ".jpg": "image/jpeg", ".png": "image/png",
  ".pdf": "application/pdf", ".txt": "text/plain; charset=utf-8" };

const store = {
  async get(k) {
    try { return JSON.parse(fs.readFileSync(STATE, "utf-8"))[k] ?? null; } catch { return null; }
  },
  async set(k, v) {
    let all = {};
    try { all = JSON.parse(fs.readFileSync(STATE, "utf-8")); } catch {}
    all[k] = v;
    fs.mkdirSync(path.dirname(STATE), { recursive: true });
    fs.writeFileSync(STATE + ".tmp", JSON.stringify(all, null, 1));
    fs.renameSync(STATE + ".tmp", STATE);
  }
};

function json(res, obj, status = 200) {
  const body = Buffer.from(JSON.stringify(obj), "utf-8");
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store", ...corsHeaders(ORIGIN), "Content-Length": body.length });
  res.end(body);
}

function file(res, rel) {
  const target = path.normalize(path.join(ROOT, rel));
  if (!target.startsWith(ROOT) || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
    return json(res, { error: "not found" }, 404);
  }
  const data = fs.readFileSync(target);
  res.writeHead(200, { "Content-Type": MIME[path.extname(target).toLowerCase()] || "application/octet-stream",
    "Cache-Control": "no-store", "Content-Length": data.length });
  res.end(data);
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  const p = url.pathname;
  if (req.method === "OPTIONS") return json(res, {});
  if (p === "/" || p === "/index.html") return file(res, "index.html");
  if (p === "/api/ping") {
    try {
      const auth = JSON.parse(fs.readFileSync(AUTH, "utf-8"));
      return json(res, { ok: true, service: "arena-protect", users: Object.keys(auth.users).length });
    } catch (e) { return json(res, { ok: false, error: String(e) }, 500); }
  }
  if (p === "/api/check" && req.method === "POST") {
    let raw = "";
    for await (const chunk of req) raw += chunk;
    const body = parseBody(raw);
    const ip = req.socket.remoteAddress || "-";
    try {
      const auth = JSON.parse(fs.readFileSync(AUTH, "utf-8"));
      const { status, json: out } = await checkAccess({ auth, store, user: body.user, pass: body.pass, ip });
      return json(res, out, status);
    } catch (e) { return json(res, { ok: false, error: "users unavailable" }, 503); }
  }
  if (p.startsWith("/app/") || p.startsWith("/content/")) return file(res, p.slice(1));
  return json(res, { error: "not found" }, 404);
}).listen(PORT, "0.0.0.0", () => {
  console.log(`Arena protection server: http://0.0.0.0:${PORT}  (root: ${ROOT})`);
});
