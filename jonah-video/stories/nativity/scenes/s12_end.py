"""Scene 12 - the closing page, back in the boy's living room of s02 (same room, tree, star, presents, nativity set and
jumper). The step stool has been put aside; the boy kneels by the little nativity set under the tree holding the last
figure - the baby Jesus in his manger - and puts it into the empty middle of the set: the best present under the
tree. The tree star glows, warm light spreads, a soft glow rises over the little manger (God is never drawn - light
only). Hearts. Then the closing question to the child, a calm final frame and the end card '耶稣降生 · 完'.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame (page dip from s11): the boy kneeling by the set with the baby figure in his hands, looking
               at it; tree lights twinkle; the star glows softly
  '小朋友'      he looks up at us
  '博士们给耶稣送了礼物' on '礼物' the presents under the tree give a little hop and twinkle and he glances at them
  '可是你知道吗' he looks back at us, a little curious
  '耶稣，'      he lowers the figure gently into the empty middle of the set (a small bow) - it is in (sparkle)
  '才是上帝送给全世界最好的礼物' he sits back on his heels, amazed: a soft glow rises over the little manger, the tree
               star brightens and warm light spreads over the room (chime)
  '上帝爱我们'  he hugs himself, beaming, and rocks a little; hearts float up from him
  '送给了我们'  a bigger heart rises from the little manger
  line 3       '今年圣诞节' he turns round to us; '你想送给耶稣什么礼物呢' he thinks (a small thought bubble with a heart
               and a '?'), then smiles at us through the 2 s pause
  end          the bubble floats away, the end card '耶稣降生 · 完' fades in with a little heart (chime); calm final
               frame for the film's fade-out
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
from stories.nativity.scenes import s02_question as Q
from stories.nativity.scenes.s01_title import Fig, beat, breath, dip, doc, glow_svg, heart_markup, hop, keyed, snap

INK = P["ink"]
SET_X, SET_Y, SET_S = Q.SET
BABY_SPOT = (SET_X + PR.NATIVITY_SET_SPOTS["baby"][0] * SET_S, SET_Y + PR.NATIVITY_SET_SPOTS["baby"][1] * SET_S)
FIG_S = Q.FIG_K * SET_S                    # the baby-in-the-manger figurine's scale in the set
LOWER_ROT, LOWER_D = 7.0, 34.0             # how far he bows to put the figure in
STOOL_ASIDE = 600
END = (880, 430)

C.EXPRS.setdefault("ne_gifts", dict(C.EXPRS["happy"], look=(0.09, -0.03)))
C.EXPRS.setdefault("ne_down", dict(C.EXPRS["tender"], look=(0.05, 0.1)))
C.EXPRS.setdefault("ne_ask", dict(C.EXPRS["question"], look=(0.0, 0.02)))
C.EXPRS.setdefault("ne_think", dict(C.EXPRS["thoughtful"]))
C.EXPRS.setdefault("ne_blink", dict(C.EXPRS["happy"], eyes="closed"))


def boy_anchor():
    """Where he kneels so that, bowed by LOWER_ROT / LOWER_D, the figure in his hands lands on the set's baby spot."""
    pts = Q.boy_points(0, 0, "place_far", None, 1, "figure")
    (w0x, w0y), (w1x, w1y) = pts["hands"]
    ox, oy = (w0x + w1x) / 2, max(w0y, w1y) + 6 * Q.BOY_S
    r = math.radians(LOWER_ROT)
    rx, ry = ox * math.cos(r) - oy * math.sin(r), ox * math.sin(r) + oy * math.cos(r)
    return (BABY_SPOT[0] - rx, BABY_SPOT[1] - ry - LOWER_D)


BOY = boy_anchor()


def placed_svg():
    return doc(S.g(PR.nativity_figure(BABY_SPOT[0], BABY_SPOT[1], FIG_S, 1, kind="baby"), filter="wobble-fine"))


def bubble_svg():
    """A small thought bubble: a heart and a question mark."""
    cx, cy = BOY[0] - 250, BOY[1] - 470
    out = S.cloud(cx, cy + 20, 300, 120, fill="#fff8ea", seed=23, puffs=5, sw=4)
    for dx, dy, r in ((150, 120, 18), (200, 160, 12), (236, 190, 8)):
        out += f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" fill="#fff8ea" stroke="{INK}" stroke-width="3.4"/>'
    body = S.g(out, filter="wobble-fine")
    body += heart_markup(cx - 50, cy + 10, 34)
    body += (f'<text x="{cx + 55}" y="{cy + 38}" font-family="LXGW WenKai" font-weight="bold" font-size="92" '
             f'fill="#e0913a" stroke="{INK}" stroke-width="3.5" paint-order="stroke" text-anchor="middle">?</text>')
    return doc(body), (cx, cy + 20)


