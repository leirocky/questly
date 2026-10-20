"""Scene 5 — God tells Noah to build the ark (Genesis 6:13-22).

"有一天，上帝对挪亚说：" / G "挪亚，地上就要发大水了。你要造一只很大很大的船，叫方舟。" / G "你和你的家人都要进去，还要把各样的
动物带进去，一公一母，两个两个地来。" / "挪亚心想：一只大船？可是，这里离大海好远好远啊！" / "可是，挪亚还是照着上帝说的，一样一样
都去做了。"

One 2800 x 1575 stage: evening on Noah's hill. Golden-grass hills roll away to purple mountains on every side - dry
land, no water anywhere; an olive tree, rocks, a tree stump with a saw lying on it, the sun going down on the right.

  line 0  "有一天，上帝对挪亚说："  golden rays come down from above (God is only ever light); Noah looks up, amazed.
  line 1  "地上就要发大水了。"      a glowing golden picture appears in the sky like a drawing: wavy water lines;
          "你要造一只很大很大的船，" the ark is drawn in gold above the waves (wipe), and grows on "很大很大";
          "叫方舟。"                a golden label 方舟 pops under it.
  line 2  "你和你的家人都要进去，"  the family of eight appears as a golden drawing beside the ramp;
          "还要把各样的动物…"       golden pairs pop in one by one (elephants, giraffes, rabbits, doves);
          "一公一母，"              each pair bobs (he and she, the she with her bow);
          "两个两个地来。"          the whole procession shuffles toward the ramp of the golden ark.
  line 3  the picture and the rays fade. "一只大船？" Noah looks left, looks right, scratches his head ('?');
          "这里离大海好远好远啊！"  the camera pulls back over the dry hills; a little round inset shows the sea far,
                                    far away at the end of a long dotted road.
  line 4  "可是，挪亚还是照着…"     he nods firmly three times (determined);
          "一样一样都去做了。"      he rolls up his sleeves, reaches to the stump and lifts the saw. Calm last frame.
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
from stories.daniel.scenes.s05_prays import clamp
from stories.david.scenes.s08_saul import Actor, clamp_cam, pop_tf, pt, rays_svg, sparkle_dyn, sprite
from stories.noah.scenes.s04_noah import cycle, fam, fam_custom, flowers, glow_svg, grass_strokes

INK = P["ink"]
SW, SH = 2800, 1575
GY = 1290
K = 1.4
XN = 560                       # Noah's spot on the hill top
STUMP = (XN + 225, GY - 6)     # the tree stump with the saw on it (bottom centre)
TINT = "#e6c9c0"               # evening haze
GOLD = "#ffe2a0"


def f1(v):
    return f"{v:.1f}"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


# ================================================================== the golden sky drawing
def gold(markup, k=0.84):
    return PR._haze(markup, GOLD, k, 0.55)


def golden(markup, glow=0.75):
    """A glowing golden line drawing of markup (a soft blurred halo under a gilded copy)."""
    halo = PR._haze(markup, "#ffd36e", 1.0, 1.0)
    return doc(f'<g filter="url(#blur-md)" opacity="{glow}">{halo}</g>' + gold(markup))


ARK = (1450, 700, 0.42)        # sky ark: keel x, keel y, scale
FAM0 = 1905                    # the golden family line: Noah (leading) x
PAIRS = (("elephant", 2390), ("giraffe", 2615), ("rabbit", 2745))


def waves_svg():
    out = ""
    for i, (y, a, wl, ph) in enumerate(((735, 16, 170, 0.0), (770, 14, 150, 1.7), (805, 12, 190, 0.8))):
        d = S.wave_line(y, a, wl, ph, x0=960, x1=2650)
        out += f'<path d="{d}" fill="none" stroke="#c78a2a" stroke-width="{7 - i}" stroke-linecap="round"/>'
        out += f'<path d="{d}" fill="none" stroke="#fff3c8" stroke-width="{3 - 0.6 * i}" stroke-linecap="round"/>'
    return doc(f'<g filter="url(#blur-md)" opacity="0.8">{out}</g>' + S.g(out, filter="wobble-fine"))


def ark_draw():
    x, y, s = ARK
    return golden(PR.ark(x, y, s, ramp=True))


def label_svg():
    x, y = ARK[0], ARK[1] + 95
    return doc(f'<g filter="url(#blur-md)" opacity="0.7">{S.text(x, y, "方舟", size=96, fill="#ffd36e")}</g>'
               + S.text(x, y, "方舟", size=104, fill="#fff3c8",
                        extra='stroke="#b9781f" stroke-width="9" stroke-linejoin="round" paint-order="stroke"'))


def family_draw():
    return golden(C.noah_family(FAM0, ARK[1], ARK[2], -1, pose="walk_a", gap=110, marks=False), 0.6)


def pair_draw(kind, x, phase=0):
    pose = "walk_a" if phase == 0 else "walk_b"
    return golden(PR.animal_pair(kind, x, ARK[1], ARK[2], -1, pose=pose), 0.6)


def doves_draw(w):
    return golden(PR.animal_pair("dove", 2250, 420, ARK[2] * 1.3, -1, phase=w), 0.6)


# ================================================================== backdrop (evening, dry hills)
def sky_svg():
    defs = (S.lin_grad("s5sky", [(0, "#8d8cc0"), (0.38, "#d7a3b4"), (0.66, "#f2b98e"), (0.85, "#f8d698"),
                                 (1, "#f9e2b0")])
            + S.rad_grad("s5sun", [(0, "#fff3cc", 0.95), (0.3, "#ffd99a", 0.55), (1, "#f8c38a", 0)]))
    body = S.rect_bg("url(#s5sky)", SW, SH)
    body += '<ellipse cx="2380" cy="900" rx="900" ry="520" fill="url(#s5sun)"/>'
    body += S.g(f'<circle cx="2380" cy="905" r="88" fill="#fbcf6a" stroke="{S.mix(P["sun_hot"], INK, 0.35)}" '
                f'stroke-width="5"/><circle cx="2350" cy="878" r="28" fill="#fff4cc" opacity="0.6"/>',
                filter="wobble-fine")
    # long soft evening cloud streaks
    for x, y, w, h, c in ((520, 300, 620, 34, "#e9b9c0"), (1800, 210, 760, 30, "#efc3c3"), (2300, 560, 520, 26, "#f6cfa8"),
                          (900, 620, 480, 22, "#f3c9b0")):
        body += (f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{h}" fill="{c}" opacity="0.75"/>'
                 f'<ellipse cx="{x - 40}" cy="{y - 12}" rx="{w / 2.6}" ry="{h * 0.6}" fill="#fbe6d6" opacity="0.6"/>')
    return doc(body, defs)


def far_svg():
    m1 = S.mix("#8f84ad", TINT, 0.25)
    m2 = S.mix("#a497b5", TINT, 0.35)
    body = S.path(S.hill(-200, 1300, 960, 330, seed=3, bumps=3, bottom=1300), fill=m2, sw=2.6)
    body += S.path(S.hill(1000, 3000, 950, 260, seed=12, bumps=4, bottom=1300), fill=m2, sw=2.6)
    body += S.path(S.hill(400, 2000, 990, 200, seed=5, bumps=3, bottom=1300), fill=m1, sw=2.6)
    out = S.g(body, filter="wobble")
    # snowy tips on the farthest peaks (inland, far from any sea)
    # rolling dry golden hills receding
    h1 = S.mix("#d4b06a", TINT, 0.35)
    h2 = S.mix("#c9a85e", TINT, 0.2)
    out += S.g(S.path(S.hill(-200, 3000, 1030, 110, seed=8, bumps=6, bottom=1400), fill=h1, sw=2.6)
               + S.path(S.hill(-300, 3100, 1085, 120, seed=2, bumps=6, bottom=1400), fill=h2, sw=2.6), filter="wobble")
    rng = random.Random(4)
    trees = ""
    for i in range(16):
        x = rng.uniform(950, 2780)
        trees += PR.olive_tree(x, 1060 + rng.uniform(-25, 40), rng.uniform(0.12, 0.18), seed=i)
    for i in range(5):
        x = rng.uniform(1100, 2700)
        trees += PR.sheep(x, 1100 + rng.uniform(0, 50), 0.16, 1 if i % 2 else -1, variant=i % 4, pose="graze")
    out += PR._haze(trees, TINT, 0.4, 0.35)
    # a winding dusty road into the distance (no water anywhere)
    out += (f'<path d="M1150,1400 C1500,1300 1300,1200 1700,1150 S2150,1090 2400,1060 S2700,1040 2900,1035" fill="none" '
            f'stroke="#e8cf9a" stroke-width="44" stroke-linecap="round" opacity="0.6"/>')
    return doc(out)


def hill_svg():
    defs = S.lin_grad("s5hill", [(0, "#b8b45e"), (0.4, "#a5a650"), (1, "#8e9446")])
    pts = [(-60, 1180), (200, 1150), (500, 1135), (800, 1150), (1050, 1185), (1300, 1250), (1600, 1330), (1950, 1390),
           (2400, 1430), (2860, 1450)]
    d = S.smooth_path(pts, closed=False) + f" L2860,{SH + 40} L-60,{SH + 40} Z"
    out = f'<path d="{d}" fill="url(#s5hill)" stroke="{INK}" stroke-width="5"/>'
    rng = random.Random(9)
    out += grass_strokes(rng, 60, 0, 1500, 1180, SH, "#7b7f3a")
    out += grass_strokes(rng, 30, 1400, SW, 1380, SH, "#7b7f3a")
    out += f'<ellipse cx="620" cy="1300" rx="460" ry="60" fill="#d8c97e" opacity="0.45"/>'
    out += flowers(rng, 14, 50, 1300, 1200, 1450, 0.9)
    # rocks
    for x, y, rx, ry in ((1130, 1320, 70, 40), (1210, 1340, 40, 24), (130, 1260, 60, 34)):
        out += S.path(S.blob(x, y, rx, ry, 0.12, 9, seed=x), fill="#c9b79a", sw=4)
        out += f'<ellipse cx="{x - rx * 0.3}" cy="{y - ry * 0.4}" rx="{rx * 0.4}" ry="{ry * 0.25}" fill="#fff4e0" opacity="0.5"/>'
    return doc(S.g(out, filter="wobble"), defs)


def props_svg():
    out = PR.olive_tree(150, GY - 70, 1.15, seed=6)
    out += PR.bush(1000, GY - 40, 0.6, variant=2)
    # the tree stump (bottom centre STUMP), top at STUMP y - 92
    x, y = STUMP
    top = y - 92
    st = (f'<path d="M{x - 70},{y} C{x - 62},{y - 40} {x - 60},{top + 20} {x - 58},{top} L{x + 58},{top} '
          f'C{x + 60},{top + 20} {x + 62},{y - 40} {x + 74},{y} Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M{x - 92},{y + 2} q20,-20 30,-8 M{x + 94},{y + 2} q-22,-20 -30,-8" fill="none" stroke="{INK}" '
          f'stroke-width="5" stroke-linecap="round"/>'
          f'<ellipse cx="{x}" cy="{top}" rx="58" ry="18" fill="{P["wood_light"]}" stroke="{INK}" stroke-width="5"/>'
          f'<ellipse cx="{x}" cy="{top}" rx="34" ry="10" fill="none" stroke="{P["wood"]}" stroke-width="3"/>'
          f'<ellipse cx="{x}" cy="{top}" rx="14" ry="4" fill="none" stroke="{P["wood"]}" stroke-width="3"/>'
          f'<path d="M{x - 30},{y - 20} l0,-40 M{x + 20},{y - 14} l0,-46" stroke="{P["wood_dark"]}" stroke-width="3" '
          f'opacity="0.6"/>')
    out += S.g(st, filter="wobble-fine")
    out += PR.grass_tuft(x + 90, y + 10, 0.8, variant=1)
    out += PR.grass_tuft(x - 100, y + 8, 0.7, variant=0)
    return doc(out)


def saw_on_stump():
    x, y = STUMP
    return doc(PR.saw(x - 70, y - 100, 0.95, 1, rot=-4))


def fg_svg(sway=0.0):
    out = ""
    for x, y, s, v in ((60, SH + 20, 1.6, 1), (380, SH + 40, 1.3, 0), (1480, SH + 40, 1.4, 1), (2150, SH + 30, 1.5, 2),
                       (2700, SH + 30, 1.4, 1)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sway)
    return doc(out)


# ================================================================== little overlays
def inset_svg(cx, cy, r):
    """A round picture-book inset: the sea, far, far away at the end of a long road over dry hills."""
    uid = "s5ins"
    defs = (S.lin_grad(uid + "s", [(0, "#a7d3e6"), (0.6, "#d8ecef"), (1, "#f5e8c8")])
            + f'<clipPath id="{uid}c"><circle cx="{cx}" cy="{cy}" r="{r - 10}"/></clipPath>')
    inner = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#{uid}s)"/>'
    hz = cy - 20
    # the sea: a thin blue band on the horizon with a tiny sail and a gull
    inner += f'<rect x="{cx - r}" y="{hz - 6}" width="{2 * r}" height="30" fill="#5a9fc2"/>'
    inner += f'<path d="{S.wave_line(hz - 6, 3, 40, 0, cx - r, cx + r)}" fill="none" stroke="#e8f6f6" stroke-width="3"/>'
    inner += (f'<path d="M{cx + 70},{hz - 4} l26,0 l-6,8 l-16,0 Z M{cx + 82},{hz - 6} l0,-30 l14,26 Z" fill="#fff4e0" '
              f'stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    inner += (f'<path d="M{cx - 60},{hz - 60} q8,-8 16,0 q8,-8 16,0" fill="none" stroke="{INK}" stroke-width="3" '
              f'stroke-linecap="round"/>')
    # dry hills in front, and a long road winding toward the sea
    inner += S.path(S.hill(cx - r - 20, cx + r + 20, hz + 40, 30, seed=3, bumps=3, bottom=cy + r + 20), fill="#d6b56c",
                    sw=3)
    inner += S.path(S.hill(cx - r - 20, cx + r + 20, hz + 110, 40, seed=6, bumps=2, bottom=cy + r + 20),
                    fill="#c3a95c", sw=3)
    inner += (f'<path d="M{cx - 40},{cy + r} C{cx - 20},{cy + 120} {cx + 60},{cy + 100} {cx + 20},{hz + 70} '
              f'S{cx + 10},{hz + 30} {cx + 30},{hz + 18}" fill="none" stroke="#efdcae" stroke-width="22" '
              f'stroke-linecap="round"/>')
    out = f'<g clip-path="url(#{uid}c)">{inner}</g>'
    out += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 10}" fill="none" stroke="#e8c062" stroke-width="5"/>')
    return S.g(out, filter="wobble-fine"), defs


def far_arrow_svg(x0, y0, x1, y1):
    """A long dotted road-arrow from Noah's hill toward the inset: 好远好远."""
    pts = [(M.lerp(x0, x1, u), M.lerp(y0, y1, u) - 160 * math.sin(math.pi * u)) for u in [k / 24 for k in range(25)]]
    d = S.smooth_path(pts, closed=False)
    col = S.mix(P["sun_hot"], INK, 0.35)
    out = (f'<path d="{d}" fill="none" stroke="#fff4dc" stroke-width="14" stroke-linecap="round" opacity="0.7"/>'
           f'<path d="{d}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round" stroke-dasharray="4 22"/>')
    ax, ay = pts[-1]
    bx, by = pts[-3]
    a = math.atan2(ay - by, ax - bx)
    for s_ in (1, -1):
        out += (f'<path d="M{f1(ax)},{f1(ay)} l{f1(-34 * math.cos(a + s_ * 0.5))},{f1(-34 * math.sin(a + s_ * 0.5))}" '
                f'stroke="{col}" stroke-width="8" stroke-linecap="round"/>')
    return doc(out)


