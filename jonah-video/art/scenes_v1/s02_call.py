"""Scene 2 — God calls Jonah (Jonah 1:1-2).

Jonah's home village in the green-gold hills of Israel on a fresh morning: flat-roofed houses, olive trees,
grazing sheep, a dirt road winding away east (right). Jonah stands outside his house with a scroll while the
camera drifts in (line 0). As the narrator says "God said to him" the clouds above him part and warm golden
rays pour down with sparkles; Jonah looks up, hand at his ear, surprised (line 1). While God speaks the light
pulses gently and a picture-book vision opens in a soft cloud bubble in the eastern sky: the great city of
Nineveh (line 2); a small grey cloud of wrongdoing gathers over it and Jonah becomes worried (line 3).
God is never drawn — only light, sparkles and his voice.

Scale: Jonah 1.2 (~400 px), his house 1.15 (door ~405 px), sheep 0.78-0.95, a big olive tree framing the
right edge; the house is its own layer after the sky so the parting cloud bank passes behind its roof.
Jonah's pose / face changes are hard switches sold by a small squash, hop or dip (no crossfaded doubles);
on "你要去警告他们" he puts a hand to his chest ("me?"). The sheep keep their hooves planted: only their
heads turn, on their own layers.

All events are keyed to ctx.lines[i].start / .end (nothing hard-coded to the voice take).
"""
import math

from art import characters as CH
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

# ------------------------------------------------------------------ stage & layout (stage px)
SW, SH = 2400, 1350          # a little larger than the default stage so the camera can travel

JX, JY, JS = 960, 1150, 1.2   # Jonah: ground anchor, scale (~400 px tall)
HOUSE = (330, 1088, 1.15)     # Jonah's house (variant 3), ground anchor: door ~405 px, matches Jonah
HOUSE_SRC = (360, 1088, 0.95)  # the house placement the hand-drawn house details were authored for
GAP = (990, 215)              # where the clouds part (source of the light)
BX, BY = 1672, 418            # centre of the vision window
RX, RY = 304, 188             # vision window radii
SKY_SEED = 2                  # nineveh_skyline seed for the vision

# near meadow: sheep (x, ground y, scale, facing) at about person scale for their depth
SHEEP = [(1515, 1082, 0.95, -1), (1730, 1050, 0.86, 1), (2000, 1036, 0.78, -1)]
TREE = (2175, 1188, 1.55)     # the big olive tree framing the right edge
FG_TUFTS = [(40, 1330, 2, 1.5), (170, 1345, 0, 1.6), (300, 1352, 2, 1.3), (2150, 1345, 0, 1.5),
            (2270, 1330, 2, 1.6), (2390, 1342, 0, 1.5)]


def _house_tf():
    """SVG transform that maps the authored house-detail coordinates onto the current HOUSE placement."""
    (ox, oy, os_), (hx, hy, hs) = HOUSE_SRC, HOUSE
    return f"translate({hx},{hy}) scale({hs / os_:.5f}) translate({-ox},{-oy})"


def _hp(x, y):
    """A point given in the authored house-detail coordinates -> stage px for the current HOUSE."""
    (ox, oy, os_), (hx, hy, hs) = HOUSE_SRC, HOUSE
    k = hs / os_
    return hx + (x - ox) * k, hy + (y - oy) * k


def _doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def _f(v):
    return f"{v:.1f}"


# ------------------------------------------------------------------ drawing helpers
def _ridge(pts, fill, sw=3.0, ink=None, bottom=SH + 80, extra=""):
    """Closed land shape whose top edge runs through pts."""
    d = S.smooth_path(pts, closed=False) + f" L{_f(pts[-1][0])},{bottom} L{_f(pts[0][0])},{bottom} Z"
    ink = ink or P["ink"]
    return (f'<path d="{d}" fill="{fill}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round" '
            f'stroke-linecap="round" {extra}/>')


def _stroke(d, color, w, opacity=1.0, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}" {extra}/>')


def _fan(cx, cy, length, angles, widths):
    """Light-ray wedges fanning out from (cx, cy); angles in degrees (90 = straight down)."""
    d = ""
    for a, w in zip(angles, widths):
        a0, a1 = math.radians(a - w / 2), math.radians(a + w / 2)
        am = math.radians(a)
        p0 = (cx + 18 * math.cos(am - 1.2), cy + 18 * math.sin(am - 1.2))
        p3 = (cx + 18 * math.cos(am + 1.2), cy + 18 * math.sin(am + 1.2))
        p1 = (cx + length * math.cos(a0), cy + length * math.sin(a0))
        p2 = (cx + length * math.cos(a1), cy + length * math.sin(a1))
        d += f"M{_f(p0[0])},{_f(p0[1])} L{_f(p1[0])},{_f(p1[1])} L{_f(p2[0])},{_f(p2[1])} L{_f(p3[0])},{_f(p3[1])} Z "
    return d


def _cumulus(circles, base, hi, under, sw=3.5, glow=None, uid="c"):
    """One puffy cloud silhouette from overlapping circles (x, y, r): a single outer ink line, a lighter
    top-left highlight on every puff, a soft shaded underside and an optional golden glow (gx, gy, r, a)."""
    xs = [c[0] for c in circles]
    ys = [c[1] + c[2] for c in circles]
    bx0, bx1, by = min(xs), max(xs), max(ys)
    base_el = (sum(xs) / len(xs), by - 18, (bx1 - bx0) / 2 + 10, 30)

    def shapes(attrs, k=1.0, dy=0.0, dx=0.0):
        out = (f'<ellipse cx="{_f(base_el[0])}" cy="{_f(base_el[1])}" rx="{_f(base_el[2])}" ry="{_f(base_el[3])}" '
               f'{attrs}/>') if k == 1.0 else ""
        for x, y, r in circles:
            out += f'<circle cx="{_f(x + dx * r)}" cy="{_f(y + dy * r)}" r="{_f(r * k)}" {attrs}/>'
        return out

    cid = f"cl{uid}"
    defs = f'<clipPath id="{cid}">{shapes("")}</clipPath>'
    body = shapes(f'fill="{base}" stroke="{P["ink"]}" stroke-width="{sw * 2}"') + shapes(f'fill="{base}"')
    inner = f'<rect x="{_f(bx0 - 200)}" y="{_f(by - 60)}" width="{_f(bx1 - bx0 + 400)}" height="90" fill="{under}" opacity="0.75" filter="url(#soft)"/>'
    inner += shapes(f'fill="{hi}" opacity="0.9"', k=0.8, dy=-0.2, dx=-0.08)
    if glow:
        gx, gy, gr, ga = glow
        inner += f'<circle cx="{_f(gx)}" cy="{_f(gy)}" r="{_f(gr)}" fill="#ffd36e" opacity="{ga}" filter="url(#blur-lg)"/>'
    body += f'<g clip-path="url(#{cid})">{inner}</g>'
    return f"<defs>{defs}</defs>" + body


LEFT_CL = [(470, 262, 62), (560, 220, 88), (668, 186, 112), (782, 206, 98), (872, 244, 70), (610, 270, 60),
           (740, 268, 66), (920, 276, 46)]
RIGHT_CL = [(1092, 270, 50), (1160, 236, 78), (1268, 190, 110), (1382, 214, 92), (1468, 252, 64),
            (1222, 276, 60), (1340, 274, 62)]


def _cloud_bank(circles, gold, uid):
    base = S.mix("#f7efe2", "#ffe2a0", 0.5 * gold)
    hi = S.mix("#fffaf0", "#fff4cf", 0.6 * gold)
    under = S.mix("#e2d3c8", "#f2c27a", 0.55 * gold)
    glow = (GAP[0], GAP[1] + 20, 260, 0.75 * gold) if gold > 0 else None
    return S.g(_cumulus(circles, base, hi, under, glow=glow, uid=f"{uid}{int(gold * 10)}"), filter="wobble")


