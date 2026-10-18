"""Scene 9 — the king's sleepless night (Daniel 6:18).

The king's bedroom in the palace at night (one 2112 x 1188 stage): an indigo plastered wall with a painted
rosette frieze, a big arched window on the left (moon, stars and, far away on a dark hill, the two little torches
beside the den), a servants' archway on the far left, the bedroom door on the right, two bronze lamp stands, the
royal couch on a rug, a low table with the untouched supper, and a musician with her lyre.

  line 0 '那天晚上，国王回到宫里。'   the king comes in through the door (planted-foot walk, sad) and sits down on
                                      the edge of his couch, chin in hand (sit_sad).
         '他不吃饭，'                  he looks at the supper on the little table beside him and shakes his head.
         '也不要人奏乐，'              the musician, ready by her lyre, bows and quietly leaves through the archway;
                                      the lyre stays silent on its cushion.
         '整夜都睡不着觉。'            the moon climbs in the window, the lamps burn low; he cannot sit still: he
                                      stands up and paces toward the door, hands behind his back (pace_a/pace_b).
  line 1 '他走来走去，'                he turns and paces all the way back across the room ...
         '一会儿看看窗外，'            ... to the window, and stands looking out at the moon (toward the far den).
         '一会儿又叹一口气。'          he sighs: shoulders lift and drop, hand to his forehead (sad), a little
                                      breath-curl floats from his mouth.
         '他一直在想：但以理怎么样了？' he looks out again; a thought bubble rises from his head: Daniel sitting
                                      in the dark den, and a "?" — calm hold to the end (it dissolves into the den).

Pose changes are hard cuts on a squash dip; walking and pacing use planted-foot strides (s17 step_walk).
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import lut_tint, phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap, step_walk
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]
FLOOR = 990                # walking lane (feet)
WALL_Y = 880               # where the wall meets the floor
KS = 1.1                   # king scale
STEP = 85 * KS
WIN = (330, 770, 170, 720)  # window opening x0, x1, arch top, sill
DOOR = (1800, 2060, 330)   # door x0, x1, top of the arch
ARCH = (-40, 170, 380)     # servants' archway x0, x1, top
COUCH = (1340, 975, 1.0)
TABLE = (1000, 962)
MUS = (650, 985, 1.05)     # musician
LYRE = (520, 990)


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


def swap(t_on, t_off):
    return lambda t: Tf(alpha=1.0 if t_on <= t < t_off else 0.0)


def arch_path(x0, x1, top, bottom):
    r = (x1 - x0) / 2
    return (f"M{x0},{bottom} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{bottom} Z")


# ============================================================================ backdrops


def outside_svg():
    """What the window shows: night sky, moon glow, stars painted in, dark hills, the den's torches far away."""
    x0, x1, top, sill = WIN
    defs = S.lin_grad("s9sky", [(0, "#1c2444"), (0.6, "#2c3a62"), (1, "#4a5a82")])
    body = f'<rect x="{x0 - 20}" y="{top - 20}" width="{x1 - x0 + 40}" height="{sill - top + 40}" fill="url(#s9sky)"/>'
    rng = random.Random(4)
    for _ in range(18):
        x, y = rng.uniform(x0 + 10, x1 - 10), rng.uniform(top + 20, sill - 200)
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(1.6, 3.2))}" fill="#f2ead2" opacity="0.8"/>'
    body += S.path(S.hill(x0 - 40, x1 + 40, sill - 70, 90, seed=6, bottom=sill + 30), fill="#26304c", sw=3)
    body += S.path(S.hill(x0 - 40, x1 + 40, sill - 20, 50, seed=8, bottom=sill + 30), fill="#1e2740", sw=3)
    # far away on the hill: the two torches beside the den (tiny warm points)
    for tx in (548, 592):
        body += (f'<circle cx="{tx}" cy="{sill - 132}" r="16" fill="#f0a850" opacity="0.35" filter="url(#soft)"/>'
                 f'<circle cx="{tx}" cy="{sill - 132}" r="4" fill="#ffd690"/>'
                 f'<path d="M{tx},{sill - 128} L{tx},{sill - 112}" stroke="#4a3426" stroke-width="2"/>')
    return doc(S.g(body, filter="wobble"), defs)


