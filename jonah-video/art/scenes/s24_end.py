"""Scene 24 (v2) — closing page: how would you answer? God's love is wider than the sea, higher than the sky.

One wide sunset double-page spread on a 3300 x 1860 stage (no cuts). It is the approved v1 spread
(art/scenes_v1/s13_end.py: art and motion techniques copied here and re-laid out), widened to the left and
heightened, so the full spread now shows both peoples:
  * LEFT: Israel's green coast hills (soft terraces, olive trees, sheep, a path down to the bay, a little village
    of flat-roofed houses on the summit, a lavender ridge behind) with four Israelites on a grassy knoll;
  * LEFT-CENTRE: the calm bay under the setting sun, its golden glitter path, the little ship with its three
    sailors and the great fish leaping out of the mid sea band (about twice the ship's length);
  * CENTRE: Jonah on his grassy hill;
  * RIGHT: the golden plain and Nineveh glowing in the last light, five Ninevites come forward on the plain
    toward Jonah (both peoples are drawn large enough to read on a phone: Israelites ~0.41, Ninevites ~0.34);
  * ABOVE: a huge dusk sky — sunset gradient, layered evening clouds, later the evening star and first stars.

Timing (every beat keyed to the subtitle chunk that holds its phrase; ``when()`` places a phrase inside a chunk
by its character position and snaps it to the matching comma pause found in the voice file):
  * opening: dip through the blank warm page (as v1, timed from the timeline's xfade), so s23's Jonah and this one
    never share a frame. Jonah stands on the left third looking east at Nineveh and its people (in dusk shade).
  * line 0 "约拿是怎么回答的呢？" — a big hand-lettered "?" pops up beside Jonah's head; "圣经没有告诉我们" —
    Jonah puts his hand to his chin, pondering.
  * line 1 "如果你是约拿" — the camera pushes in slowly on him; "你会怎么回答上帝呢？" — he looks up to the sky,
    the "?" swells and glows, warm light gathers round him and a few sparkles drift down. The 2.5 s pause is a
    quiet hold (breathing, blinking, sea and clouds moving) for the child to think.
  * line 2 "上帝的爱" — the "?" bursts into golden sparkles, Jonah lowers his hand and smiles, the camera starts to
    pull back; "比大海还要宽" — it widens west over the sea while the great fish leaps across the sun's path;
    "比天空还要高" — it tilts up to the full spread and the sun's rays fan out up to the top of the sky.
    "他爱以色列人" — warm light blooms over Israel's headland, the Israelites light up and wave; "也爱尼尼微人"
    — the same over Nineveh, the Ninevites wave; "他爱约拿" — a glow and a warm rim light on Jonah, who puts his
    hand on his heart, smiling up into the light; "也爱你和我" — the camera eases closer and little hearts float
    up from the bottom of the page (from "you and me").
  * line 3 "我们做错了事" — dusk starts to deepen over the sky (the rays dim under it); "只要回到上帝身边" — two
    doves fly home out of the east and land beside Jonah, who closes his eyes in the warm light;
    "他总会给我们重新开始的机会" — he opens them, smiling; the evening star comes out, then the first stars (with
    a few twinkling ones), and the great fish leaps once more past the ship while a sailor waves.
  * line 4 "上帝也希望我们像他一样" — calm wide hold, Jonah stands looking at the city, smiling;
    "爱惜身边的每一个人" — a warm glow lights up behind every single person, one after another, and lamps come on
    in the houses, from Israel's village across to Nineveh;
    "连我们不喜欢的人也一样" — both peoples wave to each other, and one dove from Israel and one from Nineveh fly
    toward each other (the Nineveh one arcs over Jonah's head) and land side by side, facing each other, in front
    of Jonah; a tiny heart pops above them.
  * end of the narration: the hand-lettered end card '约拿的故事 · 完' fades in high in the sky, a swash is drawn
    out from its centre and a small heart pops in (chime). The film then fades out (assemble.py).
Pose / face changes are hard switches sold by a small squash (never crossfaded doubles), each held >= 0.5 s.
Camera: one continuous move through monotone-cubic keys (v1), peak < ~19 output px / frame, always inside the stage.
Cost: the sunset rays are painted into the sky layer (a 4-drawing flipbook: their outward reveal, then the same
rays at half strength as evening falls) and the sky stops at the horizon; the near sea is static and flattened with
the land.
Library gaps worked around here: characters.py has no per-expression blink (local eyes-closed copies of 'happy' and
'neutral' are registered in C.EXPRS), and fx.sparkles measures its drift from the scene start, not from t0
(sparkles_from() shifts the rect to compensate).
"""
import bisect
import math
import random

import numpy as np
from scipy import ndimage

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene

SW, SH = 3300, 1860
DX, DY = 400, 195        # where the approved v1 spread (2800 x 1620) sits inside this stage

HORIZON = 955 + DY       # 1150 sea horizon
MID_WL = 1022 + DY       # waterline of the mid sea band (the ship sails on it)
NEAR_WL = 1180 + DY      # waterline of the near sea band
SUN = (1150, 1110)       # setting sun (sinks SUN_SINK px during the scene)
SUN_R = 92
SUN_SINK = 74
JONAH_X = 1400 + DX      # 1800
JONAH_S = 0.8
CITY_X0, CITY_X1, CITY_Y, CITY_S = 1770 + DX, 2690 + DX, 986 + DY, 0.5
CARD_X, CARD_Y = 1690, 560   # end-card text baseline centre

# the ship sails slowly west; its stern (SHIP_X + 113) stays >= 50 stage px (64 output px in the opening framing)
# clear of Jonah's back, and its bow (SHIP_X - 100) clear of the first leap's rising tail
SHIP_X, SHIP_S, SHIP_VX = 1580, 0.19, -1.5
FISH_S = 0.32            # leaps from the MID band (same depth as the ship): ~2x the ship's length
SPLASH_K = 0.8

ISR_FOOT = NEAR_WL + 28  # waterline of Israel's coast (it stands in the near sea band)
# crest of Israel's hills (left): a soft summit with the village, a dip, a grassy knoll where the Israelites
# stand, then a long slope down to the bay
ISR_KEYS = ((-220, 1004), (-40, 975), (120, 962), (260, 978), (390, 1022), (500, 1040), (580, 1036),
            (670, 1042), (770, 1100), (880, 1230), (980, 1345), (1050, ISR_FOOT))

PAPER_RGB = (243, 233, 210)   # the compositor's blank-page base colour
XFADE_DEFAULT = 1.0           # the cross-dissolve into this scene (read from the timeline when available)

PUNCT = "，。；：？！、,.;:?!"

# Blink drawings that close only the eyes: characters.py has no per-expression blink helper, so register local
# eyes-closed copies of the expressions Jonah blinks from (a blink from 'happy' must keep the open grin, and one
# from 'neutral' its brows). setdefault keeps it idempotent and leaves the shared expressions untouched.
C.EXPRS.setdefault("e24_blink_happy", dict(C.EXPRS["happy"], eyes="closed"))
C.EXPRS.setdefault("e24_blink_neutral", dict(C.EXPRS["neutral"], eyes="closed"))
BLINK_EXPR = {"happy": "e24_blink_happy", "neutral": "e24_blink_neutral"}


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ timing helpers


_PAUSES = {}


def _pauses(ctx, i):
    """Silent gaps (absolute s) inside utterance i, found in its voice file; [] if it cannot be read."""
    key = (ctx.id, i, round(ctx.lines[i].start, 3))
    if key in _PAUSES:
        return _PAUSES[key]
    out = []
    try:
        import soundfile as sf
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"), dtype="float32")
        if x.ndim == 2:
            x = x.mean(axis=1)
        hop = sr // 100
        nb = len(x) // hop
        e = np.sqrt((x[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1))
        env = np.convolve(e, np.ones(5) / 5, "same")
        quiet = env < 0.04 * env.max()
        st = None
        for k, q in enumerate(list(quiet) + [False]):
            if q and st is None:
                st = k
            elif not q and st is not None:
                if k - st >= 8 and st > 0:
                    out.append((ctx.lines[i].start + st / 100, ctx.lines[i].start + k / 100))
                st = None
    except Exception:
        out = []
    _PAUSES[key] = out
    return out


def when(ctx, phrase, fallback=None):
    """Start time of ``phrase``: the start of its subtitle chunk if it opens one; otherwise its character position
    inside the chunk, snapped to the end of the comma pause just before it (from the voice file).
    ``fallback`` = (line index, fraction of the line) if the phrase is not in the script any more."""
    for i, ln in enumerate(ctx.lines):
        for ch in (ln.chunks or []):
            if phrase not in ch.text:
                continue
            k = ch.text.index(phrase)
            if k == 0:
                return ch.start
            body = ch.text.rstrip(PUNCT)

            def w(s):
                return sum(0.5 if c in PUNCT else 1.0 for c in s)
            est = ch.start + (ch.end - ch.start) * w(ch.text[:k]) / max(1.0, w(body))
            if ch.text[k - 1] in PUNCT:
                near = [b for a, b in _pauses(ctx, i) if abs(b - est) < 0.4]
                if near:
                    return min(near, key=lambda b: abs(b - est))
            return est
        if phrase in ln.text and not ln.chunks:
            return ln.start + (ln.end - ln.start) * ln.text.index(phrase) / max(1, len(ln.text))
    if fallback is None:
        raise KeyError(phrase)
    li, fr = fallback
    li = min(li, len(ctx.lines) - 1)
    ln = ctx.lines[li]
    return ln.start + fr * (ln.end - ln.start)


def smooth_keys(keys):
    """Monotone cubic (Fritsch-Carlson) interpolation through (t, v) keys (v1 s13_end)."""
    ts = [k[0] for k in keys]
    vs = [k[1] for k in keys]
    n = len(keys)
    d = [(vs[i + 1] - vs[i]) / (ts[i + 1] - ts[i]) for i in range(n - 1)]
    m = [0.0] * n
    for i in range(1, n - 1):
        if d[i - 1] * d[i] > 0:
            h0, h1 = ts[i] - ts[i - 1], ts[i + 1] - ts[i]
            w1, w2 = 2 * h1 + h0, h1 + 2 * h0
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])

    def f(t):
        if t <= ts[0]:
            return vs[0]
        if t >= ts[-1]:
            return vs[-1]
        i = min(n - 2, bisect.bisect_right(ts, t) - 1)
        h = ts[i + 1] - ts[i]
        s = (t - ts[i]) / h
        h00, h10 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s
        h01, h11 = -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
        return h00 * vs[i] + h10 * h * m[i] + h01 * vs[i + 1] + h11 * h * m[i + 1]
    return f


def bez3(p0, c1, c2, p3, u):
    v = 1 - u
    a, b, c, d = v * v * v, 3 * v * v * u, 3 * v * u * u, u * u * u
    return (a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1])


# ============================================================================ ground lines


def hill_y(x):
    """Ground line of Jonah's hill (v1 shape)."""
    base = 1100 + DY + 0.00024 * (x - JONAH_X) ** 2
    k = min(1.0, max(0.0, (abs(x - JONAH_X) - 260) / 320))
    return base + k * 16 * math.sin((x - JONAH_X) / 150.0)


_ISR_F = smooth_keys(ISR_KEYS)


def isr_y(x):
    """Crest line of Israel's hills (left)."""
    k = min(1.0, max(0.0, (900 - x) / 200))
    return _ISR_F(x) + 3 * k * math.sin(x / 55.0)


# ============================================================================ sky


SKY_BOTTOM = HORIZON + 70   # the sky layer stops here: below it the sea and the land always cover the stage


