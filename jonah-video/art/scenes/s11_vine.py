"""Scene 11 — the castor plant (Jonah 4:1-8).

A dry hillside east of Nineveh (the city small on the western horizon, left). Jonah sits in his little
booth facing the city. He sulks (grumpy steam puffs, a red anger mark); God makes a castor plant spring up
beside the booth (golden light, sparkles) and its big leaves shade him; he is very happy in a golden
evening. Dusk falls and a short starry night passes while he sleeps; at dawn a little worm inches out from
behind a pebble and nibbles the stem (crumbs fly); the plant withers. The sun climbs overhead and blazes,
a hot east wind blows sand and dead leaves, a lizard scurries for cover and Jonah grows faint.

Every event is keyed to ctx.lines[i] (start/end) so it follows the narration.

Notes for maintainers
* Jonah's pose changes are near-hard cuts (1 frame) hidden by a squash-and-hop (plus a little dust poof);
  only same-pose expression changes crossfade softly.
* The canopy shade is physical: a ground shadow ellipse plus a cool multiply tint of Jonah's own silhouette
  (same flipbook / motion as Jonah). Nothing darkens the far sky or dunes.
* Night is a ~0.8 s hold of a real night (blue land grade, starry sky, moon with a soft halo) spanning
  "第二天"; dusk starts at the end of line 2.
* Camera: few long sine-eased moves (slow drift, one push-in to the bite, one pull-back for the heat).
"""
import math
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as CH
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine import raster
from engine.scene import BOIL_TOKEN, Scene

# ------------------------------------------------------------------ layout (stage px)
GY = 962            # ground line of the knoll (plant root, booth, Jonah)
SP = 1.3            # plant / booth / Jonah scale
XP = 830            # castor root
XB = XP + PR.CASTOR_BOOTH_DX * SP   # booth centre (canopy arches over its roof)
XJ = XB + 28        # Jonah (sitting, facing the city on the left)
SW = 1.55           # worm scale (a touch big so a child can see it)
XW = XP - (12 * SP + 40 * SW)       # worm anchor with its mouth in the stem notch
NOTCH = (XP - 12 * SP, GY - 16 * SP)  # the bite notch in the stem (stage px)
HORIZON = 640
LIZ = (1606, 950)   # lizard basking on its stone

SUN_W = (360, 215)      # afternoon sun (west, over the city)
SUN_E = (1900, 690)     # dawn sun (east, rising behind the hills)
SUN_HOT = (1490, 225)   # noon sun, high over Jonah's head

INK = P["ink"]


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def _sharp(f, soft=0.45):
    """Flipbook index with shorter crossfades: holds each drawing, blends only around the switch."""
    i = math.floor(f)
    u = f - i
    lo = 0.5 - soft / 2
    return i + _clamp((u - lo) / soft)


def _env(t, a, b, c, d):
    """0 before a, ramps to 1 at b, holds, back to 0 at d (smooth)."""
    if t <= a or t >= d:
        return 0.0
    if t < b:
        return M.progress(t, a, b, "sine")
    if t <= c:
        return 1.0
    return 1 - M.progress(t, c, d, "sine")


# ------------------------------------------------------------------ drawing helpers
def _rock(x, y, w, h, seed=0, fill=None, sw=4):
    fill = fill or P["stone"]
    d = S.blob(x, y - h * 0.45, w / 2, h / 2, wobble=0.12, n=9, seed=seed)
    hi = S.blob(x - w * 0.12, y - h * 0.62, w * 0.28, h * 0.2, wobble=0.15, n=7, seed=seed + 1)
    return (S.path(d, fill=fill, sw=sw) +
            f'<path d="{hi}" fill="{S.shade(fill, 0.35)}" opacity="0.7"/>' +
            f'<path d="M{x - w * 0.42:.0f},{y - h * 0.12:.0f} Q{x:.0f},{y + h * 0.02:.0f} {x + w * 0.44:.0f},'
            f'{y - h * 0.16:.0f}" fill="none" stroke="{S.shade(fill, -0.25)}" stroke-width="{sw * 1.6:.1f}" '
            f'opacity="0.45" stroke-linecap="round"/>')


def _stone(x, y, w, h, seed=0, fill=None, sw=4, shadow=True, crack=False):
    """Faceted desert stone standing on the ground at (x, y): flattish base, angular top, a shaded east
    side, a sunlit top facet and a soft contact shadow (so it sits ON the sand, not floats)."""
    rnd = random.Random(seed)
    fill = fill or P["stone"]
    n = rnd.choice((5, 6, 7))
    skew = rnd.uniform(-0.2, 0.2)
    pts = [(x + w * 0.5, y + h * 0.03)]
    for i in range(n):
        a = math.pi * (i + 0.5) / n
        k = rnd.uniform(0.82, 1.06)
        pts.append((x + w * 0.5 * math.cos(a) * k + skew * w * 0.5 * math.sin(a),
                    y - h * (math.sin(a) ** 0.75) * k))
    pts.append((x - w * 0.5, y + h * 0.03))
    pts.append((x, y + h * 0.09))
    d = S.smooth_path(pts, tension=0.55)
    cid = f"stn{seed}_{int(x)}_{int(y)}_{int(w)}"
    peak = x + skew * w * 0.5
    side = (f'<path d="M{peak + w * 0.06:.1f},{y - h * 1.3:.1f} L{x + w:.1f},{y - h * 1.3:.1f} '
            f'L{x + w:.1f},{y + h:.1f} L{peak + w * 0.2:.1f},{y + h:.1f} Z" fill="{S.shade(fill, -0.24)}" '
            f'opacity="0.55"/>')
    top = (f'<ellipse cx="{peak - w * 0.14:.1f}" cy="{y - h * 0.8:.1f}" rx="{w * 0.24:.1f}" ry="{h * 0.17:.1f}" '
           f'fill="{S.shade(fill, 0.45)}" opacity="0.75"/>')
    out = ""
    if shadow:
        out += (f'<ellipse cx="{x + w * 0.1:.1f}" cy="{y + h * 0.05:.1f}" rx="{w * 0.62:.1f}" '
                f'ry="{max(5.0, h * 0.16):.1f}" fill="{INK}" opacity="0.2" filter="url(#soft)"/>')
    out += (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{fill}"/>'
            f'<g clip-path="url(#{cid})">{side}{top}</g>')
    if crack:
        out += (f'<path d="M{peak + w * 0.02:.1f},{y - h * 0.9:.1f} l{w * 0.05:.1f},{h * 0.3:.1f} '
                f'l{-w * 0.04:.1f},{h * 0.22:.1f}" fill="none" stroke="{S.shade(fill, -0.4)}" '
                f'stroke-width="{sw * 0.6:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    out += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return out


def _pebbles(x, y, k=1.0, seed=0, n=3):
    """A little cluster of pebbles (with shadows) on the ground."""
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        w = rnd.uniform(16, 30) * k
        out += _stone(x + rnd.uniform(-28, 28) * k, y + rnd.uniform(-3, 4) * k, w, w * rnd.uniform(0.45, 0.62),
                      seed=seed * 7 + i, fill=S.mix(P["stone"], P["stone_dark"], rnd.uniform(0, 0.5)),
                      sw=2.6)
    return out


def _cracks(x, y, size, seed=0, col="#9a6a3e"):
    """Cracked dry earth: a few branching hairline cracks, foreshortened onto the ground plane."""
    rnd = random.Random(seed)
    out = ""
    for b in range(3):
        a = rnd.uniform(0, 2 * math.pi) + b * 2.1
        px, py = x, y
        pts = [(px, py)]
        step = size * rnd.uniform(0.6, 1.0) / 4
        for j in range(4):
            a += rnd.uniform(-0.6, 0.6)
            px += step * math.cos(a)
            py += step * math.sin(a) * 0.32
            pts.append((px, py))
            if j == 1 and rnd.random() < 0.75:
                a2 = a + rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.1)
                out += (f'<path d="M{px:.1f},{py:.1f} l{step * 0.8 * math.cos(a2):.1f},'
                        f'{step * 0.8 * math.sin(a2) * 0.32:.1f}" stroke="{col}" stroke-width="2" '
                        f'stroke-linecap="round" fill="none" opacity="0.55"/>')
        out += ('<path d="M' + " L".join(f"{u:.1f},{v:.1f}" for u, v in pts) + f'" stroke="{col}" '
                f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.6"/>')
    return out


def _dune(pts, grad_id, sw=3.5, rim=None):
    """Sand dune whose top edge runs through pts; closed down past the bottom of the stage."""
    d = S.smooth_path(pts, closed=False) + f" L{pts[-1][0]},{H + 80} L{pts[0][0]},{H + 80} Z"
    out = S.path(d, fill=f"url(#{grad_id})", sw=sw)
    if rim:   # sunlit rim just under the crest
        rp = [(x, y + 14) for x, y in pts[1:-1]]
        out += (f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="{rim}" stroke-width="12" '
                f'opacity="0.55" stroke-linecap="round"/>')
    return out


def _puff(cx, cy, r):
    """Little cartoon puff of angry steam: warm grey with a hot pink-red rim."""
    pts = [(-0.55, 0.1, 0.55), (0.0, -0.25, 0.7), (0.55, 0.05, 0.55), (0.05, 0.32, 0.5)]
    body = ""
    for dx, dy, k in pts:
        body += (f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#ddd0cb" '
                 f'stroke="#b8473f" stroke-width="8"/>')
    for dx, dy, k in pts:
        body += f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#ddd0cb"/>'
    body += (f'<ellipse cx="{cx + 0.05 * r:.1f}" cy="{cy + 0.42 * r:.1f}" rx="{0.75 * r:.1f}" ry="{0.22 * r:.1f}" '
             f'fill="#ef9c92" opacity="0.65"/>')
    body += f'<circle cx="{cx - 0.15 * r:.1f}" cy="{cy - 0.42 * r:.1f}" r="{0.17 * r:.1f}" fill="#f8f1ea"/>'
    return S.g(body, filter="wobble-fine")


def _anger(cx, cy, s=24, col="#dc4a3c"):
    """The cartoon 'cross-popping vein' anger mark: four rounded corners pointing at the centre."""
    g_ = s * 0.3
    d = ""
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        d += (f"M{cx + sx * g_:.1f},{cy + sy * s:.1f} Q{cx + sx * g_:.1f},{cy + sy * g_:.1f} "
              f"{cx + sx * s:.1f},{cy + sy * g_:.1f} ")
    return S.g(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{s * 0.46:.1f}" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{s * 0.25:.1f}" stroke-linecap="round"/>',
               filter="wobble-fine")


def _star(cx, cy, r, fill="#f6d35a", sw=3):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}" {st}/>'


