"""Scene 5 — Joseph is sent to his brothers and put into the dry pit (Genesis 37:12-24).

Three picture-book pages on one 7200 x 1188 stage (hard page cuts on the narration):

  page 1 (home, x 0-2750)  line 0 '有一天，爸爸叫约瑟去看看在远处放羊的哥哥们。'  old Jacob in front of the family tent
          talks to Joseph (sound arcs); Joseph nods, waves goodbye (Jacob waves back) and sets off to the right with
          planted-foot strides; the camera walks with him past olive trees and the hills.
  page 2 (Dothan, x 2800-4912)  line 1 '哥哥们远远看见约瑟走来，就说：'  the ten brothers with their flock; far away on the
          hill path a tiny bright many-coloured figure walks down toward them (a coloured glow + sparkles: the coat);
          '看见' the brothers turn their heads.   line 2 (B) '看，那个做梦的来了！'  one brother points, two whisper face
          to face, the others fold their arms.
  page 3 (the pit, x 5000-7200; s06 continues on the same page)  a picture-book cross-section: the meadow on top, the
          earth cut open in front, the dry stone-lined pit.  line 3 '他们剥下约瑟的彩衣，'  Joseph stands in his plain
          under-tunic (coat='torn') and the coat tumbles through the air (whoosh trail) and lands on the grass (dust);
          '把他丢进一个干枯的坑里。'  Joseph hops over the opening, holds the rope and is let down into the shaft hand over
          hand (Levi holds the rope at the rim) - he lands with a little dust puff; the rope is pulled up.
          '坑里一滴水也没有。'  he scuffs the dry sandy floor: a dust puff, dust motes in the shaft.
          line 4 (Y) '哥哥！放我出去！'  Joseph calls up (call_up, worried, sound arcs rising); the brothers at the rim turn
          away. The last frame (Joseph standing sad at the bottom, brothers turned away) is s06's first frame.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import arcs_markup, cuts, dip, happy_hop, hop, nod, puff_markup, puff_motion, snap
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import blink_expr, make_cam, sheep_layer, when, with_blinks
from stories.joseph.scenes.s04_dream import (bros_markup, clouds_markup, dust_markup, dust_motion, family_tent,
                                             far_hills_markup, meadow_markup, pop_in, pop_out, show, sky_svg, sprite,
                                             stomp, sun_markup, tuft_row)

SW, SH = 7300, 1188
INK = P["ink"]
GY = 1030
SC = 0.9
WALK_P = 0.26
OX2 = 2800                # page 2 (Dothan pasture)
OX3 = 5100                # page 3 (the pit, cross-section)
# ---- page 3 geometry (page-local x; add the page offset). s06 draws the same page at offset 0.
GC = 560                  # front edge of the ground (top of the cross-section)
GS = GC - 6               # figures on the top surface
PX = 800                  # pit centre
PS = 0.9                  # pit scale
FLOOR = GC + PR.PIT_DEPTH * PS
P3_W = 3400
P3_BROS = [  # variant, x (page-local), facing while watching the pit
    (2, PX - 300, 1), (3, PX + 520, -1), (0, PX + 670, -1), (1, PX + 820, -1), (6, PX + 970, -1), (9, PX + 1120, -1)]
ROPER = 2                 # Levi holds the rope (s05 lowering, s06 pulling up); Judah (3) sells him in s06
COAT_LAND = (PX + 400, GS + 2)


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ page 3 (shared with s06)


def p3_sky_markup(ox, w=P3_W):
    defs = S.lin_grad(f"p3sky{ox}", [(0, "#94c9df"), (0.6, "#c4e3e9"), (1, "#f1ead2")])
    return (f"<defs>{defs}</defs>"
            f'<rect x="{ox - 20}" y="-20" width="{w + 40}" height="{GC + 40}" fill="url(#p3sky{ox})"/>')


def p3_land_markup(ox, w=P3_W):
    """Far hills, the top surface of the meadow with the road, and the earth cut open in front (no pit)."""
    out = ""
    UP = 610 - GC                # the upper land is drawn for GC=610 and lifted
    # far hills (one long range, with the faint pyramids far right for s06's last line)
    out += S.g(S.path(S.hill(ox - 80, ox + w + 80, 420, 120, seed=31, bottom=GC + UP, bumps=6), "#bdd3c4", sw=3) +
               S.path(S.hill(ox - 80, ox + w + 80, 455, 80, seed=33, bottom=GC + UP, bumps=5), "#acc9a2", sw=3.5),
               filter="wobble")
    rng = random.Random(4)
    trees = ""
    for i in range(int(w / 230)):
        x = ox + 90 + i * 230 + rng.uniform(-50, 50)
        trees += PR.olive_tree(x, 452 - rng.uniform(0, 26), rng.uniform(0.13, 0.17), seed=i + 3)
    out += trees
    # top surface: meadow band from the horizon to the front edge
    gid = f"p3top{ox}"
    defs = S.lin_grad(gid, [(0, "#b4cf82"), (1, "#97ba62")])
    top = (f"M{ox - 40},{GC + UP} L{ox - 40},468 Q{ox + w * 0.25},452 {ox + w * 0.5},466 Q{ox + w * 0.75},478 "
           f"{ox + w + 40},460 L{ox + w + 40},{GC + UP} Z")
    out += f"<defs>{defs}</defs>" + S.g(S.path(top, f"url(#{gid})", sw=4), filter="wobble")
    # the road: along the meadow behind the pit, curving up to the far horizon on the right
    road = (f"M{ox - 40},548 C{ox + 600},560 {ox + 1400},544 {ox + 2100},538 C{ox + 2600},534 {ox + 2900},500 "
            f"{ox + 3150},474 L{ox + 3190},474 C{ox + 2960},506 {ox + 2680},552 {ox + 2140},566 "
            f"C{ox + 1400},584 {ox + 600},590 {ox - 40},584 Z")
    out += S.g(S.path(road, "#e2c792", sw=3) +
               f'<path d="M{ox - 40},566 C{ox + 600},575 {ox + 1400},562 {ox + 2120},552 C{ox + 2700},542 '
               f'{ox + 2950},500 {ox + 3170},474" fill="none" stroke="#cfae74" stroke-width="3" '
               f'stroke-dasharray="14 12" opacity="0.7"/>', filter="wobble")
    # meadow strokes and flowers on the top surface
    rng = random.Random(7)
    for _ in range(int(w / 9)):
        x = ox + rng.uniform(0, w)
        y = rng.uniform(478, GC + UP - 6)
        if 536 < y < 596 and x < ox + 2400:
            continue
        h = 6 + (y - 470) * 0.08
        out += (f'<path d="M{f1(x)},{f1(y)} l{f1(rng.uniform(-3, 3))},{f1(-h)}" stroke="#6f9446" stroke-width="2.4" '
                f'stroke-linecap="round" opacity="0.65"/>')
    for _ in range(int(w / 70)):
        x = ox + rng.uniform(0, w)
        y = rng.uniform(482, GC + UP - 10)
        if 536 < y < 596 and x < ox + 2400:
            continue
        c = rng.choice(("#f3d36b", "#f6efe0", "#e99a8f"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="4" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
    out = f'<g transform="translate(0,{-UP})">{out}</g>'

    # the earth cut open in front: soil layers, pebbles and roots, down below the frame
    sid = f"p3soil{ox}"
    defs = S.lin_grad(sid, [(0, "#c9a070"), (0.45, "#b0845a"), (0.9, "#8f6a48"), (1, "#86634a")])
    out += f"<defs>{defs}</defs>"
    out += f'<rect x="{ox - 40}" y="{GC}" width="{w + 80}" height="{SH - GC + 40}" fill="url(#{sid})"/>'
    rng = random.Random(12)
    for k in range(1, 6):
        yy = GC + k * 105
        pts = [(ox - 60 + j * 300, yy + rng.uniform(-16, 16)) for j in range(int(w / 300) + 3)]
        out += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="#8a6646" stroke-width="3" '
                f'opacity="0.35"/>')
    peb = ""
    for _ in range(int(w / 24)):
        x = ox + rng.uniform(0, w)
        y = rng.uniform(GC + 30, SH + 10)
        if abs(x - (ox + PX)) < 200:
            continue
        peb += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(5, 13))}" ry="{f1(rng.uniform(4, 8))}" '
                f'fill="{rng.choice(("#c9bca6", "#a8a49c", "#d6c7aa"))}" stroke="{INK}" stroke-width="2"/>')
    roots = ""
    for _ in range(int(w / 110)):
        x = ox + rng.uniform(0, w)
        if abs(x - (ox + PX)) < 220:
            continue
        pts = [(x, GC + 2)]
        for j in range(4):
            pts.append((pts[-1][0] + rng.uniform(-14, 14), pts[-1][1] + rng.uniform(12, 24)))
        roots += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="#7a5638" stroke-width="2.4" '
                  f'stroke-linecap="round" opacity="0.7"/>')
    # bigger buried stones and two friendly worms in their little tunnels
    big = ""
    for x, y, r in ((ox + 260, GC + 300, 34), (ox + 1350, GC + 200, 40), (ox + 1900, GC + 380, 30),
                    (ox + 2600, GC + 260, 38), (ox + 3100, GC + 420, 34), (ox + 1550, GC + 470, 26)):
        big += S.path(S.blob(x, y, r * 1.5, r, 0.12, 9, seed=int(x)), "#b9ad98", sw=3)
        big += f'<ellipse cx="{f1(x - r * 0.4)}" cy="{f1(y - r * 0.35)}" rx="{f1(r * 0.4)}" ry="{f1(r * 0.18)}" fill="#e2d8c4"/>'
    for x, y in ((ox + 1150, GC + 330), (ox + 2250, GC + 220)):
        big += (f'<path d="M{x - 90},{y + 10} Q{x - 40},{y - 30} {x + 10},{y + 4} Q{x + 50},{y + 30} {x + 95},{y - 6}" '
                f'fill="none" stroke="#7d5a3e" stroke-width="30" stroke-linecap="round" opacity="0.55"/>')
        big += PR.worm(x + 40, y + 16, 0.9, 1)
    out += S.g(peb + roots, filter="wobble-fine") + big
    out += (f'<path d="M{ox - 40},{GC} L{ox + w + 40},{GC}" stroke="{INK}" stroke-width="5" fill="none" '
            f'filter="url(#wobble)"/>')
    # grass fringe along the front edge
    fr = ""
    for i in range(int(w / 26)):
        x = ox + i * 26 + rng.uniform(-8, 8)
        if abs(x - (ox + PX)) < 175:
            continue
        hgt = rng.uniform(10, 22)
        fr += (f'<path d="M{f1(x - 7)},{GC + 3} L{f1(x + rng.uniform(-4, 4))},{f1(GC - hgt)} L{f1(x + 7)},{GC + 3} Z" '
               f'fill="#88ad55" stroke="{INK}" stroke-width="2"/>')
    out += S.g(fr, filter="wobble-fine")
    return out


def p3_pit_markup(ox):
    """The dry, stone-lined pit in cross-section (the props cutaway, its soil blended into the page's)."""
    x = ox + PX
    cid = f"p3pitclip{ox}"
    d = (f"M{x - 215},{GC - 60} L{x + 215},{GC - 60} L{x + 215},{GC + 4} L{x + 158},{GC + 4} L{x + 158},{FLOOR + 2} "
         f"L{x - 158},{FLOOR + 2} L{x - 158},{GC + 4} L{x - 215},{GC + 4} Z")
    return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{PR.pit(x, GC, PS, view="cutaway", width=240)}</g>')


def p3_props_markup(ox):
    """Little things on the surface: a bush, a rock pile, a few dry tufts by the pit."""
    out = PR.bush(ox + 1500, GC - 50, 0.45, variant=2) + PR.bush(ox + 220, GC - 90, 0.4, variant=0)
    out += PR.bush(ox + 2600, GC - 80, 0.4, variant=1)
    for x, s, v in ((ox + PX - 210, 0.5, 1), (ox + PX + 205, 0.45, 1), (ox + 2300, 0.5, 0)):
        out += PR.grass_tuft(x, GC - 2, s, variant=v)
    return out


def p3_background(ox, w=P3_W, docf=None):
    """Static page-3 background document (sky, land, pit, props)."""
    docf = docf or doc
    return docf(p3_sky_markup(ox, w) + p3_land_markup(ox, w) + p3_pit_markup(ox) + p3_props_markup(ox))


def up_arcs_markup(x, y, k, s=1.0):
    """Sound arcs rising above a head (calling up)."""
    out = ""
    for i in range(3):
        r = (14 + 14 * i + (k - 2) * 2) * s
        out += (f'<path d="M{f1(x - r * 0.9)},{f1(y - r * 0.45)} Q{f1(x)},{f1(y - r * 1.25)} {f1(x + r * 0.9)},'
                f'{f1(y - r * 0.45)}" fill="none" stroke="{INK}" stroke-width="{5 * s:.1f}" stroke-linecap="round" '
                f'opacity="0.85"/>')
    return S.g(out, filter="wobble-fine")


def p3_bro(ox, v, x, facing, pose, expr, gy=GS):
    return C.ground_shadow(ox + x, gy, SC, 120) + C.brothers(ox + x, gy, SC, facing, variant=v, pose=pose, expr=expr,
                                                             staff=False)


ROPE_X_OFF = -40          # the rope hangs at PX - 40
JF = -1                   # Joseph faces left in the shaft (toward the rope side)


def joseph_pit_x(ox):
    """Joseph's anchor x in the shaft so that his far (rope) hand hangs at the rope line."""
    hx = C.hand_positions(C.joseph, 0, 0, SC, JF, pose="hold_rope", coat="torn")[0][0]
    return ox + PX + ROPE_X_OFF - hx


# ============================================================================ pages 1 and 2


def p1_background():
    out = S.g(far_hills_markup(w=2800, base=770, seed=8, tents=False), filter="wobble")
    out += S.g(S.path(S.hill(-80, 2880, 905, 130, seed=24, bumps=4), "#a3c47c", sw=4), filter="wobble")
    for x, y, s, f, v in ((1350, 905, 0.34, 1, 0), (1410, 900, 0.32, -1, 2), (2250, 902, 0.33, 1, 3)):
        out += PR.sheep(x, y, s, f, variant=v, pose="graze")
    out += S.g(meadow_markup(-80, 2880, 905, SH + 20, seed=9), filter="wobble")
    # the path out of the camp
    out += S.g(S.path(f"M900,1062 C1400,1040 1900,1050 2900,1030 L2900,1080 C1900,1100 1400,1096 900,1112 Z",
                      "#d9c08c", sw=3, extra='opacity="0.85"'), filter="wobble")
    out += PR.olive_tree(1500, 990, 0.62, seed=5) + PR.olive_tree(2550, 985, 0.7, seed=6)
    out += PR.bush(2080, 1000, 0.5, variant=1) + PR.bush(1250, 1005, 0.45, variant=0)
    out += family_tent(250, GY, 0.85, lamp=False)
    out += PR.jar(700, GY - 6, 0.6) + PR.sack(650, GY - 2, 0.5)
    return doc(out)


P2_PIT = (OX2 + 760, 1000)
P2_PATH = [(OX2 + 470, 690), (OX2 + 560, 700), (OX2 + 650, 716), (OX2 + 730, 736)]


def p2_background():
    ox = OX2
    out = S.g(f'<g transform="translate({ox},0)">{far_hills_markup(w=2112, base=740, seed=14, tents=False)}</g>')
    # the big hill on the left with the path Joseph comes down
    hill = S.hill(ox - 100, ox + 1300, 900, 260, seed=41, bumps=2)
    out += S.g(S.path(hill, "#a9c97c", sw=4), filter="wobble")
    path = (f"M{ox + 300},{688} C{ox + 450},{684} {ox + 600},{700} {ox + 760},{748} C{ox + 900},{790} {ox + 960},{830} "
            f"{ox + 1000},{900} L{ox + 1060},{900} C{ox + 1010},{820} {ox + 930},{776} {ox + 790},{732} "
            f"C{ox + 640},{688} {ox + 460},{674} {ox + 300},{678} Z")
    out += S.g(S.path(path, "#dcc391", sw=2.5), filter="wobble")
    out += PR.olive_tree(ox + 260, 700, 0.3, seed=7) + PR.olive_tree(ox + 1150, 760, 0.36, seed=8)
    out += S.g(S.path(S.hill(ox + 900, ox + 2200, 930, 90, seed=43, bumps=2), "#a3c47c", sw=4), filter="wobble")
    out += S.g(f'<g>{meadow_markup(ox - 80, ox + 2200, 920, SH + 20, seed=13)}</g>', filter="wobble")
    out += PR.pit(P2_PIT[0], P2_PIT[1], 0.75, view="outside")
    out += PR.bush(ox + 2020, 980, 0.55, variant=3) + PR.olive_tree(ox + 2080, 990, 0.6, seed=9)
    return doc(out)


P2_FRONT = [(1, OX2 + 1240), (2, OX2 + 1395), (4, OX2 + 1515), (0, OX2 + 1700), (3, OX2 + 1860)]
P2_BACK = [(5, OX2 + 1320), (7, OX2 + 1610), (8, OX2 + 1780), (9, OX2 + 1950)]
P2_GYB = GY - 30


FG1 = [(60, 1160, 1.2, 0), (640, 1178, 1.0, 2), (1180, 1172, 1.1, 0), (1700, 1180, 1.0, 2), (2300, 1168, 1.15, 0),
       (2700, 1176, 1.0, 0)]
FG2 = [(OX2 + 40, 1170, 1.15, 2), (OX2 + 600, 1178, 1.0, 0), (OX2 + 1150, 1182, 1.0, 0), (OX2 + 2060, 1168, 1.15, 2)]
FG3 = [(OX3 + 120, GC + 2, 0.7, 0), (OX3 + 1300, GC + 2, 0.6, 2), (OX3 + 1900, GC + 2, 0.7, 0)]


def fg_svg(k):
    return doc(tuft_row(FG1 + FG2, k * 2.1) + tuft_row(FG3, k * 2.1 + 1))


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]
    clamp, cam_path = make_cam(SW, SH)

    # ---------------- times
    t_cut2 = snap(L1.start - 0.05)
    t_cut3 = snap(L3.start - 0.03)
    t_talk = when(ctx, "爸爸叫约瑟")
    t_go_see = when(ctx, "去看看")
    t_far = when(ctx, "在远处")
    t_wave = snap(t_far - 0.15)
    t_turn = snap(t_wave + 0.75)
    t_walk = snap(t_turn + 0.12)
    t_see = snap(when(ctx, "远远看见"))
    t_comes = when(ctx, "约瑟走来")
    t_point = snap(L2.start - 0.05)
    t_whisper = snap(L2.start + 0.35)
    t_coat = t_cut3 + 0.05                                  # the coat flies
    t_coat_land = snap(t_coat + 0.85)
    t_drop = snap(when(ctx, "把他丢进") - 0.05)
    t_hang = t_drop + 0.45
    t_land = snap(min(when(ctx, "坑里一滴水") - 0.2, t_hang + 2.0))
    t_dry = when(ctx, "一滴水也没有")
    t_rope_up = snap(t_land + 0.45)
    t_call = snap(L4.start - 0.08)
    t_away = snap(L4.start + 0.55)
    t_settle = snap(L4.end + 0.35)

    # ---------------- camera (hard page cuts)
    JW0 = 1090                                              # Joseph's spot on page 1
    n_w = int((t_cut2 - t_walk) / WALK_P) + 1
    step = 80.0
    C1a = Cam(980, 740, 1320)
    C1b = Cam(JW0 + n_w * step * 0.62 + 120, 740, 1320)
    C2a = Cam(OX2 + 1250, 640, 1700)
    C2b = Cam(OX2 + 1056, 594, 2112)
    C2c = Cam(OX2 + 1290, 650, 1640)
    C3a = Cam(OX3 + PX + 250, 520, 1500)
    C3b = Cam(OX3 + PX + 120, 620, 1560)
    C3e = Cam(OX3 + 1000, 530, 1800)
    page1 = cam_path([(0, C1a), (t_walk + 0.2, C1a), (t_cut2, C1b)])
    page2 = cam_path([(0, C2a), (t_see + 0.2, C2a), (t_comes + 1.2, C2b), (L1.end + 0.1, C2b), (t_cut3, C2c)])
    page3 = cam_path([(0, C3a), (t_drop - 0.2, C3a), (t_hang + 0.9, C3b), (t_dry + 0.8, C3b), (L4.start - 0.3, C3e),
                      (T, C3e)])
    sc.camera = lambda t: page1(t) if t < t_cut2 else (page2(t) if t < t_cut3 else page3(t))

    # ---------------- skies and backgrounds
    sc.add("sky", sky_svg("s5sky", [(0, "#8ec6df"), (0.55, "#bfe2ea"), (1, "#f2ead0")], SW, SH), z=0, wc=0.5)
    sc.add("sun", doc(sun_markup(2300, 230, 66) + sun_markup(OX2 + 1900, 200, 66)), z=0.1, wc=0.3)
    sc.add("clouds", doc(clouds_markup(((400, 200, 320, 74, 1), (1300, 140, 260, 60, 2), (2200, 250, 300, 70, 3),
                                        (OX2 + 300, 180, 300, 70, 4), (OX2 + 1250, 120, 260, 60, 5),
                                        (OX2 + 1800, 300, 220, 52, 6)))),
           z=0.2, wc=0.6, motion=lambda t: Tf(dx=-7 * t))
    sc.add("p1", p1_background(), z=1)
    sc.add("p2", p2_background(), z=1)
    sc.add("p3_sky", doc(p3_sky_markup(OX3)), z=0.05, wc=0.5)
    sc.add("p3", doc(p3_land_markup(OX3) + p3_pit_markup(OX3) + p3_props_markup(OX3)), z=1)
    # the camera never shows the page seams, but keep the clouds on page 3 above its own sky
    sc.add("p3_clouds", doc(clouds_markup(((OX3 + 300, 150, 300, 70, 7), (OX3 + 1200, 110, 260, 60, 8),
                                           (OX3 + 1900, 210, 240, 56, 9)))), z=0.06, wc=0.6,
           motion=lambda t: Tf(dx=-7 * t))

    # =============================================================== page 1: Jacob sends Joseph
    JX = 880

    def jac(pose, expr=None):
        return C.ground_shadow(JX, GY, SC, 120) + C.jacob(JX, GY, SC, 1, pose=pose, expr=expr)
    jfr = [jac("stand", "kind"), jac("talk", "happy"), jac("bless", "happy"), jac("stand", blink_expr("kind")),
           jac("talk", blink_expr("happy"))]
    jb = [(0, 0), (snap(t_talk - 0.1), 1), (snap(t_wave + 0.2), 2), (snap(t_cut2 - 0.6), 0)]
    jb = with_blinks(jb, {0: 3, 1: 4}, [0.7, 2.6])
    sprite(sc, "jacob", 2.0, jfr, (JX, GY), base=jb, docf=doc,
           bumps=[dip(snap(t_talk - 0.1), SC, (JX, GY), 5), dip(snap(t_wave + 0.2), SC, (JX, GY), 5),
                  nod(t_go_see + 0.2, (JX, GY), 3, 0.5), nod(t_far + 0.9, (JX, GY), 3, 0.5)],
           breathe=(0.01, 3.1, 0.2), extra=show(0, t_cut2))
    jh = C.body_points(C.jacob, JX, GY, SC, 1, pose="talk")["head"]
    sc.add("jarcs", [doc(arcs_markup(jh[0] + 66, jh[1] + 22, 1, k, 1.15)) for k in (1, 2, 3)], z=2.05, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_talk, t_wave))

    def jo1(x, pose, facing, expr=None):
        return C.ground_shadow(x, GY, SC, 110) + C.joseph(x, GY, SC, facing, pose=pose, expr=expr)
    end_x = JW0 + n_w * step
    ofr = [jo1(end_x, "walk_a", 1), jo1(end_x, "walk_b", 1), jo1(end_x, "stand", -1, "happy"),
           jo1(end_x, "ride_wave", -1, "happy"), jo1(end_x, "stand", 1, "happy"), jo1(end_x, "stand", -1, blink_expr("happy"))]
    ob = with_blinks([(0, 2), (t_wave, 3), (t_turn, 4)], {2: 5}, [1.3, 3.2])
    sprite(sc, "joseph1", 2.2, ofr, (end_x, GY), base=ob, walks=[(t_walk, n_w, step, 0)], start_off=-n_w * step,
           docf=doc, bumps=[nod(t_go_see + 0.35, (end_x, GY), -4, 0.5), happy_hop(snap(t_wave - 0.4), SC, (end_x, GY), 14),
                            dip(t_wave, SC, (end_x, GY), 5), dip(t_turn, SC, (end_x, GY), 5)],
           breathe=(0.012, 2.6, 0.0), extra=show(0, t_cut2))

    # sheep near the tent on page 1
    for i, (x, y, s, f, v) in enumerate(((260, 1110, 0.8, 1, 1), (1250, 1090, 0.75, -1, 0), (1960, 1100, 0.8, 1, 2))):
        sheep_layer(sc, f"sheep1_{i}", 2.1, x, y, s, f, v, seed=20 + i, T=t_cut2, docf=doc,
                    bleats=((t_walk + 0.6,) if i == 1 else ()))

    # =============================================================== page 2: the brothers see him coming
    # tiny Joseph walking down the hill path (a bright coloured dot)
    jsmall = 0.27

    def path_pt(u):
        pts = P2_PATH
        k = min(len(pts) - 2, int(u * (len(pts) - 1)))
        v = u * (len(pts) - 1) - k
        return pts[k][0] + (pts[k + 1][0] - pts[k][0]) * v, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * v
    ref = P2_PATH[0]
    tfr = [doc(C.joseph(ref[0], ref[1], jsmall, 1, pose=p)) for p in ("walk_a", "walk_b")]

    def tiny_m(t):
        u = M.progress(t, t_cut2, t_cut3, "linear")
        x, y = path_pt(u)
        k = 1 + 0.25 * u
        return Tf(dx=x - ref[0], dy=y - ref[1], sx=k, sy=k, px=ref[0], py=ref[1],
                  alpha=1.0 if t_cut2 <= t < t_cut3 else 0.0)
    sc.add("tiny_joseph", tfr, z=1.5, wc=0.6, frame_at=lambda t: float(int(t / 0.24) % 2), motion=tiny_m)
    gl_id = "s5cglow"
    glow = doc(f'<ellipse cx="{ref[0]}" cy="{ref[1] - 36}" rx="80" ry="84" fill="url(#{gl_id})"/>',
               S.rad_grad(gl_id, [(0, "#fff3c0", 1.0), (0.45, "#f8c86a", 0.6), (1, "#f2a0c0", 0)]))
    sc.add("tiny_glow", glow, z=1.45, wc=0,
           motion=lambda t: Tf(dx=tiny_m(t).dx, dy=tiny_m(t).dy, alpha=tiny_m(t).alpha * (0.55 + 0.35 * M.progress(
               t, t_see - 0.1, t_see + 0.4) * (0.75 + 0.25 * math.sin(t * 5)))))

    def tiny_sparkle_fx():
        base = FX.sparkles((-60, -130, 60, 10), count=9, t0=t_see - 0.1, t1=t_cut3, size=(6, 12), drift=0, seed=52)

        def fx(frame, t, view):
            if not (t_cut2 <= t < t_cut3):
                return frame
            m = tiny_m(t)

            class V:
                scale = view.scale

                @staticmethod
                def to_out(x, y):
                    return view.to_out(x + ref[0] + m.dx, y + ref[1] + m.dy)
            return base(frame, t, V)
        return fx
    sc.fx.append(tiny_sparkle_fx())

    # the flock
    for i, (x, y, s, f, v, bl) in enumerate(((OX2 + 900, 1120, 0.85, 1, 0, ()), (OX2 + 1080, 1060, 0.7, -1, 2, ()),
                                            (OX2 + 1150, 1150, 0.9, 1, 3, (t_see + 1.2,)),
                                            (OX2 + 2010, 1110, 0.8, -1, 1, ()), (OX2 + 600, 1045, 0.65, 1, 1, ()))):
        sheep_layer(sc, f"sheep2_{i}", 2.4 if y > 1080 else 1.9, x, y, s, f, v, seed=30 + i, T=t_cut3, docf=doc,
                    bleats=bl)
    # brothers: look up at '看见'; at the B line one points, two whisper, the others fold their arms
    def p2row(vs, gy, s, pose_of):
        out = ""
        for v, x in vs:
            pose, f, e = pose_of(v)
            out += C.ground_shadow(x, gy, s, 120) + C.brothers(x, gy, s, f, variant=v, pose=pose, expr=e, staff=False)
        return out
    sp_v = P2_FRONT[0][0]

    def look(e):
        return lambda v: ("stand", -1, e)

    def b_line(v):
        if v == sp_v:
            return ("point", -1, "angry")
        if v == 2:
            return ("whisper", 1, "sly")
        if v == 4:
            return ("whisper", -1, "sly")
        return ("cross_arms", -1, "jealous")
    fronts = [p2row(P2_FRONT, GY, SC, look("neutral")), p2row(P2_FRONT, GY, SC, look("surprised")),
              p2row(P2_FRONT, GY, SC, b_line), p2row(P2_FRONT, GY, SC, look(blink_expr("neutral")))]
    backs = [p2row(P2_BACK, P2_GYB, SC * 0.95, look("neutral")), p2row(P2_BACK, P2_GYB, SC * 0.95, look("surprised")),
             p2row(P2_BACK, P2_GYB, SC * 0.95, b_line), p2row(P2_BACK, P2_GYB, SC * 0.95, look(blink_expr("neutral")))]
    for name, fr, z, ph, gy in (("bros2_back", backs, 2.3, 0.3, P2_GYB), ("bros2_front", fronts, 2.6, 0.0, GY)):
        cx = OX2 + 1600
        base = with_blinks([(0, 0), (snap(t_see + ph * 0.3), 1), (snap(t_point + ph * 0.5), 2)], {0: 3},
                           [t_cut2 + 0.5 + ph])
        sprite(sc, name, z, fr, (cx, gy), base=base, docf=doc,
               bumps=[dip(snap(t_see + ph * 0.3), SC, (cx, gy), 5), dip(snap(t_point + ph * 0.5), SC, (cx, gy), 7),
                      nod(t_whisper + 0.4 + ph, (cx, gy), 2, 0.6)],
               breathe=(0.008, 2.8, ph), extra=show(t_cut2, t_cut3))
    sph = C.body_points(C.brothers, P2_FRONT[0][1], GY, SC, -1, variant=sp_v, pose="point")["head"]
    sc.add("p2arcs", [doc(arcs_markup(sph[0] - 60, sph[1] + 20, -1, k, 1.2)) for k in (1, 2, 3)], z=2.65, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_point + 0.1, L2.end))
    # whisper marks (little dotted sound puffs between the whisperers)
    wx = (P2_FRONT[1][1] + P2_FRONT[2][1]) / 2
    wy = GY - 0.9 * 300
    sc.add("whisper", [doc(S.g("".join(f'<circle cx="{f1(wx + 18 * math.cos(a + k))}" cy="{f1(wy - 30 + 10 * math.sin(a * 2 + k))}" '
                                       f'r="4" fill="{P["ink_soft"]}"/>' for a in (0, 2.1, 4.2)), filter="wobble-fine"))
                       for k in (0, 1, 2)], z=2.66, wc=0, frame_at=lambda t: float(int(t * 6) % 3),
           motion=show(t_whisper + 0.15, t_cut3))

    # =============================================================== page 3: the coat, the pit
    def bro3(v, x, f, pose, expr):
        return p3_bro(OX3, v, x, f, pose, expr)
    # brothers (Levi, v2, holds the rope)
    others = [b for b in P3_BROS if b[0] != ROPER]
    left = [b for b in others if b[1] < PX]
    right = [b for b in others if b[1] > PX]
    for name, grp, z, ph in ((("b3_right", right, 2.4, 0.5),) if not left else
                             (("b3_left", left, 2.4, 0.2), ("b3_right", right, 2.4, 0.5))):
        cx = OX3 + sum(b[1] for b in grp) / len(grp)
        fr = ["".join(bro3(v, x, f, "cross_arms", "angry") for v, x, f in grp),
              "".join(bro3(v, x, f, "stand", "neutral") for v, x, f in grp),
              "".join(bro3(v, x, -f, "cross_arms", "neutral") for v, x, f in grp),
              "".join(bro3(v, x, f, "stand", blink_expr("neutral")) for v, x, f in grp)]
        base = with_blinks([(0, 0), (snap(t_hang + ph), 1), (snap(t_away + ph * 0.4), 2)], {1: 3},
                           [t_land + 0.9 + ph])
        sprite(sc, name, z, [doc(f) for f in fr], (cx, GS), base=base, docf=doc,
               bumps=[dip(snap(t_hang + ph), SC, (cx, GS), 4), dip(snap(t_away + ph * 0.4), SC, (cx, GS), 6),
                      stomp(snap(t_coat_land + 0.05), SC, (cx, GS), 5)],
               breathe=(0.008, 2.9, ph), extra=show(t_cut3))
    jv, jx3, jf = [b for b in P3_BROS if b[0] == ROPER][0]
    jfr3 = [bro3(jv, jx3, jf, "cross_arms", "angry"), bro3(jv, jx3, jf, "pull", "determined"),
            bro3(jv, jx3, jf, "stand", "neutral"), bro3(jv, jx3, -jf, "stand", "neutral"),
            bro3(jv, jx3, jf, "stand", blink_expr("neutral"))]
    jb3 = with_blinks([(0, 0), (snap(t_drop + 0.2), 1), (t_rope_up + 0.45, 2), (t_away, 3)], {2: 4}, [t_dry + 0.6])
    sprite(sc, "roper", 2.45, [doc(f) for f in jfr3], (OX3 + jx3, GS), base=jb3, docf=doc,
           bumps=[dip(snap(t_drop + 0.2), SC, (OX3 + jx3, GS), 6), dip(t_rope_up + 0.45, SC, (OX3 + jx3, GS), 6),
                  dip(t_away, SC, (OX3 + jx3, GS), 6)],
           breathe=(0.01, 2.7, 0.1), extra=show(t_cut3))
    # the rope: from the roper's fists to the rim, then down the shaft to Joseph's hand
    fists = C.hand_positions(C.brothers, OX3 + jx3, GS, SC, jf, variant=jv, pose="pull")
    rx = OX3 + PX + ROPE_X_OFF
    rim = (OX3 + PX - 118, GC - 6)
    rope_top = (f'M{f1(fists[0][0])},{f1(fists[0][1])} L{f1(fists[1][0])},{f1(fists[1][1])} '
                f'Q{f1(rim[0] - 10)},{f1(rim[1] - 40)} {f1(rim[0])},{f1(rim[1])} Q{f1(rx - 20)},{f1(GC - 12)} '
                f'{f1(rx)},{f1(GC + 8)}')
    rope_css = lambda d, w: (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 5}" stroke-linecap="round"/>'  # noqa: E731
                             f'<path d="{d}" fill="none" stroke="{P["wood_light"]}" stroke-width="{w}" '
                             f'stroke-linecap="round"/>')
    t_rope_gone = t_rope_up + 0.45
    sc.add("rope_top", doc(S.g(rope_css(rope_top, 6), filter="wobble-fine")), z=2.5,
           motion=show(snap(t_drop + 0.2), t_rope_gone))
    rope_down = f"M{f1(rx)},{f1(GC + 4)} L{f1(rx + 3)},{f1(FLOOR - 20)}"
    rope_len = FLOOR - 20 - GC

    # Joseph on the surface (13.4 - drop), then in the shaft
    JT = OX3 + PX + 230

    def jtop(pose, expr):
        return C.ground_shadow(JT, GS, SC, 110) + C.joseph(JT, GS, SC, -1, pose=pose, expr=expr, coat="torn")
    jtfr = [jtop("stand", "surprised"), jtop("sad", "sad"), jtop("stand", blink_expr("surprised"))]
    t_sad = snap(t_coat_land + 0.25)
    sprite(sc, "jtop", 2.7, jtfr, (JT, GS), base=with_blinks([(0, 0), (t_sad, 1)], {0: 2}, [t_coat + 0.4]), docf=doc,
           bumps=[dip(t_sad, SC, (JT, GS), 5), dip(t_drop, SC, (JT, GS), 8)],
           breathe=(0.012, 2.4, 0.0), extra=show(t_cut3, t_drop + 0.02))
    PJ = joseph_pit_x(OX3)

    def jpit(pose, expr):
        return C.joseph(PJ, FLOOR, SC, JF, pose=pose, expr=expr, coat="torn")
    shadow_floor = doc(C.ground_shadow(PJ, FLOOR - 4, SC, 120))
    jpfr = [jpit("hold_rope", "worried"), jpit("stand", "worried"), jpit("sad", "sad"), jpit("call_up", "worried"),
            jpit("stand", blink_expr("worried")), jpit("sad", blink_expr("sad"))]
    y_hang = GC + 150
    hand_dy = C.hand_positions(C.joseph, 0, 0, SC, JF, pose="hold_rope", coat="torn")[0][1]

    def pit_dy(t):
        """Joseph's vertical offset from the floor: hop in over the rim, hand-over-hand down the rope."""
        if t < t_drop:
            return GS - FLOOR
        if t < t_hang:
            u = (t - t_drop) / (t_hang - t_drop)
            y = (GS - FLOOR) + ((y_hang - FLOOR) - (GS - FLOOR)) * M.ease("inout")(u) - 70 * math.sin(math.pi * u)
            return y
        n = 4
        seg = (t_land - t_hang) / n
        k = min(n, max(0.0, (t - t_hang) / seg))
        i = int(k)
        frac = k - i
        prog = (i + (M.ease("inout")(frac) if i < n else 0)) / n
        return (y_hang - FLOOR) * (1 - prog)

    def pit_dx(t):
        if t < t_drop:
            return JT - PJ
        if t < t_hang:
            u = (t - t_drop) / (t_hang - t_drop)
            return (JT - PJ) * (1 - M.ease("inout")(u))
        return 0.0
    t_stand = snap(t_land)
    t_sad2 = snap(t_dry + 0.1)
    t_end_sad = snap(L4.end + 0.3)
    jpb = with_blinks([(0, 0), (t_stand, 1), (t_sad2, 2), (t_call, 3), (t_end_sad, 2)], {1: 4, 2: 5},
                      [t_land + 0.9, T - 0.7])
    sc.add("jpit", [doc(f) for f in jpfr], z=1.6, frame_at=cuts(jpb),
           motion=M.combine(lambda t: Tf(dx=pit_dx(t), dy=pit_dy(t)),
                            dip(t_stand, SC, (PJ, FLOOR), 9), dip(t_sad2, SC, (PJ, FLOOR), 5),
                            dip(t_call, SC, (PJ, FLOOR), 6), dip(t_end_sad, SC, (PJ, FLOOR), 5),
                            hop(t_call + 0.6, [(0, {"dy": 0}), (0.15, {"dy": -10}), (0.3, {"dy": 0})], (PJ, FLOOR)),
                            hop(t_call + 1.0, [(0, {"dy": 0}), (0.15, {"dy": -8}), (0.3, {"dy": 0})], (PJ, FLOOR)),
                            M.breathe(0.012, 2.5, pivot=(PJ, FLOOR)),
                            show(t_drop - 0.02)))
    sc.add("jpit_shadow", shadow_floor, z=1.55, wc=0,
           motion=lambda t: Tf(alpha=M.progress(t, t_land - 0.5, t_land, "sine")))
    sc.add("rope_down", doc(S.g(rope_css(rope_down, 6), filter="wobble-fine")), z=1.58,
           reveal=lambda t: {"mode": "down", "soft": 6,
                             "frac": max(0.0, min(1.0, ((FLOOR + pit_dy(t) + hand_dy) - GC + 20) / rope_len))
                             if t < t_rope_up else
                             max(0.0, min(1.0, ((FLOOR + hand_dy) - GC + 20) / rope_len)) *
                             (1 - M.progress(t, t_rope_up, t_rope_gone, "in"))},
           motion=show(snap(t_drop + 0.2), t_rope_gone + 0.05))
    # calling up: rising sound arcs
    jh3 = C.body_points(C.joseph, PJ, FLOOR, SC, JF, pose="call_up", coat="torn")["head_top"]
    sc.add("call_arcs", [doc(up_arcs_markup(jh3[0] + 6, jh3[1] - 40, k, 1.3)) for k in (1, 2, 3)], z=1.62, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_call + 0.1, L4.end + 0.1))
    # dust: landing and the dry scuff; dust motes in the shaft
    for i, (tt, w) in enumerate(((t_land, 200), (t_dry + 0.45, 170))):
        sc.add(f"pdust{i}", doc(dust_markup(PJ + (0 if i == 0 else 40), FLOOR - 6, w, seed=40 + i)), z=1.65, wc=0.3,
               motion=dust_motion(tt, (PJ, FLOOR)))
    sc.fx.append(FX.motes((OX3 + PX - 120, GC + 40, OX3 + PX + 120, FLOOR - 30), count=14, t0=t_land, t1=T + 1,
                          color=(240, 220, 180), size=(2.5, 5), seed=61, alpha=140))

    # the coat: pulled off -> tumbles through the air -> lies on the grass
    c0 = (JT - 20, GS - 190)
    c1 = (COAT_LAND[0] + OX3, COAT_LAND[1] - 40)
    cs = 0.5
    bundle = doc(PR.coat_of_colours(c0[0], c0[1], cs, 1, state="bundle"))

    def coat_m(t):
        u = M.progress(t, t_coat, t_coat_land, "linear")
        x = c0[0] + (c1[0] - c0[0]) * u
        y = c0[1] + (c1[1] - c0[1]) * u - 230 * math.sin(math.pi * u)
        return Tf(dx=x - c0[0], dy=y - c0[1], rot=-420 * u, px=c0[0], py=c0[1],
                  alpha=1.0 if t_coat - 0.02 <= t < t_coat_land else 0.0)
    sc.add("coat_fly", bundle, z=2.8, motion=coat_m)
    trail = ""
    for k in range(3):
        pts = []
        for j in range(9):
            u = 0.08 + 0.72 * j / 8
            x = c0[0] + (c1[0] - c0[0]) * u
            y = c0[1] + (c1[1] - c0[1]) * u - 230 * math.sin(math.pi * u) + (k - 1) * 26
            pts.append((x, y))
        trail += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["ink_soft"]}" '
                  f'stroke-width="5" stroke-linecap="round" stroke-dasharray="40 26" opacity="0.7"/>')
    sc.add("coat_trail", doc(S.g(trail, filter="wobble-fine")), z=2.75, wc=0,
           reveal=lambda t: {"mode": "left", "soft": 60, "frac": M.progress(t, t_coat + 0.1, t_coat_land - 0.05, "linear")},
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_coat_land - 0.1, t_coat_land + 0.4, "sine")))
    sc.add("coat_lying", doc(PR.coat_of_colours(c1[0], COAT_LAND[1], cs, 1, state="lying")), z=2.3,
           motion=M.combine(show(t_coat_land), hop(t_coat_land, [(0, {"sy": 0.85}), (0.12, {"sy": 1.05}), (0.25, {"sy": 1})],
                                                    (c1[0], COAT_LAND[1]))))
    sc.add("coat_dust", doc(dust_markup(c1[0], COAT_LAND[1] + 4, 200, seed=44)), z=2.85, wc=0.3,
           motion=dust_motion(t_coat_land, (c1[0], COAT_LAND[1])))
    sc.add("hop_puff", doc(puff_markup(JT - 60, GS - 150, 110, 170, seed=7, k=0.7)), z=2.9, wc=0,
           motion=puff_motion(t_drop + 0.02, (JT - 60, GS - 150)))

    # ---------------- foreground grass
    sc.add("fg", [fg_svg(k) for k in range(3)], z=3.5, frame_at=lambda t: float(int(t * 2.2) % 3))

    # ---------------- sound
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0.0, dur=t_cut2 + 0.3, gain_db=-20, fade_in=0.8, fade_out=0.4)
    sc.sfx("footsteps", t_walk, dur=t_cut2 - t_walk, gain_db=-17, fade_out=0.2)
    sc.sfx("sheep", t_walk + 0.6, gain_db=-15, pan=-0.2)
    sc.sfx("sheep", t_see + 1.2, gain_db=-14, pan=-0.3)
    sc.sfx("sparkle", t_see - 0.05, gain_db=-15, pan=-0.5)
    sc.sfx("whoosh", t_coat + 0.05, gain_db=-9)
    sc.sfx("cloth", t_coat_land - 0.05, gain_db=-11, pan=0.2)
    sc.sfx("whoosh", t_drop + 0.05, gain_db=-14)
    sc.sfx("thud", t_land, gain_db=-8)
    sc.sfx("thud", t_dry + 0.45, gain_db=-16)
    sc.sfx("cloth", t_away, gain_db=-17)
    return sc
