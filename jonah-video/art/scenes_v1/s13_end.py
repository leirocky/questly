"""Scene 13 — closing page: God's love is wider than the sea and higher than the sky.

One wide sunset double-page spread on a 2800 x 1620 stage (no cuts):
  * WEST (left): the calm sea under the setting sun, a golden glitter path, the little ship (with three
    sailors on deck) sailing toward the sun and the great fish leaping happily out past the ship — it leaps
    from the mid sea band, so at that depth it is about twice the ship's length (a really huge fish).
  * MIDDLE: Jonah standing peacefully on a grassy hill, looking out over it all.
  * EAST (right): a golden plain with the city of Nineveh glowing in the last light, a few townspeople at the
    end of the road.
  * ABOVE: a huge, high dusk sky — sunset gradient, layered evening clouds, the evening star and the first stars.

Timing (all keyed to the narration, phrase times derived from ctx.lines):
  * opening: a dip through the blank warm page. The scene starts as plain paper colour, so the 0.8 s
    cross-dissolve from s12 fades s12 out to the page, and the page then fades back up to this picture
    (PAPER_DIP). The two Jonahs (s12's large seated one and this small standing one) are never on screen
    together. The opening framing is kept: Jonah on the left third, looking east at Nineveh.
  * line 0 "上帝的爱，比海更宽，比天更高。": two-stage camera. "比海更宽": the frame widens (top kept low,
    sweeping west) so the sea opens up and the great fish leaps across the sun's glitter path; "比天更高": the
    frame tilts up and grows to the full spread, the sky deepens and the evening star and first stars come out.
  * line 1 "他愿意给每一个人，重新开始的机会。": the camera pushes in on Jonah; warm golden light blooms from the
    sun over everything (rays, glow, motes, a warm rim on Jonah's sun side), Nineveh's lamps light up and the
    townspeople step into the light, the sailors wave, Jonah closes his eyes in the warm light, doves fly in
    from the east above the city — two land beside Jonah, three glide on toward the sunset — and the fish leaps
    once more. The camera then eases back out to make room for the end card.
  * end of the narration: a hand-lettered end card '约拿的故事 · 完' fades in high in the sky, a swash is drawn
    out from its centre and a small heart pops in (chime). The film then fades out (assemble.py).
"""
import bisect
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

SHIP_X, SHIP_S = 1000, 0.19
FISH_S = 0.32            # leaps from the MID band (same depth as the ship): ~2x the ship's length
SPLASH_K = 0.8           # splash / ripple size at the mid-band depth

# Dip through the warm paper colour at the s12 -> s13 cross-dissolve. The xfade mixes s12 * (1 - t/0.8) with this
# scene * t/0.8. The page fully covers this scene until PAPER_DIP[0], when s12 is down to ~5 %, and then lifts
# (eased) by PAPER_DIP[1], before the fish's first leap. The result is s12 -> blank page (~99 % page at t = 0.8)
# -> s13, so the two Jonahs never share a frame (overlap < 0.1 %).
PAPER_RGB = (243, 233, 210)   # the compositor's blank-page base colour (paper grain is multiplied on top)
PAPER_DIP = (0.76, 1.4)


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


def bez3(p0, c1, c2, p3, u):
    v = 1 - u
    a, b, c, d = v * v * v, 3 * v * v * u, 3 * v * u * u, u * u * u
    return (a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1])


def smooth_keys(keys):
    """Monotone cubic (Fritsch-Carlson) interpolation through (t, v) keys: smooth velocity through
    intermediate keys, no overshoot, flat at the ends and at local extrema/holds."""
    ts = [k[0] for k in keys]
    vs = [k[1] for k in keys]
    n = len(keys)
    d = [(vs[i + 1] - vs[i]) / (ts[i + 1] - ts[i]) for i in range(n - 1)]
    m = [0.0] * n
    for i in range(1, n - 1):
        if d[i - 1] * d[i] > 0:
            h0, h1 = ts[i] - ts[i - 1], ts[i + 1] - ts[i]
            w1, w2 = 2 * h1 + h0, h1 + 2 * h0
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])

    def f(t):
        if t <= ts[0]:
            return vs[0]
        if t >= ts[-1]:
            return vs[-1]
        i = min(n - 2, bisect.bisect_right(ts, t) - 1)
        h = ts[i + 1] - ts[i]
        s = (t - ts[i]) / h
        h00, h10 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s
        h01, h11 = -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
        return h00 * vs[i] + h10 * h * m[i] + h01 * vs[i + 1] + h11 * h * m[i + 1]
    return f


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


def soft_cloud(cx, cy, w, h, seed, top, lit, op=0.85):
    """Ink-less high cloud: lighter, softer, further away."""
    gid = f"e13s{seed}"
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{lit}"/></linearGradient>')
    body = f'<g opacity="{op}">' + S.cloud(cx, cy, w, h, f"url(#{gid})", seed=seed, sw=0) + "</g>"
    return body, defs


