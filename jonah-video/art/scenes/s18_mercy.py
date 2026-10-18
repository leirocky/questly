"""Scene 18 — God has mercy on Nineveh (Jonah 3:10), v2.

"上帝看见他们真的改掉了坏行为，就可怜他们，没有毁灭这座城。 / 整座尼尼微城，都得到了平安！"

One 2800 x 1575 stage, no cuts: a wide view over the whole city of Nineveh from a family's flat mud-brick roof.
Foreground: the roof terrace (a reed mat, a ladder hatch, pots, a dovecote with doves, a lamb and a goat in
sackcloth blankets) where a family in sackcloth kneels in prayer as a group - the girl in front of grandpa,
mother holding the boy close, father a step back. Beyond the low parapet: the street below (only the heads and
shoulders of the neighbours kneeling there show over our wall), rows of flat roofs (people praying on them too),
an open square in the middle of the city full of kneeling people, palms, the great ziggurat (small, far off on
the left - the light never falls on it), the far city with its wall, and blue mountains on the horizon. A heavy
overcast cloud hangs low over the whole city (adapted from the approved v1 s10 ending: cloud banks, gleam, rays).

  line 0  "上帝看见他们真的改掉了坏行为，"  overcast and calm, everyone kneels with eyes closed. God sees: the
                                          middle of the cloud, right above the square of praying people,
                                          warms to gold, a golden seam glows along its lower edge, the gloom
                                          under it thins and a few sparkles drift down (never a figure); the
                                          girl peeks up at it. The camera opens on the low overcast over the
                                          roofs of the city (no big figure in frame, so nobody from s17's
                                          street of praying families shows twice in the dissolve), tilts down
                                          and pulls back onto our praying roof (nearly settled as the girl
                                          peeks) and drifts slowly over the roof.
          "就可怜他们，"                    the middle cloud splits into two halves that slide apart (chime),
                                          golden light pours down in rays over the square, the homes and our
                                          roof, the gloom lifts; the family tilts up to look into the light.
          "没有毁灭这座城。"                the cloud banks, opaque, are pushed aside by the light: they slide outward
                                          and roll up and away off the frame; the sky turns gold, the warm
                                          light spreads over all the roofs; faces turn to relief and joy, the
                                          neighbours on the roofs, in the square and in the street smile up;
                                          doves take off from the roofs.
  line 1  "整座尼尼微城，"                  one continuous camera pull-out to the whole city: the doves burst from
                                          the dovecote and circle over the roofs; people all over the city stand
                                          up and cheer in a wave from the centre outward.
          "都得到了平安！"                  the children jump and cheer (left of the subtitle box), father raises
                                          his arms, the lamb and the goat hop; sparkles twinkle over the city;
                                          a soft blue comes back at the top of the sky. Calm, joyful hold.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a small dip /
squash-and-hop; the clouds' dark -> lit recolouring is a crossfade of the same drawing. All times come from the
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

GAP_X = 1640                 # where the cloud parts: right above the open square full of kneeling people
ZIG_X, ZIG_Y, ZIG_S = 420, 985, 0.32    # the great ziggurat, far off on the left (base hidden by row A)
SKY_Y = 930                  # far skyline ground line
ROW_A_Y, ROW_A_S = 1042, 0.29
ROW_B_Y, ROW_B_S = 1186, 0.38
SQUARE_Y = 1162              # ground line of the people kneeling in the open square (between row A and row B)
STREET_Y = 1304              # the street below, beyond our parapet: our wall hides the neighbours below the chest
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


def sky_blue_svg():
    """Soft clear blue that comes back at the top of the sky at the end (eases the dissolve into s19)."""
    defs = (S.lin_grad("s18skyb", [(0, "#a6d2e6", 0.95), (0.45, "#b8dbe8", 0.6), (1, "#c8e2ea", 0)]) +
            S.rad_grad("s18skyh", [(0, "#ffffff", 1), (0.55, "#ffffff", 0.75), (1, "#ffffff", 0)]))
    mask = (f'<mask id="s18skym" maskUnits="userSpaceOnUse" x="-20" y="-20" width="{SW + 40}" height="560">'
            f'<rect x="-20" y="-20" width="{SW + 40}" height="560" fill="#ffffff"/>'
            f'<ellipse cx="{GAP_X}" cy="120" rx="760" ry="420" fill="#000000" opacity="0.8" filter="url(#blur-lg)"/>'
            f'</mask>')
    body = f'<rect x="-20" y="-20" width="{SW + 40}" height="540" fill="url(#s18skyb)" mask="url(#s18skym)"/>'
    return doc(body, defs + mask)


def fair_clouds_svg():
    """Fair-weather clouds, placed outside the earlier (closer) camera views: the pull-out brings them in from
    the top and side edges of the frame after the overcast has gone (they never show through it)."""
    body = ""
    for cx, cy, w, h, seed in ((380, 92, 340, 104, 61), (1060, 58, 260, 84, 62), (2290, 78, 310, 98, 63),
                               (2700, 330, 240, 78, 64), (20, 318, 210, 66, 65)):
        body += S.cloud(cx, cy, w, h, "#fff6e2", seed=seed, sw=3, shade_fill="#f6d9a8")
    return doc(S.g(body, filter="wobble"))


def mountains_svg():
    """Faint blue mountains on the eastern horizon (aerial perspective)."""
    far = S.hill(-100, 1500, 800, 120, seed=7, bumps=4)
    far2 = S.hill(1200, 2950, 800, 150, seed=9, bumps=4)
    near = S.hill(-100, 2950, 825, 70, seed=12, bumps=7)
    body = (S.path(far, "#c9cbd6", sw=2.5) + S.path(far2, "#c4c6d4", sw=2.5)
            + S.path(near, "#d8d2cc", sw=2.5))
    return doc(S.g(body, filter="wobble", opacity=0.95))


def palm(x, y, s, lean=0.0):
    return PR.palm_tree(x, y, s, lean=lean)


# row B houses: (x, variant, facing). The gap in the middle is the open square where the light lands.
ROW_B = [(-60, 2, 1), (300, 0, 1), (640, 1, -1), (990, 3, 1), (1330, 0, -1), (1960, 2, 1), (2330, 3, -1),
         (2650, 0, 1), (2930, 1, -1)]
# row A (farther): homes fill the middle behind the square
ROW_A = [(-40, 0, 1), (190, 2, -1), (430, 3, 1), (660, 0, -1), (880, 1, 1), (1120, 2, 1), (1350, 0, -1),
         (1565, 2, 1), (1770, 0, -1), (1930, 3, 1), (2150, 0, -1), (2380, 2, 1), (2620, 1, -1), (2850, 0, 1)]
ROOF_DY = {0: -510, 1: -845, 2: -524, 3: -594}


def roof_y(i):
    x, v, fc = ROW_B[i]
    return ROW_B_Y + ROOF_DY[v] * ROW_B_S


def city_svg():
    """Far skyline, the great ziggurat (far left), two rows of houses with palms and the open square (static)."""
    defs = (S.lin_grad("s18haze", [(0, "#f1e2c4", 0), (1, "#f1e2c4", 0.5)]) +
            S.lin_grad("s18ground", [(0, "#e8d4aa"), (0.5, "#e2c899"), (1, "#d9bb88")]))
    body = PR.nineveh_skyline(-120, 2920, SKY_Y, scale=0.66, seed=5, haze=0.5)
    body += f'<rect x="-20" y="{SKY_Y - 200}" width="{SW + 40}" height="210" fill="url(#s18haze)"/>'
    # the city floor between the house rows (streets, yards and the square seen from above)
    gy0, gy1 = SKY_Y - 6, PAR_TOP + 30
    ground = f'<rect x="-30" y="{gy0}" width="{SW + 60}" height="{gy1 - gy0}" fill="url(#s18ground)"/>'
    lanes = "".join(f'<path d="M-30,{y} L{SW + 30},{y}"/>' for y in (SKY_Y + 40, ROW_A_Y + 26, ROW_A_Y + 70, ROW_A_Y + 112))
    ground += f'<g stroke="{P["sand_dark"]}" stroke-width="2" opacity="0.28" fill="none">{lanes}</g>'
    # paving of the open square
    sq = (f'<path d="{S.blob(GAP_X, SQUARE_Y - 6, 190, 40, 0.06, 12, 3)}" fill="#ecd7ad" opacity="0.8"/>'
          f'<path d="{S.blob(GAP_X, SQUARE_Y - 6, 120, 24, 0.06, 10, 4)}" fill="none" stroke="{P["sand_dark"]}" '
          f'stroke-width="2.5" opacity="0.35"/>')
    body += S.g(ground + sq, filter="wobble")
    body += PR.ziggurat(ZIG_X, ZIG_Y, ZIG_S)
    # row A (farther) with palms behind
    rowa = ""
    for x, s, ln in ((70, 0.29, 0.1), (560, 0.32, -0.1), (1040, 0.28, 0.15), (1250, 0.32, -0.2), (1680, 0.3, 0.12),
                     (2050, 0.3, 0.1), (2520, 0.32, -0.1), (2760, 0.28, 0.2)):
        rowa += palm(x, ROW_A_Y - 10, s, ln)
    for x, v, fc in ROW_A:
        rowa += PR.house(x, ROW_A_Y, ROW_A_S, variant=v, facing=fc)
    body += f'<g opacity="1">{rowa}</g>'
    body += f'<rect x="-20" y="{ROW_A_Y - 120}" width="{SW + 40}" height="140" fill="url(#s18haze)" opacity="0.6"/>'
    # row B (nearer): two palms at the sides of the open square, houses
    rowb = ""
    for x, s, ln in ((1464, 0.42, 0.16), (1818, 0.4, -0.14), (170, 0.38, 0.1), (2140, 0.39, -0.12)):
        rowb += palm(x, ROW_B_Y - 8, s, ln)
    for x, v, fc in ROW_B:
        rowb += PR.house(x, ROW_B_Y, ROW_B_S, variant=v, facing=fc)
    # the street in front of row B (below our parapet)
    street = (f'<path d="M-30,{ROW_B_Y - 4} L{SW + 30},{ROW_B_Y - 4} L{SW + 30},{PAR_TOP + 20} L-30,{PAR_TOP + 20} Z" '
              f'fill="#e3c796" stroke="{INK}" stroke-width="3"/>')
    street += (f'<g stroke="{P["ink_soft"]}" stroke-width="2" opacity="0.25" fill="none">'
               + "".join(f'<path d="M-30,{y} L{SW + 30},{y}"/>' for y in (ROW_B_Y + 14, ROW_B_Y + 34))
               + "</g>")
    # a few jars and a sack in the street
    street += PR.jar(1385, ROW_B_Y + 14, 0.36) + PR.jar(1412, ROW_B_Y + 20, 0.3)
    street += PR.sack(2290, ROW_B_Y + 28, 0.32, seed=2)
    body += rowb + S.g(street, filter="wobble")
    return doc(body, defs)


# ============================================================================ our roof terrace


MAT = (150, 1190, 1418, 1572)     # reed mat under the family: x0, x1, y0, y1


def terrace_svg():
    defs = (S.lin_grad("s18floor", [(0, "#dcbd8c"), (0.4, "#e7cb9a"), (1, "#ecd2a4")]) +
            S.lin_grad("s18par", [(0, "#d3ae78"), (1, "#c49c66")]) +
            S.lin_grad("s18hatch", [(0, "#5a3d2b"), (1, "#7a5638")]))
    out = ""
    # floor (plaster) with perspective joints converging on the square
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
    # plaster patches on the parapet
    for cx, cy in ((520, 1298), (1300, 1284), (2210, 1304)):
        par += f'<path d="{S.blob(cx, cy, 60, 18, 0.25, 8, cx + 7)}" fill="#e3c592" opacity="0.8"/>'
    out += par
    # ladder hatch at the front right (a ladder top pokes out of it)
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
    mx0, mx1, my0, my1 = MAT
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
    # pots, a rope coil and a sack along the parapet (static props under the subtitle box at the end)
    deco = (PR.jar(1330, 1376, 0.7) + PR.jar(1410, 1398, 0.54, color="#c46f48")
            + PR.rope_coil(1600, 1404, 0.64) + PR.sack(1790, 1402, 0.62, seed=5)
            + PR.jar(1255, 1440, 0.46, color="#b9845a"))
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
            + PR.bush(-40, SH + 16, 0.95, variant=3) + PR.grass_tuft(1230, SH + 6, 0.9, variant=0))
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


# the family on our roof, grouped with overlaps and different depths (the children well left of the subtitle
# box of the final framing): name -> (kind, variant, x, y, facing, z)
FAMILY = {
    "girl": ("child", 1, 330, 1522, 1, 31.2),       # in front of grandpa
    "grandpa": ("elder", 1, 462, 1458, 1, 30.0),
    "mother": ("woman", 3, 640, 1480, 1, 30.5),     # the boy kneels close against her
    "boy": ("child", 0, 772, 1518, 1, 31.0),
    "father": ("man", 2, 965, 1444, 1, 29.8),       # a step back
}

# neighbours in the street below our parapet (z 4: our terrace hides them below the chest), in small
# irregular groups: (kind, variant, x, y, scale, facing)
STREET = {
    "st_l": [("woman", 0, 1196, STREET_Y, 0.46, 1), ("child", 2, 1250, STREET_Y - 8, 0.46, 1),
             ("man", 3, 1352, STREET_Y + 2, 0.46, -1)],
    "st_c": [("elder", 2, 1548, STREET_Y - 2, 0.46, 1), ("woman", 1, 1668, STREET_Y + 3, 0.46, -1),
             ("child", 3, 1718, STREET_Y - 10, 0.46, -1)],
    "st_r": [("man", 1, 1908, STREET_Y, 0.46, -1), ("man", 0, 2052, STREET_Y + 4, 0.46, 1),
             ("woman", 2, 2112, STREET_Y - 2, 0.46, -1)],
}

# the open square in the middle of the city, right under the gap in the cloud
SQUARE = {
    "sq_back": [("man", 1, 1598, SQUARE_Y - 26, 0.31, 1), ("woman", 2, 1676, SQUARE_Y - 30, 0.31, -1),
                ("elder", 3, 1735, SQUARE_Y - 24, 0.31, -1)],
    "sq_l": [("man", 2, 1500, SQUARE_Y, 0.34, 1), ("woman", 3, 1546, SQUARE_Y + 6, 0.34, 1),
             ("child", 1, 1590, SQUARE_Y + 12, 0.34, 1)],
    "sq_r": [("child", 0, 1680, SQUARE_Y + 12, 0.34, -1), ("elder", 0, 1722, SQUARE_Y + 2, 0.34, -1),
             ("woman", 0, 1780, SQUARE_Y + 8, 0.34, -1)],
}


def roof_people():
    """Little groups kneeling on the roofs of row B (varied counts, spacing and facing): name -> members."""
    s = 0.31
    plan = {  # roof index: [(kind, variant, dx from the roof centre, facing)]
        1: [("man", 1, -52, 1), ("woman", 0, 0, 1), ("child", 2, 40, -1)],
        2: [("woman", 2, -18, 1), ("child", 0, 30, -1)],
        3: [("elder", 0, 22, 1)],
        4: [("woman", 1, -30, 1), ("man", 3, 8, 1)],
        5: [("child", 3, -44, 1), ("man", 0, 4, -1)],
        6: [("woman", 3, -48, -1), ("elder", 2, 30, -1)],
        7: [("man", 2, -10, -1)],
    }
    out = {}
    for i, mem in plan.items():
        x, v, fc = ROW_B[i]
        ry = roof_y(i) + 2
        cx = x - 40 * ROW_B_S * fc
        out[f"roof{i}"] = [(k, var, cx + dx, ry + (2 if j % 2 else 0), s, f) for j, (k, var, dx, f) in enumerate(mem)]
    return out


# ============================================================================ light


def light_fx(gloom_a, hole_r, gap, warm_a, glow_a, glow_s, glow_c, glow_r=(900, 520), glow_floor=(1190, 1290)):
    """One cheap output-space pass (instead of three full-frame glaze layers, see the render budget):

    * gloom: a cool multiply glaze under the overcast (strongest at the top of the frame). It thins under the
      cloud's middle as God sees, then lifts outward from the cloud gap: a soft elliptical hole of radius
      hole_r(t) (stage px) centred on ``gap`` lets the light spread over the city, while gloom_a(t) thins the
      rest;
    * warm: a light golden multiply glaze, warm_a(t);
    * glow: a warm screen glow over the square and the roofs where the rays land (glow_c, radii
      glow_r * glow_s(t)), glow_a(t); it fades out below our parapet (stage y glow_floor) so the family in the
      foreground keeps its own colours.
    The maps are computed on a 1/8-resolution grid and upsampled (they are all soft).
    """
    f = 8
    gw, gh = OUT_W // f, OUT_H // f
    X, Y = np.meshgrid((np.arange(gw) + 0.5) * f, (np.arange(gh) + 0.5) * f)
    v = (Y / OUT_H)[..., None]
    gstr = np.interp(Y / OUT_H, [0, 0.4, 0.7, 1.0], [0.32, 0.27, 0.17, 0.1])[..., None]
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
            oy0 = view.to_out(0, 0)[1]
            sy = (Y - oy0) / view.scale                       # stage y of each grid cell (camera never rotates)
            a = a * np.clip((glow_floor[1] - sy) / (glow_floor[1] - glow_floor[0]), 0, 1)
            s8 = np.zeros((gh, gw, 4), np.uint8)
            s8[..., :3] = np.clip(gcol * a[..., None] + 0.5, 0, 255)
            arr = cv2.subtract(255, cv2.multiply(cv2.subtract(255, arr), cv2.subtract(255, up(s8)), scale=1 / 255.0))
        return Image.fromarray(arr, "RGBA")
    return fx


# cloud colours: an overcast grey (lighter than v1's storm slate so the dissolve from s17's hazy sky does not
# darken into a storm; the lowest banks are the lightest, so the cloud thins toward its bottom edge). The gloom
# is applied after all layers by light_fx. Lit: warm gold-beige, the clouds catching God's light (not v1's mauve,
# which turns bruise-purple under the cool gloom).
CLOUD_DARK = {"back": ("#9b9eac", "#828495"), "front": ("#9294a3", "#7b7d8c"), "low": ("#9fa1ac", "#8c8d98")}
CLOUD_LIT = {"back": ("#c8b39c", "#a8937f"), "front": ("#c6ae95", "#a68f7b"), "low": ("#cfb48f", "#ab9279"),
             "centre": ("#d6b98a", "#b0946f")}


def bank_frames(items, kind, rect=None, lit_kind=None):
    out = []
    for fill, shade in (CLOUD_DARK[kind], CLOUD_LIT[lit_kind or kind]):
        extra = ""
        if rect:
            x0, x1, y1 = rect
            extra = f'<rect x="{x0}" y="-40" width="{x1 - x0}" height="{y1 + 40}" fill="{fill}"/>'
        out.append(V.cloud_bank_svg(items, fill, shade, extra=extra))
    return out


# the overcast over the city: (items, kind, rect). The middle banks (back_c*, low_c*) are drawn as left and
# right halves so they can slide apart, opaque, when the cloud splits; together they look like one bank.
BANKS = {
    "back_l": ([(240, 60, 920, 360, 71), (900, 30, 860, 330, 72), (260, 300, 760, 300, 83)], "back",
               (-40, 1240, 230)),
    "back_r": ([(2440, 50, 960, 350, 73), (2790, 90, 620, 300, 74), (2700, 300, 640, 280, 84)], "back",
               (2020, 2900, 230)),
    "back_cl": ([(GAP_X - 215, 118, 480, 360, 75)], "back", (1190, GAP_X - 80, 140)),
    "back_cr": ([(GAP_X + 215, 124, 480, 350, 87)], "back", (GAP_X + 80, 2060, 140)),
    "front_l": ([(1080, 250, 1060, 380, 76)], "front", (560, 1580, 190)),
    "front_r": ([(2230, 260, 1020, 360, 77)], "front", (1740, 2900, 190)),
    "low_l": ([(380, 560, 700, 220, 78), (1060, 560, 660, 230, 79)], "low", None),
    "low_r": ([(2200, 555, 720, 225, 80), (2760, 575, 500, 200, 81)], "low", None),
    "low_cl": ([(GAP_X - 150, 532, 380, 205, 82)], "low", None),
    "low_cr": ([(GAP_X + 155, 526, 390, 212, 88)], "low", None),
}


def cloud_geom(cx, cy, w, h, seed, puffs=6):
    """The circles and base ellipse of S.cloud(cx, cy, w, h, seed=seed, puffs=puffs) (same random sequence)."""
    r = random.Random(seed)
    circles = []
    for i in range(puffs):
        u = (i + 0.5) / puffs
        rad = h * (0.42 + 0.35 * math.sin(math.pi * u)) * r.uniform(0.85, 1.12)
        x = cx - w / 2 + w * u + r.uniform(-w * 0.03, w * 0.03)
        y = cy + h * 0.18 - rad * 0.55 + r.uniform(-h * 0.06, h * 0.06)
        circles.append((x, y, rad))
    return circles, (cx, cy + h * 0.2, w * 0.52, h * 0.32)


def rim_svg(items, rid, y0, y1, col="#ffe6a0", r_out=12, r_in=9):
    """God's light catching the lower edge of a cloud bank (a golden 'silver lining'): a soft band straddling
    the bank's silhouette (r_in px inside, r_out px outside, blurred), only below y0 and full by y1."""
    sil = ""
    for cx, cy, w, h, seed in items:
        circles, (bx, by, brx, bry) = cloud_geom(cx, cy, w, h, seed)
        sil += f'<ellipse cx="{f1(bx)}" cy="{f1(by)}" rx="{f1(brx)}" ry="{f1(bry)}"/>'
        sil += "".join(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}"/>' for x, y, r in circles)
    hgt = SH - y0
    defs = (f'<filter id="{rid}f" x="-10%" y="-25%" width="120%" height="150%">'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="{r_out}" result="d"/>'
            f'<feMorphology in="SourceAlpha" operator="erode" radius="{r_in}" result="e"/>'
            f'<feComposite in="d" in2="e" operator="out" result="ring"/>'
            f'<feGaussianBlur in="ring" stdDeviation="6" result="rb"/>'
            f'<feFlood flood-color="{col}"/><feComposite in2="rb" operator="in"/></filter>'
            + S.lin_grad(f"{rid}g", [(0, "#ffffff", 0), (min(1.0, (y1 - y0) / hgt), "#ffffff", 1), (1, "#ffffff", 1)])
            + f'<mask id="{rid}m" maskUnits="userSpaceOnUse" x="-100" y="-100" width="{SW + 200}" height="{SH + 200}">'
              f'<rect x="-40" y="{y0}" width="{SW + 80}" height="{hgt}" fill="url(#{rid}g)"/></mask>')
    body = (f'<g mask="url(#{rid}m)"><g filter="url(#{rid}f)"><g filter="url(#wobble)" fill="#000000">{sil}</g>'
            f'</g></g>')
    return doc(body, defs)


