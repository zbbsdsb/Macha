"""Build the Macha "First World Operator" recruitment PDF.

Run:  python build_pdf.py

Emits, into ``recruitment/``:
    Macha_First_World_Operator.pdf           English edition
    Macha_First_World_Operator_zh-CN.pdf     Chinese edition

Everything is drawn on a raw ReportLab canvas against the grid defined in
``design_system``; all wording comes from ``content`` and is never hard-coded
here.

Spacing convention: ``Doc.paragraph`` returns the baseline slot *after* the last
line, so blocks compose additively. Block heights are computed by the same
function that draws them (see ``duty_metrics`` used by both ``duty_block`` and
``page_work``), which is what keeps the two halves of a row aligned.

Pass ``--debug-frame`` to overlay the content box, column grid and baseline grid.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from reportlab import rl_config
from reportlab.pdfgen import canvas as rl_canvas

import design_system as ds
from content import CONTENT
from design_system import (
    ACCENT,
    ACCENT_SOFT,
    BASELINE,
    COL_W,
    CONTENT_BOTTOM,
    CONTENT_TOP,
    CONTENT_W,
    GUTTER,
    INK,
    INK_2,
    INK_3,
    MARGIN_L,
    MARGIN_R,
    PAGE_H,
    PAGE_W,
    PAPER,
    RULE,
    RULE_SOFT,
    TINT,
    Doc,
    TextStyle,
    col_x,
    span_w,
    span_x,
    text_width,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FONT_DIR = ROOT / "fonts"

TOTAL_PAGES = 8
Y_TITLE = CONTENT_TOP - 26.0


# --------------------------------------------------------------------------
# shared furniture and reusable blocks
# --------------------------------------------------------------------------


def page_head(d: Doc, page_no: int, title: str, sub: str, section: str, c: dict,
              sub_width: float | None = None) -> float:
    """Frame + title + sub + rule. Returns the first free content baseline."""
    d.page_frame(page_no, TOTAL_PAGES, section, c["footer"]["left"], c["footer"]["right"])
    d.text(MARGIN_L, Y_TITLE, title, d.style("page_title"), INK)
    y = Y_TITLE - d.style("page_title").size * 0.60 - 6.0
    if sub:
        y = d.paragraph(MARGIN_L, y, sub, d.style("page_sub"), INK_2,
                        width=sub_width if sub_width else span_w(4))
    rule_y = y - 3.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, rule_y)
    return rule_y - 26.0


def gp(d: Doc, en_value: float) -> float:
    """Inter-block gap.

    Chinese copy occupies noticeably more vertical space per unit of meaning
    than English — fewer characters per line, taller leading — so the dense
    pages tighten their structural gaps in the Chinese edition instead of
    running past the foot of the measure.
    """
    return en_value if d.lang == "en" else round(en_value * 0.72, 1)


def mono_block(d: Doc, x: float, y: float, title: str, color=INK) -> float:
    d.text(x, y, title, d.style("mono_m"), color)
    return y - 16.0


def bullet_list(d: Doc, x: float, y: float, items: list[str], width: float,
                style_key: str = "small", color=INK_2, marker=INK_3,
                marker_size: float = 2.6) -> float:
    """Square-bulleted list. Returns the baseline slot below the last item."""
    style = d.style(style_key)
    cursor = y
    for item in items:
        d.square(x + 0.4, cursor + style.size * 0.30, marker_size, marker, True)
        lines = d.para_lines(item, style, width - 11.0)
        for i, line in enumerate(lines):
            d.text(x + 11.0, cursor - i * style.leading, line, style, color)
        cursor -= len(lines) * style.leading + 3.0
    return cursor


def bullets_height(d: Doc, items: list[str], width: float,
                   style_key: str = "small") -> float:
    style = d.style(style_key)
    return sum(len(d.para_lines(item, style, width - 11.0)) * style.leading + 3.0
               for item in items)


def duty_metrics(d: Doc, duty: dict, width: float, accent: bool = False) -> dict:
    """Geometry of one duty block. The single source of truth for its height."""
    body = d.style("body_m") if accent else d.style("body")
    small = d.style("small")
    m: dict = {"body_lines": d.para_lines(duty["body"], body, width), "body_lead": body.leading}

    bullets_h = 0.0
    if duty.get("bullets"):
        bullets_h = 4.0 + bullets_height(d, duty["bullets"], width)
    m["bullets_h"] = bullets_h

    chain_rows = 0
    if duty.get("chain"):
        chip_style = d.style("mono_s")
        rows, cw = 1, 0.0
        for chip in duty["chain"]:
            w = text_width(chip, chip_style) + 9.0
            if cw + w > width:
                rows += 1
                cw = 0.0
            cw += w + 5.0
        chain_rows = rows
    m["chain_rows"] = chain_rows

    foot_h = 0.0
    m["foot_lines"] = []
    if duty.get("foot"):
        m["foot_lines"] = d.para_lines(duty["foot"], small, width - 9.0)
        foot_h = 6.0 + len(m["foot_lines"]) * small.leading
    m["foot_h"] = foot_h

    m["total"] = (17.0 + len(m["body_lines"]) * body.leading
                  + bullets_h + chain_rows * 15.0 + foot_h)
    return m


def duty_block(d: Doc, x: float, y: float, width: float, duty: dict,
               accent: bool = False) -> float:
    """Draw one numbered duty. Returns the baseline slot below the block."""
    body = d.style("body_m") if accent else d.style("body")
    small = d.style("small")
    m = duty_metrics(d, duty, width, accent)

    d.text(x, y, duty["num"], d.style("mono_m"), ACCENT if accent else INK_3)
    d.text(x + 21.0, y, duty["name"], d.style("section"), INK, tracking=0.55)

    cursor = y - 17.0
    for i, line in enumerate(m["body_lines"]):
        d.text(x, cursor - i * body.leading, line, body, INK)
    cursor -= (len(m["body_lines"]) - 1) * body.leading + body.leading

    if duty.get("bullets"):
        cursor = bullet_list(d, x, cursor - 4.0, duty["bullets"], width, color=INK_2)

    if duty.get("chain"):
        chip_style = d.style("mono_s")
        chip_y, chip_x = cursor, x
        for chip in duty["chain"]:
            w = text_width(chip, chip_style) + 9.0
            if chip_x + w > x + width:
                chip_x, chip_y = x, chip_y - 15.0
            d.stroke(RULE, 0.5)
            d.c.rect(chip_x, chip_y - 3.5, w, 13.0, stroke=1, fill=0)
            d.text(chip_x + 4.5, chip_y, chip, chip_style, INK_2)
            chip_x += w + 5.0
        cursor = chip_y - 15.0

    if duty.get("foot"):
        cursor -= 6.0
        d.square(x, cursor + 3.0, 3.1, ACCENT, True)
        for i, line in enumerate(m["foot_lines"]):
            d.text(x + 9.0, cursor - i * small.leading, line, small, INK)
        cursor -= len(m["foot_lines"]) * small.leading

    return cursor


# --------------------------------------------------------------------------
# 01 — cover
# --------------------------------------------------------------------------


def page_cover(d: Doc, c: dict) -> None:
    cv = c["cover"]

    # -- furniture first, so the fill-balance measurement excludes it -------
    for i in range(ds.COLUMNS + 1):
        x = MARGIN_L + i * (COL_W + GUTTER)
        d.vrule(x, PAGE_H - 26.0, PAGE_H - 18.0, RULE)
        d.vrule(x, 26.0, 34.0, RULE)

    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, 799.89, RULE)
    d.text(MARGIN_L, 786.0, cv["eyebrow"], d.style("mono_m"), INK, tracking=3.4)
    d.text(MARGIN_L, 786.0, c["footer"]["right"], d.style("mono_s"), INK_3,
           align="right", width=CONTENT_W)
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, 50.0, RULE)
    d.text(MARGIN_L, 39.0, c["footer"]["cover_strip"], d.style("mono_s"), INK_3)

    d.min_y = CONTENT_TOP

    # -- content -----------------------------------------------------------
    d.label(MARGIN_L, 508.0, cv["env"], d.style("mono"), INK_2, tick=True)

    y = 462.0
    for line in cv["title_lines"]:
        d.text(MARGIN_L, y, line, d.style("cover_title"), INK)
        y -= d.style("cover_title").leading
    title_bottom = y + d.style("cover_title").leading

    d.hrule(MARGIN_L, col_x(1) + COL_W, title_bottom - 17.0, INK, 1.0)

    sub_y = title_bottom - 40.0
    d.text(MARGIN_L, sub_y, cv["subtitle"], d.style("cover_sub"), INK)
    if cv.get("title_cn"):
        sub_y -= 20.0
        d.text(MARGIN_L, sub_y, cv["title_cn"], d.style("cover_sub"), INK_2)

    q_style = TextStyle(13.6, 20.0, -0.05, "regular", "text")
    qy = sub_y - 58.0
    for line in cv["question_lines"]:
        d.text(MARGIN_L, qy, line, q_style, INK)
        qy -= q_style.leading

    d.paragraph(MARGIN_L, qy - 16.0, cv["standfirst"], d.style("small"), INK_2,
                width=span_w(4))

    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, 116.0, RULE)
    cell_w = CONTENT_W / len(cv["status"])
    for i, (key, value) in enumerate(cv["status"]):
        x = MARGIN_L + i * cell_w
        d.text(x, 100.0, key, d.style("mono_s"), INK_3)
        d.paragraph(x, 86.0, value, d.style("micro"), INK, width=cell_w - 12.0)


# --------------------------------------------------------------------------
# 02 — the question
# --------------------------------------------------------------------------


def page_question(d: Doc, c: dict) -> None:
    q = c["question"]
    y = page_head(d, 2, q["title"], q["sub"], "02 \u2014 THE QUESTION", c, sub_width=span_w(4))
    y += 14.0

    left = span_x(0, 3)
    right = span_x(4, 5)

    d.label(right[0], y, "THE USUAL QUESTION" if d.lang == "en" else "通常被问的问题",
            d.style("mono"), INK_3)
    d.paragraph(right[0], y - 15.0,
                "how do we make the NPC smarter?" if d.lang == "en" else "怎样才能让 NPC 更聪明？",
                d.style("small"), INK_3, width=right[1])
    d.hrule(right[0], right[0] + right[1], y - 38.0, RULE_SOFT)
    d.label(right[0], y - 56.0, "THE QUESTION WE ASK" if d.lang == "en" else "我们要问的问题",
            d.style("mono"), ACCENT, tick=True)
    d.paragraph(right[0], y - 71.0,
                "why does more intelligence not produce presence?"
                if d.lang == "en" else "为什么更多的智能，换不来更多的存在感？",
                d.style("small"), INK, width=right[1])

    cursor = d.paragraph(left[0], y, q["p1"], d.style("body"), INK, width=left[1])
    cursor = d.paragraph(left[0], cursor - 18.0, q["p2"], d.style("body_m"), INK,
                         width=left[1])

    band_y = min(cursor - 34.0, y - 104.0)
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, band_y, RULE)
    cursor = band_y - 34.0

    d.paragraph(MARGIN_L, cursor, q["belief_intro"], d.style("small"), INK_2,
                width=span_w(4))
    cursor -= 46.0

    body_x = col_x(1)
    body_w = span_x(1, 4)[1]
    for num, headline, note in q["beliefs"]:
        d.text(MARGIN_L, cursor, num, d.style("mono_m"), ACCENT)
        d.text(body_x, cursor, headline, d.style("section"), INK, tracking=0.2)
        d.paragraph(body_x, cursor - 15.5, note, d.style("small"), INK_2, width=body_w)
        cursor -= 56.0

    d.hrule(body_x, PAGE_W - MARGIN_R, cursor + 22.0, RULE_SOFT)
    cursor -= 30.0
    cursor = d.paragraph(body_x, cursor, q["p3"], d.style("body"), INK, width=body_w)

    cursor -= 18.0
    d.square(MARGIN_L, cursor + 3.0, 3.1, ACCENT, True)
    d.paragraph(MARGIN_L + 9.0, cursor + 5.0, q["closing"], d.style("small"), INK,
                width=span_w(4))


# --------------------------------------------------------------------------
# 03 — the role
# --------------------------------------------------------------------------


def page_role(d: Doc, c: dict) -> None:
    r = c["role"]
    y = page_head(d, 3, r["title"], r["sub"], "03 \u2014 THE ROLE", c, sub_width=span_w(4))
    y += 16.0

    d.text(MARGIN_L, y, r["lead"], d.style("lead"), INK)
    y -= 26.0
    d.label(MARGIN_L, y, r["not"], d.style("mono"), INK_2, tick=True)
    y -= 28.0
    d.paragraph(MARGIN_L, y, r["bridge"], d.style("body"), INK_2, width=span_w(4))
    y -= 42.0

    desc_x = col_x(2)
    desc_w = span_x(2, 5)[1]
    for name, desc in r["parts"]:
        d.text(MARGIN_L, y, name, d.style("mono_m"), INK)
        d.paragraph(desc_x, y, desc, d.style("body"), INK_2, width=desc_w)
        y -= 42.0
        d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y + 14.0, RULE_SOFT)

    y -= 30.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= 38.0

    col_a = span_x(0, 2)
    col_b = span_x(3, 5)

    cy = mono_block(d, col_a[0], y,
                    "THE HONEST VERSION" if d.lang == "en" else "诚实的说法", INK)
    d.paragraph(col_a[0], cy, r["honest"], d.style("body"), INK, width=col_a[1])

    cy = mono_block(d, col_b[0], y, r["zero_title"], ACCENT)
    cy = d.paragraph(col_b[0], cy, r["zero_body"], d.style("small"), INK_2, width=col_b[1])
    cy = bullet_list(d, col_b[0], cy - 8.0, r["zero_items"], col_b[1],
                     style_key="item", color=INK, marker=INK_3)
    cy -= 16.0
    d.square(col_b[0], cy + 3.0, 3.1, ACCENT, True)
    d.paragraph(col_b[0] + 9.0, cy + 5.0, r["zero_close"], d.style("small"), INK,
                width=col_b[1] - 9.0)


# --------------------------------------------------------------------------
# 04 — what you will do
# --------------------------------------------------------------------------


def page_work(d: Doc, c: dict) -> None:
    w = c["work"]
    y = page_head(d, 4, w["title"], w["sub"], "04 \u2014 WHAT YOU WILL DO", c,
                  sub_width=span_w(5))
    y += gp(d, 20.0)

    a = span_x(0, 2)
    b = span_x(3, 5)
    d1, d2, d3, d4, d5 = w["duties"]

    # -- row 1: run the world / be the first player ----------------------
    duty_block(d, a[0], y, a[1], d1)
    duty_block(d, b[0], y, b[1], d2)
    y -= max(duty_metrics(d, d1, a[1])["total"],
             duty_metrics(d, d2, b[1])["total"]) + gp(d, 30.0)
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= gp(d, 38.0)

    # -- row 2: find the fake, full measure, accent-marked ---------------
    left_duty = {**d3, "bullets": None}
    row_h = max(
        duty_metrics(d, left_duty, a[1], accent=True)["total"],
        16.0 + bullets_height(d, d3["bullets"], b[1]),
    )
    d.vrule(MARGIN_L - 13.0, y - row_h + 4.0, y + 10.0, ACCENT, 2.0)
    duty_block(d, MARGIN_L + 2.0, y, a[1] - 2.0, left_duty, accent=True)
    d.text(b[0], y, "LOOK FOR" if d.lang == "en" else "要找的是这些",
           d.style("mono"), INK_3)
    bullet_list(d, b[0], y - 17.0, d3["bullets"], b[1], color=INK_2, marker=ACCENT)
    y -= row_h + gp(d, 34.0)
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= gp(d, 38.0)

    # -- row 3: create situations / report experience --------------------
    duty_block(d, a[0], y, a[1], d4)
    duty_block(d, b[0], y, b[1], d5)


# --------------------------------------------------------------------------
# 05 — who we are looking for
# --------------------------------------------------------------------------


def page_fit(d: Doc, c: dict) -> None:
    f = c["fit"]
    y = page_head(d, 5, f["title"], f["sub"], "05 \u2014 WHO WE ARE LOOKING FOR", c,
                  sub_width=span_w(5))
    y += 16.0

    d.vrule(MARGIN_L - 13.0, y - 54.0, y + 10.0, ACCENT, 2.0)
    y = d.paragraph(MARGIN_L, y, f["quote"], d.style("quote"), INK, width=span_w(5))
    y -= 40.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= 34.0

    left = span_x(0, 2)
    right = span_x(3, 5)

    cy = mono_block(d, left[0], y, f["spec_title"], INK)
    stars_w = 5 * 5.0 + 4 * 2.6
    for name, filled in f["spec"]:
        cy -= 34.0
        d.text(left[0], cy, name, d.style("small"), INK)
        d.rating(left[0] + left[1] - stars_w, cy - 0.7, filled)

    cy = mono_block(d, right[0], y, f["profile_title"], INK)
    cy = bullet_list(d, right[0], cy, f["profile"], right[1],
                     style_key="item", color=INK_2)

    band_y = min(cy - 40.0, 274.0)
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, band_y, RULE)
    cy = band_y - 34.0

    d.label(MARGIN_L, cy, f["not_title"], d.style("mono_m"), ACCENT, tick=True)
    cy -= 26.0

    items = f["not_items"]
    half = (len(items) + 1) // 2
    for idx, (x, _) in enumerate((span_x(0, 2), span_x(3, 5))):
        bullet_list(d, x, cy, items[idx * half:(idx + 1) * half], span_w(3),
                    style_key="item", color=INK_2, marker=RULE)


# --------------------------------------------------------------------------
# 06 — the experiment
# --------------------------------------------------------------------------


def loop_diagram(d: Doc, x: float, y_top: float, width: float,
                 nodes: list[tuple[str, str, bool]], feedback_label: str,
                 target_bottom: float | None = None) -> float:
    """Vertical chain with a return rail; returns the baseline slot below it.

    When ``target_bottom`` is given and the natural layout would end above it,
    the slack is distributed evenly between the nodes so the diagram fills the
    column instead of leaving dead space at the foot of the page.
    """
    ann_style = d.style("small")
    spine_x = x + 1.5
    text_x = x + 17.0
    inner_w = width - 17.0 - 22.0
    rail_x = x + width - 1.0

    def build(pitch_extra: float) -> list[tuple[float, str, list[str], bool]]:
        out: list[tuple[float, str, list[str], bool]] = []
        cursor = y_top
        for label, note, accent in nodes:
            lines = d.para_lines(note, ann_style, inner_w)
            out.append((cursor, label, lines, accent))
            cursor -= 13.5 + len(lines) * ann_style.leading + 16.0 + pitch_extra
        return out

    def bottom_of(rows: list[tuple[float, str, list[str], bool]]) -> float:
        y_last, _, lines, _ = rows[-1]
        return y_last - 12.5 - (len(lines) - 1) * ann_style.leading - 18.0

    layout = build(0.0)
    if target_bottom is not None:
        gaps = max(1, len(nodes) - 1)
        # Stretch to meet the band, leaving the intended section gap. Capped as
        # a guard only: an unbounded stretch would run the diagram into the
        # band on a short page.
        extra = min(48.0, (bottom_of(layout) - target_bottom) / gaps)
        if extra > 1.0:
            layout = build(extra)

    for i, (ny, label, lines, accent) in enumerate(layout):
        color = ACCENT if accent else INK
        d.square(spine_x - 2.3, ny + ann_style.size * 0.28, 4.6, color, True)
        d.text(text_x, ny, label, d.style("mono_m"), color)
        for j, line in enumerate(lines):
            d.text(text_x, ny - 12.5 - j * ann_style.leading, line, ann_style,
                   INK if accent else INK_2)
        if i < len(layout) - 1:
            tail = ny - 12.5 - (len(lines) - 1) * ann_style.leading
            d.arrow_down(spine_x, tail - 5.0, layout[i + 1][0] + 10.0, INK_3, 0.6, 4.2)

    first_y = layout[0][0]
    last_y = layout[-1][0]
    last_lines = layout[-1][2]
    arrival_y = first_y + 30.0
    # The rail leaves *below* the final annotation. A horizontal stroke at the
    # node's own baseline would cut straight through its label.
    rail_start_y = last_y - 12.5 - (len(last_lines) - 1) * ann_style.leading - 8.0
    d.stroke(INK_3, 0.6)
    d.c.line(spine_x, last_y + ann_style.size * 0.28, spine_x, rail_start_y)
    d.c.line(spine_x, rail_start_y, rail_x, rail_start_y)
    d.c.line(rail_x, rail_start_y, rail_x, arrival_y)
    d.c.line(rail_x, arrival_y, spine_x, arrival_y)
    d.arrow_down(spine_x, arrival_y, first_y + 11.0, INK_3, 0.6, 4.2)
    d.rotated_text(rail_x - 4.0, (last_y + first_y) / 2.0 + 14.0, feedback_label,
                   d.style("mono_s"), INK_3)

    return bottom_of(layout)


def stack_band(d: Doc, y: float, c: dict, dry: bool = False) -> float:
    """Architecture stack: Macha Core -> Layer Protocol -> Layer -> environment.

    Boxes are positioned *downwards from the caption baseline* rather than from
    the inter-block gap. Tying box geometry to a gap constant meant that
    tightening the gap for the Chinese edition pushed the boxes up through their
    own caption.

    Returns the lowest baseline drawn. With ``dry=True`` it performs the same
    arithmetic without drawing, so ``page_experiment`` can bottom-anchor the band
    and then size the loop diagram to stop clear above it.
    """
    e = c["experiment"]
    small = d.style("small")
    mono = d.style("mono")

    if not dry:
        d.label(MARGIN_L, y, e["stack_title"], d.style("mono_m"), INK)

    items = e["stack"]
    gap = 17.0
    box_w = (CONTENT_W - gap * (len(items) - 1)) / len(items)
    box_h = 25.0
    box_top = y - 13.0
    box_bottom = box_top - box_h
    chip_baseline = box_bottom + box_h * 0.5 - mono.size * 0.36

    if not dry:
        for i, item in enumerate(items):
            x = MARGIN_L + i * (box_w + gap)
            primary = i == 0
            d.stroke(INK if primary else RULE, 0.5)
            d.c.setFillColor(ACCENT_SOFT if primary else TINT)
            d.c.rect(x, box_bottom, box_w, box_h, stroke=1, fill=1)
            d.text(x, chip_baseline, item, mono, INK, align="center", width=box_w)
            if i < len(items) - 1:
                d.arrow_right(x + box_w + 3.5, x + box_w + gap - 3.5,
                              box_bottom + box_h * 0.5, INK_3, 0.6, 3.0)

    y = box_bottom - gp(d, 26.0)
    note_lines = d.para_lines(e["stack_note"], small, span_w(5))
    if not dry:
        for i, line in enumerate(note_lines):
            d.text(MARGIN_L, y - i * small.leading, line, small, INK_2)
    y -= len(note_lines) * small.leading
    y -= gp(d, 40.0)

    last_x = MARGIN_L + (len(items) - 1) * (box_w + gap) + box_w
    if not dry:
        d.c.setDash(1.6, 2.2)
        d.stroke(RULE, 0.6)
        d.c.line(last_x, y + 28.0, PAGE_W - MARGIN_R, y + 28.0)
        d.c.setDash()
        d.hrule(MARGIN_L, last_x - 4.0, y + 28.0, RULE, 0.6)
        # align="right" measures from the box's LEFT edge, not the right edge
        d.text(MARGIN_L, y + 38.0, e["stack_future"], d.style("mono_s"), INK_3,
               align="right", width=CONTENT_W)

    rule_lines = d.para_lines(e["stack_rule"], small, span_w(4))
    if not dry:
        d.square(MARGIN_L, y + 13.0, 3.1, ACCENT, True)
        for i, line in enumerate(rule_lines):
            d.text(MARGIN_L + 9.0, y + 15.0 - i * small.leading, line, small, INK)
    return y + 15.0 - (len(rule_lines) - 1) * small.leading


def page_experiment(d: Doc, c: dict) -> None:
    e = c["experiment"]
    y = page_head(d, 6, e["title"], e["sub"], "06 \u2014 THE EXPERIMENT", c, sub_width=span_w(5))
    y += gp(d, 14.0)

    left = span_x(0, 2)
    right = span_x(3, 5)

    d.label(left[0], y, e["loop_title"], d.style("mono"), INK_3)

    ry = d.paragraph(right[0], y, e["right_a"], d.style("body"), INK, width=right[1])
    ry = d.paragraph(right[0], ry - 10.0, e["right_b"], d.style("body_m"), INK,
                     width=right[1])
    ry = d.paragraph(right[0], ry - 24.0, e["state_note"], d.style("micro"), INK_3,
                     width=right[1])
    d.hrule(right[0], right[0] + right[1], ry + 3.0, RULE)
    sy = mono_block(d, right[0], ry - 14.0, e["state_title"], INK)
    for label, value in e["state"]:
        sy -= 26.0
        d.leader_row(right[0], sy, label, value, right[1],
                     style=d.style("small"), right_style=d.style("mono_s"))
    sy -= 22.0
    d.square(right[0], sy + 3.0, 3.1, ACCENT, True)
    close_lines = d.para_lines(e["state_close"], d.style("small"), right[1] - 9.0)
    for i, line in enumerate(close_lines):
        d.text(right[0] + 9.0, sy + 5.0 - i * d.style("small").leading, line,
               d.style("small"), INK)
    sy = sy + 5.0 - (len(close_lines) - 1) * d.style("small").leading

    # Bottom-anchor the architecture band, then size the loop to stop clear
    # above it.
    #
    # band_top is the band's caption baseline; its topmost ink is the caption's
    # cap height, ~8pt above that. And loop_diagram reports
    # bottom_of = (last annotation baseline - 18), i.e. ~16pt above the last ink.
    band_h = 400.0 - stack_band(d, 400.0, c, dry=True)
    band_top = CONTENT_BOTTOM + band_h + 30.0
    band_edge = band_top + 8.0
    rail_target = band_edge + 50.0

    loop_bottom = loop_diagram(d, left[0], y - gp(d, 50.0), left[1], e["loop"],
                               e["loop_label"], target_bottom=rail_target)

    ink_clearance = (loop_bottom + 16.0) - band_edge
    if ink_clearance < 10.0:
        print(f"  ! page 06 ({d.lang}): loop ink {ink_clearance:.1f}pt from the band")
    if sy < band_edge + 12.0:
        print(f"  ! page 06 ({d.lang}): right column at {sy:.1f} vs band edge "
              f"{band_edge:.1f}")
    if os.environ.get("MACHA_REPORT"):
        print(f"  . p06 ({d.lang}) loop bottom {loop_bottom:6.1f}  band edge "
              f"{band_edge:6.1f}  clearance {ink_clearance:6.1f}")

    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, band_top + 14.0, RULE)
    stack_band(d, band_top, c)


# --------------------------------------------------------------------------
# 07 — your first experiment
# --------------------------------------------------------------------------


def page_first(d: Doc, c: dict) -> None:
    f = c["first"]
    y = page_head(d, 7, f["title"], f["sub"], "07 \u2014 YOUR FIRST EXPERIMENT", c,
                  sub_width=span_w(4))
    y += 22.0

    d.label(MARGIN_L, y, f["task_title"], d.style("mono_m"), ACCENT)
    y -= 30.0

    task_style = TextStyle(19.0 if d.lang == "en" else 17.5,
                           25.5 if d.lang == "en" else 30.0, -0.25, "regular", "display")
    y = d.paragraph(MARGIN_L, y, f["task"][0], task_style, INK, width=span_w(5))
    y = d.paragraph(MARGIN_L, y - 8.0, f["task_body"], d.style("body"), INK_2,
                    width=span_w(4))

    y -= 26.0
    d.vrule(MARGIN_L - 13.0, y - 20.0, y + 9.0, ACCENT, 2.0)
    d.text(MARGIN_L, y, f["rule"], d.style("lead"), INK)
    y -= 38.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= 32.0

    d.text(MARGIN_L, y, f["ask_title"], d.style("mono_m"), INK)
    y -= 32.0

    q_style = d.style("lead")
    q_width = span_w(3) - 30.0
    for i, question in enumerate(f["asks"]):
        x = MARGIN_L if i % 2 == 0 else col_x(3)
        yy = y - (i // 2) * 78.0
        d.text(x, yy, f"{i + 1:02d}", d.style("num"), ACCENT)
        d.paragraph(x + 28.0, yy, question, q_style, INK, width=q_width)

    y -= 2 * 78.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, y, RULE)
    y -= 28.0

    d.label(MARGIN_L, y, f["why_title"], d.style("mono_m"), INK)
    y -= 18.0
    y = d.paragraph(MARGIN_L, y, f["why"], d.style("body"), INK, width=span_w(4))
    y -= 14.0
    d.square(MARGIN_L, y + 3.0, 3.1, ACCENT, True)
    d.paragraph(MARGIN_L + 9.0, y + 5.0, f["why_foot"], d.style("small"), INK, width=span_w(4))

    d.text(MARGIN_L, CONTENT_BOTTOM + 4.0, f["no_interview"], d.style("mono"), INK_3)


# --------------------------------------------------------------------------
# 08 — join us
# --------------------------------------------------------------------------


def page_join(d: Doc, c: dict) -> None:
    j = c["join"]
    y = page_head(d, 8, j["title"], j["sub"], "08 \u2014 JOIN US", c, sub_width=span_w(4))
    y += 16.0

    steps_top = y
    left = span_x(0, 3)
    right = span_x(4, 5)

    for num, name, body, time in j["steps"]:
        d.text(left[0], y, num, d.style("num"), ACCENT)
        d.text(left[0] + 30.0, y, name, d.style("section"), INK, tracking=0.55)
        cy = d.paragraph(left[0] + 30.0, y - 18.0, body, d.style("body"), INK_2,
                         width=left[1] - 30.0)
        d.text(left[0] + 30.0, cy - 14.0, time, d.style("mono_s"), INK_3)
        y = cy - 38.0
        d.hrule(left[0], left[0] + left[1], y + 19.0, RULE_SOFT)

    cy = mono_block(d, right[0], steps_top, j["near_title"], INK)
    cy = d.paragraph(right[0], cy, j["near"], d.style("small"), INK_2, width=right[1])
    cy -= 30.0
    d.hrule(right[0], right[0] + right[1], cy + 16.0, RULE)
    cy -= 12.0
    cy = mono_block(d, right[0], cy, j["tbd_title"], ACCENT)
    cy = d.paragraph(right[0], cy, j["tbd_body"], d.style("small"), INK_2, width=right[1])
    cy -= 16.0
    for label, value in j["tbd"]:
        d.leader_row(right[0], cy, label, value, right[1],
                     style=d.style("small"), right_style=d.style("mono_s"))
        cy -= 19.0

    band_y = CONTENT_BOTTOM + 110.0
    d.hrule(MARGIN_L, PAGE_W - MARGIN_R, band_y, RULE)
    by = band_y - 26.0
    d.label(MARGIN_L, by, j["apply_label"], d.style("mono_m"), ACCENT)
    email_style = TextStyle(21.0, 26.0, -0.3, "medium", "display")
    d.text(MARGIN_L, by - 32.0, j["apply_email"], email_style, INK)
    d.text(MARGIN_L, by - 48.0, j["apply_subject"], d.style("mono_s"), INK_3)
    d.paragraph(col_x(3), by - 18.0, j["apply_note"], d.style("small"), INK_2,
                width=span_w(3))
    d.paragraph(MARGIN_L, CONTENT_BOTTOM + 20.0, j["closing"], d.style("small"), INK,
                width=span_w(5))


# --------------------------------------------------------------------------
# document assembly
# --------------------------------------------------------------------------


def _debug_overlay(d: Doc) -> None:
    d.stroke(ACCENT, 0.3)
    d.c.setDash(1, 3)
    d.c.rect(MARGIN_L, CONTENT_BOTTOM, CONTENT_W, CONTENT_TOP - CONTENT_BOTTOM,
             stroke=1, fill=0)
    for i in range(ds.COLUMNS + 1):
        x = MARGIN_L + i * (COL_W + GUTTER)
        d.c.line(x, CONTENT_BOTTOM, x, CONTENT_TOP)
    y = CONTENT_BOTTOM
    while y < CONTENT_TOP:
        d.c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
        y += BASELINE
    d.c.setDash()


PAGES = [
    page_cover,
    page_question,
    page_role,
    page_work,
    page_fit,
    page_experiment,
    page_first,
    page_join,
]


def build(lang: str, out_path: Path, debug_frame: bool = False,
          report: bool = False) -> Path:
    content = CONTENT[lang]
    # never declare an unembedded font in a document meant for public release
    rl_config.canvas_basefontname = ds.base_font_name()
    c = rl_canvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    suffix = "" if lang == "en" else " (\u4e2d\u6587\u7248)"
    c.setTitle("Macha \u2014 First World Operator" + suffix)
    c.setAuthor("Macha")
    c.setSubject("Early-stage experimental recruitment document")
    c.setCreator("Macha recruitment build (ReportLab)")

    for index, compose in enumerate(PAGES):
        c.setFillColor(PAPER)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        doc = Doc(c, lang)
        compose(doc, content)
        if debug_frame:
            _debug_overlay(doc)
        if report:
            slack = doc.min_y - CONTENT_BOTTOM
            flag = "  <-- loose" if slack > 150 else ("  <-- TIGHT" if slack < 12 else "")
            print(f"  {lang} p{index + 1:02d}  lowest content y = {doc.min_y:6.1f}"
                  f"   bottom margin = {slack:6.1f}{flag}")
        c.showPage()

    c.save()
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--debug-frame", action="store_true",
                        help="overlay content box, column grid and baseline grid")
    parser.add_argument("--report", action="store_true",
                        help="print per-page fill balance (lowest content baseline)")
    parser.add_argument("--out-dir", default=str(ROOT))
    args = parser.parse_args()

    ds.register_fonts(FONT_DIR)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for lang, name in (
        ("en", "Macha_First_World_Operator.pdf"),
        ("zh", "Macha_First_World_Operator_zh-CN.pdf"),
    ):
        path = build(lang, out_dir / name, debug_frame=args.debug_frame,
                     report=args.report)
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
