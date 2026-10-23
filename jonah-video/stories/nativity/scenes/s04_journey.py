"""Scene 4 - Luke 2:1-5. Nazareth: Joseph the carpenter beside Mary at their house (he waves hello; little name tags
pop up); the emperor's herald reads the decree in the village square under a red Roman banner, the emperor's portrait
pops up, numbers pop over everyone's heads ('how many people?'); everyone packs up and sets off in different
directions to their home towns; a little list of names is written. A picture-book map unrolls: a dotted path runs from
拿撒勒 in the north to 伯利恒 in the south and a little board-game piece of Joseph, Mary and the donkey hops along it.
Then the road: Mary, now visibly expecting, rides the donkey with a hand on her belly (a little heart); they set off
along the long road while the sun and the moon chase each other over the sky (days passing); at last they reach the
hills of Bethlehem at dusk.

Beats (syllable onsets measured in the voice clip through the Storm film's Beats class; nothing hard-coded to the take):
  0 .. 0.9     calm page (the page-dip from s03 lands here): Mary and Joseph by their house, his sawhorse and plank,
               the donkey nibbling; clouds drift, hens peck
  '马利亚'      a name tag '马利亚' pops over Mary (pop)
  '约瑟'        a name tag '约瑟' pops over Joseph and he waves (hard-cut wave frames)
  '那时候'      cut to the village square: the herald on a stone step reads the decree (scroll), a red Roman banner
  '罗马皇帝'    the emperor's portrait medallion pops up beside the banner (chime)
  '一共有多少人' numbers 1..9 pop over the heads one by one (pop each), Joseph and Mary are 8 and 9
  '命令'        the herald raises the scroll and proclaims (horn)
  '每个人'      everyone turns and walks off with bundles, jars and sacks, half to the left and half to the right
               (planted-foot strides, footsteps); '老家': Mary and Joseph look at each other
  '登记名字'    a little name list pops up and '约瑟' '马利亚' are written on it (cloth, sparkle)
  '约瑟的老家'  cut: on a wooden table a scroll map unrolls (cloth): 拿撒勒 (north) ... on '伯利恒' its marker pops
  '也要去伯利恒' the dotted path draws from Nazareth down to Bethlehem while the little piece hops along it (pop
               hops); it arrives on the second '伯利恒' (sparkle)
  '这时候'      cut: morning at the start of the long road: Mary on the donkey (pregnant, hand on her belly, tender),
               Joseph holding the lead rope, looking back at her; the camera eases in
  '小宝宝'      a little heart pops over her belly (sparkle); '出生了' a few warm twinkles, and the sky begins to turn:
               from here to the end of line 5 it runs at one steady pace (~1.85 s a day) through two nights - the
               sun sets, stars and moon cross, dawn (a rooster), day again - and lands on the third evening; the land
               darkens and warms with it
  '走啊走'      from the end of line 4 the camera makes one slow 4 s pull-back and pan; on the first '走' Joseph turns and
               leads off (planted strides on the '走's and between them), the donkey walks, the rope sags and tightens
  '好多天'      at the end of the line, cut (dusk to dusk): the hills of Bethlehem with the lit little town ahead, the
               travellers arrived and still; calm hold - s05 starts on exactly this frame (plain 1 s cross-dissolve;
               s05 imports add_arrival).
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, cuts, heart_markup, snap
from stories.storm.scenes.s03_friends import Beats
from stories.nativity.scenes.s03_angel import (WASH, anemone, blink, blinks_for, breathm, clouds_markup, cypress, dipm,
                                               f1, flyer_frames, gate, hen_svg, olive, popm, sky_svg, stepper, vhouse)

INK = P["ink"]
CREAM = "#fff6e3"
WS, HS = 3600, 1188

JOSEPH_STEP = 86          # lead_a <-> lead_b: the planted ankle moves 86 px (scale 1)
TOWN_STEP = 84            # townsfolk walk_a <-> walk_b / carry_walk_a <-> _b
MARY_STEP = 73
DONKEY_CYCLE = 87         # px per donkey walk cycle (scale 1)


def doc(body, defs=""):
    return S.svg_doc(body, defs, WS, HS)


def clamp_cam(c, x0=0, x1=WS):
    cw = min(c.w, x1 - x0, HS * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, x0 + cw / 2), x1 - cw / 2), min(max(c.y, ch / 2), HS - ch / 2), cw, c.rot)


# ================================================================== little helpers


def name_tag(x, y, text, size=46, col="#3f62a2"):
    """A cream name label with a pointer under it, LXGW WenKai (anchor = pointer tip)."""
    w = size * (len(text) + 0.9)
    h = size * 1.45
    b = (f'<path d="M{f1(x - w / 2)},{f1(y - 18 - h)} h{f1(w)} q14,0 14,14 v{f1(h - 28)} q0,14 -14,14 h{f1(-w / 2 + 16)} '
         f'l-16,18 l-16,-18 h{f1(-w / 2 + 16)} q-14,0 -14,-14 v{f1(-h + 28)} q0,-14 14,-14 Z" fill="{CREAM}" '
         f'stroke="#cdb284" stroke-width="4"/>')
    b = S.g(b, filter="wobble-fine")
    b += (f'<text x="{f1(x + 7)}" y="{f1(y - 18 - h * 0.30)}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" '
          f'fill="{col}" text-anchor="middle">{text}</text>')
    return b


def number_badge(x, y, n, r=34):
    b = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f6d36b" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.18}" fill="#fff6d0" opacity="0.8"/>')
    b = S.g(b, filter="wobble-fine")
    b += (f'<text x="{x}" y="{y + r * 0.42}" font-family="LXGW WenKai" font-weight="bold" font-size="{r * 1.3:.0f}" '
          f'fill="{INK}" text-anchor="middle">{n}</text>')
    return b


def joseph_wave(x, y, s, facing=1, k=0, expr="joyful"):
    """Joseph waving hello with his open far hand (two wave frames k=0/1); staff in the near hand."""
    a1, a2 = ((100, 150), (122, 166))[k % 2]
    ps = dict(C._JCZ["talk"])
    ps["arms"] = (("fk", a1, a2), C._JC_STAFF_ARM)
    ps["hands"] = ("open", "fist")
    D = C._joseph_c_design()
    D["front"] = C._hooks(C._joseph_staff(D))
    inner, _ = C._figure(D, C._JOSEPH_C_M, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"joseph_carpenter-n345wave{k}")


def joseph(x, y, s, facing=1, pose="stand", expr=None, staff=True, shadow=True, phase=0.0):
    sh = C.ground_shadow(x, y, s, 120, 0.18) if shadow else ""
    return sh + C.joseph_carpenter(x, y, s, facing, pose=pose, expr=expr, staff=staff, phase=phase)


def townie(x, y, s, facing, kind, v, pose, item=None, expr=None, phase=0.0, shadow=True):
    sh = C.ground_shadow(x, y, s, 110, 0.16) if shadow else ""
    return sh + C.townsfolk(x, y, s, facing, kind=kind, variant=v, pose=pose, item=item, expr=expr, phase=phase)


# ================================================================== the travellers (donkey + Mary + Joseph + rope)
HALTER = "#b8473c"


def halter_local(nod=0.0):
    hx, hy = 128, -214 + nod
    d = (f"M{hx - 14},{hy - 18} Q{hx - 22},{hy + 10} {hx - 4},{hy + 34} M{hx - 6},{hy + 28} Q{hx + 16},{hy + 44} "
         f"{hx + 36},{hy + 30}")
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{HALTER}" stroke-width="3.6" stroke-linecap="round"/>'
            f'<circle cx="{hx + 34}" cy="{hy + 32}" r="5" fill="#d9b46a" stroke="{INK}" stroke-width="2.2"/>')


def donkey_svg(x, y, s, facing=1, pose="stand", phase=0.0, eyes="open", shadow=True):
    """props.donkey with Mary's blue saddle blanket and a halter whose ring the rope dynamic layer starts from."""
    walk = pose == "walk"
    bob = -3 * math.sin(4 * math.pi * phase) if walk else 0.0
    nod = 4 * math.sin(2 * math.pi * phase) if walk else 0.0
    sh = C.ground_shadow(x, y, s, 250, 0.18) if shadow else ""
    return (sh + PR.donkey(x, y, s, facing, pose=pose, phase=phase, saddle="blue", eyes=eyes) +
            PR._place(halter_local(nod + bob), x, y, s, facing))


def halter_ring(phase, walk):
    bob = -3 * math.sin(4 * math.pi * phase) if walk else 0.0
    nod = 4 * math.sin(2 * math.pi * phase) if walk else 0.0
    return 162.0, -182.0 + nod + bob


