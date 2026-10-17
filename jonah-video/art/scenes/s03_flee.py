"""Scene 3 — Jonah flees to Joppa and boards a ship for Tarshish (Jonah 1:3).

Staging (one wide panorama; west = left, east = right; no cuts):
  * line 0 '可是约拿不想去。' — a sunny crossroads on the coastal road. The signpost shows 他施 pointing left (west)
    and 尼尼微 pointing right (east). Jonah looks at the Nineveh arrow, puts his palm out and shakes his head
    (pose 'refuse', scared), then spins round (whoosh).
  * line 1 '他跑到海边的约帕，坐上一条开往他施的船，' — he runs west (run_a / run_b flipbook) along the road into
    the harbour of Joppa; the camera pans with him (smoothed, always leftward) over the hill town with its stone
    walls, the harbour wall and the wooden pier. A pier sailor swings a jar up to the sailor on deck, who
    catches it and stows it behind the rail; Jonah dashes past the sailors and leaps aboard over the rail
    (whoosh, thud).
  * line 2 '想要躲开上帝。' — the deck sailor hauls the halyard and the sail unrolls down from the yard, the
    captain points west and the ship sails away from the pier toward the open sea (bow wave, foam streaming
    back along the hull); Jonah ducks behind the stern rail beside the cargo and peeks back nervously at the
    shore, where the pier sailors set their cargo down and point after the ship. The camera settles before
    the closing dissolve.

Depth order (back -> front): sky, sun, clouds | far sea, hills (parallax 0.25), Joppa town (parallax 0.1) |
harbour wall + moored boat | harbour water, glints | harbour corner block | ship group (hull, halyard, sail,
crew, Jonah, hull cover, rail) | water in front of the hull, glints, hull shadow, bow wave, foam | quay, road,
crossroads, pier | water in front of the pier posts | pier sailors and their cargo, Jonah running |
foreground | gulls.
"""
import math
import random
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 4200, 1188        # the far layers are painted to SW so their parallax never shows an edge
PAINT_R = 3900             # right edge of the painted ground / foreground: the camera never goes past it

K = 0.8                    # person / ship scale
GY = 910                   # walking line: road, quay and pier planks (feet of Jonah)
BACK_Y = 896               # feet of cargo standing on the quay
PIER_Y = GY + 4            # feet of the pier sailors (soles overlap the plank band)
SHIP_X, SHIP_WL = 1520, 968            # docked ship: hull centre on the waterline
DECK = SHIP_WL + PR.SHIP_DECK_Y * K    # 836: feet of people on deck
RAIL = SHIP_WL - 220 * K               # ~792: top of the rail
PIER_X0, PIER_X1 = 1420, 2200
QUAY_X = 2190              # where the stone quay / land begins
SIGN_X, SIGN_Y = 3580, 898
JX0 = 3360                 # Jonah's spot at the crossroads
BOARD_X = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, -150, PR.SHIP_DECK_Y)[0]   # Jonah on deck (stern side)
LEAP_X = BOARD_X + 120     # where he takes off from the pier
SEA_RIGHT = 2260           # sea layers end under the quay / behind the harbour corner block
SEA_FAR_R = 2950           # the far sea ends behind the eastern hills (no sea on the Nineveh side)

P1X, P2X = 2120, 1950      # pier sailors: P1 carries a crate, P2 swings a jar up to the ship
DECK_SAILOR_LX = 90        # deck sailor (local ship x): by the mast, catches the jar, then hauls the halyard
CAPTAIN_LX = 230           # captain near the bow

SHIP_SEED = 211            # shared watercolour seed: ship_back and the unrolling sail band match pixel for pixel
OLIVE_LEAF, OLIVE_DARK, OLIVE_BARK = "#a3b08a", "#7d8c69", "#9a8c78"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def ugrad(id_, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a[0] if a else 1}"/>' for o, c, *a in stops)
    return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" '
            f'y2="{y2}">{s}</linearGradient>')


def no_olive_dots(markup):
    """PR.olive_tree's small dark olives read as eyes / mouths at background scales: drop them."""
    return re.sub(r'<ellipse[^>]*fill="#5c4a63"[^>]*/>', "", markup)


def ship_place(body):
    """Local ship markup (facing right, scale 1, anchor = waterline centre) -> stage, mirrored like the ship."""
    return (f'<g filter="url(#wobble-fine)"><g transform="translate({SHIP_X},{SHIP_WL}) scale({-K},{K})">'
            f'{body}</g></g>')


def compose(b, pivot, dx=0.0, dy=0.0, sx=1.0, sy=1.0, rot=0.0, alpha=1.0):
    """A local motion (scale / rotate about ``pivot``, then shift) followed by the ship transform ``b``.

    Returns one Tf (pivot = ``pivot``) so things on deck can dip, squash or lean while riding the ship."""
    s = b.sx
    a = math.radians(b.rot)
    c, si = math.cos(a), math.sin(a)
    vx, vy = pivot[0] + dx - b.px, pivot[1] + dy - b.py
    nx = b.px + b.dx + s * (c * vx - si * vy)
    ny = b.py + b.dy + s * (si * vx + c * vy)
    return Tf(dx=nx - pivot[0], dy=ny - pivot[1], rot=b.rot + rot, sx=s * sx, sy=s * sy, alpha=b.alpha * alpha,
              px=pivot[0], py=pivot[1])


def apply_tf(tf, x, y, pivot):
    """Stage position of point (x, y) of a layer moved by ``tf`` (pivot default ``pivot``)."""
    px = tf.px if tf.px is not None else pivot[0]
    py = tf.py if tf.py is not None else pivot[1]
    a = math.radians(tf.rot)
    c, s = math.cos(a), math.sin(a)
    vx, vy = (x - px) * tf.sx, (y - py) * tf.sy
    return px + tf.dx + c * vx - s * vy, py + tf.dy + s * vx + c * vy