def _tiny_olive(x, y, s, seed=0):
    """Distant olive tree: a trunk and two or three grey-green blobs (cheap)."""
    c = S.mix(P["olive"], "#cfd9bf", 0.35)
    out = _stroke(f"M{_f(x)},{_f(y)} Q{_f(x - 4 * s)},{_f(y - 22 * s)} {_f(x + 2 * s)},{_f(y - 40 * s)}",
                  S.mix(P["ink_soft"], "#9b8f80", 0.4), 6 * s)
    for i, (ox, oy, r) in enumerate([(-14, -52, 22), (12, -58, 24), (0, -72, 20)]):
        out += (f'<path d="{S.blob(x + ox * s, y + oy * s, r * s, r * 0.8 * s, 0.12, 8, seed + i)}" fill="{c}" '
                f'stroke="{S.mix(P["ink"], c, 0.45)}" stroke-width="{2.4 * s:.1f}"/>')
    return out


def _olive(x, y, s, seed=0, haze=0.0):
    """Mid-distance olive tree without fruit dots: twisted trunk, three silvery-green leaf clumps."""
    import random
    r = random.Random(seed)
    leaf = S.mix(S.mix(P["olive"], "#a9b98c", 0.35), "#dfe6cf", haze)
    leaf_hi = S.mix(leaf, "#eef3dc", 0.45)
    bark = S.mix("#8c7a66", "#cfd3c0", haze)
    ink = S.mix(P["ink"], leaf, 0.25 + 0.4 * haze)
    lw = 3.2 * s
    out = (f'<path d="M{_f(x - 9 * s)},{_f(y)} C{_f(x - 4 * s)},{_f(y - 30 * s)} {_f(x - 16 * s)},{_f(y - 50 * s)} '
           f'{_f(x - 30 * s)},{_f(y - 78 * s)} M{_f(x - 2 * s)},{_f(y - 36 * s)} C{_f(x + 8 * s)},{_f(y - 58 * s)} '
           f'{_f(x + 20 * s)},{_f(y - 66 * s)} {_f(x + 32 * s)},{_f(y - 84 * s)}" fill="none" stroke="{ink}" '
           f'stroke-width="{_f(15 * s)}" stroke-linecap="round"/>')
    out += (f'<path d="M{_f(x - 9 * s)},{_f(y)} C{_f(x - 4 * s)},{_f(y - 30 * s)} {_f(x - 16 * s)},{_f(y - 50 * s)} '
            f'{_f(x - 30 * s)},{_f(y - 78 * s)} M{_f(x - 2 * s)},{_f(y - 36 * s)} C{_f(x + 8 * s)},{_f(y - 58 * s)} '
            f'{_f(x + 20 * s)},{_f(y - 66 * s)} {_f(x + 32 * s)},{_f(y - 84 * s)}" fill="none" stroke="{bark}" '
            f'stroke-width="{_f(9 * s)}" stroke-linecap="round"/>')
    for i, (ox, oy, rx, ry) in enumerate([(-38, -92, 46, 32), (34, -100, 50, 34), (-2, -128, 48, 34)]):
        ox += r.uniform(-6, 6)
        d = S.blob(x + ox * s, y + oy * s, rx * s, ry * s, 0.13, 9, seed * 7 + i)
        out += f'<path d="{d}" fill="{leaf}" stroke="{ink}" stroke-width="{_f(lw)}"/>'
        d2 = S.blob(x + (ox - 10) * s, y + (oy - 9) * s, rx * 0.5 * s, ry * 0.42 * s, 0.15, 7, seed * 7 + i + 3)
        out += f'<path d="{d2}" fill="{leaf_hi}" opacity="0.8"/>'
    out += f'<ellipse cx="{_f(x)}" cy="{_f(y + 2 * s)}" rx="{_f(60 * s)}" ry="{_f(7 * s)}" fill="{P["grass_dark"]}" opacity="0.25"/>'
    return out


def _olive_big(x, y, s=1.0, seed=0):
    """Near olive tree (about 400 x 380 px at s=1): gnarled trunk with a knot hole, three limbs, silvery
    leaf clumps with leaf slivers and a few scattered single olives (no paired dots that read as eyes)."""
    import random
    r = random.Random(seed)

    def X(v):
        return _f(x + v * s)

    def Y(v):
        return _f(y + v * s)

    ink = P["ink"]
    bark, bark_d = "#9c8e7c", "#7d6f5f"
    out = ""
    limbs = [((-14, -128), (-60, -170), (-110, -215)), ((0, -136), (-6, -210), (8, -270)),
             ((14, -124), (70, -160), (124, -205))]
    for (a, b, c) in limbs:
        d = f"M{X(a[0])},{Y(a[1])} Q{X(b[0])},{Y(b[1])} {X(c[0])},{Y(c[1])}"
        out += _stroke(d, ink, 30 * s) + _stroke(d, bark, 22 * s)
    trunk = [(-52, 4), (-30, -40), (-40, -92), (-24, -140), (20, -140), (32, -96), (22, -46), (46, 4)]
    out += (f'<path d="{S.smooth_path([(x + px * s, y + py * s) for px, py in trunk])}" fill="{bark}" stroke="{ink}" '
            f'stroke-width="{_f(4 * s)}"/>')
    out += _stroke(f"M{X(-20)},{Y(-12)} Q{X(-30)},{Y(-60)} {X(-16)},{Y(-110)} M{X(14)},{Y(-20)} Q{X(22)},{Y(-70)} "
                   f"{X(8)},{Y(-120)}", bark_d, 4 * s, 0.7)
    out += (f'<ellipse cx="{X(-2)}" cy="{Y(-72)}" rx="{_f(11 * s)}" ry="{_f(18 * s)}" fill="#5e4a3a" stroke="{ink}" '
            f'stroke-width="{_f(3 * s)}"/>')
    out += (f'<path d="M{X(-60)},{Y(6)} q20,-14 40,-6 M{X(28)},{Y(4)} q18,-12 38,-2" fill="none" stroke="{ink}" '
            f'stroke-width="{_f(3.5 * s)}" stroke-linecap="round"/>')
    leaf = S.mix(P["olive"], "#b6c39a", 0.4)
    leaf_d = S.mix(P["olive"], P["leaf_dark"], 0.3)
    leaf_hi = "#dfe7cc"
    clumps = [(-128, -246, 96, 64), (8, -302, 112, 72), (132, -240, 96, 62), (-44, -214, 70, 44),
              (74, -210, 72, 44)]
    for i, (cx, cy, rx, ry) in enumerate(clumps):
        d = S.blob(x + cx * s, y + cy * s, rx * s, ry * s, 0.12, 11, seed * 10 + i)
        out += f'<path d="{d}" fill="{leaf}" stroke="{ink}" stroke-width="{_f(4 * s)}"/>'
        dd = S.blob(x + cx * s, y + (cy + ry * 0.35) * s, rx * 0.85 * s, ry * 0.5 * s, 0.12, 9, seed * 10 + i + 5)
        out += f'<path d="{dd}" fill="{leaf_d}" opacity="0.45"/>'
        dh = S.blob(x + (cx - rx * 0.2) * s, y + (cy - ry * 0.3) * s, rx * 0.5 * s, ry * 0.35 * s, 0.15, 8, i + 9)
        out += f'<path d="{dh}" fill="{S.mix(leaf, leaf_hi, 0.5)}" opacity="0.8"/>'
        for k in range(int(rx / 7)):
            lx = cx + r.uniform(-rx * 0.75, rx * 0.75)
            ly = cy + r.uniform(-ry * 0.6, ry * 0.6)
            rot = r.uniform(-50, 50)
            out += (f'<ellipse cx="{X(lx)}" cy="{Y(ly)}" rx="{_f(10 * s)}" ry="{_f(3 * s)}" fill="{leaf_hi}" '
                    f'opacity="0.85" transform="rotate({rot:.0f} {X(lx)} {Y(ly)})"/>')
    for (ox, oy) in [(-150, -232), (-96, -262), (30, -280), (-16, -318), (120, -258), (160, -226), (88, -204)]:
        out += (f'<ellipse cx="{X(ox)}" cy="{Y(oy)}" rx="{_f(6 * s)}" ry="{_f(8 * s)}" fill="#5c4a6e" '
                f'stroke="{ink}" stroke-width="{_f(1.6 * s)}"/>')
    return out


