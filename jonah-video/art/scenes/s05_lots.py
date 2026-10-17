"""Scene 5 — the lots (Jonah 1:6-12).

A tall dollhouse cut-away of the ship. The scene opens below deck exactly where scene 4 left Jonah: asleep on a
bed of grain sacks (head on the right) under the swinging lantern, the ladder to the hatch on the right. While the
dark s04 frame dissolves in, the captain is already walking in from the right at the level of the sacks, behind the
ladder and the tied amphorae (a planted-foot walk cycle); he bends down over two in-betweens, kneels by Jonah's head
and shakes him awake; Jonah sits up rubbing his eye while the captain rises, hops back to stand, turns and points up
the ladder (each main pose held long enough to read; the camera widens only once he has knelt). Jonah gets to his feet and the camera rises gently through the deck to the rainy deck.

On deck a sailor holds out the clay lots pot; the sailors draw (one lifts his plain stick, the others hold theirs).
Jonah climbs up through the open hatch, walks to the pot and draws the last lot himself: he holds it up and it glows
in his hand, warm light breaks through the clouds onto him (God's presence is only light), and he steps back. The two nearest
sailors point at him, the others start back in surprise. Jonah, sorry and brave, confesses (hand on chest, the
lot against it) and turns round (a paper cut-out turn) to point to the raging sea; the sailors exchange worried looks; the camera slowly pushes in.
The storm goes on (a bit lighter): rain, a tilting horizon with big waves beyond the rail, one soft thunder.

Stage 2112 x 2440: deck world y 0..1190, cut section 1190..1262, hold 1262..2440.
"""
import math
import random
from dataclasses import replace

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SH = 2120            # stage height
DECK_CUT = 1190      # near (cut) edge of the deck floor
HOLD_TOP = 1262      # top of the hold interior
RAIL_TOP = 800       # top of the far bulwark
DECK_BACK = 892      # where the deck floor meets the far bulwark

# ---- hold: the opening frame continues the LAST FRAME OF s04 (Jonah asleep on grain sacks, head on the right,
# lantern, ladder up to the hatch). Elements are placed from their s04 end-frame OUTPUT positions through hp():
# the opening camera CAM_HOLD0 maps stage (H0) to the frame centre at HK output px per stage px, the same scale as
# s04's final figure (Jonah ~1.84 x on screen). If s04's ending is reframed, re-measure the S04_* points.
H0, HK = (1381.0, 1552.0), 1.6
CAM_HOLD0 = Cam(H0[0], H0[1], 1920 / HK)


def hp(ox, oy):
    """s04 end-frame output px -> s05 stage px (opening camera)."""
    return (H0[0] + (ox - 960) / HK, H0[1] + (oy - 540) / HK)


S04_HEAD = (1066, 788)            # sleeping Jonah's head centre
S04_FLOOR = 1042                  # floor line
S04_LAMP = (894, 218)             # lantern hook
S04_LADDER = ((1515, 200), (1715, 201), (1667, 1056), (1867, 1057))   # rails: top-left, top-right, bottom l, r
HS = 1.15                         # people scale in the hold (on screen ~1.84 x in the opening frame)
FLOOR = round(hp(0, S04_FLOOR)[1])                      # hold floor line (back wall foot)
HJ = (round(hp(*S04_HEAD)[0] - 136.43 * HS), round(hp(*S04_HEAD)[1] + 78.6 * HS))   # Jonah's anchor (bed top)
HOLD_LAMP = tuple(round(v) for v in hp(*S04_LAMP))
HX = 1790                         # hatch centre (deck opening; the hold ladder below lines up with it)


def _ladder_rails():
    (a, b, c, d) = [hp(*q) for q in S04_LADDER]
    k = (c[0] - a[0]) / (c[1] - a[1])
    top = (a[0] - k * (a[1] - HOLD_TOP + 6), b[0] - k * (b[1] - HOLD_TOP + 6))
    bot = (c[0] + k * (FLOOR + 12 - c[1]), d[0] + k * (FLOOR + 12 - d[1]))
    return tuple(round(v) for v in top), tuple(round(v) for v in bot)


LAD_TOP, LAD_BOT = _ladder_rails()                      # ladder rails at HOLD_TOP - 6 and at FLOOR + 12
CAM_HOLD1 = Cam(1322, FLOOR - 338, 1560)                # wider, after the captain arrives

# ---- deck
CAM_DECK = Cam(1295, 680, 1620)   # end of the rise (the captain at the far left is still out of frame)
CAM_WIDE = Cam(1080, 650, 1860)   # everyone, when the lot falls on Jonah
CAM_PUSH = Cam(1424, 735, 1350)   # slow push-in on Jonah and the nearest sailors (lines 2-3)
CAM_END = Cam(1420, 737, 1336)
MAST_X = 820                      # left edge of the mast (58 wide)
CAPT = (400, 1012, 1.02)          # front row, far left
S0 = (690, 916, 0.84)             # variant 1, back row
S1 = (990, 958, 0.92)             # variant 0, middle row: draws a lot during the narration (x set from the pot)
S3 = (1280, 1016, 1.06)           # variant 3, front row: holds the pot out at arm's length, later points
S2 = (1350, 906, 0.85)            # variant 2, back row, just behind-right of S3 (their pointing arms stack)
JY = 995                          # Jonah's ground line on deck
JEND = 1640                       # Jonah's mark after he steps back from the pot (alone, in the light)
POT_S = 1.0
HATCH_B = (1712, 1868, 978)       # back edge of the hatch opening (x0, x1, y)
HATCH_F = (1696, 1884, 1032)      # front edge
CLIP_Y = HATCH_F[2] - 3           # the climbing Jonah is hidden below this line (top of the front lip)

SWAY_PIVOT = (1056, 820)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=SH)


def sea_rot(t):
    """Outboard world tilt (deg): the horizon rocks against the level ship."""
    return 1.45 * math.sin(2 * math.pi * t / 5.4 + 0.6)


def tilted(m=None):
    """Combine a layer motion with the sea tilt about SWAY_PIVOT (m's own pivot/scale preserved)."""
    px, py = SWAY_PIVOT

    def f(t):
        th = sea_rot(t)
        v = m(t) if m else Tf()
        bx = v.px if v.px is not None else px
        by = v.py if v.py is not None else py
        # base point of the layer's own transform, rotated about the sway pivot
        a = math.radians(th)
        qx = px + (bx + v.dx - px) * math.cos(a) - (by + v.dy - py) * math.sin(a)
        qy = py + (bx + v.dx - px) * math.sin(a) + (by + v.dy - py) * math.cos(a)
        return Tf(qx - bx, qy - by, v.rot + th, v.sx, v.sy, v.alpha, bx, by)
    return f


# ============================================================== small drawing helpers

def peaky_band(y0, amp, wl, phase=0.0, x0=-80, x1=W + 80, bottom=1060, sharp=1.7, step=None, seed=None, var=0.0):
    """Storm-sea band whose top has pointed crests (crest where (x/wl+phase) % 1 == 0).
    With a seed, every crest gets its own height (amp * (1 +- var))."""
    step = step or wl / 10
    pts = []
    x = x0
    while x <= x1 + step:
        v = x / wl + phase
        u = v % 1.0
        h = (0.5 + 0.5 * math.cos(2 * math.pi * u)) ** sharp
        pts.append((x, y0 - amp * h * crest_mul(round(v), seed, var)))
        x += step
    d = S.smooth_path(pts, closed=False)
    return d + f" L{S.fmt(pts[-1][0])},{bottom} L{S.fmt(pts[0][0])},{bottom} Z"


def crest_mul(k, seed, var):
    if seed is None or var <= 0:
        return 1.0
    return 1.0 + var * (2 * random.Random(seed * 1000 + k).random() - 1)


def crest_xs(wl, phase, x0=-80, x1=W + 80):
    k0 = math.floor(x0 / wl + phase) - 1
    out = []
    for k in range(k0, k0 + int((x1 - x0) / wl) + 4):
        x = (k - phase) * wl
        if x0 - wl < x < x1 + wl:
            out.append((k, x))
    return out


def foam_cap(x, y, w, seed=0, fill=None, opacity=1.0, curl=True):
    """Little foam crown sitting on a wave crest (a few overlapping puffs of varied size + a curl)."""
    r = random.Random(seed)
    fill = fill or P["foam"]
    out = ""
    n = r.choice((3, 4, 4, 5))
    for i in range(n):
        u = (i + 0.5) / n
        cx = x - w / 2 + w * u + r.uniform(-w * 0.08, w * 0.08)
        rad = w * (0.13 + 0.12 * math.sin(math.pi * u)) * r.uniform(0.75, 1.25)
        out += f'<circle cx="{S.fmt(cx)}" cy="{S.fmt(y + rad * 0.3 + r.uniform(-2, 3))}" r="{S.fmt(rad)}" fill="{fill}"/>'
    if curl:
        out += (f'<path d="M{S.fmt(x - w * 0.55)},{S.fmt(y + w * 0.18)} q{S.fmt(w * 0.2)},{S.fmt(-w * 0.32)} '
                f'{S.fmt(w * 0.45)},{S.fmt(-w * 0.12)}" fill="none" stroke="{S.INK}" stroke-width="3" '
                f'stroke-linecap="round" opacity="0.5"/>')
    return f'<g opacity="{opacity}">{out}</g>'


def shield(cx, cy, r, col):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" {S.STROKE}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="#fff6e3" stroke-width="5" '
            f'opacity="0.75"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.25:.1f}" fill="{P["gold"]}" {S.STROKE_THIN}/>')


def plank_lines(x0, x1, ys, seed=0, color=None, joint_every=(160, 320), sw=2.5, opacity=0.55):
    """Horizontal plank seams with staggered butt joints."""
    r = random.Random(seed)
    color = color or S.INK
    out = ""
    for i, y in enumerate(ys):
        out += (f'<path d="M{x0},{y:.1f} L{x1},{y:.1f}" stroke="{color}" stroke-width="{sw}" '
                f'opacity="{opacity}" fill="none"/>')
        if i + 1 < len(ys):
            y2 = ys[i + 1]
            x = x0 + r.uniform(0, joint_every[1])
            while x < x1:
                out += (f'<path d="M{x:.1f},{y:.1f} L{x:.1f},{y2:.1f}" stroke="{color}" stroke-width="{sw}" '
                        f'opacity="{opacity * 0.8:.2f}"/>')
                out += (f'<circle cx="{x + 9:.1f}" cy="{(y + y2) / 2:.1f}" r="2.6" fill="{color}" '
                        f'opacity="{opacity * 0.8:.2f}"/>')
                x += r.uniform(*joint_every)
    return out


def thick_ladder(xt, yt, xb, yb, rungs=10):
    """s04-style ladder: two thick rails (xt = (left, right) at yt, xb at yb) and round rungs."""
    wood, wl = P["wood"], P["wood_light"]
    lad = ""
    for a, b in zip(xt, xb):
        lad += f'<path d="M{a},{yt} L{b},{yb}" fill="none" stroke="{S.INK}" stroke-width="30" stroke-linecap="round"/>'
        lad += f'<path d="M{a},{yt} L{b},{yb}" fill="none" stroke="{wl}" stroke-width="20" stroke-linecap="round"/>'
    for k in range(1, rungs + 1):
        u = k / (rungs + 1)
        y = yt + (yb - yt) * u
        xa = xt[0] + (xb[0] - xt[0]) * u
        xc = xt[1] + (xb[1] - xt[1]) * u
        lad += f'<line x1="{xa:.0f}" y1="{y:.0f}" x2="{xc:.0f}" y2="{y:.0f}" stroke="{S.INK}" stroke-width="20" stroke-linecap="round"/>'
        lad += f'<line x1="{xa:.0f}" y1="{y:.0f}" x2="{xc:.0f}" y2="{y:.0f}" stroke="{wood}" stroke-width="11" stroke-linecap="round"/>'
    return S.g(lad, filter="wobble-fine")


