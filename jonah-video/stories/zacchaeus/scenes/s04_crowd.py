"""Scene 4 - Luke 19:3. News spreads that Jesus is coming; Jericho lines the road; short Zacchaeus can't see past the
wall of backs.

Shots (the same tall 2112 x 1980 stage as s03_jericho; hard cuts on phrase boundaries):
  A  the street page, opening on exactly the last frame of s03 (plain 1 s cross-dissolve: the same layers, seeds,
     positions and camera; ambient motion runs on the film's global clock): Zacchaeus alone on the near verge.
  B  closer, behind the crowd: the wall of backs along the near side of the road (adults seen from behind), the far
     side's crowd looking down the road over their heads, Zacchaeus in front of the wall.
  P  his point of view: a towering wall of backs and the backs of heads.
  B  back behind the crowd for the sigh, the squeeze, the elbow and the pacing.
  Z  close on Zacchaeus in front of the wall for the closing question: his thinking face.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity film's
Tm class, chunk fallback; nothing is hard-coded to the take):
  0 .. 1.0      identical to the end of s03 (calm; palms sway, swifts glide, people breathe)
  '大家听说'     a boy comes running along the road from the left (planted run frames), stops in the middle and
                points back down the road; '耶稣' the people turn to him; '要来了' he cheers and hops
  '都跑到'       everyone hurries to the road: the people of the street dash to its edges and new groups run in from
                both sides (running feet); the far side lines up looking and pointing down the road, the near side
                turns its backs to us - the crowd lines the road (hubbub swells)
  '撒该也想看看' Zacchaeus looks up, eager (hop) and hurries up behind the crowd (planted strides)
  '撒该心想'     cut: behind the wall of backs; he puts a hand to his chin and a thought bubble opens (pop)
  '路过'         in the bubble Jesus walks along a palm-lined road, past and away out of the picture
  '看不见'       the road in the bubble is empty and a big '?' pops up; he looks worried
  '没有机会了'   determined (squash); the bubble closes
  '个子太矮了'   he looks up at the tall backs and stretches himself tall - no use - and sags
  '跳' '跳'      he jumps on each 跳 (crouch, up, land; the soles leave the ground), each time behind the backs
  '看不见'       he lands frustrated (a sweat drop)
  '踮起脚'       he goes up on tiptoe, wobbling; '还是看不见' still nothing - he comes down
  '前面的人'     cut to his low point of view: a towering wall of backs, people shuffling
  '后脑勺'       the view bobs up twice as he jumps: only the backs of heads (a straw hat, head-cloths, a veil)
  end of line   cut back: he lets out a big sigh (a little puff), shoulders dropping
  '挤进去'       he pushes in between two backs (squeeze); the two wobble
  '不让他'       the big man elbows back; Zacchaeus is knocked back (bumped, little stars, thud) and stumbles
  '团团转'       he paces to and fro in a little circle, hands behind his back
  '团团转' end  he stops and thinks (a fist on his hip, a hand at his chin)
  '小朋友'       cut close on him thinking (gentle sway, blinks); '你猜' a little thinking cloud pops up and three dots
                fill it one by one; the camera eases in; calm hold for the child to guess (page dip to s05, where the
                idea pops)
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
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import snap
from stories.zacchaeus.scenes.s03_jericho import (
    SFE, SK, SNE, SRY, STREET_FOLK, TIME, W, H, ZAC_WALK, ZY, Z_C0, Actor, add_street_set, blink,
    breathm, cam_keys, doc, f1, gate, hopm, popm, shadow, street_breath, street_cam_end, street_final,
    street_folk_markup, street_folk_order, street_z, zac_c_markup)

INK = P["ink"]

# ================================================================== SHOT A: the street (shared page from s03)
FAR_Y = SFE + 8                      # the far side's line
NEAR_F, NEAR_B = SNE + 16, SNE - 12  # the near side's two rows of backs (front, back)
ZT = (1240, 912)                     # where Zacchaeus stops behind the near crowd

# the people of the street (from s03) run to their places: name -> (target x, target y, final key)
STREET_TARGET = {
    "mum":   (1215, NEAR_F, ("crowd_back", "neutral", -1, 0.0)),
    "kid":   (1290, NEAR_F + 6, ("crowd_back", "neutral", -1, 0.3)),
    "men1":  (1600, NEAR_B, ("crowd_back", "neutral", -1, 0.5)),
    "men2":  (1700, NEAR_F, ("crowd_back", "neutral", 1, 0.2)),
    "elder": (820, NEAR_B, ("crowd_back", "neutral", -1, 0.7)),
    "w1":    (700, FAR_Y, ("look", "eager", -1)),
    "w2":    (820, FAR_Y + 2, ("point", "eager", -1)),
    "fs":    (1250, FAR_Y - 2, ("cheer", "happy", -1)),
    "m3":    (1830, FAR_Y + 4, ("wave", "happy", -1)),
}
# groups running in from off the page: (name, side (-1 = from the left), y, members [(kind, variant, x, final key)])
GROUPS = [
    ("g_farL", -1, FAR_Y, [("man", 1, 150, ("point", "eager", -1)), ("child", 2, 245, ("cheer", "eager", -1)),
                           ("woman", 4, 340, ("look", "eager", -1)), ("farmer", 0, 455, ("stand", "happy", -1))]),
    ("g_farR", 1, FAR_Y, [("woman", 2, 1460, ("look", "eager", -1)), ("man", 0, 1565, ("point", "eager", -1)),
                          ("child", 3, 1660, ("wave", "happy", -1)), ("elder", 3, 1960, ("look", "kind", -1))]),
    ("g_nearL", -1, NEAR_F, [("man", 3, 120, ("crowd_back", "neutral", -1, 0.1)), ("woman", 0, 222, ("crowd_back", "neutral", -1, 0.6)),
                             ("fruit_seller", 1, 330, ("crowd_back", "neutral", -1, 0.3)), ("man", 5, 440, ("crowd_back", "neutral", 1, 0.8)),
                             ("woman", 5, 545, ("crowd_back", "neutral", -1, 0.4))]),
    ("g_nearM", -1, NEAR_B, [("farmer", 2, 650, ("crowd_back", "neutral", -1, 0.2)), ("man", 4, 950, ("crowd_back", "neutral", -1, 0.9)),
                             ("woman", 3, 1050, ("crowd_back", "neutral", 1, 0.5)), ("man", 1, 1145, ("crowd_back", "neutral", -1, 0.3)),
                             ("fruit_seller", 2, 1340, ("crowd_back", "neutral", -1, 0.6))]),
    ("g_nearR", 1, NEAR_F, [("man", 0, 1405, ("crowd_back", "neutral", -1, 0.7)), ("woman", 1, 1505, ("crowd_back", "neutral", -1, 0.1)),
                            ("man", 2, 1830, ("crowd_back", "neutral", -1, 0.4)), ("farmer", 1, 1935, ("crowd_back", "neutral", 1, 0.6)),
                            ("elder", 2, 2040, ("crowd_back", "neutral", -1, 0.3))]),
]
BOY = (640, SRY + 8)                 # the news-bringer stops here (road centre)


def group_markup(members, y, key):
    """key ('run', k, facing) | ('final', k): every member at its final x."""
    b = ""
    for j, m in enumerate(members):
        kind, v, x, fk = m
        yy = y + (j % 2) * 4
        if key[0] == "run":
            ph = 0.0 if (key[1] + j) % 2 == 0 else 0.5
            pose = "run_to_see" if kind != "elder" else "walk"
            b += shadow(x, yy, SK, 110, 0.15) + C.jericho_folk(x, yy, SK, key[2], kind=kind, variant=v, pose=pose, phase=ph)
        else:
            pose, expr, f = fk[0], fk[1], fk[2]
            ph = (fk[3] if len(fk) > 3 else 0.0) + 0.25 * key[1]
            if pose == "wave":
                ph = 0.5 * key[1] + 0.2 * j
            b += shadow(x, yy, SK, 110, 0.15) + C.jericho_folk(x, yy, SK, f, kind=kind, variant=v, pose=pose, expr=expr,
                                                                phase=ph)
    return b


def boy_markup(key):
    pose, expr, f = key[0], key[1], key[2]
    ph = key[3] if len(key) > 3 else 0.0
    return shadow(*BOY, SK, 80, 0.16) + C.jericho_folk(*BOY, SK, f, kind="child", variant=0, pose=pose, expr=expr, phase=ph)


# ================================================================== SET D: behind the crowd (closer)
KC = 1.3
DNE = 935                            # the near side's front row of backs
DBR = DNE - 42 * KC                  # ... and the row behind it
DRY = DNE - 150 * KC                 # road centre
DFE = DRY - 150 * KC                 # far edge (the far crowd)
ZD = (1010, DNE + 55)                # Zacchaeus in front of the wall (feet clear of the subtitle box)
A_POS = (948, DNE + 2)               # the two backs he squeezes between (A left, B right - B elbows him)
B_POS = (1080, DNE - 2)
BACK_KINDS = ["man", "woman", "farmer", "man", "elder", "woman", "fruit_seller", "man", "woman", "man"]


def d_back_svg():
    b = PR.jericho_sky(-10, -10, W + 10, 400, time=TIME, sun=None, clouds=0.8, birds=0, seed=23, scale=1.0)
    b += PR.jericho_street(-240, W + 240, DRY, KC, part="back", time=TIME, seed=13)
    b += PR.jericho_street(-240, W + 240, DRY, KC, part="road", time=TIME, seed=13, bottom=1300)
    return doc(b)


def d_far_crowd_svg(k):
    return doc(C.jericho_crowd(1056, DFE + 6, KC * 0.94, -1, n=16, pose="line", width=1750, rows=2, seed=5, phase=k / 3))


def back_row_members(row):
    """[(x, kind, variant, facing, phase0)] for the wall of backs (row 0 front, 1 behind), without A and B."""
    rng = random.Random(40 + row)
    out = []
    step = 97 * KC * (1 - 0.05 * row)
    if row == 0:
        xs = [A_POS[0] - step * k for k in range(1, 12)] + [B_POS[0] + step * k for k in range(1, 12)]
    else:
        xs = [A_POS[0] + 66 - step * k for k in range(0, 12)] + [A_POS[0] + 66 + step * k for k in range(1, 12)]
    for i, x in enumerate(sorted(xs)):
        if x < -90 or x > W + 90:
            continue
        kind = BACK_KINDS[(i * 3 + row * 5) % len(BACK_KINDS)]
        out.append((x + rng.uniform(-8, 8), kind, (i * 5 + row * 2) % 6 + 3 * (i % 2), -1 if (i + row) % 4 else 1,
                    rng.uniform(0, 1)))
    return out


def back_row_svg(row, k):
    y = DNE if row == 0 else DBR
    s = KC * (1 - 0.05 * row)
    b = ""
    for (x, kind, v, f, ph) in back_row_members(row):
        b += C.jericho_folk(x, y + (4 if int(x) % 2 else 0), s, f, kind=kind, variant=v, pose="crowd_back", phase=ph + k / 3)
    return doc(b)


def zac_d_markup(key):
    """key (pose, expr[, phase[, facing]]) at ZD; the shadow shrinks while he is in the air."""
    pose, expr = key[0], key[1]
    ph = key[2] if len(key) > 2 else 0.0
    f = key[3] if len(key) > 3 else 1
    lift = 0.0
    if pose == "jump":
        lift = C._jump_lift(ph) * KC
    elif pose == "jump_air":
        lift = C.ZAC_JUMP * KC
    sh = shadow(*ZD, KC, 110 * (1 - 0.45 * lift / (C.ZAC_JUMP * KC)), 0.18 * (1 - 0.4 * lift / (C.ZAC_JUMP * KC)))
    return sh + C.zacchaeus(*ZD, KC, f, pose=pose, expr=expr, phase=ph)


def ab_markup(who, key):
    x, y = A_POS if who == "A" else B_POS
    kind, v = ("woman", 4) if who == "A" else ("man", 5)
    pose, expr, f = key[0], key[1], key[2]
    ph = key[3] if len(key) > 3 else 0.0
    return C.jericho_folk(x, y, KC, f, kind=kind, variant=v, pose=pose, expr=expr, phase=ph)


# ---- the thought bubble
BUB = (560, 300)                     # centre of the thought bubble's picture
BUB_RX, BUB_RY = 250, 140            # the picture (an ellipse)
BUB_W = 2 * BUB_RX
BUB_CLIP = "zq4bubclip"


def scallop_cloud(cx, cy, rx, ry, n=16, r=46, seed=3, fill="#fffaf0", sw=4.0):
    """A classic thought cloud: puffs round an ellipse, one outer ink outline."""
    rng = random.Random(seed)
    puffs = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * rng.uniform(0.85, 1.15)
        puffs.append((cx + (rx + rr * 0.35) * math.cos(a), cy + (ry + rr * 0.35) * math.sin(a), rr))
    out = ""
    for x, y, rr in puffs:
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr)}" fill="{fill}" stroke="{INK}" stroke-width="{f1(2 * sw)}"/>'
    out += f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx + 10)}" ry="{f1(ry + 10)}" fill="{fill}" stroke="{INK}" stroke-width="{f1(2 * sw)}"/>'
    for x, y, rr in puffs:
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr)}" fill="{fill}"/>'
    out += f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx + 10)}" ry="{f1(ry + 10)}" fill="{fill}"/>'
    return out


def bubble_frame_svg():
    cx, cy = BUB
    b = ""
    # trail of little bubbles down to his head
    hx, hy = ZD[0] - 30, ZD[1] - 300 * KC
    tx, ty = cx + BUB_RX * 0.55, cy + BUB_RY + 40
    for k, r in enumerate((14, 22, 32)):
        u = 0.16 + 0.27 * k
        b += PR._circ(hx + (tx - hx) * u, hy + (ty - hy) * u, r, "#fffaf0", 3.4)
    b += scallop_cloud(cx, cy, BUB_RX, BUB_RY)
    # the little picture inside: a palm-lined road under a turquoise sky
    clip = f'<clipPath id="{BUB_CLIP}"><ellipse cx="{cx}" cy="{cy}" rx="{BUB_RX}" ry="{BUB_RY}"/></clipPath>'
    inner = (f'<rect x="{cx - 400}" y="{cy - 300}" width="800" height="600" fill="{S.mix("#acd9d0", "#fffaf0", 0.15)}"/>'
             f'<rect x="{cx - 400}" y="{cy + 26}" width="800" height="300" fill="{S.mix("#e8cc94", "#fffaf0", 0.1)}"/>')
    inner += PR._p(f"M{cx - 400},{cy + 62} L{cx + 400},{cy + 56} L{cx + 400},{cy + 112} L{cx - 400},{cy + 118} Z",
                   S.mix("#f4e2b6", "#fffaf0", 0.15), 2.4)
    for px, s_, sd in ((cx - 200, 0.27, 3), (cx + 20, 0.23, 5), (cx + 210, 0.28, 7)):
        inner += PR.date_palm(px, cy + 42, s_, 1, height=1.0, time=TIME, seed=sd)
    for px in (cx - 120, cx + 120):
        inner += PR.jericho_house(px, cy + 40, 0.3, 1, variant=int(px) % 4, time=TIME, seed=2)
    b += clip + f'<g clip-path="url(#{BUB_CLIP})">{inner}</g>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{BUB_RX}" ry="{BUB_RY}" fill="none" stroke="#d9c095" stroke-width="3.5"/>'
    return doc(S.g(b, filter="wobble-fine"))


BUB_JS = 0.40                        # Jesus inside the bubble


def bubble_jesus_svg(x, pose):
    cx, cy = BUB
    y = cy + 92
    j = C.ground_shadow(x, y, BUB_JS, 90, 0.14) + C.jesus(x, y, BUB_JS, 1, pose=pose, expr="kind")
    clip = (f'<clipPath id="{BUB_CLIP}j"><ellipse cx="{cx}" cy="{cy}" rx="{BUB_RX - 3}" '
            f'ry="{BUB_RY - 3}"/></clipPath>')
    return doc(clip + f'<g clip-path="url(#{BUB_CLIP}j)">{j}</g>')


def question_svg(x, y, size=150, col="#c8643c"):
    return doc(f'<text x="{x}" y="{y}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" fill="{col}" '
               f'stroke="{INK}" stroke-width="5" paint-order="stroke" text-anchor="middle">?</text>')


def puff_svg(x, y, r):
    """A little sigh puff (three soft circles)."""
    b = ""
    for dx, dy, rr in ((0, 0, 1.0), (r * 0.9, -r * 0.5, 0.75), (r * 1.6, -r * 1.2, 0.5)):
        b += PR._circ(x + dx, y + dy, r * rr, "#fffaf0", 3, extra='opacity="0.95"')
    return doc(S.g(b, filter="wobble-fine"))


def think_cloud_svg(x, y, k=1.0):
    """A little cream thinking cloud (the dots pop in on top of it)."""
    b = scallop_cloud(x, y, 62 * k, 30 * k, n=9, r=22 * k, seed=5, sw=3.0 * min(1.3, k))
    return doc(S.g(b, filter="wobble-fine"))


def dot_svg(x, y, r=9):
    return doc(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="#6a4a36"/>')


# ================================================================== SET Z: close on his thinking face (the closing question)
ZK = 2.0                             # Zacchaeus close
ZZ = (930, 1100)                     # his feet (below the subtitle line; his face is in the middle of the page)
ZB0, ZB1 = (1.95, 1040), (1.82, 972)     # the backs behind him: (scale, feet y) front row, row behind
ZRY = 520 + 150 * 1.45               # the street behind (far edge at 520)


def z_back_svg():
    b = PR.jericho_sky(-10, -10, W + 10, 300, time=TIME, sun=None, clouds=0.6, birds=0, seed=33, scale=1.4)
    b += PR.jericho_street(-300, W + 300, ZRY, 1.45, part="back", time=TIME, seed=19)
    b += PR.jericho_street(-300, W + 300, ZRY, 1.45, part="road", time=TIME, seed=19, bottom=1300)
    return doc(b)


def z_far_svg(k):
    return doc(C.jericho_crowd(1000, 526, 1.3, -1, n=12, pose="line", width=1500, rows=2, seed=9, phase=k / 3))


def z_backs_svg(row, k):
    s_, y = ZB0 if row == 0 else ZB1
    rng = random.Random(90 + row)
    kinds = ["man", "woman", "farmer", "man", "woman", "elder", "fruit_seller", "man"]
    step = 92 * s_ * 1.0
    x = -120 + (0 if row == 0 else step / 2)
    i = 0
    b = ""
    while x < W + 200:
        b += C.jericho_folk(x + rng.uniform(-10, 10), y + rng.uniform(-6, 6), s_, -1 if (i + row) % 3 else 1,
                            kind=kinds[(i + 3 * row) % len(kinds)], variant=(i * 5 + row) % 6 + 3 * (i % 2),
                            pose="crowd_back", phase=rng.uniform(0, 1) + k / 3)
        x += step
        i += 1
    return doc(b)


def zac_z_markup(key):
    pose, expr = key[0], key[1]
    return shadow(*ZZ, ZK, 110, 0.18) + C.zacchaeus(*ZZ, ZK, 1, pose=pose, expr=expr)


# ================================================================== SET P: his point of view (the wall of backs)
PV_FRONT = (3.0, 2150)               # scale, feet y (below the page)
PV_BACK = (2.7, 2075)


def pov_back_svg():
    b = PR.jericho_sky(-10, 480, W + 10, 1990, time=TIME, sun=None, clouds=1.0, birds=0, seed=29, scale=1.4)
    for i, (x, s_, sd) in enumerate(((180, 1.05, 3), (720, 0.95, 5), (1300, 1.1, 7), (1900, 1.0, 9))):
        b += PR.date_palm(x, 1720, s_, 1 if i % 2 else -1, height=1.0, lean=(-0.1, 0.12, -0.05, 0.15)[i], time=TIME, seed=sd)
    for i, (x, v) in enumerate(((420, 1), (1030, 2), (1640, 0))):
        b += PR.jericho_house(x, 1820, 1.4, 1 if i % 2 else -1, variant=v, time=TIME, seed=i)
    return doc(b)


def pov_row_svg(row, k):
    s, y = PV_FRONT if row == 0 else PV_BACK
    rng = random.Random(70 + row)
    kinds = (["man", "farmer", "woman", "man", "fruit_seller", "woman", "man", "elder", "woman"] if row == 0 else
             ["woman", "man", "elder", "man", "woman", "farmer", "man", "woman", "man", "woman"])
    step = 92 * s * 1.02
    x0 = -60 if row == 0 else -60 + step / 2
    b = ""
    i = 0
    x = x0
    while x < W + 260:
        kind = kinds[i % len(kinds)]
        v = (i * 5 + row * 3) % 6
        f = -1 if (i + row) % 3 else 1
        ph = rng.uniform(0, 1) + k / 3
        b += C.jericho_folk(x + rng.uniform(-14, 14), y + rng.uniform(-10, 10), s, f, kind=kind, variant=v, pose="crowd_back",
                            phase=ph)
        x += step
        i += 1
    return doc(b)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    L = ctx.lines
    fin = street_final()

    t_cutB = snap(L[2].start - 0.3)
    t_cutP = snap(L[4].start - 0.25)
    t_cutB2 = snap(tm.end(4, "撒该只看见别人的后脑勺") - 0.05)
    t_cutZ = snap(L[6].start - 0.12)
    gA, gB, gP, gZ = gate(-1, t_cutB), gate(t_cutB, 1e9), gate(t_cutP, t_cutB2), gate(t_cutZ, 1e9)
    gD = lambda t: Tf(alpha=1.0 if (t_cutB <= t < t_cutP or t_cutB2 <= t < t_cutZ) else 0.0)   # noqa: E731

    # ------------------------------------------------------------ SHOT A: the street
    add_street_set(sc, gA, g0, z=50.0)
    t_tingshuo = tm.at(0, "大家听说耶稣要来了", 0)
    t_yesu = tm.at(0, "大家听说耶稣要来了", 4)
    t_lai = tm.at(0, "大家听说耶稣要来了", 7)
    t_pao = tm.at(0, "都跑到街上去看", 1)
    t_kan = tm.at(0, "都跑到街上去看", 6)
    t_zac = tm.at(1, "撒该也想看看", 0)
    t_xiang = tm.at(1, "撒该也想看看", 3)
    t_yesu2 = tm.at(1, "耶稣是什么样的人", 0)

    # the boy with the news: runs in along the road, points back down it, cheers
    boy = Actor("a_boy", BOY, SK, boy_markup, 51.06, 501, g0, gA)
    n_run = 10
    run_per = 0.13
    t_b0 = snap(max(1.02, t_tingshuo - n_run * run_per + 0.25))     # he enters the page after the dissolve
    boy.cut(0, ("run_a", "eager", 1))
    dist = BOY[0] + 60.0
    boy.shift(-dist)
    for i in range(n_run):
        boy.cut(t_b0 + i * run_per, ("run_a" if i % 2 == 0 else "run_b", "eager", 1))
    boy.moves.append(lambda t, d=dist, t0=t_b0, t1=t_b0 + n_run * run_per: (d * M.progress(t, t0, t1, lambda u: u * (2 - u) * 0.6 + 0.4 * u), 0.0))
    t_bstop = snap(t_b0 + n_run * run_per)
    boy.cut(t_bstop, ("point", "shout", -1), dip=6)
    t_bcheer = snap(t_lai - 0.05)
    boy.cut(t_bcheer, ("cheer", "shout", 1), dip=5)
    boy.extra += [hopm(t_bcheer + 0.1, SK, 30, 0.3), hopm(t_bcheer + 0.55, SK, 26, 0.3)]
    t_brun = snap(max(t_pao + 0.4, t_bcheer + 1.0))
    boy.cut(t_brun, ("run_a", "eager", -1), dip=5)
    for i in range(1, 12):
        boy.cut(t_brun + i * run_per, ("run_a" if i % 2 == 0 else "run_b", "eager", -1))
    boy.moves.append(lambda t, t0=t_brun: (-900 * SK * max(0.0, t - t0) / (12 * run_per) * min(1.0, max(0.0, t - t0) / 0.3), 0.0))
    boy.extra.append(breathm(g0, 2.6, 0.01))
    boy.build(sc)
    sc.sfx("footsteps_run", t_b0, dur=n_run * run_per + 0.1, gain_db=-17, pan=-0.4)

    # the people of the street: turn to the boy, then dash to the road's edges
    order = street_folk_order()
    for i, name in enumerate(order):
        d = STREET_FOLK[name]
        key0, (ox, oy) = fin[name]
        hx, hy = d["home"]
        tx, ty, fkey = STREET_TARGET[name]
        t_turn = snap(t_yesu + 0.08 * i)
        t_go = snap(t_pao - 0.1 + 0.07 * i)
        x_now = hx + ox
        f_boy = -1 if x_now > BOY[0] else 1
        turn_key = {"kid": ("point", "eager", f_boy), "w2": ("point", "eager", f_boy), "fs": ("smile", "surprised", f_boy)}.get(
            name, ("stand", "surprised", f_boy))
        draw = (lambda k, name=name: street_folk_markup(name, k))
        # 1) exactly as at the end of s03, then turning to the boy
        a1 = Actor(f"c_{name}", (hx, hy), SK, draw, street_z(name), 410 + i, g0,
                   lambda t, t_go=t_go: Tf(alpha=gA(t).alpha * (1.0 if t < t_go else 0.0)))
        a1.shift(ox, oy)
        a1.cut(0, key0)
        a1.cut(t_turn, turn_key, dip=5)
        a1.extra.append(street_breath(g0, i))
        a1.build(sc)
        # 2) the dash to the road's edge and the place in the line (layered by the new row; same seed and drawings)
        z2 = (51.0 if ty < SRY else 51.08) + ty / 100000.0
        a = Actor(f"c2_{name}", (hx, hy), SK, draw, z2, 410 + i, g0,
                  lambda t, t_go=t_go: Tf(alpha=gA(t).alpha * (1.0 if t >= t_go else 0.0)))
        a.shift(ox, oy)
        a.cut(0, turn_key)
        dx, dy = tx - (hx + ox), ty - (hy + oy)
        f_run = 1 if dx > 0 else -1
        kind = d["kind"]
        if abs(dx) < 45 and abs(dy) < 25:
            t_arr = t_go
            a.moves.append(lambda t, dx=dx, dy=dy, t0=t_go: (dx * M.progress(t, t0 - 0.1, t0 + 0.15, "sine"),
                                                            dy * M.progress(t, t0 - 0.1, t0 + 0.15, "sine")))
        else:
            steps = max(2, int(abs(dx) / 70) + 1)
            per = 0.13 if kind != "elder" else 0.24
            for k in range(steps):
                pose = ("run_a" if k % 2 == 0 else "run_b") if kind != "elder" else ("walk_a" if k % 2 == 0 else "walk_b")
                a.cut(t_go + k * per, (pose, "eager", f_run))
            t_arr = snap(t_go + steps * per)
            a.moves.append(lambda t, dx=dx, dy=dy, t0=t_go, t1=t_arr: (dx * M.progress(t, t0, t1, "sine"),
                                                                      dy * M.progress(t, t0, t1, "sine")))
        if fkey[0] == "crowd_back":
            a.loop(t_arr, [(fkey[0], fkey[1], fkey[2], (fkey[3] + q / 3) % 1.0) for q in range(3)], 0.45, phase=0.3 * i)
        elif fkey[0] == "wave":
            a.loop(t_arr, [(fkey[0], fkey[1], fkey[2], q / 4) for q in range(4)], 0.12)
        else:
            a.cut(t_arr, fkey)
        a.dips.append((snap(t_arr), 5))
        a.extra.append(street_breath(g0, i))
        a.build(sc)

    # groups running in from both sides
    for gi, (gname, side, gy, members) in enumerate(GROUPS):
        far = gy < SRY
        z = (51.0 if far else 51.08) + gy / 100000.0 + gi * 0.000001
        travel = (max(m[2] for m in members) + 160) if side < 0 else (W - min(m[2] for m in members) + 160)
        g = Actor(gname, (members[0][2], gy), SK, lambda k, members=members, gy=gy: group_markup(members, gy, k), z, 520 + gi,
                  g0, gA)
        t_g0 = snap(t_pao - 0.25 + 0.18 * gi)
        dur = 0.7 + travel / 1100
        t_g1 = snap(t_g0 + dur)
        g.cut(0, ("run", 0, -side))
        k = 0
        while t_g0 + k * 0.13 < t_g1:
            g.cut(t_g0 + k * 0.13, ("run", k % 2, -side))
            k += 1
        g.moves.append(lambda t, tr=travel * side, t0=t_g0, t1=t_g1: (tr * (1 - M.progress(t, t0, t1, "out")), 0.0))
        g.loop(t_g1, [("final", q % 3) for q in range(3)], 0.45, phase=0.37 * gi)
        g.dips.append((t_g1, 5))
        g.build(sc)
        sc.sfx("footsteps_run", t_g0, dur=dur, gain_db=-19, pan=0.6 * side)

    # Zacchaeus: lonely -> looks up, eager -> hurries up behind the crowd
    zkey0, (zox, zoy) = fin["zac"]
    za = Actor("c_zac", (Z_C0, ZY), SK, zac_c_markup, 52.0, 401, g0, gA)
    za.shift(zox, zoy)
    za.cut(0, zkey0)
    t_zup = snap(t_zac + 0.15)
    za.cut(t_zup, ("stand", "eager"))
    za.extra.append(hopm(t_zup, SK, 22, 0.3))
    t_zw = snap(t_xiang)
    x_now = Z_C0 + zox
    nz = 7
    first = (ZT[0] - x_now) / SK - sum(ZAC_WALK[i % 4][1] for i in range(1, nz))
    za.walk(t_zw, [((k, "eager"), a_) for k, a_ in ZAC_WALK], nz, 0.2, 1, first_adv=first,
            slope=(ZT[1] - ZY) / (ZT[0] - x_now))
    t_zstop = snap(t_zw + nz * 0.2)
    za.cut(t_zstop, ("tiptoe", "eager"), dip=4)
    za.cut(snap(t_zstop + 0.9), ("stand", "eager"), dip=4)
    za.extra.append(breathm(g0, 3.0, 0.010))
    za.build(sc)
    sc.sfx("footsteps", t_zw, dur=nz * 0.2 + 0.1, gain_db=-20)

    camA = cam_keys([(0, street_cam_end()), (1.0, street_cam_end()), (t_tingshuo + 0.2, Cam(980, 630, 1880)),
                     (t_pao - 0.3, Cam(1000, 625, 1900)), (t_pao + 1.6, Cam(1080, 610, 1960)),
                     (t_zw - 0.2, Cam(1100, 630, 1900)), (t_cutB, Cam(1180, 690, 1560))],
                    ["linear", "sine", "linear", "sine", "sine", "sine"])

    # ------------------------------------------------------------ SET D: behind the crowd
    sc.add("d_back", d_back_svg(), z=10.0, seed=601, motion=gD)
    sc.add("d_far", [d_far_crowd_svg(k) for k in range(3)], z=10.1, seed=603, motion=gD,
           frame_at=lambda t: float(int((t + g0) / 0.5) % 3))
    sc.add("d_row1", [back_row_svg(1, k) for k in range(3)], z=10.2, seed=605, motion=gD,
           frame_at=lambda t: float(int((t + g0) / 0.47 + 1) % 3))
    sc.add("d_row0", [back_row_svg(0, k) for k in range(3)], z=10.4, seed=607, motion=gD,
           frame_at=lambda t: float(int((t + g0) / 0.43 + 2) % 3))

    # beats (lines 2-6)
    t_xinxiang = tm.at(2, "撒该心想", 0)
    t_luguo = tm.at(2, "耶稣只是路过这里", 0)
    t_kbj = tm.at(2, "今天要是看不见", 4)
    t_jiu = tm.at(2, "就没有机会了", 0)
    t_jh = tm.at(2, "就没有机会了", 3)
    t_ai = tm.at(3, "撒该的个子太矮了", 6)
    t_tiao1 = tm.at(3, "他跳呀跳", 1)
    t_tiao2 = tm.at(3, "他跳呀跳", 3)
    t_kbj2 = tm.at(3, "看不见", 0)
    t_dian = tm.at(3, "他踮起脚", 1)
    t_hai = tm.at(3, "还是看不见", 0)
    t_hnao = tm.at(4, "撒该只看见别人的后脑勺", 8)
    t_ji = tm.at(5, "他想挤进去", 2)
    t_burang = tm.at(5, "大家都不让他", 3)
    t_tuan = tm.at(5, "撒该急得团团转", 4)
    t_xpy = tm.at(6, "小朋友", 0)
    t_cai = tm.at(6, "你猜撒该想到了什么好办法", 1)
    t_fa = tm.at(6, "你猜撒该想到了什么好办法", 10)

    # the two backs A (left) and B (right, the elbow)
    aa = Actor("d_A", A_POS, KC, lambda k: ab_markup("A", k), 10.41, 611, g0, gD)
    aa.loop(0, [("crowd_back", "neutral", -1, q / 3) for q in range(3)], 0.5, phase=0.2)
    bb = Actor("d_B", B_POS, KC, lambda k: ab_markup("B", k), 10.42, 612, g0, gD)
    bb.loop(0, [("crowd_back", "neutral", 1, q / 3 + 0.1) for q in range(3)], 0.46, phase=0.6)

    # Zacchaeus behind the wall
    zd = Actor("d_zac", ZD, KC, zac_d_markup, 10.6, 621, g0, gD)
    zd.cut(0, ("stand", "eager"))
    t_think = snap(t_xinxiang + 0.1)
    zd.cut(t_think, ("think", "ponder"), dip=5)
    t_worry = snap(t_kbj + 0.1)
    zd.cut(t_worry, ("stand", "worried"), dip=5)
    t_det = snap(t_jh - 0.1)
    zd.cut(t_det, ("stand", "determined"), dip=7)
    t_look = snap(L[3].start + 0.2)
    zd.cut(t_look, ("tiptoe", "worried"), dip=4)
    t_stretch = snap(t_ai - 0.15)
    zd.extra.append(lambda t, t0=t_stretch: Tf(sy=1 + 0.06 * math.sin(math.pi * min(1.0, max(0.0, (t - t0) / 0.7)))
                                               * (1.0 if t < t0 + 0.7 else 0.0)))
    zd.cut(snap(t_stretch + 0.75), ("stand", "frustrated"), dip=6)
    # the two jumps: take-off on each 跳
    jump_keys = []
    phs = (0.1, 0.25, 0.38, 0.5, 0.62, 0.75, 0.88)
    jstep = 0.06
    t_prev = -10.0
    for jt, t_j in enumerate((t_tiao1, t_tiao2)):
        t_s = snap(max(t_j - 0.1, t_prev + len(phs) * jstep))
        for q, ph in enumerate(phs):
            zd.cut(t_s + q * jstep, ("jump", "eager" if ph < 0.78 else "frustrated", ph))
        jump_keys.append(t_s)
        t_prev = t_s
    t_land = snap(jump_keys[-1] + len(phs) * jstep)
    zd.cut(t_land, ("jump_land", "frustrated"))
    zd.cut(snap(max(t_land + 0.55, t_kbj2 + 0.3)), ("stand", "frustrated"), dip=4)
    t_tip = snap(t_dian - 0.05)
    zd.cut(t_tip, ("tiptoe", "eager"), dip=4)
    zd.extra.append(lambda t, t0=t_tip, t1=t_cutP: Tf(rot=2.2 * math.sin(2 * math.pi * (t - t0) / 0.7) if t0 + 0.2 < t < t1 else 0.0))
    t_still = snap(t_hai + 0.05)
    zd.cut(t_still, ("tiptoe", "frustrated"))
    # after the point of view: the sigh, the squeeze, the elbow, the pacing, the thinking face
    t_sigh = snap(t_cutB2 + 0.12)
    zd.cut(t_cutB2, ("stand", "frustrated"))
    zd.cut(t_sigh, ("lonely", "sad"), dip=8)
    t_sq = snap(t_ji - 0.15)
    sq_hand = sum(h[0] for h in C.body_points(C.zacchaeus, 0, 0, KC, 1, pose="squeeze")["hands"]) / 2
    sq_dx, sq_dy = (A_POS[0] + B_POS[0]) / 2 - sq_hand - ZD[0], DNE + 12 - ZD[1]
    zd.cut(t_sq, ("squeeze", "determined"), dip=4)
    t_bump = snap(t_burang + 0.06)
    zd.moves.append(lambda t, t0=t_sq: (sq_dx * M.progress(t, t0 - 0.15, t0 + 0.2, "sine") *
                                        (1 - M.progress(t, t_bump, t_bump + 0.35, "out")),
                                        sq_dy * M.progress(t, t0 - 0.15, t0 + 0.2, "sine") *
                                        (1 - M.progress(t, t_bump, t_bump + 0.35, "out"))))
    zd.extra.append(lambda t, t0=t_sq, t1=t_bump: Tf(dx=3 * math.sin(2 * math.pi * (t - t0) / 0.18) if t0 + 0.25 < t < t1 else 0.0))
    zd.cut(t_bump, ("bumped", "surprised", 0.0, 1))
    zd.moves.append(lambda t, t0=t_bump: (-55 * KC * M.progress(t, t0, t0 + 0.45, "out"), 12 * KC * M.progress(t, t0, t0 + 0.45, "out")))
    zd.extra.append(hopm(t_bump + 0.02, KC, 20, 0.3))
    t_stand2 = snap(t_bump + 0.75)
    zd.cut(t_stand2, ("stand", "frustrated"), dip=6)
    # pacing: three steps left, turn, three steps right, turn (a little circle)
    t_p0 = snap(min(t_tuan - 0.75, t_stand2 + 0.55))
    pace = (("pace_a", 68), ("pace_b", 68))
    t_p1 = zd.walk(t_p0, [((k, "frustrated", 0.0, -1), a_) for k, a_ in pace], 2, 0.24, -1, first_adv=30, slope=-0.12)
    t_p2 = zd.walk(snap(t_p1), [((k, "frustrated", 0.0, 1), a_) for k, a_ in pace], 4, 0.24, 1, first_adv=40, slope=-0.08)
    t_p3 = zd.walk(snap(t_p2), [((k, "frustrated", 0.0, -1), a_) for k, a_ in pace], 2, 0.24, -1, first_adv=40, slope=0.0)
    t_th = snap(max(t_p3, t_xpy - 0.75))
    zd.cut(t_th, ("think", "ponder"), dip=6)
    zd.extra.append(breathm(g0, 3.0, 0.011))
    zd.blinks([t_cutB + 0.6, t_think + 1.2],
              {("think", "ponder"): ("think", blink("ponder")), ("stand", "eager"): ("stand", blink("eager"))})
    zd.build(sc)
    sc.sfx("whoosh", jump_keys[0] + 0.1, gain_db=-20)
    sc.sfx("whoosh", jump_keys[1] + 0.1, gain_db=-20)
    sc.sfx("thud", jump_keys[0] + 0.40, gain_db=-20)
    sc.sfx("thud", t_land + 0.02, gain_db=-18)
    sc.sfx("cloth", t_sq, gain_db=-16)
    sc.sfx("thud", t_bump, gain_db=-11)
    sc.sfx("pop", t_bump + 0.05, gain_db=-18)
    sc.sfx("footsteps", t_p0, dur=t_p3 - t_p0, gain_db=-19)

    # A and B react: wobble when he pushes, A closes in, B elbows back
    aa.extra.append(lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * (t - t_sq) / 0.3) if t_sq + 0.15 < t < t_bump else 0.0))
    bb.extra.append(lambda t: Tf(rot=-1.5 * math.sin(2 * math.pi * (t - t_sq) / 0.32) if t_sq + 0.15 < t < t_bump - 0.3 else 0.0))
    t_el = snap(t_bump - 0.1)
    bb.cut(t_el, ("elbow", "cross", 1), dip=4)
    bb.loop(snap(t_el + 1.0), [("crowd_back", "neutral", 1, q / 3 + 0.1) for q in range(3)], 0.46, phase=0.6, dip=4)
    aa.cut(snap(t_bump - 0.25), ("crowd_back", "neutral", -1, 0.0), dip=3)
    aa.moves.append(lambda t: (14 * M.progress(t, t_bump - 0.25, t_bump + 0.1, "sine"), 0.0))
    aa.loop(snap(t_bump + 0.5), [("crowd_back", "neutral", -1, q / 3) for q in range(3)], 0.5, phase=0.2)
    aa.build(sc)
    bb.build(sc)

    # the thought bubble: Jesus walks past and away, the empty road, a '?'
    t_bub = snap(t_xinxiang + 0.45)
    t_bub_out = snap(t_jh + 0.55)
    bub_piv = (BUB[0], BUB[1] + 60)
    sc.add("d_bubble", bubble_frame_svg(), z=10.8, wc=0.5, seed=631,
           motion=M.combine(popm(t_bub, bub_piv, 0.4, t_out=t_bub_out, out_dur=0.3, wob=False), gD))
    sc.sfx("pop", t_bub, gain_db=-10)
    n_js = 15
    x_js0 = BUB[0] - BUB_RX + 50
    step_js = JESUS_STEP = 87 * BUB_JS
    t_q = snap(t_kbj)
    t_js0 = snap(t_bub + 0.3)
    js_per = min(0.27, (t_q - 0.12 - t_js0) / n_js)
    jfr = []
    for i in range(n_js + 1):
        jfr.append(bubble_jesus_svg(x_js0 + i * JESUS_STEP, "walk_a" if i % 2 == 0 else "walk_b"))
    del step_js
    sc.add("d_bub_jesus", jfr, z=10.81, wc=0.4, seed=633,
           frame_at=lambda t: float(min(n_js, max(0, int((t - t_js0) / js_per) + 1))) if t >= t_js0 else 0.0,
           motion=M.combine(popm(t_bub, bub_piv, 0.4, t_out=t_bub_out, out_dur=0.3, wob=False),
                            lambda t: Tf(alpha=1.0 if t < t_js0 + (n_js + 0.5) * js_per else 0.0), gD))
    sc.add("d_bub_q", question_svg(BUB[0] + 10, BUB[1] + 62), z=10.82, wc=0, seed=635,
           motion=M.combine(popm(t_q, (BUB[0] + 10, BUB[1] + 10), 0.35, t_out=t_bub_out, out_dur=0.25), gD))
    sc.sfx("pop", t_q, gain_db=-12)

    # the sigh puff and the thinking dots
    head = C.body_points(C.zacchaeus, *ZD, KC, 1, pose="lonely")["head"]
    t_puff = snap(t_sigh + 0.15)
    sc.add("d_puff", puff_svg(head[0] + 60, head[1] + 10, 16), z=10.85, wc=0.3, seed=641,
           motion=M.combine(lambda t: (Tf(alpha=0.0) if t < t_puff or t > t_puff + 1.1 else
                                       Tf(dx=50 * (t - t_puff), dy=-40 * (t - t_puff), sx=0.6 + 0.6 * (t - t_puff),
                                          sy=0.6 + 0.6 * (t - t_puff), alpha=min(1.0, (t - t_puff) / 0.15) *
                                          (1 - M.progress(t, t_puff + 0.6, t_puff + 1.1, "sine")),
                                          px=head[0] + 60, py=head[1] + 10)), gD))
    th_off = zd.off(T)

    # ------------------------------------------------------------ SET Z: close on his thinking face
    sc.add("z_back", z_back_svg(), z=30.0, seed=801, motion=gZ)
    sc.add("z_far", [z_far_svg(k) for k in range(3)], z=30.1, seed=803, motion=gZ,
           frame_at=lambda t: float(int((t + g0) / 0.5) % 3))
    sc.add("z_row1", [z_backs_svg(1, k) for k in range(3)], z=30.2, seed=805, motion=gZ,
           frame_at=lambda t: float(int((t + g0) / 0.47 + 1) % 3))
    sc.add("z_row0", [z_backs_svg(0, k) for k in range(3)], z=30.3, seed=807, motion=gZ,
           frame_at=lambda t: float(int((t + g0) / 0.43 + 2) % 3))
    zz = Actor("z_zac", ZZ, ZK, zac_z_markup, 30.5, 811, g0, gZ)
    zz.cut(0, ("think", "ponder"))
    t_thoughtful = snap(t_cai + 0.1)
    zz.cut(t_thoughtful, ("think", "thoughtful"), dip=3)
    zz.extra.append(breathm(g0, 3.2, 0.010))
    zz.extra.append(lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * (t - t_cutZ) / 3.6) * min(1.0, max(0.0, t - t_cutZ) / 1.0),
                                 px=ZZ[0], py=ZZ[1]))
    zz.blinks([t_cutZ + 0.9, t_thoughtful + 1.4, t_fa + 0.5],
              {("think", "ponder"): ("think", blink("ponder")), ("think", "thoughtful"): ("think", blink("thoughtful"))})
    zz.build(sc)
    zth = C.body_points(C.zacchaeus, *ZZ, ZK, 1, pose="think")["head"]
    tcx, tcy = zth[0] + 230, zth[1] - 250
    t_tc = snap(t_cai + 0.35)
    sc.add("z_tcloud", think_cloud_svg(tcx, tcy, 1.5), z=30.6, wc=0.4, seed=850,
           motion=M.combine(popm(t_tc, (tcx - 90, tcy + 60), 0.35, wob=False), gZ))
    trail = [(zth[0] + 95, zth[1] - 120, 12), (zth[0] + 140, zth[1] - 170, 18)]
    for k, (x_, y_, r_) in enumerate(trail):
        sc.add(f"z_trail{k}", doc(S.g(PR._circ(x_, y_, r_, "#fffaf0", 3.4), filter="wobble-fine")), z=30.59, wc=0.3,
               seed=855 + k, motion=M.combine(popm(snap(t_tc - 0.25 + 0.12 * k), (x_, y_), 0.25, wob=False), gZ))
    for k in range(3):
        t_dot = snap(t_tc + 0.45 + 0.4 * k)
        dx_, dy_ = tcx - 48 + 48 * k, tcy
        sc.add(f"z_dot{k}", dot_svg(dx_, dy_, 13), z=30.61, wc=0, seed=851 + k,
               motion=M.combine(popm(t_dot, (dx_, dy_), 0.25, wob=False), gZ))
        sc.sfx("pop", t_dot, gain_db=-24)

    # ------------------------------------------------------------ SET P: the point of view
    sc.add("p_back", pov_back_svg(), z=20.0, seed=701, motion=gP)
    sc.add("p_row1", [pov_row_svg(1, k) for k in range(3)], z=20.1, seed=703, motion=gP,
           frame_at=lambda t: float(int((t + g0) / 0.5) % 3))
    sc.add("p_row0", [pov_row_svg(0, k) for k in range(3)], z=20.2, seed=705, motion=gP,
           frame_at=lambda t: float(int((t + g0) / 0.44 + 1) % 3))

    # ------------------------------------------------------------ camera
    camD1 = cam_keys([(t_cutB, Cam(1000, 570, 2000)), (t_jh, Cam(1000, 575, 2000)), (t_ai - 0.6, Cam(1040, 590, 2100)),
                      (t_cutP, Cam(1040, 590, 2100))], ["sine", "sine", "linear"])

    def bob(t):
        y = 0.0
        for tj in (t_hnao - 0.45, t_hnao + 0.15):
            if tj <= t <= tj + 0.5:
                y -= 70 * math.sin(math.pi * (t - tj) / 0.5)
        return y
    camP0 = cam_keys([(t_cutP, Cam(1056, 1386, 2112)), (t_cutB2, Cam(1056, 1300, 1900))], "sine")

    def camP(t):
        c = camP0(t)
        return Cam(c.x, c.y + bob(t), c.w)
    camD2 = cam_keys([(t_cutB2, Cam(1040, 590, 2100)), (t_cutZ, Cam(1040, 600, 2040))], "sine")
    camZ = cam_keys([(t_cutZ, Cam(1056, 594, 2112)), (min(T - 1.0, t_fa + 0.5), Cam(1040, 560, 1940)),
                     (T, Cam(1040, 560, 1940))], ["sine", "linear"])

    def cam(t):
        if t < t_cutB:
            return camA(t)
        if t < t_cutP:
            return camD1(t)
        if t < t_cutB2:
            return camP(t)
        if t < t_cutZ:
            return camD2(t)
        return camZ(t)
    sc.camera = cam

    # ------------------------------------------------------------ sound
    sc.sfx("crowd", 0, dur=t_pao, gain_db=-24, fade_in=0.8, fade_out=0.6)
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-28, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", t_pao - 0.3, dur=T - t_pao + 0.6, gain_db=-17, fade_in=0.8, fade_out=1.2)
    sc.sfx("cheer", t_pao + 0.6, dur=2.0, gain_db=-22, fade_in=0.4, fade_out=0.8)
    return sc
