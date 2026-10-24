"""Scene 7 - John 6:11, Mark 6:41. Jesus takes the five loaves and the two fish, looks up to heaven and gives thanks
(warm light from above only - God is never drawn); he breaks the bread and hands it to the disciples, who carry it to
the groups; the bread and the fish in the disciples' baskets never run out, and everyone eats as much as they want.

Starts with a plain 1 s fade from s06_sit: the first second here is pixel-identical to s06's last second (the same
stage, layers, seeds, camera, film-clock breathing / clouds / swallows / flowers / glints, every figure in its END_*
drawing - the world and the cast come from s06_sit's helpers). Jesus stays seated on the teaching rock with the boy's
open basket on his lap (seated versions of look_up_bless / break_bread / give_bread on the library rig; the basket
stays on his lap while he breaks and gives).

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's
beat(); nothing is hard-coded to the take). Times are for the current take:
  0 .. 1.0      s06's last frame: the whole hillside seated, Jesus on his rock with the basket, the boy beside him,
                Peter and John with their empty baskets at their feet
  1.0 ..        the camera glides in to Jesus (wide -> medium by '抬头', a slow reverent push to '感谢')
  '拿起' 1.35   he lifts the basket from his lap to his chest
  '抬头' 3.90   he raises it toward heaven and looks up (thanks); warm light pours down from above (soft beams, a pool of
                light, drifting motes, a gentle warm vignette); the boy looks up in awe, Peter and John in wonder
  '感谢' 5.45   the light swells (chime, sparkle), little sparkles drift down; Peter and John close their eyes; held
  6.3 .. 7.3    the silent pause: the blessing rests - Jesus holds the basket up to heaven in the light (a blink), motes
                and sparkles drift down; at 7.3 the basket comes back to his lap and the light softens (faintly to the cut)
  '然后' 7.75   Peter stoops and picks up his empty basket (8.3) and walks up to Jesus with it (planted-foot strides)
  '他把饼' 8.61  a whole loaf in Jesus's hands; '掰开' 9.32 he breaks it (6 frames, crumbs, crunch); the boy gasps
  '递给' 10.03  Peter holds his basket out; Jesus hands him the piece - it drops in (10.5, sparkle); '门徒再' 11.19
                the basket is suddenly heaped full (sparkle burst, chime), Peter beams, turns and carries it off to the
                people (11.8); John picks up his basket (11.5) and comes forward
  '鱼也是' 13.34 Jesus breaks a fish (13.2-13.9) and hands it into John's basket (14.2 / 14.6, sparkle)
  '分' 15.03    hard cut on the phrase start (14.91) to the families at the front: Philip, Peter and Andrew hand out from
                their heaped baskets - a new piece in the hand on every '分' (15.03 / 15.60 / 16.14 / 16.54) and then on
                and on (~0.8 s per piece); a little sparkle burst at the basket for every piece that keeps coming, steady
                sparkles over the baskets from '饼一直分不完'; the people at the front take each piece and eat
  '鱼也一直' 18.69  Peter and Andrew hand out fish
  '想吃多少' 20.93  every group eats (staggered, nearest first; laughing, yum) while the camera eases back to show them;
                '就吃多少' 22.02 Philip hands the little boy a second piece; he takes it and grins (laugh, hop)
  23.1 .. end   the camera settles; calm hold (2.5 s) for the page turn into s08 (dippaper)
"""
import math
import random

from art import characters as C
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import beat, voice_marks
from stories.noah.scenes.s01_title import snap
from stories.loaves.scenes import s06_sit as S6
from stories.loaves.scenes.s06_sit import (
    BASKET_K, BOY_SIT, BOY_STAND, BS, CAM_END, DISC, END_BOY, END_DISC, END_JESUS, END_WALK, FEATURED, H, JSTAND, RECEIVERS,
    ROCK, W, WALKERS, Actor, Burst, add_groups, add_world, basket_spot, blink, blink_times, boy_svg, cam_path, disc_svg, doc,
    feat_end, feat_svg, ground_basket_svg, hopm, jesus_svg, k_of_y, person_pose, zy)

