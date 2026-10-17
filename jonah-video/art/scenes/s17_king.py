"""Scene 17 — the king of Nineveh repents and sends out his decree (Jonah 3:6-9), v2.

One wide 4800 x 1440 stage, no cuts: the palace throne room on the left (the same purple-curtained portico,
throne and king as v1 s10), its terrace and steps, then the street outside — a little animal yard with a feed
manger and a stone water trough, and a street where families live. The camera starts close on the king and
travels right with the heralds and the decree.

  line 0  "国王听说了，"            a messenger in sackcloth tells the seated king the news (sound arcs) and points
                                    out to the city; the king is startled ("!").
          "也从宝座上站起来，"      he leans forward and rises from his throne (squash, hard cut, spring up) and
                                    steps forward.
          "脱下漂亮的王袍，"        he lifts off his tall crown, turns to the throne and — in a cloth puff — his purple
                                    robe comes off and lands folded on the throne seat with the crown on top...
          "换上粗麻布衣服，"        ...and he stands in scratchy burlap sackcloth; he turns back, shivers.
          "坐在灰堆里，"            a heap of ashes puffs up in front of the throne and he sits down in it.
          "表示真心认错。"          he bows his head, sorry; the messenger and the scribe bow their heads too.
  line 1  "国王又派人在全城宣告："  the king lifts his head and speaks; the messenger and the scribe nod and walk out
                                    onto the terrace one after the other (the camera goes with them); the scribe
                                    unrolls the decree by the column while the messenger blows his long bronze horn
                                    (s16's horn) at the open end; far heralds answer from the roofs, then kneel.
  line 2  "所有的人和牛羊，都不可以吃，"  (the king's words, read from the scroll) the camera glides on to the yard:
                                    a cow and a goat munch at the manger — the farmer lays a plank lid over it,
                                    they lift their heads ("?").
          "也不可以喝。"            his daughter pulls a reed mat over the water trough; the lamb looks up ("?").
  line 3  "人和牛羊，都要穿上麻布衣服，"  pop, pop, pop: the cow, goat, sheep, lamb and donkey each get a little
                                    sackcloth blanket (cloth puffs and happy hops).
          "诚心向上帝呼求。"        the farmer, his daughter and the neighbours kneel and pray; the animals bow;
                                    the camera drifts on along the street.
  line 4  "每个人都要改掉坏行为，"  two neighbours who were shouting and pointing at each other stop and hang their
                                    heads; a young man lays a kind hand on an old neighbour's shoulder;
          "不再欺负别人。"          a big boy who had snatched a little girl's toy lamb gives it back; the two men
                                    step together and shake hands.
          "说不定上帝会可怜我们，"  everyone kneels and looks up hopefully;
          "我们就能活下来！"        peaceful, hopeful faces (the children smile); the camera tilts up with their gaze
                                    as a soft warm light begins to seep through the clouds (God's full mercy and the
                                    joy come in s18). Calm hold for the dissolve.

Camera: every pan stays under ~20 output px per frame (long pans widen the view a little in the middle, and the
viewport is clamped to the painted stage). Doves drift across the street sky; a crier on a roof keeps reading.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a small squash /
dip, or under a cloth puff. All times are derived from the narration chunks.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s10_repent as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 5400, 1440
INK = P["ink"]

# ------------------------------------------------------------------ palace geometry (v1 s10, widened)
LINTEL_Y0, LINTEL_Y1 = 300, 418
DAIS_BACK, DAIS_Y, DAIS_FRONT, DAIS_BOTTOM = 1055, 1150, 1187, 1295
WALL_X1 = 900
COL1_X, COL2_X = 925, 1500
COL_W = 80
DAIS_X1 = 1880                       # front-right corner of the dais / terrace
STEPS = (1540, 1840)                 # front steps down to the street (x range of the top step)

KS = 1.15                            # king scale
THRONE_X, THRONE_Y = 430, 1135
SPOT_X, SPOT_Y = 800, 1153           # where the king stands and sits in the ashes
RISE_X = 535                         # where he first stands up (right in front of the seat)
BUNDLE_X, BUNDLE_Y = THRONE_X - 8, THRONE_Y - 74 * KS

MSG = dict(x=1130, y=1157, s=1.08, v=2)     # the messenger (later blows the horn)
SCR = dict(x=1005, y=1100, s=0.98, v=3)     # the king's scribe (later reads the decree)
HORN_X, READ_X = 1760, 1450                  # their places on the terrace (horn at the open end)

# ------------------------------------------------------------------ street / yard geometry
BACK_Y = 1000                        # ground line of the house row at the back of the street
FENCE_Y = 1135                       # the yard fence (behind the animals)

MANGER = (2268, 2468, 1135, 1240)    # x0, x1, top, ground
TROUGH = (2850, 3100, 1222, 1292)
FARMER = dict(x=2370, y=1185, s=0.9, v=0)
GIRL_Y = dict(x=2965, y=1205, s=0.9, v=3)
COW = dict(x=2600, y=1265, s=1.0, f=-1)
GOAT = dict(x=2150, y=1275, s=0.95, f=1)
SHEEP = dict(x=2765, y=1308, s=1.05, f=1)
LAMB = dict(x=3162, y=1268, s=0.68, f=-1)
DONKEY = dict(x=3330, y=1150, s=0.78, f=-1)

MAN_A = dict(x=3900, y=1272, s=1.0, v=1)
MAN_B = dict(x=4350, y=1278, s=1.0, v=3)
SHAKE_DX = 99                        # each man steps this far toward the other to shake hands
KID_G = dict(x=4600, y=1306, s=0.85, v=1)    # the little girl
KID_B = dict(x=4815, y=1298, s=1.0, v=0)     # the big boy
MOTHER = dict(x=4995, y=1212, s=0.92, v=2)

HOUSES = ((1180, 0, 1), (1620, 2, -1), (2190, 1, 1), (2600, 3, -1), (3080, 0, 1), (3420, 2, 1), (3880, 1, -1),
          (4260, 3, 1), (4720, 0, -1), (5150, 2, 1))
ROOF_Y = {0: 770, 1: 620, 2: 764, 3: 733}   # roof surface of each house variant at scale 0.45


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ timing helpers


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval so no frame is ambiguous."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    """[(t, frame index)] -> frame_at with HARD cuts (indices may go back and forth)."""
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


def hop(t0, keys, pivot, curves="sine"):
    """Additive keyed bump around t0: keys [(dt, {...})] that start and end at identity."""
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


def dip(t0, s, pivot, depth=9.0):
    """Squash-dip whose bottom is at t0 (where a pose cut hides)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": 0.95}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pivot, ["in", "out", "sine"])


def nod(t0, pivot, deg=3.0, dur=0.5):
    return hop(t0, [(0, {"rot": 0}), (dur * 0.4, {"rot": deg}), (dur, {"rot": 0})], pivot)


def happy_hop(t0, s, pivot, h=18.0):
    return hop(t0, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5 * s, "sy": 0.94}), (0.17, {"dy": -h * s, "sy": 1.04}),
                    (0.34, {"dy": 0, "sy": 0.97}), (0.46, {"dy": 0, "sy": 1})], pivot,
               ["in", "out", "in", "sine"])


def cam_path(keys):
    """keys [(t, Cam, bump)]: sine-eased moves between key cameras; ``bump`` widens the view by that many stage px
    in the middle of the move that starts at the key (a gentle pull-back that keeps long pans calm on screen)."""
    keys = sorted(keys, key=lambda k: k[0])

    def c(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, bump), (t1, b, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                v = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
                w = M.lerp(a.w, b.w, u) + bump * math.sin(math.pi * v)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), M.lerp(a.y, b.y, u), w))
        return keys[-1][1]
    return c


def clamp_cam(c, margin=4):
    """Keep the viewport inside the painted stage."""
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), SH - h / 2 - margin)
    return Cam(x, y, c.w)


def chunk(line, phrase):
    return next(c for c in line.chunks if phrase in c.text)


def within(c, u):
    return c.start + (c.end - c.start) * u


# ============================================================================ sky & city (static backdrops)


def sky_svg():
    defs = S.lin_grad("s17sky", [(0, "#a7a7bf"), (0.35, "#c3bfcb"), (0.68, "#e0d3c6"), (1, "#eedfc2")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="1120" fill="url(#s17sky)"/>', defs)


CLOUDS_BACK = [(1500, 175, 520, 150, 1), (2350, 120, 420, 120, 2), (3150, 205, 560, 160, 3), (4000, 130, 460, 130, 4),
               (4800, 240, 460, 130, 5), (900, 110, 380, 110, 6), (5400, 150, 420, 120, 7)]
CLOUDS_FRONT = [(1900, 330, 360, 100, 11), (2900, 400, 300, 86, 12), (3700, 340, 380, 104, 13),
                (4450, 430, 300, 84, 14), (1250, 470, 260, 74, 15), (5150, 360, 340, 96, 16)]


def clouds_svg(items, fill, shade):
    body = "".join(S.cloud(cx, cy, w, h, fill, seed=sd, puffs=5, sw=3, shade_fill=shade) for cx, cy, w, h, sd in items)
    return doc(S.g(body, filter="wobble"))


def hope_svg():
    """A soft warm light seeping through the clouds at the very end (God's full mercy comes in s18)."""
    defs = S.rad_grad("s17hope", [(0, "#fff6d8", 1), (0.3, "#ffe9b0", 0.7), (0.65, "#ffd88c", 0.25),
                                  (1, "#ffd88c", 0)])
    return doc(f'<ellipse cx="4700" cy="360" rx="1250" ry="560" fill="url(#s17hope)"/>', defs)


def far_svg():
    """Far skyline, the house row at the back of the street, palms and the street ground (static)."""
    defs = (S.lin_grad("s17street", [(0, "#e3cda3"), (0.4, "#dcc191"), (1, "#cfae79")]) +
            S.lin_grad("s17haze", [(0, "#eadccb", 0), (1, "#eadccb", 0.6)]))
    body = PR.nineveh_skyline(980, 5500, 985, scale=0.82, seed=6, haze=0.48, tint="#e2d6c8")
    body += f'<rect x="-20" y="760" width="{SW + 40}" height="240" fill="url(#s17haze)"/>'
    # street ground
    ground = (f'<path d="M-30,{BACK_Y - 12} L{SW + 30},{BACK_Y - 12} L{SW + 30},{SH + 30} L-30,{SH + 30} Z" '
              f'fill="url(#s17street)" stroke="{INK}" stroke-width="3"/>')
    rng = random.Random(4)
    marks = ""
    for _ in range(140):
        x, y = rng.uniform(1700, SW), rng.uniform(BACK_Y + 30, SH - 10)
        w = rng.uniform(14, 40) * (0.5 + (y - BACK_Y) / 500)
        marks += f'<path d="M{f1(x)},{f1(y)} q{f1(w / 2)},{f1(-3)} {f1(w)},0"/>'
    for _ in range(60):
        x, y = rng.uniform(1700, SW), rng.uniform(BACK_Y + 30, SH - 10)
        r = rng.uniform(2.5, 6) * (0.5 + (y - BACK_Y) / 500)
        marks += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r)}" fill="{P["sand_dark"]}" stroke="none"/>'
    ground += (f'<g stroke="{P["sand_dark"]}" stroke-width="2.5" fill="none" opacity="0.5" '
               f'stroke-linecap="round">{marks}</g>')
    body += S.g(ground, filter="wobble")
    # houses along the back of the street, palms between them
    deco = ""
    for x, s, ln in ((1985, 0.46, -0.1), (2850, 0.5, 0.12), (3640, 0.48, -0.08), (4490, 0.5, 0.1),
                     (5330, 0.46, -0.1)):
        deco += PR.palm_tree(x, BACK_Y - 4, s, lean=ln)
    houses = ""
    for x, v, fc in HOUSES:
        houses += PR.house(x, BACK_Y, 0.45, variant=v, facing=fc)
    body += deco + houses
    # pots, a sack and a bench against the house fronts
    body += PR.jar(2030, BACK_Y + 6, 0.42) + PR.jar(2066, BACK_Y + 10, 0.34) + PR.sack(3255, BACK_Y + 14, 0.4, seed=2)
    body += PR.jar(4050, BACK_Y + 8, 0.4, color="#b86a46") + PR.bush(4570, BACK_Y + 12, 0.45, variant=1)
    body += PR.jar(5000, BACK_Y + 8, 0.4) + PR.sack(5040, BACK_Y + 14, 0.36, seed=5)
    return doc(body, defs)


def far_people_svg():
    """The whole city prays: small figures in sackcloth kneeling along the back of the street (static)."""
    rng = random.Random(12)
    body = ""
    for i, x in enumerate((2060, 2330, 2520, 2760, 3060, 3250, 3700, 4020, 4480, 4880, 5120, 5300)):
        y = rng.uniform(1040, 1072)
        s = 0.42 + (y - 1000) * 0.0022
        kind = ("man", "woman", "elder", "child", "woman", "man")[i % 6]
        f = rng.choice((-1, 1))
        body += C.ground_shadow(x, y, s, 150, opacity=0.16)
        body += C.citizen(x, y, s, f, kind=kind, variant=i % 4, pose="kneel_pray", attire="sackcloth")
    return doc(body)


