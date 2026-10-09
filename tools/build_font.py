"""Build the site font, KT Sans, from Mona Sans.

Usage (from the repo root): npm run build:font
                        or: python tools/build_font.py
Needs: pip install fonttools brotli

Mona Sans is licensed under the SIL Open Font License 1.1 with the Reserved Font Name "Mona".
Subsetting a font counts as modifying it, and a modified font may not use a reserved name,
so the cut-down web file is renamed KT Sans. Only run this script to change the font file,
for example to add characters to UNICODES.
"""
import io
import urllib.request
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
OUT_FONT = ROOT / "assets/fonts/kt-sans-latin-var.woff2"
OUT_LICENSE = ROOT / "assets/fonts/LICENSE-kt-sans.txt"

# Pinned upstream release: https://github.com/github/mona-sans
TAG = "v2.0.27"
SOURCE = f"https://raw.githubusercontent.com/github/mona-sans/{TAG}/fonts/variable/MonaSansVF%5Bwdth,opsz,wght%5D.ttf"
SOURCE_LICENSE = f"https://raw.githubusercontent.com/github/mona-sans/{TAG}/OFL.txt"

# The site uses normal to expanded widths and regular to extra-bold weights. Optical size is fixed
# at 20, Mona Sans' standard design: keeping the whole axis would add about 55 KB.
AXIS_LIMITS = {"wdth": (100, 125), "wght": (400, 800), "opsz": 20}

# Google Fonts' Latin range, plus arrows for links such as "All projects ->".
# Keep in sync with unicode-range in sass/base/_fonts.scss.
UNICODES = (
    "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
    "U+2000-206F, U+20AC, U+2122, U+2190-2199, U+2212, U+2215, U+FEFF, U+FFFD"
)

FEATURES = [
    "kern", "mark", "mkmk", "ccmp", "locl", "liga", "rlig", "rvrn",
    "case", "tnum", "pnum", "frac", "numr", "dnom", "sups", "subs", "sinf", "ordn",
    "ss01", "ss02", "ss03", "ss04", "ss05", "ss06", "ss07", "ss08", "ss09", "ss10",
]

NEW_NAME = "KT Sans"

# Copyright, trademark, maker, designer, description, URLs and licence keep their original text.
ATTRIBUTION_NAME_IDS = {0, 7, 8, 9, 10, 11, 12, 13, 14}

LICENSE_HEADER = f"""KT Sans is a modified version of Mona Sans {TAG} (https://github.com/github/mona-sans).
Changes: subset to Latin characters and arrows, width axis limited to 100-125,
weight axis limited to 400-800, optical size fixed at 20, and renamed, as the
licence below requires for modified versions that cannot use the Reserved Font
Name "Mona".
The complete original font is available from the address above.

"""


def parse_unicodes(spec):
    codes = []
    for part in spec.replace("U+", "").split(","):
        start, _, end = part.strip().partition("-")
        codes.extend(range(int(start, 16), int(end or start, 16) + 1))
    return codes


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def rename(font):
    names = [r for r in font["name"].names if r.nameID not in ATTRIBUTION_NAME_IDS]
    for record in names:
        text = record.toUnicode()
        renamed = text.replace("Mona Sans", NEW_NAME).replace("MonaSans", NEW_NAME.replace(" ", ""))
        if renamed != text:
            record.string = renamed
    leftover = [f"{r.nameID}: {r.toUnicode()}" for r in names if "Mona" in r.toUnicode()]
    if leftover:
        raise SystemExit(f"Reserved name still present in: {leftover}")


def main():
    font = TTFont(io.BytesIO(fetch(SOURCE)))
    font = instantiateVariableFont(font, AXIS_LIMITS)

    options = Options()
    options.layout_features = FEATURES
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.flavor = "woff2"
    subsetter = Subsetter(options)
    subsetter.populate(unicodes=parse_unicodes(UNICODES))
    subsetter.subset(font)

    rename(font)
    OUT_FONT.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = "woff2"
    font.save(OUT_FONT)
    OUT_LICENSE.write_text(LICENSE_HEADER + fetch(SOURCE_LICENSE).decode("utf-8"), encoding="utf-8", newline="\n")

    axes = ", ".join(f"{a.axisTag} {a.minValue:g}-{a.maxValue:g}" for a in font["fvar"].axes)
    print(f"{OUT_FONT.relative_to(ROOT)}: {OUT_FONT.stat().st_size // 1024} KB, {len(font.getGlyphOrder())} glyphs, axes {axes}")


if __name__ == "__main__":
    main()