INK = "#4b3426"


def last_sub(ctx, li, phrase):
    """Start of the last speech sub-segment of the measured phrase (e.g. the second '分' of '分啊分')."""
    for ent in voice_marks(ctx, li):
        if ent[0] == phrase or phrase in ent[0]:
            return ent[3][-1][0]
    return ctx.lines[li].at(phrase)


def phrase_marks(ctx, li, phrase):
    return [ent for ent in voice_marks(ctx, li) if ent[0] == phrase]


# ---------------------------------------------------------------- the disciples' custom drawings (library rig)
def _disc_custom(v, x, y, s, f, ps, expr, item_key=None, phase=0.0, fill=None, food="bread"):
    vi = C._disciple_index(v)
    D, m = C._disciple_design(vi, 0.0, False)
    if item_key:
        D["front"] = C._hooks(C._disciple_lf_items(D, item_key, phase, fill, food, True))
    inner, _ = C._figure(D, m, ps, expr or ps["expr"], C._fsign(f), True)
    return C._wrap_out(inner, x, y, s, f, f"disciple{vi}-lf7")


def disc7_svg(v, x, y, s, key):
    """('stoop', f, expr) hands on the basket rim on the grass | ('carry', f, expr, fill) | ('cwalk', f, ab, fill) |
    ('recv', f, expr, fill) the basket held out low to Jesus | ('hand', f, phase, fill, food, expr) handing out,
    reaching down to someone seated | anything else: s06's disc_svg."""
    kind = key[0]
    if kind == "stoop":
        _, f, expr = key
        bx = 64                                    # the basket stands 64 px (scale 1) toward f, a little behind
        rim = -6 - 104 * BASKET_K
        ps = C._P(t=36, h=-6, drop=30, legs=(("ik", 30, 1), ("ik", -26, 1)),
                  arms=(("ik", "abs", bx + 34, rim + 2, 1), ("ik", "abs", bx - 20, rim + 6, 1)), hands=("fist", "fist"), expr=expr,
                  look=(0.04, 0.07))
        return _disc_custom(v, x, y, s, f, ps, expr)
    if kind == "carry":
        _, f, expr, fill = key
        return C.disciples(x, y, s, f, variant=v, pose="carry_basket", expr=expr, fill=fill)
    if kind == "cwalk":
        _, f, ab, fill = key
        return C.disciples(x, y, s, f, variant=v, pose=f"carry_basket_walk_{ab}", expr="happy", fill=fill)
    if kind == "recv":
        _, f, expr, fill = key
        ps = C._P(t=14, h=12, legs=((10, 3), (-8, -3)), arms=(("ik", "abs", 100, -150, 1), ("ik", "abs", 46, -144, 1)),
                  hands=("fist", "fist"), expr=expr, look=(0.04, 0.05))
        return _disc_custom(v, x, y, s, f, ps, expr, "receive", fill=fill)
    if kind == "hand":
        _, f, ph, fill, food, expr = key
        e = math.sin(math.pi * ph)
        ps = C._P(t=12 + 16 * e, h=10, legs=((10, 3), (-8, -3)), drop=4 + 6 * e,
                  arms=(("ik", "abs", 74, -150, 1), ("ik", "abs", 60 + 52 * e, -158 + 52 * e, 1)), hands=("fist", "fist"),
                  expr=expr, look=(0.04, 0.08))
        return _disc_custom(v, x, y, s, f, ps, expr, "hand_out", phase=ph, fill=fill, food=food)
    return disc_svg(v, x, y, s, key)


