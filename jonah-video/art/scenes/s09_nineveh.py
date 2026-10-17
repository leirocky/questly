"""Scene 9 — Nineveh (Jonah 3:1-4).

God calls Jonah a second time; this time he obeys, walks into the great city and preaches.

Staging (one wide 3300 x 1188 stage, no cuts):
  * line 0 — a sandy road among palms outside the great city. Clouds part, soft golden rays shine on Jonah; he
    looks up and listens, nods ("他听话了") and sets off toward the gate (walk_a/walk_b flipbook).
  * line 1 — the camera pans gently across the Nineveh panorama: massive crenellated wall (closed by a corner
    tower) with a big open gate, a ziggurat rising above the wall beside the gate, rooftops, palms, flat-roofed
    houses and the river Tigris. Jonah, small under the towering gate, walks into the passage; the camera "flies
    through" the arch (every outside layer scales up around the opening until the opening fills the frame, then
    the outside is dropped) and we are inside, in a busy market square. The inside of the city is painted
    *behind* the outside layers, so it is what shows above the wall and through the gate arch before that.
    Jonah walks out of the passage straight onto the stone step (he stays at step-top level the whole way).
  * line 2 — Jonah stands on the step, arm raised, and calls out; townspeople stop, turn toward him, are
    surprised (two of them point at him), then worried.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3300, 1188

# outside geometry -----------------------------------------------------------------------------
WALL_X0, WALL_X1, WALL_Y, WALL_H = 1060, 3340, 880, 440
GX, GWD = 1720, 230                         # gate centre x and width
_K = WALL_H / 260.0
_SPRING = WALL_Y - WALL_H * 0.62
_R2 = GWD / 2 * 0.55                        # bright far-side opening (we cut it out to see the city inside)
HOLE_TOP = _SPRING + 30 * _K - _R2
GATE_C = (GX, (HOLE_TOP + WALL_Y) / 2)      # centre of the gate opening (y pivot of the fly-through)
# the part of the opening that is clear of its rim stroke, wobble and the outside ground (x0, x1, spring y, bottom)
HOLE_CLEAR = (GX - _R2 + 8, GX + _R2 - 8, _SPRING + 30 * _K, WALL_Y - 12)

# inside geometry ------------------------------------------------------------------------------
SKY_X0, SKY_SEED = 860, 55                  # inside skyline (its own hazy ziggurat lands left of the gate)
ZIG_X, ZIG_S = 2280, 0.5                    # the big ziggurat, beside the gate (right of its tower)
BACK_Y = 792                                # ground line of the back row of houses
STEP_X, STEP_Y = 1850, 934                  # step platform: centre x, ground (bottom) line
STEP_TOP = 872                              # where Jonah stands (front edge of the upper tier)

JONAH_S = 0.95
STEP = 0.26                                 # seconds per walking stride outside (flipbook flip = one step)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def poly(pts, fill, sw=4, extra=""):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="{fill}" stroke="{P["ink"]}" stroke-width="{sw}" stroke-linejoin="round" '
            f'{extra}/>')


# ============================================================================ drawing helpers


def sky_svg():
    defs = S.lin_grad("s9sky", [(0, P["sky_day_top"]), (0.42, P["sky_day"]),
                                (0.62, S.mix(P["sky_day"], P["sky_warm"], 0.55)), (1, P["sky_warm"])])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s9sky)"/>', defs)


def clouds_svg(items):
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, "#fdf6e8", seed=seed, sw=3, shade_fill="#e9dccb")
    return doc(S.g(body, filter="wobble"))


def cloud_rim_svg(item, gx, gy, rx, ry, uid):
    """Soft gold light on the inner edge of a parting cloud, masked to the cloud's own (wobbled) silhouette."""
    cx, cy, w, h, seed = item
    sil = S.cloud(cx, cy, w, h, "#ffffff", seed=seed, sw=0)
    defs = (f'<mask id="s9rm{uid}" maskUnits="userSpaceOnUse" x="-50" y="-300" width="{SW}" height="900">'
            f'<g filter="url(#wobble)">{sil}</g></mask>'
            + S.rad_grad(f"s9rg{uid}", [(0, "#f6c25a", 0.85), (0.55, "#f0b040", 0.45), (1, "#f0b040", 0)]))
    body = (f'<g mask="url(#s9rm{uid})"><ellipse cx="{gx}" cy="{gy}" rx="{rx}" ry="{ry}" '
            f'fill="url(#s9rg{uid})"/></g>')
    return doc(body, defs)


def rays_svg(src, target, spread=28, n=5, length=1160, kind="add"):
    """A fan of thin, separated golden rays from src toward target, plus a warm glow on the target.

    Two passes with the same geometry: kind='mul' (multiply-blended pale gold) takes some blue out of the sky so
    the beams read warm, kind='add' (low-opacity deep gold) brightens them without clipping to white."""
    sx, sy = src
    a0 = math.degrees(math.atan2(target[1] - sy, target[0] - sx))
    if kind == "mul":
        stops = (("#ffd890", 0.42), ("#ffdc9c", 0.3), ("#ffe0a8", 0.1))
    else:
        stops = (("#f0a848", 0.2), ("#f0a040", 0.14), ("#f0a040", 0.05))
    defs = (f'<radialGradient id="s9ray" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="{length}">'
            f'<stop offset="0" stop-color="{stops[0][0]}" stop-opacity="{stops[0][1]}"/>'
            f'<stop offset="0.65" stop-color="{stops[1][0]}" stop-opacity="{stops[1][1]}"/>'
            f'<stop offset="1" stop-color="{stops[2][0]}" stop-opacity="{stops[2][1]}"/></radialGradient>'
            + S.rad_grad("s9glow", [(0, "#f6c25a", 0.34), (0.5, "#f0b040", 0.13), (1, "#f0b040", 0)]))
    d = ""
    rng = random.Random(4)
    for i in range(n):
        a = math.radians(a0 - spread / 2 + spread * i / (n - 1) + rng.uniform(-1.5, 1.5))
        wa = math.radians(rng.uniform(1.1, 1.9))
        r0, r1 = 40, length
        pts = [(sx + r0 * math.cos(a - wa / 4), sy + r0 * math.sin(a - wa / 4)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 4), sy + r0 * math.sin(a + wa / 4))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    tx, ty = target
    body = f'<path d="{d}" fill="url(#s9ray)" filter="url(#soft)"/>'
    if kind == "add":
        body += (f'<ellipse cx="{tx}" cy="{ty - 90}" rx="250" ry="290" fill="url(#s9glow)"/>'
                 f'<ellipse cx="{tx}" cy="{ty + 62}" rx="230" ry="46" fill="url(#s9glow)"/>')
    return doc(body, defs)


def river_band(top, bot):
    """Closed path from a top polyline (left->right) and a bottom polyline (left->right)."""
    d = S.smooth_path(top, closed=False, tension=0.9)
    b = list(reversed(bot))
    for x, y in b:
        d += f" L{f1(x)},{f1(y)}"
    return d + " Z"