def mid(pts):
    return (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2


# ============================================================================ background pieces


def sky_svg():
    defs = ugrad("s3sky", 0, 0, 0, 760, [(0, "#7fc0dc"), (0.45, P["sky_day"]),
                                          (0.85, S.mix(P["sky_day"], "#fff6dc", 0.55)), (1, "#fbf1d6")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s3sky)"/>', defs)


SUN = (3195, 300)


def sun_svg():
    x, y = SUN
    defs = S.rad_grad("s3sunglow", [(0, "#fffbe6", 0.95), (0.3, "#fff1bf", 0.6), (1, "#fff1bf", 0)])
    body = (f'<circle cx="{x}" cy="{y}" r="330" fill="url(#s3sunglow)"/>' +
            S.g(f'<circle cx="{x}" cy="{y}" r="62" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], P["ink"], 0.2)}" '
                f'stroke-width="3.5"/>'
                f'<circle cx="{x - 18}" cy="{y - 20}" r="22" fill="#fff3c4" opacity="0.7"/>', filter="wobble"))
    return doc(body, defs)


def clouds_svg():
    items = [(1150, 205, 330, 105, 1), (1650, 330, 210, 70, 2), (2150, 150, 300, 95, 3), (2850, 215, 360, 115, 4),
             (3350, 120, 240, 80, 5), (3800, 290, 320, 100, 6), (760, 300, 240, 80, 7)]
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, "#fffaf0", seed=seed, sw=3, shade_fill="#dbe9ee")
    return doc(S.g(body, filter="wobble"))


HZ = 560   # horizon


def tree(x, y, s, seed=0, col=None, haze=0.0, trunk=None):
    """Simple round picture-book tree (trunk + three leafy puffs), for small distant trees."""
    rng = random.Random(seed)
    col = col or S.mix(P["olive"], P["leaf"], rng.uniform(0.2, 0.6))
    col = S.mix(col, P["sky_day"], haze)
    dark = S.shade(col, -0.22)
    trunk = S.mix(trunk or P["wood_dark"], P["sky_day"], haze)
    sw = max(1.6, 3.2 * s)
    out = (f'<path d="M{f1(x - 7 * s)},{f1(y)} Q{f1(x - 3 * s)},{f1(y - 50 * s)} {f1(x - 2 * s)},{f1(y - 88 * s)} '
           f'L{f1(x + 6 * s)},{f1(y - 88 * s)} Q{f1(x + 5 * s)},{f1(y - 45 * s)} {f1(x + 9 * s)},{f1(y)} Z" '
           f'fill="{trunk}" stroke="{P["ink"]}" stroke-width="{f1(sw)}" stroke-linejoin="round"/>')
    puffs = [(-30, -100, 38, 30), (26, -104, 36, 30), (0, -132, 42, 34)]
    for dx, dy, rx, ry in puffs:
        out += (f'<ellipse cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" rx="{f1(rx * s)}" ry="{f1(ry * s)}" '
                f'fill="{col}" stroke="{P["ink"]}" stroke-width="{f1(sw * 2)}"/>')
    for dx, dy, rx, ry in puffs:
        out += f'<ellipse cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" rx="{f1(rx * s)}" ry="{f1(ry * s)}" fill="{col}"/>'
    out += (f'<ellipse cx="{f1(x - 4 * s)}" cy="{f1(y - 100 * s)}" rx="{f1(46 * s)}" ry="{f1(14 * s)}" fill="{dark}" '
            f'opacity="0.45"/>'
            f'<ellipse cx="{f1(x - 10 * s)}" cy="{f1(y - 142 * s)}" rx="{f1(16 * s)}" ry="{f1(10 * s)}" '
            f'fill="{S.shade(col, 0.3)}" opacity="0.7"/>')
    return out


def olive(x, y, s, seed=0):
    """Distant olive tree: grey-green puffs on a grey-brown trunk, no olives (they read as faces when small)."""
    return tree(x, y, s, seed=seed, col=OLIVE_LEAF, trunk=OLIVE_BARK)


# The far layer and the town move with camera parallax (anchored at the opening frame): by the end of the
# scene the far layer has slid about FAR_SHIFT px left. Things that should sit in a particular place in the
# closing frame (the rocks off Joppa, a horizon ship) are painted FAR_SHIFT px further right.
FAR_SHIFT = 460


def far_svg():
    """Open sea to the horizon, a distant ship, the rocks off Joppa, hazy hills to the east."""
    hz = HZ
    defs = (ugrad("s3farsea", 0, hz, 0, SH, [(0, S.mix(P["sea_pale"], "#eef6ee", 0.35)), (0.22, P["sea_pale"]),
                                             (0.6, P["sea_light"]), (1, S.mix(P["sea_light"], P["sea"], 0.5))]) +
            ugrad("s3hill1", 0, 420, 0, 700, [(0, S.mix(P["olive"], P["sky_day"], 0.62)),
                                               (1, S.mix(P["olive"], P["sky_day"], 0.45))]) +
            ugrad("s3hill2", 0, 560, 0, 900, [(0, S.mix(P["grass"], P["sky_day"], 0.32)),
                                               (1, S.mix(P["grass"], P["sand"], 0.35))]))
    sea_w = SEA_FAR_R + 20
    body = f'<rect x="-20" y="{hz}" width="{sea_w}" height="{SH - hz + 40}" fill="url(#s3farsea)"/>'
    body += (f'<path d="M-20,{hz} L{SEA_FAR_R},{hz}" stroke="{P["ink"]}" stroke-width="2.2" opacity="0.5"/>'
             f'<rect x="-20" y="{hz - 30}" width="{sea_w}" height="40" fill="#fbf4dc" opacity="0.35" '
             f'filter="url(#soft)"/>')
    # sun glitter streaks on the far sea
    rng = random.Random(3)
    for i in range(60):
        x = rng.uniform(0, SEA_FAR_R - 150)
        y = hz + 12 + (rng.random() ** 1.6) * 280
        w = rng.uniform(16, 44) * (0.6 + (y - hz) / 300)
        body += (f'<path d="M{f1(x)},{f1(y)} l{f1(w)},0" stroke="#fbfdf6" stroke-width="2.6" '
                 f'stroke-linecap="round" opacity="{rng.uniform(0.35, 0.7):.2f}"/>')
    # a distant ship on the horizon, behind the town end of the harbour where nothing covers it
    # (hull below its waterline painted over with sea)
    for x, y, s, f in ((2350, 592, 0.075, -1),):
        body += PR.ship(x, y, s, f, sail="full", lantern=False)
        body += f'<rect x="{x - 70}" y="{y}" width="140" height="16" fill="url(#s3farsea)"/>'
    # the rocks off Joppa (they slide into place west of the departing ship by the end)
    rocks = ""
    rock_c = S.mix(P["stone_dark"], P["sky_day"], 0.3)
    ox = FAR_SHIFT
    for x, base, w, h in ((440, 668, 120, 92), (530, 672, 80, 56), (365, 674, 60, 34), (610, 676, 44, 24)):
        x += ox
        pk = [(x - w / 2, base), (x - w * 0.36, base - h * 0.55), (x - w * 0.14, base - h * 0.82),
              (x + w * 0.04, base - h), (x + w * 0.22, base - h * 0.7), (x + w * 0.4, base - h * 0.45),
              (x + w / 2, base)]
        d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pk) + " Z"
        rocks += S.path(d, fill=rock_c, sw=2.8)
        rocks += (f'<path d="M{f1(x + w * 0.04)},{f1(base - h)} L{f1(x + w * 0.22)},{f1(base - h * 0.7)} '
                  f'L{f1(x + w * 0.4)},{f1(base - h * 0.45)} L{f1(x + w / 2)},{f1(base)} L{f1(x + w * 0.08)},'
                  f'{f1(base)} Z" fill="{S.shade(rock_c, -0.18)}" opacity="0.6"/>')
    rocks += (f'<path d="M{340 + ox},676 q40,-9 80,0 t80,0 t80,0 t60,0" stroke="{P["foam"]}" stroke-width="5" '
              f'fill="none" stroke-linecap="round" opacity="0.85"/>')
    body += S.g(rocks, filter="wobble")
    # far hills to the east (toward Nineveh): they run past the right edge of the stage and hide the end of
    # the far sea, so there is only land and sky on the Nineveh side
    far_hills = S.path(S.hill(2000, 4100, 640, 175, seed=11, bottom=900, bumps=5), fill="url(#s3hill1)", sw=2.5)
    near_hills = S.path(S.hill(2850, 4050, 880, 280, seed=4, bottom=1000, bumps=3), fill="url(#s3hill2)", sw=3)
    body += S.g(far_hills, filter="wobble")
    trees = ""
    for i, (x, y, sc) in enumerate(((2580, 566, 0.32), (2625, 560, 0.28), (3130, 524, 0.3), (3175, 528, 0.34),
                                    (3660, 548, 0.3), (3712, 542, 0.28), (3990, 520, 0.3))):
        trees += tree(x, y, sc, seed=i, haze=0.45)
    body += S.g(trees, filter="wobble-fine")
    body += S.g(near_hills, filter="wobble")
    grove = ""
    for i, (x, y, sc) in enumerate(((3150, 708, 0.62), (3205, 700, 0.5), (3300, 668, 0.55), (3690, 650, 0.58),
                                    (3745, 655, 0.48), (3880, 690, 0.6), (3440, 672, 0.45))):
        grove += tree(x, y, sc, seed=i + 10, haze=0.12)
    grove = S.g(grove, filter="wobble-fine")
    # sheep grazing on the slope behind Jonah (well clear of his refusing palm and of the signboards)
    for x, y, f in ((3195, 728, 1), (3252, 718, -1), (3045, 770, 1)):
        grove += PR.animal(x, y, 0.2, f, kind="sheep")
    body += grove
    return doc(body, defs)


