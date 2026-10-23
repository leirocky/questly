"""Scene 2 - the opening question to the child. A cosy bedroom at night: the little girl in her star pyjamas stands on
the rug hugging her star pillow, looking at the window; outside the wind blows - clouds race past the moon, a tree
branch thrashes, leaves fly; the curtains billow into the room and the window rattles. Then she turns to the picture on
her wall - a little fishing boat on an evening lake - and we fly into it: the story's lake, where the waves grow big.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers; nothing is
hard-coded to the take):
  0 .. 1.0     s01's title page, continued exactly (title_page(..., toff)): the plain cross-dissolve between the two
               scenes blends identical pictures; the title lettering then fades
  '小朋友'      a round page-iris opens on the bedroom: the girl hugging her pillow, the curtains stirring
  '很大很大'    two little swells of wind on the two '大': the curtains lift, the branch bends
  '风呼呼地吹'  a gust on each '呼' (whoosh): the curtains billow high into the room, the branch thrashes, leaves fly,
               the clouds race; she leans back, surprised (pose cut hidden by a squash dip)
  '窗户哐哐地响' two shake beats of the window frame on the two '哐' (rattle ticks, wooden knocks); she flinches with a
               little hop on each, scared
  '你会不会害怕' she hugs the pillow tight; on '害怕' she peeks at the window, curious (cut in a dip); pause: she peeks
  line 1       '今天的故事里' she turns round to the picture on the wall (hop cut), the camera glides toward it and
               the picture lights up and comes alive (chime); we zoom into it: '有一群人在船上' a little fishing boat
               on the violet-gold evening lake, Jesus asleep at the stern, his friends around him; '好大好大的风浪'
               on the first '好大' the sky turns stormy and the waves rise (splash on '大'), on the second '好大' they
               grow bigger still (big splash over the bow); the sail flaps, the friends hold on - big, but friendly
  end          the boat riding the big waves, rocking (page dip to s03)

Shared with s15_end: the room (room_svg, outside_svg, branch_svg, window_frames, bed_markup, frame geometry), the
wind helpers and the picture-in-the-frame machinery (frame_tf, ZOOM_P, GK0).
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.storm.scenes import s01_title as T1
from stories.storm.scenes.s01_title import (blink, boxed, char_times, compose, cuts, dip, evening_water, f1,
                                            iris_reveal, snap, ugrad, voice_marks, water_ripples, zoom_about)

INK = P["ink"]

# ---- the room (stage px)
BASE_Y = 880                         # wall / floor line
KID = (1250, 1020, 1.65)             # the girl (x, ground y, scale); bed and child share the scale
BED = (560, 992)
WIN = (1690, 700, 1.08)              # window_wind anchor (middle of the sill top) and scale
OPEN = (WIN[0] - 200 * WIN[2], WIN[1] - 460 * WIN[2], WIN[0] + 200 * WIN[2], WIN[1])   # glass opening
GK0 = 0.28                           # the picture on the wall = the full-stage picture scaled by GK0
FX0, FY0 = 405.0, 196.0              # its top-left corner on the wall
FRW, FRH = W * GK0, H * GK0
ZOOM_P = (FX0 / (1 - GK0), FY0 / (1 - GK0))    # scaling the picture about this point keeps (0,0) at (FX0, FY0)
NAIL = (FX0 + FRW / 2, FY0 - 52)
IRIS_C = (1350, 640)
WIND_LV = (0.22, 0.38, 0.54, 0.70, 0.85, 1.0)
WPH = 8                              # curtain / wind phases
WALL_TOP = ("#525b8c", "#606a98")

# ---- the picture (full-stage coordinates; shown at GK0 on the wall, then full screen)
G_HZ = 700                           # far shore of the evening lake
G_LAKE_S = 0.6
GB = (1090, 962, 0.52)               # the boat: waterline anchor, scale
G_LAKE_K = 0.9                       # storm_lake scale (bigger waves than the boat's scale: '好大好大的风浪')
G_LEVEL = GB[1] - 46 * G_LAKE_K     # storm_lake far edge: the hull rides a little higher than STORM_BOAT_DY puts it
G_SUN = 0.2
LPH = 12                             # storm_lake phases (0.075 s each)

C.EXPRS.setdefault("sw_look", dict(C.EXPRS["worried"], look=(0.05, -0.05)))
C.EXPRS.setdefault("sw_curious", dict(eyes="dot", brow=(-0.06, 0.0, -0.11), mouth="small_o", look=(0.07, -0.03)))
C.EXPRS.setdefault("sw_wonder", dict(eyes="dot", brow=(-0.06, 0.01, -0.10), mouth="smile", look=(0.05, -0.10),
                                     blush=True))
for _e in ("sw_look", "sw_curious", "sw_wonder", "surprised", "scared", "smile", "happy", "peaceful", "awed"):
    C.EXPRS.setdefault(f"st_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


# ================================================================== the room

def _star4(x, y, r, col, op):
    return (f'<path d="M{f1(x)},{f1(y - r)} Q{f1(x + r * 0.15)},{f1(y - r * 0.15)} {f1(x + r)},{f1(y)} '
            f'Q{f1(x + r * 0.15)},{f1(y + r * 0.15)} {f1(x)},{f1(y + r)} Q{f1(x - r * 0.15)},{f1(y + r * 0.15)} '
            f'{f1(x - r)},{f1(y)} Q{f1(x - r * 0.15)},{f1(y - r * 0.15)} {f1(x)},{f1(y - r)} Z" fill="{col}" '
            f'opacity="{op}"/>')


def bed_markup(x, y, s, quilt="#7f9fd4", wood="#c19466"):
    """The child's wooden bed (headboard with a moon cut-out on the left), a plain cream pillow, a patchwork
    quilt; the girl's star pillow is hers to hold. Mattress top at y + PR.BED_TOP * s."""
    out = PR._rect(-290, -330, 46, 330, wood, 4, rx=10)
    out += PR._p("M-300,-330 Q-267,-372 -234,-330 Z", wood, 4)
    out += PR._p("M-280,-270 a16,16 0 1,0 22,-14 a12,12 0 1,1 -22,14 Z", "#f4d77a", 2.6)
    out += PR._rect(250, -210, 40, 210, wood, 4, rx=10)
    out += PR._rect(-250, -120, 510, 40, wood, 4, rx=8)
    out += PR._rect(-246, -170, 500, 54, "#efe6d6", 4, rx=20)
    out += PR._p("M-232,-168 Q-150,-196 -60,-178 Q60,-196 180,-180 Q250,-176 262,-150 L262,-106 Q0,-90 -232,-110 Z",
                 quilt, 4)
    for xx in range(-200, 240, 70):
        out += PR._line(xx, -180, xx - 6, -100, sw=2.4, color=S.shade(quilt, -0.25), extra='opacity="0.7"')
    for xx in range(-170, 240, 140):
        out += PR._circ(xx, -140, 6, "#f4d77a", 0, extra='opacity="0.85"')
    # the plain pillow at the headboard
    out += PR._p("M-236,-196 Q-232,-222 -196,-224 L-120,-222 Q-92,-220 -94,-196 Q-96,-172 -122,-170 L-200,-170 "
                 "Q-234,-170 -236,-196 Z", "#f3ecdf", 3.6)
    out += PR._p("M-210,-212 Q-160,-206 -112,-212", sw=2.2, stroke="#d8cdb8")
    out += PR._tube("M-262,0 L-262,-20", 18, S.shade(wood, -0.2), 3) + PR._tube("M268,0 L268,-20", 18,
                                                                                 S.shade(wood, -0.2), 3)
    return PR._place(out, x, y, s, 1)


def teddy_markup(x, y, k=1.0):
    """A small brown teddy bear sitting (anchor = its seat)."""
    c, cl = "#a47a5c", "#d8b894"
    b = (f'<ellipse cx="0" cy="-34" rx="30" ry="34" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
         f'<ellipse cx="0" cy="-30" rx="16" ry="18" fill="{cl}"/>'
         f'<ellipse cx="-24" cy="-6" rx="14" ry="10" fill="{c}" stroke="{INK}" stroke-width="3"/>'
         f'<ellipse cx="24" cy="-6" rx="14" ry="10" fill="{c}" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="-22" cy="-108" r="11" fill="{c}" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="22" cy="-108" r="11" fill="{c}" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="0" cy="-86" r="27" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
         f'<ellipse cx="0" cy="-77" rx="11" ry="8" fill="{cl}"/>'
         f'<circle cx="-9" cy="-92" r="3" fill="{INK}"/><circle cx="9" cy="-92" r="3" fill="{INK}"/>'
         f'<circle cx="0" cy="-80" r="3.2" fill="{INK}"/>'
         f'<path d="M-24,-58 Q0,-48 24,-58" stroke="#d96a6a" stroke-width="6" fill="none"/>'
         f'<ellipse cx="-30" cy="-44" rx="9" ry="16" fill="{c}" stroke="{INK}" stroke-width="3" '
         f'transform="rotate(20 -30 -44)"/>'
         f'<ellipse cx="30" cy="-44" rx="9" ry="16" fill="{c}" stroke="{INK}" stroke-width="3" '
         f'transform="rotate(-20 30 -44)"/>')
    return f'<g transform="translate({f1(x)},{f1(y)}) scale({k})">{b}</g>'


