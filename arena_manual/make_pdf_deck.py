# -*- coding: utf-8 -*-
"""PDF-версия презентации в high-tech дизайне + защита: изменение и печать запрещены,
снятие ограничений — паролем владельца."""
import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.utils import ImageReader

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJB", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DM", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
pdfmetrics.registerFont(TTFont("DMB", os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")))

BG = HexColor("#070b14"); PANEL = HexColor("#0d1526"); PANEL2 = HexColor("#1e293b")
CYAN = HexColor("#22d3ee"); BLUE = HexColor("#3b82f6"); VIOLET = HexColor("#8b5cf6")
WHITE = HexColor("#e5e7eb"); MUT = HexColor("#94a3b8"); DIM = HexColor("#475569")
GREEN = HexColor("#34d399"); RED = HexColor("#f87171")

W, H = 960, 540
SH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
RATIO = {"arena_workspace.png": 322 / 1059.0, "arena_feedback.png": 228 / 787.0,
         "arena_chatbar.png": 173 / 698.0, "arena_toggle.png": 486 / 888.0,
         "gh_merge.png": 576 / 934.0}


class Deck:
    def __init__(self, path, password):
        enc = StandardEncryption("12345678", "turbo2*(+", canPrint=1,
                                 canModify=0, canCopy=0, canAnnotate=0,
                                 strength=128)
        self.c = canvas.Canvas(path, pagesize=(W, H), encrypt=enc)
        self.n = 0

    def X(self, x): return x * 72
    def Y(self, y): return H - y * 72

    def rect(self, x, y, w, h, fill=None, line=None, lw=1):
        c = self.c
        c.saveState()
        if fill:
            c.setFillColor(fill)
        if line:
            c.setStrokeColor(line); c.setLineWidth(lw)
            if fill:
                c.rect(self.X(x), self.Y(y + h), w * 72, h * 72, stroke=1, fill=1 if fill else 0)
            else:
                c.rect(self.X(x), self.Y(y + h), w * 72, h * 72, stroke=1, fill=0)
        elif fill:
            c.rect(self.X(x), self.Y(y + h), w * 72, h * 72, stroke=0, fill=1)
        c.restoreState()

    def text(self, x, y, size, color, s, font="DJ"):
        c = self.c
        c.saveState()
        c.setFillColor(color)
        c.setFont(font, size)
        c.drawString(self.X(x), self.Y(y) - size, s)
        c.restoreState()

    def wrap(self, s, font, size, maxw):
        out, cur = [], ""
        for w in s.split():
            t = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= maxw:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
        return out

    def decor(self):
        self.n += 1
        c = self.c
        self.rect(0, 0, 13.333, 7.5, fill=BG)
        self.rect(0, 0, 13.333, 0.045, fill=CYAN)
        self.rect(0, 0.045, 4.5, 0.02, fill=BLUE)
        for hx, hy in [(0.35, 0.35), (12.70, 0.35), (0.35, 6.93), (12.70, 6.93)]:
            self.rect(hx, hy, 0.28, 0.02, fill=DIM)
            self.rect(hx if hx < 1 else hx + 0.26, hy if hy < 1 else hy - 0.28, 0.02, 0.28, fill=DIM)
        for r in range(3):
            for k in range(8):
                self.rect(10.2 + k * 0.28, 0.30 + r * 0.22, 0.04, 0.04, fill=DIM)
        self.text(0.55, 7.06, 9, DIM, "ARENA.AI // AGENT_MODE // PRESENTATION v1.7", "DM")
        self.text(12.1, 7.06, 9, CYAN, "%02d / 09" % self.n, "DM")
        # строка разработчика с кликабельными контактами
        y, size, x = 7.32, 8, 0.55
        segs = [
            ("разработчик: Захаревич Игорь Владимирович", None, MUT),
            ("  ·  ", None, DIM),
            ("ziv@csl.by", "mailto:ziv@csl.by", CYAN),
            ("  ·  ", None, DIM),
            ("csl.by", "http://csl.by", CYAN),
            ("  ·  ", None, DIM),
            ("+375 29 337-14-12", "tel:+375293371412", CYAN),
        ]
        for text, url, color in segs:
            w = pdfmetrics.stringWidth(text, "DM", size)
            self.text(x, y, size, color, text, "DM")
            if url:
                b = H - y * 72 - size
                self.c.linkURL(url, (x * 72, b - 2, x * 72 + w, b + size + 2), relative=0)
            x += w / 72.0

    def header(self, code, kicker, title):
        self.decor()
        self.text(0.7, 0.75, 12, CYAN, "// %s · %s" % (code, kicker), "DMB")
        self.text(0.7, 1.35, 26, WHITE, title, "DJB")
        self.rect(0.72, 1.78, 1.7, 0.045, fill=CYAN)
        self.rect(2.5, 1.78, 0.45, 0.045, fill=BLUE)
        self.rect(3.03, 1.78, 0.16, 0.045, fill=VIOLET)

    def bullets(self, x, y, w, items, size=14):
        yy = y
        for head, rest in items:
            self.text(x, yy, size, CYAN, "▸", "DMB")
            self.text(x + 0.22, yy, size, WHITE, head, "DJB")
            yy += 0.30
            for ln in self.wrap(rest, "DJ", size - 2, w * 72 - 20):
                self.text(x + 0.22, yy, size - 2, MUT, ln)
                yy += 0.26
            yy += 0.14

    def screen(self, path, x, y, w, tag=None):
        h = w * RATIO[path]
        self.rect(x - 0.09, y - 0.09, w + 0.18, h + 0.18, fill=PANEL, line=BLUE, lw=1)
        self.rect(x - 0.09, y - 0.09, w + 0.18, 0.035, fill=CYAN)
        c = self.c
        c.saveState()
        c.drawImage(os.path.join(SH, path), self.X(x), self.Y(y + h), w * 72, h * 72)
        c.restoreState()
        if tag:
            self.text(x - 0.09, y + h + 0.32, 8.5, DIM, tag, "DM")

    def panelbox(self, x, y, w, h, line, fill):
        self.rect(x, y, w, h, fill=fill, line=line, lw=1.2)

    def done(self):
        self.c.save()


d = Deck("/home/user/Презентация_AI_Arena_Agent_Mode_protected.pdf", "turbo2*(+")

# ---- 1 титул
d.decor()
d.rect(0.7, 1.15, 0.12, 2.6, fill=CYAN)
d.text(1.05, 1.35, 12, CYAN, "[ ARENA_AI // AGENT_MODE // OVERVIEW ]", "DMB")
d.text(1.05, 2.2, 34, WHITE, "AI Arena:", "DJB")
d.text(1.05, 2.85, 34, CYAN, "возможности Agent Mode", "DJB")
d.text(1.05, 3.5, 16, MUT, "Что умеет агент, как устроены инструменты и подключения —")
d.text(1.05, 3.85, 16, MUT, "и какой результат вы получаете в конце.")
d.panelbox(1.05, 4.35, 7.6, 1.5, PANEL2, PANEL)
d.text(1.3, 4.72, 12, GREEN, "> agent.run(task)", "DMB")
d.text(1.3, 5.05, 10, MUT, "tools: [web_search, bash, files, images, github]", "DM")
d.text(1.3, 5.35, 10, MUT, "result: docs // tables // prototypes // PR", "DM")
d.text(1.05, 6.35, 9, DIM, "Источники: help.arena.ai · блог Arena · docs.github.com · 8 октября 2026", "DM")
d.screen("arena_workspace.png", 8.9, 2.1, 3.9, "workspace://session_files")

d.c.showPage()
# ---- 2
d.header("01", "ЧТО ТАКОЕ AGENT MODE", "Одна модель делает задачу от начала и до конца")
d.bullets(0.7, 2.1, 7.2, [
    ("Не чат, а рабочий процесс", "цель формулируете один раз — агент сам строит план и выполняет шагами"),
    ("Инструменты из коробки", "поиск в сети, песочница Linux, файлы, генерация картинок"),
    ("Контекст сохраняется", "«переделай таблицу», «добавь раздел» продолжаются с того же места"),
    ("Обратная связь в конце", "Yes / No / Keep working — оценка и продолжение работы"),
])
d.screen("arena_feedback.png", 8.5, 2.3, 4.3, "feedback://was_this_task_successful")

d.c.showPage()
# ---- 3
d.header("02", "ИНСТРУМЕНТЫ АГЕНТА", "Что агент делает руками")
d.bullets(0.7, 2.1, 12.0, [
    ("Поиск и чтение страниц", "актуальные данные из интернета, сайты и документы"),
    ("Песочница bash", "пакеты, скрипты, тесты, серверы; проверяет и чинит ошибки"),
    ("Файлы", "Word- и Excel-совместимые отчёты, Markdown, CSV, HTML"),
    ("Генерация изображений", "иллюстрации и макеты по запросу"),
    ("Уточняющие вопросы", "если задача неоднозначна — спросит, а не додумает"),
    ("Загрузка ваших файлов", "Add files: PNG, PDF, TXT, MD, CSV, HTML, CSS, JS, JSON"),
])

d.c.showPage()
# ---- 4
d.header("03", "РАБОЧЕЕ ПРОСТРАНСТВО", "Всё, что создано, — перед глазами")
d.bullets(0.7, 2.1, 6.6, [
    ("Workspace", "панель справа: файлы сессии, предпросмотр, скачивание"),
    ("Diff", "изменения построчно: последний ход или вся ветка"),
    ("Checks", "статус автопроверок: проходит / упало / в процессе"),
    ("Превью", "живой просмотр сервера, запущенного в песочнице"),
    ("Без GitHub — ZIP", "кнопка Download скачивает всё архивом"),
])
d.screen("arena_workspace.png", 7.8, 2.1, 5.0, "workspace://arena_expert_*")

d.c.showPage()
# ---- 5
d.header("04", "GITHUB", "Результат уходит в ваш репозиторий")
d.bullets(0.7, 2.1, 6.8, [
    ("Подключение в один клик", "OAuth и выбор репозиториев — Manage repositories"),
    ("Агент работает в копии", "клон в песочнице; коммиты и Pull Request — сам"),
    ("Ревью и мерж — ваши", "Diff и Checks помогают принять работу"),
    ("Хранилище документов", "папки shablony / activity / tp, образцы Word и Excel"),
    ("Загрузка образцов", "Add file → Upload files прямо в браузере"),
])
d.screen("gh_merge.png", 8.1, 2.0, 4.7, "github://pull_request → merge")

d.c.showPage()
# ---- 6
d.header("05", "ПОДКЛЮЧЕНИЯ", "Сервисы, к которым агент дотягивается")
d.bullets(0.7, 2.1, 7.4, [
    ("GitHub", "код, репозитории, PR — главная связка для документов"),
    ("Google и другие", "документы, файлы, почта, календарь — набор по аккаунту"),
    ("Тумблер на чат", "подключение включается отдельно для разговора"),
    ("От вашего имени", "агент видит и делает только разрешённое вам"),
    ("Отключение обратимо", "повторное включение — реавторизация, ресурсы сохраняются"),
])
d.screen("arena_toggle.png", 8.6, 2.1, 4.2, "connections://github = ON")

d.c.showPage()
# ---- 7
d.header("06", "РЕЗУЛЬТАТ", "Что вы получаете в конце")
d.bullets(0.7, 2.1, 12.0, [
    ("Готовые документы", "отчёты, справки, письма по вашим образцам — Word и Excel"),
    ("Таблицы и аналитика", "агрегаты, топ-10, дубли и пропуски, графики"),
    ("Прототипы", "сайт или приложение с живым превью из песочницы"),
    ("Разбор входящих файлов", "выжимки из PDF, сравнительные таблицы документов"),
    ("Доставка", "Pull Request в репозиторий или ZIP из Workspace"),
    ("Источники", "ссылки и даты рядом с утверждениями — по запросу"),
])

d.c.showPage()
# ---- 8
d.header("07", "ПРАВИЛА БЕЗ ОПАСНОСТИ", "Три минуты, которые экономят час")
d.bullets(0.7, 2.1, 12.0, [
    ("Забирайте результат", "оставшееся в песочнице — скачать или отправить в репозиторий"),
    ("После мержа пуша нет", "смержили или закрыли PR — сессия больше не отправляет файлы"),
    ("Один PR на сессию", "крупную работу разбивайте на несколько чатов"),
    ("Секреты — не в промпт", "токены и пароли не вставляйте в текст задачи"),
    ("Лимиты", "Battle Mode в Text/Code Arena не тратит дневной баланс Agent Mode"),
])
d.panelbox(0.7, 5.55, 11.93, 1.15, RED, HexColor("#1a0b10"))
d.text(0.95, 5.92, 12, RED, "[!] ГЛАВНАЯ ЛОВУШКА:", "DMB")
d.text(0.95, 6.22, 11, WHITE, "файлы после мержа PR нельзя ни запушить, ни скачать, ни перенести.")
d.text(0.95, 6.48, 11, MUT, "Сначала убедитесь, что всё отправлено, — потом мержите.")

d.c.showPage()
# ---- 9
d.header("08", "КАК НАЧАТЬ", "Четыре шага до первого результата")
d.bullets(0.7, 2.1, 6.8, [
    ("1 · Откройте arena.ai/agent", "или переключите режим в меню слева сверху"),
    ("2 · Опишите задачу простыми словами", "«сделай отчёт по образцу, вот шаблон»"),
    ("3 · Прикрепите файлы", "Add files — образцы, документы, данные"),
    ("4 · Нажмите стрелку", "и принимайте работу: Yes / No / Keep working"),
])
d.screen("arena_chatbar.png", 8.1, 2.2, 4.7, "input://prompt + add_files → run")
d.panelbox(0.7, 5.5, 11.93, 1.1, GREEN, HexColor("#071a14"))
d.text(0.95, 5.87, 12, GREEN, "[OK]", "DMB")
d.text(1.6, 5.87, 11, WHITE, "Подробности — в «Инструкции по работе с AI Arena» (v1.7):")
d.text(0.95, 6.17, 11, MUT, "16 глав, пошаговый раздел для новичка, кликабельные ссылки на Arena и GitHub.")

d.c.showPage()
d.done()
print("OK pdf deck saved")
