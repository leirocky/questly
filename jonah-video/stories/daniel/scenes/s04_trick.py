"""Scene 4 — the officials trick the king into signing the decree (Daniel 6:6-9).

Same hall and stage as s02 / s03 (stories/daniel/scenes/s02_daniel.py), opening on s03's last frame: the four
officials scheming by the records table. The terrace layers are included again, so a sliver of the bright terrace
may show beyond the curtain pier when the camera is near the throne.

  line 0  "于是，这些官员一起去见国王，说："  the four turn and walk together to the throne (planted-foot strides, the
                                        camera travels with them)
  line 1  (O) "王啊，愿你万岁！"          they bow low (smug); the king smiles
          "请你下一道命令：三十天之内，"  the leader stands up holding the decree; a speech bubble shows "30天"
          "谁都不可以向别的神或者别的人祷告，"  the bubble shows a person praying, crossed out
          "只能向王祈求。"                the bubble shows a person kneeling before the king's crown; the king is pleased
  line 2  (O) "谁要是不听，就把他扔进狮子坑里！"  the bubble shows a (friendly) lion peeking out of the den
  line 3  "国王没有想到这是一个圈套，"    the bubble pops away; the officials exchange sly whispers; the king smiles
                                        unaware
          "就在命令上签了名。"            the leader steps up and hands over the decree (cut on a dip): the king raises
                                        his seal and presses it on (thud, a little gold glint on the seal)
          "按照国家的规矩，国王签了名的命令，"  the officials bow and stroll away, pleased; the camera eases in on the
                                        king with the sealed decree
          "谁也不能改。"                  the seal glints once
  end     calm, uncluttered frame: the king alone on his throne with the decree, guards, curtain (dissolves into s05).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import arcs_markup, dip, nod, snap
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.scene import Scene
from stories.daniel.scenes.s02_daniel import (
    FLOOR_Y, KS, OVS_S, SH, SW, THRONE_HX, THRONE_Y, actor, add_hall, basket_markup, bcam, cam_path, chunk, city_svg,
    doc, hx, king_fig, off, parapet_svg, records_table_markup, scene_offset, terrace_clouds_svg, terrace_sky_svg)
from stories.daniel.scenes.s03_jealous import A_X, B_X, BASKET, C_X, D_X

INK = P["ink"]
OS = OVS_S
LINE_X = {"A": 830, "B": 1000, "C": 1170, "D": 1340}       # in front of the throne
EXIT_X = {"A": 1560, "B": 1640, "C": 1720, "D": 1800}     # strolling away (out of the final frame)
HAND_X = 670                                               # the leader steps up here to hand over the decree
GOLD_DARK = "#b98a2a"
SEAL_RED = "#c0533a"


# ---------------------------------------------------------------- the king raising his seal (in-between)
STAMP_UP = C._P(t=-2, h=12, lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8,
                arms=(("ik", "body", 82, -76, 1), ("ik", "body", 66, -92, 1)), hands=("fist", "fist"),
                look=(0.03, 0.06))


def _stamp_up_front(D):
    """As characters._sign_front (seated) but the seal is lifted above the sheet and nothing is stamped yet."""
    fmt = C.fmt

    def front(st):
        W0, W1 = st["arms"][0][2], st["arms"][1][2]
        hr, skin = st["m"]["hr"], D["skin"]
        x0, x1 = W0[0] - 30, W0[0] + 26
        top = W0[1]
        bot = top + 64
        s = (f'<path d="M{fmt(x0 + 3)},{fmt(top)} L{fmt(x1 - 3)},{fmt(top)} L{fmt(x1)},{fmt(bot - 8)} '
             f'Q{fmt((x0 + x1) / 2)},{fmt(bot + 6)} {fmt(x0)},{fmt(bot - 4)} Z" fill="{C.PARCH}" {C._st(3.0)}/>')
        s += C._writing(x0 + 8, x1 - 8, top + 10, bot - 30, rows=3)
        s += (f'<rect x="{fmt(x0 - 9)}" y="{fmt(top - 7)}" width="{fmt(x1 - x0 + 18)}" height="14" rx="6" '
              f'fill="{C.PARCH_ROLL}" {C._st(3.0)}/>')
        s += f'<circle cx="{fmt(W0[0])}" cy="{fmt(W0[1])}" r="{fmt(hr)}" fill="{skin}" {C._st(3.2)}/>'
        sx, sy = W1[0] - 6, W1[1] + 18
        s += (f'<rect x="{fmt(sx - 8)}" y="{fmt(sy - 30)}" width="16" height="30" rx="5" fill="{C.GOLD}" {C._st(2.8)}/>'
              f'<ellipse cx="{fmt(sx)}" cy="{fmt(sy - 1)}" rx="11" ry="4.5" fill="{C.GOLD_DARK}" {C._st(2.4)}/>'
              f'<circle cx="{fmt(sx)}" cy="{fmt(sy - 34)}" r="7" fill="{C.GOLD}" {C._st(2.6)}/>')
        s += f'<circle cx="{fmt(W1[0])}" cy="{fmt(W1[1] - 6)}" r="{fmt(hr)}" fill="{skin}" {C._st(3.2)}/>'
        return s
    return front


def king_stamp_up(expr="happy"):
    D = C._king_design("darius", "sit_throne", False, False)
    D["front"] = _stamp_up_front(D)
    inner, _ = C._figure(D, C._KING_M, STAMP_UP, expr, 1, True)
    return C._wrap_out(inner, hx(THRONE_HX), THRONE_Y, KS, 1, "king-stamp-up")


# ---------------------------------------------------------------- the speech bubble and its pictures


def bubble_shell(cx, cy, w, h, tx, ty):
    """Rounded speech bubble centred at (cx, cy) with a tail toward (tx, ty)."""
    r = 60
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    bx = cx - w * 0.18
    d = (f"M{x0 + r},{y0} L{x1 - r},{y0} Q{x1},{y0} {x1},{y0 + r} L{x1},{y1 - r} Q{x1},{y1} {x1 - r},{y1} "
         f"L{bx + 40},{y1} L{tx},{ty} L{bx - 10},{y1} L{x0 + r},{y1} Q{x0},{y1} {x0},{y1 - r} L{x0},{y0 + r} "
         f"Q{x0},{y0} {x0 + r},{y0} Z")
    return S.g(f'<path d="{d}" fill="#fffaf0" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>',
               filter="wobble-fine")


def crown_icon(x, y, s=1.0):
    """The king's crenellated gold crown with jewels (bottom centre at x, y)."""
    w, h = 120 * s, 80 * s
    d = f"M{x - w / 2},{y} L{x - w / 2},{y - h} "
    for k in range(5):
        xa = x - w / 2 + w * k / 5
        d += f"L{xa + w / 10},{y - h} L{xa + w / 10},{y - h - 22 * s} L{xa + w / 5},{y - h - 22 * s} L{xa + w / 5},{y - h} "
    d += f"L{x + w / 2},{y} Z"
    out = f'<path d="{d}" fill="{P["crown"]}" stroke="{INK}" stroke-width="{4 * s:.1f}" stroke-linejoin="round"/>'
    for k, col in enumerate(("#4f86b0", "#b07cc8", "#4f86b0")):
        out += (f'<circle cx="{x - 30 * s + 30 * s * k:.1f}" cy="{y - h * 0.5:.1f}" r="{10 * s:.1f}" fill="{col}" '
                f'stroke="{INK}" stroke-width="{2.5 * s:.1f}"/>')
    out += (f'<rect x="{x - w / 2 - 6 * s:.1f}" y="{y - 14 * s:.1f}" width="{w + 12 * s:.1f}" height="{16 * s:.1f}" '
            f'rx="{6 * s:.1f}" fill="{GOLD_DARK}" stroke="{INK}" stroke-width="{3 * s:.1f}"/>')
    return S.g(out, filter="wobble-fine")