def bucket(x, y, s=1.0):
    w, h = 70 * s, 78 * s
    body = (f'<path d="M{x - w / 2},{y - h} L{x + w / 2},{y - h} L{x + w * 0.4},{y} L{x - w * 0.4},{y} Z" '
            f'fill="{P["wood_light"]}" {S.STROKE}/>'
            f'<ellipse cx="{x}" cy="{y - h}" rx="{w / 2}" ry="{10 * s}" fill="#5f7d8a" {S.STROKE}/>'
            f'<path d="M{x - w * 0.47},{y - h * 0.68} L{x + w * 0.47},{y - h * 0.68} M{x - w * 0.43},{y - h * 0.25} '
            f'L{x + w * 0.43},{y - h * 0.25}" stroke="#6d6a66" stroke-width="{6 * s}"/>'
            f'<path d="M{x - w / 2},{y - h} Q{x},{y - h - 60 * s} {x + w / 2},{y - h}" fill="none" '
            f'stroke="{S.INK}" stroke-width="{4 * s}"/>')
    return S.g(body, filter="wobble-fine")


# ============================================================== deck world

def sky_layer():
    defs = (S.lin_grad("dsky", [(0, "#36415a"), (0.42, "#4f5d77"), (0.77, "#7f8da2"), (1, "#9eaab8")]) +
            S.rad_grad("dbreak", [(0, "#f6e2b4", 0.75), (0.5, "#e7cf9c", 0.3), (1, "#d9cdb4", 0)]) +
            S.lin_grad("curtain", [(0, "#c9d3dc", 0.0), (0.3, "#c9d3dc", 0.22), (1, "#c9d3dc", 0.0)]))
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="800" fill="url(#dsky)"/>'
    body += '<ellipse cx="1650" cy="300" rx="430" ry="170" fill="url(#dbreak)"/>'
    soft = ""
    for (cx, cy, rx, ry, col) in [(250, 170, 520, 150, "#323c52"), (900, 110, 640, 150, "#36415a"),
                                  (2000, 150, 420, 140, "#323c52"), (620, 300, 360, 80, "#465370")]:
        soft += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}"/>'
    body += S.g(soft, filter="blur-md")
    for (x0, x1) in [(180, 420), (860, 1080)]:
        body += S.g(f'<path d="M{x0},300 L{x1},300 L{x1 - 90},600 L{x0 - 90},600 Z" fill="url(#curtain)"/>',
                    filter="soft")
    bank = ""
    for i, (cx, cy, w, h, col) in enumerate([(120, 250, 560, 150, "#59667f"), (760, 210, 600, 140, "#55627b"),
                                              (1240, 200, 420, 120, "#5c6982"), (2080, 205, 520, 150, "#55627b")]):
        bank += S.cloud(cx, cy, w, h, col, seed=10 + i, sw=2.5)
    body += S.g(bank, filter="wobble")
    return doc(body, defs)


def sea_far_layer():
    """Distant storm swell on the horizon: irregular crest heights, foam caps of varied size, some missing."""
    wl, ph = 190, 0.3
    sea = S.path(peaky_band(592, 16, wl, ph, bottom=800, seed=3, var=0.55), fill="#5a7b8c", sw=3)
    r = random.Random(41)
    for k, x in crest_xs(wl, ph):
        if r.random() < 0.38:
            continue
        m = crest_mul(k, 3, 0.55)
        sea += foam_cap(x + r.uniform(-6, 6), 592 - 16 * m - 3, 34 * r.uniform(0.55, 1.25) * (0.6 + 0.4 * m),
                        seed=k, opacity=round(r.uniform(0.45, 0.75), 2), curl=r.random() < 0.5)
    sea += S.path(peaky_band(608, 10, 150, 0.6, bottom=800, seed=8, var=0.5), fill="#507285", stroke=False)
    return doc(S.g(sea, filter="wobble"))


def clouds_layer():
    c = ""
    for i, (cx, cy, w, h) in enumerate([(700, 385, 440, 105), (1180, 360, 360, 90), (2180, 370, 440, 105)]):
        c += S.cloud(cx, cy, w, h, "#6c7a91", seed=30 + i, sw=2.5)
    return doc(S.g(c, filter="wobble"))


def sea_mid_layer():
    wl, ph = 520, 0.15
    defs = S.lin_grad("smid", [(0, "#5b8a9b"), (0.45, "#3e687c"), (1, "#2c4d60")])
    body = S.path(peaky_band(690, 64, wl, ph, bottom=880, sharp=2.2, seed=5, var=0.3), fill="url(#smid)", sw=4)
    r = random.Random(77)
    for k, x in crest_xs(wl, ph):
        m = crest_mul(k, 5, 0.3)
        w = 86 * r.uniform(0.7, 1.2) * m
        top = 690 - 64 * m
        body += foam_cap(x + r.uniform(-14, 14), top + 4, w, seed=20 + k)
        body += (f'<path d="M{x - 60 + r.uniform(-20, 20):.1f},{top + 34:.1f} q30,26 70,30 '
                 f'M{x + 30 + r.uniform(-20, 20):.1f},{top + 46:.1f} q26,18 64,16" fill="none" '
                 f'stroke="{P["foam"]}" stroke-width="5" stroke-linecap="round" opacity="0.55"/>')
    return doc(S.g(body, filter="wobble"), defs)


def big_wave_layer():
    """A huge breaking wave beyond the starboard rail (right), curling toward the ship."""
    defs = S.lin_grad("bigw", [(0, "#74a2b0"), (0.35, "#4a788b"), (1, "#2c4d60")])
    pts = [(1240, 860), (1380, 770), (1520, 630), (1640, 530), (1740, 470), (1840, 440), (1950, 448),
           (2060, 488), (2180, 548), (2280, 610)]
    d = S.smooth_path(pts, closed=False) + " L2280,880 L1240,880 Z"
    body = S.path(d, fill="url(#bigw)", sw=5)
    body += ('<path d="M1500,700 Q1620,640 1700,600" fill="none" stroke="#335a6c" stroke-width="10" '
             'stroke-linecap="round" opacity="0.6"/>')
    for (x, y) in [(1560, 660), (1660, 610), (1900, 560), (2020, 600), (1780, 650), (1460, 760)]:
        body += (f'<path d="M{x},{y} q34,26 92,30" fill="none" stroke="{P["foam"]}" stroke-width="6" '
                 f'stroke-linecap="round" opacity="0.5"/>')
    crest = S.smooth_path([(1690, 494), (1760, 462), (1850, 440), (1950, 446), (2060, 484), (2180, 544),
                           (2290, 606)], closed=False)
    curl = "M1700,494 C1660,498 1640,540 1664,562 C1688,582 1716,560 1704,542"
    body += f'<path d="{crest}" fill="none" stroke="{S.INK}" stroke-width="46" stroke-linecap="round"/>'
    body += f'<path d="{curl}" fill="none" stroke="{S.INK}" stroke-width="34" stroke-linecap="round"/>'
    body += f'<path d="{crest}" fill="none" stroke="{P["foam"]}" stroke-width="38" stroke-linecap="round"/>'
    body += f'<path d="{curl}" fill="none" stroke="{P["foam"]}" stroke-width="26" stroke-linecap="round"/>'
    body += foam_cap(1850, 430, 100, seed=52) + foam_cap(2040, 466, 84, seed=53)
    return doc(S.g(body, filter="wobble"), defs)


def splash_layer(cx, cy, seed, k=1.0):
    """Soft cartoon splash thrown up over the rail: a few rounded water tongues with drops at their tips, light
    blue shading on their undersides, a puffy foam mound at the base. (cx, cy) = base of the burst (rail top)."""
    r = random.Random(seed)
    foam, ink, blue = P["foam"], S.INK, "#bcd9e2"
    sw = 2.6 * k
    tongues, drops = "", ""
    n = 5
    for i in range(n):
        ang = math.radians(-152 + 124 * (i + 0.5) / n + r.uniform(-6, 6))
        ln = r.uniform(78, 120) * k * (1.12 if 0 < i < n - 1 else 0.82)
        w = r.uniform(25, 32) * k
        ca, sa = math.cos(ang), math.sin(ang)
        nx, ny = -sa, ca
        base_l = (cx + nx * w, cy + ny * w)
        base_r = (cx - nx * w, cy - ny * w)
        mid_l = (cx + 0.55 * ln * ca + nx * w * 0.55, cy + 0.55 * ln * sa + ny * w * 0.55)
        mid_r = (cx + 0.55 * ln * ca - nx * w * 0.55, cy + 0.55 * ln * sa - ny * w * 0.55)
        tip_l = (cx + 0.9 * ln * ca + nx * w * 0.42, cy + 0.9 * ln * sa + ny * w * 0.42)
        tip_r = (cx + 0.9 * ln * ca - nx * w * 0.42, cy + 0.9 * ln * sa - ny * w * 0.42)
        apex = (cx + 1.08 * ln * ca, cy + 1.08 * ln * sa)
        pts = [base_l, mid_l, tip_l, apex, tip_r, mid_r, base_r]
        d = S.smooth_path(pts, closed=False, tension=0.9) + " Z"
        tongues += f'<path d="{d}" fill="{foam}" stroke="{ink}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
        # light blue shading along the lower side of the tongue
        sh = S.smooth_path([base_r, ((mid_r[0] + mid_l[0] * 0.3) / 1.3, (mid_r[1] + mid_l[1] * 0.3) / 1.3),
                            ((tip_r[0] * 2 + apex[0]) / 3, (tip_r[1] * 2 + apex[1]) / 3)], closed=False)
        tongues += (f'<path d="{sh}" fill="none" stroke="{blue}" stroke-width="{w * 0.55:.1f}" stroke-linecap="round" '
                    f'opacity="0.75"/>')
        dr = w * r.uniform(0.36, 0.48)
        dx_, dy_ = cx + (1.08 * ln + dr * 1.9) * ca, cy + (1.08 * ln + dr * 1.9) * sa
        drops += (f'<circle cx="{dx_:.1f}" cy="{dy_:.1f}" r="{dr:.1f}" fill="{foam}" stroke="{ink}" '
                  f'stroke-width="{sw * 0.8:.1f}"/>'
                  f'<circle cx="{dx_ + dr * 0.3:.1f}" cy="{dy_ + dr * 0.3:.1f}" r="{dr * 0.45:.1f}" fill="{blue}"/>')
    for i in range(4):
        ang = math.radians(r.uniform(-160, -20))
        dist = r.uniform(130, 190) * k
        rr = r.uniform(6, 10) * k
        drops += (f'<circle cx="{cx + dist * math.cos(ang):.1f}" cy="{cy + dist * math.sin(ang):.1f}" r="{rr:.1f}" '
                  f'fill="{foam}" stroke="{ink}" stroke-width="{sw * 0.7:.1f}"/>')
    ms = ""
    pts = [(cx + (i - 2) * 30 * k + r.uniform(-6, 6), cy - r.uniform(4, 16) * k, r.uniform(26, 34) * k) for i in range(5)]
    for x, y, rr in pts:
        ms += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr + sw:.1f}" fill="{ink}"/>'
    for x, y, rr in pts:
        ms += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{foam}"/>'
    for x, y, rr in pts[1:4]:
        ms += f'<ellipse cx="{x:.1f}" cy="{y + rr * 0.45:.1f}" rx="{rr * 0.75:.1f}" ry="{rr * 0.35:.1f}" fill="{blue}" opacity="0.8"/>'
    return doc(S.g(tongues + drops + ms, filter="wobble-fine"))