def far_outside_svg():
    """Plain, hills and the far Tigris, left of the wall (clipped so it never covers the gate arch)."""
    defs = (S.lin_grad("s9plain", [(0, S.mix(P["sand_light"], P["sky_warm"], 0.5)), (0.45, P["sand_light"]),
                                   (1, P["sand"])]) +
            S.lin_grad("s9river", [(0, S.mix(P["sea_light"], P["sky_day"], 0.4)), (1, P["sea"])]) +
            f'<clipPath id="s9farclip"><rect x="-40" y="0" width="{WALL_X0 + 140}" height="{SH + 40}"/></clipPath>')
    hills = (S.path(S.hill(-80, 760, 690, 70, seed=3, bumps=2), fill=S.mix(P["stone"], P["sky_day"], 0.55), sw=2.5)
             + S.path(S.hill(500, 1500, 700, 55, seed=5, bumps=2), fill=S.mix(P["stone"], P["sky_day"], 0.45),
                      sw=2.5))
    plain = f'<path d="M-40,708 C300,700 700,712 1000,716 S1400,720 1500,722 L1500,{SH + 40} L-40,{SH + 40} Z" ' \
            f'fill="url(#s9plain)" stroke="{P["ink"]}" stroke-width="2.5"/>'
    top = [(-40, 742), (250, 748), (560, 758), (880, 770), (1150, 782), (1420, 790)]
    bot = [(-40, 772), (250, 782), (560, 800), (880, 818), (1150, 832), (1420, 842)]
    river = S.path(river_band(top, bot), fill="url(#s9river)", sw=3)
    hl = ""
    for x0, y0, ln in ((80, 760, 90), (330, 770, 120), (620, 784, 100), (860, 795, 80)):
        hl += (f'<path d="M{x0},{y0} q{ln / 2},-5 {ln},0" stroke="{P["foam"]}" stroke-width="4" fill="none" '
               f'stroke-linecap="round" opacity="0.75"/>')
    # far palms and bushes on the plain
    deco = ""
    for x, y, s, ln in ((90, 724, 0.32, -0.2), (170, 728, 0.28, 0.2), (760, 733, 0.3, 0.1)):
        deco += PR.palm_tree(x, y, s, lean=ln, dates=False)
    for x, y, s, v in ((420, 735, 0.35, 2), (640, 742, 0.3, 0)):
        deco += PR.bush(x, y, s, v)
    for x, y, s in ((250, 806, 0.45), (520, 820, 0.5), (980, 840, 0.45), (1320, 852, 0.42)):
        deco += PR.reeds(x, y, s)
    body = S.g(hills + plain, filter="wobble") + S.g(river + hl, filter="wobble") + deco
    return doc(f'<g clip-path="url(#s9farclip)">{body}</g>', defs)


