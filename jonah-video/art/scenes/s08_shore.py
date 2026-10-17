"""Scene 8 — the great fish spits Jonah out onto dry land (Jonah 2:10).

One line: "上帝吩咐大鱼，大鱼就把约拿吐到了陆地上。" Bright sunny beach: blue sky, palms, gentle surf; the beach
curves away to the right into the distance with a grassy bank and palms behind it.

  start      the great fish rests in the shallows at the waterline, eye closed, mouth shut.
  "上帝吩咐"  warm golden rays stream down from the sun and end on the fish's head (God speaks; never a figure):
             a gold glow and rim light settle on its head (one pulse on "吩咐"), sparkles twinkle round it and a
             pool of light lies on the water in front of its face;
  "大鱼"      the fish opens its eye and listens;
  "就把约拿"  it gulps / heaves twice and opens its mouth wide — Jonah is seen inside (clipped by the jaws)...
  "吐"        ...and spits him out in a spray of water: he somersaults through the air in a comic arc, growing
             smoothly from his in-mouth size to his beach size,
  "陆地上"    lands on his bottom on the sand (puff of sand), bounces once and sits there dizzy, soaking wet with
             seaweed on his head-cloth, little stars circling his head. A gull standing on the beach takes off.
  end        the fish closes its mouth in smooth steps with a happy smile, does a cartoon turn behind a splash
             and swims away out to sea (to the left), sinking as it goes, tail wagging.
"""
import math

import cv2
import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.paths import FPS
from engine.scene import Scene

HORIZON = 472
SUN = (250, 118)
FX0, FY0, FS = 560, 640, 0.9          # the great fish: anchor (body centre) and scale
WATER_Y = 786                         # top of the near water band (in front of the fish's belly)
LAND = (1284, 955)                    # Jonah's seat on the sand (sit anchor): at the end of the scene the camera
                                      # frames his head where s09 opens with him standing (matched dissolve)
JS = 0.98                             # Jonah's scale on the beach
JS_MOUTH = 0.72                       # ... inside the fish's mouth (0.8 x the fish scale, props recipe)
GULL0 = (1725, 878)                   # the standing gull's feet
CRAB0 = (1850, 952)                   # the crab (out of the gull's take-off cone, above the subtitle zone)
HEAD = (FX0 + 330, FY0 - 150)         # the fish's head / eye region (stage, at rest)
AWAY_S = 0.8                          # fish size after its turn (a little further out to sea)
HAPPY_SHIFT = 260                     # the happy / turning frames are drawn this much further right so the whole
                                      # tail is on the canvas (at FX0 its tip is off-stage, x < 0); fish_tf undoes it

# shoreline from the near (bottom) edge, bending right and flattening as it recedes toward the far end
SHORE = [(905, 1270), (968, 1110), (1040, 985), (1130, 872), (1240, 786), (1332, 713), (1436, 650),
         (1548, 600), (1650, 566)]
TIP = (1712, 553)                     # rounded far end of the beach
# back edge of the sand (grassy bank begins), from the far tip down to the right edge, with small dunes
BACK = [(1758, 556), (1820, 568), (1880, 584), (1950, 598), (2020, 620), (2090, 640), (2160, 664), (2262, 700)]


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs)


def _cr_samples(pts, n=10):
    """Points along the open Catmull-Rom curve that S.smooth_path draws through ``pts``."""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[0]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        for k in range(1, n + 1):
            u = k / n
            a, b, c, d = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3
            out.append((a * p1[0] + b * c1[0] + c * c2[0] + d * p2[0], a * p1[1] + b * c1[1] + c * c2[1] + d * p2[1]))
    return out


def _depth(y):
    """1 at the near waterline (y >= WATER_Y), shrinking toward 0 at the horizon (perspective)."""
    return max(0.0, min(1.0, (y - HORIZON) / (WATER_Y - HORIZON)))


def _back_y(x):
    pts = [TIP] + BACK
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


# ============================================================================ painting


