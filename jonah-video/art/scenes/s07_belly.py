"""Scene 7 — inside the great fish (Jonah 1:17-2:9).

Three days and three nights in the belly of the fish: a cosy, dim cave of soft rib arches over a wet fleshy
floor, a puddle with little fishes, swallowed seaweed and a jar from the ship. Line 0 counts the days with
three suns and three moons popping up one by one in a round glow at the top while Jonah sits sad; line 1 he
kneels and prays; lines 2-3 God hears him: a warm golden glow grows around him, sparkles rise, the walls warm
up from him outward, and at line 3 the glow is fullest and Jonah lifts his face, hopeful.

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
VP = (1240.0, 450.0)        # vanishing point (the far, dark end of the belly)
CN = (1070.0, 590.0)        # centre of the nearest rib ring
RX, RY = 1010.0, 560.0      # radii of the nearest rib ring
FLOOR_Y = 985.0             # floor height where it meets the nearest rib
SUPER = 2.4                 # superellipse exponent (slightly boxy, arch-like rings)
DEPTHS = (0.19, 0.24, 0.31, 0.42, 0.6, 1.0)     # far -> near (perspective scale of each rib)
NEAR_FRAME = 1.34                               # an extra, very near rib that frames the corners

JX, JY, JS = 880.0, 920.0, 1.62     # Jonah's anchor and scale
GX, GY = 858.0, 690.0              # centre of God's warm glow (Jonah's chest)
TOP = (1090.0, 195.0)              # the round "days" glow at the top


def _oval(k):
    cx = VP[0] + (CN[0] - VP[0]) * k
    cy = VP[1] + (CN[1] - VP[1]) * k
    return cx, cy, RX * k, RY * k


def _sp(c, e):
    return math.copysign(abs(c) ** (2 / e), c)


def _oval_pts(k, n=60, wob=0.0, seed=0):
    cx, cy, rx, ry = _oval(k)
    r = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        f = 1 + r.uniform(-wob, wob)
        pts.append((cx + f * rx * _sp(math.cos(a), SUPER), cy + f * ry * _sp(math.sin(a), SUPER)))
    return pts


def _oval_at(k, ang_deg):
    """Point on ring k at angle (deg; 0 = right, 90 = down, 270 = top)."""
    cx, cy, rx, ry = _oval(k)
    a = math.radians(ang_deg)
    return cx + rx * _sp(math.cos(a), SUPER), cy + ry * _sp(math.sin(a), SUPER)


def _floor_y(k):
    return VP[1] + (FLOOR_Y - VP[1]) * k


def _floor_x(k, side):
    """Where the floor meets the wall at depth k (side -1 left, +1 right)."""
    y = _floor_y(k)
    cx, cy, rx, ry = _oval(k)
    v = min(1.0, abs(y - cy) / ry)
    return cx + side * rx * (1 - v ** SUPER) ** (1 / SUPER)


def _ring_y_top(k, x):
    cx, cy, rx, ry = _oval(k)
    u = min(1.0, abs(x - cx) / rx)
    return cy - ry * (1 - u ** SUPER) ** (1 / SUPER)


def _dpath(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


# ----------------------------------------------------------------- palettes
COOL = dict(
    far="#1c1a2c", wall_in="#62406a", wall_out="#3a2a4c", wall_low="#2f5560", pillow="#8a6896",
    tuck="#24182e", rib="#d8bcb4", rib_shadow="#a0808f", rib_hi="#f3e2d8", floor_far="#2b2238",
    floor="#61405c", floor_near="#6e4a63", floor_edge="#3e2a46", ridge="#87607c", sheen="#a6cfd2",
    puddle="#3c6f7c",
)
WARM = dict(
    far="#583036", wall_in="#d08a62", wall_out="#9a5458", wall_low="#b8704e", pillow="#f5bf8e",
    tuck="#6a3438", rib="#fbe6bc", rib_shadow="#e0ac7c", rib_hi="#fff6dc", floor_far="#5e3234",
    floor="#b87058", floor_near="#c88464", floor_edge="#8a4c48", ridge="#eaa87c", sheen="#ffe6ae",
    puddle="#e8b46a",
)


def _fog(k):
    """0 = lost in the far darkness, 1 = clear."""
    return min(1.0, max(0.0, (k - 0.14) / 0.86)) ** 0.7


def belly_svg(pal, tag, vign_col, vign):
    defs = ""
    far = pal["far"]
    body = S.rect_bg(far)
    defs += S.rad_grad(f"hole{tag}", [(0, S.mix(far, "#000000", 0.2)), (0.5, far),
                                      (1, S.mix(far, pal["wall_out"], 0.5))], cx=VP[0] / W, cy=VP[1] / H, r=0.5)
    body += f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#hole{tag})"/>'
    ks = list(DEPTHS)
    rnd = random.Random(7)
    for i, k in enumerate(ks):
        f = _fog(k)
        w_in, w_out, w_low = (S.mix(far, pal[c], f) for c in ("wall_in", "wall_out", "wall_low"))
        gid = f"wall{tag}{i}"
        defs += (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{GX:.0f}" cy="{GY - 150:.0f}" '
                 f'r="1500"><stop offset="0.2" stop-color="{w_in}"/><stop offset="0.6" stop-color="{w_out}"/>'
                 f'<stop offset="1" stop-color="{S.mix(w_out, far, 0.45)}"/></radialGradient>')
        lid = f"wlow{tag}{i}"
        defs += (f'<linearGradient id="{lid}" gradientUnits="userSpaceOnUse" x1="0" y1="{_floor_y(k) - 520 * k:.0f}" '
                 f'x2="0" y2="{_floor_y(k):.0f}"><stop offset="0" stop-color="{w_low}" stop-opacity="0"/>'
                 f'<stop offset="1" stop-color="{w_low}" stop-opacity="0.85"/></linearGradient>')
        ring = f"M-200,-200 H{W + 200} V{H + 200} H-200 Z " + S.smooth_path(_oval_pts(k, wob=0.004, seed=i))
        body += f'<path d="{ring}" fill="url(#{gid})" fill-rule="evenodd"/>'
        body += f'<path d="{ring}" fill="url(#{lid})" fill-rule="evenodd"/>'
        # soft pillowy wall between this rib and the next nearer one: lit middle, shadow tucked under the rib
        k2 = ks[i + 1] if i + 1 < len(ks) else NEAR_FRAME
        gap = k2 - k
        mid = S.smooth_path(_oval_pts(k + gap * 0.5, wob=0.012, seed=40 + i))
        body += (f'<path d="{mid}" fill="none" stroke="{S.mix(far, pal["pillow"], f)}" '
                 f'stroke-width="{RY * gap * 0.55:.1f}" opacity="{0.5 * (0.35 + 0.65 * f):.2f}" filter="url(#blur-md)"/>')
        tuck = S.smooth_path(_oval_pts(k2 - gap * 0.1, wob=0.006, seed=60 + i))
        body += (f'<path d="{tuck}" fill="none" stroke="{S.mix(far, pal["tuck"], f)}" '
                 f'stroke-width="{RY * gap * 0.22:.1f}" opacity="0.55" filter="url(#soft)"/>')
        # wet glints on the upper wall
        for j in range((5 if k < 0.9 else 2) if k >= 0.4 else 2):
            kk = k + gap * rnd.uniform(0.3, 0.7)
            a0 = rnd.uniform(195, 345)
            p0, p1 = _oval_at(kk, a0), _oval_at(kk, a0 + rnd.uniform(4, 9))
            body += (f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" stroke="{pal["sheen"]}" '
                     f'stroke-width="{7 * kk:.1f}" stroke-linecap="round" opacity="{0.3 * f:.2f}" filter="url(#soft)"/>')
        # the rib arch: ink edge, bone band with a soft shadow along its inner edge and a highlight
        bw = 74 * k
        ow = max(1.8, 4.5 * k)
        rib, rib_sh, rib_hi = (S.mix(far, pal[c], f) for c in ("rib", "rib_shadow", "rib_hi"))
        ink = S.mix(far, P["ink"], max(0.3, f))
        rd = S.smooth_path(_oval_pts(k, wob=0.006, seed=20 + i))
        sh_d = S.smooth_path(_oval_pts(k - bw * 0.22 / RY, wob=0.006, seed=20 + i))
        hi_d = S.smooth_path(_oval_pts(k + bw * 0.16 / RY, wob=0.006, seed=20 + i))
        body += S.g(
            f'<path d="{rd}" fill="none" stroke="{ink}" stroke-width="{bw + 2 * ow:.1f}"/>'
            f'<path d="{rd}" fill="none" stroke="{rib}" stroke-width="{bw:.1f}"/>'
            f'<path d="{sh_d}" fill="none" stroke="{rib_sh}" stroke-width="{bw * 0.42:.1f}" opacity="0.75" '
            f'filter="url(#soft)"/>'
            f'<path d="{hi_d}" fill="none" stroke="{rib_hi}" stroke-width="{bw * 0.16:.1f}" opacity="0.8"/>',
            filter="wobble")

    # ---- floor: soft fleshy floor with lumpy edges, fading into the far darkness
    xl, xr = _floor_x(1.0, -1), _floor_x(1.0, 1)
    fl = [(VP[0], VP[1] + 6), (xl, FLOOR_Y), (-80, FLOOR_Y + 120), (-80, H + 80), (W + 80, H + 80),
          (W + 80, FLOOR_Y + 120), (xr, FLOOR_Y)]
    defs += (f'<linearGradient id="floor{tag}" gradientUnits="userSpaceOnUse" x1="0" y1="{VP[1]:.0f}" x2="0" '
             f'y2="{H}"><stop offset="0" stop-color="{far}"/><stop offset="0.2" stop-color="{far}"/>'
             f'<stop offset="0.42" stop-color="{pal["floor_far"]}"/><stop offset="0.75" stop-color="{pal["floor"]}"/><stop offset="1" stop-color="{pal["floor_near"]}"/>'
             f'</linearGradient>')
    defs += (f'<radialGradient id="flit{tag}" gradientUnits="userSpaceOnUse" cx="{GX:.0f}" cy="{JY:.0f}" r="620">'
             f'<stop offset="0" stop-color="{pal["ridge"]}" stop-opacity="0.45"/>'
             f'<stop offset="1" stop-color="{pal["ridge"]}" stop-opacity="0"/></radialGradient>')
    floor = f'<path d="{_dpath(fl)}" fill="url(#floor{tag})"/>'
    floor += f'<path d="{_dpath(fl)}" fill="url(#flit{tag})"/>'
    # darker floor edges along the walls (the floor curves up into them)
    for side in (-1, 1):
        edge = [(VP[0], VP[1] + 6)]
        for kk in (0.25, 0.4, 0.6, 0.8, 1.0, 1.25):
            edge.append((VP[0] + (_floor_x(1.0, side) - VP[0]) * kk + side * 4, _floor_y(kk)))
        for kk in (1.25, 1.0, 0.8, 0.6, 0.4, 0.25):
            edge.append((VP[0] + (_floor_x(1.0, side) - VP[0]) * kk - side * 150 * kk, _floor_y(kk) + 10 * kk))
        floor += (f'<path d="{S.smooth_path(edge)}" fill="{pal["floor_edge"]}" opacity="0.55" '
                  f'filter="url(#blur-md)"/>')
    # soft ridges across the floor at every rib (the ribs' ends sink into the floor)
    for i, k in enumerate(DEPTHS):
        if k < 0.24:
            continue
        f = _fog(k)
        y = _floor_y(k)
        a, b = _floor_x(k, -1), _floor_x(k, 1)
        sag = 30 * k
        top = f"M{a:.1f},{y:.1f} Q{(a + b) / 2:.1f},{y + 2 * sag:.1f} {b:.1f},{y:.1f}"
        floor += (f'<path d="{top}" fill="none" stroke="{S.mix(far, pal["floor_edge"], f)}" '
                  f'stroke-width="{34 * k:.1f}" stroke-linecap="round" opacity="0.55" '
                  f'transform="translate(0,{12 * k:.1f})" filter="url(#soft)"/>')
        floor += (f'<path d="{top}" fill="none" stroke="{S.mix(far, pal["ridge"], f)}" '
                  f'stroke-width="{22 * k:.1f}" stroke-linecap="round" opacity="0.8"/>')
        # soft contact shadows where the bones sink into the floor
        for side, xx in ((-1, a), (1, b)):
            floor += (f'<ellipse cx="{xx - side * 30 * k:.1f}" cy="{y + 6 * k:.1f}" rx="{80 * k:.1f}" '
                      f'ry="{18 * k:.1f}" fill="{pal["tuck"]}" opacity="0.6" filter="url(#soft)"/>')
    # puddles that will catch the golden light, and wet sheen
    for (x, y, rx, ry, op) in ((1235, 905, 120, 20, 0.85), (1385, 790, 60, 9, 0.6), (620, 860, 70, 11, 0.6)):
        floor += S.g(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{pal["puddle"]}" opacity="{op}" '
                     f'stroke="{S.mix(far, P["ink"], 0.7)}" stroke-width="2.5"/>'
                     f'<ellipse cx="{x - rx * 0.25:.1f}" cy="{y - ry * 0.25:.1f}" rx="{rx * 0.45:.1f}" '
                     f'ry="{max(2.0, ry * 0.25):.1f}" fill="{pal["sheen"]}" opacity="0.6"/>', filter="wobble-fine")
    for (x, y, rx, ry, op) in ((1050, 975, 180, 16, 0.22), (1460, 1000, 150, 14, 0.2), (1110, 820, 80, 9, 0.18)):
        floor += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{pal["sheen"]}" opacity="{op}" filter="url(#soft)"/>'
    body += S.g(floor, filter="wobble")
    # far-end fog: the tunnel (and its floor) sink softly into darkness
    defs += (f'<radialGradient id="fog{tag}" gradientUnits="userSpaceOnUse" cx="{VP[0]:.0f}" cy="{VP[1] + 30:.0f}" '
             f'r="320"><stop offset="0" stop-color="{far}" stop-opacity="0.92"/><stop offset="0.5" '
             f'stop-color="{far}" stop-opacity="0.55"/><stop offset="1" stop-color="{far}" stop-opacity="0"/>'
             f'</radialGradient>')
    body += f'<ellipse cx="{VP[0]:.0f}" cy="{VP[1] + 30:.0f}" rx="420" ry="330" fill="url(#fog{tag})"/>'

    # ---- the nearest rib, framing the corners of the picture (dark, close to us)
    k = NEAR_FRAME
    ringn = f"M-200,-200 H{W + 200} V{H + 200} H-200 Z " + S.smooth_path(_oval_pts(k, wob=0.004, seed=91))
    body += f'<path d="{ringn}" fill="{S.mix(pal["wall_out"], far, 0.55)}" fill-rule="evenodd"/>'
    bw = 120
    rd = S.smooth_path(_oval_pts(k, wob=0.006, seed=92))
    rib_near = S.mix(pal["rib_shadow"], far, 0.45)
    body += S.g(f'<path d="{rd}" fill="none" stroke="{P["ink"]}" stroke-width="{bw + 10}"/>'
                f'<path d="{rd}" fill="none" stroke="{rib_near}" stroke-width="{bw}"/>'
                f'<path d="{S.smooth_path(_oval_pts(k + 0.02, wob=0.006, seed=92))}" fill="none" '
                f'stroke="{S.mix(pal["rib"], far, 0.35)}" stroke-width="16" opacity="0.7"/>', filter="wobble")
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


# ----------------------------------------------------------------- custom fx: rising prayer sparkles
def rising_sparkles(cx, y_bottom, y_top, spread, count, level, color=(255, 232, 160), seed=21):
    """Golden sparkles rising around Jonah; level(t) 0..1 sets how many are lit."""
    rng = np.random.default_rng(seed)
    bx = rng.uniform(-spread, spread, count)
    ph = rng.uniform(0, 1, count)
    sp = rng.uniform(55, 110, count)
    sz = rng.uniform(7, 15, count)
    order = rng.permutation(count) / count
    span = y_bottom - y_top

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
            env = min(1.0, u / 0.15, (1 - u) / 0.3)
            tw = 0.65 + 0.35 * math.sin(t * 5 + i * 2.3)
            a = int(235 * env * tw * min(1.0, (k - order[i]) * 6 + 0.3))
            if a <= 4:
                continue
            ox, oy = view.to_out(xx, yy)
            r = sz[i] * view.scale * (0.6 + 0.4 * tw)
            w = r * 0.22
            g = r * 0.6
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*color, a // 4))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


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

    sc.add("belly_warm", belly_svg(WARM, "w", "#2a1420", 0.42), seed=11, reveal=warm_reveal,
           motion=M.keys([(warm_t0 - 0.05, {"alpha": 0}), (warm_t0 + 0.6, {"alpha": 1.0})], "sine"))

    # little glowing nubs on the walls (bioluminescence), gently pulsing; they fade as God's light comes
    def glow_cluster(centres):
        out = ""
        for (k, ang, sc_) in centres:
            cx, cy = _oval_at(k, ang)
            for (ox, oy, r) in ((0, 0, 15), (25, -9, 11), (-21, 9, 10), (6, 21, 8)):
                x, y, r = cx + ox * sc_, cy + oy * sc_, r * sc_
                out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="#6fd8cc" opacity="0.22" filter="url(#soft)"/>'
            for (ox, oy, r) in ((0, 0, 15), (25, -9, 11), (-21, 9, 10), (6, 21, 8)):
                x, y, r = cx + ox * sc_, cy + oy * sc_, r * sc_
                out += S.g(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#9fe6da" stroke="{S.mix(P["ink"], "#2a5a66", 0.4)}" '
                           f'stroke-width="2.6"/><circle cx="{x - r * 0.32:.1f}" cy="{y - r * 0.32:.1f}" r="{r * 0.3:.1f}" '
                           f'fill="#f2fff8"/>', filter="wobble-fine")
        return S.svg_doc(out)
    nub_fade = M.keys([(L2.start, {"alpha": 1.0}), (L3.start, {"alpha": 0.35})], "sine")
    sc.add("nubs_l", glow_cluster([(0.8, 214, 1.0), (1.17, 236, 1.2)]), wc=0.3,
           motion=M.combine(M.pulse(0.6, 1.0, 2.8), nub_fade))
    sc.add("nubs_r", glow_cluster([(0.8, 324, 0.9), (0.82, 14, 0.8)]), wc=0.3,
           motion=M.combine(M.pulse(0.6, 1.0, 3.3, 0.4), nub_fade))

    # ---------------------------------------------------------- God's light behind Jonah
    halo = S.svg_doc(
        f'<circle cx="{GX}" cy="{GY}" r="640" fill="url(#halo)"/>',
        defs=S.rad_grad("halo", [(0, "#ffe6a6", 0.72), (0.22, "#fbd38a", 0.55), (0.52, "#f2ad5c", 0.25),
                                 (1, "#e8913f", 0)]))
    glow_keys = M.keys([(L2.start - 0.1, {"alpha": 0, "s": 0.3}), (L2.start + 1.4, {"alpha": 0.7, "s": 0.72}),
                        (L3.start, {"alpha": 0.9, "s": 1.0}), (L3.start + 0.7, {"alpha": 1.0, "s": 1.18})],
                       ["out", "sine", "out"], pivot=(GX, GY))
    sc.add("halo", halo, wc=0, motion=M.combine(glow_keys, M.breathe(0.025, 2.6, pivot=(GX, GY))))

    rays = S.svg_doc(S.path(S.rays(GX, GY, 200, 760, n=14, width_deg=4.5), fill="url(#rayg)", stroke=False,
                            extra='filter="url(#blur-md)"'),
                     defs=f'<radialGradient id="rayg" gradientUnits="userSpaceOnUse" cx="{GX}" cy="{GY}" r="760">'
                          f'<stop offset="0.2" stop-color="#7a5626"/><stop offset="1" stop-color="#7a5626" '
                          f'stop-opacity="0"/></radialGradient>')
    sc.add("rays", rays, wc=0, blend="add", motion=M.combine(
        M.keys([(L3.start - 0.7, {"alpha": 0, "s": 0.8}), (L3.start + 0.7, {"alpha": 1.0, "s": 1.0})], "out",
               pivot=(GX, GY)),
        lambda t: Tf(rot=2.2 * t, px=GX, py=GY)))

    # a faint cool rim of light behind Jonah so he reads in the dark
    rim = S.svg_doc(f'<ellipse cx="{JX - 20}" cy="{JY - 230}" rx="215" ry="240" fill="url(#rim)"/>',
                    defs=S.rad_grad("rim", [(0, "#22404a"), (0.6, "#0e1c22"), (1, "#000000")]))
    sc.add("rim", rim, wc=0, blend="add")

    # ---------------------------------------------------------- Jonah
    shadow = C.ground_shadow(JX + 10, JY, 1.0, width=320, opacity=0.4)
    k0, k1 = L1.start - 0.2, L1.start + 0.12      # kneeling down as "他在黑暗中…" begins
    sit = S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="sit", expr="sad"))
    sc.add("jonah_sit", sit, motion=M.combine(
        M.breathe(0.012, 3.4, pivot=(JX, JY)),
        M.keys([(k0 + 0.16, {"alpha": 1, "dy": 0}), (k1 + 0.12, {"alpha": 0, "dy": -14})], "sine")))
    kneel = [S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="kneel_pray")),
             S.svg_doc(shadow + C.jonah(JX, JY, JS, 1, pose="kneel_pray", expr="happy"))]
    lift0, lift1 = L3.start - 0.1, L3.start + 0.5
    sc.add("jonah_kneel", kneel, frame_at=lambda t: M.progress(t, lift0, lift1, "sine"), motion=M.combine(
        M.breathe(0.01, 3.0, pivot=(JX, JY), phase=0.3),
        M.keys([(k0, {"alpha": 0, "dy": 22}), (k1, {"alpha": 1, "dy": 0}), (lift0, {"rot": 0}),
                (lift1 + 0.3, {"rot": -3.0, "dy": -4})], ["sine", "linear", "out"], pivot=(JX, JY))))

    # ---------------------------------------------------------- swallowed things on the floor
    stuff = PR.seaweed(1425, 868, 0.42, variant=2)
    stuff += PR.jar(1500, 862, 0.5, rot=78)
    stuff += shell(1580, 882, 0.8)
    stuff += starfish(705, 975, 30, rot=12)
    stuff += shell(1180, 1010, 0.9, "#e7c2d8")
    sc.add("floor_things", S.svg_doc(dimmed(stuff, 0.9)))

    def weeds_right(sw):
        return S.svg_doc(dimmed(PR.seaweed(1860, 1075, 1.3, variant=0, sway=sw) +
                                PR.seaweed(2010, 1095, 1.05, variant=2, sway=-sw * 0.8) +
                                PR.seaweed(1710, 1090, 0.9, variant=1, sway=sw * 0.6), 0.72))
    sc.add("weeds_r", [weeds_right(s) for s in (-0.7, -0.35, 0.0, 0.35, 0.7)],
           frame_at=lambda t: 2 + 2 * math.sin(2 * math.pi * t / 4.6))

    # left: the puddle with little fishes
    PX, PY, PRX, PRY = 320.0, 1010.0, 320.0, 72.0
    pool = (f'<ellipse cx="{PX}" cy="{PY + 8}" rx="{PRX + 28}" ry="{PRY + 20}" fill="{COOL["floor_near"]}" '
            f'{S.STROKE}/>'
            f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="url(#pool)" {S.STROKE_THIN}/>')
    sc.add("pool", S.svg_doc(dimmed(S.g(pool, filter="wobble"), 0.8),
                             defs=S.rad_grad("pool", [(0, "#3f8c96"), (0.7, "#2a5f70"), (1, "#22465a")])))
    fishes = [("orange", 1, 90, 1030, 14, 0.0), ("yellow", -1, 570, 1008, -12, 0.4), ("pink", 1, 400, 966, 8, 0.7)]
    for i, (col, fac, x0, y0, vx, ph) in enumerate(fishes):
        frames = [S.svg_doc(dimmed(PR.small_fish(x0, y0, 0.85, fac, col, tail=tl), 0.84)) for tl in (-0.7, 0.7)]
        sc.add(f"fish{i}", frames, frame_at=lambda t, ph=ph: 0.5 + 0.5 * math.sin(2 * math.pi * (t / 0.8 + ph)),
               motion=M.combine(M.drift(vx=vx), M.bob(4, 2.2, ph)))
    surf = (f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX - 4}" ry="{PRY - 3}" fill="#6fb3bd" opacity="0.36"/>'
            + S.path(f"M{PX - 220},{PY - 30} q40,-10 80,0 t80,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.7"')
            + S.path(f"M{PX + 40},{PY + 24} q35,-9 70,0 t70,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.55"'))
    sc.add("pool_surface", S.svg_doc(surf), wc=0.4, motion=M.bob(3, 3.0, axis="x"))

    # hanging kelp draped over the near rib (pendulum sway); drips fall from the left strand's tip
    hx1, hx2 = 300.0, 1850.0
    hy1, hy2 = _ring_y_top(1.0, hx1), _ring_y_top(1.0, hx2)
    len1 = 300.0
    hang_l = (kelp_strand(hx1 - 30, hy1, 230, 34, "#5e7d3c", seed=1, curl=-1) +
              kelp_strand(hx1, hy1 + 4, len1, 40, P["olive"], seed=2) +
              kelp_strand(hx1 + 36, hy1 - 4, 170, 30, "#4f7a52", seed=3))
    sc.add("hang_l", S.svg_doc(dimmed(S.g(hang_l, filter="wobble-fine"), 0.78)), motion=M.sway(2.0, 5.2, (hx1, hy1)))
    hang_r = (kelp_strand(hx2 - 24, hy2, 250, 36, P["olive"], seed=4) +
              kelp_strand(hx2 + 20, hy2 + 2, 190, 30, "#5e7d3c", seed=5, curl=-1))
    sc.add("hang_r", S.svg_doc(dimmed(S.g(hang_r, filter="wobble-fine"), 0.74)), motion=M.sway(-1.8, 4.4, (hx2, hy2), 0.3))

    DX, DY0 = hx1, hy1 + len1 + 6
    drips = (1.7, 6.6, 10.6)
    fall = 0.5

    def drop_motion(t):
        for td in drips:
            if td - 0.6 <= t < td:            # the drop swells at the tip
                s = 0.3 + 0.7 * M.progress(t, td - 0.6, td, "out")
                return Tf(sx=s, sy=s, alpha=1.0, px=DX, py=DY0 - 14)
            if td <= t < td + fall:
                u = (t - td) / fall
                return Tf(dy=(PY - 4 - DY0) * u * u, alpha=1.0)
        return Tf(alpha=0.0)
    sc.add("drop", S.svg_doc(drop_shape(DX, DY0, 1.2)), wc=0, motion=drop_motion)

    def ripple_motion(delay):
        def m(t):
            for td in drips:
                ti = td + fall + delay
                if ti <= t < ti + 1.2:
                    u = (t - ti) / 1.2
                    s = 0.4 + 2.6 * M.ease("out")(u)
                    return Tf(sx=s, sy=s, alpha=0.9 * (1 - u), px=DX, py=PY - 4)
            return Tf(alpha=0.0)
        return m
    ring = S.svg_doc(f'<ellipse cx="{DX}" cy="{PY - 4}" rx="26" ry="7" fill="none" stroke="{P["sea_pale"]}" '
                     f'stroke-width="3.5"/>')
    sc.add("ripple_a", ring, wc=0, motion=ripple_motion(0.0))
    sc.add("ripple_b", ring, wc=0, motion=ripple_motion(0.28))

    # soft golden beam from the top glow down onto Jonah (God hears him)
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

    # ---------------------------------------------------------- three days and three nights
    top_glow = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] + 4}" rx="500" ry="125" fill="url(#tg)"/>',
        defs=S.rad_grad("tg", [(0, "#fff4d8", 0.5), (0.6, "#f6e2c0", 0.3), (1, "#f0d8b0", 0)]))
    sc.add("days_glow", top_glow, wc=0, motion=M.keys(
        [(0.5, {"alpha": 0}), (1.0, {"alpha": 1}), (L1.start + 0.6, {"alpha": 1}), (L1.end, {"alpha": 0})], "sine"))
    gold_top = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] - 10}" rx="380" ry="160" fill="url(#gt)"/>',
        defs=S.rad_grad("gt", [(0, "#9a7a40", 1), (0.45, "#7a5a28", 0.6), (1, "#6a4a20", 0)]))
    sc.add("gold_top", gold_top, wc=0, blend="add", motion=M.combine(
        M.keys([(L2.start - 0.1, {"alpha": 0}), (L2.start + 0.8, {"alpha": 1})], "sine"),
        M.breathe(0.04, 2.6, pivot=TOP)))

    n = 6
    t_first, t_last = L0.start + 0.35, L0.end - 0.55
    for i in range(n):
        x = TOP[0] + (i - (n - 1) / 2) * 150
        y = TOP[1] + ((i - (n - 1) / 2) / ((n - 1) / 2)) ** 2 * 20
        icon = sun_icon(x, y, 38) if i % 2 == 0 else moon_icon(x, y, 40)
        disc_col = "#ffe7a0" if i % 2 == 0 else "#cfe0f2"
        disc = f'<circle cx="{x}" cy="{y}" r="74" fill="url(#d{i})"/>'
        ti = t_first + (t_last - t_first) * i / (n - 1)
        sc.add(f"day{i}", S.svg_doc(disc + icon, defs=S.rad_grad(f"d{i}", [(0, disc_col, 0.9), (0.6, disc_col, 0.45),
                                                                          (1, disc_col, 0)])),
               wc=0.3, motion=M.combine(
                   M.keys([(ti, {"alpha": 0, "s": 0.2}), (ti + 0.18, {"alpha": 1}), (ti + 0.42, {"s": 1.0}),
                           (L1.start + 0.6 + 0.08 * i, {"alpha": 1, "dy": 0}),
                           (L1.end + 0.08 * i, {"alpha": 0, "dy": -26})],
                          ["sine", "back", "linear", "sine"], pivot=(x, y)),
                   M.bob(3, 2.4, i * 0.17)))

    # ---------------------------------------------------------- camera: slow push-in towards Jonah
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W)), (T, Cam(1000, 580, W * 0.85))], "sine")

    # ---------------------------------------------------------- particles
    def prayer_level(t):
        return (0.18 * M.progress(t, L1.start + 0.6, L1.end, "sine") +
                0.5 * M.progress(t, L2.start, L2.end, "sine") +
                0.32 * M.progress(t, L3.start - 0.2, L3.start + 0.6, "sine"))
    sc.fx = [
        FX.motes((0, 100, W, 950), count=18, color=(160, 205, 200), size=(3, 6), alpha=55, seed=5),
        rising_sparkles(GX + 10, JY - 20, 180, 230, 40, prayer_level),
        FX.sparkles((GX - 330, GY - 330, GX + 330, GY + 180), count=18, t0=L3.start - 0.2,
                    color=(255, 240, 190), size=(8, 18), drift=-8, seed=17),
    ]

    # ---------------------------------------------------------- sound
    sc.sfx("underwater", 0, dur=T + 0.6, gain_db=-12, fade_in=0.8, fade_out=1.0)
    sc.sfx("heartbeat", 0, dur=T + 0.6, gain_db=-12, fade_in=0.8, fade_out=1.0)
    sc.sfx("drip", 0, dur=T + 0.6, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", k0, gain_db=-16)
    sc.sfx("chime", L2.start, gain_db=-8)
    sc.sfx("sparkle", L3.start, gain_db=-9)
    return sc
