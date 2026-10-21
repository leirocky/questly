"""Scene 14 — the closing page. One tall page, no cuts: high on the wall of the siblings' room (the room of s02) a
string with clothes-pegs; three little picture-book panels of Joseph's hard road pop onto it as they are named; then
the camera glides down to the siblings - the little brother still sulking under his storm cloud - and through the
pause; then they make up: sorry, a hug (the cloud turns sunny), a warm corner picture of Joseph hugging his brother,
and the toy shared, smiling. End card '约瑟和彩衣 · 完' with a small heart.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame: the empty string with its pegs high on the wallpaper, sunbeam motes
  '被卖'        panel 1 pops onto the string and swings: the caravan - a trader leading a camel, Joseph (torn
               tunic) sad behind it (pop)
  '被冤枉'      panel 2: an Egyptian guard leading Joseph (servant's linen) away between painted columns (pop)
  '关进监牢'    panel 3: Joseph sitting sad on the straw under a small barred prison window (pop)
  '从来没有离开上帝' in each panel in turn Joseph folds his hands and prays (little bounce)
  '上帝也从来没有离开他' a soft golden light glows up in every panel, one after another, with twinkles (chime)
  line 1       '小朋友' the camera glides down the wall to the siblings: the little one still sulking with arms
               crossed under his drizzling cloud, the sister holding the horse, a bit sorry; '你愿意原谅他吗？' he
               glances back over his shoulder; the 2 s pause holds on them (breathing, blinks, drizzle)
  line 2       '上帝可以把不好的事' she walks over (planted-foot steps) and says sorry (head bowed);
               '变成好事' he turns round and they hug (squash cut): the cloud turns into a smiling sunny cloud and
               floats off, two little hearts pop up; '像约瑟一样' a warm corner picture of Joseph hugging his
               brother glows up (hug_pair, chime); '学会原谅' she holds the horse out to share, both smiling
  end          the end card '约瑟和彩衣 · 完' fades in with a little heart (chime); calm final frame for the film's
               fade-out
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.joseph.scenes import s02_question as Q
from stories.joseph.scenes.s01_title import blink_name, char_times, cuts, dip, heart_markup, snap, voice_marks

INK = P["ink"]
OY = 700                                    # the room is s02's room moved down by OY
SH = 1188 + OY
KS, KY = Q.KS, Q.KY + OY
SIS0, SIS1, BRO = Q.SIS_X - 50, 1006, Q.BRO_X     # sister: by the rug -> beside him (hug gap 70*KS)
SIS_SORRY = 912
CLOUD = (BRO + 18, Q.CLOUD[1] + OY)
STRING_Y = 214
PANELS = [(420, 0.0, -2.0), (1056, 0.0, 1.5), (1692, 0.0, -1.2)]   # (centre x, -, tilt)
PW, PH = 520, 400
PK = 1.14                                   # panels are drawn at PW x PH and scaled up by PK about the top
PANEL_TOP = 262
CORNER = (432, 1052)                         # the warm corner picture centre (stage)
CW, CH = 470, 330
END = (1080, 1000)


def doc(body, defs=""):
    return S.svg_doc(body, defs, W, SH)


# ================================================================== the room and the string


def wall_svg():
    body, defs = Q.room_body(oy=OY, top=-20, drawing=False, clock=False)
    return doc(body, defs)


def string_svg():
    d = f"M-30,{STRING_Y - 10} Q{W / 2},{STRING_Y + 70} {W + 30},{STRING_Y - 10}"
    b = (f'<path d="{d}" stroke="{INK}" stroke-width="7" fill="none"/>'
         f'<path d="{d}" stroke="#d9b98a" stroke-width="3.5" fill="none"/>')
    for x in (-10, W + 10):
        b += f'<circle cx="{x}" cy="{STRING_Y - 10}" r="14" fill="#b07a48" stroke="{INK}" stroke-width="3"/>'
    return doc(S.g(b, filter="wobble-fine"))


def string_y(x):
    u = (x + 30) / (W + 60)
    return (1 - u) ** 2 * (STRING_Y - 10) + 2 * u * (1 - u) * (STRING_Y + 70) + u ** 2 * (STRING_Y - 10)


def peg(x, y):
    return (f'<rect x="{x - 9}" y="{y - 26}" width="18" height="56" rx="5" fill="#e8b45a" stroke="{INK}" '
            f'stroke-width="3"/><path d="M{x - 9},{y + 4} L{x + 9},{y + 4}" stroke="{INK}" stroke-width="2.5"/>')


def empty_pegs_svg(k):
    """Pegs already clipped on the string where picture k will hang (a calm first frame)."""
    b = ""
    for cx, _, _ in PANELS[k:k + 1]:
        for dx in (-150 * PK, 150 * PK):
            x = cx + dx
            b += peg(x, string_y(x) + 10)
    return doc(S.g(b, filter="wobble-fine"))


# ================================================================== the three panels


def _panel_frame(cx, inner, defs_id, tilt, glow=False):
    x0, y0 = cx - PW / 2, PANEL_TOP
    ix0, iy0, iw, ih = x0 + 20, y0 + 20, PW - 40, PH - 40
    clip = f'<clipPath id="{defs_id}"><rect x="{ix0}" y="{iy0}" width="{iw}" height="{ih}" rx="10"/></clipPath>'
    b = (f'<rect x="{x0 + 8}" y="{y0 + 12}" width="{PW}" height="{PH}" rx="14" fill="{INK}" opacity="0.22" '
         f'filter="url(#soft)"/>'
         f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" rx="14" fill="#fbf4e2" stroke="{INK}" stroke-width="4.5"/>')
    b += f'<g clip-path="url(#{defs_id})">{inner}</g>'
    b += (f'<rect x="{ix0}" y="{iy0}" width="{iw}" height="{ih}" rx="10" fill="none" stroke="{INK}" '
          f'stroke-width="3"/>')
    for dx in (-150, 150):
        b += peg(cx + dx, y0 + 4)
    return (f'<g transform="rotate({tilt} {cx} {y0}) translate({cx},{y0}) scale({PK}) translate({-cx},{-y0})">'
            f'{b}</g>'), clip


def panel_caravan(cx, pray=False):
    x0, y0 = cx - PW / 2, PANEL_TOP
    gy = y0 + PH - 64
    defs = S.lin_grad("j14p1", [(0, "#f6d9a6"), (1, "#f9e9c8")])
    b = f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" fill="url(#j14p1)"/>'
    b += f'<circle cx="{x0 + 420}" cy="{y0 + 92}" r="38" fill="#fbe1a0" stroke="{INK}" stroke-width="3"/>'
    b += S.path(S.hill(x0 - 40, x0 + PW + 40, gy - 30, 50, seed=3, bumps=3, bottom=y0 + PH + 20), fill="#ecc98c",
                sw=3)
    b += S.path(f"M{x0 - 20},{gy - 6} Q{cx},{gy - 26} {x0 + PW + 20},{gy - 8} L{x0 + PW + 20},{y0 + PH + 20} "
                f"L{x0 - 20},{y0 + PH + 20} Z", fill="#e5bb78", sw=3)
    b += PR._haze(PR.pyramids(x0 + 400, gy - 40, 0.1, n=2, haze=0.3, ground=False), "#f6d9a6", 0.2, 0.2)
    s = 0.48
    b += C.ground_shadow(x0 + 255, gy + 2, s, 300, 0.16)
    b += PR.camel(x0 + 250, gy, s, 1, pose="walk", phase=0.25)
    b += C.trader(x0 + 455, gy, s, 1, variant=0, pose="lead", expr="neutral")
    b += C.joseph(x0 + 92, gy, s, 1, pose="pray" if pray else "sad", coat="torn",
                  expr="peaceful" if pray else "sad")
    frame, clip = _panel_frame(cx, b, "j14c1", PANELS[0][2])
    return doc(S.g(frame), defs + clip)


def panel_guard(cx, pray=False):
    x0, y0 = cx - PW / 2, PANEL_TOP
    gy = y0 + PH - 60
    defs = S.lin_grad("j14p2", [(0, "#efe1c4"), (1, "#e2cda4")])
    b = f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" fill="url(#j14p2)"/>'
    # painted frieze and floor
    for k in range(10):
        col = ("#4f86c6", "#c9714a", "#6fae55")[k % 3]
        b += f'<rect x="{x0 + k * 56}" y="{y0 + 46}" width="40" height="18" fill="{col}" opacity="0.8"/>'
    b += f'<rect x="{x0}" y="{gy}" width="{PW}" height="80" fill="#c9a877" stroke="{INK}" stroke-width="3"/>'
    b += PR.egypt_column(x0 + 70, gy, 0.62, height=420) + PR.egypt_column(x0 + PW - 60, gy, 0.62, height=420)
    s = 0.5
    b += C.ground_shadow(x0 + 330, gy + 2, s, 140, 0.16) + C.ground_shadow(x0 + 175, gy + 2, s, 120, 0.16)
    b += C.egyptian(x0 + 330, gy, s, 1, kind="guard", pose="lead", expr="neutral")
    b += C.joseph(x0 + 178, gy, s, 1, pose="pray" if pray else "sad", attire="slave",
                  expr="peaceful" if pray else "sad")
    frame, clip = _panel_frame(cx, b, "j14c2", PANELS[1][2])
    return doc(S.g(frame), defs + clip)


def panel_prison(cx, pray=False):
    x0, y0 = cx - PW / 2, PANEL_TOP
    gy = y0 + PH - 58
    defs = S.lin_grad("j14p3", [(0, "#a99a86"), (1, "#8f816f")])
    b = f'<rect x="{x0}" y="{y0}" width="{PW}" height="{PH}" fill="url(#j14p3)"/>'
    rng = random.Random(4)
    for r in range(7):
        for c in range(6):
            xx = x0 + c * 96 + (48 if r % 2 else 0) - 30
            yy = y0 + r * 52
            b += (f'<rect x="{xx}" y="{yy}" width="90" height="46" rx="8" fill="{S.shade("#a99a86", rng.uniform(-0.08, 0.08))}" '
                  f'stroke="{INK}" stroke-width="2" opacity="0.7"/>')
    b += PR.prison_window(x0 + 330, y0 + 100, 0.42, light=0.8, wall=False)
    b += f'<rect x="{x0}" y="{gy}" width="{PW}" height="80" fill="#8a7a64" stroke="{INK}" stroke-width="3"/>'
    for k in range(14):
        xx = x0 + 120 + k * 16
        b += (f'<path d="M{xx},{gy + 6} l{rng.uniform(-14, 14):.0f},{-rng.uniform(8, 18):.0f}" stroke="#d9b45a" '
              f'stroke-width="3"/>')
    s = 0.5
    b += C.ground_shadow(x0 + 200, gy + 2, s, 160, 0.18)
    if pray:
        b += C.joseph(x0 + 200, gy, s, 1, pose="kneel_pray", attire="prisoner", expr="peaceful")
    else:
        b += C.joseph(x0 + 190, gy, s, 1, pose="sit", attire="prisoner", expr="sad")
    frame, clip = _panel_frame(cx, b, "j14c3", PANELS[2][2])
    return doc(S.g(frame), defs + clip)


def panel_glow_svg(cx, tilt):
    x0, y0 = cx - PW / 2, PANEL_TOP
    gid = f"j14g{int(cx)}"
    defs = S.rad_grad(gid, [(0, "#ffe590", 0.95), (0.5, "#ffcf6a", 0.6), (1, "#f7b955", 0.22)], cx=0.62, cy=0.25,
                      r=0.85)
    b = (f'<g transform="rotate({tilt} {cx} {y0}) translate({cx},{y0}) scale({PK}) translate({-cx},{-y0})">'
         f'<rect x="{x0 + 20}" y="{y0 + 20}" width="{PW - 40}" '
         f'height="{PH - 40}" rx="10" fill="url(#{gid})"/>'
         f'<g clip-path="url(#{gid}c)"><path d="{S.rays(x0 + PW - 40, y0 + 10, 30, 520, n=9, width_deg=9, rot=95)}" '
         f'fill="#fff1bf" opacity="0.55" filter="url(#soft)"/></g></g>')
    defs += (f'<clipPath id="{gid}c"><rect x="{x0 + 20}" y="{y0 + 20}" width="{PW - 40}" height="{PH - 40}" '
             f'rx="10"/></clipPath>')
    return doc(b, defs)


# ================================================================== the siblings and the corner picture


def sib(who, x, pose, facing, expr, toy=None):
    return doc(C.ground_shadow(x + 4 * facing, KY + 2, KS, 120 if who == "big" else 100, 0.2) +
               C.child(x, KY, KS, facing, pose=pose, expr=expr, sibling=who, toy=toy))


def hug_svg(expr="happy"):
    out = C.ground_shadow(SIS1 + 70 * KS / 2, KY + 2, KS, 200, 0.2)
    out += C.hug_pair(SIS1, KY, KS, 1, a=(C.child, dict(sibling="big", expr=expr)),
                      b=(C.child, dict(sibling="little", expr=expr)), gap=70)
    return doc(out)


def corner_svg():
    """A framed, warm picture-book corner: Joseph (ruler) hugging his brother Judah, golden light behind them."""
    cx, cy = CORNER
    x0, y0 = cx - CW / 2, cy - CH / 2
    gy = y0 + CH - 46
    defs = (S.lin_grad("j14cs", [(0, "#f9e3b4"), (1, "#f6cf96")]) +
            S.rad_grad("j14cl", [(0, "#fff4cc", 1), (0.5, "#ffe6aa", 0.55), (1, "#ffe6aa", 0)]) +
            f'<clipPath id="j14cc"><rect x="{x0 + 18}" y="{y0 + 18}" width="{CW - 36}" height="{CH - 36}" rx="12"/>'
            f'</clipPath>')
    pic = f'<rect x="{x0}" y="{y0}" width="{CW}" height="{CH}" fill="url(#j14cs)"/>'
    pic += f'<ellipse cx="{cx}" cy="{cy - 40}" rx="230" ry="190" fill="url(#j14cl)"/>'
    pic += f'<rect x="{x0}" y="{gy}" width="{CW}" height="80" fill="#e2c48c"/>'
    pic += PR.egypt_column(x0 + 52, gy, 0.5, height=420) + PR.egypt_column(x0 + CW - 52, gy, 0.5, height=420)
    s = 0.62
    hx = cx - 30 * s
    pic += C.ground_shadow(cx + 10, gy + 2, s, 260, 0.18)
    pic += C.brothers(hx - 150 * s, gy, s * 0.97, 1, variant=0, pose="hug", expr="tearful")
    pic += C.hug_pair(hx, gy, s, 1, a=(C.joseph, dict(attire="ruler", expr="tearful")),
                      b=(C.brothers, dict(variant=3, expr="tearful")))
    b = (f'<rect x="{x0 + 10}" y="{y0 + 14}" width="{CW}" height="{CH}" rx="18" fill="{INK}" opacity="0.25" '
         f'filter="url(#soft)"/>'
         f'<rect x="{x0}" y="{y0}" width="{CW}" height="{CH}" rx="18" fill="#c9924f" stroke="{INK}" stroke-width="5"/>'
         f'<rect x="{x0 + 10}" y="{y0 + 10}" width="{CW - 20}" height="{CH - 20}" rx="14" fill="#f2c45c" '
         f'stroke="{INK}" stroke-width="3"/>')
    b += f'<g clip-path="url(#j14cc)">{pic}</g>'
    b += (f'<rect x="{x0 + 18}" y="{y0 + 18}" width="{CW - 36}" height="{CH - 36}" rx="12" fill="none" '
          f'stroke="{INK}" stroke-width="3"/>')
    return doc(b, defs)


def corner_glow_svg():
    cx, cy = CORNER
    defs = S.rad_grad("j14cg", [(0, "#fff0c0", 0.9), (0.5, "#ffe0a0", 0.4), (1, "#ffe0a0", 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{CW * 0.85}" ry="{CH * 0.95}" fill="url(#j14cg)"/>', defs)


def end_card_svg():
    x, y = END
    defs = S.rad_grad("j14card", [(0, "#fff3d6", 0.85), (0.6, "#ffe9c0", 0.35), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 40}" rx="600" ry="160" fill="url(#j14card)"/>' +
           S.text(x, y, "约瑟和彩衣 · 完", size=100, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=W, H=SH)
    T = ctx.duration
    L = ctx.lines
    m0, m1, m2 = (voice_marks(ctx, i) for i in range(3))

    def ph(m, i, default):
        return m[i] if len(m) > i else (str(i), default, default + 0.8, [(default, default + 0.8)])

    p_sold = ph(m0, 0, L[0].start)
    p_wrong = ph(m0, 1, L[0].start + 1.2)
    p_jail = ph(m0, 2, L[0].start + 2.2)
    p_never = ph(m0, 3, L[0].chunks[1].start if len(L[0].chunks) > 1 else L[0].start + 3.6)
    p_god = ph(m0, 4, L[0].chunks[-1].start)
    t_pan = [char_times(p_sold)[min(2, len(p_sold[0]) - 1)], p_wrong[1],
             char_times(p_jail)[min(1, len(p_jail[0]) - 1)]]
    t_pray = char_times(p_never)[min(2, len(p_never[0]) - 1)]
    t_glow = p_god[1]
    t_kid = ph(m1, 0, L[1].start)[1]
    p_bad = ph(m1, 1, L[1].start + 0.9)
    p_will = ph(m1, 2, L[1].chunks[-1].start)
    t_will = p_will[1]
    p_l2a = ph(m2, 0, L[2].start)
    p_l2b = ph(m2, 1, L[2].start + 1.9)
    p_l2c = ph(m2, 2, L[2].chunks[-1].start)
    p_l2d = ph(m2, 3, L[2].end - 1.0)
    t_good = p_l2b[1]
    t_like = p_l2c[1]
    t_learn = p_l2d[1]
    t_end = max(L[2].end + 0.15, T - 1.3)
    t_still = T - 0.45

    # ---------------------------------------------------------------- room, string, pegs
    sc.add("wall", wall_svg(), z=0)
    sc.add("string", string_svg(), z=1)
    for k in range(3):
        sc.add(f"pegs{k}", empty_pegs_svg(k), z=1.1,
               motion=lambda t, k=k: Tf(alpha=1.0 if t < snap(t_pan[k] - 0.04) + 0.1 else 0.0))

    # ---------------------------------------------------------------- the three panels
    makers = (panel_caravan, panel_guard, panel_prison)
    t_prays = [snap(t_pray + 0.22 * k) for k in range(3)]
    t_glows = [t_glow + 0.25 * k for k in range(3)]
    for k, (cx, _, tilt) in enumerate(PANELS):
        tp = snap(t_pan[k] - 0.04)
        piv = (cx, string_y(cx) + 4)
        frames = [makers[k](cx), makers[k](cx, pray=True)]

        def pmot(t, tp=tp, piv=piv, k=k):
            if t < tp:
                return Tf(alpha=0)
            u = min(1.0, (t - tp) / 0.42)
            s = 0.3 + 0.7 * M.ease("back")(u)
            w = t - tp
            settle = 1 - M.progress(t, t_still - 1.2, t_still, "sine")
            rot = 7 * math.exp(-w * 2.2) * math.sin(2 * math.pi * w / 1.1) + \
                0.8 * math.sin(2 * math.pi * (t / 3.3 + 0.3 * k)) * settle
            return Tf(sx=s, sy=s, rot=rot, alpha=min(1.0, w / 0.08), px=piv[0], py=piv[1])
        tb = t_prays[k]
        bounce = M.keys([(tb - 0.1, {"dy": 0}), (tb + 0.05, {"dy": 6}), (tb + 0.2, {"dy": -6}), (tb + 0.4, {"dy": 0})],
                        ["in", "out", "sine"])
        sc.add(f"panel{k}", frames, z=2 + k * 0.1, frame_at=cuts([(0, 0), (tb, 1)]), seed=20 + 3 * k,
               motion=M.combine(pmot, bounce))
        tg = t_glows[k]

        def gmot(t, tg=tg, pm=pmot, b=bounce, k=k):
            base = M.combine(pm, b)(t)
            a = M.progress(t, tg, tg + 0.7, "sine") * (0.75 + 0.25 * math.sin(2 * math.pi * (t / 2.2 + 0.3 * k)))
            return Tf(base.dx, base.dy, base.rot, base.sx, base.sy, base.alpha * a, base.px, base.py)
        sc.add(f"panel_glow{k}", panel_glow_svg(cx, tilt), z=2.05 + k * 0.1, wc=0, blend="screen", motion=gmot)
        sc.fx.append(FX.sparkles((cx - PK * PW / 2 + 40, PANEL_TOP + 40, cx + PK * PW / 2 - 40, PANEL_TOP + PK * PH - 60), count=7,
                                 t0=tg, t1=t_kid + 1.2, size=(9, 17), period=1.4, drift=-10, seed=30 + k))

    # ---------------------------------------------------------------- the siblings
    t_walk = snap(p_l2a[1] + 0.05)
    nsteps, period = 2, 0.3
    step = (SIS_SORRY - SIS0) / nsteps
    cut_t = [snap(t_walk + i * period) for i in range(nsteps)]
    t_walk_end = snap(t_walk + nsteps * period)
    t_sorry = snap(max(t_walk_end + 0.05, char_times(p_l2a)[min(5, len(p_l2a[0]) - 1)] - 0.1))
    t_hug = snap(t_good - 0.02)
    t_share = snap(t_learn - 0.05)
    t_peek = snap(t_will + 0.1)
    t_peek_end = snap(t_peek + 1.6)

    bnames = ["hold", "hold_b", "hold_w", "walk_a", "walk_b", "sorry", "sorry_b", "share", "share_b"]
    bfr = [sib("big", SIS0, "stand", 1, "sly", "horse"), sib("big", SIS0, "stand", 1, blink_name("neutral"), "horse"),
           sib("big", SIS0, "stand", 1, "worried", "horse"),
           sib("big", SIS0, "walk_a", 1, "sorry", "horse"), sib("big", SIS0, "walk_b", 1, "sorry", "horse"),
           sib("big", SIS_SORRY, "sorry", 1, "sorry"), sib("big", SIS_SORRY, "sorry", 1, blink_name("sorry")),
           sib("big", SIS1 - 40, "share", 1, "happy", "horse"),
           sib("big", SIS1 - 40, "share", 1, blink_name("happy"), "horse")]
    BI = {n: i for i, n in enumerate(bnames)}
    bents = [(0, BI["hold"]), (snap(p_bad[1] + 0.3), BI["hold_w"]), (t_sorry, BI["sorry"]), (t_share, BI["share"])]
    for tb, base, bl in ((t_kid + 0.9, "hold", "hold_b"), (t_will + 1.5, "hold_w", "hold_b"),
                         (t_will + 2.9, "hold_w", "hold_b"), (t_sorry + 0.8, "sorry", "sorry_b"),
                         (t_share + 0.9, "share", "share_b")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in bents) and not (t_walk - 0.2 < tb < t_walk_end + 0.2):
            bents += [(tb, BI[bl]), (snap(tb + 0.13), BI[base])]
    bents.sort()
    bfa0 = cuts(bents)

    def big_fa(t):
        if t_walk <= t < t_walk_end:
            return float(BI["walk_a"] + min(nsteps - 1, int((t - t_walk) / period)) % 2)
        return bfa0(t)

    def big_x(t):
        x = 0.0
        for tc in cut_t:
            x += step * M.progress(t, tc - 0.07, tc + 0.08, "sine")
        if t >= t_walk_end:      # drawings after the walk are placed at SIS1 themselves
            return 0.0 if t >= t_sorry else x
        return x

    def big_m(t):
        hide = t_hug <= t < t_share
        dy = 0.0
        for tc in cut_t:
            if tc - 0.07 <= t <= tc + 0.08:
                dy -= 5 * KS * math.sin(math.pi * (t - tc + 0.07) / 0.15)
        return Tf(dx=big_x(t), dy=dy, alpha=0.0 if hide else 1.0)
    sc.add("big", bfr, z=10, frame_at=big_fa, seed=51,
           motion=M.combine(big_m, dip(t_sorry, KS, (SIS_SORRY, KY), 7), dip(t_share, KS, (SIS1, KY), 7),
                            M.breathe(0.011, 2.6, pivot=(SIS1, KY))))

    lnames = ["sulk", "sulk_b", "sulk_sad", "peek", "laugh", "laugh_b"]
    lfr = [sib("little", BRO, "sulk", -1, "cross"), sib("little", BRO, "sulk", -1, blink_name("cross")),
           sib("little", BRO, "sulk", -1, "sad"), sib("little", BRO, "sulk", 1, "sad"),
           sib("little", BRO, "stand", -1, "laugh"), sib("little", BRO, "stand", -1, blink_name("happy"))]
    LI = {n: i for i, n in enumerate(lnames)}
    lents = [(0, LI["sulk"]), (snap(p_bad[1] + 0.2), LI["sulk_sad"]), (t_peek, LI["peek"]),
             (t_peek_end, LI["sulk_sad"]), (t_share, LI["laugh"])]
    for tb, base, bl in ((t_kid + 0.4, "sulk", "sulk_b"), (t_will + 2.6, "sulk_sad", "sulk_b"),
                         (t_share + 1.2, "laugh", "laugh_b")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in lents):
            lents += [(tb, LI[bl]), (snap(tb + 0.13), LI[base])]
    lents.sort()

    def little_m(t):
        hide = t_hug <= t < t_share
        r = 0.0
        if t < t_hug:
            r = 1.4 * math.sin(2 * math.pi * t / 1.7)
        return Tf(rot=r, alpha=0.0 if hide else 1.0, px=BRO, py=KY)
    sc.add("little", lfr, z=11, frame_at=cuts(lents), seed=57,
           motion=M.combine(little_m, dip(t_peek, KS, (BRO, KY), 6), dip(t_peek_end, KS, (BRO, KY), 6),
                            dip(t_share, KS, (BRO, KY), 7), M.breathe(0.013, 2.3, pivot=(BRO, KY), phase=0.4)))
    hpiv = (SIS1 + 35 * KS, KY)
    sc.add("hug", [hug_svg("happy"), hug_svg(blink_name("happy"))], z=12, seed=61,
           frame_at=lambda t: 1.0 if snap(t_like + 0.6) <= t < snap(t_like + 0.73) else 0.0,
           motion=M.combine(lambda t: Tf(alpha=1.0 if t_hug <= t < t_share else 0.0), dip(t_hug, KS, hpiv, 8),
                            lambda t: Tf(rot=1.6 * math.sin(2 * math.pi * (t - t_hug) / 1.4) if t > t_hug + 0.3 else 0,
                                         px=hpiv[0], py=hpiv[1])))

    # the storm cloud: drizzling over him; on the hug it turns into a smiling sunny cloud and floats off
    cx_, cy_ = CLOUD
    cfr = [Q.storm_cloud_svg(cx_, cy_, k, w=W, h=SH) for k in range(3)] + [Q.storm_cloud_svg(cx_, cy_, 0, w=W, h=SH,
                                                                                            sun=1.0)]

    def cloud_fa(t):
        if t >= t_hug:
            return 3.0
        return float(int(t / 0.12) % 3)

    def cloud_m(t):
        u = t - t_hug
        dy = 4 * math.sin(2 * math.pi * t / 1.8)
        dx = 0.0
        a = 1.0
        s = 1.0
        if u >= 0:
            s = 1 + 0.15 * math.sin(math.pi * min(1.0, u / 0.3))
            dy -= 120 * M.progress(t, t_hug + 0.6, t_hug + 2.4, "inout")
            dx = 160 * M.progress(t, t_hug + 0.6, t_hug + 2.4, "inout")
            a = 1 - M.progress(t, t_hug + 1.6, t_hug + 2.4, "sine")
        return Tf(dx=dx, dy=dy, sx=s, sy=s, alpha=a, px=cx_, py=cy_)
    sc.add("cloud", cfr, z=13, frame_at=cloud_fa, motion=cloud_m, wc=0.5)
    sc.fx.append(FX.sparkles((cx_ - 140, cy_ - 80, cx_ + 140, cy_ + 60), count=8, t0=t_hug, t1=t_hug + 1.6,
                             size=(10, 20), period=0.9, drift=-20, seed=71))
    # two little hearts over the hug
    for i, (dx, r, d) in enumerate(((-30, 26, 0.0), (70, 20, 0.25))):
        hx, hy = SIS1 + 70 * KS / 2 + dx, KY - 520 - 30 * i
        th = snap(t_hug + 0.25 + d)

        def hm(t, th=th, hx=hx, hy=hy, i=i):
            if t < th:
                return Tf(alpha=0)
            u = min(1.0, (t - th) / 0.4)
            s = 0.2 + 0.8 * M.ease("back")(u)
            a = 1 - M.progress(t, t_share - 0.4, t_share, "sine")
            return Tf(sx=s, sy=s, dy=-10 * math.sin(2 * math.pi * ((t - th) / 2.0 + 0.3 * i)) - 20 * (1 - a),
                      alpha=a, px=hx, py=hy)
        sc.add(f"heart{i}", doc(heart_markup(hx, hy, r)), z=14 + i * 0.01, wc=0, motion=hm)

    # the warm corner picture (Joseph hugging his brothers)
    ccx, ccy = CORNER
    t_corner = snap(t_like - 0.05)
    sc.add("corner_glow", corner_glow_svg(), z=15, wc=0, blend="screen",
           motion=M.combine(lambda t: Tf(alpha=M.progress(t, t_corner, t_corner + 0.8, "sine") *
                                         (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.4))),
                            M.breathe(0.03, 2.4, pivot=(ccx, ccy))))
    sc.add("corner", corner_svg(), z=15.1, seed=81, motion=M.keys(
        [(t_corner, {"alpha": 0, "s": 0.5, "rot": -4}), (t_corner + 0.12, {"alpha": 1}),
         (t_corner + 0.5, {"s": 1.0, "rot": -1.5})], ["out", "back"], pivot=(ccx, ccy)))
    sc.fx.append(FX.sparkles((ccx - CW / 2, ccy - CH / 2, ccx + CW / 2, ccy + CH / 2), count=8, t0=t_corner + 0.2,
                             t1=t_end + 0.6, size=(9, 17), period=1.5, drift=-8, seed=83))

    # ---------------------------------------------------------------- end card and heart
    ex, ey = END
    sc.add("endcard", end_card_svg(), z=20, wc=0, motion=M.keys(
        [(t_end, {"alpha": 0, "s": 0.95, "dy": 16}), (t_end + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    hx, hy = ex, ey + 74
    th = t_end + 0.45
    sc.add("endheart", doc(heart_markup(hx, hy, 30)), z=20.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))
    sc.fx.append(FX.sparkles((ex - 420, ey - 120, ex + 420, ey + 40), count=6, t0=t_end + 0.4, size=(9, 16),
                             period=2.0, drift=0, seed=87))
    sc.fx.append(FX.motes((200, 120, 1900, 1500), count=24, color=(255, 244, 210), seed=89, alpha=90))

    # ---------------------------------------------------------------- camera: down the wall to the siblings
    c_wall0 = Cam(W / 2, 560, W * 0.96)
    c_wall1 = Cam(W / 2, 548, W * 0.92)
    c_kids = Cam(1010, OY + 676, 1760)
    t_down0 = max(L[0].end + 0.2, t_kid - 0.35)
    sc.camera = M.cam_keys([(0, c_wall0), (t_down0, c_wall1), (t_down0 + 1.6, c_kids),
                            (t_hug, Cam(1022, OY + 668, 1700)), (t_end, Cam(1040, OY + 660, 1740)),
                            (T, Cam(1040, OY + 658, 1720))], ["sine", "inout", "sine", "sine", "sine"])

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T, gain_db=-21, fade_in=0.8, fade_out=1.5)
    for k, tp in enumerate(t_pan):
        sc.sfx("pop", tp - 0.04, gain_db=-12, pan=-0.6 + 0.6 * k)
    sc.sfx("chime", t_glow, gain_db=-12)
    sc.sfx("sparkle", t_glow + 0.4, gain_db=-16)
    sc.sfx("whoosh", t_down0 + 0.2, gain_db=-20)
    sc.sfx("rain", t_down0, dur=t_hug - t_down0 + 0.2, gain_db=-29, fade_in=0.8, fade_out=0.4)
    sc.sfx("footsteps", t_walk, dur=t_walk_end - t_walk + 0.05, gain_db=-18, pan=-0.1)
    sc.sfx("sparkle", t_hug + 0.05, gain_db=-13)
    sc.sfx("pop", t_hug + 0.25, gain_db=-15)
    sc.sfx("chime", t_corner + 0.05, gain_db=-14, pan=-0.5)
    sc.sfx("sparkle", t_share, gain_db=-16)
    sc.sfx("chime", t_end + 0.1, gain_db=-12)
    return sc
