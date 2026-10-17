"""Scene 15 — the great city (Jonah 3:3b-4), v2.

"Nineveh is a very, very big city: it takes three whole days to walk all the way through it. Jonah went into the
city, walked a day's journey and, as he walked, called out: 'In forty days Nineveh will be destroyed!'"

One 3200 x 1800 stage, two paintings on it, joined by a camera fly-through of the west gate:

  * OUTSIDE — the panorama (line 0). A morning view of Nineveh from the plain: the long crenellated front wall
    with two gates and corner towers whose side walls run back toward the horizon, the palace on its mound, the
    great ziggurat, rows and rows of flat roofs, a hazy skyline that goes on and on, the river Tigris winding in
    on the right with boats, fields, palms, sheep and a resting camel. The picture opens close on the road and
    the west gate, where little Jonah is walking up to the city (calm frame for the dissolve).
      "尼尼微是一座非常非常大的城，" — the camera pulls back and back until the whole city fills the page.
      "要走整整三天，" — a picture-book device: a trail of little footprints walks itself across the city from the
          west gate to the far east end, and at each third of the way a smiling sun pops up (1, 2, 3).
      "才能走遍整座城。" — the trail and suns stay up, the suns bob; then the trail fades and the camera pushes in
          toward the west gate as Jonah reaches it.
  * THE FLY-THROUGH (v1 technique, "约拿进了城，"): every outside layer scales up around the gate opening (a hole
    cut through the wall and everything behind it) until the opening covers the frame; then the outside is dropped
    and we are inside, in a street, with Jonah walking in from the gate.
  * INSIDE — a long street that opens onto the market square (line 1, line 2).
      "走了一天的路，一边走，" — Jonah walks east (planted-foot walk cycle: the drawing follows the distance
          walked), the camera tracking him past houses, palms, laundry, children playing and passers-by. The day
          goes by: the sun rises behind the roofs on the left, arcs over the street and sinks toward the right; the
          light goes from rosy morning through white noon to golden afternoon; Jonah's shadow swings round.
      "一边大声喊：" — still walking, he raises his arm and calls out (sound arcs); people he passes stop and look.
      He lowers his arm, reaches the market square and walks up the two tiers of the stone step.
      Line 2 (Jonah) "再过四十天，尼尼微就要毁灭了！" — arm high, he proclaims; the people in the square stop and
          turn to him (hard pose cuts sold by little hops), "!" marks pop over their heads, a mother points; on
          "尼尼微就要毁灭了" they look worried (hand to chin, the girl hangs her head). He lowers his arm; a calm,
          readable last second (golden late-afternoon light, low sun over the rooftops) for the dissolve into s16.

Notes for maintainers
* Every time comes from ctx.lines[i].start / .end / .at(phrase) (fractions only inside one chunk).
* Characters in the street and market are SPRITES: drawn on small canvases (rasterised + watercoloured once,
  cached on disk like layers) and placed by Dynamic layers; full-stage layers would cost ~5 s each to rasterise
  on this big stage. Things seen in the zoomed-out panorama stay ordinary layers (they get the compositor's
  mip-mapped downscaling).
* Pose changes are hard cuts hidden by a squash-and-hop; expression-only changes are cuts too. No crossfades
  between different drawings of a figure.
"""
import math
import random
from contextlib import contextmanager

import cv2
import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s09_nineveh as V
from art.style import P
from engine import motion as M
from engine import raster
from engine import watercolor as WC
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3200, 1800
INK = P["ink"]

# ================================================================ outside (panorama) geometry
WALL_Y, WALL_H = 1100, 260
K = WALL_H / 260.0
WALL_X0, WALL_X1 = 250, 2990
SEAM_X = 1360                       # the front wall is two city_wall pieces; a tower hides the joint
GX, GWD = 640, 156                  # west gate (Jonah goes in here; the camera flies through it)
GX2, GWD2 = 2060, 140               # a second gate further east
SPRING = WALL_Y - WALL_H * 0.62
HOLE_R = 60                         # see-through opening: inside the open door leaves and the arch rim
HOLE_D = (f"M{GX - HOLE_R},{WALL_Y + 3} L{GX - HOLE_R},{SPRING:.1f} A{HOLE_R},{HOLE_R} 0 0 1 {GX + HOLE_R},"
          f"{SPRING:.1f} L{GX + HOLE_R},{WALL_Y + 3} Z")
HOLE_CLEAR = (GX - HOLE_R + 8, GX + HOLE_R - 8, SPRING, WALL_Y - 12)
HORIZON = 640

# footprint trail ("three days' walk") over the city, west gate -> east end
TRAIL = [(GX + 10, 850), (820, 760), (1150, 705), (1550, 690), (1950, 700), (2350, 680), (2750, 700),
         (2950, 770)]

# ================================================================ inside (street + market) geometry
GY = 1310                           # street ground line (Jonah's feet)
BACK_Y = 1120                       # ground line of the back row of houses
STEP_X, STEP_Y = 1810, 1324         # the stone step in the market: centre, bottom line
STEP_TOP = STEP_Y - 62              # where Jonah stands to preach
JX_STOP = STEP_X - 20               # his spot on the step
JS = 0.92                           # Jonah's scale in the street
WALK_A, WALK_N = 56, 6              # planted-foot walk: ankle travel (figure px) per half step, drawings per step
ADV = 2 * WALK_A / WALK_N * JS      # stage px the anchor advances per walk drawing (planted sole stays put)
CAM_ST0 = Cam(1180, 1000, 1800)     # the street framing right after the fly-through
SKY_BOT = 1130                      # the street sky is hidden by houses and floor below this


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def keyed(keys_, curve="sine"):
    """Scalar keyframes [(t, v), ...] -> f(t), eased between keys."""
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


def hole_mask(mid):
    return (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{SW + 100}" height="{SH + 100}">'
            f'<rect x="-50" y="-50" width="{SW + 100}" height="{SH + 100}" fill="#fff"/>'
            f'<path d="{HOLE_D}" fill="#000"/></mask>')


def poly(pts, fill, sw=4, extra=""):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" '
            f'{extra}/>')


def haze(markup, k, tint=None):
    """Aerial perspective: push every colour toward the sky colour (fills by k, ink by k/2)."""
    return PR._haze(markup, tint or S.mix(P["sky_day"], P["sky_warm"], 0.6), k, 0.5 * k)


# ================================================================ sprites


class Sprite:
    """Drawings of one figure rasterised on a small canvas (raster + watercolour cached on disk, exactly like
    layers) and placed per frame by a Dynamic layer. Markup is drawn with its anchor at (ax, ay)."""

    def __init__(self, cw, ch, ax, ay, wc=1.0, seed=0):
        self.cw, self.ch, self.ax, self.ay = int(cw), int(ch), ax, ay
        self.wc, self.seed = wc, seed
        self.svgs, self.imgs = [], None
        self._rs = {}

    def add(self, markup):
        self.svgs.append(S.svg_doc(markup, w=self.cw, h=self.ch).replace(S.BOIL_TOKEN, "1"))
        return len(self.svgs) - 1

    def load(self):
        if self.imgs is None:
            out = []
            for svg in self.svgs:
                im = raster.rasterize(svg, self.cw, self.ch)
                if self.wc > 0:
                    im = WC.watercolor(im, seed=self.seed, strength=self.wc)
                out.append(im)
            self.imgs = out
        return self.imgs

    def place(self, i, x, y, sx=1.0, sy=1.0, dy=0.0, alpha=1.0):
        """(image, top-left) with the anchor at stage (x, y + dy); squash/stretch about the anchor."""
        im = self.load()[int(i)]
        ax, ay = self.ax, self.ay
        if abs(sx - 1) > 2e-3 or abs(sy - 1) > 2e-3:
            w, h = im.size
            nw, nh = max(1, round(w * sx)), max(1, round(h * sy))
            key = (int(i), nw, nh)
            if key not in self._rs:
                if len(self._rs) > 400:
                    self._rs.clear()
                self._rs[key] = im.resize((nw, nh), Image.BILINEAR)
            im = self._rs[key]
            ax, ay = ax * nw / w, ay * nh / h
        if alpha < 0.998:
            if alpha <= 0.002:
                return None
            a = np.asarray(im).copy()
            a[..., 3] = (a[..., 3].astype(np.float32) * alpha).astype(np.uint8)
            im = Image.fromarray(a, "RGBA")
        return im, (x - ax, y + dy - ay)


_SPRITES = []


def sprite(cw, ch, ax, ay, wc=1.0, seed=0):
    s = Sprite(cw, ch, ax, ay, wc, seed)
    _SPRITES.append(s)
    return s


def person_sprite(s, wide=170, tall=360, seed=0):
    """Canvas for a figure at scale s (anchor bottom centre, head room for hops)."""
    cw, ch = 2 * wide * s + 40, tall * s + 70
    return sprite(cw, ch, cw / 2, ch - 22, seed=seed)


# ================================================================ Jonah (custom rig poses)

_EXTRA_EXPRS = {"serious": dict(eyes="dot", brow=(0.015, -0.005, -0.02), mouth="flat")}


@contextmanager
def extra_exprs():
    added = [k for k in _EXTRA_EXPRS if k not in C.EXPRS]
    for k in added:
        C.EXPRS[k] = _EXTRA_EXPRS[k]
    try:
        yield
    finally:
        for k in added:
            C.EXPRS.pop(k, None)