def sky_svg(rays=0.0, ray_op=1.0):
    """Sunset sky (gradient, sun halo, glow over the city, far streaks and puffs). rays 0 / 0.5 / 1: the sun's
    golden rays painted in (screen blend), 0.5 = only out to ~half the sky (a step of the outward reveal).
    ray_op < 1: the same full-reach rays, weaker (they fade as evening falls)."""
    defs = (f'<linearGradient id="e24sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{HORIZON + 40}">'
            '<stop offset="0" stop-color="#323d6b"/>'
            '<stop offset="0.2" stop-color="#4d4f86"/>'
            '<stop offset="0.37" stop-color="#7a63a0"/>'
            '<stop offset="0.52" stop-color="#b47ea6"/>'
            '<stop offset="0.66" stop-color="#e0918b"/>'
            '<stop offset="0.78" stop-color="#f3a873"/>'
            '<stop offset="0.9" stop-color="#f8c584"/>'
            '<stop offset="1" stop-color="#fbe1a6"/></linearGradient>' +
            S.rad_grad("e24sunhalo", [(0, "#fff4c8", 0.95), (0.18, "#ffe3a0", 0.7), (0.5, "#ffc888", 0.28),
                                      (1, "#ffb880", 0)]) +
            S.rad_grad("e24cityglow", [(0, "#ffd9a0", 0.55), (0.6, "#f8c08e", 0.2), (1, "#f8c08e", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOTTOM + 20}" fill="url(#e24sky)"/>'
            f'<ellipse cx="{SUN[0]}" cy="{SUN[1] + 20}" rx="1150" ry="600" fill="url(#e24sunhalo)"/>'
            f'<ellipse cx="2630" cy="{CITY_Y - 76}" rx="760" ry="300" fill="url(#e24cityglow)"/>')
    rng = random.Random(21)
    streaks = ""
    for cx, cy, w, h, col, op in ((330, 810, 520, 16, "#ffe2a6", 0.75), (980, 850, 640, 14, "#ffd79a", 0.6),
                                  (1500, 792, 480, 12, "#f9c6a0", 0.55), (2050, 750, 700, 16, "#f6b9a6", 0.5),
                                  (2550, 820, 420, 12, "#f9cba3", 0.55), (700, 750, 380, 10, "#ffd8a0", 0.5),
                                  (-180, 790, 420, 12, "#ffd8a0", 0.5)):
        for k in range(3):
            streaks += (f'<ellipse cx="{f1(cx + DX + rng.uniform(-60, 60))}" cy="{f1(cy + DY + k * 13)}" '
                        f'rx="{f1(w / 2 * rng.uniform(0.6, 1.0))}" ry="{f1(h * rng.uniform(0.6, 1.0))}" '
                        f'fill="{col}" opacity="{op}"/>')
    body += S.g(streaks, filter="soft")
    high, hdefs = clouds_svg("high")
    body += high
    if rays > 0:
        r_body, r_defs = rays_markup(rays, ray_op)
        body += r_body
        defs += r_defs
    clip = f'<clipPath id="e24skyclip"><rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOTTOM + 20}"/></clipPath>'
    return doc(f'<g clip-path="url(#e24skyclip)">{body}</g>', defs + hdefs + clip)


DUSK_H = 900


def dusk_svg():
    """Deepening indigo at the top of the sky (comes with the first stars)."""
    defs = (f'<linearGradient id="e24dusk" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{DUSK_H}">'
            '<stop offset="0" stop-color="#1c2550" stop-opacity="0.66"/>'
            '<stop offset="0.5" stop-color="#2b3263" stop-opacity="0.3"/>'
            '<stop offset="1" stop-color="#2b3263" stop-opacity="0"/></linearGradient>')
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{DUSK_H + 20}" fill="url(#e24dusk)"/>', defs)


def star_path(x, y, r, w=0.24):
    k = r * w
    return (f"M{f1(x)},{f1(y - r)} L{f1(x + k)},{f1(y - k)} L{f1(x + r)},{f1(y)} L{f1(x + k)},{f1(y + k)} "
            f"L{f1(x)},{f1(y + r)} L{f1(x - k)},{f1(y + k)} L{f1(x - r)},{f1(y)} L{f1(x - k)},{f1(y - k)} Z")


def stars_svg(seeds=((1, 5, 14), (11, 4, 13), (23, 4, 13))):
    body = ""
    for seed, n_big, n_small in seeds:
        body += _stars_markup(seed, n_big, n_small)
    return doc(body)


def _stars_markup(seed, n_big, n_small):
    rng = random.Random(seed)
    body = ""
    placed = tries = 0
    while placed < n_big + n_small and tries < 6000:
        tries += 1
        x, y = rng.uniform(140, SW - 140), rng.uniform(150, 760 - rng.uniform(0, 140))
        if not star_ok(x, y, 8 if placed < n_big else 0):
            continue
        if placed < n_big:
            r = rng.uniform(10, 16)
            body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.9)}" fill="#fff3cc" opacity="0.25"/>'
            body += f'<path d="{star_path(x, y, r)}" fill="#fff7dc"/>'
        else:
            body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(2.0, 3.6))}" fill="#fff4d4"/>'
        placed += 1
    return body


EV_STAR = (1290, 770)   # clear of the drifting inked cloud at (870, 835) all scene long, and of the end card


def evening_star_svg(x, y):
    body = (f'<circle cx="{x}" cy="{y}" r="36" fill="#fff2c4" opacity="0.22"/>'
            f'<circle cx="{x}" cy="{y}" r="18" fill="#fff4cf" opacity="0.4"/>'
            f'<path d="{star_path(x, y, 32, 0.14)}" fill="#fffae6"/>'
            f'<path d="{star_path(x, y, 16, 0.3)}" fill="#fffdf2" transform="rotate(45 {x} {y})"/>')
    return doc(body)


def sun_svg():
    x, y = SUN
    defs = S.rad_grad("e24sun", [(0, "#fff6d2"), (0.55, "#fde08a"), (1, "#f7b24c")])
    body = (f'<circle cx="{x}" cy="{y}" r="{SUN_R + 70}" fill="#ffe6a8" opacity="0.35" filter="url(#soft)"/>'
            + S.g(f'<circle cx="{x}" cy="{y}" r="{SUN_R}" fill="url(#e24sun)" stroke="#f0a24a" '
                  f'stroke-width="4"/>', filter="wobble"))
    return doc(body, defs)


def sunset_cloud(cx, cy, w, h, seed, top, lit):
    gid = f"e24c{seed}"
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="0.55" stop-color="{S.mix(top, lit, 0.45)}"/>'
            f'<stop offset="1" stop-color="{lit}"/></linearGradient>')
    body = S.cloud(cx, cy, w, h, f"url(#{gid})", seed=seed, sw=2.5)
    body += (f'<path d="M{f1(cx - w * 0.38)},{f1(cy + h * 0.36)} Q{f1(cx)},{f1(cy + h * 0.53)} '
             f'{f1(cx + w * 0.38)},{f1(cy + h * 0.36)}" stroke="#fff0c0" stroke-width="{f1(max(4, h * 0.07))}" '
             f'fill="none" stroke-linecap="round" opacity="0.8"/>')
    return body, defs


def soft_cloud(cx, cy, w, h, seed, top, lit, op=0.85):
    gid = f"e24s{seed}"
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{lit}"/></linearGradient>')
    body = f'<g opacity="{op}">' + S.cloud(cx, cy, w, h, f"url(#{gid})", seed=seed, sw=0) + "</g>"
    return body, defs


def streak_cloud(cx, cy, w, h, col, op, seed):
    rng = random.Random(seed)
    body = ""
    for k in range(4):
        body += (f'<ellipse cx="{f1(cx + rng.uniform(-0.18, 0.18) * w)}" cy="{f1(cy + (k - 1.5) * h * 0.55)}" '
                 f'rx="{f1(w / 2 * rng.uniform(0.45, 0.95))}" ry="{f1(h * rng.uniform(0.45, 0.8))}" fill="{col}" '
                 f'opacity="{op * rng.uniform(0.7, 1.0):.2f}"/>')
    return f'<g filter="url(#soft)">{body}</g>'


# soft ink-less puffs (stage px): the two high ones are painted into the sky layer, the low one drifts with the
# inked clouds
SOFT_CLOUDS = ((1880 + DX, 735 + DY, 210, 48, 7, "#cf9db6", "#fbc9a0", 0.8),
               (210 + DX, 330 + DY, 230, 58, 4, "#a48cba", "#dcabbb", 0.7),
               (2860 + DX, 250 + DY, 250, 56, 9, "#9c88ba", "#cfa6bf", 0.6))
# high far streaks (cx, cy, w, h, colour, opacity, seed), painted into the sky layer
STREAKS = ((2540 + DX, 240 + DY, 560, 16, "#b8a0c8", 0.75, 1), (400 + DX, 165 + DY, 440, 13, "#a996c4", 0.7, 2),
           (2290 + DX, 330 + DY, 300, 10, "#c7a6c4", 0.6, 3), (380, 230, 520, 14, "#9e8fc0", 0.6, 4),
           (2950, 170, 480, 13, "#9a8cc0", 0.55, 5))


def _keep_out():
    """Ellipses (cx, cy, rx, ry) round everything in the sky that stars must not be drawn over: the high soft
    puffs and streaks baked into the sky layer below the star field (S.cloud reaches ~0.4w + 0.86h sideways and
    from cy - 1.15h to cy + 0.52h; a streak ~0.66w by 1.6h, plus its soft blur)."""
    out = []
    for cx, cy, w, h, *_ in SOFT_CLOUDS:
        if cy <= 600 + DY:
            out.append((cx, cy - 0.32 * h, max(0.52 * w, 0.4 * w + 0.86 * h) + 22, 0.84 * h + 22))
    for cx, cy, w, h, *_ in STREAKS:
        out.append((cx, cy, 0.66 * w + 16, 1.6 * h + 18))
    return out


SKY_KEEP_OUT = _keep_out()


def star_ok(x, y, margin=0.0):
    """True if a star at (x, y) stays clear of the end-card box and of the high clouds and streaks."""
    if CARD_X - 700 < x < CARD_X + 700 and CARD_Y - 230 < y < CARD_Y + 175:   # keep the end card clean
        return False
    for cx, cy, rx, ry in SKY_KEEP_OUT:
        if ((x - cx) / (rx + margin)) ** 2 + ((y - cy) / (ry + margin)) ** 2 < 1.0:
            return False
    return True


def clouds_svg(part="low"):
    """v1's evening clouds moved into this stage, plus a cloud over Israel's hills and higher streaks for the
    taller sky (all clear of the end-card box). part 'high' = the far ink-less streaks and puffs (static, painted
    into the sky layer); 'low' = the inked sunset clouds and one soft puff (a slowly drifting layer)."""
    inked, defs = "", ""
    for cx, cy, w, h, seed, top, lit in (
            (470, 640, 330, 84, 11, "#c497b4", "#f4c2a4"),
            (300, 695, 480, 108, 3, "#d9a3b6", "#ffd9a0"),
            (2590, 545, 330, 86, 12, "#ab8db6", "#e8b4ac"),
            (2400, 600, 520, 112, 2, "#b993b8", "#f7c1a2"),
            (1030, 772, 250, 58, 5, "#dca3b2", "#ffdca0"),
            (-220, 610, 380, 92, 14, "#c095b4", "#f2bea6")):
        b, d = sunset_cloud(cx + DX, cy + DY, w, h, seed, top, lit)
        inked += b
        defs += d
    soft, high = "", ""
    for cx, cy, w, h, seed, top, lit, op in SOFT_CLOUDS:
        b, d = soft_cloud(cx, cy, w, h, seed, top, lit, op)
        if cy > 600 + DY:
            soft += b
        else:
            high += b
        defs += d
    high = "".join(streak_cloud(*st) for st in STREAKS) + high
    if part == "high":
        return high, defs
    return doc(soft + S.g(inked, filter="wobble"), defs)


def rays_markup(reach=1.0, op=1.0):
    """Soft golden rays fanning up from the sun over the sky, screen-blended into the sky layer. reach < 1 masks
    them to a disc round the sun (a step of the outward reveal on '比天空还要高')."""
    sx, sy = SUN
    defs = (f'<radialGradient id="e24ray" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="2500">'
            '<stop offset="0" stop-color="#ffd890" stop-opacity="0.44"/>'
            '<stop offset="0.5" stop-color="#ffcf88" stop-opacity="0.21"/>'
            '<stop offset="1" stop-color="#ffcf88" stop-opacity="0.05"/></radialGradient>' +
            S.rad_grad("e24warm", [(0, "#ffcf87", 0.36), (0.3, "#ffb874", 0.15), (1, "#ffb070", 0)]))
    rng = random.Random(8)
    d = ""
    for i in range(11):
        a = math.radians(-178 + i * 17.6 + rng.uniform(-4, 4))
        wa = math.radians(rng.uniform(2.2, 3.6))
        r0, r1 = SUN_R + 60, 2700
        pts = [(sx + r0 * math.cos(a - wa / 3), sy + r0 * math.sin(a - wa / 3)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 3), sy + r0 * math.sin(a + wa / 3))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    body = (f'<ellipse cx="{sx}" cy="{sy}" rx="1500" ry="800" fill="url(#e24warm)"/>'
            f'<path d="{d}" fill="url(#e24ray)" filter="url(#blur-md)"/>')
    mask = ""
    if reach < 1.0:
        rr = 700 + 900 * reach
        defs += (f'<radialGradient id="e24raymg{int(reach * 100)}" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" '
                 f'r="{rr}"><stop offset="0" stop-color="#fff"/><stop offset="0.55" stop-color="#fff"/>'
                 f'<stop offset="1" stop-color="#000"/></radialGradient>'
                 f'<mask id="e24raym{int(reach * 100)}" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{SW + 100}" '
                 f'height="{SH + 100}"><rect x="-50" y="-50" width="{SW + 100}" height="{SH + 100}" '
                 f'fill="url(#e24raymg{int(reach * 100)})"/></mask>')
        mask = f' mask="url(#e24raym{int(reach * 100)})"'
    op_attr = f' opacity="{op:.2f}"' if op < 1.0 else ""
    return f'<g style="mix-blend-mode:screen"{mask}{op_attr}>{body}</g>', defs


# ============================================================================ sea (v1)


def _sea_strokes():
    rng = random.Random(5)
    far, mid = "", ""
    for _ in range(34):
        x = rng.uniform(-20, 2050)
        y = rng.uniform(HORIZON + 10, MID_WL - 12)
        ln = rng.uniform(30, 90) * (0.6 + (y - HORIZON) / 140)
        far += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-4 {f1(ln)},0" stroke="#f6dcc8" stroke-width="2.5" '
                f'fill="none" stroke-linecap="round" opacity="0.6"/>')
    for _ in range(40):
        x = rng.uniform(-20, 2100)
        y = rng.uniform(MID_WL + 18, NEAR_WL - 10)
        ln = rng.uniform(40, 120)
        mid += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-6 {f1(ln)},0" stroke="#d9c6e0" stroke-width="3" '
                f'fill="none" stroke-linecap="round" opacity="0.55"/>')
    return far, mid


