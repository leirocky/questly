"""Scene 2 — the opening question to the child: "have you ever seen really big rain?" A little child in a yellow
raincoat stands on tiptoe at a big window watching the rain (drops racing down the glass, puddles rippling in the
garden); the rain grows on each 哗啦啦; then we go through the window and the whole page fills with rain; a
picture-book day counter jumps to forty.

Beats (phrase onsets measured in the voice clip, see s01_title.voice_marks; nothing hard-coded to the take):
  0 .. 1.0     s01's title page, continued exactly (title_page(..., toff)): the plain cross-dissolve between the two
               scenes blends identical pictures; the title lettering then fades
  '小朋友'      a round page-iris opens on the cosy window: the child on tiptoe at the sill, amazed, rain outside
  '哗啦啦' x2   on each one the rain steps up (light -> heavy -> pouring), a big '哗啦啦' sound word pops up on the
               glass, the child bobs on her toes; the puddles ripple faster; rain sfx layers swell
  line 1       '今天的故事里' -> we push through the window (the room grows past the frame and fades): the page is
               the rainy garden, rain everywhere; '好大好大的雨' -> pouring rain, rings in the puddles
  '下了多久呢'  a picture-book counter card pops up: a big number and four rows of ten suns
  '整整四十天'  the count runs up and lands on 40 (all forty suns filled) with a bounce and a sparkle
  end          calm hold on the rainy page with the 40-day card (page dip to s03)
"""
import math
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes import s01_title as T1
from stories.noah.scenes.s01_title import char_times, cuts, dip, f1, snap, voice_marks

INK = P["ink"]
WIN = (900, 120, 1900, 752)         # window opening x0, y0, x1, sill top
MULL_X, MULL_Y = 1400, 430           # mullions
PIV = (1400, 436)                    # zoom-through pivot (window centre)
KID = (820, 1046, 2.0)                # child anchor (peek_window: hands on the sill)
FLOOR_Y = 960
CARD = (1056, 560)                   # day counter card centre
CARD_W, CARD_H = 1040, 610
NUM_Y = 452
ROWS_Y = (560, 622, 684, 746)
ROW_S = 1.2
RAIN_LV = (0.45, 0.85, 1.35)
RAIN_PH = 6


def doc(body, defs=""):
    return S.svg_doc(body, defs)


C.EXPRS.setdefault("n2_blink_amazed", dict(C.EXPRS["amazed"], eyes="closed"))
C.EXPRS.setdefault("n2_blink_laugh", dict(C.EXPRS["laugh"], eyes="closed"))


# ================================================================== outside (full page, seen through the window)

