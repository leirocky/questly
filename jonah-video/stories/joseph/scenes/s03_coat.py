"""Scene 3 — Genesis 37:2-4. Canaan: rolling hills, flocks and tents. Old Jacob steps out of his big goat-hair tent;
his twelve sons pop up one by one as they are counted (a little number badge counts 1..12: the ten older brothers,
then Joseph, then little Benjamin); a warm heart floats over Jacob and Joseph; Jacob holds up a new coat and its
coloured bands appear one per colour word; Joseph puts it on and twirls; then the ten older brothers fold their arms,
jealous, one after another, and the front one grumbles to his brother.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers, so a new take
stays in sync):
  0 .. 2       calm wide establishing page: clouds drift, sheep graze and bleat, grass sways, birds fly
  '有一个爸爸'   Jacob steps out of the dark tent doorway and walks left (planted-foot strides, footsteps)
  '雅各'        he stops and raises his hand in greeting (squash cut), a little sparkle (chime)
  '十二个儿子'   the camera widens; the twelve sons pop up one after another (pop each), the number badge counting
               1..12: the ten brothers left to right, then Joseph (11) beside Jacob, then Benjamin (12)
  '雅各最疼爱的' Jacob turns to Joseph (squash cut); on '最' a warm heart pops up over the two of them (sparkle)
  '第十一个'     a small badge '11' pops over Joseph's head; '约瑟' Joseph hops happily
  '做了一件'     Jacob holds up the new coat - plain cream (cloth)
  红 黄 蓝 绿    each colour word fades in its band (progress 1/6 per band) with sparkles in that colour (sparkle)
  '好漂亮'       a puff of sparkles: Joseph wears the finished coat (all six colours), twirls twice (squash flips,
               whoosh) and stands proud; Benjamin cheers
  '哥哥们看见了' the camera glides left to the ten brothers
  '酸溜溜的'     their faces turn jealous one after another as they fold their arms (squash cuts, nearest first)
  B line       '凭什么只给他做？' the front brother turns to his neighbour and grumbles behind his hand (whisper);
               the neighbour leans in and nods; calm hold (page dip to s04)
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.joseph.scenes import s01_title as T1
from stories.joseph.scenes.s01_title import blink_name, char_times, cuts, dip, doc, heart_markup, snap, voice_marks

INK = P["ink"]
GY = 1012                    # ground line (front row)
SC = 0.95                    # everyone's scale
JAC_X0, JAC_X = 1803, 1220   # Jacob: tent doorway -> his spot
JOS_X, BEN_X = 1486, 1668
TENT = (1722, GY - 14)       # big tent: bottom centre of the doorway
FRONT = [(170, 6), (360, 2), (550, 0), (740, 3), (930, 7)]          # (x, variant), front row (ground GY + 6)
BACK = [(265, 4), (455, 8), (645, 1), (835, 5), (1025, 9)]         # back row (ground GY - 34, 0.94 scale)
BADGE = (1056, 300)
COLOR_RGB = ((240, 112, 100), (250, 214, 92), (112, 160, 230), (128, 198, 108))


def step_walk(t0, n, step, period, s, move=0.15):
    """Planted-foot walk with only two stride drawings (walk_a / walk_b), copied from art/scenes/s17_king.py: each
    drawing holds its anchor still; as the next one cuts in, the anchor advances one stride with a little lift.
    Returns (frame_at(t) -> 0/1 or None, dx(t), dy(t), t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]
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


# ================================================================== backdrop


def sky_svg():
    defs = (S.lin_grad("j3sky", [(0, "#8cc6de"), (0.5, "#bfe0e6"), (0.85, "#e6eedb"), (1, "#f4ecd2")]) +
            S.rad_grad("j3sun", [(0, "#fff6d6", 0.9), (0.4, "#fff0c0", 0.4), (1, "#fff0c0", 0)]))
    b = S.rect_bg("url(#j3sky)") + '<circle cx="1900" cy="110" r="480" fill="url(#j3sun)"/>'
    return doc(b, defs)


