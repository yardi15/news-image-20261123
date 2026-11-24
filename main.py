"""The World in One Day: Monday 23 November 2026.

Draws a dense newspaper front page summing up the day's world news
and writes it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

Pure Python standard library only. No network, no clock, no
randomness: two runs write byte-identical output.
"""

import os

from draw import (
    Canvas, ILLOS, PAPER, PANEL, INK, RED, RULE, GREY, WHITE,
    REGION_COLORS, STATUS_COLORS, STATUS_DEFS,
    draw_map, draw_status, text_width, wrap_text,
)

PRESS_TIME = "00:30 UTC"
W, H = 1024, 1024

# ---------------------------------------------------------------- stories

LEADS = [
    {
        "num": 1, "region": "NORTH AMERICA", "status": "CONFIRMED",
        "illo": "chip", "banner": "HUANG IS BACK", "callout": "+31.5%",
        "headline": "NVIDIA BRINGS BACK HUANG",
        "body": ("Board reinstates Jensen Huang as chief, 11 days after he quit "
                 "over affair revelations. Trump says he gave the board 'enough "
                 "assurance'. Shares jump 31.5%, best day since 2003. Nasdaq up "
                 "6.5%, S&P up 4.7%."),
        "source": "REUTERS \u2022 CNN",
        "lon": -121.9, "lat": 37.3,
    },
    {
        "num": 2, "region": "MIDDLE EAST", "status": "CLAIM",
        "illo": "strait", "banner": "DRONE DOWN", "callout": "$14.7BN",
        "headline": "IRAN CLAIMS DRONE DOWN, DEFIES BLOCKADE",
        "body": ("Iran's army says it shot down a US LUCAS drone east of Hormuz. "
                 "Tehran vows 'all available means' against the US blockade. US "
                 "sanctions 20-plus exchange houses; $14.7bn flagged."),
        "source": "REUTERS \u2022 US TREASURY",
        "lon": 56.5, "lat": 26.5,
    },
    {
        "num": 3, "region": "EUROPE", "status": "OFFICIAL",
        "illo": "sanctions", "banner": "22ND SANCTIONS", "callout": "60 BANKS",
        "headline": "EU PROPOSES 22ND SANCTIONS PACKAGE",
        "body": ("The Commission proposes banning 60 Russian banks from SWIFT and "
                 "listing 70-plus shadow-fleet ships. A crypto task force would "
                 "chase evasion. Visa bans for ex-combatants."),
        "source": "REUTERS \u2022 EUROPEAN COMMISSION",
        "lon": 4.4, "lat": 50.8,
    },
]