def merlons(x0, x1, ytop, col, mw, gap, mh, sw=4, slope=0.0):
    """Stepped Assyrian crenellations evenly spread over x0..x1 (``slope`` lowers the base by px per px)."""
    out = ""
    n = max(1, int((x1 - x0 + gap) // (mw + gap)))
    step = (x1 - x0 - mw) / max(1, n - 1)
    s5 = mw / 5
    for i in range(n):
        a = x0 + i * step
        y = ytop + slope * (a - x0)
        pts = [(a, y), (a, y - mh * 0.4), (a + s5, y - mh * 0.4), (a + s5, y - mh * 0.75), (a + 2 * s5, y - mh * 0.75),
               (a + 2 * s5, y - mh), (a + 3 * s5, y - mh), (a + 3 * s5, y - mh * 0.75), (a + 4 * s5, y - mh * 0.75),
               (a + 4 * s5, y - mh * 0.4), (a + mw, y - mh * 0.4), (a + mw, y)]
        out += poly(pts, col, sw)
    return out


def rosette_band(x0, x1, yc, h):
    out = f'<rect x="{f1(x0)}" y="{f1(yc - h / 2)}" width="{f1(x1 - x0)}" height="{f1(h)}" fill="#4f86b0" ' \
          f'stroke="{P["ink"]}" stroke-width="3.5"/>'
    k = h / 26
    n = max(1, int((x1 - x0) // (34 * k)))
    for i in range(n):
        cx = x0 + (i + 0.5) * (x1 - x0) / n
        for j in range(6):
            a = j * math.pi / 3
            out += f'<circle cx="{f1(cx + 5 * k * math.cos(a))}" cy="{f1(yc + 5 * k * math.sin(a))}" ' \
                   f'r="{f1(3.6 * k)}" fill="#f4e3b0"/>'
        out += f'<circle cx="{f1(cx)}" cy="{f1(yc)}" r="{f1(3 * k)}" fill="{P["crown"]}"/>'
    return out


def corner_tower_svg():
    """Square corner tower closing the left end of the wall, with the side wall receding behind it."""
    k = _K
    col = P["sand"]
    dark = S.shade(col, -0.2)
    ink = P["ink"]
    x0, x1 = WALL_X0 - 50 * k, WALL_X0 + 70 * k
    top = WALL_Y - WALL_H - 100 * k
    out = ""
    # side wall going back (away from us) from the corner: lower, shaded, with sloping crenellations
    bx = x0 - 120
    back_top0, back_top1 = WALL_Y - WALL_H, WALL_Y - WALL_H + 40
    out += merlons(bx + 4, x0 - 4, back_top1 - 2, S.shade(col, -0.14), 26 * k, 10 * k, 24 * k, 3.5,
                   slope=(back_top0 - back_top1) / (x0 - bx))
    out += poly([(bx, WALL_Y - 26), (x0, WALL_Y), (x0, back_top0), (bx, back_top1)], S.shade(col, -0.14), 4)
    for i in range(1, 9):
        u = i / 9
        ya, yb = back_top1 + (WALL_Y - 26 - back_top1) * u, back_top0 + (WALL_Y - back_top0) * u
        out += f'<path d="M{f1(bx + 3)},{f1(ya)} L{f1(x0 - 3)},{f1(yb)}" stroke="{dark}" stroke-width="1.8" ' \
               f'opacity="0.35"/>'
    # the tower: shaded left face, front face, base band, brick courses, slit windows, rosette band, merlons
    out += merlons(x0 - 6 * k, x1 + 6 * k, top, col, 40 * k, 16 * k, 34 * k)
    out += poly([(x0, WALL_Y), (x0 - 16 * k, WALL_Y - 8 * k), (x0 - 16 * k, top - 8 * k), (x0, top)],
                S.shade(col, -0.18), 4)
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(x1 - x0)}" height="{f1(WALL_Y - top)}" ' \
           f'fill="{S.shade(col, 0.06)}" stroke="{ink}" stroke-width="4"/>'
    out += f'<rect x="{f1(x0 + 2)}" y="{f1(WALL_Y - 26 * k)}" width="{f1(x1 - x0 - 4)}" height="{f1(24 * k)}" ' \
           f'fill="{S.shade(col, -0.12)}"/>'
    yy = top + 26 * k
    while yy < WALL_Y - 20 * k:
        out += f'<path d="M{f1(x0 + 3)},{f1(yy)} L{f1(x1 - 3)},{f1(yy)}" stroke="{dark}" stroke-width="1.8" ' \
               f'opacity="0.35"/>'
        yy += 26 * k
    cx = (x0 + x1) / 2
    for wy in (top + 70 * k, top + 170 * k):
        out += f'<rect x="{f1(cx - 6 * k)}" y="{f1(wy)}" width="{f1(12 * k)}" height="{f1(34 * k)}" rx="{f1(6 * k)}" ' \
               f'fill="#4a3426" stroke="{ink}" stroke-width="3"/>'
    out += rosette_band(x0 + 6 * k, x1 - 6 * k, top + 22 * k, 22 * k)
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(x1 - x0)}" height="{f1(WALL_Y - top)}" fill="none" ' \
           f'stroke="{ink}" stroke-width="4"/>'
    return S.g(out, filter="wobble-fine")


def wall_svg():
    hole = (f"M{f1(GX - _R2)},{WALL_Y + 2} L{f1(GX - _R2)},{f1(_SPRING + 30 * _K)} "
            f"A{f1(_R2)},{f1(_R2)} 0 0 1 {f1(GX + _R2)},{f1(_SPRING + 30 * _K)} L{f1(GX + _R2)},{WALL_Y + 2} Z")
    defs = (f'<mask id="s9hole" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{SW + 100}" height="{SH + 100}">'
            f'<rect x="-50" y="-50" width="{SW + 100}" height="{SH + 100}" fill="#fff"/>'
            f'<path d="{hole}" fill="#000"/></mask>')
    wall = PR.city_wall(WALL_X0, WALL_X1, WALL_Y, WALL_H, gate=(GX, GWD), doors_open=1.0, seed=9)
    # long banners on the gate towers
    ban = ""
    for tx in (GX - GWD / 2 - 60 * _K, GX + GWD / 2 + 60 * _K):
        top = WALL_Y - WALL_H * 1.45 + 60 * _K
        ban += (f'<path d="M{tx - 34},{top} L{tx + 34},{top} L{tx + 34},{top + 230} L{tx},{top + 200} '
                f'L{tx - 34},{top + 230} Z" fill="{P["terracotta"]}" stroke="{P["ink"]}" stroke-width="4" '
                f'stroke-linejoin="round"/>'
                f'<circle cx="{tx}" cy="{top + 80}" r="18" fill="{P["gold"]}" stroke="{P["ink"]}" stroke-width="3"/>'
                f'<rect x="{tx - 40}" y="{top - 10}" width="80" height="12" rx="5" fill="{P["wood"]}" '
                f'stroke="{P["ink"]}" stroke-width="3"/>')
    rim = (f'<path d="{hole}" fill="none" stroke="{S.mix(P["glow"], P["sand_light"], 0.3)}" stroke-width="10" '
           f'opacity="0.8"/><path d="{hole}" fill="none" stroke="{P["ink"]}" stroke-width="4"/>')
    body = f'<g mask="url(#s9hole)">{wall}</g>' + corner_tower_svg() + S.g(rim + ban, filter="wobble-fine")
    return doc(body, defs)


def road_path():
    left = [(170, SH + 40), (470, 1080), (800, 990), (1150, 935), (1450, 905), (GX - 125, WALL_Y)]
    right = [(GX + 125, WALL_Y), (1560, 920), (1300, 975), (1040, 1050), (820, 1130), (720, SH + 40)]
    d = S.smooth_path(left, closed=False, tension=0.8)
    d += f" L{right[0][0]},{right[0][1]}"
    d += " " + S.smooth_path(right, closed=False, tension=0.8).replace("M", "L", 1)
    return d + " Z"


def outside_ground_svg():
    defs = (S.lin_grad("s9gr", [(0, P["sand"]), (1, S.mix(P["sand"], P["sand_dark"], 0.45))]) +
            S.lin_grad("s9road", [(0, S.mix(P["sand_light"], "#fffaf0", 0.2)), (1, P["sand_light"])]) +
            S.lin_grad("s9riv2", [(0, S.mix(P["sea_light"], P["sky_day"], 0.25)), (0.5, P["sea"]),
                                  (1, P["sea_deep"])]))
    ground = (f'<path d="M-40,{SH + 40} L-40,905 C300,898 700,892 1000,888 S1300,{WALL_Y - 4} 1500,{WALL_Y - 4} '
              f'L{SW + 40},{WALL_Y - 4} L{SW + 40},{SH + 40} Z" fill="url(#s9gr)" stroke="{P["ink"]}" '
              f'stroke-width="3"/>')
    road = S.path(road_path(), fill="url(#s9road)", sw=3)
    # road details: pebbles and wheel ruts
    rng = random.Random(11)
    peb = ""
    for _ in range(40):
        u = rng.random()
        x = 300 + u * 1350 + rng.uniform(-60, 60)
        y = 1100 - u * 210 + rng.uniform(-25, 25)
        r = rng.uniform(3, 8) * (1.2 - 0.5 * u)
        peb += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r)}" fill="{P["sand_dark"]}" ' \
               f'opacity="0.55"/>'
    # the Tigris on the right, flowing past the wall
    riv_top = [(2040, SH + 40), (2120, 1040), (2260, 972), (2600, 952), (3000, 946), (SW + 40, 944)]
    rd = S.smooth_path(riv_top, closed=False, tension=0.8) + f" L{SW + 40},{SH + 40} Z"
    river = S.path(rd, fill="url(#s9riv2)", sw=3.5)
    hl = ""
    for x0, y0, ln in ((2300, 990, 140), (2560, 1010, 180), (2900, 980, 160), (3100, 1040, 150), (2420, 1080, 200),
                       (2780, 1120, 170), (2200, 1130, 120), (3050, 1150, 180)):
        hl += (f'<path d="M{x0},{y0} q{ln / 2},-7 {ln},0" stroke="{P["foam"]}" stroke-width="5" fill="none" '
               f'stroke-linecap="round" opacity="0.7"/>')
    # houses outside the wall on the river bank
    houses = PR.house(2470, 918, 0.36, 0) + PR.house(2780, 914, 0.4, 3, facing=-1) + PR.house(3150, 918, 0.36, 2)
    # palms, bushes, reeds, rocks, grass
    deco = ""
    deco += PR.palm_tree(2290, 930, 0.62, lean=0.15) + PR.palm_tree(2620, 925, 0.55, lean=-0.2)
    deco += PR.palm_tree(3000, 925, 0.6, lean=0.1)
    for x, y, s in ((2150, 1000, 0.5), (2330, 968, 0.45), (2700, 950, 0.4), (3240, 948, 0.45), (2960, 948, 0.38)):
        deco += PR.reeds(x, y, s)
    for x, y, s, v in ((380, 968, 0.55, 2), (1200, 925, 0.5, 0), (1980, 905, 0.5, 1), (560, 1150, 0.7, 2)):
        deco += PR.bush(x, y, s, v)
    for x, y, s, v in ((260, 1040, 0.8, 1), (640, 1000, 0.7, 2), (900, 1150, 0.9, 0), (1500, 960, 0.6, 1),
                       (1060, 960, 0.6, 2), (1880, 940, 0.6, 1), (1640, 1010, 0.7, 2), (2010, 1000, 0.6, 1)):
        deco += PR.grass_tuft(x, y, s, v)
    rocks = ""
    for x, y, rx, ry, seed in ((1180, 1040, 46, 26, 1), (1240, 1052, 26, 16, 2), (430, 1120, 40, 22, 3),
                               (1900, 975, 34, 18, 4)):
        rocks += S.path(S.blob(x, y, rx, ry, 0.15, 8, seed), fill=P["stone_dark"], sw=3)
    body = (S.g(ground + road + peb + river + hl, filter="wobble") + houses + deco + S.g(rocks, filter="wobble-fine"))
    return doc(body, defs)


def river_glints_svg(phase, which):
    """Short shimmering highlight dashes on the far ('far') or near ('near') river; two phases twinkle in turn.
    Far glints stay on the visible stretch of the far river, well left of the wall and its corner tower."""
    rng = random.Random(30 + phase + (10 if which == "near" else 0))
    body = ""
    for _ in range(10 if which == "far" else 14):
        if which == "far":
            x = rng.uniform(0, WALL_X0 - 170)
            y = 752 + (x / 1300) * 40 + rng.uniform(0, 22)
            ln = rng.uniform(16, 34)
        else:
            x = rng.uniform(2220, SW - 40)
            y = rng.uniform(975, 1170)
            ln = rng.uniform(26, 60)
        body += (f'<path d="M{f1(x)},{f1(y)} l{f1(ln)},0" stroke="#fffaf0" stroke-width="{3 if y < 900 else 5}" '
                 f'stroke-linecap="round" opacity="0.85"/>')
    return doc(body)