class Travellers:
    """Joseph leading the donkey with Mary riding it. All drawings sit at a reference anchor (xr, yr) at scale K and
    are moved / scaled by motion functions, so any path and perspective works:
      dpos(t) -> (x, y, k)       donkey anchor (stage) and perspective factor
      dphase(t) -> walk phase in [0, 1) or None (standing)
      jpos(t) -> (x, y, k)       Joseph anchor
      jframe(t) -> key into self.jkeys;  mframe(t) -> key into self.mkeys;  deyes(t) -> 'open' | 'closed'
    Joseph's poses: ('lead_a'|'lead_b'|'stand'|..., facing, expr); Mary's: (expr, ...) riding, pregnant."""

    def __init__(self, sc, name, K, xr, yr, jkeys, mkeys, z=3.0, gatef=None, seed=400, clock=None):
        self.clock = clock or (lambda t: t)
        self.sc, self.name, self.K, self.xr, self.yr = sc, name, K, xr, yr
        self.jkeys, self.mkeys, self.z, self.gatef, self.seed = list(jkeys), list(mkeys), z, gatef, seed
        self.seat = PR.donkey_points(xr, yr, K, 1, "stand")["seat"]
        self.jx_ref = xr + (PR.DONKEY_LEAD[0] - C.JOSEPH_LEAD_HAND[0]) * K

    def add(self, dpos, dphase, jpos, jframe, mframe, deyes=lambda t: "open", jextra=None, mextra=None):
        sc, K, xr, yr = self.sc, self.K, self.xr, self.yr
        g = self.gatef or (lambda t: Tf())
        # ---- donkey: 8 walk phases + stand (+ blink)
        dfr = [S.svg_doc(donkey_svg(xr, yr, K, 1, "walk", k / 8), "", WS, HS) for k in range(8)]
        dfr += [S.svg_doc(donkey_svg(xr, yr, K, 1, "stand"), "", WS, HS),
                S.svg_doc(donkey_svg(xr, yr, K, 1, "stand", eyes="closed"), "", WS, HS)]

        def qphase(t):
            ph = dphase(t)
            return None if ph is None else (int((ph % 1.0) * 8 + 1e-6) % 8) / 8

        def d_fa(t):
            q = qphase(t)
            if q is None:
                return 9.0 if deyes(t) == "closed" else 8.0
            return float(round(q * 8) % 8)

        def d_mot(t):
            x, y, k = dpos(t)
            a = g(t).alpha
            return Tf(dx=x - xr, dy=y - yr, sx=k, sy=k, px=xr, py=yr, alpha=a)
        sc.add(f"{self.name}_donkey", dfr, z=self.z, frame_at=d_fa, motion=d_mot, seed=self.seed)
        # ---- Mary riding (follows the seat bob)
        sx, sy = self.seat
        mfr = [S.svg_doc(C.mary(sx, sy, K, 1, pose="ride", expr=e, pregnant=True), "", WS, HS) for e in self.mkeys]

        def m_mot(t):
            x, y, k = dpos(t)
            q = qphase(t)
            bob = -3 * math.sin(4 * math.pi * q) if q is not None else 0.0
            a = g(t).alpha
            br = 1 + 0.008 * math.sin(2 * math.pi * self.clock(t) / 2.9)
            return Tf(dx=x - xr, dy=y - yr + bob * K * k, sx=k, sy=k * br, px=xr, py=yr, alpha=a)
        sc.add(f"{self.name}_mary", mfr, z=self.z + 0.02, frame_at=lambda t: float(mframe(t)),
               motion=M.combine(m_mot, mextra) if mextra else m_mot, seed=self.seed + 1)
        # ---- Joseph
        jfr, jhand = [], []
        for pose, f, e in self.jkeys:
            jx = self.jx_ref
            jfr.append(S.svg_doc(joseph(jx, yr, K, f, pose, e, staff=False), "", WS, HS))
            jhand.append(C.body_points(C.joseph_carpenter, jx, yr, K, f, pose=pose, expr=e, staff=False)["hands"][1])

        def j_mot(t):
            x, y, k = jpos(t)
            a = g(t).alpha
            br = 1 + 0.008 * math.sin(2 * math.pi * self.clock(t) / 3.1 + 1.0)
            return Tf(dx=x - self.jx_ref, dy=y - yr, sx=k, sy=k * br, px=self.jx_ref, py=yr, alpha=a)
        sc.add(f"{self.name}_joseph", jfr, z=self.z + 0.04, frame_at=lambda t: float(jframe(t)),
               motion=M.combine(j_mot, jextra) if jextra else j_mot, seed=self.seed + 2)

        # ---- the lead rope: from the halter ring to Joseph's near fist (sags when slack)
        def rope(t):
            if g(t).alpha <= 0.01:
                return None
            x, y, k = dpos(t)
            q = qphase(t)
            rx, ry = halter_ring(q if q is not None else 0.0, q is not None)
            a = (x + rx * K * k, y + ry * K * k)
            jx, jy, jk = jpos(t)
            hx, hy = jhand[int(jframe(t))]
            b = (jx + (hx - self.jx_ref) * jk, jy + (hy - yr) * jk)
            dist = math.hypot(b[0] - a[0], b[1] - a[1])
            rest = 105 * K * k
            sag = 10 * K * k + max(0.0, rest - dist) * 0.55
            return draw_rope(a, b, sag, K * k)
        sc.add_dynamic(f"{self.name}_rope", rope, z=self.z + 0.03)


def draw_rope(a, b, sag, s, ss=3):
    """A rope from a to b (stage px) sagging by `sag`; drawn at ss x and downsampled (ink outline, rope colour)."""
    pad = 20
    x0, y0 = min(a[0], b[0]) - pad, min(a[1], b[1]) - pad
    x1, y1 = max(a[0], b[0]) + pad, max(a[1], b[1]) + pad + sag
    w, h = int(x1 - x0) + 1, int(y1 - y0) + 1
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag * 2
    pts = []
    for i in range(17):
        u = i / 16
        x = (1 - u) ** 2 * a[0] + 2 * u * (1 - u) * mx + u * u * b[0]
        y = (1 - u) ** 2 * a[1] + 2 * u * (1 - u) * my + u * u * b[1]
        pts.append(((x - x0) * ss, (y - y0) * ss))
    d.line(pts, fill=(75, 52, 38, 255), width=max(2, int(6.5 * s * ss)), joint="curve")
    d.line(pts, fill=(197, 140, 90, 255), width=max(1, int(3.4 * s * ss)), joint="curve")
    im = im.resize((w, h), Image.LANCZOS)
    return im, (int(x0), int(y0))


# ================================================================== the village panorama (house + square)
HOUSE = (820, 905, 1.0)
GY = 940                  # people's ground line in front of the house / in the square
PLAT = (2700, 905)        # the herald's step (top centre)
BANNER_X = 2860


def pano_back_svg():
    sky, defs = sky_svg(WS, HS, sun=(3320, 120), key="n4")
    b = sky
    far = S.path(S.hill(-200, WS + 200, 560, 110, seed=41, bumps=7), fill="#c3c8b8", sw=2.4)
    far += S.path(S.hill(-200, WS + 200, 625, 80, seed=42, bumps=8), fill="#b4c09e", sw=2.6)
    b += S.g(far, filter="wobble")
    # the village hill behind, houses climbing it
    hill = [(-120, 640), (300, 520), (800, 470), (1400, 430), (2000, 420), (2600, 450), (3200, 500), (3720, 560)]
    defs += S.lin_grad("n4hill", [(0, "#cfc896"), (0.45, "#bdbb80"), (1, "#a8ae6c")])
    b += S.g(S.path(S.smooth_path(hill, closed=False) + f" L3720,{HS + 40} L-120,{HS + 40} Z", fill="url(#n4hill)",
                    sw=3.4), filter="wobble")
    rng = random.Random(14)
    cols = [WASH, "#efe3c8", "#f4ecdc", "#e9d9b8", "#efe6d2", "#f0dcc0"]
    doors = ["#5f7f9a", "#7a5a40", "#4f8f8a", "#9a6a42", "#b8603e"]

    def top(x):
        for (xa, ya), (xb, yb) in zip(hill, hill[1:]):
            if xa <= x <= xb:
                return ya + (yb - ya) * (x - xa) / (xb - xa)
        return hill[-1][1]
    hs = ""
    for i, x in enumerate(range(-40, WS + 60, 130)):
        hs += olive(x + rng.uniform(-30, 30), top(x) + 30, 0.32, 80 + i, col="#a9b585", dark="#8a9864")
    for r in (3, 2, 1, 0):
        k = 0.82 - 0.1 * r
        xx = -40 + rng.uniform(0, 80)
        while xx < WS + 40:
            w = rng.uniform(96, 146) * k
            h = rng.uniform(66, 100) * k
            y0 = top(xx + w / 2) + 70 + 62 * (3 - r) + rng.uniform(-4, 4)
            if rng.random() < 0.2:
                hs += olive(xx + 40 * k, y0, 0.4 * k + 0.06, int(xx) + r)
                xx += 100 * k
                continue
            hs += vhouse(xx, y0, w, h, rng.choice(cols), door=rng.choice(doors), win=rng.choice((1, 1, 2)),
                         stair=4 if rng.random() < 0.2 else 0, seed=int(xx) + 7 * r, s=k, dome=rng.random() < 0.06,
                         awning=rng.choice((None, None, "#c9714a", "#5f97a8")))
            if rng.random() < 0.28:
                hs += cypress(xx + w + 18 * k, y0 + 2, rng.uniform(110, 160) * k, 26 * k, sw=2.2)
                xx += 26 * k
            xx += w + rng.uniform(24, 60) * k
    b += S.g(hs, filter="wobble-fine")
    return doc(b, defs)


def well_svg(x, y):
    """A round stone well with a wooden frame, rope and bucket (anchor = front foot of the well)."""
    b = f'<ellipse cx="{x}" cy="{y - 92}" rx="96" ry="26" fill="#5a4a3a" stroke="{INK}" stroke-width="3.6"/>'
    b += f'<path d="M{x - 96},{y - 92} L{x - 96},{y - 8} Q{x},{y + 22} {x + 96},{y - 8} L{x + 96},{y - 92} Q{x},{y - 66} {x - 96},{y - 92} Z" fill="#d6c39c" stroke="{INK}" stroke-width="3.6"/>'
    rng = random.Random(3)
    for row in range(3):
        for i in range(6):
            sx = x - 84 + i * 34 + (17 if row % 2 else 0)
            sy = y - 70 + row * 26 + 8 * math.sin((sx - x) / 96 * 1.4)
            if abs(sx - x) < 88:
                b += f'<ellipse cx="{sx}" cy="{sy:.1f}" rx="14" ry="9" fill="{S.mix("#c9b48e", "#e2d2ae", rng.random())}" stroke="{S.shade("#c9b48e", -0.4)}" stroke-width="1.8"/>'
    b += f'<ellipse cx="{x}" cy="{y - 92}" rx="96" ry="26" fill="none" stroke="{INK}" stroke-width="3.6"/>'
    for sx in (-80, 80):
        b += f'<path d="M{x + sx - 7},{y - 90} L{x + sx - 5},{y - 250} L{x + sx + 7},{y - 250} L{x + sx + 9},{y - 90} Z" fill="{PR.NAT_WOOD}" stroke="{INK}" stroke-width="3.2"/>'
    b += f'<rect x="{x - 96}" y="{y - 262}" width="192" height="18" rx="6" fill="{PR.NAT_WOOD_DARK}" stroke="{INK}" stroke-width="3.2"/>'
    b += f'<path d="M{x + 10},{y - 244} L{x + 10},{y - 170}" stroke="#c9a46a" stroke-width="4"/>'
    b += f'<path d="M{x - 8},{y - 172} h36 l-6,40 h-24 Z" fill="#a8794c" stroke="{INK}" stroke-width="3"/>'
    return S.g(b, filter="wobble-fine")


def platform_svg(x, y):
    """The herald's two-step stone platform (top at y)."""
    b = ""
    for i, (w, h, yy) in enumerate(((300, 26, y + 10), (240, 30, y - 18))):
        b += f'<path d="M{x - w / 2},{yy + h} L{x - w / 2},{yy} L{x + w / 2},{yy} L{x + w / 2},{yy + h} Z" fill="{S.mix("#d9c7a2", "#cbb68e", i)}" stroke="{INK}" stroke-width="3.4"/>'
        for j in range(1, 5):
            b += f'<path d="M{x - w / 2 + j * w / 5},{yy} v{h}" stroke="{S.shade("#cbb68e", -0.3)}" stroke-width="2"/>'
    b += f'<path d="M{x - 160},{y + 36} L{x - 150},{y + 66} L{x + 150},{y + 66} L{x + 160},{y + 36} Z" fill="#c9b38a" stroke="{INK}" stroke-width="3.4"/>'
    return S.g(b, filter="wobble-fine")


