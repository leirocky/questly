"""Picture-book post-processing: watercolour pigment texture and paper.

``watercolor(img)`` is applied once per rasterised layer (cached):
  * low-frequency pigment density variation (uneven washes),
  * fine granulation,
  * edge pooling: pigment darkens slightly along shape silhouettes and along
    colour boundaries inside the layer, like dried watercolour.

``paper_multiplier(w, h)`` is a static cream paper grain multiplied over every
output frame, so the whole film reads as printed on textured paper.
"""
import hashlib
from functools import lru_cache

import numpy as np
from PIL import Image
from scipy import ndimage

from engine.paths import CACHE


def _smooth_noise(h, w, sigma, rng):
    """Gaussian-smoothed noise in [-1, 1], generated at reduced resolution for speed."""
    f = max(1, int(sigma / 2))
    small = rng.standard_normal((max(2, h // f + 2), max(2, w // f + 2))).astype(np.float32)
    small = ndimage.gaussian_filter(small, max(0.5, sigma / f), mode="wrap")
    im = Image.fromarray(small, mode="F").resize((w, h), Image.BICUBIC)
    n = np.asarray(im, dtype=np.float32)
    n = n - n.mean()
    return n / (np.abs(n).max() + 1e-6)


def _blur(a, r):
    return ndimage.gaussian_filter(a.astype(np.float32), r)


def watercolor(img, seed=0, strength=1.0, edge=1.0, grain=1.0):
    """Return a new RGBA image with watercolour texture. strength=0 returns a copy."""
    if strength <= 0:
        return img.copy()
    key = hashlib.sha1(img.tobytes() + f"{img.size}{seed}{strength}{edge}{grain}".encode()).hexdigest()[:20]
    path = CACHE / "wc" / f"{key}.png"
    if path.exists():
        return Image.open(path).convert("RGBA")
    rng = np.random.default_rng(seed + 1000)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    rgb, a = arr[..., :3], arr[..., 3]
    h, w = a.shape

    # Pigment density: big soft blotches + medium mottling + fine granulation.
    dens = 0.075 * _smooth_noise(h, w, 70, rng) + 0.045 * _smooth_noise(h, w, 14, rng)
    dens += 0.028 * grain * (rng.standard_normal((h, w)).astype(np.float32))
    dens *= strength

    # Edge pooling along the alpha silhouette (inner rim).
    rim = np.clip(a - _blur(a, 5.0), 0, 1) * 2.2
    # Edge pooling along internal colour boundaries.
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    inner = np.abs(lum - _blur(lum, 2.5))
    inner = np.clip(inner * 4.0, 0, 1)
    pool = edge * strength * (0.20 * rim + 0.12 * inner)

    factor = (1.0 + dens - pool)[..., None]
    out_rgb = np.clip(rgb * factor, 0, 1)
    # Washes are slightly translucent at their very edges.
    out_a = a * (1 - 0.06 * strength * np.clip(rim, 0, 1))
    out = np.dstack([out_rgb, out_a])
    res = Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA")
    path.parent.mkdir(parents=True, exist_ok=True)
    res.save(path)
    return res


@lru_cache(maxsize=4)
def paper_multiplier(w, h, seed=42, strength=1.0):
    """uint16 multiplier (0..256 == 0..1.0) per pixel and channel for warm paper grain + vignette."""
    rng = np.random.default_rng(seed)
    fine = rng.standard_normal((h, w)).astype(np.float32)
    fine = _blur(fine, 0.7)
    fine /= np.abs(fine).max() + 1e-6
    mottle = _smooth_noise(h, w, 40, rng)
    # Paper fibres: thin streaks from stretched noise.
    fib = rng.standard_normal((h // 6 + 1, w // 40 + 1)).astype(np.float32)
    fib = np.asarray(Image.fromarray(fib, "F").resize((w, h), Image.BICUBIC), np.float32)
    fib = np.clip(fib - 1.6, 0, None)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vign = np.clip(r - 0.55, 0, None) ** 2 * 0.22
    m = 1.0 - strength * (0.035 * (fine * 0.5 + 0.5) + 0.03 * (mottle * 0.5 + 0.5) + 0.004 * fib + vign)
    tint = np.array([1.0, 0.985, 0.95], np.float32)  # warm cream
    mult = np.clip(m[..., None] * tint, 0, 1)
    return (mult * 256).astype(np.uint16)


def apply_paper(frame_rgb_u8, mult_u16):
    """Multiply an HxWx3 uint8 frame by the paper multiplier (in place-safe)."""
    return ((frame_rgb_u8.astype(np.uint16) * mult_u16) >> 8).astype(np.uint8)
