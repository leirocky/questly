"""Scene 5 — the captain wakes Jonah (Jonah 1:6).

Line 0 (N)  船长找到了约拿，把他摇醒，说：
Line 1 (C)  快醒醒！风浪这么大，你怎么还在睡觉？
Line 2 (C)  快起来，求你的神救救我们吧！也许你的神会可怜我们，让我们活下来。

The scene opens on exactly the picture s04 ends on: v1 s04's lantern-lit hold painting (V4.hold_svg, same watercolour
seed), Jonah asleep on the grain sacks breathing in time with the snore, 'Z z z', the swinging lantern, rain through
the grated hatch, and s04's final camera (V4.V0, 0.96 x V4.VIEW_W_INT painting px wide). The hold keeps rocking
gently with the ship and the storm stays audible.

As the narrator names the captain the hatch grating is flung open (cold storm light and rain pour in), his legs
appear in the opening and he climbs down the ladder, back to it, in three readable moves of three rungs each (two
alternating climb drawings, both fists gripping the rails at shoulder / chest height: a short piece of rail is drawn
over each fist with the fingers curled round it, so the grip reads even where his coat hides the painted rails).
The last move lands him on the floor in a squash, and he hurries to Jonah at once with a planted-foot walk (the
drawing follows the distance walked, the planted sole never slides; 3 frames per drawing for the first steps).
He steps up onto the end of the bed through a reaching in-between, kneels behind Jonah's head (C.captain 'wake'
recipe, drawn behind Jonah so Jonah's face stays clear) and shakes him by the shoulder ('把他摇醒', little shake marks).
He straightens up ('rise'), hops backwards off the bed (3 airborne frames of a low tuck, arms in, on a small arc
back and down), lands crouched at his standing spot (held 4 frames, squash and a soft thud) and only then stands.
Jonah props himself up on his elbows two frames into the captain's landing, once the captain's head has left the
space above the pillow (a 3-frame in-between), then sits up rubbing his eye one frame after the captain stands
(on '说：').
Line 1: the captain urges him ('快醒醒！'); in the pause before '风浪这么大' thunder cracks through the hatch and the
ship lurches — he clutches his cap and Jonah turns round with a start; then he spreads his palms
('你怎么还在睡觉？').
Line 2: he points up through the hatch to the deck ('快起来' — Jonah gets up: a 3-frame half-risen in-between with a
hand pushing on the sacks, then his feet), looks up ('求你的神'), raises both hands to heaven ('救救我们吧' — a second
flash), then clasps his hands and pleads (a nod on '可怜', a lean-in on '让我们活下来'); Jonah lowers his eyes, sorry
(he knows the storm is his doing), then tilts his head right back to the hatch as a faint far flash and a soft rumble
come from above, and the camera tilts up with his gaze — calm for the last 1.2 s.
Camera: s04's framing while the captain climbs, then a slow drift (< 80 px/s) to a closer two-shot for line 1, up a
little so the hatch is in frame while he points, a push-in during the plea and a gentle tilt up to the hatch at the end.
Every pose change is a hard cut sold by a small squash-and-hop (no crossfades between poses); every main pose is
held for at least half a second; all key times come from the narration (sub-phrases are timed from the punctuation
pauses in the voice files, with a proportional fallback); the hard cuts of the fast sequences sit on the frame grid.

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
RUNGS = [300 + 812 * k / 9 for k in range(10)]          # rung k centre line (0 = top end of the rails, 9 = floor)


def lad_cx(y):
    """Centre between the ladder rails at height y."""
    return (HX0 + 50 + HX1 - 60) / 2 + LAD_K * (y - 300)


# where things stand
KNEEL = (JX + 234 * JS, JY)          # the captain kneeling on the bed behind Jonah's head (C.captain 'wake' recipe)
X_ARR = 1622                         # his last walk contact on the floor, just past the end of the bed
CAP_X = 1600                         # his standing spot while he talks (left of the cold light shaft)
J_WAKE_X = 1262                      # Jonah sitting up (facing left, legs along the bed)
J_WAKE_IB_X = 1125                   # Jonah propped up on his hands (in-between of sitting up): head halfway
#                                      between the pillow and the sitting head
J_SIT_X = 1212                       # Jonah sitting, turned toward the captain
J_STAND_X = 1274                     # Jonah on his feet in front of the bed (clear of the swinging lantern)
J_IB_X = (J_SIT_X + J_STAND_X) / 2   # Jonah half-risen (in-between of getting up)

# the captain's walk: CAP_N drawings per step, two steps per cycle (see cap_walk_pose)
CAP_A = 58
CAP_N = 4
CAP_DD = 2 * CAP_A * JS / CAP_N      # stage px the anchor advances per drawing (planted sole stays put)
FR = 1 / 30


def snap(t):
    """Put a hard cut halfway between two frames, so it lands on an exact frame whatever the float noise."""
    return (round(t / FR) - 0.5) * FR


def trapezoid(a=0.25):
    """Ease with a constant-speed middle: speed ramps up over the first ``a`` of the move and down over the last
    ``a`` (peak speed 1/(1-a) x the average, vs pi/2 x for 'sine') — for long camera drifts."""
    vm = 1 / (1 - a)

    def f(u):
        if u <= a:
            return vm * u * u / (2 * a)
        if u >= 1 - a:
            return 1 - vm * (1 - u) ** 2 / (2 * a)
        return vm * (u - a / 2)
    return f


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


# ------------------------------------------------------------- the climb (back to the ladder, fists on the rails)

SLIDE_REF_Y = 700.0                  # the climb drawings are made with their anchor here, then moved along the ladder
LAD_TH = math.atan(LAD_K)
SLIDE_ROT = -math.degrees(LAD_TH)    # his body leans with the ladder (top toward the left)
RAIL_OFF = 95 * math.cos(LAD_TH)     # the rails' distance from the ladder's centre line (stage px)
RAIL_HALF = RAIL_OFF / JS            # ... in figure px
SLIDE_X0 = lad_cx(SLIDE_REF_Y)
GRIP_PUSH = 3.0                      # fist centres this far (figure px) outside the rail centre lines
RAIL_PIECE = 25                      # half-length (stage px) of the rail piece drawn over each fist


def fist_centre(ps, i, m=C._CAPTAIN_M):
    """Centre of the fist of arm i (0 far, 1 near) of an ('ik', 'abs', ...) arm, in anchor coordinates (figure px,
    x toward ``facing``, y up negative) — computed exactly as C._figure places it."""
    t = ps["t"]
    u = C._rot((0, -1), t)
    f = C._rot((1, 0), t)
    G = 4 + m["th"] + m["sh"] + C._sole_off(0, m["fl"]) - ps["drop"]
    sx = m["sw"] if i == 0 else -m["sw"]
    uy = m["T"] - m["sdrop"]
    S_ = (f[0] * sx + u[0] * uy, f[1] * sx + u[1] * uy)
    spec = ps["arms"][i]
    E, W_ = C._ik(S_, (spec[2], G + spec[3]), m["ua"] * ps["reach"], m["fa"] * ps["reach"], spec[4])
    d = C._nrm(C._sub(W_, E))
    c = C._add(W_, C._mul(d, 0.45 * m["hr"]))
    return c[0], c[1] - G


def climb_pose(far_h, near_h, far_lift, near_lift, bends=(1, 1)):
    """Back to the ladder (facing -1, so the far arm grips the left rail and the near arm the right one), the fist
    centres at far_h / near_h figure px above the feet, just outside the rail lines, elbows bent outward; the foot on
    the raised side one rung up (lift in figure px)."""
    def mk(tg):
        return C._P(t=-2, h=12, legs=(("ik", 24 if far_lift else 22, 1, far_lift),
                                      ("ik", -24 if near_lift else -22, 1, near_lift)),
                    arms=(("ik", "abs", tg[0][0], tg[0][1], bends[0]), ("ik", "abs", tg[1][0], tg[1][1], bends[1])),
                    hands=("fist", "fist"))
    want = ((RAIL_HALF + GRIP_PUSH, -far_h), (-RAIL_HALF - GRIP_PUSH, -near_h))
    tg = [list(want[0]), list(want[1])]
    for _ in range(5):                       # aim the fist centres (not the wrists) at the rails and heights
        ps = mk(tg)
        for i in (0, 1):
            c = fist_centre(ps, i)
            tg[i][0] += want[i][0] - c[0]
            tg[i][1] += want[i][1] - c[1]
    return mk(tg)


def rail_lift(dx):
    """Ankle lift (figure px) that puts a foot dx figure px toward 'facing' (-1) one rung above the planted one."""
    return (RUNGS[1] - RUNGS[0] + dx * JS * math.sin(LAD_TH)) / (JS * math.cos(LAD_TH))


def grip_svg(ps, sides=(0, 1)):
    """A short piece of the ladder rail over each fist in ``sides`` (same rail as the painting: 32 px ink, 22 px light
    wood) with the fingers curled round its front, in the climb drawing's own (untilted) coordinates."""
    skin = C._captain_design()["skin"]
    out = ""
    for i in sides:
        _, fy = fist_centre(ps, i)
        xr = SLIDE_X0 + (-RAIL_OFF if i == 0 else RAIL_OFF)
        yc = SLIDE_REF_Y + fy * JS
        out += (f'<path d="M{xr:.1f},{yc - RAIL_PIECE:.1f} L{xr:.1f},{yc + RAIL_PIECE:.1f}" stroke="{INK}" '
                f'stroke-width="32"/>'
                f'<path d="M{xr:.1f},{yc - RAIL_PIECE - 1:.1f} L{xr:.1f},{yc + RAIL_PIECE + 1:.1f}" '
                f'stroke="{P["wood_light"]}" stroke-width="22"/>')
        side = -1 if i == 0 else 1           # the outer side of this rail (the knuckles bulge out there)
        for k, dy in enumerate((-12.5, 0.0, 12.5)):
            w_ = 40 - 3 * abs(k - 1)
            x0 = xr - w_ / 2 + side * 2
            out += (f'<rect x="{x0:.1f}" y="{yc + dy - 7:.1f}" width="{w_:.1f}" height="14" rx="7" fill="{skin}" '
                    f'stroke="{INK}" stroke-width="3.6"/>')
    return S.g(out, filter="wobble-fine")


