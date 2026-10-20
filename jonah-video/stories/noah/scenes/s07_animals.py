"""Scene 7 - 然后，动物们来了！ The animals come two by two (Genesis 7:2-3, 8-9; 6:21).

One wide sunny hilltop page (3400 x 1400 stage, everybody at scale 0.6 on one ground line): the finished ark stands on
the hill (door open, ramp down to the right, high window open); a sandy path runs from the right edge to the foot of
the ramp; Noah stands in the grass in front of the path and welcomes everybody.

  line 0  '然后，动物们来了！'  wide page; Noah cheers; the elephants appear at the right edge (the queue begins).
  line 1  '大象来了，咚，咚，咚！'  the camera eases in on the path: the elephant pair stamps three heavy steps, one
          on each 咚 (squash, dust puffs at the feet, a little camera thump, a thud).
          '小鸟飞来了，扑扑扑！'  three songbird pairs fly in from the upper left; the lead pair beats its wings hard
          on each 扑 (lift + flap marks) and they swoop in at the high window (giraffes reach the door, bow, go in).
          '狮子来了，嗷呜！'  the lion pair arrives at the foot of the ramp; on 嗷呜 the lion stops and gives a playful
          roar (mouth wide, eyes shut, mane-fluff strokes, sound arcs); the lioness smiles; Noah laughs.
          '小兔子跳来了，蹦蹦蹦！'  two rabbits peek out of the bush by the ramp, hop out along the grass and, one hop on
          each 蹦, bound into the gap behind the lions and up the ramp.
  line 2  '它们都是两个两个来的，一公一母，排着队走进方舟。'  the camera pulls back: a long happy queue of pairs (hippos,
          monkeys, horses, ducks, deer, sheep, cows, foxes, turtles last and slow) walks up the ramp and in at the door;
          on 一公一母 little hearts pop over the pairs; Noah nods along.
  line 3  '挪亚还在方舟里装满了吃的东西，有人吃的，也有动物吃的。'  Noah's family arrives carrying food (sacks, baskets,
          hay, grain, a jar, vegetables) up the path; Noah waves them in and points to the ark, then steps in at the
          back of the line. They stop on the ramp in a line (the turtles are just inside) - the calm end frame that
          s08 starts from (plain cross-dissolve).

Everything walking uses planted strides (the drawing follows the distance); pose changes are hard cuts hidden in
small squash dips. All times derive from the narration (subtitle chunks, refined by the voiced stretches of the take).
The sprites / steppers / door clip / backdrop helpers here are shared with s08_door and s09_flood.
"""
import math
import random

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import arcs_markup
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine import watercolor as WC
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene

SW, SH = 3400, 1400
GY = 1170                       # ground line (path) for everybody
SC = 0.6                        # one scale for the ark, people and animals
AX = 1150                       # ark anchor (keel on the ground line)
INK = P["ink"]
AP = PR.ark_points(AX, GY, SC, 1)
DX0, DTOP, DX1, SILL = AP["door_box"]
RTX, RTY = AP["ramp_top"]
RBX, RBY = AP["ramp_bottom"]
WBOX = AP["window_box"]
NOAH_SPOT = (2120, GY + 56)     # Noah welcomes everybody, standing in the grass in front of the path
FAM_GAP = 105                   # the family's spacing in their line on the ramp
FAM_ORDER = ["shem", "daughter_in_law0", "ham", "daughter_in_law1", "japheth", "daughter_in_law2", "noah_wife", "noah"]
FAM_ITEMS = {"shem": "sack", "daughter_in_law0": "basket", "ham": "hay", "daughter_in_law1": "grain",
             "japheth": "jar", "daughter_in_law2": "veg", "noah_wife": "basket"}
FAM_FRONT = 1335                # where the first of the line stands at the end (on the landing, by the door)
FAM_END = {n: FAM_FRONT + k * FAM_GAP for k, n in enumerate(FAM_ORDER)}
PUNCT = "，。；：？！、,.;:?!…—"


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return v
    return fa


# ============================================================================ narration timing
_SEGS = {}
_ALIGN = {}


def voice_segs(ctx, i):
    """Voiced stretches [(start, end)] (scene seconds) of narration line i, from its take; None if unavailable."""
    key = (ctx.id, i)
    if key in _SEGS:
        return _SEGS[key]
    out = None
    try:
        import soundfile as sf
        line = ctx.lines[i]
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"), dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        if abs(len(x) / sr - (line.end - line.start)) < 0.3:
            hp = int(sr * 0.01)
            m = len(x) // hp
            e = np.sqrt((x[:m * hp].reshape(m, hp) ** 2).mean(axis=1)) + 1e-7
            db = np.convolve(20 * np.log10(e), np.ones(3) / 3, mode="same")
            db -= db.max()
            q = db < -30
            segs, j = [], 0
            while j < m:
                if not q[j]:
                    k = j
                    while k < m and not q[k]:
                        k += 1
                    if segs and j - segs[-1][1] < 8:
                        segs[-1][1] = k
                    else:
                        segs.append([j, k])
                    j = k
                else:
                    j += 1
            out = [(line.start + a * 0.01, line.start + b * 0.01) for a, b in segs if b - a >= 6]
    except Exception:
        out = None
    _SEGS[key] = out
    return out


def _groups(text):
    out, cur = [], ""
    for ch in text:
        if ch in PUNCT:
            if cur:
                out.append(cur)
                cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _align(groups, segs):
    """Match punctuation-separated text groups to voiced stretches (several groups in one stretch, or one group over
    several stretches), minimising the spread of the speaking rate. Returns the start time of every character."""
    n, m = len(groups), len(segs)
    cnt = [len(g) for g in groups]
    dur = [b - a for a, b in segs]
    r0 = sum(dur) / max(1, sum(cnt))
    INF = 1e18
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] >= INF:
                continue
            for i2 in range(i + 1, n + 1):            # groups i..i2-1 in stretch j
                if j >= m:
                    break
                c = sum(cnt[i:i2])
                cost = c * math.log((dur[j] / c) / r0) ** 2 + 0.05 * (i2 - i - 1)
                if best[i][j] + cost < best[i2][j + 1]:
                    best[i2][j + 1] = best[i][j] + cost
                    back[i2][j + 1] = (i, j, "g")
            if i < n:
                for j2 in range(j + 2, m + 1):         # group i over stretches j..j2-1
                    d = sum(dur[j:j2])
                    cost = cnt[i] * math.log((d / cnt[i]) / r0) ** 2 + 0.05 * (j2 - j - 1)
                    if best[i][j] + cost < best[i + 1][j2]:
                        best[i + 1][j2] = best[i][j] + cost
                        back[i + 1][j2] = (i, j, "s")
    if best[n][m] >= INF:
        return None
    steps = []
    i, j = n, m
    while (i, j) != (0, 0):
        pi, pj, kind = back[i][j]
        steps.append((pi, i, pj, j, kind))
        i, j = pi, pj
    times = []
    for gi0, gi1, sj0, sj1, kind in reversed(steps):
        if kind == "g":
            a, b = segs[sj0]
            c = sum(cnt[gi0:gi1])
            times += [a + (b - a) * k / c for k in range(c)]
        else:
            c = cnt[gi0]
            ss = segs[sj0:sj1]
            if c == len(ss):
                times += [s[0] for s in ss]
            else:
                tot = sum(b - a for a, b in ss)
                for k in range(c):
                    v = tot * k / c
                    for a, b in ss:
                        if v <= b - a + 1e-9:
                            times.append(a + v)
                            break
                        v -= b - a
    return times


def _chunk_est(line, idx):
    """Character idx (in line.text) -> estimated start from the subtitle chunks."""
    pos = 0
    for c in line.chunks:
        k = line.text.find(c.text, pos)
        if k < 0:
            continue
        if k <= idx < k + len(c.text):
            body = c.text.rstrip(PUNCT)

            def w(s):
                return sum(0.5 if ch in PUNCT else 1.0 for ch in s)
            return c.start + (c.end - c.start) * w(c.text[:idx - k]) / max(1.0, w(body))
        pos = k + len(c.text)
    return line.start + (line.end - line.start) * idx / max(1, len(line.text))


def pt(ctx, i, phrase, occ=0):
    """When ``phrase`` (its occ-th occurrence) of line i starts."""
    line = ctx.lines[i]
    idx = -1
    for _ in range(occ + 1):
        idx = line.text.find(phrase, idx + 1)
        if idx < 0:
            raise KeyError(f"{phrase!r} #{occ} not in {line.text!r}")
    key = (ctx.id, i)
    if key not in _ALIGN:
        segs = voice_segs(ctx, i)
        _ALIGN[key] = _align(_groups(line.text), segs) if segs else None
    ts = _ALIGN[key]
    if ts is None:
        return _chunk_est(line, idx)
    ci = sum(1 for ch in line.text[:idx] if ch not in PUNCT)
    return ts[min(ci, len(ts) - 1)]


