"""Scene 11 — the star leads the wise men to the house; gold, frankincense and myrrh (Matthew 2:9-11).

N '忽然，那颗星星又出现了，在前面给他们带路！' / N '星星一直走到伯利恒，停在了一座房子的上面。' /
N '博士们高兴极了！他们走进房子，看见了小耶稣和妈妈马利亚，就跪下来拜他。' /
N '他们打开宝盒，送上了三样礼物：黄金、乳香，还有没药。' / N '乳香和没药，都是又香又贵重的香料。这些，都是送给王的宝贝！'

Shares s10_star's stage (4000 x 1480) and its journey framing CAM_J; the night road is s10's own card D, drawn by
s10_star.add_journey(late=True) at journey time t + (s10 duration - 1.0), so the first second of this scene is exactly
the last second of s10 (plain 1 s cross-dissolve). Three places on the same framing, joined by page-turn dips through
the paper colour (the film's own transition for a change of place, so people of two shots never overlap):
  THE NIGHT ROAD   '忽然' the caravan walks on;  '星星' the star appears ahead (upper right) with a sparkle and a chime;
                   '又出现了' the riders look up, amazed;  '在前面' Melchior points ahead, Caspar and Balthasar cheer;
                   '带路' the star glides on ahead, they ride on happily.                       (dip on the line break)
  BETHLEHEM        night: the little town on its hill, the limestone family_house, the caravan arriving on the road;
                   '星星一直走到伯利恒' the star glides across the sky to the town;  '停在了' it stops over the house;
                   '一座房子的上面' a beam of light down to the roof, which glows;  the camels stop at the house.
                   '博士们高兴极了' the riders cheer (hops), sparkles round the star.            (dip before '他们走进房子')
  THE HOUSE        a warm room: Mary on the bench with little Jesus (a toddler) on her lap, Joseph beside them, starlight
                   through the window, a lamp;  '他们走进房子' the three walk in from the right carrying their treasures
                   (planted-foot walks);  '小耶稣' the toddler waves;  '妈妈马利亚' Mary smiles;  '跪' they kneel and bow
                   low, treasures on the floor;  '打开宝盒' they kneel up holding them out;  '黄金' the casket opens and
                   shines (coins), the toddler reaches;  '乳香' the alabaster jar opens;  '没药' the flask opens, the
                   toddler waves;  '乳香和没药…香料' curls of sweet smoke and sparkles rise from the two jars, Mary breathes
                   it in;  '这些' all three treasures glow together;  '王' a soft warm light round the child, who laughs;
                   calm hold for the page turn.
Pose changes are hard cuts sold by a squash-and-hop (Actor); walks are planted-foot cycles; Jesus is a toddler, no halo.
"""
import math
import random

from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_N, walk_pose
from art.style import P
from engine import motion as M
from engine.loader import context
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s08_saul import Actor, WalkPath, sparkle_dyn
from stories.nativity.scenes import s10_star as A
from stories.nativity.scenes.s10_star import (CAM_J, JX0, JY0, SH, SW, alpha_m, blink, clamp, ct, doc, f1, fig_sprite,
                                              jdoc, magus, paper_dip)
from stories.noah.scenes.s01_title import snap

INK = P["ink"]
# Bethlehem (view-local u, v of CAM_J)
HOUSE = (1520, 1000, 0.8)                  # family_house exterior: anchor, scale
ROOF_Y = HOUSE[1] - 602 * HOUSE[2]
STAR_STOP = (HOUSE[0] - 10, ROOF_Y - 300)
CSB = 0.58                                 # the caravan arriving in Bethlehem
ROAD_V = 1046
CB_US = (0, -310, -620)
# the room (view-local): family_house interior anchor, people on its floor line
ROOM = (1036, 980)
KI = 1.1
MARY_U = ROOM[0] - 150
JOSEPH_U = ROOM[0] - 430
KNEEL_U = (1240, 1575, 1910)               # Melchior (gold), Caspar (frankincense), Balthasar (myrrh); facing left
WALK_RATE = 22.0                           # walk drawings per second (~275 px/s)
WALK_STRIDE = 34                           # a short, stately stride under the long robes (figure px per half step)


def st(u, v):
    """View-local -> stage."""
    return JX0 + u, JY0 + v