def yard_back_svg():
    """The yard fence (behind the animals) and a hitching post (static)."""
    x0, x1, y = 1985, 3480, FENCE_Y
    ink = INK
    posts, rails = "", ""
    for i, x in enumerate(range(x0, x1 + 1, 95)):
        h = 92 + (i % 2) * 6
        posts += (f'<path d="M{x - 9},{y} L{x - 8},{y - h} Q{x},{y - h - 9} {x + 8},{y - h} L{x + 9},{y} Z" '
                  f'fill="{P["wood"]}" stroke="{ink}" stroke-width="3.5"/>')
    for yy in (y - 70, y - 34):
        rails += (f'<path d="M{x0 - 20},{yy} C{(x0 + x1) / 2},{yy + 6} {(x0 + x1) / 2},{yy - 6} {x1 + 20},{yy}" '
                  f'stroke="{ink}" stroke-width="15" fill="none" stroke-linecap="round"/>'
                  f'<path d="M{x0 - 20},{yy} C{(x0 + x1) / 2},{yy + 6} {(x0 + x1) / 2},{yy - 6} {x1 + 20},{yy}" '
                  f'stroke="{P["wood_light"]}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    body = rails + posts
    # a coil of rope on a post and a little straw on the ground (no food in reach)
    body += PR.rope_coil(2745, y + 4, 0.6) + PR.jar(3225, y + 10, 0.62) + PR.sack(3290, y + 16, 0.55, seed=4)
    return doc(S.g(body, filter="wobble-fine"))


def manger_markup():
    x0, x1, top, gy = MANGER
    ink = INK
    w = x1 - x0
    legs = ""
    for lx in (x0 + 14, x1 - 14):
        legs += (f'<path d="M{lx - 18},{gy} L{lx + 16},{top + 40} M{lx + 18},{gy} L{lx - 16},{top + 40}" '
                 f'stroke="{ink}" stroke-width="13" stroke-linecap="round"/>'
                 f'<path d="M{lx - 18},{gy} L{lx + 16},{top + 40} M{lx + 18},{gy} L{lx - 16},{top + 40}" '
                 f'stroke="{P["wood_dark"]}" stroke-width="6.5" stroke-linecap="round"/>')
    box = (f'<path d="M{x0},{top} L{x1},{top} L{x1 - 14},{top + 52} L{x0 + 14},{top + 52} Z" fill="{P["wood"]}" '
           f'stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
           f'<path d="M{x0 + 6},{top + 18} L{x1 - 6},{top + 18} M{x0 + 10},{top + 35} L{x1 - 10},{top + 35}" '
           f'stroke="{P["wood_dark"]}" stroke-width="2.5" opacity="0.7"/>'
           f'<path d="M{x0 - 6},{top} L{x1 + 6},{top}" stroke="{ink}" stroke-width="12" stroke-linecap="round"/>'
           f'<path d="M{x0 - 6},{top} L{x1 + 6},{top}" stroke="{P["wood_light"]}" stroke-width="6" '
           f'stroke-linecap="round"/>')
    for k in (0.3, 0.7):
        nx = x0 + w * k
        box += f'<circle cx="{f1(nx)}" cy="{top + 9}" r="3" fill="{ink}"/>'
    return S.g(legs + box, filter="wobble-fine")


def hay_markup():
    """Hay heaped in the manger (hidden under the plank lid later)."""
    x0, x1, top, _ = MANGER
    rng = random.Random(8)
    out = (f'<path d="M{x0 + 8},{top + 2} Q{x0 + 30},{top - 26} {(x0 + x1) / 2},{top - 22} '
           f'Q{x1 - 30},{top - 28} {x1 - 8},{top + 2} Z" fill="#e3c26a" stroke="{INK}" stroke-width="3"/>')
    for _ in range(26):
        x = rng.uniform(x0 + 14, x1 - 14)
        y = top - rng.uniform(2, 20)
        a = rng.uniform(-50, 50)
        ln = rng.uniform(14, 26)
        out += (f'<path d="M{f1(x)},{f1(y)} l{f1(ln * math.sin(math.radians(a)))},{f1(-ln * math.cos(math.radians(a)) * 0.5)}" '
                f'stroke="{rng.choice(("#c99a3c", "#f2d98a", "#b48a34"))}" stroke-width="2.6" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def trough_markup():
    x0, x1, top, gy = TROUGH
    ink = INK
    stone, dark, light = P["stone"], P["stone_dark"], P["stone_light"]
    body = (f'<path d="M{x0},{top} L{x1},{top} L{x1 - 6},{gy} L{x0 + 6},{gy} Z" fill="{stone}" stroke="{ink}" '
            f'stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{x0 - 4},{top - 10} L{x1 + 4},{top - 10} L{x1 + 4},{top + 8} L{x0 - 4},{top + 8} Z" '
            f'fill="{light}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{x0 + 30},{top + 26} l18,0 M{x0 + 110},{top + 40} l24,0 M{x1 - 50},{top + 22} l16,0" '
            f'stroke="{dark}" stroke-width="3" stroke-linecap="round"/>')
    # water surface seen over the rim
    body += (f'<path d="M{x0 + 8},{top - 8} Q{(x0 + x1) / 2},{top - 16} {x1 - 8},{top - 8} L{x1 - 8},{top - 2} '
             f'L{x0 + 8},{top - 2} Z" fill="{P["sea_light"]}" stroke="none"/>'
             f'<path d="M{x0 + 30},{top - 10} q14,-4 28,0 M{x0 + 110},{top - 11} q14,-4 28,0" stroke="#e8f6f4" '
             f'stroke-width="3" fill="none" stroke-linecap="round"/>')
    return S.g(body, filter="wobble-fine")


def plank_markup(cx, cy, s=1.0):
    """The wooden lid for the manger, centred at (cx, cy) (two boards and a batten)."""
    w, h = (MANGER[1] - MANGER[0] + 24) * s, 22 * s
    out = (f'<rect x="{f1(cx - w / 2)}" y="{f1(cy - h / 2)}" width="{f1(w)}" height="{f1(h)}" rx="{4 * s}" '
           f'fill="{P["wood_light"]}" stroke="{INK}" stroke-width="{4 * s:.1f}"/>'
           f'<path d="M{f1(cx - w / 2 + 6)},{f1(cy)} L{f1(cx + w / 2 - 6)},{f1(cy)}" stroke="{P["wood_dark"]}" '
           f'stroke-width="{2.5 * s:.1f}"/>'
           f'<rect x="{f1(cx - 9 * s)}" y="{f1(cy - h / 2 - 3 * s)}" width="{18 * s}" height="{f1(h + 6 * s)}" '
           f'fill="{P["wood"]}" stroke="{INK}" stroke-width="{3 * s:.1f}"/>')
    return S.g(out, filter="wobble-fine")


def mat_markup(cx, cy, s=1.0):
    """A woven reed mat (water-trough cover), centred at (cx, cy)."""
    w, h = (TROUGH[1] - TROUGH[0] + 26) * s, 30 * s
    out = (f'<rect x="{f1(cx - w / 2)}" y="{f1(cy - h / 2)}" width="{f1(w)}" height="{f1(h)}" rx="{6 * s}" '
           f'fill="#d8b36a" stroke="{INK}" stroke-width="{3.5 * s:.1f}"/>')
    for k in range(1, 12):
        x = cx - w / 2 + w * k / 12
        out += (f'<path d="M{f1(x)},{f1(cy - h / 2 + 3)} L{f1(x - 4 * s)},{f1(cy + h / 2 - 3)}" stroke="#a9843f" '
                f'stroke-width="{2.4 * s:.1f}"/>')
    for k in (-1, 1):
        out += (f'<path d="M{f1(cx + k * w / 2)},{f1(cy - 3)} l{f1(k * 8 * s)},4 M{f1(cx + k * w / 2)},{f1(cy + 4)} '
                f'l{f1(k * 9 * s)},2" stroke="#a9843f" stroke-width="{2.4 * s:.1f}" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


# ============================================================================ palace (adapted from v1 s10)


def palace_svg():
    defs = (S.lin_grad("s10wall", [(0, "#dcc093"), (1, "#c9a774")]) +
            S.lin_grad("s10col", [(0, "#efdcb8"), (0.55, "#dfc495"), (1, "#c8a571")], x2=1, y2=0) +
            S.lin_grad("s10curt", [(0, "#8a5cae"), (1, "#5f3c80")]) +
            S.lin_grad("s10floor", [(0, "#cfb184"), (1, "#e3cba0")]) +
            S.lin_grad("s10front", [(0, "#c49e6a"), (1, "#a9834f")]) +
            S.lin_grad("s10shadow", [(0, INK, 0.35), (1, INK, 0)]))
    ink = INK
    wall = (f'<rect x="-30" y="{LINTEL_Y1 - 10}" width="{WALL_X1 + 30}" height="{DAIS_BACK - LINTEL_Y1 + 20}" '
            f'fill="url(#s10wall)" stroke="{ink}" stroke-width="4"/>')
    bricks = ""
    r = random.Random(3)
    y = LINTEL_Y1 + 40
    row = 0
    while y < DAIS_BACK:
        bricks += f'<path d="M-30,{y} L{WALL_X1},{y}"/>'
        off = 0 if row % 2 else 45
        for x in range(-30 + off, WALL_X1, 90):
            if r.random() < 0.55:
                bricks += f'<path d="M{x},{y - 40} L{x},{y}"/>'
        y += 40
        row += 1
    wall += f'<g stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.55" fill="none">{bricks}</g>'
    wall += (f'<rect x="-30" y="{LINTEL_Y1 + 22}" width="{WALL_X1 + 30}" height="56" fill="#3f79a8" '
             f'stroke="{ink}" stroke-width="3.5"/>' + V.rosettes(10, WALL_X1 - 20, LINTEL_Y1 + 50, 72, 19))
    wall += (f'<rect x="-30" y="{DAIS_BACK - 64}" width="{WALL_X1 + 30}" height="50" fill="#4a86b2" '
             f'stroke="{ink}" stroke-width="3.5"/>'
             + "".join(f'<path d="M{x},{DAIS_BACK - 22} l22,-22 l22,22" fill="none" stroke="#f3e6c8" '
                       f'stroke-width="4"/>' for x in range(-20, WALL_X1 - 30, 44)))
    # royal curtain behind the throne
    cx0, cx1, ct, cb = 262, 640, LINTEL_Y1 + 92, DAIS_BACK - 64
    folds = ""
    n = 7
    for i in range(n + 1):
        x = cx0 + (cx1 - cx0) * i / n
        folds += (f'<path d="M{f1(x + 22)},{ct + 8} C{f1(x + 30)},{ct + 240} {f1(x + 14)},{cb - 160} '
                  f'{f1(x + 26)},{cb - 6}" stroke="#4d2f6a" stroke-width="7" opacity="0.45" fill="none"/>')
    curtain = (f'<path d="M{cx0},{ct} L{cx1},{ct} L{cx1 + 6},{cb} '
               + " ".join(f'Q{f1(cx1 - (cx1 - cx0) * (i + 0.5) / n)},{cb + 22} {f1(cx1 - (cx1 - cx0) * (i + 1) / n)},{cb}'
                          for i in range(n))
               + f' Z" fill="url(#s10curt)" stroke="{ink}" stroke-width="4"/>')
    fringe = "".join(f'<path d="M{f1(x)},{cb + 4} l0,22" stroke="{P["crown"]}" stroke-width="5" '
                     f'stroke-linecap="round"/>' for x in range(cx0 + 8, cx1, 16))
    border = (f'<path d="M{cx0 + 18},{ct + 20} L{cx0 + 18},{cb - 14} M{cx1 - 18},{ct + 20} L{cx1 - 14},{cb - 14}" '
              f'stroke="{P["crown"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    emblem = (f'<circle cx="{(cx0 + cx1) / 2}" cy="{ct + 130}" r="54" fill="{P["crown"]}" stroke="{ink}" '
              f'stroke-width="4"/>' + V.rosettes((cx0 + cx1) / 2, (cx0 + cx1) / 2, ct + 130, 100, 44,
                                                 fill="#fff3d6", centre="#c9714a"))
    rod = (f'<rect x="{cx0 - 30}" y="{ct - 12}" width="{cx1 - cx0 + 60}" height="16" rx="8" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/><circle cx="{cx0 - 30}" cy="{ct - 4}" r="15" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/><circle cx="{cx1 + 30}" cy="{ct - 4}" r="15" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/>')
    wall += curtain + folds + border + fringe + emblem + rod
    # a wall niche with a little oil lamp (its flame is a separate flickering layer)
    wall += (f'<path d="M738,{DAIS_BACK - 300} L738,{DAIS_BACK - 410} Q788,{DAIS_BACK - 470} 838,{DAIS_BACK - 410} '
             f'L838,{DAIS_BACK - 300} Z" fill="#a98a5e" stroke="{ink}" stroke-width="4"/>'
             f'<path d="M760,{DAIS_BACK - 302} Q788,{DAIS_BACK - 282} 816,{DAIS_BACK - 302} Z" fill="#c9714a" '
             f'stroke="{ink}" stroke-width="3.5"/>')
    cols = V.column(COL1_X, LINTEL_Y1 - 4, DAIS_BACK + 14) + V.column(COL2_X, LINTEL_Y1 - 4, DAIS_BACK + 14)
    lintel = (f'<rect x="-30" y="{LINTEL_Y0}" width="{COL2_X + 110}" height="{LINTEL_Y1 - LINTEL_Y0}" '
              f'fill="#d6b682" stroke="{ink}" stroke-width="4.5"/>'
              f'<rect x="-30" y="{LINTEL_Y0 + 30}" width="{COL2_X + 110}" height="56" fill="#3f79a8" '
              f'stroke="{ink}" stroke-width="3.5"/>' + V.rosettes(16, COL2_X + 60, LINTEL_Y0 + 58, 76, 20))
    merlons = ""
    for x in range(-20, COL2_X + 60, 92):
        merlons += (f'<path d="M{x},{LINTEL_Y0} L{x},{LINTEL_Y0 - 26} L{x + 14},{LINTEL_Y0 - 26} '
                    f'L{x + 14},{LINTEL_Y0 - 48} L{x + 30},{LINTEL_Y0 - 48} L{x + 30},{LINTEL_Y0 - 66} '
                    f'L{x + 46},{LINTEL_Y0 - 66} L{x + 46},{LINTEL_Y0 - 48} L{x + 62},{LINTEL_Y0 - 48} '
                    f'L{x + 62},{LINTEL_Y0 - 26} L{x + 76},{LINTEL_Y0 - 26} L{x + 76},{LINTEL_Y0} Z" '
                    f'fill="#cfae79" stroke="{ink}" stroke-width="4"/>')
    under = (f'<rect x="-30" y="{LINTEL_Y1}" width="{WALL_X1 + 30}" height="70" fill="url(#s10shadow)" '
             f'opacity="0.5"/>')
    floor = (f'<path d="M-30,{DAIS_BACK} L{DAIS_X1 - 50},{DAIS_BACK} L{DAIS_X1},{DAIS_FRONT} L-30,{DAIS_FRONT} Z" '
             f'fill="url(#s10floor)" stroke="{ink}" stroke-width="4"/>')
    tiles = ""
    for i in range(1, 4):
        yy = DAIS_BACK + (DAIS_FRONT - DAIS_BACK) * i / 4
        tiles += f'<path d="M-30,{f1(yy)} L{f1(DAIS_X1 - 50 + 50 * i / 4)},{f1(yy)}"/>'
    for x in range(40, DAIS_X1 - 40, 120):
        tiles += f'<path d="M{x},{DAIS_BACK} L{x - 12},{DAIS_FRONT}"/>'
    floor += f'<g stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.5" fill="none">{tiles}</g>'
    floor += (f'<path d="M190,{DAIS_BACK + 30} L640,{DAIS_BACK + 30} L670,{DAIS_FRONT - 12} L160,{DAIS_FRONT - 12} Z" '
              f'fill="#a84a3c" stroke="{ink}" stroke-width="3.5"/>'
              f'<path d="M214,{DAIS_BACK + 44} L622,{DAIS_BACK + 44} L644,{DAIS_FRONT - 26} L188,{DAIS_FRONT - 26} Z" '
              f'fill="none" stroke="{P["crown"]}" stroke-width="5"/>')
    front = (f'<path d="M-30,{DAIS_FRONT} L{DAIS_X1},{DAIS_FRONT} L{DAIS_X1},{DAIS_BOTTOM} L-30,{DAIS_BOTTOM} Z" '
             f'fill="url(#s10front)" stroke="{ink}" stroke-width="4"/>'
             f'<rect x="-30" y="{DAIS_FRONT + 22}" width="{DAIS_X1 + 30}" height="40" fill="#3f79a8" '
             f'stroke="{ink}" stroke-width="3.5"/>' + V.rosettes(10, DAIS_X1 - 20, DAIS_FRONT + 42, 64, 14))
    side = (f'<path d="M{DAIS_X1 - 50},{DAIS_BACK} L{DAIS_X1},{DAIS_FRONT} L{DAIS_X1},{DAIS_BOTTOM} '
            f'L{DAIS_X1 - 50},{DAIS_BOTTOM - 110} Z" fill="#b18c58" stroke="{ink}" stroke-width="4"/>')
    steps = ""
    for i in range(3):
        x0, x1 = STEPS[0] - 26 * i, STEPS[1] + 26 * i
        y0 = DAIS_FRONT + 8 + 36 * i
        steps += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{DAIS_BOTTOM - y0 + 18 + 8 * i}" '
                  f'fill="{S.mix("#e3cba0", "#c49e6a", 0.25 + 0.2 * i)}" stroke="{ink}" stroke-width="4"/>'
                  f'<path d="M{x0 + 4},{y0 + 12} L{x1 - 4},{y0 + 12}" stroke="#f1e2c4" stroke-width="5" '
                  f'opacity="0.8"/>')
    pots = (PR.palm_tree(118, DAIS_BACK + 30 - 110, 0.42, lean=0.1, dates=False)
            + PR.jar(118, DAIS_BACK + 30 - 52, 1.05, color="#c46f48"))
    # a big glazed jar on the terrace by the far column
    pots += PR.jar(1580, DAIS_BACK + 2, 0.7, color="#3f79a8")
    body = (S.g(wall, filter="wobble") + S.g(cols + lintel + merlons, filter="wobble") + under
            + S.g(floor + front + side, filter="wobble") + S.g(steps, filter="wobble") + pots)
    return doc(body, defs)


def lamp_flame_svg(k):
    """The niche lamp's little flame + glow (3 flicker drawings)."""
    cx, cy = 788, DAIS_BACK - 318
    h = (30, 36, 33)[k]
    lean = (-3, 2, 4)[k]
    defs = S.rad_grad(f"s17lamp{k}", [(0, "#fff1c0", 0.85), (0.5, "#ffd98a", 0.35), (1, "#ffd27a", 0)])
    body = (f'<ellipse cx="{cx}" cy="{cy - 10}" rx="90" ry="80" fill="url(#s17lamp{k})"/>'
            f'<path d="M{cx - 10},{cy} Q{cx - 12},{cy - h * 0.5} {cx + lean},{cy - h} Q{cx + 12},{cy - h * 0.5} '
            f'{cx + 10},{cy} Q{cx},{cy + 6} {cx - 10},{cy} Z" fill="#f6b84a" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{cx - 4},{cy - 2} Q{cx - 5},{cy - h * 0.35} {cx + lean * 0.5},{cy - h * 0.6} '
            f'Q{cx + 5},{cy - h * 0.35} {cx + 4},{cy - 2} Z" fill="#fff0b8"/>')
    return doc(S.g(body, filter="wobble-fine"), defs)


def throne_svg():
    return doc(PR.throne(THRONE_X, THRONE_Y, KS, 1))


def bundle_markup():
    """The king's purple robe, folded, a sleeve over the seat edge, the crown on top (from v1 s10)."""
    ink, k = INK, KS * 0.92
    royal, light, dark, gold = P["royal"], P["royal_light"], S.shade(P["royal"], -0.25), P["crown"]
    low = (f'<path d="M-82,0 C-88,-14 -86,-26 -76,-30 L74,-32 C86,-28 90,-12 84,0 Z" fill="{dark}" '
           f'stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>')
    top = (f'<path d="M-74,-26 C-80,-40 -74,-54 -60,-56 L58,-58 C72,-56 78,-42 72,-28 C40,-22 -40,-22 -74,-26 Z" '
           f'fill="{royal}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
           f'<path d="M-60,-50 C-20,-54 30,-55 62,-52" stroke="{light}" stroke-width="6" fill="none" '
           f'stroke-linecap="round"/>'
           f'<path d="M-72,-30 C-40,-26 40,-26 72,-31" stroke="{gold}" stroke-width="7" fill="none" '
           f'stroke-linecap="round"/>')
    sleeve = (f'<path d="M58,-30 C80,-30 96,-14 98,10 C100,34 96,52 90,64 L64,62 C68,44 70,22 64,4 Z" '
              f'fill="{royal}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
              f'<path d="M64,58 L91,60" stroke="{gold}" stroke-width="9" stroke-linecap="round"/>'
              + "".join(f'<path d="M{66 + 6 * i},66 l0,12" stroke="{gold}" stroke-width="3.5" '
                        f'stroke-linecap="round"/>' for i in range(5)))
    crown = V.crown_svg_markup(-6, -52, 0.8, tilt=-7)
    body = f'<g transform="translate({f1(BUNDLE_X)},{f1(BUNDLE_Y)}) scale({k:.3f})">{low + sleeve + top + crown}</g>'
    return S.g(body, filter="wobble-fine")


# ============================================================================ little marks & props


def puff_markup(cx, cy, rx, ry, seed=0, k=1.0):
    """Cartoon 'quick change' poof (v1 s10): soft dust clouds hugging a figure + a few whoosh lines."""
    rng = random.Random(seed)
    dust = ""
    for i, deg in enumerate((-25, 8, 40, 72, 108, 140, 172, 205)):
        a = math.radians(deg + rng.uniform(-6, 6))
        px, py = cx + rx * 0.92 * math.cos(a), cy + ry * 0.95 * math.sin(a)
        w = k * rng.uniform(62, 84)
        dust += S.cloud(px, py, w, w * 0.62, "#f1e6cc", seed=seed * 17 + i, puffs=3, sw=2.4 * min(1, k + 0.2),
                        shade_fill="#dfcda8")
    lines = ""
    for a0, span, rr in ((-48, 40, 1.22), (-8, 34, 1.32), (188, -40, 1.22), (148, -34, 1.32)):
        pts = [(cx + rx * rr * math.cos(math.radians(a0 + span * j / 6)),
                cy + ry * rr * 0.92 * math.sin(math.radians(a0 + span * j / 6))) for j in range(7)]
        lines += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["ink_soft"]}" '
                  f'stroke-width="{4.5 * k:.1f}" stroke-linecap="round" opacity="0.75"/>')
    return S.g(lines, filter="wobble-fine") + S.g(dust, filter="wobble-fine", opacity=0.92)


