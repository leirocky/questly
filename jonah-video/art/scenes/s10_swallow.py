"""Scene 10 (v2) — Jonah sinks; the great fish God prepared swims up and swallows him (Jonah 1:17).

Underwater, tall stage (2112 x 2400): the bright underside of the sea surface (with the ship's hull drifting
away) at the top, open blue water with light shafts in the middle, reefs and the blue deep at the bottom.
The camera sinks slowly with Jonah (continuous-velocity Hermite path, < 5 output px per frame); the near
reef rocks rise into view a little faster than the rest (parallax).

  line 0  '约拿往下沉，一直往下沉。'  Jonah sinks slowly and dreamily through the light shafts, a trickle of
          bubbles rising from him; jellyfish and a little school of fish drift by.
  line 1  '可是，上帝早就为约拿安排好了一条大鱼。'  one soft warm-gold beam slants down from the surface past
          Jonah into the deep ('可是'/'上帝'), with golden glints; the great fish rises diagonally out of the
          blue at the lower left, first a dark shadow, then warming into view, clear and friendly (happy eye)
          by '大鱼'. Jonah notices it (expression cut hidden by a squash-hop).
  line 2  '大鱼游过来，张开大嘴，' the fish swims up to Jonah, spots him (eye opens) and opens its mouth wide;
          '一口就把约拿吞了下去！' it lunges and gulps him (v1 hand-off: the moving Jonah is pulled into the
          opening and replaced by a darkened copy clipped inside the closing mouth), wiggles happily, bubbles;
          on '吞了下去' a little cartoon swallow-lump slides down its belly.
  tail    the happy fish glides on; the camera eases in on it (the next scene opens inside its belly).

The camera pushes in gently while the mouth opens and eases back out with the glide. Key moments are placed
with phrase_time() (chunk + character share), never with fixed times or fixed fractions of a line.

Reuses the approved v1 underwater art / gulp mechanics from art/scenes_v1/s06_fish.py.
"""
import math
from dataclasses import replace

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s06_fish as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.scene import Scene

W, H = 2112, 2400
WL = 190                 # underside of the sea surface (the bright 'mirror' is above it)

JS = 0.8                 # Jonah's scale
JB = (1240.0, 520.0)     # Jonah's layer: bbox centre where he is drawn (motion moves him)

FSC = 0.82               # the great fish's scale
FX0, FY0 = 860.0, 1392.0  # the fish is drawn here (its pose when it waits with its mouth open)
SWALLOW_L = (405.0, 62.0)          # fish-local point Jonah ends at (inside the opening)
SWALLOW_S, SWALLOW_ROT = 0.5, -26.0  # his scale factor and on-screen rotation there

NEAR_K = 0.30            # near rocks move this fraction against it (they rise faster into view)

UW_DEFS = V.UW_DEFS      # s6uwt (underwater tint), s6uwd (inside the mouth), s6halo


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


PUNCT = set("，。！？、；：,.!?;:…“”‘’\"' ")


def phrase_time(line, phrase):
    """When the narrator reaches ``phrase``: the start of the subtitle chunk that contains it plus the phrase's
    share of that chunk by character offset (punctuation not counted). Falls back to the whole line when no
    chunk has it, so a re-generated voice with different chunking still gives a sensible time."""
    for c in line.chunks:
        if phrase in c.text:
            txt, t0, t1 = c.text, c.start, c.end
            break
    else:
        txt, t0, t1 = line.text, line.start, line.end
    i = txt.index(phrase)
    n = sum(ch not in PUNCT for ch in txt)
    k = sum(ch not in PUNCT for ch in txt[:i])
    return t0 + (t1 - t0) * k / max(1, n)


def hermite(keys):
    """Smooth path through (t, value, slope) keys with continuous velocity (cubic Hermite)."""
    keys = sorted(keys)

    def f(t):
        if t <= keys[0][0]:
            t0, v0, s0 = keys[0]
            return v0 + s0 * (t - t0)
        if t >= keys[-1][0]:
            t1, v1, s1 = keys[-1]
            return v1 + s1 * (t - t1)
        for (t0, v0, s0), (t1, v1, s1) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                h = t1 - t0
                u = (t - t0) / h
                h00 = 2 * u ** 3 - 3 * u ** 2 + 1
                h10 = u ** 3 - 2 * u ** 2 + u
                h01 = -2 * u ** 3 + 3 * u ** 2
                h11 = u ** 3 - u ** 2
                return h00 * v0 + h10 * h * s0 + h01 * v1 + h11 * h * s1
        return keys[-1][1]
    return f


# ============================================================================ static painting


def far_plane():
    """Water gradient, the blue deep, hazy far reefs and kelp, a far school of fish (parallax layer)."""
    defs = (
        S.lin_grad("s10uw", [(0, "#78c3cd"), (0.08, "#62b4c7"), (0.25, "#4a9cb8"), (0.45, "#3887a9"),
                             (0.65, "#2c7398"), (0.82, "#235f86"), (1, "#1b4f73")]) +
        S.rad_grad("s10abyss", [(0, "#163f5c", 0.75), (0.6, "#183f5c", 0.35), (1, "#183f5c", 0)]) +
        S.lin_grad("s10haze", [(0, "#2f7898", 0), (1, "#25668a", 0.5)])
    )
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#s10uw)"/>'
    # the blue deep the fish comes from (lower left)
    b += '<ellipse cx="560" cy="2330" rx="1100" ry="560" fill="url(#s10abyss)"/>'
    # far reefs (light, hazy), both sides of the deep
    far_rock = S.mix("#2f7898", "#9fd0d6", 0.28)
    b += S.g(
        S.path(S.smooth_path([(-60, H + 40), (-50, 1760), (40, 1650), (170, 1610), (280, 1680), (360, 1820),
                              (450, 2020), (520, 2260), (560, H + 40)], closed=True), fill=far_rock, sw=3) +
        S.path(S.smooth_path([(1560, H + 40), (1620, 2160), (1700, 1940), (1800, 1760), (1920, 1640),
                              (2050, 1590), (2180, 1620), (2190, H + 40)], closed=True), fill=far_rock, sw=3),
        filter="wobble", opacity=0.85)
    tex = ""
    crev = S.mix("#2f7898", "#1f5776", 0.45)
    for pts in ([(70, 1710), (120, 1780), (105, 1870)], [(230, 1700), (262, 1790), (330, 1840)],
                [(90, 2020), (170, 2080), (190, 2190)], [(340, 1960), (390, 2050), (450, 2100)],
                [(1980, 1680), (1940, 1770), (1960, 1870)], [(2080, 1660), (2050, 1760), (2090, 1830)],
                [(1800, 1980), (1860, 2050), (1850, 2160)], [(2010, 1950), (1980, 2040)]):
        tex += S.path(S.smooth_path(pts, closed=False), stroke=False,
                      extra=f'stroke="{crev}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.5"')
    for cx, cy, rx, ry in ((150, 1650, 110, 26), (2040, 1620, 120, 26), (310, 1730, 60, 16), (1880, 1760, 70, 18)):
        tex += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#a9d8d8" opacity="0.3"/>'
    b += S.g(tex, filter="wobble")
    back_weed = (PR.seaweed(150, 1650, 0.75, 0) + PR.seaweed(262, 1668, 0.6, 2) + PR.seaweed(1990, 1595, 0.8, 0) +
                 PR.seaweed(1890, 1690, 0.6, 3) + PR.seaweed(440, 1920, 0.55, 1) + PR.seaweed(1740, 1900, 0.6, 2))
    b += S.g(back_weed, opacity=0.6)
    # far kelp forest silhouettes in the blue distance
    kelp = ""
    for i, (x, h, lean) in enumerate([(600, 560, 30), (690, 420, -20), (1500, 460, -25), (1600, 600, 20),
                                      (1690, 430, -15), (1080, 300, 15), (1290, 360, -20), (880, 340, 22)]):
        y0 = H + 40
        pts = [(x + lean * math.sin(k / 5 * math.pi * 1.3) * (k / 5), y0 - h * k / 5) for k in range(6)]
        kelp += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="#3a7f9c" stroke-width="{22 - i % 3 * 4}" fill="none" stroke-linecap="round" '
                             f'opacity="0.5"')
        for k in range(1, 5):
            px, py = pts[k]
            side = 1 if k % 2 else -1
            kelp += (f'<ellipse cx="{px + side * 22:.0f}" cy="{py:.0f}" rx="26" ry="10" fill="#3a7f9c" '
                     f'opacity="0.5" transform="rotate({side * -30} {px + side * 22:.0f} {py:.0f})"/>')
    b += S.g(kelp, filter="wobble")
    b += f'<rect x="-20" y="1500" width="{W + 40}" height="{H - 1500 + 20}" fill="url(#s10haze)"/>'
    return doc(b, defs)