def fg_palm_svg(x, y, s, lean, dates=True, extra=""):
    return doc(PR.palm_tree(x, y, s, lean=lean, dates=dates) + extra)


def boat_svg():
    x, y = 2760, 1060
    hull = (f'<path d="M{x - 120},{y - 30} Q{x - 100},{y + 18} {x},{y + 20} Q{x + 100},{y + 18} {x + 125},{y - 34} '
            f'Q{x},{y - 8} {x - 120},{y - 30} Z" fill="{P["wood"]}" stroke="{P["ink"]}" stroke-width="4" '
            f'stroke-linejoin="round"/>'
            f'<path d="M{x - 100},{y - 12} Q{x},{y + 6} {x + 104},{y - 14}" stroke="{P["wood_dark"]}" '
            f'stroke-width="3" fill="none"/>')
    man = C.citizen(x - 20, y - 14, 0.42, 1, kind="man", variant=3, pose="stand")
    pole = (f'<path d="M{x + 30},{y - 150} L{x + 70},{y + 40}" stroke="{P["wood_dark"]}" stroke-width="6" '
            f'stroke-linecap="round"/>')
    water = (f'<path d="M{x - 150},{y + 16} q30,-8 60,0 M{x + 80},{y + 14} q30,-8 60,0" stroke="{P["foam"]}" '
             f'stroke-width="4" fill="none" stroke-linecap="round"/>')
    return doc(man + S.g(pole + hull, filter="wobble-fine") + water)


# ---------------------------------------------------------------------------- inside the city


def stall(cx, gy, w=230, s=1.0, stripe=None, goods="fruit", seed=0):
    """A market stall: two posts, a striped scalloped awning, a cloth-covered table with goods."""
    stripe = stripe or P["terracotta"]
    ink = P["ink"]
    hw = w / 2
    top, front = gy - 250 * s, gy - 190 * s
    out = ""
    for px in (cx - hw, cx + hw):
        out += (f'<rect x="{f1(px - 6 * s)}" y="{f1(top)}" width="{f1(12 * s)}" height="{f1(gy - top)}" rx="3" '
                f'fill="{P["wood"]}" stroke="{ink}" stroke-width="3"/>')
    # table
    ty = gy - 92 * s
    out += (f'<rect x="{f1(cx - hw + 4)}" y="{f1(ty)}" width="{f1(w - 8)}" height="{f1(16 * s)}" rx="4" '
            f'fill="{P["wood_light"]}" stroke="{ink}" stroke-width="3"/>'
            f'<path d="M{f1(cx - hw + 8)},{f1(ty + 16 * s)} L{f1(cx + hw - 8)},{f1(ty + 16 * s)} '
            f'L{f1(cx + hw - 14)},{f1(gy - 8)} L{f1(cx - hw + 14)},{f1(gy - 8)} Z" fill="{P["headcloth"]}" '
            f'stroke="{ink}" stroke-width="3"/>'
            f'<path d="M{f1(cx - hw + 10)},{f1(ty + 40 * s)} L{f1(cx + hw - 10)},{f1(ty + 40 * s)}" '
            f'stroke="{stripe}" stroke-width="{f1(7 * s)}"/>')
    # goods on the table
    g = ""
    if goods == "fruit":
        for i, (fc, n) in enumerate(((P["terracotta"], 5), ("#e9a23b", 5), (P["leaf"], 3))):
            bx = cx - hw + 45 * s + i * (w - 90 * s) / 2
            g += (f'<path d="M{f1(bx - 36 * s)},{f1(ty - 22 * s)} Q{f1(bx)},{f1(ty + 12 * s)} {f1(bx + 36 * s)},'
                  f'{f1(ty - 22 * s)} Z" fill="{P["wood_light"]}" stroke="{ink}" stroke-width="3"/>')
            for j in range(n):
                fx = bx + (j - (n - 1) / 2) * 13 * s
                fy = ty - 26 * s - (8 * s if 0 < j < n - 1 else 0)
                g += f'<circle cx="{f1(fx)}" cy="{f1(fy)}" r="{f1(11 * s)}" fill="{fc}" stroke="{ink}" stroke-width="2.5"/>'
    elif goods == "pots":
        for i in range(3):
            bx = cx - hw + 40 * s + i * (w - 80 * s) / 2
            col = (P["terracotta"], S.mix(P["terracotta"], P["sand"], 0.4), P["jonah_sash"])[i]
            g += (f'<path d="M{f1(bx - 22 * s)},{f1(ty)} Q{f1(bx - 34 * s)},{f1(ty - 40 * s)} {f1(bx - 12 * s)},'
                  f'{f1(ty - 58 * s)} L{f1(bx + 12 * s)},{f1(ty - 58 * s)} Q{f1(bx + 34 * s)},{f1(ty - 40 * s)} '
                  f'{f1(bx + 22 * s)},{f1(ty)} Z" fill="{col}" stroke="{ink}" stroke-width="3"/>'
                  f'<rect x="{f1(bx - 14 * s)}" y="{f1(ty - 66 * s)}" width="{f1(28 * s)}" height="{f1(10 * s)}" '
                  f'rx="3" fill="{S.shade(col, 0.2)}" stroke="{ink}" stroke-width="2.5"/>')
    else:  # cloth rolls
        for i, col in enumerate((P["royal_light"], P["jonah_sash"], P["gold"], P["terracotta"])):
            bx = cx - hw + 34 * s + i * (w - 68 * s) / 3
            g += (f'<rect x="{f1(bx - 20 * s)}" y="{f1(ty - 34 * s)}" width="{f1(40 * s)}" height="{f1(34 * s)}" '
                  f'rx="{f1(14 * s)}" fill="{col}" stroke="{ink}" stroke-width="3"/>'
                  f'<path d="M{f1(bx - 10 * s)},{f1(ty - 30 * s)} L{f1(bx - 10 * s)},{f1(ty - 4 * s)}" '
                  f'stroke="{S.shade(col, -0.3)}" stroke-width="2"/>')
    out += g
    # awning
    aw = (f'M{f1(cx - hw - 18 * s)},{f1(top)} L{f1(cx + hw + 18 * s)},{f1(top)} '
          f'L{f1(cx + hw + 34 * s)},{f1(front)} L{f1(cx - hw - 34 * s)},{f1(front)} Z')
    out += f'<path d="{aw}" fill="{P["sail"]}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>'
    n = 6
    x0, x1 = cx - hw - 34 * s, cx + hw + 34 * s
    t0, t1 = cx - hw - 18 * s, cx + hw + 18 * s
    for i in range(0, n, 2):
        a, b = i / n, (i + 1) / n
        out += (f'<path d="M{f1(t0 + (t1 - t0) * a)},{f1(top)} L{f1(t0 + (t1 - t0) * b)},{f1(top)} '
                f'L{f1(x0 + (x1 - x0) * b)},{f1(front)} L{f1(x0 + (x1 - x0) * a)},{f1(front)} Z" fill="{stripe}"/>')
    # scallops
    sc_ = ""
    for i in range(n):
        a, b = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
        col = stripe if i % 2 == 0 else P["sail"]
        sc_ += (f'<path d="M{f1(a)},{f1(front)} Q{f1((a + b) / 2)},{f1(front + 30 * s)} {f1(b)},{f1(front)} Z" '
                f'fill="{col}" stroke="{ink}" stroke-width="3"/>')
    out += f'<path d="{aw}" fill="none" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>' + sc_
    # ground goods
    out += PR.sack(cx + hw - 20 * s, gy, 0.42 * s, seed=seed) + PR.jar(cx - hw + 10 * s, gy - 34 * s, 0.4 * s)
    return S.g(out, filter="wobble-fine")