# ============================================================================ sprites
class Spr:
    """Drawings of one figure on a small canvas (rasterised + watercoloured, cached on disk, cropped), placed per
    frame by a Dynamic layer. Markup is drawn with its anchor at (ax, ay). get() scales and tilts about the anchor."""

    def __init__(self, cw, ch, ax, ay, wc=1.0, seed=0):
        self.cw, self.ch = int(math.ceil(cw)), int(math.ceil(ch))
        self.ax, self.ay = ax, ay
        self.wc, self.seed = wc, seed
        self.svgs, self.imgs, self.offs = [], None, None
        self._c = {}

    def add(self, markup):
        self.svgs.append(S.svg_doc(markup, w=self.cw, h=self.ch).replace(S.BOIL_TOKEN, "1"))
        return len(self.svgs) - 1

    def load(self):
        if self.imgs is None:
            out, offs = [], []
            for svg in self.svgs:
                im = raster.rasterize(svg, self.cw, self.ch)
                if self.wc > 0:
                    im = WC.watercolor(im, seed=self.seed, strength=self.wc)
                bb = im.getchannel("A").getbbox() or (0, 0, 2, 2)
                x0, y0 = max(0, bb[0] - 2), max(0, bb[1] - 2)
                x1, y1 = min(im.width, bb[2] + 2), min(im.height, bb[3] + 2)
                out.append(im.crop((x0, y0, x1, y1)))
                offs.append((x0, y0))
            self.imgs, self.offs = out, offs
        return self.imgs

    def get(self, i, sx=1.0, sy=1.0, rot=0.0):
        """(image, anchor x, anchor y inside it)."""
        self.load()
        i = int(i)
        sx, sy = round(sx, 3), round(sy, 3)
        rot = round(rot * 2) / 2
        key = (i, sx, sy, rot)
        hit = self._c.get(key)
        if hit is not None:
            return hit
        im = self.imgs[i]
        ox, oy = self.offs[i]
        ax, ay = self.ax - ox, self.ay - oy
        if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
            w, h = im.size
            nw, nh = max(1, round(w * sx)), max(1, round(h * sy))
            im = im.resize((nw, nh), Image.BILINEAR)
            ax, ay = ax * nw / w, ay * nh / h
        if abs(rot) >= 0.25:
            w, h = im.size
            pad = int(0.3 * max(w, h)) + 4
            big = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
            big.paste(im, (pad, pad))
            im = big.rotate(-rot, resample=Image.BICUBIC, center=(ax + pad, ay + pad))
            bb = im.getchannel("A").getbbox() or (0, 0, 2, 2)
            im = im.crop(bb)
            ax, ay = ax + pad - bb[0], ay + pad - bb[1]
        if len(self._c) > 500:
            self._c.clear()
        self._c[key] = (im, ax, ay)
        return self._c[key]


def figure_spr(half_w, top, scale=SC, seed=0, foot=40, wc=1.0):
    """A canvas for one figure whose drawing spans +-half_w and up to `top` (scale-1 px) above its anchor."""
    cw = 2 * half_w * scale + 60
    ch = top * scale + foot + 50
    return Spr(cw, ch, cw / 2, ch - foot, wc=wc, seed=seed)


# ============================================================================ walking
def path_y(x):
    """The walking surface: the path, the ramp, the landing at the sill (and the hold floor inside)."""
    if x >= RBX:
        return GY
    if x <= RTX:
        return SILL
    return PR.ark_ramp_y(x, AX, GY, SC, 1)


def path_pose(x, span):
    """(anchor y, tilt) of a figure whose feet are `span` px apart, centred at x on the walking surface."""
    if span <= 0:
        return path_y(x), 0.0
    yl, yr = path_y(x - span / 2), path_y(x + span / 2)
    return (yl + yr) / 2, math.degrees(math.atan2(yr - yl, span))


class Stepper:
    """Planted strides along x: each stride the drawing changes and the anchor moves one stride in a short ease
    (and lifts a little); between strides the feet stay put. Built from a continuous plan xc(t) (cuts where the
    plan crosses each stride mark) or from explicit cut times."""

    def __init__(self, xc, t0, t1, stride, shift=0.0, mf=0.5, cut_times=None, max_move=0.22, hold=0.55):
        self.xc = xc
        if cut_times is None:
            ts = np.arange(t0, t1, 1 / 240.0)
            xs = np.array([xc(t) for t in ts])
            d = np.abs(xs - xs[0])
            marks = np.floor(d / stride + shift)
            idx = np.nonzero(np.diff(marks) > 0)[0] + 1
            cut_times = [float(ts[k]) for k in idx]
        self.cuts = list(cut_times)
        self.x0 = xc(t0)
        self.pos = [xc(c) for c in self.cuts]
        self.ms = []
        for k, c in enumerate(self.cuts):
            gaps = [g for g in ((c - self.cuts[k - 1]) if k else None,
                                (self.cuts[k + 1] - c) if k + 1 < len(self.cuts) else None) if g is not None]
            per = min(gaps) if gaps else 0.3
            self.ms.append(min(max_move, mf * per))
        self.hold = hold

    def x(self, t):
        x = self.x0
        for k, c in enumerate(self.cuts):
            m = self.ms[k]
            if t < c - 0.45 * m:
                break
            prev = self.pos[k - 1] if k else self.x0
            x = prev + (self.pos[k] - prev) * M.progress(t, c - 0.45 * m, c + 0.55 * m, "sine")
        return x

    def lift(self, t):
        """0..1 bump while a stride moves (for a little step bounce)."""
        for k, c in enumerate(self.cuts):
            m = self.ms[k]
            if c - 0.45 * m <= t <= c + 0.55 * m:
                return math.sin(math.pi * (t - c + 0.45 * m) / m)
        return 0.0

    def k(self, t):
        """Index of the current stride drawing, or None when standing (no stride for a while)."""
        j = None
        for k, c in enumerate(self.cuts):
            if c <= t:
                j = k
            else:
                break
        if j is None:
            return None
        nxt = self.cuts[j + 1] - self.cuts[j] if j + 1 < len(self.cuts) else None
        if nxt is not None and nxt <= self.hold:
            return j
        per = min(self.hold, self.cuts[j] - self.cuts[j - 1]) if j > 0 else self.hold
        return j if t - self.cuts[j] < per else None

    def moving(self, t):
        return self.k(t) is not None

    def end(self):
        return self.cuts[-1] if self.cuts else 0.0


def lin_plan(points):
    """[(t, x)] -> piecewise-linear x(t) (held before the first and after the last point)."""
    pts = sorted(points)

    def xc(t):
        if t <= pts[0][0]:
            return pts[0][1]
        for (ta, xa), (tb, xb) in zip(pts, pts[1:]):
            if t <= tb:
                return xa + (xb - xa) * (t - ta) / (tb - ta) if tb > ta else xb
        return pts[-1][1]
    return xc


# ============================================================================ door / window clipping
def make_door_clip(x0=DX0, top=DTOP, x1=DX1, sill=SILL, shade=0.5, gate_x=None):
    """Stage-space version of props.in_ark_door for a placed sprite: hidden left of the stern-side jamb and above
    the lintel; shaded as it goes into the dim hold (once its anchor is past gate_x)."""
    gate_x = (x0 + 0.52 * (x1 - x0)) if gate_x is None else gate_x

    def clip(im, left, top_, t=None, anchor=None):
        w, h = im.size
        if left >= x1 + 1:
            return im
        xs = left + np.arange(w, dtype=np.float32) + 0.5
        ys = top_ + np.arange(h, dtype=np.float32) + 0.5
        vx0 = np.clip((xs - x0) / 1.5 + 0.5, 0, 1)
        vx1 = np.clip((xs - x1) / 1.5 + 0.5, 0, 1)
        vt = np.clip((ys - top) / 1.5 + 0.5, 0, 1)
        vis = np.maximum(vx1[None, :], vx0[None, :] * vt[:, None])
        if vis.max() <= 0.003:
            return None
        arr = np.asarray(im).astype(np.float32)
        gate = 1.0 if anchor is None else clamp((gate_x - anchor) / 45.0)
        depth = np.clip((x1 - xs) / (x1 - x0), 0, 1) * (1 - vx1) * gate
        dk = (1 - shade * depth ** 0.8)[None, :] * np.ones((h, 1), np.float32)
        dk = 1 - (1 - dk) * vt[:, None]
        arr[..., :3] *= dk[..., None]
        arr[..., 3] *= vis
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return clip


def make_box_clip(box, active):
    """Keep only what is inside box (x0, y0, x1, y1) while active(t) (a bird flying in at the window)."""
    bx0, by0, bx1, by1 = box

    def clip(im, left, top_, t=None, anchor=None):
        if t is not None and not active(t):
            return im
        w, h = im.size
        xs = left + np.arange(w, dtype=np.float32) + 0.5
        ys = top_ + np.arange(h, dtype=np.float32) + 0.5
        vx = np.clip((xs - bx0) / 1.5 + 0.5, 0, 1) * np.clip((bx1 - xs) / 1.5 + 0.5, 0, 1)
        vy = np.clip((ys - by0) / 1.5 + 0.5, 0, 1) * np.clip((by1 - ys) / 1.5 + 0.5, 0, 1)
        vis = vy[:, None] * vx[None, :]
        if vis.max() <= 0.003:
            return None
        arr = np.asarray(im).astype(np.float32)
        arr[..., 3] *= vis
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return clip