def stone_wall(x0, x1, top, height, seed, towers=(), gate=None, uid="w", merlons=True):
    """Light limestone city wall with crenellations; ``top(x)`` gives the wall-top y."""
    rng = random.Random(seed)
    n = 40
    tpts = [(x0 + (x1 - x0) * i / n, top(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    body_d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in tpts)
    body_d += f" L{f1(x1)},{f1(top(x1) + height)} L{f1(x0)},{f1(top(x0) + height)} Z"
    stone = P["stone_light"]
    out = ""
    # merlons
    x = x0 + 6
    while merlons and x < x1 - 20:
        y = top(x + 11)
        out += (f'<path d="M{f1(x)},{f1(y + 2)} L{f1(x)},{f1(y - 16)} Q{f1(x + 11)},{f1(y - 21)} {f1(x + 22)},'
                f'{f1(y - 16)} L{f1(x + 22)},{f1(y + 2)} Z" fill="{stone}" stroke="{P["ink"]}" stroke-width="2.6" '
                f'stroke-linejoin="round"/>')
        x += 38
    cid = f"s3wc{uid}"
    out += f'<clipPath id="{cid}"><path d="{body_d}"/></clipPath>'
    out += f'<path d="{body_d}" fill="{stone}" stroke="{P["ink"]}" stroke-width="3" stroke-linejoin="round"/>'
    # shading toward the bottom + stone courses
    lines = ""
    for i in range(1, 7):
        yy = i * height / 6.5
        pts = " L".join(f"{f1(px)},{f1(py + yy)}" for px, py in tpts[::4])
        lines += f'<path d="M{pts}" stroke="{P["stone_dark"]}" stroke-width="1.6" fill="none" opacity="0.55"/>'
        off = 0 if i % 2 else 22
        xx = x0 + off
        while xx < x1:
            ty = top(xx) + yy
            lines += f'<path d="M{f1(xx)},{f1(ty)} l0,{f1(-height / 6.5)}" stroke="{P["stone_dark"]}" ' \
                     f'stroke-width="1.5" opacity="0.5"/>'
            xx += 44 + rng.uniform(-6, 6)
    lines += (f'<rect x="{x0}" y="{f1(min(y for _, y in tpts) + height * 0.55)}" width="{x1 - x0}" '
              f'height="{height}" fill="{P["stone_dark"]}" opacity="0.22"/>')
    out += f'<g clip-path="url(#{cid})">{lines}</g>'
    if gate:
        gx, gw = gate
        gy = top(gx) + height
        gt = gy - height * 0.78
        out += (f'<path d="M{f1(gx - gw / 2)},{f1(gy)} L{f1(gx - gw / 2)},{f1(gt + gw / 2)} '
                f'A{f1(gw / 2)},{f1(gw / 2)} 0 0 1 {f1(gx + gw / 2)},{f1(gt + gw / 2)} L{f1(gx + gw / 2)},{f1(gy)} Z" '
                f'fill="{S.mix(P["wood_dark"], P["ink"], 0.35)}" stroke="{P["ink"]}" stroke-width="3"/>'
                f'<path d="M{f1(gx - gw / 2 - 7)},{f1(gt + gw / 2)} A{f1(gw / 2 + 7)},{f1(gw / 2 + 7)} 0 0 1 '
                f'{f1(gx + gw / 2 + 7)},{f1(gt + gw / 2)}" stroke="{P["stone_dark"]}" stroke-width="5" fill="none"/>')
    for tx, tw, th in towers:
        ty = top(tx) - th
        by = top(tx) + height + 2
        out += (f'<rect x="{f1(tx - tw / 2)}" y="{f1(ty)}" width="{tw}" height="{f1(by - ty)}" '
                f'fill="{S.mix(stone, P["sand"], 0.25)}" stroke="{P["ink"]}" stroke-width="3"/>'
                f'<rect x="{f1(tx + tw / 2 - tw * 0.3)}" y="{f1(ty)}" width="{f1(tw * 0.3)}" height="{f1(by - ty)}" '
                f'fill="{P["stone_dark"]}" opacity="0.3"/>')
        mx = tx - tw / 2 + 2
        while mx < tx + tw / 2 - 12:
            out += (f'<rect x="{f1(mx)}" y="{f1(ty - 15)}" width="16" height="17" rx="3" '
                    f'fill="{S.mix(stone, P["sand"], 0.25)}" stroke="{P["ink"]}" stroke-width="2.4"/>')
            mx += 26
        out += (f'<rect x="{f1(tx - 5)}" y="{f1(ty + 22)}" width="10" height="24" rx="5" '
                f'fill="{S.mix(P["wood_dark"], P["ink"], 0.4)}"/>')
    return out


def town_svg():
    """Joppa: a hill town above the harbour, stone walls, flat-roofed houses, palms."""
    defs = (ugrad("s3hill", 0, 520, 0, 900, [(0, S.mix(P["grass"], P["sand_light"], 0.45)),
                                               (0.55, S.mix(P["sand"], P["grass"], 0.3)), (1, P["sand"])]) +
            f'<filter id="s3hazef" x="-2%" y="-2%" width="104%" height="104%">'
            f'<feFlood flood-color="{S.mix(P["sky_day"], "#fff6e0", 0.3)}" flood-opacity="0.26" result="f"/>'
            f'<feComposite in="f" in2="SourceGraphic" operator="in" result="h"/>'
            f'<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="h"/></feMerge></filter>')
    hill_pts = [(1660, 880), (1730, 846), (1850, 770), (1990, 672), (2160, 588), (2360, 545), (2560, 548),
                (2760, 590), (2950, 660), (3120, 735), (3300, 800), (3420, 830)]
    hd = S.smooth_path(hill_pts, closed=False) + " L3420,1000 L1660,1000 Z"
    town = S.g(S.path(hd, fill="url(#s3hill)", sw=3.2), filter="wobble")
    # houses: back row on the crest, then rows down the slope (small: the town is across the harbour)
    rows = (((2180, 612, 2, 0.17, 1), (2280, 578, 0, 0.18, -1), (2385, 566, 3, 0.17, 1), (2490, 566, 1, 0.16, 1),
             (2590, 574, 0, 0.17, -1), (2690, 596, 2, 0.16, 1), (2790, 626, 3, 0.16, -1)),
            ((2070, 662, 0, 0.19, 1), (2170, 650, 3, 0.2, -1), (2300, 636, 1, 0.19, 1), (2420, 632, 2, 0.2, -1),
             (2545, 636, 3, 0.19, 1), (2660, 648, 0, 0.2, -1), (2780, 668, 1, 0.18, 1), (2890, 696, 0, 0.18, -1)))
    for row in rows:
        for x, y, v, sc, f in row:
            town += PR.house(x, y, sc, v, f)
    town += PR.palm_tree(2236, 664, 0.22) + PR.palm_tree(2604, 650, 0.2, lean=-0.2)
    town += PR.palm_tree(2360, 668, 0.24, lean=0.2) + PR.palm_tree(2840, 690, 0.2, lean=0.1)

    def wtop(x):
        return 676 + 0.00012 * (x - 2420) ** 2

    town += S.g(stone_wall(1930, 2980, wtop, 70, 7, towers=((1958, 54, 46), (2250, 58, 52), (2600, 58, 52),
                                                              (2960, 50, 42)), gate=(2430, 50), uid="town"),
                filter="wobble-fine")
    # a little watchtower with a flag on the crest
    town += S.g(f'<rect x="2452" y="470" width="56" height="96" fill="{P["stone_light"]}" stroke="{P["ink"]}" '
                f'stroke-width="3"/><rect x="2446" y="458" width="68" height="16" fill="{P["stone"]}" '
                f'stroke="{P["ink"]}" stroke-width="3"/><path d="M2480,458 L2480,410" stroke="{P["wood_dark"]}" '
                f'stroke-width="4"/><path d="M2480,412 q22,6 40,0 q-12,10 0,20 q-20,-6 -40,0 Z" '
                f'fill="{P["terracotta"]}" stroke="{P["ink"]}" stroke-width="2.4"/>'
                f'<rect x="2472" y="494" width="12" height="22" rx="6" fill="{S.mix(P["wood_dark"], P["ink"], 0.4)}"/>',
                filter="wobble-fine")
    # lower town by the harbour, outside the wall
    for x, y, v, sc, f in ((2235, 836, 2, 0.24, 1), (2350, 826, 0, 0.25, -1), (2475, 820, 3, 0.23, 1),
                           (2600, 818, 1, 0.22, -1), (2725, 824, 2, 0.22, 1), (2850, 836, 0, 0.21, -1)):
        town += PR.house(x, y, sc, v, f)
    town += PR.palm_tree(2300, 840, 0.3, lean=-0.25) + PR.palm_tree(2790, 840, 0.28, lean=0.2)
    town += S.g(olive(3080, 760, 0.62, seed=2) + olive(1990, 742, 0.5, seed=5), filter="wobble-fine")
    # aerial haze pushes the town back
    body = f'<g filter="url(#s3hazef)">{town}</g>'
    # shore rocks where the hill meets the harbour
    rocks = ""
    for i, (x, y, rx, ry) in enumerate(((1742, 848, 44, 24), (1800, 830, 50, 28), (1862, 840, 38, 22),
                                         (1690, 866, 34, 18))):
        rocks += S.path(S.blob(x, y, rx, ry, 0.15, 8, seed=i), fill=S.mix(P["stone"], P["stone_dark"], 0.3), sw=3)
    body += S.g(rocks, filter="wobble")
    return doc(body, defs)


HW_TOP = 775        # top of the harbour sea wall (its face shows above the harbour water at ~824)


def harbour_back_svg():
    """Harbour sea wall along the back of the basin (behind the water), mooring rings, a moored fishing boat.

    Static and drawn before the harbour water, so the water laps at the wall foot and the boat's hull."""
    out = ""

    def qtop(x):
        return float(HW_TOP)

    out += S.g(stone_wall(1872, 2345, qtop, 110, 3, uid="quay", merlons=False), filter="wobble-fine")
    # coping stones along the top and a squat end pier where the wall meets the hill
    out += S.g(f'<rect x="1866" y="{HW_TOP - 9}" width="482" height="13" rx="4" fill="{P["stone"]}" '
               f'stroke="{P["ink"]}" stroke-width="2.8"/>'
               f'<path d="M1852,{HW_TOP + 70} L1852,{HW_TOP - 18} Q1872,{HW_TOP - 30} 1892,{HW_TOP - 18} '
               f'L1892,{HW_TOP + 70} Z" fill="{S.mix(P["stone_light"], P["stone"], 0.5)}" stroke="{P["ink"]}" '
               f'stroke-width="3"/>'
               f'<rect x="1878" y="{HW_TOP - 24}" width="12" height="90" fill="{P["stone_dark"]}" opacity="0.3"/>',
               filter="wobble-fine")
    # mooring rings and their iron plates, above the water line
    rings = ""
    for x in (1960, 2120, 2250):
        rings += (f'<rect x="{x - 6}" y="{HW_TOP + 14}" width="12" height="9" rx="2" fill="{P["wood_dark"]}"/>'
                  f'<circle cx="{x}" cy="{HW_TOP + 29}" r="8" fill="none" stroke="{P["ink"]}" stroke-width="2.8"/>')
    out += S.g(rings, filter="wobble-fine")
    # small fishing boat moored at the wall: its lower hull sits below the water line (the water covers it)
    by = 818      # gunwale
    out += S.g(f'<path d="M1985,{by} Q2040,{by + 40} 2110,{by} L2104,{by - 12} L1992,{by - 12} Z" '
               f'fill="{P["wood_light"]}" stroke="{P["ink"]}" stroke-width="3"/>'
               f'<path d="M1992,{by - 12} L2104,{by - 12}" stroke="{P["jonah_sash"]}" stroke-width="4"/>'
               f'<path d="M2048,{by - 12} L2048,{by - 70}" stroke="{P["wood_dark"]}" stroke-width="3.5"/>'
               f'<path d="M2048,{by - 66} L2080,{by - 24} L2048,{by - 24} Z" fill="{P["sail"]}" '
               f'stroke="{P["ink"]}" stroke-width="2.4"/>'
               f'<path d="M1990,{by - 8} Q1975,{by - 2} 1966,{HW_TOP + 36}" stroke="{P["sackcloth_dark"]}" '
               f'stroke-width="2.6" fill="none"/>', filter="wobble-fine")
    return doc(out)


def harbour_corner_svg():
    """Stone corner block where the harbour wall turns to meet the quay, with steps down to the water.

    Drawn in front of the harbour water so the end of the water band is always hidden behind it."""
    x0, x1, top = 2228, 2345, 784

    def ctop(x):
        return float(top)

    out = S.g(stone_wall(x0, x1, ctop, 112, 13, uid="corner", merlons=False), filter="wobble-fine")
    # steps down into the water on the harbour side
    steps = ""
    for i, (sx, sy) in enumerate(((x0 - 18, top + 14), (x0 - 34, top + 28), (x0 - 48, top + 42))):
        steps += (f'<rect x="{sx}" y="{sy}" width="{x0 - sx + 4}" height="{896 - sy}" '
                  f'fill="{S.mix(P["stone_light"], P["stone"], 0.25 + 0.2 * i)}" stroke="{P["ink"]}" '
                  f'stroke-width="2.6"/>')
    out += S.g(steps, filter="wobble-fine")
    out += S.g(f'<rect x="{x0 - 6}" y="{top - 8}" width="{x1 - x0 + 12}" height="12" rx="4" fill="{P["stone"]}" '
               f'stroke="{P["ink"]}" stroke-width="2.8"/>'
               # a wooden bollard on the corner
               f'<rect x="2300" y="{top - 46}" width="24" height="42" rx="8" fill="{P["wood_dark"]}" '
               f'stroke="{P["ink"]}" stroke-width="3"/>'
               f'<ellipse cx="2312" cy="{top - 46}" rx="14" ry="6" fill="{P["wood"]}" stroke="{P["ink"]}" '
               f'stroke-width="2.8"/>', filter="wobble-fine")
    # water lapping at the foot of the steps
    out += S.g(f'<path d="M{x0 - 62},830 q12,-6 24,0 t24,0 t20,0" stroke="{P["foam"]}" stroke-width="5" '
               f'fill="none" stroke-linecap="round" opacity="0.9"/>', filter="wobble-fine")
    return doc(out)


def sea_band_svg(y, amp, wl, phase, c_top, c_bot, foam_y, seed, foam_x=(), foam_op=0.75, x1=SEA_RIGHT, sw=3.0,
                 line=0.55, ticks=26):
    gid = f"s3sea{seed}"
    defs = ugrad(gid, 0, y - amp, 0, min(SH, y + 260), [(0, c_top), (1, c_bot)])
    edge = S.mix(P["ink"], c_top, 1 - line)
    body = (f'<path d="{S.wave_band(y, amp, wl, phase, x0=-140, x1=x1, bottom=SH + 60)}" fill="url(#{gid})" '
            f'stroke="{edge}" stroke-width="{sw}" stroke-linejoin="round"/>')
    for fx0, fx1, dy in foam_x:
        body += S.path(S.wave_line(y + foam_y + dy, amp * 0.8, wl, phase, x0=fx0, x1=fx1), stroke=False,
                       extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="{foam_op}"')
    rng = random.Random(seed)
    for i in range(ticks):
        tx = rng.uniform(-40, x1 - 60)
        ty = y + rng.uniform(26, 210)
        w = rng.uniform(22, 46)
        body += (f'<path d="M{f1(tx)},{f1(ty)} q{f1(w / 2)},{f1(-w * 0.32)} {f1(w)},0" stroke="{P["foam"]}" '
                 f'stroke-width="3.2" fill="none" stroke-linecap="round" opacity="{rng.uniform(0.45, 0.8):.2f}"/>')
    return doc(S.g(body, filter="wobble"), defs)


def glints_svg(x0, x1, y0, y1, n, seed):
    """Sun glints on the water: small flat cream dashes, a few tiny four-point stars."""
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        k = 0.75 + 0.5 * (y - y0) / max(1.0, y1 - y0)
        w = rng.uniform(10, 24) * k
        out += (f'<path d="M{f1(x - w / 2)},{f1(y)} l{f1(w)},0" stroke="#fffbea" stroke-width="{2.4 * k:.1f}" '
                f'stroke-linecap="round" opacity="{rng.uniform(0.65, 0.95):.2f}"/>')
        if rng.random() < 0.2:
            s = rng.uniform(4, 6) * k
            out += (f'<path d="M{f1(x)},{f1(y - s)} L{f1(x)},{f1(y + s)} M{f1(x - s * 0.8)},{f1(y)} '
                    f'L{f1(x + s * 0.8)},{f1(y)}" stroke="#fffbea" stroke-width="1.6" stroke-linecap="round" '
                    f'opacity="0.85"/>')
    return doc(out)


def _grass_strokes(x0, x1, y0, y1, n, seed, col, op=0.55):
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        h = rng.uniform(10, 22) * (0.7 + 0.6 * (y - y0) / max(1, y1 - y0))
        out += (f'<path d="M{f1(x)},{f1(y)} q{f1(rng.uniform(-3, 3))},{f1(-h / 2)} {f1(rng.uniform(-6, 6))},{f1(-h)}" '
                f'stroke="{col}" stroke-width="2.6" fill="none" stroke-linecap="round" opacity="{op}"/>')
    return out


def _flowers(x0, x1, y0, y1, n, seed):
    rng = random.Random(seed)
    cols = ("#f3d36b", "#f0a0a8", "#fffaf0", "#e37a5a", "#c9a7e0")
    out = ""
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        r = rng.uniform(4, 7) * (0.8 + 0.5 * (y - y0) / max(1, y1 - y0))
        c = rng.choice(cols)
        out += (f'<path d="M{f1(x)},{f1(y + r * 2.2)} L{f1(x)},{f1(y)}" stroke="{P["leaf_dark"]}" stroke-width="2"/>'
                f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{c}" stroke="{P["ink"]}" stroke-width="1.8"/>'
                f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.35)}" fill="{P["sun_hot"]}"/>')
    return out


def land_svg():
    """Quay, road, crossroads with the signpost, grassy verge, pier with cargo."""
    defs = (ugrad("s3ground", 0, 840, 0, 1188, [(0, S.mix(P["grass"], P["leaf_light"], 0.3)), (0.35, P["grass"]),
                                                  (1, S.mix(P["grass"], P["grass_dark"], 0.6))]) +
            ugrad("s3road", 0, 878, 0, 950, [(0, P["sand_light"]), (1, S.mix(P["sand"], P["sand_light"], 0.4))]))
    out = ""
    # ground mass right of the quay
    gpts = [(QUAY_X - 10, 892), (2400, 868), (2700, 858), (3000, 860), (3300, 854), (3600, 850), (3960, 852)]
    gd = S.smooth_path(gpts, closed=False) + f" L3960,{SH + 40} L{QUAY_X - 10},{SH + 40} Z"
    out += S.g(S.path(gd, fill="url(#s3ground)", sw=3.5), filter="wobble")
    out += _grass_strokes(2420, 3900, 858, 880, 90, 5, P["grass_dark"], 0.5)
    # the coastal road
    rd = (f"M{QUAY_X - 10},884 C2600,878 3000,882 3500,880 C3700,880 3820,882 3960,880 "
          f"L3960,948 C3500,952 3000,950 2500,948 L{QUAY_X - 10},946 Z")
    out += S.g(S.path(rd, fill="url(#s3road)", sw=3), filter="wobble")
    rng = random.Random(21)
    for i in range(90):
        x = rng.uniform(QUAY_X + 20, 3900)
        y = rng.uniform(890, 942)
        r = rng.uniform(2, 5)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.6)}" ry="{f1(r)}" fill="{P["sand_dark"]}" '
                f'opacity="0.5"/>')
    out += (f'<path d="M{QUAY_X + 420},934 C2900,929 3300,935 3900,931" stroke="{P["sand_dark"]}" '
            f'stroke-width="2.4" fill="none" opacity="0.4"/>')
    # stone paving on the quay
    out += (f'<path d="M{QUAY_X - 10},884 L{QUAY_X + 380},879 L{QUAY_X + 392},947 L{QUAY_X - 10},946 Z" '
            f'fill="{P["stone_light"]}" stroke="{P["ink"]}" stroke-width="3"/>')
    for i in range(9):
        x = QUAY_X + 20 + i * 44
        out += f'<path d="M{x},884 L{x - 6},946" stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.6"/>'
    out += (f'<path d="M{QUAY_X - 6},915 L{QUAY_X + 386},913" stroke="{P["stone_dark"]}" stroke-width="2" '
            f'opacity="0.5"/>')

    # quay wall face (down into the water) then a grassy bank in front of the road
    def ftop(x):
        return 946.0

    out += S.g(stone_wall(QUAY_X - 10, QUAY_X + 300, ftop, 260, 9, uid="front", merlons=False),
               filter="wobble-fine")
    bank = (f"M{QUAY_X + 290},946 C{QUAY_X + 330},990 {QUAY_X + 340},1060 {QUAY_X + 330},{SH + 40} "
            f"L3960,{SH + 40} L3960,946 Z")
    out += S.g(S.path(bank, fill="url(#s3ground)", sw=3), filter="wobble")
    # a low dry-stone wall along the front edge of the road
    stones = ""
    rng = random.Random(33)
    x = QUAY_X + 420
    while x < 3960:
        w = rng.uniform(34, 56)
        h = rng.uniform(20, 28)
        stones += S.path(S.blob(x + w / 2, 960, w / 2, h / 2, 0.12, 7, seed=int(x)),
                         fill=S.mix(P["stone"], P["stone_light"], rng.uniform(0, 0.6)), sw=2.6)
        x += w + rng.uniform(-6, 2)
    out += S.g(stones, filter="wobble-fine")
    out += _grass_strokes(QUAY_X + 360, 3900, 990, 1180, 260, 7, P["grass_dark"], 0.5)
    out += _grass_strokes(QUAY_X + 360, 3900, 980, 1150, 90, 8, S.mix(P["leaf_light"], "#fffaf0", 0.2), 0.6)
    out += _flowers(QUAY_X + 400, 3900, 1000, 1170, 70, 9)
    # trees and bushes at the crossroads (the olive without its dark olives: they read as faces)
    out += no_olive_dots(PR.olive_tree(2870, 872, 0.62, seed=4))
    out += PR.bush(3080, 874, 0.55, 1) + PR.bush(3800, 870, 0.55, 0) + PR.bush(2560, 874, 0.5, 3)
    out += PR.signpost(SIGN_X, SIGN_Y, 1.0)
    for x, v in ((2700, 0), (2990, 2), (3260, 0), (3430, 2), (3700, 0), (3900, 1)):
        out += PR.grass_tuft(x, 880, 0.6, v)
    # the pier (in front of the docked ship)
    out += PR.harbor_dock(PIER_X0, PIER_X1, GY, depth=230, scale=K)
    # cargo waiting on the quay: crates, jars, sacks
    out += (PR.crate(2390, BACK_Y - 44, 0.62) + PR.crate(2445, BACK_Y - 44, 0.62) + PR.crate(2417, BACK_Y - 108, 0.58)
            + PR.jar(2238, BACK_Y - 52, 0.55) + PR.jar(2272, BACK_Y - 46, 0.48, rot=8)
            + PR.sack(2505, BACK_Y - 2, 0.55, seed=2) + PR.sack(2548, BACK_Y, 0.48, seed=5))
    out += PR.rope_coil(1520, BACK_Y + 8, 0.6)
    # quay bollard with a resting gull
    out += (f'<g filter="url(#wobble-fine)"><rect x="2606" y="842" width="30" height="52" rx="10" '
            f'fill="{P["wood_dark"]}" stroke="{P["ink"]}" stroke-width="3.2"/>'
            f'<ellipse cx="2621" cy="844" rx="17" ry="7" fill="{P["wood"]}" stroke="{P["ink"]}" stroke-width="3"/></g>')
    out += PR.gull(2622, 805, 0.55, -1, pose="stand")
    return doc(out, defs)


