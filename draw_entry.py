#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: one 1024x1024 PNG summarising
Monday 23 November 2026 world news (morning snapshot, ~05:30 UTC —
see research-23nov.md; refresh due 25 Nov 07:00 WIB before submit).

Formula (top-20 study): 40 stories, 9 regions, 3 drawn panels,
newspaper layout — masthead, one full-width lead, a 3x13 grid of
short stories, one-line source footer. All text is ASCII only (the
minus sign is the plain hyphen "-"); any text that would overflow its
box aborts the run with an error instead of drawing outside it.

Deterministic: fixed fonts, fixed layout, no timestamps, so two runs
produce byte-identical PNG output.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
PAPER = (247, 243, 236)      # warm off-white page
INK = (22, 26, 34)           # near-black text
NAVY = (20, 33, 61)          # masthead band
NAVY_LINE = (232, 184, 75)   # gold rule under masthead
GOLD = (232, 184, 75)        # date colour on navy
CARD = (255, 255, 255)       # story cards
CARD_EDGE = (214, 206, 192)  # card border
MUTED = (96, 100, 110)       # secondary text
WHITE = (255, 255, 255)
LIGHT = (205, 212, 224)      # masthead subline
RED = (178, 34, 34)          # WAR lead / MARKETS
BLUE = (24, 78, 140)         # EUROPE
BROWN = (122, 74, 18)        # MIDEAST
TEAL = (13, 110, 109)        # E. ASIA
PURPLE = (88, 44, 120)       # S. ASIA
GREEN = (34, 110, 52)        # SE ASIA
CYAN = (0, 119, 139)         # OCEANIA
ROSE = (176, 48, 96)         # N. AMERICA
GOLD_D = (190, 140, 10)      # S. AMERICA
ORANGE = (200, 90, 30)       # AFRICA

FONT_DIR = "/usr/share/fonts/truetype/noto"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        raise SystemExit("missing font: %s" % path)
    return ImageFont.truetype(path, size)


F_TITLE = None   # set in main()
F_DATE = None
F_KICKER = None
F_SUB = None
F_TAG = None
F_HEAD = None
F_BODY = None
F_MINI = None
F_DRAW = None
F_FOOT = None


def check_ascii(text, where):
    for ch in text:
        if ord(ch) > 127:
            raise SystemExit("non-ASCII char %r in %s" % (ch, where))
    if "\u2212" in text:
        raise SystemExit("U+2212 minus sign found in %s" % where)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; aborts if a single word is wider than max_w."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if not cur:
                raise SystemExit("word too wide for its box: %r" % word)
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, max_lines, line_h, fill):
    """Draw wrapped text; abort if it needs more than max_lines lines."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) > max_lines:
        raise SystemExit(
            "text overflow: %d lines > %d allowed: %r"
            % (len(lines), max_lines, text[:60])
        )
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=fill)
    return y + len(lines) * line_h


def tag_chip(draw, x, y, label, colour):
    """Small filled tag chip; returns width used."""
    pad_x, pad_y = 8, 2
    w = int(draw.textlength(label, font=F_TAG)) + 2 * pad_x
    h = F_TAG.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=colour)
    draw.text((x + pad_x, y + pad_y - 1), label, font=F_TAG, fill=WHITE)
    return w, h


def draw_lead(draw, box):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                           outline=CARD_EDGE, width=2)
    draw.rounded_rectangle([x0, y0, x0 + 10, y1], radius=5, fill=RED)
    inner_x = x0 + 28
    inner_w = x1 - inner_x - 24
    y = y0 + 12
    tag_w, tag_h = tag_chip(draw, inner_x, y, "WAR - UKRAINE", RED)
    draw.text((inner_x + tag_w + 12, y + 1),
              "Overnight campaign - NATO emergency session today",
              font=F_SUB, fill=MUTED)
    y += tag_h + 6
    head = "Ukraine strikes deep into Russia as NATO meets"
    y = draw_wrapped(draw, head, F_HEAD, inner_x, y, inner_w, 1, 34, INK)
    y += 6
    body = (
        "Overnight drones hit the Kaleykino oil station in Tatarstan, "
        "1,500 km from the front, and the Novoshakhtinsk refinery; a "
        "Russian corvette sank off Libya. Three Russian missiles were "
        "confirmed in Poland on Nov 20; NATO holds an emergency session "
        "in Brussels today. In Dymer, nine were killed when a drone "
        "collapsed a block; Odesa is in blackout."
    )
    y = draw_wrapped(draw, body, F_BODY, inner_x, y, inner_w, 4, 21, INK)
    if y > y1 - 8:
        raise SystemExit("lead card overflow: text bottom %d > %d" % (y, y1 - 8))


def draw_mini(draw, box, tag, colour, head):
    """One dense grid cell: region tag + headline (max 2 lines)."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=CARD_EDGE, width=1)
    inner_x = x0 + 12
    inner_w = x1 - inner_x - 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    y = draw_wrapped(draw, head, F_MINI, inner_x, y0 + 19, inner_w,
                     2, 14, INK)
    if y > y1 - 1:
        raise SystemExit("mini %s overflow: text bottom %d > %d"
                         % (tag, y, y1 - 1))