def moon_svg():
    x, y = 505, 345
    defs = S.rad_grad("s9mg", [(0, "#fff6da", 0.6), (0.45, "#e8e2d0", 0.2), (1, "#e8e2d0", 0)])
    body = f'<circle cx="{x}" cy="{y}" r="170" fill="url(#s9mg)"/>'
    body += S.g(f'<circle cx="{x}" cy="{y}" r="54" fill="#f8efd2" stroke="{P["ink_soft"]}" stroke-width="3"/>'
                f'<circle cx="{x - 16}" cy="{y - 12}" r="10" fill="#eadfc0"/>'
                f'<circle cx="{x + 18}" cy="{y + 14}" r="8" fill="#eadfc0"/>'
                f'<circle cx="{x + 6}" cy="{y - 24}" r="5" fill="#eadfc0"/>', filter="wobble-fine")
    return doc(body, defs)


def room_svg():
    """Wall with the window/door/archway holes cut out, frieze, dado, floor, rug (static)."""
    x0, x1, top, sill = WIN
    defs = S.lin_grad("s9wall", [(0, "#2a3158"), (0.6, "#3a4370"), (1, "#454d78")])
    defs += S.lin_grad("s9floor", [(0, "#4a3e58"), (1, "#5d4c5e")])
    holes = (arch_path(x0, x1, top, sill) + " " + arch_path(DOOR[0], DOOR[1], DOOR[2], WALL_Y) + " " +
             arch_path(ARCH[0], ARCH[1], ARCH[2], WALL_Y))
    wall = f"M-20,-20 L{W + 20},-20 L{W + 20},{WALL_Y} L-20,{WALL_Y} Z " + holes
    body = f'<path d="{wall}" fill="url(#s9wall)" fill-rule="evenodd"/>'
    # frieze band with rosettes
    fy = 118
    body += f'<rect x="-20" y="{fy - 34}" width="{W + 40}" height="68" fill="#4f4a7a" {S.STROKE}/>'
    body += f'<rect x="-20" y="{fy - 22}" width="{W + 40}" height="44" fill="#3d5a7a"/>'
    for i, x in enumerate(range(30, W, 92)):
        body += (f'<circle cx="{x}" cy="{fy}" r="15" fill="#c9a24e" {S.STROKE_THIN}/>'
                 f'<circle cx="{x}" cy="{fy}" r="6" fill="#7b4f9d"/>')
    # dado band
    body += f'<rect x="-20" y="{WALL_Y - 150}" width="{W + 40}" height="150" fill="#323a62"/>'
    body += S.path(f"M-20,{WALL_Y - 150} L{W + 20},{WALL_Y - 150}", sw=3)
    for x in range(40, W, 140):
        body += f'<rect x="{x}" y="{WALL_Y - 120}" width="100" height="90" rx="10" fill="none" stroke="#4a5280" stroke-width="5"/>'
    # wall outline around the holes
    body += S.path(holes, sw=4.5)
    # window: thick frame, sill, curtains
    r = (x1 - x0) / 2
    frame = (f'<path d="M{x0 - 26},{sill} L{x0 - 26},{top + r} A{r + 26},{r + 26} 0 0 1 {x1 + 26},{top + r} '
             f'L{x1 + 26},{sill} L{x1},{sill} L{x1},{top + r} A{r},{r} 0 0 0 {x0},{top + r} L{x0},{sill} Z" '
             f'fill="#b9a27a" {S.STROKE}/>')
    frame += f'<rect x="{x0 - 44}" y="{sill}" width="{x1 - x0 + 88}" height="30" rx="6" fill="#c9b28a" {S.STROKE}/>'
    body += frame
    # floor with tiles and a rug
    body += f'<rect x="-20" y="{WALL_Y}" width="{W + 40}" height="{H - WALL_Y + 20}" fill="url(#s9floor)"/>'
    body += S.path(f"M-20,{WALL_Y} L{W + 20},{WALL_Y}", sw=4.5)
    tiles = ""
    for i in range(-12, 26):
        xa = W / 2 + i * 110
        xb = W / 2 + i * 220
        tiles += f'<path d="M{xa},{WALL_Y} L{xb},{H + 20}"/>'
    for yy in (900, 955, 1025, 1110):
        tiles += f'<path d="M-20,{yy} L{W + 20},{yy}"/>'
    body += f'<g stroke="#6d5a6e" stroke-width="3" opacity="0.6">{tiles}</g>'
    rug = f"M1000,{WALL_Y + 52} L1780,{WALL_Y + 52} L1880,{H - 60} L900,{H - 60} Z"
    body += S.path(rug, fill="#8a3e48", sw=4)
    body += S.path(f"M1030,{WALL_Y + 68} L1750,{WALL_Y + 68} L1842,{H - 78} L938,{H - 78} Z", fill="none",
                   sw=0, extra='stroke="#d6a65a" stroke-width="7"')
    for k in range(9):
        u = (k + 0.5) / 9
        cx = 1060 + 700 * u + (u - 0.5) * 60
        body += f'<circle cx="{f1(cx)}" cy="{H - 130}" r="12" fill="#d6a65a" opacity="0.8"/>'
    return doc(S.g(body, filter="wobble"), defs)