def rig_markup():
    """Mast (centred on MAST_X + 29), shrouds, the torn striped sail of s04/s06 on a yard centred on the mast."""
    mx = MAST_X + 29
    b = ""
    for xr in (mx - 330, mx + 330):
        b += f'<path d="M{mx},-200 L{xr},{RAIL_TOP + 6}" stroke="{P["ink_soft"]}" stroke-width="5" fill="none"/>'
    b += f'<rect x="{MAST_X}" y="-40" width="58" height="{972 + 40}" fill="url(#mast)" {S.STROKE}/>'
    for yy in (640, 690):
        b += f'<rect x="{MAST_X - 6}" y="{yy}" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<path d="M{mx - 57},972 Q{mx},940 {mx + 57},972 Z" fill="{P["wood_dark"]}" {S.STROKE}/>'
    b += f'<path d="M{mx + 29},610 L{mx + 76},610" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linecap="round"/>'
    # the torn sail (props.ship's 'torn' sail, mirrored like the ship in s04 / s06), yard centred on the mast
    k, y_yard = 0.84, 300
    base_y = y_yard + 848 * k
    sail = PR._sail("torn", "s05sail")
    b += (f'<g transform="rotate(5 {mx} {y_yard})"><g transform="translate({mx},{base_y}) scale({-k},{k}) '
          f'translate(10,0)">{sail}</g></g>')
    # sheets from the sail's lower corners down to the bulwark
    for lx, dx in ((-300, 210), (280, -230)):
        sx = mx - k * (lx + 10)
        b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} L{sx + dx:.0f},{RAIL_TOP + 4}" stroke="{P["ink_soft"]}" '
              f'stroke-width="4" fill="none"/>')
    defs = S.lin_grad("mast", [(0, P["wood_dark"]), (0.4, P["wood_light"]), (1, P["wood"])], x1=0, y1=0, x2=1, y2=0)
    return S.g(b, filter="wobble"), defs


def hatch_markup():
    """Open deck hatch: a dark opening with warm light rising from the hold, the ladder's top, a raised coaming and
    the lid lying open flat beside it on two iron hinges."""
    (bx0, bx1, by), (fx0, fx1, fy) = HATCH_B, HATCH_F
    wood, wd, wl = P["wood"], P["wood_dark"], P["wood_light"]
    out = ""
    # lid, flipped open to the right onto the deck
    lx0b, lx1b, lx0f, lx1f = bx1 + 6, bx1 + 160, fx1 + 6, fx1 + 186
    out += (f'<path d="M{lx0b},{by} L{lx1b},{by} L{lx1f},{fy} L{lx0f},{fy} Z" fill="{S.mix(wood, wd, 0.25)}" '
            f'{S.STROKE}/>')
    for u in (0.33, 0.66):
        out += (f'<path d="M{lx0b + (lx1b - lx0b) * u:.0f},{by + 2} L{lx0f + (lx1f - lx0f) * u:.0f},{fy - 2}" '
                f'stroke="{S.INK}" stroke-width="2.5" opacity="0.6"/>')
    out += (f'<path d="M{lx0b + 18},{by + 14} L{lx1b - 4},{by + 14} M{lx0f + 18},{fy - 14} L{lx1f - 8},{fy - 14}" '
            f'stroke="{wl}" stroke-width="9" stroke-linecap="round"/>')
    out += f'<ellipse cx="{(lx1b + lx1f) / 2 - 30:.0f}" cy="{(by + fy) / 2:.0f}" rx="14" ry="7" fill="none" stroke="#6d6a66" stroke-width="5"/>'
    for yy in (by + 14, fy - 14):
        out += (f'<rect x="{bx1 - 14}" y="{yy - 6}" width="44" height="12" rx="4" fill="#6d6a66" {S.STROKE_THIN}/>'
                f'<circle cx="{bx1 + 8}" cy="{yy}" r="4" fill="#9a9488"/>')
    # coaming (raised frame) and the dark opening
    out += (f'<path d="M{bx0 - 14},{by - 10} L{bx1 + 14},{by - 10} L{fx1 + 16},{fy + 12} L{fx0 - 16},{fy + 12} Z" '
            f'fill="{wd}" {S.STROKE}/>')
    out += f'<path d="M{bx0},{by} L{bx1},{by} L{fx1},{fy} L{fx0},{fy} Z" fill="url(#hatchin)" {S.STROKE}/>'
    # the ladder's top rung just inside the opening (nothing sticks up above the deck)
    out += (f'<line x1="{HX - 52}" y1="{by + 16}" x2="{HX + 48}" y2="{by + 16}" stroke="{S.INK}" stroke-width="14" '
            f'stroke-linecap="round" opacity="0.8"/>'
            f'<line x1="{HX - 52}" y1="{by + 16}" x2="{HX + 48}" y2="{by + 16}" stroke="{wood}" stroke-width="7" '
            f'stroke-linecap="round" opacity="0.8"/>')
    # front lip of the coaming (the climbing Jonah is hidden behind it)
    out += (f'<path d="M{fx0 - 16},{fy - 2} L{fx1 + 16},{fy - 2} L{fx1 + 18},{fy + 14} L{fx0 - 18},{fy + 14} Z" '
            f'fill="{wl}" {S.STROKE}/>')
    defs = S.lin_grad("hatchin", [(0, "#3b2416"), (0.55, "#6a3c1f"), (1, "#d98a45")])
    return out, defs


