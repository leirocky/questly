"""Scene 7 - meanwhile, the little lamb alone (Luke 15:4 'the one that is lost'). It opens on exactly the last frame of
s06 (a plain fade: the ninety-nine resting at dusk, the shepherd's lantern going up the path - the same clock, he keeps
walking); on '这时候' it cuts to the lamb on a rocky slope high in the hills, beside a big rock. The lavender dusk turns
to a silver night while it is said, the moon comes up round and bright, the wind blows (the thorn bush and the grass
sway, leaves fly), a round friendly owl blinks and puffs a soft 'hoo'. The lamb trembles and bleats on each '咩', then
curls up behind the rock, peeking out. Never frightening: soft lavender and silver, a big kind moon, a cute owl.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Storm film's
Beats class; nothing hard-coded to the take):
  0 .. 1.0      identical to the end of s06 (the shepherd walking up the path, lantern glowing)
  '这时候'       cut to the rocky slope at dusk: the lamb trots in toward the big rock (bell)
  '小羊一个人'   it stops by the rock and looks around, big worried eyes; '山上' it looks back over its shoulder
  '天黑了'       the light sinks gently (~1.4 s) from lavender dusk to a silver night, the moon rises, stars come out
  '风呼呼地吹'   a gust on each '呼': the thorn bush rocks, the grass bends, leaves blow across (wind); the lamb
                scurries half behind the big rock and crouches, ears down, trembling; after '吹' the owl puffs a soft
                'hoo' (it blinks now and then all through)
  '好害怕'       still trembling behind the rock
  '咩——咩——'    it lifts its head and bleats (sound arcs, a soft baa on each '咩'); the two come close together, so it
                holds the bleat straight through with a little squash on the second '咩', then curls up
  end           it curls up small behind the rock, peeking out, blinking; calm under the big moon (page dip to s08)
"""
import math
import random

from art import props as PR
from art import style as S
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import snap
from stories.storm.scenes.s03_friends import Beats
from stories.lost_sheep.scenes.s05_flock import (H5, INK, W5, Fig, cam_path, clamp01, clamp_cam, clock_loop, doc, env, f1,
                                                 gate, squash,
                                                 lamb_markup)
from stories.lost_sheep.scenes.s06_count import CAM_WIDE, add_dusk_hillside, plan6

# ------------------------------------------------------------------ the rocky slope (shot B, its own stage region)
GB = 980                     # ground line at the big rock
SB = 1.32                    # scale of the slope, the rock, the lamb, the owl
RX0, RX1 = -60, 2700
ROCK_X = 1300
BUSH = (930, GB + 50)
LAMB_STAND = (ROCK_X + 300, GB + 14)               # where it stops beside the rock
LAMB_HIDE = (ROCK_X + 205, GB - 20)                # half behind the rock's right side, peeking out
LAMB_IN = ROCK_X + 760                              # trots in from here
OWL_TREE = (690, GB - 40)
OWL = (810, GB - 385)
MOON = (1765, 440)
MOON_RISE = 140
TIMES7 = (0.62, 0.7, 0.78, 0.85)
CAM_B0 = Cam(1330, 700, 1760)
CAM_B1 = Cam(1400, 742, 1540)


def tod_index7(tm):
    if tm <= TIMES7[0]:
        return 0.0
    for i in range(len(TIMES7) - 1):
        if TIMES7[i] <= tm <= TIMES7[i + 1]:
            return i + (tm - TIMES7[i]) / (TIMES7[i + 1] - TIMES7[i])
    return len(TIMES7) - 1.0


def sky7_svg(time):
    return doc(PR.spring_sky(-10, -10, RX1 + 10, GB - 120, time=time, clouds=0.55, seed=12, scale=SB))


def slope_svg(time, part):
    return doc(PR.rocky_slope(RX0, RX1, GB, SB, time=time, part=part, rock_x=ROCK_X, bush_x=False, seed=4))