def sea_far_svg():
    defs = (f'<linearGradient id="e24far" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#e4b0a6"/><stop offset="0.12" stop-color="#ad8fad"/>'
            '<stop offset="0.4" stop-color="#6d7aa6"/><stop offset="1" stop-color="#46578a"/></linearGradient>' +
            S.rad_grad("e24seaglow", [(0, "#ffe2a4", 0.55), (0.5, "#f9c495", 0.2), (1, "#f9c495", 0)]))
    far_h = MID_WL + 45 - HORIZON
    far = f'<rect x="-20" y="{HORIZON}" width="{SW + 40}" height="{far_h}" fill="url(#e24far)"/>'
    far += (f'<clipPath id="e24farclip"><rect x="-20" y="{HORIZON}" width="{SW + 40}" height="{far_h}"/></clipPath>'
            f'<ellipse cx="{SUN[0]}" cy="{HORIZON + 40}" rx="760" ry="120" fill="url(#e24seaglow)" '
            f'clip-path="url(#e24farclip)"/>')
    far += (f'<path d="M-20,{HORIZON} L{SW + 20},{HORIZON}" stroke="{P["ink"]}" stroke-width="2.5" '
            f'opacity="0.6"/>')
    strokes, _ = _sea_strokes()
    return doc(S.g(far, filter="wobble") + S.g(strokes, filter="wobble-fine"), defs)


def sea_mid_svg():
    defs = (f'<linearGradient id="e24mid" gradientUnits="userSpaceOnUse" x1="0" y1="{MID_WL}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#9886ae"/><stop offset="0.3" stop-color="#6879a6"/>'
            '<stop offset="1" stop-color="#3f5285"/></linearGradient>')
    mid = S.path(S.wave_band(MID_WL, 4, 300, 0.7, x0=-60, x1=2160, bottom=NEAR_WL + 45), fill="url(#e24mid)", sw=3)
    crest = S.path(S.wave_line(MID_WL - 3, 4, 300, 0.7, x0=-60, x1=2160), stroke=False,
                   extra='stroke="#fbe6c8" stroke-width="4" fill="none" opacity="0.55"')
    _, strokes = _sea_strokes()
    return doc(S.g(mid + crest, filter="wobble") + S.g(strokes, filter="wobble-fine"), defs)


def glitter_svg(seed, y0=HORIZON + 6, y1=NEAR_WL - 6):
    rng = random.Random(seed)
    body = ""
    y = HORIZON + 6
    while y < NEAR_WL - 6:
        half = 26 + (y - HORIZON) * 0.55
        n = 2 + int((y - HORIZON) / 60)
        for _ in range(n):
            x = SUN[0] + rng.uniform(-half, half)
            ln = rng.uniform(10, 26) * (0.7 + (y - HORIZON) / 180)
            op = rng.uniform(0.55, 0.95)
            if y0 <= y < y1:
                body += (f'<rect x="{f1(x - ln / 2)}" y="{f1(y)}" width="{f1(ln)}" '
                         f'height="{f1(3 + (y - HORIZON) / 90)}" rx="2" fill="#ffe9a8" opacity="{op:.2f}"/>')
        y += 7 + (y - HORIZON) * 0.05
    return doc(body)


def near_sea_svg():
    defs = (f'<linearGradient id="e24near" gradientUnits="userSpaceOnUse" x1="0" y1="{NEAR_WL}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#6a75a6"/><stop offset="0.45" stop-color="#4b5c8e"/>'
            '<stop offset="1" stop-color="#36487a"/></linearGradient>')
    band = S.path(S.wave_band(NEAR_WL, 6, 360, 1.9, x0=-80, x1=1900, bottom=SH + 60), fill="url(#e24near)", sw=3.5)
    crest = S.path(S.wave_line(NEAR_WL - 4, 6, 360, 1.9, x0=-80, x1=1900), stroke=False,
                   extra='stroke="#fbe6c8" stroke-width="5" fill="none" opacity="0.6"')
    rng = random.Random(9)
    body = ""
    y = NEAR_WL + 10
    while y < SH:
        half = 26 + (y - HORIZON) * 0.55
        for _ in range(3 + int((y - NEAR_WL) / 70)):
            x = SUN[0] + rng.uniform(-half, half)
            ln = rng.uniform(18, 46)
            body += (f'<rect x="{f1(x - ln / 2)}" y="{f1(y)}" width="{f1(ln)}" height="5" rx="2.5" fill="#ffe2a0" '
                     f'opacity="{rng.uniform(0.45, 0.85):.2f}"/>')
        y += 16
    for _ in range(30):
        x = rng.uniform(-60, 1800)
        yy = rng.uniform(NEAR_WL + 30, SH - 30)
        ln = rng.uniform(60, 150)
        body += (f'<path d="M{f1(x)},{f1(yy)} q{f1(ln / 2)},-8 {f1(ln)},0" stroke="#b9c3e0" stroke-width="4" '
                 f'fill="none" stroke-linecap="round" opacity="0.5"/>')
    return doc(S.g(band + crest, filter="wobble") + S.g(body, filter="wobble-fine"), defs)


def near_waves_svg(k):
    """Soft wave strokes on the visible part of the near bay (between Israel's shore and Jonah's sandy shore),
    drawn after the land and clipped to the open water; k = drawing 0..2 (strokes shifted for a slow shimmer)."""
    top = ISR_FOOT + 10
    pts = [(x, top) for x in range(-120, 1201, 60)] + [(x, hill_y(x) - 2) for x in range(1200, -121, -40)]
    clip = ('<clipPath id="e24nearclip"><path d="M' + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) +
            ' Z"/></clipPath>')
    rng = random.Random(77)
    body = ""
    for _ in range(26):
        x = rng.uniform(-100, 1100)
        y = rng.uniform(top + 15, 1860)
        if y > hill_y(x) - 10:
            continue
        ln = rng.uniform(50, 130) * (0.7 + (y - top) / 600)
        ph = rng.uniform(0, 3)
        dx = 14 * math.sin(2 * math.pi * (k / 3 + ph / 3))
        op = 0.35 + 0.25 * (0.5 + 0.5 * math.cos(2 * math.pi * (k / 3 + ph / 3)))
        body += (f'<path d="M{f1(x + dx)},{f1(y)} q{f1(ln / 2)},-7 {f1(ln)},0" stroke="#c4cbe6" stroke-width="4" '
                 f'fill="none" stroke-linecap="round" opacity="{op:.2f}"/>')
    return doc(f'<g clip-path="url(#e24nearclip)">{S.g(body, filter="wobble-fine")}</g>', clip)


# ============================================================================ Israel's headland (left)


# village on the summit: (x, variant, scale, facing); houses sit on the crest line
HOUSES = ((290, 0, 0.17, 1), (395, 2, 0.16, -1), (490, 3, 0.15, 1))   # leftmost house clear of the wide frame
# lamp spots (local house coords at scale 1, facing right): windows only, measured from props.house drawings
# (a glowing disc on a closed wooden door read as a target)
HOUSE_LAMPS = {0: ((152, -330),), 2: ((128, -330), (262, -330)), 3: ((-182, -395),)}


def headland_markup():
    """Israel's hills (left): a pale far ridge, and the near green coast hills with the little village on the
    summit, olive trees, a path down to a grassy knoll (where the Israelites stand) and a long slope to the bay."""
    x_end = ISR_KEYS[-1][0]
    defs = ('<linearGradient id="e24isr" gradientUnits="userSpaceOnUse" x1="0" y1="960" x2="0" y2="1410">'
            '<stop offset="0" stop-color="#b3bd66"/><stop offset="0.3" stop-color="#97ad5e"/>'
            '<stop offset="1" stop-color="#6c8a58"/></linearGradient>'
            '<linearGradient id="e24isrsh" gradientUnits="userSpaceOnUse" x1="0" y1="1000" x2="0" y2="1410">'
            '<stop offset="0" stop-color="#58487a" stop-opacity="0"/>'
            '<stop offset="0.45" stop-color="#58487a" stop-opacity="0.1"/>'
            '<stop offset="1" stop-color="#3f3766" stop-opacity="0.38"/></linearGradient>'
            '<linearGradient id="e24isrglaze" gradientUnits="userSpaceOnUse" x1="-200" y1="0" x2="1050" y2="0">'
            '<stop offset="0" stop-color="#ffc890" stop-opacity="0.3"/>'
            '<stop offset="0.6" stop-color="#ffc48a" stop-opacity="0.6"/>'
            '<stop offset="1" stop-color="#ffc48a" stop-opacity="0.8"/></linearGradient>'
            '<filter id="e24vshade" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
            'values="0.9 0.03 0 0 0.02  0.02 0.86 0 0 0.02  0.03 0.03 0.88 0 0.05  0 0 0 1 0"/></filter>')
    # far ridge of Israel's hills, sinking behind the near hills before they reach the bay
    ridge_pts = [(-220, 930), (-60, 900), (120, 884), (300, 906), (470, 958), (600, 1012), (700, 1080)]
    rd = S.smooth_path(ridge_pts, closed=False) + " L700,1200 L-220,1200 Z"
    ridge = f'<path d="{rd}" fill="#b9a6b2" stroke="{P["ink"]}" stroke-width="2.5" stroke-linejoin="round"/>'
    ridge += S.path(S.smooth_path([(x + 4, y + 8) for x, y in ridge_pts[1:6]], closed=False), stroke=False,
                    extra='stroke="#f7d6ae" stroke-width="5" fill="none" opacity="0.55" stroke-linecap="round"')
    ridge_trees = ""
    rng = random.Random(5)
    for x in (-150, -90, 30, 70, 210, 380):
        y = smooth_keys(ridge_pts)(x) + rng.uniform(6, 14)
        ridge_trees += (f'<ellipse cx="{f1(x)}" cy="{f1(y - 9)}" rx="{f1(rng.uniform(9, 14))}" ry="9" '
                        f'fill="#9c93a4" opacity="0.9"/>')
    # the near hills
    xs = list(range(-220, x_end, 20))
    crest = [(x, isr_y(x)) for x in xs] + [(x_end, ISR_FOOT)]
    crest_d = S.smooth_path(crest, closed=False)
    base = [(x, ISR_FOOT + 4 * math.sin(x / 37.0)) for x in range(x_end, -241, -40)]
    hd = crest_d + "".join(f" L{f1(x)},{f1(y)}" for x, y in base) + " Z"
    land = f'<path d="{hd}" fill="url(#e24isr)"/>'
    clip = 'clip-path="url(#e24isrclip)"'
    inner = f'<clipPath id="e24isrclip"><path d="{hd}"/></clipPath>'
    rng = random.Random(61)
    dabs = ""
    for _ in range(30):
        x = rng.uniform(-200, 1000)
        y = rng.uniform(isr_y(x) + 30, ISR_FOOT - 10)
        dabs += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(50, 120))}" ry="{f1(rng.uniform(12, 26))}" '
                 f'fill="{rng.choice(["#7fa553", "#a4c46c", "#76935a"])}" opacity="0.3" filter="url(#soft)"/>')
    # soft field strips and stone terrace lines following the slope
    terr = ""
    for k, (y0, x0, x1) in enumerate(((1095, -220, 560), (1185, -220, 720), (1275, -220, 860))):
        pts = [(x, y0 + 14 * math.sin(x / 150.0 + k) + 0.06 * (x - x0)) for x in range(x0, x1 + 1, 60)]
        terr += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra='stroke="#6f8a4c" stroke-width="4" fill="none" opacity="0.45" stroke-linecap="round"')
        terr += S.path(S.smooth_path([(x, y + 5) for x, y in pts], closed=False), stroke=False,
                       extra='stroke="#d4d692" stroke-width="3" fill="none" opacity="0.4" stroke-linecap="round"')
    ticks = ""
    for _ in range(60):
        x = rng.uniform(-200, 1000)
        top = isr_y(x)
        y = top + 24 + rng.random() ** 1.3 * (ISR_FOOT - top - 40)
        if y > ISR_FOOT - 12:
            continue
        k = 0.7 + (y - 1000) / 900
        ticks += (f'<path d="M{f1(x - 3 * k)},{f1(y)} q{f1(-1 * k)},-{f1(7 * k)} {f1(-7 * k)},-{f1(11 * k)} '
                  f'M{f1(x)},{f1(y)} q{f1(0.5 * k)},-{f1(9 * k)} {f1(3 * k)},-{f1(16 * k)} '
                  f'M{f1(x + 3 * k)},{f1(y)} q{f1(2 * k)},-{f1(6 * k)} {f1(8 * k)},-{f1(9 * k)}" stroke="#5f8340" '
                  f'stroke-width="{f1(2.2 * k)}" fill="none" stroke-linecap="round" opacity="0.6"/>')
    fl = ""
    for _ in range(36):
        x = rng.uniform(-150, 980)
        y = rng.uniform(isr_y(x) + 20, ISR_FOOT - 20)
        fl += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(3.5, 6))}" '
               f'fill="{rng.choice(["#f7e3a1", "#f3a9a0", "#fbf1d8", "#e9c46a"])}" stroke="{P["ink"]}" '
               f'stroke-width="1.4"/>')
    path_pts = [(520, 1048), (540, 1050), (470, 1048), (560, 1050), (640, 1090), (600, 1160), (700, 1250),
                (820, 1330), (900, 1398)]
    trail = S.path(S.smooth_path(path_pts, closed=False), stroke=False,
                   extra='stroke="#ead6a6" stroke-width="13" fill="none" opacity="0.85" stroke-linecap="round"')
    shade = (f'<rect x="-240" y="960" width="1320" height="500" fill="url(#e24isrsh)" {clip}/>'
             f'<g {clip} style="mix-blend-mode:multiply"><path d="{crest_d}" fill="none" stroke="url(#e24isrglaze)" '
             f'stroke-width="160" filter="url(#blur-md)"/></g>')
    ink = f'<path d="{crest_d}" fill="none" stroke="{P["ink"]}" stroke-width="3.5" stroke-linejoin="round"/>'
    rim = S.path(S.smooth_path([(x, isr_y(x) + 6) for x in range(560, x_end - 20, 30)], closed=False), stroke=False,
                 extra='stroke="#f4e39a" stroke-width="6" fill="none" opacity="0.8" stroke-linecap="round"')
    rocks = ""
    for x, w, h, sd in ((860, 60, 28, 1), (930, 44, 22, 2), (990, 64, 28, 3), (300, 56, 26, 4)):
        y = ISR_FOOT + 6
        rocks += (f'<path d="{S.blob(x, y - h * 0.4, w / 2, h / 2, 0.15, 8, seed=sd)}" fill="#9d8a92" '
                  f'stroke="{P["ink"]}" stroke-width="2.5"/>')
    foam = S.path(S.smooth_path([(x, ISR_FOOT + 4 * math.sin(x / 37.0) + 2) for x in range(-220, x_end + 21, 40)],
                                closed=False), stroke=False,
                  extra=f'stroke="{P["foam"]}" stroke-width="6" fill="none" opacity="0.85" stroke-linecap="round"')
    # the village (in the soft backlit shade), olive trees, bushes and two sheep on the slope
    village = (PR.olive_tree(40, isr_y(40) + 4, 0.24, seed=2) + PR.olive_tree(150, isr_y(150) + 3, 0.21, seed=7) +
               PR.olive_tree(-80, isr_y(-80) + 3, 0.22, seed=3))
    for x, v, s, fc in HOUSES:
        village += PR.house(x, isr_y(x) + 3, s, variant=v, facing=fc)
    village += PR.bush(205, isr_y(205) + 8, 0.2, 1) + PR.bush(-10, isr_y(-10) + 7, 0.2, 3)
    slope = ""
    for x, y, s, sd in ((140, 1150, 0.22, 1), (420, 1240, 0.25, 3), (760, 1290, 0.22, 4), (40, 1290, 0.27, 6)):
        slope += PR.olive_tree(x, y, s, seed=sd)
    slope += PR.animal(250, 1205, 0.2, facing=1, kind="sheep") + PR.animal(305, 1222, 0.21, facing=-1, kind="sheep")
    slope += PR.bush(560, 1180, 0.3, 1) + PR.bush(-60, 1200, 0.32, 0)
    head = (S.g(land + f'<g {clip}>{dabs}{terr}</g>', filter="wobble") +
            S.g(f'<g {clip}>{ticks}{fl}{trail}</g>', filter="wobble-fine") +
            S.g(shade + rocks + foam + ink + rim, filter="wobble") +
            f'<g filter="url(#e24vshade)">{village}{slope}</g>')
    return S.g(ridge + ridge_trees, filter="wobble") + inner + head, defs