def bubble_svg(kind, cx, cy, tx, ty):
    out = bubble_shell(cx, cy, 380, 290, tx, ty)
    if kind == "30":
        font = 'font-family="LXGW WenKai" font-weight="bold" text-anchor="middle"'
        out += (f'<text x="{cx - 26}" y="{cy + 52}" {font} font-size="150" fill="#2f5f9e" stroke="{INK}" '
                f'stroke-width="3">30</text><text x="{cx + 118}" y="{cy + 52}" {font} font-size="70" '
                f'fill="{P["terracotta"]}" stroke="{INK}" stroke-width="2">天</text>')
        for k in range(5):        # five little suns: days going by
            sx = cx - 120 + 60 * k
            out += (f'<circle cx="{sx}" cy="{cy - 92}" r="13" fill="{P["sun"]}" stroke="{INK}" stroke-width="2.5"/>')
    elif kind == "no_pray":
        out += C.citizen(cx - 4, cy + 112, 0.68, 1, kind="man", variant=0, pose="kneel_pray")
        out += (f'<circle cx="{cx - 4}" cy="{cy + 8}" r="122" fill="none" stroke="#c0533a" stroke-width="15" '
                f'opacity="0.9"/><path d="M{cx - 90},{cy - 78} L{cx + 82},{cy + 94}" stroke="#c0533a" '
                f'stroke-width="15" stroke-linecap="round" opacity="0.9"/>')
    elif kind == "king":
        out += C.citizen(cx - 92, cy + 120, 0.66, 1, kind="man", variant=0, pose="kneel_pray")
        out += (f'<ellipse cx="{cx + 90}" cy="{cy + 98}" rx="70" ry="16" fill="#6b4291" stroke="{INK}" '
                f'stroke-width="3.5"/>') + crown_icon(cx + 90, cy + 86, 1.0)
        for a in (-50, -20, 10, 40):     # little shine lines around the crown
            r0, r1 = 92, 116
            aa = math.radians(a - 90)
            out += (f'<path d="M{cx + 90 + r0 * math.cos(aa):.1f},{cy + 40 + r0 * math.sin(aa):.1f} '
                    f'L{cx + 90 + r1 * math.cos(aa):.1f},{cy + 40 + r1 * math.sin(aa):.1f}" stroke="{P["crown"]}" '
                    f'stroke-width="6" stroke-linecap="round"/>')
    elif kind == "lion":
        x, y, s = cx, cy + 60, 0.62
        out += PR.lion_den(x, y, s, view="outside", part="back")
        out += PR.in_den_hole(PR.lion(x + 6, y + 70, 0.42, 1, pose="sit", eyes="open"), x, y, s)
        out += PR.lion_den(x, y, s, view="outside", part="front")
    return doc(out)


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    L0, L1, L2, L3 = ctx.lines
    t_off = scene_offset(ctx.id)
    c_long = chunk(L1, "万岁")
    c_30 = chunk(L1, "三十天")
    c_nopray = chunk(L1, "别的神")
    c_king = chunk(L1, "只能向王")
    c_trap = chunk(L3, "圈套")
    c_sign = chunk(L3, "签了名")
    c_rule = chunk(L3, "规矩")
    c_never = chunk(L3, "谁也不能改")

    # ---------------- backdrops (the terrace beyond the pier, the hall, the records table)
    sc.add("sky", terrace_sky_svg(), z=0, wc=0.6, seed=11)
    sc.add("clouds", terrace_clouds_svg(), z=0.5, motion=M.drift(vx=6), seed=12)
    sc.add("city", city_svg(), z=1, seed=13)
    sc.add("parapet", parapet_svg(), z=2, seed=14)
    add_hall(sc, z0=3, t_off=t_off)
    sc.add("table", doc(records_table_markup()), z=6.6, seed=130)
    sc.add("basket", doc(basket_markup(hx(BASKET[0]), BASKET[1], 0.9)), z=7.6, seed=131)

    # ---------------- timing
    t_walk = L0.start + 0.15
    t_bow = c_long.start + 0.1
    t_present = c_30.start + 0.1
    t_up = c_long.end + 0.5                   # the others straighten up after the bow
    t_whisper = c_trap.start + 0.3
    t_hand = c_sign.start - 0.6               # the leader steps up to the throne
    t_give = None                             # set below: when he arrives
    t_leave = c_rule.start + 0.1

    # ---------------- the officials
    S_ = {"A": (0, A_X, "scheme", 1, 7.3, 0.3), "B": (2, B_X, "whisper", -1, 7.4, 0.6),
          "C": (1, C_X, "scheme", 1, 7.25, 0.15), "D": (3, D_X, "whisper", -1, 7.45, 0.55)}
    order = ("A", "B", "C", "D")
    arrive = {}
    for k, who in enumerate(order):
        v, sx_, pose0, fac0, z, ph = S_[who]
        x = hx(sx_)
        ap = (x, FLOOR_Y)
        lead = who == "A"
        d1 = LINE_X[who] - sx_
        n1 = max(2, round(abs(d1) / (87 * OS)))
        t1 = t_walk + 0.07 * k
        t1e = snap(t1 + n1 * 0.25)
        arrive[who] = t1e
        fr = [off(x, FLOOR_Y, v, "walk_a", -1, s=OS), off(x, FLOOR_Y, v, "walk_b", -1, s=OS),
              off(x, FLOOR_Y, v, pose0, fac0, s=OS),
              off(x, FLOOR_Y, v, "stand", -1, "smug", s=OS),
              off(x, FLOOR_Y, v, "bow", -1, s=OS),
              off(x, FLOOR_Y, v, "read" if lead else "stand", -1, "smug" if lead else "sly", s=OS),
              off(x, FLOOR_Y, v, "whisper" if who in ("B", "C") else "scheme", 1 if who == "B" else -1, s=OS),
              off(x, FLOOR_Y, v, "bow", -1, s=OS),
              off(x, FLOOR_Y, v, "walk_a", 1, "sly", s=OS), off(x, FLOOR_Y, v, "walk_b", 1, "sly", s=OS)]
        walks = [(t1, n1, d1 / n1, 0, 0.25)]
        bumps = [dip(snap(t1), OS, ap, 5), dip(snap(t1e), OS, ap, 5)]
        t_b = t_bow + 0.08 * k
        base = [(0, 2), (snap(t1e), 3), (snap(t_b), 4)]
        bumps.append(dip(snap(t_b), OS, ap, 8))
        if lead:
            base.append((snap(t_present), 5))
            bumps.append(dip(snap(t_present), OS, ap))
            # steps up to the throne and hands the decree over
            d2 = HAND_X - LINE_X[who]
            n2 = 2
            walks.append((t_hand, n2, d2 / n2, 0, 0.27))
            t_give = snap(t_hand + n2 * 0.27) + 0.05
            base += [(snap(t_give), 7), (snap(t_give + 1.6), 3)]
            bumps += [dip(snap(t_give), OS, ap, 8), dip(snap(t_give + 1.6), OS, ap, 5)]
            d3 = EXIT_X[who] - HAND_X
            t3 = t_leave + 0.45
        else:
            base.append((snap(t_up + 0.1 * k), 5))
            bumps.append(dip(snap(t_up + 0.1 * k), OS, ap, 5))
            tw = t_whisper + 0.25 * k
            base += [(snap(tw), 6), (snap(c_sign.start + 0.3 + 0.1 * k), 3)]
            bumps += [dip(snap(tw), OS, ap), dip(snap(c_sign.start + 0.3 + 0.1 * k), OS, ap, 5)]
            d3 = EXIT_X[who] - LINE_X[who]
            t3 = t_leave + 0.45 - 0.12 * k
        n3 = max(2, round(abs(d3) / (87 * OS)))
        walks.append((t3, n3, d3 / n3, 8, 0.27))
        actor(sc, f"of{who}", z, fr, ap, OS, seed={"A": 122, "B": 123, "C": 126, "D": 127}[who], base=base,
              walks=walks, bumps=bumps, breathe=(0.01, 3.0, ph + t_off / 3.0))
        if lead:
            lead_head = C.body_points(C.official, hx(LINE_X["A"]), FLOOR_Y, OS, -1, variant=0, pose="stand")["head"]
            lead_exit = (t3, n3)
    sc.sfx("footsteps", t_walk, dur=max(arrive.values()) - t_walk + 0.15, gain_db=-12, fade_in=0.05, fade_out=0.3,
           rate=1 / 0.25)

    # ---------------- King Darius
    kp = (hx(THRONE_HX), THRONE_Y)
    t_smile = c_long.start + 0.6
    t_pleased = c_king.start + 0.3
    t_stamp = t_give + 0.55
    kfr = [king_fig("sit_throne"), king_fig("sit_throne", "happy"), king_stamp_up("happy"),
           king_fig("sit_sign", "happy")]
    sc.add("king", [doc(f) for f in kfr], z=5, seed=120,
           frame_at=lambda t: float(0 if t < snap(t_smile) else 1 if t < snap(t_give) else
                                    2 if t < snap(t_stamp) else 3),
           motion=M.combine(dip(snap(t_smile), KS, kp, 4), nod(t_smile + 0.1, kp, 2.5, 0.6),
                            M.keys([(t_pleased, {"dy": 0, "sy": 1}), (t_pleased + 0.18, {"dy": -8, "sy": 1.03}),
                                    (t_pleased + 0.45, {"dy": 0, "sy": 1})], "sine", pivot=kp),
                            dip(snap(t_give), KS, kp, 5),
                            M.keys([(t_stamp - 0.12, {"dy": 0}), (t_stamp, {"dy": 6}), (t_stamp + 0.2, {"dy": 0})],
                                   ["in", "out"], pivot=kp),
                            M.breathe(0.008, 3.2, pivot=kp, phase=0.3 + t_off / 3.2)))
    # where the seal lands on the decree (sit_sign: near hand + (-6, 18), the mark at +(9, 4))
    hands = C.hand_positions(C.king, kp[0], kp[1], KS, 1, pose="sit_sign", attire="darius", throne=False)
    seal = (hands[1][0] - 6 * KS + 9 * KS, hands[1][1] + 22 * KS)

    # ---------------- the speech bubble (the officials' plan) above the leader
    bub = (lead_head[0] + 210, lead_head[1] - 330)
    tail = (lead_head[0] + 40, lead_head[1] - 90)
    kinds = ("30", "no_pray", "king", "lion")
    t_k = [c_30.start + 0.35, c_nopray.start + 0.25, c_king.start + 0.15, L2.start + 0.2]
    t_bub_end = L2.end + 0.45
    sc.add("bubble", [bubble_svg(k, bub[0], bub[1], tail[0], tail[1]) for k in kinds], z=9.8, wc=0.4,
           frame_at=lambda t: float(sum(t >= snap(x) for x in t_k[1:])),
           motion=M.combine(
               M.keys([(t_k[0] - 0.01, {"alpha": 0, "s": 0.5}), (t_k[0] + 0.25, {"alpha": 1, "s": 1.05}),
                       (t_k[0] + 0.42, {"s": 1.0}), (t_bub_end - 0.3, {"alpha": 1, "s": 1.0}),
                       (t_bub_end, {"alpha": 0, "s": 0.7})], ["out", "sine", "sine", "in"], pivot=tail),
               *[M.keys([(snap(x) - 0.01, {"s": 1.0}), (snap(x) + 0.09, {"s": 1.06}), (snap(x) + 0.25, {"s": 1.0})],
                        "sine", pivot=bub) for x in t_k[1:]]))
    for x in t_k:
        sc.sfx("pop", x, gain_db=-17, pan=-0.1)
    lh = lead_head
    arcs = [doc(arcs_markup(lh[0] - 46 * OS, lh[1] + 26 * OS, -1, k, OS)) for k in (1, 2, 3)]
    on = [(L1.start, c_long.end), (c_30.start, L1.end), (L2.start, L2.end)]
    keys = []
    for a, b in on:
        keys += [(a, {"alpha": 0}), (a + 0.12, {"alpha": 1}), (b - 0.12, {"alpha": 1}), (b, {"alpha": 0})]
    sc.add("arcs", arcs, z=9.8, wc=0, frame_at=lambda t: float(int(t * 7) % 3), motion=M.keys(keys, "sine"))

    # ---------------- camera (s03's last framing first)
    sc.camera = cam_path([
        (0.0, bcam(hx(2050), 1900), 0),
        (t_walk + 0.1, bcam(hx(2050), 1900), 0, "sine"),
        (max(arrive.values()) + 0.2, bcam(hx(820), 2000), 0),
        (c_30.start, bcam(hx(820), 2000), 0),
        (c_30.start + 1.8, bcam(hx(800), 1900), 0),
        (t_hand - 0.2, bcam(hx(800), 1900), 0),
        (t_give + 0.4, bcam(hx(640), 1820), 0),
        (t_leave + 0.3, bcam(hx(640), 1820), 0),
        (t_leave + 3.6, bcam(hx(470), 1740), 0),
    ])

    sc.fx = [
        FX.motes((hx(950), 520, hx(2900), 1250), count=40, t0=0, color=(255, 246, 214), size=(2, 5), alpha=110,
                 seed=22),
        # a glint on the fresh seal (beside the decree, well below and in front of the king's face)
        FX.sparkles((seal[0] + 8, seal[1] - 10, seal[0] + 70, seal[1] + 40), count=4, t0=t_stamp + 0.05,
                    t1=t_stamp + 1.4, color=(255, 236, 170), size=(8, 15), period=1.0, drift=0, seed=41),
        FX.sparkles((seal[0] + 8, seal[1] - 10, seal[0] + 70, seal[1] + 40), count=4, t0=c_never.start,
                    t1=c_never.end + 1.0, color=(255, 236, 170), size=(8, 15), period=1.2, drift=0, seed=42),
    ]

    # ---------------- sound
    for k in range(4):
        sc.sfx("cloth", t_bow + 0.08 * k, gain_db=-17 - k, pan=0.1 * k)
    sc.sfx("cloth", t_present - 0.05, gain_db=-13)
    sc.sfx("cloth", t_give - 0.05, gain_db=-14)
    sc.sfx("thud", t_stamp, gain_db=-8)
    sc.sfx("sparkle", t_stamp + 0.1, gain_db=-20)
    sc.sfx("footsteps", lead_exit[0] - 0.4, dur=lead_exit[1] * 0.27 + 0.5, gain_db=-14, fade_in=0.1, fade_out=0.6,
           rate=1 / 0.27)
    sc.sfx("sparkle", c_never.start + 0.1, gain_db=-21)
    return sc