def draw_chart(draw, box, tag, colour, head):
    """Drawn panel: tag + Bitcoin sparkline + one-line headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=CARD_EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # sparkline: daily closes Fri 58,952 - Sat 60,216 - Sun 60,784 - Mon 61,100
    vals = [58952, 60216, 60784, 61100]
    lo, hi = min(vals), max(vals)
    cx0, cx1 = inner_x, x1 - 60
    cy0, cy1 = y0 + 20, y0 + 31
    pts = []
    for i, v in enumerate(vals):
        px = cx0 + i * (cx1 - cx0) // 3
        py = cy1 - (v - lo) * (cy1 - cy0) // (hi - lo)
        pts.append((px, py))
    draw.line(pts, fill=BLUE, width=2)
    draw.ellipse([pts[-1][0] - 3, pts[-1][1] - 3,
                  pts[-1][0] + 3, pts[-1][1] + 3], fill=BLUE)
    draw.text((x1 - 56, y0 + 19), "$61k", font=F_DRAW, fill=BLUE)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("chart panel overflow: %d > %d" % (y, y1 - 1))


def draw_ship(draw, box, tag, colour, head):
    """Drawn panel: tag + tanker pictogram + one-line headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=CARD_EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # containers
    draw.rectangle([inner_x + 22, y0 + 20, inner_x + 44, y0 + 25],
                   fill=BROWN)
    draw.rectangle([inner_x + 48, y0 + 20, inner_x + 70, y0 + 25],
                   fill=TEAL)
    # hull
    draw.polygon([(inner_x + 12, y0 + 25), (inner_x + 84, y0 + 25),
                  (inner_x + 76, y0 + 31), (inner_x + 20, y0 + 31)],
                 fill=NAVY)
    # waves
    draw.line([(inner_x, y0 + 32), (x1 - 12, y0 + 32)], fill=TEAL, width=1)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("ship panel overflow: %d > %d" % (y, y1 - 1))


