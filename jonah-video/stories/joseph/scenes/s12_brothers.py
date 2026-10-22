"""Scene 12 — the famine; the brothers come to Egypt and bow before Joseph (Genesis 42:1-9).

One 5000 x 1188 stage with two places, joined by a page-turn dip through the paper colour between the lines:
on the left Canaan in the famine (hot sky, a field withering to cracked stubble, Jacob's tents, a bare tree), on the
right Joseph's hall in Egypt (painted walls, a doorway at the left, a colonnade to a garden on the right, grain sacks).
s13_forgive starts on exactly this hall, camera and characters (a plain cross-dissolve): it imports the hall from here.

  opening        Canaan: the ten brothers stand in a line with two donkeys, old Jacob and little Benjamin by the tents.
  '饥荒来了'     the field withers to dry, cracked stubble; the sun burns hotter (heat shimmer).
  '没有粮食吃'   an empty grain jar topples over (clonk, dust): nothing inside; the brothers droop, sad.
  '就来到埃及买粮' Jacob waves them off; the brothers and the donkeys walk off to the right (planted-foot steps).
  (between lines) a page-turn dip through the paper colour to Joseph's hall.
  L1 opening     the brothers stand before Joseph, who sits on his gilded seat; servants by the grain sacks.
  '跪下下拜'     they kneel and bow low, one after another (thuds, dust).
  '可是'         Joseph knows them at once: he rises with a little start, a hand to his heart, eyes wide.
  '认不出约瑟'   the brothers look up puzzled ('?' marks): they do not know him.
  L2 '你还记得约瑟的梦吗' a dream bubble rises over the hall from Joseph: the brothers' sheaves stand in a row beneath
                 Joseph's sheaf, which stands up and glows;
  '麦捆向他下拜'  the sheaves bow, right above the bowing brothers;
  '现在真的发生了' the brothers dip lower in time with the sheaves; golden twinkles; then the bubble fades away.
  ending         calm: the hall, the brothers bowing, Joseph standing, moved (= s13's first frame).
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

from .s11_ruler import (arcs_markup, blink, cuts, dip, f1, happy_hop, hop, puff_markup, snap, star_path,  # noqa: F401
                        step_walk, twinkles_markup, when, with_blinks, clamp_cam)

SW, SH = 5000, 1188
INK = P["ink"]
G = 960                     # everybody's ground line
SC = 0.9                    # everybody's scale
# ---- Canaan
X0 = 1850                   # the leading brother in the caravan
LINE = [(0, 0), (3, -120), ("donkey", -272), (1, -425), (2, -545), (4, -665), ("donkey", -817), (5, -970),
        (6, -1090), (7, -1210), (8, -1330), (9, -1450)]
JACOB = (300, 960, 0.9)     # Jacob at the tents on the left; Benjamin beside him
# ---- the hall
HALL_L = 2470               # the hall's left wall (a doorway in it)
CHX = 4240                  # Joseph's seat (faces left)
SEAT_X = CHX + 18 * SC      # Joseph seated / standing up in front of the seat
JX = 4135                   # Joseph standing
XC = 3300                   # centre of the brothers' formation
# (dx, back row?, variant): back row first (drawn behind), Judah (3) front right, Reuben (0) back right
FORM = [(-345, True, 4), (-115, True, 8), (115, True, 1), (345, True, 5), (575, True, 0),
        (-460, False, 6), (-230, False, 2), (0, False, 9), (230, False, 7), (460, False, 3)]
SERVANTS = [(4470, 2, "carry"), (4600, 0, "stand")]
WALL_TOP, WALL_BOT = 175, 790
CH = Cam(3700, 600, 1950)   # the hall shot (s13 starts here)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def brother_pos(k):
    dx, back, v = FORM[k]
    return XC + dx * SC, G - (40 * SC if back else 0), SC * (0.96 if back else 1.0), v


# ============================================================================ Canaan backdrop


SUN = (1420, 250)


def canaan_sky_svg():
    """A hot, dusty famine sky: ochre to pale cream, thin dust streaks, a big sun."""
    defs = S.lin_grad("sky12", [(0, "#dd9c5c"), (0.45, "#efc283"), (0.8, "#f6dcab"), (1, "#f8e6c2")])
    defs += S.rad_grad("sun12", [(0, "#fff0c0", 0.95), (0.3, "#f9cf7a", 0.55), (1, "#f9cf7a", 0)])
    body = f'<rect x="-20" y="-20" width="2420" height="900" fill="url(#sky12)"/>'
    body += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="560" fill="url(#sun12)"/>'
    rng = random.Random(5)
    for i in range(9):
        x, y, w = rng.uniform(-100, 2200), rng.uniform(90, 560), rng.uniform(260, 520)
        body += (f'<path d="M{f1(x)},{f1(y)} q{f1(w * 0.5)},-14 {f1(w)},0" fill="none" stroke="#f9e2b4" '
                 f'stroke-width="{rng.randint(9, 16)}" stroke-linecap="round" opacity="0.7"/>')
    body += (f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="104" fill="#f8c35a" stroke="#e48f3a" stroke-width="6" '
             f'filter="url(#wobble)"/><circle cx="{SUN[0] - 30}" cy="{SUN[1] - 30}" r="34" fill="#fbd884" opacity="0.8"/>')
    return doc(body, defs)


def sun_rays_svg():
    d = S.rays(SUN[0], SUN[1], 140, 420, n=14, width_deg=8)
    return doc(f'<path d="{d}" fill="#fbd27a" opacity="0.55" filter="url(#soft)"/>')


def canaan_land_svg():
    out = ""
    defs = S.lin_grad("earth12", [(0, "#d8b07a"), (1, "#c49660")])
    out += S.path(S.hill(-100, 1300, 760, 110, seed=4, bottom=820, bumps=3), "#d9b98a", sw=3.5)
    out += S.path(S.hill(900, 2400, 770, 80, seed=9, bottom=820, bumps=3), "#e0c296", sw=3.5)
    out += S.path(f"M-40,{750} L2400,{748} L2400,{SH + 30} L-40,{SH + 30} Z", "url(#earth12)", sw=3.5)
    # cracked earth in front
    rng = random.Random(3)
    for i in range(70):
        x, y = rng.uniform(0, 2350), rng.uniform(900, SH - 10)
        d = f"M{f1(x)},{f1(y)}"
        for _ in range(3):
            x += rng.uniform(-30, 30)
            y += rng.uniform(4, 18)
            d += f" L{f1(x)},{f1(y)}"
        out += f'<path d="{d}" fill="none" stroke="#9a7046" stroke-width="2.6" opacity="0.65"/>'
    for x, y, v in ((980, 1110, 1), (1600, 1150, 2), (300, 1140, 0), (2250, 1080, 1)):
        out += PR.grass_tuft(x, y, 0.7, variant=v)
    return doc(out, defs)


def bare_tree(x, y, s):
    """A dry, leafless tree (the famine)."""
    col, dark = "#9a7454", "#6f4f36"
    out = S.path(f"M{x - 22 * s},{y} C{x - 10 * s},{y - 120 * s} {x - 30 * s},{y - 200 * s} {x - 6 * s},{y - 300 * s} "
                 f"L{x + 16 * s},{y - 296 * s} C{x + 4 * s},{y - 200 * s} {x + 26 * s},{y - 110 * s} {x + 24 * s},{y} Z", col, sw=4)
    for a, l, y0 in ((-40, 150, 230), (35, 170, 260), (-70, 110, 150), (60, 120, 180), (-15, 90, 300)):
        r = math.radians(a - 90)
        x0, yy0 = x, y - y0 * s
        x1, y1 = x0 + l * s * math.cos(r), yy0 + l * s * math.sin(r)
        out += (f'<path d="M{f1(x0)},{f1(yy0)} Q{f1((x0 + x1) / 2 + 10 * s)},{f1((yy0 + y1) / 2)} {f1(x1)},{f1(y1)}" '
                f'stroke="{INK}" stroke-width="{f1(13 * s)}" stroke-linecap="round" fill="none"/>'
                f'<path d="M{f1(x0)},{f1(yy0)} Q{f1((x0 + x1) / 2 + 10 * s)},{f1((yy0 + y1) / 2)} {f1(x1)},{f1(y1)}" '
                f'stroke="{col}" stroke-width="{f1(6 * s)}" stroke-linecap="round" fill="none"/>')
        tx, ty = x1 + 26 * s * math.cos(r - 0.6), y1 + 26 * s * math.sin(r - 0.6)
        out += f'<path d="M{f1(x1)},{f1(y1)} L{f1(tx)},{f1(ty)}" stroke="{dark}" stroke-width="{f1(4 * s)}" stroke-linecap="round"/>'
    return S.g(out, filter="wobble-fine")


def canaan_props_svg():
    """Jacob's tents and the bare trees (in front of the field band)."""
    out = PR.tent(-60, 860, 0.5, -1, flag=False) + PR.tent(250, 884, 0.66, 1, flag=False)
    out += bare_tree(2150, 905, 1.0) + bare_tree(660, 830, 0.62) + bare_tree(1250, 800, 0.45)
    return doc(out)


