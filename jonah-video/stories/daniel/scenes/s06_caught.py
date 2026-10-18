"""Scene 6 — caught praying (Daniel 6:11-13).

"那些官员早就躲在外面偷看。'看！他在向他的上帝祷告！' 他们急忙跑去告诉国王：'王啊，但以理不听你的命令，他一天三次
向他的上帝祷告！'"

Two places, joined by a soft page-turn dissolve:
  * THE STREET (s05's stage, drawings and clocks: the scene opens on s05's last frame — Daniel kneeling at his
    open window in the warm prayer light).
      line 0  "那些官员早就躲在外面偷看。" the camera eases down and right to the big storage jars by the street:
              one, two, three jealous officials pop up from behind them (hop cuts from a crouch) and peek up at the
              window with sly faces.
      line 1  "看！他在向他的上帝祷告！" the front official jumps up and points up at the window ("!"); the other two
              turn face to face and whisper, smirking.
      line 2  "他们急忙跑去告诉国王：" they come out from behind the jars and hurry off to the left along the street
              (fast planted-foot walk), the camera following a little.
  * THE PALACE (s07's hall, palace_layers): a dissolve as they leave the frame.
      line 3  "王啊，但以理不听你的命令，" the three bow low before King Darius on his throne; the front official
              rises and points back toward Daniel's house; the king is startled.
              "他一天三次向他的上帝祷告！" a picture bubble pops up over them: Daniel kneeling at his window under
              three little suns; the king looks worried. The bubble pops away; calm last frame (s07 starts on it).
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
from stories.daniel.scenes import s05_prays as A
from stories.daniel.scenes import s07_king_sad as B
from stories.daniel.scenes.s05_prays import (GY, WALK_N, Perf, clamp, doc, fig, phrase_t, sprite,
                                             walk_pose)

KO = 0.75                       # officials' scale in the street
OFF_X = {1: 2690, 2: 2778, 0: 2905}    # behind the jars (v1, v2 whisper face to face; v0 at the right)
FRONT_X = 2420
DX = 430                        # the palace is drawn shifted right by DX on this stage (s07 draws it unshifted)                  # walking left past here they are clear of the jars (drawn in front of the stair)
OFF_Y = GY - 10

# scene-local official poses
HIDE = C._P(t=34, h=-6, drop=118, legs=(("ik", 34, 1), ("ik", -36, 1)),
            arms=(("ik", "abs", 92, -150, 1), ("ik", "abs", 76, -132, 1)), hands=("open", "open"), expr="sly")
PEEK_UP = C._P(t=20, h=-22, drop=14, legs=(("ik", 30, 1), ("ik", -32, 1)),
               arms=(("ik", "abs", 96, -212, 1), ("ik", "abs", 78, -190, 1)), hands=("open", "open"),
               expr="sly", look=(0.04, -0.07))
POINT_UP = C._P(t=-4, h=-18, legs=((6, 2), (-6, -2)), arms=(("fk", 132, 140), ("fk", -8, -3)),
                hands=("point", "fist"), expr="shout", look=(0.04, -0.08))


def s05_clock():
    """(s05 duration, s05 kneel time) so the window light and breathing continue exactly from s05."""
    try:
        c5 = context("s05_prays")
        return c5.duration, c5.lines[3].chunks[1].start + 0.05
    except Exception:
        return 24.43, 19.88


def build(ctx):
    sc = Scene(ctx, W=A.SW, H=A.SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]
    T5, k5 = s05_clock()
    toff = T5 - 1.0                                  # s06 t=0 is s05's t = T5 - 1 (the 1 s dissolve)

    # ---------------------------------------------------------------- beats
    t_peek = [L0.start + 0.75, L0.start + 1.2, L0.start + 1.65]   # v1, v2, v0 pop up
    t_point = L1.start - 0.05                        # "看！" v0 jumps up and points
    t_whisp = phrase_t(L1, "他在向", 0.25) + 0.05    # v1 and v2 whisper face to face
    t_run = L2.start - 0.15                          # "他们急忙跑去告诉国王"
    t_x0 = L2.end + 0.05                             # dissolve to the palace
    t_x1 = t_x0 + 0.75
    t_rise = L3.chunks[0].start + 0.9                # "但以理不听你的命令": v0 rises and points back
    t_king0 = L3.chunks[0].start + 1.25              # the king is startled
    t_bub = L3.chunks[1].start - 0.1                 # "他一天三次…" picture bubble
    t_king1 = L3.chunks[1].start + 0.9               # the king worried
    t_bub_out = min(L3.end + 0.25, T - 1.2)
    t_bow2 = L3.end - 0.3                            # v0 bows again

    street_a = lambda t: 1.0 - M.progress(t, t_x0, t_x1, "sine")
    pal_a = lambda t: M.progress(t, t_x0, t_x1, "sine")

    # ================================================================ THE STREET (s05's stage)
    A.add_backdrop(sc, toff, alpha=street_a)
    A.add_far(sc)
    A.add_street(sc)
    sc.add("win_back", A.window_back_svg(1.0), wc=0.5)
    sp_in, DI = A.window_daniel_sprite()
    sc.add_dynamic("daniel_in", Perf(sp_in, [(0, DI["pray"], 0)], lambda t: (A.WIN_X - 6, A.FLOOR_UP),
                                     breathe=A.WIN_BREATHE[0], bper=A.WIN_BREATHE[1],
                                     phase=(toff % A.WIN_BREATHE[1]) / A.WIN_BREATHE[1],
                                     alpha=lambda t: 1.0 if t < t_x1 else 0.0))
    A.add_house(sc, toff)
    sc.add("win_front", A.window_front_svg(1.0), wc=0.6)
    A.add_doves(sc, toff, alpha=street_a)

    # the officials behind the jars
    sprs, perfs = {}, {}
    for v in (1, 2, 0):
        sp = sprite(520, 470, 260, 430, seed=60 + v)
        x0 = OFF_X[v]
        idx = dict(hide=sp.add(fig(C._official_design(v), C._OFFICIAL_M, dict(HIDE), "sly", sp.ax, sp.ay, KO, -1, "h")),
                   peek=sp.add(fig(C._official_design(v), C._OFFICIAL_M, dict(PEEK_UP), "sly", sp.ax, sp.ay, KO, -1, "p")),
                   whisper=sp.add(C.official(sp.ax, sp.ay, KO, 1 if v == 1 else -1, variant=v, pose="whisper")),
                   point=sp.add(fig(C._official_design(v), C._OFFICIAL_M, dict(POINT_UP), "shout", sp.ax, sp.ay, KO, -1, "u")))
        W = []
        for k in range(2 * WALK_N):
            ps = walk_pose(k, A=66)
            ps["t"] = 10                              # leaning into the hurry
            W.append(sp.add(fig(C._official_design(v), C._OFFICIAL_M, ps, "sly", sp.ax, sp.ay, KO, -1, "w")))
        sprs[v] = (sp, idx, W)

    adv = 2 * 66 / WALK_N * KO
    rate = 34.0                                       # drawings / s: a hurried walk (~560 px/s)
    starts = {1: t_run, 2: t_run + 0.12, 0: t_run + 0.24}

    for i, v in enumerate((1, 2, 0)):
        sp, idx, W = sprs[v]
        x0 = OFF_X[v]
        sched = [(0, idx["hide"], 0), (t_peek[i], idx["peek"], 1.0)]
        if v == 0:
            sched += [(t_point, idx["point"], 1.2)]
        else:
            sched += [(t_whisp + 0.15 * (v == 2), idx["whisper"], 0.8)]
        tw = starts[v]
        sched += [(tw - 0.1, W[0], 0.4)]

        def wk(t, tw=tw):
            return None if t < tw else int((t - tw) * rate + 1e-6)

        def walk(t, W=W, wk=wk):
            k = wk(t)
            return None if k is None else W[k % (2 * WALK_N)]

        def pos(t, x0=x0, wk=wk):
            k = wk(t)
            return (x0 if k is None else x0 - k * adv), OFF_Y

        # behind the jars while hiding; once clear of them (x < FRONT_X) they walk IN FRONT of the stair
        back = lambda t, pos=pos: street_a(t) if pos(t)[0] >= FRONT_X else 0.0
        front = lambda t, pos=pos: street_a(t) if pos(t)[0] < FRONT_X else 0.0
        sc.add_dynamic(f"off{v}", Perf(sp, sched, pos, walk=walk, breathe=0.012, bper=2.6 + 0.3 * i,
                                       phase=0.2 * i, alpha=back))
        perfs[v] = Perf(sp, sched, pos, walk=walk, breathe=0.012, bper=2.6 + 0.3 * i, phase=0.2 * i, alpha=front)

    # "!" over the pointing official
    hx, hy = OFF_X[0] + 40, OFF_Y - 372             # above the pointing official's hat
    bang = doc(S.g(f'<path d="M{hx},{hy - 70} L{hx + 8},{hy - 10}" stroke="{P["ink"]}" stroke-width="12" stroke-linecap="round"/>'
                   f'<circle cx="{hx + 10}" cy="{hy + 14}" r="7" fill="{P["ink"]}"/>', filter="wobble-fine"))

    def bang_m(t):
        u = t - t_point - 0.05
        if u < 0 or u > 1.4:
            return Tf(alpha=0.0)
        k = M.ease("back")(clamp(u / 0.2))
        return Tf(sx=max(0.01, k), sy=max(0.01, k), alpha=1 - M.progress(u, 1.0, 1.4, "sine"), px=hx, py=hy + 20)
    sc.add("bang", bang, wc=0, motion=bang_m)

    A.add_front(sc, toff, alpha=street_a)
    for v in (1, 2, 0):
        sc.add_dynamic(f"off{v}_front", perfs[v])

    # the prayer light at the window (continues from s05)
    win_a = lambda t: 0.75 * (0.85 + 0.15 * math.sin(2 * math.pi * (t + toff - k5) / 2.6)) * street_a(t)
    sc.add("beam2", A.light_rays_svg(A.WIN_X - 420, 120, A.WIN_X - 60, A.WIN_Y - 60, 5, 0.92, (210, 70), "s5b2"),
           wc=0, blend="screen", motion=lambda t: Tf(alpha=win_a(t)))

    # ================================================================ THE PALACE (fades in over the street)
    sc.add("palace", B.palace_flat_svg(0.08, dx=DX, beams_a=0.25), wc=0.7, motion=lambda t: Tf(alpha=pal_a(t)))
    PX = {1: 1330 + DX, 2: 1480 + DX, 0: 1640 + DX}
    ks = sprite(520, 480, 260, 440, seed=70)
    k_sit = B.king_fig(ks, "sit_throne", facing=-1)
    k_surp = B.king_fig(ks, "sit_throne", "surprised", facing=-1)
    k_worry = B.king_fig(ks, "sit_throne", "worried", facing=-1)
    sc.add_dynamic("king", Perf(ks, [(0, k_sit, 0), (t_king0, k_surp, 0.7), (t_king1, k_worry, 0.4)],
                                lambda t: (B.THRONE_X + DX, B.DAIS_Y), alpha=pal_a, breathe=0.010, bper=3.4))
    for i, v in enumerate((1, 2, 0)):
        sp = sprite(560, 480, 280, 440, seed=75 + v)
        bow = B.official_fig(sp, v, "bow", facing=1)
        sched = [(0, bow, 0)]
        if v == 0:
            pt = B.official_fig(sp, v, "point", "shout", facing=-1)
            sch = B.official_fig(sp, v, "scheme", "smug", facing=1)
            sched += [(t_rise, pt, 1.0), (t_bub - 0.05, sch, 0.7), (t_bow2, bow, 0.6)]
        sc.add_dynamic(f"poff{v}", Perf(sp, sched, lambda t, v=v: (PX[v], B.FY), alpha=pal_a, breathe=0.012,
                                        bper=2.8 + 0.3 * i, phase=0.25 * i))

    # the picture bubble: Daniel kneeling at his window under three little suns
    bx, by = 1560 + DX, 700
    inner = ""
    ws = 0.42
    wx, wy = bx + 10, by + 92
    inner += PR.upstairs_window(wx, wy, ws, open=1.0, part="back", wall=False, glow=0.8)
    inner += C.daniel(wx - 3, wy + 90 * ws, ws, -1, pose="kneel_pray")
    wall_patch = (f'<path d="M{wx - 160},{wy - 150} L{wx + 160},{wy - 150} L{wx + 160},{wy + 40} L{wx - 160},{wy + 40} Z '
                  f'M{wx - 40},{wy} L{wx - 40},{wy - 110} L{wx + 40},{wy - 110} L{wx + 40},{wy} Z" fill="{A.HOUSE_COL}" '
                  f'fill-rule="evenodd" stroke="{P["ink"]}" stroke-width="3"/>')
    inner += S.g(wall_patch, filter="wobble-fine")
    inner += PR.upstairs_window(wx, wy, ws, open=1.0, part="front", wall=False)
    for j, (sx_, sy_) in enumerate(((bx + 130, by - 40), (bx, by - 78), (bx - 130, by - 40))):
        inner += f'<g transform="translate({sx_},{sy_}) scale(0.42)">{A.sun_local()}</g>'
    cid = "s6bub"
    clip = f'<clipPath id="{cid}"><ellipse cx="{bx}" cy="{by}" rx="215" ry="148"/></clipPath>'
    content = f'{clip}<g clip-path="url(#{cid})">{inner}</g>'
    bub = doc(A.bubble_svg(bx, by, 220, 150, (PX[0] + 20, B.FY - 360), content))
    sc.add("bubble", bub, wc=0.4, motion=lambda t: Tf(**_mul(A._pop(t, t_bub, t_bub_out, bx, by + 80), pal_a(t))))

    # ---------------------------------------------------------------- CAMERA
    cam0 = Cam(2338, 738, 1460)                      # s05's last frame
    camE = Cam(2440, 905, 1500)                      # window + the jars
    camE2 = Cam(2425, 912, 1480)
    camF = Cam(2335, 915, 1500)                      # they hurry out on the left; the palace is framed here too
    camP = Cam(B.CAM0.x + DX, B.CAM0.y, B.CAM0.w)    # s07's first frame
    sc.camera = M.cam_keys([(0.0, cam0), (L0.start + 0.1, cam0), (t_peek[0] + 0.5, camE), (t_run, camE2),
                            (t_x0, camF), (t_x1 + 0.2, camF), (T, camP)], "sine")

    # ---------------------------------------------------------------- FX
    sp_fx = FX.sparkles((A.WIN_X - 330, 420, A.WIN_X + 230, 640), count=14, t0=k5 + 0.3, t1=1e9,
                        color=(255, 238, 170), size=(8, 16), period=1.6, drift=-8, seed=9)

    def win_sparkles(frame, t, view):
        if t > t_x1:
            return frame
        return sp_fx(frame, t + toff, view)
    motes = FX.motes((300, 300, 3000, 1300), count=20, color=(255, 246, 214), size=(3, 6), alpha=90)
    sc.fx = [win_sparkles, lambda frame, t, view: frame if t > t_x1 else motes(frame, t, view)]

    # ---------------------------------------------------------------- SOUND
    sc.sfx("birds", 0, dur=t_x1, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("wind_soft", 0, dur=t_x1, gain_db=-20, fade_in=0.8, fade_out=0.8)
    for i, ts in enumerate(t_peek):
        sc.sfx("pop", ts, gain_db=-14 + i, pan=0.35 + 0.05 * i)
    sc.sfx("cloth", t_point, gain_db=-13, pan=0.4)
    sc.sfx("pop", t_point + 0.05, gain_db=-12, pan=0.4)
    sc.sfx("cloth", t_whisp, gain_db=-17, pan=0.3)
    sc.sfx("whoosh", t_run, gain_db=-16, pan=0.2)
    sc.sfx("footsteps_run", t_run, dur=t_x1 - t_run, gain_db=-13, fade_in=0.1, fade_out=0.5, pan=-0.1)
    sc.sfx("cloth", t_x1 - 0.1, gain_db=-16)
    sc.sfx("cloth", t_rise, gain_db=-15, pan=-0.1)
    sc.sfx("pop", t_bub, gain_db=-11)
    sc.sfx("pop", t_bub_out, gain_db=-15)
    return sc


def _mul(tf, a):
    return dict(dx=tf.dx, dy=tf.dy, rot=tf.rot, sx=tf.sx, sy=tf.sy, alpha=tf.alpha * a, px=tf.px, py=tf.py)
