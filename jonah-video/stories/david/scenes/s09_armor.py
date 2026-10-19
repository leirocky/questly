"""Scene 9 — Saul's armour (1 Samuel 17:38-39).

"扫罗王把自己的盔甲给大卫穿上。头上戴上铜头盔，身上穿上铠甲，腰上挂上一把大刀。大卫试着走了几步。哐当，哐当……哎呀，
太重了，根本走不动！'这些我穿不惯。' 大卫就把盔甲全都脱了下来。"

The same tent, stage and camera that s08 ends on (a plain 1 s cross-dissolve joins them): Saul has just blessed
David; David holds his staff; soldier A (the king's attendant) stands by the map table at the right, soldier B on
guard by the entrance. Comic, piece by piece:

  line 0  "扫罗王把自己的盔甲给大卫穿上。"  Saul turns to his attendant ("my armour!"); David lays his staff down (it tips
                                            over onto the rug with a clack); the attendant fetches the armour pile from
                                            the table and holds it out beside the king.
          "头上戴上铜头盔，"               Saul takes the bronze helmet, turns and lowers it onto David - clonk! - and
                                            it slides right down over his eyes (three little slips).
          "身上穿上铠甲，"                 Saul takes the mail coat and drops it over him - whoomp - far too long, it
                                            pools on the floor.
          "腰上挂上一把大刀。"             Saul stoops and hangs the long sword at his belt: David sags under the
                                            weight, the scabbard tip thunks onto the floor (dust).
  line 1  "大卫试着走了几步。"             a hop-turn; two careful steps toward the entrance;
          "哐当，哐当……"                 two big clanking steps, one per 哐当 (a hop, a clank burst, dust, the sword
                                            scraping);
          "哎呀，太重了，"                 he wobbles back on his heels, arms flailing, nearly tips over;
          "根本走不动！"                   he gets stuck, sinking a little, puffing.
  line 2  "这些我穿不惯。"                 he turns to Saul and pushes the helmet up to peek out: an honest, sorry face.
  line 3  "大卫就把盔甲全都脱了下来。"     the helmet comes off and clanks to the floor, the sword drops, he hops out of
                                            the mail coat, which slumps into a heap - himself again! He picks up his
                                            staff (bag on his hip); Saul shrugs and smiles. Calm last second.

Shared with s08 (imported): the tent drawings, positions, sprites, poses and helpers. Every cyclic motion runs on
s08's clock shifted by (s08 duration - 1 s), and the first second holds s08's last pose, so the dissolve matches.
Pose changes are hard cuts sold by squash-and-hop; carried pieces are separate sprites that follow the hands.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.loader import context
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s08_saul as A
from stories.david.scenes.s08_saul import (DAVID_POSE, D_ST, FY, INK, K, SAUL_END_X, SOLA_X, SOLB_X, DAVID_X, WALK_A,
                                           Actor, WalkPath, _P, clamp, doc, f1, pt, sprite, walk_adv, walk_drawings)

POSES = C.POSES
DX0 = DAVID_X                  # David at the start
SX = SAUL_END_X                # Saul (stands here the whole scene)


# ------------------------------------------------------------------ the armour pieces
def coat_held(cx, top, s=1.0):
    """Saul's mail coat held up by its shoulders (top centre cx, top): long grey ring mail with sleeves."""
    w, h = 150 * s, 300 * s
    sl = 64 * s
    d = (f"M{cx - w * 0.32},{top} L{cx + w * 0.32},{top} L{cx + w * 0.5 + sl},{top + 30 * s} "
         f"L{cx + w * 0.5 + sl * 0.85},{top + 96 * s} L{cx + w * 0.5},{top + 70 * s} L{cx + w * 0.62},{top + h} "
         f"Q{cx},{top + h + 26 * s} {cx - w * 0.62},{top + h} L{cx - w * 0.5},{top + 70 * s} "
         f"L{cx - w * 0.5 - sl * 0.85},{top + 96 * s} L{cx - w * 0.5 - sl},{top + 30 * s} Z")
    out = f'<path d="{d}" fill="{C.MAIL}" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>'
    ring = S.shade(C.MAIL, -0.3)
    for r_ in range(9):
        yy = top + 34 * s + r_ * 30 * s
        half = w * (0.36 + 0.26 * r_ / 8)
        n = int(2 * half / (20 * s))
        for j in range(n + 1):
            xx = cx - half + j * 2 * half / max(1, n) + (10 * s if r_ % 2 else 0)
            if abs(xx - cx) < half - 6 * s:
                out += f'<circle cx="{f1(xx)}" cy="{f1(yy)}" r="{f1(5 * s)}" fill="none" stroke="{ring}" stroke-width="{2 * s}"/>'
    out += (f'<path d="M{cx - 24 * s},{top} Q{cx},{top + 26 * s} {cx + 24 * s},{top}" fill="{S.shade(C.MAIL, -0.2)}" '
            f'stroke="{INK}" stroke-width="{3 * s}"/>')
    out += (f'<path d="M{cx - w * 0.55},{top + h - 16 * s} Q{cx},{top + h + 10 * s} {cx + w * 0.55},{top + h - 16 * s}" '
            f'fill="none" stroke="{S.shade(C.MAIL, -0.25)}" stroke-width="{6 * s}"/>')
    return S.g(out, filter="wobble-fine")


