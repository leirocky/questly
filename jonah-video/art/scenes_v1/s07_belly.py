"""Scene 7 — inside the great fish (Jonah 1:17-2:9).

Three days and three nights in the belly of the fish: a cosy, dim, living cave of soft, slightly crooked rib
arches that bends away out of sight, wet fleshy walls with folds, a lumpy floor, a pool with little fishes,
swallowed seaweed and a jar from the ship. Line 0 counts the days: a round glow opens at the top and three
suns and three moons pop up in pairs on '过了三天三夜' while Jonah sits sad; the row fades early in line 1
('in the darkness') as he swaps to kneeling and prays; lines 2-3 God hears him: a warm golden glow grows behind
him, sparkles rise, the walls warm up from him outward, and at line 3 the glow is fullest and Jonah lifts his
face, hopeful.

Note: engine blend="screen" saturates (cv2.add clips before the subtract), so glows here use "add"/"normal".
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

# ----------------------------------------------------------------- geometry of the belly
# The belly is a soft tube of rib arches. Every rib is its own slightly squashed, tilted, wobbly ring (seeded
# jitter), the ribs are spaced unevenly, and the tube bends to the right and a little up with depth, so its
# far end curves away behind the right-hand wall instead of ending in a straight vanishing point.
VP = (1240.0, 450.0)        # where a straight tube would vanish (the bend pulls the far end off to the right)
CN = (1070.0, 590.0)        # centre of the k = 1 rib ring
RX, RY = 1010.0, 560.0      # radii of the k = 1 ring
FLOOR_K = 0.705             # floor level below a ring's centre, as a fraction of its half-height
SUPER = 2.2                 # superellipse exponent (soft, slightly arch-like rings)
BEND = (700.0, -130.0)      # sideways / upward drift of the far end, weighted by (1 - k)^3
DEPTHS = (0.15, 0.19, 0.245, 0.335, 0.45, 0.63, 1.0)     # far -> near (perspective scale), unevenly spaced
NEAR_FRAME = 1.34                                         # an extra, very near rib that frames the corners
KS = DEPTHS + (NEAR_FRAME,)
NEAR_I = len(DEPTHS) - 1                                  # index of the k = 1 rib

JX, JY, JS = 880.0, 920.0, 1.62     # Jonah's anchor and scale
GX, GY = 858.0, 690.0              # centre of God's warm glow (Jonah's chest)
TOP = (1090.0, 195.0)              # the round "days" glow at the top
PX, PY, PRX, PRY = 320.0, 1010.0, 320.0, 72.0      # the pool (water ellipse)


def _base(k):
    """Unjittered ring at depth k: centre and radii."""
    b = max(0.0, 1 - k) ** 3
    return (VP[0] + (CN[0] - VP[0]) * k + BEND[0] * b, VP[1] + (CN[1] - VP[1]) * k + BEND[1] * b, RX * k, RY * k)


def _make_ribs():
    ribs = []
    for i, k in enumerate(KS):
        r = random.Random(300 + 17 * i)
        cx, cy, rx, ry = _base(k)
        j = 20 * min(k, 1.0)
        s = 1 + r.uniform(-0.06, 0.06)
        ribs.append(dict(
            k=k, cx=cx + r.uniform(-j, j), cy=cy + r.uniform(-j, j) * 0.6,
            rx=rx * s * (1 + r.uniform(-0.025, 0.025)), ry=ry * s,
            tilt=math.radians(r.uniform(-3, 3)), e=SUPER + r.uniform(-0.12, 0.12),
            harm=[(r.uniform(0.006, 0.016), n, r.uniform(0, 2 * math.pi)) for n in (2, 3, 5)],
            thick=r.uniform(0.86, 1.14)))
    return ribs


RIBS = _make_ribs()


def _sp(c, e):
    return math.copysign(abs(c) ** (2 / e), c)


def _rib_pt(i, a):
    """Point on rib i's centre line at angle a (radians; 0 = right, pi/2 = down, 3pi/2 = top)."""
    rb = RIBS[i]
    h = 1 + sum(am * math.sin(n * a + ph) for am, n, ph in rb["harm"])
    lx, ly = rb["rx"] * h * _sp(math.cos(a), rb["e"]), rb["ry"] * h * _sp(math.sin(a), rb["e"])
    c, s = math.cos(rb["tilt"]), math.sin(rb["tilt"])
    return rb["cx"] + lx * c - ly * s, rb["cy"] + lx * s + ly * c


def _normal(i, a):
    p0, p1 = _rib_pt(i, a - 0.002), _rib_pt(i, a + 0.002)
    tx, ty = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(tx, ty) or 1.0
    nx, ny = ty / ln, -tx / ln
    p = _rib_pt(i, a)
    if (p[0] - RIBS[i]["cx"]) * nx + (p[1] - RIBS[i]["cy"]) * ny < 0:
        nx, ny = -nx, -ny
    return nx, ny


def _rib_pts(i, n=96, off=None):
    """Closed contour of rib i, optionally pushed outward by off(a) px along the normal."""
    pts = []
    for j in range(n):
        a = 2 * math.pi * j / n
        x, y = _rib_pt(i, a)
        if off is not None:
            nx, ny = _normal(i, a)
            o = off(a)
            x, y = x + nx * o, y + ny * o
        pts.append((x, y))
    return pts


def _wall_pt(i, u, a):
    """Point on the wall between rib i (u = 0) and the nearer rib i + 1 (u = 1) at angle a (radians)."""
    p, q = _rib_pt(i, a), _rib_pt(i + 1, a)
    return p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u


def _wall_pts(i, u, n=72, a0=0.0, a1=2 * math.pi, wob=0.0, seed=0, closed=True):
    r = random.Random(seed)
    m = n if closed else n + 1
    return [_wall_pt(i, u + r.uniform(-wob, wob), a0 + (a1 - a0) * j / n) for j in range(m)]


def _floor_y(i):
    cx, cy, rx, ry = _base(KS[i])
    return cy + FLOOR_K * ry


def _floor_x(i, side):
    """Where the floor meets rib i (side -1 left, +1 right)."""
    yf = _floor_y(i)
    a0, a1 = (math.pi / 2, math.pi) if side < 0 else (0.0, math.pi / 2)
    prev = None
    for j in range(401):
        a = a0 + (a1 - a0) * j / 400
        x, y = _rib_pt(i, a)
        if prev is not None and (prev[1] - yf) * (y - yf) <= 0:
            u = (yf - prev[1]) / ((y - prev[1]) or 1e-9)
            return prev[0] + (x - prev[0]) * u
        prev = (x, y)
    return _rib_pt(i, a1 if side < 0 else a0)[0]


def _rib_top_y(i, x):
    """Height of rib i's centre line above stage x (upper half of the ring)."""
    prev = None
    for j in range(721):
        a = math.pi + math.pi * j / 720
        px_, py_ = _rib_pt(i, a)
        if prev is not None and (prev[0] - x) * (px_ - x) <= 0:
            u = (x - prev[0]) / ((px_ - prev[0]) or 1e-9)
            return prev[1] + (py_ - prev[1]) * u
        prev = (px_, py_)
    return RIBS[i]["cy"] - RIBS[i]["ry"]


