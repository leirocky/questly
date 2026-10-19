"""Scene 7 — Israel's camp: Goliath's voice, the soldiers run, David asks, Eliab scolds (1 Samuel 17:20-30).

One 3000 x 1300 stage, no cuts: Israel's camp on the hilltop in front (a big striped goat-hair tent on the left,
another on the right, blue banners, a rack of spears and shields, a campfire with a pot on a tripod, a supply cart
with sacks and jars); behind the camp the valley, and across it the Philistine hill with its red tents, where
Goliath stands, small in the distance (but still very big!).

  line 0  '大卫刚到军营，'  David walks in from the left with his basket (planted-foot strides); a soldier waves.
          '就听见了一个好大好大的声音。'  far across the valley Goliath raises his spear and roars: sound rings roll
          over the camp, the tents shake, the pot lid rattles (clatter), the banners whip; David is startled.
  line 1  Goliath: '胆小鬼们！谁敢出来跟我打？'  the camera zooms across the valley to him (shouting, a jagged
          shout burst with '!!'), two more booming beats shake the camp.
  line 2  '以色列的士兵一看见歌利亚，'  the camera pulls back; the soldiers see him and go scared and trembly
          (Goliath points at them). '转身就跑。'  they turn and run (run cycles) past David - whoosh! - his
          basket flies out of his hand and bumps onto the ground, he spins round to watch them; one hides behind the
          big tent and peeks out trembling; Goliath laughs (ha ha).
  line 3  David: '这个人是谁？'  puzzled, looking at the giant.  '他怎么敢骂永生上帝的军队呢？'  he becomes brave
          and points up to heaven at '永生上帝' (a glint of golden light in the sky).
  line 4  '大卫的大哥以利押听见了，很生气。'  Eliab marches in from the right, cross; at '很生气' he plants his
          fists on his hips and a little grumble cloud puffs over his head.
  line 5  Eliab: '你来这里做什么？'  he points at David (scold).  '你的羊谁看着呢？'  hands on hips; a small thought
          bubble with a sheep pops up.  '你就是来看热闹的吧！'  scold again, wagging the finger.
  line 6  David: '我又做了什么呢？'  open hands with a little shrug.  '我只是问问而已。'  kind and calm; Eliab
          huffs. Calm end frame.

Pose changes are hard cuts hidden in squashes; runs are 2-frame cycles; booms are layer shakes. Goliath is big and
loud but a little comic. All times derive from the narration chunks.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import (arcs_markup, cuts, dip, grumble_markup, happy_hop, hop, nod, question_markup, snap)
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import (actor, blink_expr, cam_at, make_cam, scallop_path, tuft_row, when,
                                               with_blinks)

SW, SH = 3000, 1300
INK = P["ink"]
GY = 1140
SC = 1.05
WALK_P = 0.27
GOL = (1960, 812, 0.31)        # Goliath far across the valley (x, ground y, scale)
DX = 1000                      # David's spot
EX = 1300                      # Eliab's spot
TENT_A = (300, 1150, 0.95)     # big tent on the left (soldiers hide behind it)
FIRE = (1700, 1062)
CART = (2560, 1080)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ drawings


def sky_svg():
    defs = S.lin_grad("s7sky", [(0, "#93c6dc"), (0.6, "#c7e2e4"), (1, "#f3e6c6")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s7sky)"/>', defs)


def clouds_svg():
    out = ""
    for cx, cy, w, h, sd in ((300, 200, 340, 80, 1), (1100, 120, 280, 64, 2), (1750, 240, 380, 86, 3),
                             (2500, 150, 330, 74, 4), (3050, 280, 260, 60, 5)):
        out += S.cloud(cx, cy, w, h, fill="#fbf4e6", seed=sd + 10, sw=3, shade_fill="#dbe3e6")
    return doc(S.g(out, filter="wobble"))


def far_svg():
    """Hazy ridges, the Philistine hill across the valley with red tents, the valley floor and brook."""
    out = ""
    out += S.path(S.hill(-60, SW + 60, 760, 150, seed=31, bumps=4), "#c2d2c4", sw=3)
    # Philistine hill (right half), with a little rocky ledge where Goliath stands
    hill = S.smooth_path([(900, 900), (1300, 820), (1700, 720), (2050, 650), (2400, 610), (2800, 620), (3100, 660)],
                         closed=False) + " L3100,1000 L900,1000 Z"
    out += S.path(hill, "#c6c189", sw=4)
    out += S.path(S.smooth_path([(1250, 900), (1600, 860), (1960, 818), (2300, 800), (2700, 790), (3100, 800)],
                                closed=False) + " L3100,1000 L1250,1000 Z", "#b8b47c", sw=3.5)
    for x, y, s in ((2250, 640, 0.24), (2470, 618, 0.27), (2700, 626, 0.25), (2900, 640, 0.23), (2080, 668, 0.22)):
        out += PR.tent(x, y, s, -1, side="philistine")
    for x, y, s in ((1700, 760, 0.28), (2600, 700, 0.3), (1380, 840, 0.25), (2200, 712, 0.24)):
        out += PR.bush(x, y, s, variant=2)
    for x, y, s, sd in ((1520, 800, 0.26, 1), (2380, 650, 0.22, 2), (2830, 652, 0.2, 3), (1220, 862, 0.22, 4)):
        out += PR.olive_tree(x, y, s, seed=sd)
    for x, y, s in ((300, 772, 0.2), (520, 760, 0.22), (760, 768, 0.2)):
        out += PR.olive_tree(x, y, s, seed=int(x))
    # rocky ledge under Goliath
    gx, gy, _ = GOL
    out += (f'<path d="M{gx - 120},{gy + 14} Q{gx - 90},{gy - 8} {gx},{gy - 6} Q{gx + 90},{gy - 8} {gx + 130},{gy + 16} Z" '
            f'fill="#d3c39a" stroke="{INK}" stroke-width="3.5"/>')
    # valley floor with the brook
    defs = S.lin_grad("s7val", [(0, "#bdcf93"), (1, "#a9c27f")])
    out += S.path(f"M-60,880 Q800,860 1500,890 Q2300,910 {SW + 60},880 L{SW + 60},1000 L-60,1000 Z", "url(#s7val)",
                  sw=3.5)
    out += (f'<path d="M-60,912 Q700,900 1400,922 Q2200,944 {SW + 60},914" fill="none" stroke="#7fb8cc" '
            f'stroke-width="14" stroke-linecap="round"/><path d="M-60,912 Q700,900 1400,922 Q2200,944 {SW + 60},914" '
            f'fill="none" stroke="#d5eef0" stroke-width="3" stroke-dasharray="20 26"/>')
    return doc(S.g(out, filter="wobble"), defs)


def plateau_svg():
    """The hilltop the camp stands on (front), trodden ground and grass."""
    defs = S.lin_grad("s7gr", [(0, "#a6bf6c"), (0.35, "#c7b98a"), (1, "#b9a274")])
    out = S.path(S.wave_band(950, 12, 1100, 0.3, x0=-60, x1=SW + 60, bottom=SH + 60, seed=4), "url(#s7gr)", sw=4.5)
    rng = random.Random(7)
    for _ in range(46):
        x, y = rng.uniform(0, SW), rng.uniform(1000, 1290)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(8, 18))}" ry="{f1(rng.uniform(4, 7))}" '
                f'fill="#a88f62" opacity="0.6"/>')
    for x, y, s, v in ((80, 975, 0.6, 0), (700, 968, 0.5, 1), (2050, 975, 0.6, 0), (2850, 970, 0.55, 1),
                       (1800, 990, 0.45, 2)):
        out += PR.grass_tuft(x, y, s, variant=v)
    for x, y in ((620, 985), (2280, 990)):
        out += (f'<ellipse cx="{x}" cy="{y}" rx="44" ry="24" fill="#c9b893" stroke="{INK}" stroke-width="3.5"/>'
                f'<ellipse cx="{x + 40}" cy="{y + 8}" rx="26" ry="15" fill="#bba982" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(out, filter="wobble"), defs)


def banner_markup(x, y, h=330, wave=0.0, col="#4a78b0"):
    """A pole with a blue banner (cream band); ``wave`` 0..1 ripples it."""
    ph = 2 * math.pi * wave
    top = y - h
    pts_t = [(x + 6 + k * 22, top + 10 + 8 * math.sin(ph + k * 0.9)) for k in range(7)]
    pts_b = [(x + 6 + k * 22, top + 92 + 8 * math.sin(ph + k * 0.9) + k * 2.5) for k in range(7)][::-1]
    d = S.smooth_path(pts_t, closed=False) + " L" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts_b[:1])
    d += " " + S.smooth_path(pts_b, closed=False).replace("M", "L", 1) + " Z"
    band = S.smooth_path([(a, b + 38) for a, b in pts_t], closed=False)
    return (f'<path d="M{x},{y} L{x},{top - 8}" stroke="{P["wood_dark"]}" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{top - 12}" r="9" fill="{P["gold"]}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="{band}" fill="none" stroke="#efe3c6" stroke-width="12"/>')


def camp_back_svg(wave=0.0):
    """Camp pieces behind the people: the right tent, banners, the spear rack."""
    out = PR.tent(2830, 1010, 0.7, -1, side="israel", flag=False)
    out += PR.tent(1110, 975, 0.5, 1, side="israel", flag=False)
    for x, y, h in ((700, 990, 330), (1520, 1000, 300), (2470, 1000, 320)):
        out += banner_markup(x, y, h, wave + x * 0.001)
    # spear and shield rack
    rx, ry = 2230, 1030
    for k in range(4):
        out += (f'<path d="M{rx - 60 + k * 36},{ry} L{rx - 40 + k * 36},{ry - 250}" stroke="{P["wood"]}" '
                f'stroke-width="8" stroke-linecap="round"/><path d="M{rx - 46 + k * 36},{ry - 248} l6,-34 l8,30 Z" '
                f'fill="#b9b2a4" stroke="{INK}" stroke-width="2.5"/>')
    out += (f'<path d="M{rx - 90},{ry - 120} L{rx + 110},{ry - 120}" stroke="{P["wood_dark"]}" stroke-width="10" '
            f'stroke-linecap="round"/>')
    for k in range(2):
        out += PR.round_shield(rx - 30 + k * 96, ry - 70, 0.9, kind="israel", rot=-8 + 16 * k)
    return doc(S.g(out, filter="wobble-fine"))


def tent_a_svg(wave):
    x, y, s = TENT_A
    return doc(C.ground_shadow(x, y, s, 600, 0.16) + PR.tent(x, y, s, 1, side="israel", wave=wave))


def cart_svg():
    x, y = CART
    out = ""
    out += PR.sack(x - 90, y - 92, 0.7, seed=2) + PR.sack(x + 10, y - 96, 0.75, seed=5)
    out += PR.jar(x + 105, y - 150, 0.55)
    out += (f'<path d="M{x - 190},{y - 100} L{x + 170},{y - 100} L{x + 160},{y - 40} L{x - 180},{y - 40} Z" '
            f'fill="{P["wood"]}" stroke="{INK}" stroke-width="4.5"/>'
            f'<path d="M{x - 185},{y - 70} L{x + 165},{y - 70}" stroke="{P["wood_dark"]}" stroke-width="3"/>'
            f'<path d="M{x - 180},{y - 50} L{x - 330},{y + 50}" stroke="{P["wood_dark"]}" stroke-width="12" '
            f'stroke-linecap="round"/>')
    wx, wy, r = x + 20, y - 8, 66
    spokes = "".join(f'<path d="M{wx},{wy} L{f1(wx + r * math.cos(a))},{f1(wy + r * math.sin(a))}" '
                     f'stroke="{P["wood_dark"]}" stroke-width="6"/>' for a in [k * math.pi / 4 for k in range(8)])
    out += (f'<circle cx="{wx}" cy="{wy}" r="{r}" fill="none" stroke="{P["wood"]}" stroke-width="14"/>'
            f'<circle cx="{wx}" cy="{wy}" r="{r + 7}" fill="none" stroke="{INK}" stroke-width="3.5"/>'
            f'<circle cx="{wx}" cy="{wy}" r="{r - 7}" fill="none" stroke="{INK}" stroke-width="3"/>' + spokes +
            f'<circle cx="{wx}" cy="{wy}" r="13" fill="{P["wood_light"]}" stroke="{INK}" stroke-width="3"/>')
    return doc(C.ground_shadow(x, y + 56, 1, 420, 0.16) + S.g(out, filter="wobble-fine"))


def fire_svg():
    x, y = FIRE
    out = ""
    for k in range(7):
        a = math.pi * k / 6
        out += (f'<ellipse cx="{f1(x + 90 * math.cos(a) * 1.0 - 0)}" cy="{f1(y + 8 - 12 * math.sin(a))}" rx="24" ry="15" '
                f'fill="#b8ad9c" stroke="{INK}" stroke-width="3"/>')
    out += (f'<path d="M{x - 70},{y - 4} L{x + 70},{y - 26}" stroke="{P["wood_dark"]}" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M{x - 66},{y - 26} L{x + 70},{y - 2}" stroke="{P["wood"]}" stroke-width="18" stroke-linecap="round"/>')
    # tripod
    out += (f'<path d="M{x - 95},{y + 10} L{x},{y - 250} L{x + 95},{y + 10} M{x},{y - 250} L{x + 14},{y + 16}" '
            f'fill="none" stroke="{P["wood_dark"]}" stroke-width="8" stroke-linecap="round"/>')
    out += f'<path d="M{x},{y - 246} L{x},{y - 160}" stroke="{INK}" stroke-width="3"/>'
    return doc(S.g(out, filter="wobble-fine"))


def flame_svg(k):
    x, y = FIRE
    rng = random.Random(k)
    h = 120 + 18 * math.sin(k * 2.1)
    d = (f"M{x - 52},{y - 12} Q{x - 64},{y - h * 0.5} {x - 18 + rng.uniform(-8, 8)},{y - h} "
         f"Q{x - 6},{y - h * 0.55} {x + 8},{y - h * 0.8 + rng.uniform(-10, 10)} Q{x + 30},{y - h * 0.45} "
         f"{x + 34 + rng.uniform(-6, 6)},{y - h * 0.75} Q{x + 66},{y - h * 0.35} {x + 52},{y - 12} Z")
    d2 = (f"M{x - 28},{y - 14} Q{x - 32},{y - h * 0.4} {x - 6},{y - h * 0.62} Q{x + 6},{y - h * 0.35} "
          f"{x + 18},{y - h * 0.5} Q{x + 36},{y - h * 0.3} {x + 28},{y - 14} Z")
    defs = S.rad_grad(f"s7fg{k}", [(0, "#ffdc8a", 0.6), (1, "#ffdc8a", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y - 60}" rx="190" ry="140" fill="url(#s7fg{k})"/>' +
               S.g(f'<path d="{d}" fill="#f6a43c" stroke="{INK}" stroke-width="3.5"/><path d="{d2}" fill="#fbd46b"/>',
                   filter="wobble-fine"), defs)


def pot_svg(k):
    """The pot hanging on the tripod; k = 0 rest, 1 / 2 lid jumping (rattle)."""
    x, y = FIRE[0], FIRE[1] - 160
    lid = ((0, 0), (-7, -14), (6, -10))[k]
    lr = (0, -12, 10)[k]
    out = (f'<path d="M{x - 52},{y + 16} Q{x - 62},{y + 92} {x},{y + 98} Q{x + 62},{y + 92} {x + 52},{y + 16} Z" '
           f'fill="#6e6a66" stroke="{INK}" stroke-width="4"/>'
           f'<path d="M{x - 40},{y + 10} Q{x},{y - 22} {x + 40},{y + 10}" fill="none" stroke="{INK}" stroke-width="3"/>'
           f'<g transform="translate({lid[0]},{lid[1]}) rotate({lr} {x} {y + 14})">'
           f'<path d="M{x - 56},{y + 16} Q{x},{y - 8} {x + 56},{y + 16} Z" fill="#8a847c" stroke="{INK}" '
           f'stroke-width="4"/><circle cx="{x}" cy="{y}" r="9" fill="#8a847c" stroke="{INK}" stroke-width="3"/></g>')
    if k:
        out += (f'<path d="M{x - 80},{y - 10} l-18,-12 M{x + 78},{y - 14} l18,-14 M{x - 74},{y + 30} l-22,-2" '
                f'stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def steam_svg(k):
    x, y = FIRE[0], FIRE[1] - 180
    out = ""
    for i in range(3):
        yy = y - 40 - 50 * i - 10 * k
        out += (f'<path d="M{x - 10 + 14 * i},{yy} q-16,-20 0,-40 q16,-20 0,-40" fill="none" stroke="#fdf6e6" '
                f'stroke-width="7" stroke-linecap="round" opacity="{0.55 - 0.15 * i}"/>')
    return doc(out)


def gol(pose, expr=None):
    x, y, s = GOL
    return doc(C.ground_shadow(x, y, s, 260, 0.2) + C.goliath(x, y, s, -1, pose=pose, expr=expr))


def burst_svg(k):
    """Jagged shout burst beside Goliath's head with '!!'."""
    x, y = GOL[0] - 230, GOL[1] - 260
    rng = random.Random(k + 3)
    pts = []
    n = 18
    for i in range(n):
        a = 2 * math.pi * i / n
        r = (1.0 if i % 2 == 0 else 0.68) + rng.uniform(-0.07, 0.07)
        pts.append((x + 120 * r * math.cos(a), y + 82 * r * math.sin(a)))
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    tail = f"M{x + 60},{y + 40} L{x + 175},{y + 70} L{x + 85},{y + 18} Z"
    body = (f'<path d="{tail}" fill="#fff3d6" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="#fff3d6" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    txt = S.text(x, y + 30, "!!", size=92, fill="#c9503a", extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"')
    return doc(S.g(body, filter="wobble-fine") + txt)


