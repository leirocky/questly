"""Scene 13 — closing page: God's love is wider than the sea and higher than the sky.

One wide sunset double-page spread on a 2800 x 1620 stage (no cuts):
  * WEST (left): the calm sea under the setting sun, a golden glitter path, the little ship sailing toward
    the sun and the great fish leaping happily out of the water.
  * MIDDLE: Jonah standing peacefully on a grassy hill, looking out over it all.
  * EAST (right): a golden plain with the city of Nineveh glowing in the last light.
  * ABOVE: a huge, high dusk sky — sunset gradient, clouds, the evening star and the first stars.

Timing (all keyed to the narration, phrase times derived from ctx.lines):
  * line 0 "上帝的爱，比海更宽，比天更高。": the camera pulls back from Jonah to the full spread ("比海更宽":
    the sea opens up and the great fish leaps across the sun's glitter path; "比天更高": the frame grows upward,
    the sky deepens and the evening star and first stars come out).
  * line 1 "他愿意给每一个人，重新开始的机会。": warm golden light blooms from the sun over everything (rays,
    glow, motes), Nineveh's lamps light up and sparkle, Jonah closes his eyes in the warm light, doves fly in
    from the east — two land beside Jonah, three glide on toward the sunset — and the fish leaps once more.
  * after the narration: a hand-lettered end card '约拿的故事 · 完' fades in high in the sky, a swash is drawn
    out from its centre and a small heart pops in (chime). The film then fades out (assemble.py).
"""
import math
import random

import numpy as np
from scipy import ndimage

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 2800, 1620

HORIZON = 955            # sea horizon
MID_WL = 1022            # waterline of the mid sea band (the ship sails on it)
NEAR_WL = 1180           # waterline of the near sea band (the fish leaps out of it)
SUN = (505, 918)         # setting sun (sinks a little during the scene)
SUN_R = 92
JONAH_X = 1400
JONAH_S = 0.8
CITY_X0, CITY_X1, CITY_Y, CITY_S = 1770, 2690, 986, 0.5
CARD_X, CARD_Y = 1400, 412   # end-card text baseline centre

SHIP_X, SHIP_S = 965, 0.19
FISH_S = 0.3


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def hill_y(x):
    """Ground line of Jonah's hill (stage px)."""
    base = 1100 + 0.00024 * (x - JONAH_X) ** 2
    k = min(1.0, max(0.0, (abs(x - JONAH_X) - 260) / 320))
    return base + k * 16 * math.sin((x - JONAH_X) / 150.0)


def bez(p0, p1, p2, u):
    a, b, c = (1 - u) ** 2, 2 * u * (1 - u), u * u
    return a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]


# ============================================================================ sky


def sky_svg():
    defs = (f'<linearGradient id="e13sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{HORIZON + 40}">'
            '<stop offset="0" stop-color="#36416f"/>'
            '<stop offset="0.17" stop-color="#4d4f86"/>'
            '<stop offset="0.34" stop-color="#7a63a0"/>'
            '<stop offset="0.5" stop-color="#b47ea6"/>'
            '<stop offset="0.64" stop-color="#e0918b"/>'
            '<stop offset="0.77" stop-color="#f3a873"/>'
            '<stop offset="0.9" stop-color="#f8c584"/>'
            '<stop offset="1" stop-color="#fbe1a6"/></linearGradient>' +
            S.rad_grad("e13sunhalo", [(0, "#fff4c8", 0.95), (0.18, "#ffe3a0", 0.7), (0.5, "#ffc888", 0.28),
                                      (1, "#ffb880", 0)]) +
            S.rad_grad("e13cityglow", [(0, "#ffd9a0", 0.55), (0.6, "#f8c08e", 0.2), (1, "#f8c08e", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#e13sky)"/>'
            f'<ellipse cx="{SUN[0]}" cy="{SUN[1] + 20}" rx="1100" ry="560" fill="url(#e13sunhalo)"/>'
            f'<ellipse cx="2230" cy="{CITY_Y - 76}" rx="760" ry="300" fill="url(#e13cityglow)"/>')
    # soft horizontal streak clouds near the horizon (no ink: far away, glowing)
    rng = random.Random(21)
    streaks = ""
    for cx, cy, w, h, col, op in ((330, 810, 520, 16, "#ffe2a6", 0.75), (980, 850, 640, 14, "#ffd79a", 0.6),
                                  (1500, 792, 480, 12, "#f9c6a0", 0.55), (2050, 750, 700, 16, "#f6b9a6", 0.5),
                                  (2550, 820, 420, 12, "#f9cba3", 0.55), (700, 750, 380, 10, "#ffd8a0", 0.5)):
        for k in range(3):
            streaks += (f'<ellipse cx="{f1(cx + rng.uniform(-60, 60))}" cy="{f1(cy + k * 13)}" '
                        f'rx="{f1(w / 2 * rng.uniform(0.6, 1.0))}" ry="{f1(h * rng.uniform(0.6, 1.0))}" '
                        f'fill="{col}" opacity="{op}"/>')
    body += S.g(streaks, filter="soft")
    return doc(body, defs)


def dusk_svg(stars=""):
    """Deepening indigo at the top of the sky; ``stars`` (markup) come out together with it."""
    defs = ('<linearGradient id="e13dusk" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="620">'
            '<stop offset="0" stop-color="#1f2a55" stop-opacity="0.62"/>'
            '<stop offset="0.55" stop-color="#2b3263" stop-opacity="0.25"/>'
            '<stop offset="1" stop-color="#2b3263" stop-opacity="0"/></linearGradient>')
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="640" fill="url(#e13dusk)"/>' + stars, defs)


def star_path(x, y, r, w=0.24):
    k = r * w
    return (f"M{f1(x)},{f1(y - r)} L{f1(x + k)},{f1(y - k)} L{f1(x + r)},{f1(y)} L{f1(x + k)},{f1(y + k)} "
            f"L{f1(x)},{f1(y + r)} L{f1(x - k)},{f1(y + k)} L{f1(x - r)},{f1(y)} L{f1(x - k)},{f1(y - k)} Z")


def stars_svg(seed, n_big, n_small):
    return doc(stars_markup(seed, n_big, n_small))


def stars_markup(seed, n_big, n_small):
    rng = random.Random(seed)
    body = ""
    placed = 0
    tries = 0
    while placed < n_big + n_small and tries < 4000:
        tries += 1
        x, y = rng.uniform(40, SW - 40), rng.uniform(30, 560 - rng.uniform(0, 120))
        if 840 < x < 1960 and 200 < y < 580:      # keep the end-card area clean
            continue
        if placed < n_big:
            r = rng.uniform(9, 15)
            body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.9)}" fill="#fff3cc" opacity="0.25"/>'
            body += f'<path d="{star_path(x, y, r)}" fill="#fff7dc"/>'
        else:
            body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(1.8, 3.4))}" fill="#fff4d4"/>'
        placed += 1
    return body


