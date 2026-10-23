"""Scene 8 - the search at night under a silver moon (Luke 15:4 '去找那一只'). Three picture-book shots joined by hard
cuts at phrase boundaries, then one long shot on the rocky slope that dissolves (plain 1 s fade) into s09_found.

  A  the high hills (props.high_hills + high_path_points, time=1): the winding path climbs from the bottom right up
     over the hills to a far pass under the moon.
  B  the little stream at night (props.spring_hills time=1, its four stepping stones).
  C  the rocky slope (props.rocky_slope time=1 without its own rock / bush; my thorn_bush, big_rock, a trodden path,
     ridge trees, bushes and night flowers), the same place as s09: the big rock on the right; the lamb is curled up
     in the rock's shadow on its far side, just out of the frame (s09 finds it).

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers, checked for sanity,
falling back to the subtitle chunks; nothing hard-coded to the take). Times are for the current take:
  0 .. 0.9      calm page (the page-dip from s07 lands here): the shepherd at the foot of the steep path, lantern
                lit, looking up the hill; stars twinkle, clouds drift, grass sways, the lantern flickers
  '翻过' 1.55   he climbs (climb_a / climb_b, the raised foot on the higher ground, the crook planted ahead) up the
                steep first stretch of the path, getting smaller with the perspective
  '走过' 3.14   at the bend he turns and walks the winding path (planted-foot walk, perspective scale); the camera
                pulls back and up: the long winding path to the pass and the moon
  '跨过' 4.91   cut to the stream: he hops across the four stepping stones toward us (step_a in the air, step_b
                balanced on each stone), a silver ripple and a tiny splash on every landing, onto the near bank
  '小羊' 7.17   (H) he turns and calls into the valley, hands cupped (call): sound arcs fly out and a soft echo
                '小羊…' answers from the far hills; '小羊' 8.27 he turns and calls the other way; '你在哪里' 9.37
                he calls again (arcs, echo)
  '找啊找' 10.98 cut to the rocky slope: he walks in, stops and peers ahead, lantern raised (look_around);
                '找啊找' 12.27 he turns and looks back
  '天越来越黑'   a cloud slides over the moon (it still peeks out), the night deepens (the lantern glow reads
                stronger); he walks on to the thorn bush
  '路越来越难走'  push_through: he leans into the thorns, the bush shakes (rustle)
  '一直找'       he comes out and walks on, determined, the camera following him toward the big rock
  '一定要找到它'  he stops and raises the lantern high (look_around, determined), the lantern light swells
  end           calm hold: the last second is identical to s09's first second (plain fade; s09 calls the shared
                add_slope / Slope helpers below on the same stage with the same seeds and the global clock)

The stage, the drawing helpers, the Fig flipbook figure and the slope backdrop are shared with s09_found (and the
timing / figure helpers with s10_party).
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
PUNCT = "，。？！：；、…,.?!:;—"

# ------------------------------------------------------------------ stage (shared with s09)
SW, SH = 2900, 1300
FS = 0.85                       # people scale on the slope (the shepherd ~320 px tall)
NIGHT = 1.0                     # props time: the silver moonlit night

# night tint for people / the lamb (a multiply in sRGB, like a low-opacity blue-violet layer)
TINT = (0.80, 0.84, 0.95)
NIGHT_DEFS = ('<filter id="ntint" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
              f'<feColorMatrix type="matrix" values="{TINT[0]} 0 0 0 0  0 {TINT[1]} 0 0 0  0 0 {TINT[2]} 0 0  0 0 0 1 0"/>'
              '</filter>'
              '<filter id="silw" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">'
              '<feFlood flood-color="#1c2340"/><feComposite in2="SourceAlpha" operator="in"/></filter>')


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, NIGHT_DEFS + defs, w, h)


def f1(v):
    return f"{v:.1f}"


def tinted(markup):
    return f'<g filter="url(#ntint)">{markup}</g>'


# ------------------------------------------------------------------ timing
class Beats:
    """at(li, text, k): onset of character k of ``text`` in line li, measured in the voice clip (voice_marks). A
    measured phrase that starts before the previous one ended or outside its line is ignored; then the subtitle chunk
    containing the text is used, proportionally."""

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

    def at(self, li, text, k=0, occ=0):
        ln = self.ctx.lines[li]
        n = 0
        for m in self.marks[li]:
            if m and text in m[0]:
                if n < occ:
                    n += 1
                    continue
                ct = char_times(m)
                return ct[min(m[0].index(text) + k, len(ct) - 1)]
        n = 0
        for c in ln.chunks:
            if text in c.text:
                body = c.text.rstrip(PUNCT)
                i = c.text.index(text) if occ == 0 else c.text.find(text, c.text.index(text) + 1)
                i = max(0, i) + k
                return c.start + (c.end - c.start) * min(i, len(body)) / max(1, len(body))
        i = max(0, ln.text.find(text)) + k
        return ln.start + (ln.end - ln.start) * i / max(1, len(ln.text))

    def end(self, li, text, occ=0):
        n = 0
        for m in self.marks[li]:
            if m and text in m[0]:
                if n < occ:
                    n += 1
                    continue
                return m[2]
        for c in self.ctx.lines[li].chunks:
            if text in c.text:
                return c.end
        return self.ctx.lines[li].end


# ------------------------------------------------------------------ small motion helpers
def env(t, t0, t1, fin=0.4, fout=0.4):
    """0 -> 1 -> 0 envelope."""
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def clamp_cam(c, w=SW, h=SH, x0=0.0, x1=None):
    x1 = w if x1 is None else x1
    cw = min(c.w, x1 - x0, h * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, x0 + cw / 2 + 1), x1 - cw / 2 - 1), min(max(c.y, ch / 2 + 1), h - ch / 2 - 1), cw, c.rot)


def cam_path(keys, curves, w=SW, h=SH, x0=0.0, x1=None):
    f = M.cam_keys([(t, clamp_cam(c, w, h, x0, x1)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), w, h, x0, x1)


def gfx(make, g0, t0=-1e4, t1=1e9, **kw):
    """An engine.fx effect on the film's global clock (identical in two scenes joined by a plain fade)."""
    inner = make(t0=t0 + g0, t1=t1 + g0 if t1 < 1e8 else 1e9, **kw)
    return lambda frame, t, view: inner(frame, t + g0, view)


def flicker(g0, base=0.9, amp=0.1, seed=0.0):
    """A warm flame flicker (0..1 factor) on the global clock."""
    def f(t):
        u = t + g0 + seed
        return base + amp * (0.55 * math.sin(2 * math.pi * u / 0.53) * math.sin(2 * math.pi * u / 1.71) +
                             0.45 * math.sin(2 * math.pi * u / 0.29 + 1.3))
    return f


# ------------------------------------------------------------------ the track: an anchor moving over time
class Track:
    """Anchor position over time: holds, eased moves and hop arcs. pos(t) -> (x, y, k, ground_y); k = the figure's
    scale relative to its reference drawing (perspective)."""

    def __init__(self, x, y, k=1.0):
        self.moves = []
        self.x0, self.y0, self.k0 = x, y, k
        self.cur = (x, y, k)

    def to(self, t0, t1, x, y, k=None, lift=0.0, curve="sine"):
        k = self.cur[2] if k is None else k
        self.moves.append((t0, t1, self.cur, (x, y, k), lift, curve))
        self.cur = (x, y, k)
        return self

    def __call__(self, t):
        x, y, k = self.x0, self.y0, self.k0
        for t0, t1, a, b, lift, curve in self.moves:
            if t < t0:
                break
            if t >= t1:
                x, y, k = b
                continue
            u = M.progress(t, t0, t1, curve)
            x, y, k = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
            v = (t - t0) / max(1e-6, t1 - t0)
            return x, y - lift * math.sin(math.pi * v), k, y
        return x, y, k, y


class PathLine:
    """A dense polyline (x, y, k) with arc length measured in GROUND units (screen length / k)."""

    def __init__(self, pts):
        self.pts = pts
        self.cum = [0.0]
        for (xa, ya, ka), (xb, yb, kb) in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + math.hypot(xb - xa, yb - ya) / max(0.05, (ka + kb) / 2))

    def at(self, sg):
        sg = max(0.0, min(self.cum[-1], sg))
        for i in range(len(self.pts) - 1):
            if self.cum[i + 1] >= sg:
                u = (sg - self.cum[i]) / max(1e-6, self.cum[i + 1] - self.cum[i])
                a, b = self.pts[i], self.pts[i + 1]
                return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
        return self.pts[-1]

    def sigma_near(self, x, y):
        best = min(range(len(self.pts)), key=lambda i: (self.pts[i][0] - x) ** 2 + (self.pts[i][1] - y) ** 2)
        return self.cum[best]