def sky():
    defs = (S.lin_grad("s8sky", [(0, "#6fb6dc"), (0.45, "#9dd2e8"), (0.85, "#d2ecef"), (1, "#e9f5ec")]) +
            S.rad_grad("s8sunglow", [(0, "#fff8da", 1), (0.25, "#fff1c2", 0.75), (0.6, "#fde9b4", 0.25),
                                     (1, "#fde9b4", 0)]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 60}" fill="url(#s8sky)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="420" fill="url(#s8sunglow)"/>'
    # soft sun rays
    b += S.g(f'<path d="{S.rays(SUN[0], SUN[1], 110, 230, n=14, width_deg=9, rot=8)}" fill="#fff3c8" opacity="0.7"/>',
             filter="wobble")
    b += S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="86" fill="{P["sun"]}" '
             f'stroke="{S.shade(P["sun_hot"], -0.15)}" stroke-width="4"/>'
             f'<circle cx="{SUN[0] - 24}" cy="{SUN[1] - 26}" r="34" fill="#fde49a" opacity="0.8"/>',
             filter="wobble")
    return doc(b, defs)


def clouds():
    sh = "#d9e6ee"
    b = (S.cloud(760, 150, 360, 110, "#fbf6ec", seed=11, sw=3, shade_fill=sh) +
         S.cloud(1330, 250, 260, 82, "#fbf6ec", seed=12, sw=3, shade_fill=sh) +
         S.cloud(1840, 120, 330, 100, "#fbf6ec", seed=13, sw=3, shade_fill=sh) +
         S.cloud(-60, 330, 260, 80, "#fbf6ec", seed=14, sw=3, shade_fill=sh) +
         S.cloud(2350, 300, 260, 80, "#fbf6ec", seed=15, sw=3, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def landscape():
    """Far coast, sea, beach curving away to the right horizon, grassy bank — one flattened static painting."""
    shore_pts = SHORE + [TIP] + BACK
    beach = S.smooth_path(shore_pts, closed=False) + " L2262,1270 L905,1270 Z"
    defs = (
        S.lin_grad("s8sea", [(0, "#b9e3e2"), (0.1, "#86cbd6"), (0.42, "#55acc5"), (0.75, "#4bb0c3"),
                             (1, "#5fc3c4")]) +
        S.lin_grad("s8sand", [(0, "#f4e0b0"), (0.45, P["sand"]), (1, "#e4bd80")], x1=0.8, y1=0, x2=0.2, y2=1) +
        S.lin_grad("s8grass", [(0, "#b9d38c"), (0.5, "#9cc067"), (1, "#86b052")], x1=0, y1=0, x2=0.3, y2=1) +
        f'<clipPath id="s8beachclip"><path d="{beach}"/></clipPath>'
    )
    b = ""
    # distant hazy hills on the horizon, right
    b += S.g(S.path(S.hill(1250, 2320, HORIZON + 8, 118, seed=21, bottom=HORIZON + 140, bumps=3),
                    fill="#bdd5c4", sw=2.5) +
             S.path(S.hill(1700, 2320, HORIZON + 12, 70, seed=23, bottom=HORIZON + 140, bumps=2),
                    fill="#acc9a8", sw=2.5), filter="wobble")
    # a tiny far island on the left horizon
    b += S.g(S.path(S.hill(150, 430, HORIZON + 3, 34, seed=24, bottom=HORIZON + 6, bumps=2), fill="#a9cfcf",
                    sw=2), filter="wobble", opacity=0.9)
    # sea
    b += f'<rect x="-20" y="{HORIZON}" width="{W + 40}" height="{H - HORIZON + 20}" fill="url(#s8sea)"/>'
    b += S.g(S.path(f"M-20,{HORIZON} L{TIP[0] - 20},{HORIZON}", sw=3), filter="wobble", opacity=0.5)
    hl = ""
    for i, (x, y, w) in enumerate([(30, 490, 150), (420, 498, 210), (820, 488, 140), (1090, 500, 150),
                                    (170, 538, 240), (640, 550, 200), (990, 532, 160), (20, 608, 260),
                                    (520, 640, 230), (1010, 598, 190), (1130, 660, 110), (240, 700, 280),
                                    (760, 712, 160), (1300, 512, 130), (1470, 496, 110), (1250, 566, 120),
                                    (1400, 560, 90), (1520, 530, 70), (1240, 640, 90), (1340, 618, 60)]):
        hl += S.path(S.wave_line(y, 3 + i % 3, w / 1.6, i, x0=x, x1=x + w), stroke=False,
                     extra=f'stroke="{P["foam"]}" stroke-width="{3 + (y - 480) / 70:.1f}" fill="none" '
                           f'stroke-linecap="round" opacity="0.75"')
    b += S.g(hl, filter="wobble")
    # grassy bank behind the beach (from the far tip to the right edge, up to the horizon)
    # (fill only: it tapers into the horizon on the left, inked only along the back of the beach)
    land = S.smooth_path([(TIP[0] - 190, HORIZON + 3), (TIP[0] - 90, HORIZON + 14), (TIP[0] - 30, HORIZON + 40),
                          TIP] + BACK, closed=False) + f" L2262,{HORIZON + 3} Z"
    b += S.g(S.path(land, fill="url(#s8grass)", stroke=False), filter="wobble")
    b += S.g(f'<path d="M{TIP[0] - 180},{HORIZON + 4} Q{TIP[0] - 60},{HORIZON + 16} {TIP[0] - 18},{HORIZON + 48}" '
             f'fill="none" stroke="{P["grass_dark"]}" stroke-width="2.2" opacity="0.6" stroke-linecap="round"/>',
             filter="wobble")
    # beach (fill only; the ink is drawn below, thinning with distance)
    b += S.g(S.path(beach, fill="url(#s8sand)", stroke=False), filter="wobble")
    # wet sand band along the waterline, narrowing with distance (clipped to the beach)
    samp = _cr_samples(SHORE + [TIP], 8)
    wet_a = wet_b = ""
    for p0, p1 in zip(samp, samp[1:]):
        k = _depth((p0[1] + p1[1]) / 2)
        seg = f'M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}'
        wet_a += f'<path d="{seg}" stroke-width="{max(6.0, 84 * k):.1f}"/>'
        wet_b += f'<path d="{seg}" stroke-width="{max(2.5, 34 * k):.1f}"/>'
    b += (f'<g clip-path="url(#s8beachclip)"><g fill="none" stroke="#dcb57a" stroke-linecap="round" '
          f'opacity="0.8">{wet_a}</g><g fill="none" stroke="#d0a76c" stroke-linecap="round" opacity="0.55">'
          f'{wet_b}</g></g>')
    # shoreline ink: 4.5 px near, ~1.8 px at the far end; thin ink along the back of the beach
    ink = ""
    for p0, p1 in zip(samp, samp[1:]):
        k = _depth((p0[1] + p1[1]) / 2)
        ink += (f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" '
                f'stroke-width="{1.8 + 2.7 * k:.2f}"/>')
    ink += f'<path d="{S.smooth_path([TIP] + BACK, closed=False)}" stroke-width="2.4"/>'
    b += S.g(f'<g fill="none" stroke="{S.INK}" stroke-linecap="round" stroke-linejoin="round">{ink}</g>',
             filter="wobble")
    # little dunes along the back of the beach (soft light humps with a darker foot)
    dunes = ""
    for x, w_, h_ in ((1770, 56, 8), (1880, 74, 10), (1990, 86, 12), (2120, 96, 14), (2230, 104, 15)):
        y = _back_y(x) + 10 + h_
        dunes += (f'<path d="M{x - w_ / 2:.0f},{y:.0f} Q{x:.0f},{y - 2 * h_:.0f} {x + w_ / 2:.0f},{y:.0f} Z" '
                  f'fill="{P["sand_light"]}" opacity="0.85"/>'
                  f'<path d="M{x - w_ / 2:.0f},{y:.0f} Q{x:.0f},{y + 5:.0f} {x + w_ / 2:.0f},{y:.0f}" fill="none" '
                  f'stroke="{P["sand_dark"]}" stroke-width="2.5" opacity="0.5" stroke-linecap="round"/>')
    b += S.g(f'<g clip-path="url(#s8beachclip)">{dunes}</g>', filter="wobble")
    # sand ripples
    rip = ""
    for x, y, w in ((1330, 820, 110), (1480, 700, 120), (1640, 760, 150), (1820, 820, 140), (1980, 900, 130),
                    (1240, 1010, 150), (1560, 1080, 170), (1880, 1010, 150), (1700, 920, 100), (1560, 650, 70),
                    (1760, 600, 70), (1900, 630, 60)):
        rip += S.path(S.wave_line(y, 4 * max(0.5, _depth(y)), w / 1.3, x / 100, x0=x, x1=x + w), stroke=False,
                      extra=f'stroke="{P["sand_dark"]}" stroke-width="{1.8 + 1.7 * _depth(y):.1f}" fill="none" '
                            f'opacity="0.4"')
    b += S.g(rip, filter="wobble")
    # shells, starfish, pebbles
    b += S.g(_starfish(1650, 985, 30, "#f0956f", 12) + _starfish(1446, 992, 20, "#f2b06b", -20) +
             _shell(1880, 870, 18, "#f6d6c8") + _shell(1345, 1010, 14, "#f8e6cf") + _shell(2010, 1070, 20, "#f3cdbd") +
             _pebble(1530, 1040, 16) + _pebble(1556, 1050, 10) + _pebble(1600, 700, 12) + _pebble(1290, 870, 11) +
             _pebble(1700, 600, 7),
             filter="wobble-fine")
    b += _driftwood(1660, 742, 0.9) + _beach_weed(1290, 818, 0.8, 0) + _beach_weed(1430, 712, 0.6, 1) + \
        _beach_weed(1105, 1035, 1.0, 2)
    # grassy bank details: flowers, bushes and tufts (only where the bank is)
    mead = ""
    for x, y, r, col in ((1740, 510, 4, "#f6d36b"), (1790, 528, 5, "#f3a6b3"), (1850, 512, 5, "#fbf3e3"),
                         (1900, 548, 5, "#f6d36b"), (1960, 530, 6, "#f3a6b3"), (2010, 566, 6, "#f6d36b"),
                         (2070, 540, 6, "#fbf3e3"), (2120, 590, 7, "#f3a6b3"), (2190, 560, 6, "#f6d36b"),
                         (1700, 498, 4, "#fbf3e3")):
        if y < _back_y(x) - 10 and x > TIP[0] - 20:
            mead += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="{S.INK}" stroke-width="1.6"/>'
                     f'<circle cx="{x}" cy="{y}" r="{r * 0.35:.1f}" fill="#e7a13c"/>')
    b += S.g(mead, filter="wobble-fine")
    b += (PR.bush(1800, 506, 0.18, 0) + PR.bush(1985, 516, 0.24, 3) + PR.bush(2190, 530, 0.3, 1) +
          PR.grass_tuft(1900, 506, 0.3, 2) + PR.grass_tuft(2100, 524, 0.36, 0))
    # tufts and little bushes breaking the line along the back of the beach
    for x, s_, v in ((1730, 0.24, 0), (1800, 0.3, 1), (1915, 0.36, 0), (2040, 0.42, 2), (2140, 0.48, 0),
                     (2230, 0.55, 1)):
        b += PR.grass_tuft(x, _back_y(x) + 4, s_, v)
    b += PR.bush(1860, _back_y(1860) + 6, 0.26, 1) + PR.bush(2090, _back_y(2090) + 8, 0.34, 0)
    return doc(b, defs)


def _starfish(cx, cy, r, col, rot=0):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + 36 * i)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.62))
    d = S.smooth_path(pts, tension=0.55)
    dots = "".join(f'<circle cx="{cx + r * 0.5 * math.cos(math.radians(rot - 90 + 72 * i)):.1f}" '
                   f'cy="{cy + r * 0.5 * 0.62 * math.sin(math.radians(rot - 90 + 72 * i)):.1f}" r="{r * 0.08:.1f}" '
                   f'fill="#fff0dc"/>' for i in range(5))
    return S.path(d, fill=col, sw=3) + dots


def _shell(cx, cy, r, col):
    d = (f"M{cx - r},{cy + r * 0.3} Q{cx - r * 0.9},{cy - r * 0.9} {cx},{cy - r * 0.95} "
         f"Q{cx + r * 0.9},{cy - r * 0.9} {cx + r},{cy + r * 0.3} Q{cx},{cy + r * 0.75} {cx - r},{cy + r * 0.3} Z")
    ribs = "".join(S.path(f"M{cx},{cy + r * 0.45} L{cx + r * 0.8 * math.sin(math.radians(a)):.1f},"
                          f"{cy - r * 0.75 * math.cos(math.radians(a)):.1f}", sw=1.8) for a in (-60, -30, 0, 30, 60))
    return S.path(d, fill=col, sw=3) + ribs


def _pebble(cx, cy, r):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.62:.1f}" fill="#c9b9a2" stroke="{S.INK}" '
            f'stroke-width="2.5"/><ellipse cx="{cx - r * 0.3:.1f}" cy="{cy - r * 0.2:.1f}" rx="{r * 0.35:.1f}" '
            f'ry="{r * 0.18:.1f}" fill="#e6dccb"/>')


def _driftwood(x, y, s=1.0):
    """A sun-bleached branch lying on the sand."""
    d = (f"M{x - 110 * s},{y + 4 * s} Q{x - 40 * s},{y - 18 * s} {x + 60 * s},{y - 6 * s} "
         f"L{x + 118 * s},{y - 4 * s}")
    br = (f"M{x + 10 * s},{y - 10 * s} Q{x + 30 * s},{y - 40 * s} {x + 62 * s},{y - 46 * s}"
          f" M{x - 60 * s},{y - 4 * s} Q{x - 80 * s},{y - 26 * s} {x - 96 * s},{y - 34 * s}")
    return (f'<path d="{d}" fill="none" stroke="{S.INK}" stroke-width="{24 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#c9b394" stroke-width="{17 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="{br}" fill="none" stroke="{S.INK}" stroke-width="{12 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="{br}" fill="none" stroke="#c9b394" stroke-width="{6.5 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x - 70 * s},{y - 4 * s} Q{x},{y - 12 * s} {x + 70 * s},{y - 8 * s}" fill="none" '
            f'stroke="#a8916f" stroke-width="{2.5 * s:.1f}"/>')


