# -*- coding: utf-8 -*-
"""Obrazki rozdziału krok po kroku (wersja polska)."""
from reportlab.graphics.shapes import Line, Rect, String

from diagrams import _label, INK, MUTED, GREEN, ACCENT
from uitk import (badge_n, btn, bubble, check, field, file_row, icon_file, make,
                  pill, radio, toggle, win)


def f7(g):
    win(g, 6, 6, 488, 140, "github.com — strona główna")
    btn(g, 22, 106, 96, 16, "New repository", kind="green", size=6.8)
    badge_n(g, 14, 122, 1)
    _label(g, 70, 96, "zielony przycisk po lewej", 6.4, MUTED)
    g0 = 452
    g.add(Rect(g0, 118, 14, 14, rx=3, ry=3, fillColor="#f4f6f9", strokeColor="#c7d0de", strokeWidth=0.8))
    g.add(String(g0 + 7, 121.5, "+", fontName="DJ-Bold", fontSize=9, fillColor=INK, textAnchor="middle"))
    g.add(Rect(382, 84, 96, 30, rx=4, ry=4, fillColor="#ffffff", strokeColor="#c7d0de", strokeWidth=0.9))
    g.add(Rect(384, 98, 92, 14, rx=3, ry=3, fillColor="#eff4ff", strokeColor="#eff4ff"))
    g.add(String(390, 102, "New repository", fontName="DJ", fontSize=7, fillColor=INK))
    badge_n(g, 376, 105, 1)
    _label(g, 250, 40, "Oba sposoby prowadzą do tego samego formularza", 6.8, MUTED)


def f8(g):
    win(g, 6, 6, 488, 182, "github.com/new — tworzenie repozytorium")
    field(g, 26, 142, 220, "Repository name  (nazwa repozytorium)", "moje-dokumenty", badge=1)
    _label(g, 262, 150, "nazwa — literami łacińskimi,", 6.4, MUTED, anchor="start")
    _label(g, 262, 141, "bez spacji: moje-dokumenty", 6.4, MUTED, anchor="start")
    radio(g, 26, 116, "Public  (widzą wszyscy)", on=False)
    radio(g, 26, 96, "Private  (widzisz tylko Ty)", on=True,
          note="do dokumentów wybieraj Private", badge=2)
    check(g, 26, 66, "Add a README file  (utwórz plik-opis)", on=True, badge=3)
    btn(g, 26, 30, 110, 16, "Create repository", kind="green", size=6.8, badge=4)
    _label(g, 150, 35, "kliknij — i repozytorium gotowe", 6.4, MUTED, anchor="start")


def f9(g):
    win(g, 6, 6, 488, 168, "github.com/ty/moje-dokumenty")
    _label(g, 26, 150, "moje-dokumenty", 8.2, INK, bold=True, anchor="start")
    badge_n(g, 108, 153, 1)
    _label(g, 120, 150, "to adres Twojej „szafki” na pliki", 6.4, MUTED, anchor="start")
    _label(g, 26, 134, "Code    Issues    Pull requests    Settings", 6.8, MUTED, anchor="start")
    btn(g, 396, 128, 76, 14, "Add file", size=6.6)
    file_row(g, 26, 102, 446, "D", "README.md")
    file_row(g, 26, 80, 446, "F", "activity   — tu odkładamy gotowe „Activity”")
    file_row(g, 26, 58, 446, "F", "tp         — tu odkładamy gotowe TP")
    file_row(g, 26, 36, 446, "F", "shablony   — Twoje wzory dokumentów")
    _label(g, 26, 20, "Foldery utworzysz tu przyciskiem Add file albo poprosisz agenta", 6.4, MUTED, anchor="start")


def f10(g):
    win(g, 6, 6, 488, 148, "Arena — panel połączeń")
    file_row(g, 26, 108, 446, "G", "GitHub — kod i pliki Twoich repozytoriów")
    btn(g, 392, 110, 80, 13, "Connect", kind="blue", size=6.6, badge=1)
    g.add(Line(26, 96, 472, 96, strokeColor="#c7d0de", strokeWidth=0.6))
    _label(g, 26, 82, "Po autoryzacji:", 6.8, INK, bold=True, anchor="start")
    file_row(g, 26, 56, 446, "G", "GitHub — podłączono")
    toggle(g, 420, 60, on=True)
    btn(g, 300, 24, 130, 13, "Manage repositories", size=6.4, badge=2)
    _label(g, 26, 28, "wybierz, które repozytoria widzi Arena", 6.4, MUTED, anchor="start")