def puff_motion(t0, pivot):
    return hop(t0, [(-0.06, {"alpha": 0, "s": 0.8, "dy": 0}), (0.02, {"alpha": 1, "s": 0.97, "dy": -4}),
                    (0.16, {"alpha": 0.85, "s": 1.06, "dy": -12}), (0.4, {"alpha": 0, "s": 1.14, "dy": -24})],
               pivot, ["out", "sine", "in"])


def ash_cloud_markup(cx, cy, w, seed=0):
    """A low grey puff of ash dust (when the heap appears / when he sits down)."""
    rng = random.Random(seed)
    out = ""
    for i in range(6):
        px = cx + (i - 2.5) / 2.5 * w * 0.5 + rng.uniform(-10, 10)
        py = cy - rng.uniform(0, 30)
        sz = rng.uniform(70, 100) * w / 300
        out += S.cloud(px, py, sz, sz * 0.6, "#d9d3cb", seed=seed * 13 + i, puffs=3, sw=2.2, shade_fill="#bdb5ab")
    return S.g(out, filter="wobble-fine", opacity=0.9)


def arcs_markup(x, y, facing, k, s=1.0):
    """'Speaking' sound arcs in front of a mouth (k = 1..3 for a flicker)."""
    out = ""
    for i in range(3):
        r = (13 + 13 * i + (k - 2) * 2) * s
        sx, sy = x + facing * r * 0.45, y - r * 0.85
        qx, qy = x + facing * r * 1.2, y
        ex, ey = x + facing * r * 0.45, y + r * 0.85
        out += (f'<path d="M{f1(sx)},{f1(sy)} Q{f1(qx)},{f1(qy)} {f1(ex)},{f1(ey)}" '
                f'fill="none" stroke="{INK}" stroke-width="{5 * s:.1f}" stroke-linecap="round" opacity="0.85"/>')
    return S.g(out, filter="wobble-fine")


def blast_markup(x, y, facing, k, s=1.0, ang=-42):
    """Horn blast: three wide arcs and a few short dashes from the bell, tilted up along the horn."""
    out = ""
    for i in range(3):
        r = (30 + 26 * i + (k - 2) * 4) * s
        a0, a1 = math.radians(ang - 32), math.radians(ang + 32)
        p0 = (x + facing * r * math.cos(a0), y + r * math.sin(a0))
        p1 = (x + facing * r * 1.12 * math.cos(math.radians(ang)), y + r * 1.12 * math.sin(math.radians(ang)))
        p2 = (x + facing * r * math.cos(a1), y + r * math.sin(a1))
        out += (f'<path d="M{f1(p0[0])},{f1(p0[1])} Q{f1(p1[0])},{f1(p1[1])} {f1(p2[0])},{f1(p2[1])}" fill="none" '
                f'stroke="{INK}" stroke-width="{5.5 * s:.1f}" stroke-linecap="round" opacity="0.85"/>')
    return S.g(out, filter="wobble-fine")