def clouds_svg():
    sh = "#d6e6ee"
    b = (S.cloud(360, 180, 340, 100, "#fbf6ec", seed=31, sw=3.5, shade_fill=sh) +
         S.cloud(1180, 120, 300, 90, "#fbf6ec", seed=32, sw=3.2, shade_fill=sh) +
         S.cloud(1640, 300, 220, 70, "#f8f3ea", seed=33, sw=2.8, shade_fill=sh) +
         S.cloud(760, 380, 200, 60, "#f8f3ea", seed=34, sw=2.6, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def far_svg():
    b = S.path(S.hill(-200, W + 200, 640, 90, seed=41, bumps=4), fill="#c4d7c4", sw=2.2)
    b += S.path(S.hill(-200, W + 200, 700, 70, seed=42, bumps=5), fill="#b3cda1", sw=2.4)
    trees = ""
    for x, y, s in ((140, 690, 0.28), (980, 700, 0.24), (1500, 690, 0.26), (2020, 696, 0.3)):
        trees += PR.olive_tree(x, y, s, seed=int(x))
    tents = PR.tent(560, 708, 0.3, 1, side="israel", flag=False) + PR.tent(820, 716, 0.24, -1, side="israel",
                                                                              flag=False)
    flock = ""
    rng = random.Random(11)
    for i in range(10):
        x = 1100 + i * 52 + rng.uniform(-14, 14)
        y = 716 + rng.uniform(0, 18)
        flock += PR.sheep(x, y, 0.2, 1 if i % 3 else -1, i % 4, pose="graze" if i % 2 else "stand")
    return doc(S.g(b, filter="wobble") + PR._haze(trees + tents + flock, "#c9d9c4", 0.4, 0.4))


def mid_svg():
    """The middle meadow with a grazing flock, olive trees and a little stone sheepfold."""
    d = S.smooth_path([(-100, 820), (300, 772), (700, 760), (1100, 776), (1500, 770), (1900, 760), (W + 100, 772)],
                      closed=False) + f" L{W + 100},{H + 60} L-100,{H + 60} Z"
    defs = S.lin_grad("j3mid", [(0, "#a9c97f"), (1, "#98bd6c")])
    b = S.g(S.path(d, fill="url(#j3mid)", sw=3), filter="wobble")
    fold = ""
    for i in range(14):
        x = 1240 + i * 30
        fold += (f'<ellipse cx="{x}" cy="{796 - 8 * math.sin(i)}" rx="20" ry="13" fill="#d6cbb2" stroke="{INK}" '
                 f'stroke-width="2.4"/>')
    b += S.g(fold, filter="wobble-fine")
    items = PR.olive_tree(80, 800, 0.62, seed=7) + PR.olive_tree(1990, 790, 0.55, seed=9)
    items += PR.bush(1120, 790, 0.5, variant=1) + PR.bush(300, 800, 0.45, variant=0)
    flock = ""
    for i, (x, y) in enumerate(((420, 806), (520, 798), (610, 812), (700, 800), (800, 810), (1600, 800),
                                (1700, 806))):
        flock += PR.sheep(x, y, 0.42, 1 if i % 2 else -1, i % 4, pose="graze" if i % 3 else "stand")
    b += PR._haze(items + flock, "#d3e2c8", 0.12, 0.15)
    return doc(b, defs)


def tent_svg():
    """Jacob's big striped tent (custom: the library tent is too small for a man to walk out of): a wide ridge tent
    with sloping cloth walls in cream / brown bands, the front flaps tied back round a dark doorway with a lamp glow,
    a centre pole, guy ropes and pegs."""
    x, y = TENT
    band_a, band_b, inner = "#e6d3ae", "#9c7653", "#3a2a20"
    outline = (f"M{x - 360},{y} L{x - 300},{y - 250} Q{x - 220},{y - 400} {x - 110},{y - 430} L{x + 110},{y - 430} "
               f"Q{x + 220},{y - 400} {x + 300},{y - 250} L{x + 360},{y} Z")
    b = ""
    for sx in (-1, 1):
        for ex, ey, px_ in ((300, 250, 450), (200, 390, 430)):
            b += (f'<path d="M{x + sx * ex},{y - ey} L{x + sx * px_},{y - 2}" stroke="#8a6a45" stroke-width="3"/>'
                  f'<rect x="{x + sx * px_ - 5}" y="{y - 16}" width="10" height="20" fill="{P["wood_dark"]}" '
                  f'stroke="{INK}" stroke-width="2"/>')
    b += S.path(outline, fill=band_a, sw=4.5)
    st = ""
    for k, yy in enumerate(range(y - 440, y + 10, 46)):
        if k % 2:
            st += f'<rect x="{x - 400}" y="{yy}" width="800" height="23" fill="{band_b}"/>'
    st += f'<rect x="{x - 400}" y="{y - 440}" width="800" height="70" fill="{S.shade(band_b, -0.15)}"/>'
    for xx in (-300, -200, 200, 300):
        st += (f'<path d="M{x + xx * 0.86},{y - 410 + abs(xx) * 0.5} L{x + xx * 1.15},{y}" stroke="{INK}" '
               f'stroke-width="2.4" opacity="0.35"/>')
    b += f'<g clip-path="url(#j3tc)">{st}</g>' + S.path(outline, fill="none", sw=4.5)
    # the doorway and the tied-back flaps
    door = f"M{x - 110},{y} L{x - 64},{y - 330} Q{x},{y - 368} {x + 64},{y - 330} L{x + 110},{y} Z"
    b += S.path(door, fill=inner, sw=4)
    b += (f'<ellipse cx="{x + 34}" cy="{y - 190}" rx="46" ry="56" fill="#f2b45a" opacity="0.28" filter="url(#soft)"/>'
          f'<path d="M{x + 24},{y - 200} l18,0 l-4,22 l-10,0 Z" fill="#c9714a" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M{x + 33},{y - 202} q6,-10 2,-22" stroke="#f6d36b" stroke-width="4" fill="none"/>')
    for sx in (-1, 1):
        flap = (f"M{x + sx * 64},{y - 330} Q{x + sx * 140},{y - 250} {x + sx * 150},{y - 150} "
                f"Q{x + sx * 160},{y - 60} {x + sx * 186},{y} L{x + sx * 120},{y} Q{x + sx * 100},{y - 120} "
                f"{x + sx * 64},{y - 330} Z")
        b += S.path(flap, fill=S.shade(band_a, -0.08), sw=3.5)
        b += (f'<path d="M{x + sx * 108},{y - 170} Q{x + sx * 130},{y - 160} {x + sx * 150},{y - 168}" '
              f'stroke="#b5523b" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b += (f'<path d="M{x},{y - 430} L{x},{y - 500}" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
          f'<path d="M{x},{y - 430} L{x},{y - 500}" stroke="{P["wood"]}" stroke-width="7" stroke-linecap="round"/>'
          f'<circle cx="{x}" cy="{y - 504}" r="8" fill="{P["gold"]}" stroke="{INK}" stroke-width="2.4"/>')
    defs = f'<clipPath id="j3tc"><path d="{outline}"/></clipPath>'
    return doc(S.g(b, filter="wobble-fine"), defs)


def near_svg():
    d = S.smooth_path([(-100, 960), (400, 952), (900, 948), (1400, 958), (1900, 950), (W + 100, 956)], closed=False)
    d += f" L{W + 100},{H + 60} L-100,{H + 60} Z"
    defs = S.lin_grad("j3near", [(0, "#a6cc66"), (0.5, "#93b85c"), (1, "#7fa64d")])
    b = S.path(d, fill="url(#j3near)", sw=4)
    for x, y, rx in ((300, 1080, 220), (1000, 1100, 260), (1700, 1090, 220)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.14:.0f}" fill="#b6d470" opacity="0.6"/>'
    fl = T1.flowers(random.Random(17), 80, -40, W + 40, 975, 1180)
    return doc(S.g(b, filter="wobble") + S.g(fl, filter="wobble-fine"), defs)


def tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((40, 1186, 1.2, 2), (470, 1176, 1.0, 0), (860, 1190, 1.0, 2), (1230, 1186, 1.0, 0),
                       (1620, 1188, 1.1, 2), (1980, 1180, 1.2, 1), (1080, 1090, 0.6, 2), (300, 1060, 0.55, 0)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


# ================================================================== people


def shadow(x, y, s, w=150):
    return C.ground_shadow(x, y + 2, s, w, 0.2)


def jacob_svg(x, pose, facing, expr=None, progress=1.0):
    return doc(shadow(x, GY, SC) + C.jacob(x, GY, SC, facing, pose=pose, expr=expr, progress=progress))


def joseph_svg(pose, facing, expr, coat=None):
    return doc(shadow(JOS_X, GY, SC, 130) + C.joseph(JOS_X, GY, SC, facing, pose=pose, expr=expr, coat=coat))


def benjamin_svg(pose, expr):
    return doc(shadow(BEN_X, GY, SC, 90) + C.brothers(BEN_X, GY, SC, -1, variant="benjamin", pose=pose, expr=expr))


def brother_svg(x, y, s, v, pose, facing, expr, staff=None):
    return doc(shadow(x, y, s, 140) + C.brothers(x, y, s, facing, variant=v, pose=pose, expr=expr, staff=staff))


def badge_svg(n, x, y, r=58, size=74):
    if n <= 0:
        return doc("")
    defs = S.lin_grad("j3bg", [(0, "#ec8a45"), (1, "#c2552a")])
    b = (f'<circle cx="{x + 4}" cy="{y + 7}" r="{r}" fill="{INK}" opacity="0.22" filter="url(#soft)"/>'
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffaf0" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{x}" cy="{y}" r="{r - 10}" fill="none" stroke="#f2c84b" stroke-width="4" '
         f'stroke-dasharray="8 7"/>')
    b = S.g(b, filter="wobble-fine")
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b += (f'<text x="{x}" y="{y + size * 0.36:.0f}" {font} fill="url(#j3bg)" stroke="{INK}" stroke-width="3" '
          f'paint-order="stroke">{n}</text>')
    return doc(b, defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines
    marks = [voice_marks(ctx, i) for i in range(len(L))]

    def phr(li, text, default):
        for m in marks[li]:
            if text in m[0] or m[0] in text:
                return m
        return (text, default, default + 0.8, [(default, default + 0.8)])

    def at(li, text, k=0):
        """onset of character k of the measured phrase containing ``text``"""
        m = phr(li, text, L[li].start)
        ct = char_times(m)
        j = m[0].index(text) + k if text in m[0] else 0
        return ct[min(j, len(ct) - 1)]

    t_dad = phr(0, "有一个爸爸", L[0].start + 1.2)[1]
    t_jacob = at(0, "雅各")
    t_twelve = at(0, "十二")
    p_sons = phr(0, "他有十二个儿子", L[0].chunks[-1].start)
    t_love = at(1, "最")
    t_turn = snap(phr(1, "雅各最疼爱的", L[1].start)[1] - 0.05)
    t_eleven = at(1, "十一")
    t_jo = phr(1, "约瑟", L[1].end - 0.5)[1]
    t_give = snap(at(2, "做了"))
    t_cols = [phr(2, c, L[2].chunks[-1].start + 0.6 * i)[1] for i, c in enumerate(("红的", "黄的", "蓝的", "绿的"))]
    t_pretty = phr(2, "好漂亮", L[2].end - 0.8)[1]
    t_saw = phr(3, "哥哥们看见了", L[3].start)[1]
    p_sour = phr(3, "心里酸溜溜的", L[3].start + 1.4)
    t_sour = at(3, "酸溜溜")
    t_b = L[4].start
    t_b2 = L[4].chunks[0].start + 0.45 * (L[4].end - L[4].start)

    # ------------------------------------------------------------ backdrop
    sc.add("sky", sky_svg(), wc=0.5)
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=7))
    sc.add("far", far_svg())
    sc.add("mid", mid_svg())
    # a few animated sheep on the meadow (head up / graze), one bleats
    for i, (x, y, s, f, v, per, ph_) in enumerate(((1880, 980, 0.62, -1, 0, 5.2, 0.0), (1990, 1010, 0.58, -1, 2, 6.1, 0.4),
                                                    (60, 1000, 0.6, 1, 3, 5.7, 0.7))):
        fr = [doc(C.ground_shadow(x, y + 2, s, 190, 0.18) + PR.sheep(x, y, s, f, v, pose=p))
              for p in ("graze", "stand", "bleat")]
        t_bl = 1.2 + i * 7.5

        def sfa(t, per=per, ph_=ph_, t_bl=t_bl):
            if t_bl <= t < t_bl + 0.9:
                return 2.0
            return 1.0 if ((t / per + ph_) % 1.0) < 0.35 else 0.0
        sc.add(f"sheep{i}", fr, frame_at=sfa, seed=70 + i, motion=M.breathe(0.012, 2.8 + 0.3 * i, pivot=(x, y)))
    sc.add("tent", tent_svg())
    sc.add("near", near_svg())

    # ------------------------------------------------------------ Jacob
    walk_n, period = 7, 0.28
    step = (JAC_X0 - JAC_X) / walk_n
    t_w0 = snap(t_dad - 0.3)
    wfa, wdx, wdy, t_w1 = step_walk(t_w0, walk_n, step, period, SC)
    names = ["walk_a", "walk_b", "stand_l", "bless_l", "stand_r", "stand_r_b", "give0", "give1", "give2", "give3",
             "give4", "talk_r", "talk_r_b"]
    jfr = [jacob_svg(JAC_X0, "walk_a", -1), jacob_svg(JAC_X0, "walk_b", -1), jacob_svg(JAC_X, "stand", -1, "kind"),
           jacob_svg(JAC_X, "bless", -1, "happy"), jacob_svg(JAC_X, "stand", 1, "kind"),
           jacob_svg(JAC_X, "stand", 1, blink_name("kind")),
           *[jacob_svg(JAC_X, "give", 1, "happy", k / 6) for k in range(5)],
           jacob_svg(JAC_X, "talk", 1, "happy"), jacob_svg(JAC_X, "talk", 1, blink_name("happy"))]
    JN = {n: i for i, n in enumerate(names)}
    t_greet = snap(t_jacob - 0.02)
    t_greet_end = snap(min(t_greet + 1.1, t_twelve - 0.1))
    t_on = snap(t_pretty - 0.12)
    jents = [(0, JN["walk_a"]), (t_w1, JN["stand_l"]), (t_greet, JN["bless_l"]), (t_greet_end, JN["stand_l"]),
             (t_turn, JN["stand_r"]), (t_give, JN["give0"]), (t_on, JN["talk_r"])]
    for tb, base, bl in ((t_eleven + 0.5, "stand_r", "stand_r_b"), (t_on + 1.4, "talk_r", "talk_r_b"),
                         (t_sour + 0.5, "talk_r", "talk_r_b")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in jents):
            jents += [(tb, JN[bl]), (snap(tb + 0.13), JN[base])]
    jents.sort()
    base_fa = cuts(jents)

    def jac_fa(t):
        w = wfa(t)
        if w is not None:
            return w
        if t_give <= t < t_on:
            p = sum(M.progress(t, tc - 0.05, tc + 0.25, "sine") for tc in t_cols)
            return float(JN["give0"]) + min(4.0, p)
        return base_fa(t)

    def jac_m(t):
        if t < t_w0 - 0.12:
            return Tf(alpha=0)
        a = M.progress(t, t_w0 - 0.12, t_w0 + 0.3, "sine")
        if t < t_w1:
            return Tf(dx=-wdx(t), dy=wdy(t), alpha=a)
        return Tf()
    jpiv = (JAC_X, GY)
    sc.add("jacob", jfr, frame_at=jac_fa, seed=11,
           motion=M.combine(jac_m, *[dip(tc, SC, jpiv, 7) for tc in (t_w1, t_greet, t_greet_end, t_turn, t_give,
                                                                       t_on)],
                            lambda t: Tf(sx=1 + 0.01 * math.sin(2 * math.pi * t / 2.9),
                                         sy=1 + 0.01 * math.sin(2 * math.pi * t / 2.9), px=JAC_X, py=GY)))

    # ------------------------------------------------------------ the twelve sons pop up as they are counted
    sons = []
    order = sorted([(x, v, "F") for x, v in FRONT] + [(x, v, "B") for x, v in BACK])
    pop0 = t_twelve - 0.05
    pop1 = max(p_sons[2] + 0.1, pop0 + 1.3)
    pop_t = [snap(pop0 + (pop1 - pop0) * i / 11) for i in range(12)]
    # jealousy ripple: nearest to Joseph first
    sour_order = sorted(range(10), key=lambda i: -order[i][0])
    sour0, sour1 = t_sour - 0.05, max(p_sour[2], t_sour + 1.0)
    sour_t = {}
    for k, i in enumerate(sour_order):
        sour_t[i] = snap(sour0 + (sour1 - sour0) * k / 9)
    front_x = max(x for x, _ in FRONT)
    neigh_x = sorted(x for x, _ in FRONT)[-2]
    t_wh = snap(t_b - 0.05)
    t_nod = [snap(t_b2), snap(t_b2 + 0.45)]

    def pop_motion(tp, piv, s):
        def m(t):
            if t < tp:
                return Tf(alpha=0)
            u = min(1.0, (t - tp) / 0.4)
            k = 0.35 + 0.65 * M.ease("back")(u)
            return Tf(sx=k, sy=k, dy=-30 * s * math.sin(math.pi * u) * (1 - u), alpha=min(1.0, (t - tp) / 0.08),
                      px=piv[0], py=piv[1])
        return m

    for i, (x, v, row) in enumerate(order):
        y = GY + 6 if row == "F" else GY - 34
        s = SC if row == "F" else SC * 0.94
        fr = [brother_svg(x, y, s, v, "stand", 1, "neutral"), brother_svg(x, y, s, v, "stand", 1, blink_name("neutral")),
              brother_svg(x, y, s, v, "cross_arms", 1, "jealous"),
              brother_svg(x, y, s, v, "cross_arms", 1, blink_name("jealous"))]
        tc = sour_t[i]
        ents = [(0, 0), (tc, 2)]
        if x == front_x:
            fr.append(brother_svg(x + 26, y, s, v, "whisper", -1, "jealous"))
            ents.append((t_wh, 4))
        for tb in (pop_t[i] + 1.6 + 0.37 * i, pop_t[i] + 5.5 + 0.61 * i, pop_t[i] + 10.2 + 0.43 * i):
            tb = snap(tb)
            if tb < tc - 0.3:
                ents += [(tb, 1), (snap(tb + 0.13), 0)]
        tb = snap(tc + 1.4 + 0.2 * (i % 3))
        if tb < (t_wh - 0.3 if x == front_x else T - 0.5):
            ents += [(tb, 3), (snap(tb + 0.13), 2)]
        ents.sort()
        piv = (x, y)
        mots = [pop_motion(pop_t[i], piv, s), dip(tc, s, piv, 7),
                M.breathe(0.011, 2.5 + 0.17 * (i % 4), pivot=piv, phase=0.13 * i)]
        if x == front_x:
            mots.append(dip(t_wh, s, piv, 7))
            mots.append(lambda t, piv=piv: Tf(rot=-2.5 * M.progress(t, t_wh, t_wh + 0.4, "sine") *
                                              (1 + 0.25 * math.sin(2 * math.pi * (t - t_wh) / 0.7)),
                                              px=piv[0], py=piv[1]))
        if x == neigh_x:      # leans in to listen, then nods twice
            def lean(t, piv=piv):
                r = 3.0 * M.progress(t, t_wh + 0.15, t_wh + 0.55, "sine")
                for tn in t_nod:
                    u = t - tn
                    if 0 <= u < 0.3:
                        r += 2.5 * math.sin(math.pi * u / 0.3)
                return Tf(rot=r, px=piv[0], py=piv[1])
            mots.append(lean)
        sc.add(f"bro{i}", fr, frame_at=cuts(ents), seed=100 + 7 * i, z=20 + (0 if row == "B" else 1) + 0.01 * i,
               motion=M.combine(*mots))
        sons.append((x, y, s))

    # Joseph (11th) and Benjamin (12th)
    names = ["stand", "stand_b", "amazed", "amazed_b", "coat_l", "coat_r", "coat_l_b"]
    jo_fr = [joseph_svg("stand", -1, "happy"), joseph_svg("stand", -1, blink_name("happy")),
             joseph_svg("stand", -1, "amazed"), joseph_svg("stand", -1, blink_name("amazed")),
             joseph_svg("stand", -1, "proud", "colours"), joseph_svg("stand", 1, "proud", "colours"),
             joseph_svg("stand", -1, blink_name("proud"), "colours")]
    ON = {n: i for i, n in enumerate(names)}
    flips = [t_on, snap(t_on + 0.34), snap(t_on + 0.68), snap(t_on + 1.02)]
    t_jo_pop = pop_t[10]
    oents = [(0, ON["stand"]), (t_give, ON["amazed"]), (flips[0], ON["coat_r"]), (flips[1], ON["coat_l"]),
             (flips[2], ON["coat_r"]), (flips[3], ON["coat_l"])]
    for tb, base, bl in ((t_jo_pop + 1.3, "stand", "stand_b"), (t_love + 1.0, "stand", "stand_b"),
                         (t_cols[1] + 0.35, "amazed", "amazed_b"), (flips[3] + 1.2, "coat_l", "coat_l_b"),
                         (t_sour + 0.9, "coat_l", "coat_l_b"), (t_b + 0.8, "coat_l", "coat_l_b")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in oents):
            oents += [(tb, ON[bl]), (snap(tb + 0.13), ON[base])]
    oents.sort()
    opiv = (JOS_X, GY)

    def twirl(t):
        """squash flips: squeeze to a sliver at each facing cut, a lift through the spin"""
        sx, dy = 1.0, 0.0
        for tf_ in flips:
            u = t - tf_
            if -0.12 <= u < 0.12:
                sx = min(sx, 0.18 + 0.82 * abs(u) / 0.12)
        if flips[0] - 0.12 <= t < flips[-1] + 0.2:
            u = (t - flips[0] + 0.12) / (flips[-1] - flips[0] + 0.32)
            dy = -26 * SC * math.sin(math.pi * u)
        return Tf(sx=sx, dy=dy, px=JOS_X, py=GY)
    t_hop = snap(t_jo)
    hop = M.keys([(t_hop - 0.12, {"dy": 0, "sy": 1}), (t_hop, {"dy": 6, "sy": 0.96}),
                  (t_hop + 0.18, {"dy": -24, "sy": 1.03}), (t_hop + 0.38, {"dy": 0, "sy": 0.97}),
                  (t_hop + 0.52, {"dy": 0, "sy": 1})], ["in", "out", "in", "sine"], pivot=opiv)
    sc.add("joseph", jo_fr, frame_at=cuts(oents), seed=41, z=30,
           motion=M.combine(pop_motion(t_jo_pop, opiv, SC), hop, dip(t_give, SC, opiv, 6), twirl,
                            M.breathe(0.012, 2.4, pivot=opiv)))
    bnames = ["stand", "stand_b", "amazed", "cheer", "happy"]
    ben_fr = [benjamin_svg("stand", "happy"), benjamin_svg("stand", blink_name("happy")),
              benjamin_svg("stand", "amazed"), benjamin_svg("cheer", "laugh"), benjamin_svg("stand", "happy")]
    BN = {n: i for i, n in enumerate(bnames)}
    t_cheer = snap(t_pretty + 0.15)
    bents = [(0, BN["stand"]), (snap(t_cols[0] + 0.1), BN["amazed"]), (t_cheer, BN["cheer"]),
             (snap(t_cheer + 1.3), BN["happy"])]
    for tb in (pop_t[11] + 1.0, t_love + 1.5, t_eleven + 0.9, t_saw + 1.0, t_b + 0.3):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in bents):
            base = BN["happy"] if tb > t_cheer else BN["stand"]
            bents += [(tb, BN["stand_b"]), (snap(tb + 0.13), base)]
    bents.sort()
    bpiv = (BEN_X, GY)
    bh = [snap(t_cheer + 0.05 + 0.32 * k) for k in range(3)]

    def ben_hops(t):
        dy = 0.0
        for th in bh:
            u = t - th
            if 0 <= u < 0.3:
                dy -= 16 * SC * math.sin(math.pi * u / 0.3)
        return Tf(dy=dy)
    sc.add("benjamin", ben_fr, frame_at=cuts(bents), seed=47, z=31,
           motion=M.combine(pop_motion(pop_t[11], bpiv, SC), dip(snap(t_cols[0] + 0.1), SC, bpiv, 5),
                            dip(t_cheer, SC, bpiv, 6), ben_hops, M.breathe(0.014, 2.2, pivot=bpiv, phase=0.3)))

    # ------------------------------------------------------------ badges and the heart
    bx, by = BADGE

    def count(t):
        return sum(1 for tp in pop_t if t >= tp)
    t_badge_out = max(pop_t[-1] + 1.0, t_turn - 0.2)

    def badge_m(t):
        if t < pop_t[0]:
            return Tf(alpha=0)
        a = min(1.0, (t - pop_t[0]) / 0.15) * (1 - M.progress(t, t_badge_out, t_badge_out + 0.35, "sine"))
        s = 1.0
        for tp in pop_t:
            u = t - tp
            if 0 <= u < 0.16:
                s = 1 + 0.18 * math.sin(math.pi * u / 0.16)
        return Tf(sx=s, sy=s, alpha=a, dy=3 * math.sin(2 * math.pi * t / 2.6), px=bx, py=by)
    sc.add("badge", [badge_svg(n, bx, by) for n in range(13)], z=50, wc=0, frame_at=lambda t: float(count(t)),
           motion=badge_m)
    ex, ey = JOS_X, GY - 360 * SC - 40
    t_11 = snap(t_eleven - 0.05)
    t_11_out = max(t_hop + 0.6, t_give - 0.6)
    sc.add("badge11", badge_svg(11, ex, ey, r=46, size=58), z=50.1, wc=0, motion=M.combine(
        M.keys([(t_11, {"alpha": 0, "s": 0.3}), (t_11 + 0.1, {"alpha": 1}), (t_11 + 0.4, {"s": 1.0}),
                (t_11_out, {"alpha": 1, "s": 1.0}), (t_11_out + 0.3, {"alpha": 0, "s": 0.6})],
               ["out", "back", "linear", "in"], pivot=(ex, ey)),
        lambda t: Tf(dy=3 * math.sin(2 * math.pi * t / 1.9)), hop))
    hx, hy = (JAC_X + JOS_X) / 2, GY - 400 * SC
    t_heart = snap(t_love - 0.05)
    t_heart_out = t_give - 0.5

    def heart_m(t):
        if t < t_heart or t > t_heart_out + 0.4:
            return Tf(alpha=0)
        u = min(1.0, (t - t_heart) / 0.45)
        s = (0.2 + 0.8 * M.ease("back")(u)) * (1 + 0.06 * math.sin(2 * math.pi * (t - t_heart) / 0.8))
        a = 1 - M.progress(t, t_heart_out, t_heart_out + 0.4, "sine")
        return Tf(sx=s, sy=s, dy=-8 * math.sin(2 * math.pi * (t - t_heart) / 2.4) - 30 * (1 - a), alpha=a,
                  px=hx, py=hy)
    sc.add("heart", doc(heart_markup(hx, hy, 46)), z=51, wc=0, motion=heart_m)
    sc.fx.append(FX.sparkles((hx - 150, hy - 110, hx + 150, hy + 70), count=6, t0=t_heart, t1=t_heart_out,
                             size=(9, 16), period=1.3, drift=-10, seed=31))

    # ------------------------------------------------------------ sparkles: greeting, colours, the twirl
    jx, jy = JAC_X, GY
    sc.fx.append(FX.sparkles((jx - 150, jy - 400 * SC, jx + 40, jy - 220 * SC), count=5, t0=t_greet,
                             t1=t_greet + 1.2, size=(9, 16), period=1.0, drift=-12, seed=33))
    cx0, cx1 = JAC_X + 40 * SC, JAC_X + 200 * SC
    cy0, cy1 = GY - 300 * SC, GY - 60 * SC
    for k, tc in enumerate(t_cols):
        sc.fx.append(FX.sparkles((cx0, cy0, cx1, cy1), count=7, t0=tc - 0.05, t1=tc + 0.75, color=COLOR_RGB[k],
                                 size=(10, 20), period=0.7, drift=-20, seed=40 + k))
    sc.fx.append(FX.sparkles((JOS_X - 160, GY - 360 * SC, JOS_X + 160, GY - 20), count=14, t0=t_on - 0.1,
                             t1=flips[-1] + 0.9, size=(12, 24), period=0.8, drift=-24, seed=48))
    sc.add("tufts", [tufts_svg(k) for k in range(3)], z=60, frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.5) % 4]))
    sc.fx.append(FX.sparkles((100, 1000, 2000, 1150), count=6, color=(255, 250, 225), size=(7, 12), period=2.0,
                             drift=0, seed=52))

    # little birds crossing the sky
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (col, y0, vx, ph_, t0) in enumerate((("blue", 260, 80, 0.0, 0.0), ("yellow", 320, 70, 0.4, 0.0),
                                                ("red", 240, -75, 0.2, 9.0))):
        def fly(t, y0=y0, vx=vx, ph_=ph_, t0=t0, i=i):
            x = (-250 + 300 * i if vx > 0 else W + 250) + vx * (t - t0)
            return Tf(dx=x - 200, dy=y0 - 200 + 24 * math.sin(2 * math.pi * (t / 2.2 + ph_)),
                      alpha=1.0 if t >= t0 else 0.0)
        sc.add(f"bird{i}", [doc(PR.songbird(200, 200, 0.42, 1 if vx > 0 else -1, wing=w, color=col)) for w in wings],
               z=2, motion=fly, wc=0.3, frame_at=lambda t, ph_=ph_: float(int(t / 0.07 + ph_ * 8) % 8))

    # ------------------------------------------------------------ camera
    wide = Cam(W / 2, H / 2 + 8, W * 0.97)
    t_wide = t_twelve - 0.25
    t_close = t_turn + 0.1
    t_pan = t_saw - 0.05
    sc.camera = M.cam_keys([
        (0, Cam(W / 2, H / 2 + 6, W * 0.975)), (t_w0, Cam(W / 2 + 40, H / 2 + 10, W * 0.95)),
        (t_greet + 0.2, Cam(1360, 660, 1500)), (t_wide - 0.75, Cam(1340, 662, 1520)), (t_wide + 0.2, wide),
        (t_close - 0.1, Cam(W / 2 + 20, H / 2 + 8, W * 0.94)), (t_close + 1.1, Cam(1380, 708, 1180)),
        (t_give - 0.1, Cam(1370, 700, 1140)), (t_give + 1.0, Cam(1345, 716, 1000)), (t_on - 0.2, Cam(1350, 714, 980)), (t_on + 0.6, Cam(1430, 690, 1260)),
        (t_pan, Cam(1420, 688, 1270)), (t_pan + 1.3, Cam(700, 690, 1380)), (t_b - 0.2, Cam(700, 700, 1320)),
        (t_b + 1.2, Cam(760, 712, 1220)), (T, Cam(770, 714, 1200))],
        ["sine", "sine", "sine", "inout", "inout", "inout", "sine", "sine", "sine", "sine", "sine", "inout", "sine",
         "sine", "sine"])

    # ------------------------------------------------------------ sound
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-18, fade_in=0.8, fade_out=1.2)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-24, fade_in=0.8, fade_out=1.2)
    sc.sfx("sheep", 1.25, gain_db=-17, pan=0.7)
    sc.sfx("sheep", 8.75, gain_db=-19, pan=0.8)
    sc.sfx("footsteps", t_w0, dur=t_w1 - t_w0 + 0.1, gain_db=-17, pan=0.4)
    sc.sfx("chime", t_greet, gain_db=-15)
    for i, tp in enumerate(pop_t):
        xpos = order[i][0] if i < 10 else (JOS_X, BEN_X)[i - 10]
        sc.sfx("pop", tp, gain_db=-16, pan=-0.8 + 1.6 * xpos / W)
    sc.sfx("sparkle", t_heart, gain_db=-15)
    sc.sfx("pop", t_11, gain_db=-14, pan=0.4)
    sc.sfx("cloth", t_give, gain_db=-12, pan=0.2)
    for tc in t_cols:
        sc.sfx("sparkle", tc, gain_db=-17, pan=0.2)
    sc.sfx("whoosh", t_on, gain_db=-14, pan=0.3)
    sc.sfx("chime", t_on + 0.1, gain_db=-14)
    sc.sfx("cloth", sour0 + 0.1, gain_db=-17, pan=-0.3)
    sc.sfx("cloth", sour1 - 0.3, gain_db=-18, pan=-0.6)
    return sc