def openings_svg():
    """The dark corridor behind the door and the archway (drawn under the wall)."""
    body = (f'<path d="{arch_path(DOOR[0], DOOR[1], DOOR[2], WALL_Y + 5)}" fill="#1c1a2e"/>'
            f'<ellipse cx="{(DOOR[0] + DOOR[1]) / 2 - 30}" cy="{WALL_Y - 160}" rx="70" ry="100" fill="#4a3424" '
            f'opacity="0.7" filter="url(#soft)"/>')
    body += f'<path d="{arch_path(ARCH[0], ARCH[1], ARCH[2], WALL_Y + 5)}" fill="#1a1a2c"/>'
    return doc(body)


def frame_markup(x0, x1, top):
    r = (x1 - x0) / 2
    return (f'<path d="M{x0 - 22},{WALL_Y} L{x0 - 22},{top + r} A{r + 22},{r + 22} 0 0 1 {x1 + 22},{top + r} '
            f'L{x1 + 22},{WALL_Y} L{x1},{WALL_Y} L{x1},{top + r} A{r},{r} 0 0 0 {x0},{top + r} L{x0},{WALL_Y} Z" '
            f'fill="#8d6a4a" {S.STROKE}/>')


def wall_dress_svg():
    """Door frame with its curtain, window curtains, a tapestry behind the couch (behind the figures)."""
    body = frame_markup(*DOOR)
    body += (f'<path d="M{DOOR[1]},{DOOR[2] + 90} Q{DOOR[1] - 70},{DOOR[2] + 150} {DOOR[1] - 46},{WALL_Y - 280} '
             f'Q{DOOR[1] - 30},{WALL_Y - 120} {DOOR[1] - 60},{WALL_Y} L{DOOR[1]},{WALL_Y} Z" fill="#7b4f9d" {S.STROKE}/>')
    x0, x1, top, sill = WIN
    for sx, xe in ((-1, x0 - 26), (1, x1 + 26)):
        xi = xe - sx * 50
        body += (f'<path d="M{xe + sx * 40},{top - 20} Q{xi},{top + 160} {xe - sx * 10},{sill - 220} '
                 f'Q{xe + sx * 20},{sill - 120} {xe + sx * 10},{sill + 40} L{xe + sx * 70},{sill + 40} '
                 f'Q{xe + sx * 70},{sill - 200} {xe + sx * 60},{top - 20} Z" fill="#7b4f9d" {S.STROKE}/>')
        body += f'<ellipse cx="{xe + sx * 30}" cy="{sill - 220}" rx="34" ry="12" fill="#d6a65a" {S.STROKE_THIN}/>'
    body += (f'<path d="M{x0 - 80},{top - 30} L{x1 + 80},{top - 30}" stroke="#8d6a4a" stroke-width="14" '
             f'stroke-linecap="round"/>')
    # tapestry: a rosette and two friendly lions, hung from a rod behind the couch
    tx0, tx1, ty0, ty1 = 1400, 1660, 300, 660
    body += (f'<path d="M{tx0},{ty0} L{tx1},{ty0} L{tx1},{ty1} L{(tx0 + tx1) / 2 + 60},{ty1 - 10} L{(tx0 + tx1) / 2},'
             f'{ty1 + 22} L{(tx0 + tx1) / 2 - 60},{ty1 - 10} L{tx0},{ty1} Z" fill="#7a3a4a" {S.STROKE}/>')
    body += (f'<rect x="{tx0 + 22}" y="{ty0 + 22}" width="{tx1 - tx0 - 44}" height="{ty1 - ty0 - 60}" fill="none" '
             f'stroke="#d6a65a" stroke-width="7"/>')
    cxm, cym = (tx0 + tx1) / 2, ty0 + 150
    for j in range(12):
        a = j * math.pi / 6
        body += (f'<ellipse cx="{f1(cxm + 46 * math.cos(a))}" cy="{f1(cym + 46 * math.sin(a))}" rx="22" ry="11" '
                 f'fill="#d6a65a" transform="rotate({j * 30} {f1(cxm + 46 * math.cos(a))} {f1(cym + 46 * math.sin(a))})"/>')
    body += f'<circle cx="{cxm}" cy="{cym}" r="26" fill="#3d5a7a" {S.STROKE_THIN}/>'
    body += PR.lion(cxm - 70, ty1 - 64, 0.18, 1, pose="sit") + PR.lion(cxm + 70, ty1 - 64, 0.18, -1, pose="sit")
    body += f'<path d="M{tx0 - 30},{ty0} L{tx1 + 30},{ty0}" stroke="#8d6a4a" stroke-width="14" stroke-linecap="round"/>'
    return doc(S.g(body, filter="wobble-fine"))