def inside_far_body():
    """The city mound seen past the market: hazy rooftops and towers, palms, the skyline's own small hazy ziggurat
    (left of the gate), the big ziggurat (right of the gate tower, seen above the outer wall from outside) and a
    house closing the left end of the back row."""
    body = PR.nineveh_skyline(SKY_X0, SW + 40, 700, scale=1.25, seed=SKY_SEED, haze=0.42)
    body += PR.ziggurat(ZIG_X, 742, ZIG_S)
    for x, y, s, ln in ((1330, 790, 0.82, 0.15), (2020, 790, 0.9, -0.1), (2920, 795, 0.85, 0.2),
                        (3220, 800, 0.8, -0.2), (1000, 770, 0.7, 0.1)):
        body += PR.palm_tree(x, y, s, lean=ln, dates=True)
    body += PR.house(1060, BACK_Y - 30, 0.48, 2, facing=-1)
    return body


def inside_far_svg():
    """Static part: only right of the wall's left end, so nothing of the city shows beside the wall outside."""
    defs = f'<clipPath id="s9infar"><rect x="{WALL_X0}" y="-50" width="{SW}" height="{SH + 100}"/></clipPath>'
    return doc(f'<g clip-path="url(#s9infar)">{inside_far_body()}</g>', defs)


def inside_far_left_svg():
    """The same painting left of the wall's end, feathered out to the right so it blends into the static part
    (a hard clip edge would get watercolour edge pooling). Shown only once we are inside the walls."""
    defs = (f'<linearGradient id="s9lmg" gradientUnits="userSpaceOnUse" x1="{WALL_X0 + 20}" y1="0" '
            f'x2="{WALL_X0 + 190}" y2="0"><stop offset="0" stop-color="#ffffff"/>'
            f'<stop offset="1" stop-color="#000000"/></linearGradient>'
            + f'<mask id="s9lm" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{WALL_X0 + 300}" '
              f'height="{SH + 100}"><rect x="-50" y="-50" width="{WALL_X0 + 300}" height="{SH + 100}" '
              f'fill="url(#s9lmg)"/></mask>')
    return doc(f'<g mask="url(#s9lm)">{inside_far_body()}</g>', defs)


def inside_mid_svg():
    """Plaza floor, the back row of flat-roofed houses and the market stalls."""
    defs = S.lin_grad("s9plaza", [(0, S.mix(P["sand_light"], P["stone_light"], 0.5)), (0.4, P["sand_light"]),
                                  (1, S.mix(P["sand"], P["sand_light"], 0.3))])
    floor = (f'<rect x="{WALL_X0 - 220}" y="{BACK_Y - 30}" width="{SW}" height="{SH}" fill="url(#s9plaza)" '
             f'stroke="{P["ink"]}" stroke-width="3"/>')
    # paving: soft brick courses in perspective
    pav = ""
    for i, yy in enumerate((812, 838, 868, 904, 946, 994, 1048, 1110)):
        pav += (f'<path d="M{WALL_X0 - 220},{yy} L{SW + 20},{yy}" stroke="{P["sand_dark"]}" stroke-width="2" '
                f'opacity="{0.25 + i * 0.03:.2f}"/>')
    rng = random.Random(7)
    for _ in range(96):
        yy = rng.choice((812, 838, 868, 904, 946, 994, 1048))
        x = rng.uniform(WALL_X0 - 200, SW)
        h = {812: 26, 838: 30, 868: 36, 904: 42, 946: 48, 994: 54, 1048: 62}[yy]
        pav += (f'<path d="M{f1(x)},{yy} l{f1(rng.uniform(-6, 6))},{h}" stroke="{P["sand_dark"]}" stroke-width="2" '
                f'opacity="0.3"/>')
    houses = (PR.house(1300, BACK_Y, 0.52, 0) + PR.house(1640, BACK_Y, 0.5, 1) + PR.house(2170, BACK_Y, 0.54, 2)
              + PR.house(2760, BACK_Y, 0.55, 3) + PR.house(3170, BACK_Y, 0.5, 1, facing=-1))
    doves = (PR.dove(1215, BACK_Y - 0.52 * 510 - 20, 0.45, 1, pose="stand")
             + PR.dove(2080, BACK_Y - 0.54 * 524 - 20, 0.45, -1, pose="stand")
             + PR.dove(2120, BACK_Y - 0.54 * 524 - 20, 0.42, 1, pose="stand"))
    stalls = (stall(1260, 856, 240, 0.95, P["jonah_sash"], "pots", 1) + stall(2480, 852, 250, 0.95, P["terracotta"],
                                                                                 "fruit", 2)
              + stall(3000, 858, 230, 0.95, P["royal_light"], "cloth", 3))
    extra = PR.animal(3170, 880, 0.55, -1, kind="camel") + PR.jar(2330, 846, 0.42) + PR.jar(2368, 852, 0.36)
    body = S.g(floor + pav, filter="wobble") + houses + doves + stalls + extra
    return doc(body, defs)


def step_svg():
    """A two-tier stone step in the square with a glazed blue rosette band (Jonah preaches from it)."""
    x, y = STEP_X, STEP_Y
    ink = P["ink"]
    st, stl, std = P["stone"], P["stone_light"], P["stone_dark"]
    out = ""
    # lower tier
    out += (f'<path d="M{x - 190},{y - 34} L{x + 190},{y - 34} L{x + 214},{y - 50} L{x - 166},{y - 50} Z" '
            f'fill="{stl}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{x - 190}" y="{y - 34}" width="380" height="34" fill="{st}" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M{x + 190},{y} L{x + 214},{y - 16} L{x + 214},{y - 50} L{x + 190},{y - 34} Z" fill="{std}" '
            f'stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>')
    # upper tier
    y2 = y - 34
    out += (f'<path d="M{x - 130},{y2 - 28} L{x + 130},{y2 - 28} L{x + 150},{y2 - 42} L{x - 110},{y2 - 42} Z" '
            f'fill="{stl}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{x - 130}" y="{y2 - 28}" width="260" height="28" fill="{st}" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M{x + 130},{y2} L{x + 150},{y2 - 14} L{x + 150},{y2 - 42} L{x + 130},{y2 - 28} Z" '
            f'fill="{std}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>')
    band = f'<rect x="{x - 186}" y="{y - 24}" width="372" height="16" fill="#4f86b0" stroke="{ink}" stroke-width="2.5"/>'
    for i in range(11):
        cx = x - 170 + i * 34
        band += f'<circle cx="{cx}" cy="{y - 16}" r="5" fill="#f4e3b0"/><circle cx="{cx}" cy="{y - 16}" r="2" ' \
                f'fill="{P["crown"]}"/>'
    shadow = f'<ellipse cx="{x + 20}" cy="{y + 4}" rx="230" ry="16" fill="{ink}" opacity="0.18" filter="url(#soft)"/>'
    return doc(shadow + S.g(out + band, filter="wobble-fine"))


# ---------------------------------------------------------------------------- marks


def exclaim_svg(x, y, s=1.0):
    ink = P["ink"]
    pts = []
    for i in range(16):
        r = (40 if i % 2 == 0 else 29) * s
        a = math.radians(i * 22.5)
        pts.append((x + 3 * s + r * math.cos(a), y - 14 * s + r * 1.12 * math.sin(a)))
    burst = ('<path d="M' + " L".join(f"{f1(px)},{f1(py)}" for px, py in pts) + f' Z" fill="#fff6dc" '
             f'stroke="{ink}" stroke-width="{3.5 * s}" stroke-linejoin="round"/>')
    body = burst + (f'<path d="M{x},{y - 40 * s} L{x + 3 * s},{y - 4 * s}" stroke="{ink}" stroke-width="{9 * s}" '
            f'stroke-linecap="round"/>'
            f'<circle cx="{x + 5 * s}" cy="{y + 12 * s}" r="{5.5 * s}" fill="{ink}"/>')
    return doc(S.g(body, filter="wobble-fine"))


