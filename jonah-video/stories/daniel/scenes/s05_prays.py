"""Scene 5 — Daniel keeps praying (Daniel 6:10).

"但以理知道了这道命令。可是他没有害怕，也没有躲起来。他知道这样做会有危险，可是他更相信上帝。他回到家，上了楼，
打开朝着耶路撒冷的窗户。他像平常一样，一天三次，跪下来向上帝祷告，感谢上帝。"

One 3200 x 1560 stage, no cuts: a sunny Babylon street. On the left a long mud-brick wall with the king's decree
posted on it (s04 ends in the palace, so the scene opens on this new place); above the wall the flat roofs of the
city and, far away to the west on a blue hill, tiny Jerusalem with its temple. On the right Daniel's two-storey
house: an outside stair with a solid parapet up to a landing and the upper door, the teal-shuttered upstairs window,
the ground-floor door with an awning, doves on the roof, a palm and a cluster of big storage jars by the street
(s06 continues on this stage: the officials hide behind those jars).

  line 0  "但以理知道了这道命令。"   Daniel stands at the wall reading the decree; on "命令" he puts his hand to his
                                      chin, thinking.
          "可是他没有害怕，"         a little hop-turn: he faces us, hand on his chest, chin up, smiling (not afraid);
          "也没有躲起来。"           a calm nod (he stays right where he is).
  line 1  "他知道这样做会有危险，"   hand to chin again, a little worried; a thought bubble pops up: a roaring lion.
          "可是他更相信上帝。"       the bubble pops away; soft golden light falls on him from above (God is shown
                                      only as light); he looks up into it, happy; then hand on chest again.
  line 2  "他回到家，上了楼，"       he walks home (planted-foot walk) and climbs the outside stair (his legs are
                                      behind the stair's parapet), the camera following; he steps through the
                                      upper door into the shade.
          "打开朝着耶路撒冷的窗户。" the teal shutters swing open: Daniel in the window, arms spread; he turns to
                                      face west; a trail of golden dots arcs from the window to far-away Jerusalem,
                                      which glows.
  line 3  "他像平常一样，一天三次，" the camera moves in on the window; three smiling suns pop up across the sky one
                                      after the other (morning, noon, evening: 1, 2, 3), Daniel nodding with each.
          "跪下来向上帝祷告，"       he kneels and prays; warm light pours down on the window, the room glows.
          "感谢上帝。"               he lifts both arms in thanks; then folds his hands again (calm last frame —
                                      s06 opens on exactly this framing and picks up the praying Daniel).

Shared with s06 (same stage): SW, SH, GY, K, the house / window / jar geometry and every *_svg drawing below,
plus the small helpers (Perf, phrase_t, walk drawings). Pose changes are hard cuts sold by a squash-and-hop;
the walk is a planted-foot cycle (the anchor advances by whole drawings); nothing crossfades between two drawings
of a figure. Camera: few long sine moves, within ~15 output px / frame.
"""
import math
import random

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_A, WALK_N, sprite, walk_pose
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3200, 1560
GY = 1300                     # street ground line (feet)
K = 0.7                       # person scale on this stage
INK = P["ink"]

# ------------------------------------------------------------------ geometry
WALL_TOP = 930                # the decree wall (x -60 .. WALL_X1)
WALL_X1 = 1480
DECREE = (1175, 1075, 0.72)   # posted decree (centre, scale)
READ_X = 1330                 # Daniel reading the decree
HX0, HX1 = 1500, 2820         # Daniel's house front wall
ROOF_Y = 600                  # top of the house wall (parapet above)
FLOOR_UP = 960                # upstairs floor / landing level
WIN_X = 2400                  # upstairs window: sill-top anchor
WIN_Y = FLOOR_UP - round(PR.WINDOW_FLOOR_Y * K)          # 897
STAIR_X0, STAIR_X1 = 1560, 1960                          # stair foot (on GY) .. top (on FLOOR_UP)
LANDING_X1 = 2120
DOOR_X, DOOR_W, DOOR_H = 2058, 96, 214                   # upper door (centre, width, height above FLOOR_UP)
PARAPET = 112                 # parapet height above the treads (hides the climber's legs)
GDOOR_X = 2215                # ground-floor door
JAR_X = 2770                  # jar cluster (s06: the officials hide behind it)
JERUSALEM = (1130, 758)       # tiny far-away Jerusalem on its hill (west)
SUNS = [(2860, 478), (2330, 422), (1800, 478)]            # morning (east), noon, evening (west)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def poly(pts, fill, sw=4, extra=""):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}" {st} {extra}/>'


def rect(x, y, w, h, fill, sw=4, rx=0, extra=""):
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" fill="{fill}" {st} {extra}/>'


def phrase_t(line, phrase, frac=0.0):
    """Start of ``phrase`` inside its subtitle chunk (estimated by character index); falls back to ``frac`` of
    the line if the phrase is gone (an edited script never breaks the build)."""
    for c in line.chunks:
        i = c.text.find(phrase)
        if i >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、")))
            return c.start + (c.end - c.start) * i / n
    return line.start + (line.end - line.start) * frac


def haze(markup, k, tint="#dfe6e6"):
    return PR._haze(markup, tint, k, 0.55 * k)


def bricks(x0, x1, y0, y1, col, seed, n=10):
    """Scattered exposed-brick patches on plaster (x0..x1, y0 top .. y1 bottom)."""
    rng = random.Random(seed)
    out = ""
    dark = S.shade(col, -0.16)
    for _ in range(n):
        bx, by = rng.uniform(x0, x1 - 60), rng.uniform(y0, y1 - 40)
        for r_ in range(rng.randint(2, 3)):
            off = 14 if r_ % 2 else 0
            for c_ in range(rng.randint(1, 3)):
                out += rect(bx + off + c_ * 30, by + r_ * 15, 26, 11, S.shade(col, -0.06), 0, 2,
                            f'stroke="{dark}" stroke-width="2" opacity="0.8"')
    return out


# ------------------------------------------------------------------ sky + distance
def sky_svg(warm=0.0):
    top = S.mix("#8cc6dd", "#e9a777", warm)
    mid = S.mix("#c3e3e8", "#f6c48c", warm)
    low = S.mix("#f6e6c0", "#fbd9a0", warm)
    defs = (S.lin_grad("s5sky", [(0, top), (0.42, mid), (0.62, low), (1, low)])
            + S.rad_grad("s5glow", [(0, "#fff6da", 0.8), (0.5, "#fdebc4", 0.3), (1, "#fdebc4", 0)]))
    body = S.rect_bg("url(#s5sky)", SW, SH)
    body += '<ellipse cx="1150" cy="760" rx="900" ry="380" fill="url(#s5glow)"/>'
    return doc(body, defs)


