"""Scene 7 - Luke 2:8-12. The fields outside Bethlehem at night: a deep starry sky, the little town's lights on the
far hill, olive trees on the ridge, a stone sheepfold with the flock, a small campfire with the shepherds round it.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers, checked for sanity and
falling back to the subtitle chunk; nothing hard-coded to the take). Times are for the current take:
  0 .. 0.9     calm frame (the page turns in over it): the fire flickers, stars twinkle, the town lights glimmer,
               the old shepherd sleeps (z's), the young one dozes by the fire, the sturdy one leans on his crook
               watching the flock, a man and the boy warm their hands; the dog sleeps, sheep breathe
  '有一群牧羊人' a slow push-in on the group
  '夜里'        the watcher turns into a walk (planted strides) over to the dozing young shepherd
  '轮流'        he leans over and gives the sleeper's shoulder two little shakes; the young one wakes (surprised)
  ~0.6 s later the young one stands up with the crook (the handover, hidden in a squash dip); on '羊群' he walks
               to the watch spot and stands there with the crook, while the other sits down by the fire and lies
               down; every pose holds >= 0.5 s
  '忽然'        a light flashes beside the flock and an angel appears in it, floating a little above the grass
               (chime); the shepherds and the dog startle one after another
  '上帝的光'    the glory of the Lord grows round the whole group (a great dome of white-gold light, rays) and on
               '照亮了四周' the night darkness lifts from the whole field
  '吓坏了'      the shepherds fall back: shield their eyes / sit frozen, the boy grabs his lamb, the sheep jump up
               and huddle (bleats), the dropped crook falls on the grass
  '不要怕'      the angel blesses (palm out); the shepherds slowly lower their arms one by one
  '大好消息'    wings open wide, joyful; '所有人' a shower of little sparkles
  '伯利恒'      the angel points toward the town's lights on the far hill; two shepherds turn to look; '救主' a soft
               warm glow breathes over the little town
  '你们会看见'  the angel holds up an open hand: a soft picture-bubble opens above it with the swaddled baby asleep
               in a manger, glowing; '包着布' a twinkle on the cloth, '马槽' the manger glows, '记号' a sparkle
  end          calm, everyone gazing at the vision; the last second is identical to s08's first (a plain fade)
The geometry, drawings and helpers below are shared with s08_choir and s09_visit.
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
from stories.noah.scenes.s01_title import char_times, snap, voice_marks

INK = P["ink"]
PUNCT = "，。？！：；、…,.?!:;"

# ------------------------------------------------------------------ stage (shared with s08)
W7, H7 = 2112, 1800          # a tall stage: the sky of s08 (the heavenly host) is above the fields
GY = 1420                    # night_hills near ground line
K = 0.78                     # people scale
SK = 0.68                    # sheep scale
FIRE = (770, GY + 104)
HX0, HX1 = -350, W7 + 350    # night_hills extent: the little town lands at ~HX0 + 0.22 * width
TOWN = (HX0 + 0.22 * (HX1 - HX0), GY - 270)
FOLD = (1835, GY + 18)
ANGEL = (1400, GY + 104)     # the angel's ground point (it hovers LIFT above it)
LIFT = 70
GLORY = (1060, GY + 150)

# shepherds: key -> (variant, x, y) of their first spot
SHEP = {
    "old": (1, 430, GY + 92),
    "beard": (5, 590, GY + 70),
    "boy": (2, 604, GY + 186),
    "young": (0, 940, GY + 122),
    "sturdy": (3, 1182, GY + 80),
}
YOUNG_UP = (968, GY + 126)             # the young one stands up here ...
YOUNG_WATCH = (1178, GY + 114)         # ... and walks to the watch spot in front of the other
NUDGE = (1036, GY + 96)                # where the watcher stands to nudge the dozing one (behind him, right)
STURDY_REST = (1012, GY + 98)          # where the watcher sits and lies down
LAMB0 = (478, GY + 196)
DOG0 = (196, GY + 206)
CROOK_DROP = (1262, GY + 160)
SHEEP_OUT = [(1512, GY + 150, 1, 0, "lie"), (1636, GY + 214, -1, 1, "sleep"), (1730, GY + 146, 1, 2, "lie"),
             (1960, GY + 210, -1, 3, "sleep")]
SHEEP_IN = [(1700, GY - 6, 1, 1, "sleep"), (1840, GY - 22, -1, 0, "lie"), (1960, GY - 2, -1, 2, "sleep")]
HUDDLE = [(1590, GY + 166), (1680, GY + 188), (1770, GY + 160), (1860, GY + 196)]

# expressions with closed eyes for blinks
BLINKABLE = ("kind", "happy", "amazed", "awed", "joyful", "surprised", "scared", "warm", "startled", "tender",
             "thoughtful", "proclaim", "calm", "neutral")
for _e in BLINKABLE:
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"nv_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"nv_blink_{expr}"


def f1(v):
    return f"{v:.1f}"


def doc7(body, defs=""):
    return S.svg_doc(body, defs, W7, H7)


# ------------------------------------------------------------------ timing
class Tm:
    """at(li, text, k): onset of character k of ``text`` in line li, measured in the voice clip (voice_marks). A
    measured phrase that starts before the previous one ended or outside its line is ignored; then the subtitle
    chunk containing the text is used, proportionally."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.marks = []
        for i, ln in enumerate(ctx.lines):
            try:
                ms = voice_marks(ctx, i)
            except Exception:
                ms = []
            ok, prev_end = [], ln.start - 0.35
            for m in ms:
                if m[1] < prev_end - 0.05 or m[1] > ln.end + 0.3 or m[2] < m[1]:
                    ok.append(None)
                else:
                    ok.append(m)
                    prev_end = m[2]
            self.marks.append(ok)

    def at(self, li, text, k=0):
        ln = self.ctx.lines[li]
        for m in self.marks[li]:
            if m and text in m[0]:
                ct = char_times(m)
                return ct[min(m[0].index(text) + k, len(ct) - 1)]
        for c in ln.chunks:
            if text in c.text:
                body = c.text.rstrip(PUNCT)
                i = c.text.index(text) + k
                return c.start + (c.end - c.start) * min(i, len(body)) / max(1, len(body))
        i = max(0, ln.text.find(text)) + k
        return ln.start + (ln.end - ln.start) * i / max(1, len(ln.text))

    def end(self, li, text):
        for m in self.marks[li]:
            if m and text in m[0]:
                return m[2]
        for c in self.ctx.lines[li].chunks:
            if text in c.text:
                return c.end
        return self.ctx.lines[li].end


# ------------------------------------------------------------------ motion helpers
def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def hop(t0, s, piv, height=24.0, dur=0.36):
    """A little hop whose take-off is at t0 (a pose cut hides at the squash before it)."""
    def m(t):
        u = t - t0
        if u < -0.12 or u > dur + 0.18:
            return Tf()
        if u < 0:
            k = (u + 0.12) / 0.12
            return Tf(dy=5 * s * k, sy=1 - 0.05 * k, px=piv[0], py=piv[1])
        if u < dur:
            v = u / dur
            return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.04 * math.sin(math.pi * v), px=piv[0],
                      py=piv[1])
        k = 1 - (u - dur) / 0.18
        return Tf(dy=3 * s * math.sin(math.pi * k), sy=1 - 0.035 * math.sin(math.pi * k), px=piv[0], py=piv[1])
    return m


