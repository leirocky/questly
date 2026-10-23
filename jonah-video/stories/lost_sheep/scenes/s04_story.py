"""Scene 4 - Luke 15:3-4. Jesus hears the grumbling and tells a story. The same courtyard, cast and camera as the end of
s03_meal (a plain cross-dissolve joins them). Jesus turns kindly to the Pharisees, stands up and turns to everyone; as he
asks his question a little picture book appears in his hands, floats up above his head and unfolds into a wide page: the
spring hills with the shepherd and his big flock, and one little lamb apart. Everyone leans in to think, and the camera
flies into the page until its picture fills the frame (s05 begins inside Jesus' story).

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity film's
Tm class, chunk fallback; nothing is hard-coded to the take):
  0 .. 1.0      identical to the end of s03 (the meal laughing on, the Pharisees with folded arms, frowning)
  '听见'         Jesus turns to the Pharisees, kind, not angry; the tax collector beside him glances at them too
  '就给他们'     he stands up (hop) and looks at them kindly; the elder Pharisee is taken aback
  '讲'           he turns to everyone at the table, telling; the guests turn to listen
  '故事'         he holds out both open hands
  Z '如果'       a little coral picture book pops up in his hands (chime, sparkle) and floats up above his head ...
  '你有一百只羊' ... and unfolds (8 frames, ~1 s) into a wide glowing page (page rustle): the spring hills, the shepherd
                leading his big flock, the little lamb apart sniffing a poppy; on '一百' the guests look up in wonder,
                a far bleat from the page
  '丢了一只'     a soft golden ring pulses twice round the little lamb in the page (a tiny bleat); the camera begins
                one slow, continuous flight into the page (a log-space zoom about the page, so it never jerks)
  '你会怎么做呢' Jesus turns to the Pharisees with the question; everyone, the Pharisees too, leans in to think
                (chin on the hand) and the camera flies on into the page (whoosh) until the picture fills the frame:
                a sharp full-resolution copy of the page fades in over the zoomed page, the courtyard's warm light,
                dust motes and the sparkles melt away
  end          calm hold inside the page (the flock nibbling) for the page-turn into s05
The page device (page_inner, story page frames, the hi-res copy) is shared with s11_meaning.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.lost_sheep.scenes import s03_meal as S3
from stories.lost_sheep.scenes.s03_meal import (END3, END_CAM, H3, K, PH, SEATS, SEAT_Y, STAND_Y, W3, Actor, add_air,
                                                add_flyers, add_front, add_gate_overlay, add_set, add_sparrows, breath,
                                                cam3, cam_seq, coin_stack_svg, log_push, splice, doc3, f1, guest_fn, jesus_fn, lean, ph_fn,
                                                sunlight_svg)
from stories.nativity.scenes.s07_shepherds import Tm, env, snap

# ------------------------------------------------------------------ the story page (shared with s11)
PW, PHT = 880, 528                       # the open double page
PX, PY = SEATS["jesus"], 560             # its spine foot when it floats open above Jesus
P0 = (PX - PW / 2, PY - PHT)             # the page's top-left on the stage (page coordinates (0, 0))
CAM_PAGE = Cam(PX, 296, 840)             # the camera inside the page (the picture fills the frame)
HI_F = 2112 / CAM_PAGE.w                 # the hi-res copy's up-scale: crisp at the page camera
HI_V0 = (CAM_PAGE.x - CAM_PAGE.w / 2, CAM_PAGE.y - CAM_PAGE.w * 9 / 32)
UNFOLD = [0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]     # the 8 quantised frames props.story_page suggests
GY_P = 405                               # the page's meadow line (page coordinates)
LAMB_P = (760, GY_P + 70)                # the little lamb in the page


def page_inner(phase=0.0):
    """Jesus' story in page coordinates (0, 0)-(PW, PHT): the bright spring hills, the shepherd leading his big flock,
    the little lamb apart sniffing a poppy."""
    s = 0.55
    gy = GY_P
    sx = 90
    pts = PR.spring_hills_points(0, PW, gy, s, stream_x=sx)
    b = PR.spring_sky(0, 0, PW, PHT, time=0, sun=(700, 92), clouds=0.8, scale=s, seed=4)
    b += PR.spring_hills(0, PW, gy, s, part="back", stream_x=sx, flowers=0.7)
    b += PR.spring_hills(0, PW, gy, s, part="mid", stream_x=sx, flowers=0.7)
    b += PR.flock(150, 720, gy - 140 * s, gy + 30, n=46, scale=s * 0.8, top=pts["mid_top"],
                  gaps=[(330, gy + 10, 80), (760, gy + 40, 90)], phase=phase, seed=3)
    b += PR.spring_hills(0, PW, gy, s, part="front", stream_x=sx, flowers=0.7)
    b += PR.flock(400, 680, gy - 6, gy + 60, n=9, scale=s * 0.95, k_far=0.85, phase=phase, seed=8,
                  gaps=[(330, gy + 40, 120)])
    b += C.parable_shepherd(330, gy + 40, s, 1, pose="lead_a")
    b += PR.little_lamb(LAMB_P[0], LAMB_P[1], s, -1, pose="sniff_flower", phase=phase)
    return b


def page_frames(inner, glow=0.6):
    return [doc3(PR.story_page(PX, PY, PW, PHT, inner=inner, unfold=u, glow=glow if u > 0 else 0.35)) for u in UNFOLD]


def hires_svg(inner):
    """The page's picture again at HI_F x size, placed so that the page camera's view maps to the canvas (0, 0)-(2112,
    1188); the layer is shrunk back by 1 / HI_F (hires_motion), so it is pixel-sharp when the camera is inside the
    page."""
    # the same nesting as story_page: the wobble filter's user space has its origin at the spine foot
    ax, ay = (PX - HI_V0[0]) * HI_F, (PY - HI_V0[1]) * HI_F
    clip = (f'<clipPath id="ls4hi"><rect x="{-PW / 2 + 12}" y="{-PHT + 12}" width="{PW - 24}" height="{PHT - 24}" '
            f'rx="6"/></clipPath>')
    return doc3(f'<g transform="translate({ax:.2f},{ay:.2f}) scale({HI_F:.5f})">{clip}<g filter="url(#wobble-fine)">'
                f'<g clip-path="url(#ls4hi)"><g transform="translate({-PW / 2},{-PHT})">{inner}</g></g></g></g>')


def hover(t, g0):
    """The open page's gentle hover (stage px), shared by the page and its hi-res copy."""
    return 3.0 * math.sin(2 * math.pi * (t + g0) / 2.6)