# ================================================================== figures
def mary_hold(x, y, s, facing=1, tpose="sit", texpr="happy", tphase=0.0, mexpr="kind"):
    """Mary seated on the bench (characters.mary 'sit_hold') with toddler_jesus on her lap in any TODDLER sit pose."""
    ps = C._mary_pose("sit_hold", 0.0)
    D = C._mary_design(mexpr)

    def mid(stt):
        H, K = stt["legs"][1][0], stt["legs"][1][1]
        lap = C._add(C._lerp(H, K, 0.58), (0, -0.5 * stt["m"]["lw"] - 9))
        inner, bb, last = C._toddler_inner(tpose, texpr, tphase, True)
        return f'<g transform="translate({C.fmt(lap[0])},{C.fmt(lap[1])})">{inner}</g>'
    D["behind"], D["mid"], D["front"] = C._hooks(), C._hooks(mid), C._hooks()
    inner, _ = C._figure(D, C._MARY_M, ps, mexpr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"mary-hold-{tpose}")


def toddler_point(x, y, s):
    """Stage point of the toddler's chest on Mary's lap (for his soft glow)."""
    return x + 52 * s, y - 150 * s


# ================================================================== Bethlehem drawings (view-local)
def ext_sky_svg():
    return jdoc(PR.starry_sky(-80, -80, 2200, 940, density=1.0, time="night", seed=55, milky_way=True))


def ext_town_svg():
    out = PR.bethlehem_town(-160, 2260, 880, 0.62, time="night", part="back", seed=3)
    # fields and the road up to the house
    grass = PR._nt("#7a9a58", "night")
    out += PR._p(PR._sm([(-120, 905), (500, 880), (1100, 900), (1700, 880), (2250, 896)], closed=False) +
                 " L2250,1300 L-120,1300 Z", grass, 3.4)
    road = PR._nt("#e0c69a", "night")
    out += PR._p(f"M-120,{ROAD_V - 40} Q700,{ROAD_V - 52} 1300,{ROAD_V - 44} Q1460,{ROAD_V - 44} 1520,{ROAD_V - 50} "
                 f"Q1600,{ROAD_V - 52} 1640,{ROAD_V - 30} Q1700,{ROAD_V + 10} 1600,{ROAD_V + 50} Q1400,{ROAD_V + 64} 1100,{ROAD_V + 66} "
                 f"Q500,{ROAD_V + 70} -120,{ROAD_V + 76} Z", road, 3.4)
    rng = random.Random(9)
    for i in range(16):
        u = rng.uniform(-80, 1500)
        out += PR._ell(u, ROAD_V + rng.uniform(-20, 50), 9, 4, PR._nt("#bfa278", "night"), 0)
    for i in range(40):
        u, v = rng.uniform(-100, 2220), rng.uniform(ROAD_V + 90, 1190)
        k = 0.8 + (v - ROAD_V) / 300
        out += PR._p(f"M{f1(u - 8 * k)},{f1(v)} l{f1(5 * k)},{f1(-16 * k)} l{f1(5 * k)},{f1(13 * k)} l{f1(5 * k)},"
                     f"{f1(-18 * k)} l{f1(5 * k)},{f1(15 * k)}", sw=2.2, stroke=PR._nt("#4f7a36", "night"))
    return jdoc(f'<g filter="url(#wobble)">{out}</g>')


def ext_house_svg(k):
    x, y, s = HOUSE
    return jdoc(PR.family_house(x, y, s, 1, view="exterior", time="night", star_light=k, lamp=1.0))


def ext_front_svg():
    """Foreground framing at the bottom corners: a rock, bushes, a palm on the right."""
    out = ""
    out += PR._ell(60, 1170, 150, 60, PR._nt("#b4aa98", "night"), 3.6)
    out += S.cloud(-20, 1150, 210, 100, fill=PR._nt("#5f7a42", "night"), seed=4, puffs=5, sw=3.2,
                   shade_fill=PR._nt("#4a6234", "night"))
    out += S.cloud(1990, 1130, 260, 120, fill=PR._nt("#5f7a42", "night"), seed=8, puffs=5, sw=3.2,
                   shade_fill=PR._nt("#4a6234", "night"))
    out += PR._place(PR._palm(-0.06, 0, True, True), 2060, 1120, 0.75)
    return jdoc(f'<g filter="url(#wobble)">{out}</g>')