def canaan_field_svg(dry):
    return doc(PR.field(-40, 2400, 742, depth=150, ripe=0.55, dry=dry, seed=7))


def shimmer_svg(k):
    """Heat shimmer: wavy lines rising off the dry field (3-frame flicker)."""
    out = ""
    rng = random.Random(11)
    for i in range(16):
        x = rng.uniform(100, 2300)
        y = rng.uniform(620, 760) - 12 * k
        d = S.wave_line(y, 5, 46, k * 2.1 + i, x, x + rng.uniform(70, 130), step=10)
        out += f'<path d="{d}" fill="none" stroke="#fff3d6" stroke-width="4" stroke-linecap="round" opacity="0.7"/>'
    return doc(out)


# ============================================================================ the hall (shared with s13)


def hall_back_svg():
    """Joseph's hall: outside light through the doorway and the colonnade, painted walls, columns, floor."""
    out = ""
    defs = S.lin_grad("hsky12", [(0, "#9fd0e2"), (1, "#f4e4bd")])
    defs += S.lin_grad("hwall12", [(0, "#f1dcb0"), (1, "#e5c895")])
    defs += S.lin_grad("hfloor12", [(0, "#dcbd8f"), (1, "#cba87a")])
    defs += S.lin_grad("hceil12", [(0, "#24555e"), (1, "#2f6b74")])
    L = HALL_L
    # outside (seen through the doorway and the colonnade): sky, palms, garden
    out += f'<rect x="{L - 40}" y="-20" width="{SW - L + 60}" height="{WALL_BOT + 30}" fill="url(#hsky12)"/>'
    out += S.path(S.hill(4380, SW + 80, WALL_BOT - 10, 40, seed=6, bottom=WALL_BOT + 40, bumps=2), "#b8c98a", sw=3)
    out += PR.pyramids(4800, WALL_BOT - 30, 0.22, n=2, haze=0.5, ground=False)
    for x, sc_, ln in ((4560, 0.55, 0.1), (4760, 0.62, -0.12), (4930, 0.5, 0.15)):
        out += PR.palm_tree(x, WALL_BOT + 10, sc_, lean=ln)
    out += PR.bush(4660, WALL_BOT + 6, 0.5, variant=0) + PR.bush(4880, WALL_BOT + 4, 0.45, variant=2)
    out += S.path(S.hill(L - 40, L + 300, WALL_BOT - 20, 30, seed=2, bottom=WALL_BOT + 40, bumps=2), "#e9d2a0", sw=3)
    out += PR.palm_tree(L + 150, WALL_BOT + 10, 0.5, lean=0.1)
    # the back wall (with the doorway on the left and open to the colonnade on the right)
    wall = (f"M{L},{WALL_TOP} L4440,{WALL_TOP} L4440,{WALL_BOT} L{L + 330},{WALL_BOT} L{L + 330},{WALL_BOT - 430} "
            f"Q{L + 230},{WALL_BOT - 500} {L + 130},{WALL_BOT - 430} L{L + 130},{WALL_BOT} L{L},{WALL_BOT} Z")
    out += S.path(wall, "url(#hwall12)", sw=4)
    # turquoise dado with a lotus band, a block frieze under the ceiling
    out += S.path(f"M{L + 330},{WALL_BOT - 120} L4440,{WALL_BOT - 120} L4440,{WALL_BOT} L{L + 330},{WALL_BOT} Z", "#5f9e96", sw=3)
    out += S.path(f"M{L},{WALL_BOT - 120} L{L + 130},{WALL_BOT - 120} L{L + 130},{WALL_BOT} L{L},{WALL_BOT} Z", "#5f9e96", sw=3)
    for i, x in enumerate(range(L + 350, 4430, 60)):
        y0 = WALL_BOT - 104
        out += (f'<path d="M{x},{y0 + 44} Q{x - 16},{y0 + 16} {x - 7},{y0} Q{x},{y0 + 12} {x + 7},{y0} '
                f'Q{x + 16},{y0 + 16} {x},{y0 + 44} Z" fill="{"#f4e6c4" if i % 2 else "#e8c25a"}" stroke="{INK}" stroke-width="2.4"/>')
    cols = ["#3f6fa8", "#c9533f", "#e8c25a", "#4f8a6a"]
    for i, x in enumerate(range(L, 4440, 46)):
        out += f'<rect x="{x}" y="{WALL_TOP + 6}" width="40" height="30" fill="{cols[i % 4]}" opacity="0.85"/>'
    out += f'<path d="M{L},{WALL_TOP + 40} L4440,{WALL_TOP + 40}" stroke="{INK}" stroke-width="4"/>'
    # wall paintings: wheat sheaves and a granary (Joseph's good years) in soft colours
    for x in (3050, 3560, 4070):
        for j in range(3):
            xx = x + (j - 1) * 46
            out += (f'<path d="M{xx},{WALL_BOT - 140} L{xx - 12},{WALL_BOT - 250} M{xx},{WALL_BOT - 140} L{xx},{WALL_BOT - 262} '
                    f'M{xx},{WALL_BOT - 140} L{xx + 12},{WALL_BOT - 250}" stroke="#c99a3e" stroke-width="5" stroke-linecap="round"/>')
            out += f'<ellipse cx="{xx}" cy="{WALL_BOT - 262}" rx="11" ry="22" fill="#e8c25a" stroke="{INK}" stroke-width="2.4"/>'
            out += f'<path d="M{xx - 14},{WALL_BOT - 190} L{xx + 14},{WALL_BOT - 190}" stroke="{INK}" stroke-width="4"/>'
    out += (f'<rect x="3260" y="300" width="200" height="140" rx="8" fill="#a9d6e6" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M3290,440 L3330,390 L3370,440 Z" fill="#e8cf96" stroke="{INK}" stroke-width="3"/>')
    for k in range(1, 4):
        out += f'<rect x="{3260 + 50 * k - 5}" y="300" width="10" height="140" fill="#b8915c" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="3246" y="440" width="228" height="18" fill="#cdae78" stroke="{INK}" stroke-width="4"/>'
    # back columns
    for x in (2830, 3780, 4430):
        out += PR.egypt_column(x, WALL_BOT + 2, 1.2, height=500)
    # the ceiling: dark teal with golden rosettes, a cornice
    out += f'<rect x="{L - 30}" y="-30" width="{SW - L + 60}" height="{WALL_TOP + 30}" fill="url(#hceil12)"/>'
    rng = random.Random(4)
    for i in range(70):
        x, y = rng.uniform(L, SW), rng.uniform(10, WALL_TOP - 40)
        out += f'<path d="{star_path(x, y, 9, 0.3)}" fill="#f2c14e"/>'
    out += f'<rect x="{L - 30}" y="{WALL_TOP - 34}" width="{SW - L + 60}" height="34" fill="#e8c25a" stroke="{INK}" stroke-width="4"/>'
    for x in range(L - 20, SW + 20, 30):
        out += f'<rect x="{x}" y="{WALL_TOP - 28}" width="12" height="22" fill="{"#3f6fa8" if (x // 30) % 2 else "#c9533f"}"/>'
    # the colonnade's columns on the right (the garden between them)
    for x in (4620, 4860):
        out += PR.egypt_column(x, WALL_BOT + 6, 1.35, height=470)
    # floor
    out += f'<rect x="{L - 30}" y="{WALL_BOT}" width="{SW - L + 60}" height="{SH - WALL_BOT + 30}" fill="url(#hfloor12)"/>'
    for y in (812, 846, 890, 945, 1010, 1085):
        out += f'<path d="M{L - 30},{y} L{SW + 30},{y}" stroke="#b38e5e" stroke-width="2.5" opacity="0.55"/>'
    for x in range(L - 200, SW + 300, 150):
        out += f'<path d="M{x},{WALL_BOT} L{x - (x - 3700) * 0.45},{SH + 30}" stroke="#b38e5e" stroke-width="2.5" opacity="0.45"/>'
    out += f'<path d="M{L - 30},{WALL_BOT} L{SW + 30},{WALL_BOT}" stroke="{INK}" stroke-width="4"/>'
    # a woven mat where the brothers kneel
    mat = f"M2840,{905} L3990,{900} L4020,{1010} L2810,{1016} Z"
    out += S.path(mat, "#d9a95a", sw=3.5)
    for k in range(1, 12):
        x = 2840 + k * 96
        out += f'<path d="M{x},{904} L{x - 22},{1014}" stroke="#b9853e" stroke-width="3" opacity="0.7"/>'
    out += f'<path d="M2836,{922} L3994,{917} M2818,{996} L4012,{991}" stroke="#a5452f" stroke-width="5"/>'
    # the cut-away left wall edge
    out += f'<rect x="{L - 40}" y="{WALL_TOP - 40}" width="44" height="{WALL_BOT - WALL_TOP + 44}" fill="#e3c792" stroke="{INK}" stroke-width="4"/>'
    out += f'<path d="M{L - 18},{WALL_BOT} L{L - 18},{SH + 30}" stroke="{INK}" stroke-width="3" opacity="0.5"/>'
    # grain sacks stacked against the right wall
    out += PR.grain_sacks(4520, 880, 0.95, n=6) + PR.grain_sacks(4350, 870, 0.8, n=3) + PR.grain_sacks(2620, 880, 0.75, n=3)
    out += PR.grain_heap(4700, 900, 0.6, size=1.0, seed=2)
    return doc(S.g(out, filter="wobble"), defs)