def far_school():
    """A far school of tiny fish (hazy silhouettes) in the open water — its own small drifting layer."""
    school = ""
    rng = np.random.default_rng(4)
    for i in range(16):
        a = 2 * math.pi * i / 16
        x = 330 + 150 * math.cos(a) + rng.uniform(-30, 30)
        y = 1020 + 60 * math.sin(a) + rng.uniform(-14, 14)
        school += (f'<path d="M{x - 14:.0f},{y:.0f} q14,-9 28,0 q-14,9 -28,0 Z M{x - 13:.0f},{y:.0f} l-9,-6 l0,12 Z" '
                   f'fill="#5aa3bb" opacity="0.6"/>')
    return doc(school)


def surface_glow():
    """The soft bright glow just below the sea surface (static background)."""
    defs = S.lin_grad("s10glow", [(0, "#e8f7ee", 0.55), (0.4, "#d0efe8", 0.18), (1, "#d0efe8", 0)])
    return doc(f'<rect x="-20" y="{WL - 30}" width="{W + 40}" height="360" fill="url(#s10glow)"/>', defs)


def surface():
    """The bright underside of the sea surface (a wavy 'mirror' ceiling). It sits ABOVE the ship layer, so the
    hull's straight clip edge is always tucked under the wavy, inked waterline (also while the hull bobs)."""
    defs = S.lin_grad("s10mir", [(0, "#eef8ec"), (0.55, "#d3efe6"), (1, "#a8dcdc")])
    b = ""
    # mirror: filled above a wavy line
    pts = []
    x = -60
    while x <= W + 120:
        pts.append((x, WL + 9 * math.sin(2 * math.pi * x / 260) + 4 * math.sin(2 * math.pi * x / 97 + 1)))
        x += 30
    d = S.smooth_path(pts, closed=False) + f" L{W + 120},-30 L-60,-30 Z"
    b += S.path(d, fill="url(#s10mir)", stroke=False)
    b += S.g(S.path(S.smooth_path(pts, closed=False), sw=3.5, extra='opacity="0.55"'), filter="wobble")
    # wave undersides (soft teal streaks) and bright glints in the mirror
    streak = ""
    for i, (y, a, lam, ph, dash) in enumerate([(40, 7, 210, 0.3, "120 80"), (88, 8, 250, 1.6, "160 70"),
                                               (132, 9, 300, 2.4, "200 90"), (166, 6, 230, 0.9, "90 140")]):
        streak += S.path(S.wave_line(y, a, lam, ph), stroke=False,
                         extra=f'stroke="#8fcfd2" stroke-width="{5 + i}" fill="none" opacity="0.6" '
                               f'stroke-dasharray="{dash}" stroke-linecap="round"')
    for x, y, w in [(140, 60, 90), (520, 28, 120), (900, 110, 70), (1300, 50, 110), (1700, 96, 90),
                    (1980, 40, 80), (330, 150, 60), (1130, 160, 80), (1560, 150, 60)]:
        streak += (f'<path d="M{x},{y} q{w / 2:.0f},-10 {w},0" stroke="#fffcf0" stroke-width="5" fill="none" '
                   f'stroke-linecap="round" opacity="0.75"/>')
    b += S.g(streak, filter="wobble")
    return doc(b, defs)


def ripple_lights():
    """Rippling light lines just under the surface (drift sideways)."""
    b = ""
    for i in range(7):
        y = WL + 40 + i * 38
        b += S.path(S.wave_line(y, 6, 170 + 20 * i, i * 1.3, x0=-140 + (i % 2) * 90, x1=W + 140), stroke=False,
                    extra=f'stroke="#d8f3ee" stroke-width="{5.5 - i * 0.55:.1f}" fill="none" '
                          f'opacity="{0.42 - i * 0.045:.2f}" stroke-dasharray="{90 + 15 * i} {60 + 25 * i}"')
    return doc(S.g(b, filter="wobble"))


def shafts(set_):
    defs = S.lin_grad(f"s10sh{set_}", [(0, "#f6fbe4", 0.05), (0.1, "#f6fbe4", 0.42), (0.5, "#d8f3ec", 0.16),
                                        (1, "#d8f3ec", 0)])
    # set 0: static beams (flattened with the background); set 1: two shimmering beams over Jonah's path
    beams = ([(1180, 100, -260, 1500), (1640, 80, -300, 1350), (520, 70, -200, 1200), (2010, 120, -380, 1700),
              (860, 70, -230, 1250), (1840, 90, -330, 1500), (260, 60, -170, 1000)]
             if set_ == 0 else
             [(1400, 150, -300, 1700), (1600, 60, -330, 1550)])
    b = ""
    for x, w, lean, ln in beams:
        y0 = WL - 6
        b += (f'<path d="M{x},{y0} L{x + w},{y0} L{x + w + lean},{y0 + ln} L{x + lean - w * 0.6},{y0 + ln} Z" '
              f'fill="url(#s10sh{set_})"/>')
    return doc(S.g(b, filter="soft"), defs)


SHIP_X, SHIP_S = 640, 0.8


