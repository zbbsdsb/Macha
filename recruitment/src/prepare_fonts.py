"""Prepare the embeddable font set for the Macha recruitment PDF.

Produces static, embeddable TTFs into ``recruitment/fonts/`` so that the PDF
renders identically everywhere (no reliance on the reader's installed fonts).

Typefaces used
--------------
Inter / Inter Display   SIL Open Font License 1.1   (rsms/inter)
IBM Plex Mono           SIL Open Font License 1.1   (IBM)
Noto Sans SC            SIL Open Font License 1.1   (Google)

Inter ships as a 36-face TrueType Collection (``Inter.ttc``); ReportLab cannot
use a TTC directly, so the needed faces are extracted into standalone TTFs.
Noto Sans SC ships as a variable font; the three weights we need are instanced
into statics so that weight, not axis interpolation, decides the rendering.

Run:  python prepare_fonts.py
Idempotent — existing outputs are reused.
"""

from __future__ import annotations

import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont, TTCollection
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FONT_DIR = ROOT / "fonts"
CACHE = ROOT / ".fontcache"

INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
NOTO_SC_VF = (
    "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
)
PLEX_BASE = "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/ibmplexmono/"

# name in Inter.ttc -> output filename
INTER_FACES = {
    "Inter": "Inter-Regular.ttf",
    "Inter Medium": "Inter-Medium.ttf",
    "Inter SemiBold": "Inter-SemiBold.ttf",
    "Inter Bold": "Inter-Bold.ttf",
    "Inter Display": "InterDisplay-Regular.ttf",
    "Inter Display Medium": "InterDisplay-Medium.ttf",
    "Inter Display SemiBold": "InterDisplay-SemiBold.ttf",
    "Inter Display Bold": "InterDisplay-Bold.ttf",
    "Inter ExtraBold": "Inter-ExtraBold.ttf",
}

# Noto Sans SC weights to instance
NOTO_WEIGHTS = {
    400: "NotoSansSC-Regular.ttf",
    500: "NotoSansSC-Medium.ttf",
    700: "NotoSansSC-Bold.ttf",
}

PLEX_FILES = {
    "IBMPlexMono-Regular.ttf": "IBMPlexMono-Regular.ttf",
    "IBMPlexMono-Medium.ttf": "IBMPlexMono-Medium.ttf",
    "IBMPlexMono-SemiBold.ttf": "IBMPlexMono-SemiBold.ttf",
    "IBMPlexMono-Bold.ttf": "IBMPlexMono-Bold.ttf",
}

# Local fallbacks, used only if the network is unavailable.
LOCAL_FALLBACKS = {
    "noto_sc_vf": [
        Path("C:/Windows/Fonts/NotoSansSC-VF.ttf"),
    ],
    "inter_ttc": [CACHE / "Inter.ttc"],
}


def log(msg: str) -> None:
    print(f"[fonts] {msg}", flush=True)


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        log(f"cached  {dest.name}")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    log(f"fetch   {dest.name}")
    req = urllib.request.Request(url, headers={"User-Agent": "macha-recruitment-build"})
    with urllib.request.urlopen(req, timeout=180) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh)
    if dest.stat().st_size < 1024:
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"download too small, giving up: {url}")
    return dest


def find_local(key: str) -> Path | None:
    for candidate in LOCAL_FALLBACKS.get(key, []):
        if candidate.exists() and candidate.stat().st_size > 0:
            log(f"local   {candidate}")
            return candidate
    return None


def extract_inter() -> None:
    needed = [f for f in INTER_FACES.values() if not (FONT_DIR / f).exists()]
    if not needed:
        log("inter   already extracted")
        return

    ttc_path = find_local("inter_ttc")
    if ttc_path is None:
        zip_path = download(INTER_ZIP, CACHE / "Inter-4.1.zip")
        with zipfile.ZipFile(zip_path) as zf:
            with zf.open("Inter.ttc") as src, open(CACHE / "Inter.ttc", "wb") as dst:
                shutil.copyfileobj(src, dst)
        ttc_path = CACHE / "Inter.ttc"

    collection = TTCollection(str(ttc_path))
    by_name: dict[str, TTFont] = {}
    for font in collection.fonts:
        name_table = font["name"]
        family = name_table.getName(1, 3, 1, 0x409) or name_table.getName(1, 1, 0, 0)
        style = name_table.getName(2, 3, 1, 0x409) or name_table.getName(2, 1, 0, 0)
        if family is None or style is None:
            continue
        family, style = str(family), str(style)
        if style in ("Regular", "Bold"):
            key = family if style == "Regular" else f"{family} Bold"
            by_name.setdefault(key, font)

    for key, out_name in INTER_FACES.items():
        out = FONT_DIR / out_name
        if out.exists():
            continue
        font = by_name.get(key)
        if font is None:
            raise RuntimeError(f"face not found in Inter.ttc: {key!r}")
        font.save(str(out))
        log(f"extract {out_name}  <- Inter.ttc:{key}")


def extract_noto_sc() -> None:
    if all((FONT_DIR / f).exists() for f in NOTO_WEIGHTS.values()):
        log("noto    already instanced")
        return

    vf_path = None
    try:
        vf_path = download(NOTO_SC_VF, CACHE / "NotoSansSC-VF.ttf")
    except Exception as exc:  # noqa: BLE001 - fall back to a local copy
        log(f"noto    download failed ({exc}); trying local fallback")
        vf_path = find_local("noto_sc_vf")
    if vf_path is None:
        raise RuntimeError("no Noto Sans SC variable font available")

    for weight, out_name in NOTO_WEIGHTS.items():
        out = FONT_DIR / out_name
        if out.exists():
            continue
        font = TTFont(str(vf_path))
        static = instancer.instantiateVariableFont(
            font, {"wght": weight}, inplace=False, updateFontNames=True
        )
        static.save(str(out))
        log(f"instance {out_name}  <- wght {weight}")


def fetch_plex() -> None:
    for remote, local in PLEX_FILES.items():
        out = FONT_DIR / local
        if out.exists():
            log(f"plex    {local} present")
            continue
        try:
            download(PLEX_BASE + remote, out)
        except Exception as exc:  # noqa: BLE001
            log(f"plex    {remote} failed: {exc}")


def verify() -> bool:
    expected = list(INTER_FACES.values()) + list(NOTO_WEIGHTS.values()) + list(PLEX_FILES.values())
    missing = [f for f in expected if not (FONT_DIR / f).exists()]
    if missing:
        log("MISSING: " + ", ".join(missing))
        return False
    log(f"ok      {len(expected)} static fonts in {FONT_DIR}")
    return True


def main() -> int:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    extract_inter()
    extract_noto_sc()
    fetch_plex()
    return 0 if verify() else 1


if __name__ == "__main__":
    sys.exit(main())