def banner_svg(sway=0.0):
    """A red Roman banner with a golden eagle on a pole (sway -1..1 swings its tails)."""
    x, top, bot = BANNER_X, 470, 905
    b = f'<path d="M{x - 6},{bot + 30} L{x - 5},{top} L{x + 5},{top} L{x + 6},{bot + 30} Z" fill="{PR.NAT_WOOD_DARK}" stroke="{INK}" stroke-width="3"/>'
    b += f'<rect x="{x - 70}" y="{top + 20}" width="140" height="12" rx="5" fill="#d9a83c" stroke="{INK}" stroke-width="2.8"/>'
    sk = 10 * sway
    d = (f"M{x - 64},{top + 32} L{x + 64},{top + 32} L{x + 64 + sk},{top + 220} L{x + 32 + sk},{top + 196} "
         f"L{x + sk},{top + 222} L{x - 32 + sk},{top + 196} L{x - 64 + sk},{top + 220} Z")
    b += f'<path d="{d}" fill="#b8342c" stroke="{INK}" stroke-width="3.4"/>'
    b += f'<path d="M{x - 54},{top + 44} L{x + 54},{top + 44}" stroke="#e9c35c" stroke-width="4"/>'
    ey = top + 110
    # golden eagle with spread wings
    eg = "#efc04a"
    for sx in (-1, 1):
        b += (f'<path d="M{x},{ey} Q{x + sx * 30},{ey - 30} {x + sx * 50},{ey - 22} L{x + sx * 44},{ey - 12} '
              f'L{x + sx * 50},{ey - 4} L{x + sx * 40},{ey + 4} L{x + sx * 44},{ey + 12} Q{x + sx * 22},{ey + 12} {x},{ey + 20} Z" '
              f'fill="{eg}" stroke="{INK}" stroke-width="2.4"/>')
    b += f'<ellipse cx="{x}" cy="{ey + 10}" rx="11" ry="20" fill="{eg}" stroke="{INK}" stroke-width="2.4"/>'
    b += f'<circle cx="{x}" cy="{ey - 16}" r="9" fill="{eg}" stroke="{INK}" stroke-width="2.4"/>'
    b += f'<path d="M{x + 7},{ey - 18} l9,4 l-9,3 Z" fill="#e08a3c" stroke="{INK}" stroke-width="1.6"/>'
    b += f'<path d="M{x - 20},{ey + 40} Q{x},{ey + 56} {x + 20},{ey + 40}" fill="none" stroke="{eg}" stroke-width="5"/>'
    b += f'<circle cx="{x}" cy="{top - 4}" r="11" fill="#e9c35c" stroke="{INK}" stroke-width="2.6"/>'
    return S.svg_doc(S.g(b, filter="wobble-fine"), "", WS, HS)


def emperor_svg(x, y, r=120):
    """A round golden medallion with a friendly cartoon portrait of the Roman emperor (laurel wreath, purple toga)."""
    skin, hair = "#e9b98e", "#7a5a3c"
    b = f'<circle cx="{x}" cy="{y}" r="{r + 16}" fill="#e9b83c" stroke="{INK}" stroke-width="5"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f6e7c2" stroke="{INK}" stroke-width="3.4"/>'
    cid = "n4medc"
    inner = f'<path d="M{x - 90},{y + r} Q{x - 86},{y + 40} {x},{y + 36} Q{x + 86},{y + 40} {x + 90},{y + r} Z" fill="#7b4f9d" stroke="{INK}" stroke-width="3.4"/>'
    inner += f'<path d="M{x - 40},{y + 42} L{x + 10},{y + r} M{x - 48},{y + 50} L{x + 2},{y + r}" stroke="#e9c35c" stroke-width="6"/>'
    inner += f'<path d="M{x - 18},{y + 20} h36 v22 q-18,10 -36,0 Z" fill="{skin}" stroke="{INK}" stroke-width="3"/>'
    inner += f'<ellipse cx="{x}" cy="{y - 18}" rx="46" ry="50" fill="{skin}" stroke="{INK}" stroke-width="3.4"/>'
    inner += f'<path d="M{x - 44},{y - 26} Q{x - 46},{y - 70} {x},{y - 70} Q{x + 46},{y - 70} {x + 44},{y - 26} Q{x + 30},{y - 50} {x},{y - 52} Q{x - 30},{y - 50} {x - 44},{y - 26} Z" fill="{hair}" stroke="{INK}" stroke-width="3"/>'
    for th in (168, 148, 128, 108, 72, 52, 32, 12):
        a = math.radians(th)
        lx, ly = x + 54 * math.cos(a), y - 30 - 46 * math.sin(a)
        inner += (f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="15" ry="7" fill="#6f9a52" stroke="{INK}" stroke-width="1.8" '
                  f'transform="rotate({-th + 90 + (25 if th > 90 else -25):.0f} {lx:.1f} {ly:.1f})"/>')
    inner += f'<circle cx="{x - 16}" cy="{y - 16}" r="5" fill="{INK}"/><circle cx="{x + 16}" cy="{y - 16}" r="5" fill="{INK}"/>'
    inner += f'<circle cx="{x - 18}" cy="{y - 18}" r="1.6" fill="#fff"/><circle cx="{x + 14}" cy="{y - 18}" r="1.6" fill="#fff"/>'
    inner += f'<path d="M{x - 12},{y + 6} Q{x},{y + 16} {x + 12},{y + 6}" fill="none" stroke="{INK}" stroke-width="3"/>'
    inner += f'<ellipse cx="{x - 28}" cy="{y}" rx="8" ry="5" fill="{P["cheek"]}" opacity="0.7"/><ellipse cx="{x + 28}" cy="{y}" rx="8" ry="5" fill="{P["cheek"]}" opacity="0.7"/>'
    b += f'<clipPath id="{cid}"><circle cx="{x}" cy="{y}" r="{r - 2}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" stroke-width="3.4"/>'
    for i in range(12):
        a = 2 * math.pi * i / 12
        b += f'<circle cx="{x + (r + 8) * math.cos(a):.1f}" cy="{y + (r + 8) * math.sin(a):.1f}" r="4" fill="#fff2c4"/>'
    return S.svg_doc(S.g(b, filter="wobble-fine"), "", WS, HS)


def pano_near_svg():
    """Mary's house, Joseph's sawhorse, the lane; the square with its houses, well and the herald's step."""
    defs = S.lin_grad("n4gnd", [(0, "#e2c798"), (1, "#c9a672")])
    b = ""
    # big houses along the back of the square
    sq = ""
    for x, w, h, col, door, aw, st in ((1900, 300, 250, "#efe3c8", "#4f8f8a", "#c9714a", 0),
                                       (2280, 250, 300, WASH, "#7a5a40", None, 5),
                                       (3010, 280, 260, "#f0dcc0", "#5f7f9a", "#5f97a8", 0),
                                       (3360, 300, 300, "#efe6d2", "#9a6a42", "#c9714a", 0)):
        sq += vhouse(x, 880, w, h, col, door=door, win=2, stair=st, seed=x, s=1.25, awning=aw)
    b += S.g(sq, filter="wobble-fine")
    b += S.g(cypress(2640, 878, 260, 44) + cypress(2955, 878, 220, 40), filter="wobble-fine")
    b += olive(1660, 905, 0.85, 31)
    b += PR.nazareth_house(*HOUSE[:2], HOUSE[2], 1, view="exterior", time="day")
    # the ground: lane in front of the house, the square
    gd = f"M-60,{HS + 40} L-60,880 Q900,868 1800,876 Q2700,880 3700,876 L3700,{HS + 40} Z"
    b += S.g(S.path(gd, fill="url(#n4gnd)", sw=3.4), filter="wobble")
    rng = random.Random(23)
    pv = ""
    for i in range(120):                       # paving stones in the square, pebbles along the lane
        x = rng.uniform(1820, 3640)
        y = rng.uniform(900, 1180)
        pv += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(26, 44) * (0.6 + 0.4 * (y - 880) / 300))}" '
               f'ry="{f1(rng.uniform(10, 16) * (0.6 + 0.4 * (y - 880) / 300))}" fill="#d6b884" stroke="#b8956a" stroke-width="1.6" opacity="0.8"/>')
    for i in range(40):
        x = rng.uniform(-40, 1800)
        y = rng.uniform(890, 1100)
        pv += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(5, 10))}" ry="{f1(rng.uniform(3, 5))}" fill="#c9a272" opacity="0.8"/>'
    b += S.g(pv, filter="wobble-fine")
    b += well_svg(2300, 930)
    b += platform_svg(*PLAT)
    # Joseph's carpentry: a sawhorse with a plank, a saw leaning on it, a pile of timber
    b += PR.timber_pile(1600, 940, 0.55)
    b += PR.sawhorse(1440, 950, 0.75)
    b += PR.saw(1500, 952, 0.6, 1, rot=-70)
    for x, y, s_, v in ((120, 1010, 0.8, 0), (560, 1040, 0.7, 2), (1820, 1060, 0.8, 1), (3560, 1050, 0.9, 0)):
        b += PR.grass_tuft(x, y, s_, variant=v)
    fl = ""
    for i in range(16):
        fl += anemone(rng.uniform(0, 1700), rng.uniform(1060, 1170), rng.uniform(0.8, 1.1),
                      rng.choice(("#d8463c", "#f2f0e2", "#c9a6e0")))
    b += S.g(fl, filter="wobble-fine")
    return doc(b, defs)


# ================================================================== the map
MAPC = (1056, 520)


def table_svg():
    defs = S.lin_grad("n4tab", [(0, "#8a5a3a"), (1, "#6e452c")])
    b = f'<rect x="-40" y="-40" width="2200" height="1280" fill="url(#n4tab)"/>'
    for i in range(9):
        y = 40 + i * 140
        b += f'<path d="M-40,{y} Q1000,{y + 18} 2160,{y - 10}" fill="none" stroke="#5a3a24" stroke-width="3" opacity="0.5"/>'
    b += f'<ellipse cx="1056" cy="560" rx="1100" ry="700" fill="#f6d9a0" opacity="0.18"/>'
    return doc(S.g(b, filter="wobble"), defs)


NAZ = (1060, 300)
BETH = (985, 772)
PATH = [(1060, 318), (1215, 540), (990, 752)]       # quadratic bezier Nazareth -> Bethlehem


def bez(u, p=PATH):
    (x0, y0), (x1, y1), (x2, y2) = p
    return ((1 - u) ** 2 * x0 + 2 * u * (1 - u) * x1 + u * u * x2, (1 - u) ** 2 * y0 + 2 * u * (1 - u) * y1 + u * u * y2)