# planted-foot walk of the parable shepherd: the cycle a, c, b, c; the anchor advances (scale 1 px) on each cut
WALK_FRAMES = ("walk_a", "walk_c", "walk_b", "walk_c")
WALK_ADV = (29.0, 26.0, 59.0, 56.0)       # advance INTO frame i (c->a, a->c, c->b, b->c): 170 px per cycle
CARRY_FRAMES = ("carry_a", "carry_c", "carry_b", "carry_c")


# ------------------------------------------------------------------ the figure: a flipbook with cuts
class Fig:
    """One figure on its own flipbook layer. States are hashable keys drawn by ``draw(key)`` at the reference anchor
    ``ref`` (stage px); ``cut`` switches state with a hard cut (hidden in a squash dip unless dip=False). ``track``
    (Track) moves / scales the drawing over time; loops[key] = (n, period) cycles sub-frames draw(key, i) on the
    film's global clock. Blinks: 0.13 s closed-eye frames."""

    def __init__(self, name, draw, ref, z, g0, seed=0, loops=None, wc=1.0, track=None):
        self.name, self.draw, self.ref, self.z, self.g0, self.seed, self.wc = name, draw, ref, z, g0, seed, wc
        self.loops = loops or {}
        self.ents, self.dips, self.mots = [], [], []
        self.track = track or Track(*ref)
        self.alpha = None

    def cut(self, t, key, dip=True, depth=7.0):
        t = snap(t) if t > 0 else 0.0
        self.ents = [e for e in self.ents if e[0] != t]
        self.ents.append((t, key))
        if dip and t > 0:
            self.dips.append((t, depth))
        return self

    def key_at(self, t):
        ents = sorted(self.ents, key=lambda e: e[0])
        cur = ents[0][1] if ents else None
        for tk, n in ents:
            if tk <= t:
                cur = n
        return cur

    def blinks(self, pairs, t_from, t_to, rng, every=(2.4, 4.2)):
        """pairs: {key: closed-eye key}; no blink within 0.35 s of another cut."""
        t = t_from + rng.uniform(0.4, 1.4)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.3:
            cur = self.key_at(t)
            if cur in pairs and all(abs(t - tk) > 0.35 for tk in cut_ts):
                self.ents += [(snap(t), pairs[cur]), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def point(self, t, q, ground=False):
        """Stage position at time t of the reference-drawing point q (track only, no squash)."""
        x, y, k, gy = self.track(t)
        if ground:
            y = gy
        return x + (q[0] - self.ref[0]) * k, y + (q[1] - self.ref[1]) * k

    def motion(self):
        px, py = self.ref
        tr = self.track

        def base(t):
            x, y, k, _ = tr(t)
            return Tf(dx=x - px, dy=y - py, sx=k, sy=k, px=px, py=py)
        mots = [base] + [squash(td, FS, self.ref, depth) for td, depth in self.dips] + self.mots
        al = self.alpha
        if al is not None:
            mots.append(lambda t: Tf(alpha=al(t)))
        return M.combine(*mots)

    def build(self, sc, blend="normal"):
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
                frames.append(doc(self.draw(n, k) if n in self.loops else self.draw(n)))
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
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=self.wc, motion=self.motion(), blend=blend)
        return self


def breath(piv, g0, period=3.0, amount=0.012, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start), so neighbouring scenes breathe in step."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def walk_x(fig, tr, t0, t1, x0, x1, keyf, y=None, start=0, frames=WALK_FRAMES, k=1.0, s=FS):
    """Planted-foot walk of the parable shepherd along a straight line from x0 to x1 (stage px) between t0 and t1:
    hard cuts through the cycle a, c, b, c with the anchor advancing on each cut (the planted foot stays put). keyf(frame
    name) -> Fig key. Returns the time of the last cut."""
    y = tr.cur[1] if y is None else y
    f = 1 if x1 >= x0 else -1
    dist = abs(x1 - x0)
    n = max(2, int(round(dist / (170 * s * k) * 4)))
    adv = [WALK_ADV[(start + i) % 4] for i in range(n)]
    tot = sum(adv)
    per = max(0.12, (t1 - t0) / n)
    x = x0
    tk = t0
    for i in range(n):
        tk = snap(t0 + i * per)
        fig.cut(tk, keyf(frames[(start + i) % 4]), dip=False)
        xn = x + f * dist * adv[i] / tot
        tr.to(tk - 0.05, tk + 0.07, xn, y, None)
        x = xn
    return tk


# ------------------------------------------------------------------ the shepherd
SH_DOWN = ("kneel_hug", "lift", "cheer", "dance", "call", "worried", "puzzled", "knock", "wave", "count")
_BLINK_DONE = set()


def blink_expr(e):
    """A closed-eye variant of expression e (registered once in characters.EXPRS)."""
    name = f"ls8b_{e}"
    if name not in C.EXPRS:
        C.EXPRS[name] = dict(C.EXPRS[e], eyes="closed")
    return name


def shep_key(pose, f=1, expr=None, phase=0.0, lamb=None, eyes="open", crook=True, marks=True, lantern=True):
    return (pose, f, expr, round(phase, 3), lamb, eyes, crook, marks, lantern)


SLOPE_END_KEY = shep_key("look_around", 1, "determined", 0.0)   # the s08 end / s09 start pose


def shep_markup(key, x, y, s=FS, tint=True):
    pose, f, expr, phase, lamb, eyes, crook, marks, lantern = key
    m = C.parable_shepherd(x, y, s, f, pose=pose, expr=expr, phase=phase, crook=crook, lantern=lantern, glow=0.0,
                           lamb=lamb, lamb_eyes=eyes, marks=marks)
    return tinted(m) if tint else m


def lantern_ref(key, x, y, s=FS):
    """Where the lantern's light comes from (reference drawing at anchor x, y)."""
    pose, f, expr, phase, lamb, eyes, crook, marks, lantern = key
    if pose in SH_DOWN:
        return x - 92 * s * f, y - 40 * s
    bp = C.shepherd_points(x, y, s, f, pose=pose, phase=phase, lantern=True, lamb=lamb, crook=crook)
    hx, hy = bp["lantern"]
    return hx + 1 * s * f, hy + 44 * s


def rot_about(deg_fn, q, p):
    """A rotation of deg_fn(t) degrees about the point q, for a layer whose motions pivot about p."""
    def m(t):
        th = math.radians(deg_fn(t))
        vx, vy = p[0] - q[0], p[1] - q[1]
        c, s_ = math.cos(th), math.sin(th)
        return Tf(rot=math.degrees(th), dx=c * vx - s_ * vy - vx, dy=s_ * vx + c * vy - vy)
    return m


class ShoulderLamb:
    """The little lamb across the shepherd's shoulders as separate parts so it can nuzzle his cheek (the recipe in
    characters, LOST SHEEP FILM): for shepherd keys with lamb=False and a carry* pose, the lamb's back part is drawn
    inside the shepherd's frames and its front part (head, collar, front legs) on a layer above that rotates about the
    base of its neck in little pulses at ``nuzzle_t``. Call finish(sc) after the shepherd's cuts (instead of sh.build)."""

    def __init__(self, sh, s, g0, z, seed, nuzzle_t=(), eyes="happy", name="lamb_front", deg=7.0, tint=None):
        tinted_ = tint or tinted
        self.tint = tinted_
        self.sh, self.s, self.g0, self.z, self.seed = sh, s, g0, z, seed
        self.nuzzle_t, self.eyes, self.name, self.deg = list(nuzzle_t), eyes, name, deg
        self.ref = sh.ref
        self._cache = {}
        base = sh.draw

        def draw_sh(key, k=None):
            body = base(key) if k is None else base(key, k)
            if self.is_sep(key):
                lx, ly = self.anchor(key)
                back = tinted_(PR.little_lamb(lx, ly, 1.1 * s, key[1], pose="on_shoulders", part="back", eyes=eyes))
                return back + body
            return body
        sh.draw = draw_sh

    @staticmethod
    def is_sep(key):
        return key is not None and key[4] is False and key[0].startswith("carry")

    def anchor(self, key):
        if key not in self._cache:
            self._cache[key] = C.shepherd_points(self.ref[0], self.ref[1], self.s, key[1], pose=key[0], phase=key[3],
                                                 lamb=False)["lamb"]
        return self._cache[key]

    def nuzzle_deg(self, t):
        key = self.sh.key_at(t)
        if not self.is_sep(key):
            return 0.0
        v = 0.0
        for tn in self.nuzzle_t:
            v += env(t, tn, tn + 0.7, 0.2, 0.4) * (1 + 0.3 * math.sin(2 * math.pi * (t - tn) / 0.23))
        return -self.deg * key[1] * min(1.2, v)

    def head_point(self, t):
        """Stage point above the lamb's head (for hearts)."""
        key = self.sh.key_at(t)
        lx, ly = self.anchor(key) if self.is_sep(key) else (self.ref[0], self.ref[1] - 300 * self.s)
        x, y = self.sh.point(t, (lx, ly))
        return x + key[1] * 40 * self.s, y - 80 * self.s

    def finish(self, sc):
        sh = self.sh
        sh.build(sc)
        eyes, s = self.eyes, self.s
        front = Fig(self.name, lambda key: (self.tint(PR.little_lamb(*self.anchor(key), 1.1 * s, key[1], pose="on_shoulders",
                                                                  part="front", eyes=eyes)) if self.is_sep(key) else ""),
                    self.ref, self.z, self.g0, seed=self.seed, track=sh.track)
        front.ents = list(sh.ents)
        front.dips = list(sh.dips)
        front.mots = [m for m in sh.mots]
        ref = self.ref

        def neck(t):
            key = sh.key_at(t)
            return self.anchor(key) if self.is_sep(key) else (ref[0], ref[1] - 250 * s)
        front.mots.append(lambda t: rot_about(self.nuzzle_deg, sh.point(t, neck(t)), sh.point(t, ref))(t))
        front.build(sc)
        return front


