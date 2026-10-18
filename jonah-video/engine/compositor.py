"""Turns a Scene into frames: rasterise -> watercolour -> animate -> fx -> paper -> subtitles.

Layers are kept as premultiplied uint8 arrays so affine resampling (OpenCV)
never produces dark fringes. Consecutive static layers are flattened once; moving
layers are transformed per frame only inside their output bounding box.
"""
import math
import subprocess
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from engine import raster
from engine import watercolor as WC
from engine.motion import Tf
from engine.paths import FONT_BOLD, FPS, OUT_H, OUT_W

# --------------------------------------------------------------------- matrices


def _T(x, y):
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], np.float64)


def _S(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], np.float64)


def _R(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float64)


def cam_matrix(cam):
    """Stage px -> output px."""
    s = OUT_W / cam.w
    return _T(OUT_W / 2, OUT_H / 2) @ _S(s, s) @ _R(-cam.rot) @ _T(-cam.x, -cam.y)


def layer_matrix(tf, pivot):
    px = tf.px if tf.px is not None else pivot[0]
    py = tf.py if tf.py is not None else pivot[1]
    return _T(px + tf.dx, py + tf.dy) @ _R(tf.rot) @ _S(tf.sx, tf.sy) @ _T(-px, -py)


@dataclass
class View:
    M: np.ndarray
    scale: float
    t: float

    def to_out(self, x, y):
        v = self.M @ np.array([x, y, 1.0])
        return float(v[0]), float(v[1])


# --------------------------------------------------------------------- preparation


def to_pm(img):
    """PIL RGBA -> premultiplied uint8 numpy (H, W, 4)."""
    a = np.asarray(img.convert("RGBA"), np.uint8)
    out = a.copy()
    alpha = a[..., 3:4].astype(np.uint16)
    out[..., :3] = ((a[..., :3].astype(np.uint16) * alpha + 127) // 255).astype(np.uint8)
    return out


class Item:
    """A drawable: list of premultiplied frames (numpy HxWx4) sharing one crop offset."""

    def __init__(self, name, imgs, off, pivot, layer=None, dyn=None, z=0):
        self.name, self.imgs, self.off, self.pivot = name, imgs, off, pivot
        self.layer, self.dyn, self.z = layer, dyn, z
        self._variants = {}

    def variant(self, idx, r):
        key = (idx, r)
        if key not in self._variants:
            im = self.imgs[idx]
            h, w = im.shape[:2]
            self._variants[key] = cv2.resize(im, (max(1, round(w * r)), max(1, round(h * r))),
                                             interpolation=cv2.INTER_AREA)
        return self._variants[key]


def _prepare_layer_frames(scene, layer):
    out = []
    for i, svg in enumerate(layer.frames):
        im = raster.rasterize(svg, scene.W, scene.H)
        if layer.wc > 0:
            im = WC.watercolor(im, seed=layer.seed + i * 0, strength=layer.wc, edge=layer.wc_edge)
        out.append(im)
    return out


def prepare(scene):
    """Rasterise all layers and build the ordered draw list."""
    entries = sorted([("L", l.z, l) for l in scene.layers] + [("D", d.z, d) for d in scene.dynamics],
                     key=lambda e: e[1])
    items = []
    pending = None  # stage canvas accumulating consecutive static layers
    pending_names = []

    def flush():
        nonlocal pending, pending_names
        if pending is not None:
            bbox = pending.getchannel("A").getbbox()
            if bbox:
                crop = to_pm(pending.crop(bbox))
                items.append(Item("+".join(pending_names), [crop], bbox[:2],
                                  ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)))
        pending, pending_names = None, []

    for kind, z, obj in entries:
        if kind == "D":
            flush()
            items.append(Item(obj.name, None, (0, 0), (0, 0), dyn=obj, z=z))
            continue
        frames = _prepare_layer_frames(scene, obj)
        if obj.is_static:
            if pending is None:
                pending = Image.new("RGBA", (scene.W, scene.H), (0, 0, 0, 0))
            pending.alpha_composite(frames[0])
            pending_names.append(obj.name)
            continue
        flush()
        bbox = None
        for f in frames:
            b = f.getchannel("A").getbbox()
            if b:
                bbox = b if bbox is None else (min(bbox[0], b[0]), min(bbox[1], b[1]),
                                               max(bbox[2], b[2]), max(bbox[3], b[3]))
        if bbox is None:
            continue
        crops = [to_pm(f.crop(bbox)) for f in frames]
        items.append(Item(obj.name, crops, bbox[:2],
                          ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2), layer=obj, z=z))
    flush()
    return items