def map_svg(half=None):
    """The parchment map (to be unrolled): coast and sea, the lake of Galilee, the Jordan, the Dead Sea, hills, trees,
    Nazareth's house marker with its label, a compass."""
    x0, y0, x1, y1 = 300, 60, 1812, 960
    b = f'<path d="M{x0},{y0} Q{(x0 + x1) / 2},{y0 - 14} {x1},{y0} L{x1},{y1} Q{(x0 + x1) / 2},{y1 + 14} {x0},{y1} Z" fill="#f2e2bc" stroke="{INK}" stroke-width="4"/>'
    rng = random.Random(8)
    for i in range(14):
        b += f'<ellipse cx="{rng.uniform(x0 + 60, x1 - 60):.0f}" cy="{rng.uniform(y0 + 60, y1 - 60):.0f}" rx="{rng.uniform(60, 160):.0f}" ry="{rng.uniform(30, 70):.0f}" fill="#e6d0a0" opacity="0.45"/>'
    cid = "n4mapc"
    sea = (f"M{x0 - 10},{y0 - 10} L790,{y0 - 10} Q760,200 730,330 Q700,470 660,600 Q630,720 600,{y1 + 10} L{x0 - 10},{y1 + 10} Z")
    inner = f'<path d="{sea}" fill="#a9d0da" stroke="{INK}" stroke-width="3.4"/>'
    for i in range(8):
        wx, wy = 400 + (i % 3) * 90, 160 + i * 95
        inner += f'<path d="M{wx},{wy} q12,-10 24,0 q12,10 24,0" fill="none" stroke="#5f97a8" stroke-width="3"/>'
    inner += f'<path d="M790,{y0} Q760,200 730,330 Q700,470 660,600 Q630,720 600,{y1}" fill="none" stroke="#7fb3c4" stroke-width="10" opacity="0.6"/>'
    # green land wash, hills, trees
    inner += f'<path d="M800,{y0} Q1100,140 1500,{y0} L1500,420 Q1200,520 820,460 Z" fill="#c9d39a" opacity="0.5"/>'
    for (hx, hy, s_) in ((880, 200, 1.0), (930, 380, 0.9), (1150, 420, 1.0), (860, 560, 1.1), (1100, 640, 0.9),
                         (900, 690, 0.8), (1180, 860, 1.0), (840, 860, 0.9), (1420, 520, 0.9), (1500, 300, 0.8),
                         (1620, 640, 1.0), (1650, 820, 0.9)):
        inner += f'<path d="M{hx - 40 * s_},{hy} Q{hx - 20 * s_},{hy - 34 * s_} {hx},{hy - 36 * s_} Q{hx + 20 * s_},{hy - 34 * s_} {hx + 40 * s_},{hy}" fill="#d9c08a" stroke="{S.shade("#d9c08a", -0.45)}" stroke-width="3"/>'
    for (tx, ty) in ((960, 250), (1000, 230), (1120, 330), (950, 470), (1220, 700), (880, 780), (1080, 860)):
        inner += f'<path d="M{tx},{ty} v-16" stroke="{PR.NAT_WOOD_DARK}" stroke-width="3"/><circle cx="{tx}" cy="{ty - 24}" r="12" fill="#8fab62" stroke="{INK}" stroke-width="2.4"/>'
    # the lake of Galilee, the Jordan, the Dead Sea
    inner += f'<path d="M1330,170 Q1385,175 1392,250 Q1396,330 1345,345 Q1300,340 1302,260 Q1300,180 1330,170 Z" fill="#9cc8d6" stroke="{INK}" stroke-width="3.4"/>'
    inner += f'<path d="M1345,345 Q1370,420 1340,480 Q1310,540 1350,600 Q1385,660 1345,700" fill="none" stroke="#7fb3c4" stroke-width="9"/>'
    inner += f'<path d="M1345,345 Q1370,420 1340,480 Q1310,540 1350,600 Q1385,660 1345,700" fill="none" stroke="{INK}" stroke-width="2" opacity="0.5"/>'
    inner += f'<path d="M1330,700 Q1385,705 1385,800 Q1385,900 1338,915 Q1296,905 1300,800 Q1298,705 1330,700 Z" fill="#9cc8d6" stroke="{INK}" stroke-width="3.4"/>'
    b += f'<clipPath id="{cid}"><path d="M{x0},{y0} Q{(x0 + x1) / 2},{y0 - 14} {x1},{y0} L{x1},{y1} Q{(x0 + x1) / 2},{y1 + 14} {x0},{y1} Z"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'
    b += f'<path d="M{x0},{y0} Q{(x0 + x1) / 2},{y0 - 14} {x1},{y0} L{x1},{y1} Q{(x0 + x1) / 2},{y1 + 14} {x0},{y1} Z" fill="none" stroke="{INK}" stroke-width="4"/>'
    b += f'<path d="M{x0 + 22},{y0 + 22} L{x1 - 22},{y0 + 22} L{x1 - 22},{y1 - 22} L{x0 + 22},{y1 - 22} Z" fill="none" stroke="#b8956a" stroke-width="3" stroke-dasharray="14 10"/>'
    # compass
    cx, cy = 1650, 210
    b += f'<circle cx="{cx}" cy="{cy}" r="56" fill="#f6ebcf" stroke="{INK}" stroke-width="3"/>'
    b += f'<path d="M{cx},{cy - 70} L{cx + 14},{cy} L{cx},{cy + 70} L{cx - 14},{cy} Z" fill="#c9714a" stroke="{INK}" stroke-width="2.6"/>'
    b += f'<path d="M{cx - 70},{cy} L{cx},{cy - 12} L{cx + 70},{cy} L{cx},{cy + 12} Z" fill="#e9c35c" stroke="{INK}" stroke-width="2.4"/>'
    body = S.g(b, filter="wobble-fine")
    body += f'<text x="{cx}" y="{cy - 82}" font-family="LXGW WenKai" font-weight="bold" font-size="44" fill="{INK}" text-anchor="middle">北</text>'
    # Nazareth: a little white house with a teal door
    nx, ny = NAZ
    hb = (f'<path d="M{nx - 30},{ny + 22} L{nx - 30},{ny - 14} L{nx + 30},{ny - 14} L{nx + 30},{ny + 22} Z" fill="#f6f0e2" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M{nx - 36},{ny - 14} h72 v-8 h-72 Z" fill="#e2d4b4" stroke="{INK}" stroke-width="2.6"/>'
          f'<path d="M{nx - 8},{ny + 22} v-18 q8,-8 16,0 v18 Z" fill="#4f8fa8" stroke="{INK}" stroke-width="2.2"/>')
    body += S.g(hb, filter="wobble-fine")
    body += label_markup(nx - 150, ny - 30, "拿撒勒")
    if half is not None:
        cx_ = MAPC[0]
        x_a, x_b = (0, cx_) if half < 0 else (cx_, 2112)
        body = (f'<clipPath id="n4mh{half + 1}"><rect x="{x_a}" y="0" width="{x_b - x_a}" height="{HS}"/></clipPath>'
                f'<g clip-path="url(#n4mh{half + 1})">{body}</g>')
    return doc(body)


def label_markup(x, y, text, size=56):
    w = size * (len(text) + 0.6)
    b = S.g(f'<rect x="{x - w / 2}" y="{y - size * 0.9}" width="{w}" height="{size * 1.3}" rx="16" fill="{CREAM}" '
            f'stroke="#b8956a" stroke-width="3.4"/>', filter="wobble-fine")
    b += (f'<text x="{x}" y="{y + size * 0.12}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" '
          f'fill="{INK}" text-anchor="middle">{text}</text>')
    return b


def beth_marker_svg():
    bx, by = BETH
    b = ""
    for i, (dx, dy, w, h) in enumerate(((-26, 0, 34, 30), (8, -8, 40, 38), (-6, 14, 30, 24))):
        b += (f'<path d="M{bx + dx - w / 2},{by + dy + 14} v{-h} h{w} v{h} Z" fill="{("#f2e2c4", "#e9d6b0", "#f6ecd6")[i]}" stroke="{INK}" stroke-width="2.8"/>'
              f'<rect x="{bx + dx - 4}" y="{by + dy + 14 - h * 0.6}" width="8" height="10" fill="#f6c25a" stroke="{INK}" stroke-width="1.6"/>')
    body = S.g(b, filter="wobble-fine")
    body += label_markup(bx + 200, by + 26, "伯利恒")
    return doc(body)


def path_svg():
    pts = [bez(i / 40) for i in range(41)]
    d = S.smooth_path(pts, closed=False)
    return doc(f'<path d="{d}" fill="none" stroke="#b8473c" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 24"/>')


def token_svg():
    """A little board-game piece: Joseph leading the donkey with Mary riding, on a round wooden base."""
    x, y = NAZ[0], NAZ[1] + 24
    s = 0.27
    b = f'<ellipse cx="{x}" cy="{y}" rx="104" ry="24" fill="{PR.NAT_WOOD}" stroke="{INK}" stroke-width="3.4"/>'
    b += f'<path d="M{x - 104},{y} v10 q104,30 208,0 v-10" fill="{PR.NAT_WOOD_DARK}" stroke="{INK}" stroke-width="3.4"/>'
    b += f'<ellipse cx="{x}" cy="{y}" rx="104" ry="24" fill="{PR.NAT_WOOD_LIGHT}" stroke="{INK}" stroke-width="3"/>'
    dx = x - 40
    b += PR.donkey(dx, y, s, 1, pose="stand", saddle="blue", bridle=True)
    st = PR.donkey_points(dx, y, s, 1, "stand")
    b += C.mary(*st["seat"], s, 1, pose="ride", pregnant=True)
    b += C.joseph_carpenter(st["lead"][0] - C.JOSEPH_LEAD_HAND[0] * s, y, s, 1, pose="lead_a", expr="kind")
    return doc(b)


def rolls_svg(side):
    x = MAPC[0]
    return doc(S.g(f'<rect x="{x - 26}" y="40" width="52" height="940" rx="22" fill="#e2cb98" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="{x - 10}" y="18" width="20" height="30" rx="5" fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
                   f'<rect x="{x - 10}" y="972" width="20" height="30" rx="5" fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
                   f'<path d="M{x - 8},70 L{x - 8},950" stroke="{S.shade("#e2cb98", -0.25)}" stroke-width="3"/>',
                   filter="wobble-fine"))


# ================================================================== the road (days passing)
RX0, RX1, RY = -1300, 2300, 1060       # journey_road placement: the winding road climbs to the far town at x ~1580
YR = 1002                             # the near path the travellers walk on (crossing the land in front)
REF = Cam(1056, 594, 2112)            # sky drawn for this camera, then pinned to the screen
KR = 0.74                             # travellers' scale on the road


def road_at(d):
    """(x, y, k) of the near path at x = d (straight, no perspective)."""
    return d, YR, 1.0


def near_path_markup():
    """The near footpath across the land (the travellers walk on it); it joins the winding road to Bethlehem."""
    rng = random.Random(17)
    d = (f"M-60,{YR - 34} Q600,{YR - 44} 1200,{YR - 36} Q1800,{YR - 28} 2400,{YR - 40} L2400,{YR + 38} Q1800,{YR + 30} "
         f"1200,{YR + 40} Q600,{YR + 46} -60,{YR + 34} Z")
    b = S.path(d, fill="#e2c99a", sw=3.2)
    for i in range(60):
        x = rng.uniform(-40, 2380)
        b += f'<ellipse cx="{x:.0f}" cy="{YR + rng.uniform(-28, 30):.0f}" rx="{rng.uniform(5, 11):.0f}" ry="{rng.uniform(3, 5):.0f}" fill="#c9a878" opacity="0.8"/>'
    for i in range(40):
        x = rng.uniform(-40, 2380)
        y = YR + (36 if i % 2 else -36) + rng.uniform(-4, 4)
        b += f'<path d="M{x - 8:.0f},{y:.0f} l5,-15 l5,12 l5,-17 l5,13" fill="none" stroke="#5f8a40" stroke-width="2.4"/>'
    return S.g(b, filter="wobble")