def far_details_svg(time):
    """Life on the far hillside of the rocky slope: little round trees along the far ridge, boulders and wiry grass."""
    pal = PR._ls_pal(time)
    t = PR._ls_t(time)
    W_ = RX1 - RX0
    seed = 4
    far = [(RX0 - 60 + (W_ + 120) * i / 30, GB - 260 * SB - 160 * SB * (i / 30) + 30 * SB * math.sin(i * 0.9 + seed))
           for i in range(31)]
    near = [(RX0 - 60 + (W_ + 120) * i / 24, GB - 40 * SB - 90 * SB * (i / 24) + 12 * SB * math.sin(i * 1.7 + seed))
            for i in range(25)]

    def y_at(pts, x):
        return PR._poly_y_at(pts, x)
    rng = random.Random(41)
    b = ""
    for i in range(13):
        x = RX0 + 80 + i * (W_ - 160) / 12 + rng.uniform(-40, 40)
        if abs(x - MOON[0]) < 90:
            continue
        b += PR._round_tree(x, y_at(far, x) + 16 * SB, rng.uniform(0.42, 0.6) * SB, t, seed=60 + i, kind="light")
    for i in range(16):
        x = RX0 + rng.uniform(100, W_ - 100)
        y0, y1 = y_at(far, x) + 40 * SB, y_at(near, x) - 10 * SB
        if y1 - y0 < 30:
            continue
        y = rng.uniform(y0, y1)
        k = 0.5 + 0.6 * (y - y0) / max(1.0, y1 - y0)
        r = rng.uniform(16, 30) * SB * k
        b += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.5)}" ry="{f1(r * 0.8)}" fill="{pal["rock"]}" '
              f'stroke="{INK}" stroke-width="{f1(2.6 * k)}"/>'
              f'<ellipse cx="{f1(x - r * 0.35)}" cy="{f1(y - r * 0.32)}" rx="{f1(r * 0.7)}" ry="{f1(r * 0.25)}" '
              f'fill="{S.mix(pal["rock"], pal["rim"], 0.55)}" opacity="0.75"/>')
    for i in range(9):
        x = RX0 + rng.uniform(100, W_ - 100)
        y = y_at(far, x) + rng.uniform(70, 160) * SB
        if y > y_at(near, x) - 30:
            continue
        b += PR._cluster([(x - 16 * SB, y, 16 * SB), (x + 12 * SB, y - 2 * SB, 18 * SB), (x, y - 13 * SB, 16 * SB)],
                         S.mix(pal["tree"], pal["dark"], 0.3), 2.4)
    b += PR._grass_strokes(RX0, RX1, min(p[1] for p in far) + 60, GB - 60, 80, 43, S.mix(pal["dark"], pal["near"], 0.4),
                           0.9 * SB)
    return doc(S.g(b, filter="wobble"))


def moon_svg(time):
    k = clamp01((PR._ls_t(time) - 0.45) / 0.35)
    mx, my = MOON
    mr = 66 * SB
    out = PR._ls_glow(mx, my, mr * 4.6, mr * 4.6, 0.6 * k, "s7moon", "#f6f4e6", "#b9c8e6")
    out += (f'<circle cx="{f1(mx)}" cy="{f1(my)}" r="{f1(mr)}" fill="{PR.MOON_SILVER}" '
            f'stroke="{S.mix(INK, PR.MOON_SILVER, 0.5)}" stroke-width="{f1(3.2 * SB)}"/>')
    for (dx, dy, r) in ((-0.30, -0.18, 0.18), (0.25, 0.20, 0.13), (0.10, -0.38, 0.09), (-0.12, 0.34, 0.10)):
        out += f'<circle cx="{f1(mx + dx * mr)}" cy="{f1(my + dy * mr)}" r="{f1(r * mr)}" fill="#e2ddc6" opacity="0.8"/>'
    out += (f'<path d="M{f1(mx - mr * 0.62)},{f1(my - mr * 0.5)} A{f1(mr * 0.8)},{f1(mr * 0.8)} 0 0 1 '
            f'{f1(mx + mr * 0.2)},{f1(my - mr * 0.78)}" fill="none" stroke="#fffdf4" stroke-width="{f1(4 * SB)}" '
            f'opacity="0.7"/>')
    return doc(S.g(out, filter="wobble"))


