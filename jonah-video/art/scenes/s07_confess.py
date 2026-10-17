"""Scene 7 (v2) — the sea grows wilder; Jonah tells the sailors to throw him in (Jonah 1:11-12).

Medium shot on the rainy deck of the v1 lots scene (art/scenes_v1/s05_lots.py: same bulwark with painted shields,
mast, torn striped sail, hatch, storm sky and sea); the crew stand on the left (the captain, sailors 1, 0, 3 and 2),
Jonah on the right in front of the open hatch, facing them, still holding the softly glowing marked lot from s06.
The scene opens on s06's closing framing (camera, sky, curling breaker, Jonah's pose and lot, the last of the warm
light on him), so the dissolve only changes the crew; the camera then pulls back as the sea rises.

Line 0 (N) '海浪越来越大，' the storm grows: big dark swells rise up beyond the rail one after another, the curling
        breaker on the right towers higher, the sky darkens under a heavy cloud bank, the rain thickens and the
        horizon rocks harder (the ship stays level, the world tilts). '越来越凶。' lightning strikes, a breaker
        bursts over the rail and showers the deck, the camera jolts: the sailors flinch (hard pose cuts sold by a
        squash-and-hop), the captain grabs his cap. '水手们问约拿：' they turn to Jonah; the ginger-bearded sailor
        steps toward him; Jonah lifts his head.
Line 1 (S) '我们该拿你怎么办，' the ginger sailor holds out both hands to Jonah, pleading; '海才会平静下来呢？' he
        spreads his arms helplessly; Jonah lowers his eyes.
Line 2 (J) '你们把我抬起来，' Jonah, sorry but brave, lays his hand on his chest; '扔进海里吧，' he turns like a paper
        cut-out and points over the rail to the raging sea — a breaker bursts right where he points; the sailors
        gasp. '海就会平静下来。' he turns back to them with a calm, open hand.
Line 3 (J) '我知道，' hand on chest again, looking at them; '这场大风浪，' he looks up at the storm (a far flash);
        '都是因为我。' he bows his head. The sailors exchange a sad look; the camera slowly pushes in. The scene ends
        on a calm, held frame.

Every key time comes from the narration chunks (sub-phrases inside a chunk are placed by their characters and
snapped to a nearby pause in the voice take, see Cues). Pose changes are hard cuts (never crossfaded), every pose
is held >= 0.5 s. Stage 2112 x 2120 (the v1 lots stage; the camera stays on the deck world, y < 1190).
"""
import math
import random
from dataclasses import replace

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s04_storm as V4
from art.scenes_v1 import s05_lots as V5
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD, OUT_H, OUT_W
from engine.scene import Scene

SH = V5.SH                                   # 2120: the v1 lots stage (deck world y 0..1190)
RAIL_TOP, DECK_BACK, DECK_CUT = V5.RAIL_TOP, V5.DECK_BACK, V5.DECK_CUT
SWAY_PIVOT = V5.SWAY_PIVOT
MX = V5.MAST_X + 29                          # mast centre

# cast: (x, ground y, scale)
CAPT = (560, 1012, 1.04)
S1 = (722, 918, 0.86)        # variant 1 (red stripes, blue cap), back row left of the mast
S0 = (1000, 962, 0.94)       # variant 0 (blue stripes, red headband), middle row
S3 = (1170, 1020, 1.08)      # variant 3 (ginger beard), front row: the one who asks
S3_STEP = 52                 # ...he steps this far toward Jonah
S2 = (1385, 914, 0.86)       # variant 2 (teal stripes), back row
JON = (1600, 1004, 1.04)     # Jonah, in front of the hatch

PUNCT = "，。！？：；、,.!?:;"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=SH)


# ============================================================== narration timing

def _nchar(s):
    return max(1, sum(1 for ch in s if ch not in PUNCT and not ch.isspace()))