def star_svg_at(u, v, k=1.0, pulse=0.0, beam=0.0, beam_to=None, scale=0.5):
    x, y = st(u, v)
    bt = st(*beam_to) if beam_to else None
    return doc(PR.the_star(x, y, scale, intensity=k, pulse=pulse, beam=beam, beam_to=bt))


# ================================================================== the room drawings (view-local)
def room_svg(k):
    return jdoc(PR.family_house(ROOM[0], ROOM[1], KI, 1, view="interior", time="night", star_light=k, lamp=1.0))


def room_lamp_svg(k):
    return jdoc(PR._warm_glow(ROOM[0] + 450 * KI, ROOM[1] - 380 * KI, 380, 300, 0.45 * k, "n11lamp"))


def glow_svg(u, v, r, key, col0=PR.STAR_CORE, col1=PR.STAR_GOLD, k=0.9):
    return jdoc(PR._warm_glow(u, v, r, r * 0.9, k, key, col0, col1))


def floor_gifts_svg():
    out = ""
    for i in range(3):
        out += PR.gift(KNEEL_U[i] - 168, ROOM[1] + 10, 0.66 * KI, -1, kind=PR.GIFT_KINDS[i])
    return jdoc(out)


# ================================================================== fragrance curls (dynamic)
def fragrance_dyn(srcs, t0, t1, k_fn, seed=5):
    """Curls of sweet smoke rising and drifting left from the stage points srcs (frankincense and myrrh)."""
    rng = random.Random(seed)
    curls = [(i, (j + rng.uniform(-0.1, 0.1)) / 4, rng.uniform(0.8, 1.2), rng.uniform(-1, 1)) for i in range(len(srcs))
             for j in range(4)]
    xs = [p[0] for p in srcs]
    ys = [p[1] for p in srcs]
    x0, y0 = min(xs) - 380, min(ys) - 420
    w, h = int(max(xs) - x0 + 120), int(max(ys) - y0 + 40)

    def fn(t):
        if t < t0 or t > t1:
            return None
        k = k_fn(t)
        if k <= 0.01:
            return None
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for (i, ph, sp, sd) in curls:
            sx, sy = srcs[i][0] - x0, srcs[i][1] - y0
            life = ((t - t0) * 0.42 * sp + ph) % 1.0
            pts = []
            n = 22
            for j in range(n):
                u = j / (n - 1) * life
                yy = sy - u * 360 + 30 * u * u
                xx = sx - u * u * 330 + 34 * math.sin(7.0 * u + t * 2.0 * sp + sd * 3) * (0.25 + u)
                pts.append((xx, yy))
            env = math.sin(math.pi * life)
            for j in range(len(pts) - 1):
                u = j / (n - 1)
                a = int(235 * k * env * (1 - u ** 1.6))
                if a > 3:
                    wdt = max(4, int(14 * (1 - u * 0.55)))
                    d.line([pts[j], pts[j + 1]], fill=(150, 112, 120, min(255, int(a * 0.5))), width=wdt + 5)
            for j in range(len(pts) - 1):
                u = j / (n - 1)
                a = int(235 * k * env * (1 - u ** 1.6))
                if a > 3:
                    wdt = max(4, int(14 * (1 - u * 0.55)))
                    d.line([pts[j], pts[j + 1]], fill=(255, 250, 238, min(255, a)), width=wdt)
        return im, (x0, y0)
    return fn