def _flowers(x, y, n, spread, seed, colors=("#f6d36b", "#f3a0a8", "#fffaf0", "#c9a7e0")):
    import random
    r = random.Random(seed)
    out = ""
    for i in range(n):
        fx_, fy = x + r.uniform(-spread, spread), y + r.uniform(-spread * 0.18, spread * 0.18)
        c = r.choice(colors)
        rr = r.uniform(4.5, 7.5)
        out += (f'<circle cx="{_f(fx_)}" cy="{_f(fy)}" r="{_f(rr)}" fill="{c}" stroke="{S.mix(P["ink"], c, 0.4)}" '
                f'stroke-width="1.6"/><circle cx="{_f(fx_)}" cy="{_f(fy)}" r="{_f(rr * 0.35)}" fill="#e7a73d"/>')
    return out


def _rock(x, y, w, h, seed=0, fill=None):
    fill = fill or P["stone"]
    d = S.blob(x, y - h * 0.45, w / 2, h / 2, wobble=0.12, n=9, seed=seed)
    hi = S.blob(x - w * 0.12, y - h * 0.62, w * 0.26, h * 0.18, wobble=0.15, n=7, seed=seed + 1)
    return S.path(d, fill=fill, sw=3.5) + f'<path d="{hi}" fill="{S.shade(fill, 0.4)}" opacity="0.75"/>'


def _path_edges(pts, widths):
    """Left / right edge points of a band of the given widths around a centreline."""
    left, right = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        (x0, y0), (x1, y1) = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        w = widths[i] / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left, right


def _dirt_path(uid, pts, widths, y_near, y_far, fill, ink_w=3.0, fade=(0.95, 0.85, 0.12), ruts=True,
               pebbles=(), seed=0):
    """A tapering dirt path: pale fill that fades toward the far end, ink only along the two side edges
    (no closing line across the ends), optional faint wheel ruts and a few pebbles."""
    import random
    r = random.Random(seed)
    left, right = _path_edges(pts, widths)
    a0, a1, a2 = fade
    defs = (f'<linearGradient id="{uid}f" gradientUnits="userSpaceOnUse" x1="0" y1="{y_near}" x2="0" y2="{y_far}">'
            f'<stop offset="0" stop-color="{fill}" stop-opacity="{a0}"/>'
            f'<stop offset="0.6" stop-color="{fill}" stop-opacity="{a1}"/>'
            f'<stop offset="1" stop-color="{fill}" stop-opacity="{a2}"/></linearGradient>'
            f'<linearGradient id="{uid}e" gradientUnits="userSpaceOnUse" x1="0" y1="{y_near}" x2="0" y2="{y_far}">'
            f'<stop offset="0" stop-color="{S.mix(P["ink"], fill, 0.4)}" stop-opacity="0.95"/>'
            f'<stop offset="0.7" stop-color="{S.mix(P["ink"], fill, 0.5)}" stop-opacity="0.7"/>'
            f'<stop offset="1" stop-color="{S.mix(P["ink"], fill, 0.6)}" stop-opacity="0"/></linearGradient>')
    body = f'<path d="{S.smooth_path(left + right[::-1], closed=True, tension=0.8)}" fill="url(#{uid}f)"/>'
    if ruts:
        rl, rr = _path_edges(pts, [w * 0.42 for w in widths])
        rc = S.mix(P["sand_dark"], fill, 0.35)
        for side in (rl, rr):
            body += _stroke(S.smooth_path(side, closed=False), rc, max(1.6, ink_w * 0.8), 0.45,
                            f'stroke-dasharray="{_f(38 * ink_w / 3)} {_f(16 * ink_w / 3)}"')
    for (px, py, pr) in pebbles:
        c = r.choice([P["stone"], P["stone_light"], S.mix(P["stone"], P["stone_dark"], 0.5)])
        body += (f'<ellipse cx="{_f(px)}" cy="{_f(py)}" rx="{_f(pr)}" ry="{_f(pr * 0.62)}" fill="{c}" '
                 f'stroke="{S.mix(P["ink"], c, 0.35)}" stroke-width="{_f(max(1.5, pr * 0.22))}"/>')
    for side in (left, right):
        body += _stroke(S.smooth_path(side, closed=False, tension=0.8), f"url(#{uid}e)", ink_w)
    return f"<defs>{defs}</defs>" + body


# ------------------------------------------------------------------ static backdrops
def _sky_svg():
    defs = (S.lin_grad("sky", [(0, "#97c9de"), (0.26, "#bfe0e4"), (0.42, "#eaeed6"), (0.52, "#fbe8c0"),
                               (1, "#f7dcae")]) +
            S.rad_grad("sunglow", [(0, "#fff6d8", 0.95), (0.4, "#ffe6ad", 0.5), (1, "#ffdca0", 0)]))
    body = S.rect_bg("url(#sky)", SW, SH)
    body += '<ellipse cx="2260" cy="660" rx="760" ry="430" fill="url(#sunglow)"/>'
    return _doc(body, defs)


