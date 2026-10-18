"""Per-frame procedural effects, applied in output space after layers are composited.

Each factory returns ``fx(frame, t, view)`` which draws on/returns the frame
(PIL RGBA, 1920x1080). ``view.to_out(x, y)`` maps stage px to output px and
``view.scale`` is output px per stage px. All effects are deterministic in t.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from engine.motion import progress
from engine.paths import OUT_H, OUT_W


def _env(t, t0, t1, fade=0.5):
    if t < t0 or t > t1:
        return 0.0
    return min(1.0, progress(t, t0, t0 + fade, "sine"), 1 - progress(t, t1 - fade, t1, "sine") if t1 < 1e8 else 1.0)


def rain(t0=0.0, t1=1e9, density=1.0, angle=14, length=46, speed=1700, color=(225, 233, 242), alpha=110,
         width=2, seed=5):
    """Slanted rain streaks over the whole frame."""
    n = int(420 * density)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = speed * rng.uniform(0.75, 1.25, n)
    ln = length * rng.uniform(0.6, 1.3, n)
    a = math.radians(angle)
    dx, dy = math.sin(a), math.cos(a)

    def fx(frame, t, view):
        k = _env(t, t0, t1, 0.6)
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0 + sp * t) % (OUT_H + 80) - 40
        x = (x0 - sp * t * dx / dy) % (OUT_W + 400) - 200
        col = (*color, int(alpha * k))
        for i in range(n):
            d.line([(x[i], y[i]), (x[i] + ln[i] * dx, y[i] + ln[i] * dy)], fill=col, width=width)
        frame.alpha_composite(ov)
        return frame
    return fx


def lightning(times, dur=0.45, strength=0.75, color=(235, 240, 255)):
    """Bright double-flicker flashes at the given times (s)."""
    def env(u):
        # two quick peaks then decay
        return max(math.exp(-((u - 0.03) / 0.03) ** 2), 0.7 * math.exp(-((u - 0.16) / 0.05) ** 2)) + \
            0.25 * math.exp(-u / 0.2) * (u > 0)

    def fx(frame, t, view):
        k = 0.0
        for ts in times:
            if ts <= t <= ts + dur:
                k = max(k, env(t - ts))
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (*color, int(255 * min(1.0, strength * k))))
        return Image.alpha_composite(frame, ov)
    return fx


def tint(color, alpha_fn, mode="normal"):
    """Colour wash over the frame. alpha_fn(t) -> 0..1. mode: normal | multiply | screen."""
    col = np.array(color, np.float32) / 255.0

    def fx(frame, t, view):
        a = float(alpha_fn(t))
        if a <= 0.003:
            return frame
        if mode == "normal":
            ov = Image.new("RGBA", frame.size, (*color, int(255 * min(1, a))))
            return Image.alpha_composite(frame, ov)
        arr = np.asarray(frame, np.float32) / 255.0
        rgb = arr[..., :3]
        if mode == "multiply":
            rgb = rgb * (1 - a + a * col)
        elif mode == "screen":
            rgb = 1 - (1 - rgb) * (1 - a * col)
        arr = np.dstack([rgb, arr[..., 3:]])
        return Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    return fx


def vignette(strength_fn, color=(20, 16, 30)):
    """Darken frame edges; strength_fn(t) -> 0..1."""
    yy, xx = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)
    r = np.sqrt(((xx - OUT_W / 2) / (OUT_W / 2)) ** 2 + ((yy - OUT_H / 2) / (OUT_H / 2)) ** 2)
    base = np.clip((r - 0.35) / 0.95, 0, 1) ** 1.6

    def fx(frame, t, view):
        s = float(strength_fn(t))
        if s <= 0.003:
            return frame
        a = (np.clip(base * s, 0, 1) * 255).astype(np.uint8)
        ov = Image.new("RGBA", frame.size, color)
        ov.putalpha(Image.fromarray(a, "L"))
        return Image.alpha_composite(frame, ov)
    return fx


def bubbles(rect, count=18, t0=0.0, t1=1e9, rise=90, size=(6, 22), color=(235, 248, 255), seed=9):
    """Rising bubbles spawned inside a stage-space rect (x0, y0, x1, y1)."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = rect
    bx = rng.uniform(x0, x1, count)
    ph = rng.uniform(0, 1, count)
    rs = rng.uniform(*size, count)
    sp = rise * rng.uniform(0.6, 1.4, count)
    span = y1 - y0

    def fx(frame, t, view):
        k = _env(t, t0, t1, 0.5)
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            yy = y1 - ((ph[i] * span + sp[i] * t) % span)
            xx = bx[i] + 10 * math.sin(t * 2 + i)
            ox, oy = view.to_out(xx, yy)
            r = rs[i] * view.scale
            fade = min(1.0, (y1 - yy) / 80, (yy - y0) / 80)
            a = int(170 * k * max(0, fade))
            d.ellipse([ox - r, oy - r, ox + r, oy + r], outline=(*color, a), width=max(2, int(r / 5)))
            d.ellipse([ox - r * 0.45, oy - r * 0.55, ox - r * 0.1, oy - r * 0.2], fill=(255, 255, 255, a))
        frame.alpha_composite(ov)
        return frame
    return fx


