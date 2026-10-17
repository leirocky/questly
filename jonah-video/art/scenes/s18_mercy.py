"""Scene 18 — God has mercy on Nineveh (Jonah 3:10), v2.

"上帝看见他们真的改掉了坏行为，就可怜他们，没有毁灭这座城。 / 整座尼尼微城，都得到了平安！"

One 2800 x 1575 stage, no cuts: a wide view over the whole city of Nineveh from a family's flat mud-brick roof.
Foreground: the roof terrace (a reed mat, a ladder hatch, pots, a dovecote with doves, a lamb and a goat in
sackcloth blankets) where a family in sackcloth kneels in prayer - grandpa, father, mother, a girl and a boy.
Beyond the low parapet: a street where neighbours kneel, rows of flat roofs (people praying on them too), palms,
the great ziggurat, the far city with its wall and palace, and blue mountains on the horizon. A heavy grey cloud
hangs low over the whole city (adapted from the approved v1 s10 ending: same cloud banks, gleam, rays, glazes).

  line 0  "上帝看见他们真的改掉了坏行为，"  calm and grey, everyone kneels with eyes closed; a warm glow kindles
                                          behind the cloud right above the ziggurat (God sees - never a figure);
                                          the girl peeks up at it; the camera drifts slowly over the praying roof.
          "就可怜他们，"                    the cloud splits above the ziggurat (chime), golden light pours down in
                                          rays over the city, the gloom lifts; the family looks up in wonder.
          "没有毁灭这座城。"                the cloud banks drift apart and dissolve, the sky turns gold, the warm
                                          light spreads over all the roofs; faces turn to relief and joy, the
                                          neighbours on the roofs and in the street smile up; doves rise.
  line 1  "整座尼尼微城，"                  the camera pulls out to the whole city: the doves burst from the dovecote
                                          and circle over the roofs; people all over the city stand up and cheer in
                                          a wave from the centre outward.
          "都得到了平安！"                  the children jump and cheer, father raises his arms, the lamb and the goat
                                          hop; sparkles twinkle over the city. Calm, joyful hold for the dissolve.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a small dip /
squash-and-hop; the cloud's dark -> lit recolouring is a crossfade of the same drawing. All times come from the
narration chunks (a phrase inside a chunk is placed by its character index), with fallbacks if the text changes.
"""
import math
import random

import cv2
import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s10_repent as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import OUT_H, OUT_W
from engine.scene import Scene

SW, SH = 2800, 1575
INK = P["ink"]

GAP_X = 1640                 # where the cloud parts (right above the ziggurat)
ZIG_Y, ZIG_S = 1010, 0.42    # the great ziggurat (its base is hidden by the house rows)
SKY_Y = 930                  # far skyline ground line
ROW_A_Y, ROW_A_S = 1042, 0.29
ROW_B_Y, ROW_B_S = 1186, 0.38
STREET_Y = 1240              # ground line of the neighbours kneeling in the street beyond our parapet
PAR_TOP, PAR_FACE, PAR_BOT = 1240, 1257, 1336    # our parapet: top surface, inner face top, foot (floor starts)
FS = 1.35                    # family scale

f1 = V.f1


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def phrase_t(line, phrases, default):
    """Start time of the first of ``phrases`` found in ``line``: the chunk start plus the phrase's character
    offset inside that chunk (so it follows a re-generated voice)."""
    for ph in phrases:
        for c in line.chunks:
            i = c.text.find(ph)
            if i >= 0:
                n = max(1, len(c.text.rstrip("，。！？、：；")))
                return c.start + (c.end - c.start) * i / n
        if not line.chunks and ph in line.text:
            return line.start + (line.end - line.start) * line.text.find(ph) / max(1, len(line.text))
    return default


def cut_at(t, fps=30):
    """Snap a hard cut to the middle of a frame interval (no frame shows a half-way blend)."""
    return (math.floor(t * fps) + 0.5) / fps


# ============================================================================ sky & far city