def _field(pts, fill, stripe, seed=0):
    """A soft patch of crop field on a hillside with a few furrow strokes."""
    d = S.smooth_path(pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    out = f'<path d="{d}" fill="{fill}" stroke="{S.mix(P["ink"], fill, 0.55)}" stroke-width="2"/>'
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    w = (max(xs) - min(xs)) * 0.38
    for i in range(-1, 2):
        out += _stroke(f"M{_f(cx - w)},{_f(cy + i * 9)} Q{_f(cx)},{_f(cy + i * 9 - 6)} {_f(cx + w)},{_f(cy + i * 9 + 2)}",
                       stripe, 2.2, 0.6)
    return out


def _far_hills_svg():
    far1 = S.mix(P["olive"], "#d6e6e0", 0.62)
    far2 = S.mix(P["grass"], "#e3e6c6", 0.42)
    ink1 = S.mix(P["ink"], far1, 0.55)
    ink2 = S.mix(P["ink"], far2, 0.4)
    body = _ridge([(-60, 690), (180, 640), (420, 668), (690, 612), (960, 650), (1230, 598), (1500, 640),
                   (1790, 606), (2080, 648), (2300, 618), (2460, 640)], far1, 2.5, ink1)
    for x, y, s in [(240, 660, 0.35), (560, 655, 0.3), (1340, 635, 0.32), (1640, 640, 0.3), (2010, 650, 0.3)]:
        body += _tiny_olive(x, y + 8, s, seed=int(x))
    body += _ridge([(-60, 760), (240, 712), (520, 742), (820, 700), (1120, 735), (1420, 694), (1720, 728),
                    (2020, 690), (2300, 722), (2460, 708)], far2, 3, ink2)
    gold = S.mix("#e9d38e", far2, 0.35)
    body += _field([(560, 742), (690, 722), (800, 728), (760, 750), (610, 756)], gold, S.mix(gold, P["earth"], 0.3))
    body += _field([(1500, 724), (1640, 708), (1760, 716), (1700, 742), (1560, 744)], gold, S.mix(gold, P["earth"], 0.3))
    body += _field([(2120, 716), (2260, 708), (2380, 716), (2330, 736), (2170, 738)],
                   S.mix(P["grass_dark"], far2, 0.5), S.mix(P["grass_dark"], far2, 0.2))
    for x, y, s, v in [(1480, 726, 0.13, 0), (1560, 720, 0.11, 2), (1625, 730, 0.12, 0), (2220, 714, 0.11, 2)]:
        body += PR.house(x, y, s, variant=v)
    for x, y, s in [(320, 735, 0.42), (900, 722, 0.4), (1250, 728, 0.42), (1880, 712, 0.4), (2350, 720, 0.38)]:
        body += _tiny_olive(x, y + 6, s, seed=int(x) + 3)
    return _doc(S.g(body, filter="wobble"))


def _mid_hills_svg():
    gA = S.mix(P["grass"], P["sand"], 0.30)
    gB = S.mix(P["grass"], P["sand"], 0.16)
    defs = (S.lin_grad("midA", [(0, S.shade(gA, 0.2)), (1, gA)]) +
            S.lin_grad("midB", [(0, S.shade(gB, 0.18)), (1, S.mix(gB, P["grass_dark"], 0.12))]))
    body = _ridge([(-60, 850), (220, 800), (520, 822), (820, 860), (1100, 840)], "url(#midA)", 3.5)
    body += _field([(120, 838), (300, 818), (440, 830), (400, 862), (180, 866)], S.mix("#e4cf7e", gA, 0.3),
                   S.mix(P["earth"], gA, 0.4))
    body += _ridge([(700, 900), (1000, 838), (1320, 790), (1640, 812), (1960, 782), (2240, 806), (2460, 790)],
                   "url(#midB)", 3.5)
    body += _field([(1700, 838), (1880, 812), (2040, 820), (2010, 856), (1760, 864)], S.mix("#e4cf7e", gB, 0.25),
                   S.mix(P["earth"], gB, 0.4))
    # stone terraces on the hillsides
    tc = S.mix(P["grass_dark"], gB, 0.35)
    for i, y in enumerate([872, 912]):
        body += _stroke(f"M{1420 + i * 30},{y + 8} Q1700,{y - 26} 1980,{y - 6} T2440,{y - 18}", tc, 4, 0.5)
    body += _stroke("M-40,885 Q260,858 620,890", S.mix(P["grass_dark"], gA, 0.4), 4, 0.5)
    # the path from Jonah's yard reappears over the near ridge and winds up to the village, with a fork
    # running off east (toward Nineveh)
    road = S.mix(P["sand_light"], P["sand"], 0.35)
    body += _dirt_path("mp1", [(1352, 1060), (1340, 1010), (1318, 968), (1290, 934), (1276, 906), (1284, 884)],
                       [40, 34, 28, 22, 17, 12], 1040, 884, road, ink_w=2.2, fade=(0.95, 0.9, 0.35),
                       ruts=False, pebbles=[(1328, 990, 3.5), (1300, 950, 3)], seed=3)
    body += _dirt_path("mp2", [(1322, 975), (1390, 958), (1470, 930), (1560, 912), (1650, 902)],
                       [26, 22, 18, 14, 10], 975, 902, road, ink_w=2.0, fade=(0.9, 0.7, 0.0), ruts=False)
    # the village on the hillside
    body += _olive(1095, 880, 0.55, seed=4, haze=0.15)
    body += PR.house(1160, 862, 0.17, variant=2)
    body += PR.house(1262, 846, 0.19, variant=0)
    body += PR.house(1345, 852, 0.16, variant=1, facing=-1)
    body += PR.house(1225, 884, 0.15, variant=3)
    # olive groves
    for x, y, s, sd in [(1560, 852, 0.62, 1), (1700, 838, 0.55, 2), (1840, 826, 0.58, 3), (2000, 830, 0.6, 5),
                        (2150, 842, 0.55, 6), (2300, 828, 0.6, 7), (40, 868, 0.6, 8), (470, 858, 0.55, 9),
                        (1440, 872, 0.5, 10)]:
        body += _olive(x, y, s, seed=sd, haze=0.12)
    return _doc(S.g(body, filter="wobble"), defs)


def _drystone_wall(x0, x1, y, seed=0, k=1.0):
    import random
    r = random.Random(seed)
    out = ""
    x = x0
    sw = _f(2.6 * min(1.3, k))
    while x < x1:
        w = r.uniform(34, 52) * k
        h = r.uniform(22, 30) * k
        yy = y + 8 * math.sin(x / 260.0)
        fill = r.choice([P["stone"], P["stone_light"], S.mix(P["stone"], P["stone_dark"], 0.4)])
        out += (f'<rect x="{_f(x)}" y="{_f(yy - h)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(9 * k)}" fill="{fill}" '
                f'stroke="{P["ink"]}" stroke-width="{sw}"/>')
        if r.random() < 0.6:
            w2 = r.uniform(30, 44) * k
            out += (f'<rect x="{_f(x + w * 0.4)}" y="{_f(yy - h - 20 * k)}" width="{_f(w2)}" height="{_f(22 * k)}" '
                    f'rx="{_f(9 * k)}" fill="{S.shade(fill, 0.15)}" stroke="{P["ink"]}" stroke-width="{sw}"/>')
        x += w - 2
    return out


def _house_details():
    """Grapevine over the door, a flower window, a bench and a basket. Authored in the coordinates of a
    house at HOUSE_SRC; the caller maps them onto HOUSE with _house_tf()."""
    import random
    r = random.Random(5)
    leaf, leaf_d, leaf_l = P["leaf"], P["leaf_dark"], P["leaf_light"]
    out = ""
    vine = "M262,1092 C250,1010 274,940 258,860 C246,800 262,770 300,748 C360,716 450,712 520,742 C560,760 580,800 596,850"
    out += _stroke(vine, P["ink"], 11) + _stroke(vine, P["wood"], 6)
    out += _stroke("M258,900 C226,880 214,850 222,820 M300,748 C300,712 324,700 340,690", P["wood"], 4, 0.9)
    pts = [(250, 1010), (270, 960), (244, 905), (266, 860), (250, 812), (282, 768), (330, 735), (380, 722),
           (430, 722), (480, 730), (530, 748), (570, 786), (590, 834), (226, 836), (338, 694)]
    for i, (x, y) in enumerate(pts):
        rr = r.uniform(19, 26)
        c = r.choice([leaf, leaf, leaf_l, S.mix(leaf, leaf_d, 0.5)])
        rot = r.uniform(0, 360)
        out += (f'<path d="{S.blob(x, y, rr, rr * 0.85, 0.22, 7, 40 + i, rot)}" fill="{c}" stroke="{P["ink"]}" '
                f'stroke-width="2.6"/>')
        out += _stroke(f"M{x},{y} l{_f(rr * 0.5)},{_f(-rr * 0.3)} M{x},{y} l{_f(-rr * 0.4)},{_f(-rr * 0.4)}",
                       S.mix(c, P["leaf_dark"], 0.6), 1.8, 0.8)
    for gx, gy in [(352, 752), (468, 754), (566, 808)]:
        for j, (ox, oy) in enumerate([(0, 0), (-9, -9), (9, -9), (-14, -20), (0, -20), (14, -20), (-6, 10), (6, 10),
                                      (0, 20)]):
            out += (f'<circle cx="{gx + ox}" cy="{gy + 20 - oy}" r="7.5" fill="{S.mix("#7b4f9d", "#5a3a78", (j % 3) / 3)}" '
                    f'stroke="{P["ink"]}" stroke-width="2"/>')
        out += f'<circle cx="{gx - 3}" cy="{gy + 16}" r="2.5" fill="#d9c6ea" opacity="0.8"/>'
    # small window with a flower pot (right of the door)
    out += (f'<path d="M538,742 L538,672 Q566,640 594,672 L594,742 Z" fill="{S.mix(P["wood_dark"], P["ink"], 0.3)}" '
            f'stroke="{P["ink"]}" stroke-width="4"/>')
    out += f'<rect x="530" y="740" width="72" height="12" rx="4" fill="{P["wood"]}" stroke="{P["ink"]}" stroke-width="3"/>'
    out += (f'<path d="M546,740 L550,716 L584,716 L588,740 Z" fill="{P["terracotta"]}" stroke="{P["ink"]}" '
            f'stroke-width="3"/>')
    for fx_, fy in [(552, 700), (567, 690), (582, 702)]:
        out += f'<circle cx="{fx_}" cy="{fy}" r="9" fill="#e45e52" stroke="{P["ink"]}" stroke-width="2.2"/>'
        out += f'<circle cx="{fx_}" cy="{fy}" r="3" fill="#f6d36b"/>'
    out += f'<path d="M548,714 q-8,-10 2,-16 M586,714 q8,-10 -2,-16" fill="{leaf}" stroke="{P["ink"]}" stroke-width="2"/>'
    # bench with a basket by the wall
    wd = P["wood"]
    out += f'<rect x="96" y="1028" width="150" height="16" rx="5" fill="{wd}" stroke="{P["ink"]}" stroke-width="3.5"/>'
    for lx in (108, 220):
        out += f'<rect x="{lx}" y="1042" width="14" height="44" rx="3" fill="{P["wood_dark"]}" stroke="{P["ink"]}" stroke-width="3"/>'
    out += (f'<path d="M140,1028 Q138,996 172,994 Q206,996 204,1028 Z" fill="{P["sand_dark"]}" stroke="{P["ink"]}" '
            f'stroke-width="3"/>')
    out += _stroke("M146,1012 L198,1012 M150,1002 L194,1002", S.mix(P["sand_dark"], P["ink"], 0.4), 2, 0.8)
    out += _stroke("M150,996 Q172,960 196,996", P["wood_dark"], 4)
    for ax, ay, c in [(160, 990, "#e2a13a"), (176, 986, "#d9893c"), (188, 992, "#e9b84a")]:
        out += f'<circle cx="{ax}" cy="{ay}" r="9" fill="{c}" stroke="{P["ink"]}" stroke-width="2.2"/>'
    return S.g(S.g(out, transform=_house_tf()), filter="wobble-fine")


# the near path from Jonah's yard over the ridge (centreline and widths, stage px)
NEAR_PATH = [(850, 1272), (985, 1212), (1098, 1146), (1188, 1090), (1262, 1048), (1314, 1024)]
NEAR_PATH_W = [190, 168, 140, 100, 64, 40]


def _near_ground_svg():
    """The meadow plane: ridge, drystone wall, yard, path, rocks, the big framing olive tree, tufts."""
    g1 = S.mix(P["grass"], "#e3d98a", 0.28)
    defs = (S.lin_grad("near", [(0, S.shade(g1, 0.12)), (0.5, g1), (1, S.mix(g1, P["grass_dark"], 0.35))]) +
            S.rad_grad("yard", [(0, P["sand_light"], 1), (0.75, S.mix(P["sand_light"], P["sand"], 0.3), 0.9),
                                (1, P["sand"], 0)]))
    body = ""
    body += _ridge([(-60, 1000), (300, 985), (700, 1010), (1100, 1032), (1500, 1002), (1900, 975), (2200, 990),
                    (2460, 978)], "url(#near)", 4)
    body += _drystone_wall(1600, 2460, 1004, seed=3, k=1.45)
    # dirt yard in front of the house; the path leaves it and runs east over the ridge
    body += '<ellipse cx="640" cy="1150" rx="640" ry="92" fill="url(#yard)"/>'
    road = S.mix(P["sand_light"], P["sand"], 0.35)
    body += _dirt_path("np", NEAR_PATH, NEAR_PATH_W, 1272, 1024, road, ink_w=3.2, fade=(0.97, 0.92, 0.5),
                       pebbles=[(1050, 1196, 6), (1140, 1132, 5), (1176, 1112, 4), (1232, 1070, 4),
                                (1006, 1236, 7)], seed=8)
    body += _rock(1238, 1166, 86, 44, seed=3)
    body += _rock(1296, 1150, 50, 28, seed=5, fill=P["stone_light"])
    for x, y, v in [(1640, 1056, 2), (1890, 1034, 0), (2330, 1024, 2), (1150, 1214, 2), (1352, 1110, 0)]:
        body += PR.grass_tuft(x, y, 0.95, variant=v)
    body += _flowers(1700, 1100, 14, 220, 4)
    body += _flowers(1420, 1150, 8, 120, 6)
    body += _olive_big(*TREE, seed=2)
    body += _flowers(2230, 1205, 10, 180, 7)
    return _doc(S.g(body, filter="wobble"), defs)


def _house_svg():
    """Jonah's house with its vine, window, bench and jars. Its own static layer, drawn after the sky
    clouds and the heavenly glow, so the parting cloud bank passes behind the roof."""
    hx, hy, hs = HOUSE
    body = PR.house(hx, hy, hs, variant=3)
    body += _house_details()
    jx, jy = _hp(640, 1062)
    body += PR.jar(jx, jy, 0.6)
    jx, jy = _hp(700, 1076)
    body += PR.jar(jx, jy, 0.46, color=S.mix(P["terracotta"], P["sand"], 0.3))
    body += PR.bush(-10, 1124, 0.9, variant=1)
    body += S.g(PR.grass_tuft(800, 1170, 0.95, variant=0) + _flowers(330, 1200, 8, 170, 9), filter="wobble")
    body += CH.ground_shadow(JX, JY, JS, width=130, opacity=0.25)
    return _doc(body)


def _tuft_svg(x, y, v, s):
    return _doc(PR.grass_tuft(x, y, s, variant=v))


# ------------------------------------------------------------------ heavenly light (never a figure)
def _glow_svg():
    """Soft heavenly glow in the cloud gap plus a fan of rays pouring DOWN from it (not a full sunburst, so
    it never reads as a second sun). Kept gentle so the sky stays blue at the top left and the land keeps
    its contrast. The house is a later layer, so no mask is needed."""
    gx, gy = GAP
    defs = (S.rad_grad("hg", [(0, "#fffbec", 0.6), (0.22, "#fff0c0", 0.52), (0.55, "#ffd98a", 0.24),
                              (1, "#ffd27a", 0)]) +
            f'<radialGradient id="burst" gradientUnits="userSpaceOnUse" cx="{gx}" cy="{gy}" r="700">'
            f'<stop offset="0" stop-color="#fff6d0" stop-opacity="0.75"/>'
            f'<stop offset="0.45" stop-color="#ffe9a6" stop-opacity="0.32"/>'
            f'<stop offset="1" stop-color="#ffe3a0" stop-opacity="0"/></radialGradient>')
    angles = [36, 46, 56, 66, 76, 104, 114, 124, 134, 144]       # the centre is the cone over Jonah
    widths = [5, 4, 6, 4.5, 5.5, 5.5, 4.5, 6, 4, 5]
    body = f'<path d="{_fan(gx, gy, 700, angles, widths)}" fill="url(#burst)" filter="url(#soft)" opacity="0.85"/>'
    body += f'<ellipse cx="{gx}" cy="{gy}" rx="500" ry="300" fill="url(#hg)"/>'
    body += f'<ellipse cx="{gx}" cy="{gy + 10}" rx="210" ry="110" fill="#fffaf0" opacity="0.5" filter="url(#blur-md)"/>'
    return _doc(body, defs)


def _rays_svg():
    gx, gy = GAP
    defs = (f'<linearGradient id="rayg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{JY + 120}">'
            f'<stop offset="0" stop-color="#fff6d2" stop-opacity="0.8"/>'
            f'<stop offset="0.55" stop-color="#ffeaa8" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#ffe08e" stop-opacity="0.16"/></linearGradient>' +
            f'<linearGradient id="coneg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{JY + 120}">'
            f'<stop offset="0" stop-color="#fff2c4" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#ffe39a" stop-opacity="0.12"/></linearGradient>' +
            S.rad_grad("pool", [(0, "#fff1c0", 0.85), (0.6, "#ffe39a", 0.35), (1, "#ffd77e", 0)]) +
            S.rad_grad("halo", [(0, "#fff6d6", 0.7), (0.6, "#ffe7a4", 0.3), (1, "#ffe0a0", 0)]))
    length = JY + 180 - gy
    cx = gx - 30
    body = f'<path d="{_fan(cx, gy + 10, length, [90.5], [17])}" fill="url(#coneg)" filter="url(#blur-lg)"/>'
    body += (f'<path d="{_fan(cx, gy + 10, length, [80.5, 85.5, 90.2, 95, 100], [3.4, 2.2, 3.8, 2.4, 3.2])}" '
             f'fill="url(#rayg)" filter="url(#soft)"/>')
    body += f'<ellipse cx="{JX}" cy="{_f(JY - 187 * JS)}" rx="{_f(153 * JS)}" ry="{_f(220 * JS)}" fill="url(#halo)"/>'
    body += f'<ellipse cx="{JX}" cy="{JY - 4}" rx="{_f(213 * JS)}" ry="{_f(50 * JS)}" fill="url(#pool)"/>'
    return _doc(body, defs)


def _warm_svg():
    """Additive warm light (premultiplied 'add' blend, so the colours are small)."""
    defs = S.rad_grad("warm", [(0, "#3a2a0c", 1), (0.5, "#1e1505", 0.85), (1, "#100800", 0)])
    return _doc(f'<ellipse cx="{GAP[0] - 20}" cy="700" rx="720" ry="660" fill="url(#warm)"/>', defs)


# ------------------------------------------------------------------ the vision bubble
def _bubble_svg():
    import random
    r = random.Random(11)
    defs = (f'<clipPath id="win"><ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}"/></clipPath>' +
            f'<linearGradient id="vsky" gradientUnits="userSpaceOnUse" x1="0" y1="{BY - RY}" x2="0" y2="{BY + 60}">'
            f'<stop offset="0" stop-color="#eeb57c"/><stop offset="0.55" stop-color="#f4cd98"/>'
            f'<stop offset="1" stop-color="#f9e2b8"/></linearGradient>' +
            S.rad_grad("vhalo", [(0, "#fff3c8", 0.9), (0.6, "#ffe3a0", 0.5), (1, "#ffd98a", 0)]) +
            S.lin_grad("vsand", [(0, "#efcf98"), (1, "#e2b678")]))
    body = f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 190}" ry="{RY + 165}" fill="url(#vhalo)"/>'
    puffs = []
    n = 18
    for i in range(n):
        a = 2 * math.pi * i / n + 0.12
        rr = r.uniform(58, 80) * (0.85 if math.sin(a) < -0.3 else 1.0)
        puffs.append((BX + (RX + 34) * math.cos(a), BY + (RY + 30) * math.sin(a), rr))
    cream, under = "#fff8ea", "#f4e2c3"
    ring = ""
    for x, y, rr in puffs:
        ring += f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(rr)}" fill="{cream}" stroke="{P["ink"]}" stroke-width="8"/>'
    for x, y, rr in puffs:
        fill = under if y > BY + RY * 0.55 else cream
        ring += f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(rr - 1)}" fill="{fill}"/>'
    ring += f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 34}" ry="{RY + 30}" fill="{cream}"/>'
    body += S.g(ring, filter="wobble")
    inner = S.rect_bg("url(#vsky)", SW, SH)
    inner += f'<ellipse cx="{BX + 150}" cy="{BY - 70}" rx="170" ry="90" fill="#fff0cc" opacity="0.45" filter="url(#blur-md)"/>'
    inner += _ridge([(BX - RX - 40, BY + 50), (BX - 120, BY + 34), (BX + 80, BY + 46), (BX + RX + 40, BY + 30)],
                    S.mix(P["sand"], "#f2d4a4", 0.5), 2, S.mix(P["ink"], P["sand"], 0.5))
    # the great city fills the middle of the window: walls, towers, ziggurat (scale 0.5, almost no haze)
    gy = BY + 98
    inner += PR.nineveh_skyline(BX - RX + 6, BX + RX - 6, gy, 0.5, seed=SKY_SEED, haze=0.03)
    inner += _ridge([(BX - RX - 40, gy + 4), (BX, gy + 1), (BX + RX + 40, gy + 6)], "url(#vsand)", 2.5)
    inner += (f'<path d="M{BX - RX - 40},{gy + 28} C{BX - 150},{gy + 18} {BX + 60},{gy + 36} {BX + RX + 40},{gy + 22} '
              f'L{BX + RX + 40},{gy + 52} C{BX + 80},{gy + 64} {BX - 160},{gy + 44} {BX - RX - 40},{gy + 58} Z" '
              f'fill="{P["sea_light"]}" stroke="{P["ink"]}" stroke-width="2.5"/>')
    inner += _stroke(f"M{BX - 200},{gy + 40} q30,-6 60,0 M{BX + 40},{gy + 46} q30,-6 60,0 "
                     f"M{BX + 170},{gy + 36} q24,-5 48,0", P["foam"], 3, 0.8)
    for x in (BX - 236, BX + 226):
        inner += PR.palm_tree(x, gy + 14, 0.13, dates=False)
    body += f'<g clip-path="url(#win)">{S.g(inner, filter="wobble-fine")}</g>'
    body += (f'<ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}" fill="none" stroke="#f3c860" stroke-width="10" '
             f'opacity="0.55" filter="url(#soft)"/>')
    body += S.g(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}" fill="none" stroke="{P["ink"]}" '
                f'stroke-width="4"/>', filter="wobble")
    return _doc(body, defs)


