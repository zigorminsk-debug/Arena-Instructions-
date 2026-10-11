# -*- coding: utf-8 -*-
"""Мини-набор для рисования понятных «скриншотов» интерфейсов (языконезависимый)."""
from reportlab.graphics.shapes import Circle, Group, Rect, String

from diagrams import (ACCENT, ACCENT_BG, AMBER, AMBER_BG, FONT, FONT_B, GREEN,
                      GREEN_BG, GREY_BG, INK, LINE, MUTED, RED, SCALE, WHITE,
                      _arrow, _drawing, _label)


def win(g, x, y, w, h, title):
    """Окно браузера с верхней панелью."""
    g.add(Rect(x, y, w, h, rx=6, ry=6, fillColor=WHITE, strokeColor=LINE, strokeWidth=1))
    g.add(Rect(x, y + h - 16, w, 16, rx=6, ry=6, fillColor=GREY_BG,
               strokeColor=LINE, strokeWidth=0.8))
    g.add(Rect(x + 1, y + h - 16, w - 2, 8, fillColor=GREY_BG, strokeColor=GREY_BG))
    for i, c in enumerate([RED, AMBER, GREEN]):
        g.add(Circle(x + 9 + i * 7, y + h - 8, 2.1, fillColor=c, strokeColor=None))
    g.add(String(x + 30, y + h - 10.5, title, fontName=FONT, fontSize=6.8,
                 fillColor=MUTED))


def btn(g, x, y, w, h, label, kind="plain", size=7.2, badge=None):
    if kind == "green":
        fill, edge, tcol = GREEN, GREEN, WHITE
    elif kind == "blue":
        fill, edge, tcol = ACCENT, ACCENT, WHITE
    else:
        fill, edge, tcol = WHITE, LINE, INK
    g.add(Rect(x, y, w, h, rx=3.5, ry=3.5, fillColor=fill, strokeColor=edge,
               strokeWidth=0.9))
    g.add(String(x + w / 2.0, y + h / 2.0 - 2.6, label, fontName=FONT_B,
                 fontSize=size, fillColor=tcol, textAnchor="middle"))
    if badge is not None:
        badge_n(g, x - 7, y + h, badge)


def badge_n(g, x, y, n):
    g.add(Circle(x, y, 5.4, fillColor=ACCENT, strokeColor=WHITE, strokeWidth=1.2))
    g.add(String(x, y - 2.4, str(n), fontName=FONT_B, fontSize=6.6,
                 fillColor=WHITE, textAnchor="middle"))


def field(g, x, y, w, label, value, badge=None):
    g.add(String(x, y + 13, label, fontName=FONT, fontSize=6.6, fillColor=MUTED))
    g.add(Rect(x, y, w, 13, rx=2.5, ry=2.5, fillColor=WHITE, strokeColor=LINE,
               strokeWidth=0.9))
    g.add(String(x + 5, y + 4, value, fontName=FONT, fontSize=7.0, fillColor=INK))
    if badge is not None:
        badge_n(g, x - 7, y + 8, badge)


def radio(g, x, y, label, on=False, note=None, badge=None):
    g.add(Circle(x + 3, y + 3, 3, fillColor=WHITE, strokeColor=LINE, strokeWidth=0.9))
    if on:
        g.add(Circle(x + 3, y + 3, 1.6, fillColor=ACCENT, strokeColor=None))
    g.add(String(x + 10, y + 0.6, label, fontName=FONT_B if on else FONT,
                 fontSize=7.0, fillColor=INK))
    if note:
        g.add(String(x + 10, y - 8, note, fontName=FONT, fontSize=6.4, fillColor=MUTED))
    if badge is not None:
        badge_n(g, x - 7, y + 3, badge)


def check(g, x, y, label, on=True, badge=None):
    g.add(Rect(x, y, 8, 8, rx=1.6, ry=1.6, fillColor=WHITE, strokeColor=LINE,
               strokeWidth=0.9))
    if on:
        g.add(String(x + 1.6, y + 0.8, "✓", fontName=FONT_B, fontSize=6.6,
                     fillColor=GREEN))
    g.add(String(x + 12, y + 1.2, label, fontName=FONT, fontSize=7.0, fillColor=INK))
    if badge is not None:
        badge_n(g, x - 7, y + 4, badge)


def toggle(g, x, y, on=True):
    fill = GREEN if on else GREY_BG
    g.add(Rect(x, y, 20, 9, rx=4.5, ry=4.5, fillColor=fill, strokeColor=LINE,
               strokeWidth=0.7))
    kx = x + 13.5 if on else x + 3
    g.add(Circle(kx, y + 4.5, 3.2, fillColor=WHITE, strokeColor=LINE, strokeWidth=0.6))


def icon_file(g, x, y, kind):
    col = {"W": ACCENT, "X": GREEN, "D": INK, "F": AMBER, "G": INK}[kind]
    g.add(Rect(x, y, 11, 12, rx=2, ry=2, fillColor=col, strokeColor=col))
    g.add(String(x + 5.5, y + 3.2, kind, fontName=FONT_B, fontSize=6.6,
                 fillColor=WHITE, textAnchor="middle"))


def file_row(g, x, y, w, kind, name, badge=None, dl=False):
    g.add(Rect(x, y, w, 16, rx=3, ry=3, fillColor=WHITE, strokeColor=LINE,
               strokeWidth=0.7))
    icon_file(g, x + 5, y + 2, kind)
    g.add(String(x + 21, y + 5, name, fontName=FONT, fontSize=7.0, fillColor=INK))
    if dl:
        g.add(String(x + w - 8, y + 5, "↓", fontName=FONT_B, fontSize=8,
                     fillColor=ACCENT, textAnchor="middle"))
    if badge is not None:
        badge_n(g, x - 7, y + 8, badge)


def bubble(g, x, y, w, h, lines, who="user"):
    fill = ACCENT_BG if who == "user" else GREY_BG
    g.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=fill, strokeColor=LINE,
               strokeWidth=0.7))
    ty = y + h - 9
    for ln in lines:
        bold = ln.startswith("*")
        txt = ln.lstrip("*")
        g.add(String(x + 7, ty, txt, fontName=FONT_B if bold else FONT,
                     fontSize=6.8, fillColor=INK))
        ty -= 9


def pill(g, x, y, w, label, kind="green", badge=None):
    fill, edge, tcol = {
        "green": (GREEN_BG, GREEN, GREEN),
        "blue": (ACCENT_BG, ACCENT, ACCENT),
        "amber": (AMBER_BG, AMBER, AMBER),
    }[kind]
    g.add(Rect(x, y, w, 12, rx=6, ry=6, fillColor=fill, strokeColor=edge,
               strokeWidth=0.8))
    g.add(String(x + w / 2.0, y + 3.4, label, fontName=FONT_B, fontSize=6.8,
                 fillColor=tcol, textAnchor="middle"))
    if badge is not None:
        badge_n(g, x - 7, y + 6, badge)


def make(fn, height):
    def wrapper():
        g = Group()
        fn(g)
        return _drawing(g, 482, height, SCALE)
    return wrapper