def _hull_top(x):      # the same hull curves as props._ship (ship-local, scale 1, facing right)
    return -165 - 75 * (abs(x) / 480) ** 3.2


def _hull_bot(x):
    return 96 - 250 * (abs(x) / 490) ** 3.5


def hull_underside():
    """Planks of the hull's underside seen from below (ship-local markup, placed like props.ship): wet light
    near the waterline darkening toward the keel, curved plank seams, a dark keel strip, two weed tufts."""
    xs = [-480 + i * 20 for i in range(49)]
    pts = [(x, _hull_top(x)) for x in xs] + [(503, -196), (494, -136), (466, -72), (418, -14), (340, 40), (200, 80),
                                            (0, 96), (-200, 82), (-350, 42), (-430, -14), (-478, -80),
                                            (-500, -146), (-505, -204)]
    hull_d = S.smooth_path(pts, closed=True, tension=0.5)
    wd = P["wood_dark"]
    lit = S.mix(P["wood_light"], "#9fd6d6", 0.3)
    deep = S.mix(S.shade(wd, -0.3), P["sea_deep"], 0.12)
    defs = ('<linearGradient id="s10hullg" gradientUnits="userSpaceOnUse" x1="0" y1="-60" x2="0" y2="100">'
            f'<stop offset="0" stop-color="{lit}"/><stop offset="0.35" stop-color="{S.mix(P["wood"], lit, 0.25)}"/>'
            f'<stop offset="0.75" stop-color="{S.mix(wd, P["wood"], 0.3)}"/><stop offset="1" stop-color="{deep}"/>'
            '</linearGradient>'
            f'<clipPath id="s10hullc"><path d="{hull_d}"/></clipPath>')
    inner = '<rect x="-560" y="-70" width="1120" height="200" fill="url(#s10hullg)"/>'
    # curved plank seams following the keel line
    for k in (0.3, 0.52, 0.72):
        sp = [(x, -40 + (_hull_bot(x) + 40) * k) for x in range(-480, 481, 30)]
        inner += S.path(S.smooth_path(sp, closed=False), stroke=False,
                        extra=f'stroke="{S.shade(wd, -0.2)}" stroke-width="4" fill="none" stroke-linecap="round" '
                              f'opacity="0.75"')
        hl = [(x, y + 5) for x, y in sp]
        inner += S.path(S.smooth_path(hl, closed=False), stroke=False,
                        extra=f'stroke="{S.shade(lit, 0.3)}" stroke-width="3" fill="none" stroke-linecap="round" '
                              f'opacity="0.35"')
    # plank butt joints and trenails
    rng = np.random.default_rng(8)
    for k0, k1 in ((0.3, 0.52), (0.52, 0.72)):
        for x in rng.uniform(-330, 330, 4):
            y0, y1 = -40 + (_hull_bot(x) + 40) * k0, -40 + (_hull_bot(x) + 40) * k1
            inner += (f'<path d="M{x:.0f},{y0 + 3:.0f} L{x + 3:.0f},{y1 - 3:.0f}" stroke="{S.shade(wd, -0.2)}" '
                      f'stroke-width="3.5" opacity="0.6"/>')
    for x in range(-300, 320, 75):
        y = -40 + (_hull_bot(x) + 40) * 0.62
        inner += f'<circle cx="{x}" cy="{y:.0f}" r="3.2" fill="{S.shade(wd, -0.3)}" opacity="0.7"/>'
    # keel strip along the bottom
    keel = [(x, _hull_bot(x) - 7) for x in range(-380, 381, 20)]
    inner += S.path(S.smooth_path(keel, closed=False), stroke=False,
                    extra=f'stroke="{S.shade(wd, -0.3)}" stroke-width="18" fill="none" stroke-linecap="round"')
    # rippled light caught on the planks just under the waterline
    inner += ('<path d="M-360,8 Q-180,22 0,14 Q180,6 360,16" stroke="#e9f7ef" stroke-width="10" fill="none" '
              'stroke-linecap="round" opacity="0.28" filter="url(#soft)"/>')
    b = f'<g clip-path="url(#s10hullc)">{inner}</g>' + S.path(hull_d, sw=4.5)
    # two little weed tufts trailing from the keel
    weed = S.mix(P["leaf_dark"], "#3a7f9c", 0.35)
    for x0, lens in ((-150, (58, 40, 70)), (210, (44, 30))):
        y0 = _hull_bot(x0) - 4
        for k, ln in enumerate(lens):
            wp = [(x0 + 9 * k - ln * 0.35 * (j / 5) ** 1.5 + 5 * math.sin(j * 1.25 + 2 * k), y0 + ln * j / 5)
                  for j in range(6)]
            b += S.path(S.smooth_path(wp, closed=False), stroke=False,
                        extra=f'stroke="{weed}" stroke-width="{7 - k}" fill="none" stroke-linecap="round" '
                              f'opacity="0.8"')
    return defs, f'<g transform="translate({SHIP_X},{WL}) scale({-SHIP_S},{SHIP_S})">{b}</g>'


def ship_hull():
    """The ship's hull seen from below (bow left, sailing on west), veiled by the water. Clipped well above the
    waterline: the static mirror layer above it hides the cut behind the wavy, inked surface line."""
    clip = f'<clipPath id="s10below"><rect x="-20" y="{WL - 40}" width="{W + 40}" height="400"/></clipPath>'
    veil = ('<filter id="s10veil"><feColorMatrix type="matrix" values="0 0 0 0 0.42  0 0 0 0 0.72  0 0 0 0 0.78  '
            '0 0 0 1 0"/></filter>')
    hdefs, under = hull_underside()
    ship = (PR.ship(SHIP_X, WL, SHIP_S, -1, sail="torn", part="back") + S.g(under, filter="wobble-fine") +
            PR.ship(SHIP_X, WL, SHIP_S, -1, sail="torn", part="front"))
    b = (f'<g clip-path="url(#s10below)">{ship}'
         f'<g filter="url(#s10veil)" opacity="0.2">{ship}</g></g>')
    # soft light glinting along the wet keel
    b += (f'<path d="M{SHIP_X - 300},{WL + 40} Q{SHIP_X},{WL + 78} {SHIP_X + 330},{WL + 34}" stroke="#d9f2ee" '
          f'stroke-width="6" fill="none" stroke-linecap="round" opacity="0.35" filter="url(#soft)"/>')
    return doc(b, clip + veil + hdefs)