BANNERS = [(3045, 214), (4100, 214)]


def banner_svg(x, y):
    """A long red-and-gold cloth banner hanging from the frieze (it sways a little)."""
    w, h = 96, 330
    out = f'<rect x="{x - w / 2 - 10}" y="{y - 8}" width="{w + 20}" height="16" rx="6" fill="{P["wood"]}" stroke="{INK}" stroke-width="4"/>'
    body = f"M{x - w / 2},{y} L{x + w / 2},{y} L{x + w / 2},{y + h} L{x},{y + h + 40} L{x - w / 2},{y + h} Z"
    out += S.path(body, "#c0473b", sw=4)
    for k, yy in enumerate((y + 40, y + 120, y + 200, y + 280)):
        out += f'<rect x="{x - w / 2 + 3}" y="{yy}" width="{w - 6}" height="14" fill="#e8c25a"/>'
    out += (f'<circle cx="{x}" cy="{y + 160}" r="24" fill="#e8c25a" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y + 160}" r="10" fill="#3f6fa8"/>')
    for k in range(7):
        xx = x - w / 2 + 8 + k * (w - 16) / 6
        yy = y + h + 40 * (1 - abs(xx - x) / (w / 2))
        out += f'<path d="M{f1(xx)},{f1(yy - 4)} l0,22" stroke="#e8c25a" stroke-width="5" stroke-linecap="round"/>'
    return doc(S.g(out, filter="wobble-fine"))