def exclaim_markup(x, y, s=1.0):
    body = (f'<path d="M{x - 9 * s},{y - 70 * s} L{x + 9 * s},{y - 70 * s} L{x + 5 * s},{y - 20 * s} '
            f'L{x - 5 * s},{y - 20 * s} Z" fill="#c9714a" stroke="{INK}" stroke-width="{4 * s}" '
            f'stroke-linejoin="round"/><circle cx="{x}" cy="{y - 4 * s}" r="{8 * s}" fill="#c9714a" '
            f'stroke="{INK}" stroke-width="{4 * s}"/>')
    for a in (-60, -30, 30, 60):
        r0, r1 = 52 * s, 72 * s
        aa = math.radians(a - 90)
        body += (f'<path d="M{f1(x + r0 * math.cos(aa))},{f1(y - 36 * s + r0 * math.sin(aa))} '
                 f'L{f1(x + r1 * math.cos(aa))},{f1(y - 36 * s + r1 * math.sin(aa))}" stroke="{INK}" '
                 f'stroke-width="{4 * s}" stroke-linecap="round"/>')
    return S.g(body, filter="wobble-fine")


def question_markup(x, y, s=1.0):
    """A hand-drawn '?' (puzzled animal)."""
    d = (f"M{f1(x - 16 * s)},{f1(y - 52 * s)} C{f1(x - 16 * s)},{f1(y - 78 * s)} {f1(x + 20 * s)},{f1(y - 80 * s)} "
         f"{f1(x + 20 * s)},{f1(y - 54 * s)} C{f1(x + 20 * s)},{f1(y - 36 * s)} {f1(x)},{f1(y - 36 * s)} "
         f"{f1(x)},{f1(y - 18 * s)}")
    return S.g(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{13 * s:.1f}" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="#e8b63c" stroke-width="{6.5 * s:.1f}" stroke-linecap="round"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y - 2 * s)}" r="{7 * s:.1f}" fill="#e8b63c" stroke="{INK}" '
               f'stroke-width="{3.5 * s:.1f}"/>', filter="wobble-fine")


def grumble_markup(x, y, s=1.0, seed=0):
    """An angry scribble cloud above a head."""
    rng = random.Random(seed)
    pts = []
    for i in range(26):
        a = i * 1.9
        r = (18 + 6 * math.sin(i * 1.3)) * s
        pts.append((x + r * 1.5 * math.cos(a) + rng.uniform(-3, 3), y + r * 0.8 * math.sin(a) + rng.uniform(-3, 3)))
    d = S.smooth_path(pts, closed=False)
    return S.g(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{4.5 * s:.1f}" stroke-linecap="round" '
               f'opacity="0.9"/>', filter="wobble-fine")


def tear_markup(x, y, s=1.0):
    return (f'<path d="M{f1(x)},{f1(y)} Q{f1(x - 6 * s)},{f1(y + 12 * s)} {f1(x)},{f1(y + 16 * s)} '
            f'Q{f1(x + 6 * s)},{f1(y + 12 * s)} {f1(x)},{f1(y)} Z" fill="#9fd0e0" stroke="{INK}" '
            f'stroke-width="{2.4 * s:.1f}"/>')


def horn_markup(hx, hy, s, facing=1):
    """The long bronze herald's horn (same design as s16) from the mouth (hx, hy) up and forward."""
    f = facing
    pts = [(hx, hy), (hx + f * 52 * s, hy - 14 * s), (hx + f * 104 * s, hy - 40 * s), (hx + f * 146 * s, hy - 78 * s)]
    d = S.smooth_path(pts, closed=False)
    bx, by = pts[-1]
    body = (f'<path d="{d}" stroke="{INK}" stroke-width="{17 * s:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#d9a441" stroke-width="{10 * s:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#f5d78a" stroke-width="{3 * s:.1f}" fill="none" stroke-linecap="round" '
            f'opacity="0.8" transform="translate(0,{-2 * s:.1f})"/>'
            f'<g transform="translate({f1(bx)},{f1(by)}) rotate({-42 * f})">'
            f'<path d="M{-8 * f * s},{-9 * s} L{f * 30 * s},{-26 * s} Q{f * 40 * s},0 {f * 30 * s},{26 * s} '
            f'L{-8 * f * s},{9 * s} Z" fill="#d9a441" stroke="{INK}" stroke-width="{4 * s:.1f}" '
            f'stroke-linejoin="round"/><ellipse cx="{f * 33 * s}" cy="0" rx="{8 * s}" ry="{25 * s}" fill="#8c5a24" '
            f'stroke="{INK}" stroke-width="{3.5 * s:.1f}"/></g>')
    return S.g(body, filter="wobble-fine"), (bx + f * 36 * s * math.cos(math.radians(42)),
                                               by - 36 * s * math.sin(math.radians(42)))


def hip_horn_markup(px, py, s, facing=1):
    """The horn hanging at the hip on a cord (before it is blown)."""
    f = facing
    pts = [(px - f * 34 * s, py - 6 * s), (px + f * 2 * s, py + 26 * s), (px + f * 40 * s, py + 30 * s)]
    d = S.smooth_path(pts, closed=False)
    return S.g(f'<path d="M{f1(px - f * 30 * s)},{f1(py - 62 * s)} L{f1(px - f * 30 * s)},{f1(py - 8 * s)}" '
               f'stroke="{P["wood_dark"]}" stroke-width="{3 * s:.1f}"/>'
               f'<path d="{d}" stroke="{INK}" stroke-width="{14 * s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<path d="{d}" stroke="#d9a441" stroke-width="{8 * s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<ellipse cx="{f1(px + f * 44 * s)}" cy="{f1(py + 29 * s)}" rx="{6 * s:.1f}" ry="{13 * s:.1f}" '
               f'fill="#8c5a24" stroke="{INK}" stroke-width="{3 * s:.1f}"/>', filter="wobble-fine")


def toy_markup(cx, by, s=1.0):
    """A little wooden toy lamb on wheels (bottom centre (cx, by))."""
    out = (f'<rect x="{f1(cx - 34 * s)}" y="{f1(by - 18 * s)}" width="{68 * s:.1f}" height="{9 * s:.1f}" '
           f'rx="{3 * s:.1f}" fill="{P["wood"]}" stroke="{INK}" stroke-width="{3 * s:.1f}"/>')
    for wx in (-22, 22):
        out += (f'<circle cx="{f1(cx + wx * s)}" cy="{f1(by - 8 * s)}" r="{8 * s:.1f}" fill="{P["wood_dark"]}" '
                f'stroke="{INK}" stroke-width="{3 * s:.1f}"/><circle cx="{f1(cx + wx * s)}" cy="{f1(by - 8 * s)}" '
                f'r="{2.4 * s:.1f}" fill="{P["wood_light"]}"/>')
    for lx in (-16, 14):
        out += (f'<path d="M{f1(cx + lx * s)},{f1(by - 18 * s)} l0,{-10 * s:.1f}" stroke="{INK}" '
                f'stroke-width="{7 * s:.1f}" stroke-linecap="round"/>')
    wool = ""
    for i, (dx, dy, r) in enumerate(((-18, -40, 14), (-4, -46, 15), (12, -42, 14), (-12, -30, 13), (8, -30, 13),
                                     (20, -34, 11))):
        wool += f'<circle cx="{f1(cx + dx * s)}" cy="{f1(by + dy * s)}" r="{r * s:.1f}" fill="#f6efe0"/>'
    out += (f'<g stroke="{INK}" stroke-width="{6 * s:.1f}">' + wool + '</g>' + wool)
    out += (f'<ellipse cx="{f1(cx + 32 * s)}" cy="{f1(by - 46 * s)}" rx="{11 * s:.1f}" ry="{13 * s:.1f}" '
            f'fill="#dcb89c" stroke="{INK}" stroke-width="{3 * s:.1f}"/>'
            f'<circle cx="{f1(cx + 35 * s)}" cy="{f1(by - 49 * s)}" r="{2.4 * s:.1f}" fill="{INK}"/>'
            f'<ellipse cx="{f1(cx + 22 * s)}" cy="{f1(by - 54 * s)}" rx="{8 * s:.1f}" ry="{4 * s:.1f}" '
            f'fill="#dcb89c" stroke="{INK}" stroke-width="{2.4 * s:.1f}"/>')
    out += (f'<path d="M{f1(cx - 34 * s)},{f1(by - 14 * s)} q{-20 * s:.1f},{8 * s:.1f} {-30 * s:.1f},{-6 * s:.1f}" '
            f'stroke="#c9714a" stroke-width="{3 * s:.1f}" fill="none" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


# ============================================================================ animals (body / head split)

# Markers of the first head shape in props._animal() output (the head is drawn last), and the neck pivots
# (local, scale 1, facing right).
HEAD_SPLIT = {"sheep": ("rotate(-24 54 -110)", "<ellipse", (50, -92)),
              "goat": ("M86,-194", "<path", (84, -160)),
              "cow": ("M118,-190", "<path", (112, -140))}


def animal_parts(x, y, s, facing, kind, sackcloth):
    """(body markup, head markup, neck pivot in stage px) of props.animal(): the head is split off so it can nod
    while the hooves stay planted (the v1 s02 sheep trick). Falls back to (whole animal, '', pivot)."""
    full = PR.animal(x, y, s, facing, kind=kind, sackcloth=sackcloth)
    if kind not in HEAD_SPLIT:
        return full, "", (x, y)
    marker, tag, (nx, ny) = HEAD_SPLIT[kind]
    pv = (x + facing * nx * s, y + ny * s)
    i = full.find(marker)
    j = full.rfind(tag, 0, i) if i >= 0 else -1
    k = full.find("<g transform=")
    k = full.find(">", k) + 1 if k >= 0 else 0
    if j <= k or not full.endswith("</g></g>"):
        return full, "", pv
    return full[:j] + "</g></g>", full[:k] + full[j:], pv


def head_motion(body_m, ha, F, N, f):
    """The body's motion (pivot F = hooves) re-expressed about the neck N, plus the head's own nod there, so the
    head stays on the neck through squashes and breathing."""
    def m(t):
        b = body_m(t)
        return Tf(dx=b.dx + (1 - b.sx) * (F[0] - N[0]), dy=b.dy + (1 - b.sy) * (F[1] - N[1]), rot=b.rot + f * ha(t),
                  sx=b.sx, sy=b.sy, alpha=b.alpha, px=N[0], py=N[1])
    return m


# ============================================================================ people


def person(kind, variant, x, y, s, facing, pose, expr=None, extra="", shadow=True, attire="sackcloth"):
    sw = {"kneel_pray": 170}.get(pose, 110)
    if kind == "child":
        sw = 120 if pose == "kneel_pray" else 86
    out = C.ground_shadow(x, y, s, sw, opacity=0.2) if shadow else ""
    return out + C.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, attire=attire, expr=expr) + extra