def house_lamp_points():
    out = []
    for x, v, s, fc in HOUSES:
        y = isr_y(x) + 3
        for lx, ly in HOUSE_LAMPS[v]:
            out.append(PR.local_to_stage(x, y, s, fc, lx, ly))
    return out


# ============================================================================ land (v1 hill, plain, city)


def land_svg():
    """Israel's headland, the far hills, the golden plain with Nineveh, the shoreline and Jonah's grassy hill
    (one static layer; v1's land re-laid out on this stage)."""
    defs = (f'<linearGradient id="e24plain" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="1495">'
            '<stop offset="0" stop-color="#eec08a"/><stop offset="0.35" stop-color="#d9b877"/>'
            '<stop offset="1" stop-color="#a9ad62"/></linearGradient>'
            '<linearGradient id="e24hill" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#bcbd63"/><stop offset="0.42" stop-color="#a6b65d"/>'
            '<stop offset="0.62" stop-color="#8ca858"/><stop offset="1" stop-color="#6f8757"/></linearGradient>'
            f'<linearGradient id="e24hillsh" gradientUnits="userSpaceOnUse" x1="0" y1="{1100 + DY}" x2="0" y2="{SH}">'
            '<stop offset="0" stop-color="#58487a" stop-opacity="0"/>'
            '<stop offset="0.25" stop-color="#58487a" stop-opacity="0.13"/>'
            '<stop offset="1" stop-color="#3f3766" stop-opacity="0.55"/></linearGradient>'
            f'<linearGradient id="e24hillcool" gradientUnits="userSpaceOnUse" x1="{1550 + DX}" y1="0" x2="{SW}" y2="0">'
            '<stop offset="0" stop-color="#5a4a80" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#5a4a80" stop-opacity="0.24"/></linearGradient>'
            f'<linearGradient id="e24glaze" gradientUnits="userSpaceOnUse" x1="{250 + DX}" y1="0" x2="{2500 + DX}" y2="0">'
            '<stop offset="0" stop-color="#ffc48a" stop-opacity="0.75"/>'
            '<stop offset="0.4" stop-color="#ffc890" stop-opacity="0.6"/>'
            '<stop offset="0.62" stop-color="#ffc0a8" stop-opacity="0.3"/>'
            '<stop offset="1" stop-color="#ffc0a8" stop-opacity="0"/></linearGradient>' +
            S.rad_grad("e24jglow", [(0, "#ffe7a8", 0.55), (1, "#ffe7a8", 0)]))
    head, hdefs = headland_markup()
    defs += hdefs
    far_hills = (S.path(S.hill(1590 + DX, 2200 + DX, HORIZON + 6, 70, seed=4, bumps=2, bottom=HORIZON + 120),
                        fill="#c59bab", sw=2.5) +
                 S.path(S.hill(2050 + DX, 2880 + DX + 120, HORIZON + 6, 95, seed=6, bumps=2, bottom=HORIZON + 120),
                        fill="#b994ab", sw=2.5))
    shore = [(x + DX, y + DY) for x, y in ((1565, 953), (1470, 980), (1340, 1025), (1210, 1080), (1090, 1145),
                                          (990, 1220))]
    d = S.smooth_path(shore, closed=False)
    d += f" L{SW + 40},{SH + 60} L{SW + 40},{HORIZON - 2} Z"
    plain = f'<path d="{d}" fill="url(#e24plain)" stroke="{P["ink"]}" stroke-width="3" stroke-linejoin="round"/>'
    foam = S.path(S.smooth_path([(p[0] - 6, p[1] + 2) for p in shore], closed=False), stroke=False,
                  extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="0.8" stroke-linecap="round"')
    rng = random.Random(12)
    fields = ""
    for cx, cy, w, h, col in ((1720, 1060, 260, 40, "#cdb46c"), (2050, 1110, 330, 52, "#d7a96a"),
                              (2480, 1060, 300, 40, "#c9b773"), (1880, 1200, 300, 60, "#b9b268"),
                              (2380, 1220, 360, 62, "#cfae6c"), (2700, 1150, 260, 50, "#bdb56c"),
                              (1640, 1005, 160, 22, "#d8b878"), (2600, 1010, 200, 24, "#d4b47a")):
        cx, cy = cx + DX, cy + DY
        k = (cy - 980 - DY) / 300
        fields += f'<path d="{S.blob(cx, cy, w / 2, h / 2, 0.08, 8, seed=int(cx - DX))}" fill="{col}" opacity="0.75"/>'
        for j in range(3):
            yy = cy - h * 0.25 + j * h * 0.25
            fields += (f'<path d="M{f1(cx - w * 0.36)},{f1(yy)} L{f1(cx + w * 0.36)},{f1(yy)}" stroke="#a98a52" '
                       f'stroke-width="{f1(1.5 + 2 * k)}" opacity="0.4" stroke-linecap="round"/>')
    for _ in range(14):
        x = rng.uniform(1450 + DX, 2900 + DX)
        y = rng.uniform(1000 + DY, 1290 + DY)
        ln = rng.uniform(60, 160) * (0.6 + (y - 980 - DY) / 300)
        fields += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},-3 {f1(ln)},0" stroke="#b6955a" stroke-width="2.5" '
                   f'fill="none" stroke-linecap="round" opacity="0.4"/>')
    road_d = (f"M{1620 + DX},{1250 + DY} C{1760 + DX},{1140 + DY} {1900 + DX},{1070 + DY} {2050 + DX},{1035 + DY} "
              f"S{2200 + DX},{1000 + DY} {2232 + DX},{CITY_Y + 2}")
    road = (f'<path d="{road_d}" stroke="#f4dcaa" stroke-width="22" fill="none" stroke-linecap="round" '
            f'opacity="0.9"/><path d="{road_d}" stroke="#c99b5d" stroke-width="2" fill="none" '
            f'stroke-dasharray="6 14" opacity="0.5"/>')
    sheep = ""
    for x, y, f in ((2330, 1172, 1), (2370, 1185, -1), (2560, 1062, -1), (1830, 1118, 1), (2760, 1100, -1)):
        sheep += PR.animal(x + DX, y + DY, 0.17 + (y - 1050) / 2500, facing=f, kind="sheep")
    deco = ""
    for x, y, s, ln in ((1690, 1002, 0.2, -0.2), (1735, 1008, 0.17, 0.2), (2730, 1000, 0.2, 0.1),
                        (1950, 1062, 0.24, 0.1), (2620, 1118, 0.22, 0.2)):
        deco += PR.palm_tree(x + DX, y + DY, s, lean=ln, dates=False)
    for x, y, s, v in ((1600, 1040, 0.3, 0), (2420, 1170, 0.34, 1), (2050, 1110, 0.3, 3)):
        deco += PR.bush(x + DX, y + DY, s, v)
    city_glow = (f'<ellipse cx="{(CITY_X0 + CITY_X1) / 2}" cy="{CITY_Y - 120}" rx="620" ry="230" fill="#ffdca0" '
                 f'opacity="0.25" filter="url(#blur-md)"/>')
    city = PR.nineveh_skyline(CITY_X0, CITY_X1, CITY_Y, scale=CITY_S, seed=2, haze=0.22, tint="#f6c08f")

    # Jonah's hill
    pts = [(x, hill_y(x)) for x in range(-80, SW + 81, 40)]
    crest_d = S.smooth_path(pts, closed=False)
    hd = crest_d + f" L{SW + 80},{SH + 80} L-80,{SH + 80} Z"
    hill = f'<path d="{hd}" fill="url(#e24hill)"/>'
    hill_ink = f'<path d="{crest_d}" fill="none" stroke="{P["ink"]}" stroke-width="4" stroke-linejoin="round"/>'
    clip = 'clip-path="url(#e24hillclip)"'
    glaze = (f'<clipPath id="e24hillclip"><path d="{hd}"/></clipPath>'
             f'<rect x="-80" y="{1000 + DY}" width="{SW + 160}" height="{SH}" fill="url(#e24hillsh)" {clip}/>'
             f'<rect x="-80" y="{1000 + DY}" width="{SW + 160}" height="{SH}" fill="url(#e24hillcool)" {clip}/>'
             f'<g {clip} style="mix-blend-mode:multiply"><path d="{crest_d}" fill="none" stroke="url(#e24glaze)" '
             f'stroke-width="240" filter="url(#blur-md)"/></g>')
    hatch = ""
    rng2 = random.Random(44)
    for _ in range(30):
        x = rng2.uniform(300 + DX, 2900 + DX)
        top = hill_y(x)
        y = top + 60 + rng2.random() * 380
        if y > SH + 40:
            continue
        col = rng2.choice(["#7fa553", "#9cc06a", "#7a9a52"])
        hatch += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng2.uniform(80, 200))}" ry="{f1(rng2.uniform(18, 40))}" '
                  f'fill="{col}" opacity="0.28" filter="url(#soft)"/>')
    for _ in range(96):
        x = rng2.uniform(380 + DX, 2880 + DX)
        top = hill_y(x)
        y = top + 26 + rng2.random() ** 1.5 * 430
        if y > SH or abs(x - JONAH_X) < 70 and y < top + 70:
            continue
        k = 0.8 + (y - 1100 - DY) / 450
        col = "#62853f" if x < JONAH_X + 250 else "#56733f"
        hatch += (f'<path d="M{f1(x - 3 * k)},{f1(y)} q{f1(-1 * k)},-{f1(7 * k)} {f1(-7 * k)},-{f1(11 * k)} '
                  f'M{f1(x)},{f1(y)} q{f1(0.5 * k)},-{f1(9 * k)} {f1(3 * k)},-{f1(16 * k)} '
                  f'M{f1(x + 3 * k)},{f1(y)} q{f1(2 * k)},-{f1(6 * k)} {f1(8 * k)},-{f1(9 * k)}" stroke="{col}" '
                  f'stroke-width="{f1(2.3 * k)}" fill="none" stroke-linecap="round" opacity="0.7"/>')
    rim_pts = [(x, hill_y(x) + 7) for x in range(1020 + DX, 1520 + DX, 30)]
    rim = S.path(S.smooth_path(rim_pts, closed=False), stroke=False,
                 extra='stroke="#f4e39a" stroke-width="7" fill="none" opacity="0.75" stroke-linecap="round"')
    sand_top = [(x, hill_y(x) + 3) for x in range(200, 1401, 40)]
    sand_bot = [(x, hill_y(x) + 3 + (43 + 10 * math.sin(x / 90)) * min(1.0, max(0.0, (1385 - x) / 300)))
                for x in range(1400, 199, -40)]
    sd = S.smooth_path(sand_top, closed=False) + "".join(f" L{f1(x)},{f1(y)}" for x, y in sand_bot) + " Z"
    sand = f'<path d="{sd}" fill="#ecc99a" opacity="0.95"/>'
    shore_foam = S.path(S.smooth_path([(x, hill_y(x) - 2) for x in range(200, 1410, 40)], closed=False),
                        stroke=False,
                        extra=f'stroke="{P["foam"]}" stroke-width="7" fill="none" opacity="0.9" stroke-linecap="round"')
    rocks = ""
    for x, w, h, sd_ in ((550, 70, 34, 1), (625, 46, 24, 2), (960, 54, 26, 3)):
        y = hill_y(x) + 6
        rocks += (f'<path d="{S.blob(x, y - h * 0.4, w / 2, h / 2, 0.15, 8, seed=sd_)}" fill="#a28c8c" '
                  f'stroke="{P["ink"]}" stroke-width="3"/>')
        rocks += (f'<path d="M{f1(x - w * 0.42)},{f1(y - h * 0.45)} q{f1(w * 0.2)},-{f1(h * 0.4)} {f1(w * 0.45)},'
                  f'-{f1(h * 0.42)}" stroke="#f1d9b3" stroke-width="3" fill="none" opacity="0.8"/>')
    jy = hill_y(JONAH_X)
    halo = f'<ellipse cx="{JONAH_X}" cy="{jy}" rx="230" ry="46" fill="url(#e24jglow)"/>'
    shadow = C.ground_shadow(JONAH_X + 18, jy + 3, JONAH_S, width=130, opacity=0.25)
    fl = ""
    rng = random.Random(33)
    for _ in range(70):
        x = rng.uniform(1000, 2950)
        if abs(x - JONAH_X) < 90 or 1540 < x < 1700 and rng.random() < 0.7:
            continue
        y = hill_y(x) + rng.uniform(25, 120 + abs(x - JONAH_X) * 0.12)
        if y > SH:
            continue
        col = rng.choice(["#f7e3a1", "#f3a9a0", "#fbf1d8", "#e9c46a"])
        r = rng.uniform(4, 7)
        fl += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{P["ink"]}" stroke-width="1.5"/>'
    front = ""
    for x, dy, v, sc_ in ((1120, 150, 2, 1.0), (1650, 190, 2, 1.1), (900, 260, 0, 1.2), (1900, 300, 2, 1.15),
                          (1330, 330, 0, 1.25)):
        front += PR.grass_tuft(x + DX, hill_y(x + DX) + dy, sc_, variant=v)
    front += PR.bush(2330 + DX, hill_y(2330 + DX) + 40, 0.75, 1) + PR.bush(470 + DX, hill_y(470 + DX) + 60, 0.6, 3)
    hill_group = (hill + S.g(hatch, filter="wobble-fine") + sand + shore_foam + rocks +
                  S.g(fl, filter="wobble-fine") + front + glaze + hill_ink + rim)
    body = (head + S.g(far_hills, filter="wobble") + city_glow + city +
            S.g(plain + fields + road + foam, filter="wobble") + deco + sheep +
            S.g(hill_group, filter="wobble") + halo + shadow)
    return doc(body, defs)


