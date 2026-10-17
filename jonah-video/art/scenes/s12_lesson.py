"""Scene 12 — God's lesson (Jonah 4:10-11).

All four lines are God speaking, gently. Late afternoon, warm golden light. One wide 3800 x 1650 stage:

  * right: Jonah's dry knoll east of the city, with his little booth and the withered castor plant (same
    drawings and scale as s11). Jonah sits at the edge of the knoll, facing the city, holding a dry leaf;
  * left / below: the green Tigris plain in front of Nineveh's wall and open gate, full of life — elders,
    mothers, children playing ball, men at the gate, and a pasture with sheep, lambs, goats, cows, donkeys.

Timing (all keyed to ctx.lines):
  line 0  "约拿，这棵蓖麻不是你栽种的，"  clouds part, golden rays and sparkles fall on Jonah; he is sad, turns
          the dry leaf in his hand; another dead leaf flutters down from the plant.
  line 1  "你尚且这样爱惜它。"  Jonah looks down at the leaf, thoughtful (lifts it a little).
  line 2  "尼尼微有十二万多…人"  the camera sweeps out over the whole city (wide reveal on "尼尼微") and settles
          on the people; golden sparkles twinkle over the plain; hearts rise over children, mothers, elders.
  line 3  "还有许多牲畜，我怎能不爱惜呢？"  the camera glides to the pasture (a sheep bleats), hearts over the
          animals; then it rises back to Jonah, whose face softens (peaceful); a chime and soft sparkles at the end.
"""
import math
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
GY = 830                 # knoll top: Jonah, plant root, booth
SP = 1.3                 # Jonah / plant / booth scale (as in s11)
XJ = 2840                # Jonah (sitting, facing the city on the left)
XP = 3030                # withered castor root
XB = XP + PR.CASTOR_BOOTH_DX * SP   # booth (the dead canopy arches over its roof, as in s11)

WALL_Y = 770             # city wall ground line
GATE_X = 1380
SUN = (430, 300)         # low western sun

# knoll silhouette (top edge), left slope runs down into the plain
KNOLL = [(2060, SH + 80), (2170, 1450), (2300, 1220), (2430, 1040), (2560, 905), (2700, 845), (2900, 830),
         (3200, 826), (3500, 816), (3880, 806)]


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


