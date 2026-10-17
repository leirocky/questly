"""Scene 5 — the captain wakes Jonah (Jonah 1:6).

Line 0 (N)  船长找到了约拿，把他摇醒，说：
Line 1 (C)  快醒醒！风浪这么大，你怎么还在睡觉？
Line 2 (C)  快起来，求你的神救救我们吧！也许你的神会可怜我们，让我们活下来。

The scene opens on exactly the picture s04 ends on: v1 s04's lantern-lit hold painting (V4.hold_svg, same watercolour
seed), Jonah asleep on the grain sacks breathing in time with the snore, 'Z z z', the swinging lantern, rain through
the grated hatch, and s04's final camera (V4.V0, 0.96 x V4.VIEW_W_INT painting px wide). The hold keeps rocking
gently with the ship and the storm stays audible.

As the narrator names the captain the hatch grating is flung open (cold storm light and rain pour in), his sandals
appear in the opening and he scrambles down the ladder two rungs at a time (two alternating climb drawings, the
body dropping a rung pair per drawing), hops off with a landing squash at its foot and
hurries to Jonah with a planted-foot walk (the drawing follows the distance walked, the planted sole never slides).
He steps up onto the end of the bed through a reaching in-between, kneels behind Jonah's head (C.captain 'wake'
recipe, drawn behind Jonah so Jonah's face stays clear) and shakes him by the shoulder ('把他摇醒', little shake marks).
Jonah sits up rubbing his eye while the captain hops down to his standing spot (same frame, so the heads never
overlap).
Line 1: the captain urges him ('快醒醒！'), clutches his cap as thunder cracks through the hatch and the ship lurches
('风浪这么大' — Jonah turns round with a start), then spreads his palms ('你怎么还在睡觉？').
Line 2: he points up through the hatch to the deck ('快起来' — Jonah jumps to his feet), looks up ('求你的神'), raises
both hands to heaven ('救救我们吧' — a second flash), then clasps his hands and pleads (a nod on '可怜', a lean-in on
'让我们活下来'); Jonah lowers his eyes, sorry (he knows the storm is his doing), then looks up toward the hatch and the
storm above — the calm final frame. The camera eases out once the captain is down, then pushes slowly in on the two.
Every pose change is a hard cut sold by a small squash-and-hop (no crossfades between poses); every main pose is
held for at least half a second; all key times come from the narration (sub-phrases are timed from the punctuation
pauses in the voice files, with a proportional fallback).

Stage = the hold painting's own canvas, 2400 x 1350.
"""
import json
import math
import random
import zlib

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s04_storm as V4
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD, CACHE
from engine.scene import Scene

W, H = V4.W, V4.H                    # 2400 x 1350 (the s04 hold painting's canvas)
INK = S.INK
JS = V4.JS                           # people scale in the hold (1.75)
JX, JY = V4.J_PAINT                  # sleeping Jonah's anchor (as in s04)
LHX, LHY = V4.LANTERN_HOOK
HX0, HX1 = V4.HATCH
HY0, HY1 = V4.HATCH_Y
BEAM_BOT = 316                       # underside of the long deck beam below the hatch
OPEN_Y1 = 256                        # the hatch opening shows between HY0 and the beam top
FLOOR_Y = 1116                       # people standing on the hold floor (just in front of the back wall)
CAM0 = Cam(V4.V0[0], V4.V0[1], V4.VIEW_W_INT * 0.96)   # s04's final framing

# ladder (painted by V4.hold_svg): rails from (HX0+50, 300) / (HX1-60, 300) down to (HX0+200, 1112) / (HX1+90, 1112)
LAD_K = 150 / 812


def lad_cx(y):
    """Centre between the ladder rails at height y."""
    return (HX0 + 50 + HX1 - 60) / 2 + LAD_K * (y - 300)


# where things stand
KNEEL = (JX + 234 * JS, JY)          # the captain kneeling on the bed behind Jonah's head (C.captain 'wake' recipe)
X_ARR = 1622                         # his last walk contact on the floor, just past the end of the bed
CAP_X = 1652                         # his standing spot while he talks
J_WAKE_X = 1286                      # Jonah sitting up (facing left, legs along the bed)
J_SIT_X = 1236                       # Jonah sitting, turned toward the captain
J_STAND_X = 1296                     # Jonah on his feet in front of the bed (clear of the swinging lantern)

# the captain's walk: CAP_N drawings per step, two steps per cycle (see cap_walk_pose)
CAP_A = 58
CAP_N = 4
CAP_DD = 2 * CAP_A * JS / CAP_N      # stage px the anchor advances per drawing (planted sole stays put)
FR = 1 / 30


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=H)


# ============================================================== narration timing

PUNCT = "，。！？：；、,.!?:;"


def _subphrases(text):
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in PUNCT:
            out.append(cur)
            cur = ""
    if cur.strip():
        out.append(cur)
    return out


def _nchar(s):
    return max(1, sum(1 for ch in s if ch not in PUNCT and not ch.isspace()))


def _voice_gaps(path):
    """Silent stretches (>= 70 ms) inside a voice take: [(start, end)] in seconds, or [] if unreadable."""
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
    sil = e < 0.02 * e.max()
    gaps, i = [], 0
    while i < nb:
        if sil[i]:
            j = i
            while j < nb and sil[j]:
                j += 1
            if j - i >= 7 and i > 0 and j < nb:
                gaps.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return gaps


