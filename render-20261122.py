#!/usr/bin/env python3
"""Render 'SUNDAY 22 NOVEMBER 2026 - THE WORLD IN ONE DAY', a 1024x1024
broadsheet front page for make.fun news-image-20261122. All text is drawn
with PIL; no AI-generated text or images. Deterministic: same bytes every
run. Written in-session for this bounty; structural lessons only from the
23 Nov build (clamp all art inside its box, verify at full size and 300px).
"""

import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (22, 21, 19)
RED = (166, 30, 30)
NAVY = (30, 58, 92)
GREEN = (34, 110, 60)
GREY = (112, 106, 94)
LIGHT = (234, 227, 211)
TAN = (210, 196, 164)
GOLD = (176, 132, 52)
WHITE = (255, 255, 255)
DUSK_TOP = (58, 66, 102)
DUSK_BOT = (24, 28, 56)
NIGHT = (16, 24, 48)
HALL = (26, 44, 70)

DJ = "/usr/share/fonts/truetype/dejavu/"
NOTO = "/usr/share/fonts/truetype/noto/"


def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def serif_b(s):
    return font([DJ + "DejaVuSerif-Bold.ttf", NOTO + "NotoSerif-Bold.ttf"], s)


def serif(s):
    return font([DJ + "DejaVuSerif.ttf", NOTO + "NotoSerif-Regular.ttf"], s)


def serif_i(s):
    return font([NOTO + "NotoSerif-Italic.ttf", DJ + "DejaVuSerif.ttf"], s)


def sans(s):
    return font([DJ + "DejaVuSans.ttf", NOTO + "NotoSans-Regular.ttf"], s)


def sans_b(s):
    return font([DJ + "DejaVuSans-Bold.ttf", NOTO + "NotoSans-Bold.ttf"], s)


def mono(s):
    return font([DJ + "DejaVuSansMono.ttf"], s)


def tw(d, text, f):
    b = d.textbbox((0, 0), text, font=f)
    return b[2] - b[0]


def th(d, text, f):
    b = d.textbbox((0, 0), text, font=f)
    return b[3] - b[1]


def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_serif_b(d, text, max_w, start=64):
    for s in range(start, 28, -1):
        f = serif_b(s)
        if tw(d, text, f) <= max_w:
            return f
    return serif_b(28)


def tag_color(label):
    if label == "CLAIM":
        return RED
    if label == "REPORTED":
        return NAVY
    return GREEN


def tag_chip(d, x, y, label):
    f = sans_b(10)
    w = tw(d, label, f) + 12
    d.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=tag_color(label))
    d.text((x + 6, y + 3), label, font=f, fill=WHITE)
    return w


def rule(d, x0, x1, y, w=2, col=INK):
    d.line([(x0, y), (x1, y)], fill=col, width=w)


# ---------------------------------------------------------------- stories
HEROES = [
    {
        "n": 1,
        "tag": "CONFIRMED",
        "head": "COP31 COLLAPSES \u2014 NO DEAL",
        "body": "The longest COP on record ends Sunday with no cover decision. "
                "The EU, UK, Norway, Panama and island states reject the final "
                "text \u2014 it names no fossil fuels and drops the $120bn "
                "adaptation target. Side deals on just transition are adopted instead.",
        "art": "hall",
    },
    {
        "n": 2,
        "tag": "CLAIM",
        "head": "IRAN CLAIMS US RADARS HIT IN BAHRAIN",
        "body": "The IRGC says missile and drone strikes hit two US Patriot "
                "radars at al-Riffa and Awali Sakhir on Saturday night. Bahrain "
                "says defences intercepted the attacks; a Sitra Island facility "
                "burns, 2 injured. CENTCOM denies an F-16 was damaged.",
        "art": "night",
    },
    {
        "n": 3,
        "tag": "REPORTED",
        "head": "RUSSIA FIRES 186 DRONES",
        "body": "186 drones launched overnight, 72 of them jet-powered Shaheds; "
                "161 downed or suppressed, hits at 18 sites. One drone destroys "
                "a five-storey block in Dymer, Kyiv region: 2 killed, 14 missing "
                "including 2 children, 8 rescued.",
        "art": "drones",
    },
]