def streak_cloud(cx, cy, w, h, col, op, seed):
    """Thin wind-drawn streak cloud (a few overlapping soft ellipses)."""
    rng = random.Random(seed)
    body = ""
    for k in range(4):
        body += (f'<ellipse cx="{f1(cx + rng.uniform(-0.18, 0.18) * w)}" cy="{f1(cy + (k - 1.5) * h * 0.55)}" '
                 f'rx="{f1(w / 2 * rng.uniform(0.45, 0.95))}" ry="{f1(h * rng.uniform(0.45, 0.8))}" fill="{col}" '
                 f'opacity="{op * rng.uniform(0.7, 1.0):.2f}"/>')
    return f'<g filter="url(#soft)">{body}</g>'


def clouds_svg():
    """Varied evening sky: two big layered clouds lit from below near the horizon (inked), one small inked
    puff over the sea, ink-less soft puffs higher up and thin streaks highest (clear of the end-card box)."""
    inked, defs = "", ""
    for it in (  # back layer first: cx, cy, w, h, seed, top colour, lit underside
            (470, 640, 330, 84, 11, "#c497b4", "#f4c2a4"),
            (300, 695, 480, 108, 3, "#d9a3b6", "#ffd9a0"),
            (2590, 545, 330, 86, 12, "#ab8db6", "#e8b4ac"),
            (2400, 600, 520, 112, 2, "#b993b8", "#f7c1a2"),
            (1030, 772, 250, 58, 5, "#dca3b2", "#ffdca0")):
        b, d = sunset_cloud(*it)
        inked += b
        defs += d
    soft = ""
    for it in ((1880, 735, 210, 48, 7, "#cf9db6", "#fbc9a0", 0.8), (210, 330, 230, 58, 4, "#a48cba", "#dcabbb", 0.7)):
        b, d = soft_cloud(*it)
        soft += b
        defs += d
    streaks = (streak_cloud(2540, 240, 560, 16, "#b8a0c8", 0.75, 1) +
               streak_cloud(400, 165, 440, 13, "#a996c4", 0.7, 2) +
               streak_cloud(2290, 330, 300, 10, "#c7a6c4", 0.6, 3))
    return doc(streaks + soft + S.g(inked, filter="wobble"), defs)


# ============================================================================ sea


def _sea_strokes():
    """Soft wave strokes: (far-band markup, mid-band markup) — same random sequence as before the split."""
    rng = random.Random(5)
    far, mid = "", ""
    for _ in range(26):
        x = rng.uniform(-20, 1650)
        y = rng.uniform(HORIZON + 10, MID_WL - 12)
        ln = rng.uniform(30, 90) * (0.6 + (y - HORIZON) / 140)
        far += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-4 {f1(ln)},0" stroke="#f6dcc8" stroke-width="2.5" '
                f'fill="none" stroke-linecap="round" opacity="0.6"/>')
    for _ in range(30):
        x = rng.uniform(-20, 1700)
        y = rng.uniform(MID_WL + 18, NEAR_WL - 10)
        ln = rng.uniform(40, 120)
        mid += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-6 {f1(ln)},0" stroke="#d9c6e0" stroke-width="3" '
                f'fill="none" stroke-linecap="round" opacity="0.55"/>')
    return far, mid


def sea_far_svg():
    """Far sea from the horizon down (the great fish leaps out of the water in front of it)."""
    defs = (f'<linearGradient id="e13far" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#e4b0a6"/><stop offset="0.12" stop-color="#ad8fad"/>'
            '<stop offset="0.4" stop-color="#6d7aa6"/><stop offset="1" stop-color="#46578a"/></linearGradient>' +
            S.rad_grad("e13seaglow", [(0, "#ffe2a4", 0.55), (0.5, "#f9c495", 0.2), (1, "#f9c495", 0)]))
    # only the strip down to just below the mid band's top edge is ever visible (the mid band, the plain and the
    # hill cover the rest), so the layer stops there — much cheaper to move with the camera every frame
    far_h = MID_WL + 45 - HORIZON
    far = f'<rect x="-20" y="{HORIZON}" width="{SW + 40}" height="{far_h}" fill="url(#e13far)"/>'
    far += (f'<clipPath id="e13farclip"><rect x="-20" y="{HORIZON}" width="{SW + 40}" height="{far_h}"/></clipPath>'
            f'<ellipse cx="{SUN[0]}" cy="{HORIZON + 40}" rx="700" ry="120" fill="url(#e13seaglow)" '
            f'clip-path="url(#e13farclip)"/>')
    far += (f'<path d="M-20,{HORIZON} L{SW + 20},{HORIZON}" stroke="{P["ink"]}" stroke-width="2.5" '
            f'opacity="0.6"/>')
    strokes, _ = _sea_strokes()
    return doc(S.g(far, filter="wobble") + S.g(strokes, filter="wobble-fine"), defs)


