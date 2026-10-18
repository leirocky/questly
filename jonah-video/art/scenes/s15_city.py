"""Scene 15 — the great city (Jonah 3:3b-4), v2.

"Nineveh is a very, very big city: it takes three whole days to walk all the way through it. Jonah went into the
city, walked a day's journey and, as he walked, called out: 'In forty days Nineveh will be destroyed!'"

One 3200 x 1800 stage, two paintings on it, joined by a camera fly-through of the west gate:

  * OUTSIDE — the panorama (line 0). A morning view of Nineveh from the plain: the long crenellated front wall
    with two gates (it runs off both edges of the stage, so no end of the city is ever seen), the palace on its
    mound, the great ziggurat, rows and rows of flat roofs, a hazy skyline that goes on and on, the river Tigris
    winding in on the right with boats, fields, palms, sheep and a resting camel. The picture opens close on the
    road and the west gate, where little Jonah stands looking at the city (calm frame for the dissolve).
      "尼尼微是一座非常非常大的城，" — he sets off up the road (it bends in from the lower left, so he walks up-right,
          side-on, with a planted-foot walk) while the camera travels east along the wall and pulls back: palace,
          ziggurat, the second gate, the river — and the wall still runs on past both edges of the page.
      "要走整整三天，" — a picture-book device: a trail of little footprints walks itself across the city from the
          west gate toward the east, and at each third of the way a smiling sun pops up (1, 2, 3).
      "才能走遍整座城。" — the trail and suns stay up, the suns bob; then they fade and the camera pushes in on the
          west gate (it settles ~30% from the left) as Jonah walks into the deep shade of the passage, darkening
          until the shade has swallowed him.
  * THE FLY-THROUGH (v1 technique, "约拿进了城，"): every outside layer scales up around the gate opening (a hole
    cut through the wall and everything behind it) until the opening covers the frame; then the outside is dropped
    and we are inside, in a street, with Jonah walking in from the gate. The camera's zoom keeps going through the
    start of the fly (no stop-and-whoosh). The people in the street are drawn only once the opening's bottom edge
    has left the frame (before that the threshold would cut them off at the knees: giants standing in a pit).
  * INSIDE — a long street that opens onto the market square (line 1, line 2).
      "走了一天的路，一边走，" — Jonah walks east (planted-foot walk cycle: the drawing follows the distance
          walked), the camera tracking him past houses, palms, laundry, children playing and passers-by (who walk
          with planted-foot cycles too). The day goes by: the sun rises behind the roofs on the left, arcs over the
          street and sinks toward the right; the light goes from rosy morning through white noon to a golden
          afternoon (apricot sky, a warm glow round the low sun); Jonah's shadow swings round.
      "一边走，一边大声喊：" — still walking, he raises his arm and calls out (sound arcs); people he passes stop and
          look. He lowers his arm, reaches the market square and climbs the two tiers of the stone step on explicit
          footfalls (ledge, then top: the planted foot stays put, the body rises onto each tread, a little squash
          at each landing).
      Line 2 (Jonah) "再过四十天，尼尼微就要毁灭了！" — arm high, he proclaims (his mouth follows the loudness of the
          voice take, shut in the comma pause); the people in the square stop and turn to him (hard pose cuts sold
          by little hops), "!" marks pop over their heads, a mother points; from "尼尼微就要毁灭了" (keyed to the
          end of the comma pause found in the voice) they look worried (hand to chin, the girl hangs her head) and
          the street's bustle drops to a hush. The camera glides on so Jonah ends ~23% from the left, as s16 opens;
          he lowers his arm with a stern face (s16's opening expression); a calm, readable last second (golden
          late-afternoon light, low sun over the rooftops) for the dissolve into s16.

Notes for maintainers
* Every time comes from ctx.lines[i].start / .end / .at(phrase), phrase_time() (character position inside
  one chunk) or the voice take's loudness envelope (build/voice/lines/<id>_02.wav; falls back to the comma's
  character position when the take is missing).
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
WALL_X0, WALL_X1 = -260, SW + 260   # the front wall runs off both edges of the stage: no city end is ever seen
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
TRAIL = [(GX + 10, 850), (820, 760), (1150, 705), (1550, 690), (1950, 700), (2300, 682), (2640, 694),
         (2830, 760)]

# ================================================================ inside (street + market) geometry
GY = 1310                           # street ground line (Jonah's feet)
BACK_Y = 1120                       # ground line of the back row of houses
STEP_X, STEP_Y = 1810, 1324         # the stone step in the market: centre, bottom line
STEP_TOP = STEP_Y - 62              # where Jonah stands to preach
JS = 0.92                           # Jonah's scale in the street
WALK_A, WALK_N = 56, 6              # planted-foot walk: ankle travel (figure px) per half step, drawings per step
ADV = 2 * WALK_A / WALK_N * JS      # stage px the anchor advances per walk drawing (planted sole stays put)
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

_EXTRA_EXPRS = {"serious": dict(eyes="dot", brow=(0.015, -0.005, -0.02), mouth="flat"),
                # earnest proclaiming brows with the mouth shut (the pauses in Jonah's cry)
                "call_shut": dict(eyes="dot", brow=(-0.07, 0.02, -0.07), mouth="flat")}


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


_KIND_M = {"man": C._ADULT, "woman": C._metrics(C._ADULT, 0.96, 0.92), "child": C._CHILD}


def cfig(x, y, s, kind, variant, facing, ps, expr=None):
    """A townsperson (same design as C.citizen) in a custom rig pose: their planted-foot walk drawings."""
    D = C._citizen_design(kind, variant, "normal")
    inner, _ = C._figure(D, _KIND_M[kind], ps, expr or "neutral", C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"{kind}{variant}-gait")


def leg_k(kind):
    m = _KIND_M[kind]
    return (m["th"] + m["sh"]) / (C._ADULT["th"] + C._ADULT["sh"])


def gait(pdx, sdx, plift, slift, parity, ph, u, arm="down", lk=1.0):
    """One drawing of a planted-foot walk: planted ankle at pdx, swinging ankle at sdx (figure px from the anchor),
    each foot ``lift`` figure px above the anchor's ground line (a foot on a higher tread, or in the air).
    parity 0: the far leg is planted. ph: phase in the two-step cycle (arm swing); u: phase in the step (pelvis bob).
    arm: 'down' (both arms swing), 'mid' / 'up' (far arm raised: calling out). lk: leg length / adult leg length."""
    plant = ("ik", pdx, 1, plift) if abs(plift) > 1e-9 else ("ik", pdx, 1)
    swing = ("ik", sdx, 1, slift)
    sw = 34 * math.cos(math.pi * ph)
    far, hands = ("fk", -sw, -sw + 14), ("fist", "fist")
    if arm == "up":
        far, hands = ("fk", 150, 166), ("open", "fist")
    elif arm == "mid":
        far, hands = ("fk", 116, 142), ("open", "fist")
    drop = 12 + 4 * math.cos(2 * math.pi * u)
    return C._P(t=4, h=-3, legs=(plant, swing) if parity == 0 else (swing, plant),
                arms=(far, ("fk", sw, sw + 14)), hands=hands, drop=drop * lk if lk != 1.0 else drop)


def walk_pose(k, arm="down", A=WALK_A, lk=1.0):
    """Planted-foot walk drawing k on level ground (WALK_N drawings per step, two steps per cycle): the planted
    ankle goes from +A to -A figure px while the other foot swings through, so advancing the anchor 2A/WALK_N
    figure px per drawing keeps the planted sole on one spot."""
    ph = (k % (2 * WALK_N)) / WALK_N
    step, u = divmod(ph, 1.0)
    swing_lift = 22 * math.sin(math.pi * u) if lk == 1.0 else 22 * lk * math.sin(math.pi * u)
    return gait(A * (1 - 2 * u), -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 0.0, swing_lift, int(step), ph,
                u, arm, lk)


def climb_pose(feet, treads, k, s=JS):
    """Walk drawing k (WALK_N per step) over explicit footfalls: during step n = k // WALK_N the ankle planted at
    stage x feet(n) (on a tread treads(n) stage px above the street) never moves. The body rises onto a higher tread
    over the first 40% of the step; the swing foot travels low and only rises to the next tread's height late in
    its swing (when it crosses the riser), so the knee never comes up high under the robe (which would read as
    kneeling). The robe is drawn a little narrower while climbing. Returns (pose, anchor x, anchor y)."""
    n, j = divmod(k, WALK_N)
    u = j / WALK_N
    prev, plant, nxt = feet(n - 1), feet(n), feet(n + 1)
    hp, hn, hx = treads(n - 1), treads(n), treads(n + 1)
    ax = M.lerp((prev + plant) / 2, (plant + nxt) / 2, u)

    def ss(v):
        v = min(1.0, max(0.0, v))
        return v * v * (3 - 2 * v)
    H = M.lerp(min(hp, hn), hn, ss(u / 0.4))
    e = 0.5 - 0.5 * math.cos(math.pi * u)
    sx = prev + (nxt - prev) * (u + e) / 2
    w = hp + (hx - hp) * ss((u - 0.3) / 0.45) + (15 if hx <= hp else 7) * s * math.sin(math.pi * u)
    ph = (k % (2 * WALK_N)) / WALK_N
    ps = gait((plant - ax) / s, (sx - ax) / s, (hn - H) / s, (w - H) / s, n % 2, ph, u)
    ps["flare"] = -9
    return ps, ax, GY - H


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
    mound = (f'<path d="M-300,{HORIZON + 120} C500,{HORIZON + 40} 1300,{HORIZON + 10} 1700,{HORIZON + 20} '
             f'S2700,{HORIZON + 40} {SW + 300},{HORIZON + 120} L{SW + 100},{WALL_Y} L-100,{WALL_Y} Z" '
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
        span_l = -110 + row * 20
        span_r = SW + 110 - row * 20
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


PAS_STOPS = [(0, "#3a2a20"), (0.6, "#4a3426"), (1, "#5c4231")]
PAS_Y0, PAS_Y1 = SPRING - GWD / 2 - 6, WALL_Y + 4          # bbox of the passage gradient


def passage_color(y):
    """The passage gradient's colour (RGB floats) at stage y: little Jonah darkens toward it as he walks in."""
    u = min(1.0, max(0.0, (y - PAS_Y0) / (PAS_Y1 - PAS_Y0)))
    for (o0, c0), (o1, c1) in zip(PAS_STOPS, PAS_STOPS[1:]):
        if u <= o1:
            k = (u - o0) / (o1 - o0)
            a, b = S.hex_rgb(c0), S.hex_rgb(c1)
            return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))
    return S.hex_rgb(PAS_STOPS[-1][1])