def jelly(x, y, s, col, seed=0):
    """A small friendly jellyfish: translucent bell with a frilly rim, a sleepy smile and wavy tentacles."""
    rng = np.random.default_rng(seed)
    ink = P["ink"]
    tent = ""
    for i in range(5):
        tx = x + (-34 + 17 * i) * s
        L = (90 + rng.uniform(-10, 30)) * s
        pts = [(tx + 9 * s * math.sin(k * 1.4 + i), y + 12 * s + L * k / 4) for k in range(5)]
        tent += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="{S.shade(col, -0.15)}" stroke-width="{4.5 * s:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.8"')
    # two frilly oral arms
    for dx in (-10, 10):
        pts = [(x + dx * s + 12 * s * math.sin(k * 1.1 + dx), y + 10 * s + 18 * s * k) for k in range(5)]
        tent += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="{S.shade(col, 0.25)}" stroke-width="{11 * s:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.85"')
    bell = (f"M{x - 56 * s:.1f},{y + 12 * s:.1f} C{x - 60 * s:.1f},{y - 50 * s:.1f} {x - 30 * s:.1f},{y - 74 * s:.1f} "
            f"{x:.1f},{y - 74 * s:.1f} C{x + 30 * s:.1f},{y - 74 * s:.1f} {x + 60 * s:.1f},{y - 50 * s:.1f} "
            f"{x + 56 * s:.1f},{y + 12 * s:.1f} ")
    for i in range(7):    # scalloped rim, right to left
        x1 = x + 56 * s - (i + 1) * 16 * s
        bell += f"Q{x1 + 8 * s:.1f},{y + 22 * s:.1f} {x1:.1f},{y + 12 * s:.1f} "
    bell += "Z"
    body = tent + S.path(bell, fill=col, sw=3.5 * s, extra='fill-opacity="0.9"')
    body += (f'<path d="M{x - 36 * s:.1f},{y - 30 * s:.1f} Q{x - 30 * s:.1f},{y - 58 * s:.1f} {x - 6 * s:.1f},'
             f'{y - 62 * s:.1f}" stroke="#fff6f0" stroke-width="{7 * s:.1f}" fill="none" stroke-linecap="round" '
             f'opacity="0.7"/>')
    # sleepy happy face
    for ex in (-16, 16):
        body += (f'<path d="M{x + ex * s - 7 * s:.1f},{y - 16 * s:.1f} q{7 * s:.1f},-7 {14 * s:.1f},0" stroke="{ink}" '
                 f'stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>')
    body += (f'<path d="M{x - 6 * s:.1f},{y - 4 * s:.1f} q{6 * s:.1f},{6 * s:.1f} {12 * s:.1f},0" stroke="{ink}" '
             f'stroke-width="{3 * s:.1f}" fill="none" stroke-linecap="round"/>')
    for ex in (-30, 30):
        body += f'<ellipse cx="{x + ex * s:.1f}" cy="{y - 6 * s:.1f}" rx="{8 * s:.1f}" ry="{5 * s:.1f}" fill="{P["cheek"]}" opacity="0.7"/>'
    return S.g(body, filter="wobble-fine")


def near_rocks():
    """Foreground reef rocks framing the bottom corners (near plane, parallax), with corals and anemones."""
    rock = S.mix("#24607c", P["stone_dark"], 0.22)
    b = S.g(
        S.path(S.smooth_path([(-80, H + 60), (-70, 1830), (30, 1760), (170, 1735), (300, 1790), (380, 1900),
                              (430, 2060), (470, H + 60)], closed=True), fill=rock, sw=5) +
        S.path(S.smooth_path([(1700, H + 60), (1740, 1990), (1830, 1860), (1960, 1800), (2090, 1810),
                              (2200, 1850), (2210, H + 60)], closed=True), fill=rock, sw=5), filter="wobble")
    rt = ""
    for pts in ([(60, 1820), (110, 1880), (100, 1960)], [(250, 1800), (290, 1870)], [(1850, 1900), (1900, 1980)],
                [(2050, 1840), (2020, 1920), (2060, 1990)], [(160, 1950), (230, 2010)]):
        rt += S.path(S.smooth_path(pts, closed=False), stroke=False,
                     extra=f'stroke="{S.shade(rock, -0.25)}" stroke-width="7" fill="none" stroke-linecap="round" '
                           f'opacity="0.6"')
    rt += '<ellipse cx="160" cy="1752" rx="100" ry="15" fill="#9fd0d6" opacity="0.32"/>'
    rt += '<ellipse cx="1980" cy="1818" rx="100" ry="15" fill="#9fd0d6" opacity="0.32"/>'
    b += S.g(rt, filter="wobble")
    b += V._anemone(300, 1792, 1.1, "#e9877f") + V._anemone(1900, 1830, 1.0, "#f0a65a")
    b += V._anemone(110, 1765, 0.8, "#d98bc0")
    b += PR.seaweed(2040, 1812, 0.75, 3) + PR.seaweed(200, 1745, 0.7, 1)
    b += V._starfish(1820, 1925, 26, "#e7926f", rot=12) + V._shell(380, 1905, 18)
    return doc(b)


# ============================================================================ characters


def jonah_markup(facing, expr, filt="s6uwt", c=JB, s=1.0, rot=0.0):
    ax, ay = c[0] - facing * 1.5 * JS * s, c[1] + 165 * JS * s
    tr = f' transform="rotate({rot:.2f} {c[0]:.1f} {c[1]:.1f})"' if rot else ""
    return f'<g filter="url(#{filt})"{tr}>{C.jonah(ax, ay, JS * s, facing, pose="float", expr=expr)}</g>'


def fish_silhouette(e, tl):
    """The fish filled flat with deep-water colour (overlay that fades as it rises out of the deep)."""
    # deep-water blue (sRGB #17425f), darker than the surrounding water: a shadow rising from the deep
    flt = ('<filter id="s10silh" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" '
           'values="0 0 0 0 0.09  0 0 0 0 0.26  0 0 0 0 0.37  0 0 0 1 0"/></filter>')
    return doc(f'<g filter="url(#s10silh)">{PR.fish(FX0, FY0, FSC, 1, mouth=0.0, eye=e, tail=tl)}</g>', flt)


def fish_glow():
    defs = S.rad_grad("s10fglow", [(0, "#fff0c0", 0.55), (0.45, "#ffe8a8", 0.22), (1, "#ffe8a8", 0)])
    return doc(f'<ellipse cx="{FX0 + 60}" cy="{FY0 - 40}" rx="640" ry="440" fill="url(#s10fglow)"/>', defs)


BEAM_TOP, BEAM_BOT = (1700.0, WL - 20.0), (470.0, 1600.0)   # God's light: from the surface down to the deep


