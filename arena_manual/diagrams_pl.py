# -*- coding: utf-8 -*-
"""Schematy wektorowe (wersja polska) — geometria jak w diagrams.py."""
from diagrams import (_arrow, _box, _drawing, _label, ACCENT, ACCENT_BG, AMBER,
                      AMBER_BG, DARK, GREEN, GREEN_BG, GREY_BG, INK, LIGHT, LINE,
                      MUTED, RED, RED_BG, SCALE, WHITE)


def diagram_architecture(width=482, height=210):
    g = __import__("reportlab.graphics.shapes", fromlist=["Group"]).Group()
    _box(g, 6, 130, 100, 40, "Użytkownik", "prompt, pliki, ocena",
         fill=GREY_BG, edge=LINE)
    _box(g, 138, 122, 116, 56, "Agent Mode", "model orkiestratora",
         fill=DARK, edge=DARK, tcolor=WHITE, subcolor=LIGHT)
    _box(g, 138, 78, 116, 34, "Workspace", "piaskownica: pliki sesji",
         fill=GREEN_BG, edge=GREEN, tsize=8.2, ssize=6.6)
    tools = [("Powłoka i kod", 190), ("Szukanie w sieci", 158),
             ("Czytanie stron", 126), ("Pliki i podgląd", 94),
             ("Obrazy", 62), ("Mowa / audio", 30)]
    for name, y in tools:
        _box(g, 288, y, 92, 24, name, fill=ACCENT_BG, edge=ACCENT, tsize=7.6)
    _box(g, 402, 40, 92, 140, "", None, fill=AMBER_BG, edge=AMBER)
    _label(g, 448, 160, "Usługi", 8.2, INK, bold=True)
    _label(g, 448, 150, "zewnętrzne", 8.2, INK, bold=True)
    for i, t in enumerate(["konektory", "GitHub i API", "strony www", "npm / pip"]):
        _label(g, 448, 132 - i * 11, t, 6.8, MUTED)
    _arrow(g, 106, 150, 138, 150)
    _label(g, 122, 156, "zadanie", 6.4)
    _arrow(g, 138, 140, 106, 140, color=ACCENT, dashed=True)
    _label(g, 122, 130, "wynik", 6.4, ACCENT)
    _arrow(g, 196, 122, 196, 112, color=GREEN)
    _label(g, 234, 114, "czyta i zapisuje", 6.4, GREEN)
    for _, y in tools:
        _arrow(g, 254, 150, 288, y + 12)
    for _, y in tools:
        _arrow(g, 380, y + 12, 402, 110, color=AMBER, dashed=True)
    _label(g, 250, 12, "Na schemacie nie pokazano: zmiana modelu wewnątrz sesji, procesy w tle i podgląd portów",
           6.4, MUTED)
    return _drawing(g, width, height, SCALE)


def diagram_loop(width=482, height=112):
    from reportlab.graphics.shapes import Group
    g = Group()
    steps = [("1. Prompt", 6, 80), ("2. Plan", 96, 80), ("3. Narzędzia", 186, 88),
             ("4. Pliki", 284, 66), ("5. Kontrola", 360, 80), ("6. Wynik", 448, 46)]
    for name, x, w in steps:
        _box(g, x, 58, w, 30, name, tsize=7.6)
        if x + w < 486:
            _arrow(g, x + w + 1, 73, x + w + 8, 73)
    _box(g, 6, 8, 488, 26, "Informacja zwrotna: „kontynuuj”, doprecyzowania, punktowe poprawki, ocena wyniku",
         fill=AMBER_BG, edge=AMBER, tsize=7.4)
    _arrow(g, 250, 58, 250, 34, color=AMBER)
    _arrow(g, 20, 34, 20, 58, color=AMBER, dashed=True)
    return _drawing(g, width, height, SCALE)


def diagram_connector_states(width=482, height=112):
    from reportlab.graphics.shapes import Group
    g = Group()
    _box(g, 6, 66, 106, 34, "Nie podłączono", "usługa nie wybrana", fill=GREY_BG, edge=LINE)
    _box(g, 152, 66, 104, 34, "Podłączono", "OAuth przeszła", fill=ACCENT_BG, edge=ACCENT)
    _box(g, 296, 66, 96, 34, "Wyłączono", "nie dla tego czatu", fill=AMBER_BG, edge=AMBER)
    _box(g, 432, 66, 62, 34, "Włączono", None, fill=GREEN_BG, edge=GREEN, tsize=7.8)
    _arrow(g, 112, 83, 152, 83)
    _arrow(g, 256, 83, 296, 83)
    _arrow(g, 392, 83, 432, 83)
    _label(g, 132, 90, "podłącz", 6.2)
    _label(g, 276, 90, "przełącznik czatu", 6.2)
    _label(g, 412, 90, "włącz", 6.2)
    _box(g, 152, 8, 342, 34, "Narzędzia usługi dogrywają się na żądanie: jedna usługa — jeden czat",
         fill=GREY_BG, edge=LINE, tsize=7.2)
    _arrow(g, 463, 66, 463, 42, color=GREEN, dashed=True)
    return _drawing(g, width, height, SCALE)


