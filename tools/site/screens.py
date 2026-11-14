#!/usr/bin/env python3
"""Copies the app's own screens into site/screens as small WebP, for the phones, the tablet and the foldable.

The screens are the app's screenshot references, which its CI renders and checks (English). They are large PNGs
(several MB together), so they are cut to what a device shows and scaled to twice the size the page sets them at, then
saved as WebP. Run it after the app's screenshots change, with the path to a checkout of joeldenke/Novila:

    python3 tools/site/screens.py ../Novila

Needs Pillow (pip install pillow). The site's builder only copies site/screens and stays standard library only.
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site" / "screens"
REFS = "src/test/screenshots/se.novila.feature"

# A phone shows the top of a screen at 1078 x 2400 px (a 20:9 phone at 2.625x); the page sets it at most 300 px wide.
PHONE = (1078, 2400)
PHONE_WIDTH = 600
QUALITY = 82

# name: (screenshot reference in the app, the part a device shows or None for all of it, width in px)
SCREENS = {
    "today": (f"feature/today/{REFS}.today.TodayScreenKt.TodayScreenPreview.H1400dp.png", PHONE, PHONE_WIDTH),
    "training": (
        f"feature/training/{REFS}.training.TrainingScreenKt.TrainingScreenPreview.H1600dp_WITH_BACKGROUND.png",
        PHONE,
        PHONE_WIDTH,
    ),
    "sleep": (
        f"feature/sleep/{REFS}.sleep.SleepScreenKt.SleepScreenPreview.H1000dp_WITH_BACKGROUND.png",
        PHONE,
        PHONE_WIDTH,
    ),
    "nutrition": (
        f"feature/nutrition/{REFS}.nutrition.NutritionScreenKt.NutritionScreenPreview.H1200dp_WITH_BACKGROUND.png",
        PHONE,
        PHONE_WIDTH,
    ),
    "tablet": (f"feature/today/{REFS}.today.TodayScreenKt.TodayScreenLandscapePreview.W1200dp_H800dp.png", None, 1600),
    "foldable": (
        f"feature/training/{REFS}.training.TrainingScreenKt.TrainingScreenFoldablePreview"
        ".W852dp_H880dp_WITH_BACKGROUND.png",
        None,
        1200,
    ),
}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: screens.py <path to a checkout of joeldenke/Novila>")
    app = Path(sys.argv[1])
    OUT.mkdir(exist_ok=True)
    for name, (source, part, width) in SCREENS.items():
        image = Image.open(app / source).convert("RGB")
        if part:
            if image.width < part[0] or image.height < part[1]:
                sys.exit(f"{source} is {image.size}, smaller than the {part} a device shows")
            image = image.crop((0, 0, *part))
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
        target = OUT / f"{name}.webp"
        image.save(target, "WEBP", quality=QUALITY, method=6)
        print(f"{target.relative_to(ROOT)}  {image.width}x{image.height}  {target.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