class Phrases:
    """Every punctuation-delimited piece of every line, timed: subtitle chunks first, then the pauses in the voice
    take inside a chunk (the pause nearest to a proportional estimate), then the estimate itself."""

    def __init__(self, ctx):
        self.items = []          # (text, start, end, line index)
        self.gaps = []
        for i, ln in enumerate(ctx.lines):
            gaps = [(ln.start + a, ln.start + b)
                    for a, b in _voice_gaps(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav")]
            self.gaps += gaps
            chunks = ln.chunks or []
            spans = [(c.text, c.start, c.end) for c in chunks] or [(ln.text, ln.start, ln.end)]
            for text, c0, c1 in spans:
                subs = _subphrases(text)
                n = [_nchar(s) for s in subs]
                tot, acc, bounds, used = sum(n), 0, [], set()
                for k in range(len(subs) - 1):
                    acc += n[k]
                    est = c0 + (c1 - c0) * acc / tot
                    best = None
                    for gi, (a, b) in enumerate(gaps):
                        if gi in used or not (c0 + 0.15 < a and b < c1 - 0.1):
                            continue
                        if bounds and a <= bounds[-1][1]:
                            continue
                        d = abs((a + b) / 2 - est)
                        if d < 0.7 and (best is None or d < best[0]):
                            best = (d, gi, a, b)
                    if best:
                        used.add(best[1])
                        bounds.append((best[2], best[3]))
                    else:
                        bounds.append((est - 0.05, est + 0.05))
                s = c0
                for k, sub in enumerate(subs):
                    e = bounds[k][0] if k < len(bounds) else c1
                    self.items.append((sub, s, e, i))
                    if k < len(bounds):
                        s = bounds[k][1]

    def find(self, key):
        for it in self.items:
            if key in it[0]:
                return it
        return None

    def start(self, key, default):
        it = self.find(key)
        return it[1] if it else default

    def end(self, key, default):
        it = self.find(key)
        return it[2] if it else default

    def inner(self, key, sub, default):
        """Time at which ``sub`` starts inside the piece containing ``key`` (snapped to a nearby voice pause)."""
        it = self.find(key)
        if not it or sub not in it[0]:
            return default
        text, s, e, _ = it
        est = s + (e - s) * _nchar(text[:text.index(sub)]) / _nchar(text)
        best = None
        for a, b in self.gaps:
            if s < a and b < e and abs(b - est) < 0.35 and (best is None or abs(b - est) < abs(best - est)):
                best = b
        return best if best is not None else est


# ============================================================== snore -> breathing (as in v1 s04, own cache file)

def snore_inhale_peaks(scene_id, at, dur):
    """Scene times at which the snore cue (rendered as audio/mix.py renders it) reaches the end of each inhale."""
    key = f"{scene_id}:snore:{float(at)}:{float(dur):.4f}"
    path = CACHE / "s05_captain_snore_peaks.json"
    try:
        cache = json.loads(path.read_text())
    except Exception:
        cache = {}
    if key in cache:
        return [at + p for p in cache[key]]
    try:
        from scipy import signal

        from audio import sfx
        from engine.paths import SR
        seed = zlib.crc32(f"{scene_id}:snore:{float(at)}".encode()) & 0xFFFF
        x = np.asarray(sfx.make("snore", dur, SR, seed=seed), np.float64)
        x = x.mean(axis=1) if x.ndim == 2 else x
        y = signal.sosfiltfilt(signal.butter(4, (150, 360), "bandpass", fs=SR, output="sos"), x)
        hop = SR // 100
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
        tmp = path.with_suffix(".part")
        tmp.write_text(json.dumps(cache))
        tmp.replace(path)
    except Exception:
        pass
    return [at + p for p in rel]


# ============================================================== figures

def cap_fig(x, y, ps, facing=-1, expr="worried", label="pose", shadow=True, scale=JS):
    """The captain (same design and rig as C.captain) in a scene-local pose record."""
    inner, _ = C._figure(C._captain_design(), C._CAPTAIN_M, dict(ps), expr, C._fsign(facing))
    out = C.ground_shadow(x, y + 2, scale, width=130) if shadow else ""
    return out + C._wrap_out(inner, x, y, scale, facing, f"captain-{label}")


def jonah_fig(x, y, ps, facing=1, expr="neutral", label="pose", scale=JS):
    """Jonah (same design as C.jonah) in a scene-local pose record."""
    inner, _ = C._figure(C._jonah_design(), C._ADULT, dict(ps), expr, C._fsign(facing))
    return C._wrap_out(inner, x, y, scale, facing, f"jonah-{label}")


def cap_walk_pose(k):
    """Walk drawing k (v1 s05's planted-foot cycle with CAP_N drawings per step): the planted ankle goes from +CAP_A
    to -CAP_A figure px (forward = +) while the other foot swings from -CAP_A to +CAP_A, lifted mid-swing; drawing 0
    is the contact with the far foot forward."""
    ph = (k % (2 * CAP_N)) / CAP_N
    step, u = divmod(ph, 1.0)
    plant = ("ik", CAP_A * (1 - 2 * u), 1)
    swing = ("ik", -CAP_A + 2 * CAP_A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, 26 * math.sin(math.pi * u))
    sw = 40 * math.cos(math.pi * ph)
    return C._P(t=9, h=-6, legs=(plant, swing) if step == 0 else (swing, plant),
                arms=(("fk", -sw, -sw + 18), ("fk", sw, sw + 18)), drop=14 + 4 * math.cos(2 * math.pi * u))


SLIDE_REF_Y = 700.0                  # the slide drawing is made with its anchor here, then moved along the ladder
SLIDE_ROT = -math.degrees(math.atan(LAD_K))   # his body leans with the ladder (top toward the left)
RAIL_HALF = 95 * math.cos(math.radians(SLIDE_ROT)) / JS   # rail half-spacing across his (tilted) body, figure px


def cap_poses():
    return {
        # climbing down the ladder, back to it (the layer is tilted by SLIDE_ROT so he lies along the rails):
        # one hand high on one rail, the other low on the other rail, the foot on that side raised one rung
        "climb_a": C._P(t=-2, h=12, legs=(("ik", 10, 1, 50), ("ik", -8, 1, 0)),
                        arms=(("ik", "abs", RAIL_HALF + 4, -318, 1), ("ik", "abs", -RAIL_HALF - 2, -168, 1)),
                        hands=("fist", "fist")),
        "climb_b": C._P(t=-2, h=12, legs=(("ik", 8, 1, 0), ("ik", -10, 1, 50)),
                        arms=(("ik", "abs", RAIL_HALF + 2, -168, -1), ("ik", "abs", -RAIL_HALF - 4, -318, -1)),
                        hands=("fist", "fist")),
        # landing at the foot of the ladder: crouched, arms out for balance
        "land": C._P(t=12, h=-4, drop=40, legs=(("ik", 34, 1), ("ik", -30, 1)),
                     arms=(("fk", 58, 96), ("fk", -46, -20)), hands=("open", "open")),
        # stepping up onto the bed end, reaching for Jonah (in-between of the hop into the kneel)
        "reach": C._P(t=30, h=-10, drop=30, legs=(("ik", 34, 1), ("ik", -34, 1, 18)),
                      arms=(("fk", 62, 84), ("fk", 46, 76)), hands=("open", "open")),
        # kneeling on the bed behind Jonah: C.captain 'wake' (far hand on his shoulder, near hand on his head)
        # straightening up again after the shake (still kneeling)
        "rise": C._P(t=14, h=-6, drop=34, legs=(("ik", 52, 1), ("ik", -24, 1)),
                     arms=(("fk", 24, 50), ("fk", 18, 44)), hands=("open", "open")),
        "stand": C.POSES["stand"],
        # "快醒醒！": leaning in, both palms raised toward Jonah
        "urge": C._P(t=7, h=-2, legs=((8, 2), (-8, -3)), arms=(("fk", 46, 146), ("fk", 26, 136)),
                     hands=("open", "open")),
        # "风浪这么大": both hands on his cap
        "worried": C.POSES["worried"],
        # "你怎么还在睡觉？": palms up in front, head tilted
        "why": C._P(t=2, h=12, legs=((6, 2), (-6, -2)), arms=(("fk", 8, 72), ("fk", -16, 64)),
                    hands=("open", "open")),
        # "快起来，": near arm up and back toward the hatch (pointing to the deck), far hand beckoning Jonah
        "up": C._P(t=-3, h=-2, legs=((6, 2), (-6, -2)), arms=(("fk", 46, 128), ("fk", -152, -164)),
                   hands=("open", "point")),
        # "求你的神": still pointing up to the deck, now looking up at the hatch
        "uplook": C._P(t=-5, h=-22, legs=((6, 2), (-6, -2)), arms=(("fk", 22, 34), ("fk", -136, -150)),
                       hands=("fist", "point"), look=(-0.04, -0.08)),
        # "救救我们吧！": both hands raised to heaven
        "pray": C._P(t=-6, h=-20, legs=((6, 2), (-6, -2)), arms=(("fk", 152, 168), ("fk", -152, -168)),
                     hands=("open", "open"), look=(0.02, -0.06)),
        # "也许你的神会可怜我们……": hands clasped at the chest, leaning toward Jonah
        "plead": C._P(t=6, h=8, legs=((6, 2), (-6, -2)),
                      arms=(("ik", "torso", 1.45, 0.64, 1), ("ik", "torso", 1.45, 0.64, 1)),
                      hands=("none", "pray")),
    }


def jonah_poses():
    return {
        # looking up toward the hatch and the storm above (he knows it is his doing)
        "stand_up": C._P(t=-2, h=-16, arms=(("fk", 12, 8), ("fk", -6, -2)), look=(0.05, -0.08)),
        "stand_sorry": C._P(t=3, h=16, arms=(("ik", "torso", 0.9, 0.24, 1), ("ik", "torso", 0.95, 0.2, 1)),
                            hands=("none", "fist")),
    }


# ============================================================== hold extras (the opening hatch, light, rain)

def hatch_open_svg(seed):
    """The hatch opening without its grating: dark storm sky, scudding cloud, rain (one frame of a boil loop)."""
    r = random.Random(seed)
    x0, x1, y0, y1 = HX0 + 2, HX1 - 2, HY0 + 2, OPEN_Y1 + 2
    defs = S.lin_grad("osky", [(0, "#2a3446"), (0.6, P["storm_sky_top"]), (1, P["storm_sky"])])
    body = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#osky)"/>'
    cl = ""
    for k in range(4):
        cx = x0 + (x1 - x0) * (k + 0.5) / 4 + r.uniform(-20, 20)
        cl += f'<ellipse cx="{cx:.0f}" cy="{y0 + r.uniform(10, 40):.0f}" rx="{r.uniform(60, 90):.0f}" ' \
              f'ry="{r.uniform(18, 28):.0f}" fill="#46536a" opacity="0.8"/>'
    body += S.g(cl, filter="soft")
    for _ in range(30):
        x, y = r.uniform(x0, x1 + 30), r.uniform(y0 - 30, y1 - 10)
        ln = r.uniform(26, 46)
        body += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 0.3 * ln:.0f}" y2="{y + ln:.0f}" stroke="#dde7f0" '
                 f'stroke-width="3.5" stroke-linecap="round" opacity="{r.uniform(0.45, 0.85):.2f}"/>')
    clip = f'<clipPath id="hoc"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath>'
    return doc(f'{clip}<g clip-path="url(#hoc)">{body}</g>', defs)