def _dips(path):
    """Low-energy stretches (>= 40 ms) inside a voice take: [(start, end)] s from the take's start."""
    try:
        import soundfile as sf
        x, sr = sf.read(str(path), dtype="float32")
    except Exception:
        return []
    if x.ndim == 2:
        x = x.mean(axis=1)
    hop = sr // 100
    nb = len(x) // hop
    if nb < 10:
        return []
    e = np.sqrt((x[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1))
    e = np.convolve(e, np.ones(3) / 3, mode="same")
    low = e < 0.06 * e.max()
    out, i = [], 0
    while i < nb:
        if low[i]:
            j = i
            while j < nb and low[j]:
                j += 1
            if j - i >= 4 and i > 0 and j < nb:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


class Cues:
    """Times of phrases in the narration. A phrase at the start of a subtitle chunk starts with the chunk; one
    inside a chunk is placed by its characters and snapped to the end of a nearby pause in the voice take."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.dips = []
        for i, ln in enumerate(ctx.lines):
            for a, b in _dips(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"):
                self.dips.append((ln.start + a, ln.start + b))

    def at(self, phrases, default):
        for ph in ([phrases] if isinstance(phrases, str) else phrases):
            for ln in self.ctx.lines:
                spans = [(c.text, c.start, c.end) for c in ln.chunks] or [(ln.text, ln.start, ln.end)]
                for text, c0, c1 in spans:
                    k = text.find(ph)
                    if k < 0:
                        continue
                    if _nchar(text[:k]) <= 1 and not any(ch not in PUNCT for ch in text[:k]):
                        return c0
                    est = c0 + (c1 - c0) * _nchar(text[:k]) / _nchar(text)
                    best, score = None, -1.0          # prefer a long pause (a comma) near the estimate
                    for a, b in self.dips:
                        if c0 < a and b < c1 and abs(b - est) < 0.45:
                            sc_ = (b - a) - 0.15 * abs(b - est)
                            if sc_ > score:
                                best, score = b, sc_
                    return best if best is not None else est
        return default

    def end(self, phrases, default):
        """End of the voice inside the chunk holding the phrase (= start of the pause after it)."""
        for ph in ([phrases] if isinstance(phrases, str) else phrases):
            for ln in self.ctx.lines:
                for c in ln.chunks:
                    if ph in c.text:
                        return c.end
        return default


# ============================================================== painting

def tilt_amp_fn(grow):
    return lambda t: 1.45 + 1.25 * grow(t)


def make_tilted(grow):
    """Outboard world tilt about SWAY_PIVOT (the horizon rocks against the level ship); grows with the storm."""
    amp = tilt_amp_fn(grow)

    def sea_rot(t):
        return amp(t) * math.sin(2 * math.pi * t / 5.0 + 0.6)

    def tilted(m=None):
        px, py = SWAY_PIVOT

        def f(t):
            th = sea_rot(t)
            v = m(t) if m else Tf()
            bx = v.px if v.px is not None else px
            by = v.py if v.py is not None else py
            a = math.radians(th)
            qx = px + (bx + v.dx - px) * math.cos(a) - (by + v.dy - py) * math.sin(a)
            qy = py + (bx + v.dx - px) * math.sin(a) + (by + v.dy - py) * math.cos(a)
            return Tf(qx - bx, qy - by, v.rot + th, v.sx, v.sy, v.alpha, bx, by)
        return f
    return tilted, sea_rot


def sky_markup(dark):
    """V5's storm sky (dark=False) or the same sky under a heavy storm cover (dark=True: a slate wash and a bank
    of dark storm clouds over the warm cloud break), with V5's far sea on the horizon. The far sea is part of
    this static painting (only the nearer swells rock) to keep the frame cost down."""
    sfx = "d" if dark else "l"
    defs = (S.lin_grad(f"dsky{sfx}", [(0, "#36415a"), (0.42, "#4f5d77"), (0.77, "#7f8da2"), (1, "#9eaab8")]) +
            S.rad_grad(f"dbreak{sfx}", [(0, "#f6e2b4", 0.75), (0.5, "#e7cf9c", 0.3), (1, "#d9cdb4", 0)]) +
            S.lin_grad(f"curtain{sfx}", [(0, "#c9d3dc", 0.0), (0.3, "#c9d3dc", 0.22), (1, "#c9d3dc", 0.0)]))
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="800" fill="url(#dsky{sfx})"/>'
    body += f'<ellipse cx="1650" cy="300" rx="430" ry="170" fill="url(#dbreak{sfx})"/>'
    soft = ""
    for (cx, cy, rx, ry, col) in [(250, 170, 520, 150, "#323c52"), (900, 110, 640, 150, "#36415a"),
                                  (2000, 150, 420, 140, "#323c52"), (620, 300, 360, 80, "#465370")]:
        soft += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}"/>'
    body += S.g(soft, filter="blur-md")
    for (x0, x1) in [(180, 420), (860, 1080)]:
        body += S.g(f'<path d="M{x0},300 L{x1},300 L{x1 - 90},600 L{x0 - 90},600 Z" fill="url(#curtain{sfx})"/>',
                    filter="soft")
    bank = ""
    for i, (cx, cy, w, h, col) in enumerate([(120, 250, 560, 150, "#59667f"), (760, 210, 600, 140, "#55627b"),
                                              (1240, 200, 420, 120, "#5c6982"), (2080, 205, 520, 150, "#55627b")]):
        bank += S.cloud(cx, cy, w, h, col, seed=10 + i, sw=2.5)
    body += S.g(bank, filter="wobble")
    if dark:
        defs += S.lin_grad("s7gl", [(0, "#1d2536", 0.8), (0.55, "#27324a", 0.5), (1, "#3a4760", 0.12)])
        body += f'<rect x="-30" y="-30" width="{W + 60}" height="{RAIL_TOP + 40}" fill="url(#s7gl)"/>'
        heavy = ""
        for i, (cx, cy, w, h) in enumerate([(1560, 150, 760, 250), (2090, 210, 560, 220), (1020, 70, 660, 200),
                                             (420, 120, 720, 230), (-60, 200, 420, 200)]):
            heavy += V4.storm_cloud(cx, cy, w, h, seed=70 + i, fill="#3c4860", under="#262f42", rim="#8390a6", sw=4)
        body += S.g(heavy, filter="wobble")
    # far sea on the horizon (V5.sea_far_layer)
    wl, ph = 190, 0.3
    sea = S.path(V5.peaky_band(592, 16, wl, ph, bottom=800, seed=3, var=0.55), fill="#5a7b8c", sw=3)
    r = random.Random(41)
    for k, x in V5.crest_xs(wl, ph):
        if r.random() < 0.38:
            continue
        m = V5.crest_mul(k, 3, 0.55)
        sea += V5.foam_cap(x + r.uniform(-6, 6), 592 - 16 * m - 3, 34 * r.uniform(0.55, 1.25) * (0.6 + 0.4 * m),
                           seed=k, opacity=round(r.uniform(0.45, 0.75), 2), curl=r.random() < 0.5)
    sea += S.path(V5.peaky_band(608, 10, 150, 0.6, bottom=800, seed=8, var=0.5), fill="#507285", stroke=False)
    if dark:
        sea += f'<rect x="-30" y="560" width="{W + 60}" height="260" fill="#22304a" opacity="0.22"/>'
    return body + S.g(sea, filter="wobble"), defs


def sky_layer(dark):
    body, defs = sky_markup(dark)
    return doc(body, defs)


def surge_layer():
    """Tall dark swells that rise up behind the rail as the storm grows (v1 s04 sea painting)."""
    f = V4.wave_fn(660, 84, 620, 0.9, p=2.3, lean=0.4)
    defs = S.lin_grad("s7sg", [(0, "#4f7f92"), (0.35, "#355e72"), (1, "#22404f")])
    d, _ = V4.band_path(f, -200, W + 200, step=14, bottom=950)
    body = S.path(d, fill="url(#s7sg)", sw=4.5)
    r = random.Random(4)
    for xc, yc in V4.crests(f, -200, W + 200):
        y = yc + 84 * 1.4 + r.uniform(8, 26)
        xa, xb = xc - 620 * r.uniform(0.2, 0.3), xc + 620 * r.uniform(0.15, 0.28)
        body += (f'<path d="M{xa:.0f},{y:.0f} Q{(xa + xb) / 2:.0f},{y - 28:.0f} {xb:.0f},{y + 8:.0f}" fill="none" '
                 f'stroke="#1c3542" stroke-width="7" opacity="0.4" stroke-linecap="round"/>')
        body += (f'<path d="M{xc - 150:.0f},{yc + 60:.0f} q60,34 140,40" fill="none" stroke="{P["foam"]}" '
                 f'stroke-width="6" stroke-linecap="round" opacity="0.5"/>')
    caps = ""
    for i, (xc, yc) in enumerate(V4.crests(f, -170, W + 170)):
        caps += V4.foam_cap(f, xc, 620, 84, 300 + i, 1.15)
    return doc(S.g(body, filter="wobble") + S.g(caps, filter="wobble-fine"), defs)


SAIL_K, SAIL_YARD = 0.84, 300


def rig_layer():
    """V5's rig without the sail: shrouds, mast with rope bands, mast foot and lantern hook (a static column)."""
    b = ""
    for xr in (MX - 330, MX + 330):
        b += f'<path d="M{MX},-200 L{xr},{RAIL_TOP + 6}" stroke="{P["ink_soft"]}" stroke-width="5" fill="none"/>'
    b += f'<rect x="{V5.MAST_X}" y="-40" width="58" height="{972 + 40}" fill="url(#s7mast)" {S.STROKE}/>'
    for yy in (640, 690):
        b += f'<rect x="{V5.MAST_X - 6}" y="{yy}" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<path d="M{MX - 57},972 Q{MX},940 {MX + 57},972 Z" fill="{P["wood_dark"]}" {S.STROKE}/>'
    b += f'<path d="M{MX + 29},610 L{MX + 76},610" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linecap="round"/>'
    defs = S.lin_grad("s7mast", [(0, P["wood_dark"]), (0.4, P["wood_light"]), (1, P["wood"])], x1=0, y1=0, x2=1, y2=0)
    return doc(S.g(b, filter="wobble"), defs)


