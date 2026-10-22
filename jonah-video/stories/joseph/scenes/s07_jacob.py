"""Scene 7 — the brothers bring the coat home; Jacob weeps (Genesis 37:31-35).

One 2600 x 1188 page at Jacob's tent (the same family tent as s04 / s05), warm late afternoon.

  line 0  '哥哥们把彩衣弄得又破又脏，'  on the right, Judah holds up Joseph's coat; '又破又脏' - a puff of dust and the
          coat is torn and dirty (no blood).  '拿回家给爸爸看。'  five brothers walk home to old Jacob (planted feet, the
          camera glides with them) and Judah holds the coat up to show him; Jacob is startled.
  line 1  '雅各以为约瑟被野兽吃掉了，'  Jacob bows his head; a small thought bubble rises: a soft, faded wild-animal
          silhouette walking away and a tiny torn coat (gentle, not frightening).  Jacob takes the coat and sinks down
          holding it, crying (jacob 'cry'); the brothers look down, ashamed.
          '伤心得哭了很久很久。'  the brothers quietly walk away; the camera comes close to Jacob, tears falling; the sun
          and the moon wheel over the tent - day, night, day, night - while a row of little suns and moons fills up
          above him (many days). It ends in a calm, soft evening.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import cuts, dip, hop, nod, puff_markup, puff_motion, snap, step_walk, tear_markup
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import blink_expr, make_cam, sheep_layer, when, with_blinks
from stories.joseph.scenes.s04_dream import (clouds_markup, dream_cloud, family_tent, far_hills_markup, meadow_markup,
                                             moon_markup, pop_in, pop_out, show, sky_svg, sprite, stars_markup,
                                             sun_markup, tuft_row)

SW, SH = 2600, 1188
INK = P["ink"]
GY = 1030
SC = 0.9
WALK_P = 0.27
TENT_X = 200
JX = 870                  # Jacob
HOLD_X = 1080             # Judah (holding the coat) when he stops in front of Jacob
BROS = [(0, 1250), (1, 1410), (2, 1570), (6, 1730)]   # the others, at their stops
N_IN = 8
STEP = 76.0
WHEEL = (950, 1150)       # centre of the sun / moon wheel
WHEEL_R = 560


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


def f1(v):
    return f"{v:.1f}"


def background_svg():
    out = S.g(far_hills_markup(w=SW, base=770, seed=11, tents=False), filter="wobble")
    out += S.g(S.path(S.hill(-80, SW + 80, 905, 120, seed=27, bumps=3), "#a3c47c", sw=4), filter="wobble")
    for x, y, s, f, v in ((1500, 905, 0.33, 1, 0), (1570, 900, 0.31, -1, 2), (2250, 902, 0.33, 1, 3)):
        out += PR.sheep(x, y, s, f, variant=v, pose="graze")
    out += S.g(meadow_markup(-80, SW + 80, 905, SH + 20, seed=17), filter="wobble")
    out += PR.olive_tree(2420, 985, 0.72, seed=4) + PR.bush(1900, 1000, 0.5, variant=1)
    out += family_tent(TENT_X, GY, 0.85, lamp=False)
    out += PR.jar(TENT_X + 400, GY - 4, 0.65) + PR.sack(TENT_X + 345, GY - 2, 0.55)
    return doc(out)


def wheel_svg():
    """Sun (top) and moon (bottom) on a big wheel; rotating the layer around WHEEL moves them across the sky."""
    cx, cy = WHEEL
    return doc(sun_markup(cx, cy - WHEEL_R, 48) + moon_markup(cx, cy + WHEEL_R, 38))


def thought_inner(cx, cy):
    """Jacob's sad thought: a hazy hill, a soft faded wild-animal shape walking away and a tiny torn coat."""
    sil = (f'<filter id="s7sil" x="-10%" y="-10%" width="120%" height="120%">'
           f'<feFlood flood-color="#a59a8c" result="c"/><feComposite in="c" in2="SourceAlpha" operator="in"/></filter>')
    out = f"<defs>{sil}</defs>"
    out += f'<rect x="{cx - 260}" y="{cy - 160}" width="520" height="320" fill="#e9e4dc"/>'
    out += S.path(S.hill(cx - 260, cx + 260, cy + 50, 40, seed=3, bottom=cy + 170, bumps=2), "#d6d2b8", sw=2.5)
    out += f'<g filter="url(#s7sil)" opacity="0.75">{PR.lion(cx + 70, cy + 52, 0.32, 1, pose="stand")}</g>'
    out += PR.coat_of_colours(cx - 95, cy + 58, 0.28, 1, state="lying", torn=True, dirty=True)
    return out


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[:2]
    clamp, cam_path = make_cam(SW, SH)

    t_tear = snap(when(ctx, "又破又脏"))
    t_walk = snap(t_tear + 0.55)
    t_stop = snap(t_walk + N_IN * WALK_P)
    t_show = snap(max(t_stop + 0.05, when(ctx, "给爸爸看") - 0.05))
    t_jsurp = snap(t_stop - 0.35)
    t_jsad = snap(L1.start + 0.1)
    t_beast = when(ctx, "野兽")
    t_take = snap(L1.chunks[0].end - 0.45)
    t_cry = when(ctx, "伤心得哭了")
    t_leave = snap(t_cry + 0.2)
    t_days0 = t_cry + 0.35
    t_days1 = min(T - 0.6, L1.end + 0.9)
    DAYS = 1.69                                   # wheel turns (days) during '很久很久'

    # ---------------- camera
    C0 = Cam(1780, 706, 1400)
    C1 = Cam(1260, 706, 1400)
    C2 = Cam(1080, 720, 1300)
    C3 = Cam(950, 790, 1060)
    sc.camera = cam_path([(0, C0), (t_walk - 0.1, C0), (t_stop + 0.3, C1), (t_jsad, C1), (t_take + 0.6, C2),
                          (t_cry, C2), (t_cry + 2.2, C3), (T, C3)])

    # ---------------- day / night
    def phase(t):
        return DAYS * M.progress(t, t_days0, t_days1, "sine")

    def height(t):                                # sun height -1..1 (1 = noon); starts in the afternoon
        a = 2 * math.pi * (phase(t) + 0.06)
        return math.cos(a)

    def night(t):
        return min(1.0, max(0.0, (0.25 - height(t)) / 0.5))

    def dusk(t):
        h = height(t)
        return max(0.0, 1 - abs(h - 0.05) / 0.35) * (1 - night(t) * 0.5)
    sc.add("sky", sky_svg("s7sky", [(0, "#8ec6df"), (0.55, "#c7e3e6"), (1, "#f6e6c8")], SW, SH), z=0, wc=0.5)
    sc.add("sky_dusk", sky_svg("s7dusk", [(0, "#b9a6d3"), (0.4, "#f1b8b0"), (0.75, "#f8c992"), (1, "#fbe0b0")], SW, SH),
           z=0.05, wc=0.4, motion=lambda t: Tf(alpha=dusk(t) * 0.9 * M.progress(t, t_days0 - 0.2, t_days0 + 0.3)))
    sc.add("sky_night", sky_svg("s7night", [(0, "#16203a"), (0.6, "#2b3a62"), (1, "#4a5a84")], SW, SH), z=0.1, wc=0.4,
           motion=lambda t: Tf(alpha=night(t)))
    sc.add("stars", doc(stars_markup(5, 0, SW, 10, 760, 80)), z=0.15, wc=0, motion=lambda t: Tf(alpha=night(t) ** 1.5))
    sc.add("wheel", wheel_svg(), z=0.17, wc=0.3,
           motion=lambda t: Tf(rot=360 * (phase(t) + 0.06), px=WHEEL[0], py=WHEEL[1]))
    sc.add("clouds", doc(clouds_markup(((400, 210, 320, 74, 1), (1300, 150, 280, 64, 2), (2150, 240, 300, 70, 3),
                                        (900, 330, 200, 46, 4)))), z=0.2, wc=0.6,
           motion=lambda t: Tf(dx=-8 * t - 120 * phase(t), alpha=1 - 0.6 * night(t)))
    sc.add("bg", background_svg(), z=1)

    # ---------------- Jacob
    def jac(pose, expr=None):
        return C.ground_shadow(JX, GY, SC, 120) + C.jacob(JX, GY, SC, 1, pose=pose, expr=expr)
    jfr = [jac("stand", "kind"), jac("stand", "surprised"), jac("sad", "sad"), jac("cry", "crying"),
           jac("stand", blink_expr("kind")), jac("sad", blink_expr("sad"))]
    jb = with_blinks([(0, 0), (t_jsurp, 1), (t_jsad, 2), (t_take, 3)], {0: 4, 2: 5}, [1.4, 3.6, t_beast + 0.6])
    sprite(sc, "jacob", 2.0, jfr, (JX, GY), base=jb, docf=doc,
           bumps=[dip(t_jsurp, SC, (JX, GY), 4), hop(t_jsurp, [(0, {"dy": 0}), (0.1, {"dy": -12}), (0.3, {"dy": 0})],
                                                       (JX, GY)),
                  dip(t_jsad, SC, (JX, GY), 6), dip(t_take, SC, (JX, GY), 10),
                  # sobbing: little shoulder heaves while he cries
                  lambda t: Tf(sy=1 - 0.012 * max(0.0, math.sin(t * 7.0)) * M.progress(t, t_take + 0.3, t_take + 0.8),
                               px=JX, py=GY)],
           breathe=(0.012, 2.8, 0.1))
    sc.add("take_puff", doc(puff_markup(JX + 110, GY - 150, 120, 110, seed=3, k=0.6)), z=2.9, wc=0,
           motion=puff_motion(t_take, (JX + 110, GY - 150)))
    # falling tears
    head = C.body_points(C.jacob, JX, GY, SC, 1, pose="cry")["head"]
    for i in range(3):
        tx, ty = head[0] + (14 if i % 2 else -8) * SC, head[1] + 28 * SC
        period = 1.1 + 0.2 * i

        def tear_m(t, tx=tx, ty=ty, period=period, ph=i * 0.37):
            if t < t_take + 0.4:
                return Tf(alpha=0.0)
            u = ((t - t_take) / period + ph) % 1.0
            return Tf(dy=70 * u * u, alpha=min(1.0, u * 6) * (1 - u), px=tx, py=ty)
        sc.add(f"tear{i}", doc(tear_markup(tx, ty, 1.6)), z=2.95, wc=0, motion=tear_m)

    # ---------------- Judah with the coat
    hv = 3
    hx_near = C.hand_positions(C.brothers, 0, 0, SC, -1, variant=hv, pose="walk_a")[1]
    ht_near = C.hand_positions(C.brothers, 0, 0, SC, -1, variant=hv, pose="talk")[1]
    start_off = N_IN * STEP

    def hold(pose, expr):
        return C.ground_shadow(HOLD_X, GY, SC, 120) + C.brothers(HOLD_X, GY, SC, -1, variant=hv, pose=pose, expr=expr,
                                                                 staff=False)
    hfr = [hold("walk_a", "neutral"), hold("walk_b", "neutral"), hold("talk", "neutral"), hold("sad", "ashamed"),
           hold("walk_a", "ashamed"), hold("walk_b", "ashamed"), hold("talk", blink_expr("neutral"))]
    hfr2 = [hold("walk_a", "ashamed"), hold("walk_b", "ashamed")]
    n_out = 6
    hb = with_blinks([(0, 2), (snap(t_take + 0.05), 3)], {2: 6}, [0.6, t_show + 0.8])
    hdx = sprite(sc, "judah", 2.5, hfr, (HOLD_X, GY), base=hb, docf=doc,
                 walks=[(t_walk, N_IN, -STEP, 0), (t_leave, n_out, 0.0, 4)], start_off=start_off, period=WALK_P,
                 bumps=[dip(snap(t_take + 0.05), SC, (HOLD_X, GY), 6), dip(t_stop, SC, (HOLD_X, GY), 4),
                        nod(t_show + 0.3, (HOLD_X, GY), -3, 0.5)],
                 breathe=(0.009, 2.7, 0.3))
    # the coat in his near hand (clean -> torn and dirty); lifted to show it; vanishes into Jacob's arms
    cpos = (HOLD_X + ht_near[0], GY + ht_near[1] + 4)
    cfr = [doc(PR.coat_of_colours(cpos[0], cpos[1], 0.46, 1, state="held")),
           doc(PR.coat_of_colours(cpos[0], cpos[1], 0.46, 1, state="held", torn=True, dirty=True))]
    walk_dy = hx_near[1] - ht_near[1]

    def coat_m(t):
        walking = t_walk - 0.05 <= t < t_stop + 0.05
        lift = -46 * M.progress(t, t_show, t_show + 0.35, "back")
        sway = 4 * math.sin(t * 3.1)
        return Tf(dx=hdx(t) + (hx_near[0] - ht_near[0] if walking else 0), dy=(walk_dy if walking else 0) + lift,
                  rot=sway, px=cpos[0], py=cpos[1], alpha=1.0 if t < t_take else 0.0)
    sc.add("coat", cfr, z=2.55, frame_at=cuts([(0, 0), (t_tear, 1)]), motion=coat_m)
    sc.add("tear_puff", doc(puff_markup(cpos[0], cpos[1] + 60, 90, 80, seed=4, k=0.55)), z=2.6, wc=0,
           motion=M.combine(puff_motion(t_tear, (cpos[0], cpos[1] + 60)), M.still(Tf(dx=start_off))))
    # the other brothers walk home behind him, then hang their heads and walk away
    for i, (v, x) in enumerate(BROS):
        def bro(pose, f, expr, v=v, x=x):
            return C.ground_shadow(x, GY, SC, 120) + C.brothers(x, GY, SC, f, variant=v, pose=pose, expr=expr,
                                                                staff=False)
        fr = [bro("walk_a", -1, "neutral"), bro("walk_b", -1, "neutral"), bro("stand", -1, "neutral"),
              bro("sad", -1, "ashamed"), bro("walk_a", 1, "ashamed"), bro("walk_b", 1, "ashamed"),
              bro("stand", -1, blink_expr("neutral"))]
        off = 0.06 * (i + 1)
        tw = snap(t_walk + off)
        ts = snap(t_take + 0.12 + 0.07 * i)
        tl = snap(t_leave + 0.15 + 0.1 * i)
        b = with_blinks([(0, 2), (ts, 3)], {2: 6}, [1.0 + 0.4 * i, t_show + 0.5 + 0.2 * i])
        sprite(sc, f"bro{i}", 2.4 - 0.01 * i, fr, (x, GY), base=b, docf=doc,
               walks=[(tw, N_IN, -STEP, 0), (tl, 7, 95.0, 4)], start_off=start_off, period=WALK_P,
               bumps=[dip(ts, SC, (x, GY), 5)], breathe=(0.009, 2.8, 0.2 * i))
    # Judah walks away too (patch his walk-out step: the sprite above used 0 step for the second walk)
    jl = [l for l in sc.layers if l.name == "judah"][0]
    w1 = step_walk(t_walk, N_IN, -STEP, WALK_P, SC)
    w2 = step_walk(t_leave + 0.05, n_out + 2, 95.0, WALK_P, SC)
    fb = cuts(hb)

    def jfa(t):
        v = w1[0](t)
        if v is not None:
            return v
        v = w2[0](t)
        if v is not None:
            return v + 4
        return fb(t)
    jl.frame_at = jfa
    jl.motion = M.combine(M.with_pivot(lambda t: Tf(dx=start_off + w1[1](t) + w2[1](t), dy=w1[2](t) + w2[2](t)),
                                       (HOLD_X, GY)),
                          dip(snap(t_take + 0.05), SC, (HOLD_X, GY), 6), dip(t_stop, SC, (HOLD_X, GY), 4),
                          nod(t_show + 0.3, (HOLD_X, GY), -3, 0.5), M.breathe(0.009, 2.7, pivot=(HOLD_X, GY), phase=0.3))
    hdx_fix = lambda t: start_off + w1[1](t) + w2[1](t)  # noqa: E731
    sc.layers[[l.name for l in sc.layers].index("coat")].motion = (
        lambda t: (lambda m: Tf(dx=hdx_fix(t) + m.dx - hdx(t), dy=m.dy, rot=m.rot, px=m.px, py=m.py, alpha=m.alpha))(
            coat_m(t)))

    # ---------------- Jacob's sad thought
    bh = C.body_points(C.jacob, JX, GY, SC, 1, pose="sad")["head_top"]
    tcx, tcy = bh[0] + 40, bh[1] - 250
    t_th0 = snap(t_beast - 0.25)
    t_th1 = snap(t_take + 0.1)
    sc.add("thought", doc(dream_cloud(tcx, tcy, 420, 260, S.g(thought_inner(tcx, tcy), filter="wobble"), seed=12,
                                      fill="#f3efe6")), z=3.0, wc=0.35,
           motion=M.combine(pop_in(t_th0, (tcx - 40, tcy + 100)), pop_out(t_th1, (tcx, tcy)), M.bob(3, 2.4)))
    for i, (dx, dy, r) in enumerate(((-110, 160, 15), (-140, 200, 10))):
        x, y = tcx + dx, tcy + dy
        sc.add(f"tdot{i}", doc(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f3efe6" stroke="{INK}" stroke-width="3.4"/>'),
               z=3.0, wc=0, motion=M.combine(pop_in(t_th0 - 0.1 * (i + 1), (x, y)), pop_out(t_th1 - 0.05, (x, y))))

    # ---------------- many days: a row of suns and moons filling above Jacob
    dcx, dcy = 980, 545

    def filled(t):
        return math.floor(10 * M.progress(t, t_days0 + 0.3, t_days1 - 0.1, "linear") + 1e-6) / 2.0
    steps = [k / 2 for k in range(0, 11)]
    dfr = [doc(PR.day_counter(dcx, dcy, 0.8, n=5, filled=f, icons="pair", gap=74)) for f in steps]
    sc.add("days", dfr, z=3.1, wc=0.3, frame_at=lambda t: float(steps.index(min(5.0, max(0.0, filled(t))))),
           motion=M.combine(pop_in(t_days0 - 0.15, (dcx, dcy)), M.bob(3, 2.6)))
    # night shade over the land and people (the counter and the sky stay clear)
    sc.add("night_shade", doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="#4a5590"/>'), z=2.98,
           wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.62 * night(t)))
    sc.fx.append(FX.tint((255, 200, 150), lambda t: 0.12 + 0.12 * dusk(t), mode="multiply"))

    # ---------------- foreground
    FG = [(60, 1160, 1.2, 0), (520, 1178, 1.0, 2), (1150, 1172, 1.05, 0), (1700, 1180, 1.0, 2), (2350, 1166, 1.15, 0)]
    sc.add("fg", [doc(tuft_row(FG, k * 2.1)) for k in range(3)], z=2.97, frame_at=lambda t: float(int(t * 2.2) % 3))

    # ---------------- sound
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_tear - 0.05, gain_db=-10)
    sc.sfx("footsteps", t_walk, dur=N_IN * WALK_P, gain_db=-17, pan=0.3)
    sc.sfx("cloth", t_show, gain_db=-15)
    sc.sfx("cloth", t_take, gain_db=-13)
    sc.sfx("footsteps", t_leave, dur=2.0, gain_db=-21, fade_out=0.6, pan=0.4)
    sc.sfx("night", t_days0, dur=T - t_days0, gain_db=-22, fade_in=1.0, fade_out=1.0)
    sc.sfx("sheep", 1.2, gain_db=-20, pan=0.5)
    return sc
