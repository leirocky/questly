"""Scene 10 — Nineveh repents (Jonah 3:5-10).

The people and the king believe God, wear sackcloth and fast; God sees and has mercy.

Staging (one 2800 x 1575 stage, no cuts; the wide shot is the whole stage at ~0.69 output px per stage px):
  * line 0 — close on the king in his open palace portico, seated on his purple throne. A messenger (olive robe,
    long dark hair - deliberately NOT Jonah's cream head-cloth) tells him the news (sound arcs), then turns and
    points out to the city. The king is startled, rises from his throne (squash, near-cut to standing right in
    front of it, then a few bobbing steps forward) and takes off his tall crown. Through the portico we see the
    city under a heavy grey cloud.
  * line 1 — "都穿上麻衣": the king turns to the throne; in a little cloth-swirl puff his purple robe becomes burlap
    sackcloth and the folded robe with the crown on top arcs out of his hands onto the throne seat (Jonah 3:6
    "laid his robe from him"). A heap of ashes appears and he sits down in it, head bowed. The messenger and the
    far townspeople kneel; the camera pulls out to the whole city: the people in sackcloth (men, women,
    children, elders) kneel in prayer in a wave across the square, and even the animals wear sackcloth blankets.
  * lines 2-3 — "上帝看见…就怜悯他们": the heavy grey cloud over the city parts in the middle and warm golden light
    shines through the gap and pours down in rays (God's mercy - never drawn as a person); the banks drift apart
    and dissolve, the sky turns gold, sparkles drift; then "没有降下灾祸": the people and the king look up with
    relief and joy, children jump and cheer, doves rise from behind the rooftops.

Pose changes are near-cuts (0.06 s) hidden at the bottom of a small dip / squash; only expression changes use a
longer crossfade. The grey cloud banks sit ABOVE the cool gloom glaze (their colours are pre-darkened), so the
golden gleam between the gloom and the banks shows warm through the parting gap.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 2800, 1575

# palace geometry -----------------------------------------------------------------------------------------
WALL_X1 = 690              # right edge of the palace back wall
COL1_X, COL2_X = 712, 1186  # column centres (the portico opening lies between them)
COL_W = 80
LINTEL_Y0, LINTEL_Y1 = 300, 418
DAIS_BACK, DAIS_Y, DAIS_FRONT = 1160, 1255, 1292   # dais top: back edge, where people stand, front edge
DAIS_BOTTOM = 1400
DAIS_X1 = 1310

KS = 1.15                  # king scale
THRONE_X, THRONE_Y = 430, 1240
SPOT_X, SPOT_Y = 770, 1258  # where the king stands, sits in ashes and kneels
RISE_X = 600               # where he first stands up, just in front of the throne's footstool
MSG_X, MSG_Y, MSG_S, MSG_V = 1180, 1262, 1.1, 2   # messenger: man variant 2 (olive robe, long dark hair)
GAP_X = 1965               # where the grey cloud parts and the golden light breaks through
BUNDLE_X, BUNDLE_Y = THRONE_X - 8, THRONE_Y - 74 * KS   # folded robe + crown resting on the throne cushion

PLAZA_Y = 1012             # back edge of the square (house fronts)
SKY_H = 1060               # the sky layers stop here (hidden by the square below)
HOUSE_Y = 1036


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


CUT = 0.06                 # near-cut for real pose changes (2 frames at 30 fps)


def sched(entries, fade=CUT):
    """entries [(t, idx) or (t, idx, fade)] with idx increasing by one each step -> frame_at.

    Each change starts at t and crossfades over its fade: use CUT for pose changes (hide them under a dip, see
    ``hop``) and a longer fade only when just the expression changes.
    """
    entries = sorted((e[0], e[1], e[2] if len(e) > 2 else fade) for e in entries)

    def fa(t):
        v = float(entries[0][1])
        for (t0, i0, _), (t1, i1, f) in zip(entries, entries[1:]):
            if t >= t1:
                v = float(i1)
                if t < t1 + f:
                    v = i0 + (i1 - i0) * M.progress(t, t1, t1 + f, "sine")
        return v
    return fa


def hop(t0, keys, pivot, curves="sine"):
    """Additive keyed bump around t0: keys [(dt, {dx, dy, rot, sx, sy, s})] that start and end at identity."""
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


# ============================================================================ backgrounds


def sky_grey_svg():
    defs = S.lin_grad("s10skyg", [(0, "#7c8096"), (0.4, "#9a9bae"), (0.72, "#b9b6b8"), (1, "#d3c9b8")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_H + 20}" fill="url(#s10skyg)"/>', defs)


def sky_gold_svg():
    """Clear sky after God's mercy: pale blue-cream at the top (keeps some contrast) warming to gold at the sun."""
    defs = (S.lin_grad("s10skyw", [(0, "#c4dfea"), (0.3, "#e9e0c6"), (0.64, "#fae2b0"), (1, "#fff1d2")]) +
            S.rad_grad("s10sun", [(0, "#fff8dc", 1), (0.25, "#ffefb8", 0.85), (0.6, "#ffe09a", 0.35),
                                  (1, "#ffd98a", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_H + 20}" fill="url(#s10skyw)"/>'
            f'<ellipse cx="{GAP_X - 20}" cy="40" rx="900" ry="620" fill="url(#s10sun)"/>')
    return doc(body, defs)


def fair_clouds_svg():
    """Small cream fair-weather clouds (own layer so they can drift)."""
    fair = ""
    for cx, cy, w, h, seed in ((520, 175, 300, 95, 31), (1150, 110, 240, 80, 32), (2520, 210, 320, 100, 33),
                               (1560, 300, 200, 64, 34)):
        fair += S.cloud(cx, cy, w, h, "#fff6e2", seed=seed, sw=3, shade_fill="#f6d9a8")
    return doc(S.g(fair, filter="wobble"))


def cloud_bank_svg(items, fill, shade, extra=""):
    body = extra
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, fill, seed=seed, puffs=6, sw=3.5, shade_fill=shade)
    return doc(S.g(body, filter="wobble"))


def city_svg():
    """Far skyline, house row and the paved square (static)."""
    defs = (S.lin_grad("s10plaza", [(0, "#e8d0a2"), (0.35, "#e2c493"), (1, "#d2ac76")]) +
            S.lin_grad("s10haze", [(0, "#f1e2c4", 0), (1, "#f1e2c4", 0.55)]))
    body = PR.nineveh_skyline(300, 2900, 985, scale=0.95, seed=2, haze=0.42)
    body += f'<rect x="-20" y="760" width="{SW + 40}" height="260" fill="url(#s10haze)"/>'
    # paved square
    plaza = (f'<path d="M-30,{PLAZA_Y} L{SW + 30},{PLAZA_Y} L{SW + 30},{SH + 30} L-30,{SH + 30} Z" '
             f'fill="url(#s10plaza)" stroke="{P["ink"]}" stroke-width="3"/>')
    joints = ""
    vx, vy = 1900, 640
    y = PLAZA_Y + 26
    k = 0
    while y < SH + 20:
        joints += f'<path d="M-30,{f1(y)} L{SW + 30},{f1(y)}"/>'
        k += 1
        y += 22 + k * 9
    for i in range(-14, 22):
        xb = vx + i * 260
        # line from the back edge toward the viewer, converging on the vanishing point
        t0 = (PLAZA_Y - vy) / (SH + 40 - vy)
        x_top = vx + (xb - vx) * t0
        joints += f'<path d="M{f1(x_top)},{PLAZA_Y} L{f1(xb)},{SH + 40}"/>'
    plaza += (f'<g stroke="{P["ink_soft"]}" stroke-width="2" opacity="0.22" fill="none" '
              f'stroke-linecap="round">{joints}</g>')
    body += S.g(plaza, filter="wobble")
    # houses along the back of the square, palms between them
    deco = ""
    for x, s, ln in ((1655, 0.5, -0.15), (2300, 0.55, 0.1), (2690, 0.48, -0.1)):
        deco += PR.palm_tree(x, HOUSE_Y - 6, s, lean=ln)
    houses = ""
    for x, v, fc in ((1460, 2, -1), (1880, 0, 1), (2130, 1, -1), (2490, 3, 1), (2800, 0, -1)):
        houses += PR.house(x, HOUSE_Y, 0.42, variant=v, facing=fc)
    body += deco + houses
    # a few pots and a well-curb at the back of the square
    body += PR.jar(1610, HOUSE_Y + 4, 0.45) + PR.jar(1650, HOUSE_Y + 8, 0.36)
    body += PR.sack(2005, HOUSE_Y + 14, 0.42, seed=3)
    return doc(body, defs)


# ============================================================================ palace


def rosettes(x0, x1, y, step, r, fill="#f6ead0", centre="#e8b63c"):
    out = ""
    x = x0
    while x <= x1:
        petals = "".join(
            f'<ellipse cx="{f1(x + r * 0.55 * math.cos(a))}" cy="{f1(y + r * 0.55 * math.sin(a))}" '
            f'rx="{f1(r * 0.42)}" ry="{f1(r * 0.42)}" fill="{fill}"/>'
            for a in [i * math.pi / 4 for i in range(8)])
        out += petals + f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.38)}" fill="{centre}"/>'
        x += step
    return out


