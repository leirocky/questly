"""Scene 8 - the storm comes (Mark 4:37): 忽然，起了一阵大风。呼——呼——！乌云跑过来，把月亮都遮住了。
浪一个接一个打进船里，哗啦！哗啦！船里的水越来越多。

This module also holds THE SHARED WORLD of the five boat scenes s08 - s12 (one stage, one boat, one crew, one sky
and lake): s09_scared, s10_wake, s11_calm and s12_question import it, so the plain cross-dissolves between them
match exactly. Everything that keeps moving through a dissolve (the swell under the boat, the wave / sail / water
flipbooks, the racing cloud banks, rain and wind streaks) is keyed to FILM time (scene start + t, whole frames), so
the last second of one scene and the first second of the next draw the very same frames.

The world: a 3200 x 1800 stage; the fishing boat (props.fishing_boat, bow to the right) at (1600, 1150), scale 0.8,
with everybody in it at the same scale; storm_lake at scale 1.1 with the boat at LEVEL + STORM_BOAT_DY * 1.1; the
moon high on the right (2330, 330); the wind blows from the left (clouds race, rain falls and streaks curl to the
right). Jesus sleeps on the stern cushion (left). The twelve keep their places all through:
    far row (behind):  Philip -400, Bartholomew -250, Matthew -100, Thaddaeus 60, James son of Alphaeus 340, Judas 480
    near row (front):  Andrew -330, James -170, Thomas 10, Peter 150 (the mast: 'cling'), John 390, Simon 540
Layers (z): night sky 0, far hills .5, storm sky 1, moon 1.5, cloud banks 2 - 2.5, calm lake 4, storm lake (back) 5,
boat back 10, sail 10.5, far row 11, (Jesus' glow 11.9), Jesus 12, near row 13, boat front 14, lantern 14.5,
splashes 15, storm lake (front) 16, calm lake in front of the hull 16.5.

Beats of this scene (from the voice-measured phrase marks of the take, see beat()):
  start         a calm, starry night (s07's mood): the moon, stars twinkling, a silver lake with the moon's path,
                far hills with a few lit windows; the boat sails gently (full sail, the lantern glowing); the crew
                relaxed, Jesus asleep on the cushion at the stern.
  '忽然'         a first gust: wind streaks sweep across, the sail snaps loose and flaps, the boat lurches, the
                lantern swings; everybody looks up, worried, kerchief tails streaming.
  '起了一阵大风'  the wind builds; the silver lake ruffles into grey waves (calm_lake -> storm_lake .05 -> .2);
                Peter grabs the mast.
  '呼—' '呼—'   one big gust on each 呼 (sweeping streaks, a lurch, whoosh): the dark cloud banks race in from the
                left; the crew get scared (arms up), John grabs the sail rope; the waves rise (.5).
  '乌云跑过来'    the banks race across; the sky turns storm grey; the far hills vanish.
  '把月亮都遮住了' the high bank sweeps over the moon and hides it (its glow and path go out); the rain begins.
  '浪一个接一个打进船里' the waves grow one after another (.5 -> 1); small spray bursts at the bow.
  '哗啦！' x2    a wave bursts over the near gunwale (amidships, then by the bow): spray, a lurch, camera bump,
                splash; everybody is soaked; water sloshes inside (0 -> .2 -> .35).
  '船里的水越来越多' the water inside rises (.35 -> .5); Jesus still sleeps, peaceful.
  end           the full storm held steady (= the first frame of s09_scared: plain cross-dissolve).
"""
import math
import random
import zlib

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import IDENTITY, Cam, Tf
from engine.paths import OUT_H, OUT_W
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, voice_marks

INK = P["ink"]

# ================================================================== the shared world (s08 - s12)
SW, SH = 3200, 1800             # one stage for the five boat scenes
K = 0.8                         # the boat and everybody in it
SL = 1.1                        # storm_lake scale (STORM_BOAT_DY is measured in lake units)
BX, BY = 1600, 1150             # the boat's anchor (waterline under the middle of the hull), bow to the right
FACING = 1
LEVEL = BY - PR.STORM_BOAT_DY * SL      # storm_lake far edge
HORIZON = LEVEL - 33                    # the visible horizon (storm and calm)
SKY_BOT = HORIZON + 90
MOON = (2330, 330)
MOON_R = 62
BP = PR.boat_points(BX, BY, K, FACING)
FPS = 30
STORM = PR.STORM_SKY_COLS
HOOK = (BX - 760 * K, BY - 352 * K)     # the stern-post lantern hook (fishing_boat's own lantern place)
DECK_Y = BY - 178 * K                   # Jesus standing on the stern deck
DECK_X = BX - 560 * K
LAKE_BOTTOM = 1720                      # nothing below this is ever seen
WAVES = 8                               # storm_lake phases (one every 3 film frames)

# the twelve: name -> (variant, local x, row); the far row stands 40 px higher behind
CREW = {
    "philip": (4, -400, "far"), "bartholomew": (5, -250, "far"), "matthew": (6, -100, "far"),
    "thaddaeus": (9, 60, "far"), "jamesa": (8, 340, "far"), "judas": (11, 480, "far"),
    "andrew": (1, -330, "near"), "james": (2, -170, "near"), "thomas": (7, 10, "near"),
    "peter": (0, 150, "near"), "john": (3, 390, "near"), "simon": (10, 540, "near"),
}
FAR = [n for n, v in CREW.items() if v[2] == "far"]
NEAR = [n for n, v in CREW.items() if v[2] == "near"]
Z_ROW = {"far": 11.0, "near": 13.0}


def spot(lx, row="near"):
    """Stage point of a boat-local floor spot (tilt 0)."""
    return BX + lx * K * FACING, BY + (PR.BOAT_FAR_FLOOR_Y if row == "far" else 0) * K


def foot_of(name):
    _v, lx, row = CREW[name]
    return spot(lx, row)


def z_of(name):
    _v, lx, row = CREW[name]
    return Z_ROW[row] + (lx + 800) / 20000


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def seed_of(name):
    return zlib.crc32(name.encode()) % 9973


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


# ------------------------------------------------------------------ time
def gframe(ctx, t):
    """Film frame index of scene time t (exact, so neighbouring scenes agree inside the cross-dissolves)."""
    return int(round((ctx.start + t) * FPS))


def gtime(ctx, t):
    return gframe(ctx, t) / FPS


def keyed(keys, curve="inout"):
    """Scalar keyframes [(t, v)] -> f(t), eased between keys."""
    ks = sorted(keys, key=lambda k: k[0])

    def f(t):
        if t <= ks[0][0]:
            return ks[0][1]
        for (ta, a), (tb, b) in zip(ks, ks[1:]):
            if t <= tb:
                return a + (b - a) * M.progress(t, ta, tb, curve)
        return ks[-1][1]
    return f


def beat(ctx, li, phrase, k=0):
    """Onset (scene s) of the k-th occurrence of ``phrase`` in line li: the voice-measured phrase marks of the
    take (pauses found in the clip; the Noah film's helpers), the character offset inside the phrase."""
    n = 0
    for ent in voice_marks(ctx, li):
        pos = ent[0].find(phrase)
        while pos >= 0:
            if n == k:
                return char_times(ent)[pos]
            n += 1
            pos = ent[0].find(phrase, pos + 1)
    raise KeyError(phrase)


def phrase_end(ctx, li, phrase):
    for ent in voice_marks(ctx, li):
        if phrase in ent[0]:
            return ent[2]
    raise KeyError(phrase)


def tri(u):
    """Triangle wave 0 -> 1 -> 0 over one unit."""
    u = u % 1.0
    return 2 * u if u < 0.5 else 2 - 2 * u