def outside_svg():
    defs = (S.lin_grad("n2sky", [(0, "#7f90a6"), (0.45, "#a3b2c0"), (1, "#c9d2d4")]) +
            S.lin_grad("n2grass", [(0, "#86a666"), (1, "#5f8650")]))
    b = S.rect_bg("url(#n2sky)")
    # soft rain clouds
    cl = ""
    for cx, cy, w, h, sd in ((300, 150, 620, 170, 1), (1100, 90, 760, 190, 2), (1850, 170, 640, 170, 3),
                             (700, 300, 420, 110, 4), (1560, 320, 460, 120, 5)):
        cl += S.cloud(cx, cy, w, h, "#9aa8b9", seed=sd + 40, sw=3, shade_fill="#7d8b9e")
    b += S.g(cl, filter="wobble", opacity=0.95)
    # misty far hills and little houses with warm windows
    far = S.path(S.hill(-200, W + 200, 600, 90, seed=5, bumps=4), fill="#9fb2b0", sw=2.2)
    houses = ""
    for x, y, w, h, roof, wall in ((380, 585, 150, 110, "#9a6a5a", "#d9cbb4"), (560, 600, 120, 90, "#7f6a8a", "#d6c6b0"),
                                   (1500, 588, 160, 115, "#a0694e", "#dccdb4"), (1700, 598, 120, 92, "#6f7f8a", "#d4c4ac"),
                                   (1880, 590, 140, 104, "#9a6a5a", "#d9cbb4")):
        houses += (f'<rect x="{x - w / 2}" y="{y - h}" width="{w}" height="{h}" fill="{wall}" stroke="{INK}" '
                   f'stroke-width="3"/>'
                   f'<path d="M{x - w / 2 - 16},{y - h} L{x},{y - h - h * 0.62} L{x + w / 2 + 16},{y - h} Z" '
                   f'fill="{roof}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                   f'<rect x="{x - w * 0.28}" y="{y - h * 0.68}" width="{w * 0.2}" height="{h * 0.26}" fill="#f6d68c" '
                   f'stroke="{INK}" stroke-width="2.5"/>'
                   f'<rect x="{x + w * 0.1}" y="{y - h * 0.68}" width="{w * 0.2}" height="{h * 0.26}" fill="#f6d68c" '
                   f'stroke="{INK}" stroke-width="2.5"/>'
                   f'<rect x="{x - w * 0.08}" y="{y - h * 0.4}" width="{w * 0.16}" height="{h * 0.4}" fill="#8a5a3c" '
                   f'stroke="{INK}" stroke-width="2.5"/>')
    b += S.g(far, filter="wobble") + PR._haze(S.g(houses, filter="wobble-fine"), "#a9b8bf", 0.35, 0.4)
    # the garden
    d = S.smooth_path([(-100, 640), (400, 628), (900, 640), (1400, 632), (1900, 645), (W + 100, 636)], closed=False)
    b += S.path(d + f" L{W + 100},{H + 60} L-100,{H + 60} Z", fill="url(#n2grass)", sw=3.5)
    # path of wet stones winding to the front
    path_d = "M1240,640 C1180,720 1320,800 1200,900 C1080,1000 1180,1120 1100,1220 L1420,1220 C1460,1100 1360,990 1460,900 C1560,800 1400,720 1300,640 Z"
    b += S.path(path_d, fill="#b7ab98", sw=3)
    rng = random.Random(3)
    stones = ""
    for _ in range(26):
        u = rng.uniform(0, 1)
        y = 650 + u * 560
        cx = 1270 + 70 * math.sin(u * 5.5) + rng.uniform(-60, 60) * (0.4 + u)
        r = 10 + 22 * u
        stones += (f'<ellipse cx="{f1(cx)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r * 0.7)}" fill="#cfc4b2" '
                   f'stroke="{INK}" stroke-width="2"/>')
    b += S.g(stones, filter="wobble-fine", opacity=0.9)
    # fence
    fence = ""
    for x in range(-20, W + 40, 70):
        if 1180 < x < 1380:
            continue
        fence += (f'<path d="M{x},700 L{x},610 L{x + 14},594 L{x + 28},610 L{x + 28},700 Z" fill="#e8dcc0" '
                  f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    fence += (f'<rect x="-40" y="630" width="1230" height="14" fill="#ddd0b2" stroke="{INK}" stroke-width="2.5"/>'
              f'<rect x="1380" y="630" width="{W - 1340}" height="14" fill="#ddd0b2" stroke="{INK}" stroke-width="2.5"/>')
    b += S.g(fence, filter="wobble-fine")
    # a round tree, bushes and drooping flowers
    trees = (f'<path d="M560,720 L548,500 L585,500 L590,720 Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="3.5"/>' +
             S.cloud(568, 450, 360, 260, "#6f9a5a", seed=61, puffs=5, sw=3.5, shade_fill="#56804a"))
    trees += S.cloud(1960, 520, 300, 210, "#6a9456", seed=62, puffs=4, sw=3.5, shade_fill="#527a46")
    trees += f'<path d="M1950,720 L1942,560 L1972,560 L1978,720 Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="3.5"/>'
    b += S.g(trees, filter="wobble")
    b += PR.bush(180, 760, 1.0, variant=1) + PR.bush(860, 740, 0.8, variant=0) + PR.bush(1700, 760, 0.95, variant=3)
    fl = ""
    for x, y, s in ((300, 1000, 1.2), (700, 960, 1.1), (1700, 1010, 1.2), (2000, 960, 1.0), (60, 900, 0.9),
                    (980, 820, 0.8)):
        fl += PR.grass_tuft(x, y, s, variant=2, sway=0.6)
    b += fl
    return doc(b, defs)


PUDDLES = [(1010, 712, 0.75, 240), (1620, 706, 0.6, 220), (560, 1010, 1.25, 300), (1680, 1060, 1.15, 300),
           (1290, 860, 0.9, 200)]


def puddle_svg(i, k):
    x, y, s, w = PUDDLES[i]
    return doc(PR.puddle(x, y, s, width=w, ripple=k / 4, sky="#b4c2cc"))


def rain_svg(level, ph):
    return doc(PR.rain(ph / RAIN_PH, RAIN_LV[level], 0, 0, W, H, angle=8, seed=level * 3 + 1))


# ================================================================== the room (overlay with the window hole)

def wall_svg():
    x0, y0, x1, y1 = WIN
    defs = (S.lin_grad("n2wall", [(0, "#efd6b4"), (1, "#f4e2c4")]) +
            S.lin_grad("n2floor", [(0, "#b98455"), (1, "#9c6b42")]))
    outer = f"M-40,-40 L{W + 40},-40 L{W + 40},{H + 40} L-40,{H + 40} Z"
    hole = f"M{x0},{y0} L{x0},{y1} L{x1},{y1} L{x1},{y0} Z"
    b = f'<path d="{outer} {hole}" fill="url(#n2wall)" fill-rule="evenodd"/>'
    for x in range(-40, W + 60, 110):
        b += (f'<path d="M{x},-40 L{x},{FLOOR_Y} " stroke="#e6c79f" stroke-width="40" opacity="0.45" '
              f'clip-path="url(#n2wc)"/>')
    defs += f'<clipPath id="n2wc"><path d="{outer} {hole}" clip-rule="evenodd"/></clipPath>'
    # small flowers on the wallpaper
    for i, x in enumerate(range(55, W, 110)):
        for j, y in enumerate(range(70 + (i % 2) * 70, FLOOR_Y - 60, 140)):
            if x0 - 30 < x < x1 + 30 and y0 - 30 < y < y1 + 60:
                continue
            b += (f'<circle cx="{x}" cy="{y}" r="7" fill="#f2b9a0" opacity="0.8"/>'
                  f'<circle cx="{x}" cy="{y}" r="2.5" fill="#e79b6b" opacity="0.9"/>')
    # skirting board and floor
    b += (f'<rect x="-40" y="{FLOOR_Y}" width="{W + 80}" height="{H - FLOOR_Y + 60}" fill="url(#n2floor)"/>'
          f'<rect x="-40" y="{FLOOR_Y - 24}" width="{W + 80}" height="26" fill="#d8b48a" stroke="{INK}" '
          f'stroke-width="3"/>')
    for x in range(-40, W + 60, 180):
        b += f'<path d="M{x},{FLOOR_Y + 2} L{x - 60},{H + 40}" stroke="#8a5d3a" stroke-width="3" opacity="0.6"/>'
    b += f'<ellipse cx="760" cy="1080" rx="560" ry="74" fill="#d9776a" stroke="{INK}" stroke-width="3.5"/>'
    b += '<ellipse cx="760" cy="1080" rx="490" ry="56" fill="none" stroke="#f2c38f" stroke-width="8" stroke-dasharray="20 14"/>'
    deco = wall_deco()
    return doc(S.g(b, filter="wobble") + deco, defs)


def wall_deco():
    """A child's rainbow drawing pinned to the wall, a coat hook with a polka-dot umbrella."""
    x, y, w, h = 300, 210, 300, 230
    b = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fbf4e2" stroke="{INK}" stroke-width="4" '
         f'transform="rotate(-4 {x + w / 2} {y + h / 2})"/>')
    cols = ("#e8706a", "#f0a050", "#f2d45c", "#8cc56a", "#6aaee0", "#9a84cf")
    g_ = ""
    for i, c in enumerate(cols):
        r = 112 - 13 * i
        g_ += (f'<path d="M{x + w / 2 - r},{y + h - 40} A{r},{r} 0 0 1 {x + w / 2 + r},{y + h - 40}" stroke="{c}" '
               f'stroke-width="12" fill="none" stroke-linecap="round"/>')
    g_ += S.cloud(x + w / 2 - 100, y + h - 44, 80, 34, "#ffffff", seed=3, puffs=3, sw=2.5)
    g_ += S.cloud(x + w / 2 + 100, y + h - 44, 80, 34, "#ffffff", seed=4, puffs=3, sw=2.5)
    b += f'<g transform="rotate(-4 {x + w / 2} {y + h / 2})">{g_}</g>'
    b += f'<circle cx="{x + w / 2 - 6}" cy="{y + 8}" r="9" fill="#e45c5c" stroke="{INK}" stroke-width="2.5"/>'
    # coat hook + umbrella
    hx, hy = 470, 560
    b += (f'<rect x="{hx - 70}" y="{hy - 16}" width="140" height="24" rx="8" fill="#b07a48" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M{hx},{hy} q0,26 -16,30" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    ux, uy = hx - 16, hy + 30
    b += (f'<path d="M{ux},{uy} q-24,-4 -26,18 L{ux - 26},{uy + 230}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
          f'<path d="M{ux - 26},{uy + 40} C{ux - 90},{uy + 120} {ux - 70},{uy + 200} {ux - 40},{uy + 235} L{ux - 10},{uy + 235} '
          f'C{ux + 30},{uy + 200} {ux + 40},{uy + 120} {ux - 26},{uy + 40} Z" fill="#5aa6c8" stroke="{INK}" stroke-width="4" '
          f'stroke-linejoin="round"/>')
    for dx, dy in ((-48, 120), (-20, 160), (2, 110), (-40, 190), (-14, 210)):
        b += f'<circle cx="{ux + dx}" cy="{uy + dy}" r="7" fill="#fbf4e2"/>'
    return S.g(b, filter="wobble-fine")


def frame_svg():
    x0, y0, x1, y1 = WIN
    fw = 34
    wood, dark = "#c99662", "#a0703f"
    b = ""
    # frame and mullions
    b += (f'<path d="M{x0 - fw},{y0 - fw} L{x1 + fw},{y0 - fw} L{x1 + fw},{y1} L{x0 - fw},{y1} Z '
          f'M{x0},{y0} L{x0},{y1} L{x1},{y1} L{x1},{y0} Z" fill="{wood}" fill-rule="evenodd" stroke="{INK}" '
          f'stroke-width="4"/>')
    b += (f'<rect x="{MULL_X - 12}" y="{y0}" width="24" height="{y1 - y0}" fill="{wood}" stroke="{INK}" stroke-width="3.5"/>'
          f'<rect x="{x0}" y="{MULL_Y - 11}" width="{x1 - x0}" height="22" fill="{wood}" stroke="{INK}" stroke-width="3.5"/>')
    b += f'<path d="M{x0 - fw + 6},{y0 - fw + 8} L{x1 + fw - 6},{y0 - fw + 8}" stroke="#e2b984" stroke-width="5"/>'
    # sill board
    b += (f'<path d="M{x0 - 70},{y1 - 6} L{x1 + 70},{y1 - 6} L{x1 + 56},{y1 + 30} L{x0 - 56},{y1 + 30} Z" '
          f'fill="#d8a873" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
          f'<path d="M{x0 - 56},{y1 + 30} L{x1 + 56},{y1 + 30} L{x1 + 56},{y1 + 44} L{x0 - 56},{y1 + 44} Z" '
          f'fill="{dark}" stroke="{INK}" stroke-width="3.5"/>')
    # curtains, tied back
    for side in (-1, 1):
        cx = x0 - fw - 40 if side < 0 else x1 + fw + 40
        top = y0 - 80
        pts = [(cx - 70, top), (cx + 70, top), (cx + 60 * side + 30, y1 - 280), (cx + 40 * side, y1 - 210),
               (cx + 30, y1 + 120), (cx - 30, y1 + 120), (cx - 40 * side, y1 - 210), (cx + 60 * side - 30, y1 - 280)]
        b += S.path(S.smooth_path(pts), fill="#e9a6a0", sw=4)
        for k in (-35, 0, 35):
            b += f'<path d="M{cx + k},{top + 20} Q{cx + k + 30 * side},{y1 - 300} {cx + k * 0.4},{y1 + 100}" stroke="#d48a86" stroke-width="5" fill="none"/>'
        b += (f'<ellipse cx="{cx + 38 * side}" cy="{y1 - 222}" rx="26" ry="16" fill="#f2d27a" stroke="{INK}" '
              f'stroke-width="3"/>')
    b += (f'<rect x="{x0 - 160}" y="{y0 - 104}" width="{x1 - x0 + 320}" height="20" rx="10" fill="{dark}" '
          f'stroke="{INK}" stroke-width="3.5"/>')
    # on the sill: a potted plant and a little toy ark
    px, py = x1 - 120, y1 - 6
    pot = (f'<path d="M{px - 40},{py - 70} L{px + 40},{py - 70} L{px + 30},{py} L{px - 30},{py} Z" fill="{P["terracotta"]}" '
           f'stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    for a in (-40, -15, 10, 35):
        r = math.radians(a - 90)
        ex, ey = px + 70 * math.cos(r), py - 70 + 70 * math.sin(r)
        pot += (f'<path d="M{px},{py - 70} Q{f1((px + ex) / 2 - 10)},{f1((py - 70 + ey) / 2)} {f1(ex)},{f1(ey)} '
                f'Q{f1((px + ex) / 2 + 14)},{f1((py - 70 + ey) / 2 + 10)} {px},{py - 70} Z" fill="#7fae5a" '
                f'stroke="{INK}" stroke-width="2.5"/>')
    b += pot
    toy = PR.ark(x1 - 330, y1 - 8, 0.085, -1, ramp=False, door=0.0)
    return doc(S.g(b, filter="wobble-fine") + toy)


def glass_svg():
    x0, y0, x1, y1 = WIN
    b = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#dfeaf0" opacity="0.10"/>'
    for (ax, ay) in ((x0 + 60, y0 + 40), (MULL_X + 50, y0 + 40)):
        b += (f'<path d="M{ax},{ay + 140} L{ax + 140},{ay} L{ax + 175},{ay} L{ax + 35},{ay + 140} Z" fill="#ffffff" '
              f'opacity="0.13"/>')
    return doc(b)


def room_svg():
    """Wall, glass sheen and window frame in one layer (they always move together)."""
    def body(svg):
        return svg[svg.index("</defs>") + 7:svg.rindex("</svg>")]

    def defs(svg):
        return svg[svg.index("<defs>") + 6:svg.index("</defs>")].replace(S.svg_doc("")[S.svg_doc("").index("<defs>") + 6:S.svg_doc("").index("</defs>")], "")
    parts = [wall_svg(), glass_svg(), frame_svg()]
    return doc("".join(body(p) for p in parts), "".join(defs(p) for p in parts))


def kid_svg(expr):
    x, y, s = KID
    return doc(C.ground_shadow(x + 10, y + 2, s, 100, 0.2) + C.child(x, y, s, 1, pose="peek_window", expr=expr))


def word_svg(x, y, rot, size=118):
    defs = S.lin_grad("n2wg", [(0, "#7cc3e6"), (1, "#3b86b8")])
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    tr = f'transform="rotate({rot} {x} {y})"'
    b = (f'<g {tr}><text x="{x}" y="{y}" {font} fill="#fffaf0" stroke="#fffaf0" stroke-width="22" '
         f'stroke-linejoin="round">哗啦啦！</text>'
         f'<text x="{x}" y="{y}" {font} fill="url(#n2wg)" stroke="{INK}" stroke-width="4" '
         f'stroke-linejoin="round">哗啦啦！</text></g>')
    # little drops flying off the word
    for dx, dy, r in ((-260, -80, 14), (250, -96, 12), (290, -20, 9), (-300, -10, 10)):
        cx, cy = x + dx, y + dy
        b += (f'<path d="M{cx},{cy - r * 1.8} Q{cx + r},{cy - r * 0.2} {cx},{cy + r} Q{cx - r},{cy - r * 0.2} '
              f'{cx},{cy - r * 1.8} Z" fill="#bfe3f2" stroke="{INK}" stroke-width="3" transform="rotate({rot} {x} {y})"/>')
    return doc(b, defs)


# ================================================================== the counter card

def card_svg():
    cx, cy = CARD
    x0, y0 = cx - CARD_W / 2, cy - CARD_H / 2
    b = (f'<rect x="{x0 + 10}" y="{y0 + 16}" width="{CARD_W}" height="{CARD_H}" rx="40" fill="{INK}" opacity="0.28" '
         f'filter="url(#soft)"/>'
         f'<rect x="{x0}" y="{y0}" width="{CARD_W}" height="{CARD_H}" rx="40" fill="#fffaf0" stroke="{INK}" '
         f'stroke-width="5"/>'
         f'<rect x="{x0 + 18}" y="{y0 + 18}" width="{CARD_W - 36}" height="{CARD_H - 36}" rx="28" fill="#f3ead2" '
         f'stroke="{INK}" stroke-width="3" stroke-dasharray="14 10"/>')
    # a little cloud with drops in the top corners
    for sx in (x0 + 120, x0 + CARD_W - 120):
        b += S.cloud(sx, y0 + 96, 120, 50, "#c3ccd8", seed=int(sx), puffs=3, sw=3, shade_fill="#a4afbe")
        for k in range(3):
            dx = sx - 30 + 30 * k
            dy = y0 + 150 + 12 * (k % 2)
            b += (f'<path d="M{dx},{dy - 12} Q{dx + 8},{dy} {dx},{dy + 8} Q{dx - 8},{dy} {dx},{dy - 12} Z" '
                  f'fill="#9fd0e6" stroke="{INK}" stroke-width="2"/>')
    return doc(S.g(b, filter="wobble-fine"))


def day_word_svg():
    cx = CARD[0]
    return doc(S.text(cx + 90, NUM_Y, "天", size=120, anchor="start", fill="#5a7fa8",
                      extra=f'stroke="{INK}" stroke-width="3.5" paint-order="stroke"'))


def number_svg(n):
    if n == 0:
        n = "?"
    cx = CARD[0] + 70
    font = 'font-family="LXGW WenKai" font-weight="bold" font-size="190" text-anchor="end"'
    defs = S.lin_grad("n2ng", [(0, "#ec8a45"), (1, "#c2552a")])
    b = (f'<text x="{cx}" y="{NUM_Y + 8}" {font} fill="#fffaf0" stroke="#fffaf0" stroke-width="18" '
         f'stroke-linejoin="round">{n}</text>'
         f'<text x="{cx}" y="{NUM_Y + 8}" {font} fill="url(#n2ng)" stroke="{INK}" stroke-width="4" '
         f'stroke-linejoin="round">{n}</text>')
    return doc(b, defs)


def row_svg(filled):
    return doc(PR.day_counter(CARD[0], ROWS_Y[0], ROW_S, n=10, filled=filled, icons="sun", gap=64))


# ================================================================== glass drops (procedural)

class GlassDrops:
    def __init__(self, seed=7):
        rng = np.random.default_rng(seed)
        x0, y0, x1, y1 = WIN
        n = 18
        xs = []
        while len(xs) < n:
            x = rng.uniform(x0 + 20, x1 - 20)
            if abs(x - MULL_X) > 30:
                xs.append(x)
        self.x = np.array(xs)
        self.r = rng.uniform(8, 14, n)
        self.v = rng.uniform(70, 170, n)
        self.ph = rng.uniform(0, 1, n)
        self.wob = rng.uniform(0, 6.28, n)
        self.dots = [(rng.uniform(x0 + 10, x1 - 10), rng.uniform(y0 + 10, y1 - 10), rng.uniform(2.5, 5.5))
                     for _ in range(70)]
        self.box = (x0, y0, x1, y1)

    def __call__(self, t, alpha=1.0):
        if alpha <= 0.01:
            return None
        x0, y0, x1, y1 = self.box
        k = 2
        w, h = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        a = alpha
        for (dx, dy, r) in self.dots:
            X, Y = (dx - x0) * k, (dy - y0) * k
            d.ellipse([X - r * k, Y - r * k, X + r * k, Y + r * k], fill=(232, 242, 247, int(120 * a)),
                      outline=(110, 128, 146, int(90 * a)), width=2)
        span = (y1 - y0) + 60
        for i in range(len(self.x)):
            # stop-and-go racing: speed pulses
            s = self.v[i] * (t + 0.35 * math.sin(2 * math.pi * (t / 1.7 + self.ph[i])))
            y = (self.ph[i] * span + s) % span - 30
            x = self.x[i] + 4 * math.sin(y / 60 + self.wob[i])
            r = self.r[i]
            X, Y = (x - x0) * k, (y - y0) * k
            tl = min(y - y0, 120 + 60 * self.ph[i]) * k
            if tl > 0:
                d.line([(X, Y - tl), (X, Y)], fill=(225, 236, 244, int(90 * a)), width=int(r * 0.9))
            d.ellipse([X - r * k, Y - r * 1.15 * k, X + r * k, Y + r * k], fill=(228, 240, 247, int(200 * a)),
                      outline=(96, 116, 138, int(170 * a)), width=3)
            d.ellipse([X - r * 0.55 * k, Y - r * 0.7 * k, X - r * 0.1 * k, Y - r * 0.25 * k],
                      fill=(255, 252, 244, int(220 * a)))
        arr = cv2.resize(np.asarray(im), (w, h), interpolation=cv2.INTER_AREA)
        # keep the mullions clear
        arr[:, int(MULL_X - 12 - x0):int(MULL_X + 12 - x0), 3] = 0
        arr[int(MULL_Y - 11 - y0):int(MULL_Y + 11 - y0), :, 3] = 0
        return Image.fromarray(arr, "RGBA")


# ================================================================== build

def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    m0 = voice_marks(ctx, 0)
    m1 = voice_marks(ctx, 1)
    t_kid = m0[0][1]
    t_hua = [m[1] for m in m0 if m[0] == "哗啦啦"]
    if len(t_hua) < 2:
        L = ctx.lines[0]
        t_hua = [L.end - 1.6, L.end - 0.7]
    t_line1 = m1[0][1]
    t_how = m1[2][1] if len(m1) > 2 else ctx.lines[1].chunks[-1].start
    forty = m1[3] if len(m1) > 3 else m1[-1]
    fc = char_times(forty)
    t_forty = fc[2] if len(fc) > 2 else forty[1] + 0.4      # '四'
    t_count0 = t_how + 0.35
    t_land = t_forty + 0.12

    # --- the title page from s01, continued (identical picture across the cross-dissolve)
    tl = load_timeline()
    c01 = context("s01_title", tl)
    starts = {s["id"]: s["start"] for s in tl["scenes"]}
    toff = starts[ctx.id] - starts["s01_title"]
    t_iris = max(1.0, t_kid + 0.02)
    t_iris_end = t_iris + 1.1
    page_gate = lambda t: 1.0 if t < t_iris_end + 0.05 else 0.0           # noqa: E731
    title_gate = lambda t: 1.0 - M.progress(t, 1.0, 1.4, "sine")          # noqa: E731
    cam_title, fx_title, _ = T1.title_page(sc, c01, toff, gate=page_gate, title_gate=title_gate)

    def iris(t):
        if t >= t_iris_end:
            return {"mode": "up", "frac": 1.0}
        return {"mode": "radial", "frac": M.progress(t, t_iris, t_iris_end, "sine") * 1.02, "soft": 90,
                "cx": PIV[0], "cy": PIV[1]}
    on = lambda t: 1.0 if t >= t_iris else 0.0                             # noqa: E731

    # --- zoom through the window on line 1
    tz0, tz1 = t_line1 - 0.1, t_line1 + 1.5
    zk = lambda t: M.progress(t, tz0, tz1, "in")                            # noqa: E731

    def room_m(t):
        u = zk(t)
        s = 1.0 + 2.6 * u
        return Tf(sx=s, sy=s, alpha=on(t) * (1 - M.progress(t, tz0 + 0.8, tz1, "sine")), px=PIV[0], py=PIV[1])

    def out_m(t):
        s = 1.0 + 0.1 * zk(t) + 0.012 * max(0.0, t - tz1)
        return Tf(sx=s, sy=s, alpha=on(t), px=PIV[0], py=PIV[1] + 120)

    sc.add("outside", outside_svg(), motion=out_m, reveal=iris, z=20)
    for i in range(len(PUDDLES)):
        sc.add(f"puddle{i}", [puddle_svg(i, k) for k in range(4)], motion=out_m, reveal=iris, z=21, wc=0.5,
               frame_at=lambda t, i=i: float((int(t * (4.0 if t < t_hua[0] else 6.0 if t < t_hua[1] else 9.0)) + i)
                                             % 4))

    # rain: three intensities, stepping up on each 哗啦啦 (a quick 0.2 s swell)
    lv_t = [t_iris, t_hua[0], t_hua[1]]

    def rain_alpha(level):
        def m(t):
            a = M.progress(t, lv_t[level] - 0.05, lv_t[level] + 0.2, "out")
            if level + 1 < 3:
                a *= 1 - M.progress(t, lv_t[level + 1] + 0.15, lv_t[level + 1] + 0.4, "sine")
            return Tf(alpha=a * on(t))
        return m
    for lv in range(3):
        sc.add(f"rain{lv}", [rain_svg(lv, k) for k in range(RAIN_PH)], motion=rain_alpha(lv), reveal=iris,
               z=22 + lv * 0.1, wc=0.25, frame_at=lambda t, lv=lv: float(int(t / 0.06 + lv * 2) % RAIN_PH))

    # the room overlay
    sc.add("room", room_svg(), motion=room_m, reveal=iris, z=30)
    drops = GlassDrops()

    def drops_fn(t):
        if t < t_iris:
            return None
        a = M.progress(t, t_iris + 0.5, t_iris_end, "sine") * (1 - M.progress(t, tz0, tz0 + 0.35, "sine"))
        im = drops(t, a)
        return None if im is None else (im, (WIN[0], WIN[1]))
    sc.add_dynamic("drops", drops_fn, z=31.2)

    # the child on tiptoe: blinks, a little bob on each 哗啦啦 (laughing on the second)
    kx, ky, ks = KID
    kfr = [kid_svg("amazed"), kid_svg("n2_blink_amazed"), kid_svg("laugh"), kid_svg("n2_blink_laugh")]
    c1, c2 = snap(t_hua[0] + 0.05), snap(t_hua[1] + 0.05)
    kents = [(0, 0), (c2, 2)]
    for tb in (t_iris_end + 0.6, t_hua[0] - 0.6, t_line1 - 0.5):
        tb = snap(tb)
        if abs(tb - c2) > 0.4:
            base = 2 if tb > c2 else 0
            kents += [(tb, base + 1), (snap(tb + 0.13), base)]
    kents = sorted(kents)

    def tiptoe(t):
        dy = 0.0
        for th in (c1, c2):
            u = t - th
            if 0 <= u < 0.5:
                dy -= 14 * math.sin(math.pi * u / 0.5) * ks
        return Tf(dy=dy + 2.0 * math.sin(2 * math.pi * t / 2.4))
    sc.add("kid", kfr, frame_at=cuts(kents), reveal=iris, z=32,
           motion=M.combine(room_m, tiptoe, dip(c2, ks, (kx, ky), 6), M.breathe(0.01, 2.6, pivot=(kx, ky))))

    # sound words
    for i, (th, (wx, wy, rot)) in enumerate(zip(t_hua, ((1150, 300, -7), (1640, 560, 6)))):
        t0 = th - 0.04

        def wm(t, t0=t0, wx=wx, wy=wy):
            if t < t0:
                return Tf(alpha=0)
            u = min(1.0, (t - t0) / 0.38)
            s = 0.4 + 0.6 * M.ease("back")(u)
            a = min(1.0, (t - t0) / 0.1) * (1 - M.progress(t, tz0 - 0.2, tz0 + 0.25, "sine"))
            return Tf(sx=s, sy=s, dy=3 * math.sin(2 * math.pi * (t - t0) / 1.1), alpha=a, px=wx, py=wy - 40)
        sc.add(f"word{i}", word_svg(wx, wy, rot), motion=wm, z=33, wc=0)

    # --- the counter card
    ccx, ccy = CARD
    card_m = M.keys([(t_how - 0.01, {"alpha": 0, "s": 0.55, "dy": 40}), (t_how + 0.32, {"alpha": 1, "s": 1.04, "dy": 0}),
                     (t_how + 0.5, {"s": 1.0})], ["out", "sine"], pivot=(ccx, ccy))
    card_bob = lambda t: Tf(dy=3 * math.sin(2 * math.pi * t / 3.2))         # noqa: E731
    cm = M.combine(card_m, card_bob)
    sc.add("card", card_svg(), motion=cm, z=40, wc=0.35)
    sc.add("day_word", day_word_svg(), motion=cm, z=40.2, wc=0)

    def count(t):
        u = M.progress(t, t_count0, t_land, "in")
        return int(round(40 * u)) if t >= t_count0 else 0

    sc.add("number", [number_svg(n) for n in range(41)], z=40.3, wc=0, frame_at=lambda t: float(count(t)),
           motion=M.combine(cm, M.keys([(t_land - 0.02, {"s": 1.0}), (t_land + 0.12, {"s": 1.28}),
                                        (t_land + 0.42, {"s": 1.0})], ["out", "back"], pivot=(ccx - 30, NUM_Y - 60))))
    rows = [row_svg(f) for f in range(11)]
    for r in range(4):
        def rfa(t, r=r):
            return float(min(10, max(0, count(t) - 10 * r)))
        sc.add(f"row{r}", rows, z=40.25, wc=0, frame_at=rfa,
               motion=M.combine(cm, lambda t, r=r: Tf(dy=ROWS_Y[r] - ROWS_Y[0])))

    # --- camera: s01's slow push continues; the room drifts toward the window; wide on the rainy page
    c_end = cam_title(1.0)
    cam_room = M.cam_keys([(1.0, c_end), (t_hua[1] + 0.8, Cam(1140, 560, 1830)), (tz0, Cam(1150, 556, 1800)),
                           (tz1 + 0.6, Cam(W / 2, H / 2, W * 0.96)), (T, Cam(W / 2, H / 2 + 6, W * 0.94))],
                          ["sine", "sine", "sine", "sine"])
    sc.camera = lambda t: cam_title(t) if t <= 1.0 else cam_room(t)
    sc.fx = fx_title

    # --- sound
    sc.sfx("rain", t_iris, dur=T - t_iris + 0.3, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("rain", t_hua[0] - 0.05, dur=T - t_hua[0] + 0.3, gain_db=-19, fade_in=0.25, fade_out=1.0)
    sc.sfx("rain", t_hua[1] - 0.05, dur=T - t_hua[1] + 0.3, gain_db=-17, fade_in=0.25, fade_out=1.0)
    sc.sfx("drip", t_iris, dur=tz1 - t_iris, gain_db=-22, fade_in=0.6, fade_out=0.6)
    for th in t_hua:
        sc.sfx("splash_small", th, gain_db=-15)
    sc.sfx("whoosh", tz0 + 0.3, gain_db=-15)
    sc.sfx("pop", t_how + 0.05, gain_db=-13)
    sc.sfx("pop", t_land, gain_db=-10)
    sc.sfx("sparkle", t_land + 0.05, gain_db=-14)
    return sc
