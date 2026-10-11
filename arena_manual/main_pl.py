# -*- coding: utf-8 -*-
"""Сборка польской версии PDF: python3 main_pl.py"""
import os

from reportlab.platypus import Paragraph

import content_pl as content
from builder import Doc, Manual, S, register_fonts

META = {
    "title": "Szczegółowa instrukcja pracy z AI Arena (Agent Mode)",
    "author": "Przewodnik po Arena Agent Mode",
    "subject": "Praca z dokumentami, plikami, narzędziami i usługami zewnętrznymi w Arena",
    "header": "Instrukcja pracy z AI Arena · Agent Mode",
    "footer": "Opracowano na podstawie oficjalnych materiałów help.arena.ai i bloga Arena",
    "version": "wersja 1.13 · 8 października 2026",
    "page_label": "str.",
    "link_txt": "otwórz stronę ↗",
}


def build():
    register_fonts()
    out = "/home/user/Instrukcja_pracy_z_AI_Arena_PL.pdf"
    doc = Doc(out, META)
    m = Manual(META)
    m.f.extend(content.cover_flow(META))

    m.f.append(Paragraph("Spis treści", S["h1"]))
    m.toc()
    m.pagebreak()

    content.build(m, META)

    doc.multiBuild(m.f)
    return out


if __name__ == "__main__":
    path = build()
    print("OK:", path, os.path.getsize(path), "bytes")
