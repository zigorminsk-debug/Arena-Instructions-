# -*- coding: utf-8 -*-
"""Сборка одного самодостаточного HTML-файла (Arena_Instruction_App.html).

Внутрь вшивается только ШИФРОТЕКСТ страниц (content/content.bin) — без пароля
он бесполезен, как и раньше остаётся нужен сервер защиты для проверки доступа.

    python3 tools/make_single_file.py [--api https://адрес-сервера]

Файл можно пересылать (Telegram, почта, флешка). Важно: открывать его нужно в
браузере, который даёт доступ к шифрованию (HTTPS-ссылка с того же домена или
www/файл на компьютере). На телефоне, где файл открыт из файлового менеджера,
браузер может запретить шифрование — тогда откройте ссылку.
"""
import argparse
import base64
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Arena_Instruction_App.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="", help="адрес сервера защиты для вшивания в файл")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    app_js = open(os.path.join(ROOT, "app", "app.js"), encoding="utf-8").read()
    cfg_js = open(os.path.join(ROOT, "app", "config.js"), encoding="utf-8").read()
    sealed = open(os.path.join(ROOT, "content", "content.bin"), "rb").read()
    bundle_b64 = base64.b64encode(sealed).decode()

    cfg_js = cfg_js.replace('api: ""', 'api: "%s"' % a.api, 1) if a.api else cfg_js

    inject = ("<script>window.ARENA_BUNDLE_B64=\"%s\";</script>\n"
              "<script>%s</script>\n<script>%s</script>" % (bundle_b64, cfg_js, app_js))
    for tag in ('<script src="app/config.js"></script>\n<script src="app/app.js"></script>',
                '<script src="app/config.js"></script><script src="app/app.js"></script>'):
        if tag in html:
            html = html.replace(tag, inject, 1)
            break
    else:
        raise SystemExit("в index.html не найдены подключения скриптов")

    html = html.replace("</title>", "</title>\n<!-- единый файл: страницы внутри зашифрованы -->", 1)
    open(a.out, "w", encoding="utf-8").write(html)
    print("OK: %s (%.2f МБ, api: %s)" % (a.out, os.path.getsize(a.out) / 1048576, a.api or "как в config.js"))


if __name__ == "__main__":
    main()