def sky_grad_svg(tt):
    cols = PR._sky_at(tt)
    gid = f"n4dn{int(round(tt * 100))}"
    defs = S.lin_grad(gid, [(0, cols[0]), (0.3, cols[1]), (0.55, cols[2]), (0.75, cols[3]), (1, cols[4])])
    return doc(f'<rect x="-60" y="-60" width="2232" height="1308" fill="url(#{gid})"/>', defs)


def stars_svg(k):
    rng = random.Random(77)
    b = ""
    for i in range(110):
        x, y = rng.uniform(-40, 2150), rng.uniform(-40, 760) ** 1.0
        r = rng.uniform(1.4, 3.4) * (0.75 + 0.5 * ((i + k) % 2))
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6d2"/>'
    for i in range(10):
        x, y = rng.uniform(0, 2112), rng.uniform(0, 600)
        r = 9 + 4 * ((i + k) % 2)
        b += f'<path d="M{x},{y - r} L{x + 2.6},{y - 2.6} L{x + r},{y} L{x + 2.6},{y + 2.6} L{x},{y + r} L{x - 2.6},{y + 2.6} L{x - r},{y} L{x - 2.6},{y - 2.6} Z" fill="#fff6d2"/>'
    return doc(b)


def sun_svg():
    defs = S.rad_grad("n4sg", [(0, "#fff6d2", 0.9), (0.4, "#ffe9a8", 0.45), (1, "#ffe9a8", 0)])
    return doc(f'<circle cx="1056" cy="300" r="190" fill="url(#n4sg)"/>' +
               S.g(f'<g transform="translate(1056,300)">{PR._sun_icon(58)}</g>', filter="wobble-fine"), defs)


def moon_svg():
    defs = S.rad_grad("n4mg", [(0, "#f6f0d8", 0.6), (1, "#f6f0d8", 0)])
    return doc(f'<circle cx="1056" cy="300" r="120" fill="url(#n4mg)"/>' +
               S.g(f'<g transform="translate(1056,300)">{PR._moon_icon(50)}</g>', filter="wobble-fine"), defs)


def road_extras_svg():
    """Foreground detail along the near road: grass tufts, flowers, a bush, stones."""
    rng = random.Random(31)
    b = ""
    for (x, y, s_, v) in ((60, 1120, 1.1, 0), (300, 1150, 0.9, 2), (980, 1130, 1.0, 1), (1300, 1100, 0.8, 0),
                          (1700, 1120, 1.0, 2), (2100, 1140, 0.9, 1), (760, 1060, 0.7, 2), (1500, 1020, 0.6, 0)):
        b += PR.grass_tuft(x, y, s_, variant=v)
    fl = ""
    for i in range(40):
        x = rng.uniform(-20, 2600)
        y = rng.uniform(1010, 1180)
        fl += anemone(x, y, rng.uniform(0.7, 1.1), rng.choice(("#d8463c", "#f2f0e2", "#f2c94e", "#c9a6e0")))
    b += S.g(fl, filter="wobble-fine")
    b += PR.bush(1800, 1000, 0.8, variant=1) + PR.bush(-20, 1040, 0.9, variant=3)
    st = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.55:.0f}" fill="#b4aa98" stroke="{INK}" stroke-width="3"/>'
                 for x, y, rx in ((1180, 1060, 46), (1240, 1072, 30), (2300, 1040, 40)))
    b += S.g(st, filter="wobble-fine")
    return doc(b)


def tint_fx(amount_fn, color_fn, y0=0.18, y1=0.55):
    """Multiply the land (below a soft line from y0 to y1 of the frame height) by a colour: night / dusk light."""
    from engine.paths import OUT_H
    yy = np.arange(OUT_H, dtype=np.float32)[:, None]
    mask = np.clip((yy / OUT_H - y0) / (y1 - y0), 0, 1)

    def fx(frame, t, view):
        a = float(amount_fn(t))
        if a <= 0.01:
            return frame
        col = np.array(color_fn(t), np.float32) / 255.0
        arr = np.asarray(frame, np.float32)
        k = (1 - a * mask)[..., None] + (a * mask)[..., None] * col[None, None, :]
        rgb = arr[..., :3] * k
        out = np.dstack([np.clip(rgb, 0, 255), arr[..., 3:]]).astype(np.uint8)
        return Image.fromarray(out, "RGBA")
    return fx


# ================================================================== the arrival at Bethlehem (dusk) - shared with s05
AK = 0.74                           # travellers' scale
AY = 962                            # their ground line
ARRIVAL_CAM = Cam(930, 640, 1720)   # the last frame of s04 = the first frame of s05
TOWN_Y = 770


def arrival_back_svg():
    return doc(PR.starry_sky(-40, -40, 2152, 900, density=0.55, twinkle=0.0, milky_way=False, time="dusk", seed=5))


def arrival_town_svg():
    return doc(PR.bethlehem_town(-20, 2132, TOWN_Y, 0.8, "dusk", "back", seed=3))


def arrival_near_svg():
    """The dusk fields below Bethlehem: the road winding up to the town gate, rocks, cypresses, grass."""
    defs = S.lin_grad("n4ag", [(0, "#8a8462"), (0.5, "#76724f"), (1, "#5f5c42")])
    b = ""
    gd = f"M-60,{HS + 40} L-60,820 Q500,780 1100,{TOWN_Y + 4} Q1700,780 2200,830 L2200,{HS + 40} Z"
    b += S.path(gd, fill="url(#n4ag)", sw=3.4)
    # the road: near band across, then up to the gate
    gx = -20 + 0.55 * 2152 - 40 * 0.8
    road = (f"M-60,{AY + 40} Q600,{AY + 30} 1000,{AY + 22} Q1220,{AY + 10} 1220,{AY - 80} Q1200,{TOWN_Y + 70} {gx + 22},{TOWN_Y - 26} "
            f"L{gx - 22},{TOWN_Y - 26} Q1100,{TOWN_Y + 80} 1110,{AY - 70} Q1080,{AY - 40} 900,{AY - 36} Q500,{AY - 36} -60,{AY - 40} Z")
    b += S.path(road, fill="#b9a27c", sw=3.4)
    rng = random.Random(11)
    peb = ""
    for i in range(30):
        x = rng.uniform(-40, 1150)
        peb += f'<ellipse cx="{x:.0f}" cy="{AY + rng.uniform(-30, 26):.0f}" rx="{rng.uniform(5, 10):.0f}" ry="4" fill="#9a8664" opacity="0.8"/>'
    b += peb
    b += S.g(cypress(1500, 860, 230, 40, col="#3f5a3a") + cypress(1545, 866, 180, 34, col="#3f5a3a") +
             cypress(380, 880, 200, 36, col="#3f5a3a"), filter="wobble-fine")
    b += olive(1850, 900, 0.7, 51, col="#7f8a68", dark="#646e50") + olive(150, 905, 0.55, 52, col="#7f8a68", dark="#646e50")
    st = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.55:.0f}" fill="#8a8274" stroke="{INK}" stroke-width="3"/>'
                 for x, y, rx in ((1380, 1080, 52), (1440, 1095, 34), (1960, 1060, 44), (640, 1110, 38)))
    b += S.g(st, filter="wobble-fine")
    for (x, y, s_, v) in ((80, 1130, 1.0, 0), (820, 1150, 0.9, 2), (1700, 1130, 1.0, 1), (2050, 1150, 0.9, 0)):
        b += PR.grass_tuft(x, y, s_, variant=v)
    # warm dusk light low on the land
    b += f'<ellipse cx="1100" cy="{TOWN_Y + 40}" rx="900" ry="120" fill="#f6c27a" opacity="0.16"/>'
    return doc(S.g(b, filter="wobble"), defs)


GATE = (-20 + 0.55 * 2152 - 40 * 0.8, TOWN_Y - 26)          # the town gate (bottom of the doorway) on the arrival page
FAR_A, FAR_B = (1208, 892), (GATE[0] + 4, GATE[1] + 6)      # the far road up to the gate
FAR_WALKERS = [("traveller", 1, 0.0), ("traveller_woman", 2, 60.0), ("traveller", 4, 118.0)]


def far_walker_frames(kind, v):
    s0 = 0.22
    return [doc(C.townsfolk(FAR_A[0], FAR_A[1], s0, -1, kind=kind, variant=v, pose=p_, item="bundle"))
            for p_ in ("carry_walk_a", "carry_walk_b")]