def breath(piv, g0, period=3.0, amount=0.012, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start), so neighbouring scenes breathe in step."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def rot_about(deg_fn, q, p):
    """A rotation of deg_fn(t) degrees about the point q, for a layer whose motions pivot about p (M.combine keeps
    one pivot): the rotation about p plus the translation that moves its centre to q."""
    def m(t):
        th = math.radians(deg_fn(t))
        vx, vy = p[0] - q[0], p[1] - q[1]
        c, s_ = math.cos(th), math.sin(th)
        return Tf(rot=math.degrees(th), dx=c * vx - s_ * vy - vx, dy=s_ * vx + c * vy - vy)
    return m


def env(t, t0, t1, fin=0.4, fout=0.4):
    """0 -> 1 -> 0 envelope."""
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def clamp_cam(c, w=W7, h=H7):
    cw = min(c.w, w, h * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), w - cw / 2 - 1), min(max(c.y, ch / 2 + 1), h - ch / 2 - 1), cw, c.rot)


def cam_path(keys, curves, w=W7, h=H7):
    f = M.cam_keys([(t, clamp_cam(c, w, h)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), w, h)


class Fig:
    """One figure on its own flipbook layer. States are names -> markup (``draw(state)``); ``cut`` switches state
    with a hard cut (hidden in a squash dip unless dip=False). A state may loop ``loops[state] = (n, period)``
    sub-frames on the film's global clock (draw(state, k)). Blinks: 0.13 s closed-eye frames where no cut is near."""

    def __init__(self, name, draw, piv, s, z, g0, seed=0, docf=doc7, loops=None):
        self.name, self.draw, self.piv, self.s, self.z, self.g0 = name, draw, piv, s, z, g0
        self.seed, self.docf = seed, docf
        self.loops = loops or {}
        self.ents, self.dips, self.mots = [], [], []
        self.blinks = []

    def cut(self, t, state, dip=True, depth=7.0):
        t = snap(t) if t > 0 else 0.0
        self.ents.append((t, state))
        if dip and t > 0:
            self.dips.append((t, depth))
        return self

    def state_at(self, t):
        cur = None
        for tk, n in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = n
        return cur

    def add_blinks(self, pairs, t_from, t_to, rng, every=(2.4, 4.4)):
        """pairs: {state: closed-eye state}."""
        t = t_from + rng.uniform(0.3, 1.6)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.3:
            cur = self.state_at(t)
            if cur in pairs and all(abs(t - tk) > 0.35 for tk in cut_ts):
                self.ents += [(snap(t), pairs[cur]), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def build(self, sc, wc=1.0, extra_motion=None):
        ents = sorted(self.ents, key=lambda e: e[0])
        names = []
        for _, n in ents:
            if n not in names:
                names.append(n)
        frames, index = [], {}
        for n in names:
            nl, _ = self.loops.get(n, (1, 1.0))
            for k in range(nl):
                index[(n, k)] = len(frames)
                frames.append(self.docf(self.draw(n, k) if n in self.loops else self.draw(n)))
        g0, loops = self.g0, self.loops

        def fa(t):
            cur = ents[0][1]
            for tk, n in ents:
                if t >= tk:
                    cur = n
            if cur in loops:
                nl, per = loops[cur]
                return float(index[(cur, int((t + g0) / per) % nl)])
            return float(index[(cur, 0)])
        mots = [squash(td, self.s, self.piv, depth) for td, depth in self.dips] + self.mots
        if extra_motion is not None:
            mots.append(extra_motion)
        piv = self.piv
        motion = M.combine(lambda t: Tf(px=piv[0], py=piv[1]), *mots) if mots else None
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=wc, motion=motion)
        return self


def walk_steps(t0, n, stride, period=0.26, lift=5.0, s=K, move=0.14):
    """Planted-foot walk: n strides of ``stride`` px (signed), the anchor advancing across each cut. Returns
    ([(t, 'walk_a'|'walk_b')], offset(t) -> dx, dy, t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]
    t_end = snap(t0 + n * period)
    ents = [(tc, "walk_a" if k % 2 == 0 else "walk_b") for k, tc in enumerate(cut_t)]

    def off(t):
        x = y = 0.0
        for tk in cut_t:
            u = M.progress(t, tk - move * 0.45, tk + move * 0.55, "sine")
            x += stride * u
            if tk - move * 0.45 <= t <= tk + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - tk + move * 0.45) / move)
        return x, y
    return ents, off, t_end


# ------------------------------------------------------------------ drawings: the night fields
def sky_svg(h=None):
    return doc7(PR.starry_sky(-10, -10, W7 + 10, GY - 120 if h is None else h, density=1.15, twinkle=0.0,
                              milky_way=True, time="night", seed=7))


HILL_SEED = 12


def hills_svg():
    """night_hills, with a patch over the straight bottom edge of the town's mound (props draws it as a closed
    shape whose base line shows above the middle ridge)."""
    far_c = PR._nt("#6f7f62", "night", 1.25)
    tx, base = TOWN[0], GY - 270
    patch = (f'<path d="M{f1(tx - 236)},{f1(base + 20)} L{f1(tx + 236)},{f1(base + 20)} L{f1(tx + 250)},'
             f'{f1(base + 44)} L{f1(tx - 250)},{f1(base + 44)} Z" fill="{far_c}"/>')
    return doc7(PR.night_hills(HX0, HX1, GY, 1.0, part="all", fire_x=False, fold_x=False, town=True,
                               seed=HILL_SEED, bottom=H7 + 40) + patch)


def town_lights_svg(k):
    """A soft warm glow over the little town on the far hill (k: 0..1)."""
    tx, ty = TOWN
    gid = f"twg{int(k * 100)}"
    defs = S.rad_grad(gid, [(0, "#ffe2a0", 0.75), (0.5, "#f6c46a", 0.3), (1, "#f6c46a", 0)])
    return doc7(f'<ellipse cx="{f1(tx)}" cy="{f1(ty - 80)}" rx="{f1(330 * (0.7 + 0.3 * k))}" ry="{f1(150)}" '
                f'fill="url(#{gid})"/>', defs)


def window_twinkles_svg(seed, n=7):
    """A few lit windows of the far town that glimmer (drawn as small warm dots with a halo)."""
    rng = random.Random(seed)
    tx, ty = TOWN
    b = ""
    for _ in range(n):
        x = tx + rng.uniform(-170, 170)
        y = ty + rng.uniform(-110, -60)
        b += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="9" fill="#ffd27a" opacity="0.35"/>'
              f'<rect x="{f1(x - 3.5)}" y="{f1(y - 4)}" width="7" height="8" fill="#ffe7a8"/>')
    return doc7(b)


def star_svg(x, y, r):
    """One twinkling star (a four-point sparkle with a halo)."""
    w = r * 0.22
    pts = [(x, y - r), (x + w, y - w), (x + r, y), (x + w, y + w), (x, y + r), (x - w, y + w), (x - r, y), (x - w, y - w)]
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    return doc7(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.9)}" fill="#fff4cc" opacity="0.25"/>'
                f'<path d="{d}" fill="#fff8de"/><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.2)}" fill="#fffdf2"/>')


def add_star_twinkles(sc, g0, ymax, seed=21, n=14, z=0.5, t_on=None):
    rng = random.Random(seed)
    for i in range(n):
        x, y = rng.uniform(60, W7 - 60), rng.uniform(40, ymax)
        r = rng.uniform(9, 16)
        per, ph = rng.uniform(2.2, 4.2), rng.random()

        def m(t, per=per, ph=ph, x=x, y=y):
            v = math.sin(2 * math.pi * ((t + g0) / per + ph))
            a = max(0.0, v) ** 2
            if t_on is not None:
                a *= t_on(t)
            return Tf(alpha=a, sx=0.6 + 0.4 * a, sy=0.6 + 0.4 * a, px=x, py=y)
        sc.add(f"twinkle{seed}_{i}", star_svg(x, y, r), z=z + 0.001 * i, wc=0, motion=m)


def fold_svg(part):
    return doc7(PR.sheepfold(FOLD[0], FOLD[1], 0.8, 1, part=part, time="night"))


def fire_svg(k):
    return doc7(PR.campfire(FIRE[0], FIRE[1], 0.62, phase=k / 4, fire=1.0, glow=True))


def fire_pool_svg():
    gid = "firepool"
    defs = S.rad_grad(gid, [(0, "#ffd890", 0.55), (0.45, "#f6a43c", 0.22), (1, "#f6a43c", 0)])
    return doc7(f'<ellipse cx="{FIRE[0]}" cy="{FIRE[1] - 10}" rx="560" ry="230" fill="url(#{gid})"/>', defs)


def night_shade_svg():
    """Multiply layer: the cool night over the field, with a warm hole round the fire."""
    gid, hid = "nshade", "nhole"
    defs = (S.lin_grad(gid, [(0, "#ffffff", 0), (0.18, "#9aa8d8", 0.75), (1, "#7d8cc4", 0.95)]) +
            S.rad_grad(hid, [(0, "#ffffff", 1), (0.55, "#ffffff", 0.7), (1, "#ffffff", 0)]))
    top = GY - 330
    b = f'<rect x="-20" y="{top}" width="{W7 + 40}" height="{H7 - top + 40}" fill="url(#{gid})"/>'
    b += f'<ellipse cx="{FIRE[0]}" cy="{FIRE[1] - 60}" rx="520" ry="300" fill="url(#{hid})"/>'
    return doc7(b, defs)


def glory_svg(p):
    return doc7(PR.glory(GLORY[0], GLORY[1], 1.0, progress=p, width=1900, height=1250, rays=True, seed=3))


def glory_light_svg():
    """Screen layer: the white-gold glory lighting the field and everyone in it."""
    gid = "glight"
    defs = S.rad_grad(gid, [(0, "#fff3c8", 0.62), (0.45, "#ffe6a6", 0.36), (1, "#ffe6a6", 0)])
    return doc7(f'<ellipse cx="{GLORY[0]}" cy="{GLORY[1] - 220}" rx="1250" ry="650" fill="url(#{gid})"/>', defs)


def tufts_svg(k):
    """Foreground grass tufts swaying (frame k of 3)."""
    rng = random.Random(5)
    b = ""
    for i in range(26):
        x = -30 + i * 88 + rng.uniform(-20, 20)
        y = H7 - rng.uniform(4, 60)
        h = rng.uniform(36, 70)
        lean = (k - 1) * 5 + rng.uniform(-3, 3)
        col = S.mix("#3f5a3a", "#2d4030", rng.random())
        b += (f'<path d="M{f1(x - 12)},{f1(y)} Q{f1(x - 8 + lean)},{f1(y - h * 0.6)} {f1(x - 4 + lean * 1.6)},'
              f'{f1(y - h)} Q{f1(x)},{f1(y - h * 0.5)} {f1(x + 2)},{f1(y)} M{f1(x)},{f1(y)} Q{f1(x + 6 + lean)},'
              f'{f1(y - h * 0.7)} {f1(x + 14 + lean * 1.4)},{f1(y - h * 0.85)} Q{f1(x + 10)},{f1(y - h * 0.4)} '
              f'{f1(x + 12)},{f1(y)} Z" fill="{col}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>')
    return doc7(S.g(b, filter="wobble-fine"))


def crook_lying(x, y, s=K, rot=-4):
    """A shepherd's crook lying on the grass (dropped)."""
    L = 360 * s
    col = "#8a5a32"
    d = (f"M{f1(x - L / 2)},{f1(y)} L{f1(x + L / 2 - 30 * s)},{f1(y - 4 * s)} "
         f"Q{f1(x + L / 2 + 22 * s)},{f1(y - 8 * s)} {f1(x + L / 2 + 20 * s)},{f1(y - 40 * s)} "
         f"Q{f1(x + L / 2 + 16 * s)},{f1(y - 66 * s)} {f1(x + L / 2 - 10 * s)},{f1(y - 56 * s)}")
    sh = C.ground_shadow(x, y + 2, s, 340, 0.18)
    return sh + (f'<g transform="rotate({rot} {f1(x)} {f1(y)})" filter="url(#wobble-fine)">'
                 f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f1(15 * s)}" stroke-linecap="round" '
                 f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{f1(8 * s)}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/></g>')


