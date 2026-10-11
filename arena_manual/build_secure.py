# -*- coding: utf-8 -*-
"""Сборка защищённой части репозитория.

Что делает:
  1. берёт страницы инструкции (private/pages/*.jpg или извлекает их из старого
     HTML-файла --from-html);
  2. шифрует их одним ключом контента CK (AES-256-GCM) -> content/content.bin
     (этот файл можно публиковать: без пароля он бесполезен);
  3. для каждого пользователя считает PBKDF2-проверку пароля и заворачивает CK
     его личным ключом -> auth/users.json (тоже полностью публичный: там нет ни
     одного пароля, только соль/хеш и зашифрованный ключ);
  4. по ключу --check проверяет, что всё сходится: расшифровывает контент
     паролем каждого пользователя и сверяет страницы по sha256.

Запуск:
    python3 arena_manual/gen_users.py            # при необходимости: новые доступы
    python3 arena_manual/build_secure.py         # собрать content/ и auth/
    python3 arena_manual/build_secure.py --check  # проверить целостность

Требуется: pip install cryptography openpyxl
"""
import argparse
import base64
import hashlib
import hmac
import json
import os
import struct
import sys

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit("Нужен модуль cryptography:  pip install cryptography")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRIVATE = os.path.join(ROOT, "private")
AUTH_OUT = os.path.join(ROOT, "auth", "users.json")
BUNDLE_OUT = os.path.join(ROOT, "content", "content.bin")
CK_FILE = os.path.join(PRIVATE, "content_key.bin")
PLAIN = os.path.join(PRIVATE, "users_plain.json")
PAGES_DIR = os.path.join(PRIVATE, "pages")

MAGIC = b"ARENAPG1"
AAD_CK = b"arena-ck-v1"
AAD_BUNDLE = b"arena-bundle-v1"
ITER = 600_000
DK_LEN = 32


# ---------------------------------------------------------------- утилиты
def b64(b: bytes) -> str:
    return base64.b64encode(b).decode()


def pbkdf2(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt,
                               iterations, DK_LEN)


def wrap_ck(password: str, salt_k: bytes, ck: bytes, iterations: int) -> str:
    kek = pbkdf2(password, salt_k, iterations)
    nonce = os.urandom(12)
    return b64(nonce + AESGCM(kek).encrypt(nonce, ck, AAD_CK))


def unwrap_ck(password: str, salt_k_b64: str, wrapped_b64: str,
              iterations: int) -> bytes:
    kek = pbkdf2(password, base64.b64decode(salt_k_b64), iterations)
    blob = base64.b64decode(wrapped_b64)
    return AESGCM(kek).decrypt(blob[:12], blob[12:], AAD_CK)


def pack_bundle(pages):
    """Формат: MAGIC(8) | count(4) | sizes(4*count) | сами JPEG-байты."""
    parts = [MAGIC, struct.pack(">I", len(pages))]
    parts.append(b"".join(struct.pack(">I", len(p)) for p in pages))
    parts.extend(pages)
    return b"".join(parts)


def unpack_bundle(data: bytes):
    assert data[:8] == MAGIC, "не тот формат контента"
    n = struct.unpack(">I", data[8:12])[0]
    sizes = [struct.unpack(">I", data[12 + 4 * i:16 + 4 * i])[0] for i in range(n)]
    off = 12 + 4 * n
    out = []
    for s in sizes:
        out.append(data[off:off + s])
        off += s
    return out


def load_pages(pages_dir, from_html=None):
    if os.path.isdir(pages_dir) and any(f.endswith(".jpg") for f in os.listdir(pages_dir)):
        files = sorted(f for f in os.listdir(pages_dir) if f.endswith(".jpg"))
        return [open(os.path.join(pages_dir, f), "rb").read() for f in files]
    if from_html and os.path.exists(from_html):
        import re
        src = open(from_html, encoding="utf-8").read()
        m = re.search(r"var PAGES = (\[.*?\]);", src, re.S)
        if not m:
            sys.exit("в %s не найден массив PAGES" % from_html)
        return [base64.b64decode(p.split(",", 1)[1]) for p in json.loads(m.group(1))]
    sys.exit("нет страниц: положите JPEG в %s или укажите --from-html" % pages_dir)


