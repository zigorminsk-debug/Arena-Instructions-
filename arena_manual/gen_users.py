# -*- coding: utf-8 -*-
"""Генерация личных доступов (100 пользователей + служебные аккаунты).

Пароли НИКОГДА не попадают в публичную часть репозитория:
  * private/users_plain.json                  — источник правды (пароли в открытом виде, только у вас)
  * private/Таблица_логинов_и_паролей.xlsx    — таблица для выдачи пользователям
  * auth/users.json                           — публичный файл: только соль + PBKDF2-проверка (хеш)

Запуск:  python3 arena_manual/gen_users.py            # создать/пересобрать список
         python3 arena_manual/gen_users.py --show       # показать, что уже сгенерировано
         python3 arena_manual/gen_users.py --owner-pass НОВЫЙ_ПАРОЛЬ

Внимание: пароль владельца (developer) тоже хранится только в виде хеша.
"""
import argparse
import json
import os
import random
import secrets
import string

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRIVATE = os.path.join(ROOT, "private")
PLAIN = os.path.join(PRIVATE, "users_plain.json")
XLSX = os.path.join(PRIVATE, "Таблица_логинов_и_паролей.xlsx")

# без 0/O/1/l/i — чтобы не путать символы при вводе с телефона
ALPHA = "abcdefghjkmnpqrstuvwxyz23456789"
PW_LEN = 10                      # 10 символов из 31 ≈ 49,5 бита энтропии
N_USERS = 100
DEFAULT_MAX = 5


def new_password(rng):
    return "".join(rng.choice(ALPHA) for _ in range(PW_LEN))


def build(owner_pass=None, seed=20261011):
    rng = random.Random(seed)
    if os.path.exists(PLAIN):
        data = json.load(open(PLAIN, encoding="utf-8"))
    else:
        data = {"v": 1, "users": {}}

    users = data["users"]
    used = {u["pass"] for u in users.values()}

    for i in range(1, N_USERS + 1):
        login = "user%03d" % i
        if login in users:
            continue
        while True:
            pw = new_password(rng)
            if pw not in used:
                break
        used.add(pw)
        users[login] = {"pass": pw, "max": DEFAULT_MAX, "role": "user"}

    # резервный общий аккаунт (в таблице был указан нерабочий reader/12345678)
    if "reader" not in users:
        while True:
            pw = new_password(secrets.SystemRandom())
            if pw not in used:
                break
        used.add(pw)
        users["reader"] = {"pass": pw, "max": DEFAULT_MAX, "role": "shared"}

    # владелец — без лимита; пароль берём из private/owner_pass.txt
    import local_secrets
    if "developer" not in users:
        pw = owner_pass or local_secrets.owner_password()
        users["developer"] = {"pass": pw, "max": None, "role": "owner"}
    elif owner_pass:
        users["developer"]["pass"] = owner_pass
        local_secrets.write("owner_pass.txt", owner_pass)
    users["developer"]["role"] = "owner"
    users["developer"]["max"] = None

    data["users"] = users
    os.makedirs(PRIVATE, exist_ok=True)
    json.dump(data, open(PLAIN, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return data


def make_xlsx(data):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    except ImportError:
        print("! openpyxl не установлен — таблица XLSX не создана "
              "(pip install openpyxl)")
        return

    hdr_fill = PatternFill("solid", fgColor="1F3864")
    hdr_font = Font(color="FFFFFF", bold=True, size=11)
    thin = Side(style="thin", color="B9C4DA")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    wb = Workbook()
    ws = wb.active
    ws.title = "Пользователи"
    ws.append(["№", "Логин", "Пароль", "Просмотров", "Роль", "Выдан / не выдан"])
    for c in ws[1]:
        c.fill, c.font, c.border = hdr_fill, hdr_font, border
        c.alignment = Alignment(horizontal="center")

    users = data["users"]
    i = 0
    for login, rec in users.items():
        if rec["role"] == "owner":
            continue
        i += 1
        ws.append([i, login, rec["pass"],
                   "без лимита" if rec["max"] is None else rec["max"],
                   rec["role"], "не выдан"])
        for c in ws[ws.max_row]:
            c.border = border
        ws.cell(ws.max_row, 2).font = Font(name="Consolas")
        ws.cell(ws.max_row, 3).font = Font(name="Consolas")
    for col, w in zip("ABCDEF", (6, 12, 13, 13, 12, 18)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"

    ws2 = wb.create_sheet("Служебные")
    ws2.append(["Роль", "Логин", "Пароль", "Лимит"])
    for c in ws2[1]:
        c.fill, c.font = hdr_fill, hdr_font
    for login, rec in users.items():
        if rec["role"] in ("owner", "shared"):
            ws2.append([{"owner": "Владелец (без лимита)",
                         "shared": "Общий резервный"}[rec["role"]],
                        login, rec["pass"], rec["max"] or "без лимита"])
    for col, w in zip("ABCD", (24, 12, 14, 13)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Как выдавать")
    lines = [
        ["1.", "Отправляйте каждому пользователю ТОЛЬКО его строку: логин + пароль и ссылку на инструкцию."],
        ["2.", "Не пересылайте эту таблицу целиком — в ней все пароли."],
        ["3.", "Один логин = один человек: 5 просмотров, счётчик ведёт сервер защиты."],
        ["4.", "Пароль владельца (developer) не вписывайте в письма — он у вас один."],
        ["5.", "Если пароль попал в чужие руки — сгенерируйте доступы заново: python3 arena_manual/gen_users.py --force"],
    ]
    for row in lines:
        ws3.append(row)
    ws3.column_dimensions["A"].width = 5
    ws3.column_dimensions["B"].width = 110

    wb.save(XLSX)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-pass", help="задать новый пароль владельца")
    ap.add_argument("--show", action="store_true", help="показать сводку без изменений")
    args = ap.parse_args()

    if args.show:
        data = json.load(open(PLAIN, encoding="utf-8"))
        users = data["users"]
        print("пользователей:", len(users))
        print("владелец:", "developer" in users)
        print("таблица:", XLSX if os.path.exists(XLSX) else "нет")
        raise SystemExit(0)

    data = build(owner_pass=args.owner_pass)
    make_xlsx(data)
    print("OK: %d записей -> %s" % (len(data["users"]), PLAIN))
    print("    таблица -> %s" % XLSX)
    print("Публичный файл доступов (только хеши) собирает build_secure.py")