def _gloom_svg():
    """Grey wash over the vision (the city's wrongdoing), darker near the cloud."""
    defs = (f'<clipPath id="win2"><ellipse cx="{BX}" cy="{BY}" rx="{RX - 2}" ry="{RY - 2}"/></clipPath>' +
            S.rad_grad("gl", [(0, "#6d6c7c", 0.42), (0.6, "#7c7b8a", 0.2), (1, "#8a8996", 0.08)], cy=0.22, r=0.85))
    body = (f'<g clip-path="url(#win2)"><rect x="{BX - RX}" y="{BY - RY}" width="{2 * RX}" height="{2 * RY}" '
            f'fill="url(#gl)"/></g>')
    return _doc(body, defs)


GREY = (BX + 20, BY - 120)     # centre of the grey cloud of wrongdoing, just over the skyline


def _grey_cloud_svg():
    """A small grey cloud over the city with a few grey wisps rising into it from the streets (no
    violence). Clipped to the vision window so it never spills over the window's rim."""
    cx, cy = GREY
    defs = f'<clipPath id="win3"><ellipse cx="{BX}" cy="{BY}" rx="{RX - 3}" ry="{RY - 3}"/></clipPath>'
    body = ""
    for x0 in (BX - 130, BX - 20, BX + 110):
        body += _stroke(f"M{x0},{BY + 70} c-14,-18 14,-30 0,-48 s14,-26 2,-44 s-12,-22 0,-38", "#8a8898", 5, 0.5)
    body += S.cloud(cx, cy, 210, 70, "#a9a7b3", seed=21, sw=3, shade_fill="#86849a")
    body += S.cloud(cx - 112, cy + 22, 84, 34, "#b3b1bc", seed=23, sw=2.5, shade_fill="#8f8da0")
    body += S.cloud(cx + 116, cy + 16, 80, 32, "#b3b1bc", seed=24, sw=2.5, shade_fill="#8f8da0")
    sc_ = "#6f6d7d"
    body += _stroke(f"M{cx - 36},{cy + 4} c8,-14 20,10 28,-4 s18,12 26,-2", sc_, 3.5, 0.9)
    body += _stroke(f"M{cx + 30},{cy + 16} c6,-10 14,8 20,-3 s14,9 20,-2", sc_, 3, 0.8)
    return _doc(f'<g clip-path="url(#win3)">{S.g(body, filter="wobble-fine")}</g>', defs)