def passage_svg():
    """The deep shadow inside the open west gate (shown until the camera flies through it). Plain dark, so little
    Jonah can walk into it and be swallowed by the shade."""
    r = GWD / 2
    d = (f"M{GX - r - 6},{WALL_Y + 4} L{GX - r - 6},{SPRING:.1f} A{r + 6},{r + 6} 0 0 1 {GX + r + 6},{SPRING:.1f} "
         f"L{GX + r + 6},{WALL_Y + 4} Z")
    defs = S.lin_grad("s15pas", PAS_STOPS)
    body = (f'<path d="{d}" fill="url(#s15pas)"/>'
            f'<path d="M{GX - HOLE_R},{WALL_Y + 3} L{GX - HOLE_R + 26},{WALL_Y - 8} L{GX + HOLE_R - 26},{WALL_Y - 8} '
            f'L{GX + HOLE_R},{WALL_Y + 3} Z" fill="#6a4c36" opacity="0.8"/>')
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


# the road comes in from the lower left and runs up-right to the west gate (little Jonah walks up it side-on)
ROAD_C = [(170, SH + 40), (285, 1600), (385, 1430), (480, 1280), (568, 1170), (GX, WALL_Y)]
ROAD_HW = [330, 245, 190, 145, 112, 92]


def road_edges():
    return ([(x - hw, y) for (x, y), hw in zip(ROAD_C, ROAD_HW)],
            [(x + hw, y) for (x, y), hw in zip(ROAD_C, ROAD_HW)])


def road_path():
    left, right = road_edges()
    right = right[::-1]
    d = S.smooth_path(left, closed=False, tension=0.8)
    d += f" L{right[0][0]},{right[0][1]}"
    d += " " + S.smooth_path(right, closed=False, tension=0.8).replace("M", "L", 1)
    return d + " Z"


def _road_samples():
    pts = []
    n = len(ROAD_C)
    for i in range(n - 1):
        p0, p1, p2, p3 = ROAD_C[max(0, i - 1)], ROAD_C[i], ROAD_C[i + 1], ROAD_C[min(n - 1, i + 2)]
        for j in range(30):
            u = j / 30
            pts.append(tuple(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * u + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * u * u
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * u ** 3) for c in (0, 1)))
    pts.append(ROAD_C[-1])
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return pts, cum


_ROAD = _road_samples()