def jfig(x, y, s, ps, expr, facing=1, label="j", marks=True):
    inner, _ = C._figure(C._jonah_design(), C._ADULT, ps, expr, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


def walk_pose(k, arm="down"):
    """Planted-foot walk drawing k (WALK_N drawings per step, two steps per cycle): the planted ankle goes from
    +A to -A figure px while the other foot swings through, so advancing the anchor ADV stage px per drawing keeps
    the planted sole on one spot. arm: 'down' (both arms swing), 'mid' / 'up' (far arm raised: calling out)."""
    ph = (k % (2 * WALK_N)) / WALK_N
    step, u = divmod(ph, 1.0)
    A = WALK_A
    plant = ("ik", A * (1 - 2 * u), 1)
    swing = ("ik", -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, 22 * math.sin(math.pi * u))
    sw = 34 * math.cos(math.pi * ph)
    far, hands = ("fk", -sw, -sw + 14), ("fist", "fist")
    if arm == "up":
        far, hands = ("fk", 150, 166), ("open", "fist")
    elif arm == "mid":
        far, hands = ("fk", 116, 142), ("open", "fist")
    return C._P(t=4, h=-3, legs=(plant, swing) if step == 0 else (swing, plant),
                arms=(far, ("fk", sw, sw + 14)), hands=hands, drop=12 + 4 * math.cos(2 * math.pi * u))


STAND = C._P(arms=(("fk", 14, 8), ("fk", -8, -3)))
PREACH = dict(C.POSES["preach"])


# ================================================================ outside: drawing


def pano_sky_body():
    defs = (S.lin_grad("s15psky", [(0, P["sky_day_top"]), (0.28, P["sky_day"]),
                                   (0.44, S.mix(P["sky_day"], P["sky_warm"], 0.55)), (0.52, P["sky_warm"]),
                                   (1, P["sky_warm"])])
            + S.rad_grad("s15pglow", [(0, "#fff3d6", 0.75), (0.5, "#fde9c4", 0.3), (1, "#fde9c4", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s15psky)"/>'
            f'<ellipse cx="2900" cy="560" rx="900" ry="420" fill="url(#s15pglow)"/>')
    return body, defs


def pano_clouds_svg(items):
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, "#fdf6e8", seed=seed, sw=3, shade_fill="#efe2d0")
    return doc(S.g(body, filter="wobble"))


def corner_tower(xe, side):
    """Square corner tower closing one end of the front wall (side -1: left end at xe, +1: right end), with the
    side wall running back up the page toward the horizon behind it (adapted from v1 s09)."""
    k = K
    col = P["sand"]
    dark = S.shade(col, -0.2)
    x0, x1 = xe - 50 * k, xe + 70 * k
    top = WALL_Y - WALL_H - 100 * k
    out = ""
    # the side wall recedes up-left (lower and hazier as it goes), ending in a small far corner tower
    bx, by = x0 - 300, WALL_Y - 330
    hb = WALL_H * 0.55
    side_col = S.mix(S.shade(col, -0.2), P["sky_warm"], 0.08)
    out += V.merlons(bx + 4, x0 - 4, by - hb - 2, side_col, 24 * k, 9 * k, 20 * k, 3.2,
                     slope=((WALL_Y - WALL_H) - (by - hb)) / (x0 - bx))
    out += poly([(bx, by), (x0, WALL_Y), (x0, WALL_Y - WALL_H), (bx, by - hb)], side_col, 3.5)
    for i in range(1, 9):
        u = i / 9
        ya, yb = (by - hb) + hb * u, (WALL_Y - WALL_H) + WALL_H * u
        out += (f'<path d="M{f1(bx + 3)},{f1(ya)} L{f1(x0 - 3)},{f1(yb)}" stroke="{dark}" stroke-width="1.6" '
                f'opacity="0.3"/>')
    for u in (0.22, 0.48, 0.72):                      # buttresses, closer together toward the far end
        xa = x0 + (bx - x0) * u
        ya_b = WALL_Y + (by - WALL_Y) * u
        ha = WALL_H + (hb - WALL_H) * u
        wb = 26 * (1 - 0.45 * u)
        out += poly([(xa, ya_b), (xa - wb, ya_b - 0.9 * wb), (xa - wb, ya_b - ha - 10), (xa, ya_b - ha - 8)],
                    S.shade(side_col, 0.1), 3)
    fk = 0.6
    ft = by - hb - 50 * fk
    far = (V.merlons(bx - 34 * fk, bx + 34 * fk, ft, side_col, 22 * fk, 8 * fk, 20 * fk, 2.6)
           + f'<rect x="{f1(bx - 30 * fk)}" y="{f1(ft)}" width="{f1(60 * fk)}" height="{f1(by - ft)}" '
             f'fill="{side_col}" stroke="{INK}" stroke-width="3"/>')
    out = far + out
    out += V.merlons(x0 - 6 * k, x1 + 6 * k, top, col, 40 * k, 16 * k, 34 * k)
    out += poly([(x0, WALL_Y), (x0 - 16 * k, WALL_Y - 8 * k), (x0 - 16 * k, top - 8 * k), (x0, top)],
                S.shade(col, -0.18), 4)
    out += (f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(x1 - x0)}" height="{f1(WALL_Y - top)}" '
            f'fill="{S.shade(col, 0.06)}" stroke="{INK}" stroke-width="4"/>')
    out += (f'<rect x="{f1(x0 + 2)}" y="{f1(WALL_Y - 26 * k)}" width="{f1(x1 - x0 - 4)}" height="{f1(24 * k)}" '
            f'fill="{S.shade(col, -0.12)}"/>')
    yy = top + 26 * k
    while yy < WALL_Y - 20 * k:
        out += (f'<path d="M{f1(x0 + 3)},{f1(yy)} L{f1(x1 - 3)},{f1(yy)}" stroke="{dark}" stroke-width="1.8" '
                f'opacity="0.35"/>')
        yy += 26 * k
    cx = (x0 + x1) / 2
    for wy in (top + 70 * k, top + 170 * k):
        out += (f'<rect x="{f1(cx - 6 * k)}" y="{f1(wy)}" width="{f1(12 * k)}" height="{f1(34 * k)}" '
                f'rx="{f1(6 * k)}" fill="#4a3426" stroke="{INK}" stroke-width="3"/>')
    out += V.rosette_band(x0 + 6 * k, x1 - 6 * k, top + 22 * k, 22 * k)
    out += (f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(x1 - x0)}" height="{f1(WALL_Y - top)}" fill="none" '
            f'stroke="{INK}" stroke-width="4"/>')
    if side > 0:
        out = f'<g transform="translate({2 * xe},0) scale(-1,1)">{out}</g>'
    return S.g(out, filter="wobble-fine")


def temple(x, y, s, col=None):
    """A small flat-topped temple / tower block with a glazed band (interior filler, local bottom centre)."""
    col = col or P["stone_light"]
    w, h = 120, 210
    out = V.merlons(-w / 2 - 4, w / 2 + 4, -h, col, 22, 8, 20, 3)
    out += f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="{col}" stroke="{INK}" stroke-width="3.5"/>'
    out += V.rosette_band(-w / 2 + 4, w / 2 - 4, -h + 30, 18)
    out += (f'<path d="M-18,0 L-18,-60 A18,18 0 0 1 18,-60 L18,0 Z" fill="#5b4232" stroke="{INK}" '
            f'stroke-width="3"/>')
    for wx in (-36, 30):
        out += f'<rect x="{wx}" y="{-h + 70}" width="10" height="22" rx="5" fill="#5b4232"/>'
    return S.g(f'<g transform="translate({f1(x)},{f1(y)}) scale({s:.3f})">{out}</g>', filter="wobble-fine")


def pano_back_svg():
    """Sky + everything behind the front wall in one layer (the gate opening cut out)."""
    sky, sdefs = pano_sky_body()
    body, defs = interior_body()
    return doc(f'<g mask="url(#s15hi)">{sky}{body}</g>', sdefs + defs)


def interior_body():
    """Everything behind the front wall, painted as if seen from a little above (further = higher on the page):
    the far plain and hills, the hazy skyline that goes on and on, rows and rows of roofs climbing the city
    mound, the palace on its mound, the great ziggurat, temples, towers and palms. The gate opening is cut out."""
    rng = random.Random(15)
    defs = (S.lin_grad("s15fp", [(0, S.mix(P["sand_light"], P["sky_warm"], 0.55)),
                                 (1, S.mix(P["sand_light"], P["sand"], 0.3))])
            + hole_mask("s15hi"))
    far_col = S.mix(P["stone"], P["sky_day"], 0.55)
    base = S.path(S.hill(-80, 1000, HORIZON + 10, 70, seed=4, bumps=2), fill=far_col, sw=2.5)
    base += S.path(S.hill(2200, 3300, HORIZON + 10, 85, seed=8, bumps=2), fill=far_col, sw=2.5)
    base += (f'<rect x="-40" y="{HORIZON}" width="{SW + 80}" height="{SH - HORIZON + 40}" fill="url(#s15fp)" '
             f'stroke="{INK}" stroke-width="2.5"/>')
    body = S.g(base, filter="wobble")
    # the far city (hazy): it keeps going behind everything
    body += PR.nineveh_skyline(-60, SW + 60, HORIZON + 30, scale=0.95, seed=21, haze=0.55)
    # the city mound (warm ground the houses stand on)
    mound = (f'<path d="M{WALL_X0 - 300},{WALL_Y - 330} C700,{HORIZON + 40} 1300,{HORIZON + 10} 1700,{HORIZON + 20} '
             f'S2600,{HORIZON + 40} {WALL_X1 + 300},{WALL_Y - 330} L{WALL_X1 + 60},{WALL_Y} L{WALL_X0 - 60},{WALL_Y} Z" '
             f'fill="{S.mix(P["sand"], P["sky_warm"], 0.25)}" stroke="{INK}" stroke-width="2.5"/>')
    body += S.g(mound, filter="wobble")
    rows = ((HORIZON + 70, 0.15, 0.36), (HORIZON + 112, 0.17, 0.28), (HORIZON + 156, 0.19, 0.2),
            (HORIZON + 200, 0.21, 0.13), (HORIZON + 246, 0.235, 0.06))
    landmarks = {
        # (row index to draw after, markup)
        1: haze(PR.ziggurat(2330, HORIZON + 120, 0.4), 0.12),
        2: haze(S.g(f'<g transform="translate(1290,{HORIZON + 150}) scale(1.45)">{PR._palace(1.0)}</g>',
                    filter="wobble-fine"), 0.1),
    }
    for row, (gy, sc, hz_) in enumerate(rows):
        span_l = WALL_X0 - 300 + (row + 1) * 55
        span_r = WALL_X1 + 300 - (row + 1) * 55
        x = span_l + rng.uniform(0, 80)
        houses = ""
        while x < span_r:
            v = rng.randint(0, 3)
            free_pal = not (1120 < x < 1470 and 1 <= row <= 2)
            free_zig = not (2120 < x < 2540 and row <= 1)
            if free_pal and free_zig:
                if rng.random() < 0.12:
                    houses += temple(x, gy + rng.uniform(-6, 6), sc * 2.0 * rng.uniform(0.9, 1.1))
                else:
                    houses += PR.house(x, gy + rng.uniform(-8, 8), sc * rng.uniform(0.9, 1.08), v,
                                       facing=rng.choice((1, -1)))
            x += rng.uniform(170, 240) * sc / 0.2
        for _ in range(5 + row):
            px = rng.uniform(span_l + 60, span_r - 60)
            houses += PR.palm_tree(px, gy + 10, 0.2 * sc / 0.17 * rng.uniform(0.85, 1.1),
                                   lean=rng.uniform(-0.3, 0.3), dates=False)
        body += haze(houses, hz_)
        if row in landmarks:
            body += landmarks[row]
    return body, defs