def _beach_weed(x, y, s=1.0, seed=0):
    """A little tangle of washed-up seaweed."""
    b = ""
    for i, (dx, ln, ang) in enumerate(((-20, 60, -12), (0, 76, 4), (18, 54, 18), (-6, 44, 30))):
        a = math.radians(ang + seed * 7)
        x1, y1 = x + dx * s + ln * s * math.cos(a), y - 6 * s + ln * s * math.sin(a) * 0.35
        cx, cy = (x + dx * s + x1) / 2, (y + y1) / 2 - 16 * s
        col = ("#6a8f3c", "#7fa34a", "#5d7f36", "#8aa850")[i]
        b += (f'<path d="M{x + dx * s:.0f},{y:.0f} Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f}" fill="none" '
              f'stroke="{S.INK}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>'
              f'<path d="M{x + dx * s:.0f},{y:.0f} Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f}" fill="none" '
              f'stroke="{col}" stroke-width="{5 * s:.1f}" stroke-linecap="round"/>')
    return b


def crab(x, y, s=1.0, step=0):
    """A small friendly crab seen from the front (anchor: between its feet). step 0/1 = leg shuffle.
    Muted coral red so it stays a background detail next to Jonah."""
    red, dark, light = "#d48a6c", "#a8664f", "#eab49a"
    b = ""
    for side in (-1, 1):
        for k in range(3):
            lift = (4 if (k + step + (side > 0)) % 2 else 0) * s
            hx, hy = x + side * (14 + 9 * k) * s, y - 18 * s
            kx, ky = x + side * (34 + 10 * k) * s, y - (26 - 4 * k) * s - lift
            fx_, fy = x + side * (40 + 12 * k) * s, y - lift * 0.5
            b += (f'<path d="M{hx:.1f},{hy:.1f} L{kx:.1f},{ky:.1f} L{fx_:.1f},{fy:.1f}" fill="none" '
                  f'stroke="{S.INK}" stroke-width="{7 * s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                  f'<path d="M{hx:.1f},{hy:.1f} L{kx:.1f},{ky:.1f} L{fx_:.1f},{fy:.1f}" fill="none" '
                  f'stroke="{dark}" stroke-width="{3.5 * s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    for side in (-1, 1):
        ax, ay = x + side * 26 * s, y - 30 * s
        cx, cy = x + side * 44 * s, y - (54 + 3 * step * (side > 0)) * s
        b += (f'<path d="M{ax:.1f},{ay:.1f} Q{x + side * 44 * s:.1f},{y - 34 * s:.1f} {cx:.1f},{cy + 8 * s:.1f}" '
              f'fill="none" stroke="{S.INK}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>'
              f'<path d="M{ax:.1f},{ay:.1f} Q{x + side * 44 * s:.1f},{y - 34 * s:.1f} {cx:.1f},{cy + 8 * s:.1f}" '
              f'fill="none" stroke="{red}" stroke-width="{5 * s:.1f}" stroke-linecap="round"/>')
        b += (f'<path d="M{cx - 12 * s:.1f},{cy + 4 * s:.1f} Q{cx - 14 * s:.1f},{cy - 16 * s:.1f} {cx:.1f},'
              f'{cy - 14 * s:.1f} Q{cx + 14 * s:.1f},{cy - 14 * s:.1f} {cx + 12 * s:.1f},{cy + 2 * s:.1f} '
              f'L{cx + 2 * s:.1f},{cy - 4 * s:.1f} Z" fill="{red}" stroke="{S.INK}" stroke-width="{3 * s:.1f}" '
              f'stroke-linejoin="round"/>')
    b += (f'<ellipse cx="{x}" cy="{y - 26 * s:.1f}" rx="{30 * s:.1f}" ry="{18 * s:.1f}" fill="{red}" '
          f'stroke="{S.INK}" stroke-width="{3.5 * s:.1f}"/>'
          f'<ellipse cx="{x - 8 * s:.1f}" cy="{y - 33 * s:.1f}" rx="{12 * s:.1f}" ry="{5 * s:.1f}" fill="{light}"/>')
    for side in (-1, 1):
        ex, ey = x + side * 9 * s, y - 52 * s
        b += (f'<path d="M{x + side * 6 * s:.1f},{y - 40 * s:.1f} L{ex:.1f},{ey + 6 * s:.1f}" stroke="{S.INK}" '
              f'stroke-width="{3 * s:.1f}"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="{6.5 * s:.1f}" fill="#fbf3e3" '
              f'stroke="{S.INK}" stroke-width="{2.5 * s:.1f}"/><circle cx="{ex + 1 * s:.1f}" cy="{ey + 1 * s:.1f}" '
              f'r="{3 * s:.1f}" fill="#3a271b"/>')
    b += (f'<path d="M{x - 7 * s:.1f},{y - 22 * s:.1f} Q{x},{y - 16 * s:.1f} {x + 7 * s:.1f},{y - 22 * s:.1f}" '
          f'fill="none" stroke="{S.INK}" stroke-width="{2.5 * s:.1f}" stroke-linecap="round"/>')
    return f'<g filter="url(#wobble-fine)">{b}</g>'


def palms(sway):
    return doc(PR.palm_tree(1748, 536, 0.26, lean=0.3, sway=sway * 0.4) +
               PR.palm_tree(1925, 572, 0.36, lean=-0.2, sway=-sway * 0.5) +
               PR.palm_tree(1800, 630, 0.7, lean=0.25, sway=sway) +
               PR.palm_tree(2030, 700, 1.0, lean=-0.35, sway=-sway))


def mid_waves():
    """Foam crest lines on the open water between the horizon and the fish (moving layer)."""
    b = ""
    for i, (x, y, w) in enumerate([(-40, 742, 420), (430, 760, 360), (120, 668, 300), (760, 690, 260),
                                    (980, 748, 200), (300, 600, 220), (1180, 610, 110)]):
        b += S.path(S.wave_line(y, 6, w / 2.2, i * 1.7, x0=x, x1=x + w), stroke=False,
                    extra=f'stroke="{P["foam"]}" stroke-width="{5 + (y - 600) / 40:.1f}" fill="none" '
                          f'stroke-linecap="round" opacity="0.8"')
    return doc(S.g(b, filter="wobble"))


def _scallop_band(pts, depth=16, r=24):
    """Foam band hanging under a wavy top edge: top follows pts (left->right), bottom is a row of scallops."""
    d = S.smooth_path(pts, closed=False)
    x1, y1 = pts[-1]
    d += f" L{x1:.0f},{y1 + depth:.0f}"
    x = x1
    i = 0
    while x > pts[0][0]:
        nx = x - 2 * r
        yy = _wave_y(pts, nx) + depth + (5 if i % 2 else 0)
        d += f" A{r},{r * 0.7:.0f} 0 0 1 {nx:.0f},{yy:.0f}"
        x = nx
        i += 1
    return d + " Z"


def _wave_y(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


def near_water():
    """Water band in front of the fish's belly, running up onto the sand along the shoreline."""
    defs = S.lin_grad("s8near", [(0, "#62c5c7", 0.8), (0.22, "#52b6c3", 0.94), (1, "#3d9bb7", 1)])
    pts = []
    x = -120
    while x <= 1236:
        pts.append((x, WATER_Y + 8 * math.sin(x / 95.0) + 4 * math.sin(x / 31.0)))
        x += 34
    top = S.smooth_path(pts, closed=False)
    d = top + " L1240,786 L1130,872 L1040,985 L968,1110 L905,1270 L-120,1270 Z"
    body = S.path(d, fill="url(#s8near)", sw=4)
    foam = f'<path d="{_scallop_band(pts[:-1], 14, 22)}" fill="{P["foam"]}" opacity="0.85"/>'
    for i, (x, y, w) in enumerate([(40, 870, 240), (420, 905, 280), (760, 858, 190), (150, 985, 300),
                                    (560, 1015, 250), (60, 1100, 260), (520, 1135, 230)]):
        foam += S.path(S.wave_line(y, 5, w / 2.0, i, x0=x, x1=x + w), stroke=False,
                       extra=f'stroke="#c4ece8" stroke-width="{4 + (y - 850) / 70:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.7"')
    # foam lace where the water meets the sand
    lace = S.smooth_path([(905, 1270), (968, 1110), (1040, 985), (1130, 872), (1240, 786)], closed=False)
    foam += (f'<path d="{lace}" fill="none" stroke="{P["foam"]}" stroke-width="18" stroke-linecap="round" '
             f'opacity="0.92"/>')
    return doc(S.g(body + foam, filter="wobble"), defs)


def swash():
    """Foam lace along the far part of the shoreline, thinning with distance — washes in and out."""
    b = ""
    samp = _cr_samples(SHORE[4:] + [TIP], 6)
    for p0, p1 in zip(samp, samp[1:]):
        k = _depth((p0[1] + p1[1]) / 2)
        w = 2.5 + 10.5 * k
        b += (f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{P["foam"]}" '
              f'stroke-width="{w:.1f}" stroke-linecap="round" opacity="0.9"/>')
        b += (f'<path d="M{p0[0] - 9 * k:.1f},{p0[1] + 6 * k:.1f} L{p1[0] - 9 * k:.1f},{p1[1] + 6 * k:.1f}" '
              f'fill="none" stroke="#a6dcd8" stroke-width="{w * 0.4:.1f}" stroke-linecap="round" opacity="0.6"/>')
    return doc(S.g(b, filter="wobble"))


RIPPLE = (FX0 + 400, WATER_Y + 50)      # ring centre on the water in front of the fish's mouth


def ripples():
    """A pair of foam ripple rings on the water: only the front (lower) arcs, so they stay on the water.
    Bright foam over a pale-teal under-stroke (drawn without the watercolour pass so they stay crisp)."""
    cx, cy = RIPPLE
    b = ""
    for rx, ry, w, op in ((105, 18, 6, 0.95), (150, 26, 5, 0.8)):
        arc = f"M{cx - rx},{cy} A{rx},{ry} 0 0 0 {cx + rx},{cy}"
        dash = f'stroke-dasharray="{rx * 0.8:.0f} {rx * 0.16:.0f}" stroke-dashoffset="{rx * 0.1:.0f}"'
        b += (f'<path d="{arc}" transform="translate(0,3)" fill="none" stroke="#9fd6d3" stroke-width="{w + 4}" '
              f'stroke-linecap="round" opacity="{op * 0.8:.2f}" {dash}/>'
              f'<path d="{arc}" fill="none" stroke="#fbfdf6" stroke-width="{w}" stroke-linecap="round" '
              f'opacity="{op}" {dash}/>')
    return doc(S.g(b, filter="wobble-fine"))


def _teardrop(x, y, r, ang):
    """Path data of a water drop of radius r at (x, y) whose point trails opposite to the flight angle (deg)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tx, ty = x - ux * r * 2.4, y - uy * r * 2.4
    return (f"M{tx:.1f},{ty:.1f} Q{x - ux * r * 0.6 + px * r * 1.25:.1f},{y - uy * r * 0.6 + py * r * 1.25:.1f} "
            f"{x + ux * r:.1f},{y + uy * r:.1f} Q{x - ux * r * 0.6 - px * r * 1.25:.1f},"
            f"{y - uy * r * 0.6 - py * r * 1.25:.1f} {tx:.1f},{ty:.1f} Z")


def splash_crown():
    """Water splash for the fish's turn: an irregular translucent sheet of water thrown up (white water at the
    top, pale teal below), lobes leaning outward, drops flying off, and a lumpy foam mound at the waterline."""
    cx, y = FX0, WATER_Y + 6
    span = 190
    lobes = [(-1.0, 120, -36), (-0.55, 215, -20), (-0.12, 265, -4), (0.3, 230, 12), (0.68, 175, 26),
             (1.0, 105, 40)]          # (position -1..1, height, outward lean px)
    pts = [(cx - span - 34, y + 6)]
    for i, (u, h, lean) in enumerate(lobes):
        tx, ty = cx + span * u + lean, y - h
        w = 15 + 0.05 * h                    # rounded lobe top (two shoulder points instead of a point)
        pts += [(tx - w, ty + 9), (tx, ty - 3), (tx + w, ty + 9)]
        if i + 1 < len(lobes):
            u2, h2, lean2 = lobes[i + 1]
            pts.append(((tx + cx + span * u2 + lean2) / 2, y - min(h, h2) * 0.62))
    pts.append((cx + span + 34, y + 6))
    sheet = S.smooth_path(pts, closed=False) + " Z"
    defs = (f'<linearGradient id="s8spl" gradientUnits="userSpaceOnUse" x1="0" y1="{y - 270}" x2="0" y2="{y}">'
            f'<stop offset="0" stop-color="{P["foam"]}"/><stop offset="0.3" stop-color="#e9f7f3"/>'
            f'<stop offset="0.65" stop-color="#bfe7e6" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="#9fd8d8" stop-opacity="0.75"/></linearGradient>')
    b = S.path(sheet, fill="url(#s8spl)", sw=3.5)
    for u, h, lean in lobes[1:-1]:
        tx = cx + span * u + lean
        bx = cx + span * u * 0.7
        b += (f'<path d="M{bx:.1f},{y - 12} Q{(bx + tx) / 2:.1f},{y - h * 0.5:.1f} {tx - 4:.1f},{y - h + 40:.1f}" '
              f'stroke="#fbfdf8" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # drops thrown outward and up
    for u, h, lean in lobes:
        side = 1 if u > 0 else -1
        for j, (ox, oy, r) in enumerate(((26, -38, 9), (60, -8, 6), (6, -76, 6))):
            if (int(h) + j) % 3 == 0:
                continue
            x_, y_ = cx + span * u + lean + side * ox, y - h + oy
            ang = math.degrees(math.atan2(-1.6, side * (0.6 + abs(u))))
            b += S.path(_teardrop(x_, y_, r, ang), fill="#d8f2ef", sw=2.4)
    # lumpy foam mound along the waterline (varied puffs, biggest in the middle)
    rng = np.random.default_rng(31)
    blobs = []
    x = cx - span - 50
    while x < cx + span + 50:
        near = 1 - abs(x - cx) / (span + 50)
        r = 10 + 26 * near ** 0.7 * rng.uniform(0.7, 1.15)
        blobs.append((x, y - r * rng.uniform(0.1, 0.55), r))
        x += r * rng.uniform(0.9, 1.4)
    c = "".join(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r:.1f}"/>' for bx, by, r in blobs)
    b += f'<g fill="{P["foam"]}" stroke="{S.INK}" stroke-width="7">{c}</g><g fill="{P["foam"]}">{c}</g>'
    return doc(S.g(b, filter="wobble-fine"), defs)


def foreground():
    """Rocks in the water (lower left) and beach grass (lower right) framing the page."""
    rock = "#a4ab9c"
    defs = S.lin_grad("s8rock", [(0, "#bfc4b4"), (0.55, rock), (1, "#7d8a86")])
    b = S.g(
        S.path(S.blob(110, 1130, 150, 84, 0.12, seed=3), fill="url(#s8rock)", sw=4) +
        S.path(S.blob(300, 1190, 115, 64, 0.12, seed=4), fill="url(#s8rock)", sw=4) +
        '<path d="M30,1090 Q90,1060 170,1080" fill="none" stroke="#e1e4d6" stroke-width="10" '
        'stroke-linecap="round" opacity="0.8"/>'
        '<path d="M250,1150 Q300,1132 350,1146" fill="none" stroke="#e1e4d6" stroke-width="8" '
        'stroke-linecap="round" opacity="0.8"/>' +
        _beach_weed(200, 1112, 0.8, 3) +
        f'<ellipse cx="200" cy="1196" rx="260" ry="26" fill="{P["foam"]}" opacity="0.85"/>' +
        S.path(S.wave_line(1176, 6, 60, 0, x0=-30, x1=440), stroke=False,
               extra=f'stroke="{P["foam"]}" stroke-width="10" fill="none" stroke-linecap="round"'), filter="wobble")
    b += (PR.grass_tuft(1990, 1185, 1.5, 1) + PR.grass_tuft(2090, 1190, 1.7, 0) + PR.grass_tuft(1860, 1205, 1.2, 1))
    return doc(b, defs)


# ---------------------------------------------------------------------------- God's light on the fish


def god_rays():
    """Warm rays streaming from the sun and ending on the great fish's head, plus a soft halo around the head
    on the sky (behind the fish). Revealed from the sun outward."""
    hx, hy = HEAD
    b = ""
    for ang, wdt, r1 in ((22.5, 4.5, 700), (27.5, 3.2, 760), (31.5, 6.0, 745), (36.5, 3.8, 700), (41, 5.0, 640)):
        r0 = 100
        a0, a1 = math.radians(ang - wdt / 2), math.radians(ang + wdt / 2)
        pts = [(SUN[0] + r0 * math.cos(a0), SUN[1] + r0 * math.sin(a0)),
               (SUN[0] + r1 * math.cos(a0 - 0.012), SUN[1] + r1 * math.sin(a0 - 0.012)),
               (SUN[0] + r1 * math.cos(a1 + 0.012), SUN[1] + r1 * math.sin(a1 + 0.012)),
               (SUN[0] + r0 * math.cos(a1), SUN[1] + r0 * math.sin(a1))]
        b += f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="url(#s8ray)"/>'
    defs = (f'<linearGradient id="s8ray" gradientUnits="userSpaceOnUse" x1="{SUN[0]}" y1="{SUN[1]}" '
            f'x2="{hx}" y2="{hy}"><stop offset="0" stop-color="#fff4c4" stop-opacity="0.95"/>'
            f'<stop offset="0.55" stop-color="#ffe48a" stop-opacity="0.75"/>'
            f'<stop offset="0.9" stop-color="#ffe08a" stop-opacity="0.45"/>'
            f'<stop offset="1" stop-color="#ffe08a" stop-opacity="0.15"/></linearGradient>')
    defs += S.rad_grad("s8halo", [(0, "#fff2b8", 0.75), (0.45, "#ffe9a0", 0.35), (1, "#ffe9a0", 0)])
    glow = f'<ellipse cx="{hx - 20}" cy="{hy - 30}" rx="420" ry="320" fill="url(#s8halo)"/>'
    return doc(S.g(b, filter="soft") + glow, defs)


def head_glow():
    """Soft gold veil ON the fish's head and eye (normal blend, drawn above the fish, moves with it)."""
    hx, hy = HEAD
    defs = S.rad_grad("s8hglow", [(0, "#fff7d2", 1), (0.35, "#ffeaa6", 0.75), (0.7, "#ffe08a", 0.3),
                                  (1, "#ffe08a", 0)])
    return doc(f'<ellipse cx="{hx}" cy="{hy}" rx="380" ry="300" fill="url(#s8hglow)"/>', defs)


def head_light():
    """Warm light added onto the head (additive blend: the colour is the amount of light added)."""
    hx, hy = HEAD
    defs = S.rad_grad("s8hlight", [(0, "#6a5420", 1), (0.4, "#5a4418", 0.8), (0.75, "#3c2c0c", 0.35),
                                   (1, "#3c2c0c", 0)])
    return doc(f'<ellipse cx="{hx + 10}" cy="{hy - 10}" rx="340" ry="280" fill="url(#s8hlight)"/>', defs)


def head_rim():
    """Gold rim light along the sun-facing (upper-left) edges of the fish's head, back and dorsal fin: the fish
    silhouette minus itself shifted away from the sun, softened, kept inside the silhouette, faded out away
    from the head."""
    hx, hy = HEAD
    fishm = PR.fish(FX0, FY0, FS, 1, mouth=0.0, eye="open", tail=0.0)
    defs = ('<filter id="s8rim" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            '<feOffset in="SourceAlpha" dx="24" dy="16" result="o"/>'
            '<feComposite in="SourceAlpha" in2="o" operator="out" result="r"/>'
            '<feGaussianBlur in="r" stdDeviation="6" result="rb"/>'
            '<feComposite in="rb" in2="SourceAlpha" operator="in" result="ri"/>'
            '<feFlood flood-color="#fff4c4"/>'
            '<feComposite in2="ri" operator="in"/></filter>' +
            S.rad_grad("s8rimfade", [(0, "#ffffff", 1), (0.55, "#ffffff", 0.85), (1, "#ffffff", 0)]) +
            f'<mask id="s8rimmask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<ellipse cx="{hx - 60}" cy="{hy - 40}" rx="520" ry="380" fill="url(#s8rimfade)"/></mask>')
    return doc(f'<g mask="url(#s8rimmask)"><g filter="url(#s8rim)">{fishm}</g></g>', defs)


def light_pool():
    """A pool of warm light on the water in front of the fish's face."""
    cx, cy = FX0 + 485, WATER_Y + 34
    defs = S.rad_grad("s8pool", [(0, "#fff3c0", 0.95), (0.5, "#ffe597", 0.55), (1, "#ffe597", 0)])
    b = f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="30" fill="url(#s8pool)"/>'
    for dx, dy, w in ((-70, -4, 46), (10, 6, 62), (70, -8, 36), (-20, 16, 40)):
        b += (f'<path d="M{cx + dx - w / 2},{cy + dy} q{w / 2},-4 {w},0" stroke="#fff6d2" stroke-width="4" '
              f'fill="none" stroke-linecap="round" opacity="0.9"/>')
    return doc(S.g(b, filter="wobble-fine"), defs)


def sand_puff(side):
    """A soft dusty sand cloudlet beside Jonah's seat (side -1 left / +1 right): no ink, sandy tint, blurred.
    The left one sits a little closer (the waterline is just beyond his feet)."""
    x = LAND[0] + side * (105 if side > 0 else 85)
    tint, shade = "#f6e7c4", "#dcbd86"
    b = S.cloud(x, LAND[1] - 22, 112, 46, tint, seed=40 + side, puffs=4, sw=0, shade_fill=shade)
    b += S.cloud(x + side * 66, LAND[1] - 6, 66, 30, tint, seed=42 + side, puffs=3, sw=0, shade_fill=shade)
    return doc(f'<g filter="url(#s8dust)">{b}</g>',
               '<filter id="s8dust" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/>'
               '</filter>')


# ============================================================================ particles


class Overlay:
    """Small antialiased RGBA canvas for particles (drawn with OpenCV at 1/4 px precision). Colours are
    drawn premultiplied (so antialiased edges never go dark) and converted to straight alpha on output."""

    def __init__(self, pts, pad, w_max=1920, h_max=1080):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.x0 = int(max(0, min(xs) - pad))
        self.y0 = int(max(0, min(ys) - pad))
        self.x1 = int(min(w_max, max(xs) + pad))
        self.y1 = int(min(h_max, max(ys) + pad))
        self.ok = self.x1 > self.x0 and self.y1 > self.y0
        if self.ok:
            self.a = np.zeros((self.y1 - self.y0, self.x1 - self.x0, 4), np.uint8)

    @staticmethod
    def _pm(col):
        a = col[3] / 255.0
        return (col[0] * a, col[1] * a, col[2] * a, col[3])

    def _p(self, x, y):
        return int(round((x - self.x0) * 4)), int(round((y - self.y0) * 4))

    def circle(self, x, y, r, col):
        cv2.circle(self.a, self._p(x, y), max(1, int(r * 4)), self._pm(col), -1, cv2.LINE_AA, 2)

    def poly(self, pts, col):
        p = np.array([self._p(x, y) for x, y in pts], np.int32)
        cv2.fillPoly(self.a, [p], self._pm(col), cv2.LINE_AA, 2)

    def polyline(self, pts, col, w):
        p = np.array([self._p(x, y) for x, y in pts], np.int32)
        cv2.polylines(self.a, [p], False, self._pm(col), max(1, int(round(w))), cv2.LINE_AA, 2)

    def image(self):
        a = self.a.astype(np.float32)
        al = a[..., 3:4]
        rgb = np.where(al > 0, a[..., :3] * 255.0 / np.maximum(al, 1), 0)
        return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al]).astype(np.uint8), "RGBA")

    def paste(self, frame):
        if self.ok:
            frame.alpha_composite(self.image(), dest=(self.x0, self.y0))
        return frame