def grate_svg():
    """The hatch grating (V4.hatch_slats) above the beam, on its own layer so it can swing open."""
    clip = f'<clipPath id="grc"><rect x="{HX0 - 30}" y="{HY0 - 30}" width="{HX1 - HX0 + 60}" height="{OPEN_Y1 - HY0 + 30}"/></clipPath>'
    return doc(f'{clip}<g clip-path="url(#grc)">{S.g(V4.hatch_slats(), filter="wobble-fine")}</g>')


def shaft_svg():
    """Cold storm light falling through the open hatch onto the floor."""
    defs = S.lin_grad("cshaft", [(0, "#d6e4f2", 0.55), (0.55, "#b9cde0", 0.22), (1, "#b9cde0", 0.0)])
    d = (f"M{HX0 + 10},{OPEN_Y1} L{HX1 - 10},{OPEN_Y1} L{HX1 + 190},{FLOOR_Y + 40} "
         f"L{HX0 + 10},{FLOOR_Y + 40} Z")
    body = f'<path d="{d}" fill="url(#cshaft)" filter="url(#blur-md)"/>'
    body += (f'<ellipse cx="{HX0 + 190}" cy="{FLOOR_Y + 30}" rx="230" ry="34" fill="#cfdeea" opacity="0.35" '
             f'filter="url(#blur-md)"/>')
    return doc(body, defs)