# --------------------------------------------------------------------- drawing


def _reveal_mask(rv, w, h, off):
    mode, frac, soft = rv.get("mode", "up"), float(rv.get("frac", 1.0)), float(rv.get("soft", 40))
    if frac >= 1.0 and mode != "radial":
        return None
    if mode in ("up", "down"):
        v = np.arange(h, dtype=np.float32)[:, None]
        edge = h * (1 - frac) if mode == "up" else h * frac
        d = (v - edge) if mode == "up" else (edge - v)
        m = np.clip(d / soft + 0.5, 0, 1) * np.ones((1, w), np.float32)
    elif mode in ("left", "right"):
        u = np.arange(w, dtype=np.float32)[None, :]
        edge = w * frac if mode == "left" else w * (1 - frac)
        d = (edge - u) if mode == "left" else (u - edge)
        m = np.clip(d / soft + 0.5, 0, 1) * np.ones((h, 1), np.float32)
    elif mode == "radial":
        cx, cy = rv.get("cx", off[0] + w / 2) - off[0], rv.get("cy", off[1] + h / 2) - off[1]
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        maxd = max(math.hypot(cx, cy), math.hypot(w - cx, cy), math.hypot(cx, h - cy), math.hypot(w - cx, h - cy))
        m = np.clip((frac * maxd - dist) / soft + 0.5, 0, 1)
    else:
        raise ValueError(mode)
    return m


def _apply_mask(pm, m):
    return (pm.astype(np.float32) * m[..., None] + 0.5).astype(np.uint8)


def composite_pm(frame, src, x0, y0, blend="normal"):
    """Composite premultiplied src (h, w, 4) onto opaque RGB frame (H, W, 3) at (x0, y0)."""
    h, w = src.shape[:2]
    H, W = frame.shape[:2]
    if x0 < 0 or y0 < 0 or x0 + w > W or y0 + h > H:
        cx0, cy0 = max(0, -x0), max(0, -y0)
        cx1, cy1 = min(w, W - x0), min(h, H - y0)
        if cx1 <= cx0 or cy1 <= cy0:
            return
        src = src[cy0:cy1, cx0:cx1]
        x0, y0, h, w = x0 + cx0, y0 + cy0, cy1 - cy0, cx1 - cx0
    dst = frame[y0:y0 + h, x0:x0 + w]
    rgb = src[..., :3]
    a = src[..., 3]
    if blend == "normal":
        inv = cv2.merge([255 - a] * 3)
        dst[:] = cv2.add(cv2.multiply(dst, inv, scale=1 / 255.0), rgb)
    elif blend == "add":
        dst[:] = cv2.add(dst, rgb)
    elif blend == "screen":
        # 255 - (255 - d)(255 - s)/255; computed via complements so nothing saturates early.
        dst[:] = cv2.subtract(255, cv2.multiply(cv2.subtract(255, dst), cv2.subtract(255, rgb), scale=1 / 255.0))
    elif blend == "multiply":
        k = cv2.add(cv2.merge([255 - a] * 3), rgb)
        dst[:] = cv2.multiply(dst, k, scale=1 / 255.0)
    else:
        raise ValueError(blend)