def _smoke_svg():
    """A thin wisp of cooking-fire smoke rising from the village."""
    x, y = 1252, 812
    d = f"M{x},{y} C{x - 18},{y - 40} {x + 22},{y - 70} {x + 2},{y - 110} S{x - 26},{y - 160} {x - 6},{y - 200}"
    defs = '<filter id="smk" x="-50%" y="-20%" width="200%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>'
    body = _stroke(d, "#f4ede0", 24, 0.45, 'filter="url(#soft)"')
    body += _stroke(d, "#fbf6ec", 10, 0.5, 'filter="url(#smk)"')
    return _doc(body, defs)


# ------------------------------------------------------------------ creatures
DOVE_WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)
WING_CYCLE = (0, 1, 2, 3, 4, 3, 2, 1)


def _dove_frames(x, y, s, facing=1):
    return [_doc(PR.dove(x, y, s, facing, wing=w)) for w in DOVE_WINGS]


def _flap(rate=9.0, phase=0.0, glide=None):
    def f(t):
        if glide and glide[0] <= t <= glide[1]:
            return 2.0
        return float(WING_CYCLE[int((t * rate + phase) % len(WING_CYCLE))])
    return f


SHEEP_NECK = (50, -92)        # local pivot (scale 1, facing right) for turning a sheep's head