# ------------------------------------------------------------------ figures
def shep_markup(key, pose, expr, facing, x, y, crook=True, lamb=True, shadow=True, marks=True, phase=0.0):
    v = SHEP[key][0]
    sh = ""
    if shadow:
        wid = {"sleep": 300, "sit": 210, "sit_warm": 210, "kneel": 170}.get(pose, 130)
        if v == 2:
            wid *= 0.75
        sh = C.ground_shadow(x + (-50 * K * facing if pose == "sleep" else 0), y, K, wid, 0.2)
    return sh + C.shepherds(x, y, K, facing, variant=v, pose=pose, expr=expr, crook=crook, lamb=lamb, marks=marks,
                            phase=phase)


def sheep_markup(x, y, f, v, pose, lamb=False, s=SK):
    wid = 190 if pose in ("lie", "sleep") else 170
    return C.ground_shadow(x, y, s, wid, 0.2) + PR.sheep(x, y, s, f, variant=v, pose=pose, lamb=lamb)


def angel_markup(pose, expr=None, k=0, glow=0.6, x=None, y=None, facing=-1, lift=LIFT, wings=None, nph=6):
    ax, ay = (ANGEL if x is None else (x, y))
    return C.angel(ax, ay, K, facing, pose=pose, expr=expr, variant=0, glow=glow, wings=wings, phase=k / nph,
                   lift=lift)