def owl_tree_svg(time):
    """A small gnarled tree on the left with a long branch for the owl."""
    pal = PR._ls_pal(time)
    bark = PR._lt("#7a5a44", time, 0.8)
    x, y = OWL_TREE
    s = SB
    trunk = (f"M{f1(x - 40 * s)},{f1(y + 30 * s)} C{f1(x - 30 * s)},{f1(y - 120 * s)} {f1(x - 60 * s)},{f1(y - 230 * s)} "
             f"{f1(x - 20 * s)},{f1(y - 330 * s)} C{f1(x - 5 * s)},{f1(y - 370 * s)} {f1(x + 20 * s)},{f1(y - 380 * s)} "
             f"{f1(x + 34 * s)},{f1(y - 360 * s)} C{f1(x + 10 * s)},{f1(y - 300 * s)} {f1(x + 20 * s)},{f1(y - 160 * s)} "
             f"{f1(x + 42 * s)},{f1(y + 30 * s)} Z")
    b = f'<path d="{trunk}" fill="{bark}" stroke="{INK}" stroke-width="{f1(4 * s)}" stroke-linejoin="round"/>'
    # branches
    for (ax, ay, cy, bx_, by_, w) in ((x + 12 * s, OWL[1] + 24, OWL[1] + 14, OWL[0] + 160 * s, OWL[1] - 4, 15),
                                      (x - 30 * s, y - 250 * s, y - 320 * s, x - 150 * s, y - 330 * s, 11),
                                      (x + 5 * s, y - 360 * s, y - 440 * s, x + 60 * s, y - 470 * s, 9)):
        d = f"M{f1(ax)},{f1(ay)} Q{f1((ax + bx_) / 2)},{f1(cy)} {f1(bx_)},{f1(by_)}"
        b += (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f1((w + 7) * s)}" stroke-linecap="round"/>'
              f'<path d="{d}" fill="none" stroke="{bark}" stroke-width="{f1(w * s)}" stroke-linecap="round"/>')
    # a few round leaf clumps
    leaf = S.mix(pal["tree"], pal["dark"], 0.2)
    for (cx, cy, r) in ((x - 150 * s, y - 345 * s, 38), (x + 64 * s, y - 486 * s, 34), (OWL[0] + 172 * s, OWL[1] - 10, 26),
                        (x - 40 * s, y - 390 * s, 30)):
        b += (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r * s + 3.5)}" fill="{INK}"/>'
              f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r * s)}" fill="{leaf}"/>'
              f'<ellipse cx="{f1(cx - r * 0.3 * s)}" cy="{f1(cy - r * 0.35 * s)}" rx="{f1(r * 0.4 * s)}" ry="{f1(r * 0.22 * s)}" '
              f'fill="{pal["rim"]}" opacity="0.35"/>')
    return doc(S.g(b, filter="wobble"))


def bush_svg(time):
    return doc(PR.thorn_bush(BUSH[0], BUSH[1], SB, time=time, sway=0.0, part="all", seed=4))


def tufts_svg(k, time):
    """Foreground wiry grass tufts bending in the wind (frame k: 0 upright .. 2 bent hard)."""
    pal = PR._ls_pal(time)
    rng = random.Random(15)
    b = ""
    for i in range(30):
        x = RX0 + 40 + i * 92 + rng.uniform(-24, 24)
        y = GB + 205 + rng.uniform(-10, 40)
        h = rng.uniform(46, 86)
        lean = -(k * 9 + rng.uniform(-2, 2)) - 2
        col = S.mix(pal["dark"], pal["near"], rng.uniform(0.1, 0.45))
        b += (f'<path d="M{f1(x - 12)},{f1(y)} Q{f1(x - 8 + lean)},{f1(y - h * 0.6)} {f1(x - 4 + lean * 1.8)},{f1(y - h)} '
              f'Q{f1(x)},{f1(y - h * 0.5)} {f1(x + 2)},{f1(y)} M{f1(x)},{f1(y)} Q{f1(x + 6 + lean)},{f1(y - h * 0.7)} '
              f'{f1(x + 12 + lean * 1.6)},{f1(y - h * 0.86)} Q{f1(x + 10)},{f1(y - h * 0.4)} {f1(x + 12)},{f1(y)} Z" '
              f'fill="{col}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>')
    return doc(S.g(b, filter="wobble-fine"))


