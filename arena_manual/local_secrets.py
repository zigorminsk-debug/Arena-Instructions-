# -*- coding: utf-8 -*-
"""Пароли автора берутся ТОЛЬКО из private/ — в репозитории их быть не должно.

Файлы:
    private/owner_pass.txt — пароль владельца (он же открывает protected/*.enc
                             и снимает защиту с PDF, собранных reportlab);
    private/user_pass.txt  — общий пароль на открытие PDF для читателей.

Если файла нет, значение можно задать переменной окружения ARENA_OWNER_PASS
или ARENA_USER_PASS, а для новых сборок построителя — аргументом --owner-pass.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE = os.path.join(ROOT, "private")


def read(name, env=None, default=None):
    env = env or ("ARENA_" + name.replace(".txt", "").upper())
    if os.environ.get(env):
        return os.environ[env]
    path = os.path.join(PRIVATE, name)
    if os.path.exists(path):
        return open(path, encoding="utf-8").read().strip()
    return default


def write(name, value):
    os.makedirs(PRIVATE, exist_ok=True)
    path = os.path.join(PRIVATE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(value.strip() + "\n")
    return path


def owner_password(required=True):
    pw = read("owner_pass.txt")
    if not pw and required:
        raise SystemExit(
            "Нет private/owner_pass.txt — пароль владельца хранится только у вас.\n"
            "Создайте файл с паролем или задайте переменную ARENA_OWNER_PASS.")
    return pw


def user_password(default="12345678"):
    return read("user_pass.txt", default=default)
