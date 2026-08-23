#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build an academic-styled English PDF from 04_Paper_FINAL.md (reportlab Platypus pipeline)."""
import re, sys
from html.parser import HTMLParser
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable)

SRC = r"D:\github projects\personal_clone_repo\Macha_Research\04_Paper_FINAL.md"
OUT = r"D:\github projects\personal_clone_repo\Macha_Research\The_Relational_Gap_Paper.pdf"

# --- font families so <b>/<i> work with built-in fonts -----------------------------
for fam, n, b, i, bi in [
    ("Times", "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"),
    ("Helvetica", "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"),
    ("Courier", "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique"),
]:
    registerFontFamily(fam, normal=n, bold=b, italic=i, boldItalic=bi)

# --- glyph safety: built-in fonts are WinAnsi --------------------------------------
WINANSI_OK = set(chr(c) for c in range(0x20, 0x7F)) | set(
    "\u00a0\u00a7\u00b7\u00d7\u00e7\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u20ac"
    "\u00a1\u00bf\u00e9\u00e8\u00ea\u00e0\u00e2\u00ee\u00f4\u00fb\u00fc\u00f6\u00e4"
    "\u00eb\u00ef\u00f1\u00b0\u00b1\u00bd\u00bc\u00be\u00a2\u00a3\u00a5\u00a6\u00ab"
    "\u00bb\u00a9\u00ae\u2122\u00ad\u00b4\u00a8\u02dc\u02c6\u00b2\u00b3\u00b9\u00a4"
    "\u00aa\u00ba\u00c6\u00e6\u0152\u0153\u00c0\u00c1\u00c2\u00c3\u00c4\u00c5\u00c7"
    "\u00c8\u00c9\u00ca\u00cb\u00cc\u00cd\u00ce\u00cf\u00d0\u00d1\u00d2\u00d3\u00d4"
    "\u00d5\u00d6\u00d8\u00d9\u00da\u00db\u00dc\u00dd\u00de\u00df\u00e1\u00e2\u00e3"
    "\u00e5\u00e6\u00e7\u00e8\u00e9\u00ea\u00eb\u00ec\u00ed\u00ee\u00ef\u00f0\u00f2"
    "\u00f3\u00f4\u00f5\u00f6\u00f8\u00f9\u00fa\u00fb\u00fc\u00fd\u00fe\u00ff")

text = open(SRC, encoding="utf-8").read()
bad = sorted({ch for ch in text if ord(ch) > 127 and ch not in WINANSI_OK})
if bad:
    sys.exit("FATAL: glyphs not renderable by built-in fonts: " + " ".join(f"U+{ord(c):04X}" for c in bad))

# --- strip front matter; keep title/subtitle/meta for a custom header ---------------
m = re.match(r"^# (.+?)\n## (.+?)\n\n\*\*(.+?)\*\*\n\*(.+?)\*\n\n---\n", text, re.S)
if m:
    title, subtitle, meta, note = m.groups()
    body = text[m.end():]
else:
    title, subtitle, meta, note = "The Relational Gap", "", "", ""
    body = text

html_body = markdown.markdown(body, extensions=["extra"])

# --- markdown HTML -> reportlab paragraph markup ------------------------------------
def rl_inline(s):
    s = s.replace("<sup>", "<super>").replace("</sup>", "</super>")
    s = re.sub(r"<code>(.*?)</code>", lambda mm: '<font face="Courier">' + mm.group(1) + "</font>", s, flags=re.S)
    return s

