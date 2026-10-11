# -*- coding: utf-8 -*-
"""Движок вёрстки PDF-инструкции по Arena Agent Mode (кириллица: DejaVu)."""
import os

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = HexColor("#111827")
MUTED = HexColor("#4b5563")
ACCENT = HexColor("#1d4ed8")
ACCENT_SOFT = HexColor("#eff4ff")
LINE = HexColor("#d7dde8")
ROW_ALT = HexColor("#f7f8fb")
CODE_BG = HexColor("#f4f6f9")
CODE_BORDER = HexColor("#dbe1ea")
GREEN = HexColor("#065f46")
GREEN_BG = HexColor("#ecfdf5")
AMBER = HexColor("#92400e")
AMBER_BG = HexColor("#fffbeb")
RED = HexColor("#991b1b")
RED_BG = HexColor("#fef2f2")


def register_fonts():
    pdfmetrics.registerFont(TTFont("DJ", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DJ-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DJM", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
    pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-Bold", italic="DJ", boldItalic="DJ-Bold")


def styles():
    s = {}
    s["body"] = ParagraphStyle("body", fontName="DJ", fontSize=9.6, leading=14.2,
                               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    s["lead"] = ParagraphStyle("lead", parent=s["body"], fontSize=10.6, leading=15.6,
                               textColor=MUTED, spaceAfter=8)
    s["h1"] = ParagraphStyle("h1", fontName="DJ-Bold", fontSize=19, leading=23,
                             textColor=INK, spaceBefore=4, spaceAfter=8)
    s["h2"] = ParagraphStyle("h2", fontName="DJ-Bold", fontSize=12.6, leading=16,
                             textColor=ACCENT, spaceBefore=12, spaceAfter=5)
    s["h3"] = ParagraphStyle("h3", fontName="DJ-Bold", fontSize=10.4, leading=14,
                             textColor=INK, spaceBefore=9, spaceAfter=3)
    s["bullet"] = ParagraphStyle("bullet", parent=s["body"], alignment=TA_LEFT,
                                 leftIndent=11, bulletIndent=1, spaceAfter=3.5, leading=13.6)
    s["bullet2"] = ParagraphStyle("bullet2", parent=s["bullet"], leftIndent=22, bulletIndent=12)
    s["num"] = ParagraphStyle("num", parent=s["bullet"])
    s["num2"] = ParagraphStyle("num2", parent=s["num"], leftIndent=24, bulletIndent=13)
    s["code"] = ParagraphStyle("code", fontName="DJM", fontSize=8.1, leading=11.4,
                               textColor=HexColor("#1f2937"), alignment=TA_LEFT,
                               leftIndent=4, rightIndent=4, spaceBefore=1, spaceAfter=1)
    s["cell"] = ParagraphStyle("cell", fontName="DJ", fontSize=8.4, leading=11.4,
                               textColor=INK, alignment=TA_LEFT)
    s["cellb"] = ParagraphStyle("cellb", parent=s["cell"], fontName="DJ-Bold")
    s["head"] = ParagraphStyle("head", fontName="DJ-Bold", fontSize=8.5, leading=11.2,
                               textColor=colors.white, alignment=TA_LEFT)
    s["note_b"] = ParagraphStyle("note_b", fontName="DJ-Bold", fontSize=9.4, leading=13,
                                 textColor=INK, spaceAfter=2)
    s["note_t"] = ParagraphStyle("note_t", fontName="DJ", fontSize=9.1, leading=13,
                                 textColor=INK, alignment=TA_JUSTIFY)
    s["cap"] = ParagraphStyle("cap", fontName="DJ", fontSize=8.3, leading=11,
                              textColor=MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=9)
    s["toc1"] = ParagraphStyle("toc1", fontName="DJ-Bold", fontSize=10, leading=17, textColor=INK)
    s["toc2"] = ParagraphStyle("toc2", fontName="DJ", fontSize=9.2, leading=13.6,
                               textColor=MUTED, leftIndent=13)
    return s


S = styles()


class HeadPara(Paragraph):
    """Заголовок с якорем для оглавления и закладок PDF."""

    def __init__(self, text, style, anchor):
        Paragraph.__init__(self, text, style)
        self.anchor = anchor


class Doc(BaseDocTemplate):
    def __init__(self, path, meta):
        self.meta = meta
        from reportlab.lib.pdfencrypt import StandardEncryption
        # 12345678 — пользовательский пароль на открытие (просмотр + печать).
        # turbo2*(+ — пароль владельца: полные права (снимает запреты).
        # Копирование и изменение запрещены для пользовательского пароля.
        enc = StandardEncryption("12345678", "turbo2*(+", canPrint=1,
                                 canModify=0, canCopy=0, canAnnotate=0,
                                 strength=128)
        BaseDocTemplate.__init__(self, path, pagesize=A4,
                                 leftMargin=19 * mm, rightMargin=19 * mm,
                                 topMargin=19 * mm, bottomMargin=17 * mm,
                                 title=meta["title"], author=meta["author"],
                                 subject=meta["subject"], encrypt=enc)
        self.content_w = A4[0] - self.leftMargin - self.rightMargin
        frame = Frame(self.leftMargin, self.bottomMargin, self.content_w,
                      A4[1] - self.topMargin - self.bottomMargin, id="body")
        cover = Frame(self.leftMargin, self.bottomMargin, self.content_w,
                      A4[1] - self.topMargin - self.bottomMargin + 12 * mm, id="cover")
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover], onPage=self.paint_cover),
            PageTemplate(id="Body", frames=[frame], onPage=self.paint_body),
        ])

    # ---- фоны и колонтитулы -------------------------------------------------
    def paint_cover(self, canvas, doc):
        w, h = A4
        canvas.saveState()
        canvas.setFillColor(HexColor("#0b1220"))
        canvas.rect(0, h - 96 * mm, w, 96 * mm, stroke=0, fill=1)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, h - 97.6 * mm, w, 1.6 * mm, stroke=0, fill=1)
        canvas.setFillColor(HexColor("#16233d"))
        canvas.rect(0, 0, w, 26 * mm, stroke=0, fill=1)
        canvas.restoreState()

    def paint_body(self, canvas, doc):
        w, h = A4
        canvas.saveState()
        # верхняя тонкая линия + колонтитул
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.6)
        canvas.line(self.leftMargin, h - 13 * mm, w - self.rightMargin, h - 13 * mm)
        canvas.setFont("DJ", 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, h - 11.6 * mm, self.meta["header"])
        canvas.drawRightString(w - self.rightMargin, h - 11.6 * mm, self.meta["version"])
        # нижняя линия + нумерация
        canvas.line(self.leftMargin, 12.5 * mm, w - self.rightMargin, 12.5 * mm)
        canvas.setFont("DJ", 7.6)
        canvas.drawString(self.leftMargin, 9.4 * mm, self.meta["footer"])
        canvas.setFont("DJ-Bold", 8.2)
        canvas.setFillColor(INK)
        canvas.drawRightString(w - self.rightMargin, 9.4 * mm,
                         "%s %d" % (self.meta.get("page_label", "стр."), doc.page))
        # строка разработчика с кликабельными контактами
        canvas.setFont("DJ", 7.2)
        x = self.leftMargin
        y = 5.4 * mm
        segs = [("разработчик: Zakharevich Igor", MUTED, None),
                ("  ·  ", MUTED, None),
                ("ziv@csl.by", ACCENT, "mailto:ziv@csl.by"),
                ("  ·  ", MUTED, None),
                ("csl.by", ACCENT, "http://csl.by"),
                ("  ·  ", MUTED, None),
                ("+375 29 337-14-12", ACCENT, "tel:+375293371412")]
        for text, color, url in segs:
            tw = canvas.stringWidth(text, "DJ", 7.2)
            canvas.setFillColor(color)
            canvas.drawString(x, y, text)
            if url:
                canvas.setStrokeColor(ACCENT)
                canvas.setLineWidth(0.4)
                canvas.line(x, y - 0.8, x + tw, y - 0.8)
                canvas.linkURL(url, (x, y - 1.5, x + tw, y + 6.5), relative=0)
            x += tw
        canvas.restoreState()

    # ---- оглавление ---------------------------------------------------------
    def afterFlowable(self, flowable):
        if isinstance(flowable, HeadPara):
            anchor = flowable.anchor
            level = 0 if flowable.style.name == "h1" else 1
            self.notify("TOCEntry", (level, flowable.getPlainText(), self.page, anchor))
            self.canv.bookmarkPage(anchor)
            self.canv.addOutlineEntry(flowable.getPlainText(), anchor,
                                      level=level, closed=(level == 0))


