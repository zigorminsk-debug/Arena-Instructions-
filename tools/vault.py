# -*- coding: utf-8 -*-
"""Хранилище файлов автора: упаковать PDF/PPTX/XLSX в репозиторий, но закрытым.

Файлы кладутся в protected/*.enc — они остаются в репозитории, но открыть их
можно только паролем владельца (AES-256-GCM, PBKDF2-SHA256 600000).

    python3 tools/vault.py pack  "private/Инструкция.pdf" protected/Инструкция.pdf.enc
    python3 tools/vault.py unpack protected/Инструкция.pdf.enc  private/Инструкция.pdf
    python3 tools/vault.py list protected

Требуется: pip install cryptography
"""
import argparse
import getpass
import hashlib
import os
import sys

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit("Нужен модуль cryptography:  pip install cryptography")

MAGIC = b"ARENAVLT1"
ITER = 600_000


def derive(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITER, 32)


def pack(src: str, dst: str, password: str):
    data = open(src, "rb").read()
    salt, nonce = os.urandom(16), os.urandom(12)
    ct = AESGCM(derive(password, salt)).encrypt(nonce, data, MAGIC)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    open(dst, "wb").write(MAGIC + salt + nonce + ct)
    print("OK: %s -> %s (%.2f МБ)" % (src, dst, os.path.getsize(dst) / 1048576))


def unpack(src: str, dst: str, password: str):
    blob = open(src, "rb").read()
    if blob[:9] != MAGIC:
        sys.exit("не тот формат файла")
    try:
        data = AESGCM(derive(password, blob[9:25])).decrypt(blob[25:37], blob[37:], MAGIC)
    except Exception:
        sys.exit("неверный пароль или файл повреждён")
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    open(dst, "wb").write(data)
    print("OK: %s -> %s (%.2f МБ)" % (src, dst, len(data) / 1048576))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["pack", "unpack", "list"])
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--password", help="пароль (иначе будет запрошен)")
    a = ap.parse_args()

    if a.action == "list":
        for root, _, files in os.walk(a.src):
            for f in sorted(files):
                p = os.path.join(root, f)
                print("%10.2f МБ  %s" % (os.path.getsize(p) / 1048576, p))
        raise SystemExit(0)

    if not a.dst:
        sys.exit("укажите второй путь (куда)")
    pw = a.password or getpass.getpass("Пароль владельца: ")
    if a.action == "pack":
        pack(a.src, a.dst, pw)
    else:
        unpack(a.src, a.dst, pw)