def shaft_rain_svg(seed):
    """Rain blowing in through the open hatch (one frame of a boil loop), inside the light shaft."""
    r = random.Random(seed)
    body = ""
    for _ in range(26):
        y = r.uniform(OPEN_Y1 + 40, FLOOR_Y - 60)
        u = (y - OPEN_Y1) / (FLOOR_Y - OPEN_Y1)
        xl = HX0 + 30
        xr = HX1 - 20 + 200 * u
        x = r.uniform(xl, xr)
        ln = r.uniform(30, 52)
        body += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 0.28 * ln:.0f}" y2="{y + ln:.0f}" stroke="#e2ebf3" '
                 f'stroke-width="3" stroke-linecap="round" opacity="{r.uniform(0.35, 0.7) * (1 - 0.5 * u):.2f}"/>')
    for _ in range(3):   # little rings on the floor puddle
        x = r.uniform(HX0 + 70, HX0 + 290)
        y = r.uniform(1142, 1158)
        rr = r.uniform(12, 24)
        body += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr * 0.3:.1f}" fill="none" stroke="#e8f0f6" '
                 f'stroke-width="2.5" opacity="0.55"/>')
    return doc(body)


def flash_svg():
    """Lightning seen through the hatch: a cold bloom at the opening and down the shaft."""
    body = (f'<path d="M{HX0 + 20},{BEAM_BOT - 20} L{HX1 - 20},{BEAM_BOT - 20} L{HX1 + 220},{FLOOR_Y} '
            f'L{HX0 + 20},{FLOOR_Y} Z" fill="#a9bde4" opacity="0.5" filter="url(#blur-lg)"/>'
            f'<ellipse cx="{(HX0 + HX1) / 2}" cy="{(HY0 + OPEN_Y1) / 2}" rx="280" ry="150" fill="#c8d6f0" '
            f'opacity="0.85" filter="url(#blur-md)"/>')
    return doc(body)


class Cutout:
    """Pixels of the watercoloured hold painting inside a mask (identical to the painting's own pixels: rasterised
    and watercoloured exactly as the compositor does it), drawn OVER a figure that passes behind that part of the
    room: the ceiling and beam round the hatch, the right-hand foreground post."""

    def __init__(self, layer, mask_body, box):
        self.layer, self.mask_body, self.box = layer, mask_body, box
        self.res = None

    def get(self):
        if self.res is None:
            from engine import raster
            from engine import watercolor as WC
            hl = self.layer
            im = raster.rasterize(hl.frames[0], W, H)
            if hl.wc > 0:
                im = WC.watercolor(im, seed=hl.seed, strength=hl.wc, edge=hl.wc_edge)
            m = raster.rasterize(doc(self.mask_body).replace(S.BOIL_TOKEN, "1"), W, H).getchannel("A")
            crop = np.asarray(im.crop(self.box)).copy()
            a = crop[..., 3].astype(np.float32) * (np.asarray(m.crop(self.box), np.float32) / 255.0)
            crop[..., 3] = (a + 0.5).astype(np.uint8)
            self.res = (Image.fromarray(crop, "RGBA"), self.box[:2])
        return self.res


# ============================================================== motion helpers

def bump(t, ts, w=0.07):
    """0..1..0 triangle just after ts (a 3-4 frame hop that sells a pose swap)."""
    return max(0.0, 1 - abs(t - ts - 0.035) / w)


def pop(t, switches, amt=0.08):
    """Squash factor (sx, sy) for a quick 'pop' at each pose switch."""
    sx = sy = 1.0
    for ts in switches:
        u = (t - ts) / 0.24
        if 0 <= u <= 1:
            b = math.sin(math.pi * u) * (1 - u)
            sy *= 1 - amt * b
            sx *= 1 + 0.55 * amt * b
    return sx, sy


def keyed(keys_, curve="sine"):
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


def flipbook(sc, name, keyframes, z, motion, wc=1.0):
    """Layer from [(t, svg), ...] with hard switches at the given times."""
    times = [k[0] for k in keyframes]
    svgs = [k[1] if k[1].startswith("<svg") else doc(k[1]) for k in keyframes]

    def at(t):
        i = 0
        for j, tj in enumerate(times):
            if t >= tj:
                i = j
        return float(i)
    if len(svgs) == 1:
        sc.add(name, svgs[0], z=z, motion=motion, wc=wc)
    else:
        sc.add(name, svgs, z=z, motion=motion, frame_at=at, wc=wc)


# ============================================================== build