class Flow(HTMLParser):
    BLOCK = {"h1", "h2", "h3", "h4", "p", "blockquote", "hr", "pre"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.flow = []                 # final flowables (strings / specials)
        self.cur = []                  # inline buffer of current block
        self.inline_depth = 0          # inside p/h/li/bq: capture data
        self.bq_depth = 0
        self.list_stack = []           # ('ul'|'ol', [items])
        self.cur_item = None
        self.block_kind = None         # kind of the inline block being collected
    def _push(self):
        if self.inline_depth == 0:
            self.inline_depth = 1
    def _flush(self):
        if self.cur:
            txt = re.sub(r"[ \t]+", " ", "".join(self.cur)).strip()
            self.cur = []
            return txt
        return None
    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t == "li":
            if self.cur_item is not None:
                self.list_stack[-1][1].append(self._flush())
            self.cur_item = True
            self._push(); return
        if t in ("ul", "ol"):
            self.list_stack.append([t, []])
            self.cur_item = None
            return
        if t == "blockquote":
            self.bq_depth += 1; self._push(); return
        if t == "hr":
            self.flow.append(("hr", None)); return
        if t in ("h1", "h2", "h3", "h4"):
            self.block_kind = t; self._push(); return
        if t == "p":
            if self.bq_depth == 0 and not self.list_stack:
                self.block_kind = t
            self._push(); return
        if t == "em":   self.cur.append("<i>");   self._push(); return
        if t == "strong": self.cur.append("<b>"); self._push(); return
        if t == "sub":  self.cur.append("<sub>"); self._push(); return
        if t == "sup":  self.cur.append("<super>"); self._push(); return
        if t == "code": self.cur.append('<font face="Courier">'); self._push(); return
        if t == "br":   self.cur.append("<br/>"); return
        # ignore unknown tags but still capture their text
        self._push()
    def handle_endtag(self, tag):
        t = tag.lower()
        if t in ("em",): self.cur.append("</i>"); return
        if t == "strong": self.cur.append("</b>"); return
        if t == "sub":  self.cur.append("</sub>"); return
        if t == "sup":  self.cur.append("</super>"); return
        if t == "code": self.cur.append("</font>"); return
        if t == "blockquote":
            self.bq_depth -= 1
            txt = self._flush()
            if txt is not None:
                self.flow.append(("bq", txt))
            return
        if t in ("li",):
            if self.list_stack and self.cur_item is not None:
                self.list_stack[-1][1].append(self._flush())
                self.cur_item = None
            return
        if t in ("ul", "ol"):
            if self.list_stack:
                kind, items = self.list_stack.pop()
                items = [it for it in items if it]
                self.flow.append(("list", (kind, items)))
            return
        if t in ("h1", "h2", "h3", "h4", "p"):
            if t == "p" and (self.bq_depth > 0 or self.list_stack):
                return  # absorbed by parent container (blockquote / list item)
            txt = self._flush()
            if txt:
                self.flow.append((self.block_kind or t, txt))
            self.block_kind = None
            return
        if t == "pre":
            return
    def handle_data(self, data):
        if not self.inline_depth:
            return
        data = data.replace("\n", " ")
        data = data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.cur.append(data)

f = Flow()
f.feed(html_body)
f.close()
if f.cur_item is not None and f.list_stack:
    f.list_stack[-1][1].append(f._flush())
if f.cur and f._flush() is not None:  # trailing text safety
    pass

# --- styles -------------------------------------------------------------------------
BLACK = colors.HexColor("#111111")
GRAY = colors.HexColor("#444444")
st_title   = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=21, leading=25,
                            alignment=TA_CENTER, textColor=BLACK, spaceAfter=6)
st_sub     = ParagraphStyle("sub", fontName="Helvetica-Bold", fontSize=13, leading=17,
                            alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=12)
st_meta    = ParagraphStyle("meta", fontName="Helvetica", fontSize=9.5, leading=13,
                            alignment=TA_CENTER, textColor=GRAY, spaceAfter=2)
st_note    = ParagraphStyle("note", fontName="Times-Italic", fontSize=9.5, leading=13.5,
                            alignment=TA_JUSTIFY, textColor=GRAY, spaceBefore=6, spaceAfter=2)
st_h2      = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                            spaceBefore=15, spaceAfter=6, keepWithNext=1, textColor=BLACK)
st_h3      = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                            spaceBefore=10, spaceAfter=4, keepWithNext=1, textColor=colors.HexColor("#222222"))
st_body    = ParagraphStyle("body", fontName="Times", fontSize=10.5, leading=15,
                            alignment=TA_JUSTIFY, spaceAfter=7, textColor=BLACK)
st_bq      = ParagraphStyle("bq", parent=st_body, fontName="Times-Italic",
                            leftIndent=22, rightIndent=18, textColor=colors.HexColor("#222222"),
                            spaceBefore=6, spaceAfter=8)
st_li      = ParagraphStyle("li", parent=st_body, spaceAfter=3)

def build_flowables():
    out = []
    out.append(Paragraph(title, st_title))
    if subtitle:
        out.append(Paragraph(subtitle, st_sub))
    if meta:
        out.append(Paragraph(meta, st_meta))
    if note:
        out.append(Paragraph(note, st_note))
    out.append(Spacer(1, 8))
    out.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#BBBBBB"),
                          spaceBefore=4, spaceAfter=12))
    for kind, content in f.flow:
        if kind == "hr":
            out.append(HRFlowable(width="100%", thickness=0.8,
                                  color=colors.HexColor("#BBBBBB"), spaceBefore=8, spaceAfter=10))
        elif kind == "h2":
            out.append(Paragraph(rl_inline(content), st_h2))
        elif kind == "h3":
            out.append(Paragraph(rl_inline(content), st_h3))
        elif kind == "p":
            out.append(Paragraph(rl_inline(content), st_body))
        elif kind == "list":
            k, items = content
            for idx, it in enumerate(items, 1):
                prefix = ("%d. " % idx) if k == "ol" else "\u2022 "
                li = ParagraphStyle("li", parent=st_body, leftIndent=18,
                                    firstLineIndent=-18, spaceAfter=3)
                out.append(Paragraph(rl_inline(prefix + it), li))
        elif kind == "bq":
            out.append(Paragraph(rl_inline(content), st_bq))
    return out

def footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("The Relational Gap: What Players Actually Want from an Intelligent NPC")
    canvas.setAuthor("Macha Research Program")
    canvas.setSubject("Player-NPC relationship; relational gap; NPC architecture")
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawCentredString(A4[0] / 2.0, 1.1 * cm, "Page %d" % doc.page)
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2.0 * cm, rightMargin=2.0 * cm,
                        topMargin=2.2 * cm, bottomMargin=2.4 * cm,
                        title="The Relational Gap: What Players Actually Want from an Intelligent NPC",
                        author="Macha Research Program")
doc.build(build_flowables(), onFirstPage=footer, onLaterPages=footer)
print("OK ->", OUT)