# ---------------------------------------------------------------- сборка
def build(pages_dir, from_html, iterations):
    plain = json.load(open(PLAIN, encoding="utf-8"))
    users = plain["users"]
    pages = load_pages(pages_dir, from_html)
    print("страниц: %d, суммарно %.2f МБ" % (len(pages), sum(map(len, pages)) / 1048576))

    ck = os.urandom(32)
    bundle = pack_bundle(pages)
    nonce = os.urandom(12)
    sealed = nonce + AESGCM(ck).encrypt(nonce, bundle, AAD_BUNDLE)

    os.makedirs(os.path.dirname(BUNDLE_OUT), exist_ok=True)
    os.makedirs(os.path.dirname(AUTH_OUT), exist_ok=True)
    os.makedirs(PRIVATE, exist_ok=True)
    open(CK_FILE, "wb").write(ck)
    open(BUNDLE_OUT, "wb").write(sealed)

    out = {"v": 1, "iter": iterations, "users": {}}
    for login, rec in users.items():
        salt_v, salt_k = os.urandom(16), os.urandom(16)
        verifier = pbkdf2(rec["pass"], salt_v, iterations)
        out["users"][login] = {
            "role": rec.get("role", "user"),
            "max": rec.get("max", 5),
            "salt_v": b64(salt_v),
            "verifier": b64(verifier),
            "salt_k": b64(salt_k),
            "wrapped_ck": wrap_ck(rec["pass"], salt_k, ck, iterations),
        }
    json.dump(out, open(AUTH_OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    manifest = {"pages": len(pages),
                "page_sha256": [hashlib.sha256(p).hexdigest() for p in pages],
                "bundle_sha256": hashlib.sha256(sealed).hexdigest(),
                "aad_bundle": AAD_BUNDLE.decode(),
                "aad_ck": AAD_CK.decode()}
    json.dump(manifest, open(os.path.join(PRIVATE, "build_manifest.json"), "w"),
              indent=1)

    print("OK: %s (%.2f МБ)" % (BUNDLE_OUT, os.path.getsize(BUNDLE_OUT) / 1048576))
    print("OK: %s (%d пользователей, только хеши)" % (AUTH_OUT, len(out["users"])))


# ---------------------------------------------------------------- проверка
def check(iterations=None):
    auth = json.load(open(AUTH_OUT, encoding="utf-8"))
    plain = json.load(open(PLAIN, encoding="utf-8"))["users"]
    manifest = json.load(open(os.path.join(PRIVATE, "build_manifest.json"), encoding="utf-8"))
    sealed = open(BUNDLE_OUT, "rb").read()
    assert hashlib.sha256(sealed).hexdigest() == manifest["bundle_sha256"], "файл контента изменён"

    it = iterations or auth["iter"]
    bad = 0
    for login, rec in auth["users"].items():
        pw = plain[login]["pass"]
        # 1) проверка пароля как на сервере
        verifier = pbkdf2(pw, base64.b64decode(rec["salt_v"]), it)
        if not hmac.compare_digest(verifier, base64.b64decode(rec["verifier"])):
            print("ПАРОЛЬ НЕ СХОДИТСЯ:", login)
            bad += 1
            continue
        # 2) разворачиваем ключ контента и расшифровываем
        try:
            ck = unwrap_ck(pw, rec["salt_k"], rec["wrapped_ck"], it)
            pages = unpack_bundle(AESGCM(ck).decrypt(sealed[:12], sealed[12:], AAD_BUNDLE))
        except Exception as e:
            print("НЕ РАСШИФРОВЫВАЕТСЯ:", login, e)
            bad += 1
            continue
        if [hashlib.sha256(p).hexdigest() for p in pages] != manifest["page_sha256"]:
            print("СТРАНИЦЫ НЕ СОВПАДАЮТ:", login)
            bad += 1
    if bad:
        sys.exit("ПРОВЕРКА НЕ ПРОЙДЕНА: %d проблем" % bad)
    print("ПРОВЕРКА ОК: %d доступов, %d страниц, контент расшифровывается каждым паролем"
          % (len(auth["users"]), manifest["pages"]))

    # заодно: не попали ли пароли в публичные файлы
    for path in (AUTH_OUT, BUNDLE_OUT):
        blob = open(path, "rb").read()
        for login, rec in plain.items():
            if rec["pass"].encode() in blob:
                sys.exit("УТЕЧКА: пароль %s найден в %s" % (login, path))
    print("ПРОВЕРКА ОК: паролей нет ни в auth/users.json, ни в content/content.bin")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=PAGES_DIR)
    ap.add_argument("--from-html", default=None,
                    help="извлечь страницы из старого HTML-файла с массивом PAGES")
    ap.add_argument("--iter", type=int, default=ITER)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        check()
    else:
        build(a.pages, a.from_html, a.iter)