BRIEFS = [
    {
        "num": 4, "region": "ASIA", "status": "CONFIRMED", "illo": "peaks",
        "headline": "INDIA PLEDGES $1.62BN TO NEPAL",
        "body": ("Modi pledges 240bn rupees after talks with PM Shah: $377m grant, "
                 "$1.24bn credit. After August flood that killed 1,500."),
        "source": "REUTERS \u2022 AP", "lon": 77.2, "lat": 28.6,
    },
    {
        "num": 5, "region": "AFRICA", "status": "CLAIM", "illo": "corvette",
        "headline": "KYIV CLAIMS IT SANK RUSSIAN CORVETTE",
        "body": ("Zelenskyy says sea drones sank the Merkury off Benghazi and hit a "
                 "helicopter. Libya says two drones hit; 10 wounded."),
        "source": "AP \u2022 CNN", "lon": 20.1, "lat": 32.1,
    },
    {
        "num": 6, "region": "EUROPE", "status": "CONFIRMED", "illo": "rubble",
        "headline": "DYMER TOLL RISES TO 11",
        "body": ("An 11th body is pulled from the Kyiv-region block hit Sunday. Boy "
                 "Davyd, 7, was pulled alive. Two still missing."),
        "source": "REUTERS", "lon": 30.0, "lat": 50.8,
    },
    {
        "num": 7, "region": "AFRICA", "status": "CONFIRMED", "illo": "un",
        "headline": "UN AND US CONDEMN KHARTOUM STRIKES",
        "body": ("UN and US condemn Sunday's strikes on UN premises; four killed, a "
                 "child among them. Sudan blames Ethiopia."),
        "source": "AFP \u2022 UN", "lon": 32.6, "lat": 15.5,
    },
    {
        "num": 8, "region": "MIDDLE EAST", "status": "CONFIRMED", "illo": "well",
        "headline": "ISRAELI STRIKE KILLS UNRWA WORKER",
        "body": ("Adel Al-Helo is killed near a water well in Jabalia; three wounded. "
                 "UNRWA says 397 of its staff have died in the war."),
        "source": "REUTERS \u2022 UNRWA", "lon": 34.5, "lat": 31.5,
    },
    {
        "num": 9, "region": "ASIA", "status": "CONFIRMED", "illo": "chart",
        "headline": "ASIA SLIDES; TAIWAN REBOUNDS",
        "body": ("Kospi falls 3.4% to a 10-month low; Samsung down 3.1%. Taiex "
                 "rebounds 2.2%. Tokyo shut after Friday's 5.1% drop."),
        "source": "REUTERS", "lon": 127.0, "lat": 37.5,
    },
    {
        "num": 10, "region": "LATIN AMERICA", "status": "CONFIRMED", "illo": "cuffs",
        "headline": "US EXTRADITION ORDER FOR 'EL CHAPO ISIDRO'",
        "body": ("Mexico says a US extradition order exists for Fausto Isidro Meza "
                 "Flores. Eight more gang members arrested after the raid."),
        "source": "REUTERS", "lon": -107.4, "lat": 24.8,
    },
    {
        "num": 11, "region": "GLOBAL", "status": "CONFIRMED", "illo": "cop",
        "headline": "AFTER COP31: 'WORST COP EVER'",
        "body": ("Guterres 'deeply disappointed' as the Antalya talks end with no "
                 "deal. 90 nations back an electrification pledge."),
        "source": "REUTERS \u2022 CNN", "lon": 30.7, "lat": 36.9,
    },
    {
        "num": 12, "region": "ASIA", "status": "CONFIRMED", "illo": "court",
        "headline": "HASINA TO BE JAILED IF SHE RETURNS",
        "body": ("Dhaka says Sheikh Hasina will be arrested on return after her death "
                 "sentence. The ousted leader lives in exile in India."),
        "source": "REUTERS", "lon": 90.4, "lat": 23.8,
    },
    {
        "num": 13, "region": "OCEANIA", "status": "CONFIRMED", "illo": "cricket",
        "headline": "NEW ZEALAND HOLDS INDIA TO A DRAW",
        "body": ("A rearguard earns the hosts a draw in the first Test at Basin "
                 "Reserve. Australia rises to second; New Zealand third."),
        "source": "REUTERS \u2022 ABC", "lon": 174.8, "lat": -41.3,
    },
]