# ============================================================================ lamps


def city_lamp_points(cache={}):
    """Window spots on the skyline: sampled from the rasterised skyline's solid areas (v1)."""
    key = (CITY_X0, CITY_X1, CITY_Y, CITY_S, SW, SH)
    if key in cache:
        return cache[key]
    sk = doc(PR.nineveh_skyline(CITY_X0, CITY_X1, CITY_Y, scale=CITY_S, seed=2, haze=0.22, tint="#f6c08f"))
    a = np.asarray(raster.rasterize(sk, SW, SH).getchannel("A")) > 250
    a = ndimage.binary_erosion(a, iterations=7)
    rng = random.Random(17)
    pts = []
    y0, y1 = int(CITY_Y - 240), int(CITY_Y - 62)
    for _ in range(6000):
        x = rng.randint(CITY_X0 + 10, CITY_X1 - 10)
        y = rng.randint(y0, y1)
        if not a[y, x]:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 30 ** 2 for px, py in pts):
            continue
        pts.append((x, y))
        if len(pts) >= 44:
            break
    cache[key] = pts
    return pts


def lamps_svg(pts, r=15, w=7, h=10):
    body = ""
    for x, y in pts:
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="#ffd27a" opacity="0.32"/>'
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.55)}" fill="#ffe2a0" opacity="0.4"/>'
        body += (f'<rect x="{f1(x - w / 2)}" y="{f1(y - h / 2)}" width="{w}" height="{h}" rx="2.5" fill="#ffe08e" '
                 f'stroke="#9a5a2a" stroke-width="1.2"/>')
    return doc(body)


# ============================================================================ ship / fish / splash (v1)

SAILORS = ((175, 2, 1), (-120, 1, 1), (-265, 3, -1))
WAVE_POSES = ("stand", "pray", "lift")


def ship_svg(x, wl, wave_pose="stand"):
    clip = f'<clipPath id="e24shipclip"><rect x="{x - 400}" y="{wl - 400}" width="800" height="{400 + 4}"/></clipPath>'
    crew = ""
    for i, (lx, var, fc) in enumerate(SAILORS):
        sx, sy = PR.local_to_stage(x, wl, SHIP_S, -1, lx, PR.SHIP_DECK_Y)
        pose = wave_pose if i == 1 else "stand"
        crew += C.sailor(sx, sy, SHIP_S, facing=fc, variant=var, pose=pose, expr="happy", marks=False)
    ship = (PR.ship(x, wl, SHIP_S, facing=-1, sail="full", lantern=True, part="back") + crew +
            PR.ship(x, wl, SHIP_S, facing=-1, sail="full", lantern=True, part="front"))
    wake = (f'<path d="M{x - 115},{wl + 2} q60,-7 120,-2 q50,4 95,1" stroke="{P["foam"]}" stroke-width="4" '
            f'fill="none" stroke-linecap="round" opacity="0.85"/>'
            f'<path d="M{x + 70},{wl + 9} q50,-4 110,0" stroke="{P["foam"]}" stroke-width="3" fill="none" '
            f'stroke-linecap="round" opacity="0.6"/>')
    return doc(f'<g clip-path="url(#e24shipclip)">{ship}</g>' + S.g(wake, filter="wobble-fine"), clip)


def splash_svg(x, y, k=1.0):
    rng = random.Random(int(x) + 3)
    drops = ""
    for i in range(8):
        a = math.radians(-160 + 140 * i / 7 + rng.uniform(-8, 8))
        dist = rng.uniform(45, 95) * k
        dx, dy = math.cos(a) * dist, math.sin(a) * dist * 1.15
        r = rng.uniform(6, 11) * k
        rot = math.degrees(a) + 90
        drops += (f'<ellipse cx="{f1(x + dx)}" cy="{f1(y + dy)}" rx="{f1(r * 0.7)}" ry="{f1(r)}" '
                  f'transform="rotate({f1(rot)} {f1(x + dx)} {f1(y + dy)})" fill="{P["foam"]}" '
                  f'stroke="{P["ink"]}" stroke-width="{f1(2.5 * k)}"/>')

    def X(v):
        return f1(x + v * k)

    def Y(v):
        return f1(y + v * k)
    crown = (f'<path d="M{X(-78)},{Y(4)} C{X(-66)},{Y(-30)} {X(-48)},{Y(-58)} {X(-30)},{Y(-34)} '
             f'C{X(-20)},{Y(-70)} {X(6)},{Y(-82)} {X(14)},{Y(-40)} C{X(30)},{Y(-66)} {X(56)},{Y(-52)} '
             f'{X(58)},{Y(-22)} C{X(70)},{Y(-30)} {X(80)},{Y(-10)} {X(82)},{Y(4)} Z" fill="{P["foam"]}" '
             f'stroke="{P["ink"]}" stroke-width="{f1(3 * k)}"/>')
    base = (f'<ellipse cx="{x}" cy="{Y(4)}" rx="{f1(98 * k)}" ry="{f1(15 * k)}" fill="{P["foam"]}" '
            f'stroke="{P["ink"]}" stroke-width="{f1(2.5 * k)}" opacity="0.95"/>')
    return doc(S.g(base + crown + drops, filter="wobble-fine"))


def ripple_svg(x, y, k=1.0):
    body = (f'<ellipse cx="{x}" cy="{y}" rx="{f1(70 * k)}" ry="{f1(11 * k)}" fill="none" stroke="{P["foam"]}" '
            f'stroke-width="{f1(5 * k)}" opacity="0.85"/>'
            f'<ellipse cx="{x}" cy="{f1(y + 2 * k)}" rx="{f1(120 * k)}" ry="{f1(18 * k)}" fill="none" '
            f'stroke="{P["foam"]}" stroke-width="{f1(3.5 * k)}" opacity="0.55"/>')
    return doc(S.g(body, filter="wobble-fine"))


LEAP_RISE, LEAP_DROP = 200, 205
LEAP_U_END = 1.16
SNOUT = (590, 20)


def leap_pose(u, xa, xb, fc):
    x = xa + (xb - xa) * u
    y = MID_WL + LEAP_RISE - (LEAP_RISE + LEAP_DROP) * 4 * u * (1 - u)
    rot = fc * (-40 + 86 * M.ease("sine")(min(1.0, max(0.0, u))))
    return x, y, rot


def leap_snout(u, xa, xb, fc):
    x, y, rot = leap_pose(u, xa, xb, fc)
    lx, ly = SNOUT[0] * FISH_S * fc, SNOUT[1] * FISH_S
    r = math.radians(rot)
    return x + lx * math.cos(r) - ly * math.sin(r), y + lx * math.sin(r) + ly * math.cos(r)


def leap_crossings(xa, xb, fc):
    out, above = [], False
    for i in range(int(LEAP_U_END * 500) + 1):
        u = i / 500
        sx, sy = leap_snout(u, xa, xb, fc)
        if not above and sy < MID_WL:
            out.append((u, sx - fc * 30))
            above = True
        elif above and sy > MID_WL:
            out.append((u, sx))
            break
    return out


# ============================================================================ people