def hires_motion(alpha, g0, u=None):
    return lambda t: Tf(dx=HI_V0[0], dy=HI_V0[1] + hover(t, g0) * (u(t) if u else 1.0), sx=1 / HI_F, sy=1 / HI_F,
                        px=0, py=0, alpha=alpha(t))


def page_glow_svg():
    gid = "ls4pg"
    defs = S.rad_grad(gid, [(0, "#fff6d6", 0.75), (0.45, "#ffe3a0", 0.32), (1, "#ffe3a0", 0)])
    return doc3(f'<ellipse cx="{PX}" cy="{PY - PHT / 2}" rx="{PW * 0.78}" ry="{PHT * 0.95}" fill="url(#{gid})"/>', defs)


def ring_svg(x, y, r):
    return doc3(f'<g filter="url(#wobble-fine)"><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="none" '
                f'stroke="#fff3c0" stroke-width="7" opacity="0.95"/><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 1.25)}" '
                f'fill="none" stroke="#ffe08a" stroke-width="4" opacity="0.6"/></g>')


def book_motion(hands, t_pop, t_r0, t_r1, g0, t_fold=None, fold=None):
    """The little book: pops up in Jesus' hands at t_pop, floats from the hands to the open-page anchor (t_r0 -> t_r1),
    hovers gently. (s11 plays it backwards with fold=(t0, t1): from the anchor down into the hands.)"""
    hx, hy = hands

    def m(t):
        if fold is None:
            u = M.progress(t, t_r0, t_r1, "inout")
            k = M.progress(t, t_pop, t_pop + 0.32, "back") if t < t_pop + 0.32 else 1.0
            a = 1.0 if t >= t_pop else 0.0
        else:
            u = 1 - M.progress(t, fold[0], fold[1], "inout")
            k = 1 - M.progress(t, fold[1] + 0.05, fold[1] + 0.35, "in")
            a = 1.0 if t < fold[1] + 0.35 else 0.0
        x = hx + (PX - hx) * u
        y = hy + (PY - hy) * u - 26 * math.sin(math.pi * u)
        y += hover(t, g0) * u
        return Tf(dx=x - PX, dy=y - PY, sx=max(k, 0.001), sy=max(k, 0.001), px=PX, py=PY, alpha=a)
    return m