def sky_gold_svg():
    defs = (S.lin_grad("s18skyw", [(0, "#bcdbe6"), (0.28, "#e6e1c8"), (0.55, "#fbe3b1"), (0.8, "#fff0cf"),
                                   (1, "#fff3d8")]) +
            S.rad_grad("s18sun", [(0, "#fff8dc", 1), (0.25, "#ffefb8", 0.85), (0.6, "#ffe09a", 0.35),
                                  (1, "#ffd98a", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_Y + 40}" fill="url(#s18skyw)"/>'
            f'<ellipse cx="{GAP_X}" cy="250" rx="940" ry="520" fill="url(#s18sun)"/>')
    return doc(body, defs)


def fair_clouds_svg():
    body = ""
    for cx, cy, w, h, seed in ((380, 170, 340, 104, 61), (1030, 100, 260, 84, 62), (2330, 130, 310, 98, 63),
                               (2690, 330, 240, 78, 64), (720, 400, 200, 64, 65)):
        body += S.cloud(cx, cy, w, h, "#fff6e2", seed=seed, sw=3, shade_fill="#f6d9a8")
    return doc(S.g(body, filter="wobble"))


def mountains_svg():
    """Faint blue mountains on the eastern horizon (aerial perspective)."""
    far = S.hill(-100, 1500, 800, 120, seed=7, bumps=4)
    far2 = S.hill(1200, 2950, 800, 150, seed=9, bumps=4)
    near = S.hill(-100, 2950, 825, 70, seed=12, bumps=7)
    body = (S.path(far, "#c9cbd6", sw=2.5) + S.path(far2, "#c4c6d4", sw=2.5)
            + S.path(near, "#d8d2cc", sw=2.5))
    snow = ""
    return doc(S.g(body + snow, filter="wobble", opacity=0.95))


def palm(x, y, s, lean=0.0):
    return PR.palm_tree(x, y, s, lean=lean)


# row B houses: (x, variant, facing). Gap around the ziggurat so the light lands in the middle of the city.
ROW_B = [(-60, 2, 1), (300, 0, 1), (640, 1, -1), (990, 3, 1), (1330, 0, -1), (1960, 2, 1), (2330, 3, -1),
         (2650, 0, 1), (2930, 1, -1)]
ROW_A = [(-40, 0, 1), (190, 2, -1), (430, 3, 1), (660, 0, -1), (880, 1, 1), (1120, 2, 1), (1350, 0, -1),
         (1930, 3, 1), (2150, 0, -1), (2380, 2, 1), (2620, 1, -1), (2850, 0, 1)]
ROOF_DY = {0: -510, 1: -845, 2: -524, 3: -594}


def city_svg():
    """Far skyline, the great ziggurat and two rows of houses with palms (static)."""
    defs = (S.lin_grad("s18haze", [(0, "#f1e2c4", 0), (1, "#f1e2c4", 0.5)]) +
            S.lin_grad("s18ground", [(0, "#e8d4aa"), (0.5, "#e2c899"), (1, "#d9bb88")]))
    body = PR.nineveh_skyline(-120, 2920, SKY_Y, scale=0.66, seed=5, haze=0.5)
    body += f'<rect x="-20" y="{SKY_Y - 200}" width="{SW + 40}" height="210" fill="url(#s18haze)"/>'
    # the city floor between the house rows (streets and yards seen from above)
    gy0, gy1 = SKY_Y - 6, PAR_TOP + 30
    ground = f'<rect x="-30" y="{gy0}" width="{SW + 60}" height="{gy1 - gy0}" fill="url(#s18ground)"/>'
    lanes = "".join(f'<path d="M-30,{y} L{SW + 30},{y}"/>' for y in (SKY_Y + 40, ROW_A_Y + 26, ROW_A_Y + 70, ROW_A_Y + 112))
    ground += f'<g stroke="{P["sand_dark"]}" stroke-width="2" opacity="0.28" fill="none">{lanes}</g>'
    body += S.g(ground, filter="wobble")
    body += PR.ziggurat(GAP_X, ZIG_Y, ZIG_S)
    # row A (farther) with palms behind
    rowa = ""
    for x, s, ln in ((70, 0.29, 0.1), (560, 0.32, -0.1), (1040, 0.28, 0.15), (1250, 0.32, -0.2), (2050, 0.3, 0.1),
                     (2520, 0.32, -0.1), (2760, 0.28, 0.2)):
        rowa += palm(x, ROW_A_Y - 10, s, ln)
    for x, v, fc in ROW_A:
        rowa += PR.house(x, ROW_A_Y, ROW_A_S, variant=v, facing=fc)
    body += f'<g opacity="1">{rowa}</g>'
    body += f'<rect x="-20" y="{ROW_A_Y - 120}" width="{SW + 40}" height="140" fill="url(#s18haze)" opacity="0.6"/>'
    # row B (nearer): palms in the open square in front of the ziggurat, houses
    rowb = ""
    for x, s, ln in ((1560, 0.44, -0.15), (1745, 0.4, 0.12), (1470, 0.36, 0.2), (1850, 0.35, -0.1),
                     (170, 0.38, 0.1), (2140, 0.39, -0.12)):
        rowb += palm(x, ROW_B_Y - 8, s, ln)
    for x, v, fc in ROW_B:
        rowb += PR.house(x, ROW_B_Y, ROW_B_S, variant=v, facing=fc)
    # the street in front of row B (between it and our parapet)
    street = (f'<path d="M-30,{ROW_B_Y - 4} L{SW + 30},{ROW_B_Y - 4} L{SW + 30},{PAR_TOP + 20} L-30,{PAR_TOP + 20} Z" '
              f'fill="#e3c796" stroke="{INK}" stroke-width="3"/>')
    street += (f'<g stroke="{P["ink_soft"]}" stroke-width="2" opacity="0.25" fill="none">'
               + "".join(f'<path d="M-30,{y} L{SW + 30},{y}"/>' for y in (ROW_B_Y + 14, ROW_B_Y + 34))
               + "</g>")
    # a well and a few jars in the street
    street += PR.jar(1385, ROW_B_Y + 14, 0.36) + PR.jar(1412, ROW_B_Y + 20, 0.3)
    street += PR.sack(2290, ROW_B_Y + 28, 0.32, seed=2)
    body += rowb + S.g(street, filter="wobble")
    return doc(body, defs)


# ============================================================================ our roof terrace


def terrace_svg():
    defs = (S.lin_grad("s18floor", [(0, "#dcbd8c"), (0.4, "#e7cb9a"), (1, "#ecd2a4")]) +
            S.lin_grad("s18par", [(0, "#d3ae78"), (1, "#c49c66")]) +
            S.lin_grad("s18hatch", [(0, "#5a3d2b"), (1, "#7a5638")]))
    out = ""
    # floor (plaster) with perspective joints converging on the ziggurat
    out += (f'<rect x="-30" y="{PAR_BOT}" width="{SW + 60}" height="{SH - PAR_BOT + 40}" fill="url(#s18floor)" '
            f'stroke="{INK}" stroke-width="4"/>')
    j = ""
    vx, vy = GAP_X, 760
    for i in range(-12, 16):
        xb = vx + i * 300
        t0 = (PAR_BOT - vy) / (SH + 40 - vy)
        xt = vx + (xb - vx) * t0
        j += f'<path d="M{f1(xt)},{PAR_BOT} L{f1(xb)},{SH + 40}"/>'
    y, k = PAR_BOT + 34, 0
    while y < SH + 20:
        j += f'<path d="M-30,{f1(y)} L{SW + 30},{f1(y)}"/>'
        k += 1
        y += 34 + k * 14
    out += f'<g stroke="{P["sand_dark"]}" stroke-width="2.4" opacity="0.32" fill="none">{j}</g>'
    # a few worn plaster patches and cracks
    rng = random.Random(4)
    for cx, cy, rx, ry in ((1560, 1400, 120, 16), (2050, 1530, 140, 22), (1480, 1550, 90, 16), (2560, 1420, 80, 14)):
        out += f'<path d="{S.blob(cx, cy, rx, ry, 0.2, 8, cx)}" fill="#f2dcb2" opacity="0.7"/>'
    for cx, cy in ((1620, 1480), (2290, 1390), (1820, 1540)):
        pts = [(cx + i * 18, cy + rng.uniform(-6, 6) + i * 3) for i in range(5)]
        out += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["sand_dark"]}" '
                f'stroke-width="2.5" opacity="0.6"/>')
    # parapet: top surface (seen slightly from above), inner face with brick courses
    par = (f'<path d="M-30,{PAR_TOP} L{SW + 30},{PAR_TOP} L{SW + 30},{PAR_FACE} L-30,{PAR_FACE} Z" fill="#ecd3a3" '
           f'stroke="{INK}" stroke-width="4"/>'
           f'<rect x="-30" y="{PAR_FACE}" width="{SW + 60}" height="{PAR_BOT - PAR_FACE}" fill="url(#s18par)" '
           f'stroke="{INK}" stroke-width="4"/>')
    br = ""
    yy, row = PAR_FACE + 22, 0
    while yy < PAR_BOT - 4:
        br += f'<path d="M-30,{yy} L{SW + 30},{yy}"/>'
        off = 0 if row % 2 else 40
        for x in range(-30 + off, SW + 30, 80):
            if rng.random() < 0.6:
                br += f'<path d="M{x},{yy - 22} L{x},{yy}"/>'
        yy += 22
        row += 1
    par += f'<g stroke="{P["sand_dark"]}" stroke-width="2" opacity="0.5" fill="none">{br}</g>'
    # plaster patches on the parapet and a drain spout
    for cx, cy in ((520, 1298), (1300, 1284), (2210, 1304)):
        par += f'<path d="{S.blob(cx, cy, 60, 18, 0.25, 8, cx + 7)}" fill="#e3c592" opacity="0.8"/>'
    out += par
    # ladder hatch at the front left (a ladder top pokes out of it)
    hx0, hx1, hy0 = 2620, 2820, 1500
    out += (f'<path d="M{hx0},{hy0} L{hx1},{hy0} L{hx1 + 40},{SH + 40} L{hx0 - 40},{SH + 40} Z" fill="url(#s18hatch)" '
            f'stroke="{INK}" stroke-width="4"/>')
    lad = ""
    for lx in (2672, 2774):
        lad += (f'<path d="M{lx},{SH + 40} L{lx + 6},{hy0 - 120}" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
                f'<path d="M{lx},{SH + 40} L{lx + 6},{hy0 - 120}" stroke="{P["wood"]}" stroke-width="13" '
                f'stroke-linecap="round"/>')
    for ry in (hy0 - 90, hy0 - 20, hy0 + 50):
        lad += (f'<path d="M{2676},{ry} L{2778},{ry}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
                f'<path d="M{2676},{ry} L{2778},{ry}" stroke="{P["wood_light"]}" stroke-width="8" stroke-linecap="round"/>')
    out += lad
    # reed mat under the family
    mx0, mx1, my0, my1 = 210, 1420, 1418, 1572
    mat = (f'<path d="M{mx0 + 40},{my0} L{mx1 - 10},{my0} L{mx1 + 30},{my1} L{mx0 - 20},{my1} Z" fill="#d9b86a" '
           f'stroke="{INK}" stroke-width="4"/>')
    stripes = ""
    for i in range(1, 9):
        u = i / 9
        stripes += (f'<path d="M{f1(mx0 + 40 + (mx1 - mx0 - 50) * u)},{my0 + 3} '
                    f'L{f1(mx0 - 20 + (mx1 - mx0 + 50) * u)},{my1 - 3}"/>')
    mat += f'<g stroke="#b8934a" stroke-width="3" fill="none" opacity="0.8">{stripes}</g>'
    mat += (f'<path d="M{mx0 + 26},{my0 + 30} L{mx1 + 2},{my0 + 30} M{mx0 + 6},{my1 - 34} L{mx1 + 18},{my1 - 34}" '
            f'stroke="{P["terracotta"]}" stroke-width="7" opacity="0.8"/>')
    out += mat
    # pots and a basket along the parapet, a bedroll
    deco = (PR.jar(1545, 1370, 0.7) + PR.jar(1625, 1392, 0.54, color="#c46f48")
            + PR.sack(2240, 1408, 0.66, seed=5) + PR.rope_coil(1745, 1404, 0.64))
    return doc(S.g(out, filter="wobble") + deco, defs)


DOVECOTE_X, DOVECOTE_Y = 2430, 1452
DC_K = 1.25
DC_TOP = DOVECOTE_Y - 380 * DC_K


def dovecote_svg():
    """A little mud-brick dove tower on the roof: tapered, rows of round holes with stick perches, domed top."""
    k = DC_K
    x, y = DOVECOTE_X, DOVECOTE_Y
    top = DOVECOTE_Y - 380
    w0, w1 = 130, 100        # half widths at the base and the top (drawn at k = 1, scaled about the base)
    col = "#dcb984"
    out = (f'<path d="M{x - w0},{y} L{x - w1},{top + 40} L{x + w1},{top + 40} L{x + w0},{y} Z" fill="{col}" '
           f'stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    # shade on the right side
    out += (f'<path d="M{x + 40},{y - 4} L{x + 34},{top + 44} L{x + w1 - 4},{top + 44} L{x + w0 - 4},{y - 4} Z" '
            f'fill="{S.shade(col, -0.12)}" opacity="0.6"/>')
    # terracotta band and a cornice
    out += (f'<path d="M{x - w1 - 6},{top + 72} L{x + w1 + 6},{top + 72} L{x + w1 + 8},{top + 96} '
            f'L{x - w1 - 8},{top + 96} Z" fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3.5"/>')
    out += (f'<rect x="{x - w1 - 18}" y="{top + 28}" width="{2 * w1 + 36}" height="18" rx="6" fill="#ecd3a3" '
            f'stroke="{INK}" stroke-width="4"/>')
    # domed top with a knob
    out += (f'<path d="M{x - w1 + 4},{top + 30} C{x - w1 + 10},{top - 52} {x + w1 - 10},{top - 52} {x + w1 - 4},{top + 30} Z" '
            f'fill="{S.shade(col, 0.1)}" stroke="{INK}" stroke-width="4.5"/>'
            f'<circle cx="{x}" cy="{top - 34}" r="11" fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3.5"/>')
    # rows of holes with perches
    for r, (yy, n) in enumerate(((top + 140, 3), (top + 215, 4), (top + 290, 4))):
        half = w1 + (w0 - w1) * (yy - top - 40) / (y - top - 40) - 26
        for i in range(n):
            hx = x - half + 2 * half * (i + 0.5) / n
            out += (f'<path d="M{f1(hx - 13)},{yy} L{f1(hx - 13)},{yy - 16} A13,13 0 0 1 {f1(hx + 13)},{yy - 16} '
                    f'L{f1(hx + 13)},{yy} Z" fill="#5a3d2b" stroke="{INK}" stroke-width="3"/>')
            out += (f'<path d="M{f1(hx - 22)},{yy + 6} L{f1(hx + 22)},{yy + 6}" stroke="{INK}" stroke-width="8" '
                    f'stroke-linecap="round"/><path d="M{f1(hx - 22)},{yy + 6} L{f1(hx + 22)},{yy + 6}" '
                    f'stroke="{P["wood_light"]}" stroke-width="4" stroke-linecap="round"/>')
    # a few bricks
    rng = random.Random(8)
    for _ in range(9):
        bx, by = x + rng.uniform(-90, 60), rng.uniform(top + 110, y - 30)
        out += (f'<rect x="{f1(bx)}" y="{f1(by)}" width="30" height="13" rx="3" fill="none" '
                f'stroke="{S.shade(col, -0.2)}" stroke-width="2" opacity="0.7"/>')
    out = f'<g transform="translate({x},{y}) scale({k}) translate({-x},{-y})">{out}</g>'
    return C.ground_shadow(x, y, 1.2 * k, 280, opacity=0.2) + S.g(out, filter="wobble-fine")


def foreground_svg():
    """Static framing: potted plants and jars in the bottom corners."""
    body = (PR.bush(2770, SH + 8, 1.05, variant=1) + PR.jar(2600, SH - 46, 0.9) + PR.jar(2680, SH - 20, 0.66)
            + PR.grass_tuft(2470, SH + 4, 1.0, variant=2)
            + PR.bush(-10, SH + 16, 0.95, variant=3) + PR.grass_tuft(330, SH + 6, 0.9, variant=0))
    return doc(body)


# ============================================================================ people


def person(kind, variant, x, y, s, facing, state):
    """state: 'pray' (kneeling, eyes closed), 'peek' (kneeling, eyes open), 'wonder' (kneeling, looking up,
    surprised), 'glad' (kneeling, happy), 'cheer' (standing, arms up, happy)."""
    pose, expr = {"pray": ("kneel_pray", None), "peek": ("kneel_pray", "neutral"),
                  "wonder": ("kneel_pray", "surprised"), "glad": ("kneel_pray", "happy"),
                  "cheer": ("cheer", "happy")}[state]
    child = kind == "child"
    sh_w = (90 if state == "cheer" else 130) if child else (120 if state == "cheer" else 175)
    return (C.ground_shadow(x, y, s, sh_w, opacity=0.2)
            + C.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, attire="sackcloth", expr=expr))


# the family on our roof: name -> (kind, variant, x, y, facing, z)
FAMILY = {
    "grandpa": ("elder", 1, 405, 1466, 1, 30.0),
    "father": ("man", 2, 636, 1476, 1, 30.2),
    "girl": ("child", 1, 832, 1516, 1, 31.0),
    "mother": ("woman", 3, 1062, 1472, 1, 30.4),
    "boy": ("child", 0, 1270, 1512, 1, 31.2),
}

# neighbours: in the street beyond the parapet and kneeling on the roofs of row B
STREET = {
    "st_l": [("woman", 0, 1440, STREET_Y, 0.44, 1), ("man", 3, 1508, STREET_Y + 4, 0.44, 1),
             ("child", 2, 1566, STREET_Y + 6, 0.44, 1)],
    "st_c": [("elder", 2, 1700, STREET_Y, 0.44, -1), ("man", 0, 1768, STREET_Y + 4, 0.44, -1),
             ("woman", 1, 1838, STREET_Y + 2, 0.44, -1), ("child", 3, 1898, STREET_Y + 6, 0.44, -1)],
    "st_r": [("man", 1, 2010, STREET_Y + 2, 0.44, -1), ("woman", 2, 2082, STREET_Y + 4, 0.44, -1),
             ("elder", 3, 2155, STREET_Y, 0.44, -1)],
}


def roof_people():
    """Little groups kneeling on the roofs of row B: name -> members."""
    out = {}
    picks = {1: ("man", 1, "woman", 0), 3: ("elder", 0, "child", 1), 4: ("woman", 2, "man", 3),
             5: ("man", 0, "child", 2), 6: ("woman", 1, "elder", 2), 2: ("child", 0, "woman", 3)}
    s = 0.31
    for i, (k1, v1, k2, v2) in picks.items():
        x, v, fc = ROW_B[i]
        ry = ROW_B_Y + ROOF_DY[v] * ROW_B_S + 2
        cx = x - 40 * ROW_B_S * fc
        f = 1 if x < GAP_X else -1
        out[f"roof{i}"] = [(k1, v1, cx - 26, ry, s, f), (k2, v2, cx + 26, ry + 1, s, f)]
    return out


# ============================================================================ light


def light_fx(gloom_a, hole_r, gap, warm_a, glow_a, glow_s, glow_c, glow_r=(900, 520)):
    """One cheap output-space pass (instead of three full-frame glaze layers, see the render budget):

    * gloom: a cool multiply glaze under the heavy cloud (strongest at the top of the frame). From God's mercy
      on it lifts outward from the cloud gap: a soft elliptical hole of radius hole_r(t) (stage px) centred on
      ``gap`` lets the light spread over the city, while gloom_a(t) thins what is left;
    * warm: a light golden multiply glaze, warm_a(t);
    * glow: a warm screen glow over the roofs where the rays land (glow_c, radii glow_r * glow_s(t)), glow_a(t).
    The maps are computed on a 1/8-resolution grid and upsampled (they are all soft).
    """
    f = 8
    gw, gh = OUT_W // f, OUT_H // f
    X, Y = np.meshgrid((np.arange(gw) + 0.5) * f, (np.arange(gh) + 0.5) * f)
    v = (Y / OUT_H)[..., None]
    gstr = np.interp(Y / OUT_H, [0, 0.4, 0.7, 1.0], [0.62, 0.55, 0.36, 0.22])[..., None]
    top, bot = np.array([0x8d, 0x90, 0xad]) / 255.0, np.array([0xb4, 0xb1, 0xc0]) / 255.0
    gdark = gstr * (1 - (top * (1 - v) + bot * v))           # darkening per channel at full gloom
    wdark = 0.14 * (1 - np.array([255, 223, 174]) / 255.0)
    gcol = np.array([255, 196, 92], np.float64)

    def up(small):
        return cv2.resize(small, (OUT_W, OUT_H), interpolation=cv2.INTER_LINEAR)

    def fx(frame, t, view):
        ag, aw, al = gloom_a(t), warm_a(t), glow_a(t)
        if ag <= 0.003 and aw <= 0.003 and al <= 0.003:
            return frame
        arr = np.array(frame)                                 # RGBA uint8 copy
        if ag > 0.003 or aw > 0.003:
            mult = np.ones((gh, gw, 3))
            if ag > 0.003:
                d = gdark * ag
                R = hole_r(t) * view.scale
                if R > 1:
                    cx, cy = view.to_out(*gap)
                    dist = np.sqrt(((X - cx) / 1.35) ** 2 + (Y - cy) ** 2)
                    hole = np.clip((R - dist) / (0.6 * R + 60) + 0.5, 0, 1)
                    d = d * (1 - hole)[..., None]
                mult *= 1 - d
            if aw > 0.003:
                mult *= 1 - wdark * aw
            m8 = np.full((gh, gw, 4), 255, np.uint8)
            m8[..., :3] = np.clip(mult * 255 + 0.5, 0, 255)
            arr = cv2.multiply(arr, up(m8), scale=1 / 255.0)
        if al > 0.003:
            cx, cy = view.to_out(*glow_c)
            k = glow_s(t) * view.scale
            r = np.sqrt(((X - cx) / (glow_r[0] * k)) ** 2 + ((Y - cy) / (glow_r[1] * k)) ** 2)
            a = np.interp(r, [0, 0.45, 1.0], [0.5, 0.26, 0.0]) * al
            s8 = np.zeros((gh, gw, 4), np.uint8)
            s8[..., :3] = np.clip(gcol * a[..., None] + 0.5, 0, 255)
            arr = cv2.subtract(255, cv2.multiply(cv2.subtract(255, arr), cv2.subtract(255, up(s8)), scale=1 / 255.0))
        return Image.fromarray(arr, "RGBA")
    return fx


# cloud colours: v1's pre-darkened greys divided by the gloom they now sit under (the gloom is applied after
# all layers by light_fx); the lit colours are v1's
CLOUD_DARK = {"back": ("#8a8ea0", "#6d7085"), "front": ("#7f8396", "#64677b"), "low": ("#7b7f92", "#606377")}


def bank_frames(items, kind, rect=None):
    out = []
    for fill, shade in (CLOUD_DARK[kind], V.CLOUD_LIT[kind]):
        extra = ""
        if rect:
            x0, x1, y1 = rect
            extra = f'<rect x="{x0}" y="-40" width="{x1 - x0}" height="{y1 + 40}" fill="{fill}"/>'
        out.append(V.cloud_bank_svg(items, fill, shade, extra=extra))
    return out


# grey cloud banks over the city: (items, kind, rect)
BANKS = {
    "back_l": ([(240, 60, 920, 360, 71), (900, 30, 860, 330, 72), (260, 300, 760, 300, 83)], "back",
               (-40, 1240, 230)),
    "back_r": ([(2440, 50, 960, 350, 73), (2790, 90, 620, 300, 74), (2700, 300, 640, 280, 84)], "back",
               (2020, 2900, 230)),
    "back_c": ([(GAP_X, 120, 860, 360, 75)], "back", (1260, 2020, 160)),
    "front_l": ([(1080, 250, 1060, 380, 76)], "front", (560, 1580, 190)),
    "front_r": ([(2230, 260, 1020, 360, 77)], "front", (1740, 2900, 190)),
    "low_l": ([(380, 560, 700, 220, 78), (1060, 560, 660, 230, 79)], "low", None),
    "low_r": ([(2200, 555, 720, 225, 80), (2760, 575, 500, 200, 81)], "low", None),
    "low_c": ([(GAP_X, 530, 560, 210, 82)], "low", None),
}


# ============================================================================ doves


DOVE_REF = V.DOVE_REF


def dove_frames(facing, scale=0.85, perched=False):
    fr = [doc(PR.dove(DOVE_REF[0], DOVE_REF[1], scale, facing, wing=w)) for w in V.WINGS]
    if perched:
        fr = [doc(PR.dove(DOVE_REF[0], DOVE_REF[1] + 0, scale, facing, pose="stand"))] + fr
    return fr


def perch_wings(t_off, rate, phase, glide_from):
    """Frame index for a perched dove: 0 (standing) until t_off, then the wing cycle (frames 1..5)."""
    cyc = V.wing_cycle(rate, phase, glide_from)

    def fa(t):
        if t < t_off:
            return 0.0
        return 1.0 + cyc(t)
    return fa


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    l0 = L[0]
    l1 = L[1] if len(L) > 1 else None

    # ---- timing (all from the narration) ----
    t_see = l0.start
    t_mercy = phrase_t(l0, ("可怜", "怜悯"), l0.start + 0.45 * (l0.end - l0.start))
    t_spared = phrase_t(l0, ("没有",), t_mercy + 0.45 * (l0.end - t_mercy))
    if l1 is not None:
        t_whole = l1.start
        t_peace = phrase_t(l1, ("都得到", "平安"), l1.start + 0.5 * (l1.end - l1.start))
    else:
        t_whole = l0.end + 0.3
        t_peace = min(T - 2.0, t_whole + 1.4)
    t_peek = t_see + 0.55 * (t_mercy - t_see)
    t_gold0, t_gold1 = t_mercy + 0.3, t_spared + 1.2       # sky turns gold
    t_wonder = t_mercy + 0.3                                # the family looks up into the light
    t_glad = t_spared + 0.1                                 # relief and joy
    t_cheer0 = t_whole + 0.15                               # the city cheers, from the centre outward

    # ---- sky and city: one static group (the grey of the storm comes from the gloom in light_fx) ----
    sc.add("sky", sky_gold_svg(), z=0, wc=0.6)
    sc.add("mountains", mountains_svg(), z=1.5)
    sc.add("city", city_svg(), z=2)
    sc.add("fair", fair_clouds_svg(), z=2.4, motion=M.combine(
        M.keys([(t_spared + 0.9, {"alpha": 0}), (t_spared + 2.2, {"alpha": 1})], "sine"), M.drift(vx=5, t0=t_spared)))

    # ---- neighbours on the roofs and in the street: pray -> glad (wave from the centre) -> cheer ----
    def dist_delay(gx, k=0.00045):
        return abs(gx - GAP_X) * k

    def add_group(name, members, z, base_glad, base_cheer):
        frames = [doc("".join(person(*m, state=st) for m in members)) for st in ("pray", "glad", "cheer")]
        xs = [m[2] for m in members]
        gx, gy = sum(xs) / len(xs), max(m[3] for m in members)
        s = members[0][4]
        tg = base_glad + dist_delay(gx) * 2.2
        tc = cut_at(base_cheer + dist_delay(gx) * 2.4)
        lift = V.hop(tg, [(-0.1, {"dy": 0}), (0, {"dy": 3 * s}), (0.16, {"dy": -6 * s}), (0.32, {"dy": 0})],
                     (gx, gy), ["in", "out", "sine"])
        jump = V.hop(tc, [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 8 * s, "sy": 0.93}), (0.18, {"dy": -30 * s, "sy": 1.03}),
                          (0.36, {"dy": 0, "sy": 1}), (0.9, {"dy": 0}), (1.06, {"dy": -16 * s}), (1.22, {"dy": 0})],
                     (gx, gy), ["in", "out", "in", "linear", "out", "in"])
        sc.add(name, frames, z=z, frame_at=V.sched([(0, 0), (cut_at(tg), 1), (tc, 2)], fade=0.0),
               motion=M.combine(lift, jump, M.breathe(0.01, 3.1, pivot=(gx, gy), phase=len(name) * 0.17)))

    for i, (name, members) in enumerate(roof_people().items()):
        add_group(name, members, 3 + 0.01 * i, t_glad + 0.2, t_cheer0)
    for i, (name, members) in enumerate(STREET.items()):
        add_group(name, members, 4 + 0.01 * i, t_glad + 0.05, t_cheer0 + 0.1)

    # ---- our roof ----
    sc.add("terrace", terrace_svg(), z=10)
    sc.add("dovecote", doc(dovecote_svg()), z=10.5)
    sc.add("foreground", foreground_svg(), z=38)

    # animals in sackcloth on the roof
    def animal_layer(name, kind, x, y, s, facing, z, hop_t, per=2.6, ph=0.0):
        body = C.ground_shadow(x, y, s, 230, opacity=0.2) + PR.animal(x, y, s, facing, kind=kind, sackcloth=True)
        parts = [M.breathe(0.012, per, pivot=(x, y), phase=ph),
                 M.keys([(hop_t, {"dy": 0}), (hop_t + 0.16, {"dy": -26 * s}), (hop_t + 0.34, {"dy": 0}),
                         (hop_t + 0.52, {"dy": -14 * s}), (hop_t + 0.68, {"dy": 0})], ["out", "in", "out", "in"])]
        sc.add(name, doc(body), z=z, motion=M.combine(*parts))

    animal_layer("goat", "goat", 2190, 1410, 0.82, -1, 29.0, t_peace + 0.45, per=2.5, ph=0.2)
    animal_layer("lamb", "sheep", 2000, 1436, 0.82, -1, 29.5, t_peace + 0.2, per=2.2, ph=0.6)

    # the family
    fam_wonder = {"grandpa": 0.3, "father": 0.15, "girl": 0.0, "mother": 0.22, "boy": 0.08}
    fam_glad = {"grandpa": 0.35, "father": 0.2, "girl": 0.05, "mother": 0.12, "boy": 0.0}
    fam_cheer = {"girl": 0.0, "boy": 0.14, "father": 0.32}
    for name, (kind, v, x, y, fc, z) in FAMILY.items():
        states = ["pray"]
        sched = [(0, 0)]
        if name == "girl":
            states.append("peek")
            sched.append((cut_at(t_peek), len(states) - 1))
        tw = cut_at(t_wonder + fam_wonder[name])
        tg = cut_at(t_glad + fam_glad[name])
        states.append("wonder")
        sched.append((tw, len(states) - 1))
        states.append("glad")
        sched.append((tg, len(states) - 1))
        tc = None
        if name in fam_cheer:
            tc = cut_at(t_peace + fam_cheer[name])
            states.append("cheer")
            sched.append((tc, len(states) - 1))
        frames = [doc(person(kind, v, x, y, FS, fc, st)) for st in states]
        pv = (x, y)
        parts = [M.breathe(0.009, 3.0, pivot=pv, phase=len(name) * 0.21)]
        lift = [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 4, "sy": 0.975}), (0.16, {"dy": -7, "sy": 1.015}),
                (0.34, {"dy": 0, "sy": 1})]
        for t_c in [e[0] for e in sched[1:]]:
            if t_c != tc:
                parts.append(V.hop(t_c, lift, pv, ["in", "out", "sine"]))
        if tc is not None:
            kid = kind == "child"
            big = 40 if kid else 16
            seq = [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 8, "sy": 0.93}), (0.2, {"dy": -big, "sy": 1.03}),
                   (0.4, {"dy": 0, "sy": 1})]
            if kid:      # extra joy hops, all finished before the calm last second
                for t_a, hgt in ((0.75, 26), (1.55, 16)):
                    if tc + t_a + 0.32 < T - 1.05:
                        seq += [(t_a, {"dy": 0}), (t_a + 0.16, {"dy": -hgt}), (t_a + 0.32, {"dy": 0})]
            parts.append(V.hop(tc, seq, pv, ["in", "out", "in"] + ["linear", "out", "in"] * 2))

        sc.add(name, frames, z=z, frame_at=V.sched(sched, fade=0.0), motion=M.combine(*parts))

    # ---- doves: four perched on the dovecote burst out on "整座尼尼微城", two rise from the roofs earlier ----
    k = DC_K
    perched = [  # (x, y body centre when perched, facing, flight [(dt, dx, dy)], rate, phase)
        (DOVECOTE_X - 34 * k, DC_TOP - 40 * k - 30, -1,
         [(0, 0, 0), (0.7, -260, -300), (2.0, -820, -560), (4.5, -1700, -800)], 11, 0.0),
        (DOVECOTE_X + 44 * k, DC_TOP - 26 * k - 30, 1,
         [(0, 0, 0), (0.8, 180, -330), (2.2, 120, -700), (4.5, -400, -900)], 12, 0.3),
        (DOVECOTE_X - 76 * k, DC_TOP + 146 * k - 30, -1,
         [(0, 0, 0), (0.7, -300, -220), (2.1, -1000, -420), (4.5, -2000, -600)], 12.5, 0.6),
        (DOVECOTE_X + 74 * k, DC_TOP + 221 * k - 30, 1,
         [(0, 0, 0), (0.8, 200, -300), (2.3, -100, -700), (4.5, -900, -950)], 11.5, 0.2),
    ]
    fr_pl, fr_pr = dove_frames(-1, 0.85, True), dove_frames(1, 0.85, True)
    for i, (px, py, fc, path, rate, ph) in enumerate(perched):
        t_off = t_whole + 0.08 + 0.12 * i
        pts = [(t_off + dt, px + dx, py + dy) for dt, dx, dy in path]
        pts = [(t_off - 0.01, px, py)] + pts[1:]
        sc.add(f"dove{i}", fr_pl if fc < 0 else fr_pr, z=34 + 0.01 * i, seed=900 + (fc > 0),
               frame_at=perch_wings(t_off, rate, ph, T - 1.6),
               motion=M.combine(V.flight(pts, DOVE_REF),
                                lambda t, a=t_off, p=ph: Tf(dy=1.5 * math.sin(2 * math.pi * (t / 1.3 + p))) if t < a
                                else Tf()))
    fr_l, fr_r = V.dove_frames(-1), V.dove_frames(1)
    far_doves = [  # (facing, [(t, x, y)], rate, phase, scale)
        (-1, [(t_spared + 0.5, 1900, 960), (t_spared + 1.6, 1700, 700), (t_whole + 1.0, 1350, 520), (T, 900, 360)], 12, 0.1),
        (1, [(t_spared + 0.8, 1420, 980), (t_spared + 1.9, 1560, 740), (t_whole + 1.2, 1900, 570), (T, 2300, 400)], 13, 0.5),
        (-1, [(t_whole + 0.4, 1100, 940), (t_whole + 1.4, 1000, 700), (T, 700, 480)], 12, 0.8),
    ]
    for i, (fc, pts, rate, ph) in enumerate(far_doves):
        ta = pts[0][0]
        sc.add(f"fdove{i}", fr_l if fc < 0 else fr_r, z=2.5 + 0.01 * i, seed=910 + (fc > 0),
               frame_at=V.wing_cycle(rate, ph, glide_from=T - 2.0),
               motion=M.combine(V.flight(pts, DOVE_REF),
                                M.keys([(ta - 0.01, {"alpha": 0, "s": 0.4}), (ta + 0.25, {"alpha": 1, "s": 0.62})],
                                       "out", pivot=DOVE_REF),
                                M.bob(6, 0.9, phase=ph, axis="y")))

    # ---- golden light behind the cloud: kindles while God sees, bursts through the gap ----
    sc.add("gleam", V.gleam_svg(GAP_X, 330, 280, 360), z=40.1, wc=0, motion=M.combine(
        M.keys([(0, {"alpha": 0.3, "sx": 0.5, "sy": 0.6}), (t_see, {"alpha": 0.3, "sx": 0.5, "sy": 0.6}),
                (t_mercy - 0.1, {"alpha": 0.85, "sx": 0.8, "sy": 0.85}),
                (t_mercy + 0.6, {"alpha": 1, "sx": 1.1, "sy": 1.05}),
                (t_spared + 0.2, {"alpha": 0.85, "sx": 1.22, "sy": 1.12}),
                (t_spared + 1.4, {"alpha": 0, "sx": 1.3, "sy": 1.16})],
               ["sine", "sine", "out", "sine", "sine"], pivot=(GAP_X, 200)),
        M.pulse(0.88, 1.0, 2.6)))

    # ---- the heavy grey cloud: churns, catches light, parts at the gap, drifts apart and dissolves ----
    lit_c = lambda t: 0.2 + 0.8 * M.progress(t, t_see + 0.3, t_mercy + 0.3, "sine")   # the centre warms first
    lit = lambda t: M.progress(t, t_mercy - 0.6, t_mercy + 1.4, "sine")

    def cloud_motion(part_dx, go_dx, go_dy, t_go1, fade0, fade1, drift, pivot, s1=1.06, part_dy=0, churn=0.0):
        return M.combine(
            M.keys([(t_mercy, {"dx": 0, "dy": 0, "s": 1.0}), (t_mercy + 0.6, {"dx": part_dx, "dy": part_dy, "s": 1.0}),
                    (t_go1, {"dx": go_dx, "dy": go_dy, "s": s1})], ["out", "sine"], pivot=pivot),
            M.keys([(fade0, {"alpha": 1}), (fade1, {"alpha": 0})], "sine"),
            M.drift(vx=drift),
            M.bob(churn, 5.5, phase=pivot[0] / 977.0, axis="y") if churn else None,
            M.bob(churn * 2.2, 7.5, phase=pivot[0] / 1311.0, axis="x") if churn else None)

    dur = max(1.6, l0.end - t_mercy)                     # the cloud dissolves over the whole phrase
    plan = {  # name: (z, part_dx, go_dx, go_dy, go_end, fade0, fade1, drift, pivot, s1, part_dy)
        "back_l": (40.2, -20, -420, -180, 0.62, 0.42, 0.66, -3, (560, 80), 1.06, 0),
        "back_r": (40.21, 25, 420, -170, 0.62, 0.42, 0.66, 3, (2500, 80), 1.06, 0),
        "back_c": (40.22, 0, 0, -150, 0.35, 0.0, 0.2, 0, (GAP_X, 120), 1.3, -40),
        "low_l": (40.3, -40, -300, -170, 0.7, 0.36, 0.7, -2, (760, 560), 1.04, -10),
        "low_r": (40.31, 40, 300, -160, 0.7, 0.36, 0.7, 2, (2400, 560), 1.04, -10),
        "low_c": (40.32, 0, 0, -230, 0.3, 0.0, 0.17, 0, (GAP_X, 530), 1.35, -60),
        "front_l": (40.4, -110, -540, -220, 0.85, 0.5, 0.82, -3, (1080, 250), 1.06, 0),
        "front_r": (40.41, 110, 540, -200, 0.85, 0.5, 0.82, 3, (2230, 260), 1.06, 0),
    }
    for name, (z, pdx, gdx, gdy, ge, f0, f1_, dr, pv, s1, pdy) in plan.items():
        items, kind, rect = BANKS[name]
        fa = lit_c if name.endswith("_c") else lit
        sc.add(f"cloud_{name}", bank_frames(items, kind, rect), z=z, frame_at=fa,
               motion=cloud_motion(pdx, gdx, gdy, t_mercy + ge * dur, t_mercy + f0 * dur, t_mercy + f1_ * dur,
                                   dr, pv, s1, pdy, churn=5.0))

    # ---- God's mercy: golden rays pour down through the gap ----
    rsrc = (GAP_X, 330)
    sc.add("rays", V.rays_svg(rsrc, 92, 97, n=11, length=1600, seed=6), z=41, wc=0, blend="add",
           motion=M.combine(M.keys([(t_mercy + 0.05, {"alpha": 0, "sx": 0.4, "sy": 0.3}), (t_mercy + 0.75, {"alpha": 1}),
                                    (t_spared + 0.8, {"sx": 1.0, "sy": 1.0}), (t_whole + 1.5, {"alpha": 0.4})],
                                   ["sine", "out", "sine"], pivot=rsrc),
                            M.pulse(0.8, 1.0, 3.2), M.sway(1.0, 7.0, rsrc)))
    # gloom lifting outward from the gap, warm glaze, warm glow spreading over the roofs (see light_fx)
    gloom_a = M.keys([(t_mercy, {"alpha": 1}), (t_gold1 + 0.3, {"alpha": 0})], "sine")
    hole = M.keys([(t_mercy + 0.1, {"s": 0}), (t_mercy + 0.9, {"s": 500}), (t_gold1, {"s": 3400})], ["out", "sine"])
    warm_a = M.keys([(t_gold0, {"alpha": 0}), (t_gold1 + 0.4, {"alpha": 1})], "sine")
    glow = M.combine(M.keys([(t_mercy + 0.3, {"alpha": 0, "s": 0.25}), (t_spared, {"alpha": 0.75, "s": 0.8}),
                             (t_whole + 0.6, {"alpha": 0.36, "s": 1.7}), (T, {"alpha": 0.28, "s": 1.9})],
                            ["out", "sine", "sine"]), M.pulse(0.9, 1.0, 3.0))
    light = light_fx(lambda t: gloom_a(t).alpha, lambda t: hole(t).sx, (GAP_X, 500), lambda t: warm_a(t).alpha,
                     lambda t: glow(t).alpha, lambda t: glow(t).sx, (GAP_X, 1020))

    # ---- camera: close over the praying roof, a little up toward the light, then the whole city ----
    sc.camera = M.cam_keys([
        (0, Cam(1265, 902, 2290)),
        (t_mercy, Cam(1340, 888, 2250)),
        (t_spared + 1.2, Cam(1390, 858, 2400)),
        (t_whole + 2.6, Cam(1400, 789, 2756)),
        (T, Cam(1400, 787, 2760)),
    ], ["sine", "inout", "inout", "sine"])

    # ---- effects ----
    sc.fx = [
        light,
        FX.sparkles((200, 300, 2600, 1150), count=34, t0=t_gold0 + 0.6, t1=T + 1, color=(255, 238, 172),
                    size=(9, 20), drift=-10, seed=31),
        FX.sparkles((300, 600, 2500, 1250), count=26, t0=t_peace - 0.2, t1=T + 1, color=(255, 230, 150),
                    size=(8, 17), drift=-14, seed=37, period=1.3),
        FX.motes((100, 150, 2700, 1400), count=40, t0=t_gold0 + 0.4, t1=T + 1, color=(255, 240, 200),
                 size=(3, 7), alpha=140, seed=41),
    ]

    # ---- sound ----
    sc.sfx("wind_soft", 0, dur=t_spared + 1.5, gain_db=-17, fade_in=0.8, fade_out=1.5)
    sc.sfx("chime", t_mercy, gain_db=-8)
    sc.sfx("sparkle", t_mercy + 0.9, gain_db=-12)
    sc.sfx("birds", t_spared + 0.3, dur=T - t_spared - 0.3 + 0.8, gain_db=-13, fade_in=1.2, fade_out=0.8)
    sc.sfx("whoosh", t_whole + 0.08, gain_db=-17)
    sc.sfx("cheer", t_cheer0, dur=T - t_cheer0 + 0.8, gain_db=-15, fade_in=0.9, fade_out=0.8)
    sc.sfx("sparkle", t_peace, gain_db=-13)
    sc.sfx("sheep", t_peace + 0.25, gain_db=-12, pan=0.4)
    return sc
