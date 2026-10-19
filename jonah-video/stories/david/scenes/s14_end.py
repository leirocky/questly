"""Scene 14 — the closing page: God is bigger than any giant; what is the giant you are afraid of?

One tall 2600 x 1800 stage on the Bethlehem hill at evening, no cuts: an indigo-to-rose sky with the first stars and
a thin moon, hazy violet hills with the little lamp-lit village, and on the grassy hilltop David sitting with his
sheep, playing his small harp (little music notes float up); beside him his shepherd's bag (four stones peeking out:
he only needed one) and his staff in the grass.

  line 0  '大卫并不比歌利亚高，也不比歌利亚壮。'  a picture-book measuring chart pops up in the sky: a little boy
          outline next to a giant outline on a height ruler (the giant grows up to his full height at '高'; at '壮'
          he puffs out wide, a bit silly).
          '可是大卫知道，上帝比任何巨人都大。'  the chart flies away, the camera tilts up into the huge starry sky and
          a soft golden light spreads over it (God is light, never a figure); stars twinkle.
  line 1  '小朋友，你心里，'  the camera comes back down; a second picture card pops up beside David: a little child
          (not David) on her own.  '有没有一个让你害怕的巨人呢？'  a soft, slightly silly 'worry giant' (a shadow
          cloud with goggly eyes and wiggly arms - a fear, not a person) rises up behind her; she looks worried.
          The 2 s pause holds on it (the cloud wobbles, she trembles a little).
  line 2  '下次害怕的时候，你也可以像大卫一样，'  David on the hill glows softly as he plays.
          '对上帝说：'  the child kneels and folds her hands; warm golden light pours into the card.
          '上帝啊，我相信你和我在一起！'  the worry giant shrinks and puffs away into little clouds; she smiles;
          stars come out in her sky. The card flies away; the camera settles on the starry hill and the end card
          '大卫和歌利亚 · 完' fades in with a little heart (chime). Calm final frame for the film's fade-out.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import cuts, dip, hop, snap
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import blink_expr, cam_at, heart_markup, make_cam, tuft_row, when, with_blinks

SW, SH = 2600, 1800
INK = P["ink"]
GY = 1585                   # the hilltop where David sits
SCD = 1.25                  # David and the sheep
DX = 1560
CARD = (420, 770, 1180, 1290)     # picture cards (x0, y0, x1, y1)
FLOOR = 1240                      # ground line inside the cards
CARD_X, CARD_Y = 1300, 820        # the end card


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


C.EXPRS.setdefault("dv14_smile", dict(C.EXPRS["peaceful"], mouth="grin"))


# ============================================================================ backdrop


def sky_svg():
    defs = S.lin_grad("s14sky", [(0, "#232c55"), (0.3, "#3e4479"), (0.55, "#7a5f93"), (0.72, "#c9849a"),
                                 (0.84, "#f0a88a"), (1, "#f6c99a")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s14sky)"/>', defs)


def stars_svg(seed=14, n=140, y1=1050, big=True):
    rng = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y = rng.uniform(0, SW), rng.uniform(20, y1)
        if CARD_X - 700 < x < CARD_X + 700 and CARD_Y - 170 < y < CARD_Y + 120:
            continue
        r = rng.uniform(2.2, 5.0) * (1.25 - 0.5 * y / y1)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fff6d8"/>'
    if big:
        for x, y, r in ((2150, 300, 24), (420, 220, 20), (1700, 120, 18)):
            out += (f'<path d="M{x},{y - r} L{x + r * 0.24},{y - r * 0.24} L{x + r},{y} L{x + r * 0.24},{y + r * 0.24} '
                    f'L{x},{y + r} L{x - r * 0.24},{y + r * 0.24} L{x - r},{y} L{x - r * 0.24},{y - r * 0.24} Z" '
                    f'fill="#fff3c8" stroke="{P["ink_soft"]}" stroke-width="2"/>')
        out += (f'<path d="M2330,520 a62,62 0 1,0 54,94 a48,48 0 1,1 -54,-94 Z" fill="#fff0c4" '
                f'stroke="{P["ink_soft"]}" stroke-width="3"/>')
    return doc(out)


def clouds_svg():
    out = ""
    for cx, cy, w, h, sd in ((300, 1150, 380, 70, 1), (2300, 1080, 420, 80, 2), (1150, 1200, 300, 56, 3)):
        out += S.cloud(cx, cy, w, h, fill="#e9a3a6", seed=sd + 30, sw=3, shade_fill="#a77d9f")
    return doc(S.g(out, filter="wobble", opacity=0.9))


def hills_svg():
    out = ""
    out += S.path(S.hill(-60, SW + 60, 1380, 160, seed=41, bottom=SH + 60, bumps=4), "#8a77a5", sw=3)
    # the little village of Bethlehem, lamp-lit
    for x, y, s, v, f in ((420, 1330, 0.18, 0, 1), (560, 1316, 0.2, 2, -1), (700, 1330, 0.17, 3, 1)):
        out += PR.house(x, y, s, variant=v, facing=f)
    for x, y in ((395, 1290), (548, 1283), (700, 1296), (585, 1236)):
        out += (f'<circle cx="{x}" cy="{y}" r="16" fill="#ffd98c" opacity="0.45" filter="url(#soft)"/>'
                f'<rect x="{x - 6}" y="{y - 8}" width="12" height="16" rx="3" fill="#ffe3a0" stroke="{INK}" '
                f'stroke-width="2"/>')
    out += S.path(S.hill(-60, SW + 60, 1460, 130, seed=44, bottom=SH + 60, bumps=3), "#6f6f94", sw=3.5)
    for x, y, s in ((300, 1400, 0.4), (2250, 1390, 0.42), (1900, 1420, 0.32)):
        out += PR.olive_tree(x, y, s, seed=int(x))
    return doc(S.g(out, filter="wobble"))


def hilltop_svg():
    defs = S.lin_grad("s14hill", [(0, "#6f8f62"), (1, "#4f6b4f")])
    d = S.smooth_path([(-60, 1640), (500, 1560), (1100, 1540), (1600, 1546), (2100, 1562), (SW + 60, 1620)],
                      closed=False) + f" L{SW + 60},{SH + 60} L-60,{SH + 60} Z"
    out = S.path(d, "url(#s14hill)", sw=4.5)
    rng = random.Random(3)
    for _ in range(40):
        x, y = rng.uniform(0, SW), rng.uniform(1600, 1790)
        c = rng.choice(("#e9d9a6", "#d9b3c8", "#c9c0e6"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(4, 7))}" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    return doc(S.g(out, filter="wobble"), defs)


FG = [(60, 1800, 1.3, 0), (420, 1795, 1.0, 1), (900, 1800, 1.1, 0), (1350, 1798, 0.9, 1), (1820, 1800, 1.2, 0),
      (2250, 1796, 1.1, 1), (2560, 1800, 1.2, 0)]


def fg_svg(k):
    return doc(S.g(tuft_row(FG, k * 2.1), opacity=0.92))


def glow_god_svg():
    cx, cy = 1300, -80
    defs = S.rad_grad("s14god", [(0, "#fff0c0", 0.95), (0.45, "#ffe0a0", 0.4), (1, "#ffe0a0", 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy + 200}" rx="1500" ry="900" fill="url(#s14god)"/>'
               f'<path d="{S.rays(cx, cy, 160, 1500, 13, 5, rot=30)}" fill="#ffdf9a" opacity="0.32" filter="url(#soft)"/>',
               defs)


def david_glow_svg():
    defs = S.rad_grad("s14dg", [(0, "#ffe7a8", 0.75), (0.5, "#ffd98c", 0.3), (1, "#ffd98c", 0)])
    return doc(f'<ellipse cx="{DX + 20}" cy="{GY - 110}" rx="300" ry="240" fill="url(#s14dg)"/>', defs)


def note_svg(i):
    x, y = DX + 120, GY - 230
    d = (f'<ellipse cx="{x}" cy="{y}" rx="14" ry="10" transform="rotate(-20 {x} {y})" fill="#fff3d6" stroke="{INK}" '
         f'stroke-width="3"/><path d="M{x + 12},{y - 3} L{x + 12},{y - 52}" stroke="{INK}" stroke-width="3.5"/>')
    if i % 2:
        d += f'<path d="M{x + 12},{y - 52} q18,6 20,26" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    return doc(S.g(d, filter="wobble-fine"))


# ============================================================================ the picture cards


def card_frame_svg(kind):
    x0, y0, x1, y1 = CARD
    if kind == "chart":
        defs = S.lin_grad("s14c1", [(0, "#fbf3df"), (1, "#f1e3c2")])
    else:
        defs = S.lin_grad("s14c2", [(0, "#8e86b6"), (0.6, "#c7a6c1"), (1, "#e8c3b3")])
    fill = "url(#s14c1)" if kind == "chart" else "url(#s14c2)"
    out = (f'<rect x="{x0 + 10}" y="{y0 + 14}" width="{x1 - x0}" height="{y1 - y0}" rx="34" fill="{INK}" opacity="0.25" '
           f'filter="url(#soft)"/>'
           f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="34" fill="#fffaf0" stroke="{INK}" '
           f'stroke-width="5"/>'
           f'<rect x="{x0 + 18}" y="{y0 + 18}" width="{x1 - x0 - 36}" height="{y1 - y0 - 36}" rx="22" fill="{fill}" '
           f'stroke="{INK}" stroke-width="3"/>')
    if kind == "chart":
        # height ruler with ticks
        rx = x0 + 70
        out += f'<path d="M{rx},{FLOOR} L{rx},{y0 + 50}" stroke="{P["wood"]}" stroke-width="14" stroke-linecap="round"/>'
        for k, y in enumerate(range(FLOOR, y0 + 50, -36)):
            w = 26 if k % 2 == 0 else 14
            out += f'<path d="M{rx},{y} L{rx + w},{y}" stroke="{INK}" stroke-width="3"/>'
        out += f'<path d="M{x0 + 40},{FLOOR} L{x1 - 40},{FLOOR}" stroke="{INK}" stroke-width="4"/>'
    else:
        out += (f'<path d="M{x0 + 18},{FLOOR - 4} Q{(x0 + x1) / 2},{FLOOR - 30} {x1 - 18},{FLOOR - 4} '
                f'L{x1 - 18},{y1 - 40} Q{x1 - 18},{y1 - 18} {x1 - 40},{y1 - 18} L{x0 + 40},{y1 - 18} '
                f'Q{x0 + 18},{y1 - 18} {x0 + 18},{y1 - 40} Z" fill="#7e9a6c" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(out, filter="wobble-fine"), defs)


SIL_DEFS = (f'<filter id="s14sil" x="-20%" y="-10%" width="140%" height="120%">'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d"/>'
            f'<feFlood flood-color="{INK}" result="ink"/><feComposite in="ink" in2="d" operator="in" result="o"/>'
            f'<feFlood flood-color="FILL" result="f"/><feComposite in="f" in2="SourceAlpha" operator="in" result="fi"/>'
            f'<feMerge><feMergeNode in="o"/><feMergeNode in="fi"/></feMerge></filter>')


def silhouette(markup, fill):
    return doc(f'<g filter="url(#s14sil)">{markup}</g>', SIL_DEFS.replace("FILL", fill))


BOY_X, GIANT_X, CHS = 600, 930, 0.62


def chart_boy_svg():
    return silhouette(C.david(BOY_X, FLOOR - 2, CHS, 1, pose="stand"), "#9cc27a")


def chart_giant_svg():
    return silhouette(C.goliath(GIANT_X, FLOOR - 2, CHS, -1, pose="stand", spear=False), "#c9a27a")


def chart_lines_svg(which):
    x0, x1 = CARD[0] + 70, CARD[2] - 50
    y = FLOOR - (252 if which == 0 else 634) * CHS
    col = "#5f9a5a" if which == 0 else "#b06a3a"
    out = (f'<path d="M{x0},{f1(y)} L{x1},{f1(y)}" stroke="{col}" stroke-width="5" stroke-dasharray="16 12" '
           f'stroke-linecap="round"/><circle cx="{x0}" cy="{f1(y)}" r="9" fill="{col}" stroke="{INK}" stroke-width="3"/>')
    return doc(out)


def chart_labels_svg():
    out = (S.text(BOY_X, FLOOR + 36, "大卫", size=34, fill=INK) + S.text(GIANT_X, FLOOR + 36, "歌利亚", size=34, fill=INK))
    return doc(out)


def flex_svg():
    """Little 'puff' ticks around the giant outline when he puffs out ('壮')."""
    out = ""
    cy = FLOOR - 330 * CHS
    for side in (-1, 1):
        for k in range(3):
            a = math.radians(-30 + 30 * k)
            x0 = GIANT_X + side * (150 * CHS + 10)
            out += (f'<path d="M{f1(x0 + side * 14 * math.cos(a))},{f1(cy + 60 * math.sin(a))} '
                    f'l{f1(side * 26 * math.cos(a))},{f1(26 * math.sin(a))}" stroke="{INK}" stroke-width="5" '
                    f'stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


KID_X = 600
KS = 1.0
WORRY = (930, FLOOR + 6)      # the worry giant's base


def kid(pose, expr=None):
    return doc(C.ground_shadow(KID_X, FLOOR, KS, 110) +
               C.citizen(KID_X, FLOOR, KS, 1, kind="child", variant=1, pose=pose, expr=expr))


def worry_svg(k):
    """The worry giant: a soft lumpy shadow cloud with goggly eyes and wiggly arms (silly, not scary)."""
    x, y = WORRY
    rng = random.Random(k * 7 + 1)
    j = lambda a: a + rng.uniform(-6, 6)  # noqa: E731
    body = S.smooth_path([(x - 150, y), (j(x - 165), y - 120), (j(x - 140), y - 250), (j(x - 95), y - 330),
                          (j(x - 20), y - 375), (j(x + 60), y - 365), (j(x + 120), y - 310), (j(x + 150), y - 200),
                          (j(x + 165), y - 90), (x + 150, y), (j(x + 100), y - 20), (j(x + 50), y + 4),
                          (j(x), y - 18), (j(x - 50), y + 4), (j(x - 100), y - 22)])
    wig = 14 * math.sin(k * 2.1)
    arm_l = (f"M{x - 140},{y - 210} Q{x - 230},{y - 250 + wig} {x - 250},{y - 330 - wig} "
             f"Q{x - 214},{y - 320} {x - 200},{y - 290} Q{x - 180},{y - 250} {x - 130},{y - 240} Z")
    arm_r = (f"M{x + 140},{y - 200} Q{x + 230},{y - 240 - wig} {x + 240},{y - 320 + wig} "
             f"Q{x + 206},{y - 312} {x + 192},{y - 284} Q{x + 172},{y - 244} {x + 130},{y - 232} Z")
    col = "#4f4c6e"
    out = (f'<path d="{arm_l}" fill="{col}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
           f'<path d="{arm_r}" fill="{col}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
           f'<path d="{body}" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
           f'<path d="M{x - 90},{y - 300} Q{x - 40},{y - 345} {x + 20},{y - 340}" fill="none" stroke="#6d6a90" '
           f'stroke-width="10" stroke-linecap="round"/>')
    # goggly eyes (looking down at the child), wobbly brows, a wiggly 'oooh' mouth
    for ex, er in ((x - 48, 34), (x + 34, 28)):
        out += (f'<circle cx="{ex}" cy="{y - 250}" r="{er}" fill="#f6f0dc" stroke="{INK}" stroke-width="4"/>'
                f'<circle cx="{ex - 12}" cy="{y - 238}" r="{er * 0.42:.1f}" fill="{INK}"/>'
                f'<circle cx="{ex - 15}" cy="{y - 243}" r="4" fill="#f6f0dc"/>')
    out += (f'<path d="M{x - 82},{y - 296} q30,-18 58,-4 M{x + 14},{y - 288} q24,-16 48,0" fill="none" '
            f'stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{x - 40},{y - 180} q14,-14 28,0 q14,14 28,0 q14,-14 28,0" fill="none" stroke="#f6f0dc" '
            f'stroke-width="6" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def card_light_svg():
    x0, y0, x1, y1 = CARD
    cx = (x0 + x1) / 2
    defs = S.rad_grad("s14cl", [(0, "#fff0c0", 0.95), (0.5, "#ffe0a0", 0.45), (1, "#ffe0a0", 0)])
    body = (f'<clipPath id="s14cc"><rect x="{x0 + 18}" y="{y0 + 18}" width="{x1 - x0 - 36}" height="{y1 - y0 - 36}" '
            f'rx="22"/></clipPath><g clip-path="url(#s14cc)">'
            f'<ellipse cx="{cx - 100}" cy="{y0}" rx="520" ry="420" fill="url(#s14cl)"/>'
            f'<path d="{S.rays(cx - 100, y0 - 40, 40, 620, 9, 7, rot=40)}" fill="#fff0c4" opacity="0.45" '
            f'filter="url(#soft)"/></g>')
    return doc(body, defs)


def card_stars_svg():
    x0, y0, x1, _ = CARD
    rng = random.Random(5)
    out = ""
    for _ in range(14):
        x, y = rng.uniform(x0 + 60, x1 - 60), rng.uniform(y0 + 50, y0 + 260)
        r = rng.uniform(5, 9)
        out += (f'<path d="M{f1(x)},{f1(y - r)} L{f1(x + r * 0.28)},{f1(y - r * 0.28)} L{f1(x + r)},{f1(y)} '
                f'L{f1(x + r * 0.28)},{f1(y + r * 0.28)} L{f1(x)},{f1(y + r)} L{f1(x - r * 0.28)},{f1(y + r * 0.28)} '
                f'L{f1(x - r)},{f1(y)} L{f1(x - r * 0.28)},{f1(y - r * 0.28)} Z" fill="#fff3c8"/>')
    return doc(out)


def puffs_svg(i):
    x, y = WORRY
    rng = random.Random(i + 20)
    out = ""
    for k in range(3):
        px = x + rng.uniform(-150, 150)
        py = y - rng.uniform(60, 340)
        w = rng.uniform(46, 76)
        out += S.cloud(px, py, w, w * 0.62, "#8a87ad", seed=i * 5 + k, puffs=3, sw=2.4, shade_fill="#6d6a90")
    return doc(S.g(out, filter="wobble-fine"))


def end_card_svg():
    out = (f'<ellipse cx="{CARD_X}" cy="{CARD_Y - 40}" rx="760" ry="200" fill="url(#s14card)"/>' +
           S.text(CARD_X, CARD_Y, "大卫和歌利亚 · 完", size=132, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    defs = S.rad_grad("s14card", [(0, "#ffe9bb", 0.4), (0.6, "#ffd9a8", 0.14), (1, "#ffd9a8", 0)])
    return doc(out, defs)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]
    _, cam_path = make_cam(SW, SH)
    BOT = SH - 4

    t_chart = L0.start + 0.05
    t_tall = when(ctx, "高") - 0.35
    t_strong = when(ctx, "也不比") + 0.4
    t_but = L0.chunks[1].start
    t_god = when(ctx, "上帝比任何") + 0.2
    t_card = L1.start + 0.05
    t_worry = L1.chunks[1].start + 0.15
    t_like = when(ctx, "像大卫")
    t_pray = snap(when(ctx, "对上帝说") + 0.05)
    t_believe = when(ctx, "我相信")
    t_gone = t_believe + 0.3
    t_smile = snap(t_gone + 0.7)
    t_card_out = min(L2.end - 0.9, t_gone + 1.6)
    t_end = t_card_out + 0.45
    t_still = T - 0.6

    # ---- camera
    CA = cam_at(1300, 1900, BOT)
    CS = Cam(1300, 680, 2300)
    CEND = cam_at(1300, 2120, BOT)
    sc.camera = cam_path([(0, CA), (t_but + 0.3, CA), (t_god + 0.5, CS), (L0.end + 0.4, CS), (t_card + 0.6, CA),
                          (t_card_out, CA), (t_end + 1.2, CEND), (T, CEND)])
    still = lambda t: 1.0 - M.progress(t, t_still - 0.8, t_still, "sine")  # noqa: E731

    # ---- sky
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("stars", stars_svg(), z=0.2, wc=0.2,
           motion=lambda t: Tf(alpha=0.55 + 0.45 * M.progress(t, t_god - 0.5, t_god + 1.5, "sine")))
    sc.add("god", glow_god_svg(), z=0.3, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.85 * M.progress(t, t_god - 0.4, t_god + 1.3, "sine") *
                               (1 - 0.55 * M.progress(t, L0.end + 0.4, t_card + 1.0, "sine")) +
                               0.3 * M.progress(t, t_pray, t_pray + 1.5, "sine") *
                               (1 - 0.4 * M.progress(t, t_end, T, "sine"))))
    sc.add("clouds", clouds_svg(), z=0.4, wc=0.6, motion=lambda t: Tf(dx=-6 * min(t, t_still)))
    sc.add("hills", hills_svg(), z=1)
    sc.add("hilltop", hilltop_svg(), z=2)
    sc.fx.append(FX.sparkles((150, 60, 2450, 700), count=26, t0=t_god - 0.2, t1=t_still, size=(8, 18), drift=4,
                             seed=31))
    sc.fx.append(FX.motes((300, 1400, 2400, 1700), count=14, color=(255, 236, 160), size=(3, 6), seed=17, alpha=170))

    # ---- David and his sheep
    sc.add("dglow", david_glow_svg(), z=2.4, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.35 + 0.65 * M.progress(t, t_like, t_like + 0.6, "sine") *
                               (1 - 0.6 * M.progress(t, t_pray + 0.5, t_pray + 2.0, "sine"))))
    dfr = [doc(C.ground_shadow(DX, GY, SCD, 200) + C.david(DX, GY, SCD, 1, pose="sit_harp", expr=e))
           for e in ("peaceful", "kind", blink_expr("kind"))]
    dbase = [(0, 0), (snap(t_like + 0.1), 1), (snap(t_pray + 1.2), 0), (snap(t_end + 0.3), 1)]
    dbase = with_blinks(dbase, {1: 2}, [t_like + 1.2, T - 1.0])
    sc.add("david", dfr, z=3, frame_at=cuts(dbase),
           motion=M.combine(lambda t: Tf(dy=-3 * abs(math.sin(math.pi * t / 0.9)) * still(t)),
                            lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * t / 1.8) * still(t), px=DX, py=GY),
                            dip(snap(t_like + 0.1), SCD, (DX, GY), 4), dip(snap(t_end + 0.3), SCD, (DX, GY), 4)))
    for i in range(4):
        per = 3.2

        def nm(t, i=i, per=per):
            u = ((t + i * per / 4) % per) / per
            a = math.sin(math.pi * u) * still(t) if t < t_still else 0.0
            return Tf(dx=40 * u + 18 * math.sin(2 * math.pi * u + i), dy=-170 * u, alpha=a)
        sc.add(f"note{i}", note_svg(i), z=3.1, wc=0.2, motion=nm)
    SHEEP = [(1240, GY + 20, 1.05, 1, 0, False, "graze"), (1880, GY + 16, 1.1, -1, 1, False, "stand"),
             (2130, GY + 48, 1.0, -1, 3, False, "graze"), (1060, GY + 78, 1.0, 1, 2, True, "stand"),
             (870, GY + 40, 0.95, 1, 2, False, "stand")]
    for i, (x, y, s, f, v, lamb, p0) in enumerate(SHEEP):
        fr = [doc(C.ground_shadow(x, y, s, 190 if not lamb else 130, 0.2) +
                  PR.sheep(x, y, s, f, variant=v, pose=p, lamb=lamb)) for p in ("stand", "graze")]
        rng = random.Random(i + 3)
        k0 = 0 if p0 == "stand" else 1
        ents = [(0, k0)]
        tt = rng.uniform(3, 5)
        while tt < t_still - 1.5:
            ents.append((snap(tt), 1 - ents[-1][1]))
            tt += rng.uniform(3.5, 6)
        sc.add(f"sheep{i}", fr, z=2.6 + 0.05 * (y - GY) / 10, frame_at=cuts(ents),
               motion=M.combine(lambda t, x=x, y=y, ph=rng.uniform(0, 1): Tf(
                   sx=1 + 0.013 * math.sin(2 * math.pi * (t / 2.8 + ph)) * still(t),
                   sy=1 + 0.013 * math.sin(2 * math.pi * (t / 2.8 + ph)) * still(t), px=x, py=y),
                   *[hop(tk, [(-0.06, {"sy": 1}), (0, {"sy": 0.96}), (0.16, {"sy": 1})], (x, y))
                     for tk, _ in ents[1:]]))
    # his shepherd's bag (four stones left: he needed only one)
    sc.add("props", doc(C.ground_shadow(DX + 175, GY + 22, 1, 110, 0.2) +
                        PR.shepherd_bag(DX + 175, GY + 22, 0.82, -1, stones=4, strap=False)), z=3.05)
    sc.add("fg", [fg_svg(k) for k in range(3)], z=5, frame_at=lambda t: float(int(t * 2.0) % 3) if t < t_still else 0.0)

    # ---- card 1: the measuring chart (line 0)
    ccx, ccy = (CARD[0] + CARD[2]) / 2, (CARD[1] + CARD[3]) / 2
    t_c1_out = t_but + 0.15

    def card_in_out(t_in, t_out, piv=(ccx, ccy)):
        return M.keys([(t_in - 0.01, {"alpha": 0, "s": 0.6, "dy": 30}), (t_in + 0.3, {"alpha": 1, "s": 1.04, "dy": 0}),
                       (t_in + 0.45, {"s": 1.0}), (t_out, {"alpha": 1, "s": 1.0, "dy": 0, "rot": 0}),
                       (t_out + 0.45, {"alpha": 0, "s": 0.5, "dy": -160, "rot": -8})],
                      ["out", "sine", "linear", "in"], pivot=piv)
    c1 = lambda: card_in_out(t_chart, t_c1_out)  # noqa: E731
    sc.add("card1", card_frame_svg("chart"), z=6, wc=0.4, motion=c1())
    sc.add("chart_lab", chart_labels_svg(), z=6.05, wc=0, motion=c1())
    sc.add("chart_l0", chart_lines_svg(0), z=6.06, wc=0,
           motion=M.combine(c1(), lambda t: Tf(alpha=M.progress(t, t_chart + 0.5, t_chart + 0.8))))
    sc.add("chart_l1", chart_lines_svg(1), z=6.06, wc=0,
           motion=M.combine(c1(), lambda t: Tf(alpha=M.progress(t, t_tall + 0.5, t_tall + 0.8))))
    sc.add("chart_boy", chart_boy_svg(), z=6.1, wc=0.3,
           motion=M.combine(c1(), M.keys([(t_chart + 0.2, {"alpha": 0, "sy": 0.3}), (t_chart + 0.45, {"alpha": 1, "sy": 1.08}),
                                          (t_chart + 0.6, {"sy": 1.0})], "out", pivot=(BOY_X, FLOOR)),
                            hop(t_strong + 0.5, [(0, {"dy": 0}), (0.12, {"dy": -16}), (0.3, {"dy": 0})], (BOY_X, FLOOR))))
    sc.add("chart_giant", chart_giant_svg(), z=6.1, wc=0.3,
           motion=M.combine(c1(), M.keys([(t_tall - 0.3, {"alpha": 0, "sy": 0.2, "sx": 0.9}),
                                          (t_tall - 0.2, {"alpha": 1}), (t_tall + 0.45, {"sy": 1.06, "sx": 1.0}),
                                          (t_tall + 0.6, {"sy": 1.0}), (t_strong, {"sx": 1.0}),
                                          (t_strong + 0.25, {"sx": 1.22, "sy": 1.02}), (t_strong + 0.45, {"sx": 1.12, "sy": 1.0}),
                                          (t_strong + 0.7, {"sx": 1.16})],
                                         ["out", "out", "out", "sine", "linear", "out", "sine", "sine"],
                                         pivot=(GIANT_X, FLOOR))))
    sc.add("flex", flex_svg(), z=6.15, wc=0,
           motion=M.combine(c1(), lambda t: Tf(alpha=1.0 if t_strong + 0.2 <= t < t_strong + 1.1 else 0.0)))

    # ---- card 2: the child and the worry giant (lines 1-2)
    c2 = lambda: card_in_out(t_card, t_card_out)  # noqa: E731
    sc.add("card2", card_frame_svg("worry"), z=6, wc=0.4, motion=c2())
    sc.add("card_stars", card_stars_svg(), z=6.02, wc=0,
           motion=M.combine(c2(), lambda t: Tf(alpha=M.progress(t, t_gone + 0.2, t_gone + 0.9) *
                                               (0.75 + 0.25 * math.sin(t * 4)))))
    sc.add("card_light", card_light_svg(), z=6.03, wc=0, blend="screen",
           motion=M.combine(c2(), lambda t: Tf(alpha=M.progress(t, t_pray, t_pray + 1.0, "sine"))))
    wx, wy = WORRY
    sc.add("worry", [worry_svg(k) for k in range(3)], z=6.05, wc=0.4, frame_at=lambda t: float(int(t * 4) % 3),
           motion=M.combine(c2(),
                            M.keys([(t_worry - 0.01, {"alpha": 0, "s": 0.25}), (t_worry + 0.2, {"alpha": 0.95}),
                                    (t_worry + 1.3, {"s": 1.0}), (t_gone, {"s": 1.0, "alpha": 0.95}),
                                    (t_gone + 0.15, {"s": 1.06}), (t_gone + 0.75, {"s": 0.15, "alpha": 0})],
                                   ["out", "out", "linear", "sine", "in"], pivot=(wx, wy)),
                            lambda t: Tf(sx=1 + 0.03 * math.sin(t * 3.1), sy=1 + 0.025 * math.sin(t * 2.3 + 1),
                                         px=wx, py=wy)))
    for i in range(4):
        tp = t_gone + 0.35 + 0.12 * i
        sc.add(f"puff{i}", puffs_svg(i), z=6.06, wc=0,
               motion=M.combine(c2(), M.keys([(tp - 0.01, {"alpha": 0, "s": 0.5, "dy": 0}),
                                              (tp + 0.15, {"alpha": 0.9, "s": 1.0}),
                                              (tp + 1.2, {"alpha": 0, "s": 0.7, "dy": -150})], ["out", "sine"],
                                             pivot=(wx, wy - 200))))
    kfr = [kid("stand", "neutral"), kid("stand", "worried"), kid("kneel_pray", "worried"), kid("kneel_pray"),
           kid("kneel_pray", "dv14_smile"), kid("stand", blink_expr("worried"))]
    kbase = [(0, 0), (snap(t_worry + 0.5), 1), (t_pray, 2), (snap(t_pray + 0.9), 3), (t_smile, 4)]
    kbase = with_blinks(kbase, {1: 5}, [13.6, 14.6])
    tremble = lambda t: Tf(dx=1.6 * math.sin(t * 37) if t_worry + 0.6 < t < t_pray - 0.1 else 0.0)  # noqa: E731
    sc.add("kid", kfr, z=6.1, wc=0.5, frame_at=cuts(kbase),
           motion=M.combine(c2(), tremble, dip(snap(t_worry + 0.5), KS, (KID_X, FLOOR), 6),
                            dip(t_pray, KS, (KID_X, FLOOR), 10), dip(t_smile, KS, (KID_X, FLOOR), 4),
                            M.breathe(0.012, 2.6, pivot=(KID_X, FLOOR))))

    # ---- end card
    sc.add("endcard", end_card_svg(), z=7, wc=0, motion=M.keys(
        [(t_end, {"alpha": 0, "s": 0.95, "dy": 16}), (t_end + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(CARD_X, CARD_Y - 50)))
    hx, hy = CARD_X, CARD_Y + 72
    th = t_end + 0.5
    sc.add("heart", doc(heart_markup(hx, hy, 30)), z=7.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))
    sc.fx.append(FX.vignette(lambda t: 0.3))

    # ---- sound
    sc.sfx("night", 0.0, dur=T, gain_db=-18, fade_in=0.8, fade_out=1.5)
    sc.sfx("pop", t_chart + 0.1, gain_db=-14)
    sc.sfx("grow", t_tall - 0.3, gain_db=-15)
    sc.sfx("pop", t_strong + 0.2, gain_db=-12)
    sc.sfx("whoosh", t_c1_out, gain_db=-16)
    sc.sfx("chime", t_god, gain_db=-12)
    sc.sfx("pop", t_card + 0.1, gain_db=-14)
    sc.sfx("cloth", t_pray, gain_db=-16)
    sc.sfx("sparkle", t_pray + 0.3, gain_db=-15)
    sc.sfx("wither", t_gone, gain_db=-17)
    sc.sfx("pop", t_gone + 0.4, gain_db=-14)
    sc.sfx("whoosh", t_card_out, gain_db=-17)
    sc.sfx("chime", t_end + 0.1, gain_db=-13)
    return sc
