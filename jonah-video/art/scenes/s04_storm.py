"""Scene 4 — the storm (Jonah 1:4-5).

Line 0  God hurls a great wind on the sea: after a calm, readable first beat dark clouds roll in, big rounded
        foam-crested waves heave, rain, lightning (bold tapering bolts reaching out of the cloud undersides).
Line 1  The ship pitches hard (about +-10 deg), the sail tears at the first flash peak (scraps fly off downwind),
        a wave bursts over the bow, the camera shakes.
Line 2  The frightened sailors (one prays to his god) heave a jar, a crate, another jar and a sack overboard:
        hard pose cuts sold by keyed lean / squash, each piece flies in a spinning arc and splashes into the sea.
Line 3  The hull opens in cutaway and the camera holds the contrast (crew panicking above, Jonah asleep below)
        through '约拿却躺在船舱底下'; then it dives in: the outside darkens, the hold painting blooms outward from
        the hull opening, and on '呼呼大睡' we are in the warm lantern-lit hold where Jonah sleeps on grain sacks,
        breathing in time with the snore, 'Z z z' drifting up, rain and flickers still visible through the hatch.
        As the line ends the picture dips to (warm) black, fully dark by the first frames of the cross-dissolve:
        s05 opens on its own, slightly different drawing of this hold, and dissolving one into the other read as
        double vision (two lanterns, two ladders, doubled jars). s05 now fades up out of the dark instead.

Stage 2400 x 1350. Everything aboard shares one ship transform ``ship_tf(t)``; the hold is a separate
full-resolution painting attached to the ship at scale K (its Jonah sits exactly on the cutaway's Jonah, its
cargo is laid out like the cutaway's), so the camera can zoom into it without blur.
"""
import json
import math
import random
from dataclasses import replace

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import CACHE, OUT_H, OUT_W
from engine.scene import Scene

W, H = 2400, 1350
INK = S.INK

# ---------------------------------------------------------------- ship geometry (stage px, un-rotated)
SS = 0.92                      # ship / crew scale
SF = -1                        # bow to the left: sailing west toward Tarshish
SX, SY = 1230.0, 985.0         # ship anchor = hull centre on the waterline
PIV = (SX, SY + 40.0)          # pitch pivot (a little under the waterline)
DECK = SY + PR.SHIP_DECK_Y * SS

# hold painting: its own 2400 x 1350 canvas, framed around Q0, attached to the ship at scale K
Q0 = (1215.0, 712.0)
V0 = (1215.0, 627.0)           # painting point at the centre of the final view (high enough to show the hatch)
JS = 1.75                      # Jonah's scale inside the painting
J_PAINT = (1080.0, 1000.0)     # Jonah's anchor in the painting
K = SS / JS                    # painting px -> stage px
VIEW_W_INT = 1900.0            # painting px across the frame when the dive ends
LANTERN_HOOK = (1150.0, 322.0)
HATCH = (1690, 1990)           # hatch opening x range in the painting
HATCH_Y = (150, 256)           # hatch opening y range (the deck beam runs across below it)

# where '呼呼大睡' starts, as a fraction of narration line 3 (measured on the voice take: the comma pause sits
# at 0.64-0.70 of the line)
L3_SLEEP_FRAC = 0.66

# cool storm light over everything outside (ship, crew, cargo); the lanterns and the hold stay warm
GRADE_DEFS = ('<filter id="stormgrade" x="-5%" y="-5%" width="110%" height="110%" '
              'color-interpolation-filters="sRGB">'
              '<feColorMatrix type="saturate" values="0.84"/>'
              '<feColorMatrix type="matrix" values="0.87 0 0 0 0  0 0.9 0 0 0  0 0 0.97 0 0.012  0 0 0 1 0"/>'
              '</filter>')


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=H)


def graded(markup):
    return f'<g filter="url(#stormgrade)">{markup}</g>'


def ship_pt(lx, ly):
    """Ship-local point -> stage (un-rotated ship)."""
    return PR.local_to_stage(SX, SY, SS, SF, lx, ly)


def deck_y_at(x):
    """Stage y of the deck / hull top at stage x (the deck rises toward bow and stern)."""
    lx = (x - SX) / (SS * SF)
    return SY + (PR.SHIP_DECK_Y - 75 * (abs(lx) / 480) ** 3.2) * SS