# ---------------------------------------------------------------- light from above (God is never drawn)
def beams_svg(cx, top, x_land, y_land):
    """Soft warm beams falling from above the frame onto Jesus."""
    defs = (f'<linearGradient id="lf7bm" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="{y_land}">'
            f'<stop offset="0" stop-color="#fff3c8" stop-opacity="1"/><stop offset="0.65" stop-color="#ffe2a0" stop-opacity="0.7"/>'
            f'<stop offset="1" stop-color="#ffd98a" stop-opacity="0.0"/></linearGradient>')
    b = ""
    for dx0, dx1, w0, w1, op in ((-70, -120, 50, 110, 0.8), (40, 30, 80, 170, 1.0), (150, 190, 44, 100, 0.75), (-170, -260, 30, 80, 0.45),
                                 (250, 340, 26, 80, 0.4)):
        x0, x1 = cx + dx0, x_land + dx1
        b += (f'<path d="M{x0 - w0},{top} L{x1 - w1},{y_land} L{x1 + w1},{y_land} L{x0 + w0},{top} Z" fill="url(#lf7bm)" '
              f'opacity="{op}" filter="url(#soft)"/>')
    return doc(b, defs)


def pool_svg(x, y, rx, ry):
    defs = S.rad_grad("lf7pl", [(0, "#fff4cf", 0.85), (0.45, "#ffe3a0", 0.45), (1, "#ffe3a0", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#lf7pl)"/>', defs)


class Envelope:
    """Piecewise-linear-ish scalar keyed on scene time: keys [(t, v)] eased with sine."""

    def __init__(self, keys):
        self.keys = sorted(keys)

    def __call__(self, t):
        ks = self.keys
        if t <= ks[0][0]:
            return ks[0][1]
        for (ta, a), (tb, b) in zip(ks, ks[1:]):
            if t <= tb:
                return a + (b - a) * M.progress(t, ta, tb, "sine")
        return ks[-1][1]


# ================================================================== the scene
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(7)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731

    # ---- beats
    t_na = b(0, "拿起")
    t_tai = b(0, "抬头")
    t_gx = b(0, "感谢")
    t_l0e = ctx.lines[0].end
    t_rh = b(1, "然后")
    t_ta = b(1, "他把饼")
    t_bai = b(1, "掰开")
    t_dg = b(1, "递给")
    t_mtz = b(1, "门徒再")
    t_fg = b(1, "分给")
    t_yu = b(1, "鱼也是")
    t_l1e = ctx.lines[1].end
    fen = []
    for ent in phrase_marks(ctx, 2, "分啊分"):
        fen += [ent[1], ent[3][-1][0]]
    if len(fen) < 4:
        fen = [b(2, "分", k) for k in range(4)]
    t_byz = b(2, "饼一直")
    t_yz = b(2, "鱼也一直")
    t_xc = b(2, "想吃多少")
    t_jc = b(2, "就吃多少")
    t_l2e = ctx.lines[2].end
    T_CUT = snap(fen[0] - 0.12)                # cut to the families at the front
    shot1 = lambda t: Tf(alpha=1.0 if t < T_CUT else 0.0)          # noqa: E731
    shot2 = lambda t: Tf(alpha=1.0 if t >= T_CUT else 0.0)         # noqa: E731
    always = lambda t: Tf()                                          # noqa: E731  (keeps s06's non-static draw path)

    # ---- the world and the groups (seated; on '想吃多少' they eat, group after group, nearest the camera first)
    add_world(sc, g0, always)
    eat_t = {}
    for g in S6.GROUPS:
        u = (g["x"] - 1300) / 1300.0 + (1300 - g["y"]) / 600.0
        eat_t[g["gi"]] = t_xc - 0.1 + 0.55 * max(0.0, min(1.0, u))

    def plan(g):
        return [(-1, "sit", None), (eat_t[g["gi"]], "eat", 6 if g["row"] >= 3 else 4)]
    add_groups(sc, g0, plan, always)

    # ---- featured front-row people: s06's end drawings; s07: the three who take the bread, the children eat
    recv_of = {id(p): (name, side) for name, g, p, side in RECEIVERS}
    stations = {}
    for name, g, p, side in RECEIVERS:
        d_ = (150 if p["kind"] == "child" else 175)
        y_d = p["y"] - 10 * p["k"]
        s_d = k_of_y(y_d)
        stations[name] = (p["x"] - side * d_ * s_d, y_d, s_d, side, p)
    feat_actors = {}
    for j, (g, p, role) in enumerate(FEATURED):
        a = Actor(f"feat{j}", (p["x"], p["y"]), p["k"], lambda key, p=p: feat_svg7(p, key), zy(p["y"], 0.001), 300 + j, g0)
        a.cut(-1, feat_end(p, role))
        sp = person_pose(p, "sit")
        if id(p) not in recv_of:
            if role == "child":
                a.cut(eat_t[g["gi"]], ("sit_eat", "yum", 0.0), dip=6)
                a.cut(snap(t_jc + 0.3 + 0.2 * (j % 3)), ("sit_laugh", "laugh", 0.0), dip=5)
            elif role == "mother":
                a.cut(eat_t[g["gi"]], (sp, "kind", 0.0), dip=5)
        feat_actors[id(p)] = a
        a.blinks(blink_times(1.2, T - 1.3, rng, 3.4), {})
    # (the receivers' cuts follow their disciple's hand-out beats; built below)

    # ---- Jesus (seated on the rock, the boy's basket on his lap)
    jes = Actor("jesus", JSTAND, S6.JS, lambda key: jesus_svg(key), zy(JSTAND[1]), 109, g0)
    jes.cut(-1, END_JESUS)
    t_lift = snap(t_na - 0.04)
    jes.cut(t_lift, ("lift", "warm", (0.04, -0.02)), dip=5)
    t_bl = snap(t_tai - 0.06)
    jes.cut(t_bl, ("bless", "thanks", 0.0), dip=6)
    t_down = snap(max(t_l0e + 0.35, t_rh - 0.45))   # the blessing rests through the silent pause, then the basket comes down
    jes.cut(t_down, ("lap", "smile", (0.04, 0.05)), dip=5)
    t_loaf = snap(t_ta - 0.1)
    jes.cut(t_loaf, ("break", 0.0, None), dip=4)
    br0 = snap(t_bai - 0.12)
    for q, ph in enumerate((0.2, 0.35, 0.5, 0.65, 0.8, 1.0)):
        jes.cut(br0 + 0.09 * q, ("break", ph, None))
    t_give = snap(t_dg + 0.05)
    jes.cut(t_give, ("give", None, "warm"), dip=4)
    t_back = snap(t_give + 0.42)                  # the piece drops into Peter's basket: his hands go back to the lap
    jes.cut(t_back, ("lap", "warm", (0.04, 0.0)), dip=4)
    t_fish = snap(t_yu - 0.12)
    jes.cut(t_fish, ("break", 0.0, "fish"), dip=4)
    for q, ph in enumerate((0.2, 0.35, 0.5, 0.65, 0.8, 1.0)):
        jes.cut(t_fish + 0.25 + 0.08 * q, ("break", ph, "fish"))
    t_give2 = snap(t_fish + 0.25 + 0.08 * 6 + 0.25)
    jes.cut(t_give2, ("give", "fish", "warm"), dip=4)
    jes.cut(snap(t_give2 + 0.42), ("lap", "smile", (0.04, 0.0)), dip=4)
    jes.blinks(blink_times(1.2, T_CUT - 0.2, rng, 3.0), {
        END_JESUS: ("lap", blink("warm"), (0.03, 0.0)),
        ("bless", "thanks", 0.0): ("bless", blink("thanks"), 0.0),
        ("lap", "warm", (0.04, 0.0)): ("lap", blink("warm"), (0.04, 0.0)),
        ("give", None, "warm"): ("give", None, blink("warm"))})
    jes.extra.append(lambda t: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.4)))
    jes.build(sc)

    # ---- the light from above
    lx, ly = ROCK[0] + 30, ROCK[1] - 150
    light = Envelope([(0, 0), (t_tai - 0.2, 0), (t_tai + 0.8, 0.62), (t_gx - 0.1, 0.7), (t_gx + 0.5, 1.0), (t_l0e + 0.5, 0.95),
                      (t_down - 0.1, 0.92), (t_rh + 0.8, 0.38), (t_yu, 0.32), (T_CUT - 0.3, 0.22), (T_CUT, 0.0)])
    sc.add("beams", beams_svg(ROCK[0] + 60, -40, lx, ly + 120), z=45, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=light(t) * (0.92 + 0.08 * math.sin(2 * math.pi * (g0 + t) / 3.1)) if t < T_CUT else 0.0))
    sc.add("pool", pool_svg(lx - 10, ly, 230, 210), z=zy(ROCK[1], 0.02), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=light(t) * 0.9 if t < T_CUT else 0.0))
    sc.fx.append(FX.tint((255, 226, 160), lambda t: 0.05 * light(t) if t < T_CUT else 0.0, mode="screen"))
    sc.fx.append(FX.vignette(lambda t: 0.32 * light(t) if t < T_CUT else 0.0, color=(70, 44, 30)))
    sc.fx.append(FX.motes((lx - 260, 80, lx + 300, ly + 40), count=26, t0=t_tai, t1=T_CUT - 0.1, color=(255, 240, 200), size=(3, 7),
                          seed=31, alpha=170))
    sc.fx.append(FX.sparkles((lx - 200, ly - 300, lx + 220, ly + 80), count=12, t0=t_gx - 0.2, t1=max(t_l0e + 1.4, t_rh + 0.2), color=(255, 236, 170),
                             size=(8, 15), period=1.4, drift=18, seed=33))   # (t1 below)

    # ---- the boy
    boy = Actor("boy", BOY_STAND, BS, lambda key: boy_svg(key, *(BOY_SIT if key[0].startswith("sit") else BOY_STAND)),
                zy(BOY_STAND[1]), 113, g0)
    boy.cut(-1, END_BOY)
    boy.cut(snap(t_tai + 0.25), ("sit", "awed"), dip=3)
    boy.cut(snap(t_bai + 0.25), ("sit", "surprised"), dip=4)
    boy.cut(snap(t_mtz + 0.15), ("sit", "delighted"), dip=5)
    boy.extra.append(hopm(snap(t_mtz + 0.15), BS, 18, 0.32))
    boy.cut(snap(t_yu + 1.2), ("sit", "happy"))
    boy.blinks(blink_times(1.3, T_CUT - 0.2, rng, 2.8), {END_BOY: ("sit", blink("happy")), ("sit", "happy"): ("sit", blink("happy"))})
    boy.extra.append(lambda t: Tf(sy=1 + 0.008 * math.sin(2 * math.pi * (g0 + t) / 2.6 + 1)))
    boy.build(sc)

    # ---- Peter: picks up his basket, steps up, receives the bread (it fills), carries it off to the people
    v, (px, py) = DISC["peter"]
    sp_ = k_of_y(py)
    pe = Actor("peter", (px, py), sp_, lambda key, v=v, px=px, py=py, s=sp_: disc7_svg(v, px, py, s, key), zy(py), 120 + v, g0)
    pe.cut(-1, END_DISC["peter"])
    pe.cut(snap(t_tai + 0.4), ("stand", -1, "awed"), dip=3)
    pe.cut(snap(t_gx + 0.1), ("stand", -1, "peaceful"), dip=3)
    t_stoop = snap(t_rh + 0.05)
    pe.cut(t_stoop, ("stoop", -1, "happy"), dip=5)
    t_lift_b = snap(t_stoop + 0.5)
    pe.cut(t_lift_b, ("carry", -1, "happy", 0.0), dip=6)
    jx_hand = ROCK[0] + 122 * S6.JS                # Jesus's giving hand (seated)
    rx_target = jx_hand + 92 * sp_                 # Peter stands so the basket's middle is under it
    n_st = max(1, int(round((px - rx_target) / (S6.DISC_ADV * sp_))))
    adv = (px - rx_target) / n_st
    t_w0 = snap(t_dg - 0.3 * n_st - 0.25)
    pe.walk(t_w0, [("cwalk", -1, "a", 0.0), ("cwalk", -1, "b", 0.0)], n_st, 0.3, adv, -1)
    t_recv = snap(t_dg - 0.18)
    pe.cut(t_recv, ("recv", -1, "awed", 0.0), dip=4)
    t_in = snap(t_give + 0.42)
    pe.cut(t_in, ("recv", -1, "awed", 0.5), dip=3)
    t_full = snap(t_mtz + 0.02)
    pe.cut(t_full, ("recv", -1, "amazed", 1.0), dip=5)
    t_go = snap(t_full + 0.6)
    pe.cut(t_go, ("carry", 1, "happy", 1.0), dip=4)
    pe.walk(snap(t_go + 0.3), [("cwalk", 1, "a", 1.0), ("cwalk", 1, "b", 1.0)], 11, 0.3, S6.DISC_ADV * sp_, 1)
    pe.extra.append(lambda t: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.1)))
    pe.gates.append(shot1)
    pe.build(sc)
    bx, by = basket_spot(px, py, sp_, -1)
    sc.add("peter_basket", doc(ground_basket_svg(px, py, sp_, -1, seed=11 + v)), z=zy(by, -0.004), seed=125 + v,
           motion=lambda t: Tf(alpha=1.0 if t < t_lift_b else 0.0))
    bxr = rx_target - 76 * sp_
    sc.fx.append(Burst(bxr, py - 150 * sp_, t_in, n=8, r=(30, 90), dur=0.7, seed=41, size=(7, 13)))
    sc.fx.append(Burst(bxr, py - 160 * sp_, t_full, n=16, r=(60, 200), dur=1.0, seed=43, size=(9, 18)))

    # ---- John: picks up his basket, comes forward, receives the fish
    v, (jx, jy) = DISC["john"]
    sj = k_of_y(jy)
    jo = Actor("john", (jx, jy), sj, lambda key, v=v, jx=jx, jy=jy, s=sj: disc7_svg(v, jx, jy, s, key), zy(jy), 120 + v, g0)
    jo.cut(-1, END_DISC["john"])
    jo.cut(snap(t_tai + 0.55), ("stand", -1, "awed"), dip=3)
    jo.cut(snap(t_gx + 0.25), ("stand", -1, "peaceful"), dip=3)
    jo.cut(snap(max(t_l0e + 0.6, t_rh - 0.1)), ("stand", -1, "happy"), dip=3)
    t_jstoop = snap(t_mtz + 0.3)
    jo.cut(t_jstoop, ("stoop", -1, "happy"), dip=5)
    t_jlift = snap(t_jstoop + 0.5)
    jo.cut(t_jlift, ("carry", -1, "happy", 0.0), dip=6)
    jx_target = jx_hand + 92 * sj + 10
    n_j = max(1, int(round((jx - jx_target) / (S6.DISC_ADV * sj))))
    adv_j = (jx - jx_target) / n_j
    t_jw = snap(max(t_jlift + 0.35, t_give2 - 0.3 * n_j - 0.45))
    t_jl = jo.walk(t_jw, [("cwalk", -1, "a", 0.0), ("cwalk", -1, "b", 0.0)], n_j, 0.3, adv_j, -1)
    t_jrecv = snap(max(t_jl + 0.3, t_give2 - 0.2))
    jo.cut(t_jrecv, ("recv", -1, "awed", 0.0), dip=4)
    t_jin = snap(t_give2 + 0.42)
    jo.cut(t_jin, ("recv", -1, "amazed", 0.5), dip=4)
    jo.extra.append(lambda t: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.1 + 3)))
    jo.gates.append(shot1)
    jo.build(sc)
    bx, by = basket_spot(jx, jy, sj, -1)
    sc.add("john_basket", doc(ground_basket_svg(jx, jy, sj, -1, seed=11 + v)), z=zy(by, -0.004), seed=125 + v,
           motion=lambda t: Tf(alpha=1.0 if t < t_jlift else 0.0))
    sc.fx.append(Burst(jx_target - 76 * sj, jy - 150 * sj, t_jin, n=10, r=(30, 110), dur=0.8, seed=47, size=(7, 14)))

    # ---- Andrew, Philip, James: s06's end drawings until the cut (off camera in shot 1)
    for j, (v, (x0, y0), (x1, y1)) in enumerate(WALKERS):
        s = k_of_y(y0)
        d = Actor(f"walker{j}", (x0, y0), s, lambda key, v=v, x0=x0, y0=y0, s=s: disc_svg(v, x0, y0, s, key), zy(y0), 130 + v, g0)
        d.cut(-1, END_WALK[j])
        d.moves.append(lambda t, dx=x1 - x0: (dx, 0.0))
        d.extra.append(lambda t, v=v: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.2 + v)))
        d.gates.append(shot1)
        d.build(sc)

    # ---- shot 2: the disciples hand out from baskets that never run out
    hand_ts = {}
    loop_per = 0.78
    for k_, (name, (sx, sy, ss, side, p)) in enumerate(stations.items()):
        v = {"philip": 4, "peter": 0, "andrew": 1}[name]
        a = Actor(f"st_{name}", (sx, sy), ss, lambda key, v=v, sx=sx, sy=sy, s=ss: disc7_svg(v, sx, sy, s, key), zy(sy, -0.002),
                  160 + k_, g0)
        food = lambda t: "fish" if t_yz - 0.1 <= t < t_xc - 0.3 and name in ("peter", "andrew") else "bread"   # noqa: E731
        beats_ = [f_ + 0.04 * k_ for f_ in fen]
        tt = fen[-1] + 0.05 * k_ + loop_per * 0.9
        stop = t_jc - 0.75 if name == "philip" else t_jc - 0.2
        while tt < stop:
            beats_.append(tt)
            tt += loop_per * (1.0 + 0.08 * ((k_ + len(beats_)) % 3))
        if name == "philip":
            beats_.append(t_jc + 0.05)            # the second piece for the little boy
        hand_ts[name] = beats_
        a.cut(-1, ("hand", side, 0.0, 1.0, "bread", "happy"))
        for tb in beats_:
            fd = food(tb)
            for q, ph in enumerate((0.25, 0.5, 0.5, 0.75, 0.0)):
                a.cut(tb - 0.16 + 0.11 * q, ("hand", side, ph, 1.0, fd, "happy"))

        a.extra.append(lambda t, k_=k_: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.1 + k_)))
        a.gates.append(shot2)
        a.build(sc)
        # sparkles where the new pieces keep coming
        rim = (sx + side * 40 * ss, sy - 150 * ss)
        for tb in beats_:
            sc.fx.append(Burst(rim[0], rim[1], tb + 0.3, n=6, r=(24, 80), dur=0.6, seed=int(tb * 100) % 97, size=(9, 16)))
        sc.fx.append(FX.sparkles((rim[0] - 50 * ss, rim[1] - 60 * ss, rim[0] + 50 * ss, rim[1] + 20 * ss), count=5, t0=t_byz,
                                 t1=t_jc + 0.6, color=(255, 236, 170), size=(6, 11), period=1.0, drift=-16, seed=51 + k_))
    # the receivers: take each piece (sit_receive, turned to their disciple), then eat; a second piece on '就吃多少'
    for name, g, p, side in RECEIVERS:
        a = feat_actors[id(p)]
        kind_food = lambda t: "fish" if t_yz - 0.1 <= t < t_xc - 0.3 and name in ("peter", "andrew") else "bread"   # noqa: E731
        f_r = -side
        for i, tb in enumerate(hand_ts[name]):
            if tb > t_xc + 0.6 and not (name == "philip" and tb > t_jc):
                continue
            a.cut(tb - 0.12, ("sit_receive", "delighted", 0.0, f_r, kind_food(tb)), dip=4 if i == 0 else None)
            a.cut(tb + 0.42, ("sit_eat", "yum", 0.0, f_r, kind_food(tb)))
        if name == "philip":                    # the little boy takes a second piece and grins
            a.cut(snap(t_jc + 0.5), ("sit_laugh", "laugh", 0.0, f_r, "bread"), dip=6)
            a.extra.append(hopm(snap(t_jc + 0.5), p["k"], 14, 0.3))
    for a in feat_actors.values():
        a.build(sc)

    # ---- camera
    c_j = Cam(668, 876, 1060)
    c_j1 = Cam(676, 872, 1040)
    c_j2 = Cam(712, 882, 1090)
    c_j3 = Cam(736, 886, 1120)
    c_jw = Cam(720, 872, 1300)
    side1 = cam_path([(0.0, CAM_END), (1.0, CAM_END), (t_tai - 0.1, c_jw), (t_gx + 0.2, c_j), (max(t_l0e + 0.6, t_rh - 0.1), c_j1),
                      (t_dg - 0.4, c_j2),
                      (T_CUT, c_j3)], ["linear", "inout", "sine", "sine", "sine", "sine"])
    c_s0 = Cam(1905, 1010, 1150)
    c_s1 = Cam(1890, 1004, 1190)
    c_s2 = Cam(1830, 972, 1440)
    side2 = cam_path([(T_CUT, c_s0), (t_xc - 0.3, c_s1), (min(T - 1.1, t_l2e + 0.3), c_s2), (T, c_s2)], ["sine", "inout", "linear"])
    sc.camera = lambda t: side1(t) if t < T_CUT else side2(t)

    # ---- sound
    sc.sfx("crowd", 0, dur=T + 0.5, gain_db=-21, fade_in=0.6, fade_out=1.0, pan=0.2)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-25, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("cloth", t_lift, gain_db=-19, pan=-0.3)
    sc.sfx("cloth", t_bl, gain_db=-18, pan=-0.3)
    sc.sfx("chime", t_tai + 0.2, gain_db=-17)
    sc.sfx("chime", t_gx, gain_db=-13)
    sc.sfx("sparkle", t_gx + 0.1, gain_db=-16)
    sc.sfx("cloth", t_down, gain_db=-20, pan=-0.3)
    sc.sfx("cloth", t_stoop, gain_db=-20, pan=0.1)
    sc.sfx("crunch", br0, dur=0.7, gain_db=-17, pan=-0.3)
    sc.sfx("footsteps", t_w0, dur=0.3 * n_st + 0.3, gain_db=-22, pan=0.0)
    sc.sfx("sparkle", t_in, gain_db=-17, pan=-0.1)
    sc.sfx("sparkle", t_full, gain_db=-12, pan=-0.1)
    sc.sfx("chime", t_full + 0.05, gain_db=-16)
    sc.sfx("footsteps", t_go + 0.3, dur=3.4, gain_db=-22, fade_out=0.8, pan=0.4)
    sc.sfx("cloth", t_jstoop, gain_db=-21, pan=0.2)
    sc.sfx("crunch", t_fish + 0.25, dur=0.6, gain_db=-19, pan=-0.3)
    sc.sfx("sparkle", t_jin, gain_db=-16, pan=-0.1)
    sc.sfx("crowd", T_CUT, dur=T - T_CUT + 0.5, gain_db=-15, fade_in=0.3, fade_out=1.2, pan=0.2)
    for i, tb in enumerate(fen):
        sc.sfx("pop", tb, gain_db=-19 - (i % 2), pan=0.2 * (i % 3) - 0.2)
    sc.sfx("sparkle", t_byz + 0.1, gain_db=-15, pan=0.2)
    sc.sfx("sparkle", t_yz + 0.1, gain_db=-16, pan=-0.2)
    sc.sfx("cheer", t_xc, dur=2.6, gain_db=-19, fade_in=0.4, fade_out=1.2)
    sc.sfx("crunch", t_xc + 0.4, dur=1.6, gain_db=-21)
    return sc


def feat_svg7(p, key):
    """feat_svg plus s07's keys (pose, expr, phase, facing, food)."""
    if len(key) == 3:
        return feat_svg(p, key)
    pose, expr, ph, f, food = key
    q = dict(p, f=f)
    return S6.person_svg(q, "sit", pose=pose, expr=expr, phase=ph, food=food)
