"""Scene 6 — the caravan; Joseph is sold for twenty pieces of silver (Genesis 37:25-28).

The same picture-book cross-section page as the end of s05 (drawn by s05's page-3 functions at offset 0, plus the
far end of the road with the pyramids on the horizon), on a 3600 x 1188 stage. The first frame is s05's last frame.

  line 0  '这时候，来了一队骆驼。'  a caravan walks in from the left along the road: an Ishmaelite trader leading two
          loaded camels (pace walk cycles, planted feet). Levi sees them first and points; the other brothers turn.
          '那是去埃及做生意的商人。'  a little picture bubble over the trader shows where they are going: pyramids.
  line 1  '哥哥们把约瑟拉上来，'  Levi throws the rope down and pulls (pull); Joseph (hold_rope) comes up hand over hand
          and hops out beside the pit.  '用二十块银子把他卖了。'  Judah steps up to the trader, who holds out the silver:
          in a floating counting panel the coins count up two by two to twenty (a '20' badge pops); Joseph, sad, walks
          over behind the last camel.
  line 2  '约瑟被带到了很远很远的埃及。'  the caravan sets off to the right, Joseph walking sadly behind the camels; the
          camera glides ahead along the road; far away the little caravan comes out from behind a low hill and grows
          smaller and smaller toward the pyramids on the horizon, in warm late light.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import arcs_markup, cuts, dip, hop, nod, puff_markup, puff_motion, snap, step_walk
from art.style import P
from engine import motion as M
from engine import fx as FX
from engine.loader import load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import blink_expr, make_cam, when, with_blinks
from stories.joseph.scenes.s04_dream import (clouds_markup, dream_cloud, dust_markup, dust_motion, pop_in, pop_out,
                                             show, sprite, tuft_row)
from stories.joseph.scenes import s05_pit as A

SW, SH = 3440, 1188
INK = P["ink"]
SC = A.SC
GC, GS, PX, FLOOR = A.GC, A.GS, A.PX, A.FLOOR
CS = 0.8                  # caravan scale (on the road, a little further back)
RY = 526                  # road line (caravan anchors)
TX = 960                  # where the trader stops
CAM_A = TX - 301          # camel A (its lead rope ends in the trader's hand)
CAM_B = CAM_A - 330
TSTEP, TPER = 68.0, 0.375  # trader stride / period -> 181 px/s
SPEED = TSTEP / TPER
CPH = 113 * CS / 8 / SPEED  # camel walk phase period (planted feet)
JX_OUT = PX - 180         # Joseph after he is pulled out
JX_CAR = CAM_B - 150      # Joseph behind the last camel
JUDAH_X = PX + 520
JUDAH_TO = TX + 210


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


def f1(v):
    return f"{v:.1f}"


def s05_duration():
    try:
        return next(s["duration"] for s in load_timeline()["scenes"] if s["id"] == "s05_pit")
    except Exception:  # noqa: BLE001
        return 23.73


def mound_markup():
    """A low grassy hill on the meadow that the far road passes behind."""
    out = S.path("M2370,506 C2470,446 2760,440 2870,500 L2870,530 L2370,530 Z", "#a6c67a", sw=0)
    out += S.path("M2370,506 C2470,446 2760,440 2870,500", "none", sw=3.5)
    out += PR.bush(2540, 470, 0.32, variant=0) + PR.grass_tuft(2700, 474, 0.4, variant=2)
    return S.g(out, filter="wobble")


def pyramids_markup():
    return PR.pyramids(3235, 416, 0.2, n=3, haze=0.55, ground=False)


def bubble_markup(cx, cy):
    """A small picture bubble: pyramids and a palm (where the traders are going)."""
    inner = (f'<rect x="{cx - 200}" y="{cy - 120}" width="400" height="240" fill="#cfe6ea"/>'
             f'<rect x="{cx - 200}" y="{cy + 30}" width="400" height="100" fill="#ebc98f"/>'
             + PR.pyramids(cx + 10, cy + 40, 0.17, n=3, ground=False)
             + PR.palm_tree(cx - 120, cy + 70, 0.2) + PR.palm_tree(cx + 135, cy + 74, 0.17))
    return dream_cloud(cx, cy, 300, 190, S.g(inner, filter="wobble"), seed=9)


def coin_panel_markup(cx, cy, n, badge=False):
    """A floating counting panel: n silver coins in rows of ten, and a '20' badge."""
    out = (f'<rect x="{cx - 170}" y="{cy - 70}" width="340" height="140" rx="40" fill="#fbf6ea" stroke="{INK}" '
           f'stroke-width="5"/>')
    if n > 0:
        out += PR.coins(cx, cy + 48 if n > 10 else cy + 20, 1.0, n=n, kind="row")
    if badge:
        out += (f'<circle cx="{cx + 170}" cy="{cy - 66}" r="44" fill="#e8b63c" stroke="{INK}" stroke-width="5"/>'
                + S.text(cx + 170, cy - 50, "20", size=46, fill=INK))
    return S.g(out, filter="wobble-fine")


def far_caravan_markup(x, y, k):
    """The caravan far away (built at scale 0.3 around (x, y)), walk frame k of 4."""
    s = 0.3
    ph = k / 4
    out = ""
    jx = x - 640 * s
    out += C.joseph(jx, y, s, 1, pose=("walk_a", "walk_b")[k % 2], expr="sad", coat="torn")
    out += PR.camel(x - 420 * s, y, s, 1, pose="walk", phase=(ph + 0.5) % 1)
    out += PR.camel(x - 90 * s, y, s, 1, pose="walk", phase=ph)
    out += C.trader(x + 200 * s, y, s, 1, pose=("lead", "lead_b")[k % 2])
    return out


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    T5 = s05_duration()
    L0, L1, L2 = ctx.lines[:3]
    clamp, cam_path = make_cam(SW, SH)

    # ---------------- times
    t_in0 = 0.45
    n_in = 15
    t_in1 = snap(t_in0 + n_in * TPER)
    t_see = snap(when(ctx, "来了一队") - 0.1)
    t_turn = snap(t_see + 0.55)
    t_egypt = when(ctx, "去埃及做生意")
    t_rope = snap(when(ctx, "哥哥们把约瑟") - 0.05)
    t_grab = snap(t_rope + 0.35)
    t_up0 = t_grab + 0.2
    t_top = snap(when(ctx, "拉上来") + 0.75)
    t_out = snap(t_top + 0.35)               # standing beside the pit
    t_silver = snap(when(ctx, "二十块银子") - 0.1)
    t_count0 = t_silver + 0.35
    t_badge = snap(t_count0 + 1.25)
    t_sold = when(ctx, "把他卖了")
    t_jwalk = snap(t_out + 0.7)
    t_go = snap(L1.end + 0.25)
    t_far = when(ctx, "很远很远")

    # ---------------- camera
    C0 = Cam(1000, 530, 1800)                # = s05's last frame
    C1 = Cam(780, 520, 1560)
    C2 = Cam(800, 610, 1500)
    C3 = Cam(820, 566, 1560)
    C4 = Cam(2600, 470, 1480)
    C5 = Cam(2770, 452, 1300)
    sc.camera = cam_path([(0, C0), (t_see - 0.3, C0), (t_see + 1.9, C1), (t_rope - 0.2, C1), (t_rope + 0.9, C2),
                          (t_silver - 0.3, C2), (t_silver + 0.8, C3), (t_go + 0.2, C3), (t_go + 3.5, C4), (T, C5)])

    # ---------------- background (identical to s05 page 3 at offset 0)
    sc.add("sky", doc(A.p3_sky_markup(0, SW)), z=0, wc=0.5)
    sc.add("pyramids", doc(pyramids_markup()), z=1.05, wc=0.5)
    sc.add("land", doc(A.p3_land_markup(0) + A.p3_pit_markup(0) + A.p3_props_markup(0)), z=1)
    sc.add("clouds", doc(clouds_markup(((300, 150, 300, 70, 7), (1200, 110, 260, 60, 8), (1900, 210, 240, 56, 9),
                                        (2700, 140, 280, 64, 10), (3150, 210, 230, 54, 11)))), z=0.06, wc=0.6,
           motion=lambda t: Tf(dx=-7 * (t + T5)))
    sc.add("mound", doc(mound_markup()), z=1.3)

    # ---------------- far caravan (behind the mound, toward the pyramids)
    t_far0 = snap(t_go + 2.3)
    fx0, fy0 = 2600, 474
    fx1, fy1 = 3110, 430
    sc.add("far_caravan", [doc(far_caravan_markup(fx0, fy0, k)) for k in range(4)], z=1.2, wc=0.6,
           frame_at=lambda t: float(int(t / 0.17) % 4),
           motion=lambda t: (lambda u: Tf(dx=(fx1 - fx0) * u, dy=(fy1 - fy0) * u, sx=1 - 0.55 * u, sy=1 - 0.55 * u,
                                          px=fx0, py=fy0, alpha=M.progress(t, t_far0, t_far0 + 0.7, "sine")))(
               M.progress(t, t_far0, T + 0.6, "linear")))

    # ---------------- the brothers
    right = [b for b in A.P3_BROS if b[1] > PX and b[0] != 3]
    rcx = sum(b[1] for b in right) / len(right)

    def bro(v, x, f, pose, expr):
        return A.p3_bro(0, v, x, f, pose, expr)
    rfr = ["".join(bro(v, x, -f, "cross_arms", "neutral") for v, x, f in right),      # s05's last state
           "".join(bro(v, x, f, "stand", "surprised") for v, x, f in right),
           "".join(bro(v, x, f, "stand", "neutral") for v, x, f in right),
           "".join(bro(v, x, f, "stand", blink_expr("neutral")) for v, x, f in right),
           "".join(bro(v, x, f, "cross_arms", "neutral") for v, x, f in right)]
    rb = with_blinks([(0, 0), (t_turn + 0.1, 1), (snap(t_egypt), 2), (snap(t_go + 0.4), 4)], {2: 3},
                     [t_rope + 1.0, t_sold + 0.5])
    sprite(sc, "bros_right", 2.4, [doc(f) for f in rfr], (rcx, GS), base=rb, docf=doc,
           bumps=[dip(t_turn + 0.1, SC, (rcx, GS), 6), dip(snap(t_egypt), SC, (rcx, GS), 4),
                  dip(snap(t_go + 0.4), SC, (rcx, GS), 4)],
           breathe=(0.008, 2.9, 0.5 + T5 / 2.9))
    # Judah (v3): turns, then steps up to the trader and takes the silver
    jv, jx0, jf = [b for b in A.P3_BROS if b[0] == 3][0]
    n_j = 2
    j_step = (JUDAH_TO - jx0) / n_j

    def jud(pose, f, expr):
        return A.p3_bro(0, jv, JUDAH_TO, f, pose, expr)
    jfr = [jud("walk_a", -1, "neutral"), jud("walk_b", -1, "neutral"), jud("cross_arms", 1, "neutral"),
           jud("stand", -1, "surprised"), jud("stand", -1, "neutral"), jud("talk", -1, "sly"),
           jud("stand", -1, blink_expr("neutral")), jud("cross_arms", -1, "neutral")]
    t_jw = snap(t_silver - n_j * 0.3 - 0.05)
    jb = with_blinks([(0, 2), (t_turn, 3), (snap(t_egypt + 0.1), 4), (snap(t_silver + 0.1), 5), (snap(t_go + 0.4), 7)],
                     {4: 6}, [t_rope + 1.3])
    sprite(sc, "judah", 2.45, [doc(f) for f in jfr], (JUDAH_TO, GS), base=jb, walks=[(t_jw, n_j, j_step, 0)],
           start_off=jx0 - JUDAH_TO, period=0.3, docf=doc,
           bumps=[dip(t_turn, SC, (JUDAH_TO, GS), 6), dip(snap(t_silver + 0.1), SC, (JUDAH_TO, GS), 5),
                  nod(t_sold + 0.2, (JUDAH_TO, GS), -3, 0.5), dip(snap(t_go + 0.4), SC, (JUDAH_TO, GS), 4)],
           breathe=(0.008, 2.9, 0.5 + T5 / 2.9))
    # Levi: sees the caravan and points; pulls Joseph up
    lv, lx, lf = [b for b in A.P3_BROS if b[0] == A.ROPER][0]
    lfr = [A.p3_bro(0, lv, lx, -lf, "stand", "neutral"), A.p3_bro(0, lv, lx, -lf, "point", "surprised"),
           A.p3_bro(0, lv, lx, lf, "pull", "determined"), A.p3_bro(0, lv, lx, lf, "stand", "neutral"),
           A.p3_bro(0, lv, lx, -lf, "stand", blink_expr("neutral"))]
    t_lv_done = snap(t_out + 0.3)
    lb = with_blinks([(0, 0), (t_see, 1), (snap(t_see + 1.6), 0), (t_rope, 2), (t_lv_done, 3)], {0: 4},
                     [t_in1 + 0.2])
    pulls = [hop(t_up0 + i * (t_top - t_up0) / 4, [(0, {"dx": 0}), (0.14, {"dx": -14}), (0.3, {"dx": 0})], (lx, GS))
             for i in range(4)]
    sprite(sc, "levi", 2.45, [doc(f) for f in lfr], (lx, GS), base=lb, docf=doc,
           bumps=[dip(t_see, SC, (lx, GS), 6), dip(snap(t_see + 1.6), SC, (lx, GS), 4), dip(t_rope, SC, (lx, GS), 6),
                  dip(t_lv_done, SC, (lx, GS), 5)] + pulls,
           breathe=(0.01, 2.7, 0.1 + T5 / 2.7))
    sh = C.body_points(C.brothers, lx, GS, SC, -lf, variant=lv, pose="point")["head"]
    sc.add("levi_arcs", [doc(arcs_markup(sh[0] - 56, sh[1] + 18, -1, k, 1.1)) for k in (1, 2, 3)], z=2.46, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_see + 0.1, t_see + 1.5))

    # ---------------- the rope and Joseph coming up
    fists = C.hand_positions(C.brothers, lx, GS, SC, lf, variant=lv, pose="pull")
    rx = PX + A.ROPE_X_OFF
    rim = (PX - 118, GC - 6)
    rope_top = (f'M{f1(fists[0][0])},{f1(fists[0][1])} L{f1(fists[1][0])},{f1(fists[1][1])} '
                f'Q{f1(rim[0] - 10)},{f1(rim[1] - 40)} {f1(rim[0])},{f1(rim[1])} Q{f1(rx - 20)},{f1(GC - 12)} '
                f'{f1(rx)},{f1(GC + 8)}')

    def rope_css(d, w):
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 5}" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="{P["wood_light"]}" stroke-width="{w}" stroke-linecap="round"/>')
    t_rope_gone = t_out + 0.05
    sc.add("rope_top", doc(S.g(rope_css(rope_top, 6), filter="wobble-fine")), z=2.5, motion=show(t_rope, t_rope_gone))
    PJ = A.joseph_pit_x(0)
    JF = A.JF
    hand_dy = C.hand_positions(C.joseph, 0, 0, SC, JF, pose="hold_rope", coat="torn")[0][1]
    y_top = GC + 150 - FLOOR                 # dy when his hands reach the rim

    def up_dy(t):
        if t < t_up0:
            return 0.0
        n = 4
        seg = (t_top - t_up0) / n
        k = min(n, max(0.0, (t - t_up0) / seg))
        i = int(k)
        prog = (i + (M.ease("inout")(k - i) if i < n else 0)) / n
        return y_top * prog

    def hop_m(t):
        """From the rim position, a hop up and over to the surface beside the pit."""
        if t < t_top:
            return 0.0, up_dy(t)
        u = M.progress(t, t_top, t_out, "inout")
        dx = (JX_OUT - PJ) * u
        dy = y_top + ((GS - FLOOR) - y_top) * u - 60 * math.sin(math.pi * u)
        return dx, dy
    rope_down = f"M{f1(rx)},{f1(GC + 4)} L{f1(rx + 3)},{f1(FLOOR - 20)}"
    rope_len = FLOOR - 20 - GC
    sc.add("rope_down", doc(S.g(rope_css(rope_down, 6), filter="wobble-fine")), z=1.58,
           reveal=lambda t: {"mode": "down", "soft": 6,
                             "frac": max(0.0, min(1.0, (FLOOR + hand_dy + up_dy(t) - GC + 20) / rope_len)) *
                             M.progress(t, t_rope, t_rope + 0.3, "out")},
           motion=show(t_rope, t_top + 0.05))

    def jpit(pose, expr):
        return C.joseph(PJ, FLOOR, SC, JF, pose=pose, expr=expr, coat="torn")
    jpfr = [jpit("sad", "sad"), jpit("hold_rope", "worried"), jpit("sad", blink_expr("sad"))]
    sc.add("jpit", [doc(f) for f in jpfr], z=1.6,
           frame_at=cuts(with_blinks([(0, 0), (t_grab, 1)], {0: 2}, [t_see + 1.2, t_egypt + 0.8])),
           motion=M.combine(lambda t: Tf(dx=hop_m(t)[0], dy=hop_m(t)[1]), dip(t_grab, SC, (PJ, FLOOR), 6),
                            M.breathe(0.012, 2.5, pivot=(PJ, FLOOR), phase=T5 / 2.5), show(0, t_out)))
    sc.add("jpit_shadow", doc(C.ground_shadow(PJ, FLOOR - 4, SC, 120)), z=1.55, wc=0,
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_up0, t_up0 + 0.4, "sine")))
    sc.fx.append(FX.motes((PX - 120, GC + 40, PX + 120, FLOOR - 30), count=14, t0=-2, t1=t_top + 0.5,
                          color=(240, 220, 180), size=(2.5, 5), seed=61, alpha=140))
    sc.add("out_puff", doc(puff_markup(JX_OUT, GS - 140, 100, 160, seed=8, k=0.7)), z=2.9, wc=0,
           motion=puff_motion(t_out, (JX_OUT, GS - 140)))
    # Joseph on the surface: sad; walks over behind the last camel; follows the caravan
    n_jw = 6
    jw_step = (JX_CAR - JX_OUT) / n_jw
    JPER = 0.3
    t_jw_end = snap(t_jwalk + n_jw * JPER)
    t_jfollow = snap(t_go + 0.55)
    jstep_f = 77.0
    jper_f = jstep_f / SPEED
    n_jf = int((T - t_jfollow) / jper_f) + 1

    def js(x, pose, f, expr="sad"):
        return C.ground_shadow(x, GS, SC, 110) + C.joseph(x, GS, SC, f, pose=pose, expr=expr, coat="torn")
    X0 = JX_CAR
    jsfr = [js(X0, "walk_a", -1), js(X0, "walk_b", -1), js(X0, "walk_a", 1), js(X0, "walk_b", 1), js(X0, "sad", -1),
            js(X0, "sad", 1), js(X0, "sad", 1, blink_expr("sad"))]
    jsb = with_blinks([(0, 4), (t_jw_end, 5)], {5: 6}, [t_badge + 0.5])
    sprite(sc, "joseph", 2.7, [doc(f) for f in jsfr], (X0, GS), base=jsb,
           walks=[(t_jwalk, n_jw, jw_step, 0), (t_jfollow, n_jf, jstep_f, 2)], start_off=JX_OUT - X0, period=JPER,
           docf=doc, bumps=[dip(t_jw_end, SC, (X0, GS), 5)], breathe=(0.012, 2.4, 0.0), extra=show(t_out))
    # the follow walk uses its own (slower) period: patch the second walk
    jl = sc.layers[-1]
    w1 = step_walk(t_jwalk, n_jw, jw_step, JPER, SC)
    w2 = step_walk(t_jfollow, n_jf, jstep_f, jper_f, SC)
    fb = cuts(jsb)

    def jfa(t):
        v = w1[0](t)
        if v is not None:
            return v
        v = w2[0](t)
        if v is not None:
            return v + 2
        return fb(t)
    jl.frame_at = jfa
    jl.motion = M.combine(M.with_pivot(lambda t: Tf(dx=JX_OUT - X0 + w1[1](t) + w2[1](t), dy=w1[2](t) + w2[2](t)),
                                       (X0, GS)),
                          dip(t_jw_end, SC, (X0, GS), 5), M.breathe(0.012, 2.4, pivot=(X0, GS)), show(t_out))

    # ---------------- the caravan (near)
    t_dep = t_go
    n_dep = int((T - t_dep) / TPER) + 1

    def car_dx(t):
        """Caravan x offset from the stop: walking in, standing, walking off (linear = planted pace for camels)."""
        if t < t_in1:
            return -n_in * TSTEP + SPEED * max(0.0, t - t_in0)
        if t < t_dep:
            return 0.0
        return SPEED * (t - t_dep)

    def camel_phase(t):
        if t < t_in1:
            return (max(0.0, t - t_in0) / CPH) % 8
        if t < t_dep:
            return None
        return ((t - t_dep) / CPH) % 8
    for name, cx, z, off in (("camel_b", CAM_B, 2.1, 4), ("camel_a", CAM_A, 2.15, 0)):
        fr = [doc(PR.camel(cx, RY, CS, 1, pose="walk", phase=k / 8)) for k in range(8)]
        fr.append(doc(PR.camel(cx, RY, CS, 1, pose="stand")))
        fr.append(doc(PR.camel(cx, RY, CS, 1, pose="stand", eyes="closed")))

        def fa(t, off=off):
            ph = camel_phase(t)
            if ph is None:
                tt = t - t_in1
                return 9.0 if (tt % 3.1) > 2.95 else 8.0
            return float((int(ph) + off) % 8)
        sc.add(name, fr, z=z, frame_at=fa,
               motion=lambda t: Tf(dx=car_dx(t), dy=(-3 * CS * abs(math.sin(math.pi * (t - t_in1) / 3.0))
                                                     if t_in1 <= t < t_dep else 0.0)))
        sc.add(name + "_shadow", doc(C.ground_shadow(cx, RY + 2, CS, 300, 0.18)), z=z - 0.01, wc=0,
               motion=lambda t: Tf(dx=car_dx(t)))
    # the trader
    tw_in = step_walk(t_in0, n_in, TSTEP, TPER, CS)
    tw_out = step_walk(t_dep, n_dep, TSTEP, TPER, CS)

    def trd(pose, expr=None):
        return C.ground_shadow(TX, RY, CS, 110) + C.trader(TX, RY, CS, 1, variant=0, pose=pose, expr=expr)
    tfr = [trd("lead"), trd("lead_b"), trd("stand", "happy"), trd("talk", "happy"), trd("give", "happy"),
           trd("count", "happy"), trd("stand", blink_expr("happy"))]
    t_tstand = t_in1
    tb = with_blinks([(0, 2), (snap(t_egypt - 0.1), 3), (snap(t_silver), 4), (t_count0 + 1.4, 3), (snap(t_sold + 0.6), 2)],
                     {2: 6}, [t_rope + 1.0, t_top])
    tfb = cuts(tb)

    def tfa(t):
        for w in (tw_in, tw_out):
            v = w[0](t)
            if v is not None:
                return v
        return tfb(t)
    sc.add("trader", [doc(f) for f in tfr], z=2.2, frame_at=tfa,
           motion=M.combine(M.with_pivot(lambda t: Tf(dx=-n_in * TSTEP + tw_in[1](t) + tw_out[1](t),
                                                      dy=tw_in[2](t) + tw_out[2](t)), (TX, RY)),
                            dip(snap(t_tstand), CS, (TX, RY), 5), dip(snap(t_egypt - 0.1), CS, (TX, RY), 4),
                            dip(snap(t_silver), CS, (TX, RY), 5), nod(t_sold + 0.2, (TX, RY), 3, 0.5),
                            M.breathe(0.01, 2.6, pivot=(TX, RY))))
    # the picture bubble over the trader (pyramids: going to Egypt)
    th = C.body_points(C.trader, TX, RY, CS, 1, pose="talk")["head_top"]
    bx, by = th[0] + 230, th[1] - 30
    sc.add("egypt_bubble", doc(bubble_markup(bx, by)), z=3.0, wc=0.4,
           motion=M.combine(pop_in(t_egypt + 0.15, (bx - 60, by + 90)), pop_out(L0.end + 0.45, (bx, by)),
                            M.bob(4, 2.2)))
    for i, (dx, dy, r) in enumerate(((-150, 70, 13), (-185, 95, 9))):
        sc.add(f"eb_dot{i}", doc(f'<circle cx="{bx + dx}" cy="{by + dy}" r="{r}" fill="#fbf6ea" stroke="{INK}" '
                                 f'stroke-width="3.4"/>'), z=3.0, wc=0,
               motion=M.combine(pop_in(t_egypt + 0.05 - 0.05 * i, (bx + dx, by + dy)),
                                pop_out(L0.end + 0.35, (bx + dx, by + dy))))
    # counting the silver
    px_, py_ = (TX + JUDAH_TO) / 2 - 10, 250
    counts = list(range(2, 21, 2))
    cfr = [doc(coin_panel_markup(px_, py_, 0))] + [doc(coin_panel_markup(px_, py_, n)) for n in counts]
    cfr.append(doc(coin_panel_markup(px_, py_, 20, badge=True)))
    cent = [(0, 0)] + [(snap(t_count0 + 0.12 * (i + 1)), i + 1) for i in range(len(counts))] + [(t_badge, len(cfr) - 1)]
    t_cend = snap(t_go + 0.1)
    sc.add("coins", cfr, z=3.05, wc=0.3, frame_at=cuts(cent),
           motion=M.combine(pop_in(t_silver + 0.1, (px_, py_ + 70)), pop_out(t_cend, (px_, py_)),
                            hop(t_badge, [(0, {"s": 1}), (0.12, {"s": 1.08}), (0.3, {"s": 1})], (px_ + 170, py_ - 66))))
    sc.add("coin_sparkle", doc(S.g(f'<path d="{S.rays(px_ + 170, py_ - 66, 54, 84, 10, 9)}" fill="#f2c14e" '
                                   f'opacity="0.8"/>', filter="wobble-fine")), z=3.04, wc=0,
           motion=M.combine(lambda t: Tf(alpha=M.progress(t, t_badge, t_badge + 0.2) * (1 - M.progress(t, t_badge + 0.6, t_badge + 1.1))),
                            M.breathe(0.08, 0.6, pivot=(px_ + 170, py_ - 66))))
    # the coat stays on the grass
    sc.add("coat", doc(PR.coat_of_colours(PX + 400, GS + 2, 0.5, 1, state="lying")), z=2.3)

    # ---------------- foreground tufts (as s05, same phase)
    FG3 = [(120, GC + 2, 0.7, 0), (1300, GC + 2, 0.6, 2), (1900, GC + 2, 0.7, 0), (2900, GC + 2, 0.7, 2),
           (3400, GC + 2, 0.6, 0)]
    sc.add("fg", [doc(tuft_row(FG3, k * 2.1 + 1)) for k in range(3)], z=3.5,
           frame_at=lambda t: float(int((t + T5) * 2.2) % 3))

    # ---------------- late warm light for the long journey
    warm = lambda t: M.progress(t, t_go, t_go + 3.5, "sine")  # noqa: E731
    sc.fx.append(FX.tint((255, 196, 140), lambda t: 0.2 * warm(t), mode="multiply"))
    sc.fx.append(FX.vignette(lambda t: 0.35 * warm(t)))

    # ---------------- sound
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_in0, dur=t_in1 - t_in0, gain_db=-17, fade_in=0.6, pan=-0.4)
    sc.sfx("whoosh", t_rope, gain_db=-14)
    sc.sfx("cloth", t_out, gain_db=-14)
    for i in range(0, len(counts), 2):
        sc.sfx("coins", t_count0 + 0.12 * (i + 1), gain_db=-13 + (i // 4))
    sc.sfx("pop", t_badge, gain_db=-11)
    sc.sfx("sparkle", t_badge + 0.05, gain_db=-17)
    sc.sfx("footsteps", t_dep, dur=T - t_dep, gain_db=-17, fade_out=1.0, pan=0.3)
    sc.sfx("wind_hot", t_far, dur=T - t_far, gain_db=-22, fade_in=1.0, fade_out=1.0)
    return sc