def shadow_markup(x, y, s=FS, w=150, op=0.26):
    return C.ground_shadow(x, y, s, w, op, color="#1d2440")


def add_lantern_light(sc, name, fig, key_lantern, z, g0, radius=300, k=0.9, alpha=None, extra=None, s=FS,
                      pool=0.75):
    """A warm light ('screen') that follows the shepherd's lantern (glow=0 in the figure), and a flat warm pool on
    the ground under it."""
    px, py = fig.ref
    gid = f"lglow_{name}"
    defs = S.rad_grad(gid, [(0, "#fff1c4", 0.95), (0.16, "#ffd27a", 0.6), (0.5, "#f6a43c", 0.2), (1, "#f6a43c", 0)])
    r = radius * s
    gc = f"lcore_{name}"
    defs += S.rad_grad(gc, [(0, "#fff6d6", 0.9), (0.35, "#ffdc8c", 0.45), (1, "#ffc861", 0)])
    body = (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r)}" ry="{f1(r * 0.86)}" fill="url(#{gid})"/>'
            f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r * 0.34)}" ry="{f1(r * 0.32)}" fill="url(#{gc})"/>')
    fl = flicker(g0, 0.92, 0.08, seed=len(name))
    cache = {}

    def lpos(t):
        key = fig.key_at(t)
        if key not in cache:
            cache[key] = key_lantern(key)
        return fig.point(t, cache[key])

    def m(t):
        lx, ly = lpos(t)
        a = k * fl(t) * (alpha(t) if alpha else 1.0)
        sc_ = 1.0 + 0.03 * math.sin(2 * math.pi * (t + g0) / 0.71)
        if extra:
            sc_ *= extra(t)
        return Tf(dx=lx - px, dy=ly - py, sx=sc_, sy=sc_, px=px, py=py, alpha=max(0.0, min(1.0, a)))
    sc.add(name, doc(body, defs), z=z, wc=0, blend="screen", motion=m)
    if pool > 0:
        gp = f"lpool_{name}"
        dp = S.rad_grad(gp, [(0, "#ffd890", 0.7), (0.45, "#f6a43c", 0.25), (1, "#f6a43c", 0)])
        pb = f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r * 1.25)}" ry="{f1(r * 0.36)}" fill="url(#{gp})"/>'

        def mp(t):
            lx, ly = lpos(t)
            gx, gy = fig.point(t, fig.ref, ground=True)
            sc_ = extra(t) if extra else 1.0
            lift = max(0.0, min(1.0, (gy - ly) / (260 * s * sc_)))      # a raised lantern lights a wider, softer pool
            a = pool * k * fl(t) * (alpha(t) if alpha else 1.0) * (0.75 + 0.25 * lift)
            return Tf(dx=lx - px, dy=gy - py, sx=sc_ * (0.85 + 0.3 * lift), sy=sc_, px=px, py=py,
                      alpha=max(0.0, min(1.0, a)))
        sc.add(name + "_pool", doc(pb, dp), z=z - 0.5, wc=0, blend="screen", motion=mp)
    return lpos


# ------------------------------------------------------------------ the sky
def moon_markup(mx, my, mr, glow=1.0, disc=True):
    """The silver full moon of this film (the same drawing as props.spring_sky's moon), glow and disc separately."""
    out = ""
    if glow > 0:
        out += PR._ls_glow(mx, my, mr * 5, mr * 5, 0.55 * glow, "s8moon", "#f6f4e6", "#b9c8e6")
    if disc:
        out += (f'<circle cx="{f1(mx)}" cy="{f1(my)}" r="{f1(mr)}" fill="{PR.MOON_SILVER}" stroke="{S.mix(INK, PR.MOON_SILVER, 0.5)}" '
                f'stroke-width="{f1(3.2 * mr / 70)}"/>')
        for (dx, dy, r) in ((-0.30, -0.18, 0.18), (0.25, 0.20, 0.13), (0.10, -0.38, 0.09), (-0.12, 0.34, 0.10)):
            out += f'<circle cx="{f1(mx + dx * mr)}" cy="{f1(my + dy * mr)}" r="{f1(r * mr)}" fill="#e2ddc6" opacity="0.8"/>'
        out += (f'<path d="M{f1(mx - mr * 0.62)},{f1(my - mr * 0.5)} A{f1(mr * 0.8)},{f1(mr * 0.8)} 0 0 1 {f1(mx + mr * 0.2)},'
                f'{f1(my - mr * 0.78)}" fill="none" stroke="#fffdf4" stroke-width="{f1(4 * mr / 70)}" opacity="0.7" '
                f'stroke-linecap="round"/>')
    return out


def cloud_markup(cx, cy, w, seed=0, time=NIGHT):
    pal = PR._ls_pal(time)
    return S.g(PR._ls_cloud(cx, cy, w, w * 0.46, pal["cloud"], pal["cloud_sh"], pal["rim"], 0.6, seed, 3.2),
               filter="wobble")


def twinkle_markup(x, y, r, col="#fbf6e2"):
    w = r * 0.22
    pts = [(x, y - r), (x + w, y - w), (x + r, y), (x + w, y + w), (x, y + r), (x - w, y + w), (x - r, y), (x - w, y - w)]
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    return f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.6)}" fill="{col}" opacity="0.3"/><path d="{d}" fill="{col}"/>'