def unfold_at(t0, t1, reverse=False):
    n = len(UNFOLD) - 1

    def fa(t):
        u = M.progress(t, t0, t1, "linear")
        if reverse:
            u = 1 - u
        return float(min(n, int(u * n + 1e-6)))
    return fa


def hands_mid(pose, f):
    hp = C.body_points(C.jesus, SEATS["jesus"], STAND_Y, K, f, pose=pose)["hands"]
    return ((hp[0][0] + hp[1][0]) / 2, min(hp[0][1], hp[1][1]) + 6)


# ------------------------------------------------------------------ the seated cast (shared with s11)
def seated_actors(g0, start, rng_seed=40):
    """The meal at the table and the Pharisees, each starting in state start[name] (drawn at the seat / standing
    anchor). Same names, layers and order as s03, so neighbouring scenes match."""
    acts = {}
    acts["jesus"] = Actor("jesus", jesus_fn, (SEATS["jesus"], SEAT_Y), 50, g0, seed=101)
    z = {"tax0": 52, "tax1": 51.2, "tax2": 51.1, "woman": 49.2, "young": 49.1, "labourer": 49.0}
    for who, zz in z.items():
        name = who if who.startswith("tax") else who + "_in"
        seed = {"tax0": 111, "tax1": 121, "tax2": 122, "woman": 140, "young": 141, "labourer": 142}[who]
        if who in S3.BASES:
            base, off = S3.BASES[who]
            a = Actor(name, guest_fn(who), base, zz, g0, piv=(SEATS[who], SEAT_Y), seed=seed, oy0=SEAT_Y - S3.BACK_Y)
            a.path = lambda t, off=off: (off[0], off[1], 1.0)
        else:
            a = Actor(name, guest_fn(who), (SEATS[who], SEAT_Y), zz, g0, seed=seed)
        acts[who] = a
    for v, (x, y) in PH.items():
        acts[f"ph{v}"] = Actor(f"ph{v}", ph_fn(v), (x, y), 70 + (0.2 if v == 0 else (0.1 if v == 2 else 0.0)), g0,
                               seed=160 + v, shadow=110)
    for k, a in acts.items():
        a.cut(0, start[k])
    return acts


