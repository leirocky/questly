"""Scene 9 - Luke 2:15-20. The shepherds visit the baby. Six shots, never cross-dissolved (nobody shows twice): a
page-turn dip through the paper colour (0.9 s) from the fields to the hillside path and (0.84 s) from the night stable
to the morning street, hard cuts on phrase boundaries elsewhere (the page dips into the scene from s08 and out of it
to s10):

  A  the fields (s07/s08's stage): the host rises back into heaven, the opening in the sky closes, the glory fades
     and the night is quiet again; the shepherds look at each other; the boy cheers 'let's go!' and points at the town
  B  a hillside path at night with Bethlehem on its hill: the shepherds run down toward the town (planted run strides),
     the lamb trotting at the boy's heels
  C  a Bethlehem street at night, the doorways dark: two shepherds peek into doorways ('找啊找'); at the end of the
     street the little cave-stable glows warm with the family inside - the boy points: '找到了！'
  D  the cave-stable (props.stable, as in s05 / s06): Joseph, Mary and the baby in the manger, the ox and the donkey;
     the shepherds come in and kneel; the boy offers his lamb and lays it by the manger; '他就是…救主' a soft warm
     glow round the baby (no halo)
  E  the same street in the morning: the shepherds cheer and tell everyone they meet; more people come to listen;
     '都很惊讶' surprised faces
  F  morning in the stable: close on Mary on a hay bale holding the sleeping baby, thoughtful; a soft memory bubble
     near her shows the angel, then the angel over the kneeling shepherds ('记在心里，想了又想'); calm last frame

Beats (syllable onsets measured in the voice clip, see s07_shepherds.Tm; nothing hard-coded to the take):
  '回天上'      A: the host rises and fades, heaven closes, the angel goes up too (whoosh, chime)
  '你看看我'    A: the man with the beard and the young shepherd turn to their neighbours; '我看看你' the others look
               back; '说' everyone stands up
  line 2 (S)   A: the boy cheers (hop) and on '伯利恒' points up at the town on the far hill; the others cheer and
               turn toward it
  '急急忙忙'    B: they run (footsteps)
  '找'  '找'    C: the young one, then the bearded one, peek into dark doorways ('?')
  '找到了'      C: the boy points at the warm little stable at the end of the street ('!', a bleat; everyone turns)
  '约瑟和马利亚' D: the shepherds come in; Joseph welcomes them, Mary looks up; they kneel
  '马槽'        D: the camera moves in to the manger; the boy offers the lamb and lays it down by the manger
  '救主'        D: a soft warm glow round the baby, a twinkle
  '好开心'      E: the shepherds cheer (hops); '见到人就说' they tell (arms wide); '天使' two point up at the sky;
               more people walk up to listen
  '惊讶'        E: the listeners start, '!' marks
  '马利亚呢'    F: Mary with the baby, thoughtful; '这些事' the memory bubble opens with the angel; '记在心里' the
               kneeling shepherds fade in below the same angel; '想了又想' the bubble swells softly twice; it fades,
               Mary closes her eyes peacefully: calm hold (page dip to s10)
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes import s08_choir as S8
from stories.nativity.scenes.s07_shepherds import (ANGEL, ANGEL_LOOP, DOG0, H7, HUDDLE, K, LIFT, SEED, SHEEP_IN,
                                                    SHEEP_OUT, SHEP, SK, STURDY_REST, TOWN, W7, YOUNG_WATCH, Fig, Tm,
                                                    add_crook, add_fields, angel_bob, angel_draw, blink, breath,
                                                    cam_path, doc7, dog_draw, env, f1, gsparkles, hop, pop_motion,
                                                    rot_about, sheep_in_draw, sheep_markup, sheep_out_draw, shep_draw,
                                                    squash, zorder)
from stories.noah.scenes.s01_title import snap

INK = P["ink"]
R = H7 - 1188                       # top of the 2112 x 1188 region where shots B-F are painted (stage y)
FULL = Cam(1056, R + 594, 2112)

# ---- shot B: the hillside path down to the town (runners go right -> left, toward the town as in shot A)
KB = 0.74


def path_y(x):
    return R + 800 + (2112 - x) * 0.08


# ---- shots C / E: the street (bethlehem_town part='street', seed 4, x0 = -100): the doorways' x spans
DOORS = [(432, 542), (771, 881), (1093, 1203), (1504, 1614), (1908, 2018)]
STREET_Y = R + 720                  # bethlehem_town y (doors stand on STREET_Y - 30)
KC = 0.95
CAVE = (150, R + 700)               # the little stable at the left end of the street (doorway floor)
CAVE_K = 0.45

# ---- shot D: the cave-stable
KD = 0.92
SD = (1000, R + 940)
SP = PR.stable_points(*SD, KD)
KNEEL_D = {"old": (1300, R + 958), "beard": (1430, R + 1030), "young": (1570, R + 1046), "sturdy": (1710, R + 1028),
           "boy": (1178, R + 996)}
OUTSIDE_D = ("beard", "young", "sturdy")      # these kneel at the threshold, in front of the stable's front part

# ---- shot F: morning in the stable, close on Mary
SF_K = 2.3
MARY_F = (760, R + 985)
SF = (MARY_F[0] + 150 * SF_K, MARY_F[1] + 10 * SF_K)

SHOTS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}


def shep_s(key, pose, expr, facing, x, y, s, crook=False, lamb=True, marks=True, shadow=True):
    v = SHEP[key][0]
    sh = ""
    if shadow:
        wid = {"sit": 210, "kneel": 170}.get(pose, 130) * (0.75 if v == 2 else 1.0)
        sh = C.ground_shadow(x, y, s, wid, 0.2)
    return sh + C.shepherds(x, y, s, facing, variant=v, pose=pose, expr=expr, crook=crook, lamb=lamb, marks=marks)


def shep_draw_s(key, s, spots):
    """Fig drawing: state 'pose|expr|facing|spot|flags' at scale s (spots: name -> (x, y))."""
    def d(n):
        pose, expr, f, where, flags = n.split("|")
        x, y = spots[where]
        return shep_s(key, pose, expr, int(f), x, y, s, crook="c" in flags, marks="m" in flags)
    return d


def mark_svg(x, y, ch, size=64, col="#fff4d6"):
    return doc7(S.text(x, y, ch, size=size, fill=col, weight="bold",
                       extra=f'stroke="{INK}" stroke-width="5" paint-order="stroke"'))


def warm_glow_svg(cx, cy, rx, ry, a=0.9, col="#ffe2a0", gid="wg"):
    defs = S.rad_grad(gid, [(0, col, a), (0.5, col, a * 0.4), (1, col, 0)])
    return doc7(f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>', defs)


def stride_track(t0, x0, step, frames, n, lift, s):
    """Run / trot track at 30 fps: a flip every ``frames`` frames (the flips sit in the middle of a frame interval);
    the anchor holds still while a foot is planted and covers ``step`` px (signed) in the two frames round each
    flip (the flight, with a bounce). Returns (x(t), bounce(t), flip times)."""
    per = frames / 30.0
    flips = [snap(t0 + k * per) for k in range(n)]
    w = 1 / 30.0

    def x(t):
        v = x0
        for tk in flips:
            v += step * min(1.0, max(0.0, (t - (tk - w)) / (2 * w)))
        return v

    def b(t):
        for tk in flips:
            if tk - w <= t <= tk + w:
                return lift * s * math.sin(math.pi * (t - tk + w) / (2 * w))
        return 0.0
    return x, b, flips


# ================================================================== shot backdrops
def run_bg_svg():
    """Shot B: the starry sky, Bethlehem on its hill (left), the valley, the hillside path the shepherds run down."""
    b = PR.starry_sky(-10, R - 10, W7 + 10, R + 860, density=1.1, time="night", seed=13)
    b += PR.bethlehem_town(-300, 1320, R + 690, 0.84, time="night", part="back", seed=2)
    far = PR._nt("#6f7f62", "night", 1.25)
    mid = PR._nt("#5f7a4e", "night", 1.1)
    near = PR._nt("#5e7d48", "night")
    b += S.path(S.hill(-200, W7 + 200, R + 760, 70, seed=21, bottom=R + 1260, bumps=4), fill=far, sw=3)
    b += S.path(S.hill(-200, W7 + 200, R + 860, 60, seed=22, bottom=R + 1260, bumps=3), fill=mid, sw=3)
    for x, y, s in ((1380, R + 720, 0.34), (1620, R + 706, 0.3), (1880, R + 716, 0.32), (300, R + 760, 0.3)):
        b += PR._haze(PR.olive_tree(x, y, s, seed=int(x)), PR._nt("#556a44", "night"), 0.3, 0.3)
    # the near hillside: high on the right, sloping down to the left
    pts = [(-200, R + 1060), (300, R + 1010), (900, R + 950), (1500, R + 880), (2000, R + 830), (2320, R + 810)]
    d = S.smooth_path(pts, closed=False) + f" L2320,{R + 1260} L-200,{R + 1260} Z"
    gid = "s9near"
    defs = S.lin_grad(gid, [(0, near), (1, S.shade(near, -0.3))])
    b += f'<path d="{d}" fill="url(#{gid})" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
    # the path: a pale dusty band along the slope
    top = [(x, path_y(x) - 26 - 6 * math.sin(x / 170)) for x in range(-200, 2400, 100)]
    bot = [(x, path_y(x) + 34 + 5 * math.sin(x / 140)) for x in range(2300, -300, -100)]
    pd = S.smooth_path(top, closed=False) + " L" + " L".join(f"{f1(a)},{f1(c)}" for a, c in bot) + " Z"
    b += f'<path d="{pd}" fill="{PR._nt("#c9ad80", "night", 1.1)}" stroke="{INK}" stroke-width="2.6" opacity="0.92"/>'
    rng = random.Random(3)
    for _ in range(46):
        x = rng.uniform(-50, W7 + 50)
        y = rng.uniform(path_y(x) + 60, R + 1180)
        if y < R + 760:
            continue
        b += (f'<path d="M{f1(x - 8)},{f1(y)} l5,-18 l5,14 l5,-20 l5,16" fill="none" stroke="#3f5a30" '
              f'stroke-width="2.6" stroke-linecap="round"/>')
    for x, y, rx in ((520, R + 1130, 60), (1720, R + 1050, 48), (2020, R + 1150, 70)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.5}" fill="{PR._nt("#8a8478", "night")}" ' \
             f'stroke="{INK}" stroke-width="3"/>'
    return doc7(S.g(b, filter="wobble"), defs)


def street_bg_svg(time):
    """Shots C / E: the same street at night (dark doorways) and in the morning."""
    sky_t = "night" if time == "night" else "dawn"
    b = PR.starry_sky(-10, R - 10, W7 + 10, R + 720, density=1.0 if time == "night" else 0.6, time=sky_t, seed=17)
    b += PR.bethlehem_town(-100, 2200, R + 380, 0.75, time=time, part="back", seed=2,
                           lit=0.35 if time == "night" else None)
    b += PR.bethlehem_town(-100, 2200, STREET_Y, 1.0, time=time, part="street", seed=4,
                           lit=0.1 if time == "night" else None)
    b += (f'<rect x="-20" y="{R + 1070}" width="{W7 + 40}" height="160" '
          f'fill="{PR._nt("#a88a62", time)}"/>')
    if time == "night":            # the little stable at the end of the street, with the family inside
        cp = PR.stable_points(*CAVE, CAVE_K)
        b += PR.stable(*CAVE, CAVE_K, part="back", time="night", lamp=1.0)
        b += PR.donkey(*cp["donkey"], CAVE_K * 0.88, 1, pose="lie_look", sacks=0)
        b += C.joseph_carpenter(*cp["joseph"], CAVE_K, 1, pose="watch")
        b += C.mary(*cp["mary"], CAVE_K, 1, pose="kneel")
        b += C.baby_jesus(*cp["bed"], CAVE_K, 1, state="in_manger")
        b += PR.manger(*cp["manger"], CAVE_K, 1, part="front", time="day")
        b += PR.stable(*CAVE, CAVE_K, part="front", time="night", lamp=1.0)
    return doc7(b)


def stable_bg_svg():
    """Shot D: sky, ground and the back of the cave-stable (with its manger)."""
    b = PR.starry_sky(-10, R - 10, W7 + 10, R + 1100, density=1.1, time="night", seed=19)
    near = PR._nt("#5e7d48", "night")
    b += S.path(S.hill(-200, W7 + 200, R + 900, 40, seed=31, bottom=R + 1260, bumps=3), fill=near, sw=3.4)
    b += PR.stable(*SD, KD, part="back", time="night")
    return doc7(b)


def stable_f_svg():
    """Shot F: the stable close up in the morning (back part, with the empty manger) and Mary's hay bale."""
    b = PR.starry_sky(-10, R - 10, W7 + 10, R + 1188, density=0.0, time="dawn", seed=19)
    b += PR.stable(*SF, SF_K, part="back", time="dawn", lamp=0.55)
    return doc7(b)