def passage_svg():
    """The inside of the open west gate (shown until the camera flies through it)."""
    r = GWD / 2
    d = (f"M{GX - r - 6},{WALL_Y + 4} L{GX - r - 6},{SPRING:.1f} A{r + 6},{r + 6} 0 0 1 {GX + r + 6},{SPRING:.1f} "
         f"L{GX + r + 6},{WALL_Y + 4} Z")
    r2 = r * 0.5
    far = (f"M{GX - r2},{WALL_Y - 6} L{GX - r2},{SPRING + 34:.1f} A{r2},{r2} 0 0 1 {GX + r2},{SPRING + 34:.1f} "
           f"L{GX + r2},{WALL_Y - 6} Z")
    defs = S.lin_grad("s15pas", [(0, "#3a2a20"), (0.6, "#4a3426"), (1, "#5c4231")])
    body = (f'<path d="{d}" fill="url(#s15pas)"/>'
            f'<path d="{far}" fill="{S.mix(P["sand_light"], P["sky_warm"], 0.45)}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{GX - r2 + 4},{WALL_Y - 22} L{GX + r2 - 4},{WALL_Y - 22} L{GX + r2 - 2},{WALL_Y - 6} '
            f'L{GX - r2 + 2},{WALL_Y - 6} Z" fill="{P["sand"]}"/>'
            f'<path d="M{GX - r2 - 30},{WALL_Y + 2} L{GX - r2},{WALL_Y - 6} L{GX + r2},{WALL_Y - 6} '
            f'L{GX + r2 + 30},{WALL_Y + 2} Z" fill="#6a4c36"/>')
    return doc(S.g(body, filter="wobble-fine"), defs)


def pano_front_svg():
    """The front wall (gate opening cut out) and the plain in front of it, in one layer."""
    wall, wdefs = wall_body()
    ground, gdefs = ground_body()
    return doc(wall + ground, wdefs + gdefs)


def wall_body():
    wall = PR.city_wall(WALL_X0, SEAM_X, WALL_Y, WALL_H, gate=(GX, GWD), doors_open=1.0, seed=9)
    wall += PR.city_wall(SEAM_X, WALL_X1, WALL_Y, WALL_H, gate=(GX2, GWD2), doors_open=0.75, seed=13)
    wall += S.g(PR._tower(SEAM_X, WALL_Y, 96 * K, WALL_H + 56 * K, P["sand"], K), filter="wobble-fine")
    wall += corner_tower(WALL_X0, -1) + corner_tower(WALL_X1, 1)
    ban = ""
    for gx_, gw_ in ((GX, GWD), (GX2, GWD2)):
        for tx in (gx_ - gw_ / 2 - 60 * K, gx_ + gw_ / 2 + 60 * K):
            top = WALL_Y - WALL_H * 1.45 + 64 * K
            ban += (f'<path d="M{tx - 26},{top} L{tx + 26},{top} L{tx + 26},{top + 150} L{tx},{top + 128} '
                    f'L{tx - 26},{top + 150} Z" fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3.5" '
                    f'stroke-linejoin="round"/>'
                    f'<circle cx="{tx}" cy="{top + 56}" r="13" fill="{P["gold"]}" stroke="{INK}" stroke-width="3"/>'
                    f'<rect x="{tx - 31}" y="{top - 8}" width="62" height="10" rx="4" fill="{P["wood"]}" '
                    f'stroke="{INK}" stroke-width="3"/>')
    rim = (f'<path d="{HOLE_D}" fill="none" stroke="{S.mix(P["glow"], P["sand_light"], 0.3)}" stroke-width="6" '
           f'opacity="0.6"/>')
    defs = hole_mask("s15hw")
    return f'<g mask="url(#s15hw)">{wall}{S.g(ban + rim, filter="wobble-fine")}</g>', defs


def road_path():
    left = [(120, SH + 40), (330, 1560), (470, 1330), (560, 1190), (GX - 92, WALL_Y)]
    right = [(GX + 92, WALL_Y), (730, 1190), (760, 1330), (800, 1560), (860, SH + 40)]
    d = S.smooth_path(left, closed=False, tension=0.8)
    d += f" L{right[0][0]},{right[0][1]}"
    d += " " + S.smooth_path(right, closed=False, tension=0.8).replace("M", "L", 1)
    return d + " Z"


RIVER_BANK = [(SW + 40, 1128), (2980, 1160), (2730, 1240), (2520, 1380), (2390, 1560), (2330, SH + 40)]


def boat(x, y, s, facing=1, who=3):
    k = s
    hull = (f'<path d="M{x - 120 * k},{y - 30 * k} Q{x - 100 * k},{y + 18 * k} {x},{y + 20 * k} '
            f'Q{x + 100 * k},{y + 18 * k} {x + 125 * k},{y - 34 * k} Q{x},{y - 8 * k} {x - 120 * k},{y - 30 * k} Z" '
            f'fill="{P["wood"]}" stroke="{INK}" stroke-width="{4 * k:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{x - 100 * k},{y - 12 * k} Q{x},{y + 6 * k} {x + 104 * k},{y - 14 * k}" '
            f'stroke="{P["wood_dark"]}" stroke-width="{3 * k:.1f}" fill="none"/>')
    man = C.citizen(x - 20 * k * facing, y - 14 * k, 0.42 * k, facing, kind="man", variant=who, pose="stand")
    pole = (f'<path d="M{x + 30 * k * facing},{y - 150 * k} L{x + 70 * k * facing},{y + 40 * k}" '
            f'stroke="{P["wood_dark"]}" stroke-width="{6 * k:.1f}" stroke-linecap="round"/>')
    water = (f'<path d="M{x - 150 * k},{y + 16 * k} q{30 * k},{-8 * k} {60 * k},0 M{x + 80 * k},{y + 14 * k} '
             f'q{30 * k},{-8 * k} {60 * k},0" stroke="{P["foam"]}" stroke-width="{4 * k:.1f}" fill="none" '
             f'stroke-linecap="round"/>')
    return man + S.g(pole + hull, filter="wobble-fine") + water


def field(pts, col, stripes, seed=0):
    d = S.smooth_path(pts, closed=True, tension=0.35)
    out = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="2.5"/>'
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    cid = f"s15fld{seed}"
    rows = ""
    for i in range(1, stripes):
        u = i / stripes
        y = min(ys) + (max(ys) - min(ys)) * u
        rows += (f'<path d="M{min(xs) - 20},{f1(y)} L{max(xs) + 20},{f1(y + 6)}" stroke="{S.shade(col, -0.18)}" '
                 f'stroke-width="3" opacity="0.6"/>')
    return out + f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{rows}</g>'


def ground_body():
    defs = (S.lin_grad("s15gr", [(0, S.mix(P["sand_light"], P["sand"], 0.4)), (0.5, P["sand"]),
                                 (1, S.mix(P["sand"], P["grass"], 0.35))])
            + S.lin_grad("s15road", [(0, S.mix(P["sand_light"], "#fffaf0", 0.25)), (1, P["sand_light"])])
            + S.lin_grad("s15riv", [(0, S.mix(P["sea_light"], P["sky_day"], 0.3)), (0.45, P["sea"]),
                                    (1, P["sea_deep"])]))
    ground = (f'<path d="M-40,{SH + 40} L-40,{WALL_Y - 46} L{WALL_X0 - 240},{WALL_Y - 46} L{WALL_X0 - 50},'
              f'{WALL_Y - 4} L{WALL_X1 + 50},{WALL_Y - 4} L{WALL_X1 + 240},{WALL_Y - 46} L{SW + 40},{WALL_Y - 46} '
              f'L{SW + 40},{SH + 40} Z" fill="url(#s15gr)" stroke="{INK}" stroke-width="3"/>')
    fields = (field([(880, 1185), (1240, 1175), (1300, 1265), (900, 1285)], S.mix(P["grass"], P["sand"], 0.25), 5, 1)
              + field([(1420, 1180), (1900, 1172), (1980, 1270), (1460, 1290)], S.mix(P["leaf_light"], P["sand"],
                                                                                    0.3), 6, 2)
              + field([(1020, 1390), (1740, 1370), (1860, 1540), (1080, 1580)], S.mix(P["grass"], P["sand"], 0.15), 7,
                      3)
              + field([(2010, 1190), (2440, 1185), (2380, 1300), (2060, 1310)], S.mix(P["gold"], P["sand"], 0.55), 5,
                      4))
    road = S.path(road_path(), fill="url(#s15road)", sw=3)
    rng = random.Random(11)
    peb = ""
    for _ in range(36):
        u = rng.random()
        y = SH - u * (SH - WALL_Y - 40)
        x = 330 + (GX - 330) * u + rng.uniform(-80, 80) * (1 - u) + 160 * (1 - u)
        r = rng.uniform(3, 7) * (1.3 - 0.8 * u)
        peb += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r)}" fill="{P["sand_dark"]}" '
                f'opacity="0.5"/>')
    rd = S.smooth_path(RIVER_BANK, closed=False, tension=0.8) + f" L{SW + 40},{SH + 40} Z"
    river = S.path(rd, fill="url(#s15riv)", sw=3.5)
    hl = ""
    for x0, y0, ln in ((3000, 1175, 90), (2850, 1215, 120), (2700, 1290, 160), (2960, 1330, 150), (2600, 1420, 170),
                       (2850, 1470, 200), (2520, 1560, 160), (2750, 1620, 220), (3050, 1560, 180), (2450, 1720, 200),
                       (2900, 1730, 210)):
        hl += (f'<path d="M{x0},{y0} q{ln / 2},-7 {ln},0" stroke="{P["foam"]}" stroke-width="5" fill="none" '
               f'stroke-linecap="round" opacity="0.65"/>')
    body = S.g(ground + fields + road + peb + river + hl, filter="wobble", extra="")
    deco = ""
    # farmhouses, palms, bushes, reeds, sheep, a resting camel and its owner
    deco += PR.house(1560, 1200, 0.2, 0) + PR.house(1700, 1206, 0.18, 3, facing=-1)
    for x, y, s, ln in ((860, 1190, 0.36, 0.2), (930, 1200, 0.32, -0.1), (2140, 1250, 0.42, -0.2),
                        (2260, 1215, 0.36, 0.15), (2600, 1170, 0.3, 0.1), (2470, 1195, 0.33, -0.25),
                        (380, 1210, 0.4, -0.1), (300, 1230, 0.34, 0.2)):
        deco += PR.palm_tree(x, y, s, lean=ln)
    for x, y, s, v in ((520, 1250, 0.4, 2), (820, 1330, 0.45, 0), (1350, 1340, 0.42, 1), (2000, 1380, 0.5, 0),
                       (1250, 1215, 0.32, 2), (2280, 1400, 0.55, 3)):
        deco += PR.bush(x, y, s, v)
    for x, y, s in ((2560, 1365, 0.42), (2430, 1500, 0.5), (2360, 1660, 0.58), (2700, 1250, 0.36),
                    (2860, 1195, 0.3)):
        deco += PR.reeds(x, y, s)
    for x, y, s, f in ((1240, 1470, 0.3, 1), (1330, 1490, 0.27, -1), (1450, 1460, 0.28, 1), (1560, 1505, 0.3, -1)):
        deco += C.ground_shadow(x, y, s, 140) + PR.animal(x, y, s, f, kind="sheep")
    deco += C.ground_shadow(2140, 1500, 0.36, 300) + PR.animal(2140, 1500, 0.36, -1, kind="camel")
    deco += C.ground_shadow(2030, 1512, 0.36, 110) + C.citizen(2030, 1512, 0.36, 1, kind="man", variant=2)
    for x, y, s, v in ((200, 1500, 0.8, 1), (600, 1460, 0.7, 2), (980, 1640, 0.8, 0), (1500, 1680, 0.9, 1),
                       (1900, 1620, 0.8, 2), (700, 1700, 0.9, 0), (1200, 1760, 1.0, 2)):
        deco += PR.grass_tuft(x, y, s, v)
    rocks = ""
    for x, y, rx, ry, seed in ((880, 1500, 40, 22, 1), (930, 1512, 22, 13, 2), (430, 1660, 38, 20, 3)):
        rocks += S.path(S.blob(x, y, rx, ry, 0.15, 8, seed), fill=P["stone_dark"], sw=3)
    return body + deco + S.g(rocks, filter="wobble-fine"), defs