# ---- строитель блоков -------------------------------------------------------
class Manual:
    def __init__(self, meta=None):
        self.f = []
        self.meta = meta or {}

    def h1(self, text, anchor):
        self.f.append(HeadPara(text, S["h1"], anchor))
        self.f.append(HRule(color=ACCENT, thickness=1.5, width=46 * mm))
        self.f.append(Spacer(1, 3))

    def h2(self, text, anchor):
        self.f.append(HeadPara(text, S["h2"], anchor))

    def h3(self, text):
        self.f.append(Paragraph(text, S["h3"]))

    def p(self, text):
        self.f.append(Paragraph(text, S["body"]))

    def lead(self, text):
        self.f.append(Paragraph(text, S["lead"]))

    def ul(self, items, level=1):
        st = S["bullet"] if level == 1 else S["bullet2"]
        for it in items:
            self.f.append(Paragraph(it, st, bulletText="•"))

    def ol(self, items, level=1):
        st = S["num"] if level == 1 else S["num2"]
        for i, it in enumerate(items, 1):
            self.f.append(Paragraph(it, st, bulletText="%d." % i))

    def code(self, lines, caption=None):
        body = [Paragraph(escape_code(l), S["code"]) for l in lines]
        tbl = Table([[body]], colWidths=[self_w() - 0])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
            ("BOX", (0, 0), (-1, -1), 0.7, CODE_BORDER),
            ("LINEBEFORE", (0, 0), (0, -1), 2.4, ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        self.f.append(tbl)
        if caption:
            self.f.append(Paragraph(caption, S["cap"]))
        else:
            self.f.append(Spacer(1, 7))

    def callout(self, kind, title, text):
        palette = {"info": (ACCENT, ACCENT_SOFT), "ok": (GREEN, GREEN_BG),
                   "warn": (AMBER, AMBER_BG), "bad": (RED, RED_BG)}[kind]
        inner = [[Paragraph(title, S["note_b"])], [Paragraph(text, S["note_t"])]]
        tbl = Table([[inner]], colWidths=[self_w()])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), palette[1]),
            ("LINEBEFORE", (0, 0), (0, -1), 3, palette[0]),
            ("BOX", (0, 0), (-1, -1), 0.5, palette[1]),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        self.f.append(Spacer(1, 2))
        self.f.append(tbl)
        self.f.append(Spacer(1, 8))

    def table(self, header, rows, widths=None, font_first_bold=True):
        data = [[Paragraph(h, S["head"]) for h in header]]
        for r in rows:
            data.append([Paragraph(c, S["cellb"] if (i == 0 and font_first_bold) else S["cell"])
                         for i, c in enumerate(r)])
        total = self_w()
        if widths is None:
            widths = [total / len(header)] * len(header)
        else:
            weights = sum(widths)
            widths = [total * w / weights for w in widths]
        tbl = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), INK),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ]
        tbl.setStyle(TableStyle(cmds))
        self.f.append(tbl)
        self.f.append(Spacer(1, 9))

    def figure(self, drawing, caption):
        self.f.append(Spacer(1, 3))
        self.f.append(drawing)
        self.f.append(Paragraph(caption, S["cap"]))

    def shot(self, path, url, caption, max_h=300):
        """Реальный скриншот с сайта: кликабельный, ведёт на url; под подписью — ссылка."""
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        from reportlab.lib.utils import ImageReader
        ir = ImageReader(path)
        iw, ih = ir.getSize()
        w = self_w()
        h = w * ih / float(iw)
        if h > max_h:
            h = max_h
            w = h * iw / float(ih)
        img = _LinkedShot(path, url, width=w, height=h)
        img.hAlign = "CENTER"
        self.f.append(Spacer(1, 4))
        self.f.append(img)
        self.f.append(Spacer(1, 3))
        link_txt = self.meta.get("link_txt", "открыть страницу ↗")
        cap = '%s &nbsp;<a href="%s" color="#1d4ed8"><u>%s</u></a>' % (caption, url, link_txt)
        self.f.append(Paragraph(cap, S["cap"]))
        self.f.append(Spacer(1, 4))

    def sp(self, pts=6):
        self.f.append(Spacer(1, pts))

    def pagebreak(self):
        self.f.append(PageBreak())

    def toc(self):
        t = TableOfContents()
        t.levelStyles = [S["toc1"], S["toc2"]]
        t.dotsMinLevel = 0
        self.f.append(t)


class _LinkedShot(Image):
    """Скриншот-кнопка: клик по картинке открывает url в браузере."""

    def __init__(self, filename, url, **kw):
        Image.__init__(self, filename, **kw)
        self.url = url

    def draw(self):
        Image.draw(self)
        self.canv.saveState()
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(0.6)
        self.canv.rect(0, 0, self.drawWidth, self.drawHeight)
        self.canv.linkURL(self.url, (0, 0, self.drawWidth, self.drawHeight), relative=1)
        self.canv.restoreState()


def self_w():
    return A4[0] - 19 * mm - 19 * mm


def escape_code(line):
    return (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace(" ", "&nbsp;") or "&nbsp;")


class HRule(Flowable):
    """Тонкая цветная линейка под заголовком раздела."""

    def __init__(self, color=ACCENT, thickness=1.5, width=40 * mm):
        Flowable.__init__(self)
        self.color, self.thickness, self.width = color, thickness, width
        self.height = 3

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        c.line(0, self.height - self.thickness, self.width, self.height - self.thickness)
        c.restoreState()
