# -*- coding: utf-8 -*-
"""Страж репозитория: проверяет, что защита не сломана.

Запускается вручную (python3 tools/check_repo.py) и в GitHub Actions при каждом
изменении (.github/workflows/guard.yml). Проверяет:

  1. ни в одном файле публичной части нет паролей из private/users_plain.json;
  2. в auth/users.json нет открытых паролей — только соль/хеш/завёрнутый ключ;
  3. content/content.bin — именно шифротекст (нет признаков JPEG и заголовка);
  4. в публичной части нет «сырых» PDF/PPTX/XLSX/архивов с содержимым
     инструкции и паролями (они должны лежать в protected/*.enc или в private/);
  5. приложение не содержит пароля владельца и не подключает страницы напрямую.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_SKIP = {"private", ".git", "node_modules", ".venv", "server"}
problems = []


def public_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in PUBLIC_SKIP]
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ROOT)
            if rel.startswith("private" + os.sep) or rel.startswith("." + os.sep):
                continue
            yield rel, p


def main():
    plain_path = os.path.join(ROOT, "private", "users_plain.json")
    passwords = []
    if os.path.exists(plain_path):
        plain = json.load(open(plain_path, encoding="utf-8"))["users"]
        passwords = [(login, rec["pass"]) for login, rec in plain.items()]

    # 1. пароли в публичных файлах
    for rel, p in public_files():
        try:
            blob = open(p, "rb").read()
        except Exception:
            continue
        for login, pw in passwords:
            if pw.encode() in blob:
                problems.append("пароль %s найден в публичном файле %s" % (login, rel))

    # 2. auth/users.json
    auth_path = os.path.join(ROOT, "auth", "users.json")
    if not os.path.exists(auth_path):
        problems.append("нет auth/users.json — запустите arena_manual/build_secure.py")
    else:
        auth = json.load(open(auth_path, encoding="utf-8"))
        for login, rec in auth.get("users", {}).items():
            for field in ("pass", "password", "pw"):
                if field in rec:
                    problems.append("в auth/users.json у %s есть поле %s" % (login, field))
            for field in ("salt_v", "verifier", "salt_k", "wrapped_ck"):
                if field not in rec:
                    problems.append("в auth/users.json у %s нет поля %s" % (login, field))
        if auth.get("iter", 0) < 100_000:
            problems.append("слишком мало итераций PBKDF2: %s" % auth.get("iter"))

    # 3. content/content.bin
    bundle_path = os.path.join(ROOT, "content", "content.bin")
    if not os.path.exists(bundle_path):
        problems.append("нет content/content.bin — запустите arena_manual/build_secure.py")
    else:
        blob = open(bundle_path, "rb").read()
        if b"\xff\xd8\xff" in blob[:4096] or b"JFIF" in blob[:4096]:
            problems.append("content/content.bin похож на незашифрованные страницы!")
        if b"ARENAPG1" in blob[:64]:
            problems.append("content/content.bin содержит открытый заголовок пакета")

    # 4. «сырые» файлы с содержимым
    bad_ext = {".pdf", ".pptx", ".xlsx", ".docx", ".zip", ".7z", ".rar"}
    for rel, p in public_files():
        if os.path.splitext(rel)[1].lower() in bad_ext:
            problems.append("в публичной части лежит незашифрованный файл %s" % rel)

    # 5. приложение
    app_js = open(os.path.join(ROOT, "app", "app.js"), encoding="utf-8").read()
    if re.search(r"owner\s*:\s*\{", app_js):
        problems.append("в app.js снова появился блок owner с паролем")
    cfg = open(os.path.join(ROOT, "app", "config.js"), encoding="utf-8").read()
    if re.search(r"pass\s*:", cfg):
        problems.append("в app/config.js есть поле pass")

    # 6. старые незащищённые файлы
    for old in ("arena_manual/users.json", "arena_web/index.html"):
        if os.path.exists(os.path.join(ROOT, old)):
            problems.append("остался старый файл в открытом виде: %s" % old)

    if problems:
        print("НАЙДЕНЫ ПРОБЛЕМЫ:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("ПРОВЕРКА ОК: паролей и открытого содержимого в публичной части нет")


if __name__ == "__main__":
    main()