def arcs_svg(cx, cy, n, facing=1):
    body = ""
    for i in range(n):
        r = 44 + i * 30
        a0, a1 = math.radians(-38), math.radians(38)
        x0, y0 = cx + facing * r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + facing * r * math.cos(a1), cy + r * math.sin(a1)
        sweep = 1 if facing > 0 else 0
        body += (f'<path d="M{f1(x0)},{f1(y0)} A{r},{r} 0 0 {sweep} {f1(x1)},{f1(y1)}" fill="none" '
                 f'stroke="{P["ink"]}" stroke-width="7" stroke-linecap="round" opacity="{0.95 - i * 0.12:.2f}"/>')
    return doc(S.g(body, filter="wobble-fine"))


# ============================================================================ motion helpers


def fly(local=None, pivot=None, g=None, s_fn=None, a_fn=None):
    """Compose a layer's own motion (about ``pivot``) with the fly-through scale s_fn(t) about g and alpha a_fn(t)."""
    gx, gy = g

    def m(t):
        lt = local(t) if local else Tf()
        px = lt.px if lt.px is not None else pivot[0]
        py = lt.py if lt.py is not None else pivot[1]
        s = s_fn(t)
        return Tf(dx=(s - 1) * (px - gx) + s * lt.dx, dy=(s - 1) * (py - gy) + s * lt.dy, rot=lt.rot,
                  sx=s * lt.sx, sy=s * lt.sy, alpha=lt.alpha * a_fn(t), px=px, py=py)
    return m


def sched(entries):
    """Flipbook index from a schedule [(t, value), ...]. value: a frame index or ('alt', a, b, period), which
    alternates frames a and b every ``period`` s counted from the entry's time."""
    entries = sorted(entries, key=lambda e: e[0])

    def f(t):
        cur, t0 = entries[0][1], entries[0][0]
        for ts, v in entries:
            if t >= ts:
                cur, t0 = v, ts
        if isinstance(cur, tuple):
            _, a, b, per = cur
            return float((a, b)[int(max(0.0, t - t0) / per) % 2])
        return float(cur)
    return f


def fly_pivot_x(cam):
    """Fly-through centre x inside the clear opening that makes both of its sides reach the two frame edges of
    ``cam`` at the same scale (so the opening fills the frame as early as possible)."""
    a, b = HOLE_CLEAR[0], HOLE_CLEAR[1]
    c, d = cam.x - cam.w / 2, cam.x + cam.w / 2
    return (a * d - c * b) / (d + a - b - c)