# ================================================================== Noah drawings
_P = C._P
LOOK = _P(h=-14, arms=(("fk", 14, 8), ("fk", -8, -3)), look=(0.03, -0.09), expr="amazed")
# rolling up a sleeve: the far forearm raised in front, the near hand tugging its cuff from the wrist (A) to the elbow (B)
ROLL_A = _P(h=8, arms=(("fk", 20, 140), ("ik", "abs", 74, -206, 1)), hands=("fist", "fist"), look=(0.05, 0.02))
ROLL_B = _P(h=8, arms=(("fk", 20, 140), ("ik", "abs", 52, -184, 1)), hands=("fist", "fist"), look=(0.05, 0.03))
REACH = _P(t=14, h=8, drop=6, legs=(("ik", 24, 1), ("ik", -20, 1)), arms=(("fk", 14, 8), ("ik", "abs", 150, -98, 1)),
           hands=("fist", "fist"), look=(0.05, 0.06))
HOLD = _P(h=-6, arms=(("fk", 14, 8), ("fk", 34, 150)), hands=("fist", "fist"), look=(0.03, -0.04))


def saw_held(D, rot=-58):
    def f(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        blade = f'<g transform="translate({f1(W[0])},{f1(W[1])}) rotate({rot}) scale(0.85)">{C._prp()._saw_shape()}</g>'
        return blade + C._fist(W, hr, D["skin"], 2, 0)
    return f


def roll_marks(D):
    def f(st):
        W = st["arms"][1][2]
        out = ""
        for k in range(2):
            out += (f'<path d="M{f1(W[0] - 30 - 14 * k)},{f1(W[1] - 36 - 10 * k)} q10,-12 22,-6" fill="none" '
                    f'stroke="{P["ink_soft"]}" stroke-width="3" stroke-linecap="round"/>')
        return out
    return f


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines

    # ------------------------------------------------------------ beats
    t_god = pt(ctx, 0, "上帝对挪亚")
    t_g1 = L[1].start                                    # God speaks
    t_water = pt(ctx, 1, "地上就要")
    t_build = pt(ctx, 1, "你要造")
    t_big = pt(ctx, 1, "很大很大")
    t_name = pt(ctx, 1, "叫方舟")
    t_fam = L[2].start
    t_anim = pt(ctx, 2, "还要把")
    t_pair = pt(ctx, 2, "一公一母")
    t_two = pt(ctx, 2, "两个两个")
    t_g_end = L[2].end
    t_think = L[3].start                                 # 挪亚心想：一只大船？
    t_far = pt(ctx, 3, "可是，这里")
    t_obey = L[4].start
    t_do = pt(ctx, 4, "一样一样")

    # ------------------------------------------------------------ backdrop
    sc.add("sky", sky_svg(), wc=0.45)
    sc.add("far", far_svg(), wc=0.7)
    sc.add("hill", hill_svg(), wc=0.8)
    sc.add("props", props_svg(), wc=0.7)
    # birds flying home in the evening
    def bird(x, y, s, up):
        k = -1 if up else 0.4
        return (f'<path d="M{f1(x - 22 * s)},{f1(y + 10 * s * k)} Q{f1(x - 10 * s)},{f1(y - 4 * s)} {f1(x)},{f1(y + 4 * s)} '
                f'Q{f1(x + 10 * s)},{f1(y - 4 * s)} {f1(x + 22 * s)},{f1(y + 10 * s * k)}" fill="none" '
                f'stroke="#5e4a5a" stroke-width="{4 * s}" stroke-linecap="round"/>')
    birds = [doc(bird(0, 0, 1.1, up) + bird(90, 30, 0.9, not up) + bird(170, -10, 0.8, up)) for up in (True, False)]
    sc.add("birds", birds, wc=0, frame_at=lambda t: float(int(t * 4) % 2),
           motion=lambda t: Tf(dx=-300 + 70 * t, dy=420 - 4 * t))

    # ------------------------------------------------------------ God's light
    light_a = lambda t: (M.progress(t, t_god - 0.2, t_g1 + 0.2, "sine") *
                         (1 - M.progress(t, t_g_end + 0.1, t_g_end + 1.2, "sine")))
    rays = rays_svg(XN + 260, -200, XN + 10, GY - 260, 10, "s5r", n=8, wk=1.8, pool=(330, 90), w=SW, h=SH)
    sc.add("rays", rays, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=light_a(t) * (0.88 + 0.12 * math.sin(2 * math.pi * t / 2.3))))
    sc.add("topglow", glow_svg(XN + 400, -80, 700, "s5tg", a=0.9, w=SW, h=SH), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=light_a(t)))
    sc.add_dynamic("light_sparkle", sparkle_dyn((XN - 260, 120, XN + 520, GY - 520), count=16, t0=t_god, t1=t_g_end + 1.0,
                                                size=(8, 15), period=1.4, drift=8, seed=5))

    # ------------------------------------------------------------ the golden picture in the sky
    pic_out = lambda t: 1 - M.progress(t, t_g_end - 0.1, t_g_end + 0.9, "sine")
    sc.add("waves", waves_svg(), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_water + 0.5, t_water + 1.6, "sine"), "soft": 120},
           motion=lambda t: Tf(alpha=0.9 * (1 - M.progress(t, t_fam - 0.4, t_fam + 0.4, "sine"))))
    ax, ay, _ = ARK

    def ark_m(t):
        k = 0.9 + 0.1 * M.progress(t, t_big, t_big + 0.6, "back")
        return Tf(sx=k, sy=k, px=ax, py=ay, alpha=pic_out(t))
    sc.add("ark_pic", ark_draw(), wc=0, motion=ark_m,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_build + 0.15, t_build + 1.5, "linear"),
                             "soft": 90})
    sc.add("label", label_svg(), wc=0,
           motion=lambda t: (lambda p: Tf(sx=p.sx, sy=p.sy, dy=p.dy, alpha=p.alpha * pic_out(t), px=p.px,
                                          py=p.py))(pop_tf(t, t_name + 0.1, T + 5, ax, ay + 70, bob=3)))
    slide = lambda t: -150 * M.progress(t, t_two, t_two + 1.7, "inout")
    bobs = lambda t, ph: -8 * abs(math.sin(math.pi * (t - t_two) / 0.32 + ph)) if t_two < t < t_two + 1.7 else 0.0
    fam_in = lambda t: M.progress(t, t_fam + 0.15, t_fam + 0.75, "sine")
    sc.add("fam_pic", family_draw(), wc=0,
           motion=lambda t: Tf(dx=slide(t) + 40 * (1 - fam_in(t)), dy=bobs(t, 0), alpha=0.95 * fam_in(t) * pic_out(t)))
    n_pairs = len(PAIRS)
    for i, (kind, x) in enumerate(PAIRS):
        ti = t_anim + 0.25 + (t_pair - t_anim - 0.3) * i / n_pairs
        frames = [pair_draw(kind, x, 0), pair_draw(kind, x, 1)]
        hop_t = t_pair + 0.12 * i

        def pm(t, ti=ti, x=x, hop_t=hop_t, i=i):
            a = M.progress(t, ti, ti + 0.3, "sine")
            k = 0.7 + 0.3 * M.ease("back")(clamp((t - ti) / 0.35))
            hop = -18 * math.sin(math.pi * clamp((t - hop_t) / 0.35)) - 12 * math.sin(math.pi * clamp((t - hop_t - 0.4) / 0.3))
            return Tf(dx=slide(t), dy=hop + bobs(t, 0.5 * (i + 1)), sx=k, sy=k, px=x, py=ay, alpha=0.95 * a * pic_out(t))
        sc.add(f"pair{i}", frames, wc=0, motion=pm,
               frame_at=lambda t: float(int((t - t_two) / 0.32) % 2) if t > t_two else 0.0)
    t_doves = t_anim + 0.25 + (t_pair - t_anim - 0.3) * n_pairs / (n_pairs + 0.5)
    dv = [doves_draw(w) for w in (0.0, 0.25, 0.5, 0.75)]
    sc.add("doves_pic", dv, wc=0, frame_at=lambda t: float(int(t * 7) % 4),
           motion=lambda t: Tf(dx=slide(t) * 1.4, dy=8 * math.sin(t * 2.2),
                               alpha=0.95 * M.progress(t, t_doves, t_doves + 0.3, "sine") * pic_out(t)))
    sc.add_dynamic("pic_sparkle", sparkle_dyn((1000, 250, 2700, 820), count=18, t0=t_build + 0.3, t1=t_g_end + 0.9,
                                              size=(7, 14), period=1.5, drift=-6, seed=8))

    # ------------------------------------------------------------ the saw on the stump (until he picks it up)
    t_reach = t_do + 1.05
    t_hold = t_reach + 0.4
    sc.add("saw_stump", saw_on_stump(), wc=0.5, motion=lambda t: Tf(alpha=1.0 if t < t_hold else 0.0))

    # ------------------------------------------------------------ NOAH
    spN = sprite(700, 640, 330, 580, seed=60)
    st_kind = fam(spN, "noah", "stand", expr="kind")
    look = [fam_custom(spN, "noah", LOOK, e, label=f"look{e}") for e in ("amazed", "surprised", "happy", "laugh")]
    look_l = fam(spN, "noah", "stand", facing=-1, expr="puzzled")
    look_r = fam(spN, "noah", "stand", facing=1, expr="puzzled")
    scratch = fam(spN, "noah", "scratch_head")
    scratch_l = fam(spN, "noah", "scratch_head", facing=-1)
    nod = fam(spN, "noah", "nod", expr="determined")
    st_det = fam(spN, "noah", "stand", expr="determined")
    D = C._family_design("noah")
    roll_a = fam_custom(spN, "noah", ROLL_A, "determined", front=roll_marks(D), label="rollA")
    roll_b = fam_custom(spN, "noah", ROLL_B, "determined", label="rollB")
    reach = fam_custom(spN, "noah", REACH, "determined", label="reach")
    hold = fam_custom(spN, "noah", HOLD, "determined", front=saw_held(D), label="hold")
    hold_k = fam_custom(spN, "noah", HOLD, "happy", front=saw_held(D), label="holdk")

    sched = [(0, st_kind, 0), (t_god + 0.1, look[0], 0.9), (t_water + 0.4, look[1], 0.4),
             (t_build + 0.3, look[0], 0.4), (t_fam + 0.3, look[2], 0.4), (t_pair, look[3], 0.4),
             (t_g_end + 0.3, look[2], 0.0)]
    sched += [(t_think + 0.2, look_l, 0.7), (t_think + 0.85, look_r, 0.7), (t_think + 1.5, look_l, 0.5),
              (t_think + 2.0, scratch, 1.0), (t_far + 1.5, scratch_l, 0.5), (t_far + 2.6, scratch, 0.5)]
    t_nod = t_obey + 0.35
    for k in range(3):
        sched += [(t_nod + 0.56 * k, nod, 0.6 if k == 0 else 0.0), (t_nod + 0.56 * k + 0.28, st_det, 0.0)]
    sched += cycle(t_do + 0.05, t_reach, [roll_a, roll_b], 0.22, hop=0.5)
    sched += [(t_reach, reach, 0.7), (t_hold, hold, 1.1), (T - 0.9, hold_k, 0.0)]
    sc.add("shN", doc(C.ground_shadow(XN, GY, K, width=125, opacity=0.24)), wc=0)
    sc.add_dynamic("noah", Actor(spN, sched, lambda t: (XN, GY), bper=3.2, phase=0.2))

    # a little 'cloth' twitch mark on each sleeve roll is drawn in ROLL_A; a glint when the saw is lifted
    gx, gy = XN + 130 * K, GY - 400 * K
    star = (f'<path d="M{gx},{gy - 34} L{gx + 9},{gy - 9} L{gx + 34},{gy} L{gx + 9},{gy + 9} L{gx},{gy + 34} '
            f'L{gx - 9},{gy + 9} L{gx - 34},{gy} L{gx - 9},{gy - 9} Z" fill="#fff4c8" stroke="#d9a441" stroke-width="3"/>')
    sc.add("glint", doc(star), wc=0, motion=lambda t: pop_tf(t, t_hold + 0.15, t_hold + 0.7, gx, gy, bob=0))

    # ------------------------------------------------------------ the far-away sea inset (line 3)
    IX, IY, IR = 2240, 400, 230
    ins, defs = inset_svg(IX, IY, IR)
    t_ins_in, t_ins_out = t_far + 0.55, t_obey - 0.15
    sc.add("inset", doc(ins, defs), wc=0.3, motion=lambda t: pop_tf(t, t_ins_in, t_ins_out, IX, IY, bob=3))
    sc.add("far_arrow", far_arrow_svg(XN + 70, GY - 570, IX - IR - 30, IY + 60), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_ins_in + 0.2, t_ins_in + 1.4, "inout"), "soft": 60},
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_ins_out - 0.1, t_ins_out + 0.25, "sine")))

    sc.add("fg", [fg_svg(sw) for sw in (-0.5, 0.0, 0.5)], wc=0.7,
           frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.6))
    # first evening stars and a few fireflies near the end
    sc.add_dynamic("stars", sparkle_dyn((200, 60, 2600, 420), count=10, t0=t_obey - 1.0, t1=T + 2, color=(255, 246, 220),
                                        size=(5, 9), period=2.2, drift=0, seed=12))

    # ------------------------------------------------------------ CAMERA
    c0 = Cam(1250, 840, 2500)
    c_full = Cam(1400, 787, 2800)
    c_close = Cam(800, 989, 1700)
    c_end = Cam(860, 975, 1780)
    keys = [(0.0, c0), (t_g1 - 0.3, c0), (t_build + 0.2, c_full), (t_g_end + 0.4, c_full), (t_think + 1.3, c_close),
            (t_far - 0.1, c_close), (t_far + 1.2, c_full), (t_obey - 0.2, c_full), (t_obey + 1.4, c_end),
            (T, Cam(866, 977, 1770))]
    sc.camera = clamp_cam(M.cam_keys(keys, "sine"), SW, SH)

    # ------------------------------------------------------------ SOUND
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("night", 0, dur=T + 0.8, gain_db=-26, fade_in=1.5, fade_out=1.0)
    sc.sfx("chime", t_god, gain_db=-12)
    sc.sfx("sparkle", t_water + 0.5, gain_db=-17)
    sc.sfx("grow", t_build + 0.15, gain_db=-14)
    sc.sfx("pop", t_name + 0.1, gain_db=-13)
    sc.sfx("sparkle", t_fam + 0.15, gain_db=-17)
    for i in range(n_pairs):
        sc.sfx("pop", t_anim + 0.25 + (t_pair - t_anim - 0.3) * i / n_pairs, gain_db=-14, pan=0.4)
    sc.sfx("pop", t_doves, gain_db=-16, pan=0.3)
    sc.sfx("footsteps", t_two, dur=1.7, gain_db=-22, fade_in=0.1, fade_out=0.4, pan=0.4)
    sc.sfx("pop", t_ins_in, gain_db=-13, pan=0.5)
    sc.sfx("whoosh", t_ins_in + 0.2, gain_db=-20, pan=0.4)
    sc.sfx("pop", t_ins_out, gain_db=-16, pan=0.5)
    sc.sfx("cloth", t_do + 0.05, gain_db=-14)
    sc.sfx("cloth", t_do + 0.5, gain_db=-16)
    sc.sfx("thud", t_hold, gain_db=-16)
    sc.sfx("sparkle", t_hold + 0.15, gain_db=-18)
    return sc