def _dead_leaf(cx, cy, r, col, curl=0.0):
    """A dry, slightly curled leaf with a midrib and stalk (blown by the hot wind)."""
    k = 1 + curl
    d = (f"M{cx:.1f},{cy - r:.1f} C{cx + r * 0.75 * k:.1f},{cy - r * 0.55:.1f} {cx + r * 0.7:.1f},{cy + r * 0.55:.1f} "
         f"{cx:.1f},{cy + r:.1f} C{cx - r * 0.55:.1f},{cy + r * 0.5:.1f} {cx - r * 0.75 / k:.1f},{cy - r * 0.5:.1f} "
         f"{cx:.1f},{cy - r:.1f} Z")
    rib = (f'<path d="M{cx:.1f},{cy + r * 1.35:.1f} Q{cx + r * 0.12:.1f},{cy:.1f} {cx:.1f},{cy - r * 0.8:.1f}" '
           f'fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    veins = "".join(f'<path d="M{cx + r * 0.05:.1f},{cy + r * v:.1f} l{r * 0.4 * sgn:.1f},{-r * 0.3:.1f}" '
                    f'stroke="{S.shade(col, -0.3)}" stroke-width="2" stroke-linecap="round"/>'
                    for v in (-0.35, 0.05, 0.45) for sgn in (-1, 1))
    return S.g(S.path(d, fill=col, sw=3) + veins + rib, filter="wobble-fine")


def _swirl(x, y, length, loop=34, col="#fff4dc"):
    """A picture-book wind stroke: a long line ending in a curl."""
    d = (f"M{x:.0f},{y:.0f} C{x + length * 0.35:.0f},{y - 18:.0f} {x + length * 0.7:.0f},{y + 14:.0f} "
         f"{x + length:.0f},{y:.0f} c{loop:.0f},-6 {loop:.0f},-{loop * 1.4:.0f} 0,-{loop * 1.1:.0f} "
         f"c-{loop * 0.6:.0f},{loop * 0.25:.0f} -{loop * 0.3:.0f},{loop * 0.8:.0f} {loop * 0.25:.0f},{loop * 0.55:.0f}")
    return (f'<path d="{d}" fill="none" stroke="{P["ink_soft"]}" stroke-width="11" stroke-linecap="round" opacity="0.35"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')