def opening_covers(cam, s, piv):
    """True when the clear gate opening, scaled by s about piv, covers the whole camera viewport."""
    hx0, hx1, hspring, hbot = HOLE_CLEAR
    px, py = piv
    vx0, vx1 = cam.x - cam.w / 2, cam.x + cam.w / 2
    vy0, vy1 = cam.y - cam.w * 9 / 32, cam.y + cam.w * 9 / 32
    X0, X1 = px + s * (hx0 - px), px + s * (hx1 - px)
    Ys, Yb = py + s * (hspring - py), py + s * (hbot - py)
    return X0 <= vx0 - 4 and X1 >= vx1 + 4 and Ys <= vy0 - 4 and Yb >= vy1 + 4


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.line(0), ctx.line(1), ctx.line(2)
    d0, d1, d2 = L0.end - L0.start, L1.end - L1.start, L2.end - L2.start

    # ---- key times (all derived from the narration) ----
    t_call = L0.start                          # God calls: clouds part, rays
    t_look = L0.start + 0.35                   # Jonah looks up and listens
    t_nod = L0.start + 0.75 * d0               # "他听话了": he nods
    t_up = t_nod + 0.38
    t_walk = t_nod + 0.55                      # sets off
    t_gate = L1.start + 0.43 * d1              # reaches the gate
    t_fly0, t_fly1 = t_gate + 0.05, t_gate + 0.8    # fly through the arch
    t_show = t_fly0 + 0.1                      # front crowd starts being drawn (still hidden by the wall)
    t_climb = L1.start + 0.70 * d1             # out of the passage, on the step
    t_on = t_climb + 0.3                       # at his spot on the step
    t_preach = t_on + 0.05                     # "大声呼喊": arm up (mouth still closed until he speaks)
    t_turn = L1.end + 0.05                     # people stop and turn
    t_wow = L2.start + 0.3                     # surprised hop + "!"
    t_phr2 = L2.start + 0.46 * d2              # "尼尼微就要倾覆了"
    t_worry = t_phr2 + 0.5

    # ---- camera: a gentle push during line 0, one sine pan right over the panorama, one push-in through the
    #      gate onto the market framing, then only a slow push-in to the end (no reversals) ----
    t_pan1 = t_gate - 0.35
    t_mkt = t_fly0 + 0.5
    CAM_MKT = Cam(1940, 628, 1700)
    camf = M.cam_keys([
        (0, Cam(960, 600, 1720)),
        (t_up, Cam(985, 604, 1720)),
        (t_pan1, Cam(1940, 596, 1980)),
        (t_mkt, CAM_MKT),
        (T, Cam(1975, 626, 1520)),
    ], "sine")
    sc.camera = camf
    cam_x0 = camf(t_up).x

    def par(k):
        """Camera-linked horizontal parallax: k > 0 for far things (they lag), k < 0 for near ones."""
        return lambda t: Tf(dx=k * (camf(t).x - cam_x0))

    # ---- fly-through: outside layers scale about FLY_C; once the clear opening covers the frame they are dropped
    FLY_C = (fly_pivot_x(CAM_MKT), GATE_C[1])
    part = M.progress
    s_fly = lambda t: 1 + 19.0 * part(t, t_fly0, t_fly1, "in")
    s_far = lambda t: 1 + 2.0 * part(t, t_fly0, t_fly1, "in")
    t_cut = t_fly1
    k = 0
    while t_fly0 + k / 120 < t_fly1:
        tt = t_fly0 + k / 120
        if opening_covers(camf(tt), s_fly(tt), FLY_C):
            t_cut = tt
            break
        k += 1
    a_fly = lambda t: 1.0 if t < t_cut else 0.0
    # the inside's left end is revealed while the scaled-up wall still covers that part of the frame
    t_left = t_fly0 + (t_fly1 - t_fly0) * (3.0 / 19.0) ** (1 / 3)      # s_fly == 4

    def F(local=None, pivot=FLY_C, s_fn=s_fly):
        return fly(local, pivot, FLY_C, s_fn, a_fly)

    # ---- sky and clouds (shared by outside and inside; behind the city skyline) ----
    sc.add("sky", sky_svg(), z=0, wc=0.6)
    sc.add("clouds", clouds_svg([(1330, 100, 400, 115, 3), (2260, 50, 340, 95, 5), (3090, 120, 380, 110, 7),
                                 (1240, 236, 250, 76, 9)]), z=1.0,
           motion=M.combine(M.drift(vx=7), par(0.35)))
    CL = (520, 150, 440, 135, 21)
    CR = (1010, 120, 400, 125, 22)
    cl_m = M.combine(lambda t: Tf(dx=-150 * part(t, t_call - 0.3, t_call + 1.4, "inout") + 4 * t), par(0.35))
    cr_m = M.combine(lambda t: Tf(dx=170 * part(t, t_call - 0.3, t_call + 1.4, "inout") + 4 * t), par(0.35))
    sc.add("cloud_l", clouds_svg([CL]), z=1.1, motion=cl_m)
    sc.add("cloud_r", clouds_svg([CR]), z=1.2, motion=cr_m)
    ray_a = M.keys([(0, {"alpha": 0.25}), (t_call - 0.1, {"alpha": 0.3}), (t_call + 0.9, {"alpha": 1.0}),
                    (t_walk + 0.2, {"alpha": 0.9}), (t_walk + 1.1, {"alpha": 0.0})], "sine")
    sc.add("rim_l", cloud_rim_svg(CL, 742, 150, 150, 110, "l"), z=1.15, wc=0, motion=M.combine(cl_m, ray_a))
    sc.add("rim_r", cloud_rim_svg(CR, 805, 130, 140, 100, "r"), z=1.25, wc=0, motion=M.combine(cr_m, ray_a))

    # ---- inside the city (behind the outside layers) ----
    sc.add("in_far", inside_far_svg(), z=2, wc=0.9)
    sc.add("in_far_left", inside_far_left_svg(), z=2.05, wc=0.9,
           motion=lambda t: Tf(alpha=1.0 if t >= t_left else 0.0))
    sc.add("in_mid", inside_mid_svg(), z=3)

    # townspeople: one flipbook layer each, anchored at the spot where they end up
    def person(name, kind, variant, x, y, s, face, z, walk=None, period=0.4, idle=None, turn=None, late=None,
               hop=True, vis=None):
        """walk=(x_from, t_a, t_b): walk from x_from to x during [t_a, t_b], one walk_a/walk_b flip per ``period``
        (travel per flip ~ 100-120 px * s so the feet don't slide), then wait. idle=(pose, expr, period):
        alternate stand / pose while waiting. turn=(t, facing, expr): stop and turn. late=(t, pose, expr)."""
        shw = C.ground_shadow(x, y, s, 80 if kind == "child" else 100)
        frames, entries = [], []

        def add(**kw):
            frames.append(doc(shw + C.citizen(x, y, s, kind=kind, variant=variant, **kw)))
            return len(frames) - 1
        wait = add(facing=face, pose="stand")
        if idle:
            wait = ("alt", wait, add(facing=face, pose=idle[0], expr=idle[1]), idle[2])
        if walk:
            wa, wb = add(facing=face, pose="walk_a"), add(facing=face, pose="walk_b")
            entries += [(0, ("alt", wa, wb, period)), (walk[2], wait)]
        else:
            entries.append((0, wait))
        end_face = face
        if turn:
            entries.append((turn[0], add(facing=turn[1], pose="stand", expr=turn[2])))
            end_face = turn[1]
        if late:
            entries.append((late[0], add(facing=end_face, pose=late[1], expr=late[2])))
        parts = [M.breathe(0.012, 3.0 + variant * 0.3, pivot=(x, y), phase=variant * 0.17)]
        if walk:
            parts.append(M.keys([(walk[1], {"dx": walk[0] - x}), (walk[2], {"dx": 0})], "linear"))
        if hop:
            parts.append(M.keys([(t_wow - 0.01, {"dy": 0}), (t_wow + 0.13, {"dy": -16 * s}),
                                 (t_wow + 0.33, {"dy": 0})], ["out", "in"]))
        if vis is not None:     # hidden behind the outer wall until then: skip drawing it
            parts.append(lambda t: Tf(alpha=1.0 if t >= vis else 0.0))
        sc.add(name, frames, z=z, frame_at=sched(entries), motion=M.combine(*parts))
        return C.body_points(C.citizen, x, y, s, end_face, kind=kind, variant=variant, pose="stand")["head_top"]

    # back row (seen through the gate arch from outside): two strollers at a natural pace (~70 px per flip at
    # scale 0.6) who end up right of the step, clear of the front heads and their "!" marks; a boy at the fruit stall
    person("back_m1", "man", 1, 2080, BACK_Y + 26, 0.58, 1, 5.0, walk=(1480, 0.3, 3.9), period=0.4,
           turn=(t_turn, -1, "surprised"), hop=False)
    person("back_w1", "woman", 3, 2200, BACK_Y + 40, 0.6, 1, 5.1, walk=(1500, 2.0, 5.7), period=0.38,
           turn=(t_turn + 0.1, -1, "surprised"), hop=False)
    person("back_c1", "child", 0, 2330, BACK_Y + 52, 0.62, 1, 5.2, turn=(t_turn + 0.05, -1, "surprised"), hop=False)

    sc.add("step", step_svg(), z=6)

    # ---- outside: the plain, the wall with the gate, the road (fly-through) ----
    sc.add("out_far", far_outside_svg(), z=10, motion=F(s_fn=s_far))
    sc.add("out_wall", wall_svg(), z=12, motion=F())
    sc.add("out_ground", outside_ground_svg(), z=13, motion=F())
    for which in ("far", "near"):
        for ph in (0, 1):
            tw = (lambda ph_: lambda t: Tf(alpha=0.5 + 0.5 * math.sin(t * 2.6 + math.pi * ph_)))(ph)
            sc.add(f"glint_{which}{ph}", river_glints_svg(ph, which),
                   z=(10.5 if which == "far" else 14) + ph * 0.1, wc=0,
                   motion=F(local=tw, pivot=FLY_C, s_fn=s_far if which == "far" else s_fly))
    sc.add("boat", boat_svg(), z=14.5, motion=F(local=M.combine(M.bob(5, 2.8), M.sway(1.2, 3.4, (2760, 1060))),
                                                pivot=(2760, 1060)))
    # swaying palms near the road (the big foreground one gets a little extra parallax)
    for i, (x, y, s, ln, z) in enumerate(((140, 1180, 1.35, 0.3, 16), (1105, 935, 0.92, 0.05, 15.2),
                                          (600, 905, 0.78, -0.15, 15.1), (2120, 935, 0.8, -0.1, 15.3))):
        sw = M.sway(0.9 if s > 1 else 0.7, 4.2 + i * 0.5, (x, y), phase=i * 0.23)
        if i == 0:
            sw = M.combine(sw, par(-0.15))
        sc.add(f"palm{i}", fg_palm_svg(x, y, s, ln), z=z, motion=F(local=sw, pivot=(x, y)))

    # golden rays on Jonah while God calls (they drift with the clouds they come from)
    JX, JY = 980, 960
    ray_m = M.combine(M.sway(1.0, 5.0, (760, -160)), ray_a, par(0.35))
    sc.add("rays_mul", rays_svg((760, -160), (JX, JY - 60), kind="mul"), z=17.9, wc=0, blend="multiply",
           motion=ray_m)
    sc.add("rays", rays_svg((760, -160), (JX, JY - 60), kind="add"), z=18, wc=0, blend="add", motion=ray_m)

    # ---- Jonah ----
    poses = [("stand", None), ("listen", None), ("confess", "peaceful"), ("stand", "happy"), ("walk_a", None),
             ("walk_b", None), ("preach", "worried"), ("preach", "call"), ("preach", "shout")]
    jframes = [doc(C.ground_shadow(JX, JY, JONAH_S, 120) + C.jonah(JX, JY, JONAH_S, 1, pose=p, expr=e))
               for p, e in poses]
    j_sched = sched([(0, 0), (t_look, 1), (t_nod, 2), (t_up, 3), (t_walk, ("alt", 4, 5, STEP)),
                     (t_fly0 + 0.35, ("alt", 4, 5, 0.34)), (t_on - 0.04, 0), (t_preach, 6),
                     (L2.start, ("alt", 7, 8, 0.19)), (L2.start + 0.37 * d2, 7), (t_phr2, ("alt", 8, 7, 0.19)),
                     (L2.end - 0.05, 6)])

    # path: road -> gate (small under the towering gate) -> through the passage at step-top level -> along the
    # step to his spot. He never drops below STEP_TOP while over the step; he grows back to hero size while the
    # wall flies past (the camera is moving forward).
    def P_(t, x, y, s):
        return (t, {"dx": x - JX, "dy": y - JY, "s": s / JONAH_S})
    j_keys = M.keys([P_(0, JX, JY, 0.95), P_(t_walk, JX, JY, 0.95), P_(t_gate - 0.1, GX - 20, WALL_Y + 6, 0.64),
                     P_(t_fly0 + 0.35, GX + 6, STEP_TOP, 0.6), P_(t_climb, STEP_X - 70, STEP_TOP, 0.86),
                     P_(t_on, STEP_X - 10, STEP_TOP, 0.88), P_(T, STEP_X - 10, STEP_TOP, 0.88)],
                    ["linear", "linear", "linear", "sine", "out", "linear"], pivot=(JX, JY))
    nod = M.keys([(t_nod - 0.01, {"dy": 0}), (t_nod + 0.12, {"dy": 7}), (t_up, {"dy": 0})], "sine")
    emph = M.keys([(t_preach, {"dy": 0}), (t_preach + 0.12, {"dy": -6}), (t_preach + 0.3, {"dy": 0}),
                   (L2.start - 0.01, {"dy": 0}), (L2.start + 0.12, {"dy": -8}), (L2.start + 0.3, {"dy": 0}),
                   (t_phr2 - 0.01, {"dy": 0}), (t_phr2 + 0.12, {"dy": -8}), (t_phr2 + 0.3, {"dy": 0})], "sine")
    sc.add("jonah", jframes, z=20, frame_at=j_sched,
           motion=M.combine(j_keys, nod, emph, M.breathe(0.01, 3.2, pivot=(JX, JY))))

    # sound arcs only while he actually speaks (line 2)
    hp = C.body_points(C.jonah, STEP_X - 10, STEP_TOP, 0.88, 1, pose="preach")["head"]
    mx, my = hp[0] + 48, hp[1] + 18
    arc_on = lambda t: part(t, L2.start, L2.start + 0.2) * (1 - part(t, L2.end - 0.1, L2.end + 0.3))
    sc.add("arcs", [arcs_svg(mx, my, 1), arcs_svg(mx, my, 2), arcs_svg(mx, my, 3)], z=21, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=lambda t: Tf(alpha=arc_on(t)))

    # ---- inside crowd in front (revealed as we pass through the gate) ----
    heads = {}
    # left group: a man with his donkey chatting with a friend; a woman strolls in from the left and points
    heads["cr_man1"] = person("cr_man1", "man", 0, 1435, 992, 0.84, 1, 7.0,
                              turn=(t_turn + 0.1, 1, "surprised"), vis=t_show)
    heads["cr_man0"] = person("cr_man0", "man", 3, 1528, 962, 0.84, -1, 6.95, idle=("listen", "neutral", 0.9),
                              turn=(t_turn, 1, "surprised"), late=(t_worry + 0.1, "listen", None), vis=t_show)
    heads["cr_woman2"] = person("cr_woman2", "woman", 2, 1612, 1014, 0.86, 1, 7.4,
                                walk=(1260, t_show, t_turn - 0.3), period=0.36,
                                turn=(t_turn, 1, "surprised"), late=(t_wow + 0.6, "point", "surprised"), vis=t_show)
    # right group: a mother and her girl walk in from the right (the girl points), an elder and a man at the stalls
    heads["cr_child1"] = person("cr_child1", "child", 1, 2280, 1012, 0.84, -1, 7.5,
                                walk=(2560, t_show + 0.15, t_turn - 0.15), period=0.26,
                                turn=(t_turn, -1, "surprised"), late=(t_wow + 0.5, "point", "surprised"), vis=t_show)
    heads["cr_woman1"] = person("cr_woman1", "woman", 1, 2425, 990, 0.84, -1, 7.3,
                                walk=(2725, t_show, t_turn - 0.1), period=0.44,
                                turn=(t_turn, -1, "surprised"), late=(t_worry, "listen", None), vis=t_show)
    heads["cr_elder0"] = person("cr_elder0", "elder", 0, 2585, 974, 0.84, 1, 7.2,
                                turn=(t_turn + 0.15, -1, "surprised"), late=(t_worry + 0.25, "listen", None),
                                vis=t_show)
    heads["cr_man3"] = person("cr_man3", "man", 3, 2690, 1034, 0.9, 1, 7.6,
                              turn=(t_turn + 0.1, -1, "surprised"), late=(t_phr2 + 0.2, "listen", None), vis=t_show)
    # animals in the square
    sc.add("donkey", doc(C.ground_shadow(1270, 984, 0.78, 200) + PR.animal(1270, 984, 0.78, 1, kind="donkey")),
           z=6.9, motion=M.combine(M.sway(0.6, 3.1, (1270, 984)), lambda t: Tf(alpha=float(t >= t_show))))
    an = doc(C.ground_shadow(2590, 1060, 0.75, 180) + PR.animal(2590, 1060, 0.75, -1, kind="sheep")
             + C.ground_shadow(2730, 1072, 0.62, 150) + PR.animal(2730, 1072, 0.62, -1, kind="sheep"))
    sc.add("sheep", an, z=7.8, motion=M.combine(M.bob(2, 2.6), lambda t: Tf(alpha=float(t >= t_show))))

    # "!" marks right above the surprised heads
    for i, nm in enumerate(("cr_man0", "cr_woman2", "cr_woman1", "cr_elder0")):
        hx, hy = heads[nm]
        x, y = hx + 2, hy - 50
        sc.add(f"wow{i}", exclaim_svg(x, y, 0.9), z=30 + i, wc=0,
               motion=M.keys([(t_wow - 0.05 + i * 0.08, {"alpha": 0, "s": 0.4, "dy": 10}),
                              (t_wow + 0.2 + i * 0.08, {"alpha": 1, "s": 1, "dy": 0}),
                              (t_phr2 + 0.6, {"alpha": 1}), (t_phr2 + 1.2, {"alpha": 0})],
                             ["back", "linear", "sine"], pivot=(x, y)))

    # doves flying over the city
    def doves(k_):
        body = ""
        for j, (x, y, s) in enumerate(((1500, 260, 0.5), (1600, 210, 0.42), (1440, 190, 0.38))):
            w = (1.0, 0.0, -1.0)[(k_ + j) % 3]
            body += PR.dove(x, y, s, 1, wing=w)
        return doc(body)
    sc.add("doves", [doves(0), doves(1), doves(2)], z=40, frame_at=lambda t: float(int(t * 9) % 3),
           motion=M.combine(M.drift(vx=120, vy=-8), M.bob(10, 1.6)))

    # ---- effects ----
    sc.fx = [
        FX.sparkles((760, 560, 1260, 980), count=22, t0=t_call, t1=t_walk + 0.6, color=(255, 238, 170),
                    size=(8, 18), drift=-14, seed=19),
    ]

    # ---- sound ----
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-14, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_call, gain_db=-8)
    sc.sfx("footsteps", t_walk, dur=t_on - t_walk, gain_db=-12, fade_in=0.1, fade_out=0.2, rate=1 / STEP)
    sc.sfx("whoosh", t_fly0 + 0.1, gain_db=-12)
    sc.sfx("crowd", t_fly0 + 0.2, dur=T - t_fly0 + 0.6, gain_db=-14, fade_in=0.6, fade_out=0.8)
    sc.sfx("sheep", t_fly1 + 0.3, gain_db=-16, pan=0.4)
    sc.sfx("pop", t_wow, gain_db=-14)
    return sc