def column(cx, top, bottom, w=COL_W):
    h = bottom - top
    sh = (f'<rect x="{cx - w / 2}" y="{top + 60}" width="{w}" height="{h - 100}" fill="url(#s10col)" '
          f'stroke="{P["ink"]}" stroke-width="4"/>')
    flutes = "".join(f'<path d="M{f1(cx - w / 2 + w * k / 5)},{top + 80} L{f1(cx - w / 2 + w * k / 5)},'
                     f'{bottom - 50}" stroke="{P["stone_dark"]}" stroke-width="2.5" opacity="0.7"/>'
                     for k in range(1, 5))
    bands = ""
    for yy in (top + 120, bottom - 110):
        bands += (f'<rect x="{cx - w / 2 - 3}" y="{yy}" width="{w + 6}" height="18" rx="4" fill="{P["crown"]}" '
                  f'stroke="{P["ink"]}" stroke-width="3"/>')
    cap = (f'<path d="M{cx - w / 2 - 34},{top + 62} C{cx - w / 2 - 62},{top + 50} {cx - w / 2 - 58},{top + 6} '
           f'{cx - w / 2 - 26},{top + 10} L{cx + w / 2 + 26},{top + 10} C{cx + w / 2 + 58},{top + 6} '
           f'{cx + w / 2 + 62},{top + 50} {cx + w / 2 + 34},{top + 62} Z" fill="{P["crown"]}" '
           f'stroke="{P["ink"]}" stroke-width="4"/>'
           f'<circle cx="{cx - w / 2 - 34}" cy="{top + 38}" r="11" fill="none" stroke="{P["ink"]}" '
           f'stroke-width="3"/><circle cx="{cx + w / 2 + 34}" cy="{top + 38}" r="11" fill="none" '
           f'stroke="{P["ink"]}" stroke-width="3"/>'
           f'<rect x="{cx - w / 2 - 14}" y="{top}" width="{w + 28}" height="14" fill="{S.shade(P["crown"], -0.2)}" '
           f'stroke="{P["ink"]}" stroke-width="3"/>')
    base = (f'<path d="M{cx - w / 2 - 22},{bottom} L{cx - w / 2 - 14},{bottom - 40} L{cx + w / 2 + 14},'
            f'{bottom - 40} L{cx + w / 2 + 22},{bottom} Z" fill="{P["stone_dark"]}" stroke="{P["ink"]}" '
            f'stroke-width="4"/>')
    return sh + flutes + bands + cap + base


