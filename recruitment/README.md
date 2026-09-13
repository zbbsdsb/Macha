# Recruitment document — build source

The public recruitment document for Macha's first **First World Operator**
(Minecraft Server Lead / First Player) — the first person to operate a test
environment and report on whether an agent reads as real.

The PDF is the deliverable. This directory is the editable source.

| File | What it is |
|---|---|
| `Macha_First_World_Operator.pdf` | English edition, 8 pages, A4 |
| `Macha_First_World_Operator_zh-CN.pdf` | Chinese edition, same layout system |
| `DESIGN.md` | Full design rationale: positioning, page structure, visual system, layout spec, review log |
| `positioning-review.md` | Criticism of the role definition itself, with concrete recommendations |
| `src/content.py` | **All copy, both languages.** Edit wording here, never in the layout code. |
| `src/design_system.py` | Grid, type scale, palette, mixed-script typesetting, annotation and diagram primitives |
| `src/build_pdf.py` | The eight page compositions |
| `src/prepare_fonts.py` | Fetches and statics the embedded fonts (reproducible) |
| `src/render_preview.py` | Rasterises pages and builds contact sheets for visual review |

## Rebuilding

```bash
python src/prepare_fonts.py            # fonts are committed; only needed if fonts/ is empty
python src/build_pdf.py                # writes both PDFs
python src/build_pdf.py --report       # + per-page fill balance
python src/build_pdf.py --debug-frame  # + content box, column grid, baseline grid overlay
python src/render_preview.py --dpi 110 # + page PNGs and contact sheets in .preview/
```

Requires `reportlab`, `fonttools`, `pillow`, and `pypdfium2` (preview only).

## Layout rules worth knowing before editing

- **Spacing convention.** `Doc.paragraph()` returns the baseline slot *after* the
  last line, so blocks compose additively. Every constant in `build_pdf.py`
  assumes this. Changing it will cause overlapping text.
- **Measure and draw together.** Block heights come from the same function that
  draws them (`duty_metrics` used by both `duty_block` and `page_work`), so the
  two halves of a row cannot drift apart.
- **Language gaps.** Chinese sets taller per unit of meaning, so `gp()` tightens
  structural gaps in the Chinese edition (factor 0.72). Do not use raw pixel gaps
  on dense pages.
- **Diagrams are vector.** Arrows and squares are drawn, never set as glyphs —
  font symbol coverage differs between Inter, Plex Mono and Noto Sans SC.
- **Never ship without rendering.** Two of the defects found during this build
  (`align="right"`'s x semantics; an inverted sign on a diagram target) were
  invisible in the source and obvious on the page.

## Note on content integrity

Everything the document claims about Macha's maturity is taken from this
repository's own `docs/roadmap.md` and `docs/architecture.md`. The real cognitive
core is Phase 3 and does not exist yet; the document says so explicitly.
Compensation, contract, location and hours are marked TBD rather than invented.
Keep it that way when editing.