def foreground_svg():
    out = ""
    # rocks and reeds at the quay corner (hide where the water meets the quay)
    out += S.g(S.path(S.blob(QUAY_X + 20, 1150, 130, 74, 0.12, 9, seed=8),
                      fill=S.mix(P["stone"], P["stone_dark"], 0.35), sw=4) +
               S.path(S.blob(QUAY_X + 150, 1176, 110, 56, 0.12, 9, seed=9), fill=P["stone"], sw=4), filter="wobble")
    out += PR.reeds(QUAY_X - 60, 1140, 0.7, 0) + PR.reeds(QUAY_X + 230, 1192, 0.6, 1)
    for x, v, sc in ((2760, 2, 1.0), (2960, 0, 1.1), (3150, 2, 0.9), (3330, 0, 1.0), (3520, 2, 1.1), (3700, 0, 1.0),
                     (3880, 2, 0.95)):
        out += PR.grass_tuft(x, 1192, sc, v)
    out += S.g(S.path(S.blob(3020, 1180, 120, 56, 0.15, 9, seed=3), fill=S.mix(P["stone"], P["sand"], 0.3), sw=4),
               filter="wobble")
    out += PR.bush(3880, 1196, 0.9, 3)
    return doc(out)


# ============================================================================ ship group


def ship_svg(part, sail):
    return doc(PR.ship(SHIP_X, SHIP_WL, K, -1, sail=sail, part=part, lantern=True))


# The sail band: everything of ship(part='back') above the rail between the stern and bow posts. Only the
# sail and its sheets differ between sail='furled' and sail='full' there; the clip cuts only thin stays and
# (behind a rail shield) the mast foot, so the band redrawn over the furled ship lines up exactly.
SAIL_CLIP_LOCAL = [(-405, -1000), (425, -1000), (425, -232), (342, -232), (342, -200), (-342, -200),
                   (-342, -232), (-405, -232)]
SAIL_TOP_L, SAIL_FOOT_L, SAIL_BELLY_L = -842, -548, -474   # local y: yard line, foot corners, foot middle


