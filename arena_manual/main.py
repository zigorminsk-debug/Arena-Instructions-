# -*- coding: utf-8 -*-
"""Сборка PDF: python3 main.py"""
import os

from reportlab.platypus import Paragraph

import content
from builder import Doc, Manual, S, register_fonts

META = {
    "title": "Подробная инструкция по работе с AI Arena (Agent Mode)",
    "author": "Arena.ai Agent Mode guide",
    "subject": "Работа с документами, файлами, инструментами и внешними сервисами в Arena",
    "header": "Инструкция по работе с AI Arena · Agent Mode",
    "footer": "Подготовлено по официальным материалам help.arena.ai и блога Arena",
    "version": "версия 1.13 · 8 октября 2026",
    "link_txt": "открыть страницу ↗",
}


def build():
    register_fonts()
    out = "/home/user/Инструкция_по_работе_с_AI_Arena.pdf"
    doc = Doc(out, META)
    m = Manual(META)
    m.f.extend(content.cover_flow(META))

    m.f.append(Paragraph("Содержание", S["h1"]))
    m.toc()
    m.pagebreak()

    content.build(m, META)

    doc.multiBuild(m.f)
    return out


if __name__ == "__main__":
    path = build()
    print("OK:", path, os.path.getsize(path), "bytes")