# ============================================================================ actors
def squash_dip(t0, depth=0.05, dur=0.3):
    """(dy, sy) of a quick squash with its bottom at t0 (a pose cut hides there)."""
    def f(t):
        u = t - t0
        if u < -0.12 or u > dur:
            return 0.0, 1.0
        if u < 0:
            k = M.progress(u, -0.12, 0.0, "in")
            return 0.0, 1 - depth * k
        k = M.progress(u, 0.0, dur, "out")
        return 0.0, 1 - depth * (1 - k) + 0.25 * depth * math.sin(math.pi * k)
    return f


def jump_bump(t0, h, dur=0.42):
    """(dy, sy): crouch, hop up h px, land."""
    def f(t):
        u = t - t0
        if u < -0.1 or u > dur:
            return 0.0, 1.0
        if u < 0:
            return 0.0, 1 - 0.06 * M.progress(u, -0.1, 0, "sine")
        k = u / dur
        return -h * math.sin(math.pi * k), 1 + 0.05 * math.sin(math.pi * k) - 0.06 * max(0, 1 - k * 4)
    return f


class Actor:
    """A figure on a Spr. x(t); the surface gives y and tilt (span = distance between the feet); drawing = walk
    cycle while the Stepper strides, else base(t); bumps(t) -> (dy, sy); breathing while standing."""

    def __init__(self, spr, xfn, base, stepper=None, walk=(0, 1), span=0.0, yoff=0.0, bumps=(), alpha=None,
                 breathe=(0.012, 2.8, 0.0), bounce=0.0, rock=0.0, clip=None, yfn=None, rotfn=None, kshift=0,
                 surface=None, dyfn=None, scalefn=None):
        self.spr, self.xfn, self.base, self.st = spr, xfn, base, stepper
        self.walk, self.span, self.yoff, self.bumps = walk, span, yoff, list(bumps)
        self.alpha, self.breathe, self.bounce, self.rock = alpha, breathe, bounce, rock
        self.clip, self.yfn, self.rotfn, self.kshift = clip, yfn, rotfn, kshift
        self.surface = surface or path_pose
        self.dyfn, self.scalefn = dyfn, scalefn

    def state(self, t):
        a = 1.0 if self.alpha is None else self.alpha(t)
        if a <= 0.002:
            return None
        x = self.xfn(t)
        if self.yfn is not None:
            y, rot = self.yfn(t), 0.0
        else:
            y, rot = self.surface(x, self.span)
        y += self.yoff
        k = self.st.k(t) if self.st is not None else None
        if k is not None and self.walk:
            i = self.walk[(k + self.kshift) % len(self.walk)]
            lift = self.st.lift(t)
            y -= self.bounce * lift
            if self.rock:
                rot += self.rock * (1 if (k + self.kshift) % 2 else -1) * (0.4 + 0.6 * lift)
            sy = 1.0
        else:
            i = self.base(t)
            b = self.breathe
            sy = 1 + b[0] * math.sin(2 * math.pi * (t / b[1] + b[2])) if b else 1.0
        for bf in self.bumps:
            dy, s_ = bf(t)
            y += dy
            sy *= s_
        if self.dyfn is not None:
            y += self.dyfn(t)
        if self.rotfn is not None:
            rot += self.rotfn(t)
        sx = 1 + 0.5 * (1 - sy)
        if self.scalefn is not None:
            k_ = self.scalefn(t)
            sx *= k_
            sy *= k_
        return i, x, y, rot, sx, sy, a

    def __call__(self, t):
        st = self.state(t)
        if st is None:
            return None
        i, x, y, rot, sx, sy, a = st
        im, ax, ay = self.spr.get(i, sx, sy, rot)
        left, top = x - ax, y - ay
        if self.clip is not None:
            im = self.clip(im, left, top, t, x)
            if im is None:
                return None
        if a < 0.998:
            arr = np.asarray(im).copy()
            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
            im = Image.fromarray(arr, "RGBA")
        return im, (left, top)


# ============================================================================ camera
def clamp_cam(c, sw=SW, sh=SH, margin=4):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), sw - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), sh - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_at(x, w, bottom):
    return Cam(x, bottom - w * 9 / 32, w)


def cam_path(keys, sw=SW, sh=SH):
    """[(t, Cam[, curve])]: eased moves between key cameras (the bottom edge is interpolated), clamped."""
    ks = [(k[0], clamp_cam(k[1], sw, sh), k[2] if len(k) > 2 else "sine") for k in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= ks[0][0]:
            return ks[0][1]
        if t >= ks[-1][0]:
            return ks[-1][1]
        for (t0, a, cv), (t1, b, _) in zip(ks, ks[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, cv)
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w), sw, sh)
        return ks[-1][1]
    return cam


# ============================================================================ backdrop (shared with s08)
def sky_svg():
    defs = S.lin_grad("n7sky", [(0, "#86c2dd"), (0.42, "#b6dde9"), (0.68, "#e3eedc"), (0.8, "#f5ebcf"),
                                (1, "#f6e6c4")])
    defs += S.rad_grad("n7sun", [(0, "#fff6d6", 0.95), (0.3, "#fde9b0", 0.55), (1, "#fde9b0", 0)])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#n7sky)"/>'
               f'<circle cx="2980" cy="250" r="720" fill="url(#n7sun)"/>', defs)


def sun_svg():
    x, y = 2980, 250
    out = (f'<path d="{S.rays(x, y, 112, 240, 14, 8)}" fill="#fbd46b" opacity="0.5"/>'
           f'<circle cx="{x}" cy="{y}" r="92" fill="#fbcf6a" stroke="#e9a35a" stroke-width="5"/>'
           f'<circle cx="{x - 26}" cy="{y - 28}" r="24" fill="#fde7a8"/>')
    return doc(S.g(out, filter="wobble"))


CLOUDS = [[(420, 230, 420, 96, 1), (1500, 150, 340, 80, 2), (2350, 300, 380, 86, 3)],
          [(900, 420, 300, 66, 4), (1900, 470, 260, 58, 5), (3200, 120, 420, 96, 6), (-80, 120, 300, 70, 7)]]


def clouds_svg(i):
    out = ""
    for cx, cy, w, h, sd in CLOUDS[i]:
        out += S.cloud(cx, cy, w, h, fill="#fbf4e6", seed=sd, sw=3, shade_fill="#dbe5ea")
    return doc(S.g(out, filter="wobble"))


def far_svg():
    """Hazy far ridges below the hilltop (the ark's hill stands high above the plain)."""
    out = ""
    out += S.path(S.hill(-60, SW + 60, 1000, 150, seed=3, bumps=6), "#bdd3cc", sw=3)
    out += S.path(S.hill(-60, SW + 60, 1030, 90, seed=8, bumps=5), "#adc9b9", sw=3)
    rng = random.Random(4)
    for _ in range(26):
        x = rng.uniform(0, SW)
        y = rng.uniform(985, 1030)
        out += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(9, 16))}" ry="{f1(rng.uniform(7, 11))}" fill="#93b49d"/>'
    return doc(S.g(out, filter="wobble"))


def mid_svg():
    """The rolling top of the hill behind the ark: grass, olive trees, bushes."""
    defs = S.lin_grad("n7mid", [(0, "#accc80"), (1, "#97bc68")])
    out = S.path(S.hill(-80, SW + 80, 1095, 70, seed=21, bumps=4), "url(#n7mid)", sw=4)
    for x, y, s, sd in ((260, 1086, 0.42, 1), (2440, 1080, 0.36, 2), (2780, 1088, 0.4, 3), (3240, 1076, 0.34, 4),
                        (1960, 1082, 0.3, 5)):
        out += PR.olive_tree(x, y, s, seed=sd)
    for x, y, s, v in ((520, 1094, 0.5, 0), (1830, 1090, 0.42, 3), (2620, 1092, 0.45, 1), (3020, 1090, 0.5, 0)):
        out += PR.bush(x, y, s, variant=v)
    return doc(S.g(out, filter="wobble"), defs)