# ------------------------------------------------------------------ camera
def clamp_cam(c, margin=6):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), SH - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys, bumps=()):
    """[(t, Cam)] eased (sine) camera moves inside the stage, plus little bumps [(t0, amp px, dur)]."""
    ks = [(t, clamp_cam(c)) for t, c in sorted(keys, key=lambda k: k[0])]

    def cam(t):
        c = ks[0][1] if t <= ks[0][0] else ks[-1][1]
        for (t0, a), (t1, b) in zip(ks, ks[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                c = Cam(M.lerp(a.x, b.x, u), M.lerp(a.y, b.y, u), M.lerp(a.w, b.w, u))
                break
        dx = dy = 0.0
        for t0, amp, dur in bumps:
            if t0 <= t <= t0 + dur:
                u = (t - t0) / dur
                e = amp * (1 - u) ** 2 * min(1.0, u / 0.08)
                dx += e * math.sin((t - t0) * 47.0)
                dy += e * math.cos((t - t0) * 39.0)
        if dx or dy:
            c = Cam(min(max(c.x + dx, c.w / 2 + 1), SW - c.w / 2 - 1),
                    min(max(c.y + dy, c.w * 9 / 32 + 1), SH - c.w * 9 / 32 - 1), c.w)
        return c
    return cam


# ------------------------------------------------------------------ the boat's rocking
def _rw(g):
    return 0.72 * math.sin(2 * math.pi * g / 3.4) + 0.28 * math.sin(2 * math.pi * g / 1.9 + 1.3)


def _bw(g):
    return 0.7 * math.sin(2 * math.pi * g / 2.6 + 0.4) + 0.3 * math.sin(2 * math.pi * g / 1.45 + 2.0)


def _kick(u):
    """A lurch: quick rise, slow settle (peak ~1 at u ~ 0.16 s), exactly 0 after 1.4 s."""
    if u <= 0 or u >= 1.4:
        return 0.0
    w = 1.0 if u < 0.9 else 1 - M.progress(u, 0.9, 1.4, "sine")
    return 1.38 * (1 - math.exp(-u / 0.07)) * math.exp(-u / 0.45) * w


STORM_TILT, STORM_BOB = 4.5, 8.0         # the steady storm swell at every storm seam (s08|s09|s10|s11)
CALM_TILT, CALM_BOB = 0.9, 2.5           # the gentle rocking on calm water (s08 start, s11|s12)


class Rock:
    """Tilt (deg) and bob (px at scale 1) of the boat: a swell keyed to film time (neighbouring scenes rock alike
    through a dissolve) times an amplitude envelope amp(t) / bob(t), plus lurches [(t0, deg, bob)] and an optional
    extra(t) -> (deg, bob) (a slow dip)."""

    def __init__(self, ctx, amp, bob, kicks=(), extra=None):
        self.ctx, self.amp, self.bob_amp, self.kicks, self.extra = ctx, amp, bob, list(kicks), extra

    def tilt(self, t):
        v = self.amp(t) * _rw(gtime(self.ctx, t))
        for t0, deg, _b in self.kicks:
            v += deg * _kick(t - t0)
        if self.extra:
            v += self.extra(t)[0]
        return max(-8.0, min(8.0, v))

    def bob(self, t):
        v = self.bob_amp(t) * _bw(gtime(self.ctx, t))
        for t0, _d, b in self.kicks:
            v += b * _kick(t - t0)
        if self.extra:
            v += self.extra(t)[1]
        return max(-15.0, min(15.0, v))

    def tf(self, t):
        return Tf(dy=self.bob(t) * K, rot=self.tilt(t), px=BX, py=BY)


def on_boat(rock, foot, own=None):
    """Motion of something standing at ``foot`` in the boat: its own motion (pivot at the foot) then the boat's."""
    fx, fy = foot

    def m(t):
        b = rock.tf(t)
        o = own(t) if own else IDENTITY
        ox, oy = fx + o.dx, fy + o.dy
        a = math.radians(b.rot)
        c, s = math.cos(a), math.sin(a)
        rx = BX + c * (ox - BX) - s * (oy - BY) + b.dx
        ry = BY + s * (ox - BX) + c * (oy - BY) + b.dy
        return Tf(dx=rx - fx, dy=ry - fy, rot=b.rot + o.rot, sx=o.sx, sy=o.sy, alpha=o.alpha, px=fx, py=fy)
    return m


def breath(ctx, amount=0.008, period=3.2, phase=0.0):
    """Breathing (a small vertical stretch at the feet), keyed to film time."""
    return lambda t: Tf(sy=1 + amount * math.sin(2 * math.pi * (gtime(ctx, t) / period + phase)))


def hop(t0, keys, curves="sine"):
    return M.keys([(t0 + dt, d) for dt, d in keys], curves)


def dip(t0, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * K, "sy": 0.95}),
                    (0.13, {"dy": -3 * K, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], ["in", "out", "sine"])


def flinch(t0, dx=-10.0, depth=6.0):
    """Recoil from a splash: a quick squash and a lean away, then back."""
    return hop(t0, [(0, {"dx": 0, "dy": 0, "sy": 1, "rot": 0}),
                    (0.12, {"dx": dx * K, "dy": depth * K, "sy": 0.96, "rot": -1.5 * (1 if dx > 0 else -1)}),
                    (0.55, {"dx": 0, "dy": 0, "sy": 1, "rot": 0})], ["out", "sine"])


def jitter(ctx, t0, t1, amp=3.0, step=3, seed=1, ramp=0.25):
    """Fear tremble: a small sideways jitter changing every ``step`` film frames, inside [t0, t1] (ramping in and out
    over ``ramp`` s; pass t0 < 0 / t1 > T to have it fully on at a scene's start / end)."""
    def m(t):
        if t < t0 or t > t1:
            return IDENTITY
        e = min(1.0, (t - t0) / ramp if ramp else 1.0, (t1 - t) / ramp if (ramp and t1 < 1e8) else 1.0)
        k = gframe(ctx, t) // step
        r = random.Random(k * 7919 + seed).uniform(-1, 1)
        return Tf(dx=amp * K * e * r)
    return m


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


class Actor:
    """One figure (or prop) riding in the boat, on its own flipbook layer: hard cuts between drawings (at()), film-
    time keyed cycles (cycle()), cross-fades only between drawings that differ in colour (xfade: dry -> wet), own
    motions (move(); pivot at the foot) + the boat's rocking."""

    def __init__(self, ctx, name, foot, rock, z=None):
        self.ctx, self.name, self.foot, self.rock = ctx, name, foot, rock
        self.z = z if z is not None else z_of(name)
        self.bodies, self.idx, self.segs, self.motions = [], {}, [], []

    def frame(self, body):
        if body not in self.idx:
            self.idx[body] = len(self.bodies)
            self.bodies.append(body)
        return self.idx[body]

    def at(self, t0, body):
        self.segs.append((t0, ("hold", self.frame(body))))
        return self

    def cycle(self, t0, bodies, step=3, offset=0):
        ids = [self.frame(b) for b in bodies]
        self.segs.append((t0, ("cycle", ids, step, offset)))
        return self

    def xfade(self, t0, t1, a, b):
        """Cross-fade a -> b (the same pose, different colouring) over [t0, t1]; then hold b."""
        i = len(self.bodies)
        self.bodies += [a, b]
        self.idx.setdefault(a, i)
        self.idx.setdefault(b, i + 1)
        self.segs.append((t0, ("xfade", i, t0, t1)))
        return self

    def move(self, *ms):
        self.motions += [m for m in ms if m]
        return self

    def frame_at(self, t):
        seg = self.segs[0][1]
        for t0, s in self.segs:
            if t >= t0:
                seg = s
        if seg[0] == "hold":
            return float(seg[1])
        if seg[0] == "cycle":
            ids, step, off = seg[1], seg[2], seg[3]
            return float(ids[(gframe(self.ctx, t) // step + off) % len(ids)])
        i, a, b = seg[1], seg[2], seg[3]
        return i + M.progress(t, a, b, "sine")

    def add(self, sc, wc=1.0):
        self.segs.sort(key=lambda s: s[0])
        own = M.combine(*self.motions) if self.motions else None
        frames = [doc(b) for b in self.bodies]
        sc.add(self.name, frames, z=self.z, motion=on_boat(self.rock, self.foot, own),
               frame_at=self.frame_at if len(frames) > 1 else None, wc=wc, seed=seed_of(self.name))
        return self


# ================================================================== drawings
def night_body(progress=1.0):
    return PR.night_sky(-20, -20, SW + 20, SKY_BOT, moon=None, stars=90, progress=progress, twinkle=0.35, seed=4)


def hills_body():
    """Low far hills round the lake at night (a few lit windows of far villages)."""
    rng = random.Random(5)
    out = ""
    for col, y0, amp in (("#4a4f86", HORIZON + 2, 150), ("#3b4174", HORIZON + 8, 80)):
        pts = [(-60, y0)]
        x = -60
        while x < SW + 120:
            x += rng.uniform(170, 320)
            pts.append((x, y0 - amp * rng.uniform(0.35, 1.0)))
        pts.append((SW + 60, y0))
        d = S.smooth_path(pts, closed=False, tension=0.7) + f" L{SW + 60},{HORIZON + 60} L-60,{HORIZON + 60} Z"
        out += S.path(d, col, sw=3.2)
    for x, dy in ((420, 26), (452, 30), (488, 24), (2740, 22), (2772, 27), (3010, 25)):
        out += f'<rect x="{x}" y="{HORIZON - dy}" width="9" height="9" rx="2" fill="{P["glow"]}" opacity="0.9"/>'
    return S.g(out, filter="wobble")


def moon_body(part="disc"):
    mx, my = MOON
    mr = MOON_R
    if part == "halo":
        gid = "s8moonhalo"
        return (f'<defs>{S.rad_grad(gid, [(0, "#f8f2dc", 0.6), (0.35, "#d8dcf0", 0.24), (1, "#d8dcf0", 0)])}</defs>'
                f'<circle cx="{mx}" cy="{my}" r="{mr * 4.6:.0f}" fill="url(#{gid})"/>')
    out = PR._circ(mx, my, mr, "#f6f0da", 3, stroke=S.mix(INK, "#f6f0da", 0.5))
    for (dx, dy, r) in ((-0.3, -0.2, 0.18), (0.25, 0.15, 0.13), (-0.05, 0.38, 0.1), (0.35, -0.3, 0.08)):
        out += PR._circ(mx + dx * mr, my + dy * mr, r * mr, "#e4dcc0", 0, extra='opacity="0.8"')
    return S.g(out, filter="wobble-fine")


def storm_grad_body():
    return PR.storm_sky(-20, -20, SW + 20, SKY_BOT, density=0.0, wind=0.0, seed=2)


# storm cloud banks: looping strips (period = the stage width) racing left -> right, keyed to film time
BANKS = {
    # name: (seed, y band (top, bottom), cloud width range, colour, speed px/s, count)
    "high": (11, (60, 560), (560, 860), STORM[2], 44.0, 7),
    "low": (23, (520, 1010), (700, 1080), S.shade(STORM[1], -0.05), 105.0, 7),
}
MOON_CLOUD_X = 1600              # the big cloud of the high bank that slides over the moon


def bank_clouds(name):
    seed, (y0, y1), (w0, w1), _col, _v, n = BANKS[name]
    rng = random.Random(seed)
    out = []
    for i in range(n):
        x = (i + rng.uniform(-0.25, 0.25)) * SW / n
        w = rng.uniform(w0, w1)
        h = w * rng.uniform(0.32, 0.42)
        y = rng.uniform(y0 + h * 0.5, y1 - h * 0.4)
        out.append((x, y, w, h, seed * 31 + i))
    if name == "high":
        out.append((MOON_CLOUD_X, MOON[1] + 70, 860, 330, 977))
    return out


def bank_body(name):
    _seed, _band, _w, col, _v, _n = BANKS[name]
    light = S.mix(col, STORM[3], 0.38)
    out = ""
    for x, y, w, h, sd in bank_clouds(name):
        for xx in (x - SW, x, x + SW):
            if xx + w < -10 or xx - w > SW + 10:
                continue
            out += S.cloud(xx, y, w, h, fill=col, seed=sd, puffs=6, sw=3.8, shade_fill=S.shade(col, -0.25))
            out += S.cloud(xx - w * 0.06, y - h * 0.08, w * 0.55, h * 0.5, fill=light, seed=sd + 7, puffs=4, sw=2.6)
    return S.g(out, filter="wobble")


_S8 = {}


def s08_cover():
    """Film time when the high bank's big cloud is centred on the moon (s08 '遮住'): all scenes place the banks
    from it, so they agree through every dissolve."""
    if "g" not in _S8:
        from engine.loader import context
        c = context("s08_storm")
        _S8["g"] = gtime(c, beat(c, 0, "遮住") - 0.1)
    return _S8["g"]


def bank_x(ctx, name, t, slow=None):
    """Offset (0..SW) of a bank strip at scene time t. slow(t) = seconds 'lost' (a slow-down in s11)."""
    v = BANKS[name][4]
    off = (MOON[0] - MOON_CLOUD_X - v * s08_cover()) if name == "high" else 0.0
    g = gtime(ctx, t) - (slow(t) if slow else 0.0)
    return (off + v * g) % SW


def calm_body(phase=0.0, glow=1.0, front=False):
    body = PR.calm_lake(-20, SW + 20, HORIZON, phase=phase, moon_x=MOON[0], bottom=LAKE_BOTTOM, glow=glow, seed=6)
    if not front:
        return body
    # the same water in front of the hull (hides it below the waterline), a soft shadow and waterline ripples
    cid = "s8calmfront"
    y0 = BY - 3
    shade_ = (f'<ellipse cx="{BX - 20}" cy="{y0 + 30}" rx="{640 * K:.0f}" ry="24" fill="#1d2550" opacity="0.32" '
              f'filter="url(#soft)"/>')
    rip = ""
    for i, (x0, x1, dy) in enumerate(((-560, -300, 10), (-200, 120, 16), (210, 470, 9), (-420, -120, 30),
                                      (60, 380, 34), (-720, -600, 6), (560, 700, 7))):
        rip += (f'<path d="M{BX + x0 * K:.0f},{y0 + dy} q{(x1 - x0) * K / 2:.0f},-5 {(x1 - x0) * K:.0f},0" '
                f'fill="none" stroke="{PR.CALM_WATER[3]}" stroke-width="3.2" stroke-linecap="round" '
                f'opacity="{0.55 - 0.04 * i:.2f}"/>')
    return (f'<clipPath id="{cid}"><rect x="-20" y="{y0}" width="{SW + 40}" height="{SH - y0 + 40}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{body}{shade_}</g>' + S.g(rip, filter="wobble-fine"))


CALM_PH = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10]      # the calm lake's ripples drift back and forth through these


def calm_frame_at(ctx, period=12.0):
    n = len(CALM_PH)
    return lambda t: tri(gtime(ctx, t) / period) * (n - 1)


ROW_V = (34.0, -52.0, 78.0, -110.0)    # px/s of the four wave rows (alternating directions, nearer = faster)
ROWS = [(0, 10, 26, 320, 2, 1), (40, 14, 52, 400, 1, -1), (110, 18, 86, 500, None, 1), (210, 24, 118, 600, 0, -1)]


def row_len(i):
    return ROWS[i][3] * SL


def _row_col(i):
    c = ROWS[i][4]
    return S.mix(PR.STORM_WATER[1], PR.STORM_WATER[0], 0.5) if c is None else PR.STORM_WATER[c]


def lake_row_body(i, wave, bottom=None, seed=3):
    """Row i (0 far .. 3 near) of props.storm_lake, drawn with that function's own shapes and colours but one row per
    layer and with identical foam caps on every crest, so the row is exactly periodic (wavelength row_len(i)) and
    can slide smoothly sideways (the props' phase loop jumps 1-2 wavelengths per loop). Row 0 carries the base
    water; the near rows sit a little higher for small waves so they still hide the keel."""
    s = SL
    wv = clamp(wave, 0.0, 1.2)
    x0, x1 = -20, SW + 20
    if bottom is None:
        bottom = LAKE_BOTTOM if i >= 2 else BY + 170
    level = LEVEL - (26 * (1 - min(1.0, wave)) if i >= 2 else 0.0)
    dy, a0, a1, L, _c, dirn = ROWS[i]
    A, L = (a0 + a1 * wv) * s, L * s
    col = _row_col(i)
    yy = level + dy * s
    p_ = i * 1.7
    out = ""
    if i == 0:
        out += PR._rect(x0 - 40, level - 30 * s, x1 - x0 + 80, bottom - level + 30 * s, PR.STORM_WATER[2], 0)
    pts = PR._crest_wave(x0 - 60, x1 + 60, yy, A, L, p_, 1.4 + 0.5 * wv)
    d = PR._sm(pts, closed=False) + f" L{f1(x1 + 60)},{f1(bottom)} L{f1(x0 - 60)},{f1(bottom)} Z"
    out += PR._p(d, col, 3.4 * s, stroke=S.shade(col, -0.45) if i else INK)
    cid = PR._uid("s8row", i, round(wv, 3), bottom)
    lit = [(px, py + 6 * s) for px, py in pts] + [(px, py + A * 0.45 + 16 * s) for px, py in reversed(pts)]
    inner = PR._p(PR._poly(lit), S.shade(col, 0.2), 0, extra='opacity="0.55"')
    inner += PR._p(PR._sm([(px, py + A * 0.75 + 22 * s) for px, py in pts], closed=False), sw=3 * s,
                   stroke=S.shade(col, 0.28), extra='opacity="0.5"')
    out += PR._clip(cid, d, inner)
    if wv > 0.05:
        caps = ""
        for k in range(-2, int((x1 - x0 + 120) / L) + 3):
            cx = (k - p_ / (2 * math.pi)) * L
            if cx < x0 - 80 - L * 0.5 or cx > x1 + 80 + L * 0.5:
                continue
            ty = yy - A
            cw = (20 + 34 * wv) * s * (1 + 0.22 * i)
            caps += PR._foam_cap(cx, ty, cw, A, dirn, s, S.shade(col, -0.35), seed + i)
            for j in range(3):
                fx = cx - dirn * cw * (1.0 + 0.55 * j)
                caps += PR._p(f"M{f1(fx)},{f1(ty + A * (0.40 + 0.18 * j))} q{f1(dirn * 18 * s)},{f1(-8 * s)} "
                              f"{f1(dirn * 38 * s)},{f1(2 * s)}", sw=(3.6 - 0.7 * j) * s, stroke=PR.STORM_FOAM,
                              extra=f'opacity="{0.85 - 0.2 * j:.2f}"')
            if i >= 1:
                rng = random.Random(seed * 31 + i)
                for j in range(5):
                    a = rng.uniform(-2.6, -0.5)
                    r = rng.uniform(20, 70) * s
                    caps += PR._circ(cx + dirn * 20 * s + r * math.cos(a) * dirn, ty + r * math.sin(a),
                                     rng.uniform(2.5, 5.5) * s, PR.STORM_FOAM, 1.4 * s, stroke=S.shade(col, -0.3))
        out += caps
    return f'<g filter="url(#wobble)">{out}</g>'


def row_dx(ctx, i, t, slow=None):
    """Sideways offset of row i at scene time t: film-time keyed, wrapped by one wavelength (centred)."""
    L = row_len(i)
    g = gtime(ctx, t) - (slow(t) if slow else 0.0)
    return ((ROW_V[i] * g + L / 2) % L) - L / 2


def row_heave(ctx, i, t):
    return 3.5 * math.sin(2 * math.pi * gtime(ctx, t) / (2.1 + 0.37 * i) + 1.9 * i)


def boat_back_body(wet=False):
    return PR.fishing_boat(BX, BY, K, FACING, sail="none", flag=False, wet=wet, part="back", oars="in")


def boat_front_body(water=0.0, phase=0.0, wet=False):
    return PR.fishing_boat(BX, BY, K, FACING, sail="none", flag=False, water=water, phase=phase, wet=wet,
                           part="front", oars="in")


def sail_body(state="full", phase=0.0, haul=0.0, flag=None):
    """The sail, the yard, its sheets and the pennant (fishing_boat's own drawing, on a layer of its own).
    haul 0..1 brails the flapping sail up toward the yard (s09: John hauling on the rope)."""
    rig = 3.4
    stay = S.shade(INK, 0.12)
    mx, mtop = PR.BOAT_MAST_TOP
    fp = phase if flag is None else flag
    w1 = 10 * math.sin(2 * math.pi * fp)
    out = PR._p(f"M{mx},{mtop + 6} Q{mx + 40},{f1(mtop - 10 + w1)} {mx + 86},{f1(mtop + 2 - w1)} "
                f"Q{mx + 50},{f1(mtop + 18 + w1)} {mx},{mtop + 26} Z", "#c9a24a", 3.2)
    out += PR._ell(mx, mtop, 15, 8, PR.BOAT_WOOD_DARK, 3.4)
    sid = PR._uid("s8sail", state, round(phase, 3), round(haul, 3))
    if state == "furled":
        out += PR._boat_sail("furled", phase, sid)
    else:
        sv, cl, cr = PR._boat_sail(state, phase, sid)
        if haul > 0:
            yt = PR.BOAT_YARD_Y + 8
            cut = cl[1] + (yt + 40 - cl[1]) * haul           # the foot rises toward the yard
            cid = PR._uid("s8haul", round(phase, 3), round(haul, 3))
            out += (f'<clipPath id="{cid}"><rect x="-400" y="-1100" width="1400" height="{f1(cut + 1100)}"/>'
                    f'</clipPath><g clip-path="url(#{cid})">{sv}</g>')
            pts = [(PR._lerp(-110, 570, u / 10), cut + 8 * math.sin(u * 2.3 + phase * 6)) for u in range(11)]
            roll = pts + [(x + 4, y + 26 + 6 * math.sin(i * 1.7)) for i, (x, y) in reversed(list(enumerate(pts)))]
            out += PR._p(PR._sm(roll, closed=True, tension=0.6), PR.SAIL_LINEN, 4)
            for u in (0.15, 0.4, 0.65, 0.88):
                xx = PR._lerp(-110, 570, u)
                out += PR._p(f"M{f1(xx - 10)},{f1(cut + 4)} Q{f1(xx)},{f1(cut + 22)} {f1(xx + 10)},{f1(cut + 4)}",
                             sw=2.4, stroke=S.shade(PR.SAIL_LINEN, -0.35))
            cl, cr = (-110, cut + 20), (570, cut + 20)
        else:
            out += sv
        if state == "flapping":
            a = math.sin(2 * math.pi * phase)
            out += PR._p(PR._sm([cl, (cl[0] - 60, cl[1] + 140 + 20 * a), (-420, -175)], closed=False), sw=rig,
                         stroke=stay)
            out += PR._p(PR._sm([cr, (cr[0] + 40 + 30 * a, cr[1] + 160), (640, -190)], closed=False), sw=rig,
                         stroke=stay)
        else:
            out += PR._line(cl[0], cl[1], -440, -165, sw=rig, color=stay)
            out += PR._line(cr[0], cr[1], 650, -195, sw=rig, color=stay)
    return PR._place(out, BX, BY, K, FACING)


def lantern_body():
    hx, hy = HOOK
    rope = PR._line(BX - 752 * K, BY - 372 * K, hx, hy, sw=3)
    return rope + PR.hanging_lantern(hx, hy, K * 0.8, swing=0.0, lit=True)


def disciple(name, pose="stand", expr=None, phase=0.0, shake=0.0, item="bucket", wind=0.0, wet=False, facing=1,
             at=None, marks=True):
    v, _lx, _row = CREW[name]
    x, y = at if at else foot_of(name)
    return C.disciples(x, y, K, facing, variant=v, pose=pose, expr=expr, phase=phase, shake=shake, item=item,
                       wind=wind, wet=wet, marks=marks)


def jesus_body(pose="sleep", expr=None, wind=0.0, facing=1, at=None, marks=True, glow=0.0):
    if at is None:
        at = BP["sleep"] if pose in ("sleep", "wake") else (DECK_X, DECK_Y)
    return C.jesus(at[0], at[1], K, facing, pose=pose, expr=expr, wind=wind, marks=marks, glow=glow)


def _tongue(x, y, ang, L, w, bend=0.0):
    """One tongue of a splash: from a narrow base at (x, y) out to a round tip, starting ang degrees from straight up
    and curling a further ``bend`` degrees along its length. Returns path data and (tip x, tip y, dir x, dir y)."""
    n = 7
    axis, dirs = [(x, y)], []
    px, py = x, y
    for j in range(n):
        a = math.radians(ang + bend * (j / (n - 1)) ** 1.5)
        dx, dy = math.sin(a), -math.cos(a)
        dirs.append((dx, dy))
        px, py = px + dx * L / n, py + dy * L / n
        axis.append((px, py))
    left, right = [], []
    for j, (ax, ay) in enumerate(axis):
        dx, dy = dirs[min(j, n - 1)]
        nx, ny = -dy, dx
        ww = w * (0.28 + 0.72 * (j / n) ** 0.6) * 0.5
        left.append((ax - nx * ww, ay - ny * ww))
        right.append((ax + nx * ww, ay + ny * ww))
    dx, dy = dirs[-1]
    tx, ty = axis[-1]
    r = w * 0.5
    tip = [(tx + dx * r * 0.7 - dy * r * 0.7, ty + dy * r * 0.7 + dx * r * 0.7), (tx + dx * r, ty + dy * r),
           (tx + dx * r * 0.7 + dy * r * 0.7, ty + dy * r * 0.7 - dx * r * 0.7)]
    pts = left + tip[::-1] + right[::-1]
    pts = left[:-1] + [tip[2], tip[1], tip[0]] + right[::-1][1:]
    return S.smooth_path(pts, closed=True, tension=0.7), (tx + dx * r, ty + dy * r, dx, dy)


def spray_body(x, y, k, seed=0, side=1):
    """A wave bursting up over the near gunwale at stage (x, y): a picture-book splash - curling tongues of water
    fanning up and over with white foam caps, round drops flying from their tips, foam slapping the hull below.
    k 0..4: the crest hits, the burst, the full fan, falling back into the boat, last drops."""
    rng = random.Random(seed)
    foam, water, edge = PR.STORM_FOAM, "#a9c6d2", S.shade(PR.STORM_WATER[1], -0.4)
    L = (80, 190, 270, 215, 0)[k] * K
    spread = (26, 40, 52, 62, 0)[k]
    n = (4, 6, 7, 7, 0)[k]
    out, caps = "", []
    for i in range(n):
        u = i / max(1, n - 1) - 0.5
        ang = u * 2 * spread + 10 * side + rng.uniform(-5, 5)
        ln = L * (1 - 0.4 * abs(u) * 2) * rng.uniform(0.88, 1.1)
        bend = (1 if u >= 0 else -1) * (14 + 30 * abs(u)) + (24 if k == 3 else 0) * (1 if u >= 0 else -1)
        w = (46 + 18 * (1 - abs(u) * 2)) * K
        bx = x + u * 70 * K
        d, (tx, ty, dx, dy) = _tongue(bx, y, ang, ln, w, bend)
        out += f'<path d="{d}" fill="{water}" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>'
        d2, _ = _tongue(bx + 0.0, y, ang, ln * 0.8, w * 0.42, bend)
        out += f'<path d="{d2}" fill="{foam}" opacity="0.85"/>'
        if k in (1, 2, 3):
            caps.append((tx, ty, w * (0.42 if k < 3 else 0.32)))
        if k in (1, 2):                # a drop leaving the tip
            gap = (18 + 16 * k) * K
            dxp, dyp = tx + dx * gap, ty + dy * gap
            out += (f'<path d="{PR._raindrop_d(dxp, dyp, 8 * K + 3)}" fill="{water}" stroke="{INK}" '
                    f'stroke-width="2.4" transform="rotate({math.degrees(math.atan2(dx, -dy)):.0f} {f1(dxp)} {f1(dyp)})"/>')
    # white foam caps on the tongue tips
    blobs = []
    for cx, cy, r in caps:
        for j in range(3):
            blobs.append((cx + rng.uniform(-0.6, 0.6) * r, cy + rng.uniform(-0.5, 0.4) * r, r * rng.uniform(0.55, 0.85)))
    out += "".join(PR._circ(bx, by, br, foam, 2 * 3.0, stroke=INK) for bx, by, br in blobs)
    out += "".join(PR._circ(bx, by, br, foam, 0) for bx, by, br in blobs)
    # loose drops
    nd = (5, 10, 16, 20, 16)[k]
    for i in range(nd):
        a = rng.uniform(-155, -25) + 8 * side
        rr = rng.uniform(0.45, 1.2) * (L if L else 230 * K) * (1.15 if k >= 3 else 1.0)
        dx_, dy_ = math.cos(math.radians(a)) * rr, math.sin(math.radians(a)) * rr
        if k >= 3:
            dy_ += rng.uniform(30, 130) * K
        sz = rng.uniform(5, 9) * K + 2
        out += (f'<path d="{PR._raindrop_d(x + dx_, y + dy_, sz)}" fill="{foam}" stroke="{edge}" '
                f'stroke-width="2"/>')
    # foam slapping the hull below the gunwale
    if k <= 3:
        m = (6, 9, 9, 6)[k]
        hb = [(x + (i / (m - 1) - 0.5) * (120 + 60 * k) * K, y + rng.uniform(10, 46) * K,
               rng.uniform(18, 30) * K * (1.0 if k < 3 else 0.7)) for i in range(m)]
        out += "".join(PR._circ(bx, by, br, foam, 2 * 3.0, stroke=INK) for bx, by, br in hb)
        out += "".join(PR._circ(bx, by, br, foam, 0) for bx, by, br in hb)
    return S.g(out, filter="wobble-fine")


def add_spray(sc, ctx, rock, name, t0, lx, seed=0, side=1, scale=1.0, z=15.0):
    """A spray burst over the near gunwale at boat-local x (rides with the boat), starting at t0 (~0.75 s)."""
    gx = BX + lx * K
    gy = BY + PR._ng(lx) * K + 4
    times = [0.0, 0.07, 0.17, 0.33, 0.52]
    bodies = [doc(spray_body(gx, gy, k, seed, side)) for k in range(5)]

    def fa(t):
        u = t - t0
        i = 0
        for k, tk in enumerate(times):
            if u >= tk:
                i = k
        return float(i)

    def own(t):
        u = t - t0
        if u < 0 or u > 0.8:
            return Tf(alpha=0.0)
        a = 1.0 - clamp((u - 0.55) / 0.25)
        s = scale * (0.85 + 0.15 * clamp(u / 0.2))
        return Tf(alpha=a, sx=s, sy=s)
    sc.add(name, bodies, z=z, frame_at=fa, motion=on_boat(rock, (gx, gy), own), wc=0.4, seed=seed_of(name))


# ================================================================== shared layer builders
def add_night(sc, ctx, alpha=None, progress=None, steps=(0.0, 0.25, 0.5, 0.75, 1.0)):
    """The night sky (z 0): static, or a flipbook over star progress (stars appearing) when progress(t) is given."""
    if progress is None:
        sc.add("night", doc(night_body(1.0)), z=0, wc=0.45, seed=seed_of("night"),
               motion=(lambda t: Tf(alpha=alpha(t))) if alpha else None)
        return
    n = len(steps)

    def fa(t):
        p = progress(t)
        for i in range(n - 1):
            if p <= steps[i + 1]:
                return i + (p - steps[i]) / (steps[i + 1] - steps[i])
        return float(n - 1)
    sc.add("night", [doc(night_body(p)) for p in steps], z=0, wc=0.45, seed=seed_of("night"), frame_at=fa,
           motion=(lambda t: Tf(alpha=alpha(t))) if alpha else None)


def add_moon(sc, halo, disc, hills=None):
    sc.add("moon_halo", doc(moon_body("halo")), z=1.5, wc=0.0, seed=seed_of("moon_halo"),
           motion=lambda t: Tf(alpha=halo(t)))
    sc.add("moon", doc(moon_body("disc")), z=1.6, wc=0.5, seed=seed_of("moon"), motion=lambda t: Tf(alpha=disc(t)))
    if hills:
        sc.add("hills", doc(hills_body()), z=0.5, wc=0.6, seed=seed_of("hills"), motion=lambda t: Tf(alpha=hills(t)))


def add_storm_sky(sc, ctx, alpha, banks_alpha=None, fronts=None, slow=None, soft=None):
    """The storm sky (z 1, alpha(t)) and the two racing cloud banks (z 2 / 2.5), each a looping strip drawn twice.
    fronts: {bank: front_x(t)} reveals a bank from the left up to front_x (the clouds racing in, s08) with a soft
    edge of soft[bank] px."""
    sc.add("storm_grad", doc(storm_grad_body()), z=1.0, wc=0.5, seed=seed_of("storm_grad"),
           motion=lambda t: Tf(alpha=alpha(t)))
    soft = soft or {"low": 520, "high": 320}
    for nm, z in (("high", 2.0), ("low", 2.5)):
        body = doc(bank_body(nm))
        ba = banks_alpha.get(nm) if banks_alpha else None
        fr = fronts.get(nm) if fronts else None
        sf = soft[nm]
        for j in (0, 1):
            def mo(t, nm=nm, j=j, ba=ba, fr=fr, sf=sf):
                x = bank_x(ctx, nm, t, slow) - SW * j
                a = ba(t) if ba else 1.0
                if fr is not None and fr(t) + sf / 2 <= x:
                    a = 0.0
                return Tf(dx=x, alpha=a)

            rv = None
            if fr is not None:
                def rv(t, nm=nm, j=j, fr=fr, sf=sf):
                    x = bank_x(ctx, nm, t, slow) - SW * j
                    return {"mode": "left", "frac": clamp((fr(t) - x) / SW, 0.0, 1.0), "soft": sf}
            sc.add(f"bank_{nm}{j}", body, z=z + 0.01 * j, wc=0.7, seed=seed_of("bank_" + nm), motion=mo, reveal=rv)


def add_calm_lake(sc, ctx, alpha=None, glow=1.0, name="calm", front=True, z=4.0, front_alpha=None):
    """The calm moonlit lake (z 4) and the same water in front of the hull (z 16.5); alpha / front_alpha(t)."""
    fa = calm_frame_at(ctx)
    mo = (lambda t: Tf(alpha=alpha(t))) if alpha else None
    sc.add(name, [doc(calm_body(ph, glow)) for ph in CALM_PH], z=z, wc=0.5, seed=seed_of(name), frame_at=fa,
           motion=mo)
    if front:
        fal = front_alpha or alpha
        sc.add(name + "_front", [doc(calm_body(ph, glow, front=True)) for ph in CALM_PH], z=16.5 + (z - 4.0),
               wc=0.5, seed=seed_of(name + "_front"), frame_at=fa,
               motion=(lambda t: Tf(alpha=fal(t))) if fal else None)


def add_storm_lake(sc, ctx, levels, lvl, alpha=None, front_dy=None, back_dy=None, slow=None, heave=None,
                   full_back=()):
    """The stormy lake as four sliding wave rows: rows 0-1 behind the boat (z 5.0 / 5.1), rows 2-3 in front (z 16.0 /
    16.1). Each row is a flipbook over the wave sizes ``levels`` (lvl(t) = fractional index, cross-fades between
    neighbouring sizes) moved sideways by row_dx (slow(t) = seconds lost to a slow-down); back_dy / front_dy(t) lift
    the rows (a swell); heave(t) 0..1 scales a small up-down bob; levels listed in full_back get back rows that
    reach the bottom of the frame (cross-fades with the calm lake)."""
    for i in range(4):
        frames = [doc(lake_row_body(i, w, bottom=(LAKE_BOTTOM if (i < 2 and w in full_back) else None)))
                  for w in levels]
        dyf = back_dy if i < 2 else front_dy

        def mo(t, i=i, dyf=dyf):
            h = (heave(t) if heave else 1.0) * row_heave(ctx, i, t)
            return Tf(dx=row_dx(ctx, i, t, slow), dy=h + (dyf(t) if dyf else 0.0), alpha=alpha(t) if alpha else 1.0)
        nm = f"lake_row{i}"
        sc.add(nm, frames, z=(5.0 if i < 2 else 15.9) + 0.1 * i, wc=0.6, seed=seed_of(nm), motion=mo,
               frame_at=(lambda t: clamp(lvl(t), 0.0, len(levels) - 1.0)) if len(frames) > 1 else None)


def add_boat(sc, ctx, rock, wet, water_levels, water, slosh=None, lantern_amp=None):
    """Boat back (z 10; wet(t) 0..1 cross-fades dry -> wet), boat front (z 14; water(t) = fractional index into
    water_levels, slosh phases film-time keyed; slosh(t) False holds them still), the swinging lantern (z 14.5)."""
    sc.add("boat_back", [doc(boat_back_body(False)), doc(boat_back_body(True))], z=10.0, motion=rock.tf,
           seed=seed_of("boat_back"), frame_at=lambda t: clamp(wet(t)))
    nl = len(water_levels)
    frames = []
    for p in range(4):
        for i, w in enumerate(water_levels):
            frames.append(doc(boat_front_body(w, p / 4, wet=w > 0 or i > 0)))

    def fa(t):
        p = (gframe(ctx, t) // 5) % 4 if (slosh is None or slosh(t)) else 0
        return p * nl + clamp(water(t), 0.0, nl - 1.0)
    sc.add("boat_front", frames, z=14.0, motion=rock.tf, seed=seed_of("boat_front"), frame_at=fa)
    amp = lantern_amp or (lambda t: 14.0)

    def lant(t):
        g = gtime(ctx, t)
        r = amp(t) * (0.8 * math.sin(2 * math.pi * g / 1.35) + 0.2 * math.sin(2 * math.pi * g / 0.7 + 1))
        return Tf(rot=r - 0.6 * rock.tilt(t))
    sc.add("lantern", doc(lantern_body()), z=14.5, seed=seed_of("lantern"), motion=on_boat(rock, HOOK, lant))


def add_sail(sc, ctx, rock, plan):
    """Sail layer (z 10.5). plan: [(t0, kind, ...)]: ('full',) flag flutter | ('flap',) the flapping cycle |
    ('haul', haul fn) brailing | ('furled', step) furled, flag fluttering every step frames (0 = still)."""
    bodies, segs = [], []
    idx = {}

    def fr(body):
        if body not in idx:
            idx[body] = len(bodies)
            bodies.append(body)
        return idx[body]
    for t0, kind, *arg in plan:
        if kind == "full":
            segs.append((t0, "cyc", [fr(sail_body("full", 0.0, flag=i / 4)) for i in range(4)], 6))
        elif kind == "flap":
            segs.append((t0, "cyc", [fr(sail_body("flapping", i / 8)) for i in range(8)], 3))
        elif kind == "haul":
            hauls = arg[0]
            segs.append((t0, "haul", {h: [fr(sail_body("flapping", i / 4, haul=h)) for i in range(4)]
                                      for h in hauls}, arg[1]))
        elif kind == "furled":
            stp = arg[0] if arg else 3
            if stp:
                segs.append((t0, "cyc", [fr(sail_body("furled", 0.0, flag=i / 4)) for i in range(4)], stp))
            else:
                segs.append((t0, "cyc", [fr(sail_body("furled", 0.0, flag=0.0))], 3))

    def fa(t):
        seg = segs[0]
        for s in segs:
            if t >= s[0]:
                seg = s
        g = gframe(ctx, t)
        if seg[1] == "cyc":
            ids, stp = seg[2], seg[3]
            return float(ids[(g // stp) % len(ids)])
        table, hf = seg[2], seg[3]
        h = hf(t)
        return float(table[h][(g // 3) % 4])
    sc.add("sail", [doc(b) for b in bodies], z=10.5, motion=rock.tf, seed=seed_of("sail"), frame_at=fa)


# ================================================================== procedural effects (film-time keyed)
class Rain:
    """Slanted rain streaks over the frame (wind from the left: falling down-right), positions keyed to film
    time; intensity(t) 0..1; bubble = ((x, y, rx, ry) stage ellipse, strength(t)): no drops fall inside it."""

    def __init__(self, ctx, intensity, n=520, angle=16, speed=1650, length=50, seed=8, bubble=None):
        rng = np.random.default_rng(seed)
        self.ctx, self.I, self.bubble = ctx, intensity, bubble
        self.x0 = rng.uniform(-300, OUT_W + 300, n)
        self.y0 = rng.uniform(0, OUT_H + 120, n)
        self.sp = speed * rng.uniform(0.8, 1.2, n)
        self.ln = length * rng.uniform(0.6, 1.3, n)
        self.rank = rng.uniform(0, 1, n)
        a = math.radians(angle)
        self.dx, self.dy = math.sin(a), math.cos(a)

    def __call__(self, frame, t, view):
        k = self.I(t)
        if k <= 0.01:
            return frame
        g = gtime(self.ctx, t)
        y = (self.y0 + self.sp * g) % (OUT_H + 120) - 60
        x = (self.x0 + self.sp * g * self.dx / self.dy) % (OUT_W + 600) - 300
        col = (222, 230, 240, int(118 * min(1.0, k)))
        bub = None
        if self.bubble:
            (bx, by, brx, bry), bs = self.bubble[0], self.bubble[1](t)
            if bs > 0.01:
                cx, cy = view.to_out(bx, by)
                bub = (cx, cy, brx * view.scale, bry * view.scale, bs)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in np.nonzero(self.rank < min(1.0, k))[0]:
            if bub:
                q = ((x[i] - bub[0]) / bub[2]) ** 2 + ((y[i] - bub[1]) / bub[3]) ** 2
                if q < 1.0 and (self.rank[i] * 7.3) % 1.0 < bub[4]:
                    continue
            d.line([(x[i], y[i]), (x[i] + self.ln[i] * self.dx, y[i] + self.ln[i] * self.dy)], fill=col, width=2)
        frame.alpha_composite(ov)
        return frame


class Wind:
    """Curly white wind streaks (storm_sky's look) rushing left -> right through the sky, film-time keyed;
    level(t) 0..1; gusts [(t0, dur)] send big sweeping streaks across the whole frame."""

    def __init__(self, ctx, level, gusts=(), n=16, seed=4, y_band=(140, 760), speed=760, avoid=None):
        rng = random.Random(seed)
        self.ctx, self.level, self.gusts, self.avoid = ctx, level, list(gusts), avoid
        self.items = [(rng.random(), rng.uniform(*y_band), rng.uniform(170, 330), rng.uniform(18, 32),
                       rng.uniform(0.75, 1.3), rng.random()) for _ in range(n)]
        self.speed = speed

    @staticmethod
    def _shape(x, y, L, curl, view, lift=10.0):
        pts = [(x + L * j / 8, y - lift * 4 * (j / 8) * (1 - j / 8)) for j in range(9)]
        cx, cy = x + L, y - curl * 0.5
        for j in range(1, 7):
            a = math.pi / 2 - j * math.pi / 6 * 1.7
            pts.append((cx + curl * 0.55 * math.cos(a), cy + curl * 0.5 * math.sin(a)))
        return [view.to_out(px, py) for px, py in pts]

    def __call__(self, frame, t, view):
        k = self.level(t)
        gk = [((t - t0) / dur, a) for t0, dur, a in self.gusts if t0 <= t <= t0 + dur]
        if k <= 0.01 and not gk:
            return frame
        g = gtime(self.ctx, t)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        span = SW + 900
        w = max(2, int(round(3.6 * view.scale)))
        av = None
        if self.avoid and self.avoid[1](t) > 0.05:
            av = self.avoid[0]
        if k > 0.01:
            for (r, y, L, curl, sp, ph) in self.items:
                x = -450 + ((r * span + g * self.speed * sp) % span)
                a = int(150 * min(1.0, k) * (0.5 + 0.5 * math.sin(2 * math.pi * (g * 0.6 + ph))))
                if av and (((x + L / 2 - av[0]) / (av[2] + L / 2)) ** 2 + ((y - av[1]) / av[3]) ** 2) < 1.0:
                    continue
                if a >= 8:
                    d.line(self._shape(x, y, L, curl, view), fill=(232, 238, 244, a), width=w, joint="curve")
        for u, amp in gk:
            for j, (y, L) in enumerate(((300, 640), (520, 860), (720, 600), (420, 520))):
                x = -1000 + (SW + 1600) * (u * 1.1 - 0.07 * j)
                a = int(225 * amp * math.sin(math.pi * min(1.0, u * 1.1)))
                if a > 8:
                    d.line(self._shape(x, y + 26 * math.sin(u * 6 + j), L, 40, view, lift=26), fill=(242, 246, 250, a),
                           width=max(3, int(round(5.5 * view.scale))), joint="curve")
        frame.alpha_composite(ov)
        return frame


class Twinkle:
    """The bigger stars of night_body() glint (film-time keyed); alpha(t)."""

    def __init__(self, ctx, alpha, seed=4, stars=90, progress=None):
        rng = random.Random(seed)
        x0, y0, x1, y1 = -20, -20, SW + 20, SKY_BOT
        self.pts = []
        for i in range(stars):
            sx, sy = x0 + rng.random() * (x1 - x0), y0 + rng.random() ** 1.3 * (y1 - y0) * 0.8
            big = rng.random() < 0.25
            rng.random()
            if big:
                self.pts.append((sx, sy, i / stars, (i * 0.37) % 1.0))
        self.ctx, self.alpha, self.progress = ctx, alpha, progress

    def __call__(self, frame, t, view):
        a0 = self.alpha(t)
        if a0 <= 0.01:
            return frame
        g = gtime(self.ctx, t)
        pr = self.progress(t) if self.progress else 1.0
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for sx, sy, k, ph in self.pts:
            if k > pr:
                continue
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (g / 2.3 + ph))
            if tw < 0.45:
                continue
            ox, oy = view.to_out(sx, sy)
            r = (10 + 14 * tw) * view.scale
            a = int(200 * a0 * (tw - 0.45) / 0.55)
            w = r * 0.18
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r), (ox - w, oy + w),
                       (ox - r, oy), (ox - w, oy - w)], fill=(255, 246, 214, a))
        frame.alpha_composite(ov)
        return frame


# ================================================================== crew helpers
def calm_crew_pose(name):
    """The crew sailing on the calm evening lake (s08 start)."""
    return {"philip": ("stand", -1, "kind"), "bartholomew": ("stand", 1, "happy"), "matthew": ("stand", -1, "kind"),
            "thaddaeus": ("stand", 1, "tired"), "jamesa": ("stand", -1, "happy"), "judas": ("stand", 1, "kind"),
            "andrew": ("sit", -1, "kind"), "james": ("stand", 1, "happy"), "thomas": ("sit", 1, "tired"),
            "peter": ("stand", 1, "happy"), "john": ("sit", -1, "kind"), "simon": ("stand", -1, "happy")}[name]


def storm_crew_pose(name):
    """The crew at the height of the storm (end of s08 = start of s09): pose, facing, item."""
    return {"philip": ("scared", -1), "bartholomew": ("shout", 1), "matthew": ("scared", -1),
            "thaddaeus": ("scared", 1), "jamesa": ("scared", -1), "judas": ("scared", 1),
            "andrew": ("scared", -1), "james": ("scared", 1), "thomas": ("scared", -1),
            "peter": ("cling", 1), "john": ("pull_rope", -1), "simon": ("shout", 1)}[name]


def storm_body(name, wet=True, expr=None):
    pose, fc = storm_crew_pose(name)
    at = BP["cling"] if pose == "cling" else None
    return disciple(name, pose, expr=expr, shake=0.25 if pose in ("scared", "cling") else 0.0, wet=wet, wind=1.0,
                    facing=fc, at=at)


TREMBLE = {n: (2.6 if CREW[n][2] == "near" else 2.2) for n in CREW}
CAM_END = Cam(1585, 935, 2380)        # s08's last camera = s09's first


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[:2]

    t_hu = beat(ctx, 0, "忽然")
    t_wind = t_hu + 0.45                                   # '起了一阵大风' (the take has no pause after 忽然)
    t_huA, t_huB = beat(ctx, 0, "呼", 0), beat(ctx, 0, "呼", 1)
    t_cloud = beat(ctx, 0, "乌云")
    t_moon = beat(ctx, 0, "把月亮")
    t_cover = beat(ctx, 0, "遮住")
    t_wave = beat(ctx, 1, "浪")
    t_one = [beat(ctx, 1, "一个", 0), beat(ctx, 1, "一个", 1)]
    t_in = beat(ctx, 1, "打进")
    t_hua = [beat(ctx, 1, "哗啦", 0), beat(ctx, 1, "哗啦", 1)]
    t_water = beat(ctx, 1, "船里的水")
    t_more = beat(ctx, 1, "越来越多")
    t_hold = T - 1.25                                      # from here on: the steady storm (s09's first frame)

    # ---------------- camera: wide on the calm night, a slow push in as the storm grows
    C0 = Cam(1600, 900, 2500)
    C1 = CAM_END
    sc.camera = cam_path([(0, C0), (t_wave - 0.6, C0), (t_hold - 0.3, C1), (T, C1)],
                         bumps=[(t_hu, 5, 0.5), (t_huA, 8, 0.6), (t_huB, 8, 0.6), (t_hua[0] + 0.05, 12, 0.7),
                                (t_hua[1] + 0.05, 12, 0.7)])

    # ---------------- the boat's motion
    amp = keyed([(0, CALM_TILT), (t_hu, CALM_TILT), (t_wind + 0.6, 2.4), (t_huB + 0.4, 3.8), (t_wave + 0.8, STORM_TILT)])
    bob = keyed([(0, CALM_BOB), (t_hu, CALM_BOB), (t_wind + 0.6, 5.0), (t_wave + 0.8, STORM_BOB)])
    rock = Rock(ctx, amp, bob, kicks=[(t_hu + 0.05, 2.2, 2.0), (t_huA, 2.8, 3.0), (t_huB, 2.6, 3.0),
                                     (t_hua[0] + 0.04, -4.0, 9.0), (t_hua[1] + 0.04, 3.6, 8.0)])

    # ---------------- sky: the night, then the storm racing in over the moon
    storm_a = keyed([(t_huA - 0.2, 0.0), (t_cover + 0.3, 1.0)], "sine")
    add_night(sc, ctx)
    add_moon(sc, halo=keyed([(t_moon - 0.3, 1.0), (t_cover + 0.1, 0.0)], "sine"),
             disc=keyed([(t_cover - 0.05, 1.0), (t_cover + 0.45, 0.0)], "sine"),
             hills=keyed([(t_huA, 1.0), (t_cover, 0.0)], "sine"))
    front_low = keyed([(t_huA - 0.1, -600.0), (t_cloud + 0.5, 1700.0), (t_cover + 0.4, SW + 800.0)], "linear")
    mc = MOON[0] + MOON_R + 260
    front_high = keyed([(t_huB - 0.05, -600.0), (t_moon, 1500.0), (t_cover, mc), (t_cover + 1.4, SW + 800.0)],
                       "linear")
    add_storm_sky(sc, ctx, storm_a, fronts={"low": front_low, "high": front_high})
    sc.fx.append(Twinkle(ctx, lambda t: 1.0 - storm_a(t)))

    # ---------------- the lake: silver calm -> grey waves rising
    levels = [0.05, 0.2, 0.5, 1.0]
    lvl = keyed([(t_hu + 0.2, 0.0), (t_wind + 1.0, 1.0), (t_huA + 0.1, 1.0), (t_huB + 0.7, 2.0), (t_wave, 2.0),
                 (t_one[0] + 0.3, 2.35), (t_one[1] + 0.3, 2.7), (t_in + 0.3, 3.0)])
    storm_in = keyed([(t_hu + 0.15, 0.0), (t_wind + 0.9, 1.0)], "sine")
    add_calm_lake(sc, ctx, alpha=lambda t: 1.0 if storm_in(t) < 0.999 else 0.0,
                  front_alpha=lambda t: 1.0 - storm_in(t))
    add_storm_lake(sc, ctx, levels, lvl, alpha=storm_in, full_back=(0.05, 0.2),
                   heave=keyed([(t_hu, 0.15), (t_wave + 0.5, 1.0)], "sine"))

    # ---------------- the boat
    wet = keyed([(t_hua[0] + 0.08, 0.0), (t_hua[0] + 0.6, 1.0)], "sine")
    wl = [0.0, 0.2, 0.35, 0.5]
    water = keyed([(t_hua[0] + 0.12, 0.0), (t_hua[0] + 0.45, 1.0), (t_hua[1] + 0.12, 1.0), (t_hua[1] + 0.45, 2.0),
                   (t_water + 0.1, 2.0), (t_more + 0.5, 3.0)])
    add_boat(sc, ctx, rock, wet, wl, water,
             lantern_amp=keyed([(t_hu, 4.0), (t_hu + 0.4, 16.0), (t_wind + 1, 12.0), (t_huA, 18.0)]))
    add_sail(sc, ctx, rock, [(0, "full"), (snap(t_hu + 0.06), "flap")])

    # ---------------- the crew: relaxed -> worried on the first gust -> scared on 呼 呼 -> soaked by the waves
    t_look = snap(t_hu + 0.12)
    order_a = {"andrew", "james", "philip", "matthew", "judas"}            # scared on the first 呼
    for k, name in enumerate(CREW):
        pose0, fc0, ex0 = calm_crew_pose(name)
        foot = BP["cling"] if name == "peter" else foot_of(name)
        a = Actor(ctx, name, foot, rock)
        a.at(0, disciple(name, pose0, expr=ex0, facing=fc0))
        stand_pose = "stand" if pose0 == "stand" else "sit"
        a.at(t_look, disciple(name, stand_pose, expr="worried", facing=fc0, wind=1.0))
        if name == "peter":
            t_s = snap(t_wind + 0.55)
        elif name == "john":
            t_s = snap(t_huA + 0.05)
        elif name in order_a:
            t_s = snap(t_huA + 0.05 + 0.04 * (k % 3))
        else:
            t_s = snap(t_huB + 0.05 + 0.04 * (k % 3))
        dry, soaked = storm_body(name, wet=False), storm_body(name, wet=True)
        a.at(t_s, dry)
        a.xfade(t_hua[0] + 0.1 + 0.03 * (k % 4), t_hua[0] + 0.7 + 0.03 * (k % 4), dry, soaked)
        a.move(dip(t_look, 4.0), dip(t_s, 9.0 if pose0 == "sit" else 7.0), breath(ctx, 0.007, 3.0 + 0.2 * k, k * 0.13),
               jitter(ctx, t_s + 0.15, 1e9, TREMBLE[name], seed=k + 1))
        lx = CREW[name][1]
        a.move(flinch(t_hua[0] + 0.06, dx=8.0 if lx > -250 else -8.0, depth=7.0 if lx < 50 else 4.0),
               flinch(t_hua[1] + 0.06, dx=-8.0 if lx > 250 else 6.0, depth=7.0 if lx > 250 else 4.0))
        a.add(sc)
    jz = Actor(ctx, "jesus", BP["sleep"], rock, z=12.0)
    jz.at(0, jesus_body("sleep")).move(breath(ctx, 0.012, 3.6)).add(sc)

    # ---------------- spray: little bursts at the bow as the waves come, two big ones on 哗啦
    for i, tb in enumerate((t_one[0] + 0.1, t_one[1] + 0.1, t_in + 0.05)):
        add_spray(sc, ctx, rock, f"bowspray{i}", tb, 600 + 40 * (i % 2), seed=40 + i, side=-1, scale=0.55 + 0.1 * i)
    add_spray(sc, ctx, rock, "spray0", t_hua[0] - 0.04, -200, seed=7, side=1, scale=1.0)
    add_spray(sc, ctx, rock, "spray1", t_hua[1] - 0.04, 330, seed=9, side=-1, scale=1.0)

    # ---------------- weather effects
    rain = keyed([(t_cover - 0.3, 0.0), (t_cover + 0.9, 0.35), (t_wave + 1.2, 0.62)], "sine")
    sc.fx.append(Rain(ctx, rain))
    wind = keyed([(t_hu - 0.05, 0.0), (t_hu + 0.3, 0.45), (t_wind + 0.8, 0.6), (t_huA, 0.95)], "sine")
    sc.fx.append(Wind(ctx, wind, gusts=[(t_hu - 0.08, 0.75, 0.7), (t_huA - 0.1, 0.85, 1.0), (t_huB - 0.1, 0.85, 1.0)]))

    # ---------------- sound
    sc.sfx("waves_calm", 0.0, dur=t_wind + 1.2, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("night", 0.0, dur=t_hu + 0.6, gain_db=-22, fade_in=0.8, fade_out=0.5)
    sc.sfx("whoosh", t_hu - 0.1, gain_db=-12)
    sc.sfx("storm_wind", t_hu - 0.1, dur=T - t_hu + 0.1, gain_db=-17, fade_in=1.2, fade_out=0.8)
    sc.sfx("whoosh", t_huA - 0.12, gain_db=-9, pan=-0.3)
    sc.sfx("whoosh", t_huB - 0.12, gain_db=-9, pan=0.3)
    sc.sfx("waves_storm", t_wind, dur=T - t_wind, gain_db=-15, fade_in=2.0, fade_out=0.8)
    sc.sfx("ship_creak", t_wind + 0.5, dur=T - t_wind - 0.5, gain_db=-21, fade_in=1.0, fade_out=0.8)
    sc.sfx("rain", t_cover - 0.4, dur=T - t_cover + 0.4, gain_db=-19, fade_in=1.2, fade_out=0.8)
    sc.sfx("cloth", t_hu + 0.05, gain_db=-14)
    for i, tb in enumerate((t_one[0] + 0.1, t_one[1] + 0.1, t_in + 0.05)):
        sc.sfx("splash_small", tb, gain_db=-14 + 2 * i, pan=0.4)
    sc.sfx("splash", t_hua[0] - 0.04, gain_db=-6, pan=-0.15)
    sc.sfx("splash", t_hua[1] - 0.04, gain_db=-6, pan=0.25)
    return sc