def deck_layer():
    """Far bulwark with shields, rig and sail, deck planks, the open hatch and the cut-away section."""
    defs = (S.lin_grad("deckf", [(0, "#b98450"), (0.5, P["wood_light"]), (1, "#a96f42")]) +
            S.lin_grad("bulw", [(0, P["wood"]), (1, "#7e4e2e")]))
    b = ""
    b += f'<rect x="-30" y="{RAIL_TOP + 14}" width="{W + 60}" height="{DECK_BACK - RAIL_TOP - 4}" fill="url(#bulw)" {S.STROKE}/>'
    b += plank_lines(-30, W + 30, [842, 868], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += f'<rect x="{x - 12}" y="{RAIL_TOP + 4}" width="24" height="{DECK_BACK - RAIL_TOP}" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    for xr in (MAST_X + 29 - 330, MAST_X + 29 + 330):
        b += f'<circle cx="{xr}" cy="{RAIL_TOP + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += shield(x, 852, 33, cols[i % 4])
    b += (f'<path d="M-30,{RAIL_TOP} L{W + 30},{RAIL_TOP} L{W + 30},{RAIL_TOP + 18} L-30,{RAIL_TOP + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    b += f'<rect x="-30" y="{DECK_BACK}" width="{W + 60}" height="{DECK_CUT - DECK_BACK + 4}" fill="url(#deckf)" {S.STROKE}/>'
    ys = [906, 924, 946, 972, 1003, 1039, 1080, 1126, 1176]
    b += plank_lines(-30, W + 30, ys, seed=7, opacity=0.45, joint_every=(260, 620))
    for (x, y, rx, ry) in [(660, 1062, 130, 16), (1180, 1112, 160, 18), (1600, 1150, 120, 14), (420, 1150, 90, 12)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9fb3bd" opacity="0.45"/>'
        b += f'<path d="M{x - rx * 0.5},{y - 3} l{rx * 0.5},0" stroke="#e8eef0" stroke-width="3" opacity="0.6"/>'
    hm, hdefs = hatch_markup()
    b += hm
    rig, rdefs = rig_markup()
    b = S.g(b, filter="wobble") + rig
    cut = ""
    cut += f'<rect x="-30" y="{DECK_CUT - 4}" width="{W + 60}" height="{HOLD_TOP - DECK_CUT + 8}" fill="{P["wood_dark"]}" {S.STROKE}/>'
    cut += f'<rect x="-30" y="{DECK_CUT + 8}" width="{W + 60}" height="26" fill="{P["jonah_sash"]}" {S.STROKE_THIN}/>'
    tri = ""
    for x in range(-20, W + 40, 64):
        tri += f'M{x},{DECK_CUT + 34} l26,0 l-13,18 z '
    cut += f'<path d="{tri}" fill="{P["terracotta"]}" {S.STROKE_THIN}/>'
    for x in range(60, W + 40, 330):
        if 1640 < x < 1900:
            continue
        cut += f'<rect x="{x}" y="{DECK_CUT + 40}" width="70" height="{HOLD_TOP - DECK_CUT - 34}" fill="#5e3820" {S.STROKE_THIN}/>'
    return doc(b + S.g(cut, filter="wobble"), defs + hdefs + rdefs)


def deck_props_layer():
    """A crate and a jar against the far bulwark, behind the captain."""
    return doc(PR.crate(525, 925, 1.05) + PR.jar(452, 948, 0.62, rot=-6) +
               C.ground_shadow(525, 979, 1.0, width=150, opacity=0.18))


def deck_foreground():
    return doc(PR.rope_coil(300, 1128, 1.5) + bucket(560, 1112, 1.1))


# ============================================================== hold (echoes the s04 hold)

def grid_net(x0, y0, x1, y1):
    """s04's net: a square-mesh fishing net hung flat on the wall from a rope between two pegs."""
    body = f'<path d="M{x0},{y0} L{x1},{y0} L{x1 - 6},{y1} L{x0 + 8},{y1 + 6} Z" fill="#b89a62" fill-opacity="0.22"/>'
    mesh = ""
    n = 9
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        mesh += f"M{x:.1f},{y0} L{x + (2 if i % 2 else -2):.1f},{y1} "
    m = 5
    for j in range(1, m + 1):
        y = y0 + (y1 - y0) * j / m
        mesh += f"M{x0:.1f},{y:.1f} Q{(x0 + x1) / 2:.1f},{y + 6:.1f} {x1:.1f},{y:.1f} "
    body += f'<path d="{mesh}" stroke="{S.INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    body += f'<path d="{mesh}" stroke="#e4cf9c" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    body += (f'<path d="M{x0 - 14},{y0} L{x1 + 14},{y0}" stroke="{S.INK}" stroke-width="10" stroke-linecap="round"/>'
             f'<path d="M{x0 - 14},{y0} L{x1 + 14},{y0}" stroke="#c9a76a" stroke-width="5" stroke-linecap="round"/>')
    for x in (x0 - 14, x1 + 14):
        body += f'<circle cx="{x}" cy="{y0}" r="8" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    return S.g(body, filter="wobble-fine")


def oar(x0, x1, xb, y):
    """An oar racked on the wall: shaft x0..x1, blade out to xb."""
    wl, wd = P["wood_light"], P["wood_dark"]
    out = (f'<path d="M{x0},{y} L{x1},{y}" stroke="{S.INK}" stroke-width="16" stroke-linecap="round"/>'
           f'<path d="M{x0},{y} L{x1},{y}" stroke="{wl}" stroke-width="9" stroke-linecap="round"/>')
    out += (f'<path d="M{x1 - 10},{y - 4} Q{(x1 + xb) / 2},{y - 22} {xb},{y - 6} Q{xb + 8},{y + 4} {xb},{y + 12} '
            f'Q{(x1 + xb) / 2},{y + 22} {x1 - 10},{y + 4} Z" fill="{S.mix(wl, P["sand"], 0.3)}" {S.STROKE_THIN}/>')
    out += f'<path d="M{x1},{y} L{xb - 12},{y + 2}" stroke="{wd}" stroke-width="2.5" opacity="0.5"/>'
    return out


def sack_bed(x0, x1, top, bottom, jx):
    """Jonah's bed from s04: three grain sacks laid side by side, a sack pillow on the right and the folded teal
    blanket at the foot (left)."""
    sc_, scd = P["sackcloth"], P["sackcloth_dark"]
    h = bottom - top
    bed = ""
    n = 3
    edges = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    for i in range(n):
        a, b = edges[i] - (0 if i == 0 else 10), edges[i + 1] + (0 if i == n - 1 else 10)
        col = S.mix(sc_, P["sand"], 0.12 * i)
        d = (f"M{a:.0f},{top + 4} Q{a - 15:.0f},{top + h / 2:.0f} {a + 3:.0f},{bottom} L{b - 3:.0f},{bottom} "
             f"Q{b + 15:.0f},{top + h / 2:.0f} {b:.0f},{top + 4} Q{(a + b) / 2:.0f},{top - 10} {a:.0f},{top + 4} Z")
        bed += S.path(d, fill=col, sw=4)
        for k in range(4):
            xx = a + (b - a) * (k + 1) / 5
            bed += (f'<path d="M{xx:.0f},{top + 8} Q{xx + 4:.0f},{top + h / 2:.0f} {xx:.0f},{bottom - 4}" fill="none" '
                    f'stroke="{scd}" stroke-width="2.5" opacity="0.5"/>')
        bed += (f'<path d="M{a + 14:.0f},{top + h * 0.3:.0f} L{b - 14:.0f},{top + h * 0.3:.0f}" stroke="{scd}" '
                f'stroke-width="2.5" stroke-dasharray="8 7" opacity="0.6"/>')
    px_, py_ = jx + 164, top - 14
    bed += S.path(S.blob(px_, py_, 82, 30, 0.08, 10, seed=3), fill=S.mix(P["headcloth"], sc_, 0.45), sw=4)
    bed += (f'<path d="M{px_ - 50},{py_ - 6} Q{px_},{py_ + 6} {px_ + 52},{py_ - 7}" fill="none" stroke="{scd}" '
            f'stroke-width="2.5" opacity="0.5"/>')
    tx = x0 - 20
    bed += S.path(f"M{tx},{top + 2} Q{tx - 9},{top - 30} {tx + 20},{top - 32} L{tx + 78},{top - 32} "
                  f"Q{tx + 92},{top - 14} {tx + 78},{top + 2} Z", fill=P["jonah_sash"], sw=4)
    bed += f'<path d="M{tx + 6},{top - 15} L{tx + 78},{top - 15}" stroke="{S.shade(P["jonah_sash"], -0.35)}" stroke-width="3"/>'
    return S.g(bed, filter="wobble-fine")


def hold_front_props():
    """Hold props the captain walks in behind (also drawn into the hold layer, in this order around the bed):
    (tied amphorae + the crates at the right edge, the ladder, the little sack at the bed's right end)."""
    j1, j2 = hp(1420, 922), hp(1556, 930)
    jars = PR.jar(j1[0], j1[1], 0.96, rot=-4) + PR.jar(j2[0], j2[1], 0.94, rot=5, color=S.mix(P["terracotta"], P["sand"], 0.35))
    rope = S.mix(P["sackcloth"], P["sand"], 0.35)
    ra, rb = hp(1350, 885), hp(1625, 892)
    jars += (f'<path d="M{ra[0]:.0f},{ra[1]:.0f} Q{(ra[0] + rb[0]) / 2:.0f},{ra[1] + 12:.0f} {rb[0]:.0f},{rb[1]:.0f}" fill="none" '
             f'stroke="{S.INK}" stroke-width="9" stroke-linecap="round"/>'
             f'<path d="M{ra[0]:.0f},{ra[1]:.0f} Q{(ra[0] + rb[0]) / 2:.0f},{ra[1] + 12:.0f} {rb[0]:.0f},{rb[1]:.0f}" fill="none" '
             f'stroke="{rope}" stroke-width="4.5" stroke-linecap="round"/>')
    jars += PR.crate(2030, FLOOR - 48 * 1.25 + 6, 1.25) + PR.crate(2040, FLOOR - 48 * 1.25 - 128, 1.1, rot=3)
    ladder = thick_ladder(LAD_TOP, HOLD_TOP - 6, LAD_BOT, FLOOR + 12, rungs=8)
    s1 = hp(1355, 1044)
    return jars, ladder, PR.sack(s1[0], s1[1], 0.62, seed=2)


def hold_layer():
    """The hold below deck, laid out like the end of s04 (see hp()), widened with more cargo for the wider shot."""
    wood, wd = P["wood"], P["wood_dark"]
    defs = (S.lin_grad("hwall", [(0, "#6b3f23"), (0.35, "#93603a"), (1, "#7a4a2a")]) +
            S.lin_grad("hfloor", [(0, "#a8713f"), (1, "#7a4a2a")]) +
            S.rad_grad("hvig", [(0, "#2a160c", 0), (0.6, "#2a160c", 0.06), (1, "#2a160c", 0.62)], cx=0.58, cy=0.6) +
            S.lin_grad("shaft", [(0, "#cfe0ea", 0.42), (1, "#cfe0ea", 0.0)]))
    b = f'<rect x="-30" y="{HOLD_TOP - 10}" width="{W + 60}" height="{FLOOR - HOLD_TOP + 20}" fill="url(#hwall)"/>'
    ys = [HOLD_TOP + 70 + 58 * i for i in range(11)]
    b += plank_lines(-30, W + 30, [y for y in ys if y < FLOOR - 10], seed=21, opacity=0.36, joint_every=(300, 640))
    # upright timbers (s04's posts) and the dark frame timbers at the edges of s04's view
    for x in [hp(485, 0)[0], hp(1335, 0)[0], 560, 2050]:
        b += (f'<rect x="{x - 26:.0f}" y="{HOLD_TOP}" width="52" height="{FLOOR - HOLD_TOP}" fill="{wd}" {S.STROKE}/>'
              f'<path d="M{x - 10:.0f},{HOLD_TOP + 20} L{x - 9:.0f},{FLOOR - 20}" stroke="{wood}" stroke-width="7" opacity="0.8"/>')
    for x in [hp(35, 0)[0], hp(1885, 0)[0]]:
        b += f'<rect x="{x - 30:.0f}" y="{HOLD_TOP}" width="60" height="{FLOOR - HOLD_TOP}" fill="{S.shade(wd, -0.25)}" {S.STROKE}/>'
    # ceiling (underside of the deck) with beam ends over the posts, the grated hatch with rain and grey light
    # (the ceiling reaches up over the lower part of the deck's cut band, which s04's ending does not show)
    b += f'<rect x="-30" y="{HOLD_TOP - 54}" width="{W + 60}" height="100" fill="#4e2e1b" {S.STROKE}/>'
    b += f'<rect x="-30" y="{HOLD_TOP - 54}" width="{W + 60}" height="10" fill="{P["jonah_sash"]}" opacity="0.8"/>'
    b += f'<rect x="-30" y="{HOLD_TOP + 34}" width="{W + 60}" height="14" fill="{wood}" opacity="0.7" {S.STROKE_THIN}/>'
    for x in [hp(485, 0)[0], hp(1335, 0)[0], 560, 2050]:
        b += f'<rect x="{x - 26:.0f}" y="{HOLD_TOP + 30}" width="52" height="46" rx="6" fill="{wood}" {S.STROKE}/>'
    hx0, hx1 = HX - 100, HX + 100
    b += f'<rect x="{hx0}" y="{HOLD_TOP - 8}" width="{hx1 - hx0}" height="50" fill="#a9b8c4" {S.STROKE}/>'
    r = random.Random(5)
    for _ in range(9):
        x = r.uniform(hx0 + 8, hx1 - 14)
        b += f'<path d="M{x:.0f},{HOLD_TOP - 4} l-5,{r.uniform(20, 38):.0f}" stroke="#e6edf0" stroke-width="2.5" opacity="0.8"/>'
    for x in range(hx0 + 30, hx1, 46):
        b += f'<rect x="{x - 6}" y="{HOLD_TOP - 8}" width="12" height="50" fill="{wood}" {S.STROKE_THIN}/>'
    b += S.g(f'<path d="M{hx0},{HOLD_TOP + 44} L{hx1},{HOLD_TOP + 44} L{hx1 + 150},{FLOOR + 30} '
             f'L{hx0 - 40},{FLOOR + 30} Z" fill="url(#shaft)"/>', filter="soft")
    # floor with planks running toward the back wall
    b += f'<rect x="-30" y="{FLOOR}" width="{W + 60}" height="{SH - FLOOR + 30}" fill="url(#hfloor)" {S.STROKE}/>'
    vx, vy = H0[0], FLOOR - 420
    for x in range(-900, W + 1000, 120):
        xa = vx + (x - vx) * (FLOOR - vy) / (SH + 40 - vy)
        b += f'<line x1="{xa:.0f}" y1="{FLOOR}" x2="{x}" y2="{SH + 40}" stroke="{S.INK}" stroke-width="3" opacity="0.3"/>'
    for y in (FLOOR + 50, FLOOR + 120):
        b += f'<line x1="-30" y1="{y}" x2="{W + 30}" y2="{y}" stroke="{S.INK}" stroke-width="3" opacity="0.22"/>'
    b += f'<ellipse cx="{HX + 40}" cy="{FLOOR + 52}" rx="130" ry="16" fill="#9fb3bd" opacity="0.5" {S.STROKE_THIN}/>'
    b += f'<ellipse cx="{HX + 20}" cy="{FLOOR + 48}" rx="50" ry="5" fill="#dfeaf0" opacity="0.6"/>'
    b = S.g(b, filter="wobble")
    # wall gear like s04: square net, two racked oars, a hanging rope coil
    nx0, ny0 = hp(100, 225)
    nx1, ny1 = hp(470, 420)
    b += grid_net(round(nx0), round(ny0), round(nx1), round(ny1))
    oars = ""
    for (oa, ob, oc, oy) in ((90, 560, 745, 482), (90, 600, 800, 548)):
        x0_, y_ = hp(oa, oy)
        oars += oar(round(x0_), round(hp(ob, 0)[0]), round(hp(oc, 0)[0]), round(y_))
    for ox in (150, 360):
        px_, py_ = hp(ox, 515)
        oars += f'<rect x="{px_ - 7:.0f}" y="{py_ - 34:.0f}" width="14" height="70" rx="5" fill="{wd}" {S.STROKE_THIN}/>'
    b += S.g(oars, filter="wobble-fine")
    peg = hp(512, 655)
    b += f'<circle cx="{peg[0]:.0f}" cy="{peg[1]:.0f}" r="7" fill="{wd}" {S.STROKE_THIN}/>'
    rc = hp(530, 752)
    b += PR.rope_coil(rc[0], rc[1], 0.72)
    # cargo: s04's crate with a sack on it and a smaller crate (left), tied amphorae (right); more for the wide shot
    cargo = ""
    c1 = hp(365, 948)
    cargo += PR.crate(c1[0], c1[1], 1.0) + PR.sack(c1[0] - 8, c1[1] - 56, 0.64, seed=8)
    c2 = hp(150, 968)
    cargo += PR.crate(c2[0], c2[1], 0.86, rot=-2)
    cargo += PR.crate(660, FLOOR - 48 * 1.3 + 6, 1.3) + PR.sack(745, FLOOR + 8, 1.0, seed=6)
    cargo += PR.jar(600, FLOOR - 120, 0.9, rot=-5)
    jars, ladder, end_sack = hold_front_props()
    b += cargo + jars + ladder
    bx0, bx1 = hp(540, 0)[0], hp(1290, 0)[0] + 30
    b += sack_bed(round(bx0), round(bx1), HJ[1], FLOOR + 6, HJ[0])
    b += end_sack
    b += f'<path d="M{HOLD_LAMP[0]},{HOLD_TOP + 44} L{HOLD_LAMP[0]},{HOLD_LAMP[1] + 4}" stroke="{S.INK}" stroke-width="4"/>'
    b += (f'<rect x="{HOLD_LAMP[0] - 12}" y="{HOLD_TOP + 40}" width="24" height="14" rx="4" fill="{wd}" '
          f'{S.STROKE_THIN}/>')
    b += f'<rect x="-30" y="{HOLD_TOP - 54}" width="{W + 60}" height="{SH - HOLD_TOP + 84}" fill="url(#hvig)"/>'
    return doc(b, defs)


# ============================================================== animation helpers

def flip(sc, name, keyframes, z, motion=None, frame_at=None):
    """Flipbook layer from [(t, markup), ...] with hard pose switches at the given times."""
    times = [k[0] for k in keyframes]
    svgs = [doc(k[1]) for k in keyframes]

    def default_at(t):
        i = 0
        for j, tj in enumerate(times):
            if t >= tj:
                i = j
        return float(i)

    if len(svgs) == 1:
        sc.add(name, svgs[0], motion=motion, z=z)
    else:
        sc.add(name, svgs, motion=motion, z=z, frame_at=frame_at or default_at)
    return times


def alive(x, y, switches=(), phase=0.0, amp=0.011, period=3.1, extra=None):
    """Breathing (vertical stretch about the feet) + a squash 'pop' at every pose switch."""
    def m(t):
        sy = 1 + amp * math.sin(2 * math.pi * (t / period + phase))
        sx = 1.0
        for ts in switches:
            u = (t - ts) / 0.24
            if 0 <= u <= 1:
                bmp = math.sin(math.pi * u) * (1 - u)
                sy *= 1 - 0.09 * bmp
                sx *= 1 + 0.05 * bmp
        if extra:
            e = extra(t)
            return Tf(e.dx, e.dy, e.rot, sx, sy, e.alpha, x, y)
        return Tf(sx=sx, sy=sy, px=x, py=y)
    return m


def bump(t, ts, w=0.06):
    """0..1..0 triangle centred just after ts (a 3-4 frame hop that sells a pose swap; as in s06)."""
    return max(0.0, 1 - abs(t - ts - 0.03) / w)


def turned(m, ts, w=0.1, depth=0.7, px=None):
    """Paper cut-out turn: squeeze the layer horizontally about its pivot (or px) around each facing flip in ts,
    so the mirrored pose swaps in on the thinnest frame instead of popping."""
    def f(t):
        tf = m(t)
        k = 1.0
        for s in ts:
            u = abs(t - s) / w
            if u < 1:
                k *= 1 - depth * (1 - u)
        if px is not None:
            tf = replace(tf, px=px(t) if callable(px) else px)
        return replace(tf, sx=tf.sx * k) if k != 1.0 else tf
    return f


def captain_fig(x, y, scale=1.0, facing=1, ps=None, expr="worried", label="pose"):
    """The captain (same design and rig as C.captain) in a scene-local pose record ps (C._P(...)), for his
    entrance in the hold: the walk cycle and the in-betweens into and out of his crouch."""
    inner, _ = C._figure(C._captain_design(), C._CAPTAIN_M, dict(ps), expr, C._fsign(facing))
    return C._wrap_out(inner, x, y, scale, facing, f"captain-{label}")


# The captain's walk: CAP_N drawings per step, two steps per cycle. Drawing k (phase k / CAP_N, 0..2): the planted
# ankle (far leg in the first step, near leg in the second) goes from +CAP_A to -CAP_A figure px (forward = +) while
# the other foot swings from -CAP_A to +CAP_A, lifted mid-swing; drawing 0 is the contact with the far foot forward.
# So the planted sole stays on one spot of the floor when the anchor advances CAP_A * 2 / CAP_N * scale per drawing.
CAP_A = 56
CAP_N = 5


def cap_walk_pose(k):
    ph = (k % (2 * CAP_N)) / CAP_N
    step, u = divmod(ph, 1.0)
    plant = ("ik", CAP_A * (1 - 2 * u), 1)
    swing = ("ik", -CAP_A + 2 * CAP_A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, 24 * math.sin(math.pi * u))
    sw = 38 * math.cos(math.pi * ph)            # arms swing against the legs
    return C._P(t=7, h=-5, legs=(plant, swing) if step == 0 else (swing, plant),
                arms=(("fk", -sw, -sw + 16), ("fk", sw, sw + 16)), drop=14 + 4 * math.cos(2 * math.pi * u))


class FrontCutout:
    """Hold props the walking captain passes behind (the ladder, the tied amphorae, the crates at the right edge,
    the little sack at the bed's end), as the hold's OWN pixels: the hold layer rasterised and watercoloured exactly
    as the compositor does it (same svg, seed and strength), cut out by the props' alpha and with the lantern glow
    (additive, at rest) added. Drawn over the walking captain it is invisible wherever he is not behind a prop."""

    def __init__(self, hold_layer, glow_layer, props_svg):
        self.hold, self.glow, self.props_svg = hold_layer, glow_layer, props_svg
        self.res = None

    def image(self):
        if self.res is None:
            import numpy as np
            from PIL import Image
            from engine import raster
            from engine import watercolor as WC
            hl = self.hold
            hold = raster.rasterize(hl.frames[0], W, SH)
            if hl.wc > 0:
                hold = WC.watercolor(hold, seed=hl.seed, strength=hl.wc, edge=hl.wc_edge)
            mask = raster.rasterize(self.props_svg.replace(S.BOIL_TOKEN, "1"), W, SH).getchannel("A")
            box = mask.getbbox()
            h = np.asarray(hold.crop(box), np.float32)
            g = np.asarray(raster.rasterize(self.glow.frames[0], W, SH).crop(box), np.float32)
            rgb = h[..., :3] + g[..., :3] * (g[..., 3:4] / 255.0)        # the glow layer blends additively
            a = np.asarray(mask.crop(box), np.float32)[..., None] * (h[..., 3:4] / 255.0)
            out = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
            self.res = (Image.fromarray(out, "RGBA"), box[:2])
        return self.res


def stick(fn, x, y, s, facing, how, **kw):
    """A plain lot stick in a figure's hand: 'up' (held up in the far hand), 'near' (hanging from the near hand)
    or 'carry' (held in both hands in front, being looked at)."""
    far, near = C.hand_positions(fn, x, y, s, facing, **kw)
    if how == "carry":
        hx, hy = (far[0] + near[0]) / 2, (far[1] + near[1]) / 2
        return PR.lot(hx + 4 * facing * s, hy - 10 * s, 0.9 * s, rot=-28 * facing)
    if how == "up":
        return PR.lot(far[0] + 3 * facing, far[1] - 26 * s, 0.9 * s, rot=-80 * facing)
    return PR.lot(near[0] + 2 * facing, near[1] + 24 * s, 0.9 * s, rot=82 * facing)


def keyed(keys_, curve="sine"):
    """Scalar keyframes [(t, v), ...] -> f(t), eased between keys."""
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


class ClimbSprite:
    """Jonah climbing up the hatch ladder, cut off below the hatch's front lip. The figure is rasterised once
    (lazily, cached on disk) on a small canvas and cropped per frame in stage space, so the cut stays fixed while
    he rises."""
    CW, CH, AX, AY = 360, 460, 180, 440

    def __init__(self, poses, seed=91):
        self.poses = poses        # list of (pose, facing, expr)
        self.seed = seed
        self.imgs = None

    def images(self):
        if self.imgs is None:
            from engine import raster
            from engine import watercolor as WC
            self.imgs = []
            for pose, facing, expr in self.poses:
                svg = S.svg_doc(C.jonah(self.AX, self.AY, 1.0, facing, pose=pose, expr=expr), w=self.CW, h=self.CH)
                im = raster.rasterize(svg.replace(S.BOIL_TOKEN, "1"), self.CW, self.CH)
                self.imgs.append(WC.watercolor(im, seed=self.seed))
        return self.imgs

    def frame(self, idx, x, y, clip_y):
        im = self.images()[idx]
        left, top = round(x - self.AX), round(y - self.AY)
        h = int(clip_y - top)
        if h <= 4:
            return None
        if h < self.CH:
            im = im.crop((0, 0, self.CW, h))
        return im, (left, top)


# ============================================================== build

def build(ctx):
    T = ctx.duration
    L = ctx.lines
    sc = Scene(ctx, W=W, H=SH)

    # ---------------------------------------------------------------- key times (all from the narration)
    # hold: the captain is already walking in from the right as the dark s04 frame dissolves into this one: on the
    # sack-bed level behind the ladder and the amphorae (feet clear of the subtitle band), at a steady pace, the
    # planted foot fixed on the floor (the drawing follows the distance walked). He arrives as the narrator names
    # him, bends down over two in-between drawings, kneels with a squash and wakes Jonah ("船长叫醒了他"); he rises
    # through an in-between and hops back to stand. Every main pose is held 0.3-0.5 s so a child can read it; the
    # camera widens only once he has knelt; the rise to the deck starts once Jonah is on his feet.
    FR = 1 / 30
    t_arr = round((L[0].start + 0.1) / FR) * FR      # first frame of the bend (the walk's last contact just before)
    t_ib2 = t_arr + 1.5 * FR                         # 2 frames per in-between
    t_crouch = t_arr + 3.5 * FR                      # kneels by Jonah's head (the boundaries sit between frames) ...
    t_situp = L[0].start + 0.74                      # Jonah sits up rubbing his eye; the captain stands back (same
    #                                                  frame: the sitting Jonah's head would cover the kneeler's face)
    t_rise = t_situp - 0.1                           # ... the captain starts to rise (3 frames) ...
    t_shake0, t_shake1 = t_crouch + 0.06, t_rise     # ... after shaking him
    t_cpoint = t_situp + 0.30                        # captain turns and points up the ladder
    t_standup = t_situp + 0.50                       # Jonah gets to his feet
    t_walk = t_standup + 0.36                        # ...and heads for the ladder
    t_pan0 = t_standup + 0.05                        # gentle rise to the deck (sine, ~1.4 s)
    t_pan1 = t_pan0 + 1.4
    # deck ("水手们抽签，签落在了约拿身上")
    t_glow = L[1].start + 0.45                       # the lot glows in Jonah's hand
    t_raise = t_glow - 0.1                           # ...which he holds up high
    t_draw = t_glow - 0.2                            # he pulls the last stick out of the pot
    t_reach = t_draw - 0.16                          # his hand goes to the last stick
    t_jwalk1 = t_reach - 0.02
    t_out = t_jwalk1 - 0.5                           # steps out of the hatch and walks to the pot
    t_climb0 = t_out - 0.38                          # head and shoulders rise through the hatch
    t_s1_reach = t_out - 0.36                        # S1 draws as the deck comes into view (before the pot turns)
    t_s1_lift = t_s1_reach + 0.24
    t_s1_stand = t_s1_lift + 0.28
    t_turn = t_out + 0.02                            # the pot-holder turns to offer the pot to Jonah
    t_jback0, t_jback1 = t_glow + 0.62, t_glow + 0.94   # holds the glowing lot up ~0.7 s, then steps back
    t_pot0, t_pot1 = t_glow + 0.2, t_glow + 0.4     # the pot-holder pulls the pot back to his side
    t_pt3, t_pt2 = t_glow + 0.4, t_glow + 0.46       # the two nearest sailors point
    t_react = [t_glow + 0.48, t_glow + 0.54, t_glow + 0.6]   # S1, S0, captain start back
    # Jonah's confession (lines 2-3)
    t_confess = L[2].start - 0.05
    t_listen = L[2].start + 0.35
    t_thunder = L[2].start + 1.70                    # in the pause between his two sentences
    t_sea = L[2].start + 1.88                        # "把我抛进海里吧"
    t_story_splash = t_sea + 0.55
    t_look0 = t_sea + 0.35                           # sailors exchange worried looks
    t_look1 = L[2].end - 0.25
    t_calm = L[3].start - 0.05                       # "海就会平静下来"
    t_open = L[3].start + 0.62                       # ...eyes open again, calm and brave
    t_l3 = L[3].start + 0.3

    # ---------------------------------------------------------------- outboard world (rocks against the ship)
    sc.add("sky", sky_layer(), z=0, wc=0.7)
    sc.add("sea_far", sea_far_layer(), z=0.5, motion=tilted(), wc=0.9)
    sc.add("clouds", clouds_layer(), z=1, motion=M.drift(vx=14), wc=0.8)

    # golden light from the cloud break when the lot falls on Jonah (God is never drawn, only light)
    beam_env = keyed([(t_glow - 0.06, 0.0), (t_glow + 0.55, 1.0), (t_confess + 0.6, 0.85), (t_sea - 0.2, 0.6),
                      (t_sea + 1.4, 0.3), (T, 0.26)])
    bdefs = (S.rad_grad("brk", [(0, "#ffd77e", 0.85), (0.45, "#ffbf55", 0.42), (1, "#ffbf55", 0)]) +
             S.lin_grad("rayg", [(0, "#ffd98a", 0.7), (1, "#ffbf55", 0.0)]))
    brk = (S.g('<ellipse cx="1650" cy="300" rx="420" ry="190" fill="url(#brk)"/>', filter="soft") +
           S.g(S.path(S.rays(1650, 290, 60, 520, n=13, width_deg=5, rot=8), fill="#ffd27a", stroke=False,
                      extra='opacity="0.4"'), filter="blur-md") +
           S.g('<ellipse cx="1650" cy="318" rx="250" ry="70" fill="#ffe2a0" opacity="0.5"/>', filter="blur-md"))
    sc.add("break_glow", doc(brk, bdefs), z=1.5, wc=0, motion=lambda t: Tf(alpha=beam_env(t)))

    sc.add("big_wave", big_wave_layer(), z=3, motion=tilted(M.combine(
        M.bob(26, 3.4, 0.1), lambda t: Tf(dx=18 * math.sin(2 * math.pi * t / 6.8)))))
    sc.add("sea_mid", sea_mid_layer(), z=4, motion=tilted(M.combine(M.bob(20, 3.4, 0.35), M.bob(46, 6.0, axis="x"))))

    # splashes over the rail: a few ambient bursts kept away from Jonah's face, and one story splash right where
    # he points when he says "把我抛进海里吧"
    splashes = [(L[0].end - 0.5, 2010, 0.7, 3, False), (L[2].start + 0.8, 1995, 0.82, 7, False),
                (t_story_splash, 1890, 1.12, 11, True), (min(L[3].start + 0.6, T - 2.1), 2030, 0.7, 5, False)]

    def splash_m(base, t0, dur=0.95):
        def m(t):
            u = (t - t0) / dur
            if not (0 <= u < 1):
                return Tf(alpha=0.0)
            s = 0.25 + 0.85 * M.ease("out")(min(1.0, u / 0.6))
            a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.5, 1.0, "sine"))
            return Tf(dy=50 * u * u, sx=s, sy=s, alpha=a, px=base[0], py=base[1])
        return tilted(m)
    for i, (ts, sx_, k, seed, story) in enumerate(splashes):
        base = (sx_, RAIL_TOP + 14)
        sc.add(f"splash{i}", splash_layer(base[0], base[1], seed, k), z=5 + 0.1 * i, motion=splash_m(base, ts),
               wc=0.3)
        if story:
            sc.sfx("splash", ts, gain_db=-11, pan=0.7)
        else:
            sc.sfx("splash_small", ts, gain_db=-16, pan=max(-0.8, min(0.8, (sx_ - 1056) / 1200)))

    # ---------------------------------------------------------------- ship
    sc.add("deck", deck_layer(), z=10)

    # Jonah climbing up through the hatch (cut off below the hatch lip)
    climb = ClimbSprite([("walk_a", -1, "worried"), ("walk_b", -1, "worried")])
    climb.images()                     # rasterise now (disk-cached) so render workers never need Chromium
    y_lo, y_hi = CLIP_Y + 338, JY + 5

    def climb_fn(t):
        if not (t_climb0 <= t < t_out):
            return None
        u = M.progress(t, t_climb0, t_out, "out")
        y = M.lerp(y_lo, y_hi, u)
        idx = int((t_out - t) / 0.19) % 2
        return climb.frame(idx, HX, y, CLIP_Y)
    sc.add_dynamic("jonah_climb", climb_fn, z=10.3)

    hg_defs = S.rad_grad("hg", [(0, "#ffcf86", 0.75), (0.5, "#f6a956", 0.28), (1, "#f2a95a", 0)])
    sc.add("hatch_glow", doc(f'<ellipse cx="{HX}" cy="{HATCH_F[2] - 30}" rx="190" ry="120" fill="url(#hg)"/>', hg_defs),
           z=10.4, blend="add", wc=0, motion=M.pulse(0.75, 1.0, 1.7))
    sc.add("split", doc(""), z=10.5, motion=M.still())
    sc.add("hold", hold_layer(), z=11)

    # ---------------------------------------------------------------- hold animation
    hx_, hy_ = HOLD_LAMP
    lan_sway = M.sway(7, 2.7, pivot=(hx_, hy_))
    hold_vis = lambda t: Tf(alpha=0.0 if t > t_pan1 + 0.2 else 1.0)          # noqa: E731
    glow_defs = S.rad_grad("lg", [(0, "#ffcf86", 0.34), (0.45, "#ffbf6a", 0.13), (1, "#ffbf6a", 0)])
    sc.add("hold_glow", doc(f'<ellipse cx="{hx_}" cy="{hy_ + 160}" rx="700" ry="520" fill="url(#lg)"/>', glow_defs),
           z=12, motion=M.combine(lan_sway, hold_vis), blend="add", wc=0)
    sc.add("hold_lantern", doc(PR.lantern(hx_, hy_, 1.0)), z=13, motion=M.combine(lan_sway, hold_vis))

    jx, jy = HJ
    js = HS
    kx = jx + 234 * js                     # the captain crouches on Jonah's other side (beyond his head)
    cap_back = 50                          # ...then stands and hops back
    shaking = lambda t: t_shake0 <= t <= t_shake1                            # noqa: E731

    # His walk (cap_walk_pose) on the bed level jy, right to left, ends with the far foot landing right of Jonah's
    # head (X_ARR); the anchor moves in CAP_DD steps, one per drawing, so the planted sole never slides.
    CAP_DD = 2 * CAP_A * js / CAP_N        # stage px per drawing
    CAP_P = 2 * FR                         # each drawing held 2 frames: 3 steps/s, ~620 output px/s
    X_ARR = 1604                           # anchor at the last contact (far foot at X_ARR - CAP_A * js)
    foot = X_ARR - CAP_A * js              # ...which stays planted through both in-betweens
    X_IB1, X_IB2 = 1588, 1572              # anchors of the in-betweens (the trailing foot steps in)

    def walk_k(t):
        """Index of the walk drawing on screen (0 = the last contact, negative = earlier drawings)."""
        return math.floor((t - t_arr) / CAP_P + 1.25)

    ib1 = C._P(t=16, h=-6, drop=24, legs=(("ik", (X_IB1 - foot) / js, 1), ("ik", (X_IB1 - 1622) / js, 1, 12)),
               arms=(("fk", 24, 52), ("fk", 30, 64)), hands=("open", "open"))
    ib2 = C._P(t=28, h=-10, drop=32, legs=(("ik", (X_IB2 - foot) / js, 1), ("ik", (X_IB2 - 1600) / js, 1)),
               arms=(("fk", 30, 52), ("ik", "abs", 96, -118, 1)), hands=("fist", "open"))
    rise = C._P(t=18, h=-6, drop=20, legs=(("ik", 46, 1), ("ik", -26, 1)),
                arms=(("fk", 10, 30), ("fk", 14, 36)), hands=("open", "open"))
    cap_sh = C.ground_shadow(kx, jy + 2, js)
    # walking + bending in: on its own layer BEHIND the ladder / amphorae cut-out (z 14.5, added at the end)
    walk_frames = [doc(captain_fig(kx, jy, js, -1, cap_walk_pose(k), label=f"walk{k}")) for k in range(2 * CAP_N)]
    walk_frames += [doc(cap_sh + captain_fig(kx, jy, js, -1, ib1, label="bend")),
                    doc(cap_sh + captain_fig(kx, jy, js, -1, ib2, label="reach"))]

    def cap_walk_at(t):
        if t < t_arr - 0.5 * FR:
            return float(walk_k(t) % (2 * CAP_N))
        return float(2 * CAP_N + (t >= t_ib2))

    def cap_walk_m(t):
        if t >= t_crouch:
            return Tf(alpha=0.0)
        if t < t_arr - 0.5 * FR:
            x = X_ARR - walk_k(t) * CAP_DD
        else:
            x = X_IB2 if t >= t_ib2 else X_IB1
        return Tf(dx=x - kx)

    def cap_m(t):
        """Kneel, rise, stand and point (in front of the props): breathing, a landing squash on the kneel, the
        shake, and a little hop back to his standing spot."""
        if t < t_crouch or t > t_pan1 + 0.2:
            return Tf(alpha=0.0)
        sy = 1 + 0.011 * math.sin(2 * math.pi * (t / 3.1 + 0.3))
        q = 1.0 if t < t_crouch + 0.085 else 1 - M.progress(t, t_crouch + 0.085, t_crouch + 0.21, "sine")
        sy *= 1 - 0.075 * q
        sx = 1 + 0.035 * q
        if shaking(t):
            return Tf(dx=7 * math.sin(2 * math.pi * 4.6 * t), sx=sx, sy=sy, px=kx, py=jy)
        if t >= t_situp:
            u = M.progress(t, t_situp, t_situp + 0.15, "linear")
            return Tf(dx=cap_back * M.ease("sine")(u), dy=-16 * math.sin(math.pi * u) - 8 * bump(t, t_cpoint),
                      sx=sx, sy=sy, px=kx, py=jy)
        return Tf(sx=sx, sy=sy, px=kx, py=jy)

    flip(sc, "hold_captain", [
        (t_crouch, C.captain(kx, jy, js, -1, pose="wake")),
        (t_rise, captain_fig(kx, jy, js, -1, rise, label="rise")),
        (t_situp, cap_sh + C.captain(kx, jy, js, -1, pose="stand", expr="worried")),
        (t_cpoint, cap_sh + C.captain(kx, jy, js, 1, pose="point", expr="worried")),
    ], z=14.6, motion=turned(cap_m, [t_cpoint], w=0.08))

    jsx = jx + 155                         # where he sits up / stands (head stays near the pillow)
    hold_j = [
        (0, C.jonah(jx, jy, js, -1, pose="sleep", marks=False)),
        (t_situp, C.jonah(jsx, jy, js, -1, pose="wake")),
        (t_standup, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="stand", expr="surprised")),
        (t_walk, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="walk_a", expr="worried")),
        (t_walk, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="walk_b", expr="worried")),
    ]

    def hold_j_at(t):
        if t >= t_walk:
            return 3.0 + (int((t - t_walk) / 0.2) % 2)
        return float(max(i for i, (tk, _) in enumerate(hold_j[:3]) if t >= tk))

    def hold_j_extra(t):
        # hidden once the climbing Jonah rises through the hatch (the tilt can still show this one's head)
        if t > t_pan1 + 0.2 or t >= t_climb0:
            return Tf(alpha=0.0)
        if shaking(t):
            return Tf(dx=6 * math.sin(2 * math.pi * 4.6 * t - 0.5), rot=1.2 * math.sin(2 * math.pi * 4.6 * t - 0.5))
        if t >= t_walk:
            return Tf(dx=330 * (t - t_walk), dy=-6 * abs(math.sin(math.pi * (t - t_walk) / 0.2)))
        return Tf(dy=-8 * (bump(t, t_situp) + bump(t, t_standup)))
    # pivot on the sleeper, then on the sitting / standing Jonah (jsx), who turns round as he gets up
    flip(sc, "hold_jonah", hold_j, z=15, frame_at=hold_j_at,
         motion=turned(alive(jx, jy, [t_situp, t_standup], 0.0, amp=0.008, extra=hold_j_extra), [t_standup],
                       w=0.08, px=lambda t: jx if t < t_situp else jsx))

    # Z z z still drifting up from the sleeper (continues s04), fading as the captain arrives
    head = (jx + 157 * js / 1.15, jy - 92)
    for i, delay in enumerate((0.0, 0.9)):
        zsvg = doc(S.text(head[0] + 40, head[1] - 40, "Z", size=54, fill="#fff3d6",
                          extra=f'stroke="{S.INK}" stroke-width="6" paint-order="stroke"'))

        def zm(t, delay=delay):
            per = 1.8
            u = ((t + delay) % per) / per
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine"))
            a *= 1 - M.progress(t, L[0].start - 0.18, L[0].start + 0.12, "sine")
            s = 0.5 + 0.7 * u
            return Tf(50 + 120 * u + 18 * math.sin(u * 6.0), -20 - 210 * u, -12 + 22 * u, s, s, a,
                      head[0] + 40, head[1] - 55)
        sc.add(f"zz{i}", zsvg, wc=0, z=14.15, motion=zm)   # behind the captain walking past them

    # ---------------------------------------------------------------- deck characters
    mlx, mly = MAST_X + 29 + 47, 610
    sc.add("deck_lantern", doc(PR.lantern(mlx, mly, 0.8)), z=20, motion=M.sway(9, 2.9, pivot=(mlx, mly)))
    sc.add("deck_props", deck_props_layer(), z=20.5)

    # the pot, held out at arm's length by S3 (by its lip): first to S1 (facing left), then to Jonah (facing
    # right); after the lot glows he pulls it back to his side and points with the free hand
    s3x, s3y, s3s = S3

    def pot_held(facing, hand=0):
        h = C.hand_positions(C.sailor, s3x, s3y, s3s, facing, variant=3, pose="point")[hand]
        return (h[0] + (40 * facing if hand == 0 else 4 * facing) * POT_S, h[1] + 72 * POT_S)
    pot_l, pot_r, pot_side = pot_held(-1), pot_held(1), pot_held(1, hand=1)
    # S1 reaches into the pot (his pointing hand at the sticks) during "水手们抽签"
    s1x, s1y, s1s = S1
    s1h = C.hand_positions(C.sailor, 0, s1y, s1s, 1, variant=0, pose="point")[0]
    s1x = pot_l[0] - s1h[0]
    # the last stick (lots_jar(sticks=1): from the mouth (0,-56) to the tip (-25.5,-132.4), see props._lots_jar):
    # Jonah's drawing hand closes on it just above the lip
    jhand = C.hand_positions(C.jonah, 0, 0, 1.0, -1, pose="point")[0]
    mouth = (pot_r[0], pot_r[1] - 56 * POT_S)
    tip = (pot_r[0] - 25.5 * POT_S, pot_r[1] - 132.4 * POT_S)
    hy = JY + jhand[1]
    u_ = (mouth[1] - hy) / (mouth[1] - tip[1])
    JX0 = mouth[0] + u_ * (tip[0] - mouth[0]) - jhand[0]   # Jonah's spot while drawing
    jxe = JEND
    JSTEP = JEND - JX0

    def sailor_frames(x, y, s, variant, keys_):
        out = []
        for t, pose, facing, expr, held in keys_:
            mk = C.ground_shadow(x, y + 2, s) + C.sailor(x, y, s, facing, variant=variant, pose=pose, expr=expr)
            if held:
                mk += stick(C.sailor, x, y, s, facing, held, variant=variant, pose=pose)
            out.append((t, mk))
        return out

    # S2 (back row, behind-right of S3): holds his plain stick down, watches the hatch, then points at Jonah
    s2x, s2y, s2s = S2
    k2 = [(0, "stand", 1, "worried", "near"), (t_pt2, "point", 1, "surprised", None),
          (t_listen + 0.08, "stand", 1, "worried", None), (t_look0 - 0.05, "scared", 1, None, None),
          (t_look1 + 0.06, "stand", -1, "worried", None), (t_l3 + 0.2, "stand", 1, "worried", None)]
    flip(sc, "s2", sailor_frames(s2x, s2y, s2s, 2, k2), z=21, motion=alive(s2x, s2y, [k[0] for k in k2[1:]], 0.55))

    # S0 (back row, left): crouched over the plain stick he drew (facing away), then starts back
    s0x, s0y, s0s = S0
    k0 = [(0, "carry", -1, "worried", "carry"), (t_react[1], "scared", 1, "surprised", None),
          (t_listen + 0.24, "stand", 1, "worried", None), (t_look0 + 0.1, "stand", -1, "worried", None),
          (t_l3 + 0.1, "stand", 1, "worried", None)]
    flip(sc, "s0", sailor_frames(s0x, s0y, s0s, 1, k0), z=21.5,
         motion=alive(s0x, s0y, [k[0] for k in k0[1:]], 0.8,
                      extra=lambda t: Tf(dx=-22 * M.progress(t, t_react[1], t_react[1] + 0.25, "out"))))

    # S1 (middle row): draws during "水手们抽签": hand in the pot, lifts the stick briefly, then holds it down
    k1 = [(0, "stand", 1, "worried", None), (t_s1_reach, "point", 1, "worried", None),
          (t_s1_lift, "lift", 1, "worried", "up"), (t_s1_stand, "stand", 1, "worried", "near"),
          (t_react[0], "stand", 1, "surprised", None), (t_listen + 0.16, "stand", 1, "worried", None),
          (t_look0 + 0.06, "stand", 1, "sad", None), (t_l3, "stand", 1, "worried", None)]

    def s1_extra(t):
        u = M.progress(t, t_react[0], t_react[0] + 0.25, "out") * (1 - M.progress(t, t_listen, t_listen + 0.6, "sine"))
        return Tf(dx=-28 * M.progress(t, t_react[0], t_react[0] + 0.25, "out"), rot=-4.5 * u)
    flip(sc, "s1", sailor_frames(s1x, s1y, s1s, 0, k1), z=22,
         motion=alive(s1x, s1y, [k[0] for k in k1[1:]], 0.2, extra=s1_extra))

    # Jonah on deck (frames drawn at his drawing spot JX0; the motion walks him in and steps him back)
    def jframe(pose, facing, expr, lot=None):
        mk = C.ground_shadow(JX0, JY + 2, 1.0) + C.jonah(JX0, JY, 1.0, facing, pose=pose, expr=expr)
        if lot:
            where, marked = lot
            far, near = C.hand_positions(C.jonah, JX0, JY, 1.0, facing, pose=pose)
            if where in ("up", "fist"):  # sticking up out of the fist (raised hand, or just pulled out)
                mk += PR.lot(far[0] + 2 * facing, far[1] - 30, 1.1, rot=-78 * facing, marked=marked)
            elif where == "chest":     # pressed to his chest: "it's me"
                mk += PR.lot(near[0] - 4 * facing, near[1] + 4, 1.1, rot=-24 * facing, marked=marked)
            else:                      # hanging from the near hand
                mk += PR.lot(near[0] + 2 * facing, near[1] + 26, 1.0, rot=84 * facing, marked=marked)
        return mk
    jfr = [jframe("walk_a", -1, "worried"), jframe("walk_b", -1, "worried"),
           jframe("point", -1, "worried"), jframe("point", -1, "worried", ("fist", False)),
           jframe("preach", -1, "worried", ("up", False)), jframe("preach", -1, "surprised", ("up", True)),
           jframe("confess", -1, "surprised", ("chest", True)),
           jframe("confess", -1, "sorry", ("chest", True)),
           jframe("point", 1, "sad", ("near", True)),
           jframe("confess", -1, "peaceful", ("chest", True)),
           jframe("confess", -1, "neutral", ("chest", True))]

    def j_at(t):
        if t < t_reach:
            return float(int(max(0.0, t - t_out) / 0.14) % 2)
        if t < t_draw:
            return 2.0
        if t < t_raise:
            return 3.0
        if t < t_glow:
            return 4.0
        if t < t_glow + 0.16:
            return 4.0 + (t - t_glow) / 0.16
        for tk, idx in ((t_open, 10), (t_calm, 9), (t_sea, 8), (t_confess, 7), (t_jback0, 6)):
            if t >= tk:
                return float(idx)
        return 5.0
    jwalk_dx = keyed([(t_out, HX - JX0), (t_jwalk1, 0.0)], "linear")

    def jstep(t):
        return JSTEP * M.progress(t, t_jback0, t_jback1, "sine")

    def j_extra(t):
        if t < t_out:
            return Tf(alpha=0.0)
        if t < t_jwalk1:
            u = (t - t_out) / (t_jwalk1 - t_out)
            return Tf(dx=jwalk_dx(t), dy=(y_hi - JY) * (1 - u) - 5 * abs(math.sin(math.pi * (t - t_out) / 0.14)))
        u = M.progress(t, t_jback0, t_jback1, "sine")
        lift = 8 * math.sin(math.pi * M.progress(t, t_raise, t_raise + 0.2, "linear"))   # yanks the lot up
        return Tf(dx=jstep(t), dy=-10 * math.sin(math.pi * u) - lift)
    jswitch = [t_reach, t_raise, t_jback0, t_confess, t_sea, t_calm, t_open]
    # he turns round like a paper cut-out to point at the sea and back (no bare mirror pop of the figure + lot)
    sc.add("jonah", [doc(f) for f in jfr], z=23, frame_at=j_at,
           motion=turned(alive(JX0, JY, jswitch, 0.1, extra=j_extra), (t_sea, t_calm)))

    # warm light on Jonah: a gold wash in the beam (normal blend keeps it gold over the blue) + small highlights
    wdefs = (S.lin_grad("beamw", [(0, "#ffbf55", 0.5), (0.35, "#ffcb6a", 0.32), (0.8, "#ffd98a", 0.12),
                                   (1, "#ffd98a", 0.0)]) +
             S.lin_grad("beamh", [(0, "#fff0c0", 0.0), (0.25, "#ffe7a8", 0.3), (0.85, "#ffe29a", 0.1),
                                  (1, "#ffe39a", 0.0)]) +
             S.rad_grad("jg", [(0, "#ffe2a0", 0.55), (0.45, "#ffd27a", 0.25), (1, "#ffd27a", 0)]) +
             S.rad_grad("pool", [(0, "#ffc85e", 0.5), (1, "#ffc85e", 0)]))
    sc.add("beam_wash", doc(S.g(f'<path d="M1500,250 L1800,250 L{jxe + 230},1010 L{jxe - 240},1010 Z" '
                                f'fill="url(#beamw)"/>', filter="blur-md") +
                            f'<ellipse cx="{jxe}" cy="{JY + 4}" rx="230" ry="46" fill="url(#pool)"/>', wdefs),
           z=19, wc=0, motion=lambda t: Tf(alpha=beam_env(t)))
    sc.add("beam_hi", doc(S.g(f'<path d="M1580,260 L1720,260 L{jxe + 110},990 L{jxe - 120},990 Z" '
                              f'fill="url(#beamh)"/>', filter="blur-md"), wdefs),
           z=19.1, wc=0, blend="add", motion=lambda t: Tf(alpha=beam_env(t)))
    sc.add("jonah_glow", doc(f'<ellipse cx="{JX0}" cy="{JY - 190}" rx="250" ry="320" fill="url(#jg)"/>', wdefs),
           z=22.9, wc=0, blend="add",
           motion=lambda t: Tf(dx=jstep(t), alpha=beam_env(t) * (0.8 + 0.2 * math.sin(2 * math.pi * t / 1.3))))

    # captain (front row, far left: out of frame until the camera widens at the reveal)
    cx_, cy_, cs_ = CAPT
    kc = [(0, "stand", "worried"), (t_react[2], "worried", "surprised"), (t_listen + 0.3, "stand", "worried"),
          (t_look0 + 0.2, "worried", None), (t_l3 + 0.15, "stand", "worried")]
    flip(sc, "captain", [(t, C.ground_shadow(cx_, cy_ + 2, cs_) + C.captain(cx_, cy_, cs_, 1, pose=p, expr=e))
                         for t, p, e in kc], z=24,
         motion=alive(cx_, cy_, [k[0] for k in kc[1:]], 0.65,
                      extra=lambda t: Tf(alpha=1.0 if t >= t_pan1 else 0.0)))

    # S3 (front row): holds the pot out to S1, turns and offers it to Jonah, then points at him
    k3 = [(0, "point", -1, "worried"), (t_turn, "point", 1, "worried"), (t_pt3, "point", 1, "surprised"),
          (t_listen, "stand", 1, "worried"), (t_look0, "stand", -1, "worried"), (t_look1, "stand", 1, "worried")]
    flip(sc, "s3", [(t, C.ground_shadow(s3x, s3y + 2, s3s) + C.sailor(s3x, s3y, s3s, f, variant=3, pose=p, expr=e))
                    for t, p, f, e in k3], z=25, motion=alive(s3x, s3y, [k[0] for k in k3[1:]], 0.4))

    # the pot: 2 sticks (S1's and Jonah's), 1 after S1 draws, 0 after Jonah draws; it swings round with S3's turn
    # and ends hanging from his near hand (later he holds it at his side while standing)
    pot_frames = [(0, PR.lots_jar(pot_l[0], pot_l[1], POT_S, sticks=2)),
                  (t_s1_lift, PR.lots_jar(pot_l[0], pot_l[1], POT_S, sticks=1)),
                  (t_draw, PR.lots_jar(pot_l[0], pot_l[1], POT_S, sticks=0))]
    stand_side = C.hand_positions(C.sailor, s3x, s3y, s3s, 1, variant=3, pose="stand")[1]
    pot_stand = (stand_side[0] + 4 * POT_S, stand_side[1] + 72 * POT_S)
    pot_stand_l = C.hand_positions(C.sailor, s3x, s3y, s3s, -1, variant=3, pose="stand")[1]
    pot_stand_l = (pot_stand_l[0] - 4 * POT_S, pot_stand_l[1] + 72 * POT_S)
    pdx = keyed([(t_turn - 0.14, 0.0), (t_turn + 0.14, pot_r[0] - pot_l[0]), (t_pot0, pot_r[0] - pot_l[0]),
                 (t_pot1, pot_side[0] - pot_l[0]), (t_listen - 0.01, pot_side[0] - pot_l[0]),
                 (t_listen, pot_stand[0] - pot_l[0]), (t_look0 - 0.01, pot_stand[0] - pot_l[0]),
                 (t_look0, pot_stand_l[0] - pot_l[0]), (t_look1 - 0.01, pot_stand_l[0] - pot_l[0]),
                 (t_look1, pot_stand[0] - pot_l[0])], "sine")
    pdy = keyed([(t_turn - 0.14, 0.0), (t_turn, -36.0), (t_turn + 0.14, 0.0), (t_pot0, 0.0),
                 (t_pot1, pot_side[1] - pot_l[1]), (t_listen - 0.01, pot_side[1] - pot_l[1]),
                 (t_listen, pot_stand[1] - pot_l[1]), (t_look0 - 0.01, pot_stand[1] - pot_l[1]),
                 (t_look0, pot_stand_l[1] - pot_l[1]), (t_look1 - 0.01, pot_stand_l[1] - pot_l[1]),
                 (t_look1, pot_stand[1] - pot_l[1])], "sine")
    jiggle = [t_s1_lift, t_draw, t_pot1]
    flip(sc, "pot", pot_frames, z=25.5,
         motion=lambda t: Tf(pdx(t), pdy(t), sum(3.0 * math.sin(2 * math.pi * 7 * (t - tj)) * max(0.0, 1 - abs(t - tj) / 0.25)
                                                 for tj in jiggle), px=pot_l[0], py=pot_l[1]))

    sc.add("deck_fg", deck_foreground(), z=30)

    # ---------------------------------------------------------------- camera
    hold_mid = Cam(CAM_HOLD0.x - 6, CAM_HOLD0.y, CAM_HOLD0.w + 10)
    # the widening waits until the captain has knelt (after the s04 dissolve, apart from his walk and bend-in)
    cam_keys = [(0.0, CAM_HOLD0), (t_crouch, hold_mid), (t_crouch + 0.65, CAM_HOLD1),
                (t_pan0, Cam(CAM_HOLD1.x - 4, CAM_HOLD1.y + 2, CAM_HOLD1.w + 8)), (t_pan1, CAM_DECK),
                (t_glow + 0.25, Cam(CAM_DECK.x - 5, CAM_DECK.y - 4, CAM_DECK.w + 10)),
                (t_glow + 1.3, CAM_WIDE), (t_confess, CAM_WIDE), (L[3].start - 0.1, CAM_PUSH), (T, CAM_END)]
    cam_base = M.cam_keys(cam_keys, "sine")
    roll0 = -0.6                           # s04 ends with the hold tilted ~0.4-0.9 deg clockwise

    def cam(t):
        c = cam_base(t)
        k = M.progress(t, 0.6, 2.0, "sine")
        return Cam(c.x, c.y, c.w, roll0 * (1 - k) + k * 0.3 * math.sin(2 * math.pi * t / 5.4 + 2.2))
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    sc.fx = [
        rain_fx(),
        FX.lightning([t_thunder], dur=0.5, strength=0.22),
        FX.sparkles((jxe - 170, JY - 400, jxe + 170, JY - 40), count=24, t0=t_glow - 0.05, t1=t_sea + 0.6,
                    color=(255, 226, 140), size=(8, 18), period=1.3, drift=-18, seed=5),
        FX.motes((850, 1380, 1950, FLOOR - 30), count=26, t1=t_pan1, color=(255, 228, 170), size=(3, 6), alpha=130),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_storm", 0, dur=T + 0.8, gain_db=-14, fade_in=0.8, fade_out=1.0)
    sc.sfx("storm_wind", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("rain", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("ship_creak", 0, dur=t_pan1 + 0.5, gain_db=-15, fade_in=0.6, fade_out=0.8)
    sc.sfx("footsteps_run", 0.0, dur=t_arr + 0.1, gain_db=-16, pan=0.35, fade_in=0.3, fade_out=0.15,
           rate=1 / (CAP_N * CAP_P))      # his steps (one per CAP_N drawings)
    sc.sfx("cloth", t_standup - 0.05, gain_db=-8)
    sc.sfx("footsteps_run", t_walk, dur=0.7, gain_db=-17, pan=0.3, fade_out=0.4)
    sc.sfx("lots", t_s1_reach, gain_db=-8, pan=0.05)
    sc.sfx("footsteps", t_out, dur=t_jwalk1 - t_out + 0.1, gain_db=-17, pan=0.45, fade_out=0.15)
    sc.sfx("lots", t_reach - 0.04, gain_db=-9, pan=0.3)
    sc.sfx("sparkle", t_glow - 0.04, gain_db=-7, pan=0.35)
    for tt in (t_sea, t_calm):             # soft robe swish on his two turns (under his own voice)
        sc.sfx("cloth", tt - 0.05, gain_db=-14, pan=0.35)
    sc.sfx("thunder", t_thunder, dur=2.4, gain_db=-14, pan=0.4, fade_out=1.2)

    # ---------------------------------------------------------------- the captain's walk-in (added last: the
    # watercolour seeds of the layers above stay as they were)
    sc.add("hold_captain_walk", walk_frames, z=14.2, frame_at=cap_walk_at, motion=cap_walk_m, seed=171)
    hold_l = next(l for l in sc.layers if l.name == "hold")
    glow_l = next(l for l in sc.layers if l.name == "hold_glow")
    jars, ladder, end_sack = hold_front_props()
    front = FrontCutout(hold_l, glow_l, doc(jars + ladder + end_sack))
    front.image()                      # rasterise now (disk-cached) so render workers never need Chromium
    sc.add_dynamic("hold_front", lambda t: front.image() if t < t_crouch else None, z=14.5)
    return sc


# ============================================================== rain (deck only)

def rain_fx(density=1.0, seed=8):
    """Slanted rain that only falls outdoors (above the deck's cut edge)."""
    import numpy as np
    from PIL import Image, ImageDraw
    from engine.paths import OUT_H, OUT_W

    n = int(360 * density)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = 1650 * rng.uniform(0.75, 1.25, n)
    ln = 44 * rng.uniform(0.6, 1.3, n)
    al = rng.uniform(70, 130, n).astype(int)
    a = math.radians(13)
    dx, dy = math.sin(a), math.cos(a)
    m = 40
    spx = rng.uniform(80, W - 80, m)
    spy = rng.uniform(DECK_BACK + 20, DECK_CUT - 20, m)
    sph = rng.uniform(0, 1, m)

    def fx(frame, t, view):
        _, ycut = view.to_out(1090, DECK_CUT)
        if ycut <= 0:
            return frame
        ylim = min(OUT_H, int(ycut))
        ov = Image.new("RGBA", (OUT_W, ylim), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0 + sp * t) % (OUT_H + 80) - 40
        x = (x0 - sp * t * dx / dy) % (OUT_W + 400) - 200
        for i in range(n):
            if y[i] > ylim:
                continue
            ye = min(y[i] + ln[i] * dy, ylim)
            xe = x[i] + (ye - y[i]) * dx / dy
            d.line([(x[i], y[i]), (xe, ye)], fill=(226, 234, 242, int(al[i])), width=2)
        for i in range(m):
            ph = (t * 2.2 + sph[i]) % 1.0
            if ph > 0.3:
                continue
            ox, oy = view.to_out(spx[i], spy[i])
            if oy > ylim - 2:
                continue
            r = (3 + 14 * ph / 0.3) * view.scale
            aa = int(150 * (1 - ph / 0.3))
            d.arc([ox - r, oy - r * 0.45, ox + r, oy + r * 0.45], 190, 350, fill=(232, 240, 245, aa), width=2)
        frame.alpha_composite(ov, (0, 0))
        return frame
    return fx
