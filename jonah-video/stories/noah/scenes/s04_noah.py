"""Scene 4 — Noah was different (Genesis 6:8-10).

"可是，有一个人不一样。他的名字叫挪亚。" / "挪亚爱上帝，听上帝的话，每天都和上帝同行。" / "挪亚有三个儿子，名字叫闪、含和雅弗。"

One 3300 x 1688 stage: a sunny green hillside in the morning. Far away on the left, down in the valley, the grey
quarrelling town of s03 sits under its own little grey cloud; up here everything is bright: an olive tree on a knoll,
a trodden path, the neighbour's house and Noah's house with a palm-frond shade and a washing line, sheep grazing,
butterflies, songbirds.

  start   calm wide picture: the grey town far left, Noah standing on the knoll in the sun.
  line 0  "可是，有一个人不一样。"   the camera leaves the grey town and pushes in on Noah; a warm sunbeam finds him.
          "他的名字叫挪亚。"         a happy hop and a wave; a name ribbon "挪亚" pops above him.
  line 1  "挪亚爱上帝，听上帝的话，"  he kneels to pray; soft golden rays come down on him (God is only light).
          "每天都和上帝同行。"       he gets up and walks along the path with a small golden light walking beside him;
                                    on the way he lifts the neighbour lady's heavy water jar and carries it to her
                                    door (planted-foot walks); she cheers, a heart pops.
  line 2  "挪亚有三个儿子，"         he walks on home, where his wife waves; the light rises away into the sky.
          "名字叫闪、含和雅弗。"     the three sons step forward one by one, each keyed to his name, with a hop and a
                                    name ribbon; then the three daughters-in-law join: the whole family of eight.
  end     calm family portrait in front of Noah's house (dippaper to s05).

Shared helpers for s05 / s06 (same illustrator): doc(), fam(), fam_walk(), ribbon(), glow_svg(), cycle().
Pose changes are hard cuts sold by squash-and-hop (Actor); walks are planted-foot cycles.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_A, WALK_N, walk_pose
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.daniel.scenes.s05_prays import clamp, fig
from stories.david.scenes.s08_saul import (Actor, WalkPath, clamp_cam, heart, pop_tf, pt, rays_svg, sparkle_dyn,
                                           sprite)

INK = P["ink"]
SW, SH = 3300, 1688
GY = 1420                      # ground line (feet)
K = 1.1                        # person scale
TINT = "#dfeaf0"               # aerial haze


def f1(v):
    return f"{v:.1f}"


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


# ================================================================== figures (shared with s05 / s06)
FAM_KEY = {"noah": "noah", "noah_wife": "wife", "shem": "shem", "ham": "ham", "japheth": "japheth",
           "daughter_in_law0": "dil0", "daughter_in_law1": "dil1", "daughter_in_law2": "dil2"}


def fam(sp, who, pose="stand", s=K, facing=1, **kw):
    """A library drawing of a family member on sprite sp (anchored at the sprite anchor)."""
    return sp.add(C.family_member(who, sp.ax, sp.ay, s, facing, pose=pose, **kw))


def fam_custom(sp, who, ps, expr, s=K, facing=1, front=None, behind=None, mid=None, label="x"):
    D = C._family_design(FAM_KEY[who])
    D["front"], D["behind"], D["mid"] = front, behind, mid
    m = C._FAMILY[FAM_KEY[who]]["m"]
    return sp.add(fig(D, m, dict(ps), expr, sp.ax, sp.ay, s, facing, f"{who}-{label}"))


def fam_walk(sp, who, s=K, facing=1, expr="happy", arms=None, front=None, A=WALK_A, lk=1.0):
    """2*WALK_N planted-foot walk drawings of a family member (arms: fixed (far, near) specs + hands, or None)."""
    idx = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k, A=A, lk=lk)
        if arms is not None:
            ps["arms"], ps["hands"] = arms
        idx.append(fam_custom(sp, who, ps, expr, s, facing, front=front, label=f"w{k}"))
    return idx


def walk_adv(s, A=WALK_A):
    return 2 * A / WALK_N * s


def cycle(t0, t1, frames, dt, hop=0.0):
    """Schedule entries cycling through drawing indices every dt seconds from t0 to t1."""
    out, t, i = [], t0, 0
    while t < t1:
        out.append((t, frames[i % len(frames)], hop if i == 0 else 0.0))
        t += dt
        i += 1
    return out


def ribbon(cx, cy, label, w=None, col="#e9746a", size=58):
    """A picture-book name ribbon (cream banner with folded red tails) with the name on it."""
    w = w or (size * len(label) + 70)
    h = size * 1.35
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    dk = S.shade(col, -0.25)
    tl = (f'<path d="M{f1(x0 + 14)},{f1(y0 + 16)} L{f1(x0 - 56)},{f1(y0 + 20)} L{f1(x0 - 30)},{f1(cy + 12)} '
          f'L{f1(x0 - 58)},{f1(y1 + 18)} L{f1(x0 + 14)},{f1(y1 + 14)} Z" fill="{col}" stroke="{INK}" stroke-width="4" '
          f'stroke-linejoin="round"/>')
    tr = (f'<path d="M{f1(x1 - 14)},{f1(y0 + 16)} L{f1(x1 + 56)},{f1(y0 + 20)} L{f1(x1 + 30)},{f1(cy + 12)} '
          f'L{f1(x1 + 58)},{f1(y1 + 18)} L{f1(x1 - 14)},{f1(y1 + 14)} Z" fill="{col}" stroke="{INK}" stroke-width="4" '
          f'stroke-linejoin="round"/>')
    fold = (f'<path d="M{f1(x0 + 14)},{f1(y1 + 14)} L{f1(x0)},{f1(y1)} L{f1(x0 + 14)},{f1(y1)} Z" fill="{dk}"/>'
            f'<path d="M{f1(x1 - 14)},{f1(y1 + 14)} L{f1(x1)},{f1(y1)} L{f1(x1 - 14)},{f1(y1)} Z" fill="{dk}"/>')
    band = (f'<path d="M{f1(x0)},{f1(y0)} Q{f1(cx)},{f1(y0 - 12)} {f1(x1)},{f1(y0)} L{f1(x1)},{f1(y1)} '
            f'Q{f1(cx)},{f1(y1 - 12)} {f1(x0)},{f1(y1)} Z" fill="#fff4dc" stroke="{INK}" stroke-width="4.5" '
            f'stroke-linejoin="round"/>')
    out = S.g(tl + tr + fold + band, filter="wobble-fine")
    out += S.text(cx, cy + size * 0.36 - 6, label, size=size, fill=S.shade(col, -0.45))
    return out


def glow_svg(cx, cy, r, uid, col="#fff0b8", a=0.85, w=SW, h=SH):
    defs = S.rad_grad(uid, [(0, "#fffaf0", a), (0.25, col, a * 0.8), (0.6, col, a * 0.3), (1, col, 0)])
    return doc(f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="url(#{uid})"/>', defs, w, h)


def grass_strokes(rng, n, x0, x1, y0, y1, col, sk=1.0):
    out = ""
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = sk * (0.5 + 0.9 * (y - y0) / max(1, (y1 - y0)))
        out += (f'<path d="M{f1(x)},{f1(y)} q{f1(5 * s)},{f1(-15 * s)} {f1(11 * s)},0 m{f1(5 * s)},0 '
                f'q{f1(5 * s)},{f1(-12 * s)} {f1(10 * s)},0" fill="none" stroke="{col}" stroke-width="{f1(2 + 2 * s)}" '
                f'opacity="0.55" stroke-linecap="round"/>')
    return out


def flowers(rng, n, x0, x1, y0, y1, s=1.0):
    out = ""
    cols = ["#f4a6b4", "#f6d36b", "#fffaf0", "#c9a0dc", "#f08f6c"]
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        c = rng.choice(cols)
        r = s * rng.uniform(6, 10)
        for k in range(5):
            a = 2 * math.pi * k / 5
            out += f'<circle cx="{f1(x + r * math.cos(a))}" cy="{f1(y + r * math.sin(a) * 0.8)}" r="{f1(r * 0.6)}" fill="{c}"/>'
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.45)}" fill="#e8a33c"/>'
    return out


# ================================================================== backdrop
TOWN = (120, 760, 905)          # grey town: x0, x1, its ground line far away
KNOLL_X = 1000                  # Noah stands / prays here
NB_HOUSE = 1640                 # neighbour's house anchor
NH_HOUSE = 2430                 # Noah's house anchor
HOUSE_Y = GY - 125              # houses stand a little up the slope behind the path


def sky_svg():
    defs = (S.lin_grad("s4sky", [(0, "#8fcae2"), (0.5, "#c3e3ea"), (0.8, "#f6ebcf"), (1, "#fbe8c4")])
            + S.rad_grad("s4sun", [(0, "#fff8dc", 0.95), (0.4, "#fdeec6", 0.45), (1, "#fdeec6", 0)]))
    body = S.rect_bg("url(#s4sky)", SW, SH)
    body += '<ellipse cx="2850" cy="300" rx="1000" ry="620" fill="url(#s4sun)"/>'
    body += S.g(f'<circle cx="2850" cy="250" r="96" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
                f'stroke-width="5"/><circle cx="2818" cy="220" r="30" fill="#fff4cc" opacity="0.7"/>',
                filter="wobble-fine")
    # the grey sky over the far town (left)
    defs += S.rad_grad("s4grey", [(0, "#8d9098", 0.55), (0.6, "#9da1a8", 0.25), (1, "#a9adb3", 0)])
    body += '<ellipse cx="420" cy="620" rx="700" ry="430" fill="url(#s4grey)"/>'
    return doc(body, defs)


def far_svg():
    """Far blue ridges, the valley with the grey quarrelling town under its little grey cloud."""
    ridge = S.mix("#9fb8c8", "#e9e6dc", 0.35)
    body = S.path(S.hill(-200, 1500, 930, 230, seed=4, bumps=3, bottom=1300), fill=ridge, sw=2.6)
    body += S.path(S.hill(1100, 3500, 920, 200, seed=9, bumps=3, bottom=1300), fill=S.mix(ridge, "#c9dcc0", 0.3),
                   sw=2.6)
    out = S.g(body, filter="wobble")
    # the valley floor in front of the ridges (dull, greyer on the left)
    vd = S.lin_grad("s4val", [(0, "#a7ab9a"), (0.45, "#b9c79a"), (1, "#c3d59a")], x1=0, y1=0, x2=1, y2=0)
    out += S.g(S.path(S.hill(-200, 1900, 985, 90, seed=2, bumps=3, bottom=1400), fill="url(#s4val)", sw=2.6)
               + S.path(S.hill(1500, 3500, 975, 110, seed=6, bumps=3, bottom=1400), fill="#bccf96", sw=2.6),
               filter="wobble")
    rng0 = random.Random(3)
    trees = ""
    for i in range(14):
        x = rng0.uniform(900, 3300)
        trees += PR.olive_tree(x, 990 + rng0.uniform(-30, 20), rng0.uniform(0.14, 0.2), seed=i)
    out += PR._haze(trees, TINT, 0.45, 0.4)
    # the grey town (small, far): flat-roofed houses, a few bare trees
    rng = random.Random(7)
    town = ""
    xs = sorted(rng.uniform(TOWN[0], TOWN[1]) for _ in range(9))
    for i, x in enumerate(xs):
        town += PR.house(x, TOWN[2] + rng.uniform(-8, 10), rng.uniform(0.13, 0.17), variant=i % 4,
                         facing=1 if i % 2 else -1)
    town = PR._haze(town, "#9a9ea6", 0.55, 0.35)
    out += town
    # its grumpy little grey cloud and a few cross scribbles (quarrel marks)
    cl = S.cloud(420, 700, 420, 100, "#8f949c", seed=5, sw=3, shade_fill="#767b84")
    cl += S.cloud(640, 670, 240, 66, "#9a9fa7", seed=8, sw=3)
    out += S.g(cl, filter="wobble", opacity=0.9)
    for x, y in ((300, 830), (520, 815), (680, 840)):     # little zigzag grumble marks over the quarrelling town
        out += (f'<path d="M{x - 18},{y} l9,-10 l9,10 l9,-10 l9,10" fill="none" stroke="#6f6a66" stroke-width="3.5" '
                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.75"/>')
    return doc(out, vd)


def hill_svg():
    """The green hillside the story happens on: a knoll with an olive tree on the left, the slope rising gently to
    the right behind the path."""
    defs = S.lin_grad("s4hill", [(0, "#a9cc68"), (0.5, "#93ba58"), (1, "#7aa247")])
    pts = [(-60, 1120), (300, 1080), (700, 1010), (1000, 990), (1300, 1030), (1700, 1010), (2200, 960), (2700, 930),
           (3100, 950), (3360, 940)]
    d = S.smooth_path(pts, closed=False) + f" L3360,{SH + 40} L-60,{SH + 40} Z"
    out = f'<path d="{d}" fill="url(#s4hill)" stroke="{INK}" stroke-width="5"/>'
    rng = random.Random(11)
    out += grass_strokes(rng, 90, 0, SW, 1040, SH, P["grass_dark"])
    # soft lighter patches
    for x, y, rx in ((500, 1200, 260), (1500, 1150, 300), (2500, 1080, 280)):
        out += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.18}" fill="#c4dc84" opacity="0.45"/>'
    # the trodden path along the ground line, rising a little toward the houses
    out += (f'<path d="M760,{GY + 70} C1200,{GY + 40} 1700,{GY + 50} 2200,{GY + 30} S3000,{GY + 30} 3400,{GY + 20}" '
            f'fill="none" stroke="#dcc796" stroke-width="150" stroke-linecap="round" opacity="0.55"/>')
    out += (f'<path d="M760,{GY + 70} C1200,{GY + 40} 1700,{GY + 50} 2200,{GY + 30} S3000,{GY + 30} 3400,{GY + 20}" '
            f'fill="none" stroke="#e8d8ac" stroke-width="70" stroke-linecap="round" opacity="0.5"/>')
    out += flowers(rng, 40, 0, SW, 1080, 1330, 1.1)
    return doc(S.g(out, filter="wobble"), defs)


def houses_svg():
    out = PR.olive_tree(KNOLL_X - 230, GY - 120, 1.05, seed=3)
    out += PR.bush(KNOLL_X + 260, GY - 150, 0.7, variant=1)
    out += PR.house(NB_HOUSE, HOUSE_Y, 0.8, variant=0, facing=1)
    out += PR.bush(NB_HOUSE + 340, HOUSE_Y + 10, 0.65, variant=3)
    out += PR.house(NH_HOUSE, HOUSE_Y - 10, 0.82, variant=3, facing=-1)
    out += PR.palm_tree(NH_HOUSE + 450, HOUSE_Y - 20, 0.95, lean=-0.2)
    out += PR.bush(NH_HOUSE + 700, HOUSE_Y + 30, 0.8, variant=1)
    # a little wooden bench and flower pots by Noah's door
    out += S.g(f'<rect x="{NH_HOUSE - 330}" y="{HOUSE_Y - 70}" width="170" height="20" rx="6" fill="{P["wood_light"]}" '
               f'stroke="{INK}" stroke-width="4"/><rect x="{NH_HOUSE - 315}" y="{HOUSE_Y - 52}" width="16" height="52" '
               f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3.5"/><rect x="{NH_HOUSE - 190}" y="{HOUSE_Y - 52}" '
               f'width="16" height="52" fill="{P["wood"]}" stroke="{INK}" stroke-width="3.5"/>', filter="wobble-fine")
    return doc(out)


def fg_svg(sway=0.0):
    out = ""
    for x, y, s, v in ((80, SH + 20, 1.7, 2), (420, SH + 40, 1.4, 0), (1350, SH + 40, 1.5, 2), (2050, SH + 30, 1.4, 0),
                       (2900, SH + 30, 1.6, 2), (3230, SH + 40, 1.4, 0)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sway)
    return doc(out)


def sheep_svg(k):
    out = ""
    for i, (x, y, s, f, v) in enumerate(((240, 1150, 0.42, 1, 0), (380, 1130, 0.36, -1, 2), (3120, 1030, 0.4, -1, 3))):
        pose = "graze" if (k + i) % 3 != 0 else "stand"
        out += PR.sheep(x, y, s, f, variant=v, pose=pose)
    return doc(out)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines

    # ------------------------------------------------------------ beats
    t_diff = L[0].start                                  # "可是，有一个人不一样。"
    t_name = pt(ctx, 0, "他的名字")                      # "他的名字叫挪亚。"
    t_noah = pt(ctx, 0, "叫挪亚")
    t_pray = pt(ctx, 1, "挪亚爱上帝")
    t_walk = pt(ctx, 1, "每天都")
    t_sons = L[2].start                                  # "挪亚有三个儿子，"
    t_shem = pt(ctx, 2, "闪")
    t_ham = pt(ctx, 2, "含")
    t_jap = pt(ctx, 2, "雅弗")
    t_ham = max(t_ham, t_shem + 0.42)
    t_jap = max(t_jap, t_ham + 0.42)
    t_wives = max(L[2].end - 0.15, t_jap + 0.5)
    t_wives = min(t_wives, T - 1.25)

    # ------------------------------------------------------------ positions
    G = 2200                                             # family portrait centre (noah_family(facing=-1) anchor)
    # noah_family's portrait mirrored (facing=-1): Noah on the left facing right, his wife on his right
    grp = {name: (G - dx * K, GY + dy * K, (0.97 if dy < 0 else 1.0), -f) for name, dx, dy, f in C._GROUP}
    # ... but the sons in reading order, left to right: Shem, Ham, Japheth (each turned toward the middle)
    grp["shem"], grp["japheth"] = ((grp["japheth"][0], grp["shem"][1], grp["shem"][2], 1),
                                   (grp["shem"][0], grp["japheth"][1], grp["japheth"][2], -1))
    adv = walk_adv(K)
    X0 = KNOLL_X
    JAR_X = 1290
    X_LIFT = JAR_X - 52 * K
    X_DROP = 1430
    NB_X = 1625                                          # the neighbour at her door (door at ~NB_HOUSE - 70)
    X_HOME = grp["noah"][0]
    rate = 17.0
    t_up = t_walk + 0.02
    w1 = WalkPath([(t_up + 0.12, X0, X_LIFT, rate)], [0], adv)
    t_lift = w1.end(0) + 0.05
    t_carry = t_lift + 0.38
    w2 = WalkPath([(t_carry, X_LIFT, X_DROP, rate - 1)], [0], adv)
    t_drop = w2.end(0) + 0.04
    t_nb_in = t_drop + 0.95                              # she goes in at her door
    t_home = t_drop + 1.1
    w3 = WalkPath([(t_home, X_DROP, X_HOME, rate)], [0], adv)
    t_arrive = w3.end(0)
    t_turn = t_arrive

    # ------------------------------------------------------------ SKY / BACKDROP (static, consecutive)
    sc.add("sky", sky_svg(), wc=0.45)
    sc.add("far", far_svg(), wc=0.7)
    sc.add("hill", hill_svg(), wc=0.8)
    sc.add("houses", houses_svg(), wc=0.7)
    # clouds drift; the grey one over the town stays put and just bobs
    for i, (cx, cy, w, h, sd, v) in enumerate(((1350, 230, 360, 100, 3, 7), (2150, 160, 300, 86, 7, 5),
                                                (3050, 520, 260, 74, 11, 6), (1800, 470, 220, 60, 5, 4))):
        sc.add(f"cloud{i}", doc(S.g(S.cloud(cx, cy, w, h, "#fdf6e8", seed=sd, sw=3, shade_fill="#efe2d0"),
                                    filter="wobble")), wc=0.7,
               motion=M.combine(M.drift(vx=-v), M.bob(3, 7 + i, i * 0.3)))
    sc.add("sheep", [sheep_svg(k) for k in range(3)], wc=0.7,
           frame_at=lambda t: float(int(t / 1.7) % 3))
    # laundry on the washing line flutters (a tiny sway of the whole house would be wrong; use butterflies instead)

    # ------------------------------------------------------------ the sunbeam on Noah (line 0)
    beam = rays_svg(2850, 250, X0 + 10, GY - 200, 5, "s4beam", n=5, wk=2.2, pool=(260, 70), w=SW, h=SH)
    sc.add("beam", beam, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.75 * M.progress(t, t_diff + 0.3, t_diff + 1.4, "sine") *
                               (1 - M.progress(t, t_pray - 0.2, t_pray + 0.5, "sine"))))
    # the golden rays while he prays (God is only light)
    rays = rays_svg(X0 + 150, -80, X0 + 10, GY - 190, 9, "s4pray", n=7, wk=1.6, pool=(300, 80), w=SW, h=SH)
    sc.add("prayrays", rays, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.95 * M.progress(t, t_pray, t_pray + 0.9, "sine") *
                               (1 - M.progress(t, t_walk + 0.2, t_walk + 1.0, "sine"))))
    sc.add_dynamic("pray_sparkle", sparkle_dyn((X0 - 200, GY - 560, X0 + 220, GY - 120), count=12, t0=t_pray + 0.2,
                                               t1=t_walk + 0.8, size=(8, 15), period=1.3, drift=-14, seed=4))

    # ------------------------------------------------------------ the jar (on the ground before / after)
    jar_s = 0.62 * K
    jar_g = lambda x: PR.jar(x, GY - 82 * jar_s, jar_s)
    sc.add("jar0", doc(C.ground_shadow(JAR_X, GY, K, width=70, opacity=0.2) + jar_g(JAR_X)), wc=0.5,
           motion=lambda t: Tf(alpha=1.0 if t < t_lift else 0.0))
    JAR_DROP_X = X_DROP + 60 * K
    sc.add("jar1", doc(C.ground_shadow(JAR_DROP_X, GY, K, width=70, opacity=0.2) + jar_g(JAR_DROP_X)), wc=0.5,
           motion=lambda t: Tf(alpha=1.0 if t >= t_drop else 0.0))

    # ------------------------------------------------------------ NOAH
    spN = sprite(620, 600, 300, 540, seed=40)
    n_stand = fam(spN, "noah", "stand", expr="kind")
    n_stand_h = fam(spN, "noah", "stand", expr="happy")
    n_waves = [fam(spN, "noah", "wave", phase=ph) for ph in (0.0, 0.25, 0.5, 0.75)]
    n_kneel = fam(spN, "noah", "kneel_pray")
    n_carry = fam(spN, "noah", "carry", item="jar")
    n_turn = fam(spN, "noah", "stand", s=K, facing=1, expr="happy")
    n_turn_k = fam(spN, "noah", "stand", s=K, facing=1, expr="kind")
    n_walk = fam_walk(spN, "noah")
    D0 = C._family_design("noah")
    jar_front = C._nh_items(D0, "carry", 0.0, "jar", False, True, True)[2]
    carry_arms = C._nh_carry_pose("jar")
    n_cwalk = fam_walk(spN, "noah", arms=(carry_arms["arms"], carry_arms["hands"]), front=jar_front)
    w1.draw = [n_walk]
    w2.draw = [n_cwalk]
    w3.draw = [n_walk]

    sched = [(0, n_stand, 0)]
    sched += cycle(t_noah - 0.05, t_noah + 1.6, n_waves, 0.13, hop=1.2)
    sched += [(t_noah + 1.6, n_stand_h, 0.4)]
    sched += [(t_pray, n_kneel, 1.0), (t_up, n_stand_h, 0.9), (t_lift, n_stand_h, 0), (t_lift, n_carry, 1.1),
              (t_drop, n_stand_h, 0.8), (t_turn, n_turn, 0.7), (t_wives + 0.6, n_turn_k, 0.0)]

    def n_pos(t):
        if t < t_lift:
            return w1.x(t), GY
        if t < t_home:
            return w2.x(t), GY
        return w3.x(t), GY

    def n_walkfr(t):
        for w in (w1, w2, w3):
            f = w.frame(t)
            if f is not None:
                return f
        return None

    shadow = doc(C.ground_shadow(0, GY, K, width=125, opacity=0.24))
    sc.add("shadowN", shadow, wc=0, motion=lambda t: Tf(dx=n_pos(t)[0]))

    # ------------------------------------------------------------ the golden light that walks beside him
    LR = 150 * K

    def light_xy(t):
        x, _ = n_pos(max(0.0, t - 0.3))
        y = GY - 205 * K + 10 * math.sin(2 * math.pi * t / 1.6)
        # it comes down out of the prayer rays and rises away into the sky at home
        down = 1 - M.progress(t, t_walk - 0.1, t_walk + 0.7, "out")
        up = M.progress(t, t_arrive - 0.2, t_arrive + 1.4, "in")
        return x - 120 * K, y - 520 * down - 700 * up

    def light_a(t):
        return M.progress(t, t_walk - 0.1, t_walk + 0.5, "sine") * (1 - M.progress(t, t_arrive + 0.4, t_arrive + 1.4,
                                                                                    "sine"))

    O = 500                                              # the glow is drawn at (O, O) and moved from there
    sc.add("light", glow_svg(O, O, LR, "s4lg", a=0.95), wc=0, blend="screen",
           motion=lambda t: (lambda p, a: Tf(dx=p[0] - O, dy=p[1] - O, alpha=a,
                                             sx=1 + 0.06 * math.sin(2 * math.pi * t / 1.1),
                                             sy=1 + 0.06 * math.sin(2 * math.pi * t / 1.1), px=O, py=O))(light_xy(t),
                                                                                                         light_a(t)))
    sc.add("light_core", glow_svg(O, O, 46 * K, "s4lc", col="#fff6d8", a=1.0), wc=0, blend="screen",
           motion=lambda t: (lambda p, a: Tf(dx=p[0] - O, dy=p[1] - O, alpha=a))(light_xy(t), light_a(t)))

    # ------------------------------------------------------------ the neighbour lady
    spB = sprite(560, 560, 280, 520, seed=41)
    DB = C._citizen_design("woman", 3, "normal")
    mB = C._metrics(C._ADULT, 0.96, 0.92)
    b_tired = spB.add(C.citizen(spB.ax, spB.ay, K, -1, kind="woman", variant=3, pose="stand", expr="tired"))
    b_happy = spB.add(C.citizen(spB.ax, spB.ay, K, -1, kind="woman", variant=3, pose="cheer", expr="happy"))
    b_thank = spB.add(C.citizen(spB.ax, spB.ay, K, -1, kind="woman", variant=3, pose="cheer", expr="laugh"))
    b_in = spB.add(C.citizen(spB.ax, spB.ay, K, -1, kind="woman", variant=3, pose="walk_b", expr="happy"))
    t_nb_end = t_drop
    sched_b = [(0, b_tired, 0), (t_lift + 0.08, b_happy, 1.0), (t_drop + 0.05, b_thank, 0.8),
               (t_nb_in, b_in, 0.5)]

    def nb_in(t):                                        # stepping in at her door: up, a little smaller, fading
        return M.progress(t, t_nb_in + 0.1, t_nb_in + 0.5, "sine")

    nb_alpha = lambda t: 1 - nb_in(t)
    sc.add("shadowB", doc(C.ground_shadow(NB_X, GY, K, width=115, opacity=0.22)), wc=0,
           motion=lambda t: Tf(alpha=nb_alpha(t)))
    sc.add_dynamic("neighbour", Actor(spB, sched_b, lambda t: (NB_X - 45 * nb_in(t), GY - 70 * nb_in(t)),
                                      alpha=nb_alpha, bper=2.8, phase=0.4))
    noah_actor = Actor(spN, sched, n_pos, walk=n_walkfr, bper=3.0, phase=0.1)
    # a heart from the neighbour
    hx, hy = NB_X + 10, GY - 420 * K
    sc.add("heart", doc(S.g(heart(hx, hy, 70) + heart(hx + 70, hy - 50, 44, "#f4a6b4"), filter="wobble-fine")), wc=0,
           motion=lambda t: pop_tf(t, t_nb_end + 0.05, t_nb_end + 1.5, hx, hy, bob=6))

    # ------------------------------------------------------------ Noah's name ribbon
    rx, ry = X0 + 6, GY - 400 * K - 70
    sc.add("rib_noah", doc(ribbon(rx, ry, "挪亚", col="#e9746a")), wc=0,
           motion=lambda t: pop_tf(t, t_noah + 0.05, t_pray - 0.25, rx, ry, bob=4))

    # ------------------------------------------------------------ the family
    def member(name, t_in, side, z_name, ribbon_label=None, rcol=None, wave_t=None):
        x, y, s, f = grp[name]
        sp = sprite(640, 600, 320, 540, seed=50 + len(z_name))
        st = fam(sp, name, "stand", s=K * s, facing=f, expr="happy")
        stk = fam(sp, name, "stand", s=K * s, facing=f, expr="kind")
        sched_m = [(0, st, 0), (t_in + 0.3, st, 1.0), (T - 0.6, stk, 0.0)]
        if wave_t is not None:
            wv = [fam(sp, name, "wave", s=K * s, facing=f, phase=ph) for ph in (0.0, 0.25, 0.5, 0.75)]
            sched_m = [(0, stk, 0)] + cycle(wave_t[0], wave_t[1], wv, 0.14, hop=0.6) + [(wave_t[1], st, 0.4),
                                                                                         (T - 0.6, stk, 0.0)]
        # stepping forward: from a little behind / beside into the portrait, with a hop on arrival
        def pos(t, x=x, y=y):
            u = M.progress(t, t_in, t_in + 0.3, "out")
            return x + side * 70 * (1 - u), y - 34 * (1 - u)

        def alpha(t):
            return M.progress(t, t_in, t_in + 0.1, "sine")
        sc.add(f"sh_{name}", doc(C.ground_shadow(x, y, K * s, width=115, opacity=0.2)), wc=0,
               motion=lambda t: Tf(alpha=alpha(t)))
        sc.add_dynamic(z_name, Actor(sp, sched_m, pos, alpha=alpha, bper=2.8 + 0.07 * len(name), phase=len(name) * 0.13))
        if ribbon_label:
            bx, by = x, y - 345 * K * s - 60
            sc.add(f"rib_{name}", doc(ribbon(bx, by, ribbon_label, col=rcol, size=50)), wc=0,
                   motion=lambda t, bx=bx, by=by, t0=t_in: pop_tf(t, t0 + 0.1, T + 5, bx, by, bob=3))

    # back row first (drawn behind), then the front row
    member("daughter_in_law1", t_wives + 0.15, 1, "dil1")
    member("shem", t_shem, 0, "shem", "闪", "#5b7fb4")
    member("ham", t_ham, 0, "ham", "含", "#d06a48")
    member("japheth", t_jap, 0, "japheth", "雅弗", "#7aa556")
    member("daughter_in_law0", t_wives, 1, "dil0")
    member("noah_wife", -1.0, 0, "wife", wave_t=(t_drop + 0.6, t_arrive - 0.1))
    # Noah is drawn between his wife and daughter_in_law2 (front row)
    sc.add_dynamic("noah", noah_actor)
    member("daughter_in_law2", t_wives + 0.08, -1, "dil2")

    # sparkles round the whole family at the end
    sc.add_dynamic("fam_sparkle", sparkle_dyn((G - 460, GY - 520, G + 380, GY - 300), count=10, t0=t_wives + 0.3,
                                              t1=T + 1, size=(8, 14), period=1.5, drift=-6, seed=9))

    # ------------------------------------------------------------ butterflies and birds
    bfs = [doc(PR.butterfly(0, 0, 0.8, flap=fl, color="yellow")) for fl in (0, 0.25, 0.5, 0.75)]
    sc.add("bf1", bfs, wc=0.3, frame_at=lambda t: float(int(t * 14) % 4),
           motion=lambda t: Tf(dx=1250 + 220 * math.sin(2 * math.pi * t / 7.0),
                               dy=GY - 330 + 60 * math.sin(2 * math.pi * t / 3.1) + 14 * math.sin(2 * math.pi * t / 0.9)))
    bfs2 = [doc(PR.butterfly(0, 0, 0.7, flap=fl, color="pink")) for fl in (0, 0.25, 0.5, 0.75)]
    sc.add("bf2", bfs2, wc=0.3, frame_at=lambda t: float((int(t * 13) + 2) % 4),
           motion=lambda t: Tf(dx=2350 + 300 * math.sin(2 * math.pi * (t / 8.0 + 0.3)),
                               dy=GY - 520 + 70 * math.sin(2 * math.pi * t / 3.7) + 12 * math.sin(2 * math.pi * t / 0.8)))
    birds = [doc(PR.songbird(0, 0, 0.7, -1, wing=w, color=c) + PR.songbird(110, 40, 0.6, -1, wing=-w, color="yellow"))
             for w, c in ((1, "blue"), (0.5, "blue"), (0, "blue"), (-0.5, "blue"), (-1, "blue"), (-0.5, "blue"),
                          (0, "blue"), (0.5, "blue"))]
    sc.add("birds", birds, wc=0.3, frame_at=lambda t: float(int(t * 16) % 8),
           motion=lambda t: Tf(dx=3200 - 120 * t, dy=380 + 30 * math.sin(t * 1.3)))

    sc.add("fg", [fg_svg(sw) for sw in (-0.5, 0.0, 0.5)], wc=0.7,
           frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.4))

    # ------------------------------------------------------------ CAMERA
    c0 = Cam(1300, 957, 2600)
    c1 = Cam(1180, 1084, 1900)
    c_pray = Cam(1170, 1100, 1800)
    c_nb = Cam(1380, 1084, 1900)
    c_fam = Cam(2180, 1120, 1640)
    keys = [(0.0, c0), (t_diff + 0.2, c0), (t_diff + 1.9, c1), (t_pray, c1), (t_walk, c_pray),
            (t_drop, c_nb), (t_home, c_nb), (max(t_arrive + 0.2, t_shem - 0.1), c_fam), (T, Cam(2182, 1120, 1636))]
    sc.camera = clamp_cam(M.cam_keys(keys, "sine"), SW, SH)

    # ------------------------------------------------------------ SOUND
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("sheep", 1.4, gain_db=-22, pan=-0.6)
    sc.sfx("pop", t_noah + 0.05, gain_db=-12)
    sc.sfx("cloth", t_pray, gain_db=-16)
    sc.sfx("chime", t_pray + 0.15, gain_db=-14)
    sc.sfx("footsteps", t_up + 0.1, dur=t_drop - t_up, gain_db=-15, fade_in=0.1, fade_out=0.2)
    sc.sfx("sparkle", t_walk + 0.1, gain_db=-17)
    sc.sfx("thud", t_drop, gain_db=-14)
    sc.sfx("pop", t_nb_end + 0.08, gain_db=-14, pan=-0.1)
    sc.sfx("footsteps", t_home, dur=t_arrive - t_home, gain_db=-16, fade_in=0.1, fade_out=0.2, pan=0.2)
    for tt in (t_shem, t_ham, t_jap):
        sc.sfx("pop", tt + 0.12, gain_db=-11, pan=0.1)
    sc.sfx("sparkle", t_wives + 0.3, gain_db=-15)
    return sc