def clouds_svg(i):
    items = [(560, 230, 330, 92, 3), (1700, 160, 260, 76, 7), (2700, 250, 300, 84, 11), (3150, 120, 220, 64, 5),
             (120, 420, 210, 60, 9)]
    cx, cy, w, h, sd = items[i]
    return doc(S.g(S.cloud(cx, cy, w, h, "#fdf6e8", seed=sd, sw=3, shade_fill="#efe2d0"), filter="wobble"))


def jerusalem_local():
    """Tiny far-away Jerusalem (local, bottom centre on its hilltop): a little walled city with a temple."""
    wall, lt, roof = "#d9cdb8", "#ece2cf", "#c9b89c"
    out = ""
    # houses climbing behind the wall
    for x, y, w, h in [(-62, -38, 26, 22), (-36, -44, 22, 26), (30, -40, 24, 24), (52, -34, 22, 20)]:
        out += rect(x, y, w, h, lt, 2.2)
    # the temple: a white block with a gold roof edge and a porch
    out += rect(-18, -78, 40, 48, "#f3ead6", 2.4)
    out += rect(-22, -84, 48, 8, "#e8c062", 2.2)
    out += rect(-4, -60, 12, 30, "#8a6d52", 1.6)
    out += f'<path d="M-30,-30 L-30,-62 L-22,-62 L-22,-30 Z" fill="{lt}" stroke="{INK}" stroke-width="2"/>'
    # wall with tiny merlons
    out += rect(-80, -26, 160, 26, wall, 2.4)
    for mx in range(-78, 80, 14):
        out += rect(mx, -32, 8, 7, wall, 1.8)
    return out


def far_svg():
    """Far blue hills to the west with tiny Jerusalem on the highest one, rows of hazy Babylon roofs, palms
    and the ziggurat (Etemenanki) beyond the house."""
    rng = random.Random(5)
    hill1 = S.mix("#a9b9cf", "#e9e3d6", 0.35)
    hill2 = S.mix("#b9c4cf", "#efe6d2", 0.5)
    body = S.path(S.hill(-200, 1900, 900, 150, seed=3, bumps=3), fill=hill2, sw=2.2)
    # Jerusalem's hill (the highest, a soft dome under the city)
    jx, jy = JERUSALEM
    body += S.path(f"M{jx - 420},905 C{jx - 260},800 {jx - 150},{jy + 4} {jx},{jy} "
                   f"C{jx + 150},{jy + 4} {jx + 260},800 {jx + 420},905 Z", fill=hill1, sw=2.4)
    body += S.path(S.hill(1800, 3400, 905, 90, seed=8, bumps=2), fill=hill2, sw=2.2)
    out = S.g(body, filter="wobble")
    out += S.g(f'<g transform="translate({jx},{jy + 3}) scale(1.15)">{haze(jerusalem_local(), 0.12)}</g>',
               filter="wobble-fine")
    # the ziggurat beyond the house (right), hazy
    out += haze(PR.ziggurat(3020, 960, 0.34), 0.42)
    # rows of flat roofs and palms (only their tops show above the decree wall)
    houses = ""
    x = -120
    while x < SW + 120:
        if not (1440 < x < 2860):
            houses += PR.house(x, 985 + rng.uniform(-6, 6), 0.2 * rng.uniform(0.9, 1.12), rng.randint(0, 3),
                               facing=rng.choice((1, -1)))
        x += rng.uniform(170, 240)
    palms = ""
    for px in (260, 880, 1380, 2950, 3120):
        palms += PR.palm_tree(px, 955, 0.36 * rng.uniform(0.9, 1.1), lean=rng.uniform(-0.25, 0.25), dates=False)
    out += haze(palms, 0.45) + haze(houses, 0.42)
    return doc(out)


def jerusalem_glow_svg():
    jx, jy = JERUSALEM
    defs = S.rad_grad("s5jg", [(0, "#fff4c8", 0.95), (0.4, "#ffe7a0", 0.5), (1, "#ffe7a0", 0)])
    return doc(f'<ellipse cx="{jx}" cy="{jy - 40}" rx="230" ry="150" fill="url(#s5jg)"/>', defs)


# ------------------------------------------------------------------ the decree wall + street
def wall_svg():
    col = S.mix(P["sand"], P["stone"], 0.55)
    top = WALL_TOP
    out = rect(-60, top, WALL_X1 + 60, GY - top + 10, col, 5)
    # coping and merlon-like caps
    out += rect(-70, top - 18, WALL_X1 + 84, 24, S.shade(col, 0.12), 4, 6)
    for mx in range(-40, WALL_X1 - 20, 120):
        out += rect(mx, top - 50, 64, 34, S.shade(col, 0.12), 4, 5)
    # glazed blue band with rosettes (Babylon)
    out += rect(-60, top + 70, WALL_X1 + 60, 36, "#4f86b0", 4)
    for rx_ in range(0, WALL_X1, 92):
        out += f'<circle cx="{rx_ + 30}" cy="{top + 88}" r="11" fill="#f2e2b4" stroke="{INK}" stroke-width="2.5"/>'
        out += f'<circle cx="{rx_ + 30}" cy="{top + 88}" r="4" fill="#e8b63c"/>'
    out += bricks(-40, WALL_X1 - 20, top + 130, GY - 40, col, 4, n=12)
    # the wall's end (right): a rounded pier
    out += rect(WALL_X1 - 36, top - 64, 52, GY - top + 74, S.shade(col, 0.06), 5, 8)
    # base shadow
    out += f'<rect x="-60" y="{GY - 26}" width="{WALL_X1 + 60}" height="26" fill="{INK}" opacity="0.10"/>'
    return doc(S.g(out, filter="wobble"))


def decree_svg():
    x, y, s = DECREE
    # a wooden board behind it, with two pegs
    out = S.g(rect(x - 98 * s - 14, y - 142 * s - 12, 196 * s + 28, 284 * s + 24, P["wood_light"], 4, 8)
              + f'<circle cx="{x - 60 * s}" cy="{y - 128 * s}" r="6" fill="{P["wood_dark"]}"/>'
              + f'<circle cx="{x + 60 * s}" cy="{y - 128 * s}" r="6" fill="{P["wood_dark"]}"/>', filter="wobble-fine")
    out += PR.decree(x, y, s)
    return doc(out)