def add_banners(sc, ctx, z=10.2):
    """The banners sway on GLOBAL film time, so s12's end and s13's start match in the cross-dissolve."""
    for i, (x, y) in enumerate(BANNERS):
        sc.add(f"banner{i}", banner_svg(x, y), z=z, seed=125 + i,
               motion=lambda t, x=x, y=y, i=i: Tf(rot=1.6 * math.sin(2 * math.pi * ((ctx.start + t) / 3.4 + 0.37 * i)),
                                                  px=x, py=y))


def hall_light_svg():
    """Daylight falling in through the doorway (static, shared with s13 so the dissolve matches)."""
    return doc(f'<path d="M2600,350 L2800,350 L3150,{G + 20} L2650,{G + 20} Z" fill="#fff3c8" opacity="0.45" '
               f'filter="url(#blur-md)"/>')


def hall_front_svg():
    """Foreground: a big column at the far left of the hall shot and a jar of grain at the right."""
    out = PR.egypt_column(2700, SH + 60, 1.85, height=520)
    out += PR.jar(4620, 1130, 1.15) + PR.grain_sacks(4500, 1150, 1.0, n=2)
    return doc(out)


def seat_svg():
    return doc(C.ground_shadow(CHX, G, SC, 170) + PR.egypt_throne(CHX, G, SC, -1))


def joseph_frames():
    """Joseph in the hall: seated, standing up surprised (hand to heart), standing, blinks. Standing frames are drawn
    at SEAT_X (the layer slides them to JX), so the cut from the seat has no jump."""
    def Jsit(expr):
        return doc(C.joseph(SEAT_X, G, SC, -1, pose="ride", expr=expr, attire="ruler"))

    def Jst(pose, expr):
        return doc(C.ground_shadow(SEAT_X, G, SC, 120) + C.joseph(SEAT_X, G, SC, -1, pose=pose, expr=expr, attire="ruler"))
    return [Jsit("kind"), Jsit(blink("kind")),                     # 0, 1
            Jst("cry", "surprised"), Jst("stand", "kind"),         # 2, 3
            Jst("stand", blink("kind")), Jst("stand", "sad")]      # 4, 5


def brother_frames(k):
    x, y, s, v = brother_pos(k)

    def B(pose, expr):
        return doc(C.ground_shadow(x, y, s, 130 if pose == "bow" else 110) +
                   C.brothers(x, y, s, 1, variant=v, pose=pose, expr=expr, staff=False))
    return [B("stand", "worried"), B("stand", blink("worried")),   # 0, 1
            B("bow", "worried"), B("bow", "puzzled"),              # 2, 3
            B("bow", blink("worried")), B("bow", "ashamed")]       # 4, 5