def add_twinkles(sc, name, g0, box, n, z, seed, gate=None):
    """Three layers of little four-point stars pulsing out of step on the global clock."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for j in range(3):
        b = "".join(twinkle_markup(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(6, 11)) for _ in range(n))
        per = 2.3 + 0.6 * j

        def m(t, j=j, per=per):
            a = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t + g0) / per + j / 3)))
            return Tf(alpha=a * (gate(t) if gate else 1.0))
        sc.add(f"{name}{j}", doc(b), z=z + 0.001 * j, wc=0, motion=m)


def tufts_markup(box, n, seed, lean, col_a="#3d6a6c", col_b="#2c5058", hmin=30, hmax=58):
    """Foreground grass tufts (night-tinted) of five thin blades each, leaning ``lean`` px."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    b = ""
    for i in range(n):
        x = x0 + (x1 - x0) * (i + rng.uniform(0.1, 0.9)) / n
        y = rng.uniform(y0, y1)
        h = rng.uniform(hmin, hmax)
        col = S.mix(col_a, col_b, rng.random())
        for j in range(5):
            dx = (j - 2) * 5.5
            hh = h * (0.62 + 0.38 * (1 - abs(j - 2) / 2)) * rng.uniform(0.85, 1.1)
            tip = dx * 2.2 + lean * rng.uniform(0.7, 1.3) * (0.6 + 0.4 * hh / h)
            w = 4.2
            b += (f'<path d="M{f1(x + dx - w)},{f1(y)} Q{f1(x + dx + tip * 0.3)},{f1(y - hh * 0.55)} {f1(x + dx + tip)},'
                  f'{f1(y - hh)} Q{f1(x + dx + tip * 0.35 + w * 0.6)},{f1(y - hh * 0.5)} {f1(x + dx + w)},{f1(y)} Z" '
                  f'fill="{col}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    return S.g(b, filter="wobble-fine")


def add_tufts(sc, name, g0, box, n, seed, z, gate=None, period=0.8):
    frames = [doc(tufts_markup(box, n, seed, lean)) for lean in (-5, 0, 5)]
    al = (lambda t: Tf(alpha=gate(t))) if gate else None
    sc.add(name, frames, z=z, seed=seed, frame_at=lambda t: float((0, 1, 2, 1)[int((t + g0) / period) % 4]),
           motion=al)


# ------------------------------------------------------------------ the rocky slope (shot C; all of s09)
RGY = 1010                       # the big rock's base line (ground of the slope at the rock)
WGY = 1046                       # the shepherd's walking line, a little in front of the rock
RX, RS = 2200, 1.12              # the big rock (bbox about x -166 .. +159)
BX, BYY = 960, WGY + 4           # the thorn bush he pushes through
BUSH_S = 0.95
LAMB_S = FS * 1.12               # the little lamb at the scale parable_shepherd(kneel_hug) draws it
LAMB_HIDE = (RX + 236, RGY + 24)  # tucked against the rock's far (right) side, out of the s08 / s09 opening frame
MOON_C = (1980, 440)
MOON_R = 74
COVER_X = MOON_C[0] - 200        # the covering cloud's centre x at the s08/s09 boundary (the moon peeks out)
SHADE_A = 0.62                   # the rock's shadow over the hidden lamb
CLOUD_V = -4.0                   # its slow drift (px/s)
SLOPE_SEED = 3
CLOCK_REF = 160.0
SLOPE_CAM0 = Cam(RX + 110 - 825, 760, 1650)   # the s08 end / s09 start frame (the lamb just out of view)                # global seconds where the slope's slow cloud drift is at its drawn place


def slope_sky_svg():
    sky = PR.spring_sky(-10, -10, SW + 10, RGY - 60, time=NIGHT, moon=None, clouds=0, stars=1.0, seed=11, scale=1.0)
    return doc(sky)


def _slope_ridge(i_max=30):
    """The far ridge line of props.rocky_slope(-60, SW + 60, RGY, 1.0, seed=SLOPE_SEED) (same formula)."""
    x0, W_ = -60, SW + 120
    return [(x0 - 60 + (W_ + 120) * i / 30, RGY - 260 - 160 * (i / 30) + 30 * math.sin(i * 0.9 + SLOPE_SEED))
            for i in range(i_max + 1)]


def _poly_y(pts, x):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / max(1e-6, xb - xa)
    return pts[-1][1] if x > pts[-1][0] else pts[0][1]


def slope_back_svg():
    pal = PR._ls_pal(NIGHT)
    # a soft far range behind the ridge, silver-rimmed
    far = PR._ls_hill_pts(-80, SW + 80, RGY - 300, 150, 12, 3)
    b = (f'<path d="{PR._band_path(far, RGY)}" fill="{pal["far2"]}" stroke="{INK}" stroke-width="3"/>'
         f'<path d="{S.smooth_path(far, closed=False)}" fill="none" stroke="{pal["rim"]}" stroke-width="4" opacity="0.6"/>')
    b = S.g(b, filter="wobble")
    b += PR.rocky_slope(-60, SW + 60, RGY, 1.0, time=NIGHT, part="back", rock_x=False, bush_x=False, seed=SLOPE_SEED,
                        bottom=SH + 30)
    # little round trees along the far ridge, two bigger ones on the slope
    ridge = _slope_ridge()
    ridge_full = _slope_ridge()
    rng = random.Random(23)
    tr = ""
    for i, x in enumerate((140, 520, 690, 1230, 1580, 2480, 2640)):
        y = _poly_y(ridge, x) + rng.uniform(16, 40)
        tr += PR._round_tree(x, y, rng.uniform(0.42, 0.6), NIGHT, seed=60 + i, kind="light" if i % 3 == 0 else "round")
    tr += PR._round_tree(250, RGY - 34, 1.45, NIGHT, seed=5)
    tr += PR._round_tree(2790, RGY - 50, 1.2, NIGHT, seed=8, kind="light")
    # soft round bushes and a few rocks where the far ridge meets the slope (depth, and less empty ridge)
    slope_top = [(-120 + 3140 * i / 24, RGY - 40 - 90 * (i / 24) + 12 * math.sin(i * 1.7 + SLOPE_SEED)) for i in range(25)]
    rng2 = random.Random(29)
    for i in range(16):
        x = 60 + i * 185 + rng2.uniform(-50, 50)
        if abs(x - BX) < 260 or abs(x - RX) < 260:
            continue
        y = _poly_y(slope_top, x) + rng2.uniform(-6, 10)
        r = rng2.uniform(22, 36)
        if i % 3 == 1:
            tr += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.3)}" ry="{f1(r * 0.75)}" fill="{pal["rock"]}" '
                   f'stroke="{INK}" stroke-width="3"/><ellipse cx="{f1(x - r * 0.3)}" cy="{f1(y - r * 0.3)}" '
                   f'rx="{f1(r * 0.6)}" ry="{f1(r * 0.22)}" fill="{S.mix(pal["rock"], pal["rim"], 0.5)}" opacity="0.7"/>')
        else:
            tr += PR._cluster([(x - r * 0.8, y, r * 0.8), (x + r * 0.6, y - 2, r * 0.9), (x, y - r * 0.6, r * 0.85)],
                              S.mix(pal["tree"], pal["near"], 0.35), 3.0)
            tr += (f'<ellipse cx="{f1(x - r * 0.2)}" cy="{f1(y - r * 1.1)}" rx="{f1(r * 0.4)}" ry="{f1(r * 0.16)}" '
                   f'fill="{S.mix(pal["tree"], pal["rim"], 0.45)}" opacity="0.7"/>')
    b += S.g(tr, filter="wobble")
    # the far ridge gets a soft shade toward its foot (volume)
    gid = "ridgeshade"
    b += (f'<defs>{S.lin_grad(gid, [(0, "#5a6690", 0), (0.55, "#5a6690", 0.10), (1, "#4a5680", 0.26)])}</defs>'
          f'<path d="{S.smooth_path(ridge_full, closed=False)} L{S.smooth_path(slope_top[::-1], closed=False)[1:]} Z" '
          f'fill="url(#{gid})"/>')
    # the trodden path along the slope (he walks on it in s08 and walks home on it in s09)
    pcol = S.mix(PR._lt("#ecdcb8", NIGHT, 0.75), pal["near2"], 0.38)
    top, bot = [], []
    for i in range(23):
        x = -80 + (SW + 160) * i / 22
        yc = WGY + 6 + 7 * math.sin(i * 0.9 + 1.3)
        hw = 22 + 6 * math.sin(i * 1.7 + 0.4)
        top.append((x, yc - hw))
        bot.append((x, yc + hw))
    d = S.smooth_path(top, closed=False) + " L" + S.smooth_path(bot[::-1], closed=False)[1:] + " Z"
    b += S.g(f'<path d="{d}" fill="{pcol}" opacity="0.8" stroke="{INK}" stroke-width="2.4" stroke-opacity="0.45"/>'
             f'<path d="{S.smooth_path(top, closed=False)}" fill="none" stroke="{pal["rim"]}" stroke-width="3" '
             f'opacity="0.35"/>', filter="wobble")
    rngp = random.Random(41)
    dd = ""
    for i in range(40):
        x = rngp.uniform(0, SW)
        dd += f"M{f1(x)},{f1(WGY + rngp.uniform(-8, 22))} l{f1(rngp.uniform(8, 16))},0 "
    b += f'<path d="{dd}" stroke="{S.shade(pcol, -0.25)}" stroke-width="2.6" opacity="0.5" stroke-linecap="round"/>'
    # a few night flowers among the stones
    rng = random.Random(17)
    fl = ""
    for i in range(30):
        x = rng.uniform(40, SW - 40)
        y = rng.uniform(RGY + 70, SH - 20)
        if abs(x - BX) < 230 and y < BYY + 70:
            continue
        fl += PR.wildflower(x, y, rng.uniform(0.9, 1.3), rng.choice(("daisy", "clover", "buttercup", "daisy")),
                            sway=rng.uniform(-0.5, 0.5), time=NIGHT)
    return doc(b + fl)


def rock_svg():
    return doc(PR.big_rock(RX, RGY, RS, time=NIGHT, seed=2))


def bush_svg(part, sway):
    return doc(PR.thorn_bush(BX, BYY, BUSH_S, time=NIGHT, sway=sway, part=part, seed=4))


