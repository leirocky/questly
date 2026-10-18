"""Scene 2 — Daniel in Babylon; King Darius, his 120 officials and the three overseers (Daniel 6:1-3).

One wide 5300 x 1440 stage, no cuts. On the left a palace roof terrace above Babylon (the blue Ishtar gate, the
great ziggurat, flat roofs and date palms in the morning haze); a massive pier with a drawn-back curtain; then
King Darius's audience hall (shared with s03 and s04, see the HALL section): cedar ceiling beams, a blue glazed
frieze of friendly walking lions, the record shelves, tall Persian bull-capital columns, a red runner, and the
throne on its dais under a fringed canopy with two palace guards.

  line 0  "很久很久以前，有一个人，"     calm city establishing frame; Daniel walks in along the terrace (planted-foot
                                        strides) and stops
          "名叫但以理。"                he turns to us and greets with an open hand (cut on a dip), happy
          "他是以色列人，住在很远的巴比伦。"  he points out over the great city; the camera drifts toward the ziggurat
  line 1  "但以理很爱上帝，每天都向上帝祷告。"  he turns west (toward far-away Jerusalem), half-kneels and kneels to
                                        pray; warm light rays fall on him from the morning sky (God = light only),
                                        a few sparkles in the sky (never on his face); chime
  line 2  "大利乌王管理着一个很大的国家。"  the camera glides right past the curtain pier into the hall and settles on
                                        King Darius on his throne (he nods and smiles)
          "他派了一百二十个官员，"        the camera widens; three rows of officials pop up, row by row (pop sfx)
          "又派了三个总管，来管理这些官员。"  three overseers (Daniel in the middle of the group) step out of the
                                        front row and walk to the throne (planted-foot strides), the camera follows
  line 3  "但以理就是三个总管中的一个。"  the camera pushes in; Daniel bows; the other two glance at him
          "他做事又认真，又诚实，"        Daniel unrolls a scroll and reads it attentively (cloth sfx)
          "国王很喜欢他，"                the king smiles happily; three little hearts float up beside him (not on faces)
          "想让他管理整个国家。"          the king opens his hand toward Daniel (in-between drawing, dip); Daniel bows
  end     calm medium shot: the king, Daniel reading, the two other overseers; s03 opens on this same framing.

Pose changes are hard cuts hidden in a small squash (dip) or a cloth puff; walking uses s17's planted-foot
step_walk. All times derive from the narration chunks.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import (arcs_markup, cuts, dip, happy_hop, hop, nod, snap, step_walk, trap)
from art.scenes_v1.s10_repent import rosettes
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 5300, 1440
INK = P["ink"]

# ============================================================================ shared hall geometry (s02-s04)
HX0 = 2300                       # stage x of hall x = 0 (the inner face of the curtain pier)
WALL_BOT = 1040                  # back wall meets the floor
CEIL = 150                       # underside of the ceiling beams
DAIS = (80, 680, 1158, 1246)     # hall x0, x1, top surface y, bottom of its front face
THRONE_HX, THRONE_Y = 330, 1160  # the king's anchor (on the dais)
KS = 1.0                         # king scale
FLOOR_Y = 1262                   # where the overseers / officials stand in front of the throne
COL_FRONT = (1400, 2720)         # free-standing columns near the camera (hall x), base y COL_BASE
COL_BASE = 1318
SHELF = (1700, 2230, 520, 958)   # record shelves in the back wall (hall x0, x1, top, bottom)
TABLE_HX, TABLE_Y = 2150, 1196   # the records table (s03 / s04 only), base on the floor
GUARDS = ((96, 1150, 0), (636, 1150, 2))    # (hall x, ground y, variant) beside the dais

WALL_A, WALL_B = "#e8d1a6", "#d7b885"
BLUE, BLUE_DARK, GOLD = "#3f79a8", "#2f5f8a", P["crown"]
CEDAR, CEDAR_DARK = "#8b5a37", "#62402a"


def hx(v):
    return HX0 + v


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def chunk(line, phrase):
    return next(c for c in line.chunks if phrase in c.text)


def clamp_cam(c, margin=4, sw=SW, sh=SH):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), sw - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), sh - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys, sw=SW, sh=SH):
    """keys [(t, Cam, bump[, curve])]: eased moves between key cameras (clamped to the stage). The viewport's
    BOTTOM edge is interpolated (not its centre) and ``bump`` widens the view in the middle of a move (sin^2, zero
    zoom speed at both ends) — the same scheme as s17's cam_path, for this stage size."""
    keys = sorted([(k[0], clamp_cam(k[1], sw=sw, sh=sh), k[2], k[3] if len(k) > 3 else "sine") for k in keys],
                  key=lambda k: k[0])

    def bottom(c):
        return c.y + c.w * 9 / 32

    def c(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, bump, curve), (t1, b, _, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, curve)
                v = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
                w = M.lerp(a.w, b.w, u) + bump * math.sin(math.pi * v) ** 2
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w), sw=sw, sh=sh)
        return keys[-1][1]
    return c


def bcam(x, w, bottom=SH - 4):
    """Camera of width w centred on x whose bottom edge sits at ``bottom``."""
    return Cam(x, bottom - w * 9 / 32, w)


# ---------------------------------------------------------------------------- hall drawings


def _beams(x0, x1):
    out = (f'<rect x="{x0}" y="-20" width="{x1 - x0}" height="{CEIL - 22}" fill="{CEDAR}" stroke="{INK}" '
           f'stroke-width="4"/>')
    out += f'<path d="M{x0},{CEIL - 70} L{x1},{CEIL - 70}" stroke="{CEDAR_DARK}" stroke-width="5" opacity="0.7"/>'
    for x in range(x0 + 30, x1, 128):        # round beam ends poking out of the wall
        out += (f'<rect x="{x}" y="{CEIL - 46}" width="74" height="54" rx="14" fill="#a06c44" stroke="{INK}" '
                f'stroke-width="4"/><circle cx="{x + 37}" cy="{CEIL - 19}" r="13" fill="none" stroke="{CEDAR_DARK}" '
                f'stroke-width="3" opacity="0.7"/>')
    out += (f'<rect x="{x0}" y="{CEIL + 8}" width="{x1 - x0}" height="70" fill="url(#hshadow)" opacity="0.55"/>')
    return out


def _frieze(x0, x1, y0=212, y1=338):
    """Blue glazed brick band with friendly lions walking toward the throne (the Ishtar-gate lions)."""
    out = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{BLUE}" stroke="{INK}" '
           f'stroke-width="4"/>')
    bricks = ""
    for y in range(y0 + 24, y1, 24):
        bricks += f'<path d="M{x0},{y} L{x1},{y}"/>'
    out += f'<g stroke="{BLUE_DARK}" stroke-width="2" opacity="0.5" fill="none">{bricks}</g>'
    out += (f'<rect x="{x0}" y="{y0 - 34}" width="{x1 - x0}" height="30" fill="{BLUE_DARK}" stroke="{INK}" '
            f'stroke-width="3.5"/>' + rosettes(x0 + 30, x1, y0 - 19, 62, 12, fill="#f3e6c8", centre=GOLD))
    out += (f'<rect x="{x0}" y="{y1 + 4}" width="{x1 - x0}" height="30" fill="{BLUE_DARK}" stroke="{INK}" '
            f'stroke-width="3.5"/>' + rosettes(x0 + 60, x1, y1 + 19, 62, 12, fill="#f3e6c8", centre=GOLD))
    lions = ""
    for i, x in enumerate(range(x0 + 170, x1 - 60, 330)):
        lions += PR.lion(x, y1 - 12, 0.29, -1, pose="walk_a" if i % 2 else "walk_b", tail=0.4)
    return out + lions


