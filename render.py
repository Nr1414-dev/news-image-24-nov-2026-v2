#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024 PNG).

Dark navy poster: masthead + date, a small globe motif, six numbered
story cards in big type, and a footer naming the day. Fixed data only,
no network, fully deterministic output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (11, 30, 58)
NAVY_LIGHT = (16, 44, 82)
CARD = (23, 58, 104)
CARD_EDGE = (58, 108, 168)
GOLD = (232, 184, 92)
WHITE = (245, 247, 250)
MUTED = (190, 205, 225)
INK = (8, 20, 38)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

ACCENTS = [
    (232, 90, 79),    # Estonia - red
    (232, 184, 92),   # Ukraine - gold
    (86, 190, 140),   # Nvidia - green
    (96, 165, 250),   # Nepal - blue
    (216, 130, 200),  # Gaza - mauve
    (120, 200, 210),  # COP31 - teal
]

STORIES = [
    ("1", "ESTONIA", "RUSSIA WARNS ESTONIA OF 'OPEN WAR'",
     "Moscow protests border closure from 1 Dec"),
    ("2", "UKRAINE", "ZELENSKY: RUSSIA PLANS NEW STRIKES",
     "Kyiv warns of fresh attacks after drone raid"),
    ("3", "NVIDIA", "HUANG IS BACK AT NVIDIA",
     "Board reinstates CEO; shares leap a third"),
    ("4", "NEPAL", "INDIA GIVES NEPAL $1.62BN",
     "Flood rebuild aid as Modi, Shah open rail link"),
    ("5", "GAZA", "UN WORKER KILLED IN GAZA STRIKE",
     "UNRWA staffer dies at Jabalia water well"),
    ("6", "COP31", "COP31 ENDS WITH NO DEAL",
     "Climate talks split over fossil fuels"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Small stylised globe: blue disc, meridians, latitude lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 180),
                 outline=(150, 200, 240), width=3)
    # latitude lines
    for frac, half in ((0.55, 0.83), (0.0, 1.0), (-0.55, 0.83)):
        y = cy + int(frac * r)
        hw = int(half * r)
        draw.line([cx - hw, y, cx + hw, y], fill=(150, 200, 240), width=2)
    # meridians (ellipses clipped by the disc outline look)
    for rx in (int(r * 0.45), int(r * 0.85)):
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r],
                     outline=(150, 200, 240), width=2)
    draw.ellipse([cx - int(r * 0.42), cy - int(r * 0.42),
                  cx - int(r * 0.05), cy - int(r * 0.05)],
                 fill=(190, 220, 245))


def draw_card(draw, x, y, w, h, num, kicker, headline, sub, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14,
                           fill=CARD, outline=CARD_EDGE, width=2)
    # accent bar on the left edge
    draw.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=accent)
    tx = x + 26
    # number badge
    draw.ellipse([tx, y + 18, tx + 44, y + 62], fill=accent)
    num_font = font(SANS_BOLD, 26)
    nw = draw.textlength(num, font=num_font)
    draw.text((tx + (44 - nw) / 2, y + 21), num, font=num_font, fill=INK)
    # kicker
    kick_font = font(SANS_BOLD, 19)
    draw.text((tx + 58, y + 28), kicker, font=kick_font, fill=GOLD)
    # headline, wrapped, up to 3 lines
    head_font = font(SANS_BOLD, 29)
    lines = wrap(draw, headline, head_font, w - 52)
    hy = y + 76
    for line in lines:
        draw.text((tx, hy), line, font=head_font, fill=WHITE)
        hy += 36
    # subhead, wrapped, up to 2 lines
    sub_font = font(SANS, 19)
    lines = wrap(draw, sub, sub_font, w - 52)
    sy = hy + 8
    for line in lines:
        draw.text((tx, sy), line, font=sub_font, fill=MUTED)
        sy += 26


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # faint top band
    draw.rectangle([0, 0, W, 196], fill=NAVY_LIGHT)
    draw.line([0, 196, W, 196], fill=GOLD, width=3)

    # globe motif, top-right corner (clear of the masthead text)
    draw_globe(draw, 960, 62, 32)

    # masthead
    mast_font = font(SERIF_BOLD, 46)
    mast = "THE WORLD IN ONE IMAGE"
    mw = draw.textlength(mast, font=mast_font)
    draw.text(((W - mw) / 2, 34), mast, font=mast_font, fill=WHITE)

    # date line
    date_font = font(SANS_BOLD, 27)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 102), date, font=date_font, fill=GOLD)

    # theme line
    theme_font = font(SANS_ITALIC, 22)
    theme = "Warnings, a comeback \u2014 and no climate deal."
    tw = draw.textlength(theme, font=theme_font)
    draw.text(((W - tw) / 2, 146), theme, font=theme_font, fill=MUTED)

    # six cards: 2 columns x 3 rows
    margin = 28
    gap = 16
    card_w = (W - 2 * margin - gap) // 2
    card_h = 218
    top = 216
    for i, (num, kicker, headline, sub) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw_card(draw, x, y, card_w, card_h, num, kicker, headline, sub,
                  ACCENTS[i])

    # footer
    foot_font = font(SANS_BOLD, 22)
    foot = "24 NOVEMBER 2026  \u2022  6 STORIES, ONE WORLD"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, 962), foot, font=foot_font, fill=GOLD)
    draw.line([margin, 946, W - margin, 946], fill=CARD_EDGE, width=2)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