def toy_boat_markup(x, y, k=1.0):
    """A little toy sailboat (red hull, cream sail) standing on the shelf (anchor = bottom centre)."""
    b = (f'<path d="M-60,-30 L60,-30 Q52,0 30,0 L-30,0 Q-52,0 -60,-30 Z" fill="#d9634e" stroke="{INK}" '
         f'stroke-width="3.4" stroke-linejoin="round"/>'
         f'<path d="M-50,-22 L50,-22" stroke="#f6d36b" stroke-width="5"/>'
         f'<path d="M0,-30 L0,-128" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M4,-124 L52,-40 L4,-40 Z" fill="#f6efe0" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
         f'<path d="M-4,-110 L-40,-44 L-4,-44 Z" fill="#8fc0d8" stroke="{INK}" stroke-width="3" '
         f'stroke-linejoin="round"/>'
         f'<path d="M0,-128 l22,8 l-22,6 Z" fill="#f2c14e" stroke="{INK}" stroke-width="2.4"/>')
    return f'<g transform="translate({f1(x)},{f1(y)}) scale({k})">{b}</g>'


def room_svg(scene="s02"):
    """The bedroom: wallpaper with little stars (hole where the window glass is), moonlight on the floor, the
    picture's nail and string, a shelf with books and a toy sailboat, the bed with a teddy, the rug."""
    hx0, hy0, hx1, hy1 = OPEN[0] - 8, OPEN[1] - 8, OPEN[2] + 8, OPEN[3] + 4
    defs = ugrad("swwall", -20, BASE_Y, [(0, WALL_TOP[0]), (1, WALL_TOP[1])])
    defs += ugrad("swfloor", BASE_Y, H, [(0, "#73627a"), (1, "#5a4c62")])
    defs += S.rad_grad("swmoonf", [(0, "#c4cff0", 0.42), (0.6, "#aeb8e2", 0.18), (1, "#aeb8e2", 0)])
    wall = (f'<path d="M-30,-30 L{W + 30},-30 L{W + 30},{BASE_Y + 2} L-30,{BASE_Y + 2} Z '
            f'M{hx0},{hy0} L{hx0},{hy1} L{hx1},{hy1} L{hx1},{hy0} Z" fill="url(#swwall)" fill-rule="evenodd"/>')
    pat = ""
    rng = random.Random(4)
    for j, y in enumerate(range(40, BASE_Y - 40, 96)):
        for x in range(30 + (j % 2) * 70, W, 140):
            xx, yy = x + rng.uniform(-6, 6), y + rng.uniform(-6, 6)
            if hx0 - 60 < xx < hx1 + 60 and hy0 - 40 < yy < hy1 + 40:
                continue
            if (j + x // 140) % 3 == 0:
                pat += _star4(xx, yy, 11, "#8b93c2", 0.55)
            else:
                pat += f'<circle cx="{f1(xx)}" cy="{f1(yy)}" r="4" fill="#8188b8" opacity="0.5"/>'
    wall += pat
    # a soft vertical light band of the moonlight on the wall beside the window
    wall += (f'<path d="M{hx0 - 40},{hy1 + 4} L{hx1 + 30},{hy1 + 4} L{hx1 + 140},{BASE_Y} L{hx0 - 120},{BASE_Y} Z" '
             f'fill="#9aa6d6" opacity="0.18"/>')
    # baseboard and floor boards
    fl = (f'<rect x="-30" y="{BASE_Y}" width="{W + 60}" height="{H - BASE_Y + 40}" fill="url(#swfloor)"/>'
          f'<rect x="-30" y="{BASE_Y - 22}" width="{W + 60}" height="24" fill="#454d7c" stroke="{INK}" '
          f'stroke-width="3"/><path d="M-30,{BASE_Y - 18} L{W + 30},{BASE_Y - 18}" stroke="#7680b0" '
          f'stroke-width="3" opacity="0.7"/>')
    yv = BASE_Y
    for k in range(6):
        yv += 26 + 22 * k
        fl += f'<path d="M-30,{yv} L{W + 30},{yv}" stroke="#4d4058" stroke-width="2.6" opacity="0.55"/>'
    rng = random.Random(9)
    yv, k = BASE_Y, 0
    while yv < H + 30:
        nh = 26 + 22 * k
        for x in range(int(rng.uniform(-80, 0)) + (k % 2) * 120, W + 80, 260 + 30 * k):
            fl += (f'<path d="M{x},{yv + 2} L{x - 4},{yv + nh - 2}" stroke="#4d4058" stroke-width="2.4" '
                   f'opacity="0.5"/>')
        yv += nh
        k += 1
    # moonlight falling through the window onto the floor (with the mullion shadows)
    mx0, mx1 = OPEN[0], OPEN[2]
    fl += (f'<path d="M{mx0 + 10},{BASE_Y + 4} L{mx1 + 30},{BASE_Y + 4} L{mx1 + 260},{H + 20} L{mx0 - 60},{H + 20} Z" '
           f'fill="#b9c3ec" opacity="0.2"/>')
    cxm = (mx0 + mx1) / 2
    fl += (f'<path d="M{cxm + 8},{BASE_Y + 4} L{cxm + 120},{H + 20}" stroke="#4d4560" stroke-width="16" '
           f'opacity="0.18"/>')
    fl += (f'<path d="M{mx0 + 40},{BASE_Y + 120} L{mx1 + 120},{BASE_Y + 120}" stroke="#4d4560" stroke-width="12" '
           f'opacity="0.15"/>')
    # rug
    rcx, rcy = 1240, 1056
    fl += (f'<ellipse cx="{rcx}" cy="{rcy}" rx="400" ry="70" fill="#b47e94" stroke="{INK}" stroke-width="4"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="340" ry="56" fill="none" stroke="#e2b0a8" stroke-width="9" '
           f'stroke-dasharray="24 14"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="250" ry="38" fill="#c890a2"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="160" ry="22" fill="none" stroke="#f0c8b0" stroke-width="6"/>')
    # the picture's nail and string
    nx, ny = NAIL
    st = (f'<path d="M{FX0 + 70},{FY0 + 4} L{nx},{ny} L{FX0 + FRW - 70},{FY0 + 4}" stroke="#2f2a3a" '
          f'stroke-width="3" fill="none" opacity="0.8"/><circle cx="{nx}" cy="{ny}" r="7" fill="#c9a86a" '
          f'stroke="{INK}" stroke-width="2.6"/>')
    # a shelf with picture books, a little potted plant and a toy sailboat
    sx0, sx1, sy = 1040, 1350, 560
    sh = (f'<rect x="{sx0}" y="{sy}" width="{sx1 - sx0}" height="18" rx="5" fill="#b38a62" stroke="{INK}" '
          f'stroke-width="3.4"/>'
          f'<path d="M{sx0 + 30},{sy + 18} l0,30 l26,-30 Z M{sx1 - 30},{sy + 18} l0,30 l-26,-30 Z" fill="#9a7452" '
          f'stroke="{INK}" stroke-width="3"/>')
    x = sx0 + 14
    rng = random.Random(21)
    for i in range(6):
        bw = rng.uniform(20, 32)
        bh = rng.uniform(80, 112)
        col = ("#c96a62", "#5f8ac0", "#e2b84e", "#6e9e62", "#9a72b4", "#e08a4a")[i]
        tilt = -10 if i == 5 else 0
        sh += (f'<rect x="{x:.0f}" y="{sy - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" stroke="{INK}" '
               f'stroke-width="2.6" transform="rotate({tilt} {x + bw:.0f} {sy})"/>'
               f'<rect x="{x + 4:.0f}" y="{sy - bh + 12:.0f}" width="{bw - 8:.0f}" height="6" fill="#fbf3e3" '
               f'opacity="0.7" transform="rotate({tilt} {x + bw:.0f} {sy})"/>')
        x += bw + 3
    sh += toy_boat_markup(sx1 - 70, sy, 0.9)
    px_ = sx0 + 220
    sh += (f'<path d="M{px_ - 22},{sy - 44} L{px_ + 22},{sy - 44} L{px_ + 16},{sy} L{px_ - 16},{sy} Z" '
           f'fill="#c9714a" stroke="{INK}" stroke-width="3"/>')
    for a in (-55, -20, 15, 50):
        r = math.radians(a - 90)
        ex, ey = px_ + 52 * math.cos(r), sy - 44 + 52 * math.sin(r)
        sh += (f'<path d="M{px_},{sy - 44} Q{f1((px_ + ex) / 2 - 8)},{f1((sy - 44 + ey) / 2)} {f1(ex)},{f1(ey)} '
               f'Q{f1((px_ + ex) / 2 + 9)},{f1((sy - 44 + ey) / 2 + 7)} {px_},{sy - 44} Z" fill="#6f9e5c" '
               f'stroke="{INK}" stroke-width="2.4"/>')
    bx, by = BED
    s = KID[2]
    bed = bed_markup(bx, by, s)
    tx = bx + 175 * s if scene == "s15" else bx - 120 * s      # s15: the girl sits by the headboard
    bed += teddy_markup(tx, by + PR.BED_TOP * s + 6, 0.95)
    bed = C.ground_shadow(bx + 10, by + 4, s, 330, 0.2) + bed
    body = (S.g(wall, filter="wobble") + S.g(st, filter="wobble-fine") + S.g(fl, filter="wobble") +
            S.g(sh, filter="wobble-fine") + bed)
    return body, defs


def frame_border_svg(glow=0.0):
    """The wooden frame round the picture (on the wall, around the GK0-sized picture)."""
    b = 26
    x0, y0, x1, y1 = FX0, FY0, FX0 + FRW, FY0 + FRH
    wood, dark, lite = "#c79a5e", "#8f6a42", "#e8c48a"
    d = (f"M{x0 - b},{y0 - b} L{x1 + b},{y0 - b} L{x1 + b},{y1 + b} L{x0 - b},{y1 + b} Z "
         f"M{x0},{y0} L{x0},{y1} L{x1},{y1} L{x1},{y0} Z")
    out = f'<path d="{d}" fill="{wood}" fill-rule="evenodd" stroke="{INK}" stroke-width="4"/>'
    out += (f'<rect x="{x0 - b + 7}" y="{y0 - b + 7}" width="{x1 - x0 + 2 * b - 14}" height="{y1 - y0 + 2 * b - 14}" '
            f'fill="none" stroke="{lite}" stroke-width="3" opacity="0.8"/>'
            f'<rect x="{x0 - 5}" y="{y0 - 5}" width="{x1 - x0 + 10}" height="{y1 - y0 + 10}" fill="none" '
            f'stroke="{dark}" stroke-width="5"/>')
    for cx, cy in ((x0 - b / 2, y0 - b / 2), (x1 + b / 2, y0 - b / 2), (x0 - b / 2, y1 + b / 2), (x1 + b / 2, y1 + b / 2)):
        out += f'<circle cx="{cx}" cy="{cy}" r="5" fill="{lite}" stroke="{INK}" stroke-width="2"/>'
    out += (f'<rect x="{x0 - b}" y="{y1 + b - 2}" width="{x1 - x0 + 2 * b}" height="10" fill="#2a2440" '
            f'opacity="0.25" filter="url(#soft)"/>')
    return doc(S.g(out, filter="wobble-fine"))


def frame_glow_svg():
    defs = S.rad_grad("swfg", [(0, "#ffe6a8", 0.65), (0.55, "#ffd890", 0.25), (1, "#ffd890", 0)])
    cx, cy = FX0 + FRW / 2, FY0 + FRH / 2
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{FRW * 0.9}" ry="{FRH * 1.05}" fill="url(#swfg)"/>', defs)


# ---- outside the window (behind the wall: seen only through the glass)

OUT_BOX = (int(OPEN[0]) - 60, int(OPEN[1]) - 30, int(OPEN[2]) + 40, int(OPEN[3]) + 20)
MOON = (OPEN[2] - 84, OPEN[1] + 92)


def outside_svg(stars=0.0):
    x0, y0, x1, y1 = OUT_BOX
    defs = ugrad("swout", y0, y1, [(0, "#232a52"), (0.6, "#343d6e"), (1, "#4a5288")])
    defs += S.rad_grad("swmoonh", [(0, "#f6f0da", 0.5), (0.4, "#c8cfee", 0.18), (1, "#c8cfee", 0)])
    b = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#swout)"/>'
    rng = random.Random(3)
    for i in range(16):
        sx, sy = rng.uniform(x0, x1), rng.uniform(y0, y0 + (y1 - y0) * 0.55)
        a = min(1.0, max(0.0, stars * 16 - i)) * 0.5 + 0.35
        b += f'<circle cx="{f1(sx)}" cy="{f1(sy)}" r="{rng.uniform(1.6, 3.2):.1f}" fill="#f6eecf" opacity="{a:.2f}"/>'
    mx, my = MOON
    b += f'<circle cx="{mx}" cy="{my}" r="150" fill="url(#swmoonh)"/>'
    b += PR._circ(mx, my, 36, "#f4eed8", 3, stroke=S.mix(INK, "#f4eed8", 0.45))
    for dx, dy, r in ((-10, -8, 7), (9, 6, 5), (-2, 14, 4)):
        b += f'<circle cx="{mx + dx}" cy="{my + dy}" r="{r}" fill="#e2dac0" opacity="0.8"/>'
    # far roofs of the town with warm lit windows, dark trees
    gy = OPEN[3] + 6
    town = ""
    rng = random.Random(8)
    hx = x0 - 20
    while hx < x1 + 40:
        w = rng.uniform(70, 120)
        h = rng.uniform(70, 130)
        col = rng.choice(("#2b3260", "#323a6a", "#28305a"))
        town += (f'<path d="M{f1(hx)},{gy} L{f1(hx)},{f1(gy - h)} L{f1(hx + w / 2)},{f1(gy - h - w * 0.4)} '
                 f'L{f1(hx + w)},{f1(gy - h)} L{f1(hx + w)},{gy} Z" fill="{col}" stroke="#1d2244" stroke-width="2.4"/>')
        for k in range(rng.randint(1, 2)):
            if rng.random() < 0.7:
                wx, wy = hx + w * rng.uniform(0.2, 0.65), gy - h * rng.uniform(0.35, 0.75)
                town += f'<rect x="{f1(wx)}" y="{f1(wy)}" width="16" height="18" fill="#f6d27a" opacity="0.9"/>'
        hx += w + rng.uniform(4, 18)
    for tx, ty, r in ((OPEN[0] + 60, gy - 120, 70), (OPEN[2] - 40, gy - 90, 56)):
        town += S.cloud(tx, ty, r * 2, r * 1.3, "#25304e", seed=int(tx), puffs=4, sw=2.4, shade_fill="#1f2944")
    b += town
    return boxed(S.g(b, filter="wobble-fine"), OUT_BOX, defs)


BRANCH_PIV = (OPEN[0] - 30, OPEN[3] - 150)
BRANCH_BOX = (int(BRANCH_PIV[0] - 110), int(BRANCH_PIV[1] - 330), int(BRANCH_PIV[0] + 500), int(BRANCH_PIV[1] + 90))


def branch_svg(k=0):
    """A tree branch reaching across the window from the left (rotates about BRANCH_PIV); k = leaf flutter frame."""
    bx, by = BRANCH_PIV
    tc, lc, lc2 = "#2c3456", "#3e5c66", "#4f7270"
    pts = [(bx - 40, by + 30), (bx + 90, by - 30), (bx + 220, by - 110), (bx + 340, by - 150), (bx + 430, by - 160)]
    out = PR._tube(S.smooth_path(pts, closed=False), 18, tc, 3)
    out += PR._tube(S.smooth_path([(bx + 150, by - 70), (bx + 210, by - 10), (bx + 270, by + 20)], closed=False),
                    9, tc, 2.6)
    out += PR._tube(S.smooth_path([(bx + 260, by - 128), (bx + 300, by - 210), (bx + 330, by - 250)], closed=False),
                    8, tc, 2.6)
    rng = random.Random(7)
    leaves = [(bx + 90, by - 30), (bx + 160, by - 72), (bx + 220, by - 110), (bx + 300, by - 145),
              (bx + 380, by - 158), (bx + 430, by - 160), (bx + 270, by + 20), (bx + 330, by - 250),
              (bx + 300, by - 210), (bx + 230, by - 5)]
    for i, (lx, ly) in enumerate(leaves):
        for j in range(3):
            a = rng.uniform(-150, 30) + 22 * math.sin(k * 2.1 + i + j)
            r = math.radians(a)
            ex, ey = lx + 30 * math.cos(r), ly + 30 * math.sin(r)
            out += PR._ell(ex, ey, 19, 9, lc if (i + j) % 2 else lc2, 2.4, stroke="#1d2244",
                           extra=f'transform="rotate({a:.0f} {f1(ex)} {f1(ey)})"')
    return boxed(S.g(out, filter="wobble-fine"), BRANCH_BOX)


CLOUD_BOX = (-20, 100, 420, 300)


def cloud_svg(i):
    w, h = (230, 170, 200)[i], (70, 54, 62)[i]
    col = ("#58609a", "#5f66a0", "#525a92")[i]
    b = S.cloud(200, 200, w, h, col, seed=30 + i, puffs=5, sw=2.6, shade_fill=S.shade(col, -0.18))
    b += (f'<path d="M{200 - w * 0.3:.0f},{200 - h * 0.32:.0f} q{w * 0.2:.0f},{-h * 0.2:.0f} {w * 0.4:.0f},0" '
          f'stroke="#b8bfe6" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>')
    for k in range(2):           # a wind streak trailing the cloud
        yy = 200 + h * (0.1 + 0.3 * k)
        b += (f'<path d="M{200 - w * 0.9:.0f},{yy:.0f} q{w * 0.3:.0f},-8 {w * 0.55:.0f},0" stroke="#c9d0ee" '
              f'stroke-width="3" fill="none" stroke-linecap="round" opacity="0.5"/>')
    return boxed(S.g(b, filter="wobble-fine"), CLOUD_BOX)


CLOUD_Y = (OPEN[1] + 70, OPEN[1] + 230, OPEN[1] + 150)


# ---- the window itself (frame, glass, sill, curtains) - library window_wind(part='front')

WIN_BOX = (int(WIN[0] - 400 * WIN[2]), int(WIN[1] - 560 * WIN[2]), int(WIN[0] + 400 * WIN[2]),
           int(WIN[1] + 130 * WIN[2]))


def window_front_svg(wind, phase, glow=0.0):
    x, y, s = WIN
    return boxed(PR.window_wind(x, y, s, wind=wind, phase=phase, part="front", glow=glow), WIN_BOX)


def rattle_svg():
    """Little rattle ticks at the window frame's corners (drawn on top for the '哐' beats)."""
    x0, y0, x1, y1 = OPEN
    out = ""
    for cx, cy, sg in ((x0 - 62, y0 + 40, -1), (x1 + 62, y0 + 40, 1), (x0 - 62, y1 - 60, -1), (x1 + 62, y1 - 60, 1)):
        for k in range(3):
            out += (f'<path d="M{cx + sg * 15 * k},{cy - 18 + 4 * k} l{sg * 10},{30 - 8 * k}" stroke="#e8e0f6" '
                    f'stroke-width="5" stroke-linecap="round" fill="none"/>')
            out += (f'<path d="M{cx + sg * 15 * k},{cy - 18 + 4 * k} l{sg * 10},{30 - 8 * k}" stroke="{INK}" '
                    f'stroke-width="2.4" stroke-linecap="round" fill="none"/>')
    return doc(out)


# ---- the girl

KID_BOX = (int(KID[0] - 220), int(KID[1] - 430), int(KID[0] + 220), int(KID[1] + 24))


def kid_svg(pose, facing, expr, x=None, y=None, box=KID_BOX, pillow=True):
    kx, ky, ks = KID
    x = kx if x is None else x
    y = ky if y is None else y
    return boxed(C.child(x, y, ks, facing, pose=pose, expr=expr, outfit="pyjamas", pillow=pillow), box)


def kid_shadow_svg():
    kx, ky, ks = KID
    return boxed(C.ground_shadow(kx + 6, ky + 2, ks, 120, 0.24), KID_BOX)


# ================================================================== wind


class Wind:
    """A wind strength w(t) 0..1 from a base level and gusts, with integrals for cloud travel and branch phase."""

    def __init__(self, base, gusts, T, dt=1 / 120):
        self.base, self.gusts = base, gusts
        n = int(T / dt) + 3
        ts = np.arange(n) * dt
        ws = np.array([self.w(t) for t in ts])
        self.ts, self.dt = ts, dt
        self.travel = np.concatenate([[0.0], np.cumsum((30 + 300 * ws[:-1]) * dt)])
        self.phase = np.concatenate([[0.0], np.cumsum((0.7 + 1.5 * ws[:-1]) * dt)])

    def w(self, t):
        v = self.base(t)
        for t0, amp, att, dec in self.gusts:
            u = t - t0
            if u < -att:
                continue
            g = amp * (0.5 - 0.5 * math.cos(math.pi * (u + att) / att)) if u < 0 else amp * math.exp(-u / dec)
            v = max(v, g)
        return min(1.0, v)

    def _interp(self, arr, t):
        return float(np.interp(t, self.ts, arr))

    def travel_at(self, t):
        return self._interp(self.travel, t)

    def phase_at(self, t):
        return self._interp(self.phase, t)

    def level(self, t, levels=WIND_LV):
        v = self.w(t)
        return min(range(len(levels)), key=lambda i: abs(levels[i] - v))


def add_outside(sc, wind, z, iris=None, alpha=None, iris_c=None, t_on=0.0):
    """The view through the window: sky + moon + town (static), three clouds racing with the wind (wrapping
    behind the wall), the thrashing branch and flying leaves (behind the wall layer). ``iris(box, cx, cy)`` makes an
    opening iris reveal for a boxed layer (cx, cy: the iris centre in that layer's own coordinates)."""
    a_ = alpha or (lambda t: 1.0)
    ic = iris_c or (0, 0)
    sc.add("sw_outside", outside_svg(), z=z, reveal=iris(OUT_BOX, ic[0], ic[1]) if iris else None,
           motion=(lambda t: Tf(alpha=a_(t))) if alpha else None, wc=0.6)
    span = (OPEN[2] - OPEN[0]) + 700

    def cpos(t, i):
        x = (wind.travel_at(t) + i * span / 3 + 140) % span
        return OPEN[0] - 330 + x - 200, CLOUD_Y[i] - 200 + 6 * math.sin(t * 0.9 + i)
    for i in range(3):
        def cm(t, i=i):
            dx, dy = cpos(t, i)
            return Tf(dx=dx, dy=dy, alpha=a_(t))
        rv = None
        if iris:
            rv = iris(CLOUD_BOX, lambda t, i=i: ic[0] - cpos(t, i)[0], lambda t, i=i: ic[1] - cpos(t, i)[1])
        sc.add(f"sw_cloud{i}", cloud_svg(i), z=z + 0.1 + i * 0.01, motion=cm, reveal=rv, wc=0.5)

    def brot(t):
        w = wind.w(t)
        ph = wind.phase_at(t)
        return -(1.5 + 7.5 * w) * (0.55 + 0.45 * math.sin(2 * math.pi * ph)) + 1.5

    def bm(t):
        return Tf(rot=brot(t), px=BRANCH_PIV[0], py=BRANCH_PIV[1], alpha=a_(t))

    def b_c(t, k):
        a = math.radians(-brot(t))
        dx, dy = ic[0] - BRANCH_PIV[0], ic[1] - BRANCH_PIV[1]
        q = (BRANCH_PIV[0] + dx * math.cos(a) - dy * math.sin(a), BRANCH_PIV[1] + dx * math.sin(a) + dy * math.cos(a))
        return q[k]
    sc.add("sw_branch", [branch_svg(k) for k in range(3)], z=z + 0.2, motion=bm,
           reveal=iris(BRANCH_BOX, lambda t: b_c(t, 0), lambda t: b_c(t, 1)) if iris else None,
           frame_at=lambda t: float(int(t / (0.16 - 0.08 * wind.w(t))) % 3), wc=0.5)

    leaves = Leaves(wind)
    sc.add_dynamic("sw_leaves", lambda t: leaves(t, a_(t) if t >= t_on else 0.0), z=z + 0.3)


class Leaves:
    """Leaves torn off by the gusts, flying past outside the window (drawn with PIL, behind the wall)."""

    def __init__(self, wind, n=14, seed=5):
        rng = random.Random(seed)
        self.wind = wind
        self.items = [(rng.uniform(0, 1), rng.uniform(OPEN[1] + 20, OPEN[3] - 40), rng.uniform(0.7, 1.3),
                       rng.uniform(0, 6.28), rng.choice(("#9ab48c", "#c8ae6e", "#86aa94", "#b8c27a"))) for _ in range(n)]
        self.x0, self.y0 = int(OPEN[0]) - 40, int(OPEN[1]) - 20
        self.w, self.h = int(OPEN[2] - OPEN[0]) + 80, int(OPEN[3] - OPEN[1]) + 40

    def __call__(self, t, alpha=1.0):
        if alpha <= 0.01:
            return None
        trav = self.wind.travel_at(t)
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        drawn = False
        for i, (u0, yy, sp, ph, col) in enumerate(self.items):
            x = ((u0 * 1600 + trav * 2.6 * sp) % 1600) - 400
            if not (-30 < x < self.w + 30):
                continue
            wv = self.wind.w(t)
            if wv < 0.45 + 0.04 * (i % 5):
                continue
            y = yy - self.y0 + 30 * math.sin(t * 3 + ph) + 0.08 * x
            a = math.radians((t * 360 * sp + ph * 57) % 360)
            c = tuple(int(col[k:k + 2], 16) for k in (1, 3, 5))
            pts = []
            for k in range(10):
                q = 2 * math.pi * k / 10
                px, py = 24 * math.cos(q) * (0.6 + 0.4 * abs(math.cos(t * 7 + ph))), 9 * math.sin(q)
                pts.append((x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)))
            d.polygon(pts, fill=(*c, int(230 * alpha)), outline=(29, 34, 68, int(230 * alpha)))
            drawn = True
        if not drawn:
            return None
        return im, (self.x0, self.y0)


def window_frames(wind_levels=WIND_LV, glows=(0.0,)):
    """window_wind front frames, index = (phase * n_glow + g) * n_levels + level."""
    out = []
    for p in range(WPH):
        for gl in glows:
            for wv in wind_levels:
                out.append(window_front_svg(wv, p / WPH, gl))
    return out


# ================================================================== the picture (the story's lake)

GBOX = (0, 0, W, H)


def g_pts():
    return PR.boat_points(GB[0], GB[1], GB[2], 1)


def g_sky_a_svg():
    return doc(PR.lake_galilee(-40, W + 40, G_HZ + 250 * G_LAKE_S, G_LAKE_S, time="sunset", shore=None, part="back",
                               boats=False, top=-40, sun_x=G_SUN) +
               S.g(PR._haze(S.cloud(1600, 170, 420, 74, "#f8cdb0", seed=12, puffs=5, sw=3, shade_fill="#e3a2b2") +
                               S.cloud(420, 260, 300, 60, "#f8cdb0", seed=13, puffs=5, sw=3, shade_fill="#e3a2b2"),
                               "#c99ab2", 0.08, 0.5, 0.75), filter="wobble"))


G_STOPS = [(0.0, "#f7cf92"), (0.12, "#eeb08e"), (0.36, "#b98aa6"), (0.66, "#7d6ca2"), (1.0, "#4b4783")]


def g_water_a_svg():
    body, defs = evening_water("swgw", G_HZ - 2, H + 40, stops=G_STOPS, hz=G_HZ)
    body += f'<path d="M-30,{G_HZ + 1} L{W + 30},{G_HZ + 1}" stroke="#ffe0a8" stroke-width="4" opacity="0.8"/>'
    bx, by, bs = GB
    hw = 690 * bs
    body += (f'<path d="M{bx - hw},{by + 2} Q{bx},{by + 30} {bx + hw},{by + 2} Q{bx + hw * 0.7},{by + 90} {bx},{by + 100} '
             f'Q{bx - hw * 0.7},{by + 90} {bx - hw},{by + 2} Z" fill="#3b376c" opacity="0.36"/>')
    return doc(S.g(body, filter="wobble"), defs)


def g_ripples_svg(k):
    bx, by, bs = GB
    avoid = ((bx - 760 * bs, by - 220 * bs, bx + 760 * bs, by + 6),)
    return doc(S.g(water_ripples(k % 6, 6, 31, G_HZ, H + 20, sun_x=W * G_SUN, avoid=avoid, count=80),
                   filter="wobble-fine"))


def g_strip_a_svg():
    bx, by, bs = GB
    x0, x1 = bx - 760 * bs, bx + 760 * bs
    top = S.wave_line(by - 3, 2.6, 110, 0.6, x0=x0, x1=x1)
    d = top + f" L{x1},{by + 70 * bs + 20} L{x0},{by + 70 * bs + 20} Z"
    defs = ugrad("swgs", G_HZ, H, G_STOPS)
    body = f'<path d="{d}" fill="url(#swgs)"/>'
    body += (f'<path d="{S.wave_line(by - 1, 2.6, 110, 0.6, x0=bx - 690 * bs, x1=bx + 700 * bs)}" stroke="#ffe4c0" '
             f'stroke-width="4" fill="none" opacity="0.85"/>')
    mask = (f'<linearGradient id="swgsm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" '
            f'stop-opacity="0"/><stop offset="0.1" stop-color="#fff"/><stop offset="0.9" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="swgsmask"><rect x="{x0}" y="{by - 30}" width="{x1 - x0}" height="140" fill="url(#swgsm)"/></mask>')
    return doc(f'<g mask="url(#swgsmask)">{S.g(body, filter="wobble-fine")}</g>', defs + mask)


def g_storm_base_svg():
    """The cold storm sky gradient alone (the cloud banks are separate drifting layers)."""
    return doc(PR.storm_sky(-20, -40, W + 20, G_LEVEL + 40, density=0.0, wind=0.0, rain=0.0, seed=7, scale=0.8))


BANKS = ((0.10, 0.85, 0), (0.36, 1.1, 1), (0.62, 1.35, 2))      # (height in the sky, size, colour index)
BANK_V = (45, 85, 140)                                          # drift speeds (px/s)


def g_bank_svg(b):
    """One bank of storm clouds as a seamless horizontal tile (period W): drawn twice side by side it can drift."""
    c0, c1, c2, c3 = PR.STORM_SKY_COLS
    ny, k, ci = BANKS[b]
    col = (c2, S.mix(c1, c2, 0.4), S.shade(c1, -0.05))[ci]
    light = S.mix(col, c3, 0.35)
    rng = random.Random(20 + b)
    s = 0.8
    H_ = G_LEVEL + 80
    out = ""
    for i in range(7):
        bx = (i + rng.uniform(-0.3, 0.3)) * W / 7
        by = -40 + H_ * (ny + rng.uniform(-0.1, 0.1))
        w = rng.uniform(420, 700) * s * k
        h = w * rng.uniform(0.32, 0.42)
        for cx in (bx - W, bx, bx + W):
            if cx + w * 0.6 < -10 or cx - w * 0.6 > W + 10:
                continue
            out += S.cloud(cx, by, w, h, fill=col, seed=60 + b * 20 + i, puffs=6, sw=3.6 * s,
                           shade_fill=S.shade(col, -0.25))
            out += S.cloud(cx - w * 0.06, by - h * 0.08, w * 0.55, h * 0.5, fill=light, seed=67 + b * 20 + i,
                           puffs=4, sw=2.6 * s)
    return doc(S.g(out, filter="wobble"))


def g_streaks_svg():
    rng = random.Random(9)
    out = ""
    for i in range(16):
        wx = rng.uniform(0, W)
        wy = rng.uniform(80, G_LEVEL - 40)
        L = rng.uniform(140, 300) * 0.8
        curl = rng.uniform(16, 30) * 0.8
        for x in (wx - W, wx, wx + W):
            out += (f'<path d="M{f1(x)},{f1(wy)} q{f1(L * 0.5)},-10 {f1(L)},0 q{f1(curl)},2 {f1(curl * 0.4)},'
                    f'{f1(-curl * 0.8)}" stroke="#e6ecf2" stroke-width="3" fill="none" stroke-linecap="round" '
                    f'opacity="0.6"/>')
    return doc(S.g(out, filter="wobble-fine"))


def g_storm_lake_svg(level, k, part):
    wave = (0.55, 1.0)[level]
    return doc(PR.storm_lake(-20, W + 20, G_LEVEL, phase=k / LPH, wave=wave, spray=0.4 + 0.3 * level, part=part,
                             seed=3, scale=G_LAKE_K))


def g_boat_svg(state, k, part):
    bx, by, bs = GB
    if state == "calm":
        return doc(PR.fishing_boat(bx, by, bs, 1, sail="full", phase=k / 4, part=part))
    return doc(PR.fishing_boat(bx, by, bs, 1, sail="flapping", phase=k / 6, part=part, wet=True))


G_FAR = ((5, 1), (8, 2), (10, 4), (6, 5))


def g_far_svg(state):
    p = g_pts()["far_stand"]
    out = ""
    for j, (v, i) in enumerate(G_FAR):
        x, y = p[i]
        f = -1 if i >= 3 else 1
        if state == "calm":
            out += C.disciples(x, y, GB[2], f, variant=v, pose="stand", expr="happy" if j % 2 else "kind")
        else:
            out += C.disciples(x, y, GB[2], f, variant=v, pose="scared", expr="worried", shake=0.0, wet=True, wind=1.0)
    return doc(out)


def g_jesus_svg():
    x, y = g_pts()["sleep"]
    return doc(C.jesus(x, y, GB[2], 1, pose="sleep"))


def g_near_svg(state, ph=0.0):
    p = g_pts()
    s = GB[2]
    out = ""
    if state == "calm":
        x, y = p["stand"][1]
        out += C.disciples(x, y, s, 1, variant=3, pose="stand", expr="happy")
        x, y = p["stand"][2]
        out += C.disciples(x, y, s, -1, variant=1, pose="sit", expr="kind")
        x, y = p["stand"][4]
        out += C.disciples(x, y, s, 1, variant=0, pose="pull_rope", expr="happy")
    else:
        x, y = p["stand"][1]
        out += C.disciples(x, y, s, -1, variant=1, pose="bail", phase=ph, expr="worried", wet=True, wind=1.0)
        x, y = p["cling"]
        out += C.disciples(x, y, s, 1, variant=3, pose="cling", expr="worried", wet=True, wind=1.0)
        x, y = p["stand"][4]
        out += C.disciples(x, y, s, 1, variant=0, pose="pull_rope", expr="worried", wet=True, wind=1.0)
    return doc(out)


def g_splash_svg(big=1.0):
    """A burst of white foam and spray thrown up over the bow (boat-local drawing, placed with the boat)."""
    rng = random.Random(int(big * 10))
    ink = S.mix(INK, "#5a7890", 0.35)
    foam = PR.STORM_FOAM
    out = ""
    for i in range(10):
        u = i / 9
        x = 560 + 240 * u
        y = -230 - 230 * math.sin(math.pi * (0.15 + 0.7 * u)) * big
        r = (34 + 18 * math.sin(math.pi * u)) * (0.8 + 0.2 * big)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r + 4)}" fill="{ink}"/>'
    for i in range(10):
        u = i / 9
        x = 560 + 240 * u
        y = -230 - 230 * math.sin(math.pi * (0.15 + 0.7 * u)) * big
        r = (34 + 18 * math.sin(math.pi * u)) * (0.8 + 0.2 * big)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{foam}"/>'
        out += f'<circle cx="{f1(x - r * 0.3)}" cy="{f1(y - r * 0.3)}" r="{f1(r * 0.3)}" fill="#ffffff" opacity="0.6"/>'
    for i in range(int(16 * big)):
        a = rng.uniform(-2.9, -0.3)
        d = rng.uniform(150, 330) * big
        x, y = 680 + d * math.cos(a), -300 + d * math.sin(a) * 0.9
        r = rng.uniform(7, 15)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{foam}" stroke="{ink}" stroke-width="3"/>'
    return doc(PR._place(out, GB[0], GB[1], GB[2], 1))


