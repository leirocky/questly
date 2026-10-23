"""Scene 1 - title page: the little cave-stable of Bethlehem on its hill under a deep-blue starry sky; one big golden
star shines a soft beam down on it; warm lamplight glows in the doorway; sheep rest on the hillside in front; the
lights of the little town glimmer on the far ridge. Book title.

Beats (keyed to ctx.lines[0] '圣经绘本：耶稣降生。'; phrase / syllable onsets are measured in the voice clip with the
Noah film's voice_marks helpers (fallback: proportions of the subtitle chunk), so a re-generated voice stays in sync):
  start        calm frame (the film fades in over it): stars twinkle, the great star breathes, the lamp flickers,
               the grass stirs, the sheep breathe
  ~1.1 s       the near sleeping sheep lifts its head and looks about (squash-dip hides the pose cut; a soft bleat)
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime)
  '耶稣降生'    the four title characters pop in one by one on their syllables (pop); the star's beam brightens
  end          calm hold with a slow push-in. s02_question follows with a plain 1 s cross-dissolve into the warm
               living room (a different place): the stable's warm doorway sits where s02's tree glows, so the
               dissolve passes warm light into warm light.

Shared helpers for this illustrator's other scenes (s02_question, s06_birth, s12_end): Fig (one figure on its own
flipbook layer with hard cuts and its own motions), beat / keyed / dip / hop / breath / arc_jump, Twinkle (star
twinkles in output space, optionally flaring on given times), glow_svg.
"""
import math
import random

from PIL import Image, ImageDraw

from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, IDENTITY
from engine.paths import FPS, load_story
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, f1, heart_markup, snap, title_char_svg, voice_marks  # noqa: F401

INK = P["ink"]
CREAM = "#fff6e3"

HILL_Y = 1010                          # night_hills near ground line
STAB = (1400, 935, 0.44)               # the stable: doorway floor (x, y), scale
STAR = (1400, 186, 0.6)                # the great star (centre, scale)
STAR_BEAM_TO = (1400, 478)             # the beam lands on the stable's hill top
RIB = (610, 170)                       # ribbon centre
TITLE_X, TITLE_Y, TITLE_SIZE, TITLE_STEP = 610, 418, 168, 196
TITLE_COLS = ("#fff3c4", "#f7c95a", "#e0913a")


# ================================================================== shared helpers

def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


def gframe(ctx, t):
    """Film frame index of scene time t."""
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
    """Onset (scene s) of the k-th occurrence of ``phrase`` in line li, from the voice-measured phrase marks (character
    offset inside the phrase); fallback: the subtitle chunk that contains it."""
    n = 0
    try:
        for ent in voice_marks(ctx, li):
            pos = ent[0].find(phrase)
            while pos >= 0:
                if n == k:
                    return char_times(ent)[pos]
                n += 1
                pos = ent[0].find(phrase, pos + 1)
    except Exception:                                    # noqa: BLE001 - fall back to the subtitle chunks
        pass
    return ctx.lines[li].at(phrase)


def phrase_end(ctx, li, phrase):
    for ent in voice_marks(ctx, li):
        if phrase in ent[0]:
            return ent[2]
    return ctx.lines[li].end


def hop(t0, keys, curves="sine"):
    return M.keys([(t0 + dt, d) for dt, d in keys], curves)


