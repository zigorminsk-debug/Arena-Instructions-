# -*- coding: utf-8 -*-
"""Сервер защиты AI Arena Manual (свой сервер / локальный запуск).

Отдаёт приложение и /api/check: проверяет пароль (PBKDF2-SHA256, как в
auth/users.json), ведёт счётчик просмотров, ограничивает перебор паролей и
возвращает браузеру ключ контента, завёрнутый в ключ пользователя.

Запуск:  python3 server/local_server.py            # порт 8000
         python3 server/local_server.py 8080 --origin https://zigorminsk-debug.github.io
Переменные: ARENA_ADMIN_KEY — ключ для чтения /api/state (иначе только с localhost)

Зависимостей нет — только стандартная библиотека Python 3.8+.
"""
import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUTH = os.path.join(ROOT, "auth", "users.json")
STATE = os.path.join(HERE, "state", "views.json")

MAX_FAILS = 8                 # неверных попыток на пользователя
LOCK_SEC = 15 * 60            # блокировка после них
IP_FAILS = 40                 # суммарно неверных попыток с одного адреса
IP_WINDOW = 10 * 60
MIME = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
        ".bin": "application/octet-stream", ".jpg": "image/jpeg", ".png": "image/png",
        ".pdf": "application/pdf", ".ico": "image/x-icon", ".txt": "text/plain; charset=utf-8"}

LOCK = threading.Lock()
_users_cache = {"mtime": 0, "data": None}


def load_auth():
    with LOCK:
        mtime = os.path.getmtime(AUTH)
        if _users_cache["mtime"] != mtime:
            _users_cache["data"] = json.load(open(AUTH, encoding="utf-8"))
            _users_cache["mtime"] = mtime
        return _users_cache["data"]


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"users": {}, "ips": {}}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False)
    os.replace(tmp, STATE)


def pbkdf2(password, salt, iterations):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, 32)


class Handler(BaseHTTPRequestHandler):
    server_version = "ArenaProtect/2.0"
    protocol_version = "HTTP/1.1"
    origin = "*"
    admin_key = os.environ.get("ARENA_ADMIN_KEY", "")

    # ------------------------------------------------ служебное
    def _headers(self, code, ctype, length, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", self.origin)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.send_header("Content-Length", str(length))
        self.end_headers()

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._headers(code, "application/json; charset=utf-8", len(body))
        self.wfile.write(body)

    def _file(self, path):
        if not os.path.isfile(path):
            return self._json({"error": "not found"}, 404)
        data = open(path, "rb").read()
        ext = os.path.splitext(path)[1].lower()
        self._headers(200, MIME.get(ext, "application/octet-stream"), len(data))
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    # ------------------------------------------------ GET
    def do_OPTIONS(self):
        self._json({})

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self._file(os.path.join(ROOT, "index.html"))
        if path == "/api/ping":
            return self._json({"ok": True, "service": "arena-protect", "users": len(load_auth()["users"])})
        if path == "/api/state":
            if not self.admin_key or self.headers.get("X-Admin-Key") != self.admin_key:
                return self._json({"error": "forbidden"}, 403)
            return self._json(load_state())
        if path.startswith("/app/") or path.startswith("/content/"):
            target = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
            if not target.startswith(ROOT):
                return self._json({"error": "forbidden"}, 403)
            return self._file(target)
        return self._json({"error": "not found"}, 404)

    # ------------------------------------------------ POST /api/check
    def do_POST(self):
        path = self.path.split("?")[0]
        if path != "/api/check":
            return self._json({"error": "not found"}, 404)
        length = int(self.headers.get("Content-Length") or 0)
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            req = {}
        user = str(req.get("user", "")).strip()
        pwd = str(req.get("pass", ""))
        ip = self.client_address[0]
        now = time.time()

        auth = load_auth()
        rec = auth["users"].get(user)
        if not user or not pwd:
            return self._json({"ok": False})

        with LOCK:
            st = load_state()
            u = st["users"].get(user, {})
            if u.get("lock", 0) > now:
                return self._json({"ok": False, "wait": int((u["lock"] - now) * 1000)})
            iprec = st["ips"].get(ip, {})
            if iprec.get("ts", 0) < now - IP_WINDOW:
                iprec = {}
            if iprec.get("f", 0) >= IP_FAILS:
                return self._json({"ok": False, "wait": int(IP_WINDOW * 1000)})

            ok = bool(rec)
            if ok:
                verifier = pbkdf2(pwd, base64.b64decode(rec["salt_v"]), auth["iter"])
                ok = hmac.compare_digest(verifier, base64.b64decode(rec["verifier"]))

            if not ok:
                u["f"] = u.get("f", 0) + 1
                if u["f"] >= MAX_FAILS:
                    u["lock"] = now + LOCK_SEC
                    u["f"] = 0
                st["users"][user] = u
                iprec["f"] = iprec.get("f", 0) + 1
                iprec["ts"] = now
                st["ips"][ip] = iprec
                save_state(st)
                return self._json({"ok": False})

            u["f"] = 0
            n = u.get("v", 0)
            unlimited = rec["max"] is None
            if not unlimited and n >= rec["max"]:
                st["users"][user] = u
                save_state(st)
                return self._json({"ok": False, "limit": True})
            u["v"] = n + 1
            st["users"][user] = u
            st["ips"].pop(ip, None)
            save_state(st)

        body = {"ok": True, "role": rec.get("role", "user"), "iter": auth["iter"],
                "salt_k": rec["salt_k"], "wrapped_ck": rec["wrapped_ck"],
                "max": rec["max"], "unlimited": unlimited,
                "left": None if unlimited else rec["max"] - u["v"]}
        return self._json(body)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("port", nargs="?", type=int, default=8000)
    ap.add_argument("--origin", default="*",
                    help="разрешённый источник CORS (по умолчанию *)")
    a = ap.parse_args()
    Handler.origin = a.origin
    srv = ThreadingHTTPServer(("0.0.0.0", a.port), Handler)
    print("Arena protection server: http://0.0.0.0:%d  (доступов: %d)"
          % (a.port, len(load_auth()["users"])))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
