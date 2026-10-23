"""Scene 2 - the opening question, at a modern street festival: colourful shop-houses with striped awnings, bunting and
red paper lanterns across the street, confetti in the air, a parade float with a big smiling sun mascot and balloons
gliding past behind a thick wall of grown-ups' backs. In front of the wall: the little boy in the royal-blue tracksuit
and yellow cap, holding his dad's hand (parent kind='dad', variant=1).

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers; fallback: the
subtitle chunks):
  start        calm, wide frame (1 s cross-dissolve from the title page; the boy and his dad stand on the right where
               the tree and Zacchaeus were, the float is still off-screen left so its sun mascot never doubles with
               anything on the title page): the float rolls in from the left and slows to a glide, the sun's rays
               turn, the balloons bob, confetti flutters, the bunting flaps, the crowd shuffles (phones and little
               flags bob); the boy holds his dad's hand and gazes up at the backs, dad smiles at the parade
  '小朋友'      the boy lets go and trots two steps up to the wall (planted-foot steps); the camera eases in
  '你有没有'    on tiptoe, reaching up (frustrated)
  '被前面的大人挡住' two hops ('jump_see': crouch, a real arc in the air, land) - still only backs
  '什么都看不见' on tiptoe again, wobbling; on '看不见' he drops back onto his heels with a pout
  pause 0.8 s  arms folded, pouting at the wall (frustrated but cute); dad glances down and notices
  '有一个人也是这样' the boy looks round at us, pouting ('me too!'); dad smiles knowingly and steps up behind him
  '可是'        dad crouches and takes him under the arms (the boy surprised and delighted)
  '他想了一个好办法' dad lifts him (lift phases 0 -> 1, 8 drawings) onto his shoulders (whoosh); on '法' the boy is up,
               waving both arms and beaming above the crowd; then he points at the parade (sparkle). The camera rises
               and opens out to show the float he can now see. Calm last frame for the page turn into s03.
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
from stories.nativity.scenes.s01_title import Fig, beat, breath, dip, doc, hop, keyed, snap
from stories.noah.scenes.s01_title import f1
from stories.zacchaeus.scenes.s01_title import EX, Confetti, Patch, safe_camera, stepped

INK = P["ink"]

CY, CS = 902, 0.9                   # the crowd's front row (street_festival y) and scale
PS = 1.3                            # the boy and his dad (closer to us)
FY = 1060                           # their ground line
XB1 = 1240                          # where the boy stands at the wall (and is lifted)
XB0 = XB1 + 128                     # where he holds dad's hand at first (two planted-foot strides back)
XD0 = XB0 + C.CHILD_HOLD["dad"][0] * PS        # dad at first
LIFT_DX = 60 * PS                   # parent 'lift': the boy stands this far in front of dad's anchor
XDL = XB1 + LIFT_DX                 # dad's anchor for the lift and the shoulder ride
FLOAT = (640, 0.72)                 # the parade float: drawn at this x, scale


def float_dx(t):
    """The float rolls in from beyond the left edge (off-screen during the dissolve), slows down and glides on."""
    return -1040 + 958 * (1 - math.exp(-t / 2.5)) + 14.0 * t


# ================================================================== drawings

def _no_confetti(orig):
    def rect(*a, **kw):
        if "rotate(" in str(kw.get("extra", "")):          # street_festival's baked confetti: we animate our own
            return ""
        return orig(*a, **kw)
    return rect


def street_svg():
    """The festival street without its float (we animate our own) and without the frozen confetti."""
    with Patch(_rect=_no_confetti(PR._rect)):
        body = PR.street_festival(-60, W + 60, CY, CS, part="back", seed=2, bottom=H + 60, float_x=-9999)
    return doc(body)


def street_shade_svg():
    """A soft shadow band where the crowd stands and a little warm light on the road in front."""
    b = (f'<rect x="-40" y="{CY - 40}" width="{W + 80}" height="70" rx="30" fill="#6a6058" opacity="0.18" '
         f'filter="url(#soft)"/>')
    b += f'<ellipse cx="{W * 0.6}" cy="{FY + 40}" rx="900" ry="90" fill="#fffaf0" opacity="0.22" filter="url(#blur-md)"/>'
    return doc(b)


def float_body_svg():
    """The parade float (seen over the crowd): a blue skirted wagon with yellow scallops, a striped pole holding the sun
    mascot up, pennants at its corners."""
    fx, s = FLOAT
    fy = CY - 300 * CS
    k = s
    out = PR._p(f"M{f1(fx - 300 * k)},{f1(fy)} L{f1(fx - 280 * k)},{f1(fy - 120 * k)} L{f1(fx + 280 * k)},{f1(fy - 120 * k)} "
                f"L{f1(fx + 300 * k)},{f1(fy)} Z", "#3f8fd0", 3.6 * k)
    for j in range(12):
        xx = fx - 270 * k + j * 49 * k
        out += PR._p(f"M{f1(xx)},{f1(fy - 120 * k)} q{f1(24 * k)},{f1(26 * k)} {f1(49 * k)},0", "#f2c43c", 2.6 * k)
    for j in range(6):
        xx = fx - 240 * k + j * 96 * k
        out += f'<circle cx="{f1(xx)}" cy="{f1(fy - 60 * k)}" r="{f1(9 * k)}" fill="#fff3c4" stroke="{INK}" stroke-width="{f1(2.2 * k)}"/>'
    sx_, sy_ = fx, fy - 330 * k
    out += PR._rect(fx - 9 * k, sy_ + 100 * k, 18 * k, fy - 120 * k - sy_ - 100 * k, "#f6ecd8", 2.8 * k)
    for j in range(4):
        yy = sy_ + 120 * k + j * 40 * k
        out += PR._p(f"M{f1(fx - 9 * k)},{f1(yy)} L{f1(fx + 9 * k)},{f1(yy - 14 * k)}", sw=6 * k, stroke="#e2503c")
    for sd in (-1, 1):
        px = fx + sd * 270 * k
        out += PR._line(px, fy - 120 * k, px, fy - 250 * k, sw=3 * k, color="#6a5a4a")
        out += PR._p(f"M{f1(px)},{f1(fy - 250 * k)} L{f1(px + sd * 50 * k)},{f1(fy - 236 * k)} L{f1(px)},{f1(fy - 222 * k)} Z",
                     PR.FESTIVAL_COLS[(sd + 1) % 7], 2.4 * k)
    return doc(S.g(out, filter="wobble-fine"))


def sun_centre():
    fx, s = FLOAT
    return fx, CY - 300 * CS - 330 * s


def rays_svg():
    sx_, sy_ = sun_centre()
    k = FLOAT[1]
    return doc(S.g(PR._p(S.rays(sx_, sy_, 120 * k, 190 * k, n=12, width_deg=14, rot=0), "#f6a43c", 2.6 * k),
                   filter="wobble-fine"))


def sun_face_svg(blink=False):
    sx_, sy_ = sun_centre()
    k = FLOAT[1]
    out = PR._circ(sx_, sy_, 120 * k, "#f6c84a", 4 * k)
    if blink:
        for sd in (-1, 1):
            out += PR._p(f"M{f1(sx_ + sd * 40 * k - 14 * k)},{f1(sy_ - 16 * k)} q{f1(14 * k)},{f1(10 * k)} {f1(28 * k)},0",
                         sw=5 * k)
    else:
        out += PR._circ(sx_ - 40 * k, sy_ - 16 * k, 12 * k, "#3a2a20", 0) + PR._circ(sx_ + 40 * k, sy_ - 16 * k, 12 * k, "#3a2a20", 0)
        out += PR._circ(sx_ - 36 * k, sy_ - 20 * k, 4 * k, "#fffaf0", 0) + PR._circ(sx_ + 44 * k, sy_ - 20 * k, 4 * k, "#fffaf0", 0)
    out += PR._p(f"M{f1(sx_ - 50 * k)},{f1(sy_ + 26 * k)} Q{f1(sx_)},{f1(sy_ + 76 * k)} {f1(sx_ + 50 * k)},{f1(sy_ + 26 * k)}", sw=6 * k)
    out += PR._ell(sx_ - 70 * k, sy_ + 24 * k, 18 * k, 11 * k, "#f08a6a", 0) + PR._ell(sx_ + 70 * k, sy_ + 24 * k, 18 * k, 11 * k, "#f08a6a", 0)
    return doc(S.g(out, filter="wobble-fine"))


BALLOONS = ((-220, -330), (-160, -420), (190, -380), (240, -300), (-250, -230), (150, -470))


def balloon_svg(j):
    fx, k = FLOAT
    fy = CY - 300 * CS
    bx_, by_ = BALLOONS[j]
    col = PR.FESTIVAL_COLS[j % len(PR.FESTIVAL_COLS)]
    cx, cy = fx + bx_ * k, fy + by_ * k
    out = PR._line(cx, cy + 40 * k, fx + bx_ * 0.6 * k, fy - 120 * k, sw=1.8 * k, color="#6a5a4a")
    out += PR._ell(cx, cy, 30 * k, 38 * k, col, 3 * k)
    out += PR._p(f"M{f1(cx - 6 * k)},{f1(cy + 37 * k)} L{f1(cx + 6 * k)},{f1(cy + 37 * k)} L{f1(cx)},{f1(cy + 46 * k)} Z", col, 2.2 * k)
    out += PR._ell(cx - 10 * k, cy - 14 * k, 7 * k, 10 * k, "#fffaf0", 0, extra='opacity="0.7"')
    return doc(S.g(out, filter="wobble-fine")), (fx + bx_ * 0.6 * k, fy - 120 * k)


NCB = 8                             # crowd arm-bob drawings per loop (phones and flags)


def crowd_people(seed=5):
    """The wall of grown-ups' backs (modern festival-goers from behind), two rows: [(row, x, y, scale, kind, h, seed, f)]."""
    rng = random.Random(seed)
    out = []
    for r in (1, 0):
        sp = 132 * CS
        x = -90 + (sp / 2 if r else 0)
        j = 0
        while x < W + 90:
            out.append((r, x + rng.uniform(-14, 14), CY - 36 * CS * r, CS * (1 - 0.04 * r), (j * 3 + r * 5 + 1) % 8,
                        rng.uniform(305, 350), seed + j + 10 * r, 1 if rng.random() < 0.5 else -1))
            x += sp * rng.uniform(0.92, 1.08)
            j += 1
    return out