def bubble_svg(cx, cy, r, hand):
    """A soft picture-bubble: the swaddled baby asleep in the manger, glowing, with a little trail of dots down to
    the angel's raised hand."""
    gid, rid, cid = "bubg", "bubr", "bubclip"
    defs = (S.rad_grad(gid, [(0, "#fffaf0", 1), (0.6, "#fff1cf", 1), (1, "#f6dca0", 1)]) +
            S.rad_grad(rid, [(0, "#fff4cc", 0.0), (0.7, "#fff4cc", 0.0), (0.86, "#ffe8a8", 0.55), (1, "#ffe8a8", 0)]))
    b = f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r * 1.35)}" fill="url(#{rid})"/>'
    hx, hy = hand
    for i, u in enumerate((0.3, 0.58)):          # little trail of dots up from the hand
        px = hx + (cx - hx) * u
        py = hy + (cy + r * 0.85 - hy) * u
        rr = (7 + 6 * i)
        b += f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{rr}" fill="#fff6dc" stroke="{INK}" stroke-width="2.6"/>'
    body = f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="url(#{gid})"/>'
    ms = r / 158
    mx, my = cx, cy + r * 0.86
    inner = (PR.manger(mx, my, ms, 1, part="back", glow=1.0, time="day") +
             C.baby_jesus(*PR.manger_points(mx, my, ms, 1)["bed"], ms, 1, state="in_manger", glow=0.8) +
             PR.manger(mx, my, ms, 1, part="front", time="day"))
    hay = ""
    rng = random.Random(4)
    for _ in range(14):
        x = cx + rng.uniform(-r * 0.8, r * 0.8)
        y = my + rng.uniform(-6, 14)
        hay += (f'<path d="M{f1(x)},{f1(y)} l{f1(rng.uniform(-14, 14))},{f1(rng.uniform(-6, 2))}" '
                f'stroke="#d9b45a" stroke-width="2.4" stroke-linecap="round"/>')
    clip = f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r - 3)}"/></clipPath>'
    b += body + f'<g clip-path="url(#{cid})">' + hay + inner + '</g>'
    b += (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="none" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r - 9)}" fill="none" stroke="#f2c14e" stroke-width="3" '
          f'opacity="0.7"/>')
    return doc7(S.g(b, filter="wobble-fine"), defs + clip)


def baby_glow_svg(cx, cy, r):
    gid = "bglow"
    defs = S.rad_grad(gid, [(0, "#fff6cf", 0.9), (0.5, "#ffe39a", 0.4), (1, "#ffe39a", 0)])
    return doc7(f'<ellipse cx="{f1(cx)}" cy="{f1(cy + r * 0.12)}" rx="{f1(r * 0.62)}" ry="{f1(r * 0.42)}" '
                f'fill="url(#{gid})"/>', defs)


def sparkle_svg(x, y, r, col="#fff6d0"):
    w = r * 0.2
    pts = [(x, y - r), (x + w, y - w), (x + r, y), (x + w, y + w), (x, y + r), (x - w, y + w), (x - r, y), (x - w, y - w)]
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    return doc7(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.7)}" fill="{col}" opacity="0.35"/>'
                f'<path d="{d}" fill="{col}" stroke="#e8b84a" stroke-width="2"/>'
                f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.18)}" fill="#fffdf2"/>')


def pop_motion(t0, piv, dur=0.5, t1=None, out=0.4):
    """Scale-pop in at t0 (and fade out at t1)."""
    def m(t):
        if t < t0:
            return Tf(alpha=0.0)
        u = M.progress(t, t0, t0 + dur, "back")
        a = M.progress(t, t0, t0 + dur * 0.6, "sine")
        if t1 is not None:
            a *= 1 - M.progress(t, t1 - out, t1, "sine")
        s = 0.3 + 0.7 * u
        return Tf(alpha=a, sx=s, sy=s, px=piv[0], py=piv[1])
    return m


# ------------------------------------------------------------------ backdrop shared by s07 / s08 / s09 (fields)
def add_fields(sc, g0, glory_on=None, shade_on=None, town_glow=None, field_on=None, on=None):
    """Sky, twinkles, far hills with the town, fold, campfire. glory_on(t) 0..1 drives the glory dome; field_on(t)
    (default glory_on) the white-gold light on the field, which lifts the night shade; shade_on(t) multiplies the
    night shade; town_glow(t) a warm breath on the town; on(t) (optional) the opacity of all of it (a shot that
    dissolves away)."""
    n0 = len(sc.layers)
    _add_fields(sc, g0, glory_on, shade_on, town_glow, field_on)
    if on is not None:
        for lay in sc.layers[n0:]:
            base = lay.motion
            lay.motion = (lambda base: (lambda t: Tf(alpha=on(t)) if base is None else
                                        (lambda b: Tf(b.dx, b.dy, b.rot, b.sx, b.sy, b.alpha * on(t), b.px, b.py))(base(t))))(base)


def _add_fields(sc, g0, glory_on, shade_on, town_glow, field_on):
    if field_on is None:
        field_on = glory_on
    sc.add("sky", sky_svg(), z=0)
    add_star_twinkles(sc, g0, GY - 330, seed=21, n=16, z=0.5)
    sc.add("town_glow", town_lights_svg(1.0), z=1.05, wc=0, blend="screen", motion=lambda t: Tf(
        alpha=min(1.0, 0.3 + 0.08 * math.sin(2 * math.pi * (t + g0) / 3.7) + (0.7 * town_glow(t) if town_glow else 0.0))))
    sc.add("hills", hills_svg(), z=1)
    for i in range(3):
        sc.add(f"windows{i}", window_twinkles_svg(31 + i, 5), z=1.1 + 0.01 * i, wc=0, motion=lambda t, i=i: Tf(
            alpha=max(0.0, math.sin(2 * math.pi * ((t + g0) / (2.9 + 0.7 * i) + 0.33 * i)))))
    if glory_on is not None:
        gp = (0.08, 0.2, 0.36, 0.55, 0.78, 1.0)
        sc.add("glory", [glory_svg(p) for p in gp], z=2, wc=0.5,
               frame_at=lambda t: max(0.0, min(len(gp) - 1.0, _inv_interp(gp, glory_on(t)))),
               motion=lambda t: Tf(alpha=min(1.0, glory_on(t) / gp[0]) * (0.92 + 0.08 * math.sin(
                   2 * math.pi * (t + g0) / 2.6)) if glory_on(t) > 0.002 else 0.0))
    sc.add("fold_back", fold_svg("back"), z=3)
    sc.add("fold_front", fold_svg("front"), z=5.5)
    sc.add("fire_pool", fire_pool_svg(), z=5.6, wc=0, motion=lambda t: Tf(
        alpha=(0.75 + 0.25 * math.sin(2 * math.pi * (t + g0) / 0.9) * math.sin(2 * math.pi * (t + g0) / 2.3)) *
        (1 - 0.6 * (field_on(t) if field_on else 0.0))))
    sc.add("fire", [fire_svg(k) for k in range(4)], z=6 + FIRE[1] / 1000, wc=0.6,
           frame_at=lambda t: float(int((t + g0) / 0.11) % 4))
    shade = lambda t: (shade_on(t) if shade_on else 1.0) * (1 - (field_on(t) if field_on else 0.0))
    sc.add("night_shade", night_shade_svg(), z=30, wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.5 * shade(t)))
    if glory_on is not None:
        sc.add("glory_light", glory_light_svg(), z=31, wc=0, blend="screen", motion=lambda t: Tf(
            alpha=0.55 * field_on(t) * (0.9 + 0.1 * math.sin(2 * math.pi * (t + g0) / 2.6))))
    sc.add("tufts", [tufts_svg(k) for k in range(3)], z=40, frame_at=lambda t: float((0, 1, 2, 1)[int((t + g0) / 0.7)
                                                                                                   % 4]))