def street_svg():
    defs = S.lin_grad("s5st", [(0, S.mix(P["sand_light"], P["sand"], 0.35)), (1, S.mix(P["sand"], P["earth"], 0.25))])
    out = f'<rect x="-40" y="{GY - 14}" width="{SW + 80}" height="{SH - GY + 60}" fill="url(#s5st)" stroke="{INK}" stroke-width="4"/>'
    rng = random.Random(12)
    # paving stones in loose rows
    for row, yy in enumerate((GY + 34, GY + 92, GY + 170)):
        x = -30 + row * 40
        while x < SW + 40:
            w = rng.uniform(70, 120) * (1 + 0.25 * row)
            out += (f'<ellipse cx="{f1(x)}" cy="{f1(yy + rng.uniform(-6, 6))}" rx="{f1(w / 2 - 8)}" ry="{f1(9 + 6 * row)}" '
                    f'fill="{S.mix(P["sand_light"], P["stone"], rng.uniform(0.2, 0.6))}" stroke="{P["ink_soft"]}" '
                    f'stroke-width="2.4" opacity="0.75"/>')
            x += w + rng.uniform(20, 60)
    return doc(S.g(out, filter="wobble"), defs)


# ------------------------------------------------------------------ Daniel's house
HOUSE_COL = S.mix(P["sand_light"], P["stone"], 0.45)


def house_svg():
    """Front wall with holes for the upstairs window and the upper door, roof edge, beam ends, parapet, the
    ground-floor door with an awning, little windows, pots and plants."""
    col = HOUSE_COL
    x0, x1 = HX0, HX1
    o = WIN_X
    wx0, wx1 = o - 95 * K, o + 95 * K
    wy0, wy1 = WIN_Y - 262 * K, WIN_Y
    dx0, dx1 = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2
    dy0 = FLOOR_UP - DOOR_H
    r = 14 * K
    win = (f"M{f1(wx0)},{f1(wy1)} L{f1(wx0)},{f1(wy0 + r)} Q{f1(wx0)},{f1(wy0)} {f1(wx0 + r)},{f1(wy0)} "
           f"L{f1(wx1 - r)},{f1(wy0)} Q{f1(wx1)},{f1(wy0)} {f1(wx1)},{f1(wy0 + r)} L{f1(wx1)},{f1(wy1)} Z")
    door = (f"M{f1(dx0)},{FLOOR_UP} L{f1(dx0)},{f1(dy0 + 40)} A{DOOR_W / 2},{40} 0 0 1 {f1(dx1)},{f1(dy0 + 40)} "
            f"L{f1(dx1)},{FLOOR_UP} Z")
    wall = f"M{x0},{ROOF_Y} L{x1},{ROOF_Y} L{x1},{GY + 4} L{x0},{GY + 4} Z " + win + " " + door
    cid = "s5hwall"
    out = f'<path d="{wall}" fill="{col}" fill-rule="evenodd" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    out += (f'<clipPath id="{cid}"><path d="{wall}" clip-rule="evenodd"/></clipPath><g clip-path="url(#{cid})">'
            + bricks(x0 + 20, x1 - 20, ROOF_Y + 60, GY - 30, col, 21, n=14)
            # soft shade under the roof edge and a floor band between the storeys
            + f'<rect x="{x0}" y="{ROOF_Y}" width="{x1 - x0}" height="46" fill="{INK}" opacity="0.10"/>'
            + f'<rect x="{x0}" y="{FLOOR_UP + 6}" width="{x1 - x0}" height="16" fill="{INK}" opacity="0.07"/></g>')
    # parapet + roof slab with beam ends
    out += rect(x0 - 26, ROOF_Y - 22, x1 - x0 + 52, 26, S.shade(col, 0.1), 4, 6)
    out += rect(x0 - 14, ROOF_Y - 64, x1 - x0 + 28, 44, S.shade(col, 0.04), 4, 6)
    for bx in range(int(x0 + 40), int(x1 - 20), 86):
        out += f'<circle cx="{bx}" cy="{ROOF_Y + 18}" r="11" fill="{P["wood"]}" stroke="{INK}" stroke-width="3.2"/>'
        out += f'<circle cx="{bx}" cy="{ROOF_Y + 18}" r="4" fill="{P["wood_dark"]}"/>'
    # upper door frame and step
    out += f'<path d="{door}" fill="none" stroke="{INK}" stroke-width="10"/>'
    out += f'<path d="{door}" fill="none" stroke="{P["wood"]}" stroke-width="5"/>'
    # ground-floor door with a striped awning
    gx, gw, gh = GDOOR_X, 120, 250
    out += rect(gx - gw / 2 - 12, GY - gh - 12, gw + 24, gh + 12, P["wood_light"], 4, 8)
    out += rect(gx - gw / 2, GY - gh, gw, gh, P["wood"], 4, 6)
    for k in (1, 2):
        out += f'<path d="M{gx - gw / 2 + k * gw / 3},{GY - gh + 8} L{gx - gw / 2 + k * gw / 3},{GY - 6}" stroke="{P["wood_dark"]}" stroke-width="3"/>'
    out += f'<circle cx="{gx + 36}" cy="{GY - 120}" r="7" fill="{P["crown"]}" stroke="{INK}" stroke-width="2.4"/>'
    aw_y = GY - gh - 26
    stripes = ""
    for i in range(7):
        xa = gx - 110 + i * 220 / 7
        stripes += poly([(xa, aw_y - 40), (xa + 220 / 7, aw_y - 40), (xa + 220 / 7 + 6, aw_y + 14), (xa + 6, aw_y + 14)],
                        "#3b8b89" if i % 2 == 0 else "#f2e6cc", 3)
    out += stripes
    out += rect(gx - 116, aw_y - 48, 232, 12, P["wood"], 3.4, 5)
    # a small barred window upstairs on the left, a vine climbing beside it
    out += rect(1700, 700, 64, 96, "#5b4232", 4, 28)
    for bx in (1721, 1743):
        out += f'<path d="M{bx},{704} L{bx},{792}" stroke="{P["wood"]}" stroke-width="5"/>'
    out += rect(1688, 790, 88, 14, P["wood_light"], 3, 4)
    vine = "M1612,960 C1590,880 1640,820 1618,740 C1600,680 1650,640 1640,600"
    out += f'<path d="{vine}" fill="none" stroke="{P["leaf_dark"]}" stroke-width="5"/>'
    for i in range(9):
        u = i / 8
        vx, vy = 1620 + 18 * math.sin(i * 1.7), 950 - 340 * u
        out += (f'<ellipse cx="{f1(vx + (10 if i % 2 else -10))}" cy="{f1(vy)}" rx="16" ry="10" fill="{P["leaf"]}" '
                f'stroke="{INK}" stroke-width="2.6" transform="rotate({-30 if i % 2 else 30} {f1(vx)} {f1(vy)})"/>')
        if i % 3 == 1:
            out += f'<circle cx="{f1(vx + 4)}" cy="{f1(vy - 12)}" r="8" fill="#e98aa8" stroke="{INK}" stroke-width="2.2"/>'
    # little ground-floor windows
    for wx in (2480, 2640):
        out += rect(wx - 22, GY - 230, 44, 60, "#5b4232", 4, 18)
        out += rect(wx - 30, GY - 172, 60, 12, P["wood_light"], 3, 4)
    # pots and plants
    out += pot(2340, GY, 0.8, "#b8946a", flowers=True)
    out += pot(2700, ROOF_Y - 64, 0.75, "#c9714a", flowers=True)
    out += pot(1600, ROOF_Y - 64, 0.7, "#b8946a")
    # a little washing line on the roof
    out += f'<path d="M1880,{ROOF_Y - 64} L1880,{ROOF_Y - 170} M2240,{ROOF_Y - 64} L2240,{ROOF_Y - 170}" stroke="{P["wood_dark"]}" stroke-width="7" stroke-linecap="round"/>'
    out += f'<path d="M1880,{ROOF_Y - 160} Q2060,{ROOF_Y - 130} 2240,{ROOF_Y - 160}" fill="none" stroke="{P["ink_soft"]}" stroke-width="3"/>'
    for cx, w, c in ((1950, 56, "#e9d7a8"), (2050, 70, "#c9714a"), (2160, 52, "#9ccc6a")):
        yy = ROOF_Y - 160 + 30 * math.sin(math.pi * (cx - 1880) / 360) * 1.0
        out += poly([(cx - w / 2, yy), (cx + w / 2, yy + 2), (cx + w / 2 - 4, yy + 66), (cx - w / 2 + 4, yy + 62)], c, 3)
    return doc(S.g(out, filter="wobble"))