def _sharp(f, soft=0.4):
    """Flipbook index that holds each drawing and only crossfades briefly around the switch."""
    i = math.floor(f)
    u = f - i
    lo = 0.5 - soft / 2
    return i + _clamp((u - lo) / soft)


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
    out = f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(w * 0.62)}" ry="{f1(12 * s)}" fill="{P["ink"]}" opacity="0.18" filter="url(#soft)"/>'
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


def _end_tower(cx, y, k, col=None):
    """Corner tower closing the right end of the city wall (matches props.city_wall colours at scale k)."""
    col = col or P["sand"]
    w, h = 104 * k, 170 + 64 * k
    x0, x1, top = cx - w / 2, cx + w / 2, y - h
    sw = 4 * 0.7
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


def hearts_fx(spots, t0, t1, rise=150, life=2.6, period=2.9, size=34, seed=3):
    """Hearts rising from stage spots [(x, y, spread)] between t0 and t1 (each spot emits on a staggered cycle)."""
    rng = np.random.default_rng(seed)
    slots = []
    for (x, y, spread) in spots:
        for j in range(2):
            slots.append((x + rng.uniform(-spread, spread), y + rng.uniform(-10, 6), rng.uniform(0, period),
                          rng.uniform(0, 6.28), rng.uniform(0.8, 1.15)))

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
            sx = x + 16 * math.sin(2 * math.pi * age / 1.7 + ph)
            sy = y - rise * (1 - (1 - u) ** 1.6)
            grow = 0.55 + 0.45 * min(1.0, age / 0.45)
            a = min(1.0, age / 0.3) * min(1.0, (life - age) / 0.7)
            ox, oy = view.to_out(sx, sy)
            spr = _heart_sprite(round(size * k * grow * view.scale / 2) * 2)
            if a < 0.999:
                spr = spr.copy()
                spr.putalpha(spr.getchannel("A").point(lambda v, a=a: int(v * a)))
            frame.alpha_composite(spr, (int(ox - spr.width / 2), int(oy - spr.height / 2)))
        return frame
    return fx


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    l0, l1, l2, l3 = L[0], L[1], L[2], L[3]

    # --- key times ----------------------------------------------------------------------------
    t_light0 = l0.start - 0.2                 # God speaks: clouds part, golden rays on Jonah
    t_leaf_fall = l0.start + 0.8              # a dead leaf flutters down from the plant ("这棵蓖麻")
    t_thought = l1.start + 0.2                # "你尚且这样爱惜它" -> Jonah looks at the leaf, thoughtful
    t_look = l1.end - 0.15                    # he lifts his gaze toward the city
    t_pan0, t_pan1 = l1.end - 0.35, l2.start + 2.5   # sweep out over the city to the people
    t_city0 = l2.start - 0.2                  # golden sparkles begin to twinkle over the plain
    t_hearts_p = l2.start + 0.7               # hearts over the people
    t_pan2, t_pan3 = l2.end - 0.15, l3.start + 1.0   # glide to the pasture
    t_baa = l3.start + 0.85                   # a sheep bleats ("牲畜")
    t_hearts_a = l3.start + 0.4
    t_back0, t_back1 = l3.start + 1.75, l3.end - 0.55  # "我怎能不爱惜呢" — rise back to Jonah
    t_peace = l3.end - 0.62                   # Jonah's face softens as the camera settles
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
    sc.add("far_clouds", far_clouds, z=2, wc=0.6)     # static: flattens with the whole background (cheap)
    cl_l = doc(S.g(S.cloud(2590, 300, 420, 116, "#fdf1e2", seed=11, sw=3.5, shade_fill="#f0c9b0") +
                   S.cloud(2280, 380, 220, 66, "#fdf1e2", seed=14, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    cl_r = doc(S.g(S.cloud(3250, 285, 460, 124, "#fdf1e2", seed=12, sw=3.5, shade_fill="#f0c9b0") +
                   S.cloud(3640, 400, 280, 84, "#fdf1e2", seed=13, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    part = lambda t: M.progress(t, t_light0 - 0.3, l0.start + 2.2, "inout")
    # (z above the static land so sky + land flatten into one item; they never overlap the hills or city)
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
    # distant dunes east of the city (seen behind Jonah)
    far += S.path(S.smooth_path([(2280, 700), (2500, 660), (2750, 690), (3000, 650), (3300, 680), (3600, 640),
                                 (3900, 660)], closed=False) + " L3900,900 L2280,900 Z", fill="#ecd3a0", stroke=False, extra=FAR_INK)
    for (x, y, w_) in [(2560, 708, 140), (2980, 690, 180), (3420, 676, 150), (3760, 690, 120)]:
        far += (f'<path d="M{x - w_ / 2},{y} q{w_ / 2},-14 {w_},0" fill="none" stroke="#d9b98a" stroke-width="4" '
                f'opacity="0.6" stroke-linecap="round"/>')
    for (x, y, s) in [(2420, 650, 0.12), (2470, 655, 0.1), (3140, 620, 0.11)]:
        far += PR.palm_tree(x, y, s, lean=0.1)
    sc.add("far_hills", doc(S.g(far, filter="wobble")), z=3, wc=0.6)
    city = PR.nineveh_skyline(-60, 2240, 668, scale=0.62, seed=3, haze=0.3, tint="#f6dcb0")
    sc.add("city", doc(city), z=3.1, wc=0.6)

    # the plain in front of the wall: fields, road, pasture
    pl = f'<rect x="-40" y="{WALL_Y - 40}" width="2560" height="{SH - WALL_Y + 120}" fill="url(#plain)"/>'
    # the plain fades into the pale desert east of the city (behind the knoll) instead of ending at an edge
    pl += (f'<rect x="2150" y="{WALL_Y - 40}" width="{SW - 2050}" height="{SH - WALL_Y + 120}" fill="url(#plainfade)"/>')
    rng = np.random.default_rng(7)
    # far fields (strips) near the wall
    field_cols = ["#c9cc7e", "#e6cf88", "#b5c271", "#dcc47c", "#c3cf86"]
    xs = [-60, 260, 560, 900, 1180, 1560, 1860, 2140, 2420]
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        y0, y1 = WALL_Y + 8, WALL_Y + 60 + 20 * (i % 3)
        col = field_cols[i % len(field_cols)]
        d = f"M{x0 + 6},{y0} L{x1 - 6},{y0} L{x1 + 10},{y1} L{x0 - 4},{y1} Z"
        pl += f'<path d="{d}" fill="{col}" stroke="{P["ink"]}" stroke-width="2.5" stroke-linejoin="round" opacity="0.95"/>'
        for k in range(4):     # furrows
            yy = y0 + (y1 - y0) * (k + 1) / 5
            pl += (f'<line x1="{x0 + 8}" y1="{yy:.0f}" x2="{x1 - 4}" y2="{yy:.0f}" stroke="{S.shade(col, -0.18)}" '
                   f'stroke-width="2" opacity="0.7"/>')
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
    # warm late-afternoon light pooled over the plain (baked in: a dynamic glow cost ~37 ms/frame)
    pl += '<ellipse cx="1150" cy="1080" rx="1350" ry="560" fill="url(#cg)"/>'
    plain_defs = (S.lin_grad("plain", [(0, "#e4cf8c"), (0.25, "#d4cd84"), (1, "#b3bf6b")]) +
                  S.lin_grad("plainfade", [(0, "#ecd3a0", 0), (0.2, "#ecd3a0", 1), (1, "#ecd3a0", 1)], x2=1, y2=0) +
                  S.lin_grad("past", [(0, "#b0cb6c"), (0.5, "#9dbf60"), (1, "#8ab156")]) +
                  S.rad_grad("cg", [(0, "#fff0c0", 0.32), (0.55, "#ffe6a8", 0.14), (1, "#ffe0a0", 0)]))
    sc.add("plain", doc(S.g(pl, filter="wobble"), plain_defs), z=4, wc=0.8)

    # city wall with the open gate (in front of the skyline)
    wall = PR.city_wall(-60, 2320, WALL_Y, height=170, gate=(GATE_X, 140), doors_open=1.0, seed=2, ink=0.7)
    wall += _end_tower(2320, WALL_Y, 170 / 260)
    sc.add("wall", doc(wall), z=4.1, wc=0.7)

    # trees, bushes, the well (static)
    mid = ""
    for (x, y, s, ln) in [(120, 812, 0.4, -0.1), (470, 806, 0.36, 0.15), (1060, 812, 0.34, 0.1),
                          (1700, 810, 0.38, -0.12), (2050, 818, 0.42, 0.1), (2240, 830, 0.34, -0.2)]:
        mid += PR.palm_tree(x, y, s, lean=ln)
    for (x, y, s, sd) in [(760, 860, 0.32, 1), (1880, 880, 0.34, 2)]:
        mid += PR.olive_tree(x, y, s, seed=sd)
    for (x, y, s, v) in [(30, 960, 0.5, 0), (300, 905, 0.4, 1), (1700, 965, 0.42, 3), (2330, 1010, 0.5, 0),
                         (1200, 990, 0.4, 1), (60, 1300, 0.7, 1)]:
        mid += PR.bush(x, y, s, variant=v)
    mid += _well(470, 1040, 0.62)
    sc.add("mid", doc(mid), z=4.2, wc=0.8)

    # Jonah's knoll (dry, sandy) with the slope down into the plain
    kd = S.smooth_path(KNOLL, closed=False) + f" L{SW + 80},{SH + 80} L{KNOLL[0][0]},{SH + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4.5)
    # sunlit rim just under the crest (the low sun is in the west, on the left)
    rp = [(x + 12, y + 18) for x, y in KNOLL[2:]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f7dfaa" stroke-width="18" opacity="0.6"/>'
    # a lower, darker sand terrace in front (depth)
    terr = [(2180, 1520), (2450, 1330), (2800, 1250), (3200, 1215), (3550, 1190), (3900, 1170)]
    knoll += S.path(S.smooth_path(terr, closed=False) + f" L3900,{SH + 80} L2150,{SH + 80} Z", fill="url(#kn2)", sw=4)
    knoll += (f'<path d="{S.smooth_path([(x + 10, y + 16) for x, y in terr[1:]], closed=False)}" fill="none" '
              f'stroke="#ecc98e" stroke-width="12" opacity="0.5"/>')
    # the footpath Jonah climbed up from the city
    fp = S.smooth_path([(2330, SH + 60), (2420, 1450), (2560, 1300), (2700, 1180), (2760, 1050), (2700, 930),
                        (2760, 862), (2800, 858), (2790, 935), (2840, 1050), (2790, 1190), (2650, 1320),
                        (2540, 1460), (2480, SH + 60)], closed=True, tension=0.8)
    knoll += f'<path d="{fp}" fill="#f2d9a6" opacity="0.85"/>'
    # soft strata strokes and wind ripples
    for (x, y, w_) in [(2900, 960, 200), (3300, 900, 240), (3600, 1000, 180), (3050, 1110, 220), (2600, 1050, 120),
                       (3400, 1090, 200), (2950, 1350, 260), (3500, 1330, 220), (2500, 1180, 110), (3200, 1500, 260)]:
        knoll += (f'<path d="M{x - w_ / 2},{y} q{w_ / 2},-16 {w_},0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.42" stroke-linecap="round"/>')
    for (x, y, r) in [(2660, 852, 9), (3180, 846, 8), (3220, 852, 6), (3560, 842, 9), (2540, 935, 7), (2470, 1010, 8),
                      (2380, 1150, 9), (2960, 1240, 8), (3380, 1265, 7)]:
        knoll += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4}" ry="{r}" fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="3"/>'
    knoll += _rock(2330, 1260, 130, 58, seed=43, sw=4) + _rock(3540, 1010, 110, 50, seed=44, sw=4)
    knoll += PR.bush(2560, 1120, 0.6, variant=2) + PR.bush(3700, 900, 0.7, variant=2) + PR.bush(3080, 1235, 0.75, variant=2)
    for (x, y, s_) in [(2600, 880, 0.7), (3150, 845, 0.6), (2430, 1080, 0.75), (3330, 1000, 0.7), (2880, 1200, 0.8),
                       (3700, 1180, 0.9)]:
        knoll += PR.grass_tuft(x, y, s_, variant=1)
    sc.add("knoll", doc(S.g(knoll, filter="wobble"),
                        S.lin_grad("kn", [(0, "#ebc68a"), (0.3, "#e2b679"), (1, "#d09c62")]) +
                        S.lin_grad("kn2", [(0, "#ddaa6c"), (1, "#c58f58")])), z=5, wc=0.9)

    # booth (behind the plant) + soft shadow — same drawing as s11
    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{P["ink"]}" opacity="0.16" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    # Jonah's few belongings in the booth: a water jar and a sack
    booth += PR.sack(XB - 30, GY + 2, 0.62, seed=3) + PR.jar(XB + 95, GY - 50, 0.6)
    sc.add("booth", doc(booth), z=5.6, wc=0.8)     # in front of the clouds and doves

    # =============================================================== PEOPLE on the plain
    def person(name, x, y, kind, variant, pose="stand", facing=1, expr="happy", z=None, motion=None, frames=None,
               frame_at=None, s=None):
        s = s or plain_scale(y)
        shadow = CH.ground_shadow(x, y, s, width=90 if kind == "child" else 120, opacity=0.2)
        if frames is None:
            svg = doc(shadow + CH.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, expr=expr))
        else:
            svg = [doc(shadow + CH.citizen(x, y, s, facing, kind=kind, variant=variant, pose=p, expr=e))
                   for p, e in frames]
        sc.add(name, svg, z=z if z is not None else 6 + y / 1000, wc=0.6, motion=motion, frame_at=frame_at)
        return s

    def breathe(x, y, ph, amt=0.012, per=2.8):
        return M.breathe(amt, per, pivot=(x, y), phase=ph)

    def nod(x, y, ph, deg=1.2, per=2.6):
        return M.sway(deg, per, pivot=(x, y), phase=ph)

    # elders by the well (left)
    person("elder0", 330, 1010, "elder", 0, "stand", 1, "happy", motion=M.combine(nod(330, 1010, 0.1), breathe(330, 1010, 0.3)))
    person("elder1", 600, 985, "elder", 1, "stand", -1, "peaceful", motion=M.combine(nod(600, 985, 0.6, 1.0, 3.1),
                                                                                    breathe(600, 985, 0.7)))
    # mothers with children
    person("mother0", 700, 1070, "woman", 1, "stand", 1, "happy", motion=M.combine(nod(700, 1070, 0.2, 1.5, 3.0),
                                                                                  breathe(700, 1070, 0.1)))
    person("girl0", 785, 1090, "child", 1, "stand", -1, "happy", motion=M.combine(M.bob(3, 1.3, 0.2),
                                                                                  breathe(785, 1090, 0.5)))
    person("mother1", 1560, 925, "woman", 3, "stand", -1, "happy", motion=M.combine(nod(1560, 925, 0.4, 1.2, 2.7),
                                                                                    breathe(1560, 925, 0.9)))

    # a family in front: grandfather, mother and a toddler hopping with joy
    person("grandpa", 165, 1300, "elder", 2, "stand", 1, "happy", motion=M.combine(nod(165, 1300, 0.15, 1.2, 2.8),
                                                                                    breathe(165, 1300, 0.4)))
    person("mother2", 300, 1330, "woman", 2, "stand", 1, "happy", motion=M.combine(nod(300, 1330, 0.55, 1.4, 3.2),
                                                                                    breathe(300, 1330, 0.2)))

    # children playing ball (jump: stand <-> cheer)
    def hop(x, y, per, ph, h=26):
        def m(t):
            u = (t / per + ph) % 1.0
            dy = -h * math.sin(math.pi * u / 0.5) if u < 0.5 else 0.0
            sq = 1.0
            if 0.5 <= u < 0.62:
                sq = 1 - 0.05 * math.sin(math.pi * (u - 0.5) / 0.12)
            return Tf(dy=dy, sx=1 / sq ** 0.5, sy=sq, px=x, py=y)
        return m

    def hop_frame(per, ph):
        return lambda t: 1.0 if ((t / per + ph) % 1.0) < 0.5 else 0.0

    kids = [("kid0", 930, 1200, 0, 1, 1.25, 0.0), ("kid1", 1190, 1215, 2, -1, 1.25, 0.5),
            ("kid2", 1060, 1150, 3, 1, 1.05, 0.25), ("kid3", 560, 1185, 1, 1, 1.4, 0.65),
            ("toddler", 395, 1350, 0, -1, 0.9, 0.1)]
    for (nm, x, y, v, fc, per, ph) in kids:
        person(nm, x, y, "child", v, facing=fc, frames=[("stand", "happy"), ("cheer", "happy")],
               frame_at=hop_frame(per, ph), motion=hop(x, y, per, ph, {"kid3": 18, "toddler": 14}.get(nm, 24)),
               s=0.56 if nm == "toddler" else None)

    # the ball tossed between kid0 and kid1
    ball_svg = doc(S.g(f'<circle cx="1060" cy="900" r="15" fill="#e2683f" stroke="{P["ink"]}" stroke-width="3.5"/>'
                       f'<path d="M1046,895 Q1060,884 1074,895" fill="none" stroke="#f6d36a" stroke-width="4"/>'
                       f'<path d="M1048,908 Q1060,916 1072,906" fill="none" stroke="#3b8b89" stroke-width="4"/>',
                       filter="wobble-fine"))
    xa, ya = 930 + 40, 1200 - 0.6 * 224 * plain_scale(1200) - 34
    xb, yb = 1190 - 40, 1215 - 0.6 * 224 * plain_scale(1215) - 34

    def ball(t):
        per = 1.25
        u = (t / per) % 2.0
        if u < 1:
            x0, y0, x1, y1, v = xa, ya, xb, yb, u
        else:
            x0, y0, x1, y1, v = xb, yb, xa, ya, u - 1
        x = x0 + (x1 - x0) * v
        y = y0 + (y1 - y0) * v - 150 * 4 * v * (1 - v)
        return Tf(dx=x - 1060, dy=y - 900, rot=360 * v)
    sc.add("ball", ball_svg, z=7.5, wc=0.4, motion=lambda t: (lambda b: Tf(dx=b.dx, dy=b.dy, rot=b.rot,
                                                                           px=1060, py=900))(ball(t)))

    # men and women near the gate (far, small)
    person("man0", GATE_X - 120, 835, "man", 0, "stand", 1, "happy", motion=breathe(GATE_X - 120, 835, 0.2))
    person("woman0", GATE_X + 110, 840, "woman", 0, "stand", -1, "happy", motion=breathe(GATE_X + 110, 840, 0.6))
    person("man1", GATE_X + 200, 850, "man", 2, "cheer", -1, "happy",
           motion=M.combine(nod(GATE_X + 200, 850, 0.3, 2.0, 1.6), breathe(GATE_X + 200, 850, 0.1)))
    person("child_g", GATE_X + 30, 860, "child", 2, "stand", 1, "happy", motion=M.bob(3, 0.9, 0.3))
    person("man2", 230, 870, "man", 1, "stand", 1, "happy", motion=breathe(230, 870, 0.4))
    person("woman1", 940, 880, "woman", 2, "cheer", 1, "happy",
           motion=M.combine(nod(940, 880, 0.1, 2.0, 1.8), breathe(940, 880, 0.3)))

    # =============================================================== ANIMALS in the pasture
    def beast(name, x, y, kind, facing, s, motion=None, z=None):
        shadow = CH.ground_shadow(x, y, s, width=230 if kind in ("cow", "donkey") else 190, opacity=0.2)
        sc.add(name, doc(shadow + PR.animal(x, y, s, facing, kind=kind)), z=z if z is not None else 6 + y / 1000,
               wc=0.6, motion=motion)

    sheep = [(1375, 1240, 1, 0.6), (1580, 1300, -1, 0.62), (1720, 1235, -1, 0.58), (1470, 1390, 1, 0.66),
             (1800, 1350, -1, 0.64)]
    for i, (x, y, fc, s) in enumerate(sheep):
        mot = M.combine(M.bob(2.5, 2.2 + 0.3 * i, i * 0.27), nod(x, y, i * 0.31, 1.2, 2.9))
        if i == 1:     # the one who bleats: a happy little hop
            mot = M.combine(mot, M.keys([(t_baa - 0.12, {"dy": 0}), (t_baa + 0.05, {"dy": -16}),
                                         (t_baa + 0.25, {"dy": 0})], ["out", "in"]))
        beast(f"sheep{i}", x, y, "sheep", fc, s, mot)
    # lambs frolic
    for i, (x, y, fc) in enumerate([(1650, 1410, -1), (1930, 1420, 1)]):
        beast(f"lamb{i}", x, y, "sheep", fc, 0.4, hop(x, y, 0.95 + 0.2 * i, 0.3 * i, 20))
    beast("goat0", 1950, 1180, "goat", -1, 0.55, M.combine(nod(1950, 1180, 0.2, 1.8, 2.3), M.bob(2, 2.0, 0.1)))
    beast("goat1", 2080, 1290, "goat", -1, 0.6, M.combine(nod(2080, 1290, 0.7, 1.5, 2.6), M.bob(2, 2.4, 0.4)))
    beast("cow0", 1560, 1090, "cow", 1, 0.52, M.combine(nod(1560, 1090, 0.5, 0.8, 3.6), breathe(1560, 1090, 0.2)))
    beast("cow1", 1240, 1450, "cow", 1, 0.68, M.combine(nod(1240, 1450, 0.1, 0.8, 3.9), breathe(1240, 1450, 0.6)))
    beast("donkey0", 2120, 1110, "donkey", -1, 0.5, M.combine(nod(2120, 1110, 0.4, 1.4, 3.0), breathe(2120, 1110, 0.3)))
    beast("donkey1", 1330, 1120, "donkey", 1, 0.5, M.combine(nod(1330, 1120, 0.8, 1.2, 3.3), breathe(1330, 1120, 0.5)))
    # a shepherd boy cheering among the flock
    person("shepherd", 2010, 1410, "child", 0, facing=-1, frames=[("stand", "happy"), ("cheer", "happy")],
           frame_at=hop_frame(1.6, 0.2), motion=hop(2010, 1410, 1.6, 0.2, 14), s=0.6)

    # baa arcs
    bx, by = 1580 - 0.62 * 112, 1300 - 0.62 * 100
    sc.add("baa", doc(_baa(bx, by, 0.9)), z=9, wc=0.3, motion=lambda t: Tf(
        alpha=_env(t, t_baa - 0.05, t_baa + 0.1, t_baa + 0.7, t_baa + 1.0),
        sx=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"),
        sy=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"), px=bx, py=by))

    # =============================================================== WITHERED PLANT + JONAH
    plant = doc(PR.castor_plant(XP, GY, SP, growth=1, wither=1, bite=1, side=1, seed=2))
    sc.add("castor", plant, z=10, wc=0.9, motion=lambda t: Tf(
        rot=0.6 * math.sin(2 * math.pi * t / 3.6) + 0.25 * math.sin(2 * math.pi * t / 1.7), px=XP, py=GY))

    # God's golden light on Jonah (lines 0-1), drawn behind him
    a_light = lambda t: _env(t, t_light0, t_light0 + 1.2, t_pan0 + 0.6, t_pan1 - 0.4)
    GAP = (XJ + 55, 250)       # where the clouds part
    beam = doc(
        S.g(f'<path d="M{GAP[0] - 150},{GAP[1]} L{GAP[0] + 150},{GAP[1]} L{XJ + 330},{GY + 30} L{XJ - 330},{GY + 30} Z" '
            f'fill="url(#bm)"/>', filter="blur-md") +
        f'<ellipse cx="{XJ - 10}" cy="{GY - 150}" rx="360" ry="300" fill="url(#jg)"/>',
        S.lin_grad("bm", [(0, "#ffe6a8", 0.22), (0.6, "#ffdc96", 0.12), (1, "#ffd68a", 0.05)]) +
        S.rad_grad("jg", [(0, "#ffe2a0", 0.28), (0.5, "#ffd890", 0.11), (1, "#ffd080", 0)]))
    a_end = lambda t: 0.55 * M.progress(t, t_peace - 0.2, t_peace + 1.2, "sine")
    sc.add("god_light", beam, z=10.5, wc=0, blend="add",
           motion=lambda t: Tf(alpha=max(a_light(t), a_end(t)) * (0.85 + 0.15 * math.sin(t * 2.6))))
    rays = doc(S.g(_ray_fan(GAP[0], GAP[1] - 40, 760, [64, 74, 83, 91, 99, 108, 118], w0=8, w1=46,
                            fill="#ffe2a0", opacity=0.3), filter="soft"))
    sc.add("rays", rays, z=10.6, wc=0, blend="add", motion=lambda t: Tf(
        alpha=a_light(t) * (0.75 + 0.25 * math.sin(t * 1.9)),
        rot=2.0 * math.sin(t * 0.45), px=GAP[0], py=GAP[1] - 40))

    # Jonah: sad -> thoughtful (sorry) -> looking at the city (neutral) -> peaceful
    exprs = ["sad", "sorry", "neutral", "peaceful"]
    jshadow = CH.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)
    jframes = [doc(jshadow + CH.jonah(XJ, GY, SP, -1, pose="sit", expr=e)) for e in exprs]
    switch = [(t_thought, 0.25), (t_look, 0.25), (t_peace, 0.35)]

    def jonah_frame(t):
        f = 0.0
        for i, (ts, d) in enumerate(switch):
            if t >= ts:
                f = i + M.progress(t, ts, ts + d, "sine")
        return f

    def jonah_tf(t):
        s = 1 + 0.011 * math.sin(2 * math.pi * t / 3.2)
        dy = 0.0
        rot = 0.0
        # hears his name: a small lift
        u = t - l0.start
        if 0 <= u < 1.2:
            dy -= 5 * math.sin(math.pi * u / 1.2)
        # thoughtful sigh
        u = t - t_thought
        if 0 <= u < 1.4:
            s *= 1 - 0.012 * math.sin(math.pi * u / 1.4)
            rot -= 1.2 * math.sin(math.pi * u / 1.4)
        # peaceful: a slow, deep, relaxed breath
        k = M.progress(t, t_peace - 0.1, t_peace + 0.8, "sine")
        s *= 1 + k * 0.01 * math.sin(2 * math.pi * (t - t_peace) / 2.4)
        return Tf(dy=dy, rot=rot, sx=s, sy=s, px=XJ, py=GY)

    sc.add("jonah", jframes, z=11, frame_at=jonah_frame, motion=jonah_tf, wc=0.6)

    # the dry leaf in Jonah's near hand
    hand = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit")["hands"][1]
    lcx, lcy = hand[0] - 58, hand[1] - 62
    leaf = doc(_dry_leaf(lcx, lcy, 50, rot=-30, stalk=(hand[0] - 2, hand[1] + 4)))

    def leaf_tf(t):
        j = jonah_tf(t)
        # where Jonah's breathing / lift carries the hand
        hx = XJ + (hand[0] - XJ) * j.sx
        hy = GY + (hand[1] - GY) * j.sy + j.dy
        lift = M.progress(t, t_thought - 0.1, t_thought + 0.7, "inout") * (1 - M.progress(t, t_look, t_look + 0.6))
        twirl = 4 * math.sin(2 * math.pi * t / 2.2) * _env(t, l0.start + 0.6, l0.start + 1.2, l1.end, l1.end + 0.6)
        rot = -14 * lift + twirl + 1.5 * math.sin(2 * math.pi * t / 1.3)
        return Tf(dx=hx - hand[0], dy=hy - hand[1] - 6 * lift, rot=rot, sx=j.sx, sy=j.sy, px=hand[0], py=hand[1])

    sc.add("leaf", leaf, z=11.2, wc=0.5, motion=leaf_tf)

    # a dead leaf flutters down from the plant and settles by Jonah's feet
    fl0 = (XB - 150, GY - 400)  # from the dead canopy over the booth...
    fl1 = (XB - 230, GY + 14)   # ...it lands flat in front of the booth (never crossing Jonah)
    fleaf = doc(_dry_leaf(fl0[0], fl0[1], 40, rot=20, col="#cfa95e"))     # lighter straw colour: reads on the canopy

    def fleaf_tf(t):
        u = M.progress(t, t_leaf_fall, t_leaf_fall + 3.2, "linear")
        if t < t_leaf_fall:
            return Tf(alpha=0.0)
        e = 1 - (1 - u) ** 1.4
        x = fl0[0] + (fl1[0] - fl0[0]) * e + 60 * math.sin(2 * math.pi * u * 1.6) * (1 - u)
        y = fl0[1] + (fl1[1] - fl0[1]) * u
        rot = 50 * math.sin(2 * math.pi * u * 1.6) * (1 - u) - 8 * u
        flip = abs(math.cos(math.pi * u * 2.6))          # tumbling (seen edge-on now and then)
        sy = (0.3 + 0.7 * flip) * (1 - u) + 0.5 * u     # ends lying flat
        a = M.progress(t, t_leaf_fall, t_leaf_fall + 0.25)
        return Tf(dx=x - fl0[0], dy=y - fl0[1], rot=rot, sx=1 - 0.1 * u, sy=sy, alpha=a,
                  px=fl0[0], py=fl0[1])

    sc.add("fall_leaf", fleaf, z=11.1, wc=0.5, motion=fleaf_tf)

    # =============================================================== DOVES gliding home toward the city
    def flock(name, birds, t0, t1, dx, dy, z):
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
                                M.bob(6, 0.9), lambda t: Tf(alpha=_env(t, t0, t0 + 0.4, t1 - 0.4, t1))))

    flock("doves_a", [(3700, 330, 0.42), (3790, 296, 0.36), (3830, 360, 0.34)], -0.5, l1.end + 0.3, -1150, 30, 5.4)
    flock("doves_b", [(3250, 330, 0.42), (3340, 290, 0.36), (3390, 365, 0.34)], l3.start + 2.0, T + 2.5, -760, -30,
          5.45)

    # =============================================================== FOREGROUND (static)
    fg = ""
    for (x, y, s, v) in [(3560, 1120, 1.2, 1), (3720, 1090, 1.0, 1), (2620, 1300, 1.0, 1), (3150, 1400, 1.1, 1), (2990, 1190, 0.9, 2), (3300, 1250, 0.8, 1),
                         (3250, 1262, 0.7, 2)]:
        fg += PR.grass_tuft(x, y, s, variant=v)
    fg += _rock(3420, 1160, 220, 96, seed=51) + _rock(3700, 1385, 260, 120, seed=52)
    sc.add("fg", doc(S.g(fg)), z=20, wc=0.9)

    # =============================================================== CAMERA
    C0 = Cam(2930, 640, 1460)        # Jonah close
    C0b = Cam(2905, 655, 1360)       # slow push-in while God speaks
    C1 = Cam(950, 1005, 1660)        # the people
    C1b = Cam(1030, 1000, 1610)
    C2 = Cam(1740, 1150, 1600)       # the animals
    C2b = Cam(1785, 1140, 1560)
    C3 = Cam(2600, 705, 1880)        # back to Jonah, the plain below him
    C3b = Cam(2610, 700, 1840)

    def lerp_cam(a, b, u, bump=0.0, ub=None):
        ub = u if ub is None else ub
        return Cam(M.lerp(a.x, b.x, u), M.lerp(a.y, b.y, u), M.lerp(a.w, b.w, u) + bump * math.sin(math.pi * ub))

    def camera(t):
        if t < t_pan0:
            return lerp_cam(C0, C0b, M.progress(t, 0, t_pan0, "sine"))
        if t < t_pan1:      # sweep out over the whole city, then settle on the people
            u = M.progress(t, t_pan0, t_pan1, "inout")
            return lerp_cam(C0b, C1, u, bump=900)
        if t < t_pan2:
            return lerp_cam(C1, C1b, M.progress(t, t_pan1, t_pan2, "sine"))
        if t < t_pan3:
            return lerp_cam(C1b, C2, M.progress(t, t_pan2, t_pan3, "inout"), bump=120)
        if t < t_back0:
            return lerp_cam(C2, C2b, M.progress(t, t_pan3, t_back0, "sine"))
        if t < t_back1:
            u = M.progress(t, t_back0, t_back1, "inout")
            return lerp_cam(C2b, C3, u, bump=200)
        return lerp_cam(C3, C3b, M.progress(t, t_back1, T, "sine"))

    sc.camera = camera

    # =============================================================== FX
    sc.fx = [
        FX.sparkles((XJ - 330, GY - 520, XJ + 260, GY - 40), count=22, t0=t_light0 + 0.3, t1=t_pan1 - 0.6,
                    color=(255, 238, 175), size=(9, 20), drift=-10, seed=21),
        FX.motes((XJ - 500, 0, XJ + 400, GY), count=30, t0=t_light0, t1=t_pan1, color=(255, 244, 205), seed=22),
        FX.sparkles((200, 700, 2300, 1150), count=34, t0=t_city0 + 0.4, t1=T + 1, color=(255, 238, 175),
                    size=(8, 18), drift=-8, seed=23),
        hearts_fx([(330, 830, 20), (600, 812, 20), (700, 880, 20), (790, 950, 12), (930, 1025, 20),
                   (1190, 1035, 20), (545, 1035, 8), (1060, 985, 20), (1260, 688, 15), (1490, 698, 15),
                   (1580, 700, 15), (940, 728, 15), (230, 712, 15), (1560, 768, 12), (165, 1075, 15), (300, 1095, 15),
                   (395, 1205, 10)],
                  t_hearts_p, t_pan2 + 0.6, rise=130, period=2.6, seed=31),
        hearts_fx([(1590, 955, 25), (1365, 1138, 20), (1610, 1195, 12), (1740, 1140, 20), (1830, 1258, 20),
                   (1975, 1020, 15), (2100, 1120, 12), (2130, 938, 15), (1310, 948, 15), (1220, 1280, 20),
                   (1650, 1352, 10), (1930, 1362, 10), (2010, 1255, 12)],
                  t_hearts_a, T + 1, rise=120, size=36, period=2.6, seed=32),
        FX.sparkles((XJ - 300, GY - 420, XJ + 200, GY - 60), count=16, t0=t_peace, t1=T + 1, color=(255, 240, 190),
                    size=(8, 16), drift=-6, seed=24),
    ]

    # =============================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("birds", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8, pan=-0.2)
    sc.sfx("sheep", t_baa, gain_db=-11, pan=-0.3)
    sc.sfx("chime", t_chime, gain_db=-10)
    return sc