def dip(t0, depth=8.0, squash=0.95):
    """Squash-dip (depth in stage px) whose bottom is at t0 (a pose cut hides there)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth, "sy": squash}),
                    (0.13, {"dy": -0.35 * depth, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], ["in", "out", "sine"])


def breath(ctx, amount=0.008, period=3.2, phase=0.0):
    """Breathing (a small vertical stretch at the feet), keyed to film time."""
    return lambda t: Tf(sy=1 + amount * math.sin(2 * math.pi * (gtime(ctx, t) / period + phase)))


def arc_jump(t0, t1, dx, dy, height):
    """A hop from the foot point to (dx, dy) (stage px) between t0 and t1 along a parabola ``height`` px high,
    with a crouch before take-off and a squash on landing."""
    def m(t):
        if t <= t0 - 0.12:
            return IDENTITY
        if t < t0:                                      # crouch
            u = M.progress(t, t0 - 0.12, t0, "sine")
            return Tf(dy=6 * u, sy=1 - 0.05 * u)
        if t < t1:
            u = (t - t0) / (t1 - t0)
            e = M.ease("sine")(u)
            return Tf(dx=dx * e, dy=dy * e - height * 4 * u * (1 - u), sy=1.03 - 0.03 * abs(2 * u - 1))
        u = t - t1
        if u < 0.26:                                    # land
            k = math.sin(math.pi * u / 0.26)
            return Tf(dx=dx, dy=dy + 6 * k, sy=1 - 0.05 * k)
        return Tf(dx=dx, dy=dy)
    return m


def glow_svg(cx, cy, rx, ry, gid, c0="#fff4d0", c1="#ffd986", a0=0.9, a1=0.38):
    defs = S.rad_grad(gid, [(0, c0, a0), (0.45, c1, a1), (1, c1, 0)])
    return doc(f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>', defs)


def flicker(t, seed=0.0):
    """A lamp-flame flicker in 0..1 (smooth, irregular)."""
    return (0.5 + 0.22 * math.sin(2 * math.pi * (t * 1.7 + seed)) + 0.16 * math.sin(2 * math.pi * (t * 3.9 + 0.3 + seed))
            + 0.12 * math.sin(2 * math.pi * (t * 7.3 + 0.7 + 2 * seed)))


class Fig:
    """One figure (or prop) on its own flipbook layer: hard cuts between drawings (at()), film-time keyed cycles
    (cycle()), its own motions (move(); pivot at the foot point)."""

    def __init__(self, ctx, name, foot, z, seed=None):
        self.ctx, self.name, self.foot, self.z = ctx, name, foot, z
        self.seed = seed
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
        ids, step, off = seg[1], seg[2], seg[3]
        return float(ids[(gframe(self.ctx, t) // step + off) % len(ids)])

    def add(self, sc, wc=1.0, docs=True):
        self.segs.sort(key=lambda s: s[0])
        own = M.combine(*self.motions) if self.motions else None
        frames = [S.svg_doc(b, "", sc.W, sc.H) if docs else b for b in self.bodies]
        mot = M.with_pivot(own, self.foot) if own else None
        sc.add(self.name, frames, z=self.z, motion=mot, frame_at=self.frame_at if len(frames) > 1 else None, wc=wc,
               seed=self.seed)
        return self


class Twinkle:
    """Star twinkles drawn in output space: four-pointed sparkles at stage points [(x, y, r)] that breathe slowly and
    flare (bigger, brighter) at the given times. alpha_fn(t) scales them all (e.g. 0 while the sky is out of view).
    Put the stars only where open sky shows (fx draw over every layer)."""

    def __init__(self, stars, flares=(), alpha_fn=None, color=(255, 246, 214), seed=5, base=0.55, period=(1.6, 3.4)):
        rng = random.Random(seed)
        self.stars = [(x, y, r, rng.random(), rng.uniform(*period)) for x, y, r in stars]
        self.flares = list(flares)             # (t, amp, set of star indices or None = all)
        self.alpha_fn = alpha_fn or (lambda t: 1.0)
        self.color, self.base = color, base

    def flare(self, i, t):
        k = 0.0
        for tf, amp, who in self.flares:
            if who is not None and i not in who:
                continue
            u = t - tf
            if -0.08 < u < 0.9:
                k = max(k, amp * (1 - math.exp(-(u + 0.08) / 0.03)) * math.exp(-max(0.0, u) / 0.22))
        return k

    def __call__(self, frame, t, view):
        a0 = self.alpha_fn(t)
        if a0 <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i, (x, y, r, ph, per) in enumerate(self.stars):
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t / per + ph))
            fl = self.flare(i, t)
            k = self.base * tw + fl
            if k < 0.08:
                continue
            ox, oy = view.to_out(x, y)
            if not (-60 < ox < frame.size[0] + 60 and -60 < oy < frame.size[1] + 60):
                continue
            rr = r * view.scale * (0.55 + 0.45 * tw + 1.3 * fl)
            a = int(255 * a0 * min(1.0, k))
            w = rr * 0.2
            g = rr * 0.7
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*self.color, a // 5))
            d.polygon([(ox, oy - rr), (ox + w, oy - w), (ox + rr, oy), (ox + w, oy + w), (ox, oy + rr),
                       (ox - w, oy + w), (ox - rr, oy), (ox - w, oy - w)], fill=(*self.color, a))
            c = max(1.5, rr * 0.16)
            d.ellipse([ox - c, oy - c, ox + c, oy + c], fill=(255, 253, 242, a))
        frame.alpha_composite(ov)
        return frame


def sky_stars(n, box, avoid, seed=1, r=(6, 13)):
    """n star points inside box (x0, y0, x1, y1), none inside the avoid test avoid(x, y) -> bool."""
    rng = random.Random(seed)
    out = []
    tries = 0
    while len(out) < n and tries < n * 60:
        tries += 1
        x, y = rng.uniform(box[0], box[2]), rng.uniform(box[1], box[3])
        if avoid(x, y) or any((x - a) ** 2 + (y - b) ** 2 < 70 ** 2 for a, b, _ in out):
            continue
        out.append((x, y, rng.uniform(*r)))
    return out


def ribbon_svg(text, cx, cy, hw=430, h=80, band_col="#a8433f", size=44):
    """The ribbon header (story.SUBTITLE) in this film's colours: a warm red band with gold stitching."""
    tail_col, fold_col = S.shade(band_col, -0.16), S.shade(band_col, -0.38)
    b = ""
    for sd in (-1, 1):
        ex = cx + sd * hw
        top, bot = cy - h / 2 + 26, cy + h / 2 + 26
        pts = [(ex - sd * 30, top), (ex + sd * 95, top), (ex + sd * 66, (top + bot) / 2), (ex + sd * 95, bot),
               (ex - sd * 30, bot)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z", fill=tail_col, sw=3.5)
        fold = [(ex, cy + h / 2 + 6), (ex - sd * 30, bot), (ex - sd * 30, cy + h / 2 + 6)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in fold) + " Z", fill=fold_col, sw=3)
    band = (f"M{cx - hw},{cy - h / 2 + 8} Q{cx},{cy - h / 2 - 12} {cx + hw},{cy - h / 2 + 8} "
            f"L{cx + hw},{cy + h / 2 + 6} Q{cx},{cy + h / 2 - 14} {cx - hw},{cy + h / 2 + 6} Z")
    b += S.path(band, fill=band_col, sw=3.5)
    for yy, q in ((cy - h / 2 + 18, cy - h / 2), (cy + h / 2 - 4, cy + h / 2 - 22)):
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#f2cf86" stroke-width="3" '
              f'fill="none" opacity="0.85" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="2">{text}</text>')
    return doc(body)