def pot(x, y, s, col, flowers=False):
    out = (f'<path d="M{x - 34 * s},{y - 70 * s} Q{x - 48 * s},{y - 30 * s} {x - 24 * s},{y} L{x + 24 * s},{y} '
           f'Q{x + 48 * s},{y - 30 * s} {x + 34 * s},{y - 70 * s} Z" fill="{col}" stroke="{INK}" stroke-width="{4 * s:.1f}"/>')
    out += rect(x - 40 * s, y - 82 * s, 80 * s, 14 * s, S.shade(col, 0.15), 4 * s, 4)
    leaves = ""
    for a in (-60, -30, 0, 30, 60):
        ra = math.radians(a - 90)
        ex, ey = x + 70 * s * math.cos(ra), y - 82 * s + 70 * s * math.sin(ra)
        leaves += (f'<path d="M{x},{y - 82 * s} Q{(x + ex) / 2 - 14 * s},{(y - 82 * s + ey) / 2} {ex},{ey} '
                   f'Q{(x + ex) / 2 + 14 * s},{(y - 82 * s + ey) / 2} {x},{y - 82 * s} Z" fill="{P["leaf"]}" '
                   f'stroke="{INK}" stroke-width="{3 * s:.1f}"/>')
        if flowers:
            leaves += f'<circle cx="{ex}" cy="{ey}" r="{9 * s}" fill="#e98a8a" stroke="{INK}" stroke-width="{2.4 * s:.1f}"/>'
    return out + leaves


def door_dark_svg():
    """The shade behind the upper door (drawn under the house wall)."""
    dx0 = DOOR_X - DOOR_W / 2
    return doc(rect(dx0 - 10, FLOOR_UP - DOOR_H - 10, DOOR_W + 20, DOOR_H + 14, "#3e2b20", 0))


def window_back_svg(glow):
    return doc(PR.upstairs_window(WIN_X, WIN_Y, K, open=1.0, part="back", wall=False, glow=glow))


def window_front_svg(op):
    return doc(PR.upstairs_window(WIN_X, WIN_Y, K, open=op, part="front", wall=False))


def stair_steps(n=8):
    """[(x0, x1, tread_y)] of the outside stair's steps."""
    run, h = (STAIR_X1 - STAIR_X0) / n, (GY - FLOOR_UP) / n
    return [(STAIR_X0 + i * run, STAIR_X0 + (i + 1) * run, GY - (i + 1) * h) for i in range(n)]


def stair_svg():
    """The solid mud-brick outside stair: a stepped parapet (in front of Daniel while he climbs: it hides his
    legs) up to the landing at the upper door."""
    col = S.shade(HOUSE_COL, -0.04)
    steps = stair_steps()
    top = [(STAIR_X0 - 46, GY - PARAPET * 0.55)]
    for x0, x1, ty in steps:
        top += [(x0, ty - PARAPET), (x1, ty - PARAPET)]
    top += [(LANDING_X1, FLOOR_UP - PARAPET)]
    pts = [(STAIR_X0 - 46, GY + 4)] + top + [(LANDING_X1, GY + 4)]
    out = poly(pts, col, 5)
    # coping caps on every step
    cap = S.shade(col, 0.16)
    out += rect(STAIR_X0 - 54, GY - PARAPET * 0.55 - 10, 62, 18, cap, 3.6, 4)
    for x0, x1, ty in steps:
        out += rect(x0 - 6, ty - PARAPET - 10, x1 - x0 + 12, 18, cap, 3.6, 4)
    out += rect(STAIR_X1 - 6, FLOOR_UP - PARAPET - 10, LANDING_X1 - STAIR_X1 + 14, 18, cap, 3.6, 4)
    cid = "s5stair"
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    sh = ""
    for x0, x1, ty in steps:          # shadow under each cap and a faint diagonal of the hidden treads
        sh += f'<rect x="{f1(x0)}" y="{f1(ty - PARAPET + 8)}" width="{f1(x1 - x0)}" height="14" fill="{INK}" opacity="0.08"/>'
    out += (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
            + bricks(STAIR_X0, LANDING_X1, FLOOR_UP - 40, GY, col, 33, n=8) + sh
            # an arched niche under the landing
            + f'<path d="M{LANDING_X1 - 150},{GY} L{LANDING_X1 - 150},{GY - 120} A55,55 0 0 1 {LANDING_X1 - 40},{GY - 120} '
              f'L{LANDING_X1 - 40},{GY} Z" fill="{S.shade(col, -0.25)}" stroke="{INK}" stroke-width="4"/>'
            + f'<rect x="{LANDING_X1 - 30}" y="{FLOOR_UP - PARAPET}" width="30" height="{GY - FLOOR_UP + PARAPET}" '
              f'fill="{INK}" opacity="0.07"/></g>')
    # a pot with a little plant on the newel at the stair foot
    out += pot(STAIR_X0 - 23, GY - PARAPET * 0.55 - 10, 0.5, "#c9714a", flowers=True)
    return doc(S.g(out, filter="wobble"))