def rings_svg(k):
    """Booming sound rings rolling from the giant toward the camp (left)."""
    x, y = GOL[0] - 60, GOL[1] - 170
    out = ""
    for i in range(3):
        r = 80 + 90 * i + 30 * k
        a0, a1 = math.radians(140), math.radians(220)
        p0 = (x + r * math.cos(a0), y + r * math.sin(a0))
        p1 = (x + r * math.cos(a1), y + r * math.sin(a1))
        out += (f'<path d="M{f1(p0[0])},{f1(p0[1])} A{r},{r} 0 0,1 {f1(p1[0])},{f1(p1[1])}" fill="none" '
                f'stroke="#fff6e2" stroke-width="16" stroke-linecap="round" opacity="0.6"/>'
                f'<path d="M{f1(p0[0])},{f1(p0[1])} A{r},{r} 0 0,1 {f1(p1[0])},{f1(p1[1])}" fill="none" '
                f'stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity="0.85"/>')
    return doc(S.g(out, filter="wobble-fine"))


def haha_svg(k):
    x, y = GOL[0] + 70, GOL[1] - 250
    t = "哈哈" if k == 0 else "哈"
    return doc(S.text(x + 10 * k, y - 18 * k, t, size=54, fill="#fff3d6",
                      extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"'))


def whoosh_svg(x, y, k):
    out = ""
    for i in range(3):
        yy = y - 40 + 34 * i + 4 * k
        out += (f'<path d="M{x + 30 + 20 * i},{yy} q90,-10 190,0" fill="none" stroke="{INK}" stroke-width="5" '
                f'stroke-linecap="round" opacity="0.7"/>')
    return doc(S.g(out, filter="wobble-fine"))


def dust_svg(x, y, seed=0):
    rng = random.Random(seed)
    out = ""
    for i in range(4):
        px = x + i * 34 + rng.uniform(-6, 6)
        sz = rng.uniform(40, 62)
        out += S.cloud(px, y - rng.uniform(0, 14), sz, sz * 0.6, "#efe2c4", seed=seed * 9 + i, puffs=3, sw=2.4,
                       shade_fill="#d8c7a0")
    return doc(S.g(out, filter="wobble-fine", opacity=0.9))


def sheep_bubble_svg():
    x, y = EX + 120, GY - 520
    out = (f'<path d="{scallop_path(x, y, 120, 82, 12, 0.5)}" fill="#fffaf0" stroke="{INK}" stroke-width="4.5"/>'
           f'<circle cx="{x - 70}" cy="{y + 110}" r="15" fill="#fffaf0" stroke="{INK}" stroke-width="3.5"/>'
           f'<circle cx="{x - 96}" cy="{y + 150}" r="9" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(out, filter="wobble-fine") + PR.sheep(x + 4, y + 46, 0.5, -1, variant=0, pose="bleat") +
               question_markup(x + 82, y - 12, 0.55))


def glint_svg():
    x, y = DX + 180, 400
    defs = S.rad_grad("s7gl", [(0, "#ffe9a8", 0.9), (0.4, "#ffd98a", 0.45), (1, "#ffd98a", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="420" ry="260" fill="url(#s7gl)"/>'
               f'<path d="{S.rays(x, y - 40, 60, 520, 10, 6, rot=20)}" fill="#ffd98a" opacity="0.4" filter="url(#soft)"/>',
               defs)


FG = [(40, 1300, 1.2, 0), (420, 1295, 1.0, 1), (1180, 1300, 0.9, 0), (1700, 1298, 1.1, 1), (2250, 1300, 1.0, 0),
      (2700, 1296, 1.2, 1), (2960, 1300, 1.0, 0)]


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4, L5, L6 = ctx.lines[:7]
    clamp, cam_path = make_cam(SW, SH)
    BOT = SH - 4

    # ---- times
    n_in = 12
    step_in = 92.0
    t_in = 0.25
    t_arr = snap(t_in + n_in * WALK_P)
    t_wave = 1.4
    t_boom = max(t_arr + 0.25, when(ctx, "好大好大") + 0.25)
    booms = [t_boom, t_boom + 0.9, L1.start + 0.05, when(ctx, "谁敢") + 0.05]
    t_see = when(ctx, "一看见") + 0.1
    t_point = snap(t_see + 0.5)
    t_run = when(ctx, "转身就跑") - 0.1
    t_laugh = snap(t_run + 0.8)
    t_who = L3.start
    t_dare = L3.chunks[1].start
    t_god = when(ctx, "永生上帝")
    t_el = snap(L4.start + 0.1)
    t_angry = when(ctx, "很生气")
    t_e1 = snap(L5.start)
    t_e2 = snap(L5.chunks[1].start)
    t_e3 = snap(L5.chunks[2].start)
    t_d1 = snap(L6.start)
    t_d2 = snap(L6.chunks[1].start)

    # ---- camera
    C0 = cam_at(1120, 1700, BOT)
    CW = cam_at(1460, 1760, BOT)
    CG = Cam(1940, 610, 1150)
    CR = cam_at(1250, 1860, BOT)
    CD = cam_at(1525, 1620, BOT)
    CE = cam_at(1170, 1420, BOT)
    CF = cam_at(1170, 1380, BOT)
    cam = cam_path([(0, C0), (t_arr - 0.6, C0), (t_boom + 0.3, CW), (L1.start - 0.4, CW), (L1.start + 0.7, CG),
                    (L1.end + 0.1, CG), (t_see + 0.2, CR), (t_run + 1.8, CR), (t_who + 0.6, CD), (L4.start + 0.2, CD),
                    (t_angry + 0.6, CE), (L5.end, CE), (T, CF)])
    shakes = [M.shake(9, b, b + 0.5, 11, seed=i + 2) for i, b in enumerate(booms)]

    def camera(t):
        c = cam(t)
        dx = sum(s(t).dx for s in shakes)
        dy = sum(s(t).dy for s in shakes)
        return clamp(Cam(c.x + dx * c.w / 2112, c.y + dy * c.w / 2112, c.w))
    sc.camera = camera

    boom_k = lambda t: max([math.exp(-max(0.0, t - b) / 0.35) if t >= b else 0.0 for b in booms])  # noqa: E731
    shake_m = lambda amp, seed: M.combine(*[M.shake(amp, b, b + 0.6, 14, seed=seed + i)  # noqa: E731
                                            for i, b in enumerate(booms)])

    # ---- backdrop
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg(), z=0.2, wc=0.6, motion=M.drift(vx=-8))
    sc.add("far", far_svg(), z=1)
    sc.add("glint", glint_svg(), z=1.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, t_god - 0.1, t_god + 0.6, "sine") *
                               (1 - M.progress(t, L3.end + 0.3, L3.end + 1.4, "sine"))))

    # ---- Goliath far away
    gx, gy, gs = GOL
    gfr = [gol("stand"), gol("shout"), gol("mock_point"), gol("laugh"), gol("stand", "sneer")]
    gbase = [(0, 0), (snap(booms[0] - 0.12), 1), (snap(L1.end + 0.2), 4), (t_point, 2), (t_laugh, 3),
             (snap(t_laugh + 1.6), 4)]
    sc.add("goliath", gfr, z=1.2, frame_at=cuts(gbase),
           motion=M.combine(*[dip(tk, gs, (gx, gy), 14) for tk, _ in gbase[1:]],
                            M.breathe(0.012, 2.4, pivot=(gx, gy)),
                            *[hop(b, [(0, {"dy": 0}), (0.08, {"dy": -10}), (0.25, {"dy": 0})], (gx, gy))
                              for b in booms]))
    sc.add("rings", [rings_svg(k) for k in range(3)], z=1.3, wc=0, frame_at=lambda t: float(int(t * 9) % 3),
           motion=lambda t: Tf(alpha=min(1.0, 1.6 * boom_k(t)) if boom_k(t) > 0.04 else 0.0))
    sc.add("burst", [burst_svg(k) for k in range(2)], z=1.35, wc=0, frame_at=lambda t: float(int(t * 6) % 2),
           motion=M.combine(M.keys([(L1.start - 0.02, {"alpha": 0, "s": 0.5}), (L1.start + 0.15, {"alpha": 1, "s": 1.08}),
                                    (L1.start + 0.3, {"s": 1.0}), (L1.end, {"alpha": 1}), (L1.end + 0.3, {"alpha": 0})],
                                   "out", pivot=(gx - 230, gy - 260)),
                            M.pulse(0.92, 1.0, 0.5)))
    sc.add("haha", [haha_svg(k) for k in range(2)], z=1.35, wc=0, frame_at=lambda t: float(int(t * 4) % 2),
           motion=lambda t: Tf(alpha=M.progress(t, t_laugh, t_laugh + 0.2) * (1 - M.progress(t, t_laugh + 1.4,
                                                                                         t_laugh + 1.7))))

    sc.add("plateau", plateau_svg(), z=2)
    sc.add("camp_back", [camp_back_svg(w) for w in (0.0, 0.33, 0.66)], z=2.1,
           frame_at=lambda t: float(int(t * (9 if boom_k(t) > 0.2 else 3)) % 3), motion=shake_m(3, 20))
    sc.add("cart", cart_svg(), z=2.2, motion=shake_m(2, 30))
    sc.add("fire", fire_svg(), z=2.3)
    sc.add("flame", [flame_svg(k) for k in range(3)], z=2.31, wc=0.4, frame_at=lambda t: float(int(t * 7) % 3))
    sc.add("pot", [pot_svg(k) for k in range(3)], z=2.32,
           frame_at=lambda t: float(1 + int(t * 12) % 2) if boom_k(t) > 0.25 else 0.0)
    sc.add("steam", [steam_svg(k) for k in range(3)], z=2.33, wc=0, frame_at=lambda t: float(int(t * 3) % 3),
           motion=M.pulse(0.6, 1.0, 2.3))

    # ---- soldiers (camp)
    SOL = [  # x, variant, facing at start, z
        (1290, 0, -1, 3.3), (1540, 1, 1, 3.2), (1850, 2, 1, 3.25), (2240, 3, 1, 3.15)]
    run_v = 900.0
    hide_x = TENT_A[0] + 280
    for i, (x, v, f0, z) in enumerate(SOL):
        def sol(pose, facing, expr=None, shake=0.0, x=x, v=v):
            return C.ground_shadow(x, GY, SC, 120) + C.soldier(x, GY, SC, facing, side="israel", variant=v, pose=pose,
                                                              expr=expr, shake=shake)
        fr = [sol("stand", f0, "happy" if i == 0 else None), sol("point", 1, "surprised"),
              sol("stand", 1, "scared"), sol("stand", 1, "scared", 0.5), sol("run_a", -1), sol("run_b", -1),
              sol("stand", f0, blink_expr("happy" if i == 0 else "neutral"))]
        tr = t_run + 0.22 * i
        tsee = snap(t_see + 0.12 * i)
        base = [(0, 0), (snap(booms[0] + 0.15 + 0.1 * i), 1), (tsee, 2)]
        base = with_blinks(base, {0: 6}, [2.2 + 0.7 * i])
        hide = i == 2
        t_stop = tr + (x - hide_x) / run_v + 0.12 if hide else 1e9   # (+0.12: the run starts with a short ramp)

        def fa(t, base=base, tr=tr, t_stop=t_stop):
            if tr <= t < t_stop:
                return float(4 + int((t - tr) / 0.13) % 2)
            if t >= t_stop:
                return 7.0
            v_ = cuts(base)(t)
            if v_ == 2 and int(t * 8) % 2:        # trembling
                return 3.0
            return v_
        if hide:
            fr.append(sol("cower", 1, "scared", 0.0))
            fr.append(sol("cower", 1, "scared", 0.5))

            def fa(t, base=base, tr=tr, t_stop=t_stop, _f=fa):  # noqa: F811
                if t >= t_stop:
                    return 7.0 + int(t * 8) % 2
                return _f(t)

        def mv(t, x=x, tr=tr, t_stop=t_stop, hide=hide):
            if t < tr:
                return Tf()
            tt = min(t, t_stop) - tr
            d = run_v * (tt - 0.12 * (1 - math.exp(-tt / 0.12)))
            return Tf(dx=-d - (0 if not hide or t < t_stop else 0))
        bumps = [dip(snap(booms[0] + 0.15 + 0.1 * i), SC, (x, GY), 6), dip(tsee, SC, (x, GY), 6),
                 hop(tr, [(0, {"dy": 0}), (0.08, {"dy": -16}), (0.2, {"dy": 0})], (x, GY))]
        if i == 0:
            bumps.append(nod(t_wave, (x, GY), -4, 0.6))
        if hide:
            bumps.append(dip(snap(t_stop), SC, (hide_x, GY), 8))
        zz = z if not hide else 2.4        # the hider runs behind the big tent
        sc.add(f"soldier{i}", [doc(f) for f in fr], z=zz, frame_at=fa, motion=M.combine(mv, *bumps,
                                                                      M.breathe(0.01, 2.8, pivot=(x, GY), phase=i * 0.3)))
        sc.add(f"dust{i}", dust_svg(x + 40, GY + 4, seed=i), z=zz - 0.01, wc=0,
               motion=M.combine(lambda t, mv=mv: Tf(dx=mv(t).dx * 0.85),
                                M.keys([(tr, {"alpha": 0}), (tr + 0.1, {"alpha": 0.9}), (tr + 0.9, {"alpha": 0})],
                                       "sine")))
    sc.add("tent_a", [tent_a_svg(w) for w in (0.0, 0.33, 0.66)], z=2.5,
           frame_at=lambda t: float(int(t * (9 if boom_k(t) > 0.2 else 3)) % 3), motion=shake_m(3, 40))

    # ---- David
    dfr_def = [
        ("walk_a", 1, None, dict(basket=True)), ("walk_b", 1, None, dict(basket=True)),             # 0 1
        ("stand", 1, "happy", dict(basket=True)), ("stand", 1, "surprised", dict(basket=True)),     # 2 3
        ("stand", -1, "surprised", {}), ("talk", 1, "puzzled", {}), ("stand", 1, "brave", {}),     # 4 5 6
        ("point_up", 1, "brave", {}), ("stand", 1, "surprised", {}), ("stand", 1, "worried", {}),  # 7 8 9
        ("talk", 1, "puzzled", {}), ("talk", 1, "kind", {}),                                        # 10 11
        ("stand", 1, blink_expr("happy"), dict(basket=True)), ("talk", 1, blink_expr("puzzled"), {}),  # 12 13
        ("stand", 1, blink_expr("brave"), {}), ("stand", 1, blink_expr("worried"), {}),             # 14 15
        ("talk", 1, blink_expr("kind"), {})]                                                        # 16
    dfr = [C.ground_shadow(DX, GY, SC, 110) + C.david(DX, GY, SC, f, pose=p, expr=e, **kw) for p, f, e, kw in dfr_def]
    t_spin = snap(t_run + 0.45)             # the first runner whooshes past
    dbase = [(0, 2), (snap(t_boom + 0.1), 3), (t_spin, 4), (snap(t_who - 0.1), 5), (snap(t_dare + 0.05), 6),
             (snap(t_god), 7), (snap(L3.end + 0.3), 6), (snap(t_el + 0.5), 8), (snap(t_angry), 9), (t_d1, 10),
             (t_d2, 11)]
    dbase = with_blinks(dbase, {2: 12, 5: 13, 6: 14, 9: 15, 11: 16}, [16.6, 22.2, 28.6, 31.8, 37.4, T - 0.8])
    actor(sc, "david", 3.5, dfr, (DX, GY), SC, base=dbase, walks=[(t_in, n_in, step_in, 0)],
          start_off=-n_in * step_in, docf=doc,
          bumps=[dip(t_arr, SC, (DX, GY), 6), happy_hop(snap(t_wave + 0.4), SC, (DX, GY), 10),
                 hop(snap(t_boom + 0.1), [(-0.05, {"dy": 0}), (0.08, {"dy": -22}), (0.3, {"dy": 0})], (DX, GY)),
                 hop(t_spin, [(-0.08, {"rot": 0}), (0.06, {"rot": -7}), (0.25, {"rot": 4}), (0.5, {"rot": 0})],
                     (DX, GY)),
                 dip(snap(t_who - 0.1), SC, (DX, GY), 6), dip(snap(t_dare + 0.05), SC, (DX, GY), 7),
                 dip(snap(t_god), SC, (DX, GY), 8), dip(snap(L3.end + 0.3), SC, (DX, GY), 5),
                 dip(snap(t_el + 0.5), SC, (DX, GY), 5), dip(snap(t_angry), SC, (DX, GY), 5),
                 dip(t_d1, SC, (DX, GY), 7),
                 hop(t_d1 + 0.35, [(0, {"sy": 1, "dy": 0}), (0.15, {"sy": 1.035, "dy": -6}), (0.45, {"sy": 1, "dy": 0})],
                     (DX, GY)),
                 hop(t_d1 + 1.3, [(0, {"sy": 1, "dy": 0}), (0.15, {"sy": 1.03, "dy": -5}), (0.45, {"sy": 1, "dy": 0})],
                     (DX, GY)),
                 dip(t_d2, SC, (DX, GY), 5), nod(t_d2 + 0.9, (DX, GY), 3, 0.6)],
          breathe=(0.012, 2.7, 0.1))
    # whoosh lines at David as the soldiers pass
    sc.add("whoosh", [whoosh_svg(DX - 40, GY - 150, k) for k in range(2)], z=3.6, wc=0,
           frame_at=lambda t: float(int(t * 10) % 2),
           motion=lambda t: Tf(alpha=1.0 if t_spin - 0.05 <= t <= t_spin + 0.7 else 0.0, dx=-200 * max(0, t - t_spin)))
    # the basket flies out of his hand and bumps onto the ground
    bh = C.hand_positions(C.david, DX, GY, SC, 1, pose="stand", basket=True)[1]
    bx0, by0 = bh[0] + 3 * SC, bh[1] + 57 * SC
    bx1, by1 = DX + 120, GY + 22
    bk = 0.55 * SC

    def basket_m(t):
        if t < t_spin:
            return Tf(alpha=0.0)
        u = M.progress(t, t_spin, t_spin + 0.42, "linear")
        x = M.lerp(bx0, bx1, u)
        y = M.lerp(by0, by1, u) - 120 * math.sin(math.pi * u)
        if t > t_spin + 0.42:
            v = t - t_spin - 0.42
            y -= 26 * abs(math.sin(math.pi * min(v, 0.3) / 0.3)) * math.exp(-v * 3)
        rot = 200 * u if u < 1 else 360
        return Tf(dx=x - bx1, dy=y - by1, rot=rot % 360 if u < 1 else 0.0, px=bx1, py=by1 - 30 * bk)
    sc.add("basket", doc(C.ground_shadow(bx1, by1, bk, 160) + PR.bread_basket(bx1, by1, bk)), z=3.55, motion=basket_m)

    # ---- Eliab
    n_e = 10
    step_e = -90.0
    t_e_end = snap(t_el + n_e * 0.25)

    def eli(pose, expr=None):
        return C.ground_shadow(EX, GY, SC, 130) + C.eliab(EX, GY, SC, -1, pose=pose, expr=expr)
    efr = [eli("walk_a", "cross"), eli("walk_b", "cross"), eli("stand", "cross"), eli("hands_hips", "cross"),
           eli("scold", "cross"), eli("hands_hips", blink_expr("cross")), eli("talk", "cross")]
    ebase = [(0, 2), (t_e_end, 2), (snap(t_angry + 0.1), 3), (t_e1, 4), (t_e2, 3), (t_e3, 4),
             (snap(L5.end + 0.3), 3)]
    ebase = with_blinks(ebase, {3: 5}, [30.3, 35.2, 38.0, T - 0.6])
    ep = (EX, GY)
    ws = [(t_el, n_e, step_e, 0)]
    sc_e = actor(sc, "eliab", 3.7, efr, ep, SC, base=ebase, walks=ws, start_off=-n_e * step_e, period=0.25,
                 bumps=[dip(t_e_end, SC, ep, 6), dip(snap(t_angry + 0.1), SC, ep, 8), dip(t_e1, SC, ep, 7),
                        dip(t_e2, SC, ep, 6), dip(t_e3, SC, ep, 7), dip(snap(L5.end + 0.3), SC, ep, 5),
                        hop(t_e3 + 0.3, [(0, {"rot": 0}), (0.15, {"rot": -2.5}), (0.3, {"rot": 1.5}),
                                         (0.45, {"rot": -2}), (0.6, {"rot": 0})], (EX, GY)),
                        hop(t_e1 + 0.2, [(0, {"dy": 0}), (0.1, {"dy": -8}), (0.25, {"dy": 0})], ep),
                        nod(t_d2 + 1.0, ep, -3, 0.7)],
                 extra=lambda t: Tf(alpha=1.0 if t >= t_el - 0.05 else 0.0))
    del sc_e
    eh = C.body_points(C.eliab, EX, GY, SC, -1, pose="hands_hips")["head"]
    sc.add("grumble", [doc(grumble_markup(eh[0] + 10, eh[1] - 150, 0.85, seed=k)) for k in range(3)], z=3.8, wc=0,
           frame_at=lambda t: float(int(t * 6) % 3),
           motion=M.combine(M.keys([(t_angry + 0.1, {"alpha": 0, "s": 0.4}), (t_angry + 0.3, {"alpha": 1, "s": 1.05}),
                                    (t_angry + 0.45, {"s": 1.0}), (L5.start - 0.1, {"alpha": 1}),
                                    (L5.start + 0.3, {"alpha": 0})], "out", pivot=(eh[0], eh[1] - 150)),
                            M.bob(4, 0.8)))
    sc.add("sheep_bub", sheep_bubble_svg(), z=3.85, wc=0.3,
           motion=M.combine(M.keys([(t_e2 + 0.1, {"alpha": 0, "s": 0.3}), (t_e2 + 0.32, {"alpha": 1, "s": 1.06}),
                                    (t_e2 + 0.45, {"s": 1.0}), (t_e3 - 0.1, {"alpha": 1, "s": 1.0}),
                                    (t_e3 + 0.15, {"alpha": 0, "s": 0.4})], "out", pivot=(EX + 50, GY - 420)),
                            M.bob(4, 1.6)))
    # Eliab's scolding arcs
    em = C.body_points(C.eliab, EX, GY, SC, -1, pose="scold")["head"]
    sc.add("earcs", [doc(arcs_markup(em[0] - 64, em[1] + 16, -1, k, 1.3)) for k in (1, 2, 3)], z=3.9, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=lambda t: Tf(alpha=1.0 if (t_e1 + 0.1 <= t < t_e1 + 1.1 or t_e3 + 0.1 <= t < t_e3 + 1.4) else 0.0))

    # ---- foreground
    sc.add("fg", [doc(tuft_row(FG, k * 2.1)) for k in range(3)], z=6, frame_at=lambda t: float(int(t * 2.2) % 3))

    # ---- sound
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0.0, dur=T, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_in, dur=n_in * WALK_P, gain_db=-17, pan=-0.4)
    sc.sfx("thunder", booms[0] - 0.05, dur=2.2, gain_db=-15, fade_out=0.8, duck_db=-3)
    for b in booms:
        sc.sfx("thud", b, gain_db=-9, pan=0.3)
        sc.sfx("lots", b + 0.05, dur=0.8, gain_db=-17, pan=0.1)
    sc.sfx("whoosh", t_run + 0.25, gain_db=-11)
    sc.sfx("footsteps_run", t_run, dur=2.2, gain_db=-12, fade_out=0.6)
    sc.sfx("whoosh", t_spin, gain_db=-10, pan=-0.2)
    sc.sfx("thud", t_spin + 0.42, gain_db=-14, pan=0.1)
    sc.sfx("chime", t_god + 0.05, gain_db=-17)
    sc.sfx("footsteps", t_el, dur=n_e * 0.25, gain_db=-15, pan=0.3)
    sc.sfx("pop", t_angry + 0.15, gain_db=-14)
    sc.sfx("sheep", t_e2 + 0.15, gain_db=-15, pan=0.2)
    return sc
