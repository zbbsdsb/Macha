"""Macha recruitment PDF — design system.

A small canvas-level layout engine. Deliberately built on raw ReportLab canvas
rather than Platypus: the specification calls for a strict Swiss grid with
technical annotations, and flowable auto-layout would fight that.

Design position: early-stage research laboratory document. Typography-driven,
monochrome with one annotation accent, hairline rules, generous whitespace,
large page numbers, no gradients, no decorative iconography.

Core capabilities
-----------------
* A4 page with a 6-column grid and a 12 pt baseline unit.
* Mixed-script typesetting: Latin runs use Inter / Inter Display, Han runs use
  Noto Sans SC. ReportLab has no font fallback, so runs are resolved per
  character against each face's real cmap.
* Annotation vocabulary: leader-dot rows, tracking mono labels, index gutters,
  rating squares, hairline rules.
* Vector diagram primitives (arrows and nodes are drawn, never set as glyphs,
  so the output does not depend on which symbols a font happens to contain).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as PDFTTFont

# --------------------------------------------------------------------------
# Page geometry — A4
# --------------------------------------------------------------------------

PAGE_W, PAGE_H = 595.276, 841.89

MARGIN_L = 44.0
MARGIN_R = 44.0
MARGIN_T = 42.0
MARGIN_B = 50.0

CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
COLUMNS = 6
GUTTER = 12.0
COL_W = (CONTENT_W - GUTTER * (COLUMNS - 1)) / COLUMNS

BASELINE = 12.0

FRAME_TOP_RULE = PAGE_H - MARGIN_T
FRAME_TOP_TEXT = FRAME_TOP_RULE - 10.5
CONTENT_TOP = FRAME_TOP_RULE - 34.0
FRAME_BOT_RULE = MARGIN_B
FRAME_BOT_TEXT = FRAME_BOT_RULE - 11.0
CONTENT_BOTTOM = FRAME_BOT_RULE + 18.0


def col_x(i: int) -> float:
    """Left edge of column *i* (0-based)."""
    return MARGIN_L + i * (COL_W + GUTTER)


def span_w(n: int) -> float:
    """Width of a span covering *n* columns."""
    return n * COL_W + (n - 1) * GUTTER


def span_x(i: int, j: int) -> tuple[float, float]:
    """(x, width) for the span from column *i* to column *j* inclusive."""
    return col_x(i), col_x(j) + COL_W - col_x(i)


# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

PAPER = HexColor("#FBFAF7")
INK = HexColor("#131211")
INK_2 = HexColor("#57544C")
INK_3 = HexColor("#918D84")
RULE = HexColor("#DAD5CA")
RULE_SOFT = HexColor("#E9E5DC")
ACCENT = HexColor("#C2391A")
ACCENT_SOFT = HexColor("#F1DED7")
TINT = HexColor("#EFECE4")
TINT_DARK = HexColor("#E2DED4")


def ink_alpha(alpha: float) -> Color:
    """Paper-blended ink, for tints that must sit under type."""
    return Color(
        PAPER.red + (INK.red - PAPER.red) * alpha,
        PAPER.green + (INK.green - PAPER.green) * alpha,
        PAPER.blue + (INK.blue - PAPER.blue) * alpha,
    )


# --------------------------------------------------------------------------
# Type scale
# --------------------------------------------------------------------------
#
# Sizes are given in points as (size, leading, tracking). Tracking is extra
# character spacing; display sizes carry negative tracking, annotation labels
# carry positive tracking. Han text gets a larger size and much looser leading
# because dense ideographs need more air than Latin lowercase.


@dataclass(frozen=True)
class TextStyle:
    size: float
    leading: float
    tracking: float = 0.0
    weight: str = "regular"      # regular | medium | semibold | bold
    family: str = "text"         # text | display | mono


SCALE = {
    "en": {
        "cover_title": TextStyle(46, 48, -1.15, "semibold", "display"),
        "cover_sub": TextStyle(13.2, 18, 0.0, "regular", "text"),
        "page_title": TextStyle(29, 32, -0.5, "medium", "display"),
        "page_sub": TextStyle(11.4, 15, 0.15, "regular", "text"),
        "section": TextStyle(10.0, 13, 0.75, "semibold", "text"),
        "lead": TextStyle(13.0, 18.5, -0.05, "regular", "text"),
        "body": TextStyle(9.2, 14.2, 0.0, "regular", "text"),
        "body_m": TextStyle(9.2, 14.2, 0.0, "medium", "text"),
        "small": TextStyle(8.1, 12.4, 0.0, "regular", "text"),
        "item": TextStyle(8.1, 15.0, 0.0, "regular", "text"),
        "micro": TextStyle(7.1, 10.6, 0.0, "regular", "text"),
        "mono": TextStyle(6.9, 10.6, 0.62, "regular", "mono"),
        "mono_m": TextStyle(6.9, 10.6, 0.62, "medium", "mono"),
        "mono_s": TextStyle(6.1, 9.6, 0.5, "regular", "mono"),
        "mono_write": TextStyle(7.4, 12.0, 0.1, "regular", "mono"),
        "quote": TextStyle(12.2, 17.5, -0.05, "regular", "text"),
        "num": TextStyle(15.5, 16, -0.2, "medium", "display"),
    },
    "zh": {
        "cover_title": TextStyle(44, 49, -1.0, "semibold", "display"),
        "cover_sub": TextStyle(13.0, 20, 0.0, "regular", "text"),
        "page_title": TextStyle(28, 33, -0.4, "medium", "display"),
        "page_sub": TextStyle(11.6, 18, 0.1, "regular", "text"),
        "section": TextStyle(10.2, 15, 0.6, "semibold", "text"),
        "lead": TextStyle(13.4, 22.0, 0.0, "regular", "text"),
        "body": TextStyle(9.8, 17.2, 0.0, "regular", "text"),
        "body_m": TextStyle(9.8, 17.2, 0.0, "medium", "text"),
        "small": TextStyle(8.8, 15.0, 0.0, "regular", "text"),
        "item": TextStyle(8.8, 15.6, 0.0, "regular", "text"),
        "micro": TextStyle(7.8, 13.0, 0.0, "regular", "text"),
        "mono": TextStyle(7.2, 11.6, 0.4, "regular", "mono"),
        "mono_m": TextStyle(7.2, 11.6, 0.4, "medium", "mono"),
        "mono_s": TextStyle(6.4, 10.4, 0.3, "regular", "mono"),
        "mono_write": TextStyle(7.6, 12.4, 0.0, "regular", "mono"),
        "quote": TextStyle(12.6, 21.0, 0.0, "regular", "text"),
        "num": TextStyle(15.5, 16, -0.2, "medium", "display"),
    },
}

# CJK-aware leading multipliers applied on top of the base leading when a
# paragraph mixes scripts: Han glyphs need more vertical room at the same size.
HAN_LEAD_BONUS = 1.0


# --------------------------------------------------------------------------
# Font registration and mixed-script resolution
# --------------------------------------------------------------------------

FONT_FILES = {
    ("text", "regular"): "Inter-Regular.ttf",
    ("text", "medium"): "Inter-Medium.ttf",
    ("text", "semibold"): "Inter-SemiBold.ttf",
    ("text", "bold"): "Inter-Bold.ttf",
    ("display", "regular"): "InterDisplay-Regular.ttf",
    ("display", "medium"): "InterDisplay-Medium.ttf",
    ("display", "semibold"): "InterDisplay-SemiBold.ttf",
    ("display", "bold"): "InterDisplay-Bold.ttf",
    ("mono", "regular"): "IBMPlexMono-Regular.ttf",
    ("mono", "medium"): "IBMPlexMono-Medium.ttf",
    ("mono", "semibold"): "IBMPlexMono-SemiBold.ttf",
    ("mono", "bold"): "IBMPlexMono-Bold.ttf",
}

CJK_FILES = {
    "regular": "NotoSansSC-Regular.ttf",
    "medium": "NotoSansSC-Medium.ttf",
    "semibold": "NotoSansSC-Bold.ttf",
    "bold": "NotoSansSC-Bold.ttf",
}

_PS_NAMES: dict[tuple[str, str], str] = {}
_CJK_NAMES: dict[str, str] = {}
_CMAPS: dict[str, set[int]] = {}

# Ranges that must always go through the Han face, even if the Latin face
# happens to carry the codepoint.
_HAN_RANGES = (
    (0x2E80, 0x2EFF),    # CJK radicals
    (0x3000, 0x303F),    # CJK punctuation
    (0x3040, 0x30FF),    # kana
    (0x3400, 0x4DBF),    # ext A
    (0x4E00, 0x9FFF),    # unified
    (0xF900, 0xFAFF),    # compatibility
    (0xFE30, 0xFE4F),    # vertical forms
    (0xFF00, 0xFFEF),    # fullwidth forms
    (0x20000, 0x2FA1F),  # ext B+
)


def is_han(cp: int) -> bool:
    return any(lo <= cp <= hi for lo, hi in _HAN_RANGES)


def register_fonts(font_dir: Path) -> None:
    """Register every face once, and cache its cmap for run resolution."""
    if _PS_NAMES:
        return

    for (family, weight), filename in FONT_FILES.items():
        ps = f"Macha-{family}-{weight}"
        path = font_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"missing font: {path}  (run prepare_fonts.py)")
        pdfmetrics.registerFont(PDFTTFont(ps, str(path)))
        _PS_NAMES[(family, weight)] = ps
        _CMAPS[ps] = set(TTFont(str(path)).getBestCmap().keys())

    for weight, filename in CJK_FILES.items():
        ps = f"Macha-han-{weight}"
        path = font_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"missing font: {path}  (run prepare_fonts.py)")
        if ps not in _CMAPS:
            pdfmetrics.registerFont(PDFTTFont(ps, str(path)))
            _CMAPS[ps] = set(TTFont(str(path)).getBestCmap().keys())
        _CJK_NAMES[weight] = ps


@dataclass(frozen=True)
class Run:
    text: str
    font: str


def base_font_name() -> str:
    """An embedded face to install as ReportLab's canvas base font.

    ReportLab's default base font is Helvetica, which ships as a declared but
    unembedded resource even when nothing uses it. Pointing the base font at one
    of our own registered faces removes that from the output.
    """
    return _PS_NAMES[("text", "regular")]


def face_for(style: TextStyle) -> str:
    return _PS_NAMES[(style.family, style.weight)]


def _has(font: str, cp: int) -> bool:
    return cp in _CMAPS.get(font, ())


def resolve(text: str, style: TextStyle) -> list[Run]:
    """Split *text* into runs of Latin and Han, choosing a face per character."""
    latin = face_for(style)
    han = _CJK_NAMES[style.weight]
    runs: list[Run] = []
    buf: list[str] = []
    current = None

    for ch in text:
        cp = ord(ch)
        if ch in ("\u200b",):
            continue
        if is_han(cp):
            target = han
        elif _has(latin, cp):
            target = latin
        else:
            target = han if _has(han, cp) else latin
        if target != current:
            if buf:
                runs.append(Run("".join(buf), current))
            buf, current = [ch], target
        else:
            buf.append(ch)
    if buf:
        runs.append(Run("".join(buf), current))
    return runs


def run_width(runs: list[Run], size: float) -> float:
    return sum(pdfmetrics.stringWidth(r.text, r.font, size) for r in runs)


def text_width(text: str, style: TextStyle, tracking: float | None = None) -> float:
    runs = resolve(text, style)
    tr = style.tracking if tracking is None else tracking
    return run_width(runs, style.size) + tr * max(0, len(text) - 1)


# --------------------------------------------------------------------------
# Wrapping
# --------------------------------------------------------------------------

_NO_BREAK_BEFORE = set("，。、；：？！）》」』】〉·%,.;:?!)]}»″’")
_NO_BREAK_AFTER = set("（《「『【〈([{«‘“")


def _tokens(text: str) -> list[str]:
    """Split into wrap units: Han chars break individually, Latin by word."""
    out: list[str] = []
    buf: list[str] = []
    for ch in text:
        if ch == " ":
            if buf:
                out.append("".join(buf))
                buf = []
            out.append(" ")
        elif is_han(ord(ch)):
            if buf:
                out.append("".join(buf))
                buf = []
            out.append(ch)
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def wrap(text: str, style: TextStyle, width: float, tracking: float | None = None) -> list[str]:
    """Greedy wrap honouring both Latin word boundaries and Han per-char breaks."""
    tr = style.tracking if tracking is None else tracking
    lines: list[str] = []
    for hard in text.split("\n"):
        if not hard:
            lines.append("")
            continue
        line = ""
        for tok in _tokens(hard):
            candidate = line + tok
            if line and text_width(candidate.rstrip(), style, tr) > width:
                if tok == " ":
                    lines.append(line)
                    line = ""
                else:
                    lines.append(line.rstrip())
                    line = "" if tok == " " else tok
            else:
                line = candidate
        lines.append(line.rstrip())
    return lines


# --------------------------------------------------------------------------
# Document wrapper
# --------------------------------------------------------------------------


class Doc:
    """Canvas plus the layout vocabulary used by the page compositions."""

    def __init__(self, canvas, lang: str = "en"):
        self.c = canvas
        self.lang = lang
        self.tokens = SCALE[lang]
        # Lowest y reached by page content, for fill-balance diagnostics.
        # Page furniture is excluded: page_frame resets this after drawing.
        self.min_y = CONTENT_TOP

    def _track(self, y: float) -> None:
        if y < self.min_y:
            self.min_y = y

    # -- style helpers ----------------------------------------------------

    def style(self, key: str) -> TextStyle:
        return self.tokens[key]

    # -- colour helpers ---------------------------------------------------

    def fill(self, color) -> None:
        self.c.setFillColor(color)

    def stroke(self, color, width: float = 0.5) -> None:
        self.c.setStrokeColor(color)
        self.c.setLineWidth(width)

    # -- primitives -------------------------------------------------------

    def hrule(self, x1: float, x2: float, y: float, color=RULE, width: float = 0.5) -> None:
        self.stroke(color, width)
        self.c.line(x1, y, x2, y)
        self._track(y)

    def vrule(self, x: float, y1: float, y2: float, color=RULE, width: float = 0.5) -> None:
        self.stroke(color, width)
        self.c.line(x, y1, x, y2)
        self._track(min(y1, y2))

    def square(self, x: float, y: float, size: float, color=INK, filled: bool = True) -> None:
        self._track(y)
        if filled:
            self.fill(color)
            self.c.rect(x, y, size, size, stroke=0, fill=1)
        else:
            self.stroke(color, 0.5)
            self.c.rect(x, y, size, size, stroke=1, fill=0)

    def _line_text_object(self, x: float, y: float, runs: list[Run], style: TextStyle,
                          color, tracking: float) -> None:
        """One text object per line so glyph advances (incl. tracking) are the PDF's."""
        self._track(y)
        obj = self.c.beginText(x, y)
        obj.setFillColor(color)
        obj.setCharSpace(tracking)
        for run in runs:
            obj.setFont(run.font, style.size)
            obj.textOut(run.text)
        self.c.drawText(obj)

    def text(
        self,
        x: float,
        y: float,
        s: str,
        style: TextStyle,
        color=INK,
        tracking: float | None = None,
        align: str = "left",
        width: float | None = None,
    ) -> float:
        """Draw a single line of mixed-script text. Returns the advance width."""
        if not s:
            return 0.0
        tr = style.tracking if tracking is None else tracking
        runs = resolve(s, style)
        w = run_width(runs, style.size) + tr * max(0, len(s) - 1)
        if align == "right" and width is not None:
            x = x + width - w
        elif align == "center" and width is not None:
            x = x + (width - w) / 2
        self._line_text_object(x, y, runs, style, color, tr)
        return w

    def paragraph(
        self,
        x: float,
        y: float,
        text: str,
        style: TextStyle,
        color=INK,
        width: float | None = None,
        max_lines: int | None = None,
    ) -> float:
        """Draw wrapped text.

        Returns the baseline slot for the line *after* the last one, so that
        sequential blocks compose additively. Every spacing constant in the page
        compositions assumes this convention.
        """
        width = CONTENT_W if width is None else width
        lines = wrap(text, style, width)
        if max_lines is not None:
            lines = lines[:max_lines]
        cursor = y
        for line in lines:
            if line:
                self.text(x, cursor, line, style, color)
            cursor -= style.leading
        return cursor

    def para_lines(self, text: str, style: TextStyle, width: float) -> list[str]:
        return wrap(text, style, width)
    def label(
        self,
        x: float,
        y: float,
        s: str,
        style: TextStyle | None = None,
        color=INK_2,
        tick: bool = False,
        tick_color=ACCENT,
    ) -> float:
        """Mono annotation label, optionally prefixed by an accent tick."""
        style = style or self.style("mono")
        if tick:
            self.square(x, y + style.size * 0.30, 3.1, tick_color, True)
            x += 7.5
        return self.text(x, y, s, style, color)

    def leader_row(
        self,
        x: float,
        y: float,
        left: str,
        right: str,
        width: float,
        style: TextStyle | None = None,
        color=INK,
        right_color=INK,
        dot_color=RULE,
        right_style: TextStyle | None = None,
    ) -> None:
        """Label ......... value — the technical-document leader-dot row."""
        style = style or self.style("body")
        right_style = right_style or style
        lw = self.text(x, y, left, style, color)
        rw = text_width(right, right_style)
        gap_start = x + lw + 5.0
        gap_end = x + width - rw - 5.0
        if gap_end > gap_start:
            self.dotted_line(gap_start, gap_end, y + style.size * 0.30, dot_color)
        self.text(x + width - rw, y, right, right_style, right_color)

    def dotted_line(self, x1: float, x2: float, y: float, color=RULE, gap: float = 4.2, r: float = 0.4) -> None:
        self.fill(color)
        self._track(y)
        span = x2 - x1
        if span <= 0:
            return
        n = max(1, int(span // gap))
        step = span / n
        for i in range(n + 1):
            self.c.circle(x1 + i * step, y, r, stroke=0, fill=1)

    def rating(self, x: float, y: float, filled: int, total: int = 5, size: float = 5.0, gap: float = 2.6) -> float:
        for i in range(total):
            self.square(x + i * (size + gap), y, size, INK if i < filled else RULE, i < filled)
        return total * size + (total - 1) * gap

    def arrow_down(self, x: float, y_top: float, y_bot: float, color=INK, width: float = 0.6, head: float = 3.4) -> None:
        self.stroke(color, width)
        self.c.line(x, y_top, x, y_bot + head)
        self._head(x, y_bot, head, -90, color)

    def arrow_up(self, x: float, y_bot: float, y_top: float, color=INK, width: float = 0.6, head: float = 3.4) -> None:
        self.stroke(color, width)
        self.c.line(x, y_bot, x, y_top - head)
        self._head(x, y_top, head, 90, color)

    def arrow_right(self, x1: float, x2: float, y: float, color=INK, width: float = 0.6, head: float = 3.4) -> None:
        self.stroke(color, width)
        self.c.line(x1, y, x2 - head, y)
        self._head(x2, y, head, 0, color)

    def _head(self, x: float, y: float, size: float, angle_deg: float, color) -> None:
        self._track(y)
        a = math.radians(angle_deg)
        path = self.c.beginPath()
        for offset in (150, -150):
            b = a + math.radians(offset)
            path.moveTo(x, y)
            path.lineTo(x + size * math.cos(b), y + size * math.sin(b))
        path.close()
        self.fill(color)
        self.c.drawPath(path, stroke=0, fill=1)

    # -- page furniture ---------------------------------------------------

    def page_frame(
        self,
        page_no: int,
        total: int,
        section: str,
        footer_left: str,
        footer_right: str,
    ) -> None:
        """Top and bottom furniture. Identical on every interior page."""
        mono = self.style("mono")
        mono_s = self.style("mono_s")

        self.hrule(MARGIN_L, PAGE_W - MARGIN_R, FRAME_TOP_RULE, RULE)
        self.text(MARGIN_L, FRAME_TOP_TEXT, section, mono, INK_2)
        self.text(
            MARGIN_L,
            FRAME_TOP_TEXT,
            f"{page_no:02d} / {total:02d}",
            mono,
            INK,
            align="right",
            width=CONTENT_W,
        )

        self.hrule(MARGIN_L, PAGE_W - MARGIN_R, FRAME_BOT_RULE, RULE)
        self.text(MARGIN_L, FRAME_BOT_TEXT, footer_left, mono_s, INK_3)
        self.text(
            MARGIN_L,
            FRAME_BOT_TEXT,
            footer_right,
            mono_s,
            INK_3,
            align="right",
            width=CONTENT_W,
        )
        # furniture is drawn; measure only real content from here on
        self.min_y = CONTENT_TOP

    def rotated_text(self, x: float, y: float, s: str, style: TextStyle,
                     color=INK, angle: float = 90.0) -> None:
        """Draw a single line rotated about (x, y); used for rail labels.

        This runs in a translated frame, so the local origin is not a page
        coordinate: fill-balance tracking is suspended and the anchor recorded
        instead, otherwise the diagram would report content at y = 0.
        """
        if not s:
            return
        saved = self.min_y
        self.c.saveState()
        self.c.translate(x, y)
        self.c.rotate(angle)
        self._line_text_object(0.0, 0.0, resolve(s, style), style, color, style.tracking)
        self.c.restoreState()
        self.min_y = saved
        self._track(y)

    def page_title(self, y: float, title: str, sub: str | None = None) -> float:
        """Display title + optional sub-line. Returns the last baseline drawn."""
        self.text(MARGIN_L, y, title, self.style("page_title"), INK)
        if not sub:
            return y
        sub_y = y - self.style("page_sub").size - 7.0
        self.text(MARGIN_L, sub_y, sub, self.style("page_sub"), INK_2)
        return sub_y
