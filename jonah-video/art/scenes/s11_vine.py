"""Scene 11 — the castor plant (Jonah 4:1-8).

A dry hillside east of Nineveh (the city small on the western horizon, left). Jonah sits in his little
booth facing the city. He sulks (grumpy puffs); God makes a castor plant spring up beside the booth
(golden light, sparkles) and its big leaves shade him; he is very happy in a golden evening. A quick
night passes (stars), and at dawn a little worm crawls out and nibbles the stem; the plant withers. The
sun climbs overhead and blazes, a hot east wind blows sand and dead leaves, and Jonah grows faint.

Every event is keyed to ctx.lines[i] (start/end) so it follows the narration.
"""
import math

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
from engine.scene import Scene

# ------------------------------------------------------------------ layout (stage px)
GY = 962            # ground line of the knoll (plant root, booth, Jonah)
SP = 1.3            # plant / booth / Jonah scale
XP = 830            # castor root
XB = XP + PR.CASTOR_BOOTH_DX * SP   # booth centre (canopy arches over its roof)
XJ = XB + 28        # Jonah (sitting, facing the city on the left)
SW = 1.55           # worm scale (a touch big so a child can see it)
XW = XP - (12 * SP + 40 * SW)       # worm anchor with its mouth in the stem notch
HORIZON = 640

SUN_W = (360, 215)      # afternoon sun (west, over the city)
SUN_E = (1900, 690)     # dawn sun (east, rising behind the hills)
SUN_HOT = (1500, 170)   # noon sun, high over Jonah's head


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
    """Little cartoon puff of grumpiness (steam cloud)."""
    body = ""
    pts = [(-0.55, 0.1, 0.55), (0.0, -0.25, 0.7), (0.55, 0.05, 0.55), (0.05, 0.3, 0.5)]
    for dx, dy, k in pts:
        body += f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#efe7da" ' \
                f'stroke="{P["ink"]}" stroke-width="7"/>'
    for dx, dy, k in pts:
        body += f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#efe7da"/>'
    body += f'<circle cx="{cx - 0.15 * r:.1f}" cy="{cy - 0.4 * r:.1f}" r="{0.18 * r:.1f}" fill="#fffaf0" opacity="0.8"/>'
    return S.g(body, filter="wobble-fine")


def _star(cx, cy, r, fill="#f6d35a", sw=3):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    st = f'stroke="{P["ink"]}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}" {st}/>'