def rock_shadow_svg():
    """Multiply: the rock's moon shadow on its right side, where the lamb is curled up (a dim shape only)."""
    gid = "rkshade"
    defs = S.rad_grad(gid, [(0, "#4a5470", 1), (0.55, "#66708c", 0.8), (1, "#9aa2b8", 0)])
    cx, cy = LAMB_HIDE[0] - 10, LAMB_HIDE[1] - 40
    return doc(f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="190" ry="120" fill="url(#{gid})"/>', defs)


def lamb_markup(pose, phase=0.0, eyes="open", f=-1, x=None, y=None, s=LAMB_S, tint=True):
    x = LAMB_HIDE[0] if x is None else x
    y = LAMB_HIDE[1] if y is None else y
    m = PR.little_lamb(x, y, s, f, pose=pose, phase=phase, eyes=eyes)
    sh = shadow_markup(x, y, s, 120, 0.22)
    return sh + (tinted(m) if tint else m)


class Slope:
    """The rocky slope backdrop and its shared moving parts (s08 shot C and s09). Everything that moves is a function
    of the film's global clock or of 'u_cover' (0 = the moon free, 1 = behind the cloud), so s08's last second and
    s09's first second are identical.
      cover(t): 0..1 how far the cloud is over the moon; dark(t): 0..1 the deeper night; bright(t): 0..1 the moon
      shining out brighter (s09)."""

    def __init__(self, sc, g0, cover, dark, bright=None, z0=0.0, cloud_x=None):
        self.sc, self.g0 = sc, g0
        bright = bright or (lambda t: 0.0)
        sc.add("sl_sky", slope_sky_svg(), z=z0 + 0.0, seed=501)
        add_twinkles(sc, "sl_tw", g0, (0, 0, SW, RGY - 360), 7, z0 + 0.05, seed=31)
        # the moon: glow + disc on their own layers so the cloud can cover it and it can shine out later
        mx, my = MOON_C
        sc.add("sl_moonglow", doc(moon_markup(mx, my, MOON_R, glow=1.0, disc=False)), z=z0 + 0.1, wc=0,
               motion=lambda t: Tf(alpha=max(0.0, min(1.0, 1.0 - 0.6 * cover(t) + 0.0 * bright(t))),
                                   sx=1 + 0.35 * bright(t), sy=1 + 0.35 * bright(t), px=mx, py=my))
        sc.add("sl_moon", doc(moon_markup(mx, my, MOON_R, glow=0.0, disc=True)), z=z0 + 0.12, seed=503,
               motion=lambda t: Tf(alpha=1.0, sx=1 + 0.04 * bright(t), sy=1 + 0.04 * bright(t), px=mx, py=my))
        # drifting clouds (global clock); cloud 0 is the one that covers the moon
        cx_fn = cloud_x or (lambda t: COVER_X + CLOUD_V * (t + g0 - CLOCK_REF))
        sc.add("sl_cloud0", doc(cloud_markup(COVER_X, my + 40, 340, seed=41)), z=z0 + 0.2, seed=505,
               motion=lambda t: Tf(dx=cx_fn(t) - COVER_X))
        for i, (cx, cy, w, v) in enumerate(((560, 250, 300, 5.0), (1240, 140, 250, 3.5), (2650, 230, 270, 4.5),
                                            (120, 480, 220, 3.0))):
            sc.add(f"sl_cloud{i + 1}", doc(cloud_markup(cx, cy, w, seed=43 + 2 * i)), z=z0 + 0.19, seed=507 + i,
                   motion=lambda t, v=v: Tf(dx=v * (t + g0 - CLOCK_REF)))
        sc.add("sl_back", slope_back_svg(), z=z0 + 1.0, seed=511)
        add_tufts(sc, "sl_tufts_far", g0, (60, RGY + 20, SW - 60, RGY + 60), 22, 61, z0 + 1.1)
        # the moonlight that brightens everything when the moon shines out (s09)
        gid = "slmoonlight"
        defs = S.rad_grad(gid, [(0, "#e8eeff", 0.6), (0.35, "#c4d0ee", 0.25), (1, "#b9c8ec", 0)])
        sc.add("sl_moonlight", doc(f'<ellipse cx="{mx}" cy="{my + 120}" rx="1500" ry="900" fill="url(#{gid})"/>', defs),
               z=z0 + 40, wc=0, blend="screen", motion=lambda t: Tf(alpha=0.42 * bright(t)))
        # the deeper night (multiply), lifted by bright
        gid2 = "sldark"
        defs2 = S.lin_grad(gid2, [(0, "#5a6496", 1), (0.6, "#7680b0", 1), (1, "#8a92c0", 1)])
        sc.add("sl_dark", doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#{gid2})"/>', defs2),
               z=z0 + 39, wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.26 * dark(t) * (1 - bright(t))))

    def add_front(self, z_rock, z_bush_back, z_bush_front, bush_sway=None, lamb_light=None):
        """The big rock, the rock's shadow and the thorn bush (back / front parts, shaking with bush_sway(t) -1..1)."""
        sc, g0 = self.sc, self.g0
        sc.add("sl_rock", rock_svg(), z=z_rock, seed=521)
        sways = (-1.0, -0.5, 0.0, 0.5, 1.0)
        fa = None
        if bush_sway is not None:
            fa = lambda t: float(min(range(5), key=lambda i: abs(sways[i] - bush_sway(t))))
        else:
            fa = lambda t: 2.0
        sc.add("sl_bush_back", [bush_svg("back", v) for v in sways], z=z_bush_back, seed=523, frame_at=fa)
        sc.add("sl_bush_front", [bush_svg("front", v) for v in sways], z=z_bush_front, seed=525, frame_at=fa)


X_LOOK = 420                     # the slope shepherd's reference drawing anchor (s08 and s09 draw him here)
X_END = 1640                     # where he stands at the s08 / s09 boundary
LIGHT_UP = 0.18                  # the lantern light swells this much on '一定要找到它' (and stays so into s09)


def slope_shepherd(sc, g0, track, z=30.0):
    """The shepherd on the slope as a Fig drawn at (X_LOOK, WGY) with a fixed seed: s08 and s09 render identical
    pixels for the same key (call .build(sc) after the cuts; then add_slope_shepherd_extras)."""
    return Fig("shepC", lambda key: shep_markup(key, X_LOOK, WGY), (X_LOOK, WGY), z, g0, seed=541, track=track)


def add_slope_shepherd_extras(sc, fig, g0, z=30.0, extra=None, alpha=None):
    """Ground shadow and the lantern light (+ pool) of the slope shepherd; returns the lantern position function."""
    def sm(t):
        p = fig.point(t, (X_LOOK, WGY), ground=True)
        return Tf(dx=p[0] - X_LOOK, dy=p[1] - WGY, alpha=alpha(t) if alpha else 1.0)
    sc.add("shC_shadow", doc(shadow_markup(X_LOOK, WGY, FS, 170, 0.26)), z=z - 0.1, wc=0, motion=sm)
    return add_lantern_light(sc, "shC_light", fig, lambda key: lantern_ref(key, X_LOOK, WGY), z + 8.0, g0, radius=340,
                             k=1.0, extra=extra, alpha=alpha)


