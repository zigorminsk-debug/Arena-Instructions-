# -*- coding: utf-8 -*-
"""Картинки пошагового раздела (русский)."""
from reportlab.graphics.shapes import Rect, String

from diagrams import _label, MUTED, INK, ACCENT, GREEN
from uitk import (badge_n, btn, bubble, check, field, file_row, icon_file, make,
                  pill, radio, toggle, win)


def f7(g):  # GitHub: где кнопка создания
    win(g, 6, 6, 488, 140, "github.com — главная")
    btn(g, 22, 106, 96, 16, "New repository", kind="green", size=6.8)
    badge_n(g, 14, 122, 1)
    _label(g, 70, 96, "зелёная кнопка слева", 6.4, MUTED)
    # плюс справа
    g0 = 452
    from reportlab.graphics.shapes import Rect, String
    g.add(Rect(g0, 118, 14, 14, rx=3, ry=3, fillColor="#f4f6f9", strokeColor="#c7d0de", strokeWidth=0.8))
    g.add(String(g0 + 7, 121.5, "+", fontName="DJ-Bold", fontSize=9, fillColor=INK, textAnchor="middle"))
    g.add(Rect(382, 84, 96, 30, rx=4, ry=4, fillColor="#ffffff", strokeColor="#c7d0de", strokeWidth=0.9))
    g.add(Rect(384, 98, 92, 14, rx=3, ry=3, fillColor="#eff4ff", strokeColor="#eff4ff"))
    g.add(String(390, 102, "New repository", fontName="DJ", fontSize=7, fillColor=INK))
    badge_n(g, 376, 105, 1)
    _label(g, 250, 40, "Подойдёт любой из двух способов — откроется одна и та же форма", 6.8, MUTED)


def f8(g):  # форма создания репозитория
    win(g, 6, 6, 488, 182, "github.com/new — создание репозитория")
    field(g, 26, 142, 220, "Repository name  (имя репозитория)", "moi-dokumenty", badge=1)
    _label(g, 262, 150, "имя — латинскими буквами,", 6.4, MUTED, anchor="start")
    _label(g, 262, 141, "без пробелов: moi-dokumenty", 6.4, MUTED, anchor="start")
    radio(g, 26, 116, "Public  (видят все)", on=False)
    radio(g, 26, 96, "Private  (видите только вы)", on=True,
          note="для документов выбирайте Private", badge=2)
    check(g, 26, 66, "Add a README file  (создать файл-описание)", on=True, badge=3)
    btn(g, 26, 30, 110, 16, "Create repository", kind="green", size=6.8, badge=4)
    _label(g, 150, 35, "нажмите — и репозиторий создан", 6.4, MUTED, anchor="start")


def f9(g):  # репозиторий готов
    win(g, 6, 6, 488, 168, "github.com/vy/moi-dokumenty")
    _label(g, 26, 150, "moi-dokumenty", 8.2, INK, bold=True, anchor="start")
    badge_n(g, 100, 153, 1)
    _label(g, 112, 150, "это адрес вашего «шкафа» для файлов", 6.4, MUTED, anchor="start")
    _label(g, 26, 134, "Code    Issues    Pull requests    Settings", 6.8, MUTED, anchor="start")
    btn(g, 396, 128, 76, 14, "Add file", size=6.6)
    file_row(g, 26, 102, 446, "D", "README.md")
    file_row(g, 26, 80, 446, "F", "activity   — сюда кладём готовые «Активити»")
    file_row(g, 26, 58, 446, "F", "tp         — сюда кладём готовые ТП")
    file_row(g, 26, 36, 446, "F", "shablony   — ваши образцы документов")
    _label(g, 26, 20, "Папки можно создать прямо здесь кнопкой Add file или попросить агента", 6.4, MUTED, anchor="start")


def f10(g):  # подключение в Arena
    win(g, 6, 6, 488, 148, "Arena — панель подключений")
    file_row(g, 26, 108, 446, "G", "GitHub — код и файлы ваших репозиториев")
    btn(g, 392, 110, 80, 13, "Connect", kind="blue", size=6.6, badge=1)
    from reportlab.graphics.shapes import Line
    g.add(Line(26, 96, 472, 96, strokeColor="#c7d0de", strokeWidth=0.6))
    _label(g, 26, 82, "После авторизации:", 6.8, INK, bold=True, anchor="start")
    file_row(g, 26, 56, 446, "G", "GitHub — подключено")
    toggle(g, 420, 60, on=True)
    btn(g, 300, 24, 130, 13, "Manage repositories", size=6.4, badge=2)
    _label(g, 26, 28, "выбрать, какие репозитории видит Arena", 6.4, MUTED, anchor="start")


