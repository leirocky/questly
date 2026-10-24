"""Scene 4 - Mark 6:35-37, John 6:5-7. The sun sinks over the lake; everyone's tummy rumbles; the disciples come to
Jesus, worried: send the people to the villages to buy food. Jesus: "You give them something to eat." They are amazed;
Jesus asks Philip where they could buy bread (he already knows what he will do); Philip counts on his fingers, shakes
his head: even a lot of money would not buy everyone a mouthful.

The hillside world of s03 (imported from s03_crowd: the same stage, layers, seeds, people and global-clock motion), so
the plain 1 s cross-dissolve from s03 starts on exactly s03's last frame. The page dip into s05 (another illustrator)
ends on a calm frame: Jesus smiling, Philip with his hands spread, the golden hillside.

Beats (syllable onsets measured in the voice clips through the Nativity film's Tm; nothing hard-coded to the take):
  0 .. 1.0     identical to the end of s03 (the healed man with his crutch up, the child laughing in her lap)
  '天快黑了'     the camera eases back to the whole hillside; the sun sinks toward the far hills and the light turns
               golden (sky, lake and grass cross-fade from time .4 to .55); the healed man walks off home, his crutch on
               his shoulder
  '肚子'         the family at the front look down at their tummies; on each 咕 / 噜 a tummy wobbles and a rumble mark
               pops (the man, the mother, the boy, the girl; little marks over the groups too); the children pat their
               tummies, sad and hungry (a gurgle)
  '门徒们来'     the five disciples walk over to Jesus (planted strides); he turns to them
  line 1       worried: Peter talks ('这里什么吃的都没有'), James talks on '天也晚了', John points across the lake to
               the villages on '附近的村子', Andrew talks on '自己买东西吃吧'
  '你们给他们吃吧' Jesus calmly opens his hands
  '吓了一跳'     the disciples jump (hands at their cheeks, two '!' marks)
  '耶稣又问腓力'  the camera moves to Jesus and Philip; Jesus turns to him and asks; Philip looks up, surprised
  line 5       close on Jesus: a gentle knowing smile; '早就知道' a soft warm glow; Philip ponders
  '掰着手指'     Philip counts on his fingers (one, two, three) through '算了算'; '摇摇头' he shakes his head
  line 7       a picture-book card: a heap of coins that grows on '好多好多钱' -> an arrow -> a crowd of little people,
               each with only a tiny crumb (they pop on '每个人', the crumbs on '一小口'); Philip spreads his hands
  end          the card fades; a calm hold for the page turn
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.loaves.scenes.s03_crowd import (
    CAM_F_END, CREAM, DISC_F, FAMILY, FAMILY_Y, H, H_TIME, JK, LAME, LAME_V, RX, RY, SEED_H, W, Z_H, Actor, Loop, add_f_people,
    add_groups, add_hill, add_sun, blink, breathm, cam_keys, disc, doc, env, f1, f_end_keys, folk, gate, hk, hopm, jes, mark_svg,
    popm, shadow, warm_glow_svg)
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import snap

INK = P["ink"]
T_END = 0.55                            # the golden hour the light reaches
SUN_DROP = (30.0, 80.0)                # how far the sun sinks (px)
# where the disciples stop in front of Jesus (Philip nearest: 170 px at his scale, as the Philip-counting composition)
DISC_TALK = {"p4": RX + 170 * JK, "p0": RX + 320 * JK, "p1": RX + 460 * JK, "p2": RX + 600 * JK, "p3": RX + 740 * JK}
CARD = (1640, 560)                      # the coins-and-crumbs card
CARD_W, CARD_H = 600, 330


# ================================================================== drawings
def crutch_walker_markup(x, y, s, key):
    """The healed man walking home (kind='man', the same variant) with his crutch resting on his near shoulder."""
    pose, expr, f = key[0], key[1], key[2]
    body = folk(x, y, s, f, kind="man", v=LAME_V, pose=pose, expr=expr)
    sh = C.body_points(C.galilee_folk, x, y, s, f, kind="man", variant=LAME_V, pose=pose)["shoulders"][1]
    a = (sh[0] + f * 52 * s, sh[1] + 96 * s)
    b = (sh[0] - f * 92 * s, sh[1] - 118 * s)
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    c = (f"M{f1(a[0])},{f1(a[1])} L{f1(b[0])},{f1(b[1])}")
    out = (f'<path d="{c}" stroke="{INK}" stroke-width="{f1(13 * s)}" stroke-linecap="round" fill="none"/>'
           f'<path d="{c}" stroke="#a8744a" stroke-width="{f1(8 * s)}" stroke-linecap="round" fill="none"/>')
    cp = (f"M{f1(b[0] + nx * 15 * s)},{f1(b[1] + ny * 15 * s)} L{f1(b[0] - nx * 15 * s)},{f1(b[1] - ny * 15 * s)}")
    out += (f'<path d="{cp}" stroke="{INK}" stroke-width="{f1(14 * s)}" stroke-linecap="round" fill="none"/>'
            f'<path d="{cp}" stroke="#c9a46a" stroke-width="{f1(9 * s)}" stroke-linecap="round" fill="none"/>')
    return shadow(x, y, s, 100, 0.15) + body + S.g(out, filter="wobble-fine")


def rumble_svg(x, y, k=1.0, col="#b8643c"):
    """A tummy-rumble mark: three little wobbly arcs."""
    out = ""
    for j, (dx, dy, r) in enumerate(((0, 0, 1.0), (16 * k, -14 * k, 0.8), (-14 * k, -16 * k, 0.7))):
        rr = 16 * k * r
        out += (f'<path d="M{f1(x + dx - rr)},{f1(y + dy)} q{f1(rr * 0.5)},{f1(-rr * 0.7)} {f1(rr)},0 t{f1(rr)},0" fill="none" '
                f'stroke="{col}" stroke-width="{f1(4.2 * k)}" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def card_svg(stage, n_coins=0, n_people=0, crumbs=False):
    """The picture-book card: a heap of coins -> an arrow -> a crowd of little people, each with a tiny crumb."""
    cx, cy = CARD
    w, h = CARD_W, CARD_H
    x0, y0 = cx - w / 2, cy - h / 2
    b = PR._p(f"M{f1(x0 + 20)},{f1(y0)} L{f1(x0 + w - 20)},{f1(y0 + 2)} Q{f1(x0 + w)},{f1(y0 + 2)} {f1(x0 + w - 2)},{f1(y0 + 22)} "
              f"L{f1(x0 + w + 2)},{f1(y0 + h - 20)} Q{f1(x0 + w)},{f1(y0 + h)} {f1(x0 + w - 22)},{f1(y0 + h - 2)} L{f1(x0 + 20)},{f1(y0 + h)} "
              f"Q{f1(x0)},{f1(y0 + h)} {f1(x0 + 2)},{f1(y0 + h - 20)} L{f1(x0)},{f1(y0 + 22)} Q{f1(x0)},{f1(y0)} {f1(x0 + 20)},{f1(y0)} Z",
              "#fbf3e0", 4.5)
    b += PR._p(f"M{f1(x0 + 14)},{f1(y0 + 14)} L{f1(x0 + w - 14)},{f1(y0 + 14)} L{f1(x0 + w - 14)},{f1(y0 + h - 14)} "
               f"L{f1(x0 + 14)},{f1(y0 + h - 14)} Z", sw=2.2, stroke="#d9c095")
    art = ""
    if n_coins > 0:
        art += PR.coin_pile(x0 + 140, cy + 92, 1.7 + 0.03 * n_coins, n=n_coins, style="heap", seed=4)
    if stage >= 1:   # the arrow
        ax0, ax1, ay = x0 + 250, x0 + 330, cy + 10
        art += PR._p(f"M{f1(ax0)},{f1(ay)} Q{f1((ax0 + ax1) / 2)},{f1(ay - 16)} {f1(ax1)},{f1(ay)}", sw=7, stroke="#c8643c")
        art += PR._p(f"M{f1(ax1 - 18)},{f1(ay - 16)} L{f1(ax1 + 4)},{f1(ay)} L{f1(ax1 - 20)},{f1(ay + 12)}", sw=7, stroke="#c8643c")
    rng = random.Random(9)
    cols = ["#d9707a", "#e8a53a", "#4f9ec8", "#9a78c0", "#c0603e", "#eadfc4"]
    hairs = ["#2f2219", "#4a2f1f", "#241a15", "#ece6da", "#3a2618"]
    k = 0
    for row in range(3):
        for j in range(5 - (row % 2)):
            if k >= n_people:
                break
            px = x0 + 385 + j * 44 + (row % 2) * 22 + rng.uniform(-4, 4)
            py = cy - 70 + row * 62
            art += PR._ell(px, py + 26, 19, 14, cols[(k * 5 + row) % 6], 2.6)
            art += PR._circ(px, py, 15, "#e2ad85" if k % 3 else "#c48a62", 2.6)
            art += PR._p(f"M{f1(px - 15)},{f1(py - 2)} Q{f1(px - 14)},{f1(py - 19)} {f1(px)},{f1(py - 18)} Q{f1(px + 14)},{f1(py - 17)} {f1(px + 15)},{f1(py - 4)} "
                         f"Q{f1(px)},{f1(py - 10)} {f1(px - 15)},{f1(py - 2)} Z", hairs[k % 5], 2.0)
            art += PR._circ(px + 6, py - 1, 2.0, "#2e2630", 0)
            if crumbs:
                art += PR._p(f"M{f1(px + 1)},{f1(py + 8)} q5,-3 10,0", sw=2.0)
                art += PR._circ(px + 17, py + 9, 5.0, "#e8b864", 1.8) + PR._circ(px + 15.5, py + 7.5, 1.6, "#fff2c4", 0)
            else:
                art += PR._p(f"M{f1(px + 1)},{f1(py + 7)} q5,3 10,0", sw=2.0)
            k += 1
    return doc(S.g(b, filter="wobble") + S.g(art, filter="wobble-fine"))


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    L = ctx.lines
    g_all = gate(-1, 1e9)

    # ---- beats
    t_tian = tm.at(0, "天快黑了", 0)
    t_duzi = tm.at(0, "大家的肚子", 3)
    gulu = [tm.at(0, "咕噜咕噜叫", k) for k in range(4)]
    t_men = tm.at(0, "门徒们来对耶稣说", 0)
    t_lai = tm.at(0, "门徒们来对耶稣说", 3)
    t_zheli = tm.at(1, "这里什么吃的都没有", 0)
    t_wan = tm.at(1, "天也晚了", 0)
    t_fujin = tm.at(1, "让大家到附近的村子里", 4)
    t_ziji = tm.at(1, "自己买东西吃吧", 0)
    t_ni = tm.at(2, "你们给他们吃吧", 0)
    t_xia = tm.at(3, "门徒们吓了一跳", 3)
    t_wen = tm.at(3, "耶稣又问腓力", 2)
    t_feili = tm.at(3, "耶稣又问腓力", 4)
    t_zhe = tm.at(5, "耶稣这样问", 0)
    t_qishi = tm.at(5, "其实", 0)
    t_zhidao = tm.at(5, "耶稣自己早就知道要怎么做了", 6)
    t_bai = tm.at(6, "腓力掰着手指算了算", 2)
    t_suan = tm.at(6, "腓力掰着手指算了算", 6)
    t_yao = tm.at(6, "摇摇头说", 0)
    t_jiusuan = tm.at(7, "就算花好多好多钱买饼", 0)
    t_hua = tm.at(7, "就算花好多好多钱买饼", 2)
    t_duo1 = tm.at(7, "就算花好多好多钱买饼", 3)
    t_duo2 = tm.at(7, "就算花好多好多钱买饼", 5)
    t_ye = tm.at(7, "也不够每个人吃一小口啊", 0)
    t_mei = tm.at(7, "也不够每个人吃一小口啊", 3)
    t_xiao = tm.at(7, "也不够每个人吃一小口啊", 8)
    t_a = tm.at(7, "也不够每个人吃一小口啊", 10)

    # ---- the hillside: the light turns golden, the sun sinks
    t_l0 = max(1.0, t_tian)                       # nothing moves during the dissolve from s03
    u_light = lambda t: M.progress(t, t_l0, t_l0 + 2.6, "sine")   # noqa: E731
    sun_pos = lambda t: (SUN_DROP[0] * M.progress(t, t_l0, t_l0 + 3.0, "sine"),   # noqa: E731
                         SUN_DROP[1] * M.progress(t, t_l0, t_l0 + 3.0, "sine"))
    add_hill(sc, g_all, g0, times=(H_TIME, T_END), u=u_light)
    add_sun(sc, g_all, times=(H_TIME, T_END), u=u_light, pos=sun_pos)
    add_groups(sc, g_all, g0)

    # ---- the people (they start exactly as s03 ends)
    acts = add_f_people(sc, g_all, g0, Z_H + 6.5)
    ek = f_end_keys()
    for nm, a in acts.items():
        a.cut(0, ek[nm])

    # the healed man walks home with his crutch on his shoulder
    t_go = snap(t_tian + 0.45)
    lx, ly = LAME[0] - 62 * JK, LAME[1]
    acts["lame"].gatef = gate(-1, t_go)
    acts["lame"].dips.append((t_go, 5))
    walker = Actor("walker", (lx, ly), JK, lambda k: crutch_walker_markup(lx, ly, JK, k), Z_H + 6.5 + ly / 10000.0 + 0.00001,
                   SEED_H + 400, g0, gate(t_go, 1e9))
    walker.cut(0, ("walk_a", "joyful", -1))
    n_steps = 12
    walker.walk(t_go, [(("walk_a", "joyful", -1), 86), (("walk_b", "joyful", -1), 86)], n_steps, 0.25, -1)
    walker.dips.append((t_go, 5))
    walker.extra.append(breathm(g0, 3.0, 0.010))
    walker.build(sc)
    sc.sfx("footsteps", t_go, dur=n_steps * 0.25, gain_db=-24, pan=-0.5)

    # the hungry family: look down at their tummies, rumbles, the children pat their tummies
    fam_react = [("sit", "worried"), ("sit", "worried"), ("sit_pat_tummy", "sad"), ("sit_pat_tummy", "sad"), ("sit", "tired")]
    rumble_who = [0, 1, 2, 3]
    for j in range(len(FAMILY)):
        a = acts[f"fam{j}"]
        t_look = snap(t_duzi - 0.1 + 0.06 * j)
        pose, expr = fam_react[j]
        if pose == "sit_pat_tummy":
            a.loop(snap(gulu[0] + 0.25 + 0.1 * j), [(pose, expr, ph) for ph in (0.0, 0.5)], 0.22, dip=4)
            a.cut(t_look, ("sit", "worried"), dip=3)
            a.cut(snap(t_lai + 0.6 + 0.2 * j), ("sit", "sad"), dip=3)
        else:
            a.cut(t_look, (pose, expr), dip=3)
            a.cut(snap(t_lai + 0.9 + 0.15 * j), ("sit_listen" if j % 2 == 0 else "sit", "tired"), dip=3)
    for q, j in enumerate(rumble_who):
        kind, v, x, dy = FAMILY[j]
        y = FAMILY_Y + dy
        s_ = hk(y)
        tg = gulu[q]
        acts[f"fam{j}"].extra.append(lambda t, tg=tg: Tf(sx=1 + 0.06 * math.sin(math.pi * min(1.0, max(0.0, (t - tg) / 0.3))),
                                                         sy=1 - 0.04 * math.sin(math.pi * min(1.0, max(0.0, (t - tg) / 0.3)))))
        tx, ty = x + 30 * s_, y - 50 * s_
        sc.add(f"rumble{q}", rumble_svg(tx, ty, 1.35 * s_), z=Z_H + 7.5, wc=0.2, seed=SEED_H + 410 + q,
               motion=popm(snap(tg), (tx, ty), 0.2, t_out=snap(tg + 0.85), out_dur=0.25))
    for q, (gx, gy) in enumerate(((560, 900), (2150, 860), (2380, 1010), (1290, 790), (180, 830))):
        tg = gulu[q % 4] + 0.05
        sc.add(f"grumble{q}", rumble_svg(gx, gy, 1.1), z=Z_H + 7.4, wc=0.2, seed=SEED_H + 420 + q,
               motion=popm(snap(tg), (gx, gy), 0.2, t_out=snap(tg + 0.7), out_dur=0.25))
    sc.sfx("bubbles", gulu[0] - 0.05, dur=1.0, gain_db=-20, fade_in=0.05, fade_out=0.3)

    # the mother and her healed child stay, the child bouncing now and then
    acts["mother"].extra.append(hopm(5.2, hk(acts["mother"].hy), 6, 0.22))

    # ---- the disciples walk over to Jesus; their talk; amazement; Philip
    order = ["p4", "p0", "p1", "p2", "p3"]
    var = {nm: v for nm, v, x, y in DISC_F}
    xs = {nm: x for nm, v, x, y in DISC_F}
    t_arrive = {}
    for i, nm in enumerate(order):
        a = acts[nm]
        dist = xs[nm] - DISC_TALK[nm]
        n = 4
        t0 = snap(t_men + 0.02 + 0.07 * i)
        adv = dist / n / a.s
        exp = "worried" if i % 2 == 0 else "concerned"
        a.cut(snap(t0 - 0.02), ("stand", exp, -1), dip=3)
        a.walk(t0, [(("walk_a", exp, -1), adv), (("walk_b", exp, -1), adv)], n, 0.27, -1)
        t_arrive[nm] = snap(t0 + n * 0.27)
        a.cut(t_arrive[nm], ("worried", "worried", -1), dip=4)
    sc.sfx("footsteps", t_men, dur=1.4, gain_db=-20)
    # their lines
    acts["p0"].cut(snap(t_zheli - 0.05), ("talk", "concerned", -1), dip=3)
    acts["p2"].cut(snap(t_wan - 0.05), ("talk", "concerned", -1), dip=3)
    acts["p0"].cut(snap(t_wan + 0.2), ("worried", "worried", -1), dip=3)
    acts["p3"].cut(snap(t_fujin - 0.15), ("point", "concerned", 1), dip=4)
    acts["p2"].cut(snap(t_fujin + 0.1), ("worried", "worried", -1), dip=3)
    acts["p1"].cut(snap(t_ziji - 0.05), ("talk", "concerned", -1), dip=3)
    acts["p3"].cut(snap(t_ziji + 0.3), ("worried", "worried", -1), dip=3)
    # '你们给他们吃吧': they listen; '吓了一跳': amazed, a jump
    for i, nm in enumerate(order):
        acts[nm].cut(snap(t_ni + 0.1 + 0.05 * i), ("stand", "surprised", -1), dip=2)
        t_j = snap(t_xia - 0.06 + 0.04 * i)
        acts[nm].cut(t_j, ("amazed", "amazed", -1), dip=None)
        acts[nm].extra.append(hopm(t_j + 0.02, acts[nm].s, 24, 0.3))
        if nm != "p4":
            acts[nm].cut(snap(t_feili + 0.4 + 0.08 * i), ("worried", "worried", -1), dip=3)
    for j, nm in enumerate(("p0", "p2")):
        a = acts[nm]
        x, y = DISC_TALK[nm], a.hy
        hx_, hy_ = x - 10, y - 380 * a.s
        sc.add(f"ex{j}", mark_svg(hx_, hy_, "!", 74), z=Z_H + 7.6, wc=0.0, seed=SEED_H + 430 + j,
               motion=popm(snap(t_xia + 0.05 * j), (hx_, hy_ - 20), 0.22, t_out=snap(t_xia + 1.3), out_dur=0.25))
    sc.sfx("pop", t_xia, gain_db=-14)
    sc.sfx("whoosh", t_xia - 0.05, gain_db=-22)
    # Philip: surprised to be asked; worried; ponders; counts; shakes his head; spreads his hands
    ph = acts["p4"]
    ph.cut(snap(t_feili + 0.05), ("stand", "surprised", -1), dip=4)
    ph.cut(snap(L[4].start + 0.4), ("worried", "concerned", -1), dip=3)
    ph.cut(snap(t_zhe + 0.3), ("stand", "ponder", -1), dip=3)
    t_c0 = snap(t_bai - 0.05)
    t_c1 = snap(t_yao - 0.08)
    ph.loop(t_c0, [("count_fingers", "count", -1, p_) for p_ in (0.0, 0.34, 0.67)], 0.36, phase=0.0, dip=3)
    ph.loop(t_c1, [("shake_head", "doubtful", -1, p_) for p_ in (0.0, 0.25, 0.5, 0.75)], 0.13, dip=4)
    ph.cut(snap(t_c1 + 0.95), ("talk", "doubtful", -1), dip=3)
    t_spread = snap(t_ye - 0.05)
    ph.cut(t_spread, ("shake_head", "doubtful", -1, 0.0), dip=4)
    ph.loop(snap(t_mei), [("shake_head", "doubtful", -1, p_) for p_ in (0.0, 0.25, 0.5, 0.75)], 0.13)
    ph.cut(snap(t_a - 0.1), ("shake_head", "doubtful", -1, 0.5, False), dip=3)
    for nm in order:
        acts[nm].blinks([t_arrive[nm] + 2.0, t_ni - 0.6, 24.0 + 0.3 * order.index(nm), 28.5 + 0.4 * order.index(nm), 31.6],
                        {("worried", "worried", -1): ("worried", blink("worried"), -1),
                         ("stand", "ponder", -1): ("stand", blink("ponder"), -1)})

    # ---- Jesus: turns to his friends, answers, asks Philip, smiles knowingly
    j_ = acts["jesus"]
    j_.cut(snap(t_men + 0.4), ("stand", "warm", 1), dip=3)
    j_.cut(snap(t_zheli + 0.4), ("stand", "kind", 1), dip=2)
    j_.cut(snap(t_ni - 0.12), ("open_hands", "kind", 1), dip=3)
    j_.cut(snap(t_xia + 0.3), ("stand", "smile", 1), dip=2)
    j_.cut(snap(t_wen - 0.1), ("ask", "gentle_question", 1), dip=3)
    j_.cut(snap(t_zhe - 0.05), ("look_kind", "kind", 1), dip=3)
    j_.cut(snap(t_qishi), ("look_kind", "smile", 1), dip=2)
    j_.cut(snap(t_bai - 0.2), ("stand", "kind", 1), dip=2)
    j_.cut(snap(t_a + 0.15), ("stand", "smile", 1), dip=2)
    j_.blinks([8.6, 11.9, 13.6, 17.0, 23.4, 27.3, 35.0, 39.0, 41.5],
              {("stand", "kind", 1): ("stand", blink("kind"), 1), ("look_kind", "kind", 1): ("look_kind", blink("kind"), 1),
               ("stand", "warm", 1): ("stand", blink("warm"), 1)})
    # a soft warm light on '早就知道'
    hx_, hy_ = RX + 10 * JK, RY - 250 * JK
    sc.add("j_glow", warm_glow_svg(hx_, hy_, 260 * JK, 300 * JK, "#ffd88a", 0.5, "j4"), z=Z_H + 6.49, wc=0.0, seed=SEED_H + 440,
           blend="screen", motion=lambda t: Tf(alpha=env(t, t_zhidao - 0.6, t_zhidao + 2.0, 0.7, 1.0)))
    sc.sfx("chime", t_zhidao - 0.3, gain_db=-20)

    for nm, a in acts.items():
        a.build(sc)

    # ---- the card: coins -> arrow -> little people with tiny crumbs
    t_card = snap(t_hua - 0.1)
    t_card_out = snap(min(T - 0.6, t_a + 0.9))
    stages = [(t_card, (0, 6, 0, False)), (snap(t_duo1), (0, 12, 0, False)), (snap(t_duo2), (0, 20, 0, False)),
              (snap(t_ye - 0.05), (1, 20, 0, False))]
    for q in range(14):
        stages.append((snap(t_mei - 0.1 + 0.07 * q), (1, 20, q + 1, False)))
    stages.append((snap(t_xiao - 0.05), (1, 20, 14, True)))
    keys = []
    for _, kk in stages:
        if kk not in keys:
            keys.append(kk)
    frames = [card_svg(k[0], k[1], k[2], k[3]) for k in keys]
    idx = {k: i for i, k in enumerate(keys)}

    def card_fa(t):
        cur = stages[0][1]
        for ts, kk in stages:
            if t >= ts:
                cur = kk
        return float(idx[cur])
    sc.add("card", frames, z=Z_H + 8.0, wc=0.4, seed=SEED_H + 450, frame_at=card_fa,
           motion=popm(t_card, (CARD[0] - 200, CARD[1] + 180), 0.35, t_out=t_card_out, out_dur=0.4, wob=False))
    sc.sfx("pop", t_card, gain_db=-14)
    sc.sfx("coins", t_duo1 - 0.02, gain_db=-14)
    sc.sfx("coins", t_duo2 - 0.02, gain_db=-12)
    for q in range(0, 14, 3):
        sc.sfx("pop", t_mei - 0.1 + 0.07 * q, gain_db=-24)
    sc.sfx("sparkle", t_xiao - 0.05, gain_db=-20)

    # ---- camera
    cam = cam_keys([(0, CAM_F_END), (t_l0, CAM_F_END), (t_duzi - 0.3, Cam(1180, 780, 2360)),
                    (t_men - 0.15, Cam(1010, 842, 2010)), (t_lai + 1.2, Cam(1390, 870, 1860)), (t_ni, Cam(1400, 866, 1840)),
                    (t_wen - 0.1, Cam(1380, 868, 1860)), (t_feili + 0.6, Cam(1130, 880, 1560)), (t_zhe, Cam(1120, 878, 1540)),
                    (t_qishi + 0.4, Cam(1060, 870, 1480)), (t_bai - 0.3, Cam(1080, 872, 1500)), (t_suan, Cam(1170, 875, 1520)),
                    (t_jiusuan - 0.1, Cam(1180, 870, 1560)), (t_hua + 0.4, Cam(1290, 820, 1720)), (T, Cam(1300, 818, 1700))],
                   ["linear", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "sine", "linear"])
    sc.camera = cam

    # ---- sound
    sc.sfx("crowd", 0, dur=T + 0.3, gain_db=-28, fade_in=1.0, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-27, fade_in=1.0, fade_out=1.0)
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-29, fade_in=1.0, fade_out=1.0)
    sc.sfx("birds", 0, dur=t_lai, gain_db=-30, fade_in=1.0, fade_out=1.5)
    return sc
