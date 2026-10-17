"""Scene 9 (v2) — the sailors throw Jonah into the sea; at once the sea is calm; they fear the LORD, offer a
sacrifice and make vows (Jonah 1:15-16).

Two shots joined by a push-in cross-dissolve in the pause after line 1:

  A (lines 0-1)  the approved v1 wide shot (art/scenes_v1/s06_fish.py, surface half): the ship (bow LEFT, torn
                 striped sail, sailors 0-3 and the captain) rocking in the storm.
  B (line 2)     on the calm, sunlit deck (the deck of s06/s07 seen from on board: bulwark with painted shields,
                 mast and torn sail): the crew kneel round a small bronze brazier, the offering flame sends its
                 smoke up into the sunlight, they lift their hands to make vows.

Narration (every key time comes from the chunks; a phrase inside a chunk is placed by its characters and snapped
to a pause in the voice take, see Cues):
  line 0 '于是，他们把约拿抬起来，扔进了大海。'
         '他们'     the two lifters crouch either side of Jonah (head bowed, sorry) and take hold of him;
         '抬起来'   they hoist him overhead ('carried' on their hands; the cut is sold by a squash-hop and he rises
                    onto their hands); '扔进了' heave (dip, push) and launch: he flies over the stern in an arc;
         '大海'     splash crown, drops, ripples, a burst of bubbles; the crew watch, worried.
  line 1 '一下子，'  the rain stops at once, the storm banks slide away, the sky turns blue;
         '海就平静了' the storm crests sink and the sea flattens, a golden sunbeam falls on the water, the crew
                    (pose cut) pray and point in awe; the splash rings spread out on the calm water;
         '风停了，'  the curly wind marks blowing across the sky fade away and the whipping pennant goes slack,
                    gulls glide in;
         '浪也静了。' the last swell settles, the ship lies still, glints sparkle on the water.
  pause          slow push-in on the ship, cross-dissolve to the deck.
  line 2 '水手们看见了，' standing on the calm deck in the sunshine they gaze at the sea in wonder (one points to
                    the light, one lifts his hands);
         '心里对耶和华又敬又怕。' one after another they kneel and bow their heads, palms together;
         '他们向耶和华献上祭物，' the captain lifts a bowl of grain over the brazier; at '献上' he pours it in:
                    the flame flares, sparks rise and a big curl of smoke climbs into the sunbeams; the others
                    raise their heads to watch it;
         '还许下了诺言。' they all lift their hands to the sky (vows); warm sparkles in the light (God is shown
                    only as light).
  The scene ends on a held, calm frame (the raised hands, the flame, the smoke in the sunlight).

Pose changes are hard cuts (never crossfaded) sold by squash-and-hops; every pose is held >= 0.5 s. Stage 2112 x
1188; the camera stays inside the painted area (both shots are painted over the whole stage).
"""
import math
import random
from dataclasses import replace

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s05_lots as V5
from art.scenes_v1 import s06_fish as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.paths import BUILD
from engine.scene import Scene

W, H = 2112, 1188
HORIZON, WL = V.HORIZON, V.WL          # 690, 880 (v1 wide shot)
SX, SS, SF = V.SX, V.SS, V.SF          # ship anchor x, scale, facing (-1: bow left)
DECK = V.DECK
SPLASH = V.SPLASH
JS = V.JS

# ---- shot A cast on the deck line (x, variant); all face the stern (+1) unless noted
S3_X, CAPT_X, S1_X, L0_X, JON_X, L2_X = 545, 640, 725, 805, 893, 985
HAND_Y = DECK - 316.5 * SS                                   # 'lift' hand line
JCAR_C = ((L0_X + L2_X) / 2, HAND_Y + 6 * SS - 39.5 * JS)      # carried Jonah: bbox centre
JCAR = (JCAR_C[0] - 20 * JS, HAND_Y + 6 * SS)                  # ...and anchor (facing -1, head to the stern)
JAIR_ROT = V.JAIR_ROT
JAIR_C = JCAR_C
JAIR = (JAIR_C[0] + 1 * JS, JAIR_C[1] + 135.5 * JS)          # 'fall' anchor
PEN = PR.local_to_stage(SX, WL, SS, SF, -10, -930)           # masthead (pennant root)

# ---- shot B: the deck seen from on board
B_HOR, B_RAIL, B_DBACK = 560, 780, 872
SUN_B = (1560, 422)
MAST_B = 480
ALT = (1415, 1004)                     # brazier: foot line centre
RIM_Y = ALT[1] - 140                   # bowl rim
FLAME_B = (ALT[0], RIM_Y - 6)          # flame base
SMOKE_O = (ALT[0] + 2, RIM_Y - 70)     # smoke origin (the flame tip)
B_CAPT = (1190, 1034, 1.02)
B_S2 = (950, 1040, 1.04)               # variant 2, front row
B_S3 = (690, 1046, 1.06)               # variant 3 (ginger beard), front row left
B_S0 = (1075, 954, 0.88)               # variant 0, back row
B_S1 = (820, 952, 0.88)                # variant 1, back row
GULL_B = (318, B_RAIL - 26)            # gull perched on the rail

PUNCT = "，。！？：；、,.!?:;"


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


# ============================================================================ narration timing


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

    def at(self, phrase, default, snap=True):
        for ln in self.ctx.lines:
            spans = [(c.text, c.start, c.end) for c in ln.chunks] or [(ln.text, ln.start, ln.end)]
            for text, c0, c1 in spans:
                k = text.find(phrase)
                if k < 0:
                    continue
                if not any(ch not in PUNCT for ch in text[:k]):
                    return c0
                est = c0 + (c1 - c0) * _nchar(text[:k]) / _nchar(text)
                best, score = None, -1.0
                for a, b in (self.dips if snap else ()):
                    if c0 < a and b < c1 and abs(b - est) < 0.45:
                        sc_ = (b - a) - 0.15 * abs(b - est)
                        if sc_ > score:
                            best, score = b, sc_
                return best if best is not None else est
        return default


def hermite(keys):
    """Smooth path through (t, value, slope) keys with continuous velocity (cubic Hermite)."""
    keys = sorted(keys)

    def f(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, v0, s0), (t1, v1, s1) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                h = t1 - t0
                u = (t - t0) / h
                h00 = 2 * u ** 3 - 3 * u ** 2 + 1
                h10 = u ** 3 - 2 * u ** 2 + u
                h01 = -2 * u ** 3 + 3 * u ** 2
                h11 = u ** 3 - u ** 2
                return h00 * v0 + h10 * h * s0 + h01 * v1 + h11 * h * s1
        return keys[-1][1]
    return f


def bump(t, ts, w=0.07):
    """0..1..0 triangle centred just after ts (a 3-4 frame hop that sells a pose cut)."""
    return max(0.0, 1 - abs(t - ts - 0.03) / w)


def steps(keys):
    """Hard-cut flipbook index: keys = [(t, idx), ...]."""
    keys = sorted(keys)

    def f(t):
        idx = keys[0][1]
        for tk, i in keys:
            if t >= tk:
                idx = i
        return float(idx)
    return f


# ============================================================================ shot A painting


A_CAST = [("s3", S3_X, 3), ("capt", CAPT_X, None), ("s1", S1_X, 1), ("l0", L0_X, 0), ("l2", L2_X, 2)]
A_STAGES = [
    # 0 before the lift: the lifters stand either side of Jonah; the bow sailor still prays (s08)
    dict(s3=("pray", "scared", 1), capt=("worried", None, 1), s1=("stand", "worried", 1),
         l0=("stand", "worried", 1), l2=("stand", "worried", -1)),
    # 1 '他们' they crouch and take hold of him
    dict(s3=("pray", "scared", 1), capt=("worried", None, 1), s1=("stand", "worried", 1),
         l0=("carry", "worried", 1), l2=("carry", "worried", -1)),
    # 2 '抬起来' hoisted overhead
    dict(s3=("scared", None, 1), capt=("worried", None, 1), s1=("scared", None, 1),
         l0=("lift", None, 1), l2=("lift", None, 1)),
    # 3 after the throw: watching the splash
    dict(s3=("scared", None, 1), capt=("worried", None, 1), s1=("scared", None, 1),
         l0=("stand", "worried", 1), l2=("point", "worried", 1)),
    # 4 the sea is calm: awe
    dict(s3=("pray", "surprised", 1), capt=("stand", "surprised", 1), s1=("pray", "surprised", 1),
         l0=("pray", "surprised", 1), l2=("point", "surprised", 1)),
]


def a_crew(stage):
    st = A_STAGES[stage]
    b = ""
    for name, x, v in A_CAST:
        pose, ex, f = st[name]
        if name == "capt":
            b += C.captain(x, DECK, SS, f, pose=pose, expr=ex)
        else:
            b += C.sailor(x, DECK, SS, f, variant=v, pose=pose, expr=ex)
    return doc(b)