def ballistic(origin, t0, n, ang, speed, size, life, grav, seed, spread=(18, 14)):
    """n particles launched around ``origin`` (a point, or a list of points to pick from)."""
    rng = np.random.default_rng(seed)
    a = np.radians(rng.uniform(*ang, n))
    v = rng.uniform(*speed, n)
    if isinstance(origin, list):
        k = rng.integers(0, len(origin), n)
        ox = np.array([origin[i][0] for i in k])
        oy = np.array([origin[i][1] for i in k])
    else:
        ox, oy = np.full(n, origin[0]), np.full(n, origin[1])
    return dict(t0=t0 + rng.uniform(0, 0.06, n), x=ox + rng.uniform(-spread[0], spread[0], n),
                y=oy + rng.uniform(-spread[1], spread[1], n), vx=v * np.cos(a), vy=v * np.sin(a),
                r=rng.uniform(*size, n), life=rng.uniform(*life, n), grav=grav)


def live_particles(P_, t, floor):
    """Yield (i, x, y, vx, vy, age_frac) for the particles of set P_ alive at t (above ``floor``)."""
    age = t - P_["t0"]
    live = (age >= 0) & (age <= P_["life"])
    for i in np.nonzero(live)[0]:
        a = age[i]
        x = P_["x"][i] + P_["vx"][i] * a
        y = P_["y"][i] + P_["vy"][i] * a + 0.5 * P_["grav"] * a * a
        if y > floor:
            continue
        yield i, x, y, P_["vx"][i], P_["vy"][i] + P_["grav"] * a, a / P_["life"][i]