def evening_star_svg(x, y):
    body = (f'<circle cx="{x}" cy="{y}" r="34" fill="#fff2c4" opacity="0.22"/>'
            f'<circle cx="{x}" cy="{y}" r="17" fill="#fff4cf" opacity="0.4"/>'
            f'<path d="{star_path(x, y, 30, 0.14)}" fill="#fffae6"/>'
            f'<path d="{star_path(x, y, 15, 0.3)}" fill="#fffdf2" transform="rotate(45 {x} {y})"/>')
    return doc(body)


def sun_svg():
    x, y = SUN
    defs = S.rad_grad("e13sun", [(0, "#fff6d2"), (0.55, "#fde08a"), (1, "#f7b24c")])
    body = (f'<circle cx="{x}" cy="{y}" r="{SUN_R + 70}" fill="#ffe6a8" opacity="0.35" filter="url(#soft)"/>'
            + S.g(f'<circle cx="{x}" cy="{y}" r="{SUN_R}" fill="url(#e13sun)" stroke="#f0a24a" '
                  f'stroke-width="4"/>', filter="wobble"))
    return doc(body, defs)


def sunset_cloud(cx, cy, w, h, seed, top, lit):
    """Flat-bottomed evening cloud lit from below by the setting sun: lavender top, glowing gold-pink belly."""
    gid = f"e13c{seed}"
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="0.55" stop-color="{S.mix(top, lit, 0.45)}"/>'
            f'<stop offset="1" stop-color="{lit}"/></linearGradient>')
    body = S.cloud(cx, cy, w, h, f"url(#{gid})", seed=seed, sw=2.5)
    # glowing rim just inside the flat underside of the cloud
    body += (f'<path d="M{f1(cx - w * 0.38)},{f1(cy + h * 0.36)} Q{f1(cx)},{f1(cy + h * 0.53)} '
             f'{f1(cx + w * 0.38)},{f1(cy + h * 0.36)}" stroke="#fff0c0" stroke-width="{f1(max(4, h * 0.07))}" '
             f'fill="none" stroke-linecap="round" opacity="0.8"/>')
    return body, defs


def clouds_svg():
    items = [  # cx, cy, w, h, seed, top colour, lit underside
        (300, 650, 330, 84, 3, "#d9a3b6", "#ffd9a0"),
        (1010, 745, 250, 62, 5, "#dca3b2", "#ffdca0"),
        (1890, 700, 220, 58, 7, "#cf9db6", "#fbc9a0"),
        (2390, 560, 400, 100, 2, "#b993b8", "#f7c1a2"),
        (2620, 250, 250, 66, 9, "#9c87b4", "#d9a6b6"),
        (230, 300, 240, 64, 4, "#9f88b6", "#dca8b8"),
        (690, 175, 180, 48, 8, "#8b7fb0", "#c79bb6"),
    ]
    body, defs = "", ""
    for it in items:
        b, d = sunset_cloud(*it)
        body += b
        defs += d
    return doc(S.g(body, filter="wobble"), defs)


# ============================================================================ sea


def sea_svg():
    """Far sea (horizon to bottom) + the mid band the ship sails on, with soft wave strokes (one static layer)."""
    defs = (f'<linearGradient id="e13far" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#e4b0a6"/><stop offset="0.12" stop-color="#ad8fad"/>'
            '<stop offset="0.4" stop-color="#6d7aa6"/><stop offset="1" stop-color="#46578a"/></linearGradient>'
            f'<linearGradient id="e13mid" gradientUnits="userSpaceOnUse" x1="0" y1="{MID_WL}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#9886ae"/><stop offset="0.3" stop-color="#6879a6"/>'
            '<stop offset="1" stop-color="#3f5285"/></linearGradient>' +
            S.rad_grad("e13seaglow", [(0, "#ffe2a4", 0.55), (0.5, "#f9c495", 0.2), (1, "#f9c495", 0)]))
    far = f'<rect x="-20" y="{HORIZON}" width="{SW + 40}" height="{SH - HORIZON + 20}" fill="url(#e13far)"/>'
    far += f'<ellipse cx="{SUN[0]}" cy="{HORIZON + 40}" rx="700" ry="120" fill="url(#e13seaglow)"/>'
    far += (f'<path d="M-20,{HORIZON} L{SW + 20},{HORIZON}" stroke="{P["ink"]}" stroke-width="2.5" '
            f'opacity="0.6"/>')
    rng = random.Random(5)
    strokes = ""
    for _ in range(26):
        x = rng.uniform(-20, 1650)
        y = rng.uniform(HORIZON + 10, MID_WL - 12)
        ln = rng.uniform(30, 90) * (0.6 + (y - HORIZON) / 140)
        strokes += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-4 {f1(ln)},0" stroke="#f6dcc8" stroke-width="2.5" '
                    f'fill="none" stroke-linecap="round" opacity="0.6"/>')
    mid = S.path(S.wave_band(MID_WL, 4, 300, 0.7, x0=-60, x1=1760, bottom=SH + 60), fill="url(#e13mid)", sw=3)
    for _ in range(30):
        x = rng.uniform(-20, 1700)
        y = rng.uniform(MID_WL + 18, NEAR_WL - 10)
        ln = rng.uniform(40, 120)
        strokes += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-6 {f1(ln)},0" stroke="#d9c6e0" stroke-width="3" '
                    f'fill="none" stroke-linecap="round" opacity="0.55"/>')
    crest = S.path(S.wave_line(MID_WL - 3, 4, 300, 0.7, x0=-60, x1=1760), stroke=False,
                   extra='stroke="#fbe6c8" stroke-width="4" fill="none" opacity="0.55"')
    return doc(S.g(far, filter="wobble") + S.g(mid + crest, filter="wobble") + S.g(strokes, filter="wobble-fine"),
               defs)