def leaf_svg(x, y, col, s=1.0):
    d = (f"M{f1(x - 16 * s)},{f1(y)} Q{f1(x - 4 * s)},{f1(y - 12 * s)} {f1(x + 16 * s)},{f1(y)} "
         f"Q{f1(x - 4 * s)},{f1(y + 12 * s)} {f1(x - 16 * s)},{f1(y)} Z")
    return doc(S.g(f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="2.4"/>'
                   f'<path d="M{f1(x - 14 * s)},{f1(y)} L{f1(x + 12 * s)},{f1(y)}" stroke="{INK}" stroke-width="1.6" '
                   f'opacity="0.6"/>', filter="wobble-fine"))


def star_svg(x, y, r):
    w = r * 0.22
    pts = [(x, y - r), (x + w, y - w), (x + r, y), (x + w, y + w), (x, y + r), (x - w, y + w), (x - r, y), (x - w, y - w)]
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    return doc(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.9)}" fill="#f6f2e0" opacity="0.25"/>'
               f'<path d="{d}" fill="#fbf8ea"/><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.2)}" fill="#fffdf4"/>')


def owl_draw(time):
    def d(st):
        blink, hoot = st
        return PR.owl(OWL[0], OWL[1], 0.95 * SB, 1, pose="perch", blink=blink, hoot=hoot, branch=False, time=time)
    return d