# ============================================================================ helpers: transforms


def tf_matrix(tf):
    """3x3 matrix of a layer Tf (same convention as the compositor: T(p+d) R S T(-p))."""
    px = tf.px if tf.px is not None else 0.0
    py = tf.py if tf.py is not None else 0.0
    r = math.radians(tf.rot)
    c, s = math.cos(r), math.sin(r)
    a, b, cc, d = c * tf.sx, -s * tf.sy, s * tf.sx, c * tf.sy
    return np.array([[a, b, px + tf.dx - (a * px + b * py)], [cc, d, py + tf.dy - (cc * px + d * py)], [0, 0, 1]])


def apply(Mx, p):
    v = Mx @ np.array([p[0], p[1], 1.0])
    return float(v[0]), float(v[1])


def svg_matrix(Mx):
    return (f"matrix({Mx[0, 0]:.6f},{Mx[1, 0]:.6f},{Mx[0, 1]:.6f},{Mx[1, 1]:.6f},"
            f"{Mx[0, 2]:.3f},{Mx[1, 2]:.3f})")


# ============================================================================ build


def fish_frames():
    """(facing, mouth, eye, tail) per flipbook frame."""
    calm = [-0.3, -0.15, 0.0, 0.15, 0.3]                                 # small lazy wag while resting
    swim = [-0.7, -0.35, 0.0, 0.35, 0.7]
    fr = [(1, 0.0, "closed", tl) for tl in calm]                         # 0-4   resting
    fr += [(1, 0.0, "open", tl) for tl in calm]                          # 5-9   listening
    fr += [(1, k / 8, "surprised", 0.0) for k in range(1, 9)]            # 10-17 opening wide
    fr += [(1, m, e, 0.0) for m, e in ((0.9, "surprised"), (0.78, "surprised"), (0.65, "open"), (0.5, "open"),
                                       (0.36, "happy"), (0.22, "happy"), (0.1, "happy"))]  # 18-24 closing
    fr += [(1, 0.0, "happy", tl) for tl in swim]                         # 25-29 happy, turning, swimming away
    return fr