def gold_beam():
    """God's providence as light (never a figure): one soft warm-gold beam slanting from the surface down past
    Jonah to where the great fish rises, with a warm pool of light where it lands."""
    (x0, y0), (x1, y1) = BEAM_TOP, BEAM_BOT
    ln = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / ln, (x1 - x0) / ln

    def quad(w0, w1):
        p = [(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1),
             (x0 - nx * w0, y0 - ny * w0)]
        return "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in p) + " Z"

    def grad(gid, col, stops):
        s_ = "".join(f'<stop offset="{o}" stop-color="{col}" stop-opacity="{a}"/>' for o, a in stops)
        return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" '
                f'x2="{x1:.0f}" y2="{y1:.0f}">{s_}</linearGradient>')

    defs = (grad("s10bo", "#ffb040", [(0, 0.0), (0.1, 0.34), (0.7, 0.3), (1, 0.0)]) +
            grad("s10bc", "#ffd880", [(0, 0.0), (0.08, 0.62), (0.65, 0.44), (1, 0.0)]) +
            S.rad_grad("s10bpool", [(0, "#ffd77a", 0.4), (0.5, "#ffd77a", 0.16), (1, "#ffd77a", 0)]) +
            '<filter id="s10bblur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="26"/>'
            '</filter><filter id="s10bblur2" x="-30%" y="-30%" width="160%" height="160%">'
            '<feGaussianBlur stdDeviation="10"/></filter>')
    b = (f'<path d="{quad(120, 330)}" fill="url(#s10bo)" filter="url(#s10bblur)"/>'
         f'<path d="{quad(36, 120)}" fill="url(#s10bc)" filter="url(#s10bblur2)"/>'
         f'<ellipse cx="{x1 + 120:.0f}" cy="{y1 - 120:.0f}" rx="520" ry="300" fill="url(#s10bpool)"/>')
    return doc(b, defs)


BELLY = ([-292.0, -110.0, 60.0, 178.0], [232.0, 292.0, 306.0, 297.0])   # fish-local belly contour (props._fish)
LUMP_X0, LUMP_X1 = 120.0, -125.0      # the swallow-lump slides from behind the gill to the middle of the belly
LUMP_A, LUMP_H = 80.0, 44.0           # its half-width and depth (fish-local px)


def belly_y(x):
    return float(np.interp(x, *BELLY))


def lump_pivot():
    return FX0 + LUMP_X0 * FSC, FY0 + belly_y(LUMP_X0) * FSC


def belly_slope(x):
    """Tilt (deg) of the belly contour under a lump centred at x."""
    return math.degrees(math.atan2(belly_y(x + LUMP_A) - belly_y(x - LUMP_A), 2 * LUMP_A))


def swallow_lump():
    """A little cartoon swallow-lump bulging out of the fish's belly (fish-local markup at LUMP_X0, placed like
    the fish). Its top edge sits on the belly contour, so scaling it vertically about lump_pivot() grows it."""
    xc, a, h = LUMP_X0, LUMP_A, LUMP_H
    yc = belly_y(xc)
    pl, pr = (xc - a, belly_y(xc - a)), (xc + a, belly_y(xc + a))
    arc = [pl, (xc - 0.72 * a, yc + 0.7 * h), (xc - 0.3 * a, yc + 0.97 * h), (xc + 0.3 * a, yc + 0.97 * h),
           (xc + 0.72 * a, yc + 0.7 * h), pr]
    inside = [(xc + 0.8 * a, yc - 16), (xc, yc - 22), (xc - 0.8 * a, yc - 16)]
    belly = P["fish_belly"]
    body = S.path(S.smooth_path(arc + inside, closed=True), fill=belly, stroke=False)
    body += (f'<ellipse cx="{xc - 10:.0f}" cy="{yc + 10:.0f}" rx="46" ry="14" fill="{S.shade(belly, 0.55)}" '
             f'opacity="0.8"/>')
    body += S.path(S.smooth_path(arc, closed=False), sw=4.5)
    return doc(S.g(f'<g transform="translate({FX0},{FY0}) scale({FSC})">{body}</g>', filter="wobble-fine"))


# ============================================================================ effects