# ------------------------------------------------------------------ the scene
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    b = Beats(ctx)
    rng = random.Random(7)

    t_zhe = b.at(0, "这时候")
    t_xy = b.at(0, "小羊一个人在山上")
    t_shan = b.at(0, "小羊一个人在山上", 6)
    t_tian = b.at(0, "天黑了")
    t_feng = b.at(0, "风呼呼地吹")
    t_hu1 = b.at(0, "风呼呼地吹", 1)
    t_hu2 = b.at(0, "风呼呼地吹", 2)
    t_chui = b.at(0, "风呼呼地吹", 4)
    t_pa = b.at(1, "小羊好害怕", 2)
    t_jiao = b.at(1, "一直叫")
    t_m1 = b.at(1, "咩——咩——")
    t_m2 = b.at(1, "咩——咩——", 3)
    t_cut = snap(max(1.25, b.end(0, "这时候") + 0.06))

    # ================================================================ shot A: s06's last frame, the same clock
    try:
        tl = load_timeline()
        s6 = next(s for s in tl["scenes"] if s["id"] == "s06_count")
        ctx6 = context("s06_count", tl)
        offset = ctx.start - s6["start"]
        _, t_go6, _ = plan6(ctx6)
    except Exception:
        offset, t_go6 = 34.17, 28.9
    add_dusk_hillside(sc, g0, gate(-1e9, t_cut), offset, t_go6)
    shotB = gate(t_cut, 1e9)

    # ================================================================ shot B: the rocky slope, dusk -> night
    # dusk -> night: a gentle ~1.4 s fall of the light on '天黑了' (sine over 2.3 s; 80 % of it in the middle 1.36 s)
    night = lambda t: M.progress(t, t_tian - 0.25, t_tian + 2.05, "sine")

    def tod(t):
        return 0.62 + 0.04 * M.progress(t, t_cut, t_tian, "sine") + 0.19 * night(t)
    tfa = lambda t: tod_index7(tod(t))
    sc.add("sky7", [sky7_svg(tm) for tm in TIMES7], z=20, frame_at=tfa, seed=701, motion=shotB)
    # twinkling stars as the night comes
    srng = random.Random(21)
    for i in range(26):
        x, y = srng.uniform(300, RX1 - 300), srng.uniform(60, 480)
        if math.hypot(x - MOON[0], y - MOON[1]) < 240:
            continue
        r = srng.uniform(9, 16)
        per, ph = srng.uniform(2.0, 3.8), srng.random()

        def sm(t, per=per, ph=ph, x=x, y=y):
            a = max(0.0, math.sin(2 * math.pi * ((t + g0) / per + ph))) ** 2 * M.progress(t, t_tian, t_feng + 0.8)
            return Tf(alpha=a * (1.0 if t >= t_cut else 0.0), sx=0.6 + 0.4 * a, sy=0.6 + 0.4 * a, px=x, py=y)
        sc.add(f"star{i}", star_svg(x, y, r), z=20.05 + 0.001 * i, wc=0, seed=720 + i, motion=sm)
    sc.add("moon", [moon_svg(tm) for tm in TIMES7], z=20.1, frame_at=tfa, seed=702, wc=0.5,
           motion=M.combine(lambda t: Tf(dy=MOON_RISE * (1 - M.progress(t, t_cut, t_feng + 1.2, "out")), px=MOON[0], py=MOON[1]),
                            shotB))
    sc.add("slope_back", [slope_svg(tm, "back") for tm in TIMES7], z=21, frame_at=tfa, seed=703, motion=shotB)
    sc.add("far_details", [far_details_svg(tm) for tm in TIMES7], z=21.05, frame_at=tfa, seed=710, motion=shotB)
    sc.add("owl_tree", [owl_tree_svg(tm) for tm in (0.62, 0.85)], z=21.2, seed=704,
           frame_at=night, motion=shotB)
    # the thorn bush rocks in the gusts
    gust = lambda t: (env(t, t_hu1 - 0.15, t_hu1 + 0.55, 0.15, 0.35) + env(t, t_hu2 - 0.12, t_hu2 + 0.7, 0.15, 0.45) +
                      0.35 * env(t, t_feng - 0.2, t_pa, 0.4, 0.8))
    sc.add("bush", [bush_svg(tm) for tm in (0.62, 0.85)], z=21.3, seed=705,
           frame_at=night,
           motion=M.combine(lambda t: Tf(rot=-(4.5 * gust(t)) * (0.8 + 0.2 * math.sin(2 * math.pi * t / 0.45))
                                         - 0.6 * math.sin(2 * math.pi * (t + g0) / 3.1), px=BUSH[0], py=BUSH[1]), shotB))
    # the owl: blinks, a soft hoot near the end
    owl = Fig("owl", owl_draw(0.75), OWL, 0.95 * SB, 21.4, g0, seed=706)
    owl.cut(0, (0.0, 0.0))
    for tb in (t_cut + 0.9, t_xy + 1.7, t_pa + 0.3, T - 2.6):
        owl.cut(tb, (1.0, 0.0), dip=False)
        owl.cut(tb + 0.14, (0.0, 0.0), dip=False)
    t_hoo = t_chui + 0.35
    for i, hv in enumerate((0.6, 1.0, 1.0, 0.6, 0.0)):
        owl.cut(t_hoo + 0.16 * i, (0.0, hv), dip=False)
    owl.mots += [lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * (t + g0) / 2.7)), shotB]
    owl.build(sc)

    # the lamb: trots in, stops by the rock, looks around; scurries half behind it in the gust; trembles, bleats, hides
    sx_, sy_ = LAMB_STAND
    hx_, hy_ = LAMB_HIDE
    t_in0 = t_cut + 0.05
    t_in1 = t_xy + 0.8
    n_steps = 12
    step_t = [t_in0 + (t_in1 - t_in0) * i / n_steps for i in range(n_steps)]
    step_dx = (sx_ - LAMB_IN) / n_steps
    t_hop = t_hu1 - 0.12
    HOP = 0.5                                     # the scurry behind the rock: one 0.5 s hop (animated)

    def lpos(t):
        """The lamb's anchor (continuous)."""
        if t < t_hop:
            x = LAMB_IN + sum(step_dx * M.progress(t, ts - 0.02, ts + 0.1, "sine") for ts in step_t)
            y = sy_ - sum(5 * SB * math.sin(math.pi * clamp01((t - ts + 0.02) / 0.14)) for ts in step_t
                          if ts - 0.02 <= t <= ts + 0.12)
            return x, y
        u = M.progress(t, t_hop, t_hop + HOP, "sine")
        return sx_ + (hx_ - sx_) * u, sy_ + (hy_ - sy_) * u - 10 * SB * math.sin(math.pi * clamp01((t - t_hop) / HOP))

    def lst(pose, f=-1, at=LAMB_STAND, tm=0.66, eyes="open", ph=0.0):
        return (pose, ph, at[0], at[1], f, eyes, tm)

    def ldraw(st, k=None):
        pose, ph, x, y, f, eyes, tm = st
        if k is not None:
            ph = k / 4.0
        return lamb_markup(x, y, pose, ph, f, eyes, tm, s=SB)

    lamb = Fig("lamb", ldraw, LAMB_STAND, SB, 21.5, g0, seed=707, pivot=lambda st: (st[2], st[3]))
    lamb.cut(0, lst("walk_b"))
    for i, ts in enumerate(step_t):
        lamb.cut(ts - 0.02, lst("walk_a" if i % 2 == 0 else "walk_b"), dip=False)
    look = lst("look_around")
    lamb.cut(t_in1 + 0.06, look, depth=5)
    lamb.cut(max(t_shan, t_in1 + 0.62), lst("look_around", ph=0.6), depth=4)       # looks back (>= 0.5 s each)
    look2 = lst("look_around", tm=0.76)
    lamb.cut(t_tian + 0.25, look2, depth=4)
    hop = lst("hop", -1, LAMB_STAND, 0.85)
    lamb.loops[hop] = (5, lambda t: int(clamp01((t - t_hop) / HOP) * 5 - 1e-6))     # phase k/4: 0 .. 1
    lamb.cut(t_hop, hop, depth=4)
    scared = lst("scared", 1, LAMB_HIDE, 0.85)
    lamb.loops[scared] = (4, clock_loop(g0, 0.07))
    lamb.cut(t_hop + HOP, scared, depth=7)
    bleat = lst("bleat", 1, LAMB_HIDE, 0.85)
    lamb.loops[bleat] = (4, clock_loop(g0, 0.09))
    hide = lst("hide", 1, LAMB_HIDE, 0.85)
    lamb.cut(t_m1 - 0.08, bleat, depth=4)
    if t_m2 - t_m1 < 0.7:
        # the two '咩' come close together: hold the bleat straight through (a little squash accents the second one),
        # then curl up behind the rock - no 2-frame flash of another pose in between
        lamb.mots.append(squash(t_m2 - 0.02, SB, LAMB_HIDE, 5.0))
    else:
        lamb.cut(t_m1 + 0.32, scared, dip=False)
        lamb.cut(t_m2 - 0.08, bleat, depth=4)
    t_hide = max(t_m2 + 0.42, t_m1 + 0.55)
    lamb.cut(t_hide, hide, depth=7)
    lamb.add_blinks({look: lst("look_around", eyes="closed"), look2: lst("look_around", tm=0.76, eyes="closed"),
                     hide: lst("hide", 1, LAMB_HIDE, 0.85, eyes="closed")}, t_in1, T, rng, every=(1.5, 2.4))

    def lmot(t):
        st = lamb.state_at(t)
        if st[0] in ("walk_a", "walk_b", "hop"):
            x, y = lpos(t)
            return Tf(dx=x - st[2], dy=y - st[3])
        return Tf()
    lamb.mots += [lmot, lambda t: Tf(sy=1 + 0.022 * math.sin(2 * math.pi * (t + g0) / 1.9)), shotB]
    lamb.build(sc)
    # soft moonlight round the rock and the lamb once the moon is up (silver, gentle)
    ml = doc(PR._ls_glow(ROCK_X + 120, GB - 60, 620, 330, 1.0, "s7pool", "#eef2ff", "#b9c8e6"))
    sc.add("moon_pool", ml, z=21.55, wc=0, blend="screen", seed=730,
           motion=M.combine(lambda t: Tf(alpha=0.28 * M.progress(t, t_tian + 0.2, t_feng + 1.4, "sine")), shotB))
    sky_glow = doc(PR._ls_glow(MOON[0], MOON[1], 900, 700, 1.0, "s7sky", "#e8ecfb", "#8ea6d6"))
    sc.add("moon_glow", sky_glow, z=20.15, wc=0, blend="screen", seed=731,
           motion=M.combine(lambda t: Tf(alpha=0.3 * M.progress(t, t_tian - 0.2, t_feng + 1.2, "sine"),
                                         dy=MOON_RISE * (1 - M.progress(t, t_cut, t_feng + 1.2, "out")),
                                         px=MOON[0], py=MOON[1]), shotB))
    sc.add("slope_front", [slope_svg(tm, "front") for tm in TIMES7], z=21.6, frame_at=tfa, seed=708, motion=shotB)
    sc.add("tufts", [tufts_svg(k, 0.8) for k in range(3)], z=21.8, seed=709, wc=0.8,
           frame_at=lambda t: float(min(2, int(2.6 * gust(t))) if gust(t) > 0.12 else (0, 1)[int((t + g0) / 0.9) % 2]),
           motion=shotB)
    # leaves blowing across on the gusts
    lrng = random.Random(33)
    for i in range(7):
        t0 = t_hu1 - 0.3 + 0.18 * i + lrng.uniform(0, 0.25)
        y0 = lrng.uniform(500, 1150)
        x0 = 2300 + lrng.uniform(0, 300)
        dur = lrng.uniform(1.4, 2.1)
        col = S.mix("#8ea86a", "#b0a0c8", lrng.random())
        sc.add(f"leaf{i}", leaf_svg(x0, y0, col, lrng.uniform(0.9, 1.4)), z=21.9 + 0.001 * i, seed=740 + i, wc=0.4,
               motion=lambda t, t0=t0, dur=dur, x0=x0, y0=y0, i=i: (lambda u: Tf(
                   dx=-1900 * u, dy=-120 * math.sin(math.pi * u) + 40 * math.sin(2 * math.pi * u * 2 + i),
                   rot=540 * u, px=x0, py=y0,
                   alpha=(1.0 if t >= t_cut else 0.0) * (1 - M.progress(u, 0.75, 1.0)) * M.progress(u, 0.0, 0.08)))(
                   clamp01((t - t0) / dur)))

    # ================================================================ camera
    cam_a = clamp_cam(CAM_WIDE)                      # exactly s06's last camera (cam_path clamps)
    camA = lambda t: cam_a
    cam_end = Cam(1410, 736, 1400)
    camB = cam_path([(t_cut, CAM_B0), (t_xy + 0.6, CAM_B0), (t_pa, CAM_B1), (T - 1.0, cam_end), (T, cam_end)],
                    ["linear", "inout", "sine", "linear"])
    sc.camera = lambda t: camA(t) if t < t_cut else camB(t)

    # ================================================================ sound
    sc.sfx("night", 0, dur=T + 0.4, gain_db=-22, fade_in=0.3, fade_out=0.8)
    sc.sfx("footsteps", 0, dur=t_cut + 0.2, gain_db=-26, pan=0.3, fade_in=0.2, fade_out=0.2)
    sc.sfx("sparkle", t_cut + 0.2, gain_db=-25, root=91, pan=0.2)
    sc.sfx("wind_soft", t_tian - 0.5, dur=T - t_tian + 0.9, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("storm_wind", t_hu1 - 0.3, dur=1.5, gain_db=-24, fade_in=0.3, fade_out=0.8)
    sc.sfx("whoosh", t_hu1 - 0.1, gain_db=-22, pan=-0.3)
    sc.sfx("whoosh", t_hu2 - 0.1, gain_db=-23, pan=0.3)
    sc.sfx("sheep", t_m1 - 0.02, gain_db=-20, pan=0.1, pitch=1.35)
    sc.sfx("sheep", t_m2 - 0.02, gain_db=-20, pan=0.1, pitch=1.4)
    return sc