def jars_svg():
    """Big clay storage jars and a basket by the street, right of the house (s06: the officials hide here)."""
    out = ""
    for x, s, c in ((JAR_X - 110, 1.05, "#c27a4e"), (JAR_X + 120, 1.15, "#b8946a"), (JAR_X + 10, 1.35, "#c9714a")):
        y = GY + 20
        out += (f'<path d="M{x - 40 * s},{y - 150 * s} Q{x - 92 * s},{y - 90 * s} {x - 50 * s},{y - 10 * s} '
                f'Q{x},{y + 6 * s} {x + 50 * s},{y - 10 * s} Q{x + 92 * s},{y - 90 * s} {x + 40 * s},{y - 150 * s} Z" '
                f'fill="{c}" stroke="{INK}" stroke-width="5"/>')
        out += rect(x - 46 * s, y - 166 * s, 92 * s, 20 * s, S.shade(c, 0.15), 4, 6)
        out += (f'<path d="M{x - 70 * s},{y - 100 * s} Q{x},{y - 84 * s} {x + 70 * s},{y - 100 * s}" fill="none" '
                f'stroke="{S.shade(c, -0.25)}" stroke-width="4"/>')
        out += (f'<path d="M{x - 52 * s},{y - 120 * s} Q{x - 62 * s},{y - 80 * s} {x - 48 * s},{y - 50 * s}" fill="none" '
                f'stroke="{S.shade(c, 0.35)}" stroke-width="7" stroke-linecap="round" opacity="0.6"/>')
    sh = f'<ellipse cx="{JAR_X}" cy="{GY + 22}" rx="260" ry="20" fill="{INK}" opacity="0.14" filter="url(#soft)"/>'
    return doc(sh + S.g(out, filter="wobble-fine"))


def palm_svg(x, y, s, sway):
    return doc(PR.palm_tree(x, y, s, lean=-0.1, sway=sway))


def fg_svg():
    out = ""
    for x, v, s in ((40, 0, 1.3), (300, 2, 1.1), (900, 0, 1.2), (1480, 1, 1.2), (3150, 0, 1.3)):
        out += PR.grass_tuft(x, GY + 140 + (x % 50), s, variant=v)
    return doc(out)


# ------------------------------------------------------------------ device drawings
def bubble_svg(cx, cy, rx, ry, tail_to, content, seed=4):
    """A puffy thought bubble (cream) with three little trailing puffs toward ``tail_to`` and ``content`` inside."""
    puff = ""
    n = 11
    for i in range(n):
        a = 2 * math.pi * i / n
        puff += f'<circle cx="{f1(cx + rx * 0.92 * math.cos(a))}" cy="{f1(cy + ry * 0.9 * math.sin(a))}" r="{f1(0.34 * ry)}" ATTR/>'
    puff += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" ATTR/>'
    fill = "#fff8ea"
    body = puff.replace("ATTR", f'fill="{fill}" stroke="{INK}" stroke-width="9"') + puff.replace("ATTR", f'fill="{fill}"')
    tx, ty = tail_to
    for k, r_ in ((0.55, 20), (0.75, 14), (0.9, 9)):
        px_, py_ = cx + (tx - cx) * k, cy + ry * 0.6 + (ty - cy - ry * 0.6) * k
        body += f'<circle cx="{f1(px_)}" cy="{f1(py_)}" r="{r_}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
    return S.g(body, filter="wobble-fine") + content


def sun_local(r=50):
    rays = S.rays(0, 0, r * 1.25, r * 1.85, n=12, width_deg=11)
    out = f'<path d="{rays}" fill="#ffd36e" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" stroke-width="3"/>'
    out += f'<circle cx="0" cy="0" r="{r}" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.35)}" stroke-width="4"/>'
    out += f'<circle cx="{-r * 0.36}" cy="{-r * 0.1}" r="{r * 0.09}" fill="{INK}"/><circle cx="{r * 0.36}" cy="{-r * 0.1}" r="{r * 0.09}" fill="{INK}"/>'
    out += f'<path d="M{-r * 0.34},{r * 0.22} Q0,{r * 0.52} {r * 0.34},{r * 0.22}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    out += f'<circle cx="{-r * 0.6}" cy="{r * 0.2}" r="{r * 0.14}" fill="#f6a07a" opacity="0.7"/><circle cx="{r * 0.6}" cy="{r * 0.2}" r="{r * 0.14}" fill="#f6a07a" opacity="0.7"/>'
    return out


def sun_svg(i):
    x, y = SUNS[i]
    num = (f'<circle cx="74" cy="-70" r="30" fill="#fff6dc" stroke="{S.mix(P["sun_hot"], INK, 0.4)}" stroke-width="4"/>'
           + S.text(74, -52, str(i + 1), size=48, fill=S.mix(P["sun_hot"], INK, 0.55)))
    return doc(S.g(f'<g transform="translate({x},{y})">{sun_local()}</g>', filter="wobble-fine")
               + f'<g transform="translate({x},{y})">{num}</g>')


def light_rays_svg(ox, oy, tx, ty, spread, length_k, pool, uid, n=5):
    """Soft golden rays from a point above the frame (ox, oy) toward (tx, ty), fanning +-spread degrees, and a
    warm pool of light at the target (God's light — never a figure)."""
    ang = math.degrees(math.atan2(ty - oy, tx - ox))
    dist = math.hypot(tx - ox, ty - oy) * length_k
    defs = (S.lin_grad(uid, [(0, "#fff1b8", 0.0), (0.35, "#ffe9a0", 0.55), (1, "#ffe39a", 0.12)],
                       x1=0, y1=0, x2=1, y2=0)
            + S.rad_grad(uid + "p", [(0, "#fff3c6", 0.85), (0.5, "#ffe9a8", 0.35), (1, "#ffe9a8", 0)]))
    body = ""
    for i in range(n):
        a = ang + spread * (2 * i / (n - 1) - 1)
        w = 22 + 10 * (i % 2)
        body += (f'<path d="M0,-6 L{f1(dist)},{-w} L{f1(dist)},{w} L0,6 Z" fill="url(#{uid})" '
                 f'transform="translate({ox},{oy}) rotate({a:.2f})"/>')
    body = f'<g filter="url(#soft)">{body}</g>'
    rx, ry = pool
    body += f'<ellipse cx="{tx}" cy="{ty}" rx="{rx}" ry="{ry}" fill="url(#{uid}p)"/>'
    return doc(body, defs)


def trail_dot_pts():
    """Points of the golden dotted trail from the window to Jerusalem (a high arc westward)."""
    x0, y0 = WIN_X - 120, WIN_Y - 150
    x1, y1 = JERUSALEM[0] + 30, JERUSALEM[1] - 70
    pts = []
    n = 24
    for i in range(n):
        u = i / (n - 1)
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - 260 * math.sin(math.pi * u)
        pts.append((x, y))
    return pts


def trail_dot_svg(x, y, r):
    return doc(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r * 2.4}" fill="#fff1b8" opacity="0.6" filter="url(#soft)"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="#ffd96a" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
               f'stroke-width="2.5"/>')