def g_dim_svg():
    return doc(f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 20}" fill="#262a52"/>')


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    m0 = voice_marks(ctx, 0)
    m1 = voice_marks(ctx, 1)
    L0, L1 = ctx.lines[0], ctx.lines[1]

    def ph(m, i, text, a, b):
        return m[i] if len(m) > i and m[i][0] == text else (text, a, b, [(a, b)])
    p_kid = ph(m0, 0, "小朋友", L0.start, L0.start + 0.6)
    p_q = ph(m0, 1, "你遇到过很大很大的风吗", L0.start + 0.9, L0.chunks[0].end)
    p_hu = ph(m0, 2, "风呼呼地吹", L0.chunks[1].start, L0.chunks[1].start + 1.4)
    p_kuang = ph(m0, 3, "窗户哐哐地响", L0.chunks[1].start + 1.6, L0.chunks[1].end)
    p_fear = ph(m0, 4, "你会不会害怕", L0.chunks[-1].start, L0.end)
    p_today = ph(m1, 0, "今天的故事里", L1.start, L1.start + 1.1)
    p_boat = ph(m1, 1, "有一群人在船上", L1.chunks[0].start + 1.4, L1.chunks[0].end)
    p_big = ph(m1, 2, "遇到了好大好大的风浪", L1.chunks[-1].start, L1.end)
    cq, chu, ckg, cfr, cbig = (char_times(p) for p in (p_q, p_hu, p_kuang, p_fear, p_big))
    t_kid = p_kid[1]
    t_da = [cq[5], cq[7]]                         # '大' '大'
    t_hu = [chu[1], chu[2]]                       # '呼' '呼'
    t_kg = [ckg[2], ckg[3]]                       # '哐' '哐'
    t_fear0 = p_fear[1]
    t_peek = snap(cfr[4] - 0.03)                  # '害'
    t_today = p_today[1]
    t_boat = p_boat[1]
    t_hao = [cbig[3], cbig[5]]                    # '好' '好'
    t_daa = [cbig[4], cbig[6]]                    # '大' '大'

    # ---- s01's title page, continued (identical picture across the cross-dissolve)
    tl = load_timeline()
    c01 = context("s01_title", tl)
    starts = {s["id"]: s["start"] for s in tl["scenes"]}
    toff = starts[ctx.id] - starts["s01_title"]
    t_iris = max(1.0, t_kid + 0.02)
    t_iris_end = t_iris + 1.15
    page_gate = lambda t: 1.0 if t < t_iris_end + 0.05 else 0.0           # noqa: E731
    title_gate = lambda t: 1.0 - M.progress(t, 1.0, 1.4, "sine")          # noqa: E731
    cam_title, fx_title, _ = T1.title_page(sc, c01, toff, gate=page_gate, title_gate=title_gate)

    def radius(t):
        if t >= t_iris_end:
            return None
        return M.progress(t, t_iris, t_iris_end, "sine") * 1650 - 70      # negative: nothing shows yet

    def iris(box, cx=IRIS_C[0], cy=IRIS_C[1]):
        return iris_reveal(box, cx, cy, radius)

    # ---- the zoom into the picture on line 1
    t_turn = snap(t_today + 0.06)
    t_glow = t_today + 0.3
    t_alive = t_glow + 0.25
    tz0, tz1 = max(t_today + 0.7, t_boat - 0.7), max(t_today + 2.0, t_boat + 0.6)

    def kz(t):
        u = M.progress(t, tz0, tz1, "inout")
        return GK0 * (1 / GK0) ** u
    room_on = lambda t: 1.0 if t < tz1 + 0.05 else 0.0                     # noqa: E731

    wind = Wind(lambda t: 0.22 + 0.16 * M.progress(t, t_iris + 0.6, t_da[0], "sine")
                - 0.06 * M.progress(t, t_fear0, t_fear0 + 1.2, "sine") - 0.08 * M.progress(t, t_today, t_today + 1, "sine"),
                [(t_da[0], 0.5, 0.12, 0.45), (t_da[1], 0.58, 0.12, 0.5),
                 (t_hu[0], 1.0, 0.14, 0.55), (t_hu[1], 1.0, 0.12, 0.9),
                 (t_kg[0], 0.8, 0.08, 0.6), (t_kg[1], 0.82, 0.06, 0.9)], T)

    # ---- the room (z 100..): outside view behind the wall, the wall, the window, the girl
    Z = 100
    add_outside(sc, wind, Z, iris=iris, alpha=room_on, iris_c=IRIS_C, t_on=t_iris_end)
    body, defs = room_svg()
    sc.add("sw_room", boxed(body, GBOX, defs), z=Z + 1, reveal=iris(GBOX), motion=lambda t: Tf(alpha=room_on(t)))

    # window front: curtains / wind level x phase, two shake beats on '哐'
    wfr = window_frames()
    nl = len(WIND_LV)

    def win_fa(t):
        p = int(t / 0.085) % WPH
        return float(p * nl + wind.level(t))

    def shake_beats(t, amp=6.0):
        dx = dy = 0.0
        for tk in t_kg:
            u = t - tk
            if 0 <= u < 0.3:
                e = math.exp(-u / 0.1)
                dx += amp * e * math.sin(2 * math.pi * u * 22)
                dy += 0.4 * amp * e * math.cos(2 * math.pi * u * 17)
        return dx, dy

    def win_m(t):
        dx, dy = shake_beats(t)
        return Tf(dx=dx, dy=dy, alpha=room_on(t))
    sc.add("sw_window", wfr, z=Z + 2, frame_at=win_fa, motion=win_m, reveal=iris(WIN_BOX), seed=61, wc=0.8)

    def tick_m(t):
        a = 0.0
        for tk in t_kg:
            u = t - tk
            if -0.02 <= u < 0.32:
                a = max(a, 1.0 - u / 0.32)
        dx, dy = shake_beats(t, 4)
        return Tf(dx=dx, dy=dy, alpha=a * room_on(t))
    sc.add("sw_ticks", rattle_svg(), z=Z + 2.1, motion=tick_m, wc=0)

    # the girl
    kx, ky, ks = KID
    kfr = {
        "look": kid_svg("hug_pillow", 1, "sw_look"), "look_b": kid_svg("hug_pillow", 1, blink("sw_look")),
        "surp": kid_svg("hug_pillow", 1, "surprised"), "surp_b": kid_svg("hug_pillow", 1, blink("surprised")),
        "scared": kid_svg("hug_pillow", 1, "scared"),
        "cur": kid_svg("hug_pillow", 1, "sw_curious"), "cur_b": kid_svg("hug_pillow", 1, blink("sw_curious")),
        "turn": kid_svg("hug_pillow", -1, "sw_wonder"), "turn_b": kid_svg("hug_pillow", -1, blink("sw_wonder")),
    }
    names = list(kfr)
    KI = {k: i for i, k in enumerate(names)}
    t_surp = snap(t_hu[0] + 0.02)
    t_scared = snap(t_kg[0] + 0.01)
    ents = [(0, KI["look"]), (t_surp, KI["surp"]), (t_scared, KI["scared"]), (t_peek, KI["cur"]),
            (t_turn, KI["turn"])]
    for tb, base in ((t_iris_end + 0.5, "look"), (t_hu[0] - 0.75, "look"), (t_hu[1] + 0.75, "surp"),
                     (t_peek + 0.9, "cur"), (t_today - 0.3, "cur"), (t_turn + 0.9, "turn")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.35 for tk, _ in ents):
            ents += [(tb, KI[base + "_b"]), (snap(tb + 0.13), KI[base])]
    ents = sorted(ents)
    feet = (kx, ky)

    def lean(t):
        r = 0.0
        for tk in t_hu:
            u = t - tk
            if u > -0.1:
                r -= 3.2 * math.exp(-max(0.0, u) / 0.5) * M.progress(t, tk - 0.1, tk + 0.08, "out")
        r += 3.5 * M.progress(t, t_peek, t_peek + 0.45, "sine") * (1 - M.progress(t, t_turn - 0.25, t_turn, "sine"))
        return Tf(rot=r, px=kx, py=ky)

    def hops(t):
        dy = 0.0
        for tk, hgt in ((t_kg[0], 26), (t_kg[1], 12)):
            u = t - tk
            if 0 <= u < 0.32:
                dy -= hgt * math.sin(math.pi * u / 0.32)
        u = t - t_turn
        if 0 <= u < 0.36:
            dy -= 22 * math.sin(math.pi * u / 0.36)
        return Tf(dy=dy)

    def squeeze(t):
        k = M.progress(t, t_fear0, t_fear0 + 0.3, "out") * (1 - M.progress(t, t_peek - 0.1, t_peek + 0.4, "sine"))
        return Tf(sx=1 + 0.025 * k, sy=1 - 0.03 * k, px=kx, py=ky)
    kid_m = M.combine(lean, hops, squeeze, dip(t_surp, ks, feet, 6), dip(t_scared, ks, feet, 8),
                      dip(t_peek, ks, feet, 5), dip(t_turn, ks, feet, 7), M.breathe(0.012, 2.6, pivot=feet),
                      lambda t: Tf(alpha=room_on(t)))
    sc.add("sw_kid_sh", kid_shadow_svg(), z=Z + 2.9, reveal=iris(KID_BOX), motion=lambda t: Tf(alpha=room_on(t)))
    sc.add("sw_kid", [kfr[k] for k in names], z=Z + 3, frame_at=cuts(ents), motion=kid_m, reveal=iris(KID_BOX),
           seed=71)

    # ---- the picture: on the wall at GK0, alive from t_alive, then zoomed to full screen
    def frozen(t):
        return t < t_alive

    def g_rock(t):
        if frozen(t):
            return Tf(px=GB[0], py=GB[1])
        a = M.progress(t, t_alive, t_alive + 1.0, "sine")
        s1 = M.progress(t, t_hao[0] - 0.05, t_hao[0] + 0.5, "sine")
        s2 = M.progress(t, t_hao[1] - 0.05, t_hao[1] + 0.5, "sine")
        amp_r = 1.0 + 2.4 * s1 + 2.6 * s2
        amp_y = 3.0 + 5 * s1 + 5 * s2
        per = 4.2 - 1.2 * s1 - 0.6 * s2
        ph_ = (t - t_alive) / per
        lurch = 0.0
        for tk, amp in ((t_daa[0], 4.0), (t_daa[1], 6.0)):
            u = t - tk
            if -0.15 <= u < 0.9:
                lurch += amp * math.sin(math.pi * min(1.0, (u + 0.15) / 0.5)) * math.exp(-max(0.0, u) / 0.5)
        return Tf(rot=a * (amp_r * math.sin(2 * math.pi * ph_) - lurch), dy=a * amp_y * math.sin(2 * math.pi * ph_ + 1.1),
                  px=GB[0], py=GB[1])

    def gz(inner=None):
        """Motion of a picture layer: inner motion (picture coords), then the zoom from the wall to the screen."""
        def m(t):
            z = zoom_about(kz(t), ZOOM_P)
            return compose(z, inner(t)) if inner else z
        return m

    def g_iris(box=GBOX):
        """The opening iris expressed in the picture's own (unzoomed) coordinates (it is at GK0 then)."""
        x0, y0, x1, y1 = box
        cx = ZOOM_P[0] + (IRIS_C[0] - ZOOM_P[0]) / GK0
        cy = ZOOM_P[1] + (IRIS_C[1] - ZOOM_P[1]) / GK0
        return iris_reveal(box, cx, cy, lambda t: None if radius(t) is None else radius(t) / GK0, soft=90 / GK0)

    def with_alpha(m, a):
        return lambda t: (lambda tf: Tf(tf.dx, tf.dy, tf.rot, tf.sx, tf.sy, tf.alpha * a(t), tf.px, tf.py))(m(t))

    # storm crossfades on the two '好'
    def st_a(t):
        return 1 - M.progress(t, t_hao[0] - 0.05, t_hao[0] + 0.3, "sine")

    def st_b(t):        # stays opaque under C until C is opaque itself (no see-through crossfade)
        return M.progress(t, t_hao[0] - 0.05, t_hao[0] + 0.3, "sine") * (1.0 if t < t_hao[1] + 0.32 else 0.0)

    def st_c(t):
        return M.progress(t, t_hao[1], t_hao[1] + 0.3, "sine")

    def lph(t):
        return float(int(t / 0.075) % LPH)

    ZG = 150
    sc.add("swg_sky_a", g_sky_a_svg(), z=ZG, motion=with_alpha(gz(), lambda t: 1.0 if st_a(t) > 0.001 or t < t_hao[0] else 0.0),
           reveal=g_iris(), wc=0.6)
    sc.add("swg_water_a", g_water_a_svg(), z=ZG + 0.1, motion=with_alpha(gz(), lambda t: 1.0 if t < t_hao[0] + 0.35 else 0.0),
           reveal=g_iris(), wc=0.7)
    sc.add("swg_ripples", [g_ripples_svg(k) for k in range(6)] + [g_ripples_svg(0)], z=ZG + 0.2,
           motion=with_alpha(gz(), lambda t: 1.0 if t < t_hao[0] + 0.35 else 0.0), reveal=g_iris(), wc=0.3,
           frame_at=lambda t: 0.0 if frozen(t) else ((t - t_alive) / 0.42) % 6)
    # the storm sky: gradient, three cloud banks drifting at their own speeds (each a seamless tile drawn twice),
    # wind streaks; the lowest, darkest bank rolls in on the second '好大'
    st_bc = lambda t: M.progress(t, t_hao[0] - 0.05, t_hao[0] + 0.3, "sine")   # noqa: E731
    sc.add("swg_sbase", g_storm_base_svg(), z=ZG + 0.3, motion=with_alpha(gz(), st_bc), wc=0.6)
    t_s0 = t_hao[0] - 0.1

    def drift(v, c):
        def m(t):
            d = (v * max(0.0, t - t_s0) + 300) % W
            return Tf(dx=d - c * W)
        return m
    for b in range(3):
        bank = g_bank_svg(b)
        af = st_bc if b < 2 else st_c
        for c in range(2):
            sc.add(f"swg_bank{b}_{c}", bank, z=ZG + 0.31 + b * 0.01 + c * 0.001,
                   motion=with_alpha(gz(drift(BANK_V[b], c)), af), wc=0.6, seed=101 + b)
    for c in range(2):
        sc.add(f"swg_streaks{c}", g_streaks_svg(), z=ZG + 0.35 + c * 0.001,
               motion=with_alpha(gz(drift(320, c)), lambda t: 0.5 * st_bc(t) + 0.5 * st_c(t)), wc=0.3)
    for lv, af in ((0, st_b), (1, st_c)):
        sc.add(f"swg_slake_b{lv}", [g_storm_lake_svg(lv, k, "back") for k in range(LPH)], z=ZG + 0.4 + lv * 0.01,
               motion=with_alpha(gz(), af), frame_at=lph, wc=0.6)
    # the boat and the people in it
    calm_on = lambda t: 1.0 if t < snap(t_hao[0] + 0.12) else 0.0          # noqa: E731
    storm_on = lambda t: 1.0 - calm_on(t)                                   # noqa: E731
    bfr = [g_boat_svg("calm", k, "back") for k in range(4)] + [g_boat_svg("storm", k, "back") for k in range(6)]

    def bback_fa(t):
        if frozen(t):
            return 0.0
        if calm_on(t):
            return float(int(t / 0.14) % 4)
        return 4.0 + float(int(t / 0.08) % 6)
    sc.add("swg_boat_back", bfr, z=ZG + 0.5, motion=gz(g_rock), frame_at=bback_fa, reveal=g_iris(), seed=81)
    t_crew = snap(t_daa[0])
    sc.add("swg_far", [g_far_svg("calm"), g_far_svg("storm")], z=ZG + 0.51, motion=gz(g_rock),
           frame_at=lambda t: 1.0 if t >= t_crew else 0.0, reveal=g_iris(), seed=83)
    sc.add("swg_jesus", g_jesus_svg(), z=ZG + 0.52, motion=gz(g_rock), reveal=g_iris(), seed=85)
    nfr = [g_near_svg("calm")] + [g_near_svg("storm", p_ / 6) for p_ in range(6)]

    def near_fa(t):
        if t < t_crew:
            return 0.0
        return 1.0 + float(int((t - t_crew) / 0.11) % 6)
    sc.add("swg_near", nfr, z=ZG + 0.53, motion=gz(g_rock), frame_at=near_fa, reveal=g_iris(), seed=87)
    ffr = [g_boat_svg("calm", 0, "front"), g_boat_svg("storm", 0, "front")]
    sc.add("swg_boat_front", ffr, z=ZG + 0.54, motion=gz(g_rock), frame_at=lambda t: 0.0 if calm_on(t) else 1.0,
           reveal=g_iris(), seed=89)
    sc.add("swg_strip", g_strip_a_svg(), z=ZG + 0.55, motion=with_alpha(gz(), lambda t: 1.0 if t < t_hao[0] + 0.32 else 0.0),
           reveal=g_iris(), wc=0.5)
    for lv, af in ((0, st_b), (1, st_c)):
        sc.add(f"swg_slake_f{lv}", [g_storm_lake_svg(lv, k, "front") for k in range(LPH)], z=ZG + 0.6 + lv * 0.01,
               motion=with_alpha(gz(), af), frame_at=lph, wc=0.6)
    # foam thrown over the bow on the two '大'
    for i, (tk, big) in enumerate(zip(t_daa, (1.0, 1.35))):
        piv = (GB[0] + 640 * GB[2], GB[1] - 200 * GB[2])

        def sp_m(t, tk=tk, piv=piv):
            u = t - (tk - 0.06)
            if u < 0 or u > 0.9:
                return Tf(alpha=0)
            grow = M.ease("out")(min(1.0, u / 0.22))
            a = min(1.0, u / 0.06) * (1 - M.progress(u, 0.35, 0.9, "sine"))
            inner = Tf(sx=0.35 + 0.75 * grow, sy=0.3 + 0.8 * grow, dy=40 * max(0.0, u - 0.3) ** 2 * 4, alpha=a,
                       px=piv[0], py=piv[1])
            return compose(gz(g_rock)(t), inner)
        sc.add(f"swg_splash{i}", g_splash_svg(big), z=ZG + 0.65, motion=sp_m, wc=0.3)
    # the night dims the picture on the wall; it lights up when it comes alive
    sc.add("swg_dim", g_dim_svg(), z=ZG + 0.8, wc=0, reveal=g_iris(),
           motion=with_alpha(gz(), lambda t: 0.34 * (1 - M.progress(t, t_glow - 0.1, t_glow + 0.5, "sine"))))
    sc.add("sw_fglow", frame_glow_svg(), z=ZG - 1, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=room_on(t) * M.progress(t, t_glow - 0.2, t_glow + 0.4, "sine")
                               * (1 - M.progress(t, tz0, tz0 + 0.5, "sine")) * (0.85 + 0.15 * math.sin(t * 5))))

    def border_m(t):
        k = kz(t) / GK0
        return Tf(sx=k, sy=k, px=ZOOM_P[0], py=ZOOM_P[1], alpha=1.0 if t < tz1 - 0.05 else 0.0)
    sc.add("sw_border", frame_border_svg(), z=ZG + 0.9, motion=border_m, reveal=iris((int(FX0 - 40), int(FY0 - 40),
                                                                                     int(FX0 + FRW + 40),
                                                                                     int(FY0 + FRH + 40))), seed=91)

    # ---- effects: the night tint over the room, sparkles as the picture comes alive, spray, rain
    night = lambda t: 0.16 * M.progress(t, t_iris, t_iris_end, "sine") * (1 - M.progress(t, tz0, tz1 - 0.3, "sine"))  # noqa
    sc.fx = list(fx_title)
    sc.fx.append(FX.tint((150, 160, 215), night, mode="multiply"))
    sc.fx.append(FX.rain(t0=t_hao[1] - 0.1, t1=T + 1.0, density=0.55, angle=20, length=40, speed=1500,
                         color=(214, 224, 236), alpha=95, width=2, seed=7))
    sc.fx.append(FX.sparkles((FX0 - 20, FY0 - 20, FX0 + FRW + 20, FY0 + FRH + 20), count=10, t0=t_glow - 0.1,
                             t1=tz0 + 0.3, size=(9, 17), period=1.2, drift=-10, seed=93))

    # ---- camera: s01's push continues; the room; glide toward the picture; through the zoom to the full page
    c_end = cam_title(1.0)
    c_room = Cam(1120, 606, 1960)
    c_pic = Cam(905, 520, 1790)
    c_full = Cam(W / 2, H / 2, W * 0.955)

    def kick(t):
        dx, dy = shake_beats(t, 2.5)
        return dx, dy
    cam_room = M.cam_keys([(1.0, c_end), (t_iris_end + 0.3, c_room), (t_hu[0], Cam(1150, 600, 1900)),
                           (t_fear0, Cam(1180, 610, 1820)), (t_today - 0.1, Cam(1170, 606, 1830)),
                           (tz0 + 0.1, c_pic)], ["sine"] * 5)
    cam_zoom = M.cam_keys([(tz0 + 0.1, c_pic), (tz1, c_full), (T, Cam(W / 2 + 20, H / 2 + 6, W * 0.92))],
                          ["inout", "sine"])

    def camera(t):
        if t <= 1.0:
            return cam_title(t)
        c = cam_room(t) if t < tz0 + 0.1 else cam_zoom(t)
        dx, dy = kick(t)
        return Cam(c.x + dx, c.y + dy, c.w, c.rot)
    sc.camera = camera

    # ---- sound
    sc.sfx("wind_soft", t_iris - 0.2, dur=tz1 - t_iris + 0.6, gain_db=-19, fade_in=0.6, fade_out=0.8)
    sc.sfx("storm_wind", t_hu[0] - 0.3, dur=t_kg[1] + 0.8 - t_hu[0], gain_db=-17, fade_in=0.2, fade_out=1.0)
    for i, tk in enumerate(t_hu):
        sc.sfx("whoosh", tk - 0.05, gain_db=-13 + i, pan=0.4)
    sc.sfx("cloth", t_hu[0], gain_db=-17, pan=0.5)
    for tk in t_kg:
        sc.sfx("hammer", tk - 0.01, dur=0.22, gain_db=-12, pan=0.45)
    sc.sfx("sparkle", t_glow, gain_db=-15, pan=-0.3)
    sc.sfx("chime", t_glow + 0.1, gain_db=-15)
    sc.sfx("whoosh", tz0 + 0.2, gain_db=-14)
    sc.sfx("waves_calm", tz0 + 0.3, dur=t_hao[0] - tz0 + 0.3, gain_db=-17, fade_in=0.6, fade_out=0.4)
    sc.sfx("waves_storm", t_hao[0] - 0.1, dur=T - t_hao[0] + 0.4, gain_db=-17, fade_in=0.3, fade_out=1.2)
    sc.sfx("storm_wind", t_hao[0] - 0.1, dur=T - t_hao[0] + 0.4, gain_db=-20, fade_in=0.4, fade_out=1.2)
    sc.sfx("rain", t_hao[1], dur=T - t_hao[1] + 0.4, gain_db=-26, fade_in=0.6, fade_out=1.2)
    sc.sfx("splash", t_daa[0] - 0.05, gain_db=-13, pan=0.3)
    sc.sfx("splash", t_daa[1] - 0.05, gain_db=-10, pan=0.35)
    return sc