ALSO = [
    (14, "NORTH AMERICA", "REPORTED", "Trump expects China to buy 250 more Boeing planes", "CNBC"),
    (15, "NORTH AMERICA", "REPORTED", "Anthropic shares slide after last week's debut", "IBD"),
    (16, "NORTH AMERICA", "REPORTED", "US Marines seek missiles with double the range", "WIRES"),
    (17, "NORTH AMERICA", "REPORTED", "Schumer warns of security risks in Huang's return", "WIRES"),
    (18, "LATIN AMERICA", "CONFIRMED", "Mexico: 4 soldiers, 7 gunmen killed in Chapo raid", "BREITBART"),
    (19, "LATIN AMERICA", "REPORTED", "Plus Ultra halts Latin America flights", "TRAVEL+TOUR"),
    (20, "EUROPE", "REPORTED", "NATO in Berlin warns Russia, pledges space defence", "WIRES"),
    (21, "EUROPE", "REPORTED", "Netanyahu-Eisenkot coalition talks end without a deal", "WIRES"),
    (22, "EUROPE", "CONFIRMED", "Finland backs anti-tank barriers on Russian border", "WIRES"),
    (23, "EUROPE", "REPORTED", "Spain's right set to win majority, polls say", "WIRES"),
    (24, "MIDDLE EAST", "REPORTED", "Houthi attacks in Taiz kill 2, wound 8", "WIRES"),
    (25, "MIDDLE EAST", "CLAIM", "Moscow to launch nuclear-armed satellite, media claim", "WIRES"),
    (26, "MIDDLE EAST", "CLAIM", "Iran sets conditions for reopening Hormuz", "WIRES"),
    (27, "ASIA", "REPORTED", "China agrees to new AI discussion mechanism", "WIRES"),
    (28, "ASIA", "CONFIRMED", "S. Korea chip exports up 294% in Nov 1-20", "WIRES"),
    (29, "ASIA", "REPORTED", "Rohingya activists seek action after ICJ Myanmar ruling", "WIRES"),
    (30, "ASIA", "REPORTED", "SCO forum in Delhi urges joint heritage protection", "WIRES"),
    (31, "ASIA", "REPORTED", "Hong Kong AI stocks down about 60% this year", "WIRES"),
    (32, "AFRICA", "REPORTED", "Libya parliament moves to unify government bodies", "WIRES"),
    (33, "AFRICA", "CONFIRMED", "Ethiopia to host COP32 in Addis Ababa next year", "WIRES"),
    (34, "OCEANIA", "CONFIRMED", "Australia shares set to slide; NZX falls 1%", "REUTERS"),
    (35, "OCEANIA", "CONFIRMED", "Jetstar ordered to notify 1.1m passengers of refunds", "ABC"),
    (36, "GLOBAL", "REPORTED", "UN chief urges global AI safety framework in a year", "WIRES"),
    (37, "GLOBAL", "CONFIRMED", "Gold rebounds 2.7% to $3,635; oil slips to $81", "WIRES"),
    (38, "LATIN AMERICA", "CLAIM", "Argentina FM questions Brazil election result", "SAGIRE"),
]

TIMELINE = [
    ("06:30", "Kospi closes down 3.4%, a 10-month low"),
    ("07:23", "Dymer toll rises to 11 (Reuters)"),
    ("14:30", "US markets open; Nvidia surges"),
    ("15:35", "EU proposes 22nd sanctions package"),
    ("19:37", "Reuters: Huang reinstated as Nvidia CEO"),
    ("21:00", "Gold closes +2.7% at $3,635; WTI -4.2%"),
]

DATECHECK = [
    ("22 NOV", "COP31 ends with no deal in Antalya"),
    ("22 NOV", "Khartoum drone strikes: 4 killed, UN hit"),
    ("22 NOV", "Democrats clinch 258th House seat"),
    ("21 NOV", "Cikande factory fire: 24 body bags"),
    ("20 NOV", "Wall Street slides into correction"),
    ("NOT YET", "BepiColombo Mercury orbit capture"),
    ("NOT YET", "Democrats take Congress, 3 Jan 2027"),
]

NUMBERS = [
    ("+31.5%", "NVIDIA SHARES"),
    ("11", "DEAD IN DYMER"),
    ("$1.62BN", "FOR NEPAL"),
    ("60", "BANKS OFF SWIFT"),
    ("$14.7BN", "SHADOW BANK"),
    ("-3.4%", "KOSPI"),
]

LEGEND_DEFS = {
    "CONFIRMED": "2+ outlets",
    "OFFICIAL": "govt statement",
    "REPORTED": "one source",
    "CLAIM": "unverified claim",
    "PENDING": "developing",
}


# ---------------------------------------------------------------- layout

