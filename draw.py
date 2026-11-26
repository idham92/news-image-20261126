#!/usr/bin/env python3
"""Render a one-page newspaper front page for 26 November 2026.

Layout (1024 x 1024, portrait broadsheet feel):
  masthead -> lead story (full width) -> 2x2 story grid -> markets band -> footer
All six stories are drawn with shared helpers so the page stays consistent.
"""
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"

PAGE = 1024
MARGIN = 48
CONTENT_W = PAGE - 2 * MARGIN

PAPER = (253, 252, 247)
INK = (17, 17, 17)
SOFT = (84, 84, 84)
ACCENT = (163, 18, 18)
BAND = (240, 237, 228)
RULE = (150, 150, 150)


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(canvas, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if canvas.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(canvas, x, y, lines, font, fill, leading):
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        canvas.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def headline_fit(canvas, text, start_size, max_width, max_lines, min_size=18):
    """Shrink the serif-bold headline until it wraps into max_lines."""
    size = start_size
    while size > min_size:
        font = load(SERIF_BOLD, size)
        lines = wrap_text(canvas, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = load(SERIF_BOLD, min_size)
    return font, wrap_text(canvas, text, font, max_width)


def kicker_line(canvas, x, y, label):
    font = load(SANS_BOLD, 18)
    canvas.text((x, y), label, font=font, fill=ACCENT)
    return y + 26


def story_block(canvas, x, y, width, kicker, headline, summary,
                head_size=27, max_head_lines=3, summary_size=19):
    """One grid story: kicker, headline, summary. Returns bottom y."""
    y = kicker_line(canvas, x, y, kicker)
    font, lines = headline_fit(canvas, headline, head_size, width, max_head_lines)
    y = draw_lines(canvas, x, y, lines, font, INK, int(head_size * 1.18))
    y += 6
    sfont = load(SANS, summary_size)
    slines = wrap_text(canvas, summary, sfont, width)
    return draw_lines(canvas, x, y, slines, sfont, SOFT, int(summary_size * 1.35))


def build_page():
    sheet = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(sheet)

    # ---- Masthead ----
    eyebrow = load(SANS_BOLD, 20)
    d.text((PAGE // 2, 34), "WORLD NEWS", font=eyebrow, fill=ACCENT, anchor="ma")
    title = load(SERIF_BOLD, 58)
    d.text((PAGE // 2, 62), "THE WORLD IN ONE PAGE", font=title, fill=INK, anchor="ma")
    dateline = load(SANS, 21)
    d.text((PAGE // 2, 138), "THURSDAY, 26 NOVEMBER 2026", font=dateline,
           fill=SOFT, anchor="ma")
    d.line([(MARGIN, 172), (PAGE - MARGIN, 172)], fill=INK, width=4)
    d.line([(MARGIN, 180), (PAGE - MARGIN, 180)], fill=INK, width=1)

    # ---- Lead story: Middle East, full width ----
    y = 200
    y = kicker_line(d, MARGIN, y, "MIDDLE EAST  —  OIL SHOCK")
    font, lines = headline_fit(
        d, "Houthis claim strike on Saudi Arabia's biggest refinery",
        40, CONTENT_W, 2)
    y = draw_lines(d, MARGIN, y, lines, font, INK, 48)
    y += 8
    sfont = load(SANS, 22)
    slines = wrap_text(
        d,
        "Brent crude tops $94 after Houthi forces claim attacks on the "
        "Ras Tanura refinery and Riyadh's financial district.",
        sfont, CONTENT_W)
    y = draw_lines(d, MARGIN, y, slines, sfont, SOFT, 30)
    y += 14
    d.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=RULE, width=1)
    y += 18

    # ---- 2 x 2 grid ----
    col_w = (CONTENT_W - 32) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + 32
    grid_top = y

    end_l1 = story_block(
        d, left_x, grid_top, col_w,
        "TRADE  —  US TARIFFS",
        "US proposes new tariffs on 14 trading partners",
        "Highest rates aimed at China over excess industrial capacity; "
        "Taiwan faces up to 15%.")
    end_r1 = story_block(
        d, right_x, grid_top, col_w,
        "KOREA  —  NUCLEAR",
        "Kim orders wider deployment of tactical nuclear weapons",
        "North Korea's leader says nuclear material production capacity is "
        "being systematically expanded (KCNA).")
    row2_y = max(end_l1, end_r1) + 20
    d.line([(MARGIN, row2_y - 10), (PAGE - MARGIN, row2_y - 10)], fill=RULE, width=1)

    end_l2 = story_block(
        d, left_x, row2_y, col_w,
        "UKRAINE  —  AIR BASE",
        "Ukraine says it struck a major Russian air base",
        "Kyiv claims five planes damaged in the strike.")
    end_r2 = story_block(
        d, right_x, row2_y, col_w,
        "SPACE  —  TIANGONG",
        "First Pakistani astronaut joins China's space station",
        "Muhammad Zeeshan Ali is the first foreign astronaut to travel to "
        "Tiangong on Shenzhou-24.")
    grid_bottom = max(end_l2, end_r2)
    mid_x = MARGIN + col_w + 16
    d.line([(mid_x, grid_top), (mid_x, grid_bottom)], fill=RULE, width=1)

    # ---- Markets band ----
    band_top = grid_bottom + 16
    band_h = 104
    d.rectangle([(MARGIN, band_top), (PAGE - MARGIN, band_top + band_h)], fill=BAND)
    d.line([(MARGIN, band_top), (PAGE - MARGIN, band_top)], fill=ACCENT, width=3)
    bx, by = MARGIN + 20, band_top + 14
    by = kicker_line(d, bx, by, "MARKETS  —  TAIWAN")
    mfont, mlines = headline_fit(
        d, "Taiwan shares plunge 1,927 points", 26, CONTENT_W - 40, 1)
    by = draw_lines(d, bx, by, mlines, mfont, INK, 30)
    msum = load(SANS, 18)
    d.text((bx, by + 2),
           "Stocks fall to 38,195 as the NT dollar weakens past 33 per dollar "
           "on US tariff fears.",
           font=msum, fill=SOFT)

    # ---- Footer ----
    foot_y = band_top + band_h + 22
    d.line([(MARGIN, foot_y), (PAGE - MARGIN, foot_y)], fill=INK, width=2)
    sfont = load(SANS, 16)
    d.text((PAGE // 2, foot_y + 10),
           "Sources: Reuters · BBC · CNN · KCNA · SimpleLife.news",
           font=sfont, fill=SOFT, anchor="ma")

    sheet.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build_page()