# ================================================================== drawings

def sky_svg():
    return doc(PR.starry_sky(-40, -40, W + 40, 1000, density=1.0, twinkle=0.15, milky_way=True, seed=31))


def hills_back_svg():
    return doc(PR.night_hills(-80, W + 80, HILL_Y, 1.0, part="back", fire_x=False, fold_x=False, town=True, seed=4))


def field_svg():
    return doc(PR.night_hills(-80, W + 80, HILL_Y, 1.0, part="front", fire_x=False, fold_x=False, town=True, seed=4,
                              bottom=H + 60))


def star_svg(k):
    x, y, s = STAR
    return doc(PR.the_star(x, y, s, intensity=1.0, pulse=k, rays=True, beam=0.0))


def beam_svg():
    x, y, s = STAR
    bx, by = STAR_BEAM_TO
    gid = "n1beam"
    w0, w1 = 22, 150
    poly = f"M{x - w0},{y} L{bx - w1},{by} L{bx + w1},{by} L{x + w0},{y} Z"
    defs = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="{y}" x2="{bx}" y2="{by}">'
            f'<stop offset="0" stop-color="{PR.STAR_CORE}" stop-opacity="0.7"/>'
            f'<stop offset="1" stop-color="{PR.STAR_GOLD}" stop-opacity="0.16"/></linearGradient>')
    body = f'<path d="{poly}" fill="url(#{gid})" filter="url(#soft)"/>'
    return doc(body, defs)


def hilltop_glow_svg():
    bx, by = STAR_BEAM_TO
    return glow_svg(bx, by + 30, 300, 120, "n1hg", "#fff6d8", "#ffe7a6", 0.55, 0.22)