def build(ctx):
    sc = Scene(ctx, W=W3, H=H3)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    at = tm.at
    import random
    rng = random.Random(41)

    t_ting = at(0, "听见")
    t_jiu = at(0, "就给")
    t_jiang = at(0, "讲了")
    t_gushi = at(0, "故事")
    t_ru = at(1, "如果")
    t_you = at(1, "你有")
    t_yibai = at(1, "一百")
    t_yang = at(1, "只羊", 1)
    t_diu = at(1, "丢了")
    t_ni = at(1, "你会")
    t_zuo = at(1, "怎么做")
    t_qend = ctx.lines[1].end

    add_set(sc, g0, "day")
    add_gate_overlay(sc)
    add_front(sc, g0)
    add_sparrows(sc, g0)
    add_flyers(sc, g0)
    sc.add("coins", coin_stack_svg(0, 1.0), z=61, seed=301)

    acts = seated_actors(g0, END3)
    sto = STAND_Y - SEAT_Y
    jes = acts["jesus"]
    # '耶稣听见了': kindly to the Pharisees
    jes.cut(t_ting, ("sit_look_kind", "kind", 1, 0, 0, 0))
    jes.cut(t_jiu, ("look_kind", "kind", 1, 0, 0, sto), depth=10)
    jes.cut(t_jiang + 0.05, ("tell", "smile", -1, 0, 0, sto))
    jes.cut(t_gushi, ("open_hands", "smile", -1, 0, 0, sto))
    t_pop = t_ru + 0.05
    t_r0, t_r1 = t_pop + 0.34, t_pop + 0.9
    t_u0, t_u1 = t_r1 - 0.06, t_r1 + 1.05
    jes.cut(t_r1 + 0.1, ("open_hands", "warm", -1, 0, 0, sto), depth=3)
    jes.cut(t_yibai + 0.1, ("tell", "smile", -1, 0, 0, sto))
    jes.cut(t_diu, ("look_kind", "kind", -1, 0, 0, sto))
    jes.cut(t_ni, ("tell", "smile", 1, 0, 0, sto))
    jes.blinks(1.2, T - 0.3, rng)

    oy = 0
    # the guests: they hush, turn to listen, look up at the page, lean in to think
    plan = {
        "tax0": [(t_ting + 0.25, ("listen", "worried", 1, 0, 0, oy)), (t_jiang + 0.25, ("listen", "kind", -1, 0, 0, oy)),
                 (t_yibai, ("smile", "surprised", -1, 0, 0, oy)), (t_ni + 0.1, ("listen", "ponder", -1, 0, 0, oy))],
        "tax1": [(t_ting + 0.4, ("smile", "neutral", 1, 0, 0, oy)), (t_jiang + 0.35, ("listen", "kind", 1, 0, 0, oy)),
                 (t_yibai + 0.15, ("warm", "touched", 1, 0, 0, oy)), (t_ni + 0.2, ("listen", "ponder", 1, 0, 0, oy))],
        "tax2": [(t_ting + 0.6, ("smile", "neutral", 1, 0, 0, oy)), (t_jiang + 0.45, ("listen", "kind", 1, 0, 0, oy)),
                 (t_yibai + 0.3, ("smile", "surprised", 1, 0, 0, oy)), (t_ni + 0.3, ("listen", "ponder", 1, 0, 0, oy))],
        "woman": [(t_ting + 0.5, ("smile", "neutral", 1, 0, 0, oy)), (t_jiang + 0.5, ("listen", "kind", 1, 0, 0, oy)),
                  (t_yibai + 0.2, ("warm", "touched", 1, 0, 0, oy)), (t_ni + 0.35, ("listen", "ponder", 1, 0, 0, oy))],
        "young": [(t_ting + 0.7, ("smile", "neutral", 1, 0, 0, oy)), (t_jiang + 0.6, ("listen", "kind", 1, 0, 0, oy)),
                  (t_yibai + 0.35, ("smile", "surprised", 1, 0, 0, oy)), (t_ni + 0.25, ("listen", "ponder", 1, 0, 0, oy))],
        "labourer": [(t_ting + 0.8, ("smile", "neutral", 1, 0, 0, oy)), (t_jiang + 0.7, ("listen", "kind", 1, 0, 0, oy)),
                     (t_yibai + 0.45, ("warm", "touched", 1, 0, 0, oy)), (t_ni + 0.4, ("listen", "ponder", 1, 0, 0, oy))],
    }
    for who, cuts in plan.items():
        a = acts[who]
        for tc, st in cuts:
            a.cut(tc, st)
        f = 1 if who != "tax0" else -1
        a.extra.append(lean(t_ni + 0.15, 1e9, 3.2 * f, (SEATS[who], SEAT_Y), fin=0.5))
        a.blinks(1.2, T - 0.3, rng)
    # the Pharisees: caught grumbling, they listen, glance at each other at the page, then lean in to think
    p0, p1, p2 = acts["ph0"], acts["ph1"], acts["ph2"]
    p0.cut(t_ting + 0.35, ("stand", "surprised", -1, 0, 0, 0))
    p2.cut(t_ting + 0.55, ("stand", "worried", -1, 0, 0, 0))
    p1.cut(t_jiu + 0.2, ("arms_folded", "stern", -1, 0, 0, 0))
    p0.cut(t_jiang + 0.3, ("arms_folded", "ponder", -1, 0, 0, 0))
    p2.cut(t_gushi, ("arms_folded", "stern", -1, 0, 0, 0))
    p0.cut(t_yibai + 0.2, ("look_at_each_other", "ponder", 1, 0, 0, 0))
    p2.cut(t_yibai + 0.35, ("look_at_each_other", "ponder", -1, 0, 0, 0))
    p1.cut(t_diu, ("stand", "ponder", -1, 0, 0, 0))
    for a, dt in ((p0, 0.12), (p2, 0.25), (p1, 0.35)):
        a.cut(t_ni + dt, ("think", "ponder", -1, 0, 0, 0))
        a.extra.append(lean(t_ni + dt + 0.1, 1e9, -2.6, a.base, fin=0.5))
        a.blinks(1.2, T - 0.3, rng)
    for a in acts.values():
        a.build(sc)

    # ---------------------------------------------------------------- the picture book
    inner = page_inner(0.0)
    hands = hands_mid("open_hands", -1)
    sc.add("page_glow", page_glow_svg(), z=80, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=0.9 * M.progress(t, t_u0 + 0.2, t_u1, "sine") *
                               (0.92 + 0.08 * math.sin(2 * math.pi * (t + g0) / 2.2))))
    sc.add("book", page_frames(inner), z=81, frame_at=unfold_at(t_u0, t_u1),
           motion=book_motion(hands, t_pop, t_r0, t_r1, g0))
    lx, ly = P0[0] + LAMB_P[0], P0[1] + LAMB_P[1] - 30
    for i in range(2):
        tp = t_diu + 0.05 + 0.45 * i
        sc.add(f"lamb_ring{i}", ring_svg(lx, ly, 46), z=82, blend="screen", wc=0,
               motion=lambda t, tp=tp: Tf(alpha=env(t, tp, tp + 0.7, 0.15, 0.45),
                                          sx=0.7 + 0.5 * M.progress(t, tp, tp + 0.7, "out"),
                                          sy=0.7 + 0.5 * M.progress(t, tp, tp + 0.7, "out"), px=lx, py=ly))
    # inside the page: a sharp copy fades in over the zoomed page as the camera flies in (the flock nibbles)
    t_p0, t_p1 = t_ni + 0.05, T - 1.0
    t_h0, t_h1 = t_p0 + 0.42 * (t_p1 - t_p0), t_p1 - 0.08
    hi = [hires_svg(page_inner(ph)) for ph in (0.0, 0.5)]
    sc.add("page_hi", hi, z=83, wc=0.5,
           frame_at=lambda t: 0.0 if t < t_h1 + 0.15 else float(int((t + g0) / 0.7) % 2),
           motion=hires_motion(lambda t: M.progress(t, t_h0, t_h1, "sine"), g0))
    sc.fx.append(FX.sparkles((P0[0] - 40, P0[1] - 10, P0[0] + PW + 40, PY + 30), count=16, t0=t_u0 + 0.3,
                             t1=t_p0 + 0.6, color=(255, 240, 190), size=(8, 16), period=1.7, drift=-6, seed=44))
    sc.fx.append(FX.sparkles((hands[0] - 60, hands[1] - 80, hands[0] + 60, hands[1] + 10), count=7, t0=t_pop - 0.1,
                             t1=t_r1 + 0.2, color=(255, 236, 170), size=(7, 13), period=1.1, drift=-20, seed=45))

    # ---------------------------------------------------------------- camera
    c_turn = Cam(2100, 740, 1500)
    c_tell = Cam(1720, 730, 1650)
    c_page = Cam(1880, 594, 2112)
    t_c0 = t_diu + 0.25                     # one continuous flight into the page (log-space zoom)
    # the courtyard's warm light and dust melt away as we fly into the page
    sc.add("sun", sunlight_svg("day"), z=95, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_c0, t_p1, "sine")))
    add_air(sc, g0, "day", t1=t_p1)
    base = cam_seq([(0.0, END_CAM), (1.0, END_CAM), (t_jiu + 0.3, c_turn), (t_gushi, c_tell), (t_r0, c_tell),
                    (t_u1, c_page), (t_c0, c_page), (t_p1, CAM_PAGE, "linear"), (T, CAM_PAGE)])
    sc.camera = splice(base, t_c0, t_p1, log_push(t_c0, t_p1, c_page, CAM_PAGE))

    # ---------------------------------------------------------------- sound
    sc.sfx("crowd", 0, dur=t_p1, gain_db=-29, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T, gain_db=-26, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_jiu, gain_db=-22)
    sc.sfx("chime", t_pop, gain_db=-15)
    sc.sfx("sparkle", t_pop + 0.1, gain_db=-19)
    sc.sfx("cloth", t_u0 + 0.15, gain_db=-17)
    sc.sfx("sheep", t_yang + 0.15, gain_db=-24, pan=0.2)
    sc.sfx("sheep", t_diu + 0.3, gain_db=-21, pan=0.4)
    sc.sfx("whoosh", t_p0 + 0.2, gain_db=-16)
    sc.sfx("sparkle", t_p1 - 0.3, gain_db=-21)
    return sc