def _dead_leaf(cx, cy, r, col, curl=0.0):
    """A dry, slightly curled leaf with a midrib and stalk (blown by the hot wind)."""
    k = 1 + curl
    d = (f"M{cx:.1f},{cy - r:.1f} C{cx + r * 0.75 * k:.1f},{cy - r * 0.55:.1f} {cx + r * 0.7:.1f},{cy + r * 0.55:.1f} "
         f"{cx:.1f},{cy + r:.1f} C{cx - r * 0.55:.1f},{cy + r * 0.5:.1f} {cx - r * 0.75 / k:.1f},{cy - r * 0.5:.1f} "
         f"{cx:.1f},{cy - r:.1f} Z")
    rib = (f'<path d="M{cx:.1f},{cy + r * 1.35:.1f} Q{cx + r * 0.12:.1f},{cy:.1f} {cx:.1f},{cy - r * 0.8:.1f}" '
           f'fill="none" stroke="{P["ink"]}" stroke-width="2.5" stroke-linecap="round"/>')
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
    t_night = (l2.end + l3.start) / 2 + 0.05      # middle of the night flash
    t_dawn = l3.start + 0.45
    t_worm0, t_worm1 = l3.start + 0.35, l3.start + 1.25    # worm crawls in ("一条虫子")
    t_bite0 = l3.start + 1.45                     # "咬了蓖麻"
    t_bite1 = t_bite0 + 0.9
    t_with0 = l3.start + 0.71 * (l3.end - l3.start)  # "蓖麻枯干了"
    t_with1 = l3.end + 0.1
    t_sun0, t_sun1 = l4.start - 0.35, l4.start + 0.75  # "烈日当头"
    t_wind = l4.start + 1.05                      # "热风吹来"
    t_faint = l4.start + 2.2                      # "约拿热得发昏"

    # =============================================================== SKY
    sky_h = 665          # the far hills / plain cover everything below
    sky_day = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>',
        defs=S.lin_grad("g", [(0, "#8fc4dc"), (0.5, "#c9e3df"), (0.82, "#f4e2b8"), (1, "#f6dcab")]))
    a_gold = lambda t: _env(t, t_gold0 - 0.3, t_gold1 - 0.4, t_night - 0.25, t_night + 0.1)
    a_night = lambda t: _env(t, t_night - 0.35, t_night - 0.05, t_night + 0.1, t_night + 0.45)
    a_dawn = lambda t: _env(t, t_night + 0.05, t_night + 0.55, t_sun0 + 0.3, t_sun1 + 0.2)
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
    for i in range(52):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, 560)
        stars += _star(x, y, rng.uniform(3, 7.5), "#fbf0c8", sw=0)
    mx, my = 1780, 170
    moon = (f'<path d="M{mx},{my - 70} A70,70 0 1 1 {mx},{my + 70} A54,70 0 1 0 {mx},{my - 70} Z" fill="#fbf1cf" '
            f'stroke="{P["ink"]}" stroke-width="3"/>')
    sky_night = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>' + stars +
        f'<circle cx="{mx - 20}" cy="{my}" r="160" fill="#fbf1cf" opacity="0.12"/>' + S.g(moon, filter="wobble-fine"),
        defs=S.lin_grad("g", [(0, P["night"]), (0.6, P["night_light"]), (1, "#6b6f95")]))
    sc.add("sky_night", sky_night, wc=0.4, motion=lambda t: Tf(alpha=a_night(t)))

    sky_dawn = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="900" ry="360" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#b3b0da"), (0.45, "#e8c4cc"), (0.8, "#f8d6aa"), (1, "#f9ddb0")]) +
        S.rad_grad("r", [(0, "#fff0c4", 0.9), (0.5, "#fcd3a0", 0.45), (1, "#f6c7a0", 0)]))
    sc.add("sky_dawn", sky_dawn, wc=0.5, motion=lambda t: Tf(alpha=a_dawn(t)))

    sky_hot = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="900" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#f2c46c"), (0.5, "#f8d891"), (1, "#fbe3ad")]) +
        S.rad_grad("r", [(0, "#fffbe6", 1), (0.25, "#fff1bf", 0.8), (0.6, "#fbd98c", 0.25), (1, "#f6c46a", 0)]))
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

    sink = M.keys([(t_gold0 - 0.2, {"dy": 0}), (t_night - 0.15, {"dy": HORIZON - SUN_W[1] + 90})], "in")
    sc.add("sun_day", sun_svg(CX, CY, 78, P["sun"], "#fff3c4", 300),
           motion=at(SUN_W, M.combine(sink, lambda t: Tf(alpha=1 - M.progress(t, t_gold0, t_gold1, "sine")))))
    sc.add("sun_set", sun_svg(CX, CY, 84, "#f59a52", "#ffd08a", 360),
           motion=at(SUN_W, M.combine(sink, lambda t: Tf(alpha=_env(t, t_gold0, t_gold1, 99, 100)))))
    climb = M.keys([(t_night, {"dx": 0, "dy": 60}), (t_dawn + 0.8, {"dx": -20, "dy": -40}),
                    (t_sun0 + 0.2, {"dx": -70, "dy": -170}),
                    (t_sun1, {"dx": SUN_HOT[0] - SUN_E[0], "dy": SUN_HOT[1] - SUN_E[1], "s": 1.25})],
                   ["out", "linear", "inout"], pivot=(CX, CY))
    sc.add("sun_dawn", sun_svg(CX, CY, 82, "#f8c070", "#ffe0b0", 330),
           motion=at(SUN_E, M.combine(climb, lambda t: Tf(alpha=_env(t, t_night + 0.1, t_dawn + 0.3, t_sun1 - 0.3,
                                                                     t_sun1 + 0.2)))))

    # hot noon sun: blazing disc + slowly turning rays
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
    rays = S.svg_doc(S.g(
        f'<path d="{ray_d}" fill="#ffc94f" stroke="#e39a3c" stroke-width="4" stroke-linejoin="round" opacity="0.9"/>'
        f'<path d="{S.rays(hx, hy, 135, 230, n=14, width_deg=7, rot=12.9)}" fill="#fff0b0" opacity="0.8"/>',
        filter="wobble"))
    sc.add("sun_rays", rays, wc=0.3,
           motion=at(SUN_HOT, M.combine(lambda t: Tf(rot=12 * t, px=hx, py=hy),
                                        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.3, t_sun1 + 0.4, "sine") *
                                                     (0.85 + 0.15 * math.sin(t * 5.0))))))
    hot = S.svg_doc(
        f'<circle cx="{hx}" cy="{hy}" r="300" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{hx}" cy="{hy}" r="118" fill="#ffd650" stroke="#e89a3a" stroke-width="6"/>'
            f'<circle cx="{hx}" cy="{hy}" r="88" fill="#fff0a8"/>'
            f'<circle cx="{hx - 30}" cy="{hy - 30}" r="34" fill="#fffbe6" opacity="0.8"/>', filter="wobble"),
        defs=S.rad_grad("hg", [(0, "#fff6cc", 0.95), (0.45, "#ffe08a", 0.55), (1, "#ffcf6a", 0)]))
    sc.add("sun_hot", hot, wc=0.4, motion=at(SUN_HOT, M.combine(
        M.breathe(0.035, 1.3, pivot=(hx, hy)),
        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.4, t_sun1 + 0.1, "sine")))))

    # --- clouds ----------------------------------------------------------------------------------
    clouds = S.svg_doc(S.g(
        S.cloud(700, 150, 290, 88, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
        S.cloud(1640, 290, 240, 76, "#fdf1e2", seed=5, sw=3, shade_fill="#f0d6c4") +
        S.cloud(2080, 120, 320, 96, "#fdf3e4", seed=8, sw=3, shade_fill="#f0d6c4") +
        S.cloud(110, 400, 190, 60, "#fdf1e2", seed=9, sw=3, shade_fill="#f0d6c4"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=M.combine(
        M.drift(vx=-7), lambda t: Tf(alpha=(1 - 0.25 * _env(t, t_gold0, t_gold1, 99, 100) -
                                            0.75 * M.progress(t, t_sun0, t_sun1, "sine")) *
                                     (1 - M.progress(t, t_sun1, t_sun1 + 0.6, "sine")))))

    # =============================================================== LAND (static, flattened)
    far = ""
    far += S.path(S.smooth_path([(-80, HORIZON + 8), (150, 600), (420, 585), (700, 610), (950, 590),
                                 (1250, 560), (1550, 585), (1850, 570), (2200, 600)], closed=False) +
                  f" L{W + 80},{HORIZON + 30} L-80,{HORIZON + 30} Z", fill="#e3d3c0", sw=3)
    far += S.path(S.smooth_path([(1000, HORIZON + 6), (1300, 612), (1600, 598), (1900, 615), (2200, 605)],
                                closed=False) + f" L{W + 80},{HORIZON + 30} L1000,{HORIZON + 30} Z", fill="#dfcbb0", sw=3)
    sc.add("far_hills", S.svg_doc(S.g(far, filter="wobble")), wc=0.7)

    city = PR.nineveh_skyline(20, 560, HORIZON + 4, scale=0.42, seed=2, haze=0.42, tint="#efdcbc")
    sc.add("city", S.svg_doc(city), wc=0.6)

    plain = S.path(f"M-80,{HORIZON} L{W + 80},{HORIZON} L{W + 80},{H + 80} L-80,{H + 80} Z", fill="url(#pl)", sw=0)
    plain += f'<path d="M-80,{HORIZON + 2} L{W + 80},{HORIZON + 2}" stroke="{P["ink"]}" stroke-width="3" opacity="0.55"/>'
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
    sc.add("plain", S.svg_doc(S.g(plain, filter="wobble"), defs=defs), wc=0.8)

    mid = ""
    for (x, y, s, v) in [(260, 740, 0.4, 2), (640, 772, 0.42, 2), (1010, 884, 0.45, 2), (1600, 768, 0.45, 2),
                         (1880, 742, 0.4, 2), (1420, 812, 0.5, 2), (130, 760, 0.32, 2)]:
        mid += PR.bush(x, y, s, variant=v)
    for (x, y, s) in [(1950, 728, 0.3), (2050, 734, 0.24)]:
        mid += PR.palm_tree(x, y, s, lean=-0.2)
    for (x, y, w_, h_, sd) in [(1700, 860, 110, 58, 3), (1340, 900, 80, 40, 4), (360, 790, 70, 34, 6),
                               (900, 830, 60, 30, 7)]:
        mid += _rock(x, y, w_, h_, seed=sd, sw=3)
    sc.add("mid", S.svg_doc(mid), wc=0.8)

    # the knoll Jonah sits on
    knoll_pts = [(-80, 1035), (200, 1010), (480, 980), (760, 964), (1100, 959), (1450, 962), (1700, 954),
                 (1920, 930), (2200, 905)]
    kd = S.smooth_path(knoll_pts, closed=False) + f" L{W + 80},{H + 80} L-80,{H + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4)
    rp = [(x, y + 16) for x, y in knoll_pts[1:-1]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f0cf95" stroke-width="14" opacity="0.5"/>'
    for (x, y) in [(260, 1050), (560, 1020), (1460, 1012), (1660, 1040), (1960, 1000), (1000, 1035), (760, 1080)]:
        knoll += (f'<path d="M{x - 70},{y} q70,-16 140,0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.45" stroke-linecap="round"/>')
    for (x, y, r) in [(640, 984, 9), (1590, 985, 8), (1630, 992, 6), (470, 1002, 7), (1780, 1000, 9), (980, 990, 6)]:
        knoll += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4}" ry="{r}" fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="3"/>'
    sc.add("knoll", S.svg_doc(S.g(knoll, filter="wobble"),
                              defs=S.lin_grad("kn", [(0, "#e6bc7c"), (0.3, "#dcab69"), (1, "#c38c55")])), wc=0.9)

    # foreground corner rocks (static: flattened with the land; nothing moving passes behind them)
    fg = ""
    fg += _rock(150, 1160, 290, 130, seed=31) + _rock(360, 1180, 160, 72, seed=32)
    fg += _rock(1960, 1165, 250, 115, seed=33) + _rock(1790, 1185, 140, 64, seed=34)
    fg += PR.bush(2075, 1112, 1.05, variant=2)
    sc.add("fg_rocks", S.svg_doc(S.g(fg, filter="wobble")), wc=0.9)

    # booth + its soft contact shadow (afternoon light from the west, shadow falls east)
    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{P["ink"]}" opacity="0.16" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    sc.add("booth", S.svg_doc(booth), wc=0.8)

    # =============================================================== CANOPY SHADE (ground)
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
        rot = 0.7 * math.sin(2 * math.pi * t / 3.4)
        wind = M.progress(t, t_wind - 0.3, t_wind + 0.6, "sine")
        rot = rot * (1 - wind) + wind * (-2.0 + 1.4 * math.sin(2 * math.pi * t / 0.95) + 0.5 * math.sin(t * 9.1))
        return Tf(rot=rot, sx=s, sy=s, alpha=a, px=XP, py=GY)

    sc.add("castor", plant_frames, frame_at=plant_frame, motion=plant_motion, wc=0.9)

    # =============================================================== JONAH (flipbook of poses)
    poses = [("sit_sulk", "angry"), ("sit", "surprised"), ("sit_happy", "happy"), ("sit", "peaceful"),
             ("sit", "sad"), ("sit_faint", "tired"), ("sit_faint", "dizzy")]
    jshadow = CH.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)
    jframes = [S.svg_doc(jshadow + CH.jonah(XJ, GY, SP, -1, pose=p, expr=e)) for p, e in poses]
    switch = [(t_grow0 + 0.45, 0.2), (t_happy, 0.22), (t_night - 0.05, 0.2), (t_with0 + 0.25, 0.2),
              (l4.start + 0.3, 0.2), (t_faint, 0.25)]

    def jonah_frame(t):
        f = 0.0
        for i, (ts, d) in enumerate(switch):
            f = i + M.progress(t, ts, ts + d, "sine") if t >= ts else f
        return f

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
        if t_happy <= t < t_night:   # happy rocking
            k = M.progress(t, t_happy, t_happy + 0.4)
            rot = k * 1.6 * math.sin(2 * math.pi * (t - t_happy) / 1.1)
            dy = -k * 4 * abs(math.sin(2 * math.pi * (t - t_happy) / 1.1))
        if t >= t_faint:           # dizzy wobble
            k = M.progress(t, t_faint, t_faint + 0.6)
            rot = k * 2.4 * math.sin(2 * math.pi * (t - t_faint) / 1.8)
        return Tf(dy=dy, rot=rot, sx=s, sy=sy, px=XJ, py=GY)

    sc.add("jonah", jframes, frame_at=jonah_frame, motion=jonah_motion, wc=0.6)

    # canopy shade veil over Jonah and the booth
    veil = S.svg_doc(
        f'<path d="M{XB - 380},{GY - 480} Q{XB},{GY - 600} {XB + 380},{GY - 480} L{XB + 380},{GY + 20} '
        f'L{XB - 380},{GY + 20} Z" fill="#b9b2cf" filter="url(#blur-md)"/>')
    sc.add("shade_veil", veil, wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.38 * shade_amt(t)))

    # --- grumpy puffs ---------------------------------------------------------------------------
    hp = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit_sulk")
    hx0, hy0 = hp["head"]
    for side_, (ox, oy) in enumerate([(-92, -8), (84, -22)]):
        cx, cy = hx0 + ox, hy0 + oy
        sgn = -1 if side_ == 0 else 1

        def puff_motion(t, cx=cx, cy=cy, sgn=sgn, ph=side_ * 0.08):
            for th in huffs:
                u = t - th - ph
                if 0 <= u < 0.95:
                    a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.45, 0.95, "sine"))
                    s = 0.35 + 0.8 * M.ease("out")(min(1.0, u / 0.6))
                    return Tf(dx=sgn * 50 * M.ease("out")(min(1, u / 0.8)), dy=-95 * u, sx=s, sy=s, alpha=a,
                              px=cx, py=cy)
            return Tf(alpha=0.0)

        sc.add(f"puff{side_}", S.svg_doc(_puff(cx, cy, 34)), motion=puff_motion, wc=0.3)

    # =============================================================== WORM
    worm_frames = [S.svg_doc(PR.worm(XW, GY + 2, SW, 1, crawl=c, chomp=ch))
                   for c, ch in [(1.0, 0), (0.5, 0), (0, 0), (0, 0.5), (0, 1.0)]]

    def worm_frame(t):
        if t < t_worm1:
            u = (t - t_worm0) * 2.6
            return 2 - 2 * abs(math.sin(math.pi * u)) if u > 0 else 2.0
        if t_bite0 <= t < t_with0 + 0.6:
            u = (t - t_bite0) * 3.2
            return 2 + 2 * abs(math.sin(math.pi * u))
        return 2.0

    sc.add("worm", worm_frames, frame_at=worm_frame, wc=0.5, motion=M.combine(
        M.keys([(t_worm0, {"dx": -210, "alpha": 0}), (t_worm0 + 0.2, {"alpha": 1}), (t_worm1, {"dx": 0})], "linear"),
        lambda t: Tf(dy=-3 * abs(math.sin(t * 6)) if t > t_with0 + 0.6 else 0)))
    # pebble the worm crawls out from behind
    sc.add("pebble", S.svg_doc(S.g(_rock(XW - 215, GY + 16, 130, 62, seed=21, sw=4), filter="wobble-fine")), wc=0.8)

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

    # =============================================================== DOVES flying home at sunset
    dove_frames = [S.svg_doc(PR.dove(1900, 300, 0.62, -1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    for i, (t0, dy, ph) in enumerate([(l1.end - 0.9, 0, 0), (l1.end - 0.55, 80, 2)]):
        dur = 2.9
        sc.add(f"dove{i}", dove_frames, frame_at=flap(11, ph), wc=0.4, motion=M.combine(
            M.keys([(t0, {"dx": 330, "dy": dy - 40}), (t0 + dur, {"dx": -2150, "dy": dy + 60})], "linear"),
            M.bob(10, 0.6, ph * 0.1)))

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
                                [(560, 1000, 0.65, 1)],
                                [(1520, 990, 0.65, 1), (1700, 985, 0.6, 1)]]):
        frames = [S.svg_doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts))
                  for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", frames, frame_at=grass_frame_fn(gi * 0.23), wc=0.7)

    # --- hot east wind: swirls and blowing dead leaves (from the right, toward the city) ----------
    for i, (y, ln, ph) in enumerate([(420, 360, 0.0), (610, 300, 0.45), (820, 380, 0.8), (300, 260, 1.15)]):
        x0 = 1700
        sw_svg = S.svg_doc(S.g(_swirl(x0, y, ln), filter="wobble-fine"))

        def swirl_motion(t, ph=ph, x0=x0, y=y):
            if t < t_wind - 0.2:
                return Tf(alpha=0.0)
            u = ((t - t_wind + 0.2 + ph) % 1.6) / 1.6
            a = math.sin(math.pi * u) * M.progress(t, t_wind - 0.2, t_wind + 0.3)
            return Tf(dx=500 - 1500 * u, dy=12 * math.sin(6 * u), alpha=0.9 * a)

        sc.add(f"swirl{i}", sw_svg, motion=swirl_motion, wc=0.2)

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
    sc.camera = M.cam_keys([
        (0.0, Cam(1060, 600, 2000)),
        (l0.end, Cam(1010, 610, 1900)),
        (t_grow0 + 0.3, Cam(1020, 595, 1960)),
        (t_shade1, Cam(1050, 580, 2010)),
        (l2.end, Cam(1080, 590, 1900)),
        (t_worm0, Cam(1060, 600, 1900)),
        (t_bite0 + 0.2, Cam(960, 720, 1450)),
        (t_with0, Cam(975, 705, 1490)),
        (t_with1, Cam(1060, 590, 1990)),
        (t_faint - 0.2, Cam(1130, 580, 1900)),
        (T, Cam(1140, 590, 1860)),
    ], "inout")

    # =============================================================== FX
    def grade(frame, t, view):
        mul = np.array([255.0, 255.0, 255.0])
        for col, k in [((255, 216, 172), _env(t, t_gold0 - 0.3, t_gold1, t_night - 0.3, t_night + 0.1)),
                       ((80, 92, 160), _env(t, t_night - 0.3, t_night - 0.05, t_night + 0.1, t_night + 0.45) * 0.8),
                       ((246, 220, 230), _env(t, t_night, t_night + 0.4, t_bite0, t_sun1) * 0.8),
                       ((255, 224, 184), M.progress(t, t_sun0 + 0.2, t_sun1 + 0.4, "sine"))]:
            if k > 0:
                mul *= (255 - (255 - np.array(col, float)) * k) / 255.0
        if (mul >= 254.5).all():
            return frame
        arr = cv2.multiply(np.asarray(frame), (float(mul[0]) / 255, float(mul[1]) / 255, float(mul[2]) / 255, 1.0))
        return Image.fromarray(arr, "RGBA")

    rng2 = np.random.default_rng(17)
    NDUST = 150
    dx0 = rng2.uniform(0, 1, NDUST)
    dy0 = rng2.uniform(0.2, 1.0, NDUST)
    dsp = rng2.uniform(0.7, 1.4, NDUST)
    dln = rng2.uniform(24, 100, NDUST)
    dal = rng2.uniform(80, 170, NDUST)

    def dust(frame, t, view):
        k = M.progress(t, t_wind - 0.4, t_wind + 0.6, "sine")
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        Wf, Hf = frame.size
        for i in range(NDUST):
            x = (dx0[i] * (Wf + 300) - t * 1100 * dsp[i]) % (Wf + 300) - 150
            y = dy0[i] * Hf + 18 * math.sin(t * 3 + i)
            a = int(dal[i] * k * (0.5 + 0.5 * dy0[i]))
            if i % 3 == 0:
                r = 2 + (i % 4)
                d.ellipse([x - r, y - r, x + r, y + r], fill=(214, 172, 112, a))
            else:
                d.line([(x, y), (x + dln[i], y - dln[i] * 0.08)], fill=(250, 230, 188, a), width=2 + i % 3)
        frame.alpha_composite(ov)
        return frame

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
        FX.vignette(lambda t: 0.36 * M.progress(t, t_sun1, t_faint + 0.8, "sine") *
                    (0.85 + 0.15 * math.sin(t * 3.2)), color=(150, 72, 24)),
    ]

    # =============================================================== SOUND
    sc.sfx("wind_soft", 0, dur=t_sun0 + 0.6, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("sparkle", t_grow0 - 0.1, gain_db=-9)
    sc.sfx("grow", t_grow0, dur=None, gain_db=-7)
    sc.sfx("sparkle", t_grow1 - 0.4, gain_db=-12, pan=0.2)
    sc.sfx("birds", l1.end - 0.3, dur=l2.end - l1.end + 0.6, gain_db=-14, fade_in=0.3, fade_out=0.5, pan=-0.2)
    sc.sfx("crunch", t_bite0, gain_db=-6, pan=-0.2)
    sc.sfx("wither", t_with0, gain_db=-8)
    sc.sfx("wind_hot", t_wind - 0.4, dur=T - t_wind + 1.2, gain_db=-11, fade_in=0.6, fade_out=0.8)
    sc.sfx("heat", t_sun0 + 0.2, dur=T - t_sun0 + 0.6, gain_db=-13, fade_in=0.8, fade_out=0.8)
    return sc