def draw_ballot(draw, box, tag, colour, head):
    """Drawn panel: tag + ballot-box pictogram + one-line headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=CARD_EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # ballot box
    bx0, by0, bx1, by1 = inner_x + 6, y0 + 20, inner_x + 26, y0 + 32
    draw.rectangle([bx0, by0, bx1, by1], outline=NAVY, width=2)
    draw.line([(bx0 + 4, by0 + 3), (bx1 - 4, by0 + 3)], fill=NAVY, width=2)
    draw.line([(bx0 + 3, by0 + 8), (bx0 + 8, by0 + 11),
               (bx0 + 15, by0 + 3)], fill=GREEN, width=2)
    draw.text((bx1 + 8, y0 + 20), "258+ seats", font=F_DRAW, fill=INK)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("ballot panel overflow: %d > %d" % (y, y1 - 1))


# (kind, tag, colour, headline) — kind: "mini", "chart", "ship", "ballot"
STORIES = [
    ("mini", "EUROPE", BLUE, "COP31 collapses with no deal; longest summit ever"),
    ("mini", "EUROPE", BLUE, "France rejects EU budget over farm income guarantees"),
    ("mini", "EUROPE", BLUE, "Thousands march on living costs in Lisbon, Paris, Madrid"),
    ("mini", "EUROPE", BLUE, "EU and Indonesia sign free-trade deal after a decade"),
    ("mini", "EUROPE", BLUE, "Germany gives spies wider powers against hybrid threats"),
    ("mini", "EUROPE", BLUE, "UK extends NHS Palantir data deal to 2029"),
    ("ship", "MIDEAST", BROWN, "Two tankers hit mines in Hormuz"),
    ("mini", "MIDEAST", BROWN, "Houthis claim strikes on Saudi oil refinery"),
    ("mini", "MIDEAST", BROWN, "Bahrain: two hurt as Iran strike hits civilian site"),
    ("mini", "MIDEAST", BROWN, "IDF warns Netanyahu: Iran strike risks wider war"),
    ("mini", "MIDEAST", BROWN, "Likud and Eisenkot end coalition talks with no deal"),
    ("mini", "MIDEAST", BROWN, "Gaza: nine killed; 1,600+ dead since ceasefire"),
    ("mini", "E. ASIA", TEAL, "Kospi falls 3.7% as AI selloff spreads; Seoul readies fund"),
    ("mini", "E. ASIA", TEAL, "South Korea minister quits over AI exam-cheating scandal"),
    ("mini", "E. ASIA", TEAL, "Japan quake M5.7 injures 22; trains halted"),
    ("mini", "E. ASIA", TEAL, "Kim Jong Un visits China via new Yalu River bridge"),
    ("mini", "E. ASIA", TEAL, "Taiwan shares down 17% in a week; short sales curbed"),
    ("mini", "E. ASIA", TEAL, "China cuts margin needs to 80% from November 30"),
    ("mini", "S. ASIA", PURPLE, "India now Asia's third most powerful nation"),
    ("mini", "S. ASIA", PURPLE, "Nepal PM Balen Shah begins first India visit"),
    ("mini", "S. ASIA", PURPLE, "India, China hold 10-day talks to ease border tensions"),
    ("mini", "SE ASIA", GREEN, "Indonesia factory fire: 3 dead, dozens missing"),
    ("mini", "SE ASIA", GREEN, "Selangor floods: 1,800+ evacuated in Malaysia"),
    ("mini", "OCEANIA", CYAN, "New Zealand election too close to call"),
    ("mini", "OCEANIA", CYAN, "Australian music promoter Molly Meldrum dies at 83"),
    ("mini", "OCEANIA", CYAN, "M6.5 quake hits Vanuatu region; deep, no tsunami alert"),
    ("ballot", "N. AMERICA", ROSE, "Democrats win House majority since 1992"),
    ("mini", "N. AMERICA", ROSE, "Nasdaq falls 5.3% in worst week since 2020"),
    ("mini", "N. AMERICA", ROSE, "Trump reposts 'TrumpCare' pitch; hits out at Schumer"),
    ("mini", "N. AMERICA", ROSE, "Chapo Isidro captured in Sinaloa; 11 killed in gunfight"),
    ("mini", "N. AMERICA", ROSE, "1,389 Indian children held in US custody since 2023"),
    ("mini", "S. AMERICA", GOLD_D, "Peru: 5,459 coastal animals dead; El Nino until Feb 2027"),
    ("mini", "S. AMERICA", GOLD_D, "Ecuador readies flood plan for November 29 vote"),
    ("mini", "S. AMERICA", GOLD_D, "Colombia: man hit by firebomb during protests"),
    ("mini", "AFRICA", ORANGE, "Sudan: drones hit Khartoum, damage UN building"),
    ("mini", "AFRICA", ORANGE, "WHO warns as fighting disrupts Ebola work in Congo"),
    ("mini", "AFRICA", ORANGE, "Nigeria boat capsizes; 29 mourners drowned"),
    ("mini", "AFRICA", ORANGE, "Ethiopia launches polio drive for 11m children"),
    ("chart", "MARKETS", RED, "Bitcoin holds above $61,000"),
]

DRAWERS = {"mini": draw_mini, "chart": draw_chart,
           "ship": draw_ship, "ballot": draw_ballot}


def main():
    global F_TITLE, F_DATE, F_KICKER, F_SUB, F_TAG
    global F_HEAD, F_BODY, F_MINI, F_DRAW, F_FOOT

    F_TITLE = load_font("NotoSans-Bold.ttf", 52)
    F_DATE = load_font("NotoSans-Bold.ttf", 26)
    F_KICKER = load_font("NotoSans-Bold.ttf", 18)
    F_SUB = load_font("NotoSans-Regular.ttf", 19)
    F_TAG = load_font("NotoSans-Bold.ttf", 11)
    F_HEAD = load_font("NotoSans-Bold.ttf", 28)
    F_BODY = load_font("NotoSans-Regular.ttf", 17)
    F_MINI = load_font("NotoSans-Bold.ttf", 13)
    F_DRAW = load_font("NotoSans-Bold.ttf", 13)
    F_FOOT = load_font("NotoSans-Regular.ttf", 16)

    if len(STORIES) != 39:
        raise SystemExit("story count must be 39 minis + lead = 40, got %d"
                         % len(STORIES))

    texts = [
        "THE WORLD IN ONE IMAGE",
        "WORLD NEWS",
        "Monday, November 23, 2026",
        "40 stories - 9 regions - 3 drawn - as reported on Monday",
    ]
    for t in texts:
        check_ascii(t, "masthead")
    for kind, tag, colour, head in STORIES:
        check_ascii(head, "story head " + tag)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------------
    mast_h = 116
    draw.rectangle([0, 0, W, mast_h], fill=NAVY)
    draw.rectangle([0, mast_h - 4, W, mast_h], fill=NAVY_LINE)
    draw.text((36, 8), "THE WORLD IN ONE IMAGE",
              font=F_KICKER, fill=GOLD)
    draw.text((36, 24), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    draw.text((36, 80), "Monday, November 23, 2026",
              font=F_DATE, fill=GOLD)
    sub = "40 stories - 9 regions - 3 drawn - as reported on Monday"
    sub_w = draw.textlength(sub, font=F_SUB)
    draw.text((W - 36 - sub_w, 12), sub, font=F_SUB, fill=LIGHT)

    # ---- lead story -----------------------------------------------------
    draw_lead(draw, (36, 124, W - 36, 292))

    # ---- 3x13 grid -------------------------------------------------------
    gx0, gy0 = 36, 300
    gw, gh, gap = 309, 48, 4
    for i, (kind, tag, colour, head) in enumerate(STORIES):
        col = i % 3
        row = i // 3
        x0 = gx0 + col * (gw + 12)
        y0 = gy0 + row * (gh + gap)
        DRAWERS[kind](draw, (x0, y0, x0 + gw, y0 + gh), tag, colour, head)

    # ---- footer ----------------------------------------------------------
    foot = ("Sources: Reuters - AP - BBC - Al Jazeera - CNN - Finnhub  |  "
            "Reported Monday, Nov 23, 2026")
    check_ascii(foot, "footer")
    fw = draw.textlength(foot, font=F_FOOT)
    if fw > W - 72:
        raise SystemExit("footer too wide: %d" % fw)
    draw.text(((W - fw) / 2, 984), foot, font=F_FOOT, fill=MUTED)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (OUT_PATH, W, H))


if __name__ == "__main__":
    main()