CARDS = [
    ("4", "REPORTED", "SPARTA II STILL BURNING",
     "Russian cargo ship hit by drones Saturday in the Gulf of Finland; fire "
     "burns through Sunday night. 16 crew evacuated.", "ship"),
    ("5", "CONFIRMED", "HONG KONG VOTES",
     "Election Committee polls: 856 candidates for 723 seats; record turnout.", "ballot"),
    ("6", "CONFIRMED", "INDIA DECLARE 720/9",
     "Record Test total in New Zealand \u2014 Pant 128, Gill 98. Hosts 119/2 at "
     "stumps on Day 4.", "cricket"),
    ("7", "CONFIRMED", "VERSTAPPEN WINS LAS VEGAS GP",
     "Third win in four years on the Strip. Russell hits the barriers, 9th; "
     "Leclerc and Hamilton collide.", "car"),
    ("8", "CONFIRMED", "ALCARAZ WINS ATP FINALS",
     "Beats world No. 1 Zverev 6-2 7-6(7) in Turin for a maiden title.", "tennis"),
    ("9", "CONFIRMED", "LIVERPOOL 4-0 TEN-MAN MAN UTD",
     "Pochettino's debut turns sour: Yoro sent off in the 8th minute; United "
     "drop into the relegation zone.", "football"),
    ("10", "REPORTED", "CIKANDE: 3 DEAD, 36 MISSING",
     "Candy-factory fire at PT Fonusa Agung Mulia in Tangerang, Saturday "
     "evening. Rescuers search Sunday.", "flame"),
    ("11", "REPORTED", "BAYELSA BOAT: 24 DEAD",
     "A boat carrying mourners capsizes in Nigeria's Bayelsa State.", "boat"),
    ("12", "REPORTED", "HAMAS SEEKS EMERGENCY TALKS",
     "After Saturday's strike on a Gaza food van kills 3, Hamas asks mediators "
     "for an urgent meeting.", "talks"),
    ("13", "CONFIRMED", "IRAN RATIONS ELECTRICITY",
     "Two-hour daily power cuts begin across Iran as gas output lags demand.", "plug"),
    ("14", "CONFIRMED", "BOLSONARO IN INTENSIVE CARE",
     "Brazil's ex-president is stable in a Bras\u00edlia hospital with a bowel "
     "obstruction.", "cross"),
    ("15", "CONFIRMED", "POPE LEO XIV HOSTS 1,300 POOR GUESTS",
     "The 10th World Day of the Poor lunch in the Vatican feeds 1,300 guests.", "dove"),
    ("16", "REPORTED", "HORMUZ: 2 TANKERS HIT",
     "Two tankers hit leaving the Strait of Hormuz, UKMTO says; crews told to "
     "coordinate transits with Iran.", "tanker"),
]

ALSO = [
    "S. Korea education minister quits over AI exam cheating.",
    "Nepal PM Shah begins India visit, his first foreign trip.",
    "Denmark expels a Russian attach\u00e9 over an alleged plot.",
    "Australia's Marles rejects a US report on AUKUS subs.",
    "Estonia to shut its Russia border from 1 Dec.",
    "FBI probes hack of crime database; US state pauses gun checks.",
    "Belgian controllers join Monday strike; most flights grounded.",
    "Manipur toxic-liquor toll reaches 19.",
    "Sudan: drone strikes hit Khartoum and a UN facility.",
    "Libya: sea drones hit Russian corvette Merkury, 10 hurt.",
    "OpenRouter expels 3 providers after prompt-leak probe.",
    "Somalia expels UAE ambassador, recalls its envoy.",
    "Kenya discharges its last Ebola patient.",
    "DR Congo: attack on Cantine kills 40.",
    "Lebanon: Aoun demands Israel withdraw from the south.",
    "PSG's Dou\u00e9 suffers ACL injury; surgery due this week.",
    "Barcelona fight back to beat Villarreal 3-2.",
    "Thitikul wins a third straight LPGA title.",
    "Ladakh: 70% turnout in first panchayat polls since 2019.",
]

