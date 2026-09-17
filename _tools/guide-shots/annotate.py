"""Crop the dev-site captures (h-*.png) and draw numbered callouts that match the guide's steps.

Captures are lossless PNGs at native screen resolution, taken with the page at CSS zoom 1.75
(the browser extension's zoom action on a sub-region of the viewport; full-frame screenshots
are downscaled JPEGs and look blurry). Box coordinates are in each capture's own pixels.
Output: ../../assets/img/<name>.png. Never save these as JPEG.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "assets" / "img"
RED = (222, 53, 11)
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
SIDEBAR_EDGE = 359  # x of Jira's sidebar border in the full-width captures

# name: (capture, crop box, hide sidebar sliver?, [(label, box, badge position), ...])
SHOTS = {
    "open-recert": ("h-home.png", (0, 0, 1526, 705), False, [
        ("1", (18, 176, 348, 286), "tl"),
        ("2", (396, 196, 1470, 697), "tl"),
    ]),
    "take-snapshot": ("h-campaigns.png", (355, 175, 1505, 590), True, [
        ("1", (809, 347, 1109, 390), "tl"),
    ]),
    "snapshot-started": ("h-snapshot.png", (355, 65, 1505, 330), True, [
        ("2", (397, 197, 1473, 265), "left"),
    ]),
    "campaign-controls": ("h-campaigns.png", (355, 175, 1505, 420), True, [
        ("1", (399, 242, 1467, 291), "left"),
        ("2", (399, 295, 1467, 345), "left"),
        ("3", (399, 347, 534, 390), "below"),
    ]),
    "create-campaign": ("h-campaigns.png", (355, 225, 1505, 420), True, [
        ("6", (535, 347, 807, 390), "below"),
    ]),
    "plan-table": ("h-plan.png", (355, 255, 1505, 530), True, [
        ("4", (397, 367, 459, 519), "left"),
        ("5", (1249, 361, 1471, 523), "left"),
    ]),
    "evidence-button": ("h-plan.png", (355, 45, 1505, 220), True, [
        ("1", (1223, 75, 1369, 211), "left"),
    ]),
    "evidence": ("h-evidence.png", (355, 15, 1505, 335), True, [
        ("2", (399, 57, 1471, 108), "left"),
        ("3", (399, 111, 707, 154), "left"),
        ("4", (399, 167, 1471, 325), "left"),
    ]),
    "review": ("h-review.png", (355, 140, 1505, 630), True, [
        ("1", (397, 417, 881, 541), "left"),
        ("2", (397, 305, 1483, 359), "left"),
        ("3", (1049, 445, 1313, 535), "right"),
        ("4", (397, 575, 601, 623), "left"),
    ]),
    "review-listed": ("h-listed.png", (0, 0, 1179, 417), False, [
        ("5", (44, 12, 1135, 410), "left"),
    ]),
}


def badge(d, label, x, y):
    r = 18
    d.ellipse((x - r, y - r, x + r, y + r), fill=RED, outline="white", width=3)
    d.text((x, y), label, font=FONT, fill="white", anchor="mm")


def badge_xy(pos, x0, y0, x1, y1):
    if pos == "tl":
        return x0, y0
    if pos == "below":
        return (x0 + x1) // 2, y1 + 20
    if pos == "right":
        return x1 + 26, (y0 + y1) // 2
    return x0 - 24, (y0 + y1) // 2


for name, (src, crop, hide_sidebar, marks) in SHOTS.items():
    im = Image.open(HERE / src).convert("RGB")
    d = ImageDraw.Draw(im)
    if hide_sidebar:
        d.rectangle((crop[0], crop[1], SIDEBAR_EDGE, crop[3]), fill="white")
    for _, box, _ in marks:
        d.rounded_rectangle(box, radius=8, outline=RED, width=4)
    for label, box, pos in marks:
        badge(d, label, *badge_xy(pos, *box))
    out = im.crop(crop)
    out.save(OUT / f"{name}.png", optimize=True)
    print(name, out.size)