def behind_overcast(fxs, motions, t_on, margin=10, q=2):
    """Output-space fx (sparkles, motes; they are drawn after every layer) seen as if in the air BEHIND the
    overcast: while a cloud bank is in frame their drawing is masked by the banks' silhouettes - the base
    ellipses, puff circles and top rects that cloud_bank_svg draws, moved by each bank's motion and the camera,
    grown by ``margin`` stage px for the ink line and the wobble, softened a little - so nothing twinkles on a
    cloud face and the opening sky shows them as the banks roll away. The mask is drawn at 1/q resolution.
    Before ``t_on`` (none of them shows yet) and once every bank has left the frame they draw directly, exactly
    as unwrapped."""
    banks = []          # (motion, ellipses (n, 4) [cx, cy, rx, ry], rects [(x0, y0, x1, y1)]) in stage px
    for name, mo in motions.items():
        items, _, rect = BANKS[name]
        ells = []
        for cx, cy, w, h, seed in items:
            circles, base = cloud_geom(cx, cy, w, h, seed)
            ells += [base] + [(x, y, r, r) for x, y, r in circles]
        banks.append((mo, np.array(ells, np.float64), [(rect[0], -40, rect[1], rect[2])] if rect else []))
    mw, mh = OUT_W // q, OUT_H // q
    sub = 16                                   # cv2 fixed-point sub-pixel factor (shift=4)

    def keep_mask(t, view):
        M = view.M
        k = M[0, 0] / q                        # mask px per stage px (the camera never rotates)
        cov = None
        for mo, ells, rects in banks:
            tf = mo(t)
            # stage -> mask px for this bank: x -> ax * x + bx (scale tf.sx about the pivot, then move)
            ax, ay = k * tf.sx, k * tf.sy
            bx = M[0, 2] / q + k * (tf.px + tf.dx - tf.sx * tf.px)
            by = M[1, 2] / q + k * (tf.py + tf.dy - tf.sy * tf.py)
            ex, ey = ells[:, 0] * ax + bx, ells[:, 1] * ay + by
            rx, ry = ells[:, 2] * ax + margin * k, ells[:, 3] * ay + margin * k
            rr = [(x0 * ax + bx - margin * k, y0 * ay + by - margin * k, x1 * ax + bx + margin * k,
                   y1 * ay + by + margin * k) for x0, y0, x1, y1 in rects]
            lo_x = min([(ex - rx).min()] + [r[0] for r in rr])
            hi_x = max([(ex + rx).max()] + [r[2] for r in rr])
            lo_y = min([(ey - ry).min()] + [r[1] for r in rr])
            hi_y = max([(ey + ry).max()] + [r[3] for r in rr])
            if hi_x < -2 or lo_x > mw + 2 or hi_y < -2 or lo_y > mh + 2:
                continue                       # this bank is out of frame
            if cov is None:
                cov = np.zeros((mh, mw), np.uint8)
            for x, y, a, b in zip(ex, ey, rx, ry):
                cv2.ellipse(cov, (round(x * sub), round(y * sub)), (round(a * sub), round(b * sub)), 0, 0, 360,
                            255, -1, cv2.LINE_AA, 4)
            for x0, y0, x1, y1 in rr:
                cv2.rectangle(cov, (round(x0 * sub), round(y0 * sub)), (round(x1 * sub), round(y1 * sub)), 255, -1,
                              cv2.LINE_AA, 4)
        if cov is None:
            return None
        cov = cv2.GaussianBlur(cov, (0, 0), 0.75)
        return cv2.resize(255 - cov, (OUT_W, OUT_H), interpolation=cv2.INTER_LINEAR)

    def fx(frame, t, view):
        keep = keep_mask(t, view) if t >= t_on else None
        if keep is None:
            for f in fxs:
                res = f(frame, t, view)
                frame = frame if res is None else res
            return frame
        layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        for f in fxs:
            res = f(layer, t, view)
            layer = layer if res is None else res
        arr = np.array(layer)
        arr[..., 3] = cv2.multiply(np.ascontiguousarray(arr[..., 3]), keep, scale=1 / 255.0)
        frame.alpha_composite(Image.fromarray(arr, "RGBA"))
        return frame
    return fx


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