def end_card_svg():
    x, y = END
    defs = S.rad_grad("n12card", [(0, "#fff3d6", 0.9), (0.6, "#ffe9c0", 0.4), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 34}" rx="440" ry="130" fill="url(#n12card)"/>' +
           S.text(x, y, "耶稣降生 · 完", size=88, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_gift = beat(ctx, 0, "礼物")
    t_know = beat(ctx, 0, "可是")
    t_jesus = beat(ctx, 0, "耶稣", 1)
    t_best = beat(ctx, 0, "才是")
    t_world = beat(ctx, 0, "最好的")
    t_love = beat(ctx, 1, "爱")
    t_us = beat(ctx, 1, "送给了我们")
    t_l2end = L[1].end
    t_year = beat(ctx, 2, "今年")
    t_what = beat(ctx, 2, "你想")
    t_q = beat(ctx, 2, "什么礼物")
    t_end = L[2].end

    # ---------------- the boy
    c_friend = snap(t_friend + 0.08)
    c_gift = snap(t_gift - 0.12)
    c_know = snap(t_know)
    low0, land = t_jesus - 0.22, snap(t_jesus + 0.3)
    c_sit = snap(land + 0.62)
    c_hug = snap(t_love - 0.12)
    c_turn = snap(t_year - 0.05)
    c_think = snap(t_what + 0.1)
    c_smile = snap(t_end + 0.25)
    X, Y = BOY
    boy = Fig(ctx, "boy", BOY, z=8, seed=91)
    boy.at(0, Q.boy(X, Y, "place_far", "ne_down", 1, "figure"))
    boy.at(c_friend, Q.boy(X, Y, "place_far", "nq_us", 1, "figure"))
    boy.at(c_gift, Q.boy(X, Y, "place_far", "ne_gifts", 1, "figure"))
    boy.at(c_know, Q.boy(X, Y, "place_far", "ne_ask", 1, "figure"))
    boy.at(snap(low0), Q.boy(X, Y, "place_far", "ne_down", 1, "figure"))
    boy.at(land, Q.boy(X, Y, "place_far", "ne_down", 1, None))
    boy.at(c_sit, Q.boy(X, Y, "kneel_look", "awed", 1))
    boy.at(c_hug, Q.boy(X, Y, "kneel_hug", "joyful", 1))
    boy.at(c_turn, Q.boy(X, Y, "kneel_look", "nq_us", -1))
    boy.at(c_think, Q.boy(X, Y, "kneel_look", "ne_think", -1))
    boy.at(c_smile, Q.boy(X, Y, "kneel_look", "nq_us", -1))
    for tb in (c_smile + 1.3,):
        if tb + 0.14 < T:
            boy.at(snap(tb), Q.boy(X, Y, "kneel_look", "ne_blink", -1))
            boy.at(snap(tb + 0.14), Q.boy(X, Y, "kneel_look", "nq_us", -1))
    bow = keyed([(low0, 0.0), (land, 1.0), (land + 0.45, 0.0)], "sine")
    rock = lambda t: Tf(rot=2.2 * math.sin(2 * math.pi * (t - c_hug) / 1.6) * M.progress(t, c_hug, c_hug + 0.4, "sine")
                        * (1 - M.progress(t, c_turn - 0.4, c_turn, "sine")) if c_hug <= t < c_turn else 0.0)  # noqa: E731
    boy.move(lambda t: Tf(dy=LOWER_D * bow(t), rot=LOWER_ROT * bow(t)), rock,
             dip(c_friend, 4), dip(c_gift, 4), dip(c_know, 4), dip(c_sit, 6), dip(c_hug, 6), dip(c_turn, 7),
             dip(c_think, 3), dip(c_smile, 3), breath(ctx, 0.009, 3.0))
    boy.add(sc)

    # ---------------- the room (as s02, the stool put aside)
    sc.add("room", Q.room_svg(), z=0, wc=0.8)
    sc.add("tree", [Q.tree_svg(k) for k in range(4)] + [Q.tree_svg(0)], z=2, seed=21, frame_at=lambda t: (t / 0.45) % 4)
    sc.add("baubles", Q.baubles_svg(), z=2.1, seed=23)
    sc.add("hung", Q.hung_bauble_svg(), z=2.2, seed=25)
    sc.add("set", Q.set_svg(), z=3, seed=27)
    sc.add("placed", placed_svg(), z=3.05, seed=28, motion=lambda t: Tf(alpha=1.0 if t >= land else 0.0))
    gx, gy, gs = Q.GIFTS
    gift_hop = hop(t_gift, [(0, {"sy": 1.0, "dy": 0}), (0.12, {"sy": 0.94, "dy": 4}), (0.3, {"sy": 1.05, "dy": -12}),
                            (0.5, {"sy": 1.0, "dy": 0})], ["out", "out", "sine"])
    sc.add("gifts", Q.gifts_svg(), z=3.1, seed=29, motion=M.with_pivot(gift_hop, (gx, gy)))
    sc.add("box", Q.box_svg(), z=1.9, seed=31)
    sc.add("stool", doc(Q.stool_body(STOOL_ASIDE)), z=1.8, seed=33)

    # ---------------- the star, the warm light, the glow over the little manger
    sc.add("topper", [Q.topper_svg(1.0, rot=r) for r in (0, 10, 20)], z=2.5, seed=37, wc=0.3,
           frame_at=lambda t: (t / 1.6) % 2.0,
           motion=lambda t: Tf(sx=1 + 0.03 * math.sin(2 * math.pi * t / 2.2), sy=1 + 0.03 * math.sin(2 * math.pi * t / 2.2),
                               px=Q.TOP[0], py=Q.TOP[1]))
    bright = keyed([(t_best - 0.1, 0.0), (t_world + 0.4, 1.0)], "sine")
    sc.add("topglow", glow_svg(Q.TOP[0], Q.TOP[1], 300, 300, "nqtg", "#fff6d0", "#ffd970", 0.9, 0.4), z=2.6, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=(0.55 + 0.45 * bright(t)) * (0.8 + 0.2 * math.sin(2 * math.pi * t / 1.9))))
    sc.add("wash", Q.warm_wash_svg(), z=1.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(0.45 + 0.55 * bright(t)) * (0.92 + 0.08 * math.sin(2 * math.pi * t / 2.7))))
    spread = keyed([(t_best - 0.1, 0.0), (t_world + 0.9, 1.0)], "out")
    sc.add("spread", glow_svg(Q.TOP[0], Q.TOP[1] + 120, 1050, 720, "n12sp", "#ffe8b0", "#f8c870", 0.5, 0.22), z=1.6, wc=0,
           blend="screen", motion=lambda t: Tf(sx=0.25 + 0.75 * spread(t), sy=0.25 + 0.75 * spread(t),
                                               alpha=0.9 * spread(t), px=Q.TOP[0], py=Q.TOP[1]))
    rise = keyed([(land, 0.0), (land + 0.8, 1.0)], "out")
    bx_, by_ = BABY_SPOT
    sc.add("mglow", glow_svg(bx_, by_ - 60, 190, 170, "n12mg", "#fffbea", "#ffe7a0", 0.95, 0.42), z=3.2, wc=0,
           blend="screen", motion=lambda t: Tf(dy=-26 * rise(t) - 6 * math.sin(2 * math.pi * t / 2.3) * rise(t),
                                               alpha=rise(t) * (0.75 + 0.25 * bright(t))))
    sc.add("sglow", glow_svg(SET_X, SET_Y - 120, 300, 200, "n12sg", "#fff1c6", "#ffd27a", 0.6, 0.25), z=3.15, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=0.7 * rise(t)))

    # ---------------- hearts
    def heart(name, x0, y0, r, t0, dx=0.0, rise_px=260, life=2.6, z=9.5):
        def m(t):
            if t < t0 or t > t0 + life:
                return Tf(alpha=0.0)
            u = (t - t0) / life
            s_ = M.ease("back")(min(1.0, (t - t0) / 0.35))
            a = min(1.0, (t - t0) / 0.15) * (1 - M.progress(u, 0.65, 1.0, "sine"))
            return Tf(dx=dx * u + 10 * math.sin(2 * math.pi * (t - t0) / 1.3), dy=-rise_px * M.ease("out")(u),
                      sx=s_, sy=s_, alpha=a, px=x0, py=y0)
        sc.add(name, doc(heart_markup(x0, y0, r)), z=z, wc=0, motion=m)
    chest = (X + 30 * Q.BOY_S, Y - 120 * Q.BOY_S)
    for i, (dx, r, dt) in enumerate(((-40, 26, 0.0), (30, 20, 0.18), (-5, 32, 0.36), (55, 18, 0.6))):
        heart(f"heart{i}", chest[0] + dx, chest[1] - 40, r, t_love + dt, dx=(-30, 20, -10, 35)[i])
    heart("heart_big", bx_, by_ - 80, 40, t_us - 0.05, dx=-20, rise_px=300, life=3.0)

    # ---------------- the thought bubble (heart and '?')
    bsvg, bc = bubble_svg()
    b_in, b_out = snap(t_q - 0.25), snap(t_end + 1.2)   # keep the thought up through the answer pause

    def bub_m(t):
        if t < b_in or t > b_out + 0.4:
            return Tf(alpha=0.0)
        u = M.progress(t, b_in, b_in + 0.45, "back")
        s_ = 0.3 + 0.7 * u
        a = min(1.0, (t - b_in) / 0.12)
        dy = 3 * math.sin(2 * math.pi * t / 2.4)
        if t > b_out:
            v = (t - b_out) / 0.4
            dy -= 60 * v
            a *= 1 - v
        return Tf(sx=s_, sy=s_, alpha=a, dy=dy, px=bc[0] + 150, py=bc[1] + 120)
    sc.add("bubble", bsvg, z=10, wc=0.3, motion=bub_m)

    # ---------------- end card
    ex, ey = END
    t_card = snap(t_end + 1.8)   # the script leaves the child 2 s to answer: the card comes late in it
    sc.add("endcard", end_card_svg(), z=20, wc=0, motion=M.keys(
        [(t_card, {"alpha": 0, "s": 0.95, "dy": 16}), (t_card + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    hx, hy = ex, ey + 66
    th = t_card + 0.45
    sc.add("endheart", doc(heart_markup(hx, hy, 30)), z=20.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))

    # ---------------- sparkles
    sc.fx.append(FX.sparkles((gx - 170, gy - 190, gx + 170, gy - 20), count=6, t0=t_gift, t1=t_gift + 1.6, size=(9, 16),
                             period=1.0, drift=-10, seed=51))
    sc.fx.append(FX.sparkles((bx_ - 120, by_ - 260, bx_ + 120, by_ - 20), count=9, t0=land, size=(8, 15), period=1.6,
                             drift=-22, seed=53))
    sc.fx.append(FX.sparkles((Q.TOP[0] - 180, Q.TOP[1] - 160, Q.TOP[0] + 180, Q.TOP[1] + 120), count=8, size=(8, 15),
                             period=1.7, drift=-6, seed=55))
    sc.fx.append(FX.sparkles((ex - 420, ey - 120, ex + 420, ey + 40), count=6, t0=t_card + 0.4, size=(9, 16), period=2.0,
                             drift=0, seed=57))
    sc.fx.append(FX.motes((500, 200, 1900, 950), count=18, color=(255, 240, 200), seed=59, alpha=85))

    # ---------------- camera
    c0 = Cam(1240, 722, 1560)
    c1 = Cam(1255, 742, 1420)
    c2 = Cam(1190, 700, 1640)
    c3 = Cam(1196, 690, 1350)
    sc.camera = M.cam_keys([(0, c0), (low0 - 0.8, c0), (land + 0.2, c1), (t_best + 0.3, c1), (t_world + 1.2, c2),
                            (t_year, c2), (t_end + 0.6, c3), (T, Cam(1196, 688, 1330))], "sine")

    # ---------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-31, fade_in=0.8, fade_out=1.5)
    sc.sfx("pop", t_gift + 0.05, gain_db=-17, pan=0.4)
    sc.sfx("sparkle", t_gift + 0.12, gain_db=-19, pan=0.4)
    sc.sfx("thud", land - 0.02, gain_db=-24)
    sc.sfx("sparkle", land + 0.05, gain_db=-14)
    sc.sfx("chime", t_best + 0.2, gain_db=-11)
    sc.sfx("sparkle", t_love + 0.05, gain_db=-16)
    sc.sfx("pop", t_love + 0.1, gain_db=-21)
    sc.sfx("sparkle", t_us, gain_db=-17)
    sc.sfx("cloth", c_turn, gain_db=-20)
    sc.sfx("pop", b_in + 0.05, gain_db=-18, pan=-0.3)
    sc.sfx("chime", t_card + 0.1, gain_db=-12)
    return sc