def draw_masthead(cv):
    cv.text_center("THE WORLD IN ONE DAY", W // 2, 12, 5, INK, bold=True)
    cv.text_center("MONDAY 23 NOVEMBER 2026", W // 2, 54, 2, RED, bold=True)
    cv.text("38 STORIES \u2022 8 REGIONS \u2022 13 FIELDS", 16, 76, 1, INK, bold=True)
    cv.text_right("PRESS TIME " + PRESS_TIME, W - 16, 76, 1, RED, bold=True)
    cv.hline(16, 94, W - 32, RED, 3)
    cv.hline(16, 99, W - 32, INK, 1)


def draw_lead(cv, story, x, y, w):
    # illustration with region tag, status badge, banner + callout
    ILLOS[story["illo"]](cv, x, y, w, 116)
    cv.rect(x, y, w, 116, INK, 1)
    rcol = REGION_COLORS[story["region"]]
    cv.fill_rect(x + 1, y + 1, text_width(story["region"], 1) + 10, 11, rcol)
    cv.text(story["region"], x + 6, y + 3, 1, WHITE, bold=True)
    chip_w = text_width(story["status"], 1) + 10
    draw_status(cv, x + w - chip_w - 4, y + 4, story["status"])
    # banner strip
    cv.fill_rect(x, y + 92, w, 24, INK)
    cv.text(story["banner"], x + 8, y + 98, 2, WHITE, bold=True)
    cv.text_right(story["callout"], x + w - 8, y + 98, 2, (250, 204, 21), bold=True)
    # headline + body + source
    lines = wrap_text(story["headline"], w, 2)
    yy = y + 124
    for ln in lines[:2]:
        cv.text(ln, x, yy, 2, INK, bold=True)
        yy += 17
    yy = y + 162
    for ln in wrap_text(story["body"], w, 1)[:5]:
        cv.text(ln, x, yy, 1, INK)
        yy += 9
    cv.text(story["source"], x, y + 212, 1, GREY)
    cv.text_right(str(story["num"]), x + w, y + 212, 1, RED, bold=True)
    cv.hline(x, y + 228, w, RULE, 1)


def draw_numbers(cv, y):
    cv.fill_rect(16, y, W - 32, 34, RED)
    slot = (W - 32) // len(NUMBERS)
    for i, (val, lab) in enumerate(NUMBERS):
        cx = 16 + slot * i + slot // 2
        cv.text_center(val, cx, y + 4, 2, WHITE, bold=True)
        cv.text_center(lab, cx, y + 22, 1, (255, 230, 200))
        if i:
            cv.vline(16 + slot * i, y + 5, 24, (255, 255, 255), 1)


def draw_brief(cv, story, x, y, w):
    ILLOS[story["illo"]](cv, x, y, w, 48)
    cv.rect(x, y, w, 48, INK, 1)
    chip_w = text_width(story["status"], 1) + 10
    draw_status(cv, x + w - chip_w - 3, y + 3, story["status"])
    cv.fill_rect(x + 1, y + 37, text_width(story["region"], 1) + 8, 10,
                 REGION_COLORS[story["region"]])
    cv.text(story["region"], x + 5, y + 39, 1, WHITE, bold=True)
    yy = y + 52
    for ln in wrap_text(story["headline"], w, 1)[:2]:
        cv.text(ln, x, yy, 1, INK, bold=True)
        yy += 9
    yy = y + 72
    for ln in wrap_text(story["body"], w, 1)[:4]:
        cv.text(ln, x, yy, 1, INK)
        yy += 9
    cv.text(story["source"], x, y + 110, 1, GREY)
    cv.text_right(str(story["num"]), x + w, y + 110, 1, RED, bold=True)


def draw_also(cv, y):
    cv.text("ALSO ON", 16, y, 2, RED, bold=True)
    cv.text_right("25 MORE STORIES", W - 16, y, 2, INK, bold=True)
    cv.hline(16, y + 18, W - 32, RED, 2)
    yy = y + 26
    for col in range(2):
        items = ALSO[col * 13:(col + 1) * 13]
        xx = 16 + col * 504
        ly = yy
        for num, region, status, text, source in items:
            cv.fill_rect(xx, ly + 1, 6, 6, REGION_COLORS[region])
            cx = xx + 10
            cx = cv.text(str(num) + ".", cx, ly, 1, RED, bold=True)
            cx = cv.text(" " + text, cx, ly, 1, INK)
            cx = cv.text(" \u2014 " + source, cx, ly, 1, GREY)
            cv.text(" [" + status + "]", cx, ly, 1, STATUS_COLORS[status], bold=True)
            ly += 15


def draw_bottom(cv, y):
    # --- map panel
    cv.text("THE WORLD \u2014 13 PLACES PINNED", 16, y, 1, INK, bold=True)
    pins = [(s["lon"], s["lat"], s["num"], s["region"]) for s in LEADS + BRIEFS]
    draw_map(cv, 20, y + 14, 336, 74, pins)
    cv.rect(20, y + 14, 336, 74, INK, 1)
    leg = [("N AMERICA", "NORTH AMERICA"), ("LATIN AM", "LATIN AMERICA"),
           ("EUROPE", "EUROPE"), ("M EAST", "MIDDLE EAST")]
    leg2 = [("ASIA", "ASIA"), ("AFRICA", "AFRICA"),
            ("OCEANIA", "OCEANIA"), ("GLOBAL", "GLOBAL")]
    lx = 20
    for lab, reg in leg:
        cv.fill_rect(lx, y + 92, 6, 6, REGION_COLORS[reg])
        lx = cv.text(" " + lab, lx + 8, y + 91, 1, INK) + 10
    lx = 20
    for lab, reg in leg2:
        cv.fill_rect(lx, y + 102, 6, 6, REGION_COLORS[reg])
        lx = cv.text(" " + lab, lx + 8, y + 101, 1, INK) + 10
    # --- timeline panel
    cv.text("MONDAY IN SIX MOMENTS (UTC)", 368, y, 1, INK, bold=True)
    cv.vline(360, y, 108, RULE, 1)
    ty = y + 14
    for t, text in TIMELINE:
        cv.text(t, 368, ty, 1, RED, bold=True)
        cv.text(text, 368 + 42, ty, 1, INK)
        ty += 13
        if t != TIMELINE[-1][0]:
            cv.hline(368, ty - 3, 296, (226, 220, 200), 1)
    # --- date check panel
    cv.text("DATE CHECK \u2014 NOT 23 NOVEMBER", 672, y, 1, INK, bold=True)
    cv.vline(664, y, 108, RULE, 1)
    dy = y + 14
    for lab, text in DATECHECK:
        col = RED if lab == "NOT YET" else INK
        cv.text(lab, 672, dy, 1, col, bold=True)
        cv.text(text, 672 + 48, dy, 1, INK)
        dy += 12


def draw_footer(cv, y):
    cv.hline(16, y - 4, W - 32, INK, 1)
    x = 16
    for status, _label in STATUS_DEFS:
        w = draw_status(cv, x, y, status)
        x += w + 4
        x = cv.text(LEGEND_DEFS[status], x, y + 2, 1, INK) + 14
    cv.text("Wires read to " + PRESS_TIME + " \u2022 Sources: Reuters, AP, AFP, BBC, "
            "CNN, European Commission, US Treasury, UN \u2022 All stories dated "
            "Monday 23 November 2026.", 16, y + 16, 1, GREY)


# ------------------------------------------------------------------ main

def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    for i, story in enumerate(LEADS):
        draw_lead(cv, story, 16 + i * 334, 104, 324)
    draw_numbers(cv, 350)
    for i, story in enumerate(BRIEFS):
        col = i % 5
        row = i // 5
        draw_brief(cv, story, 16 + col * 200, 390 + row * 124, 192)
    draw_also(cv, 638)
    draw_bottom(cv, 864)
    draw_footer(cv, 982)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    cv = build()
    from draw import write_png
    write_png(cv, os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