def sparkles(rect, count=24, t0=0.0, t1=1e9, color=(255, 236, 170), size=(8, 20), period=1.6, drift=-12,
             seed=11):
    """Twinkling four-point stars inside a stage-space rect (divine light, magic). They drift ``drift`` px/s
    from the moment they appear (t0), so a late set still starts inside its rect."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = rect
    px = rng.uniform(x0, x1, count)
    py = rng.uniform(y0, y1, count)
    ph = rng.uniform(0, 1, count)
    sz = rng.uniform(*size, count)

    def fx(frame, t, view):
        k = _env(t, t0, t1, 0.6)
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t / period + ph[i]))
            if tw < 0.15:
                continue
            ox, oy = view.to_out(px[i], py[i] + drift * (t - t0))
            r = sz[i] * view.scale * (0.5 + 0.5 * tw)
            a = int(230 * k * tw)
            w = r * 0.22
            g = r * 0.55
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*color, a // 4))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


def motes(rect, count=30, t0=0.0, t1=1e9, color=(255, 246, 214), size=(3, 7), seed=13, alpha=150):
    """Slowly drifting soft dust / light motes (warm sunbeams, underwater particles)."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = rect
    px = rng.uniform(x0, x1, count)
    py = rng.uniform(y0, y1, count)
    vx = rng.uniform(-12, 12, count)
    vy = rng.uniform(-14, 6, count)
    sz = rng.uniform(*size, count)
    ph = rng.uniform(0, 6.28, count)

    def fx(frame, t, view):
        k = _env(t, t0, t1, 0.8)
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        w, h = x1 - x0, y1 - y0
        for i in range(count):
            xx = x0 + (px[i] - x0 + vx[i] * t + 8 * math.sin(t * 0.7 + ph[i])) % w
            yy = y0 + (py[i] - y0 + vy[i] * t) % h
            ox, oy = view.to_out(xx, yy)
            r = sz[i] * view.scale
            a = int(alpha * k * (0.6 + 0.4 * math.sin(t * 1.3 + ph[i])))
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


def fade(color=(0, 0, 0), t_in=None, t_out=None, dur=0.6):
    """Fade from colour at scene start (t_in) and/or to colour ending at t_out."""
    def fx(frame, t, view):
        a = 0.0
        if t_in is not None:
            a = max(a, 1 - progress(t, t_in, t_in + dur, "sine"))
        if t_out is not None:
            a = max(a, progress(t, t_out - dur, t_out, "sine"))
        if a <= 0.003:
            return frame
        ov = Image.new("RGBA", frame.size, (*color, int(255 * a)))
        return Image.alpha_composite(frame, ov)
    return fx