def ground_svg():
    """The hilltop meadow: the sandy path to the ramp, flowers, pebbles and the leftovers of the building work."""
    rng = random.Random(9)
    defs = S.lin_grad("n7gr", [(0, "#a2c466"), (0.45, "#90b858"), (1, "#7aa34a")])
    defs += S.lin_grad("n7path", [(0, "#ecd6a6"), (1, "#dcbd88")])
    defs += S.rad_grad("n7sh", [(0, "#4b3426", 0.28), (1, "#4b3426", 0)])
    out = S.path(S.wave_band(1112, 10, 1300, 0.4, x0=-60, x1=SW + 60, bottom=SH + 60, seed=2), "url(#n7gr)", sw=4)
    # the ark's soft shadow on the grass
    out += f'<ellipse cx="{AX + 40}" cy="{GY + 8}" rx="620" ry="34" fill="url(#n7sh)"/>'
    # the sandy path: from the right edge to the foot of the ramp (and a worn patch under the ramp)
    top = [(RBX - 120, GY - 18), (RBX + 200, GY - 24), (2300, GY - 26), (2900, GY - 22), (SW + 60, GY - 28)]
    bot = [(SW + 60, GY + 32), (2900, GY + 30), (2300, GY + 34), (RBX + 200, GY + 30), (RBX - 120, GY + 22)]
    d = S.smooth_path(top, closed=False) + " L" + " L".join(f"{f1(x)},{f1(y)}" for x, y in bot[:1])
    d += " " + S.smooth_path(bot, closed=False).replace("M", "L", 1) + " Z"
    out += f'<path d="{d}" fill="url(#n7path)" stroke="{S.shade("#dcbd88", -0.25)}" stroke-width="3" opacity="0.95"/>'
    for _ in range(46):
        x = rng.uniform(RBX - 60, SW)
        y = rng.uniform(GY - 14, GY + 22)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(5, 11))}" ry="{f1(rng.uniform(3, 5))}" '
                f'fill="#c9a874" opacity="0.75"/>')
    # meadow flowers and pebbles (not on the path)
    for _ in range(95):
        x = rng.uniform(-20, SW + 20)
        y = rng.uniform(1120, 1148) if rng.random() < 0.45 else rng.uniform(1215, 1385)
        if RBX - 80 < x < SW and GY - 40 < y < GY + 40:
            continue
        if rng.random() < 0.18:
            out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(8, 14))}" ry="{f1(rng.uniform(5, 8))}" '
                    f'fill="#d8cdb6" stroke="{INK}" stroke-width="2.2"/>')
            continue
        c = rng.choice(("#f6e27a", "#fff3d6", "#f0998a", "#c9a7e0", "#f6e27a"))
        r = rng.uniform(4.5, 8)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{c}" stroke="{INK}" stroke-width="2"/>'
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.35)}" fill="#e9a35a"/>'
    # leftovers of the building work at the stern (continuity with s06)
    out += PR.timber_pile(250, GY + 6, 0.62, 1, kind="planks")
    out += PR.sawhorse(470, GY + 20, 0.55, 1, plank=False)
    out += PR.pitch_bucket(560, GY + 26, 0.5, 1)
    out += PR.plank(350, GY + 40, 0.6, rot=6)
    out += PR.hay(3180, GY - 2, 0.62, 1, kind="bale")
    out += PR.grass_tuft(3330, GY + 30, 0.9, variant=0) + PR.grass_tuft(2470, GY + 44, 0.8, variant=2)
    return doc(S.g(out, filter="wobble"), defs)


def ark_svg(door=1.0, window=1.0, glow=0.0, wet=False):
    return doc(PR.ark(AX, GY, SC, 1, door=door, window=window, glow=glow, wet=wet))


BUSH = (1560, GY + 50, 0.72)


def bush_svg(k=0):
    x, y, s = BUSH
    return doc(PR.bush(x, y, s, variant=1) + PR.grass_tuft(x - 70, y + 6, 0.7, variant=0, sway=0.3 * (k - 1)) +
               PR.grass_tuft(x + 80, y + 8, 0.6, variant=2, sway=0.3 * (1 - k)))


FG_TUFTS = [(30, 1395, 1.35, 0), (260, 1392, 1.1, 2), (700, 1398, 1.2, 0), (1150, 1396, 1.0, 2), (1480, 1398, 1.15, 0),
            (1900, 1396, 1.0, 2), (2350, 1398, 1.2, 0), (2700, 1392, 1.0, 2), (3050, 1398, 1.25, 0), (3330, 1394, 1.1, 2),
            (520, 1396, 0.9, 1), (2550, 1398, 0.9, 1)]


def fg_svg(k):
    out = ""
    for x, y, s, v in FG_TUFTS:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.5 * math.sin(k * 2.1 + x * 0.013))
    return doc(out)


def add_backdrop(sc, toff=0.0, ark=True):
    """Sky, sun, clouds, hills, meadow (+ the ark, door open). toff shifts the cyclic clocks (s08 continues s07)."""
    sc.add("sky", sky_svg(), z=0, wc=0.45)
    sc.add("sun", sun_svg(), z=0.1, wc=0.3, motion=M.breathe(0.012, 4.0, pivot=(2980, 250)))
    for i, v in enumerate((7.0, 4.5)):
        sc.add(f"clouds{i}", clouds_svg(i), z=0.2 + 0.05 * i, wc=0.6,
               motion=lambda t, v=v: Tf(dx=-v * (t + toff)))
    sc.add("far", far_svg(), z=1, wc=0.7)
    sc.add("mid", mid_svg(), z=1.5)
    sc.add("ground", ground_svg(), z=2)
    if ark:
        sc.add("ark", ark_svg(), z=3)


def add_foreground(sc, toff=0.0):
    sc.add("bush", [bush_svg(k) for k in range(3)], z=40, frame_at=lambda t: float(int((t + toff) * 2.0) % 3))
    sc.add("fg", [fg_svg(k) for k in range(3)], z=60, frame_at=lambda t: float(int((t + toff) * 2.2) % 3))


BUTTERFLIES = [  # colour, centre of its loop, loop radii, period, phase
    ("orange", (2560, 1040), (120, 40), 7.0, 0.0),
    ("yellow", (760, 1060), (90, 50), 6.0, 0.4),
    ("pink", (2980, 1120), (100, 36), 8.0, 0.7),
]


def add_butterflies(sc, z=45, toff=0.0, alpha=None):
    for i, (col, (cx, cy), (rx, ry), per, ph) in enumerate(BUTTERFLIES):
        fr = [doc(PR.butterfly(cx, cy, 0.42, flap=f, color=col)) for f in (0.0, 0.25, 0.5, 0.75)]

        def mv(t, cx=cx, cy=cy, rx=rx, ry=ry, per=per, ph=ph):
            u = 2 * math.pi * ((t + toff) / per + ph)
            a = 1.0 if alpha is None else alpha(t)
            return Tf(dx=rx * math.sin(u), dy=ry * math.sin(2 * u) * 0.6 - 10 * math.sin(u * 3), alpha=a,
                      rot=8 * math.cos(u), px=cx, py=cy)
        sc.add(f"bfly{i}", fr, z=z, wc=0.4, frame_at=lambda t, i=i: float(int((t + toff) * 14 + i) % 4), motion=mv)


# ============================================================================ the animals
#            half-width, top, foot span, stride, shadow width (all scale-1 px, the shadow at the figure's scale)
KIND = {
    "elephant": (330, 560, 290, 175, 330),
    "giraffe": (300, 720, 220, 205, 230),
    "zebra": (210, 370, 200, 150, 220),
    "horse": (230, 400, 215, 160, 230),
    "hippo": (260, 250, 250, 130, 300),
    "deer": (200, 420, 190, 150, 200),
    "fox": (200, 210, 160, 120, 190),
    "monkey": (110, 210, 50, 80, 110),
    "duck": (100, 140, 40, 60, 100),
    "sheep": (130, 180, 120, 100, 150),
    "cow": (220, 250, 210, 130, 240),
    "turtle": (130, 110, 120, 70, 160),
    "lion": (200, 360, 210, 150, 240),
    "rabbit": (120, 260, 80, 0, 110),
}
# pair extents (front, rear) of the male anchor, facing left, at scale 0.6 (measured from renders)
EXT = {"elephant": (-256, 138), "lion": (-195, 111), "rabbit": (-68, 42), "giraffe": (-188, 90), "zebra": (-173, 89),
       "horse": (-187, 100), "hippo": (-226, 127), "deer": (-161, 83), "fox": (-131, 115), "monkey": (-62, 57),
       "duck": (-84, 44), "sheep": (-118, 60), "cow": (-187, 86), "turtle": (-111, 60)}
WALKS = ("walk_a", "walk_b")


def animal_markup(kind, female, x, y, facing=-1, pose="stand", eyes="open", phase=0.0, shadow=True):
    """One animal of a pair (the female 0.96x with her bow) + its ground shadow, anchor (x, y)."""
    s = SC * (0.96 if female else 1.0)
    sh = C.ground_shadow(x, y, s * (0.8 if kind == "lion" else 1.0), KIND[kind][4], 0.2) if shadow else ""
    return sh + PR._one(kind, x, y, s, facing, pose, female, eyes, phase)


def animal_spr(kind, female, seed, poses=WALKS + ("stand",), facing=-1, extra=()):
    hw, top = KIND[kind][0], KIND[kind][1]
    sp = figure_spr(hw, top, seed=seed)
    idx = {}
    for p in poses:
        idx[p] = sp.add(animal_markup(kind, female, sp.ax, sp.ay, facing, p))
    for name, markup_fn in extra:
        idx[name] = sp.add(markup_fn(sp.ax, sp.ay))
    return sp, idx


def pair_gap(kind):
    return PR._PAIR_DX[kind] * SC


# ============================================================================ Noah and the family
def fam_markup(name, x, y, pose, facing=-1, expr=None, phase=0.0, shadow=True):
    kw = dict(pose=pose, expr=expr, phase=phase)
    if pose.startswith("carry"):
        kw["item"] = FAM_ITEMS.get(name, "sack")
    out = C.ground_shadow(x, y, SC, 120, 0.2) if shadow else ""
    return out + C.family_member(name, x, y, SC, facing, **kw)


def person_spr(seed, hw=190, top=400):
    return figure_spr(hw, top, seed=seed, foot=36)