def _inv_interp(vals, v):
    """Fractional index of v in the increasing list vals."""
    if v <= vals[0]:
        return 0.0
    for i in range(len(vals) - 1):
        if vals[i] <= v <= vals[i + 1]:
            return i + (v - vals[i]) / (vals[i + 1] - vals[i])
    return len(vals) - 1.0


def zorder(y):
    return 10 + y / 1000


def gsparkles(rect, g0, t0=-1e4, t1=1e9, **kw):
    """FX.sparkles on the film's global clock (identical in two scenes joined by a plain fade)."""
    inner = FX.sparkles(rect, t0=t0 + g0, t1=t1 + g0 if t1 < 1e8 else 1e9, **kw)
    return lambda frame, t, view: inner(frame, t + g0, view)


# ------------------------------------------------------------------ figures of the fields (shared with s08 / s09)
SEED = {"old": 101, "beard": 103, "boy": 105, "lamb": 107, "young": 109, "crook": 111, "sturdy": 113, "dog": 70,
        "angel": 121, "bubble": 131, "bubble_glow": 132, "vis_sparkle": 133}
# the state every figure is in at the end of s07 (= the start of s08)
FINAL = {"old": "kneel|awed|1|a|", "beard": "stand|awed|1|a|", "boy": "hold_lamb|amazed|1|a|",
         "young": "look_up|awed|1|w|", "sturdy": "kneel|awed|1|r|", "dog": "sit|open", "angel": "announce|warm",
         "sheep_in": "look_up", "sheep_out": "look_up|h|-1"}
SPOTS = {"a": None, "w": YOUNG_WATCH, "r": STURDY_REST, "n": NUDGE, "u": YOUNG_UP}
ANGEL_LOOP = (6, 0.2)


def shep_draw(key, spots=None):
    """Drawing function for Fig: state 'pose|expr|facing|spot|flags' (flags: c = crook, m = marks)."""
    sp = dict(SPOTS, **(spots or {}))

    def d(n):
        pose, expr, f, where, flags = n.split("|")
        x, y = SHEP[key][1:] if where == "a" else sp[where]
        return shep_markup(key, pose, expr, int(f), x, y, crook="c" in flags, marks="m" in flags)
    return d


def shep_piv(key, where="a"):
    return SHEP[key][1:] if where == "a" else SPOTS[where]


def sheep_in_draw(i):
    x, y, f, v, _ = SHEEP_IN[i]
    return lambda n: sheep_markup(x, y, f, v, n)


def sheep_out_draw(i):
    x, y, f, v, _ = SHEEP_OUT[i]
    hx, hy = HUDDLE[i]

    def d(n):
        p, where, ff = n.split("|")
        px, py = (x, y) if where == "a" else (hx, hy)
        return sheep_markup(px, py, int(ff), v, p)
    return d


def dog_draw(n):
    x, y = DOG0
    pose, eyes = n.split("|")
    return C.ground_shadow(x, y, SK, 200, 0.2) + PR.dog(x, y, SK, 1, pose=pose, eyes=eyes)


def angel_draw(n, k):
    pose, expr = n.split("|")
    return angel_markup(pose, expr or None, k)


def angel_bob(g0):
    return lambda t: Tf(dy=6 * math.sin(2 * math.pi * (t + g0) / 2.8))


def bubble_geom():
    ax, ay = ANGEL
    hand = C.hand_positions(C.angel, ax, ay, K, -1, pose="announce", lift=LIFT)[0]
    return (hand[0], hand[1] - 18), (hand[0] - 80, hand[1] - 250, 158)


def add_bubble(sc, g0, t_bub, t_mc=-100.0, t_cloth=None, t_mark=-100.0, t_out=None, out_dur=0.55):
    """The vision bubble above the angel's raised hand: pops in at t_bub, shrinks back into the hand at t_out."""
    hand, (bcx, bcy, br) = bubble_geom()
    bob = lambda t: Tf(dy=6 * math.sin(2 * math.pi * (t + g0) / 2.8) + 3 * math.sin(2 * math.pi * (t + g0) / 3.7))

    def out_m(t):
        if t_out is None or t < t_out:
            return Tf()
        u = M.progress(t, t_out, t_out + out_dur, "in")
        return Tf(alpha=1 - M.progress(t, t_out, t_out + out_dur, "sine"), sx=1 - 0.7 * u, sy=1 - 0.7 * u,
                  px=hand[0], py=hand[1])
    pop = pop_motion(t_bub, hand, 0.6) if t_bub > -50 else (lambda t: Tf())
    sc.add("bubble", bubble_svg(bcx, bcy, br, hand), z=34, seed=SEED["bubble"], motion=M.combine(out_m, pop, bob))
    sc.add("bubble_glow", baby_glow_svg(bcx, bcy, br), z=34.1, wc=0, blend="screen", seed=SEED["bubble_glow"],
           motion=M.combine(out_m, lambda t: Tf(
               alpha=(0.35 + 0.3 * env(t, t_mc - 0.1, t_mc + 1.6, 0.3, 0.8)) * M.progress(t, t_bub + 0.3, t_bub + 0.9) *
               (0.85 + 0.15 * math.sin(2 * math.pi * (t + g0) / 1.9))), bob))
    items = [(t_mark + 0.05, 40, -40, 30, None)]
    if t_cloth is not None:
        items.insert(0, (t_cloth + 0.1, -18, 10, 22, t_cloth + 1.6))
    for i, (tt, dxs, dys, r, t1) in enumerate(items):
        sx_, sy_ = bcx + dxs, bcy + dys
        pop_s = pop_motion(tt, (sx_, sy_), 0.35, t1=t1) if tt > -50 else (lambda t: Tf())
        sc.add(f"vis_sparkle{i}", sparkle_svg(sx_, sy_, r), z=34.2, wc=0, seed=SEED["vis_sparkle"] + i,
               motion=M.combine(out_m, pop_s, lambda t, sx_=sx_, sy_=sy_: Tf(
                   rot=20 * math.sin(2 * math.pi * (t + g0) / 2.0), px=sx_, py=sy_), bob))


