# -*- coding: utf-8 -*-
"""Готовит сервер защиты в виде ОДНОГО файла для вставки в панель
Deno Deploy или Cloudflare Workers (без установки программ и без git).

    python3 tools/make_server_files.py

Результат в tools/_generated/ (в репозиторий не попадает):
    deno_single.js    — вставить на deno.com/deploy/routes (Playground)
    worker_single.js  — вставить в панели Cloudflare (Workers → Create → код)
Код — тот же самый, что в server/deno.js и server/worker.js: скрипт просто
подставляет содержимое server/arena_core.mjs вместо строки import.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "_generated")
IMPORT = re.compile(r'^import \{([^}]+)\} from "\./arena_core\.mjs";\s*$', re.M)


def build(adapter, name, header):
    core = open(os.path.join(ROOT, "server", "arena_core.mjs"), encoding="utf-8").read()
    src = open(os.path.join(ROOT, "server", adapter), encoding="utf-8").read()
    # экспорт из ядра -> локальные функции
    core = core.replace("export const ", "const ").replace("export async function ", "async function ")
    core = core.replace("export function ", "function ")
    src = IMPORT.sub("", src, count=1)
    single = header + "\n" + core + "\n\n/* ===== адаптер ===== */\n" + src
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    open(path, "w", encoding="utf-8").write(single)
    print("OK: %s (%d КБ)" % (path, len(single) // 1024))


if __name__ == "__main__":
    build("deno.js", "deno_single.js",
          "/* Единый файл сервера защиты AI Arena для Deno Deploy. "
          "Вставьте целиком в панель Deno Deploy (Playground) и нажмите Deploy. */")
    build("worker.js", "worker_single.js",
          "/* Единый файл сервера защиты AI Arena для Cloudflare Workers. "
          "Вставьте целиком в панели Cloudflare (Workers → Create application → код). "
          "Не забудьте привязать KV namespace с именем ARENA_KV. */")
    print("Готово. Подробные шаги: docs/ЗАЩИТА.md")