def door_front_svg():
    """The servants' archway frame and its curtain (drawn over the musician leaving through it)."""
    body = frame_markup(*ARCH)
    body += (f'<path d="M{ARCH[1]},{ARCH[2] + 70} Q{ARCH[1] - 70},{ARCH[2] + 120} {ARCH[1] - 46},{WALL_Y - 260} '
             f'Q{ARCH[1] - 30},{WALL_Y - 120} {ARCH[1] - 60},{WALL_Y} L{ARCH[1]},{WALL_Y} Z" fill="#6a6a9a" {S.STROKE}/>')
    return doc(S.g(body, filter="wobble-fine"))


LAMPS = ((235, 935), (1690, 935))


def lamp_stand(x, y):
    """Tall bronze lamp stand (tripod feet) with a clay oil lamp on top (lit)."""
    top = y - 300
    body = (f'<path d="M{x - 50},{y} Q{x - 20},{y - 30} {x - 6},{y - 60} L{x + 6},{y - 60} Q{x + 20},{y - 30} {x + 50},{y} '
            f'L{x + 34},{y} Q{x + 10},{y - 30} {x},{y - 40} Q{x - 10},{y - 30} {x - 34},{y} Z" fill="#b3833f" {S.STROKE_THIN}/>')
    body += f'<rect x="{x - 7}" y="{top}" width="14" height="{y - 60 - top}" fill="#b3833f" {S.STROKE_THIN}/>'
    for yy in (top + 60, y - 120):
        body += f'<ellipse cx="{x}" cy="{yy}" rx="16" ry="7" fill="#d6a65a" {S.STROKE_THIN}/>'
    body += f'<ellipse cx="{x}" cy="{top}" rx="46" ry="10" fill="#d6a65a" {S.STROKE}/>'
    body += PR.oil_lamp(x - 14, top - 4, 0.75)
    return body


def table_svg():
    x, y = TABLE
    body = ""
    for lx in (-80, 0, 80):
        body += (f'<path d="M{x + lx - 7},{y - 70} L{x + lx * 1.15 - 6},{y} L{x + lx * 1.15 + 6},{y} L{x + lx + 7},{y - 70} Z" '
                 f'fill="#8d6a4a" {S.STROKE_THIN}/>')
    body += f'<ellipse cx="{x}" cy="{y - 74}" rx="140" ry="28" fill="#b3833f" {S.STROKE}/>'
    body += f'<ellipse cx="{x}" cy="{y - 78}" rx="120" ry="20" fill="#d6a65a"/>'
    body += PR.food_tray(x, y - 84, 0.68)
    return doc(S.g(body, filter="wobble-fine") + C.ground_shadow(x, y + 4, 1.0, 280, 0.25))


def lyre_svg():
    x, y = LYRE
    return doc(C.ground_shadow(x, y + 4, 0.7, 150, 0.25) + PR.cushion(x, y, 0.62, "#a17cc0") + PR.lyre(x + 6, y - 36, 0.62, -1))