def f11(g):
    win(g, 6, 6, 240, 152, "Manage repositories")
    check(g, 22, 122, "moje-dokumenty", on=True, badge=1)
    check(g, 22, 100, "stary-projekt", on=False)
    check(g, 22, 78, "prywatne", on=False)
    btn(g, 22, 34, 70, 14, "Save", kind="blue", size=6.8)
    _label(g, 100, 39, "zaznacz potrzebne", 6.4, MUTED, anchor="start")
    win(g, 258, 6, 236, 152, "Arena — ten czat")
    _label(g, 274, 128, "Połączenia czatu:", 6.8, INK, bold=True, anchor="start")
    _label(g, 274, 106, "GitHub", 7.4, INK, bold=True, anchor="start")
    toggle(g, 440, 104, on=True)
    badge_n(g, 466, 110, 2)
    _label(g, 274, 88, "włączone dla tej rozmowy", 6.4, MUTED, anchor="start")
    _label(g, 274, 60, "Przełącznik wyłączony — agent nie widzi", 6.4, MUTED, anchor="start")
    _label(g, 274, 51, "GitHuba, nawet jeśli jest podłączony", 6.4, MUTED, anchor="start")


def f12(g):
    win(g, 6, 6, 488, 178, "Arena — czat Agent Mode")
    bubble(g, 128, 112, 344, 46, [
        "*Zrób dokument Word „Activity na marzec”:",
        "cel, budżet, kalendarz działań.",
        "Zapisz w folderze activity."], who="user")
    badge_n(g, 478, 152, 1)
    bubble(g, 26, 52, 344, 48, [
        "*Gotowe. Plik activity/aktywnosc-mart.docx utworzony.",
        "Otwarty Pull Request #12 — to propozycja zapisania",
        "pliku w repozytorium. Sprawdź i kliknij Merge."], who="agent")
    badge_n(g, 376, 94, 2)
    _label(g, 26, 24, "Piszesz zadanie prostymi słowami — agent robi plik sam", 6.6, MUTED, anchor="start")


def f13(g):
    win(g, 6, 6, 488, 170, "Pull Request #12 — Activity na marzec")
    _label(g, 26, 146, "Zmiany:  + activity/aktywnosc-mart.docx", 7.0, INK, anchor="start")
    pill(g, 26, 118, 140, "✓ Checks: kontrole przeszły", kind="green", badge=1)
    btn(g, 26, 78, 130, 16, "Merge pull request", kind="green", size=6.8, badge=2)
    _label(g, 168, 83, "kliknij — plik ostatecznie", 6.4, MUTED, anchor="start")
    _label(g, 168, 74, "zapisze się w repozytorium", 6.4, MUTED, anchor="start")
    btn(g, 26, 46, 130, 16, "Pobierz pliki", kind="plain", size=6.8, badge=3)
    _label(g, 168, 51, "albo po prostu zabierz pliki,", 6.4, MUTED, anchor="start")
    _label(g, 168, 42, "nie zapisując ich w repozytorium", 6.4, MUTED, anchor="start")


def f14(g):
    win(g, 6, 6, 488, 172, "github.com/ty/moje-dokumenty")
    file_row(g, 26, 128, 300, "W", "activity/aktywnosc-mart.docx", badge=1, dl=True)
    file_row(g, 26, 104, 300, "W", "tp/tp-ekspres.docx", dl=True)
    file_row(g, 26, 80, 300, "X", "activity/budzet-mart.xlsx", dl=True)
    icon_file(g, 360, 116, "W")
    _label(g, 380, 120, "Word otworzy się", 6.6, INK, anchor="start")
    _label(g, 380, 111, "na komputerze", 6.6, INK, anchor="start")
    icon_file(g, 360, 84, "X")
    _label(g, 380, 88, "Excel otworzy się", 6.6, INK, anchor="start")
    _label(g, 380, 79, "na komputerze", 6.6, INK, anchor="start")
    badge_n(g, 348, 124, 2)
    _label(g, 26, 40, "Klik w wiersz pliku → po prawej Download: plik się pobierze", 6.6, MUTED, anchor="start")
    _label(g, 26, 28, "i otworzy w Wordzie lub Excelu jak zwykły dokument", 6.6, MUTED, anchor="start")


fig_n1 = make(f7, 152)
fig_n2 = make(f8, 194)
fig_n3 = make(f9, 180)
fig_n4 = make(f10, 160)
fig_n5 = make(f11, 164)
fig_n6 = make(f12, 190)
fig_n7 = make(f13, 182)
fig_n8 = make(f14, 184)