def f11(g):  # выбор репозитория + тумблер
    win(g, 6, 6, 240, 152, "Manage repositories")
    check(g, 22, 122, "moi-dokumenty", on=True, badge=1)
    check(g, 22, 100, "staryj-proekt", on=False)
    check(g, 22, 78, "lichnoe", on=False)
    btn(g, 22, 34, 70, 14, "Save", kind="blue", size=6.8)
    _label(g, 100, 39, "отметьте галочкой нужный", 6.4, MUTED, anchor="start")
    win(g, 258, 6, 236, 152, "Arena — этот чат")
    _label(g, 274, 128, "Подключения чата:", 6.8, INK, bold=True, anchor="start")
    _label(g, 274, 106, "GitHub", 7.4, INK, bold=True, anchor="start")
    toggle(g, 440, 104, on=True)
    badge_n(g, 466, 110, 2)
    _label(g, 274, 88, "включено для этого разговора", 6.4, MUTED, anchor="start")
    _label(g, 274, 60, "Тумблер выключен — агент не видит", 6.4, MUTED, anchor="start")
    _label(g, 274, 51, "GitHub, даже если он подключён", 6.4, MUTED, anchor="start")


def f12(g):  # задача в чате
    win(g, 6, 6, 488, 178, "Arena — чат Agent Mode")
    bubble(g, 128, 112, 344, 46, [
        "*Сделай документ Word «Активити на март»:",
        "цель, бюджет, календарь действий.",
        "Сохрани в папку activity."], who="user")
    badge_n(g, 478, 152, 1)
    bubble(g, 26, 52, 344, 48, [
        "*Готово. Файл activity/aktivnost-mart.docx создан.",
        "Открыт Pull Request #12 — это предложение сохранить",
        "файл в репозиторий. Проверьте и нажмите Merge."], who="agent")
    badge_n(g, 376, 94, 2)
    _label(g, 26, 24, "Вы пишете задачу простыми словами — агент делает файл сам", 6.6, MUTED, anchor="start")


def f13(g):  # Pull Request и Merge
    win(g, 6, 6, 488, 170, "Pull Request #12 — Активити на март")
    _label(g, 26, 146, "Изменения:  + activity/aktivnost-mart.docx", 7.0, INK, anchor="start")
    pill(g, 26, 118, 130, "✓ Checks: проверки пройдены", kind="green", badge=1)
    btn(g, 26, 78, 130, 16, "Merge pull request", kind="green", size=6.8, badge=2)
    _label(g, 168, 83, "нажмите — файл окончательно", 6.4, MUTED, anchor="start")
    _label(g, 168, 74, "сохранится в репозитории", 6.4, MUTED, anchor="start")
    btn(g, 26, 46, 130, 16, "Скачать файлы", kind="plain", size=6.8, badge=3)
    _label(g, 168, 51, "или просто заберите файлы себе,", 6.4, MUTED, anchor="start")
    _label(g, 168, 42, "не сохраняя их в репозиторий", 6.4, MUTED, anchor="start")


def f14(g):  # где лежат документы
    win(g, 6, 6, 488, 172, "github.com/vy/moi-dokumenty")
    file_row(g, 26, 128, 300, "W", "activity/aktivnost-mart.docx", badge=1, dl=True)
    file_row(g, 26, 104, 300, "W", "tp/tp-kofemashina.docx", dl=True)
    file_row(g, 26, 80, 300, "X", "activity/byudzhet-mart.xlsx", dl=True)
    icon_file(g, 360, 116, "W")
    _label(g, 380, 120, "Word откроется", 6.6, INK, anchor="start")
    _label(g, 380, 111, "на компьютере", 6.6, INK, anchor="start")
    icon_file(g, 360, 84, "X")
    _label(g, 380, 88, "Excel откроется", 6.6, INK, anchor="start")
    _label(g, 380, 79, "на компьютере", 6.6, INK, anchor="start")
    badge_n(g, 348, 124, 2)
    _label(g, 26, 40, "Нажали на строку файла → справа кнопка Download: файл скачается", 6.6, MUTED, anchor="start")
    _label(g, 26, 28, "и откроется в Word или Excel как обычный документ", 6.6, MUTED, anchor="start")


fig_n1 = make(f7, 152)
fig_n2 = make(f8, 194)
fig_n3 = make(f9, 180)
fig_n4 = make(f10, 160)
fig_n5 = make(f11, 164)
fig_n6 = make(f12, 190)
fig_n7 = make(f13, 182)
fig_n8 = make(f14, 184)