WAG = [0, 1, 2, 3, 4, 3, 2, 1]
F_OPEN, F_CLOSE, F_HAPPY = 10, 18, 25


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines[0]
    d = L.end - L.start

    # ---- timing, keyed to the words of the narration
    t_light0 = L.start + 0.03 * d          # 上帝吩咐… golden light
    t_light1 = L.start + 0.46 * d
    t_pulse = max(L.start + 0.12 * d, t_light0 + 0.42)   # …吩咐: the glow pulses once
    t_wake = L.start + 0.22 * d            # …大鱼: the fish opens its eye
    t_heave = L.start + 0.50 * d           # 大鱼就把约拿: two big gulps
    t_open0 = L.start + 0.615 * d
    t_spit = L.start + 0.70 * d            # 吐
    t_land = L.start + 0.835 * d           # 陆地上
    t_hop = t_land + 0.30                  # second (small) bounce contact
    t_close0 = t_spit + 0.16
    t_close1 = t_close0 + 7 / FPS          # 7 closing poses, exactly one per video frame, then shut
    t_turn0 = t_land + 0.22                # the fish turns round (behind a splash)...
    t_turn1 = t_turn0 + 0.26
    t_swim = t_turn1 - 0.04                # ...and swims away
    t_peek = t_open0 + 0.14                # Jonah can be seen inside the opening mouth
    t_out = t_spit + 0.15                  # Jonah has cleared the lips: from now on he is drawn in front

    # ---- painting
    sc.add("sky", sky(), z=0, wc=0.6)
    sc.add("clouds", clouds(), z=1, motion=M.drift(vx=14))
    sc.add("landscape", landscape(), z=2)
    pal = [palms(s) for s in (-0.35, 0.0, 0.35)]
    sc.add("palms", pal, z=3, frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.6))

    def light_env(t):      # on the head as the rays arrive there (~frac 0.6 of the reveal)
        return progress(t, t_light0 + 0.16, t_light0 + 0.5, "sine") * (1 - progress(t, t_light1, t_light1 + 0.6, "sine"))

    reveal_t1 = t_light0 + 0.9

    def rays_reveal(t):
        if t >= reveal_t1:
            return {"mode": "down", "frac": 1.0}
        return {"mode": "radial", "frac": progress(t, t_light0, reveal_t1, "out"), "soft": 160,
                "cx": SUN[0], "cy": SUN[1]}
    sc.add("god_rays", god_rays(), z=4, wc=0, reveal=rays_reveal,
           motion=lambda t: Tf(alpha=(1 - progress(t, t_light1, t_light1 + 0.6, "sine")) * float(t >= t_light0)))
    sc.add("mid_waves", mid_waves(), z=5, wc=0.5, wc_edge=0, motion=M.combine(M.bob(5, 3.1), M.bob(14, 4.7, 0.2, axis="x")))
    sc.add("swash", swash(), z=6,
           motion=lambda t: Tf(dx=-9 * math.sin(2 * math.pi * t / 3.4), dy=7 * math.sin(2 * math.pi * t / 3.4),
                               alpha=0.75 + 0.25 * math.sin(2 * math.pi * t / 3.4 + 0.6)))

    # gulls in the sky
    gw = [1.0, 0.5, 0.0, -0.5, -1.0]
    gulls = [doc(PR.gull(1010, 330, 0.42, 1, wing=w) + PR.gull(1160, 395, 0.34, 1, wing=gw[(i + 2) % 5]))
             for i, w in enumerate(gw)]
    GF = [0, 1, 2, 3, 4, 3, 2, 1]
    sc.add("gulls", gulls, z=7, motion=M.combine(M.drift(vx=48, vy=-5), M.bob(10, 2.2)),
           frame_at=lambda t: float(GF[int(t * 9) % 8]))

    # ---- the great fish
    frames = fish_frames()
    open_set = {i for i, f in enumerate(frames) if f[1] > 0}

    def fish_idx(t):
        if t < t_wake:
            return float(WAG[int(t * 7) % 8])
        if t < t_open0:
            return 5.0 + WAG[int(t * 7) % 8]
        if t < t_close0:
            return F_OPEN + min(7, int(8 * progress(t, t_open0, t_spit, "out")))
        if t < t_close1:
            return F_CLOSE + min(6, int(7 * (t - t_close0) / (t_close1 - t_close0)))
        return F_HAPPY + WAG[int(t * (7 if t < t_turn0 else 11)) % 8]

    def fish_tf(t):
        x = 0.0
        y = 7 * math.sin(2 * math.pi * t / 2.7)
        rot = 0.8 * math.sin(2 * math.pi * t / 3.3)
        sx = sy = 1.0
        # two big gulps before spitting
        for tg in (t_heave + 0.05, t_heave + 0.32):
            k = math.exp(-((t - tg) / 0.08) ** 2)
            sx += 0.06 * k
            sy -= 0.05 * k
            y -= 14 * k
            rot -= 2.5 * k
        # spit recoil
        if t > t_spit - 0.05:
            k = progress(t, t_spit - 0.05, t_spit + 0.05, "out") * (1 - progress(t, t_spit + 0.08, t_spit + 0.6))
            x -= 45 * k
            rot -= 4 * k
            sy += 0.03 * k
        # happy wiggle after closing
        if t > t_close1:
            w = math.exp(-(t - t_close1) / 0.4) * (1 - progress(t, t_turn0 - 0.1, t_turn0))
            rot += 2.5 * w * math.sin(2 * math.pi * 3.0 * (t - t_close1))
        # cartoon turn: squash to a sliver behind the splash, come out mirrored (facing the open sea) and a
        # little smaller (further out); a small hop and stretch at the middle of the turn
        th = progress(t, t_turn0, t_turn1, "inout")
        k_s = lerp(1.0, AWAY_S, th)
        mid = math.sin(math.pi * th)
        sx *= math.cos(math.pi * th) * k_s
        sy *= k_s * (1 + 0.07 * mid)
        y -= 26 * mid
        # ...then swims away to the left, accelerating and sinking, nose dipping
        v = max(0.0, t - t_swim)
        x -= 60 * v + 700 * v * v
        y += 50 * v + 230 * v * v
        rot -= 7 * progress(t, t_swim, t_swim + 0.8, "sine")
        # a quick tail-driven sway while swimming
        rot += 1.6 * math.sin(2 * math.pi * 1.6 * v) * progress(t, t_swim, t_swim + 0.2)
        if fish_idx(t) >= F_HAPPY:          # shifted drawing: same placement (pivot and offset move with it)
            return Tf(dx=x - HAPPY_SHIFT, dy=y, rot=rot, sx=sx, sy=sy, px=FX0 + HAPPY_SHIFT, py=FY0 + 120)
        return Tf(dx=x, dy=y, rot=rot, sx=sx, sy=sy, px=FX0, py=FY0 + 120)

    back = []
    front = []
    for i, (fc, mo, ey, tl) in enumerate(frames):
        fx0 = FX0 + (HAPPY_SHIFT if i >= F_HAPPY else 0)
        if i in open_set:
            back.append(doc(PR.fish(FX0, FY0, FS, fc, mouth=mo, eye=ey, tail=tl, part="back")))
            front.append(doc(PR.fish(FX0, FY0, FS, fc, mouth=mo, eye=ey, tail=tl, part="front")))
        else:
            back.append(doc(PR.fish(fx0, FY0, FS, fc, mouth=mo, eye=ey, tail=tl)))
            front.append(doc(""))
    sc.add("fish_back", back, z=10, motion=fish_tf, frame_at=fish_idx)

    # ---- God's light on the fish: glow + rim light above it, moving with it; a pulse on "吩咐"
    def glow_m(peak, pulse):
        def m(t):
            a = light_env(t)
            if a <= 0:
                return Tf(alpha=0.0)
            f = fish_tf(t)
            k = peak + pulse * math.exp(-((t - t_pulse) / 0.16) ** 2)
            return Tf(dx=f.dx, dy=f.dy, rot=f.rot, sx=f.sx, sy=f.sy, alpha=a * k, px=f.px, py=f.py)
        return m
    sc.add("head_glow", head_glow(), z=10.5, wc=0, motion=glow_m(0.3, 0.1))
    sc.add("head_light", head_light(), z=10.55, wc=0, blend="add", motion=glow_m(0.8, 0.25))
    sc.add("head_rim", head_rim(), z=10.6, wc=0, motion=glow_m(0.85, 0.15))

    # ---- Jonah: seen inside the open mouth, spat out, somersaults, lands on the sand
    piv = (LAND[0], LAND[1] - 132 * JS)          # body centre of the 'fall' figure drawn at LAND
    end = (LAND[0] + 4, LAND[1] - 120 * JS)
    ROT0, ROT1 = -312.0, 46.0

    def mouth_at(t):
        return frames[int(fish_idx(t))][1]

    def in_mouth(t):
        """Jonah inside the mouth: (centre stage px, rotation, absolute scale)."""
        m = max(0.75, mouth_at(t))
        cl = PR.fish_mouth_points(m)["center"]
        rest = PR.local_to_stage(FX0, FY0, FS, 1, cl[0], cl[1] + 8)
        f = fish_tf(t)
        x, y = apply(tf_matrix(f), rest)
        s = lerp(JS_MOUTH, 0.76, progress(t, t_peek, t_spit, "sine"))
        return (x, y + 4 * math.sin(t * 40)), f.rot + ROT0 + 6 * math.sin(t * 25), s

    B0, R0, S0 = in_mouth(t_spit)
    # comic arc: out of the mouth to the right, up, hang, and drop onto the sand (cubic Bezier)
    B = [B0, (B0[0] + 330, B0[1] - 120), (end[0] - 40, 40), end]

    def warp(v):          # fast out of the mouth, a little hang at the top, fast fall
        return 0.62 * (1 - (1 - v) ** 2.2) + 0.38 * v ** 2.4 if v < 1 else 1.0

    def flight(t):
        v = min(1.0, max(0.0, (t - t_spit) / (t_land - t_spit)))
        u = warp(v)
        c = [(1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3]
        x = sum(k * p[0] for k, p in zip(c, B))
        y = sum(k * p[1] for k, p in zip(c, B))
        rot = lerp(R0, ROT1, 0.5 * u + 0.5 * v)
        s = lerp(S0, JS, M.ease("sine")(v))                 # grows smoothly over the whole arc
        return x, y, rot, s

    def jonah_state(t):
        """(centre, rot, abs scale, squash) of the 'fall' figure while in the mouth / flying."""
        if t < t_spit:
            c, r, s = in_mouth(t)
            return c, r, s, 1.0
        x, y, r, s = flight(t)
        return (x, y), r, s, 1 + 0.06 * math.sin(t * 30)

    def jonah_tf(t):
        if t < t_land:
            (x, y), rot, s, sq = jonah_state(t)
            k = s / JS
            return Tf(dx=x - piv[0], dy=y - piv[1], rot=rot, sx=k, sy=k * sq, px=piv[0], py=piv[1])
        # landed: squash, one small bounce, then a woozy sway
        u = t - t_land
        sx = sy = 1.0
        dy = 0.0
        if u < 0.08:
            k = math.sin(math.pi * u / 0.16)
            sx, sy = 1 + 0.16 * k, 1 - 0.2 * k
        elif u < t_hop - t_land:
            v = (u - 0.08) / (t_hop - t_land - 0.08)
            dy = -52 * 4 * v * (1 - v)
            sx, sy = 1 - 0.04 * (1 - v), 1 + 0.06 * (1 - v)
        else:
            w = u - (t_hop - t_land)
            k = math.exp(-w / 0.12) * math.cos(2 * math.pi * w / 0.3)
            sx, sy = 1 + 0.07 * k, 1 - 0.09 * k
        rot = 3.5 * math.sin(2 * math.pi * (t - t_land) / 1.2) * progress(t, t_land + 0.3, t_land + 0.7)
        sy *= 1 + 0.012 * math.sin(2 * math.pi * t / 2.2)
        return Tf(dy=dy, rot=rot, sx=sx, sy=sy, px=LAND[0], py=LAND[1])

    j_fall = C.jonah(LAND[0], LAND[1], JS, -1, pose="fall", expr="surprised", wet=True)
    j_frames = [doc(j_fall), doc(C.jonah(LAND[0], LAND[1], JS, -1, pose="sit", expr="dizzy", wet=True))]
    wetpatch = (f'<ellipse cx="{LAND[0] - 15}" cy="{LAND[1] + 6}" rx="150" ry="30" fill="#c99d63" opacity="0.55"/>'
                f'<ellipse cx="{LAND[0] + 95}" cy="{LAND[1] + 16}" rx="30" ry="8" fill="#c99d63" opacity="0.5"/>'
                f'<ellipse cx="{LAND[0] - 160}" cy="{LAND[1] + 14}" rx="22" ry="6" fill="#c99d63" opacity="0.5"/>')
    sc.add("wetpatch", doc(S.g(wetpatch, filter="wobble")), z=15.4,
           motion=lambda t: Tf(alpha=progress(t, t_land, t_land + 0.5, "out")))
    sc.add("shadow", doc(C.ground_shadow(LAND[0] - 10, LAND[1], JS, width=230, opacity=0.25)), z=15.5,
           motion=lambda t: Tf(alpha=progress(t, t_land - 0.25, t_land, "in"),
                               sx=lerp(0.4, 1.0, progress(t, t_land - 0.25, t_land, "in")), px=LAND[0], py=LAND[1]))

    # Inside the mouth (and while leaving it) Jonah is drawn between fish(part='back') and fish(part='front'),
    # clipped by the mouth opening (props in_fish_mouth recipe). The clip must stay glued to the fish, so this
    # layer moves WITH the fish and every frame bakes Jonah's pose relative to it: one flipbook frame per
    # video frame time in [t_peek, t_out).
    n0 = int(math.ceil(t_peek * FPS - 1e-6))
    n1 = int(math.ceil(t_out * FPS - 1e-6))
    in_times = [n / FPS for n in range(n0, n1)]
    in_frames = []
    for tk in in_times:
        (x, y), r, s, sq = jonah_state(tk)
        k = s / JS
        Jm = tf_matrix(Tf(dx=x - piv[0], dy=y - piv[1], rot=r, sx=k, sy=k * sq, px=piv[0], py=piv[1]))
        loc = np.linalg.inv(tf_matrix(fish_tf(tk))) @ Jm
        fig = f'<g transform="{svg_matrix(loc)}">{j_fall}</g>'
        in_frames.append(doc(PR.in_fish_mouth(fig, FX0, FY0, FS, 1, mouth=mouth_at(tk))))

    def jin_motion(t):
        if t < t_peek - 0.02 or t >= t_out:
            return Tf(alpha=0.0)
        f = fish_tf(t)
        return Tf(dx=f.dx, dy=f.dy, rot=f.rot, sx=f.sx, sy=f.sy, px=f.px, py=f.py,
                  alpha=progress(t, t_peek - 0.02, t_peek + 0.06, "linear"))
    sc.add("jonah_in", in_frames, z=12, motion=jin_motion,
           frame_at=lambda t: float(min(len(in_times) - 1, max(0, int(round((t - in_times[0]) * FPS))))))
    sc.add("jonah", j_frames, z=16, motion=lambda t: Tf(alpha=0.0) if t < t_out else jonah_tf(t),
           frame_at=lambda t: 0.0 if t < t_land else 1.0)
    sc.add("fish_front", front, z=13, motion=fish_tf, frame_at=fish_idx)

    sc.add("near_water", near_water(), z=14,
           motion=M.combine(M.bob(5, 2.9, 0.1), M.bob(10, 4.1, axis="x")))
    sc.add("light_pool", light_pool(), z=14.3, wc=0,
           motion=lambda t: Tf(dx=4 * math.sin(2 * math.pi * t / 4.1), alpha=0.85 * light_env(t)))

    def ring(tc, k, dx0):
        def m(t):
            u = (t - tc) / 1.2
            if u < 0 or u > 1:
                return Tf(alpha=0.0)
            sc_ = lerp(0.5, 1.3, 1 - (1 - u) ** 2) * k
            return Tf(dx=dx0, sx=sc_, sy=sc_, alpha=math.sin(math.pi * min(1, u * 1.6)) * (1 - u),
                      px=RIPPLE[0], py=RIPPLE[1])
        return m
    rip = ripples()
    sc.add("ripple1", rip, z=15, wc=0, motion=ring(t_spit + 0.02, 1.0, fish_tf(t_spit + 0.02).dx))
    sc.add("ripple2", rip, z=15.05, wc=0, motion=ring(t_turn0 + 0.1, 1.35, FX0 - RIPPLE[0]))

    # the splash the fish turns behind
    def splash_m(t):
        if t < t_turn0 - 0.03 or t > t_turn1 + 0.24:
            return Tf(alpha=0.0)
        rise = progress(t, t_turn0 - 0.03, t_turn0 + 0.12, "out")
        fall = progress(t, t_turn0 + 0.16, t_turn1 + 0.24, "in")       # collapses back into the sea
        return Tf(sx=lerp(0.6, 1.08, rise) * (1 + 0.15 * fall), sy=lerp(0.15, 1.0, rise) * (1 - 0.85 * fall),
                  alpha=1 - progress(t, t_turn1, t_turn1 + 0.24, "sine"), px=FX0, py=WATER_Y + 8)
    sc.add("splash", splash_crown(), z=14.6, wc=0.5, motion=splash_m)

    # sand puffs on landing (+ smaller ones on the bounce): soft dust bursting out sideways, gone in ~0.4 s
    def puff(tc, big, side):
        def m(t):
            u = (t - tc) / 0.42
            if u < 0 or u > 1:
                return Tf(alpha=0.0)
            e = 1 - (1 - u) ** 3
            s = lerp(0.35, 1.05, e) * big
            a = 0.55 * min(1.0, u * 8) * (1 - progress(u, 0.25, 1.0, "sine"))
            return Tf(dx=side * (60 if side > 0 else 28) * e * big, dy=-24 * e, sx=s, sy=s, alpha=a,
                      px=LAND[0] + side * 40, py=LAND[1])
        return m
    for i, (tc, big) in enumerate(((t_land, 1.0), (t_hop, 0.6))):
        for side in (-1, 1):
            sc.add(f"puff{i}{side}", sand_puff(side), z=16.5 + i * 0.1 + side * 0.01, wc=0,
                   motion=puff(tc, big, side))

    # sand grains kicked up on landing: drawn on the stage just behind Jonah
    grains = ballistic((LAND[0], LAND[1] - 10), t_land, 30, (-165, -15), (250, 650), (1.6, 2.6), (0.3, 0.55), 2400,
                       82, spread=(70, 10))

    def grains_dyn(t):
        pts = list(live_particles(grains, t, LAND[1] + 30))
        if not pts:
            return None
        ov = Overlay([(p[1], p[2]) for p in pts], 24, w_max=W, h_max=H)
        if not ov.ok:
            return None
        for i, x, y, vx, vy, fr in pts:
            a = 1 - fr ** 3
            r = grains["r"][i]
            ov.polyline([(x - vx * 0.009, y - vy * 0.009), (x, y)], (176, 134, 82, int(150 * a)), 2 * r * 0.8)
            ov.circle(x, y, r, (168, 124, 72, int(235 * a)))
        return ov.image(), (ov.x0, ov.y0)
    sc.add_dynamic("grains", grains_dyn, z=15.9)

    # the standing gull takes fright and flies off steeply when Jonah lands
    g_fr = [doc(PR.gull(*GULL0, 0.72, -1, pose="stand"))] + \
        [doc(PR.gull(GULL0[0], GULL0[1] - 40 * 0.72, 0.72, 1, wing=w)) for w in gw]
    t_g = t_land + 0.12

    def gull_idx(t):
        if t < t_g:
            return 0.0
        return 1.0 + GF[int((t - t_g) * 12) % 8]          # starts on the wings-up frame

    def gull_tf(t):
        if t < t_g:
            return Tf(dy=-4 * abs(math.sin(math.pi * t / 0.9)) * progress(t, 0.0, 0.1))
        u = t - t_g
        return Tf(dx=210 * u + 160 * u * u, dy=-500 * u - 420 * u * u, rot=-16 * min(1, u * 4))

    # a little crab scuttling sideways on the sand (small, muted, out of the gull's way)
    crab_m = lambda t: Tf(dx=-34 * math.sin(2 * math.pi * t / 5.0), dy=-5 * math.sin(2 * math.pi * t / 5.0))
    sc.add("crab", [doc(crab(*CRAB0, 0.52, k)) for k in (0, 1)], z=18, motion=crab_m,
           frame_at=lambda t: float(int(t * 8) % 2))
    sc.add("gull_stand", g_fr, z=18.5, motion=gull_tf, frame_at=gull_idx)
    sc.add("foreground", foreground(), z=19)

    # ---- camera: wide while the fish acts, then (once Jonah has landed; the fish's turn and splash stay in
    # frame) a push toward Jonah that settles before the dissolve into s09 and only drifts during it. The end
    # framing is a matched dissolve: Jonah's head lands on the output spot (~985, 643) where s09's standing
    # Jonah's head is (s09: JX, JY = 980, 960 under Cam(960, 600, 1720)), at about his size, so the wet seated
    # Jonah turns into the standing one instead of two Jonahs side by side. A small bump when Jonah lands.
    cam = M.cam_keys([(0, Cam(990, 606, 1930)), (t_open0, Cam(1050, 594, 2030)),
                      (t_land + 0.2, Cam(1062, 600, 2010)), (T - 0.5, Cam(1266, 689, 1688)),
                      (T, Cam(1271, 693, 1672))], ["sine", "inout", "sine", "linear"])
    sc.camera = M.cam_shake(cam, amp=7, t0=t_land, t1=t_land + 0.35, freq=14, seed=5)

    # ---- effects (output space): spray of water drops from the mouth and from the turn
    lip_a = PR.local_to_stage(FX0, FY0, FS, 1, *PR.fish_mouth_points(1.0)["upper"])
    lip_b = PR.local_to_stage(FX0, FY0, FS, 1, *PR.fish_mouth_points(1.0)["lower"])
    Fspit = tf_matrix(fish_tf(t_spit))
    mouth_line = [apply(Fspit, (lerp(lip_a[0], lip_b[0], u), lerp(lip_a[1], lip_b[1], u)))
                  for u in np.linspace(0.12, 0.7, 9)]
    spray = ballistic(mouth_line, t_spit - 0.03, 40, (-55, -5), (380, 950), (2.2, 6.0), (0.3, 0.5), 1900, 81,
                      spread=(10, 10))
    turn_line = [(FX0 + dx, WATER_Y - 6) for dx in np.linspace(-260, 260, 9)]
    turn_spray = ballistic(turn_line, t_turn0 + 0.02, 34, (-125, -55), (300, 760), (2.2, 5.5), (0.35, 0.55), 1900,
                           83, spread=(16, 6))

    def jonah_box(t):
        if t < t_spit or t > t_land + 0.6:
            return None
        if t < t_land:
            x, y, _, s = flight(t)
            r = 125 * s
            return (x - r, y - r, x + r, y + r)
        return (LAND[0] - 130, LAND[1] - 240, LAND[0] + 90, LAND[1] + 10)

    def particles(frame, t, view):
        drops = []
        lip_x = FX0 + 380 + fish_tf(t).dx
        box = jonah_box(t)
        for P_, cull_lip in ((spray, True), (turn_spray, False)):
            for i, x, y, vx, vy, fr in live_particles(P_, t, WATER_Y + 12):
                if cull_lip and x < lip_x:
                    continue
                if box and box[0] < x < box[2] and box[1] < y < box[3]:
                    continue
                ox, oy = view.to_out(x, y)
                tx, ty = view.to_out(x - vx * 0.012, y - vy * 0.012)
                drops.append((ox, oy, P_["r"][i] * view.scale, 1 - fr ** 3, tx, ty))
        # speed lines trailing Jonah
        lines = []
        if t_spit + 0.04 < t < t_land:
            for off in (-26, 0, 26):
                seg = []
                for k in range(7):
                    tt = t - 0.025 - k * 0.022
                    if tt < t_spit:
                        break
                    x, y, _, _ = flight(tt)
                    if x < lip_x + 60:          # no streaks over the fish's open mouth
                        break
                    x2, y2, _, _ = flight(tt + 0.01)
                    nx, ny = -(y2 - y), (x2 - x)
                    n = math.hypot(nx, ny) or 1
                    seg.append(view.to_out(x + off * nx / n, y + off * ny / n))
                if len(seg) > 2:
                    lines.append(seg)
        # dizzy stars around Jonah's head
        stars = []
        if t > t_land + 0.05:
            tf = jonah_tf(t)
            k = progress(t, t_land + 0.05, t_land + 0.3, "out")
            for i in range(3):
                ang = 2 * math.pi * (t * 1.05 + i / 3)
                sx_ = jhead[0] + 62 * math.cos(ang)
                sy_ = jhead[1] - 14 + 15 * math.sin(ang)
                # follow the bounce / sway (approximate: translate only)
                stars.append((view.to_out(sx_, sy_ + tf.dy), (11 + 3 * math.sin(ang)) * view.scale, k,
                              0.6 + 0.4 * math.sin(ang)))
        allpts = [(p[0], p[1]) for p in drops] + [(p[4], p[5]) for p in drops] + [q for s in lines for q in s] + \
            [s[0] for s in stars]
        if not allpts:
            return frame
        ov = Overlay(allpts, 40)
        if not ov.ok:
            return frame
        for seg in lines:
            ov.polyline(seg, (252, 248, 236, 170), 5 * view.scale)
        for ox, oy, r, a, tx, ty in drops:
            ov.polyline([(tx, ty), (ox, oy)], (196, 228, 238, int(70 * a)), max(1.0, r * 1.1))
            ov.circle(ox, oy, r, (186, 224, 238, int(160 * a)))
            ov.circle(ox - r * 0.32, oy - r * 0.32, max(0.6, r * 0.34), (255, 255, 252, int(220 * a)))
        for (ox, oy), r, k, front_ in stars:
            star = []
            for j in range(10):
                a = -math.pi / 2 + j * math.pi / 5
                rr = r if j % 2 == 0 else r * 0.45
                star.append((ox + rr * math.cos(a), oy + rr * math.sin(a)))
            ov.poly([(x + 1.5, y + 1.5) for x, y in star], (110, 75, 45, int(150 * k)))
            ov.poly(star, (255, 214, 92, int(255 * k * (0.55 + 0.45 * front_))))
        return ov.paste(frame)

    jhead = C.body_points(C.jonah, LAND[0], LAND[1], JS, -1, pose="sit", wet=True)["head_top"]

    sc.fx = [
        FX.sparkles((1090, 490, 1340, 760), count=7, color=(255, 252, 236), size=(5, 10), period=1.3, drift=0,
                    seed=88),
        FX.sparkles((30, 840, 980, 1000), count=12, color=(255, 252, 236), size=(5, 11), period=1.5, drift=0,
                    seed=87),
        FX.sparkles((HEAD[0] - 300, HEAD[1] - 250, HEAD[0] + 260, HEAD[1] + 170), count=22, t0=t_light0 + 0.3,
                    t1=t_light1 + 0.5, color=(255, 222, 120), size=(14, 26), period=1.5, drift=-12, seed=89),
        particles,
    ]

    # ---- sound
    sc.sfx("waves_calm", 0, dur=T, gain_db=-10, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_light0 + 0.15, gain_db=-12)
    sc.sfx("gull", 0.25, gain_db=-16, pan=-0.4)
    for tg in (t_heave + 0.05, t_heave + 0.32):
        sc.sfx("gulp", tg - 0.04, gain_db=-14, pan=-0.3)
    # spit / whoosh / landing thud kept clear of the narration ("…吐到了陆地上"): the spit's peak (~+0.15 s) falls on
    # the aspiration of "吐" as Jonah clears the lips, not on its vowel; whoosh and thud are softer so "到" and "陆"
    # stay on top
    sc.sfx("spit", t_spit - 0.12, gain_db=-9, pan=-0.15)
    sc.sfx("whoosh", t_spit + 0.04, gain_db=-13, pan=0.15)
    sc.sfx("thud", t_land - 0.01, gain_db=-8, pan=0.3)
    sc.sfx("thud", t_hop - 0.01, gain_db=-13, pan=0.3)
    sc.sfx("gull", max(t_g + 0.05, L.end - 0.07), gain_db=-15, pan=0.6)   # after "陆地上", gull still in frame
    sc.sfx("splash_small", t_turn0 + 0.02, gain_db=-13, pan=-0.45)
    return sc