def servant_frames(i):
    x, v, pose = SERVANTS[i]

    def E(p, expr=None, f=-1):
        return doc(C.ground_shadow(x, G - 30, SC, 110) +
                   C.egyptian(x, G - 30, SC, f, kind="servant", variant=v, pose=p, expr=expr, item="sack"))
    return [E(pose), E(pose, blink("neutral"))]


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]
    s = SC

    # ---- key times ----
    t_famine = snap(L0.start + 0.1)                     # '饥荒来了': the field withers
    t_empty = snap(L0.at("约瑟的哥哥们") + 0.9)           # '没有粮食吃': the jar topples
    t_go = snap(when(ctx, "就来到埃及买粮"))              # they set off
    t_dip = (L0.end + L1.start) / 2                     # page-turn dip to the hall
    DIP = 0.5
    t_bow = snap(when(ctx, "跪下下拜") - 0.12)            # they kneel and bow
    t_rise = snap(when(ctx, "可是", 1) + 0.05)           # Joseph rises, a hand to his heart
    t_puz = snap(L1.at("他们认不出约瑟") + 0.1)           # puzzled faces
    t_calm = snap(L1.end + 0.25)                        # Joseph's face softens
    t_bub = snap(L2.start + 0.2)                        # the dream bubble rises
    t_jrise = snap(L2.start + 1.2)                      # Joseph's sheaf stands up and glows
    t_sbow = snap(L2.at("哥哥们的麦捆") + 0.1)           # the sheaves bow
    t_true = snap(L2.at("现在真的发生了") + 0.05)          # it has come true
    t_bub_out = min(L2.end - 0.3, T - 1.6)          # the bubble fades
    t_back = t_true + 0.5                               # the camera settles back on the hall shot

    # ---- camera ----
    CA = Cam(1010, 636, 1860)
    CA2 = Cam(1250, 636, 1860)
    CJ = Cam(3880, 640, 1640)                           # closer: Joseph and the front brothers
    CW = Cam(3640, 594, 2080)                           # the dream and the bowing brothers together

    def cam(t):
        if t < t_dip:
            u = M.progress(t, t_go - 0.2, t_dip + 0.3, "sine")
            c = Cam(M.lerp(CA.x, CA2.x, u), CA.y, CA.w)
        else:
            c = CH
            k1 = M.progress(t, t_rise - 0.3, t_rise + 1.0, "sine") * (1 - M.progress(t, t_bub - 0.6, t_bub + 0.6, "sine"))
            c = Cam(M.lerp(c.x, CJ.x, k1), M.lerp(c.y, CJ.y, k1), M.lerp(c.w, CJ.w, k1))
            k2 = M.progress(t, t_bub - 0.3, t_bub + 1.0, "sine") * (1 - M.progress(t, t_back, min(T - 0.8, t_back + 1.5), "sine"))
            c = Cam(M.lerp(c.x, CW.x, k2), M.lerp(c.y, CW.y, k2), M.lerp(c.w, CW.w, k2))
        return clamp_cam(c, SW, SH)
    sc.camera = cam

    def dip_paper(frame, t, view):
        a = max(0.0, 1 - abs(t - t_dip) / DIP)
        if a <= 0.003:
            return frame
        a = 0.5 - 0.5 * math.cos(math.pi * a)
        from PIL import Image
        ov = Image.new("RGBA", frame.size, (247, 240, 226, int(255 * a)))
        return Image.alpha_composite(frame, ov)

    # ============================================================== Canaan
    sc.add("c_sky", canaan_sky_svg(), z=0, wc=0.5, seed=101)
    sc.add("c_sunglow", doc(f'<circle cx="1480" cy="210" r="300" fill="#fff0b0" opacity="0.6" filter="url(#blur-lg)"/>'),
           z=0.2, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.35 + 0.65 * M.progress(t, t_famine, t_famine + 1.6, "sine")
                               + 0.08 * math.sin(2 * math.pi * t / 1.7)))
    sc.add("c_rays", sun_rays_svg(), z=0.1, wc=0, blend="screen",
           motion=lambda t: Tf(rot=4 * t, px=SUN[0], py=SUN[1], alpha=0.6 + 0.4 * M.progress(t, t_famine, t_famine + 1.5)))
    sc.add("c_land", canaan_land_svg(), z=1, seed=102)
    drys = [0.0, 0.25, 0.5, 0.75, 1.0]
    sc.add("c_field", [canaan_field_svg(d) for d in drys], z=1.1, seed=103,
           frame_at=lambda t: float(min(4, max(0, int((t - t_famine) / 0.3) + 1))) if t >= t_famine else 0.0)
    sc.add("c_props", canaan_props_svg(), z=1.12, seed=108)
    sc.add("c_shimmer", [shimmer_svg(k) for k in range(3)], z=1.15, wc=0, frame_at=lambda t: float(int(t * 5) % 3),
           motion=lambda t: Tf(alpha=0.7 * M.progress(t, t_famine + 0.3, t_famine + 1.5, "sine")
                               * (1 - M.progress(t, t_dip, t_dip + 0.1))))

    # Jacob and Benjamin by the tents; Jacob waves them off
    jx, jy, js = JACOB
    J = lambda pose, expr=None: doc(C.ground_shadow(jx, jy, js, 120) +            # noqa: E731
                                    C.jacob(jx, jy, js, 1, pose=pose, expr=expr))
    jfr = [J("stand", "worried"), J("stand", blink("worried")), J("bless", "kind"), J("bless", blink("kind"))]
    t_bless = snap(t_go + 0.15)
    sc.add("jacob", jfr, z=1.3, seed=104,
           frame_at=cuts(with_blinks([(0, 0), (t_bless, 2)], {0: 1, 2: 3}, [1.6, 3.9, 6.0])),
           motion=M.combine(M.breathe(0.012, 3.2, pivot=(jx, jy)), dip(t_bless, js, (jx, jy), 5),
                            lambda t: Tf(rot=2.5 * math.sin(2 * math.pi * (t - t_bless) / 0.8) if t > t_bless + 0.3 else 0.0,
                                         px=jx, py=jy)))
    bx = jx + 130 * js
    Bn = lambda pose, expr=None: doc(C.ground_shadow(bx, jy, js, 90) +              # noqa: E731
                                     C.brothers(bx, jy, js, 1, variant="benjamin", pose=pose, expr=expr))
    sc.add("benjamin", [Bn("stand", "sad"), Bn("stand", blink("sad")), Bn("stand", "worried")], z=1.31, seed=105,
           frame_at=cuts(with_blinks([(0, 0), (snap(t_go + 0.4), 2)], {0: 1}, [2.7, 5.2])),
           motion=M.combine(M.breathe(0.015, 2.5, pivot=(bx, jy)), dip(snap(t_go + 0.4), js, (bx, jy), 4)))

    # the empty jar topples over at '没有粮食吃'
    jar_x, jar_y = 150, G - 2
    sc.add("jar", doc(C.ground_shadow(jar_x, jar_y, 1.0, 90) + PR.jar(jar_x, jar_y, 0.95)), z=1.5, seed=106,
           motion=lambda t: Tf(rot=84 * M.ease("bounce")(M.progress(t, t_empty, t_empty + 0.55, "linear")),
                               px=jar_x + 38, py=jar_y))
    sc.add("jar_dust", [doc(puff_markup(jar_x + 120, jar_y - 18, 70 + 20 * k, 26 + 6 * k, seed=k)) for k in range(3)],
           z=1.55, wc=0.6, frame_at=lambda t: float(min(2, max(0, int((t - t_empty - 0.35) / 0.12)))),
           motion=lambda t: Tf(alpha=M.progress(t, t_empty + 0.3, t_empty + 0.4) * (1 - M.progress(t, t_empty + 0.8, t_empty + 1.2))))

    # the brothers' caravan: a line facing right; they set off at '就来到埃及买粮'
    WALK_P = 0.3
    STEP = 70 * s
    n_steps = int((t_dip + 0.6 - t_go) / WALK_P) + 1
    fa_w, dxw, dyw, _ = step_walk(t_go + 0.1, n_steps, STEP, WALK_P, s)

    def caravan(mode):
        out = ""
        for i, (v, dx) in enumerate(reversed(LINE)):
            if v == "donkey":
                continue
            x = X0 + dx * s
            idx = LINE.index((v, dx))
            if mode in ("a", "b"):
                pose = "walk_a" if (idx % 2 == 0) == (mode == "a") else "walk_b"
                expr = "worried"
            else:
                pose, expr = "stand", mode
            out += C.ground_shadow(x, G, s, 110) + C.brothers(x, G, s, 1, variant=v, pose=pose, expr=expr)
        return doc(out)
    cfr = [caravan("worried"), caravan("sad"), caravan("a"), caravan("b")]
    base_c = cuts([(0, 0), (t_empty + 0.3, 1)])

    def car_fa(t):
        w = fa_w(t)
        return base_c(t) if w is None else 2.0 + w
    pvc = (X0 - 700 * s, G)
    sc.add("caravan", cfr, z=1.6, seed=107, frame_at=car_fa,
           motion=M.combine(lambda t: Tf(dx=dxw(t), dy=dyw(t)), M.breathe(0.01, 3.0, pivot=pvc),
                            dip(snap(t_empty + 0.3), s, pvc, 6)))
    # the donkeys with grain sacks (empty sacks folded on the saddle: sacks=0 .. they go to buy grain)
    speed = STEP / WALK_P
    for i, (v, dx) in enumerate([e for e in LINE if e[0] == "donkey"]):
        x = X0 + dx * s
        frames = [doc(C.ground_shadow(x, G, s, 220) + PR.donkey(x, G, s, 1, pose="walk", phase=k / 8, sacks=2))
                  for k in range(8)]
        frames.append(doc(C.ground_shadow(x, G, s, 220) + PR.donkey(x, G, s, 1, pose="stand", sacks=2)))
        t0 = t_go + 0.1

        def d_dx(t, t0=t0):
            return speed * max(0.0, t - t0) * M.progress(t, t0, t0 + 0.3, "sine") if t > t0 else 0.0

        def d_fa(t, t0=t0, i=i, d_dx=d_dx):
            if t < t0:
                return 8.0
            return float(int((d_dx(t) / (87 * s) + 0.3 * i) * 8) % 8)
        sc.add(f"donkey{i}", frames, z=1.6 + 0.01 * (i + 1), seed=110 + i, frame_at=d_fa,
               motion=M.combine(lambda t, d_dx=d_dx: Tf(dx=d_dx(t)),
                                # an idle head-bob while standing (tail swish suggested by a tiny sway)
                                lambda t, x=x, i=i: Tf(rot=0.8 * math.sin(2 * math.pi * (t / 2.1 + 0.4 * i)), px=x, py=G)
                                if t < t0 else Tf()))

    # ============================================================== the hall
    sc.add("h_back", hall_back_svg(), z=10, seed=120)
    sc.add("h_light", hall_light_svg(), z=10.1, wc=0, blend="screen")
    sc.add("h_seat", seat_svg(), z=10.5, seed=121)
    add_banners(sc, ctx)
    # servants by the grain sacks (they stay; s13 sends them out)
    for i in range(len(SERVANTS)):
        x = SERVANTS[i][0]
        sc.add(f"servant{i}", servant_frames(i), z=10.6 + 0.01 * i, seed=122 + i,
               frame_at=cuts(with_blinks([(0, 0)], {0: 1}, [8.0 + 2.3 * i, 12.5 + i, 16.4 - i])),
               motion=M.breathe(0.012, 2.8 + 0.3 * i, pivot=(x, G - 30), phase=0.3 * i))

    # the brothers before Joseph: they bow (closest first), look up puzzled, bow lower when the dream comes true
    order = sorted(range(10), key=lambda k: -FORM[k][0])
    for k in range(10):
        x, y, s_, v = brother_pos(k)
        rank = order.index(k)
        tb = snap(t_bow + 0.045 * rank)
        tp = snap(t_puz + 0.05 * rank)
        tw = snap(t_bub + 0.3 + 0.04 * rank)
        ent = [(0, 0), (tb, 2), (tp, 3), (tw, 2)]
        pv = (x, y)
        sc.add(f"bro{k}", brother_frames(k), z=11 + (0 if FORM[k][1] else 0.5) + 0.01 * k, seed=130 + k,
               frame_at=cuts(with_blinks(ent, {0: 1, 2: 4}, [7.6 + 0.07 * k, 13.6 + 0.11 * k, 18.6 + 0.09 * k])),
               motion=M.combine(M.breathe(0.012, 2.7 + 0.13 * k, pivot=pv, phase=0.17 * k),
                                hop(tb - 0.12, [(0, {"dy": 0, "sy": 1}), (0.12, {"dy": 10 * s_, "sy": 0.93}),
                                                (0.3, {"dy": 0, "sy": 1.02}), (0.42, {"dy": 0, "sy": 1})], pv,
                                    ["in", "out", "sine"]),
                                dip(tp, s_, pv, 5),
                                # puzzled: heads tilt a little
                                hop(tp, [(0, {"rot": 0}), (0.3, {"rot": (3 if k % 2 else -3)}), (1.3, {"rot": (3 if k % 2 else -3)}),
                                         (1.7, {"rot": 0})], pv),
                                # 'now it came true': a deeper bow in time with the sheaves
                                hop(t_true + 0.03 * rank, [(0, {"dy": 0, "sy": 1}), (0.3, {"dy": 8 * s_, "sy": 0.94}),
                                                           (0.9, {"dy": 8 * s_, "sy": 0.94}), (1.3, {"dy": 0, "sy": 1})], pv)))
    # dust puffs as they kneel
    dpts = [brother_pos(k) for k in range(10) if not FORM[k][1]]
    sc.add("bow_dust", [doc("".join(puff_markup(x + 60 * s, y - 10, 46 + 12 * j, 18 + 4 * j, seed=j + int(x))
                                    for x, y, _, _ in dpts)) for j in range(3)], z=11.8, wc=0.6,
           frame_at=lambda t: float(min(2, max(0, int((t - t_bow - 0.1) / 0.12)))),
           motion=lambda t: Tf(alpha=0.75 * M.progress(t, t_bow + 0.05, t_bow + 0.15) * (1 - M.progress(t, t_bow + 0.6, t_bow + 1.0))))
    # '?' marks over some brothers
    qs = []
    for k in (5, 7, 9, 2, 3):
        x, y, s_, v = brother_pos(k)
        hx, hy = C.body_points(C.brothers, x, y, s_, 1, variant=v, pose="bow", staff=False)["head"]
        qs.append((hx + 10, hy - 95))
    for i, (qx, qy) in enumerate(qs):
        tq = snap(t_puz + 0.12 * i)
        sc.add(f"q{i}", doc(f'<text x="{qx}" y="{qy}" font-family="LXGW WenKai" font-weight="bold" font-size="64" '
                            f'fill="#fbf3e2" stroke="{INK}" stroke-width="4" paint-order="stroke" text-anchor="middle">?</text>'),
               z=12, wc=0, seed=150 + i,
               motion=M.combine(hop(tq, [(0, {"s": 0.01, "alpha": 0}), (0.18, {"s": 1.2, "alpha": 1}), (0.3, {"s": 1.0}),
                                         (1.5, {"s": 1.0, "alpha": 1}), (1.9, {"s": 0.8, "alpha": 0})], (qx, qy + 10)),
                                lambda t, i=i: Tf(rot=6 * math.sin(2 * math.pi * (t / 0.9 + 0.3 * i)), px=qx, py=qy)))

    # Joseph: seated; rises with a start (hand to heart); softens; watches the dream come true
    jf = joseph_frames()
    j_ent = [(0, 0), (t_rise, 2), (t_calm, 5), (snap(t_bub - 0.1), 3)]
    pvj = (JX, G)
    sc.add("joseph", jf, z=11.6, seed=160,
           frame_at=cuts(with_blinks(j_ent, {0: 1, 3: 4}, [7.7, 13.2, 16.0, 18.4, 19.9])),
           motion=M.combine(lambda t: Tf(dx=(JX - SEAT_X) * M.progress(t, t_rise, t_rise + 0.32, "out")),
                            M.breathe(0.01, 3.0, pivot=pvj),
                            happy_hop(t_rise, s, (SEAT_X, G), 16), dip(t_calm, s, pvj, 5), dip(snap(t_bub - 0.1), s, pvj, 4),
                            # a small start: a quick shiver
                            lambda t: Tf(rot=1.6 * math.sin(2 * math.pi * (t - t_rise) / 0.18)
                                         * (1 - M.progress(t, t_rise + 0.3, t_rise + 1.0)) if t > t_rise + 0.3 else 0.0,
                                         px=JX, py=G)))
    # surprise lines by his head
    hpj = C.body_points(C.joseph, JX, G, s, -1, pose="cry", attire="ruler")["head"]
    lines = ""
    for a in (-150, -120, -90):
        r = math.radians(a)
        x0, y0 = hpj[0] + 80 * math.cos(r), hpj[1] + 80 * math.sin(r)
        x1, y1 = hpj[0] + 112 * math.cos(r), hpj[1] + 112 * math.sin(r)
        lines += f'<path d="M{f1(x0)},{f1(y0)} L{f1(x1)},{f1(y1)}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    sc.add("start_lines", doc(S.g(lines, filter="wobble-fine")), z=11.7, wc=0,
           motion=lambda t: Tf(alpha=M.progress(t, t_rise + 0.25, t_rise + 0.35) * (1 - M.progress(t, t_rise + 1.1, t_rise + 1.4))))

    # ---- the dream bubble: the sheaves above the brothers and Joseph ----
    BX, BY, BW, BH = 3590, 318, 1560, 380
    head = C.body_points(C.joseph, JX, G, s, -1, pose="stand", attire="ruler")["head_top"]
    tail = (head[0] + 30, head[1] - 40)
    sheaf_y = BY + 100
    sx_list = []
    for k in range(10):
        x, y, s_, v = brother_pos(k)
        sx_list.append((x + 40 * s, sheaf_y - (18 if FORM[k][1] else 0), 0.5 if FORM[k][1] else 0.54, k))
    sx_list.sort(key=lambda e: e[1])

    def bubble(rise, glow, bowk):
        inner = f'<rect x="{BX - BW}" y="{BY - BH}" width="{2 * BW}" height="{2 * BH}" fill="#fbf1d9"/>'
        inner += S.path(S.hill(BX - BW, BX + BW, sheaf_y + 4, 16, seed=3, bottom=BY + BH, bumps=4), "#e7cf86", sw=3)
        for i, (x, y, sz, k) in enumerate(sx_list):
            inner += PR.wheat_sheaf(x, y, sz, 1, bow=bowk, seed=k)
        inner += PR.wheat_sheaf(JX - 10, sheaf_y + 6, 0.62, -1, rise=rise, glow=glow, seed=12)
        return doc(PR.dream_bubble(BX, BY, BW, BH, tail=tail, inner=inner, seed=4))
    bstates = [(0.35, 0.0, 0.0), (0.6, 0.3, 0.0), (0.85, 0.65, 0.0), (1.0, 1.0, 0.0)]
    bstates += [(1.0, 1.0, k / 8) for k in range(1, 9)]
    bfr = [bubble(*st) for st in bstates]

    def bub_fa(t):
        if t < t_jrise:
            return 0.0
        if t < t_sbow:
            return float(min(3, int((t - t_jrise) / 0.16) + 1))
        return float(min(11, 3 + int((t - t_sbow) / 0.15) + 1))

    def bub_m(t):
        u = M.progress(t, t_bub, t_bub + 0.5, "back")
        a = M.progress(t, t_bub, t_bub + 0.18) * (1 - M.progress(t, t_bub_out, t_bub_out + 0.7, "sine"))
        k = 0.06 + 0.94 * u
        # gentle float, and a little nod with the brothers when it comes true
        nod = 10 * math.sin(math.pi * M.progress(t, t_true, t_true + 1.2, "linear"))
        return Tf(sx=k, sy=k, px=tail[0], py=tail[1], alpha=a,
                  dy=4 * math.sin(2 * math.pi * t / 2.6) + nod)
    sc.add("bubble", bfr, z=13, seed=170, frame_at=bub_fa, motion=bub_m)
    # golden twinkles over the bubble and the brothers when it comes true
    tw_pts = [(BX - 600, BY - 120, 20), (BX - 200, BY - 160, 16), (BX + 300, BY - 140, 18), (BX + 640, BY - 60, 22),
              (3000, 690, 16), (3420, 700, 18), (3800, 690, 15), (JX + 70, 560, 18)]
    sc.add("twinkles", [doc(twinkles_markup(tw_pts, k)) for k in range(3)], z=13.5, wc=0,
           frame_at=lambda t: float(int(t * 6) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_true, t_true + 0.3) * (1 - M.progress(t, t_bub_out + 0.2, t_bub_out + 0.9))))

    sc.add("h_front", hall_front_svg(), z=20, seed=180)

    sc.fx.append(FX.motes((2700, 300, 4700, 950), count=26, t0=t_dip, seed=31, alpha=110))
    sc.fx.append(dip_paper)

    # ---- sound ----
    sc.sfx("wind_hot", 0.0, dur=t_dip + 0.3, gain_db=-15, fade_in=0.8, fade_out=0.5)
    sc.sfx("heat", t_famine, dur=t_dip - t_famine, gain_db=-20, fade_in=0.8, fade_out=0.4)
    sc.sfx("wither", t_famine + 0.1, gain_db=-12)
    sc.sfx("thud", t_empty + 0.32, gain_db=-8)
    sc.sfx("footsteps", t_go + 0.1, dur=t_dip - t_go + 0.2, gain_db=-14, fade_out=0.4)
    sc.sfx("whoosh", t_dip - 0.35, gain_db=-16)
    sc.sfx("crowd", t_dip, dur=T - t_dip, gain_db=-26, fade_in=0.6, fade_out=0.8)
    sc.sfx("thud", t_bow + 0.12, gain_db=-10)
    sc.sfx("thud", t_bow + 0.3, gain_db=-13)
    sc.sfx("cloth", t_bow + 0.05, gain_db=-12)
    sc.sfx("pop", t_rise, gain_db=-12)
    sc.sfx("pop", t_puz + 0.05, gain_db=-14)
    sc.sfx("pop", t_puz + 0.3, gain_db=-16)
    sc.sfx("chime", t_bub, gain_db=-11)
    sc.sfx("grow", t_jrise, gain_db=-16)
    sc.sfx("sparkle", t_sbow + 0.2, gain_db=-13)
    sc.sfx("sparkle", t_true + 0.1, gain_db=-11)
    return sc