def sea_mid_svg():
    """The mid sea band the ship sails on (drawn in front of the leaping fish, so it hides the fish's dive)."""
    defs = (f'<linearGradient id="e13mid" gradientUnits="userSpaceOnUse" x1="0" y1="{MID_WL}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#9886ae"/><stop offset="0.3" stop-color="#6879a6"/>'
            '<stop offset="1" stop-color="#3f5285"/></linearGradient>')
    # (its lower part is always hidden by the near band and the hill, so it ends at NEAR_WL + 45)
    mid = S.path(S.wave_band(MID_WL, 4, 300, 0.7, x0=-60, x1=1760, bottom=NEAR_WL + 45), fill="url(#e13mid)", sw=3)
    crest = S.path(S.wave_line(MID_WL - 3, 4, 300, 0.7, x0=-60, x1=1760), stroke=False,
                   extra='stroke="#fbe6c8" stroke-width="4" fill="none" opacity="0.55"')
    _, strokes = _sea_strokes()
    return doc(S.g(mid + crest, filter="wobble") + S.g(strokes, filter="wobble-fine"), defs)


def glitter_svg(seed, y0=HORIZON + 6, y1=NEAR_WL - 6):
    """The sun's golden path on the water; only the rows with y0 <= y < y1 are drawn (same random sequence)."""
    rng = random.Random(seed)
    body = ""
    y = HORIZON + 6
    while y < NEAR_WL - 6:
        half = 26 + (y - HORIZON) * 0.55
        n = 2 + int((y - HORIZON) / 60)
        for _ in range(n):
            x = SUN[0] + rng.uniform(-half, half)
            ln = rng.uniform(10, 26) * (0.7 + (y - HORIZON) / 180)
            op = rng.uniform(0.55, 0.95)
            if y0 <= y < y1:
                body += (f'<rect x="{f1(x - ln / 2)}" y="{f1(y)}" width="{f1(ln)}" '
                         f'height="{f1(3 + (y - HORIZON) / 90)}" rx="2" fill="#ffe9a8" opacity="{op:.2f}"/>')
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
            '<stop offset="0" stop-color="#bcbd63"/><stop offset="0.42" stop-color="#a6b65d"/>'
            '<stop offset="0.62" stop-color="#8ca858"/><stop offset="1" stop-color="#6f8757"/></linearGradient>'
            # cool violet shade deepening down the near slope (the low sun only lights the crest)
            f'<linearGradient id="e13hillsh" gradientUnits="userSpaceOnUse" x1="0" y1="1100" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#58487a" stop-opacity="0"/>'
            '<stop offset="0.25" stop-color="#58487a" stop-opacity="0.13"/>'
            '<stop offset="1" stop-color="#3f3766" stop-opacity="0.55"/></linearGradient>'
            # the east slope faces away from the sun: extra cool shade toward the right
            '<linearGradient id="e13hillcool" gradientUnits="userSpaceOnUse" x1="1550" y1="0" x2="2800" y2="0">'
            '<stop offset="0" stop-color="#5a4a80" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#5a4a80" stop-opacity="0.24"/></linearGradient>'
            # warm gold-rose sunset glaze along the crest (multiplied, like a transparent watercolour wash),
            # strongest on the sun (west) side
            '<linearGradient id="e13glaze" gradientUnits="userSpaceOnUse" x1="250" y1="0" x2="2500" y2="0">'
            '<stop offset="0" stop-color="#ffc48a" stop-opacity="0.75"/>'
            '<stop offset="0.4" stop-color="#ffc890" stop-opacity="0.6"/>'
            '<stop offset="0.62" stop-color="#ffc0a8" stop-opacity="0.3"/>'
            '<stop offset="1" stop-color="#ffc0a8" stop-opacity="0"/></linearGradient>' +
            S.rad_grad("e13jglow", [(0, "#ffe7a8", 0.55), (1, "#ffe7a8", 0)]))
    # far lavender hills behind the city; the near one starts behind the plain (top at HORIZON-2 from x=1565)
    # so no side edge or fill shows on the sea
    far_hills = (S.path(S.hill(1590, 2200, HORIZON + 6, 70, seed=4, bumps=2), fill="#c59bab", sw=2.5) +
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
    crest_d = S.smooth_path(pts, closed=False)
    hd = crest_d + f" L{SW + 80},{SH + 80} L-80,{SH + 80} Z"
    hill = f'<path d="{hd}" fill="url(#e13hill)"/>'
    hill_ink = f'<path d="{crest_d}" fill="none" stroke="{P["ink"]}" stroke-width="4" stroke-linejoin="round"/>'
    # (each glaze element carries its own clip so it blends with the hill as its backdrop)
    clip = 'clip-path="url(#e13hillclip)"'
    glaze = (f'<clipPath id="e13hillclip"><path d="{hd}"/></clipPath>'
             f'<rect x="-80" y="1000" width="{SW + 160}" height="{SH}" fill="url(#e13hillsh)" {clip}/>'
             f'<rect x="-80" y="1000" width="{SW + 160}" height="{SH}" fill="url(#e13hillcool)" {clip}/>'
             f'<g {clip} style="mix-blend-mode:multiply"><path d="{crest_d}" fill="none" stroke="url(#e13glaze)" '
             f'stroke-width="240" filter="url(#blur-md)"/></g>')
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
    # (the strip tapers to a point at its east end instead of stopping in a vertical cut)
    sand_top = [(x, hill_y(x) + 3) for x in range(-80, 1001, 40)]
    sand_bot = [(x, hill_y(x) + 3 + (43 + 10 * math.sin(x / 90)) * min(1.0, max(0.0, (985 - x) / 300)))
                for x in range(1000, -81, -40)]
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

    # the hill and everything on it share one wobble so the sunset glaze / shade stays inside the inked edge
    hill_group = (hill + S.g(hatch, filter="wobble-fine") + sand + shore_foam + rocks +
                  S.g(fl, filter="wobble-fine") + front + glaze + hill_ink + rim)
    body = (S.g(far_hills, filter="wobble") + city_glow + city +
            S.g(plain + fields + road + foam, filter="wobble") + deco + sheep +
            S.g(hill_group, filter="wobble") + halo + shadow)
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


# sailors on deck: (local x on the ship, variant, facing); the middle one waves during line 1 (Jonah 1:16 —
# the sailors who were saved too)
SAILORS = ((175, 2, 1), (-120, 1, 1), (-265, 3, -1))
WAVE_POSES = ("stand", "pray", "lift")


def ship_svg(x, wl, wave_pose="stand"):
    clip = f'<clipPath id="e13shipclip"><rect x="{x - 400}" y="{wl - 400}" width="800" height="{400 + 4}"/></clipPath>'
    crew = ""
    for i, (lx, var, fc) in enumerate(SAILORS):
        sx, sy = PR.local_to_stage(x, wl, SHIP_S, -1, lx, PR.SHIP_DECK_Y)
        pose = wave_pose if i == 1 else "stand"
        crew += C.sailor(sx, sy, SHIP_S, facing=fc, variant=var, pose=pose, expr="happy", marks=False)
    ship = (PR.ship(x, wl, SHIP_S, facing=-1, sail="full", lantern=True, part="back") + crew +
            PR.ship(x, wl, SHIP_S, facing=-1, sail="full", lantern=True, part="front"))
    wake = (f'<path d="M{x - 115},{wl + 2} q60,-7 120,-2 q50,4 95,1" stroke="{P["foam"]}" stroke-width="4" '
            f'fill="none" stroke-linecap="round" opacity="0.85"/>'
            f'<path d="M{x + 70},{wl + 9} q50,-4 110,0" stroke="{P["foam"]}" stroke-width="3" fill="none" '
            f'stroke-linecap="round" opacity="0.6"/>')
    return doc(f'<g clip-path="url(#e13shipclip)">{ship}</g>' + S.g(wake, filter="wobble-fine"), clip)


def splash_svg(x, y, k=1.0):
    rng = random.Random(int(x) + 3)
    drops = ""
    for i in range(8):
        a = math.radians(-160 + 140 * i / 7 + rng.uniform(-8, 8))
        dist = rng.uniform(45, 95) * k
        dx, dy = math.cos(a) * dist, math.sin(a) * dist * 1.15
        r = rng.uniform(6, 11) * k
        rot = math.degrees(a) + 90
        drops += (f'<ellipse cx="{f1(x + dx)}" cy="{f1(y + dy)}" rx="{f1(r * 0.7)}" ry="{f1(r)}" '
                  f'transform="rotate({f1(rot)} {f1(x + dx)} {f1(y + dy)})" fill="{P["foam"]}" '
                  f'stroke="{P["ink"]}" stroke-width="{f1(2.5 * k)}"/>')

    def X(v):
        return f1(x + v * k)

    def Y(v):
        return f1(y + v * k)
    crown = (f'<path d="M{X(-78)},{Y(4)} C{X(-66)},{Y(-30)} {X(-48)},{Y(-58)} {X(-30)},{Y(-34)} '
             f'C{X(-20)},{Y(-70)} {X(6)},{Y(-82)} {X(14)},{Y(-40)} C{X(30)},{Y(-66)} {X(56)},{Y(-52)} '
             f'{X(58)},{Y(-22)} C{X(70)},{Y(-30)} {X(80)},{Y(-10)} {X(82)},{Y(4)} Z" fill="{P["foam"]}" '
             f'stroke="{P["ink"]}" stroke-width="{f1(3 * k)}"/>')
    base = (f'<ellipse cx="{x}" cy="{Y(4)}" rx="{f1(98 * k)}" ry="{f1(15 * k)}" fill="{P["foam"]}" '
            f'stroke="{P["ink"]}" stroke-width="{f1(2.5 * k)}" opacity="0.95"/>')
    return doc(S.g(base + crown + drops, filter="wobble-fine"))


def ripple_svg(x, y, k=1.0):
    body = (f'<ellipse cx="{x}" cy="{y}" rx="{f1(70 * k)}" ry="{f1(11 * k)}" fill="none" stroke="{P["foam"]}" '
            f'stroke-width="{f1(5 * k)}" opacity="0.85"/>'
            f'<ellipse cx="{x}" cy="{f1(y + 2 * k)}" rx="{f1(120 * k)}" ry="{f1(18 * k)}" fill="none" '
            f'stroke="{P["foam"]}" stroke-width="{f1(3.5 * k)}" opacity="0.55"/>')
    return doc(S.g(body, filter="wobble-fine"))


# ============================================================================ townspeople / Jonah's rim light

# tiny Ninevites at the end of the road in front of the wall: (x, y, kind, variant, facing, waves)
TOWNSFOLK = ((2128, 978, "child", 0, 1, True), (2166, 984, "man", 0, 1, False), (2200, 990, "woman", 2, 1, False),
             (2262, 989, "child", 1, -1, True), (2296, 985, "woman", 1, -1, False), (2334, 980, "elder", 0, -1, False))
TOWN_S = 0.085


def town_svg(lit, phase):
    """Townspeople in the dusk (lit=False: dim violet silhouettes) or stepping into the warm lamp light
    (lit=True, with a soft glow behind them). phase 0/1 swaps the two children's poses (waving)."""
    people = ""
    for i, (x, y, kind, var, fc, waves) in enumerate(TOWNSFOLK):
        pose = ("cheer" if (phase + i) % 2 == 0 else "stand") if waves else "stand"
        people += C.citizen(x, y, TOWN_S, facing=fc, kind=kind, variant=var, pose=pose, expr="happy", marks=False)
    if lit:
        defs = ('<filter id="e13townlit" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
                'values="1.02 0 0 0 0.04  0 0.95 0 0 0.02  0 0 0.82 0 0  0 0 0 1 0"/></filter>')
        glow = ('<ellipse cx="2232" cy="974" rx="150" ry="42" fill="#ffd9a0" opacity="0.55" '
                'filter="url(#soft)"/>')
        return doc(glow + f'<g filter="url(#e13townlit)">{people}</g>', defs)
    defs = ('<filter id="e13towndim" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
            'values="0.22 0.06 0 0 0.2  0.04 0.2 0 0 0.15  0.05 0.05 0.26 0 0.25  0 0 0 1 0"/></filter>')
    return doc(f'<g filter="url(#e13towndim)">{people}</g>', defs)


def rim_svg(markup):
    """Warm sunset rim light on the west (sun-facing) edge of a figure: a band 3..10 px inside its left
    silhouette edge (just inside the ink line), in warm gold."""
    defs = ('<filter id="e13rim" x="-20%" y="-20%" width="140%" height="140%">'
            '<feOffset in="SourceAlpha" dx="3" dy="0" result="o1"/>'
            '<feOffset in="SourceAlpha" dx="10" dy="1" result="o2"/>'
            '<feComposite in="o1" in2="o2" operator="out" result="band"/>'
            '<feComposite in="band" in2="SourceAlpha" operator="in" result="band2"/>'
            '<feGaussianBlur in="band2" stdDeviation="1.3" result="bb"/>'
            '<feFlood flood-color="#ffd27e" result="c"/>'
            '<feComposite in="c" in2="bb" operator="in"/></filter>')
    return doc(f'<g filter="url(#e13rim)">{markup}</g>', defs)


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
    """Cubic-Bezier flight p0 -> p3 (control points c1, c2) from t0 to t1; optional landing (then 'stand').
    Non-landing doves can shrink (scale_end) and fade (alpha_end over the last 40% of the path) into the
    sunset glow."""

    def __init__(self, t0, t1, p0, c1, c2, p3, scale, land=False, phase=0.0, flap_fps=15.0, glide=(1.1, 0.7),
                 scale_end=None, alpha_end=1.0):
        self.t0, self.t1, self.p0, self.c1, self.c2, self.p3 = t0, t1, p0, c1, c2, p3
        self.scale, self.land, self.phase, self.flap_fps, self.glide = scale, land, phase, flap_fps, glide
        self.scale_end = scale if scale_end is None else scale_end
        self.alpha_end = alpha_end

    def pos(self, t):
        u = min(1.0, max(0.0, (t - self.t0) / (self.t1 - self.t0)))
        if self.land:
            u = 1 - (1 - u) ** 1.6   # slow down for the landing
        return bez3(self.p0, self.c1, self.c2, self.p3, u)

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
        a = M.lerp(1.0, self.alpha_end, M.progress(u, 0.6, 1.0, "sine"))
        return Tf(dx=x - DOVE_BASE[0], dy=y - DOVE_BASE[1] + bobv * k, sx=k, sy=k, alpha=a,
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


# tufts on the hill next to Jonah: (x, variant, scale) — each on its own layer with a rotation sway
TUFTS = ((1215, 2, 0.75), (1290, 0, 0.6), (1545, 0, 0.62), (1660, 2, 0.8), (1010, 0, 0.8), (1840, 1, 0.75),
         (860, 2, 0.9), (2050, 0, 0.9))

# great-fish leap geometry (the fish leaps out of the MID band, behind it)
LEAP_RISE, LEAP_DROP = 200, 205      # centre starts LEAP_RISE below the waterline, apex LEAP_DROP above it
LEAP_U_END = 1.16                    # keep diving past u=1 until even the tail tip is under the mid band
SNOUT = (590, 20)                    # snout tip, local fish coords at scale 1 facing right (mouth 0.12)


def leap_pose(u, xa, xb, fc):
    x = xa + (xb - xa) * u
    y = MID_WL + LEAP_RISE - (LEAP_RISE + LEAP_DROP) * 4 * u * (1 - u)
    rot = fc * (-40 + 86 * M.ease("sine")(min(1.0, max(0.0, u))))
    return x, y, rot


def leap_snout(u, xa, xb, fc):
    x, y, rot = leap_pose(u, xa, xb, fc)
    lx, ly = SNOUT[0] * FISH_S * fc, SNOUT[1] * FISH_S
    r = math.radians(rot)
    return x + lx * math.cos(r) - ly * math.sin(r), y + lx * math.sin(r) + ly * math.cos(r)


def leap_crossings(xa, xb, fc):
    """(u, x) where the snout breaks the surface going up, and where it re-enters going down."""
    out, above = [], False
    for i in range(int(LEAP_U_END * 500) + 1):
        u = i / 500
        sx, sy = leap_snout(u, xa, xb, fc)
        if not above and sy < MID_WL:
            out.append((u, sx - fc * 30))
            above = True
        elif above and sy > MID_WL:
            out.append((u, sx))
            break
    return out


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.line(0), ctx.line(1)
    d0, d1 = L0.end - L0.start, L1.end - L1.start
    t_sea = L0.start + 0.355 * d0       # "比海更宽"
    t_sky = L0.start + 0.697 * d0       # "比天更高"
    t_all = L1.start                    # "他愿意给每一个人"
    t_new = L1.start + 0.53 * d1        # "重新开始的机会"
    t_card = L1.end - 0.1               # end card (fully readable ~0.4 s later, well before the film fade-out)

    # ------------------------------------------------------------------ sky
    sc.add("sky", sky_svg(), wc=0.55)
    sc.add("dusk", dusk_svg(stars_markup(2, 8, 30)), wc=0,
           motion=M.keys([(t_sky - 0.3, {"alpha": 0}), (t_sky + 1.6, {"alpha": 0.8}), (T, {"alpha": 1.0})], "sine"))
    star_in = lambda a, b: M.keys([(a, {"alpha": 0}), (b, {"alpha": 1})], "sine")  # noqa: E731
    # three star fields with their own twinkle period / phase, so the stars do not pulse in unison
    for k, (seed, nb, ns, per, ph) in enumerate(((1, 4, 12, 1.7, 0.0), (11, 3, 11, 2.3, 0.37),
                                                  (23, 3, 11, 2.9, 0.71))):
        a = t_sky + 0.1 + 0.2 * k
        sc.add(f"stars_{k}", stars_svg(seed, nb, ns), wc=0,
               motion=M.combine(star_in(a, a + 1.2), M.pulse(0.3, 1.0, per, ph)))
    ev = (600, 560)
    sc.add("evening_star", evening_star_svg(*ev), wc=0,
           motion=M.combine(M.keys([(t_sky - 0.1, {"alpha": 0, "s": 0.2}), (t_sky + 0.45, {"alpha": 1, "s": 1.0})],
                                   "back", pivot=ev), M.pulse(0.75, 1.0, 1.4)))
    sc.add("sun", sun_svg(), motion=M.keys([(0, {"dy": 0}), (T, {"dy": 58})], "linear"))
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=7))

    # ------------------------------------------------------------------ sea: far band, fish, mid band, ship, near
    sc.add("sea_far", sea_far_svg())
    glit = [glitter_svg(s, HORIZON + 6, MID_WL) for s in (1, 2, 3)]
    sc.add("glitter_far", glit + [glit[0]], wc=0.3, frame_at=lambda t: (t * 2.6) % 3.0,
           motion=M.pulse(0.75, 1.0, 2.3))

    # the great fish: two happy leaps out past the ship ("比海更宽", and again on "重新开始的机会")
    leaps = [  # (start, duration, x_start_centre, x_end_centre, facing)
        (t_sea - 0.12, 1.35, 740, 380, -1),
        (t_new - 0.25, 1.35, 300, 650, 1),
    ]
    splash_events = []
    for i, (ls, ld, xa, xb, fc) in enumerate(leaps):
        fx0, fy0 = (xa + xb) / 2, MID_WL
        frames = [doc(PR.fish(fx0, fy0, FISH_S, facing=fc, eye="happy", mouth=0.12, tail=tv))
                  for tv in (0.65, 0.0, -0.65)]

        def fish_motion(t, ls=ls, ld=ld, xa=xa, xb=xb, fc=fc, fx0=fx0, fy0=fy0):
            u = (t - ls) / ld
            if u <= 0 or u >= LEAP_U_END:
                return Tf(alpha=0.0)
            x, y, rot = leap_pose(u, xa, xb, fc)
            return Tf(dx=x - fx0, dy=y - fy0, rot=rot, px=fx0, py=fy0)

        sc.add(f"fish{i}", frames, motion=fish_motion, seed=90 + i,
               frame_at=lambda t: float((0, 1, 2, 1)[int(t * 9) % 4]))
        for u, xs in leap_crossings(xa, xb, fc):
            splash_events.append((ls + u * ld, xs))

    sc.add("sea_mid", sea_mid_svg())
    glit_m = [glitter_svg(s, MID_WL, NEAR_WL - 6) for s in (1, 2, 3)]
    sc.add("glitter_mid", glit_m + [glit_m[0]], wc=0.3, frame_at=lambda t: (t * 2.6) % 3.0,
           motion=M.pulse(0.75, 1.0, 2.3))

    sp0 = (600, MID_WL)
    sp_svg, rp_svg = splash_svg(*sp0, k=SPLASH_K), ripple_svg(*sp0, k=SPLASH_K)
    for k, (ts, xs) in enumerate(splash_events):
        dx = xs - sp0[0]
        sc.add(f"ripple{k}", rp_svg, wc=0.4, seed=71, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.5, "sy": 0.5}), (ts + 0.05, {"alpha": 1, "sx": 0.6, "sy": 0.6}),
                    (ts + 1.6, {"alpha": 0, "sx": 1.9, "sy": 1.5})], "out", pivot=sp0),
            M.still(Tf(dx=dx))))
        sc.add(f"splash{k}", sp_svg, wc=0.4, seed=73, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.3, "sy": 0.2}), (ts + 0.02, {"alpha": 1, "sx": 0.45, "sy": 0.35}),
                    (ts + 0.28, {"alpha": 1, "sx": 1.0, "sy": 1.0}), (ts + 0.75, {"alpha": 0, "sx": 1.15, "sy": 0.7})],
                   "out", pivot=(sp0[0], sp0[1] + 8 * SPLASH_K)),
            M.still(Tf(dx=dx))))
        sc.sfx("splash_small", ts - 0.03, gain_db=-16, pan=-0.6)

    # the ship with its sailors; the middle sailor waves both arms during line 1 (stepped, no blending)
    ship_wl = MID_WL + 2

    def ship_frame(t):
        if t < t_all - 0.1 or t > t_card + 0.6:
            return 0.0
        return float((1, 2)[int((t - t_all) * 3.2) % 2])
    sc.add("ship", [ship_svg(SHIP_X, ship_wl, p) for p in WAVE_POSES], frame_at=ship_frame, motion=M.combine(
        M.drift(vx=-9),
        M.sway(1.6, 3.6, pivot=(SHIP_X, ship_wl)),
        M.bob(3, 2.9)))

    sc.add("sea_near", near_sea_svg(), motion=M.combine(M.bob(9, 6.0, axis="x"), M.bob(2.5, 3.1)))

    # ------------------------------------------------------------------ land, city, townspeople, Jonah
    sc.add("land", land_svg())
    pts = city_lights()
    sc.add("city_lights", lights_svg(pts), wc=0, motion=M.combine(
        M.keys([(0, {"alpha": 0.45}), (t_all - 0.2, {"alpha": 0.55}), (t_all + 1.0, {"alpha": 1.0})], "sine"),
        M.pulse(0.85, 1.0, 1.7)))

    t_l0, t_l1 = t_all - 0.2, t_all + 0.9

    def town_frame(t):
        p = M.progress(t, t_l0, t_l1, "sine")
        if p < 1.0:
            return p                       # dusk silhouettes -> lit (same drawing, so a crossfade is clean)
        if t > t_card + 0.6:
            return 1.0
        return float(1 + int((t - t_l1) * 2.5) % 2)   # the children wave (stepped)
    sc.add("town", [town_svg(False, 0), town_svg(True, 0), town_svg(True, 1)], wc=0.5, frame_at=town_frame)

    jy = hill_y(JONAH_X) + 4
    j_frames = [doc(C.jonah(JONAH_X, jy, JONAH_S, 1, pose="stand", expr=e)) for e in ("happy", "peaceful")]
    t_eyes_close, t_eyes_open = t_all + 0.55, t_new + 0.45
    j_breathe = M.breathe(0.012, 3.4, pivot=(JONAH_X, jy))
    sc.add("jonah", j_frames, seed=55,
           frame_at=lambda t: 1.0 if t_eyes_close <= t < t_eyes_open else 0.0,
           motion=j_breathe)
    # warm sunset rim on his west (sun) side while the golden light blooms
    sc.add("jonah_rim", rim_svg(C.jonah(JONAH_X, jy, JONAH_S, 1, pose="stand", expr="happy")), wc=0,
           motion=M.combine(j_breathe, M.keys([(t_all - 0.2, {"alpha": 0}), (t_all + 1.3, {"alpha": 0.9})], "sine")))

    for k, (x, v, s) in enumerate(TUFTS):
        by = hill_y(x) + 8
        sc.add(f"tuft{k}", doc(PR.grass_tuft(x, by, s, variant=v)),
               motion=M.sway(3.2 if v == 2 else 2.4, 3.0 + 0.3 * (k % 3), pivot=(x, by), phase=k * 0.17))

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
        # two come in high over Nineveh (above its skyline) and land beside Jonah
        DoveFlight(t_all + 0.05, t_new + 0.35, (2900, 400), (2150, 420), (1620, 640), (1530, gy(1530)), LD,
                   land=True, phase=0.1),
        DoveFlight(t_all + 0.35, t_new + 0.75, (2930, 470), (2200, 480), (1680, 680), (1612, gy(1612)), LD * 0.96,
                   land=True, phase=0.45),
        # a little flock glides on westward above the skyline and under the end card, shrinking and fading into
        # the sunset glow; end points spread out and well clear of the ship
        DoveFlight(t_all + 0.15, T + 0.15, (2920, 540), (2150, 550), (1250, 700), (420, 805), 0.85, phase=0.3,
                   scale_end=0.35, alpha_end=0.6),
        DoveFlight(t_all + 0.55, T + 0.05, (2960, 600), (2200, 610), (1300, 690), (660, 795), 0.8, phase=0.7,
                   scale_end=0.33, alpha_end=0.6),
        DoveFlight(t_all + 0.85, T + 0.2, (2940, 480), (2100, 520), (1150, 710), (250, 825), 0.85, phase=0.55,
                   scale_end=0.35, alpha_end=0.6),
    ]
    for k, fl in enumerate(flights):
        sc.add(f"dove{k}", dframes, seed=77, motion=fl.motion, frame_at=fl.frame)

    # ------------------------------------------------------------------ end card
    sc.add("card_glow", card_glow_svg(), wc=0, motion=M.keys([(t_card - 0.1, {"alpha": 0}),
                                                               (t_card + 0.5, {"alpha": 1})], "sine"))
    sc.add("card_text", card_text_svg(), wc=0, motion=M.combine(
        M.keys([(t_card, {"alpha": 0, "s": 0.95, "dy": 18}), (t_card + 0.4, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
               pivot=(CARD_X, CARD_Y - 50)),
        M.breathe(0.004, 4.0, pivot=(CARD_X, CARD_Y - 50))))
    sw0, sw1 = t_card + 0.15, t_card + 0.7
    sc.add("swash_l", swash_svg(-1), wc=0,
           reveal=lambda t: {"mode": "right", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    sc.add("swash_r", swash_svg(1), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    th = t_card + 0.3
    sc.add("heart", heart_svg(), wc=0, motion=M.combine(
        M.keys([(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back",
               pivot=HEART),
        heartbeat(th + 0.6)))

    # ------------------------------------------------------------------ camera
    # (time, centre x, viewport width, viewport bottom); interpolated with a monotone cubic so the move flows
    # through the intermediate keys. "比海更宽": widen with the top kept low (mostly horizontal growth, drifting
    # west over the sea); "比天更高": tilt up and finish the zoom so the sky grows upward; line 1: push in on
    # Jonah (eyes closing, doves landing); then ease back out so the end card has room.
    # Opening: Jonah on the left third, looking east at Nineveh. The picture comes up from the blank page
    # (PAPER_DIP fx below) rather than dissolving over s12. A plain cross-dissolve put s12's large seated Jonah
    # next to (or, with a centred framing, on top of) this small standing one: two Jonahs at once. On
    # "上帝的爱，比海更宽" the camera sweeps west past him and reaches the sea before the great fish breaks the
    # surface (the extra x-only key at t_sea keeps the leap where it was).
    t_a = t_sky - 0.07
    t_b = L0.end + 0.1
    t_c = L1.start + 0.05
    t_push = L1.start + 0.55 * d1
    t_out0 = max(t_push + 0.1, t_new + 0.3)
    t_out1 = t_card + 0.5
    x_open, b_open = 1650, 1360         # Jonah (stage x 1400) at screen x ~640, his feet at y ~747
    ck = [(0.0, x_open, 1500, b_open), (0.5, x_open, 1500, b_open), (t_a, 1250, 2080, 1600),
          (t_b, 1400, 2720, 1556), (t_c, 1400, 2720, 1556), (t_push, 1335, 2300, 1562), (t_out0, 1335, 2300, 1562),
          (t_out1, 1400, 2640, 1558), (max(T, t_out1 + 0.5), 1400, 2600, 1555)]
    cx_k = [(k[0], k[1]) for k in ck]
    cx_k.insert(2, (t_sea, 1325))       # x only: front-load the westward sweep so the leap stays in frame
    cx_f = smooth_keys(cx_k)
    cw_f = smooth_keys([(k[0], k[2]) for k in ck])
    cb_f = smooth_keys([(k[0], k[3]) for k in ck])

    def cam(t):
        w = cw_f(t)
        return Cam(cx_f(t), cb_f(t) - w * 9 / 32, w)
    sc.camera = cam

    # ------------------------------------------------------------------ fx
    sc.fx = [
        FX.sparkles((CITY_X0 + 40, CITY_Y - 230, CITY_X1 - 40, CITY_Y - 40), count=16, t0=t_all + 0.2,
                    color=(255, 236, 170), size=(6, 13), period=1.8, drift=0, seed=31),
        FX.motes((200, 380, 2600, 1250), count=34, t0=t_all - 0.2, color=(255, 236, 190), size=(2.5, 6),
                 alpha=120, seed=17),
        FX.sparkles((HEART[0] - 110, HEART[1] - 70, HEART[0] + 110, HEART[1] + 40), count=7, t0=th + 0.2,
                    color=(255, 240, 200), size=(7, 14), period=1.4, drift=0, seed=5),
        # last, so the blank page covers everything (subtitles are drawn after fx, so line 0's appears on it)
        FX.tint(PAPER_RGB, lambda t: 1.0 - M.progress(t, PAPER_DIP[0], PAPER_DIP[1], "sine")),
    ]

    # ------------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-12, fade_in=0.8, fade_out=1.6, pan=-0.3)
    sc.sfx("birds", t_all - 0.4, dur=T - t_all + 0.8, gain_db=-18, fade_in=1.0, fade_out=1.6, pan=0.2)
    sc.sfx("chime", t_card, gain_db=-8)
    return sc