def mail_heap(cx, by, s=1.0):
    """The mail coat slumped into a heap on the floor (bottom centre cx, by)."""
    w = 170 * s
    d = (f"M{cx - w / 2},{by} C{cx - w / 2 + 6 * s},{by - 40 * s} {cx - 40 * s},{by - 66 * s} {cx - 6 * s},{by - 58 * s} "
         f"C{cx + 26 * s},{by - 76 * s} {cx + w / 2 - 6 * s},{by - 44 * s} {cx + w / 2},{by} Z")
    out = f'<path d="{d}" fill="{C.MAIL}" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>'
    ring = S.shade(C.MAIL, -0.3)
    for r_, (yy, half) in enumerate(((by - 46 * s, 40 * s), (by - 28 * s, 62 * s), (by - 12 * s, 74 * s))):
        n = int(2 * half / (20 * s))
        for j in range(n + 1):
            xx = cx - half + j * 2 * half / max(1, n) + (8 * s if r_ % 2 else 0)
            out += f'<circle cx="{f1(xx)}" cy="{f1(yy)}" r="{f1(5 * s)}" fill="none" stroke="{ring}" stroke-width="{2 * s}"/>'
    out += (f'<path d="M{cx - 20 * s},{by - 40 * s} q30,{-6 * s} {50 * s},{14 * s}" fill="none" stroke="{S.shade(C.MAIL, -0.25)}" '
            f'stroke-width="{4 * s}"/>')
    # a sleeve flopped over the edge
    out += (f'<path d="M{cx + 50 * s},{by - 30 * s} C{cx + 90 * s},{by - 34 * s} {cx + 110 * s},{by - 10 * s} {cx + 118 * s},{by} '
            f'L{cx + 84 * s},{by} C{cx + 80 * s},{by - 12 * s} {cx + 66 * s},{by - 14 * s} {cx + 50 * s},{by - 12 * s} Z" '
            f'fill="{C.MAIL}" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>')
    return S.g(out, filter="wobble-fine")


def clank_burst(cx, cy, s=1.0):
    """A comic clank: short radiating strokes and a little yellow star."""
    out = ""
    for i in range(7):
        a = math.radians(-160 + i * 23)
        out += (f'<path d="M{f1(cx + 34 * s * math.cos(a))},{f1(cy + 34 * s * math.sin(a))} '
                f'L{f1(cx + 66 * s * math.cos(a))},{f1(cy + 66 * s * math.sin(a))}" stroke="{P["ink_soft"]}" '
                f'stroke-width="{5 * s}" stroke-linecap="round"/>')
    pts = []
    for i in range(10):
        r = (24 if i % 2 == 0 else 10) * s
        a = math.radians(-90 + 36 * i)
        pts.append(f"{f1(cx + r * math.cos(a))},{f1(cy + r * math.sin(a))}")
    out += f'<path d="M{" L".join(pts)} Z" fill="#f6d36a" stroke="{INK}" stroke-width="{3 * s}" stroke-linejoin="round"/>'
    return S.g(out, filter="wobble-fine")


def dust_puff(cx, cy, s=1.0):
    out = ""
    for dx, dy, r in ((-40, -6, 22), (-12, -16, 28), (20, -10, 24), (44, -2, 18)):
        out += (f'<circle cx="{f1(cx + dx * s)}" cy="{f1(cy + dy * s)}" r="{f1(r * s)}" fill="#efe1c2" '
                f'stroke="{P["ink_soft"]}" stroke-width="{2.5 * s}" opacity="0.9"/>')
    return S.g(out, filter="wobble-fine")


# ------------------------------------------------------------------ poses
SAUL_HOLD = _P(t=10, h=2, arms=(("fk", 94, 104), ("fk", 98, 110)), hands=("open", "open"), expr="kind")
SAUL_LOWER = _P(t=16, h=8, arms=(("fk", 80, 90), ("fk", 84, 94)), hands=("open", "open"), expr="kind",
                look=(0.02, 0.06))
SAUL_STOOP = _P(t=22, h=6, drop=10, legs=(("ik", 30, 1), ("ik", -24, 1)), arms=(("fk", 70, 80), ("fk", 74, 86)),
                hands=("fist", "fist"), expr="kind", look=(0.02, 0.08))
SAUL_SHRUG = _P(h=-4, arms=(("fk", 40, 110), ("fk", 40, 110)), hands=("open", "open"), expr="laugh")
SOLD_CARRY = _P(t=4, arms=(("fk", 60, 96), ("fk", 66, 100)), hands=("open", "open"), expr="happy")
DAV_PLAIN = _P(arms=(("fk", 14, 8), ("fk", -8, -3)))
DAV_LOOKUP = _P(h=-20, look=(0.02, -0.1), arms=(("fk", 14, 8), ("fk", -8, -3)))
DAV_PEEK = _P(h=-4, arms=(("fk", 165, 185), ("fk", -8, -3)), hands=("open", "fist"))
DAV_FREE = _P(h=-8, arms=(("fk", 110, 130), ("fk", -110, -130)), hands=("open", "open"))


def hands_mid(fn, x, y, facing):
    h = C.body_points(fn, x, y, K, facing)["hands"]
    return (h[0][0] + h[1][0]) / 2, (h[0][1] + h[1][1]) / 2