def draw_image(frame, pm, M, alpha=1.0, blend="normal"):
    """Draw premultiplied numpy image whose local px map to output px via forward 3x3 matrix M."""
    h, w = pm.shape[:2]
    det = abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])
    if det < 1e-9 or alpha <= 0.002:
        return
    corners = M @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]], np.float64)
    x0 = max(0, int(math.floor(corners[0].min())) - 1)
    y0 = max(0, int(math.floor(corners[1].min())) - 1)
    x1 = min(OUT_W, int(math.ceil(corners[0].max())) + 1)
    y1 = min(OUT_H, int(math.ceil(corners[1].max())) + 1)
    if x1 <= x0 or y1 <= y0:
        return
    A = (_T(-x0, -y0) @ M)[:2]
    # cv2 maps pixel centres; shift by half a pixel so stage px edges line up with SVG/PIL convention.
    A = A.copy()
    A[:, 2] += 0.5 * (A[:, 0] + A[:, 1]) - 0.5
    reg = cv2.warpAffine(pm, A, (x1 - x0, y1 - y0), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT,
                         borderValue=(0, 0, 0, 0))
    if alpha < 0.998:
        reg = cv2.convertScaleAbs(reg, alpha=alpha)
    composite_pm(frame, reg, x0, y0, blend)


def _draw_item(frame, item, t, C):
    if item.dyn is not None:
        res = item.dyn.fn(t)
        if res is None:
            return
        img, (x, y) = res
        draw_image(frame, to_pm(img), C @ _T(x, y), 1.0, item.dyn.blend)
        return
    layer = item.layer
    tf = layer.motion(t) if (layer and layer.motion) else Tf()
    if tf.alpha <= 0.002:
        return
    # Pick (or crossfade) the flipbook frame.
    idx = 0
    img = item.imgs[0]
    if len(item.imgs) > 1:
        f = layer.frame_at(t) if layer.frame_at else 0.0
        f = min(max(f, 0.0), len(item.imgs) - 1)
        i0 = int(math.floor(f))
        frac = f - i0
        idx = i0
        img = item.imgs[i0]
        if frac > 0.01 and i0 + 1 < len(item.imgs):
            img = cv2.addWeighted(item.imgs[i0], 1 - frac, item.imgs[i0 + 1], frac, 0)
            idx = None
    if layer and layer.reveal:
        m = _reveal_mask(layer.reveal(t), img.shape[1], img.shape[0], item.off)
        if m is not None:
            img = _apply_mask(img, m)
            idx = None
    L = layer_matrix(tf, item.pivot) if layer else np.eye(3)
    M = C @ L @ _T(*item.off)
    s_eff = math.sqrt(abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]))
    if s_eff < 0.78:
        r = max(0.2, round(s_eff * 1.15, 1))
        if idx is not None:
            img = item.variant(idx, r)
        else:
            h, w = img.shape[:2]
            img = cv2.resize(img, (max(1, round(w * r)), max(1, round(h * r))), interpolation=cv2.INTER_AREA)
        M = M @ _S(1 / r, 1 / r)
    draw_image(frame, img, M, tf.alpha, layer.blend if layer else "normal")


# --------------------------------------------------------------------- subtitles

SPEAKER_COLORS = {"N": (74, 50, 34), "G": (150, 92, 14), "J": (30, 88, 96),
                  "C": (120, 52, 40), "S": (52, 70, 120), "K": (96, 52, 120)}