def glitter_svg(seed):
    """The sun's golden path on the water (horizon .. near waterline)."""
    rng = random.Random(seed)
    body = ""
    y = HORIZON + 6
    while y < NEAR_WL - 6:
        half = 26 + (y - HORIZON) * 0.55
        n = 2 + int((y - HORIZON) / 60)
        for _ in range(n):
            x = SUN[0] + rng.uniform(-half, half)
            ln = rng.uniform(10, 26) * (0.7 + (y - HORIZON) / 180)
            body += (f'<rect x="{f1(x - ln / 2)}" y="{f1(y)}" width="{f1(ln)}" height="{f1(3 + (y - HORIZON) / 90)}" '
                     f'rx="2" fill="#ffe9a8" opacity="{rng.uniform(0.55, 0.95):.2f}"/>')
        y += 7 + (y - HORIZON) * 0.05
    return doc(body)


def near_sea_svg():
    defs = (f'<linearGradient id="e13near" gradientUnits="userSpaceOnUse" x1="0" y1="{NEAR_WL}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#6a75a6"/><stop offset="0.45" stop-color="#4b5c8e"/>'
            '<stop offset="1" stop-color="#36487a"/></linearGradient>')
    band = S.path(S.wave_band(NEAR_WL, 6, 360, 1.9, x0=-80, x1=1500, bottom=SH + 60), fill="url(#e13near)", sw=3.5)
    crest = S.path(S.wave_line(NEAR_WL - 4, 6, 360, 1.9, x0=-80, x1=1500), stroke=False,
                   extra='stroke="#fbe6c8" stroke-width="5" fill="none" opacity="0.6"')
    rng = random.Random(9)
    body = ""
    y = NEAR_WL + 10
    while y < SH:  # continuation of the glitter path + wave strokes
        half = 26 + (y - HORIZON) * 0.55
        for _ in range(3 + int((y - NEAR_WL) / 70)):
            x = SUN[0] + rng.uniform(-half, half)
            ln = rng.uniform(18, 46)
            body += (f'<rect x="{f1(x - ln / 2)}" y="{f1(y)}" width="{f1(ln)}" height="5" rx="2.5" fill="#ffe2a0" '
                     f'opacity="{rng.uniform(0.45, 0.85):.2f}"/>')
        y += 16
    for _ in range(22):
        x = rng.uniform(-40, 1400)
        yy = rng.uniform(NEAR_WL + 30, SH - 30)
        ln = rng.uniform(60, 150)
        body += (f'<path d="M{f1(x)},{f1(yy)} q{f1(ln / 2)},-8 {f1(ln)},0" stroke="#b9c3e0" stroke-width="4" '
                 f'fill="none" stroke-linecap="round" opacity="0.5"/>')
    return doc(S.g(band + crest, filter="wobble") + S.g(body, filter="wobble-fine"), defs)


# ============================================================================ land