def palace_svg():
    defs = (S.lin_grad("s10wall", [(0, "#dcc093"), (1, "#c9a774")]) +
            S.lin_grad("s10col", [(0, "#efdcb8"), (0.55, "#dfc495"), (1, "#c8a571")], x2=1, y2=0) +
            S.lin_grad("s10curt", [(0, "#8a5cae"), (1, "#5f3c80")]) +
            S.lin_grad("s10floor", [(0, "#cfb184"), (1, "#e3cba0")]) +
            S.lin_grad("s10front", [(0, "#c49e6a"), (1, "#a9834f")]) +
            S.lin_grad("s10shadow", [(0, P["ink"], 0.35), (1, P["ink"], 0)]))
    ink = P["ink"]
    # back wall with brick courses
    wall = (f'<rect x="-30" y="{LINTEL_Y1 - 10}" width="{WALL_X1 + 30}" height="{DAIS_BACK - LINTEL_Y1 + 20}" '
            f'fill="url(#s10wall)" stroke="{ink}" stroke-width="4"/>')
    bricks = ""
    r = random.Random(3)
    y = LINTEL_Y1 + 40
    row = 0
    while y < DAIS_BACK:
        bricks += f'<path d="M-30,{y} L{WALL_X1},{y}"/>'
        off = 0 if row % 2 else 45
        for x in range(-30 + off, WALL_X1, 90):
            if r.random() < 0.55:
                bricks += f'<path d="M{x},{y - 40} L{x},{y}"/>'
        y += 40
        row += 1
    wall += f'<g stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.55" fill="none">{bricks}</g>'
    # glazed blue band with rosettes (top) and a low blue dado
    wall += (f'<rect x="-30" y="{LINTEL_Y1 + 22}" width="{WALL_X1 + 30}" height="56" fill="#3f79a8" '
             f'stroke="{ink}" stroke-width="3.5"/>' + rosettes(10, WALL_X1 - 20, LINTEL_Y1 + 50, 72, 19))
    wall += (f'<rect x="-30" y="{DAIS_BACK - 64}" width="{WALL_X1 + 30}" height="50" fill="#4a86b2" '
             f'stroke="{ink}" stroke-width="3.5"/>'
             + "".join(f'<path d="M{x},{DAIS_BACK - 22} l22,-22 l22,22" fill="none" stroke="#f3e6c8" '
                       f'stroke-width="4"/>' for x in range(-20, WALL_X1 - 30, 44)))
    # royal curtain behind the throne
    cx0, cx1, ct, cb = 262, 640, LINTEL_Y1 + 92, DAIS_BACK - 64
    folds = ""
    pts = [(cx0, ct)]
    n = 7
    for i in range(n + 1):
        x = cx0 + (cx1 - cx0) * i / n
        folds += (f'<path d="M{f1(x + 22)},{ct + 8} C{f1(x + 30)},{ct + 300} {f1(x + 14)},{cb - 200} '
                  f'{f1(x + 26)},{cb - 6}" stroke="#4d2f6a" stroke-width="7" opacity="0.45" fill="none"/>')
    curtain = (f'<path d="M{cx0},{ct} L{cx1},{ct} L{cx1 + 6},{cb} '
               + " ".join(f'Q{f1(cx1 - (cx1 - cx0) * (i + 0.5) / n)},{cb + 22} {f1(cx1 - (cx1 - cx0) * (i + 1) / n)},{cb}'
                          for i in range(n))
               + f' Z" fill="url(#s10curt)" stroke="{ink}" stroke-width="4"/>')
    fringe = "".join(f'<path d="M{f1(x)},{cb + 4} l0,22" stroke="{P["crown"]}" stroke-width="5" '
                     f'stroke-linecap="round"/>' for x in range(cx0 + 8, cx1, 16))
    border = (f'<path d="M{cx0 + 18},{ct + 20} L{cx0 + 18},{cb - 14} M{cx1 - 18},{ct + 20} L{cx1 - 14},{cb - 14}" '
              f'stroke="{P["crown"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    emblem = (f'<circle cx="{(cx0 + cx1) / 2}" cy="{ct + 150}" r="54" fill="{P["crown"]}" stroke="{ink}" '
              f'stroke-width="4"/>' + rosettes((cx0 + cx1) / 2, (cx0 + cx1) / 2, ct + 150, 100, 44,
                                               fill="#fff3d6", centre="#c9714a"))
    rod = (f'<rect x="{cx0 - 30}" y="{ct - 12}" width="{cx1 - cx0 + 60}" height="16" rx="8" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/><circle cx="{cx0 - 30}" cy="{ct - 4}" r="15" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/><circle cx="{cx1 + 30}" cy="{ct - 4}" r="15" fill="{P["crown"]}" '
           f'stroke="{ink}" stroke-width="3.5"/>')
    wall += curtain + folds + border + fringe + emblem + rod
    # columns and lintel
    cols = column(COL1_X, LINTEL_Y1 - 4, DAIS_BACK + 14) + column(COL2_X, LINTEL_Y1 - 4, DAIS_BACK + 14)
    lintel = (f'<rect x="-30" y="{LINTEL_Y0}" width="{COL2_X + 110}" height="{LINTEL_Y1 - LINTEL_Y0}" '
              f'fill="#d6b682" stroke="{ink}" stroke-width="4.5"/>'
              f'<rect x="-30" y="{LINTEL_Y0 + 30}" width="{COL2_X + 110}" height="56" fill="#3f79a8" '
              f'stroke="{ink}" stroke-width="3.5"/>' + rosettes(16, COL2_X + 60, LINTEL_Y0 + 58, 76, 20))
    merlons = ""
    for x in range(-20, COL2_X + 60, 92):
        merlons += (f'<path d="M{x},{LINTEL_Y0} L{x},{LINTEL_Y0 - 26} L{x + 14},{LINTEL_Y0 - 26} '
                    f'L{x + 14},{LINTEL_Y0 - 48} L{x + 30},{LINTEL_Y0 - 48} L{x + 30},{LINTEL_Y0 - 66} '
                    f'L{x + 46},{LINTEL_Y0 - 66} L{x + 46},{LINTEL_Y0 - 48} L{x + 62},{LINTEL_Y0 - 48} '
                    f'L{x + 62},{LINTEL_Y0 - 26} L{x + 76},{LINTEL_Y0 - 26} L{x + 76},{LINTEL_Y0} Z" '
                    f'fill="#cfae79" stroke="{ink}" stroke-width="4"/>')
    under = (f'<rect x="-30" y="{LINTEL_Y1}" width="{WALL_X1 + 30}" height="70" fill="url(#s10shadow)" '
             f'opacity="0.5"/>')
    # dais top (floor) and front face with steps
    floor = (f'<path d="M-30,{DAIS_BACK} L{DAIS_X1 - 50},{DAIS_BACK} L{DAIS_X1},{DAIS_FRONT} L-30,{DAIS_FRONT} Z" '
             f'fill="url(#s10floor)" stroke="{ink}" stroke-width="4"/>')
    tiles = ""
    for i in range(1, 4):
        yy = DAIS_BACK + (DAIS_FRONT - DAIS_BACK) * i / 4
        tiles += f'<path d="M-30,{f1(yy)} L{f1(DAIS_X1 - 50 + 50 * i / 4)},{f1(yy)}"/>'
    for x in range(40, DAIS_X1, 120):
        tiles += f'<path d="M{x},{DAIS_BACK} L{x - 12},{DAIS_FRONT}"/>'
    floor += f'<g stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.5" fill="none">{tiles}</g>'
    # rug under the throne
    floor += (f'<path d="M190,{DAIS_BACK + 30} L640,{DAIS_BACK + 30} L670,{DAIS_FRONT - 12} L160,{DAIS_FRONT - 12} Z" '
              f'fill="#a84a3c" stroke="{ink}" stroke-width="3.5"/>'
              f'<path d="M214,{DAIS_BACK + 44} L622,{DAIS_BACK + 44} L644,{DAIS_FRONT - 26} L188,{DAIS_FRONT - 26} Z" '
              f'fill="none" stroke="{P["crown"]}" stroke-width="5"/>')
    front = (f'<path d="M-30,{DAIS_FRONT} L{DAIS_X1},{DAIS_FRONT} L{DAIS_X1},{DAIS_BOTTOM} L-30,{DAIS_BOTTOM} Z" '
             f'fill="url(#s10front)" stroke="{ink}" stroke-width="4"/>'
             f'<rect x="-30" y="{DAIS_FRONT + 22}" width="{DAIS_X1 + 30}" height="40" fill="#3f79a8" '
             f'stroke="{ink}" stroke-width="3.5"/>' + rosettes(10, DAIS_X1 - 20, DAIS_FRONT + 42, 64, 14))
    side = (f'<path d="M{DAIS_X1 - 50},{DAIS_BACK} L{DAIS_X1},{DAIS_FRONT} L{DAIS_X1},{DAIS_BOTTOM} '
            f'L{DAIS_X1 - 50},{DAIS_BOTTOM - 110} Z" fill="#b18c58" stroke="{ink}" stroke-width="4"/>')
    steps = ""
    for i in range(3):
        x0, x1 = 940 - 26 * i, 1270 + 26 * i
        y0 = DAIS_FRONT + 8 + 36 * i
        steps += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{DAIS_BOTTOM - y0 + 18 + 8 * i}" '
                  f'fill="{S.mix("#e3cba0", "#c49e6a", 0.25 + 0.2 * i)}" stroke="{ink}" stroke-width="4"/>'
                  f'<path d="M{x0 + 4},{y0 + 12} L{x1 - 4},{y0 + 12}" stroke="#f1e2c4" stroke-width="5" '
                  f'opacity="0.8"/>')
    # potted palms at the far left of the dais
    pots = (PR.palm_tree(118, DAIS_BACK + 30 - 110, 0.42, lean=0.1, dates=False)
            + PR.jar(118, DAIS_BACK + 30 - 52, 1.05, color="#c46f48"))
    body = (S.g(wall, filter="wobble") + S.g(cols + lintel + merlons, filter="wobble") + under
            + S.g(floor + front + side, filter="wobble") + S.g(steps, filter="wobble") + pots)
    return doc(body, defs)


def throne_svg():
    return doc(PR.throne(THRONE_X, THRONE_Y, KS, 1))


def crown_svg_markup(cx, by, s=1.0, tilt=-8):
    """The king's tall gold crown lying on the throne cushion (local drawing, bottom centre at (cx, by))."""
    ink = P["ink"]
    w, h = 84 * s, 70 * s
    body = (f'<path d="M{-w / 2},0 L{-w / 2 * 0.92},{-h} A{w / 2 * 0.92},{12 * s} 0 0 1 {w / 2 * 0.92},{-h} '
            f'L{w / 2},0 A{w / 2},{13 * s} 0 0 1 {-w / 2},0 Z" fill="{P["crown"]}" stroke="{ink}" '
            f'stroke-width="{4 * s}" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="{-h}" rx="{w / 2 * 0.92}" ry="{12 * s}" fill="{S.shade(P["crown"], 0.35)}" '
            f'stroke="{ink}" stroke-width="{3.5 * s}"/>'
            f'<path d="M{-10 * s},{-h - 4 * s} L0,{-h - 34 * s} L{10 * s},{-h - 4 * s} Z" fill="{P["crown"]}" '
            f'stroke="{ink}" stroke-width="{3.5 * s}" stroke-linejoin="round"/>'
            f'<path d="M{-w / 2 + 3},{-12 * s} A{w / 2},{12 * s} 0 0 0 {w / 2 - 3},{-12 * s}" fill="none" '
            f'stroke="{S.shade(P["crown"], -0.25)}" stroke-width="{6 * s}"/>')
    for k, xx in enumerate((-24, 0, 24)):
        body += (f'<circle cx="{xx * s}" cy="{-h * 0.52 + (4 if k != 1 else 6) * s}" r="{7.5 * s}" '
                 f'fill="{P["royal"]}" stroke="{ink}" stroke-width="{2.5 * s}"/>')
    return f'<g transform="translate({f1(cx)},{f1(by)}) rotate({tilt})">{body}</g>'