def _pilaster(cx, top, bottom, w=86):
    out = (f'<rect x="{cx - w / 2}" y="{top}" width="{w}" height="{bottom - top}" fill="#e9d8b6" stroke="{INK}" '
           f'stroke-width="4"/>')
    for k in (1, 2, 3):
        x = cx - w / 2 + w * k / 4
        out += f'<path d="M{f1(x)},{top + 40} L{f1(x)},{bottom - 30}" stroke="#c9ad80" stroke-width="3"/>'
    out += (f'<rect x="{cx - w / 2 - 14}" y="{top - 4}" width="{w + 28}" height="34" rx="8" fill="#efdfbf" '
            f'stroke="{INK}" stroke-width="4"/><rect x="{cx - w / 2 - 10}" y="{top + 30}" width="{w + 20}" '
            f'height="14" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{cx - w / 2 - 14}" y="{bottom - 30}" width="{w + 28}" height="30" rx="6" fill="#efdfbf" '
            f'stroke="{INK}" stroke-width="4"/>')
    return out


def _window(cx, top, bottom, w=150):
    """Tall clerestory window with a stepped frame and bright sky (the sun shafts are a separate layer)."""
    out = ""
    for k, col in ((34, "#c9ad80"), (18, "#e2cba2")):
        out += (f'<rect x="{cx - w / 2 - k}" y="{top - k}" width="{w + 2 * k}" height="{bottom - top + 2 * k}" '
                f'fill="{col}" stroke="{INK}" stroke-width="3.5"/>')
    out += (f'<rect x="{cx - w / 2}" y="{top}" width="{w}" height="{bottom - top}" fill="url(#hwin)" '
            f'stroke="{INK}" stroke-width="4"/>')
    out += S.cloud(cx + 10, top + 90, 120, 44, "#fff8ea", seed=int(cx) % 97, puffs=3, sw=2.5)
    for k in range(1, 3):        # wooden lattice bars
        x = cx - w / 2 + w * k / 3
        out += f'<path d="M{f1(x)},{top} L{f1(x)},{bottom}" stroke="{CEDAR}" stroke-width="7"/>'
    out += (f'<rect x="{cx - w / 2 - 40}" y="{bottom + 34}" width="{w + 80}" height="22" rx="6" fill="#efdfbf" '
            f'stroke="{INK}" stroke-width="3.5"/>')
    return out