def bubble_svg(cx, cy, r, trail):
    """Thought bubble: Daniel sitting peacefully in the dark den (a little picture), with three small puffs."""
    cid = "s9bub"
    inner = (f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#s9bg)"/>')
    rng = random.Random(3)
    for row in range(6):
        for col in range(7):
            sx = cx - r + col * 66 + (33 if row % 2 else 0) + rng.uniform(-6, 6)
            sy = cy - r + 18 + row * 44
            inner += (f'<ellipse cx="{f1(sx)}" cy="{f1(sy)}" rx="28" ry="17" fill="#5a4c66" stroke="#3a3048" '
                      f'stroke-width="2.5"/>')
    inner += f'<rect x="{cx - r}" y="{cy + r * 0.5}" width="{2 * r}" height="{r}" fill="#6a5a5a"/>'
    inner += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="{r * 0.75}" ry="{r * 0.7}" fill="url(#s9bglow)"/>'
    inner += PR.lion(cx - r * 0.5, cy + r * 0.7, 0.36, 1, pose="sleep", variant=0)
    inner += C.daniel(cx + 30, cy + r * 0.66, 0.7, -1, pose="sit_pray")
    body = (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>')
    body += S.g(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["foam"]}" stroke-width="14"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" {S.STROKE}/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r - 7}" fill="none" {S.STROKE_THIN}/>', filter="wobble-fine")
    defs = (S.rad_grad("s9bg", [(0, "#3a3050"), (1, "#221c34")]) +
            S.rad_grad("s9bglow", [(0, "#e8c27a", 0.45), (0.6, "#c99a5a", 0.12), (1, "#c99a5a", 0)]))
    return body, defs


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1 = ctx.line(0), ctx.line(1)

    t_food = phrase_t(L0, "不吃饭")
    t_music = phrase_t(L0, "不要人奏乐")
    t_sleep = L0.at("整夜都睡不着觉")
    t_window = phrase_t(L1, "看看窗外")
    t_sigh = L1.at("叹一口气")
    t_think = L1.at("他一直在想")
    t_what = phrase_t(L1, "但以理怎么样了")

    # ---------------------------------------------------------------- static room
    sc.add("outside", outside_svg(), seed=3)
    sc.add("moon", moon_svg(), wc=0.4, motion=M.keys([(0, {"dx": -30, "dy": 40}), (T, {"dx": 40, "dy": -20})],
                                                     "linear"))
    sc.add("openings", openings_svg(), seed=5)
    sc.add("room", room_svg(), seed=7)
    sc.add("wall_dress", wall_dress_svg(), seed=9)
    lamps = "".join(lamp_stand(x, y) for x, y in LAMPS)
    sc.add("lamps", doc(S.g(lamps, filter="wobble-fine") +
                        "".join(C.ground_shadow(x, y + 2, 1.0, 120, 0.25) for x, y in LAMPS)))
    cx, cy, cs = COUCH
    sc.add("couch", doc(C.ground_shadow(cx, cy + 4, 1.0, 420, 0.28) + PR.couch(cx, cy, cs, 1)))
    sc.add("table", table_svg())
    sc.add("lyre", lyre_svg())

    # ---------------------------------------------------------------- the musician: ready -> bows -> leaves
    mx, my, ms = MUS
    t_bow = snap(t_music + 0.15)
    m_go = snap(t_bow + 0.75)
    m_n = 5
    m_fa, m_dx, m_dy, m_end = step_walk(m_go, m_n, 85 * ms, 0.3, ms)
    mus = [doc(C.citizen(mx, my, ms, 1, kind="woman", variant=1, pose="stand", expr="happy")),
           doc(C.citizen(mx, my, ms, 1, kind="woman", variant=1, pose="sad", expr="sorry")),
           doc(C.citizen(mx, my, ms, -1, kind="woman", variant=1, pose="walk_a")),
           doc(C.citizen(mx, my, ms, -1, kind="woman", variant=1, pose="walk_b"))]
    mp = (mx, my)
    m_fade = M.keys([(m_end - 0.5, {"alpha": 1}), (m_end + 0.1, {"alpha": 0})], "sine")
    sc.add("sh_mus", doc(C.ground_shadow(mx, my, ms, 120, 0.28)),
           motion=M.combine(lambda t: Tf(dx=-m_dx(t)), m_fade))
    sc.add("musician", mus,
           frame_at=lambda t: 2 + m_fa(t) if m_fa(t) is not None else cuts([(0, 0), (t_bow, 1)])(t),
           motion=M.combine(lambda t: Tf(dx=-m_dx(t), dy=m_dy(t)), m_fade, dip(t_bow, ms, mp, 6),
                            dip(m_go - 0.02, ms, mp, 4), M.breathe(0.01, 3.0, pivot=mp)))

    # ---------------------------------------------------------------- the king
    # A: walks in from the door, sits on the couch, stands up and paces toward the door
    KX_IN = 1950
    n_in = 6
    k_fa, k_dx, k_dy, k_arr = step_walk(snap(0.45), n_in, STEP, 0.3, KS)
    KX_SIT0 = KX_IN - n_in * STEP                     # where he stops by the couch
    t_sit = snap(k_arr + 0.12)
    sit_x, sit_y = cx + 20 * cs, cy - 152 * cs + 67 * KS
    t_up = snap(t_sleep + 0.55)
    n_r = 2                                           # paces toward the door ...
    PP = 0.34
    r_fa, r_dx, r_dy, r_end = step_walk(snap(t_up + 0.35), n_r, STEP, PP, KS)
    t_turn = snap(r_end + 0.1)
    n_l = 9                                           # ... turns, and paces back across the room to the window
    l_fa, l_dx, l_dy, l_end = step_walk(snap(t_turn + 0.25), n_l, STEP, PP * 0.9, KS)
    KX_WIN = KX_SIT0 + n_r * STEP - n_l * STEP
    t_look = snap(max(l_end + 0.05, t_window - 0.2))
    t_sad = snap(t_sigh + 0.35)
    t_look2 = snap(t_think)

    walk_in = [doc(C.king(KX_SIT0, FLOOR, KS, -1, pose=p, attire="darius", expr="sad")) for p in ("walk_a", "walk_b")]
    walk_in += [doc(C.king(KX_SIT0, FLOOR, KS, -1, pose="stand", attire="darius", expr="sad"))]
    sc.add("sh_kin", doc(C.ground_shadow(KX_SIT0, FLOOR, KS, 130, 0.3)),
           motion=M.combine(swap(-1, t_sit), lambda t: Tf(dx=n_in * STEP - k_dx(t))))
    sc.add("king_in", walk_in, frame_at=lambda t: k_fa(t) if k_fa(t) is not None else 2.0,
           motion=M.combine(swap(-1, t_sit), lambda t: Tf(dx=n_in * STEP - k_dx(t), dy=k_dy(t))))

    # seated on the edge of the couch, chin in hand: shakes his head at the supper; open, worried eyes
    sit = [doc(C.king(sit_x, sit_y, KS, -1, pose="sit_sad", attire="darius", throne=False)),
           doc(C.king(sit_x, sit_y, KS, -1, pose="sit_sad", attire="darius", throne=False, expr="worried"))]
    sp = (sit_x, sit_y)
    shake = hop(t_food + 0.1, [(0, {"rot": 0}), (0.15, {"rot": 1.6}), (0.35, {"rot": -1.6}), (0.55, {"rot": 1.4}),
                               (0.75, {"rot": -1.0}), (0.95, {"rot": 0})], (sit_x, sit_y - 200 * KS))
    sc.add("king_sit", sit, frame_at=cuts([(0, 0), (t_sleep, 1)]),
           motion=M.combine(swap(t_sit, t_up), dip(t_sit, KS, sp, 9), shake, M.breathe(0.012, 3.4, pivot=sp)))

    # B: stands up, paces right (to the door side), turns, paces left to the window
    KX_UP = KX_SIT0 + 10
    pace_r = [doc(C.king(KX_UP, FLOOR, KS, 1, pose=p, attire="darius")) for p in ("stand", "pace_a", "pace_b")]
    pace_r[0] = doc(C.king(KX_UP, FLOOR, KS, 1, pose="stand", attire="darius", expr="worried"))
    kp_up = (KX_UP, FLOOR)
    sc.add("sh_kr", doc(C.ground_shadow(KX_UP, FLOOR, KS, 130, 0.3)),
           motion=M.combine(swap(t_up, t_turn), lambda t: Tf(dx=r_dx(t))))
    sc.add("king_pace_r", pace_r, frame_at=lambda t: 1 + r_fa(t) if r_fa(t) is not None else 0.0,
           motion=M.combine(swap(t_up, t_turn), lambda t: Tf(dx=r_dx(t), dy=r_dy(t)), dip(t_up, KS, kp_up, 8)))

    KX_T = KX_UP + n_r * STEP
    pace_l = [doc(C.king(KX_T, FLOOR, KS, -1, pose=p, attire="darius")) for p in ("pace_a", "pace_b")]
    pace_l += [doc(C.king(KX_T, FLOOR, KS, -1, pose="stand", attire="darius", expr="worried"))]
    pace_l += [doc(C.king(KX_T, FLOOR, KS, -1, pose="sad", attire="darius"))]
    kp_t = (KX_T, FLOOR)

    def pl_frame(t):
        f = l_fa(t)
        if f is not None:
            return f
        if t < t_turn + 0.25:
            return 2.0
        return cuts([(0, 2), (t_sad, 3), (t_look2, 2)])(t)
    sigh = hop(t_sad - 0.45, [(0, {"sy": 1.0}), (0.35, {"sy": 1.025}), (0.9, {"sy": 0.975}), (1.5, {"sy": 1.0})],
               (KX_T, FLOOR))

    def pl_move(t):
        return Tf(dx=-l_dx(t), dy=l_dy(t))
    sc.add("sh_kl", doc(C.ground_shadow(KX_T, FLOOR, KS, 130, 0.3)),
           motion=M.combine(swap(t_turn, 1e9), lambda t: Tf(dx=-l_dx(t))))
    sc.add("king_pace_l", pace_l, frame_at=pl_frame,
           motion=M.combine(swap(t_turn, 1e9), pl_move,
                            M.with_pivot(lambda t: Tf(), kp_t),
                            dip(t_turn, KS, kp_t, 7), dip(t_look, KS, kp_t, 5), dip(t_sad, KS, kp_t, 6),
                            dip(t_look2, KS, kp_t, 5),
                            lambda t: Tf(dx=0) if t < t_sad - 0.5 else M.with_pivot(sigh, (KX_WIN, FLOOR))(t),
                            M.breathe(0.01, 3.0, pivot=(KX_WIN, FLOOR))))

    # the sigh: a little breath curl from his mouth, drifting and fading
    head = C.body_points(C.king, KX_WIN, FLOOR, KS, -1, pose="sad", attire="darius")["head"]
    bx, by = head[0] - 70, head[1] + 10
    curl = (f'<path d="M{bx + 6},{by + 4} q-18,-4 -30,-12" fill="none" stroke="{P["foam"]}" stroke-width="6" '
            f'stroke-linecap="round" opacity="0.85"/>'
            + S.g(S.cloud(bx - 62, by - 16, 70, 34, fill=P["foam"], seed=3, puffs=3, sw=2.5), opacity=0.9))
    sc.add("sigh", doc(curl), wc=0, motion=M.keys(
        [(t_sad + 0.15, {"alpha": 0, "dx": 0, "dy": 0, "s": 0.6}), (t_sad + 0.45, {"alpha": 0.9, "s": 1.0}),
         (t_sad + 1.6, {"alpha": 0, "dx": -60, "dy": -40, "s": 1.25})], ["out", "sine"], pivot=(bx, by)))

    # ---------------------------------------------------------------- thought bubble
    hd = C.body_points(C.king, KX_WIN, FLOOR, KS, -1, pose="stand", attire="darius")["head"]
    BX, BY, BR = KX_WIN + 360, 360, 175
    trail = [(hd[0] + 80, hd[1] - 110, 14), (hd[0] + 140, hd[1] - 175, 22), (hd[0] + 205, hd[1] - 250, 32)]
    for i, (px_, py_, r) in enumerate(trail):
        puff = S.g(f'<circle cx="{f1(px_)}" cy="{f1(py_)}" r="{r}" fill="{P["foam"]}" {S.STROKE}/>', filter="wobble-fine")
        ti = t_think + 0.12 + 0.18 * i
        sc.add(f"puff{i}", doc(puff), wc=0.3, motion=M.keys(
            [(ti, {"alpha": 0, "s": 0.3}), (ti + 0.12, {"alpha": 1}), (ti + 0.35, {"s": 1.0})], ["sine", "back"],
            pivot=(px_, py_)))
    bub, bdefs = bubble_svg(BX, BY, BR, trail)
    tb = t_think + 0.68
    sc.add("bubble", doc(bub, bdefs), wc=0.5, motion=M.combine(
        M.keys([(tb, {"alpha": 0, "s": 0.25}), (tb + 0.15, {"alpha": 1}), (tb + 0.5, {"s": 1.0})], ["sine", "back"],
               pivot=(BX - 120, BY + 120)),
        M.bob(4, 3.2)))
    q = S.text(BX + BR + 60, BY - 40, "?", size=150, fill="#f2e2b8", extra=f'stroke="{INK}" stroke-width="5" paint-order="stroke"')
    sc.add("question", doc(q), wc=0, motion=M.combine(
        M.keys([(t_what, {"alpha": 0, "s": 0.4, "rot": -12}), (t_what + 0.15, {"alpha": 1}),
                (t_what + 0.45, {"s": 1.0, "rot": 0})], ["sine", "back"], pivot=(BX + BR + 60, BY - 80)),
        lambda t: Tf(rot=4 * math.sin(2 * math.pi * t / 1.8), px=BX + BR + 60, py=BY - 80) if t > t_what + 0.5 else Tf()))

    # ---------------------------------------------------------------- the door and archway frames (over people)
    sc.add("door_front", door_front_svg(), seed=19)

    # ---------------------------------------------------------------- light
    x0, x1, top, sill = WIN
    beam = (f'<path d="M{x0},{sill + 40} L{x1},{sill + 40} L{x1 + 260},{H + 20} L{x0 + 120},{H + 20} Z" fill="url(#s9beam)" '
            f'filter="url(#blur-md)"/>'
            f'<path d="M{x0 + 30},{top + 120} L{x1 - 30},{top + 120} L{x1 + 260},{H} L{x0 + 160},{H} Z" '
            f'fill="url(#s9beam2)" filter="url(#blur-lg)"/>')
    bdefs2 = (S.lin_grad("s9beam", [(0, "#2a3448", 1), (1, "#1a2030", 0.3)]) +
              S.lin_grad("s9beam2", [(0, "#1e2638", 0.9), (1, "#141a26", 0)]))
    sc.add("moonbeam", doc(beam, bdefs2), wc=0, blend="add", motion=M.pulse(0.9, 1.0, 5.0))
    glow_defs = S.rad_grad("s9lg", [(0, "#6a4418", 1), (0.35, "#4a2c10", 0.6), (1, "#000000", 0)])
    for i, (x, y) in enumerate(LAMPS):
        lx_, ly_ = x + 24, y - 340
        sc.add(f"lamp_glow{i}", doc(f'<circle cx="{lx_}" cy="{ly_}" r="380" fill="url(#s9lg)"/>', glow_defs), wc=0,
               blend="add", motion=M.combine(M.pulse(0.78, 1.0, 0.8 + 0.13 * i, 0.3 * i),
                                             M.keys([(0, {"alpha": 1.0}), (T, {"alpha": 0.7})], "linear"),
                                             M.breathe(0.04, 1.1, pivot=(lx_, ly_), phase=0.5 * i)))

    # ---------------------------------------------------------------- camera
    start = Cam(1250, 645, 1720)
    room = Cam(1150, 640, 1800)
    near = Cam(900, 610, 1560)
    end = Cam(880, 604, 1500)
    sc.camera = M.cam_keys([(0, start), (t_food, start), (t_music + 0.6, room), (t_turn + 0.3, room),
                            (t_look + 1.0, near), (T, end)], "sine")

    sc.fx = [lut_tint((196, 196, 232), lambda t: 0.16, mode="multiply"),
             FX.sparkles((WIN[0] + 30, WIN[2] + 40, WIN[1] - 30, WIN[2] + 220), count=8, color=(255, 246, 214),
                         size=(4, 7), period=2.4, drift=0, seed=5)]

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=T + 0.1, gain_db=-15, fade_in=0.8, fade_out=0.9)
    sc.sfx("fire", 0, dur=T + 0.1, gain_db=-24, fade_in=0.8, fade_out=0.9)
    sc.sfx("footsteps", 0.45, dur=k_arr - 0.45, gain_db=-16, fade_in=0.4, fade_out=0.3, pan=0.3)
    sc.sfx("cloth", t_sit - 0.05, gain_db=-15)
    sc.sfx("cloth", t_bow, gain_db=-20, pan=-0.4)
    sc.sfx("footsteps", m_go, dur=m_end - m_go, gain_db=-21, fade_out=0.4, pan=-0.6)
    sc.sfx("cloth", t_up - 0.05, gain_db=-17)
    sc.sfx("footsteps", snap(t_up + 0.35), dur=l_end - t_up - 0.35, gain_db=-19, fade_in=0.2, fade_out=0.3)
    sc.sfx("wind_soft", t_sigh - 0.1, dur=1.6, gain_db=-17, fade_in=0.3, fade_out=0.8)
    sc.sfx("sparkle", tb, gain_db=-16)
    sc.sfx("pop", t_what, gain_db=-17)
    return sc