# ================================================================== the scene
def build(ctx):
    sc = Scene(ctx, W=W7, H=H7)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    rng = random.Random(9)

    # ---- beats
    t_hui = tm.at(0, "回天上")
    t_kan1 = tm.at(0, "看看")
    t_kan2 = tm.at(0, "我看看你", 1)
    t_shuo = tm.at(0, "说")
    t_s0 = ctx.lines[1].start
    t_kuai = tm.at(1, "快去")
    t_blh = tm.at(1, "伯利恒")
    t_kkb = tm.at(1, "看看吧")
    t_run = tm.at(2, "急急忙忙")
    t_pao = tm.at(2, "跑到")
    t_blh2 = tm.at(2, "伯利恒")
    t_zhao1 = tm.at(2, "找啊找")
    t_zhao2 = tm.at(2, "找啊找", 2)
    t_found = tm.at(2, "找到了")
    t_ym = tm.at(2, "约瑟")
    t_dou = tm.at(2, "都在那里")
    t_xyh = tm.at(2, "小婴孩")
    t_tang = tm.at(2, "躺在")
    t_mc = tm.at(2, "马槽")
    t_ta = tm.at(3, "他就是")
    t_jz = tm.at(3, "救主")
    t_pai = tm.at(3, "上帝派来")
    t_kx = tm.at(4, "好开心")
    t_jian = tm.at(4, "见到人")
    t_ts = tm.at(4, "天使")
    t_gs = tm.at(4, "告诉")
    t_tj = tm.at(5, "听见")
    t_jy = tm.at(5, "都很惊讶")
    t_mly = tm.at(5, "马利亚呢")
    t_zx = tm.at(5, "这些事")
    t_jx = tm.at(5, "记在心里")
    t_xx1 = tm.at(5, "想了又想")
    t_xx2 = tm.at(5, "想了又想", 3)

    # ---- shot changes: no cross-dissolves (people must never show twice). A paper dip (a page turn, 0.9 / 0.84 s)
    # where there is a pause between lines (fields -> path, night stable -> morning street), hard cuts on the
    # phrase boundaries elsewhere. Cut times sit in the middle of a frame interval.
    DIP_AB, DIP_DE = 0.45, 0.42
    c_AB = snap(0.5 * (ctx.lines[1].end + ctx.lines[2].start))
    c_BC = snap(0.5 * (tm.end(2, "伯利恒") + t_zhao1))
    c_CD = snap(0.5 * (tm.end(2, "找到了") + t_ym))
    c_DE = snap(0.5 * (ctx.lines[3].end + ctx.lines[4].start))
    c_EF = snap(0.5 * (tm.end(5, "都很惊讶") + t_mly))
    order = ["A", "B", "C", "D", "E", "F"]
    starts = {"A": -1e9, "B": c_AB, "C": c_BC, "D": c_CD, "E": c_DE, "F": c_EF}

    def shot_alpha(name):
        i = order.index(name)
        t0 = starts[name]
        t1 = starts[order[i + 1]] if i + 1 < len(order) else 1e9
        return lambda t: 1.0 if t0 <= t < t1 else 0.0

    def zb(name):
        return 100 * order.index(name)

    def shot_m(name):
        al = shot_alpha(name)
        return lambda t: Tf(alpha=al(t))

    # ================================================================ A: the fields
    aA = shot_alpha("A")
    t_close0, t_close1 = t_hui - 0.2, t_hui + 1.4
    close_k = lambda t: M.progress(t, t_close0, t_close1, "inout")
    glory_k = lambda t: (1 - 0.22) * (1 - M.progress(t, t_hui + 0.3, t_hui + 1.7, "inout"))
    field_k = lambda t: (1 - 0.3) * (1 - M.progress(t, t_hui + 0.3, t_hui + 1.9, "inout"))
    add_fields(sc, g0, glory_on=glory_k, field_on=field_k, on=aA)

    # the heaven light closes, the host rises away
    def heaven_fa(t):
        v = 0.12 + 0.88 * (1 - close_k(t))
        P_ = S8.HEAVEN_P
        for i in range(len(P_) - 1):
            if P_[i] <= v <= P_[i + 1]:
                return i + (v - P_[i]) / (P_[i + 1] - P_[i])
        return len(P_) - 1.0
    sc.add("heaven", [S8.heaven_svg(p) for p in S8.HEAVEN_P], z=0.7, wc=0.5, frame_at=heaven_fa,
           motion=lambda t: Tf(alpha=min(1.0, (1 - close_k(t)) * 4) * aA(t)))
    for gi in range(3):
        x0, x1, y, n, s, rows, seed = S8.GROUPS[gi]
        cx, cy = (x0 + x1) / 2, y - 120
        tr = t_hui - 0.5 + 0.2 * (2 - gi)
        per = 3.0 + 0.4 * gi

        def m(t, tr=tr, per=per, gi=gi):
            u = M.progress(t, tr, tr + 1.4, "in")
            return Tf(dy=-560 * u + 7 * math.sin(2 * math.pi * ((t + g0) / per + 0.3 * gi)),
                      alpha=(1 - M.progress(t, tr + 0.5, tr + 1.4, "sine")) * aA(t))
        sc.add(f"choir{gi}", [S8.choir_svg(gi, k) for k in range(S8.CHOIR_PH)], z=0.8 + 0.01 * gi, wc=0.8,
               seed=150 + gi, frame_at=lambda t, gi=gi: float(int((t + g0) / 0.2 + 2 * gi) % S8.CHOIR_PH), motion=m)
        sc.fx.append(gsparkles((x0, y - 500, x1, y), g0, t0=tr + 0.2, t1=tr + 1.8, count=12, color=(255, 244, 200),
                               size=(8, 15), period=1.0, drift=-60, seed=80 + gi))
    ax, ay = ANGEL
    an = Fig("angel", angel_draw, (ax, ay - LIFT), K, zorder(ay) + 0.001, g0, seed=SEED["angel"],
             loops={"sing|sing": ANGEL_LOOP, "float|": ANGEL_LOOP})
    an.cut(0, "sing|sing")
    an.cut(t_hui - 0.65, "float|", depth=4)
    t_up0 = t_hui - 0.4
    an.mots += [angel_bob(g0), lambda t: Tf(dy=-60 - 620 * M.progress(t, t_up0, t_up0 + 1.6, "in"),
                                           alpha=(1 - M.progress(t, t_up0 + 0.7, t_up0 + 1.6, "sine")) * aA(t))]
    an.build(sc)
    sc.add("angel_shadow", doc7(C.ground_shadow(ax, ay, K, 170, 0.25, color="#fff3c0")), z=zorder(ay) - 0.01, wc=0,
           motion=lambda t: Tf(alpha=0.6 * (1 - M.progress(t, t_up0, t_up0 + 0.8, "sine")) * aA(t)))
    sc.fx.append(gsparkles((ax - 160, ay - 900, ax + 160, ay - 200), g0, t0=t_up0 + 0.2, t1=t_up0 + 2.0, count=10,
                           color=(255, 244, 200), size=(8, 14), period=0.9, drift=-90, seed=84))

    # the flock settles down again, the dog sits
    for i, (x, y, f, v, pose) in enumerate(SHEEP_IN):
        a = Fig(f"sheep_in{i}", sheep_in_draw(i), (x, y), SK, 4 + y / 10000, g0, seed=80 + i)
        a.cut(0, "look_up")
        a.cut(t_hui + 1.6 + 0.4 * i, "lie", depth=5)
        a.cut(t_kkb + 0.3 * i, "sleep" if i != 1 else "lie", depth=3)
        a.mots.append(breath((x, y), g0, 2.6 + 0.3 * i, 0.02, 0.3 * i))
        a.build(sc, extra_motion=shot_m("A"))
    for i, (x, y, f, v, pose) in enumerate(SHEEP_OUT):
        hx, hy = HUDDLE[i]
        a = Fig(f"sheep_out{i}", sheep_out_draw(i), (x, y), SK, zorder(max(y, hy)), g0, seed=90 + i)
        a.cut(0, "look_up|h|1" if i in (1, 3) else "look_up|h|-1")
        a.cut(t_hui + 1.9 + 0.35 * i, f"lie|h|{-1 if i % 2 else 1}", depth=5)
        a.mots.append(breath((x, y), g0, 2.4 + 0.2 * i, 0.02, 0.5 * i))
        a.build(sc, extra_motion=shot_m("A"))
    dg = Fig("dog", dog_draw, DOG0, SK, zorder(DOG0[1]), g0, seed=SEED["dog"])
    dg.cut(0, "look_up|open")
    dg.cut(t_hui + 1.5, "sit|open", depth=4)
    dg.cut(t_s0 + 0.4, "stand|open", depth=4)
    dg.mots.append(breath(DOG0, g0, 2.2, 0.02))
    dg.build(sc, extra_motion=shot_m("A"))

    # the shepherds: kneeling, look at each other, stand up, cheer and turn toward the town
    def figA(key, piv):
        return Fig(key, shep_draw(key), piv, K, zorder(piv[1] if key != "young" else YOUNG_WATCH[1] + 12), g0,
                   seed=SEED[key])
    old = figA("old", SHEP["old"][1:])
    old.cut(0, "kneel|awed|1|a|")
    old.cut(t_kan2 + 0.05, "kneel|happy|1|a|", depth=5)
    old.cut(t_shuo + 0.45, "stand|joyful|1|a|", depth=8)
    old.cut(t_kuai + 0.3, "cheer|joyful|1|a|", depth=6)
    old.cut(t_kkb + 0.1, "stand|happy|-1|a|", depth=5)
    beard = figA("beard", SHEP["beard"][1:])
    beard.cut(0, "kneel|awed|1|a|")
    beard.cut(t_kan1, "kneel|amazed|-1|a|", depth=5)
    beard.cut(t_shuo + 0.3, "stand|joyful|-1|a|", depth=8)
    beard.cut(t_kuai + 0.05, "cheer|joyful|-1|a|", depth=7)
    beard.cut(t_kkb - 0.1, "stand|happy|-1|a|", depth=5)
    young = figA("young", YOUNG_WATCH)
    young.cut(0, "kneel|awed|1|w|")
    young.cut(t_kan1 + 0.06, "kneel|amazed|-1|w|", depth=5)
    t_yup = t_shuo + 0.15
    young.cut(t_yup, "stand|joyful|-1|w|c", depth=8)
    young.cut(t_blh + 0.2, "stand|happy|-1|w|c", dip=False)
    sturdy = figA("sturdy", STURDY_REST)
    sturdy.cut(0, "kneel|awed|1|r|")
    sturdy.cut(t_kan2 + 0.12, "kneel|happy|1|r|", depth=5)
    sturdy.cut(t_shuo + 0.6, "stand|joyful|1|r|", depth=8)
    sturdy.cut(t_kuai + 0.2, "cheer|joyful|1|r|", depth=6)
    sturdy.cut(t_kkb + 0.05, "stand|happy|-1|r|", depth=5)
    xb, yb = SHEP["boy"][1:]
    boy = figA("boy", (xb, yb))
    boy.cut(0, "look_up|happy|1|a|")
    boy.cut(t_kan2 + 0.25, "stand|amazed|-1|a|", depth=5)
    t_cheer = t_s0 + 0.02
    boy.cut(t_cheer, "cheer|joyful|-1|a|", depth=7)
    boy.cut(t_blh, "point_up|joyful|-1|a|", depth=6)
    boy.mots.append(hop(t_cheer + 0.12, K, (xb, yb), 30, 0.34))
    boy.mots.append(hop(t_kkb + 0.05, K, (xb, yb), 18, 0.3))
    for f_, k_ in ((old, 0.1), (beard, 0.4), (young, 0.2), (sturdy, 0.6), (boy, 0.7)):
        f_.mots.append(breath(f_.piv, g0, 3.0 + 0.2 * k_, 0.012, k_))
        f_.build(sc, extra_motion=shot_m("A"))
    sc.add("lamb_up", doc7(sheep_markup(xb + 70, yb + 12, -1, 3, "look_up", lamb=True)), z=zorder(yb + 12),
           seed=SEED["lamb"], motion=M.combine(breath((xb + 70, yb + 12), g0, 2.0, 0.025), shot_m("A")))
    add_crook(sc, motion=lambda t: Tf(alpha=(1.0 if t < snap(t_yup) else 0.0) * aA(t)))
    sc.fx.append(gsparkles((TOWN[0] - 220, TOWN[1] - 170, TOWN[0] + 220, TOWN[1] - 30), g0, t0=t_blh - 0.1,
                           t1=c_AB - DIP_AB, count=10, color=(255, 230, 160), size=(7, 13), period=1.3, drift=-6,
                           seed=86))
    sc.add("town_call", doc7(f'<defs>{S.rad_grad("tcl", [(0, "#ffe2a0", 0.9), (1, "#ffe2a0", 0)])}</defs>'
                             f'<ellipse cx="{f1(TOWN[0])}" cy="{f1(TOWN[1] - 70)}" rx="300" ry="140" fill="url(#tcl)"/>'),
           z=1.08, wc=0, blend="screen", motion=lambda t: Tf(alpha=env(t, t_blh - 0.2, c_AB, 0.5, 0.4)))

    # ================================================================ B: running down the hillside to the town
    zB = zb("B")
    sc.add("run_bg", run_bg_svg(), z=zB, motion=shot_m("B"))
    runners = [("boy", 0.0, 2140, 4, -70, 20), ("young", 0.12, 2290, 5, -88, 24),
               ("beard", 0.2, 2420, 5, -88, 24), ("sturdy", 0.3, 2560, 5, -88, 24),
               ("old", 0.38, 2700, 5, -82, 18)]
    tB0 = c_AB - DIP_AB                          # they set off under the page turn
    tB_end = c_BC
    for key, dt, x0, per, step, lift in runners:
        n = int((tB_end - tB0 - dt) / (per / 30.0)) + 1
        xf, bf, flips = stride_track(tB0 + dt, x0, step, per, n, lift, KB)
        xr = 1056                                 # drawn here (inside the stage), moved by the motion
        yr = path_y(xr)
        frames = [doc7(shep_s(key, p, "joyful", -1, xr, yr, KB, marks=True)) for p in ("run_a", "run_b")]

        def fa(t, flips=flips):
            k = sum(1 for tk in flips if t >= tk)
            return float(k % 2)

        def mot(t, xf=xf, bf=bf, xr=xr, yr=yr):
            x = xf(t)
            return Tf(dx=x - xr, dy=path_y(x) - yr - bf(t), alpha=shot_alpha("B")(t))
        sc.add(f"run_{key}", frames, frame_at=fa, z=zB + 10 + (6 - runners.index((key, dt, x0, per, step, lift))) * 0.01,
               seed=SEED[key], motion=mot)
    # the lamb trots at the boy's heels
    lxf, lbf, lflips = stride_track(tB0 + 0.04, 2140 + 110, -35, 2, int((tB_end - tB0) * 15) + 1, 9, SK)
    lxr = 1056
    lamb_fr = [doc7(sheep_markup(lxr, path_y(lxr) + 10, -1, 3, p, lamb=True)) for p in ("walk_a", "walk_b")]
    sc.add("run_lamb", lamb_fr, frame_at=lambda t: float(sum(1 for tk in lflips if t >= tk) % 2), z=zB + 10.1,
           seed=SEED["lamb"], motion=lambda t: Tf(dx=lxf(t) - lxr, dy=path_y(lxf(t)) - path_y(lxr) - lbf(t),
                                                   alpha=shot_alpha("B")(t)))

    # ================================================================ C: the street at night, the dark doorways
    zC = zb("C")
    sc.add("street_night", street_bg_svg("night"), z=zC, motion=shot_m("C"))
    sc.add("cave_glow", warm_glow_svg(CAVE[0] + 20, CAVE[1] - 130, 360, 230, 0.7, gid="cvg"), z=zC + 1, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=shot_alpha("C")(t) * (0.75 + 0.15 * math.sin(
               2 * math.pi * (t + g0) / 1.7) + 0.25 * env(t, t_found - 0.1, t_found + 1.5, 0.3, 0.6))))
    spots_c = {"y": (1262, R + 846), "b": (1676, R + 838), "o": (880, R + 900), "s": (1470, R + 920),
               "k": (600, R + 930)}
    cfigs = {}
    for key, spot in (("young", "y"), ("beard", "b"), ("old", "o"), ("sturdy", "s"), ("boy", "k")):
        cfigs[key] = Fig(f"c_{key}", shep_draw_s(key, KC, spots_c), spots_c[spot], KC, zC + 10 + spots_c[spot][1] / 1000,
                         g0, seed=SEED[key])
    yc, bc, oc, stc, kc = (cfigs[k] for k in ("young", "beard", "old", "sturdy", "boy"))
    yc.cut(0, "stand|happy|-1|y|c")
    yc.cut(t_zhao1 - 0.1, "stand|kind|-1|y|c", dip=False)
    yc.cut(t_found + 0.15, "stand|joyful|-1|y|c", depth=5)
    yc.mots.append(rot_about(lambda t: -9 * env(t, t_zhao1 - 0.15, t_found + 0.05, 0.25, 0.25), spots_c["y"],
                             spots_c["y"]))
    bc.cut(0, "stand|happy|-1|b|")
    bc.cut(t_zhao2 - 0.1, "stand|kind|-1|b|", dip=False)
    bc.cut(t_found + 0.25, "stand|joyful|-1|b|", depth=5)
    bc.mots.append(rot_about(lambda t: -9 * env(t, t_zhao2 - 0.15, t_found + 0.1, 0.25, 0.25), spots_c["b"],
                             spots_c["b"]))
    oc.cut(0, "stand|kind|1|o|")
    oc.cut(t_zhao2 + 0.1, "stand|kind|-1|o|", depth=4)
    oc.cut(t_found + 0.2, "stand|joyful|-1|o|", depth=5)
    stc.cut(0, "stand|kind|-1|s|")
    stc.cut(t_found + 0.3, "stand|joyful|-1|s|", depth=5)
    kc.cut(0, "stand|happy|1|k|")
    kc.cut(t_found - 0.05, "point_up|joyful|-1|k|", depth=8)
    kc.mots.append(hop(t_found + 0.1, KC, spots_c["k"], 26, 0.32))
    for i, f_ in enumerate(cfigs.values()):
        f_.mots.append(breath(f_.piv, g0, 2.8 + 0.2 * i, 0.012, 0.3 * i))
        f_.build(sc, extra_motion=shot_m("C"))
    lkx, lky = spots_c["k"][0] + 64, spots_c["k"][1] + 10
    sc.add("c_lamb", [doc7(sheep_markup(lkx, lky, -1, 3, p, lamb=True)) for p in ("stand", "bleat")], z=zC + 10.9,
           seed=SEED["lamb"], frame_at=lambda t: 1.0 if t_found + 0.2 <= t < t_found + 0.9 else 0.0,
           motion=M.combine(breath((lkx, lky), g0, 2.0, 0.025), shot_m("C")))
    for i, (tt, key) in enumerate(((t_zhao1, "y"), (t_zhao2, "b"))):
        x, y = spots_c[key]
        qx, qy = x + 30, y - 330 * KC - 30
        sc.add(f"qmark{i}", mark_svg(qx, qy, "?", 96), z=zC + 20, wc=0,
               motion=M.combine(pop_motion(tt + 0.1, (qx, qy), 0.35, t1=t_found + 0.1, out=0.25), shot_m("C")))
    ex_, ey_ = spots_c["k"][0] - 10, spots_c["k"][1] - 240 * KC - 40
    sc.add("emark_c", mark_svg(ex_, ey_, "!", 104, "#ffe08a"), z=zC + 20, wc=0,
           motion=M.combine(pop_motion(t_found + 0.05, (ex_, ey_), 0.35), shot_m("C")))

    # ================================================================ D: the stable
    zD = zb("D")
    sc.add("stable_bg", stable_bg_svg(), z=zD, motion=shot_m("D"))
    s_an = KD * 0.88
    ox_x, ox_y = SP["ox"][0] + 150, SP["ox"][1] - 52
    don = Fig("d_donkey", lambda n: PR.donkey(*SP["donkey"], s_an, 1, pose=n, sacks=0), SP["donkey"], s_an, zD + 2,
              g0, seed=301)
    don.cut(0, "lie_look")
    don.cut(t_ym + 0.4, "lie", depth=3)
    don.cut(t_mc + 0.3, "lie_look", depth=3)
    don.mots.append(breath(SP["donkey"], g0, 3.3, 0.016))
    don.build(sc, extra_motion=shot_m("D"))
    oxf = Fig("d_ox", lambda n: PR.ox(ox_x, ox_y, s_an, -1, pose=n), (ox_x, ox_y), s_an, zD + 2.1, g0, seed=302)
    oxf.cut(0, "lie_look")
    oxf.cut(t_ym + 0.6, "lie", depth=3)
    oxf.cut(t_ta + 0.2, "lie_look", depth=3)
    oxf.mots.append(breath((ox_x, ox_y), g0, 3.6, 0.016, 0.4))
    oxf.build(sc, extra_motion=shot_m("D"))
    jx, jy = SP["joseph"]
    jo = Fig("d_joseph", lambda n: C.joseph_carpenter(jx, jy, KD, 1, pose=n.split("|")[0], expr=n.split("|")[1] or None),
             (jx, jy), KD, zD + 3, g0, seed=303)
    jo.cut(0, "watch|tender")
    jo.cut(t_ym + 0.05, "talk|kind", depth=6)
    jo.cut(t_xyh + 0.3, "watch|tender", depth=5)
    jo.add_blinks({"watch|tender": f"watch|{blink('tender')}", "talk|kind": f"talk|{blink('kind')}"}, 0.3, T, rng)
    jo.mots.append(breath((jx, jy), g0, 3.2, 0.012))
    jo.build(sc, extra_motion=shot_m("D"))
    mx, my = SP["mary"]
    ma = Fig("d_mary", lambda n: C.mary(mx, my, KD, 1, pose=n.split("|")[0], expr=n.split("|")[1] or None),
             (mx, my), KD, zD + 3.1, g0, seed=304)
    ma.cut(0, "kneel|tender")
    ma.cut(t_ym + 0.5, "kneel_up|kind", depth=5)
    ma.cut(t_xyh + 0.1, "kneel|tender", depth=5)
    ma.cut(t_ta + 0.1, "kneel|joyful", dip=False)
    ma.cut(t_pai + 0.2, "kneel|tender", dip=False)
    ma.add_blinks({"kneel_up|kind": f"kneel_up|{blink('kind')}"}, 0.3, T, rng)
    ma.mots.append(breath((mx, my), g0, 3.0, 0.012, 0.3))
    ma.build(sc, extra_motion=shot_m("D"))
    bx_, by_ = SP["bed"]
    sc.add("d_baby", doc7(C.baby_jesus(bx_, by_, KD, 1, state="in_manger", hand=True)), z=zD + 4, seed=305,
           motion=M.combine(lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * (t + g0) / 2.4), px=bx_, py=by_),
                            shot_m("D")))
    sc.add("d_manger_front", doc7(PR.manger(*SP["manger"], KD, 1, part="front", time="day")), z=zD + 4.1, seed=306,
           motion=shot_m("D"))
    # the shepherds walk in from the right and kneel
    spots_d = {k: v for k, v in KNEEL_D.items()}
    for key, (kx, ky) in KNEEL_D.items():
        spots_d[key + "_w"] = (kx, ky)
    dfigs = {}
    walk_in = {"boy": (0.0, 5), "old": (0.1, 5), "beard": (0.18, 5), "young": (0.26, 5), "sturdy": (0.34, 5)}
    t_in0 = c_CD - 0.3                           # already walking in when the picture cuts to the stable
    for key, (kx, ky) in KNEEL_D.items():
        dt, nst = walk_in[key]
        stride = (62 if key != "boy" else 46) * KD
        zz = (zD + 9.2 if key in OUTSIDE_D else zD + 5) + ky / 10000
        f_ = Fig(f"d_{key}", shep_draw_s(key, KD, spots_d), (kx, ky), KD, zz, g0, seed=SEED[key])
        t0 = t_in0 + dt
        per = 0.27
        for k in range(nst):
            f_.cut(t0 + k * per, f"{'walk_a' if k % 2 == 0 else 'walk_b'}|happy|-1|{key}_w|", dip=False)
        t_arr = snap(t0 + nst * per)

        def walk_off(t, t0=t0, per=per, nst=nst, stride=stride, t_arr=t_arr):
            if t >= t_arr:
                return Tf()
            done = 0.0
            for k in range(nst):
                done += M.progress(t, t0 + k * per - 0.07, t0 + k * per + 0.08, "sine")
            return Tf(dx=stride * (nst - done), dy=-3 * KD * abs(math.sin(math.pi * (t - t0) / per)) if t > t0 else 0)
        f_.mots.append(walk_off)
        dfigs[key] = (f_, t_arr)
    # kneel at '都在那里' (staggered); the boy offers his lamb at the manger, then lays it down and kneels
    for i, key in enumerate(("old", "beard", "young", "sturdy")):
        f_, t_arr = dfigs[key]
        t_kn = max(t_arr + 0.55, t_dou + 0.15 * i)
        f_.cut(t_arr, f"stand|happy|-1|{key}|", depth=3)
        f_.cut(t_kn, f"kneel|awed|-1|{key}|", depth=8)
        f_.cut(t_ta + 0.25 + 0.15 * i, f"kneel|{'joyful' if i % 2 else 'peaceful'}|-1|{key}|", dip=False)
        f_.add_blinks({f"kneel|awed|-1|{key}|": f"kneel|{blink('awed')}|-1|{key}|",
                       f"kneel|joyful|-1|{key}|": f"kneel|{blink('joyful')}|-1|{key}|"}, t_kn + 0.4, T, rng)
        f_.mots.append(breath(KNEEL_D[key], g0, 3.0 + 0.2 * i, 0.012, 0.3 * i))
    fbo, t_arr_b = dfigs["boy"]
    fbo.cut(t_arr_b, "hold_lamb|happy|-1|boy|", depth=3)
    t_offer = t_tang - 0.1
    fbo.cut(t_offer, "hold_lamb|joyful|-1|boy|", depth=5)
    t_lay = t_mc + 0.35
    fbo.cut(t_lay, "kneel|happy|-1|boy|", depth=8)
    fbo.cut(t_ta + 0.3, "kneel|awed|-1|boy|", dip=False)
    kbx, kby = KNEEL_D["boy"]
    fbo.mots.append(lambda t: Tf(dx=-22 * env(t, t_offer - 0.1, t_lay + 0.05, 0.35, 0.2), rot=-4 * env(
        t, t_offer - 0.1, t_lay + 0.05, 0.35, 0.2), px=kbx, py=kby))
    fbo.mots.append(breath(KNEEL_D["boy"], g0, 2.6, 0.014, 0.7))
    for key, (f_, _) in dfigs.items():
        f_.build(sc, extra_motion=shot_m("D"))
    lmx, lmy = SP["manger"][0] + 118 * KD, SP["manger"][1] + 26
    sc.add("d_lamb", doc7(sheep_markup(lmx, lmy, -1, 3, "lie", lamb=True, s=KD * 0.9)), z=zD + 4.5, seed=SEED["lamb"],
           motion=M.combine(lambda t: Tf(alpha=1.0 if t >= snap(t_lay) else 0.0), breath((lmx, lmy), g0, 2.0, 0.025),
                            squash(snap(t_lay), KD, (lmx, lmy), 5), shot_m("D")))
    sc.add("stable_front", doc7(PR.stable(*SD, KD, part="front", time="night")), z=zD + 9, seed=307,
           motion=shot_m("D"))
    # the lamplight flickers; the soft glow round the baby
    lpx, lpy = SP["lamp"]
    sc.add("d_lamp", warm_glow_svg(lpx, lpy + 60, 420, 300, 0.55, gid="dlamp"), z=zD + 9.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=shot_alpha("D")(t) * (0.7 + 0.18 * math.sin(2 * math.pi * (t + g0) / 0.8) *
                                                            math.sin(2 * math.pi * (t + g0) / 2.1))))
    glow_k = lambda t: M.progress(t, t_ta - 0.1, t_ta + 1.2, "inout")
    sc.add("d_babyglow", warm_glow_svg(bx_, by_ - 30, 260, 170, 0.95, "#fff0c0", gid="dbg"), z=zD + 9.6, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=shot_alpha("D")(t) * (0.15 + 0.85 * glow_k(t)) * (
               0.88 + 0.12 * math.sin(2 * math.pi * (t + g0) / 2.2))))
    sc.fx.append(gsparkles((bx_ - 260, by_ - 260, bx_ + 260, by_ + 20), g0, t0=t_jz - 0.1, t1=c_DE - DIP_DE, count=14,
                           color=(255, 240, 190), size=(7, 14), period=1.5, drift=-8, seed=90))

    # ================================================================ E: the street in the morning
    zE = zb("E")
    sc.add("street_day", street_bg_svg("dawn"), z=zE, motion=shot_m("E"))
    KE = 0.9
    tf_spots = {"woman": (590, R + 910), "elder": (1020, R + 904), "child": (1470, R + 930), "man": (1860, R + 912),
                "trav": (190, R + 846), "woman2": (1190, R + 830)}
    tf_kind = {"woman": ("woman", 1), "elder": ("elder", 0), "child": ("child", 1), "man": ("man", 2),
               "trav": ("traveller", 3), "woman2": ("woman", 4)}
    sh_spots = {"young": (420, R + 920), "beard": (860, R + 914), "boy": (1320, R + 946), "old": (1700, R + 920),
                "sturdy": (1580, R + 840)}

    def tf_draw(key):
        kind, v = tf_kind[key]
        x, y = tf_spots[key]

        def d(n):
            pose, expr, f = n.split("|")
            item = "jar" if kind == "woman" and pose in ("carry", "carry_walk_a", "carry_walk_b", "squeeze") else None
            return (C.ground_shadow(x, y, KE, 120 if kind != "child" else 90, 0.18) +
                    C.townsfolk(x, y, KE, int(f), kind=kind, variant=v, pose=pose, expr=expr, item=item))
        return d
    efigs = {}
    tf_plan = {"woman": [(0, "carry|happy|-1"), (t_jian + 0.5, "listen|kind|-1"), (t_jy + 0.02, "squeeze|surprised|-1")],
               "elder": [(0, "stand|happy|-1"), (t_jian + 0.65, "listen|kind|-1"), (t_jy + 0.1, "stand|amazed|-1")],
               "child": [(0, "stand|happy|-1"), (t_jian + 0.8, "listen|happy|-1"), (t_jy + 0.18, "cheer|surprised|-1")],
               "man": [(0, "stand|happy|-1"), (t_jian + 0.55, "listen|kind|-1"), (t_jy + 0.06, "cheer|surprised|-1")],
               "trav": [(0, "stand|happy|1"), (t_gs - 0.2, "listen|kind|1"), (t_jy + 0.14, "stand|amazed|1")],
               "woman2": [(0, "stand|happy|1"), (t_gs, "listen|kind|1"), (t_jy + 0.22, "stand|surprised|1")]}
    for key, plan in tf_plan.items():
        x, y = tf_spots[key]
        f_ = Fig(f"e_{key}", tf_draw(key), (x, y), KE, zE + 10 + y / 1000, g0, seed=400 + len(efigs))
        for tt, st in plan:
            f_.cut(tt, st, depth=5 if tt > 0 else 7)
        f_.mots.append(hop(snap(plan[-1][0]) + 0.05, KE, (x, y), 14, 0.26))
        f_.mots.append(breath((x, y), g0, 3.0 + 0.15 * len(efigs), 0.012, 0.2 * len(efigs)))
        if key in ("trav", "woman2"):      # they walk up to listen
            fdir = 1 if key == "trav" else -1
            t0w = t_jian + (0.3 if key == "trav" else 0.6)
            nst, per, strd = 4, 0.28, 60 * KE
            for k in range(nst):
                f_.cut(t0w + k * per, f"{'walk_a' if k % 2 == 0 else 'walk_b'}|happy|{fdir}", dip=False)
            t_arr = snap(t0w + nst * per)
            f_.cut(t_arr, f"stand|happy|{fdir}", depth=3)

            def wo(t, t0w=t0w, per=per, nst=nst, strd=strd, t_arr=t_arr, fdir=fdir):
                if t >= t_arr:
                    return Tf()
                done = sum(M.progress(t, t0w + k * per - 0.07, t0w + k * per + 0.08, "sine") for k in range(nst))
                return Tf(dx=-fdir * strd * (nst - done))
            f_.mots.append(wo)
        efigs[key] = f_
    shE = {}
    for key, (x, y) in sh_spots.items():
        f_ = Fig(f"e_{key}", shep_draw_s(key, KE, {"e": (x, y)}), (x, y), KE, zE + 10 + y / 1000, g0, seed=SEED[key])
        shE[key] = f_
    face = {"young": 1, "beard": 1, "boy": 1, "old": 1, "sturdy": 1}
    for i, key in enumerate(("young", "beard", "boy", "old", "sturdy")):
        f_ = shE[key]
        x, y = sh_spots[key]
        fc = face[key]
        f_.cut(0, f"stand|happy|{fc}|e|")
        t_c = t_kx + 0.12 * i
        f_.cut(t_c, f"cheer|joyful|{fc}|e|", depth=7)
        f_.mots.append(hop(snap(t_c) + 0.1, KE, (x, y), 26, 0.32))
        t_t = t_jian + 0.2 + 0.12 * i
        f_.cut(t_t, f"tell|joyful|{fc}|e|", depth=6)
        if key in ("young", "beard"):
            f_.cut(t_ts + 0.05 + 0.1 * i, f"point_up|joyful|{fc}|e|", depth=5)
            f_.cut(t_gs + 0.3 + 0.1 * i, f"tell|joyful|{fc}|e|", depth=5)
        f_.cut(t_tj + 0.3 + 0.1 * i, f"stand|happy|{fc}|e|", depth=4)
        f_.add_blinks({f"stand|happy|{fc}|e|": f"stand|{blink('happy')}|{fc}|e|"}, t_tj + 0.5, T, rng)
        f_.mots.append(breath((x, y), g0, 2.8 + 0.2 * i, 0.012, 0.25 * i))
        f_.build(sc, extra_motion=shot_m("E"))
    for f_ in efigs.values():
        f_.build(sc, extra_motion=shot_m("E"))
    elx, ely = sh_spots["boy"][0] + 70, sh_spots["boy"][1] + 8
    sc.add("e_lamb", doc7(sheep_markup(elx, ely, 1, 3, "stand", lamb=True, s=SK * 1.0)), z=zE + 10 + ely / 1000 + 0.001,
           seed=SEED["lamb"], motion=M.combine(breath((elx, ely), g0, 2.0, 0.025), shot_m("E")))
    for i, key in enumerate(("woman", "elder", "child", "man", "woman2")):
        x, y = tf_spots[key]
        top = y - {"child": 250, "woman": 400, "man": 360}.get(key, 340) * KE - 34
        sc.add(f"e_mark{i}", mark_svg(x + 10, top, "!", 104, "#ffe08a"), z=zE + 30, wc=0,
               motion=M.combine(pop_motion(t_jy + 0.08 + 0.06 * i, (x + 10, top), 0.35),
                                shot_m("E")))
    sc.fx.append(gsparkles((300, R + 300, 1900, R + 700), g0, t0=t_kx, t1=t_kx + 1.8, count=16, color=(255, 236, 170),
                           size=(8, 15), period=1.0, drift=-20, seed=92))

    # ================================================================ F: Mary keeps these things in her heart
    zF = zb("F")
    sc.add("stable_f", stable_f_svg(), z=zF, motion=shot_m("F"))
    dsp = PR.stable_points(*SF, SF_K)
    sc.add("f_animals", doc7(PR.donkey(*dsp["donkey"], SF_K * 0.88, 1, pose="sleep", sacks=0) +
                             PR.ox(dsp["ox"][0] + 60, dsp["ox"][1] - 20, SF_K * 0.88, -1, pose="sleep")), z=zF + 1,
           seed=501, motion=M.combine(breath((SF[0], SF[1]), g0, 3.6, 0.008), shot_m("F")))
    bale = (MARY_F[0] + 40 * SF_K, MARY_F[1])
    sc.add("f_bale", doc7(PR.hay(bale[0], bale[1], 0.58 * SF_K, 1, kind="bale")), z=zF + 2, seed=502,
           motion=shot_m("F"))
    mf = Fig("f_mary", lambda n: C.mary(MARY_F[0], MARY_F[1], SF_K, 1, pose="sit_baby", expr=n, glow=0.25),
             MARY_F, SF_K, zF + 3, g0, seed=503)
    mf.cut(0, "thoughtful")
    mf.cut(t_zx - 0.2, "tender", dip=False)
    mf.cut(t_jx + 0.3, "thoughtful", dip=False)
    mf.cut(t_xx2 + 0.2, "peaceful", dip=False)
    mf.mots.append(breath(MARY_F, g0, 3.4, 0.01))
    mf.mots.append(rot_about(lambda t: 1.4 * math.sin(2 * math.pi * (t + g0) / 5.0) * env(t, t_xx1 - 0.3, T, 0.8, 1),
                             (MARY_F[0], MARY_F[1] - 60), MARY_F))
    mf.build(sc, extra_motion=shot_m("F"))
    sc.add("f_sun", doc7(f'<defs>{S.lin_grad("fsun", [(0, "#fff2cc", 0.0), (0.35, "#fff2cc", 0.5), (1, "#fff2cc", 0)], 0, 0, 1, 1)}'
                         f'</defs><path d="M1500,{R - 20} L2140,{R - 20} L1320,{R + 1200} L560,{R + 1200} Z" '
                         f'fill="url(#fsun)"/>'), z=zF + 8, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=shot_alpha("F")(t) * (0.45 + 0.08 * math.sin(2 * math.pi * (t + g0) / 4.0))))
    sc.add("f_glow", warm_glow_svg(MARY_F[0] + 40, MARY_F[1] - 150 * SF_K, 480, 380, 0.55, "#fff0c0", gid="fgl"),
           z=zF + 8.1,
           wc=0, blend="screen", motion=lambda t: Tf(alpha=shot_alpha("F")(t) * (0.8 + 0.2 * math.sin(
               2 * math.pi * (t + g0) / 2.6))))
    from engine import fx as FX
    sc.fx.append(FX.motes((900, R + 60, 2000, R + 1100), count=26, t0=c_EF - 0.6, t1=T + 1, color=(255, 246, 214),
                          size=(3, 6), seed=97, alpha=120))
    # the memory bubble: the angel, then the shepherds kneeling
    bcx, bcy, brx, bry = 1440, R + 290, 300, 210
    head = (MARY_F[0] + 20, MARY_F[1] - 236 * SF_K)

    def membub(content, key):
        cid = f"mb{key}"
        shape = S.blob(bcx, bcy, brx, bry, wobble=0.05, n=14, seed=8)
        gid = f"mbg{key}"
        defs = (S.rad_grad(gid, [(0, "#fffaf0", 1), (0.65, "#fff3d6", 1), (1, "#f4dcaa", 1)]) +
                f'<clipPath id="{cid}"><path d="{shape}"/></clipPath>')
        b = f'<path d="{shape}" fill="url(#{gid})"/>'
        b += f'<g clip-path="url(#{cid})">{content}</g>'
        b += f'<path d="{shape}" fill="none" stroke="{INK}" stroke-width="4"/>'
        b += (f'<path d="{shape}" fill="none" stroke="#f2c14e" stroke-width="3" opacity="0.6" '
              f'transform="translate({bcx},{bcy}) scale(0.95) translate({-bcx},{-bcy})"/>')
        return doc7(S.g(b, filter="wobble-fine"), defs)
    dots = ""
    for i, u in enumerate((0.25, 0.5)):
        px = head[0] + (bcx - brx * 0.8 - head[0]) * u + 60
        py = head[1] + (bcy + bry * 0.6 - head[1]) * u - 40
        dots += f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{9 + 7 * i}" fill="#fff6dc" stroke="{INK}" stroke-width="2.6"/>'
    # the same angel in both pictures (identical drawing), so the second only adds the shepherds below it
    angel_pic = C.angel(bcx + 130, bcy + 40, 0.4, -1, pose="float", glow=0.6, lift=0)
    shep_pic = (angel_pic +
                shep_s("boy", "hold_lamb", "happy", 1, bcx - 200, bcy + 156, 0.42) +
                shep_s("old", "kneel", "awed", 1, bcx - 125, bcy + 150, 0.42) +
                shep_s("beard", "kneel", "awed", 1, bcx - 50, bcy + 146, 0.42) +
                shep_s("young", "kneel", "awed", 1, bcx + 25, bcy + 152, 0.42))
    sky_bits = (f'<rect x="{bcx - brx}" y="{bcy - bry}" width="{2 * brx}" height="{2 * bry}" fill="#2a3a64"/>'
                f'<ellipse cx="{bcx}" cy="{bcy + bry}" rx="{brx * 1.2}" ry="{bry * 0.45}" fill="#4f6a46"/>')
    glow_bits = (f'<defs>{S.rad_grad("mbgl", [(0, "#fff6d0", 0.95), (1, "#fff6d0", 0)])}</defs>'
                 f'<ellipse cx="{bcx}" cy="{bcy - 10}" rx="{brx * 0.7}" ry="{bry * 0.9}" fill="url(#mbgl)"/>')
    t_m1 = t_zx - 0.05
    t_m2 = t_jx + 0.05
    t_mout = max(t_xx2 + 0.15, T - 1.5)
    bub_out = lambda t: 1 - M.progress(t, t_mout, t_mout + 0.7, "sine")
    bob = lambda t: Tf(dy=5 * math.sin(2 * math.pi * (t + g0) / 3.0),
                       sx=1 + 0.025 * env(t, t_xx1 - 0.1, t_xx1 + 0.7, 0.3, 0.4) + 0.025 * env(t, t_xx2 - 0.1,
                                                                                            t_xx2 + 0.7, 0.3, 0.4),
                       sy=1 + 0.025 * env(t, t_xx1 - 0.1, t_xx1 + 0.7, 0.3, 0.4) + 0.025 * env(t, t_xx2 - 0.1,
                                                                                            t_xx2 + 0.7, 0.3, 0.4),
                       px=bcx, py=bcy)
    sc.add("f_dots", doc7(dots), z=zF + 9, wc=0.4, motion=M.combine(
        lambda t: Tf(alpha=M.progress(t, t_m1 - 0.3, t_m1, "sine") * bub_out(t)), shot_m("F")))
    sc.add("f_bub_angel", membub(sky_bits + glow_bits + angel_pic, "a"), z=zF + 9.1, seed=504, motion=M.combine(
        pop_motion(t_m1, (bcx - brx * 0.6, bcy + bry * 0.6), 0.55), bob,
        lambda t: Tf(alpha=bub_out(t)), shot_m("F")))
    # the second picture (same sky, glow and angel) fades in over the first: only the shepherds appear
    sw = lambda t: M.progress(t, t_m2, t_m2 + 0.7, "sine")
    sc.add("f_bub_shep", membub(sky_bits + glow_bits + shep_pic, "s"), z=zF + 9.2, seed=505, motion=M.combine(
        lambda t: Tf(alpha=sw(t) * bub_out(t)), bob, shot_m("F")))
    sc.fx.append(gsparkles((bcx - brx, bcy - bry - 40, bcx + brx, bcy + bry), g0, t0=t_m1, t1=t_mout + 0.6, count=10,
                           color=(255, 244, 210), size=(6, 12), period=1.6, drift=-6, seed=94))

    # ================================================================ camera
    # each shot has its own framing; the camera jumps only on a hard cut or at the middle of a paper dip
    keys = []

    def shot(*pts):
        for t, c, crv in pts:
            keys.append((t, c, crv))

    def cut_at(tc, cam_in):
        keys.append((tc - 0.004, keys[-1][1], "linear"))
        keys.append((tc + 0.004, cam_in, "linear"))
    shot((0.0, Cam(1056, 1090, 2112), "linear"), (t_hui - 0.3, Cam(1056, 1090, 2112), "linear"),
         (t_hui + 1.9, Cam(880, 1292, 1600), "sine"), (t_s0, Cam(860, 1288, 1620), "sine"),
         (c_AB, Cam(830, 1284, 1650), "sine"))
    cut_at(c_AB, Cam(1120, 1262, 1840))
    shot((c_BC, Cam(920, 1262, 1840), "sine"))
    cut_at(c_BC, Cam(1000, 1262, 1800))
    shot((t_found - 0.15, Cam(960, 1262, 1800), "sine"), (c_CD, Cam(900, 1262, 1800), "sine"))
    cut_at(c_CD, Cam(1060, 1252, 1820))
    shot((t_xyh - 0.1, Cam(1060, 1252, 1820), "linear"), (t_mc + 0.5, Cam(1150, 1280, 1520), "sine"),
         (t_pai, Cam(1140, 1276, 1540), "sine"), (c_DE, Cam(1110, 1266, 1600), "sine"))
    cut_at(c_DE, Cam(1040, 1254, 1660))
    shot((c_EF, Cam(1060, 1250, 1640), "sine"))
    cut_at(c_EF, Cam(1100, 1184, 1880))
    shot((T, Cam(1084, 1182, 1850), "sine"))
    sc.camera = cam_path([(t, c) for t, c, _ in keys], [crv for _, _, crv in keys[1:]])

    # the page turns inside the scene (through the paper colour, like the film's 'dippaper' transitions)
    def paper_dip(mid, half, col=(247, 240, 226)):
        from PIL import Image

        def fx(frame, t, view):
            u = abs(t - mid) / half
            if u >= 1.0:
                return frame
            a = 0.5 + 0.5 * math.cos(math.pi * u)
            return Image.alpha_composite(frame, Image.new("RGBA", frame.size, (*col, int(255 * a + 0.5))))
        return fx
    sc.fx.append(paper_dip(c_AB, DIP_AB))
    sc.fx.append(paper_dip(c_DE, DIP_DE))

    # ================================================================ sound
    sc.sfx("night", 0, dur=c_DE + 0.2, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0, dur=c_AB, gain_db=-21, fade_in=0.8, fade_out=0.6, pan=-0.2)
    sc.sfx("whoosh", t_hui - 0.2, gain_db=-17)
    sc.sfx("chime", t_hui, gain_db=-16)
    sc.sfx("sheep", t_hui + 2.0, gain_db=-24, pan=0.5)
    sc.sfx("cloth", t_shuo + 0.3, gain_db=-21)
    sc.sfx("cheer", t_s0 + 0.1, dur=1.2, gain_db=-24, fade_in=0.1, fade_out=0.6)
    sc.sfx("footsteps_run", c_AB - 0.2, dur=c_BC - c_AB + 0.25, gain_db=-17, fade_in=0.3, fade_out=0.15)
    sc.sfx("sheep", c_AB + 1.2, gain_db=-23, pan=0.3)
    sc.sfx("pop", t_zhao1 + 0.1, gain_db=-20, pan=0.2)
    sc.sfx("pop", t_zhao2 + 0.1, gain_db=-20, pan=0.5)
    sc.sfx("sheep", t_found + 0.2, gain_db=-19, pan=-0.4)
    sc.sfx("sparkle", t_found, gain_db=-19, pan=-0.6)
    sc.sfx("footsteps", c_CD, dur=t_in0 + 1.7 - c_CD, gain_db=-23, pan=0.4, fade_in=0.05, fade_out=0.5)
    sc.sfx("cloth", t_dou + 0.2, gain_db=-21)
    sc.sfx("sheep", t_lay, gain_db=-22, pan=0.1)
    sc.sfx("chime", t_ta, gain_db=-15)
    sc.sfx("sparkle", t_jz, gain_db=-18)
    sc.sfx("rooster", c_DE + 0.3, gain_db=-21, pan=-0.5)
    sc.sfx("birds", c_DE, dur=T - c_DE + 0.3, gain_db=-22, fade_in=0.6, fade_out=1.0)
    sc.sfx("cheer", t_kx + 0.1, dur=1.4, gain_db=-21, fade_in=0.1, fade_out=0.6)
    sc.sfx("crowd", t_jian, dur=c_EF - t_jian, gain_db=-25, fade_in=0.6, fade_out=0.3)
    sc.sfx("footsteps", t_jian + 0.3, dur=1.4, gain_db=-25)
    sc.sfx("pop", t_jy + 0.05, gain_db=-19)
    sc.sfx("chime", t_m1, gain_db=-18, pan=0.4)
    sc.sfx("sparkle", t_m2, gain_db=-20, pan=0.4)
    return sc