def land_svg():
    """Far hills, golden plain with Nineveh, the shoreline, and Jonah's grassy hill (one static layer)."""
    defs = (f'<linearGradient id="e13plain" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="1300">'
            '<stop offset="0" stop-color="#eec08a"/><stop offset="0.35" stop-color="#d9b877"/>'
            '<stop offset="1" stop-color="#a9ad62"/></linearGradient>'
            '<linearGradient id="e13hill" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#b9bf62"/><stop offset="0.42" stop-color="#a7bb5e"/>'
            '<stop offset="0.62" stop-color="#8eac57"/><stop offset="1" stop-color="#6f8a55"/></linearGradient>'
            f'<linearGradient id="e13hillsh" gradientUnits="userSpaceOnUse" x1="0" y1="1100" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#4b4a6a" stop-opacity="0"/>'
            '<stop offset="0.3" stop-color="#4b4a6a" stop-opacity="0.06"/>'
            '<stop offset="1" stop-color="#3f3d63" stop-opacity="0.5"/></linearGradient>' +
            S.rad_grad("e13jglow", [(0, "#ffe7a8", 0.55), (1, "#ffe7a8", 0)]))
    # far lavender hills behind the city
    far_hills = (S.path(S.hill(1480, 2200, HORIZON + 6, 70, seed=4, bumps=2), fill="#c59bab", sw=2.5) +
                 S.path(S.hill(2050, 2880, HORIZON + 6, 95, seed=6, bumps=2), fill="#b994ab", sw=2.5))
    # plain: from the shoreline (horizon at x~1560) eastward; its near edge disappears behind the hill
    shore = [(1565, HORIZON - 2), (1470, 980), (1340, 1025), (1210, 1080), (1090, 1145), (990, 1220)]
    d = S.smooth_path(shore, closed=False)
    d += f" L{SW + 40},{SH + 60} L{SW + 40},{HORIZON - 2} Z"
    plain = f'<path d="{d}" fill="url(#e13plain)" stroke="{P["ink"]}" stroke-width="3" stroke-linejoin="round"/>'
    foam = S.path(S.smooth_path([(p[0] - 6, p[1] + 2) for p in shore], closed=False), stroke=False,
                  extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="0.8" stroke-linecap="round"')
    # field patches, furrows and a road from behind the hill toward the city gate
    rng = random.Random(12)
    fields = ""
    for cx, cy, w, h, col in ((1720, 1060, 260, 40, "#cdb46c"), (2050, 1110, 330, 52, "#d7a96a"),
                              (2480, 1060, 300, 40, "#c9b773"), (1880, 1200, 300, 60, "#b9b268"),
                              (2380, 1220, 360, 62, "#cfae6c"), (2700, 1150, 260, 50, "#bdb56c"),
                              (1640, 1005, 160, 22, "#d8b878"), (2600, 1010, 200, 24, "#d4b47a")):
        k = (cy - 980) / 300
        fields += (f'<path d="{S.blob(cx, cy, w / 2, h / 2, 0.08, 8, seed=int(cx))}" fill="{col}" opacity="0.75"/>')
        for j in range(3):
            yy = cy - h * 0.25 + j * h * 0.25
            fields += (f'<path d="M{f1(cx - w * 0.36)},{f1(yy)} L{f1(cx + w * 0.36)},{f1(yy)}" stroke="#a98a52" '
                       f'stroke-width="{f1(1.5 + 2 * k)}" opacity="0.4" stroke-linecap="round"/>')
    for _ in range(12):
        x = rng.uniform(1450, 2750)
        y = rng.uniform(1000, 1290)
        ln = rng.uniform(60, 160) * (0.6 + (y - 980) / 300)
        fields += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-3 {f1(ln)},0" stroke="#b6955a" stroke-width="2.5" '
                   f'fill="none" stroke-linecap="round" opacity="0.4"/>')
    road = (f'<path d="M1620,1250 C1760,1140 1900,1070 2050,1035 S2200,1000 2232,{CITY_Y + 2}" stroke="#f4dcaa" '
            f'stroke-width="20" fill="none" stroke-linecap="round" opacity="0.9"/>'
            f'<path d="M1620,1250 C1760,1140 1900,1070 2050,1035 S2200,1000 2232,{CITY_Y + 2}" stroke="#c99b5d" '
            f'stroke-width="2" fill="none" stroke-dasharray="6 14" opacity="0.5"/>')
    sheep = ""
    for x, y, f in ((2290, 1155, -1), (2330, 1168, 1), (2560, 1062, -1), (1830, 1118, 1)):
        sheep += PR.animal(x, y, 0.17 + (y - 1050) / 2500, facing=f, kind="sheep")
    deco = ""
    for x, y, s, ln in ((1690, 1002, 0.2, -0.2), (1735, 1008, 0.17, 0.2), (2730, 1000, 0.2, 0.1),
                        (1980, 1062, 0.24, 0.1), (2560, 1110, 0.27, -0.15), (2620, 1118, 0.22, 0.2)):
        deco += PR.palm_tree(x, y, s, lean=ln, dates=False)
    for x, y, s, v in ((1600, 1040, 0.3, 0), (2420, 1150, 0.34, 1), (2140, 1110, 0.3, 3)):
        deco += PR.bush(x, y, s, v)
    city_glow = f'<ellipse cx="{(CITY_X0 + CITY_X1) / 2}" cy="{CITY_Y - 120}" rx="620" ry="230" fill="#ffdca0" ' \
                f'opacity="0.25" filter="url(#blur-md)"/>'
    city = PR.nineveh_skyline(CITY_X0, CITY_X1, CITY_Y, scale=CITY_S, seed=2, haze=0.22, tint="#f6c08f")

    # Jonah's hill
    pts = [(x, hill_y(x)) for x in range(-80, SW + 81, 40)]
    hd = S.smooth_path(pts, closed=False) + f" L{SW + 80},{SH + 80} L-80,{SH + 80} Z"
    hill = (f'<path d="{hd}" fill="url(#e13hill)" stroke="{P["ink"]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="{hd}" fill="url(#e13hillsh)"/>')
    hatch = ""
    rng2 = random.Random(44)
    for _ in range(26):   # soft darker / lighter dabs of grass colour
        x = rng2.uniform(300, 2700)
        top = hill_y(x)
        y = top + 60 + rng2.random() * 380
        if y > SH + 40:
            continue
        col = rng2.choice(["#7fa553", "#9cc06a", "#7a9a52"])
        hatch += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng2.uniform(80, 200))}" ry="{f1(rng2.uniform(18, 40))}" '
                  f'fill="{col}" opacity="0.28" filter="url(#soft)"/>')
    for _ in range(80):  # little three-blade grass ticks
        x = rng2.uniform(380, 2750)
        top = hill_y(x)
        y = top + 26 + rng2.random() ** 1.5 * 430
        if y > SH or abs(x - JONAH_X) < 70 and y < top + 70:
            continue
        k = 0.8 + (y - 1100) / 450
        col = "#62853f" if x < JONAH_X + 250 else "#56733f"
        hatch += (f'<path d="M{f1(x - 3 * k)},{f1(y)} q{f1(-1 * k)},-{f1(7 * k)} {f1(-7 * k)},-{f1(11 * k)} '
                  f'M{f1(x)},{f1(y)} q{f1(0.5 * k)},-{f1(9 * k)} {f1(3 * k)},-{f1(16 * k)} '
                  f'M{f1(x + 3 * k)},{f1(y)} q{f1(2 * k)},-{f1(6 * k)} {f1(8 * k)},-{f1(9 * k)}" stroke="{col}" '
                  f'stroke-width="{f1(2.3 * k)}" fill="none" stroke-linecap="round" opacity="0.7"/>')
    # sunlit rim on the left (sun-facing) shoulder of the hill
    rim_pts = [(x, hill_y(x) + 7) for x in range(1020, 1520, 30)]
    rim = S.path(S.smooth_path(rim_pts, closed=False), stroke=False,
                 extra='stroke="#f4e39a" stroke-width="7" fill="none" opacity="0.75" stroke-linecap="round"')
    # sandy shore at the lower left where the hill meets the sea, with a foam line
    sand_top = [(x, hill_y(x) + 3) for x in range(-80, 1000, 40)]
    sand_bot = [(x, hill_y(x) + 46 + 10 * math.sin(x / 90)) for x in range(960, -81, -40)]
    sd = S.smooth_path(sand_top, closed=False) + "".join(f" L{f1(x)},{f1(y)}" for x, y in sand_bot) + " Z"
    sand = f'<path d="{sd}" fill="#ecc99a" opacity="0.95"/>'
    shore_foam = S.path(S.smooth_path([(x, hill_y(x) - 2) for x in range(-80, 1010, 40)], closed=False),
                        stroke=False,
                        extra=f'stroke="{P["foam"]}" stroke-width="7" fill="none" opacity="0.9" stroke-linecap="round"')
    rocks = ""
    for x, w, h, sd_ in ((150, 70, 34, 1), (225, 46, 24, 2), (560, 54, 26, 3)):
        y = hill_y(x) + 6
        rocks += (f'<path d="{S.blob(x, y - h * 0.4, w / 2, h / 2, 0.15, 8, seed=sd_)}" fill="#a28c8c" '
                  f'stroke="{P["ink"]}" stroke-width="3"/>')
        rocks += (f'<path d="M{f1(x - w * 0.42)},{f1(y - h * 0.45)} q{f1(w * 0.2)},-{f1(h * 0.4)} {f1(w * 0.45)},'
                  f'-{f1(h * 0.42)}" stroke="#f1d9b3" stroke-width="3" fill="none" opacity="0.8"/>')
    # Jonah's warm halo of light on the ground + shadow
    jy = hill_y(JONAH_X)
    halo = f'<ellipse cx="{JONAH_X}" cy="{jy}" rx="230" ry="46" fill="url(#e13jglow)"/>'
    shadow = C.ground_shadow(JONAH_X + 18, jy + 3, JONAH_S, width=130, opacity=0.25)
    # flowers dotted on the hill
    fl = ""
    rng = random.Random(33)
    for _ in range(60):
        x = rng.uniform(600, 2500)
        if abs(x - JONAH_X) < 90:
            continue
        y = hill_y(x) + rng.uniform(25, 120 + abs(x - JONAH_X) * 0.12)
        if y > SH:
            continue
        col = rng.choice(["#f7e3a1", "#f3a9a0", "#fbf1d8", "#e9c46a"])
        r = rng.uniform(4, 7)
        fl += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{P["ink"]}" stroke-width="1.5"/>'

    front = ""   # bigger flower clumps and bushes on the near slope (static)
    for x, dy, v, sc_ in ((1120, 150, 2, 1.0), (1650, 190, 2, 1.1), (900, 260, 0, 1.2), (1900, 300, 2, 1.15),
                          (1330, 330, 0, 1.25)):
        front += PR.grass_tuft(x, hill_y(x) + dy, sc_, variant=v)
    front += PR.bush(2330, hill_y(2330) + 40, 0.75, 1) + PR.bush(470, hill_y(470) + 60, 0.6, 3)

    body = (S.g(far_hills, filter="wobble") + city_glow + city +
            S.g(plain + fields + road + foam, filter="wobble") + deco + sheep +
            S.g(hill + rim, filter="wobble") + S.g(hatch, filter="wobble-fine") + S.g(sand + shore_foam + rocks, filter="wobble") +
            halo + shadow + S.g(fl, filter="wobble-fine") + front)
    return doc(body, defs)


