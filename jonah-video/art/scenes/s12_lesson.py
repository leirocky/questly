"""Scene 12 — God's lesson (Jonah 4:10-11).

All four lines are God speaking, gently. Late afternoon, warm golden light. One wide 3800 x 1650 stage:

  * right: Jonah's dry knoll east of the city — a near, higher vantage point (its crest sits above the city
    wall's ground line and its dark front slope overlaps the plain) — with his little booth and the withered
    castor plant (same drawings and scale as s11). Jonah sits at the edge of the knoll, facing the city,
    holding a dry leaf;
  * left / below: the green Tigris plain in front of Nineveh's hazy wall and open gate, full of life — elders,
    mothers with their children, children playing ball, people walking in and out of the gate, little figures on
    the wall walk, and a pasture with sheep, lambs, goats, cows and donkeys. Long soft shadows point east (the
    low sun is in the west, on the left).

Timing (all keyed to ctx.lines; the first 0.8 s is a still frame for the dissolve from s11):
  line 0  "约拿，这棵蓖麻不是你栽种的，"  Jonah looks up at his name; clouds part, golden rays fall on him (a
          warm light pass sits on Jonah himself); he is sad, turns the dry leaf in his hand; a dead leaf
          wobbles loose from the canopy and flutters down.
  line 1  "你尚且这样爱惜它。"  Jonah looks down at the leaf, thoughtful ('sorry'). Near the end of the line the
          camera starts a slow pull-back while Jonah leans toward the city ('worried', no smile yet).
  line 2  "尼尼微有十二万多…人"  the pull-back settles on a held wide view of the whole city with Jonah on his
          knoll (doves fly ahead of the camera and leave the frame); then one continuous slow glide descends
          to the people (hearts rise over them, one each, above their heads).
  line 3  "还有许多牲畜，我怎能不爱惜呢？"  the glide drifts on over the pasture (a sheep bleats, hearts over the
          animals) and rises back up the knoll to Jonah; the camera settles, then pushes in slowly while his
          face softens (peaceful, the only smile); a chime at the end. The last frames put Jonah's face at the
          centre, where s13 opens on him.
Camera: every move is re-parametrised by output-space arc length (zoom included) with soft ramps, so the
peak speed stays under ~20 output px / frame.
"""
import math
import random
from bisect import bisect_left
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

from art import characters as CH
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3800, 1650

# ------------------------------------------------------------------ layout (stage px)
GY = 710                 # knoll crest: Jonah, plant root, booth (above the wall's ground line: a higher vantage)
SP = 1.3                 # Jonah / plant / booth scale (as in s11)
XJ = 2680                # Jonah (sitting, facing the city on the left)
XP = 2870                # withered castor root
XB = XP + PR.CASTOR_BOOTH_DX * SP   # booth (the dead canopy arches over its roof, as in s11)

WALL_Y = 770             # city wall ground line
GATE_X = 1380
SUN = (430, 300)         # low western sun


def kmap(x, y):
    """Map the knoll's detail sketch (drawn for a crest at y 830) onto the raised, shifted knoll."""
    return (x - 160, GY + (y - 830) * (SH + 80 - GY) / (SH + 80 - 830))


# knoll silhouette (top edge); the left slope runs down into (and over) the plain
KNOLL = [(1900, SH + 80), (2010, 1421), (2140, 1157), (2270, 951), (2400, 800), (2490, 736), (2560, 712),
         (2740, 709), (3040, 705), (3340, 694), (3720, 682), (3900, 680)]

ABOX = {"sheep": (-95, -147, 121, 3), "goat": (-91, -256, 139, 3), "cow": (-139, -226, 195, 3),
        "donkey": (-115, -303, 170, 3)}
HEAD_DX = {"sheep": 78, "goat": 88, "cow": 140, "donkey": 118}   # heart above the head (facing side)

FIGS = []                # [(name, bbox, heart_spot)] filled by build(): used to place hearts, and by checks
HEARTS = {}              # {"people": [...], "animals": [...]} final heart spots


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def _env(t, a, b, c, d):
    """0 before a, ramps to 1 at b, holds, back to 0 at d (smooth)."""
    if t <= a or t >= d:
        return 0.0
    if t < b:
        return M.progress(t, a, b, "sine")
    if t <= c:
        return 1.0
    return 1 - M.progress(t, c, d, "sine")


def plain_scale(y):
    """Figure scale on the plain: smaller (farther) near the wall, bigger toward the viewer."""
    return 0.36 + (y - 790) * (0.27 / 470)


# ------------------------------------------------------------------ drawing helpers
def _rock(x, y, w, h, seed=0, fill=None, sw=4):
    fill = fill or P["stone"]
    d = S.blob(x, y - h * 0.45, w / 2, h / 2, wobble=0.12, n=9, seed=seed)
    hi = S.blob(x - w * 0.12, y - h * 0.62, w * 0.28, h * 0.2, wobble=0.15, n=7, seed=seed + 1)
    return (S.path(d, fill=fill, sw=sw) +
            f'<path d="{hi}" fill="{S.shade(fill, 0.35)}" opacity="0.7"/>' +
            f'<path d="M{x - w * 0.42:.0f},{y - h * 0.12:.0f} Q{x:.0f},{y + h * 0.02:.0f} {x + w * 0.44:.0f},'
            f'{y - h * 0.16:.0f}" fill="none" stroke="{S.shade(fill, -0.25)}" stroke-width="{sw * 1.6:.1f}" '
            f'opacity="0.45" stroke-linecap="round"/>')


def _dry_leaf(cx, cy, r, rot=0.0, col=None, stalk=None):
    """A withered castor leaf: palmate, 7 pointed lobes curling in, brown with pale veins.

    stalk=(x, y): end of the leaf stalk (e.g. in Jonah's hand)."""
    col = col or P["leaf_dead"]
    lobes = 7
    span = 320.0                       # degrees covered by the lobes (a notch at the stalk)
    step = span / lobes
    pts = []
    for i in range(lobes):
        a = -90 + rot + (i - (lobes - 1) / 2) * step
        k = 1.0 - 0.22 * abs(i - (lobes - 1) / 2) / 3          # side lobes a little shorter
        for da, rr in ((-0.5, 0.5), (-0.3, 0.84), (0.04, 1.02), (0.3, 0.82)):
            aa = math.radians(a + da * step)
            rk = rr * (k if rr > 0.6 else 1.0)
            pts.append((cx + r * rk * math.cos(aa), cy + r * rk * math.sin(aa)))
    a_end = math.radians(-90 + rot + span / 2)
    pts.append((cx + r * 0.5 * math.cos(a_end), cy + r * 0.5 * math.sin(a_end)))
    pts.append((cx + r * 0.16 * math.cos(math.radians(rot + 90)), cy + r * 0.16 * math.sin(math.radians(rot + 90))))
    d = S.smooth_path(pts, closed=True, tension=0.85)
    out = ""
    if stalk:
        sx, sy = stalk
        out += (f'<path d="M{f1(sx)},{f1(sy)} Q{f1((sx + cx) / 2 + 6)},{f1((sy + cy) / 2 + 4)} {f1(cx)},{f1(cy)}" '
                f'fill="none" stroke="{P["ink"]}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M{f1(sx)},{f1(sy)} Q{f1((sx + cx) / 2 + 6)},{f1((sy + cy) / 2 + 4)} {f1(cx)},{f1(cy)}" '
                f'fill="none" stroke="#a5784a" stroke-width="4" stroke-linecap="round"/>')
    out += S.path(d, fill=col, sw=3.5)
    vein = S.shade(col, 0.35)
    for i in range(lobes):
        a0 = math.radians(-90 + rot + (i - (lobes - 1) / 2) * step)
        k = 1.0 - 0.22 * abs(i - (lobes - 1) / 2) / 3
        out += (f'<path d="M{f1(cx)},{f1(cy)} L{f1(cx + r * k * 0.74 * math.cos(a0))},{f1(cy + r * k * 0.74 * math.sin(a0))}" '
                f'stroke="{vein}" stroke-width="2.6" stroke-linecap="round" opacity="0.8"/>')
    # a darker dry rim and a few crinkle lines
    out += f'<path d="{d}" fill="none" stroke="{S.shade(col, -0.25)}" stroke-width="5" opacity="0.35"/>'
    for (dx, dy, rr) in ((-0.3, -0.25, 0.08), (0.28, 0.1, 0.06), (0.05, -0.5, 0.05)):
        out += f'<circle cx="{f1(cx + dx * r)}" cy="{f1(cy + dy * r)}" r="{f1(rr * r)}" fill="{S.shade(col, -0.3)}" opacity="0.7"/>'
    out += f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r * 0.07)}" fill="{S.shade(col, -0.2)}"/>'
    return S.g(out, filter="wobble-fine")


