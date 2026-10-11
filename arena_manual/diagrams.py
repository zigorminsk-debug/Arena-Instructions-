# -*- coding: utf-8 -*-
"""Векторные схемы для инструкции (reportlab.graphics)."""
import math

from reportlab.graphics.shapes import Drawing, Group, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor

INK = HexColor("#111827")
MUTED = HexColor("#4b5563")
ACCENT = HexColor("#1d4ed8")
ACCENT_BG = HexColor("#eff4ff")
LINE = HexColor("#c7d0de")
GREEN = HexColor("#047857")
GREEN_BG = HexColor("#ecfdf5")
AMBER = HexColor("#b45309")
AMBER_BG = HexColor("#fffbeb")
RED = HexColor("#b91c1c")
RED_BG = HexColor("#fef2f2")
DARK = HexColor("#0b1220")
GREY_BG = HexColor("#f4f6f9")
WHITE = HexColor("#ffffff")
LIGHT = HexColor("#9fb0cc")

FONT = "DJ"
FONT_B = "DJ-Bold"


def _box(g, x, y, w, h, title, sub=None, fill=ACCENT_BG, edge=ACCENT,
         tcolor=INK, subcolor=MUTED, tsize=8.4, ssize=7.0):
    g.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=fill, strokeColor=edge, strokeWidth=0.9))
    if sub:
        g.add(String(x + w / 2.0, y + h / 2.0 + 1.5, title, fontName=FONT_B,
                     fontSize=tsize, fillColor=tcolor, textAnchor="middle"))
        g.add(String(x + w / 2.0, y + h / 2.0 - 8.6, sub, fontName=FONT,
                     fontSize=ssize, fillColor=subcolor, textAnchor="middle"))
    else:
        g.add(String(x + w / 2.0, y + h / 2.0 - 3, title, fontName=FONT_B,
                     fontSize=tsize, fillColor=tcolor, textAnchor="middle"))


def _arrow(g, x1, y1, x2, y2, color=LINE, width=1.1, dashed=False):
    ln = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width)
    if dashed:
        ln.strokeDashArray = [3, 2]
    g.add(ln)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 4.6
    x1h = x2 - size * math.cos(ang - 0.42)
    y1h = y2 - size * math.sin(ang - 0.42)
    x2h = x2 - size * math.cos(ang + 0.42)
    y2h = y2 - size * math.sin(ang + 0.42)
    g.add(Polygon([x2, y2, x1h, y1h, x2h, y2h], fillColor=color,
                  strokeColor=color, strokeWidth=0.4))


def _label(g, x, y, text, size=7.0, color=MUTED, bold=False, anchor="middle"):
    g.add(String(x, y, text, fontName=FONT_B if bold else FONT, fontSize=size,
                 fillColor=color, textAnchor=anchor))


def _drawing(g, width, height, scale):
    d = Drawing(width, height)
    g.scale(scale, scale)
    d.add(g)
    return d


SCALE = 482.0 / 500.0


# ---------------------------------------------------------------------------
def diagram_architecture(width=482, height=210):
    g = Group()
    _box(g, 6, 130, 100, 40, "Пользователь", "промпт, файлы, оценка",
         fill=GREY_BG, edge=LINE)
    _box(g, 138, 122, 116, 56, "Agent Mode", "модель-оркестратор",
         fill=DARK, edge=DARK, tcolor=WHITE, subcolor=LIGHT)
    _box(g, 138, 78, 116, 34, "Workspace", "песочница: файлы сессии",
         fill=GREEN_BG, edge=GREEN, tsize=8.2, ssize=6.6)
    tools = [("Оболочка и код", 190), ("Поиск в интернете", 158),
             ("Чтение страниц", 126), ("Файлы и превью", 94),
             ("Изображения", 62), ("Речь / аудио", 30)]
    for name, y in tools:
        _box(g, 288, y, 92, 24, name, fill=ACCENT_BG, edge=ACCENT, tsize=7.6)
    _box(g, 402, 40, 92, 140, "", None, fill=AMBER_BG, edge=AMBER)
    _label(g, 448, 160, "Внешние", 8.2, INK, bold=True)
    _label(g, 448, 150, "сервисы", 8.2, INK, bold=True)
    for i, t in enumerate(["коннекторы", "GitHub и API", "веб-страницы", "npm / pip"]):
        _label(g, 448, 132 - i * 11, t, 6.8, MUTED)
    _arrow(g, 106, 150, 138, 150)
    _label(g, 122, 156, "задача", 6.4)
    _arrow(g, 138, 140, 106, 140, color=ACCENT, dashed=True)
    _label(g, 122, 130, "итог", 6.4, ACCENT)
    _arrow(g, 196, 122, 196, 112, color=GREEN)
    _label(g, 232, 114, "читает и пишет", 6.4, GREEN)
    for _, y in tools:
        _arrow(g, 254, 150, 288, y + 12)
    for _, y in tools:
        _arrow(g, 380, y + 12, 402, 110, color=AMBER, dashed=True)
    _label(g, 250, 12, "На схеме не показаны: смена модели внутри сессии, фоновые процессы и предпросмотр портов",
           6.4, MUTED)
    return _drawing(g, width, height, SCALE)


# ---------------------------------------------------------------------------
def diagram_loop(width=482, height=112):
    g = Group()
    steps = [("1. Промпт", 6, 80), ("2. План", 96, 80), ("3. Инструменты", 186, 88),
             ("4. Файлы", 284, 66), ("5. Проверка", 360, 80), ("6. Итог", 448, 46)]
    for name, x, w in steps:
        _box(g, x, 58, w, 30, name, tsize=7.6)
        if x + w < 486:
            _arrow(g, x + w + 1, 73, x + w + 8, 73)
    _box(g, 6, 8, 488, 26, "Обратная связь: «продолжить», уточнения, точечные правки, оценка результата",
         fill=AMBER_BG, edge=AMBER, tsize=7.4)
    _arrow(g, 250, 58, 250, 34, color=AMBER)
    _arrow(g, 20, 34, 20, 58, color=AMBER, dashed=True)
    return _drawing(g, width, height, SCALE)


