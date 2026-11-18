#!/usr/bin/env python3
"""Render 'THE WORLD TODAY - WEDNESDAY 18 NOVEMBER 2026' front page.

Draws a dense newspaper front page at 1024x1024 with PIL (build-time only).
Output: entry.jpg (JPEG quality 85). Deterministic: no timestamps, no random.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 246)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
GREY = (90, 88, 80)
LIGHT = (232, 228, 214)
GREEN = (18, 120, 60)

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

MAST = font("DejaVuSerif-Bold.ttf", 62)
MAST_SUB = font("DejaVuSans.ttf", 15)
KICK = font("DejaVuSans-Bold.ttf", 15)
LEAD_H = font("DejaVuSerif-Bold.ttf", 34)
LEAD_D = font("DejaVuSans.ttf", 16)
SEC = font("DejaVuSans-Bold.ttf", 14)
NUM = font("DejaVuSans-Bold.ttf", 15)
HEAD = font("DejaVuSerif-Bold.ttf", 15)
DECK = font("DejaVuSans.ttf", 12)
MAP_T = font("DejaVuSans-Bold.ttf", 13)
MAP_C = font("DejaVuSans.ttf", 11)
MKT = font("DejaVuSans.ttf", 11)
MKT_B = font("DejaVuSans-Bold.ttf", 11)
FOOT = font("DejaVuSans.ttf", 11)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width,
                    break_long_words=False, break_on_hyphens=False) or [""])
    # re-wrap by pixel width using the font
    out = []
    for line in lines:
        while d.textlength(line, font=fnt) > width and " " in line:
            cut = line.rfind(" ", 0, len(line) - 1)
            # find a split point that fits
            lo, hi = 0, len(line)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if d.textlength(line[:mid], font=fnt) <= width:
                    lo = mid
                else:
                    hi = mid - 1
            cut = line.rfind(" ", 0, lo + 1)
            if cut <= 0:
                cut = lo
            out.append(line[:cut])
            line = line[cut:].lstrip()
        out.append(line)
    return out

def rule(y, x0=24, x1=1000, w=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=w)

# ---------- Masthead ----------
d.text((512, 8), "THE WORLD TODAY", font=MAST, fill=INK, anchor="ma")
d.text((512, 78), "WEDNESDAY 18 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PAGE  •  $250 PRIZE EDITION",
       font=MAST_SUB, fill=GREY, anchor="ma")
rule(108)

# ---------- Lead story (No. 1) ----------
d.text((24, 120), "LEAD  •  UKRAINE", font=KICK, fill=RED)
lead_head = "UKRAINE STRIKES KERCH BRIDGE \u2014 ROAD SPAN COLLAPSES"
for i, ln in enumerate(wrap(lead_head, LEAD_H, 976)):
    d.text((24, 142 + i * 38), ln, font=LEAD_H, fill=INK)
d.text((24, 222),
       "Second day of strikes on the bridge to Crimea; part of the road span fell into the strait.",
       font=LEAD_D, fill=(40, 40, 40))
rule(252)

# ---------- Map panel + Markets ----------
# Map panel
d.rectangle([24, 264, 560, 386], outline=INK, width=2)
d.rectangle([24, 264, 560, 288], fill=NAVY)
d.text((36, 269), "WHERE IT HAPPENED", font=MAP_T, fill=(255, 255, 255))
d.text((420, 269), "WORLD MAP", font=MAP_T, fill=(200, 205, 220))
# sea
d.rectangle([26, 290, 558, 384], fill=(38, 58, 96))
land = (216, 205, 160)
def _sx(x):
    return int(26 + (x - 26) * 0.84)
continents = [
    [(70, 308), (150, 292), (215, 300), (205, 332), (150, 348), (95, 342), (60, 322)],
    [(215, 338), (252, 332), (268, 356), (242, 378), (218, 362)],
    [(332, 298), (372, 288), (388, 302), (362, 316), (336, 312)],
    [(342, 322), (392, 316), (408, 346), (382, 372), (352, 356)],
    [(402, 288), (522, 282), (582, 302), (562, 332), (482, 342), (422, 326)],
    [(522, 352), (572, 346), (582, 366), (532, 372)],
]
for poly in continents:
    d.polygon([(_sx(x), y) for x, y in poly], fill=land, outline=(120, 120, 100))
# flashpoint dots (plain red markers; story numbers are in the story list below)
dots = [(368, 300), (430, 322), (372, 344), (140, 318),
        (520, 312), (92, 296), (470, 296), (585, 348),
        (392, 318), (396, 314), (618, 368), (492, 330),
        (300, 322), (352, 304), (228, 348), (452, 326),
        (338, 298), (540, 322)]
for x, y in dots:
    x = _sx(x)
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED, outline=(255, 255, 255), width=1)

# Markets box
d.rectangle([572, 264, 1000, 386], outline=INK, width=2)
d.rectangle([572, 264, 1000, 288], fill=NAVY)
d.text((584, 269), "MARKETS", font=MAP_T, fill=(255, 255, 255))
d.text((920, 269), "18 NOV", font=MAP_T, fill=(200, 205, 220))
markets_left = [
    ("CAC 40", "8,216.78", "-1.62%"),
    ("DAX", "26,045.37", "-2.08%"),
    ("FTSE 100", "10,689.87", "-1.76%"),
    ("S&P 500", "7,340.53", "-1.03%"),
    ("Nasdaq", "24,328.38", "-0.74%"),
]
markets_right = [
    ("Nikkei 225", "59,024.28", "+0.28%"),
    ("Hang Seng", "23,297.16", "-0.90%"),
    ("VIX", "25.46", "+11.13%"),
    ("Brent", "$91.55", "-1.71%"),
    ("Gold", "$3,775", ""),
]
for col, rows in ((584, markets_left), (796, markets_right)):
    for i, (name, val, pct) in enumerate(rows):
        y = 296 + i * 17
        d.text((col, y), name, font=MKT_B, fill=INK)
        d.text((col + 78, y), val, font=MKT, fill=INK)
        if pct:
            d.text((col + 148, y), pct, font=MKT_B,
                   fill=GREEN if pct.startswith("+") else RED)
rule(398)

# ---------- Numbered stories 2-20 ----------
stories = [
    (2, "US STRIKES IRANIAN MISSILE SITE ON QESHM ISLAND; IRAN FIRES DRONES AT BAHRAIN AND KUWAIT",
     "US radar in Bahrain and Patriot systems in Kuwait were among the targets."),
    (3, "EBOLA IN DR CONGO MORE THAN DOUBLES \u2014 11,000 CASES, 5,400 DEAD",
     "Three in four children under five who catch it die, health officials warn."),
    (4, "US LOSES MEASLES-FREE STATUS AFTER 26 YEARS",
     "5,400 cases and 10 deaths as the virus spreads across the country."),
    (5, "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN TOMORROW",
     "First trilateral summit as APEC leaders open their meeting in China."),
    (6, "DEMOCRATS WIN ALASKA SENATE SEAT",
     "Peltola's victory gives the party 56 seats in the Senate."),
    (7, "RUSSIAN MILITARY PLANE CRASHES IN SIBERIA",
     "Nineteen people dead in the crash in Russia's far east."),
    (8, "6.0 EARTHQUAKE STRIKES PAPUA NEW GUINEA; 5.3 IN ROMANIA",
     "Two strong quakes on the same day; no tsunami warning issued."),
    (9, "GAZA: COLD KILLS IN TENTS AS FLOODS WORSEN",
     "Four nations demand aid access as winter closes in on the displaced."),
    (10, "ISRAEL: EISENKOT TAPPED TO FORM GOVERNMENT",
     "Move bypasses Netanyahu as coalition talks enter a new phase."),
    (11, "CATEGORY 5 CYCLONE XAVIER HITS NORTHERN COOK ISLANDS",
     "Cyclone Akvan nears India as the Pacific storm season peaks."),
    (12, "WORLD COURT TO RULE ON MYANMAR GENOCIDE CASE",
     "Judges to deliver their long-awaited verdict at The Hague."),
    (13, "MS DHONI RETIRES FROM IPL",
     "Indian cricket legend ends his Indian Premier League career."),
    (14, "FRANCE: FOURTH WEEKEND OF COST-OF-LIVING PROTESTS",
     "Demonstrators return to the streets over prices and wages."),
    (15, "CYBER-ATTACK DISABLES SUPERMARKET FREEZERS IN SEVEN EUROPEAN COUNTRIES",
     "US outages reach the NSA as the attack spreads across systems."),
    (16, "US DETAILS $12BN IN VENEZUELAN OIL AND MINERAL REVENUE",
     "Washington publishes the figures behind its Venezuela policy."),
    (17, "PAKISTANI MAN JAILED 330 MONTHS OVER PLOT TO KILL TRUMP",
     "Court hands down the sentence in the assassination-plot case."),
    (18, "UK CLIMATE BODY WARNS WEAKER EV RULES PUT TARGETS AT RISK",
     "Advisers say loosening electric-vehicle rules endangers climate goals."),
    (19, "GTA VI SET FOR GLOBAL RELEASE AT MIDNIGHT THURSDAY",
     "The year's most awaited game launches worldwide within hours."),
    (20, "XI CALLS FOR LOWER TRADE BARRIERS AS APEC LEADERS GATHER",
     "IAEA chief Grossi seeks the UN's top job as leaders meet in Shenzhen."),
]

cols = [(24, 502), (522, 1000)]
y = 410
for idx, (num, head, deck) in enumerate(stories):
    col = idx % 2
    row = idx // 2
    x0, x1 = cols[col]
    yy = 410 + row * 57
    wpx = x1 - x0 - 34
    d.text((x0, yy), f"{num}.", font=NUM, fill=RED)
    hlines = wrap(head, HEAD, wpx)
    for j, ln in enumerate(hlines[:2]):
        d.text((x0 + 34, yy + j * 18), ln, font=HEAD, fill=INK)
    dlines = wrap(deck, DECK, wpx)
    dy = yy + len(hlines[:2]) * 18 + 1
    for ln in dlines[:1]:
        d.text((x0 + 34, dy), ln, font=DECK, fill=GREY)
    if col == 0:
        d.line([(512, yy + 2), (512, yy + 52)], fill=LIGHT, width=1)

# ---------- Footer ----------
rule(984)
d.text((24, 994),
       "Sources: BBC  •  Reuters  •  Al Jazeera  •  AP  •  NPR     |     THE WORLD TODAY \u2014 Wednesday 18 November 2026",
       font=FOOT, fill=GREY)

img.save("entry.jpg", "JPEG", quality=85, optimize=True, progressive=False)
print("saved entry.jpg")
