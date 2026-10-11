# -*- coding: utf-8 -*-
"""Сервер защиты AI Arena Manual: хранит таблицу логинов/паролей и счётчик
просмотров. Счётчик живой: не сбрасывается кешем, другим устройством,
пересохранением файла. Запуск: python3 counter_server.py [порт] (по умолчанию 8000)."""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(BASE, "..", "arena_web")
STATE = os.path.join(BASE, "views_state.json")
USERS = json.load(open(os.path.join(BASE, "users.json"), encoding="utf-8"))
LOCK = threading.Lock()


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {}


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=1, ensure_ascii=False)
    os.replace(tmp, STATE)


class Handler(BaseHTTPRequestHandler):
    server_version = "ArenaProtect/1.0"

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json({})

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            path = os.path.join(WEB, "index.html")
            with open(path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/api/ping":
            self._json({"ok": True, "users": len(USERS)})
        elif self.path == "/api/state":
            # служебный эндпоинт владельца: текущие счётчики
            self._json(load_state())
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/check":
            return self._json({"error": "not found"}, 404)
        length = int(self.headers.get("Content-Length") or 0)
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            req = {}
        user = str(req.get("user", "")).strip()
        pwd = str(req.get("pass", ""))
        rec = USERS.get(user)
        with LOCK:
            if not rec or rec["pass"] != pwd:
                return self._json({"ok": False})
            st = load_state()
            n = st.get(user, 0)
            if n >= rec["max"]:
                return self._json({"ok": False, "limit": True})
            st[user] = n + 1
            save_state(st)
            left = rec["max"] - st[user]
        self._json({"ok": True, "left": left, "max": rec["max"]})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Arena protection server on 0.0.0.0:%d" % port)
    srv.serve_forever()