def _fig(design, metrics, x, y, s, facing, ps, expr, label, marks=False):
    inner, _ = C._figure(design, metrics, ps, expr, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


WAVE_A = C._P(h=-6, arms=(("fk", 14, 8), ("fk", -150, -160)), hands=("fist", "open"), expr="happy")
WAVE_B = C._P(h=-6, arms=(("fk", 14, 8), ("fk", -146, -184)), hands=("fist", "open"), expr="happy")
CHEER = dict(C.POSES["cheer"])
STAND = dict(C.POSES["stand"])


def _metrics_for(kind):
    if kind == "child":
        return C._CHILD
    if kind == "woman":
        return C._metrics(C._ADULT, 0.96, 0.92)
    return C._ADULT


def israelite_design(kind, var):
    """Israelite villagers from the citizens' rig (as s02): a man gets a short beard and a blue-grey head-cloth
    (no Assyrian curls; never Jonah's cream-and-orange)."""
    d = C._citizen_design(kind, var, "normal")
    if kind == "man":
        hair = d.get("hair", "#4a2f1f")
        d.update(beard=("short", hair), hat=("headcloth", "#b9c4cf", "#5e7896"), tail=("#b9c4cf", "#5e7896"),
                 long_hair=None, ears=False)
        d.pop("shawl", None)
        d.pop("shawl_trim", None)
    return d


# (x, kind, variant, scale) on the headland plateau, all facing east (right)
ISRAELITES = ((588, "man", 3, 0.42), (634, "woman", 1, 0.41), (674, "child", 0, 0.41), (709, "child", 1, 0.4))
# (x, y, kind, variant, scale) on the plain before Nineveh, come forward toward Jonah, all facing west (left)
# (all inside the close push-in framing too, so none is cut by its right edge during the quiet hold)
NINEVITES = ((2292, 1326, "man", 0, 0.34), (2330, 1330, "woman", 2, 0.335), (2366, 1335, "child", 1, 0.335),
             (2402, 1339, "man", 3, 0.34), (2440, 1344, "child", 0, 0.33))


def group_markup(who, phase):
    """phase -1 = standing (happy), 0 / 1 = the two waving drawings (adults and children alternate)."""
    out = ""
    for i, it in enumerate(ISRAELITES if who == "isr" else NINEVITES):
        if who == "isr":
            x, kind, var, s = it
            y = isr_y(x) + 3
            fc = 1
            d = israelite_design(kind, var)
        else:
            x, y, kind, var, s = it
            fc = -1
            d = C._citizen_design(kind, var, "normal")
        m = _metrics_for(kind)
        if phase < 0:
            ps = STAND
        elif kind == "child":
            ps = CHEER if (phase + i) % 2 == 0 else STAND
        else:
            ps = WAVE_A if (phase + i) % 2 == 0 else WAVE_B
        out += C.ground_shadow(x + 4 * fc, y + 2, s, width=110, opacity=0.2)
        out += _fig(d, m, x, y, s, fc, ps, "happy", f"{who}{i}-{phase}")
    return out


def group_svg(who, lit, phase):
    body = group_markup(who, phase)
    if lit:
        defs = ('<filter id="e24grplit" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
                'values="1.03 0 0 0 0.03  0 0.97 0 0 0.02  0 0 0.86 0 0  0 0 0 1 0"/></filter>')
        return doc(f'<g filter="url(#e24grplit)">{body}</g>', defs)
    defs = ('<filter id="e24grpdim" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
            'values="0.78 0.04 0 0 0.05  0.02 0.74 0 0 0.05  0.04 0.04 0.82 0 0.09  0 0 0 1 0"/></filter>')
    return doc(f'<g filter="url(#e24grpdim)">{body}</g>', defs)


# Jonah's pose records (all from the shared rig)
J_THINK = C._P(h=-2, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"))
J_THINK_UP = C._P(h=-19, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
                  look=(0.04, -0.11))
J_HEART = C._P(h=-10, arms=(("fk", 14, 8), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
               look=(0.02, -0.05))


def jonah_markup(ps, expr):
    jy = hill_y(JONAH_X) + 4
    return _fig(C._jonah_design(), C._ADULT, JONAH_X, jy, JONAH_S, 1, ps, expr, f"jonah-{id(ps)}-{expr}")


def rim_svg(markup):
    """Warm sunset rim light on the west (sun-facing) edge of a figure (v1)."""
    defs = ('<filter id="e24rim" x="-20%" y="-20%" width="140%" height="140%">'
            '<feOffset in="SourceAlpha" dx="3" dy="0" result="o1"/>'
            '<feOffset in="SourceAlpha" dx="10" dy="1" result="o2"/>'
            '<feComposite in="o1" in2="o2" operator="out" result="band"/>'
            '<feComposite in="band" in2="SourceAlpha" operator="in" result="band2"/>'
            '<feGaussianBlur in="band2" stdDeviation="1.3" result="bb"/>'
            '<feFlood flood-color="#ffd27e" result="c"/>'
            '<feComposite in="c" in2="bb" operator="in"/></filter>')
    return doc(f'<g filter="url(#e24rim)">{markup}</g>', defs)


def alive(x, y, switches=(), phase=0.0, amp=0.011, period=3.1):
    """Breathing (vertical stretch about the feet) + a squash 'pop' at every pose switch (v1 s05)."""
    def m(t):
        sy = 1 + amp * math.sin(2 * math.pi * (t / period + phase))
        sx = 1.0
        for ts in switches:
            u = (t - ts) / 0.24
            if 0 <= u <= 1:
                bmp = math.sin(math.pi * u) * (1 - u)
                sy *= 1 - 0.09 * bmp
                sx *= 1 + 0.05 * bmp
        return Tf(sx=sx, sy=sy, px=x, py=y)
    return m


# ============================================================================ doves (v1)


DOVE_BASE = (1700, 900)
DOVE_WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)
FLAP_CYCLE = (0, 1, 2, 3, 4, 3, 2, 1)
D_STAND = 5
LD = 0.78   # landed doves' scale


def dove_frames(facing):
    x, y = DOVE_BASE
    frames = [doc(PR.dove(x, y, 1.0, facing=facing, wing=w)) for w in DOVE_WINGS]
    frames.append(doc(PR.dove(x, y, 1.0, facing=facing, pose="stand")))
    return frames


def gy(x):
    """Anchor y of a landed dove ('stand' feet are +38*scale below its anchor) on Jonah's hill."""
    return hill_y(x) - 38 * LD + 3


class DoveFlight:
    """Cubic-Bezier flight p0 -> p3 from t0 to t1; optional landing (then 'stand' with little pecks) — v1."""

    def __init__(self, t0, t1, p0, c1, c2, p3, scale, land=False, phase=0.0, flap_fps=15.0, glide=(1.1, 0.7),
                 scale0=None, fade=0.0):
        self.t0, self.t1, self.p0, self.c1, self.c2, self.p3 = t0, t1, p0, c1, c2, p3
        self.fade = fade
        self.scale, self.land, self.phase, self.flap_fps, self.glide = scale, land, phase, flap_fps, glide
        self.scale0 = scale if scale0 is None else scale0

    def pos(self, t):
        u = min(1.0, max(0.0, (t - self.t0) / (self.t1 - self.t0)))
        if self.land:
            u = 1 - (1 - u) ** 1.6
        return bez3(self.p0, self.c1, self.c2, self.p3, u)

    def motion(self, t):
        if t < self.t0 - 0.05:
            return Tf(alpha=0.0)
        x, y = self.pos(t)
        if self.land and t > self.t1:
            bobv = -2.5 * abs(math.sin(2 * math.pi * (t - self.t1) * 0.45 + self.phase)) ** 6
        else:
            bobv = 6 * math.sin(2 * math.pi * (t * 1.6 + self.phase))
        u = min(1.0, max(0.0, (t - self.t0) / (self.t1 - self.t0)))
        k = M.lerp(self.scale0, self.scale, u)
        a = M.progress(t, self.t0 - 0.05, self.t0 - 0.05 + self.fade, "sine") if self.fade > 0 else 1.0
        return Tf(dx=x - DOVE_BASE[0], dy=y - DOVE_BASE[1] + bobv * k, sx=k, sy=k, alpha=a, px=DOVE_BASE[0],
                  py=DOVE_BASE[1])

    def frame(self, t):
        if self.land and t >= self.t1:
            return float(D_STAND)
        if self.land and t >= self.t1 - 0.35:
            return 0.0
        on, off = self.glide
        cyc = (t - self.t0 + self.phase * (on + off)) % (on + off)
        if cyc > on:
            return 2.0
        return float(FLAP_CYCLE[int(cyc * self.flap_fps) % len(FLAP_CYCLE)])


# ============================================================================ "?", hearts, end card


Q_POS = (1912, 1012)     # baseline centre of the question mark (above-right of Jonah's head)


def question_svg():
    x, y = Q_POS
    return doc(S.text(x, y, "?", size=170, fill="#fff3d6",
                      extra=f'stroke="{P["ink"]}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))


def question_glow_svg():
    x, y = Q_POS
    defs = S.rad_grad("e24qglow", [(0, "#ffe9a8", 0.5), (0.5, "#ffd890", 0.2), (1, "#ffd890", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y - 60}" rx="105" ry="112" fill="url(#e24qglow)"/>', defs)


def heart_path(x, y, r):
    return (f"M{f1(x)},{f1(y + 0.95 * r)} C{f1(x - 1.7 * r)},{f1(y - 0.1 * r)} {f1(x - 0.95 * r)},{f1(y - 1.3 * r)} "
            f"{f1(x)},{f1(y - 0.5 * r)} C{f1(x + 0.95 * r)},{f1(y - 1.3 * r)} {f1(x + 1.7 * r)},{f1(y - 0.1 * r)} "
            f"{f1(x)},{f1(y + 0.95 * r)} Z")


def heart_markup(x, y, r, fill="#e8706a", sw=5):
    return (f'<path d="{heart_path(x, y, r)}" fill="{fill}" stroke="{P["ink"]}" stroke-width="{sw}" '
            f'stroke-linejoin="round"/>'
            f'<ellipse cx="{f1(x - 0.62 * r)}" cy="{f1(y - 0.48 * r)}" rx="{f1(0.22 * r)}" ry="{f1(0.14 * r)}" '
            f'transform="rotate(-35 {f1(x - 0.62 * r)} {f1(y - 0.48 * r)})" fill="#fde3d6"/>')


FLOAT_HEART = (1700, 1700)   # where the rising hearts are drawn (moved by their motion)


def float_heart_svg(fill):
    x, y = FLOAT_HEART
    glow = f'<circle cx="{x}" cy="{y}" r="60" fill="#ffe0b0" opacity="0.4" filter="url(#soft)"/>'
    return doc(glow + S.g(heart_markup(x, y, 33, fill, 4.5), filter="wobble-fine"))


def card_text_svg():
    return doc(S.text(CARD_X, CARD_Y, "约拿的故事 · 完", size=172, fill="#fff3d6",
                      extra=f'stroke="{P["ink"]}" stroke-width="13" paint-order="stroke" stroke-linejoin="round"'))


def card_glow_svg():
    defs = S.rad_grad("e24card", [(0, "#ffe9bb", 0.42), (0.6, "#ffd9a8", 0.16), (1, "#ffd9a8", 0)])
    return doc(f'<ellipse cx="{CARD_X}" cy="{CARD_Y - 40}" rx="820" ry="250" fill="url(#e24card)"/>', defs)


def swash_svg(side):
    cx, y = CARD_X, CARD_Y + 84

    def X(v):
        return f1(cx + side * v)
    d = (f"M{X(84)},{y - 2} C{X(150)},{y + 10} {X(240)},{y + 12} {X(330)},{y - 4} "
         f"C{X(380)},{y - 14} {X(400)},{y - 40} {X(372)},{y - 46} C{X(346)},{y - 50} {X(338)},{y - 22} {X(366)},{y - 12} "
         f"C{X(410)},{y + 4} {X(460)},{y - 6} {X(500)},{y - 20}")
    return doc(f'<path d="{d}" stroke="{P["ink"]}" stroke-width="17" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/>'
               f'<path d="{d}" stroke="#fff3d6" stroke-width="8" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/>')


HEART = (CARD_X, CARD_Y + 86)


def heartbeat(t0, pivot, amp=0.06, period=1.1):
    def m(t):
        if t <= t0:
            return Tf(px=pivot[0], py=pivot[1])
        k = 1 + amp * max(0.0, math.sin(2 * math.pi * (t - t0) / period)) ** 4
        return Tf(sx=k, sy=k, px=pivot[0], py=pivot[1])
    return m


def card_heart_svg():
    x, y = HEART
    return doc(S.g(heart_markup(x, y, 40), filter="wobble-fine"))


def burst_fx(cx, cy, t0, n=14, dist=(90, 200), dur=1.0, size=(9, 18), color=(255, 236, 170), seed=3):
    """Golden four-point sparkles flying out from (cx, cy) (stage px) at t0, shrinking and fading over dur."""
    from PIL import Image, ImageDraw
    rng = random.Random(seed)
    parts = [(2 * math.pi * (i + rng.uniform(-0.3, 0.3)) / n, rng.uniform(*dist), rng.uniform(*size))
             for i in range(n)]

    def fx(frame, t, view):
        u = (t - t0) / dur
        if not 0.0 <= u <= 1.0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        e = 1 - (1 - u) ** 3
        for a, dd, sz in parts:
            ox, oy = view.to_out(cx + math.cos(a) * dd * e, cy + math.sin(a) * dd * e - 40 * u)
            r = sz * view.scale * (1.0 - 0.55 * u)
            al = int(240 * min(1.0, u / 0.08) * (1 - u) ** 1.3)
            w, g = r * 0.24, r * 0.6
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*color, al // 4))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, al))
        frame.alpha_composite(ov)
        return frame
    return fx


def sparkles_from(rect, t0, drift, **kw):
    """FX.sparkles, but drifting from t0: FX.sparkles places each sparkle at py + drift * t with t counted from
    the scene start, so a late, drifting set would appear far from its rect. Shift the rect to compensate."""
    x0, y0, x1, y1 = rect
    off = -drift * t0
    return FX.sparkles((x0, y0 + off, x1, y1 + off), t0=t0, drift=drift, **kw)


def star_points(rect, n, seed):
    """n twinkle positions inside rect that keep clear of the high clouds, streaks and end card (star_ok)."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = rect
    pts, tries = [], 0
    while len(pts) < n and tries < 4000:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if star_ok(x, y, 20) and all((x - a) ** 2 + (y - b) ** 2 > 140 ** 2 for a, b in pts):
            pts.append((x, y))
    return pts


def twinkle_fx(pts, t0, color=(255, 246, 214), size=(9, 16), period=2.4, seed=61):
    """Twinkling four-point stars at fixed stage positions (FX.sparkles' drawing, without drift or a random rect)."""
    from PIL import Image, ImageDraw
    rng = random.Random(seed)
    ph = [rng.uniform(0, 1) for _ in pts]
    sz = [rng.uniform(*size) for _ in pts]

    def fx(frame, t, view):
        k = M.progress(t, t0, t0 + 0.6, "sine")
        if k <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for (x, y), p, z in zip(pts, ph, sz):
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t / period + p))
            if tw < 0.15:
                continue
            ox, oy = view.to_out(x, y)
            r = z * view.scale * (0.5 + 0.5 * tw)
            a = int(230 * k * tw)
            w, g = r * 0.22, r * 0.55
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(*color, a // 4))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


# ============================================================================ warm light blooms


def bloom_svg(cx, cy, rx, ry, col="#ffcf87", op=0.34, name="b"):
    defs = S.rad_grad(f"e24bl{name}", [(0, col, op), (0.45, col, op * 0.45), (1, col, 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#e24bl{name})"/>', defs)


# ============================================================================ build


CAM_WIDE_X = 1655   # centre of the full-spread framing: the whole village (left) and Nineveh (right) in frame

TUFTS = ((1215, 2, 0.75), (1290, 0, 0.6), (1545, 0, 0.62), (1660, 2, 0.8), (1010, 0, 0.8), (1840, 1, 0.75),
         (860, 2, 0.9), (2050, 0, 0.9))


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    try:
        from engine.loader import load_timeline
        xf = float(load_timeline().get("xfade", XFADE_DEFAULT))
    except Exception:
        xf = XFADE_DEFAULT
    # dip through the blank page (v1 s13_end): the page covers this scene until s23 is down to ~5 % of the
    # dissolve, then lifts, so s23's last Jonah and this one never share a frame
    paper_dip = (0.95 * xf, 0.95 * xf + 0.65)
    nl = len(ctx.lines)
    L_last = ctx.lines[-1]

    # ------------------------------------------------------------------ narration beats
    t_q = when(ctx, "回答的呢", (0, 0.45))           # the "?" pops up
    t_think = when(ctx, "圣经没有", (0, 0.5))         # hand to chin
    t_if = when(ctx, "如果你是约拿", (1, 0.0))        # push in
    t_up = when(ctx, "你会怎么回答", (1, 0.42))       # looks up to the sky
    l_ask = ctx.lines[min(1, nl - 1)]
    t_love = when(ctx, "上帝的爱", (2, 0.0))          # "?" bursts, Jonah smiles, pull back starts
    t_sea = when(ctx, "比大海", (2, 0.11))            # widen west, fish leaps
    t_sky = when(ctx, "比天空", (2, 0.27))            # tilt up, rays
    t_isr = when(ctx, "他爱以色列人", (2, 0.43))      # light on Israel
    t_nin = when(ctx, "也爱尼尼微人", (2, 0.58))      # light on Nineveh
    t_jon = when(ctx, "他爱约拿", (2, 0.74))          # light on Jonah, hand on heart
    t_you = when(ctx, "也爱你和我", (2, 0.87))        # hearts float up from the page's edge
    t_wrong = when(ctx, "我们做错了事", (3, 0.0))     # dusk deepens
    t_back = when(ctx, "只要回到", (3, 0.24))         # doves fly home
    t_chance = when(ctx, "他总会给", (3, 0.52))       # evening star
    t_new = when(ctx, "重新开始", (3, 0.75))          # fish leaps again, sailor waves
    t_hope = when(ctx, "上帝也希望", (4, 0.0))        # Jonah stands, looking at the city
    t_each = when(ctx, "爱惜身边", (4, 0.35))         # lamps light up
    t_even = when(ctx, "连我们不喜欢", (4, 0.63))     # both peoples wave; two doves meet
    t_card = L_last.end - 0.1                          # end card

    # ------------------------------------------------------------------ sky
    t_rays = t_sky + 0.05      # "比天空还要高": the rays fan out from the sun up to the top of the sky

    t_dim0 = max(t_wrong, t_rays + 2.1)    # evening falls: the same rays, weaker (frame 3 = frame 2 at half opacity)
    t_dim1 = max(t_dim0 + 1.0, t_chance + 2.0)

    def sky_frame(t):
        if t < t_rays:
            return 0.0
        if t < t_rays + 0.8:
            return M.progress(t, t_rays, t_rays + 0.8, "sine")
        if t < t_rays + 2.0:
            return 1.0 + M.progress(t, t_rays + 0.8, t_rays + 2.0, "sine")
        return 2.0 + M.progress(t, t_dim0, t_dim1, "sine")
    sc.add("sky", [sky_svg(0), sky_svg(0.5), sky_svg(1.0), sky_svg(1.0, 0.5)], wc=0.55, frame_at=sky_frame)
    sc.add("dusk", dusk_svg(), wc=0, motion=M.keys(
        [(0, {"alpha": 0}), (t_wrong - 0.3, {"alpha": 0}), (t_chance + 1.4, {"alpha": 0.85}), (T, {"alpha": 1.0})],
        ["sine", "sine", "linear"]))
    # the first stars come out one field after the evening star; they hold steady (no unison pulse) and a few
    # separate fx stars twinkle each on its own phase (below)
    sc.add("stars", stars_svg(), wc=0, motion=M.keys([(t_chance + 0.6, {"alpha": 0}), (t_chance + 2.2, {"alpha": 1})],
                                                    "sine"))
    sc.add("evening_star", evening_star_svg(*EV_STAR), wc=0, motion=M.combine(
        M.keys([(t_chance - 0.05, {"alpha": 0, "s": 0.2}), (t_chance + 0.5, {"alpha": 1, "s": 1.0})], "back",
               pivot=EV_STAR), M.pulse(0.75, 1.0, 1.4)))
    sc.add("sun", sun_svg(), motion=M.keys([(0, {"dy": 0}), (T, {"dy": SUN_SINK})], "linear"))
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=4))
    # ------------------------------------------------------------------ sea: far band, fish, mid band, ship, near
    sc.add("sea_far", sea_far_svg())
    glit = [glitter_svg(s, HORIZON + 6, MID_WL) for s in (1, 2, 3)]
    sc.add("glitter_far", glit + [glit[0]], wc=0.3, frame_at=lambda t: (t * 2.6) % 3.0,
           motion=M.pulse(0.75, 1.0, 2.3))

    # both leaps pass well west of the ship (its bow is at ~SHIP_X - 100 + SHIP_VX * t)
    leaps = [(t_sea - 0.12, 1.35, 1245, 1005, -1), (t_new - 0.25, 1.35, 850, 1180, 1)]
    splash_events = []
    for i, (ls, ld, xa, xb, fc) in enumerate(leaps):
        fx0, fy0 = (xa + xb) / 2, MID_WL
        frames = [doc(PR.fish(fx0, fy0, FISH_S, facing=fc, eye="happy", mouth=0.12, tail=tv))
                  for tv in (0.65, 0.0, -0.65)]

        def fish_motion(t, ls=ls, ld=ld, xa=xa, xb=xb, fc=fc, fx0=fx0, fy0=fy0):
            u = (t - ls) / ld
            if u <= 0 or u >= LEAP_U_END:
                return Tf(alpha=0.0)
            x, y, rot = leap_pose(u, xa, xb, fc)
            return Tf(dx=x - fx0, dy=y - fy0, rot=rot, px=fx0, py=fy0)

        sc.add(f"fish{i}", frames, motion=fish_motion, seed=90 + i,
               frame_at=lambda t: float((0, 1, 2, 1)[int(t * 9) % 4]))
        for u, xs in leap_crossings(xa, xb, fc):
            splash_events.append((ls + u * ld, xs))

    sc.add("sea_mid", sea_mid_svg())
    glit_m = [glitter_svg(s, MID_WL, NEAR_WL - 6) for s in (1, 2, 3)]
    sc.add("glitter_mid", glit_m + [glit_m[0]], wc=0.3, frame_at=lambda t: (t * 2.6) % 3.0,
           motion=M.pulse(0.75, 1.0, 2.3))

    sp0 = (1150, MID_WL)
    sp_svg, rp_svg = splash_svg(*sp0, k=SPLASH_K), ripple_svg(*sp0, k=SPLASH_K)
    for k, (ts, xs) in enumerate(splash_events):
        dx = xs - sp0[0]
        sc.add(f"ripple{k}", rp_svg, wc=0.4, seed=71, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.5, "sy": 0.5}), (ts + 0.05, {"alpha": 1, "sx": 0.6, "sy": 0.6}),
                    (ts + 1.6, {"alpha": 0, "sx": 1.9, "sy": 1.5})], "out", pivot=sp0),
            M.still(Tf(dx=dx))))
        sc.add(f"splash{k}", sp_svg, wc=0.4, seed=73, motion=M.combine(
            M.keys([(ts - 0.01, {"alpha": 0, "sx": 0.3, "sy": 0.2}), (ts + 0.02, {"alpha": 1, "sx": 0.45, "sy": 0.35}),
                    (ts + 0.28, {"alpha": 1, "sx": 1.0, "sy": 1.0}), (ts + 0.75, {"alpha": 0, "sx": 1.15, "sy": 0.7})],
                   "out", pivot=(sp0[0], sp0[1] + 8 * SPLASH_K)),
            M.still(Tf(dx=dx))))
        sc.sfx("splash_small", ts - 0.03, gain_db=-15, pan=-0.4)

    ship_wl = MID_WL + 2
    t_wave0, t_wave1 = t_new - 0.2, min(T - 1.2, t_new + 2.4)

    def ship_frame(t):
        if t < t_wave0 or t > t_wave1:
            return 0.0
        return float((1, 2)[int((t - t_wave0) * 3.2) % 2])
    sc.add("ship", [ship_svg(SHIP_X, ship_wl, p) for p in WAVE_POSES], frame_at=ship_frame, motion=M.combine(
        M.drift(vx=SHIP_VX), M.sway(1.6, 3.6, pivot=(SHIP_X, ship_wl)), M.bob(3, 2.9)))

    sc.add("sea_near", near_sea_svg())   # static: flattened with the land

    # ------------------------------------------------------------------ land, lamps, people
    sc.add("land", land_svg())
    nw = [near_waves_svg(k) for k in range(3)]
    sc.add("near_waves", nw + [nw[0]], wc=0.3, frame_at=lambda t: (t * 0.9) % 3.0)

    # lamps: Nineveh's windows glow faintly from the start; on "爱惜身边的每一个人" lamps pop on group by group,
    # from Israel's village across to Nineveh
    cpts = sorted(city_lamp_points())
    hpts = house_lamp_points()
    span = 1.6
    groups = [("lamps_isr", hpts, 0.0, 14, 6, 8)]
    n_c = 4
    for g in range(n_c):
        groups.append((f"lamps_city{g}", cpts[g * len(cpts) // n_c:(g + 1) * len(cpts) // n_c], 0.3, 22, 9, 12))
    for gi, (name, pts, base, r, w, h) in enumerate(groups):
        tp = t_each + 0.15 + span * gi / (len(groups) - 1)
        sc.add(name, lamps_svg(pts, r, w, h), wc=0, motion=M.combine(
            M.keys([(0, {"alpha": base}), (tp - 0.01, {"alpha": base}), (tp + 0.12, {"alpha": 1.0})], "out"),
            M.pulse(0.85, 1.0, 1.7, 0.13 * gi)))
        if gi in (0, 2, 4):
            sc.sfx("pop", tp, gain_db=-17, pan=-0.6 + 0.3 * gi)

    # "爱惜身边的每一个人": a warm glow lights up behind every single person, one after another, from the
    # Israelites across to the Ninevites (drawn just behind the figures)
    folk = ([(x, isr_y(x) + 3, s) for x, _, _, s in ISRAELITES] + [(x, y, s) for x, y, _, _, s in NINEVITES])
    for i, (x, y, s) in enumerate(folk):
        tp = t_each + 0.1 + i * 1.55 / (len(folk) - 1)
        piv = (x, y - 150 * s)
        sc.add(f"halo{i}", bloom_svg(x, y - 150 * s, 66, 92, col="#ffe2a0", op=0.6, name=f"p{i}"), wc=0, blend="add",
               motion=M.combine(M.keys([(tp, {"alpha": 0, "s": 0.4}), (tp + 0.22, {"alpha": 1.0, "s": 1.08}),
                                        (tp + 0.6, {"alpha": 0.8, "s": 1.0})], "out", pivot=piv),
                                M.pulse(0.85, 1.0, 2.1, 0.17 * i)))

    def group_layer(name, who, t_lit, waves, z_phase=0.0):
        def frame_at(t):
            p = M.progress(t, t_lit - 0.3, t_lit + 0.35, "sine")
            if p < 1.0:
                return p
            for a, b in waves:
                if a <= t < b:
                    return float(2 + int((t - a) * 2.6 + z_phase) % 2)
            return 1.0
        frames = [group_svg(who, False, -1), group_svg(who, True, -1), group_svg(who, True, 0),
                  group_svg(who, True, 1)]
        sc.add(name, frames, wc=0.5, frame_at=frame_at)

    t_wave_end = min(T - 1.0, t_even + 2.9)
    group_layer("israelites", "isr", t_isr, [(t_isr + 0.35, t_isr + 3.2), (t_even + 0.1, t_wave_end)])
    group_layer("ninevites", "nin", t_nin, [(t_nin + 0.35, t_nin + 3.0), (t_even + 0.25, t_wave_end)], 0.5)

    # ------------------------------------------------------------------ Jonah
    jy = hill_y(JONAH_X) + 4
    poses = [  # (switch time, pose record, expression, pop) — pop: a pose change sold by a small squash
        (0.0, STAND, "neutral", False),
        (t_think, J_THINK, "neutral", True),          # hand to chin: "圣经没有告诉我们"
        (t_up, J_THINK_UP, "neutral", True),          # looks up to the sky: "你会怎么回答上帝呢"
        (t_love, STAND, "happy", True),               # "上帝的爱": the "?" bursts, he smiles
        (t_jon, J_HEART, "happy", True),              # "他爱约拿": hand on his heart, smiling up into the light
        (t_back + 0.35, J_HEART, "peaceful", False),  # eyes closed in the warm light while the doves come home
        (t_chance + 0.1, J_HEART, "happy", False),    # eyes open again, smiling: "他总会给我们重新开始的机会"
        (t_hope, STAND, "happy", True),               # stands looking at the city (line 4)
    ]
    blinks = [2.3, t_think + 1.3, t_up + 1.6, t_up + 3.4, t_jon + 2.6, t_hope + 1.7, t_hope + 5.2, t_hope + 8.4]
    j_frames, rim_frames, blink_of = [], [], []
    for _, ps, e, _ in poses:
        mk = jonah_markup(ps, e)
        j_frames.append(doc(mk))
        rim_frames.append(rim_svg(mk))
    for i, (_, ps, e, _) in enumerate(poses):
        if e == "peaceful":
            blink_of.append(i)
        else:
            blink_of.append(len(j_frames))
            j_frames.append(doc(jonah_markup(ps, BLINK_EXPR.get(e, "peaceful"))))
    p_times = [p[0] for p in poses]

    def j_frame(t):
        i = max(0, bisect.bisect_right(p_times, t) - 1)
        for b in blinks:
            if b <= t < b + 0.13:
                return float(blink_of[i])
        return float(i)

    def rim_frame(t):
        return float(max(0, bisect.bisect_right(p_times, t) - 1))
    j_alive = alive(JONAH_X, jy, switches=[p[0] for p in poses if p[3]], amp=0.011, period=3.4)
    sc.add("jonah", j_frames, seed=55, frame_at=j_frame, motion=j_alive)
    sc.add("jonah_rim", rim_frames, wc=0, frame_at=rim_frame, motion=M.combine(
        j_alive, M.keys([(0, {"alpha": 0.45}), (t_jon - 0.2, {"alpha": 0.5}), (t_jon + 0.9, {"alpha": 1.0})],
                        "sine")))

    for k, (x, v, s) in enumerate(TUFTS):
        x += DX
        by = hill_y(x) + 8
        sc.add(f"tuft{k}", doc(PR.grass_tuft(x, by, s, variant=v)),
               motion=M.sway(3.2 if v == 2 else 2.4, 3.0 + 0.3 * (k % 3), pivot=(x, by), phase=k * 0.17))

    shade_f = ('<filter id="e24fgshade" x="-10%" y="-10%" width="120%" height="120%"><feColorMatrix type="matrix" '
               'values="0.7 0 0 0 0.05  0 0.7 0 0 0.035  0 0 0.76 0 0.09  0 0 0 1 0"/></filter>')
    fl_ = (PR.reeds(420, 1858, 1.15, variant=1) + PR.grass_tuft(560, 1858, 2.1, variant=0) +
           PR.grass_tuft(690, 1862, 1.6, variant=2))
    fr_ = (PR.bush(3130, 1878, 1.35, 1) + PR.grass_tuft(2950, 1858, 2.0, variant=2) +
           PR.grass_tuft(2850, 1862, 1.5, variant=0))
    sc.add("fg_left", doc(f'<g filter="url(#e24fgshade)">{fl_}</g>', shade_f), motion=M.sway(1.1, 4.2, (560, 1858)))
    sc.add("fg_right", doc(f'<g filter="url(#e24fgshade)">{fr_}</g>', shade_f),
           motion=M.sway(0.9, 4.8, (3000, 1870), 0.4))

    # ------------------------------------------------------------------ warm light blooms (additive)
    def bloom(name, svg, keys):
        sc.add(name, svg, wc=0, blend="add", motion=M.combine(M.keys(keys, "sine"), M.pulse(0.85, 1.0, 3.0)))
    bloom("warm_isr", bloom_svg(430, 1070, 580, 340, name="i"),
          [(0, {"alpha": 0}), (t_isr - 0.15, {"alpha": 0}), (t_isr + 1.0, {"alpha": 1.0}), (T, {"alpha": 0.75})])
    bloom("warm_city", bloom_svg(2640, 1070, 640, 280, name="c"),
          [(0, {"alpha": 0.15}), (t_nin - 0.15, {"alpha": 0.15}), (t_nin + 1.0, {"alpha": 1.0}), (T, {"alpha": 0.75})])
    bloom("warm_jonah", bloom_svg(JONAH_X, jy - 140, 270, 250, col="#ffd890", op=0.32, name="j"),
          [(0, {"alpha": 0.1}), (t_up - 0.3, {"alpha": 0.1}), (t_up + 1.2, {"alpha": 0.6}),
           (t_jon - 0.15, {"alpha": 0.6}), (t_jon + 0.9, {"alpha": 1.0}), (T, {"alpha": 0.85})])

    # ------------------------------------------------------------------ doves
    fr_left, fr_right = dove_frames(-1), dove_frames(1)
    flights = [  # (flight, frames)
        # line 3 "只要回到上帝身边": two doves fly home out of the east and land beside Jonah
        (DoveFlight(t_back + 0.05, t_back + 2.05, (3330, 595), (2550, 615), (2020, 835), (1930, gy(1930)), LD,
                    land=True, phase=0.1), fr_left),
        (DoveFlight(t_back + 0.35, t_back + 2.45, (3360, 665), (2600, 675), (2080, 875), (2012, gy(2012)),
                    LD * 0.96, land=True, phase=0.45), fr_left),
        # line 4 "连我们不喜欢的人也一样": one dove from Israel, one from Nineveh, land side by side facing each other
        # (they fade in over 0.25 s just beside each group, small, so they seem to rise from among the people)
        (DoveFlight(t_even - 0.25, t_even + 2.0, (762, 985), (1000, 800), (1380, 860), (1562, gy(1562)), LD,
                    land=True, phase=0.2, scale0=0.5, fade=0.25), fr_right),
        (DoveFlight(t_even - 0.25, t_even + 2.05, (2492, 1236), (2350, 800), (1700, 640), (1632, gy(1632)), LD,
                    land=True, phase=0.6, scale0=0.5, fade=0.25), fr_left),
    ]
    for k, (fl, frs) in enumerate(flights):
        sc.add(f"dove{k}", frs, seed=77, motion=fl.motion, frame_at=fl.frame)
    t_meet = t_even + 2.05
    th2 = t_meet + 0.25
    mini = (1597, gy(1597) - 62)
    sc.add("mini_heart", doc(S.g(heart_markup(*mini, 16, sw=3.5), filter="wobble-fine")), wc=0, motion=M.combine(
        M.keys([(th2, {"alpha": 0, "s": 0.2, "dy": 10}), (th2 + 0.1, {"alpha": 1}), (th2 + 0.45, {"s": 1.0, "dy": 0})],
               "back", pivot=mini), M.bob(3, 1.8)))

    # ------------------------------------------------------------------ the question mark
    t_qs = t_up + 0.1

    def q_motion(t):
        a = M.progress(t, t_q, t_q + 0.12, "linear") * (1 - M.progress(t, t_love + 0.06, t_love + 0.3, "sine"))
        s = M.lerp(0.25, 1.0, M.ease("back")(min(1.0, max(0.0, (t - t_q) / 0.38))))
        s *= 1 + 0.2 * M.progress(t, t_qs, t_qs + 0.8, "inout") + 0.35 * M.progress(t, t_love, t_love + 0.25, "out")
        rot = 7 * math.sin(2 * math.pi * t / 2.6)
        dy = 6 * math.sin(2 * math.pi * t / 2.1)
        return Tf(dy=dy, rot=rot, sx=s, sy=s, alpha=a, px=Q_POS[0], py=Q_POS[1] - 40)
    sc.add("q_glow", question_glow_svg(), wc=0, blend="add", motion=M.combine(
        M.keys([(t_qs, {"alpha": 0}), (t_qs + 0.8, {"alpha": 1}), (t_love, {"alpha": 1}), (t_love + 0.6, {"alpha": 0})],
               "sine"), M.pulse(0.7, 1.0, 1.6)))
    sc.add("question", question_svg(), wc=0, motion=q_motion)
    sc.sfx("pop", t_q, gain_db=-12, pan=0.2)

    # ------------------------------------------------------------------ hearts floating up toward "you and me"
    hearts = [(-620, 0.0, "#e8706a"), (-180, 0.22, "#f09a7a"), (420, 0.1, "#e8706a"), (880, 0.36, "#f2a2a0"),
              (120, 0.5, "#ee8576"), (-880, 0.62, "#f09a7a")]
    for k, (hx, dt, col) in enumerate(hearts):
        t0 = t_you + dt
        rise = 640 + 60 * (k % 3)

        def h_motion(t, t0=t0, hx=hx, rise=rise, k=k):
            u = (t - t0) / 2.6
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.6, 1.0, "sine"))
            s = 0.75 + 0.35 * math.sin(math.pi * min(1.0, u * 1.6) / 2)
            return Tf(dx=hx + 22 * math.sin(2 * math.pi * (u * 1.3 + 0.2 * k)), dy=200 - rise * M.ease("out")(u),
                      rot=8 * math.sin(2 * math.pi * (u + 0.3 * k)), sx=s, sy=s, alpha=a,
                      px=FLOAT_HEART[0], py=FLOAT_HEART[1])
        sc.add(f"float_heart{k}", float_heart_svg(col), wc=0, motion=h_motion)

    # ------------------------------------------------------------------ end card
    sc.add("card_glow", card_glow_svg(), wc=0, motion=M.keys([(t_card - 0.1, {"alpha": 0}),
                                                               (t_card + 0.5, {"alpha": 1})], "sine"))
    sc.add("card_text", card_text_svg(), wc=0, motion=M.combine(
        M.keys([(t_card, {"alpha": 0, "s": 0.95, "dy": 18}), (t_card + 0.45, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
               pivot=(CARD_X, CARD_Y - 50)),
        M.breathe(0.004, 4.0, pivot=(CARD_X, CARD_Y - 50))))
    sw0, sw1 = t_card + 0.15, t_card + 0.75
    sc.add("swash_l", swash_svg(-1), wc=0,
           reveal=lambda t: {"mode": "right", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    sc.add("swash_r", swash_svg(1), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, sw0, sw1, "inout"), "soft": 30},
           motion=M.keys([(sw0 - 0.01, {"alpha": 0}), (sw0, {"alpha": 1})], "linear"))
    th = t_card + 0.35
    sc.add("heart", card_heart_svg(), wc=0, motion=M.combine(
        M.keys([(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back",
               pivot=HEART),
        heartbeat(th + 0.6, HEART)))

    # ------------------------------------------------------------------ camera
    # (time, centre x, viewport width, viewport bottom), monotone-cubic through the keys (v1 technique).
    ck = [(0.0, 2050, 1500, 1555), (0.6, 2050, 1500, 1555),
          (t_if, 2025, 1440, 1548),
          (l_ask.end + 0.3, 1935, 1160, 1482), (t_love, 1922, 1130, 1474),
          (t_sky + 0.1, 1520, 2120, 1712),
          (t_isr + 0.45, CAM_WIDE_X, 3040, 1838), (t_jon - 0.2, CAM_WIDE_X + 4, 3010, 1836),
          (t_you + 1.3, 1705, 2700, 1830), (t_back - 0.2, 1705, 2700, 1830),
          (t_chance + 0.6, CAM_WIDE_X + 4, 3000, 1836), (t_card - 0.2, CAM_WIDE_X + 4, 3000, 1834),
          (max(T, t_card + 1), CAM_WIDE_X - 4, 2960, 1832)]
    cx_k = [(k[0], k[1]) for k in ck]
    cx_k.insert(5, (t_sea + 0.1, 1715))   # x only: front-load the westward sweep so the first leap is in frame
    cx_f = smooth_keys(cx_k)
    cw_f = smooth_keys([(k[0], k[2]) for k in ck])
    cb_f = smooth_keys([(k[0], k[3]) for k in ck])

    def cam(t):
        w = cw_f(t)
        return Cam(cx_f(t), cb_f(t) - w * 9 / 32, w)
    sc.camera = cam

    # ------------------------------------------------------------------ fx
    sc.fx = [
        # God's presence round Jonah while the question is asked (warm sparkles drifting down)
        sparkles_from((JONAH_X - 220, jy - 440, JONAH_X + 260, jy - 285), t_up + 0.2, 8, count=9, t1=t_love + 0.6,
                      color=(255, 238, 180), size=(6, 12), period=1.9, seed=41),
        # the "?" bursts into golden sparkles
        burst_fx(Q_POS[0], Q_POS[1] - 70, t_love + 0.05, n=14, dist=(110, 230), dur=1.1, size=(11, 20), seed=43),
        sparkles_from((170, 870, 800, 1090), t_isr + 0.1, -6, count=12, t1=t_isr + 4.2, color=(255, 236, 170),
                      size=(6, 12), period=1.7, seed=47),
        FX.sparkles((CITY_X0 + 40, CITY_Y - 230, CITY_X1 - 40, CITY_Y - 40), count=16, t0=t_nin + 0.1,
                    color=(255, 236, 170), size=(6, 13), period=1.8, drift=0, seed=31),
        sparkles_from((JONAH_X - 170, jy - 400, JONAH_X + 170, jy - 110), t_jon + 0.1, -14, count=8, t1=t_jon + 3.6,
                      color=(255, 240, 190), size=(6, 12), period=1.5, seed=53),
        # the first stars twinkle (upper sky, clear of the high clouds, streaks and the end card)
        twinkle_fx(star_points((220, 160, 960, 560), 5, 61), t_chance + 1.2, period=2.4, seed=61),
        twinkle_fx(star_points((2420, 150, 3120, 520), 5, 62), t_chance + 1.5, period=2.9, seed=62),
        twinkle_fx(star_points((1000, 150, 2380, 300), 4, 63), t_chance + 1.8, size=(8, 14), period=2.1, seed=63),
        FX.motes((200, 700, 3100, 1450), count=40, t0=t_isr - 0.2, color=(255, 236, 190), size=(2.5, 6),
                 alpha=120, seed=17),
        burst_fx(mini[0], mini[1] - 10, th2 + 0.05, n=8, dist=(40, 80), dur=0.9, size=(6, 11), seed=59),
        FX.sparkles((HEART[0] - 110, HEART[1] - 70, HEART[0] + 110, HEART[1] + 40), count=7, t0=th + 0.2,
                    color=(255, 240, 200), size=(7, 14), period=1.4, drift=0, seed=5),
        FX.tint(PAPER_RGB, lambda t: 1.0 - M.progress(t, paper_dip[0], paper_dip[1], "sine")),
    ]

    # ------------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-12, fade_in=0.8, fade_out=1.6, pan=-0.3)
    sc.sfx("sparkle", t_love - 0.05, gain_db=-11, pan=0.2)
    # evening birds until the first stars, then the crickets ('night') take over
    sc.sfx("birds", t_isr - 0.4, dur=t_chance + 1.5 - (t_isr - 0.4), gain_db=-19, fade_in=1.2, fade_out=2.0,
           pan=0.1)
    sc.sfx("sparkle", t_you, gain_db=-12)
    sc.sfx("cloth", t_back + 1.9, gain_db=-20, pan=0.2)
    sc.sfx("sparkle", t_chance, gain_db=-14, pan=-0.3)
    sc.sfx("night", t_chance, dur=T - t_chance + 0.8, gain_db=-22, fade_in=2.0, fade_out=1.6)
    sc.sfx("cloth", t_even + 2.0, gain_db=-21, pan=-0.05)    # the two meeting doves land side by side
    sc.sfx("pop", th2, gain_db=-18, pan=-0.05)               # ... and their tiny heart pops
    sc.sfx("chime", t_card, gain_db=-8)
    return sc