def sail_layer():
    """The torn striped sail of s04-s06 (props.ship 'torn', mirrored as in V5) on its yard, with its two sheets."""
    k, y_yard = SAIL_K, SAIL_YARD
    base_y = y_yard + 848 * k
    sail = PR._sail("torn", "s07sail")
    b = (f'<g transform="rotate(5 {MX} {y_yard})"><g transform="translate({MX},{base_y}) scale({-k},{k}) '
         f'translate(10,0)">{sail}</g></g>')
    for lx, dx in ((-300, 210), (280, -230)):
        sx = MX - k * (lx + 10)
        b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} L{sx + dx:.0f},{RAIL_TOP + 4}" stroke="{P["ink_soft"]}" '
              f'stroke-width="4" fill="none"/>')
    return doc(S.g(b, filter="wobble"))


def deck_layer():
    """V5.deck_layer without the rig: bulwark with shields, deck planks, puddles, the open hatch, and the deck
    props (a crate and a tied jar at the far left, a rope coil by the mast; a big rope coil and a bucket in front)."""
    defs = (S.lin_grad("deckf", [(0, "#b98450"), (0.5, P["wood_light"]), (1, "#a96f42")]) +
            S.lin_grad("bulw", [(0, P["wood"]), (1, "#7e4e2e")]))
    b = ""
    b += f'<rect x="-30" y="{RAIL_TOP + 14}" width="{W + 60}" height="{DECK_BACK - RAIL_TOP - 4}" fill="url(#bulw)" {S.STROKE}/>'
    b += V5.plank_lines(-30, W + 30, [842, 868], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += f'<rect x="{x - 12}" y="{RAIL_TOP + 4}" width="24" height="{DECK_BACK - RAIL_TOP}" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    for xr in (MX - 330, MX + 330):
        b += f'<circle cx="{xr}" cy="{RAIL_TOP + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += V5.shield(x, 852, 33, cols[i % 4])
    b += (f'<path d="M-30,{RAIL_TOP} L{W + 30},{RAIL_TOP} L{W + 30},{RAIL_TOP + 18} L-30,{RAIL_TOP + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    b += f'<rect x="-30" y="{DECK_BACK}" width="{W + 60}" height="{DECK_CUT - DECK_BACK + 4}" fill="url(#deckf)" {S.STROKE}/>'
    ys = [906, 924, 946, 972, 1003, 1039, 1080, 1126, 1176]
    b += V5.plank_lines(-30, W + 30, ys, seed=7, opacity=0.45, joint_every=(260, 620))
    for (x, y, rx, ry) in [(660, 1062, 130, 16), (1180, 1112, 160, 18), (1600, 1150, 120, 14), (420, 1150, 90, 12),
                           (1330, 985, 90, 10)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9fb3bd" opacity="0.45"/>'
        b += f'<path d="M{x - rx * 0.5},{y - 3} l{rx * 0.5},0" stroke="#e8eef0" stroke-width="3" opacity="0.6"/>'
    hm, hdefs = V5.hatch_markup()
    b += hm
    props = (C.ground_shadow(470, 979, 1.0, width=150, opacity=0.18) + PR.crate(470, 925, 1.05) +
             PR.jar(392, 948, 0.62, rot=-6) + PR.rope_coil(912, 968, 0.7) +
             PR.rope_coil(300, 1128, 1.5) + V5.bucket(2010, 1150, 1.1))
    return doc(S.g(b, filter="wobble") + props, defs + hdefs)


# ============================================================== figures

def _fig(design, metrics, ps, expr, x, y, s, facing, label):
    inner, _ = C._figure(design, metrics, dict(ps), expr, C._fsign(facing))
    return C._wrap_out(inner, x, y, s, facing, label)


ASK = C._P(t=6, h=-2, legs=((6, 2), (-5, -2)), arms=(("fk", 48, 92), ("fk", 36, 84)), hands=("open", "open"),
           expr="worried")
SHRUG = C._P(t=-2, h=-8, legs=((6, 2), (-5, -2)), arms=(("fk", 42, 118), ("fk", -38, -112)), hands=("open", "open"),
             expr="worried")
J_CALM = C._P(t=2, h=4, arms=(("fk", 10, 5), ("fk", 46, 84)), hands=("fist", "open"), expr="neutral")
J_CHEST = C._P(t=2, h=-2, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
               expr="neutral")
J_CHEST_UP = C._P(t=0, h=-14, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
                  look=(0.02, -0.08), expr="worried")


def sailor_mk(v, x, y, s, facing, pose, expr):
    if isinstance(pose, dict):
        return _fig(C._sailor_design(v), C._SAILOR_M, pose, expr or pose["expr"], x, y, s, facing, f"s7s{v}")
    return C.sailor(x, y, s, facing, variant=v, pose=pose, expr=expr)


def jonah_mk(x, y, s, facing, pose, expr):
    if isinstance(pose, dict):
        return _fig(C._jonah_design(), C._ADULT, pose, expr or pose["expr"], x, y, s, facing, "s7j")
    return C.jonah(x, y, s, facing, pose=pose, expr=expr)


def flip(sc, name, keyframes, z, motion=None):
    """Flipbook from [(t, markup), ...] with hard switches at the given times (never crossfaded)."""
    times = [k[0] for k in keyframes]
    svgs = [doc(k[1]) for k in keyframes]

    def at(t):
        i = 0
        for j, tj in enumerate(times):
            if t >= tj:
                i = j
        return float(i)
    if len(svgs) == 1:
        sc.add(name, svgs[0], motion=motion, z=z)
    else:
        sc.add(name, svgs, motion=motion, z=z, frame_at=at)
    return times


def bump(t, ts, w=0.07):
    return max(0.0, 1 - abs(t - ts - 0.03) / w)


# ============================================================== effects

def rain_fx(level, seed=8):
    """Slanted rain (thicker as the storm grows: level(t) 0..1 of the drops shown) + splash rings on the deck."""
    n = 520
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = 1700 * rng.uniform(0.75, 1.25, n)
    ln = 46 * rng.uniform(0.6, 1.3, n)
    al = rng.uniform(70, 135, n).astype(int)
    rank = rng.uniform(0, 1, n)
    a = math.radians(15)
    dx, dy = math.sin(a), math.cos(a)
    m = 46
    spx = rng.uniform(80, W - 80, m)
    spy = rng.uniform(DECK_BACK + 20, DECK_CUT - 30, m)
    sph = rng.uniform(0, 1, m)

    def fx(frame, t, view):
        lv = level(t)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0 + sp * t) % (OUT_H + 80) - 40
        x = (x0 - sp * t * dx / dy) % (OUT_W + 400) - 200
        for i in range(n):
            if rank[i] > lv:
                continue
            d.line([(x[i], y[i]), (x[i] + ln[i] * dx, y[i] + ln[i] * dy)], fill=(226, 234, 242, int(al[i])), width=2)
        for i in range(m):
            if rank[i] > 0.4 + 0.6 * lv:
                continue
            ph = (t * 2.2 + sph[i]) % 1.0
            if ph > 0.3:
                continue
            ox, oy = view.to_out(spx[i], spy[i])
            r = (3 + 14 * ph / 0.3) * view.scale
            aa = int(150 * (1 - ph / 0.3))
            d.arc([ox - r, oy - r * 0.45, ox + r, oy + r * 0.45], 190, 350, fill=(232, 240, 245, aa), width=2)
        frame.alpha_composite(ov)
        return frame
    return fx


def spray_fx(bursts, seed=21):
    """Water thrown over the rail by a breaker: small drops fly up from the rail, fall onto the deck and leave a
    ring where they land. bursts: [(t0, x_center, half_width, count)] in stage px."""
    rng = np.random.default_rng(seed)
    parts = []
    for t0, xc, hw, n in bursts:
        for _ in range(n):
            parts.append((t0 + rng.uniform(0, 0.2), xc + rng.uniform(-hw, hw), RAIL_TOP + rng.uniform(-24, 6),
                          rng.uniform(-240, 240), rng.uniform(-820, -380), rng.uniform(930, 1160),
                          rng.uniform(3.2, 6.5)))
    arr = np.array(parts, np.float64)
    g = 2300.0

    def fx(frame, t, view):
        live = arr[(arr[:, 0] <= t) & (arr[:, 0] > t - 1.6)]
        if not len(live):
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ts, x, y, vx, vy, land, r in live:
            age = t - ts
            disc = vy * vy + 2 * g * (land - y)
            t_land = (-vy + math.sqrt(max(0.0, disc))) / g
            if age < t_land:
                k = min(1.0, age / 0.05)
                xx, yy = x + vx * age, y + vy * age + 0.5 * g * age * age
                # a short streak along the velocity (motion blur) with a round head
                vyy = vy + g * age
                ox, oy = view.to_out(xx, yy)
                tx, ty = view.to_out(xx - vx * 0.022, yy - vyy * 0.022)
                rr = r * view.scale
                d.line([(tx, ty), (ox, oy)], fill=(214, 230, 236, int(130 * k)), width=max(2, int(rr * 1.3)))
                d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=(234, 242, 240, int(215 * k)),
                          outline=(96, 112, 120, int(120 * k)), width=1)
            else:
                u = (age - t_land) / 0.32
                if u > 1:
                    continue
                ox, oy = view.to_out(x + vx * t_land, land)
                rr = (r * 1.6 + 16 * u) * view.scale
                d.arc([ox - rr, oy - rr * 0.35, ox + rr, oy + rr * 0.35], 190, 350,
                      fill=(232, 240, 245, int(170 * (1 - u))), width=2)
        frame.alpha_composite(ov)
        return frame
    return fx


# ============================================================== build

def build(ctx):
    T = ctx.duration
    L = ctx.lines
    cue = Cues(ctx)
    sc = Scene(ctx, W=W, H=SH)

    def line_frac(i, f):
        i = min(i, len(L) - 1)
        return L[i].start + f * (L[i].end - L[i].start)

    # ---------------------------------------------------------------- key times (all from the narration)
    p0 = cue.at("海浪越来越大", L[0].start)                      # the swells start to rise
    p0b = cue.at("越来越凶", line_frac(0, 0.35))                 # lightning + the breaker over the rail
    p0c = cue.at("水手们问约拿", line_frac(0, 0.6))               # they turn to Jonah
    p1 = cue.at(["我们该拿你怎么办", "我们该"], line_frac(1, 0.0))   # pleading hands
    p1b = cue.at(["海才会平静", "才能让海平静"], line_frac(1, 0.45))           # helpless shrug
    p1e = cue.end(["海才会平静", "才能让海平静"], L[min(1, len(L) - 1)].end)
    p2 = cue.at(["你们把我抬起来", "把我抬起来"], line_frac(2, 0.0))            # hand on chest
    p2b = cue.at(["扔进海里", "抛进海里"], line_frac(2, 0.32))                 # turn + point at the sea
    p2c = cue.at("海就会平静下来", line_frac(2, 0.6))                         # back to them, calm hand
    p3 = cue.at(["我知道"], line_frac(3, 0.0))                                # hand on chest again
    p3b = cue.at(["这场大风浪", "大风浪"], line_frac(3, 0.2))                  # looks up at the storm
    p3c = cue.at(["都是因为我", "因为我"], line_frac(3, 0.55))                  # bows his head
    # keep the order sane if a voice take changes a lot
    p3 = max(p3, p2c + 1.2)
    p3b = max(p3b, p3 + 0.55)
    p3c = max(p3c, p3b + 0.6)
    t_crash = p0b + 0.02
    t_strike = p0b - 0.03
    t_far_strike = p3b + 0.08
    t_point_splash = p2b + 0.4

    # storm growth 0..1: calm-ish at the start, rising through '海浪越来越大', full at '越来越凶'
    grow = V4.keyc([(p0, 0.0), (p0b, 0.62), (p0b + 0.9, 1.0)], ["inout", "out"])
    tilted, sea_rot = make_tilted(grow)

    # ---------------------------------------------------------------- outboard world
    # the dark storm sky is the static painting; the lighter sky of s06 lies over it and fades away as the storm
    # grows (it costs nothing once it is gone)
    sc.add("sky", sky_layer(True), z=0, wc=0.7)
    sc.add("sky_light", sky_layer(False), z=0.2, wc=0.7, motion=lambda t: Tf(alpha=1 - grow(t)))
    # lightning: one bold bolt at '越来越凶', a smaller far one at '这场大风浪'
    sc.add("bolt0", doc(V4.bolt_svg(1170, 130, 600, seed=17, sway=1, w0=34), V4.BOLT_DEFS), z=0.4, wc=0,
           motion=lambda t: Tf(alpha=V4.bolt_alpha(t - t_strike)))
    sc.add("bolt1", doc(V4.bolt_svg(1460, 210, 590, seed=23, sway=-1, w0=22), V4.BOLT_DEFS), z=0.45, wc=0,
           motion=lambda t: Tf(alpha=0.85 * V4.bolt_alpha(t - t_far_strike)))
    sc.add("clouds", V5.clouds_layer(), z=1, motion=lambda t: Tf(dx=14 * t + 22 * max(0.0, t - p0)), wc=0.8)

    # the swells rise up from behind the rail one after another and keep heaving
    def surge_m(t):
        g = grow(t)
        up = 300 * (1 - g)
        heave = (14 + 30 * g) * math.sin(2 * math.pi * t / 3.6 + 0.4)
        return Tf(dx=60 * math.sin(2 * math.pi * t / 7.2) - 40 * g, dy=up + heave)
    sc.add("surge", surge_layer(), z=2, motion=tilted(surge_m), wc=0.9)

    lift_pt = lambda t: 50 * math.sin(math.pi * M.progress(t, p2b - 0.1, p2b + 1.6, "linear"))   # noqa: E731

    def bigwave_m(t):
        g = grow(t)
        return Tf(dx=18 * math.sin(2 * math.pi * t / 6.8) - 30 * g,
                  dy=-70 * g + (16 + 16 * g) * math.sin(2 * math.pi * (t / 3.4 + 0.1)) - lift_pt(t),
                  sx=1 + 0.12 * g, sy=1 + 0.12 * g, px=1760, py=880)
    sc.add("big_wave", V5.big_wave_layer(), z=3, motion=tilted(bigwave_m))
    sc.add("sea_mid", V5.sea_mid_layer(), z=4, motion=tilted(
        lambda t: Tf(dx=(46 + 20 * grow(t)) * math.sin(2 * math.pi * t / 6.0),
                     dy=(18 + 18 * grow(t)) * math.sin(2 * math.pi * (t / 3.4 + 0.35)))))

    # spray bursts over the rail (behind the bulwark): ambient ones away from the faces, the crash at '越来越凶'
    # and the one right where Jonah points ('扔进海里')
    splashes = [(p0 + 0.75, 300, 0.8, 3, "small"), (t_crash, 1500, 1.4, 7, "big"), (t_crash + 0.12, 520, 1.0, 5, None),
                (p1b + 0.75, 260, 0.75, 9, "small"), (t_point_splash, 1930, 1.35, 11, "big"),
                (p2c + 1.05, 1080, 0.8, 15, "small"), (min(p3b + 0.3, T - 2.6), 700, 0.85, 13, "small")]

    def splash_m(base, t0, dur=1.0):
        def m(t):
            u = (t - t0) / dur
            if not (0 <= u < 1):
                return Tf(alpha=0.0)
            s = 0.25 + 0.85 * M.ease("out")(min(1.0, u / 0.6))
            a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.5, 1.0, "sine"))
            return Tf(dy=50 * u * u, sx=s, sy=s, alpha=a, px=base[0], py=base[1])
        return tilted(m)
    for i, (ts, sx_, k, seed, snd) in enumerate(splashes):
        base = (sx_, RAIL_TOP + 14)
        sc.add(f"splash{i}", V5.splash_layer(base[0], base[1], seed, k), z=5 + 0.1 * i, motion=splash_m(base, ts),
               wc=0.3)
        pan = max(-0.8, min(0.8, (sx_ - 1056) / 1200))
        if snd == "big":
            sc.sfx("splash", ts, gain_db=-9, pan=pan)
        elif snd == "small":
            sc.sfx("splash_small", ts, gain_db=-15, pan=pan)

    # ---------------------------------------------------------------- ship
    sc.add("deck", deck_layer(), z=10)
    # (the hatch glow sits between the deck strip and the rig column so the two static paintings stay separate
    # items: their union would cover the whole frame)
    hg_defs = S.rad_grad("hg", [(0, "#ffcf86", 0.7), (0.5, "#f6a956", 0.25), (1, "#f2a95a", 0)])
    sc.add("hatch_glow", doc(f'<ellipse cx="{V5.HX}" cy="{V5.HATCH_F[2] - 30}" rx="190" ry="120" fill="url(#hg)"/>',
                             hg_defs), z=10.2, blend="add", wc=0, motion=M.pulse(0.7, 1.0, 1.7))
    sc.add("rig", rig_layer(), z=10.5)

    def sail_m(t):                   # the torn sail billows and shivers in the gusts (stronger as the storm grows)
        g = grow(t)
        gust = math.sin(2 * math.pi * t / 1.3) + 0.5 * math.sin(2 * math.pi * t / 0.57 + 1.0)
        return Tf(rot=(0.35 + 0.35 * g) * gust, sy=1 + (0.008 + 0.01 * g) * math.sin(2 * math.pi * t / 1.9),
                  px=MX, py=SAIL_YARD)
    sc.add("sail", sail_layer(), z=10.6, motion=sail_m)
    mlx, mly = MX + 47, 610
    sc.add("deck_lantern", doc(PR.lantern(mlx, mly, 0.8)), z=20,
           motion=lambda t: Tf(rot=(9 + 6 * grow(t)) * math.sin(2 * math.pi * t / 2.7), px=mlx, py=mly))

    # ---------------------------------------------------------------- crew
    def sailor_frames(v, x, y, s, keys_):
        return [(t, C.ground_shadow(x, y + 2, s) + sailor_mk(v, x, y, s, f, p, e)) for t, p, f, e in keys_]

    def jolt(t):                     # everyone dips at the crash
        return -6 * bump(t, t_crash, 0.1)

    # S1 (back left)
    x, y, s = S1
    k1 = [(0, "stand", 1, "worried"), (p0b + 0.2, "scared", 1, None), (p0c + 0.32, "stand", 1, "worried"),
          (p2b + 0.3, "scared", 1, None), (p2c + 0.5, "stand", 1, "worried"), (p3c + 0.3, "stand", 1, "sad")]
    flip(sc, "s1", sailor_frames(1, x, y, s, k1), z=21,
         motion=V5.alive(x, y, [k[0] for k in k1[1:]], 0.8, extra=lambda t: Tf(dy=jolt(t))))

    # S2 (back right, between the ginger sailor and Jonah)
    x, y, s = S2
    k2 = [(0, "stand", 1, "worried"), (p0b + 0.1, "scared", 1, None), (p0c + 0.2, "stand", 1, "worried"),
          (p2b + 0.16, "stand", 1, "surprised"), (p2c + 0.3, "stand", 1, "worried"), (p3c + 0.2, "stand", 1, "sad")]
    flip(sc, "s2", sailor_frames(2, x, y, s, k2), z=21.5,
         motion=V5.alive(x, y, [k[0] for k in k2[1:]], 0.55, extra=lambda t: Tf(dy=jolt(t))))

    # S0 (middle)
    x, y, s = S0
    k0 = [(0, "stand", 1, "worried"), (p0b + 0.14, "scared", 1, None), (p0c + 0.06, "stand", 1, "worried"),
          (p2b + 0.2, "scared", 1, "surprised"), (p2c + 0.45, "stand", 1, "worried"), (p3b + 0.2, "stand", 1, "sad")]
    flip(sc, "s0", sailor_frames(0, x, y, s, k0), z=22,
         motion=V5.alive(x, y, [k[0] for k in k0[1:]], 0.2, extra=lambda t: Tf(dy=jolt(t))))

    # captain (front left)
    x, y, s = CAPT
    kc = [(0, "stand", "worried"), (p0b + 0.12, "worried", None), (p0c + 0.42, "stand", "worried"),
          (p2b + 0.24, "worried", None), (p2c + 0.5, "stand", "worried"), (p3c, "stand", "sad")]
    flip(sc, "captain", [(t, C.ground_shadow(x, y + 2, s) + C.captain(x, y, s, 1, pose=p, expr=e)) for t, p, e in kc],
         z=23, motion=V5.alive(x, y, [k[0] for k in kc[1:]], 0.65, extra=lambda t: Tf(dy=jolt(t))))

    # S3 (front, the one who asks): steps toward Jonah, pleads, shrugs; later exchanges a look with S0
    x, y, s = S3
    t_step0 = p0c + 0.12
    t_step1 = t_step0 + 0.36
    t_look0, t_look1 = p3b + 0.12, p3c + 0.3
    k3 = [(0, "stand", 1, "worried"), (p0b + 0.08, "scared", 1, None), (t_step0, "stand", 1, "worried"),
          (p1 - 0.05, ASK, 1, "worried"), (p1b - 0.04, SHRUG, 1, "worried"), (p1e + 0.3, "stand", 1, "worried"),
          (p2b + 0.12, "stand", 1, "surprised"), (p2c + 0.35, "stand", 1, "worried"),
          (t_look0, "stand", -1, "sad"), (t_look1, "stand", 1, "sad")]

    def step(t):
        return S3_STEP * M.progress(t, t_step0, t_step1, "sine")

    def s3_extra(t):
        u = M.progress(t, t_step0, t_step1, "linear")
        lean = 2.0 * math.sin(math.pi * M.progress(t, p1b - 0.04, p1e + 0.3, "linear"))
        return Tf(dx=step(t), dy=-12 * math.sin(math.pi * u) + jolt(t), rot=-lean * 0.5)
    flip(sc, "s3", sailor_frames(3, x, y, s, k3), z=24,
         motion=V5.turned(V5.alive(x, y, [k[0] for k in k3[1:]], 0.4, extra=s3_extra), [t_look0, t_look1], w=0.09,
                          px=lambda t: x + step(t)))

    # ---------------------------------------------------------------- Jonah
    # He still holds the marked lot from s06 (glowing softly): pressed to his chest in the chest poses, hanging
    # from a hand otherwise.
    jx, jy, js = JON
    t_jup = p0c + 0.38
    kj = [(0, "confess", -1, "sorry", "chest"), (t_jup, "stand", -1, "worried", "near"),
          (p1b + 0.35, "stand", -1, "sad", "near"),                     # lowers his eyes at '海才会平静…'
          (p2 - 0.05, J_CHEST, -1, "neutral", "chest"), (p2b, "point", 1, "neutral", "near"),
          (p2c, J_CALM, -1, "neutral", "far"), (p3 - 0.05, J_CHEST, -1, "neutral", "chest"),
          (p3b - 0.02, J_CHEST_UP, -1, "worried", "chest"), (p3c - 0.04, "confess", -1, "sorry", "chest")]

    def lot_at(pose, facing, expr, where):
        bp = C.body_points(lambda x_, y_, s_, f_: jonah_mk(x_, y_, s_, f_, pose, expr), jx, jy, js, facing)
        far, near = bp["hands"]
        if where == "chest":
            return (near[0] - 4 * facing, near[1] + 4), 1.1 * js, -24 * facing
        h = near if where == "near" else far
        return (h[0] + 2 * facing, h[1] + 26 * js), 1.0 * js, 84 * facing

    jframes, glow_pts = [], []
    for t, p, f, e, where in kj:
        (lx, ly), ls, lr = lot_at(p, f, e, where)
        mk = C.ground_shadow(jx, jy + 2, js) + jonah_mk(jx, jy, js, f, p, e) + PR.lot(lx, ly, ls, rot=lr, marked=True)
        jframes.append((t, mk))
        glow_pts.append((lx, ly))
    jmotion = V5.turned(V5.alive(jx, jy, [k[0] for k in kj[1:]], 0.1, amp=0.010,
                                 extra=lambda t: Tf(dy=-0.6 * jolt(t))), [p2b, p2c], w=0.1)
    flip(sc, "jonah", jframes, z=25, motion=jmotion)

    # the lot's warm glow (additive, follows the lot through his pose changes and turns)
    lg_defs = S.rad_grad("s7lg", [(0, "#ffd890", 0.9), (0.4, "#ffbf60", 0.35), (1, "#ffbf60", 0)])
    glow_frames = [doc(f'<ellipse cx="{x_:.1f}" cy="{y_:.1f}" rx="70" ry="58" fill="url(#s7lg)"/>', lg_defs)
                   for x_, y_ in glow_pts]
    lot_env = V4.keyc([(0, 0.45), (p2b, 0.4), (T, 0.32)], "sine")
    kt = [k[0] for k in kj]
    sc.add("lot_glow", glow_frames, z=25.2, wc=0, blend="add",
           frame_at=lambda t: float(max(i for i, tk in enumerate(kt) if t >= tk)),
           motion=lambda t: replace(jmotion(t), alpha=lot_env(t) * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.1))))
    # the last of s06's warm light on Jonah fades as the dark storm closes in
    jg_defs = S.rad_grad("s7jg", [(0, "#ffe2a0", 0.55), (0.45, "#ffd27a", 0.25), (1, "#ffd27a", 0)])
    sc.add("jonah_light", doc(f'<ellipse cx="{jx}" cy="{jy - 190}" rx="250" ry="320" fill="url(#s7jg)"/>', jg_defs),
           z=24.9, wc=0, blend="add", motion=lambda t: Tf(alpha=0.22 * (1 - grow(t))))

    # ---------------------------------------------------------------- camera
    A = Cam(1372, 664, 1450)       # s06's closing framing (same deck, rail, wave and hatch: a clean dissolve)
    B = Cam(1110, 656, 1690)       # pulled back and up: the waves tower behind the rail
    Cc = Cam(1170, 694, 1540)      # the question
    D = Cam(1215, 690, 1520)       # Jonah answers
    E = Cam(1262, 680, 1580)       # ...includes where he points (the captain stays in frame)
    F = Cam(1300, 700, 1480)
    G = Cam(1450, 716, 1300)       # slow push-in on Jonah and the three nearest sailors at the end
    keys = [(0.0, A), (p0, Cam(A.x - 4, A.y, A.w + 8)), (p0b + 0.9, B), (p0c + 0.5, B), (p1 + 0.6, Cc),
            (p2 - 0.3, D), (p2b + 0.15, D), (p2b + 1.2, E), (p2c + 0.8, E), (p3 + 0.2, F), (T, G)]
    base = M.cam_keys(keys, "sine")
    shake1 = M.shake(9, t_crash - 0.02, t_crash + 0.7, freq=8, seed=4)
    shake2 = M.shake(4, t_point_splash, t_point_splash + 0.45, freq=8, seed=9)

    def cam(t):
        c = base(t)
        a, b = shake1(t), shake2(t)
        roll = (0.25 + 0.15 * grow(t)) * math.sin(2 * math.pi * t / 5.0 + 2.2)
        return Cam(c.x + a.dx + b.dx, c.y + a.dy + b.dy, c.w, roll + a.rot + b.rot)
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    sc.fx = [
        rain_fx(lambda t: 0.62 + 0.38 * grow(t)),
        spray_fx([(t_crash + 0.08, 1500, 240, 26), (t_crash + 0.2, 560, 150, 12),
                  (t_point_splash + 0.08, 1900, 180, 18)]),
        FX.lightning([t_strike], dur=0.5, strength=0.5),
        FX.lightning([t_far_strike], dur=0.45, strength=0.24),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_storm", 0, dur=T + 0.8, gain_db=-13, fade_in=0.8, fade_out=1.0)
    sc.sfx("storm_wind", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("rain", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("ship_creak", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("whoosh", p0 + 0.35, gain_db=-14, pan=0.2)
    sc.sfx("thunder", t_strike, gain_db=-8, pan=-0.5)
    sc.sfx("cloth", t_step0, gain_db=-15, pan=0.05)
    sc.sfx("cloth", p2b - 0.04, gain_db=-14, pan=0.5)
    sc.sfx("cloth", p2c - 0.04, gain_db=-15, pan=0.5)
    sc.sfx("thunder", t_far_strike, dur=2.6, gain_db=-16, pan=0.3, fade_out=1.2)
    return sc