def _well(x, y, s=1.0):
    """Round stone well with a wooden frame and a bucket (anchor: bottom centre)."""
    w, h = 120 * s, 70 * s
    sw = 4 * s
    out = ""
    # posts + beam
    for px in (x - w * 0.5, x + w * 0.5):
        out += (f'<rect x="{f1(px - 6 * s)}" y="{f1(y - h - 95 * s)}" width="{f1(12 * s)}" height="{f1(95 * s + h * 0.5)}" '
                f'fill="{P["wood"]}" {S.STROKE_THIN}/>')
    out += (f'<rect x="{f1(x - w * 0.62)}" y="{f1(y - h - 104 * s)}" width="{f1(w * 1.24)}" height="{f1(14 * s)}" rx="{f1(5 * s)}" '
            f'fill="{P["wood_dark"]}" {S.STROKE_THIN}/>')
    out += f'<line x1="{f1(x)}" y1="{f1(y - h - 92 * s)}" x2="{f1(x)}" y2="{f1(y - h - 40 * s)}" stroke="{P["ink"]}" stroke-width="{f1(2.5 * s)}"/>'
    out += (f'<path d="M{f1(x - 16 * s)},{f1(y - h - 42 * s)} L{f1(x + 16 * s)},{f1(y - h - 42 * s)} L{f1(x + 12 * s)},{f1(y - h - 14 * s)} '
            f'L{f1(x - 12 * s)},{f1(y - h - 14 * s)} Z" fill="{P["wood_light"]}" stroke="{P["ink"]}" stroke-width="{f1(sw * 0.8)}" stroke-linejoin="round"/>')
    # stone drum
    out += (f'<path d="M{f1(x - w / 2)},{f1(y - h)} L{f1(x - w / 2)},{f1(y - 6 * s)} Q{f1(x)},{f1(y + 12 * s)} {f1(x + w / 2)},{f1(y - 6 * s)} '
            f'L{f1(x + w / 2)},{f1(y - h)} Z" fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="{f1(sw)}" stroke-linejoin="round"/>')
    for i, yy in enumerate((y - h * 0.68, y - h * 0.36)):
        out += (f'<path d="M{f1(x - w / 2)},{f1(yy)} Q{f1(x)},{f1(yy + 14 * s)} {f1(x + w / 2)},{f1(yy)}" fill="none" '
                f'stroke="{P["stone_dark"]}" stroke-width="{f1(2.5 * s)}"/>')
        for j in range(4):
            bx = x - w / 2 + w * (j + 0.5 + 0.5 * (i % 2)) / 4
            if bx < x + w / 2 - 4:
                out += (f'<line x1="{f1(bx)}" y1="{f1(yy + 6 * s)}" x2="{f1(bx)}" y2="{f1(yy + h * 0.3)}" stroke="{P["stone_dark"]}" '
                        f'stroke-width="{f1(2.2 * s)}"/>')
    out += (f'<ellipse cx="{f1(x)}" cy="{f1(y - h)}" rx="{f1(w / 2)}" ry="{f1(13 * s)}" fill="{P["stone_light"]}" '
            f'stroke="{P["ink"]}" stroke-width="{f1(sw)}"/>'
            f'<ellipse cx="{f1(x)}" cy="{f1(y - h + 2 * s)}" rx="{f1(w * 0.38)}" ry="{f1(8 * s)}" fill="#5d4a3c"/>')
    return S.g(out, filter="wobble-fine")


def _end_tower(cx, y, k, col=None, ink=0.7):
    """Corner tower closing the right end of the city wall (matches props.city_wall colours at scale k)."""
    col = col or P["sand"]
    w, h = 104 * k, 170 + 64 * k
    x0, x1, top = cx - w / 2, cx + w / 2, y - h
    sw = 4 * ink
    st = f'stroke="{P["ink"]}" stroke-width="{sw}" stroke-linejoin="round"'
    out = ""
    # stepped Assyrian merlons
    mw = 26 * k
    n = int((w + 8 * k) // (mw + 8 * k))
    gap = (w + 8 * k - n * mw) / max(1, n - 1) if n > 1 else 0
    for i in range(n):
        mx = x0 - 4 * k + i * (mw + gap)
        st_h = 9 * k
        pts = [(mx, top), (mx, top - st_h), (mx + mw * 0.2, top - st_h), (mx + mw * 0.2, top - 2 * st_h),
               (mx + mw * 0.4, top - 2 * st_h), (mx + mw * 0.4, top - 3 * st_h), (mx + mw * 0.6, top - 3 * st_h),
               (mx + mw * 0.6, top - 2 * st_h), (mx + mw * 0.8, top - 2 * st_h), (mx + mw * 0.8, top - st_h),
               (mx + mw, top - st_h), (mx + mw, top)]
        out += '<path d="M' + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + f' Z" fill="{S.shade(col, 0.06)}" {st}/>'
    # side face (3/4 view) + front
    out += (f'<path d="M{f1(x1)},{f1(y)} L{f1(x1 + 18 * k)},{f1(y - 9 * k)} L{f1(x1 + 18 * k)},{f1(top - 9 * k)} '
            f'L{f1(x1)},{f1(top)} Z" fill="{S.shade(col, -0.22)}" {st}/>')
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(w)}" height="{f1(h)}" fill="{S.shade(col, 0.06)}" {st}/>'
    out += (f'<rect x="{f1(x0 + 2)}" y="{f1(y - 26 * k)}" width="{f1(w - 4)}" height="{f1(24 * k)}" '
            f'fill="{S.shade(col, -0.12)}"/>')
    for j in range(5):
        yy = top + 30 * k + j * 36 * k
        out += (f'<line x1="{f1(x0 + 4)}" y1="{f1(yy)}" x2="{f1(x1 - 4)}" y2="{f1(yy)}" stroke="{S.shade(col, -0.2)}" '
                f'stroke-width="2" opacity="0.5"/>')
    for yy in (top + 40 * k, top + 120 * k):
        out += (f'<rect x="{f1(cx - 6 * k)}" y="{f1(yy)}" width="{f1(12 * k)}" height="{f1(34 * k)}" rx="{f1(6 * k)}" '
                f'fill="#4a3426" {st}/>')
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(w)}" height="{f1(h)}" fill="none" {st}/>'
    return S.g(out, filter="wobble-fine")