def cap_poses():
    lf = rail_lift(24)                      # far (left) foot one rung up
    ln = rail_lift(-24)                     # near (right) foot one rung up
    return {
        # climbing down the ladder, back to it (the layer is tilted by SLIDE_ROT so he lies along the rails).
        # Fist heights sit between rungs (so the rail pieces never cover a rung end), about shoulder and chest high.
        "climb_a": climb_pose(245, 179, lf, 0),
        "climb_b": climb_pose(197, 230, 0, ln),
        # landing at the foot of the ladder / at his spot after hopping off the bed: crouched, arms out for balance
        "land": C._P(t=12, h=-4, drop=40, legs=(("ik", 34, 1), ("ik", -30, 1)),
                     arms=(("fk", 58, 96), ("fk", -46, -20)), hands=("open", "open")),
        # landing at his spot after hopping backwards off the bed: crouched, arms back and out (clear of Jonah)
        "land_bed": C._P(t=16, h=-6, drop=44, legs=(("ik", 32, 1), ("ik", -30, 1)),
                         arms=(("fk", 4, 30), ("fk", -70, -40)), hands=("open", "open")),
        # stepping up onto the bed end, reaching for Jonah (in-between of the hop into the kneel)
        "reach": C._P(t=30, h=-10, drop=30, legs=(("ik", 34, 1), ("ik", -34, 1, 18)),
                      arms=(("fk", 62, 84), ("fk", 46, 76)), hands=("open", "open")),
        # straightening up again after the shake (still kneeling on the bed, about to hop off)
        "rise": C._P(t=14, h=-6, drop=34, legs=(("ik", 52, 1), ("ik", -24, 1)),
                     arms=(("fk", 24, 50), ("fk", 18, 44)), hands=("open", "open")),
        # airborne, hopping backwards off the bed: a low tuck (pelvis dropped, soles lifted off the anchor), arms
        # bent in front at chest height
        "tuck": C._P(t=12, h=-6, drop=60, legs=(("ik", 40, 1, 40), ("ik", -18, 1, 26)),
                     arms=(("fk", 34, 78), ("fk", 14, 56)), hands=("open", "open")),
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
        # waking (3-frame in-between of sitting up): leaning right back, propped on his hands on the sacks behind him
        "wake_ib": C._P(t=-50, h=-10, legs=(("ik", 108, 1), ("ik", 116, 1)),
                        arms=(("ik", "abs", -96, -4, -1), ("ik", "abs", -66, -4, -1)), hands=("open", "open"),
                        **C._SEATED),
        # getting up off the sacks (3-frame in-between): crouched, both sandals on the floor, leaning forward, the
        # near hand still pushing on the sacks behind him, the far arm forward for balance
        "rise_ib": C._P(t=14, h=-4, drop=78, reach=1.12, legs=(("ik", 36, 1), ("ik", -34, 1)),
                        arms=(("fk", 34, 58), ("ik", "abs", -62, -62, 1)), hands=("open", "open")),
        # head tipped right back, eyes up to the hatch and the storm above (he knows it is his doing)
        "stand_up": C._P(t=-3, h=-26, arms=(("fk", 12, 8), ("fk", -6, -2)), look=(0.05, -0.13)),
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


SHAFT_TOP = BEAM_BOT + 16            # the cold light starts below the beam (blurred), so the beam stays dark wood


def shaft_svg():
    """Cold storm light falling through the open hatch onto the floor."""
    defs = S.lin_grad("cshaft", [(0, "#d6e4f2", 0.5), (0.55, "#b9cde0", 0.2), (1, "#b9cde0", 0.0)])
    d = (f"M{HX0 + 10},{SHAFT_TOP} L{HX1 - 10},{SHAFT_TOP} L{HX1 + 190},{FLOOR_Y + 40} "
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
        y = r.uniform(BEAM_BOT + 14, FLOOR_Y - 60)
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
    """Lightning seen through the hatch: the sky in the opening lights up, a soft radial bloom round the hatch fading
    to nothing at its rim, and a cold glow down the light shaft (all added onto the frame)."""
    cx, cy = (HX0 + HX1) / 2, (HY0 + OPEN_Y1) / 2
    defs = S.rad_grad("hflash", [(0, "#d4def4", 0.55), (0.45, "#c3d1ee", 0.3), (0.8, "#b8c8ea", 0.08),
                                 (1, "#b8c8ea", 0.0)])
    body = (f'<path d="M{HX0 + 20},{SHAFT_TOP} L{HX1 - 20},{SHAFT_TOP} L{HX1 + 220},{FLOOR_Y} '
            f'L{HX0 + 20},{FLOOR_Y} Z" fill="#a9bde4" opacity="0.42" filter="url(#blur-lg)"/>'
            f'<rect x="{HX0 + 3}" y="{HY0 + 3}" width="{HX1 - HX0 - 6}" height="{OPEN_Y1 - HY0 - 3}" fill="#dfe8f8" '
            f'opacity="0.7"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="420" ry="260" fill="url(#hflash)" filter="url(#blur-lg)"/>')
    return doc(body, defs)


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
    t_slide0 = t_open + 0.2                                     # his legs appear in the opening
    # the climb: an entry move into the opening, then three moves of three rungs each, the last one onto the floor
    cy = [120.0, RUNGS[1], RUNGS[4], RUNGS[7], FLOOR_Y]        # anchor (feet) heights (last hold: face clear
    #                                                             of the beam; the final 2-rung drop lands him)
    CL_MOVE = 0.13                                              # each drop takes 4 frames (ease out) ...
    CL_T = [t_slide0, t_slide0 + 0.24, t_slide0 + 0.51, t_slide0 + 0.78]   # ... and holds 4-5 frames
    t_land = snap(CL_T[-1] + CL_MOVE)                           # lands at the foot of the ladder (squash)
    t_walk0 = t_land + 3 * FR                                   # first walk drawing, straight after the squash
    n_walk = max(4, round((lad_cx(1112) - X_ARR) / CAP_DD))
    X_START = X_ARR + n_walk * CAP_DD                           # where he lands (centred on the ladder foot)
    tw = [t_walk0]                                              # walk drawing i shown from tw[i]
    for i in range(n_walk):
        tw.append(tw[-1] + (3 if i < 4 else 2) * FR)            # 3 frames per drawing for the first steps, then 2
    t_arr = tw[n_walk]                                          # last contact
    t_ib = t_arr + 2 * FR                                       # steps up onto the bed end, reaching ...
    t_bend = t_ib + 4 * FR                                      # ... and kneels behind Jonah's head
    t_shake0 = max(t_bend + 0.1, t_shake_say)
    t_jump = snap(max(t_shake0 + 0.62 + 0.25, t_say - 0.05))   # hops backwards off the bed (on "说：")
    t_rise = snap(t_jump - 0.25)                                # straightens up after the shake
    t_shake1 = t_rise
    t_cland = t_jump + 3 * FR                                   # 3 airborne frames, then lands at his spot ...
    t_cstand = t_cland + 4 * FR                                 # ... holds the crouch 4 frames, then stands
    t_wake = t_jump + 5 * FR                                    # Jonah props himself up once the captain's head
    #                                                             is clear (3-frame in-between) ...
    t_wake2 = t_wake + 3 * FR                                   # ... and sits up, a frame after the captain stands
    # line 1
    t_urge = ph.start("快醒醒", c_start) - 0.08
    t_storm = max(ph.end("快醒醒", c_start + 0.8) + 0.05,       # thunder in the pause after "快醒醒！"
                  ph.start("风浪", c_start + 0.3 * (lc[0].end - c_start)) - 0.4)
    t_cworry = t_storm + 0.05
    t_startle = t_storm + 0.14                                  # Jonah turns round with a start
    t_why = ph.start("怎么还在睡", t_storm + 1.0) - 0.06
    t_jworry = t_why + 0.75
    # line 2
    lq = lc[-1]
    t_up = ph.start("快起来", lq.start) - 0.06
    t_stand = snap(t_up + 0.4)                                  # Jonah gets up: half-risen in-between ...
    t_stand2 = t_stand + 3 * FR                                 # ... then on his feet
    t_look = ph.start("求你的神", t_up + 0.9)
    t_pray = ph.inner("求你的神", "救救", t_look + 1.05) - 0.02
    t_plead = ph.start("也许", lq.start + 0.45 * (lq.end - lq.start)) - 0.06
    t_sorry = t_plead + 0.85
    t_live = ph.start("让我们活下来", t_plead + 2.6)
    t_pity = ph.inner("也许", "可怜", t_plead + 1.4)             # a pleading nod on "可怜我们"
    t_jlook = t_live + 0.35                                     # Jonah looks up toward the storm above
    t_flash2 = t_pray + 0.08
    t_flash3 = t_jlook + 0.1                                    # a faint far flash in the hatch as he looks up
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

    # ---------------------------------------------------------------- captain: climb, land + walk, main poses
    CP = cap_poses()
    cap_layers_z = 2.85                    # behind Jonah (he kneels on the bed behind Jonah's head)

    def climb_state(t):
        """(drawing index, anchor y) on the ladder: the drawing alternates at every move, the body drops quickly
        (ease out) and holds."""
        if t < CL_T[0]:
            return 0, cy[0]
        k = max(i for i, s in enumerate(CL_T) if t >= s)
        u = M.progress(t, CL_T[k], CL_T[k] + CL_MOVE, "out")
        return (k + 1) % 2, M.lerp(cy[k], cy[k + 1], u)

    def fist_stage_y(ps, i, y):
        """Stage y of fist i of a climb drawing whose anchor is at height y (the layer is tilted by SLIDE_ROT)."""
        fx, fy = fist_centre(ps, i)
        lx, ly = -fx * JS, fy * JS                         # facing -1: forward = screen left
        return y + lx * math.sin(math.radians(SLIDE_ROT)) + ly * math.cos(math.radians(SLIDE_ROT))

    climb_keys = ("climb_a", "climb_b")
    grips_ok_y = OPEN_Y1 + RAIL_PIECE + 6                  # a rail piece never shows inside the hatch opening

    def climb_frame(t):
        k, y = climb_state(t)
        ps = CP[climb_keys[k]]
        grip = [fist_stage_y(ps, i, y) >= grips_ok_y for i in (0, 1)]
        return float(4 * k + grip[0] + 2 * grip[1])

    def climb_m(t):
        if not (t_slide0 - 0.05 <= t < t_land):
            return Tf(alpha=0.0)
        y = climb_state(t)[1]
        return Tf(dx=lad_cx(y) - SLIDE_X0, dy=y - SLIDE_REF_Y, rot=SLIDE_ROT, px=SLIDE_X0, py=SLIDE_REF_Y)
    climb_frames = []
    for key in climb_keys:
        fig = cap_fig(SLIDE_X0, SLIDE_REF_Y, CP[key], expr="worried", label=key, shadow=False)
        climb_frames += [doc(fig + grip_svg(CP[key], sides)) for sides in ((), (0,), (1,), (0, 1))]
    sc.add("cap_climb", climb_frames, z=cap_layers_z, motion=climb_m, frame_at=climb_frame)

    # landing crouch + the planted-foot walk to the bed (+ the step-in in-between), drawn at X_START
    walk_frames = [doc(cap_fig(X_START, FLOOR_Y, CP["land"], expr="worried", label="land"))]
    for k in range(2 * CAP_N):
        walk_frames.append(doc(cap_fig(X_START, FLOOR_Y, cap_walk_pose(k), expr="worried", label=f"walk{k}")))
    # in-between: stepping up onto the end of the bed and reaching for Jonah (a short hop arc into the kneel)
    walk_frames.append(doc(cap_fig(X_START, FLOOR_Y, CP["reach"], expr="worried", label="reach", shadow=False)))
    N_IB = 2 * CAP_N + 1
    ib_from = (X_ARR - 30, FLOOR_Y)
    ib_to = (KNEEL[0] + 40, KNEEL[1] + 12)

    def walk_i(t):
        """Index of the walk drawing on screen (0 .. n_walk), or None before the walk / after the last contact."""
        if t < t_walk0 or t >= t_ib:
            return None
        return max(i for i in range(n_walk + 1) if t >= tw[i])

    def walk_idx(t):
        if t < t_walk0:
            return 0
        i = walk_i(t)
        if i is None:
            return N_IB
        return 1 + (i - n_walk) % (2 * CAP_N)         # drawing n_walk is the contact with the far foot forward

    def walk_xy(t):
        if t < t_walk0:
            return X_START, FLOOR_Y
        i = walk_i(t)
        if i is not None:
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

    # kneel + shake, rise, the hop off the bed (tuck on an arc), landing crouch, then the talking poses
    kx, ky = KNEEL
    JUMP_FROM = (kx + 8, ky)               # tuck drawing's lowest point at take-off (feet on the bed top) ...
    JUMP_TO = (CAP_X, FLOOR_Y)             # ... and where the feet come down
    JUMP_H = 60                            # parabola bulge: the anchor rises ~15 px above the bed top; the lifted
    #                                        soles clear it by ~60-85 px (a small hop back and down)

    def jump_xy(t):
        u = min(1.0, max(0.0, (t - t_jump) / (t_cland - t_jump)))
        return (M.lerp(JUMP_FROM[0], JUMP_TO[0], u),
                M.lerp(JUMP_FROM[1], JUMP_TO[1], u) - 4 * JUMP_H * u * (1 - u))

    main = [
        (t_bend, C.captain(kx, ky, JS, -1, pose="wake", expr="worried")),
        (t_rise, cap_fig(kx, ky, CP["rise"], expr="worried", label="rise", shadow=False)),
        (t_jump, cap_fig(kx, ky, CP["tuck"], expr="worried", label="tuck", shadow=False)),
        (t_cland, cap_fig(CAP_X, FLOOR_Y, CP["land_bed"], expr="worried", label="land_bed")),
        (t_cstand, cap_fig(CAP_X, FLOOR_Y, CP["stand"], expr="worried", label="stand")),
        (t_urge, cap_fig(CAP_X, FLOOR_Y, CP["urge"], expr="shout", label="urge")),
        (t_cworry, cap_fig(CAP_X, FLOOR_Y, CP["worried"], expr="scared", label="worried")),
        (t_why, cap_fig(CAP_X, FLOOR_Y, CP["why"], expr="worried", label="why")),
        (t_up, cap_fig(CAP_X, FLOOR_Y, CP["up"], expr="shout", label="up")),
        (t_look, cap_fig(CAP_X, FLOOR_Y, CP["uplook"], expr="worried", label="uplook")),
        (t_pray, cap_fig(CAP_X, FLOOR_Y, CP["pray"], expr="worried", label="pray")),
        (t_plead, cap_fig(CAP_X, FLOOR_Y, CP["plead"], expr="worried", label="plead")),
    ]
    gestures = [k[0] for k in main[5:]]

    def cap_m(t):
        if t < t_bend:
            return Tf(alpha=0.0)
        sx, sy = pop(t, [t_bend, t_rise, t_cstand] + gestures, 0.07)
        lx, ly = pop(t, [t_cland], 0.13)                     # the landing squash
        sx, sy = sx * lx, sy * ly
        br = 1 + 0.011 * math.sin(2 * math.pi * (t / 3.1 + 0.3))
        if t < t_rise:
            dx = 7 * math.sin(2 * math.pi * 4.6 * (t - t_shake0)) if t_shake0 <= t < t_shake1 else 0.0
            return Tf(dx=dx, sx=sx, sy=sy * br, px=kx, py=ky)
        if t < t_jump:
            return Tf(sx=sx, sy=sy * br, px=kx, py=ky)
        if t < t_cland:                                      # airborne: the tuck drawing rides the arc
            x, y = jump_xy(t)
            return Tf(dx=x - JUMP_FROM[0], dy=y - JUMP_FROM[1], rot=4.0, px=kx, py=ky - 200)
        # at his spot: little hops at each gesture; a lean-in on "让我们活下来"
        dy = -8 * sum(bump(t, s) for s in gestures)
        rot = -2.2 * M.progress(t, t_live - 0.1, t_live + 0.5, "sine")       # held to the end (calm last frames)
        if t_pity <= t <= t_pity + 0.7:
            rot -= 1.8 * math.sin(math.pi * (t - t_pity) / 0.7)
        return Tf(dy=dy, rot=rot, sx=sx, sy=sy * (br if t >= t_cstand else 1.0), px=CAP_X, py=FLOOR_Y)
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
        (t_wake, jonah_fig(J_WAKE_IB_X, JY, JP["wake_ib"], -1, expr="sleepy", label="wake_ib")),
        (t_wake2, C.jonah(J_WAKE_X, JY, JS, -1, pose="wake", expr="sleepy")),
        (t_startle, C.jonah(J_SIT_X, JY, JS, 1, pose="sit", expr="surprised")),
        (t_jworry, C.jonah(J_SIT_X, JY, JS, 1, pose="sit", expr="worried")),
    ]

    def jseat_m(t):
        if t < t_wake or t >= t_stand:
            return Tf(alpha=0.0)
        px = J_WAKE_IB_X if t < t_wake2 else J_WAKE_X if t < t_startle else J_SIT_X
        sx, sy = pop(t, [t_wake, t_wake2, t_startle, t_jworry], 0.09)
        sy *= 1 + 0.009 * math.sin(2 * math.pi * (t / 3.3 + 0.1))
        dy = -14 * bump(t, t_wake2) - 20 * bump(t, t_startle, 0.09)
        rot = 0.0
        if t_wake2 <= t < t_startle:      # sleepy sway while rubbing the eye
            rot = 2.2 * math.sin(2 * math.pi * (t - t_wake2) / 2.6) * M.progress(t, t_wake2 + 0.2, t_wake2 + 0.8)
        # paper cut-out turn round the facing flip
        k = 1.0
        u = abs(t - t_startle) / 0.09
        if u < 1:
            k = 1 - 0.7 * (1 - u)
        return Tf(0, dy, rot, sx * k, sy, 1.0, px, JY)
    flipbook(sc, "jonah_seated", [(k[0], doc(k[1])) for k in seated], z=3.1, motion=jseat_m)

    shadow = C.ground_shadow(J_STAND_X, FLOOR_Y + 2, JS, width=120)
    standing = [
        (t_stand, C.ground_shadow(J_IB_X, FLOOR_Y + 2, JS, width=150)
         + jonah_fig(J_IB_X, FLOOR_Y, JP["rise_ib"], 1, expr="worried", label="rise")),
        (t_stand2, shadow + C.jonah(J_STAND_X, FLOOR_Y, JS, 1, pose="stand", expr="worried")),
        (t_sorry, shadow + jonah_fig(J_STAND_X, FLOOR_Y, JP["stand_sorry"], 1, expr="sorry", label="sorry")),
        (t_jlook, shadow + jonah_fig(J_STAND_X, FLOOR_Y, JP["stand_up"], 1, expr="worried", label="lookup")),
    ]

    def jstand_m(t):
        if t < t_stand:
            return Tf(alpha=0.0)
        sx, sy = pop(t, [t_stand, t_stand2, t_sorry, t_jlook], 0.09)
        sy *= 1 + 0.010 * math.sin(2 * math.pi * (t / 3.4 + 0.6))
        u = M.progress(t, t_stand2, t_stand2 + 0.2, "linear")
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
    sc.add_dynamic("cut_post", lambda t: cut_post.get() if t_slide0 <= t < t_walk0 + 0.4 else None, z=6.1)

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

    flashes = [(t_open + 0.06, 0.55), (t_storm, 1.0), (t_flash2, 0.6), (t_flash3, 0.5)]

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
    # (centre speeds stay below ~75 stage px/s; viewport inside the painting: x 2*34..W-2*34, y 34..H-34)
    CAM_L1 = Cam(1420, 660, 1650)        # the captain is down: a closer two-shot for line 1
    CAM_PT = Cam(1420, 622, 1650)        # pointing up to the deck: up a little so the hatch is in frame
    CAM_PL = Cam(1440, 626, 1500)        # pushed in on the two during the plea
    CAM_END = Cam(1440, 596, 1540)       # tilting up with Jonah's gaze: the hatch above both heads
    t_c0 = t_slide0 + 0.1
    t_c1 = max(t_c0 + 5.2, t_cstand + 1.0)
    t_p0 = lc[0].end + 0.1
    t_p1 = max(t_p0 + 1.1, t_up + 0.6)
    t_e0 = t_jlook - 0.12
    cam = M.cam_keys([(0, CAM0), (t_c0, CAM0), (t_c1, CAM_L1), (t_p0, CAM_L1), (t_p1, CAM_PT),
                      (t_plead, CAM_PT), (t_e0, CAM_PL), (END_CALM, CAM_END)],
                     ["sine", trapezoid(0.25), "sine", "sine", "sine", "sine", "sine"])

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
    for tk in CL_T[1:]:                                         # a wooden knock as his sandals hit the rungs
        sc.sfx("thud", tk + 0.08, gain_db=-17, pan=0.5)
    sc.sfx("thud", t_land, gain_db=-7, pan=0.5)
    sc.sfx("footsteps_run", t_walk0, dur=t_arr - t_walk0 + 0.15, gain_db=-12, pan=0.3, fade_out=0.15)
    sc.sfx("cloth", t_shake0, gain_db=-11, pan=0.1)
    sc.sfx("cloth", t_shake0 + 0.45, gain_db=-14, pan=0.1)
    sc.sfx("thud", t_cland, gain_db=-13, pan=0.2)               # a soft landing off the bed
    sc.sfx("cloth", t_wake, gain_db=-12, pan=-0.05)
    sc.sfx("thunder", t_storm, gain_db=-6, pan=0.35)
    sc.sfx("ship_creak", t_storm - 0.05, dur=1.6, gain_db=-8, fade_in=0.05, fade_out=0.6)
    sc.sfx("cloth", t_startle, gain_db=-14, pan=-0.05)
    sc.sfx("cloth", t_stand2, gain_db=-11, pan=0.0)
    sc.sfx("thunder", t_flash2, gain_db=-11, pan=0.35)
    sc.sfx("thunder", t_flash3, dur=max(0.8, min(2.6, T - t_flash3)), gain_db=-16, pan=0.35, fade_out=1.2)

    sc.meta = dict(t_open=t_open, t_slide0=t_slide0, t_land=t_land, t_walk0=t_walk0, t_arr=t_arr, t_bend=t_bend,
                   t_shake0=t_shake0, t_rise=t_rise, t_jump=t_jump, t_cland=t_cland, t_cstand=t_cstand,
                   t_wake=t_wake, t_wake2=t_wake2, t_urge=t_urge, t_storm=t_storm, t_startle=t_startle,
                   t_why=t_why, t_jworry=t_jworry, t_up=t_up, t_stand=t_stand, t_stand2=t_stand2, t_look=t_look,
                   t_pray=t_pray, t_plead=t_plead, t_sorry=t_sorry, t_live=t_live, t_pity=t_pity, t_jlook=t_jlook,
                   t_flash3=t_flash3, CL_T=CL_T, n_walk=n_walk, X_START=X_START, cam_keys=(t_c0, t_c1, t_p0, t_p1,
                                                                                        t_plead, t_e0, END_CALM),
                   phrases=ph.items)
    return sc