def opening_rect():
    """The cutaway hold opening (props.SHIP_INTERIOR) in stage px, un-rotated ship: (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = PR.SHIP_INTERIOR
    (ax, ay), (bx, by) = ship_pt(x0, y0), ship_pt(x1, y1)
    return min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)


# ---------------------------------------------------------------- transforms

def apply(tf, x, y):
    px = tf.px if tf.px is not None else 0.0
    py = tf.py if tf.py is not None else 0.0
    r = math.radians(tf.rot)
    c, s = math.cos(r), math.sin(r)
    X, Y = (x - px) * tf.sx, (y - py) * tf.sy
    return px + tf.dx + c * X - s * Y, py + tf.dy + s * X + c * Y


def compose(a, b):
    """Transform 'a after b' (b applied first); b must carry its pivot. a must have a uniform scale."""
    qx, qy = apply(a, b.px + b.dx, b.py + b.dy)
    return Tf(qx - b.px, qy - b.py, a.rot + b.rot, a.sx * b.sx, a.sy * b.sy, a.alpha * b.alpha, b.px, b.py)


def keyc(keys, curves="sine"):
    """Piecewise eased scalar keyframes [(t, v), ...] -> f(t); ``curves`` is one easing name or one per segment."""
    keys = sorted(keys, key=lambda k: k[0])
    cv = curves if isinstance(curves, (list, tuple)) else [curves] * max(1, len(keys) - 1)

    def f(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for i, ((t0, a), (t1, b)) in enumerate(zip(keys, keys[1:])):
            if t0 <= t <= t1:
                return a + (b - a) * M.progress(t, t0, t1, cv[min(i, len(cv) - 1)])
        return keys[-1][1]
    return f


keyf = keyc


def integrate(freq, t0, t1, n_per_s=240):
    ts = np.linspace(t0, t1, int((t1 - t0) * n_per_s) + 2)
    fr = np.array([freq(t) for t in ts])
    ph = np.concatenate([[0.0], np.cumsum((fr[1:] + fr[:-1]) / 2 * np.diff(ts))])
    return lambda t: float(np.interp(t, ts, ph))


def bolt_alpha(u):
    """A bolt stays on screen ~0.35 s with a flicker, then fades."""
    if u < 0 or u > 0.6:
        return 0.0
    return min(1.0, 1.0 - 0.4 * math.exp(-((u - 0.1) / 0.03) ** 2)) * (1 - M.progress(u, 0.32, 0.6, "sine"))


def flick(u):
    """Lightning envelope (same shape as engine.fx.lightning), u = seconds since the strike."""
    if u < 0 or u > 0.45:
        return 0.0
    return min(1.0, max(math.exp(-((u - 0.03) / 0.03) ** 2), 0.7 * math.exp(-((u - 0.16) / 0.05) ** 2))
               + 0.25 * math.exp(-u / 0.2))


# ---------------------------------------------------------------- snore -> breathing

def snore_inhale_peaks(scene_id, at, dur):
    """Scene times at which the snore cue (as audio/mix.py will render it: same seed, rate and length) reaches the
    end of each inhale. Cached on disk; [] if the sound library is unavailable."""
    key = f"{scene_id}:snore:{float(at)}:{float(dur):.4f}"
    path = CACHE / "s04_snore_peaks.json"
    try:
        cache = json.loads(path.read_text())
    except Exception:
        cache = {}
    if key in cache:
        return [at + p for p in cache[key]]
    try:
        import zlib

        from scipy import signal

        from audio import sfx
        from engine.paths import SR
        seed = zlib.crc32(f"{scene_id}:snore:{float(at)}".encode()) & 0xFFFF
        x = np.asarray(sfx.make("snore", dur, SR, seed=seed), np.float64)
        x = x.mean(axis=1) if x.ndim == 2 else x
        y = signal.sosfiltfilt(signal.butter(4, (150, 360), "bandpass", fs=SR, output="sos"), x)
        hop = SR // 100                                     # 10 ms blocks
        nb = len(y) // hop
        e = (y[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1)
        env = np.sqrt(np.convolve(e, np.ones(6) / 6, "same"))
        pk, _ = signal.find_peaks(env, height=0.4 * env.max(), distance=200)
        rel = [round(i / 100, 3) for i in pk]
    except Exception:
        return []
    cache[key] = rel
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache))
    except Exception:
        pass
    return [at + p for p in rel]


def breath_curve(peaks, per=3.5, rise=1.3, fall=1.55):
    """Chest in [-1, 1]: rises over the inhale to a maximum at each inhale end, sinks over the whistling exhale,
    rests between cycles. Extrapolated with ``per`` before / after the known cycles."""
    if not peaks:
        return lambda t: math.sin(2 * math.pi * t / per)
    pk = sorted(peaks)
    cand = [pk[0] - per * j for j in range(1, 6)] + pk + [pk[-1] + per * j for j in range(1, 6)]

    def f(t):
        v = -1.0
        for p in cand:
            if p - rise <= t <= p:
                v = max(v, -1 + 2 * M.progress(t, p - rise, p, "sine"))
            elif p < t <= p + fall:
                v = max(v, 1 - 2 * M.progress(t, p, p + fall, "sine"))
        return v
    return f


# ---------------------------------------------------------------- drawing helpers


def fm(v):
    return f"{v:.1f}"


def puffs(circles, fill, sw=4.0, shade=None, hi=None, cid=None, hi_op=0.5):
    """Union of circles with a single outer ink outline; optional soft underside shade / top highlights
    (both clipped to the union)."""
    out = "".join(f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(r + sw)}" fill="{INK}"/>' for x, y, r in circles)
    out += "".join(f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(r)}" fill="{fill}"/>' for x, y, r in circles)
    inner = ""
    if shade:
        col, (ex, ey, erx, ery), op = shade
        inner += (f'<ellipse cx="{fm(ex)}" cy="{fm(ey)}" rx="{fm(erx)}" ry="{fm(ery)}" fill="{col}" '
                  f'opacity="{op}" filter="url(#soft)"/>')
    if hi:
        for x, y, r in circles:
            if r > 10:
                inner += (f'<circle cx="{fm(x - 0.16 * r)}" cy="{fm(y - 0.24 * r)}" r="{fm(0.62 * r)}" '
                          f'fill="{hi}" opacity="{hi_op}"/>')
    if inner and cid:
        clip = "".join(f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(r)}"/>' for x, y, r in circles)
        out += f'<clipPath id="{cid}">{clip}</clipPath><g clip-path="url(#{cid})">{inner}</g>'
    return out


def storm_cloud(cx, cy, w, h, seed, fill, under, rim, sw=4.0):
    """Puffy, rounded storm cloud: a few big top puffs, a scalloped round bottom, a dark underside and a soft
    light rim along the top (both clipped inside the outline)."""
    r = random.Random(seed)
    circ = []
    n = 4
    for i in range(n):
        u = (i + 0.5) / n
        rad = h * (0.36 + 0.3 * math.sin(math.pi * u)) * r.uniform(0.88, 1.12)
        circ.append((cx - w * 0.42 + w * 0.84 * u + r.uniform(-0.03, 0.03) * w,
                     cy - rad * 0.3 + r.uniform(-0.05, 0.05) * h, rad))
    for i in range(4):
        u = (i + 0.5) / 4
        circ.append((cx - w * 0.38 + w * 0.76 * u, cy + h * 0.2, h * 0.3 * r.uniform(0.9, 1.1)))
    cid = f"sc{seed}"
    out = puffs(circ, fill, sw, shade=(under, (cx, cy + h * 0.45, w * 0.55, h * 0.32), 0.8), cid=cid)
    hl = "".join(f'<ellipse cx="{fm(x - 0.12 * rad)}" cy="{fm(y - 0.55 * rad)}" rx="{fm(0.6 * rad)}" '
                 f'ry="{fm(0.32 * rad)}" fill="{rim}" opacity="0.38"/>' for x, y, rad in circ[:n])
    clip = "".join(f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(rad)}"/>' for x, y, rad in circ)
    out += (f'<clipPath id="{cid}h">{clip}</clipPath><g clip-path="url(#{cid}h)"><g filter="url(#soft)">{hl}</g></g>')
    return out


def peaky(theta, p):
    """Wave profile in [-1, 1]: -1 at the crest (sharpish), +1 in the trough (broad)."""
    return 1 - 2 * ((1 + math.sin(theta)) / 2) ** p


def wave_fn(y0, amp, wl, phase, p=2.0, lean=0.35):
    """y0 / amp may be numbers or functions of x."""
    y0f = y0 if callable(y0) else (lambda x: y0)
    af = amp if callable(amp) else (lambda x: amp)

    def f(x):
        th = 2 * math.pi * x / wl + phase
        th += lean * math.sin(th)
        return y0f(x) + af(x) * peaky(th, p)
    return f


def band_path(f, x0=-80, x1=W + 80, step=14, bottom=H + 80):
    pts = [(x, f(x)) for x in np.arange(x0, x1 + step, step)]
    d = S.smooth_path(pts, closed=False)
    return d + f" L{x1 + step:.1f},{bottom} L{x0:.1f},{bottom} Z", pts


def crests(f, x0, x1, step=6):
    xs = np.arange(x0, x1, step)
    ys = np.array([f(x) for x in xs])
    out = []
    for i in range(1, len(xs) - 1):
        if ys[i] <= ys[i - 1] and ys[i] < ys[i + 1]:
            out.append((float(xs[i]), float(ys[i])))
    return out


def foam_cap(f, xc, wl, amp, seed, size=1.0, sw=3.0):
    """Bubbly foam riding a crest, a drooping lip on the downwind (left) face, spray dots, lace below."""
    r = random.Random(seed)
    half = 0.17 * wl * size
    rb = (9 + 0.2 * amp) * size
    circ = []
    n = max(5, int(2 * half / (rb * 0.9)))
    for i in range(n):
        u = -1 + 2 * i / (n - 1)
        x = xc + u * half
        rad = rb * (0.5 + 0.5 * (1 - abs(u)) ** 0.7) * r.uniform(0.85, 1.12)
        circ.append((x, f(x) + 0.3 * rad, rad))
    # lip curling down the leeward face
    xl = xc - half * 0.85
    circ.append((xl - rb * 0.25, f(xl) + rb * 0.95, rb * 0.62))
    circ.append((xl - rb * 0.05, f(xl) + rb * 1.75, rb * 0.4))
    out = puffs(circ, P["foam"], sw, shade=(P["sea_pale"], (xc, f(xc) + rb * 1.3, half * 1.1, rb * 0.8), 0.8),
                cid=f"fc{seed}")
    lace = ""
    for k, off in enumerate((0.55, 1.05)):
        xa, xb = xc - half * (1.3 + 0.4 * k), xc + half * (1.1 + 0.3 * k)
        pts = [(x, f(x) + amp * off + 10 + 6 * math.sin(x * 0.05 + seed)) for x in np.linspace(xa, xb, 9)]
        lace += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["foam"]}" '
                 f'stroke-width="{4.5 * size:.1f}" stroke-dasharray="{fm(30 * size)} {fm(16 * size)}" '
                 f'stroke-linecap="round" opacity="{0.55 - 0.15 * k}"/>')
    dots = ""
    for k in range(3):
        dx = r.uniform(-half * 0.9, half * 0.4)
        dy = -rb * r.uniform(1.3, 2.6)
        rr = r.uniform(3.5, 6.5) * size
        dots += (f'<circle cx="{fm(xc + dx)}" cy="{fm(f(xc + dx) + dy)}" r="{fm(rr)}" fill="{P["foam"]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
    return lace + out + dots


def sea_layer(f, fill, light, dark, wl, amp, seed, x0=-80, x1=W + 80, foam_size=1.0, sw=4.5, cap_amp=None):
    d, pts = band_path(f, x0, x1)
    body = S.path(d, fill=fill, sw=sw)
    hl = S.smooth_path([(x, y + 14 + 0.12 * amp) for x, y in pts], closed=False)
    body += (f'<path d="{hl}" fill="none" stroke="{light}" stroke-width="{12 + 0.2 * amp:.1f}" opacity="0.4" '
             f'stroke-linecap="round"/>')
    r = random.Random(seed)
    for xc, yc in crests(f, x0, x1):
        y = yc + amp * 1.6 + r.uniform(10, 30)
        xa, xb = xc - wl * r.uniform(0.2, 0.32), xc + wl * r.uniform(0.15, 0.3)
        body += (f'<path d="M{fm(xa)},{fm(y)} Q{fm((xa + xb) / 2)},{fm(y - 16 - 0.15 * amp)} {fm(xb)},{fm(y + 8)}" '
                 f'fill="none" stroke="{dark}" stroke-width="6" opacity="0.35" stroke-linecap="round"/>')
    caps = ""
    for i, (xc, yc) in enumerate(crests(f, x0 + 30, x1 - 30)):
        a = cap_amp(xc) if cap_amp else amp
        caps += foam_cap(f, xc, wl, a, seed * 31 + i, foam_size * (0.75 + 0.25 * min(1.0, a / max(amp, 1))))
    return S.g(body, filter="wobble") + S.g(caps, filter="wobble-fine")


def burst(x, y, s=1.0, seed=0, n=5, spread=62, height=150, lean=0.0):
    """Picture-book splash: foam tongues fanning up from a foamy base, plus flying droplets."""
    r = random.Random(seed)
    circ = []
    for k in range(n):
        a = math.radians(lean - spread + 2 * spread * k / (n - 1) + r.uniform(-6, 6))
        L = height * s * (0.65 + 0.5 * (1 - abs(k - (n - 1) / 2) / ((n - 1) / 2))) * r.uniform(0.85, 1.1)
        for j in range(7):
            v = j / 6
            px = x + math.sin(a) * L * v * (1 + 0.25 * v)
            py = y - math.cos(a) * L * v
            circ.append((px, py, s * (24 - 13 * v)))
    for u in np.linspace(-1, 1, 7):
        circ.append((x + u * 80 * s, y + 4 * s, s * 24 * (1 - 0.45 * abs(u))))
    out = puffs(circ, P["foam"], 3.5, shade=(P["sea_pale"], (x, y + 10 * s, 70 * s, 30 * s), 0.8), cid=f"bu{seed}")
    for k in range(7):
        a = math.radians(lean - spread - 10 + (2 * spread + 20) * k / 6 + r.uniform(-8, 8))
        dist = height * s * r.uniform(1.05, 1.35)
        rr = s * r.uniform(6, 10)
        out += (f'<circle cx="{fm(x + math.sin(a) * dist)}" cy="{fm(y - math.cos(a) * dist)}" r="{fm(rr)}" '
                f'fill="{P["foam"]}" stroke="{INK}" stroke-width="2.5"/>')
    return out


def bolt_svg(x, y0, y1, seed, sway=1, w0=34.0):
    """Bold picture-book lightning bolt: a filled, jagged ribbon that is widest at the top (which starts inside a
    cloud bank) and tapers to a point, with one short tapering fork and a soft glow behind."""
    r = random.Random(seed)
    n = 6
    pts = [(x, y0)]
    for i in range(1, n + 1):
        u = i / n
        off = r.uniform(26, 50) if i % 2 else -r.uniform(12, 30)
        pts.append((x + sway * (off + 44 * u), y0 + (y1 - y0) * u))
    hw = [w0 * (1 - i / n) ** 0.8 + 2.0 for i in range(n + 1)]

    def ribbon(cl, ws):
        left, right = [], []
        for i, ((px, py), h) in enumerate(zip(cl[:-1], ws[:-1])):
            notch = 0.0 if i == 0 else 0.45 * h * (1 if i % 2 else -1)
            left.append((px - h, py + notch))
            right.append((px + h, py - notch))
        return left + [cl[-1]] + right[::-1]

    def poly(p):
        return "M" + " L".join(f"{fm(a)},{fm(b)}" for a, b in p) + " Z"

    main = poly(ribbon(pts, hw))
    bx, by = pts[2]
    fork_cl = [(bx, by), (bx - sway * 62, by + 62), (bx - sway * 74, by + 128)]
    fork = poly(ribbon(fork_cl, [hw[2] * 0.55, hw[2] * 0.3, 0]))
    core = "M" + " L".join(f"{fm(a)},{fm(b)}" for a, b in pts[:-1])
    glow = (f'<g filter="url(#bglow)"><path d="{core}" fill="none" stroke="{P["glow"]}" stroke-width="96" '
            f'opacity="0.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    body = (f'<path d="{fork}" fill="#fff0b4" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="{main}" fill="#fff3c2" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="{core}" fill="none" stroke="#fffcef" stroke-width="7" opacity="0.75" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    return glow + S.g(body, filter="wobble-fine")


def scrap_svg(cx, cy, seed, s=1.0):
    """A small torn piece of the striped sail."""
    r = random.Random(seed)
    k = 7
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k + r.uniform(-0.2, 0.2)
        rad = s * r.uniform(0.7, 1.15) * (1 if i % 2 else 0.78)
        pts.append((cx + 34 * rad * math.cos(a), cy + 20 * rad * math.sin(a)))
    d = "M" + " L".join(f"{fm(a)},{fm(b)}" for a, b in pts) + " Z"
    cid = f"scr{seed}"
    stripe = (f'<rect x="{fm(cx - 6 * s)}" y="{fm(cy - 40 * s)}" width="{fm(20 * s)}" height="{fm(80 * s)}" '
              f'fill="{P["sail_stripe"]}" transform="rotate(14 {fm(cx)} {fm(cy)})"/>')
    return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<path d="{d}" fill="{P["sail"]}"/><g clip-path="url(#{cid})">{stripe}</g>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')


def wind_svg(x, y, L, seed, curl=1.0):
    """Curly picture-book gust: a long wavy stroke ending in a curl at its leading (left, downwind) end, plus a
    shorter parallel stroke."""
    r = random.Random(seed)
    ph = r.uniform(0, 1)

    def line(x_, y_, L_, curl_):
        pts = [(x_ + L_ / 2 - L_ * u, y_ + 16 * math.sin(u * 5.0 + ph)) for u in np.linspace(0, 1, 9)]
        if curl_:
            ex, ey = pts[-1]
            R = 34 * curl_
            cx, cy = ex - 4, ey - R
            for k in range(1, 10):
                a = math.radians(90 + 36 * k)
                rr = R * (1 - 0.06 * k)
                pts.append((cx - rr * math.cos(a), cy + rr * math.sin(a)))
        return S.smooth_path(pts, closed=False)
    out = ""
    for d, w in ((line(x, y, L, curl), 1.0), (line(x + 0.12 * L, y + 46, 0.62 * L, 0), 0.8)):
        out += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{17 * w:.1f}" stroke-linecap="round"/>'
        out += f'<path d="{d}" fill="none" stroke="#eef2ef" stroke-width="{10 * w:.1f}" stroke-linecap="round"/>'
    return out


def pennant_pts(phase):
    """Masthead pennant streaming downwind (ship-local coords, facing 1 = toward the bow)."""
    top, bot = [], []
    for k in range(9):
        u = k / 8
        fl = 9 * u * math.sin(2 * math.pi * 1.2 * u - phase)
        top.append((-10 + 150 * u, -936 - 4 * u + fl))
        bot.append((-10 + 150 * u, -902 - 30 * u + fl))
    return top + bot[::-1]



BOLT_DEFS = '<filter id="bglow" x="-300%" y="-30%" width="700%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>'


# ---------------------------------------------------------------- frame effects (local versions)

def rain_fx(t0, t1, density=1.0, angle=-15, length=42, speed=1750, color=(222, 232, 242), alpha=80, width=2,
            seed=5, hole=None):
    """Like engine.fx.rain, but each streak trails behind its drop (aligned with the motion).
    hole(t, view) -> list of output-px points or None: a polygon kept free of rain (the open hold)."""
    n = int(420 * density)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = speed * rng.uniform(0.75, 1.25, n)
    ln = length * rng.uniform(0.6, 1.3, n)
    al = rng.uniform(0.55, 1.0, n)
    a = math.radians(angle)
    dx, dy = math.sin(a), math.cos(a)

    def fx(frame, t, view):
        k = 0.0
        if t0 <= t <= t1:
            k = min(1.0, M.progress(t, t0, t0 + 0.6, "sine"), 1 - M.progress(t, t1 - 0.6, t1, "sine"))
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0 + sp * t) % (OUT_H + 80) - 40
        x = (x0 + sp * t * dx / dy) % (OUT_W + 400) - 200
        for i in range(n):
            d.line([(x[i], y[i]), (x[i] - ln[i] * dx, y[i] - ln[i] * dy)], fill=(*color, int(alpha * k * al[i])),
                   width=width)
        poly = hole(t, view) if hole else None
        if poly:
            d.polygon(poly, fill=(0, 0, 0, 0))
        frame.alpha_composite(ov)
        return frame
    return fx


def flash_fx(strikes, color=(236, 240, 255)):
    def fx(frame, t, view):
        s = max([st * flick(t - ts) for ts, st in strikes] + [0.0])
        if s <= 0.01:
            return frame
        return Image.alpha_composite(frame, Image.new("RGBA", frame.size, (*color, int(255 * min(1.0, s)))))
    return fx


def dip_fx(t0, t1, color=(20, 12, 8)):
    """Fade the whole frame to a warm near-black between t0 and t1 and keep it dark until the scene ends."""
    def fx(frame, t, view):
        k = M.progress(t, t0, t1, "sine")
        if k <= 0:
            return frame
        dark = Image.new("RGBA", frame.size, (*color, 255))
        return dark if k >= 1 else Image.blend(frame, dark, k)
    return fx


def motes_fx(region_fn, count, t0, color=(255, 236, 190), seed=13):
    """Warm dust floating in the lantern light; region_fn(t) -> (x0, y0, x1, y1) in stage px."""
    rng = np.random.default_rng(seed)
    px, py = rng.uniform(0, 1, count), rng.uniform(0, 1, count)
    vx, vy = rng.uniform(-0.012, 0.012, count), rng.uniform(-0.03, -0.004, count)
    sz, ph = rng.uniform(1.8, 4.0, count), rng.uniform(0, 6.28, count)

    def fx(frame, t, view):
        k = M.progress(t, t0, t0 + 0.8, "sine")
        if k <= 0:
            return frame
        x0, y0, x1, y1 = region_fn(t)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            u = (px[i] + vx[i] * t + 0.012 * math.sin(t * 0.7 + ph[i])) % 1.0
            v = (py[i] + vy[i] * t) % 1.0
            ox, oy = view.to_out(x0 + (x1 - x0) * u, y0 + (y1 - y0) * v)
            rr = sz[i] * view.scale
            a = int(150 * k * (0.5 + 0.5 * math.sin(t * 1.3 + ph[i])) * math.sin(math.pi * v))
            d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


# ---------------------------------------------------------------- the hold painting

def hatch_slats():
    """Grating over the hatch opening (also drawn over the hatch rain layer)."""
    hx0, hx1 = HATCH
    hy0, hy1 = HATCH_Y
    wood = P["wood"]
    out = ""
    for x in range(hx0 + 45, hx1, 70):
        out += f'<rect x="{x - 9}" y="{hy0}" width="18" height="{hy1 - hy0 + 4}" fill="{wood}" stroke="{INK}" stroke-width="4"/>'
    out += (f'<rect x="{hx0}" y="{hy0 + 44}" width="{hx1 - hx0}" height="15" fill="{wood}" stroke="{INK}" '
            f'stroke-width="4"/>')
    return out


def hatch_rain_svg(seed):
    """Rain streaks seen through the hatch (one frame of a small boil loop)."""
    hx0, hx1 = HATCH
    hy0, hy1 = HATCH_Y
    r = random.Random(seed)
    lines = ""
    for _ in range(26):
        x, y = r.uniform(hx0 + 4, hx1 + 20), r.uniform(hy0 - 30, hy1 - 6)
        L = r.uniform(26, 44)
        lines += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 0.3 * L:.0f}" y2="{y + L:.0f}" stroke="#dde7f0" '
                  f'stroke-width="3.5" stroke-linecap="round" opacity="{r.uniform(0.45, 0.85):.2f}"/>')
    clip = f'<clipPath id="hrc"><rect x="{hx0 + 3}" y="{hy0 + 3}" width="{hx1 - hx0 - 6}" height="{hy1 - hy0}"/></clipPath>'
    return doc(f'{clip}<g clip-path="url(#hrc)">{lines}</g>' + S.g(hatch_slats(), filter="wobble-fine"))


def hold_svg(clip=None):
    """The hold painting. clip=(x0, y0, x1, y1, feather): only a soft-edged rectangle of it (reveal stages)."""
    wd, wood, wl = P["wood_dark"], P["wood"], P["wood_light"]
    rope = S.mix(P["sackcloth"], P["sand"], 0.35)
    defs = (S.lin_grad("hf", [(0, S.mix(wl, wood, 0.3)), (1, S.mix(wood, wd, 0.55))])
            + S.lin_grad("hatchsky", [(0, P["storm_sky_top"]), (1, P["storm_sky"])])
            + S.lin_grad("shaft", [(0, "#c9dbea", 0.35), (1, "#c9dbea", 0.0)])
            + S.rad_grad("lampglow", [(0, "#ffe9b0", 0.6), (0.4, P["gold"], 0.25), (1, P["gold"], 0.0)])
            + S.rad_grad("vig", [(0, "#2a160e", 0.0), (0.55, "#2a160e", 0.0), (1, "#2a160e", 0.62)], cx=0.47, cy=0.6,
                         r=0.6)
            + '<filter id="edgeblur" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="14"/></filter>'
            + f'<mask id="edgefade"><rect x="34" y="34" width="{W - 68}" height="{H - 68}" fill="#fff" filter="url(#edgeblur)"/></mask>')

    def sheer(x, y):
        return y - 60 * ((x - 1200) / 1300) ** 2

    b = ""
    # hull planking: bands of slightly different wood tones following the sheer
    tones = [S.mix(wd, wood, 0.42), S.mix(wd, wood, 0.55), S.mix(wd, wood, 0.36), S.mix(wd, wood, 0.5)]
    ys = list(range(230, 1130, 60))
    planks = S.rect_bg(S.mix(wd, wood, 0.45), W, H)
    rr = random.Random(2)
    for i, y in enumerate(ys):
        top = [(x, sheer(x, y)) for x in range(-60, W + 120, 120)]
        bot = [(x, sheer(x, y + 60)) for x in range(W + 60, -120, -120)]
        planks += S.path(S.smooth_path(top + bot, closed=True, tension=0.5), fill=tones[i % 4], sw=3.5)
        for k in range(4):
            xx = rr.uniform(120, 2280)
            yy = sheer(xx, y + 30)
            planks += f'<line x1="{xx:.0f}" y1="{yy - 28:.0f}" x2="{xx + 3:.0f}" y2="{yy + 28:.0f}" stroke="{INK}" stroke-width="3.5"/>'
            for dxn in (-14, 14):
                planks += f'<circle cx="{xx + dxn:.0f}" cy="{yy - 14:.0f}" r="3.5" fill="{S.shade(wd, -0.3)}"/>'
                planks += f'<circle cx="{xx + dxn:.0f}" cy="{yy + 14:.0f}" r="3.5" fill="{S.shade(wd, -0.3)}"/>'
        for k in range(3):   # wood grain
            xx = rr.uniform(0, 2300)
            yy = sheer(xx, y + rr.uniform(16, 44))
            planks += f'<path d="M{xx:.0f},{yy:.0f} q90,-6 180,2" fill="none" stroke="{S.shade(wd, -0.2)}" stroke-width="3" opacity="0.45"/>'
    b += S.g(planks, filter="wobble")
    # ribs
    ribs = ""
    for x in (330, 760, 1580, 2080):
        bend = 40 if x < 1200 else -40
        d = f"M{x - 20},230 Q{x + bend},700 {x - 10},1120"
        ribs += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="70" stroke-linecap="round"/>'
        ribs += f'<path d="{d}" fill="none" stroke="{S.mix(wood, wd, 0.2)}" stroke-width="60" stroke-linecap="round"/>'
        ribs += f'<path d="{d}" fill="none" stroke="{wl}" stroke-width="12" opacity="0.5" transform="translate(-14,0)"/>'
        ribs += f'<path d="{d}" fill="none" stroke="{S.shade(wd, -0.3)}" stroke-width="10" opacity="0.5" transform="translate(18,0)"/>'
    b += S.g(ribs, filter="wobble")
    # two spare oars resting on pegs along the wall: round shafts tapering into darker flat blades
    oars = ""
    blade_col = S.mix(wood, wd, 0.35)
    for y, x0_, x1_ in ((575, 250, 1010), (640, 300, 1060)):
        xs = x1_ - 236
        oars += f'<path d="M{x0_},{y} L{xs + 30},{y - 2}" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/>'
        oars += f'<path d="M{x0_},{y} L{xs + 30},{y - 2}" fill="none" stroke="{wl}" stroke-width="15" stroke-linecap="round"/>'
        oars += f'<path d="M{x0_ + 10},{y - 4} L{xs},{y - 6}" stroke="{S.shade(wl, 0.3)}" stroke-width="3" opacity="0.6"/>'
        blade = (f"M{xs},{y - 8} C{xs + 70},{y - 10} {xs + 110},{y - 36} {x1_ - 52},{y - 36} "
                 f"Q{x1_ + 4},{y - 34} {x1_ + 4},{y - 4} Q{x1_ + 4},{y + 28} {x1_ - 52},{y + 28} "
                 f"C{xs + 110},{y + 28} {xs + 70},{y + 6} {xs},{y + 6} Z")
        oars += S.path(blade, fill=blade_col, sw=4.5)
        oars += (f'<path d="M{xs + 40},{y - 12} C{xs + 90},{y - 18} {xs + 130},{y - 28} {x1_ - 52},{y - 28} '
                 f'Q{x1_ - 6},{y - 27} {x1_ - 4},{y - 6}" fill="none" stroke="{wl}" stroke-width="4" opacity="0.7"/>')
        oars += (f'<path d="M{xs + 12},{y - 1} L{x1_ - 24},{y - 3}" fill="none" stroke="{S.shade(wd, -0.25)}" '
                 f'stroke-width="3.5" opacity="0.55"/>')
    for x in (440, 640):
        oars += f'<rect x="{x - 10}" y="558" width="20" height="104" rx="6" fill="{wd}" stroke="{INK}" stroke-width="4"/>'
    b += S.g(oars, filter="wobble-fine")
    # fishing net and a rope coil hanging on pegs
    net = ""
    for k in range(10):
        net += f'<path d="M{400 + k * 38},282 Q{420 + k * 38},380 {392 + k * 36},468" fill="none" stroke="{rope}" stroke-width="4"/>'
    for k in range(4):
        y = 310 + k * 42
        net += f'<path d="M398,{y} Q560,{y + 26} 742,{y}" fill="none" stroke="{rope}" stroke-width="4"/>'
    net += f'<path d="M380,272 Q560,312 760,272" fill="none" stroke="{INK}" stroke-width="7"/>'
    for x in (380, 760):
        net += f'<circle cx="{x}" cy="272" r="10" fill="{wd}" stroke="{INK}" stroke-width="4"/>'
    b += S.g(net, transform="translate(0,56)", filter="wobble-fine", opacity=0.9)
    b += f'<circle cx="790" cy="742" r="11" fill="{wd}" stroke="{INK}" stroke-width="4"/>'
    b += PR.rope_coil(790, 838, 1.25)
    # ceiling: deck planks from below, the hatch (storm sky, rain, grating) above the long beam
    hx0, hx1 = HATCH
    hy0, hy1 = HATCH_Y
    ceil = f'<rect x="-20" y="-40" width="{W + 40}" height="330" fill="{S.shade(wd, -0.35)}"/>'
    for x in range(-40, W + 40, 95):
        ceil += f'<line x1="{x}" y1="-40" x2="{x}" y2="288" stroke="{INK}" stroke-width="3" opacity="0.5"/>'
    ceil += (f'<rect x="{hx0 - 16}" y="{hy0 - 16}" width="{hx1 - hx0 + 32}" height="{hy1 - hy0 + 40}" '
             f'fill="{S.mix(wood, wd, 0.25)}" stroke="{INK}" stroke-width="5"/>')
    ceil += (f'<rect x="{hx0}" y="{hy0}" width="{hx1 - hx0}" height="{hy1 - hy0 + 20}" fill="url(#hatchsky)" '
             f'stroke="{INK}" stroke-width="4"/>')
    rr = random.Random(5)
    for k in range(12):
        xx, yy = rr.uniform(hx0 + 10, hx1 - 10), rr.uniform(hy0 + 4, hy1 - 30)
        ceil += f'<line x1="{xx:.0f}" y1="{yy:.0f}" x2="{xx - 8:.0f}" y2="{yy + 26:.0f}" stroke="#d6e2ee" stroke-width="3" opacity="0.35"/>'
    ceil += hatch_slats()
    ceil += f'<rect x="{hx0 - 16}" y="{hy0 - 16}" width="{hx1 - hx0 + 32}" height="10" fill="{wl}" opacity="0.5"/>'
    ceil += f'<rect x="-20" y="256" width="{W + 40}" height="60" fill="{S.mix(wood, wd, 0.3)}" stroke="{INK}" stroke-width="5"/>'
    ceil += f'<rect x="-20" y="261" width="{W + 40}" height="12" fill="{wl}" opacity="0.45"/>'
    for x in (330, 760, 1580, 2080):
        ceil += f'<rect x="{x - 36}" y="244" width="72" height="82" rx="8" fill="{wood}" stroke="{INK}" stroke-width="5"/>'
    b += S.g(ceil, filter="wobble")
    b += (f'<path d="M{hx0 + 20},296 L{hx1 - 20},296 L{hx1 + 160},1110 L{hx0 + 40},1110 Z" fill="url(#shaft)" '
          f'filter="url(#blur-md)"/>')
    # ladder up to the hatch
    lad = ""
    rails = ((hx0 + 50, hx0 + 200), (hx1 - 60, hx1 + 90))
    for x0_, x1_ in rails:
        lad += f'<path d="M{x0_},300 L{x1_},1112" fill="none" stroke="{INK}" stroke-width="32" stroke-linecap="round"/>'
        lad += f'<path d="M{x0_},300 L{x1_},1112" fill="none" stroke="{wl}" stroke-width="22" stroke-linecap="round"/>'
    for k in range(1, 9):
        u = k / 9
        ya = 300 + 812 * u
        xa = rails[0][0] + (rails[0][1] - rails[0][0]) * u
        xb = rails[1][0] + (rails[1][1] - rails[1][0]) * u
        lad += f'<line x1="{xa:.0f}" y1="{ya:.0f}" x2="{xb:.0f}" y2="{ya:.0f}" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
        lad += f'<line x1="{xa:.0f}" y1="{ya:.0f}" x2="{xb:.0f}" y2="{ya:.0f}" stroke="{wood}" stroke-width="12" stroke-linecap="round"/>'
    b += S.g(lad, filter="wobble-fine")
    # floor (a little puddle under the hatch)
    fl = f'<path d="M-40,1104 Q1200,1088 {W + 40},1104 L{W + 40},{H + 40} L-40,{H + 40} Z" fill="url(#hf)" stroke="{INK}" stroke-width="5"/>'
    for x in range(-700, W + 800, 150):
        fl += f'<line x1="{1200 + (x - 1200) * 0.6:.0f}" y1="1100" x2="{x:.0f}" y2="{H + 40}" stroke="{INK}" stroke-width="3" opacity="0.38"/>'
    for y in (1170, 1265):
        fl += f'<line x1="-40" y1="{y}" x2="{W + 40}" y2="{y}" stroke="{INK}" stroke-width="3" opacity="0.28"/>'
    fl += f'<ellipse cx="{hx0 + 150}" cy="1150" rx="150" ry="22" fill="{P["storm_sea_light"]}" opacity="0.55" stroke="{INK}" stroke-width="3"/>'
    fl += f'<ellipse cx="{hx0 + 120}" cy="1145" rx="60" ry="7" fill="#dfeaf0" opacity="0.6"/>'
    b += S.g(fl, filter="wobble")
    # cargo laid out like the ship's cutaway: crates and sacks toward the bow (left), amphorae lashed together
    # by the sleeper's head toward the stern (right, before the ladder)
    lc = PR.crate(420, 1050, 1.4, rot=-3) + PR.sack(250, 1122, 1.2, rot=-5, seed=8)
    lc += PR.crate(640, 1026, 1.55) + PR.sack(628, 935, 1.0, seed=5)
    b += lc
    rc = PR.jar(1668, 990, 1.5, rot=-4) + PR.jar(1772, 996, 1.42, rot=5, color=S.mix(P["terracotta"], P["sand"], 0.35))
    rc += f'<path d="M1595,958 Q1720,990 1840,962" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
    rc += f'<path d="M1595,958 Q1720,990 1840,962" fill="none" stroke="{rope}" stroke-width="7" stroke-linecap="round"/>'
    rc += PR.sack(1575, 1121, 1.05, seed=11)
    rc += PR.crate(2190, 1046, 1.5) + PR.sack(2180, 960, 0.95, seed=4)
    b += rc
    # bed of grain sacks with a sack pillow (Jonah lies on it on his own layer)
    jx, jy = J_PAINT
    bed = ""
    segs = ((jx - 250, jx + 20), (jx - 10, jx + 270), (jx + 240, jx + 440))
    for i, (x0_, x1_) in enumerate(segs):
        col = S.mix(P["sackcloth"], P["sand"], 0.12 * i)
        d = (f"M{x0_},{jy + 6} Q{x0_ - 24},{jy + 55} {x0_ + 4},{jy + 108} L{x1_ - 4},{jy + 108} "
             f"Q{x1_ + 24},{jy + 55} {x1_},{jy + 6} Q{(x0_ + x1_) / 2},{jy - 16} {x0_},{jy + 6} Z")
        bed += S.path(d, fill=col, sw=4.5)
        for k in range(4):
            xx = x0_ + (x1_ - x0_) * (k + 1) / 5
            bed += f'<path d="M{xx:.0f},{jy + 12} Q{xx + 6:.0f},{jy + 55} {xx:.0f},{jy + 100}" fill="none" stroke="{P["sackcloth_dark"]}" stroke-width="3" opacity="0.5"/>'
        bed += f'<path d="M{x0_ + 20},{jy + 28} L{x1_ - 20},{jy + 28}" stroke="{P["sackcloth_dark"]}" stroke-width="3" stroke-dasharray="10 9" opacity="0.6"/>'
    px_, py_ = jx + 265, jy - 34
    bed += S.path(S.blob(px_, py_, 135, 56, 0.08, 10, seed=3), fill=S.mix(P["headcloth"], P["sackcloth"], 0.45), sw=4.5)
    bed += f'<path d="M{px_ - 80},{py_ - 10} Q{px_},{py_ + 10} {px_ + 85},{py_ - 12}" fill="none" stroke="{P["sackcloth_dark"]}" stroke-width="3" opacity="0.5"/>'
    bed += S.path(f"M{jx - 300},{jy + 4} Q{jx - 314},{jy - 46} {jx - 268},{jy - 50} L{jx - 180},{jy - 50} "
                  f"Q{jx - 158},{jy - 22} {jx - 180},{jy + 4} Z", fill=P["jonah_sash"], sw=4)
    bed += f'<path d="M{jx - 286},{jy - 24} L{jx - 180},{jy - 24}" stroke="{S.shade(P["jonah_sash"], -0.35)}" stroke-width="3"/>'
    b += S.g(bed, filter="wobble-fine")
    # lantern hook on the beam
    lhx, lhy = LANTERN_HOOK
    b += f'<rect x="{lhx - 18}" y="{lhy - 28}" width="36" height="22" rx="6" fill="{wd}" stroke="{INK}" stroke-width="4"/>'
    # warm lamplight pooling on the wall and floor + dark warm corners
    b += f'<ellipse cx="{lhx}" cy="{lhy + 380}" rx="1100" ry="760" fill="url(#lampglow)"/>'
    b += S.rect_bg("url(#vig)", W, H)
    # foreground timbers framing the view (inside the final framing), a sack in the near left corner
    fg = ""
    for x, lean in ((300, 1), (2105, -1)):
        d = f"M{x - 40 * lean},-40 Q{x + 55 * lean},700 {x - 20 * lean},{H + 40}"
        fg += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="150"/>'
        fg += f'<path d="{d}" fill="none" stroke="{S.shade(wd, -0.4)}" stroke-width="138"/>'
        fg += f'<path d="{d}" fill="none" stroke="{wood}" stroke-width="12" opacity="0.4" transform="translate({30 * lean},0)"/>'
    b += S.g(fg, filter="wobble")
    b += S.g(PR.sack(452, 1210, 1.45, rot=8, seed=21), opacity=1.0, extra='filter="url(#fgdark)"')
    defs += ('<filter id="fgdark" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" '
             'values="0.42 0 0 0 0.02  0 0.36 0 0 0.01  0 0 0.32 0 0  0 0 0 1 0"/></filter>')
    body = f'<g mask="url(#edgefade)">{b}</g>'
    if clip:
        x0, y0, x1, y1, fe = clip
        defs += (f'<filter id="clipblur" filterUnits="userSpaceOnUse" x="-200" y="-200" width="{W + 400}" '
                 f'height="{H + 400}"><feGaussianBlur stdDeviation="{fe}"/></filter>'
                 f'<mask id="clipmask"><rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" '
                 f'rx="{min(60, fe * 2):.0f}" fill="#fff" filter="url(#clipblur)"/></mask>')
        body = f'<g mask="url(#clipmask)">{body}</g>'
    return doc(body, defs)


# ---------------------------------------------------------------- build

def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    l0, l1, l2, l3 = ctx.lines[:4]

    # --------------------------------------------------- timing (all derived from the narration)
    STRIKES = [(l0.start + 1.3, 0.36), (l1.start, 0.45), (l2.start + 0.25, 0.34)]  # (time, flash strength)
    T_TEAR = l1.start + 0.03            # the sail tears at the first flash peak
    T_CRASH = l1.start + 0.12
    rel = [l2.start + 1.1, l2.start + 1.5, l2.start + 2.05, l2.start + 2.4]           # A, B, A, B releases
    T_CUT = (max(l2.end - 0.1, rel[-1] + 0.5), max(l2.end - 0.1, rel[-1] + 0.5) + 0.4)  # the hull opens
    t_sleep = l3.start + L3_SLEEP_FRAC * (l3.end - l3.start)                         # '呼呼大睡'
    T_DIVE0 = max(T_CUT[1] + 0.7, t_sleep - 0.95)   # hold the contrast through '约拿却躺在船舱底下'
    T_DIVE1 = T_DIVE0 + 1.35
    T_REV = (T_DIVE0 + 0.4, T_DIVE0 + 0.95)         # the room blooms out of the hull opening
    T_IN = T_REV[1]
    T_ZZZ = T_REV[0] + 0.3
    T_HATCH = [T_IN + 0.35, T_IN + 1.1]              # lightning still flickering through the hatch
    # dip to black: dark by the 2nd frame of the 0.8 s cross-dissolve into s05 (s05 is then still < 5 % opaque),
    # so s05's own drawing of the hold never shows on top of this one; the fade covers the end of '呼呼大睡'
    T_BLACK = (max(T_DIVE1 + 0.15, T - 1.17), T - 0.77)

    # --------------------------------------------------- the ship's motion
    pitch_amp = keyf([(0, 3.0), (0.6, 3.5), (2.4, 7.5), (l1.start - 0.1, 10.5), (l1.end - 0.1, 10.5),
                      (l2.start + 0.4, 6.0), (T_CUT[0], 5.5), (T_DIVE1, 3.2), (T, 2.8)])
    bob_amp = keyf([(0, 8), (2.4, 20), (l1.start - 0.1, 30), (l1.end - 0.1, 30), (l2.start + 0.4, 18),
                    (T_CUT[0], 15), (T_DIVE1, 8), (T, 7)])
    freq = keyf([(0, 1 / 3.6), (2.0, 1 / 2.8), (l1.start - 0.2, 1 / 2.2), (l1.end, 1 / 2.2), (l2.start + 0.5, 1 / 2.9),
                 (T_CUT[0], 1 / 3.4), (T, 1 / 3.8)])
    phase = integrate(freq, -1.0, T + 1.0)
    sea_amp = keyf([(0, 0.45), (0.5, 0.5), (2.6, 1.0), (l1.end, 1.1), (l2.start + 0.5, 0.9), (T, 0.85)])

    def ship_tf(t):
        ph = 2 * math.pi * phase(t)
        rot = pitch_amp(t) * math.sin(ph)
        if t >= T_CRASH:   # the jolt when the wave hits the bow
            rot -= 3.0 * math.exp(-(t - T_CRASH) / 0.4) * math.sin(8 * (t - T_CRASH))
        dy = bob_amp(t) * math.sin(ph - 1.3)
        dx = 0.35 * bob_amp(t) * math.sin(0.5 * ph + 0.4)
        return Tf(dx, dy, rot, 1, 1, 1, PIV[0], PIV[1])

    def on_ship(local):
        return lambda t: compose(ship_tf(t), local(t))

    def wave_motion(by, sx_, k_ph, k_sw=0.0, lag=0.0, drop=None):
        def m(t):
            a = sea_amp(t)
            ph = 2 * math.pi * phase(t - lag)
            return Tf(dx=sx_ * a * math.sin(0.5 * ph + k_sw),
                      dy=by * a * math.sin(ph + k_ph) + (drop(t) if drop else 0.0))
        return m

    # --------------------------------------------------- sky
    sky_defs = (S.lin_grad("sky", [(0, P["storm_sky_top"]), (0.5, P["storm_sky"]),
                                   (0.8, S.mix(P["storm_sky"], P["sea_pale"], 0.3)), (1, P["storm_sea_light"])])
                + S.lin_grad("seab", [(0, S.mix(P["storm_sea_light"], P["storm_sky"], 0.3)), (0.3, P["storm_sea_light"]),
                                      (1, S.shade(P["storm_sea"], -0.2))]))
    sky = S.rect_bg("url(#sky)", W, H)
    sky += S.g("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="0.5"/>' for x, y, rx, ry, c in (
        (400, 250, 560, 170, P["storm_cloud"]), (1300, 170, 680, 160, P["storm_sky_top"]),
        (2050, 290, 560, 180, P["storm_cloud"]), (900, 480, 560, 100, P["storm_cloud_light"]),
        (1800, 500, 520, 100, P["storm_cloud_light"]))), filter="blur-md")
    sky += S.g("".join(f'<path d="M{x},340 L{x + 170},340 L{x + 60},720 L{x - 110},720 Z" fill="{P["storm_cloud"]}" '
                       f'opacity="0.3"/>' for x in (240, 1060, 1960)), filter="blur-md")
    sea_base = f'<rect x="-20" y="668" width="{W + 40}" height="{H}" fill="url(#seab)"/>'
    # distant waves and low clouds on the horizon (static: far things move slowly)
    f_far = wave_fn(705, 15, 250, 0.4, p=1.6, lean=0.25)
    far_sea = sea_layer(f_far, S.mix(P["storm_sea_light"], P["storm_sky"], 0.22), P["sea_pale"], P["storm_sea"], 250,
                        15, 1, foam_size=0.5, sw=3, x1=W + 80)
    far = ""
    for i, (x, y, w_, h_) in enumerate(((250, 615, 440, 105), (760, 585, 540, 125), (1350, 620, 480, 100),
                                        (1900, 590, 580, 125), (2330, 620, 400, 95))):
        far += storm_cloud(x, y, w_, h_, 20 + i, P["storm_cloud_light"], S.mix(P["storm_cloud"], P["storm_sky"], 0.3),
                           "#a9b4c4", sw=3)
    horizon = sea_base + S.g(far, filter="wobble") + far_sea
    sc.add("sky", doc(sky + horizon, sky_defs), wc=0.7, motion=lambda t: Tf())

    # a lighter sky at the start that the storm swallows during line 0
    light_defs = S.lin_grad("skyl", [(0, "#8b9bb0"), (0.55, "#b2c0ca"), (0.85, "#ccd6d5"), (1, "#b9cdd0")]) + sky_defs
    sky_light = S.rect_bg("url(#skyl)", W, H)
    sky_light += S.g(storm_cloud(560, 330, 560, 150, 4, "#e1e5e6", "#bfc7cf", "#f4f6f2", sw=3)
                     + storm_cloud(1720, 250, 640, 170, 6, "#e1e5e6", "#bfc7cf", "#f4f6f2", sw=3), filter="wobble")
    sc.add("sky_light", doc(sky_light + horizon, light_defs), wc=0.7,
           motion=M.keys([(0, {"alpha": 1}), (0.4, {"alpha": 1}), (l0.end - 0.1, {"alpha": 0})], "sine"))

    # rolling storm clouds: a slow drift during the calm opening, then they roll in while line 0 is spoken
    CL = ((160, 160, 720, 270), (650, 100, 780, 250), (420, 370, 840, 240), (1060, 270, 620, 200))
    CR = ((2240, 150, 780, 280), (1750, 95, 720, 240), (1960, 370, 840, 230), (1390, 230, 580, 190))
    m_left = M.combine(M.keys([(0, {"dx": -820, "dy": -60}), (0.5, {"dx": -790, "dy": -58}),
                               (l0.end + 0.1, {"dx": 0, "dy": 0})], ["sine", "inout"]),
                       M.drift(vx=6), M.bob(6, 5.0))
    m_right = M.combine(M.keys([(0, {"dx": 760, "dy": -50}), (0.5, {"dx": 735, "dy": -48}),
                                (l0.end + 0.4, {"dx": 0, "dy": 0})], ["sine", "inout"]),
                        M.drift(vx=-5), M.bob(7, 4.4, 0.3))

    # lightning bolts (behind the cloud banks): each starts ~50 px inside the underside of a bank cloud as it
    # is placed at that strike time
    bolt_spec = [(m_left, CL[3], -0.3, 700, -1), (m_right, CR[2], 0.05, 770, -1), (m_left, CL[2], 0.25, 760, -1)]
    bolts = []
    for (ts, _), (mm, (cx, cy, cw, ch), fr, y1, sway) in zip(STRIKES, bolt_spec):
        mv = mm(ts)
        bolts.append((cx + fr * cw + mv.dx, cy + 0.5 * ch - 50 + mv.dy, y1, sway))
    for i, ((ts, _), (bx, by0, by1, sway)) in enumerate(zip(STRIKES, bolts)):
        sc.add(f"bolt{i}", doc(bolt_svg(bx, by0, by1, seed=7 + i, sway=sway), BOLT_DEFS), wc=0,
               motion=(lambda ts_: lambda t: Tf(alpha=bolt_alpha(t - ts_)))(ts))

    cl, cr = P["storm_cloud"], S.mix(P["storm_cloud"], P["storm_cloud_light"], 0.3)
    under, rim = S.mix(P["storm_sky_top"], INK, 0.25), "#9aa6ba"
    left = "".join(storm_cloud(x, y, w_, h_, 40 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CL))
    right = "".join(storm_cloud(x, y, w_, h_, 60 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CR))
    sc.add("clouds_left", doc(S.g(left, filter="wobble")), wc=0.9, motion=m_left)
    sc.add("clouds_right", doc(S.g(right, filter="wobble")), wc=0.9, motion=m_right)

    gusts = [(l0.start + 0.15, 1500, 300, 560), (l0.start + 0.55, 700, 470, 480), (l0.start + 1.1, 1950, 470, 440),
             (l0.start + 1.6, 1100, 230, 600), (l1.start + 0.25, 450, 330, 460), (l1.start + 0.85, 1750, 400, 520)]
    for i, (tg, gx_, gy_, gl) in enumerate(gusts):
        sc.add(f"gust{i}", doc(S.g(wind_svg(gx_, gy_, gl, seed=30 + i), filter="wobble-fine")), wc=0,
               motion=(lambda tg_: M.combine(
                   M.keys([(tg_, {"dx": 260, "alpha": 0}), (tg_ + 0.25, {"alpha": 0.95}), (tg_ + 0.95, {"alpha": 0.95}),
                           (tg_ + 1.3, {"dx": -380, "alpha": 0})], "linear"),
                   lambda t: Tf(dy=10 * math.sin(4 * t))))(tg))

    # --------------------------------------------------- sea behind the ship
    f_mid = wave_fn(850, 52, 580, 1.3, p=2.2)
    sc.add("sea_mid", doc(sea_layer(f_mid, S.mix(P["storm_sea_light"], P["storm_sea"], 0.3), P["sea_light"],
                                    P["storm_sea"], 580, 52, 2, foam_size=0.85)),
           wc=1.0, motion=wave_motion(18, 34, -0.4, 0.5, lag=0.25))

    # --------------------------------------------------- the ship (back), crew, cargo, ship (front)
    ox0, oy0, ox1, oy1 = opening_rect()

    def ship_back(sail, cut):
        base = (PR.ship(SX, SY, SS, SF, sail=sail, cutaway=cut, part="back", flag=False)
                + PR.rope_coil(ship_pt(-150, -165)[0], DECK, SS * 0.9))
        out = graded(base)
        if cut:   # the lantern-lit hold stays warm
            out += (f'<clipPath id="holdwarm"><rect x="{ox0 + 9:.1f}" y="{oy0 + 9:.1f}" width="{ox1 - ox0 - 18:.1f}" '
                    f'height="{oy1 - oy0 - 14:.1f}" rx="30"/></clipPath><g clip-path="url(#holdwarm)">{base}</g>')
        return doc(out, GRADE_DEFS)
    cutf = lambda t: M.progress(t, *T_CUT, "sine")                          # noqa: E731
    sc.add("ship_back", [ship_back("full", False), ship_back("torn", False), ship_back("torn", True)],
           motion=ship_tf, frame_at=lambda t: float(t >= T_TEAR) + cutf(t))

    flags = []
    for ph in (0.0, 1.6, 3.2):
        pts = [ship_pt(*q) for q in pennant_pts(ph)]
        flags.append(doc(graded(S.g(S.path(S.smooth_path(pts, closed=True, tension=0.6), fill=P["sail_stripe"],
                                           sw=3.5), filter="wobble-fine")), GRADE_DEFS))
    sc.add("pennant", flags, motion=ship_tf, frame_at=lambda t: float(int(t * 6) % 3))

    # scraps of sail torn off at the flash, flying away downwind (left) in tumbling arcs
    st_tear = ship_tf(T_TEAR)
    for i, (lx, ly, dxe, peak, drop, spin, dur, s) in enumerate((
            (292, -790, -520, 70, 60, -420, 0.75, 1.7), (300, -690, -430, 30, 150, 380, 0.65, 1.35),
            (318, -610, -600, 55, 110, -300, 0.8, 1.5))):
        x0_, y0_ = apply(st_tear, *ship_pt(lx, ly))

        def scrap_m(t, x0_=x0_, y0_=y0_, dxe=dxe, peak=peak, drop=drop, spin=spin, dur=dur, i=i):
            if t < T_TEAR or t > T_TEAR + dur:
                return Tf(alpha=0.0, px=x0_, py=y0_)
            u = (t - T_TEAR) / dur
            xo = dxe * (1 - (1 - u) ** 2)
            yo = -4 * peak * u * (1 - u) + drop * u * u
            return Tf(xo, yo, spin * u, 0.55 + 0.45 * abs(math.cos(9 * u + i)), 1.0,
                      1 - M.progress(u, 0.6, 1.0, "sine"), x0_, y0_)
        sc.add(f"scrap{i}", doc(graded(S.g(scrap_svg(x0_, y0_, 90 + i, s), filter="wobble-fine")), GRADE_DEFS),
               wc=0.5, motion=scrap_m)

    # sleeping Jonah inside the cutaway hold (small; the hold painting takes over during the dive)
    jx_c, jy_c = ship_pt(*PR.SHIP_SLEEP)
    sc.add("jonah_cut", doc(C.jonah(jx_c, jy_c, SS, -1, pose="sleep", marks=False)),
           motion=on_ship(lambda t: Tf(alpha=cutf(t) * (1 - M.progress(t, T_REV[0] + 0.02, T_REV[0] + 0.18, "sine")),
                                       px=jx_c, py=jy_c)))

    # sailors: A (bow side, throws to the left), B (stern side, throws right), C (beside the mast, prays)
    AX, BX, CX = 1020.0, 1462.0, 1330.0
    s0 = STRIKES[0][0]
    T_PRAY = STRIKES[2][0] + 0.1
    GRAB, LIFT, FT = 0.48, 0.22, 0.16   # carry pose this long before release, throw pose this long before,
    #                                     the throw pose held this long after (then a bent-forward follow-through)

    def trembler(amp, t0, t1, seed):
        def m(t):
            k = amp * M.progress(t, t0, t0 + 0.2) * (1 - M.progress(t, t1 - 0.2, t1))
            return k * math.sin(t * 47 + seed), 0.4 * k * math.sin(t * 31 + seed)
        return m

    def pose_track(times):
        """Flipbook index for poses listed in the order used: a hard cut at each switch time."""
        return lambda t: float(sum(t >= ts for ts in times))

    def heave_keys(throws):
        """Forward lean (deg, + = toward the sea) and vertical squash for a sailor's throws."""
        lk, lc, sk, scv = [(0.0, 0.0)], [], [(0.0, 1.0)], []
        for tr in throws:
            lk += [(tr - LIFT, 0.0), (tr - 0.07, -8.0), (tr + 0.05, 12.0), (tr + 0.42, 0.0)]
            lc += ["linear", "sine", "out", "back"]
            tg = tr - GRAB
            sk += [(tg - 0.001, 1.0), (tg, 0.95), (tg + 0.24, 1.0)]
            scv += ["linear", "linear", "out"]
        return keyc(lk, lc), keyc(sk, scv)

    def actor(x, facing, lean, squash, trem):
        """Sailor body motion on deck (pivot at the feet): tremble, keyed lean and squash."""
        def m(t):
            ddx, ddy = trem(t)
            sy = squash(t)
            return Tf(ddx, ddy, facing * lean(t), 1 + 0.5 * (1 - sy), sy, 1.0, x, DECK)
        return m

    def sailor_frames(x, facing, variant, poses):
        return [doc(graded(C.sailor(x, DECK, SS, facing, variant=variant, pose=p, expr=e)), GRADE_DEFS)
                for p, e in poses]

    def carry_over(sx, facing, variant):
        hc = C.hand_positions(C.sailor, sx, DECK, SS, facing, variant=variant, pose="carry")
        ht = C.hand_positions(C.sailor, sx, DECK, SS, facing, variant=variant, pose="throw")
        return (((hc[0][0] + hc[1][0]) / 2, (hc[0][1] + hc[1][1]) / 2 - 6),
                ((ht[0][0] + ht[1][0]) / 2, (ht[0][1] + ht[1][1]) / 2))

    A_carry, A_over = carry_over(AX, -1, 0)
    B_carry, B_over = carry_over(BX, 1, 1)
    tA1, tB1, tA2, tB2 = rel

    # C: worried -> scared at the first strike -> prays at the third, slowly tilting his raised arms up and out
    # over the rail (clear of the mast and of B)
    c_lean = keyc([(0, 0.0), (T_PRAY, 0.0), (T_PRAY + 1.4, 6.0)], ["linear", "sine"])

    def c_motion(t):
        ddx, ddy = trembler(2.2, s0, T_PRAY + 0.1, 3)(t)
        k = M.progress(t, T_PRAY, T_PRAY + 0.5, "sine")
        ddx += 1.4 * k * math.sin(t * 8.5)
        rot = -1 * c_lean(t) + k * 1.2 * math.sin(2 * math.pi * (t - T_PRAY) / 2.4)
        return Tf(ddx, ddy, rot, 1, 1, 1, CX, DECK)

    z_crew = len(sc.layers) + len(sc.dynamics)    # A's cargo rests behind A's legs: drawn just below the crew
    sc.add("sailor_C", sailor_frames(CX, -1, 3, [("stand", "worried"), ("scared", None), ("pray", None)]),
           motion=on_ship(c_motion), frame_at=pose_track([s0 + 0.08, T_PRAY]))
    leanA, sqA = heave_keys([tA1, tA2])
    actA = actor(AX, -1, leanA, sqA, trembler(2.0, s0, tA1 - GRAB, 1))
    sc.add("sailor_A", sailor_frames(AX, -1, 0, [("point", "surprised"), ("scared", None), ("carry", None),
                                                 ("throw", None), ("carry", None), ("throw", None), ("carry", None),
                                                 ("scared", None)]),
           motion=on_ship(actA),
           frame_at=pose_track([s0 + 0.05, tA1 - GRAB, tA1 - LIFT, tA1 + FT, tA2 - LIFT, tA2 + FT, tA2 + 0.62]))
    leanB, sqB = heave_keys([tB1, tB2])
    actB = actor(BX, 1, leanB, sqB, trembler(2.0, s0 + 0.1, tB1 - GRAB, 2))
    sc.add("sailor_B", sailor_frames(BX, 1, 1, [("stand", "worried"), ("scared", None), ("carry", None),
                                                ("throw", None), ("carry", None), ("throw", None), ("carry", None),
                                                ("scared", None)]),
           motion=on_ship(actB),
           frame_at=pose_track([s0 + 0.12, tB1 - GRAB, tB1 - LIFT, tB1 + FT, tB2 - LIFT, tB2 + FT, tB2 + 0.62]))

    # the sea surface in front of the ship (for splash timing): near-wave function + its motion
    gx = lambda x: min(1.0, abs(x - SX) / 950) ** 1.4                        # noqa: E731
    f_near = wave_fn(lambda x: 1004 - 75 * gx(x), lambda x: 16 + 100 * gx(x), 600, 0.75, p=2.0, lean=0.3)
    near_drop = lambda t: 115 * M.progress(t, T_CUT[0] - 0.1, T_CUT[1] + 0.15, "inout")   # noqa: E731
    near_m = wave_motion(22, 46, 0.3, 2.0, lag=0.1, drop=near_drop)

    def surface(x, t):
        m = near_m(t)
        return f_near(x - m.dx) + m.dy

    # cargo: rests on deck -> grabbed (carry) -> overhead (throw) -> released in a spinning arc -> splash.
    # While held it follows the thrower's lean / squash, so it stays in his hands.
    splashes = []

    def cargo(name, svg, rest, carry, over, t_rel, land, spin, half_h, act, fly=0.72, peak=170, z=None):
        t_grab, t_up = t_rel - GRAB, t_rel - LIFT
        top = (over[0], over[1] - half_h + 12)

        def local_pos(t):
            if t < t_grab:
                return rest
            if t < t_up:
                u = M.progress(t, t_grab, t_grab + 0.12, "out")
                return (rest[0] + (carry[0] - rest[0]) * u, rest[1] + (carry[1] - rest[1]) * u)
            return top                       # snaps overhead with the cut to the throw pose

        def held(t):
            p = local_pos(t)
            inner = Tf(p[0] - rest[0], p[1] - rest[1], 0, 1, 1, 1, rest[0], rest[1])
            if t >= t_grab:
                inner = compose(act(t), inner)
            return compose(ship_tf(t), inner)

        rel_tf = held(t_rel)
        sx_, sy_ = apply(rel_tf, *rest)
        rot0 = rel_tf.rot

        def make_path(lx):
            return lambda u: (sx_ + (lx - sx_) * u, sy_ + (land[1] - sy_) * u - 4 * peak * u * (1 - u))

        def hit(pth):
            for i in range(60, 200):
                tt = t_rel + fly * i / 160
                x, y = pth(i / 160)
                if y >= surface(x, tt):
                    return tt, y
            return t_rel + fly, 9e9

        # among landing spots near the requested one, prefer the one whose splash is highest on screen
        best = None
        for lx in np.arange(land[0] - 110, land[0] + 111, 20):
            tt, y = hit(make_path(lx))
            score = y + 0.5 * abs(lx - land[0])
            if best is None or score < best[0]:
                best = (score, lx, tt)
        _, lx_best, t_hit = best
        path = make_path(lx_best)
        hx_, _ = path((t_hit - t_rel) / fly)

        def m(t):
            if t < t_rel:
                return held(t)
            u = (t - t_rel) / fly
            if t > t_hit + 0.35:
                return Tf(alpha=0.0, px=rest[0], py=rest[1])
            x, y = path(u)
            return Tf(x - rest[0], y - rest[1], rot0 + spin * u, 1, 1, 1, rest[0], rest[1])
        sc.add(name, doc(graded(svg), GRADE_DEFS), motion=m, z=z)
        splashes.append((t_hit, hx_, surface(hx_, t_hit) + 10, name))

    # A's crate stands behind his legs, his jar on the deck behind him (toward the stern), clear of his
    # pointing hand; both are drawn just below the crew so his hands overlap them while he holds them
    a_cr = (AX + 45, deck_y_at(AX + 45) - 37)
    a_jar = (AX + 118, deck_y_at(AX + 118) - 51)
    b_jar = (B_carry[0], deck_y_at(B_carry[0]) - 53)
    b_sack = (B_carry[0] + 52, deck_y_at(B_carry[0] + 52) + 2)
    cargo("cargo_A2", PR.crate(*a_cr, 0.78), a_cr, A_carry, A_over, tA2, (560, 1130), -320, 40, actA,
          z=z_crew - 0.6)
    cargo("cargo_A1", PR.jar(*a_jar, 0.62), a_jar, A_carry, A_over, tA1, (660, 1120), -400, 52, actA,
          z=z_crew - 0.5)
    cargo("cargo_B1", PR.jar(*b_jar, 0.66, color=S.mix(P["terracotta"], P["sand"], 0.35)), b_jar, B_carry, B_over,
          tB1, (1860, 1120), 380, 55, actB)
    cargo("cargo_B2", PR.sack(*b_sack, 0.62, seed=6), b_sack, (B_carry[0], B_carry[1] + 32),
          (B_over[0], B_over[1] + 40), tB2, (1960, 1130), 300, 40, actB)

    # front of the ship (cool storm light), its stern lantern stays warm
    lan = PR.lantern(*ship_pt(-428, -372), 0.85 * SS)
    sc.add("ship_front", doc(graded(PR.ship(SX, SY, SS, SF, sail="torn", part="front", lantern=False)) + lan,
                             GRADE_DEFS), motion=ship_tf)

    # --------------------------------------------------- sea in front of the ship
    sc.add("sea_near", doc(sea_layer(f_near, P["storm_sea"], P["storm_sea_light"], S.shade(P["storm_sea"], -0.3),
                                     600, 70, 3, foam_size=1.0, cap_amp=lambda x: 16 + 100 * gx(x))),
           wc=1.0, motion=near_m)

    for i, (ts, x, y, _) in enumerate(splashes):
        sc.add(f"splash{i}", doc(burst(x, y, 0.75, seed=i, lean=(-12 if x < SX else 12))), wc=0.5,
               motion=(lambda ts_, x_, y_: M.keys([(ts_ - 0.01, {"sy": 0.1, "sx": 0.5, "alpha": 0}),
                                                   (ts_, {"alpha": 1}),
                                                   (ts_ + 0.2, {"sy": 1.0, "sx": 1.0}),
                                                   (ts_ + 0.45, {"sy": 0.92, "sx": 1.08, "alpha": 0.95}),
                                                   (ts_ + 0.85, {"sy": 0.3, "sx": 1.2, "alpha": 0})],
                                                  ["linear", "out", "sine", "in"], pivot=(x_, y_ + 10)))(ts, x, y))

    # a big wave bursting over the bow as the ship nearly breaks; its plume fans away from the deck (and from
    # sailor A's face)
    bx, by = ship_pt(455, -60)
    sc.add("bow_crash", doc(burst(bx - 40, by + 40, 1.7, seed=12, n=6, spread=48, height=150, lean=-32)), wc=0.5,
           motion=M.keys([(T_CRASH - 0.01, {"sy": 0.15, "sx": 0.6, "alpha": 0}), (T_CRASH, {"alpha": 1}),
                          (T_CRASH + 0.28, {"sy": 1.0, "sx": 1.0}),
                          (T_CRASH + 0.75, {"sy": 0.95, "sx": 1.1, "alpha": 0.95}),
                          (T_CRASH + 1.3, {"sy": 0.3, "sx": 1.2, "alpha": 0})],
                         ["linear", "out", "sine", "in"], pivot=(bx - 40, by + 50)))

    f_fg = wave_fn(1262, 36, 540, 0.7, p=1.8, lean=0.3)
    sc.add("sea_fg", doc(sea_layer(f_fg, S.shade(P["storm_sea"], -0.18), P["storm_sea_light"],
                                   S.shade(P["storm_sea"], -0.45), 540, 36, 4, foam_size=0.8)),
           wc=1.0, motion=wave_motion(12, 30, 1.6, 3.0, lag=-0.15, drop=lambda t: 1.4 * near_drop(t)))

    # --------------------------------------------------- the dive: the outside darkens around the hull opening
    dim_d = (f"M-20,-20 H{W + 20} V{H + 20} H-20 Z "
             f"M{ox0 + 10:.1f},{oy0 + 10:.1f} H{ox1 - 10:.1f} V{oy1 - 12:.1f} H{ox0 + 10:.1f} Z")
    dim_a = lambda t: (0.74 * M.progress(t, T_DIVE0 + 0.1, T_REV[0] + 0.08, "sine")      # noqa: E731
                       + 0.24 * M.progress(t, T_REV[0] + 0.08, T_REV[0] + 0.24, "sine"))
    sc.add("dim", doc(f'<path d="{dim_d}" fill="#24150d" fill-rule="evenodd" filter="url(#blur-md)"/>'), wc=0,
           motion=lambda t: replace(ship_tf(t), alpha=dim_a(t)))

    # --------------------------------------------------- the hold painting, attached to the ship at scale K
    H0 = (jx_c - K * (J_PAINT[0] - Q0[0]), jy_c - K * (J_PAINT[1] - Q0[1]))
    place = Tf(H0[0] - Q0[0], H0[1] - Q0[1], 0, K, K, 1, Q0[0], Q0[1])

    def to_paint(x, y):
        return Q0[0] + (x - H0[0]) / K, Q0[1] + (y - H0[1]) / K

    def in_hold(local=None):
        def m(t):
            base = compose(ship_tf(t), place)
            return compose(base, local(t)) if local else base
        return m

    jx, jy = J_PAINT
    rc = (jx + 130, jy - 120)

    # the reveal grows outward from the hull opening: the opening itself, then two wider soft rectangles, then all
    px0, py0 = to_paint(ox0, oy0)
    px1, py1 = to_paint(ox1, oy1)
    full_a = lambda t: M.progress(t, T_REV[0] + 0.28, T_REV[1] - 0.03, "sine")        # noqa: E731
    # (inset x, inset y, feather), fade-in window after T_REV[0]; each stage is dropped once the next one fully
    # covers it
    stages = [((14, 14, 10), 0.0, 0.15), ((-190, -150, 50), 0.08, 0.25), ((-520, -400, 120), 0.17, 0.36)]
    t_off = [T_REV[0] + 0.26, T_REV[0] + 0.37, T_REV[1]]
    for i, ((ix, iy, fe), a0, a1) in enumerate(stages):
        sc.add(f"hold_r{i}", hold_svg(clip=(px0 + ix, py0 + iy, px1 - ix, py1 - iy, fe)), wc=1.0, seed=101,
               motion=in_hold(lambda t, a0=a0, a1=a1, off=t_off[i]: Tf(
                   alpha=M.progress(t, T_REV[0] + a0, T_REV[0] + a1, "sine") * (t < off),
                   px=Q0[0], py=Q0[1])))
    sc.add("hold", hold_svg(), wc=1.0, seed=101, motion=in_hold(lambda t: Tf(alpha=full_a(t), px=Q0[0], py=Q0[1])))

    # snore cue -> Jonah's breathing (chest highest at the end of each inhale of the actual sound)
    snore_at = round(T_CUT[0] + 0.25, 3)
    snore_dur = round(T + 0.6 - snore_at, 3)
    peaks = []
    for k in range(8):   # choose a variation whose inhale falls inside the hold, before the scene's dissolve
        at_k = round(snore_at + 0.07 * k, 3)
        pk = snore_inhale_peaks(ctx.id, at_k, round(T + 0.6 - at_k, 3))
        if not pk or any(T_IN + 0.15 <= p <= T - 1.25 for p in pk):
            snore_at, snore_dur, peaks = at_k, round(T + 0.6 - at_k, 3), pk
            break
    else:
        peaks = snore_inhale_peaks(ctx.id, snore_at, snore_dur)
    breath = breath_curve(peaks)

    fade_in = lambda t: M.progress(t, T_REV[0] + 0.02, T_REV[0] + 0.18, "sine")       # noqa: E731
    sc.add("jonah", doc(C.jonah(jx, jy, JS, -1, pose="sleep", marks=False)),
           motion=in_hold(lambda t: Tf(0, 0, 0, 1 + 0.006 * breath(t), 1 + 0.024 * breath(t), fade_in(t), jx, jy)))

    lhx, lhy = LANTERN_HOOK
    swing = lambda t: 8 * math.sin(2 * math.pi * t / 3.1 + 0.6) - 0.6 * ship_tf(t).rot     # noqa: E731
    glow = f'<ellipse cx="{lhx + 60}" cy="{lhy + 400}" rx="600" ry="520" fill="url(#lg2)"/>'
    sc.add("lamp_glow", doc(glow, S.rad_grad("lg2", [(0, "#ffd890", 0.5), (0.35, "#ffc870", 0.22), (1, "#ffc060", 0)])),
           wc=0, blend="add",
           motion=in_hold(lambda t: Tf(0, 0, swing(t), 1, 1,
                                       full_a(t) * (0.85 + 0.1 * math.sin(t * 7.3) + 0.05 * math.sin(t * 12.1)),
                                       lhx, lhy)))
    sc.add("lantern", doc(f'<line x1="{lhx}" y1="{lhy - 10}" x2="{lhx}" y2="{lhy + 44}" stroke="{INK}" stroke-width="5"/>'
                          + PR.lantern(lhx, lhy + 34, 1.5)),
           motion=in_hold(lambda t: Tf(0, 0, swing(t), 1, 1, full_a(t), lhx, lhy)))

    # Z z z drifting up from the sleeper's head
    head = (jx + 240, jy - 140)
    for i, delay in enumerate((0.0, 0.75, 1.5)):
        zsvg = doc(S.text(head[0] + 50, head[1] - 50, "Z", size=84, fill="#fff3d6",
                          extra=f'stroke="{INK}" stroke-width="8" paint-order="stroke"'))

        def zm(t, delay=delay):
            per = 2.25
            if t < T_ZZZ + delay:
                return Tf(alpha=0.0, px=head[0], py=head[1])
            u = ((t - T_ZZZ - delay) % per) / per
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine")) * full_a(t)
            s = 0.45 + 0.75 * u
            return Tf(70 + 190 * u + 26 * math.sin(u * 6.0), -30 - 330 * u, -12 + 22 * u, s, s, a,
                      head[0] + 50, head[1] - 70)
        sc.add(f"z{i}", zsvg, wc=0, motion=in_hold(zm))

    # drips from the hatch, rain boiling in the hatch and cold flickers through it (the storm still rages above)
    hx0 = HATCH[0]
    drop = (f'<path d="M{hx0 + 150},312 Q{hx0 + 162},336 {hx0 + 150},344 Q{hx0 + 138},336 {hx0 + 150},312 Z" '
            f'fill="{P["sea_pale"]}" stroke="{INK}" stroke-width="3"/>')
    for i in range(2):
        def dm(t, i=i):
            per = 1.3
            if t < T_REV[0]:
                return Tf(alpha=0.0, px=hx0 + 150, py=320)
            u = ((t + i * 0.65) % per) / per
            return Tf(0, 790 * u * u, 0, 1, 1, min(1.0, u / 0.1) * (1 - M.progress(u, 0.85, 1.0)) * full_a(t),
                      hx0 + 150, 320)
        sc.add(f"drip{i}", doc(drop), wc=0, motion=in_hold(dm))
    sc.add("hatch_rain", [hatch_rain_svg(s) for s in (1, 2, 3)], wc=0,
           motion=in_hold(lambda t: Tf(alpha=full_a(t), px=Q0[0], py=Q0[1])), frame_at=lambda t: float(int(t * 11) % 3))
    flash = (f'<path d="M{HATCH[0] + 20},296 L{HATCH[1] - 20},296 L{HATCH[1] + 200},1110 L{HATCH[0] + 20},1110 Z" '
             f'fill="#9fb6e0" opacity="0.45" filter="url(#blur-lg)"/>'
             f'<ellipse cx="{(HATCH[0] + HATCH[1]) / 2}" cy="{(HATCH_Y[0] + HATCH_Y[1]) / 2}" rx="260" ry="150" '
             f'fill="#c8d6f0" opacity="0.8" filter="url(#blur-md)"/>')
    sc.add("hatch_flash", doc(flash), wc=0, blend="add",
           motion=in_hold(lambda t: Tf(alpha=max(0.65 * flick(t - T_HATCH[0]), 0.42 * flick(t - T_HATCH[1])),
                                       px=Q0[0], py=Q0[1])))

    # warm lamplight bloom that carries the eye from the storm into the hold during the reveal
    bloom = f'<circle cx="{rc[0]}" cy="{rc[1]}" r="1150" fill="url(#bl)"/>'
    sc.add("bloom", doc(bloom, S.rad_grad("bl", [(0, "#ffd890", 0.17), (0.45, "#f6b860", 0.1), (1, "#f0a050", 0)])),
           wc=0, blend="add",
           motion=in_hold(lambda t: Tf(alpha=M.progress(t, T_REV[0] - 0.1, T_REV[0] + 0.4, "sine")
                                       * (1 - M.progress(t, T_REV[0] + 0.45, T_REV[1] + 0.35, "sine")),
                                       px=Q0[0], py=Q0[1])))

    # --------------------------------------------------- camera
    CAM_CONTRAST = Cam(1225, 795, 1350)   # crew panicking on deck above, Jonah asleep in the open hold below
    cam_ext = M.cam_keys([(0, Cam(1200, 690, 2200)), (l0.end, Cam(1205, 680, 2120)),
                          (l2.start - 0.1, Cam(1210, 675, 2060)), (l2.start + 0.9, Cam(1225, 650, 1660)),
                          (T_CUT[0], Cam(1230, 660, 1630)), (T_DIVE0 + 0.4, CAM_CONTRAST)],
                         ["inout", "inout", "inout", "inout", "sine"])
    cam_ext = M.cam_shake(cam_ext, amp=15, t0=l1.start - 0.02, t1=l1.end + 0.1, freq=7.5, seed=3)
    cam_ext = M.cam_shake(cam_ext, amp=5, t0=s0, t1=s0 + 0.7, freq=9, seed=5)
    cam_ext = M.cam_shake(cam_ext, amp=6, t0=STRIKES[2][0], t1=STRIKES[2][0] + 0.7, freq=9, seed=8)

    def camera(t):
        u = M.progress(t, T_DIVE0, T_DIVE1, "inout")
        if u <= 0:
            return cam_ext(t)
        st = ship_tf(t)
        hx, hy = apply(compose(st, place), *V0)
        ce = cam_ext(t)
        w_end = VIEW_W_INT * K * (1 - 0.04 * M.progress(t, T_DIVE1, T, "sine"))
        w = math.exp(math.log(ce.w) + (math.log(w_end) - math.log(ce.w)) * u)   # even-feeling zoom
        return Cam(ce.x + (hx - ce.x) * u, ce.y + (hy - ce.y) * u, w, ce.rot + (0.7 * st.rot - ce.rot) * u)
    sc.camera = camera

    # cull the outside world (render time): everything but the dim once the dim (>= 0.98) and the opened stages of
    # the hold hide it, the dim itself once the hold painting fills the whole frame
    def view_in_painting(t, margin=72):
        cam = camera(t)
        tf = compose(ship_tf(t), place)
        hw, hh = cam.w / 2, cam.w * 9 / 32
        cr, sr_ = math.cos(math.radians(cam.rot)), math.sin(math.radians(cam.rot))
        r = math.radians(tf.rot)
        for ax, ay in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
            x, y = cam.x + cr * ax - sr_ * ay, cam.y + sr_ * ax + cr * ay
            ox_, oy_ = apply(tf, tf.px, tf.py)          # where the painting pivot lands
            dx_, dy_ = x - ox_, y - oy_
            qx = tf.px + (math.cos(r) * dx_ + math.sin(r) * dy_) / K
            qy = tf.py + (-math.sin(r) * dx_ + math.cos(r) * dy_) / K
            if not (margin <= qx <= W - margin and margin <= qy <= H - margin):
                return False
        return True

    t_cull = T + 1
    for t in np.arange(T_IN, T + 0.001, 1 / 30):
        if all(view_in_painting(tt) for tt in np.arange(t, T + 0.001, 1 / 30)):
            t_cull = float(t)
            break
    inside = {"bloom", "hold_r0", "hold_r1", "hold_r2", "hold", "jonah", "lamp_glow", "lantern", "hatch_flash",
              "hatch_rain", "z0", "z1", "z2", "drip0", "drip1"}
    t_hidden = T_REV[0] + 0.26
    for lay in sc.layers:
        if lay.name in inside or lay.motion is None:
            continue

        def culled(t, m0=lay.motion, tc=(t_cull if lay.name == "dim" else min(t_cull, t_hidden))):
            return Tf(alpha=0.0) if t > tc else m0(t)
        lay.motion = culled

    # --------------------------------------------------- effects
    def hold_region(t):
        st = compose(ship_tf(t), place)
        x0, y0 = apply(st, 750, 330)
        x1, y1 = apply(st, 1650, 1000)
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    def rain_hole(t, view):
        if t < T_CUT[0] + 0.2:
            return None
        st = ship_tf(t)
        return [view.to_out(*apply(st, x, y)) for x, y in ((ox0, oy0), (ox1, oy0), (ox1, oy1), (ox0, oy1))]

    sc.fx = [rain_fx(0.45, T_REV[0] + 0.35, density=0.85, angle=-16, hole=rain_hole), flash_fx(STRIKES),
             motes_fx(hold_region, 24, T_IN - 0.3), dip_fx(*T_BLACK)]
    sc.meta = dict(STRIKES=STRIKES, rel=rel, splashes=[s[:3] for s in splashes], T_CUT=T_CUT, T_DIVE0=T_DIVE0,
                   T_BLACK=T_BLACK,
                   T_DIVE1=T_DIVE1, T_REV=T_REV, T_IN=T_IN, T_HATCH=T_HATCH, T_CRASH=T_CRASH, T_TEAR=T_TEAR,
                   t_cull=t_cull, snore=(snore_at, snore_dur, peaks), H0=H0, ship_tf=ship_tf, place=place,
                   camera=camera, bolts=bolts)

    # --------------------------------------------------- sound
    out_end = T_IN + 0.4
    t_in_amb = T_REV[0] - 0.3
    for name, g_out, g_in, t0 in (("storm_wind", -9, -17, 0.0), ("waves_storm", -9, -15, 0.0), ("rain", -10, -17, 0.3)):
        sc.sfx(name, t0, dur=out_end - t0, gain_db=g_out, fade_in=0.8, fade_out=1.2)
        sc.sfx(name, t_in_amb, dur=T + 0.6 - t_in_amb, gain_db=g_in, fade_in=1.0, fade_out=0.8)
    sc.sfx("drip", T_REV[0], dur=T + 0.6 - T_REV[0], gain_db=-16, fade_in=0.6, fade_out=0.8)
    sc.sfx("ship_creak", 0, dur=T + 0.6, gain_db=-11, fade_in=0.8, fade_out=0.8)
    sc.sfx("ship_creak", l1.start - 0.1, dur=l1.end - l1.start + 0.8, gain_db=-6, fade_in=0.1, fade_out=0.5)
    for (ts, _), (bx_, *_r) in zip(STRIKES, bolts):
        sc.sfx("thunder", ts, gain_db=-6, pan=max(-0.6, min(0.6, (bx_ - 1200) / 1300)))
    sc.sfx("thunder", T_HATCH[0], gain_db=-14, pan=0.3)
    sc.sfx("thunder", T_HATCH[1], gain_db=-17, pan=0.3)
    sc.sfx("cloth", T_TEAR, gain_db=-12, pan=-0.3)
    sc.sfx("splash", T_CRASH + 0.05, gain_db=-8, pan=-0.4)
    for ts, x, _, _ in splashes:
        sc.sfx("splash_small", ts, gain_db=-7, pan=max(-0.8, min(0.8, (x - 1200) / 1100)))
    for tr, pan in zip(rel, (-0.3, 0.3, -0.3, 0.3)):
        sc.sfx("whoosh", tr, gain_db=-15, pan=pan)
    sc.sfx("snore", snore_at, dur=snore_dur, gain_db=-8, fade_in=0.5, fade_out=0.6)
    return sc