def family_sprites(names=FAM_ORDER[:-1], extra_poses=()):
    """name -> (Spr, {pose: idx}) with carry_walk_a / carry_walk_b / carry (+ extra (pose, facing, expr))."""
    out = {}
    for k, nm in enumerate(names):
        sp = person_spr(70 + k)
        idx = {p: sp.add(fam_markup(nm, sp.ax, sp.ay, p)) for p in ("carry_walk_a", "carry_walk_b", "carry")}
        idx["blink"] = sp.add(fam_markup(nm, sp.ax, sp.ay, "carry", expr=blink_expr("happy")))
        for p, f, e in extra_poses:
            idx[(p, f, e)] = sp.add(fam_markup(nm, sp.ax, sp.ay, p, f, e))
        out[nm] = (sp, idx)
    return out


def blink_expr(e):
    name = f"n7_blink_{e}"
    C.EXPRS.setdefault(name, dict(C.EXPRS[e], eyes="closed"))
    return name


# ============================================================================ little overlays
def dust_markup(cx, cy, w, seed=0, col="#efe0bf"):
    rng = random.Random(seed)
    out = ""
    for i in range(3):
        px = cx + (i - 1) * w * 0.36 + rng.uniform(-5, 5)
        py = cy - rng.uniform(0, 10)
        sz = rng.uniform(40, 54) * w / 120
        out += S.cloud(px, py, sz, sz * 0.58, col, seed=seed * 11 + i, puffs=3, sw=2.2, shade_fill="#dcc79c")
    return S.g(out, filter="wobble-fine", opacity=0.92)


def impact_lines(cx, cy, w, k=1.0):
    """Short 'thump' strokes fanning up from a foot."""
    out = ""
    for a in (-160, -125, -55, -20):
        r = math.radians(a)
        x0, y0 = cx + w * 0.55 * math.cos(r), cy + w * 0.4 * math.sin(r)
        x1, y1 = cx + w * 0.95 * math.cos(r), cy + w * 0.75 * math.sin(r)
        out += (f'<path d="M{f1(x0)},{f1(y0)} L{f1(x1)},{f1(y1)}" stroke="{P["ink_soft"]}" stroke-width="{4.5 * k:.1f}" '
                f'stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def heart_markup(x, y, r, fill="#ef8c95"):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.2)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.2)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} "
         f"{f1(x)},{f1(y + r * 0.9)} Z")
    return S.g(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{max(2.5, r * 0.15):.1f}" '
               f'stroke-linejoin="round"/><ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.3)}" '
               f'rx="{f1(r * 0.18)}" ry="{f1(r * 0.12)}" fill="#fbd0c4"/>', filter="wobble-fine")


