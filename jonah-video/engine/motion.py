"""Motion helpers for scene layers and cameras.

A *motion* is a function ``m(t) -> Tf`` where ``t`` is seconds since the scene
started. Combine several with ``combine``. All motions are pure functions of
time so any frame can be rendered independently (and in parallel).
"""
import math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Tf:
    """2D transform of a layer, in stage pixels.

    The layer is scaled by (sx, sy) and rotated by ``rot`` degrees (clockwise,
    like SVG) around the pivot (px, py), then translated by (dx, dy).
    ``alpha`` multiplies the layer opacity.
    """
    dx: float = 0.0
    dy: float = 0.0
    rot: float = 0.0
    sx: float = 1.0
    sy: float = 1.0
    alpha: float = 1.0
    px: float = None
    py: float = None


IDENTITY = Tf()


# ---------------------------------------------------------------- easing
def ease(name="inout"):
    if callable(name):
        return name
    return {
        "linear": lambda u: u,
        "in": lambda u: u * u * u,
        "out": lambda u: 1 - (1 - u) ** 3,
        "inout": lambda u: 4 * u * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2,
        "sine": lambda u: 0.5 - 0.5 * math.cos(math.pi * u),
        "back": lambda u: 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2,
        "bounce": _bounce,
        "step": lambda u: 1.0 if u >= 1 else 0.0,
    }[name]


def _bounce(u):
    n, d = 7.5625, 2.75
    if u < 1 / d:
        return n * u * u
    if u < 2 / d:
        u -= 1.5 / d
        return n * u * u + 0.75
    if u < 2.5 / d:
        u -= 2.25 / d
        return n * u * u + 0.9375
    u -= 2.625 / d
    return n * u * u + 0.984375