def stable_svg(part):
    x, y, s = STAB
    return doc(PR.stable(x, y, s, 1, part=part, lamp=1.0, time="night"))


def animals_body(donkey_ear=0):
    """The ox and the donkey resting inside (traditional picture details), by the empty manger."""
    x, y, s = STAB
    pts = PR.stable_points(x, y, s)
    ox_x, ox_y = pts["ox"]
    dk_x, dk_y = pts["donkey"]
    a = s * 0.9
    return (PR.donkey(dk_x + 40 * s, dk_y, a, 1, pose="sleep" if donkey_ear == 0 else "lie", sacks=0) +
            PR.ox(ox_x, ox_y + 10 * s, a, -1, pose="lie"))


def path_svg():
    """A pale footpath from the stable's doorway down the hill toward us."""
    x, y, s = STAB
    d = (f"M{x - 120},{y + 22} C{x - 140},{y + 90} {x - 330},{y + 150} {x - 420},{H + 40} "
         f"L{x - 40},{H + 40} C{x - 60},{y + 150} {x + 40},{y + 90} {x + 60},{y + 22} Z")
    body = (f'<path d="{d}" fill="#6f7a6a" stroke="{INK}" stroke-width="3" stroke-linejoin="round" opacity="0.9"/>'
            f'<path d="M{x - 70},{y + 40} C{x - 120},{y + 130} {x - 220},{y + 170} {x - 240},{H + 40}" stroke="#8a927e" '
            f'stroke-width="10" fill="none" opacity="0.5" stroke-linecap="round"/>')
    rng = random.Random(3)
    for i in range(9):
        u = rng.random()
        px = x - 60 - 240 * u ** 1.4 + rng.uniform(-40, 40) * u
        py = y + 40 + (H - y) * u
        body += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(8 + 14 * u)}" ry="{f1(4 + 6 * u)}" fill="#59645a" '
                 f'stroke="{INK}" stroke-width="2"/>')
    return doc(S.g(body, filter="wobble"))