def add_crook(sc, t_on=0.0, motion=None):
    sc.add("crook_drop", doc7(crook_lying(*CROOK_DROP)), z=zorder(CROOK_DROP[1]) - 0.002, seed=SEED["crook"],
           motion=M.combine(lambda t: Tf(alpha=1.0 if t >= t_on else 0.0), motion))


# ------------------------------------------------------------------ the scene
def build(ctx):
    sc = Scene(ctx, W=W7, H=H7)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    rng = random.Random(7)

    # ---- beats
    t_qun = tm.at(0, "有一群")
    t_ye = tm.at(0, "夜里")
    t_lun = tm.at(0, "轮流")
    t_shou = tm.at(0, "守着")
    t_yang = tm.at(0, "羊群")
    t_hu = tm.at(1, "忽然")
    t_tian = tm.at(1, "一位天使", 2)
    t_zhan = tm.at(1, "站在")
    t_guang = tm.at(1, "上帝的光")
    t_liang = tm.at(1, "照亮")
    t_xia = tm.at(1, "吓坏", 0)
    t_bu = tm.at(2, "不要怕")
    t_hao = tm.at(2, "大好消息")
    t_suo = tm.at(2, "所有人")
    t_bl = tm.at(3, "伯利恒")
    t_jz = tm.at(3, "救主")
    t_kan = tm.at(4, "你们会看见")
    t_bu2 = tm.at(4, "包着布")
    t_mc = tm.at(4, "马槽")
    t_jh = tm.at(4, "记号")

    glory_on = lambda t: M.progress(t, t_guang - 0.05, t_guang + 0.75, "inout")
    town_glow = lambda t: env(t, t_jz - 0.2, t_kan + 0.4, 0.8, 1.0)
    field_on = lambda t: M.progress(t, t_liang - 0.1, t_liang + 0.9, "inout")
    add_fields(sc, g0, glory_on=glory_on, town_glow=town_glow, field_on=field_on)

    # ---- the sheep: in the fold (asleep, then waking and looking up), outside (jump up and huddle)
    T_B = T - 1.25              # no blinks in the last second (the plain fade to s08 must match frame for frame)
    for i, (x, y, f, v, pose) in enumerate(SHEEP_IN):
        a = Fig(f"sheep_in{i}", sheep_in_draw(i), (x, y), SK, 4 + y / 10000, g0, seed=80 + i)
        a.cut(0, pose)
        a.cut(t_tian + 0.5 + 0.3 * i, "lie" if pose == "sleep" else "look_up", depth=5)
        if pose == "sleep":
            a.cut(t_xia + 0.25 + 0.2 * i, "look_up", depth=5)
        a.mots.append(breath((x, y), g0, 2.6 + 0.3 * i, 0.02, 0.3 * i))
        a.build(sc)
    for i, (x, y, f, v, pose) in enumerate(SHEEP_OUT):
        hx, hy = HUDDLE[i]
        a = Fig(f"sheep_out{i}", sheep_out_draw(i), (x, y), SK, zorder(max(y, hy)), g0, seed=90 + i)
        a.cut(0, f"{pose}|a|{f}")
        a.cut(t_tian + 0.7 + 0.25 * i, f"{'lie' if pose == 'sleep' else 'look_up'}|a|{f}", depth=5)
        # jump up and trot to the huddle by the fold (four little strides)
        t_j = t_xia + 0.1 + 0.18 * i
        fh = 1 if hx > x else -1
        steps = 4
        for k in range(steps):
            a.cut(t_j + 0.22 * k, f"{'walk_a' if k % 2 == 0 else 'walk_b'}|a|{fh}", dip=False)
        t_arr = snap(t_j + 0.22 * steps)
        a.cut(t_arr, f"stand|h|{-1 if hx > 1700 else 1}", depth=4)
        a.cut(t_bu + 1.2 + 0.3 * i, FINAL["sheep_out"], depth=4)

        def off(t, t_j=snap(t_j), t_arr=t_arr, hx=hx, hy=hy, x=x, y=y):
            if t < t_j or t >= t_arr:
                return Tf()
            u = (t - t_j) / (t_arr - t_j)
            return Tf(dx=(hx - x) * u, dy=(hy - y) * u - 6 * abs(math.sin(math.pi * u * steps)))
        a.mots.append(off)
        a.mots.append(breath((x, y), g0, 2.4 + 0.2 * i, 0.02, 0.5 * i))
        a.build(sc)

    # ---- the dog: asleep by the fire, then up and looking at the angel
    dg = Fig("dog", dog_draw, DOG0, SK, zorder(DOG0[1]), g0, seed=SEED["dog"])
    dg.cut(0, "lie|closed")
    dg.cut(t_tian + 0.1, "look_up|open", depth=5)
    dg.cut(t_xia + 0.2, "lie|open", depth=4)
    dg.cut(t_hao + 0.5, FINAL["dog"], depth=4)
    dg.mots.append(breath(DOG0, g0, 2.2, 0.02))
    dg.build(sc)

    # ---- the shepherds
    # the old shepherd: asleep, wakes up, sits frozen, then kneels in awe
    xo, yo = SHEP["old"][1:]
    old = Fig("old", shep_draw("old"), (xo, yo), K, zorder(yo), g0, seed=SEED["old"])
    old.cut(0, "sleep|sleepy|1|a|m")
    old.cut(t_tian + 0.25, "sit|surprised|1|a|", depth=6)
    old.cut(t_xia + 0.05, "sit|scared|1|a|m", dip=False)
    old.cut(t_bu + 0.9, "sit|amazed|1|a|", depth=4)
    old.cut(t_hao + 0.3, FINAL["old"], depth=7)
    old.add_blinks({"sit|amazed|1|a|": "sit|" + blink("amazed") + "|1|a|", FINAL["old"]:
                    "kneel|" + blink("awed") + "|1|a|"}, t_bu + 1.0, T_B, rng)
    old.mots.append(breath((xo, yo), g0, 3.4, 0.014, 0.1))
    old.build(sc)

    # the man with the black beard: warming his hands, startled, shields his eyes, then stands in awe
    xb, yb = SHEP["beard"][1:]
    bd = Fig("beard", shep_draw("beard"), (xb, yb), K, zorder(yb), g0, seed=SEED["beard"])
    bd.cut(0, "sit_warm|kind|1|a|")
    bd.cut(t_tian + 0.05, "sit|surprised|1|a|", depth=5)
    bd.cut(t_xia - 0.05, "shield_eyes|scared|1|a|m", depth=9)
    bd.cut(t_bu + 0.55, "stand|amazed|1|a|", depth=6)
    bd.cut(t_hao + 0.1, "stand|happy|1|a|", dip=False)
    bd.cut(t_kan + 0.4, FINAL["beard"], dip=False)
    bd.add_blinks({"sit_warm|kind|1|a|": "sit_warm|" + blink("kind") + "|1|a|",
                   "stand|amazed|1|a|": "stand|" + blink("amazed") + "|1|a|",
                   "stand|happy|1|a|": "stand|" + blink("happy") + "|1|a|",
                   FINAL["beard"]: "stand|" + blink("awed") + "|1|a|"}, 0.4, T_B, rng)
    bd.mots.append(breath((xb, yb), g0, 3.0, 0.012, 0.4))
    bd.build(sc)

    # the boy: warming his hands, startled, grabs his lamb, then smiles
    xy_, yy_ = SHEP["boy"][1:]
    by = Fig("boy", shep_draw("boy"), (xy_, yy_), K, zorder(yy_), g0, seed=SEED["boy"])
    by.cut(0, "sit_warm|happy|1|a|")
    by.cut(t_tian + 0.15, "sit|surprised|1|a|", depth=5)
    t_grab = t_xia + 0.15
    by.cut(t_grab, "hold_lamb|scared|1|a|", depth=8)
    by.cut(t_bu + 1.3, "hold_lamb|amazed|1|a|", dip=False)
    by.cut(t_hao + 0.2, "hold_lamb|happy|1|a|", depth=4)
    by.cut(t_bl + 0.35, "hold_lamb|amazed|-1|a|", depth=5)
    by.cut(t_kan + 0.3, FINAL["boy"], depth=5)
    by.add_blinks({"sit_warm|happy|1|a|": "sit_warm|" + blink("happy") + "|1|a|",
                   "hold_lamb|happy|1|a|": "hold_lamb|" + blink("happy") + "|1|a|",
                   FINAL["boy"]: "hold_lamb|" + blink("amazed") + "|1|a|"}, 0.4, T_B, rng)
    by.mots.append(breath((xy_, yy_), g0, 2.6, 0.014, 0.7))
    by.build(sc)
    lx, ly = LAMB0
    sc.add("lamb", doc7(sheep_markup(lx, ly, 1, 3, "lie", lamb=True)), z=zorder(ly), seed=SEED["lamb"],
           motion=M.combine(breath((lx, ly), g0, 2.0, 0.025), lambda t: Tf(alpha=1.0 if t < snap(t_grab) else 0.0)))

    # the turn-taking ('夜里，他们轮流守着羊群'): the watcher walks over on '夜里' and leans over the dozing young
    # shepherd; the young one wakes on '轮流', stands up with the crook ~0.6 s later and walks to the watch spot on
    # '羊群'; the watcher sits down and lies down. Every pose holds >= 0.5 s (walk strides are a cycle).
    xs, ys = SHEP["sturdy"][1:]
    nx = NUDGE[0]
    t_turn = t_ye - 0.1
    a_ents, a_off, a_end = walk_steps(t_turn, 2, (nx - xs) / 2, period=0.27)
    t_wake = max(t_lun, a_end + 0.5)             # the nudge (0.45 s) starts after he has arrived
    t_n0 = t_wake - 0.45
    t_up = t_wake + 0.62
    t_walk = max(t_up + 0.5, t_yang + 0.2)
    t_sit = t_up + 0.55
    t_lie = max(t_sit + 0.55, t_hu - 0.45)

    # the young shepherd: dozing by the fire, nudged awake, takes the crook and keeps watch
    xg, yg = SHEP["young"][1:]
    yn = Fig("young", shep_draw("young"), YOUNG_WATCH, K, zorder(YOUNG_UP[1]), g0, seed=SEED["young"])
    yn.cut(0, "sit|sleepy|-1|a|m")
    yn.cut(t_wake, "sit|surprised|-1|a|", dip=False)
    yn.cut(t_up, "stand|happy|1|u|c", depth=8)
    w_ents, w_off, w_end = walk_steps(t_walk, 3, (YOUNG_WATCH[0] - YOUNG_UP[0]) / 3, period=0.26)
    for tk, n in w_ents:
        yn.cut(tk, f"{n}|happy|1|u|c", dip=False)
    yn.cut(w_end, "stand|kind|1|w|c", depth=4)
    yn.mots.append(lambda t: Tf(dx=w_off(t)[0], dy=w_off(t)[1] + (YOUNG_WATCH[1] - YOUNG_UP[1]) * M.progress(
        t, w_ents[0][0], w_end, "linear")) if w_ents[0][0] - 0.1 <= t < w_end else Tf())
    yn.cut(max(t_hu + 0.45, w_end + 0.55), "stand|surprised|1|w|c", depth=6)     # startled by the flash
    yn.cut(t_xia - 0.1, "shield_eyes|scared|1|w|m", depth=10)
    yn.cut(t_bu + 0.3, "look_up|amazed|1|w|", depth=6)
    yn.cut(t_hao + 0.15, "look_up|happy|1|w|", dip=False)
    yn.cut(t_bl + 0.15, "look_up|amazed|-1|w|", depth=5)
    yn.cut(t_kan + 0.2, FINAL["young"], depth=5)
    yn.add_blinks({"stand|happy|1|u|c": "stand|" + blink("happy") + "|1|u|c",
                   FINAL["young"]: "look_up|" + blink("awed") + "|1|w|"}, t_wake, T_B, rng)
    # dozing: the head nods slowly (the whole sitting figure sways a little forward)
    yn.mots.append(rot_about(lambda t: -2.2 * max(0.0, math.sin(2 * math.pi * t / 2.4)) if t < t_wake else 0.0,
                             (xg, yg), YOUNG_WATCH))
    yn.mots.append(breath(YOUNG_WATCH, g0, 3.2, 0.012, 0.2))
    yn.build(sc)
    add_crook(sc, snap(t_xia - 0.1))

    # the sturdy watcher: leaning on his crook, turns, walks over, nudges, hands over the crook, lies down
    st = Fig("sturdy", shep_draw("sturdy"), STURDY_REST, K, zorder(STURDY_REST[1]), g0, seed=SEED["sturdy"])
    st.cut(0, "lean|kind|1|a|")
    for k, (tk, n) in enumerate(a_ents):            # he turns round into his first stride (hidden in a dip)
        st.cut(tk, f"{n}|kind|-1|a|c", dip=(k == 0), depth=4)
    st.cut(a_end, "stand|happy|-1|n|c", depth=3)
    st.mots.append(lambda t: Tf(dx=a_off(t)[0], dy=a_off(t)[1] + (NUDGE[1] - ys) * M.progress(
        t, a_ents[0][0], a_end, "linear")) if a_ents[0][0] - 0.1 <= t < a_end else Tf())
    # the nudge: lean toward the sleeper and give his shoulder two little shakes; he wakes on the second one
    nudge = rot_about(lambda t: -(11 * env(t, t_n0, t_up - 0.05, 0.18, 0.2) + 2.5 * math.sin(
        2 * math.pi * (t - t_n0) / 0.22) * env(t, t_n0 + 0.1, t_n0 + 0.55, 0.08, 0.1)), (nx, NUDGE[1]), STURDY_REST)
    st.mots.append(nudge)
    st.cut(t_up, "stand|happy|-1|n|", depth=6)           # the crook goes to the young one
    st.cut(t_sit, "sit|sleepy|-1|r|", depth=8)
    st.cut(t_lie, "sleep|sleepy|1|r|m", depth=5)
    st.cut(t_tian + 0.45, "sit|surprised|1|r|", depth=7)
    st.cut(t_xia + 0.05, "kneel|scared|1|r|m", depth=8)
    st.cut(t_bu + 0.75, "kneel|amazed|1|r|", dip=False)
    st.cut(t_hao + 0.25, FINAL["sturdy"], dip=False)
    st.add_blinks({"lean|kind|1|a|": "lean|" + blink("kind") + "|1|a|",
                   FINAL["sturdy"]: "kneel|" + blink("awed") + "|1|r|"}, 0.4, T_B, rng)
    st.mots.append(breath(STURDY_REST, g0, 3.1, 0.012, 0.6))
    st.build(sc)

    # ---- the angel: appears in a flash of light beside the flock, floating
    ax, ay = ANGEL
    t_app = t_hu + 0.1
    an = Fig("angel", angel_draw, (ax, ay - LIFT), K, zorder(ay) + 0.001, g0, seed=SEED["angel"],
             loops={s: ANGEL_LOOP for s in ("float|", "bless|", "wings_open|joyful", "point_down|",
                                            "announce|proclaim", FINAL["angel"])})
    an.cut(0, "float|")
    an.cut(t_bu - 0.08, "bless|", depth=5)
    an.cut(t_hao - 0.05, "wings_open|joyful", depth=6)
    an.cut(t_bl - 0.05, "point_down|", depth=5)
    an.cut(t_kan - 0.08, "announce|proclaim", depth=5)
    an.cut(tm.end(4, "这就是") + 0.1, FINAL["angel"], dip=False)
    appear = lambda t: Tf(alpha=M.progress(t, t_app + 0.15, t_app + 0.75, "sine"),
                          dy=-40 * (1 - M.progress(t, t_app, t_app + 1.3, "out")))
    # while it points to the far town it rises a little higher
    rise = lambda t: Tf(dy=-46 * env(t, t_bl - 0.3, t_kan + 0.1, 0.9, 0.9))
    an.mots += [angel_bob(g0), appear, rise]
    an.build(sc)
    sc.add("angel_shadow", doc7(C.ground_shadow(ax, ay, K, 170, 0.25, color="#fff3c0")), z=zorder(ay) - 0.01, wc=0,
           motion=lambda t: Tf(alpha=M.progress(t, t_app + 0.3, t_app + 1.0, "sine")))
    flash_svg = doc7(f'<defs>{S.rad_grad("aflash", [(0, "#fffdf2", 1), (0.35, "#fff3c8", 0.75), (1, "#fff3c8", 0)])}'
                     f'</defs><ellipse cx="{ax}" cy="{ay - LIFT - 120}" rx="340" ry="380" fill="url(#aflash)"/>')

    def flash_m(t):
        a = env(t, t_app - 0.05, t_app + 1.6, 0.35, 1.0)
        s = 0.4 + 0.8 * M.progress(t, t_app - 0.05, t_app + 0.8, "out")
        return Tf(alpha=a, sx=s, sy=s, px=ax, py=ay - LIFT - 120)
    sc.add("angel_flash", flash_svg, z=33, wc=0, blend="screen", motion=flash_m)

    # ---- the vision: a picture-bubble above the angel's raised hand
    t_bub = t_kan + 0.25
    add_bubble(sc, g0, t_bub, t_mc=t_mc, t_cloth=t_bu2, t_mark=t_jh)

    # ---- sparkles: the glory, '所有人', the town
    sc.fx.append(gsparkles((GLORY[0] - 700, GLORY[1] - 900, GLORY[0] + 700, GLORY[1] - 60), g0, t0=t_guang + 0.3,
                           count=26, color=(255, 246, 214), size=(7, 14), period=1.9, drift=0, seed=41))
    sc.fx.append(gsparkles((ax - 420, ay - 520, ax + 260, ay - 140), g0, t0=t_suo - 0.1, t1=t_suo + 2.0, count=22,
                           color=(255, 238, 180), size=(9, 18), period=1.0, drift=-26, seed=43))
    sc.fx.append(gsparkles((TOWN[0] - 200, TOWN[1] - 160, TOWN[0] + 200, TOWN[1] - 40), g0, t0=t_jz - 0.1,
                           t1=t_kan + 0.6, count=10, color=(255, 230, 160), size=(7, 13), period=1.3, drift=-6,
                           seed=45))

    # ---- camera
    cam_end = Cam(1130, 1200, 1800)
    sc.camera = cam_path([
        (0.0, Cam(900, 1290, 1760)), (t_qun, Cam(900, 1290, 1760)), (t_lun, Cam(880, 1328, 1460)),
        (t_hu, Cam(890, 1324, 1480)), (t_zhan + 0.6, Cam(1060, 1214, 2080)), (t_xia + 1.0, Cam(1056, 1212, 2070)),
        (t_bl - 0.2, Cam(1040, 1212, 2050)), (t_bl + 1.3, Cam(990, 1214, 1980)), (t_kan, Cam(1000, 1214, 1980)),
        (t_kan + 2.2, cam_end), (T, cam_end)],
        ["linear", "inout", "sine", "sine", "sine", "sine", "inout", "sine", "inout", "linear"])

    # ---- sound
    sc.sfx("night", 0, dur=T + 0.5, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0, dur=T + 0.5, gain_db=-19, fade_in=0.8, fade_out=1.0, pan=-0.15)
    sc.sfx("snore", 0, dur=t_tian + 0.2, gain_db=-27, fade_in=0.8, fade_out=0.4, pan=-0.35)
    sc.sfx("footsteps", t_turn, dur=a_end - t_turn + 0.1, gain_db=-24, pan=0.1)
    sc.sfx("cloth", t_up, gain_db=-21)
    sc.sfx("footsteps", t_walk, dur=w_end - t_walk + 0.1, gain_db=-24, pan=0.2)
    sc.sfx("cloth", t_lie, gain_db=-23)
    sc.sfx("chime", t_app, gain_db=-11, pan=0.3)
    sc.sfx("whoosh", t_app - 0.1, gain_db=-17, pan=0.3)
    sc.sfx("grow", t_guang - 0.05, gain_db=-14)
    sc.sfx("sheep", t_xia + 0.2, gain_db=-17, pan=0.5)
    sc.sfx("sheep", t_xia + 0.75, gain_db=-20, pan=0.65)
    sc.sfx("cloth", t_xia, gain_db=-19)
    sc.sfx("sparkle", t_suo, gain_db=-17, pan=0.3)
    sc.sfx("chime", t_jz, gain_db=-19, pan=-0.5)
    sc.sfx("sparkle", t_bub, gain_db=-16, pan=0.2)
    sc.sfx("sparkle", t_jh + 0.05, gain_db=-16, pan=0.2)
    return sc
