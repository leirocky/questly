"""Scene 2 — the opening question to the child. A cosy modern room: a little brother is playing with his wooden toy
horse when his big sister grabs it; a tug of war; she wins and he turns away sulking with his arms crossed, a little
storm cloud over his head. Then the picture-book page turns to a hint of today's story: a coat of many colours hanging
on a peg, glowing, and a long road winding away toward Egypt.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers; nothing is
hard-coded to the take):
  0 .. 1.0     s01's title page, continued exactly (title_page(..., toff)): the plain cross-dissolve between the two
               scenes blends identical pictures; then the title lettering fades
  '小朋友'      a round page-iris opens on the room: the little brother holds his toy horse, his sister beside him
  '哥哥姐姐'    she grabs it - a tug of war (squash cut); '欺负过' three hard yanks, one per syllable (cloth whoosh)
  end of the question  she yanks it away and stumbles back hugging it (sly grin); he is left empty-handed (sad)
  '生过别人的气' he turns his back, arms crossed (sulk, squash cut)
  '很久很久'    a little storm cloud pops up over his head and drizzles; on the second '很久' it grumbles with a tiny
               zigzag (soft rumble); the pause holds on the sulk (blinks, breathing, drizzle)
  line 1       '今天的故事里' -> the page turns (a paper curl sweeps right to left) to the hint page: the coat on its
               peg, the road to Egypt; '有一个人被他的哥哥们欺负得好惨' footprints appear one by one along the road
               toward the far pyramids while a cloud shadow dims the page and a gust swings the coat
  '可是后来'    the shadow passes, warm light returns, the coat glows
  '很了不起的事' a sparkle burst on the coat (sparkle + chime); calm golden hold (page dip to s03)

Shared with s14_end: room_body() (the room), sibling_svg(), boxed() / reveal helpers, storm_cloud_svg().
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.joseph.scenes import s01_title as T1
from stories.joseph.scenes.s01_title import blink_name, char_times, cuts, dip, f1, snap, voice_marks

INK = P["ink"]
FLOOR_Y = 905
KS = 1.95                             # the siblings' scale
KY = 1030                             # their ground line (on the rug)
SIS_X, BRO_X = 850, 1142              # tug positions (~150*scale apart)
PIV = (990, 700)                      # iris centre
WIN = (1450, 150, 1900, 640)          # window opening
CLOUD = (BRO_X + 18, 512)             # storm cloud centre (over the brother's head)
# hint page
HOOK = (450, 352)                     # the peg the coat hangs on
POST_X = 330
ROAD_END = (1652, 664)


# ================================================================== helpers (shared with s14)


def boxed(body, box, defs="", w=W, h=H):
    """A layer document whose rasterised crop is exactly ``box`` (x0, y0, x1, y1): two nearly invisible dots mark
    the corners, so reveal masks (computed on the crop) can be expressed in stage coordinates."""
    x0, y0, x1, y1 = box
    dots = (f'<rect x="{x0}" y="{y0}" width="4" height="4" fill="#fffaf0" opacity="0.02"/>'
            f'<rect x="{x1 - 4}" y="{y1 - 4}" width="4" height="4" fill="#fffaf0" opacity="0.02"/>')
    return S.svg_doc(body + dots, defs, w, h)


def iris_reveal(box, cx, cy, radius_fn, soft=90):
    """Radial reveal of a boxed layer: everything within radius_fn(t) stage px of (cx, cy) is visible."""
    x0, y0, x1, y1 = box
    maxd = max(math.hypot(cx - x0, cy - y0), math.hypot(x1 - cx, cy - y0), math.hypot(cx - x0, y1 - cy),
               math.hypot(x1 - cx, y1 - cy))

    def rv(t):
        r = radius_fn(t)
        if r is None:
            return {"mode": "up", "frac": 1.0}
        return {"mode": "radial", "frac": r / maxd, "soft": soft, "cx": cx, "cy": cy}
    return rv


def wipe_reveal(box, edge_fn, soft=6):
    """Page-turn reveal of a boxed layer: visible right of the stage x edge_fn(t) (None = fully visible)."""
    x0, y0, x1, y1 = box

    def rv(t):
        X = edge_fn(t)
        if X is None:
            return {"mode": "up", "frac": 1.0}
        frac = 1 - (X - x0) / (x1 - x0)
        return {"mode": "right", "frac": min(1.0, max(0.0, frac)), "soft": soft}
    return rv


def room_body(oy=0, top=-20, w=W, drawing=True, clock=True):
    """The cosy modern room (wall, window with a garden view, bookshelf, a child's drawing, a clock, floor and rug).
    ``oy`` shifts it down (s14's tall page); the wallpaper runs from ``top`` to the floor. Returns (body, defs)."""
    fy = FLOOR_Y + oy
    x0, y0, x1, y1 = WIN
    y0, y1 = y0 + oy, y1 + oy
    defs = (S.lin_grad("j2wall", [(0, "#f7e6c4"), (1, "#f2d9b0")]) +
            S.lin_grad("j2floor", [(0, "#c08a58"), (1, "#a06e44")]) +
            S.lin_grad("j2sky", [(0, "#9fd0e6"), (1, "#dff0ea")]))
    b = f'<rect x="-20" y="{top}" width="{w + 40}" height="{fy - top + 2}" fill="url(#j2wall)"/>'
    for x in range(-40, w + 60, 120):
        b += f'<rect x="{x}" y="{top}" width="44" height="{fy - top}" fill="#efd5a8" opacity="0.45"/>'
    wall_pat = ""
    for i, x in enumerate(range(40, w, 120)):
        for y in range(int(top) + 60 + (i % 2) * 80, fy - 70, 160):
            if x0 - 60 < x < x1 + 60 and y0 - 140 < y < y1 + 60:
                continue
            wall_pat += (f'<circle cx="{x + 22}" cy="{y}" r="7" fill="#f2b39a" opacity="0.75"/>'
                         f'<circle cx="{x + 22}" cy="{y}" r="2.6" fill="#e48f63" opacity="0.9"/>'
                         f'<path d="M{x + 22},{y + 9} q-6,10 -14,12" stroke="#9fbf7a" stroke-width="3" fill="none" '
                         f'opacity="0.7"/>')
    b += wall_pat
    # garden through the window
    view = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#j2sky)"/>'
            + S.cloud(x0 + 140, y0 + 110, 170, 56, "#fbf6ec", seed=71, sw=3, shade_fill="#d6e6ee")
            + S.cloud(x0 + 360, y0 + 70, 120, 40, "#fbf6ec", seed=72, sw=2.5, shade_fill="#d6e6ee"))
    hill = S.smooth_path([(x0 - 10, y1 - 150), (x0 + 150, y1 - 190), (x0 + 330, y1 - 175), (x1 + 10, y1 - 205)],
                         closed=False) + f" L{x1 + 10},{y1 + 10} L{x0 - 10},{y1 + 10} Z"
    view += S.path(hill, fill="#9fc46e", sw=3)
    view += (f'<path d="M{x1 - 120},{y1 - 150} L{x1 - 126},{y1 - 290} L{x1 - 100},{y1 - 290} L{x1 - 96},{y1 - 150} Z" '
             f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
             + S.cloud(x1 - 112, y1 - 320, 190, 140, "#77a85a", seed=73, puffs=4, sw=3, shade_fill="#5e8d48"))
    for k in range(7):
        fx_ = x0 + 30 + k * 62
        view += (f'<circle cx="{fx_}" cy="{y1 - 60 + 14 * (k % 2)}" r="8" fill="{["#f6d36b", "#f2a6a0", "#fbf3e3"][k % 3]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
    b += S.g(view, filter="wobble-fine")
    # window frame, mullions, sill, curtains
    fw = 30
    wood = "#d0a06a"
    fr = (f'<path d="M{x0 - fw},{y0 - fw} L{x1 + fw},{y0 - fw} L{x1 + fw},{y1} L{x0 - fw},{y1} Z '
          f'M{x0},{y0} L{x0},{y1} L{x1},{y1} L{x1},{y0} Z" fill="{wood}" fill-rule="evenodd" stroke="{INK}" '
          f'stroke-width="4"/>'
          f'<rect x="{(x0 + x1) / 2 - 11}" y="{y0}" width="22" height="{y1 - y0}" fill="{wood}" stroke="{INK}" '
          f'stroke-width="3.5"/>'
          f'<rect x="{x0}" y="{(y0 + y1) / 2 - 10}" width="{x1 - x0}" height="20" fill="{wood}" stroke="{INK}" '
          f'stroke-width="3.5"/>'
          f'<path d="M{x0 - 60},{y1 - 6} L{x1 + 60},{y1 - 6} L{x1 + 46},{y1 + 28} L{x0 - 46},{y1 + 28} Z" '
          f'fill="#e0b07a" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    for (ax, ay) in ((x0 + 40, y0 + 30), ((x0 + x1) / 2 + 40, y0 + 30)):
        fr += (f'<path d="M{ax},{ay + 120} L{ax + 120},{ay} L{ax + 150},{ay} L{ax + 30},{ay + 120} Z" '
               f'fill="#ffffff" opacity="0.18"/>')
    for side in (-1, 1):
        cx = x0 - fw - 34 if side < 0 else x1 + fw + 34
        top_ = y0 - 70
        pts = [(cx - 62, top_), (cx + 62, top_), (cx + 52 * side + 26, y1 - 250), (cx + 34 * side, y1 - 190),
               (cx + 26, y1 + 100), (cx - 26, y1 + 100), (cx - 34 * side, y1 - 190), (cx + 52 * side - 26, y1 - 250)]
        fr += S.path(S.smooth_path(pts), fill="#9cc3a6", sw=4)
        for k in (-30, 0, 30):
            fr += (f'<path d="M{cx + k},{top_ + 20} Q{cx + k + 26 * side},{y1 - 270} {cx + k * 0.4},{y1 + 80}" '
                   f'stroke="#7fa78a" stroke-width="5" fill="none"/>')
        for k in range(5):
            fr += (f'<circle cx="{cx - 30 + 16 * k}" cy="{top_ + 80 + 70 * k}" r="5" fill="#fbf3e3" opacity="0.8"/>')
        fr += (f'<ellipse cx="{cx + 34 * side}" cy="{y1 - 196}" rx="24" ry="15" fill="#f2c45c" stroke="{INK}" '
               f'stroke-width="3"/>')
    fr += (f'<rect x="{x0 - 150}" y="{y0 - 92}" width="{x1 - x0 + 300}" height="18" rx="9" fill="#a8774a" '
           f'stroke="{INK}" stroke-width="3.5"/>')
    # a potted plant on the sill
    px, py = x0 + 60, y1 - 6
    fr += (f'<path d="M{px - 34},{py - 60} L{px + 34},{py - 60} L{px + 26},{py} L{px - 26},{py} Z" '
           f'fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    for a in (-50, -20, 10, 40):
        r = math.radians(a - 90)
        ex, ey = px + 64 * math.cos(r), py - 60 + 64 * math.sin(r)
        fr += (f'<path d="M{px},{py - 60} Q{f1((px + ex) / 2 - 10)},{f1((py - 60 + ey) / 2)} {f1(ex)},{f1(ey)} '
               f'Q{f1((px + ex) / 2 + 12)},{f1((py - 60 + ey) / 2 + 10)} {px},{py - 60} Z" fill="#7fae5a" '
               f'stroke="{INK}" stroke-width="2.5"/>')
    b += S.g(fr, filter="wobble-fine")
    # the bookshelf (left)
    bx0, bx1, btop = 110, 470, fy - 520
    sh = (f'<rect x="{bx0}" y="{btop}" width="{bx1 - bx0}" height="{fy - btop}" fill="#b98352" stroke="{INK}" '
          f'stroke-width="4"/>'
          f'<rect x="{bx0 + 16}" y="{btop + 16}" width="{bx1 - bx0 - 32}" height="{fy - btop - 32}" fill="#8e5f38"/>')
    rng = random.Random(12)
    for k in range(3):
        yb = btop + 16 + (k + 1) * (fy - btop - 32) / 3
        sh += (f'<rect x="{bx0 + 10}" y="{yb - 10}" width="{bx1 - bx0 - 20}" height="16" fill="#c99662" '
               f'stroke="{INK}" stroke-width="3"/>')
        x = bx0 + 26
        while x < bx1 - 60:
            if k == 1 and 260 < x < 360:
                # a ball and a toy boat on the middle shelf
                sh += PR.toy(x + 40, yb - 10, 0.75, 1, kind="ball")
                x += 100
                continue
            bw = rng.uniform(22, 38)
            bh = rng.uniform(90, 128)
            col = rng.choice(["#d9574a", "#4f86c6", "#f2c84b", "#6fae55", "#8e64b0", "#ef9440", "#e9e0c8"])
            tilt = rng.choice([0, 0, 0, -8]) if x > bx0 + 60 else 0
            sh += (f'<rect x="{x:.0f}" y="{yb - 10 - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" '
                   f'stroke="{INK}" stroke-width="2.5" transform="rotate({tilt} {x:.0f} {yb - 10:.0f})"/>'
                   f'<rect x="{x + 4:.0f}" y="{yb - 10 - bh + 14:.0f}" width="{bw - 8:.0f}" height="7" '
                   f'fill="#fbf3e3" opacity="0.7" transform="rotate({tilt} {x:.0f} {yb - 10:.0f})"/>')
            x += bw + 4
    # plant and a teddy on top
    sh += (f'<path d="M{bx0 + 60},{btop} L{bx0 + 120},{btop} L{bx0 + 110},{btop - 60} L{bx0 + 70},{btop - 60} Z" '
           f'fill="#5d9bb5" stroke="{INK}" stroke-width="3"/>')
    for a in (-60, -25, 10, 45):
        r = math.radians(a - 90)
        cx_, cy_ = bx0 + 90, btop - 60
        ex, ey = cx_ + 80 * math.cos(r), cy_ + 80 * math.sin(r)
        sh += (f'<path d="M{cx_},{cy_} Q{f1((cx_ + ex) / 2 - 12)},{f1((cy_ + ey) / 2)} {f1(ex)},{f1(ey)} '
               f'Q{f1((cx_ + ex) / 2 + 14)},{f1((cy_ + ey) / 2 + 10)} {cx_},{cy_} Z" fill="#7fae5a" stroke="{INK}" '
               f'stroke-width="2.5"/>')
    tx, ty = bx1 - 90, btop
    sh += (f'<circle cx="{tx}" cy="{ty - 50}" r="44" fill="#c08a58" stroke="{INK}" stroke-width="3.5"/>'
           f'<circle cx="{tx - 34}" cy="{ty - 120}" r="18" fill="#c08a58" stroke="{INK}" stroke-width="3"/>'
           f'<circle cx="{tx + 34}" cy="{ty - 120}" r="18" fill="#c08a58" stroke="{INK}" stroke-width="3"/>'
           f'<circle cx="{tx}" cy="{ty - 100}" r="38" fill="#c08a58" stroke="{INK}" stroke-width="3.5"/>'
           f'<ellipse cx="{tx}" cy="{ty - 88}" rx="16" ry="12" fill="#ecd2a8"/>'
           f'<circle cx="{tx - 13}" cy="{ty - 108}" r="4" fill="{INK}"/><circle cx="{tx + 13}" cy="{ty - 108}" r="4" '
           f'fill="{INK}"/><circle cx="{tx}" cy="{ty - 92}" r="4" fill="{INK}"/>'
           f'<path d="M{tx - 30},{ty - 66} Q{tx},{ty - 54} {tx + 30},{ty - 66}" stroke="#d9574a" stroke-width="7" '
           f'fill="none"/>')
    b += S.g(sh, filter="wobble-fine")
    # a child's crayon drawing pinned to the wall: a house, a sun and two stick figures
    dx0, dy0, dw, dh = 640, 220 + oy, 270, 200
    dr = (f'<g transform="rotate(3 {dx0 + dw / 2} {dy0 + dh / 2})">'
          f'<rect x="{dx0}" y="{dy0}" width="{dw}" height="{dh}" fill="#fbf4e2" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="{dx0 + 48}" cy="{dy0 + 46}" r="24" fill="#f6c94e"/>'
          f'<path d="M{dx0 + 130},{dy0 + 150} L{dx0 + 130},{dy0 + 100} L{dx0 + 170},{dy0 + 66} L{dx0 + 210},{dy0 + 100} '
          f'L{dx0 + 210},{dy0 + 150} Z" fill="none" stroke="#d9574a" stroke-width="6" stroke-linejoin="round"/>'
          f'<path d="M{dx0 + 20},{dy0 + 168} L{dx0 + 250},{dy0 + 168}" stroke="#6fae55" stroke-width="7"/>'
          f'<circle cx="{dx0 + 70}" cy="{dy0 + 110}" r="10" fill="none" stroke="#4f86c6" stroke-width="4"/>'
          f'<path d="M{dx0 + 70},{dy0 + 120} L{dx0 + 70},{dy0 + 150} M{dx0 + 58},{dy0 + 132} L{dx0 + 82},{dy0 + 132} '
          f'M{dx0 + 70},{dy0 + 150} L{dx0 + 62},{dy0 + 166} M{dx0 + 70},{dy0 + 150} L{dx0 + 78},{dy0 + 166}" '
          f'stroke="#4f86c6" stroke-width="4" fill="none"/>'
          f'<circle cx="{dx0 + 100}" cy="{dy0 + 120}" r="8" fill="none" stroke="#e48fb0" stroke-width="4"/>'
          f'<path d="M{dx0 + 100},{dy0 + 128} L{dx0 + 100},{dy0 + 152} M{dx0 + 90},{dy0 + 138} L{dx0 + 110},{dy0 + 138}" '
          f'stroke="#e48fb0" stroke-width="4" fill="none"/></g>'
          f'<circle cx="{dx0 + dw / 2}" cy="{dy0 + 8}" r="9" fill="#e45c5c" stroke="{INK}" stroke-width="2.5"/>')
    if drawing:
        b += S.g(dr, filter="wobble-fine")
    # a round wall clock
    cx_, cy_ = 1200, 250 + oy
    ck = (f'<circle cx="{cx_}" cy="{cy_}" r="66" fill="#f6c94e" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="{cx_}" cy="{cy_}" r="52" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>')
    for k in range(12):
        a = math.radians(k * 30)
        ck += (f'<circle cx="{f1(cx_ + 42 * math.sin(a))}" cy="{f1(cy_ - 42 * math.cos(a))}" r="3.5" '
               f'fill="{INK}"/>')
    ck += (f'<path d="M{cx_},{cy_} L{cx_ + 22},{cy_ - 12} M{cx_},{cy_} L{cx_ - 6},{cy_ - 36}" stroke="{INK}" '
           f'stroke-width="5" stroke-linecap="round"/><circle cx="{cx_}" cy="{cy_}" r="5" fill="#d9574a"/>')
    if clock:
        b += S.g(ck, filter="wobble-fine")
    # skirting board, floor boards, rug
    fl = (f'<rect x="-40" y="{fy}" width="{w + 80}" height="{H + oy - fy + 80}" fill="url(#j2floor)"/>'
          f'<rect x="-40" y="{fy - 24}" width="{w + 80}" height="26" fill="#e3bf92" stroke="{INK}" stroke-width="3"/>')
    for x in range(-60, w + 200, 170):
        fl += f'<path d="M{x},{fy + 2} L{x - 90},{H + oy + 40}" stroke="#8a5d3a" stroke-width="3" opacity="0.55"/>'
    for y in (fy + 60, fy + 150, fy + 260):
        fl += f'<path d="M-40,{y} L{w + 40},{y}" stroke="#b07a4c" stroke-width="2" opacity="0.4"/>'
    rcx, rcy = 1010, 1066 + oy
    fl += (f'<ellipse cx="{rcx}" cy="{rcy}" rx="720" ry="104" fill="#e2826e" stroke="{INK}" stroke-width="4"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="640" ry="82" fill="none" stroke="#f6cf8f" stroke-width="10" '
           f'stroke-dasharray="26 16"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="520" ry="58" fill="#ea9a82"/>'
           f'<ellipse cx="{rcx}" cy="{rcy}" rx="400" ry="40" fill="none" stroke="#fbe2bd" stroke-width="6"/>')
    b += S.g(fl, filter="wobble")
    # toy blocks on the floor by the shelf
    blocks = ""
    for (x, y, c, letter) in ((510, 960, "#4f86c6", "A"), (560, 968, "#f2c84b", "B"), (532, 914, "#d9574a", "C")):
        blocks += (f'<rect x="{x - 26}" y="{y - 52}" width="52" height="52" rx="6" fill="{c}" stroke="{INK}" '
                   f'stroke-width="3"/><text x="{x}" y="{y - 13}" font-family="LXGW WenKai" font-weight="bold" '
                   f'font-size="34" fill="#fffaf0" text-anchor="middle">{letter}</text>')
    b += S.g(S.g(blocks, filter="wobble-fine"), transform=f"translate(0,{oy})")
    return b, defs


def sibling_svg(who, x, y, s, facing, pose, expr, toy=None, shadow=True, w=W, h=H, box=None):
    out = C.ground_shadow(x + 4 * facing, y + 2, s, 120 if who == "big" else 100, 0.2) if shadow else ""
    out += C.child(x, y, s, facing, pose=pose, expr=expr, sibling=who, toy=toy)
    if box is not None:
        return boxed(out, box, w=w, h=h)
    return S.svg_doc(out, "", w, h)


def storm_cloud_svg(cx, cy, k=0, zap=False, w=W, h=H, box=None, sun=0.0):
    """A little grey sulking cloud with drizzle (drop phase k of 3); zap adds a tiny zigzag; sun 0..1 turns it into
    a bright little cloud (making up)."""
    fill = S.mix("#9aa6b8", "#fbf6ec", sun)
    shade_ = S.mix("#7d899c", "#e6eef2", sun)
    b = S.g(S.cloud(cx, cy, 230, 92, fill, seed=81, puffs=4, sw=3.2, shade_fill=shade_), filter="wobble-fine")
    if sun < 0.5:
        # a cross little face
        b += (f'<path d="M{cx - 40},{cy - 6} l16,6 M{cx + 40},{cy - 6} l-16,6" stroke="{INK}" stroke-width="4" '
              f'stroke-linecap="round"/>'
              f'<path d="M{cx - 14},{cy + 22} Q{cx},{cy + 12} {cx + 14},{cy + 22}" stroke="{INK}" stroke-width="4" '
              f'fill="none" stroke-linecap="round"/>')
        for i in range(5):
            dx = -80 + 40 * i
            yy = cy + 52 + ((k * 22 + i * 15) % 66)
            b += (f'<path d="M{cx + dx},{yy} q6,10 0,16 q-6,-6 0,-16 Z" fill="#9fd0e6" stroke="{INK}" '
                  f'stroke-width="2"/>')
        if zap:
            zx, zy = cx + 30, cy + 40
            b += (f'<path d="M{zx},{zy} L{zx - 16},{zy + 34} L{zx + 2},{zy + 34} L{zx - 12},{zy + 70} L{zx + 22},{zy + 24} '
                  f'L{zx + 4},{zy + 24} L{zx + 14},{zy} Z" fill="#f6d36b" stroke="{INK}" stroke-width="3" '
                  f'stroke-linejoin="round"/>')
    else:
        b += (f'<circle cx="{cx - 30}" cy="{cy}" r="5" fill="{INK}"/><circle cx="{cx + 30}" cy="{cy}" r="5" '
              f'fill="{INK}"/><path d="M{cx - 16},{cy + 16} Q{cx},{cy + 30} {cx + 16},{cy + 16}" stroke="{INK}" '
              f'stroke-width="4" fill="none" stroke-linecap="round"/>'
              f'<ellipse cx="{cx - 48}" cy="{cy + 12}" rx="10" ry="6" fill="#f2a6a0" opacity="0.8"/>'
              f'<ellipse cx="{cx + 48}" cy="{cy + 12}" rx="10" ry="6" fill="#f2a6a0" opacity="0.8"/>')
    if box is not None:
        return boxed(b, box, w=w, h=h)
    return S.svg_doc(b, "", w, h)


# ================================================================== the hint page


def road_pt(u):
    """Point and perspective scale along the road (u=0 near the bottom, 1 at the far end by the pyramids)."""
    pts = [(1060, 1230), (1180, 1040), (1080, 900), (1260, 790), (1480, 720), ROAD_END]
    n = len(pts) - 1
    v = min(n - 1e-6, max(0.0, u * n))
    i = int(v)
    f = v - i
    a, b = pts[i], pts[i + 1]
    # smooth (cosine) blend between control points
    g = 0.5 - 0.5 * math.cos(math.pi * f)
    x = a[0] + (b[0] - a[0]) * g
    y = a[1] + (b[1] - a[1]) * f
    s = 1.0 - 0.9 * (1 - (1 - u) ** 1.6)
    return x, y, max(0.1, s)


def hint_backdrop_svg():
    defs = (S.lin_grad("j2hsky", [(0, "#9ccbe0"), (0.4, "#d7e8dc"), (0.72, "#f6e2bd"), (1, "#f8cf9a")]) +
            S.rad_grad("j2hsun", [(0, "#fff6d8", 1), (0.35, "#ffe7b0", 0.6), (1, "#ffe7b0", 0)]) +
            S.lin_grad("j2hland", [(0, "#b9cf8a"), (1, "#8fb35c")]) +
            S.lin_grad("j2hsand", [(0, "#f1d6a0"), (1, "#e2bd7f")]))
    b = S.rect_bg("url(#j2hsky)")
    b += f'<circle cx="{ROAD_END[0] + 40}" cy="{ROAD_END[1] - 70}" r="420" fill="url(#j2hsun)"/>'
    b += (f'<circle cx="{ROAD_END[0] + 40}" cy="{ROAD_END[1] - 70}" r="52" fill="#fbe1a0" stroke="{INK}" '
          f'stroke-width="3" opacity="0.9"/>')
    cl = (S.cloud(700, 190, 330, 96, "#fbf3e6", seed=91, sw=3.2, shade_fill="#e9d9c4") +
          S.cloud(1300, 130, 260, 80, "#fbf3e6", seed=92, sw=3, shade_fill="#e9d9c4"))
    b += S.g(cl, filter="wobble")
    # far desert with the pyramids at the end of the road, sand on the right, Canaan's hills on the left
    sand = S.path(S.hill(700, W + 200, ROAD_END[1] + 30, 30, seed=93, bumps=3), fill="url(#j2hsand)", sw=2.4)
    b += S.g(sand, filter="wobble")
    b += PR.pyramids(ROAD_END[0] + 80, ROAD_END[1] + 8, 0.27, n=3, haze=0.5, ground=False)
    f1d = S.smooth_path([(-200, 690), (150, 600), (520, 590), (880, 640), (1180, 700), (1420, 760), (1560, 840)],
                        closed=False) + f" L1560,{H} L-200,{H} Z"
    f2d = S.smooth_path([(-200, 760), (200, 680), (520, 668), (820, 720), (1050, 790), (1200, 860)],
                        closed=False) + f" L1200,{H} L-200,{H} Z"
    far = S.path(f1d, fill="#b6cfa0", sw=2.4) + S.path(f2d, fill="#a6c486", sw=2.6)
    b += S.g(far, filter="wobble")
    trees = PR.olive_tree(180, 760, 0.42, seed=3) + PR.olive_tree(760, 700, 0.3, seed=6)
    trees += PR.palm_tree(1880, ROAD_END[1] + 40, 0.32) + PR.palm_tree(1980, ROAD_END[1] + 50, 0.26)
    b += PR._haze(trees, "#e8dcc0", 0.25, 0.3)
    # the near land: green turning to sand toward the right
    land = S.smooth_path([(-100, 830), (300, 820), (700, 800), (1100, 770), (1500, 735), (1800, 712), (W + 100, 700)],
                         closed=False) + f" L{W + 100},{H + 60} L-100,{H + 60} Z"
    b += S.g(S.path(land, fill="url(#j2hland)", sw=3.5), filter="wobble")
    defs += S.lin_grad("j2hblend", [(0, "#ecd29a", 0), (0.45, "#ecd29a", 0), (0.8, "#ecd29a", 0.75),
                                    (1, "#ecd29a", 0.85)], x2=1, y2=0)
    b += f'<path d="{land}" fill="url(#j2hblend)"/>'
    # the long road
    left, right = [], []
    for i in range(41):
        u = i / 40
        x, y, s = road_pt(u)
        hw = 150 * s
        left.append((x - hw, y))
        right.append((x + hw, y))
    d = S.smooth_path(left + right[::-1], closed=True)
    b += S.g(S.path(d, fill="#e8cf9c", sw=3.5), filter="wobble")
    stones = ""
    rng = random.Random(21)
    for i in range(30):
        u = rng.uniform(0.02, 0.85)
        x, y, s = road_pt(u)
        side = rng.choice([-1, 1])
        sx = x + side * 160 * s * rng.uniform(0.9, 1.2)
        r = 12 * s + 2
        stones += (f'<ellipse cx="{f1(sx)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r * 0.8)}" fill="#d9cdb6" '
                   f'stroke="{INK}" stroke-width="{max(1.5, 3 * s):.1f}"/>')
    b += S.g(stones, filter="wobble-fine")
    fl = T1.flowers(random.Random(8), 50, -40, 1000, 860, 1180, rmul=1.1)
    b += S.g(fl, filter="wobble-fine")
    b += PR.bush(1650, 800, 0.45, variant=3)
    home = PR.tent(760, 812, 0.52, -1, side="israel", flag=False)
    home += PR.sheep(560, 836, 0.5, 1, 0, pose="graze") + PR.sheep(640, 850, 0.46, -1, 2)
    home += PR.sheep(930, 842, 0.5, -1, 3, pose="graze") + PR.bush(1000, 846, 0.55, variant=1)
    b += PR._haze(home, "#e9dcc0", 0.12, 0.15)
    # the wooden post with its peg
    px = POST_X
    post = (f'<path d="M{px - 26},{H + 40} L{px - 20},{HOOK[1] - 120} Q{px},{HOOK[1] - 140} {px + 20},{HOOK[1] - 120} '
            f'L{px + 26},{H + 40} Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<path d="M{px - 6},{HOOK[1] - 100} L{px - 2},{H}" stroke="{P["wood_dark"]}" stroke-width="4" '
            f'opacity="0.5"/>'
            f'<path d="M{px + 18},{HOOK[1] - 16} L{HOOK[0] + 14},{HOOK[1] - 10} Q{HOOK[0] + 30},{HOOK[1] - 12} '
            f'{HOOK[0] + 26},{HOOK[1] - 30}" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<path d="M{px + 18},{HOOK[1] - 16} L{HOOK[0] + 14},{HOOK[1] - 10} Q{HOOK[0] + 30},{HOOK[1] - 12} '
            f'{HOOK[0] + 26},{HOOK[1] - 30}" stroke="{P["wood_light"]}" stroke-width="12" fill="none" '
            f'stroke-linecap="round"/>')
    b += S.g(post, filter="wobble-fine")
    b += PR.grass_tuft(px - 30, H - 70, 1.0, variant=2) + PR.grass_tuft(px + 50, H - 60, 0.8, variant=0)
    return S.svg_doc(b, defs)


HINT_TUFT_BOX = (0, 1030, W, H)


def hint_tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((60, 1186, 1.2, 2), (560, 1176, 1.0, 0), (880, 1190, 1.1, 2), (1500, 1188, 1.1, 0),
                       (1820, 1186, 1.2, 2), (2060, 1170, 1.0, 1)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return boxed(out, HINT_TUFT_BOX)


COAT_BOX = (0, HOOK[1] - 40, W, HOOK[1] + 400)


def hint_coat_svg():
    x, y = HOOK
    return boxed(PR.coat_of_colours(x, y - 4, 1.3, 1, state="held"), COAT_BOX)


def coat_glow_svg():
    x, y = HOOK
    defs = S.rad_grad("j2cg", [(0, "#fff3c8", 1), (0.4, "#ffe4a6", 0.7), (1, "#ffe1a0", 0)])
    return S.svg_doc(f'<ellipse cx="{x}" cy="{y + 165}" rx="360" ry="360" fill="url(#j2cg)"/>', defs)


N_STEPS = 12


def footprints_svg(n):
    out = ""
    for i in range(n):
        u = 0.08 + 0.84 * i / (N_STEPS - 1)
        x, y, s = road_pt(u)
        side = -1 if i % 2 else 1
        fx_, fy_ = x + side * 26 * s, y
        r = 21 * s + 3
        out += (f'<ellipse cx="{f1(fx_)}" cy="{f1(fy_)}" rx="{f1(r * 0.62)}" ry="{f1(r)}" fill="#b48c55" '
                f'opacity="0.85" transform="rotate(-18 {f1(fx_)} {f1(fy_)})"/>')
        for k in range(4):
            out += (f'<circle cx="{f1(fx_ - r * 0.45 + k * r * 0.3)}" cy="{f1(fy_ - r * 1.3 + abs(k - 1.5) * r * 0.12)}" '
                    f'r="{f1(r * 0.16)}" fill="#b48c55" opacity="0.85"/>')
    return S.svg_doc(out)


def curl_svg():
    """The turning page's edge: a curling strip of paper (centred on x = W/2) and its soft shadow to the right."""
    cx = W / 2
    defs = (S.lin_grad("j2curl", [(0, "#f6ecd6"), (0.6, "#fbf5e6"), (0.85, "#efe0c0"), (1, "#d8c49c")], x2=1, y2=0) +
            S.lin_grad("j2csh", [(0, INK, 0.35), (1, INK, 0)], x2=1, y2=0))
    b = (f'<rect x="{cx}" y="-40" width="90" height="{H + 80}" fill="url(#j2csh)"/>'
         f'<path d="M{cx - 100},-40 Q{cx - 112},{H / 2} {cx - 100},{H + 40} L{cx},{H + 40} L{cx},-40 Z" '
         f'fill="url(#j2curl)" stroke="{INK}" stroke-width="3.5"/>')
    return S.svg_doc(S.g(b, filter="wobble-fine"), defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    m0 = voice_marks(ctx, 0)
    m1 = voice_marks(ctx, 1)
    L0, L1 = ctx.lines[0], ctx.lines[1]

    def ph(m, i, default):
        return m[i] if len(m) > i else default
    p_kid = ph(m0, 0, ("小朋友", L0.start, L0.start + 0.5, [(L0.start, L0.start + 0.5)]))
    p_q1 = ph(m0, 1, ("你有没有被哥哥姐姐欺负过", L0.start + 0.8, L0.start + 2.6, [(L0.start + 0.8, L0.start + 2.6)]))
    p_q2 = ph(m0, 2, ("你有没有生过别人的气", L0.chunks[1].start, L0.chunks[1].end, [(L0.chunks[1].start, L0.chunks[1].end)]))
    p_q3 = ph(m0, 3, ("很久很久都不想原谅他", L0.chunks[-1].start, L0.end, [(L0.chunks[-1].start, L0.end)]))
    c1 = char_times(p_q1)
    c2 = char_times(p_q2)
    c3 = char_times(p_q3)
    t_kid = p_kid[1]
    t_grab = snap(c1[min(7, len(c1) - 1)] - 0.05)                     # '姐姐'
    yanks = [c1[k] for k in (9, 10, 11) if k < len(c1)]                 # '欺' '负' '过'
    t_win = snap(p_q1[2] + 0.12)                                         # she wins the toy
    t_sulk = snap(c2[min(4, len(c2) - 1)] - 0.04)                        # '生'
    t_cloud = snap(p_q3[1] - 0.05)                                       # '很久很久'
    t_zap = snap(c3[min(2, len(c3) - 1)])                                # the second '很久'
    t_line1 = m1[0][1] if m1 else L1.start
    p_steps = ph(m1, 1, ("有一个人被他的哥哥们欺负得好惨", L1.chunks[1].start, L1.chunks[1].end, []))
    p_but = ph(m1, 2, ("可是后来", L1.chunks[-1].start, L1.chunks[-1].start + 0.8, []))
    p_great = ph(m1, 3, ("他做了一件很了不起的事", L1.chunks[-1].start + 1.0, L1.end,
                         [(L1.chunks[-1].start + 1.0, L1.end)]))
    cg = char_times(p_great)
    t_great = cg[min(5, len(cg) - 1)]                                    # '很了不起'

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
        return M.progress(t, t_iris, t_iris_end, "sine") * 1500

    # ---- the page turn on line 1
    t_turn0 = t_line1 - 0.2
    t_turn1 = t_turn0 + 1.2

    def edge(t):
        if t < t_turn0:
            return W + 400
        if t >= t_turn1:
            return None
        return W + 140 - (W + 380) * M.progress(t, t_turn0, t_turn1, "inout")
    room_on = lambda t: 1.0 if (t >= t_iris and t < t_turn1 + 0.05) else 0.0   # noqa: E731
    hint_on = lambda t: 1.0 if t >= t_turn0 else 0.0                           # noqa: E731

    # ---- the room
    ROOM_BOX = (0, 0, W, H)
    body, defs = room_body()
    sc.add("room", boxed(S.g(body), ROOM_BOX, defs), z=100, reveal=iris_reveal(ROOM_BOX, *PIV, radius),
           motion=lambda t: Tf(alpha=room_on(t)))

    # the siblings
    KB = (560, 470, 1520, 1100)               # crop box of the sibling layers (covers every pose and the tug sway)
    big_frames = {
        "stand": sibling_svg("big", SIS_X - 20, KY, KS, 1, "stand", "happy", box=KB),
        "stand_b": sibling_svg("big", SIS_X - 20, KY, KS, 1, "stand", blink_name("happy"), box=KB),
        "tug": sibling_svg("big", SIS_X, KY, KS, 1, "tug", "cross", toy="horse", box=KB),
        "win": sibling_svg("big", SIS_X - 50, KY, KS, 1, "stand", "sly", toy="horse", box=KB),
        "win_b": sibling_svg("big", SIS_X - 50, KY, KS, 1, "stand", blink_name("happy"), toy="horse", box=KB),
    }
    little_frames = {
        "play": sibling_svg("little", BRO_X + 20, KY, KS, -1, "stand", "happy", toy="horse", box=KB),
        "play_b": sibling_svg("little", BRO_X + 20, KY, KS, -1, "stand", blink_name("happy"), toy="horse", box=KB),
        "tug": sibling_svg("little", BRO_X, KY, KS, -1, "tug", "cross", box=KB),
        "sad": sibling_svg("little", BRO_X, KY, KS, -1, "stand", "sad", box=KB),
        "sulk": sibling_svg("little", BRO_X, KY, KS, -1, "sulk", "cross", box=KB),
        "sulk_b": sibling_svg("little", BRO_X, KY, KS, -1, "sulk", blink_name("cross"), box=KB),
    }
    bn = list(big_frames)
    ln_ = list(little_frames)
    BI = {k: i for i, k in enumerate(bn)}
    LI = {k: i for i, k in enumerate(ln_)}

    def blinks(base, blink, times, ents):
        out = list(ents)
        for tb in times:
            tb = snap(tb)
            if all(abs(tb - tk) > 0.3 for tk, _ in ents):
                out += [(tb, blink), (snap(tb + 0.13), base)]
        return sorted(out)
    bents = [(0, BI["stand"]), (t_grab, BI["tug"]), (t_win, BI["win"])]
    bents = blinks(BI["stand"], BI["stand_b"], [t_iris_end - 0.3], bents)
    bents = blinks(BI["win"], BI["win_b"], [t_sulk + 0.9, t_zap + 0.6, t_line1 - 0.5], bents)
    lents = [(0, LI["play"]), (t_grab, LI["tug"]), (t_win, LI["sad"]), (t_sulk, LI["sulk"])]
    lents = blinks(LI["play"], LI["play_b"], [t_iris_end - 0.05], lents)
    lents = blinks(LI["sulk"], LI["sulk_b"], [t_cloud + 0.7, t_zap + 0.9, t_line1 - 0.2], lents)

    # tug of war: the pair sways together, a hard yank on each syllable of '欺负过'
    def tug(t):
        if not (t_grab <= t < t_win):
            return 0.0
        dx = 8 * math.sin(2 * math.pi * (t - t_grab) / 0.42)
        for i, ty in enumerate(yanks):
            u = t - ty
            if 0 <= u < 0.3:
                dx -= (16 + 6 * i) * math.sin(math.pi * u / 0.3)
        return dx

    def big_m(t):
        tf = Tf(dx=tug(t), rot=-2.0 * (tug(t) / 30.0), px=SIS_X, py=KY, alpha=room_on(t))
        return tf
    # she stumbles back two steps hugging the toy when she wins
    win_step = M.keys([(t_win - 0.05, {"dx": 0}), (t_win + 0.25, {"dx": -14}), (t_win + 0.5, {"dx": 0})],
                      ["out", "sine"])
    brx = BRO_X

    def little_m(t):
        dx = tug(t)
        u = t - t_win
        if 0 <= u < 0.6:               # empty-handed: he totters forward a step and back
            dx -= 22 * math.sin(math.pi * u / 0.6)
        return Tf(dx=dx, rot=-1.6 * (tug(t) / 30.0), px=brx, py=KY, alpha=room_on(t))

    def bob(period, phase):
        return M.breathe(0.012, period, pivot=(0, KY), phase=phase)
    cut_dips_big = [dip(tc, KS, (SIS_X, KY), 7) for tc in (t_grab, t_win)]
    cut_dips_little = [dip(tc, KS, (BRO_X, KY), 7) for tc in (t_grab, t_win, t_sulk)]
    sc.add("big", [big_frames[k] for k in bn], z=101, frame_at=cuts(bents), seed=31,
           reveal=iris_reveal(KB, *PIV, radius),
           motion=M.combine(big_m, win_step, *cut_dips_big,
                            M.breathe(0.012, 2.6, pivot=(SIS_X, KY))))
    sc.add("little", [little_frames[k] for k in ln_], z=102, frame_at=cuts(lents), seed=37,
           reveal=iris_reveal(KB, *PIV, radius),
           motion=M.combine(little_m, *cut_dips_little, M.breathe(0.014, 2.3, pivot=(BRO_X, KY), phase=0.4),
                            lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * (t - t_sulk) / 1.6)
                                         if t > t_sulk + 0.3 else 0.0, px=BRO_X, py=KY)))

    # the little storm cloud: pops up on '很久很久', drizzles, grumbles on the second '很久'
    cx_, cy_ = CLOUD
    cfr = [storm_cloud_svg(cx_, cy_, k) for k in range(3)] + [storm_cloud_svg(cx_, cy_, k, zap=True) for k in range(3)]

    def cloud_fa(t):
        k = int(t / 0.12) % 3
        return float(k + (3 if t_zap <= t < t_zap + 0.45 else 0))

    def cloud_m(t):
        if t < t_cloud:
            return Tf(alpha=0)
        u = min(1.0, (t - t_cloud) / 0.45)
        s = 0.2 + 0.8 * M.ease("back")(u)
        dy = 4 * math.sin(2 * math.pi * (t - t_cloud) / 1.8)
        dx = 0.0
        if t_zap <= t < t_zap + 0.5:
            dx = 5 * math.sin(2 * math.pi * (t - t_zap) / 0.1) * (1 - (t - t_zap) / 0.5)
        return Tf(dx=dx, dy=dy, sx=s, sy=s, alpha=min(1.0, (t - t_cloud) / 0.12) * room_on(t),
                  px=cx_, py=cy_ + 30)
    sc.add("cloud", cfr, z=103, frame_at=cloud_fa, motion=cloud_m, wc=0.5)

    # ---- the hint page (revealed under the turning page)
    HB = (0, 0, W, H)
    sc.add("hint", hint_backdrop_svg(), z=140, reveal=wipe_reveal(HB, edge), motion=lambda t: Tf(alpha=hint_on(t)))
    t_gust0 = p_steps[1] + 1.1
    t_gust1 = p_but[1] + 0.2
    gust = lambda t: M.progress(t, t_gust0, t_gust0 + 0.8, "sine") * (1 - M.progress(t, t_gust1 - 0.3, t_gust1 + 0.6, "sine"))  # noqa: E731,E501
    t_glow = t_turn1 + 0.2
    sc.add("coat_glow", coat_glow_svg(), z=140.5, wc=0, blend="screen",
           motion=M.combine(lambda t: Tf(alpha=hint_on(t) * M.progress(t, t_glow, t_glow + 0.8, "sine") *
                                         (0.75 - 0.45 * gust(t) + 0.35 * M.progress(t, p_but[1], p_but[1] + 0.8, "sine")
                                          + 0.25 * M.progress(t, t_great - 0.1, t_great + 0.4, "sine")) *
                                         (0.92 + 0.08 * math.sin(2 * math.pi * t / 2.2))),
                            M.breathe(0.03, 2.2, pivot=(HOOK[0], HOOK[1] + 165))))

    def coat_m(t):
        a = 2.0 * math.sin(2 * math.pi * t / 3.1) + gust(t) * (4.5 * math.sin(2 * math.pi * t / 1.1) + 3)
        return Tf(rot=a, px=HOOK[0], py=HOOK[1] - 6, alpha=hint_on(t))
    sc.add("coat", hint_coat_svg(), z=141, reveal=wipe_reveal(COAT_BOX, edge), motion=coat_m, seed=53)

    # footprints walking down the long road toward Egypt
    t_fp0, t_fp1 = p_steps[1] + 0.1, p_steps[2] - 0.1
    fps = [snap(t_fp0 + (t_fp1 - t_fp0) * i / (N_STEPS - 1)) for i in range(N_STEPS)]

    def fp_fa(t):
        return float(sum(1 for tp in fps if t >= tp))
    sc.add("footprints", [footprints_svg(n) for n in range(N_STEPS + 1)], z=140.4, frame_at=fp_fa, wc=0.4,
           motion=lambda t: Tf(alpha=hint_on(t)))
    sc.add("hint_tufts", [hint_tufts_svg(k) for k in range(3)], z=142, reveal=wipe_reveal(HINT_TUFT_BOX, edge),
           frame_at=lambda t: float((0, 1, 2, 1)[int(t / (0.5 if gust(t) < 0.3 else 0.25)) % 4]),
           motion=lambda t: Tf(alpha=hint_on(t)))
    # two far birds over the road
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (y0, vx, ph_) in enumerate(((330, 60, 0.0), (380, 52, 0.45))):
        def fly(t, y0=y0, vx=vx, ph_=ph_, i=i):
            x = 900 + 160 * i + vx * (t - t_turn1)
            return Tf(dx=x - 200, dy=y0 - 200 + 18 * math.sin(2 * math.pi * (t / 2.4 + ph_)),
                      alpha=M.progress(t, t_turn1, t_turn1 + 0.6, "sine"))
        sc.add(f"hbird{i}", [T1.flyer_svg("brown", w) for w in wings], z=140.3, motion=fly, wc=0.3,
               frame_at=lambda t, ph_=ph_: float(int(t / 0.08 + ph_ * 8) % 8))

    # the curling page edge
    def curl_m(t):
        X = edge(t)
        if X is None or t < t_turn0:
            return Tf(alpha=0)
        u = M.progress(t, t_turn0, t_turn1, "linear")
        k = 0.35 + 0.65 * math.sin(math.pi * u)
        return Tf(dx=X - W / 2, sx=k, px=W / 2, py=H / 2)
    sc.add("curl", curl_svg(), z=160, motion=curl_m, wc=0.3)

    # ---- light: the cloud shadow dims the page, then warm light comes back
    sc.fx = list(fx_title)
    sc.fx.append(FX.tint((70, 90, 130), lambda t: 0.16 * gust(t), mode="multiply"))
    sc.fx.append(FX.tint((255, 214, 150), lambda t: 0.10 * M.progress(t, p_but[1], p_but[1] + 1.0, "sine"),
                         mode="screen"))
    sc.fx.append(FX.sparkles((HOOK[0] - 190, HOOK[1] - 40, HOOK[0] + 190, HOOK[1] + 360), count=12, t0=t_great - 0.1,
                             size=(16, 32), period=1.2, drift=-14, seed=61))
    sc.fx.append(FX.sparkles((ROAD_END[0] - 160, ROAD_END[1] - 140, ROAD_END[0] + 200, ROAD_END[1] + 20), count=6,
                             t0=t_great + 0.25, size=(9, 18), period=1.5, drift=0, seed=63))
    sc.fx.append(FX.motes((300, 200, 1900, 900), count=26, t0=t_turn1, color=(255, 240, 200), seed=65, alpha=110))

    # ---- camera: s01's slow push continues; then the room; then the hint page drifts toward the road
    c_end = cam_title(1.0)
    c_room = Cam(1010, 676, 1760)
    cam_room = M.cam_keys([(1.0, c_end), (t_iris_end + 0.4, c_room), (t_sulk, Cam(1040, 670, 1720)),
                           (t_turn0, Cam(1050, 660, 1740)), (t_turn1 + 0.3, Cam(W / 2, H / 2, W * 0.97)),
                           (T, Cam(1110, 580, W * 0.9))], ["sine"] * 5)
    sc.camera = lambda t: cam_title(t) if t <= 1.0 else cam_room(t)

    # ---- sound
    sc.sfx("birds", 0, dur=t_iris + 0.6, gain_db=-18, fade_in=0.2, fade_out=0.6)
    sc.sfx("cloth", t_grab, gain_db=-12)
    for ty in yanks:
        sc.sfx("whoosh", ty, gain_db=-17)
    sc.sfx("thud", t_win + 0.2, gain_db=-14)
    sc.sfx("pop", t_cloud, gain_db=-13)
    sc.sfx("rain", t_cloud + 0.1, dur=t_turn0 - t_cloud + 0.3, gain_db=-27, fade_in=0.4, fade_out=0.6)
    sc.sfx("thunder", t_zap, gain_db=-27)
    sc.sfx("whoosh", t_turn0 + 0.2, gain_db=-11)
    sc.sfx("wind_soft", t_turn1, dur=T - t_turn1 + 0.3, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", t_gust0, dur=t_gust1 - t_gust0 + 0.6, gain_db=-17, fade_in=0.6, fade_out=0.8)
    sc.sfx("birds", p_but[1], dur=T - p_but[1] + 0.3, gain_db=-20, fade_in=1.0, fade_out=1.0)
    sc.sfx("sparkle", t_great, gain_db=-12)
    sc.sfx("chime", t_great + 0.1, gain_db=-13)
    return sc