def build(ctx):
    T = ctx.duration
    L = ctx.lines
    sc = Scene(ctx, W=W, H=H)
    ph = Phrases(ctx)
    l0 = L[0]
    lc = L[1:] if len(L) > 1 else L          # the captain's lines
    c_start = lc[0].start

    # ---------------------------------------------------------------- key times (all from the narration)
    t_n = l0.start                                              # "船长找到了约拿，"
    t_shake_say = ph.start("摇醒", l0.start + 0.52 * (l0.end - l0.start))
    t_say = ph.start("说", l0.end - 0.5)
    t_open = max(t_n + 0.02, 1.0)                               # the grating is flung open as the captain is named
    #                                                             (not before the 1 s cross-dissolve has finished)
    t_slide0 = t_open + 0.2                                     # his sandals appear in the opening
    t_land = t_slide0 + 0.92                                    # hops off the ladder at its foot
    t_walk0 = t_land + 0.16                                     # first walk drawing
    n_walk = max(4, round((lad_cx(1112) - X_ARR) / CAP_DD))
    X_START = X_ARR + n_walk * CAP_DD                           # where he lands (centred on the ladder foot)
    t_arr = t_walk0 + n_walk * 2 * FR                           # last contact (2 frames per drawing)
    t_ib = t_arr + 2 * FR                                       # steps up onto the bed end, reaching ...
    t_bend = t_ib + 4 * FR                                      # ... and kneels behind Jonah's head
    t_shake0 = max(t_bend + 0.1, t_shake_say)
    t_wake = max(t_shake0 + 0.85, ph.end("摇醒", t_say - 0.12) - 0.06)   # Jonah sits up at the end of "摇醒"
    t_rise = t_wake - 0.1
    t_shake1 = t_rise
    # line 1
    t_urge = ph.start("快醒醒", c_start) - 0.08
    t_storm = ph.start("风浪", c_start + 0.3 * (lc[0].end - c_start))
    t_cworry = t_storm + 0.05
    t_startle = t_storm + 0.14                                  # Jonah turns round with a start
    t_why = ph.start("怎么还在睡", t_storm + 1.0) - 0.06
    t_jworry = t_why + 0.75
    # line 2
    lq = lc[-1]
    t_up = ph.start("快起来", lq.start) - 0.06
    t_stand = t_up + 0.4                                        # Jonah jumps to his feet
    t_look = ph.start("求你的神", t_up + 0.9)
    t_pray = ph.inner("求你的神", "救救", t_look + 1.05) - 0.02
    t_plead = ph.start("也许", lq.start + 0.45 * (lq.end - lq.start)) - 0.06
    t_sorry = t_plead + 0.85
    t_live = ph.start("让我们活下来", t_plead + 2.6)
    t_pity = ph.inner("也许", "可怜", t_plead + 1.4)             # a pleading nod on "可怜我们"
    t_jlook = t_live + 0.35                                     # Jonah looks up toward the storm above
    t_flash2 = t_pray + 0.08
    END_CALM = T - 1.2

    # ---------------------------------------------------------------- the ship's gentle roll (camera) and a lurch
    def lurch(t):
        u = t - t_storm
        if u < 0 or u > 1.6:
            return 0.0
        return 1.25 * math.exp(-u / 0.45) * math.sin(2 * math.pi * u / 0.9)

    def roll(t):
        a = 0.42 * M.progress(t, 0.0, 1.6, "sine")
        return a * math.sin(2 * math.pi * t / 4.6) + lurch(t)

    # ---------------------------------------------------------------- hold painting (s04's, same seed)
    sc.add("hold", V4.hold_svg(), z=0, wc=1.0, seed=101)
    hold_layer = sc.layers[-1]

    # hatch: s04's closed grating with rain until it is flung open, then the open sky, the grating swinging up
    grate_t = (t_open, t_open + 0.26)
    sc.add("hatch_closed", [V4.hatch_rain_svg(s) for s in (1, 2, 3)], z=1, wc=0,
           motion=lambda t: Tf(alpha=1.0 if t < grate_t[0] else 0.0),
           frame_at=lambda t: float(int(t * 11) % 3))
    sc.add("hatch_open", [hatch_open_svg(s) for s in (4, 5, 6)], z=1.1, wc=0,
           motion=lambda t: Tf(alpha=1.0 if t >= grate_t[0] else 0.0),
           frame_at=lambda t: float(int(t * 11) % 3))

    def grate_m(t):
        if t < grate_t[0] or t > grate_t[1] + 0.05:
            return Tf(alpha=0.0)
        u = M.progress(t, grate_t[0], grate_t[1], "in")
        return Tf(dy=-6 * u, sy=max(0.03, 1 - u), alpha=1 - M.progress(t, grate_t[1] - 0.06, grate_t[1] + 0.05),
                  px=(HX0 + HX1) / 2, py=HY0 - 8)
    sc.add("grate", grate_svg(), z=1.2, wc=0.6, motion=grate_m)

    # ---------------------------------------------------------------- captain: slide, land + walk, main poses
    CP = cap_poses()
    cap_layers_z = 2.85                    # behind Jonah (he kneels on the bed behind Jonah's head)

    # climbing down the ladder, back to it, two rungs per move: the two climb drawings alternate at every move
    # (the raised hand / raised foot swap sides), the body drops quickly and holds (layer tilted along the rails)
    rungs = [300 + 812 * k / 9 for k in range(0, 10)]
    cy = [120.0] + [rungs[k] for k in (0, 2, 4, 6, 8)]            # anchor heights: above the hatch .. lowest rung
    STEP = (t_land - t_slide0) / (len(cy) - 0.4)
    MOVE = 0.55 * STEP

    def climb_state(t):
        """(drawing index, anchor y) on the ladder."""
        k = int((t - t_slide0) / STEP) if t >= t_slide0 else -1
        if k < 0:
            return 0, cy[0]
        if k >= len(cy) - 1:
            return (len(cy) - 1) % 2, cy[-1]
        u = M.progress(t, t_slide0 + k * STEP, t_slide0 + k * STEP + MOVE, "out")
        return (k + 1) % 2, M.lerp(cy[k], cy[k + 1], u)

    slide_x0 = lad_cx(SLIDE_REF_Y)

    def climb_m(t):
        if not (t_slide0 - 0.05 <= t < t_land):
            return Tf(alpha=0.0)
        y = climb_state(t)[1]
        x = lad_cx(y) + (X_START - lad_cx(1112)) * (y - cy[0]) / (FLOOR_Y - cy[0])
        return Tf(dx=x - slide_x0, dy=y - SLIDE_REF_Y, rot=SLIDE_ROT, px=slide_x0, py=SLIDE_REF_Y)
    sc.add("cap_climb", [doc(cap_fig(slide_x0, SLIDE_REF_Y, CP[k], expr="worried", label=k, shadow=False))
                         for k in ("climb_a", "climb_b")], z=cap_layers_z, motion=climb_m,
           frame_at=lambda t: float(climb_state(t)[0]))

    # landing crouch + the planted-foot walk to the bed (+ the step-in in-between), drawn at X_START
    walk_frames = [doc(cap_fig(X_START, FLOOR_Y, CP["land"], expr="worried", label="land"))]
    for k in range(2 * CAP_N):
        walk_frames.append(doc(cap_fig(X_START, FLOOR_Y, cap_walk_pose(k), expr="worried", label=f"walk{k}")))
    # in-between: stepping up onto the end of the bed and reaching for Jonah (a short hop arc into the kneel)
    walk_frames.append(doc(cap_fig(X_START, FLOOR_Y, CP["reach"], expr="worried", label="reach", shadow=False)))
    N_IB = 2 * CAP_N + 1
    ib_from = (X_ARR - 30, FLOOR_Y)
    ib_to = (KNEEL[0] + 40, KNEEL[1] + 12)

    def walk_idx(t):
        if t < t_walk0:
            return 0
        i = int((t - t_walk0) / (2 * FR) + 1e-6)
        if i <= n_walk:
            k = (i - n_walk) % (2 * CAP_N)          # drawing n_walk is the contact with the far foot forward
            return 1 + k
        return N_IB

    def walk_xy(t):
        if t < t_walk0:
            return X_START, FLOOR_Y
        i = int((t - t_walk0) / (2 * FR) + 1e-6)
        if i <= n_walk:
            return X_START - i * CAP_DD, FLOOR_Y
        u = M.progress(t, t_ib, t_bend, "linear")
        return (M.lerp(ib_from[0], ib_to[0], u), M.lerp(ib_from[1], ib_to[1], u) - 34 * math.sin(math.pi * u))

    def walk_m(t):
        if t < t_land or t >= t_bend:
            return Tf(alpha=0.0)
        sx, sy = pop(t, [t_land], 0.12)
        x, y = walk_xy(t)
        return Tf(dx=x - X_START, dy=y - FLOOR_Y, sx=sx, sy=sy, px=X_START, py=FLOOR_Y)
    sc.add("cap_walk", walk_frames, z=cap_layers_z, motion=walk_m, frame_at=lambda t: float(walk_idx(t)))

    kx, ky = KNEEL
    main = [
        (t_bend, C.captain(kx, ky, JS, -1, pose="wake", expr="worried")),
        (t_rise, cap_fig(kx, ky, CP["rise"], expr="worried", label="rise", shadow=False)),
        (t_wake, cap_fig(CAP_X, FLOOR_Y, CP["stand"], expr="worried", label="stand")),
        (t_urge, cap_fig(CAP_X, FLOOR_Y, CP["urge"], expr="shout", label="urge")),
        (t_cworry, cap_fig(CAP_X, FLOOR_Y, CP["worried"], expr="scared", label="worried")),
        (t_why, cap_fig(CAP_X, FLOOR_Y, CP["why"], expr="worried", label="why")),
        (t_up, cap_fig(CAP_X, FLOOR_Y, CP["up"], expr="shout", label="up")),
        (t_look, cap_fig(CAP_X, FLOOR_Y, CP["uplook"], expr="worried", label="uplook")),
        (t_pray, cap_fig(CAP_X, FLOOR_Y, CP["pray"], expr="worried", label="pray")),
        (t_plead, cap_fig(CAP_X, FLOOR_Y, CP["plead"], expr="worried", label="plead")),
    ]
    switches = [k[0] for k in main[2:]]

    def cap_m(t):
        if t < t_bend:
            return Tf(alpha=0.0)
        sx, sy = pop(t, [t_bend] + switches, 0.08)
        br = 1 + 0.011 * math.sin(2 * math.pi * (t / 3.1 + 0.3))
        sy *= br
        if t < t_rise:
            dx = 7 * math.sin(2 * math.pi * 4.6 * (t - t_shake0)) if t_shake0 <= t < t_shake1 else 0.0
            return Tf(dx=dx, sx=sx, sy=sy, px=kx, py=ky)
        if t < t_wake:
            return Tf(sx=sx, sy=sy, px=kx, py=ky)
        # hop down from the bed to his standing spot, then little hops at each gesture; a lean-in on "让我们活下来"
        u = M.progress(t, t_wake, t_wake + 0.22, "linear")
        dx = (kx + 30 - CAP_X) * (1 - M.ease("sine")(u))
        dy = (ky - FLOOR_Y) * (1 - u) - 30 * math.sin(math.pi * u) - 8 * sum(bump(t, s) for s in switches[1:])
        rot = -2.2 * M.progress(t, t_live - 0.1, t_live + 0.5, "sine") * (1 - M.progress(t, t_live + 1.6, t_live + 2.6))
        if t_pity <= t <= t_pity + 0.7:
            rot -= 1.8 * math.sin(math.pi * (t - t_pity) / 0.7)
        return Tf(dx=dx, dy=dy, rot=rot, sx=sx, sy=sy, px=CAP_X, py=FLOOR_Y)
    flipbook(sc, "cap_main", main, z=cap_layers_z + 0.05, motion=cap_m)

    # ---------------------------------------------------------------- Jonah
    # breathing in time with the snore (continues s04); the snore stops once he is shaken
    snore_at, snore_dur = 0.0, round(t_shake0 + 0.25, 3)
    peaks = []
    for k in range(6):
        at_k = round(0.07 * k, 3)
        pk = snore_inhale_peaks(ctx.id, at_k, round(snore_dur - at_k, 3))
        if not pk or any(0.5 <= p <= t_shake0 - 0.3 for p in pk):
            snore_at, peaks = at_k, pk
            break
    snore_dur = round(t_shake0 + 0.25 - snore_at, 3)
    breath = V4.breath_curve(peaks)

    def shaken(t, k=1.0):
        if t_shake0 <= t < t_shake1:
            v = math.sin(2 * math.pi * 4.6 * (t - t_shake0) - 0.5)
            return 6 * k * v, 1.3 * k * v
        return 0.0, 0.0

    def jsleep_m(t):
        if t >= t_wake:
            return Tf(alpha=0.0)
        b = breath(t) if t < t_shake0 else 0.0
        dx, rot = shaken(t)
        return Tf(dx, 0, rot, 1 + 0.006 * b, 1 + 0.024 * b, 1.0, JX, JY)
    sc.add("jonah_sleep", doc(C.jonah(JX, JY, JS, -1, pose="sleep", marks=False)), z=3, motion=jsleep_m)

    # little shake marks beside the sleeper while he is shaken (two variants flicking at 8 fps)
    def shake_marks(off):
        st = f'fill="none" stroke="{P["ink_soft"]}" stroke-width="6" stroke-linecap="round"'
        out = ""
        for x, y, ln in ((1036, 820, 50), (1112, 806, 64)):          # over his back
            y -= off
            out += f'<path d="M{x - ln / 2},{y} Q{x},{y - 14} {x + ln / 2},{y}" {st}/>'
        for x, y, ln in ((904, 862, 50), (880, 898, 62)):            # beside his knees
            x -= off
            out += f'<path d="M{x},{y - ln / 2} Q{x - 14},{y} {x},{y + ln / 2}" {st}/>'
        return doc(S.g(out, filter="wobble-fine"))
    sc.add("shake_marks", [shake_marks(0), shake_marks(10)], z=3.05, wc=0,
           motion=lambda t: Tf(alpha=M.progress(t, t_shake0 + 0.05, t_shake0 + 0.15) *
                               (1 - M.progress(t, t_shake1 - 0.12, t_shake1))),
           frame_at=lambda t: float(int(t * 8) % 2))

    JP = jonah_poses()
    seated = [
        (t_wake, C.jonah(J_WAKE_X, JY, JS, -1, pose="wake", expr="sleepy")),
        (t_startle, C.jonah(J_SIT_X, JY, JS, 1, pose="sit", expr="surprised")),
        (t_jworry, C.jonah(J_SIT_X, JY, JS, 1, pose="sit", expr="worried")),
    ]

    def jseat_m(t):
        if t < t_wake or t >= t_stand:
            return Tf(alpha=0.0)
        px = J_WAKE_X if t < t_startle else J_SIT_X
        sx, sy = pop(t, [t_wake, t_startle, t_jworry], 0.09)
        sy *= 1 + 0.009 * math.sin(2 * math.pi * (t / 3.3 + 0.1))
        dy = -14 * bump(t, t_wake) - 20 * bump(t, t_startle, 0.09)
        rot = 0.0
        if t < t_startle:      # sleepy sway while rubbing the eye
            rot = 2.2 * math.sin(2 * math.pi * (t - t_wake) / 2.6) * M.progress(t, t_wake + 0.2, t_wake + 0.8)
        # paper cut-out turn round the facing flip
        k = 1.0
        u = abs(t - t_startle) / 0.09
        if u < 1:
            k = 1 - 0.7 * (1 - u)
        return Tf(0, dy, rot, sx * k, sy, 1.0, px, JY)
    flipbook(sc, "jonah_seated", [(k[0], doc(k[1])) for k in seated], z=3.1, motion=jseat_m)

    standing = [
        (t_stand, C.ground_shadow(J_STAND_X, FLOOR_Y + 2, JS, width=120)
         + C.jonah(J_STAND_X, FLOOR_Y, JS, 1, pose="stand", expr="worried")),
        (t_sorry, C.ground_shadow(J_STAND_X, FLOOR_Y + 2, JS, width=120)
         + jonah_fig(J_STAND_X, FLOOR_Y, JP["stand_sorry"], 1, expr="sorry", label="sorry")),
        (t_jlook, C.ground_shadow(J_STAND_X, FLOOR_Y + 2, JS, width=120)
         + jonah_fig(J_STAND_X, FLOOR_Y, JP["stand_up"], 1, expr="worried", label="lookup")),
    ]

    def jstand_m(t):
        if t < t_stand:
            return Tf(alpha=0.0)
        sx, sy = pop(t, [t_stand, t_sorry, t_jlook], 0.09)
        sy *= 1 + 0.010 * math.sin(2 * math.pi * (t / 3.4 + 0.6))
        u = M.progress(t, t_stand, t_stand + 0.2, "linear")
        dy = -26 * math.sin(math.pi * u) - 6 * bump(t, t_sorry) - 6 * bump(t, t_jlook)
        return Tf(0, dy, 0, sx, sy, 1.0, J_STAND_X, FLOOR_Y)
    flipbook(sc, "jonah_stand", standing, z=3.2, motion=jstand_m)

    # Z z z drifting up from the sleeper (continues s04), fading as the captain arrives
    head = (JX + 240, JY - 140)
    for i, delay in enumerate((0.0, 0.75, 1.5)):
        zsvg = doc(S.text(head[0] + 50, head[1] - 50, "Z", size=84, fill="#fff3d6",
                          extra=f'stroke="{INK}" stroke-width="8" paint-order="stroke"'))

        def zm(t, delay=delay):
            per = 2.25
            u = ((t + delay) % per) / per
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine"))
            a *= 1 - M.progress(t, t_land, t_land + 0.5, "sine")
            s = 0.45 + 0.75 * u
            return Tf(70 + 190 * u + 26 * math.sin(u * 6.0), -30 - 330 * u, -12 + 22 * u, s, s, a,
                      head[0] + 50, head[1] - 70)
        sc.add(f"z{i}", zsvg, wc=0, z=2.8, motion=zm)

    # ---------------------------------------------------------------- occluders over the captain on the ladder
    cut_ceiling = Cutout(hold_layer,
                         f'<path d="M-40,-80 L{W + 40},-80 L{W + 40},{BEAM_BOT + 3} L-40,{BEAM_BOT + 3} Z '
                         f'M{HX0 + 3},{HY0 + 3} L{HX0 + 3},{OPEN_Y1} L{HX1 - 3},{OPEN_Y1} L{HX1 - 3},{HY0 + 3} Z" '
                         f'fill="#000" fill-rule="evenodd"/>',
                         (HX0 - 140, 0, HX1 + 150, BEAM_BOT + 6))
    cut_post = Cutout(hold_layer,
                      '<path d="M2145,-40 Q2050,700 2125,1390" fill="none" stroke="#000" stroke-width="152"/>',
                      (1990, 260, 2240, 1250))
    cut_ceiling.get()
    cut_post.get()
    sc.add_dynamic("cut_ceiling", lambda t: cut_ceiling.get() if t_slide0 - 0.1 <= t < t_land else None, z=6)
    sc.add_dynamic("cut_post", lambda t: cut_post.get() if t_slide0 <= t < t_walk0 + 0.35 else None, z=6.1)

    # ---------------------------------------------------------------- light: lantern, storm light, flashes
    swing = lambda t: 8 * math.sin(2 * math.pi * t / 3.1 + 0.6) - 0.6 * roll(t) + 5 * lurch(t)   # noqa: E731
    glow = f'<ellipse cx="{LHX + 60}" cy="{LHY + 400}" rx="600" ry="520" fill="url(#lg2)"/>'
    sc.add("lamp_glow", doc(glow, S.rad_grad("lg2", [(0, "#ffd890", 0.5), (0.35, "#ffc870", 0.22), (1, "#ffc060", 0)])),
           wc=0, blend="add", z=8,
           motion=lambda t: Tf(0, 0, swing(t), 1, 1, 0.85 + 0.1 * math.sin(t * 7.3) + 0.05 * math.sin(t * 12.1),
                               LHX, LHY))
    sc.add("lantern", doc(f'<line x1="{LHX}" y1="{LHY - 10}" x2="{LHX}" y2="{LHY + 44}" stroke="{INK}" stroke-width="5"/>'
                          + PR.lantern(LHX, LHY + 34, 1.5)), z=9,
           motion=lambda t: Tf(0, 0, swing(t), 1, 1, 1, LHX, LHY))

    open_a = lambda t: M.progress(t, grate_t[0] + 0.05, grate_t[1] + 0.25, "sine")   # noqa: E731
    sc.add("shaft", shaft_svg(), z=7, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=open_a(t) * (0.82 + 0.08 * math.sin(t * 1.7))))
    sc.add("shaft_rain", [shaft_rain_svg(s) for s in (7, 8, 9)], z=7.1, wc=0,
           motion=lambda t: Tf(alpha=open_a(t)), frame_at=lambda t: float(int(t * 11) % 3))

    flashes = [(t_open + 0.06, 0.55), (t_storm, 1.0), (t_flash2, 0.6)]

    def flash_a(t):
        return max([s * V4.flick(t - ts) for ts, s in flashes] + [0.0])
    sc.add("hatch_flash", flash_svg(), z=10, wc=0, blend="add", motion=lambda t: Tf(alpha=flash_a(t)))

    # drips from the hatch beam (as in s04)
    drop = (f'<path d="M{HX0 + 150},312 Q{HX0 + 162},336 {HX0 + 150},344 Q{HX0 + 138},336 {HX0 + 150},312 Z" '
            f'fill="{P["sea_pale"]}" stroke="{INK}" stroke-width="3"/>')
    for i in range(2):
        def dm(t, i=i):
            per = 1.3
            u = ((t + i * 0.65) % per) / per
            return Tf(0, 790 * u * u, 0, 1, 1, min(1.0, u / 0.1) * (1 - M.progress(u, 0.85, 1.0)), HX0 + 150, 320)
        sc.add(f"drip{i}", doc(drop), wc=0, z=2.7, motion=dm)     # behind the climbing captain

    # ---------------------------------------------------------------- camera
    CAM1 = Cam(1262, 676, 1940)          # once the captain is down: the whole floor, both figures
    CAM2 = Cam(1300, 672, 1910)
    CAM3 = Cam(1400, 664, 1800)          # slow push-in on the two during the plea (right edge < 2305)
    cam = M.cam_keys([(0, CAM0), (t_land - 0.25, CAM0), (t_wake + 0.5, CAM1), (t_up - 0.5, CAM2),
                      (t_plead, CAM2), (END_CALM, CAM3)], ["sine", "inout", "sine", "sine", "inout"])

    def camera(t):
        c = cam(t)
        return Cam(c.x, c.y, c.w, roll(t))
    sc.camera = camera

    # ---------------------------------------------------------------- frame effects
    sc.fx = [V4.motes_fx(lambda t: (760, 330, 1680, 1010), 24, -1.0)]

    # ---------------------------------------------------------------- sound
    D = T + 0.6
    sc.sfx("storm_wind", 0, dur=t_open + 0.4, gain_db=-17, fade_in=0.8, fade_out=0.5)
    sc.sfx("storm_wind", t_open, dur=D - t_open, gain_db=-12, fade_in=0.15, fade_out=0.8, pan=0.3)
    sc.sfx("rain", 0, dur=t_open + 0.4, gain_db=-18, fade_in=0.8, fade_out=0.5)
    sc.sfx("rain", t_open, dur=D - t_open, gain_db=-14, fade_in=0.15, fade_out=0.8, pan=0.35)
    sc.sfx("waves_storm", 0, dur=D, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("ship_creak", 0, dur=D, gain_db=-12, fade_in=0.8, fade_out=0.8)
    sc.sfx("drip", 0, dur=D, gain_db=-17, fade_in=0.8, fade_out=0.8, pan=0.4)
    sc.sfx("snore", snore_at, dur=snore_dur, gain_db=-12, fade_in=0.6, fade_out=0.3)
    sc.sfx("thud", t_open, gain_db=-9, pan=0.45)
    sc.sfx("thunder", t_open + 0.06, gain_db=-14, pan=0.35)
    sc.sfx("footsteps", t_slide0 + 0.1, dur=t_land - t_slide0 - 0.1, gain_db=-14, pan=0.5, fade_out=0.1)
    sc.sfx("thud", t_land, gain_db=-7, pan=0.5)
    sc.sfx("footsteps_run", t_walk0, dur=t_arr - t_walk0 + 0.15, gain_db=-12, pan=0.3, fade_out=0.15)
    sc.sfx("cloth", t_shake0, gain_db=-11, pan=0.1)
    sc.sfx("cloth", t_shake0 + 0.45, gain_db=-14, pan=0.1)
    sc.sfx("cloth", t_wake, gain_db=-12, pan=-0.05)
    sc.sfx("thunder", t_storm, gain_db=-6, pan=0.35)
    sc.sfx("ship_creak", t_storm - 0.05, dur=1.6, gain_db=-8, fade_in=0.05, fade_out=0.6)
    sc.sfx("cloth", t_startle, gain_db=-14, pan=-0.05)
    sc.sfx("cloth", t_stand, gain_db=-11, pan=0.0)
    sc.sfx("thunder", t_flash2, gain_db=-11, pan=0.35)

    sc.meta = dict(t_open=t_open, t_slide0=t_slide0, t_land=t_land, t_walk0=t_walk0, t_arr=t_arr, t_bend=t_bend,
                   t_shake0=t_shake0, t_wake=t_wake, t_urge=t_urge, t_storm=t_storm, t_startle=t_startle,
                   t_why=t_why, t_jworry=t_jworry, t_up=t_up, t_stand=t_stand, t_look=t_look, t_pray=t_pray,
                   t_plead=t_plead, t_sorry=t_sorry, t_live=t_live, t_pity=t_pity, t_jlook=t_jlook, n_walk=n_walk, X_START=X_START,
                   phrases=ph.items)
    return sc