def split_chunk(ctx, i, chunk_i, n):
    """Start times of the n voiced bursts inside subtitle chunk chunk_i of line i (falls back to an even split)."""
    c = ctx.lines[i].chunks[chunk_i]
    segs = A.voice_segs(ctx, i)
    if segs:
        inside = [s_ for s_ in segs if c.start - 0.15 <= s_[0] <= c.end]
        if len(inside) == n:
            return [s_[0] for s_ in inside]
    return [c.start + (c.end - c.start) * k / n for k in range(n)]


def keyed_pos(keys, curve="inout"):
    """[(t, x, y)] -> f(t) -> (x, y), eased between keys."""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1], keys[0][2]
        for (t0, x0, y0), (t1, x1, y1) in zip(keys, keys[1:]):
            if t <= t1:
                u = M.progress(t, t0, t1, curve)
                return M.lerp(x0, x1, u), M.lerp(y0, y1, u)
        return keys[-1][1], keys[-1][2]
    return f


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=A.SW, H=A.SH)
    T = ctx.duration
    L = ctx.lines
    try:
        D8 = context("s08_saul").duration
    except Exception:
        D8 = 52.43
    toff = D8 - 1.0                                   # s08's clock at this scene's t = 0 (the dissolve's start)

    # ------------------------------------------------------------ beats
    t_s = pt(ctx, 0, "扫罗王把自己")
    t_give = pt(ctx, 0, "给大卫穿上")
    t_helm = pt(ctx, 0, "头上戴上")
    t_mail = pt(ctx, 0, "身上穿上")
    t_sword = pt(ctx, 0, "腰上挂上")
    t_try = pt(ctx, 1, "大卫试着")
    t_k1, t_k2, t_aiya, t_heavy, t_stuck = split_chunk(ctx, 1, 1, 5)
    t_say = L[2].start
    t_off = L[3].start

    # soldier A fetches the armour
    a_go = t_s + 0.4
    a_pick = a_go + 0.55
    a_back = a_pick + 0.3
    AX1 = SOLA_X + 100                                 # at the table
    AX2 = SX + 245                                     # beside the king
    # the three dressing cycles
    t_take1 = max(a_back + 0.95, t_give + 0.2)
    t_hold1 = t_take1 + 0.5
    t_low1 = t_helm + 0.05
    t_land1 = t_low1 + 0.32
    t_take2 = t_land1 + 0.45
    t_hold2 = t_take2 + 0.5
    t_low2 = max(t_mail + 0.05, t_hold2 + 0.4)
    t_land2 = t_low2 + 0.28
    t_take3 = t_land2 + 0.42
    t_hold3 = t_take3 + 0.5
    t_low3 = max(t_sword + 0.05, t_hold3 + 0.4)
    t_land3 = t_low3 + 0.3
    # undressing
    t_h_off = t_off + 0.08
    t_h_land = t_h_off + 0.55
    t_sw_off = t_off + 0.75
    t_sw_land = t_sw_off + 0.25
    t_m_off = t_off + 1.3
    t_kneel = t_off + 1.95
    t_pick = t_kneel + 0.45
    t_shrug = t_off + 1.6

    # ------------------------------------------------------------ TENT
    states = lambda t: "all" if t < a_pick else "none"
    A.add_tent(sc, toff=toff, table_items=states)
    gx = (DAVID_X + SX) / 2
    sc.add("bless_glow", S.svg_doc(f'<ellipse cx="{gx}" cy="{FY - 200}" rx="330" ry="300" fill="url(#s9bg)"/>',
                                   S.rad_grad("s9bg", [(0, "#fff0bc", 0.6), (0.6, "#ffe6a0", 0.2), (1, "#ffe6a0", 0)]),
                                   w=A.SW, h=A.SH), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(0.85 + 0.15 * math.sin(2 * math.pi * (t + toff) / 2.8)) *
                               (1 - M.progress(t, 0.6, 2.2, "sine"))))

    # ------------------------------------------------------------ David's staff (laid down, picked up again)
    D0 = C._david_design(False, True)
    st_fn = A.david_fig(DAVID_POSE["stand"][0], "happy", front=C._staff_near(D0))
    hand_n = C.body_points(st_fn, DX0, FY, K, 1)["hands"][1]
    STX = hand_n[0] + 4 * K                           # the staff's tip on the floor
    t_drop = t_s + 0.45
    staff_rot = lambda t: (-86 * M.ease("in")(clamp((t - t_drop) / 0.38)) +
                           (5 * math.sin(math.pi * clamp((t - t_drop - 0.38) / 0.22)) if t > t_drop + 0.38 else 0))
    sc.add("staff", doc(PR.staff(STX, FY + 26, 1.1 * K, 1)), wc=0.6,
           motion=lambda t: Tf(rot=staff_rot(t), alpha=1.0 if t_drop <= t < t_pick else 0.0, px=STX, py=FY + 26))

    # ------------------------------------------------------------ SAUL
    spS = A.saul_sprite()
    s_bless = spS.add(A.saul_fig(A.SAUL_BLESS, "kind")(spS.ax, spS.ay, K, -1))
    s_talk_r = spS.add(C.king(spS.ax, spS.ay, K, 1, pose="talk", attire="saul", expr="kind", stool=False))
    s_take_r = spS.add(A.saul_fig(dict(POSES["reach_out"]), "kind")(spS.ax, spS.ay, K, 1))
    s_hold = spS.add(A.saul_fig(SAUL_HOLD)(spS.ax, spS.ay, K, -1))
    s_lower = spS.add(A.saul_fig(SAUL_LOWER)(spS.ax, spS.ay, K, -1))
    s_stoop = spS.add(A.saul_fig(SAUL_STOOP)(spS.ax, spS.ay, K, -1))
    s_stand = spS.add(C.king(spS.ax, spS.ay, K, -1, pose="stand", attire="saul", expr="kind", stool=False))
    s_worry = spS.add(C.king(spS.ax, spS.ay, K, -1, pose="stand", attire="saul", expr="worried", stool=False))
    s_shrug = spS.add(A.saul_fig(SAUL_SHRUG)(spS.ax, spS.ay, K, -1))
    s_sched = [(0, s_bless, 0), (t_s + 0.05, s_talk_r, 1.0),
               (t_take1, s_take_r, 0.5), (t_hold1, s_hold, 1.0), (t_low1, s_lower, 0.35),
               (t_take2, s_take_r, 0.8), (t_hold2, s_hold, 1.0), (t_low2, s_lower, 0.35),
               (t_take3, s_take_r, 0.8), (t_hold3, s_stoop, 1.0), (t_land3 + 0.45, s_stand, 0.7),
               (t_aiya + 0.15, s_worry, 0.5), (t_say + 0.7, s_stand, 0.4), (t_shrug, s_shrug, 0.9),
               (T - 1.2, s_stand, 0.4)]
    saul = A.Actor(spS, s_sched, lambda t: (SX, FY), bper=3.6, phase=0.5 + toff / 3.6, breathe=0.008)
    A.shadow_layer(sc, "shS", lambda t: SX, width=170)
    sc.add_dynamic("saul", saul)
    H_take = hands_mid(A.saul_fig(dict(POSES["reach_out"]), "kind"), SX, FY, 1)
    H_hold = hands_mid(A.saul_fig(SAUL_HOLD), SX, FY, -1)
    H_low = hands_mid(A.saul_fig(SAUL_LOWER), SX, FY, -1)
    H_stoop = hands_mid(A.saul_fig(SAUL_STOOP), SX, FY, -1)

    # ------------------------------------------------------------ SOLDIER A (fetches the armour pile)
    spA = sprite(560, 620, 280, 590, seed=63)
    a_happy = spA.add(A.soldier_fig(1, dict(POSES["stand"]), "happy")(spA.ax, spA.ay, K, -1))
    a_stand_r = spA.add(A.soldier_fig(1, dict(POSES["stand"]), "happy")(spA.ax, spA.ay, K, 1))
    a_carry = spA.add(A.soldier_fig(1, SOLD_CARRY)(spA.ax, spA.ay, K, -1))
    a_carry_r = spA.add(A.soldier_fig(1, SOLD_CARRY)(spA.ax, spA.ay, K, 1))
    a_laugh = spA.add(A.soldier_fig(1, dict(POSES["stand"]), "laugh")(spA.ax, spA.ay, K, -1))
    aw_r = walk_drawings(spA, lambda ps: A.soldier_fig(1, ps, "happy"), K, 1, WALK_A)
    aw_l = walk_drawings(spA, lambda ps: A.soldier_fig(1, ps, "happy"), K, -1, WALK_A,
                         arm=((("fk", 60, 96), "open"), (("fk", 66, 100), "open")))
    adv = walk_adv(WALK_A, K)
    a_path = WalkPath([(a_go + 0.1, SOLA_X, AX1, 22.0), (a_back + 0.12, AX1, AX2, 22.0)], [aw_r, aw_l], adv)
    t_aarr = a_path.end(1)
    a_sched = [(0, a_happy, 0), (a_go, a_stand_r, 0.8), (a_pick, a_carry_r, 0.6), (a_back, a_carry, 0.8),
               (t_aarr, a_carry, 0.3), (t_take3 + 0.35, a_happy, 0.5), (t_aiya + 0.1, a_laugh, 0.4),
               (t_stuck + 0.6, a_happy, 0.3)]
    A.shadow_layer(sc, "shA", lambda t: a_path.x(t))
    soldierA = A.Actor(spA, a_sched, lambda t: (a_path.x(t), FY), walk=a_path.frame, bper=3.4, phase=0.2 + toff / 3.4)
    sc.add_dynamic("soldierA", soldierA)
    # the pile in his hands (drawn in front of him)
    spP = sprite(260, 220, 130, 200, wc=0.6, seed=65)
    pile_d = {k_: spP.add(A.armour_pile(spP.ax, spP.ay, k_, 1.25)) for k_ in ("all", "mail_sword", "sword")}
    walk_hand = {}

    def a_hands(t):
        fr = soldierA.frame(t)
        if fr not in walk_hand:
            # hand centre of this drawing, relative to the anchor
            walk_hand[fr] = None
        x = a_path.x(t)
        facing = -1 if t >= a_back else 1
        base = hands_mid(A.soldier_fig(1, SOLD_CARRY), x, FY, facing)
        return base[0], base[1] + soldierA.hop(t)[1]

    def pile_state(t):
        if t < a_pick or t >= t_take3 + 0.05:
            return None
        if t < t_take1 + 0.05:
            return "all"
        if t < t_take2 + 0.05:
            return "mail_sword"
        return "sword"

    def pile_dyn(t):
        st = pile_state(t)
        if st is None:
            return None
        x, y = a_hands(t)
        return spP.place(pile_d[st], x - 6 * (-1 if t >= a_back else 1), y + 22)

    # ------------------------------------------------------------ DAVID
    spD = A.david_sprite()
    dd = {}
    D_st = DAVID_POSE["stand"]
    dd["staff"] = spD.add(A.david_fig(D_st[0], "happy", front=C._staff_near(D0))(spD.ax, spD.ay, K, 1))
    dd["plain"] = spD.add(A.david_fig(DAV_PLAIN, "happy")(spD.ax, spD.ay, K, 1))
    dd["lookup"] = spD.add(A.david_fig(DAV_LOOKUP, "surprised")(spD.ax, spD.ay, K, 1))
    for k_ in (1.0, 0.6, 0.25):
        dd[f"h{k_}"] = spD.add(A.david_fig(DAV_LOOKUP if k_ > 0.9 else DAV_PLAIN, "surprised",
                                           hat=A.helmet_hat(k_, tilt=7 - 9 * k_))(spD.ax, spD.ay, K, 1))
    dd["h0"] = spD.add(A.david_fig(DAV_PLAIN, "surprised", hat=A.helmet_hat(0.0))(spD.ax, spD.ay, K, 1))
    dd["h0laugh"] = spD.add(A.david_fig(DAV_PLAIN, "laugh", hat=A.helmet_hat(0.0))(spD.ax, spD.ay, K, 1))
    dd["mail"] = spD.add(A.david_fig(DAV_PLAIN, "surprised", mail=True, mid=None, hat=A.helmet_hat(0.0))(
        spD.ax, spD.ay, K, 1))
    dd["mail_laugh"] = spD.add(A.david_fig(DAV_PLAIN, "laugh", mail=True, mid=None, hat=A.helmet_hat(0.0))(
        spD.ax, spD.ay, K, 1))
    dd["full"] = spD.add(C.david(spD.ax, spD.ay, K, 1, pose="stand", armor=True, expr="worried"))
    dd["full_l"] = spD.add(C.david(spD.ax, spD.ay, K, -1, pose="stand", armor=True, expr="worried"))
    dd["walk_a"] = spD.add(C.david(spD.ax, spD.ay, K, -1, pose="walk_a", armor=True, expr="worried"))
    dd["walk_b"] = spD.add(C.david(spD.ax, spD.ay, K, -1, pose="walk_b", armor=True, expr="worried"))
    dd["wobble"] = spD.add(C.david(spD.ax, spD.ay, K, -1, pose="armor_wobble", armor=True, expr="scared",
                                   marks=False))
    dd["stuck"] = spD.add(C.david(spD.ax, spD.ay, K, -1, pose="stand", armor=True, expr="tired"))
    dd["peek"] = spD.add(A.david_fig(DAV_PEEK, "sorry", armor=True, hat=A.helmet_hat(0.75))(spD.ax, spD.ay, K, 1))
    dd["no_helm"] = spD.add(A.david_fig(DAV_PLAIN, "happy", armor=True, curls=True)(spD.ax, spD.ay, K, 1))
    dd["mail_only"] = spD.add(A.david_fig(DAV_PLAIN, "happy", mail=True, mid=None)(spD.ax, spD.ay, K, 1))
    dd["free"] = spD.add(A.david_fig(DAV_FREE, "laugh")(spD.ax, spD.ay, K, 1))
    dd["kneel"] = spD.add(C.david(spD.ax, spD.ay, K, 1, pose="kneel_pick"))
    dd["end"] = spD.add(A.david_fig(D_st[0], "happy", front=C._staff_near(D0))(spD.ax, spD.ay, K, 1))

    t_st1, t_st2 = t_try + 0.55, t_try + 1.15
    step_ts = [(t_st1, 30, "walk_a", 0.4), (t_st2, 30, "walk_b", 0.4), (t_k1, 40, "walk_a", 1.3),
               (t_k2, 40, "walk_b", 1.3)]
    DXW = DX0 - sum(s_[1] for s_ in step_ts)           # where he gets stuck
    DXE = DXW + 95                                     # after hopping out of the coat

    def d_x(t):
        x = DX0
        for ts, dx, _, _ in step_ts:
            x -= dx * M.progress(t, ts - 0.02, ts + 0.2, "out")
        x += (DXE - DXW) * M.progress(t, t_m_off - 0.02, t_m_off + 0.24, "sine")
        return x

    d_sched = [(0, dd["staff"], 0), (t_drop, dd["plain"], 0.4), (t_hold1 + 0.1, dd["lookup"], 0.5),
               (t_land1, dd["h1.0"], 0.9), (t_land1 + 0.16, dd["h0.6"], 0.35), (t_land1 + 0.3, dd["h0.25"], 0.3),
               (t_land1 + 0.44, dd["h0"], 0.5), (t_land1 + 1.0, dd["h0laugh"], 0.3),
               (t_land2, dd["mail"], 1.1), (t_land2 + 0.8, dd["mail_laugh"], 0.3),
               (t_land3, dd["full"], 0.9), (t_try, dd["full_l"], 0.8)]
    d_sched += [(ts, dd[p_], amp) for ts, dx, p_, amp in step_ts]
    d_sched += [(t_aiya, dd["wobble"], 1.0), (t_stuck, dd["stuck"], 0.6), (t_say - 0.05, dd["peek"], 1.0),
                (t_h_off, dd["no_helm"], 0.9), (t_sw_off, dd["mail_only"], 0.6), (t_m_off, dd["free"], 1.4),
                (t_kneel, dd["kneel"], 0.8), (t_pick, dd["end"], 1.0)]

    def d_rot(t):
        if t < t_aiya or t > t_stuck + 0.2:
            return 0.0
        u = t - t_aiya
        r = 13 * math.sin(2 * math.pi * u / 1.15) * math.exp(-u / 1.9)
        if t > t_heavy:
            r += 5 * math.sin(2 * math.pi * (t - t_heavy) / 0.7) * math.exp(-(t - t_heavy) / 0.6)
        return r * (1 - M.progress(t, t_stuck - 0.15, t_stuck + 0.05, "sine"))

    def d_squash(t):
        q = 1.0
        q -= 0.07 * M.progress(t, t_land3, t_land3 + 0.12, "out") * (1 - 0.5 * M.progress(t, t_land3 + 0.12,
                                                                                            t_land3 + 0.5, "sine"))
        q -= 0.03 * M.progress(t, t_stuck, t_stuck + 0.5, "sine") * (1 - M.progress(t, t_say - 0.3, t_say, "sine"))
        q += 0.035 * (M.progress(t, t_h_off, t_h_off + 0.3, "sine") * (1 - M.progress(t, t_m_off + 0.4,
                                                                                         t_m_off + 0.8, "sine")))
        return q if t < t_m_off else 1.0

    sc.add("heap", doc(mail_heap(DXW, FY + 8, 1.0 * K)), wc=0.6,
           motion=lambda t: Tf(alpha=1.0 if t >= t_m_off else 0.0,
                               sy=1 - 0.25 * (1 - M.progress(t, t_m_off, t_m_off + 0.25, "out")),
                               px=DXW, py=FY + 8))

    A.shadow_layer(sc, "shD", d_x, width=110)
    david = A.Actor(spD, d_sched, lambda t: (d_x(t), FY), rot=d_rot, squash=d_squash, bper=2.8,
                    phase=0.1 + toff / 2.8)
    sc.add_dynamic("david", david)
    sc.add_dynamic("pile", pile_dyn)

    # ------------------------------------------------------------ the carried pieces
    bp = lambda fn, x, f: C.body_points(fn, x, FY, K, f)
    head_k1 = bp(A.david_fig(DAV_LOOKUP, "surprised", hat=A.helmet_hat(1.0)), DX0, 1)["head"]
    neck = bp(A.david_fig(DAV_PLAIN, "happy"), DX0, 1)["shoulders"][1]
    hip = bp(A.david_fig(DAV_PLAIN, "happy"), DX0, 1)["pelvis"]
    pile0 = lambda t: a_hands(t)

    # helmet: pile -> Saul's hands -> held over David -> lowered onto his head
    spH = sprite(260, 220, 130, 190, wc=0.6, seed=66)
    h_draw = spH.add(PR.helmet_bronze(spH.ax, spH.ay, 1.12 * K, -1, crest=False, plume=C.CREST_RED, circlet=True))
    HR = 1.3 * K * 60                                  # helmet half width-ish

    def helm_pos(t):
        if t < t_take1 + 0.05:
            x, y = pile0(t)
            return x, y - 30
        if t < t_hold1:
            x0, y0 = pile0(t_take1 + 0.05)
            u = M.progress(t, t_take1 + 0.05, t_take1 + 0.3, "inout")
            return M.lerp(x0, H_take[0], u), M.lerp(y0 - 30, H_take[1] + 30, u)
        hop = saul.hop(t)[1]
        if t < t_low1:
            return H_hold[0] - 40, H_hold[1] + 34 + hop
        u = M.progress(t, t_low1, t_land1, "in")
        return M.lerp(H_low[0] - 40, head_k1[0] + 4, u), M.lerp(H_low[1] + 34, head_k1[1] - 18 * K, u) + hop

    sc.add_dynamic("helmet", A.Actor(spH, [(0, h_draw, 0)], helm_pos, breathe=0,
                                     alpha=lambda t: 1.0 if t_take1 + 0.05 <= t < t_land1 else 0.0))

    # mail coat: a folded bundle in the hands; when it is dropped it unfurls over him
    spC = sprite(320, 440, 160, 30, wc=0.6, seed=67)
    c_draw = spC.add(coat_held(spC.ax, spC.ay, 0.95 * K))
    spF = sprite(240, 120, 120, 100, wc=0.6, seed=69)
    f_draw = spF.add(A.mail_folded(spF.ax, spF.ay - 30, 1.25))
    head_top = bp(A.david_fig(DAV_LOOKUP, "surprised"), DX0, 1)["head_top"]

    def fold_pos(t):
        if t < t_hold2:
            x0, y0 = pile0(t_take2 + 0.05)
            u = M.progress(t, t_take2 + 0.05, t_take2 + 0.3, "inout")
            return M.lerp(x0, H_take[0], u), M.lerp(y0 - 20, H_take[1] + 10, u)
        return H_hold[0] - 40, H_hold[1] + 24 + saul.hop(t)[1]

    sc.add_dynamic("mailfold", A.Actor(spF, [(0, f_draw, 0)], fold_pos, breathe=0,
                                       alpha=lambda t: 1.0 if t_take2 + 0.05 <= t < t_low2 else 0.0))

    def coat_pos(t):
        u = M.progress(t, t_low2, t_land2, "in")
        return M.lerp(head_top[0] + 4, neck[0] + 6, u), M.lerp(head_top[1] - 150, neck[1] - 12, u)

    sc.add_dynamic("coat", A.Actor(spC, [(0, c_draw, 0)], coat_pos, breathe=0,
                                   alpha=lambda t: 1.0 if t_low2 <= t < t_land2 else 0.0,
                                   squash=lambda t: 0.55 + 0.45 * M.progress(t, t_low2, t_low2 + 0.12, "out")))

    # sword
    spW = sprite(320, 120, 160, 60, wc=0.6, seed=68)
    w_draw = spW.add(PR.sword(spW.ax, spW.ay, 0.75 * K, rot=0))

    def sword_pos(t):
        if t < t_hold3:
            x0, y0 = pile0(t_take3 + 0.05)
            u = M.progress(t, t_take3 + 0.05, t_take3 + 0.3, "inout")
            return M.lerp(x0, H_take[0], u), M.lerp(y0 - 20, H_take[1], u)
        hop = saul.hop(t)[1]
        if t < t_low3:
            return H_stoop[0], H_stoop[1] + hop
        u = M.progress(t, t_low3, t_land3, "inout")
        return M.lerp(H_stoop[0], hip[0] - 30, u), M.lerp(H_stoop[1], hip[1] + 40, u)

    sc.add_dynamic("sword", A.Actor(spW, [(0, w_draw, 0)], sword_pos, breathe=0,
                                    alpha=lambda t: 1.0 if t_take3 + 0.05 <= t < t_land3 else 0.0,
                                    rot=lambda t: -32 * M.progress(t, t_low3, t_land3, "inout")))

    # ------------------------------------------------------------ the pieces coming off
    HX_L, SW_L = DXW - 200, DXW - 10
    h_path = lambda t: (M.lerp(DXW + 6, HX_L, M.progress(t, t_h_off, t_h_land, "linear")),
                        M.lerp(head_k1[1] - 20, FY - 4, M.progress(t, t_h_off, t_h_land, "linear")) -
                        150 * math.sin(math.pi * clamp((t - t_h_off) / (t_h_land - t_h_off))) -
                        (14 * math.sin(math.pi * clamp((t - t_h_land) / 0.2)) if t > t_h_land else 0))
    sc.add_dynamic("helmet_off", A.Actor(spH, [(0, h_draw, 0)], h_path, breathe=0,
                                         alpha=lambda t: 1.0 if t >= t_h_off else 0.0,
                                         rot=lambda t: -360 * M.progress(t, t_h_off, t_h_land, "linear")))
    sw_path = lambda t: (M.lerp(hip[0] - 30 - (DX0 - DXW), SW_L, M.progress(t, t_sw_off, t_sw_land, "linear")),
                         M.lerp(hip[1] + 40, FY + 36, M.progress(t, t_sw_off, t_sw_land, "in")))
    sc.add_dynamic("sword_off", A.Actor(spW, [(0, w_draw, 0)], sw_path, breathe=0,
                                        alpha=lambda t: 1.0 if t >= t_sw_off else 0.0,
                                        rot=lambda t: -32 + 36 * M.progress(t, t_sw_off, t_sw_land, "in")))
    # ------------------------------------------------------------ clanks and dust
    def burst(name, x, y, t0, s=1.0):
        sc.add(name, doc(clank_burst(x, y, s)), wc=0,
               motion=lambda t: Tf(sx=0.6 + 0.5 * M.progress(t, t0, t0 + 0.12, "out"),
                                   sy=0.6 + 0.5 * M.progress(t, t0, t0 + 0.12, "out"),
                                   alpha=(1.0 if t0 <= t < t0 + 0.42 else 0.0) * (1 - M.progress(t, t0 + 0.25, t0 + 0.42, "sine")),
                                   px=x, py=y))

    def dust(name, x, y, t0, s=1.0):
        sc.add(name, doc(dust_puff(x, y, s)), wc=0,
               motion=lambda t: Tf(sx=0.5 + 0.8 * M.progress(t, t0, t0 + 0.6, "out"),
                                   sy=0.5 + 0.6 * M.progress(t, t0, t0 + 0.6, "out"),
                                   dy=-14 * M.progress(t, t0, t0 + 0.6, "out"),
                                   alpha=(1.0 if t >= t0 else 0.0) * (1 - M.progress(t, t0 + 0.15, t0 + 0.65, "sine")),
                                   px=x, py=y))

    burst("clank_helm", head_k1[0] + 40, head_k1[1] - 80, t_land1, 1.0)
    dust("dust_mail", DX0 + 10, FY + 6, t_land2, 1.1)
    tip_x = DX0 - 0.95 * 80 * K
    burst("clank_sword", tip_x - 10, FY - 40, t_land3, 0.8)
    dust("dust_sword", tip_x, FY + 4, t_land3, 0.9)
    x_k1 = DX0 - 60
    x_k2 = DX0 - 100
    htop = head_k1[1] - 70 * K
    burst("clank_k1", x_k1 - 10, htop, t_k1 + 0.05, 1.15)
    burst("clank_k1t", x_k1 + 100 * K, FY - 30, t_k1 + 0.07, 0.7)
    dust("dust_k1", x_k1 + 20, FY + 6, t_k1 + 0.05, 1.0)
    burst("clank_k2", x_k2 - 10, htop, t_k2 + 0.05, 1.15)
    burst("clank_k2t", x_k2 + 100 * K, FY - 30, t_k2 + 0.07, 0.7)
    dust("dust_k2", x_k2 + 20, FY + 6, t_k2 + 0.05, 1.0)
    burst("clank_h_off", HX_L, FY - 60, t_h_land, 0.9)
    burst("clank_sw_off", SW_L + 60, FY - 20, t_sw_land, 0.7)
    dust("dust_off", DXW, FY + 10, t_m_off + 0.05, 1.2)

    # ------------------------------------------------------------ SOLDIER B (on guard by the entrance, amused)
    spB = sprite(520, 680, 260, 640, seed=64)
    b_smile = spB.add(C.soldier(spB.ax, spB.ay, K, 1, variant=2, pose="stand", expr="happy"))
    b_laugh = spB.add(C.soldier(spB.ax, spB.ay, K, 1, variant=2, pose="stand", expr="laugh"))
    A.shadow_layer(sc, "shB", lambda t: SOLB_X, z=0.5)
    sc.add_dynamic("soldierB", A.Actor(spB, [(0, b_smile, 0), (t_k2 + 0.2, b_laugh, 0.4), (t_stuck + 0.8, b_smile, 0.3),
                                             (t_m_off + 0.2, b_laugh, 0.4), (T - 1.5, b_smile, 0.3)],
                                       lambda t: (SOLB_X, FY), bper=3.2, phase=0.7 + toff / 3.2))

    A.add_fg(sc, toff)

    # ------------------------------------------------------------ CAMERA
    c0 = A.CAM_MATCH
    c_fetch = Cam(1540, 1003, 1700)
    c_dress = Cam(1380, 1040, 1360)
    c_walk = Cam(1260, 1035, 1420)
    c_peek = Cam(1240, 1040, 1360)
    c_end = Cam(1220, 1025, 1480)
    sc.camera = M.cam_keys([(0.0, c0), (1.0, c0), (a_go + 0.9, c_fetch), (t_aarr - 0.3, c_fetch),
                            (t_take1 + 0.9, c_dress), (t_land3 + 0.6, c_dress), (t_k1 - 0.3, c_walk),
                            (t_say - 0.3, c_walk), (t_say + 0.8, c_peek), (t_off - 0.2, c_peek),
                            (t_off + 1.4, c_end), (T, Cam(1218, 1025, 1470))], "sine")

    motes = FX.motes((300, 400, 2600, 1300), count=26, color=(255, 240, 200), size=(3, 6), alpha=90)
    sc.fx = [lambda frame, t, view: motes(frame, t + toff, view),    # s08's motes, on s08's clock
             FX.vignette(lambda t: 0.28)]

    # ------------------------------------------------------------ SOUND
    sc.sfx("crowd", 0, dur=T + 0.8, gain_db=-28, fade_in=0.8, fade_out=1.0, pan=-0.4)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_s + 0.05, gain_db=-16, pan=0.2)
    sc.sfx("thud", t_drop + 0.38, gain_db=-14, pan=-0.1)
    sc.sfx("footsteps", a_go + 0.1, dur=t_aarr - a_go, gain_db=-16, fade_in=0.1, fade_out=0.2, pan=0.4)
    sc.sfx("coins", a_pick, gain_db=-14, pan=0.5)
    sc.sfx("cloth", t_take1, gain_db=-17, pan=0.2)
    sc.sfx("thud", t_land1, gain_db=-8)
    sc.sfx("coins", t_land1 + 0.02, gain_db=-12)
    sc.sfx("pop", t_land1 + 0.44, gain_db=-14)
    sc.sfx("cloth", t_low2, gain_db=-12)
    sc.sfx("coins", t_land2, gain_db=-10)
    sc.sfx("coins", t_land3 - 0.05, gain_db=-12)
    sc.sfx("thud", t_land3 + 0.02, gain_db=-8)
    for ts, dx, p_, amp in step_ts:
        if amp > 1:
            sc.sfx("thud", ts + 0.02, gain_db=-5, duck_db=-3)
            sc.sfx("coins", ts, gain_db=-6, duck_db=-3)
        else:
            sc.sfx("coins", ts, gain_db=-15)
    sc.sfx("whoosh", t_aiya, gain_db=-16)
    sc.sfx("cloth", t_heavy, gain_db=-16)
    sc.sfx("cloth", t_say - 0.05, gain_db=-15)
    sc.sfx("whoosh", t_h_off, gain_db=-16, pan=-0.2)
    sc.sfx("coins", t_h_land, gain_db=-8, pan=-0.3)
    sc.sfx("thud", t_h_land, gain_db=-10, pan=-0.3)
    sc.sfx("coins", t_sw_land, gain_db=-9, pan=-0.1)
    sc.sfx("cloth", t_m_off, gain_db=-12)
    sc.sfx("coins", t_m_off + 0.1, gain_db=-12)
    sc.sfx("pop", t_m_off + 0.05, gain_db=-14)
    sc.sfx("cloth", t_kneel, gain_db=-16)
    return sc