NUMBERS = [
    ("186", "DRONES FIRED"),
    ("161", "DOWNED"),
    ("2", "RADARS CLAIMED"),
    ("16", "CREW EVACUATED"),
    ("723", "HK SEATS"),
    ("720/9", "INDIA TOTAL"),
    ("36", "CIKANDE MISSING"),
]

TIMELINE = [
    ("03:00", "Objections close"),
    ("06:00", "Plenary called"),
    ("08:00", "161 of 186 downed"),
    ("14:00", "HK polls close"),
    ("17:00", "COP31 collapses"),
    ("19:42", "Alcaraz wins ATP"),
]

REGIONS = [("EUROPE", 10), ("MIDDLE EAST", 5), ("ASIA-PACIFIC", 8),
           ("AMERICAS", 3), ("AFRICA", 6), ("OCEANIA", 1), ("WORLD", 2)]

DATE_CHECK = ("DATE CHECK \u2014 Left out as other days' news: Gaza food-van "
              "strike (Sat) \u00b7 400-drone barrage (Fri) \u00b7 Peru quake 6.7 "
              "(Fri) \u00b7 'El Chapo Isidro' captured (Fri) \u00b7 Nvidia SEC "
              "probe (Fri) \u00b7 BepiColombo orbit (Sat) \u00b7 Copa "
              "Sudamericana final (Sat) \u00b7 NWSL final (Sat) \u00b7 Geneva "
              "killer-robot talks (Sat) \u00b7 EU\u2013Indonesia signing (Sat) "
              "\u00b7 Myanmar ruling (Thu).")

SOURCES = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 The Guardian "
           "\u00b7 Xinhua \u00b7 Al Jazeera \u00b7 SCMP \u00b7 Vatican News \u00b7 UKMTO")

LEGEND = ("HOW TO READ THE TAGS \u2014 REPORTED: one source's claim, not yet "
          "confirmed \u00b7 CLAIM: a party's claim, contested \u00b7 CONFIRMED: "
          "two or more outlets")


# ---------------------------------------------------------------- hero art
# Every hero illustration is drawn on its own layer exactly the size of the
# art box, then pasted in. Nothing can poke outside the box (the 23 Nov
# build's clipped-label bug was art drawn over a neighbouring strip).