def pennant(mode, ph):
    """The masthead pennant (terracotta streamer flying toward the bow, i.e. LEFT). mode: 'storm' (stretched out
    and rippling), 'ease' (sagging), 'calm' (hanging slack down the mast)."""
    x0, y0 = PEN
    n = 16
    if mode == "storm":
        L = 168
        ang = lambda s: math.radians(4 + 16 * s * math.sin(2 * math.pi * (1.4 * s - ph)))  # noqa: E731
    elif mode == "ease":
        L = 150
        ang = lambda s: math.radians(28 + 34 * s + 8 * math.sin(2 * math.pi * (s - ph)))  # noqa: E731
    else:
        L = 136
        ang = lambda s: math.radians(30 + 52 * s ** 1.3 + 8 * math.sin(2 * math.pi * (0.9 * s - ph)))  # noqa: E731
    cx, cy = x0 - 4, y0 + 14
    top, bot = [], []
    for i in range(n + 1):
        s = i / n
        a = ang(s)
        w = 22 * (1 - s) + 3
        nx, ny = -math.sin(a), -math.cos(a)      # normal of the direction (-cos a, sin a)
        top.append((cx + nx * w / 2, cy + ny * w / 2))
        bot.append((cx - nx * w / 2, cy - ny * w / 2))
        cx += -math.cos(a) * L / n
        cy += math.sin(a) * L / n
    pts = top + [(cx - math.cos(ang(1)) * 6, cy + math.sin(ang(1)) * 6)] + bot[::-1]
    d = S.smooth_path(pts, closed=True, tension=0.8)
    return doc(S.g(S.path(d, fill=P["sail_stripe"], sw=3.2), filter="wobble-fine"))


SWIRL_O = (60, 80)      # where a wind mark is drawn inside its layer


def wind_swirl(k):
    """A picture-book wind mark (a long curly stroke with one loop), drawn at the stage origin; one of 3 shapes."""
    d = ["M0,0 C60,-26 130,-30 175,-4 C205,16 190,48 162,40 C138,32 146,4 176,0 C230,-6 290,8 350,-2",
         "M0,0 C70,-14 120,-10 160,6 C190,20 176,50 150,42 C126,34 136,6 168,2 C220,-4 260,-2 300,-12",
         "M0,0 C50,-20 110,-22 150,-2 C176,12 166,40 142,34 C120,28 128,4 156,0 C200,-4 240,4 280,0"][k % 3]
    return doc(f'<g transform="translate({SWIRL_O[0]},{SWIRL_O[1]})">'
               f'<path d="{d}" fill="none" stroke="#5d6b83" stroke-width="14" stroke-linecap="round" '
               f'opacity="0.35"/><path d="{d}" fill="none" stroke="#eef2f0" stroke-width="8" stroke-linecap="round" '
               f'opacity="0.9"/></g>')


# ============================================================================ shot B painting


def b_world():
    """Calm sky with the sun, a far headland and the sunlit sea beyond the rail (one static layer)."""
    defs = (S.lin_grad("bsky", [(0, "#74b6d6"), (0.45, "#a6d5e6"), (0.8, "#e2ecd9"), (1, "#f6e2b6")]) +
            S.rad_grad("bsun", [(0, "#fff8de", 1), (0.22, "#fff1c4", 0.8), (0.6, "#ffe9b0", 0.25),
                                (1, "#ffe9b0", 0)]) +
            S.lin_grad("bsea", [(0, "#cfe8e0"), (0.3, "#9ed0d6"), (0.75, "#62a9c0"), (1, "#4a98b6")]))
    b = f'<rect x="-40" y="-40" width="{W + 80}" height="{B_HOR + 60}" fill="url(#bsky)"/>'
    b += f'<circle cx="{SUN_B[0]}" cy="{SUN_B[1]}" r="560" fill="url(#bsun)"/>'
    b += S.g(f'<circle cx="{SUN_B[0]}" cy="{SUN_B[1]}" r="78" fill="{P["sun"]}" '
             f'stroke="{S.shade(P["sun_hot"], -0.1)}" stroke-width="4"/>', filter="wobble")
    # a hazy headland far away on the left horizon (as in the v1 calm)
    b += S.g(S.path(S.hill(-140, 620, B_HOR + 4, 74, seed=4, bottom=B_HOR + 12, bumps=2),
                    fill=S.mix(P["sea_light"], "#c9d9cf", 0.5), sw=2.5), filter="wobble", opacity=0.85)
    b += S.g(S.path(S.hill(380, 760, B_HOR + 4, 30, seed=9, bottom=B_HOR + 12, bumps=1),
                    fill=S.mix(P["sea_light"], "#d6e2d8", 0.6), sw=2), filter="wobble", opacity=0.7)
    # the sea
    b += f'<rect x="-40" y="{B_HOR}" width="{W + 80}" height="{B_RAIL - B_HOR + 60}" fill="url(#bsea)"/>'
    b += S.g(S.path(f"M-40,{B_HOR} L{W + 40},{B_HOR}", sw=3), filter="wobble", opacity=0.55)
    # the sun's glitter path on the water
    r = random.Random(5)
    gl = ""
    for i in range(15):
        y = B_HOR + 7 + i * 12 + i * i * 0.45
        w = 26 + i * 10 + r.uniform(-8, 8)
        x = SUN_B[0] + r.uniform(-14, 14)
        gl += (f'<path d="M{x - w / 2:.0f},{y:.0f} L{x + w / 2:.0f},{y:.0f}" stroke="#fff7dc" '
               f'stroke-width="{3 + i * 0.4:.1f}" stroke-linecap="round" opacity="{0.8 - i * 0.03:.2f}"/>')
    b += S.g(gl, filter="wobble")
    # long calm swells
    sw_ = ""
    for i, (y, a, lam, ph) in enumerate([(B_HOR + 30, 2, 260, 0.3), (B_HOR + 66, 3, 330, 1.4),
                                         (B_HOR + 110, 4, 420, 2.2), (B_HOR + 160, 5, 520, 0.8)]):
        sw_ += S.path(S.wave_line(y, a, lam, ph, x0=-60, x1=W + 60), stroke=False,
                      extra=f'stroke="#e6f3ee" stroke-width="{2.5 + i}" fill="none" opacity="0.45" '
                            f'stroke-dasharray="{120 + 60 * i} {70 + 40 * i}" stroke-dashoffset="{37 * i}"')
    b += S.g(sw_, filter="wobble")
    return doc(b, defs)


def b_clouds(drifting):
    if drifting:          # one small cloud drifts by (the others are part of the background)
        b = S.cloud(1060, 486, 170, 52, "#fbf6ec", seed=12, sw=2.5, shade_fill="#dbe7ea")
    else:
        b = (S.cloud(-60, 420, 380, 110, "#fbf6ec", seed=3, sw=3, shade_fill="#dbe7ea") +
             S.cloud(900, 376, 300, 92, "#fbf6ec", seed=5, sw=3, shade_fill="#dbe7ea") +
             S.cloud(2080, 440, 330, 96, "#fbf6ec", seed=9, sw=3, shade_fill="#dbe7ea"))
    return doc(S.g(b, filter="wobble"))


def inner(d):
    """The content of an svg_doc (its <defs> and body) for nesting several paintings into one layer."""
    return d[d.index(">") + 1:d.rindex("</svg>")]


def b_background():
    """Shot B's static backdrop in ONE layer (cheap to composite): sky, sea, clouds, deck and rig, sunbeams."""
    return doc(inner(b_world()) + inner(b_clouds(False)) + inner(b_deck()) + inner(b_beams(0.75)))


def b_sea_lines(k):
    """Soft foam ripple strokes on the calm water (two phases, slid gently)."""
    b = ""
    r = random.Random(20 + k)
    for i in range(9):
        y = B_HOR + 22 + i * 22 + r.uniform(-4, 4)
        x = r.uniform(-100, W)
        w = 120 + i * 22
        b += S.path(S.wave_line(y, 2 + i * 0.3, w / 1.5, r.uniform(0, 6), x0=x, x1=x + w), stroke=False,
                    extra=f'stroke="#f4faf4" stroke-width="{2.5 + i * 0.35:.1f}" fill="none" opacity="0.55" '
                          f'stroke-linecap="round"')
    return doc(S.g(b, filter="wobble"))


def b_glints(k):
    """Twinkling glints on the sun path (one of four phases)."""
    rng = random.Random(40 + k)
    b = ""
    for i in range(14):
        u = rng.random()
        y = B_HOR + 12 + u * (B_RAIL - B_HOR - 20)
        x = SUN_B[0] + rng.uniform(-1, 1) * (40 + 220 * u)
        rr = 5 + 9 * rng.random()
        w = rr * 0.24
        b += (f'<path d="M{x:.1f},{y - rr:.1f} L{x + w:.1f},{y - w:.1f} L{x + rr * 1.3:.1f},{y:.1f} L{x + w:.1f},'
              f'{y + w:.1f} L{x:.1f},{y + rr:.1f} L{x - w:.1f},{y + w:.1f} L{x - rr * 1.3:.1f},{y:.1f} '
              f'L{x - w:.1f},{y - w:.1f} Z" fill="#fffbe8" opacity="0.9"/>')
    return doc(b)


def shield(cx, cy, r, col):
    return V5.shield(cx, cy, r, col)