def bundle_svg():
    """The king's purple robe, folded, with a sleeve hanging over the front of the seat and the crown on top.

    Drawn resting on the throne cushion (bottom centre at BUNDLE_X, BUNDLE_Y); the layer's motion flies it there
    from the king's hands.
    """
    ink, k = P["ink"], KS * 0.92
    royal, light, dark, gold = P["royal"], P["royal_light"], S.shade(P["royal"], -0.25), P["crown"]
    # folded stack: two soft layers, the top one slightly shorter
    low = (f'<path d="M-82,0 C-88,-14 -86,-26 -76,-30 L74,-32 C86,-28 90,-12 84,0 Z" fill="{dark}" '
           f'stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>')
    top = (f'<path d="M-74,-26 C-80,-40 -74,-54 -60,-56 L58,-58 C72,-56 78,-42 72,-28 C40,-22 -40,-22 -74,-26 Z" '
           f'fill="{royal}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
           f'<path d="M-60,-50 C-20,-54 30,-55 62,-52" stroke="{light}" stroke-width="6" fill="none" '
           f'stroke-linecap="round"/>'
           f'<path d="M-72,-30 C-40,-26 40,-26 72,-31" stroke="{gold}" stroke-width="7" fill="none" '
           f'stroke-linecap="round"/>')
    # a sleeve hanging over the front edge of the seat, gold cuff and a few fringe threads
    sleeve = (f'<path d="M58,-30 C80,-30 96,-14 98,10 C100,34 96,52 90,64 L64,62 C68,44 70,22 64,4 Z" '
              f'fill="{royal}" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>'
              f'<path d="M64,58 L91,60" stroke="{gold}" stroke-width="9" stroke-linecap="round"/>'
              + "".join(f'<path d="M{66 + 6 * i},66 l0,12" stroke="{gold}" stroke-width="3.5" '
                        f'stroke-linecap="round"/>' for i in range(5)))
    crown = crown_svg_markup(-6, -52, 0.8, tilt=-7)
    body = f'<g transform="translate({f1(BUNDLE_X)},{f1(BUNDLE_Y)}) scale({k:.3f})">{low + sleeve + top + crown}</g>'
    return doc(S.g(body, filter="wobble-fine"))


def puff_svg(cx, cy, rx, ry, seed=0, k=1.0):
    """A cartoon 'quick change' poof: small soft dust clouds hugging the sides and feet of a figure, and a few
    short whoosh lines at its sides (never over the face)."""
    rng = random.Random(seed)
    dust = ""
    for i, deg in enumerate((-25, 8, 40, 72, 108, 140, 172, 205)):
        a = math.radians(deg + rng.uniform(-6, 6))
        px, py = cx + rx * 0.92 * math.cos(a), cy + ry * 0.95 * math.sin(a)
        w = k * rng.uniform(62, 84)
        dust += S.cloud(px, py, w, w * 0.62, "#f1e6cc", seed=seed * 17 + i, puffs=3, sw=2.4, shade_fill="#dfcda8")
    lines = ""
    for a0, span, rr in ((-48, 40, 1.22), (-8, 34, 1.32), (188, -40, 1.22), (148, -34, 1.32)):
        pts = [(cx + rx * rr * math.cos(math.radians(a0 + span * j / 6)),
                cy + ry * rr * 0.92 * math.sin(math.radians(a0 + span * j / 6))) for j in range(7)]
        lines += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["ink_soft"]}" '
                  f'stroke-width="{4.5 * k:.1f}" stroke-linecap="round" opacity="0.75"/>')
    return doc(S.g(lines, filter="wobble-fine") + S.g(dust, filter="wobble-fine", opacity=0.92))


def ash_heap(x, y, s, part):
    """Scene-local heap of ashes (a soft grey mound, a few charcoal lumps, one small charred stick).

    Replaces props.ash_pile here, whose crossed logs read as a campfire next to the seated king. Anchor: bottom
    centre on the ground. part 'back' = the mound behind the sitter, 'front' = the low lip of ash in front.
    """
    ink = P["ink"]
    pale, mid, dark = S.shade(P["ash"], 0.4), S.shade(P["ash"], 0.12), S.shade(P["ash"], -0.16)
    coal = S.mix(P["ash"], ink, 0.62)
    rng = random.Random(23 if part == "back" else 29)
    out = ""
    if part == "back":
        pts = [(-158, 2), (-146, -22), (-126, -44), (-98, -64), (-66, -80), (-30, -90), (6, -90), (40, -82),
               (74, -66), (104, -46), (130, -24), (152, 2)]
        d = S.smooth_path(pts, closed=False) + " Z"
        cid = f"s10ash{part}"
        inner = (f'<path d="M-170,-24 C-90,-34 60,-30 170,-20 L170,10 L-170,10 Z" fill="{dark}"/>'
                 f'<path d="{S.blob(-18, -74, 80, 20, 0.15, 9, 4)}" fill="{pale}" opacity="0.9"/>'
                 f'<path d="{S.blob(70, -50, 34, 11, 0.2, 7, 5)}" fill="{pale}" opacity="0.7"/>')
        for _ in range(24):
            px, py = rng.uniform(-130, 130), rng.uniform(-80, -6)
            inner += (f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{f1(rng.uniform(1.6, 3.2))}" '
                      f'fill="{rng.choice((pale, dark, coal))}" opacity="0.6"/>')
        out += (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{mid}"/>'
                f'<g clip-path="url(#{cid})">{inner}</g><path d="{d}" fill="none" stroke="{ink}" stroke-width="4" '
                f'stroke-linejoin="round"/>')
        # one small charred stick poking out on the far side
        out += (f'<path d="M98,-40 L132,-62" stroke="{ink}" stroke-width="11" stroke-linecap="round"/>'
                f'<path d="M98,-40 L132,-62" stroke="{coal}" stroke-width="6" stroke-linecap="round"/>')
        for cx, cy, r in ((-86, -40, 8), (-40, -60, 6), (34, -36, 7), (110, -16, 6)):
            out += (f'<path d="{S.blob(cx, cy, r * 1.3, r, 0.25, 7, cx + 300)}" fill="{coal}" stroke="{ink}" '
                    f'stroke-width="2.5"/>')
    else:
        pts = [(-186, 2), (-170, -8), (-136, -18), (-90, -24), (-36, -26), (20, -27), (76, -24), (126, -18),
               (162, -9), (180, 2)]
        d = S.smooth_path(pts, closed=False) + " Z"
        out += (f'<path d="{d}" fill="{pale}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>'
                f'<path d="M-150,-4 C-60,-10 60,-10 156,-4" stroke="{mid}" stroke-width="7" fill="none" '
                f'stroke-linecap="round" opacity="0.7"/>')
        for _ in range(16):
            px, py = rng.uniform(-150, 150), rng.uniform(-18, -3)
            out += (f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{f1(rng.uniform(1.6, 3.0))}" '
                    f'fill="{rng.choice((mid, dark, coal))}" opacity="0.65"/>')
        for cx, cy, r in ((-112, -8, 6), (-14, -12, 5), (92, -9, 6)):
            out += (f'<path d="{S.blob(cx, cy, r * 1.3, r, 0.25, 7, cx + 500)}" fill="{coal}" stroke="{ink}" '
                    f'stroke-width="2.4"/>')
        for _ in range(12):
            px = rng.choice((-1, 1)) * rng.uniform(176, 206)
            out += (f'<circle cx="{f1(px)}" cy="{f1(rng.uniform(-5, 0))}" r="{f1(rng.uniform(2, 3.6))}" '
                    f'fill="{mid}" opacity="0.75"/>')
    return f'<g transform="translate({f1(x)},{f1(y)}) scale({s:.3f})" filter="url(#wobble-fine)">{out}</g>'


# ============================================================================ characters & marks


def arcs_svg(x, y, facing, k):
    """Little 'speaking' sound arcs in front of a mouth (k = 1..3 variants for a gentle flicker)."""
    out = ""
    for i in range(3):
        r = 13 + 13 * i + (k - 2) * 2
        sx, sy = x + facing * r * 0.45, y - r * 0.85
        qx, qy = x + facing * r * 1.2, y
        ex, ey = x + facing * r * 0.45, y + r * 0.85
        out += (f'<path d="M{f1(sx)},{f1(sy)} Q{f1(qx)},{f1(qy)} {f1(ex)},{f1(ey)}" '
                f'fill="none" stroke="{P["ink"]}" stroke-width="5" stroke-linecap="round" opacity="0.85"/>')
    return doc(S.g(out, filter="wobble-fine"))