def bubble_fx(sources, seed=3, top=WL + 16):
    """All bubbles in one fx (v1 recipe). sources: (emitter(t)->(x, y), t0, t1, rate, rise, size, spread, alpha)."""
    rng = np.random.default_rng(seed)
    parts = []
    for src, t0, t1, rate, rise, size, spread, alpha in sources:
        n = max(1, int((t1 - t0) * rate))
        ts = t0 + (np.arange(n) + rng.uniform(0, 1, n)) / rate
        for i in range(n):
            ex, ey = src(ts[i])
            parts.append((ts[i], ex + rng.uniform(-spread, spread), ey + rng.uniform(-spread, spread) * 0.5,
                          rng.uniform(*size), rise * rng.uniform(0.7, 1.3), rng.uniform(0, 6.3), alpha))
    arr = np.array(parts, np.float64)

    def fx(frame, t, view):
        live = arr[(arr[:, 0] <= t) & (arr[:, 0] > t - 7)]
        if not len(live):
            return frame
        pts = []
        for ts, x, y, r, sp, ph, al in live:
            age = t - ts
            yy = y - sp * age - 22 * age * age
            if yy < top:
                continue
            xx = x + 10 * math.sin(age * 4.5 + ph) * min(1, age * 2)
            fade = min(1.0, age / 0.12, (yy - top) / 60)
            ox, oy = view.to_out(xx, yy)
            rr = r * view.scale * (0.55 + 0.45 * min(1.0, age / 0.4))
            if -40 < ox < frame.size[0] + 40 and -40 < oy < frame.size[1] + 40:
                pts.append((ox, oy, rr, int(al * fade)))
        if not pts:
            return frame
        x0 = int(max(0, min(p[0] - p[2] for p in pts) - 4))
        y0 = int(max(0, min(p[1] - p[2] for p in pts) - 4))
        x1 = int(min(frame.size[0], max(p[0] + p[2] for p in pts) + 4))
        y1 = int(min(frame.size[1], max(p[1] + p[2] for p in pts) + 4))
        if x1 <= x0 or y1 <= y0:
            return frame
        ov = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ox, oy, r, a in pts:
            ox, oy = ox - x0, oy - y0
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(215, 240, 245, a // 5),
                      outline=(236, 250, 250, a), width=max(2, int(r / 5)))
            d.ellipse([ox - r * 0.5, oy - r * 0.6, ox - r * 0.12, oy - r * 0.22], fill=(255, 255, 250, a))
        frame.alpha_composite(ov, dest=(x0, y0))
        return frame
    return fx


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[0], ctx.lines[1], ctx.lines[2]

    # ---- timing (all from the narration; phrases placed by chunk + character share, order clamped)
    t_glint = L1.start + 0.1                       # '可是' — God's warm light begins
    t_god = phrase_time(L1, "上帝")
    t_f0 = t_god - 0.3                             # the fish rises out of the deep
    t_f1 = L1.end - 0.1                            # ...fully revealed by '一条大鱼'
    t_haze0, t_haze1 = t_f0 + 0.9, L1.end - 0.5
    t_notice = L1.end - 0.9                        # Jonah notices the fish (expression cut)
    t_swim0 = L2.start                             # '大鱼游过来' — swims up to him
    t_spot = t_swim0 - 0.05                        # the fish spots Jonah (happy eye -> open eye)
    t_open0 = max(phrase_time(L2, "张开大嘴") - 0.1, t_swim0 + 0.6)
    t_open1 = t_open0 + 0.85
    t_swim1 = t_open1 - 0.1
    t_surge0 = max(phrase_time(L2, "一口") + 0.08, t_open1 + 0.3)
    t_surge1 = t_surge0 + 0.28
    t_close0, t_close1 = t_surge1, t_surge1 + 0.18
    t_tun = max(phrase_time(L2, "吞了下去"), t_close1 + 0.45)   # the swallow-lump slides down the belly
    LUMP_DUR = 0.55

    def bump(t, ts, w=0.07):
        return max(0.0, 1 - abs(t - ts - 0.03) / w)

    # ---- camera: sinks with Jonah (continuous velocity) and a little ahead of him, so the deep below is in
    # view when the fish rises; pushes in gently while the mouth opens; eases back out with the glide
    cam_y = hermite([(0.0, 520, 62), (4.2, 805, 95), (6.4, 1040, 100), (9.0, 1285, 56), (t_open0 - 0.4, 1348, 14),
                     (t_surge0, 1352, 0), (T, 1420, 10)])
    cam_w = hermite([(0.0, 1720, 0), (4.2, 1785, 45), (6.4, 1930, 50), (9.0, 2040, 0), (t_open0 - 0.4, 2010, -35),
                     (t_surge0, 1815, 0), (t_close1 + 1.4, 1910, 24), (T, 1890, -12)])
    cam_x = hermite([(0.0, 1060, 0), (9.0, 1056, 0), (t_open0 - 0.4, 1072, 28), (t_surge0, 1150, 0),
                     (t_close1 + 1.4, 1115, -10), (T, 1100, 0)])

    def camera(t):
        return Cam(cam_x(t), cam_y(t), cam_w(t))
    sc.camera = camera
    cy1 = cam_y(T)

    # ---------------------------------------------------------------- far / mid planes
    # far plane, surface glow and the steady light shafts are static: they flatten into one background item
    sc.add("far", far_plane(), z=0, wc=0.8)
    sc.add("glow", surface_glow(), z=1, wc=0)
    sc.add("shafts_a", shafts(0), z=1.5, wc=0)
    sc.add("far_school", far_school(), z=1.7, wc=0.6,
           motion=M.combine(M.drift(vx=10, vy=-2), M.bob(6, 3.7), M.bob(4, 5.3, 0.3, axis="x")))
    sc.add("ripples", ripple_lights(), z=2, wc=0,
           motion=lambda t: Tf(dx=34 * math.sin(2 * math.pi * t / 3.1), alpha=0.8 + 0.2 * math.sin(t * 1.7)))
    sc.add("ship", ship_hull(), z=3, wc=0.7,
           motion=lambda t: Tf(dx=-16 * t, dy=3 * math.sin(2 * math.pi * t / 2.8), rot=0.6 * math.sin(2 * math.pi * t / 3.6),
                               px=SHIP_X, py=WL))
    # the bright surface 'mirror' over the hull: its wavy inked edge hides the hull's clip line
    sc.add("surface", surface(), z=3.5, wc=0.6)
    sc.add("shafts_b", shafts(1), z=5, wc=0,
           motion=lambda t: Tf(dx=-14 * math.sin(2 * math.pi * t / 7.0),
                               alpha=0.6 + 0.4 * math.sin(2 * math.pi * t / 4.6 + 2.0)))

    # God's providence: one warm-gold beam from the surface down past Jonah to where the fish rises
    def beam_a(t):
        return (progress(t, L1.start, t_god + 0.8, "sine") * (1 - progress(t, t_open0 - 1.0, t_open0, "sine"))
                * (0.88 + 0.12 * math.sin(2 * math.pi * t / 2.3)))
    sc.add("beam", gold_beam(), z=5.5, wc=0,
           motion=lambda t: Tf(rot=0.5 * math.sin(2 * math.pi * t / 6.5), alpha=beam_a(t), px=BEAM_TOP[0],
                               py=BEAM_TOP[1]))

    # jellyfish drifting up gently, pulsing (squash on each push). One wrapped counter for the pulse, so the
    # rise is continuous (no jump when the phase wraps).
    def jelly_m(x, y, period, phase, rise):
        def m(t):
            v = t / period + phase
            n = math.floor(v)
            u = v - n
            push = math.sin(math.pi * min(1.0, u / 0.35)) if u < 0.35 else 0.0
            return Tf(dx=8 * math.sin(t * 0.7 + phase * 6), dy=-rise * t - 10 * (n + min(1.0, u / 0.35)),
                      sx=1 + 0.07 * push, sy=1 - 0.09 * push, px=x, py=y)
        return m

    sc.add("jelly1", doc(jelly(470, 560, 1.0, "#f0a8c0", seed=1)), z=6, motion=jelly_m(470, 560, 2.4, 0.0, 9))
    sc.add("jelly2", doc(jelly(640, 700, 0.7, "#c8a8e8", seed=2)), z=6.1, motion=jelly_m(640, 700, 2.0, 0.4, 7))
    sc.add("jelly3", doc(jelly(1760, 900, 0.8, "#f4b8a0", seed=3)), z=6.2, motion=jelly_m(1760, 900, 2.6, 0.7, 6))

    # little fish: a school in the open water (darts away when the great fish rises), another near the reef
    t_dart = t_f0 + 1.6
    school_a = [doc(PR.small_fish(470, 930, 0.7, 1, "yellow", tail=tl) +
                    PR.small_fish(390, 985, 0.6, 1, "orange", tail=-tl) +
                    PR.small_fish(540, 1010, 0.65, 1, "yellow", tail=-tl) +
                    PR.small_fish(320, 920, 0.55, 1, "orange", tail=tl)) for tl in (0.7, -0.7)]
    sc.add("school_a", school_a, z=7,
           motion=M.combine(lambda t: Tf(dx=42 * t + 1100 * progress(t, t_dart, t_dart + 1.6, "in"),
                                         dy=-30 * t - 160 * progress(t, t_dart, t_dart + 1.6, "in")),
                            M.bob(9, 1.7)),
           frame_at=lambda t: float(int(t * (6 if t < t_dart else 12)) % 2))
    school_b = [doc(PR.small_fish(1650, 1640, 0.55, -1, "pink", tail=tl) +
                    PR.small_fish(1730, 1690, 0.5, -1, "teal", tail=-tl) +
                    PR.small_fish(1780, 1620, 0.45, -1, "purple", tail=tl)) for tl in (0.7, -0.7)]
    school_c = [doc(PR.small_fish(1700, 1050, 0.6, -1, "blue", tail=tl) +
                    PR.small_fish(1770, 1100, 0.5, -1, "yellow", tail=-tl) +
                    PR.small_fish(1830, 1030, 0.55, -1, "blue", tail=-tl) +
                    PR.small_fish(1890, 1080, 0.45, -1, "yellow", tail=tl)) for tl in (0.7, -0.7)]
    t_c = t_surge0 + 0.8       # little fish come back once all is calm again
    sc.add("school_c", school_c, z=8.5,
           motion=M.combine(lambda t: Tf(dx=480 - 400 * progress(t, t_c, T, "out"),
                                         dy=-30 * progress(t, t_c, T, "out")),
                            M.bob(7, 1.9, 0.6)),
           frame_at=lambda t: float(int(t * (8 if t < t_c + 1.2 else 4)) % 2))
    sc.add("school_b", school_b, z=8, motion=M.combine(M.drift(vx=-14), M.bob(8, 2.1, 0.3)),
           frame_at=lambda t: float(int(t * 5) % 2))

    # ---------------------------------------------------------------- the great fish
    frames = V.fish_frames()
    WAG = V.WAG

    def fish_idx(t):
        if t < t_spot:               # glides up contentedly (happy eye)
            return 18.0 + WAG[int(t * 1.5 * 8) % 8]
        if t < t_open0:              # spots Jonah (open eye)
            return float(WAG[int(t * 1.7 * 8) % 8])
        if t < t_close0:
            return 5 + min(9, int(10 * progress(t, t_open0, t_open1, "out")))
        if t < t_close1:
            return 15 + min(2, int(3 * (t - t_close0) / (t_close1 - t_close0)))
        k = 2.6 if t < t_close1 + 1.0 else 1.4
        return 18 + WAG[int(t * k * 8) % 8]

    # key poses of the fish anchor (stage px), scale factor and tilt (negative = head up). It comes up
    # diagonally out of the blue at the lower left (always moving: the rise path is a Hermite curve that starts
    # brisk and settles, extrapolated off-screen before t_f0, so there is no velocity jump on screen).
    P_DEEP, S_DEEP, R_DEEP = (60.0, 1500.0), 0.66, -13.0
    P_MID, S_MID, R_MID = (650.0, 1460.0), 0.9, -9.0
    P_WAIT, R_WAIT = (FX0, FY0), -14.0
    SURGE = 190.0
    rise = hermite([(t_f0, 0.0, 1.5 / (t_f1 - t_f0)), (t_f1, 1.0, 0.0)])

    def fish_m(t):
        u1 = max(-0.7, rise(t))
        u2 = progress(t, t_swim0, t_swim1, "inout")
        x = lerp(P_DEEP[0], P_MID[0], u1) + (P_WAIT[0] - P_MID[0]) * u2
        y = lerp(P_DEEP[1], P_MID[1], u1) + (P_WAIT[1] - P_MID[1]) * u2
        s = lerp(S_DEEP, S_MID, max(0.0, u1)) + (1.0 - S_MID) * u2
        rot = lerp(R_DEEP, R_MID, max(0.0, u1)) + (R_WAIT - R_MID) * u2
        # lunge along its heading, then glide on and level out after the gulp
        us = progress(t, t_surge0, t_surge1, "out")
        hx, hy = math.cos(math.radians(R_WAIT)), math.sin(math.radians(R_WAIT))
        x += SURGE * us * hx
        y += SURGE * us * hy
        ua = progress(t, t_close1 + 0.6, T + 1.5, "sine")
        x += 170 * ua
        y += 20 * ua
        rot += 11 * ua
        y += 9 * math.sin(2 * math.pi * t / 2.3)
        rot += 1.8 * math.sin(2 * math.pi * t / 1.7) * (1 - 0.7 * progress(t, t_open0 - 0.3, t_open0))
        rot -= 3.0 * (progress(t, t_surge0, t_surge0 + 0.15) - progress(t, t_close0, t_close1 + 0.1))
        sx = sy = s
        if t > t_close1:             # happy wiggle after the gulp
            w = math.exp(-(t - t_close1) / 0.6)
            rot += 5.0 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1))
            sy += 0.04 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1) + 1.2)
            sx -= 0.02 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1) + 1.2)
            y += -14 * w * abs(math.sin(2 * math.pi * 1.2 * (t - t_close1)))
        if t_tun < t < t_tun + LUMP_DUR:   # a tiny squash as the lump goes down
            q = math.sin(math.pi * (t - t_tun) / LUMP_DUR)
            sy -= 0.025 * q
            sx += 0.015 * q
        return Tf(dx=x - FX0, dy=y - FY0, rot=rot, sx=sx, sy=sy, px=FX0, py=FY0)

    def fish_pt(t, lx, ly):
        f = fish_m(t)
        ux, uy = lx * FSC * f.sx, ly * FSC * f.sy
        r = math.radians(f.rot)
        return (FX0 + f.dx + ux * math.cos(r) - uy * math.sin(r), FY0 + f.dy + ux * math.sin(r) + uy * math.cos(r))

    in_c = (FX0 + SWALLOW_L[0] * FSC, FY0 + SWALLOW_L[1] * FSC)
    in_rot = SWALLOW_ROT - fish_m(t_close0).rot

    def fish_back_doc(i, m, e, tl):
        halo, light = V.fish_rim()
        loc = f'transform="translate({FX0},{FY0}) scale({FSC})"'
        body = f'<g {loc}>{halo}</g>' + PR.fish(FX0, FY0, FSC, 1, mouth=m, eye=e, tail=tl, part="back")
        body += f'<g {loc}>{light}</g>'
        if 15 <= i <= 17:
            body += PR.in_fish_mouth(jonah_markup(-1, "surprised", "s6uwd", in_c, SWALLOW_S, in_rot),
                                     FX0, FY0, FSC, 1, mouth=m)
        return doc(body, UW_DEFS)

    def haze(t):
        return 0.82 * (1 - progress(t, t_haze0, t_haze1, "sine"))

    # warm glow round the fish: only once it has come out of the dark (so the rising shadow stays dark)
    sc.add("fish_glow", fish_glow(), z=29, wc=0, blend="screen",
           motion=lambda t: Tf(dx=fish_m(t).dx, dy=fish_m(t).dy,
                               alpha=progress(t, t_glint, t_f1, "sine") * (1 - progress(t, t_open0, t_surge0, "sine"))
                               * (1 - haze(t) / 0.82) * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.9))))
    sc.add("fish_back", [fish_back_doc(i, m, e, tl) for i, (m, e, tl) in enumerate(frames)],
           z=30, motion=fish_m, frame_at=fish_idx)

    # ---------------------------------------------------------------- Jonah
    jy = hermite([(0.0, 470, 72), (4.2, 762, 72), (9.0, 1130, 60), (t_surge0, 1330, 28)])
    jx = hermite([(0.0, 1240, 10), (9.0, 1330, 14), (t_surge0, 1420, 0)])

    def jonah_path(t):
        cx = jx(t) + 16 * math.sin(2 * math.pi * t / 4.2)
        cy = jy(t) + 5 * math.sin(2 * math.pi * t / 2.9)
        rot = 6 * math.sin(2 * math.pi * t / 3.4 + 0.5)
        # a little start when the mouth opens
        cy -= 26 * progress(t, t_open0, t_open0 + 0.5, "out") * (1 - progress(t, t_open0 + 0.6, t_surge0, "sine"))
        s = 1.0
        if t > t_surge0:     # sucked into the mouth, right to the spot of the in-mouth copy
            v = progress(t, t_surge0, t_close0, "in")
            tx, ty = fish_pt(min(t, t_close0), *SWALLOW_L)
            cx, cy = lerp(cx, tx, v), lerp(cy, ty, v)
            rot = lerp(rot, SWALLOW_ROT, v)
            s = lerp(1.0, SWALLOW_S, v)
        return cx, cy, rot, s

    def jonah_m(t):
        cx, cy, rot, s = jonah_path(t)
        sq = 1 - 0.16 * bump(t, t_notice - 0.03)
        hop = -10 * bump(t, t_notice - 0.03)
        return Tf(dx=cx - JB[0], dy=cy - JB[1] + hop, rot=rot, sx=s * (2 - sq), sy=s * sq,
                  alpha=float(t < t_close0), px=JB[0], py=JB[1])

    def jonah_idx(t):
        if t < t_notice:
            return 0.0
        return 1.0 + progress(t, t_surge0 + 0.08, t_close0, "linear")

    sc.add("jonah", [doc(jonah_markup(-1, "sad"), UW_DEFS), doc(jonah_markup(-1, "surprised"), UW_DEFS),
                     doc(jonah_markup(-1, "surprised", "s6uwd"), UW_DEFS)],
           z=31, motion=jonah_m, frame_at=jonah_idx)
    sc.add("fish_front", [doc(PR.fish(FX0, FY0, FSC, 1, mouth=m, eye=e, tail=tl, part="front"))
                          for m, e, tl in frames], z=32, motion=fish_m, frame_at=fish_idx)

    # '吞了下去': a little swallow-lump slides from behind the gill to the middle of the belly
    pv = lump_pivot()

    def lump_m(t):
        u = (t - t_tun) / LUMP_DUR
        if not 0.0 < u < 1.0:
            return Tf(alpha=0.0)
        g = math.sin(math.pi * u) ** 0.85
        xl = lerp(LUMP_X0, LUMP_X1, progress(u, 0.0, 1.0, "sine"))
        tx, ty = fish_pt(t, xl, belly_y(xl))
        f = fish_m(t)
        rot = f.rot + belly_slope(xl) - belly_slope(LUMP_X0)     # follows the curve of the belly
        return Tf(dx=tx - pv[0], dy=ty - pv[1], rot=rot, sx=f.sx, sy=f.sy * max(0.02, g),
                  alpha=min(1.0, 3 * g), px=pv[0], py=pv[1])
    sc.add("lump", swallow_lump(), z=32.5, motion=lump_m)

    # rising out of the deep: a flat dark-water silhouette over the fish that fades away
    sc.add("fish_haze", [fish_silhouette("happy", frames[18 + k][2]) for k in range(5)], z=33, wc=0,
           motion=lambda t: replace(fish_m(t), alpha=haze(t)),
           frame_at=lambda t: float(min(4, max(0, fish_idx(t) - 18))))

    # ---------------------------------------------------------------- near plane
    def near_m(t):
        return Tf(dy=-NEAR_K * (cam_y(t) - cy1))
    sc.add("near_rocks", near_rocks(), z=40, motion=near_m)
    sways = [k / 4 - 1 for k in range(9)]
    weeds_l = [doc(PR.seaweed(60, 1960, 1.3, 0, sway=s) + PR.seaweed(380, 2010, 1.0, 2, sway=-s) +
                   PR.seaweed(250, 1840, 0.8, 0, sway=s * 0.6)) for s in sways]
    weeds_r = [doc(PR.seaweed(1960, 1830, 1.0, 0, sway=-s) + PR.seaweed(2080, 1900, 1.3, 2, sway=s) +
                   PR.seaweed(1780, 1990, 0.9, 0, sway=-s * 0.5)) for s in sways]
    sc.add("weeds_l", weeds_l, z=41, motion=near_m,
           frame_at=lambda t: float(round(4 + 4 * math.sin(2 * math.pi * t / 3.4))))
    sc.add("weeds_r", weeds_r, z=42, motion=near_m,
           frame_at=lambda t: float(round(4 + 4 * math.sin(2 * math.pi * t / 3.1 + 1.0))))

    # ---------------------------------------------------------------- effects
    def jonah_mouth(t):
        cx, cy, rot, s = jonah_path(t)
        return cx - 38 * JS * s, cy - 118 * JS * s

    def fish_snout(t):
        return fish_pt(t, 600, 18)

    sc.fx = [
        FX.motes((0, WL + 40, W, H), count=55, color=(214, 242, 236), size=(3, 6), alpha=85, seed=17),
        # God's providence: warm golden glints along the beam and round the rising fish
        FX.sparkles((560, 950, 1250, 1450), count=12, t0=t_glint, t1=t_open0, color=(255, 232, 160),
                    size=(9, 17), period=1.7, drift=-10, seed=59),
        FX.sparkles((150, 1250, 1100, 1750), count=26, t0=t_glint + 0.4, t1=t_open0 + 0.4,
                    color=(255, 236, 170), size=(11, 23), period=1.5, drift=-14, seed=61),
        bubble_fx([
            (jonah_mouth, -2.0, t_surge0, 3.2, 115, (5, 13), 12, 200),
            (lambda t: jonah_path(t)[:2], -1.5, 2.2, 6.0, 140, (5, 15), 70, 190),
            (fish_snout, t_close0 + 0.02, t_close1 + 0.35, 42, 200, (7, 22), 34, 225),
            (fish_snout, t_close1 + 1.1, T + 1, 2.0, 105, (5, 11), 8, 170),
        ]),
    ]

    # ---- sound
    sc.sfx("underwater", 0, dur=T + 0.8, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("bubbles", 0, dur=L0.end + 0.6, gain_db=-16, pan=0.2, fade_in=0.6, fade_out=0.8)
    sc.sfx("chime", t_glint + 0.1, gain_db=-16)
    sc.sfx("whoosh", t_f0 + 0.6, gain_db=-15, pan=-0.5)      # the dark shape sweeps up from the lower left
    sc.sfx("whoosh", t_swim0 + 0.6, gain_db=-11, pan=-0.2)   # swish peaks (~0.26 s in) near the swim's top speed
    sc.sfx("gulp", t_surge0 + 0.05, gain_db=-7)      # wet onset on the lunge, bloop / pop on the snap shut
    sc.sfx("bubbles", t_close1, dur=1.1, gain_db=-12, fade_out=0.5)
    sc.sfx("bubbles", t_close1 + 1.3, dur=1.6, gain_db=-18, pan=0.3, fade_in=0.4, fade_out=0.8)

    # handles for offline checks (not used by the renderer)
    sc.debug = dict(fish_m=fish_m, fish_pt=fish_pt, jonah_path=jonah_path, camera=camera, haze=haze,
                    beam_a=beam_a, times=dict(t_f0=t_f0, t_f1=t_f1, t_haze0=t_haze0, t_haze1=t_haze1,
                                              t_notice=t_notice, t_swim0=t_swim0, t_open0=t_open0,
                                              t_open1=t_open1, t_surge0=t_surge0, t_close0=t_close0,
                                              t_close1=t_close1, t_tun=t_tun))
    return sc