def b_rig():
    """Mast, shrouds and the torn striped sail (v1 deck rig), hanging calm."""
    mx = MAST_B
    base = B_DBACK + 70
    b = ""
    for xr in (mx - 360, mx + 120):
        b += f'<path d="M{mx},-200 L{xr},{B_RAIL + 6}" stroke="{P["ink_soft"]}" stroke-width="5" fill="none"/>'
    b += f'<rect x="{mx - 29}" y="-60" width="58" height="{base + 60}" fill="url(#bmast)" {S.STROKE}/>'
    for yy in (640, 690):
        b += f'<rect x="{mx - 35}" y="{yy}" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<path d="M{mx - 57},{base} Q{mx},{base - 32} {mx + 57},{base} Z" fill="{P["wood_dark"]}" {S.STROKE}/>'
    b += f'<path d="M{mx + 29},610 L{mx + 76},610" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linecap="round"/>'
    k, y_yard = 0.84, 196
    base_y = y_yard + 848 * k
    sail = PR._sail("torn", "s9sail")
    b += (f'<g transform="rotate(3 {mx} {y_yard})"><g transform="translate({mx},{base_y}) scale({-k},{k}) '
          f'translate(10,0)">{sail}</g></g>')
    # sheets: the stern one down to the bulwark (left), the bow one tied off on the mast (clear of the crew)
    sx = mx - k * 290
    b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} L{sx - 230:.0f},{B_RAIL + 4}" stroke="{P["ink_soft"]}" '
          f'stroke-width="4" fill="none"/>')
    sx = mx + k * 310
    b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} Q{mx + 120:.0f},{base_y - 470 * k:.0f} {mx + 30},600" '
          f'stroke="{P["ink_soft"]}" stroke-width="4" fill="none"/>')
    defs = S.lin_grad("bmast", [(0, P["wood_dark"]), (0.4, P["wood_light"]), (1, P["wood"])], x1=0, y1=0, x2=1, y2=0)
    return S.g(b, filter="wobble"), defs