# ------------------------------------------------------------------ the call: sound arcs and the echo
def arc_markup(x, y, r, f, col="#f3efe0", sw=5.0):
    a0, a1 = -55, 55
    p0 = (x + f * r * math.cos(math.radians(a0)), y + r * math.sin(math.radians(a0)))
    p1 = (x + f * r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
    sweep = 1 if f > 0 else 0
    return (f'<path d="M{f1(p0[0])},{f1(p0[1])} A{f1(r)},{f1(r)} 0 0 {sweep} {f1(p1[0])},{f1(p1[1])}" fill="none" '
            f'stroke="{col}" stroke-width="{f1(sw)}" stroke-linecap="round"/>')


def add_call_arcs(sc, name, t0, origin, f, z, n=3, travel=520, dur=1.3, gate=None, scale=1.0):
    """Sound arcs flying out of the cupped hands at t0 (stage px), opening toward f, fading as they travel."""
    ox, oy = origin
    for i in range(n):
        ti = t0 + 0.16 * i
        body = arc_markup(ox, oy, 46 * scale, f, sw=6 * scale)

        def m(t, ti=ti):
            u = (t - ti) / dur
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            s_ = 1 + 1.6 * u
            a = min(1.0, u / 0.12) * (1 - u) ** 1.3 * (gate(t) if gate else 1.0)
            return Tf(dx=f * travel * scale * (1 - (1 - u) ** 2), sx=s_, sy=s_, px=ox, py=oy, alpha=a * 0.9)
        sc.add(f"{name}{i}", doc(body), z=z, wc=0, motion=m)


def echo_markup(x, y, size, text="小羊…"):
    return (f'<text x="{f1(x)}" y="{f1(y)}" font-family="LXGW WenKai" font-weight="bold" font-size="{f1(size)}" '
            f'text-anchor="middle" fill="#f6f1de" stroke="#f6f1de" stroke-width="{f1(size * 0.16)}" opacity="0.35" '
            f'stroke-linejoin="round">{text}</text>'
            f'<text x="{f1(x)}" y="{f1(y)}" font-family="LXGW WenKai" font-weight="bold" font-size="{f1(size)}" '
            f'text-anchor="middle" fill="#eef0fa">{text}</text>')


def add_echo(sc, name, t0, pts, z, text="小羊…", gate=None):
    """A soft echo answering from the hills: the word appears smaller and fainter at each point in turn."""
    for i, (x, y, size, a_max) in enumerate(pts):
        ti = t0 + 0.42 * i

        def m(t, ti=ti, a_max=a_max, x=x, y=y):
            a = env(t, ti, ti + 1.25, 0.3, 0.7) * a_max * (gate(t) if gate else 1.0)
            return Tf(alpha=a, dy=-14 * M.progress(t, ti, ti + 1.25, "out"))
        sc.add(f"{name}{i}", doc(echo_markup(x, y, size, text)), z=z, wc=0, motion=m)


# ------------------------------------------------------------------ shot A: the high hills and the winding path
HX0, HX1, HY = -200, 2700, 900  # painted x -280 .. 2780: the camera stays inside
HK = 1.0
A_FS = 0.88                      # the shepherd's scale where the path's perspective k = 1
A_MOON = (1330, 250)
A_XMAX = 2770


def hills_sky_svg():
    return doc(PR.spring_sky(-10, -10, SW + 10, HY - 200, time=NIGHT, moon=None, clouds=0, stars=1.0, seed=21))


def hills_svg():
    b = PR.high_hills(HX0, HX1, HY, HK, time=NIGHT, part="all", seed=2, bottom=SH + 30)
    pal = PR._ls_pal(NIGHT)
    # foreground framing: a big round tree and bushes at the near left
    fg = PR._round_tree(800, 1215, 2.5, NIGHT, seed=14)
    fg += PR._cluster([(660, 1230, 70), (760, 1250, 80), (900, 1262, 66), (1010, 1290, 60)],
                      S.mix(pal["tree"], pal["dark"], 0.35), 3.4)
    fg += PR._cluster([(2650, 1260, 62), (2740, 1240, 74)], S.mix(pal["tree"], pal["dark"], 0.35), 3.4)
    b += S.g(fg, filter="wobble")
    rng = random.Random(9)
    fl = ""
    items = []
    for i in range(80):
        x = rng.uniform(40, A_XMAX - 40)
        y = HY + 100 + (SH - HY - 110) * rng.random() ** 0.7
        items.append((y, x))
    for y, x in sorted(items):
        k = 0.8 + 0.8 * (y - HY) / (SH - HY)
        fl += PR.wildflower(x, y, k, rng.choice(("daisy", "clover", "buttercup", "poppy", "daisy")),
                            sway=rng.uniform(-0.5, 0.5), time=NIGHT)
    return doc(b + fl)


# ------------------------------------------------------------------ shot B: the stream and the stepping stones
BX0, BX1, BHY, BHS = -100, 2700, 820, 1.1
B_FS = 0.86
B_MOON = (1660, 368)


def stream_sky_svg():
    return doc(PR.spring_sky(-10, -10, SW + 10, BHY - 100, time=NIGHT, moon=None, clouds=0, stars=1.0, seed=27))


def stream_svg():
    return doc(PR.spring_hills(BX0, BX1, BHY, BHS, time=NIGHT, part="all", seed=4, bottom=SH + 30))


def ripple_markup(x, y, r, col="#e4ecfa"):
    return (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r)}" ry="{f1(r * 0.3)}" fill="none" stroke="{col}" '
            f'stroke-width="2.2" opacity="0.7"/>'
            f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 0.62)}" ry="{f1(r * 0.19)}" fill="none" stroke="{col}" '
            f'stroke-width="1.8" opacity="0.5"/>')


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(8)

    # ---- beats
    t_fan = bt.at(0, "翻过")
    t_shan = bt.end(0, "翻过高高的山")
    t_zou = bt.at(0, "走过")
    t_lu_end = bt.end(0, "走过弯弯的小路")
    t_kua = bt.at(0, "跨过")
    t_he_end = bt.end(0, "跨过一条小河")
    t_x1 = bt.at(1, "小羊")
    t_x2 = bt.at(1, "小羊", occ=1)
    t_nzn = bt.at(1, "你在哪里")
    t_call_end = bt.end(1, "你在哪里")
    t_z1 = bt.at(2, "找啊找")
    t_z2 = bt.at(2, "找啊找", occ=1)
    t_hei = bt.at(2, "天越来越黑")
    t_nan = bt.at(2, "路越来越难走")
    t_nan_end = bt.end(2, "路越来越难走")
    t_ks = bt.at(3, "可是")
    t_yzz2 = bt.at(3, "一直找", occ=1)
    t_yd = bt.at(3, "一定要找到它")
    t_yd_end = bt.end(3, "一定要找到它")

    t_cutB = snap(min(t_kua - 0.16, t_lu_end + 0.12))       # the stream
    t_cutC = snap((t_call_end + t_z1) / 2 + 0.05)          # the rocky slope
    gateA = lambda t: 1.0 if t < t_cutB else 0.0
    gateB = lambda t: 1.0 if t_cutB <= t < t_cutC else 0.0
    gateAB = lambda t: 1.0 if t < t_cutC else 0.0

    # ================================================================ shot C (the base: static slope + its parts)
    t_dark0 = t_hei - 0.1
    cover = lambda t: M.progress(t, t_dark0, t_dark0 + 1.7, "inout")
    dark = lambda t: M.progress(t, t_dark0 + 0.2, t_dark0 + 1.8, "sine")
    t_cov_end = t_dark0 + 1.7
    cx_start = COVER_X + 560

    def cloud_x(t):
        drift = COVER_X + CLOUD_V * (t - T)           # after covering: the slow drift, the same line as s09
        start = cx_start + CLOUD_V * 0.5 * (t - T)
        return start + (drift - start) * cover(t)
    slope = Slope(sc, g0, cover, dark, cloud_x=cloud_x)

    # the lamb, curled up in the rock's shadow (a dim shape; s09 finds it)
    lamb = Fig("lamb", lambda key: lamb_markup(*key), LAMB_HIDE, 20.0, g0, seed=531)
    lamb.cut(0, ("hide", 0.0, "open"))
    lamb.mots.append(breath(LAMB_HIDE, g0, 2.2, 0.02))
    lamb.build(sc)
    sc.add("sl_rock_shade", rock_shadow_svg(), z=20.5, wc=0, blend="multiply", motion=lambda t: Tf(alpha=SHADE_A))

    # the shepherd on the slope
    x_look = X_LOOK
    x_bush0 = BX - 172
    x_bush1 = BX + 128
    x_end = X_END
    trC = Track(x_look - 70, WGY)
    shC = slope_shepherd(sc, g0, trC)

    def walk(fig, tr, t0, t1, x0, x1, f=1, expr=None, period=0.19, start=0, y=WGY):
        return walk_x(fig, tr, t0, t1, x0, x1, lambda fr: shep_key(fr, f, expr), y=y, start=start)

    # walking in, look ahead / back ('找啊找' x2)
    walk(shC, trC, t_cutC, t_z1 - 0.1, x_look - 70, x_look, 1, "determined")
    shC.cut(t_z1 - 0.02, shep_key("look_around", 1, "worried", 0.0), depth=7)
    shC.cut(t_z2 - 0.02, shep_key("look_around", 1, "worried", 0.6), depth=7)
    # '天越来越黑': on to the bush
    t_w2 = max(t_z2 + 0.75, t_hei - 0.05)
    shC.cut(t_w2, shep_key("walk_c", 1, "determined"), depth=4)
    walk(shC, trC, t_w2 + 0.19, t_nan - 0.1, x_look, x_bush0, 1, "worried", start=2)
    # '路越来越难走': push through the thorns
    t_push = t_nan - 0.05
    shC.cut(t_push, shep_key("push_through", 1, "determined"), depth=6)
    t_push_end = max(t_nan_end + 0.15, t_push + 1.3)
    trC.to(t_push + 0.1, t_push_end, x_bush1, WGY, None, curve="inout")
    shC.mots.append(lambda t: Tf(rot=1.6 * math.sin(2 * math.pi * (t - t_push) / 0.55) * env(t, t_push, t_push_end, 0.2, 0.2),
                                 px=0, py=0) if t_push <= t <= t_push_end else Tf())
    # out and on, determined ('一直找'), then stop and raise the lantern high ('一定要找到它')
    t_out = snap(t_push_end)
    shC.cut(t_out, shep_key("walk_c", 1, "determined"), depth=5)
    t_stop = t_yd - 0.12
    walk(shC, trC, t_out + 0.2, t_stop - 0.12, x_bush1, x_end, 1, "determined", period=0.2, start=2)
    key_end = SLOPE_END_KEY
    shC.cut(t_stop, key_end, depth=8)
    rngC = random.Random(5)
    shC.blinks({key_end: shep_key("look_around", 1, blink_expr("determined"), 0.0),
                shep_key("look_around", 1, "worried", 0.0): shep_key("look_around", 1, blink_expr("worried"), 0.0)},
               t_cutC, T - 1.3, rngC)
    shC.mots.append(breath((x_look, WGY), g0, 3.0, 0.012))
    shC.build(sc)
    add_slope_shepherd_extras(sc, shC, g0, extra=lambda t: 1 + LIGHT_UP * env(t, t_yd, T + 5, 0.6, 0.1))

    # the bush shakes while he pushes through
    def bush_sway(t):
        if t_push - 0.1 <= t <= t_push_end + 0.4:
            e = env(t, t_push - 0.1, t_push_end + 0.4, 0.2, 0.45)
            return e * math.sin(2 * math.pi * (t - t_push) / 0.42)
        return 0.0
    slope.add_front(z_rock=19.0, z_bush_back=25.0, z_bush_front=35.0, bush_sway=bush_sway)
    add_tufts(sc, "sl_tufts_near", g0, (-40, SH - 70, SW + 40, SH - 10), 30, 63, 36.0)
    ffC = gfx(FX.motes, g0, rect=(200, RGY - 260, SW - 200, SH - 120), count=16, color=(255, 222, 140), size=(3, 6),
              seed=71, alpha=150)
    sc.fx.append(lambda frame, t, view: ffC(frame, t, view) if t >= t_cutC else frame)

    # ================================================================ shot B: the stream (opaque, above C)
    pb = PR.spring_hills_points(BX0, BX1, BHY, BHS)
    stones = pb["stones"]                                  # near -> far
    far_bank = (stones[3][0] + (stones[3][0] - stones[2][0]) * 0.95, stones[3][1] + (stones[3][1] - stones[2][1]) * 0.95,
                0.64)
    near_bank = (stones[0][0] + (stones[0][0] - stones[1][0]) * 0.95, stones[0][1] + (stones[0][1] - stones[1][1]) * 0.95,
                 1.03)
    hop_pts = [far_bank] + [stones[i] for i in (3, 2, 1, 0)] + [near_bank]
    zB = 100.0
    sc.add("B_sky", stream_sky_svg(), z=zB, seed=301, motion=lambda t: Tf(alpha=gateB(t)))
    add_twinkles(sc, "B_tw", g0, (0, 0, SW, BHY - 380), 6, zB + 0.05, seed=33, gate=gateB)
    sc.add("B_moonglow", doc(moon_markup(*B_MOON, MOON_R, glow=1.0, disc=False)), z=zB + 0.1, wc=0,
           motion=lambda t: Tf(alpha=gateB(t)))
    sc.add("B_moon", doc(moon_markup(*B_MOON, MOON_R, glow=0.0, disc=True)), z=zB + 0.12, seed=303,
           motion=lambda t: Tf(alpha=gateB(t)))
    for i, (cx, cy, w, v) in enumerate(((520, 200, 300, 6.0), (1500, 140, 260, 4.0), (2420, 330, 280, 5.0))):
        sc.add(f"B_cloud{i}", doc(cloud_markup(cx, cy, w, seed=81 + 2 * i)), z=zB + 0.2, seed=305 + i,
               motion=lambda t, v=v: Tf(dx=v * (t - t_cutB), alpha=gateB(t)))
    sc.add("B_hills", stream_svg(), z=zB + 1, seed=311, motion=lambda t: Tf(alpha=gateB(t)))
    # the stream's water shimmer (little silver glints sliding down the stream)
    st = pb["stream"]
    gl = ""
    rngB = random.Random(3)
    for j in range(2):
        b = ""
        for i in range(7, 13):
            x, y, w = st[i]
            for _ in range(2):
                ox = rngB.uniform(-0.6, 0.6) * w
                b += (f'<path d="M{f1(x + ox - 10)},{f1(y + rngB.uniform(-8, 8))} q10,-5 20,0" fill="none" stroke="#eef3fb" '
                      f'stroke-width="3" stroke-linecap="round"/>')
        sc.add(f"B_glint{j}", doc(b), z=zB + 1.05 + 0.001 * j, wc=0,
               motion=lambda t, j=j: Tf(alpha=gateB(t) * (0.5 + 0.5 * math.sin(2 * math.pi * ((t + g0) / 1.3 + j / 2))),
                                        dx=6 * math.sin(2 * math.pi * (t + g0) / 2.6 + j)))

    # the shepherd hops across toward us
    ref_B = (far_bank[0], far_bank[1])
    trB = Track(far_bank[0], far_bank[1], far_bank[2])
    k_ref_B = 1.0
    shB = Fig("shepB", lambda key: shep_markup(key, ref_B[0], ref_B[1], s=B_FS), ref_B, zB + 30, g0, seed=341, track=trB)
    shB.cut(0, shep_key("stand", -1, "determined"))
    hop_t0 = t_kua - 0.08
    hop_dt = max(0.24, min(0.34, (t_he_end + 0.05 - hop_t0) / 5))
    land_ts = []
    for i in range(5):
        a, b = hop_pts[i], hop_pts[i + 1]
        ts = snap(hop_t0 + i * hop_dt)
        te = ts + hop_dt * 0.72
        shB.cut(ts, shep_key("step_a", -1, "determined"), dip=False)
        trB.to(ts, te, b[0], b[1], b[2], lift=26 * b[2], curve="linear")
        shB.cut(te, shep_key("step_b", -1, "determined"), dip=False)
        land_ts.append((te, b))
    t_land = land_ts[-1][0]
    shB.cut(t_land + 0.16, shep_key("stand", -1, "determined"), depth=6)
    # he turns and calls: right, then left
    shB.cut(t_x1 - 0.12, shep_key("call", 1, "call"), depth=7)
    shB.cut(t_x2 - 0.14, shep_key("call", -1, "call"), depth=7)
    shB.cut(t_nzn - 0.1, shep_key("call", -1, "call", marks=True), dip=False)
    shB.mots.append(lambda t: Tf(rot=-3.5 * env(t, t_nzn - 0.15, t_call_end + 0.2, 0.25, 0.4), px=0, py=0))
    shB.mots.append(breath(ref_B, g0, 3.0, 0.012))
    shB.alpha = gateB
    shB.build(sc)
    sc.add("shB_shadow", doc(shadow_markup(ref_B[0], ref_B[1], B_FS, 170, 0.26)), z=zB + 29.9, wc=0,
           motion=lambda t: (lambda p, k: Tf(dx=p[0] - ref_B[0], dy=p[1] - ref_B[1], sx=k, sy=k, px=ref_B[0], py=ref_B[1],
                                             alpha=gateB(t)))(shB.point(t, ref_B, ground=True), trB(t)[2]))
    add_lantern_light(sc, "shB_light", shB, lambda key: lantern_ref(key, ref_B[0], ref_B[1], s=B_FS), zB + 38, g0,
                      radius=330, k=0.95, alpha=gateB, extra=lambda t: trB(t)[2], s=B_FS)
    # ripples on every landing
    for i, (te, b) in enumerate(land_ts[:-1]):
        sc.add(f"B_ripple{i}", doc(ripple_markup(b[0], b[1] + 6, 60 * b[2])), z=zB + 2, wc=0,
               motion=lambda t, te=te, b=b: Tf(sx=1 + 1.2 * M.progress(t, te, te + 0.9, "out"),
                                               sy=1 + 1.2 * M.progress(t, te, te + 0.9, "out"), px=b[0], py=b[1] + 6,
                                               alpha=gateB(t) * env(t, te, te + 0.9, 0.05, 0.7)))
        sc.sfx("splash_small", te, gain_db=-21, pan=-0.2 + 0.1 * i)
    # the call: arcs out of the cupped hands, the echo from the hills
    def mouth(t, key):
        bp = C.shepherd_points(ref_B[0], ref_B[1], B_FS, key[1], pose="call")
        hx, hy = bp["hands"][1]
        return shB.point(t, (hx + 30 * key[1] * B_FS, hy))
    for nm, tc, f in (("B_arcA", t_x1, 1), ("B_arcB", t_x2, -1), ("B_arcC", t_nzn, -1)):
        o = mouth(tc + 0.05, shep_key("call", f, "call"))
        add_call_arcs(sc, nm, tc + 0.05, o, f, zB + 39, gate=gateB, travel=560)
    add_echo(sc, "B_echoA", t_x1 + 0.7, [(1420, 440, 58, 0.9), (1660, 385, 44, 0.6)], zB + 1.5, gate=gateB)
    add_echo(sc, "B_echoB", t_x2 + 0.7, [(470, 450, 58, 0.9), (290, 395, 44, 0.6)], zB + 1.5, gate=gateB)
    add_echo(sc, "B_echoC", min(t_nzn + 0.55, t_cutC - 0.9), [(560, 380, 48, 0.75)], zB + 1.5, text="哪里…",
             gate=gateB)
    add_tufts(sc, "B_tufts", g0, (-40, SH - 60, SW + 40, SH - 8), 30, 65, zB + 36, gate=gateB)

    # ================================================================ shot A: the high hills (opaque, above B)
    zA = 200.0
    sc.add("A_sky", hills_sky_svg(), z=zA, seed=201, motion=lambda t: Tf(alpha=gateA(t)))
    add_twinkles(sc, "A_tw", g0, (0, 0, SW, HY - 520), 6, zA + 0.05, seed=35, gate=gateA)
    sc.add("A_moonglow", doc(moon_markup(*A_MOON, MOON_R, glow=1.0, disc=False)), z=zA + 0.1, wc=0,
           motion=lambda t: Tf(alpha=gateA(t)))
    sc.add("A_moon", doc(moon_markup(*A_MOON, MOON_R, glow=0.0, disc=True)), z=zA + 0.12, seed=203,
           motion=lambda t: Tf(alpha=gateA(t)))
    for i, (cx, cy, w, v) in enumerate(((560, 230, 300, 6.0), (1900, 150, 280, 4.0), (2620, 300, 250, 5.0))):
        sc.add(f"A_cloud{i}", doc(cloud_markup(cx, cy, w, seed=91 + 2 * i)), z=zA + 0.2, seed=205 + i,
               motion=lambda t, v=v: Tf(dx=v * t, alpha=gateA(t)))
    sc.add("A_hills", hills_svg(), z=zA + 1, seed=211, motion=lambda t: Tf(alpha=gateA(t)))

    path = PathLine([tuple(p) for p in PR.high_path_points(HX0, HX1, HY, HK, n=201)])
    u_start, u_bend = 0.035, 0.19
    sg0 = path.sigma_near(*path.pts[int(u_start * 200)][:2])
    sg_bend = path.sigma_near(*path.pts[int(u_bend * 200)][:2])
    p0 = path.at(sg0)
    ref_A = (p0[0], p0[1])
    trA = Track(p0[0], p0[1], 1.0)
    shA = Fig("shepA", lambda key: shep_markup(key, ref_A[0], ref_A[1], s=A_FS * p0[2]), ref_A, zA + 30, g0, seed=241,
              track=trA)
    shA.cut(0, shep_key("stand", 1, "determined"))
    # climbing ('翻过高高的山'): climb_a / climb_b, each step along the steep path
    t_c0 = t_fan - 0.1
    t_c1 = max(t_c0 + 1.2, t_shan + 0.05)
    n_climb = 5
    sg = sg0
    for i in range(n_climb):
        tk = snap(t_c0 + i * (t_c1 - t_c0) / n_climb)
        shA.cut(tk, shep_key("climb_a" if i % 2 == 0 else "climb_b", 1, "determined"), dip=(i == 0), depth=5)
        sg = sg0 + (sg_bend - sg0) * (i + 1) / n_climb
        q = path.at(sg)
        trA.to(tk - 0.04, tk + 0.16, q[0], q[1], q[2] / p0[2], curve="sine")
    # turn at the bend and walk the winding path ('走过弯弯的小路')
    t_turn = snap(max(t_c1 + 0.08, t_zou - 0.18))
    shA.cut(t_turn, shep_key("walk_c", -1, "determined"), depth=5)
    t_w0, t_w1 = t_turn + 0.17, t_cutB + 0.2
    per = 0.165
    n = int((t_w1 - t_w0) / per)
    for i in range(n):
        tk = snap(t_w0 + i * per)
        fr = WALK_FRAMES[(2 + i) % 4]
        shA.cut(tk, shep_key(fr, -1, "determined"), dip=False)
        sg += WALK_ADV[(2 + i) % 4] * A_FS * 1.05
        q = path.at(sg)
        trA.to(tk - 0.04, tk + 0.07, q[0], q[1], q[2] / p0[2])
    shA.mots.append(breath(ref_A, g0, 3.0, 0.012))
    shA.alpha = gateA
    shA.build(sc)
    sc.add("shA_shadow", doc(shadow_markup(ref_A[0], ref_A[1], A_FS * p0[2], 170, 0.26)), z=zA + 29.9, wc=0,
           motion=lambda t: (lambda p, k: Tf(dx=p[0] - ref_A[0], dy=p[1] - ref_A[1], sx=k, sy=k, px=ref_A[0], py=ref_A[1],
                                             alpha=gateA(t)))(shA.point(t, ref_A, ground=True), trA(t)[2]))
    add_lantern_light(sc, "shA_light", shA, lambda key: lantern_ref(key, ref_A[0], ref_A[1], s=A_FS * p0[2]), zA + 38,
                      g0, radius=330, k=0.95, alpha=gateA, extra=lambda t: trA(t)[2], s=A_FS * p0[2])
    add_tufts(sc, "A_tufts", g0, (-40, SH - 60, SW + 40, SH - 8), 30, 67, zA + 36, gate=gateA)
    ffA = gfx(FX.motes, g0, rect=(900, HY - 200, A_XMAX - 60, SH - 100), count=14, color=(255, 222, 140), size=(3, 6),
              seed=73, alpha=150)
    ffB = gfx(FX.motes, g0, rect=(0, BHY - 120, BX1, SH - 100), count=16, color=(255, 222, 140), size=(3, 6), seed=75,
              alpha=150)
    sc.fx.insert(0, lambda frame, t, view: ffA(frame, t, view) if t < t_cutB else (ffB(frame, t, view) if t < t_cutC
                                                                                  else frame))

    # ================================================================ camera
    camA = cam_path([(0.0, Cam(1800, 700, 2040)), (t_fan - 0.3, Cam(1800, 700, 2040)),
                     (t_zou, Cam(1830, 680, 1900)), (t_cutB + 0.3, Cam(1740, 660, 1940))],
                    ["linear", "sine", "sine"], x1=A_XMAX)
    camB = cam_path([(t_cutB, Cam(1160, 700, 1800)), (t_he_end + 0.2, Cam(1000, 745, 1700)),
                     (t_x2 - 0.3, Cam(990, 745, 1700)), (t_cutC, Cam(960, 750, 1680))],
                    ["inout", "sine", "sine"], x1=BX1 + 60)
    end_cam = SLOPE_CAM0
    camC = cam_path([(t_cutC, Cam(830, 770, 1560)), (t_z2 + 0.5, Cam(850, 770, 1560)),
                     (t_push_end, Cam(1120, 765, 1600)), (t_stop + 0.7, end_cam), (T, end_cam)],
                    ["sine", "inout", "inout", "linear"])
    sc.camera = lambda t: camA(t) if t < t_cutB else (camB(t) if t < t_cutC else camC(t))

    # ================================================================ sound
    sc.sfx("night", 0, dur=T + 0.5, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_c0, gain_db=-22)
    sc.sfx("footsteps", t_c0, dur=t_c1 - t_c0 + 0.1, gain_db=-23, pan=0.3)
    sc.sfx("footsteps", t_w0, dur=t_cutB - t_w0, gain_db=-24, pan=0.2)
    sc.sfx("footsteps", t_cutC, dur=t_z1 - t_cutC, gain_db=-24, pan=-0.4)
    sc.sfx("wind_soft", t_hei - 0.2, dur=2.6, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_w2, dur=t_nan - t_w2, gain_db=-24, pan=-0.3)
    sc.sfx("cloth", t_push + 0.05, gain_db=-15, pan=-0.3)
    sc.sfx("crunch", t_push + 0.3, gain_db=-23, pan=-0.3)
    sc.sfx("cloth", t_push + 0.75, gain_db=-17, pan=-0.2)
    sc.sfx("footsteps", t_out + 0.2, dur=t_stop - t_out - 0.2, gain_db=-23, pan=0.0)
    sc.sfx("cloth", t_stop, gain_db=-20, pan=0.1)
    return sc