# ================================================================== build
def build(ctx):
    T = ctx.duration
    sc = Scene(ctx, W=SW, H=SH)
    ctx10 = context("s10_star")
    toff = ctx10.duration - A.XF

    # ---------------------------------------------------------------- beats
    t_star = ct(ctx, 0, "星星")
    t_again = ct(ctx, 0, "又出现")
    t_ahead = ct(ctx, 0, "在前面")
    t_lead = ct(ctx, 0, "带路")
    t_dip1 = (ctx.lines[0].end + ctx.lines[1].start) / 2 - 0.05
    t_go = ct(ctx, 1, "一直走到")
    t_beth = ct(ctx, 1, "伯利恒")
    t_stop = ct(ctx, 1, "停在")
    t_house = ct(ctx, 1, "房子")
    t_above = ct(ctx, 1, "上面")
    t_boshi = ct(ctx, 2, "博士")
    t_joy = ct(ctx, 2, "高兴")
    t_dip2 = (ct(ctx, 2, "极了", 1) + ct(ctx, 2, "他们走进")) / 2 + 0.05
    t_in = ct(ctx, 2, "他们走进")
    t_see = ct(ctx, 2, "看见")
    t_jesus = ct(ctx, 2, "小耶稣")
    t_mama = ct(ctx, 2, "妈妈")
    t_kneel = ct(ctx, 2, "跪")
    t_bai = ct(ctx, 2, "拜他")
    t_open = ct(ctx, 3, "打开")
    t_give = ct(ctx, 3, "送上")
    t_gold = ct(ctx, 3, "黄金")
    t_frank = ct(ctx, 3, "乳香")
    t_myrrh = ct(ctx, 3, "没药")
    t_frag = ct(ctx, 4, "乳香和")
    t_smell = ct(ctx, 4, "又香")
    t_these = ct(ctx, 4, "这些")
    t_king = ct(ctx, 4, "王")
    t_treas = ct(ctx, 4, "宝贝")

    road_vis = lambda t: 1.0 if t < t_dip1 else 0.0            # noqa: E731
    town_vis = lambda t: 1.0 if t_dip1 <= t < t_dip2 else 0.0  # noqa: E731
    room_vis = lambda t: 1.0 if t >= t_dip2 else 0.0           # noqa: E731

    # ---------------------------------------------------------------- camera
    cam_town = M.cam_keys([(t_dip1, CAM_J), (t_above + 0.4, Cam(CAM_J.x + 40, CAM_J.y + 10, 2040))], "sine")
    roomc = Cam(JX0 + 1120, JY0 + 622, 1990)
    cam_room = M.cam_keys([(t_dip2, CAM_J), (t_open - 0.2, CAM_J), (t_myrrh + 0.6, roomc)], "sine")

    def camera(t):
        if t < t_dip1:
            return CAM_J
        if t < t_dip2:
            return cam_town(t)
        return cam_room(t)
    sc.camera = camera

    # ================================================================ 1. the night road (s10's card D goes on)
    def road_sched(i):
        st0 = 0.1 * i
        out = [(-10, "ride", 0), (snap(t_again + st0), "ride_look", 0.8)]
        if i == 0:
            out += [(snap(t_ahead), "ride_point", 1.0)]
        else:
            out += [(snap(t_ahead + 0.12 * i), "ride_cheer", 1.1)]
        out += [(snap(t_lead + 0.25 + st0), "ride_happy", 0.6)]
        return out
    A.add_journey(sc, ctx10, toff, rider_sched=road_sched, z0=50.0, late=True, alpha=road_vis)
    # the star appears again, ahead (upper right), and glides on ahead
    su0, sv0 = 1600, 260
    pulse_fr = [star_svg_at(su0, sv0, 1.0, (k % 4) / 4) for k in range(5)]

    def road_star_m(t):
        if t < t_star or t >= t_dip1:
            return Tf(alpha=0.0)
        g = M.progress(t, t_ahead + 0.3, t_dip1 + 0.6, "sine")
        dx, dy = 330 * g, -40 * g
        pop = M.ease("back")(clamp((t - t_star) / 0.45))
        px, py = st(su0, sv0)
        return Tf(dx=dx, dy=dy, sx=max(0.01, pop), sy=max(0.01, pop), px=px, py=py, alpha=clamp((t - t_star) / 0.25))
    sc.add("road_star", pulse_fr, z=50.6, frame_at=lambda t: (t * 1.6) % 4,
           motion=road_star_m)
    sc.add_dynamic("road_sparks", sparkle_dyn((JX0 + su0 - 260, JY0 + sv0 - 200, JX0 + su0 + 420, JY0 + sv0 + 200),
                                              count=14, t0=t_star, t1=t_dip1, size=(8, 16), period=1.2, drift=-6,
                                              seed=31), z=50.7)

    # ================================================================ 2. Bethlehem
    zt = 100.0
    sc.add("ext_sky", ext_sky_svg(), z=zt, motion=alpha_m(town_vis))
    sc.add_dynamic("ext_twinkle", sparkle_dyn((JX0 - 40, JY0, JX0 + 2150, JY0 + 560), count=20, t0=t_dip1, t1=t_dip2,
                                              size=(6, 12), period=2.0, drift=0, seed=41), z=zt + 0.05)
    # the star glides across to the town and stops over the house; then its beam reaches the roof
    beam_ks = (0.0, 0.35, 0.7, 1.0)
    sfr = [star_svg_at(STAR_STOP[0], STAR_STOP[1], 1.0, 0.0, b, (HOUSE[0], ROOF_Y + 10)) for b in beam_ks]
    sfr += [star_svg_at(STAR_STOP[0], STAR_STOP[1], 1.0, 0.5, 1.0, (HOUSE[0], ROOF_Y + 10))]
    s_from = (180, 150)
    t_arrive = t_stop + 0.15

    def town_star_m(t):
        if not town_vis(t):
            return Tf(alpha=0.0)
        g = M.progress(t, t_dip1 + 0.15, t_arrive, "sine")
        dx = (s_from[0] - STAR_STOP[0]) * (1 - g)
        arc = -60 * math.sin(math.pi * g)
        dy = (s_from[1] - STAR_STOP[1]) * (1 - g) + arc
        bob = 4 * math.sin(2 * math.pi * t / 2.6) if t > t_arrive else 0.0
        return Tf(dx=dx, dy=dy + bob)

    def town_star_fa(t):
        b = M.progress(t, t_house - 0.1, t_above + 0.3, "sine") * 3.0
        if b >= 3.0 and t > t_above + 0.8:
            return 3.0 + (0.5 + 0.5 * math.sin(2 * math.pi * (t - t_above) / 2.4))
        return b
    sc.add("town_star", sfr, z=zt + 0.1, frame_at=town_star_fa, motion=town_star_m)
    sc.add("ext_town", ext_town_svg(), z=zt + 0.2, motion=alpha_m(town_vis))
    sc.add("ext_house", [ext_house_svg(0.0), ext_house_svg(0.5), ext_house_svg(1.0)], z=zt + 0.3,
           frame_at=lambda t: 2.0 * M.progress(t, t_house, t_above + 0.4, "sine"), motion=alpha_m(town_vis))
    # the caravan arrives on the road and stops at the house
    phb0 = 0.0
    t_halt = t_above + 0.2
    rateb = 1 / 0.9
    strideb = 113 * CSB
    u_stop = 1010
    u_start = u_stop - strideb * rateb * (t_halt - t_dip1 + 0.35)

    def phase_b(t):
        return (min(t, t_halt) - t_dip1) * rateb + phb0

    def dx_b(t):
        return (phase_b(t) - phb0) * strideb

    def town_sched(i):
        out = [(-10, "ride", 0), (snap(t_beth + 0.3 + 0.1 * i), "ride_look", 0.7), (snap(t_halt + 0.1 * i), "ride", 0.6),
               (snap(t_boshi + 0.1 * i), "ride_happy", 0.5), (snap(t_joy + 0.12 * i), "ride_cheer", 1.3)]
        return out
    A.add_camels(sc, "town", CSB, (JX0 + u_start, JY0 + ROAD_V), CB_US, phase_b, dx=dx_b,
                 stand=lambda t: t >= t_halt, rider_sched=town_sched, tint=lambda t: 0.3, alpha=town_vis, z=zt + 1.0)
    sc.add("ext_front", ext_front_svg(), z=zt + 2.0, motion=alpha_m(town_vis))
    sc.add_dynamic("town_sparks", sparkle_dyn((JX0 + STAR_STOP[0] - 300, JY0 + STAR_STOP[1] - 220,
                                               JX0 + STAR_STOP[0] + 300, JY0 + STAR_STOP[1] + 260),
                                              count=18, t0=t_stop, t1=t_dip2, size=(8, 17), period=1.3, drift=-8,
                                              seed=43), z=zt + 2.1)
    sc.add_dynamic("joy_sparks", sparkle_dyn((JX0 + 300, JY0 + 520, JX0 + 1300, JY0 + 820), count=16, t0=t_joy,
                                             t1=t_dip2, size=(8, 15), period=1.1, drift=-14, seed=47), z=zt + 2.2)

    # ================================================================ 3. the house
    zr = 200.0
    sc.add("room", [room_svg(0.55), room_svg(1.0)], z=zr, frame_at=lambda t: M.progress(t, t_see, t_jesus + 0.6, "sine"),
           motion=alpha_m(room_vis))
    sc.add("room_lamp", [room_lamp_svg(0.8), room_lamp_svg(1.0), room_lamp_svg(0.9)], z=zr + 0.1, wc=0,
           frame_at=lambda t: 1.0 + 0.9 * math.sin(t * 6.1) * math.sin(t * 2.3),
           motion=alpha_m(room_vis))
    # Joseph, watching tenderly
    jsp = fig_sprite(KI, 601, wide=200)
    jd = {n: jsp.add(C.joseph_carpenter(jsp.ax, jsp.ay, KI, 1, pose="watch", expr=e)) for n, e in (
        ("kind", "kind"), ("kind_b", blink("kind")), ("tender", "tender"), ("happy", "happy"), ("happy_b", blink("happy")),
        ("joy", "joyful"))}
    js_ = [(0, "kind", 0), (t_dip2 + 1.3, "kind_b", 0), (t_dip2 + 1.43, "kind", 0), (t_jesus, "tender", 0.5),
           (t_gold, "happy", 0.5), (t_gold + 3.1, "happy_b", 0), (t_gold + 3.23, "happy", 0), (t_these, "joy", 0.5)]
    sc.add("joseph_sh", doc(C.ground_shadow(*st(JOSEPH_U, ROOM[1]), KI, 140, 0.2)), z=zr + 0.5, wc=0,
           motion=alpha_m(room_vis))
    sc.add_dynamic("joseph", Actor(jsp, [(snap(ts), jd[n], a) for ts, n, a in js_], lambda t: st(JOSEPH_U, ROOM[1]),
                                   alpha=room_vis, breathe=0.010, bper=3.1, phase=0.2), z=zr + 0.6)
    # the toddler's soft light (behind Mary), Mary with little Jesus
    tpx, tpy = toddler_point(*st(MARY_U, ROOM[1]), KI)
    sc.add("child_glow", glow_svg(tpx - JX0, tpy - JY0 - 20, 330, "n11child", k=0.9), z=zr + 0.7, wc=0,
           motion=lambda t: Tf(alpha=room_vis(t) * (0.35 * M.progress(t, t_jesus, t_jesus + 0.8, "sine") +
                                                    0.65 * M.progress(t, t_king - 0.2, t_king + 0.6, "sine")) *
                               (0.9 + 0.1 * math.sin(t * 2.4))))
    msp = fig_sprite(KI, 602, wide=220, tall=420)
    md = {}
    for n, tp, te, tph, me in (("sit", "sit", "happy", 0, "kind"), ("sit_b", "sit", "happy", 0, blink("kind")),
                               ("wave0", "sit_wave", "laugh", 0.0, "tender"), ("wave1", "sit_wave", "laugh", 0.33, "tender"),
                               ("wave2", "sit_wave", "laugh", 0.66, "tender"), ("tender", "sit", "happy", 0, "tender"),
                               ("reach", "sit_reach", "amazed", 0, "tender"), ("smell", "sit", "happy", 0, "peaceful"),
                               ("laugh", "sit", "laugh", 0, "joyful"), ("joy", "sit", "happy", 0, "joyful"),
                               ("joy_b", "sit", "happy", 0, blink("tender"))):
        md[n] = msp.add(mary_hold(msp.ax, msp.ay, KI, 1, tp, te, tph, me))
    ms_ = [(0, "sit", 0), (t_dip2 + 0.9, "sit_b", 0), (t_dip2 + 1.03, "sit", 0)]
    w0 = snap(t_jesus)
    w1 = snap(t_mama + 0.9)
    k = 0
    tw = w0
    while tw < w1:
        ms_.append((tw, ("wave0", "wave1", "wave2", "wave1")[k % 4], 0.6 if k == 0 else 0))
        tw = snap(tw + 0.16)
        k += 1
    ms_ += [(w1, "tender", 0.5), (t_kneel + 1.6, "joy_b", 0), (t_kneel + 1.73, "tender", 0),
            (snap(t_gold + 0.12), "reach", 0.7)]
    w0 = snap(t_myrrh + 0.1)
    w1 = snap(t_frag + 0.2)
    k = 0
    tw = w0
    while tw < w1:
        ms_.append((tw, ("wave0", "wave1", "wave2", "wave1")[k % 4], 0.6 if k == 0 else 0))
        tw = snap(tw + 0.16)
        k += 1
    ms_ += [(w1, "tender", 0.4), (snap(t_smell + 0.2), "smell", 0.4), (snap(t_these), "joy", 0.5),
            (snap(t_king), "laugh", 0.7), (snap(t_treas + 1.0), "joy", 0)]
    sc.add_dynamic("mary", Actor(msp, [(ts, md[n], a) for ts, n, a in ms_], lambda t: st(MARY_U, ROOM[1]), alpha=room_vis,
                                 breathe=0.008, bper=3.3, phase=0.6), z=zr + 0.8)
    # the wise men walk in from the right carrying their treasures, kneel, bow, offer, open
    adv = 2 * WALK_STRIDE / WALK_N * KI
    nwalk = 42
    for i in range(3):
        sp = fig_sprite(KI, 610 + i)
        walk = []
        for kk in range(2 * WALK_N):
            ps = walk_pose(kk, A=WALK_STRIDE)
            ps["arms"] = A.MAGI_POSES["carry_gift"]["arms"]
            ps["hands"] = ("open", "open")
            ps["expr"] = "happy"
            ps["drop"] = 0.35 * (12 + 4 * math.cos(2 * math.pi * (kk % WALK_N) / WALK_N))
            walk.append(sp.add(magus(sp.ax, sp.ay, KI, -1, i, "carry_gift", ps=ps, label=f"w{kk}")))
        d = {"carry": sp.add(magus(sp.ax, sp.ay, KI, -1, i, "carry_gift", expr="happy")),
             "carry_b": sp.add(magus(sp.ax, sp.ay, KI, -1, i, "carry_gift", expr=blink("kind"))),
             "bow": sp.add(magus(sp.ax, sp.ay, KI, -1, i, "bow")),
             "offer": sp.add(magus(sp.ax, sp.ay, KI, -1, i, "kneel_offer", expr="joyful"))}
        opens = [(0.2, 0.0), (0.4, 0.5), (0.6, 0.5), (0.8, 1.0), (1.0, 1.0)]
        for j, (o, g) in enumerate(opens):
            d[f"open{j}"] = sp.add(magus(sp.ax, sp.ay, KI, -1, i, "kneel_offer", expr="joyful", gift_open=o, gift_glow=g))
        x_end = KNEEL_U[i]
        x_start = x_end + nwalk * adv
        tw0 = snap(t_in - 0.02 + 0.06 * i)
        wp = WalkPath([(tw0, x_start, x_end, WALK_RATE)], walk, adv)
        t_arr = snap(wp.end(0))
        t_name = (t_gold, t_frank, t_myrrh)[i]
        sched = [(0, walk[0], 0), (t_arr, d["carry"], 0.5), (t_arr + 1.2 + 0.3 * i, d["carry_b"], 0),
                 (t_arr + 1.33 + 0.3 * i, d["carry"], 0), (snap(t_kneel + 0.08 * i), d["bow"], 1.0),
                 (snap(t_open + 0.08 * i), d["offer"], 1.0), (snap(t_give + 0.1 * i), d["offer"], 0.5)]
        for j in range(len(opens)):
            sched.append((snap(t_name + 0.07 * j), d[f"open{j}"], 0.7 if j == 0 else 0))

        def pos(t, wp=wp):
            return st(wp.x(t), ROOM[1])
        act = Actor(sp, sched, pos, walk=wp.frame, alpha=room_vis, breathe=0.009, bper=2.8, phase=0.37 * i,
                    rot=(lambda t, tn=t_name: -4 * math.sin(math.pi * clamp((t - tn) / 0.9)) if tn <= t <= tn + 0.9
                         else 0.0))
        sc.add(f"mag_sh{i}", doc(C.ground_shadow(*st(x_end, ROOM[1]), KI, 160, 0.2)), z=zr + 0.9, wc=0,
               motion=lambda t, wp=wp, xe=x_end: Tf(dx=wp.x(t) - xe, alpha=room_vis(t)))
        sc.add_dynamic(f"magus{i}", act, z=zr + 1.0 + 0.1 * (2 - i))
    # the treasures set on the floor while they bow
    sc.add("floor_gifts", floor_gifts_svg(), z=zr + 1.5,
           motion=lambda t: Tf(alpha=1.0 if snap(t_kneel) <= t < snap(t_open) else 0.0))
    # each treasure shines as it is named; at '这些' all three glow together
    gift_pts = []
    for i in range(3):
        gx, gy = st(KNEEL_U[i] - 76 * KI, ROOM[1] - 175 * KI)
        gift_pts.append((gx, gy))
        t_name = (t_gold, t_frank, t_myrrh)[i]
        sc.add(f"gift_glow{i}", glow_svg(gx - JX0, gy - JY0, 150, f"n11g{i}", k=0.85), z=zr + 1.6, wc=0, blend="screen",
               motion=(lambda t, tn=t_name: Tf(alpha=room_vis(t) * clamp(
                   0.9 * (M.progress(t, tn, tn + 0.3, "out") - 0.55 * M.progress(t, tn + 0.5, tn + 1.4, "sine"))
                   + 0.75 * M.progress(t, t_these, t_these + 0.6, "sine") * (0.8 + 0.2 * math.sin(3 * (t - t_these)))))))
        sc.add_dynamic(f"gift_sparks{i}", sparkle_dyn((gx - 120, gy - 150, gx + 120, gy + 40), count=9, t0=t_name,
                                                      t1=t_name + 1.6, size=(8, 15), period=1.0, drift=-20, seed=50 + i),
                       z=zr + 1.7)
    sc.add_dynamic("treasure_sparks", sparkle_dyn((gift_pts[0][0] - 160, gift_pts[0][1] - 220, gift_pts[2][0] + 140,
                                                   gift_pts[2][1] + 30), count=20, t0=t_these, t1=T + 1, size=(8, 16),
                                                  period=1.4, drift=-10, seed=57), z=zr + 1.75)
    sc.add_dynamic("fragrance", fragrance_dyn([(gift_pts[1][0], gift_pts[1][1] - 30), (gift_pts[2][0], gift_pts[2][1] - 40)],
                                              t_frank + 0.3, T + 1,
                                              lambda t: room_vis(t) * (0.35 * M.progress(t, t_frank + 0.3, t_frank + 1.0) +
                                                                       0.65 * M.progress(t, t_frag, t_frag + 0.8))),
                   z=zr + 1.8)
    sc.add_dynamic("frag_sparks", sparkle_dyn((gift_pts[1][0] - 260, gift_pts[1][1] - 420, gift_pts[2][0] + 60,
                                               gift_pts[2][1] - 60), count=14, t0=t_frag, t1=T + 1, size=(6, 12),
                                              period=1.6, drift=-22, seed=59), z=zr + 1.85)

    # page-turn dips between the places
    sc.fx.append(paper_dip(t_dip1))
    sc.fx.append(paper_dip(t_dip2))

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0.0, dur=t_dip2 + 0.4, gain_db=-21, fade_in=0.8, fade_out=0.6)
    sc.sfx("footsteps", 0.0, dur=t_dip1 + 0.3, gain_db=-25, fade_in=0.8, fade_out=0.4, rate=2.2)
    sc.sfx("sparkle", t_star - 0.05, gain_db=-17, pan=0.4)
    sc.sfx("chime", t_star + 0.05, gain_db=-13, pan=0.4)
    sc.sfx("cloth", t_ahead + 0.05, gain_db=-19, pan=0.1)
    sc.sfx("whoosh", t_dip1 - 0.1, gain_db=-21)
    sc.sfx("footsteps", t_dip1, dur=t_halt - t_dip1, gain_db=-24, fade_in=0.4, fade_out=0.3, rate=2.2, pan=-0.2)
    sc.sfx("sparkle", t_stop, gain_db=-17, pan=0.1)
    sc.sfx("grow", t_house - 0.1, gain_db=-19)
    sc.sfx("chime", t_joy, gain_db=-14)
    sc.sfx("whoosh", t_dip2 - 0.1, gain_db=-21)
    sc.sfx("footsteps", t_in, dur=nwalk / WALK_RATE + 0.15, gain_db=-19, fade_in=0.2, fade_out=0.3, rate=2.6, pan=0.3)
    sc.sfx("fire", t_dip2, dur=T - t_dip2 + 0.3, gain_db=-27, fade_in=0.8, fade_out=1.2)
    sc.sfx("cloth", t_kneel, gain_db=-16)
    sc.sfx("cloth", t_open, gain_db=-18)
    sc.sfx("coins", t_gold + 0.12, gain_db=-14, pan=0.1)
    sc.sfx("sparkle", t_gold, gain_db=-18, pan=0.1)
    sc.sfx("sparkle", t_frank, gain_db=-18, pan=0.3)
    sc.sfx("sparkle", t_myrrh, gain_db=-18, pan=0.5)
    sc.sfx("grow", t_frag, gain_db=-22, pan=0.4)
    sc.sfx("chime", t_these + 0.1, gain_db=-14)
    return sc