def bp(kind, variant, x, y, s, facing, pose):
    return C.body_points(C.citizen, x, y, s, facing, kind=kind, variant=variant, pose=pose, attire="sackcloth")


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]

    c0a, c0b, c0c = chunk(L0, "听说"), chunk(L0, "王袍"), chunk(L0, "灰堆")
    c1 = L1.chunks[0] if L1.chunks else L1
    c2a, c2b = chunk(L2, "不可以吃"), chunk(L2, "喝")
    c3a, c3b = chunk(L3, "麻布"), chunk(L3, "呼求")
    c4a, c4b, c4c = chunk(L4, "欺负"), chunk(L4, "可怜"), chunk(L4, "活下来")

    # ---- key times (all from the narration chunks; fractions mark the commas inside a chunk) ----
    t_tell = snap(c0a.start + 0.06)            # "国王听说了": the messenger speaks
    t_point = snap(within(c0a, 0.19))          # ...and points out to the city
    t_wow = within(c0a, 0.26)                  # the king is startled
    t_rise = snap(within(c0a, 0.52))           # "也从宝座上站起来": he rises
    t_msg_back = snap(t_rise - 0.25)
    t_w0 = t_rise + 0.18                       # steps forward to his spot
    t_crown = snap(c0b.start + 0.22)           # "脱下漂亮的王袍": crown off
    t_turn = snap(within(c0b, 0.3))            # turns to the throne
    t_sack = snap(within(c0b, 0.45))           # puff: robe off (flies to the throne), sackcloth on
    t_land = t_sack + 0.5
    t_front = snap(within(c0b, 0.6))           # "换上粗麻布衣服": turns back to us in sackcloth
    t_itch = within(c0b, 0.78)                 # a scratchy shiver
    t_ash = c0c.start + 0.08                   # "坐在灰堆里": the heap puffs up
    t_sit = snap(c0c.start + 0.5)              # and he sits down in it
    t_sorry = snap(within(c0c, 0.5))           # "表示真心认错": head bowed, sorry
    t_bow = snap(within(c0c, 0.56))            # messenger and scribe bow their heads
    t_speak = snap(c1.start + 0.1)             # "国王又派人…": the king speaks
    t_attn = snap(c1.start + 0.3)              # the two straighten up
    t_go = snap(c1.start + 0.85)               # ...and walk out to the terrace
    t_arrive = t_go + 1.35
    t_horn = snap(t_arrive + 0.12)             # the messenger lifts the horn
    t_blow = t_horn + 0.18
    t_scroll = snap(t_go + 1.65)               # the scribe (who followed) unrolls the decree
    t_read = L2.start + 0.05                   # the king's words are read out
    t_horn_down = snap(L2.start + 0.35)
    t_lid = snap(within(c2a, 0.68))            # "都不可以吃": the farmer lifts the plank...
    t_lid_on = t_lid + 0.42                    # ...and lays it over the manger
    t_mat = snap(c2b.start + 0.12)             # "也不可以喝": the girl pulls the mat
    t_mat_on = t_mat + 0.38
    t_cloth = within(c3a, 0.4)                 # "都要穿上麻布衣服": blankets, pop pop pop
    t_pray = snap(c3b.start + 0.2)             # "诚心向上帝呼求": kneel and pray
    t_stop = snap(c4a.start + 0.5)             # "每个人都要改掉坏行为": the two men stop
    t_hang = snap(within(c4a, 0.3))            # ...hang their heads
    t_turnb = snap(within(c4a, 0.47))          # "不再欺负别人": the boy turns back
    t_give = snap(within(c4a, 0.6))            # holds out the toy
    t_take = snap(within(c4a, 0.72))           # she takes it, both smile
    t_step = within(c4a, 0.7)                  # the men step together...
    t_shake = snap(within(c4a, 0.8))           # ...and shake hands
    t_kneel = snap(c4b.start + 0.25)           # "说不定上帝会可怜我们": kneel, look up hopefully
    t_hope = snap(c4c.start + 0.2)             # "我们就能活下来": hopeful smiles, warm light

    # ---- sky ----
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds_back", clouds_svg(CLOUDS_BACK, "#d7cfd6", "#bab0c0"), z=1, wc=0.7, motion=M.drift(vx=5))
    sc.add("hope", hope_svg(), z=1.5, wc=0,
           motion=M.combine(M.keys([(t_hope - 0.3, {"alpha": 0}), (t_hope + 1.6, {"alpha": 1})], "sine"),
                            M.pulse(0.85, 1.0, 3.0)))
    sc.add("clouds_front", clouds_svg(CLOUDS_FRONT, "#e2d9da", "#c6bcc4"), z=1.6, wc=0.7, motion=M.drift(vx=9))

    # a few far doves drift across the sky over the street (life in the quiet, fasting city)
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = (0, 1, 2, 3, 4, 3, 2, 1)
    for i, (fc, x0, y0, x1, y1, ta, tb, s, rate) in enumerate((
            (1, 1700, 560, 3500, 470, L1.end - 1.0, c3b.end, 0.5, 10.0),
            (1, 1900, 470, 3400, 420, L2.start + 0.5, c3b.end + 1.0, 0.4, 11.0),
            (-1, 5400, 520, 3500, 430, c3b.start, T + 0.5, 0.48, 9.5))):
        ref = (x0, y0)
        fr = [doc(PR.dove(x0, y0, s, fc, wing=w)) for w in wings]

        def fa(t, rate=rate, i=i):
            if int(t * 0.8 + i) % 3 == 2:          # glide now and then
                return 2.0
            return float(cyc[int(t * rate + i * 3) % 8])

        def mv(t, x0=x0, y0=y0, x1=x1, y1=y1, ta=ta, tb=tb, i=i):
            u = min(1.0, max(0.0, (t - ta) / (tb - ta)))
            return Tf(dx=(x1 - x0) * u, dy=(y1 - y0) * u + 10 * math.sin(2 * math.pi * t / 1.7 + i),
                      alpha=1.0 if ta <= t <= tb else 0.0)
        sc.add(f"dove{i}", fr, z=1.8, frame_at=fa, motion=mv, seed=950 + i)

    # ---- city, street, yard backdrop (static) ----
    sc.add("far", far_svg(), z=2)
    sc.add("yard_back", yard_back_svg(), z=2.1)

    sc.add("far_people", far_people_svg(), z=2.05)

    # far heralds on the roofs answer the horn ("全城"); one of them reads the decree out over the families
    hx_ = {x: (v, f) for x, v, f in HOUSES}
    for i, (x, dt, f) in enumerate(((2600, 0.9, -1), (3880, 1.3, 1), (5150, 1.7, -1))):
        v, _f = hx_[x]
        y, s = ROOF_Y[v], 0.42
        hd = bp("man", i, x, y, s, f, "listen")["head"]
        hm, bell = horn_markup(hd[0] + f * 15 * s, hd[1] + 20 * s, s, f)
        fr = [doc(C.citizen(x, y, s, f, kind="man", variant=i, pose="stand", attire="sackcloth")),
              doc(C.citizen(x, y, s, f, kind="man", variant=i, pose="listen", attire="sackcloth") + hm),
              doc(C.citizen(x, y, s, f, kind="man", variant=i, pose="kneel_pray", attire="sackcloth"))]
        tb = snap(t_blow + dt)
        tk = snap(t_pray + 0.6 + 0.3 * i)
        sc.add(f"roof_herald{i}", fr, z=2.2, frame_at=cuts([(0, 0), (tb, 1), (tb + 2.2, 0), (tk, 2)]),
               motion=M.combine(dip(tb, s, (x, y), 6), dip(tb + 2.2, s, (x, y), 6), dip(tk, s, (x, y), 6),
                                M.breathe(0.01, 2.8, pivot=(x, y), phase=0.3 * i)))
        sc.add(f"roof_blast{i}", [doc(blast_markup(bell[0], bell[1], f, k, s * 1.4)) for k in (1, 2, 3)], z=2.25,
               wc=0, frame_at=lambda t: float(int(t * 8) % 3),
               motion=M.keys([(tb + 0.1, {"alpha": 0}), (tb + 0.25, {"alpha": 1}), (tb + 1.9, {"alpha": 1}),
                              (tb + 2.15, {"alpha": 0})], "sine"))
    # a crier on the roof above the families reads the decree from a scroll
    v, f = hx_[4720]
    cx_, cy_, cs = 4720, ROOF_Y[v], 0.42
    ch = bp("man", 2, cx_, cy_, cs, -1, "point")
    cscroll = PR.scroll(ch["hands"][0][0] - 18 * cs, ch["hands"][0][1] - 30 * cs, 0.62 * cs, opened=True)
    sc.add("roof_crier", doc(C.citizen(cx_, cy_, cs, -1, kind="man", variant=2, pose="point", attire="sackcloth",
                                       expr="call") + cscroll), z=2.2,
           motion=M.combine(M.breathe(0.012, 2.6, pivot=(cx_, cy_)),
                            lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * t / 2.3), px=cx_, py=cy_)))
    sc.add("roof_crier_arcs", [doc(arcs_markup(ch["head"][0] - 40 * cs, ch["head"][1] + 22 * cs, -1, k, cs * 1.3))
                               for k in (1, 2, 3)], z=2.25, wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(L2.start, {"alpha": 0}), (L2.start + 0.2, {"alpha": 1}), (L4.end - 0.2, {"alpha": 1}),
                          (L4.end, {"alpha": 0})], "sine"))

    # ---- the palace ----
    sc.add("palace", palace_svg(), z=5)
    sc.add("throne", throne_svg(), z=5.1)
    sc.add("lamp", [lamp_flame_svg(k) for k in range(3)], z=5.05, wc=0.3,
           frame_at=lambda t: float(int(t * 7) % 3))

    # robe bundle (folded robe + crown) arcs from the king's hands onto the throne seat
    hands = C.body_points(C.king, SPOT_X, SPOT_Y, KS, -1, pose="remove_crown")["hands"]
    hx, hy = (hands[0][0] + hands[1][0]) / 2, (hands[0][1] + hands[1][1]) / 2
    dx0, dy0 = hx + 6 - BUNDLE_X, hy + 62 - BUNDLE_Y
    bpv = (BUNDLE_X, BUNDLE_Y)
    sc.add("bundle", doc(bundle_markup()), z=7.2, motion=M.combine(
        M.keys([(t_sack - 0.01, {"alpha": 0, "dx": dx0, "s": 0.9}), (t_sack + 0.02, {"alpha": 1}),
                (t_land, {"dx": 0, "s": 1.0})], ["linear", "sine"], pivot=bpv),
        M.keys([(t_sack, {"dy": dy0}), (t_sack + 0.22, {"dy": min(dy0, 0) - 75}), (t_land, {"dy": 0})], ["out", "in"],
               pivot=bpv),
        M.keys([(t_sack, {"rot": 12}), (t_sack + 0.26, {"rot": -8}), (t_land, {"rot": 0}), (t_land + 0.1, {"rot": 3}),
                (t_land + 0.22, {"rot": 0})], "sine", pivot=bpv),
        hop(t_land, [(0, {"sx": 1, "sy": 1}), (0.07, {"sx": 1.06, "sy": 0.88}), (0.2, {"sx": 1, "sy": 1})], bpv)))

    # the king on the throne: listens, is startled, leans forward and squashes, then hard-cuts to the standing
    # king right in front of the seat (who springs up)
    pv_seat = (THRONE_X, THRONE_Y)
    seat = [doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False)),
            doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False, expr="worried")),
            doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False, expr="surprised"))]
    sc.add("king_seat", seat, z=6, frame_at=cuts([(0, 0), (snap(t_tell + 0.3), 1), (snap(t_wow), 2)]),
           motion=M.combine(
               dip(snap(t_tell + 0.3), KS, pv_seat, 4), dip(snap(t_wow), KS, pv_seat, 6),
               hop(t_rise, [(-0.26, {"sy": 1, "rot": 0, "alpha": 1}), (0, {"sy": 0.94, "rot": 6, "alpha": 1}),
                            (0.01, {"sy": 0.94, "rot": 6, "alpha": 0})], pv_seat, ["inout", "linear"]),
               M.breathe(0.008, 3.2, pivot=pv_seat)))
    kh = C.body_points(C.king, THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False)["head_top"]
    ex, ey = kh[0] + 128, kh[1] + 44
    sc.add("wow", doc(exclaim_markup(ex, ey, 1.2)), z=9, wc=0,
           motion=M.keys([(t_wow - 0.05, {"alpha": 0, "s": 0.4}), (t_wow + 0.25, {"alpha": 1, "s": 1}),
                          (t_rise - 0.15, {"alpha": 1}), (t_rise, {"alpha": 0})],
                         ["back", "linear", "sine"], pivot=(ex, ey)))

    # ashes: the heap puffs up just before he sits in it
    ax = SPOT_X + PR.KING_ASH_DX * KS
    ash_in = M.keys([(t_ash, {"alpha": 0, "sx": 0.7, "sy": 0.4}), (t_ash + 0.35, {"alpha": 1, "sx": 1, "sy": 1})],
                    "out", pivot=(ax, SPOT_Y))
    sc.add("ash_back", doc(V.ash_heap(ax, SPOT_Y, KS, "back")), z=6.5, motion=ash_in)
    sc.add("ash_front", doc(V.ash_heap(ax, SPOT_Y, KS, "front")), z=7.5, motion=ash_in)
    for nm, tt, w, sd, a in (("ash_puff1", t_ash, 300, 3, 0.6), ("ash_puff2", t_sit, 240, 5, 0.5)):
        pv = (ax, SPOT_Y - 20)
        sc.add(nm, doc(ash_cloud_markup(ax, SPOT_Y - 20, w, sd)), z=7.6, wc=0.5,
               motion=hop(tt, [(-0.02, {"alpha": 0, "s": 0.6, "dy": 0}), (0.08, {"alpha": a, "s": 0.95}),
                               (0.6, {"alpha": 0, "s": 1.3, "dy": -60})], pv, ["out", "sine"]))

    # the king: stands in front of the throne, steps forward, takes off his crown, turns to the throne, changes
    # into sackcloth (puff), turns back, sits in the ashes, bows (sorry), speaks the decree, bows again
    kp = (SPOT_X, SPOT_Y)
    ksh = C.ground_shadow(SPOT_X, SPOT_Y, KS, 130)
    kfr = [doc(ksh + C.king(SPOT_X, SPOT_Y, KS, 1, pose="stand", expr="worried")),                       # 0
           doc(ksh + C.king(SPOT_X, SPOT_Y, KS, 1, pose="remove_crown")),                                 # 1
           doc(ksh + C.king(SPOT_X, SPOT_Y, KS, -1, pose="remove_crown")),                                # 2
           doc(ksh + C.king(SPOT_X, SPOT_Y, KS, -1, pose="stand", attire="sackcloth")),                   # 3
           doc(ksh + C.king(SPOT_X, SPOT_Y, KS, 1, pose="stand", attire="sackcloth")),                    # 4
           doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False)),                             # 5
           doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False, expr="sorry")),               # 6
           doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False, expr="call"))]                # 7
    t_unspeak = snap(c1.end - 0.3)
    step = 0.17
    bob_keys = [(0, {"dy": 0, "rot": 0})]
    for i in range(4):
        bob_keys += [(i * step + step / 2, {"dy": -7, "rot": 1.6 * (1 if i % 2 else -1)}),
                     ((i + 1) * step, {"dy": 0, "rot": 0})]
    sc.add("king", kfr, z=7,
           frame_at=cuts([(0, 0), (t_crown, 1), (t_turn, 2), (t_sack, 3), (t_front, 4), (t_sit, 5), (t_sorry, 6),
                          (t_speak, 7), (t_unspeak, 6)]),
           motion=M.combine(
               M.keys([(t_rise, {"alpha": 0}), (t_rise + 0.01, {"alpha": 1})], "linear", pivot=kp),
               M.keys([(t_w0, {"dx": RISE_X - SPOT_X}), (t_w0 + 4 * step, {"dx": 0})], "inout", pivot=kp),
               hop(t_w0, bob_keys, kp),
               hop(t_rise, [(0, {"sy": 0.9, "rot": 5}), (0.08, {"sy": 1.04, "rot": 0}), (0.18, {"sy": 0.99}),
                            (0.28, {"sy": 1.0})], kp),
               dip(t_crown, KS, kp, 10), dip(t_turn, KS, kp, 6),
               hop(t_sack, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5, "sy": 0.96}), (0.12, {"dy": -3, "sy": 1.02}),
                            (0.26, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               dip(t_front, KS, kp, 6),
               hop(t_itch, [(0, {"rot": 0}), (0.08, {"rot": -1.6}), (0.16, {"rot": 1.6}), (0.24, {"rot": -1.3}),
                            (0.32, {"rot": 1.1}), (0.42, {"rot": 0})], (SPOT_X, SPOT_Y)),
               hop(t_sit, [(-0.2, {"dy": 0, "sy": 1}), (0, {"dy": 14, "sy": 0.93}), (0.1, {"dy": -3, "sy": 1.03}),
                           (0.25, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               dip(t_sorry, KS, kp, 5), dip(t_speak, KS, kp, 4), dip(t_unspeak, KS, kp, 4),
               M.breathe(0.009, 3.0, pivot=kp, phase=0.3)))
    pk = (SPOT_X - 6, SPOT_Y - 190)
    sc.add("puff_king", doc(puff_markup(pk[0], pk[1], 118, 178, seed=3, k=1.1)), z=8, wc=0.5,
           motion=puff_motion(t_sack, pk))
    # the king's words: sound arcs (he speaks with his head still low)
    khd = C.body_points(C.king, SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False)["head"]
    sc.add("king_arcs", [doc(arcs_markup(khd[0] + 60, khd[1] + 30, 1, k, 1.1)) for k in (1, 2, 3)], z=9, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_speak, {"alpha": 0}), (t_speak + 0.15, {"alpha": 1}), (t_unspeak - 0.15, {"alpha": 1}),
                          (t_unspeak, {"alpha": 0})], "sine"))

    # ---- the messenger: tells the king, points out, bows; then walks out and blows the horn ----
    mx, my, ms, mv = MSG["x"], MSG["y"], MSG["s"], MSG["v"]
    mpel = bp("man", mv, mx, my, ms, -1, "stand")["pelvis"]
    mpel1 = bp("man", mv, mx, my, ms, 1, "stand")["pelvis"]

    def mfr(facing, pose, expr=None, horn=True):
        extra = ""
        if horn and pose not in ("listen",):
            pel = mpel if facing < 0 else mpel1
            extra = hip_horn_markup(pel[0] - facing * 6 * ms, pel[1] + 4 * ms, ms * 0.8, -facing)
        return doc(person("man", mv, mx, my, ms, facing, pose, expr, extra=extra))
    mhead = bp("man", mv, mx, my, ms, 1, "listen")["head"]
    horn_m, bell_m = horn_markup(mhead[0] + 15 * ms, mhead[1] + 20 * ms, ms, 1)
    mframes = [mfr(-1, "stand", "worried"),                                              # 0
               mfr(-1, "stand", "call"),                                                 # 1
               mfr(1, "point", "worried"),                                               # 2
               mfr(-1, "stand", "worried"),                                              # 3
               mfr(-1, "sad", "sorry"),                                                  # 4
               mfr(-1, "stand", "neutral"),                                              # 5
               mfr(1, "walk_a", "neutral"),                                              # 6
               mfr(1, "walk_b", "neutral"),                                              # 7
               mfr(1, "stand", "neutral"),                                               # 8
               doc(person("man", mv, mx, my, ms, 1, "listen", "neutral", extra=horn_m)),  # 9 blowing the horn
               mfr(1, "stand", "sad")]                                                   # 10
    WALK_P = 0.34
    m_dist = HORN_X - mx

    def walk_sched(t_go_, t_arr, first):
        def fa(t):
            if t < t_go_ or t >= t_arr:
                return None
            return float(first + int((t - t_go_) / WALK_P) % 2)
        return fa

    m_walk = walk_sched(t_go, t_arrive, 6)
    m_base = cuts([(0, 0), (t_tell, 1), (t_point, 2), (t_msg_back, 3), (t_bow, 4), (t_attn, 5), (t_arrive, 8),
                   (t_horn, 9), (t_horn_down, 10)])
    mp = (mx, my)
    walk_x = lambda d: M.keys([(t_go, {"dx": 0}), (t_go + 0.2, {"dx": d * 0.12}), (t_arrive - 0.2, {"dx": d * 0.88}),
                               (t_arrive, {"dx": d})], ["in", "linear", "out"], pivot=None)
    walk_bob = lambda t0, t1, s: (lambda t: Tf(dy=-5 * s * abs(math.sin(math.pi * (t - t0) / WALK_P)))
                                  if t0 <= t < t1 else Tf())
    sc.add("messenger", mframes, z=8.5,
           frame_at=lambda t: m_walk(t) if m_walk(t) is not None else m_base(t),
           motion=M.combine(
               M.with_pivot(walk_x(m_dist), mp), walk_bob(t_go, t_arrive, ms),
               dip(t_tell, ms, mp, 4), dip(t_point, ms, mp), dip(t_msg_back, ms, mp), dip(t_bow, ms, mp, 6),
               dip(t_attn, ms, mp, 5), nod(t_attn + 0.3, mp, -3), dip(t_go, ms, mp, 5), dip(t_arrive, ms, mp, 5),
               dip(t_horn, ms, mp), hop(t_blow, [(0, {"rot": 0}), (0.35, {"rot": -2.5}), (1.2, {"rot": -2.5}),
                                                 (1.45, {"rot": 0})], mp),
               dip(t_horn_down, ms, mp, 5),
               M.breathe(0.01, 2.8, pivot=mp, phase=0.6)))
    mh0 = bp("man", mv, mx, my, ms, -1, "stand")["head"]
    sc.add("msg_arcs", [doc(arcs_markup(mh0[0] - 58 * ms, mh0[1] + 28 * ms, -1, k, ms)) for k in (1, 2, 3)], z=9,
           wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_tell, {"alpha": 0}), (t_tell + 0.12, {"alpha": 1}), (t_point - 0.12, {"alpha": 1}),
                          (t_point, {"alpha": 0})], "sine"))
    sc.add("horn_blast", [doc(blast_markup(bell_m[0] + m_dist, bell_m[1], 1, k, ms)) for k in (1, 2, 3)], z=9,
           wc=0, frame_at=lambda t: float(int(t * 8) % 3),
           motion=M.keys([(t_blow, {"alpha": 0}), (t_blow + 0.12, {"alpha": 1}), (t_horn_down - 0.25, {"alpha": 1}),
                          (t_horn_down - 0.05, {"alpha": 0})], "sine"))

    # ---- the scribe: holds the decree scroll, bows, walks out, unrolls and reads it ----
    rx_, ry_, rs, rv = SCR["x"], SCR["y"], SCR["s"], SCR["v"]

    def scroll_closed(facing, pose):
        h = bp("man", rv, rx_, ry_, rs, facing, pose)["hands"][1]
        return PR.scroll(h[0], h[1] + 4 * rs, 0.42 * rs, rot=-70 * facing)

    rhand = bp("man", rv, rx_, ry_, rs, 1, "point")["hands"][0]
    open_scroll = PR.scroll(rhand[0] + 18 * rs, rhand[1] - 30 * rs, 0.62 * rs, opened=True)

    def rfr(facing, pose, expr=None, extra=None):
        ex_ = scroll_closed(facing, pose) if extra is None else extra
        return doc(person("man", rv, rx_, ry_, rs, facing, pose, expr, extra=ex_))
    rframes = [rfr(-1, "stand", "worried"),          # 0
               rfr(-1, "sad", "sorry"),              # 1
               rfr(-1, "stand", "neutral"),          # 2
               rfr(1, "walk_a", "neutral"),          # 3
               rfr(1, "walk_b", "neutral"),          # 4
               rfr(1, "stand", "neutral"),           # 5
               rfr(1, "point", "call", open_scroll)]  # 6 reading the decree
    r_dist = READ_X - rx_
    r_go = t_go + 0.3
    r_arr = r_go + 1.0
    r_walk = walk_sched(r_go, r_arr, 3)
    r_base = cuts([(0, 0), (t_bow + 0.1, 1), (t_attn, 2), (r_arr, 5), (t_scroll, 6)])
    rp = (rx_, ry_)
    sc.add("scribe", rframes, z=8.2,
           frame_at=lambda t: r_walk(t) if r_walk(t) is not None else r_base(t),
           motion=M.combine(
               M.with_pivot(M.keys([(r_go, {"dx": 0}), (r_go + 0.2, {"dx": r_dist * 0.08}),
                                    (r_arr - 0.2, {"dx": r_dist * 0.92}), (r_arr, {"dx": r_dist})],
                                   ["in", "linear", "out"]), rp),
               walk_bob(r_go, r_arr, rs),
               dip(t_bow + 0.1, rs, rp, 6), dip(t_attn, rs, rp, 5), nod(t_attn + 0.2, rp, -3), dip(r_arr, rs, rp, 5),
               dip(t_scroll, rs, rp),
               lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * (t - t_read) / 2.2)) if t > t_read else Tf(),
               M.breathe(0.01, 3.1, pivot=rp, phase=0.1)))
    rhd = bp("man", rv, READ_X, ry_, rs, 1, "point")["head"]
    t_read_end = c3b.end
    sc.add("read_arcs", [doc(arcs_markup(rhd[0] + 44 * rs, rhd[1] + 22 * rs, 1, k, rs)) for k in (1, 2, 3)], z=9,
           wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_read, {"alpha": 0}), (t_read + 0.15, {"alpha": 1}), (t_read_end - 0.2, {"alpha": 1}),
                          (t_read_end, {"alpha": 0})], "sine"))

    # ---- the yard: animals (heads nod on their own layers), manger, trough, farmer and his daughter ----
    puffs = []

    def beast(name, a, kind, z, head_angle, hops=(), t_sack_=None):
        x, y, s, f = a["x"], a["y"], a["s"], a["f"]
        b0, h0, pv = animal_parts(x, y, s, f, kind, False)
        b1, _, _ = animal_parts(x, y, s, f, kind, True)
        w = {"cow": 250, "goat": 190, "sheep": 190, "donkey": 230}.get(kind, 200)
        shadow = C.ground_shadow(x, y, s, w, opacity=0.2)
        base = [M.breathe(0.012, 2.6 + 0.2 * len(name), pivot=(x, y), phase=0.1 * len(name))]
        for th in hops:
            base.append(happy_hop(th, s, (x, y), 22))
        frames = [doc(shadow + b0), doc(shadow + b1)]
        fa = cuts([(0, 0), (t_sack_, 1)]) if t_sack_ is not None else (lambda t: 0.0)
        body_m = M.combine(*base)
        sc.add(name, frames, z=z, frame_at=fa, motion=body_m)
        if h0:
            sc.add(name + "_head", doc(h0), z=z + 0.01, motion=head_motion(body_m, head_angle, (x, y), pv, f))
        if t_sack_ is not None:
            puffs.append((t_sack_, x, y, s, kind))

    # head angle (deg, + = nose down): munching nods, lift at the lid, sad droop, bow at the prayer
    def munch(t_stop_, amp=7.0, per=1.1, ph=0.0, lift=-6.0, droop=4.0, t_bow_=None):
        def ha(t):
            m = amp * (0.5 + 0.5 * math.sin(2 * math.pi * (t / per + ph))) if t < t_stop_ else 0.0
            m *= 1 - M.progress(t, t_stop_ - 0.25, t_stop_, "sine")
            up = lift * M.progress(t, t_stop_ - 0.05, t_stop_ + 0.2, "out") * (1 - M.progress(t, t_stop_ + 1.1,
                                                                                               t_stop_ + 1.6, "sine"))
            dr = droop * M.progress(t, t_stop_ + 1.1, t_stop_ + 1.6, "sine")
            bw = 8.0 * M.progress(t, t_bow_, t_bow_ + 0.5, "sine") if t_bow_ else 0.0
            if t_bow_:
                bw *= 1 - 0.7 * M.progress(t, t_hope, t_hope + 0.6, "sine")
            return m + up + dr + bw
        return ha

    t_cow_up = t_lid_on + 0.08
    t_lamb_up = t_mat_on + 0.08
    beast("donkey", DONKEY, "donkey", 10.0, None, t_sack_=snap(t_cloth + 1.2))
    beast("cow", COW, "cow", 10.6, munch(t_cow_up, 6, 1.3, 0.2, -7, 4, t_pray + 0.3), hops=(snap(t_cloth),),
          t_sack_=snap(t_cloth))
    beast("goat", GOAT, "goat", 11.2, munch(t_cow_up + 0.15, 7, 1.05, 0.6, -8, 4, t_pray + 0.45),
          hops=(snap(t_cloth + 0.3),), t_sack_=snap(t_cloth + 0.3))
    beast("sheep", SHEEP, "sheep", 12.2, munch(t_lamb_up + 0.1, 5, 1.6, 0.3, -6, 4, t_pray + 0.4),
          hops=(snap(t_cloth + 0.6),), t_sack_=snap(t_cloth + 0.6))
    beast("lamb", LAMB, "sheep", 11.4, munch(t_lamb_up, 6, 1.2, 0.8, -9, 5, t_pray + 0.55),
          hops=(snap(t_cloth + 0.9),), t_sack_=snap(t_cloth + 0.9))

    # farmer behind the manger
    fx_, fy_, fs, fv = FARMER["x"], FARMER["y"], FARMER["s"], FARMER["v"]
    fhand = bp("man", fv, fx_, fy_, fs, 1, "point")["hands"][0]
    ffr = [doc(person("man", fv, fx_, fy_, fs, 1, "stand", "neutral")),
           doc(person("man", fv, fx_, fy_, fs, 1, "point", "sorry")),
           doc(person("man", fv, fx_, fy_, fs, 1, "stand", "sad")),
           doc(person("man", fv, fx_, fy_, fs, 1, "kneel_pray", "peaceful")),
           doc(person("man", fv, fx_, fy_, fs, 1, "kneel_pray", "worried")),
           doc(person("man", fv, fx_, fy_, fs, 1, "kneel_pray", "peaceful"))]
    fp = (fx_, fy_)
    t_f_after = snap(t_lid_on + 0.5)
    sc.add("farmer", ffr, z=10.1,
           frame_at=cuts([(0, 0), (t_lid, 1), (t_f_after, 2), (t_pray, 3), (t_kneel, 4), (t_hope, 5)]),
           motion=M.combine(dip(t_lid, fs, fp), dip(t_f_after, fs, fp, 5), dip(t_pray, fs, fp),
                            dip(t_kneel, fs, fp, 4), dip(t_hope, fs, fp, 4), M.breathe(0.01, 3.0, pivot=fp, phase=0.2)))
    # the manger (in front of the farmer and the animals' muzzles), its hay and the plank lid
    sc.add("hay", doc(hay_markup()), z=10.2)
    sc.add("manger", doc(manger_markup()), z=11.6)
    lid_cx = (MANGER[0] + MANGER[1]) / 2
    lid_cy = MANGER[2] - 6
    lp = (lid_cx, lid_cy)
    ldx, ldy = fhand[0] - lid_cx + 40, fhand[1] - lid_cy + 6
    sc.add("lid", doc(plank_markup(lid_cx, lid_cy)), z=11.7, motion=M.combine(
        M.keys([(t_lid - 0.01, {"alpha": 0}), (t_lid + 0.01, {"alpha": 1})], "linear", pivot=lp),
        M.keys([(t_lid, {"dx": ldx, "dy": ldy, "rot": -14}), (t_lid + 0.12, {"dx": ldx, "dy": ldy - 6, "rot": -12}),
                (t_lid_on, {"dx": 0, "dy": 0, "rot": 0})], ["sine", "in"], pivot=lp),
        hop(t_lid_on, [(0, {"sy": 1}), (0.06, {"sy": 0.86, "dy": 2}), (0.18, {"sy": 1, "dy": 0})], lp)))

    # the water trough (in front of the lamb), the girl behind it and the reed mat
    gx, gy, gs, gv = GIRL_Y["x"], GIRL_Y["y"], GIRL_Y["s"], GIRL_Y["v"]
    ghand = bp("child", gv, gx, gy, gs, 1, "point")["hands"][0]
    gfr = [doc(person("child", gv, gx, gy, gs, 1, "stand", "neutral")),
           doc(person("child", gv, gx, gy, gs, 1, "point", "sorry")),
           doc(person("child", gv, gx, gy, gs, 1, "stand", "sad")),
           doc(person("child", gv, gx, gy, gs, 1, "kneel_pray", "peaceful")),
           doc(person("child", gv, gx, gy, gs, 1, "kneel_pray", "worried")),
           doc(person("child", gv, gx, gy, gs, 1, "kneel_pray", "happy"))]
    gp = (gx, gy)
    t_g_after = snap(t_mat_on + 0.45)
    sc.add("yard_girl", gfr, z=11.3,
           frame_at=cuts([(0, 0), (t_mat, 1), (t_g_after, 2), (t_pray + 0.12, 3), (t_kneel + 0.1, 4),
                          (t_hope + 0.1, 5)]),
           motion=M.combine(dip(t_mat, gs, gp), dip(t_g_after, gs, gp, 5), dip(t_pray + 0.12, gs, gp),
                            dip(t_kneel + 0.1, gs, gp, 4), dip(t_hope + 0.1, gs, gp, 4),
                            M.breathe(0.012, 2.6, pivot=gp, phase=0.5)))
    sc.add("trough", doc(trough_markup()), z=12.0)
    mat_cx, mat_cy = (TROUGH[0] + TROUGH[1]) / 2, TROUGH[2] - 10
    mtp = (mat_cx, mat_cy)
    mdx, mdy = ghand[0] - mat_cx + 30, ghand[1] - mat_cy + 4
    sc.add("mat", doc(mat_markup(mat_cx, mat_cy)), z=12.1, motion=M.combine(
        M.keys([(t_mat - 0.01, {"alpha": 0}), (t_mat + 0.01, {"alpha": 1})], "linear", pivot=mtp),
        M.keys([(t_mat, {"dx": mdx, "dy": mdy, "rot": -10}), (t_mat + 0.1, {"dx": mdx, "dy": mdy - 5, "rot": -9}),
                (t_mat_on, {"dx": 0, "dy": 0, "rot": 0})], ["sine", "in"], pivot=mtp),
        hop(t_mat_on, [(0, {"sy": 1}), (0.06, {"sy": 0.88, "dy": 2}), (0.18, {"sy": 1, "dy": 0})], mtp)))

    # "?" over the cow and the lamb
    cow_head = (COW["x"] - 150 * COW["s"], COW["y"] - 215 * COW["s"])
    lamb_head = (LAMB["x"] - 70 * LAMB["s"], LAMB["y"] - 150 * LAMB["s"])
    for nm, (qx, qy), t0 in (("q_cow", cow_head, t_cow_up + 0.1), ("q_lamb", lamb_head, t_lamb_up + 0.1)):
        sc.add(nm, doc(question_markup(qx, qy, 1.0)), z=14, wc=0,
               motion=M.combine(M.keys([(t0, {"alpha": 0, "s": 0.4}), (t0 + 0.25, {"alpha": 1, "s": 1}),
                                        (t0 + 1.25, {"alpha": 1}), (t0 + 1.55, {"alpha": 0})],
                                       ["back", "linear", "sine"], pivot=(qx, qy)),
                                lambda t, t0=t0: Tf(rot=6 * math.sin(2 * math.pi * (t - t0) / 0.9), px=qx, py=qy)))

    # sackcloth puffs on the animals
    for i, (tp, x, y, s, kind) in enumerate(puffs):
        rx0 = {"cow": 150, "goat": 110, "sheep": 100, "donkey": 130}[kind] * s
        ry0 = {"cow": 90, "goat": 80, "sheep": 62, "donkey": 80}[kind] * s
        cy0 = y - {"cow": 140, "goat": 115, "sheep": 85, "donkey": 150}[kind] * s
        sc.add(f"puff_a{i}", doc(puff_markup(x, cy0, rx0, ry0, seed=20 + i, k=0.8 * s / 0.8)), z=14.5, wc=0.5,
               motion=puff_motion(tp, (x, cy0)))

    # ---- neighbours in the middle of the street: listen to the decree, kneel to pray ----
    mids = [("woman", 0, 3440, 1192, 0.88, -1, 0.0), ("child", 2, 3525, 1222, 0.86, -1, 0.15),
            ("elder", 1, 3610, 1168, 0.83, -1, 0.3)]
    for i, (kind, v, x, y, s, f, dt) in enumerate(mids):
        fr = [doc(person(kind, v, x, y, s, f, "listen")),
              doc(person(kind, v, x, y, s, f, "kneel_pray", "peaceful")),
              doc(person(kind, v, x, y, s, f, "kneel_pray", "worried")),
              doc(person(kind, v, x, y, s, f, "kneel_pray", "happy" if kind == "child" else "peaceful"))]
        tk, tw, th = snap(t_pray + 0.35 + dt), snap(t_kneel + 0.2 + dt), snap(t_hope + 0.15 + dt)
        sc.add(f"mid{i}", fr, z=9.5 + y / 1000, frame_at=cuts([(0, 0), (tk, 1), (tw, 2), (th, 3)]),
               motion=M.combine(dip(tk, s, (x, y)), dip(tw, s, (x, y), 4), dip(th, s, (x, y), 4),
                                M.breathe(0.01, 2.9, pivot=(x, y), phase=0.27 * i)))

    # ---- the families ----
    # background prayers (already kneeling)
    backs = [("woman", 3, 3720, 1150, 0.78, 1)]
    for i, (kind, v, x, y, s, f) in enumerate(backs):
        fr = [doc(person(kind, v, x, y, s, f, "kneel_pray", "peaceful")),
              doc(person(kind, v, x, y, s, f, "kneel_pray", "worried")),
              doc(person(kind, v, x, y, s, f, "kneel_pray", "peaceful"))]
        tw, th = snap(t_kneel + 0.5 + 0.2 * i), snap(t_hope + 0.3 + 0.15 * i)
        sc.add(f"back{i}", fr, z=9.4, frame_at=cuts([(0, 0), (tw, 1), (th, 2)]),
               motion=M.combine(dip(tw, s, (x, y), 4), dip(th, s, (x, y), 4),
                                M.breathe(0.01, 3.2, pivot=(x, y), phase=0.4 * i)))

    # the two quarrelling neighbours
    def man_frames(a, facing):
        x, y, s, v = a["x"], a["y"], a["s"], a["v"]
        return [doc(person("man", v, x, y, s, facing, "point", "angry")),        # 0
                doc(person("man", v, x, y, s, facing, "stand", "surprised")),   # 1
                doc(person("man", v, x, y, s, facing, "sad", "sorry")),         # 2
                doc(person("man", v, x, y, s, facing, "walk_b", "sorry")),      # 3
                doc(person("man", v, x, y, s, facing, "point", "happy")),       # 4
                doc(person("man", v, x, y, s, facing, "kneel_pray", "worried")),  # 5
                doc(person("man", v, x, y, s, facing, "kneel_pray", "peaceful"))]  # 6
    for nm, a, f, dt in (("man_a", MAN_A, 1, 0.0), ("man_b", MAN_B, -1, 0.12)):
        x, y, s = a["x"], a["y"], a["s"]
        pv = (x, y)
        t1, t2, t3 = snap(t_stop + dt), snap(t_hang + dt), snap(t_step + dt)
        t4, t5, t6 = snap(t_shake), snap(t_kneel + dt), snap(t_hope + dt)
        shout = lambda t, dt=dt: Tf(rot=1.8 * math.sin(2 * math.pi * (t + dt) / 0.55)) if t < t_stop + dt else Tf()
        sc.add(nm, man_frames(a, f), z=13 + y / 1000,
               frame_at=cuts([(0, 0), (t1, 1), (t2, 2), (t3, 3), (t4, 4), (t5, 5), (t6, 6)]),
               motion=M.combine(
                   M.with_pivot(M.keys([(t3, {"dx": 0}), (t4 - 0.02, {"dx": f * SHAKE_DX})], "inout"), pv),
                   M.with_pivot(shout, pv),
                   dip(t1, s, pv, 6), dip(t2, s, pv, 5), dip(t3, s, pv, 4), dip(t4, s, pv, 5), dip(t5, s, pv),
                   dip(t6, s, pv, 4),
                   hop(t4 + 0.25, [(0, {"dy": 0}), (0.12, {"dy": -6}), (0.24, {"dy": 0}), (0.36, {"dy": -6}),
                                   (0.48, {"dy": 0})], pv),
                   M.breathe(0.01, 2.7, pivot=pv, phase=0.5 + dt)))
        hdp = bp("man", a["v"], x, y, s, f, "point")["head_top"]
        sc.add(nm + "_grr", [doc(grumble_markup(hdp[0] - f * 10, hdp[1] - 40, 1.0, seed=k + (3 if f < 0 else 0)))
                             for k in range(3)], z=14, wc=0, frame_at=lambda t: float(int(t * 6) % 3),
               motion=M.keys([(0, {"alpha": 1}), (t1 - 0.25, {"alpha": 1}), (t1, {"alpha": 0})], "sine"))

    # the big boy, the little girl and her toy lamb
    bx, by, bs, bv = KID_B["x"], KID_B["y"], KID_B["s"], KID_B["v"]
    gx2, gy2, gs2, gv2 = KID_G["x"], KID_G["y"], KID_G["s"], KID_G["v"]
    bh_stand1 = bp("child", bv, bx, by, bs, 1, "stand")["hands"][0]
    bh_stand0 = bp("child", bv, bx, by, bs, -1, "stand")["hands"][1]
    bh_point = bp("child", bv, bx, by, bs, -1, "point")["hands"][0]
    TS = 0.7
    toy_at = lambda h: toy_markup(h[0], h[1] + 26 * TS, TS)
    bfr = [doc(person("child", bv, bx, by, bs, 1, "stand", "angry", extra=toy_at(bh_stand1))),   # 0 keeps the toy
           doc(person("child", bv, bx, by, bs, -1, "stand", "sorry", extra=toy_at(bh_stand0))),  # 1 turns back
           doc(person("child", bv, bx, by, bs, -1, "point", "sorry", extra=toy_at(bh_point))),   # 2 gives it back
           doc(person("child", bv, bx, by, bs, -1, "stand", "happy")),                           # 3
           doc(person("child", bv, bx, by, bs, -1, "kneel_pray", "worried")),                    # 4
           doc(person("child", bv, bx, by, bs, -1, "kneel_pray", "happy"))]                      # 5
    bpv = (bx, by)
    sc.add("boy", bfr, z=13.5,
           frame_at=cuts([(0, 0), (t_turnb, 1), (t_give, 2), (t_take, 3), (snap(t_kneel + 0.25), 4),
                          (snap(t_hope + 0.2), 5)]),
           motion=M.combine(dip(t_turnb, bs, bpv), dip(t_give, bs, bpv, 5), dip(t_take, bs, bpv, 5),
                            dip(snap(t_kneel + 0.25), bs, bpv), dip(snap(t_hope + 0.2), bs, bpv, 4),
                            happy_hop(t_take + 0.3, bs, bpv, 14),
                            M.breathe(0.012, 2.4, pivot=bpv, phase=0.2)))
    gh_listen = bp("child", gv2, gx2, gy2, gs2, 1, "listen")["hands"][1]
    ghd = bp("child", gv2, gx2, gy2, gs2, 1, "sad")["head"]
    tears = tear_markup(ghd[0] + 12 * gs2, ghd[1] + 6 * gs2, gs2) + tear_markup(ghd[0] - 4 * gs2, ghd[1] + 10 * gs2,
                                                                                gs2 * 0.8)
    toy_ground = toy_markup(gx2 + 70 * gs2, gy2 + 4, TS)
    g2fr = [doc(person("child", gv2, gx2, gy2, gs2, 1, "sad", "sad", extra=tears)),                       # 0
            doc(person("child", gv2, gx2, gy2, gs2, 1, "stand", "surprised")),                            # 1
            doc(person("child", gv2, gx2, gy2, gs2, 1, "listen", "happy",
                       extra=toy_markup(gh_listen[0] + 10, gh_listen[1] + 30 * TS, TS))),                   # 2
            doc(person("child", gv2, gx2, gy2, gs2, 1, "kneel_pray", "worried", extra=toy_ground)),       # 3
            doc(person("child", gv2, gx2, gy2, gs2, 1, "kneel_pray", "happy", extra=toy_ground))]         # 4
    g2p = (gx2, gy2)
    sc.add("little_girl", g2fr, z=13.6,
           frame_at=cuts([(0, 0), (t_give + 0.1, 1), (t_take + 0.3, 2), (snap(t_kneel + 0.35), 3),
                          (snap(t_hope + 0.1), 4)]),
           motion=M.combine(dip(t_give + 0.1, gs2, g2p, 4), dip(t_take + 0.3, gs2, g2p, 5),
                            dip(snap(t_kneel + 0.35), gs2, g2p), dip(snap(t_hope + 0.1), gs2, g2p, 4),
                            happy_hop(t_take + 0.45, gs2, g2p, 16),
                            lambda t: Tf(dy=1.5 * math.sin(2 * math.pi * t / 0.5)) if t < t_give else Tf(),
                            M.breathe(0.012, 2.3, pivot=g2p, phase=0.7)))
    # the toy hops from his hand into hers
    ty0 = (bh_point[0], bh_point[1] + 26 * TS)
    ty1 = (gh_listen[0] + 10, gh_listen[1] + 30 * TS)
    sc.add("toy_fly", doc(toy_markup(ty0[0], ty0[1], TS)), z=13.7, motion=M.combine(
        M.keys([(t_take - 0.01, {"alpha": 0}), (t_take + 0.01, {"alpha": 1}), (t_take + 0.28, {"alpha": 1}),
                (t_take + 0.3, {"alpha": 0})], "linear", pivot=ty0),
        M.keys([(t_take, {"dx": 0}), (t_take + 0.3, {"dx": ty1[0] - ty0[0]})], "sine", pivot=ty0),
        M.keys([(t_take, {"dy": 0}), (t_take + 0.13, {"dy": -40}), (t_take + 0.3, {"dy": ty1[1] - ty0[1]})],
               ["out", "in"], pivot=ty0)))

    # behind them a young man comforts an old neighbour (a hand on his shoulder), then they kneel together
    ex_, ey_, es_ = 5236, 1166, 0.82
    yx_, yy_, ys_ = 5112, 1170, 0.85
    t_help = snap(within(c4a, 0.33))
    efr = [doc(person("elder", 0, ex_, ey_, es_, -1, "sad", "sad")),
           doc(person("elder", 0, ex_, ey_, es_, -1, "stand", "happy")),
           doc(person("elder", 0, ex_, ey_, es_, -1, "kneel_pray", "worried")),
           doc(person("elder", 0, ex_, ey_, es_, -1, "kneel_pray", "peaceful"))]
    yfr = [doc(person("man", 2, yx_, yy_, ys_, 1, "stand", "sorry")),
           doc(person("man", 2, yx_, yy_, ys_, 1, "point", "happy")),
           doc(person("man", 2, yx_, yy_, ys_, 1, "kneel_pray", "worried")),
           doc(person("man", 2, yx_, yy_, ys_, 1, "kneel_pray", "peaceful"))]
    for nm, fr, x, y, s, dts in (("help_elder", efr, ex_, ey_, es_, (0.35, 0.3, 0.2)),
                                 ("help_man", yfr, yx_, yy_, ys_, (0.0, 0.2, 0.1))):
        ta, tk, th = snap(t_help + dts[0]), snap(t_kneel + dts[1]), snap(t_hope + dts[2])
        sc.add(nm, fr, z=11.0 + (0.01 if nm == "help_man" else 0), frame_at=cuts([(0, 0), (ta, 1), (tk, 2), (th, 3)]),
               motion=M.combine(dip(ta, s, (x, y), 5), dip(tk, s, (x, y)), dip(th, s, (x, y), 4),
                                M.breathe(0.01, 3.1, pivot=(x, y), phase=0.2 if nm == "help_man" else 0.7)))

    # their mother watches, then kneels with them
    mo = MOTHER
    mofr = [doc(person("woman", mo["v"], mo["x"], mo["y"], mo["s"], -1, "listen", "worried")),
            doc(person("woman", mo["v"], mo["x"], mo["y"], mo["s"], -1, "stand", "happy")),
            doc(person("woman", mo["v"], mo["x"], mo["y"], mo["s"], -1, "kneel_pray", "worried")),
            doc(person("woman", mo["v"], mo["x"], mo["y"], mo["s"], -1, "kneel_pray", "peaceful"))]
    mop = (mo["x"], mo["y"])
    sc.add("mother", mofr, z=12.5,
           frame_at=cuts([(0, 0), (snap(t_take + 0.5), 1), (snap(t_kneel + 0.45), 2), (snap(t_hope + 0.25), 3)]),
           motion=M.combine(dip(snap(t_take + 0.5), mo["s"], mop, 4), dip(snap(t_kneel + 0.45), mo["s"], mop),
                            dip(snap(t_hope + 0.25), mo["s"], mop, 4), M.breathe(0.01, 3.0, pivot=mop, phase=0.1)))

    # ---- foreground framing (static) ----
    fg = (PR.grass_tuft(1990, SH - 4, 1.0, variant=2) + PR.jar(2085, SH - 40, 0.8) + PR.grass_tuft(2560, SH + 6, 0.9)
          + PR.bush(3080, SH + 20, 0.9, variant=3) + PR.grass_tuft(3560, SH + 4, 1.0, variant=1)
          + PR.jar(4300, SH - 44, 0.85, color="#b86a46") + PR.jar(4372, SH - 24, 0.6)
          + PR.grass_tuft(4520, SH + 2, 1.1, variant=2) + PR.bush(4760, SH + 20, 1.0, variant=1))
    sc.add("foreground", doc(fg), z=20)

    # ---- camera: on the king; with the heralds to the terrace; glide (with a small pull-back on the way, to keep
    # the on-screen speed gentle) to the yard; glide on to the families; at the end tilt up with their hopeful
    # gaze toward the warm light ----
    A = Cam(930, 822, 1860)
    A2 = Cam(905, 830, 1780)
    B = Cam(1480, 870, 1950)
    Cc = Cam(2575, 945, 1760)
    D = Cam(4360, 900, 1900)
    D2 = Cam(4375, 855, 2000)
    t_bc0 = max(L2.start - 0.3, t_arrive + 0.9)
    t_cd0 = c3b.start + 0.1
    sc.camera = cam_path([
        (0, A, 0), (t_sit - 0.5, A, 0), (c0c.end, A2, 0), (t_go - 0.15, A2, 0), (t_arrive + 0.75, B, 0),
        (t_bc0, B, 380), (t_bc0 + 3.0, Cc, 0), (t_cd0, Cc, 520), (t_cd0 + 4.3, D, 0), (t_hope - 0.2, D, 0),
        (T - 1.0, D2, 0)])

    # ---- effects ----
    sc.fx = [
        FX.motes((150, 500, 1700, 1150), count=26, t0=-1, t1=c1.end + 1.5, color=(255, 236, 196), size=(2.5, 5.5),
                 alpha=120, seed=31),
        FX.motes((ax - 200, SPOT_Y - 260, ax + 200, SPOT_Y - 40), count=10, t0=t_sit, t1=c1.end + 2,
                 color=(214, 208, 200), size=(2.5, 5), alpha=150, seed=37),
        FX.motes((3000, 200, 4800, 1200), count=26, t0=t_hope, t1=T + 1, color=(255, 238, 196), size=(3, 7),
                 alpha=130, seed=41),
    ]

    # ---- sound ----
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_sack, gain_db=-8)
    sc.sfx("cloth", t_sit - 0.05, gain_db=-14)
    sc.sfx("footsteps", t_go, dur=t_arrive - t_go, gain_db=-14, fade_in=0.05, fade_out=0.2, rate=1 / WALK_P)
    sc.sfx("horn", t_blow, dur=1.3, gain_db=-11, pan=-0.1, fade_out=0.5)
    sc.sfx("horn", t_blow + 1.0, dur=1.4, gain_db=-22, pan=0.5, fade_out=0.5)
    sc.sfx("thud", t_lid_on, gain_db=-10)
    sc.sfx("thud", t_mat_on, gain_db=-15, pan=0.3)
    for i, (tp, *_r) in enumerate(puffs):
        sc.sfx("pop", tp, gain_db=-14, pan=-0.2 + 0.15 * i)
    sc.sfx("cloth", t_cloth, gain_db=-14)
    sc.sfx("sheep", snap(t_cloth + 0.95), gain_db=-12, pan=0.35)
    sc.sfx("sparkle", t_hope + 0.2, gain_db=-18)
    return sc