def _lizard(x, y, s=1.0, legs=0):
    """Small friendly sage-green lizard facing right; anchor = under its belly on the ground."""
    G, GD, GL = "#93b15b", "#6c8a40", "#cfdc98"

    def tube(d, w):
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 7}" stroke-linecap="round" '
                f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{G}" stroke-width="{w}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')

    def foot(px, py):
        return "".join(f'<path d="M{px:.1f},{py:.1f} l{dx},{dy}" stroke="{INK}" stroke-width="2.6" '
                       f'stroke-linecap="round"/>' for dx, dy in ((5, 1), (4, 4), (0, 5)))

    if legs == 0:
        far = [("M24,-11 L33,-2", (33, -2)), ("M-12,-11 L-3,-2", (-3, -2))]
        near = [("M19,-6 L27,3", (27, 3)), ("M-17,-6 L-25,3", (-25, 3))]
    else:
        far = [("M24,-11 L18,-1", (18, -1)), ("M-12,-11 L-20,-1", (-20, -1))]
        near = [("M19,-6 L12,4", (12, 4)), ("M-17,-6 L-8,4", (-8, 4))]
    body = ""
    for d, (fx_, fy_) in far:
        body += tube(d, 5) + foot(fx_, fy_)
    body += tube("M-26,-9 C-48,-13 -66,-7 -72,3 C-76,12 -68,18 -62,12", 6.5)
    body += (f'<path d="M-30,-9 C-22,-24 16,-27 32,-17 C38,-12 36,-5 28,-3 C8,1 -18,1 -30,-9 Z" fill="{G}" '
             f'stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>')
    body += (f'<path d="M26,-17 C32,-29 52,-29 60,-19 C64,-14 60,-8 52,-7 C42,-6 30,-8 26,-13 Z" fill="{G}" '
             f'stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>')
    body += f'<path d="M-22,-6 C-6,-2 14,-2 28,-6" fill="none" stroke="{GL}" stroke-width="3" stroke-linecap="round"/>'
    for cx, cy, r in ((-14, -17, 3.2), (0, -20, 3.6), (14, -19, 3.0), (-5, -12, 2.4), (-40, -10, 2.4)):
        body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GD}"/>'
    for d, (fx_, fy_) in near:
        body += tube(d, 5) + foot(fx_, fy_)
    body += (f'<circle cx="47" cy="-19" r="4.4" fill="#2e2630"/><circle cx="48.6" cy="-20.6" r="1.5" fill="#fffaf0"/>'
             f'<ellipse cx="52" cy="-12.5" rx="3.4" ry="2.2" fill="{P["cheek"]}" opacity="0.6"/>'
             f'<path d="M54,-11 q4,2.5 7,-1" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})"><g filter="url(#wobble-fine)">{body}</g></g>'


FLAT_DEFS = (f'<filter id="flat" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}" '
             f'color-interpolation-filters="sRGB"><feColorMatrix type="matrix" '
             f'values="0 0 0 0 0.62  0 0 0 0 0.6  0 0 0 0 0.8  0 0 0 1 0"/></filter>')


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines
    l0, l1, l2, l3, l4 = L[0], L[1], L[2], L[3], L[4]

    # --- key times (all relative to narration lines) -------------------------------------------
    t_grow0 = l1.start + 0.25                     # sprout pops up ("上帝让一棵…")
    t_grow1 = l1.start + 0.62 * (l1.end - l1.start) + 0.6   # fully grown as "为他遮阴" starts
    t_shade0, t_shade1 = t_grow0 + 1.0, l1.end - 0.1
    t_happy = l1.end - 0.75                       # Jonah relaxes in the shade
    t_gold0, t_gold1 = l2.start + 0.1, l2.end - 0.2
    # night: dusk from the end of line 2, a ~0.8 s full night over "第二天", dawn as it ends
    t_n0 = l2.end - 0.5                           # dusk begins
    t_n1 = l2.end - 0.07                          # full night
    t_n2 = l3.start + 0.42                        # dawn begins
    t_n3 = t_n2 + 0.5                             # dawn sky complete
    t_night = (t_n1 + t_n2) / 2                   # middle of the night (Jonah asleep)
    t_worm0, t_worm1 = l3.start + 0.5, l3.start + 1.33     # worm inches in ("一条虫子")
    t_bite0 = l3.start + 1.45                     # "咬了蓖麻"
    t_bite1 = t_bite0 + 0.9
    t_with0 = l3.start + 0.71 * (l3.end - l3.start)  # "蓖麻枯干了"
    t_with1 = l3.end + 0.1
    t_chomp1 = t_with0 + 0.6
    t_sun0, t_sun1 = l4.start - 0.35, l4.start + 0.75  # "烈日当头"
    t_wind = l4.start + 1.05                      # "热风吹来"
    t_faint = l4.start + 2.2                      # "约拿热得发昏"
    t_liz = t_sun1 - 0.15                         # the lizard runs for the shade

    # =============================================================== SKY
    sky_h = 665          # the far hills / plain cover everything below
    sky_day = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>',
        defs=S.lin_grad("g", [(0, "#8fc4dc"), (0.5, "#c9e3df"), (0.82, "#f4e2b8"), (1, "#f6dcab")]))
    a_gold = lambda t: _env(t, t_gold0 - 0.35, t_gold0 + 0.3, t_n1 - 0.05, t_n1 + 0.1)
    a_night = lambda t: _env(t, t_n0, t_n1, t_n3 - 0.05, t_n3 + 0.1)
    a_dawn = lambda t: _env(t, t_n2, t_n3, t_sun1 + 0.3, t_sun1 + 0.45)
    a_hot = lambda t: M.progress(t, t_sun0 + 0.1, t_sun1 + 0.3, "sine")
    # the day sky is not drawn while another sky covers it completely (saves a full-width layer)
    sc.add("sky_day", sky_day, wc=0.5,
           motion=lambda t: Tf(alpha=0.0 if max(a_gold(t), a_night(t), a_dawn(t), a_hot(t)) >= 0.999 else 1.0))

    sky_gold = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_W[0]}" cy="{HORIZON}" rx="900" ry="330" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#a98fb8"), (0.45, "#f0b98a"), (0.8, "#f8cf8c"), (1, "#fbdc9c")]) +
        S.rad_grad("r", [(0, "#ffe9a8", 0.9), (0.5, "#fbc77a", 0.4), (1, "#f3a873", 0)]))
    sc.add("sky_gold", sky_gold, wc=0.5, motion=lambda t: Tf(alpha=a_gold(t)))

    stars = ""
    rng = np.random.default_rng(4)
    for i in range(56):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, 560)
        stars += _star(x, y, rng.uniform(3, 8), "#fbf0c8", sw=0)
    mx, my = 1780, 170
    moon = (f'<path d="M{mx},{my - 70} A70,70 0 1 1 {mx},{my + 70} A54,70 0 1 0 {mx},{my - 70} Z" fill="#fbf1cf" '
            f'stroke="{INK}" stroke-width="3"/>')
    sky_night = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>' + stars +
        f'<circle cx="{mx - 20}" cy="{my}" r="230" fill="url(#mh)"/>' + S.g(moon, filter="wobble-fine"),
        defs=S.lin_grad("g", [(0, P["night"]), (0.6, P["night_light"]), (1, "#6b6f95")]) +
        S.rad_grad("mh", [(0, "#fbf1cf", 0.42), (0.3, "#f3ead0", 0.2), (0.65, "#c9c9dc", 0.06), (1, "#a9aecb", 0)]))
    sc.add("sky_night", sky_night, wc=0.4, motion=lambda t: Tf(alpha=a_night(t)))

    sky_dawn = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="900" ry="360" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#b3b0da"), (0.45, "#e8c4cc"), (0.8, "#f8d6aa"), (1, "#f9ddb0")]) +
        S.rad_grad("r", [(0, "#fff0c4", 0.9), (0.5, "#fcd3a0", 0.45), (1, "#f6c7a0", 0)]))
    sc.add("sky_dawn", sky_dawn, wc=0.5, motion=lambda t: Tf(alpha=a_dawn(t)))

    # hot noon sky; its big bright glow sits BEHIND the sun's rays (the sun is the lightest thing on screen)
    sky_hot = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="900" fill="url(#r)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="420" fill="url(#c)"/>',
        defs=S.lin_grad("g", [(0, "#f0bf62"), (0.5, "#f6d488"), (1, "#fae0a6")]) +
        S.rad_grad("r", [(0, "#fffbe6", 1), (0.25, "#fff1bf", 0.8), (0.6, "#fbd98c", 0.25), (1, "#f6c46a", 0)]) +
        S.rad_grad("c", [(0, "#fffef6", 1), (0.3, "#fff8dc", 0.9), (0.62, "#fff0b8", 0.4), (1, "#ffe9a6", 0)]))
    sc.add("sky_hot", sky_hot, wc=0.5, motion=lambda t: Tf(alpha=a_hot(t)))

    # --- suns (drawn at the document centre so no glow is clipped, then moved into place) -------
    CX, CY = W // 2, H // 2

    def at(pos, m=None):
        """Motion placing a centre-drawn layer at stage position pos (plus an optional extra motion)."""
        base = lambda t: Tf(dx=pos[0] - CX, dy=pos[1] - CY)
        return M.combine(base, m) if m else base

    def sun_svg(cx, cy, r, col, glow, glow_r):
        return S.svg_doc(
            f'<circle cx="{cx}" cy="{cy}" r="{glow_r}" fill="url(#sg)"/>' +
            S.g(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="{S.shade(col, -0.25)}" stroke-width="4"/>'
                f'<circle cx="{cx - r * 0.3:.0f}" cy="{cy - r * 0.3:.0f}" r="{r * 0.35:.0f}" fill="#fffaf0" opacity="0.35"/>',
                filter="wobble"),
            defs=S.rad_grad("sg", [(0, glow, 0.85), (0.35, glow, 0.35), (1, glow, 0)]))

    sink = M.keys([(t_gold0 - 0.2, {"dy": 0}), (t_n1 - 0.1, {"dy": HORIZON - SUN_W[1] + 90})], "sine")
    set_out = lambda t: 1 - M.progress(t, t_n1 - 0.25, t_n1 + 0.2, "sine")   # gone before the night / dawn
    sc.add("sun_day", sun_svg(CX, CY, 78, P["sun"], "#fff3c4", 300),
           motion=at(SUN_W, M.combine(sink, lambda t: Tf(alpha=(1 - M.progress(t, t_gold0 - 0.3, t_gold0 + 0.5,
                                                                                "sine")) * set_out(t)))))
    sc.add("sun_set", sun_svg(CX, CY, 84, "#f59a52", "#ffd08a", 360),
           motion=at(SUN_W, M.combine(sink, lambda t: Tf(alpha=M.progress(t, t_gold0 - 0.3, t_gold0 + 0.5, "sine") *
                                                          set_out(t)))))
    S_HOT = 118 / 82          # the dawn sun grows to exactly the noon disc size as it arrives
    climb = M.keys([(t_n2, {"dx": 0, "dy": 60}), (t_n3 + 0.6, {"dx": -20, "dy": -40}),
                    (t_sun0 + 0.2, {"dx": -70, "dy": -170}),
                    (t_sun1, {"dx": SUN_HOT[0] - SUN_E[0], "dy": SUN_HOT[1] - SUN_E[1], "s": S_HOT})],
                   ["out", "linear", "inout"], pivot=(CX, CY))
    sc.add("sun_dawn", sun_svg(CX, CY, 82, "#f8c070", "#ffe0b0", 330),
           motion=at(SUN_E, M.combine(climb, lambda t: Tf(alpha=_env(t, t_n2, t_n2 + 0.4, t_sun1 - 0.05,
                                                                     t_sun1 + 0.3)))))

    # hot noon sun: opaque saturated flame rays (turning) behind a bright disc
    hx, hy = CX, CY
    ray_d = ""
    for i in range(14):   # long wavy flame rays
        a = 2 * math.pi * i / 14
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for j in range(7):
            r = 150 + j * 32
            off = 14 * math.sin(j * 1.6) * (1 - j / 7)
            w_ = 26 * (1 - j / 7) + 3
            pts.append((r, off, w_))
        left = [(hx + r * ca - (off - w_) * sa, hy + r * sa + (off - w_) * ca) for r, off, w_ in pts]
        right = [(hx + r * ca - (off + w_) * sa, hy + r * sa + (off + w_) * ca) for r, off, w_ in pts]
        ray_d += S.smooth_path(left + right[::-1], closed=True, tension=0.8) + " "
    short = S.rays(hx, hy, 120, 215, n=14, width_deg=11, rot=12.9)     # short wedges between the flames
    rays = S.svg_doc(S.g(
        f'<path d="{short}" fill="#ffd34d" stroke="#b9621c" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="{ray_d}" fill="#ffb83a" stroke="#b9621c" stroke-width="4.5" stroke-linejoin="round"/>',
        filter="wobble"))
    sc.add("sun_rays", rays, wc=0.3,
           motion=at(SUN_HOT, M.combine(lambda t: Tf(rot=12 * t, px=hx, py=hy),
                                        M.breathe(0.03, 0.9, pivot=(hx, hy)),
                                        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.05, t_sun1 + 0.45, "sine")))))
    hot = S.svg_doc(
        f'<circle cx="{hx}" cy="{hy}" r="185" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{hx}" cy="{hy}" r="118" fill="#ffd94f" stroke="#c9741f" stroke-width="6"/>'
            f'<circle cx="{hx}" cy="{hy}" r="90" fill="#fff1a8"/>'
            f'<circle cx="{hx}" cy="{hy}" r="58" fill="#fffae0"/>'
            f'<circle cx="{hx - 34}" cy="{hy - 34}" r="26" fill="#fffef6" opacity="0.9"/>', filter="wobble"),
        defs=S.rad_grad("hg", [(0, "#fffef4", 1), (0.6, "#fff6cf", 0.85), (0.8, "#ffeaa0", 0.4), (1, "#ffe08a", 0)]))
    sc.add("sun_hot", hot, wc=0.4, motion=at(SUN_HOT, M.combine(
        M.breathe(0.035, 1.3, pivot=(hx, hy)),
        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.1, t_sun1 + 0.3, "sine")))))

    # --- clouds (every cloud stays inside the canvas for the whole drift) -------------------------
    clouds = S.svg_doc(S.g(
        S.cloud(700, 150, 290, 88, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
        S.cloud(1640, 290, 240, 76, "#fdf1e2", seed=5, sw=3, shade_fill="#f0d6c4") +
        S.cloud(1870, 118, 300, 92, "#fdf3e4", seed=8, sw=3, shade_fill="#f0d6c4") +
        S.cloud(150, 400, 190, 60, "#fdf1e2", seed=9, sw=3, shade_fill="#f0d6c4"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=M.combine(
        M.drift(vx=-7), lambda t: Tf(alpha=(1 - 0.25 * a_gold(t)) * (1 - 0.45 * a_night(t)) *
                                     (1 - M.progress(t, t_sun0 - 0.2, t_sun0 + 0.45, "sine")))))

    # =============================================================== LAND (static, flattened)
    far = ""
    far += S.path(S.smooth_path([(-80, HORIZON + 8), (150, 600), (420, 585), (700, 610), (950, 590),
                                 (1250, 560), (1550, 585), (1850, 570), (2200, 600)], closed=False) +
                  f" L{W + 80},{HORIZON + 30} L-80,{HORIZON + 30} Z", fill="#e3d3c0", sw=3)
    far += S.path(S.smooth_path([(1000, HORIZON + 6), (1300, 612), (1600, 598), (1900, 615), (2200, 605)],
                                closed=False) + f" L{W + 80},{HORIZON + 30} L1000,{HORIZON + 30} Z", fill="#dfcbb0", sw=3)
    far_svg = S.svg_doc(S.g(far, filter="wobble"))
    sc.add("far_hills", far_svg, wc=0.7)

    city = PR.nineveh_skyline(20, 560, HORIZON + 4, scale=0.42, seed=2, haze=0.42, tint="#efdcbc")
    city_svg = S.svg_doc(city)
    sc.add("city", city_svg, wc=0.6)

    plain = S.path(f"M-80,{HORIZON} L{W + 80},{HORIZON} L{W + 80},{H + 80} L-80,{H + 80} Z", fill="url(#pl)", sw=0)
    plain += f'<path d="M-80,{HORIZON + 2} L{W + 80},{HORIZON + 2}" stroke="{INK}" stroke-width="3" opacity="0.55"/>'
    for i in range(26):   # tiny far shrubs dotting the plain
        x = (i * 263) % 2100 + 20
        y = HORIZON + 14 + (i * 37) % 60
        plain += f'<ellipse cx="{x}" cy="{y}" rx="{9 + i % 4}" ry="5" fill="#b7a274" opacity="0.6"/>'
    # dune A (left, the city side) and the footpath Jonah came along
    plain += _dune([(-80, 742), (200, 718), (480, 734), (760, 786), (980, 856), (1150, 932), (1270, 1010)], "da",
                   rim="#f6e2b4")
    path_d = S.smooth_path([(470, 724), (520, 760), (470, 812), (600, 880), (720, 960), (640, 960), (520, 885),
                            (410, 812), (468, 760), (440, 726)])
    plain += f'<path d="{path_d}" fill="#f5e2b6" opacity="0.85"/>'
    # dune B (right, the sunrise side)
    plain += _dune([(960, 1020), (1100, 930), (1300, 836), (1550, 760), (1800, 726), (2000, 718), (2200, 732)], "db",
                   rim="#f6e0ae")
    defs = (S.lin_grad("pl", [(0, "#efdfb6"), (0.3, "#ead19f"), (1, "#e0bb82")]) +
            S.lin_grad("da", [(0, "#eed4a0"), (0.4, "#e6c48c"), (1, "#d8ad72")]) +
            S.lin_grad("db", [(0, "#ecd09a"), (0.4, "#e3bf86"), (1, "#d4a86c")]))
    plain_svg = S.svg_doc(S.g(plain, filter="wobble"), defs=defs)
    sc.add("plain", plain_svg, wc=0.8)

    # mid-ground: clustered stones of varied shape, dry shrubs and grass clumps (not evenly dotted)
    mid = ""
    for (x, y, s, v) in [(260, 740, 0.4, 2), (640, 772, 0.42, 2), (1600, 768, 0.45, 2), (1880, 742, 0.4, 2),
                         (130, 760, 0.32, 2), (1010, 884, 0.38, 2)]:
        mid += PR.bush(x, y, s, variant=v)
    for (x, y, s) in [(1950, 728, 0.3), (2050, 734, 0.24)]:
        mid += PR.palm_tree(x, y, s, lean=-0.2)
    for (x, y, s) in [(318, 796, 0.42), (1668, 866, 0.5), (1452, 905, 0.42), (950, 838, 0.36)]:
        mid += PR.grass_tuft(x, y, s, variant=1)
    for (x, y, w_, h_, sd) in [(1712, 866, 128, 64, 3), (1792, 872, 62, 34, 13), (1650, 874, 30, 16, 23),
                               (370, 794, 86, 42, 6), (424, 800, 40, 22, 16),
                               (1380, 906, 70, 36, 4), (1426, 910, 34, 17, 14),
                               (905, 842, 46, 24, 7)]:
        mid += _stone(x, y, w_, h_, seed=sd, sw=3, crack=(w_ > 100))
    mid_svg = S.svg_doc(mid)
    sc.add("mid", mid_svg, wc=0.8)

    # the knoll Jonah sits on: cracked dry earth, pebble clusters with shadows
    knoll_pts = [(-80, 1035), (200, 1010), (480, 980), (760, 964), (1100, 959), (1450, 962), (1700, 954),
                 (1920, 930), (2200, 905)]
    kd = S.smooth_path(knoll_pts, closed=False) + f" L{W + 80},{H + 80} L-80,{H + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4)
    rp = [(x, y + 16) for x, y in knoll_pts[1:-1]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f0cf95" stroke-width="14" opacity="0.5"/>'
    for (x, y) in [(260, 1050), (1660, 1040), (1960, 1000), (1000, 1035), (760, 1080)]:
        knoll += (f'<path d="M{x - 70},{y} q70,-16 140,0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.45" stroke-linecap="round"/>')
    for (x, y, s_, sd) in [(400, 1012, 70, 1), (640, 990, 50, 2), (1520, 1012, 60, 3), (1870, 990, 55, 4),
                           (1090, 1040, 46, 5)]:
        knoll += _cracks(x, y, s_, seed=sd)
    sc.add("knoll", S.svg_doc(S.g(knoll, filter="wobble"),
                              defs=S.lin_grad("kn", [(0, "#e6bc7c"), (0.3, "#dcab69"), (1, "#c38c55")])), wc=0.9)
    pebbles = (_pebbles(470, 1000, 1.0, seed=3) + _pebbles(1790, 996, 1.1, seed=4, n=2) +
               _pebbles(640, 986, 0.8, seed=5, n=2) + _pebbles(1460, 1016, 0.9, seed=6, n=2))
    sc.add("pebbles", S.svg_doc(S.g(pebbles, filter="wobble-fine")), wc=0.8)

    # foreground framing: corner stones and a tall dry shrub on the left edge (above the subtitle zone)
    fg = ""
    fg += _rock(150, 1160, 290, 130, seed=31) + _rock(360, 1180, 160, 72, seed=32)
    fg += _rock(1960, 1165, 250, 115, seed=33) + _rock(1790, 1185, 140, 64, seed=34)
    fg += _stone(40, 925, 150, 84, seed=35, sw=4) + PR.bush(92, 912, 1.2, variant=2)
    fg += PR.bush(2072, 1062, 1.05, variant=2)
    sc.add("fg_rocks", S.svg_doc(S.g(fg, filter="wobble")), wc=0.9)

    # the lizard's basking stone (behind it) ---------------------------------------------------------
    sc.add("liz_rock", S.svg_doc(S.g(_stone(LIZ[0] - 4, 994, 138, 50, seed=41, sw=4, crack=True),
                                     filter="wobble-fine")), wc=0.8)

    # =============================================================== DOVES flying home at sunset (behind
    # the plant and the booth; gone before dusk turns to night)
    dove_frames = [S.svg_doc(PR.dove(1900, 300, 0.62, -1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    for i, (t0, dy, ph) in enumerate([(l1.end - 1.2, 0, 0), (l1.end - 0.85, 80, 2)]):
        dur = 2.3
        sc.add(f"dove{i}", dove_frames, frame_at=flap(11, ph), wc=0.4, motion=M.combine(
            M.keys([(t0, {"dx": 330, "dy": dy - 40}), (t0 + dur, {"dx": -2150, "dy": dy + 60})], "linear"),
            M.bob(10, 0.6, ph * 0.1),
            lambda t: Tf(alpha=1 - M.progress(t, t_n0 - 0.2, t_n0 + 0.2, "sine"))))

    # =============================================================== LIZARD (basks, then runs for cover)
    liz_frames = [S.svg_doc(_lizard(LIZ[0], LIZ[1], 0.72, legs=k)) for k in (0, 1)]

    def liz_frame(t):
        return 0.0 if t < t_liz else float(int((t - t_liz) * 16) % 2)

    def liz_motion(t):
        if t < t_liz:
            u = (t + 0.9) % 2.8                   # lizard "push-ups": two quick bobs every few seconds
            b = math.sin(math.pi * u / 0.2) if u < 0.4 else 0.0
            b = abs(b)
            return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)
        v = t - t_liz
        # scurries off its stone and ducks behind the next one (tail last)
        return Tf(dx=158 * M.ease("out")(min(1.0, v / 0.5)), dy=38 * M.progress(v, 0.08, 0.4, "sine"),
                  alpha=1 - M.progress(v, 0.4, 0.62, "sine"))

    sc.add("lizard", liz_frames, frame_at=liz_frame, motion=liz_motion, wc=0.5)
    sc.add("liz_rock2", S.svg_doc(S.g(_stone(LIZ[0] + 150, 1002, 104, 58, seed=43, sw=4), filter="wobble-fine")),
           wc=0.8)

    # booth + its soft contact shadow (afternoon light from the west, shadow falls east)
    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{INK}" opacity="0.16" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    booth_svg = S.svg_doc(booth)
    sc.add("booth", booth_svg, wc=0.8)

    # =============================================================== CANOPY SHADE (ground only)
    shade_amt = lambda t: M.progress(t, t_shade0, t_shade1, "sine") * (1 - M.progress(t, t_with0, t_with1, "sine"))
    gshade = S.svg_doc(
        f'<ellipse cx="{XP + 330}" cy="{GY + 8}" rx="560" ry="40" fill="#8f7c8a" opacity="0.55" filter="url(#soft)"/>')
    sc.add("ground_shade", gshade, wc=0, blend="multiply", motion=lambda t: Tf(alpha=shade_amt(t)))

    # --- God's warm light on the sprout (normal blend: a soft cream beam) -------------------------
    beam = S.svg_doc(
        S.g(f'<path d="M{XP - 640},-60 L{XP - 260},-60 L{XP + 170},{GY} L{XP - 190},{GY} Z" fill="url(#bg)"/>',
            filter="blur-md") +
        f'<ellipse cx="{XP}" cy="{GY - 80}" rx="300" ry="230" fill="url(#rg)"/>',
        defs=S.lin_grad("bg", [(0, "#fff6d6", 0.0), (0.35, "#fff3c8", 0.35), (1, "#ffefb8", 0.55)]) +
        S.rad_grad("rg", [(0, "#fff8dc", 0.85), (0.5, "#fff0c0", 0.35), (1, "#ffe9a8", 0)]))
    sc.add("god_light", beam, wc=0,
           motion=lambda t: Tf(alpha=_env(t, t_grow0 - 0.4, t_grow0 + 0.3, t_grow1 + 0.1, t_shade1 + 0.3) *
                               (0.85 + 0.15 * math.sin(t * 4))))

    # =============================================================== CASTOR PLANT (flipbook)
    g_vals = [i / 24 for i in range(25)]
    plant_frames = [S.svg_doc(PR.castor_plant(XP, GY, SP, growth=g, side=1, seed=2)) for g in g_vals]
    plant_frames += [S.svg_doc(PR.castor_plant(XP, GY, SP, growth=1, bite=b, side=1, seed=2)) for b in (0.34, 0.67, 1.0)]
    w_vals = [i / 12 for i in range(1, 13)]
    plant_frames += [S.svg_doc(PR.castor_plant(XP, GY, SP, growth=1, wither=w, bite=1.0, side=1, seed=2))
                     for w in w_vals]
    NG = len(g_vals)

    def plant_frame(t):
        if t < t_bite0:
            f = (NG - 1) * M.progress(t, t_grow0, t_grow1, "inout")
        elif t < t_with0:
            f = NG - 1 + 3 * M.progress(t, t_bite0, t_bite1, "linear")
        else:
            f = NG + 2 + len(w_vals) * M.progress(t, t_with0, t_with1, "inout")
        return _sharp(f, 0.5)

    def plant_motion(t):
        a = M.progress(t, t_grow0 - 0.15, t_grow0 + 0.2, "sine")
        s = 0.6 + 0.4 * M.progress(t, t_grow0 - 0.15, t_grow0 + 0.35, "back")
        # the sway rests through the night so the plant matches the night-grade silhouette mask exactly
        rot = 0.7 * math.sin(2 * math.pi * t / 3.4) * (1 - _env(t, t_n0 - 0.45, t_n0, t_n3, t_n3 + 0.45))
        wind = M.progress(t, t_wind - 0.3, t_wind + 0.6, "sine")
        rot = rot * (1 - wind) + wind * (-2.0 + 1.4 * math.sin(2 * math.pi * t / 0.95) + 0.5 * math.sin(t * 9.1))
        return Tf(rot=rot, sx=s, sy=s, alpha=a, px=XP, py=GY)

    sc.add("castor", plant_frames, frame_at=plant_frame, motion=plant_motion, wc=0.9)

    # --- hot east wind swirls: BEHIND Jonah and in bands clear of his head ---------------------------
    for i, (y, ln, ph) in enumerate([(470, 360, 0.0), (880, 320, 0.45), (300, 260, 0.8), (600, 230, 1.15)]):
        x0 = 1700
        sw_svg = S.svg_doc(S.g(_swirl(x0, y, ln), filter="wobble-fine"))

        def swirl_motion(t, ph=ph):
            if t < t_wind - 0.2:
                return Tf(alpha=0.0)
            u = ((t - t_wind + 0.2 + ph) % 1.6) / 1.6
            a = math.sin(math.pi * u) * M.progress(t, t_wind - 0.2, t_wind + 0.3)
            return Tf(dx=500 - 1500 * u, dy=12 * math.sin(6 * u), alpha=0.9 * a)

        sc.add(f"swirl{i}", sw_svg, motion=swirl_motion, wc=0.2)

    # =============================================================== JONAH (flipbook of poses)
    poses = [("sit_sulk", "angry"), ("sit", "surprised"), ("sit_happy", "happy"), ("sit", "peaceful"),
             ("sit", "sad"), ("sit_faint", "tired"), ("sit_faint", "dizzy")]
    jshadow = CH.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)
    jframes = [S.svg_doc(jshadow + CH.jonah(XJ, GY, SP, -1, pose=p, expr=e)) for p, e in poses]
    # (time, kind, hop strength, pop lines, dust poof). Pose changes are near-hard cuts hidden by a
    # squash-and-hop; expression-only changes keep a soft crossfade.
    switch = [(t_grow0 + 0.45, "pose", 1.0, True, True),       # sulk -> sit (surprised by the sprout)
              (t_happy, "pose", 1.0, True, True),              # -> sit_happy in the shade
              (t_night, "pose", 0.45, False, False),           # -> asleep, peaceful (middle of the night)
              (t_with0 + 0.25, "expr", 0, False, False),       # peaceful -> sad
              (l4.start + 0.3, "pose", 0.7, False, True),      # -> sit_faint (slumps in the heat)
              (t_faint, "expr", 0, False, False)]              # tired -> dizzy
    def jonah_frame(t):
        f = 0.0
        for i, (ts, kind, *_r) in enumerate(switch):
            if kind == "pose":
                if t >= ts:          # hard cut (a 1-frame blend still shows as a double exposure)
                    f = float(i + 1)
            elif t >= ts:
                f = i + M.progress(t, ts, ts + 0.22, "sine")
        return f

    def hop(t):
        """Squash (before the cut) -> stretch + little hop (after it) -> settle, ~0.25 s."""
        sy, dy = 1.0, 0.0
        for ts, kind, amp, *_r in switch:
            if kind != "pose":
                continue
            u = t - ts
            if -0.09 <= u <= 0.17:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.17, "sine")
                dy = -14 * amp * math.sin(math.pi * _clamp((u + 0.01) / 0.18))
        return sy, dy

    huffs = [l0.start + 0.35, l0.start + 1.55, l0.start + 2.75]

    def jonah_motion(t):
        s = 1 + 0.012 * math.sin(2 * math.pi * t / 3.0)
        sy = s
        rot = 0.0
        dy = 0.0
        for th in huffs:          # grumpy huff: a little squash-and-stretch
            u = t - th
            if 0 <= u < 0.45:
                sy *= 1 - 0.035 * math.sin(math.pi * u / 0.45)
        if t_happy <= t < t_night:   # happy rocking (settles as night falls)
            k = M.progress(t, t_happy, t_happy + 0.4) * (1 - M.progress(t, t_n0, t_n1))
            rot = k * 1.6 * math.sin(2 * math.pi * (t - t_happy) / 1.1)
            dy = -k * 4 * abs(math.sin(2 * math.pi * (t - t_happy) / 1.1))
        if t >= t_faint:           # dizzy wobble
            k = M.progress(t, t_faint, t_faint + 0.6)
            rot = k * 2.4 * math.sin(2 * math.pi * (t - t_faint) / 1.8)
        hsy, hdy = hop(t)
        sy *= hsy
        sx = s * (1 + 0.5 * (1 - hsy))
        return Tf(dy=dy + hdy, rot=rot, sx=sx, sy=sy, px=XJ, py=GY)

    sc.add("jonah", jframes, frame_at=jonah_frame, motion=jonah_motion, wc=0.6)

    # canopy shade ON JONAH ONLY: a cool flat-colour copy of his own silhouette, multiplied
    tint_frames = [S.svg_doc(S.g(CH.jonah(XJ, GY, SP, -1, pose=p, expr=e), filter="flat"), defs=FLAT_DEFS)
                   for p, e in poses]
    sc.add("jonah_shade", tint_frames, frame_at=jonah_frame, wc=0, blend="multiply",
           motion=M.combine(jonah_motion, lambda t: Tf(alpha=0.42 * shade_amt(t))))

    # --- pose-change pop: little dust poofs at his sides + emphasis lines around his head ------------
    dust_svg = ""
    for bx, sgn in ((XJ - 178, -1), (XJ + 168, 1)):
        circ = [(0, 0, 17), (sgn * 20, -6, 13), (-sgn * 16, -4, 12), (sgn * 4, -16, 12)]
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{GY - 6 + dy}" r="{r}" fill="#f3e4c4" stroke="{P["ink_soft"]}" '
                            f'stroke-width="6"/>' for dx, dy, r in circ)
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{GY - 6 + dy}" r="{r}" fill="#f3e4c4"/>' for dx, dy, r in circ)
    dust_ts = [ts for ts, kind, _a, _l, dust in switch if kind == "pose" and dust]

    def poof_motion(t):
        for ts in dust_ts:
            u = t - ts
            if 0 <= u < 0.45:
                s = 0.5 + 0.7 * M.ease("out")(u / 0.45)
                return Tf(dy=-6 * M.ease("out")(u / 0.45), sx=s, sy=s,
                          alpha=0.9 * (1 - M.progress(u, 0.12, 0.45, "sine")), px=XJ, py=GY)
        return Tf(alpha=0.0)

    sc.add("jpop_dust", S.svg_doc(S.g(dust_svg, filter="wobble-fine")), motion=poof_motion, wc=0.3)

    lines_svg = ""
    for k in range(5):
        a = math.radians(-160 + k * 35)
        r0, r1 = 96, 132
        lines_svg += (f'<path d="M{CX + r0 * math.cos(a):.1f},{CY + r0 * math.sin(a):.1f} '
                      f'L{CX + r1 * math.cos(a):.1f},{CY + r1 * math.sin(a):.1f}" stroke="{P["ink_soft"]}" '
                      f'stroke-width="7" stroke-linecap="round"/>')
    pop_pts = []
    for i, (ts, kind, _a, lines, _d) in enumerate(switch):
        if lines:
            hp = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose=poses[i + 1][0])["head"]
            pop_pts.append((ts, hp))

    def lines_motion(t):
        for ts, (px_, py_) in pop_pts:
            u = t - ts
            if 0 <= u < 0.34:
                s = 0.82 + 0.3 * M.ease("out")(u / 0.34)
                return Tf(dx=px_ - CX, dy=py_ - CY, sx=s, sy=s,
                          alpha=1 - M.progress(u, 0.12, 0.34, "sine"), px=CX, py=CY)
        return Tf(alpha=0.0)

    sc.add("jpop_lines", S.svg_doc(S.g(lines_svg, filter="wobble-fine")), motion=lines_motion, wc=0.2)

    # --- grumpy steam puffs + anger mark on each huff (line 0) ---------------------------------------
    hp = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit_sulk")
    hx0, hy0 = hp["head"]
    for side_, (ox, oy) in enumerate([(-96, 4), (94, 12)]):
        cx, cy = hx0 + ox, hy0 + oy
        sgn = -1 if side_ == 0 else 1

        def puff_motion(t, cx=cx, cy=cy, sgn=sgn, ph=side_ * 0.07):
            for th in huffs:
                u = t - th - ph
                if 0 <= u < 0.8:
                    a = min(1.0, u / 0.05) * (1 - M.progress(u, 0.4, 0.8, "sine"))
                    if u < 0.12:
                        s = 0.3 + 0.8 * M.ease("out")(u / 0.12)
                    else:
                        s = 1.1 - 0.1 * M.progress(u, 0.12, 0.3, "sine")
                    e = M.ease("out")(min(1.0, u / 0.8))
                    return Tf(dx=sgn * 26 * e, dy=-46 * e, sx=s, sy=s, alpha=a, px=cx, py=cy)
            return Tf(alpha=0.0)

        sc.add(f"puff{side_}", S.svg_doc(_puff(cx, cy, 27)), motion=puff_motion, wc=0.3)

    ax, ay = hx0 + 56, hy0 - 60

    def anger_motion(t):
        for th in huffs:
            u = t - th + 0.04
            if 0 <= u < 0.95:
                if u < 0.1:
                    s = 1.25 * M.ease("out")(u / 0.1)
                else:
                    s = 1.25 - 0.25 * M.progress(u, 0.1, 0.24, "sine") + 0.06 * math.sin(u * 30) * (1 - u)
                return Tf(sx=s, sy=s, alpha=1 - M.progress(u, 0.65, 0.95, "sine"), px=ax, py=ay)
        return Tf(alpha=0.0)

    sc.add("anger", S.svg_doc(_anger(ax, ay, 22)), motion=anger_motion, wc=0.2)

    # =============================================================== WORM
    worm_frames = [S.svg_doc(PR.worm(XW, GY + 2, SW, 1, crawl=c, chomp=ch))
                   for c, ch in [(1.0, 0), (0.5, 0), (0, 0), (0, 0.5), (0, 1.0)]]
    NCYC, STRIDE = 2, 75.0          # two inchworm steps out from behind the pebble
    X_START = -NCYC * STRIDE

    def worm_state(t):
        """(flipbook frame, dx). Stepped frames (no crossfade): crawl arches 1,0,1,2 and reaches forward only
        while stretching flat; chomp 2,3,4,3 at 6 fps with the head 7 px back so the notch shows."""
        if t < t_worm0:
            return 2.0, X_START
        if t < t_worm1:
            v = (t - t_worm0) / (t_worm1 - t_worm0) * NCYC
            k, u = int(v), v - int(v)
            frame = (1, 0, 1, 2)[min(3, int(u * 4))]
            return float(frame), X_START + STRIDE * (k + M.progress(u, 0.6, 1.0, "sine"))
        if t < t_bite0:
            return 2.0, 0.0
        back = -7.0 * M.progress(t, t_bite0 - 0.1, t_bite0 + 0.05, "sine")
        if t < t_chomp1:
            frame = (2, 3, 4, 3)[int((t - t_bite0) * 6.0) % 4]
            return float(frame), back + (2.5 if frame == 4 else 0.0)
        return 2.0, -7.0 * (1 - M.progress(t, t_chomp1, t_chomp1 + 0.3, "sine"))

    def worm_motion(t):
        _f, dx = worm_state(t)
        dy = -3 * abs(math.sin(t * 6)) * M.progress(t, t_chomp1 + 0.3, t_chomp1 + 0.6) if t > t_chomp1 else 0.0
        return Tf(dx=dx, dy=dy, alpha=M.progress(t, t_worm0, t_worm0 + 0.2, "sine"))

    sc.add("worm", worm_frames, frame_at=lambda t: worm_state(t)[0], motion=worm_motion, wc=0.5)
    # pebble the worm crawls out from behind
    sc.add("pebble", S.svg_doc(S.g(_rock(XW + X_START - 40, GY + 16, 130, 62, seed=21, sw=4), filter="wobble-fine")),
           wc=0.8)

    # crumbs nibbled out of the notch (one little spray each time the mouth opens)
    CR_K = 3
    cbx0, cby0 = int(NOTCH[0] - 150), int(NOTCH[1] - 80)
    cw, ch = 230, int(GY + 24 - cby0)
    crumbs = []
    nb = int((t_chomp1 - t_bite0) * 6.0 / 4) + 1
    for c in range(nb):
        tc = t_bite0 + (4 * c + 2) / 6.0
        if tc > t_chomp1:
            break
        for j in range(3):
            rnd = random.Random(100 + c * 10 + j)
            vx, vy = rnd.uniform(-25, 85), rnd.uniform(150, 230)     # pop up and fall in front of the stem
            g_ = 1100.0
            drop = GY + 3 - NOTCH[1]
            u_land = (vy + math.sqrt(vy * vy + 2 * g_ * drop)) / g_
            crumbs.append((tc + j * 0.05, vx, vy, g_, u_land, rnd.uniform(3.6, 6.0),
                           ("#f4eecb", "#9ccc6a", "#6ea84b")[j % 3]))

    def crumb_fn(t):
        if t < t_bite0 + 0.2 or t > t_chomp1 + 1.6:
            return None
        im = Image.new("RGBA", (cw * CR_K, ch * CR_K), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        any_ = False
        for t0, vx, vy, g_, ul, r, col in crumbs:
            u = t - t0
            if u < 0 or u > ul + 0.9:
                continue
            uu = min(u, ul)
            x = NOTCH[0] - 4 + vx * uu
            y = NOTCH[1] - vy * uu + 0.5 * g_ * uu * uu
            a = 1 - M.progress(u, ul + 0.4, ul + 0.9)
            if a <= 0.02:
                continue
            any_ = True
            px_, py_ = (x - cbx0) * CR_K, (y - cby0) * CR_K
            rr = r * CR_K
            ia = int(255 * a)
            d.ellipse([px_ - rr - 5, py_ - rr * 0.8 - 5, px_ + rr + 5, py_ + rr * 0.8 + 5], fill=(75, 52, 38, ia))
            rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
            d.ellipse([px_ - rr, py_ - rr * 0.8, px_ + rr, py_ + rr * 0.8], fill=(*rgb, ia))
        if not any_:
            return None
        return im.resize((cw, ch), Image.LANCZOS), (cbx0, cby0)

    sc.add_dynamic("crumbs", crumb_fn)

    # =============================================================== DIZZY STARS
    ftop = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit_faint")["head_top"]
    ocx, ocy = ftop[0] + 4, ftop[1] - 26
    for i in range(3):
        def orbit(t, ph=i / 3):
            a = 2 * math.pi * (t * 0.9 + ph)
            k = M.progress(t, t_faint + 0.2, t_faint + 0.7, "sine")
            s = 0.85 + 0.2 * math.sin(a)
            return Tf(dx=80 * math.cos(a), dy=20 * math.sin(a), sx=s, sy=s, alpha=k, px=ocx, py=ocy)
        sc.add(f"dizzy{i}", S.svg_doc(S.g(_star(ocx, ocy, 22, "#ffd84a", sw=4), filter="wobble-fine")), motion=orbit,
               wc=0.3)

    # =============================================================== FOREGROUND grass (sways; small crops)
    def grass_frame_fn(ph):
        def f(t):
            wind = M.progress(t, t_wind - 0.3, t_wind + 0.5, "sine")
            calm = 1 + 0.7 * math.sin(2 * math.pi * (t / 2.6 + ph))
            gust = 2.4 + 0.6 * math.sin(2 * math.pi * (t / 0.8 + ph))
            return calm * (1 - wind) + gust * wind
        return f

    for gi, tufts in enumerate([[(40, 1115, 1.15, 1), (265, 1105, 0.95, 1), (450, 1160, 1.0, 0)],
                                [(1720, 1140, 1.0, 1), (1870, 1108, 0.95, 1)],
                                [(560, 1000, 0.65, 1), (196, 928, 0.8, 1)],
                                [(1520, 990, 0.65, 1), (1700, 985, 0.6, 1)]]):
        frames = [S.svg_doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts))
                  for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", frames, frame_at=grass_frame_fn(gi * 0.23), wc=0.7)

    # --- withered leaves dropping, then blown away by the east wind (toward the city) ---------------
    for i, (lx, ly, land_dx, tdrop) in enumerate([(XP + 250, GY - 560, -70, 0.25), (XP + 100, GY - 420, -60, 0.55),
                                                   (XP + 640, GY - 480, 60, 0.8)]):
        col = [P["leaf_dry"], "#a7834a", P["leaf_dead"]][i]
        leaf = S.svg_doc(_dead_leaf(lx, ly, 28, col, curl=0.2 * i))
        tf0 = t_with0 + tdrop
        tb0 = t_wind + 0.05 + 0.3 * i
        fall_y = GY - 10 - ly

        def drop_motion(t, tf0=tf0, tb0=tb0, i=i, land_dx=land_dx, fall_y=fall_y):
            if t < tf0:
                return Tf(alpha=0.0)
            u = min(1.0, (t - tf0) / 1.5)          # flutter down
            k = M.ease("in")(u) * 0.6 + 0.4 * u
            dx = land_dx * u + 40 * math.sin(u * 7 + i) * (1 - u)
            dy = fall_y * k
            rot = 90 * u + 35 * math.sin(u * 8 + i) * (1 - u)
            a = min(1.0, (t - tf0) / 0.15)
            if t > tb0:                            # blown away by the east wind
                v = t - tb0
                dx += -900 * v - 150 * v * v
                dy += -60 * math.sin(min(v, 1.2) * 2.6) - 30 * v
                rot += -300 * v
                a *= 1 - M.progress(v, 1.8, 2.3)
            return Tf(dx=dx, dy=dy, rot=rot, alpha=a)

        sc.add(f"drop{i}", leaf, motion=drop_motion, wc=0.5)

    for i in range(7):
        col = [P["leaf_dead"], P["leaf_dry"], "#a7834a"][i % 3]
        sx0, sy0 = XP + 160 + (i * 97) % 420, GY - 640 + (i * 61) % 260
        leaf = S.svg_doc(_dead_leaf(sx0, sy0, 26 + (i % 3) * 5, col, curl=0.25 * (i % 2)))
        tl0 = t_wind + 0.1 + i * 0.42

        def leaf_motion(t, tl0=tl0, i=i, sx0=sx0, sy0=sy0):
            u = t - tl0
            if u < 0 or u > 2.6:
                return Tf(alpha=0.0)
            dx = -850 * u - 120 * u * u
            dy = 150 * u + 45 * math.sin(u * 5 + i)
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 2.2, 2.6))
            return Tf(dx=dx, dy=dy, rot=-260 * u * (1 + 0.2 * (i % 2)), alpha=a, px=sx0, py=sy0)

        sc.add(f"leaf{i}", leaf, motion=leaf_motion, wc=0.5)

    # =============================================================== CAMERA
    # few long sine-eased moves: slow drift in (lines 0-2), one push-in to the stem base for the worm and
    # the bite (plant scale ~1.9 on screen, Jonah's face still in frame), hold, one pull-back that settles as
    # the noon sun arrives, then a very slow push toward Jonah while he faints.
    t_push0, t_push1 = l2.start + 0.15, t_bite0 + 0.2
    t_pull0, t_pull1 = t_bite1 - 0.05, l4.start + 0.85
    sc.camera = M.cam_keys([
        (0.0, Cam(1062, 600, 2000)),
        (t_push0, Cam(1050, 604, 1960)),
        (t_push1, Cam(990, 728, 1350)),
        (t_pull0, Cam(986, 730, 1332)),
        (t_pull1, Cam(1110, 586, 1800)),
        (T, Cam(1135, 582, 1765)),
    ], "sine")

    # =============================================================== FX
    _nm = {}
    mask_svgs = [far_svg, city_svg, plain_svg, mid_svg, booth_svg, plant_frames[NG - 1]]

    def night_mask():
        """Stage-space alpha of everything that stands in front of the sky during the night (the same SVGs
        as the layers, so the raster cache is hit). Built on first use only."""
        if "m" not in _nm:
            acc = None
            for svg in mask_svgs:
                im = raster.rasterize(svg.replace(BOIL_TOKEN, "1"), W, H)
                a = np.asarray(im.getchannel("A"), np.float32) / 255.0
                acc = a if acc is None else np.maximum(acc, a)
            _nm["m"] = cv2.GaussianBlur(acc, (0, 0), 1.0)
        return _nm["m"]

    def grade(frame, t, view):
        mul = np.array([1.0, 1.0, 1.0])
        for col, k in [((255, 216, 172), _env(t, t_gold0 - 0.3, t_gold0 + 0.3, t_n0, t_n1)),
                       ((246, 220, 230), 0.8 * _env(t, t_n2, t_n3, t_bite0 + 0.5, t_sun1)),
                       ((255, 224, 184), M.progress(t, t_sun0 + 0.2, t_sun1 + 0.4, "sine"))]:
            if k > 0:
                mul *= 1 - (1 - np.array(col, float) / 255.0) * k
        kn = _env(t, t_n0, t_n1, t_n2, t_n3)
        if kn <= 0.003 and (mul >= 0.998).all():
            return frame
        arr = np.asarray(frame)
        if kn <= 0.003:
            arr = cv2.multiply(arr, (float(mul[0]), float(mul[1]), float(mul[2]), 1.0))
            return Image.fromarray(arr, "RGBA")
        # night: deep blue land (everything in front of the sky, incl. the city, booth and plant) and a gentler
        # grade on the already dark night sky, separated by the land silhouette mask
        f_sky = (mul * (1 - (1 - np.array((196, 202, 236), float) / 255.0) * 0.5 * kn)).astype(np.float32)
        f_land = (mul * (1 - (1 - np.array((48, 64, 150), float) / 255.0) * 0.92 * kn)).astype(np.float32)
        A = view.M[:2].astype(np.float64).copy()
        A[:, 2] += 0.5 * (A[:, 0] + A[:, 1]) - 0.5
        m = cv2.warpAffine(night_mask(), A, (arr.shape[1], arr.shape[0]), flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)
        rgb = arr[..., :3].astype(np.float32)
        rgb *= f_sky + m[..., None] * (f_land - f_sky)
        out = arr.copy()
        out[..., :3] = np.clip(rgb + 0.5, 0, 255).astype(np.uint8)
        return Image.fromarray(out, "RGBA")

    rng2 = np.random.default_rng(17)
    NDUST = 150
    dx0 = rng2.uniform(0, 1, NDUST)
    dy0 = rng2.uniform(0.2, 1.0, NDUST)
    dsp = rng2.uniform(0.7, 1.4, NDUST)
    dln = rng2.uniform(24, 100, NDUST)
    dal = rng2.uniform(80, 170, NDUST)
    SH = 4      # cv2 sub-pixel shift bits

    def dust(frame, t, view):
        """Anti-aliased blowing sand (cv2 LINE_AA into a premultiplied overlay), thinner over Jonah."""
        k = M.progress(t, t_wind - 0.4, t_wind + 0.6, "sine")
        if k <= 0.01:
            return frame
        arr = np.array(frame)
        Hf, Wf = arr.shape[:2]
        ov = np.zeros((Hf, Wf, 4), np.uint8)
        jx, jy = view.to_out(XJ - 10, GY - 150)
        rx, ry = 230 * view.scale, 240 * view.scale
        for i in range(NDUST):
            x = (dx0[i] * (Wf + 300) - t * 1100 * dsp[i]) % (Wf + 300) - 150
            y = dy0[i] * Hf + 18 * math.sin(t * 3 + i)
            dd = math.hypot((x - jx) / rx, (y - jy) / ry)
            fig = 0.25 + 0.75 * _clamp((dd - 0.75) / 0.6)
            a = dal[i] * k * (0.5 + 0.5 * dy0[i]) * fig
            if a < 4:
                continue
            if i % 3 == 0:
                col = (214, 172, 112)
                r = 2 + (i % 4)
                cv2.circle(ov, (int(x * 16), int(y * 16)), int(r * 16),
                           tuple(c * a / 255 for c in col) + (a,), -1, cv2.LINE_AA, SH)
            else:
                col = (250, 230, 188)
                cv2.line(ov, (int(x * 16), int(y * 16)), (int((x + dln[i]) * 16), int((y - dln[i] * 0.08) * 16)),
                         tuple(c * a / 255 for c in col) + (a,), 2 + i % 3, cv2.LINE_AA, SH)
        inv = cv2.merge([255 - ov[..., 3]] * 3)
        arr[..., :3] = cv2.add(cv2.multiply(arr[..., :3], inv, scale=1 / 255.0), ov[..., :3])
        return Image.fromarray(arr, "RGBA")

    def shimmer(frame, t, view):
        k = M.progress(t, t_sun1 - 0.2, t_sun1 + 0.6, "sine")
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i, (bx, by) in enumerate([(300, 930), (1600, 900), (1880, 870), (560, 860), (1380, 1010), (180, 1060)]):
            u = ((t * 0.6 + i * 0.37) % 1.0)
            ox, oy = view.to_out(bx, by - 70 * u)
            a = int(150 * k * math.sin(math.pi * u))
            sc_ = view.scale
            for j in range(3):
                x0 = ox + (j - 1) * 20 * sc_
                pts = [(x0 + 7 * sc_ * math.sin(q * 1.1 + t * 7 + i), oy - q * 9 * sc_) for q in range(9)]
                d.line(pts, fill=(255, 248, 226, a), width=max(2, int(4 * sc_)), joint="curve")
        frame.alpha_composite(ov)
        return frame

    sc.fx = [
        FX.sparkles((XP - 300, GY - 760, XP + 640, GY - 20), count=38, t0=t_grow0 - 0.1, t1=l1.end + 0.4,
                    color=(255, 238, 160), size=(10, 24), period=1.2, drift=-10, seed=3),
        FX.motes((200, 200, 1900, 900), count=26, t0=0, t1=t_gold1, color=(255, 246, 214), alpha=110),
        grade,
        shimmer,
        dust,
        FX.vignette(lambda t: 0.25 * M.progress(t, t_sun1, t_faint + 0.8, "sine") *
                    (0.85 + 0.15 * math.sin(t * 3.2)), color=(150, 72, 24)),
    ]

    # =============================================================== SOUND
    sc.sfx("wind_soft", 0, dur=t_sun0 + 0.6, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("sparkle", t_grow0 - 0.1, gain_db=-9)
    sc.sfx("grow", t_grow0, dur=None, gain_db=-7)
    sc.sfx("sparkle", t_grow1 - 0.4, gain_db=-12, pan=0.2)
    sc.sfx("birds", l1.end - 0.3, dur=t_n0 + 0.4 - (l1.end - 0.3), gain_db=-14, fade_in=0.3, fade_out=0.5, pan=-0.2)
    sc.sfx("crunch", t_bite0, gain_db=-6, pan=-0.2)
    sc.sfx("wither", t_with0, gain_db=-8)
    sc.sfx("wind_hot", t_wind - 0.4, dur=T - t_wind + 1.2, gain_db=-11, fade_in=0.6, fade_out=0.8)
    sc.sfx("heat", t_sun0 + 0.2, dur=T - t_sun0 + 0.6, gain_db=-13, fade_in=0.8, fade_out=0.8)
    return sc