def _sheep_parts(x, y, s, f):
    """(body markup, head markup) of props.animal(kind='sheep'): the head (ears, face, top-knot, eye, mouth)
    is the last group of shapes props draws, so it can be split off and turned on its own layer while the
    hooves stay planted. Falls back to (whole sheep, '') if the markup is not in the expected form."""
    full = PR.animal(x, y, s, f, kind="sheep")
    i = full.find("rotate(-24 54 -110)")
    j = full.rfind("<ellipse", 0, i) if i >= 0 else -1
    k = full.find("<g transform=")
    k = full.find(">", k) + 1 if k >= 0 else 0
    if j <= k or not full.endswith("</g></g>"):
        return full, ""
    return full[:j] + "</g></g>", full[:k] + full[j:]


# ------------------------------------------------------------------ Jonah
def _jonah_svg(pose, expr):
    body = CH.jonah(JX, JY, JS, 1, pose=pose, expr=expr)
    hx, hy = CH.hand_positions(CH.jonah, JX, JY, JS, 1, pose=pose)[0]
    body += PR.scroll(hx, hy + 6 * JS, 0.5 * JS, rot=-74)
    body += (f'<ellipse cx="{_f(hx)}" cy="{_f(hy)}" rx="{_f(11 * JS)}" ry="{_f(13 * JS)}" fill="{P["skin"]}" '
             f'stroke="{P["ink"]}" stroke-width="{_f(4 * JS)}" filter="url(#wobble-fine)"/>')
    return _doc(body)


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[0], ctx.lines[1], ctx.lines[2], ctx.lines[3]

    # --- beats (all from the narration timings)
    t_bleat = L0.start + 0.85                 # a sheep lifts its head and bleats early on
    t_blink = L0.start + 1.15                 # Jonah blinks
    t_name = L0.start + 2.65                  # "...名叫约拿" — Jonah smiles and gives a little hop on "约拿"
    t_light = L1.start - 0.05                 # clouds start to part as "God said to him" begins
    t_look = L1.start + 0.38                  # Jonah looks up, surprised
    t_vis = L2.start + 1.3                    # the vision opens (pause after "约拿，起来，")
    t_grey = L3.start + 0.15                  # the grey cloud gathers over Nineveh
    t_worry = L3.start + 1.2                  # Jonah becomes worried (just before "坏事")
    t_beat = L3.start + 2.65                  # "你要去警告他们" — hand to his chest: "me?"
    pulse = lambda t, lo: lo + (1 - lo) * (0.5 + 0.5 * math.sin(2 * math.pi * (t - t_light) / 2.4 - 1.2))

    # --- sky + land (static: flattened into one backdrop)
    sc.add("sky", _sky_svg(), wc=0.45)
    sc.add("far_hills", _far_hills_svg(), wc=0.8)
    sc.add("mid_hills", _mid_hills_svg())
    sc.add("near_ground", _near_ground_svg())

    # --- sky things (moving; the house layer comes after them so clouds pass behind its roof)
    for i, (cx, cy, cw, ch, sd, v) in enumerate([(150, 132, 280, 86, 5, 7), (2150, 160, 260, 84, 6, 6),
                                                  (1700, 540, 200, 62, 8, 9)]):
        sc.add(f"cloud_small{i}", _doc(S.g(S.cloud(cx, cy, cw, ch, "#fdf6e8", seed=sd, sw=3, shade_fill="#efdcc4"),
                                           filter="wobble")), motion=M.drift(vx=v))

    glow_alpha = lambda t: M.progress(t, t_light, t_light + 0.7, "sine") * pulse(t, 0.82)
    sc.add("glow", _glow_svg(), wc=0, motion=lambda t: Tf(alpha=glow_alpha(t)))

    # the cloud bank above Jonah parts to let the light through
    for name, circles, d0, d1 in [("cloudL", LEFT_CL, 70, -200), ("cloudR", RIGHT_CL, -70, 150)]:
        frames = [_doc(_cloud_bank(circles, g, name)) for g in (0.0, 1.0)]
        mv = M.combine(M.keys([(0, {"dx": d0}), (t_light, {"dx": d0}), (t_light + 1.3, {"dx": d1})], "inout"),
                       M.drift(vx=2.5), M.bob(4, 6.0, 0.3 if d1 > 0 else 0.0))
        sc.add(name, frames, motion=mv, wc=0.7,
               frame_at=lambda t: M.progress(t, t_light + 0.15, t_light + 1.1, "sine"))

    # --- Jonah's house (static, in front of the sky)
    sc.add("house", _house_svg())

    # --- the vision in the eastern sky
    vis = M.combine(
        M.keys([(t_vis, {"s": 0.18, "dx": -330, "dy": 60}), (t_vis + 0.95, {"s": 1.0, "dx": 0, "dy": 0})], "back",
               pivot=(BX, BY)),
        M.keys([(t_vis, {"alpha": 0}), (t_vis + 0.45, {"alpha": 1})], "sine"),
        lambda t: Tf(dy=5 * math.sin(2 * math.pi * (t - t_vis - 0.95) / 4.6)) if t > t_vis + 0.95 else Tf())
    sc.add("vision", _bubble_svg(), motion=vis, wc=0.7)
    sc.add("gloom", _gloom_svg(), wc=0, motion=M.combine(
        vis, M.keys([(t_grey, {"alpha": 0}), (t_grey + 1.6, {"alpha": 1})], "sine")))
    sc.add("grey_cloud", _grey_cloud_svg(), motion=M.combine(
        vis, M.keys([(t_grey, {"alpha": 0, "dy": 26}), (t_grey + 1.4, {"alpha": 1, "dy": 0})], "out"),
        lambda t: Tf(dx=6 * math.sin(2 * math.pi * t / 5.0))), wc=0.6)

    sc.add("smoke", _smoke_svg(), wc=0, motion=M.combine(
        M.sway(3.0, 4.2, pivot=(1252, 812)), M.pulse(0.6, 1.0, 3.1), M.keys([(0, {"sy": 0.96}), (T, {"sy": 1.06})],
                                                                          "linear", pivot=(1252, 812))))

    # --- sheep: hooves stay planted; only the head turns (sheep 0 lifts it to bleat, sheep 1 nods while
    # grazing, sheep 2 looks around); bodies breathe
    def head_angle(i):
        if i == 0:      # lift (nose up) L0.start+0.65 .. L0.start+2.15 around the bleat
            return lambda t: 11 * (M.progress(t, t_bleat - 0.2, t_bleat + 0.05, "out") -
                                   M.progress(t, t_bleat + 0.95, t_bleat + 1.3, "inout"))
        if i == 1:      # slow grazing nod (nose down)
            return lambda t: -7 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 2.9 - 1.3))
        return lambda t: 4 * math.sin(2 * math.pi * t / 4.4 + 0.6)

    for i, (x, y, s, f) in enumerate(SHEEP):
        body, head = _sheep_parts(x, y, s, f)
        br = M.breathe(0.012, 2.6 + 0.3 * i, pivot=(x, y), phase=0.3 * i)
        sc.add(f"sheep{i}", _doc(CH.ground_shadow(x, y, s, width=180, opacity=0.2) + body), motion=br)
        if head:
            nx, ny = PR.local_to_stage(x, y, s, f, *SHEEP_NECK)
            ang = head_angle(i)
            sc.add(f"sheep{i}_head", _doc(head), motion=lambda t, ang=ang, br=br, f=f, ny=ny, nx=nx, y=y: Tf(
                dy=-(br(t).sy - 1) * (y - ny), rot=-ang(t) * f, px=nx, py=ny))

    # --- golden rays behind Jonah
    rays_alpha = lambda t: M.progress(t, t_light + 0.05, t_light + 0.65, "sine") * pulse(t, 0.75)
    sc.add("rays", _rays_svg(), wc=0, motion=lambda t: Tf(alpha=rays_alpha(t)),
           reveal=lambda t: {"mode": "down", "frac": M.progress(t, t_light + 0.05, t_light + 0.85, "out"), "soft": 160})

    # --- Jonah. Every change of pose or face is a HARD switch (no crossfade double exposures); a small
    # squash, hop or dip on the layer sells each one.
    # frames: 0 blink, 1 neutral, 2 happy, 3 listen + surprised, 4 listen + worried, 5 hand on chest, worried
    frames = [_jonah_svg("stand", "peaceful"), _jonah_svg("stand", "neutral"), _jonah_svg("stand", "happy"),
              _jonah_svg("listen", "surprised"), _jonah_svg("listen", "worried"), _jonah_svg("confess", "worried")]

    def jonah_frame(t):
        if t < t_look:
            if t_blink <= t <= t_blink + 0.13:
                return 0.0
            return 2.0 if t >= t_name else 1.0
        if t < t_worry:
            return 3.0
        return 4.0 if t < t_beat else 5.0

    jm = M.combine(
        M.keys([(t_name, {"dy": 0}), (t_name + 0.14, {"dy": -8}), (t_name + 0.32, {"dy": 0}),
                (t_worry, {"dy": 0}), (t_worry + 0.1, {"dy": 4}), (t_worry + 0.3, {"dy": 0}),
                (t_beat, {"dy": 0}), (t_beat + 0.1, {"dy": 3}), (t_beat + 0.4, {"dy": 0})], "sine"),
        M.keys([(t_look - 0.02, {"sy": 1.0, "sx": 1.0}), (t_look + 0.1, {"sy": 1.035, "sx": 0.985}),
                (t_look + 0.32, {"sy": 1.0, "sx": 1.0}),
                (t_beat - 0.01, {"sy": 1.0, "sx": 1.0}), (t_beat + 0.09, {"sy": 0.975, "sx": 1.012}),
                (t_beat + 0.42, {"sy": 1.0, "sx": 1.0})], "out", pivot=(JX, JY)),
        M.breathe(0.008, 3.2, pivot=(JX, JY)),
        M.keys([(t_worry, {"dx": 0}), (t_worry + 0.6, {"dx": -8})], "inout"))
    sc.add("jonah", frames, motion=jm, frame_at=jonah_frame)

    # --- foreground grass: each tuft rocks around its own base (sharp blades, no crossfaded ghosts)
    for i, (x, y, v, s) in enumerate(FG_TUFTS):
        sc.add(f"tuft{i}", _tuft_svg(x, y, v, s), motion=M.sway(2.4 + 0.3 * (i % 3), 3.4 + 0.25 * (i % 4),
                                                                   pivot=(x, y), phase=0.17 * i))

    # --- birds: a pair of doves crossing the open sky right of the house, rising through the parting clouds
    # and away; later one far away over the meadow
    glide0 = L0.start + 1.8
    for i, (x0, y0, s, ph, keys_) in enumerate([
            (1000, 400, 0.62, 0.0, [(0.0, {"dx": -150, "dy": 20}), (L1.start, {"dx": 520, "dy": -50}),
                                    (L2.start + 0.9, {"dx": 1300, "dy": -720})]),
            (1000, 470, 0.52, 3.0, [(0.3, {"dx": -110, "dy": 10}), (L1.start + 0.2, {"dx": 380, "dy": -40}),
                                    (L2.start + 1.1, {"dx": 1100, "dy": -740})]),
            (2200, 770, 0.34, 1.5, [(L2.start + 3.07, {"dx": 300, "dy": 0}), (T, {"dx": -560, "dy": -30})])]):
        facing = 1 if i < 2 else -1
        sc.add(f"dove{i}", _dove_frames(x0, y0, s, facing),
               motion=M.combine(M.keys(keys_, ["linear", "in"]), M.bob(14, 1.3, ph / 8)),
               frame_at=_flap(9.0 if i < 2 else 7.0, ph,
                              glide=(glide0 + i * 0.4, glide0 + 1.0 + i * 0.4) if i < 2 else None),
               wc=0.6)

    # a dove perched on the roof: looks around, turning with a little hop each time
    rx_, ry_ = _hp(585, 497)
    pd = [_doc(PR.dove(rx_, ry_, 0.6, f, pose="stand")) for f in (1, -1)]
    hops = [L0.start + 2.3, L2.start + 0.57, L3.start + 0.9, L3.start + 3.5]
    hop_keys = [(0, {"dy": 0})]
    for h in hops:
        hop_keys += [(h, {"dy": 0}), (h + 0.14, {"dy": -16}), (h + 0.3, {"dy": 0})]
    sc.add("dove_roof", pd, wc=0.6, frame_at=lambda t: float(sum(t >= h + 0.12 for h in hops) % 2),
           motion=M.keys(hop_keys, "sine"))

    # warm golden light over everything once the light comes (additive; 'screen' darkens highlights)
    warm_alpha = lambda t: 0.5 * M.progress(t, t_light + 0.15, t_light + 1.1, "sine") * pulse(t, 0.7)
    sc.add("warm", _warm_svg(), wc=0, blend="add", motion=lambda t: Tf(alpha=warm_alpha(t)))

    # --- camera: wide establishing shot -> drift in on Jonah -> tilt up WITH "上帝对他说" so the parting
    # clouds are in frame -> widen and pan right for the vision, framing the house door as a repoussoir
    sc.camera = M.cam_keys([
        (0.0, Cam(1200, 690, 2340)),
        (L1.start - 0.3, Cam(1012, 742, 1790)),
        (L1.start + 0.75, Cam(1050, 652, 2000)),
        (t_vis - 0.3, Cam(1072, 650, 2040)),
        (t_vis + 1.2, Cam(1165, 650, 1930)),
        (L3.start, Cam(1168, 651, 1930)),
        (T, Cam(1160, 646, 1900)),
    ], ["sine", "sine", "inout", "sine", "inout", "sine"])

    # --- effects
    sc.fx = [
        FX.motes((0, 300, SW, 1200), count=26, color=(255, 246, 214), size=(3, 6), alpha=110),
        FX.sparkles((GAP[0] - 300, GAP[1] + 150, GAP[0] + 330, JY - 60), count=26, t0=t_look - 0.1,
                    color=(255, 238, 170), size=(8, 18), period=1.7, drift=-6, seed=21),
        FX.sparkles((BX - RX - 80, BY - RY - 60, BX + RX + 80, BY + RY + 60), count=16, t0=t_vis + 0.3,
                    t1=t_vis + 2.6, color=(255, 240, 180), size=(9, 20), period=1.2, drift=0, seed=31),
    ]

    # --- sound
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-14, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("sheep", t_bleat, gain_db=-16, pan=0.35)
    sc.sfx("chime", L1.start, gain_db=-6)
    sc.sfx("sparkle", t_vis + 0.1, gain_db=-10, pan=0.5)
    return sc