def _ray_fan(cx, cy, length, angles, w0=10, w1=90, fill="#ffe9b5", opacity=0.5):
    """Soft light shafts fanning DOWN from (cx, cy); angles in degrees (90 = straight down)."""
    d = ""
    for i, a in enumerate(angles):
        r = math.radians(a)
        ux, uy = math.cos(r), math.sin(r)
        nx, ny = -uy, ux
        ln = length * (0.85 + 0.15 * math.sin(i * 2.3))
        ww = w1 * (0.7 + 0.3 * math.cos(i * 1.7))
        p = [(cx + nx * w0, cy + ny * w0), (cx + ux * ln + nx * ww, cy + uy * ln + ny * ww),
             (cx + ux * ln - nx * ww, cy + uy * ln - ny * ww), (cx - nx * w0, cy - ny * w0)]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in p) + " Z "
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def _baa(x, y, s=1.0):
    """Little sound arcs coming out of a bleating sheep's mouth (to the left of (x, y))."""
    out = ""
    for i, r in enumerate((16, 30, 44)):
        r *= s
        out += (f'<path d="M{f1(x - r * 0.55)},{f1(y - r * 0.85)} Q{f1(x - r * 1.15)},{f1(y)} {f1(x - r * 0.55)},{f1(y + r * 0.85)}" '
                f'fill="none" stroke="{P["ink_soft"]}" stroke-width="{f1(4.5 * s)}" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def _field(x0, x1, y0, y1, col, seed):
    """An irregular, slightly curved field patch near the wall (wider at its near edge) with soft furrows."""
    r = random.Random(seed)
    n = 5
    top = [(x0 + (x1 - x0) * i / n + r.uniform(-14, 14), y0 + r.uniform(-5, 5) - 4 * math.sin(math.pi * i / n))
           for i in range(n + 1)]
    bot = [(x1 + 16 - (x1 - x0 + 32) * i / n + r.uniform(-16, 16), y1 + r.uniform(-7, 7) + 5 * math.sin(math.pi * i / n))
           for i in range(n + 1)]
    d = S.smooth_path(top + bot, closed=True, tension=0.75)
    out = (f'<path d="{d}" fill="{col}" opacity="0.92" stroke="#8a6a4a" stroke-width="2" stroke-opacity="0.6" '
           f'stroke-linejoin="round"/>')
    for k in range(3):     # furrows, gently bowed
        u = (k + 1) / 4
        ya, yb = y0 + (y1 - y0) * u, y0 + (y1 - y0) * u
        xa, xb = x0 + 6 - 10 * u, x1 - 4 + 10 * u
        out += (f'<path d="M{xa:.0f},{ya:.0f} Q{(xa + xb) / 2:.0f},{ya + 5 + 3 * u:.0f} {xb:.0f},{yb:.0f}" fill="none" '
                f'stroke="{S.shade(col, -0.16)}" stroke-width="2" opacity="0.55" stroke-linecap="round"/>')
    return out


LSH = '<filter id="lsh" x="-20%" y="-80%" width="140%" height="260%"><feGaussianBlur stdDeviation="3.2"/></filter>'


def long_shadow(x, y, s, width, height, k=1.0):
    """Contact shadow + a long, soft late-afternoon shadow pointing east (right, slightly toward the viewer).
    Uses the #lsh filter: put it in a document made with ``shdoc``."""
    L = 0.9 * height * s * k
    ry = max(4.0, width * s * 0.1)
    return (f'<ellipse cx="{f1(x + L * 0.5 - width * s * 0.08)}" cy="{f1(y + 2 * s)}" rx="{f1(L * 0.5)}" ry="{f1(ry)}" '
            f'fill="#5f4532" opacity="0.24" transform="rotate(7 {f1(x)} {f1(y)})" filter="url(#lsh)"/>' +
            CH.ground_shadow(x, y, s, width=width, opacity=0.22))


def shdoc(body):
    return doc(body, LSH)


# ------------------------------------------------------------------ hops (with rests)
def hop_sched(seed, t_end, n=(2, 3), dur=(0.42, 0.56), rest=(0.8, 1.4)):
    """A few hops in a row (2-3), then a rest; varied durations. Returns [(t0, duration)]."""
    r = random.Random(seed)
    t = r.uniform(0.0, 0.9)
    hops = []
    while t < t_end:
        d = r.uniform(*dur)
        for _ in range(r.choice(n)):
            hops.append((t, d))
            t += d + 0.04
        t += r.uniform(*rest)
    return hops


def hop_h(hops, t):
    """Normalised height 0..1 of a hopper at time t."""
    for (t0, d) in hops:
        if t0 <= t <= t0 + d:
            return math.sin(math.pi * (t - t0) / d)
    return 0.0


def hop_motion(x, y, hops, H):
    def m(t):
        sq = 1.0
        for (t0, d) in hops:
            u = t - (t0 + d)
            if 0 <= u < 0.12:
                sq = 1 - 0.05 * math.sin(math.pi * u / 0.12)
        return Tf(dy=-H * hop_h(hops, t), sx=1 / sq ** 0.5, sy=sq, px=x, py=y)
    return m


def hop_frame(hops, lead=0.1, tail=0.06):
    """Flipbook index: 1 (arms up) while airborne, 0 (stand) at rest."""
    def f(t):
        for (t0, d) in hops:
            if t0 - lead <= t <= t0 + d + tail:
                return 1.0
        return 0.0
    return f


def shadow_motion(x, y, hops):
    """A contact shadow that stays on the ground and shrinks / fades while its owner is in the air."""
    def m(t):
        hn = hop_h(hops, t)
        return Tf(sx=1 - 0.3 * hn, sy=1 - 0.2 * hn, alpha=1 - 0.4 * hn, px=x, py=y)
    return m


# ------------------------------------------------------------------ camera paths
def _cam_path(cams, zk=0.5, n=160):
    """Smooth path through cams (Catmull-Rom on x, y, ln w), parametrised by OUTPUT-space arc length.

    Returns (at(f) -> Cam for f in 0..1, total output px, knot fractions)."""
    pts_k = [(c.x, c.y, math.log(c.w)) for c in cams]
    ext = [pts_k[0]] + pts_k + [pts_k[-1]]
    pts = []
    for i in range(len(pts_k) - 1):
        p0, p1, p2, p3 = ext[i:i + 4]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            pts.append(tuple(0.5 * (2 * p1[j] + (p2[j] - p0[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 +
                                    (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * u3) for j in range(3)))
    pts.append(pts_k[-1])
    s = [0.0]
    for a, b in zip(pts, pts[1:]):
        w = math.exp(0.5 * (a[2] + b[2]))
        s.append(s[-1] + math.hypot(b[0] - a[0], b[1] - a[1]) / w * 1920 + zk * abs(b[2] - a[2]) * 1101)
    tot = s[-1] or 1.0
    s = [v / tot for v in s]
    knots = [s[i * n] for i in range(len(pts_k))]

    def at(f):
        f = _clamp(f)
        i = bisect_left(s, f)
        if i <= 0:
            p = pts[0]
        elif i >= len(s):
            p = pts[-1]
        else:
            a, b = s[i - 1], s[i]
            u = (f - a) / (b - a) if b > a else 0.0
            p = tuple(pts[i - 1][j] + (pts[i][j] - pts[i - 1][j]) * u for j in range(3))
        return Cam(p[0], p[1], math.exp(p[2]))
    return at, tot, knots


def _glide(u, r):
    """Distance fraction for time fraction u: raised-cosine ramps (fraction r each end), constant cruise."""
    u = _clamp(u)
    if r <= 0:
        return u

    def ramp(x):
        return 0.5 * x - 0.5 * r / math.pi * math.sin(math.pi * x / r)
    tot = 1 - r
    if u < r:
        d = ramp(u)
    elif u <= 1 - r:
        d = 0.5 * r + (u - r)
    else:
        d = tot - ramp(1 - u)
    return d / tot


def _glide_inv(f, r):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _glide(mid, r) < f:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------ hearts (output-space fx)
@lru_cache(maxsize=64)
def _heart_sprite(px):
    """Anti-aliased picture-book heart (rose fill, umber ink rim, cream highlight) of ~px width."""
    px = max(8, int(px))
    k = 4
    Wd = px * k
    pad = int(Wd * 0.12)
    im = Image.new("RGBA", (Wd + 2 * pad, Wd + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(120):
        a = 2 * math.pi * i / 120
        hx = 16 * math.sin(a) ** 3
        hy = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((pad + Wd / 2 + hx * Wd / 34, pad + Wd * 0.46 + hy * Wd / 34))
    d.polygon(pts, fill=(75, 52, 38, 255))
    inner = [(Wd / 2 + pad + (x - Wd / 2 - pad) * 0.82, pad + Wd * 0.47 + (y - pad - Wd * 0.46) * 0.82) for x, y in pts]
    d.polygon(inner, fill=(236, 116, 120, 255))
    d.ellipse([pad + Wd * 0.22, pad + Wd * 0.2, pad + Wd * 0.36, pad + Wd * 0.33], fill=(255, 238, 222, 230))
    return im.resize(((Wd + 2 * pad) // k, (Wd + 2 * pad) // k), Image.LANCZOS)


def hearts_fx(spots, t0, t1, rise=72, life=2.6, period=3.5, size=42, seed=3):
    """One heart at a time rising a little above each stage spot [(x, y)] (just above a head).

    First births are spread evenly (in shuffled order) over [t0, t0 + min(period, t1 - t0)]; each spot then
    repeats every ``period`` until t1."""
    rng = np.random.default_rng(seed)
    win = max(0.05, min(period, t1 - t0))
    order = rng.permutation(len(spots))
    slots = []
    for i, (x, y) in enumerate(spots):
        off = (order[i] + rng.uniform(0.1, 0.9)) / len(spots) * win
        slots.append((x, y, off, rng.uniform(0, 6.28), rng.uniform(0.92, 1.08)))

    def fx(frame, t, view):
        if t < t0 or t > t1 + life:
            return frame
        for (x, y, off, ph, k) in slots:
            if t < t0 + off:
                continue
            age = (t - t0 - off) % period
            birth = t - age
            if birth > t1 or age > life:
                continue
            u = age / life
            sx = x + 9 * math.sin(2 * math.pi * age / 2.1 + ph)
            sy = y - rise * (1 - (1 - u) ** 1.6)
            ox, oy = view.to_out(sx, sy)
            if not (-80 < ox < frame.width + 80 and -80 < oy < frame.height + 80):
                continue
            grow = 0.55 + 0.45 * min(1.0, age / 0.5)
            a = min(1.0, age / 0.35) * min(1.0, (life - age) / 0.8)
            spr = _heart_sprite(round(size * k * grow * view.scale / 2) * 2)
            if a < 0.999:
                spr = spr.copy()
                spr.putalpha(spr.getchannel("A").point(lambda v, a=a: int(v * a)))
            frame.alpha_composite(spr, (int(ox - spr.width / 2), int(oy - spr.height / 2)))
        return frame
    return fx


def _place_hearts(names, rise=72, half=27, extra_obstacles=()):
    """Heart spot above each named figure; nudged sideways (or dropped) if its rising column would cross
    another figure (hearts are drawn over everything)."""
    boxes = {n: b for n, b, _ in FIGS}
    obstacles = [(n, b) for n, b in boxes.items()] + list(extra_obstacles)
    out = []
    for name, _, spot in FIGS:
        if name not in names or spot is None:
            continue
        x0, y0 = spot
        for dx in (0, -16, 16, -32, 32, -48, 48):
            x = x0 + dx
            col = (x - half, y0 - rise - half, x + half, y0 + 20)
            hit = any(n != name and col[0] < b[2] - 4 and col[2] > b[0] + 4 and col[1] < b[3] - 4 and col[3] > b[1] + 4
                      for n, b in obstacles)
            if not hit:
                out.append((x, y0))
                break
    return out


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    l0, l1, l2, l3 = L[0], L[1], L[2], L[3]
    FIGS.clear()
    HEARTS.clear()

    # --- key times ----------------------------------------------------------------------------
    t_still = 0.8                             # dissolve from s11: nothing new starts before this
    t_name = max(l0.start + 0.15, t_still)    # Jonah hears his name and looks up toward the light
    t_light0 = max(l0.start, t_still)         # God speaks: clouds part, golden rays on Jonah
    t_leaf_fall = l0.start + 0.8              # a dead leaf wobbles loose and flutters down ("这棵蓖麻")
    t_thought = l1.start + 0.2                # "你尚且这样爱惜它" -> Jonah looks at the leaf, thoughtful
    t_look = l1.end - 0.15                    # he leans and looks toward the city (worried, not smiling)
    t_sw0, t_sw1 = l1.end - 1.8, l2.start + 1.2      # slow pull-back to the held wide view of the city
    t_hold1 = l2.start + 1.9                  # end of the wide hold -> one continuous glide
    t_back1 = l3.end - 0.55                   # the glide lands back on Jonah ...
    t_peace = l3.end - 0.35                   # ... and then his face softens (peaceful)
    t_city0 = l2.start - 0.2                  # golden sparkles begin to twinkle over the plain
    t_hearts_p0, t_hearts_p1 = l2.start + 0.7, l2.end + 0.3
    t_hearts_a0, t_hearts_a1 = l3.start - 0.3, l3.start + 1.3
    t_baa = l3.start + 0.85                   # a sheep bleats ("牲畜")
    t_chime = l3.end

    # =============================================================== SKY
    sky = doc(
        S.rect_bg("url(#sky)", SW, SH) +
        f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="760" fill="url(#sunglow)"/>',
        defs=S.lin_grad("sky", [(0, "#bfc3d8"), (0.16, "#e6c6b6"), (0.3, "#f6d2a2"), (0.42, "#fbe0ad"),
                                (1, "#fbe6b8")]) +
        S.rad_grad("sunglow", [(0, "#fff6d2", 0.95), (0.25, "#ffe6a4", 0.6), (0.6, "#fbd08a", 0.22),
                               (1, "#f8c784", 0)]))
    sc.add("sky", sky, z=0, wc=0.5)
    sun = doc(S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="92" fill="#fcd877" stroke="#eaa951" stroke-width="5"/>'
                  f'<circle cx="{SUN[0] - 26}" cy="{SUN[1] - 26}" r="34" fill="#fffaf0" opacity="0.45"/>',
                  filter="wobble"))
    sc.add("sun", sun, z=1, wc=0.4)

    # clouds: a parting pair above Jonah (God's light comes through the gap) + soft far clouds
    far_clouds = doc(S.g(
        S.cloud(980, 190, 360, 100, "#fdf0e0", seed=4, sw=3, shade_fill="#f2cdb6") +
        S.cloud(1820, 120, 300, 86, "#fdeedd", seed=6, sw=3, shade_fill="#f2cdb6") +
        S.cloud(150, 120, 260, 80, "#fdf0e0", seed=7, sw=3, shade_fill="#f2cdb6"), filter="wobble"))
    sc.add("far_clouds", far_clouds, z=2, wc=0.6)
    cl_l = doc(S.g(S.cloud(XJ - 250, 230, 420, 116, "#fdf1e2", seed=11, sw=3.5, shade_fill="#f0c9b0") +
                   S.cloud(XJ - 560, 312, 220, 66, "#fdf1e2", seed=14, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    cl_r = doc(S.g(S.cloud(XJ + 410, 215, 460, 124, "#fdf1e2", seed=12, sw=3.5, shade_fill="#f0c9b0") +
                   S.cloud(XJ + 800, 330, 280, 84, "#fdf1e2", seed=13, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    part = lambda t: M.progress(t, t_light0, l0.start + 2.4, "inout")
    sc.add("cloud_l", cl_l, z=5.2, wc=0.6, motion=lambda t: Tf(dx=-70 * part(t) - 4 * t))
    sc.add("cloud_r", cl_r, z=5.3, wc=0.6, motion=lambda t: Tf(dx=80 * part(t) - 4 * t))

    # =============================================================== LAND (static, flattened)
    FAR_INK = 'stroke="#9a7a60" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"'
    far = ""
    far += S.path(S.smooth_path([(-80, 560), (200, 520), (520, 540), (820, 505), (1150, 530), (1500, 500),
                                 (1850, 525), (2150, 470), (2450, 500), (2750, 455), (3050, 490), (3350, 440),
                                 (3650, 470), (3900, 450)],
                                closed=False) + " L3900,900 L-80,900 Z", fill="#e6cbb8", stroke=False, extra=FAR_INK)
    far += S.path(S.smooth_path([(-80, 640), (400, 610), (900, 630), (1600, 600), (2300, 600), (2600, 575),
                                 (2950, 600), (3250, 565), (3550, 590), (3900, 570)], closed=False) +
                  " L3900,900 L-80,900 Z", fill="#e8d2aa", stroke=False, extra=FAR_INK)
    # distant dunes east of the city (seen behind Jonah's raised crest)
    far += S.path(S.smooth_path([(2200, 612), (2450, 580), (2700, 604), (2950, 566), (3250, 592), (3550, 556),
                                 (3900, 574)], closed=False) + " L3900,900 L2200,900 Z", fill="#ecd3a0", stroke=False,
                  extra=FAR_INK)
    for (x, y, w_) in [(2480, 622, 140), (2900, 608, 180), (3300, 596, 150), (3680, 604, 120)]:
        far += (f'<path d="M{x - w_ / 2},{y} q{w_ / 2},-14 {w_},0" fill="none" stroke="#d9b98a" stroke-width="4" '
                f'opacity="0.6" stroke-linecap="round"/>')
    for (x, y, s) in [(2330, 604, 0.12), (2380, 608, 0.1), (3060, 576, 0.11)]:
        far += PR.palm_tree(x, y, s, lean=0.1)
    sc.add("far_hills", doc(S.g(far, filter="wobble")), z=3, wc=0.6)
    city = PR.nineveh_skyline(-60, 2240, 668, scale=0.62, seed=3, haze=0.45, tint="#f6dcb0")
    sc.add("city", doc(city), z=3.1, wc=0.6)

    # the plain in front of the wall: fields, road, pasture
    pl = f'<rect x="-40" y="{WALL_Y - 40}" width="2560" height="{SH - WALL_Y + 120}" fill="url(#plain)"/>'
    # the plain fades into the pale desert east of the city (behind the knoll) instead of ending at an edge
    pl += (f'<rect x="2000" y="{WALL_Y - 40}" width="{SW - 1900}" height="{SH - WALL_Y + 120}" fill="url(#plainfade)"/>')
    rng = np.random.default_rng(7)
    # pasture (green) on the right half of the plain
    past = S.smooth_path([(1180, 1040), (1450, 990), (1800, 985), (2150, 1000), (2420, 1040), (2470, 1300),
                          (2360, SH + 60), (900, SH + 60), (1000, 1300)], closed=True, tension=0.9)
    pl += f'<path d="{past}" fill="url(#past)" stroke="{P["ink"]}" stroke-width="3"/>'
    # the dusty play ground in front of the wall (left)
    play = S.blob(820, 1140, 520, 140, wobble=0.06, n=12, seed=5)
    pl += f'<path d="{play}" fill="#ead39a" opacity="0.75"/>'
    # road from the gate down toward the viewer
    road = S.smooth_path([(GATE_X - 58, WALL_Y + 2), (GATE_X - 90, 900), (GATE_X - 200, 1080), (GATE_X - 330, 1300),
                          (GATE_X - 420, SH + 60), (GATE_X - 120, SH + 60), (GATE_X - 60, 1300), (GATE_X - 20, 1080),
                          (GATE_X + 30, 900), (GATE_X + 58, WALL_Y + 2)], closed=True, tension=0.8)
    pl += f'<path d="{road}" fill="#f2e0b2" stroke="{P["ink"]}" stroke-width="3"/>'
    pl += (f'<path d="M{GATE_X - 40},{WALL_Y + 40} Q{GATE_X - 120},1050 {GATE_X - 250},1500" fill="none" '
           f'stroke="#dcc28c" stroke-width="5" stroke-dasharray="2 26" stroke-linecap="round"/>')
    # meadow flowers + grass dashes on the pasture / plain
    flowers = ""
    for _ in range(140):
        x, y = rng.uniform(1050, 2380), rng.uniform(1040, SH)
        col = ["#f7f0d8", "#f3c34f", "#ef9d8f", "#d6b2e0"][int(rng.integers(0, 4))]
        r = 3 + (y - 1000) / 160
        flowers += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="0.9"/>'
    for _ in range(110):
        x, y = rng.uniform(-40, 2400), rng.uniform(900, SH)
        ln = 8 + (y - 900) / 40
        flowers += (f'<path d="M{x:.0f},{y:.0f} l{-ln * 0.3:.1f},{-ln:.1f} M{x + 5:.0f},{y:.0f} l{ln * 0.25:.1f},{-ln * 0.9:.1f}" '
                    f'stroke="#8faa52" stroke-width="2.4" stroke-linecap="round" opacity="0.7"/>')
    pl += flowers
    # warm late-afternoon light: pooled over the plain and raking in from the low western sun (left)
    pl += '<ellipse cx="1150" cy="1080" rx="1350" ry="560" fill="url(#cg)"/>'
    pl += f'<rect x="-40" y="{WALL_Y - 40}" width="2600" height="{SH - WALL_Y + 120}" fill="url(#late)"/>'
    plain_defs = (S.lin_grad("plain", [(0, "#e4cf8c"), (0.25, "#d4cd84"), (1, "#b3bf6b")]) +
                  S.lin_grad("plainfade", [(0, "#ecd3a0", 0), (0.2, "#ecd3a0", 1), (1, "#ecd3a0", 1)], x2=1, y2=0) +
                  S.lin_grad("past", [(0, "#b0cb6c"), (0.5, "#9dbf60"), (1, "#8ab156")]) +
                  S.rad_grad("cg", [(0, "#fff0c0", 0.32), (0.55, "#ffe6a8", 0.14), (1, "#ffe0a0", 0)]) +
                  S.lin_grad("late", [(0, "#ffd98a", 0.24), (0.45, "#ffe2a2", 0.1), (1, "#ffe2a2", 0)], x2=1, y2=0))
    # far fields near the wall: irregular, softly inked patches (their own, stronger wobble)
    field_cols = ["#c9cc7e", "#e6cf88", "#b5c271", "#dcc47c", "#c3cf86"]
    xs = [-60, 260, 560, 900, 1180, 1560, 1860, 2140, 2420]
    fields = ""
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + 10, xs[i + 1] - 10
        fields += _field(x0, x1, WALL_Y + 10, WALL_Y + 58 + 20 * (i % 3), field_cols[i % len(field_cols)], seed=40 + i)
    sc.add("plain", doc(S.g(pl, filter="wobble") + S.g(fields, filter="wobble-strong"), plain_defs), z=4, wc=0.8)

    # city wall with the open gate (in front of the skyline): hazy with distance, thin ink, little people on
    # the wall walk (head and shoulders above the parapet) and in the gateway
    WALL_TOP = WALL_Y - 170
    walkers_top = ""
    for i, (x, kind, pose) in enumerate([(390, "man", "stand"), (420, "woman", "stand"), (720, "child", "cheer"),
                                         (745, "man", "stand"), (1010, "woman", "cheer"), (1180, "man", "stand"),
                                         (1205, "child", "stand"), (1610, "woman", "stand"), (1640, "man", "cheer"),
                                         (1840, "elder", "stand"), (2060, "man", "stand"), (2085, "woman", "cheer")]):
        sc_ = 0.15 if kind != "child" else 0.17
        walkers_top += CH.citizen(x, WALL_TOP + (22 if kind != "child" else 8), sc_, 1 if i % 2 else -1, kind=kind,
                                  variant=i % 4, pose=pose, expr="happy")
    wall = PR.city_wall(-60, 2320, WALL_Y, height=170, gate=(GATE_X, 140), doors_open=1.0, seed=2, ink=0.55)
    wall += _end_tower(2320, WALL_Y, 170 / 260, ink=0.55)
    gateway = (CH.citizen(GATE_X - 40, WALL_Y - 2, 0.28, 1, kind="woman", variant=3, pose="stand", expr="happy") +
               CH.citizen(GATE_X + 42, WALL_Y - 2, 0.25, -1, kind="child", variant=1, pose="stand", expr="happy"))
    haze = ('<filter id="hz" x="-2%" y="-8%" width="104%" height="116%" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="saturate" values="0.72"/>'
            '<feColorMatrix type="matrix" values="0.74 0 0 0 0.251  0 0.74 0 0 0.229  0 0 0.74 0 0.195  0 0 0 1 0"/>'
            '</filter>')
    sc.add("wall", doc(f'<g filter="url(#hz)">{walkers_top}{wall}{gateway}</g>', haze), z=4.1, wc=0.7)

    # trees, bushes, the well (static)
    mid = ""
    for (x, y, s, ln) in [(120, 812, 0.4, -0.1), (470, 806, 0.36, 0.15), (1060, 812, 0.34, 0.1),
                          (1700, 810, 0.38, -0.12), (2050, 818, 0.42, 0.1), (2240, 830, 0.34, -0.2)]:
        mid += PR.palm_tree(x, y, s, lean=ln)
    for (x, y, s, sd) in [(760, 860, 0.32, 1), (1880, 880, 0.34, 2)]:
        mid += PR.olive_tree(x, y, s, seed=sd)
    for (x, y, s, v) in [(30, 960, 0.5, 0), (190, 905, 0.4, 1), (1700, 965, 0.42, 3), (2120, 1000, 0.5, 0),
                         (1215, 990, 0.4, 1), (60, 1300, 0.7, 1)]:
        mid += PR.bush(x, y, s, variant=v)
    mid += _well(470, 1040, 0.62)
    sc.add("mid", doc(mid), z=4.2, wc=0.8)

    # Jonah's knoll (dry, sandy) — raised and nearer: its slope overlaps the right edge of the pasture
    kd = S.smooth_path(KNOLL, closed=False) + f" L{SW + 80},{SH + 80} L{KNOLL[0][0]},{SH + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4.5)
    # sunlit rim just under the crest (the low sun is in the west, on the left)
    rp = [(x + 12, y + 18) for x, y in KNOLL[2:]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f7dfaa" stroke-width="18" opacity="0.6"/>'
    # a lower, darker sand terrace in front (the near slope, overlapping the plain)
    terr = [(1890, 1640), (2060, 1470)] + [kmap(x, y) for x, y in [(2450, 1330), (2800, 1250), (3200, 1215),
                                                                    (3550, 1190), (3900, 1170)]] + [(3900, 1095)]
    knoll += S.path(S.smooth_path(terr, closed=False) + f" L3900,{SH + 80} L1880,{SH + 80} Z", fill="url(#kn2)", sw=4)
    knoll += (f'<path d="{S.smooth_path([(x + 10, y + 16) for x, y in terr[1:]], closed=False)}" fill="none" '
              f'stroke="#ecc98e" stroke-width="12" opacity="0.5"/>')
    # the footpath Jonah climbed up from the city
    fp = S.smooth_path([kmap(x, y) for x, y in [(2330, SH + 60), (2420, 1450), (2560, 1300), (2700, 1180), (2760, 1050),
                                                (2700, 930), (2760, 862), (2800, 858), (2790, 935), (2840, 1050),
                                                (2790, 1190), (2650, 1320), (2540, 1460), (2480, SH + 60)]],
                       closed=True, tension=0.8)
    knoll += f'<path d="{fp}" fill="#f2d9a6" opacity="0.85"/>'
    # soft strata strokes and wind ripples
    for (x, y, w_) in [(2900, 960, 200), (3300, 900, 240), (3600, 1000, 180), (3050, 1110, 220), (2600, 1050, 120),
                       (3400, 1090, 200), (2950, 1350, 260), (3500, 1330, 220), (2500, 1180, 110), (3200, 1500, 260)]:
        x, y = kmap(x, y)
        knoll += (f'<path d="M{x - w_ / 2:.0f},{y:.0f} q{w_ / 2},-16 {w_},0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.42" stroke-linecap="round"/>')
    for (x, y, r) in [(2660, 852, 9), (3180, 846, 8), (3220, 852, 6), (3560, 842, 9), (2540, 935, 7), (2470, 1010, 8),
                      (2380, 1150, 9), (2960, 1240, 8), (3380, 1265, 7)]:
        x, y = kmap(x, y)
        knoll += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.4}" ry="{r}" fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="3"/>'
    knoll += _rock(*kmap(2330, 1260), 130, 58, seed=43, sw=4) + _rock(*kmap(3540, 1010), 110, 50, seed=44, sw=4)
    knoll += (PR.bush(*kmap(2560, 1120), 0.6, variant=2) + PR.bush(*kmap(3700, 900), 0.7, variant=2) +
              PR.bush(*kmap(3080, 1235), 0.75, variant=2))
    for (x, y, s_) in [(2600, 880, 0.7), (3150, 845, 0.6), (2430, 1080, 0.75), (3330, 1000, 0.7), (2880, 1200, 0.8),
                       (3700, 1180, 0.9)]:
        knoll += PR.grass_tuft(*kmap(x, y), s_, variant=1)
    sc.add("knoll", doc(S.g(knoll, filter="wobble"),
                        S.lin_grad("kn", [(0, "#ebc68a"), (0.3, "#e2b679"), (1, "#d09c62")]) +
                        S.lin_grad("kn2", [(0, "#d3a065"), (1, "#bb8652")])), z=5, wc=0.9)

    # booth (behind the plant) + soft shadow — same drawing as s11
    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{P["ink"]}" opacity="0.16" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    # Jonah's few belongings in the booth: a water jar and a sack
    booth += PR.sack(XB - 30, GY + 2, 0.62, seed=3) + PR.jar(XB + 95, GY - 50, 0.6)
    sc.add("booth", doc(booth), z=5.6, wc=0.8)     # in front of the clouds and doves

    # =============================================================== PEOPLE on the plain
    ground_sh = []          # static long shadows of everyone who stays on the ground (one flattened layer)

    def register(name, bbox, heart):
        FIGS.append((name, bbox, heart))

    def person(name, x, y, kind, variant, pose="stand", facing=1, expr="happy", motion=None, frames=None,
               frame_at=None, s=None, hops=None, H=0):
        s = s or plain_scale(y)
        if frames is None:
            svg = doc(CH.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, expr=expr))
            poses = [pose]
        else:
            svg = [doc(CH.citizen(x, y, s, facing, kind=kind, variant=variant, pose=p, expr=e)) for p, e in frames]
            poses = [p for p, _ in frames]
        sc.add(name, svg, z=6 + y / 1000, wc=0.6, motion=motion, frame_at=frame_at)
        width, height = (90, 224) if kind == "child" else (120, 330)
        sh = long_shadow(x, y, s, width, height)
        if hops:
            sc.add(name + "_sh", shdoc(sh), z=5.95 + y / 100000, wc=0, motion=shadow_motion(x, y, hops))
        else:
            ground_sh.append(sh)
        bbs = [CH.body_points(CH.citizen, x, y, s, facing, kind=kind, variant=variant, pose=p) for p in poses]
        bb = (min(b["bbox"][0] for b in bbs), min(b["bbox"][1] for b in bbs) - H,
              max(b["bbox"][2] for b in bbs), y + 4)
        top = bbs[0]["head_top"]
        register(name, bb, (top[0], top[1] - 25 - H))
        return s

    def breathe(x, y, ph, amt=0.012, per=2.8):
        return M.breathe(amt, per, pivot=(x, y), phase=ph)

    def nod(x, y, ph, deg=1.2, per=2.6):
        return M.sway(deg, per, pivot=(x, y), phase=ph)

    # elders by the well (left), talking across it
    person("elder0", 380, 1010, "elder", 0, "stand", 1, "happy", motion=M.combine(nod(380, 1010, 0.1), breathe(380, 1010, 0.3)))
    person("elder1", 600, 990, "elder", 1, "stand", -1, "peaceful", motion=M.combine(nod(600, 990, 0.6, 1.0, 3.1),
                                                                                    breathe(600, 990, 0.7)))
    # mothers with their children close beside them (the child overlapping the mother's robe)
    person("mother0", 700, 1072, "woman", 1, "stand", 1, "happy", motion=M.combine(nod(700, 1072, 0.2, 1.5, 3.0),
                                                                                  breathe(700, 1072, 0.1)))
    person("girl0", 736, 1088, "child", 1, "stand", -1, "happy", motion=M.combine(M.bob(2.5, 1.7, 0.2),
                                                                                  breathe(736, 1088, 0.5)))
    person("mother1", 1180, 940, "woman", 3, "stand", -1, "happy", motion=M.combine(nod(1180, 940, 0.4, 1.2, 2.7),
                                                                                    breathe(1180, 940, 0.9)))
    person("child_g", 1157, 952, "child", 2, "stand", 1, "happy", motion=M.combine(M.bob(2.5, 1.5, 0.3),
                                                                                   breathe(1157, 952, 0.2)))
    # a family in front: grandfather, mother and her toddler hopping with joy right in front of her robe
    person("grandpa", 300, 1290, "elder", 2, "stand", 1, "happy", motion=M.combine(nod(300, 1290, 0.15, 1.2, 2.8),
                                                                                   breathe(300, 1290, 0.4)))
    person("mother2", 430, 1322, "woman", 2, "stand", 1, "happy", motion=M.combine(nod(430, 1322, 0.55, 1.4, 3.2),
                                                                                   breathe(430, 1322, 0.2)))

    # children playing (hops with rests: stand <-> cheer)
    for (nm, x, y, v, fc, seed, H, s_) in [("kid2", 1005, 1295, 3, 1, 5, 22, None), ("kid3", 560, 1185, 1, 1, 6, 18, None),
                                           ("toddler", 470, 1338, 0, -1, 7, 13, 0.56)]:
        hops = hop_sched(seed, T + 1)
        person(nm, x, y, "child", v, facing=fc, frames=[("stand", "happy"), ("cheer", "happy")],
               frame_at=hop_frame(hops), motion=hop_motion(x, y, hops, H), s=s_, hops=hops, H=H)

    # two children tossing a ball: each catches it with raised hands on a little hop, and throws it straight back
    PB = 1.25                                  # one flight
    BALL_H = 14
    kidA, kidB = (930, 1200, 0, 1), (1190, 1215, 2, -1)
    catch_pts = []
    for i, (x, y, v, fc) in enumerate((kidA, kidB)):
        arrivals = [PB * (2 * k + i) for k in range(int(T / (2 * PB)) + 3)]
        hops = [(ta - 0.15, 0.45) for ta in arrivals]

        def arms(t, arrivals=arrivals):
            return 1.0 if any(ta - 0.38 <= t <= ta + 0.3 for ta in arrivals) else 0.0
        s_ = person(f"kid{i}", x, y, "child", v, facing=fc, frames=[("stand", "happy"), ("cheer", "happy")],
                    frame_at=arms, motion=hop_motion(x, y, hops, BALL_H), hops=hops, H=BALL_H)
        hand = CH.body_points(CH.citizen, x, y, s_, fc, kind="child", variant=v, pose="cheer")["hands"][0]
        lift = BALL_H * math.sin(math.pi * 0.15 / 0.45)
        catch_pts.append((hand[0] - 6 * fc, hand[1] - 16 * s_ - lift))   # just inside / above the raised hand
    (xa, ya), (xb, yb) = catch_pts
    ARC = 175
    ball_svg = doc(S.g(f'<circle cx="1060" cy="900" r="15" fill="#e2683f" stroke="{P["ink"]}" stroke-width="3.5"/>'
                       f'<path d="M1046,895 Q1060,884 1074,895" fill="none" stroke="#f6d36a" stroke-width="4"/>'
                       f'<path d="M1048,908 Q1060,916 1072,906" fill="none" stroke="#3b8b89" stroke-width="4"/>',
                       filter="wobble-fine"))

    def ball(t):
        u = (t / PB) % 2.0
        if u < 1:
            x0, y0, x1, y1, v = xa, ya, xb, yb, u
        else:
            x0, y0, x1, y1, v = xb, yb, xa, ya, u - 1
        x = x0 + (x1 - x0) * v
        y = y0 + (y1 - y0) * v - ARC * 4 * v * (1 - v)
        return Tf(dx=x - 1060, dy=y - 900, rot=360 * v, px=1060, py=900)
    sc.add("ball", ball_svg, z=7.5, wc=0.4, motion=ball)
    ball_zone = []                             # the ball's arc, as small boxes (hearts must not cross it)
    for k in range(11):
        v = k / 10
        x_, y_ = xa + (xb - xa) * v, ya + (yb - ya) * v - ARC * 4 * v * (1 - v)
        ball_zone.append(("ball", (x_ - 20, y_ - 20, x_ + 20, y_ + 20)))

    # men and women near the gate and along the wall (far, small)
    person("man0", GATE_X - 140, 838, "man", 0, "stand", 1, "happy", motion=breathe(GATE_X - 140, 838, 0.2))
    person("woman0", GATE_X + 120, 842, "woman", 0, "stand", -1, "happy", motion=breathe(GATE_X + 120, 842, 0.6))
    person("man1", GATE_X + 210, 852, "man", 2, "cheer", -1, "happy",
           motion=M.combine(nod(GATE_X + 210, 852, 0.3, 2.0, 1.6), breathe(GATE_X + 210, 852, 0.1)))
    person("man2", 250, 868, "man", 1, "stand", 1, "happy", motion=breathe(250, 868, 0.4))
    person("woman1", 940, 880, "woman", 2, "cheer", 1, "happy",
           motion=M.combine(nod(940, 880, 0.1, 2.0, 1.8), breathe(940, 880, 0.3)))

    # people walking in and out of the gate (2-frame walk flipbook while x / y move; they never stop)
    def walker(name, kind, variant, p0, p1, facing, step=0.36, phase=0.0):
        (x0, y0), (x1, y1) = p0, p1
        s0 = plain_scale(y0)
        frames = [shdoc(long_shadow(x0, y0, s0, 120, 330) +
                      CH.citizen(x0, y0, s0, facing, kind=kind, variant=variant, pose=p, expr="happy"))
                  for p in ("walk_a", "walk_b")]
        ta, tb = -1.0, T + 1.0

        def m(t):
            u = _clamp((t - ta) / (tb - ta))
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            k = plain_scale(y) / s0
            return Tf(dx=x - x0, dy=y - y0, sx=k, sy=k, px=x0, py=y0)
        sc.add(name, frames, z=6 + (y0 + y1) / 2000, wc=0.6, motion=m,
               frame_at=lambda t: float(int(t / step + phase) % 2))
        register(name, None, None)

    walker("walk0", "man", 3, (GATE_X + 12, WALL_Y + 6), (GATE_X - 170, 1070), -1, 0.38)      # out of the gate
    walker("walk1", "woman", 2, (780, 818), (1290, 818), 1, 0.36, 0.5)                    # toward the gate
    walker("walk2", "elder", 3, (1760, 812), (1470, 800), -1, 0.42)                       # toward the gate

    # =============================================================== ANIMALS in the pasture
    def beast(name, x, y, kind, facing, s, motion=None, hops=None, H=0):
        sc.add(name, doc(PR.animal(x, y, s, facing, kind=kind)), z=6 + y / 1000, wc=0.6, motion=motion)
        l, t_, r, b = ABOX[kind]
        width = (r - l) * 0.85
        sh = long_shadow(x, y, s, width, (b - t_) * 0.75)
        if hops:
            sc.add(name + "_sh", shdoc(sh), z=5.95 + y / 100000, wc=0, motion=shadow_motion(x, y, hops))
        else:
            ground_sh.append(sh)
        if facing < 0:
            l, r = -r, -l
        register(name, (x + l * s, y + t_ * s - H, x + r * s, y + b * s),
                 (x + HEAD_DX[kind] * s * facing, y + t_ * s - 25 - H))

    sheep = [(1380, 1245, 1, 0.6), (1640, 1292, -1, 0.62), (1760, 1225, -1, 0.58), (1480, 1395, 1, 0.66),
             (1840, 1390, 1, 0.64)]
    for i, (x, y, fc, s) in enumerate(sheep):
        mot = M.combine(M.bob(2.5, 2.2 + 0.3 * i, i * 0.27), nod(x, y, i * 0.31, 1.2, 2.9))
        hops = None
        if i == 1:     # the one who bleats: a happy little hop
            hops = [(t_baa - 0.12, 0.38)]
            mot = M.combine(mot, hop_motion(x, y, hops, 16))
        beast(f"sheep{i}", x, y, "sheep", fc, s, mot, hops=hops, H=16 if hops else 0)
    # lambs frolic (hops with rests)
    for i, (x, y, fc) in enumerate([(1300, 1445, 1), (1740, 1465, -1)]):
        hops = hop_sched(20 + i, T + 1, dur=(0.34, 0.44), rest=(0.7, 1.3))
        beast(f"lamb{i}", x, y, "sheep", fc, 0.4, hop_motion(x, y, hops, 18), hops=hops, H=18)
    beast("goat0", 1840, 1110, "goat", -1, 0.55, M.combine(nod(1840, 1110, 0.2, 1.8, 2.3), M.bob(2, 2.0, 0.1)))
    beast("goat1", 2000, 1285, "goat", -1, 0.6, M.combine(nod(2000, 1285, 0.7, 1.5, 2.6), M.bob(2, 2.4, 0.4)))
    beast("cow0", 1590, 1062, "cow", 1, 0.5, M.combine(nod(1590, 1062, 0.5, 0.8, 3.6), breathe(1590, 1062, 0.2)))
    beast("cow1", 1150, 1385, "cow", 1, 0.66, M.combine(nod(1150, 1385, 0.1, 0.8, 3.9), breathe(1150, 1385, 0.6)))
    beast("donkey0", 2060, 1100, "donkey", -1, 0.5, M.combine(nod(2060, 1100, 0.4, 1.4, 3.0), breathe(2060, 1100, 0.3)))
    beast("donkey1", 1290, 1110, "donkey", 1, 0.5, M.combine(nod(1290, 1110, 0.8, 1.2, 3.3), breathe(1290, 1110, 0.5)))
    # a shepherd boy cheering among the flock (between the goat and the donkey at the back)
    hops = hop_sched(9, T + 1, n=(2,), dur=(0.5, 0.6), rest=(1.0, 1.6))
    person("shepherd", 1940, 1180, "child", 0, facing=-1, frames=[("stand", "happy"), ("cheer", "happy")],
           frame_at=hop_frame(hops), motion=hop_motion(1940, 1180, hops, 14), s=0.56, hops=hops, H=14)

    # one static layer with every grounded figure's long shadow (under all figures)
    sc.add("ground_shadows", shdoc("".join(ground_sh)), z=5.9, wc=0.3)

    # baa arcs
    bx, by = 1640 - 0.62 * 112, 1292 - 0.62 * 100
    sc.add("baa", doc(_baa(bx, by, 0.9)), z=9, wc=0.3, motion=lambda t: Tf(
        alpha=_env(t, t_baa - 0.05, t_baa + 0.1, t_baa + 0.7, t_baa + 1.0),
        sx=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"),
        sy=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"), px=bx, py=by))

    # hearts: one above each head, nudged / dropped where it would rise across someone standing behind
    people = {"elder0", "elder1", "mother0", "girl0", "mother1", "child_g", "grandpa", "mother2", "kid2", "kid3",
              "toddler", "kid0", "kid1", "man0", "woman0", "man1", "man2", "woman1"}
    beasts = {n for n, _, _ in FIGS if n.startswith(("sheep", "lamb", "goat", "cow", "donkey"))} | {"shepherd"}
    FIGS[:] = [f for f in FIGS if f[1] is not None]
    HEARTS["people"] = _place_hearts(people, extra_obstacles=ball_zone)
    HEARTS["animals"] = _place_hearts(beasts)

    # =============================================================== WITHERED PLANT + JONAH
    def castor_rot(t):
        return 0.6 * math.sin(2 * math.pi * t / 3.6) + 0.25 * math.sin(2 * math.pi * t / 1.7)

    plant = doc(PR.castor_plant(XP, GY, SP, growth=1, wither=1, bite=1, side=1, seed=2))
    sc.add("castor", plant, z=10, wc=0.9, motion=lambda t: Tf(rot=castor_rot(t), px=XP, py=GY))

    # God's golden light on Jonah (lines 0-1): the beam and rays behind him stop short of the plant's stem
    a_light = lambda t: _env(t, t_light0, t_light0 + 1.2, t_sw0 + 0.6, t_sw0 + 2.3)
    a_end = lambda t: 0.55 * M.progress(t, t_peace - 0.2, t_peace + 1.2, "sine")
    GAP = (XJ + 60, 190)       # where the clouds part
    beam = doc(
        S.g(f'<path d="M{XJ - 90},{GAP[1]} L{XJ + 160},{GAP[1]} L{XJ + 140},{GY + 30} L{XJ - 260},{GY + 30} Z" '
            f'fill="url(#bm)"/>', filter="blur-md") +
        f'<ellipse cx="{XJ - 30}" cy="{GY - 170}" rx="240" ry="270" fill="url(#jg)"/>',
        S.lin_grad("bm", [(0, "#ffe6a8", 0.22), (0.6, "#ffdc96", 0.12), (1, "#ffd68a", 0.05)]) +
        S.rad_grad("jg", [(0, "#ffe2a0", 0.26), (0.5, "#ffd890", 0.1), (1, "#ffd080", 0)]))
    sc.add("god_light", beam, z=10.5, wc=0, blend="add",
           motion=lambda t: Tf(alpha=max(a_light(t), a_end(t)) * (0.85 + 0.15 * math.sin(t * 2.6))))
    rays = doc(S.g(_ray_fan(GAP[0], GAP[1] - 40, 700, [88, 96, 104, 112, 120, 128], w0=8, w1=44,
                            fill="#ffe2a0", opacity=0.3), filter="soft"))
    sc.add("rays", rays, z=10.6, wc=0, blend="add", motion=lambda t: Tf(
        alpha=a_light(t) * (0.75 + 0.25 * math.sin(t * 1.9)),
        rot=2.0 * math.sin(t * 0.45), px=GAP[0], py=GAP[1] - 40))

    # Jonah: sad -> thoughtful (sorry) -> looking toward the city (worried) -> peaceful (the only smile)
    exprs = ["sad", "sorry", "worried", "peaceful"]
    jshadow = CH.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)
    jframes = [doc(jshadow + CH.jonah(XJ, GY, SP, -1, pose="sit", expr=e)) for e in exprs]
    switch = [(t_thought, 0.25), (t_look, 0.3), (t_peace, 0.35)]

    def jonah_frame(t):
        f = 0.0
        for i, (ts, d) in enumerate(switch):
            if t >= ts:
                f = i + M.progress(t, ts, ts + d, "sine")
        return f

    def jonah_tf(t):
        """Rotations are about the seat (XJ, GY), so he stays planted; + = leans back / looks up."""
        s = 1 + 0.011 * math.sin(2 * math.pi * t / 3.2)
        sy = 1.0
        rot = 0.0
        # hears his name: sits up and looks up toward the voice and the light, then settles
        e = _env(t, t_name, t_name + 0.6, t_name + 0.8, t_name + 1.6)
        rot += 2.6 * e
        sy *= 1 + 0.03 * e
        # thoughtful sigh, looking down at the leaf
        u = t - t_thought
        if 0 <= u < 1.4:
            s *= 1 - 0.012 * math.sin(math.pi * u / 1.4)
            rot -= 1.2 * math.sin(math.pi * u / 1.4)
        # leans a little toward the city below, relaxing as his face softens
        rot -= 2.4 * M.progress(t, t_look, t_look + 0.6, "sine") * (1 - M.progress(t, t_peace - 0.1, t_peace + 1.0, "sine"))
        # peaceful: a slow, deep, relaxed breath
        k = M.progress(t, t_peace - 0.1, t_peace + 0.8, "sine")
        s *= 1 + k * 0.01 * math.sin(2 * math.pi * (t - t_peace) / 2.4)
        return Tf(rot=rot, sx=s, sy=s * sy, px=XJ, py=GY)

    sc.add("jonah", jframes, z=11, frame_at=jonah_frame, motion=jonah_tf, wc=0.6)

    def carry(j, p):
        """Where Jonah's transform j carries the stage point p."""
        r = math.radians(j.rot)
        x, y = (p[0] - XJ) * j.sx, (p[1] - GY) * j.sy
        return (XJ + x * math.cos(r) - y * math.sin(r) + j.dx, GY + x * math.sin(r) + y * math.cos(r) + j.dy)

    # the dry leaf in Jonah's near hand
    hand = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit")["hands"][1]
    lcx, lcy = hand[0] - 58, hand[1] - 62
    leaf = doc(_dry_leaf(lcx, lcy, 50, rot=-30, stalk=(hand[0] - 2, hand[1] + 4)))

    def leaf_tf(t):
        j = jonah_tf(t)
        hx, hy = carry(j, hand)
        lift = M.progress(t, t_thought - 0.1, t_thought + 0.7, "inout") * (1 - M.progress(t, t_look, t_look + 0.6))
        twirl = 4 * math.sin(2 * math.pi * t / 2.2) * _env(t, l0.start + 0.6, l0.start + 1.2, l1.end, l1.end + 0.6)
        rot = j.rot - 14 * lift + twirl + 1.5 * math.sin(2 * math.pi * t / 1.3)
        return Tf(dx=hx - hand[0], dy=hy - hand[1] - 6 * lift, rot=rot, sx=j.sx, sy=j.sy, px=hand[0], py=hand[1])

    sc.add("leaf", leaf, z=11.2, wc=0.5, motion=leaf_tf)

    # warm light ON Jonah (God's light, lines 0-1, and again as his face softens): a soft glow on his head and
    # shoulders plus a thin rim on his top-left edge, both clipped to his silhouette; it follows his motion
    J = CH.jonah(XJ, GY, SP, -1, pose="sit", expr="sad")
    hb = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit")
    hx, hy = hb["head"]
    jl_defs = (
        '<filter id="jwhite" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>'
        '<filter id="jblack" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>'
        f'<mask id="jsil" maskUnits="userSpaceOnUse" x="0" y="0" width="{SW}" height="{SH}">'
        f'<g filter="url(#jwhite)">{J}</g></mask>'
        f'<mask id="jrim" maskUnits="userSpaceOnUse" x="0" y="0" width="{SW}" height="{SH}">'
        f'<g filter="url(#jwhite)">{J}</g><g transform="translate(9,11)" filter="url(#jblack)">{J}</g></mask>' +
        S.rad_grad("jl", [(0, "#ffe2a0", 1), (0.55, "#ffdc96", 0.5), (1, "#ffd890", 0)]) +
        S.rad_grad("jr", [(0, "#fff0c8", 1), (0.6, "#ffe6b0", 0.7), (1, "#ffe0a0", 0)]))
    jl_body = (f'<g mask="url(#jsil)"><ellipse cx="{f1(hx - 10)}" cy="{f1(hy + 50)}" rx="200" ry="230" fill="url(#jl)" '
               f'opacity="0.42"/></g>'
               f'<g mask="url(#jrim)"><ellipse cx="{f1(hx - 50)}" cy="{f1(hy - 20)}" rx="250" ry="260" fill="url(#jr)"/></g>')
    j_light = lambda t: max(a_light(t), a_end(t))
    sc.add("jonah_light", doc(jl_body, jl_defs), z=11.27, wc=0, blend="add",
           motion=lambda t: (lambda j: Tf(j.dx, j.dy, j.rot, j.sx, j.sy, 0.38 * j_light(t), j.px, j.py))(jonah_tf(t)))

    # a dead leaf hangs on the canopy from the start, wobbles loose and flutters down (never crossing Jonah)
    FL_STALK = (XP + 212, GY - 462)
    fl0 = (XP + 200, GY - 412)         # its centre, overlapping a hanging canopy leaf
    fl1 = (XB - 230, GY + 14)          # it lands flat in front of the booth
    fleaf = doc(_dry_leaf(fl0[0], fl0[1], 40, rot=172, col="#a5844c", stalk=FL_STALK))
    t_wob = t_leaf_fall - 0.4

    def about_root(p, deg):
        r = math.radians(deg)
        x, y = p[0] - XP, p[1] - GY
        return (XP + x * math.cos(r) - y * math.sin(r), GY + x * math.sin(r) + y * math.cos(r))

    def fleaf_tf(t):
        if t < t_leaf_fall:
            cr = castor_rot(t)
            c = about_root(fl0, cr)
            wob = 9 * math.sin(2 * math.pi * (t - t_wob) / 0.2) * _env(t, t_wob, t_wob + 0.08, t_leaf_fall - 0.12,
                                                                      t_leaf_fall)
            return Tf(dx=c[0] - fl0[0], dy=c[1] - fl0[1], rot=cr + wob, px=fl0[0], py=fl0[1])
        cr = castor_rot(t_leaf_fall)
        st = about_root(fl0, cr)
        u = M.progress(t, t_leaf_fall, t_leaf_fall + 3.2, "linear")
        e = 1 - (1 - u) ** 1.4
        sway = math.sin(2 * math.pi * u * 1.6) * (1 - u) * min(1.0, u / 0.08)
        x = st[0] + (fl1[0] - st[0]) * e + 60 * sway
        y = st[1] + (fl1[1] - st[1]) * u
        rot = cr * (1 - u) + 50 * sway - 8 * u
        flip = abs(math.cos(math.pi * u * 2.6))          # tumbling (seen edge-on now and then)
        sy = ((0.3 + 0.7 * flip) * (1 - u) + 0.5 * u) * min(1.0, 1 - (1 - flip) * 0.7 * min(1.0, u / 0.15))
        return Tf(dx=x - fl0[0], dy=y - fl0[1], rot=rot, sx=1 - 0.1 * u, sy=max(0.3, min(1.0, sy)),
                  px=fl0[0], py=fl0[1])

    sc.add("fall_leaf", fleaf, z=11.1, wc=0.5, motion=fleaf_tf)

    # =============================================================== DOVES gliding home toward the city
    def flock(name, birds, t0, t1, dx, dy, z, fade_in=0.4):
        """birds: [(x, y, scale)] at t0; the flock drifts by (dx, dy) until t1 (flapping flipbook)."""
        frames = []
        wings = (-1.0, -0.35, 0.35, 1.0)
        for k in range(4):
            body = ""
            for i, (x, y, sc_) in enumerate(birds):
                body += PR.dove(x, y, sc_, -1, wing=wings[(k + 2 * i) % 4])
            frames.append(doc(body))
        seq = [0, 1, 2, 3, 2, 1]
        sc.add(name, frames, z=z, wc=0.4, frame_at=lambda t: float(seq[int(t * 9) % len(seq)]),
               motion=M.combine(M.keys([(t0, {"dx": 0, "dy": 0}), (t1, {"dx": dx, "dy": dy})], "linear"),
                                M.bob(6, 0.9), lambda t: Tf(alpha=_env(t, t0, t0 + fade_in, t1 - 0.3, t1))))

    # the first flock flies on toward the city ahead of the camera and leaves the frame over the top
    flock("doves_a", [(3700, 330, 0.42), (3790, 296, 0.36), (3830, 360, 0.34)], -0.5, l2.start + 2.0, -2400, -300,
          5.4, fade_in=0.01)
    flock("doves_b", [(3250, 300, 0.42), (3340, 260, 0.36), (3390, 335, 0.34)], l3.start + 2.0, T + 2.5, -760, -30,
          5.45)

    # =============================================================== FOREGROUND (static)
    fg = ""
    for (x, y, s, v) in [(3560, 1120, 1.2, 1), (3720, 1090, 1.0, 1), (2620, 1300, 1.0, 1), (3150, 1400, 1.1, 1),
                         (2990, 1190, 0.9, 2), (3300, 1250, 0.8, 1), (3250, 1262, 0.7, 2)]:
        fg += PR.grass_tuft(*kmap(x, y), s, variant=v)
    fg += _rock(*kmap(3420, 1160), 220, 96, seed=51) + _rock(*kmap(3700, 1385), 260, 120, seed=52)
    sc.add("fg", doc(S.g(fg)), z=20, wc=0.9)

    # =============================================================== CAMERA
    # Slow, gentle moves only: each move is re-parametrised by output-space arc length with soft ramps.
    C0 = Cam(XJ - 40, 455, 1600)      # Jonah + plant (Jonah near where s11 leaves him), the city end on the left
    C0b = Cam(XJ + 60, 500, 1400)     # slow push-in while God speaks
    Cw = Cam(1620, 850, 2420)         # held wide view: the whole city, the plain, the pasture, Jonah on his knoll
    Cw2 = Cam(1590, 860, 2390)
    C1 = Cam(1100, 1010, 1850)        # the people
    C2 = Cam(1620, 1120, 1800)        # the animals
    C3 = Cam(XJ - 20, 640, 1720)      # back up the knoll to Jonah
    Cf = Cam(hx, 600, 1450)           # slow push-in: Jonah's face at the centre (s13 opens on him there)
    moves = []
    for (ta, tb, cams, r) in [(t_still, t_sw0, [C0, C0b], 0.45), (t_sw0, t_sw1, [C0b, Cw], 0.27),
                              (t_sw1, t_hold1, [Cw, Cw2], 0.5), (t_hold1, t_back1, [Cw2, C1, C2, C3], 0.15),
                              (t_back1, T, [C3, Cf], 0.5)]:
        fn, _, knots = _cam_path(cams)
        moves.append((ta, tb, fn, r, knots))

    def camera(t):
        for (ta, tb, fn, r, _) in moves:
            if t < ta:
                return fn(0.0)
            if t <= tb:
                return fn(_glide((t - ta) / (tb - ta), r))
        return moves[-1][2](1.0)

    sc.camera = camera
    gl = moves[3]
    sc.cam_marks = {"people": gl[0] + (gl[1] - gl[0]) * _glide_inv(gl[4][1], gl[3]),
                    "pasture": gl[0] + (gl[1] - gl[0]) * _glide_inv(gl[4][2], gl[3])}

    # =============================================================== FX
    sc.fx = [
        FX.sparkles((XJ - 330, GY - 520, XJ + 150, GY - 40), count=22, t0=t_light0 + 0.3, t1=t_sw0 + 1.6,
                    color=(255, 238, 175), size=(9, 20), drift=-10, seed=21),
        FX.motes((XJ - 500, 0, XJ + 300, GY), count=30, t0=t_light0, t1=t_sw0 + 2.0, color=(255, 244, 205), seed=22),
        FX.sparkles((200, 700, 2300, 1150), count=34, t0=t_city0 + 0.4, t1=l3.end, color=(255, 238, 175),
                    size=(8, 18), drift=-8, seed=23),
        hearts_fx(HEARTS["people"], t_hearts_p0, t_hearts_p1, seed=31),
        hearts_fx(HEARTS["animals"], t_hearts_a0, t_hearts_a1, life=2.4, seed=32),
        FX.sparkles((XJ - 300, GY - 420, XJ + 150, GY - 60), count=16, t0=t_peace, t1=T + 1, color=(255, 240, 190),
                    size=(8, 16), drift=-6, seed=24),
    ]

    # =============================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("birds", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8, pan=-0.2)
    sc.sfx("sheep", t_baa, gain_db=-11, pan=-0.3)
    sc.sfx("chime", t_chime, gain_db=-10)
    return sc