def subtitle_image(text, speaker="N", size=50):
    font = ImageFont.truetype(str(FONT_BOLD), size)
    text = text.rstrip("，、")
    l, t_, r, b = font.getbbox(text)
    tw, th = r - l, b - t_
    px, py, m = 38, 18, 14
    W, H = tw + 2 * px + 2 * m, th + 2 * py + 2 * m
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m + 2, m + 4, W - m + 2, H - m + 4], radius=24, fill=(60, 40, 20, 70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([m, m, W - m, H - m], radius=24, fill=(252, 246, 231, 232), outline=(205, 178, 132, 255),
                        width=3)
    d.text((m + px - l, m + py - t_), text, font=font, fill=SPEAKER_COLORS.get(speaker, SPEAKER_COLORS["N"]))
    return im


class Subtitles:
    def __init__(self, ctx, fade=0.16):
        self.fade = fade
        self.items = []
        # One subtitle per chunk (falls back to one per line); each stays up until the next appears
        # or shortly after the speech ends.
        pieces = []
        for ln in ctx.lines:
            for c in (ln.chunks or [ln]):
                # a very short chunk ('可是，') would flash for ~0.4 s: show it together with the next one
                if (pieces and pieces[-1][5] is ln and c.start - pieces[-1][2] < 0.9
                        and len(pieces[-1][0]) + len(c.text) <= 24):
                    text, spk, start, _, line_end, _ = pieces.pop()
                    pieces.append((text + c.text, spk, start, c.end, line_end, ln))
                else:
                    pieces.append((c.text, ln.speaker, c.start, c.end, ln.end, ln))
        pieces = [p[:5] for p in pieces]
        for i, (text, spk, start, end, line_end) in enumerate(pieces):
            t0 = max(0.0, start - 0.08)
            t1 = min(end, line_end) + 0.3
            if i + 1 < len(pieces):
                t1 = min(t1, pieces[i + 1][2] - 0.06)
            t1 = min(t1, ctx.duration - 0.3)
            img = to_pm(subtitle_image(text, spk))
            self.items.append((t0, t1, img))

    def draw(self, frame, t):
        for t0, t1, img in self.items:
            if t0 <= t <= t1:
                a = min(1.0, (t - t0) / self.fade, (t1 - t) / self.fade)
                h, w = img.shape[:2]
                x = (OUT_W - w) // 2
                y = OUT_H - 34 - h
                composite_pm(frame, img if a >= 0.999 else cv2.convertScaleAbs(img, alpha=a), x, y)


# --------------------------------------------------------------------- rendering


class Renderer:
    def __init__(self, scene, subtitles=None, paper=None):
        self.scene = scene
        self.items = prepare(scene)
        raster.close()
        show_subs = scene.subtitles if subtitles is None else subtitles
        self.subs = Subtitles(scene.ctx) if show_subs else None
        strength = scene.paper if paper is None else paper
        self.paper = (np.minimum(WC.paper_multiplier(OUT_W, OUT_H, 42, strength), 255).astype(np.uint8)
                      if strength > 0 else None)

    def frame_array(self, t):
        """Render one frame as an RGB uint8 numpy array (OUT_H, OUT_W, 3)."""
        sc = self.scene
        cam = sc.camera(t)
        C = cam_matrix(cam)
        frame = np.empty((OUT_H, OUT_W, 3), np.uint8)
        frame[:] = (243, 233, 210)
        for item in self.items:
            _draw_item(frame, item, t, C)
        if sc.fx:
            view = View(C, OUT_W / cam.w, t)
            im = Image.fromarray(frame).convert("RGBA")
            for fx in sc.fx:
                res = fx(im, t, view)
                if res is not None:
                    im = res
            frame = np.ascontiguousarray(np.asarray(im.convert("RGB")))
        if self.paper is not None:
            frame = cv2.multiply(frame, self.paper, scale=1 / 255.0)
        if self.subs:
            self.subs.draw(frame, t)
        return frame

    def frame(self, t):
        return Image.fromarray(self.frame_array(t))


def frame_times(duration):
    n = int(round(duration * FPS))
    return [i / FPS for i in range(n)]


def render_video(scene, out_path, crf=12, preset="veryfast"):
    r = Renderer(scene)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OUT_W}x{OUT_H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
           "-pix_fmt", "yuv420p", str(out_path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for t in frame_times(scene.ctx.duration):
        p.stdin.write(r.frame_array(t).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {out_path}")


def render_stills(scene, times, out_dir, prefix=None, subtitles=None):
    r = Renderer(scene, subtitles=subtitles)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in times:
        p = out_dir / f"{prefix or scene.ctx.id}_{t:06.2f}.png"
        r.frame(t).save(p)
        paths.append(p)
    return paths
