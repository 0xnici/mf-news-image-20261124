#!/usr/bin/env python3
"""Build-time renderer for the 24 November 2026 one-image news front page.

Pillow is used ONLY here, at build time. The committed main.py never imports
this module or Pillow: it only validates and copies the pre-rendered PNG.
All illustration is original flat-vector geometry drawn with ImageDraw.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (245, 241, 232)
INK = (19, 23, 27)
RED = (190, 42, 37)
DEEP = (128, 33, 30)
GRAY = (110, 109, 102)
PALE = (223, 215, 200)
WHITE = (252, 249, 242)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FC = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"

ROOT = Path(__file__).resolve().parents[1]


def F(path, size):
    return ImageFont.truetype(path, size)


def put(d, xy, s, f, fill):
    d.text(xy, s, font=f, fill=fill)


def centered(d, box, s, f, fill):
    x0, y0, x1, y1 = box
    bb = d.textbbox((0, 0), s, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    put(d, (x0 + (x1 - x0 - w) // 2 - bb[0], y0 + (y1 - y0 - h) // 2 - bb[1]),
        s, f, fill)


def tracked(d, xy, s, f, fill, gap=2):
    x, y = xy
    for ch in s:
        put(d, (x, y), ch, f, fill)
        x += d.textlength(ch, font=f) + gap


def wrap(d, s, f, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------- original symbolic icons (no outside artwork) ----------

def icon_scales(d, cx, cy, c):
    d.line((cx - 21, cy + 17, cx + 21, cy + 17), fill=c, width=3)
    d.line((cx, cy - 21, cx, cy + 17), fill=c, width=3)
    d.line((cx - 21, cy - 13, cx + 21, cy - 13), fill=c, width=3)
    d.line((cx - 21, cy - 13, cx - 17, cy + 3), fill=c, width=2)
    d.line((cx - 17, cy + 3, cx - 7, cy + 3), fill=c, width=2)
    d.line((cx - 7, cy + 3, cx - 21, cy - 13), fill=c, width=2)
    d.line((cx + 21, cy - 13, cx + 17, cy + 3), fill=c, width=2)
    d.line((cx + 17, cy + 3, cx + 7, cy + 3), fill=c, width=2)
    d.line((cx + 7, cy + 3, cx + 21, cy - 13), fill=c, width=2)
    d.ellipse((cx - 3, cy - 24, cx + 3, cy - 18), fill=c)


def icon_tanker(d, cx, cy, c):
    # Upright tanker plus a clearly separate drifting mine.
    d.polygon([(cx - 22, cy + 4), (cx + 19, cy + 4), (cx + 12, cy + 15),
               (cx - 15, cy + 15)], fill=c)
    d.rectangle((cx - 12, cy - 4, cx + 8, cy + 2), fill=c)
    for dy in (19, 24):
        d.line((cx - 23, cy + dy, cx - 10, cy + dy), fill=c, width=2)
        d.line((cx - 4, cy + dy, cx + 9, cy + dy), fill=c, width=2)
        d.line((cx + 15, cy + dy, cx + 23, cy + dy), fill=c, width=2)
    import math
    mx, my = cx + 16, cy - 15
    d.ellipse((mx - 6, my - 6, mx + 6, my + 6), fill=RED)
    for a in range(0, 360, 60):
        rx, ry = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line((mx + 5 * rx, my + 5 * ry, mx + 10 * rx, my + 10 * ry),
               fill=RED, width=2)


def icon_return(d, cx, cy, c):
    # House with an arrow coming back to it: "asked to return".
    d.polygon([(cx - 20, cy - 2), (cx, cy - 20), (cx + 20, cy - 2)],
              outline=c, width=3)
    d.rectangle((cx - 14, cy - 2, cx + 14, cy + 18), outline=c, width=3)
    d.rectangle((cx - 4, cy + 8, cx + 4, cy + 18), fill=c)
    d.line((cx - 32, cy + 9, cx - 21, cy + 9), fill=RED, width=4)
    d.polygon([(cx - 19, cy + 9), (cx - 27, cy + 4), (cx - 27, cy + 14)],
              fill=RED)


def icon_book(d, cx, cy, c):
    d.polygon([(cx - 23, cy - 13), (cx - 2, cy - 17), (cx - 2, cy + 17),
               (cx - 23, cy + 12)], outline=c, width=3)
    d.polygon([(cx + 23, cy - 13), (cx + 2, cy - 17), (cx + 2, cy + 17),
               (cx + 23, cy + 12)], outline=c, width=3)
    d.line((cx, cy - 16, cx, cy + 16), fill=c, width=2)
    d.line((cx - 18, cy - 4, cx - 7, cy - 6), fill=c, width=2)
    d.line((cx + 7, cy - 6, cx + 18, cy - 4), fill=c, width=2)


def icon_warship(d, cx, cy, c):
    # Half-submerged hull: no explosion, so it cannot be confused with the mine tile.
    d.polygon([(cx - 23, cy + 1), (cx + 20, cy + 1), (cx + 13, cy + 16),
               (cx - 16, cy + 16)], fill=c)
    d.rectangle((cx - 7, cy - 11, cx + 7, cy + 1), fill=c)
    d.line((cx, cy - 22, cx, cy - 11), fill=c, width=3)
    for xa, xb in ((-25, -12), (-6, 8), (14, 24)):
        d.line((cx + xa, cy + 8, cx + xb, cy + 8), fill=PAPER, width=4)
    d.line((cx - 24, cy + 15, cx + 24, cy + 15), fill=c, width=2)
    d.line((cx - 18, cy + 21, cx + 18, cy + 21), fill=c, width=2)


def icon_flame(d, cx, cy, c):
    d.polygon([(cx, cy - 23), (cx + 13, cy - 3), (cx + 15, cy + 14),
               (cx, cy + 20), (cx - 15, cy + 14), (cx - 13, cy - 3)], fill=RED)
    d.polygon([(cx, cy - 5), (cx + 7, cy + 7), (cx + 6, cy + 15),
               (cx, cy + 18), (cx - 7, cy + 15), (cx - 6, cy + 7)], fill=c)


def icon_factory(d, cx, cy, c):
    d.polygon([(cx - 22, cy + 18), (cx - 22, cy - 2), (cx - 8, cy + 8),
               (cx - 8, cy - 2), (cx + 6, cy + 8), (cx + 6, cy - 8),
               (cx + 20, cy - 8), (cx + 20, cy + 18)], outline=c, width=3)
    d.rectangle((cx + 10, cy - 21, cx + 17, cy - 9), fill=RED)
    d.line((cx - 16, cy + 11, cx - 16, cy + 17), fill=c, width=2)
    d.line((cx - 2, cy + 11, cx - 2, cy + 17), fill=c, width=2)


def icon_doc(d, cx, cy, c):
    d.polygon([(cx - 17, cy - 22), (cx + 8, cy - 22), (cx + 19, cy - 11),
               (cx + 19, cy + 21), (cx - 17, cy + 21)], outline=c, width=3)
    d.line((cx + 8, cy - 22, cx + 8, cy - 11), fill=c, width=2)
    d.line((cx + 8, cy - 11, cx + 19, cy - 11), fill=c, width=2)
    for yy in (cy - 2, cy + 7, cy + 15):
        d.line((cx - 11, yy, cx + 12, yy), fill=c, width=2)
    d.line((cx - 21, cy + 24, cx + 22, cy - 25), fill=RED, width=4)


def icon_gavel(d, cx, cy, c):
    d.polygon([(cx - 19, cy - 18), (cx + 2, cy - 23), (cx + 12, cy - 5),
               (cx - 9, cy)], fill=c)
    d.line((cx - 8, cy - 3, cx + 18, cy + 20), fill=c, width=4)
    d.line((cx - 16, cy + 22, cx + 22, cy + 22), fill=c, width=3)


ICON = [icon_scales, icon_tanker, icon_return, icon_book, icon_warship,
        icon_flame, icon_factory, icon_doc, icon_gavel]

TILES = [
    ("WORLD · ICJ", "ICJ FINDS MYANMAR", "GENOCIDE", icon_scales),
    ("MIDEAST · IRAN", "IRAN SAYS 3", "TANKERS HIT MINES", icon_tanker),
    ("ASIA · BANGLADESH", "HASINA ASKS TO", "RETURN DEC 16", icon_return),
    ("VATICAN", "PAPAL DIARY", "PUBLISHED", icon_book),
    ("EUROPE · UKRAINE", "UKRAINE SAYS", "WARSHIP SUNK", icon_warship),
    ("AFRICA · ZANZIBAR", "NUNGWI HOTELS BURN ·", "TOURISTS EVACUATE", icon_flame),
    ("ASIA · INDONESIA", "FACTORY FIRE", "SEARCH CONTINUES", icon_factory),
    ("EUROPE · EU", "EU PROPOSES NEW", "RUSSIA SANCTIONS", icon_doc),
    ("US · COURT", "COURT CLEARS IOWA", "EXPLOSIVES PLAN", icon_gavel),
]


def masthead(d):
    d.rectangle((0, 0, W, 176), fill=INK)
    d.rectangle((0, 0, W, 12), fill=RED)
    tracked(d, (36, 28), "WORLD  ·  ONE DAY  ·  ONE IMAGE",
            F(FB, 16), PALE, gap=1)
    put(d, (33, 49), "TUESDAY", F(FB, 68), WHITE)
    put(d, (35, 122), "24 NOVEMBER 2026", F(FC, 50), WHITE)
    d.rectangle((812, 12, 1024, 176), fill=RED)
    centered(d, (812, 18, 1024, 132), "24", F(FB, 100), WHITE)
    centered(d, (812, 130, 1024, 170), "NOV 2026", F(FB, 18), WHITE)


def lead(d):
    # Ink illustration field, x 0..560.
    d.rectangle((0, 176, 560, 600), fill=INK)
    d.ellipse((214, 204, 502, 492), fill=DEEP)

    # Hand-authored flat-vector figure: CEO with signature glasses.
    d.polygon([(38, 600), (38, 544), (82, 502), (238, 502), (282, 544),
               (282, 600)], fill=PAPER)
    d.polygon([(138, 474), (192, 474), (192, 514), (165, 532),
               (138, 514)], fill=PAPER)
    d.ellipse((112, 366, 218, 482), fill=PAPER)
    d.polygon([(109, 420), (112, 392), (136, 364), (194, 364), (218, 392),
               (221, 420), (205, 398), (190, 384), (140, 384),
               (125, 400)], fill=INK)
    for box in ((121, 414, 167, 446), (170, 414, 216, 446)):
        d.rounded_rectangle(box, radius=8, outline=INK, width=5)
    d.line((167, 428, 170, 428), fill=INK, width=5)
    d.polygon([(150, 508), (165, 536), (180, 508)], fill=INK)

    # GPU chip with pins.
    for i in range(5):
        y = 292 + i * 36
        d.rectangle((258, y, 272, y + 14), fill=RED)
        d.rectangle((478, y, 492, y + 14), fill=RED)
    for i in range(5):
        x = 306 + i * 37
        d.rectangle((x, 256, x + 14, 270), fill=RED)
        d.rectangle((x, 450, x + 14, 464), fill=RED)
    d.rounded_rectangle((270, 270, 480, 450), radius=18,
                        fill=PAPER, outline=RED, width=7)
    d.rounded_rectangle((308, 308, 442, 412), radius=8, fill=INK)
    centered(d, (308, 308, 442, 412), "GPU", F(FB, 40), PAPER)

    # Rising market arrow (drawn last, runs just right of the chip).
    d.line((450, 566, 500, 460, 528, 358, 548, 264), fill=RED, width=16, joint="curve")
    d.polygon([(552, 250), (520, 266), (542, 298)], fill=RED)

    # Lead copy, right column.
    d.rounded_rectangle((584, 198, 790, 232), radius=4, fill=RED)
    centered(d, (584, 198, 790, 232), "THE LEAD", F(FB, 16), WHITE)
    put(d, (578, 240), "HUANG", F(FC, 88), INK)
    put(d, (580, 326), "REINSTATED", F(FC, 74), INK)
    d.rectangle((584, 408, 1004, 413), fill=RED)
    body = F(FR, 21)
    lines = wrap(d, "Nvidia CEO returns after a board reversal under Trump "
                    "pressure. Shares jump about 30%; US stocks rebound.",
                 body, 424)
    for i, line in enumerate(lines[:4]):
        put(d, (584, 426 + i * 31), line, body, INK)
    put(d, (584, 562), "WALL STREET · TECH", F(FB, 15), RED)


def numbers(d):
    d.rectangle((0, 600, W, 716), fill=INK)
    for x in (256, 512, 768):
        d.rectangle((x - 1, 612, x + 1, 704), fill=RED)
    cells = [
        ("≈30%", "NVIDIA SHARES (ABOUT)"),
        ("≈$1T", "MARKET VALUE ADDED"),
        ("$43.9B", "CROWDSTRIKE–ZSCALER"),
        ("258+", "DEMOCRAT HOUSE SEATS"),
    ]
    for i, (value, label) in enumerate(cells):
        x0 = i * 256 + 18
        put(d, (x0, 614), value, F(FB, 46), PAPER)
        put(d, (x0, 684), label, F(FB, 13), PALE)
    d.rectangle((0, 716, W, 752), fill=RED)
    put(d, (24, 721), "THE REST OF THE DAY", F(FC, 27), WHITE)
    put(d, (812, 727), "9 STORIES · 7 REGIONS", F(FB, 14), WHITE)


def tiles(d):
    xs, ys = [0, 341, 682, 1024], [752, 835, 918, 1000]
    for x in xs[1:-1]:
        d.rectangle((x - 1, 752, x + 1, 1000), fill=INK)
    for y in ys[1:-1]:
        d.rectangle((0, y - 1, 1024, y + 1), fill=INK)
    for idx, (region, line1, line2, icon) in enumerate(TILES):
        r, c = divmod(idx, 3)
        x0, y0 = xs[c], ys[r]
        icon(d, x0 + 35, y0 + 43, INK)
        put(d, (x0 + 70, y0 + 7), region, F(FB, 11), RED)
        head = F(FC, 24)
        put(d, (x0 + 68, y0 + 22), line1, head, INK)
        put(d, (x0 + 68, y0 + 47), line2, head, INK)


def footer(d):
    d.rectangle((0, 1000, W, 1004), fill=RED)
    put(d, (24, 1008),
        "COMPILED FROM THE DAY'S REPORTING · 24 NOVEMBER 2026",
        F(FR, 13), INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead(d)
    numbers(d)
    tiles(d)
    footer(d)
    out = ROOT / "entry.png"
    img.save(out, format="PNG", optimize=True)
    img.verify()
    print(f"wrote {out} ({out.stat().st_size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