def exclaim_svg(x, y, s=1.0):
    ink = P["ink"]
    body = (f'<path d="M{x - 9 * s},{y - 70 * s} L{x + 9 * s},{y - 70 * s} L{x + 5 * s},{y - 20 * s} '
            f'L{x - 5 * s},{y - 20 * s} Z" fill="#c9714a" stroke="{ink}" stroke-width="{4 * s}" '
            f'stroke-linejoin="round"/><circle cx="{x}" cy="{y - 4 * s}" r="{8 * s}" fill="#c9714a" '
            f'stroke="{ink}" stroke-width="{4 * s}"/>')
    for a in (-60, -30, 30, 60):
        r0, r1 = 52 * s, 72 * s
        aa = math.radians(a - 90)
        body += (f'<path d="M{f1(x + r0 * math.cos(aa))},{f1(y - 36 * s + r0 * math.sin(aa))} '
                 f'L{f1(x + r1 * math.cos(aa))},{f1(y - 36 * s + r1 * math.sin(aa))}" stroke="{ink}" '
                 f'stroke-width="{4 * s}" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble-fine"))


# crowd: (name, kind, variant, x, y, scale, facing). Scales follow the depth: far 0.55, back 0.66, mid 0.8,
# front 0.95 (the king 1.15 and the messenger 1.1 stand on the raised dais, slightly hierarchical).
CROWD = {
    "far": [("man", 2, 930, 1058, 0.55, 1), ("woman", 0, 985, 1062, 0.55, 1), ("elder", 1, 1038, 1056, 0.55, -1)],
    "back_l": [("man", 0, 1440, 1094, 0.66, 1), ("woman", 1, 1548, 1100, 0.66, -1),
               ("elder", 3, 1765, 1092, 0.66, 1), ("man", 2, 1872, 1098, 0.66, -1)],
    "back_r": [("woman", 3, 1990, 1094, 0.66, 1), ("man", 1, 2096, 1100, 0.66, -1),
               ("elder", 0, 2205, 1096, 0.66, -1)],
    "mid_l": [("elder", 0, 1418, 1216, 0.8, 1), ("woman", 2, 1556, 1208, 0.8, 1)],
    "mid_r": [("man", 3, 1830, 1210, 0.8, -1), ("woman", 0, 1962, 1216, 0.8, 1), ("man", 2, 2092, 1210, 0.8, -1)],
    "front_l": [("woman", 1, 1500, 1344, 0.95, 1), ("man", 1, 1662, 1352, 0.95, 1)],
    "front_r": [("elder", 2, 1975, 1346, 0.95, -1), ("man", 0, 2130, 1350, 0.95, -1)],
}
KIDS = {  # children get their own layers so they can jump for joy
    "kid_mid": ("child", 1, 1692, 1214, 0.8, -1),
    "kid_front": ("child", 2, 1820, 1354, 0.95, -1),
    "kid_back": ("child", 0, 1660, 1098, 0.66, 1),
}


def person(kind, variant, x, y, s, facing, state):
    if state == "stand":
        pose, expr = "sad", None
    elif state == "kneel":
        pose, expr = "kneel_pray", None
    elif state == "joy":
        pose, expr = ("cheer", "happy") if kind == "child" else ("kneel_pray", "happy")
    else:
        raise ValueError(state)
    sh_w = {"stand": 110, "kneel": 170, "joy": 170 if kind != "child" else 100}[state]
    if kind == "child":
        sh_w = 90 if state != "kneel" else 130
    return (C.ground_shadow(x, y, s, sh_w, opacity=0.2)
            + C.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, attire="sackcloth", expr=expr))


def group_frames(members):
    return [doc("".join(person(*m, state=st) for m in members)) for st in ("stand", "kneel", "joy")]


# ============================================================================ light & doves


def rays_svg(src, spread, a_mid, n=9, length=2100, seed=4):
    """Separate soft sunbeams fanning down from src; they start faint at the source (no hard apex)."""
    sx, sy = src
    defs = (f'<radialGradient id="s10ray" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="{length}">'
            f'<stop offset="0" stop-color="#ffe6a0" stop-opacity="0"/>'
            f'<stop offset="0.12" stop-color="#ffe6a0" stop-opacity="0.5"/>'
            f'<stop offset="0.5" stop-color="#ffd27a" stop-opacity="0.24"/>'
            f'<stop offset="1" stop-color="#ffc864" stop-opacity="0"/></radialGradient>')
    rng = random.Random(seed)
    d = ""
    for i in range(n):
        a = math.radians(a_mid - spread / 2 + spread * i / (n - 1) + rng.uniform(-2.0, 2.0))
        wa = math.radians(rng.uniform(1.3, 2.5))
        r0, r1 = 40, length * rng.uniform(0.72, 1.0)
        pts = [(sx + r0 * math.cos(a - wa / 4), sy + r0 * math.sin(a - wa / 4)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 4), sy + r0 * math.sin(a + wa / 4))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    return doc(f'<path d="{d}" fill="url(#s10ray)" filter="url(#blur-md)"/>', defs)