def sail_band_svg():
    pts = " ".join(f"{f1(SHIP_X - x * K)},{f1(SHIP_WL + y * K)}" for x, y in SAIL_CLIP_LOCAL)
    clip = f'<clipPath id="s3sailband"><polygon points="{pts}"/></clipPath>'
    return doc(f'<g clip-path="url(#s3sailband)">{PR.ship(SHIP_X, SHIP_WL, K, -1, sail="full", part="back")}</g>',
               clip)


def sail_width(v):
    """Width / centre (local) of the full sail at height v (0 yard .. 1 foot corners); see props._sail_pt."""
    sv = math.sin(math.pi * max(0.0, min(1.0, v)))
    xl = -300 - 46 * sv ** 0.9
    xr = 280 + 74 * sv ** 0.8
    return xr - xl, (xl + xr) / 2


ROLL_W, ROLL_R = 600, 17
ROLL_CY = SAIL_TOP_L + 11       # local y of the roll centre when the edge is at the yard


def sail_roll_svg():
    """The sail bundle unrolling at the lower edge of the dropping sail (local ship coords, mirrored)."""
    cx, cy, hw, r = -10, ROLL_CY, ROLL_W / 2, ROLL_R
    shape = f"M{cx - hw + r},{cy - r} L{cx + hw - r},{cy - r} A{r},{r} 0 0 1 {cx + hw - r},{cy + r} " \
            f"L{cx - hw + r},{cy + r} A{r},{r} 0 0 1 {cx - hw + r},{cy - r} Z"
    inner = ""
    for u0, u1 in ((1 / 7, 2 / 7), (3 / 7, 4 / 7), (5 / 7, 6 / 7)):
        a, b = cx - hw + ROLL_W * u0, cx - hw + ROLL_W * u1
        inner += f'<rect x="{f1(a)}" y="{cy - r - 2}" width="{f1(b - a)}" height="{2 * r + 4}" fill="{P["sail_stripe"]}"/>'
    inner += (f'<rect x="{cx - hw}" y="{cy + r * 0.25}" width="{ROLL_W}" height="{r}" '
              f'fill="{S.shade(P["sail"], -0.35)}" opacity="0.45"/>'
              f'<rect x="{cx - hw}" y="{cy - r * 0.7}" width="{ROLL_W}" height="{r * 0.45}" fill="#fffaf0" '
              f'opacity="0.35"/>')
    for i in range(1, 9):
        x = cx - hw + ROLL_W * i / 9
        inner += (f'<path d="M{f1(x - 8)},{cy - r + 2} Q{f1(x + 2)},{cy} {f1(x - 6)},{cy + r - 2}" '
                  f'stroke="{S.shade(P["sail"], -0.4)}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    body = (f'<path d="{shape}" fill="{P["sail"]}"/>'
            f'<clipPath id="s3rollc"><path d="{shape}"/></clipPath><g clip-path="url(#s3rollc)">{inner}</g>'
            f'<path d="{shape}" fill="none" stroke="{P["ink"]}" stroke-width="4.5" stroke-linejoin="round"/>')
    for ex in (cx - hw + r * 0.7, cx + hw - r * 0.7):
        body += (f'<ellipse cx="{f1(ex)}" cy="{cy}" rx="7" ry="{r - 3}" fill="{S.shade(P["sail"], -0.15)}" '
                 f'stroke="{P["ink"]}" stroke-width="3"/>'
                 f'<path d="M{f1(ex)},{cy - 6} q4,4 0,8" stroke="{P["ink"]}" stroke-width="2.2" fill="none"/>')
    return doc(ship_place(body))


def halyard_svg(hauling, hands):
    """Halyard down the mast; while hauling it runs from the mast to the deck sailor's fists."""
    mx = SHIP_X + 10 * K + 3          # just in front of the mast centre line
    top = SHIP_WL - 846 * K
    rope = P["sackcloth_dark"]
    if not hauling:
        d = f"M{f1(mx)},{f1(top)} L{f1(mx + 1)},{f1(RAIL - 18)}"
    else:
        (fx, fy), (nx, ny) = hands     # far fist (next to the mast), near fist
        d = (f"M{f1(mx)},{f1(top)} L{f1(mx + 1)},{f1(fy - 5)} L{f1(fx)},{f1(fy)} L{f1(nx)},{f1(ny)} "
             f"Q{f1(nx - 22)},{f1(ny + 8)} {f1(nx - 26)},{f1(ny + 46)}")
    body = (f'<path d="{d}" stroke="{P["ink"]}" stroke-width="5.6" fill="none" stroke-linejoin="round" '
            f'stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{rope}" stroke-width="2.8" fill="none" stroke-linejoin="round" '
            f'stroke-linecap="round"/>')
    if not hauling:
        body += (f'<rect x="{f1(mx - 9)}" y="{f1(RAIL - 24)}" width="20" height="7" rx="3" fill="{P["wood_dark"]}" '
                 f'stroke="{P["ink"]}" stroke-width="2"/>')
    return doc(S.g(body, filter="wobble-fine"))


def hull_cover_svg():
    """The ship's hull from just under the rail down — redrawn over the deck crew so legs never show."""
    y0 = SHIP_WL - 175 * K
    clip = f'<clipPath id="s3hullclip"><rect x="0" y="{f1(y0)}" width="{SW}" height="{SH}"/></clipPath>'
    return doc(f'<g clip-path="url(#s3hullclip)">{PR.ship(SHIP_X, SHIP_WL, K, -1, sail="furled", part="back")}</g>',
               clip)


def deck_cargo_svg():
    """Cargo stacked on deck, tall enough to show above the rail: jars at the bow, crates at the stern."""
    out = ""

    def deck_y(lx):
        return SHIP_WL + (-165 - 75 * (abs(lx) / 480) ** 3.2) * K

    # two amphorae at the bow (partly behind the captain)
    for lx, sc, rot in ((300, 0.5, -4), (336, 0.46, 6)):
        x = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, lx, 0)[0]
        out += PR.jar(x, deck_y(lx) - 80 * sc, sc, rot=rot)
    # a stack of crates and a sack at the stern (Jonah hides beside them)
    x = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, -272, 0)[0]
    y = deck_y(-272)
    out += PR.crate(x, y - 49 * 0.6, 0.6) + PR.crate(x + 4, y - 49 * 0.6 - 64, 0.55, rot=-5)
    xs = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, -335, 0)[0]
    out += PR.sack(xs, deck_y(-335) + 2, 0.5, seed=3)
    return doc(out)


def hull_shadow_svg():
    """Soft darker-teal shadow / reflection of the hull on the water just below the waterline."""
    c = S.mix(P["sea"], P["sea_deep"], 0.55)
    return doc(f'<ellipse cx="{SHIP_X - 20}" cy="{SHIP_WL + 16}" rx="{390 * K}" ry="17" fill="{c}" opacity="0.38" '
               f'filter="url(#soft)"/>'
               f'<ellipse cx="{SHIP_X - 40}" cy="{SHIP_WL + 8}" rx="{300 * K}" ry="8" fill="{c}" opacity="0.3" '
               f'filter="url(#soft)"/>')


BOW_X = SHIP_X - 425 * K       # bow at the waterline (stage, docked)
STERN_X = SHIP_X + 470 * K


