"""Rasterise the built PDFs for visual review.

Run:  python render_preview.py [--dpi 110]

Writes page PNGs and 2x2 contact sheets into ``recruitment/.preview/`` so the
layout can be inspected page by page. This is the check that matters: a layout
is not finished until it has been looked at.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / ".preview"


def render(pdf_path: Path, dpi: int) -> list[Path]:
    doc = pdfium.PdfDocument(str(pdf_path))
    scale = dpi / 72.0
    paths: list[Path] = []
    stem = pdf_path.stem
    for i in range(len(doc)):
        page = doc[i]
        image = page.render(scale=scale).to_pil().convert("RGB")
        path = OUT / f"{stem}-p{i + 1:02d}.png"
        image.save(path)
        paths.append(path)
    return paths


def contact_sheet(paths: list[Path], out: Path, per_sheet: int = 4,
                  thumb_width: int = 430) -> list[Path]:
    sheets: list[Path] = []
    for start in range(0, len(paths), per_sheet):
        chunk = paths[start:start + per_sheet]
        thumbs = []
        for p in chunk:
            img = Image.open(p)
            ratio = thumb_width / img.width
            thumbs.append(img.resize((thumb_width, int(img.height * ratio)), Image.LANCZOS))
        cols = 2
        rows = (len(thumbs) + cols - 1) // cols
        gap = 14
        th = thumbs[0].height
        sheet = Image.new("RGB", (cols * thumb_width + (cols + 1) * gap,
                                  rows * th + (rows + 1) * gap), (232, 230, 225))
        for i, t in enumerate(thumbs):
            r, c = divmod(i, cols)
            sheet.paste(t, (gap + c * (thumb_width + gap), gap + r * (th + gap)))
        path = out.parent / f"{out.name}-{start // per_sheet + 1}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dpi", type=int, default=110)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(ROOT.glob("Macha_First_World_Operator*.pdf")):
        pages = render(pdf, args.dpi)
        print(f"{pdf.name}: {len(pages)} pages")
        for sheet in contact_sheet(pages, OUT / f"sheet-{pdf.stem}"):
            print(f"  sheet {sheet.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