def progress(t, t0, t1, curve="inout"):
    """0 before t0, 1 after t1, eased in between."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    return ease(curve)(u)


def lerp(a, b, u):
    return a + (b - a) * u


# ---------------------------------------------------------------- motions
def still(tf=IDENTITY):
    return lambda t: tf


def keys(frames, curve="inout", pivot=None):
    """Keyframed motion.

    frames: list of (time, dict) with any of dx, dy, rot, s (uniform scale),
    sx, sy, alpha. Missing values carry over from the previous key (default
    identity). ``curve`` may be one name or a list (one per segment).
    """
    frames = sorted(frames, key=lambda k: k[0])
    full = []
    prev = {"dx": 0.0, "dy": 0.0, "rot": 0.0, "sx": 1.0, "sy": 1.0, "alpha": 1.0}
    for tk, d in frames:
        d = dict(d)
        if "s" in d:
            d["sx"] = d["sy"] = d.pop("s")
        cur = {**prev, **d}
        full.append((tk, cur))
        prev = cur
    curves = curve if isinstance(curve, (list, tuple)) else [curve] * max(1, len(full) - 1)
    px, py = pivot if pivot else (None, None)

    def m(t):
        if t <= full[0][0]:
            v = full[0][1]
        elif t >= full[-1][0]:
            v = full[-1][1]
        else:
            for i in range(len(full) - 1):
                (t0, a), (t1, b) = full[i], full[i + 1]
                if t0 <= t <= t1:
                    u = progress(t, t0, t1, curves[min(i, len(curves) - 1)])
                    v = {k: lerp(a[k], b[k], u) for k in a}
                    break
        return Tf(v["dx"], v["dy"], v["rot"], v["sx"], v["sy"], v["alpha"], px, py)

    return m


def bob(amp=6.0, period=2.4, phase=0.0, axis="y"):
    """Gentle up/down (or left/right) floating."""
    def m(t):
        v = amp * math.sin(2 * math.pi * (t / period + phase))
        return Tf(dx=v) if axis == "x" else Tf(dy=v)
    return m


def sway(deg=3.0, period=3.0, pivot=(0, 0), phase=0.0):
    """Rocking rotation around a pivot (stage px), e.g. a boat or a plant."""
    return lambda t: Tf(rot=deg * math.sin(2 * math.pi * (t / period + phase)), px=pivot[0], py=pivot[1])


def breathe(amount=0.015, period=3.0, pivot=(0, 0), phase=0.0):
    """Subtle scale pulse (characters breathing, glows pulsing)."""
    def m(t):
        s = 1 + amount * math.sin(2 * math.pi * (t / period + phase))
        return Tf(sx=s, sy=s, px=pivot[0], py=pivot[1])
    return m


def drift(vx=0.0, vy=0.0, t0=0.0):
    """Constant velocity in px/s (clouds, slow parallax)."""
    return lambda t: Tf(dx=vx * (t - t0), dy=vy * (t - t0))


def pulse(lo=0.6, hi=1.0, period=2.0, phase=0.0):
    """Opacity oscillation."""
    return lambda t: Tf(alpha=lo + (hi - lo) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / period + phase))))


def visible(t0, t1=1e9, fade=0.4):
    """Fade in at t0 and out at t1."""
    def m(t):
        a = progress(t, t0, t0 + fade, "sine") if fade > 0 else float(t >= t0)
        if t1 < 1e8:
            a *= 1 - (progress(t, t1 - fade, t1, "sine") if fade > 0 else float(t >= t1))
        return Tf(alpha=a)
    return m


def shake(amp=10.0, t0=0.0, t1=1e9, freq=9.0, seed=1):
    """Pseudo-random jitter (storm, impact). Deterministic in t."""
    def m(t):
        if not (t0 <= t <= t1):
            return IDENTITY
        a = amp * min(1.0, (t - t0) / 0.15, (t1 - t) / 0.3 if t1 < 1e8 else 1.0)
        x = math.sin(t * freq * 2.1 + seed) + 0.5 * math.sin(t * freq * 3.7 + 2 * seed)
        y = math.sin(t * freq * 1.7 + 3 * seed) + 0.5 * math.sin(t * freq * 4.3 + seed)
        return Tf(dx=a * x / 1.5, dy=a * y / 1.5, rot=a * 0.04 * math.sin(t * freq * 1.3 + seed))
    return m


def combine(*ms):
    """Sum translations/rotations, multiply scales and opacities.

    The pivot comes from the first motion that defines one.
    """
    ms = [m for m in ms if m is not None]

    def m(t):
        out = IDENTITY
        for f in ms:
            v = f(t)
            out = Tf(out.dx + v.dx, out.dy + v.dy, out.rot + v.rot, out.sx * v.sx, out.sy * v.sy,
                     out.alpha * v.alpha,
                     out.px if out.px is not None else v.px, out.py if out.py is not None else v.py)
        return out
    return m


def with_pivot(m, pivot):
    return lambda t: replace(m(t), px=pivot[0], py=pivot[1])


# ---------------------------------------------------------------- camera
@dataclass(frozen=True)
class Cam:
    """Camera viewport in stage pixels: centre (x, y), width w (height = w*9/16), rotation."""
    x: float
    y: float
    w: float
    rot: float = 0.0


def cam_keys(frames, curve="inout"):
    """frames: list of (time, Cam). Returns camera function t -> Cam."""
    frames = sorted(frames, key=lambda k: k[0])
    curves = curve if isinstance(curve, (list, tuple)) else [curve] * max(1, len(frames) - 1)

    def c(t):
        if t <= frames[0][0]:
            return frames[0][1]
        if t >= frames[-1][0]:
            return frames[-1][1]
        for i in range(len(frames) - 1):
            (t0, a), (t1, b) = frames[i], frames[i + 1]
            if t0 <= t <= t1:
                u = progress(t, t0, t1, curves[min(i, len(curves) - 1)])
                return Cam(lerp(a.x, b.x, u), lerp(a.y, b.y, u), lerp(a.w, b.w, u), lerp(a.rot, b.rot, u))
    return c


def cam_shake(cam, amp=12.0, t0=0.0, t1=1e9, freq=7.0, seed=3):
    """Add shake (stage px) to a camera function."""
    sh = shake(amp, t0, t1, freq, seed)

    def c(t):
        b, s = cam(t), sh(t)
        return Cam(b.x + s.dx, b.y + s.dy, b.w, b.rot + s.rot)
    return c