def art_hall(w, h):
    img = Image.new("RGB", (w, h), HALL)
    d = ImageDraw.Draw(img)
    # ceiling lights
    for x in (w // 6, w // 2, 5 * w // 6):
        d.ellipse([x - 5, 6, x + 5, 16], fill=(240, 220, 160))
        d.line([(x, 16), (x, 26)], fill=(200, 180, 120), width=2)
    # back wall panel
    d.rectangle([0, 26, w, h - 58], fill=(36, 58, 88))
    d.line([(0, 26), (w, 26)], fill=(70, 96, 130), width=2)
    # flags on poles, left and right
    for fx, col in ((14, (30, 58, 92)), (w - 34, (166, 30, 30))):
        d.line([(fx + 8, 30), (fx + 8, 62)], fill=(220, 210, 190), width=2)
        d.rectangle([fx + 8, 32, fx + 26, 44], fill=col)
    # empty chairs: back + seat + legs, 5 across, slim with real gaps
    cw, gap = 26, (w - 5 * 26) // 6
    cy = h - 58
    for i in range(5):
        x0 = gap + i * (26 + gap)
        d.rectangle([x0, cy - 26, x0 + 26, cy - 2], fill=(150, 158, 172))
        d.rectangle([x0 + 2, cy - 2, x0 + 24, cy + 6], fill=(120, 128, 144))
        d.line([(x0 + 4, cy + 6), (x0 + 4, cy + 16)], fill=(90, 98, 114), width=2)
        d.line([(x0 + 22, cy + 6), (x0 + 22, cy + 16)], fill=(90, 98, 114), width=2)
    # table with name plates
    d.rectangle([0, cy + 16, w, h], fill=(96, 62, 40))
    d.rectangle([0, cy + 16, w, cy + 20], fill=(120, 80, 52))
    for i in range(5):
        x0 = gap + i * (26 + gap) + 2
        d.rectangle([x0, cy + 24, x0 + 22, cy + 34], fill=(240, 234, 220))
    # gavel on the table
    gx, gy = w // 2 - 14, cy + 40
    d.rectangle([gx, gy, gx + 28, gy + 8], fill=(70, 46, 28))
    d.rectangle([gx + 12, gy + 8, gx + 16, gy + 26], fill=(90, 62, 38))
    # red NO DEAL stamp across the hall, slightly rotated
    stamp = Image.new("RGBA", (150, 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([2, 2, 147, 37], outline=(200, 30, 30), width=3)
    sd.text((10, 7), "NO DEAL", font=sans_b(24), fill=(200, 30, 30))
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (w // 2 - 75, 34), stamp)
    return img


def art_night(w, h):
    img = Image.new("RGB", (w, h), NIGHT)
    d = ImageDraw.Draw(img)
    # stars
    for (sx, sy) in [(18, 14), (52, 26), (96, 10), (150, 20), (210, 12),
                     (260, 28), (300, 14), (120, 34), (180, 8), (240, 36)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 225, 240))
    # moon (solid)
    d.ellipse([w - 52, 10, w - 22, 40], fill=(238, 232, 210))
    # interceptor arcs (gold)
    d.arc([40, -30, 180, 90], start=200, end=340, fill=GOLD, width=3)
    d.arc([150, -50, 300, 70], start=200, end=340, fill=GOLD, width=3)
    d.ellipse([104, 22, 110, 28], fill=GOLD)
    d.ellipse([218, 8, 224, 14], fill=GOLD)
    # sea horizon
    d.rectangle([0, h - 34, w, h], fill=(20, 34, 58))
    d.line([(0, h - 34), (w, h - 34)], fill=(70, 96, 130), width=2)
    # two radar domes on the shore, smaller, with ribs
    for cx in (w // 3, 2 * w // 3):
        d.pieslice([cx - 26, h - 66, cx + 26, h - 14], start=180, end=360,
                   fill=(190, 196, 206))
        d.line([(cx, h - 66), (cx, h - 14)], fill=(150, 156, 166), width=1)
        d.line([(cx - 13, h - 60), (cx - 13, h - 14)], fill=(150, 156, 166),
               width=1)
        d.line([(cx + 13, h - 60), (cx + 13, h - 14)], fill=(150, 156, 166),
               width=1)
        d.line([(cx, h - 66), (cx, h - 82)], fill=(220, 224, 232), width=2)
        d.ellipse([cx - 3, h - 85, cx + 3, h - 79], fill=(220, 224, 232))
        d.rectangle([cx - 32, h - 14, cx + 32, h - 6], fill=(140, 146, 156))
    # fire glow on the horizon, far right edge
    d.ellipse([w - 44, h - 48, w - 8, h - 24], fill=(200, 90, 30))
    d.ellipse([w - 34, h - 42, w - 18, h - 30], fill=(240, 170, 60))
    return img


def art_drones(w, h):
    img = Image.new("RGB", (w, h), DUSK_BOT)
    d = ImageDraw.Draw(img)
    # dusk bands
    for i, col in enumerate([(58, 66, 102), (48, 56, 90), (38, 46, 76),
                             (30, 36, 64), (24, 28, 56)]):
        y0 = i * (h - 40) // 5
        y1 = (i + 1) * (h - 40) // 5
        d.rectangle([0, y0, w, y1], fill=col)
    # searchlight beams from bottom corners
    d.polygon([(20, h - 40), (120, 0), (150, 0), (70, h - 40)],
              fill=(150, 158, 180))
    d.polygon([(w - 20, h - 40), (w - 120, 0), (w - 150, 0), (w - 70, h - 40)],
              fill=(150, 158, 180))
    # drones: body + 4 rotors + red light
    for (dx, dy, s) in [(70, 26, 7), (170, 44, 9), (260, 20, 6)]:
        d.rectangle([dx - s, dy - 3, dx + s, dy + 3], fill=(18, 20, 30))
        for rx in (dx - s - 6, dx + s + 6):
            d.line([(rx - 7, dy - 6), (rx + 7, dy - 6)], fill=(200, 204, 214),
                   width=2)
            d.line([(rx, dy - 3), (rx, dy - 6)], fill=(200, 204, 214), width=1)
        d.ellipse([dx - 2, dy + 4, dx + 2, dy + 8], fill=(220, 40, 40))
    # city block at the bottom
    base = h - 40
    for (bx, bw, bh) in [(0, 52, 22), (58, 40, 30), (104, 62, 18), (172, 44, 28),
                         (222, 56, 20), (284, 40, 26)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(14, 16, 26))
        for wx in range(bx + 6, bx + bw - 6, 12):
            for wy in range(base - bh + 5, base - 5, 10):
                if (wx + wy) % 24 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 190, 80))
    return img


ART = {"hall": art_hall, "night": art_night, "drones": art_drones}


# ---------------------------------------------------------------- card icons
def icon(d, kind, x, y, s=20):
    """Tiny flat icon, drawn inside a s x s box at (x, y)."""
    if kind == "ship":
        d.polygon([(x, y + 12), (x + s, y + 12), (x + s - 4, y + s),
                   (x + 4, y + s)], fill=NAVY)
        d.line([(x + s // 2, y + 12), (x + s // 2, y + 2)], fill=INK, width=2)
        d.polygon([(x + s // 2, y + 2), (x + s - 4, y + 10), (x + s // 2, y + 10)],
                  fill=RED)
    elif kind == "ballot":
        d.rectangle([x + 2, y + 8, x + s - 2, y + s], fill=NAVY)
        d.rectangle([x + 6, y + 2, x + s - 6, y + 10], fill=WHITE, outline=INK)
        d.line([(x + 8, y + 6), (x + 10, y + 8), (x + 14, y + 3)], fill=RED, width=2)
    elif kind == "cricket":
        d.line([(x + 4, y + s - 2), (x + s - 6, y + 4)], fill=(150, 110, 60), width=3)
        d.ellipse([x + s - 8, y + 2, x + s - 1, y + 9], fill=RED)
    elif kind == "car":
        d.polygon([(x + 2, y + 12), (x + 6, y + 6), (x + s - 6, y + 6),
                   (x + s - 2, y + 12)], fill=RED)
        d.rectangle([x, y + 12, x + s, y + 16], fill=RED)
        d.ellipse([x + 3, y + 15, x + 8, y + 20], fill=INK)
        d.ellipse([x + s - 8, y + 15, x + s - 3, y + 20], fill=INK)
    elif kind == "tennis":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=(190, 210, 60),
                  outline=INK)
        d.arc([x + 2, y + 2, x + s - 2, y + s - 2], start=300, end=60,
              fill=WHITE, width=2)
    elif kind == "football":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=WHITE, outline=INK)
        d.polygon([(x + 8, y + 7), (x + 12, y + 7), (x + 13, y + 11),
                   (x + 10, y + 13), (x + 7, y + 11)], fill=INK)
    elif kind == "flame":
        d.polygon([(x + 10, y + 1), (x + 16, y + 9), (x + 18, y + 14),
                   (x + 12, y + 19), (x + 4, y + 19), (x + 2, y + 12),
                   (x + 6, y + 8)], fill=(220, 90, 30))
        d.polygon([(x + 10, y + 10), (x + 13, y + 14), (x + 10, y + 17),
                   (x + 7, y + 14)], fill=(240, 180, 60))
    elif kind == "boat":
        d.polygon([(x + 2, y + 12), (x + s - 2, y + 12), (x + s - 6, y + s - 2),
                   (x + 6, y + s - 2)], fill=NAVY)
        d.polygon([(x + s // 2, y + 2), (x + s // 2, y + 11), (x + 4, y + 11)],
                  fill=WHITE)
    elif kind == "talks":
        d.rounded_rectangle([x + 1, y + 3, x + s - 1, y + 13], radius=3,
                            fill=NAVY)
        d.polygon([(x + 5, y + 13), (x + 5, y + 18), (x + 10, y + 13)], fill=NAVY)
        for lx in (x + 5, x + 5, x + 5):
            pass
        d.line([(x + 5, y + 6), (x + s - 5, y + 6)], fill=WHITE, width=1)
        d.line([(x + 5, y + 9), (x + s - 5, y + 9)], fill=WHITE, width=1)
    elif kind == "plug":
        d.rectangle([x + 6, y + 8, x + s - 6, y + s - 2], fill=INK)
        d.line([(x + 8, y + 8), (x + 8, y + 2)], fill=INK, width=2)
        d.line([(x + s - 8, y + 8), (x + s - 8, y + 2)], fill=INK, width=2)
        d.polygon([(x + 10, y + 12), (x + 7, y + 17), (x + 11, y + 17),
                   (x + 9, y + 20)], fill=GOLD)
    elif kind == "cross":
        d.rectangle([x + 8, y + 2, x + 12, y + s - 2], fill=RED)
        d.rectangle([x + 2, y + 8, x + s - 2, y + 12], fill=RED)
    elif kind == "dove":
        d.ellipse([x + 3, y + 9, x + 15, y + 16], fill=WHITE, outline=INK)
        d.ellipse([x + 11, y + 6, x + 16, y + 11], fill=WHITE, outline=INK)
        d.polygon([(x + 14, y + 8), (x + 19, y + 6), (x + 16, y + 11)], fill=GOLD)
        d.arc([x + 4, y + 2, x + 14, y + 12], start=180, end=330, fill=INK, width=2)
    elif kind == "tanker":
        d.rectangle([x + 1, y + 12, x + s - 1, y + s - 2], fill=NAVY)
        d.rectangle([x + 4, y + 6, x + 9, y + 12], fill=RED)
        d.rectangle([x + 11, y + 8, x + 16, y + 12], fill=GOLD)


# ---------------------------------------------------------------- dotted map
CONTINENTS = [  # (cx, cy, rx, ry) ellipses on a 300x150 map
    (52, 42, 62, 30),    # North America
    (88, 108, 26, 34),   # South America
    (152, 36, 26, 18),   # Europe
    (158, 88, 32, 38),   # Africa
    (218, 40, 62, 32),   # Asia
    (256, 112, 24, 14),  # Australia
]

PINS = [  # (lon, lat, n, dx, dy) dx/dy nudge px so clustered pins stay apart
    (30.7, 36.9, 1, 0, 0),      # Antalya / COP31
    (50.6, 26.2, 2, 12, 10),    # Bahrain
    (30.5, 50.5, 3, 6, -2),     # Kyiv
    (24.0, 60.0, 4, -6, -4),    # Gulf of Finland
    (114.0, 22.3, 5, 0, 0),     # Hong Kong
    (91.7, 26.1, 6, 0, 0),      # Guwahati
    (-115.1, 36.2, 7, 0, 0),    # Las Vegas
    (7.7, 45.1, 8, -8, -6),     # Turin
    (-2.99, 53.4, 9, -4, -4),   # Liverpool
    (106.6, -6.2, 10, 0, 0),    # Tangerang
    (6.3, 4.8, 11, 0, 0),       # Bayelsa
    (34.5, 31.5, 12, -6, 8),    # Gaza
    (51.4, 35.7, 13, -12, -6),  # Tehran
    (-47.9, -15.8, 14, 0, 0),   # Brasilia
    (12.45, 41.9, 15, 8, 6),    # Vatican
    (56.5, 26.6, 16, 14, -4),   # Hormuz
]


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(242, 236, 220),
                outline=GREY)
    d.text((mx + 8, my + 5), "WHERE IT HAPPENED", font=sans_b(11), fill=INK)
    ox, oy = mx, my + 20
    iw, ih = mw, mh - 20
    # dotted continents
    step = 9
    for gy in range(oy + 4, oy + ih - 2, step):
        for gx in range(ox + 4, ox + iw - 2, step):
            cx, cy = gx - ox, gy - oy
            inside = False
            for (ex, ey, rx, ry) in CONTINENTS:
                if ((cx - ex) / rx) ** 2 + ((cy - ey) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=TAN)
    # pins (smaller so the Europe / Gulf cluster stays readable)
    for (lon, lat, n, dx, dy) in PINS:
        px = ox + int((lon + 180) / 360 * iw) + dx
        py = oy + int((90 - lat) / 180 * ih) + dy
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=WHITE)
        f = sans_b(7)
        t = str(n)
        d.text((px - tw(d, t, f) // 2, py - 4), t, font=f, fill=WHITE)


# ---------------------------------------------------------------- layout
def render(out_path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M  # 976

    # kicker
    d.text((M, 14), "THE WORLD IN ONE DAY", font=sans_b(14), fill=INK)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - M - tw(d, right, sans_b(12)), 16), right, font=sans_b(12),
           fill=GREY)
    rule(d, M, W - M, 36, 2)

    # giant serif date
    df = fit_serif_b(d, "SUNDAY 22 NOVEMBER 2026", CW, 62)
    d.text((M, 40), "SUNDAY 22 NOVEMBER 2026", font=df, fill=INK)

    # deck line
    deck = ("COP31 collapses with no deal \u00b7 Iran claims US radars hit in "
            "Bahrain \u00b7 Russia fires 186 drones at Ukraine")
    d.text((M, 110), deck, font=serif_i(17), fill=RED)

    # timeline strip (narrow band: auto-fit font so all 6 items fit exactly)
    y = 134
    d.rectangle([M, y, W - M, y + 30], fill=NAVY)
    d.text((M + 10, y + 8), "THE DAY IN UTC", font=sans_b(12), fill=GOLD)
    avail = W - M - 10 - (M + 132)
    size = 11
    while size > 8:
        tf = sans(size)
        bf = sans_b(size)
        total = 0
        for (t, ev) in TIMELINE:
            total += tw(d, t, bf) + 5 + tw(d, ev, tf) + 14
        if total - 14 <= avail:
            break
        size -= 1
    tx = M + 132
    for (t, ev) in TIMELINE:
        d.text((tx, y + 8), t, font=sans_b(size), fill=WHITE)
        tx += tw(d, t, sans_b(size)) + 5
        d.text((tx, y + 8), ev, font=sans(size), fill=(215, 222, 235))
        tx += tw(d, ev, sans(size)) + 14
    y += 38

    # region strip
    d.text((M, y), "REGIONS", font=sans_b(11), fill=GREY)
    rx = M + 70
    for (name, n) in REGIONS:
        d.text((rx, y), name, font=sans_b(11), fill=INK)
        rx += tw(d, name, sans_b(11)) + 4
        d.text((rx, y), str(n), font=sans_b(11), fill=RED)
        rx += tw(d, str(n), sans_b(11)) + 16
    y += 22

    # BY THE NUMBERS strip
    d.rectangle([M, y, W - M, y + 48], fill=LIGHT, outline=GREY)
    d.text((M + 10, y + 3), "BY THE NUMBERS", font=sans_b(10), fill=GREY)
    cell = (CW - 20) / len(NUMBERS)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = M + 10 + i * cell
        nf = serif_b(22)
        d.text((cx, y + 12), num, font=nf, fill=INK)
        d.text((cx, y + 35), cap, font=sans(8), fill=GREY)
    y += 54
    rule(d, M, W - M, y, 2)
    y += 8

    # heroes: 3 panels
    hero_y = y
    hero_h = 268
    hw = (CW - 16) // 3
    for i, hero in enumerate(HEROES):
        hx = M + i * (hw + 8)
        # art box (own layer, clamped by construction)
        art = ART[hero["art"]](hw, 112)
        img.paste(art, (hx, hero_y))
        d.rectangle([hx, hero_y, hx + hw, hero_y + 112], outline=INK, width=1)
        ty = hero_y + 118
        chip_w = tag_chip(d, hx, ty, hero["tag"])
        d.text((hx + chip_w + 8, ty + 2),
               "No. %d" % hero["n"], font=sans_b(11), fill=GREY)
        hy = ty + 22
        for ln in wrap(d, hero["head"], sans_b(17), hw):
            d.text((hx, hy), ln, font=sans_b(17), fill=INK)
            hy += 21
        by = hy + 4
        for ln in wrap(d, hero["body"], sans(11), hw):
            d.text((hx, by), ln, font=sans(11), fill=(52, 48, 44))
            by += 14
    y = hero_y + hero_h
    rule(d, M, W - M, y, 1, GREY)
    y += 8

    # cards: 13 in two rows (7 + 6)
    card_y = y
    card_h = 112
    rows = [CARDS[:7], CARDS[7:]]
    for r, row in enumerate(rows):
        cw = (CW - (len(row) - 1) * 8) // len(row)
        for c, (num, tag, head, body, kind) in enumerate(row):
            cx = M + c * (cw + 8)
            cy = card_y + r * (card_h + 6)
            d.rectangle([cx, cy, cx + cw, cy + card_h], outline=GREY, width=1)
            d.text((cx + 6, cy + 5), num, font=serif_b(15), fill=RED)
            icon(d, kind, cx + cw - 26, cy + 5, 20)
            hy = cy + 26
            for ln in wrap(d, head, sans_b(10), cw - 12)[:2]:
                d.text((cx + 6, hy), ln, font=sans_b(10), fill=INK)
                hy += 12
            by = hy + 2
            for ln in wrap(d, body, sans(9), cw - 12)[:4]:
                d.text((cx + 6, by), ln, font=sans(9), fill=(52, 48, 44))
                by += 11
            tf2 = sans_b(8)
            d.text((cx + 6, cy + card_h - 13), tag, font=tf2,
                   fill=tag_color(tag))
    y = card_y + 2 * card_h + 6
    rule(d, M, W - M, y, 1, GREY)
    y += 8

    # map + ALSO
    map_y = y
    map_h = 168
    draw_map(d, M, map_y, 300, map_h)
    ax = M + 316
    aw = W - M - ax
    d.text((ax, map_y), "ALSO ON SUNDAY 22 NOVEMBER",
           font=sans_b(12), fill=INK)
    rule(d, ax, W - M, map_y + 20, 1, GREY)
    col_w = (aw - 16) // 2
    ay = map_y + 26
    af = sans(9)
    for i, item in enumerate(ALSO):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        ix = ax + col * (col_w + 16)
        iy = ay + row * 15
        txt = "%d. %s" % (17 + i, item)
        # one line only: trim with an ellipsis until it fits
        while tw(d, txt, af) > col_w and len(txt) > 12:
            txt = txt[:-4] + "\u2026"
        d.text((ix, iy), txt, font=af, fill=(52, 48, 44))
    y = map_y + map_h + 6

    # legend + date check + sources
    d.text((M, y), LEGEND, font=sans(9), fill=GREY)
    y += 15
    for ln in wrap(d, DATE_CHECK, sans_b(9), CW):
        d.text((M, y), ln, font=sans_b(9), fill=INK)
        y += 12
    y += 2
    d.text((M, y), SOURCES, font=sans(9), fill=GREY)
    y += 13

    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(target)
    data = open(target, "rb").read()
    print("%s %d bytes sha256=%s" % (target, len(data),
                                     hashlib.sha256(data).hexdigest()))