def wake_svg():
    """Bow wave (a bold foam 'V'), foam along the waterline and a short wake at the stern (moves with the ship)."""
    y = 951
    bow, stern = BOW_X, STERN_X
    fo = P["foam"]
    out = (  # the bow wave: a curling crest and two diverging foam strokes
        f'<path d="M{f1(bow - 34)},{f1(y + 6)} q22,-30 58,-22 q24,6 38,-6" stroke="{fo}" stroke-width="8" '
        f'fill="none" stroke-linecap="round" opacity="0.95"/>'
        f'<path d="M{f1(bow - 26)},{f1(y + 10)} Q{f1(bow + 60)},{f1(y + 26)} {f1(bow + 170)},{f1(y + 40)}" '
        f'stroke="{fo}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.9"/>'
        f'<path d="M{f1(bow - 12)},{f1(y + 2)} Q{f1(bow + 80)},{f1(y + 6)} {f1(bow + 190)},{f1(y + 2)}" '
        f'stroke="{fo}" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.9"/>'
        f'<path d="M{f1(bow - 52)},{f1(y + 24)} q46,-10 100,0" stroke="{fo}" stroke-width="5" fill="none" '
        f'stroke-linecap="round" opacity="0.75"/>'
        # foam along the waterline
        f'<path d="M{f1(bow + 200)},{f1(y + 3)} C{f1(bow + 330)},{f1(y + 9)} {f1(stern - 250)},{f1(y + 9)} '
        f'{f1(stern - 60)},{f1(y + 3)}" stroke="{fo}" stroke-width="5" fill="none" stroke-linecap="round" '
        f'opacity="0.7"/>')
    for i in range(5):
        x = stern - 60 + i * 70
        yy = y + 4 + i * 7
        out += (f'<path d="M{f1(x)},{f1(yy)} q{34 + i * 8},-10 {70 + i * 14},0" stroke="{fo}" '
                f'stroke-width="{7 - i * 1.0:.1f}" fill="none" stroke-linecap="round" opacity="{0.9 - i * 0.14:.2f}"/>'
                f'<path d="M{f1(x + 20)},{f1(yy + 16 + i * 3)} q{30 + i * 6},-8 {60 + i * 12},0" stroke="{fo}" '
                f'stroke-width="{4.5 - i * 0.6:.1f}" fill="none" stroke-linecap="round" '
                f'opacity="{0.7 - i * 0.1:.2f}"/>')
    return doc(S.g(out, filter="wobble-fine"))


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.line(0), ctx.line(1), ctx.line(2)

    # ---------------------------------------------------------------- key times (from the narration)
    T_REFUSE = L0.start + 0.35                       # palm out, head shake
    T_TURN = L0.end - 0.22                           # spin round (whoosh)
    T_RUN = T_TURN + 0.2                             # running
    T_LEAP = L1.start + 0.73 * (L1.end - L1.start)   # leaps from the pier ("坐上一条...船")
    T_LAND = T_LEAP + 0.42
    T_SWAP = T_LEAP + 0.56 * (T_LAND - T_LEAP)       # over the rail: front layer -> deck layer
    T_SAIL = L1.end - 0.25                           # deck sailor hauls, the sail unrolls
    T_SAIL_END = T_SAIL + 0.5                        # sail fully down
    T_SAIL_DONE = T_SAIL + 0.64                      # band layer handed back to ship_back ('full')
    T_POINT = T_SAIL + 0.3                           # captain points west (on the cloth sound)
    T_DEPART = L1.end - 0.05                         # ship leaves the pier
    T_LOOK = L2.start - 0.15                         # Jonah looks back at the shore
    T_DUCK = L2.start + 0.22                         # ... and ducks behind the rail ("躲开")
    # the jar hand-off while the camera arrives at the harbour
    T_SWING = L1.start + 1.45                        # P2 swings the jar up
    T_THROWF = T_SWING + 0.07                        # P2: carry -> throw frame
    T_REL = T_SWING + 0.16                           # jar leaves his hands
    T_CATCH = T_REL + 0.5                            # deck sailor catches it
    T_STOW = T_LEAP - 0.2                            # ... and lowers it behind the rail
    T_CRATE = T_DEPART + 0.15                        # P1 sets his crate down on the pier
    T_P2POINT = L2.start + 0.55                      # P2 points after the ship

    # ---------------------------------------------------------------- Jonah's path
    v_run = (JX0 - LEAP_X) / (T_LEAP - T_RUN - 0.15)

    def jpos(t):
        if t < T_RUN:
            return JX0, GY
        if t < T_LEAP:
            tau = t - T_RUN
            d = v_run * tau * tau / 0.6 if tau < 0.3 else v_run * (tau - 0.15)
            return JX0 - d, GY
        u = min(1.0, (t - T_LEAP) / (T_LAND - T_LEAP))
        x = LEAP_X + (BOARD_X - LEAP_X) * (1 - (1 - u) ** 1.6)
        y = GY + (DECK - GY) * u - 4 * 150 * u * (1 - u)
        return x, y

    def t_pass(x):
        """First time Jonah's x reaches x (he runs right -> left)."""
        tt = T_RUN
        while tt < T_LEAP and jpos(tt)[0] > x:
            tt += 0.01
        return tt

    # ---------------------------------------------------------------- ship motion (shared by the ship group)
    DIST = 760
    t_sail_end = T_DEPART + 3.4

    def ship_u(t):
        return M.progress(t, T_DEPART, t_sail_end, "sine")

    def ship_tf(t):
        u = ship_u(t)
        s = 1 - 0.1 * u                                  # shrinks as it heads out toward the horizon
        dy = 3.0 * math.sin(2 * math.pi * t / 3.1) + 1.5 * math.sin(2 * math.pi * t / 1.7 + 1) - 8 * u
        rot = (0.45 + 0.5 * u) * math.sin(2 * math.pi * (t / 3.6 + 0.2))
        return Tf(dx=-DIST * u, dy=dy, rot=rot, sx=s, sy=s, px=SHIP_X, py=SHIP_WL)

    # ---------------------------------------------------------------- camera (precomputed, smoothed, monotonic pans)
    X_HOLD, Y0 = 3090, 640
    X_DOCK = 1540            # where the follow target arrives as Jonah takes off: no overshoot, no reversal
    X_END = 1250             # settles here (lagging behind the departing ship) before the closing dissolve
    t_cam_end = T - 0.95

    cam_w_f = M.keys([(0, {"dx": 1600}), (T_TURN, {"dx": 1560}), (T_RUN + 1.1, {"dx": 1900}),
                      (T_LEAP, {"dx": 2000}), (T_DEPART, {"dx": 2000}), (L2.end, {"dx": 1800}),
                      (T, {"dx": 1800})], "inout")
    cam_y_f = M.keys([(0, {"dy": Y0}), (T_TURN, {"dy": 648}), (T_RUN + 1.2, {"dy": 610}),
                      (T_LEAP, {"dy": 600}), (T, {"dy": 600})], "inout")

    def cam_x_raw(t):
        w = cam_w_f(t).dx
        hold = min(X_HOLD, PAINT_R - 8 - w / 2)
        jx = jpos(min(t, T_LAND))[0]
        x = max(min(hold, jx - 0.12 * w), X_DOCK)
        return x - (X_DOCK - X_END) * M.progress(t, T_DEPART, t_cam_end, "inout")

    DT = 1 / 120
    ts = np.arange(-1.0, T + 1.0, DT)
    raw = np.array([cam_x_raw(min(max(t, 0.0), T)) for t in ts])
    sig = 0.13
    kk = np.arange(-int(3 * sig / DT), int(3 * sig / DT) + 1) * DT
    ker = np.exp(-0.5 * (kk / sig) ** 2)
    ker /= ker.sum()
    xs = np.convolve(np.pad(raw, len(kk) // 2, mode="edge"), ker, mode="valid")
    ws = np.array([cam_w_f(min(max(t, 0.0), T)).dx for t in ts])
    ys = np.array([cam_y_f(min(max(t, 0.0), T)).dy for t in ts])
    hs = ws * 9 / 16
    xs = np.clip(xs, ws / 2 + 4, PAINT_R - ws / 2 - 4)
    ys = np.clip(ys, hs / 2 + 4, SH - hs / 2 - 4)

    def cam(t):
        return Cam(float(np.interp(t, ts, xs)), float(np.interp(t, ts, ys)), float(np.interp(t, ts, ws)))

    sc.camera = cam
    CX0 = cam(0).x

    def parallax(k, vx=0.0):
        return lambda t: Tf(dx=k * (cam(t).x - CX0) + vx * t)

    # ---------------------------------------------------------------- sky / far / town
    sc.add("sky", sky_svg(), wc=0.5)
    sc.add("sun", sun_svg(), motion=parallax(0.85), wc=0.4)
    sc.add("clouds", clouds_svg(), motion=parallax(0.55, 9.0), wc=0.6)
    sc.add("far", far_svg(), motion=parallax(0.25), wc=0.8)
    sc.add("town", town_svg(), motion=parallax(0.1))
    sc.add("harbour_back", harbour_back_svg())

    # harbour water behind the ship
    sea_mid_m = M.combine(M.bob(3, 3.4), M.bob(14, 5.2, axis="x"))
    sc.add("sea_mid", sea_band_svg(824, 5, 280, 0.4, S.mix(P["sea_light"], P["sea_pale"], 0.3), P["sea_light"], 8, 31,
                                   foam_x=((-100, 700, 0), (1100, 1800, 6)), foam_op=0.6), motion=sea_mid_m)

    def twinkle(rate, phase):
        def f(t):
            v = (t * rate + phase) % 6.0
            return v if v <= 3.0 else 6.0 - v        # ping-pong 0..3 -> smooth crossfades
        return f

    sc.add("glints_mid", [glints_svg(-100, SEA_RIGHT - 40, 838, 940, 34, 100 + i) for i in range(4)],
           motion=sea_mid_m, frame_at=twinkle(2.2, 0.0), wc=0.25)
    sc.add("harbour_corner", harbour_corner_svg())

    # ---------------------------------------------------------------- ship group
    sc.add("ship_back", [ship_svg("back", "furled"), ship_svg("back", "full")], motion=ship_tf,
           frame_at=lambda t: 1.0 if t >= T_SAIL_DONE else 0.0, seed=SHIP_SEED)

    # deck sailor: catches the jar (carry), then hauls the halyard (pull) as the sail drops
    d1 = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, DECK_SAILOR_LX, PR.SHIP_DECK_Y)
    catch_hands = mid(C.hand_positions(C.sailor, *d1, K, 1, variant=0, pose="carry"))
    pull_hands = C.hand_positions(C.sailor, *d1, K, 1, variant=0, pose="pull")

    sc.add("halyard", [halyard_svg(False, pull_hands), halyard_svg(True, pull_hands)], motion=ship_tf,
           frame_at=lambda t: 1.0 if t >= T_SAIL else 0.0, wc=0.4)

    # the sail unrolls down from the yard: the full-sail band is revealed top-down over the furled ship,
    # led by a rolled bundle; once it is down ship_back switches to its 'full' frame (identical pixels)
    BB_TOP = SHIP_WL - 948 * K           # top of the band layer's content (pennant / masthead)
    BB_BOT = SHIP_WL - 200 * K

    def sail_edge_l(t):
        """Local y of the unrolling edge."""
        if t < T_SAIL_END:
            return M.lerp(SAIL_TOP_L, SAIL_BELLY_L, M.progress(t, T_SAIL, T_SAIL_END, "out"))
        return M.lerp(SAIL_BELLY_L, -200, M.progress(t, T_SAIL_END, T_SAIL_DONE - 0.02, "linear"))

    def sail_reveal(t):
        ey = SHIP_WL + sail_edge_l(t) * K
        return {"mode": "down", "frac": min(1.0, max(0.0, (ey - BB_TOP) / (BB_BOT - BB_TOP))), "soft": 10}

    def sail_tf(t):
        b = ship_tf(t)
        a = 1.0 if T_SAIL <= t < T_SAIL_DONE else 0.0
        return Tf(b.dx, b.dy, b.rot, b.sx, b.sy, a, b.px, b.py)

    sc.add("sail", sail_band_svg(), motion=sail_tf, reveal=sail_reveal, seed=SHIP_SEED)

    ROLL_PIV = (SHIP_X + 10 * K, SHIP_WL + ROLL_CY * K)

    def roll_tf(t):
        if not (T_SAIL <= t < T_SAIL_DONE):
            return Tf(alpha=0.0)
        e = sail_edge_l(t)
        v = (e - SAIL_TOP_L) / (SAIL_FOOT_L - SAIL_TOP_L)
        wv, _ = sail_width(v)
        a = (1 - M.progress(e, SAIL_FOOT_L - 14, SAIL_BELLY_L + 10, "linear")) * M.progress(t, T_SAIL, T_SAIL + 0.04)
        return compose(ship_tf(t), ROLL_PIV, dy=(e - SAIL_TOP_L) * K, sx=(wv + 16) / (ROLL_W - 4), alpha=a)

    sc.add("sail_roll", sail_roll_svg(), motion=roll_tf, wc=0.6)
    sc.add("deck_cargo", deck_cargo_svg(), motion=ship_tf)

    # captain near the bow: points west (with a small lean into the gesture) as the sail drops
    cap_xy = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, CAPTAIN_LX, PR.SHIP_DECK_Y)
    sc.add("captain", [doc(C.captain(*cap_xy, K, -1, pose="stand")), doc(C.captain(*cap_xy, K, -1, pose="point"))],
           motion=lambda t: compose(ship_tf(t), cap_xy,
                                    rot=-3.0 * (1 - M.progress(t, T_POINT, T_POINT + 0.2, "out")) * (t >= T_POINT)),
           frame_at=lambda t: 1.0 if t >= T_POINT else 0.0)

    def deck_dip(t):
        d = 0.0
        if T_CATCH <= t < T_CATCH + 0.25:
            d += 9 * math.sin(math.pi * (t - T_CATCH) / 0.25)            # absorbs the catch
        if T_STOW <= t < T_STOW + 0.34:
            d += 16 * math.sin(math.pi * (t - T_STOW) / 0.34)            # bends to set the jar down
        return d

    def deck_sailor_tf(t):
        sy = 1.0
        if T_SAIL <= t < T_SAIL + 0.16:
            sy = 0.93 + 0.07 * M.progress(t, T_SAIL, T_SAIL + 0.16, "out")   # springs into the haul
        return compose(ship_tf(t), d1, dy=deck_dip(t), sy=sy)

    sc.add("deck_sailor", [doc(C.sailor(*d1, K, 1, variant=0, pose="carry", expr="neutral")),
                           doc(C.sailor(*d1, K, 1, variant=0, pose="pull", expr="neutral"))],
           motion=deck_sailor_tf, frame_at=lambda t: 1.0 if t >= T_SAIL else 0.0)

    # the caught jar in the deck sailor's hands, then lowered behind the rail into the ship
    JAR_S = 0.45
    jd = (catch_hands[0], catch_hands[1] - 22)

    def jar_deck_tf(t):
        if t < T_CATCH or t >= T_STOW + 0.4:
            return Tf(alpha=0.0)
        low = 118 * M.progress(t, T_STOW, T_STOW + 0.34, "inout")
        return compose(ship_tf(t), jd, dy=deck_dip(t) + low)

    sc.add("jar_deck", doc(PR.jar(*jd, JAR_S)), motion=jar_deck_tf)

    # Jonah on deck (appears when he is over the rail)
    def jship_frame(t):
        if t < T_LAND + 0.06:
            return 0.0
        if t < T_LOOK:
            return 1.0
        if t < T_DUCK:
            return 2.0
        return 3.0

    jship = [doc(C.jonah(BOARD_X, DECK, K, -1, pose="run_b", expr="worried")),
             doc(C.jonah(BOARD_X, DECK, K, -1, pose="stand", expr="worried")),
             doc(C.jonah(BOARD_X, DECK, K, 1, pose="stand", expr="worried")),
             doc(C.jonah(BOARD_X, DECK, K, 1, pose="stand", expr="scared"))]

    def jship_tf(t):
        b = ship_tf(t)
        if t < T_SWAP:
            return Tf(alpha=0.0)
        if t < T_LAND:
            x, y = jpos(t)
            ox, oy = x - BOARD_X, y - DECK
        else:
            ox = 0.0
            oy = 5 * math.sin(math.pi * min(1.0, (t - T_LAND) / 0.18))            # landing dip
            oy += 104 * M.progress(t, T_DUCK, T_DUCK + 0.3, "inout")             # duck behind the rail
            oy -= 14 * M.progress(t, T_DUCK + 0.9, T_DUCK + 1.25, "inout")       # ... then peek up a little
            oy += 2.0 * math.sin(2 * math.pi * t * 1.3)
        return compose(b, (BOARD_X, DECK), dx=ox, dy=oy)

    sc.add("jonah_ship", jship, motion=jship_tf, frame_at=jship_frame)
    sc.add("hull_cover", hull_cover_svg(), motion=ship_tf)
    sc.add("ship_front", ship_svg("front", "furled"), motion=ship_tf)
    # water in front of the hull
    sea_front_m = M.combine(M.bob(4, 2.9, 0.3), M.bob(-18, 4.4, axis="x"))
    sc.add("sea_front", sea_band_svg(950, 7, 360, 1.3, P["sea_light"], S.mix(P["sea"], P["sea_deep"], 0.3), 12, 41,
                                     foam_x=((-100, 600, 0), (900, 1500, 4), (1900, 2300, 0))), motion=sea_front_m)
    sc.add("glints_front", [glints_svg(-100, SEA_RIGHT - 120, 962, 1046, 30, 200 + i) for i in range(4)],
           motion=sea_front_m, frame_at=twinkle(2.0, 1.3), wc=0.25)

    def water_tf(alpha_fn):
        return lambda t: (lambda b: Tf(b.dx, b.dy * 0.4, 0, b.sx, b.sy, alpha_fn(t), b.px, b.py))(ship_tf(t))

    sc.add("hull_shadow", hull_shadow_svg(), motion=water_tf(lambda t: 1.0), wc=0.3)
    sc.add("wake", wake_svg(), motion=water_tf(lambda t: M.progress(t, T_DEPART, T_DEPART + 0.8, "sine")))

    # foam dashes shed by the bow: they stay put in the water, so they stream back along the hull
    rngf = random.Random(77)
    FOAM_LIFE = 1.7
    foam = []
    tt = T_DEPART + 0.35
    while tt < T + 0.1:
        foam.append((tt, rngf.uniform(10, 60), rngf.uniform(2, 30), rngf.uniform(26, 58), rngf.uniform(0.7, 1.0)))
        tt += rngf.uniform(0.07, 0.12)

    def bow_x(t):
        b = ship_tf(t)
        return SHIP_X + b.dx - 425 * K * b.sx

    for i, (ts_, ox, oy, ln, op) in enumerate(foam):
        foam[i] = (ts_, bow_x(ts_) + ox, SHIP_WL - 14 + oy, ln, op)

    def foam_fn(t):
        live = [(t - ts_, x, y, ln, op) for ts_, x, y, ln, op in foam if 0 <= t - ts_ <= FOAM_LIFE]
        if not live:
            return None
        x0 = int(min(x for _, x, _, _, _ in live) - 20)
        x1 = int(max(x + ln for _, x, _, ln, _ in live) + 40)
        y0, y1 = SHIP_WL - 24, SHIP_WL + 40
        im = Image.new("RGBA", (max(1, x1 - x0), y1 - y0), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for age, x, y, ln, op in live:
            a = op * min(1.0, age / 0.15) * (1 - age / FOAM_LIFE) ** 1.3
            xx = x - x0 + 14 * age                      # a slow drift with the water
            yy = y - y0 + 3 * age
            w = 5 if age < 0.6 else 4
            d.line([(xx, yy), (xx + ln * (1 - 0.3 * age / FOAM_LIFE), yy)], fill=(244, 248, 241, int(235 * a)),
                   width=w)
        return im, (x0, y0)

    sc.add_dynamic("foam", foam_fn)

    # ---------------------------------------------------------------- land, quay, pier
    sc.add("land", land_svg())
    sc.add("sea_near", sea_band_svg(1054, 9, 440, 2.4, S.mix(P["sea"], P["sea_light"], 0.35), P["sea_deep"], 14, 51,
                                    foam_x=((-100, 800, 0), (1200, 2000, 0)), x1=QUAY_X - 25),
           motion=M.combine(M.bob(5, 2.5, 0.6), M.bob(22, 3.9, axis="x")))

    # ---------------------------------------------------------------- pier sailors (loading)
    p1 = (P1X, PIER_Y)
    p2 = (P2X, PIER_Y)
    sc.add("pier_shadows", doc(C.ground_shadow(p1[0] + 4, p1[1], K, 120, 0.24) +
                               C.ground_shadow(p2[0] - 8, p2[1], K, 130, 0.24)))

    # P1 holds a crate overhead; after the ship leaves he lowers it (lift -> carry) and sets it on the pier
    def p1_bob(t):
        k = 1 - M.progress(t, T_CRATE - 0.35, T_CRATE, "sine")     # the bob settles before he lowers it
        return Tf(dx=-8 * min(t, T_CRATE) / T, dy=-4 * abs(math.sin(math.pi * t * 1.4)) * k,
                  rot=0.8 * math.sin(math.pi * t * 1.4) * k, px=p1[0], py=p1[1])

    CRATE_S = 0.62
    c_lift = mid(C.hand_positions(C.sailor, *p1, K, -1, variant=1, pose="lift"))
    c_carry = mid(C.hand_positions(C.sailor, *p1, K, -1, variant=1, pose="carry"))
    crate_up = (c_lift[0], c_lift[1] - 34)
    crate_hip = (c_carry[0] - 4, c_carry[1] - 6)
    crate_down = (p1[0] - 108, PIER_Y - 49 * CRATE_S + 2)
    tp1 = t_pass(p1[0] + 40)

    def crate_tf(t):
        b = p1_bob(t)
        if t < T_CRATE:
            return b
        if t < T_CRATE + 0.25:
            u = M.progress(t, T_CRATE, T_CRATE + 0.25, "inout")
            x, y = M.lerp(crate_up[0], crate_hip[0], u), M.lerp(crate_up[1], crate_hip[1], u)
        else:
            u = M.progress(t, T_CRATE + 0.25, T_CRATE + 0.47, "in")
            x, y = M.lerp(crate_hip[0], crate_down[0], u), M.lerp(crate_hip[1], crate_down[1], u)
        bx, by = apply_tf(b, x, y, p1)
        return Tf(dx=bx - crate_up[0], dy=by - crate_up[1])

    def p1_frame(t):
        if t >= T_CRATE + 0.42:
            return 3.0
        if t >= T_CRATE + 0.12:
            return 2.0
        return 1.0 if tp1 <= t < tp1 + 1.4 else 0.0

    sc.add("crate1", doc(PR.crate(*crate_up, CRATE_S)), motion=crate_tf)
    sc.add("pier_sailor1", [doc(C.sailor(*p1, K, -1, variant=1, pose="lift")),
                            doc(C.sailor(*p1, K, -1, variant=1, pose="lift", expr="surprised")),
                            doc(C.sailor(*p1, K, -1, variant=1, pose="carry")),
                            doc(C.sailor(*p1, K, -1, variant=1, pose="stand", expr="neutral"))],
           frame_at=p1_frame, motion=p1_bob)

    # P2 swings his jar up to the deck sailor, watches Jonah dash past, then points after the ship
    def p2_bob(t):
        k = 1 - M.progress(t, T_SWING - 0.3, T_SWING, "sine")       # settles as he gets ready to swing
        k2 = M.progress(t, T_REL + 0.4, T_REL + 1.0, "sine")          # breathing again after the throw
        return Tf(dx=-6 * min(t, T_SWING) / T,
                  dy=-3 * abs(math.sin(math.pi * t * 1.7 + 0.6)) * k - 1.5 * math.sin(2 * math.pi * t / 2.3) ** 2 * k2,
                  rot=0.9 * math.sin(math.pi * t * 1.7 + 0.6) * k, px=p2[0], py=p2[1])

    j_carry = mid(C.hand_positions(C.sailor, *p2, K, -1, variant=3, pose="carry"))
    j_carry = (j_carry[0], j_carry[1] - 22)
    j_throw = mid(C.hand_positions(C.sailor, *p2, K, -1, variant=3, pose="throw"))
    j_throw = (j_throw[0] - 4, j_throw[1] - 28)
    tp2 = t_pass(p2[0] + 40)

    def p2_frame(t):
        if t < T_THROWF:
            return 0.0
        if t < T_REL + 0.32:
            return 1.0
        if t >= T_P2POINT:
            return 4.0
        return 3.0 if tp2 <= t < tp2 + 1.4 else 2.0

    sc.add("pier_sailor2", [doc(C.sailor(*p2, K, -1, variant=3, pose="carry", expr="neutral")),
                            doc(C.sailor(*p2, K, -1, variant=3, pose="throw", expr="happy")),
                            doc(C.sailor(*p2, K, -1, variant=3, pose="stand", expr="neutral")),
                            doc(C.sailor(*p2, K, -1, variant=3, pose="stand", expr="surprised")),
                            doc(C.sailor(*p2, K, -1, variant=3, pose="point", expr="neutral"))],
           frame_at=p2_frame, motion=p2_bob)

    catch_at = apply_tf(compose(ship_tf(T_CATCH), jd), *jd, jd)

    def jar_pier_tf(t):
        if t >= T_CATCH:
            return Tf(alpha=0.0)
        if t < T_SWING:
            b = p2_bob(t)
            x, y = apply_tf(b, *j_carry, p2)
            rot = b.rot
        elif t < T_REL:
            u = M.progress(t, T_SWING, T_REL, "inout")
            b = p2_bob(t)
            x = M.lerp(j_carry[0], j_throw[0], u) + b.dx
            y = M.lerp(j_carry[1], j_throw[1], u) - 30 * math.sin(math.pi * u) + b.dy
            rot = -14 * math.sin(math.pi * u)
        else:
            u = (t - T_REL) / (T_CATCH - T_REL)
            b = p2_bob(T_REL)
            sx0, sy0 = j_throw[0] + b.dx, j_throw[1] + b.dy
            x = M.lerp(sx0, catch_at[0], u)
            y = M.lerp(sy0, catch_at[1], u) - 150 * 4 * u * (1 - u)
            rot = 28 * math.sin(math.pi * u)
        return Tf(dx=x - j_carry[0], dy=y - j_carry[1], rot=rot, px=j_carry[0], py=j_carry[1])

    sc.add("jar_pier", doc(PR.jar(*j_carry, JAR_S)), motion=jar_pier_tf)

    # ---------------------------------------------------------------- Jonah on land
    def jland_frame(t):
        if t < T_REFUSE:
            return 0.0
        if t < T_TURN + 0.1:
            return 1.0
        if t < T_LEAP:
            return 2.0 + float(int((t - T_TURN - 0.1) * 6.5) % 2)
        return 3.0

    jland = [doc(C.jonah(JX0, GY, K, 1, pose="stand", expr="worried")),
             doc(C.jonah(JX0, GY, K, 1, pose="refuse", expr="scared")),
             doc(C.jonah(JX0, GY, K, -1, pose="run_a", expr="worried")),
             doc(C.jonah(JX0, GY, K, -1, pose="run_b", expr="worried"))]

    def jland_tf(t):
        if t >= T_SWAP:
            return Tf(alpha=0.0)
        x, y = jpos(t)
        rot = 0.0
        sx = sy = 1.0
        dy = 0.0
        if t < T_REFUSE:
            sy = 1 + 0.012 * math.sin(2 * math.pi * t / 2.2)
        if T_REFUSE + 0.08 < t < T_TURN - 0.05:   # shaking his head "no"
            env = min(1.0, (t - T_REFUSE - 0.08) / 0.15, (T_TURN - 0.05 - t) / 0.2)
            rot = 2.6 * env * math.sin(2 * math.pi * 3.4 * (t - T_REFUSE))
        if T_TURN <= t < T_TURN + 0.2:           # spin round
            u = (t - T_TURN) / 0.2
            sx = 1 - 0.78 * math.sin(math.pi * u)
            dy = -16 * math.sin(math.pi * u)
        if T_RUN <= t < T_LEAP:
            dy = -7 * abs(math.sin(math.pi * 6.5 * (t - T_TURN - 0.1)))
        return Tf(dx=x - JX0, dy=y - GY + dy, rot=rot, sx=sx, sy=sy, px=JX0, py=GY)

    # dust puffs kicked up behind his heels while he runs on the road (none on the planks)
    STRIDE = 1 / 6.5
    t_steps = [T_RUN + 0.05 + k * STRIDE for k in range(int((T_LEAP - T_RUN) / STRIDE) + 1)]
    puffs = [(ts_, jpos(ts_)[0] + 46 * K) for ts_ in t_steps if jpos(ts_)[0] > PIER_X1 + 40]
    PUFF_LIFE = 0.5

    def dust(t):
        live = [(t - ts_, x) for ts_, x in puffs if 0 <= t - ts_ <= PUFF_LIFE]
        if not live:
            return None
        x0 = min(x for _, x in live) - 70
        x1 = max(x for _, x in live) + 110
        y0, y1 = GY - 90, GY + 30
        im = Image.new("RGBA", (int(x1 - x0), int(y1 - y0)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for age, x in live:
            u = age / PUFF_LIFE
            a = int(215 * (1 - u) ** 1.2)
            for j, (ox, oy, r) in enumerate(((0, -10, 16), (22, -18, 13), (-16, -16, 11), (12, -32, 9))):
                rr = r * (0.7 + 1.1 * u)
                cx = x - x0 + ox * (1 + u) + 40 * u
                cy = GY - y0 + oy * (1 + 0.8 * u) - 14 * u
                d.ellipse([cx - rr * 1.3, cy - rr, cx + rr * 1.3, cy + rr], fill=(232, 210, 164, a),
                          outline=(150, 112, 74, int(a * 0.55)), width=2)
        return im.filter(ImageFilter.GaussianBlur(0.8)), (x0, y0)

    sc.add_dynamic("dust", dust)
    sc.add("jonah_shadow", doc(C.ground_shadow(JX0, GY + 2, K, 130, 0.25)),
           motion=lambda t: Tf(dx=jpos(min(t, T_LEAP))[0] - JX0,
                               alpha=1 - M.progress(t, T_LEAP, T_LEAP + 0.2, "linear")))
    sc.add("jonah_land", jland, motion=jland_tf, frame_at=jland_frame)

    # a butterfly flitting by the signpost (crossroads life during line 0)
    def butterfly(x, y, open_):
        k = 1.0 if open_ else 0.35
        wing = P["gold"]
        return S.g(f'<ellipse cx="{f1(x - 9 * k)}" cy="{y - 6}" rx="{f1(11 * k)}" ry="9" fill="{wing}" '
                   f'stroke="{P["ink"]}" stroke-width="2.2"/>'
                   f'<ellipse cx="{f1(x + 9 * k)}" cy="{y - 6}" rx="{f1(11 * k)}" ry="9" fill="{S.shade(wing, 0.2)}" '
                   f'stroke="{P["ink"]}" stroke-width="2.2"/>'
                   f'<ellipse cx="{f1(x - 6 * k)}" cy="{y + 5}" rx="{f1(7 * k)}" ry="6" fill="{P["sun_hot"]}" '
                   f'stroke="{P["ink"]}" stroke-width="2"/>'
                   f'<ellipse cx="{f1(x + 6 * k)}" cy="{y + 5}" rx="{f1(7 * k)}" ry="6" fill="{P["sun_hot"]}" '
                   f'stroke="{P["ink"]}" stroke-width="2"/>'
                   f'<path d="M{x},{y - 12} L{x},{y + 10}" stroke="{P["ink"]}" stroke-width="3.2" stroke-linecap="round"/>'
                   f'<path d="M{x},{y - 12} q-4,-10 -9,-12 M{x},{y - 12} q4,-10 9,-12" stroke="{P["ink"]}" '
                   f'stroke-width="1.8" fill="none"/>', filter="wobble-fine")

    BFX, BFY = 3720, 820
    sc.add("butterfly", [doc(butterfly(BFX, BFY, True)), doc(butterfly(BFX, BFY, False))],
           frame_at=lambda t: float(int(t * 11) % 2), wc=0.4,
           motion=lambda t: Tf(dx=-60 * math.sin(t * 0.9) + 25 * math.sin(t * 2.3) + 120 * max(0.0, t - 3.0),
                               dy=-30 * math.sin(t * 1.3 + 0.5) - 12 * abs(math.sin(t * 5.5))
                               - 80 * max(0.0, t - 3.0)))

    # ---------------------------------------------------------------- foreground + gulls
    sc.add("foreground", foreground_svg())

    wing = (1, 0.5, 0, -0.5, -1, -0.5, 0, 0.5)

    def gull_layer(name, x, y, s, f, vx, vy, fps, phase):
        frames = [doc(PR.gull(x, y, s, f, wing=w)) for w in wing]
        sc.add(name, frames, frame_at=lambda t: float(int(t * fps + phase) % len(wing)),
               motion=lambda t: Tf(dx=vx * t, dy=vy * t + 10 * math.sin(t * 1.7 + phase)), wc=0.6)

    gull_layer("gull1", 2760, 400, 0.7, -1, -110, 4, 9, 0)
    gull_layer("gull2", 1650, 300, 0.55, -1, -70, -3, 8, 3)

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-13, fade_in=0.8, fade_out=0.8)
    sc.sfx("birds", 0, dur=T_RUN + 1.2, gain_db=-20, fade_in=0.8, fade_out=0.8, pan=0.4)
    sc.sfx("whoosh", T_TURN - 0.05, gain_db=-8, pan=0.2)
    sc.sfx("footsteps_run", T_RUN, dur=T_LEAP - T_RUN + 0.05, gain_db=-9, fade_in=0.05, fade_out=0.15)
    sc.sfx("whoosh", T_LEAP, gain_db=-12, pan=-0.1)
    sc.sfx("thud", T_LAND, gain_db=-13)
    sc.sfx("gull", L1.start + 0.9, gain_db=-15, pan=-0.3)
    sc.sfx("ship_creak", T_LAND + 0.1, dur=T - T_LAND + 0.7, gain_db=-12, fade_in=0.4, fade_out=0.8)
    sc.sfx("cloth", T_SAIL, gain_db=-14)
    sc.sfx("gull", L2.start + 0.7, gain_db=-16, pan=0.4)
    return sc