def f15(g):
    win(g, 6, 6, 488, 150, "github.com/ty/moje-dokumenty/shablony")
    _label(g, 26, 132, "moje-dokumenty / shablony", 7.6, INK, bold=True, anchor="start")
    btn(g, 386, 126, 86, 14, "Add file", size=6.6, badge=1)
    g.add(Rect(330, 88, 142, 34, rx=4, ry=4, fillColor="#ffffff", strokeColor="#c7d0de", strokeWidth=0.9))
    g.add(String(338, 110, "Create new file", fontName="DJ", fontSize=7, fillColor=INK))
    g.add(Rect(332, 90, 138, 14, rx=3, ry=3, fillColor="#eff4ff", strokeColor="#eff4ff"))
    g.add(String(338, 94, "Upload files", fontName="DJ-Bold", fontSize=7, fillColor=INK))
    badge_n(g, 324, 97, 2)
    _label(g, 26, 60, "Otwórz potrzebny folder (np. shablony),", 6.6, MUTED, anchor="start")
    _label(g, 26, 50, "kliknij Add file i wybierz Upload files", 6.6, MUTED, anchor="start")


def f16(g):
    win(g, 6, 6, 488, 168, "Upload files — wgrywanie Twoich plików")
    g.add(Rect(26, 96, 446, 48, rx=6, ry=6, fillColor="#f7f8fb", strokeColor="#c7d0de", strokeWidth=1))
    g.add(Rect(26, 96, 446, 48, rx=6, ry=6, fillColor=None, strokeColor="#1d4ed8", strokeWidth=1))
    _label(g, 250, 122, "Przeciągnij pliki tutaj", 7.6, INK, bold=True)
    _label(g, 250, 110, "albo kliknij „choose your files” i wybierz na komputerze", 6.6, MUTED)
    badge_n(g, 18, 138, 1)
    file_row(g, 26, 66, 300, "W", "aktywnosc.docx")
    _label(g, 336, 71, "wgrany", 6.6, GREEN, anchor="start")
    badge_n(g, 18, 74, 2)
    btn(g, 26, 30, 110, 16, "Commit changes", kind="green", size=6.8, badge=3)
    _label(g, 150, 35, "kliknij — plik zapisze się w folderze", 6.6, MUTED, anchor="start")


def f17(g):
    win(g, 6, 6, 488, 150, "github.com — plik aktywnosc-mart.docx")
    icon_file(g, 26, 116, "W")
    _label(g, 44, 120, "activity / aktywnosc-mart.docx", 7.6, INK, bold=True, anchor="start")
    badge_n(g, 18, 124, 1)
    btn(g, 330, 116, 60, 14, "Raw", size=6.6)
    btn(g, 396, 116, 76, 14, "Download", kind="blue", size=6.6, badge=2)
    _label(g, 26, 92, "1. Kliknij plik w folderze activity", 6.8, INK, anchor="start")
    _label(g, 26, 80, "2. Kliknij Download — plik się pobierze", 6.8, INK, anchor="start")
    icon_file(g, 300, 40, "W")
    _label(g, 320, 48, "otworzy się w Wordzie", 6.8, INK, anchor="start")
    _label(g, 320, 38, "na Twoim komputerze", 6.8, INK, anchor="start")
    from diagrams import _arrow
    _arrow(g, 250, 48, 292, 48, color=ACCENT)


def f18(g):
    win(g, 6, 6, 488, 168, "Arena — panel Workspace (po prawej od czatu)")
    file_row(g, 26, 122, 330, "W", "aktywnosc-mart.docx", badge=1)
    btn(g, 366, 124, 52, 13, "otwórz", size=6.4)
    btn(g, 424, 124, 48, 13, "pobierz", size=6.4)
    file_row(g, 26, 96, 330, "X", "budzet-mart.xlsx")
    btn(g, 366, 98, 52, 13, "otwórz", size=6.4)
    btn(g, 424, 98, 48, 13, "pobierz", size=6.4)
    btn(g, 26, 52, 150, 16, "Download (ZIP)", kind="blue", size=6.8, badge=2)
    _label(g, 190, 57, "cała przestrzeń robocza jednym archiwum", 6.6, MUTED, anchor="start")
    _label(g, 26, 26, "„otwórz” — podgląd w Arena, „pobierz” — zabierz plik sobie", 6.6, MUTED, anchor="start")


fig_n9 = make(f15, 162)
fig_n10 = make(f16, 180)
fig_n11 = make(f17, 162)
fig_n12 = make(f18, 180)
