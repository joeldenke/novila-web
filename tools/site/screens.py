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

# A phone shows the top of a screen at 20:9 (1078 x 2400 px on a 2.625x phone); the page sets it at most 300 px wide.
PHONE = 2400 / 1078
PHONE_WIDTH = 600
QUALITY = 82

T = "feature/training/" + REFS + ".training."
S = "feature/sleep/" + REFS + ".sleep."
N = "feature/nutrition/" + REFS + ".nutrition."
D = "feature/today/" + REFS + ".today."

# name: (screenshot reference in the app, the height a device shows as a share of the width or None for all of it,
# width in px)
SCREENS = {
    "today": (D + "TodayScreenKt.TodayScreenPreview.H1400dp.png", PHONE, PHONE_WIDTH),
    "training": (T + "TrainingScreenKt.TrainingScreenPreview.H1600dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "sleep": (S + "SleepScreenKt.SleepScreenPreview.H1000dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "nutrition": (N + "NutritionScreenKt.NutritionScreenPreview.H1200dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "workout": (T + "WorkoutScreenKt.WorkoutSetPreview.H1100dp.png", PHONE, PHONE_WIDTH),
    "exercise": (T + "ExerciseDetailScreenKt.ExerciseDetailPreview.H1400dp.png", PHONE, PHONE_WIDTH),
    "sleep-week": (S + "SleepTrendsScreenKt.SleepTrendsScreenPreview.H1400dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "sleep-coach": (S + "SleepCoachScreenKt.SleepCoachScreenPreview.H2200dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "recipes": (N + "RecipesScreenKt.RecipesScreenPreview.H1200dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "recipe": (N + "RecipesScreenKt.RecipesScreenOpenPreview.H1600dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "insights": (D + "DiscoveriesScreenKt.DiscoveriesScreenPreview.H2600dp_WITH_BACKGROUND.png", PHONE, PHONE_WIDTH),
    "breathing": (
        "feature/breathing/" + REFS + ".breathing.BreathingSessionScreenKt.BreathingSessionScreenPreview"
        ".H1400dp_WITH_BACKGROUND.png",
        PHONE,
        PHONE_WIDTH,
    ),
    "habits": ("feature/settings/" + REFS + ".settings.MyHabitsScreenKt.MyHabitsPreview.H900dp_NIGHT.png", PHONE, 600),
    "widget": ("feature/widget/" + REFS + ".widget.NovilaWidget.Large.png", None, 720),
    "tablet": (D + "TodayScreenKt.TodayScreenLandscapePreview.W1200dp_H800dp.png", None, 1600),
    "foldable": (
        T + "TrainingScreenKt.TrainingScreenFoldablePreview.W852dp_H880dp_WITH_BACKGROUND.png",
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
            height = round(image.width * part)
            if image.height < height:
                sys.exit(f"{source} is {image.size}, shorter than the {height} px a device shows")
            image = image.crop((0, 0, image.width, height))
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
        target = OUT / f"{name}.webp"
        image.save(target, "WEBP", quality=QUALITY, method=6)
        print(f"{target.relative_to(ROOT)}  {image.width}x{image.height}  {target.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