def river_glints_svg(phase):
    rng = random.Random(40 + phase)
    body = ""
    for _ in range(16):
        y = rng.uniform(1180, 1780)
        u = (y - 1128) / (SH - 1128)
        xl = 2980 - (2980 - 2340) * min(1, u * 1.25)
        x = rng.uniform(xl + 60, SW - 60)
        ln = rng.uniform(22, 50) * (0.6 + 0.6 * u)
        body += (f'<path d="M{f1(x)},{f1(y)} l{f1(ln)},0" stroke="#fffaf0" stroke-width="{3 + 3 * u:.1f}" '
                 f'stroke-linecap="round" opacity="0.85"/>')
    return doc(body)


def boats_svg():
    return doc(boat(2780, 1310, 0.5, -1, 3) + boat(2620, 1600, 0.68, 1, 1))


def doves_svg(k_, pts):
    body = ""
    for j, (x, y, s) in enumerate(pts):
        w = (1.0, 0.0, -1.0)[(k_ + j) % 3]
        body += PR.dove(x, y, s, 1, wing=w)
    return doc(body)


# ---------------------------------------------------------------- the three-days device


def trail_points(n_per=None):
    """Footprints along the trail polyline: list of (x, y, angle_deg, side)."""
    d = S.smooth_path(TRAIL, closed=False, tension=0.9)
    # sample the Catmull-Rom curve densely
    pts = []
    n = len(TRAIL)
    for i in range(n - 1):
        p0 = TRAIL[max(0, i - 1)]
        p1, p2 = TRAIL[i], TRAIL[i + 1]
        p3 = TRAIL[min(n - 1, i + 2)]
        for j in range(40):
            u = j / 40
            u2, u3 = u * u, u * u * u
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)
            pts.append((x, y))
    pts.append(TRAIL[-1])
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return d, pts, cum


def point_at(frac):
    _, pts, cum = trail_points()
    target = frac * cum[-1]
    for i in range(1, len(cum)):
        if cum[i] >= target:
            u = (target - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
            a, b = pts[i - 1], pts[i]
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u,
                    math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
    return (*pts[-1], 0.0)


def footprint(x, y, ang, side, s=1.0):
    """One little sandal print (local: toes toward +x), offset sideways by side."""
    a = math.radians(ang)
    ox, oy = -math.sin(a) * 9 * side * s, math.cos(a) * 9 * side * s
    return (f'<g transform="translate({f1(x + ox)},{f1(y + oy)}) rotate({ang:.1f}) scale({s:.3f})">'
            f'<ellipse cx="4" cy="0" rx="11" ry="6.2" fill="{P["ink_soft"]}"/>'
            f'<ellipse cx="-10" cy="0" rx="5.5" ry="4.6" fill="{P["ink_soft"]}"/></g>')


def trail_svg():
    d, pts, cum = trail_points()
    ribbon = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="66" stroke-linecap="round" '
              f'stroke-linejoin="round" opacity="0.55"/>'
              f'<path d="{d}" fill="none" stroke="#fff4dc" stroke-width="58" stroke-linecap="round" '
              f'stroke-linejoin="round"/>')
    prints = ""
    L = cum[-1]
    n = int(L / 44)
    for i in range(1, n):
        x, y, ang = point_at(i / n)
        prints += footprint(x, y, ang, 1 if i % 2 else -1, 1.45)
    return doc(S.g(ribbon, filter="wobble") + S.g(prints, filter="wobble-fine"))


TRAIL_X0 = TRAIL[0][0] - 38          # approx. alpha bbox of the trail layer (for its 'left' reveal)
TRAIL_X1 = TRAIL[-1][0] + 38