def fluff_markup(cx, cy, r, k=1.0, col=None):
    """Mane-fluff strokes around a roaring lion's head."""
    col = col or "#c7652e"
    out = ""
    for i in range(10):
        a = math.radians(-200 + i * 26 + (6 if k > 1 else 0))
        x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
        x1, y1 = cx + (r + 26 * k) * math.cos(a), cy + (r + 26 * k) * math.sin(a)
        out += (f'<path d="M{f1(x0)},{f1(y0)} Q{f1((x0 + x1) / 2 + 6 * math.sin(a))},{f1((y0 + y1) / 2 - 6 * math.cos(a))} '
                f'{f1(x1)},{f1(y1)}" stroke="{col}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def flap_marks(x, y, facing=-1, k=1.0):
    """Two little 'flap' arcs above / below a bird's wings."""
    out = ""
    for dy, sgn in ((-30, -1), (22, 1)):
        x0 = x + facing * -10
        out += (f'<path d="M{f1(x0 - 26)},{f1(y + dy)} Q{f1(x0)},{f1(y + dy + sgn * 14 * k)} {f1(x0 + 26)},{f1(y + dy)}" '
                f'stroke="#fffaf0" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.9"/>')
        out += (f'<path d="M{f1(x0 - 26)},{f1(y + dy)} Q{f1(x0)},{f1(y + dy + sgn * 14 * k)} {f1(x0 + 26)},{f1(y + dy)}" '
                f'stroke="{P["ink_soft"]}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    return out


def bezier(p0, p1, p2, p3, u):
    a = (1 - u) ** 3
    b = 3 * (1 - u) ** 2 * u
    c = 3 * (1 - u) * u * u
    d = u ** 3
    return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def pop_scale(t, t0, t1, dur_in=0.3, dur_out=0.35):
    """(scale, alpha) of a pop-in at t0 with overshoot, a fade-up-and-out at t1."""
    if t < t0 or t > t1 + dur_out:
        return 0.0, 0.0
    if t < t1:
        return max(0.02, M.ease("back")(clamp((t - t0) / dur_in))), 1.0
    u = (t - t1) / dur_out
    return 1 + 0.2 * u, 1 - u


# ============================================================================ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]

    # ---------------- beats
    t_come = pt(ctx, 0, "来了")
    t_ele = pt(ctx, 1, "大象")
    t_dong = [pt(ctx, 1, "咚", k) for k in range(3)]
    t_bird = pt(ctx, 1, "小鸟")
    t_pu = [pt(ctx, 1, "扑", k) for k in range(3)]
    t_lion = pt(ctx, 1, "狮子")
    t_roar = pt(ctx, 1, "嗷呜")
    t_rab = pt(ctx, 1, "小兔子")
    t_beng = [pt(ctx, 1, "蹦", k) for k in range(3)]
    t_pairs = pt(ctx, 2, "两个两个")
    t_mf = pt(ctx, 2, "一公一母")
    t_line = pt(ctx, 2, "排着队")
    t_food = pt(ctx, 3, "挪亚还在")
    t_people = pt(ctx, 3, "有人吃的")
    t_animals_eat = pt(ctx, 3, "也有动物")

    # ---------------- the queue plan: Q(tau) = front of the elephant pair; everybody behind the lion waits while
    # he roars (tau runs slower for them)
    V = 290.0
    Q_D3 = RBX + 20                      # elephant front at the third 咚 (at the foot of the ramp)
    t_stop = t_roar - 0.42
    t_go = t_roar + 0.95

    def Q(tau):
        return Q_D3 - V * (tau - t_dong[2])

    def tau_wait(t):
        return t - clamp(t - t_stop, 0, t_go - t_stop)

    GAP = 26
    order = ["elephant", "giraffe", "zebra", "lion", "rabbit", "hippo", "monkey", "horse", "duck", "deer", "sheep",
             "cow", "fox", "turtle"]
    gaps = {"lion": 62, "rabbit": 60}
    offs, o = {}, 0.0
    for kd in order:
        offs[kd] = o
        fe, re_ = EXT[kd]
        o += (re_ - fe) + gaps.get(kd, GAP)
    waits = set(order[order.index("lion"):])

    def front_x(kd, t):
        tau = tau_wait(t) if kd in waits else t
        return Q(tau) + offs[kd]

    def anchor_plan(kd, t):
        return front_x(kd, t) - EXT[kd][0]

    X_IN = DX0 - 420                      # far enough inside to be hidden

    # turtles: on the conveyor to the foot of the ramp, then slower up it
    t_turtle_foot = None
    for k in range(4000):
        tt = 10 + k * 0.01
        if front_x("turtle", tt) <= RBX:
            t_turtle_foot = tt
            break
    V_T = 150.0

    def turtle_plan(t):
        if t <= t_turtle_foot:
            return anchor_plan("turtle", t)
        return anchor_plan("turtle", t_turtle_foot) - V_T * (t - t_turtle_foot)

    # ---------------- camera
    BOT = SH - 2
    CW = cam_at(1640, 2480, BOT)
    CE1 = cam_at(1980, 1950, BOT - 8)
    CB = cam_at(1560, 2250, BOT - 4)
    CL = cam_at(1790, 1820, BOT - 10)
    CQ = cam_at(2150, 2480, BOT)
    CQ2 = cam_at(1980, 2400, BOT)
    CR = cam_at(1830, 1900, BOT - 8)
    CEND = cam_at(1700, 1760, BOT - 10)
    t_end_pos = L3.end - 0.25
    base_cam = cam_path([(0, CW), (max(1.4, t_come + 0.2), CW), (t_ele + 0.15, CE1), (t_bird - 0.25, CE1),
                         (t_bird + 0.75, CB), (t_lion - 0.35, CB), (t_lion + 0.65, CL), (L2.start - 0.35, CL),
                         (L2.start + 1.25, CQ), (t_line, CQ), (L3.start - 0.2, CQ2), (L3.start + 1.4, CR),
                         (t_animals_eat, CR), (t_end_pos, CEND), (T, CEND)])

    def thump(t):
        v = 0.0
        for td in t_dong:
            u = t - td
            if 0 <= u <= 0.3:
                v += 6.0 * math.exp(-u / 0.07) * math.sin(2 * math.pi * u / 0.12)
        return v

    def camera(t):
        c = base_cam(t)
        return Cam(c.x, c.y + thump(t), c.w)
    sc.camera = camera

    # ---------------- backdrop
    add_backdrop(sc)
    add_foreground(sc)
    add_butterflies(sc)
    door_clip = make_door_clip()

    # ---------------- the animal queue
    z0 = 20.0
    actors = {}
    for qi, kd in enumerate(order):
        if kd == "rabbit":
            continue
        hw, top, span, stride, shw = KIND[kd]
        stride *= SC
        span *= SC
        gap = pair_gap(kd)
        plan = turtle_plan if kd == "turtle" else (lambda t, kd=kd: anchor_plan(kd, t))
        for female in (True, False):
            dxf = -gap if female else 0.0
            yo = -18 * SC if female else 0.0
            xc = (lambda t, plan=plan, dxf=dxf: plan(t) + dxf)
            if kd == "elephant":
                pe = (t_dong[2] - t_dong[0]) / 2
                cts = [t_dong[0] - pe * k for k in range(16, 0, -1)] + list(t_dong)
                k = 1
                while t_dong[2] + pe * k < 11.0:
                    cts.append(t_dong[2] + pe * k)
                    k += 1
                st = Stepper(xc, -6.0, T + 0.5, stride, cut_times=cts, mf=0.55)
            else:
                st = Stepper(xc, -6.0, T + 0.5, stride, shift=0.5 if female else 0.0, mf=0.55)
            zz = z0 - qi * 0.1 - (0.05 if female else 0.0)
            if kd == "lion":
                act = lion_actor(st, female, span, yo, door_clip, t_stop, t_roar, t_go, seed=200 + qi)
                sc.add_dynamic(f"{kd}{'_f' if female else ''}", act, z=zz)
                actors[(kd, female)] = act
                continue
            poses = {"cow": ("stand",), "giraffe": WALKS + ("stand", "bow")}.get(kd, WALKS + ("stand",))
            sp, idx = animal_spr(kd, female, seed=100 + qi * 7 + (3 if female else 0), poses=poses)
            walk = (idx["walk_a"], idx["walk_b"]) if "walk_a" in idx else (idx["stand"], idx["stand"])
            base = (lambda t, s_=idx["stand"]: s_)
            bumps = [squash_dip(td + 0.02, 0.045, 0.32) for td in t_dong] if kd == "elephant" else []
            act = Actor(sp, st.x, base, stepper=st, walk=walk, span=span, yoff=yo, bumps=bumps,
                        bounce=(5 if kd in ("duck", "monkey", "sheep") else 3) * SC,
                        rock=(2.6 if kd == "cow" else 3.5 if kd == "duck" else 0.0), clip=door_clip,
                        breathe=(0.012, 2.4 + 0.3 * (qi % 3), 0.17 * qi))
            if kd in ("giraffe", "elephant"):
                act.state = door_duck(act.state, st, kd, idx.get("bow"))
            sc.add_dynamic(f"{kd}{'_f' if female else ''}", act, z=zz)
            actors[(kd, female)] = act

    # ---------------- rabbits (from the bush, hopping into the gap behind the lions)
    add_rabbits(sc, ctx, t_rab, t_beng, lambda t: anchor_plan("rabbit", t), door_clip, z=z0 + 0.6)

    # ---------------- the lion's roar overlays
    lion_x = actors[("lion", False)].xfn(t_roar)
    head = (lion_x - 150 * SC * 0.8, GY - 240 * SC * 0.8)
    mouth = (head[0] - 70 * SC * 0.8, head[1] + 40 * SC * 0.8)
    sc.add("roar_arcs", [doc(arcs_markup(mouth[0] - 8, mouth[1], -1, k, 1.5)) for k in (1, 2, 3)], z=z0 + 1, wc=0,
           frame_at=lambda t: float(int(t * 9) % 3),
           motion=lambda t: Tf(alpha=1.0 if t_roar + 0.02 <= t < t_roar + 0.75 else 0.0))
    sc.add("roar_fluff", [doc(fluff_markup(head[0], head[1], 62, k)) for k in (1.0, 1.35)], z=z0 - 0.35, wc=0.3,
           frame_at=lambda t: float(int(t * 10) % 2),
           motion=lambda t: Tf(alpha=1.0 if t_roar + 0.02 <= t < t_roar + 0.7 else 0.0))

    # ---------------- elephant stomp dust
    for k, td in enumerate(t_dong):
        xm = actors[("elephant", False)].xfn(td + 0.2)
        xf = actors[("elephant", True)].xfn(td + 0.2)
        body = ""
        for xx, yy in ((xm - 125 * SC, GY), (xm + 120 * SC, GY), (xf - 125 * SC, GY - 11), (xf + 120 * SC, GY - 11)):
            body += dust_markup(xx, yy + 4, 70, seed=k * 5 + int(xx) % 7)
        body += impact_lines(xm - 125 * SC, GY - 4, 70) + impact_lines(xm + 120 * SC, GY - 4, 70)
        piv = (xm, GY)
        sc.add(f"dust{k}", doc(body), z=z0 + 0.5, wc=0.3,
               motion=M.keys([(td - 0.02, {"alpha": 0, "s": 0.7}), (td + 0.04, {"alpha": 1, "s": 0.95}),
                              (td + 0.22, {"alpha": 0.8, "s": 1.08, "dy": -8}),
                              (td + 0.55, {"alpha": 0, "s": 1.18, "dy": -18})], ["out", "sine", "in"], pivot=piv))

    # ---------------- songbirds into the high window
    add_birds(sc, t_bird, t_pu, z=z0 + 3)

    # ---------------- hearts at 一公一母
    t_h = t_mf + 0.15
    cam_h = base_cam(t_h + 0.3)
    xlo, xhi = cam_h.x - cam_h.w / 2 + 120, cam_h.x + cam_h.w / 2 - 120
    hsp = Spr(80, 80, 40, 40, wc=0.3, seed=7)
    hsp.add(heart_markup(40, 40, 22))
    nh = 0
    for kd in order:
        if kd in ("rabbit",) or (kd, False) not in actors:
            continue
        xm = actors[(kd, False)].xfn(t_h)
        if not (max(xlo, RBX + 60) < xm < xhi):
            continue
        top_k = KIND[kd][1] * SC * (0.55 if kd == "giraffe" else 0.9)
        t0 = t_h + 0.16 * nh

        def hpos(t, kd=kd, t0=t0, top_k=top_k):
            xm_ = actors[(kd, False)].xfn(t)
            xf_ = xm_ - pair_gap(kd)
            u = max(0.0, t - t0)
            return (xm_ + xf_) / 2 - 20 * SC, GY - top_k - 50 - 26 * u

        def hstate(t, t0=t0, hpos=hpos):
            s_, a_ = pop_scale(t, t0, t0 + 1.0)
            if a_ <= 0:
                return None
            x, y = hpos(t)
            im, ax, ay = hsp.get(0, s_, s_, 6 * math.sin(6 * (t - t0)))
            if a_ < 0.998:
                arr = np.asarray(im).copy()
                arr[..., 3] = (arr[..., 3].astype(np.float32) * a_).astype(np.uint8)
                im = Image.fromarray(arr, "RGBA")
            return im, (x - ax, y - ay)
        sc.add_dynamic(f"heart{nh}", hstate, z=z0 + 2)
        sc.sfx("pop", t0, gain_db=-15 + nh * 0.5, pan=clamp((xm - cam_h.x) / cam_h.w * 1.6, -0.8, 0.8))
        nh += 1
        if nh >= 4:
            break

    # ---------------- Noah's family carrying food (line 3) - they stop in a line on the ramp
    fam = family_sprites()
    t_fam_stop = L3.end - 0.15
    FSTEP = 51.0
    FPER = 0.25
    for k, nm in enumerate(FAM_ORDER[:-1]):
        sp, idx = fam[nm]
        x_end = FAM_END[nm]
        x_start = x_end + (3600 - FAM_FRONT)
        n = int(round((x_start - x_end) / FSTEP))
        step = (x_start - x_end) / n
        t_start = snap(t_fam_stop - n * FPER)
        cts = [t_start + j * FPER for j in range(n)]
        xc = lin_plan([(t_start - 0.2, x_start), (t_fam_stop, x_end)])
        st = Stepper(lambda t, xc=xc: xc(t), t_start - 0.2, T, step, cut_times=cts, mf=0.6, max_move=0.15)
        st.pos = [x_start - step * (j + 1) for j in range(n)]
        st.x0 = x_start
        t_hold = cts[-1] + FPER
        bl = [t_hold + 0.9 + 0.13 * k] if t_hold + 1.2 + 0.13 * k < T - 0.3 else []
        base = cuts([(0, idx["carry"])] + sum([[(snap(b), idx["blink"]), (snap(b + 0.13), idx["carry"])] for b in bl], []))
        act = Actor(sp, st.x, base, stepper=st, walk=(idx["carry_walk_a"], idx["carry_walk_b"]), span=26 * SC,
                    bounce=6 * SC, clip=door_clip, kshift=k % 2, breathe=(0.010, 2.9, 0.21 * k),
                    bumps=[squash_dip(snap(t_hold), 0.04, 0.3)])
        st.hold = FPER * 1.4
        sc.add_dynamic(f"fam_{nm}", act, z=z0 - 2.0 - 0.1 * k)

    # ---------------- Noah
    add_noah_s07(sc, ctx, dict(t_come=t_come, t_dong=t_dong, t_roar=t_roar, t_rab=t_rab, t_pairs=t_pairs,
                               t_line=t_line, t_food=t_food, t_people=t_people, t_end=t_fam_stop), z=z0 + 4)

    # ---------------- sound
    sc.sfx("birds", 0.0, dur=T, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-24, fade_in=0.8, fade_out=1.0)
    for k, td in enumerate(t_dong):
        sc.sfx("thud", td, gain_db=-5 + k, pan=0.15, duck_db=-3)
    sc.sfx("footsteps", t_ele - 0.3, dur=t_dong[0] - t_ele + 0.2, gain_db=-22, pan=0.3)
    for k, tp in enumerate(t_pu):
        sc.sfx("whoosh", tp - 0.05, gain_db=-15 + k, pan=-0.4)
    sc.sfx("whoosh", t_roar, gain_db=-14, pan=0.1)
    for k, tb in enumerate(t_beng):
        sc.sfx("pop", tb, gain_db=-11 + k, pan=0.05)
    sc.sfx("footsteps", L2.start - 0.4, dur=L3.end - L2.start, gain_db=-21, fade_in=0.6, fade_out=0.6)
    sc.sfx("cloth", t_food + 0.4, gain_db=-16, pan=0.3)
    return sc


def door_duck(orig, st, kd, bow_idx):
    """Giraffes switch to the bowing drawing on the landing (little dips per stride); elephants and giraffes squash a
    touch to fit under the lintel."""
    lim = DX1 + (230 if kd == "elephant" else 60) * SC

    def state(t):
        s_ = orig(t)
        if s_ is None:
            return None
        i, x, y, rot, sx, sy, a = s_
        if kd == "giraffe" and x <= RTX + 30:
            i = bow_idx
            if st.k(t) is not None:
                sy *= 1 - 0.035 * st.lift(t)
        if x < lim:
            sy *= 1 - 0.07 * clamp((lim - x) / 110)
        return i, x, y, rot, sx, sy, a
    return state


# ============================================================================ the lion pair
def lion_actor(st, female, span, yoff, clip, t_stop, t_roar, t_go, seed=0):
    """The lion / lioness: walk, stop, a playful roar on 嗷呜 (mouth opens wide, eyes shut, a little rear-up and
    shake), walk on."""
    ls = SC * 0.8 * (0.96 if female else 1.0)
    sp = figure_spr(260, 420, scale=ls, seed=seed)
    sh = C.ground_shadow(sp.ax, sp.ay, ls, 230, 0.2)
    if female:
        fr = [sp.add(sh + PR._one("lion", sp.ax, sp.ay, SC * 0.96, -1, p, True, e, 0.0)) for p, e in
              (("walk_a", "open"), ("walk_b", "open"), ("stand", "open"), ("stand", "happy"))]
    else:
        fr = [sp.add(sh + PR.lion(sp.ax, sp.ay, ls, -1, pose=p, mouth=m, eyes=e, tail=tl)) for p, m, e, tl in
              (("walk_a", 0, "open", 0), ("walk_b", 0, "open", 0), ("stand", 0, "open", 0),
               ("stand", 0.4, "closed", 0.6), ("stand", 0.8, "closed", 1.0), ("stand", 1.0, "closed", 1.0),
               ("stand", 0, "happy", 0.3))]
    if female:
        base = cuts([(0, fr[2]), (snap(t_roar + 0.15), fr[3]), (snap(t_go - 0.05), fr[2])])
        bumps = [squash_dip(snap(t_roar + 0.15), 0.03, 0.3)]
        rotfn = None
    else:
        r0 = snap(t_roar - 0.06)
        base = cuts([(0, fr[2]), (r0, fr[3]), (snap(r0 + 0.07), fr[4]), (snap(r0 + 0.14), fr[5]),
                     (snap(t_roar + 0.62), fr[4]), (snap(t_roar + 0.69), fr[6]), (snap(t_go - 0.05), fr[2])])
        bumps = [jump_bump(r0, 6 * SC, 0.3)]

        def rotfn(t):
            u = t - r0
            if 0 <= u <= 0.7:
                return 1.6 * math.sin(2 * math.pi * u * 9) * (1 - u / 0.7)
            return 0.0
    return Actor(sp, st.x, base, stepper=st, walk=(fr[0], fr[1]), span=span, yoff=yoff, bumps=bumps, clip=clip,
                 rotfn=rotfn, bounce=3 * SC, breathe=(0.012, 2.6, 0.3 if female else 0.0))


# ============================================================================ the rabbits
def add_rabbits(sc, ctx, t_rab, t_beng, plan, clip, z):
    """Two rabbits peek out of the bush, hop out along the grass in front of the path, then - one hop on each 蹦 -
    bound into their place in the queue (behind the lions) and on up the ramp and in."""
    bx = BUSH[0]
    y_grass = GY + 40
    for female in (False, True):
        sd = 300 + (5 if female else 0)
        sp = figure_spr(130, 300, seed=sd)
        s_ = SC * (0.96 if female else 1.0)

        def mk(pose, facing, ph=0.0, shadow=True):
            sh = C.ground_shadow(sp.ax, sp.ay, s_, 100, 0.2) if shadow and pose != "hop" else ""
            if pose == "hop" and ph < 0.1:
                sh = C.ground_shadow(sp.ax, sp.ay, s_, 100, 0.2)
            return sh + PR.ark_animal(sp.ax, sp.ay, s_, facing, "rabbit", pose, female, "open", ph)
        hop_r = [sp.add(mk("hop", 1, ph)) for ph in (0.0, 0.25, 0.5, 0.75)]
        hop_l = [sp.add(mk("hop", -1, ph)) for ph in (0.0, 0.25, 0.5, 0.75)]
        stand_r = sp.add(mk("stand", 1))
        stand_l = sp.add(mk("stand", -1))
        dt = 0.07 if female else 0.0
        dxf = -pair_gap("rabbit") if female else 0.0
        yo = -18 * SC if female else 0.0
        # the hop list: (t0, dur, x0, x1, y-off 0, y-off 1, facing, extra height)
        hops = []
        x = bx - 40 + (30 if female else 0)
        t = t_rab + 0.2
        for k in range(3):                                 # out of the bush, along the grass
            hops.append((t + k * 0.29, 0.27, x + k * 62, x + (k + 1) * 62, 40, 40, 1, 6))
        xa = x + 3 * 62
        tb0 = t_beng[0]
        t_turn = (hops[-1][0] + hops[-1][1] + tb0 - 0.14) / 2
        hops.append((t_turn, 0.16, xa, xa + 6, 40, 40, -1, 4))  # a little turning hop
        beat_dt = [t_beng[1] - t_beng[0], t_beng[2] - t_beng[1]]
        per = sum(beat_dt) / 2
        tq = [t_beng[0], t_beng[1], t_beng[2]]
        k = 1
        while tq[-1] + per < tq[0] + 4.0:
            tq.append(t_beng[2] + per * k)
            k += 1
        prev_x, prev_y = xa + 6, 40
        for j, th in enumerate(tq):
            x_to = plan(th + per * 0.8) + dxf
            y_to = 0
            hops.append((th - 0.07, per * 0.95, prev_x, x_to, prev_y, y_to, -1, 30 if j < 3 else 10))
            prev_x, prev_y = x_to, 0
        hops = [(h[0] + dt,) + h[1:] for h in hops]

        def state_xy(t, hops=hops, yo=yo):
            if t < hops[0][0]:
                return hops[0][2], hops[0][4], 1, None, 0.0
            last = hops[0]
            for h in hops:
                t0, du, x0, x1, y0, y1, fc, hh = h
                if t0 <= t < t0 + du:
                    u = (t - t0) / du
                    k = clamp((u - 0.18) / 0.62)
                    e = M.ease("sine")(k)
                    return x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, fc, u, hh * math.sin(math.pi * k)
                if t >= t0 + du:
                    last = h
            return last[3], last[5], last[6], None, 0.0

        def frame_of(u, fc):
            seq = hop_r if fc > 0 else hop_l
            if u < 0.18:
                return seq[0]
            if u < 0.36:
                return seq[1]
            if u < 0.74:
                return seq[2]
            return seq[3]
        t_peek = t_rab - 0.1 + dt

        def rstate(t, sp=sp, state_xy=state_xy, frame_of=frame_of, stand_r=stand_r, stand_l=stand_l, yo=yo,
                   t_peek=t_peek):
            if t < t_peek:
                return None
            x, yoff, fc, u, hh = state_xy(t)
            if yoff > 0:
                y, rot = GY + yoff, 0.0
            else:
                y, rot = path_pose(x, KIND["rabbit"][2] * SC)
            y += yo * (1 - yoff / 40) - hh
            if u is None:
                i = stand_r if fc > 0 else stand_l
                y_peek = 0.0
                if t < hops[0][0]:
                    y_peek = 60 * (1 - M.progress(t, t_peek, t_peek + 0.25, "out"))
                b = 1 + 0.015 * math.sin(2 * math.pi * t / 1.3)
                im, ax, ay = sp.get(i, 1, b, 0)
                y += y_peek
            else:
                i = frame_of(u, fc)
                im, ax, ay = sp.get(i, 1, 1, rot)
            left, top = x - ax, y - ay
            im = clip(im, left, top, t)
            if im is None:
                return None
            return im, (left, top)
        sc.add_dynamic(f"rabbit{'_f' if female else ''}", rstate, z=(z if yo == 0 else z - 0.02) if True else z)
        # (while they are in the grass in front of the path they are drawn in front of the queue)
    return None


# ============================================================================ the songbirds
BIRD_COLS = ("blue", "red", "yellow")


def add_birds(sc, t_bird, t_pu, z):
    """Three songbird pairs fly in from the upper left; the lead pair beats its wings hard on each 扑 (a lift and
    two little flap arcs) and they all swoop in at the open high window (shrinking, dimming, clipped to it)."""
    wx = (WBOX[0] + WBOX[2]) / 2
    wy = (WBOX[1] + WBOX[3]) / 2 + 6
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = [0, 1, 2, 3, 4, 3, 2, 1]
    box = (WBOX[0] + 4, WBOX[1] + 4, WBOX[2] - 4, WBOX[3] - 2)
    in_clip = make_box_clip(box, lambda tt: True)
    msp = Spr(150, 130, 75, 65, wc=0, seed=1)
    msp.add(flap_marks(75, 65, 1, 1.0))
    for bi, col in enumerate(BIRD_COLS):
        lead = bi == 0
        t_arr = t_pu[2] + 0.45 + 0.4 * bi
        t_dep = t_bird - 0.3 + 0.32 * bi
        for female in (False, True):
            sp = Spr(150, 150, 75, 80, wc=0.5, seed=400 + bi * 3 + female)
            fr = [sp.add(PR.songbird(75, 80, SC * 1.2 * (0.95 if female else 1.0), 1, wing=w, color=col,
                                     female=female)) for w in wings]
            p0 = (200 + 110 * bi + (60 if female else 0), 110 + 70 * bi + (40 if female else 0))
            p3 = (wx + (12 if female else -10), wy + (8 if female else -6))
            p1 = (p0[0] + 560, p0[1] + 30)
            p2 = (p3[0] - 320, p3[1] - 340)
            t0 = t_dep + (0.12 if female else 0.0)
            t1 = t_arr + (0.14 if female else 0.0)
            t_in = t1 - 0.3

            def path(t, p=(p0, p1, p2, p3), t0=t0, t1=t1):
                u = clamp((t - t0) / (t1 - t0))
                u = 0.82 * u + 0.18 * (0.5 - 0.5 * math.cos(math.pi * u))
                return bezier(*p, u), u

            def beat(t, lead=lead, t0=t0):
                """(wing phase 0..1, lift)"""
                if lead:
                    for tp in t_pu:
                        v = t - (tp - 0.1)
                        if 0 <= v < 0.2:
                            return v / 0.2, -16 * math.sin(math.pi * v / 0.2)
                return ((t - t0) * 2.8) % 1.0, 0.0

            def bstate(t, sp=sp, fr=fr, t0=t0, t1=t1, t_in=t_in, path=path, beat=beat):
                if t < t0 or t > t1:
                    return None
                (x, y), u = path(t)
                (xu, yu), _ = path(t + 0.03)
                ph, dy = beat(t)
                k = cyc[int(ph * 8) % 8]
                s_ = 1.0 - 0.45 * M.progress(t, t_in, t1, "in")
                rot = clamp(math.degrees(math.atan2(yu - y, max(1e-3, xu - x))) * 0.45, -20, 20)
                im, ax, ay = sp.get(fr[k], s_, s_, rot)
                left, top = x - ax, y + dy - ay
                if t > t_in:
                    im = in_clip(im, left, top)
                    if im is None:
                        return None
                    kd = M.progress(t, t_in, t1, "sine")
                    arr = np.asarray(im).astype(np.float32)
                    arr[..., :3] *= 1 - 0.45 * kd
                    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
                return im, (left, top)
            sc.add_dynamic(f"bird{bi}{'f' if female else 'm'}", bstate, z=z + 0.1 * bi + (0.0 if female else 0.05))
            if lead and not female:
                def mstate(t, path=path):
                    for tp in t_pu:
                        v = t - tp
                        if -0.02 <= v < 0.24:
                            (x, y), _ = path(t)
                            a = 1 - clamp(v / 0.24)
                            im, ax, ay = msp.get(0, 1 + 0.4 * clamp(v / 0.24), 1 + 0.4 * clamp(v / 0.24), 0)
                            arr = np.asarray(im).copy()
                            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
                            return Image.fromarray(arr, "RGBA"), (x - ax - 6, y - ay - 8)
                    return None
                sc.add_dynamic("bird_flaps", mstate, z=z + 0.3)


# ============================================================================ Noah (s07)
def noah_frames(sp, extra=()):
    """Noah's drawings on a person sprite: returns {name: idx}."""
    ax, ay = sp.ax, sp.ay
    sh = C.ground_shadow(ax, ay, SC, 120, 0.2)
    defs = {
        "stand_r": ("stand", 1, None), "stand_l": ("stand", -1, None), "blink_r": ("stand", 1, blink_expr("kind")),
        "blink_l": ("stand", -1, blink_expr("kind")), "cheer": ("cheer", 1, "laugh"), "talk_l": ("talk", -1, "happy"),
        "talk_r": ("talk", 1, "happy"), "nod_l": ("nod", -1, "happy"), "laugh_l": ("stand", -1, "laugh"),
        "happy_l": ("stand", -1, "happy"), "walk_a": ("walk_a", -1, None), "walk_b": ("walk_b", -1, None),
        "wave0": ("wave", 1, None), "wave1": ("wave", 1, None), "wave2": ("wave", 1, None),
        "wave3": ("wave", 1, None),
    }
    out = {}
    for nm, (pose, f, e) in list(defs.items()) + list(extra):
        ph = 0.0
        if nm.startswith("wave") and nm[-1].isdigit():
            ph = int(nm[-1]) * 0.25
        out[nm] = sp.add(sh + C.noah(ax, ay, SC, f, pose=pose, expr=e, phase=ph))
    return out


def add_noah_s07(sc, ctx, tm, z):
    sp = person_spr(60)
    fr = noah_frames(sp)
    nx, ny = NOAH_SPOT
    t_come, t_dong, t_roar = tm["t_come"], tm["t_dong"], tm["t_roar"]
    t_food, t_people, t_end = tm["t_food"], tm["t_people"], tm["t_end"]
    c_cheer = snap(t_come + 0.05)
    c_turn = snap(t_dong[1] - 0.1)
    c_talk = snap(t_dong[2] + 0.6)
    c_stand = snap(c_talk + 1.6)
    c_laugh = snap(t_roar + 0.18)
    c_laugh_end = snap(t_roar + 1.1)
    c_happy = snap(tm["t_rab"] + 0.3)
    c_nod = [snap(tm["t_pairs"] + 0.1 + 0.55 * k) for k in range(3)]
    c_talk2 = snap(tm["t_line"] + 0.1)
    c_wave = snap(t_food + 0.25)
    c_talk3 = snap(t_people - 0.1)
    # step back into the line (two strides, diagonal) at the end
    t_w0 = snap(t_end - 0.62)
    x_line = FAM_END["noah"]
    entries = [(0, fr["stand_r"]), (c_cheer, fr["cheer"]), (snap(c_cheer + 0.9), fr["stand_r"]), (c_turn, fr["stand_l"]),
               (c_talk, fr["talk_l"]), (c_stand, fr["stand_l"]), (c_laugh, fr["laugh_l"]),
               (c_laugh_end, fr["stand_l"]), (c_happy, fr["happy_l"]), (snap(c_happy + 1.6), fr["stand_l"])]
    for k, cn in enumerate(c_nod):
        entries += [(cn, fr["nod_l"]), (snap(cn + 0.28), fr["talk_l"] if k == 2 else fr["stand_l"])]
    entries += [(c_talk2, fr["talk_l"]), (snap(c_talk2 + 1.3), fr["stand_l"])]
    wave_end = snap(c_talk3 - 0.05)
    entries += [(c_wave, fr["wave0"])]
    entries += [(c_talk3, fr["talk_l"]), (snap(t_w0 - 0.25), fr["stand_l"])]
    entries = sorted(entries, key=lambda e: e[0])
    blinks = [1.5, 6.9, 12.3, 16.0, t_end + 0.7]

    def base(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        if c_wave <= t < wave_end:
            return fr[f"wave{int((t - c_wave) * 8) % 4}"]
        for b in blinks:
            if b <= t < b + 0.13 and v in (fr["stand_l"], fr["stand_r"]):
                return fr["blink_l"] if v == fr["stand_l"] else fr["blink_r"]
        return v
    pts_ = [(t_w0, nx), (t_w0 + 0.5, x_line)]
    st = Stepper(lin_plan([(t_w0 - 0.1, nx), (t_w0 + 0.45, x_line)]), t_w0 - 0.2, ctx.duration, 50,
                 cut_times=[t_w0, snap(t_w0 + 0.27)], mf=0.7, max_move=0.2)
    st.pos = [nx + (x_line - nx) * 0.5, x_line]
    st.hold = 0.4

    def yfn(t):
        u = M.progress(t, t_w0 - 0.1, t_w0 + 0.45, "sine")
        return ny + (GY - ny) * u
    bumps = [squash_dip(c, 0.045, 0.28) for c, _ in entries[1:]]
    bumps.append(jump_bump(c_cheer + 0.02, 22 * SC, 0.42))
    bumps.append(jump_bump(c_laugh + 0.02, 14 * SC, 0.36))
    bumps.append(squash_dip(snap(t_w0 + 0.55), 0.04, 0.28))
    act = Actor(sp, st.x, base, stepper=st, walk=(fr["walk_a"], fr["walk_b"]), yfn=yfn, bumps=bumps, bounce=5 * SC,
                breathe=(0.011, 3.1, 0.1))
    sc.add_dynamic("noah", act, z=z)
    return act