# ------------------------------------------------------------------ performers
class Perf:
    """A character on a Sprite: a schedule of drawings with squash-and-hop pose changes, a position function and
    optional alpha / darkening. sched: [(t, drawing index, hop amplitude)]; walk drawings are picked by walk_fn."""

    def __init__(self, sp, sched, pos, walk=None, alpha=None, dark=None, breathe=0.010, bper=3.0, phase=0.0):
        self.sp, self.sched, self.pos, self.walk = sp, sorted(sched, key=lambda e: e[0]), pos, walk
        self.alpha, self.dark, self.breathe, self.bper, self.phase = alpha, dark, breathe, bper, phase
        self._dk = {}

    def frame(self, t):
        if self.walk:
            w = self.walk(t)
            if w is not None:
                return w
        f = self.sched[0][1]
        for ts, fr, *_ in self.sched:
            if t >= ts:
                f = fr
        return f

    def hop(self, t):
        sy, dy = 1.0, 0.0
        for ts, fr, amp in self.sched:
            if amp <= 0:
                continue
            u = t - ts
            if -0.09 <= u <= 0.22:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.22, "sine")
                dy = -12 * amp * math.sin(math.pi * clamp((u + 0.01) / 0.23))
        return sy, dy

    def __call__(self, t):
        a = 1.0 if self.alpha is None else self.alpha(t)
        if a <= 0.002:
            return None
        x, y = self.pos(t)
        hs, hd = self.hop(t)
        b = 1 + self.breathe * math.sin(2 * math.pi * (t / self.bper + self.phase))
        walking = self.walk is not None and self.walk(t) is not None
        sy = hs * (1.0 if walking else b)
        sx = 1 + 0.5 * (1 - hs)
        out = self.sp.place(self.frame(t), x, y, sx, sy, hd, a)
        if out is None or self.dark is None:
            return out
        k = round(self.dark(t) * 10) / 10
        if k <= 0:
            return out
        im, xy = out
        key = (id(im), k)
        if key not in self._dk:
            arr = np.asarray(im).astype(np.float32)
            tgt = np.array([62, 43, 32], np.float32)
            arr[..., :3] = arr[..., :3] * (1 - k) + tgt * k
            if len(self._dk) > 60:
                self._dk.clear()
            self._dk[key] = Image.fromarray(arr.astype(np.uint8), "RGBA")
        return self._dk[key], xy


