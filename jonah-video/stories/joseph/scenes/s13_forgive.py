"""Scene 13 — "I am Joseph!" The brothers are forgiven; Jacob comes; the family together again (Genesis 45, 46, 50:20).

The same 5000 x 1188 stage, hall and camera as the end of s12_brothers (a plain cross-dissolve joins them): the ten
brothers kneel in two rows on the mat, Joseph stands before his gilded seat, two servants by the grain sacks.

  opening        = s12's last frame (calm).
  '约瑟再也忍不住了' Joseph turns and points the servants out; they bow and leave through the colonnade.
  '大哭起来'      he turns back and weeps (sobbing shakes, tears).
  Y '我就是约瑟'  he pulls off the court headcloth (hop-cut, the cloth flies onto his seat): his own dark curls - the
                 brothers look up, astonished.
  '吓坏了'        they jump up and back, scared (hands up, trembling).
  Y '不要害怕'    Joseph walks over to Judah and lays a hand on his shoulder (comfort); the brothers hang their heads;
  '上帝把它变成了好事' he points up: soft golden light pours down (light only), twinkles; the brothers look up;
  '救了许多人的性命' back to Judah, kind.
  '约瑟抱住哥哥们' he hugs Judah, then the brother beside him; the brothers' ashamed faces turn to tearful smiles.
  '爸爸雅各也来了' old Jacob comes in from the garden with his staff, little Benjamin beside him; Joseph runs to him and
                 they hug, both in happy tears.
  '一家人，又在一起了' the brothers cheer, Benjamin hops, hearts float up, warm light: the whole family together.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

from .s11_ruler import (arcs_markup, blink, clamp_cam, cuts, dip, f1, happy_hop, hop, joseph_bare, puff_markup, snap,
                        speaking, speaking_alpha, step_walk, twinkles_markup, when, with_blinks)
from .s12_brothers import (CH, CHX, FORM, G, JX, SC, SERVANTS, SH, SW, brother_pos, doc, hall_back_svg, hall_front_svg,
                           hall_light_svg, seat_svg, servant_frames, add_banners)

INK = P["ink"]
BACK = 36 * SC                      # the brothers jump back this far
JUDAH = 9                           # FORM index of Judah (front row, right)
NAPH = 8                            # FORM index of the brother hugged second (front row, next to Judah)
C_FAM = Cam(3600, 594, 2100)        # the whole family


def bro_x(k):
    x, y, s, v = brother_pos(k)
    return x - BACK, y, s, v


def headcloth_markup(x, y, s=1.0, rot=0.0):
    """Joseph's white court headcloth with thin gold stripes, crumpled (as he pulls it off)."""
    w, h = 120 * s, 70 * s
    out = (f'<path d="M{f1(-w / 2)},{f1(h * 0.3)} Q{f1(-w * 0.55)},{f1(-h * 0.6)} 0,{f1(-h * 0.62)} '
           f'Q{f1(w * 0.55)},{f1(-h * 0.6)} {f1(w / 2)},{f1(h * 0.3)} Q{f1(w * 0.2)},{f1(h * 0.55)} {f1(-w * 0.05)},{f1(h * 0.42)} '
           f'Q{f1(-w * 0.3)},{f1(h * 0.6)} {f1(-w / 2)},{f1(h * 0.3)} Z" fill="#f6efe0" stroke="{INK}" stroke-width="{f1(4 * s)}"/>')
    for k in range(4):
        yy = -h * 0.42 + k * h * 0.2
        out += (f'<path d="M{f1(-w * 0.42)},{f1(yy + 4 * s)} Q0,{f1(yy - 8 * s)} {f1(w * 0.42)},{f1(yy + 4 * s)}" fill="none" '
                f'stroke="#e6c97e" stroke-width="{f1(4 * s)}"/>')
    out += f'<path d="M{f1(-w * 0.46)},{f1(h * 0.12)} Q0,{f1(-h * 0.02)} {f1(w * 0.46)},{f1(h * 0.12)}" fill="none" stroke="#f2c14e" stroke-width="{f1(7 * s)}"/>'
    return f'<g transform="translate({f1(x)},{f1(y)}) rotate({rot:.1f})" filter="url(#wobble-fine)">{out}</g>'


