"""Scene 5 - Luke 2:6-7. Bethlehem at dusk. It opens on exactly the last frame of s04 (plain 1 s cross-dissolve: the lit
little town on its hill, Joseph and Mary on the donkey on the road below); they walk on toward the gate. Inside, the
street is packed like a railway station at New Year: people squeezed together with bundles held overhead, a man with a
wobbling stack of pots on his head, a hen in a basket that flaps up out of the crowd; Joseph leads the donkey through
with Mary riding, inch by inch. At the inn Joseph knocks; the innkeeper opens the door and kindly shakes his head - faces
fill every window and travellers sleep on the roof: no room. So they go into a humble cave-stable with an ox and the
donkey; Mary sits down on a bale of hay, a hand on her belly, Joseph holds up his little lamp and the stable lamp
glows warm.

Beats (syllable onsets measured in the voice clip through the Storm film's Beats class; nothing hard-coded to the take):
  0 .. 1.0     identical to the end of s04 (the clock of s04's arrival page continues: lamps, stars, the tiny travellers
               walking into the gate, breathing all match across the dissolve)
  '到了伯利恒'  Joseph leads on toward the gate (planted strides), the camera eases toward the gate
  '城里到处'    cut to the crowded street (crowd hubbub); the donkey and Joseph squeeze along (slow planted strides),
               the crowd jostles, a hen bobs in its basket, a pot stack wobbles
  '火车站一样挤' the crowd presses together on '挤' and a hen flaps up over the heads (pop)
  '客店里'      cut to the inn: Joseph knocks on '客' (knock marks, wooden knocks), the door opens on '里'
  '已经没有地方了' the innkeeper shakes his head on '已' (palms out), the faces in the windows look down, on '地方' Joseph
               puts a worried hand to his chin and Mary looks worried
  '放牲口的地方' cut to the stable at dusk: the ox looks up; Joseph and Mary walk in (planted strides)
  '住了下来'    on '住' Mary sits down on the hay bale (hand on her belly), Joseph turns and holds up his lamp, the
               stable lamp glows warm on '下' (soft crackle), motes float in the lamplight; calm last frame (page dip
               to s06 in the same stable at night)
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.loader import load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import cuts, snap
from stories.storm.scenes.s03_friends import Beats
from stories.nativity.scenes.s03_angel import blink, blinks_for, breathm, dipm, gate, hen_svg, hopm, stepper
from stories.nativity.scenes.s04_journey import (AK, ARRIVAL_CAM, AY, DONKEY_CYCLE, HS, JOSEPH_STEP, WS, Travellers,
                                                 add_arrival, clamp_cam, donkey_svg, joseph)

INK = P["ink"]


def doc(body, defs=""):
    return S.svg_doc(body, defs, WS, HS)


def s04_offset(ctx):
    """s05 time 0 = this many seconds into s04 (their cross-dissolve overlap)."""
    try:
        tl = load_timeline()
        prev = next(s for s in tl["scenes"] if s["id"] == "s04_journey")
        return ctx.start - prev["start"]
    except Exception:
        return 31.6


# ================================================================== the busy street
SY = 760                 # bethlehem_town street line (house doors at SY - 30)
TY = 992                 # the travellers' ground line in the street
KS = 0.85                # the travellers' scale in the street


def street_back_svg():
    b = PR.starry_sky(-40, -40, WS + 40, 760, density=0.5, milky_way=False, time="dusk", seed=9)
    b += PR.bethlehem_town(-100, WS + 100, 560, 0.85, "dusk", "back", seed=7)
    b += PR.bethlehem_town(-100, WS + 100, SY, 1.0, "dusk", "street", seed=9)
    b += f'<rect x="-40" y="{SY + 360}" width="{WS + 80}" height="200" fill="{PR._nt("#a88a62", "dusk")}"/>'
    return doc(b)


def crowd_svg(k, layer):
    if layer == 0:
        return doc(C.townsfolk_crowd(1700, 880, 0.78, 1, n=36, pose="squeeze", width=3500, rows=3, seed=5, phase=k / 3))
    return doc(C.townsfolk_crowd(1700, 935, 0.86, -1, n=26, pose="squeeze", width=3300, rows=2, seed=8, phase=k / 3 + 0.2,
                                 animals=False))


POTS = (1330, 952)
HENW = (1960, 950)


def flying_hen_frames(x, y):
    """The hen flapping up out of the basket (two wing frames: wings up / down)."""
    out = []
    for up in (True, False):
        b = hen_svg(x, y, 0.9, 1, False, "#f4ead8")
        wy = y - 46
        d = (f"M{x - 6},{wy} Q{x - 40},{wy - (56 if up else -4)} {x - 66},{wy - (40 if up else -26)} "
             f"Q{x - 40},{wy - (20 if up else -12)} {x - 6},{wy + 6} Z")
        b += S.g(f'<path d="{d}" fill="#f4ead8" stroke="{INK}" stroke-width="2.8"/>', filter="wobble-fine")
        for i in range(3):
            b += S.g(f'<ellipse cx="{x - 50 + 30 * i}" cy="{y - 90 - 10 * (i % 2) - (14 if up else 0)}" rx="7" ry="3.5" '
                     f'fill="#f4ead8" stroke="{INK}" stroke-width="1.8" transform="rotate({-30 + 25 * i} {x - 50 + 30 * i} '
                     f'{y - 90})"/>', filter="wobble-fine")
        out.append(doc(b))
    return out


# ================================================================== the inn
IX, IY, IS = 1250, 930, 0.95
KI = 0.95


def inn_back_svg(door):
    b = PR.starry_sky(-40, -40, 2200, 760, density=0.55, milky_way=False, time="dusk", seed=13)
    b += PR.bethlehem_town(-100, 2300, 600, 0.8, "dusk", "back", seed=21)
    b += PR.bethlehem_town(-100, 2300, IY - 30, 1.0, "dusk", "street", seed=31)
    b += PR.inn(IX, IY, IS, -1, part="back", time="dusk", door=door, full=True)
    return doc(b)


def inn_front_svg():
    return doc(PR.inn(IX, IY, IS, -1, part="front", time="dusk"))


def zzz_svg():
    x, y = IX + 300 * IS, IY - 760 * IS
    return doc(f'<text x="{x}" y="{y}" font-family="LXGW WenKai" font-weight="bold" font-size="40" fill="{P["ink_soft"]}">z</text>')


# ================================================================== the stable
BX, BY, BS = 1056, 962, 0.8
KB = 0.8


def stable_svg(part, lamp):
    b = ""
    if part == "back":
        b += PR.starry_sky(-40, -40, 2200, 1240, density=0.6, milky_way=False, time="dusk", seed=17)
        gd = "M-60,1260 L-60,1000 Q500,975 1056,985 Q1600,995 2200,975 L2200,1260 Z"
        gnd = S.path(gd, fill=PR._nt("#8a8462", "dusk"), sw=3.4)
        rng = random.Random(23)
        for i in range(36):
            x, y = rng.uniform(-40, 2160), rng.uniform(1010, 1180)
            gnd += (f'<path d="M{x - 8:.0f},{y:.0f} l5,-15 l5,12 l5,-17 l5,13" fill="none" '
                    f'stroke="{PR._nt("#4f6a3a", "dusk")}" stroke-width="2.4"/>')
        for x, y, rx in ((200, 1080, 50), (1880, 1100, 44), (1700, 1150, 30)):
            gnd += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.55:.0f}" fill="{PR._nt("#a49a8a", "dusk")}" stroke="{INK}" stroke-width="3"/>'
        b += S.g(gnd, filter="wobble")
    b += PR.stable(BX, BY, BS, 1, part=part, lamp=lamp, time="dusk", manger=True)
    return doc(b)


def spot(name):
    lx, ly = PR.STABLE_SPOTS[name]
    return BX + lx * BS, BY + ly * BS


# walk drawings and the planted-ankle advance at each cut (scale 1): a -> c -> b -> c -> a ...
MARY_ADV = (23, 50, 51, 22)
JOSEPH_ADV = (26, 60, 57, 29)
WALK_SEQ = ("walk_a", "walk_c", "walk_b", "walk_c")


def walk4(t0, n, per, adv, s):
    """Planted-foot 4-drawing walk: cut i at t0 + i*per advances adv[i % 4]*s. Returns (dx(t), frame(t) 0..3 or None
    before t0, t_end)."""
    cts = [snap(t0 + per * i) for i in range(1, n + 1)]

    def dx(t):
        x = 0.0
        for i, tc in enumerate(cts):
            x += adv[i % 4] * s * M.progress(t, tc - 0.05, tc + 0.07, "sine")
        return x

    def fr(t):
        if t < t0:
            return None
        return sum(1 for tc in cts if t >= tc) % 4
    return dx, fr, cts[-1]


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=WS, H=HS)
    T = ctx.duration
    B = Beats(ctx)
    L = ctx.lines
    OFF = s04_offset(ctx)
    clock = lambda t: t + OFF                       # noqa: E731  the arrival page's own clock (s04 time)

    t_dao = B.at(0, "到了伯利恒")
    t_cutB = snap(B.at(0, "城里到处都是人") - 0.12)
    t_ji = B.at(0, "就像过年时的火车站一样挤", 11)
    t_huoche = B.at(0, "就像过年时的火车站一样挤", 6)
    t_cutC = snap(L[1].start - 0.3)
    t_ke = B.at(1, "客店里")
    t_li = B.at(1, "客店里", 2)
    t_yi = B.at(1, "已经没有地方了")
    t_df = B.at(1, "已经没有地方了", 4)
    t_cutD = snap(L[2].start - 0.25)
    t_zhu = B.at(2, "住了下来")
    t_xia = B.at(2, "住了下来", 2)

    # ================================================================ SHOT A: the arrival (s04's last page)
    gA = gate(-1, t_cutB)
    zt = add_arrival(sc, clock, gA, z0=20.0)
    step = JOSEPH_STEP * AK
    a_steps = [snap(max(t_dao + 0.2, 1.15) + 0.4 * j) for j in range(3)]
    a_steps = [ts for ts in a_steps if ts < t_cutB - 0.1]
    jdx, jdy, jn = stepper(a_steps, step, AK, lift=5)
    DX_END = 640.0
    lead_x = (PR.DONKEY_LEAD[0] - C.JOSEPH_LEAD_HAND[0]) * AK
    t_go = a_steps[0] - 0.1 if a_steps else t_cutB
    v = step / 0.4

    def dposA(t):
        u = t - t_go
        if u <= 0:
            return DX_END, AY, 1.0
        acc = 0.3
        d = v * u * u / (2 * acc) if u < acc else v * acc / 2 + v * (u - acc)
        return DX_END + d, AY, 1.0

    def dphaseA(t):
        if t < t_go:
            return None
        return ((dposA(t)[0] - DX_END) / (DONKEY_CYCLE * AK)) % 1.0

    def jposA(t):
        return DX_END + lead_x + jdx(t), AY + jdy(t), 1.0
    xj = [("lead_a", 1, "kind"), ("lead_b", 1, "kind"), ("stand", 1, "kind"), ("stand", 1, blink("kind"))]
    xm = ["weary", "kind", blink("kind")]
    t_lead = a_steps[0] if a_steps else t_cutB

    def jfA(t):
        if t < t_lead:
            return 2
        return (jn(t) + 1) % 2
    travA = Travellers(sc, "x", AK, DX_END, AY, xj, xm, z=zt, gatef=gA, seed=4400, clock=clock)
    travA.add(dposA, dphaseA, jposA, jfA, lambda t: 1, jextra=dipm(t_lead, AK, lambda t: jposA(t)[:2], 6))

    # ================================================================ SHOT B: the busy street
    gB = gate(t_cutB, t_cutC)
    sc.add("st_back", street_back_svg(), z=1.0, motion=gB, seed=5101)

    def jostle(i, amp=4.0):
        def m(t):
            press = math.exp(-((t - t_ji) / 0.35) ** 2)
            return Tf(dx=amp * math.sin(2 * math.pi * (t / 1.3 + 0.37 * i)) + (10 if i % 2 else -10) * press,
                      sy=1 - 0.012 * press, py=960, px=1700)
        return m
    for li in (0, 1):
        sc.add(f"st_crowd{li}", [crowd_svg(k, li) for k in range(3)], z=1.1 + 0.1 * li, seed=5110 + li,
               frame_at=lambda t, li=li: float(int(t / (0.34 + 0.07 * li)) % 3),
               motion=M.combine(gB, jostle(li, 3.0 + li)))
    # a man with a wobbling stack of pots on his head
    pfr = [doc(C.ground_shadow(*POTS, 0.9, 100, 0.15) + C.townsfolk(*POTS, 0.9, 1, kind="man", variant=2, pose="squeeze",
                                                                     item="pots"))]
    sc.add("st_pots", pfr, z=1.25, seed=5120,
           motion=M.combine(gB, lambda t: Tf(rot=2.5 * math.sin(2 * math.pi * t / 0.9) + 6 * math.exp(-((t - t_ji) / 0.3) ** 2),
                                             px=POTS[0], py=POTS[1])))
    # a woman with a hen in her basket (the hen bobs) - the hen flaps up on '挤'
    t_flap = snap(t_ji - 0.05)
    hfr = [doc(C.ground_shadow(*HENW, 0.88, 100, 0.15) + C.townsfolk(*HENW, 0.88, -1, kind="woman", variant=1, pose="squeeze",
                                                                      item="hen", phase=k / 4)) for k in range(4)]
    hfr.append(doc(C.ground_shadow(*HENW, 0.88, 100, 0.15) + C.townsfolk(*HENW, 0.88, -1, kind="woman", variant=1,
                                                                          pose="squeeze", item="basket",
                                                                          expr="surprised")))
    sc.add("st_henw", hfr, z=1.26, seed=5121,
           frame_at=lambda t: 4.0 if t >= t_flap else float(int(t / 0.18) % 4),
           motion=M.combine(gB, dipm(t_flap, 0.88, HENW, 6)))
    hb = C.body_points(C.townsfolk, *HENW, 0.88, -1, kind="woman", variant=1, pose="squeeze", item="hen")["bbox"]
    hx0, hy0 = (hb[0] + hb[2]) / 2, hb[1] + 40
    sc.add("st_hen", flying_hen_frames(hx0, hy0), z=1.5, seed=5122,
           frame_at=lambda t: float(int((t - t_flap) / 0.07) % 2) if t >= t_flap else 0.0,
           motion=M.combine(gB, lambda t: (Tf(alpha=0.0) if t < t_flap else
                                           Tf(dx=60 * M.progress(t, t_flap, t_flap + 1.0, "linear"),
                                              dy=-170 * math.sin(math.pi * min(1.0, (t - t_flap) / 1.2)) + 30 *
                                              M.progress(t, t_flap + 0.9, t_flap + 1.2, "in"),
                                              alpha=1.0 if t < t_cutC else 0.0))))
    # Joseph leading the donkey through the crowd, Mary riding
    sb_steps = []
    tt = snap(t_cutB + 0.25)
    while tt < t_cutC - 0.2:
        sb_steps.append(tt)
        tt = snap(tt + 0.56)
    stepb = JOSEPH_STEP * KS
    bjdx, bjdy, bjn = stepper(sb_steps, stepb, KS, lift=4)
    D0B = 560.0
    vb = stepb / 0.56
    lead_b = (PR.DONKEY_LEAD[0] - C.JOSEPH_LEAD_HAND[0]) * KS
    t_gob = sb_steps[0] - 0.12

    def dposB(t):
        u = t - t_gob
        if u <= 0:
            return D0B, TY, 1.0
        acc = 0.3
        d = vb * u * u / (2 * acc) if u < acc else vb * acc / 2 + vb * (u - acc)
        return D0B + d, TY, 1.0

    def dphaseB(t):
        if t < t_gob:
            return None
        return ((dposB(t)[0] - D0B) / (DONKEY_CYCLE * KS)) % 1.0

    def jposB(t):
        return D0B + lead_b + bjdx(t), TY + bjdy(t), 1.0
    bj = [("lead_a", 1, "worried"), ("lead_b", 1, "worried"), ("lead_a", 1, "kind"), ("lead_b", 1, "kind")]
    bm = ["weary", "worried", blink("weary")]
    t_wor = snap(t_huoche)

    def bjf(t):
        n = bjn(t)
        return (n + 1) % 2 + (0 if t >= t_wor else 2)

    def bmf(t):
        if t >= t_ji - 0.1:
            return 1
        return 2 if abs(t - (t_cutB + 1.6)) < 0.065 else 0
    travB = Travellers(sc, "b", KS, D0B, TY, bj, bm, z=1.6, gatef=gB, seed=5130)
    travB.add(dposB, dphaseB, jposB, bjf, bmf, mextra=dipm(snap(t_ji - 0.1), KS, lambda t: travB.seat, 5))

    # ================================================================ SHOT C: the inn
    gC = gate(t_cutC, t_cutD)
    t_open0 = snap(t_li - 0.05)
    t_open1 = snap(t_open0 + 0.12)
    sc.add("inn_back", [inn_back_svg(d_) for d_ in (0.0, 0.5, 1.0)], z=3.0, seed=5201,
           frame_at=cuts([(0, 0), (t_open0, 1), (t_open1, 2)]), motion=gC)
    t_kp = snap(t_yi - 0.05)
    kfr = [doc(C.townsfolk(IX, IY, KI, -1, kind="innkeeper", pose="stand", expr="sorry"))]
    kfr += [doc(C.townsfolk(IX, IY, KI, -1, kind="innkeeper", pose="shake_head", phase=k / 4)) for k in range(4)]
    kfr.append(doc(C.townsfolk(IX, IY, KI, -1, kind="innkeeper", pose="stand", expr=blink("sorry"))))

    def k_fa(t):
        if t < t_kp:
            return 0.0
        if t < t_kp + 1.25:
            return 1.0 + float(int((t - t_kp) / 0.14) % 4)
        return 5.0 if abs(t - (t_kp + 1.9)) < 0.065 else 0.0
    sc.add("innkeeper", kfr, z=3.1, seed=5202, frame_at=k_fa,
           motion=M.combine(gC, lambda t: Tf(alpha=gC(t).alpha * (1.0 if t >= t_open1 else 0.0)),
                            hopm(t_open1, KI, (IX, IY), 8, 0.2), dipm(t_kp, KI, (IX, IY), 5), breathm((IX, IY), 2.6, 0.01)))
    sc.add("inn_front", inn_front_svg(), z=3.2, seed=5203, motion=gC)
    sc.add("inn_z", zzz_svg(), z=3.25, wc=0,
           motion=M.combine(gC, lambda t: Tf(dy=-60 * ((t / 1.6) % 1.0), dx=14 * ((t / 1.6) % 1.0),
                                             alpha=math.sin(math.pi * ((t / 1.6) % 1.0)) * gC(t).alpha)))
    # the donkey with Mary waiting, Joseph at the door
    DXC, JXC = 600, 1052
    seat = PR.donkey_points(DXC, IY + 4, KI * 0.9, 1, "stand")["seat"]
    dfr = [doc(donkey_svg(DXC, IY + 4, KI * 0.9, 1, "stand")), doc(donkey_svg(DXC, IY + 4, KI * 0.9, 1, "stand", eyes="closed"))]
    sc.add("c_donkey", dfr, z=3.3, seed=5210, frame_at=lambda t: 1.0 if abs(t - (t_cutC + 1.1)) < 0.07 else 0.0,
           motion=M.combine(gC, lambda t: Tf(rot=0.8 * math.sin(2 * math.pi * t / 2.3), px=DXC, py=IY)))
    t_mw = snap(t_df + 0.1)
    mfr = [doc(C.mary(*seat, KI * 0.9, 1, pose="ride", expr=e, pregnant=True)) for e in ("weary", blink("weary"), "worried")]
    sc.add("c_mary", mfr, z=3.31, seed=5211, frame_at=cuts(blinks_for([(0, 0), (t_mw, 2)], [t_cutC + 0.9], {0: 1})),
           motion=M.combine(gC, dipm(t_mw, KI, seat, 4), breathm(seat, 2.9, 0.01)))
    t_talk = snap(t_open0 + 0.45)
    t_worry = snap(t_df - 0.05)
    jfr = [doc(joseph(JXC, IY + 4, KI, 1, "knock", "kind", phase=ph)) for ph in (0.0, 0.5)]
    jfr += [doc(joseph(JXC, IY + 4, KI, 1, "talk", "kind")), doc(joseph(JXC, IY + 4, KI, 1, "worry", "worried")),
            doc(joseph(JXC, IY + 4, KI, 1, "stand", "kind"))]
    t_knock = snap(t_ke - 0.1)

    def jc_fa(t):
        if t < t_talk:
            if t >= t_knock:
                return float(int((t - t_knock) / 0.13) % 2)
            return 4.0
        if t < t_worry:
            return 2.0
        return 3.0
    sc.add("c_joseph", jfr, z=3.4, seed=5212, frame_at=jc_fa,
           motion=M.combine(gC, dipm(t_knock, KI, (JXC, IY), 5), dipm(t_talk, KI, (JXC, IY), 5),
                            dipm(t_worry, KI, (JXC, IY), 6), breathm((JXC, IY), 3.0, 0.01)))
    # a warm flicker on the inn lamp
    lamp_xy = (IX - (-115 - 90) * IS - 20, IY + (-340 + 20) * IS + 90)
    sc.add("inn_glow", doc(f'<circle cx="{lamp_xy[0]:.0f}" cy="{lamp_xy[1]:.0f}" r="90" fill="#ffd36e" opacity="0.5"/>'), z=3.26,
           wc=0, blend="screen", motion=M.combine(gC, lambda t: Tf(alpha=gC(t).alpha * (0.5 + 0.3 * math.sin(t * 7.1) *
                                                                                        math.sin(t * 2.3)))))

    # ================================================================ SHOT D: the stable
    gD = gate(t_cutD, 1e9)
    t_l0 = snap(t_xia - 0.1)
    lamp_f = lambda t: M.progress(t, t_l0, t_l0 + 0.6, "sine")    # noqa: E731
    sc.add("sb_back", [stable_svg("back", 0.15), stable_svg("back", 1.0)], z=5.0, seed=5301, frame_at=lamp_f, motion=gD)
    # the donkey (theirs) and the ox
    dsx, dsy = spot("donkey")
    dsx += 20
    dsx -= 40
    sdfr = [doc(donkey_svg(dsx, dsy, KB * 0.9, 1, "lie")), doc(donkey_svg(dsx, dsy, KB * 0.9, 1, "lie", eyes="closed"))]
    sc.add("d_donkey", sdfr, z=5.1, seed=5302,
           frame_at=lambda t: 1.0 if any(abs(t - tb) < 0.07 for tb in (t_cutD + 1.4, t_cutD + 3.9)) else 0.0,
           motion=M.combine(gD, lambda t: Tf(rot=0.9 * math.sin(2 * math.pi * t / 2.7), px=dsx, py=dsy)))
    ox_x, ox_y = spot("ox")
    oxfr = [doc(C.ground_shadow(ox_x, ox_y, KB * 0.9, 260, 0.14) + PR.ox(ox_x, ox_y, KB * 0.9, -1, pose=p_, eyes=e))
            for p_, e in (("lie", "open"), ("lie", "closed"), ("lie_look", "happy"))]
    t_oxl = snap(t_cutD + 1.0)
    t_oxh = snap(t_zhu + 0.25)
    sc.add("d_ox", oxfr, z=5.12, seed=5303, frame_at=cuts(blinks_for([(0, 0), (t_oxh, 2)], [t_cutD + 2.3], {0: 1})),
           motion=M.combine(gD, dipm(t_oxh, KB, (ox_x, ox_y), 4),
                            lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * t / 3.3), px=ox_x, py=ox_y)))
    # the hay bale Mary sits on
    MXD = 990
    sc.add("d_bale", doc(PR.hay(MXD - 2, BY - 4, 0.58 * KB, kind="bale")), z=5.15, seed=5304, motion=gD)
    # Mary walks in and sits down
    mdx, mfr_, m_end = walk4(t_cutD + 0.12, 16, 0.17, MARY_ADV, KB)
    MX0 = MXD + sum(MARY_ADV[i % 4] for i in range(16)) * KB
    mdf = [doc(C.ground_shadow(MX0, BY, KB, 100, 0.16) + C.mary(MX0, BY, KB, -1, pose=p_, pregnant=True, expr="weary"))
           for p_ in WALK_SEQ[:3]]
    mdf += [doc(C.mary(MXD, BY, KB, 1, pose="sit", pregnant=True, expr=e)) for e in ("tender", blink("tender"), "kind")]
    t_sit = snap(t_zhu - 0.02)
    m_ents = blinks_for([(0, 3), (snap(t_sit + 1.0), 5)], [t_sit + 1.7], {5: 4})

    def md_fa(t):
        if t < t_sit:
            f = mfr_(t)
            return float((0, 1, 2, 1)[f if f is not None else 0])
        return float(cuts(m_ents)(t))

    def md_mot(t):
        if t < t_sit:
            return Tf(dx=-mdx(t))
        return Tf()
    sc.add("d_mary", mdf, z=5.2, seed=5305, frame_at=md_fa,
           motion=M.combine(gD, md_mot, hopm(t_sit, KB, (MXD, BY), 10, 0.22), breathm((MXD, BY), 3.0, 0.01)))
    # Joseph walks in, turns and holds up his lamp under the stable lamp
    jdx_, jfr_, j_end = walk4(t_cutD + 0.05, 15, 0.19, JOSEPH_ADV, KB)
    JXD = 800
    JX0 = JXD + sum(JOSEPH_ADV[i % 4] for i in range(15)) * KB
    jdf = [doc(joseph(JX0, BY - 6, KB, -1, p_, "kind")) for p_ in WALK_SEQ[:3]]
    jdf += [doc(C.ground_shadow(JXD, BY - 6, KB, 120, 0.16) + C.joseph_carpenter(JXD, BY - 6, KB, 1, pose="hold_lamp",
                                                                              expr=e, lamp=1.0))
            for e in ("kind", "tender")]
    t_jl = snap(t_zhu + 0.12)
    t_jt = snap(t_jl + 1.2)

    def jd_fa(t):
        if t < t_jl:
            f = jfr_(t)
            return float((0, 1, 2, 1)[f if f is not None else 0])
        return 3.0 if t < t_jt else 4.0

    def jd_mot(t):
        if t < t_jl:
            return Tf(dx=-jdx_(t))
        return Tf()
    sc.add("d_joseph", jdf, z=5.21, seed=5306, frame_at=jd_fa,
           motion=M.combine(gD, jd_mot, dipm(t_jl, KB, (JXD, BY), 6), breathm((JXD, BY), 3.1, 0.01, 0.4)))
    sc.add("sb_front", [stable_svg("front", 0.15), stable_svg("front", 1.0)], z=5.4, seed=5307, frame_at=lamp_f,
           motion=gD)
    lp = PR.stable_points(BX, BY, BS, 1)["lamp"]
    gdefs = S.rad_grad("n5lg", [(0, "#fff1c6", 0.75), (0.35, "#ffd36e", 0.35), (1, "#ffd36e", 0)])
    sc.add("d_glow", doc(f'<circle cx="{lp[0]:.0f}" cy="{lp[1]:.0f}" r="330" fill="url(#n5lg)"/>', gdefs), z=5.45, wc=0,
           blend="screen", motion=M.combine(gD, lambda t: Tf(alpha=gD(t).alpha * lamp_f(t) * (0.7 + 0.2 * math.sin(t * 6.3) *
                                                                                          math.sin(t * 1.9)))))
    sc.fx.append(lambda frame, t, view, f=FX.motes((BX - 450, BY - 420, BX + 420, BY - 60), count=22, t0=t_l0 + 0.3,
                                                   color=(255, 236, 190), size=(3, 6), seed=51, alpha=120):
                 f(frame, t, view) if t >= t_cutD else frame)

    # ================================================================ camera
    camA = M.cam_keys([(0, ARRIVAL_CAM), (1.0, ARRIVAL_CAM), (t_cutB, Cam(1000, 610, 1520))], "sine")
    camB = lambda t: Cam(dposB(t)[0] + 330, 650, 1820)            # noqa: E731
    camC = M.cam_keys([(t_cutC, Cam(1080, 610, 1780)), (t_cutD, Cam(1110, 620, 1700))], "sine")
    camD = M.cam_keys([(t_cutD, Cam(1056, 640, 1800)), (t_zhu, Cam(1030, 660, 1680)), (T, Cam(1010, 676, 1580))], "sine")

    def cam(t):
        if t < t_cutB:
            return clamp_cam(camA(t), 0, 2112)
        if t < t_cutC:
            return clamp_cam(camB(t))
        if t < t_cutD:
            return clamp_cam(camC(t), 0, 2200)
        return clamp_cam(camD(t), 0, 2112)
    sc.camera = cam

    # ================================================================ sound
    sc.sfx("night", 0, dur=t_cutB + 0.2, gain_db=-24, fade_in=0.6, fade_out=0.3)
    sc.sfx("wind_soft", 0, dur=t_cutB + 0.2, gain_db=-26, fade_in=0.6, fade_out=0.3)
    sc.sfx("footsteps", t_go, dur=t_cutB - t_go + 0.2, gain_db=-18, fade_in=0.2)
    sc.sfx("crowd", t_cutB, dur=t_cutC - t_cutB + 0.2, gain_db=-12, fade_in=0.15, fade_out=0.3)
    sc.sfx("footsteps", t_cutB + 0.2, dur=t_cutC - t_cutB - 0.2, gain_db=-20)
    sc.sfx("pop", t_flap, gain_db=-12, pan=0.4)
    sc.sfx("cloth", t_flap + 0.05, gain_db=-16, pan=0.4)
    sc.sfx("crowd", t_cutC, dur=t_cutD - t_cutC + 0.2, gain_db=-26, fade_in=0.2, fade_out=0.3)
    sc.sfx("hammer", t_knock, gain_db=-12)
    sc.sfx("cloth", t_open0, gain_db=-15)
    sc.sfx("night", t_cutD, dur=T - t_cutD + 0.3, gain_db=-22, fade_in=0.3, fade_out=1.0)
    sc.sfx("footsteps", t_cutD + 0.1, dur=2.9, gain_db=-21, fade_out=0.5)
    sc.sfx("fire", t_l0, dur=T - t_l0 + 0.3, gain_db=-24, fade_in=0.5, fade_out=1.0)
    sc.sfx("sparkle", t_l0 + 0.1, gain_db=-20)
    return sc