# ============================================================================ camera


def hermite_cam(keys):
    """keys [(t, Cam, (vx, vy, vw))]: piecewise cubic Hermite through the keys with the given velocities
    (stage px/s), so a long move can start out of a slow drift and never comes to a dead stop half-way."""
    keys = sorted(keys, key=lambda k: k[0])

    def c(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, va), (t1, b, vb) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                d = t1 - t0
                u = (t - t0) / d
                h00, h10 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u
                h01, h11 = -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
                pa, pb = (a.x, a.y, a.w), (b.x, b.y, b.w)
                x, y, w = (h00 * pa[i] + h10 * d * va[i] + h01 * pb[i] + h11 * d * vb[i] for i in range(3))
                return Cam(x, y, w)
    return c


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

    # ---- sky and city (the grey of the overcast comes from the gloom in light_fx) ----
    sc.add("sky", sky_gold_svg(), z=0, wc=0.6)
    sc.add("sky_blue", sky_blue_svg(), z=0.5, wc=0.4,
           motion=M.keys([(T - 2.6, {"alpha": 0}), (T - 0.5, {"alpha": 1})], "sine"))
    sc.add("mountains", mountains_svg(), z=1.5)
    sc.add("city", city_svg(), z=2)
    # fair-weather clouds: brought into view by the camera pull-out (no pop-in, never seen through the overcast)
    sc.add("fair", fair_clouds_svg(), z=2.4, motion=M.drift(vx=3))

    # ---- neighbours on the roofs, in the square and in the street: pray -> glad (wave from the centre) -> cheer
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
    for i, (name, members) in enumerate(SQUARE.items()):
        add_group(name, members, 3.5 + 0.01 * i, t_glad - 0.05, t_cheer0)
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
    animal_layer("lamb", "sheep", 2040, 1438, 0.82, -1, 29.5, t_peace + 0.2, per=2.2, ph=0.6)

    # the family: hard pose / face cuts hidden by a small squash-and-hop; at the wonder cut the whole figure
    # tilts back a little to look up into the light (held, easing to a smaller tilt when they turn glad)
    fam_wonder = {"grandpa": 0.3, "father": 0.15, "girl": 0.0, "mother": 0.22, "boy": 0.08}
    fam_glad = {"grandpa": 0.44, "father": 0.3, "girl": 0.14, "mother": 0.38, "boy": 0.28}   # every wonder >= 1.1 s
    fam_cheer = {"girl": 0.0, "boy": 0.14, "father": 0.32}
    for name, (kind, v, x, y, fc, z) in FAMILY.items():
        states = ["pray"]
        sched = [(0, 0)]
        tp = None
        if name == "girl":
            tp = cut_at(t_peek)
            states.append("peek")
            sched.append((tp, len(states) - 1))
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
        # look up: tilt back around a point between the knees and the toes, low over the ground
        tilt = [(0, {"rot": 0})]
        if tp is not None:
            tilt += [(tp, {"rot": 0}), (tp + 0.3, {"rot": -1.6 * fc})]
        tilt += [(tw, {}), (tw + 0.3, {"rot": -3.6 * fc}), (tg, {}), (tg + 0.3, {"rot": -1.2 * fc})]
        if tc is not None:
            tilt += [(tc - 0.02, {}), (tc, {"rot": 0})]
        parts.append(M.keys(tilt, ["sine"] * (len(tilt) - 1), pivot=(x - 30 * fc, y - 24)))
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

    # ---- doves: four perched on the dovecote burst out on "整座尼尼微城", three take off from roofs earlier ----
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
    # far doves: perched on row-B roof edges from the start (small), they take off as the city is spared
    fs = 0.62
    far_doves = [  # (facing, perch (x, y), take-off time, flight [(dt, x, y)], rate, phase)
        (-1, (1838, roof_y(5) - 17), t_spared + 0.5,
         [(0.5, 1780, 870), (1.6, 1650, 680), (t_whole + 1.0 - t_spared - 0.5, 1350, 520), (T - t_spared - 0.5, 900, 360)],
         12, 0.1),
        (1, (1436, roof_y(4) - 17), t_spared + 0.8,
         [(0.5, 1480, 880), (1.5, 1580, 730), (t_whole + 1.2 - t_spared - 0.8, 1900, 570), (T - t_spared - 0.8, 2300, 400)],
         13, 0.5),
        (-1, (1150, roof_y(3) - 17), t_whole + 0.4,
         [(0.5, 1110, 860), (1.4, 1000, 690), (T - t_whole - 0.4, 700, 480)], 12, 0.8),
    ]
    for i, (fc, (qx, qy), ta, path, rate, ph) in enumerate(far_doves):
        pts = [(ta - 0.01, qx, qy)] + [(ta + dt, x, y) for dt, x, y in path]
        sc.add(f"fdove{i}", dove_frames(fc, 0.85, True), z=2.5 + 0.01 * i, seed=910 + (fc > 0),
               frame_at=perch_wings(ta, rate, ph, T - 2.0),
               motion=M.combine(V.flight(pts, DOVE_REF),
                                M.keys([(0, {"s": fs})], pivot=DOVE_REF),
                                lambda t, a=ta, p=ph: Tf(dy=6 * math.sin(2 * math.pi * (t / 0.9 + p))
                                                         * M.progress(t, a, a + 0.6, "sine")) if t > a else Tf()))

    # ---- golden light behind the cloud: grows while God sees, bursts through the gap ----
    sc.add("gleam", V.gleam_svg(GAP_X, 330, 280, 360), z=40.1, wc=0, motion=M.combine(
        M.keys([(0, {"alpha": 0.3, "sx": 0.5, "sy": 0.6}), (t_see, {"alpha": 0.3, "sx": 0.5, "sy": 0.6}),
                (t_mercy - 0.1, {"alpha": 0.85, "sx": 0.8, "sy": 0.85}),
                (t_mercy + 0.6, {"alpha": 1, "sx": 1.1, "sy": 1.05}),
                (t_spared + 0.2, {"alpha": 0.85, "sx": 1.22, "sy": 1.12}),
                (t_spared + 1.4, {"alpha": 0, "sx": 1.3, "sy": 1.16})],
               ["sine", "sine", "out", "sine", "sine"], pivot=(GAP_X, 200)),
        M.pulse(0.88, 1.0, 2.6)))

    # ---- the overcast: churns, catches the light, splits at the gap, then rolls away off the frame ----
    lit_c = lambda t: M.progress(t, t_see + 0.3, t_mercy, "sine")        # the middle warms while God sees
    lit = lambda t: M.progress(t, t_mercy - 0.6, t_mercy + 1.4, "sine")

    def roll(u, a):
        """Pushed-aside path, 0 -> 1 over u 0 -> 1: starts at once with speed a (0..1), speeds up to 2 - a,
        then keeps that speed (the bank is already off-frame) for half the move more and stops."""
        if u <= 0:
            return 0.0
        if u <= 1:
            return a * u + (1 - a) * u * u
        return 1 + (2 - a) * (min(u, 1.5) - 1)

    def cloud_motion(go_dx, go_dy, go_t, drift, pivot, s1=1.06, churn=0.0, ax=0.6, ay=0.1):
        # from the moment of mercy the light pushes the bank aside, fully opaque: it slides outward at once
        # (the middle halves part at the gap), then curves up and away, speeding up until it has left the
        # frame (the camera is widening, so each move ends well outside the final framing of the whole city)
        def go(t):
            u = (t - t_mercy) / go_t
            fx, fy = roll(u, ax), roll(u, ay)
            s = 1 + (s1 - 1) * min(1.0, fx)
            return Tf(dx=go_dx * fx, dy=go_dy * fy, sx=s, sy=s, px=pivot[0], py=pivot[1])
        return M.combine(
            go,
            M.drift(vx=drift),
            M.bob(churn, 5.5, phase=pivot[0] / 977.0, axis="y") if churn else None,
            M.bob(churn * 2.2, 7.5, phase=pivot[0] / 1311.0, axis="x") if churn else None)

    plan = {  # name: (z, go_dx, go_dy, go_t (s after the moment of mercy), drift, pivot, s1, ax)
        "back_l": (40.2, -650, -560, 2.8, -3, (560, 80), 1.06, 0.5),
        "back_r": (40.21, 650, -550, 2.8, 3, (2500, 80), 1.06, 0.5),
        "back_cl": (40.22, -700, -430, 2.6, -3, (GAP_X - 215, 120), 1.08, 0.8),
        "back_cr": (40.23, 700, -420, 2.6, 3, (GAP_X + 215, 120), 1.08, 0.8),
        "low_l": (40.3, -900, -780, 2.9, -2, (760, 560), 1.04, 0.5),
        "low_r": (40.31, 900, -780, 2.9, 2, (2400, 560), 1.04, 0.5),
        "low_cl": (40.32, -800, -740, 2.7, -2, (GAP_X - 150, 530), 1.06, 0.8),
        "low_cr": (40.33, 800, -730, 2.7, 2, (GAP_X + 155, 530), 1.06, 0.8),
        "front_l": (40.4, -800, -540, 3.0, -3, (1080, 250), 1.06, 0.5),
        "front_r": (40.41, 800, -560, 3.0, 3, (2230, 260), 1.06, 0.5),
    }
    motions = {}
    for name, (z, gdx, gdy, gt, dr, pv, s1, ax) in plan.items():
        items, kind, rect = BANKS[name]
        centre = name.startswith(("back_c", "low_c"))
        mo = cloud_motion(gdx, gdy, gt, dr, pv, s1, churn=5.0, ax=ax)
        motions[name] = mo
        sc.add(f"cloud_{name}", bank_frames(items, kind, rect, "centre" if centre else None), z=z,
               frame_at=lit_c if centre else lit, motion=mo)

    # God sees: a golden seam glows along the lower edge of the middle of the cloud before it splits; each
    # half of the seam travels with its half of the cloud and fades as the gap opens
    seam_a = M.keys([(t_see + 0.3, {"alpha": 0}), (t_mercy - 0.15, {"alpha": 0.75}), (t_mercy + 0.15, {"alpha": 0.85}),
                     (t_mercy + 0.75, {"alpha": 0})], ["sine", "sine", "sine"])
    for side in ("l", "r"):
        items = BANKS[f"low_c{side}"][0]
        sc.add(f"seam_{side}", rim_svg(items, f"s18rim{side}", 500, 590), z=40.5, wc=0, blend="screen",
               motion=M.combine(motions[f"low_c{side}"], seam_a, M.pulse(0.85, 1.0, 1.9)))

    # ---- God's mercy: golden rays pour down through the gap over the square, the homes and our roof ----
    # z 40.15: above the gleam and every other layer, but BELOW every cloud bank (40.2+), so the opaque halves
    # parting at the gap hide the ray fan until they have slid clear (no rays painted on the cloud faces)
    rsrc = (GAP_X, 330)
    sc.add("rays", V.rays_svg(rsrc, 92, 97, n=11, length=1600, seed=6), z=40.15, wc=0, blend="add",
           motion=M.combine(M.keys([(t_mercy + 0.05, {"alpha": 0, "sx": 0.4, "sy": 0.3}), (t_mercy + 0.75, {"alpha": 1}),
                                    (t_spared + 0.8, {"sx": 1.0, "sy": 1.0}), (t_whole + 1.5, {"alpha": 0.4})],
                                   ["sine", "out", "sine"], pivot=rsrc),
                            M.pulse(0.8, 1.0, 3.2), M.sway(1.0, 7.0, rsrc)))
    # gloom thinning under the middle while God sees, then lifting outward from the gap; warm glaze; warm glow
    # spreading over the square and the roofs (see light_fx)
    gloom_a = M.keys([(t_mercy, {"alpha": 1}), (t_gold1 + 0.3, {"alpha": 0})], "sine")
    hole = M.keys([(t_see, {"s": 0}), (t_see + 0.9, {"s": 120}), (t_mercy + 0.1, {"s": 170}),
                   (t_mercy + 0.9, {"s": 560}), (t_gold1, {"s": 3400})], ["sine", "sine", "out", "sine"])
    warm_a = M.keys([(t_gold0, {"alpha": 0}), (t_gold1 + 0.4, {"alpha": 1}), (T - 0.4, {"alpha": 0.6})], "sine")
    glow = M.combine(M.keys([(t_mercy + 0.3, {"alpha": 0, "s": 0.25}), (t_spared, {"alpha": 0.75, "s": 0.8}),
                             (t_whole + 0.6, {"alpha": 0.34, "s": 1.5}), (T, {"alpha": 0.22, "s": 1.6})],
                            ["out", "sine", "sine"]), M.pulse(0.9, 1.0, 3.0))
    light = light_fx(lambda t: gloom_a(t).alpha, lambda t: hole(t).sx, (GAP_X, 500), lambda t: warm_a(t).alpha,
                     lambda t: glow(t).alpha, lambda t: glow(t).sx, (GAP_X, 1130))

    # ---- camera: opens on the low overcast over the roofs of the city, tilts down and pulls back onto our
    # praying roof while God sees, drifts slowly over it, then one continuous pull-out to the whole city.
    # The opening framing keeps every big figure (our family, the street neighbours) below the frame through
    # the dissolve from s17, whose street of praying families uses the same character designs at another
    # place and scale (shown together they read as doubled people); only the tiny roof-top figures show. ----
    t_d = t_whole + 2.6
    O = Cam(1400, 553, 1760)          # overcast + far city + row-B roofs; viewport bottom y 1048 above all heads
    v_o = (-4.0, 3.0, 4.0)            # slow drift through the dissolve (bottom edge stays above y 1052)
    t_o1 = 0.5                        # the descent starts half-way through the dissolve, eased in
    A = Cam(1306, 900, 2262)          # right edge just clear of the top dove on the dovecote
    B = Cam(1340, 886, 2300)
    D = Cam(1400, 789, 2756)
    E = Cam(1400, 787, 2760)
    v_ab = tuple((getattr(B, k) - getattr(A, k)) / t_mercy for k in ("x", "y", "w"))
    v_de = tuple((getattr(E, k) - getattr(D, k)) / max(0.5, T - t_d) for k in ("x", "y", "w"))
    # land on the original slow drift A -> B (~2.2 s descent, peak ~13 px/frame on screen), nearly settled as
    # the girl peeks up
    t_land = max(t_o1 + 1.8, min(t_peek + 0.15, t_mercy - 0.9))
    O1 = Cam(*(getattr(O, k) + v_o[i] * t_o1 for i, k in enumerate(("x", "y", "w"))))
    A1 = Cam(*(getattr(A, k) + v_ab[i] * t_land for i, k in enumerate(("x", "y", "w"))))
    sc.camera = hermite_cam([(0, O, v_o), (t_o1, O1, v_o), (t_land, A1, v_ab), (t_mercy, B, v_ab),
                             (t_d, D, v_de), (max(T, t_d + 0.5), E, v_de)])

    # ---- effects ----
    sc.fx = [
        light,
        # God sees: a few slow sparkles drift down from the seam toward the praying square
        FX.sparkles((GAP_X - 250, 600, GAP_X + 250, 700), count=10, t0=t_see + 0.5, t1=t_mercy + 1.8,
                    color=(255, 234, 164), size=(6, 13), period=2.4, drift=28, seed=29),
        # sparkles over the city and light motes: in the air BEHIND the overcast - the banks still leaving
        # the frame hide them (they start while the opaque banks roll away), the opening sky shows them
        behind_overcast([
            # in the air above the skyline and over the homes, kept off every temple (the great ziggurat on
            # the far left and the two small ones in the far skyline) and off every face: no rect reaches
            # stage y >= 1060 in x 300-1100, where our family's heads are (the children's rise to y ~1190 when
            # they stand to cheer); on the left they twinkle in the sky above the skyline instead
            *[FX.sparkles(r, count=n, t0=t_gold0 + 0.6, t1=T + 1, color=(255, 238, 172), size=(9, 20),
                          drift=-10, seed=31 + i)
              for i, (r, n) in enumerate((((700, 240, 2600, 560), 14), ((990, 900, 2060, 1160), 12),
                                          ((2340, 900, 2650, 1160), 4), ((120, 280, 700, 540), 4)))],
            *[FX.sparkles(r, count=n, t0=t_peace - 0.2, t1=T + 1, color=(255, 230, 150), size=(8, 17),
                          drift=-14, seed=41 + i, period=1.3)
              for i, (r, n) in enumerate((((990, 990, 2060, 1250), 14), ((2340, 990, 2600, 1250), 4),
                                          ((120, 300, 700, 540), 3)))],
            FX.motes((100, 150, 2700, 1400), count=40, t0=t_gold0 + 0.4, t1=T + 1, color=(255, 240, 200),
                     size=(3, 7), alpha=140, seed=41),
        ], motions, t_gold0 + 0.4),
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