def heart_markup(x, y, r):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.25)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.25)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} {f1(x)},{f1(y + r * 0.9)} Z")
    return (f'<path d="{d}" fill="#ee8a8a" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.45)}" rx="{f1(r * 0.22)}" ry="{f1(r * 0.14)}" fill="#fbd3cf" '
            f'transform="rotate(-35 {f1(x - r * 0.45)} {f1(y - r * 0.45)})"/>')


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]
    s = SC

    # ---- key times ----
    t_send = snap(L0.start + 0.15)                      # '约瑟再也忍不住了': servants out
    t_cry = snap(when(ctx, "大哭起来") - 0.1)             # he weeps
    t_reveal = snap(L1.start - 0.05)                    # '我就是约瑟': headcloth off
    t_look = snap(L1.start + 0.5)                       # the brothers look up
    t_scared = snap(L2.start + 0.05)                    # '吓坏了': they jump up and back
    t_worry = snap(L2.start + 1.3)                      # Joseph's concerned face
    t_walk = snap(L2.end + 0.25)                        # he walks over to Judah
    WALK_P = 0.26
    n_steps = 4
    jx_c = bro_x(JUDAH)[0] + 95 * s                     # comforting / hugging Judah from here
    fa_w, dxw, dyw, t_walk_end = step_walk(t_walk, n_steps, (jx_c - JX) / n_steps, WALK_P, s)
    t_comfort = snap(t_walk_end + 0.02)
    t_shame = snap(when(ctx, "你们本来想害我") + 0.2)       # the brothers hang their heads
    t_god = snap(when(ctx, "上帝把它变成了好事") - 0.05)    # point up, golden light
    t_lives = snap(when(ctx, "救了许多人的性命"))          # back to Judah
    t_hug1 = snap(L4.start + 0.1)                       # hugs Judah
    t_smile = snap(L4.start + 0.5)                      # the brothers smile through tears
    t_hug2 = snap(when(ctx, "原谅了他们") - 0.15)          # hugs the next brother
    t_jacob = snap(L4.at("后来") + 0.05)                 # Jacob comes in
    t_run = snap(t_jacob + 1.15)                        # Joseph runs to him
    t_hug3 = None                                       # Joseph and Jacob hug (set below: when both have arrived)
    t_fam = snap(L4.at("一家人") + 0.05)                  # the whole family

    # ---- camera ----
    CC = Cam(3640, 640, 1640)                           # closer on Joseph and Judah during the comfort

    def cam(t):
        c = CH
        k1 = M.progress(t, t_walk - 0.2, t_walk + 1.4, "sine") * (1 - M.progress(t, t_hug2 - 0.3, t_jacob + 0.6, "sine"))
        c = Cam(M.lerp(c.x, CC.x, k1), M.lerp(c.y, CC.y, k1), M.lerp(c.w, CC.w, k1))
        k2 = M.progress(t, t_hug2 - 0.3, t_jacob + 0.9, "sine")
        c = Cam(M.lerp(c.x, C_FAM.x, k2), M.lerp(c.y, C_FAM.y, k2), M.lerp(c.w, C_FAM.w, k2))
        return clamp_cam(c, SW, SH)
    sc.camera = cam

    # ---- the hall (identical to s12) ----
    sc.add("h_back", hall_back_svg(), z=10, seed=120)
    sc.add("h_light", hall_light_svg(), z=10.1, wc=0, blend="screen")
    sc.add("h_seat", seat_svg(), z=10.5, seed=121)
    add_banners(sc, ctx)

    # ---- servants: Joseph sends them out ----
    for i, (x, v, pose) in enumerate(SERVANTS):
        def E(p, f=1, x=x, v=v):
            return doc(C.ground_shadow(x, G - 30, s, 110) +
                       C.egyptian(x, G - 30, s, f, kind="servant", variant=v, pose=p, item="sack"))
        wa, wb = ("carry_walk_a", "carry_walk_b") if pose == "carry" else ("walk_a", "walk_b")
        fr = servant_frames(i) + [E(pose, -1)] + [E(pose, 1), E(wa), E(wb)]
        t_b = snap(t_send + 0.3 + 0.12 * i)              # they nod and turn ...
        t_w = snap(t_b + 0.45)                           # ... and go out
        fw, dxs, dys, _ = step_walk(t_w, 12, 80 * s, 0.24, s)

        def fa(t, fw=fw, t_b=t_b, base=cuts(with_blinks([(0, 0)], {0: 1}, [0.5 + 0.3 * i]))):
            w = fw(t)
            if w is not None:
                return 4.0 + w
            if t >= t_b:
                return 3.0
            return base(t)
        pv = (x, G - 30)
        sc.add(f"servant{i}", fr, z=10.6 + 0.01 * i, seed=122 + i, frame_at=fa,
               motion=M.combine(lambda t, dxs=dxs, dys=dys, x=x: Tf(dx=dxs(t), dy=dys(t),
                                                                   alpha=1 - M.progress(x + dxs(t), 4880, 4960)),
                                M.breathe(0.012, 2.8 + 0.3 * i, pivot=pv, phase=0.3 * i), dip(t_b, s, pv, 6)))

    # ---- the brothers ----
    order = sorted(range(10), key=lambda k: -FORM[k][0])
    bro_layers = {}
    for k in range(10):
        x, y, s_, v = brother_pos(k)
        xb = x - BACK

        def B(pose, expr, xx=x, y=y, s_=s_, v=v, f=1):
            return doc(C.ground_shadow(xx, y, s_, 130 if pose == "bow" else 110) +
                       C.brothers(xx, y, s_, f, variant=v, pose=pose, expr=expr, staff=False))
        # bow frames at the kneeling spot; standing frames at the spot they jump back to
        fr = [B("bow", "worried"), B("bow", blink("worried")), B("bow", "surprised"),          # 0, 1, 2
              B("scared", "scared", xb), B("sad", "ashamed", xb), B("sad", blink("ashamed"), xb),  # 3, 4, 5
              B("stand", "amazed", xb), B("stand", "tearful", xb), B("stand", blink("happy"), xb),  # 6, 7, 8
              B("cheer", "tearful", xb), B("stand", "sorry", xb)]                                  # 9, 10
        rank = order.index(k)
        ts = snap(t_scared + 0.035 * rank)
        ent = [(0, 0), (snap(t_look + 0.04 * rank), 2), (ts, 3), (snap(t_shame + 0.06 * rank), 4),
               (snap(t_god + 0.5 + 0.04 * rank), 6), (snap(t_lives + 0.3 + 0.04 * rank), 10),
               (snap(t_smile + 0.07 * rank), 7), (snap(t_fam + 0.06 * rank), 9)]
        blinks = with_blinks(ent, {0: 1, 4: 5, 7: 8}, [0.4 + 0.05 * k, 13.6 + 0.1 * k, 23.0 + 0.12 * k])
        pv = (xb, y)
        bro_layers[k] = (fr, blinks, pv, ts, s_)
    for k in range(10):
        if k in (JUDAH, NAPH):
            continue
        fr, blinks, pv, ts, s_ = bro_layers[k]
        tf = snap(t_fam + 0.06 * order.index(k))
        sc.add(f"bro{k}", fr, z=11 + (0 if FORM[k][1] else 0.5) + 0.01 * k, seed=130 + k, frame_at=cuts(blinks),
               motion=M.combine(M.breathe(0.012, 2.7 + 0.13 * k, pivot=pv, phase=0.17 * k),
                                dip(snap(t_look + 0.04 * order.index(k)), s_, pv, 4),
                                # the scared jump: up and back
                                hop(ts - 0.04, [(0, {"dy": 0}), (0.14, {"dy": -46 * s_}), (0.3, {"dy": 0, "sy": 0.94}),
                                                (0.44, {"sy": 1.0})], pv, ["out", "in", "sine"]),
                                lambda t, k=k, ts=ts: Tf(rot=1.2 * math.sin(2 * math.pi * t / 0.16 + k)
                                                         if ts + 0.4 < t < t_shame else 0.0, px=pv[0], py=pv[1]),
                                dip(snap(t_shame + 0.06 * order.index(k)), s_, pv, 5),
                                happy_hop(snap(t_smile + 0.07 * order.index(k)), s_, pv, 8),
                                happy_hop(tf, s_, pv, 22),
                                hop(tf + 0.6, [(0, {"dy": 0}), (0.18, {"dy": -16 * s_}), (0.36, {"dy": 0})], pv),
                                hop(tf + 1.25, [(0, {"dy": 0}), (0.18, {"dy": -12 * s_}), (0.36, {"dy": 0})], pv)))

    # Judah (comforted, hugged first) and the second brother: their own layers, hidden while inside a hug drawing
    def special(k, t_in, t_out, extra=()):
        fr, blinks, pv, ts, s_ = bro_layers[k]
        tf = snap(t_fam + 0.06 * order.index(k))
        sc.add(f"bro{k}", fr, z=11.5 + 0.01 * k, seed=130 + k, frame_at=cuts(blinks),
               motion=M.combine(lambda t: Tf(alpha=0.0 if t_in <= t < t_out else 1.0),
                                M.breathe(0.012, 2.7 + 0.13 * k, pivot=pv, phase=0.17 * k),
                                dip(snap(t_look + 0.04 * order.index(k)), s_, pv, 4),
                                hop(ts - 0.04, [(0, {"dy": 0}), (0.14, {"dy": -46 * s_}), (0.3, {"dy": 0, "sy": 0.94}),
                                                (0.44, {"sy": 1.0})], pv, ["out", "in", "sine"]),
                                lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * t / 0.16 + k)
                                             if ts + 0.4 < t < t_shame else 0.0, px=pv[0], py=pv[1]),
                                dip(snap(t_shame + 0.06 * order.index(k)), s_, pv, 5),
                                happy_hop(tf, s_, pv, 22),
                                hop(tf + 0.6, [(0, {"dy": 0}), (0.18, {"dy": -16 * s_}), (0.36, {"dy": 0})], pv),
                                *extra))
    special(JUDAH, t_hug1, t_hug2)
    special(NAPH, t_hug2, t_run, (dip(t_run, s, bro_layers[NAPH][2], 5),))

    # ---- Joseph ----
    # frames drawn at JX (ruler), then bare-headed at JX; walking / comfort frames at JX (moved by the walk)
    def J(pose, expr, f=-1, bare=True):
        if not bare:
            return doc(C.ground_shadow(JX, G, s, 120) + C.joseph(JX, G, s, f, pose=pose, expr=expr, attire="ruler"))
        return doc(C.ground_shadow(JX, G, s, 120) + joseph_bare(JX, G, s, f, pose=pose, expr=expr))
    jfr = [J("stand", "kind", bare=False), J("stand", blink("kind"), bare=False),           # 0, 1
           J("point", "sad", 1, bare=False),                                               # 2 send them out
           J("cry", "crying", bare=False),                                                 # 3 weeps
           J("open_arms", "tearful"),                                                      # 4 'I am Joseph!'
           J("stand", "worried"), J("stand", blink("worried")),                            # 5, 6
           J("walk_a", "kind"), J("walk_b", "kind"),                                       # 7, 8
           J("comfort", "kind"), J("comfort", blink("kind")),                              # 9, 10
           J("point_up", "kind"), J("open_arms", "tearful", 1),                            # 11, 12
           J("run_a", "tearful", 1), J("run_b", "tearful", 1)]                             # 13, 14
    t_turnback = snap(t_cry)
    j_ent = [(0, 0), (t_send, 2), (t_turnback, 3), (t_reveal, 4), (t_worry, 5), (t_comfort, 9), (t_god, 11),
             (t_lives, 9)]
    jbase = cuts(with_blinks(j_ent, {0: 1, 5: 6, 9: 10}, [0.45, 10.4, 13.9, 18.5]))
    # running to Jacob: from the second hug spot to the meeting place
    x_h2 = bro_x(NAPH)[0] + 95 * s                       # hugging the second brother here
    x_meet = 3985
    RUN_P = 0.16
    n_run = 4
    fr_run, dxr, dyr, t_run_end = step_walk(t_run, n_run, (x_meet - x_h2) / n_run, RUN_P, s, move=0.1, lift=10)
    t_open = snap(t_run_end)

    def j_fa(t):
        if t_walk <= t < t_walk_end:
            w = fa_w(t)
            return 7.0 + (w or 0.0)
        if t >= t_run:
            w = fr_run(t)
            if w is not None:
                return 13.0 + w
            return 12.0
        return jbase(t)

    def j_motion(t):
        hidden = (t_hug1 <= t < t_run) or t >= t_hug3
        if t < t_hug1:
            x = dxw(t)
            y = dyw(t)
        else:
            x = x_h2 - JX + dxr(t)
            y = dyr(t)
        return Tf(dx=x, dy=y, alpha=0.0 if hidden else 1.0)
    pvj = (JX, G)
    sc.add("joseph", jfr, z=11.8, seed=160, frame_at=j_fa,
           motion=M.combine(j_motion, M.breathe(0.01, 3.0, pivot=pvj),
                            dip(t_send, s, pvj, 6), dip(t_turnback, s, pvj, 6),
                            # sobbing
                            lambda t: Tf(dy=3 * abs(math.sin(2 * math.pi * t / 0.42)) if t_turnback + 0.3 < t < t_reveal - 0.15 else 0.0,
                                         rot=0.8 * math.sin(2 * math.pi * t / 0.42) if t_turnback + 0.3 < t < t_reveal - 0.15 else 0.0,
                                         px=JX, py=G),
                            happy_hop(t_reveal, s, pvj, 20), dip(t_worry, s, pvj, 5),
                            lambda t: dip(t_comfort, s, (jx_c, G), 6)(t), lambda t: dip(t_god, s, (jx_c, G), 5)(t),
                            lambda t: dip(t_lives, s, (jx_c, G), 5)(t)))
    # speaking arcs (Joseph's two lines)
    hp = C.body_points(C.joseph, JX, G, s, -1, pose="stand", attire="ruler")["head"]
    hpc = (hp[0] + (jx_c - JX), hp[1])
    sc.add("arcs1", [doc(arcs_markup(hp[0] - 58, hp[1] + 12, -1, -0.15, k, 0.9)) for k in (1, 2, 3)], z=11.9, wc=0,
           frame_at=speaking(None), motion=speaking_alpha([(L1.start + 0.05, L1.end)]))
    sc.add("arcs3", [doc(arcs_markup(hpc[0] - 58, hpc[1] + 12, -1, -0.25, k, 0.9)) for k in (1, 2, 3)], z=11.9, wc=0,
           frame_at=speaking(None), motion=speaking_alpha([(L3.start + 0.05, t_god - 0.1), (t_lives + 0.1, L3.end)]))

    # the headcloth: pulled off, flies onto the seat
    hc0 = (hp[0] + 4, hp[1] - 40)
    seat_top = (CHX - 6, G + PR.EGYPT_SEAT_Y * s - 16)
    t_fly1 = t_reveal + 0.5
    sc.add("headcloth", doc(headcloth_markup(hc0[0], hc0[1], s)), z=10.55, seed=165, motion=lambda t: Tf(
        dx=(seat_top[0] - hc0[0]) * M.progress(t, t_reveal, t_fly1, "inout"),
        dy=(seat_top[1] - hc0[1]) * M.progress(t, t_reveal, t_fly1, "in") - 150 * math.sin(math.pi * M.progress(t, t_reveal, t_fly1, "linear")),
        rot=200 * M.progress(t, t_reveal, t_fly1, "out") + (-20 if t >= t_fly1 else 0) * 0,
        sy=1 - 0.12 * math.sin(math.pi * M.progress(t, t_fly1, t_fly1 + 0.25, "linear")),
        px=hc0[0], py=hc0[1], alpha=1.0 if t >= t_reveal else 0.0))

    # the hugs
    jc_bare = lambda **kw: (joseph_bare, dict(kw))    # noqa: E731
    xJ, yJ, sJ, vJ = bro_x(JUDAH)
    hug1 = [doc(C.ground_shadow(jx_c - 40, G, s, 220) +
                C.hug_pair(jx_c, G, s, -1, a=jc_bare(expr=e1), b=(C.brothers, dict(variant=vJ, expr=e2, staff=False))))
            for e1, e2 in (("tearful", "crying"), ("tearful", "tearful"))]
    pvh1 = (jx_c - 40, G)
    sc.add("hug1", hug1, z=11.7, seed=170, frame_at=cuts([(0, 0), (snap(t_hug1 + 0.6), 1)]),
           motion=M.combine(lambda t: Tf(alpha=1.0 if t_hug1 <= t < t_hug2 else 0.0), dip(t_hug1, s, pvh1, 7),
                            hop(t_hug1 + 0.2, [(0, {"rot": 0}), (0.4, {"rot": -2.5}), (0.8, {"rot": 2}), (1.1, {"rot": 0})], pvh1)))
    xN, yN, sN, vN = bro_x(NAPH)
    hug2 = [doc(C.ground_shadow(x_h2 - 40, G, s, 220) +
                C.hug_pair(x_h2, G, s, -1, a=jc_bare(expr="tearful"), b=(C.brothers, dict(variant=vN, expr=e2, staff=False))))
            for e2 in ("crying", "tearful")]
    pvh2 = (x_h2 - 40, G)
    sc.add("hug2", hug2, z=11.75, seed=171, frame_at=cuts([(0, 0), (snap(t_hug2 + 0.5), 1)]),
           motion=M.combine(lambda t: Tf(alpha=1.0 if t_hug2 <= t < t_run else 0.0), dip(t_hug2, s, pvh2, 7),
                            hop(t_hug2 + 0.2, [(0, {"rot": 0}), (0.4, {"rot": 2.5}), (0.8, {"rot": -2}), (1.1, {"rot": 0})], pvh2)))

    # ---- Jacob (and Benjamin) come in from the garden ----
    xj_end = x_meet + 95 * s
    xj0 = xj_end + 640
    JW = 0.27
    nj = 8
    fj, dxj, dyj, t_j_end = step_walk(t_jacob, nj, (xj_end - xj0) / nj, JW, s)
    t_hug3 = snap(max(t_j_end, t_open) + 0.12)
    Jc = lambda pose, expr=None: doc(C.ground_shadow(xj_end, G, s, 120) + C.jacob(xj_end, G, s, -1, pose=pose, expr=expr))  # noqa: E731
    jcf = [Jc("walk_a", "tearful"), Jc("walk_b", "tearful"), Jc("open_arms", "tearful")]
    sc.add("jacob", jcf, z=11.6, seed=175,
           frame_at=lambda t: (fj(t) if fj(t) is not None else (2.0 if t >= t_j_end else 0.0)),
           motion=M.combine(lambda t: Tf(dx=dxj(t) + xj0 - xj_end, dy=dyj(t), alpha=0.0 if (t < t_jacob or t >= t_hug3) else 1.0),
                            M.breathe(0.01, 3.0, pivot=(xj_end, G))))
    # Benjamin a step behind him
    xb_end = xj_end + 150 * s
    xb0 = xb_end + 640
    fb, dxb, dyb, t_b_end = step_walk(t_jacob + 0.12, 10, (xb_end - xb0) / 10, 0.215, s * 0.7)
    Bj = lambda pose, expr=None: doc(C.ground_shadow(xb_end, G, s, 80) +                 # noqa: E731
                                     C.brothers(xb_end, G, s, -1, variant="benjamin", pose=pose, expr=expr))
    bjf = [Bj("walk_a", "happy"), Bj("walk_b", "happy"), Bj("stand", "tearful"), Bj("cheer", "happy"),
           Bj("stand", blink("happy"))]
    bbase = cuts(with_blinks([(0, 2), (t_fam, 3)], {2: 4}, [25.0]))
    pvb = (xb_end, G)
    sc.add("benjamin", bjf, z=11.65, seed=176,
           frame_at=lambda t: (fb(t) if fb(t) is not None else bbase(t)),
           motion=M.combine(lambda t: Tf(dx=dxb(t) + xb0 - xb_end, dy=dyb(t), alpha=0.0 if t < t_jacob else 1.0),
                            M.breathe(0.015, 2.4, pivot=pvb), happy_hop(t_fam, s, pvb, 26),
                            hop(t_fam + 0.55, [(0, {"dy": 0}), (0.17, {"dy": -22 * s}), (0.34, {"dy": 0})], pvb),
                            hop(t_fam + 1.1, [(0, {"dy": 0}), (0.17, {"dy": -18 * s}), (0.34, {"dy": 0})], pvb)))
    # Joseph and Jacob hug
    hug3 = [doc(C.ground_shadow(x_meet + 40, G, s, 230) +
                C.hug_pair(x_meet, G, s, 1, a=jc_bare(expr="tearful"), b=(C.jacob, dict(expr="tearful"))))]
    pvh3 = (x_meet + 40, G)
    sc.add("hug3", hug3, z=11.7, seed=177,
           motion=M.combine(lambda t: Tf(alpha=1.0 if t >= t_hug3 else 0.0), dip(t_hug3, s, pvh3, 8),
                            lambda t: Tf(rot=2.2 * math.sin(2 * math.pi * (t - t_hug3) / 2.4) if t > t_hug3 + 0.3 else 0.0,
                                         px=pvh3[0], py=pvh3[1])))

    # ---- light: God turned it to good (light only); the family's warm glow ----
    defs = S.rad_grad("gl13", [(0, "#fff3c4", 0.95), (0.55, "#ffe39a", 0.4), (1, "#ffe39a", 0)])
    sc.add("god_light", doc(f'<path d="{S.rays(jx_c - 80, -300, 150, 1450, 11, 5.5, rot=60)}" fill="#fff0bf" opacity="0.5" '
                            f'filter="url(#soft)"/><ellipse cx="{jx_c - 120}" cy="{G - 220}" rx="560" ry="380" fill="url(#gl13)"/>',
                            defs), z=12.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.85 * M.progress(t, t_god - 0.1, t_god + 1.0, "sine")
                               * (1 - 0.55 * M.progress(t, t_lives + 0.5, L3.end + 1.0, "sine"))
                               * (1 - M.progress(t, t_hug2, t_jacob + 0.5, "sine"))))
    defs2 = S.rad_grad("gl13b", [(0, "#ffeec0", 0.85), (0.6, "#ffd98a", 0.3), (1, "#ffd98a", 0)])
    sc.add("family_glow", doc(f'<ellipse cx="{x_meet - 150}" cy="{G - 240}" rx="1050" ry="460" fill="url(#gl13b)"/>', defs2),
           z=12.6, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.6 * M.progress(t, t_hug3, t_fam + 0.8, "sine") * (0.85 + 0.15 * math.sin(2 * math.pi * t / 2.2))))
    # hearts floating up from the hug and over the family
    hearts = [(x_meet + 40, G - 330, 26, 0.0), (x_meet + 120, G - 360, 20, 0.5), (x_meet - 60, G - 350, 18, 0.9),
              (3320, G - 330, 22, 0.2), (3560, G - 360, 18, 0.7), (3080, G - 340, 20, 1.1), (xb_end, G - 250, 18, 0.4),
              (3760, G - 380, 24, 1.3), (2960, G - 320, 16, 1.6)]
    for i, (hx, hy, r, dt) in enumerate(hearts):
        t0 = (t_hug3 + 0.4 + dt * 0.5) if i < 3 else (t_fam + dt)
        sc.add(f"heart{i}", doc(heart_markup(hx, hy, r)), z=13 + 0.01 * i, wc=0.4, seed=180 + i,
               motion=lambda t, t0=t0, hx=hx, hy=hy, i=i: Tf(
                   dy=-75 * max(0.0, t - t0), dx=14 * math.sin(2 * math.pi * (t - t0) / 1.8 + i),
                   sx=M.progress(t, t0, t0 + 0.3, "back"), sy=M.progress(t, t0, t0 + 0.3, "back"),
                   alpha=(1 - M.progress(t, t0 + 2.6, t0 + 3.6, "sine")) if t >= t0 else 0.0, px=hx, py=hy))
    tw_pts = [(3200, 560, 18), (3520, 520, 14), (3900, 540, 20), (4250, 520, 16), (4450, 600, 14), (2980, 600, 15)]
    sc.add("twinkles_god", [doc(twinkles_markup([(jx_c - 340, 520, 18), (jx_c + 140, 470, 15), (jx_c - 620, 580, 14),
                                                 (jx_c - 120, 420, 20), (jx_c + 260, 600, 13)], k)) for k in range(3)],
           z=13.5, wc=0, frame_at=lambda t: float(int(t * 6) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_god + 0.3, t_god + 0.7) * (1 - M.progress(t, t_lives + 0.8, t_lives + 1.4))))
    sc.add("twinkles_fam", [doc(twinkles_markup(tw_pts, k)) for k in range(3)], z=13.5, wc=0,
           frame_at=lambda t: float(int(t * 6) % 3), motion=lambda t: Tf(alpha=M.progress(t, t_fam, t_fam + 0.4)))

    # dust as they jump back; as Joseph runs
    sc.add("scare_dust", [doc("".join(puff_markup(bro_x(k)[0] + 30, bro_x(k)[1] - 8, 44 + 10 * j, 16 + 4 * j, seed=k + j)
                                      for k in range(10) if not FORM[k][1])) for j in range(3)], z=11.9, wc=0.6,
           frame_at=lambda t: float(min(2, max(0, int((t - t_scared - 0.25) / 0.12)))),
           motion=lambda t: Tf(alpha=0.7 * M.progress(t, t_scared + 0.2, t_scared + 0.3) * (1 - M.progress(t, t_scared + 0.7, t_scared + 1.1))))

    sc.add("h_front", hall_front_svg(), z=20, seed=180 + 50)
    sc.fx.append(FX.motes((2700, 300, 4700, 950), count=26, seed=31, alpha=110))
    sc.fx.append(FX.sparkles((3000, 380, 4600, 760), count=18, t0=t_fam, t1=T + 1, seed=23, size=(7, 15)))

    # ---- sound ----
    sc.sfx("crowd", 0.0, dur=t_send + 2.0, gain_db=-26, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_send + 0.8, dur=2.2, gain_db=-17, pan=0.5, fade_out=0.6)
    sc.sfx("cloth", t_reveal, gain_db=-10)
    sc.sfx("whoosh", t_reveal + 0.05, gain_db=-13)
    sc.sfx("pop", t_fly1, gain_db=-15)
    sc.sfx("whoosh", t_scared, gain_db=-11)
    sc.sfx("thud", t_scared + 0.3, gain_db=-9)
    sc.sfx("footsteps", t_walk, dur=t_walk_end - t_walk + 0.1, gain_db=-16)
    sc.sfx("chime", t_god, gain_db=-11)
    sc.sfx("sparkle", t_god + 0.4, gain_db=-15)
    sc.sfx("cloth", t_hug1 + 0.02, gain_db=-14)
    sc.sfx("cloth", t_hug2 + 0.02, gain_db=-15)
    sc.sfx("footsteps", t_jacob, dur=t_j_end - t_jacob, gain_db=-16, pan=0.4)
    sc.sfx("footsteps_run", t_run, dur=t_run_end - t_run + 0.05, gain_db=-15)
    sc.sfx("cloth", t_hug3, gain_db=-12)
    sc.sfx("chime", t_hug3 + 0.15, gain_db=-12)
    sc.sfx("cheer", t_fam, dur=T - t_fam, gain_db=-14, fade_in=0.3, fade_out=1.2)
    sc.sfx("sparkle", t_fam + 0.2, gain_db=-12)
    return sc