def sun_icon(x, y, r, num):
    ink = INK
    rays = ""
    for i in range(12):
        a = math.radians(i * 30)
        r0, r1 = r * 1.18, r * (1.55 if i % 2 == 0 else 1.42)
        rays += (f'<path d="M{f1(x + r0 * math.cos(a))},{f1(y + r0 * math.sin(a))} '
                 f'L{f1(x + r1 * math.cos(a))},{f1(y + r1 * math.sin(a))}" stroke="{P["sun_hot"]}" '
                 f'stroke-width="{r * 0.16:.1f}" stroke-linecap="round"/>')
    face = (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="{P["sun"]}" stroke="{ink}" stroke-width="5"/>'
            f'<circle cx="{f1(x - r * 0.3)}" cy="{f1(y - r * 0.12)}" r="{r * 0.09:.1f}" fill="{ink}"/>'
            f'<circle cx="{f1(x + r * 0.3)}" cy="{f1(y - r * 0.12)}" r="{r * 0.09:.1f}" fill="{ink}"/>'
            f'<ellipse cx="{f1(x - r * 0.52)}" cy="{f1(y + r * 0.18)}" rx="{r * 0.15:.1f}" ry="{r * 0.09:.1f}" '
            f'fill="{P["cheek"]}" opacity="0.8"/>'
            f'<ellipse cx="{f1(x + r * 0.52)}" cy="{f1(y + r * 0.18)}" rx="{r * 0.15:.1f}" ry="{r * 0.09:.1f}" '
            f'fill="{P["cheek"]}" opacity="0.8"/>'
            f'<path d="M{f1(x - r * 0.28)},{f1(y + r * 0.22)} Q{f1(x)},{f1(y + r * 0.5)} {f1(x + r * 0.28)},'
            f'{f1(y + r * 0.22)}" stroke="{ink}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    badge_y = y + r * 2.05
    badge = (f'<circle cx="{f1(x)}" cy="{f1(badge_y)}" r="{r * 0.62:.1f}" fill="#fff6e2" stroke="{ink}" '
             f'stroke-width="4.5"/>'
             + S.text(f1(x), f1(badge_y + r * 0.27), str(num), size=int(r * 0.8), fill=INK))
    return S.g(rays + face, filter="wobble-fine") + badge


# ================================================================ inside: drawing


def sky_grad(id_, stops, y0=470, y1=1000):
    """Vertical gradient in stage coordinates (the street camera only ever sees y ~470..1000 of the sky)."""
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="0" y1="{y0}" x2="0" y2="{y1}">{st}</linearGradient>'


def street_sky_svg():
    defs = sky_grad("s15ssky", [(0, P["sky_day_top"]), (0.35, P["sky_day"]),
                                (0.7, S.mix(P["sky_day"], P["sky_warm"], 0.6)), (1, P["sky_warm"])])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOT + 20}" fill="url(#s15ssky)"/>', defs)


def street_sky_eve_svg():
    """Warm late-afternoon sky wash (fades in over the noon sky as the day goes by)."""
    defs = sky_grad("s15esky", [(0, S.mix(P["sky_day_top"], P["sky_dawn_top"], 0.6)),
                                (0.4, S.mix(P["sky_dawn"], P["sky_day"], 0.3)),
                                (0.75, S.mix(P["sky_dawn"], P["sky_warm"], 0.5)), (1, P["sky_warm"])])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOT + 20}" fill="url(#s15esky)"/>', defs)


def sun_svg(x, y):
    defs = S.rad_grad("s15sung", [(0, "#fff6d8", 0.95), (0.35, "#ffe9a8", 0.45), (1, "#ffe9a8", 0)])
    rays = ""
    for i in range(12):
        a = math.radians(i * 30 + 15)
        r0, r1 = 72, (98 if i % 2 == 0 else 88)
        rays += (f'<path d="M{f1(x + r0 * math.cos(a))},{f1(y + r0 * math.sin(a))} L{f1(x + r1 * math.cos(a))},'
                 f'{f1(y + r1 * math.sin(a))}" stroke="{P["sun_hot"]}" stroke-width="9" stroke-linecap="round" '
                 f'opacity="0.75"/>')
    body = (f'<circle cx="{x}" cy="{y}" r="220" fill="url(#s15sung)"/>' + rays +
            f'<circle cx="{x}" cy="{y}" r="58" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.2)}" '
            f'stroke-width="4"/>'
            f'<circle cx="{x - 14}" cy="{y - 16}" r="22" fill="#fff2c0" opacity="0.7"/>')
    return doc(body, defs)


def street_far_svg():
    body = PR.nineveh_skyline(-300, SW + 300, 1030, scale=1.05, seed=31, haze=0.5)
    return doc(body)


def laundry(x0, x1, y, sag, cols, seed=0, phase=0):
    """A line strung between two houses with cloths hanging from it (phase: flutter drawing 0/1)."""
    rng = random.Random(seed)
    mx = (x0 + x1) / 2
    out = (f'<path d="M{x0},{y} Q{mx},{y + 2 * sag} {x1},{y}" stroke="{P["ink_soft"]}" stroke-width="3" '
           f'fill="none"/>')
    n = len(cols)
    for i, c in enumerate(cols):
        u = (i + 0.7) / (n + 0.4)
        x = x0 + (x1 - x0) * u
        yy = y + 2 * sag * 2 * u * (1 - u) * 2 * 0.5 + sag * 0.0
        yy = y + 4 * sag * u * (1 - u)
        w = rng.uniform(42, 60)
        h = rng.uniform(52, 76)
        sk = (6 if (i + phase) % 2 else -6)
        out += (f'<path d="M{f1(x - w / 2)},{f1(yy)} L{f1(x + w / 2)},{f1(yy)} L{f1(x + w / 2 + sk)},{f1(yy + h)} '
                f'Q{f1(x + sk)},{f1(yy + h + 8)} {f1(x - w / 2 + sk)},{f1(yy + h)} Z" fill="{c}" stroke="{INK}" '
                f'stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M{f1(x - w / 2 + 3)},{f1(yy + 12)} L{f1(x + w / 2 + sk * 0.3)},{f1(yy + 12)}" '
                f'stroke="{S.shade(c, -0.2)}" stroke-width="3" opacity="0.6"/>')
    return S.g(out, filter="wobble-fine")


LAUNDRY = [(330, 640, 905, 26, (P["jonah_sash"], "#f4e3b0", P["terracotta"]), 1),
           (1035, 1340, 930, 22, (P["royal_light"], P["gold"]), 2)]


def street_back_svg(shadows=""):
    """Street floor, the back row of flat-roofed houses, palms, doorstep props and the market stalls."""
    defs = S.lin_grad("s15plaza", [(0, S.mix(P["sand_light"], P["stone_light"], 0.5)), (0.3, P["sand_light"]),
                                   (1, S.mix(P["sand"], P["sand_light"], 0.25))])
    floor = (f'<rect x="-40" y="{BACK_Y - 30}" width="{SW + 80}" height="{SH}" fill="url(#s15plaza)" '
             f'stroke="{INK}" stroke-width="3"/>')
    pav = ""
    rows = (1140, 1166, 1196, 1232, 1274, 1322, 1376, 1436, 1504, 1580)
    for i, yy in enumerate(rows):
        pav += (f'<path d="M-40,{yy} L{SW + 40},{yy}" stroke="{P["sand_dark"]}" stroke-width="2" '
                f'opacity="{0.22 + i * 0.025:.2f}"/>')
    rng = random.Random(7)
    for _ in range(230):
        i = rng.randrange(len(rows) - 1)
        yy, h = rows[i], rows[i + 1] - rows[i]
        x = rng.uniform(-40, SW + 40)
        pav += (f'<path d="M{f1(x)},{yy} l{f1(rng.uniform(-5, 5))},{h}" stroke="{P["sand_dark"]}" stroke-width="2" '
                f'opacity="0.26"/>')
    houses = ""
    for x, v, s, f in ((120, 3, 0.5, 1), (480, 1, 0.5, 1), (860, 0, 0.52, 1), (1200, 2, 0.5, -1), (1560, 3, 0.5, 1),
                       (1980, 1, 0.52, -1), (2380, 2, 0.5, 1), (2760, 0, 0.52, -1), (3120, 1, 0.5, 1)):
        houses += PR.house(x, BACK_Y, s, v, facing=f)
    palms = ""
    for x, s, ln in ((690, 0.62, 0.15), (1395, 0.66, -0.12), (2190, 0.64, 0.1), (2950, 0.6, -0.15)):
        palms += PR.palm_tree(x, BACK_Y + 8, s, lean=ln)
    props = ""
    for x, y, s in ((300, BACK_Y + 20, 0.42), (338, BACK_Y + 26, 0.34), (1040, BACK_Y + 22, 0.4),
                    (1720, BACK_Y + 18, 0.38), (2560, BACK_Y + 24, 0.4)):
        props += PR.jar(x, y - 30 * s / 0.4, s)
    props += PR.sack(940, BACK_Y + 30, 0.42, seed=3) + PR.sack(975, BACK_Y + 34, 0.34, seed=5)
    props += PR.bush(1110, BACK_Y + 26, 0.45, 1) + PR.bush(2080, BACK_Y + 30, 0.45, 3)
    doves = (PR.dove(455, BACK_Y - 0.5 * 845 - 16, 0.42, 1, pose="stand")
             + PR.dove(1150, BACK_Y - 0.5 * 524 - 16, 0.4, -1, pose="stand")
             + PR.dove(2420, BACK_Y - 0.5 * 524 - 16, 0.42, 1, pose="stand"))
    stalls = (V.stall(1520, 1176, 220, 0.9, P["jonah_sash"], "pots", 1)
              + V.stall(2330, 1172, 240, 0.9, P["terracotta"], "fruit", 2)
              + V.stall(2760, 1180, 220, 0.9, P["royal_light"], "cloth", 3))
    extra = PR.jar(2460, 1150, 0.4) + PR.jar(2496, 1156, 0.34) + PR.crate(1640, 1160, 0.4)
    body = S.g(floor + pav, filter="wobble") + houses + palms + props + doves + stalls + extra + shadows
    return doc(body, defs)


def step_svg():
    """v1's two-tier stone step with a glazed rosette band (Jonah preaches from it)."""
    x, y = STEP_X, STEP_Y
    st, stl, std = P["stone"], P["stone_light"], P["stone_dark"]
    out = (f'<path d="M{x - 190},{y - 34} L{x + 190},{y - 34} L{x + 214},{y - 50} L{x - 166},{y - 50} Z" '
           f'fill="{stl}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
           f'<rect x="{x - 190}" y="{y - 34}" width="380" height="34" fill="{st}" stroke="{INK}" stroke-width="4"/>'
           f'<path d="M{x + 190},{y} L{x + 214},{y - 16} L{x + 214},{y - 50} L{x + 190},{y - 34} Z" fill="{std}" '
           f'stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    y2 = y - 34
    out += (f'<path d="M{x - 130},{y2 - 28} L{x + 130},{y2 - 28} L{x + 150},{y2 - 42} L{x - 110},{y2 - 42} Z" '
            f'fill="{stl}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{x - 130}" y="{y2 - 28}" width="260" height="28" fill="{st}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{x + 130},{y2} L{x + 150},{y2 - 14} L{x + 150},{y2 - 42} L{x + 130},{y2 - 28} Z" '
            f'fill="{std}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    band = f'<rect x="{x - 186}" y="{y - 24}" width="372" height="16" fill="#4f86b0" stroke="{INK}" stroke-width="2.5"/>'
    for i in range(11):
        cx = x - 170 + i * 34
        band += (f'<circle cx="{cx}" cy="{y - 16}" r="5" fill="#f4e3b0"/><circle cx="{cx}" cy="{y - 16}" r="2" '
                 f'fill="{P["crown"]}"/>')
    shadow = f'<ellipse cx="{x + 20}" cy="{y + 4}" rx="230" ry="16" fill="{INK}" opacity="0.18" filter="url(#soft)"/>'
    return doc(shadow + S.g(out + band, filter="wobble-fine"))


def street_fg_svg():
    """Near things along the bottom edge (they slide by a little faster than the street; drawn for the final
    market framing, shifted with the camera)."""
    body = ""
    body += PR.jar(1255, 1470, 0.85) + PR.jar(1330, 1494, 0.66, color=S.mix(P["terracotta"], P["sand"], 0.35))
    body += PR.grass_tuft(1190, 1520, 1.1, 2)
    body += PR.sack(620, 1530, 0.9, seed=7) + PR.jar(720, 1500, 0.8) + PR.grass_tuft(800, 1530, 1.0, 0)
    body += PR.bush(2880, 1530, 1.05, 1) + PR.grass_tuft(2790, 1525, 1.1, 2)
    return doc(body)


def exclaim(x, y, s=1.0):
    pts = []
    for i in range(16):
        r = (40 if i % 2 == 0 else 29) * s
        a = math.radians(i * 22.5)
        pts.append((x + 3 * s + r * math.cos(a), y - 14 * s + r * 1.12 * math.sin(a)))
    burst = ('<path d="M' + " L".join(f"{f1(px)},{f1(py)}" for px, py in pts) + f' Z" fill="#fff6dc" '
             f'stroke="{INK}" stroke-width="{3.5 * s}" stroke-linejoin="round"/>')
    body = burst + (f'<path d="M{x},{y - 40 * s} L{x + 3 * s},{y - 4 * s}" stroke="{INK}" stroke-width="{9 * s}" '
                    f'stroke-linecap="round"/>'
                    f'<circle cx="{x + 5 * s}" cy="{y + 12 * s}" r="{5.5 * s}" fill="{INK}"/>')
    return S.g(body, filter="wobble-fine")


def arcs(cx, cy, n, facing=1, k=1.0):
    body = ""
    for i in range(n):
        r = (44 + i * 30) * k
        a0, a1 = math.radians(-38), math.radians(38)
        x0, y0 = cx + facing * r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + facing * r * math.cos(a1), cy + r * math.sin(a1)
        sweep = 1 if facing > 0 else 0
        body += (f'<path d="M{f1(x0)},{f1(y0)} A{r},{r} 0 0 {sweep} {f1(x1)},{f1(y1)}" fill="none" '
                 f'stroke="#fff6e2" stroke-width="{15 * k:.1f}" stroke-linecap="round" opacity="0.8"/>')
    for i in range(n):
        r = (44 + i * 30) * k
        a0, a1 = math.radians(-38), math.radians(38)
        x0, y0 = cx + facing * r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + facing * r * math.cos(a1), cy + r * math.sin(a1)
        sweep = 1 if facing > 0 else 0
        body += (f'<path d="M{f1(x0)},{f1(y0)} A{r},{r} 0 0 {sweep} {f1(x1)},{f1(y1)}" fill="none" '
                 f'stroke="{INK}" stroke-width="{7 * k:.1f}" stroke-linecap="round" opacity="{0.95 - i * 0.12:.2f}"/>')
    return S.g(body, filter="wobble-fine")


# ================================================================ effects


def light_fx(col_fn):
    """Multiply the whole frame by a time-varying colour (rosy morning -> white noon -> golden afternoon)."""
    def fx(frame, t, view):
        c = col_fn(t)
        if min(c) >= 254.5:
            return frame
        arr = np.asarray(frame)
        out = cv2.multiply(arr, (float(c[0]), float(c[1]), float(c[2]), 255.0), scale=1 / 255.0)
        return Image.fromarray(out, "RGBA")
    return fx


# ================================================================ build


def build(ctx):
    _SPRITES.clear()
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.line(0), ctx.line(1), ctx.line(2)
    d2 = L2.end - L2.start
    part = M.progress

    # ------------------------------------------------------------ key times (all from the narration)
    t_pull0 = max(1.05, L0.start + 0.15)              # "尼尼微是一座非常非常大的城": pull back
    cB = L0.at("要走")                                 # "要走整整三天，才能走遍整座城。"
    cB_end = next(c.end for c in L0.chunks if "要走" in c.text)
    dB = cB_end - cB
    t_wide = cB - 0.05                                # the whole city is on the page
    t_trail0, t_trail1 = cB + 0.08, cB + 0.40 * dB    # the footprint trail walks across the city
    sun_fr = (1 / 3, 2 / 3, 1.0)                      # suns at each third of the way
    t_push0 = L0.end - 0.6                            # trail fades, camera heads for the west gate
    t_fly0 = L1.start + 0.12                          # "约拿进了城": fly through the gate
    t_fly1 = t_fly0 + 0.78
    t_st = t_fly0 + 0.62                              # the street framing is reached
    t_call = L1.at("一边大声喊")                        # "一边大声喊": arm up, calling while walking
    t_calloff = L1.end + 0.1
    t_stop = L2.start - 0.3                           # he has walked up onto the step and stops
    TAU = 0.5                                         # ...slowing down over the last stride
    t_dec = t_stop - TAU
    t_preach = L2.start                               # "再过四十天，尼尼微就要毁灭了！"
    t_phr2 = L2.start + 0.31 * d2                     # (after the comma) "尼尼微就要毁灭了"
    t_turn = L2.start + 0.22                          # people stop and turn
    t_wow = t_turn + 0.18
    t_worry = t_phr2 + 0.45
    t_down = L2.end + 0.12                            # arm down: calm ending

    # ------------------------------------------------------------ Jonah's street walk (distance-driven)
    X_IN = 700.0                                      # where he is (just inside the gate) when the fly starts
    STEP_X0, STEP_X1 = STEP_X - 175, STEP_X - 92      # he climbs the two tiers between these x
    D_TOT = JX_STOP - X_IN
    V_W = D_TOT / (t_stop - t_fly0 - TAU / 2)         # walking speed (stage px / s)
    N_END = int(D_TOT / ADV)

    def walk_dist(t):
        if t <= t_dec:
            return max(0.0, t - t_fly0) * V_W
        u = min(t, t_stop) - t_dec
        return (t_dec - t_fly0) * V_W + V_W * (u - u * u / (2 * TAU))

    def walk_k(t):
        return min(N_END, int(walk_dist(t) / ADV + 1e-6))

    def jonah_x(t):
        return X_IN + walk_k(t) * ADV

    def ground_at(x):
        """Street line, then up the two tiers of the step."""
        u = min(1.0, max(0.0, (x - STEP_X0) / (STEP_X1 - STEP_X0)))
        return GY + (STEP_TOP - GY) * (0.5 - 0.5 * math.cos(math.pi * u))

    def jonah_ground(t):
        return ground_at(jonah_x(t))

    # ------------------------------------------------------------ camera
    CAM0 = Cam(820, 1128, 1560)
    CAMW = Cam(1600, 900, 3180)
    CAM_HOLD = Cam(1585, 905, 3110)
    CAM_GATE = Cam(CAM_ST0.x, 975, CAM_ST0.w)
    CAM_END0 = Cam(1900, 985, 1760)
    t_endcam = L2.start + 0.9

    RAMP = 1.5                                         # the tracking camera eases up to walking speed

    def cam_track_x(t):
        u = min(1.0, max(0.0, (t - t_st) / RAMP))
        dist = RAMP * (u ** 3 - 0.5 * u ** 4) + max(0.0, t - t_st - RAMP)
        return CAM_ST0.x + V_W * dist

    out_cam = M.cam_keys([(0, CAM0), (t_pull0, CAM0), (t_wide, CAMW), (t_push0, CAM_HOLD), (t_fly0, CAM_GATE),
                          (t_st, CAM_ST0)], "sine")
    x_hopcam = cam_track_x(t_dec)
    CAM_END = Cam(max(CAM_END0.x, x_hopcam + 0.4 * V_W * (t_endcam - t_dec)), CAM_END0.y, CAM_END0.w)

    def camf(t):
        if t < t_st:
            return out_cam(t)
        if t < t_dec:
            u = part(t, t_st, t_dec, "sine")
            return Cam(cam_track_x(t), M.lerp(CAM_ST0.y, 995, u), M.lerp(CAM_ST0.w, 1790, u))
        # glide from walking speed to rest on the market framing (Hermite: no velocity jump, no reversal)
        D = t_endcam - t_dec
        u = min(1.0, (t - t_dec) / D)
        h01 = 3 * u * u - 2 * u ** 3
        h10 = u ** 3 - 2 * u * u + u
        x = x_hopcam * (1 - h01) + CAM_END.x * h01 + V_W * D * h10
        y = M.lerp(995, CAM_END.y, part(t, t_dec, t_endcam, "sine"))
        w = M.lerp(1790, CAM_END.w, part(t, t_dec, t_endcam, "sine"))
        v = part(t, t_endcam, T, "sine")       # a very slow settle to the end
        return Cam(x + 12 * v, y - 4 * v, w - 40 * v)
    sc.camera = camf

    # ------------------------------------------------------------ fly-through (v1 technique)
    a_, b_ = HOLE_CLEAR[0], HOLE_CLEAR[1]
    c_, d_ = CAM_ST0.x - CAM_ST0.w / 2, CAM_ST0.x + CAM_ST0.w / 2
    fpx = (a_ * d_ - c_ * b_) / (d_ + a_ - b_ - c_)
    ys_, yb_ = HOLE_CLEAR[2], HOLE_CLEAR[3]
    vy0, vy1 = CAM_ST0.y - CAM_ST0.w * 9 / 32, CAM_ST0.y + CAM_ST0.w * 9 / 32
    fpy = (ys_ * vy1 - vy0 * yb_) / (vy1 + ys_ - yb_ - vy0)
    FLY_C = (fpx, fpy)
    s_fly = lambda t: 1 + 21.0 * part(t, t_fly0, t_fly1, "in")

    def covers(cam, s):
        hx0, hx1, hs, hb = HOLE_CLEAR
        px, py = FLY_C
        vx0, vx1 = cam.x - cam.w / 2, cam.x + cam.w / 2
        vy0_, vy1_ = cam.y - cam.w * 9 / 32, cam.y + cam.w * 9 / 32
        return (px + s * (hx0 - px) <= vx0 - 4 and px + s * (hx1 - px) >= vx1 + 4
                and py + s * (hs - py) <= vy0_ - 4 and py + s * (hb - py) >= vy1_ + 4)
    t_cut = t_fly1
    kk = 0
    while t_fly0 + kk / 120 < t_fly1:
        tt = t_fly0 + kk / 120
        if covers(camf(tt), s_fly(tt)):
            t_cut = tt
            break
        kk += 1
    out_a = lambda t: 1.0 if t < t_cut else 0.0
    in_a = lambda t: 1.0 if t >= t_fly0 - 0.02 else 0.0

    def F(local=None, pivot=FLY_C):
        return V.fly(local, pivot, FLY_C, s_fly, out_a)

    # ============================================================ INSIDE (behind the outside layers)
    # sky, the day's sun, clouds, hazy far city
    sc.add("st_sky", street_sky_svg(), z=1, wc=0.6, motion=lambda t: Tf(alpha=in_a(t)))
    eve = lambda t: part(t, t_call - 1.2, t_calloff + 0.4, "sine")
    sc.add("st_sky_eve", street_sky_eve_svg(), z=1.05, wc=0.6, motion=lambda t: Tf(alpha=0.9 * eve(t) * in_a(t)))
    SUN0 = (CAM_ST0.x, 620)

    sun_rel = keyed([(t_st - 0.3, -880), (L1.end + 0.3, 600), (T, 660)], "linear")

    def sun_pos(t):
        """The sun's arc over the street, relative to the camera: rises on the left, sets on the right."""
        rx = sun_rel(t)
        ry = 92 + 0.00017 * rx * rx            # a flat arc: high at the centre, low at the sides
        c = camf(max(t, t_st))
        return c.x + rx, c.y - c.w * 9 / 32 + ry
    sc.add("st_sun", sun_svg(*SUN0), z=1.2, wc=0,
           motion=lambda t: Tf(dx=sun_pos(t)[0] - SUN0[0], dy=sun_pos(t)[1] - SUN0[1], rot=3.0 * t,
                               px=SUN0[0], py=SUN0[1], alpha=in_a(t)))
    cl_par = lambda k: (lambda t: Tf(dx=k * (camf(max(t, t_st)).x - CAM_ST0.x)))
    sc.add("st_clouds", pano_clouds_svg([(640, 600, 250, 70, 31), (1420, 578, 210, 60, 33), (2250, 612, 270, 76, 35),
                                         (3000, 586, 220, 62, 37), (3600, 600, 240, 66, 39)]), z=1.4,
           motion=M.combine(M.drift(vx=9), cl_par(0.6), lambda t: Tf(alpha=in_a(t))))
    sc.add("st_far", street_far_svg(), z=1.6, wc=0.8,
           motion=M.combine(cl_par(0.4), lambda t: Tf(alpha=in_a(t))))

    for i, (x0, x1, y, sag, cols, seed) in enumerate(LAUNDRY):
        frames = [doc(laundry(x0, x1, y, sag, cols, seed, ph)) for ph in (0, 1)]
        sc.add(f"laundry{i}", frames, z=2.2, frame_at=lambda t, i=i: float(int(t * 2.6 + i) % 2),
               motion=lambda t: Tf(alpha=in_a(t)))

    # ------------------------------------------------------------ people (sprites)
    people_heads = {}
    static_shadows = []

    def walker_frames(sp, s, kind, variant, face, expr=None):
        return (sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose="walk_a", expr=expr)),
                sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose="walk_b", expr=expr)))

    def person(name, kind, variant, x, y, s, face, z, walk=None, period=0.4, idle=None, events=(), hops=(),
               shadow=True, seed=0):
        """A townsperson sprite. walk=(x_from, t_a, t_b): stands at x_from until t_a, walks (walk_a/walk_b every
        ``period`` s) to x by t_b. idle=(pose, expr, period): alternate stand / pose while waiting.
        events: [(t, facing, pose, expr)] hard pose cuts, each sold by a little hop (and hops: extra hop times)."""
        sp = person_sprite(s, seed=seed + variant * 7)
        stand0 = sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose="stand"))
        entries = [(0, stand0)]
        if idle:
            alt = sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose=idle[0], expr=idle[1]))
            entries = [(0, ("alt", stand0, alt, idle[2]))]
        if walk:
            wa, wb = walker_frames(sp, s, kind, variant, face)
            entries += [(walk[1], ("alt", wa, wb, period)), (walk[2], entries[0][1])]
        hop_ts = list(hops)
        last_face = face
        for (te, fc, pose, expr) in events:
            entries.append((te, sp.add(C.citizen(sp.ax, sp.ay, s, fc, kind=kind, variant=variant, pose=pose,
                                                 expr=expr))))
            hop_ts.append(te)
            last_face = fc
        idx_f = V.sched(entries)

        def xpos(t):
            if not walk:
                return x
            return M.lerp(walk[0], x, part(t, walk[1], walk[2], "linear"))

        def fn(t):
            if t < t_fly0 - 0.02:
                return None
            sy, dy = 1 + 0.012 * math.sin(2 * math.pi * (t / (2.8 + variant * 0.3) + variant * 0.17)), 0.0
            if idle and idle[0] == "cheer" and not any(t >= ev[0] for ev in events):
                ph = t / idle[2]
                if int(ph) % 2 == 1:                  # arms up: a little jump of joy
                    dy -= 18 * s * math.sin(math.pi * (ph % 1.0))
            for th in hop_ts:
                u = t - th
                if -0.08 <= u <= 0.3:
                    if u < 0:
                        sy *= 1 - 0.05 * part(u, -0.08, 0, "sine")
                    else:
                        sy *= 1 - 0.05 * (1 - part(u, 0, 0.1, "sine")) + 0.03 * math.sin(math.pi * min(1, u / 0.3))
                        dy -= 16 * s * math.sin(math.pi * min(1.0, u / 0.3))
            return sp.place(idx_f(t), xpos(t), y, sx=1 / math.sqrt(sy), sy=sy, dy=dy)
        if shadow and not walk:
            static_shadows.append(C.ground_shadow(x, y, s, 80 if kind == "child" else 110))
        elif shadow:
            shs = sprite(260 * s + 40, 70 * s + 30, 130 * s + 20, 35 * s + 15, wc=0)
            shi = shs.add(C.ground_shadow(shs.ax, shs.ay, s, 80 if kind == "child" else 110))
            sc.add_dynamic(name + "_sh", lambda t: shs.place(shi, xpos(t), y) if t >= t_fly0 - 0.02 else None,
                           z=z - 0.01)
        sc.add_dynamic(name, fn, z=z)
        hp = C.body_points(C.citizen, x, y, s, last_face, kind=kind, variant=variant, pose="stand")["head_top"]
        people_heads[name] = hp
        return hp

    # street: children playing by a doorway, a donkey, an old man at his door, a woman walking the other way
    person("kid0", "child", 0, 360, 1196, 0.6, 1, 3.1, idle=("cheer", "happy", 0.45), seed=1)
    person("kid1", "child", 1, 432, 1204, 0.58, -1, 3.12, idle=("cheer", "happy", 0.52), seed=2)
    person("elder_door", "elder", 1, 905, 1172, 0.58, -1, 3.0, seed=3,
           events=[(t_call + 0.3, -1, "stand", "surprised")])
    person("w_walk", "woman", 1, 1080, 1186, 0.62, -1, 3.2, walk=(1900, t_fly0, t_call + 0.15), period=0.3, seed=4,
           events=[(t_call + 0.25, 1, "stand", "surprised"), (t_call + 1.1, 1, "listen", None)])
    # market back row: a vendor by his pots, a boy at the fruit stall, a stroller
    person("vendor", "man", 2, 1395, 1188, 0.6, 1, 3.3, idle=("point", None, 1.6), seed=5,
           events=[(t_turn + 0.05, 1, "stand", "surprised"), (t_worry + 0.2, 1, "listen", None)])
    person("boy_fruit", "child", 2, 2250, 1200, 0.62, 1, 3.32, seed=6,
           events=[(t_turn + 0.1, -1, "stand", "surprised")])
    person("stroller", "man", 1, 2080, 1214, 0.62, 1, 3.34, walk=(1560, t_fly0 + 1.9, t_call + 0.5), period=0.38,
           seed=7, events=[(t_turn, -1, "stand", "surprised"), (t_worry, -1, "listen", None)])
    # a woman watching the market, a little behind Jonah's path (he walks past in front of her)
    person("woman_fl", "woman", 3, 1330, 1238, 0.7, 1, 3.6, seed=18, idle=("listen", "neutral", 1.4),
           events=[(t_call + 0.55, 1, "stand", "surprised"), (t_turn + 0.12, 1, "stand", "surprised"),
                   (t_worry + 0.05, 1, "listen", None)])

    sc.add("st_back", street_back_svg("".join(static_shadows)), z=2, motion=lambda t: Tf(alpha=in_a(t)))
    sc.add("step", step_svg(), z=4, motion=lambda t: Tf(alpha=in_a(t)))

    # ------------------------------------------------------------ Jonah (street)
    JSPR = person_sprite(JS, wide=190, tall=380, seed=91)
    with extra_exprs():
        F_WALK = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k), "neutral")) for k in range(2 * WALK_N)]
        F_MID = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "mid"), "call")) for k in range(2 * WALK_N)]
        F_UPC = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "up"), "call")) for k in range(2 * WALK_N)]
        F_UPS = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "up"), "shout")) for k in range(2 * WALK_N)]
        F_STAND = JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, STAND, "serious"))
        F_PRC = JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, PREACH, "call"))
        F_PRS = JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, PREACH, "shout"))
        F_END = F_STAND
    k_call_up = walk_k(t_call) + 2           # arm goes up over two drawings
    k_call_dn = walk_k(t_calloff)

    def mouth(t, t0, per=0.19):
        return int(max(0.0, t - t0) / per) % 2 == 1

    def j_frame(t):
        if t < t_stop:
            k = walk_k(t)
            km = k % (2 * WALK_N)
            if t < t_call or k >= k_call_dn + 2:
                return F_WALK[km]
            if k < k_call_up or k >= k_call_dn:
                return F_MID[km]
            return F_UPS[km] if mouth(t, t_call + 0.1) else F_UPC[km]
        if t < t_preach:
            return F_STAND
        if t < t_down:
            if t_phr2 - 0.1 <= t < t_phr2 + 0.08:
                return F_PRC
            if t >= L2.end - 0.04:
                return F_PRC
            return F_PRS if mouth(t, t_preach + 0.04) else F_PRC
        return F_END

    hops = [(t_stop, 0.7, False), (t_preach, 0.5, True), (t_down, 0.6, True)]

    def j_squash(t):
        sy, dy = 1.0, 0.0
        for ts, amp, up in hops:
            u = t - ts
            if -0.09 <= u <= 0.2:
                if u < 0:
                    sy = 1 - 0.05 * amp * part(u, -0.09, 0, "sine")
                elif u < 0.07:
                    sy = 1 - 0.05 * amp + 0.09 * amp * part(u, 0, 0.07, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * part(u, 0.07, 0.2, "sine")
                if up:
                    dy = -14 * amp * math.sin(math.pi * min(1.0, max(0.0, u / 0.2)))
        if t >= t_stop:
            sy *= 1 + 0.01 * math.sin(2 * math.pi * (t - t_stop) / 3.0)
        return sy, dy

    def j_fn(t):
        if t < t_fly0 - 0.02:
            return None
        sy, dy = j_squash(t)
        return JSPR.place(j_frame(t), jonah_x(t), jonah_ground(t), sx=1 / math.sqrt(sy), sy=sy, dy=dy)

    # his shadow swings round with the sun (morning: long to the right, noon: short, afternoon: to the left)
    JSH = sprite(520, 120, 260, 60, wc=0)
    JSH_I = JSH.add(C.ground_shadow(260, 60, JS, 120, opacity=0.26))

    def jsh_fn(t):
        if t < t_fly0 - 0.02:
            return None
        rx = sun_rel(t)
        off = -0.14 * rx
        stretch = 1 + min(0.9, abs(rx) / 900)
        im, (x, y) = JSH.place(JSH_I, jonah_x(t) + off * 0.5, jonah_ground(t), sx=stretch)
        return im, (x, y)
    sc.add_dynamic("jonah_sh", jsh_fn, z=4.9)
    sc.add_dynamic("jonah", j_fn, z=5)

    # sound arcs from his mouth while he calls (walking, then on the step)
    HEAD_PRE = C.body_points(C.jonah, 0, 0, JS, 1, pose="preach")["head"]
    HEAD_WALK = C.body_points(C.jonah, 0, 0, JS, 1, pose="walk_a")["head"]
    ARC = sprite(260, 260, 40, 130, wc=0)
    ARC_I = [ARC.add(arcs(40, 130, n, 1, 0.9)) for n in (1, 2, 3)]

    def arc_fn(t):
        on_walk = t_call + 0.1 <= t < t_calloff - 0.1 and walk_k(t) >= k_call_up
        on_step = t_preach + 0.05 <= t < L2.end + 0.1
        if not (on_walk or on_step):
            return None
        hx, hy = HEAD_PRE if on_step else HEAD_WALK
        return ARC.place(ARC_I[int(t * 7) % 3], jonah_x(t) + hx + 56, jonah_ground(t) + hy + 22)
    sc.add_dynamic("arcs", arc_fn, z=20)

    # ------------------------------------------------------------ market front: people who stop and turn
    person("mother", "woman", 2, 2330, 1352, 0.86, -1, 6.0, walk=(2700, t_stop - 1.5, t_turn - 0.05), period=0.4,
           seed=12, events=[(t_turn, -1, "stand", "surprised"), (t_wow + 0.55, -1, "point", "surprised"),
                            (t_worry + 0.1, -1, "listen", None)])
    person("girl", "child", 1, 2440, 1372, 0.86, -1, 6.1, walk=(2810, t_stop - 1.5, t_turn - 0.05), period=0.3,
           seed=13, events=[(t_turn + 0.05, -1, "stand", "surprised"), (t_worry + 0.3, -1, "sad", None)])
    person("elder", "elder", 0, 2590, 1346, 0.84, 1, 5.9, seed=14,
           events=[(t_turn + 0.15, -1, "stand", "surprised"), (t_worry + 0.25, -1, "listen", None)])
    person("man_r", "man", 0, 2700, 1400, 0.9, 1, 6.2, seed=15, idle=("listen", "neutral", 1.3),
           events=[(t_turn + 0.1, -1, "stand", "surprised"), (t_phr2 + 0.3, -1, "listen", None)])
    # animals in the square
    ANI = sprite(820, 360, 410, 330, seed=16)
    ani_i = ANI.add(C.ground_shadow(250, 330, 0.56, 170) + PR.animal(250, 330, 0.56, 1, kind="donkey"))
    sc.add_dynamic("donkey", lambda t: (ANI.place(ani_i, 560 + 160, 1214, sy=1 + 0.012 * math.sin(t * 2.3))
                                        if t >= t_fly0 - 0.02 else None), z=3.15)
    SHP = sprite(520, 260, 260, 230, seed=17)
    shp_i = SHP.add(C.ground_shadow(160, 230, 0.68, 160) + PR.animal(160, 230, 0.68, -1, kind="sheep")
                    + C.ground_shadow(360, 240, 0.6, 140) + PR.animal(360, 240, 0.6, -1, kind="sheep"))
    sc.add_dynamic("sheep_r", lambda t: (SHP.place(shp_i, 2860, 1420, dy=-2 * abs(math.sin(t * 1.3)))
                                         if t >= t_fly0 - 0.02 else None), z=6.3)

    # "!" marks over the surprised heads
    EXC = sprite(110, 120, 55, 75, wc=0)
    exc_i = EXC.add(exclaim(55, 75, 0.85))
    for i, nm in enumerate(("woman_fl", "mother", "elder", "man_r", "stroller")):
        hx, hy = people_heads[nm]
        x, y = hx + 2, hy - 44

        def efn(t, i=i, x=x, y=y):
            t0 = t_wow + i * 0.08
            if t < t0 or t > t_worry + 0.9:
                return None
            s = 0.4 + 0.6 * M.ease("back")(min(1.0, (t - t0) / 0.25))
            a = 1 - part(t, t_worry + 0.35, t_worry + 0.9, "sine")
            return EXC.place(exc_i, x, y + 10 * (1 - min(1.0, (t - t0) / 0.25)), sx=s, sy=s, alpha=a)
        sc.add_dynamic(f"wow{i}", efn, z=30 + i)

    sc.add("st_fg", street_fg_svg(), z=8,
           motion=M.combine(lambda t: Tf(dx=-0.22 * (camf(max(t, t_st)).x - CAM_END.x)), lambda t: Tf(alpha=in_a(t))))

    # doves flying over the street
    dpts = ((1400, 640, 0.45), (1480, 600, 0.38), (1350, 585, 0.36))
    sc.add("st_doves", [doves_svg(k, dpts) for k in range(3)], z=9, frame_at=lambda t: float(int(t * 9) % 3),
           motion=M.combine(M.drift(vx=95, vy=-6, t0=t_fly0), M.bob(9, 1.7), lambda t: Tf(alpha=in_a(t))))

    # ============================================================ OUTSIDE (the panorama, on top until the cut)
    sc.add("p_back", pano_back_svg(), z=50, wc=0.9, motion=F())
    sc.add("p_clouds", pano_clouds_svg([(470, 150, 400, 112, 3), (1720, 105, 360, 100, 5), (2860, 150, 420, 118, 7),
                                        (1060, 300, 240, 70, 11)]), z=51,
           motion=F(local=M.drift(vx=8), pivot=(1600, 300)))
    sc.add("p_passage", passage_svg(), z=53,
           motion=F(local=lambda t: Tf(alpha=1 - part(t, t_fly0, t_fly0 + 0.12, "linear")), pivot=FLY_C))
    sc.add("p_front", pano_front_svg(), z=55, motion=F())
    for ph in (0, 1):
        tw = (lambda ph_: lambda t: Tf(alpha=0.5 + 0.5 * math.sin(t * 2.6 + math.pi * ph_)))(ph)
        sc.add(f"p_glint{ph}", river_glints_svg(ph), z=56.2 + ph * 0.1, wc=0, motion=F(local=tw, pivot=FLY_C))
    sc.add("p_boats", boats_svg(), z=56.5,
           motion=F(local=M.combine(M.bob(4, 2.8), M.sway(1.0, 3.4, (2700, 1450))), pivot=(2700, 1450)))

    # tiny Jonah walking up the road to the west gate
    JROAD = [(0.0, 598, 1400, 0.49), (t_push0 - 0.4, 636, 1168, 0.36), (t_fly0 - 0.32, GX + 4, WALL_Y + 4, 0.33),
             (t_fly0 - 0.05, GX + 6, WALL_Y - 6, 0.3)]
    J0 = (598, 1400, 0.49)
    tj_frames = [doc(C.ground_shadow(J0[0], J0[1], J0[2], 120) + C.jonah(J0[0], J0[1], J0[2], 1, pose=p))
                 for p in ("walk_a", "walk_b")]
    tj_motion = M.keys([(t, {"dx": x - J0[0], "dy": y - J0[1], "s": s / J0[2]}) for t, x, y, s in JROAD],
                       ["linear", "linear", "linear"], pivot=(J0[0], J0[1]))
    tj_alpha = lambda t: Tf(alpha=1 - part(t, t_fly0 - 0.28, t_fly0 - 0.04, "sine"))
    sc.add("p_jonah", tj_frames, z=57, frame_at=lambda t: float(int(t / 0.34) % 2),
           motion=F(local=M.combine(tj_motion, tj_alpha), pivot=(J0[0], J0[1])))

    # foreground palms (sway)
    for i, (x, y, s, ln) in enumerate(((60, 1850, 1.3, 0.32), (3170, 1860, 1.15, -0.32))):
        sw = M.sway(0.8, 4.4 + i * 0.6, (x, y), phase=i * 0.3)
        sc.add(f"p_palm{i}", doc(PR.palm_tree(x, y, s, lean=ln)), z=58 + i * 0.1, motion=F(local=sw, pivot=(x, y)))

    # doves over the city
    pd = ((900, 520, 0.5), (990, 470, 0.42), (840, 455, 0.4))
    sc.add("p_doves", [doves_svg(k, pd) for k in range(3)], z=59, frame_at=lambda t: float(int(t * 8) % 3),
           motion=F(local=M.combine(M.drift(vx=70, vy=-5), M.bob(10, 1.6)), pivot=(900, 500)))

    # the three-days device: footprint trail + suns
    trail_fade = lambda t: 1 - part(t, L0.end - 0.3, L0.end + 0.25, "sine")

    def trail_reveal(t):
        u = part(t, t_trail0, t_trail1, "linear")
        x = TRAIL[0][0] + (TRAIL[-1][0] - TRAIL[0][0]) * u
        return {"mode": "left", "frac": (x - TRAIL_X0) / (TRAIL_X1 - TRAIL_X0), "soft": 30}
    sc.add("trail", trail_svg(), z=70, wc=0, reveal=trail_reveal,
           motion=F(local=lambda t: Tf(alpha=trail_fade(t) * (1.0 if t >= t_trail0 else 0.0)), pivot=FLY_C))
    sun_times = []
    for i, fr in enumerate(sun_fr):
        x, y, _ = point_at(fr)
        ts = t_trail0 + (t_trail1 - t_trail0) * ((x - TRAIL[0][0]) / (TRAIL[-1][0] - TRAIL[0][0]))
        sun_times.append(ts)
        sy_ = y - 168
        pop = M.keys([(ts - 0.02, {"s": 0.2, "alpha": 0}), (ts + 0.08, {"alpha": 1}), (ts + 0.3, {"s": 1.0})],
                     ["linear", "back"], pivot=(x, sy_))
        bobm = M.bob(6, 1.9, phase=i * 0.3)
        sc.add(f"sun{i}", doc(sun_icon(x, sy_, 58, i + 1)), z=71 + i, wc=0,
               motion=F(local=M.combine(pop, bobm, lambda t: Tf(alpha=trail_fade(t))), pivot=(x, sy_)))

    # ------------------------------------------------------------ light over the day
    def light(t):
        morning, noon, gold = (255, 240, 236), (255, 255, 255), (255, 233, 196)
        if t < t_fly0:
            return noon
        if t < t_st:
            return [M.lerp(a, b, part(t, t_fly0, t_st, "sine")) for a, b in zip(noon, morning)]
        u1 = part(t, t_st, t_st + 1.6, "sine")
        u2 = part(t, t_call - 0.9, t_calloff + 0.3, "sine")
        c = [M.lerp(a, b, u1) for a, b in zip(morning, noon)]
        return [M.lerp(a, b, u2) for a, b in zip(c, gold)]
    sc.fx = [light_fx(light)]

    # ------------------------------------------------------------ sound
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("birds", 0, dur=t_fly0 + 0.5, gain_db=-18, fade_in=0.8, fade_out=0.6)
    for ts in sun_times:
        sc.sfx("pop", ts, gain_db=-12)
    sc.sfx("sparkle", t_trail0, gain_db=-16)
    sc.sfx("whoosh", t_fly0 + 0.1, gain_db=-11)
    sc.sfx("crowd", t_fly0 + 0.2, dur=T - t_fly0 + 0.6, gain_db=-16, fade_in=0.6, fade_out=0.8)
    sc.sfx("footsteps", t_fly0, dur=t_stop - t_fly0, gain_db=-13, fade_in=0.2, fade_out=0.2,
           rate=V_W / (WALK_N * ADV))
    sc.sfx("pop", t_wow, gain_db=-14)

    # rasterise all sprite drawings now (fills the disk caches during the prepare pass, so render workers only
    # load PNGs) and close the browser if we opened it
    for sp in _SPRITES:
        sp.load()
    raster.close()
    return sc
