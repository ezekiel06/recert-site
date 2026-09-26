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
    # Captures retaken 2026-09-26 from a real customer install (recert-standin) running
    # production 4.10.0, light theme, Jira sidebar collapsed, page at CSS zoom 1.5 and the whole
    # frame captured so wide tables (the Decision column, the CSV preview) are not cut off.
    # Boxes are in each capture's own pixels; h-home/h-listed are the older dev-site captures.
    "open-recert": ("h-home.png", (0, 0, 1526, 705), False, [
        ("1", (18, 176, 348, 286), "tl"),
        ("2", (396, 196, 1470, 697), "tl"),
    ]),
    "take-snapshot": ("h-campaigns.png", (0, 60, 1530, 320), False, [
        ("1", (441, 274, 711, 309), "tl"),
    ]),
    "snapshot-started": ("h-snapshot.png", (0, 55, 1530, 200), False, [
        ("2", (50, 140, 634, 184), "left"),
    ]),
    "campaign-controls": ("h-campaigns.png", (0, 120, 1530, 320), False, [
        ("1", (34, 180, 1510, 224), "left"),
        ("2", (34, 227, 1510, 271), "left"),
        ("3", (34, 274, 155, 309), "below"),
    ]),
    "create-campaign": ("h-campaigns.png", (0, 160, 1530, 320), False, [
        ("6", (153, 274, 441, 309), "below"),
    ]),
    "plan-table": ("h-plan.png", (0, 40, 1530, 310), False, [
        ("4", (34, 110, 144, 298), "tl"),
        ("5", (1231, 110, 1510, 298), "left"),
    ]),
    "evidence-button": ("h-campaigns.png", (0, 320, 1530, 560), False, [
        ("1", (1168, 358, 1298, 552), "left"),
    ]),
    "evidence": ("h-evidence.png", (0, 35, 1530, 300), False, [
        ("2", (34, 42, 722, 76), "left"),
        ("3", (34, 78, 1510, 120), "left"),
        ("4", (34, 200, 1510, 298), "left"),
    ]),
    "review": ("h-review.png", (0, 35, 1530, 300), False, [
        ("1", (226, 112, 1184, 218), "tl"),
        ("2", (34, 88, 1510, 110), "left"),
        ("3", (1188, 118, 1504, 200), "left"),
        ("4", (34, 255, 214, 292), "left"),
    ]),
    "review-listed": ("h-review.png", (0, 300, 1530, 620), False, [
        ("5", (34, 395, 1510, 615), "tl"),
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


# A badge sits outside its box (left of it, or below it), so the capture is pasted onto a
# slightly larger white canvas first - otherwise the circles are cut off at the edges.
PAD = 58

for name, (src, crop, hide_sidebar, marks) in SHOTS.items():
    base = Image.open(HERE / src).convert("RGB")
    im = Image.new("RGB", (base.width + PAD, base.height + PAD), "white")
    im.paste(base, (PAD, 0))
    marks = [(label, (b[0] + PAD, b[1], b[2] + PAD, b[3]), pos) for label, b, pos in marks]
    crop = (crop[0], crop[1], crop[2] + PAD, crop[3] + PAD // 2)
    d = ImageDraw.Draw(im)
    if hide_sidebar:
        d.rectangle((crop[0], crop[1], SIDEBAR_EDGE + PAD, crop[3]), fill="white")
    for _, box, _ in marks:
        d.rounded_rectangle(box, radius=8, outline=RED, width=4)
    for label, box, pos in marks:
        badge(d, label, *badge_xy(pos, *box))
    out = im.crop(crop)
    out.save(OUT / f"{name}.png", optimize=True)
    print(name, out.size)