def fig(D, m, ps, expr, x, y, s, facing, label, marks=True):
    inner, _ = C._figure(D, m, ps, expr, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


# scene-local Daniel poses
BRAVE = C._P(h=-8, arms=(("fk", 14, 8), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"), expr="happy")
OPEN_ARMS = C._P(h=-4, arms=(("fk", 70, 96), ("fk", -70, -96)), hands=("open", "open"), expr="happy")
LOOK_WEST = C._P(h=-8, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="happy", look=(0.04, -0.03))


def dan(sp, pose, expr=None, facing=1, ps=None):
    if ps is not None:
        return sp.add(fig(C._daniel_design(), C._DANIEL_M, dict(ps), expr or ps["expr"], sp.ax, sp.ay, K, facing,
                          "daniel-x"))
    return sp.add(C.daniel(sp.ax, sp.ay, K, facing, pose=pose, expr=expr))


def walk_drawings(sp, D, m, s, facing, expr="neutral", A=WALK_A, label="w", arm_ps=None, **over):
    """2*WALK_N planted-foot walk drawings on sprite sp; returns their indices. ``over`` overrides pose keys."""
    idx = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k, A=A)
        if arm_ps is not None:
            ps["arms"], ps["hands"] = arm_ps["arms"], arm_ps["hands"]
        ps.update(over)
        idx.append(sp.add(fig(D, m, ps, expr, sp.ax, sp.ay, s, facing, label)))
    return idx


# ================================================================== shared layer groups (s06 reuses them)
def _al(m, alpha):
    """Multiply a motion's opacity by alpha(t) (s06 hides the street once the palace has dissolved in)."""
    if alpha is None:
        return m
    if m is None:
        return lambda t: Tf(alpha=alpha(t))
    return lambda t: (lambda v: Tf(v.dx, v.dy, v.rot, v.sx, v.sy, v.alpha * alpha(t), v.px, v.py))(m(t))


def add_backdrop(sc, toff=0.0, alpha=None):
    """Sky and drifting clouds. toff shifts the clocks of every cyclic motion (s06 passes s05's end time so the
    dissolve between the two scenes matches)."""
    sc.add("sky", sky_svg(), wc=0.45)
    for i, v in enumerate((5, 4, 6, 3.5, 4.5)):
        sc.add(f"cloud{i}", clouds_svg(i), wc=0.7,
               motion=_al(_shift(M.combine(M.drift(vx=-v), M.bob(3, 7 + i, i * 0.3)), toff), alpha))


def add_far(sc):
    sc.add("far", far_svg(), wc=0.7)


def add_street(sc):
    sc.add("wall", wall_svg(), wc=0.8)
    sc.add("decree", decree_svg(), wc=0.5)
    sc.add("street", street_svg(), wc=0.8)
    sc.add("door_dark", door_dark_svg(), wc=0.3)


def add_house(sc, toff=0.0):
    sc.add("house", house_svg(), wc=0.8)


def add_doves(sc, toff=0.0, alpha=None):
    for i, (x, f) in enumerate(((1760, 1), (2560, -1))):
        y = ROOF_Y - 64 - 34
        sc.add(f"dove{i}", doc(PR.dove(x, y, 0.55, f, pose="stand")), wc=0.5,
               motion=_al(lambda t, i=i, x=x, y=y: Tf(
                   dy=-3 * max(0, math.sin(2 * math.pi * ((t + toff) / (1.7 + 0.3 * i)))),
                   rot=3 * math.sin(2 * math.pi * (t + toff) / (2.3 + 0.4 * i)), px=x, py=y + 30), alpha))


def add_front(sc, toff=0.0, alpha=None):
    sc.add("stair", stair_svg(), wc=0.8)
    sc.add("jars", jars_svg(), wc=0.7)
    for i, (x, s) in enumerate(((430, 0.82), (3060, 0.9))):
        frames = [palm_svg(x, GY + 6, s, sw) for sw in (-0.5, 0.0, 0.5)]
        sc.add(f"palm{i}", frames, wc=0.7, motion=_al(None, alpha),
               frame_at=lambda t, i=i: 1 + math.sin(2 * math.pi * ((t + toff) / (3.6 + 0.5 * i) + 0.3 * i)))
    sc.add("fg", fg_svg(), wc=0.7)


def _shift(m, toff):
    return m if not toff else (lambda t: m(t + toff))


def window_daniel_sprite():
    """Daniel in the window: (sprite, {name: drawing index})."""
    sp_in = sprite(420, 420, 210, 380, seed=51)
    d = dict(open=dan(sp_in, None, ps=OPEN_ARMS, facing=-1), west=dan(sp_in, None, ps=LOOK_WEST, facing=-1),
             pray=dan(sp_in, "kneel_pray", facing=-1), bow=dan(sp_in, "kneel_bow", facing=-1),
             up=dan(sp_in, "kneel_up", facing=-1))
    return sp_in, d


WIN_BREATHE = (0.012, 3.2)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]

    # ---------------------------------------------------------------- beats (all from the narration)
    t_think = phrase_t(L0, "命令", 0.6) - 0.1          # hand to chin
    t_brave = L0.chunks[1].start + 0.05                # "可是他没有害怕" hop-turn, hand on chest, chin up
    t_nod = phrase_t(L0, "也没有躲起来", 0.6)          # a calm nod
    t_danger = L1.start + 0.05                         # "他知道这样做会有危险" hand to chin
    t_b_in = L1.start + 0.25                           # lion bubble
    t_b_out = L1.chunks[1].start - 0.05                # "可是他更相信上帝" bubble pops
    t_light = L1.chunks[1].start + 0.05                # golden light, he looks up
    t_chest = L1.end - 1.0                             # hand on chest again
    t_walk = L1.end - 0.55                             # sets off home
    t_door = L2.chunks[1].start + 0.25                 # reaches the upper door
    t_open = phrase_t(L2, "耶路撒冷", 0.4) - 0.05      # shutters swing open
    t_turn = t_open + 0.85                             # turns to face west
    t_trail = t_open + 0.45                            # golden trail to Jerusalem
    t_trail_end = t_trail + 1.2
    t_suns = phrase_t(L3, "一天三次", 0.3)
    sun_ts = [t_suns - 0.1, t_suns + 0.35, t_suns + 0.8]
    t_kneel = L3.chunks[1].start + 0.05                # "跪下来向上帝祷告"
    t_thanks = phrase_t(L3, "感谢上帝", 0.75)
    t_fold = min(L3.end + 0.25, T - 1.1)

    # ---------------------------------------------------------------- SKY + DISTANCE
    add_backdrop(sc)
    sc.add("jglow", jerusalem_glow_svg(), wc=0, motion=lambda t: Tf(
        alpha=M.progress(t, t_trail_end - 0.3, t_trail_end + 0.4, "sine") *
        (1 - 0.6 * M.progress(t, t_trail_end + 1.2, t_trail_end + 2.4, "sine"))))
    add_far(sc)

    # three suns ("一天三次"): pop in one after the other, bob, fade away before the prayer light
    for i in range(3):
        cx, cy = SUNS[i]
        t0 = sun_ts[i]

        def sun_m(t, t0=t0, cx=cx, cy=cy, i=i):
            if t < t0:
                return Tf(alpha=0.0)
            u = t - t0
            k = M.ease("back")(clamp(u / 0.35)) if u < 0.35 else 1.0
            a = 1 - M.progress(t, t_thanks - 0.4, t_thanks + 0.8, "sine")
            return Tf(sx=max(0.01, k), sy=max(0.01, k), dy=4 * math.sin(2 * math.pi * (u / 2.2 + i * 0.3)),
                      rot=3 * math.sin(2 * math.pi * u / 3.0), alpha=a, px=cx, py=cy)
        sc.add(f"sun{i}", sun_svg(i), wc=0.4, motion=sun_m)

    # ---------------------------------------------------------------- STREET, WALL, HOUSE
    add_street(sc)
    glows = [window_back_svg(g) for g in (0.0, 0.35, 0.7, 1.0)]
    glow_k = lambda t: 3 * M.progress(t, t_kneel + 0.2, t_kneel + 1.6, "sine")
    sc.add("win_back", glows, wc=0.5, frame_at=glow_k)

    # Daniel inside the window (between the room and the wall)
    sp_in, DI = window_daniel_sprite()
    di_open, di_west, di_pray, di_up = DI["open"], DI["west"], DI["pray"], DI["up"]
    in_sched = [(0, di_open, 0), (t_turn, di_west, 0.6)]
    for ts in sun_ts:                                  # a little nod with each sun
        if ts + 0.05 < t_kneel - 0.25:
            in_sched += [(ts + 0.05, di_west, 0.5)]
    in_sched += [(t_kneel, di_pray, 1.0), (t_thanks, di_up, 0.9), (t_fold, di_pray, 0.7)]
    stand_y = FLOOR_UP + 22                           # standing a step back in the room

    def in_pos(t):
        return WIN_X - 6, (FLOOR_UP if t >= t_kneel else stand_y)

    sc.add_dynamic("daniel_in", Perf(sp_in, in_sched, in_pos, alpha=lambda t: 1.0 if t >= t_door + 0.2 else 0.0,
                                     breathe=WIN_BREATHE[0], bper=WIN_BREATHE[1]))

    add_house(sc)
    opens = [window_front_svg(o) for o in (0.0, 0.25, 0.5, 0.75, 1.0)]
    sc.add("win_front", opens, wc=0.6, frame_at=lambda t: float(min(4, max(0, int((t - t_open) / 0.11) + 1)))
           if t >= t_open else 0.0)

    add_doves(sc)

    # ---------------------------------------------------------------- DANIEL outside
    sp = sprite(440, 420, 220, 380, seed=50)
    d_read = dan(sp, "stand", facing=-1)
    d_think = dan(sp, "listen", facing=-1)
    d_brave = dan(sp, None, ps=BRAVE, facing=1)
    d_brave_l = dan(sp, None, ps=BRAVE, facing=-1)
    d_worry = dan(sp, "listen", facing=1)
    d_up = dan(sp, "look_up", facing=1)
    W = walk_drawings(sp, C._daniel_design(), C._DANIEL_M, K, 1, "neutral", label="dwalk")
    adv = 2 * WALK_A / WALK_N * K                      # stage px per walk drawing (planted sole stays put)
    dist_flat = STAIR_X0 - READ_X
    slope = (GY - FLOOR_UP) / (STAIR_X1 - STAIR_X0)
    n_draw = int(math.ceil((DOOR_X - READ_X) / adv))
    rate = n_draw / (t_door - t_walk)

    def walk_k(t):
        if t < t_walk or t >= t_door:
            return None
        return min(n_draw, int((t - t_walk) * rate + 1e-6))

    def walk_frame(t):
        k = walk_k(t)
        return None if k is None else W[k % (2 * WALK_N)]

    def out_pos(t):
        if t < t_walk:
            return READ_X, GY
        k = walk_k(t)
        if k is None:
            k = n_draw
        x = READ_X + k * adv
        if x <= STAIR_X0:
            return x, GY
        if x <= STAIR_X1:
            return x, GY - (x - STAIR_X0) * slope
        return x, FLOOR_UP

    out_sched = [(0, d_read, 0), (t_think, d_think, 0.5), (t_brave, d_brave, 1.0), (t_nod, d_brave, 0.45),
                 (t_danger, d_worry, 0.6), (t_light, d_up, 0.9), (t_chest, d_brave, 0.6),
                 (t_walk - 0.12, W[0], 0.3)]
    dark = lambda t: M.progress(t, t_door - 0.45, t_door - 0.05, "sine") * 0.85
    sc.add_dynamic("daniel_out", Perf(sp, out_sched, out_pos, walk=walk_frame, dark=dark,
                                      alpha=lambda t: 1 - M.progress(t, t_door - 0.12, t_door + 0.12, "sine"),
                                      breathe=0.010, bper=3.0))
    # contact shadow on the street while he stands there
    sc.add("dshadow", doc(C.ground_shadow(READ_X, GY, K, width=130, opacity=0.24)), wc=0,
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_walk, t_walk + 0.3, "sine")))

    add_front(sc)

    # ---------------------------------------------------------------- the lion thought bubble
    bx, by = READ_X + 235, 845
    head = (READ_X + 20, 1040)
    lion = PR.lion(bx + 6, by + 88, 0.42, -1, pose="stand", mouth=0.66)
    sc.add("bubble", doc(bubble_svg(bx, by, 190, 128, head, lion)), wc=0.4, motion=lambda t: _pop(t, t_b_in, t_b_out, bx, by + 60))

    # ---------------------------------------------------------------- God's light on Daniel (light only)
    beam_a = lambda t: (M.progress(t, t_light - 0.05, t_light + 0.7, "sine") *
                        (1 - M.progress(t, t_walk + 0.4, t_walk + 1.6, "sine")) *
                        (0.85 + 0.15 * math.sin(2 * math.pi * (t - t_light) / 2.4)))
    sc.add("beam1", light_rays_svg(READ_X - 260, 300, READ_X - 10, GY - 20, 6, 1.0, (190, 46), "s5b1"), wc=0,
           blend="screen", motion=lambda t: Tf(alpha=0.9 * beam_a(t)))
    win_a = lambda t: (M.progress(t, t_kneel + 0.1, t_kneel + 1.2, "sine") *
                       (0.85 + 0.15 * math.sin(2 * math.pi * (t - t_kneel) / 2.6)))
    sc.add("beam2", light_rays_svg(WIN_X - 420, 120, WIN_X - 60, WIN_Y - 60, 5, 0.92, (210, 70), "s5b2"), wc=0,
           blend="screen", motion=lambda t: Tf(alpha=0.75 * win_a(t)))

    # golden trail from the window to Jerusalem
    pts = trail_dot_pts()
    for i, (x, y) in enumerate(pts):
        ti = t_trail + (t_trail_end - t_trail) * i / (len(pts) - 1)
        r = 14 - 6 * i / len(pts)

        def dot_m(t, ti=ti, x=x, y=y):
            if t < ti:
                return Tf(alpha=0.0)
            u = t - ti
            k = M.ease("back")(clamp(u / 0.25))
            a = 1 - M.progress(t, t_trail_end + 1.0, t_trail_end + 2.0, "sine")
            return Tf(sx=max(0.01, k), sy=max(0.01, k), alpha=a, px=x, py=y)
        sc.add(f"dot{i}", trail_dot_svg(x, y, r), wc=0, motion=dot_m)

    # ---------------------------------------------------------------- CAMERA
    camA0, camA1 = Cam(1330, 1018, 1320), Cam(1345, 1012, 1290)
    camB = Cam(1800, 878, 1800)
    camD0, camD1 = Cam(2330, 742, 1500), Cam(2338, 738, 1460)
    sc.camera = M.cam_keys([
        (0.0, camA0), (t_walk - 0.2, camA1), (t_door - 0.1, camB), (t_trail_end + 0.25, Cam(1795, 874, 1800)),
        (t_suns - 0.1, camD0), (T, camD1)], "sine")

    # ---------------------------------------------------------------- FX
    sc.fx = [
        FX.motes((300, 300, 3000, 1300), count=26, color=(255, 246, 214), size=(3, 6), alpha=100),
        FX.sparkles((READ_X - 260, 560, READ_X + 160, 930), count=14, t0=t_light + 0.1, t1=t_walk + 0.6,
                    color=(255, 238, 170), size=(8, 16), period=1.5, drift=-14, seed=7),
        FX.sparkles((WIN_X - 330, 420, WIN_X + 230, 640), count=14, t0=t_kneel + 0.3, t1=T + 1,
                    color=(255, 238, 170), size=(8, 16), period=1.6, drift=-8, seed=9),
    ]

    # ---------------------------------------------------------------- SOUND
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", 0, dur=t_door + 1.0, gain_db=-27, fade_in=0.8, fade_out=1.5, pan=-0.3)
    sc.sfx("cloth", t_think, gain_db=-17)
    sc.sfx("cloth", t_brave, gain_db=-15)
    sc.sfx("pop", t_b_in, gain_db=-12, pan=0.2)
    sc.sfx("pop", t_b_out, gain_db=-14, pan=0.2)
    sc.sfx("chime", t_light - 0.1, gain_db=-9)
    sc.sfx("footsteps", t_walk, dur=t_door - t_walk, gain_db=-14, fade_in=0.1, fade_out=0.3, pan=0.15)
    sc.sfx("whoosh", t_open - 0.05, gain_db=-18, pan=0.3)
    sc.sfx("thud", t_open + 0.42, gain_db=-17, pan=0.3)
    sc.sfx("sparkle", t_trail + 0.1, gain_db=-14, pan=-0.2)
    for i, ts in enumerate(sun_ts):
        sc.sfx("pop", ts, gain_db=-11, pan=(0.35, 0.0, -0.35)[i])
    sc.sfx("cloth", t_kneel, gain_db=-14, pan=0.2)
    sc.sfx("thud", t_kneel + 0.06, gain_db=-20, pan=0.2)
    sc.sfx("chime", t_kneel + 0.2, gain_db=-11, pan=0.2)
    sc.sfx("sparkle", t_thanks, gain_db=-14, pan=0.2)
    return sc


def _pop(t, t_in, t_out, px, py):
    """Bubble pop-in (overshoot) and pop-out (quick puff up and vanish)."""
    if t < t_in or t > t_out + 0.2:
        return Tf(alpha=0.0)
    if t < t_out:
        u = t - t_in
        k = M.ease("back")(clamp(u / 0.35))
        return Tf(sx=max(0.01, k), sy=max(0.01, k), dy=-4 * math.sin(2 * math.pi * u / 2.0), px=px, py=py)
    u = (t - t_out) / 0.2
    return Tf(sx=1 + 0.15 * u, sy=1 + 0.15 * u, alpha=1 - u, px=px, py=py)