def add_arrival(sc, clock, gatef, z0=20.0, walk=None):
    """The dusk arrival page (stage x 0..2112). clock(t) -> this page's own time (s04: t; s05: t + s04 offset) so the
    two scenes show identical frames across their cross-dissolve; gatef(t) -> Tf(alpha). walk = dict of the travellers'
    motion functions (dpos, dphase, jpos, jframe, mframe). Returns the Travellers object."""
    def gm(m=None):
        return M.combine(gatef, m) if m else gatef
    sc.add("ar_sky", [arrival_back_svg()], z=z0, motion=gm(), wc=0.6, seed=4401)
    sc.add("ar_town", arrival_town_svg(), z=z0 + 0.1, motion=gm(), seed=4402)
    lights = doc("".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd36e" opacity="0.5"/>'
                         for x, y, r in ((900, 600, 30), (1060, 560, 34), (1250, 590, 30), (1130, 650, 26),
                                         (980, 680, 24), (1340, 660, 26), (1135, 730, 40))))
    sc.add("ar_lights", lights, z=z0 + 0.12, wc=0, blend="screen",
           motion=gm(lambda t: Tf(alpha=0.55 + 0.25 * math.sin(2 * math.pi * clock(t) / 1.7))))
    # tiny travellers walking up the road into the town gate (planted strides; they fade into the gateway)
    L_far = math.hypot(FAR_B[0] - FAR_A[0], FAR_B[1] - FAR_A[1])
    ux, uy = (FAR_B[0] - FAR_A[0]) / L_far, (FAR_B[1] - FAR_A[1]) / L_far
    per = 0.42
    for i, (kind, v, d0) in enumerate(FAR_WALKERS):
        def wdist(t, d0=d0, i=i):
            c = clock(t) - 30.0
            n = math.floor(c / per) if c > 0 else 0
            frac = M.progress(c - n * per, -0.06, 0.1, "sine") if c > 0 else 0.0
            return d0 + 0.22 * TOWN_STEP * 0.8 * (n + frac)

        def wmot(t, wdist=wdist):
            d = wdist(t)
            k = 1 - 0.3 * min(1.0, d / L_far)
            a = gatef(t).alpha * (1 - M.progress(d, L_far - 26, L_far, "sine"))
            return Tf(dx=ux * d, dy=uy * d, sx=k, sy=k, px=FAR_A[0], py=FAR_A[1], alpha=a)
        sc.add(f"ar_w{i}", far_walker_frames(kind, v), z=z0 + 0.18 + 0.01 * i, motion=wmot, seed=4404 + i,
               frame_at=lambda t, i=i: float(max(0, math.floor((clock(t) - 30.0) / per) + i) % 2))
    sc.add("ar_near", arrival_near_svg(), z=z0 + 0.15, motion=gm(), seed=4403)
    sc.fx.append(tint_fx(lambda t: 0.32 * gatef(t).alpha, lambda t: (206, 176, 214), y0=0.55, y1=0.78))
    return z0 + 0.5


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=WS, H=HS)
    T = ctx.duration
    B = Beats(ctx)
    L = ctx.lines

    t_mly = B.at(0, "马利亚的丈夫")
    t_ys = B.at(0, "名叫约瑟", 2)
    t_cutP = snap(B.at(0, "那时候") - 0.12)
    t_lm = B.at(0, "罗马皇帝想知道")
    t_count = B.at(0, "他的国家一共有多少人", 4)
    t_ren = B.at(0, "他的国家一共有多少人", 9)
    t_ml = B.at(1, "他下了一道命令", 5)
    t_l1 = L[1].start
    t_mei = B.at(1, "每个人都要回到自己的老家")
    t_laojia = B.at(1, "每个人都要回到自己的老家", 10)
    t_dj = B.at(1, "去登记名字", 1)
    t_cutM = snap(L[2].start - 0.25)
    t_beth1 = B.at(2, "约瑟的老家在伯利恒", 6)
    t_go = B.at(2, "约瑟和马利亚也要去伯利恒")
    t_beth2 = B.at(2, "约瑟和马利亚也要去伯利恒", 9)
    t_cutR = snap(L[3].start - 0.45)
    t_dada = B.at(3, "马利亚的肚子已经大大的了", 8)
    t_bb = B.at(3, "小宝宝")
    t_cs = B.at(3, "就快要出生了", 3)
    z_on = []
    for ent in B.marks[4]:
        for ch, tc in zip(ent[0], char_times(ent)):
            if ch == "走":
                z_on.append(tc)
    t_cutX = snap(L[4].end - 0.02)      # the whole line is on the road; Bethlehem at dusk after '好多天'

    # ================================================================ SHOT P: the village panorama (static base)
    sc.add("p_back", pano_back_svg(), z=0.0, wc=0.9)
    sc.add("p_clouds", doc(clouds_markup([(500, 210, 330, 96, 41), (1500, 140, 280, 86, 42), (2500, 230, 300, 90, 43),
                                          (3300, 300, 220, 70, 44)])), z=0.05, motion=M.drift(vx=8))
    for i, (col, y0, vx, ph, t0) in enumerate((("brown", 270, 95, 0.0, 0.0), ("blue", 330, 82, 0.4, 4.2))):
        def fly(t, y0=y0, vx=vx, ph=ph, t0=t0, i=i):
            x = (300 if i == 0 else 1900) + vx * (t - t0)
            return Tf(dx=x - 200, dy=y0 - 200 + 22 * math.sin(2 * math.pi * (t / 2.1 + ph)),
                      alpha=1.0 if t < t_cutM else 0.0)
        sc.add(f"p_bird{i}", flyer_frames(col), z=0.06 + 0.01 * i, motion=fly, wc=0.3,
               frame_at=lambda t, ph=ph: float(int(t / 0.07 + ph * 8) % 8))
    sc.add("p_near", pano_near_svg(), z=0.1, wc=0.9)
    sc.add("p_banner", [banner_svg(s_) for s_ in (-1, 0, 1)], z=0.12, seed=4101,
           frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.4) % 4]))

    # ---- P1: Mary and Joseph by the house
    MXH, JXH = 1110, 1330
    gP1 = gate(-1, t_cutP)
    mfrP = [S.svg_doc(C.ground_shadow(MXH, GY, 1.0, 110, 0.18) + C.mary(MXH, GY, 1.0, 1, pose="stand", expr=e), "", WS, HS)
            for e in ("kind", blink("kind"), "happy")]
    t_mly_c = snap(t_mly + 0.1)
    sc.add("p1_mary", mfrP, z=1.0, seed=4110,
           frame_at=cuts(blinks_for([(0, 0), (t_mly_c, 2)], [1.6, 3.2], {0: 1, 2: 1})),
           motion=M.combine(gP1, dipm(t_mly_c, 1.0, (MXH, GY), 6), breathm((MXH, GY), 2.8, 0.01)))
    jfrP = [S.svg_doc(joseph(JXH, GY, 1.0, -1, "stand", "kind"), "", WS, HS),
            S.svg_doc(joseph(JXH, GY, 1.0, -1, "stand", blink("kind")), "", WS, HS),
            S.svg_doc(C.ground_shadow(JXH, GY, 1.0, 120, 0.18) + joseph_wave(JXH, GY, 1.0, -1, 0), "", WS, HS),
            S.svg_doc(C.ground_shadow(JXH, GY, 1.0, 120, 0.18) + joseph_wave(JXH, GY, 1.0, -1, 1), "", WS, HS)]
    t_wave = snap(t_ys - 0.05)
    jb = cuts(blinks_for([(0, 0)], [0.9, 2.0], {0: 1}))

    def jP_fa(t):
        if t >= t_wave:
            return 2.0 + float(int((t - t_wave) / 0.2) % 2)
        return jb(t)
    sc.add("p1_joseph", jfrP, z=1.01, seed=4111, frame_at=jP_fa,
           motion=M.combine(gP1, dipm(t_wave, 1.0, (JXH, GY), 6), breathm((JXH, GY), 3.1, 0.01, 0.3)))
    # the donkey nibbling by the timber pile
    DXH = 1760
    dfrH = [S.svg_doc(C.ground_shadow(DXH, GY - 6, 0.9, 240, 0.16) + PR.donkey(DXH, GY - 6, 0.9, -1, pose=p_, sacks=0), "", WS, HS)
            for p_ in ("stand",)]
    dfrH.append(S.svg_doc(C.ground_shadow(DXH, GY - 6, 0.9, 240, 0.16) +
                          PR.donkey(DXH, GY - 6, 0.9, -1, pose="look", eyes="happy", sacks=0), "", WS, HS))
    sc.add("p1_donkey", dfrH, z=0.9, seed=4112, frame_at=cuts([(0, 1), (snap(1.3), 0), (snap(2.6), 1)]),
           motion=M.combine(gP1, dipm(snap(1.3), 0.9, (DXH, GY), 4), dipm(snap(2.6), 0.9, (DXH, GY), 4)))
    for i, (hx, hy, f, col) in enumerate(((560, 960, 1, "#f4ead8"), (680, 975, -1, "#c9874a"))):
        fr = [S.svg_doc(C.ground_shadow(hx, hy, 0.95, 70, 0.15) + hen_svg(hx, hy, 0.95, f, pk, col), "", WS, HS)
              for pk in (False, True)]
        pk_ = [(0, 0)] + sum(([(snap(0.4 + 1.3 * j + 0.5 * i), 1), (snap(0.62 + 1.3 * j + 0.5 * i), 0)] for j in range(3)), [])
        sc.add(f"p1_hen{i}", fr, z=1.05 + 0.01 * i, frame_at=cuts(pk_), motion=gP1, seed=4113 + i)
    # name tags
    tag_m = S.svg_doc(name_tag(MXH, GY - 335, "马利亚"), "", WS, HS)
    tag_j = S.svg_doc(name_tag(JXH, GY - 395, "约瑟", col="#8a4a2a"), "", WS, HS)
    sc.add("p1_tagm", tag_m, z=1.2, wc=0, motion=popm(snap(t_mly - 0.05), (MXH, GY - 340), t_out=t_cutP, out_dur=0.01))
    sc.add("p1_tagj", tag_j, z=1.2, wc=0, motion=popm(snap(t_ys + 0.05), (JXH, GY - 400), t_out=t_cutP, out_dur=0.01))

    # ---- P2: the square
    gP2 = gate(t_cutP, t_cutM)
    HXR, HYR = PLAT[0], PLAT[1] - 18
    hfr = [S.svg_doc(townie(HXR, HYR, 1.0, 1, "herald", 0, "read", shadow=False), "", WS, HS),
           S.svg_doc(townie(HXR, HYR, 1.0, 1, "herald", 0, "announce", shadow=False), "", WS, HS),
           S.svg_doc(townie(HXR, HYR, 1.0, -1, "herald", 0, "announce", shadow=False), "", WS, HS),
           S.svg_doc(townie(HXR, HYR, 1.0, 1, "herald", 0, "read", expr="happy", shadow=False), "", WS, HS)]
    t_h1 = snap(t_ml - 0.2)
    t_h2 = snap(t_mei + 0.6)
    t_h3 = snap(t_dj - 0.1)
    sc.add("p2_herald", hfr, z=1.887, seed=4120, frame_at=cuts([(0, 0), (t_h1, 1), (t_h2, 2), (t_h3, 3)]),
           motion=M.combine(gP2, *[dipm(tc, 1.0, (HXR, HYR), 6) for tc in (t_h1, t_h2, t_h3)],
                            breathm((HXR, HYR), 2.7, 0.01)))
    # the emperor's portrait
    t_emp = snap(t_lm + 0.05)
    sc.add("p2_emperor", emperor_svg(3130, 400), z=2.6, wc=0.5,
           motion=M.combine(gP2, popm(t_emp, (3130, 400), t_out=snap(t_l1 - 0.2))))
    # listeners: (x, y, kind, variant, facing, item, leave direction)
    LIS = [(2040, 950, "man", 1, 1, "sack", -1), (2150, 985, "woman", 0, 1, "jar", -1), (2250, 1010, "child", 0, 1, None, -1),
           (2420, 990, "traveller", 2, 1, "bundle", -1), (2520, 955, "elder", 1, 1, None, -1),
           (2930, 1000, "woman", 3, -1, "basket", 1), (3040, 965, "man", 4, -1, "bundle", 1), (2990, 1060, "child", 1, -1, None, 1)]
    JX2, MX2 = 3380, 3250
    count_heads = []
    for i, (x, y, kind, v, f, item, d) in enumerate(LIS):
        s_ = 1.0
        lead_t = snap(t_mei + 0.1 + 0.14 * (i % 5))
        n_steps = 9
        per = 0.38
        steps = [snap(lead_t + 0.3 + per * j) for j in range(n_steps)]
        st = {"child": 50, "woman": 81, "traveller_woman": 81}.get(kind, TOWN_STEP) * s_   # planted-ankle stride
        dxs, dys, ns = stepper(steps, st, s_, lift=5)
        child = kind in ("child",)
        elder = kind == "elder"
        stand_pose = "listen" if i % 3 == 0 else "stand"
        if child:
            wa, wb, it = "walk_a", "walk_b", None
        elif elder:
            wa, wb, it = "walk_a", "walk_b", None
        else:
            wa, wb, it = "carry_walk_a", "carry_walk_b", item
        fr = [S.svg_doc(townie(x, y, s_, f, kind, v, stand_pose), "", WS, HS),
              S.svg_doc(townie(x, y, s_, f, kind, v, stand_pose, expr=blink("happy")), "", WS, HS),
              S.svg_doc(townie(x, y, s_, d, kind, v, "carry" if it else "stand", item=it), "", WS, HS),
              S.svg_doc(townie(x, y, s_, d, kind, v, wa, item=it), "", WS, HS),
              S.svg_doc(townie(x, y, s_, d, kind, v, wb, item=it), "", WS, HS)]

        def fa(t, lead_t=lead_t, steps=steps, ns=ns, i=i):
            if t < lead_t:
                tb = 1.2 + 1.7 * i % 4
                return 1.0 if any(abs(t - (tb + 3.1 * k_)) < 0.065 for k_ in range(4)) else 0.0
            if t < steps[0]:
                return 2.0
            return 3.0 + float((ns(t) - 1) % 2)
        piv = lambda t, x=x, y=y, dxs=dxs: (x + d * dxs(t), y)      # noqa: E731
        sc.add(f"p2_t{i}", fr, z=1.0 + y / 1000, seed=4130 + i, frame_at=fa,
               motion=M.combine(gP2, lambda t, d=d, dxs=dxs, dys=dys: Tf(dx=d * dxs(t), dy=dys(t)),
                                dipm(lead_t, s_, piv, 6), breathm(piv, 2.6 + 0.1 * i, 0.01, 0.17 * i)))
        top = C.body_points(C.townsfolk, x, y, s_, f, kind=kind, variant=v, pose=stand_pose)["bbox"][1]
        count_heads.append((x, top - 50))
    # Mary and Joseph in the square
    t_look = snap(t_laojia - 0.05)
    mfr2 = [S.svg_doc(C.ground_shadow(MX2, 975, 1.0, 110, 0.18) + C.mary(MX2, 975, 1.0, -1, pose="stand", expr=e), "", WS, HS)
            for e in ("kind", blink("kind"))]
    mfr2.append(S.svg_doc(C.ground_shadow(MX2, 975, 1.0, 110, 0.18) + C.mary(MX2, 975, 1.0, 1, pose="listen_think"), "", WS, HS))
    sc.add("p2_mary", mfr2, z=1.975, seed=4140, frame_at=cuts(blinks_for([(0, 0), (t_look, 2)], [t_cutP + 1.4, t_ml + 0.6],
                                                                     {0: 1})),
           motion=M.combine(gP2, dipm(t_look, 1.0, (MX2, 975), 6), breathm((MX2, 975), 2.8, 0.01)))
    jfr2 = [S.svg_doc(joseph(JX2, 980, 1.0, -1, "stand", "kind"), "", WS, HS),
            S.svg_doc(joseph(JX2, 980, 1.0, -1, "stand", blink("kind")), "", WS, HS),
            S.svg_doc(joseph(JX2, 980, 1.0, -1, "talk", "kind"), "", WS, HS)]
    sc.add("p2_joseph", jfr2, z=1.98, seed=4141,
           frame_at=cuts(blinks_for([(0, 0), (snap(t_look + 0.2), 2)], [t_cutP + 2.2, t_ml + 1.0], {0: 1})),
           motion=M.combine(gP2, dipm(snap(t_look + 0.2), 1.0, (JX2, 980), 6), breathm((JX2, 980), 3.0, 0.01, 0.4)))
    for who, (x, y) in (("m", (MX2, 975)), ("j", (JX2, 980))):
        count_heads.append((x, y - (370 if who == "m" else 410)))
    # counting: numbers pop over the heads
    n_c = len(count_heads)
    c0, c1 = t_count - 0.1, t_ren + 0.25
    t_clear = snap(t_ml - 0.35)
    for i, (x, y) in enumerate(count_heads):
        tp = snap(c0 + (c1 - c0) * i / (n_c - 1))
        sc.add(f"p2_n{i}", S.svg_doc(number_badge(x, y, i + 1), "", WS, HS), z=2.7 + 0.01 * i, wc=0,
               motion=M.combine(gP2, popm(tp, (x, y), t_out=t_clear + 0.03 * i)))
        sc.sfx("pop", tp, gain_db=-17, pan=(x - 2700) / 1200)
    # the list of names
    LX, LYc = 2980, 470
    lst = (f'<path d="M{LX - 230},{LYc - 130} L{LX + 230},{LYc - 130} Q{LX + 244},{LYc} {LX + 230},{LYc + 130} L{LX - 230},{LYc + 130} '
           f'Q{LX - 216},{LYc} {LX - 230},{LYc - 130} Z" fill="#f2e2bc" stroke="{INK}" stroke-width="4"/>')
    for sx in (-1, 1):
        lst += f'<rect x="{LX + sx * 240 - 16}" y="{LYc - 146}" width="32" height="292" rx="14" fill="#e2cb98" stroke="{INK}" stroke-width="4"/>'
    lst_svg = S.svg_doc(S.g(lst, filter="wobble-fine"), "", WS, HS)
    t_list = snap(t_dj - 0.15)
    sc.add("p2_list", lst_svg, z=2.8, wc=0.4, motion=M.combine(gP2, popm(t_list, (LX, LYc), wob=False)))
    names = [("约瑟", LYc - 30, "#8a4a2a"), ("马利亚", LYc + 70, "#3f62a2")]
    for j, (nm, yy, col) in enumerate(names):
        tw = (f'<text x="{LX}" y="{yy}" font-family="LXGW WenKai" font-weight="bold" font-size="76" fill="{col}" '
              f'text-anchor="middle">{nm}</text>')
        t0 = snap(t_list + 0.35 + 0.55 * j)
        sc.add(f"p2_name{j}", S.svg_doc(tw, "", WS, HS), z=2.81 + 0.01 * j, wc=0,
               motion=M.combine(gP2, lambda t, t0=t0: Tf(alpha=1.0 if t >= t0 else 0.0)),
               reveal=lambda t, t0=t0: {"mode": "left", "frac": M.progress(t, t0, t0 + 0.5, "linear"), "soft": 30})
        sc.sfx("sparkle" if j else "cloth", t0, gain_db=-16 if j else -18)

    # ================================================================ SHOT M: the map
    gM = gate(t_cutM, t_cutR)
    t_un0 = snap(t_cutM + 0.15)
    t_un1 = t_un0 + 0.75
    sc.add("m_table", table_svg(), z=10.0, motion=gM, wc=0.8, seed=4201)
    unroll = lambda t: M.progress(t, t_un0, t_un1, "out")       # noqa: E731
    for half in (-1, 1):
        sc.add(f"m_map{half}", map_svg(half), z=10.1, seed=4202, motion=gM, wc_edge=0.0,
               reveal=lambda t, half=half: {"mode": "right" if half < 0 else "left", "frac": max(0.0, unroll(t)), "soft": 12})
    for side in (-1, 1):
        sc.add(f"m_roll{side}", rolls_svg(side), z=10.15, seed=4203 + side,
               motion=M.combine(gM, lambda t, side=side: Tf(dx=side * (756 + 30) * unroll(t) + side * 28)))
    t_bm = snap(t_beth1 - 0.05)
    sc.add("m_beth", beth_marker_svg(), z=10.2, wc=0.5,
           motion=M.combine(gM, popm(t_bm, (BETH[0] + 60, BETH[1]), wob=False)))
    t_p0 = snap(t_go + 0.05)
    t_p1 = snap(t_beth2 + 0.05)
    hops = 7
    hop_t = [t_p0 + (t_p1 - t_p0) * j / hops for j in range(hops + 1)]

    def tok_u(t):
        if t <= hop_t[0]:
            return 0.0
        for j in range(hops):
            if hop_t[j] <= t < hop_t[j + 1]:
                return (j + M.progress(t, hop_t[j], hop_t[j] + (hop_t[j + 1] - hop_t[j]) * 0.8, "inout")) / hops
        return 1.0

    def tok_mot(t):
        u = tok_u(t)
        x, y = bez(u)
        lift = 0.0
        for j in range(hops):
            h0, h1 = hop_t[j], hop_t[j] + (hop_t[j + 1] - hop_t[j]) * 0.8
            if h0 <= t < h1:
                lift = -26 * math.sin(math.pi * (t - h0) / (h1 - h0))
        return Tf(dx=x - PATH[0][0], dy=y - PATH[0][1] + lift, alpha=M.progress(t, t_un1 - 0.2, t_un1 + 0.1))
    sc.add("m_path", path_svg(), z=10.18, wc=0,
           motion=gM, reveal=lambda t: {"mode": "down", "frac": 0.0 if t < t_p0 else
                                        max(0.0, min(1.0, (bez(min(1.0, tok_u(t) + 0.12))[1] - 300) / 470)), "soft": 20})
    sc.add("m_token", token_svg(), z=10.3, seed=4210, motion=M.combine(gM, tok_mot))
    sc.fx.append(lambda frame, t, view, f=FX.sparkles((BETH[0] - 80, BETH[1] - 110, BETH[0] + 80, BETH[1] + 10), count=8,
                                                      t0=t_p1, t1=t_cutR, color=(255, 236, 170), size=(8, 16), period=1.2,
                                                      drift=-8, seed=42): f(frame, t, view) if t < t_cutR else frame)
    for j in range(hops):
        sc.sfx("pop", hop_t[j] + 0.05, gain_db=-22)

    # ================================================================ SHOT R: the road
    gR = gate(t_cutR, t_cutX)
    t_walk = snap(z_on[0] - 0.02) if z_on else snap(L[4].start + 0.3)
    jsteps = [snap(t_walk + 0.48 * j) for j in range(6)]
    if len(z_on) >= 5:          # a planted stride on every '走' but the quick second one, plus the strides between
        jsteps = [snap(z_on[0]), snap(z_on[0] + 0.44), snap(z_on[2]), snap(z_on[3]), snap(z_on[4]), snap(z_on[4] + 0.48)]
    jsteps = [tj for tj in jsteps if tj < t_cutX - 0.12]
    D0 = 660.0                                     # the donkey's x at the start
    stepd = JOSEPH_STEP * KR
    dist_total = stepd * len(jsteps)
    v_d = dist_total / max(0.5, (t_cutX - t_walk)) if jsteps else 0.0
    jdx, jdy, jn = stepper(jsteps, stepd, KR, lift=5)
    lead_off = (PR.DONKEY_LEAD[0] - C.JOSEPH_LEAD_HAND[0]) * KR
    ACC = 0.35

    def dist_d(t):
        u = t - t_walk
        if u <= 0:
            return D0
        if u < ACC:
            return D0 + v_d * u * u / (2 * ACC)
        return D0 + v_d * ACC / 2 + v_d * (u - ACC)

    def dposR(t):
        return road_at(dist_d(t))

    def jposR(t):
        x, y, k = road_at(D0 + lead_off + jdx(t))
        return x, y + jdy(t), k

    def dphaseR(t):
        if t < t_walk:
            return None
        return ((dist_d(t) - D0) / (DONKEY_CYCLE * KR)) % 1.0

    jkeys = [("stand", -1, "tender"), ("stand", -1, blink("tender")), ("stand", -1, "joyful"),
             ("lead_a", 1, "kind"), ("lead_b", 1, "kind")]
    mkeys = ["tender", blink("tender"), "joyful", "kind", blink("kind")]
    t_turn = snap(t_walk - 0.0)
    t_joy = snap(t_bb + 0.05)

    def jframeR(t):
        if t >= t_turn:
            return 3 + (jn(t) + 1) % 2
        if t >= t_joy:
            return 2
        return 1 if any(abs(t - tb) < 0.065 for tb in (t_cutR + 1.5, t_cutR + 3.8)) else 0

    def mframeR(t):
        if t >= t_turn:
            return 4 if any(abs(t - tb) < 0.065 for tb in (t_turn + 0.9,)) else 3
        if t >= t_joy:
            return 2
        return 1 if any(abs(t - tb) < 0.065 for tb in (t_cutR + 2.6, t_dada + 0.9)) else 0
    x0r, y0r, _ = road_at(D0)
    trav = Travellers(sc, "r", KR, x0r, y0r, jkeys, mkeys, z=11.0, gatef=gR, seed=4300)
    jpivR = lambda t: jposR(t)[:2]                          # noqa: E731
    mpivR = lambda t: trav.seat                              # noqa: E731
    trav.add(dposR, dphaseR, jposR, jframeR, mframeR,
             jextra=M.combine(dipm(t_turn, KR, jpivR, 7), dipm(t_joy, KR, jpivR, 5)),
             mextra=M.combine(dipm(t_joy, KR, mpivR, 5), dipm(t_turn, KR, mpivR, 4)))

    # sky (pinned to the screen), sun, moon, stars, land
    # days passing: from the morning of line 4 the sky turns steadily through two nights and lands on the third
    # evening (dusk) at the cut to Bethlehem at dusk; a soft start, then one even pace (~1.85 s per day)
    t_s0 = snap(t_cs + 0.2)
    SKY0, SKY1, SOFT = 0.16, 2.5, 0.12

    def sky_t(t):
        if t <= t_s0:
            return SKY0
        u = min(1.0, (t - t_s0) / (t_cutX - t_s0))
        g_ = u * u / (2 * SOFT) if u < SOFT else u - SOFT / 2
        return SKY0 + (SKY1 - SKY0) * g_ / (1 - SOFT / 2)
    NSK = 12
    sc.add("r_sky", [sky_grad_svg(k / NSK) for k in range(NSK + 1)], z=10.5, wc=0.5, seed=4301,
           frame_at=lambda t: (sky_t(t) % 1.0) * NSK,
           motion=lambda t: pin(t, gR))

    def pin(t, g_, extra=None):
        c = camR(t)
        s_ = c.w / REF.w
        a = g_(t).alpha
        tf = Tf(dx=c.x - REF.x, dy=c.y - REF.y, sx=s_, sy=s_, px=REF.x, py=REF.y, alpha=a)
        return tf

    def arc_pos(u, R=440, rise=440, hz=700):
        a = math.pi * (1 - u)
        return 1056 + R * math.cos(a), hz - rise * math.sin(a)

    def night(t):
        tt = sky_t(t) % 1.0
        return max(0.0, 1 - abs(tt - 0.75) / 0.25) if 0.5 < tt < 1.0 else 0.0

    def body_mot(kind):
        def m(t):
            tt = sky_t(t) % 1.0
            if kind == "sun":
                vis = tt <= 0.5
                u = tt / 0.5
            else:
                vis = tt > 0.5
                u = (tt - 0.5) / 0.5
            x, y = arc_pos(u)
            c = camR(t)
            s_ = c.w / REF.w
            a = gR(t).alpha * (1.0 if vis else 0.0)
            # sun/moon live in REF screen space: (x, y) relative to REF, then pinned to the camera
            return Tf(dx=c.x - REF.x + (x - 1056) * s_, dy=c.y - REF.y + (y - 300) * s_ + (300 - REF.y) * (s_ - 1),
                      sx=s_, sy=s_, px=1056, py=300, alpha=a)
        return m
    sc.add("r_stars", [stars_svg(k) for k in range(2)], z=10.55, wc=0, seed=4302,
           frame_at=lambda t: float(int(t / 0.3) % 2),
           motion=lambda t: Tf(**{**pin(t, gR).__dict__, "alpha": gR(t).alpha * night(t)}))
    sc.add("r_sun", sun_svg(), z=10.6, wc=0.3, seed=4303, motion=body_mot("sun"))
    sc.add("r_moon", moon_svg(), z=10.61, wc=0.3, seed=4304, motion=body_mot("moon"))
    sc.add("r_land", doc(PR.journey_road(RX0, RX1, RY, 1.0, "day", seed=3) + near_path_markup()), z=10.7, motion=gR,
           seed=4305)
    sc.add("r_extras", road_extras_svg(), z=11.5, motion=gR, seed=4306)

    def tint_amt(t):
        if not (t_cutR <= t < t_cutX):
            return 0.0
        tt = sky_t(t) % 1.0
        n = night(t)
        warm = max(0.0, 1 - abs(tt - 0.5) / 0.08) + max(0.0, 1 - min(abs(tt - 1.0), abs(tt)) / 0.07)
        return min(1.0, 0.78 * n + 0.32 * warm)

    def tint_col(t):
        n = night(t)
        warm = (255, 196, 170)
        nite = (64, 76, 146)
        u = min(1.0, n * 1.5)
        return tuple(warm[i] + (nite[i] - warm[i]) * u for i in range(3))
    sc.fx.append(tint_fx(tint_amt, tint_col))
    # heart over Mary's belly on '小宝宝', twinkles on '出生了'
    hx_, hy_ = trav.seat[0] + 112 * KR, trav.seat[1] - 120 * KR
    t_heart = snap(t_bb - 0.02)
    sc.add("r_heart", S.svg_doc(heart_markup(hx_, hy_, 30), "", WS, HS), z=11.6, wc=0,
           motion=M.combine(gR, popm(t_heart, (hx_, hy_), t_out=snap(t_walk - 0.3)),
                            lambda t: Tf(dy=-18 * M.progress(t, t_heart, t_heart + 2.5, "sine"))))
    sc.fx.append(lambda frame, t, view, f=FX.sparkles((hx_ - 120, hy_ - 120, hx_ + 120, hy_ + 60), count=9, t0=snap(t_cs - 0.1),
                                                      t1=snap(t_walk - 0.2), color=(255, 226, 190), size=(7, 14),
                                                      period=1.3, drift=-10, seed=44):
                  f(frame, t, view) if t_cutR <= t < t_cutX else frame)

    # ================================================================ SHOT X: arrival at dusk
    gX = gate(t_cutX, 1e9)
    zt = add_arrival(sc, lambda t: t, gX, z0=20.0)
    # they have arrived: the page holds still (s05 starts on exactly this frame and walks them on to the gate)
    DX_END = 640.0                                   # the donkey's anchor x
    lead_x = (PR.DONKEY_LEAD[0] - C.JOSEPH_LEAD_HAND[0]) * AK
    xj = [("lead_a", 1, "kind"), ("lead_b", 1, "kind"), ("stand", 1, "kind"), ("stand", 1, blink("kind"))]
    xm = ["weary", "kind", blink("kind")]
    travX = Travellers(sc, "x", AK, DX_END, AY, xj, xm, z=zt, gatef=gX, seed=4400)
    travX.add(lambda t: (DX_END, AY, 1.0), lambda t: None, lambda t: (DX_END + lead_x, AY, 1.0), lambda t: 2,
              lambda t: 1)

    # ================================================================ camera
    camP1 = Cam(1150, 650, 1640)
    camP2 = M.cam_keys([(t_cutP, Cam(2760, 640, 1800)), (t_count - 1.3, Cam(2760, 640, 1800)),
                        (t_count + 0.8, Cam(2790, 650, 1720)), (t_mei - 0.3, Cam(2790, 650, 1720)),
                        (t_mei + 1.8, Cam(2760, 640, 1800)), (t_cutM, Cam(2800, 620, 1780))], "sine")
    camM = M.cam_keys([(t_cutM, Cam(1056, 560, 2050)), (t_cutR, Cam(1040, 570, 1960))], "sine")
    xg, yg, _ = road_at(D0)
    t_pb0 = snap(L[3].end - 0.1)               # one slow 4 s pull-back + pan over the whole walking line
    camR = M.cam_keys([(t_cutR, Cam(xg + 120, 790, 1300)), (t_dada, Cam(xg + 60, 780, 1180)),
                       (t_pb0, Cam(xg + 60, 780, 1180)), (t_cutX, Cam(xg + 430, 700, 1720))], "sine")
    camR_c = camR
    camR = lambda t: clamp_cam(camR_c(t))                     # noqa: E731
    camX = lambda t: ARRIVAL_CAM                                # noqa: E731

    def cam(t):
        if t < t_cutP:
            return clamp_cam(camP1)
        if t < t_cutM:
            return clamp_cam(camP2(t))
        if t < t_cutR:
            return clamp_cam(camM(t))
        if t < t_cutX:
            return camR(t)
        return clamp_cam(camX(t), 0, 2112)
    sc.camera = cam

    # ================================================================ sound
    sc.sfx("birds", 0, dur=t_cutM + 0.3, gain_db=-18, fade_in=1.0, fade_out=0.4)
    sc.sfx("pop", t_mly - 0.05, gain_db=-14)
    sc.sfx("pop", t_ys + 0.05, gain_db=-14)
    sc.sfx("crowd", t_cutP, dur=t_cutM - t_cutP + 0.2, gain_db=-24, fade_in=0.3, fade_out=0.4)
    sc.sfx("chime", t_emp, gain_db=-15)
    sc.sfx("horn", t_h1 - 0.1, gain_db=-12)
    sc.sfx("footsteps", t_mei + 0.4, dur=3.4, gain_db=-17, fade_in=0.2, fade_out=0.6)
    sc.sfx("cloth", t_un0, gain_db=-11)
    sc.sfx("pop", t_bm, gain_db=-13)
    sc.sfx("sparkle", t_p1, gain_db=-14)
    sc.sfx("wind_soft", t_cutR, dur=t_cutX - t_cutR + 0.2, gain_db=-22, fade_in=0.3, fade_out=0.2)
    sc.sfx("birds", t_cutR, dur=t_walk - t_cutR + 0.4, gain_db=-22, fade_in=0.4, fade_out=0.6)
    sc.sfx("sparkle", t_heart, gain_db=-14)
    sc.sfx("footsteps", t_walk, dur=t_cutX - t_walk + 0.1, gain_db=-17, fade_in=0.2, fade_out=0.3)
    def when(v):                                   # first time sky_t reaches v
        lo, hi = t_s0, t_cutX
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if sky_t(mid) < v else (lo, mid)
        return hi
    for n in (0, 1):
        sc.sfx("night", when(n + 0.56), dur=when(n + 0.95) - when(n + 0.56), gain_db=-21, fade_in=0.25, fade_out=0.3)
        sc.sfx("rooster", when(n + 1.0) - 0.05, gain_db=-21, pan=-0.3 + 0.6 * n)
    sc.sfx("night", t_cutX, dur=T - t_cutX + 0.3, gain_db=-24, fade_in=0.4, fade_out=0.6)
    sc.sfx("wind_soft", t_cutX, dur=T - t_cutX + 0.3, gain_db=-26, fade_in=0.4, fade_out=0.6)
    return sc