def _catmull(pts, steps=10):
    """Sample a Catmull-Rom curve through pts (open), returning dense points."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0, p1, p2 = pts[max(0, i - 1)], pts[i], pts[i + 1]
        p3 = pts[min(n - 1, i + 2)]
        for s in range(steps):
            t = s / steps
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1])
    return out


def _junctions():
    """Lumpy floor/wall junction curves on both sides: per side, a list (one per gap i -> i+1) of points."""
    res = {}
    for side in (-1, 1):
        r = random.Random(77 + side)
        ctrl = []
        for i in range(len(KS)):
            ctrl.append((_floor_x(i, side), _floor_y(i)))
        pts = [ctrl[0]]
        for i in range(len(KS) - 1):
            (x0, y0), (x1, y1) = ctrl[i], ctrl[i + 1]
            k = KS[i]
            for u in (0.35, 0.7):
                pts.append((x0 + (x1 - x0) * u + side * r.uniform(-26, 44) * k, y0 + (y1 - y0) * u + r.uniform(-8, 8) * k))
            pts.append((x1, y1))
        dense = _catmull(pts, 8)
        # split per gap (each gap spans 3 control segments = 24 samples)
        res[side] = [dense[i * 24:(i + 1) * 24 + 1] for i in range(len(KS) - 1)]
    return res


def _dpath(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


# ----------------------------------------------------------------- palettes
COOL = dict(
    far="#1c1a2c", wall_in="#62406a", wall_alt="#3a5874", wall_out="#3a2a4c", wall_low="#2f5560",
    pillow="#8a6896", tuck="#24182e", rib="#d8bcb4", rib_shadow="#a0808f", rib_hi="#f3e2d8",
    floor_far="#2b2238", floor="#61405c", floor_near="#6e4a63", floor_edge="#3e2a46", ridge="#87607c",
    sheen="#a6cfd2", puddle="#3c6f7c", crease="#2a1c38",
)
WARM = dict(
    far="#583036", wall_in="#d08a62", wall_alt="#c46c66", wall_out="#9a5458", wall_low="#b8704e",
    pillow="#f5bf8e", tuck="#6a3438", rib="#fbe6bc", rib_shadow="#e0ac7c", rib_hi="#fff6dc",
    floor_far="#5e3234", floor="#b87058", floor_near="#c88464", floor_edge="#8a4c48", ridge="#eaa87c",
    sheen="#ffe6ae", puddle="#e8b46a", crease="#7c3c40",
)
WALL_ALT = (0.1, 0.55, 0.2, 0.6, 0.15, 0.5, 0.25, 0.3)     # plum <-> teal (rose) panels, per gap

# soft folds in the walls between ribs: (gap, u, from deg, to deg, seed)
CREASES = ((5, 0.26, 162, 186, 1), (5, 0.42, 226, 247, 2), (5, 0.55, 296, 316, 3), (5, 0.5, -10, 12, 4),
           (4, 0.5, 194, 214, 5), (4, 0.45, 326, 344, 6))


def _fog(k):
    """0 = lost in the far darkness, 1 = clear."""
    return min(1.0, max(0.0, (k - 0.12) / 0.88)) ** 0.7


def _mound(x, y, rx, ry, pal, f, far, seed, soft=False):
    """A soft fleshy bump on the floor: shadow below, body, glossy highlight on top.
    soft=True blurs the body so it reads as a gentle swell of the floor rather than an object."""
    ridge, tuck = S.mix(far, pal["ridge"], f), S.mix(far, pal["tuck"], f)
    out = (f'<ellipse cx="{x:.1f}" cy="{y + ry * 0.55:.1f}" rx="{rx * 1.08:.1f}" ry="{ry * 0.7:.1f}" fill="{tuck}" '
           f'opacity="0.5" filter="url(#soft)"/>')
    flt = ' filter="url(#soft)"' if soft else ""
    out += (f'<path d="{S.blob(x, y - ry * 0.25, rx, ry, wobble=0.12, n=9, seed=seed)}" fill="{ridge}" '
            f'opacity="{0.75 if soft else 0.95}"{flt}/>')
    out += (f'<path d="M{x - rx * 0.5:.1f},{y - ry * 0.75:.1f} Q{x - rx * 0.05:.1f},{y - ry * 1.3:.1f} {x + rx * 0.42:.1f},'
            f'{y - ry * 0.85:.1f}" fill="none" stroke="{S.mix(far, pal["sheen"], f)}" stroke-width="{max(1.5, ry * 0.22):.1f}" '
            f'stroke-linecap="round" opacity="0.4"/>')
    return out


def belly_svg(pal, tag, vign_col, vign, pool_rim=True):
    defs = ""
    far = pal["far"]
    body = S.rect_bg(far)
    f0 = RIBS[0]
    defs += S.rad_grad(f"hole{tag}", [(0, S.mix(far, "#000000", 0.25)), (0.45, far),
                                      (1, S.mix(far, pal["wall_out"], 0.5))],
                       cx=f0["cx"] / W, cy=f0["cy"] / H, r=0.45)
    body += f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#hole{tag})"/>'

    # shared floor paint (user space, so the sections join seamlessly)
    yf0 = _floor_y(0)
    defs += (f'<linearGradient id="floor{tag}" gradientUnits="userSpaceOnUse" x1="0" y1="{yf0 - 30:.0f}" x2="0" '
             f'y2="{H}"><stop offset="0" stop-color="{far}"/><stop offset="0.12" stop-color="{S.mix(far, pal["floor_far"], 0.6)}"/>'
             f'<stop offset="0.4" stop-color="{pal["floor_far"]}"/><stop offset="0.72" stop-color="{pal["floor"]}"/>'
             f'<stop offset="1" stop-color="{pal["floor_near"]}"/></linearGradient>')
    defs += (f'<radialGradient id="flit{tag}" gradientUnits="userSpaceOnUse" cx="{GX:.0f}" cy="{JY:.0f}" r="640">'
             f'<stop offset="0" stop-color="{pal["ridge"]}" stop-opacity="0.45"/>'
             f'<stop offset="1" stop-color="{pal["ridge"]}" stop-opacity="0"/></radialGradient>')
    J = _junctions()

    # the far floor inside the farthest rib, sinking into the dark
    xl0, xr0 = _floor_x(0, -1), _floor_x(0, 1)
    ff = [(xl0 + 8, yf0 - 22), (xr0 - 8, yf0 - 22), (xr0, yf0), (xr0, H + 300), (xl0, H + 300), (xl0, yf0)]
    body += f'<path d="{S.smooth_path(ff, tension=0.4)}" fill="url(#floor{tag})"/>'

    rnd = random.Random(7)
    n_r = len(KS)
    for i in range(n_r):
        rb = RIBS[i]
        k = rb["k"]
        f = _fog(k)
        last = i == n_r - 1
        contour = S.smooth_path(_rib_pts(i, 96))
        ring = f"M-300,-300 H{W + 300} V{H + 300} H-300 Z " + contour
        if last:
            # the nearest rib, framing the corners of the picture (dark, close to us)
            body += f'<path d="{ring}" fill="{S.mix(pal["wall_out"], far, 0.55)}" fill-rule="evenodd"/>'
        else:
            alt = WALL_ALT[i % len(WALL_ALT)]
            w_in = S.mix(far, S.mix(pal["wall_in"], pal["wall_alt"], alt), f)
            w_out = S.mix(far, S.mix(pal["wall_out"], pal["wall_alt"], alt * 0.5), f)
            w_low = S.mix(far, pal["wall_low"], f)
            gid = f"wall{tag}{i}"
            defs += (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{GX:.0f}" cy="{GY - 150:.0f}" '
                     f'r="1500"><stop offset="0.2" stop-color="{w_in}"/><stop offset="0.6" stop-color="{w_out}"/>'
                     f'<stop offset="1" stop-color="{S.mix(w_out, far, 0.45)}"/></radialGradient>')
            lid = f"wlow{tag}{i}"
            yf = _floor_y(i)
            defs += (f'<linearGradient id="{lid}" gradientUnits="userSpaceOnUse" x1="0" y1="{yf - 520 * k:.0f}" '
                     f'x2="0" y2="{yf + 160 * k:.0f}"><stop offset="0" stop-color="{w_low}" stop-opacity="0"/>'
                     f'<stop offset="1" stop-color="{w_low}" stop-opacity="0.85"/></linearGradient>')
            body += f'<path d="{ring}" fill="url(#{gid})" fill-rule="evenodd"/>'
            body += f'<path d="{ring}" fill="url(#{lid})" fill-rule="evenodd"/>'
            # soft pillowy wall between this rib and the next nearer one: lit middle, shadow tucked under the rib
            gap = KS[i + 1] - k
            mid = S.smooth_path(_wall_pts(i, 0.5, wob=0.04, seed=40 + i))
            body += (f'<path d="{mid}" fill="none" stroke="{S.mix(far, pal["pillow"], f)}" '
                     f'stroke-width="{RY * gap * 0.5:.1f}" opacity="{0.42 * (0.35 + 0.65 * f):.2f}" '
                     f'filter="url(#blur-md)"/>')
            tuck = S.smooth_path(_wall_pts(i, 0.9, wob=0.02, seed=60 + i))
            body += (f'<path d="{tuck}" fill="none" stroke="{S.mix(far, pal["tuck"], f)}" '
                     f'stroke-width="{RY * gap * 0.2:.1f}" opacity="0.55" filter="url(#soft)"/>')
            # soft folds (creases) in the wall: blurred dark groove + a thin glossy edge
            for (gi, u, d0, d1, sd) in CREASES:
                if gi != i:
                    continue
                r2 = random.Random(sd)
                kk = k + gap * u
                pts, hi = [], []
                bow, ph = r2.uniform(0.02, 0.04) * r2.choice((-1, 1)), r2.uniform(0, 6.3)
                for j in range(9):
                    a = math.radians(d0 + (d1 - d0) * j / 8)
                    w = bow * math.sin(math.pi * j / 8) + 0.008 * math.sin(j * 1.7 + ph)
                    pts.append(_wall_pt(i, u + w, a))
                    hi.append(_wall_pt(i, u + w + 0.06, a))
                # (own user-space filter region: a thin vertical path's %-of-bbox region would clip the blur)
                xs, ys = [q[0] for q in pts], [q[1] for q in pts]
                pad = 40 * kk + 30
                cfid = f"cr{tag}{sd}"
                defs += (f'<filter id="{cfid}" filterUnits="userSpaceOnUse" x="{min(xs) - pad:.0f}" y="{min(ys) - pad:.0f}" '
                         f'width="{max(xs) - min(xs) + 2 * pad:.0f}" height="{max(ys) - min(ys) + 2 * pad:.0f}">'
                         f'<feGaussianBlur stdDeviation="{6 + 6 * kk:.1f}"/></filter>')
                body += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{S.mix(far, pal["crease"], f)}" '
                         f'stroke-width="{36 * kk:.1f}" stroke-linecap="round" opacity="0.5" filter="url(#{cfid})"/>')
                body += (f'<path d="{S.smooth_path(pts[1:-1], closed=False)}" fill="none" stroke="{S.mix(far, pal["crease"], f)}" '
                         f'stroke-width="{9 * kk:.1f}" stroke-linecap="round" opacity="0.35" filter="url(#{cfid})"/>')
                body += S.g(f'<path d="{S.smooth_path(hi[2:-2], closed=False)}" fill="none" '
                            f'stroke="{S.mix(far, pal["sheen"], f)}" stroke-width="{4.5 * kk:.1f}" stroke-linecap="round" '
                            f'opacity="0.3"/>', filter="wobble")
            # wet glints on the upper wall
            for j in range((5 if k < 0.9 else 3) if k >= 0.4 else 2):
                u = rnd.uniform(0.3, 0.7)
                a0 = math.radians(rnd.uniform(195, 345))
                p0, p1 = _wall_pt(i, u, a0), _wall_pt(i, u, a0 + math.radians(rnd.uniform(4, 9)))
                kk = k + gap * u
                body += (f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" stroke="{pal["sheen"]}" '
                         f'stroke-width="{7 * kk:.1f}" stroke-linecap="round" opacity="{0.3 * f:.2f}" filter="url(#soft)"/>')

        # the rib arch: a bone band, thick on top and tapering down to the floor, with an inner shadow and a highlight
        if last:
            bw, rib, rib_sh, rib_hi = 128.0, S.mix(pal["rib_shadow"], far, 0.45), S.mix(pal["rib_shadow"], far, 0.62), \
                S.mix(pal["rib"], far, 0.35)
            ink, ow = P["ink"], 5.0
        else:
            bw = 116 * k * rb["thick"]
            rib, rib_sh, rib_hi = (S.mix(far, pal[c], f) for c in ("rib", "rib_shadow", "rib_hi"))
            ink, ow = S.mix(far, P["ink"], max(0.3, f)), max(1.8, 4.5 * k)

        def wfun(a, bw=bw):
            return bw * (0.4 + 0.6 * max(0.0, -math.sin(a)) ** 0.85)
        outer = _rib_pts(i, 120, off=lambda a: wfun(a) / 2)
        inner = _rib_pts(i, 120, off=lambda a: -wfun(a) / 2)
        band = S.smooth_path(outer) + " " + S.smooth_path(inner)
        sh_d = S.smooth_path(_rib_pts(i, 96, off=lambda a: -wfun(a) * 0.3))
        hi_d = S.smooth_path(_rib_pts(i, 96, off=lambda a: wfun(a) * 0.2))
        cid = f"rb{tag}{i}"
        defs += f'<clipPath id="{cid}"><path d="{band}" clip-rule="evenodd"/></clipPath>'
        rib_svg = (f'<path d="{band}" fill="{rib}" fill-rule="evenodd"/>'
                   f'<g clip-path="url(#{cid})"><path d="{sh_d}" fill="none" stroke="{rib_sh}" '
                   f'stroke-width="{bw * 0.34:.1f}" opacity="0.8" filter="url(#soft)"/>'
                   f'<path d="{hi_d}" fill="none" stroke="{rib_hi}" stroke-width="{bw * 0.1:.1f}" opacity="0.8"/></g>'
                   f'<path d="{band}" fill="none" stroke="{ink}" stroke-width="{ow:.1f}" stroke-linejoin="round"/>')
        if not last:
            fid = f"rf{tag}{i}"
            defs += (f'<clipPath id="{fid}"><rect x="-400" y="-400" width="{W + 800}" '
                     f'height="{_floor_y(i) + 404:.1f}"/></clipPath>')
            rib_svg = f'<g clip-path="url(#{fid})">{rib_svg}</g>'
        body += S.g(rib_svg, filter="wobble")

        if last:
            continue
        # ---- the floor between this rib and the next nearer one (drawn now, so nearer walls hide it)
        k2 = KS[i + 1]
        f2 = _fog(k2)
        Lp, Rp = J[-1][i], J[1][i]
        sec = [Lp[0]] + [Rp[0]] + Rp[1:] + [(Rp[-1][0], H + 300), (Lp[-1][0], H + 300)] + Lp[::-1][:-1]
        floor = f'<path d="{_dpath(sec)}" fill="url(#floor{tag})"/>'
        floor += f'<path d="{_dpath(sec)}" fill="url(#flit{tag})"/>'
        # darker, soft edges where the floor curves up into the walls
        for side, pts in ((-1, Lp), (1, Rp)):
            shift = [(x - side * 26 * (k + k2) / 2, y + 4) for x, y in pts]
            floor += (f'<path d="{S.smooth_path(shift, closed=False)}" fill="none" stroke="{S.mix(far, pal["floor_edge"], f2)}" '
                      f'stroke-width="{70 * (k + k2) / 2:.1f}" stroke-linecap="round" opacity="0.5" filter="url(#blur-md)"/>')
        # 2-3 short, broken soft mounds where this rib sinks into the floor
        yf, xl, xr = _floor_y(i), _floor_x(i, -1), _floor_x(i, 1)
        r3 = random.Random(500 + i)
        mounds = [(xl + 16 * k, 62 * k, 26 * k, False), (xr - 16 * k, 58 * k, 25 * k, False)]
        if k >= 0.4:
            mounds.append((xl + (xr - xl) * r3.uniform(0.3, 0.7), (xr - xl) * r3.uniform(0.06, 0.09), 16 * k, True))
        for j, (mx, mrx, mry, soft) in enumerate(mounds):
            floor += _mound(mx, yf + 4 * k, mrx, mry, pal, f, far, seed=600 + i * 7 + j, soft=soft)
        body += S.g(floor, filter="wobble")

        if i == 2:
            # far-end fog: the bend of the belly sinks softly into darkness (nearer ribs paint over it)
            cxf, cyf = (RIBS[0]["cx"] + RIBS[1]["cx"]) / 2, (RIBS[0]["cy"] + RIBS[1]["cy"]) / 2 + 20
            defs += (f'<radialGradient id="fog{tag}" gradientUnits="userSpaceOnUse" cx="{cxf:.0f}" cy="{cyf:.0f}" '
                     f'r="300"><stop offset="0" stop-color="{far}" stop-opacity="0.9"/><stop offset="0.55" '
                     f'stop-color="{far}" stop-opacity="0.5"/><stop offset="1" stop-color="{far}" stop-opacity="0"/>'
                     f'</radialGradient>')
            body += f'<ellipse cx="{cxf:.0f}" cy="{cyf:.0f}" rx="380" ry="300" fill="url(#fog{tag})"/>'

        if i == n_r - 2:
            # puddles that will catch the golden light, and wet sheen on the near floor
            pud = ""
            for (x, y, rx, ry, op) in ((1215, 912, 118, 19, 0.85), (1330, 822, 58, 9, 0.6), (610, 868, 70, 11, 0.6)):
                pud += S.g(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{pal["puddle"]}" opacity="{op}" '
                           f'stroke="{S.mix(far, P["ink"], 0.7)}" stroke-width="2.5"/>'
                           f'<ellipse cx="{x - rx * 0.25:.1f}" cy="{y - ry * 0.25:.1f}" rx="{rx * 0.45:.1f}" '
                           f'ry="{max(2.0, ry * 0.25):.1f}" fill="{pal["sheen"]}" opacity="0.6"/>', filter="wobble-fine")
            for (x, y, rx, ry, op) in ((1050, 985, 180, 16, 0.2), (1470, 1010, 150, 14, 0.18), (1120, 840, 80, 9, 0.16)):
                pud += (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{pal["sheen"]}" opacity="{op}" '
                        f'filter="url(#soft)"/>')
            if pool_rim:
                # the pool's fleshy rim (its water is a separate layer above)
                rim_col = S.mix(pal["floor_near"], P["ink"], 0.18)
                pud += S.g(f'<ellipse cx="{PX}" cy="{PY + 8}" rx="{PRX + 28}" ry="{PRY + 20}" fill="{rim_col}" '
                           f'{S.STROKE}/>', filter="wobble")
            body += pud

    # dim vignette towards the edges (the light is with Jonah)
    defs += (f'<radialGradient id="vig{tag}" gradientUnits="userSpaceOnUse" cx="{GX + 80:.0f}" cy="{GY - 100:.0f}" '
             f'r="1400"><stop offset="0" stop-color="{vign_col}" stop-opacity="0"/>'
             f'<stop offset="0.3" stop-color="{vign_col}" stop-opacity="{0.09 * vign:.3f}"/>'
             f'<stop offset="0.7" stop-color="{vign_col}" stop-opacity="{0.4 * vign:.3f}"/>'
             f'<stop offset="1" stop-color="{vign_col}" stop-opacity="{0.65 * vign:.3f}"/></radialGradient>')
    body += f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#vig{tag})"/>'
    return S.svg_doc(body, defs=defs)


# a gentle dimming filter for props near the dark edges of the picture
def dim_defs(k=0.8):
    return (f'<filter id="dim" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
            f'values="{k:.3f} 0 0 0 0.01  0 {k - 0.03:.3f} 0 0 0.01  0 0 {k + 0.07:.3f} 0 0.03  0 0 0 1 0"/></filter>')


def dimmed(markup, k=0.8):
    return f'<defs>{dim_defs(k)}</defs><g filter="url(#dim)">{markup}</g>'


# ----------------------------------------------------------------- small drawings
def sun_icon(cx, cy, r):
    out = ""
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        p = [(cx + (r + 4) * math.cos(a - 0.28), cy + (r + 4) * math.sin(a - 0.28)),
             (cx + (r + 22) * math.cos(a), cy + (r + 22) * math.sin(a)),
             (cx + (r + 4) * math.cos(a + 0.28), cy + (r + 4) * math.sin(a + 0.28))]
        out += S.path(_dpath(p), fill=P["sun_hot"], sw=3)
    out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{P["sun"]}" {S.STROKE}/>'
    out += f'<circle cx="{cx - r * 0.25}" cy="{cy - r * 0.3}" r="{r * 0.22}" fill="#fff3c8" opacity="0.7"/>'
    out += f'<circle cx="{cx - r * 0.3:.1f}" cy="{cy - r * 0.05:.1f}" r="{r * 0.09:.1f}" fill="{P["ink"]}"/>'
    out += f'<circle cx="{cx + r * 0.3:.1f}" cy="{cy - r * 0.05:.1f}" r="{r * 0.09:.1f}" fill="{P["ink"]}"/>'
    out += (f'<path d="M{cx - r * 0.25:.1f},{cy + r * 0.25:.1f} Q{cx:.1f},{cy + r * 0.5:.1f} {cx + r * 0.25:.1f},'
            f'{cy + r * 0.25:.1f}" fill="none" {S.STROKE_THIN}/>')
    for sx in (-1, 1):
        out += (f'<ellipse cx="{cx + sx * r * 0.55:.1f}" cy="{cy + r * 0.22:.1f}" rx="{r * 0.15:.1f}" '
                f'ry="{r * 0.09:.1f}" fill="{P["cheek"]}" opacity="0.8"/>')
    return S.g(out, filter="wobble-fine")


def moon_icon(cx, cy, r):
    """Crescent moon (opening to the upper right) with a sleepy face and a tiny star."""
    ox, oy, rr = cx + r * 0.45, cy - r * 0.22, r * 0.84
    dx, dy = ox - cx, oy - cy
    dd = math.hypot(dx, dy)
    a = (r * r - rr * rr + dd * dd) / (2 * dd)
    hh = math.sqrt(max(0.0, r * r - a * a))
    mx, my = cx + a * dx / dd, cy + a * dy / dd
    p1 = (mx + hh * dy / dd, my - hh * dx / dd)
    p2 = (mx - hh * dy / dd, my + hh * dx / dd)
    d = (f"M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 1,0 {p2[0]:.1f},{p2[1]:.1f} "
         f"A{rr:.1f},{rr:.1f} 0 0,1 {p1[0]:.1f},{p1[1]:.1f} Z")
    out = S.path(d, fill="#f4e7b2", sw=4)
    out += f'<circle cx="{cx - r * 0.55:.1f}" cy="{cy + r * 0.38:.1f}" r="{r * 0.11:.1f}" fill="#e3cf8c"/>'
    out += f'<circle cx="{cx - r * 0.2:.1f}" cy="{cy + r * 0.72:.1f}" r="{r * 0.07:.1f}" fill="#e3cf8c"/>'
    ex, ey = cx - r * 0.42, cy - r * 0.02
    out += (f'<path d="M{ex - r * 0.15:.1f},{ey:.1f} Q{ex:.1f},{ey + r * 0.15:.1f} {ex + r * 0.15:.1f},{ey:.1f}" '
            f'fill="none" {S.STROKE_THIN}/>')
    out += (f'<ellipse cx="{ex - r * 0.02:.1f}" cy="{ey + r * 0.27:.1f}" rx="{r * 0.13:.1f}" ry="{r * 0.08:.1f}" '
            f'fill="{P["cheek"]}" opacity="0.8"/>')
    out += star_path(cx + r * 0.78, cy - r * 0.62, r * 0.24)
    return S.g(out, filter="wobble-fine")


def star_path(sx, sy, s, fill="#fff3c8", sw=2.5):
    pts = [(sx, sy - s), (sx + s * 0.3, sy - s * 0.3), (sx + s, sy), (sx + s * 0.3, sy + s * 0.3), (sx, sy + s),
           (sx - s * 0.3, sy + s * 0.3), (sx - s, sy), (sx - s * 0.3, sy - s * 0.3)]
    return S.path(_dpath(pts), fill=fill, sw=sw)


def drop_shape(x, y, s=1.0):
    d = (f"M{x:.1f},{y - 16 * s:.1f} C{x + 9 * s:.1f},{y - 3 * s:.1f} {x + 10 * s:.1f},{y + 8 * s:.1f} {x:.1f},{y + 9 * s:.1f} "
         f"C{x - 10 * s:.1f},{y + 8 * s:.1f} {x - 9 * s:.1f},{y - 3 * s:.1f} {x:.1f},{y - 16 * s:.1f} Z")
    return (S.path(d, fill=P["sea_pale"], sw=2.5) +
            f'<circle cx="{x - 3 * s:.1f}" cy="{y + 1 * s:.1f}" r="{2.2 * s:.1f}" fill="#fffaf0"/>')


def kelp_strand(x, y, length, width, col, seed=0, curl=1):
    """A ribbon of swallowed kelp draped over a rib at (x, y), hanging down with soft waves."""
    r = random.Random(seed)
    n = 9
    left, right = [], []
    for i in range(n + 1):
        u = i / n
        cx = x + curl * 26 * math.sin(u * 5.2 + seed) * u + r.uniform(-3, 3)
        cy = y - 44 + (length + 44) * u
        w = width * (0.75 + 0.35 * math.sin(u * 3.0 + 1)) * (1 - 0.65 * u ** 2)
        left.append((cx - w / 2, cy))
        right.append((cx + w / 2, cy))
    tip = (left[-1][0] + right[-1][0]) / 2, y + length + 14
    tw = (right[0][0] - left[0][0]) / 2
    top = [(left[0][0] + tw * 0.25, y - 44 - tw * 0.8), ((left[0][0] + right[0][0]) / 2, y - 44 - tw * 1.0),
           (right[0][0] - tw * 0.25, y - 44 - tw * 0.8)]
    pts = left + [tip] + right[::-1] + top[::-1]
    d = S.smooth_path(pts)
    mid = S.smooth_path([((a[0] + b[0]) / 2, a[1]) for a, b in zip(left, right)][1:-1], closed=False)
    return (S.path(d, fill=col, sw=3.5) +
            S.path(mid, stroke=False, extra=f'stroke="{S.shade(col, 0.3)}" stroke-width="3" opacity="0.7"'))


def kelp_tip(x, y, length, seed=0, curl=1):
    """Stage position of the pointed tip of kelp_strand(x, y, length, ..., seed, curl)."""
    r = random.Random(seed)
    n = 9
    cx = x
    for i in range(n + 1):
        u = i / n
        cx = x + curl * 26 * math.sin(u * 5.2 + seed) * u + r.uniform(-3, 3)
    return cx, y + length + 14


def starfish(x, y, r, col="#e98a5a", rot=0):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a) * 0.6))
    out = S.path(S.smooth_path(pts, tension=0.6), fill=col, sw=3)
    for i in range(5):
        a = math.radians(rot - 90 + i * 72)
        out += f'<circle cx="{x + r * 0.5 * math.cos(a):.1f}" cy="{y + r * 0.3 * math.sin(a):.1f}" r="2.5" fill="{S.shade(col, 0.5)}"/>'
    return S.g(out, filter="wobble-fine")


def shell(x, y, s, col="#f1d3c4"):
    d = (f"M{x - 26 * s:.1f},{y:.1f} Q{x - 30 * s:.1f},{y - 34 * s:.1f} {x:.1f},{y - 38 * s:.1f} "
         f"Q{x + 30 * s:.1f},{y - 34 * s:.1f} {x + 26 * s:.1f},{y:.1f} Z")
    out = S.path(d, fill=col, sw=3)
    for dx in (-14, -5, 5, 14):
        out += S.path(f"M{x:.1f},{y - 2:.1f} L{x + dx * s * 1.5:.1f},{y - 30 * s:.1f}", stroke=False,
                      extra=f'stroke="{S.shade(col, -0.3)}" stroke-width="2" fill="none"')
    out += f'<rect x="{x - 9 * s:.1f}" y="{y - 2:.1f}" width="{18 * s:.1f}" height="{8 * s:.1f}" rx="3" fill="{col}" {S.STROKE_THIN}/>'
    return S.g(out, filter="wobble-fine")


# ----------------------------------------------------------------- custom fx: sparkles that keep off Jonah's face
def _face_mask(face):
    """face = (cx, cy, rx, ry) in stage px -> m(x, y): 0 on the face, rising softly to 1 outside it."""
    if face is None:
        return lambda x, y: 1.0
    fcx, fcy, frx, fry = face

    def m(x, y):
        d = math.hypot((x - fcx) / frx, (y - fcy) / fry)
        return min(1.0, max(0.0, (d - 0.8) / 0.4))
    return m


def _star(d, ox, oy, r, color, a):
    w, g = r * 0.22, r * 0.6
    d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*color, a // 4))
    d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
               (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, a))


def rising_sparkles(cx, y_bottom, y_top, spread, count, level, color=(255, 232, 160), seed=21, face=None):
    """Golden sparkles rising around Jonah; level(t) 0..1 sets how many are lit. They fade out over his face."""
    rng = np.random.default_rng(seed)
    bx = rng.uniform(-spread, spread, count)
    ph = rng.uniform(0, 1, count)
    sp = rng.uniform(55, 110, count)
    sz = rng.uniform(7, 15, count)
    order = rng.permutation(count) / count
    span = y_bottom - y_top
    mask = _face_mask(face)

    def fx(frame, t, view):
        k = float(level(t))
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            if order[i] > k:
                continue
            u = (ph[i] + sp[i] * t / span) % 1.0          # 0 bottom -> 1 top
            yy = y_bottom - u * span
            xx = cx + bx[i] * (1 - 0.35 * u) + 18 * math.sin(t * 1.3 + i * 1.7)
            env = min(1.0, u / 0.15, (1 - u) / 0.3) * mask(xx, yy)
            tw = 0.65 + 0.35 * math.sin(t * 5 + i * 2.3)
            a = int(235 * env * tw * min(1.0, (k - order[i]) * 6 + 0.3))
            if a <= 4:
                continue
            ox, oy = view.to_out(xx, yy)
            _star(d, ox, oy, sz[i] * view.scale * (0.6 + 0.4 * tw), color, a)
        frame.alpha_composite(ov)
        return frame
    return fx


def twinkles(rect, count=24, t0=0.0, color=(255, 236, 170), size=(8, 20), period=1.6, drift=-12, seed=11, face=None):
    """FX.sparkles (twinkling four-point stars in a stage rect) that fade out over Jonah's face."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = rect
    px = rng.uniform(x0, x1, count)
    py = rng.uniform(y0, y1, count)
    ph = rng.uniform(0, 1, count)
    sz = rng.uniform(*size, count)
    mask = _face_mask(face)

    def fx(frame, t, view):
        k = M.progress(t, t0, t0 + 0.6, "sine")
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t / period + ph[i]))
            if tw < 0.15:
                continue
            yy = py[i] + drift * t
            a = int(230 * k * tw * mask(px[i], yy))
            if a <= 4:
                continue
            ox, oy = view.to_out(px[i], yy)
            _star(d, ox, oy, sz[i] * view.scale * (0.5 + 0.5 * tw), color, a)
        frame.alpha_composite(ov)
        return frame
    return fx