def city_lights(scene_cache={}):
    """Warm window lights on the skyline: positions sampled from the rasterised skyline's solid areas."""
    key = (CITY_X0, CITY_X1, CITY_Y, CITY_S)
    if key in scene_cache:
        return scene_cache[key]
    sk = doc(PR.nineveh_skyline(CITY_X0, CITY_X1, CITY_Y, scale=CITY_S, seed=2, haze=0.22, tint="#f6c08f"))
    a = np.asarray(raster.rasterize(sk, SW, SH).getchannel("A")) > 250
    a = ndimage.binary_erosion(a, iterations=7)
    rng = random.Random(17)
    pts = []
    y0, y1 = int(CITY_Y - 240), int(CITY_Y - 62)
    for _ in range(6000):
        x = rng.randint(CITY_X0 + 10, CITY_X1 - 10)
        y = rng.randint(y0, y1)
        if not a[y, x]:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 30 ** 2 for px, py in pts):
            continue
        pts.append((x, y))
        if len(pts) >= 44:
            break
    scene_cache[key] = pts
    return pts


def lights_svg(pts):
    body = ""
    for x, y in pts:
        body += f'<circle cx="{x}" cy="{y}" r="15" fill="#ffd27a" opacity="0.28"/>'
        body += (f'<rect x="{x - 3.5}" y="{y - 5}" width="7" height="10" rx="2.5" fill="#ffe08e" '
                 f'stroke="#9a5a2a" stroke-width="1.2"/>')
    return doc(body)


# ============================================================================ ship / fish / splash


def ship_svg(x, wl):
    clip = f'<clipPath id="e13shipclip"><rect x="{x - 400}" y="{wl - 400}" width="800" height="{400 + 4}"/></clipPath>'
    ship = PR.ship(x, wl, SHIP_S, facing=-1, sail="full", lantern=True)
    wake = (f'<path d="M{x - 115},{wl + 2} q60,-7 120,-2 q50,4 95,1" stroke="{P["foam"]}" stroke-width="4" '
            f'fill="none" stroke-linecap="round" opacity="0.85"/>'
            f'<path d="M{x + 70},{wl + 9} q50,-4 110,0" stroke="{P["foam"]}" stroke-width="3" fill="none" '
            f'stroke-linecap="round" opacity="0.6"/>')
    return doc(f'<g clip-path="url(#e13shipclip)">{ship}</g>' + S.g(wake, filter="wobble-fine"), clip)


def splash_svg(x, y):
    rng = random.Random(int(x) + 3)
    drops = ""
    for i in range(8):
        a = math.radians(-160 + 140 * i / 7 + rng.uniform(-8, 8))
        dist = rng.uniform(45, 95)
        dx, dy = math.cos(a) * dist, math.sin(a) * dist * 1.15
        r = rng.uniform(6, 11)
        rot = math.degrees(a) + 90
        drops += (f'<ellipse cx="{f1(x + dx)}" cy="{f1(y + dy)}" rx="{f1(r * 0.7)}" ry="{f1(r)}" '
                  f'transform="rotate({f1(rot)} {f1(x + dx)} {f1(y + dy)})" fill="{P["foam"]}" '
                  f'stroke="{P["ink"]}" stroke-width="2.5"/>')
    crown = (f'<path d="M{x - 78},{y + 4} C{x - 66},{y - 30} {x - 48},{y - 58} {x - 30},{y - 34} '
             f'C{x - 20},{y - 70} {x + 6},{y - 82} {x + 14},{y - 40} C{x + 30},{y - 66} {x + 56},{y - 52} '
             f'{x + 58},{y - 22} C{x + 70},{y - 30} {x + 80},{y - 10} {x + 82},{y + 4} Z" fill="{P["foam"]}" '
             f'stroke="{P["ink"]}" stroke-width="3"/>')
    base = (f'<ellipse cx="{x}" cy="{y + 4}" rx="98" ry="15" fill="{P["foam"]}" stroke="{P["ink"]}" '
            f'stroke-width="2.5" opacity="0.95"/>')
    return doc(S.g(base + crown + drops, filter="wobble-fine"))


def ripple_svg(x, y):
    body = (f'<ellipse cx="{x}" cy="{y}" rx="70" ry="11" fill="none" stroke="{P["foam"]}" stroke-width="5" '
            f'opacity="0.85"/>'
            f'<ellipse cx="{x}" cy="{y + 2}" rx="120" ry="18" fill="none" stroke="{P["foam"]}" stroke-width="3.5" '
            f'opacity="0.55"/>')
    return doc(S.g(body, filter="wobble-fine"))


# ============================================================================ doves


DOVE_BASE = (1400, 800)
DOVE_WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)
FLAP_CYCLE = (0, 1, 2, 3, 4, 3, 2, 1)
STAND = 5


def dove_frames():
    x, y = DOVE_BASE
    frames = [doc(PR.dove(x, y, 1.0, facing=-1, wing=w)) for w in DOVE_WINGS]
    frames.append(doc(PR.dove(x, y, 1.0, facing=-1, pose="stand")))
    return frames