# ---------------------------------------------------------------------------
def diagram_connector_states(width=482, height=112):
    g = Group()
    _box(g, 6, 66, 106, 34, "Не подключено", "сервис не выбран", fill=GREY_BG, edge=LINE)
    _box(g, 152, 66, 104, 34, "Подключено", "OAuth пройдена", fill=ACCENT_BG, edge=ACCENT)
    _box(g, 296, 66, 96, 34, "Выключено", "не для этого чата", fill=AMBER_BG, edge=AMBER)
    _box(g, 432, 66, 62, 34, "Включено", None, fill=GREEN_BG, edge=GREEN, tsize=7.8)
    _arrow(g, 112, 83, 152, 83)
    _arrow(g, 256, 83, 296, 83)
    _arrow(g, 392, 83, 432, 83)
    _label(g, 132, 90, "подключить", 6.2)
    _label(g, 276, 90, "тумблер чата", 6.2)
    _label(g, 412, 90, "включить", 6.2)
    _box(g, 152, 8, 342, 34, "Инструменты сервиса подгружаются по требованию: один сервис — один чат",
         fill=GREY_BG, edge=LINE, tsize=7.2)
    _arrow(g, 463, 66, 463, 42, color=GREEN, dashed=True)
    return _drawing(g, width, height, SCALE)


# ---------------------------------------------------------------------------
def diagram_github(width=482, height=156):
    g = Group()
    row1 = [("GitHub OAuth", 6), ("Репозиторий и ветка", 128), ("Клон в песочницу", 250),
            ("Правки, запуск кода", 372)]
    for name, x in row1:
        _box(g, x, 108, 112, 30, name, tsize=7.4)
    for x in (118, 240, 362):
        _arrow(g, x + 0.5, 123, x + 9.5, 123)
    row2 = [("Коммит и push", 372), ("Pull Request", 250), ("Diff и Checks", 128),
            ("Merge, завершение", 6)]
    for name, x in row2:
        _box(g, x, 54, 112, 30, name, tsize=7.4)
    _arrow(g, 428, 108, 428, 84)
    _arrow(g, 372, 69, 362.5, 69)
    _arrow(g, 250, 69, 240.5, 69)
    _arrow(g, 128, 69, 118.5, 69)
    _box(g, 6, 4, 478, 32, "После мержа или закрытия PR сессия больше не может пушить: новые файлы останутся только в чате",
         fill=RED_BG, edge=RED, tsize=7.2)
    _arrow(g, 62, 54, 62, 36, color=RED)
    return _drawing(g, width, height, SCALE)


# ---------------------------------------------------------------------------
def diagram_files(width=482, height=142):
    g = Group()
    _box(g, 6, 96, 112, 40, "Ваши файлы", "загрузка / вставка", fill=GREY_BG, edge=LINE)
    _box(g, 188, 96, 116, 40, "Workspace", "файлы сессии", fill=GREEN_BG, edge=GREEN)
    _box(g, 374, 96, 112, 40, "Результат", "превью, скачивание", fill=ACCENT_BG, edge=ACCENT)
    _arrow(g, 118, 116, 188, 116)
    _arrow(g, 304, 116, 374, 116)
    _label(g, 153, 122, "копия в песочницу", 6.2)
    _label(g, 339, 122, "агент пишет файлы", 6.2)
    _box(g, 6, 40, 228, 36, "Без GitHub: Workspace → Download (ZIP)",
         fill=ACCENT_BG, edge=ACCENT, tsize=7.4)
    _box(g, 258, 40, 228, 36, "С GitHub: ветка → Pull Request → merge",
         fill=AMBER_BG, edge=AMBER, tsize=7.4)
    _arrow(g, 404, 96, 130, 76, color=ACCENT)
    _arrow(g, 420, 96, 372, 76, color=AMBER)
    _box(g, 6, 2, 480, 28, "Между репликами сохраняются только файлы рабочей директории песочницы",
         fill=GREY_BG, edge=LINE, tsize=7.2)
    return _drawing(g, width, height, SCALE)


# ---------------------------------------------------------------------------
def diagram_docs(width=482, height=130):
    g = Group()
    left = [("PDF", 96), ("DOCX / XLSX / PPTX", 72), ("CSV / JSON", 48),
            ("Текст / Markdown / код", 24)]
    for name, y in left:
        _box(g, 6, y, 128, 20, name, tsize=7.0)
    _box(g, 176, 24, 132, 92, "Песочница", None, fill=GREEN_BG, edge=GREEN)
    _label(g, 242, 100, "Песочница", 8.2, INK, bold=True)
    for i, t in enumerate(["разбор PDF и Office", "таблицы и данные",
                           "чтение изображений", "анализ и расчёты",
                           "пересборка документа"]):
        _label(g, 242, 84 - i * 11, t, 6.8, MUTED)
    right = [("DOCX / PDF / PPTX", 96), ("XLSX / CSV", 72), ("HTML / Markdown", 48),
             ("Картинки, SVG, аудио", 24)]
    for name, y in right:
        _box(g, 350, y, 136, 20, name, tsize=7.0, fill=ACCENT_BG, edge=ACCENT)
    for y in (106, 82, 58, 34):
        _arrow(g, 134, y, 176, 70)
        _arrow(g, 308, 70, 350, y)
    return _drawing(g, width, height, SCALE)