def diagram_github(width=482, height=156):
    from reportlab.graphics.shapes import Group
    g = Group()
    row1 = [("GitHub OAuth", 6), ("Repozytorium i gałąź", 128), ("Klon do piaskownicy", 250),
            ("Poprawki, testy kodu", 372)]
    for name, x in row1:
        _box(g, x, 108, 112, 30, name, tsize=7.4)
    for x in (118, 240, 362):
        _arrow(g, x + 0.5, 123, x + 9.5, 123)
    row2 = [("Commit i push", 372), ("Pull Request", 250), ("Diff i Checks", 128),
            ("Merge, zakończenie", 6)]
    for name, x in row2:
        _box(g, x, 54, 112, 30, name, tsize=7.4)
    _arrow(g, 428, 108, 428, 84)
    _arrow(g, 372, 69, 362.5, 69)
    _arrow(g, 250, 69, 240.5, 69)
    _arrow(g, 128, 69, 118.5, 69)
    _box(g, 6, 4, 478, 32, "Po merge lub zamknięciu PR sesja nie może już pushować: nowe pliki zostaną tylko w czacie",
         fill=RED_BG, edge=RED, tsize=7.2)
    _arrow(g, 62, 54, 62, 36, color=RED)
    return _drawing(g, width, height, SCALE)


def diagram_files(width=482, height=142):
    from reportlab.graphics.shapes import Group
    g = Group()
    _box(g, 6, 96, 112, 40, "Twoje pliki", "wgranie / wklejenie", fill=GREY_BG, edge=LINE)
    _box(g, 188, 96, 116, 40, "Workspace", "pliki sesji", fill=GREEN_BG, edge=GREEN)
    _box(g, 374, 96, 112, 40, "Wynik", "podgląd, pobranie", fill=ACCENT_BG, edge=ACCENT)
    _arrow(g, 118, 116, 188, 116)
    _arrow(g, 304, 116, 374, 116)
    _label(g, 153, 122, "kopia do piaskownicy", 6.2)
    _label(g, 339, 122, "agent zapisuje pliki", 6.2)
    _box(g, 6, 40, 228, 36, "Bez GitHuba: Workspace → Download (ZIP)",
         fill=ACCENT_BG, edge=ACCENT, tsize=7.4)
    _box(g, 258, 40, 228, 36, "Z GitHubem: gałąź → Pull Request → merge",
         fill=AMBER_BG, edge=AMBER, tsize=7.4)
    _arrow(g, 404, 96, 130, 76, color=ACCENT)
    _arrow(g, 420, 96, 372, 76, color=AMBER)
    _box(g, 6, 2, 480, 28, "Między replikami zachowują się tylko pliki katalogu roboczego piaskownicy",
         fill=GREY_BG, edge=LINE, tsize=7.2)
    return _drawing(g, width, height, SCALE)


def diagram_docs(width=482, height=130):
    from reportlab.graphics.shapes import Group
    g = Group()
    left = [("PDF", 96), ("DOCX / XLSX / PPTX", 72), ("CSV / JSON", 48),
            ("Tekst / Markdown / kod", 24)]
    for name, y in left:
        _box(g, 6, y, 128, 20, name, tsize=7.0)
    _box(g, 176, 24, 132, 92, "", None, fill=GREEN_BG, edge=GREEN)
    _label(g, 242, 100, "Piaskownica", 8.2, INK, bold=True)
    for i, t in enumerate(["parsowanie PDF i Office", "tabele i dane",
                           "czytanie obrazów", "analiza i obliczenia",
                           "przebudowa dokumentu"]):
        _label(g, 242, 84 - i * 11, t, 6.8, MUTED)
    right = [("DOCX / PDF / PPTX", 96), ("XLSX / CSV", 72), ("HTML / Markdown", 48),
             ("Obrazy, SVG, audio", 24)]
    for name, y in right:
        _box(g, 350, y, 136, 20, name, tsize=7.0, fill=ACCENT_BG, edge=ACCENT)
    for y in (106, 82, 58, 34):
        _arrow(g, 134, y, 176, 70)
        _arrow(g, 308, 70, 350, y)
    return _drawing(g, width, height, SCALE)