class DoveFlight:
    """Quadratic-Bezier flight from p0 (t0) to p2 (t1); optional landing (then 'stand')."""

    def __init__(self, t0, t1, p0, p1, p2, scale, land=False, phase=0.0, flap_fps=15.0, glide=(1.1, 0.7),
                 scale_end=None):
        self.t0, self.t1, self.p0, self.p1, self.p2 = t0, t1, p0, p1, p2
        self.scale, self.land, self.phase, self.flap_fps, self.glide = scale, land, phase, flap_fps, glide
        self.scale_end = scale if scale_end is None else scale_end

    def pos(self, t):
        u = min(1.0, max(0.0, (t - self.t0) / (self.t1 - self.t0)))
        if self.land:
            u = 1 - (1 - u) ** 1.6   # slow down for the landing
        return bez(self.p0, self.p1, self.p2, u)

    def motion(self, t):
        if t < self.t0 - 0.05:
            return Tf(alpha=0.0)
        x, y = self.pos(t)
        bobv = 0.0
        if self.land and t > self.t1:
            bobv = -2.5 * abs(math.sin(2 * math.pi * (t - self.t1) * 0.9 + self.phase))  # little pecks/hops
        else:
            bobv = 6 * math.sin(2 * math.pi * (t * 1.6 + self.phase))
        u = min(1.0, max(0.0, (t - self.t0) / (self.t1 - self.t0)))
        k = M.lerp(self.scale, self.scale_end, u)
        return Tf(dx=x - DOVE_BASE[0], dy=y - DOVE_BASE[1] + bobv * k, sx=k, sy=k,
                  px=DOVE_BASE[0], py=DOVE_BASE[1])

    def frame(self, t):
        if self.land and t >= self.t1:
            return float(STAND)
        if self.land and t >= self.t1 - 0.35:
            return 0.0                          # wings up, flaring to land
        on, off = self.glide
        cyc = (t - self.t0 + self.phase * (on + off)) % (on + off)
        if cyc > on:
            return 2.0                          # glide
        return float(FLAP_CYCLE[int(cyc * self.flap_fps) % len(FLAP_CYCLE)])


# ============================================================================ end card


def card_text_svg():
    return doc(S.text(CARD_X, CARD_Y, "约拿的故事 · 完", size=172, fill="#fff3d6",
                      extra=f'stroke="{P["ink"]}" stroke-width="13" paint-order="stroke" stroke-linejoin="round"'))


def card_glow_svg():
    defs = S.rad_grad("e13card", [(0, "#ffe9bb", 0.42), (0.6, "#ffd9a8", 0.16), (1, "#ffd9a8", 0)])
    return doc(f'<ellipse cx="{CARD_X}" cy="{CARD_Y - 40}" rx="820" ry="250" fill="url(#e13card)"/>', defs)


def swash_svg(side):
    """Hand-drawn flourish under the title; side -1 = left half, +1 = right half."""
    cx, y = CARD_X, CARD_Y + 84

    def X(v):
        return f1(cx + side * v)
    d = (f"M{X(84)},{y - 2} C{X(150)},{y + 10} {X(240)},{y + 12} {X(330)},{y - 4} "
         f"C{X(380)},{y - 14} {X(400)},{y - 40} {X(372)},{y - 46} C{X(346)},{y - 50} {X(338)},{y - 22} {X(366)},{y - 12} "
         f"C{X(410)},{y + 4} {X(460)},{y - 6} {X(500)},{y - 20}")
    return doc(f'<path d="{d}" stroke="{P["ink"]}" stroke-width="17" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/>'
               f'<path d="{d}" stroke="#fff3d6" stroke-width="8" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/>')


HEART = (CARD_X, CARD_Y + 86)


def heartbeat(t0, amp=0.06, period=1.1):
    """A soft 'lub' pulse of the heart every ``period`` s after t0 (scale around HEART)."""
    def m(t):
        if t <= t0:
            return Tf(px=HEART[0], py=HEART[1])
        k = 1 + amp * max(0.0, math.sin(2 * math.pi * (t - t0) / period)) ** 4
        return Tf(sx=k, sy=k, px=HEART[0], py=HEART[1])
    return m


def heart_svg():
    x, y = HEART
    r = 40
    d = (f"M{x},{y + 0.95 * r} C{x - 1.7 * r},{y - 0.1 * r} {x - 0.95 * r},{y - 1.3 * r} {x},{y - 0.5 * r} "
         f"C{x + 0.95 * r},{y - 1.3 * r} {x + 1.7 * r},{y - 0.1 * r} {x},{y + 0.95 * r} Z")
    body = (f'<path d="{d}" fill="#e8706a" stroke="{P["ink"]}" stroke-width="5" stroke-linejoin="round"/>'
            f'<ellipse cx="{x - 0.62 * r}" cy="{y - 0.48 * r}" rx="{0.22 * r}" ry="{0.14 * r}" '
            f'transform="rotate(-35 {x - 0.62 * r} {y - 0.48 * r})" fill="#fde3d6"/>')
    return doc(S.g(body, filter="wobble-fine"))


# ============================================================================ warm light