def _shelves(x0, x1, top, bot):
    """Record room shelves in a deep wall niche: rolled scrolls (end-on) and clay tablets."""
    rng = random.Random(5)
    out = (f'<rect x="{x0 - 26}" y="{top - 26}" width="{x1 - x0 + 52}" height="{bot - top + 26}" fill="#c9ad80" '
           f'stroke="{INK}" stroke-width="4"/>'
           f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" fill="#6e4a32" stroke="{INK}" '
           f'stroke-width="4"/>')
    rows = 4
    hrow = (bot - top) / rows
    for r in range(rows):
        y = top + hrow * (r + 1)
        out += (f'<rect x="{x0 - 6}" y="{f1(y - 14)}" width="{x1 - x0 + 12}" height="18" fill="{P["wood_light"]}" '
                f'stroke="{INK}" stroke-width="3.5"/>')
        x = x0 + 16
        while x < x1 - 40:
            kind = rng.random()
            if kind < 0.62:          # a little stack of scroll ends
                n = rng.choice((2, 3))
                for j in range(n):
                    cx = x + 20 + (j % 2) * 22 + (j // 2) * 11
                    cy = y - 30 - (j // 2) * 30 - (0 if j < 2 else 4)
                    out += (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="15" fill="#f1e2bf" stroke="{INK}" '
                            f'stroke-width="3"/><circle cx="{f1(cx)}" cy="{f1(cy)}" r="5" fill="#c9a46a"/>')
                x += 66
            else:                    # a clay tablet standing up
                h = rng.uniform(52, 70)
                out += (f'<rect x="{f1(x + 4)}" y="{f1(y - 14 - h)}" width="40" height="{f1(h)}" rx="7" '
                        f'fill="#c58f62" stroke="{INK}" stroke-width="3"/>'
                        + "".join(f'<path d="M{f1(x + 12)},{f1(y - 4 - h + 10 * k)} l22,0" stroke="#8a5a3a" '
                                  f'stroke-width="2.5"/>' for k in range(1, int(h / 10) - 1)))
                x += 58
    return out


def _canopy(x0, x1, top, dais_y):
    poles = ""
    for x in (x0, x1):
        poles += (f'<rect x="{x - 9}" y="{top + 40}" width="18" height="{dais_y - top - 40}" fill="{GOLD}" '
                  f'stroke="{INK}" stroke-width="3.5"/><circle cx="{x}" cy="{top + 30}" r="18" fill="{GOLD}" '
                  f'stroke="{INK}" stroke-width="3.5"/>')
    # back drape behind the throne (purple, gold border, a rosette medallion)
    drape = (f'<path d="M{x0 + 10},{top + 80} L{x1 - 10},{top + 80} L{x1 - 4},{dais_y} L{x0 + 4},{dais_y} Z" '
             f'fill="url(#hdrape)" stroke="{INK}" stroke-width="4"/>')
    for i in range(1, 6):
        x = x0 + (x1 - x0) * i / 6
        drape += (f'<path d="M{f1(x)},{top + 90} C{f1(x + 10)},{top + 260} {f1(x - 8)},{dais_y - 200} '
                  f'{f1(x + 6)},{dais_y - 6}" stroke="#4d2f6a" stroke-width="6" opacity="0.45" fill="none"/>')
    drape += (f'<path d="M{x0 + 30},{top + 96} L{x0 + 30},{dais_y - 10} M{x1 - 30},{top + 96} L{x1 - 30},{dais_y - 10}" '
              f'stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>')
    mx = (x0 + x1) / 2
    drape += (f'<circle cx="{mx}" cy="{top + 220}" r="58" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'
              + rosettes(mx, mx, top + 220, 100, 48, fill="#fff3d6", centre=P["terracotta"]))
    # valance: a scalloped purple top with gold fringe and tassels
    n = 7
    val = f'M{x0 - 30},{top} L{x1 + 30},{top} L{x1 + 30},{top + 70} '
    for i in range(n):
        xa = x1 + 30 - (x1 - x0 + 60) * (i + 1) / n
        xm = x1 + 30 - (x1 - x0 + 60) * (i + 0.5) / n
        val += f'Q{f1(xm)},{top + 118} {f1(xa)},{top + 70} '
    val += "Z"
    out = poles + drape
    out += f'<path d="{val}" fill="#6b4291" stroke="{INK}" stroke-width="4"/>'
    out += (f'<rect x="{x0 - 40}" y="{top - 26}" width="{x1 - x0 + 80}" height="34" rx="10" fill="{GOLD}" '
            f'stroke="{INK}" stroke-width="4"/>')
    for i in range(n):
        xm = x1 + 30 - (x1 - x0 + 60) * (i + 0.5) / n
        out += (f'<path d="M{f1(xm)},{top + 98} l0,30" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
                f'<circle cx="{f1(xm)}" cy="{top + 132}" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>')
    out += (f'<path d="M{x0 - 20},{top + 34} L{x1 + 20},{top + 34}" stroke="{GOLD}" stroke-width="7" '
            f'stroke-dasharray="16 12"/>')
    return out


def _floor(x0, x1):
    """Polished stone floor with perspective joints and the red runner that leads to the throne."""
    out = (f'<rect x="{x0}" y="{WALL_BOT}" width="{x1 - x0}" height="{SH - WALL_BOT + 30}" fill="url(#hfloor)" '
           f'stroke="{INK}" stroke-width="4"/>')
    joints = ""
    y, gap = WALL_BOT + 26, 30
    while y < SH + 20:
        joints += f'<path d="M{x0},{f1(y)} L{x1},{f1(y)}"/>'
        y += gap
        gap *= 1.28
    vx, vy = (x0 + x1) / 2, 420
    for x in range(x0 - 2400, x1 + 2400, 200):
        # lines from the vanishing point through (x, WALL_BOT) down to the bottom
        k = (SH + 30 - vy) / (WALL_BOT - vy)
        joints += f'<path d="M{x},{WALL_BOT} L{f1(vx + (x - vx) * k)},{SH + 30}"/>'
    out += f'<g stroke="#b99e74" stroke-width="2.5" opacity="0.55" fill="none">{joints}</g>'
    # the runner (lies flat: a horizontal band) from the dais to the right
    ry0, ry1 = 1196, 1318
    rx0 = hx(DAIS[1] - 30)
    out += (f'<path d="M{rx0},{ry0} L{x1 + 20},{ry0} L{x1 + 20},{ry1} L{rx0 - 12},{ry1} Z" fill="#b2493d" '
            f'stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{rx0 + 10},{ry0 + 14} L{x1 + 20},{ry0 + 14} M{rx0 + 2},{ry1 - 14} L{x1 + 20},{ry1 - 14}" '
            f'stroke="{GOLD}" stroke-width="6" fill="none"/>')
    for x in range(rx0 + 60, x1, 150):
        out += (f'<path d="M{x},{(ry0 + ry1) / 2} l26,-22 l26,22 l-26,22 Z" fill="none" stroke="#e8c27a" '
                f'stroke-width="3.5" opacity="0.8"/>')
    return out


def _dais():
    x0, x1, top, bot = hx(DAIS[0]), hx(DAIS[1]), DAIS[2], DAIS[3]
    out = (f'<path d="M{x0 + 30},{top - 26} L{x1 - 30},{top - 26} L{x1},{top + 6} L{x0},{top + 6} Z" '
           f'fill="#e8d3ad" stroke="{INK}" stroke-width="4"/>')
    out += (f'<rect x="{x0}" y="{top + 6}" width="{x1 - x0}" height="{bot - top - 6}" fill="#cfae7c" stroke="{INK}" '
            f'stroke-width="4"/><rect x="{x0}" y="{top + 24}" width="{x1 - x0}" height="34" fill="{BLUE}" '
            f'stroke="{INK}" stroke-width="3.5"/>' + rosettes(x0 + 36, x1 - 20, top + 41, 64, 12, fill="#f3e6c8",
                                                             centre=GOLD))
    # a purple rug on the dais under the throne
    out += (f'<path d="M{x0 + 90},{top - 18} L{x1 - 120},{top - 18} L{x1 - 100},{top + 2} L{x0 + 70},{top + 2} Z" '
            f'fill="#6b4291" stroke="{INK}" stroke-width="3"/>')
    # two low steps on the right
    for i in range(2):
        sx0 = x1 - 6 + 0 * i
        y0 = top + 6 + 40 * i
        out += (f'<rect x="{sx0 - 10 + 46 * i}" y="{y0 + 20}" width="{90 - 30 * i}" height="{bot - y0 - 20}" '
                f'fill="{S.mix("#e3cba0", "#c49e6a", 0.2 + 0.25 * i)}" stroke="{INK}" stroke-width="4"/>')
    return out


def hall_back_svg():
    """Static back of the hall: ceiling, frieze, wall, pilasters, windows, shelves, canopy drape, floor, dais."""
    defs = (S.lin_grad("hwall", [(0, WALL_A), (1, WALL_B)]) +
            S.lin_grad("hshadow", [(0, INK, 0.45), (1, INK, 0)]) +
            S.lin_grad("hwin", [(0, "#a8d4e4"), (1, "#e9f3ea")]) +
            S.lin_grad("hdrape", [(0, "#8a5cae"), (1, "#5f3c80")]) +
            S.lin_grad("hfloor", [(0, "#dcc49a"), (0.4, "#e7d4ae"), (1, "#d3b88c")]))
    x0, x1 = HX0 - 40, SW + 30
    wall = (f'<rect x="{x0}" y="-20" width="{x1 - x0}" height="{WALL_BOT + 20}" fill="url(#hwall)" stroke="{INK}" '
            f'stroke-width="4"/>')
    bricks = ""
    r = random.Random(11)
    y, row = 420, 0
    while y < 950:
        bricks += f'<path d="M{x0},{y} L{x1},{y}"/>'
        for x in range(x0 + (0 if row % 2 else 50), x1, 100):
            if r.random() < 0.4:
                bricks += f'<path d="M{x},{y - 44} L{x},{y}"/>'
        y += 44
        row += 1
    wall += f'<g stroke="#c4a473" stroke-width="2" opacity="0.45" fill="none">{bricks}</g>'
    wall += _frieze(x0, x1)
    # dado band
    wall += (f'<rect x="{x0}" y="{WALL_BOT - 82}" width="{x1 - x0}" height="64" fill="{BLUE}" stroke="{INK}" '
             f'stroke-width="3.5"/>'
             + "".join(f'<path d="M{x},{WALL_BOT - 26} l24,-26 l24,26" fill="none" stroke="#f3e6c8" '
                       f'stroke-width="4"/>' for x in range(x0 + 10, x1, 48)))
    wall += (f'<rect x="{x0}" y="{WALL_BOT - 18}" width="{x1 - x0}" height="18" fill="#c9ad80" stroke="{INK}" '
             f'stroke-width="3"/>')
    for cx in (950, 1520, 2470):
        wall += _window(hx(cx), 450, 790)
    for cx in (720, 1235, 1610, 2320, 2900):
        wall += _pilaster(hx(cx), 372, WALL_BOT - 82)
    wall += _shelves(hx(SHELF[0]), hx(SHELF[1]), SHELF[2], SHELF[3])
    body = S.g(wall, filter="wobble") + S.g(_beams(x0, x1), filter="wobble")
    body += S.g(_canopy(hx(150), hx(520), 520, DAIS[2]), filter="wobble")
    body += S.g(_floor(x0, x1), filter="wobble") + S.g(_dais(), filter="wobble")
    # the empty throne (King Darius sits on it on his own layer)
    body += PR.throne(hx(THRONE_HX), THRONE_Y, KS, 1)
    return doc(body, defs)


def pier_svg():
    """The curtain pier between the terrace and the hall (in front of everything at that x)."""
    defs = S.lin_grad("hpier", [(0, "#d9bd8f"), (0.5, "#ead5ad"), (1, "#c9a774")], x2=1, y2=0)
    x0, x1 = 2112, HX0
    out = (f'<rect x="{x0}" y="-20" width="{x1 - x0}" height="{SH + 40}" fill="url(#hpier)" stroke="{INK}" '
           f'stroke-width="5"/>')
    for y in range(60, SH, 70):
        out += f'<path d="M{x0},{y} L{x1},{y}" stroke="#bf9f6e" stroke-width="2.5" opacity="0.6"/>'
    out += (f'<rect x="{x0}" y="200" width="{x1 - x0}" height="140" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
            + rosettes(x0 + 46, x1 - 30, 270, 92, 26, fill="#f3e6c8", centre=GOLD))
    out += (f'<rect x="{x0}" y="{SH - 260}" width="{x1 - x0}" height="64" fill="{BLUE}" stroke="{INK}" '
            f'stroke-width="3.5"/>')
    # the curtain, tied back against the hall side of the pier
    cx = x1 - 6
    cur = (f'M{cx - 120},-20 L{cx + 150},-20 C{cx + 120},300 {cx + 40},560 {cx + 30},720 '
           f'C{cx + 60},860 {cx + 120},1060 {cx + 120},1250 L{cx - 10},1250 C{cx - 10},1060 {cx - 30},860 '
           f'{cx - 40},720 C{cx - 60},560 {cx - 110},300 {cx - 120},-20 Z')
    out += f'<path d="{cur}" fill="url(#hdrape2)" stroke="{INK}" stroke-width="4.5"/>'
    for k in (-60, 0, 60):
        out += (f'<path d="M{cx + k},-10 C{cx + k * 0.6 + 10},340 {cx + 10},600 {cx + 10},720 '
                f'C{cx + 20 + k * 0.5},900 {cx + 40 + k * 0.6},1080 {cx + 55 + k * 0.7},1240" stroke="#4d2f6a" '
                f'stroke-width="6" opacity="0.4" fill="none"/>')
    out += (f'<path d="M{cx - 50},700 Q{cx + 20},740 {cx + 90},700" stroke="{GOLD}" stroke-width="16" fill="none" '
            f'stroke-linecap="round"/><circle cx="{cx + 92}" cy="704" r="15" fill="{GOLD}" stroke="{INK}" '
            f'stroke-width="3.5"/><path d="M{cx + 92},718 l-8,60 l16,0 Z" fill="{GOLD}" stroke="{INK}" '
            f'stroke-width="3"/>')
    out += (f'<path d="M{cx - 6},1250 L{cx + 126},1250" stroke="{GOLD}" stroke-width="9"/>')
    defs += S.lin_grad("hdrape2", [(0, "#8a5cae"), (1, "#5f3c80")], x2=1, y2=0)
    return doc(S.g(out, filter="wobble"), defs)


def column_svg(which):
    """One free-standing Persian column near the camera (its own layer so figures can pass behind it)."""
    h = (COL_BASE - CEIL + 8) / 0.72 - 378
    return doc(PR.persian_column(hx(COL_FRONT[which]), COL_BASE, 0.72, height=h))


def sun_shafts_svg():
    """Soft sun shafts from the clerestory windows, slanting down to the floor (screen-blended)."""
    defs = S.lin_grad("hshaft", [(0, "#fff4d6", 0.85), (1, "#fff4d6", 0)])
    out = ""
    for cx in (950, 1520, 2470):
        x = hx(cx)
        out += (f'<path d="M{x - 75},{450} L{x + 75},{450} L{x + 330},{1300} L{x + 70},{1300} Z" '
                f'fill="url(#hshaft)"/>')
    return doc(S.g(out, filter="blur-md"), defs)


def lamp_stand(x, y, s=1.0):
    """A tall bronze lamp stand with a clay oil lamp on top (lit)."""
    body = (f'<path d="M{x - 40 * s},{y} L{x + 40 * s},{y} L{x + 14 * s},{y - 40 * s} L{x - 14 * s},{y - 40 * s} Z" '
            f'fill="#b9853f" stroke="{INK}" stroke-width="{4 * s}"/>'
            f'<rect x="{x - 7 * s}" y="{y - 330 * s}" width="{14 * s}" height="{292 * s}" fill="#c9954a" '
            f'stroke="{INK}" stroke-width="{3.5 * s}"/>'
            f'<ellipse cx="{x}" cy="{y - 330 * s}" rx="{46 * s}" ry="{12 * s}" fill="#b9853f" stroke="{INK}" '
            f'stroke-width="{3.5 * s}"/>')
    return S.g(body, filter="wobble-fine") + PR.oil_lamp(x - 10 * s, y - 336 * s, 0.75 * s, lit=True)


def hall_front_svg():
    """Foreground hall props drawn in front of the people at the back (lamp stands)."""
    return doc(lamp_stand(hx(2870), 1190, 1.0))


def records_table_markup(scrolls=True):
    """The low records table with scrolls, tablets and a basket (s03 / s04)."""
    x, y = hx(TABLE_HX), TABLE_Y
    out = (f'<rect x="{x - 210}" y="{y - 132}" width="420" height="30" rx="8" fill="{P["wood_light"]}" '
           f'stroke="{INK}" stroke-width="4"/><rect x="{x - 196}" y="{y - 104}" width="392" height="20" '
           f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3.5"/>')
    for lx in (x - 180, x + 160):
        out += (f'<path d="M{lx},{y - 84} L{lx + 20},{y - 84} L{lx + 22},{y} L{lx - 2},{y} Z" fill="{P["wood"]}" '
                f'stroke="{INK}" stroke-width="3.5"/>')
    if scrolls:
        out += PR.scroll(x - 110, y - 148, 0.7, rot=-4) + PR.scroll(x + 20, y - 150, 0.65, rot=6)
        out += (f'<rect x="{x + 100}" y="{y - 200}" width="46" height="66" rx="8" fill="#c58f62" stroke="{INK}" '
                f'stroke-width="3"/><rect x="{x + 132}" y="{y - 192}" width="46" height="58" rx="8" '
                f'fill="#b98257" stroke="{INK}" stroke-width="3"/>')
    return S.g(out, filter="wobble-fine")


def basket_markup(x, y, s=1.0):
    """A woven basket full of rolled scrolls standing on the floor."""
    out = (f'<path d="M{x - 70 * s},{y - 110 * s} L{x + 70 * s},{y - 110 * s} L{x + 56 * s},{y} L{x - 56 * s},{y} Z" '
           f'fill="#c9a061" stroke="{INK}" stroke-width="{4 * s}"/>')
    for k in range(1, 5):
        yy = y - 110 * s + 22 * s * k
        out += f'<path d="M{x - 68 * s + 3 * k},{yy} L{x + 68 * s - 3 * k},{yy}" stroke="#9c7440" stroke-width="3"/>'
    for dx, rot in ((-34, -14), (-6, 4), (24, -6), (46, 12)):
        out += (f'<g transform="rotate({rot} {x + dx * s} {y - 110 * s})"><rect x="{x + (dx - 12) * s}" '
                f'y="{y - 170 * s}" width="{24 * s}" height="{70 * s}" rx="{10 * s}" fill="#f1e2bf" stroke="{INK}" '
                f'stroke-width="{3 * s}"/><path d="M{x + (dx - 12) * s},{y - 150 * s} l{24 * s},0" stroke="#c0533a" '
                f'stroke-width="{4 * s}"/></g>')
    return S.g(out, filter="wobble-fine")


def guards_svg():
    out = ""
    for gx, gy, v in GUARDS:
        out += C.ground_shadow(hx(gx), gy, 0.85, 120, opacity=0.18)
        out += C.guard(hx(gx), gy, 0.85, 1 if gx < THRONE_HX else -1, variant=v)
    return doc(out)


def add_hall(sc, z0=0.0, t_off=0.0):
    """Add the static hall layers (identical seeds in s02-s04 so the dissolves between them match). ``t_off`` = this
    scene's start relative to s02's start, so the sun-shaft shimmer continues across the cuts."""
    sc.add("hall", hall_back_svg(), z=z0, seed=101)
    pul = M.pulse(0.55, 0.8, 7.0)
    sc.add("shafts", sun_shafts_svg(), z=z0 + 0.1, wc=0, blend="screen", motion=lambda t: pul(t + t_off))
    sc.add("guards", guards_svg(), z=z0 + 1, seed=102,
           motion=M.breathe(0.006, 3.4, pivot=(hx(400), 1150), phase=t_off / 3.4))
    sc.add("hall_front", hall_front_svg(), z=8, seed=103)
    sc.add("col0", column_svg(0), z=9, seed=104)
    sc.add("col1", column_svg(1), z=9.1, seed=105)
    sc.add("pier", pier_svg(), z=9.5, seed=106)


def scene_offset(scene_id):
    """Start of ``scene_id`` relative to s02's start (from the timeline)."""
    from engine.loader import load_timeline
    sc = {s["id"]: s["start"] for s in load_timeline()["scenes"]}
    return sc[scene_id] - sc["s02_daniel"]


# ============================================================================ terrace (s02 only)
TER_Y = 1240                    # Daniel's feet on the terrace
PARAPET = 1012                  # top of the parapet wall (merlons above)
DS = 1.3                        # Daniel's scale


def terrace_sky_svg():
    defs = (S.lin_grad("tsky", [(0, "#8cc4dc"), (0.45, "#bfe0e6"), (0.8, "#f1e6c8"), (1, "#f6dfb5")]) +
            S.rad_grad("tsun", [(0, "#fff8dc", 0.95), (0.35, "#fff1c6", 0.55), (1, "#fff1c6", 0)]))
    b = f'<rect x="-20" y="-20" width="{HX0 + 40}" height="{SH + 40}" fill="url(#tsky)"/>'
    b += '<circle cx="260" cy="330" r="520" fill="url(#tsun)"/>'
    b += (f'<circle cx="260" cy="330" r="74" fill="#fff0b8" stroke="{INK}" stroke-width="3" opacity="0.95" '
          f'filter="url(#wobble)"/>')
    return doc(b, defs)


def terrace_clouds_svg():
    b = (S.cloud(820, 300, 420, 120, "#fffaf0", seed=21, sw=3.5, shade_fill="#e3edf0") +
         S.cloud(1500, 210, 360, 110, "#fffaf0", seed=22, sw=3.5, shade_fill="#e3edf0") +
         S.cloud(1950, 380, 300, 90, "#fffaf0", seed=23, sw=3, shade_fill="#e3edf0") +
         S.cloud(2500, 260, 380, 110, "#fffaf0", seed=24, sw=3.5, shade_fill="#e3edf0"))
    return doc(S.g(b, filter="wobble"))


def ishtar_gate(x, y, s=1.0):
    """The blue glazed Ishtar gate of Babylon: two crenellated towers, an arch, rows of gold animals."""
    def P_(px, py):
        return f"{x + px * s:.1f},{y + py * s:.1f}"
    out = ""
    for tx in (-230, 130):
        out += (f'<path d="M{P_(tx, 0)} L{P_(tx, -470)} L{P_(tx + 100, -470)} L{P_(tx + 100, 0)} Z" fill="{BLUE}" '
                f'stroke="{INK}" stroke-width="{4 * s:.1f}"/>')
        for k in range(4):
            mx = tx + 4 + k * 25
            out += (f'<path d="M{P_(mx, -470)} L{P_(mx, -500)} L{P_(mx + 16, -500)} L{P_(mx + 16, -470)} Z" '
                    f'fill="{BLUE}" stroke="{INK}" stroke-width="{3.5 * s:.1f}"/>')
    out += (f'<path d="M{P_(-130, 0)} L{P_(-130, -380)} L{P_(130, -380)} L{P_(130, 0)} Z" fill="{BLUE}" '
            f'stroke="{INK}" stroke-width="{4 * s:.1f}"/>')
    for k in range(9):
        mx = -128 + k * 29
        out += (f'<path d="M{P_(mx, -380)} L{P_(mx, -404)} L{P_(mx + 18, -404)} L{P_(mx + 18, -380)} Z" fill="{BLUE}" '
                f'stroke="{INK}" stroke-width="{3.5 * s:.1f}"/>')
    out += (f'<path d="M{P_(-70, 0)} L{P_(-70, -170)} A{70 * s:.1f},{70 * s:.1f} 0 0 1 {P_(70, -170)} L{P_(70, 0)} Z" '
            f'fill="#4a3428" stroke="{INK}" stroke-width="{4 * s:.1f}"/>')
    out += (f'<path d="M{P_(-82, -170)} A{82 * s:.1f},{82 * s:.1f} 0 0 1 {P_(82, -170)}" fill="none" stroke="{GOLD}" '
            f'stroke-width="{8 * s:.1f}"/>')
    # rows of little gold animals (bulls and dragons as dots / bumps) and a rosette band
    for row, yy in enumerate((-110, -230, -350)):
        for tx in (-230, 130):
            for k in range(2):
                ax = tx + 25 + k * 50
                out += (f'<ellipse cx="{P_(ax, yy).split(",")[0]}" cy="{P_(ax, yy).split(",")[1]}" '
                        f'rx="{17 * s:.1f}" ry="{11 * s:.1f}" fill="#e8c27a" stroke="{INK}" '
                        f'stroke-width="{2 * s:.1f}"/>')
    out += rosettes(x - 110 * s, x + 110 * s, y - 300 * s, 44 * s, 10 * s, fill="#f3e6c8", centre=GOLD)
    return out


def city_svg():
    """Babylon in the morning haze: the skyline, the great ziggurat, the blue Ishtar gate, palms."""
    tint = "#e8e6d6"
    far = PR.nineveh_skyline(-80, HX0 + 80, 930, 0.78, seed=4, haze=0.42, tint=tint)
    zig = PR._haze(PR.ziggurat(1430, 930, 0.44), tint, 0.38, 0.2)
    gate = PR._haze(ishtar_gate(560, 985, 0.78), tint, 0.18, 0.1)
    palms = ""
    for x, s, lean in ((80, 0.62, 0.15), (330, 0.5, -0.1), (980, 0.55, 0.1), (1180, 0.48, -0.15), (1780, 0.6, 0.12),
                       (2020, 0.5, -0.1)):
        palms += PR.palm_tree(x, PARAPET + 40, s, lean=lean)
    return doc(zig + far + gate + palms)


def parapet_svg():
    """Terrace parapet (stepped Persian merlons, blue band) and the warm stone terrace floor."""
    defs = (S.lin_grad("tpar", [(0, "#e3c995"), (1, "#c9a774")]) +
            S.lin_grad("tfl", [(0, "#d9bf91"), (1, "#ead7b0")]))
    x0, x1 = -30, 2140
    out = (f'<rect x="{x0}" y="{PARAPET}" width="{x1 - x0}" height="140" fill="url(#tpar)" stroke="{INK}" '
           f'stroke-width="4"/><rect x="{x0}" y="{PARAPET + 42}" width="{x1 - x0}" height="34" fill="{BLUE}" '
           f'stroke="{INK}" stroke-width="3.5"/>' + rosettes(x0 + 40, x1, PARAPET + 59, 70, 11, fill="#f3e6c8",
                                                            centre=GOLD))
    for x in range(x0 + 10, x1, 92):
        out += (f'<path d="M{x},{PARAPET} L{x},{PARAPET - 22} L{x + 14},{PARAPET - 22} L{x + 14},{PARAPET - 42} '
                f'L{x + 30},{PARAPET - 42} L{x + 30},{PARAPET - 60} L{x + 46},{PARAPET - 60} L{x + 46},{PARAPET - 42} '
                f'L{x + 62},{PARAPET - 42} L{x + 62},{PARAPET - 22} L{x + 76},{PARAPET - 22} L{x + 76},{PARAPET} Z" '
                f'fill="#dcc08c" stroke="{INK}" stroke-width="3.5"/>')
    fl = PARAPET + 140
    out += (f'<rect x="{x0}" y="{fl}" width="{x1 - x0}" height="{SH - fl + 30}" fill="url(#tfl)" stroke="{INK}" '
            f'stroke-width="4"/>')
    j = ""
    y, gap = fl + 22, 26
    while y < SH + 20:
        j += f'<path d="M{x0},{f1(y)} L{x1},{f1(y)}"/>'
        y += gap
        gap *= 1.3
    vx, vy = 1050, 600
    for x in range(-1200, 3300, 170):
        k = (SH + 30 - vy) / (fl - vy)
        j += f'<path d="M{x},{fl} L{f1(vx + (x - vx) * k)},{SH + 30}"/>'
    out += f'<g stroke="#b99e74" stroke-width="2.5" opacity="0.55" fill="none">{j}</g>'
    # potted plants on the terrace
    pots = PR.jar(160, 1215, 1.1, color="#c46f48") + PR.bush(160, 1135, 0.62, variant=1)
    pots += PR.jar(1790, 1220, 1.0, color=BLUE) + PR.bush(1790, 1145, 0.55, variant=0)
    return doc(S.g(out, filter="wobble") + pots, defs)


def light_rays_svg():
    """Warm light falling from the morning sky onto the praying Daniel (screen-blended, faded in)."""
    defs = S.lin_grad("trays", [(0, "#fff3cc", 0.9), (1, "#fff3cc", 0)], x1=0, y1=0, x2=1, y2=1)
    src = (420, 120)
    d = ""
    for a0, a1 in ((44, 49), (51, 57), (59, 63.5)):
        r = 1500
        p0 = (src[0] + r * math.cos(math.radians(a0)), src[1] + r * math.sin(math.radians(a0)))
        p1 = (src[0] + r * math.cos(math.radians(a1)), src[1] + r * math.sin(math.radians(a1)))
        d += f"M{src[0]},{src[1]} L{f1(p0[0])},{f1(p0[1])} L{f1(p1[0])},{f1(p1[1])} Z "
    glow = S.rad_grad("tglow", [(0, "#fff2c8", 0.75), (1, "#fff2c8", 0)])
    b = S.g(f'<path d="{d}" fill="url(#trays)"/>', filter="blur-md")
    b += f'<ellipse cx="960" cy="1060" rx="300" ry="240" fill="url(#tglow)"/>'
    return doc(b, defs + glow)


# ============================================================================ people helpers
_DM = C._DANIEL_M if hasattr(C, "_DANIEL_M") else None


def dan(x, y, pose, facing=1, expr=None, s=DS, shadow=True, sw=None):
    sh = C.ground_shadow(x, y, s, sw or (190 if "kneel" in pose else 120), opacity=0.2) if shadow else ""
    return sh + C.daniel(x, y, s, facing, pose=pose, expr=expr)


def dan_ib(ps, x, y, facing=1, s=DS, expr=None, shadow=True):
    """In-between Daniel drawing from a custom pose dict."""
    D = C._daniel_design()
    inner, _ = C._figure(D, C._DANIEL_M, ps, expr or ps["expr"], C._fsign(facing), True)
    sh = C.ground_shadow(x, y, s, 160, opacity=0.2) if shadow else ""
    return sh + C._wrap_out(inner, x, y, s, facing, "daniel-ib")


HALF_KNEEL = C._P(t=2, h=-8, drop=26, legs=(("ik", 30, 1), ("ik", -34, 1)),
                  arms=(("ik", "torso", 1.3, 0.72, 1), ("ik", "torso", 1.3, 0.72, 1)), hands=("none", "pray"),
                  expr="peaceful")


def off(x, y, v, pose, facing=1, expr=None, s=0.95, shadow=True):
    sh = C.ground_shadow(x, y, s, 120, opacity=0.2) if shadow else ""
    return sh + C.official(x, y, s, facing, variant=v, pose=pose, expr=expr)


def king_fig(pose, expr=None, x=None, y=THRONE_Y, s=KS):
    return C.king(hx(THRONE_HX) if x is None else x, y, s, 1, pose=pose, attire="darius", expr=expr, throne=False)


def king_ib(ps, expr, design_pose="sit_throne", x=None, y=THRONE_Y, s=KS):
    D = C._king_design("darius", design_pose, False, False)
    inner, _ = C._figure(D, C._KING_M, ps, expr, 1, True)
    return C._wrap_out(inner, hx(THRONE_HX) if x is None else x, y, s, 1, "king-ib")


# the seated king opening his near hand toward Daniel ("he wanted to set him over the whole kingdom")
KING_OFFER = C._P(t=-2, h=-4, lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8,
                  arms=(("ik", "knee", 0, 0.25, 1), ("fk", 62, 96)), hands=("fist", "open"), expr="happy")
KING_OFFER_HALF = C._P(t=-2, h=-2, lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8,
                       arms=(("ik", "knee", 0, 0.25, 1), ("fk", 34, 80)), hands=("fist", "open"), expr="happy")


def heart_markup(x, y, s=1.0):
    d = (f"M{f1(x)},{f1(y + 20 * s)} C{f1(x - 34 * s)},{f1(y - 4 * s)} {f1(x - 26 * s)},{f1(y - 34 * s)} "
         f"{f1(x)},{f1(y - 18 * s)} C{f1(x + 26 * s)},{f1(y - 34 * s)} {f1(x + 34 * s)},{f1(y - 4 * s)} "
         f"{f1(x)},{f1(y + 20 * s)} Z")
    return S.g(f'<path d="{d}" fill="#e9737a" stroke="{INK}" stroke-width="{3.5 * s:.1f}" stroke-linejoin="round"/>'
               f'<circle cx="{f1(x - 12 * s)}" cy="{f1(y - 12 * s)}" r="{5 * s:.1f}" fill="#fbd0c8"/>',
               filter="wobble-fine")


# ============================================================================ the crowd of officials
CROWD_ROWS = (   # (ground y, scale, hall x0, hall x1, n)
    (1052, 0.44, 1860, 2640, 14),
    (1092, 0.5, 1830, 2630, 12),
    (1140, 0.56, 1800, 2610, 10),
)
OVS_START = ((1720, 3), (1880, 0), (2040, 2))    # front row: (hall x, variant); Daniel replaces variant 3
OVS_Y = FLOOR_Y
OVS_S = 0.95
OVS_END = (860, 1060, 1250)                         # Daniel, overseer A (v0), overseer B (v2)


def crowd_row_svg(i):
    gy, s, x0, x1, n = CROWD_ROWS[i]
    rng = random.Random(40 + i)
    out = ""
    for k in range(n):
        x = hx(x0 + (x1 - x0) * (k + 0.5) / n + rng.uniform(-12, 12))
        v = (k + i * 3) % 4
        pose = "stand" if rng.random() < 0.8 else "scheme"
        out += C.ground_shadow(x, gy, s, 110, opacity=0.15)
        out += C.official(x, gy, s, -1, variant=v, pose=pose, expr="neutral" if pose == "stand" else "happy")
    return doc(out)


# ============================================================================ animation helpers (s02-s04)
WALK_P = 0.27                   # one stride drawing per WALK_P (s)


def actor(sc, name, z, frames, anchor, s, base, walks=(), bumps=(), breathe=(0.01, 3.0, 0.0), extra=None,
          start_off=0.0, seed=None):
    """A character layer: ``frames`` are drawings at ``anchor`` (index 0 / 1 = walk_a / walk_b); ``base`` is
    [(t, frame index)] of hard cuts; ``walks`` [(t0, n, step[, pair[, period]])] planted-foot walks (s17's
    step_walk) that add up, ``pair`` = index of that walk's walk_a drawing (walk_b follows it; default 0; pass None
    placeholders for 0 / 1 when the figure never walks); ``bumps`` extra motions (dips, nods, hops) about the
    anchor; ``start_off`` shifts the figure at t=0 (draw it where it ends up and start it off-stage: drawings must
    lie inside the stage). Returns dx(t)."""
    ws = [step_walk(w[0], w[1], w[2], w[4] if len(w) > 4 else WALK_P, s) for w in walks]
    pairs = [w[3] if len(w) > 3 else 0 for w in walks]
    fb = cuts(base)

    def fa(t):
        for w, pb in zip(ws, pairs):
            v = w[0](t)
            if v is not None:
                return v + pb
        return fb(t)

    def dx(t):
        return start_off + sum(w[1](t) for w in ws)

    def dy(t):
        return sum(w[2](t) for w in ws)
    mot = [M.with_pivot(lambda t: Tf(dx=dx(t), dy=dy(t)), anchor)] + list(bumps)
    if breathe:
        mot.append(M.breathe(breathe[0], breathe[1], pivot=anchor, phase=breathe[2]))
    if extra:
        mot.append(extra)
    sc.add(name, [doc(f or "") for f in frames], z=z, frame_at=fa, motion=M.combine(*mot), seed=seed)
    return dx


def rise_pop(t0, pivot, depth=36):
    """Pop up into view: from invisible and squashed below, overshoot, settle."""
    return M.keys([(t0 - 0.01, {"alpha": 0, "dy": depth, "sy": 0.8, "sx": 0.94}),
                   (t0 + 0.14, {"alpha": 1, "dy": -8, "sy": 1.05, "sx": 1.0}),
                   (t0 + 0.32, {"alpha": 1, "dy": 0, "sy": 1.0, "sx": 1.0})], ["out", "sine"], pivot=pivot)


def dove_frames(sx, sy, s, facing):
    return [doc(PR.dove(sx, sy, s, facing, wing=w)) for w in (1.0, 0.4, -0.5, -1.0, -0.4, 0.3)]


def dove_path(x0, x1, y, t0, t1, ref, amp=18, phase=0.0):
    def m(t):
        u = (t - t0) / (t1 - t0)
        x = x0 + (x1 - x0) * u
        yy = y + amp * math.sin(2 * math.pi * (u * 2.2 + phase)) - 40 * u
        a = 0.0 if t < t0 - 0.05 or t > t1 + 0.05 else 1.0
        return Tf(dx=x - ref[0], dy=yy - ref[1], alpha=a)
    return m


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines
    c_name = chunk(L0, "名叫")
    c_bab = chunk(L0, "巴比伦")
    c_king = chunk(L2, "大利乌王")
    c_120 = chunk(L2, "一百二十")
    c_3 = chunk(L2, "三个总管")
    c_one = chunk(L3, "三个总管中")
    c_work = chunk(L3, "认真")
    c_whole = chunk(L3, "整个国家")

    # ---------------- static backdrops
    sc.add("sky", terrace_sky_svg(), z=0, wc=0.6, seed=11)
    sc.add("clouds", terrace_clouds_svg(), z=0.5, motion=M.drift(vx=6), seed=12)
    sc.add("city", city_svg(), z=1, seed=13)
    sc.add("parapet", parapet_svg(), z=2, seed=14)
    add_hall(sc, z0=3)

    # ---------------- doves over the city
    for i, (y, t0, t1, ph) in enumerate(((560, 1.2, 9.5, 0.0), (610, 1.6, 10.2, 0.4))):
        ref = (1000, 600)
        sc.add(f"dove{i}", dove_frames(ref[0], ref[1], 0.55 - 0.08 * i, -1), z=1.5, wc=0.6,
               frame_at=lambda t, i=i: float(int(t * 11 + 3 * i) % 6),
               motion=dove_path(2200, -150, y, t0, t1, ref, phase=ph))

    # ---------------- Daniel on the terrace
    X0, X1 = -140, 930
    n_walk = round((X1 - X0) / (87 * DS))
    step = (X1 - X0) / n_walk
    t_go = 1.0
    t_stop = snap(t_go + n_walk * WALK_P)
    t_greet = max(t_stop + 0.25, c_name.start + 0.9)
    t_point = c_bab.start + 0.45
    t_turn = L1.start + 0.05
    t_half = t_turn + 0.4
    t_kneel = t_half + 0.22
    ap = (X1, TER_Y)
    dframes = [dan(X1, TER_Y, "walk_a"), dan(X1, TER_Y, "walk_b"), dan(X1, TER_Y, "stand"),
               dan(X1, TER_Y, "explain", expr="happy"), dan(X1, TER_Y, "point", expr="happy"),
               dan(X1, TER_Y, "stand", -1), dan_ib(HALF_KNEEL, X1, TER_Y, -1), dan(X1, TER_Y, "kneel_pray", -1)]
    actor(sc, "daniel", 6, dframes, ap, DS,
          base=[(0, 2), (snap(t_greet), 3), (snap(t_point), 4), (snap(t_turn), 5), (snap(t_half), 6),
                (snap(t_kneel), 7)],
          walks=[(t_go, n_walk, step)], start_off=X0 - X1,
          bumps=[dip(t_stop, DS, ap, 6), dip(snap(t_greet), DS, ap), nod(t_greet + 0.2, ap, -3, 0.5),
                 dip(snap(t_point), DS, ap), dip(snap(t_turn), DS, ap, 6), dip(snap(t_half), DS, ap, 10),
                 dip(snap(t_kneel), DS, ap, 8)])
    # God's light falls on him while he prays (light only, no figure)
    sc.add("rays", light_rays_svg(), z=6.5, wc=0, blend="screen",
           motion=M.combine(M.keys([(t_kneel - 0.3, {"alpha": 0}), (t_kneel + 0.9, {"alpha": 1}),
                                    (L1.end + 0.6, {"alpha": 1}), (L1.end + 2.0, {"alpha": 0.6})], "sine"),
                            M.pulse(0.85, 1.0, 3.0)))

    # ---------------- King Darius
    kp = (hx(THRONE_HX), THRONE_Y)
    t_knod = c_king.start + 1.9
    t_love = c_work.start + 0.58 * (c_work.end - c_work.start)
    t_offer = c_whole.start + 0.05
    kframes = [king_fig("sit_throne"), king_fig("sit_throne", "happy"), king_ib(KING_OFFER_HALF, "happy"),
               king_ib(KING_OFFER, "happy")]
    sc.add("king", [doc(f) for f in kframes], z=5, seed=120,
           frame_at=cuts([(0, 0), (snap(t_knod), 1), (snap(t_offer), 2), (snap(t_offer + 0.16), 3)]),
           motion=M.combine(dip(snap(t_knod), KS, kp, 4), nod(t_knod + 0.1, kp, 2.5, 0.6),
                            nod(t_love, kp, 3, 0.7), dip(snap(t_offer), KS, kp, 4),
                            M.breathe(0.008, 3.2, pivot=kp, phase=0.3)))
    khead = C.body_points(C.king, kp[0], kp[1], KS, 1, pose="sit_throne", attire="darius", throne=False)["head"]
    for i in range(3):
        hx_, hy_ = khead[0] + 95 + 42 * i, khead[1] - 120 - 22 * (i % 2)
        t0 = t_love + 0.25 * i
        sc.add(f"heart{i}", doc(heart_markup(hx_, hy_, 0.9 - 0.12 * i)), z=5.5, wc=0,
               motion=M.keys([(t0, {"alpha": 0, "dy": 20, "s": 0.6}), (t0 + 0.3, {"alpha": 1, "dy": 0, "s": 1.0}),
                              (t0 + 1.6, {"alpha": 1, "dy": -70}), (t0 + 2.2, {"alpha": 0, "dy": -95})],
                             ["out", "sine", "sine"], pivot=(hx_, hy_)))

    # ---------------- the officials: three rows pop up, the three overseers step out of the front
    t_rows = [c_120.start + 0.8, c_120.start + 1.25, c_120.start + 1.7]
    for i in range(3):
        gy, s_, x0, x1, n = CROWD_ROWS[i]
        piv = (hx((x0 + x1) / 2), gy)
        sc.add(f"crowd{i}", crowd_row_svg(i), z=4.1 + 0.1 * i, motion=rise_pop(t_rows[i], piv))
    t_walk = c_3.start + 0.1
    for i, ((sx_, v), ex) in enumerate(zip(OVS_START, OVS_END)):
        x = hx(sx_)
        ap = (x, OVS_Y)
        dist = sx_ - ex
        n = max(2, round(dist / (87 * OVS_S)))
        t0 = t_walk + 0.09 * i
        t_arr = snap(t0 + n * WALK_P)
        pop = rise_pop(t_rows[2] + 0.05 * i, ap, 30)
        if v == 3:          # Daniel
            t_bow = c_one.start + 0.35
            t_read = c_work.start + 0.12
            t_bow2 = t_offer + 0.5
            fr = [dan(x, OVS_Y, "walk_a", -1, s=OVS_S), dan(x, OVS_Y, "walk_b", -1, s=OVS_S),
                  dan(x, OVS_Y, "stand", -1, s=OVS_S), dan(x, OVS_Y, "bow", -1, s=OVS_S),
                  dan(x, OVS_Y, "read", -1, s=OVS_S), dan(x, OVS_Y, "stand", -1, "happy", s=OVS_S)]
            actor(sc, "ov_daniel", 7.2, fr, ap, OVS_S, seed=121,
                  base=[(0, 2), (snap(t_bow), 3), (snap(t_bow + 1.3), 5), (snap(t_read), 4), (snap(t_bow2), 3)],
                  walks=[(t0, n, -dist / n)],
                  bumps=[pop, dip(t_arr, OVS_S, ap, 5), dip(snap(t_bow), OVS_S, ap, 6),
                         dip(snap(t_bow + 1.3), OVS_S, ap, 5), dip(snap(t_read), OVS_S, ap),
                         lambda t, t_read=t_read: (Tf(rot=1.0 * math.sin(2 * math.pi * (t - t_read) / 2.4))
                                                   if t_read + 0.3 < t < t_bow2 else Tf()),
                         dip(snap(t_bow2), OVS_S, ap, 6)])
            dan_walk = (t0, t_arr)
        else:
            fr = [off(x, OVS_Y, v, "walk_a", -1, s=OVS_S), off(x, OVS_Y, v, "walk_b", -1, s=OVS_S),
                  off(x, OVS_Y, v, "stand", -1, s=OVS_S)]
            actor(sc, f"ov{i}", 7.0 + 0.1 * i, fr, ap, OVS_S, base=[(0, 2)], walks=[(t0, n, -dist / n)],
                  seed=121 + i, bumps=[pop, dip(t_arr, OVS_S, ap, 5)], breathe=(0.01, 3.0, 0.3 * i))

    # ---------------- camera
    sc.camera = cam_path([
        (0.0, bcam(1050, 2096), 0),
        (t_point - 0.3, bcam(1050, 2096), 0),
        (t_point + 2.2, bcam(1130, 2040), 0),
        (t_turn + 0.2, bcam(1130, 2040), 0),
        (t_turn + 1.7, bcam(1000, 1900), 0),
        (L1.end - 1.5, bcam(1000, 1900), 300, trap(0.25)),
        (c_king.start + 2.7, bcam(2930, 2112), 0),
        (c_120.start - 0.4, bcam(2930, 2112), 0, trap(0.35)),
        (c_120.start + 1.9, bcam(3700, 2540), 0),
        (t_walk + 0.2, bcam(3700, 2540), 0),
        (t_walk + 3.1, bcam(3230, 2300), 0),
        (c_one.start - 0.3, bcam(3230, 2300), 0),
        (c_one.start + 1.9, bcam(3080, 1900), 0),
    ])

    # ---------------- effects
    sc.fx = [
        # light from God while Daniel prays: sparkles in the sky above-left of him (never on his face)
        FX.sparkles((420, 420, 860, 760), count=12, t0=t_kneel + 0.2, t1=L1.end + 1.2, color=(255, 240, 190),
                    size=(8, 16), period=1.8, drift=-6, seed=21),
        FX.motes((hx(950), 520, hx(2900), 1250), count=40, t0=0, color=(255, 246, 214), size=(2, 5), alpha=110,
                 seed=22),
    ]

    # ---------------- sound
    sc.sfx("birds", 0, dur=c_king.start + 1.5, gain_db=-15, fade_in=0.8, fade_out=1.6)
    sc.sfx("wind_soft", 0, dur=c_king.start + 1.0, gain_db=-20, fade_in=0.8, fade_out=1.6)
    sc.sfx("footsteps", t_go, dur=t_stop - t_go, gain_db=-14, fade_in=0.05, fade_out=0.2, rate=1 / WALK_P)
    sc.sfx("cloth", t_greet - 0.05, gain_db=-14)
    sc.sfx("cloth", t_turn - 0.05, gain_db=-14)
    sc.sfx("cloth", t_kneel - 0.05, gain_db=-12)
    sc.sfx("chime", t_kneel + 0.05, gain_db=-11)
    sc.sfx("crowd", c_120.start + 0.3, dur=c_one.start - c_120.start + 0.5, gain_db=-19, fade_in=0.8, fade_out=1.5)
    for i, t in enumerate(t_rows):
        sc.sfx("pop", t, gain_db=-13, pan=0.2 + 0.1 * i)
    sc.sfx("footsteps", dan_walk[0], dur=dan_walk[1] - dan_walk[0] + 0.2, gain_db=-13, fade_in=0.05, fade_out=0.25,
           rate=1 / WALK_P)
    sc.sfx("cloth", c_one.start + 0.3, gain_db=-14)
    sc.sfx("cloth", t_read - 0.05, gain_db=-12)
    sc.sfx("sparkle", t_love + 0.1, gain_db=-16)
    sc.sfx("cloth", t_offer, gain_db=-15)
    sc.sfx("cloth", t_bow2, gain_db=-16)
    return sc