def crowd_group_svg(people, ph):
    out = ""
    for r, x, y, s, kind, h, sd, f in people:
        out += PR._place(PR._modern_back(kind, h, sd, ph), x, y, s, f, filt=None)
    return doc(S.g(out, filter="wobble-fine"))


def crowd_shadow_svg(people):
    b = ""
    for r, x, y, s, kind, h, sd, f in people:
        b += f'<ellipse cx="{f1(x)}" cy="{f1(y + 2)}" rx="{f1(52 * s)}" ry="{f1(9 * s)}" fill="#5a5048" opacity="0.22" filter="url(#soft)"/>'
    return doc(b)


def haze_svg():
    """Atmospheric depth: a soft cream wash over the far street and the crowd (strongest at the top), so the boy and his
    dad, who stand in front of it, read clearly."""
    gid = "zq2haze"
    defs = S.lin_grad(gid, [(0, "#fbf3e2", 0.26), (0.55, "#fbf3e2", 0.14), (0.8, "#fbf3e2", 0.06), (1, "#fbf3e2", 0.0)])
    return doc(f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#{gid})"/>', defs)


def bunting_svg(ph):
    b = PR.bunting(-80, 26, W + 80, 58, n=21, sag=64, phase=ph, scale=1.55)
    return doc(b)


def shadow(x, y=FY, w=120, s=PS, a=0.22):
    return C.ground_shadow(x, y, s, w, a, color="#5a5048")


def boy(x, y, pose, expr=None, facing=-1, phase=0.0, shade=True):
    sh = shadow(x, y, 110) if shade else ""
    return sh + C.child(x, y, PS, facing, pose=pose, expr=expr, outfit="tracksuit", phase=phase)


def dad(x, pose, expr=None, phase=0.0, rider=None):
    kw = {} if rider is None else {"rider": rider}
    return shadow(x, FY, 150) + C.parent(x, FY, PS, -1, kind="dad", variant=1, pose=pose, expr=expr, phase=phase, **kw)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_you = beat(ctx, 0, "你有没有")
    t_bei = beat(ctx, 0, "被前面")
    t_big = beat(ctx, 0, "大人")
    t_block = beat(ctx, 0, "挡住")
    t_what = beat(ctx, 0, "什么")
    t_see = beat(ctx, 0, "看不见")
    t_l0 = L[0].end
    t_today = beat(ctx, 1, "今天")
    t_one = beat(ctx, 1, "有一个人")
    t_also = beat(ctx, 1, "也是这样")
    t_but = beat(ctx, 1, "可是")
    t_he = beat(ctx, 1, "他想了")
    t_good = beat(ctx, 1, "好办法")
    t_fa = beat(ctx, 1, "法")
    t_end = L[1].end

    # ---------------------------------------------------------------- expressions
    up_backs = EX("up_backs", "worried", look=(0.05, -0.10))
    up_curious = EX("up_curious", "neutral", look=(0.05, -0.12))
    reach = EX("reach", "frustrated", look=(0.04, -0.12), sweat=0)
    pout = EX("pout", "frustrated", look=(0.04, -0.02), sweat=0)
    pout_blink = EX("pout_blink", "frustrated", eyes="closed", sweat=0)
    us_pout = EX("us_pout", "worried", mouth="pout", look=(-0.06, 0.0), blush=True)
    us_pout_blink = EX("us_pout_blink", "worried", mouth="pout", eyes="closed", blush=True)
    dad_parade = EX("dad_parade", "kind", look=(0.05, -0.08))
    dad_parade_blink = EX("dad_parade_blink", "kind", eyes="closed")
    dad_down = EX("dad_down", "kind", look=(0.04, 0.10))
    dad_idea = EX("dad_idea", "happy", look=(0.04, 0.09))
    dad_up = EX("dad_up", "happy", look=(-0.02, -0.10))
    beam = "overjoyed"

    # ---------------------------------------------------------------- the boy (his own layer until the lift)
    cb = C.body_points(C.child, 0, 0, 1, 1, pose="walk_a", outfit="tracksuit")["feet"]
    cb2 = C.body_points(C.child, 0, 0, 1, 1, pose="walk_b", outfit="tracksuit")["feet"]
    a1 = -cb[1][0] * PS                         # stand -> walk_a: the back foot stays planted
    a2 = (cb[0][0] - cb2[0][0]) * PS            # walk_a -> walk_b
    a3 = XB0 - XB1 - a1 - a2                    # walk_b -> stand (the front foot plants)
    c_go = snap(t_friend - 0.05)
    g_cuts = [c_go, snap(c_go + 0.27), snap(c_go + 0.54)]
    g_steps = [a1, a2, a3]
    c_tip = snap(max(t_you - 0.05, g_cuts[-1] + 0.45))
    hop_ts = [snap(t_bei - 0.02), snap(t_bei + 0.6)]
    HOP_AIR, HOP_H = 0.38, 78 * PS
    c_land = [snap(h + HOP_AIR) for h in hop_ts]
    c_stand1 = snap(c_land[-1] + 0.22)
    c_tip2 = snap(t_what - 0.08)
    c_drop = snap(t_see + 0.22)
    c_fold = snap(t_l0 + 0.08)
    c_us = snap(t_one - 0.1)
    c_held = snap(t_but + 0.02)                  # dad crouches and takes him under the arms
    lift_t0 = snap(t_he - 0.05)
    n_lift = 8
    lift_dt = 0.15
    lift_cuts = [snap(lift_t0 + i * lift_dt) for i in range(n_lift)]
    c_up = snap(lift_t0 + n_lift * lift_dt)      # on dad's shoulders
    c_point = snap(max(c_up + 0.55, t_fa + 0.42))

    bfig = Fig(ctx, "boy", (XB1, FY), z=6.5, seed=71)
    bfig.at(0, boy(XB1, FY, "hold_hand", up_curious))
    bfig.at(snap(0.55), boy(XB1, FY, "hold_hand", up_backs))
    walk = [boy(XB1, FY, "walk_a", up_backs), boy(XB1, FY, "walk_b", up_backs)]
    bfig.at(g_cuts[0], walk[0]).at(g_cuts[1], walk[1]).at(g_cuts[2], boy(XB1, FY, "stand", up_backs))
    bfig.at(c_tip, boy(XB1, FY, "tiptoe", reach))
    crouch = boy(XB1, FY, "jump_see", phase=0.1)
    air = boy(XB1, FY, "jump_see", phase=0.5, shade=False)
    land = boy(XB1, FY, "jump_see", phase=0.9)
    for h, cl in zip(hop_ts, c_land):
        bfig.at(snap(h - 0.13), crouch).at(h, air).at(cl, land)
    bfig.at(c_stand1, boy(XB1, FY, "stand", pout))
    bfig.at(c_tip2, boy(XB1, FY, "tiptoe", reach))
    bfig.at(c_drop, boy(XB1, FY, "stand", pout))
    bfig.at(c_fold, boy(XB1, FY, "sulk", pout, facing=1))
    tbk = snap(c_fold + 0.75)
    bfig.at(tbk, boy(XB1, FY, "sulk", pout_blink, facing=1)).at(snap(tbk + 0.13), boy(XB1, FY, "sulk", pout, facing=1))
    bfig.at(c_us, boy(XB1, FY, "sulk", us_pout, facing=1))
    tbk2 = snap(c_us + 1.1)
    bfig.at(tbk2, boy(XB1, FY, "sulk", us_pout_blink, facing=1)).at(snap(tbk2 + 0.13), boy(XB1, FY, "sulk", us_pout, facing=1))

    # the walk offset (drawn at XB1; starts at XB0 holding dad's hand, a little behind him): planted-foot steps
    def b_walk(t):
        x = XB0
        for tc, st in zip(g_cuts, g_steps):
            x -= st * M.progress(t, tc - 0.08, tc + 0.1, "sine")
        lift_ = sum(-4 * PS * math.sin(math.pi * min(1.0, max(0.0, (t - tc + 0.08) / 0.18))) for tc in g_cuts)
        back = 10 * PS * (1 - M.progress(t, g_cuts[0] - 0.08, g_cuts[-1] + 0.1, "sine"))
        return Tf(dx=x - XB1, dy=lift_ - back)

    def b_hops(t):
        for h, cl in zip(hop_ts, c_land):
            if h <= t < cl:
                u = (t - h) / (cl - h)
                return Tf(dy=46 * PS - HOP_H * 4 * u * (1 - u))
        return Tf()

    wob = keyed([(c_tip + 0.1, 0.0), (c_tip + 0.3, 1.0), (hop_ts[0] - 0.25, 1.0), (hop_ts[0] - 0.14, 0.0),
                 (c_tip2 + 0.1, 0.0), (c_tip2 + 0.3, 1.0), (c_drop - 0.15, 1.0), (c_drop, 0.0)], "sine")
    huff = keyed([(c_fold + 0.2, 0.0), (c_fold + 0.4, 1.0), (c_us - 0.3, 1.0), (c_us, 0.0)], "sine")
    bfig.move(b_walk, b_hops,
              lambda t: Tf(rot=2.6 * math.sin(2 * math.pi * t / 0.9) * wob(t)),
              lambda t: Tf(sy=1 + 0.018 * math.sin(2 * math.pi * (t - c_fold) / 1.6) * huff(t)),
              dip(c_tip, 4), dip(c_stand1, 5), dip(c_tip2, 4), dip(c_drop, 6, 0.94), dip(c_fold, 5), dip(c_us, 4),
              hop(c_drop + 0.02, [(0, {"dy": 0}), (0.1, {"dy": -6}), (0.22, {"dy": 0})], ["out", "in"]),
              breath(ctx, 0.01, 2.6))
    b_alpha = lambda t: 1.0 if t < c_held else 0.0                                   # noqa: E731

    def hop_shadow(t):                     # his shadow stays on the ground (smaller and fainter) while he is in the air
        for h, cl in zip(hop_ts, c_land):
            if h <= t < cl:
                u = (t - h) / (cl - h)
                k = 1 - 0.45 * 4 * u * (1 - u)
                return Tf(alpha=k, sx=k, sy=k, px=XB1, py=FY)
        return Tf(alpha=0.0)
    sc.add("hop_shadow", doc(shadow(XB1, FY, 110)), z=6.4, wc=0, motion=hop_shadow)
    bfig.move(lambda t: Tf(alpha=b_alpha(t)))
    bfig.add(sc)

    # ---------------------------------------------------------------- dad
    pa = C.body_points(C.parent, 0, 0, 1, 1, pose="walk_a", kind="dad", variant=1)["feet"]
    d1 = -pa[1][0] * PS                          # stand -> walk_a (back foot planted)
    d2 = (XD0 - XDL) - d1                        # walk_a -> stand behind the boy (front foot plants; ~ the stride)
    c_notice = snap(t_l0 + 0.45)
    c_smile = snap(t_also + 0.05)
    c_step = [snap(t_also + 0.42), snap(t_also + 0.78)]

    dfig = Fig(ctx, "dad", (XDL, FY), z=6.0, seed=81)
    dfig.at(0, dad(XDL, "hold_hand", dad_parade))
    dfig.at(snap(g_cuts[0] - 0.05), dad(XDL, "stand", dad_parade))
    tdb = snap(2.9)
    dfig.at(tdb, dad(XDL, "stand", dad_parade_blink)).at(snap(tdb + 0.14), dad(XDL, "stand", dad_parade))
    dfig.at(c_notice, dad(XDL, "stand", dad_down))
    dfig.at(c_smile, dad(XDL, "stand", dad_idea))
    dfig.at(c_step[0], dad(XDL, "walk_a", dad_idea)).at(c_step[1], dad(XDL, "smile", dad_idea))
    lift_ph = [0.0, 0.12, 0.25, 0.37, 0.5, 0.62, 0.75, 0.87]
    dfig.at(c_held, dad(XDL, "lift", phase=0.0, rider=dict(expr="delighted")))
    for tc, ph in zip(lift_cuts, lift_ph):
        dfig.at(tc, dad(XDL, "lift", phase=ph, rider=dict(expr="overjoyed")))
    wave = [dad(XDL, "shoulders", "happy", phase=k / 4, rider=dict(expr=beam)) for k in range(4)]
    dfig.cycle(c_up, wave, step=4)
    dfig.at(c_point, dad(XDL, "shoulders", dad_up, rider=dict(pose="on_shoulders_point", expr="delighted")))
    tdb2 = snap(c_point + 0.75)
    if tdb2 + 0.3 < T:
        dfig.at(tdb2, dad(XDL, "shoulders", EX("dad_blink_up", "happy", eyes="closed"),
                          rider=dict(pose="on_shoulders_point", expr="delighted")))
        dfig.at(snap(tdb2 + 0.14), dad(XDL, "shoulders", dad_up, rider=dict(pose="on_shoulders_point", expr="delighted")))

    def d_walk(t):
        x = XD0
        x -= d1 * M.progress(t, c_step[0] - 0.09, c_step[0] + 0.1, "sine")
        x -= d2 * M.progress(t, c_step[1] - 0.09, c_step[1] + 0.12, "sine")
        lift_ = sum(-5 * PS * math.sin(math.pi * min(1.0, max(0.0, (t - tc + 0.09) / 0.2))) for tc in c_step)
        return Tf(dx=x - XDL, dy=lift_)
    rise = hop(c_up, [(0, {"dy": 0}), (0.12, {"dy": -8}), (0.3, {"dy": 0})], ["out", "sine"])
    sway_on = keyed([(c_up + 0.3, 0.0), (c_up + 0.8, 1.0)], "sine")
    dfig.move(d_walk, dip(c_notice, 2), dip(c_smile, 3), dip(c_step[1], 3), dip(c_held, 7, 0.94), dip(c_up, 6),
              dip(c_point, 3), rise,
              lambda t: Tf(rot=1.0 * math.sin(2 * math.pi * (t - c_up) / 2.2) * sway_on(t)),
              breath(ctx, 0.008, 3.2, 0.4))
    dfig.add(sc)

    # ---------------------------------------------------------------- the street, the float, the crowd
    sc.add("street", street_svg(), z=0, wc=0.7)
    sc.add("street_shade", street_shade_svg(), z=0.1, wc=0)
    fdx = float_dx
    sxc, syc = sun_centre()
    for j in range(len(BALLOONS)):
        svg, (ax, ay) = balloon_svg(j)
        sc.add(f"balloon{j}", svg, z=1.0 + 0.01 * j, seed=90 + j,
               motion=lambda t, j=j, ax=ax, ay=ay: Tf(dx=fdx(t), dy=6 * math.sin(2 * math.pi * (t / 2.4 + 0.21 * j)),
                                                      rot=4 * math.sin(2 * math.pi * (t / 3.1 + 0.17 * j)), px=ax, py=ay))
    sc.add("float", float_body_svg(), z=1.1, seed=97, motion=lambda t: Tf(dx=fdx(t), dy=1.5 * math.sin(2 * math.pi * t / 0.9)))
    sc.add("rays", rays_svg(), z=1.2, seed=98, motion=lambda t: Tf(dx=fdx(t), rot=9 * t, px=sxc, py=syc))
    blinks = [snap(x) for x in (2.2, 6.9, 11.3)]
    sun_frames = [sun_face_svg(False), sun_face_svg(True)]
    sc.add("sun", sun_frames, z=1.3, seed=99, frame_at=lambda t: 1.0 if any(b <= t < b + 0.15 for b in blinks) else 0.0,
           motion=lambda t: Tf(dx=fdx(t), dy=1.5 * math.sin(2 * math.pi * t / 0.9) + 4 * math.sin(2 * math.pi * t / 2.7),
                               rot=3 * math.sin(2 * math.pi * t / 3.3), px=sxc, py=syc + 60))

    people = crowd_people()
    sc.add("crowd_shadow", crowd_shadow_svg(people), z=1.9, wc=0)
    for r in (1, 0):
        row = sorted([p for p in people if p[0] == r], key=lambda p: p[1])
        ng = 4 if r else 5
        for g in range(ng):
            grp = row[g * len(row) // ng:(g + 1) * len(row) // ng]
            if not grp:
                continue
            ph0 = (g * 0.37 + r * 0.21) % 1
            frames = [crowd_group_svg(grp, (k / NCB + ph0) % 1) for k in range(NCB)]
            frames.append(frames[0])
            gx = sum(p[1] for p in grp) / len(grp)
            per = 2.2 + 0.37 * g + 0.5 * r
            sc.add(f"crowd{r}_{g}", frames, z=2 + (1 - r) * 0.5 + 0.01 * g, seed=100 + 10 * r + g, wc=0.8,
                   frame_at=stepped(NCB, per, ph0, 0.05),
                   motion=lambda t, g=g, r=r, gx=gx, per=per: Tf(dy=2.2 * math.sin(2 * math.pi * (t / (per * 0.7) + 0.3 * g)),
                                                                   dx=1.5 * math.sin(2 * math.pi * (t / (per * 1.3) + 0.2 * g + r))))
    sc.add("haze", haze_svg(), z=3.0, wc=0)
    bfr = [bunting_svg(k / 8) for k in range(8)]
    sc.add("bunting", bfr + [bfr[0]], z=8, seed=120, wc=0.6, frame_at=stepped(8, 2.0, 0.0, 0.05))

    # ---------------------------------------------------------------- sparkles, confetti
    sc.fx.append(Confetti(n=30, seed=4, speed=(55, 105), box=(0.0, 0.0, 1.0, 0.72)))
    sc.fx.append(FX.sparkles((XB1 - 160, FY - 640 * PS / 1.3 - 120, XB1 + 120, FY - 420), count=6, t0=c_up + 0.05,
                             t1=c_up + 1.8, size=(9, 16), period=1.2, drift=-14, seed=23))

    # ---------------------------------------------------------------- camera
    c0 = Cam(1056, 594, 2080)                     # wide (dissolve from the title page)
    c1 = Cam(1150, 694, 1500)                     # the boy at the wall (the float rolls in on the left)
    c2 = Cam(1172, 712, 1400)                     # a little closer while he pouts and looks at us
    c3 = Cam(1040, 640, 1420)                     # risen and opened out: the float he can see now
    c4 = Cam(1046, 636, 1390)
    sc.camera = safe_camera([(0, c0), (0.7, c0), (c_tip + 0.6, c1), (t_l0 + 0.2, c1), (t_one + 0.4, c2), (c_held - 0.2, c2),
                            (c_up + 0.6, c3), (T, c4)], "sine")

    # ---------------------------------------------------------------- sound
    sc.sfx("crowd", 0, dur=T, gain_db=-24, fade_in=0.9, fade_out=1.0, density=0.8)
    sc.sfx("cheer", 0, dur=T, gain_db=-31, fade_in=1.2, fade_out=1.0)
    sc.sfx("footsteps", g_cuts[0] - 0.05, dur=g_cuts[-1] - g_cuts[0] + 0.25, gain_db=-22, fade_in=0.05, fade_out=0.2,
           rate=1 / 0.27)
    for h, cl in zip(hop_ts, c_land):
        sc.sfx("thud", cl, gain_db=-22)
    sc.sfx("thud", c_drop, gain_db=-24)
    sc.sfx("footsteps", c_step[0] - 0.05, dur=0.6, gain_db=-22, fade_in=0.05, fade_out=0.2, rate=1 / 0.36, pan=0.2)
    sc.sfx("cloth", c_held, gain_db=-17)
    sc.sfx("whoosh", lift_t0 + 0.2, gain_db=-15)
    sc.sfx("sparkle", c_up + 0.05, gain_db=-15)
    sc.sfx("pop", c_point, gain_db=-20)
    return sc
