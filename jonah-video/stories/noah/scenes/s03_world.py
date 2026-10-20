"""Scene 3 — long, long ago: the people on the earth grow worse and worse (Genesis 6:5-7, 11-12). A little old town
square in warm morning light; townspeople squabble in cartoon fashion while grey clouds gather; God's sorrow is
shown only as the warm light above dimming softly and one shining drop falling like a tear (God is never drawn).

Beats (phrase onsets measured in the voice clip, see s01_title.voice_marks):
  start          calm square in warm light, people standing about (breathing, blinking), clouds far away
  '很久很久以前'  slow push-in; doves flutter off a roof
  '越来越坏'      one after another the faces turn grumpy (pose cuts hidden by little dips); grey clouds start to
                 slide in from both sides
  '不听上帝的话'  a man in the back turns his back on the light, shaking his head ('no!')
  '你推我'        on the left a man pushes his neighbour, who stumbles back (whoosh)
  '我抢你'        in the middle a woman grabs the other woman's fruit basket (an apple bounces out)
  '天天吵架'      everybody crosses arms / scolds, little steam puffs rise over their heads; the clouds close in
  line 1         '上帝看见了' the camera lifts a little toward the warm light; '心里很难过' the light dims softly
                 and one shining drop falls, like a tear, and lands in the middle of the square with a tiny ring
  end            calm, greyish frame, everybody still sulking (page dip to s04)
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
from stories.noah.scenes.s01_title import char_times, cuts, dip, f1, snap, voice_marks

INK = P["ink"]
SH = 1500                  # tall stage: the sky with the warm light above the town square
G1, S1 = 1330, 1.18        # front row ground / scale
G2, S2 = 1172, 1.0         # back row
HZ = 905                   # town ground line
LIGHT = (1056, 150)
TEAR_TOP = 330
TEAR_X, TEAR_Y = 1056, 1236


def doc(body, defs=""):
    return S.svg_doc(body, defs, h=SH)


C.EXPRS.setdefault("n3_blink_neutral", dict(C.EXPRS["neutral"], eyes="closed"))
CROSS_ARMS = dict(arms=C.POSES["sit_sulk"]["arms"], hands=("fist", "fist"))


def cit(x, y, s, f, kind, variant, pose, expr=None, over=None, marks=True):
    """A townsperson in any pose of the shared rig (citizen() only offers a few)."""
    ps = dict(C.POSES[pose])
    if over:
        ps.update(over)
    e = expr or ps["expr"]
    D = C._citizen_design(kind, variant, "normal")
    m = C._ADULT
    if kind == "woman":
        m = C._metrics(C._ADULT, 0.96, 0.92)
    elif kind == "elder":
        m = C._metrics(C._ADULT, 0.97, 1.0)
    inner, _ = C._figure(D, m, ps, e, C._fsign(f), marks)
    tag = f"n3{kind}{variant}-{pose}-{e}-{'x' if over else 'o'}-{int(marks)}"
    return C._wrap_out(inner, x, y, s, f, tag)


# ================================================================== backdrop

def sky_svg():
    defs = (S.lin_grad("n3sky", [(0, "#f3d9a6"), (0.35, "#f1e2bd"), (0.7, "#cfe2e2"), (1, "#e8e6cf")]))
    return doc(S.rect_bg("url(#n3sky)", W, SH), defs)


def light_svg():
    x, y = LIGHT
    defs = S.rad_grad("n3light", [(0, "#fff6d2", 1.0), (0.3, "#ffe7a6", 0.75), (0.65, "#ffdc8e", 0.3),
                                  (1, "#ffdc8e", 0)])
    b = f'<ellipse cx="{x}" cy="{y}" rx="900" ry="640" fill="url(#n3light)"/>'
    b += f'<path d="{S.rays(x, y, 130, 900, 14, 6, rot=8)}" fill="#fff0c0" opacity="0.4" filter="url(#soft)"/>'
    return doc(b, defs)


def gloom_svg():
    return doc(f'<rect x="-20" y="-20" width="{W + 40}" height="{SH + 40}" fill="#9aa3b4"/>')


def far_svg():
    b = S.path(S.hill(-200, W + 200, HZ - 10, 130, seed=31, bumps=4, bottom=SH + 60), fill="#cfd6c0", sw=2.2)
    town = ""
    rng = random.Random(4)
    xs = [140, 360, 560, 800, 1300, 1520, 1720, 1940]
    for i, x in enumerate(xs):
        town += PR.house(x, HZ + 25 + rng.uniform(-8, 8), 0.4 + rng.uniform(-0.03, 0.03), variant=i % 4,
                         facing=1 if i % 2 else -1)
    for x in (260, 1040, 1630, 2060):
        town += PR.palm_tree(x, HZ + 40, 0.55, lean=0.15 if x % 2 else -0.15)
    return doc(S.g(b, filter="wobble") + PR._haze(town, "#e6dcc0", 0.35, 0.4))


def square_svg():
    defs = S.lin_grad("n3gr", [(0, "#e2c690"), (1, "#c9a46c")])
    d = S.smooth_path([(-100, HZ + 45), (500, HZ + 35), (1100, HZ + 47), (1700, HZ + 33), (W + 100, HZ + 43)],
                      closed=False)
    b = S.path(d + f" L{W + 100},{SH + 60} L-100,{SH + 60} Z", fill="url(#n3gr)", sw=3.5)
    rng = random.Random(9)
    for _ in range(50):
        x, y = rng.uniform(0, W), rng.uniform(HZ + 80, SH)
        r = rng.uniform(5, 12) * (0.6 + (y - HZ) / 450)
        b += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.6)}" ry="{f1(r * 0.8)}" fill="#d7b98a" '
              f'stroke="{INK}" stroke-width="1.8" opacity="0.8"/>')
    b = S.g(b, filter="wobble")
    # a little market stall and things lying about
    st = ""
    k = 1.25
    sx, sy = 70, 1110
    st += (f'<rect x="{sx}" y="{sy - 170}" width="16" height="170" fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
           f'<rect x="{sx + 300}" y="{sy - 170}" width="16" height="170" fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M{sx - 30},{sy - 160} L{sx + 346},{sy - 160} L{sx + 320},{sy - 220} L{sx - 4},{sy - 220} Z" '
           f'fill="#d36d4e" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    for k in range(6):
        st += (f'<path d="M{sx - 30 + k * 63},{sy - 160} q31,26 63,0" fill="#f3e4c6" stroke="{INK}" '
               f'stroke-width="3"/>')
    st += (f'<rect x="{sx - 10}" y="{sy - 70}" width="336" height="70" fill="#b98a58" stroke="{INK}" stroke-width="3"/>')
    b += S.g(st, filter="wobble-fine")
    b += PR.food_basket(sx + 70, sy - 66, 0.55, "fruit") + PR.food_basket(sx + 170, sy - 66, 0.55, "veg")
    b += PR.food_basket(sx + 260, sy - 66, 0.5, "bread")
    b += PR.jar(1990, 1110, 0.75) + PR.jar(2070, 1125, 0.62) + PR.sack(1905, 1140, 0.75, seed=2)
    b += PR.crate(690, 1105, 0.7) + PR.sack(590, 1118, 0.7, seed=5)
    b += PR.bush(1560, HZ + 70, 0.6, variant=2) + PR.bush(940, HZ + 64, 0.55, variant=0)
    return doc(b, defs)


def cloud_svg(x, y, s, w, h, seed, light):
    return doc(PR.dark_cloud(x, y, s, width=w, height=h, seed=seed, light=light))


def doves_svg(k, sx=800, sy=HZ - 190):
    out = ""
    for i, (dx, dy) in enumerate(((0, 0), (70, -30))):
        w = (1, 0, -1, 0)[(k + i * 2) % 4]
        out += PR.dove(sx + dx, sy + dy, 0.45, 1, wing=w)
    return doc(out)


FG = [(40, SH, 1.2, 1), (760, SH + 4, 1.0, 1), (1500, SH + 2, 1.1, 1), (2080, SH - 2, 1.2, 1), (1120, SH + 6, 0.8, 0)]


def fg_svg(k):
    out = ""
    for x, y, s, v in FG:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.4 * math.sin(k * 2.1 + x * 0.01))
    return doc(out)


# ================================================================== people

def person_frames(spec, frames):
    """frames: list of (pose, expr, over, marks) -> list of SVG docs (with contact shadow)."""
    x, y, s, f, kind, v = spec
    out = []
    for pose, expr, over, marks in frames:
        out.append(doc(C.ground_shadow(x, y + 2, s, 130, 0.2) + cit(x, y, s, f, kind, v, pose, expr, over, marks)))
    return out


def basket_svg(x, y, s=0.62):
    return doc(PR.food_basket(x, y, s, "fruit"))


def apple_svg(x, y):
    return doc(f'<g transform="translate({f1(x)},{f1(y)})" filter="url(#wobble-fine)"><circle cx="0" cy="0" r="15" '
               f'fill="#d9483b" stroke="{INK}" stroke-width="3"/><path d="M0,-14 q2,-10 8,-12" stroke="{INK}" '
               f'stroke-width="3" fill="none"/><ellipse cx="9" cy="-17" rx="7" ry="4" fill="#7fae5a" stroke="{INK}" '
               f'stroke-width="2"/><circle cx="-5" cy="-5" r="4" fill="#f08a7a"/></g>')


def puff_svg(x, y, s):
    return doc(S.g(S.cloud(x, y, 70 * s, 42 * s, "#f2eee6", seed=int(x) % 97, puffs=3, sw=3 * s,
                           shade_fill="#d8d2c8"), filter="wobble-fine"))


def tear_svg(r=24):
    defs = (S.lin_grad("n3tear", [(0, "#fffbe8"), (0.5, "#d8f0f6"), (1, "#9fd2e6")]) +
            S.rad_grad("n3tglow", [(0, "#fff3c4", 0.9), (0.5, "#ffe9a6", 0.35), (1, "#ffe9a6", 0)]))
    x, y = 0, 0
    d = f"M{x},{y - r * 2.2} C{x + r * 0.4},{y - r * 1.2} {x + r},{y - r * 0.4} {x + r},{y + r * 0.2} " \
        f"A{r},{r} 0 0 1 {x - r},{y + r * 0.2} C{x - r},{y - r * 0.4} {x - r * 0.4},{y - r * 1.2} {x},{y - r * 2.2} Z"
    b = (f'<circle cx="{x}" cy="{y - r * 0.4}" r="{r * 3.4}" fill="url(#n3tglow)"/>'
         f'<path d="{d}" fill="url(#n3tear)" stroke="{P["ink_soft"]}" stroke-width="3" stroke-linejoin="round"/>'
         f'<ellipse cx="{x - r * 0.38}" cy="{y - r * 0.15}" rx="{r * 0.22}" ry="{r * 0.36}" fill="#fffaf0"/>')
    return doc(f'<g transform="translate({TEAR_X},{TEAR_TOP})">{b}</g>', defs)


def ring_svg():
    return doc(f'<ellipse cx="{TEAR_X}" cy="{TEAR_Y}" rx="80" ry="20" fill="none" stroke="#fff4cc" stroke-width="6"/>'
               f'<ellipse cx="{TEAR_X}" cy="{TEAR_Y}" rx="46" ry="11" fill="#e9f4f2" opacity="0.6"/>')


# ================================================================== build

def build(ctx):
    sc = Scene(ctx, W=W, H=SH)
    T = ctx.duration
    m0 = voice_marks(ctx, 0)
    m1 = voice_marks(ctx, 1)
    names = [m[0] for m in m0]

    def at(i, default):
        return m0[i][1] if len(m0) > i else default
    t_long = at(0, ctx.lines[0].start)
    t_bad = at(1, t_long + 1.6)
    bad_c = char_times(m0[1]) if len(m0) > 1 else [t_bad + 0.15 * k for k in range(8)]
    t_worse = bad_c[min(4, len(bad_c) - 1)]                       # '越来越坏'
    t_god = at(2, t_bad + 2.0)
    t_push = at(3, t_god + 1.7)
    t_grab = at(4, t_push + 1.0)
    t_fight = at(5, t_grab + 0.9)
    t_saw = m1[0][1]
    t_sad = m1[1][1] if len(m1) > 1 else t_saw + 1.3
    t_dim0, t_dim1 = t_sad - 0.2, t_sad + 1.3
    t_tear0 = t_sad + 0.25
    t_tear1 = t_tear0 + 1.25

    # ---- sky, light and clouds
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("light", light_svg(), z=0.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(0.95 + 0.05 * math.sin(2 * math.pi * t / 3.0)) *
                               (1 - 0.68 * M.progress(t, t_dim0, t_dim1, "sine"))))
    clouds = [  # (x, y, scale, w, h, seed, light, from_dx, t_start, t_end)
        (230, 300, 1.05, 700, 250, 1, 0.7, -950, t_bad, t_fight + 0.6),
        (1890, 320, 1.05, 680, 240, 2, 0.75, 950, t_bad + 0.3, t_fight + 0.8),
        (600, 520, 0.8, 600, 200, 3, 0.9, -1150, t_worse, t_fight + 1.2),
        (1530, 510, 0.8, 620, 210, 4, 0.85, 1150, t_worse + 0.2, t_fight + 1.4),
    ]
    for i, (x, y, s, w, h, sd, li, fdx, ta, tb) in enumerate(clouds):
        def cm(t, fdx=fdx, ta=ta, tb=tb, i=i):
            u = M.progress(t, ta, tb + 1.0, "sine")
            return Tf(dx=fdx * (1 - u) + 10 * math.sin(2 * math.pi * (t / 7.0 + i * 0.3)),
                      dy=4 * math.sin(2 * math.pi * (t / 5.0 + i * 0.2)))
        sc.add(f"cloud{i}", cloud_svg(x, y, s, w, h, sd, li), z=1 + i * 0.01, motion=cm, wc=0.6)
    sc.add("far", far_svg(), z=2)
    # doves on a roof fly off on '很久很久以前'
    t_dove = t_long + 0.4

    def dove_m(t):
        u = max(0.0, t - t_dove)
        return Tf(dx=260 * u + 20 * u * u, dy=-110 * u - 8 * u * u, alpha=1 - M.progress(t, t_dove + 2.6, t_dove + 3.2))
    sc.add("doves", [doves_svg(k) for k in range(4)], z=2.2, motion=dove_m, wc=0.5,
           frame_at=lambda t: 0.0 if t < t_dove else float(int((t - t_dove) / 0.08) % 4))
    sc.add("square", square_svg(), z=3)

    # ---- people
    A = (330, G1, S1, 1, "man", 0)
    B = (538, G1, S1, -1, "man", 3)
    Gm = (790, G2, S2, 1, "man", 1)
    D_ = (1290, G1, S1, 1, "woman", 2)
    Cw = (1498, G1, S1, -1, "woman", 1)
    E = (1700, G2, S2, 1, "elder", 0)
    F = (1872, G2, S2, -1, "man", 2)
    blink = "n3_blink_neutral"

    def stagger(i):
        return snap(t_worse + 0.16 * i)

    def add_person(name, spec, frames, ents, extra=None, blinks=(), z=5.0):
        x, y, s = spec[0], spec[1], spec[2]
        piv = (x, y)
        ents = sorted(ents)
        for tb in blinks:
            tb = snap(tb)
            cur = None
            for tk, i in ents:
                if tk <= tb:
                    cur = i
            if cur == 0 and all(abs(tb - tk) > 0.35 for tk, _ in ents):
                ents += [(tb, len(frames)), (snap(tb + 0.13), 0)]
        fr = person_frames(spec, frames + ([("stand", blink, None, True)] if blinks else []))
        dips = [dip(tk, s, piv, 8) for tk, _ in sorted(ents)[1:]]
        mot = M.combine(M.breathe(0.012, 2.7, pivot=piv, phase=(x % 7) / 7), *dips, *(extra or []))
        sc.add(name, fr, z=z + (y - 1100) / 1000 + x / 100000, frame_at=cuts(sorted(ents)), motion=mot,
               seed=int(x) % 50 + 40)

    # A pushes B
    t_p = snap(t_push - 0.05)
    add_person("A", A, [("stand", "neutral", None, True), ("stand", "cross", None, True),
                        ("push", "shout", None, True), ("el_hips", "cross", None, True)],
               [(0, 0), (stagger(0), 1), (t_p, 2), (snap(t_push + 0.7), 3)], blinks=(1.4,))
    t_b = snap(t_push + 0.1)
    bx = B[0]

    def stumble(t):
        u = t - t_b
        if u < 0:
            return Tf()
        back = 70 * M.progress(t, t_b, t_b + 0.35, "out") - 70 * M.progress(t, t_b + 1.0, t_b + 1.5, "sine")
        hop_ = -22 * math.sin(math.pi * min(1.0, u / 0.35)) if u < 0.35 else 0.0
        rot = 9 * M.progress(t, t_b, t_b + 0.2, "out") * (1 - M.progress(t, t_b + 0.5, t_b + 0.9, "sine"))
        return Tf(dx=back, dy=hop_, rot=rot, px=bx, py=G1)
    add_person("B", B, [("stand", "neutral", None, True), ("stand", "cross", None, True),
                        ("scared", "surprised", None, False), ("el_scold", "cross", None, True),
                        ("stand", "cross", CROSS_ARMS, True)],
               [(0, 0), (stagger(2), 1), (t_b, 2), (snap(t_b + 0.95), 3), (snap(t_fight + 0.05), 4)],
               extra=[stumble], blinks=(2.0,))
    # G turns his back on the light: 'no!'
    add_person("G", Gm, [("stand", "neutral", None, True), ("stand", "cross", None, True),
                         ("refuse", "cross", None, True), ("stand", "cross", CROSS_ARMS, True)],
               [(0, 0), (stagger(1), 1), (snap(t_god + 0.3), 2), (snap(t_fight + 0.12), 3)], blinks=(0.7,), z=4.0)
    # D grabs C's basket
    t_g = snap(t_grab - 0.05)
    t_g2 = snap(t_grab + 0.32)
    add_person("D", D_, [("stand", "neutral", None, True), ("stand", "cross", None, True),
                         ("reach_out", "sly", None, True), ("dv_carry_basket", "smug", None, True)],
               [(0, 0), (stagger(3), 1), (t_g, 2), (t_g2, 3)], blinks=(1.9,))
    add_person("C", Cw, [("dv_carry_basket", "neutral", None, True), ("dv_carry_basket", "cross", None, True),
                         ("reach_out", "shout", None, True), ("el_scold", "cross", None, True)],
               [(0, 0), (stagger(4), 1), (t_g2, 2), (snap(t_fight + 0.2), 3)])
    # E and F scold each other, then cross arms
    add_person("E", E, [("stand", "neutral", None, True), ("el_scold", "cross", None, True),
                        ("stand", "cross", CROSS_ARMS, True)],
               [(0, 0), (stagger(5), 1), (snap(t_fight + 0.08), 2)], blinks=(1.1,), z=4.0)
    add_person("F", F, [("stand", "neutral", None, True), ("el_scold", "shout", None, True),
                        ("el_hips", "cross", None, True)],
               [(0, 0), (stagger(6), 1), (snap(t_fight + 0.16), 2)], blinks=(2.4,), z=4.0)

    # the basket: in C's hands, flies to D's on '我抢你'
    def hands_mid(spec, pose):
        x, y, s, f, kind, v = spec
        hp = C.body_points(lambda X, Y, S_, F_, **kw: cit(X, Y, S_, F_, kind, v, pose), x, y, s, f)["hands"]
        return ((hp[0][0] + hp[1][0]) / 2, (hp[0][1] + hp[1][1]) / 2)
    hc = hands_mid(Cw, "dv_carry_basket")
    hd = hands_mid(D_, "dv_carry_basket")
    bs = 0.8
    base = (hc[0], hc[1] + 44 * bs)

    def basket_m(t):
        u = M.progress(t, t_g, t_g2, "inout")
        dx = (hd[0] - hc[0]) * u
        dy = (hd[1] - hc[1]) * u - 40 * math.sin(math.pi * u)
        rot = -14 * math.sin(math.pi * u)
        brth = 2.0 * math.sin(2 * math.pi * t / 2.7)
        return Tf(dx=dx, dy=dy + brth, rot=rot, px=base[0], py=base[1])
    sc.add("basket", basket_svg(*base, bs), z=5.6, motion=basket_m, seed=91)
    # an apple bounces out of the basket
    t_ap = t_g + 0.12
    ax0, ay0 = (hc[0] + hd[0]) / 2, hc[1] - 30
    ax1, ay1 = ax0 + 70, G1 + 6

    def apple_m(t):
        if t < t_ap:
            return Tf(alpha=0)
        u = t - t_ap
        x = ax0 + min(u, 1.2) * 75
        if u < 0.55:
            k = u / 0.55
            y = ay0 + (ay1 - ay0) * k * k - 60 * math.sin(math.pi * k) * (1 - k)
        elif u < 0.9:
            k = (u - 0.55) / 0.35
            y = ay1 - 34 * math.sin(math.pi * k)
        elif u < 1.12:
            k = (u - 0.9) / 0.22
            y = ay1 - 10 * math.sin(math.pi * k)
        else:
            y = ay1
        return Tf(dx=x - ax0, dy=y - 15 - ay0, rot=min(u, 1.2) * 300, px=ax0, py=ay0)
    sc.add("apple", apple_svg(ax0, ay0), z=6.2, motion=apple_m, wc=0.5)

    # steam puffs over the quarrellers on '天天吵架'
    heads = []
    for spec in (A, B, Gm, D_, Cw, E, F):
        x, y, s = spec[0], spec[1], spec[2]
        heads.append((x + 10 * spec[3] * s, y - 370 * s, s))
    for i, (hx, hy, s) in enumerate(heads):
        for j in range(2):
            per = 1.3
            off = (i * 0.37 + j * 0.5) % 1

            def pm(t, off=off, per=per, i=i, j=j, hx=hx, hy=hy):
                t0 = t_fight + 0.1 + 0.08 * i
                if t < t0:
                    return Tf(alpha=0)
                u = ((t - t0) / per + off) % 1.0
                a = math.sin(math.pi * u) * min(1.0, (t - t0) / 0.3)
                sc_ = 0.6 + 0.7 * u
                return Tf(dx=(18 if j else -18) * u, dy=-90 * u, sx=sc_, sy=sc_, alpha=a, px=hx, py=hy)
            sc.add(f"puff{i}_{j}", puff_svg(hx, hy, s), z=6.5, motion=pm, wc=0)

    sc.add("fg", [fg_svg(k) for k in range(3)], z=7, frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.55) % 4]))

    # ---- gloom over everything as the light dims
    sc.add("gloom", gloom_svg(), z=8, wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=0.18 * M.progress(t, t_bad, t_fight + 1.0, "sine") +
                               0.22 * M.progress(t, t_dim0, t_dim1, "sine")))

    # ---- the tear
    def tear_m(t):
        if t < t_tear0 - 0.3:
            return Tf(alpha=0)
        a = M.progress(t, t_tear0 - 0.3, t_tear0, "sine") * (1 - M.progress(t, t_tear1 - 0.05, t_tear1 + 0.1))
        u = M.progress(t, t_tear0, t_tear1, "in")
        y = (TEAR_Y - TEAR_TOP - 8) * u
        sway = 6 * math.sin(2 * math.pi * (t - t_tear0) / 1.1) * (1 - u)
        return Tf(dx=sway, dy=y, alpha=a)
    sc.add("tear", tear_svg(), z=9, motion=tear_m, wc=0)

    def ring_m(t):
        u = M.progress(t, t_tear1, t_tear1 + 1.0, "out")
        if t < t_tear1:
            return Tf(alpha=0)
        return Tf(sx=0.4 + 1.6 * u, sy=0.4 + 1.6 * u, alpha=1 - u, px=TEAR_X, py=TEAR_Y)
    sc.add("ring", ring_svg(), z=8.5, motion=ring_m, wc=0)
    sc.fx.append(FX.sparkles((TEAR_X - 50, TEAR_Y - 70, TEAR_X + 50, TEAR_Y - 10), count=5, t0=t_tear1,
                             t1=t_tear1 + 1.4, size=(8, 16), period=1.0, drift=-25, seed=21))
    sc.fx.append(FX.sparkles((LIGHT[0] - 420, 120, LIGHT[0] + 420, 400), count=10, t0=0, t1=t_dim1,
                             size=(8, 15), period=2.0, drift=0, seed=23))

    # ---- camera
    sc.camera = M.cam_keys([(0, Cam(W / 2, 880, W * 0.99)), (t_push - 0.5, Cam(1050, 940, 1980)),
                            (t_fight + 0.6, Cam(1056, 935, 2000)), (t_saw + 0.1, Cam(1056, 935, 2000)),
                            (t_sad + 0.4, Cam(1056, 720, 2080)), (T, Cam(1056, 716, 2070))],
                           ["sine", "sine", "sine", "sine", "sine"])

    # ---- sound
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", t_bad, dur=t_saw - t_bad + 0.8, gain_db=-22, fade_in=1.0, fade_out=1.2)
    sc.sfx("birds", 0, dur=t_bad + 1.0, gain_db=-21, fade_in=0.6, fade_out=1.0)
    sc.sfx("whoosh", t_push - 0.02, gain_db=-14, pan=-0.6)
    sc.sfx("thud", t_b + 0.3, gain_db=-14, pan=-0.5)
    sc.sfx("whoosh", t_grab, gain_db=-15, pan=0.2)
    sc.sfx("pop", t_ap + 0.55, gain_db=-17, pan=0.2)
    sc.sfx("cloth", t_fight + 0.05, gain_db=-16)
    sc.sfx("chime", t_tear0 - 0.1, gain_db=-17)
    sc.sfx("drip", t_tear1 - 0.05, dur=0.8, gain_db=-12)
    return sc
