"""Scene 17 — the king of Nineveh repents and sends out his decree (Jonah 3:6-9), v2.

One wide 5400 x 1440 stage, no cuts: the palace throne room on the left (the same purple-curtained portico,
throne and king as v1 s10), its terrace and steps, then the street outside — a little animal yard with a feed
manger and a stone water trough, and a street where families live. The camera opens on the palace roof-line
and a warm sky (no figure in frame: s16 ends on a square full of kneeling people, with Jonah standing just where
the king sits here, and in s16's late-afternoon light), comes down and back onto the king as the news is told
(settled before he rises; the sky cools to lilac), and travels right with the heralds and the decree.

  line 0  "国王听说了，"            a messenger in sackcloth tells the seated king the news (sound arcs) and points
                                    out to the city; the king is startled ("!").
          "也从宝座上站起来，"      he leans forward, pushes himself half-way up (an in-between) and rises
                                    from his throne (spring up), and steps forward.
          "脱下漂亮的王袍，"        he reaches up, lifts off his tall crown and lowers it (in-betweens), turns to the throne and — in a cloth puff — his purple
                                    robe comes off and lands folded on the throne seat with the crown on top...
          "换上粗麻布衣服，"        ...and he stands in scratchy burlap sackcloth; he turns back, shivers.
          "坐在灰堆里，"            a heap of ashes puffs up in front of the throne; he crouches and sits down in it.
          "表示真心认错。"          he bows his head, sorry; the messenger and the scribe bow their heads too.
  line 1  "国王又派人在全城宣告："  the king lifts his head and speaks; the messenger and the scribe nod and walk out
                                    onto the terrace one after the other (planted-foot steps: the anchor advances
                                    one stride as each walk drawing cuts in, so the planted foot stays put; the
                                    camera goes with them); the scribe unrolls the decree by the column while the
                                    messenger blows his long bronze horn (s16's horn) against clear sky at the
                                    open end; the camera rests on them; far heralds answer from the roofs.
  line 2  "所有的人和牛羊，都不可以吃，"  (the king's words, read from the scroll) the camera glides on and pushes in
                                    close on the yard: a cow and a goat munch at the manger — the farmer lays a
                                    big plank lid over the hay (dust puff, bounce), they lift their heads ("?"); from
                                    here their heads are drawn in front of the lid (the swap hides in the puff).
          "也不可以喝。"            his daughter pulls a reed mat over the water trough; the lamb looks up ("?")
                                    (its head moves in front of the mat as it lands).
  line 3  "人和牛羊，都要穿上麻布衣服，"  the camera eases back out; pop, pop, pop: the cow, goat, sheep, lamb and
                                    donkey each get a little sackcloth blanket (cloth puffs and happy hops).
          "诚心向上帝呼求。"        the farmer, his daughter and the neighbours kneel and pray; the animals bow;
                                    the camera holds on the praying yard while a low grey overcast starts to roll
                                    in over the city, then glides on along the street (through the pause).
  line 4  "每个人都要改掉坏行为，"  two neighbours who were shouting and pointing at each other (storm-cloud
                                    grumbles over their heads) stop and hang their heads; a young man lays a kind
                                    hand on an old neighbour's shoulder;
          "不再欺负别人。"          a big boy who had snatched a little girl's toy lamb gives it back (she hugs it
                                    to her chest); the two men step together and shake hands.
          "说不定上帝会可怜我们，"  everyone kneels and looks up hopefully;
          "我们就能活下来！"        peaceful, hopeful faces (the children smile) under the grey, quiet overcast; the
                                    crier on the roof kneels too; the camera tilts up with their gaze to the low
                                    grey overcast over the rooftops (no family in frame: s18 opens on its own
                                    overcast over its roofs). No light yet: God's answer (the cloud parting, warm
                                    light) belongs to s18, which opens under the same grey cloud banks and gloom.
                                    Calm hold for the dissolve.

Camera: every pan stays under ~20 output px per frame (long pans widen the view a little in the middle, with
zero zoom speed at both ends, and the viewport's bottom edge is interpolated so the stage clamp never kinks a
move). Doves drift across the street sky (entering and leaving outside the frame, with soft fades as a backstop);
a crier on a roof keeps reading.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a small squash /
dip, or under a cloth puff; the king's three key actions (rise, crown off, sit in the ashes) and the two
reconciled neighbours' kneel also get short in-between drawings (custom pose dicts, see king_ib / man_ib). All times are derived from the narration chunks.
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
DONKEY = dict(x=3275, y=1150, s=0.78, f=-1)  # rump ends at x ~3365, left of the families' framing

# the families (drawn closer together than in the first draft so the pan from the yard is shorter and the
# whole group, helpers included, fits inside the final framing with a margin)
MAN_A = dict(x=3830, y=1272, s=1.0, v=1)
MAN_B = dict(x=4280, y=1278, s=1.0, v=3)
SHAKE_DX = 99                        # each man steps this far toward the other to shake hands
KID_G = dict(x=4475, y=1272, s=0.85, v=1)    # the little girl (kept above the subtitle band in the end framing)
KID_B = dict(x=4665, y=1264, s=1.0, v=0)     # the big boy
MOTHER = dict(x=4800, y=1212, s=0.92, v=2)
ELDER = dict(x=5065, y=1166, s=0.82)         # the old neighbour...
HELPER = dict(x=4915, y=1190, s=0.85)        # ...and the young man who comforts him: standing a little in front
#                                              and back from the elder, so his hand lands on the elder's shoulder

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


def trap(a=0.3):
    """Ease with a smooth trapezoid velocity profile: sine ramps over the first and last ``a`` of the move and a
    constant cruise between (peak speed 1/(1-a) x the average, vs 1.57 x for a plain sine ease)."""
    def f(u):
        if u <= 0:
            return 0.0
        if u >= 1:
            return 1.0
        if u < a:
            s = u / 2 - a / (2 * math.pi) * math.sin(math.pi * u / a)
        elif u <= 1 - a:
            s = a / 2 + (u - a)
        else:
            w = 1 - u
            s = (1 - a) - (w / 2 - a / (2 * math.pi) * math.sin(math.pi * w / a))
        return s / (1 - a)
    return f


def cam_path(keys):
    """keys [(t, Cam, bump[, curve[, zoom_lag]])]: eased moves between key cameras (each key is clamped to the
    stage first). ``bump`` widens the view by that many stage px in the middle of the move that starts at the key
    (a gentle pull-back that keeps long pans calm on screen); it follows sin^2, so the zoom starts and ends at zero
    speed. ``zoom_lag`` (0..1) holds the width change back until that fraction of the move, so a pan that ends in
    a push-in zooms while it is already slowing down (keeps the on-screen speed of the fast middle part low).
    The viewport's BOTTOM edge is interpolated (not its centre) and the bump grows the view upward, so moves near
    the bottom of the stage never run into the clamp mid-move (no kinks)."""
    keys = sorted([(k[0], clamp_cam(k[1]), k[2], k[3] if len(k) > 3 else "sine", k[4] if len(k) > 4 else 0.0)
                   for k in keys], key=lambda k: k[0])

    def bottom(c):
        return c.y + c.w * 9 / 32

    def c(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, bump, curve, zl), (t1, b, _, _, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, curve)
                v = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
                uw = M.progress(v, zl, 1.0, "sine") if zl > 0 else u
                w = M.lerp(a.w, b.w, uw) + bump * math.sin(math.pi * v) ** 2
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
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


def step_walk(t0, n, step, period, s, move=0.15):
    """Planted-foot walk with only two stride drawings (walk_a / walk_b): the drawing follows the distance, not
    the clock. Each stride drawing holds its anchor still (its planted foot stays on one floor spot); as the next
    drawing cuts in, the anchor advances one stride (``step`` px, ~85 figure px x scale: walk_a's planted front
    foot at +45 becomes walk_b's pushing back foot at -40) with a short ease and a little lift.
    Returns (frame_at(t) -> 0/1 for a/b or None when not walking, dx(t), dy(t), t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]     # drawing k (k even: walk_a) cuts in here
    t_end = snap(t0 + n * period)

    def fa(t):
        if t < cut_t[0] or t >= t_end:
            return None
        k = min(n - 1, int((t - t0) / period))
        return float(k % 2)

    def dx(t):
        x = 0.0
        for k in range(n):
            x += step * M.progress(t, cut_t[k] - move * 0.45, cut_t[k] + move * 0.55, "sine")
        return x

    def dy(t):
        y = 0.0
        for k in range(n):
            tk = cut_t[k]
            if tk - move * 0.45 <= t <= tk + move * 0.55:
                y -= 6 * s * math.sin(math.pi * (t - tk + move * 0.45) / move)
        return y
    return fa, dx, dy, t_end


# ============================================================================ sky & city (static backdrops)


def sky_svg():
    defs = S.lin_grad("s17sky", [(0, "#a7a7bf"), (0.35, "#c3bfcb"), (0.68, "#e0d3c6"), (1, "#eedfc2")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="1120" fill="url(#s17sky)"/>', defs)


def sky_warm_svg():
    """s16's warm late-afternoon light (cream-peach sky, golden glow at the upper right of the opening framing)
    over this sky for the first second, so the s16 -> s17 dissolve stays in one light; it fades to s17's cool
    lilac once the camera has come down into the throne room."""
    defs = (S.lin_grad("s17skyw", [(0, "#c4bcb6"), (0.1, "#e6d6c2"), (0.3, "#efdcbf"), (0.55, "#f4d9ae"),
                                   (0.8, "#f6d3a0"), (1, "#f6cd94")]) +
            S.rad_grad("s17sunw", [(0, "#fff3cf", 0.95), (0.3, "#ffe6ad", 0.7), (0.65, "#ffd793", 0.3),
                                   (1, "#ffcf88", 0)]))
    # (only the palace end of the stage: the camera stays left of x ~1870 while this shows)
    return doc(f'<rect x="-20" y="-20" width="2120" height="1120" fill="url(#s17skyw)"/>'
               f'<ellipse cx="1950" cy="120" rx="760" ry="600" fill="url(#s17sunw)"/>', defs)


CLOUDS_BACK = [(1500, 175, 520, 150, 1), (2350, 120, 420, 120, 2), (3150, 205, 560, 160, 3), (4000, 130, 460, 130, 4),
               (4800, 240, 460, 130, 5), (900, 110, 380, 110, 6), (5400, 150, 420, 120, 7)]
CLOUDS_FRONT = [(1900, 330, 360, 100, 11), (2900, 400, 300, 86, 12), (3700, 340, 380, 104, 13),
                (4450, 430, 300, 84, 14), (1250, 470, 260, 74, 15), (5150, 360, 340, 96, 16)]


def clouds_svg(items, fill, shade):
    body = "".join(S.cloud(cx, cy, w, h, fill, seed=sd, puffs=5, sw=3, shade_fill=shade) for cx, cy, w, h, sd in items)
    return doc(S.g(body, filter="wobble"))


# the low grey overcast that rolls in over the street while the city prays (it continues into s18, which opens
# under the same cloud banks and gloom; the colours are s18's overcast greys). (cx, cy, w, h, seed) per bank.
OVERCAST = {
    "back": ([(2650, 70, 900, 300, 71), (3450, 40, 960, 320, 72), (4300, 60, 1000, 330, 73),
              (5150, 40, 940, 310, 74)], ("#9b9eac", "#828495")),
    "front": ([(3050, 270, 780, 260, 76), (3900, 260, 860, 280, 77), (4750, 280, 840, 270, 78),
               (5450, 260, 700, 250, 79)], ("#9294a3", "#7b7d8c")),
    "low": ([(3450, 440, 560, 170, 80), (4330, 452, 620, 180, 81), (5120, 432, 540, 165, 82)],
            ("#9fa1ac", "#8c8d98")),
}


def overcast_svg(kind):
    items, (fill, shade) = OVERCAST[kind]
    body = "".join(S.cloud(cx, cy, w, h, fill, seed=sd, puffs=6, sw=3.5, shade_fill=shade)
                   for cx, cy, w, h, sd in items)
    return doc(S.g(body, filter="wobble"))


def gloom_fx(alpha_fn):
    """Cool multiply glaze, strongest at the top of the frame — the same profile and colours as s18's opening
    gloom under the overcast, so the s17 -> s18 dissolve stays in one light. alpha_fn(t) -> 0..1."""
    ys = (np.arange(OUT_H) + 0.5) / OUT_H
    gstr = np.interp(ys, [0, 0.4, 0.7, 1.0], [0.32, 0.27, 0.17, 0.1])[:, None]
    top, bot = np.array([0x8d, 0x90, 0xad]) / 255.0, np.array([0xb4, 0xb1, 0xc0]) / 255.0
    v = ys[:, None]
    gdark = gstr * (1 - (top * (1 - v) + bot * v))          # (OUT_H, 3) darkening at full strength

    def fx(frame, t, view):
        a = float(alpha_fn(t))
        if a <= 0.003:
            return frame
        m4 = np.full((OUT_H, OUT_W, 4), 255, np.uint8)
        m4[..., :3] = np.clip((1 - gdark * a) * 255 + 0.5, 0, 255).astype(np.uint8)[:, None, :]
        arr = cv2.multiply(np.asarray(frame), m4, scale=1 / 255.0)
        return Image.fromarray(arr, "RGBA")
    return fx


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
    # (the first palm stands right of the terrace corner, clear of the horn's bell and blast against the sky)
    for x, s, ln in ((2150, 0.46, 0.08), (2850, 0.5, 0.12), (3640, 0.48, -0.08), (4490, 0.5, 0.1),
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
    # (no one kneels right behind the donkey — a head would peek above its back — or where the cow's "?" goes)
    for i, x in enumerate((2060, 2330, 2635, 2760, 3060, 2915, 3700, 4020, 4480, 4880, 5120, 5300)):
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
    xe = x0 + 95 * ((x1 - x0) // 95) + 12        # the rails end just past the last post (nothing pokes into the
    for yy in (y - 70, y - 34):                   # families' framing)
        rails += (f'<path d="M{x0 - 20},{yy} C{(x0 + xe) / 2},{yy + 6} {(x0 + xe) / 2},{yy - 6} {xe},{yy}" '
                  f'stroke="{ink}" stroke-width="15" fill="none" stroke-linecap="round"/>'
                  f'<path d="M{x0 - 20},{yy} C{(x0 + xe) / 2},{yy + 6} {(x0 + xe) / 2},{yy - 6} {xe},{yy}" '
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


LID_H = 44                           # the plank lid's thickness (it covers the whole hay heap when it lands)


def plank_markup(cx, cy, s=1.0):
    """The wooden lid for the manger, centred at (cx, cy): a big pale board of three planks with two battens."""
    w, h = (MANGER[1] - MANGER[0] + 44) * s, LID_H * s
    x0, y0 = cx - w / 2, cy - h / 2
    out = (f'<rect x="{f1(x0)}" y="{f1(y0)}" width="{f1(w)}" height="{f1(h)}" rx="{6 * s}" fill="#efd7a4" '
           f'stroke="{INK}" stroke-width="{4.5 * s:.1f}"/>'
           f'<rect x="{f1(x0 + 6 * s)}" y="{f1(y0 + 5 * s)}" width="{f1(w - 12 * s)}" height="{f1(7 * s)}" '
           f'rx="{3 * s}" fill="#f8e6bf" opacity="0.9"/>')
    for k in (1, 2):
        yy = y0 + h * k / 3
        out += (f'<path d="M{f1(x0 + 5 * s)},{f1(yy)} L{f1(x0 + w - 5 * s)},{f1(yy)}" stroke="{P["wood_dark"]}" '
                f'stroke-width="{2.6 * s:.1f}" opacity="0.8"/>')
    for bx in (x0 + w * 0.22, x0 + w * 0.78):
        out += (f'<rect x="{f1(bx - 11 * s)}" y="{f1(y0 - 3 * s)}" width="{22 * s}" height="{f1(h + 6 * s)}" '
                f'rx="{3 * s}" fill="{P["wood"]}" stroke="{INK}" stroke-width="{3.5 * s:.1f}"/>'
                f'<circle cx="{f1(bx)}" cy="{f1(y0 + 8 * s)}" r="{2.6 * s:.1f}" fill="{INK}"/>'
                f'<circle cx="{f1(bx)}" cy="{f1(y0 + h - 8 * s)}" r="{2.6 * s:.1f}" fill="{INK}"/>')
    return S.g(out, filter="wobble-fine")


def dust_markup(cx, cy, w, seed=0):
    """A low puff of sandy dust (a lid / mat landing)."""
    rng = random.Random(seed)
    out = ""
    for i in range(3):
        px = cx + (i - 1) * w * 0.32 + rng.uniform(-6, 6)
        py = cy - rng.uniform(0, 12)
        sz = rng.uniform(46, 60) * w / 120
        out += S.cloud(px, py, sz, sz * 0.58, "#efe0bf", seed=seed * 11 + i, puffs=3, sw=2.2, shade_fill="#dcc79c")
    return S.g(out, filter="wobble-fine", opacity=0.9)


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


def blast_markup(x, y, facing, k, s=1.0, ang=-42, sw=5.5, halo=False):
    """Horn blast: three wide arcs from the bell, tilted up along the horn (``halo``: over a faint cream halo so
    they read against any background)."""
    out, under = "", ""
    for i in range(3):
        r = (30 + 26 * i + (k - 2) * 4) * s
        a0, a1 = math.radians(ang - 32), math.radians(ang + 32)
        p0 = (x + facing * r * math.cos(a0), y + r * math.sin(a0))
        p1 = (x + facing * r * 1.12 * math.cos(math.radians(ang)), y + r * 1.12 * math.sin(math.radians(ang)))
        p2 = (x + facing * r * math.cos(a1), y + r * math.sin(a1))
        d = f'M{f1(p0[0])},{f1(p0[1])} Q{f1(p1[0])},{f1(p1[1])} {f1(p2[0])},{f1(p2[1])}'
        if halo:
            under += (f'<path d="{d}" fill="none" stroke="#fff6e2" stroke-width="{(sw + 11) * s:.1f}" '
                      f'stroke-linecap="round" opacity="0.6"/>')
        out += (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw * s:.1f}" stroke-linecap="round" '
                f'opacity="0.88"/>')
    return S.g(under + out, filter="wobble-fine")


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
    halo = (f'<ellipse cx="{f1(x + 2 * s)}" cy="{f1(y - 42 * s)}" rx="{40 * s:.1f}" ry="{54 * s:.1f}" '
            f'fill="#fbf1dc" opacity="0.7" filter="url(#soft)"/>')
    return halo + S.g(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{13 * s:.1f}" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="#e8b63c" stroke-width="{6.5 * s:.1f}" stroke-linecap="round"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y - 2 * s)}" r="{7 * s:.1f}" fill="#e8b63c" stroke="{INK}" '
               f'stroke-width="{3.5 * s:.1f}"/>', filter="wobble-fine")


def grumble_markup(x, y, s=1.0, seed=0):
    """An angry little storm cloud centred at (x, y) over a head: a dark jagged puff on a soft light backing, with
    three short yellow lightning ticks under it (k-variants via ``seed`` flicker the zig-zags)."""
    rng = random.Random(seed)
    n = 18
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = (1.0 if i % 2 == 0 else 0.72) + rng.uniform(-0.06, 0.06)
        pts.append((x + 62 * s * r * math.cos(a), y + 36 * s * r * math.sin(a)))
    jag = "M" + " L".join(f"{f1(px)},{f1(py)}" for px, py in pts) + " Z"
    backing = (f'<ellipse cx="{f1(x)}" cy="{f1(y + 8 * s)}" rx="{86 * s:.1f}" ry="{66 * s:.1f}" fill="#fbf1dc" '
               f'opacity="0.75" filter="url(#soft)"/>')
    puff = (f'<path d="{jag}" fill="#5f5b6e" stroke="{INK}" stroke-width="{4.5 * s:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{f1(x - 34 * s)},{f1(y - 8 * s)} q{18 * s:.1f},{-12 * s:.1f} {36 * s:.1f},0" fill="none" '
            f'stroke="#8a869a" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>')
    bolts = ""
    for bx, ln in ((-30, 30), (2, 38), (32, 28)):
        x0, y0 = x + bx * s + rng.uniform(-3, 3) * s, y + 30 * s
        d = (f"M{f1(x0)},{f1(y0)} l{-7 * s:.1f},{ln * 0.45 * s:.1f} l{12 * s:.1f},{-3 * s:.1f} "
             f"l{-8 * s:.1f},{ln * 0.55 * s:.1f}")
        bolts += (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{9 * s:.1f}" stroke-linecap="round" '
                  f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#f2c84a" stroke-width="{4.5 * s:.1f}" '
                  f'stroke-linecap="round" stroke-linejoin="round"/>')
    return backing + S.g(bolts + puff, filter="wobble-fine")


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


# ---- the king's in-between drawings (custom pose dicts, built the way s14 builds Jonah's half-kneel RISE), so
# his three key actions (rise from the throne, lift off the crown, sit down in the ashes) are not one-frame swaps
_KR = C._KING_M["R"]


def king_ib(attire, design_pose, ps, expr, x, y, facing=1, crown=None):
    """In-between king drawing from a custom pose dict ``ps`` (design_pose 'stand' = crown on his head,
    'remove_crown' = crown in his hands). ``crown`` = (dx, dy, rot, tilt) re-places the held crown relative to the
    hands (in head radii; the library's own hold is (-0.05, 0.58, -8, 1.0), with the hands at the crown's middle)."""
    D = C._king_design(attire, design_pose, False, False)
    if crown is not None:
        cdx, cdy, crot, ctilt = crown
        skin = D["skin"]

        def held(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            r = st["m"]["R"]
            c = C._lerp(W0, W1, 0.5)
            out = (f'<g transform="translate({C._pt(c)}) rotate({crot})">'
                   f'{C._crown(r, x0=cdx * r, y0=cdy * r, k=1.0, tilt=ctilt)}</g>')
            for W in (W0, W1):
                out += (f'<circle cx="{C.fmt(W[0])}" cy="{C.fmt(W[1])}" r="{C.fmt(st["m"]["hr"])}" fill="{skin}" '
                        f'{C._st(3.2)}/>')
            return out
        D["front"] = held
    inner, _ = C._figure(D, C._KING_M, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, KS, facing, f"king-ib-{design_pose}")


def _hold(x, y, h=0.0, over=False):
    """Both hands holding the crown in front of him, around body point (x, y) (as the library's remove_crown)."""
    return C._P(t=-2, h=h, arms=(("ik", "body", x + 0.80 * _KR, y, 1), ("ik", "body", x - 0.86 * _KR, y + 2, 1)),
                hands=("none", "none"), far_over_head=over)


def _crouch(t, h, drop, a, b, kn=0.28):
    """Knees bent (both feet planted at a, b), hands on the knees: on the way down into the ash heap."""
    return C._P(t=t, h=h, drop=drop, legs=(("ik", a, 1), ("ik", b, 1)),
                arms=(("ik", "knee", 0, kn, 1), ("ik", "knee", 1, kn, 1)), hem=0.97, flare=-8)


# half-way up from the throne: pelvis lowered, both feet planted, hands pushing on the knees
HALF_RISE = C._P(t=18, h=-6, drop=35, legs=(("ik", 52, 1), ("ik", 64, 1)),
                 arms=(("ik", "knee", 0, 0.22, 1), ("ik", "knee", 1, 0.22, 1)), hem=0.97, flare=-6)
# taking off the crown (each step moves the crown ~50-90 stage px, never across his eyes for long):
# both hands reach up to it (design 'stand': still on his head) ...
CROWN_REACH = C._P(t=-2, h=-6, arms=(("ik", "head", 0.78, -1.15, 1), ("ik", "head", -0.70, -1.10, -1)),
                   hands=("open", "open"), far_over_head=True)
# ... lift it up and forward off his head (drawn with crown=CROWN_LIFT_AT) ...
CROWN_LIFT = C._P(t=-2, h=-6, arms=(("ik", "head", 1.45, -1.25, 1), ("ik", "head", 0.50, -1.35, -1)),
                  hands=("none", "none"), far_over_head=True)
CROWN_LIFT_AT = (0.0, 0.2, 16, 0.6)
# ... bring it out in front of his face (crown=CROWN_OUT_AT) ...
CROWN_OUT = _hold(110, -172, -2, over=True)
CROWN_OUT_AT = (-0.05, 0.4, 6, 0.8)
# ... and lower it beside his beard and on down to his chest (the library's remove_crown hold)
CROWN_LOWER = _hold(95, -120, 4)
CROWN_LOWER2 = _hold(80, -82, 6)
# sitting down into the ash heap (sackcloth): knees bend, then a deep crouch
CROUCH1 = _crouch(4, 4, 35, 36, 46, 0.24)
CROUCH2 = _crouch(8, 8, 72, 52, 64)

# a townsman half-way down to his knees (knees bent, hands coming together to pray)
HALF_KNEEL = C._P(t=2, h=-8, drop=22, legs=(("ik", 30, 1), ("ik", -30, 1)),
                  arms=(("ik", "torso", 1.3, 0.72, 1), ("ik", "torso", 1.3, 0.72, 1)), hands=("none", "pray"))


def man_ib(variant, ps, expr, x, y, s, facing):
    """In-between drawing of a townsman (citizen kind 'man', sackcloth) from a custom pose dict."""
    D = C._citizen_design("man", variant, "sackcloth")
    inner, _ = C._figure(D, C._ADULT, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"man{variant}-ib")


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
    t_attn = snap(c1.start + 0.2)              # the two straighten up (and nod)
    t_go = snap(c1.start + 0.55)               # ...and walk out to the terrace (planted-foot steps)
    WALK_P = 0.25                              # one stride drawing per WALK_P
    m_steps = 7
    t_arrive = snap(t_go + m_steps * WALK_P)
    t_horn = snap(t_arrive + 0.12)             # the messenger lifts the horn
    t_blow = t_horn + 0.18
    r_go = snap(t_go + 0.3)                    # the scribe follows
    r_steps = 5
    r_arr = snap(r_go + r_steps * WALK_P)
    t_scroll = snap(max(r_arr + 0.25, t_arrive))   # ...and unrolls the decree
    t_read = L2.start + 0.05                   # the king's words are read out
    t_horn_down = snap(max(L2.start + 0.15, t_blow + 0.9))   # the blast ends as the decree is read out
    t_lid = snap(within(c2a, 0.72))            # "都不可以吃": the farmer lifts the plank...
    t_lid_on = t_lid + 0.42                    # ...and lays it over the manger
    t_mat = snap(c2b.start + 0.12)             # "也不可以喝": the girl pulls the mat
    t_mat_on = t_mat + 0.38
    t_cloth = within(c3a, 0.4)                 # "都要穿上麻布衣服": blankets, pop pop pop
    t_pray = snap(c3b.start + 0.2)             # "诚心向上帝呼求": kneel and pray
    t_stop = snap(c4a.start + 1.1)             # "每个人都要改掉坏行为": the two men stop (first seen quarrelling)
    t_hang = snap(max(within(c4a, 0.3), t_stop + 0.4))   # ...hang their heads
    t_turnb = snap(max(within(c4a, 0.47), t_hang + 0.4))  # "不再欺负别人": the boy turns back
    t_give = snap(max(within(c4a, 0.6), t_turnb + 0.4))   # holds out the toy
    t_take = snap(max(within(c4a, 0.72), t_give + 0.4))   # she takes it, both smile
    t_step = max(within(c4a, 0.7), t_hang + 0.5)          # the men step together...
    t_shake = snap(max(within(c4a, 0.8), t_step + 0.35))  # ...and shake hands
    t_kneel = snap(c4b.start + 0.25)           # "说不定上帝会可怜我们": kneel, look up hopefully
    t_hope = snap(c4c.start + 0.2)             # "我们就能活下来": hopeful smiles (no light yet: that is s18)

    # ---- sky ----
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    # s16's warm light lingers over the sky and the clouds through the dissolve, then cools to this scene's lilac
    # (a crossfade of the same sky / cloud drawings) once the camera has come down into the throne room (the warm
    # sky layer itself is added last, so the other layers keep their watercolour seeds)
    warm_at = lambda t: 1 - M.progress(t, 1.0, 3.0, "sine")
    # the white clouds grey over while the city prays (a crossfade of the same drawing), and a low grey overcast
    # rolls in over the street from the top of the sky — the gloom s18 opens under (its warm light is s18's)
    t_oc0 = c3b.start
    t_grey = (t_oc0 + 0.5, c4b.start + 1.0)
    cloud_at = lambda t: 1 - warm_at(t) + M.progress(t, t_grey[0], t_grey[1], "sine")   # warm -> white -> grey
    sc.add("clouds_back", [clouds_svg(CLOUDS_BACK, "#fff3df", "#f2d2a6"), clouds_svg(CLOUDS_BACK, "#d7cfd6", "#bab0c0"),
                           clouds_svg(CLOUDS_BACK, "#aeadba", "#94939f")],
           z=1, wc=0.7, frame_at=cloud_at, motion=M.drift(vx=5))
    sc.add("clouds_front", [clouds_svg(CLOUDS_FRONT, "#fff3df", "#f2d2a6"), clouds_svg(CLOUDS_FRONT, "#e2d9da", "#c6bcc4"),
                            clouds_svg(CLOUDS_FRONT, "#b9b7c1", "#9e9caa")],
           z=1.6, wc=0.7, frame_at=cloud_at, motion=M.drift(vx=9))
    for k, (kind, ddy, ddx, dur, vx) in enumerate((("back", -300, 260, 9.0, -3), ("front", -360, 340, 8.0, -5),
                                                   ("low", -420, 420, 7.0, -7))):
        sc.add(f"overcast_{kind}", overcast_svg(kind), z=1.65 + 0.01 * k, wc=0.7, motion=M.combine(
            M.keys([(t_oc0 + 0.3 * k, {"dx": ddx, "dy": ddy}), (t_oc0 + 0.3 * k + dur, {"dx": 0, "dy": 0})], "out"),
            M.drift(vx=vx, t0=t_oc0 + 0.3 * k + dur),
            lambda t, k=k: Tf(dy=5 * math.sin(2 * math.pi * t / 9.0 + k))))

    # a few far doves drift across the sky over the street (life in the quiet, fasting city). Each path starts
    # and ends outside the frame the camera has at that moment (with a soft fade as a backstop).
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = (0, 1, 2, 3, 4, 3, 2, 1)
    DOVES = ((1, [(12.2, 1900, 180), (15.5, 2350, 470), (21.0, 3000, 440), (25.0, 3500, 300), (27.0, 3650, 60)],
              0.5, 10.0),
             # (dove 1 starts hidden behind the palace lintel)
             (1, [(14.9, 1440, 350), (17.0, 1950, 520), (23.0, 2900, 470), (26.5, 3500, 380), (28.8, 3800, 60)],
              0.4, 11.0),
             (-1, [(24.6, 5450, 440), (31.0, 4500, 470), (35.0, 3900, 420), (T + 0.6, 3700, 400)], 0.48, 9.5))
    for i, (fc, pts, s, rate) in enumerate(DOVES):
        x0, y0 = pts[0][1], pts[0][2]
        fr = [doc(PR.dove(x0, y0, s, fc, wing=w)) for w in wings]

        def fa(t, rate=rate, i=i):
            if int(t * 0.8 + i) % 3 == 2:          # glide now and then
                return 2.0
            return float(cyc[int(t * rate + i * 3) % 8])

        def mv(t, pts=pts, i=i):
            ta, tb = pts[0][0], pts[-1][0]
            if t <= ta or t >= tb:
                return Tf(alpha=0.0)
            for (t0, xa, ya), (t1, xb, yb) in zip(pts, pts[1:]):
                if t0 <= t <= t1:
                    u = (t - t0) / (t1 - t0)
                    x, y = M.lerp(xa, xb, u), M.lerp(ya, yb, u)
                    break
            a = min(1.0, (t - ta) / 0.4, (tb - t) / 0.4)
            return Tf(dx=x - pts[0][1], dy=y - pts[0][2] + 10 * math.sin(2 * math.pi * t / 1.7 + i), alpha=a)
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
    t_ck = snap(t_hope + 0.4)              # at the end he kneels too (pose cut hidden in a dip)
    sc.add("roof_crier", [doc(C.citizen(cx_, cy_, cs, -1, kind="man", variant=2, pose="point", attire="sackcloth",
                                        expr="call") + cscroll),
                          doc(C.citizen(cx_, cy_, cs, -1, kind="man", variant=2, pose="kneel_pray",
                                        attire="sackcloth"))], z=2.2, frame_at=cuts([(0, 0), (t_ck, 1)]),
           motion=M.combine(M.breathe(0.012, 2.6, pivot=(cx_, cy_)), dip(t_ck, cs, (cx_, cy_), 6),
                            lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * t / 2.3)
                                         * (1 - M.progress(t, t_ck - 0.7, t_ck - 0.2, "sine")), px=cx_, py=cy_)))
    sc.add("roof_crier_arcs", [doc(arcs_markup(ch["head"][0] - 40 * cs, ch["head"][1] + 22 * cs, -1, k, cs * 1.3))
                               for k in (1, 2, 3)], z=2.25, wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(L2.start, {"alpha": 0}), (L2.start + 0.2, {"alpha": 1}), (t_ck - 0.45, {"alpha": 1}),
                          (t_ck - 0.2, {"alpha": 0})], "sine"))

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

    # the king on the throne: listens, is startled, leans forward and squashes, pushes himself half-way up (an
    # in-between drawing for three frames), then hard-cuts to the standing king right in front of the seat (who
    # springs up)
    pv_seat = (THRONE_X, THRONE_Y)
    seat = [doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False)),
            doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False, expr="worried")),
            doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False, expr="surprised")),
            doc(king_ib("royal", "stand", HALF_RISE, "surprised", THRONE_X + 25, THRONE_Y + 9))]
    t_half = snap(t_rise - 0.1)
    sc.add("king_seat", seat, z=6, frame_at=cuts([(0, 0), (snap(t_tell + 0.3), 1), (snap(t_wow), 2), (t_half, 3)]),
           motion=M.combine(
               dip(snap(t_tell + 0.3), KS, pv_seat, 4), dip(snap(t_wow), KS, pv_seat, 6),
               # the seated lean ends at the half-rise cut (that drawing stands straight); gone at the swap
               hop(t_rise, [(-0.32, {"sy": 1, "rot": 0, "alpha": 1}),
                            (t_half - t_rise, {"sy": 0.94, "rot": 6, "alpha": 1}),
                            (t_half - t_rise + 0.01, {"sy": 1.0, "rot": 0, "alpha": 1}), (0, {"alpha": 1}),
                            (0.01, {"alpha": 0})], pv_seat, ["inout", "linear", "linear", "linear"]),
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
    # (the second puff rises as he crouches into the heap, so he lands in it)
    for nm, tt, w, sd, a in (("ash_puff1", t_ash, 300, 3, 0.6), ("ash_puff2", snap(t_sit - 0.13), 300, 5, 0.65)):
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
           doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False, expr="call")),                # 7
           # in-betweens (on twos): reach up to the crown, lift it up and forward off his head, bring it out in
           # front of his face, lower it beside his beard and on to his chest; bend the knees and crouch into the
           # ashes (no shadow: the heap covers his feet)
           doc(ksh + king_ib("royal", "stand", CROWN_REACH, "worried", SPOT_X, SPOT_Y)),                 # 8
           doc(ksh + king_ib("royal", "remove_crown", CROWN_LIFT, "sorry", SPOT_X, SPOT_Y,
                             crown=CROWN_LIFT_AT)),                                                       # 9
           doc(ksh + king_ib("royal", "remove_crown", CROWN_OUT, "sorry", SPOT_X, SPOT_Y,
                             crown=CROWN_OUT_AT)),                                                        # 10
           doc(ksh + king_ib("royal", "remove_crown", CROWN_LOWER, "sorry", SPOT_X, SPOT_Y)),            # 11
           doc(ksh + king_ib("royal", "remove_crown", CROWN_LOWER2, "sorry", SPOT_X, SPOT_Y)),           # 12
           doc(king_ib("sackcloth", "stand", CROUCH1, "sad", SPOT_X, SPOT_Y)),                           # 13
           doc(king_ib("sackcloth", "stand", CROUCH2, "sad", SPOT_X, SPOT_Y))]                           # 14
    F = 1 / 30                                 # (t_crown and t_sit sit mid-frame, so these cuts do too)
    t_reach, t_lift, t_out = t_crown - 11 * F, t_crown - 8 * F, t_crown - 6 * F
    t_lower, t_lower2 = t_crown - 4 * F, t_crown - 2 * F
    t_crouch1, t_crouch2 = t_sit - 6 * F, t_sit - 3 * F
    t_unspeak = snap(c1.end - 0.3)
    step = 0.17
    bob_keys = [(0, {"dy": 0, "rot": 0})]
    for i in range(4):
        bob_keys += [(i * step + step / 2, {"dy": -7, "rot": 1.6 * (1 if i % 2 else -1)}),
                     ((i + 1) * step, {"dy": 0, "rot": 0})]
    sc.add("king", kfr, z=7,
           frame_at=cuts([(0, 0), (t_reach, 8), (t_lift, 9), (t_out, 10), (t_lower, 11), (t_lower2, 12), (t_crown, 1),
                          (t_turn, 2), (t_sack, 3), (t_front, 4), (t_crouch1, 13), (t_crouch2, 14), (t_sit, 5),
                          (t_sorry, 6), (t_speak, 7), (t_unspeak, 6)]),
           motion=M.combine(
               M.keys([(t_rise, {"alpha": 0}), (t_rise + 0.01, {"alpha": 1})], "linear", pivot=kp),
               M.keys([(t_w0, {"dx": RISE_X - SPOT_X}), (t_w0 + 4 * step, {"dx": 0})], "inout", pivot=kp),
               hop(t_w0, bob_keys, kp),
               hop(t_rise, [(0, {"sy": 0.95, "rot": 3}), (0.08, {"sy": 1.04, "rot": 0}), (0.18, {"sy": 0.99}),
                            (0.28, {"sy": 1.0})], kp),
               hop(t_lift, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": -6 * KS, "sy": 1.02}), (0.12, {"dy": 0, "sy": 1})],
                   kp),
               dip(t_crown, KS, kp, 5), dip(t_turn, KS, kp, 6),
               hop(t_sack, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5, "sy": 0.96}), (0.12, {"dy": -3, "sy": 1.02}),
                            (0.26, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               dip(t_front, KS, kp, 6),
               hop(t_itch, [(0, {"rot": 0}), (0.08, {"rot": -1.6}), (0.16, {"rot": 1.6}), (0.24, {"rot": -1.3}),
                            (0.32, {"rot": 1.1}), (0.42, {"rot": 0})], (SPOT_X, SPOT_Y)),
               # sinks through the crouch drawing and lands in the heap
               hop(t_sit, [(-0.33, {"dy": 0, "sy": 1}), (t_crouch1 - t_sit, {"dy": 3, "sy": 0.99}),
                           (t_crouch2 - t_sit, {"dy": 6, "sy": 0.97}), (0, {"dy": 8, "sy": 0.95}),
                           (0.1, {"dy": -3, "sy": 1.03}), (0.25, {"dy": 0, "sy": 1})], kp,
                   ["in", "sine", "sine", "out", "sine"]),
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
    m_dist = HORN_X - mx
    m_fa, m_dx, m_dy, _ = step_walk(t_go, m_steps, m_dist / m_steps, WALK_P, ms)
    m_base = cuts([(0, 0), (t_tell, 1), (t_point, 2), (t_msg_back, 3), (t_bow, 4), (t_attn, 5), (t_arrive, 8),
                   (t_horn, 9), (t_horn_down, 10)])
    mp = (mx, my)
    sc.add("messenger", mframes, z=8.5,
           frame_at=lambda t: 6 + m_fa(t) if m_fa(t) is not None else m_base(t),
           motion=M.combine(
               M.with_pivot(lambda t: Tf(dx=m_dx(t), dy=m_dy(t)), mp),
               dip(t_tell, ms, mp, 4), dip(t_point, ms, mp), dip(t_msg_back, ms, mp), dip(t_bow, ms, mp, 6),
               dip(t_attn, ms, mp, 5), nod(t_attn + 0.1, mp, -3, 0.4), dip(t_arrive, ms, mp, 5),
               dip(t_horn, ms, mp), hop(t_blow, [(0, {"rot": 0}), (0.35, {"rot": -2.5}), (1.2, {"rot": -2.5}),
                                                 (1.45, {"rot": 0})], mp),
               dip(t_horn_down, ms, mp, 5),
               M.breathe(0.01, 2.8, pivot=mp, phase=0.6)))
    mh0 = bp("man", mv, mx, my, ms, -1, "stand")["head"]
    sc.add("msg_arcs", [doc(arcs_markup(mh0[0] - 58 * ms, mh0[1] + 28 * ms, -1, k, ms)) for k in (1, 2, 3)], z=9,
           wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_tell, {"alpha": 0}), (t_tell + 0.12, {"alpha": 1}), (t_point - 0.12, {"alpha": 1}),
                          (t_point, {"alpha": 0})], "sine"))
    sc.add("horn_blast", [doc(blast_markup(bell_m[0] + m_dist, bell_m[1], 1, k, ms, sw=7.5, halo=True))
                          for k in (1, 2, 3)], z=9,
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
    r_fa, r_dx, r_dy, _ = step_walk(r_go, r_steps, r_dist / r_steps, WALK_P, rs)
    r_base = cuts([(0, 0), (t_bow + 0.1, 1), (t_attn, 2), (r_arr, 5), (t_scroll, 6)])
    rp = (rx_, ry_)
    sc.add("scribe", rframes, z=8.2,
           frame_at=lambda t: 3 + r_fa(t) if r_fa(t) is not None else r_base(t),
           motion=M.combine(
               M.with_pivot(lambda t: Tf(dx=r_dx(t), dy=r_dy(t)), rp),
               dip(t_bow + 0.1, rs, rp, 6), dip(t_attn, rs, rp, 5), nod(t_attn + 0.15, rp, -3, 0.4),
               dip(r_arr, rs, rp, 5),
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

    def beast(name, a, kind, z, head_angle, hops=(), t_sack_=None, front=None):
        """``front`` = (z_front, t_swap): from t_swap on the head is drawn on a layer at z_front (in front of the
        manger lid / trough mat) instead of just above its body — a hard cut of the same drawing with the same
        motion (only its depth changes), so the faces stay visible once the food and water are covered."""
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
            hm = head_motion(body_m, head_angle, (x, y), pv, f)
            if front is None:
                sc.add(name + "_head", doc(h0), z=z + 0.01, motion=hm)
            else:
                zf, ts = front
                sc.add(name + "_head", doc(h0), z=z + 0.01,
                       motion=M.combine(hm, M.keys([(ts - 0.001, {"alpha": 1}), (ts, {"alpha": 0})], "linear")))
                sc.add(name + "_head_front", doc(h0), z=zf,
                       motion=M.combine(hm, M.keys([(ts - 0.001, {"alpha": 0}), (ts, {"alpha": 1})], "linear")))
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
    # once the lid / mat lands, the cow's, goat's and lamb's heads move in front of it (the swap hides under the
    # lid's dust puffs, z 11.75, which sit right on the two heads; and under the bouncing mat for the lamb)
    beast("cow", COW, "cow", 10.6, munch(t_cow_up, 6, 1.3, 0.2, -7, 4, t_pray + 0.3), hops=(snap(t_cloth),),
          t_sack_=snap(t_cloth), front=(11.72, snap(t_lid_on + 0.07)))
    beast("goat", GOAT, "goat", 11.2, munch(t_cow_up + 0.15, 7, 1.05, 0.6, -8, 4, t_pray + 0.45),
          hops=(snap(t_cloth + 0.3),), t_sack_=snap(t_cloth + 0.3), front=(11.73, snap(t_lid_on + 0.07)))
    beast("sheep", SHEEP, "sheep", 12.2, munch(t_lamb_up + 0.1, 5, 1.6, 0.3, -6, 4, t_pray + 0.4),
          hops=(snap(t_cloth + 0.6),), t_sack_=snap(t_cloth + 0.6))
    beast("lamb", LAMB, "sheep", 11.4, munch(t_lamb_up, 6, 1.2, 0.8, -9, 5, t_pray + 0.55),
          hops=(snap(t_cloth + 0.9),), t_sack_=snap(t_cloth + 0.9), front=(12.15, snap(t_mat_on + 0.08)))

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
    # the hay is hidden under the lid the moment it lands (the lid is taller than the heap)
    sc.add("hay", doc(hay_markup()), z=10.2,
           motion=M.keys([(t_lid_on - 0.01, {"alpha": 1}), (t_lid_on + 0.01, {"alpha": 0})], "linear"))
    sc.add("manger", doc(manger_markup()), z=11.6)
    lid_cx = (MANGER[0] + MANGER[1]) / 2
    lid_cy = MANGER[2] - 14
    lp = (lid_cx, lid_cy)
    ldx, ldy = fhand[0] - lid_cx + 40, fhand[1] - lid_cy + 6
    sc.add("lid", doc(plank_markup(lid_cx, lid_cy)), z=11.7, motion=M.combine(
        M.keys([(t_lid - 0.01, {"alpha": 0}), (t_lid + 0.01, {"alpha": 1})], "linear", pivot=lp),
        M.keys([(t_lid, {"dx": ldx, "dy": ldy, "rot": -14}), (t_lid + 0.12, {"dx": ldx, "dy": ldy - 6, "rot": -12}),
                (t_lid_on, {"dx": 0, "dy": 0, "rot": 0})], ["sine", "in"], pivot=lp),
        hop(t_lid_on, [(0, {"sy": 1, "dy": 0}), (0.06, {"sy": 0.86, "dy": 3}), (0.16, {"sy": 1.03, "dy": -11}),
                       (0.28, {"sy": 0.97, "dy": 0}), (0.36, {"sy": 1.0, "dy": -3}), (0.44, {"sy": 1, "dy": 0})],
            (lid_cx, lid_cy + LID_H / 2), ["out", "out", "in", "out", "in"])))
    for k, dxp in enumerate((-1, 1)):       # small puffs squeezed out at both ends of the lid
        px_, py_ = lid_cx + dxp * ((MANGER[1] - MANGER[0]) * 0.5 + 40), MANGER[2] - 4
        sc.add(f"lid_dust{k}", doc(dust_markup(px_, py_, 100, seed=40 + k)), z=11.75, wc=0.4,
               motion=hop(t_lid_on, [(-0.02, {"alpha": 0, "s": 0.5, "dx": 0, "dy": 0}),
                                     (0.07, {"alpha": 0.75, "s": 0.9}),
                                     (0.5, {"alpha": 0, "s": 1.25, "dx": dxp * 45, "dy": -22})], (px_, py_),
                          ["out", "sine"]))

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
    cow_head = (COW["x"] - 122 * COW["s"], COW["y"] - 292 * COW["s"])   # right above the cow, clear of the farmer
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
    mids = [("woman", 0, 3482, 1192, 0.88, -1, 0.0), ("child", 2, 3562, 1222, 0.86, -1, 0.15),
            ("elder", 1, 3642, 1168, 0.83, -1, 0.3)]
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
    backs = [("woman", 3, 3722, 1150, 0.78, 1)]
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
                doc(person("man", v, x, y, s, facing, "kneel_pray", "peaceful")),  # 6
                # in-between on the way down to his knees: knees bent, hands coming together
                doc(C.ground_shadow(x, y, s, 140, opacity=0.2) + man_ib(v, HALF_KNEEL, "worried", x, y, s, facing))]
    for nm, a, f, dt in (("man_a", MAN_A, 1, 0.0), ("man_b", MAN_B, -1, 0.12)):
        x, y, s = a["x"], a["y"], a["s"]
        pv = (x, y)
        t1, t2, t3 = snap(t_stop + dt), snap(t_hang + dt), snap(t_step + dt)
        t4, t5, t6 = snap(t_shake), snap(t_kneel + dt), snap(t_hope + dt)
        shout = lambda t, dt=dt: Tf(rot=1.8 * math.sin(2 * math.pi * (t + dt) / 0.55)) if t < t_stop + dt else Tf()
        sc.add(nm, man_frames(a, f), z=13 + y / 1000,
               frame_at=cuts([(0, 0), (t1, 1), (t2, 2), (t3, 3), (t4, 4), (t5 - 3 / 30, 7), (t5, 5), (t6, 6)]),
               motion=M.combine(
                   # one quick planted-foot step toward the other as the walk_b drawing cuts in (no glide)
                   M.with_pivot(M.keys([(t3 - 0.06, {"dx": 0}), (t3 + 0.12, {"dx": f * SHAKE_DX})], "sine"), pv),
                   hop(t3 - 0.06, [(0, {"dy": 0}), (0.09, {"dy": -7 * s}), (0.18, {"dy": 0})], pv),
                   M.with_pivot(shout, pv),
                   dip(t1, s, pv, 6), dip(t2, s, pv, 5), dip(t3, s, pv, 4), dip(t4, s, pv, 5), dip(t6, s, pv, 4),
                   # sinks through the half-kneel drawing (3 frames) onto his knees
                   hop(t5, [(-0.25, {"dy": 0, "sy": 1}), (-3 / 30, {"dy": 3 * s, "sy": 0.98}),
                            (0, {"dy": 9 * s, "sy": 0.95}), (0.13, {"dy": -3 * s, "sy": 1.015}),
                            (0.28, {"dy": 0, "sy": 1})], pv, ["in", "sine", "out", "sine"]),
                   hop(t4 + 0.25, [(0, {"dy": 0}), (0.12, {"dy": -6}), (0.24, {"dy": 0}), (0.36, {"dy": -6}),
                                   (0.48, {"dy": 0})], pv),
                   M.breathe(0.01, 2.7, pivot=pv, phase=0.5 + dt)))
        hdp = bp("man", a["v"], x, y, s, f, "point")["head_top"]
        sc.add(nm + "_grr", [doc(grumble_markup(hdp[0], hdp[1] - 72, 1.0, seed=k + (3 if f < 0 else 0)))
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
    toy_ground = toy_markup(gx2 + 50 * gs2, gy2 - 16, TS)      # by her knee, above the subtitle band
    toy_hug = (gh_listen[0] + 18, gh_listen[1] + 60 * TS)       # hugged to her chest, under her hand (face clear)
    g2fr = [doc(person("child", gv2, gx2, gy2, gs2, 1, "sad", "sad", extra=tears)),                       # 0
            doc(person("child", gv2, gx2, gy2, gs2, 1, "stand", "surprised")),                            # 1
            doc(person("child", gv2, gx2, gy2, gs2, 1, "listen", "happy",
                       extra=toy_markup(*toy_hug, TS))),                                                    # 2
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
    ty1 = toy_hug
    sc.add("toy_fly", doc(toy_markup(ty0[0], ty0[1], TS)), z=13.7, motion=M.combine(
        M.keys([(t_take - 0.01, {"alpha": 0}), (t_take + 0.01, {"alpha": 1}), (t_take + 0.28, {"alpha": 1}),
                (t_take + 0.3, {"alpha": 0})], "linear", pivot=ty0),
        M.keys([(t_take, {"dx": 0}), (t_take + 0.3, {"dx": ty1[0] - ty0[0]})], "sine", pivot=ty0),
        M.keys([(t_take, {"dy": 0}), (t_take + 0.13, {"dy": -40}), (t_take + 0.3, {"dy": ty1[1] - ty0[1]})],
               ["out", "in"], pivot=ty0)))

    # behind them a young man comforts an old neighbour (a hand on his shoulder), then they kneel together
    ex_, ey_, es_ = ELDER["x"], ELDER["y"], ELDER["s"]
    yx_, yy_, ys_ = HELPER["x"], HELPER["y"], HELPER["s"]
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
    sc.add("sky_warm", sky_warm_svg(), z=0.5, wc=0.5, motion=lambda t: Tf(alpha=warm_at(t)))

    # ---- camera: opens on the palace roof-line and the sky (no figure in frame: s16 ends on a square full of
    # kneeling people with Jonah standing just where the king sits here), comes down and back onto the king as the
    # news is told (settled before he rises); with the heralds to the terrace, where it rests on the horn and the
    # scroll; glide (with a small pull-back on the way, to keep the on-screen speed gentle) and push in close on the
    # yard for the two "not eat / not drink" beats; ease back out for the blankets and hold on the praying yard;
    # glide on to the families through the pause; at the end tilt up with their hopeful gaze to the grey overcast
    # over the rooftops (D3: no figure in frame), where s18 opens ----
    S0 = Cam(1160, 387, 1360)                        # lintel, merlons, column tops and sky; heads all below it
    t_s1 = 0.35                                      # the descent starts in the dissolve (s16's last frame holds)
    t_land = max(snap(t_wow) + 0.3, t_rise - 0.3)    # settled before the seated lean of the rise
    A = Cam(934, 822, 1860)
    A2 = Cam(905, 830, 1780)
    B = Cam(1600, 870, 1900)
    Cy = Cam(2560, 995, 1360)
    Cc = Cam(2820, 905, 1880)
    D = Cam(4330, 900, 1800)
    D3 = Cam(4410, 458, 1600)                        # the overcast over the rooftops (s18 opens on it)
    t_bc0 = max(L2.start + 0.25, t_arrive + 1.05)    # ~1 s on the horn and the scroll
    t_cy = max(t_bc0 + 2.7, t_lid + 0.3)             # (nearly) settled close on the yard as the lid is lifted
    t_cy1 = max(c2b.end + 0.1, t_mat_on + 1.0)
    t_cc = max(t_cloth - 0.15, t_cy1 + 1.6)
    t_cd0 = max(c3b.start + 1.2, t_pray + 1.0)       # hold on the kneeling yard
    t_cd1 = max(t_cd0 + 3.5, c4a.start + 1.4)
    t_up0 = max(t_hope + 0.4, T - 2.5)              # the hopeful smiles first, then up with their gaze...
    t_up1 = T - 0.9                                  # ...settled on the overcast for the dissolve
    sc.camera = cam_path([
        (0, S0, 0), (t_s1, S0, 0, trap(0.35)), (t_land, A, 0), (t_sit - 0.5, A, 0), (c0c.end, A2, 0),
        (t_go - 0.3, A2, 0), (t_arrive + 0.1, B, 0),
        (t_bc0, B, 350, trap(0.3), 0.35), (t_cy, Cy, 0), (t_cy1, Cy, 0), (t_cc, Cc, 0), (t_cd0, Cc, 480, trap(0.3)),
        (t_cd1, D, 0), (t_up0, D, 0, trap(0.35)), (t_up1, D3, 0)])

    # ---- effects ----
    # the cool gloom of the overcast deepens while the city prays (s18 opens in the same gloom)
    gloom = M.keys([(t_oc0, {"alpha": 0}), (c4a.end, {"alpha": 0.55}), (c4c.start, {"alpha": 0.85})], "sine")
    sc.fx = [
        FX.motes((150, 500, 1700, 1150), count=26, t0=-1, t1=c1.end + 1.5, color=(255, 236, 196), size=(2.5, 5.5),
                 alpha=120, seed=31),
        FX.motes((ax - 200, SPOT_Y - 260, ax + 200, SPOT_Y - 40), count=10, t0=t_sit, t1=c1.end + 2,
                 color=(214, 208, 200), size=(2.5, 5), alpha=150, seed=37),
        gloom_fx(lambda t: gloom(t).alpha),
    ]

    # ---- sound ----
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_sack, gain_db=-8)
    sc.sfx("cloth", t_sit - 0.05, gain_db=-14)
    sc.sfx("footsteps", t_go, dur=t_arrive - t_go, gain_db=-14, fade_in=0.05, fade_out=0.2, rate=1 / WALK_P)
    sc.sfx("horn", t_blow, dur=1.0, gain_db=-11, pan=-0.1, fade_out=0.4)    # fades before the decree's words
    # the roof heralds answer from across the city (fainter and further right)
    sc.sfx("horn", t_blow + 0.9, dur=1.4, gain_db=-22, pan=0.5, fade_out=0.5)
    sc.sfx("horn", t_blow + 1.7, dur=1.4, gain_db=-24, pan=0.7, fade_out=0.5)
    sc.sfx("thud", t_lid_on, gain_db=-10)
    sc.sfx("thud", t_mat_on, gain_db=-15, pan=0.3)
    for i, (tp, *_r) in enumerate(puffs):
        sc.sfx("pop", tp, gain_db=-14, pan=-0.2 + 0.15 * i)
    sc.sfx("cloth", t_cloth, gain_db=-14)
    # the puzzled lamb bleats in the pause after "也不可以喝" (not over the words)
    sc.sfx("sheep", L2.end + 0.05, gain_db=-17, pan=0.35)
    return sc