def gleam_svg(cx, cy, rx, ry):
    """Warm golden light behind the parting cloud (normal blend, drawn above the cool gloom glaze)."""
    defs = S.rad_grad("s10gleam", [(0, "#ffeeb4", 1), (0.4, "#ffde92", 0.92), (0.72, "#ffd27c", 0.5),
                                   (1, "#ffc864", 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#s10gleam)"/>', defs)


def glaze_svg(warm):
    """Full-frame multiply glaze: cool gloom under the cloud, or a light warm gold for God's mercy."""
    if warm:
        stops = [(0, "#ffdcaa", 0.1), (0.4, "#ffe2b0", 0.15), (1, "#ffdcaa", 0.18)]
    else:
        stops = [(0, "#8d90ad", 0.62), (0.38, "#9a9cb6", 0.5), (0.68, "#a9a8bc", 0.3), (1, "#b4b1c0", 0.2)]
    defs = S.lin_grad("s10glaze", stops)
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s10glaze)"/>', defs)


# grey cloud banks: (fill, underside) dark = the old colours already multiplied by the gloom glaze they now sit
# above; lit = the same clouds catching the warm light as they part
CLOUD_DARK = {"back": ("#666a82", "#51546c"), "front": ("#5e627a", "#4a4d64"), "low": ("#5b5f77", "#474a61")}
CLOUD_LIT = {"back": ("#b0a2aa", "#94868f"), "front": ("#aa9ca5", "#8d7f8b"), "low": ("#a6989f", "#8a7c86")}


def bank_frames(items, kind, rect=None):
    out = []
    for fill, shade in (CLOUD_DARK[kind], CLOUD_LIT[kind]):
        extra = ""
        if rect:
            x0, x1, y1 = rect
            extra = f'<rect x="{x0}" y="-40" width="{x1 - x0}" height="{y1 + 40}" fill="{fill}"/>'
        out.append(cloud_bank_svg(items, fill, shade, extra=extra))
    return out


DOVE_REF = (300, 300)
WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)


def dove_frames(facing):
    return [doc(PR.dove(DOVE_REF[0], DOVE_REF[1], 0.85, facing, wing=w)) for w in WINGS]


def wing_cycle(rate, phase, glide_from=None):
    seq = (0, 1, 2, 3, 4, 3, 2, 1)

    def fa(t):
        if glide_from is not None and t > glide_from and int((t - glide_from) * 1.3) % 3 == 1:
            return 2.0
        return float(seq[int(t * rate + phase * 8) % 8])
    return fa


def flight(pts, ref):
    """Smooth flight path through [(t, x, y)] (Catmull-Rom in time; keeps gliding, never hovers at a key)."""
    n = len(pts)

    def P(i):
        if 0 <= i < n:
            return pts[i]
        a, b = (pts[0], pts[1]) if i < 0 else (pts[-1], pts[-2])
        return (2 * a[0] - b[0], 2 * a[1] - b[1], 2 * a[2] - b[2])

    def m(t):
        if t <= pts[0][0]:
            x, y = pts[0][1], pts[0][2]
        elif t >= pts[-1][0]:
            x, y = pts[-1][1], pts[-1][2]
        else:
            i = max(k for k in range(n - 1) if pts[k][0] <= t)
            p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
            u = (t - p1[0]) / (p2[0] - p1[0])
            u2, u3 = u * u, u * u * u
            x, y = (0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2
                           + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in (1, 2))
        return Tf(dx=x - ref[0], dy=y - ref[1])
    return m


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    l0, l1, l2, l3 = L[0], L[1], L[2], L[3]

    # ---- timing (all derived from the narration) ----
    t_surprise = l0.start + 0.45
    t_point = l0.start + 0.85
    t_rise = l0.start + 1.25
    t_crown = l0.start + 2.1
    t_sack = l1.start - 0.12          # "都穿上麻衣": robe off, sackcloth on
    t_turn = t_sack - 0.4             # he turns to the throne, crown in his hands
    t_land = t_sack + 0.48            # robe + crown land on the throne seat
    t_msg_kneel = l1.start + 0.25
    t_far_kneel = l1.start + 0.4
    t_ash = l1.start + 0.4
    t_sit = l1.start + 0.7
    t_pull0, t_pull1 = l1.start + 0.55, l1.end + 0.45
    t_wave0 = l1.start + 0.85         # people kneel in a wave across the square
    s0 = t_mercy = l2.start           # chime: God sees them; the cloud parts
    t_gold0, t_gold1 = l2.start + 0.4, l2.start + 2.7
    t_joy0 = l2.end - 0.55            # people look up with relief and joy
    t_kjoy = l2.end - 0.3

    # ---- sky ----
    sc.add("sky_grey", sky_grey_svg(), z=0, wc=0.5,       # hidden (skipped) once the gold sky is fully in
           motion=lambda t: Tf(alpha=1.0 if t < t_gold1 + 0.05 else 0.0))
    sc.add("sky_gold", sky_gold_svg(), z=1, wc=0.6,
           motion=M.keys([(t_gold0, {"alpha": 0}), (t_gold1, {"alpha": 1})], "sine"))
    # fair-weather clouds come in only after the grey banks in front of them have gone (no show-through)
    sc.add("fair", fair_clouds_svg(), z=1.5, motion=M.combine(
        M.keys([(l2.start + 2.3, {"alpha": 0}), (l2.start + 3.4, {"alpha": 1})], "sine"), M.drift(vx=4, t0=t_gold0)))

    # ---- city & square (static) ----
    sc.add("city", city_svg(), z=8)

    # ---- animals in sackcloth ----
    def animal_layer(name, kind, x, y, s, facing, z, hop_t=None, per=2.8, ph=0.0):
        body = C.ground_shadow(x, y, s, 260 if kind in ("camel", "cow") else 200, opacity=0.2)
        body += PR.animal(x, y, s, facing, kind=kind, sackcloth=True)
        parts = [M.breathe(0.012, per, pivot=(x, y), phase=ph)]
        if hop_t is not None:
            parts.append(M.keys([(hop_t, {"dy": 0}), (hop_t + 0.16, {"dy": -22 * s}), (hop_t + 0.34, {"dy": 0}),
                                 (hop_t + 0.5, {"dy": -12 * s}), (hop_t + 0.64, {"dy": 0})],
                                ["out", "in", "out", "in"]))
        sc.add(name, doc(body), z=z, motion=M.combine(*parts))

    animal_layer("camel", "camel", 2560, 1118, 0.6, -1, 9.0, per=3.6)
    animal_layer("cow", "cow", 2425, 1100, 0.5, -1, 8.9, per=3.1, ph=0.3)
    animal_layer("donkey", "donkey", 2282, 1236, 0.6, -1, 13.0, per=2.9, ph=0.5)
    animal_layer("goat", "goat", 2600, 1352, 0.6, -1, 16.0, hop_t=t_joy0 + 0.5, per=2.5, ph=0.2)
    animal_layer("sheep", "sheep", 2365, 1400, 0.72, -1, 17.0, hop_t=t_joy0 + 0.25, per=2.3, ph=0.7)
    animal_layer("lamb", "sheep", 2490, 1432, 0.46, -1, 17.5, hop_t=t_joy0 + 0.75, per=2.0, ph=0.1)

    # ---- the crowd in sackcloth: stand -> kneel is a near-cut at the bottom of a dip, kneel -> joy is only the
    # expression (soft crossfade) ----
    wave = {"far": t_far_kneel, "mid_l": t_wave0, "front_l": t_wave0 + 0.15, "back_l": t_wave0 + 0.3,
            "mid_r": t_wave0 + 0.55, "front_r": t_wave0 + 0.7, "back_r": t_wave0 + 0.85}
    joy = {"far": t_joy0 + 0.2, "front_l": t_joy0, "mid_l": t_joy0 + 0.15, "back_l": t_joy0 + 0.35,
           "front_r": t_joy0 + 0.25, "mid_r": t_joy0 + 0.45, "back_r": t_joy0 + 0.6}
    zrow = {"far": 8.5, "back_l": 10, "back_r": 10.2, "mid_l": 12, "mid_r": 12.2, "front_l": 15, "front_r": 15.2}

    def kneel_dip(tk, s, pv):
        return hop(tk, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": 9 * s, "sy": 0.95}),
                        (0.12, {"dy": -2 * s, "sy": 1.01}), (0.26, {"dy": 0, "sy": 1})], pv, ["in", "out", "sine"])

    for name, members in CROWD.items():
        frames = group_frames(members)
        xs = [m[2] for m in members]
        gx, gy = sum(xs) / len(xs), max(m[3] for m in members)
        s = members[0][4]
        tk, tj = wave[name], joy[name]
        sc.add(f"crowd_{name}", frames, z=zrow[name],
               frame_at=sched([(0, 0), (tk, 1), (tj, 2, 0.26)]),
               motion=M.combine(kneel_dip(tk, s, (gx, gy)),
                                hop(tj, [(0, {"dy": 0}), (0.18, {"dy": -6 * s}), (0.4, {"dy": 0})], (gx, gy)),
                                M.breathe(0.008, 3.4, pivot=(gx, gy), phase=len(name) * 0.13)))

    kid_wave = {"kid_mid": t_wave0 + 0.4, "kid_front": t_wave0 + 0.5, "kid_back": t_wave0 + 0.95}
    kid_joy = {"kid_mid": t_joy0 + 0.3, "kid_front": t_joy0 + 0.1, "kid_back": t_joy0 + 0.5}
    kz = {"kid_mid": 12.1, "kid_front": 15.1, "kid_back": 10.1}
    for name, m in KIDS.items():
        frames = [doc(person(*m, state=st)) for st in ("stand", "kneel", "joy")]
        tk, tj = kid_wave[name], kid_joy[name]
        s, pv = m[4], (m[2], m[3])
        # kneel -> cheer is a real pose change: crouch, swap at the bottom, spring up, then two more joy hops
        jumps = hop(tj, [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 7 * s, "sy": 0.94}),
                         (0.18, {"dy": -32 * s, "sy": 1.03}),
                         (0.36, {"dy": 0, "sy": 1}), (0.7, {"dy": 0}), (0.88, {"dy": -24 * s}), (1.06, {"dy": 0}),
                         (1.5, {"dy": 0}), (1.66, {"dy": -16 * s}), (1.82, {"dy": 0})],
                    pv, ["in", "out", "in", "linear", "out", "in", "linear", "out", "in"])
        sc.add(name, frames, z=kz[name], frame_at=sched([(0, 0), (tk, 1), (tj, 2)]),
               motion=M.combine(kneel_dip(tk, s, pv), jumps, M.breathe(0.012, 2.6, pivot=pv)))

    # ---- palace ----
    sc.add("palace", palace_svg(), z=8.2)      # same static group as the city (flattened once)
    sc.add("throne", throne_svg(), z=8.3)

    # king on the throne: leans forward and squashes (anticipation), then near-cuts to standing
    pv_seat = (THRONE_X, THRONE_Y)
    seat = [doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False)),
            doc(C.king(THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False, expr="surprised"))]
    sc.add("king_seat", seat, z=23, frame_at=sched([(0, 0), (t_surprise, 1, 0.25)]),
           motion=M.combine(
               hop(t_rise, [(-0.24, {"sy": 1, "rot": 0, "alpha": 1}), (0, {"sy": 0.95, "rot": 3, "alpha": 1}),
                            (CUT, {"sy": 0.95, "rot": 3, "alpha": 0})], pv_seat, ["inout", "linear"]),
               M.breathe(0.008, 3.2, pivot=pv_seat)))

    # ashes (a heap grows just before he sits down in it)
    ax = SPOT_X + PR.KING_ASH_DX * KS
    ash_in = M.keys([(t_ash, {"alpha": 0, "sx": 0.8, "sy": 0.5}), (t_ash + 0.35, {"alpha": 1, "sx": 1, "sy": 1})],
                    "out", pivot=(ax, SPOT_Y))
    sc.add("ash_back", doc(ash_heap(ax, SPOT_Y, KS, "back")), z=24, motion=ash_in)
    sc.add("ash_front", doc(ash_heap(ax, SPOT_Y, KS, "front")), z=26, motion=ash_in)

    # the king: stands up just in front of the throne, walks forward, takes off his crown, turns to the throne,
    # changes into sackcloth (puff), sits in the ashes, and at the end gets up onto his knees with joy
    kp = (SPOT_X, SPOT_Y)
    ksh = C.ground_shadow(SPOT_X, SPOT_Y, KS, 130)
    king = [doc(ksh + C.king(SPOT_X, SPOT_Y, KS, 1, pose="stand", expr="worried")),
            doc(ksh + C.king(SPOT_X, SPOT_Y, KS, 1, pose="remove_crown")),
            doc(ksh + C.king(SPOT_X, SPOT_Y, KS, -1, pose="remove_crown")),
            doc(ksh + C.king(SPOT_X, SPOT_Y, KS, -1, pose="stand", attire="sackcloth")),
            doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="sit_ashes", ashes=False)),
            doc(C.king(SPOT_X, SPOT_Y, KS, 1, pose="kneel_pray", attire="sackcloth", expr="happy"))]
    t_w0, step = t_rise + 0.14, 0.15
    bob_keys = [(0, {"dy": 0, "rot": 0})]
    for i in range(4):
        bob_keys += [(i * step + step / 2, {"dy": -7, "rot": 1.6 * (1 if i % 2 else -1)}),
                     ((i + 1) * step, {"dy": 0, "rot": 0})]
    sc.add("king", king, z=25,
           frame_at=sched([(0, 0), (t_crown, 1), (t_turn, 2), (t_sack, 3), (t_sit, 4), (t_kjoy, 5)]),
           motion=M.combine(
               M.keys([(t_rise, {"alpha": 0}), (t_rise + CUT, {"alpha": 1})], "linear", pivot=kp),
               M.keys([(t_w0, {"dx": RISE_X - SPOT_X}), (t_w0 + 4 * step, {"dx": 0})], "inout", pivot=kp),
               hop(t_w0, bob_keys, kp),
               hop(t_rise, [(0, {"sy": 1.05}), (0.14, {"sy": 0.98}), (0.26, {"sy": 1.0})], kp),
               hop(t_crown, [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 10, "sy": 0.97}), (0.16, {"dy": -4, "sy": 1.01}),
                             (0.3, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               hop(t_turn, [(-0.1, {"dy": 0}), (0, {"dy": 6}), (0.2, {"dy": 0})], kp),
               hop(t_sack, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5, "sy": 0.96}), (0.12, {"dy": -3, "sy": 1.02}),
                            (0.26, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               hop(t_sit, [(-0.2, {"dy": 0, "sy": 1}), (0, {"dy": 14, "sy": 0.93}), (0.1, {"dy": -3, "sy": 1.03}),
                           (0.25, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               hop(t_kjoy, [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 6, "sy": 0.97}), (0.15, {"dy": -10, "sy": 1.02}),
                            (0.32, {"dy": 0, "sy": 1})], kp, ["in", "out", "sine"]),
               M.breathe(0.008, 3.0, pivot=kp, phase=0.3)))

    # quick-change puff over the robe swap
    pk = (SPOT_X - 6, SPOT_Y - 190)
    sc.add("puff_king", puff_svg(pk[0], pk[1], 118, 178, seed=3, k=1.1), z=26.5, wc=0.5,
           motion=hop(t_sack, [(-0.06, {"alpha": 0, "s": 0.8, "dy": 0}), (0.02, {"alpha": 1, "s": 0.97, "dy": -4}),
                               (0.14, {"alpha": 0.85, "s": 1.06, "dy": -12}),
                               (0.32, {"alpha": 0, "s": 1.14, "dy": -24})],
                      pk, ["out", "sine", "in"]))

    # the folded robe with the crown on top arcs from his hands onto the throne seat ("laid his robe from him")
    hands = C.body_points(C.king, SPOT_X, SPOT_Y, KS, -1, pose="remove_crown")["hands"]
    hx, hy = (hands[0][0] + hands[1][0]) / 2, (hands[0][1] + hands[1][1]) / 2
    dx0, dy0 = hx + 6 - BUNDLE_X, hy + 62 - BUNDLE_Y
    bp = (BUNDLE_X, BUNDLE_Y)
    sc.add("bundle", bundle_svg(), z=27, motion=M.combine(
        M.keys([(t_sack - 0.01, {"alpha": 0, "dx": dx0, "s": 0.9}), (t_sack + 0.02, {"alpha": 1}),
                (t_land, {"dx": 0, "s": 1.0})], ["linear", "sine"], pivot=bp),
        M.keys([(t_sack, {"dy": dy0}), (t_sack + 0.22, {"dy": min(dy0, 0) - 75}), (t_land, {"dy": 0})], ["out", "in"],
               pivot=bp),
        M.keys([(t_sack, {"rot": 12}), (t_sack + 0.26, {"rot": -8}), (t_land, {"rot": 0}), (t_land + 0.1, {"rot": 3}),
                (t_land + 0.22, {"rot": 0})], "sine", pivot=bp),
        hop(t_land, [(0, {"sx": 1, "sy": 1}), (0.07, {"sx": 1.06, "sy": 0.88}), (0.2, {"sx": 1, "sy": 1})], bp)))

    # "!" when the king hears the news
    kh = C.body_points(C.king, THRONE_X, THRONE_Y, KS, 1, pose="sit_throne", throne=False)["head_top"]
    ex, ey = kh[0] + 128, kh[1] + 44
    sc.add("wow", exclaim_svg(ex, ey, 1.2), z=27, wc=0,
           motion=M.keys([(t_surprise - 0.05, {"alpha": 0, "s": 0.4}), (t_surprise + 0.25, {"alpha": 1, "s": 1}),
                          (t_rise - 0.1, {"alpha": 1}), (t_rise + 0.12, {"alpha": 0})],
                         ["back", "linear", "sine"], pivot=(ex, ey)))

    # the messenger: tells the king, points to the city, then kneels in sackcloth too
    def msg(**kw):
        return (C.ground_shadow(MSG_X, MSG_Y, MSG_S, 120)
                + C.citizen(MSG_X, MSG_Y, MSG_S, kind="man", variant=MSG_V, **kw))
    mframes = [doc(msg(facing=-1, pose="stand", expr="call")),
               doc(msg(facing=1, pose="point", expr="worried")),
               doc(msg(facing=-1, pose="kneel_pray", attire="sackcloth")),
               doc(msg(facing=-1, pose="kneel_pray", attire="sackcloth", expr="happy"))]
    mp = (MSG_X, MSG_Y)
    sc.add("messenger", mframes, z=28,
           frame_at=sched([(0, 0), (t_point, 1), (t_msg_kneel, 2), (t_joy0 + 0.1, 3, 0.3)]),
           motion=M.combine(
               hop(t_point, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 6, "sy": 0.97}), (0.18, {"dy": 0, "sy": 1})], mp),
               kneel_dip(t_msg_kneel, 1.1, mp),
               hop(t_joy0 + 0.1, [(0, {"dy": 0}), (0.18, {"dy": -6}), (0.4, {"dy": 0})], mp),
               M.breathe(0.01, 2.8, pivot=mp, phase=0.6)))
    pm = (MSG_X + 6, MSG_Y - 165)
    sc.add("puff_msg", puff_svg(pm[0], pm[1], 96, 150, seed=8, k=0.95), z=28.5, wc=0.5,
           motion=hop(t_msg_kneel, [(-0.06, {"alpha": 0, "s": 0.8, "dy": 0}), (0.02, {"alpha": 1, "s": 0.97, "dy": -4}),
                                    (0.14, {"alpha": 0.85, "s": 1.06, "dy": -10}),
                                    (0.32, {"alpha": 0, "s": 1.14, "dy": -20})],
                      pm, ["out", "sine", "in"]))
    mh = C.body_points(C.citizen, MSG_X, MSG_Y, MSG_S, -1, kind="man", variant=MSG_V, pose="stand")["head"]
    sc.add("arcs", [arcs_svg(mh[0] - 58, mh[1] + 30, -1, k) for k in (1, 2, 3)], z=29, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(0, {"alpha": 1}), (t_point - 0.2, {"alpha": 1}), (t_point, {"alpha": 0})], "sine"))

    # ---- foreground details framing the wide shot (static) ----
    fgb = (PR.bush(2760, SH - 2, 1.0, variant=1) + PR.jar(2600, SH - 62, 0.85) + PR.jar(2672, SH - 34, 0.62)
           + PR.grass_tuft(2515, SH - 6, 1.1, variant=2) + PR.grass_tuft(1420, SH + 6, 0.9, variant=0)
           + PR.grass_tuft(1340, DAIS_BOTTOM + 30, 0.8, variant=2) + PR.grass_tuft(40, SH + 8, 1.0, variant=0))
    sc.add("foreground", doc(fgb), z=8.4)

    # ---- doves rise from behind the rooftops (below the city layer, so the houses hide their take-off, and
    # below the warm glaze so they share the light) ----
    fr_l, fr_r = dove_frames(-1), dove_frames(1)
    doves = [  # (facing, [(t, x, y)], wing rate, phase)
        (-1, [(t_gold0 + 1.3, 2900, 640), (t_joy0 + 0.6, 2240, 380), (T, 1620, 250)], 11, 0.0),
        (-1, [(t_gold0 + 1.6, 2930, 520), (t_joy0 + 0.9, 2380, 300), (T, 1900, 190)], 12, 0.4),
        (1, [(t_joy0 + 0.1, 2150, 800), (t_joy0 + 1.0, 2300, 470), (T, 2620, 330)], 13, 0.2),
        (-1, [(t_joy0 + 0.3, 1810, 910), (t_joy0 + 1.2, 1640, 520), (T, 1390, 330)], 12, 0.7),
        (-1, [(t_joy0 + 0.5, 2470, 880), (t_joy0 + 1.4, 2300, 640), (T, 2050, 470)], 11.5, 0.5),
    ]
    for i, (fc, pts, rate, ph) in enumerate(doves):
        ta = pts[0][0]
        sc.add(f"dove{i}", fr_l if fc < 0 else fr_r, z=7.5 + 0.01 * i, seed=900 if fc < 0 else 901,
               frame_at=wing_cycle(rate, ph, glide_from=T - 2.0),
               motion=M.combine(flight(pts, DOVE_REF),
                                M.keys([(ta - 0.01, {"alpha": 0, "s": 0.7}), (ta + 0.2, {"alpha": 1, "s": 1.0})],
                                       "out", pivot=DOVE_REF),
                                M.bob(8, 0.9, phase=ph, axis="y")))

    # ---- gloom (lifts from the moment God sees them) ----
    sc.add("gloom", glaze_svg(False), z=40, wc=0, blend="multiply",
           motion=M.keys([(t_mercy, {"alpha": 1}), (t_gold1 + 0.4, {"alpha": 0})], "sine"))

    # ---- golden light behind the parting cloud: above the gloom, below the banks, so it shows warm in the gap
    sc.add("gleam", gleam_svg(GAP_X, 150, 250, 330), z=40.1, wc=0, motion=M.combine(
        M.keys([(s0 - 0.05, {"alpha": 0, "sx": 0.5, "sy": 0.7}), (s0 + 0.7, {"alpha": 1, "sx": 1.0, "sy": 1.0}),
                (t_gold1 - 0.3, {"alpha": 1, "sx": 1.5, "sy": 1.25}),
                (t_gold1 + 0.6, {"alpha": 0, "sx": 1.7, "sy": 1.3})],
               ["out", "sine", "sine"], pivot=(GAP_X, 0)),
        M.pulse(0.9, 1.0, 2.6)))

    # ---- the heavy grey cloud: parts in the middle, banks move clear of each other, then fade (back first) ----
    lit = lambda t: M.progress(t, s0 + 0.15, s0 + 1.7, "sine")

    def cloud_motion(part_dx, go_dx, go_dy, t_go1, fade0, fade1, drift, pivot, s1=1.06, part_dy=0):
        return M.combine(
            M.keys([(s0, {"dx": 0, "dy": 0, "s": 1.0}), (s0 + 0.55, {"dx": part_dx, "dy": part_dy, "s": 1.0}),
                    (t_go1, {"dx": go_dx, "dy": go_dy, "s": s1})], ["out", "sine"], pivot=pivot),
            M.keys([(fade0, {"alpha": 1}), (fade1, {"alpha": 0})], "sine"),
            M.drift(vx=drift))

    sc.add("cloud_l", bank_frames([(180, 35, 900, 330, 41), (820, -5, 820, 300, 42)], "back", (-40, 1260, 80)),
           z=40.2, frame_at=lit,
           motion=cloud_motion(-20, -380, -170, s0 + 2.0, s0 + 1.1, s0 + 1.9, -4, (500, 40)))
    sc.add("cloud_low_l", bank_frames([(1720, 345, 560, 190, 47)], "low"), z=40.3, frame_at=lit,
           motion=cloud_motion(-30, -110, -125, s0 + 2.3, s0 + 1.5, s0 + 2.25, -3, (1720, 380), 1.04, -15))
    sc.add("cloud_low_r", bank_frames([(2380, 340, 640, 200, 48), (2800, 330, 420, 180, 49)], "low"), z=40.31,
           frame_at=lit, motion=cloud_motion(45, 280, -100, s0 + 2.3, s0 + 1.5, s0 + 2.25, 6, (2380, 380), 1.04, -10))
    sc.add("cloud_cl", bank_frames([(1390, 20, 1000, 360, 43)], "front", (880, 1850, 80)), z=40.4, frame_at=lit,
           motion=cloud_motion(-95, -480, -170, s0 + 3.0, s0 + 2.1, s0 + 2.95, -3, (1390, 40)))
    sc.add("cloud_cr", bank_frames([(2470, 70, 900, 330, 44)], "front", (2080, 2900, 90)), z=40.41, frame_at=lit,
           motion=cloud_motion(95, 480, -150, s0 + 3.0, s0 + 2.1, s0 + 2.95, 5, (2470, 70)))

    # ---- warm light of God's mercy ----
    sc.add("warm", glaze_svg(True), z=40.6, wc=0, blend="multiply",
           motion=M.keys([(t_gold0, {"alpha": 0}), (t_gold1 + 0.4, {"alpha": 1})], "sine"))
    rsrc = (GAP_X, 120)
    sc.add("rays", rays_svg(rsrc, 72, 98, n=9, length=1650), z=41, wc=0, blend="add",
           motion=M.combine(M.keys([(s0 + 0.15, {"alpha": 0, "sx": 0.45, "sy": 0.35}), (s0 + 1.0, {"alpha": 1}),
                                    (t_gold1, {"sx": 1.0, "sy": 1.0}), (t_gold1 + 1.2, {"alpha": 0.75})],
                                   ["sine", "out", "sine"], pivot=rsrc),
                            M.pulse(0.8, 1.0, 3.2), M.sway(1.2, 7.0, rsrc)))

    # ---- camera: on the king, then wide on the city ----
    sc.camera = M.cam_keys([
        (0, Cam(790, 1010, 1540)),
        (t_pull0, Cam(800, 1016, 1500)),
        (t_pull1, Cam(1400, 787.5, 2800)),
        (T, Cam(1432, 800, 2715)),
    ], ["sine", "inout", "sine"])

    # ---- effects ----
    sc.fx = [
        FX.sparkles((1250, 300, 2750, 1150), count=30, t0=t_gold0 + 0.8, t1=T + 1, color=(255, 238, 172),
                    size=(9, 20), drift=-10, seed=23),
        FX.motes((1100, 200, 2800, 1300), count=36, t0=t_gold0 + 0.5, t1=T + 1, color=(255, 240, 200),
                 size=(3, 7), alpha=140, seed=29),
    ]

    # ---- sound ----
    sc.sfx("crowd", 0, dur=T + 0.8, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_sack, gain_db=-8)
    sc.sfx("chime", t_mercy, gain_db=-8)
    sc.sfx("sparkle", t_gold0 + 0.8, gain_db=-12)
    sc.sfx("birds", t_gold0 + 1.3, dur=T - t_gold0 - 1.3 + 0.8, gain_db=-12, fade_in=1.0, fade_out=0.8)
    sc.sfx("sheep", t_joy0 + 0.25, gain_db=-12, pan=0.5)
    return sc