def stable_base_tufts():
    """Grass tufts along the foot of the stable's hill (blends it into the field)."""
    x, y, s = STAB
    rng = random.Random(8)
    b = ""
    for i in range(30):
        tx = x - 440 + i * 30 + rng.uniform(-8, 8)
        ty = y + 18 + rng.uniform(-4, 10)
        h = rng.uniform(14, 26)
        b += (f'<path d="M{f1(tx - 8)},{f1(ty)} l4,{f1(-h)} l4,{f1(h * 0.8)} l4,{f1(-h * 1.1)} l4,{f1(h)}" '
              f'stroke="#2f4a3a" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return doc(S.g(b, filter="wobble-fine"))


def lamp_glow_svg():
    lx, ly = PR.stable_points(*STAB)["lamp"]
    return glow_svg(lx, ly + 50, 230, 190, "n1lamp", "#fff1c6", "#ffcf70", 0.8, 0.35)


def door_spill_svg():
    x, y, s = STAB
    return glow_svg(x - 20, y + 30, 330, 46, "n1spill", "#ffe9b0", "#ffc860", 0.55, 0.25)


SHEEP = [  # x, y, scale, facing, pose (far to near)
    (1905, 972, 0.44, -1, "lie"),
    (2030, 990, 0.48, -1, "sleep"),
    (690, 986, 0.62, -1, "sleep"),
    (170, 1012, 0.76, 1, "lie"),
]
LIFT = (450, 1058, 0.84, 1)                    # the sheep that lifts its head
LAMB = (320, 1030, 0.7, -1)


def sheep_svg(i):
    x, y, s, f, pose = SHEEP[i]
    return doc(C_shadow(x, y, s) + PR.sheep(x, y, s, f, variant=i, pose=pose))


def C_shadow(x, y, s, w=190):
    return (f'<ellipse cx="{f1(x)}" cy="{f1(y + 2)}" rx="{f1(w * s / 2 + 10)}" ry="{f1(16 * s + 4)}" fill="#14213a" '
            f'opacity="0.28" filter="url(#soft)"/>')


def lift_sheep_body(pose):
    x, y, s, f = LIFT
    return C_shadow(x, y, s) + PR.sheep(x, y, s, f, variant=1, pose=pose)


def lamb_svg():
    x, y, s, f = LAMB
    return doc(C_shadow(x, y, s, 140) + PR.sheep(x, y, s, f, variant=2, pose="sleep", lamb=True))


def front_grass_svg(side):
    """Dark night bushes, grass tufts and a few little pale flowers framing the bottom corners (they sway)."""
    rng = random.Random(21 + side)
    b = ""
    if side == 0:
        bushes = ((-30, H - 10, 260, 120), (150, H + 30, 220, 90))
        xs = (-40, 560)
    else:
        bushes = ((W + 20, H - 20, 300, 140), (1880, H + 34, 240, 90))
        xs = (1600, W + 40)
    for bx, by, bw, bh in bushes:
        b += S.cloud(bx, by, bw, bh, fill="#24392f", seed=int(bx) + side, puffs=5, sw=3.2, shade_fill="#1a2b24")
    for i in range(26):
        tx = rng.uniform(*xs)
        edge = 1 - abs((tx - sum(xs) / 2) / (xs[1] - xs[0])) * 1.6
        ty = H + 10 - rng.uniform(0, 80) * max(0.2, edge)
        h = rng.uniform(22, 40)
        b += (f'<path d="M{f1(tx - 12)},{f1(ty)} l6,{f1(-h)} l6,{f1(h * 0.8)} l6,{f1(-h * 1.15)} l6,{f1(h)} l6,{f1(-h * 0.7)} '
              f'l4,{f1(h * 0.6)}" stroke="#2a4a38" stroke-width="3.4" fill="none" stroke-linecap="round" '
              f'stroke-linejoin="round"/>')
    for i in range(5):
        fx_ = rng.uniform(xs[0] + 80, xs[1] - 80)
        fy_ = H - rng.uniform(50, 100)
        b += (f'<path d="M{f1(fx_)},{f1(fy_ + 46)} Q{f1(fx_ - 6)},{f1(fy_ + 20)} {f1(fx_)},{f1(fy_)}" stroke="#2a4a38" '
              f'stroke-width="3" fill="none"/>')
        for k in range(5):
            a = 2 * math.pi * k / 5
            b += (f'<circle cx="{f1(fx_ + 7 * math.cos(a))}" cy="{f1(fy_ + 7 * math.sin(a))}" r="5" fill="#dcd8e6" '
                  f'stroke="{INK}" stroke-width="1.8"/>')
        b += f'<circle cx="{f1(fx_)}" cy="{f1(fy_)}" r="3.4" fill="#f2c94e"/>'
    return doc(S.g(b, filter="wobble-fine"))


# ================================================================== build


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    if len(marks) == 1:                       # fallback: the title is the last 4 characters
        ch = ch[-4:]
    return t_rib, ch


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_done = onsets[-1] + 0.45
    t_lift = snap(1.1)

    # ---------------- sky, star, hills
    sc.add("sky", sky_svg(), z=0, wc=0.55)
    sc.add("beam", beam_svg(), z=1, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.75 + 0.25 * M.progress(t, onsets[0], onsets[-1] + 0.4, "sine")
                               + 0.05 * math.sin(2 * math.pi * t / 3.1)))
    sc.add("star", [star_svg(k / 6) for k in range(4)], z=1.2, wc=0,
           frame_at=lambda t: 1.5 + 1.5 * math.sin(2 * math.pi * t / 4.2))
    sc.add("hills", hills_back_svg(), z=2, wc=0.8)
    sc.add("field", field_svg(), z=3, wc=0.8)
    sc.add("hilltop", hilltop_glow_svg(), z=3.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.55 + 0.25 * M.progress(t, onsets[0], onsets[-1] + 0.4, "sine")))

    # ---------------- the stable with its flickering lamp
    sc.add("path", path_svg(), z=3.2, wc=0.6)
    sc.add("stable", stable_svg("back"), z=4, wc=0.9)
    sc.add("animals", doc(animals_body()), z=4.05, seed=55,
           motion=M.with_pivot(breath(ctx, 0.01, 3.4), (STAB[0], STAB[1])))
    sc.add("stable_front", stable_svg("front"), z=4.08, wc=0.9)
    sc.add("tufts", stable_base_tufts(), z=4.1, wc=0.5)
    sc.add("lampglow", lamp_glow_svg(), z=4.2, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.35 + 0.45 * flicker(t)))
    sc.add("spill", door_spill_svg(), z=4.15, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.45 + 0.35 * flicker(t)))

    # ---------------- sheep resting on the hillside
    for i in range(len(SHEEP)):
        x, y, s, f, pose = SHEEP[i]
        sc.add(f"sheep{i}", sheep_svg(i), z=5 + i * 0.1, seed=60 + i,
               motion=M.with_pivot(breath(ctx, 0.012, 3.0 + 0.4 * i, 0.3 * i), (x, y)))
    lx, ly, ls, lf = LIFT
    lift = Fig(ctx, "sheep_lift", (lx, ly), 5.5, seed=71)
    lift.at(0, lift_sheep_body("sleep")).at(t_lift, lift_sheep_body("lie"))
    lift.move(dip(t_lift, 5.0, 0.96), breath(ctx, 0.014, 3.3, 0.6))
    lift.add(sc)
    sc.add("lamb", lamb_svg(), z=5.45, seed=73, motion=M.with_pivot(breath(ctx, 0.016, 2.6, 0.1), LAMB[:2]))

    # ---------------- foreground grass framing the corners
    for side in (0, 1):
        piv = (260, H + 20) if side == 0 else (1880, H + 20)
        sc.add(f"grass{side}", front_grass_svg(side), z=6 + side * 0.1, wc=0.6,
               motion=M.sway(0.6, 3.6 + side * 0.7, piv, phase=0.3 * side))

    # ---------------- title lettering
    story = load_story()
    rx, ry = RIB

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=rx, py=ry)
    sc.add("ribbon", ribbon_svg(story.SUBTITLE, rx, ry), z=10, motion=unfurl, wc=0)
    title = story.TITLE
    x0 = TITLE_X - TITLE_STEP * (len(title) - 1) / 2
    for i, ch in enumerate(title):
        x = x0 + i * TITLE_STEP
        t0 = onsets[min(i, len(onsets) - 1)] - 0.06

        def pop(t, t0=t0, x=x, i=i):
            if t < t0:
                return Tf(alpha=0)
            a = min(1.0, (t - t0) / 0.12)
            u = min(1.0, (t - t0) / 0.42)
            s = 0.45 + 0.55 * M.ease("back")(u)
            dy = 30 * (1 - M.ease("out")(u)) + 2.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.16))
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 60)
        sc.add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, grad_id=f"n1tg{i}", colors=TITLE_COLS),
               z=10.1 + i * 0.01, motion=pop, wc=0)

    # ---------------- camera: a slow push-in
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 + 26, H / 2 + 4, W * 0.935))], "sine")

    # ---------------- twinkles (open sky only: not over the title, the star, the hills or the stable's hill)
    sx, sy, ss = STAB

    def avoid(x, y):
        if 120 < x < 1110 and 100 < y < 520:                       # title block
            return True
        if (x - STAR[0]) ** 2 + (y - STAR[1]) ** 2 < 300 ** 2:      # the great star's halo
            return True
        if ((x - sx) / (1020 * ss)) ** 2 + ((y - (sy - 420 * ss)) / (900 * ss)) ** 2 < 1.0:   # the stable hill
            return True
        return y > 600 - 0.0 * x
    stars = sky_stars(26, (40, 30, W - 40, 600), avoid, seed=12)
    sc.fx.append(Twinkle(stars, seed=13))
    sc.fx.append(FX.sparkles((STAR[0] - 220, STAR[1] - 160, STAR[0] + 220, STAR[1] + 180), count=7, color=(255, 240, 190),
                             size=(6, 12), period=1.9, drift=0, seed=4))
    sc.fx.append(FX.sparkles((240, 230, 1000, 470), count=6, t0=t_done, color=(255, 236, 180), size=(9, 16),
                             period=2.0, drift=0, seed=9))
    sc.subtitles = False

    # ---------------- sound
    sc.sfx("night", 0, dur=T + 0.3, gain_db=-21, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-28, fade_in=1.0, fade_out=1.3)
    sc.sfx("sheep", t_lift + 0.05, gain_db=-24, pan=-0.5)
    sc.sfx("chime", t_rib, gain_db=-10)
    for t in onsets:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", t_done, gain_db=-17)
    return sc
