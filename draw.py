#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Hand-written for the make.fun news-image-20261126 bounty.
All six stories were reported on 26 November 2026.
Layout follows the 25 November front page: navy masthead, gold accents,
six numbered story blocks, navy footer with sources.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 242, 231)
NAVY = (16, 36, 62)
GOLD = (232, 184, 75)
RED = (179, 39, 30)
INK = (17, 17, 17)
GREY = (70, 70, 70)
LIGHT = (220, 226, 235)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

F_KICKER = font("DejaVuSans-Bold.ttf", 20)
F_MAST = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 42)
F_SUB = font("DejaVuSans.ttf", 21)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_SUM = font("DejaVuSans.ttf", 21)
F_NUM = font("DejaVuSans-Bold.ttf", 26)
F_FOOT = font("DejaVuSans.ttf", 18)

STORIES = [
    ("MIDDLE EAST  \u2014  OIL SHOCK", "Houthis claim strike on Saudi Arabia's biggest refinery",
     "Brent crude tops $94 after Houthi forces claim attacks on the Ras Tanura refinery and Riyadh's financial district."),
    ("TRADE  \u2014  US TARIFFS", "US proposes new tariffs on 14 trading partners",
     "Highest rates aimed at China over excess industrial capacity; Taiwan faces up to 15%."),
    ("KOREA  \u2014  NUCLEAR", "Kim orders wider deployment of tactical nuclear weapons",
     "North Korea's leader says nuclear material production capacity is being systematically expanded (KCNA)."),
    ("UKRAINE  \u2014  AIR BASE", "Ukraine says it struck a major Russian air base",
     "Kyiv claims five planes damaged in the strike."),
    ("SPACE  \u2014  TIANGONG", "First Pakistani astronaut joins China's space station",
     "Muhammad Zeeshan Ali is the first foreign astronaut to travel to Tiangong on Shenzhou-24."),
    ("MARKETS  \u2014  TAIWAN", "Taiwan shares plunge 1,927 points",
     "Stocks fall to 38,195 as the NT dollar weakens past 33 per dollar on US tariff fears."),
]

ACCENTS = [(179, 39, 30), (16, 90, 120), (120, 60, 140), (30, 110, 70), (170, 110, 20), (40, 60, 160)]

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def head_font(draw, text, max_w):
    """Largest bold headline size (29 down to 22) that fits on one line."""
    for size in range(29, 21, -1):
        fnt = font("DejaVuSans-Bold.ttf", size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
    return font("DejaVuSans-Bold.ttf", 22)

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.text((32, 18), "T H E   W O R L D   I N   O N E   P A G E", font=F_KICKER, fill=GOLD)
    d.text((30, 48), "WORLD NEWS", font=F_MAST, fill=WHITE)
    d.text((32, 122), "THURSDAY, 26 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((32, 168), "Six stories that defined the day \u2014 as reported on 26 November 2026",
           font=F_SUB, fill=LIGHT)
    d.rectangle([0, 196, W, 204], fill=RED)

    # ---- Stories ----
    top, block_h = 204, 127
    x_num, x_txt = 28, 104
    txt_w = W - x_txt - 30
    for i, (tag, head, summ) in enumerate(STORIES):
        y = top + i * block_h
        accent = ACCENTS[i]
        d.rectangle([x_num, y + 14, x_num + 54, y + 68], fill=accent)
        num = str(i + 1)
        nw = d.textlength(num, font=F_NUM)
        d.text((x_num + (54 - nw) / 2, y + 24), num, font=F_NUM, fill=WHITE)
        d.text((x_txt, y + 12), tag, font=F_TAG, fill=RED)
        d.text((x_txt, y + 38), head, font=head_font(d, head, txt_w), fill=INK)
        lines = wrap(d, summ, F_SUM, txt_w)
        assert len(lines) <= 2, f"story {i + 1} summary wraps to {len(lines)} lines: {lines}"
        ly = y + 74
        for ln in lines[:2]:
            d.text((x_txt, ly), ln, font=F_SUM, fill=GREY)
            ly += 26
        if i < len(STORIES) - 1:
            d.line([(x_txt, y + block_h - 8), (W - 30, y + block_h - 8)],
                   fill=(200, 192, 175), width=1)

    # ---- Footer ----
    fy = top + len(STORIES) * block_h  # 966
    d.rectangle([0, fy, W, H], fill=NAVY)
    foot = "Sources: Reuters  \u00b7  BBC  \u00b7  CNN  \u00b7  KCNA  \u00b7  SimpleLife.news"
    d.text((32, fy + 12), foot, font=F_FOOT, fill=LIGHT)
    d.text((32, fy + 34), "An AI-made front page for make.fun \u2014 one day, one image.",
           font=F_FOOT, fill=GOLD)

    img.save("/home/hatch/workspace/makefun/news-image-work/news-image-20261126/entry.png",
             optimize=True)
    print("saved")

if __name__ == "__main__":
    main()