def warm_svg():
    """Golden light from the setting sun (additive): a wide warm bloom, soft rays fanning up over the sky and a
    glow around Jonah. Additive (not 'screen') so bright areas never wrap."""
    sx, sy = SUN
    defs = (S.rad_grad("e13warm", [(0, "#ffcf87", 0.38), (0.3, "#ffb874", 0.16), (1, "#ffb070", 0)]) +
            f'<radialGradient id="e13ray" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="2300">'
            '<stop offset="0" stop-color="#ffd890" stop-opacity="0.34"/>'
            '<stop offset="0.5" stop-color="#ffcf88" stop-opacity="0.16"/>'
            '<stop offset="1" stop-color="#ffcf88" stop-opacity="0.03"/></radialGradient>' +
            S.rad_grad("e13jwarm", [(0, "#ffd890", 0.22), (1, "#ffd890", 0)]))
    rng = random.Random(8)
    d = ""
    for i in range(9):
        a = math.radians(-172 + i * 19 + rng.uniform(-4, 4))
        wa = math.radians(rng.uniform(2.2, 3.8))
        r0, r1 = SUN_R + 60, 2400
        pts = [(sx + r0 * math.cos(a - wa / 3), sy + r0 * math.sin(a - wa / 3)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 3), sy + r0 * math.sin(a + wa / 3))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    clip = f'<clipPath id="e13sky_only"><rect x="-20" y="-20" width="{SW + 40}" height="{HORIZON + 20}"/></clipPath>'
    body = (f'<ellipse cx="{sx}" cy="{sy}" rx="1900" ry="1000" fill="url(#e13warm)"/>'
            f'<g clip-path="url(#e13sky_only)"><path d="{d}" fill="url(#e13ray)" filter="url(#blur-md)"/></g>'
            f'<ellipse cx="{JONAH_X}" cy="{hill_y(JONAH_X) - 130}" rx="300" ry="280" fill="url(#e13jwarm)"/>')
    return doc(body, defs + clip)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.line(0), ctx.line(1)
    d0, d1 = L0.end - L0.start, L1.end - L1.start
    t_sea = L0.start + 0.355 * d0       # "比海更宽"
    t_sky = L0.start + 0.697 * d0       # "比天更高"
    t_all = L1.start                    # "他愿意给每一个人"
    t_new = L1.start + 0.53 * d1        # "重新开始的机会"
    t_card = L1.end + 0.05              # end card

    # ------------------------------------------------------------------ sky
    sc.add("sky", sky_svg(), wc=0.55)
    sc.add("dusk", dusk_svg(stars_markup(2, 8, 30)), wc=0,
           motion=M.keys([(t_sky - 0.3, {"alpha": 0}), (t_sky + 1.6, {"alpha": 0.8}), (T, {"alpha": 1.0})], "sine"))
    star_in = lambda a, b: M.keys([(a, {"alpha": 0}), (b, {"alpha": 1})], "sine")  # noqa: E731
    sc.add("stars_a", stars_svg(1, 10, 34), wc=0,
           motion=M.combine(star_in(t_sky + 0.1, t_sky + 1.3), M.pulse(0.55, 1.0, 1.9)))
    ev = (600, 560)
    sc.add("evening_star", evening_star_svg(*ev), wc=0,
           motion=M.combine(M.keys([(t_sky - 0.1, {"alpha": 0, "s": 0.2}), (t_sky + 0.45, {"alpha": 1, "s": 1.0})],
                                   "back", pivot=ev), M.pulse(0.75, 1.0, 1.4)))
    sc.add("sun", sun_svg(), motion=M.keys([(0, {"dy": 0}), (T, {"dy": 58})], "linear"))
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=7))

    # ------------------------------------------------------------------ sea
    sc.add("sea", sea_svg())
    glit = [glitter_svg(s) for s in (1, 2, 3)]
    sc.add("glitter", glit + [glit[0]], wc=0.3, frame_at=lambda t: (t * 2.6) % 3.0,
           motion=M.pulse(0.75, 1.0, 2.3))
    ship_wl = MID_WL + 2
    sc.add("ship", ship_svg(SHIP_X, ship_wl), motion=M.combine(
        M.drift(vx=-9),
        M.sway(1.6, 3.6, pivot=(SHIP_X, ship_wl)),
        M.bob(3, 2.9)))

    # the great fish: two happy leaps (behind the near sea band)
    leaps = [  # (start, duration, x_start_centre, x_end_centre, facing)
        (t_sea - 0.12, 1.35, 770, 330, -1),
        (t_new - 0.25, 1.35, 200, 610, 1),
    ]
    splash_events = []
    for i, (ls, ld, xa, xb, fc) in enumerate(leaps):
        fx0, fy0 = (xa + xb) / 2, NEAR_WL
        frames = [doc(PR.fish(fx0, fy0, FISH_S, facing=fc, eye="happy", mouth=0.12, tail=tv))
                  for tv in (0.65, 0.0, -0.65)]
        rise, drop = 185, 190

        def fish_motion(t, ls=ls, ld=ld, xa=xa, xb=xb, fc=fc, fx0=fx0, fy0=fy0):
            u = (t - ls) / ld
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            x = xa + (xb - xa) * u
            y = NEAR_WL + rise - (rise + drop) * 4 * u * (1 - u)
            rot = fc * (-40 + 86 * M.ease("sine")(u))
            return Tf(dx=x - fx0, dy=y - fy0, rot=rot, px=fx0, py=fy0)

        sc.add(f"fish{i}", frames, motion=fish_motion, seed=90 + i,
               frame_at=lambda t: float((0, 1, 2, 1)[int(t * 9) % 4]))
        # waterline crossings for the splashes
        ue = 0.13
        ur = 0.84
        splash_events.append((ls + ue * ld, xa + (xb - xa) * ue + fc * 95))
        splash_events.append((ls + ur * ld, xa + (xb - xa) * ur + fc * 40))

    sc.add("sea_near", near_sea_svg(), motion=M.combine(M.bob(9, 6.0, axis="x"), M.bob(2.5, 3.1)))

    sp0 = (600, NEAR_WL)
    sp_svg, rp_svg = splash_svg(*sp0), ripple_svg(*sp0)
    for k, (ts, xs) in enumerate(splash_events):
        dx = xs - sp0[0]
        sc.add(f"ripple{k}", rp_svg, wc=0.4, seed=71, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.5, "sy": 0.5}), (ts + 0.05, {"alpha": 1, "sx": 0.6, "sy": 0.6}),
                    (ts + 1.6, {"alpha": 0, "sx": 1.9, "sy": 1.5})], "out", pivot=sp0),
            M.still(Tf(dx=dx))))
        sc.add(f"splash{k}", sp_svg, wc=0.4, seed=73, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.3, "sy": 0.2}), (ts + 0.02, {"alpha": 1, "sx": 0.45, "sy": 0.35}),
                    (ts + 0.28, {"alpha": 1, "sx": 1.0, "sy": 1.0}), (ts + 0.75, {"alpha": 0, "sx": 1.15, "sy": 0.7})],
                   "out", pivot=(sp0[0], sp0[1] + 8)),
            M.still(Tf(dx=dx))))
        sc.sfx("splash_small", ts - 0.03, gain_db=-16, pan=-0.6)

    # ------------------------------------------------------------------ land, city, Jonah
    sc.add("land", land_svg())
    pts = city_lights()
    sc.add("city_lights", lights_svg(pts), wc=0, motion=M.combine(
        M.keys([(0, {"alpha": 0.45}), (t_all - 0.2, {"alpha": 0.55}), (t_all + 1.0, {"alpha": 1.0})], "sine"),
        M.pulse(0.85, 1.0, 1.7)))

    jy = hill_y(JONAH_X) + 4
    j_frames = [doc(C.jonah(JONAH_X, jy, JONAH_S, 1, pose="stand", expr=e)) for e in ("happy", "peaceful")]
    t_eyes_close, t_eyes_open = t_all + 0.55, t_new + 0.45
    sc.add("jonah", j_frames, seed=55,
           frame_at=lambda t: 1.0 if t_eyes_close <= t < t_eyes_open else 0.0,
           motion=M.breathe(0.012, 3.4, pivot=(JONAH_X, jy)))

    tufts = []
    for sw_ in (-0.6, 0.0, 0.6):
        body = ""
        for x, v, s in ((1215, 2, 0.75), (1290, 0, 0.6), (1545, 0, 0.62), (1660, 2, 0.8), (1010, 0, 0.8),
                        (1840, 1, 0.75), (860, 2, 0.9), (2050, 0, 0.9)):
            body += PR.grass_tuft(x, hill_y(x) + 8, s, variant=v, sway=sw_ * (0.8 if v == 2 else 1.0))
        tufts.append(doc(body))
    sc.add("tufts", tufts, frame_at=lambda t: 1.0 + 0.999 * math.sin(2 * math.pi * t / 3.2))

    # foreground framing in the lower corners (in the cool shade of the hill), gently swaying
    shade_f = ('<filter id="e13fgshade" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
               'values="0.7 0 0 0 0.05  0 0.7 0 0 0.035  0 0 0.76 0 0.09  0 0 0 1 0"/></filter>')
    fl_ = (PR.reeds(70, 1612, 1.15, variant=1) + PR.grass_tuft(200, 1612, 2.1, variant=0) +
           PR.grass_tuft(330, 1616, 1.6, variant=2))
    fr_ = (PR.bush(2720, 1640, 1.35, 1) + PR.grass_tuft(2540, 1618, 2.0, variant=2) +
           PR.grass_tuft(2440, 1622, 1.5, variant=0))
    sc.add("fg_left", doc(f'<g filter="url(#e13fgshade)">{fl_}</g>', shade_f), motion=M.sway(1.1, 4.2, (200, 1612)))
    sc.add("fg_right", doc(f'<g filter="url(#e13fgshade)">{fr_}</g>', shade_f),
           motion=M.sway(0.9, 4.8, (2600, 1630), 0.4))

    # ------------------------------------------------------------------ warm light (line 1)
    sc.add("warm", warm_svg(), wc=0, blend="add", motion=M.combine(
        M.keys([(0, {"alpha": 0.18}), (t_all - 0.3, {"alpha": 0.2}), (t_all + 1.3, {"alpha": 1.0}),
                (T, {"alpha": 0.85})], "sine"),
        M.pulse(0.88, 1.0, 3.0)))

    # ------------------------------------------------------------------ doves
    dframes = dove_frames()
    LD = 0.78  # landed doves' scale

    def gy(x):  # dove 'stand' feet are at +38*scale below its anchor
        return hill_y(x) - 38 * LD + 3
    flights = [
        DoveFlight(t_all + 0.05, t_new + 0.35, (2900, 380), (1950, 700), (1530, gy(1530)), LD, land=True,
                   phase=0.1),
        DoveFlight(t_all + 0.35, t_new + 0.75, (2930, 480), (2050, 800), (1612, gy(1612)), LD * 0.96, land=True,
                   phase=0.45),
        # a little flock glides on westward over Jonah, toward the sunset, growing smaller in the distance
        DoveFlight(t_all + 0.15, T + 0.4, (2920, 660), (1800, 660), (640, 850), 0.9, phase=0.3, scale_end=0.42),
        DoveFlight(t_all + 0.55, T + 0.7, (2960, 750), (1900, 740), (780, 890), 0.8, phase=0.7, scale_end=0.38),
        DoveFlight(t_all + 0.85, T + 0.5, (2940, 600), (1750, 700), (560, 885), 0.85, phase=0.55, scale_end=0.4),
    ]
    for k, fl in enumerate(flights):
        sc.add(f"dove{k}", dframes, seed=77, motion=fl.motion, frame_at=fl.frame)

    # ------------------------------------------------------------------ end card
    sc.add("card_glow", card_glow_svg(), wc=0, motion=M.keys([(t_card - 0.1, {"alpha": 0}),
                                                               (t_card + 0.7, {"alpha": 1})], "sine"))
    sc.add("card_text", card_text_svg(), wc=0, motion=M.combine(
        M.keys([(t_card, {"alpha": 0, "s": 0.95, "dy": 18}), (t_card + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
               pivot=(CARD_X, CARD_Y - 50)),
        M.breathe(0.004, 4.0, pivot=(CARD_X, CARD_Y - 50))))
    sw0, sw1 = t_card + 0.3, t_card + 0.95
    sc.add("swash_l", swash_svg(-1), wc=0,
           reveal=lambda t: {"mode": "right", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    sc.add("swash_r", swash_svg(1), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    th = t_card + 0.5
    sc.add("heart", heart_svg(), wc=0, motion=M.combine(
        M.keys([(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back",
               pivot=HEART),
        heartbeat(th + 0.6)))

    # ------------------------------------------------------------------ camera
    W0, W1 = 1500.0, 2720.0
    B0, B1 = 1430.0, 1556.0

    def cam(t):
        s = M.progress(t, 0.5, 3.75, "inout")
        w = M.lerp(W0, W1, s)
        bottom = M.lerp(B0, B1, s)
        p = M.progress(t, 3.9, T, "sine")
        w2 = w - 50 * p
        cy = bottom - w * 9 / 32 - 10 * p
        return Cam(JONAH_X, cy, w2)
    sc.camera = cam

    # ------------------------------------------------------------------ fx
    sc.fx = [
        FX.sparkles((CITY_X0 + 40, CITY_Y - 230, CITY_X1 - 40, CITY_Y - 40), count=16, t0=t_all + 0.2,
                    color=(255, 236, 170), size=(6, 13), period=1.8, drift=0, seed=31),
        FX.motes((200, 380, 2600, 1250), count=34, t0=t_all - 0.2, color=(255, 236, 190), size=(2.5, 6),
                 alpha=120, seed=17),
        FX.sparkles((HEART[0] - 110, HEART[1] - 70, HEART[0] + 110, HEART[1] + 40), count=7, t0=th + 0.2,
                    color=(255, 240, 200), size=(7, 14), period=1.4, drift=0, seed=5),
    ]

    # ------------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-12, fade_in=0.8, fade_out=1.6, pan=-0.3)
    sc.sfx("birds", t_all - 0.4, dur=T - t_all + 0.8, gain_db=-18, fade_in=1.0, fade_out=1.6, pan=0.2)
    sc.sfx("chime", t_card, gain_db=-8)
    return sc