def f15(g):  # Add file -> Upload files
    win(g, 6, 6, 488, 150, "github.com/vy/moi-dokumenty/shablony")
    _label(g, 26, 132, "moi-dokumenty / shablony", 7.6, INK, bold=True, anchor="start")
    btn(g, 386, 126, 86, 14, "Add file", size=6.6, badge=1)
    g.add(Rect(330, 88, 142, 34, rx=4, ry=4, fillColor="#ffffff", strokeColor="#c7d0de", strokeWidth=0.9))
    g.add(String(338, 110, "Create new file", fontName="DJ", fontSize=7, fillColor=INK))
    from reportlab.graphics.shapes import Rect as R
    g.add(R(332, 90, 138, 14, rx=3, ry=3, fillColor="#eff4ff", strokeColor="#eff4ff"))
    g.add(String(338, 94, "Upload files", fontName="DJ-Bold", fontSize=7, fillColor=INK))
    badge_n(g, 324, 97, 2)
    _label(g, 26, 60, "Откройте нужную папку (например, shablony),", 6.6, MUTED, anchor="start")
    _label(g, 26, 50, "нажмите Add file и выберите Upload files", 6.6, MUTED, anchor="start")


def f16(g):  # перетащить и Commit
    win(g, 6, 6, 488, 168, "Upload files — загрузка ваших файлов")
    from reportlab.graphics.shapes import Rect as R
    g.add(R(26, 96, 446, 48, rx=6, ry=6, fillColor="#f7f8fb", strokeColor="#c7d0de", strokeWidth=1))
    ln = None
    g.add(R(26, 96, 446, 48, rx=6, ry=6, fillColor=None, strokeColor="#1d4ed8", strokeWidth=1))
    _label(g, 250, 122, "Перетащите файлы сюда", 7.6, INK, bold=True)
    _label(g, 250, 110, "или нажмите «choose your files» и выберите на компьютере", 6.6, MUTED)
    badge_n(g, 18, 138, 1)
    file_row(g, 26, 66, 300, "W", "aktivnost.docx")
    _label(g, 336, 71, "загружен", 6.6, GREEN, anchor="start")
    badge_n(g, 18, 74, 2)
    btn(g, 26, 30, 110, 16, "Commit changes", kind="green", size=6.8, badge=3)
    _label(g, 150, 35, "нажмите — файл сохранится в папке", 6.6, MUTED, anchor="start")


def f17(g):  # скачать из репозитория
    win(g, 6, 6, 488, 150, "github.com — файл aktivnost-mart.docx")
    icon_file(g, 26, 116, "W")
    _label(g, 44, 120, "activity / aktivnost-mart.docx", 7.6, INK, bold=True, anchor="start")
    badge_n(g, 18, 124, 1)
    btn(g, 330, 116, 60, 14, "Raw", size=6.6)
    btn(g, 396, 116, 76, 14, "Download", kind="blue", size=6.6, badge=2)
    _label(g, 26, 92, "1. Кликните по файлу в папке activity", 6.8, INK, anchor="start")
    _label(g, 26, 80, "2. Нажмите Download — файл скачается", 6.8, INK, anchor="start")
    icon_file(g, 300, 40, "W")
    _label(g, 320, 48, "откроется в Word", 6.8, INK, anchor="start")
    _label(g, 320, 38, "на вашем компьютере", 6.8, INK, anchor="start")
    _arrow_l(g)


def _arrow_l(g):
    from diagrams import _arrow
    _arrow(g, 250, 48, 292, 48, color=ACCENT)


def f18(g):  # Workspace
    win(g, 6, 6, 488, 168, "Arena — панель Workspace (справа от чата)")
    file_row(g, 26, 122, 330, "W", "aktivnost-mart.docx", badge=1)
    btn(g, 366, 124, 52, 13, "открыть", size=6.4)
    btn(g, 424, 124, 48, 13, "скачать", size=6.4)
    file_row(g, 26, 96, 330, "X", "byudzhet-mart.xlsx")
    btn(g, 366, 98, 52, 13, "открыть", size=6.4)
    btn(g, 424, 98, 48, 13, "скачать", size=6.4)
    btn(g, 26, 52, 150, 16, "Download (ZIP)", kind="blue", size=6.8, badge=2)
    _label(g, 190, 57, "вся рабочая папка одним архивом", 6.6, MUTED, anchor="start")
    _label(g, 26, 26, "«открыть» — посмотреть прямо в Arena, «скачать» — забрать файл себе", 6.6, MUTED, anchor="start")


fig_n9 = make(f15, 162)
fig_n10 = make(f16, 180)
fig_n11 = make(f17, 162)
fig_n12 = make(f18, 180)