def b_deck():
    """Far bulwark with shields, the sunlit deck (puddles left by the storm), the rig, crate, jar and rope."""
    defs = (S.lin_grad("bdeck", [(0, "#c69259"), (0.45, "#d9a56b"), (1, "#b07a48")]) +
            S.lin_grad("bbulw", [(0, P["wood"]), (1, "#80502f")]) +
            S.rad_grad("bwarm", [(0, "#fff1c4", 0.55), (1, "#fff1c4", 0)]))
    b = ""
    b += (f'<rect x="-40" y="{B_RAIL + 14}" width="{W + 80}" height="{B_DBACK - B_RAIL - 4}" fill="url(#bbulw)" '
          f'{S.STROKE}/>')
    b += V5.plank_lines(-40, W + 40, [B_RAIL + 42, B_RAIL + 68], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += (f'<rect x="{x - 12}" y="{B_RAIL + 4}" width="24" height="{B_DBACK - B_RAIL}" fill="{P["wood_dark"]}" '
              f'{S.STROKE_THIN}/>')
    for xr in (MAST_B - 360, MAST_B + 360):
        b += f'<circle cx="{xr}" cy="{B_RAIL + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += shield(x, B_RAIL + 52, 33, cols[i % 4])
    b += (f'<path d="M-40,{B_RAIL} L{W + 40},{B_RAIL} L{W + 40},{B_RAIL + 18} L-40,{B_RAIL + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    # sun on the rail top
    b += (f'<path d="M-40,{B_RAIL + 5} L{W + 40},{B_RAIL + 5}" stroke="#f6dca6" stroke-width="5" opacity="0.8"/>')
    b += f'<rect x="-40" y="{B_DBACK}" width="{W + 80}" height="{H - B_DBACK + 40}" fill="url(#bdeck)" {S.STROKE}/>'
    ys, y, gap = [], B_DBACK + 14, 15
    while y < H + 40:
        ys.append(y)
        y += gap
        gap *= 1.17
    b += V5.plank_lines(-40, W + 40, ys, seed=7, opacity=0.42, joint_every=(260, 620))
    # puddles left by the storm, mirroring the sky
    for (x, y, rx, ry) in [(520, 1110, 120, 15), (1480, 1120, 150, 17), (940, 1165, 110, 13), (1720, 1010, 90, 11)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#bfe0e6" opacity="0.6"/>'
        b += (f'<path d="M{x - rx * 0.55},{y - 3} l{rx * 0.5},0 M{x + rx * 0.1},{y + 4} l{rx * 0.3},0" '
              f'stroke="#fbfdf6" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    # warm sunlight pooled on the deck under the beams
    b += '<ellipse cx="1180" cy="1010" rx="620" ry="120" fill="url(#bwarm)"/>'
    rig, rdefs = b_rig()
    b = S.g(b, filter="wobble") + rig
    # props against the bulwark (left) and a coil of rope
    b += PR.crate(360, 905, 1.0) + PR.jar(270, 930, 0.62, rot=-6) + C.ground_shadow(360, 958, 1.0, width=150,
                                                                                      opacity=0.16)
    b += PR.rope_coil(MAST_B + 70, B_DBACK + 82, 0.9)
    return doc(b, defs + rdefs)


def b_foreground():
    return doc(PR.rope_coil(290, 1150, 1.45) + V5.bucket(1660, 1132, 1.05) +
               C.ground_shadow(1660, 1134, 1.0, width=120, opacity=0.18))


def b_beams(k=1.0):
    """Wedge-shaped sunbeams falling from the sun toward the lower left (light; k scales the opacity)."""
    sx, sy = SUN_B
    defs = (f'<linearGradient id="bbeam" gradientUnits="userSpaceOnUse" x1="{sx}" y1="{sy}" x2="{sx - 900}" '
            f'y2="{sy + 900}"><stop offset="0" stop-color="#fff2c8" stop-opacity="0.75"/>'
            f'<stop offset="0.55" stop-color="#ffeec0" stop-opacity="0.32"/>'
            f'<stop offset="1" stop-color="#ffeec0" stop-opacity="0"/></linearGradient>')
    d = ""
    for ang, wd in [(112, 5), (121, 7), (131, 5), (139, 8), (149, 5), (158, 7), (168, 4)]:
        a0, a1 = math.radians(ang - wd / 2), math.radians(ang + wd / 2)
        r0, r1 = 110, 1500
        d += (f"M{sx + r0 * math.cos(a0):.1f},{sy + r0 * math.sin(a0):.1f} L{sx + r1 * math.cos(a0):.1f},"
              f"{sy + r1 * math.sin(a0):.1f} L{sx + r1 * math.cos(a1):.1f},{sy + r1 * math.sin(a1):.1f} "
              f"L{sx + r0 * math.cos(a1):.1f},{sy + r0 * math.sin(a1):.1f} Z ")
    return doc(S.g(S.g(S.path(d, fill="url(#bbeam)", stroke=False), filter="soft") +
                   f'<circle cx="{sx}" cy="{sy}" r="230" fill="#fff6d6" opacity="0.55" filter="url(#blur-md)"/>',
                   opacity=f"{k:.2f}"), defs)


def sun_glow():
    """A soft halo round the sun (screen-blended, pulsing; it swells at the vows)."""
    sx, sy = SUN_B
    defs = S.rad_grad("bhalo", [(0, "#fff4cc", 0.9), (0.35, "#ffefc0", 0.45), (1, "#ffefc0", 0)])
    return doc(f'<circle cx="{sx}" cy="{sy}" r="300" fill="url(#bhalo)"/>', defs)


# ---------------------------------------------------------------- the offering: brazier, flame, smoke


def brazier():
    """Small bronze tripod brazier with glowing coals (anchor ALT on the deck)."""
    x, y = ALT
    br, dk, lt = "#b9853f", "#7d5226", "#e4b46c"
    defs = S.lin_grad("bbowl", [(0, lt), (0.45, br), (1, dk)], x1=0, y1=0, x2=1, y2=0.4)
    b = C.ground_shadow(x, y + 2, 1.0, width=210, opacity=0.24)
    leg = ""
    # back leg (behind, shorter), then the two front legs splaying out to paw feet
    leg += (f'<path d="M{x + 10},{RIM_Y + 34} Q{x + 18},{y - 60} {x + 14},{y - 16}" stroke="{S.INK}" '
            f'stroke-width="17" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x + 10},{RIM_Y + 34} Q{x + 18},{y - 60} {x + 14},{y - 16}" stroke="{dk}" '
            f'stroke-width="9" fill="none" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        leg += (f'<path d="M{x + sgn * 44},{RIM_Y + 30} Q{x + sgn * 58},{y - 70} {x + sgn * 70},{y - 8}" '
                f'stroke="{S.INK}" stroke-width="19" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x + sgn * 44},{RIM_Y + 30} Q{x + sgn * 58},{y - 70} {x + sgn * 70},{y - 8}" '
                f'stroke="{br}" stroke-width="11" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x + sgn * 47},{RIM_Y + 40} Q{x + sgn * 58},{y - 72} {x + sgn * 66},{y - 20}" '
                f'stroke="{lt}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>'
                f'<ellipse cx="{x + sgn * 74}" cy="{y - 4}" rx="16" ry="9" fill="{br}" {S.STROKE_THIN}/>')
    # a ring brace between the legs
    leg += (f'<ellipse cx="{x + 4}" cy="{y - 58}" rx="60" ry="9" fill="none" stroke="{S.INK}" stroke-width="10"/>'
            f'<ellipse cx="{x + 4}" cy="{y - 58}" rx="60" ry="9" fill="none" stroke="{br}" stroke-width="5"/>')
    b += S.g(leg, filter="wobble-fine")
    bowl = ""
    bowl += (f'<path d="M{x - 84},{RIM_Y} Q{x - 78},{RIM_Y + 50} {x},{RIM_Y + 52} Q{x + 78},{RIM_Y + 50} '
             f'{x + 84},{RIM_Y} Z" fill="url(#bbowl)" {S.STROKE}/>')
    bowl += (f'<path d="M{x - 72},{RIM_Y + 18} Q{x},{RIM_Y + 34} {x + 72},{RIM_Y + 18}" stroke="{dk}" '
             f'stroke-width="5" fill="none" opacity="0.7"/>')
    for i in range(7):
        u = -0.75 + i * 0.25
        bowl += f'<circle cx="{x + u * 68:.1f}" cy="{RIM_Y + 26 + 6 * (1 - u * u):.1f}" r="4" fill="{lt}" opacity="0.9"/>'
    # coals heaped in the bowl, glowing
    coals = ""
    rr = random.Random(3)
    for i in range(9):
        cx = x - 58 + i * 14.5 + rr.uniform(-4, 4)
        cy = RIM_Y - 4 - 9 * math.sin(math.pi * (i + 0.5) / 9) + rr.uniform(-2, 2)
        r = rr.uniform(10, 15)
        coals += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#5e2c1e" {S.STROKE_THIN}/>'
        coals += (f'<path d="M{cx - r * 0.5:.1f},{cy:.1f} q{r * 0.4:.1f},{-r * 0.3:.1f} {r * 0.8:.1f},{r * 0.1:.1f}" '
                  f'stroke="#f39a3c" stroke-width="3" fill="none" stroke-linecap="round"/>')
    bowl += coals
    bowl += (f'<path d="M{x - 84},{RIM_Y} Q{x},{RIM_Y + 15} {x + 84},{RIM_Y}" stroke="{S.INK}" stroke-width="13" '
             f'fill="none" stroke-linecap="round"/>'
             f'<path d="M{x - 84},{RIM_Y} Q{x},{RIM_Y + 15} {x + 84},{RIM_Y}" stroke="{lt}" stroke-width="6" '
             f'fill="none" stroke-linecap="round"/>')
    b += S.g(bowl, filter="wobble-fine")
    return doc(b, defs)


def flame(i):
    """One of six hand-drawn flicker frames of the altar flame (base at FLAME_B, ~100 px tall)."""
    rr = random.Random(70 + i)
    bx, by = FLAME_B

    def tongue(cx, h, w, lean):
        pts = [(cx - w, by), (cx - w * 0.85, by - h * 0.32), (cx - w * 0.35 + lean * 0.35, by - h * 0.7),
               (cx + lean, by - h), (cx + w * 0.3 + lean * 0.5, by - h * 0.62), (cx + w * 0.85, by - h * 0.3),
               (cx + w, by)]
        return S.smooth_path(pts, closed=False, tension=0.9) + f" Q{cx},{by + w * 0.5:.1f} {cx - w:.1f},{by} Z"

    outer = [tongue(bx - 26, 64 + rr.uniform(-10, 12), 26, rr.uniform(-16, 4)),
             tongue(bx + 4, 102 + rr.uniform(-12, 14), 40, rr.uniform(-12, 12)),
             tongue(bx + 30, 58 + rr.uniform(-10, 10), 24, rr.uniform(-4, 16))]
    mid = [tongue(bx - 6, 62 + rr.uniform(-8, 10), 26, rr.uniform(-10, 10)),
           tongue(bx + 18, 40 + rr.uniform(-6, 8), 16, rr.uniform(-6, 10))]
    core = tongue(bx + 2, 30 + rr.uniform(-4, 6), 14, rr.uniform(-5, 5))
    b = "".join(f'<path d="{d}" fill="#f08c38" stroke="{S.INK}" stroke-width="7" stroke-linejoin="round"/>'
                for d in outer)
    b += "".join(f'<path d="{d}" fill="#f08c38"/>' for d in outer)
    b += "".join(f'<path d="{d}" fill="#f7cd55"/>' for d in mid)
    b += f'<path d="{core}" fill="#fff3cc"/>'
    return doc(S.g(b, filter="wobble-fine"))


def glow():
    x, y = FLAME_B
    defs = S.rad_grad("bglow", [(0, "#ffd27a", 0.75), (0.45, "#ffc56a", 0.3), (1, "#ffc56a", 0)])
    return doc(f'<circle cx="{x}" cy="{y - 40}" r="240" fill="url(#bglow)"/>', defs)


SMOKE_L = 520          # height of the smoke column


def smoke_xy(s, ph):
    """Centre line of the smoke column at height fraction s (0 = flame tip) for wave phase ph: it sways and leans
    toward the sun as it rises."""
    ox, oy = SMOKE_O
    return (ox + 150 * s ** 1.6 + 26 * s * math.sin(2 * math.pi * (1.25 * s - ph)), oy - SMOKE_L * s)


def _billows(circles):
    """Cloud-like smoke from circles [(x, y, r, colour)]: a darker rim on the outer silhouette only (all rim
    circles first, then the bodies), then small highlights."""
    rim = "".join(f'<circle cx="{x + r * 0.1:.1f}" cy="{y + r * 0.12:.1f}" r="{r * 1.06 + 2:.1f}" fill="#bfb2a3"/>'
                  for x, y, r, _ in circles)
    body = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}"/>' for x, y, r, c in circles)
    hi = "".join(f'<circle cx="{x - r * 0.28:.1f}" cy="{y - r * 0.3:.1f}" r="{r * 0.36:.1f}" fill="#fdfaf3" '
                 f'opacity="0.5"/>' for x, y, r, _ in circles[1::3])
    return rim + body + hi


SMOKE_DEFS = '<filter id="s9blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.2"/></filter>'


def smoke_column(ph, thick=1.0, tag="c"):
    """The smoke rising from the flame (phase ph of its sway): a chain of soft billows widening upward, cream-grey
    low down and pale gold where it rises into the sunlight, fading in above the flame and out at the top (mask);
    two hand-drawn curls ride on it."""
    ox, oy = SMOKE_O
    n = 18
    circ = []
    for i in range(n):
        s_ = (i + 0.35) / n
        x, y = smoke_xy(s_, ph)
        r = (11 + 46 * s_) * thick * (1 + 0.12 * math.sin(i * 2.3 + ph * 6.28))
        circ.append((x + 5 * math.sin(i * 1.7), y, r, S.mix("#ece6dd", "#fbe9bf", min(1.0, s_ * 1.4))))
    mid = f"smm{tag}{int(ph * 100)}"
    gid = f"smg{tag}{int(ph * 100)}"
    defs = (SMOKE_DEFS +
            f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{ox}" y1="{oy}" x2="{ox}" '
            f'y2="{oy - SMOKE_L - 60}"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="0.1" stop-color="#fff" stop-opacity="0.92"/>'
            f'<stop offset="0.55" stop-color="#fff" stop-opacity="0.8"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/></mask>')
    b = f'<g mask="url(#{mid})"><g filter="url(#s9blur)">{_billows(circ)}</g></g>'
    curls = ""
    for s0, sgn in ((0.32, 1), (0.6, -1)):
        x, y = smoke_xy(s0, ph)
        r = (10 + 22 * s0) * thick
        curls += (f'<path d="M{x - sgn * r:.1f},{y + r * 0.4:.1f} q{sgn * r * 0.2:.1f},{-r * 1.1:.1f} '
                  f'{sgn * r:.1f},{-r * 0.9:.1f} q{sgn * r * 0.7:.1f},{r * 0.3:.1f} {sgn * r * 0.2:.1f},{r * 0.75:.1f} '
                  f'q{-sgn * r * 0.4:.1f},{r * 0.15:.1f} {-sgn * r * 0.45:.1f},{-r * 0.2:.1f}" fill="none" '
                  f'stroke="#a8998a" stroke-width="3" stroke-linecap="round" opacity="{0.7 - 0.3 * s0:.2f}"/>')
    return doc(b + S.g(curls, filter="wobble-fine"), defs)


def soft_puff(gold, seed, r0=34):
    """A soft billow of smoke at SMOKE_O (grey-cream, or pale gold in the sunlight)."""
    rr = random.Random(seed)
    x, y = SMOKE_O
    col = "#fbe7b8" if gold else "#ece6dd"
    circ = [(x + rr.uniform(-0.55, 0.55) * r0, y + rr.uniform(-0.35, 0.3) * r0, rr.uniform(0.5, 0.75) * r0, col)
            for _ in range(5)]
    curl = (f'<path d="M{x - r0 * 0.45:.1f},{y + r0 * 0.15:.1f} q{r0 * 0.1:.1f},{-r0 * 0.45:.1f} {r0 * 0.45:.1f},'
            f'{-r0 * 0.35:.1f} q{r0 * 0.3:.1f},{r0 * 0.15:.1f} {r0 * 0.1:.1f},{r0 * 0.35:.1f}" fill="none" '
            f'stroke="{"#d8b06a" if gold else "#a8998a"}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>')
    return doc(f'<g filter="url(#s9blur)">{_billows(circ)}</g>' + S.g(curl, filter="wobble-fine"), SMOKE_DEFS)


def offering_bowl(cx, cy, s=1.0, tilt=0.0, full=True):
    """Small terracotta bowl heaped with grain (the offering), centred on its rim (cx, cy)."""
    rx, d = 34 * s, 26 * s
    sw = 3.2 * s
    st = f'stroke="{S.INK}" stroke-width="{sw:.1f}" stroke-linejoin="round"'
    b = ""
    if full:
        b += (f'<path d="M{cx - rx * 0.9:.1f},{cy:.1f} Q{cx - rx * 0.6:.1f},{cy - 22 * s:.1f} {cx:.1f},{cy - 24 * s:.1f} '
              f'Q{cx + rx * 0.6:.1f},{cy - 22 * s:.1f} {cx + rx * 0.9:.1f},{cy:.1f} Z" fill="{P["sand"]}" {st}/>')
        rr = random.Random(9)
        for _ in range(9):
            gx, gy = cx + rr.uniform(-0.6, 0.6) * rx, cy - rr.uniform(3, 17) * s
            b += f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{2.6 * s:.1f}" ry="{1.7 * s:.1f}" fill="{P["sand_dark"]}"/>'
    b += (f'<path d="M{cx - rx:.1f},{cy:.1f} Q{cx - rx * 0.92:.1f},{cy + d * 1.2:.1f} {cx:.1f},{cy + d:.1f} '
          f'Q{cx + rx * 0.92:.1f},{cy + d * 1.2:.1f} {cx + rx:.1f},{cy:.1f} Z" fill="{P["terracotta"]}" {st}/>')
    b += (f'<path d="M{cx - rx * 0.86:.1f},{cy + d * 0.38:.1f} Q{cx:.1f},{cy + d * 0.62:.1f} {cx + rx * 0.86:.1f},'
          f'{cy + d * 0.38:.1f}" stroke="{P["headcloth"]}" stroke-width="{4 * s:.1f}" fill="none"/>')
    b += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{6 * s:.1f}" fill="none" {st}/>')
    if tilt:
        b = f'<g transform="rotate({tilt:.1f} {cx:.1f} {cy:.1f})">{b}</g>'
    return S.g(b, filter="wobble-fine")


# ---------------------------------------------------------------- the kneeling crew

KNEEL = C.POSES["kneel_pray"]
P_BOW = dict(KNEEL, t=6, h=16)                                         # palms together, head bowed
P_UP = dict(KNEEL)                                                     # palms together, head tilted up
P_VOW = dict(KNEEL, t=-4, h=-20, arms=(("fk", 135, 158), ("fk", 118, 142)), hands=("open", "open"))  # hands
#                                                                      lifted up toward the light
P_OFFER = dict(KNEEL, t=2, h=2, arms=(("ik", "abs", 150, -196, 1), ("ik", "abs", 126, -186, 1)),
               hands=("open", "open"))                                 # holding the bowl out over the brazier
P_POUR = dict(KNEEL, t=4, h=10, arms=(("ik", "abs", 150, -214, 1), ("ik", "abs", 128, -204, 1)),
              hands=("open", "open"))                                 # ...tipping it into the fire
POUR_TILT = 48


def kfig(kind, variant, x, y, s, ps, expr, facing=1):
    """A sailor / the captain in any rig pose (also the custom kneeling ones): (markup, hand points in stage px)."""
    if kind == "capt":
        design, met = C._captain_design(), C._CAPTAIN_M
    else:
        design, met = C._sailor_design(variant), C._SAILOR_M
    inner, _ = C._figure(design, met, dict(ps), expr, 1 if facing >= 0 else -1, True)
    hands = [(x + hx * s * facing, y + hy * s) for hx, hy in C._LAST["hands"]]
    return C._wrap_out(inner, x, y, s, facing, f"{kind}{variant}"), hands


def b_frames(kind, variant, pos, poses):
    """Flipbook docs for one kneeling crew member. poses: [(pose dict, expr, extra)], extra None|'bowl'|'pour'."""
    x, y, s = pos
    out = []
    for ps, ex, extra in poses:
        kneeling = ps.get("legs") == KNEEL["legs"]
        body = C.ground_shadow(x + (-14 if kneeling else 0) * s, y, s, width=200 if kneeling else 130, opacity=0.2)
        fig, hands = kfig(kind, variant, x, y, s, ps, ex)
        body += fig
        if extra in ("bowl", "pour"):
            hx = (hands[0][0] + hands[1][0]) / 2
            hy = min(hands[0][1], hands[1][1])
            body += offering_bowl(hx + 4 * s, hy - 22 * s, s * 0.95, tilt=POUR_TILT if extra == "pour" else 0,
                                  full=extra == "bowl")
        out.append(doc(body))
    return out


def grains(k, lip):
    """Falling grain (3 phases) from the tipped bowl's lip into the coals."""
    x0, y0 = lip
    x1, y1 = FLAME_B[0] - 12, RIM_Y - 8
    b = ""
    for i in range(9):
        u = ((i + k / 3) / 9) % 1.0
        gx = lerp(x0, x1, u) + 4 * math.sin(i * 2.1)
        gy = lerp(y0, y1, u) + 10 * u * u
        b += (f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="4.6" ry="3.2" fill="{P["sand"]}" stroke="{S.INK}" '
              f'stroke-width="1.6"/>')
    return doc(S.g(b, filter="wobble-fine"))


# ============================================================================ effects


def sparks_fx(src, t0, t1, rate, seed=4):
    """Little rising sparks from the flame (output space)."""
    rng = np.random.default_rng(seed)
    n = max(1, int((t1 - t0) * rate))
    ts = t0 + (np.arange(n) + rng.uniform(0, 1, n)) / rate
    xs = rng.uniform(-30, 30, n)
    vx = rng.uniform(-25, 55, n)
    vy = rng.uniform(140, 260, n)
    life = rng.uniform(0.7, 1.4, n)
    ph = rng.uniform(0, 6.3, n)
    sz = rng.uniform(2.5, 4.5, n)

    def fx(frame, t, view):
        live = np.nonzero((ts <= t) & (t < ts + life))[0]
        if not len(live):
            return frame
        pts = []
        for i in live:
            age = t - ts[i]
            x = src[0] + xs[i] + vx[i] * age + 9 * math.sin(age * 7 + ph[i])
            y = src[1] - vy[i] * age + 40 * age * age
            ox, oy = view.to_out(x, y)
            r = sz[i] * view.scale * (1 - 0.5 * age / life[i])
            pts.append((ox, oy, r, int(235 * (1 - age / life[i]))))
        # draw into a small overlay around the sparks only (cheap)
        x0 = int(max(0, min(p[0] - 3 * p[2] for p in pts) - 2))
        y0 = int(max(0, min(p[1] - 3 * p[2] for p in pts) - 2))
        x1 = int(min(frame.size[0], max(p[0] + 3 * p[2] for p in pts) + 2))
        y1 = int(min(frame.size[1], max(p[1] + 3 * p[2] for p in pts) + 2))
        if x1 <= x0 or y1 <= y0:
            return frame
        ov = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ox, oy, r, a in pts:
            ox, oy = ox - x0, oy - y0
            d.ellipse([ox - r * 2.2, oy - r * 2.2, ox + r * 2.2, oy + r * 2.2], fill=(255, 190, 90, a // 4))
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(255, 226, 140, a))
        frame.alpha_composite(ov, dest=(x0, y0))
        return frame
    return fx


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[0], ctx.lines[1], ctx.lines[2]
    cue = Cues(ctx)

    # ---- timing, all from the narration
    t_grab = cue.at("他们", L0.start + 0.7) + 0.12          # the lifters crouch and take hold of Jonah
    t_lift = cue.at("抬起来", L0.start + 1.8) - 0.12        # ...hoist him overhead
    t_up = t_lift + 0.34
    t_heave0 = cue.at("扔进", L0.start + 2.6) - 0.3         # dip...
    t_launch = t_heave0 + 0.52                             # ...and heave him over the stern
    t_watch = t_launch + 0.42
    t_impact = t_launch + 0.72                             # '大海'
    t_flash = L0.start + 0.45
    t_calm0 = L1.start                                     # '一下子'
    t_calm1 = t_calm0 + 1.1                                # '海就平静了'
    t_awe = cue.at("海就", t_calm0 + 0.6) + 0.15
    t_wind = cue.at("风停了", L1.start + 2.4)                # '风停了'
    t_still = cue.at("浪也", L1.start + 3.3)                 # '浪也静了'
    t_d0 = L1.end + 0.06                                   # cross-dissolve to the deck
    t_d1 = max(t_d0 + 0.9, L2.start - 0.12)
    c2a, c2b = L2.chunks[0], L2.chunks[-1]
    t_see2 = c2a.start + 0.55                              # a sailor lifts his hands in wonder
    t_kn = cue.at("心里", c2a.start + 1.7)                  # '心里对耶和华又敬又怕' they kneel one by one
    t_off0 = c2b.start + 0.15                              # '他们向耶和华' the captain lifts the bowl
    t_pour = cue.at("献上", c2b.start + 1.6, snap=False) - 0.05   # '献上祭物' he pours it into the fire
    t_flare = t_pour + 0.22
    t_look = t_flare + 0.25                                # the others raise their heads to the smoke
    t_vow = cue.at("还许", c2b.end - 1.5) + 0.05            # '还许下了诺言' hands lifted to the sky

    def storm(t):          # 1 = full storm, 0 = calm
        return 1 - progress(t, t_calm0, t_calm1, "inout")

    def storm_fast(t):     # storm crests / banks: gone before the blue sky dominates
        return 1 - progress(t, t_calm0, t_calm0 + 0.6, "sine")

    def stillness(t):      # '浪也静了': the last swell settles
        return progress(t, t_still, t_still + 1.3, "sine")

    def a_on(t):           # shot A is hidden once the deck has dissolved in
        return 1.0 if t < t_d1 + 0.04 else 0.0

    def b_a(t):
        return progress(t, t_d0, t_d1, "sine")

    def a_only(m):
        return lambda t: replace(m(t), alpha=m(t).alpha * a_on(t)) if a_on(t) else Tf(alpha=0.0)

    def b_only(m=None):
        def f(t):
            k = b_a(t)
            if k <= 0.002:
                return Tf(alpha=0.0)
            v = m(t) if m else Tf()
            return replace(v, alpha=v.alpha * k)
        return f

    # ================================================================ shot A
    def rock(t):
        return 0.05 + 0.13 * (1 - stillness(t)) + 0.82 * storm(t)

    def ship_tf(t):
        a = rock(t)
        return Tf(dx=8 * a * math.sin(2 * math.pi * t / 3.1), dy=12 * a * math.sin(2 * math.pi * t / 2.2 + 0.6),
                  rot=4.2 * a * math.sin(2 * math.pi * t / 2.6), px=SX, py=WL)

    heave = M.keys([(t_heave0, {"dy": 0}), (t_heave0 + 0.24, {"dy": 14}), (t_launch, {"dy": -34}),
                    (t_launch + 0.35, {"dy": 0})], ["inout", "out", "inout"])

    def crew_m(t):
        s = ship_tf(t)
        hop = 7 * (bump(t, t_grab) + 1.4 * bump(t, t_lift) + bump(t, t_watch) + bump(t, t_awe))
        return Tf(dx=s.dx, dy=s.dy + 0.45 * heave(t).dy - hop, rot=s.rot, px=SX, py=WL)

    def stand_m(t):
        c = crew_m(t)
        return replace(c, dy=c.dy + 4 * bump(t, t_grab), alpha=float(t < t_lift))

    rise = 104.0

    def carried_m(t):      # hoisted onto the lifters' hands, then rides on them; pushed higher by the heave
        c = crew_m(t)
        r = rise * (1 - progress(t, t_lift, t_up, "back"))
        return Tf(dx=c.dx, dy=c.dy + r + 0.55 * min(0.0, heave(t).dy), rot=c.rot,
                  alpha=float(t_lift <= t < t_launch), px=SX, py=WL)

    # the calm-weather background is completely covered by the storm overlays until the calm: skip it till then
    def under_storm(t):
        return Tf(alpha=progress(t, t_calm0 - 0.9, t_calm0, "sine"))
    sc.add("a_background", V.background(), z=0, wc=0.8, motion=a_only(under_storm))
    sc.add("a_shafts", V.light_shafts(), z=1, wc=0, motion=a_only(under_storm))
    sc.add("a_clouds", V.clouds_clear(), z=2,
           motion=a_only(M.combine(M.visible(t_calm0 + 0.55, fade=0.45), M.drift(vx=6, t0=t_calm0))))
    sc.add("a_sunbeams", V.sunbeams(), z=3, wc=0,
           motion=a_only(lambda t: Tf(alpha=progress(t, t_calm0 + 0.3, t_calm1 + 0.4, "sine") *
                                      (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.7)))))
    t_gull = t_wind - 0.3
    gull_frames = [doc(PR.gull(1900, 470, 0.55, -1, wing=w) + PR.gull(2030, 540, 0.45, -1, wing=-w * 0.8))
                   for w in (1.0, 0.0, -1.0, 0.0)]
    sc.add("a_gulls", gull_frames, z=4,
           motion=a_only(M.combine(M.drift(vx=-110, vy=-8, t0=t_gull), M.visible(t_gull, fade=0.5))),
           frame_at=lambda t: float(int(t * 7) % 4))
    sc.add("a_storm", V.storm_overlay(), z=5, motion=a_only(lambda t: Tf(alpha=storm(t))))
    for side in (-1, 1):
        sc.add(f"a_storm_bank{side}", V.storm_bank(side), z=6,
               motion=a_only(lambda t, s=side: Tf(dx=s * 1250 * progress(t, t_calm0 - 0.1, t_calm0 + 0.65, "sine") +
                                                  s * 8 * math.sin(t * 1.3), alpha=storm_fast(t))))

    # pennant: whipping in the storm; at '风停了' it sags and hangs slack (flipbook, never crossfaded)
    pen_frames = [pennant("storm", k / 4) for k in range(4)] + [pennant("ease", 0.0), pennant("ease", 0.3)] + \
                 [pennant("calm", 0.0), pennant("calm", 0.5)]

    def pen_idx(t):
        if t < t_wind:
            return float(int(t * 11) % 4)
        if t < t_wind + 0.36:
            return 4.0 + float(t >= t_wind + 0.18)
        return 6.0 + float(int((t - t_wind) * 1.2) % 2)
    sc.add("a_pennant", pen_frames, z=10.2, motion=a_only(ship_tf), frame_at=pen_idx)

    # wind marks blowing across the sky toward the bow: strong in the storm, a breeze after the calm, gone at '风停了'
    def wind_k(t):
        return (0.55 + 0.45 * storm(t)) * (1 - progress(t, t_wind - 0.1, t_wind + 0.45, "sine"))

    swirls = [(0, 1500, 300, 0.0, 1.3), (1, 900, 470, 0.37, 1.05), (2, 1900, 560, 0.62, 1.15), (0, 400, 210, 0.81, 1.0),
              (1, 1200, 170, 0.2, 1.1)]
    span = 2400.0
    for i, (kind, x0, y0, ph, sc_) in enumerate(swirls):
        def sw_m(t, x0=x0, y0=y0, ph=ph, sc_=sc_, i=i):
            k = wind_k(t)
            if k <= 0.003:
                return Tf(alpha=0.0)
            u = (t * (0.32 + 0.1 * storm(t)) + ph) % 1.0      # position along its path (right -> left)
            x = 2250 - span * u
            env = math.sin(math.pi * u) ** 0.6
            return Tf(dx=x - SWIRL_O[0], dy=y0 - SWIRL_O[1] + 14 * math.sin(t * 2.3 + i), sx=sc_,
                      sy=sc_ * (1 + 0.1 * math.sin(t * 3 + i)), alpha=k * env, px=SWIRL_O[0], py=SWIRL_O[1])
        sc.add(f"a_wind{i}", wind_swirl(kind), z=6.5, wc=0, motion=a_only(sw_m))

    sc.add("a_ship_back", doc(PR.ship(SX, WL, SS, SF, sail="torn", part="back", flag=False)), z=10,
           motion=a_only(ship_tf))
    sc.add("a_jonah_carried", doc(C.jonah(JCAR[0], JCAR[1], JS, -1, pose="carried")), z=10.5,
           motion=a_only(carried_m))
    sc.add("a_crew", [a_crew(i) for i in range(5)], z=11, motion=a_only(crew_m),
           frame_at=steps([(0, 0), (t_grab, 1), (t_lift, 2), (t_watch, 3), (t_awe, 4)]))
    sc.add("a_jonah_stand", doc(C.jonah(JON_X, DECK, SS, 1, pose="confess")), z=11.5, motion=a_only(stand_m))
    sc.add("a_ship_front", doc(PR.ship(SX, WL, SS, SF, sail="torn", part="front")), z=12, motion=a_only(ship_tf))

    # Jonah's flight: launched from the carried centre at the top of the heave, a ballistic arc with a tumble
    c_l = carried_m(t_launch - 1e-3)
    th = math.radians(c_l.rot)
    rx, ry = JAIR_C[0] - SX, JAIR_C[1] - WL
    p0 = (SX + rx * math.cos(th) - ry * math.sin(th) + c_l.dx,
          WL + rx * math.sin(th) + ry * math.cos(th) + c_l.dy)
    p1 = (SPLASH[0], SPLASH[1] - 6)

    def jonah_air(t):
        if t < t_launch or not a_on(t):
            return Tf(alpha=0.0)
        u = min(1.0, (t - t_launch) / (t_impact - t_launch))
        x = lerp(p0[0], p1[0], u)
        y = lerp(p0[1], p1[1], u) - 4 * 230 * u * (1 - u)
        rot = c_l.rot + 60 * progress(u, 0.1, 1.0, "inout")
        a = 1 - progress(t, t_impact - 0.04, t_impact + 0.06, "linear")
        return Tf(dx=x - JAIR_C[0], dy=y - JAIR_C[1], rot=rot, alpha=a, px=JAIR_C[0], py=JAIR_C[1])

    sc.add("a_jonah_air", doc(S.g(C.jonah(JAIR[0], JAIR[1], JS, 1, pose="fall"),
                                  transform=f"rotate({JAIR_ROT} {JAIR_C[0]:.1f} {JAIR_C[1]:.1f})")),
           z=13, motion=jonah_air)

    def wave_m(storm_layer):
        def m(t):
            a = storm(t)
            f = storm_fast(t)
            amp = a if storm_layer else (0.1 + 0.25 * (1 - stillness(t)) + 0.65 * a)
            return Tf(dx=(46 if storm_layer else 30) * amp * math.sin(2 * math.pi * t / 2.9),
                      dy=(16 if storm_layer else 5) * amp * math.sin(2 * math.pi * t / 1.7 + 0.8) +
                      (40 * (1 - f) if storm_layer else 0),
                      alpha=f if storm_layer else (1 - 0.85 * f) * progress(t, t_calm0 - 0.35, t_calm0, "linear"))
        return m

    sc.add("a_waves_calm", V.near_waves(False), z=20, motion=a_only(wave_m(False)))
    sc.add("a_waves_storm", V.near_waves(True), z=21, motion=a_only(wave_m(True)))

    px_, py_ = SPLASH[0], SPLASH[1] + 10
    sc.add("a_ripples", V.ripples(), z=22, motion=a_only(M.keys(
        [(t_impact + 0.15, {"sx": 0.3, "sy": 0.3, "alpha": 0}), (t_impact + 0.35, {"alpha": 0.9}),
         (t_impact + 3.4, {"sx": 1.45, "sy": 1.45, "alpha": 0})], ["out", "sine"], pivot=(px_, py_))))
    sc.add("a_splash", V.splash_crown(), z=23, motion=a_only(M.keys(
        [(t_impact - 0.04, {"sx": 0.6, "sy": 0.15, "alpha": 0}), (t_impact + 0.02, {"alpha": 1}),
         (t_impact + 0.2, {"sx": 1.0, "sy": 1.0}), (t_impact + 0.75, {"sx": 1.15, "sy": 0.55, "alpha": 0.8}),
         (t_impact + 1.05, {"sx": 1.2, "sy": 0.3, "alpha": 0})], ["out", "out", "in", "linear"], pivot=(px_, py_))))
    sc.add("a_drops", V.splash_drops(), z=24, motion=a_only(M.keys(
        [(t_impact, {"s": 0.25, "alpha": 0, "dy": 0}), (t_impact + 0.06, {"alpha": 1}),
         (t_impact + 0.5, {"s": 1.05, "dy": -10}), (t_impact + 0.95, {"s": 1.25, "dy": 70, "alpha": 0})],
        ["out", "linear", "in"], pivot=(px_, py_))))

    # ================================================================ shot B (drawn over A, fades in)
    sc.add("b_background", b_background(), z=100, wc=0.85, motion=b_only())
    sc.add("b_cloud", b_clouds(True), z=101, motion=b_only(M.drift(vx=9)))
    sc.add("b_sea_lines", b_sea_lines(0), z=102, wc=0,
           motion=b_only(lambda t: Tf(dx=22 * math.sin(2 * math.pi * t / 7.0), alpha=0.85)))
    sc.add("b_glints", [b_glints(k) for k in range(4)], z=103, wc=0, motion=b_only(),
           frame_at=lambda t: 1.5 + 1.5 * math.sin(2 * math.pi * t / 2.3))

    # gulls gliding across the sky
    gb = [doc(PR.gull(1880, 400, 0.5, -1, wing=w) + PR.gull(2010, 452, 0.42, -1, wing=-w * 0.8))
          for w in (1.0, 0.5, 0.0, -0.5, -1.0, -0.5, 0.0, 0.5)]
    t_gb = t_d0 - 1.0
    sc.add("b_gulls", gb, z=104, motion=b_only(lambda t: Tf(dx=-118 * (t - t_gb), dy=-6 * (t - t_gb) +
                                                         10 * math.sin(t * 0.9))),
           frame_at=lambda t: float(int(t * 8) % 8) if (t // 3) % 2 == 0 else 2.0)

    # the perched gull on the rail turns its head now and then (facing flip hidden by a hop)
    g_turns = [t_d1 + 2.6, t_d1 + 5.4, t_d1 + 7.9]
    sc.add("b_gull_perch", [doc(PR.gull(GULL_B[0], GULL_B[1], 0.62, f, pose="stand")) for f in (1, -1)], z=106,
           motion=b_only(lambda t: Tf(dy=-9 * sum(bump(t, g, 0.09) for g in g_turns))),
           frame_at=lambda t: float(sum(t >= g for g in g_turns) % 2))

    # light: the sun's halo pulses gently; at the vows the beams brighten (God is shown only as light)
    sc.add("b_sunglow", sun_glow(), z=107, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=0.55 + 0.15 * math.sin(2 * math.pi * t / 3.7) +
                                      0.3 * progress(t, t_vow - 0.2, t_vow + 1.2, "sine"),
                                      sx=1 + 0.04 * math.sin(2 * math.pi * t / 3.7), sy=1 + 0.04 * math.sin(2 * math.pi * t / 3.7),
                                      px=SUN_B[0], py=SUN_B[1])))
    sc.add("b_beams", b_beams(), z=107.5, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=0.5 * progress(t, t_vow - 0.2, t_vow + 1.4, "sine") *
                                      (0.85 + 0.15 * math.sin(2 * math.pi * t / 3.1)))))

    # ---- crew (back row first)
    def b_motion(pos, cuts, kneels, phase):
        x, y, s = pos

        def m(t):
            br = 1 + 0.011 * math.sin(2 * math.pi * (t / 3.3 + phase))
            dy = -7 * sum(bump(t, c) for c in cuts)
            sy = 1.0
            for tk in kneels:
                u = t - tk
                if -0.12 <= u < 0:
                    sy *= 1 - 0.06 * (u + 0.12) / 0.12
                elif 0 <= u < 0.16:
                    sy *= 1 - 0.035 * (1 - u / 0.16)
            return Tf(dy=dy, sx=br, sy=br * sy, px=x, py=y)
        return b_only(m)

    kn = [t_kn + 0.04 + 0.21 * i for i in range(5)]     # kneel order: captain, S0, S2, S3, S1
    vw = [t_vow + 0.13 * i for i in range(5)]           # vows: captain, S2, S0, S3, S1
    lk = [t_look + 0.1 * i for i in range(4)]           # look up: S2, S0, S3, S1

    sur = "surprised"
    st_s = C.POSES["stand"]
    # S1 (back, variant 1)
    sc.add("b_s1", b_frames("s", 1, B_S1, [(st_s, sur, None), (P_BOW, "sorry", None), (P_UP, "peaceful", None),
                                           (P_VOW, "happy", None)]), z=110,
           motion=b_motion(B_S1, [lk[3], vw[4]], [kn[4]], 0.1),
           frame_at=steps([(0, 0), (kn[4], 1), (lk[3], 2), (vw[4], 3)]))
    # S0 (back, variant 0): lifts his hands in wonder first
    sc.add("b_s0", b_frames("s", 0, B_S0, [(st_s, sur, None), (C.POSES["pray"], sur, None),
                                           (P_BOW, "peaceful", None), (P_UP, "peaceful", None),
                                           (P_VOW, "peaceful", None)]), z=111,
           motion=b_motion(B_S0, [t_see2, lk[1], vw[2]], [kn[1]], 0.45),
           frame_at=steps([(0, 0), (t_see2, 1), (kn[1], 2), (lk[1], 3), (vw[2], 4)]))

    # ---- the brazier, flame, the captain (in front of it), grain, glow, smoke
    sc.add("b_brazier", brazier(), z=112, motion=b_only())

    def flame_k(t):        # size of the fire: small, flares when the offering goes in, settles a little bigger
        return 0.72 + 0.62 * progress(t, t_flare, t_flare + 0.22, "out") - \
            0.3 * progress(t, t_flare + 0.3, t_flare + 1.6, "sine")

    def flame_m(t):
        k = flame_k(t)
        fl = math.sin(t * 13.0) * 0.5 + math.sin(t * 7.3 + 1) * 0.5
        kx = 1 + 0.35 * (k - 0.72)
        return Tf(sx=0.8 * kx * (1 + 0.03 * fl), sy=k * (1 + 0.06 * fl), px=FLAME_B[0], py=FLAME_B[1] + 4)
    sc.add("b_flame", [flame(i) for i in range(6)], z=113, wc=0.5, motion=b_only(flame_m),
           frame_at=lambda t: float(int(t * 9) % 6))

    capt_frames = b_frames("capt", None, B_CAPT, [(st_s, sur, None), (P_BOW, "peaceful", None),
                                                  (P_OFFER, "peaceful", "bowl"), (P_POUR, "peaceful", "pour"),
                                                  (P_VOW, "peaceful", None)])
    sc.add("b_capt", capt_frames, z=114, motion=b_motion(B_CAPT, [t_off0, t_pour, vw[0]], [kn[0]], 0.7),
           frame_at=steps([(0, 0), (kn[0], 1), (t_off0, 2), (t_pour, 3), (vw[0], 4)]))
    # grain pouring from the tipped bowl's lip into the coals
    _, hands = kfig("capt", None, *B_CAPT, P_POUR, "peaceful")
    sk = B_CAPT[2]
    hx, hy = (hands[0][0] + hands[1][0]) / 2 + 4 * sk, min(hands[0][1], hands[1][1]) - 22 * sk
    at = math.radians(POUR_TILT)
    lip = (hx + 34 * sk * 0.95 * math.cos(at), hy + 34 * sk * 0.95 * math.sin(at))
    sc.add("b_grain", [grains(k, lip) for k in range(3)], z=114.5,
           motion=b_only(lambda t: Tf(alpha=float(t_pour + 0.04 <= t < t_pour + 0.8))),
           frame_at=lambda t: float(int(t * 10) % 3))
    sc.add("b_glow", glow(), z=115, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=min(1.0, (0.5 + 0.08 * math.sin(t * 9.1)) * flame_k(t)),
                                      sx=0.8 + 0.3 * flame_k(t), sy=0.8 + 0.3 * flame_k(t),
                                      px=FLAME_B[0], py=FLAME_B[1] - 40)))

    # smoke: a soft swaying column (5 phases, crossfaded in a loop) that thickens at the offering, puffs that
    # drift off its top toward the sun, and one big billow at the flare
    def smoke_k(t):
        return 0.75 + 0.25 * progress(t, t_flare, t_flare + 0.9, "sine")

    col = [smoke_column(k / 4, tag="a") for k in range(4)]
    col.append(col[0])
    sc.add("b_smoke", col, z=116, wc=0.3,
           motion=b_only(lambda t: Tf(alpha=smoke_k(t), sx=0.9 + 0.12 * smoke_k(t), sy=0.75 + 0.3 * smoke_k(t),
                                      px=SMOKE_O[0], py=SMOKE_O[1])),
           frame_at=lambda t: (t * 0.7) % 4.0)

    NP, PER = 4, 4.2

    def puff_u(k, t):
        return ((t - t_d0) / PER + k / NP) % 1.0

    def puff_m(k):
        def m(t):
            u = puff_u(k, t)
            env = min(1.0, u / 0.25) * (1 - progress(u, 0.55, 1.0, "sine"))
            s = (0.7 + 1.5 * u) * (0.8 + 0.25 * smoke_k(t))
            x, y = smoke_xy(0.55 + 0.45 * u, 0.0)
            return Tf(dx=x - SMOKE_O[0] + 70 * u, dy=y - SMOKE_O[1] - 120 * u, rot=(24 if k % 2 else -24) * u,
                      sx=s, sy=s, alpha=0.75 * env * smoke_k(t), px=SMOKE_O[0], py=SMOKE_O[1])
        return m

    for k in range(NP):
        sc.add(f"b_puff{k}", [soft_puff(False, 80 + k), soft_puff(True, 80 + k)], z=116.1 + k * 0.01, wc=0.3,
               motion=b_only(puff_m(k)), frame_at=lambda t, k=k: progress(puff_u(k, t), 0.1, 0.6, "linear"))

    def billow_m(t):       # the big curl of smoke at the flare
        u = (t - t_flare + 0.1) / 3.4
        if u <= 0 or u >= 1:
            return Tf(alpha=0.0)
        s = 0.6 + 2.6 * u ** 0.75
        env = min(1.0, u / 0.1) * (1 - progress(u, 0.4, 1.0, "sine"))
        x, y = smoke_xy(min(1.0, 1.15 * u ** 0.85), 0.2)
        return Tf(dx=x - SMOKE_O[0] + 40 * u, dy=y - SMOKE_O[1] - 60 * u, rot=-30 * u, sx=s, sy=s,
                  alpha=0.95 * env, px=SMOKE_O[0], py=SMOKE_O[1])
    sc.add("b_billow", [soft_puff(False, 99, 40), soft_puff(True, 99, 40)], z=116.5, wc=0.3,
           motion=b_only(billow_m), frame_at=lambda t: progress((t - t_flare) / 3.4, 0.1, 0.6, "linear"))

    # ---- front row
    sc.add("b_s2", b_frames("s", 2, B_S2, [(st_s, sur, None), (P_BOW, "peaceful", None), (P_UP, "peaceful", None),
                                           (P_VOW, "happy", None)]), z=120,
           motion=b_motion(B_S2, [lk[0], vw[1]], [kn[2]], 0.25),
           frame_at=steps([(0, 0), (kn[2], 1), (lk[0], 2), (vw[1], 3)]))
    sc.add("b_s3", b_frames("s", 3, B_S3, [(C.POSES["point"], sur, None), (P_BOW, "sorry", None),
                                           (P_UP, "peaceful", None), (P_VOW, "peaceful", None)]), z=121,
           motion=b_motion(B_S3, [lk[2], vw[3]], [kn[3]], 0.6),
           frame_at=steps([(0, 0), (kn[3], 1), (lk[2], 2), (vw[3], 3)]))
    sc.add("b_fore", b_foreground(), z=130, motion=b_only())

    # ================================================================ camera
    A0 = (1000.0, 590.0, 1700.0)
    A1 = (945.0, 634.0, 1560.0)
    B0 = (965.0, 688.0, 1470.0)
    B1 = (1010.0, 682.0, 1396.0)
    t_p0 = t_still - 0.2
    tE = min(T - 0.6, c2b.end + 0.3)

    def path(i):           # continuous velocity: ease into the push, keep moving through the dissolve, then drift
        vd = (B0[i] - A1[i]) / (t_d1 - t_d0)
        vb = (B1[i] - B0[i]) / (tE - t_d1)
        return hermite([(0.0, A0[i], 0.0), (t_p0, A0[i], 0.0), (t_d0, A1[i], 0.8 * vd),
                        (t_d1, B0[i], 0.5 * (vd + vb) * 0.5 + 0.5 * vb), (tE, B1[i], 0.0)])
    cx_, cy_, cw_ = path(0), path(1), path(2)

    def camera(t):
        a = storm(t)
        return Cam(cx_(t) + 6 * a * math.sin(2 * math.pi * t / 3.3), cy_(t) + 7 * a * math.sin(2 * math.pi * t / 2.4),
                   cw_(t), 0.45 * a * math.sin(2 * math.pi * t / 2.9))
    sc.camera = camera

    # ================================================================ effects
    sc.fx = [
        FX.lightning([t_flash], strength=0.22),
        FX.rain(t0=-1, t1=t_calm0 + 0.45, density=0.85, angle=16, alpha=105),
        V.bubble_fx([(lambda t: (SPLASH[0], WL + 110), t_impact + 0.03, t_impact + 0.45, 60, 170, (6, 18), 70, 210)]),
        # '浪也静了': glints on the flat sea (away from the ship), gone during the dissolve
        FX.sparkles((1260, 720, 2050, 870), count=16, t0=t_still, t1=t_d0 + 0.5, color=(255, 250, 226),
                    size=(5, 11), period=1.2, drift=0, seed=31),
        # deck: dust motes in the sunbeams, sparks at the flare, warm sparkles in the light at the vows
        FX.motes((700, 300, 1800, 1000), count=34, t0=t_d1 - 0.3, color=(255, 244, 206), size=(2.5, 5.5), alpha=120,
                 seed=17),
        sparks_fx((FLAME_B[0], FLAME_B[1] - 70), t_flare - 0.05, t_flare + 1.3, 22),
        sparks_fx((FLAME_B[0], FLAME_B[1] - 50), t_d1, T + 1, 1.6, seed=9),
        FX.sparkles((1270, 290, 1880, 640), count=18, t0=t_vow - 0.1, t1=T + 2, color=(255, 236, 170),
                    size=(7, 16), period=1.6, drift=-6, seed=41),
    ]

    # ================================================================ sound
    sc.sfx("storm_wind", 0, dur=t_wind + 0.2, gain_db=-14, fade_in=0.8, fade_out=1.6)
    sc.sfx("rain", 0, dur=t_calm0 + 0.6, gain_db=-16, fade_in=0.8, fade_out=0.6)
    sc.sfx("waves_storm", 0, dur=t_calm1 + 0.3, gain_db=-12, fade_in=0.8, fade_out=1.5)
    sc.sfx("ship_creak", 0, dur=t_calm1, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("thunder", t_flash - 0.02, gain_db=-18, pan=-0.3)
    sc.sfx("cloth", t_grab - 0.05, gain_db=-15, pan=0.0)
    sc.sfx("cloth", t_lift - 0.05, gain_db=-12, pan=0.05)
    sc.sfx("whoosh", t_launch + 0.02, gain_db=-11, pan=0.3)
    sc.sfx("splash", t_impact - 0.02, gain_db=-8, pan=0.4)
    sc.sfx("bubbles", t_impact + 0.08, dur=0.9, gain_db=-17, pan=0.4, fade_out=0.4)
    sc.sfx("waves_calm", t_calm0 - 0.2, dur=T - t_calm0 + 1.0, gain_db=-14, fade_in=0.9, fade_out=0.8)
    sc.sfx("chime", t_calm0 + 0.3, gain_db=-15)
    sc.sfx("gull", t_gull + 0.4, gain_db=-18, pan=0.5)
    sc.sfx("wind_soft", t_d0 - 0.4, dur=T - t_d0 + 1.2, gain_db=-20, fade_in=1.0, fade_out=0.8)
    sc.sfx("fire", t_d0, dur=T - t_d0 + 0.8, gain_db=-17, fade_in=1.0, fade_out=0.8)
    sc.sfx("fire", t_flare - 0.05, dur=2.4, gain_db=-12, fade_in=0.1, fade_out=1.4)
    sc.sfx("cloth", kn[0] - 0.05, gain_db=-17)
    sc.sfx("cloth", kn[3] - 0.05, gain_db=-18)
    sc.sfx("sparkle", t_flare - 0.02, gain_db=-14, pan=0.3)
    sc.sfx("gull", g_turns[0] - 0.1, gain_db=-20, pan=0.5)
    sc.sfx("chime", t_vow, gain_db=-14, pan=0.2)
    return sc