def road_point(frac):
    """Point on the road's centre line, frac 0 (bottom of the stage) .. 1 (the west gate threshold)."""
    pts, cum = _ROAD
    target = min(1.0, max(0.0, frac)) * cum[-1]
    for i in range(1, len(cum)):
        if cum[i] >= target:
            u = (target - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
            return (M.lerp(pts[i - 1][0], pts[i][0], u), M.lerp(pts[i - 1][1], pts[i][1], u))
    return pts[-1]


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
    ground = (f'<path d="M-40,{SH + 40} L-40,{WALL_Y - 4} L{SW + 40},{WALL_Y - 4} '
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
        x, y = road_point(0.04 + 0.92 * u)
        x += rng.uniform(-0.6, 0.6) * (280 - 190 * u)
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
    for x, y, s, v in ((700, 1262, 0.4, 2), (820, 1330, 0.45, 0), (1350, 1340, 0.42, 1), (2000, 1380, 0.5, 0),
                       (1250, 1215, 0.32, 2), (2280, 1400, 0.55, 3)):
        deco += PR.bush(x, y, s, v)
    for x, y, s in ((2560, 1365, 0.42), (2430, 1500, 0.5), (2360, 1660, 0.58), (2700, 1250, 0.36),
                    (2860, 1195, 0.3)):
        deco += PR.reeds(x, y, s)
    for x, y, s, f in ((1240, 1470, 0.3, 1), (1330, 1490, 0.27, -1), (1450, 1460, 0.28, 1), (1560, 1505, 0.3, -1)):
        deco += C.ground_shadow(x, y, s, 140) + PR.animal(x, y, s, f, kind="sheep")
    deco += C.ground_shadow(2140, 1500, 0.36, 300) + PR.animal(2140, 1500, 0.36, -1, kind="camel")
    deco += C.ground_shadow(2030, 1512, 0.36, 110) + C.citizen(2030, 1512, 0.36, 1, kind="man", variant=2)
    for x, y, s, v in ((60, 1470, 0.8, 1), (700, 1470, 0.7, 2), (980, 1640, 0.8, 0), (1500, 1680, 0.9, 1),
                       (1900, 1620, 0.8, 2), (700, 1700, 0.9, 0), (1200, 1760, 1.0, 2)):
        deco += PR.grass_tuft(x, y, s, v)
    rocks = ""
    for x, y, rx, ry, seed in ((880, 1500, 40, 22, 1), (930, 1512, 22, 13, 2), (720, 1660, 38, 20, 3)):
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
    """Golden late-afternoon sky wash (fades in over the noon sky as the day goes by): clear apricot above, gold
    toward the rooftops."""
    defs = sky_grad("s15esky", [(0, S.mix(S.mix(P["sky_dawn"], P["sky_warm"], 0.5), "#fff4e2", 0.3)),
                                (0.45, S.mix(P["sky_warm"], P["sky_dawn"], 0.35)),
                                (0.8, S.mix(P["sky_warm"], P["gold"], 0.3)), (1, S.mix(P["sky_warm"], P["gold"], 0.45))])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOT + 20}" fill="url(#s15esky)"/>', defs)


def glow_image(r=640, col=(255, 214, 140)):
    """A soft warm glow (RGBA, premultiplied-friendly) for a 'screen' dynamic around the low sun."""
    yy, xx = np.mgrid[-r:r, -r:r].astype(np.float32)
    d = np.sqrt(xx * xx + yy * yy) / r
    a = np.clip(1 - d, 0, 1) ** 2.2
    im = np.zeros((2 * r, 2 * r, 4), np.uint8)
    im[..., 0], im[..., 1], im[..., 2] = col
    im[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


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


# ================================================================ narration helpers


def phrase_time(line, phrase):
    """Start of ``phrase`` inside its subtitle chunk, interpolated by character position (chunks are timed from the
    recognised speech; inside one chunk the syllables come at a near-even pace)."""
    for c in line.chunks:
        i = c.text.find(phrase)
        if i >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、")))
            return c.start + (c.end - c.start) * i / n
    raise KeyError(f"{phrase!r} not in {line.text!r}")


def voice_env(ctx, i, line, hop=0.01):
    """Loudness envelope (dB re. the take's peak, one value per ``hop`` s from the line's start) of the voice take
    of line i, or None when the take is not on disk or does not match the line's timing."""
    try:
        import soundfile as sf
        from engine.paths import BUILD
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"), dtype="float32")
    except Exception:
        return None
    if x.ndim > 1:
        x = x.mean(axis=1)
    if abs(len(x) / sr - (line.end - line.start)) > 0.25:
        return None
    n = max(1, int(sr * hop))
    m = len(x) // n
    if m < 20:
        return None
    e = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(axis=1)) + 1e-7
    db = np.convolve(20 * np.log10(e), np.ones(3) / 3, mode="same")
    return db - db.max()


def comma_pause(line, env, hop=0.01, quiet=-28.0):
    """(start, end), in scene seconds, of the pause at the line's first comma: the deepest quiet stretch of the
    voice near the comma's character position; without a voice envelope, a guess from that position."""
    text = line.text
    n = max(1, len(text.rstrip("，。！？：；、")))
    ci = text.find("，")
    frac = ci / n if ci > 0 else 0.4
    d = line.end - line.start
    if env is not None:
        lo, hi = max(2, int((frac - 0.2) * d / hop)), min(len(env) - 3, int((frac + 0.2) * d / hop))
        if hi - lo > 6:
            avg = np.convolve(env[lo:hi], np.ones(4) / 4, mode="valid")
            j = int(np.argmin(avg)) + lo + 2
            if env[j] < quiet:
                a_, b_ = j, j
                while a_ > lo and env[a_ - 1] < quiet:
                    a_ -= 1
                while b_ < hi and env[b_ + 1] < quiet:
                    b_ += 1
                return line.start + a_ * hop, line.start + (b_ + 1) * hop
    tc = line.start + frac * d
    return tc - 0.04, tc + 0.08


def mouth_track(line, env, pause, fps, hop=0.01):
    """Per-frame mouth state while a line is spoken (0 shut, 1 open, 2 wide), following the voice's loudness, with
    one-frame flickers smoothed away. Without an envelope: a steady open/wide flap, shut in the comma pause."""
    nf = int((line.end - line.start) * fps) + 2
    st = []
    for f in range(nf):
        t0 = f / fps
        if env is not None:
            i0, i1 = int(t0 / hop), max(int(t0 / hop) + 1, int((t0 + 1 / fps) / hop))
            v = float(np.mean(env[min(i0, len(env) - 1):min(i1, len(env))])) if i0 < len(env) else -90.0
            st.append(0 if v < -26 else (1 if v < -11 else 2))
        else:
            tt = line.start + t0
            st.append(0 if pause[0] <= tt < pause[1] else 1 + int(t0 / 0.19) % 2)
    for f in range(1, nf - 1):
        if st[f] != st[f - 1] and st[f] != st[f + 1]:
            st[f] = st[f - 1]
    return st


# ================================================================ build


def build(ctx):
    _SPRITES.clear()
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.line(0), ctx.line(1), ctx.line(2)
    part = M.progress

    # ------------------------------------------------------------ key times (all from the narration)
    t_pull0 = max(1.05, L0.start + 0.15)              # "尼尼微是一座非常非常大的城": pull back and travel east
    cB = L0.at("要走")                                 # "要走整整三天，才能走遍整座城。"
    cB_end = next(c.end for c in L0.chunks if "要走" in c.text)
    dB = cB_end - cB
    t_wide = cB + 0.5                                 # the wide view of the city has settled
    t_trail0, t_trail1 = cB + 0.08, cB + 0.40 * dB    # the footprint trail walks across the city
    sun_fr = (1 / 3, 2 / 3, 1.0)                      # suns at each third of the way
    t_push0 = L0.end - 1.0                            # the camera heads for the west gate (trail fades at the end)
    t_fly0 = L1.start + 0.12                          # "约拿进了城": fly through the gate
    t_fly1 = t_fly0 + 0.78
    t_st = t_fly0 + 0.62                              # the camera's push-in has settled into the street
    t_call = phrase_time(L1, "一边走") - 0.15          # "一边走，一边大声喊": arm up, calling while he walks
    t_stop = L2.start - 0.2                           # he has walked up onto the step and stops
    t_preach = L2.start                               # "再过四十天，尼尼微就要毁灭了！"
    env2 = voice_env(ctx, 2, L2)
    t_comma0, t_comma1 = comma_pause(L2, env2)        # the pause at "，" in Jonah's cry
    t_phr2 = t_comma1                                 # "尼尼微就要毁灭了"
    t_turn = L2.start + 0.22                          # people stop and turn
    t_wow = t_turn + 0.18
    t_worry = t_phr2 + 0.15
    t_down = L2.end + 0.12                            # arm down: calm ending
    MOUTH = mouth_track(L2, env2, (t_comma0, t_comma1), ctx.fps)

    # ------------------------------------------------------------ Jonah's street walk: explicit footfalls
    S_FL = 2 * WALK_A * JS                            # stride (stage px) of one step
    N_FL = 8                                          # level steps before the climb
    P_LEDGE, P_TOP = STEP_X - 148, STEP_X - 58        # ankle spots: lower tier's side ledge, upper tier
    H_LEDGE, H_TOP = GY - 1286, GY - STEP_TOP         # their heights above the street line
    P0 = P_LEDGE - 90 - N_FL * S_FL
    X_IN = P0 - S_FL / 2                              # his anchor when the fly-through starts

    def feet(n):
        if n <= N_FL:
            return P0 + n * S_FL
        return (P_LEDGE, P_TOP, P_TOP + 90)[min(2, n - N_FL - 1)]

    def treads(n):
        return 0.0 if n <= N_FL else (H_LEDGE, H_TOP, H_TOP)[min(2, n - N_FL - 1)]
    K_CL = WALK_N * N_FL                              # first drawing of the climb (swing foot heads for the ledge)
    N_END = WALK_N * (N_FL + 2) + 3                   # passing drawing on the upper tier; then he stands
    CLIMB = {k: climb_pose(feet, treads, k) for k in range(K_CL, N_END + 1)}
    R0 = (K_CL + (N_END - K_CL) / 0.8) / (t_stop - 0.12 - t_fly0)   # drawings / s (the climb is 20% slower)
    RC = 0.8 * R0
    T_CL = t_fly0 + K_CL / R0
    V_W = ADV * R0                                    # walking speed on the street (stage px / s)

    def walk_k(t):
        if t < T_CL:
            return max(0, int((t - t_fly0) * R0 + 1e-6))
        return min(N_END, K_CL + int((t - T_CL) * RC + 1e-6))

    def k_time(k):
        return t_fly0 + k / R0 if k <= K_CL else T_CL + (k - K_CL) / RC

    def jonah_xy(t):
        if t >= t_stop:
            return P_TOP, STEP_TOP
        k = walk_k(t)
        if k < K_CL:
            return X_IN + k * ADV, GY
        return CLIMB[k][1], CLIMB[k][2]

    k_up = walk_k(t_call) + 2                          # arm goes up over two drawings ...
    k_dn = K_CL - 2                                    # ... and is down again before the climb starts
    t_calloff = k_time(k_dn)

    # ------------------------------------------------------------ camera
    CAM0 = Cam(820, 1128, 1560)                        # close on the road and the west gate
    CAMW = Cam(1650, 935, 2760)                        # the city from the gate to the river; it runs off both edges
    CAM_HOLD = Cam(1620, 945, 2720)
    CAM_ST0 = Cam(1000, 1000, 1800)                    # (y, w of) the street framing after the fly-through
    D1, D2 = t_fly0 - t_push0, t_st - t_fly0
    WG = CAM_HOLD.w + (CAM_ST0.w - CAM_HOLD.w) * D1 / (D1 + D2)   # zoom keeps going through the fly (no stall)
    YG = CAM_HOLD.y + (CAM_ST0.y - CAM_HOLD.y) * D1 / (D1 + D2)
    LE_H, LE_G = CAM_HOLD.x - CAM_HOLD.w / 2, 40.0     # frame's left edge: at the hold, when the fly starts (the
    #                                                    gate is then ~30% from the left)
    RAMP = 0.6                                         # the tracking camera eases up to walking speed
    CAM_END = Cam(P_TOP + 0.27 * 1720, 985, 1720)      # Jonah on his step ~23% from the left (as s16 opens)
    t_endcam = L2.start + 0.9
    t_dec = T_CL

    out_cam = M.cam_keys([(0, CAM0), (t_pull0, CAM0), (t_wide, CAMW), (t_push0, CAM_HOLD)], "sine")

    def left_edge(t):
        """The frame's left edge from the push-in on: it eases to rest at the far left of the stage as the zoom
        reaches the gate, then (zoom still going, through the fly) eases up to Jonah's walking speed."""
        if t < t_fly0:
            return M.lerp(LE_H, LE_G, part(t, t_push0, t_fly0, "sine"))
        d = t - t_fly0
        u = min(1.0, d / RAMP)
        return LE_G + V_W * (RAMP * (u ** 3 - 0.5 * u ** 4) + max(0.0, d - RAMP))

    def cam_wy(t):
        if t < t_fly0:
            u = (t - t_push0) / D1
            return CAM_HOLD.w + (WG - CAM_HOLD.w) * u ** 3, CAM_HOLD.y + (YG - CAM_HOLD.y) * u ** 3
        if t < t_st:
            e = 1 - (1 - (t - t_fly0) / D2) ** 3
            return WG + (CAM_ST0.w - WG) * e, YG + (CAM_ST0.y - YG) * e
        u = part(t, t_st, t_dec, "sine")
        return M.lerp(CAM_ST0.w, 1790, u), M.lerp(CAM_ST0.y, 995, u)
    x_dec = left_edge(t_dec) + 1790 / 2

    def camf(t):
        if t < t_push0:
            return out_cam(t)
        if t < t_dec:
            w, y = cam_wy(t)
            return Cam(left_edge(t) + w / 2, y, w)
        # glide from walking speed to rest on the market framing (Hermite: no velocity jump, no reversal)
        D = t_endcam - t_dec
        u = min(1.0, (t - t_dec) / D)
        h01 = 3 * u * u - 2 * u ** 3
        h10 = u ** 3 - 2 * u * u + u
        x = x_dec * (1 - h01) + CAM_END.x * h01 + V_W * D * h10
        y = M.lerp(995, CAM_END.y, part(t, t_dec, t_endcam, "sine"))
        w = M.lerp(1790, CAM_END.w, part(t, t_dec, t_endcam, "sine"))
        v = part(t, t_endcam, T, "sine")       # a very slow settle to the end
        return Cam(x + 12 * v, y - 4 * v, w - 40 * v)
    sc.camera = camf

    # ------------------------------------------------------------ fly-through (v1 technique)
    def fly_pivot(cam):
        """Centre inside the clear opening that makes its sides / top and bottom reach the frame edges of ``cam``
        at the same scale (so the opening fills the frame as early as possible)."""
        a_, b_ = HOLE_CLEAR[0], HOLE_CLEAR[1]
        c_, d_ = cam.x - cam.w / 2, cam.x + cam.w / 2
        ys_, yb_ = HOLE_CLEAR[2], HOLE_CLEAR[3]
        vy0, vy1 = cam.y - cam.w * 9 / 32, cam.y + cam.w * 9 / 32
        return ((a_ * d_ - c_ * b_) / (d_ + a_ - b_ - c_), (ys_ * vy1 - vy0 * yb_) / (vy1 + ys_ - yb_ - vy0))
    s_fly = lambda t: 1 + 21.0 * part(t, t_fly0, t_fly1, "in")

    def covers(cam, s, pv, bottom_only=False):
        hx0, hx1, hs, hb = HOLE_CLEAR
        px, py = pv
        vx0, vx1 = cam.x - cam.w / 2, cam.x + cam.w / 2
        vy0_, vy1_ = cam.y - cam.w * 9 / 32, cam.y + cam.w * 9 / 32
        if bottom_only:
            return py + s * (hb - py) >= vy1_ + 4
        return (px + s * (hx0 - px) <= vx0 - 4 and px + s * (hx1 - px) >= vx1 + 4
                and py + s * (hs - py) <= vy0_ - 4 and py + s * (hb - py) >= vy1_ + 4)

    def first_time(pv, bottom_only=False):
        kk = 0
        while t_fly0 + kk / 120 < t_fly1:
            tt = t_fly0 + kk / 120
            if covers(camf(tt), s_fly(tt), pv, bottom_only):
                return tt
            kk += 1
        return t_fly1
    FLY_C = fly_pivot(camf(t_fly0 + 0.5))
    for _ in range(3):                                 # the camera still moves during the fly: iterate the pivot
        FLY_C = fly_pivot(camf(first_time(FLY_C)))
    t_cut = first_time(FLY_C)
    # people in the street are drawn only once the opening's bottom edge has left the frame: before that, their
    # feet would be hidden by the scaled-up threshold (heads poking up over it, far too big for the little arch)
    t_show = min(t_cut, first_time(FLY_C, bottom_only=True))
    out_a = lambda t: 1.0 if t < t_cut else 0.0
    in_a = lambda t: 1.0 if t >= t_fly0 - 0.02 else 0.0
    shown = lambda t: t >= t_show - 0.05
    shown_a = lambda t: part(t, t_show - 0.05, t_show + 0.02, "linear")   # a 2-frame materialise in the whoosh

    def F(local=None, pivot=FLY_C):
        return V.fly(local, pivot, FLY_C, s_fly, out_a)

    # ============================================================ INSIDE (behind the outside layers)
    # sky, the day's sun, clouds, hazy far city
    sc.add("st_sky", street_sky_svg(), z=1, wc=0.6, motion=lambda t: Tf(alpha=in_a(t)))
    eve = lambda t: part(t, t_call - 0.9, t_calloff + 0.4, "sine")
    sc.add("st_sky_eve", street_sky_eve_svg(), z=1.05, wc=0.6, motion=lambda t: Tf(alpha=eve(t) * in_a(t)))
    SUN0 = (1100, 620)

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
    cl_par = lambda k: (lambda t: Tf(dx=k * (camf(max(t, t_st)).x - 1100)))
    sc.add("st_clouds", pano_clouds_svg([(640, 600, 250, 70, 31), (1420, 578, 210, 60, 33), (2250, 612, 270, 76, 35),
                                         (3000, 586, 220, 62, 37), (3600, 600, 240, 66, 39)]), z=1.4,
           motion=M.combine(M.drift(vx=9), cl_par(0.6), lambda t: Tf(alpha=in_a(t))))
    sc.add("st_far", street_far_svg(), z=1.6, wc=0.8,
           motion=M.combine(cl_par(0.4), lambda t: Tf(alpha=in_a(t))))
    # the low afternoon sun warms the air over the rooftops (a soft 'screen' glow that follows it)
    GR = 430
    glow = np.asarray(glow_image(GR))
    glow_q = {}

    def glow_fn(t):
        a = 0.6 * eve(t) * in_a(t)
        if a < 0.02:
            return None
        q = round(a * 14) / 14
        if q not in glow_q:
            g = glow.copy()
            g[..., 3] = (g[..., 3].astype(np.float32) * q).astype(np.uint8)
            glow_q[q] = Image.fromarray(g, "RGBA")
        x, y = sun_pos(t)
        return glow_q[q], (x - GR, y - GR)
    sc.add_dynamic("st_sunglow", glow_fn, z=1.7, blend="screen")

    for i, (x0, x1, y, sag, cols, seed) in enumerate(LAUNDRY):
        frames = [doc(laundry(x0, x1, y, sag, cols, seed, ph)) for ph in (0, 1)]
        sc.add(f"laundry{i}", frames, z=2.2, frame_at=lambda t, i=i: float(int(t * 2.6 + i) % 2),
               motion=lambda t: Tf(alpha=in_a(t)))

    # ------------------------------------------------------------ people (sprites)
    people_heads = {}

    def hop_amount(t, hops, s):
        """Squash-and-hop that hides a hard pose cut: (sy factor, dy) for hops [(time, amplitude)]."""
        sy, dy = 1.0, 0.0
        for th, amp in hops:
            u = t - th
            if -0.08 <= u <= 0.3:
                if u < 0:
                    sy *= 1 - 0.05 * amp * part(u, -0.08, 0, "sine")
                else:
                    sy *= (1 - 0.05 * amp * (1 - part(u, 0, 0.1, "sine"))
                           + 0.03 * amp * math.sin(math.pi * min(1.0, u / 0.3)))
                    dy -= 16 * s * amp * math.sin(math.pi * min(1.0, u / 0.3))
        return sy, dy

    def person(name, kind, variant, x, y, s, face, z, walk=None, idle=None, events=(), shadow=True, seed=0):
        """A townsperson sprite (drawn only from t_show on).
        walk=(x_from, t_a, t_b[, stride_k]): a planted-foot walk (WALK_N drawings per step; the figure advances one
            drawing's worth of stride at each drawing change, so the planted sole never slides) from about x_from,
            arriving at x at t_b on a passing drawing; the speed follows from the window.
        idle=(pose, expr, period): alternate stand / pose while waiting; every switch is sold by a small hop
            (a 'cheer' idle jumps for joy instead).
        events: [(t, facing, pose, expr)] hard pose cuts, each sold by a squash-and-hop."""
        sp = person_sprite(s, seed=seed + variant * 7)
        stand0 = sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose="stand"))
        alt = None
        if idle:
            alt = sp.add(C.citizen(sp.ax, sp.ay, s, face, kind=kind, variant=variant, pose=idle[0], expr=idle[1]))
        ev = [(te, sp.add(C.citizen(sp.ax, sp.ay, s, fc, kind=kind, variant=variant, pose=pose, expr=expr)))
              for (te, fc, pose, expr) in sorted(events)]
        t_ev0 = ev[0][0] if ev else 1e9
        hops = [(te, 1.0) for te, _ in ev]
        last_face = sorted(events)[-1][1] if events else face
        wf, x_from, t_a, t_b, n_w, adv, rate, dirn = None, x, -1.0, -1.0, 0, 0.0, 1.0, 1
        if walk:
            lk = leg_k(kind)
            A = WALK_A * lk * (walk[3] if len(walk) > 3 else 1.0)
            adv = 2 * A / WALK_N * s
            n_w = max(3, int(round((abs(x - walk[0]) / adv - 3) / 6)) * 6 + 3)
            t_a, t_b = walk[1], walk[2]
            rate = n_w / (t_b - t_a)
            dirn = 1 if x > walk[0] else -1
            x_from = x - dirn * n_w * adv
            wf = [sp.add(cfig(sp.ax, sp.ay, s, kind, variant, face, walk_pose(k, A=A, lk=lk))) for k in range(12)]
            if t_b < t_ev0 - 0.05:
                hops.append((t_b, 0.5))
        if idle and idle[0] != "cheer":
            k = 1
            while k * idle[2] < min(t_ev0, T):
                if not (walk and t_a - 0.1 <= k * idle[2] <= t_b + 0.1):
                    hops.append((k * idle[2], 0.4))
                k += 1

        def walk_i(t):
            return min(n_w, int((t - t_a) * rate + 1e-6))

        def idx(t):
            cur = None
            for te, fi in ev:
                if t >= te:
                    cur = fi
            if cur is not None:
                return cur
            if wf and t_a <= t < t_b:
                return wf[walk_i(t) % 12]
            if alt is not None:
                return (stand0, alt)[int(t / idle[2]) % 2]
            return stand0

        def xpos(t):
            if not wf or t >= t_b:
                return x
            return x_from if t < t_a else x_from + dirn * walk_i(t) * adv

        def fn(t):
            if not shown(t):
                return None
            sy, dy = hop_amount(t, hops, s)
            sy *= 1 + 0.012 * math.sin(2 * math.pi * (t / (2.8 + variant * 0.3) + variant * 0.17))
            if idle and idle[0] == "cheer" and t < t_ev0:
                ph = t / idle[2]
                if int(ph) % 2 == 1:                  # arms up: a little jump of joy
                    dy -= 18 * s * math.sin(math.pi * (ph % 1.0))
            return sp.place(idx(t), xpos(t), y, sx=1 / math.sqrt(sy), sy=sy, dy=dy, alpha=shown_a(t))
        if shadow:
            shs = sprite(260 * s + 40, 70 * s + 30, 130 * s + 20, 35 * s + 15, wc=0)
            shi = shs.add(C.ground_shadow(shs.ax, shs.ay, s, 80 if kind == "child" else 110))
            sc.add_dynamic(name + "_sh", lambda t: shs.place(shi, xpos(t), y, alpha=shown_a(t)) if shown(t) else None,
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
    person("w_walk", "woman", 1, 1080, 1186, 0.62, -1, 3.2, walk=(1450, t_fly0, t_call + 0.25), seed=4,
           events=[(t_call + 0.25, 1, "stand", "surprised"), (t_call + 1.1, 1, "listen", None)])
    # market back row: a vendor by his pots (hawking: he points at his wares now and then), a boy at the fruit
    # stall, a stroller
    person("vendor", "man", 2, 1395, 1188, 0.6, 1, 3.3, idle=("point", None, 1.9), seed=5,
           events=[(t_turn + 0.05, 1, "stand", "surprised"), (t_worry + 0.2, 1, "listen", None)])
    person("boy_fruit", "child", 2, 2250, 1200, 0.62, 1, 3.32, seed=6,
           events=[(t_turn + 0.1, -1, "stand", "surprised")])
    person("stroller", "man", 1, 2080, 1214, 0.62, 1, 3.34, walk=(1700, t_fly0 + 0.2, t_call + 0.5), seed=7,
           events=[(t_turn, -1, "stand", "surprised"), (t_worry, -1, "listen", None)])
    # a woman watching the market, a little behind Jonah's path (he walks past in front of her)
    person("woman_fl", "woman", 3, 1330, 1238, 0.7, 1, 3.6, seed=18,
           events=[(t_call + 0.55, 1, "stand", "surprised"), (t_turn + 0.12, 1, "listen", None),
                   (t_worry + 0.05, 1, "listen", "worried")])

    sc.add("st_back", street_back_svg(), z=2, motion=lambda t: Tf(alpha=in_a(t)))
    sc.add("step", step_svg(), z=4, motion=lambda t: Tf(alpha=in_a(t)))

    # ------------------------------------------------------------ Jonah (street)
    JSPR = person_sprite(JS, wide=190, tall=380, seed=91)
    with extra_exprs():
        F_WALK = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k), "neutral")) for k in range(2 * WALK_N)]
        F_MID = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "mid"), "call")) for k in range(2 * WALK_N)]
        F_UPC = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "up"), "call")) for k in range(2 * WALK_N)]
        F_UPS = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, walk_pose(k, "up"), "shout")) for k in range(2 * WALK_N)]
        F_CLIMB = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, CLIMB[k][0], "serious")) for k in range(K_CL, N_END + 1)]
        F_STAND = JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, STAND, "serious"))
        F_PR = [JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, PREACH, e)) for e in ("call_shut", "call", "shout")]
        F_END = JSPR.add(jfig(JSPR.ax, JSPR.ay, JS, STAND, "angry"))     # stern, as s16 opens

    def mouth(t, t0, per=0.19):
        return int(max(0.0, t - t0) / per) % 2 == 1

    def j_frame(t):
        if t < t_stop:
            k = walk_k(t)
            if k >= K_CL:
                return F_CLIMB[k - K_CL]
            km = k % (2 * WALK_N)
            if t < t_call:
                return F_WALK[km]
            if k < k_up or k >= k_dn:
                return F_MID[km]
            return F_UPS[km] if mouth(t, t_call + 0.1) else F_UPC[km]
        if t < t_preach:
            return F_STAND
        if t < t_down:
            f = int((t - L2.start) * ctx.fps + 1e-6)
            return F_PR[MOUTH[f] if 0 <= f < len(MOUTH) else 0]
        return F_END

    hops = [(t_stop, 0.7, False), (t_preach, 0.5, True), (t_down, 0.6, True),
            (k_time(K_CL + WALK_N), 0.8, False), (k_time(K_CL + 2 * WALK_N), 0.8, False)]   # climb landings

    def j_squash(t):
        sy, dy = 1.0, 0.0
        for ts, amp, up in hops:
            u = t - ts
            if -0.09 <= u <= 0.2:
                if u < 0:
                    sy *= 1 - 0.05 * amp * part(u, -0.09, 0, "sine")
                elif u < 0.07:
                    sy *= 1 - 0.05 * amp + 0.09 * amp * part(u, 0, 0.07, "sine")
                else:
                    sy *= 1 + 0.04 * amp - 0.04 * amp * part(u, 0.07, 0.2, "sine")
                if up:
                    dy -= 14 * amp * math.sin(math.pi * min(1.0, max(0.0, u / 0.2)))
        if t >= t_stop:
            sy *= 1 + 0.01 * math.sin(2 * math.pi * (t - t_stop) / 3.0)
        return sy, dy

    def j_fn(t):
        if not shown(t):
            return None
        sy, dy = j_squash(t)
        x, y = jonah_xy(t)
        return JSPR.place(j_frame(t), x, y, sx=1 / math.sqrt(sy), sy=sy, dy=dy, alpha=shown_a(t))

    # his shadow swings round with the sun (morning: long to the right, noon: short, afternoon: to the left)
    JSH = sprite(520, 120, 260, 60, wc=0)
    JSH_I = JSH.add(C.ground_shadow(260, 60, JS, 120, opacity=0.26))

    def jsh_fn(t):
        if not shown(t):
            return None
        rx = sun_rel(t)
        x, y = jonah_xy(t)
        k = walk_k(t)
        if t < t_stop and k >= K_CL:                 # on the step: under the planted foot's tread
            y = GY - treads(k // WALK_N)
        return JSH.place(JSH_I, x - 0.07 * rx, y, sx=1 + min(0.9, abs(rx) / 900), alpha=shown_a(t))
    sc.add_dynamic("jonah_sh", jsh_fn, z=4.9)
    sc.add_dynamic("jonah", j_fn, z=5)

    # sound arcs from his mouth while he calls (walking, then on the step)
    HEAD_PRE = C.body_points(C.jonah, 0, 0, JS, 1, pose="preach")["head"]
    HEAD_WALK = C.body_points(C.jonah, 0, 0, JS, 1, pose="walk_a")["head"]
    ARC = sprite(260, 260, 40, 130, wc=0)
    ARC_I = [ARC.add(arcs(40, 130, n, 1, 0.9)) for n in (1, 2, 3)]

    def arc_fn(t):
        on_walk = t_call + 0.1 <= t < t_calloff - 0.05 and walk_k(t) >= k_up
        on_step = t_preach + 0.05 <= t < L2.end + 0.1
        if not (on_walk or on_step) or not shown(t):
            return None
        hx, hy = HEAD_PRE if on_step else HEAD_WALK
        x, y = jonah_xy(t)
        return ARC.place(ARC_I[int(t * 7) % 3], x + hx + 56, y + hy + 22)
    sc.add_dynamic("arcs", arc_fn, z=20)

    # ------------------------------------------------------------ market front: people who stop and turn
    person("mother", "woman", 2, 2330, 1352, 0.86, -1, 6.0, walk=(2700, t_turn - 2.2, t_turn), seed=12,
           events=[(t_turn, -1, "stand", "surprised"), (t_wow + 0.55, -1, "point", "surprised"),
                   (t_worry + 0.1, -1, "listen", None)])
    person("girl", "child", 1, 2440, 1372, 0.86, -1, 6.1, walk=(2810, t_turn - 2.15, t_turn + 0.05, 1.15),
           seed=13, events=[(t_turn + 0.05, -1, "stand", "surprised"), (t_worry + 0.3, -1, "sad", None)])
    person("elder", "elder", 0, 2590, 1346, 0.84, 1, 5.9, seed=14,
           events=[(t_turn + 0.15, -1, "stand", "surprised"), (t_worry + 0.25, -1, "listen", None)])
    person("man_r", "man", 0, 2700, 1400, 0.9, 1, 6.2, seed=15,
           events=[(t_turn + 0.1, -1, "stand", "surprised"), (t_phr2 + 0.3, -1, "listen", None)])
    # animals in the square
    ANI = sprite(820, 360, 410, 330, seed=16)
    ani_i = ANI.add(C.ground_shadow(250, 330, 0.56, 170) + PR.animal(250, 330, 0.56, 1, kind="donkey"))
    sc.add_dynamic("donkey", lambda t: (ANI.place(ani_i, 560 + 160, 1214, sy=1 + 0.012 * math.sin(t * 2.3),
                                                  alpha=shown_a(t)) if shown(t) else None), z=3.15)
    SHP = sprite(520, 260, 260, 230, seed=17)
    shp_i = SHP.add(C.ground_shadow(160, 230, 0.68, 160) + PR.animal(160, 230, 0.68, -1, kind="sheep")
                    + C.ground_shadow(360, 240, 0.6, 140) + PR.animal(360, 240, 0.6, -1, kind="sheep"))
    sc.add_dynamic("sheep_r", lambda t: (SHP.place(shp_i, 2860, 1420, dy=-2 * abs(math.sin(t * 1.3)))
                                         if shown(t) else None), z=6.3)

    # "!" marks over the surprised heads
    EXC = sprite(110, 120, 55, 75, wc=0)
    exc_i = EXC.add(exclaim(55, 75, 0.85))
    for i, nm in enumerate(("stroller", "mother", "elder", "man_r")):
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
           motion=M.combine(lambda t: Tf(dx=-0.22 * (camf(max(t, t_st)).x - CAM_END.x)),
                            lambda t: Tf(alpha=shown_a(t))))

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

    # little Jonah walks up the road (planted-foot walk: the drawing follows the distance walked), through the
    # gate and into the shade of the passage, which swallows him before the camera flies in after him
    LJ_S = 0.58
    LJ = person_sprite(LJ_S, wide=190, tall=380, seed=92)
    for k in range(2 * WALK_N):                        # drawings 0..11: the walk cycle
        LJ.add(C.ground_shadow(LJ.ax, LJ.ay, LJ_S, 120) + jfig(LJ.ax, LJ.ay, LJ_S, walk_pose(k), "neutral"))
    LJ_STAND = LJ.add(C.ground_shadow(LJ.ax, LJ.ay, LJ_S, 120) + jfig(LJ.ax, LJ.ay, LJ_S, STAND, "neutral"))
    t_lj0 = t_pull0 + 0.5                              # he stands and looks at the great city, then sets off
    lj_scale = lambda y: float(np.interp(y, [WALL_Y - 16, WALL_Y, 1450, 1700], [0.28, 0.33, 0.52, 0.58]))
    f_lo, f_hi = 0.0, 1.0                              # where on the road he is at the start (feet at y ~ 1390,
    for _ in range(30):                                # clear of the foreground palm)
        f_md = (f_lo + f_hi) / 2
        f_lo, f_hi = (f_md, f_hi) if road_point(f_md)[1] > 1390 else (f_lo, f_md)
    path = [road_point(f_lo + (1 - f_lo) * i / 240) for i in range(241)]
    n_road = len(path)
    path += [(GX + 9 * i / 12, WALL_Y - 16 * i / 12) for i in range(1, 13)]     # into the passage's depth
    figd = [0.0]
    for i, (a_, b_) in enumerate(zip(path, path[1:])):
        ds = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) * (1.0 if i < n_road - 1 else 1.15)   # foreshortened
        figd.append(figd[-1] + ds / lj_scale((a_[1] + b_[1]) / 2))
    ADV0 = 2 * WALK_A / WALK_N                         # figure px per drawing
    t_thr = t_fly0 - 0.6                               # his feet cross the threshold
    K_THR = figd[n_road - 1] / ADV0
    R_LJ = K_THR / (t_thr - t_lj0)                     # drawings / s
    K_LJ = int(figd[-1] / ADV0)
    t_lj_end = t_lj0 + (K_LJ + 0.999) / R_LJ

    def lj_at(k):
        dd = k * ADV0
        i = max(1, min(len(figd) - 1, int(np.searchsorted(figd, dd))))
        u = (dd - figd[i - 1]) / max(1e-6, figd[i] - figd[i - 1])
        x = M.lerp(path[i - 1][0], path[i][0], u)
        y = M.lerp(path[i - 1][1], path[i][1], u)
        return x, y, lj_scale(y)
    LJ_POS = [lj_at(k) for k in range(K_LJ + 1)]

    def lj_fn(t):
        k = min(K_LJ, int(max(0.0, t - t_lj0) * R_LJ + 1e-6))
        dark = part(t, t_thr, t_lj_end, "sine")
        if dark > 0.93 or t >= t_fly0 - 0.02:          # gone into the shade (he matches it by now): cut
            return None
        x, y, s = LJ_POS[k]
        # the walk starts on a passing drawing (feet together), the closest to his standing pose
        res = LJ.place(LJ_STAND if t < t_lj0 else (k + 3) % (2 * WALK_N), x, y, sx=s / LJ_S, sy=s / LJ_S)
        if dark <= 0.01:
            return res
        im, (px, py) = res
        arr = np.asarray(im).astype(np.float32)
        rows = np.array([passage_color(py + r) for r in range(arr.shape[0])], np.float32)[:, None, :]
        arr[..., :3] = arr[..., :3] * (1 - dark) + rows * dark
        return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA"), (px, py)
    sc.add_dynamic("p_jonah", lj_fn, z=57)

    # foreground palms (sway)
    for i, (x, y, s, ln) in enumerate(((60, 1850, 1.3, 0.32), (3170, 1860, 1.15, -0.32))):
        sw = M.sway(0.8, 4.4 + i * 0.6, (x, y), phase=i * 0.3)
        sc.add(f"p_palm{i}", doc(PR.palm_tree(x, y, s, lean=ln)), z=58 + i * 0.1, motion=F(local=sw, pivot=(x, y)))

    # doves over the city
    pd = ((900, 520, 0.5), (990, 470, 0.42), (840, 455, 0.4))
    sc.add("p_doves", [doves_svg(k, pd) for k in range(3)], z=59, frame_at=lambda t: float(int(t * 8) % 3),
           motion=F(local=M.combine(M.drift(vx=70, vy=-5), M.bob(10, 1.6)), pivot=(900, 500)))

    # the three-days device: footprint trail + suns
    trail_fade = lambda t: 1 - part(t, L0.end - 0.4, L0.end + 0.2, "sine")

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
        morning, noon, gold = (255, 240, 236), (255, 255, 255), (255, 246, 230)
        if t < t_fly0:
            return noon
        if t < t_st:
            return [M.lerp(a, b, part(t, t_fly0, t_st, "sine")) for a, b in zip(noon, morning)]
        u1 = part(t, t_st, t_st + 1.6, "sine")
        u2 = part(t, t_call - 0.9, t_calloff + 0.4, "sine")
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
    # the street's bustle, then a hush while the whole square stops to listen to Jonah
    sc.sfx("crowd", t_fly0 + 0.2, dur=t_turn + 0.35 - (t_fly0 + 0.2), gain_db=-16, fade_in=0.6, fade_out=0.5)
    sc.sfx("crowd", t_turn - 0.1, dur=T - t_turn + 0.9, gain_db=-24, fade_in=0.5, fade_out=0.8)
    sc.sfx("footsteps", t_fly0, dur=t_stop - t_fly0, gain_db=-13, fade_in=0.2, fade_out=0.2, rate=R0 / WALK_N)
    sc.sfx("pop", t_wow, gain_db=-14)

    # rasterise all sprite drawings now (fills the disk caches during the prepare pass, so render workers only
    # load PNGs) and close the browser if we opened it
    for sp in _SPRITES:
        sp.load()
    raster.close()
    return sc