def _rot_pt(x, y, cx, cy, deg):
    """Rotate (x, y) about (cx, cy) by deg, clockwise on screen (same convention as the compositor)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c


# ----------------------------------------------------------------- build
def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2, L3 = (ctx.line(i) for i in range(4))

    # ---------------------------------------------------------- the belly (cool) + its warm, lit version
    warm_t0, warm_t1 = L2.start, L3.start + 0.9
    # (the cool belly is skipped once the warm one fully covers it — saves a full-frame draw)
    sc.add("belly_cool", belly_svg(COOL, "c", "#1a1430", 1.0), seed=11,
           motion=lambda t: Tf(alpha=1.0 if t < warm_t1 + 0.05 else 0.0))

    def warm_reveal(t):
        f = M.progress(t, warm_t0, warm_t1, "sine") * 1.35
        if f >= 1.34:
            return {"mode": "up", "frac": 1.0}
        return {"mode": "radial", "frac": f, "soft": 420, "cx": GX, "cy": GY}

    # the warm belly keeps a stronger warm-plum vignette, so the finale still has deep corners
    sc.add("belly_warm", belly_svg(WARM, "w", "#2a1420", 0.65), seed=11, reveal=warm_reveal,
           motion=M.keys([(warm_t0 - 0.05, {"alpha": 0}), (warm_t0 + 0.6, {"alpha": 1.0})], "sine"))

    # little glowing nubs on the walls (bioluminescence), gently pulsing; they go out as God's light comes
    def glow_cluster(centres):
        out = ""
        pts = []
        for (gi, u, ang, sc_) in centres:
            cx, cy = _wall_pt(gi, u, math.radians(ang))
            for (ox, oy, r) in ((0, 0, 15), (25, -9, 11), (-21, 9, 10), (6, 21, 8)):
                pts.append((cx + ox * sc_, cy + oy * sc_, r * sc_))
        for x, y, r in pts:
            out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="#6fd8cc" opacity="0.22" filter="url(#soft)"/>'
        for x, y, r in pts:
            out += S.g(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#9fe6da" stroke="{S.mix(P["ink"], "#2a5a66", 0.4)}" '
                       f'stroke-width="2.6"/><circle cx="{x - r * 0.32:.1f}" cy="{y - r * 0.32:.1f}" r="{r * 0.3:.1f}" '
                       f'fill="#f2fff8"/>', filter="wobble-fine")
        return S.svg_doc(out)
    nub_fade = M.keys([(L2.start, {"alpha": 1.0}), (L3.start + 0.5, {"alpha": 0.0})], "sine")
    sc.add("nubs_l", glow_cluster([(NEAR_I - 1, 0.2, 195, 0.95), (NEAR_I, 0.45, 236, 1.2)]), wc=0.3,
           motion=M.combine(M.pulse(0.6, 1.0, 2.8), nub_fade))
    sc.add("nubs_r", glow_cluster([(NEAR_I - 1, 0.5, 318, 0.9), (NEAR_I - 1, 0.55, 12, 0.8)]), wc=0.3,
           motion=M.combine(M.pulse(0.6, 1.0, 3.3, 0.4), nub_fade))

    # ---------------------------------------------------------- God's light behind Jonah
    halo = S.svg_doc(
        f'<circle cx="{GX}" cy="{GY}" r="640" fill="url(#halo)"/>',
        defs=S.rad_grad("halo", [(0, "#ffe6a6", 0.55), (0.22, "#fbd38a", 0.4), (0.52, "#f2ad5c", 0.2),
                                 (1, "#e8913f", 0)]))
    glow_keys = M.keys([(L2.start - 0.1, {"alpha": 0, "s": 0.3}), (L2.start + 1.4, {"alpha": 0.7, "s": 0.72}),
                        (L3.start, {"alpha": 0.9, "s": 1.0}), (L3.start + 0.7, {"alpha": 1.0, "s": 1.18})],
                       ["out", "sine", "out"], pivot=(GX, GY))
    sc.add("halo", halo, wc=0, motion=M.combine(glow_keys, M.breathe(0.025, 2.6, pivot=(GX, GY))))

    rays = S.svg_doc(S.path(S.rays(GX, GY, 200, 760, n=14, width_deg=4.5), fill="url(#rayg)", stroke=False,
                            extra='filter="url(#blur-md)"'),
                     defs=f'<radialGradient id="rayg" gradientUnits="userSpaceOnUse" cx="{GX}" cy="{GY}" r="760">'
                          f'<stop offset="0.2" stop-color="#6e4c22"/><stop offset="1" stop-color="#6e4c22" '
                          f'stop-opacity="0"/></radialGradient>')
    sc.add("rays", rays, wc=0, blend="add", motion=M.combine(
        M.keys([(L3.start - 0.7, {"alpha": 0, "s": 0.8}), (L3.start + 0.7, {"alpha": 1.0, "s": 1.0})], "out",
               pivot=(GX, GY)),
        lambda t: Tf(rot=2.2 * t, px=GX, py=GY)))

    # a faint cool rim of light behind Jonah so he reads in the dark
    rim = S.svg_doc(f'<ellipse cx="{JX - 20}" cy="{JY - 230}" rx="215" ry="240" fill="url(#rim)"/>',
                    defs=S.rad_grad("rim", [(0, "#22404a"), (0.6, "#0e1c22"), (1, "#000000")]))
    sc.add("rim", rim, wc=0, blend="add")

    # soft golden beam from the top glow down onto Jonah (God hears him) — BEHIND him, lighting the space,
    # not his line art
    beam_body = ""
    for wk in (1.0, 0.72, 0.46, 0.24):
        bx0, bx1 = TOP[0] - 10, GX - 15
        beam_body += (f'<path d="M{bx0 - 80 * wk:.0f},{TOP[1] - 60} L{bx0 + 80 * wk:.0f},{TOP[1] - 60} '
                      f'L{bx1 + 260 * wk:.0f},{JY + 10} L{bx1 - 260 * wk:.0f},{JY + 10} Z" fill="url(#beam)"/>')
    beam = S.svg_doc(S.g(beam_body, filter="blur-lg"),
                     defs=S.lin_grad("beam", [(0, "#4a3a20", 0.0), (0.15, "#4a3a20", 1), (0.75, "#3e2a14", 0.8),
                                              (1, "#3e2a14", 0.0)]))
    sc.add("beam", beam, wc=0, blend="add", motion=M.combine(
        M.keys([(L2.start, {"alpha": 0}), (L2.start + 1.6, {"alpha": 0.6}), (L3.start + 0.5, {"alpha": 0.9})],
               "sine"), M.pulse(0.85, 1.0, 3.1)))

    # ---------------------------------------------------------- Jonah: sits sad, then SWAPS (no crossfade) to kneel
    shadow = C.ground_shadow(JX + 10, JY, 1.0, width=320, opacity=0.4)
    ksw = L1.start - 0.05      # the swap, as "他在黑暗中…" begins
    sit = S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="sit", expr="sad"))
    sc.add("jonah_sit", sit, motion=M.combine(
        lambda t: Tf(alpha=1.0 if t < ksw else 0.0),
        M.keys([(ksw - 0.15, {"sy": 1.0, "dy": 0}), (ksw, {"sy": 0.95, "dy": 4})], "inout", pivot=(JX, JY)),
        M.breathe(0.012, 3.4, pivot=(JX, JY))))
    kneel = [S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="kneel_pray")),
             S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="kneel_pray", expr="happy"))]
    lift0, lift1 = L3.start - 0.1, L3.start + 0.5
    eyes_open = L3.start - 0.05
    sc.add("jonah_kneel", kneel, frame_at=lambda t: 0.0 if t < eyes_open else 1.0, motion=M.combine(
        lambda t: Tf(alpha=0.0 if t < ksw else 1.0),
        M.keys([(ksw, {"sy": 0.93, "dy": 6}), (ksw + 0.3, {"sy": 1.0, "dy": 0}), (lift0, {"rot": 0}),
                (lift1 + 0.3, {"rot": -3.0, "dy": -4})], ["back", "linear", "out"], pivot=(JX, JY)),
        M.breathe(0.01, 3.0, pivot=(JX, JY), phase=0.3)))

    # ---------------------------------------------------------- swallowed things on the floor
    stuff = PR.seaweed(1425, 868, 0.42, variant=2)
    stuff += PR.jar(1500, 862, 0.5, rot=78)
    stuff += shell(1580, 882, 0.8)
    stuff += starfish(705, 975, 30, rot=12)
    stuff += shell(1180, 1010, 0.9, "#e7c2d8")
    sc.add("floor_things", S.svg_doc(dimmed(stuff, 0.9)))

    # right foreground weeds: each clump rocks gently around its own base (no flipbook ghosting)
    for j, (x, y, s_, var, sw, deg, per, ph) in enumerate((
            (1860, 1075, 1.3, 0, 0.2, 2.4, 4.6, 0.0), (2010, 1095, 1.05, 2, -0.15, 3.0, 3.9, 0.35),
            (1710, 1090, 0.9, 1, 0.1, 2.0, 5.3, 0.6))):
        sc.add(f"weed{j}", S.svg_doc(dimmed(PR.seaweed(x, y, s_, variant=var, sway=sw), 0.72)),
               motion=M.sway(deg, per, (x, y), ph))

    # left: the pool (its rim is painted into the belly layers, so it warms up with them) with little fishes
    pool = f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="url(#pool)" {S.STROKE_THIN}/>'
    sc.add("pool", S.svg_doc(dimmed(S.g(pool, filter="wobble"), 0.8),
                             defs=S.rad_grad("pool", [(0, "#3f8c96"), (0.7, "#2a5f70"), (1, "#22465a")])))
    # each fish patrols back and forth inside the pool, turning at the ends; tails flip on whole frames
    # (back to front; phases chosen so the three never bunch up and don't all swim the same way)
    fishes = [("pink", 330, 986, 75, 19.0, 0.8), ("yellow", 440, 1010, 80, 20.0, 0.85),
              ("orange", 215, 1032, 80, 17.0, 0.5)]
    for i, (col, xc, yc, A, per, ph) in enumerate(fishes):
        frames = [S.svg_doc(dimmed(PR.small_fish(xc, yc, 0.85, fac, col, tail=tl), 0.84))
                  for fac in (1, -1) for tl in (-0.7, 0.7)]

        def fish_frame(t, per=per, ph=ph):
            right = math.cos(2 * math.pi * (t / per + ph)) >= 0
            return float((0 if right else 2) + int(t / 0.3 + ph * 3) % 2)

        def fish_motion(t, A=A, per=per, ph=ph):
            return Tf(dx=A * math.sin(2 * math.pi * (t / per + ph)), dy=4 * math.sin(2 * math.pi * (t / 2.2 + ph)))
        sc.add(f"fish{i}", frames, frame_at=fish_frame, motion=fish_motion)
    surf = (f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX - 4}" ry="{PRY - 3}" fill="#6fb3bd" opacity="0.36"/>'
            + S.path(f"M{PX - 220},{PY - 30} q40,-10 80,0 t80,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.7"')
            + S.path(f"M{PX + 40},{PY + 24} q35,-9 70,0 t70,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.55"'))
    sc.add("pool_surface", S.svg_doc(surf), wc=0.4, motion=M.bob(3, 3.0, axis="x"))

    # hanging kelp draped over the near rib (pendulum sway); drips fall from the middle strand's tip
    hx1, hx2 = 300.0, 1850.0
    hy1, hy2 = _rib_top_y(NEAR_I, hx1), _rib_top_y(NEAR_I, hx2)
    len1 = 300.0
    hang_l = (kelp_strand(hx1 - 30, hy1, 230, 34, "#5e7d3c", seed=1, curl=-1) +
              kelp_strand(hx1, hy1 + 4, len1, 40, P["olive"], seed=2) +
              kelp_strand(hx1 + 36, hy1 - 4, 170, 30, "#4f7a52", seed=3))
    SW_DEG, SW_PER = 2.0, 5.2

    def sway_l(t):
        return SW_DEG * math.sin(2 * math.pi * t / SW_PER)
    sc.add("hang_l", S.svg_doc(dimmed(S.g(hang_l, filter="wobble-fine"), 0.78)), motion=M.sway(SW_DEG, SW_PER, (hx1, hy1)))
    hang_r = (kelp_strand(hx2 - 24, hy2, 250, 36, P["olive"], seed=4) +
              kelp_strand(hx2 + 20, hy2 + 2, 190, 30, "#5e7d3c", seed=5, curl=-1))
    sc.add("hang_r", S.svg_doc(dimmed(S.g(hang_r, filter="wobble-fine"), 0.74)), motion=M.sway(-1.8, 4.4, (hx2, hy2), 0.3))

    tipx, tipy = kelp_tip(hx1, hy1 + 4, len1, seed=2)
    DS = 1.2
    DX, DY0 = tipx, tipy + 8            # the drop's centre while it hangs; its top touches the strand tip
    DTOP = DY0 - 16 * DS
    drips = (L0.start + 1.1, L2.start + 0.65, L3.start + 0.7)
    fall = 0.5

    def drop_motion(t):
        for td in drips:
            if td - 0.6 <= t < td:            # the drop swells at the tip, swaying with the kelp
                s = 0.3 + 0.7 * M.progress(t, td - 0.6, td, "out")
                th = sway_l(t)
                qx, qy = _rot_pt(DX, DTOP, hx1, hy1, th)
                return Tf(dx=qx - DX, dy=qy - DTOP, rot=th, sx=s, sy=s, alpha=1.0, px=DX, py=DTOP)
            if td <= t < td + fall:            # ... lets go and falls straight into the pool
                u = (t - td) / fall
                qx, qy = _rot_pt(DX, DTOP, hx1, hy1, sway_l(td))
                oy = qy - DTOP
                return Tf(dx=qx - DX, dy=oy + (PY - 4 - DY0 - oy) * u * u, alpha=1.0)
        return Tf(alpha=0.0)
    sc.add("drop", S.svg_doc(drop_shape(DX, DY0, DS)), wc=0, motion=drop_motion)

    def ripple_motion(delay):
        def m(t):
            for td in drips:
                ti = td + fall + delay
                if ti <= t < ti + 1.2:
                    u = (t - ti) / 1.2
                    s = 0.4 + 2.6 * M.ease("out")(u)
                    lx = _rot_pt(DX, DTOP, hx1, hy1, sway_l(td))[0] - DX
                    return Tf(dx=lx, sx=s, sy=s, alpha=0.9 * (1 - u), px=DX, py=PY - 4)
            return Tf(alpha=0.0)
        return m
    ring = S.svg_doc(f'<ellipse cx="{DX:.1f}" cy="{PY - 4}" rx="26" ry="7" fill="none" stroke="{P["sea_pale"]}" '
                     f'stroke-width="3.5"/>')
    sc.add("ripple_a", ring, wc=0, motion=ripple_motion(0.0))
    sc.add("ripple_b", ring, wc=0, motion=ripple_motion(0.28))

    # ---------------------------------------------------------- three days and three nights
    # A round glow opens at the top, then a sun + moon pair pops up on each pair of syllables of
    # '过了 / 三天 / 三夜' (the phrase fills the last ~1.25 s of line 0, ~0.19 s per syllable).
    # The row fades early in line 1, so "in the darkness" really looks dark before the light comes.
    n = 6
    t_pop0, step = L0.end - 1.27, 0.19
    fade0, fade1 = L1.start + 0.2, L1.start + 0.8
    top_glow = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] + 4}" rx="500" ry="125" fill="url(#tg)"/>',
        defs=S.rad_grad("tg", [(0, "#fff4d8", 0.5), (0.6, "#f6e2c0", 0.3), (1, "#f0d8b0", 0)]))
    sc.add("days_glow", top_glow, wc=0, motion=M.keys(
        [(t_pop0 - 0.7, {"alpha": 0}), (t_pop0 - 0.1, {"alpha": 1}), (fade0, {"alpha": 1}),
         (fade1 + 0.2, {"alpha": 0})], "sine"))
    gold_top = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] - 10}" rx="380" ry="160" fill="url(#gt)"/>',
        defs=S.rad_grad("gt", [(0, "#9a7a40", 1), (0.45, "#7a5a28", 0.6), (1, "#6a4a20", 0)]))
    sc.add("gold_top", gold_top, wc=0, blend="add", motion=M.combine(
        M.keys([(L2.start - 0.1, {"alpha": 0}), (L2.start + 0.8, {"alpha": 0.85})], "sine"),
        M.breathe(0.04, 2.6, pivot=TOP)))

    for i in range(n):
        x = TOP[0] + (i - (n - 1) / 2) * 150
        y = TOP[1] + ((i - (n - 1) / 2) / ((n - 1) / 2)) ** 2 * 20
        icon = sun_icon(x, y, 38) if i % 2 == 0 else moon_icon(x, y, 40)
        disc_col = "#ffe7a0" if i % 2 == 0 else "#cfe0f2"
        disc = f'<circle cx="{x}" cy="{y}" r="74" fill="url(#d{i})"/>'
        ti = t_pop0 + step * i
        sc.add(f"day{i}", S.svg_doc(disc + icon, defs=S.rad_grad(f"d{i}", [(0, disc_col, 0.9), (0.6, disc_col, 0.45),
                                                                          (1, disc_col, 0)])),
               wc=0.3, motion=M.combine(
                   M.keys([(ti, {"alpha": 0, "s": 0.2}), (ti + 0.15, {"alpha": 1}), (ti + 0.4, {"s": 1.0}),
                           (fade0 + 0.04 * i, {"alpha": 1, "dy": 0}),
                           (fade1 + 0.04 * i, {"alpha": 0, "dy": -26})],
                          ["sine", "back", "linear", "sine"], pivot=(x, y)),
                   M.bob(3, 2.4, i * 0.17)))

    # ---------------------------------------------------------- camera: slow push-in towards Jonah
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W)), (T, Cam(1000, 580, W * 0.85))], "sine")

    # ---------------------------------------------------------- particles (kept off Jonah's face)
    head = C.body_points(C.jonah, JX, JY, JS, 1, pose="kneel_pray")["head"]
    face = (head[0] - 8, head[1] - 2, 112, 118)

    def prayer_level(t):
        return (0.18 * M.progress(t, L1.start + 0.6, L1.end, "sine") +
                0.5 * M.progress(t, L2.start, L2.end, "sine") +
                0.32 * M.progress(t, L3.start - 0.2, L3.start + 0.6, "sine"))
    sc.fx = [
        FX.motes((0, 100, W, 950), count=18, color=(160, 205, 200), size=(3, 6), alpha=55, seed=5),
        rising_sparkles(GX + 10, JY - 20, 180, 230, 40, prayer_level, face=face),
        twinkles((GX - 330, GY - 330, GX + 330, GY + 180), count=18, t0=L3.start - 0.2,
                 color=(255, 240, 190), size=(8, 18), drift=-8, seed=17, face=face),
    ]

    # ---------------------------------------------------------- sound
    # beds end with the scene (fading across the outgoing transition) instead of running into s08
    sc.sfx("underwater", 0, dur=T + 0.1, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("heartbeat", 0, dur=T + 0.1, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("drip", 0, dur=T + 0.1, gain_db=-19, fade_in=0.8, fade_out=0.9, density=0.6)
    for td in drips:                    # the visible drops: a little plip as each lands in the pool
        sc.sfx("pop", td + fall, gain_db=-20, pan=-0.45)
    sc.sfx("cloth", ksw, gain_db=-16)
    sc.sfx("chime", L2.start, gain_db=-8)
    sc.sfx("sparkle", L3.start, gain_db=-9)
    return sc
