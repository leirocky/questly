"""Scene 12 — the pictures of Jonah's prayer (Jonah 2:3-9), remembered from inside the fish.

A dream-like memory painted on a tall stage (2112 x 2376): soft teal water at the top, the dark-blue flanks
and gnarled stone "roots" of undersea mountains down the sides, and a quiet sandy hollow at their foot. It is
shown inside a big thought bubble (memory_frame, output space, drawn like s19's flashback bubble: a puffy
cream cloud ring with an ink outline round the picture, the dark of the belly outside it) with a soft dark
indigo multiply vignette inside, so a small child sees at once that this is Jonah remembering. The bubble
enters at the end of the opening dissolve (never as a see-through ghost over s11): three little thought puffs
rise from where s11's last frame shows Jonah kneeling (0.55-0.95 s; his head ~ (840, 460) output px; move
TRAIL / MEM_C0 if s11's end framing changes), the bubble pops up beside them with the picture in it (0.8 s,
s12 80% in) and grows to fill the frame (1.0-2.1 s) before he plunges in. The cloud ring is drawn on a canvas
padded past the frame edges, so its outer puffs stay round while the bubble is small. It leaves
when the golden light fills the page: the cloud ring swells out past the frame edges and fades into the
white-out, and we are back inside the great fish with no frame (v1 / s11 belly, drawn in the stage's top
2112 x 1188 region).

Story beats (keyed to the narration chunks; Jonah speaks the whole scene):
  L0 '你把我丢进深海，大水包围着我，'  he plunges in from the top just after the opening dissolve (kept out of it
                                     so he never double-exposes with s11's kneeling Jonah), trailing bubbles,
                                     then drifts in the deep ('float', worried); soft current swirls circle
                                     him, loose kelp leaves and bubbles drift by.
     '海草缠在我的头上。'             a ribbon of seaweed floats in on the current and wraps over his head-cloth
                                     (gently — it slides over the top and down the back; the tail streams up).
  L1 '我一直往下沉，沉到了海底大山的脚下。'  the camera sinks with him past the mountain flanks; he lands softly
                                     at their foot ('脚下') in a little puff of sand.
  L2 '我快要支持不住的时候，'          slumped, tired, in the dim deep (the light dims a little more).
     '就想起了耶和华。'               he kneels and folds his hands (hard pose cut sold by a squash-and-hop); a
                                     tiny warm light glows at his hands.
     '我的祷告，一直达到了你的面前。' a stream of golden sparkles rises from his hands up out of the picture;
                                     warm light answers from above and a soft cone of light (with faint ray
                                     streaks) reaches down, its leading edge a soft arc of glow.
  L3 '你把我从深坑里，救了上来！'     the beam reaches him; he springs up, arms raised, and rises in the light
                                     (the seaweed slips off and drifts away); the light fills the page.
  L4 '我要大声感谢你。'               inside the fish again (s11's belly, warm glow): kneeling, hands raised.
     '我答应你的事，一定会做到。'     hands folded, a solemn little nod (the vow).
     '救恩属于耶和华！'               arms raised high, happy — the golden glow is fullest, sparkles everywhere.
The last second is a calm hold in the glowing belly.

God is never drawn: only warm light, a beam and sparkles.
Engine notes: blend="screen" saturates, so glows use "add"/"normal" (as in v1). Deep layers are switched off and
belly layers on at T_SW (inside the fully golden frame of the white-out), where the camera also cuts from the deep
to the belly region. Cost is kept down by merging the water with the parallax far peaks, giving the beam's
radial reveal mask only to its lower piece (the part on screen while it reveals), and precomputing the
memory bubble (ring + dark outside + vignette) as one multiply-and-add per frame.
"""
import math
import random
import re

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s06_fish as V6
from art.scenes_v1 import s07_belly as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.paths import OUT_H, OUT_W
from engine.scene import Scene

W, H = 2112, 2376

# ------------------------------------------------------------------ the deep (whole stage)
FLOOR = 2090                 # sand at the foot of the mountains where Jonah lands
JXD = 1060.0                 # Jonah's x on the deep floor
JSD = 1.05                   # Jonah's scale in the deep
JB0 = (1080.0, 640.0)        # the drifting Jonah is drawn with his bbox centre here (motion moves him)

# ------------------------------------------------------------------ the belly (top 2112 x 1188 of the stage)
JX, JY, JS = V.JX, V.JY, V.JS
GX, GY = V.GX, V.GY
TOP = (V.TOP[0], V.TOP[1] + 10)
PX, PY, PRX, PRY = V.PX, V.PY, V.PRX, V.PRY
NEAR_I = V.NEAR_I

_PUNCT = "，。！？：；、…—“”‘’（）,.!?:; "


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


def phrase_t(line, phrase, where=0.0, fallback=None):
    """Estimated time of ``phrase`` inside the subtitle chunk that contains it (chunk start + its share of the
    chunk's characters; punctuation counts as a short pause). ``fallback`` = fraction of the line if missing."""
    for c in line.chunks:
        if phrase in c.text:
            txt = c.text.rstrip(_PUNCT)

            def w(s):
                return sum(0.8 if ch in _PUNCT else 1.0 for ch in s)
            i = txt.index(phrase) + int(round(where * len(phrase)))
            return c.start + (c.end - c.start) * w(txt[:i]) / max(1e-6, w(txt))
    if fallback is not None:
        return line.start + (line.end - line.start) * fallback
    raise KeyError(f"{phrase!r} not in {line.text!r}")


def chunk_t(line, phrase, fallback):
    try:
        return line.at(phrase)
    except KeyError:
        return line.start + (line.end - line.start) * fallback


def swap(t_on, t_off):
    """Hard on/off switch of a pose layer (no crossfade between different poses)."""
    return lambda t: Tf(alpha=1.0 if t_on <= t < t_off else 0.0)


def apply_tf(pt, tf, pivot):
    """Stage position of point pt after a layer motion tf (rotation / scale about the pivot, then dx, dy)."""
    px = tf.px if tf.px is not None else pivot[0]
    py = tf.py if tf.py is not None else pivot[1]
    a = math.radians(tf.rot)
    x, y = (pt[0] - px) * tf.sx, (pt[1] - py) * tf.sy
    return (px + tf.dx + x * math.cos(a) - y * math.sin(a), py + tf.dy + x * math.sin(a) + y * math.cos(a))


# ================================================================== Jonah (library rig, custom poses)


def jfig(x, y, s, pose, expr=None, marks=True, **over):
    """Jonah drawn by the library rig, optionally with a modified pose record (e.g. kneeling with raised arms).
    Returns (markup, head_chain, bbox) where head_chain(markup_in_head_coords) places markup on his head (same
    transform chain as the head-cloth), and bbox is the anchor-relative bbox at scale 1."""
    # NOTE: this leans on private internals of art/characters.py (POSES, _figure, _jonah_design, _ADULT,
    # _wrap_out, _LAST, the design dict's 'front' callback and its state keys, and the figure's outer
    # <g transform>). Fail loudly if any of that changes, rather than silently drawing the seaweed off his head.
    for name in ("POSES", "_figure", "_jonah_design", "_ADULT", "_wrap_out", "_LAST"):
        assert hasattr(C, name), f"s12 jfig: art.characters.{name} is gone — update s12_deep.jfig"
    assert pose in C.POSES, f"s12 jfig: unknown pose {pose!r}"
    ps = dict(C.POSES[pose])
    ps.update(over)
    D = C._jonah_design(False)
    cap = {}

    def front(st):
        cap["Hc"], cap["ha"], cap["R"] = st["Hc"], st["ha"], st["m"]["R"]
        return ""
    D["front"] = front
    inner, bbox = C._figure(D, C._ADULT, ps, expr or ps["expr"], 1, marks)
    assert {"Hc", "ha", "R"} <= cap.keys(), (
        "s12 jfig: the design 'front' callback was not called with Hc/ha/m.R — the seaweed cannot be placed")
    m = re.match(r'<g transform="([^"]+)">', inner)
    assert m, "s12 jfig: the figure markup no longer starts with <g transform=...> — head chain unknown"
    tf = m.group(1)
    markup = C._wrap_out(inner, x, y, s, 1, f"jonah-{pose}")
    pts = dict(C._LAST)
    assert "head" in pts and "hands" in pts, "s12 jfig: art.characters._LAST lacks head/hands"
    hc, ha = cap["Hc"], cap["ha"]

    def chain(head_markup):
        return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5g},{s:.5g})"><g filter="url(#wobble-fine)">'
                f'<g transform="{tf}"><g transform="translate({hc[0]:.2f},{hc[1]:.2f}) rotate({ha:.2f})">'
                f'{head_markup}</g></g></g></g>')
    sp = lambda p: (x + p[0] * s, y + p[1] * s)  # noqa: E731
    info = dict(R=cap["R"], bbox=bbox, head=sp(pts["head"]), hands=[sp(p) for p in pts["hands"]])
    return markup, chain, info


ARMS_V = dict(arms=(("fk", 128, 150), ("fk", -132, -155)), hands=("open", "open"))     # thanks (a V)
ARMS_HIGH = dict(arms=(("fk", 150, 168), ("fk", -150, -168)), hands=("open", "open"))  # praise (high)
FLOAT_UP = dict(spin=-6, arms=(("fk", 140, 160), ("fk", -140, -160)))                 # rising in the light


# ------------------------------------------------------------------ the seaweed ribbon on his head
# Centre line in head units (R = head radius; +x = the face side, y down): it comes in from the water in front
# of / above his face, slides over the top of the head-cloth, down the back of the head to the shoulder, and on
# (when it slips off) down and away behind him.
WEED_CTRL = [(4.6, -3.7), (3.6, -2.95), (2.6, -2.2), (1.65, -1.62), (0.8, -1.24), (0.0, -1.17), (-0.62, -1.02),
             (-1.04, -0.62), (-1.22, -0.05), (-1.2, 0.56), (-1.04, 1.16), (-1.3, 1.9), (-1.9, 2.6), (-2.6, 3.3),
             (-3.4, 4.1), (-4.3, 4.9), (-5.2, 5.7)]
_STEPS = 10
WEED_PTS = V._catmull(WEED_CTRL, _STEPS)
WEED_S = [0.0]
for _i in range(1, len(WEED_PTS)):
    WEED_S.append(WEED_S[-1] + math.dist(WEED_PTS[_i - 1], WEED_PTS[_i]))
S_ON0 = WEED_S[4 * _STEPS]      # where the ribbon first touches the head-cloth (front top)
S_ON1 = WEED_S[10 * _STEPS]     # where it leaves the head (behind the neck, at the shoulder)
LEN_A = (S_ON1 - S_ON0) + 0.35  # the main ribbon: the wrapped part + a short tip curling over the brow
LEN_B = 3.0


def _weed_at(s):
    """Point and unit normal on the ribbon path at arc length s (linear extrapolation past the ends)."""
    if s <= 0:
        (x0, y0), (x1, y1) = WEED_PTS[0], WEED_PTS[1]
        d = math.dist((x0, y0), (x1, y1))
        tx, ty = (x1 - x0) / d, (y1 - y0) / d
        return (x0 + tx * s, y0 + ty * s), (-ty, tx)
    if s >= WEED_S[-1]:
        (x0, y0), (x1, y1) = WEED_PTS[-2], WEED_PTS[-1]
        d = math.dist((x0, y0), (x1, y1))
        tx, ty = (x1 - x0) / d, (y1 - y0) / d
        e = s - WEED_S[-1]
        return (x1 + tx * e, y1 + ty * e), (-ty, tx)
    lo, hi = 0, len(WEED_S) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if WEED_S[mid] <= s:
            lo = mid
        else:
            hi = mid
    u = (s - WEED_S[lo]) / max(1e-9, WEED_S[hi] - WEED_S[lo])
    (x0, y0), (x1, y1) = WEED_PTS[lo], WEED_PTS[hi]
    d = math.dist((x0, y0), (x1, y1)) or 1.0
    tx, ty = (x1 - x0) / d, (y1 - y0) / d
    return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), (-ty, tx)


def _ribbon(R, s_lead, length, width, col, phase, shift=(0.0, 0.0), amp=0.18):
    """One seaweed blade whose leading end is at arc length s_lead (head coords, px = units * R)."""
    n = 30
    cl = []
    for i in range(n + 1):
        s = s_lead - length + length * i / n
        (x, y), (nx, ny) = _weed_at(s)
        if s < S_ON0:
            f = min(1.0, (S_ON0 - s) / 1.3)
        elif s > S_ON1:
            f = min(1.0, (s - S_ON1) / 1.0)
        else:
            f = 0.0
        off = amp * f * math.sin(2 * math.pi * s / 3.4 - phase)
        cl.append(((x + shift[0] + nx * off) * R, (y + shift[1] + ny * off) * R))
    left, right = [], []
    for i, p in enumerate(cl):
        a, b = cl[max(i - 1, 0)], cl[min(i + 1, n)]
        d = math.dist(a, b) or 1.0
        nx, ny = -(b[1] - a[1]) / d, (b[0] - a[0]) / d
        u = i / n
        w = width * R * (math.sin(math.pi * min(0.97, 0.05 + u)) ** 0.55) * (1 + 0.22 * math.sin(i * 1.3 + phase))
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    out = S.path(S.smooth_path(left + right[::-1]), fill=col, sw=2.4)
    mid = S.smooth_path(cl[3:-3], closed=False)
    out += (f'<path d="{mid}" fill="none" stroke="{S.shade(col, 0.35)}" stroke-width="{0.05 * R:.1f}" '
            f'stroke-linecap="round" opacity="0.75"/>')
    return out


def weed_head(R, p, phase):
    """Both ribbons in head coords. p: 0 = floating in front of him, 1 = wrapped, 2 = slipped off behind."""
    if p <= 1:
        sa = (S_ON0 - 0.3) + (S_ON1 - S_ON0 + 0.3) * p
    else:
        sa = S_ON1 + (p - 1) * (LEN_A + 3.0)
    pb = min(1.0, max(0.0, p * 1.12 - 0.12)) if p <= 1 else p
    if pb <= 1:
        sb = (S_ON0 - 0.5) + (S_ON1 - 0.25 - S_ON0 + 0.5) * pb
    else:
        sb = S_ON1 - 0.25 + (pb - 1) * (LEN_B + 3.4)
    return (_ribbon(R, sb, LEN_B, 0.13, "#5e8a4a", phase + 1.1, shift=(0.1, 0.16), amp=0.16) +
            _ribbon(R, sa, LEN_A, 0.2, P["olive"], phase))


# ================================================================== deep-sea painting
WATER = [(0, "#7cbcc8"), (0.16, "#59a3b9"), (0.36, "#4287a8"), (0.55, "#33688f"), (0.75, "#294a7a"),
         (1, "#21365f")]
MT = dict(top="#56679b", bottom="#323f6e", edge="#283460", rim="#93a7d2", ledge="#2a355f")
FAR = dict(a="#5b86ac", b="#4d779f", ink="#3d5d84")

L_RIDGE = [(-140, 440), (0, 455), (100, 540), (170, 690), (222, 870), (272, 1060), (322, 1250), (385, 1450),
           (462, 1650), (552, 1825), (650, 1950), (750, 2040), (850, 2095)]
R_RIDGE = [(2260, 330), (2120, 372), (2020, 492), (1960, 672), (1910, 872), (1858, 1082), (1798, 1292),
           (1730, 1500), (1652, 1700), (1562, 1872), (1462, 1995), (1352, 2070), (1262, 2102)]


def _lumpy(ridge, side, seed):
    """Densify a ridge line and push rounded rock lumps out of it (side +1: the mass is on the left)."""
    r = random.Random(seed)
    dense = V._catmull(ridge, 5)
    out = []
    n = len(dense)
    for i, (x, y) in enumerate(dense):
        a, b = dense[max(0, i - 1)], dense[min(n - 1, i + 1)]
        d = math.dist(a, b) or 1.0
        nx, ny = (b[1] - a[1]) / d * side, -(b[0] - a[0]) / d * side
        k = 14 * math.sin(i * 0.95 + seed) + 9 * math.sin(i * 2.3 + 2 * seed) + r.uniform(-4, 6)
        out.append((x + nx * k, y + ny * k))
    return out


def _tube(cl, w0, w1):
    """Tapered closed shape around an open centre line (rock roots)."""
    n = len(cl)
    left, right = [], []
    for i, p in enumerate(cl):
        a, b = cl[max(i - 1, 0)], cl[min(i + 1, n - 1)]
        d = math.dist(a, b) or 1.0
        nx, ny = -(b[1] - a[1]) / d, (b[0] - a[0]) / d
        u = i / (n - 1)
        w = lerp(w0, w1, u ** 0.8) * (1 + 0.08 * math.sin(i * 1.7))
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    return S.smooth_path(left + right[::-1], tension=0.9)


def deep_bg():
    """Water gradient, soft light shafts from far above, depth haze — one opaque full-stage layer."""
    defs = S.lin_grad("dw", WATER)
    defs += S.lin_grad("dshaft", [(0, "#f4fbe6", 0.0), (0.08, "#eef9e6", 0.34), (0.5, "#d8f3ec", 0.12),
                                  (1, "#d8f3ec", 0)])
    defs += S.rad_grad("dtopglow", [(0, "#e8f6ee", 0.55), (0.5, "#cdeee8", 0.18), (1, "#cdeee8", 0)])
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#dw)"/>'
    b += '<ellipse cx="900" cy="-80" rx="1300" ry="620" fill="url(#dtopglow)"/>'
    sh = ""
    for x, w, lean, ln in [(560, 110, 260, 1500), (820, 70, 300, 1300), (1040, 150, 330, 1700),
                           (1330, 80, 360, 1400), (1560, 120, 390, 1550), (300, 60, 210, 1100),
                           (1820, 70, 420, 1250)]:
        sh += (f'<path d="M{x},-40 L{x + w},-40 L{x + w + lean},{ln} L{x + lean - w * 0.5},{ln} Z" '
               f'fill="url(#dshaft)"/>')
    b += S.g(sh, filter="soft")
    # faint drifting plankton specks painted into the water (static texture)
    r = random.Random(5)
    sp = ""
    for _ in range(140):
        x, y = r.uniform(0, W), r.uniform(0, H)
        sp += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5, 3.5):.1f}" fill="#d6f0ee" '
               f'opacity="{r.uniform(0.12, 0.3) * (1.1 - y / H * 0.5):.2f}"/>')
    b += sp
    return b, defs


def far_mountains():
    """Hazy far pinnacles of the undersea mountains with kelp silhouettes (they move a little with the camera:
    parallax). Lighter than the near flanks but close to the water colour, so the deep stays deep."""
    defs = ""
    b = ""
    peaks = [  # (ridge from left foot over the top to the right foot, colour top, colour bottom, seed)
        ([(-260, 2700), (-160, 1700), (-40, 1260), (90, 1010), (190, 905), (280, 930), (360, 1060), (430, 1170),
          (520, 1230), (610, 1420), (720, 1760), (860, 2200), (960, 2700)], "#47709c", "#2c4a78", 2),
        ([(1180, 2700), (1300, 2150), (1420, 1700), (1520, 1380), (1610, 1180), (1690, 1060), (1770, 1030),
          (1850, 1110), (1930, 1300), (2040, 1560), (2200, 1900), (2320, 2700)], "#47709c", "#2c4a78", 5),
        ([(420, 2700), (560, 2160), (690, 1760), (790, 1520), (880, 1400), (960, 1350), (1040, 1380),
          (1130, 1470), (1240, 1660), (1360, 1960), (1480, 2700)], "#3f6894", "#2a4573", 8),
    ]
    for k, (ridge, c0, c1, seed) in enumerate(peaks):
        gid = f"fm{k}"
        defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{min(y for _, y in ridge)}" '
                 f'x2="0" y2="2300"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/>'
                 f'</linearGradient>')
        lump = _lumpy(ridge, 1, seed)
        b += S.path(S.smooth_path(lump, tension=0.8), fill=f"url(#{gid})", stroke=False)
        b += S.path(S.smooth_path(lump[1:-1], closed=False, tension=0.8), stroke=False,
                    extra='stroke="#2c4670" stroke-width="3.5" fill="none" opacity="0.7"')
        # rim light along the upper ridge and a few soft ledges
        top = [(x, y + 9) for x, y in lump if y < min(yy for _, yy in ridge) + 380]
        if len(top) > 2:
            b += S.path(S.smooth_path(top, closed=False), stroke=False,
                        extra='stroke="#7fa3c6" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.4" '
                              'filter="url(#soft)"')
        r = random.Random(seed)
        for _ in range(5):
            i = r.randint(3, len(lump) - 4)
            x, y = lump[i]
            if y > 2250:
                continue
            w = r.uniform(80, 160)
            cx = (ridge[0][0] + ridge[-1][0]) / 2
            x2 = x + (cx - x) * r.uniform(0.15, 0.35)
            b += (f'<path d="M{x2 - w / 2:.0f},{y + 40:.0f} q{w / 2:.0f},{-w * 0.14:.0f} {w:.0f},0" stroke="#6f93b8" '
                  f'stroke-width="6" fill="none" stroke-linecap="round" opacity="0.32"/>')
    # far kelp forests on the slopes (soft silhouettes)
    kelp = ""
    for i, (x, y0, h, lean) in enumerate([(120, 1500, 320, 25), (200, 1420, 260, -18), (640, 1700, 360, 20),
                                          (1300, 1820, 300, -22), (1720, 1450, 340, 18), (1830, 1500, 260, -15),
                                          (980, 1900, 280, 14), (380, 1900, 300, -20)]):
        pts = [(x + lean * math.sin(k / 5 * math.pi * 1.3) * (k / 5), y0 - h * k / 5) for k in range(6)]
        kelp += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="#355d88" stroke-width="{16 - i % 3 * 3}" fill="none" stroke-linecap="round" '
                             f'opacity="0.7"')
        for k in range(1, 5):
            px, py = pts[k]
            sd = 1 if k % 2 else -1
            kelp += (f'<ellipse cx="{px + sd * 18:.0f}" cy="{py:.0f}" rx="22" ry="8" fill="#355d88" opacity="0.7" '
                     f'transform="rotate({sd * -30} {px + sd * 18:.0f} {py:.0f})"/>')
    b += kelp
    defs += S.lin_grad("fhaze", [(0, "#4287a8", 0), (0.45, "#33688f", 0.2), (1, "#21365f", 0.5)])
    b += f'<rect x="-20" y="900" width="{W + 40}" height="{H}" fill="url(#fhaze)"/>'
    return S.g(b, filter="wobble"), defs


def deep_far():
    """Water + light shafts + the far peaks in one layer (it moves a little with the camera: parallax).
    The water is painted 300 px past the stage top so the shift never shows an edge."""
    b0, d0 = deep_bg()
    b1, d1 = far_mountains()
    return doc(f'<g transform="translate(0,-300)"><rect x="-20" y="0" width="{W + 40}" height="320" '
               f'fill="#7cbcc8"/></g>' + b0 + b1, d0 + d1)


def _mass(ridge, side, gid, seed):
    """One mountain flank: lumpy ridge, gradient body, ledges, rim light; side +1 = left mass."""
    lump = _lumpy(ridge, side, seed)
    end_x, end_y = lump[-1]
    edge_x = -200 if side > 0 else W + 200
    mid_x = (end_x + edge_x) / 2
    body_pts = lump + [(end_x - side * 70, end_y + 8), (mid_x, 2080), (edge_x, 2120), (edge_x, lump[0][1])]
    d = S.smooth_path(body_pts, tension=0.7)
    out = S.path(d, fill=f"url(#{gid})", sw=5)
    # inner shading toward the stage edge
    out += S.path(d, fill=f"url(#{gid}x)", stroke=False)
    # ledges (rock shelves) roughly parallel to the ridge, inside the mass
    r = random.Random(seed + 9)
    for k in range(9):
        i0 = r.randint(2, len(lump) - 12)
        seg = lump[i0:i0 + r.randint(5, 9)]
        off = r.uniform(50, 230)
        pts = [(x - side * off, y + r.uniform(8, 30)) for x, y in seg]
        out += S.path(S.smooth_path(pts, closed=False), stroke=False,
                      extra=f'stroke="{MT["ledge"]}" stroke-width="{r.uniform(5, 9):.1f}" fill="none" '
                            f'stroke-linecap="round" opacity="0.55"')
        hi = [(x + side * 6, y - 9) for x, y in pts[1:-1]]
        if len(hi) > 1:
            out += S.path(S.smooth_path(hi, closed=False), stroke=False,
                          extra=f'stroke="{MT["rim"]}" stroke-width="4" fill="none" stroke-linecap="round" '
                                f'opacity="0.35"')
    # rim light along the ridge (light from above)
    rim = [(x - side * 12, y + 8) for x, y in lump[1:-2]]
    out += S.path(S.smooth_path(rim, closed=False), stroke=False,
                  extra=f'stroke="{MT["rim"]}" stroke-width="16" fill="none" stroke-linecap="round" opacity="0.38" '
                        f'filter="url(#soft)"')
    return out


def near_mountains():
    """Both mountain flanks, the sandy floor at their foot and the stone roots — one static layer.
    Order: floor -> roots -> flanks (their feet hide the roots' bases) -> plants."""
    defs = ""
    for gid, x0, x1 in (("mtl", -100, 900), ("mtr", W + 100, 1250)):
        defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="400" x2="0" y2="{H}">'
                 f'<stop offset="0" stop-color="{MT["top"]}"/><stop offset="0.55" stop-color="{S.mix(MT["top"], MT["bottom"], 0.6)}"/>'
                 f'<stop offset="1" stop-color="{MT["bottom"]}"/></linearGradient>')
        defs += (f'<linearGradient id="{gid}x" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">'
                 f'<stop offset="0" stop-color="{MT["edge"]}" stop-opacity="0.6"/>'
                 f'<stop offset="0.6" stop-color="{MT["edge"]}" stop-opacity="0.12"/>'
                 f'<stop offset="1" stop-color="{MT["edge"]}" stop-opacity="0"/></linearGradient>')
    b = ""
    # the sandy floor at the foot of the mountains (a soft hollow in the middle — the 'pit')
    defs += S.lin_grad("dfl", [(0, "#7a86ab"), (0.35, "#5d6a95"), (1, "#3f4a78")])
    fl = [(-200, 2150), (200, 2120), (560, 2100), (860, 2092), (1060, 2086), (1260, 2094), (1560, 2104),
          (1900, 2125), (2300, 2150), (2300, H + 200), (-200, H + 200)]
    b += S.g(S.path(S.smooth_path(fl, tension=0.6), fill="url(#dfl)", sw=5), filter="wobble")
    b += f'<ellipse cx="{JXD + 10}" cy="2130" rx="330" ry="46" fill="#3f4a78" opacity="0.35" filter="url(#blur-md)"/>'
    det = ""
    for i, (x, y, w) in enumerate(((300, 2190, 220), (620, 2160, 180), (1500, 2170, 200), (1840, 2200, 240),
                                   (950, 2230, 260), (1300, 2260, 220), (520, 2290, 240))):
        det += (f'<path d="M{x - w / 2},{y} q{w / 4},-10 {w / 2},0 t{w / 2},0" stroke="#9aa6c8" stroke-width="5" '
                f'fill="none" stroke-linecap="round" opacity="0.45"/>')
    for (x, y, rr) in ((420, 2215, 18), (455, 2228, 11), (1650, 2235, 16), (1220, 2300, 12), (760, 2320, 14),
                       (1980, 2290, 20)):
        det += (f'<ellipse cx="{x}" cy="{y}" rx="{rr * 1.4}" ry="{rr}" fill="{S.mix(MT["top"], "#9aa6c8", 0.4)}" '
                f'stroke="{P["ink"]}" stroke-width="3"/>')
    det += V6._starfish(1180, 2215, 26, "#e7926f", rot=15) + V6._starfish(760, 2262, 20, "#f0b45c", rot=-10)
    det += V6._shell(905, 2178, 17) + V6._shell(1400, 2300, 20)
    b += S.g(det, filter="wobble-fine")

    # the stone roots of the mountains: knobbly fingers of rock coming out from under each mountain's foot,
    # arching over the sand and dipping into it toward the hollow
    defs += S.lin_grad("root", [(0, "#62739f"), (0.55, "#47558c"), (1, "#343f72")])
    roots = [  # centre line (from inside the mountain), width there, width at the tip
        ([(300, 2030), (460, 2050), (580, 2032), (680, 2040), (770, 2075), (830, 2125), (848, 2165)], 74, 11),
        ([(80, 2150), (260, 2175), (420, 2172), (540, 2196), (630, 2240), (668, 2300)], 86, 13),
        ([(1830, 2030), (1660, 2052), (1540, 2036), (1440, 2046), (1360, 2080), (1305, 2128), (1290, 2168)], 74, 11),
        ([(2040, 2150), (1860, 2178), (1700, 2176), (1580, 2200), (1500, 2244), (1468, 2302)], 86, 13),
    ]
    rt = ""
    for cl, w0, w1 in roots:
        dense = V._catmull(cl, 8)
        rt += S.path(_tube(dense, w0, w1), fill="url(#root)", sw=4.5)
        n = len(dense)
        hi = []
        for i, (x, y) in enumerate(dense[1:-5], start=1):
            u = i / (n - 1)
            hi.append((x, y - lerp(w0, w1, u ** 0.8) * 0.58))
        rt += S.path(S.smooth_path(hi, closed=False), stroke=False,
                     extra=f'stroke="{MT["rim"]}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.5"')
        # knuckles: little creases across the root
        for j in (int(n * 0.38), int(n * 0.55), int(n * 0.72)):
            x, y = dense[j]
            ww = lerp(w0, w1, (j / (n - 1)) ** 0.8) * 0.75
            rt += (f'<path d="M{x - 4:.0f},{y - ww:.0f} q-9,{ww:.0f} 0,{ww * 1.7:.0f}" stroke="{MT["ledge"]}" '
                   f'stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.65"/>')
        # a soft shadow on the sand under the arch
        x, y = dense[int(n * 0.55)]
        rt += f'<ellipse cx="{x:.0f}" cy="{y + w0 * 0.55:.0f}" rx="{w0 * 1.6:.0f}" ry="{w0 * 0.2:.0f}" fill="#2a3360" opacity="0.4" filter="url(#soft)"/>'
    b += S.g(rt, filter="wobble")
    # sand banked up against the tips (they dip into the floor)
    for (x, y, rx) in ((848, 2172, 46), (668, 2306, 60), (1290, 2175, 46), (1468, 2308, 60)):
        b += S.g(f'<path d="M{x - rx},{y + 8} Q{x},{y - 22} {x + rx},{y + 8} Z" fill="#7782a8" stroke="{P["ink"]}" '
                 f'stroke-width="3"/>', filter="wobble-fine")

    # the two mountain flanks (their feet sit on the sand and cover the roots' bases)
    b += _mass(L_RIDGE, 1, "mtl", 3) + _mass(R_RIDGE, -1, "mtr", 7)

    # sea plants and anemones on the ledges of the flanks (mid-depth: lighter, friendly)
    plants = ""
    for (x, y, s_, v) in ((150, 640, 0.45, 2), (238, 905, 0.5, 0), (300, 1160, 0.55, 3), (420, 1530, 0.6, 2),
                          (1985, 590, 0.45, 0), (1915, 880, 0.5, 2), (1840, 1160, 0.55, 3), (1700, 1580, 0.6, 1)):
        plants += PR.seaweed(x, y, s_, variant=v)
    plants += V6._anemone(205, 790, 0.7, "#e9877f") + V6._anemone(1950, 770, 0.6, "#f0a65a")
    plants += V6._anemone(360, 1370, 0.75, "#d98bc0") + V6._anemone(1765, 1400, 0.7, "#e9877f")
    b += S.g(plants, opacity=0.8)
    plants2 = (PR.seaweed(560, 1990, 0.55, 1) + PR.seaweed(1580, 1985, 0.6, 2) + PR.seaweed(1640, 2215, 0.5, 3) +
               PR.seaweed(470, 2262, 0.5, 2) + V6._anemone(650, 1995, 0.75, "#f0a65a") +
               V6._anemone(1470, 2000, 0.7, "#d98bc0"))
    b += plants2
    return doc(b, defs)


def foreground():
    """Dark rock shapes framing the bottom corners of the deep (nearest plane)."""
    rock = "#252f58"
    b = S.path(S.smooth_path([(-120, H + 100), (-110, 2210), (40, 2160), (200, 2190), (320, 2290), (380, H + 100)]),
               fill=rock, sw=5)
    b += S.path(S.smooth_path([(1820, H + 100), (1880, 2270), (2000, 2190), (2150, 2170), (2260, 2200),
                               (2260, H + 100)]), fill=rock, sw=5)
    b += ('<path d="M30,2195 q90,-20 170,10" stroke="#5b6c9f" stroke-width="8" fill="none" stroke-linecap="round" '
          'opacity="0.5"/><path d="M1990,2205 q90,-26 180,-6" stroke="#5b6c9f" stroke-width="8" fill="none" '
          'stroke-linecap="round" opacity="0.5"/>')
    return doc(S.g(b, filter="wobble"))


def jelly(x, y, s, col, seed=0):
    """A small friendly jellyfish (same design as s10): translucent bell, frilly rim, sleepy smile, tentacles."""
    rng = np.random.default_rng(seed)
    ink = P["ink"]
    tent = ""
    for i in range(5):
        tx = x + (-34 + 17 * i) * s
        L = (90 + rng.uniform(-10, 30)) * s
        pts = [(tx + 9 * s * math.sin(k * 1.4 + i), y + 12 * s + L * k / 4) for k in range(5)]
        tent += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="{S.shade(col, -0.15)}" stroke-width="{4.5 * s:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.8"')
    for dx in (-10, 10):
        pts = [(x + dx * s + 12 * s * math.sin(k * 1.1 + dx), y + 10 * s + 18 * s * k) for k in range(5)]
        tent += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="{S.shade(col, 0.25)}" stroke-width="{11 * s:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.85"')
    bell = (f"M{x - 56 * s:.1f},{y + 12 * s:.1f} C{x - 60 * s:.1f},{y - 50 * s:.1f} {x - 30 * s:.1f},{y - 74 * s:.1f} "
            f"{x:.1f},{y - 74 * s:.1f} C{x + 30 * s:.1f},{y - 74 * s:.1f} {x + 60 * s:.1f},{y - 50 * s:.1f} "
            f"{x + 56 * s:.1f},{y + 12 * s:.1f} ")
    for i in range(7):
        x1 = x + 56 * s - (i + 1) * 16 * s
        bell += f"Q{x1 + 8 * s:.1f},{y + 22 * s:.1f} {x1:.1f},{y + 12 * s:.1f} "
    bell += "Z"
    body = tent + S.path(bell, fill=col, sw=3.5 * s, extra='fill-opacity="0.9"')
    body += (f'<path d="M{x - 36 * s:.1f},{y - 30 * s:.1f} Q{x - 30 * s:.1f},{y - 58 * s:.1f} {x - 6 * s:.1f},'
             f'{y - 62 * s:.1f}" stroke="#fff6f0" stroke-width="{7 * s:.1f}" fill="none" stroke-linecap="round" '
             f'opacity="0.7"/>')
    for ex in (-16, 16):
        body += (f'<path d="M{x + ex * s - 7 * s:.1f},{y - 16 * s:.1f} q{7 * s:.1f},-7 {14 * s:.1f},0" stroke="{ink}" '
                 f'stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>')
    body += (f'<path d="M{x - 6 * s:.1f},{y - 4 * s:.1f} q{6 * s:.1f},{6 * s:.1f} {12 * s:.1f},0" stroke="{ink}" '
             f'stroke-width="{3 * s:.1f}" fill="none" stroke-linecap="round"/>')
    for ex in (-30, 30):
        body += (f'<ellipse cx="{x + ex * s:.1f}" cy="{y - 6 * s:.1f}" rx="{8 * s:.1f}" ry="{5 * s:.1f}" '
                 f'fill="{P["cheek"]}" opacity="0.7"/>')
    return S.g(body, filter="wobble-fine")


def kelp_leaf(x, y, s, rot, col):
    """A loose kelp leaf drifting in the current."""
    d = (f"M{x:.1f},{y - 60 * s:.1f} C{x + 26 * s:.1f},{y - 30 * s:.1f} {x + 22 * s:.1f},{y + 30 * s:.1f} {x:.1f},"
         f"{y + 64 * s:.1f} C{x - 22 * s:.1f},{y + 30 * s:.1f} {x - 26 * s:.1f},{y - 30 * s:.1f} {x:.1f},{y - 60 * s:.1f} Z")
    out = S.path(d, fill=col, sw=3)
    out += (f'<path d="M{x:.1f},{y - 50 * s:.1f} Q{x + 5 * s:.1f},{y:.1f} {x:.1f},{y + 54 * s:.1f}" '
            f'stroke="{S.shade(col, 0.35)}" stroke-width="3" fill="none" opacity="0.8"/>')
    return S.g(out, filter="wobble-fine", transform=f"rotate({rot} {x} {y})")


def swirl_svg(cx, cy, radii, seed, col="#d8f2f0"):
    """Soft current swirls: tapered comma-shaped arcs circling a centre."""
    r = random.Random(seed)
    b = ""
    for rad in radii:
        a0 = r.uniform(0, 360)
        span = r.uniform(70, 120)
        n = 16
        outer, inner = [], []
        for i in range(n + 1):
            u = i / n
            a = math.radians(a0 + span * u)
            rr = rad * (1 - 0.12 * u)
            w = 13 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.7 + 1
            outer.append((cx + (rr + w) * math.cos(a), cy + (rr + w) * math.sin(a)))
            inner.append((cx + (rr - w) * math.cos(a), cy + (rr - w) * math.sin(a)))
        b += S.path(S.smooth_path(outer + inner[::-1]), fill=col, stroke=False, extra='opacity="0.62"')
        # a little curl at the head of the arc
        a = math.radians(a0 + span)
        hx, hy = cx + rad * 0.88 * math.cos(a), cy + rad * 0.88 * math.sin(a)
        b += (f'<circle cx="{hx + 14 * math.cos(a + 1.6):.1f}" cy="{hy + 14 * math.sin(a + 1.6):.1f}" r="7" '
              f'fill="none" stroke="{col}" stroke-width="4" opacity="0.55"/>')
    return doc(S.g(b, filter="wobble"))


def glow_bulbs(spots, seed=0):
    """Little glowing sea-lamps (bioluminescent bulbs on short stalks) on the roots — gentle light in the deep."""
    b = ""
    for (x, y, s_) in spots:
        b += f'<circle cx="{x}" cy="{y - 30 * s_:.0f}" r="{46 * s_:.0f}" fill="#7fe6d8" opacity="0.22" filter="url(#soft)"/>'
    for (x, y, s_) in spots:
        for k, (dx, h, rr) in enumerate(((-14, 34, 10), (2, 48, 12), (16, 28, 8))):
            bx, by = x + dx * s_, y - h * s_
            b += S.g(f'<path d="M{x + dx * s_ * 0.4:.1f},{y:.1f} Q{x + dx * s_:.1f},{y - h * 0.5 * s_:.1f} {bx:.1f},{by:.1f}" '
                     f'stroke="#3f6a7a" stroke-width="{4 * s_:.1f}" fill="none" stroke-linecap="round"/>'
                     f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{rr * s_:.1f}" fill="#a8f0e2" stroke="#2a5a66" '
                     f'stroke-width="2.6"/><circle cx="{bx - rr * s_ * 0.3:.1f}" cy="{by - rr * s_ * 0.3:.1f}" '
                     f'r="{rr * s_ * 0.32:.1f}" fill="#f2fff8"/>', filter="wobble-fine")
    return doc(b)


# ================================================================== effects


def bubble_fx(sources, seed=3, t_end=1e9, avoid=None):
    """Bubbles from moving emitters.
    sources: (emitter(t)->(x, y), t0, t1, rate, rise, size, spread, alpha[, vx]); vx = sideways drift px/s.
    avoid(t) -> (x, y, r_in, r_out) or None: bubbles fade out inside that circle (Jonah's face, stage px)."""
    rng = np.random.default_rng(seed)
    parts = []
    for src in sources:
        fn, t0, t1, rate, rise, size, spread, alpha = src[:8]
        vx = src[8] if len(src) > 8 else 0.0
        n = max(1, int((t1 - t0) * rate))
        ts = t0 + (np.arange(n) + rng.uniform(0, 1, n)) / rate
        for i in range(n):
            ex, ey = fn(ts[i])
            parts.append((ts[i], ex + rng.uniform(-spread, spread), ey + rng.uniform(-spread, spread) * 0.5,
                          rng.uniform(*size), rise * rng.uniform(0.7, 1.3), rng.uniform(0, 6.3), alpha,
                          vx * rng.uniform(0.75, 1.25)))
    arr = np.array(parts, np.float64)

    def fx(frame, t, view):
        if t >= t_end:
            return frame
        live = arr[(arr[:, 0] <= t) & (arr[:, 0] > t - 5)]
        if not len(live):
            return frame
        face = avoid(t) if avoid is not None else None
        ov = None
        d = None
        for ts, x, y, r, sp, ph, al, vx in live:
            age = t - ts
            yy = y - sp * age - 22 * age * age
            xx = x + vx * age + 10 * math.sin(age * 4.5 + ph) * min(1, age * 2)
            fade = min(1.0, age / 0.12, max(0.0, (5 - age) / 1.0))
            if face is not None:
                fd = math.hypot(xx - face[0], yy - face[1])
                fade *= min(1.0, max(0.0, (fd - face[2]) / (face[3] - face[2])))
                if fade <= 0.02:
                    continue
            ox, oy = view.to_out(xx, yy)
            rr = r * view.scale * (0.55 + 0.45 * min(1.0, age / 0.4))
            if not (-40 < ox < frame.size[0] + 40 and -40 < oy < frame.size[1] + 40):
                continue
            if ov is None:
                ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(ov)
            a = int(al * fade)
            d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=(215, 240, 245, a // 5),
                      outline=(236, 250, 250, a), width=max(2, int(rr / 5)))
            d.ellipse([ox - rr * 0.5, oy - rr * 0.6, ox - rr * 0.12, oy - rr * 0.22], fill=(255, 255, 250, a))
        if ov is not None:
            frame.alpha_composite(ov)
        return frame
    return fx


def prayer_stream(src, y_top, level, count=46, seed=31, color=(255, 230, 150)):
    """Golden sparkles rising quickly from Jonah's folded hands up out of the picture (his prayer).
    level(t) 0..1 sets how many are lit; src = (x, y) stage px."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 1, count)
    sp = rng.uniform(230, 360, count)
    sz = rng.uniform(10, 21, count)
    wob = rng.uniform(0, 6.3, count)
    order = rng.permutation(count) / count
    span = src[1] - y_top

    def fx(frame, t, view):
        k = float(level(t))
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(count):
            if order[i] > k:
                continue
            u = (ph[i] + sp[i] * t / span) % 1.0
            yy = src[1] - u * span
            xx = src[0] + (14 + 40 * u) * math.sin(t * 1.7 + wob[i] + u * 5)
            env = min(1.0, u / 0.08, (1 - u) / 0.15)
            tw = 0.65 + 0.35 * math.sin(t * 6 + i * 2.1)
            a = int(240 * env * tw * min(1.0, (k - order[i]) * 5 + 0.3))
            if a <= 4:
                continue
            ox, oy = view.to_out(xx, yy)
            V._star(d, ox, oy, sz[i] * view.scale * (0.6 + 0.4 * tw), color, a)
        frame.alpha_composite(ov)
        return frame
    return fx


# ------------------------------------------------------------------ the memory bubble (output space)
# The deep is Jonah's remembered prayer-picture, so it is shown INSIDE a big thought bubble, drawn the way s19
# draws its flashback bubble: a puffy cream cloud ring with an umber ink outline round a window with an ink rim
# and a soft pale-aqua glow just inside it. Outside the cloud: the dark of the belly (navy). Inside the window a
# soft indigo multiply vignette darkens the picture toward the rim.
MEM_C = (960.0, 528.0)                       # window centre at full size (output px)
MEM_A, MEM_B, MEM_N = 896.0, 478.0, 3.4      # window half-width, half-height, superellipse exponent
MEM_CREAM, MEM_UNDER, MEM_GLOW = "#f6efdf", "#dedbe2", "#bfe0ea"
MEM_NAVY = (22, 24, 56)                      # the dark round the bubble
MEM_MUL = (46, 50, 108)                      # vignette multiply colour (dark indigo)
# the opening thought trail: little puffs rising from s11's last frame's Jonah (his head ~ (840, 460) out px,
# facing right) to where the bubble pops up; the bubble then grows to fill the frame
TRAIL = [(905, 352, 11), (948, 318, 16), (1002, 278, 22)]
# the bubble's centre and scale when it pops up: far enough right that even at its pop overshoot (k ~0.325)
# its puffs keep a trail-sized gap (~28 px) from the last trail puff instead of half-burying it (the growing
# bubble then passes over the trail, nearest puff first, one or two frames each, at ~1.17-1.3 s)
MEM_C0, MEM_K0 = (1370.0, 205.0), 0.3
# the cloud ring is drawn on a canvas this much bigger than the frame on every side: its outer puffs reach
# ~58 px past the frame edges (+ the 6.5 px ink stroke and the wobble), and while the bubble is small (the
# entrance) they must stay round instead of being cut flat by the frame-sized canvas
MEM_PAD = 110


def _superellipse(a, b, cx, cy, count=240):
    pts = []
    for i in range(count):
        th = 2 * math.pi * i / count
        c, s = math.cos(th), math.sin(th)
        pts.append((cx + a * math.copysign(abs(c) ** (2 / MEM_N), c),
                    cy + b * math.copysign(abs(s) ** (2 / MEM_N), s)))
    return pts


def _puff_ring(a, b, cx, cy, spacing, rmin, rmax, seed):
    """Puffs evenly spaced (by arc length) round a superellipse."""
    pts = _superellipse(a, b, cx, cy, 960)
    acc = [0.0]
    for i in range(1, len(pts) + 1):
        acc.append(acc[-1] + math.dist(pts[i - 1], pts[i % len(pts)]))
    per = acc[-1]
    n = max(8, int(round(per / spacing)))
    r = random.Random(seed)
    out, j = [], 0
    for k in range(n):
        s = per * (k + 0.37) / n
        while acc[j + 1] < s:
            j += 1
        x, y = pts[j % len(pts)]
        out.append((x, y, r.uniform(rmin, rmax)))
    return out


def memory_ring_svg(pad=MEM_PAD):
    """The cloud ring (window cut out by an even-odd clip) + the window's glow and ink rims, in output px on a
    canvas padded by ``pad`` px on every side (output pixel (x, y) is canvas pixel (x + pad, y + pad))."""
    cx, cy = MEM_C
    ink = P["ink"]
    win = _superellipse(MEM_A, MEM_B, cx, cy)
    win_d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in win) + " Z"
    puffs = _puff_ring(MEM_A + 30, MEM_B + 28, cx, cy, 110, 48, 80, 12)   # big uneven bumps, like s19's bubble
    ring = ""
    for x, y, rr in puffs:
        ring += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{MEM_CREAM}" stroke="{ink}" stroke-width="6.5"/>'
    for x, y, rr in puffs:
        fill = MEM_UNDER if y > cy + MEM_B * 0.62 else MEM_CREAM
        ring += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr - 1:.1f}" fill="{fill}"/>'
    body = _superellipse(MEM_A + 26, MEM_B + 24, cx, cy)
    ring += S.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in body) + " Z", fill=MEM_CREAM, stroke=False)
    e0, ex, ey = -pad - 10, OUT_W + pad + 10, OUT_H + pad + 10
    defs = (f'<clipPath id="memout"><path clip-rule="evenodd" d="M{e0},{e0} H{ex} V{ey} H{e0} Z '
            f'{win_d}"/></clipPath>')
    out = f'<g clip-path="url(#memout)">{S.g(ring, filter="wobble")}</g>'
    out += (f'<path d="{win_d}" fill="none" stroke="{MEM_GLOW}" stroke-width="8" opacity="0.4" '
            f'filter="url(#soft)"/>')
    out += S.g(f'<path d="{win_d}" fill="none" stroke="{ink}" stroke-width="4.5"/>', filter="wobble")
    return S.svg_doc(f'<g transform="translate({pad},{pad})">{out}</g>', defs=defs,
                     w=OUT_W + 2 * pad, h=OUT_H + 2 * pad)


def memory_trail_svg():
    ink = P["ink"]
    b = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MEM_CREAM}" stroke="{ink}" stroke-width="5"/>'
                for x, y, r in TRAIL)
    return S.svg_doc(S.g(b, filter="wobble-fine"), w=OUT_W, h=OUT_H)


def memory_frame(level, bubble, trail, step=0.04):
    """The memory bubble in one output-space effect: picture * vignette, then the dark outside and the cloud
    ring over it. Precomputed per quantised vignette level as one multiplier M and one premultiplied addend P
    (frame' = frame * M + P), so a held frame costs one multiply and one add.
      level(t)  vignette strength 0..1 (<= 0: no bubble at all)
      bubble(t) (k, cx, cy, f): the bubble scaled by k about MEM_C and moved to centre (cx, cy) (the outside
                stays dark), and its opacity f (ring, dark outside and vignette fade together)
      trail(t)  [(scale, alpha)] for the TRAIL puffs (drawn over the dark outside)
    The ring is rasterised on a canvas padded by MEM_PAD px on every side, because its outer puffs reach past
    the frame edges. Held (k = 1) and opening out (k > 1), only its frame-sized centre crop is used (in M / P).
    While the bubble is smaller than the frame (the entrance), the picture and the dark outside (M0 / P0, no
    ring) are scaled with the bubble and the whole padded ring is composited over them, so its outer puffs stay
    round instead of being cut flat by the frame edges. Both are resampled once, anti-aliased (see shrink)."""
    from engine import raster
    from engine import watercolor as WC
    import cv2
    pad = MEM_PAD
    PW, PH = OUT_W + 2 * pad, OUT_H + 2 * pad
    ring = WC.watercolor(raster.rasterize(memory_ring_svg(pad), PW, PH), seed=12, strength=0.5)
    ring = np.asarray(ring, np.float32) / 255.0
    a_rp = ring[..., 3:4]
    ring_pm = ring[..., :3] * a_rp
    # the whole padded ring, premultiplied (rgb * a, a), for the entrance
    RP = np.dstack([(ring_pm * 255 + 0.5).astype(np.uint8), (a_rp[..., 0] * 255 + 0.5).astype(np.uint8)])
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    ux, uy = np.abs(xx - pad - MEM_C[0]) / MEM_A, np.abs(yy - pad - MEM_C[1]) / MEM_B
    rho = (ux ** MEM_N + uy ** MEM_N) ** (1 / MEM_N)        # 1 on the window rim
    a_op = np.clip((rho - 1.0) * 400 + 0.5, 0, 1)[..., None]   # outside the window (under the ring)
    # the dark outside, past the ring (padded canvas): where the trail puffs may show
    clear = (a_op[..., 0] * (1 - a_rp[..., 0]) * 255 + 0.5).astype(np.uint8)
    crop = (slice(pad, pad + OUT_H), slice(pad, pad + OUT_W))
    a_r, ring_pm, a_out = a_rp[crop], ring_pm[crop], a_op[crop]
    ux, uy, rho = ux[crop], uy[crop], rho[crop]
    # vignette: soft toward the rim, deepest in the window's corners
    vb = 0.65 * np.clip((rho - 0.5) / 0.5, 0, 1) ** 1.7 + 0.35 * np.clip((np.hypot(ux, uy) - 0.55) / 0.75, 0, 1) ** 1.4
    vb = np.clip(vb, 0, 1)[..., None]
    navy = np.array(MEM_NAVY, np.float32) / 255.0
    mul = 1.0 - np.array(MEM_MUL, np.float32) / 255.0
    keep = (1 - a_out) * (1 - a_r)
    P_rgb = navy * a_out * (1 - a_r) + ring_pm
    P_u8 = np.dstack([(P_rgb * 255 + 0.5).astype(np.uint8), np.zeros((OUT_H, OUT_W), np.uint8)])
    keep0 = 1 - a_out                                       # the same without the ring (the entrance)
    P0_u8 = np.dstack([(navy * a_out * 255 + 0.5).astype(np.uint8), np.zeros((OUT_H, OUT_W), np.uint8)])
    del ring, a_rp, a_op, a_r, ring_pm, a_out, P_rgb, yy, xx, ux, uy, rho
    one = np.full((OUT_H, OUT_W, 4), 255, np.uint8)
    opaque = np.full((OUT_H, OUT_W), 255, np.uint8)
    cache = {}

    def mult(q, ring_on=True):
        if (q, ring_on) not in cache:
            s = q * step
            m = (1.0 - s * vb * mul) * (keep if ring_on else keep0)
            cache[q, ring_on] = np.dstack([(m * 255 + 0.5).astype(np.uint8), opaque])
        return cache[q, ring_on]

    def shrink(img, k, ox, oy, cx, cy, border):
        """img scaled by k < 1 so that its pixel (ox, oy) lands on (cx, cy), in a frame. One bicubic resample,
        anti-aliased by a light Gaussian prefilter (sigma (1/k - 1) / 2) that fades out as k -> 1, so the
        picture stays as crisp as the held frame it settles into at T_GROW1 (an area resize followed by a
        bilinear warp blurred it to ~half its fine detail and it snapped into focus when the growth ended);
        while it is tiny (k < 0.2, the first frames of the pop) it is area-filtered to its size first."""
        if k >= 0.2:
            sg = 0.5 * (1.0 / k - 1.0)
            src = cv2.GaussianBlur(img, (0, 0), sg) if sg > 0.05 else img
            A = np.array([[k, 0, cx - k * ox], [0, k, cy - k * oy]], np.float32)
        else:
            h, w = img.shape[:2]
            nw, nh = max(2, int(round(w * k))), max(2, int(round(h * k)))
            lx, ly = nw / w, nh / h
            src = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
            # src pixel (i, j) is img pixel ((i + .5) / lx - .5, (j + .5) / ly - .5)
            A = np.array([[k / lx, 0, cx + k * (0.5 / lx - 0.5 - ox)],
                          [0, k / ly, cy + k * (0.5 / ly - 0.5 - oy)]], np.float32)
        return cv2.warpAffine(src, A, (OUT_W, OUT_H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT,
                              borderValue=border)

    tr = raster.rasterize(memory_trail_svg(), OUT_W, OUT_H)
    puffs = []
    for x, y, r in TRAIL:
        box = (int(x - r - 10), int(y - r - 10), int(x + r + 11), int(y + r + 11))
        puffs.append((np.asarray(tr.crop(box)), (x, y)))

    def fx(frame, t, view):
        s = float(level(t))
        if s <= 0.003:
            return frame
        k, cx, cy, f = bubble(t)
        q = int(round(s / step))
        moved = abs(cx - MEM_C[0]) > 0.05 or abs(cy - MEM_C[1]) > 0.05
        if k <= 0.01:
            arr = np.empty((OUT_H, OUT_W, 4), np.uint8)
            arr[:] = (*MEM_NAVY, 255)
        elif k > 1.001 or (k >= 0.999 and not moved):
            # held, or opening out (the exit): only the ring and the dark outside grow past the frame edges
            M, Pa = mult(q), P_u8
            if k > 1.001:
                A = np.array([[k, 0, cx - k * MEM_C[0]], [0, k, cy - k * MEM_C[1]]], np.float32)
                M = cv2.warpAffine(M, A, (OUT_W, OUT_H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(255, 255, 255, 255))
                Pa = cv2.warpAffine(Pa, A, (OUT_W, OUT_H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(0, 0, 0, 0))
            if f < 0.999:
                M = cv2.addWeighted(M, f, one, 1 - f, 0)
                Pa = cv2.convertScaleAbs(Pa, alpha=f)
            arr = cv2.add(cv2.multiply(np.asarray(frame), M, scale=1 / 255.0), Pa)
        else:
            # popping up / growing (the entrance): the remembered picture and the dark round it are scaled
            # with the bubble, then the whole (padded) cloud ring goes over them
            M0, P0 = mult(q, False), P0_u8
            if f < 0.999:
                M0 = cv2.addWeighted(M0, f, one, 1 - f, 0)
                P0 = cv2.convertScaleAbs(P0, alpha=f)
            arr = cv2.add(cv2.multiply(np.asarray(frame), M0, scale=1 / 255.0), P0)
            arr = shrink(arr, k, MEM_C[0], MEM_C[1], cx, cy, (*MEM_NAVY, 255))
            rw = shrink(RP, k, MEM_C[0] + pad, MEM_C[1] + pad, cx, cy, (0, 0, 0, 0))
            if f < 0.999:
                rw = cv2.convertScaleAbs(rw, alpha=f)
            inv = cv2.subtract(opaque, rw[..., 3])
            arr = cv2.multiply(arr, cv2.merge([inv, inv, inv, opaque]), scale=1 / 255.0)
            rw[..., 3] = 0
            arr = cv2.add(arr, rw)
        im = Image.fromarray(arr, "RGBA")
        for (pim, (x, y)), (ks, al) in zip(puffs, trail(t)):
            if ks <= 0.02 or al <= 0.01:
                continue
            h, w = pim.shape[:2]
            nw, nh = max(1, round(w * ks)), max(1, round(h * ks))
            p = cv2.resize(pim, (nw, nh), interpolation=cv2.INTER_AREA if ks < 1 else cv2.INTER_LINEAR).copy()
            x0, y0 = int(round(x - nw / 2)), int(round(y - nh / 2))
            # the growing bubble passes OVER its trail: keep each puff only where the dark outside shows
            vis = np.full((nh, nw), al, np.float32)
            if k > 0.01:
                gx, gy = np.meshgrid(np.arange(x0, x0 + nw, dtype=np.float32),
                                     np.arange(y0, y0 + nh, dtype=np.float32))
                vis *= cv2.remap(clear, MEM_C[0] + pad + (gx - cx) / k, MEM_C[1] + pad + (gy - cy) / k,
                                 cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=255) / 255.0
            p[..., 3] = (p[..., 3] * vis).astype(np.uint8)
            im.alpha_composite(Image.fromarray(p, "RGBA"), (x0, y0))
        return im
    return fx


# ================================================================== belly helpers (from s11 / v1)


def masked_doc(inner_doc, cx, cy, r, stops, tag):
    """Wrap a full SVG document in a soft radial mask centred at (cx, cy)."""
    defs = (f'<radialGradient id="mg{tag}" gradientUnits="userSpaceOnUse" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}">'
            + "".join(f'<stop offset="{o}" stop-color="#ffffff" stop-opacity="{a}"/>' for o, a in stops)
            + f'</radialGradient><mask id="mk{tag}" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{W + 100}" '
              f'height="{S.H + 100}"><rect x="-50" y="-50" width="{W + 100}" height="{S.H + 100}" fill="url(#mg{tag})"/>'
              f'</mask>')
    return S.svg_doc(f'<g mask="url(#mk{tag})">{inner_doc}</g>', defs=defs)


def glow_cluster(centres):
    out = ""
    pts = []
    for (gi, u, ang, sc_) in centres:
        cx, cy = V._wall_pt(gi, u, math.radians(ang))
        for (ox, oy, r) in ((0, 0, 15), (25, -9, 11), (-21, 9, 10), (6, 21, 8)):
            pts.append((cx + ox * sc_, cy + oy * sc_, r * sc_))
    for x, y, r in pts:
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="#6fd8cc" opacity="0.22" filter="url(#soft)"/>'
    for x, y, r in pts:
        out += S.g(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#9fe6da" stroke="{S.mix(P["ink"], "#2a5a66", 0.4)}" '
                   f'stroke-width="2.6"/><circle cx="{x - r * 0.32:.1f}" cy="{y - r * 0.32:.1f}" r="{r * 0.3:.1f}" '
                   f'fill="#f2fff8"/>', filter="wobble-fine")
    return S.svg_doc(out), (pts[0][0], pts[0][1])


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L = ctx.lines
    L0, L1, L2, L3 = L[0], L[1], L[2], L[3]
    L4 = L[4] if len(L) > 4 else L[3]

    # ---------------------------------------------------------- key times (from the narration chunks)
    t_weed = chunk_t(L0, "海草", 0.62)                  # '海草缠在我的头上' — the seaweed wraps
    t_w0, t_w1 = t_weed - 0.55, t_weed + 1.35          # ribbon floats in ... wrapped
    t_sink0 = L1.start - 0.35                           # '我一直往下沉'
    t_land = phrase_t(L1, "脚下", fallback=0.9) - 0.05  # lands at the foot of the mountains
    t_faint = L2.start                                  # '我快要支持不住的时候'
    t_kneel = chunk_t(L2, "想起", 0.3) + 0.12            # '就想起了耶和华' — kneels and prays
    t_pr = chunk_t(L2, "祷告", 0.58)                     # '我的祷告，一直达到了你的面前' — prayer rises
    t_beam0, t_beam1 = t_pr + 1.0, L3.start + 0.1       # the beam reaches down
    t_lift = L3.start + 0.12                            # '你把我从深坑里，救了上来' — lifted up
    t_wf0 = L3.end + 0.08                               # the page is fully golden-white ...
    t_wf1 = L3.end + 0.20                               # ... until here
    T_SW = (t_wf0 + t_wf1) / 2                          # switch deep -> belly under the white-out
    t_wo0 = L3.end - 0.5                                # white-out starts (late: '救了上来' must read clearly)
    t_wo1 = max(t_wf1 + 0.6, L4.start + 0.2)            # ... and has cleared
    t_vow = chunk_t(L4, "答应", 0.3) + 0.05              # '我答应你的事，一定会做到' — hands folded, a vow
    t_nod = phrase_t(L4, "一定会做到", fallback=0.55)
    t_sal = chunk_t(L4, "救恩", 0.7)                     # '救恩属于耶和华！' — praise, glow fullest
    # the memory bubble's entrance, kept late in (and mostly after) the 1.0 s opening cross-dissolve so it is
    # never a see-through ghost over s11: the thought puffs rise from s11's fading Jonah from T_TRAIL (s12 >= 55%
    # in), the bubble pops up at T_POP (s12 >= 80% in) and grows to fill the frame once the dissolve is over
    T_TRAIL, T_POP, T_GROW0, T_GROW1 = 0.55, 0.8, 1.0, 2.1

    def don(t):
        return t < T_SW

    def deep_gate(m=None):
        g = lambda t: Tf(alpha=1.0 if t < T_SW else 0.0)  # noqa: E731
        return M.combine(m, g) if m is not None else g

    def belly_gate(m=None):
        g = lambda t: Tf(alpha=1.0 if t >= T_SW else 0.0)  # noqa: E731
        return M.combine(m, g) if m is not None else g

    # ================================================================ BELLY (z 0..50, under the deep background)
    stuff = PR.seaweed(1425, 868, 0.42, variant=2)
    stuff += PR.jar(1500, 862, 0.5, rot=78)
    stuff += V.shell(1580, 882, 0.8)
    stuff += V.starfish(705, 975, 30, rot=12)
    stuff += V.shell(1180, 1010, 0.9, "#e7c2d8")
    pool = f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="url(#pool)" {S.STROKE_THIN}/>'
    # the belly as s11 ends: the cool belly with the warm-lit belly over it (radial mask around Jonah) at 85%,
    # swelling to its fullest on '救恩属于耶和华' (both switched on at the white-out)
    sc.add("belly_cool", V.belly_svg(V.COOL, "c", "#1a1430", 1.0), z=0, seed=11, motion=belly_gate())
    warm = masked_doc(V.belly_svg(V.WARM, "w", "#2a1420", 0.65), GX + 40, GY + 40, 900,
                      [(0, 1), (0.35, 0.85), (0.7, 0.3), (1, 0)], "w")
    sc.add("belly_warm", warm, z=1, seed=11, wc_edge=0.0, motion=belly_gate(M.keys(
        [(T_SW, {"alpha": 0.85}), (t_sal - 0.2, {"alpha": 0.88}), (t_sal + 1.2, {"alpha": 1.0})], "sine")))
    # the swallowed things and the pool (in front of the glow, as in s11)
    sc.add("belly_props", S.svg_doc(V.dimmed(stuff, 0.9) + V.dimmed(S.g(pool, filter="wobble"), 0.8),
                                    defs=S.rad_grad("pool", [(0, "#3f8c96"), (0.7, "#2a5f70"), (1, "#22465a")])),
           z=9.9, motion=belly_gate())


    clusters = [[(NEAR_I - 1, 0.2, 195, 0.95)], [(NEAR_I, 0.45, 236, 1.2)], [(NEAR_I - 1, 0.5, 318, 0.9)],
                [(NEAR_I - 1, 0.55, 12, 0.8)], [(NEAR_I - 2, 0.45, 300, 0.7)]]
    for j, cl in enumerate(clusters):
        cdoc, _c = glow_cluster(cl)
        sc.add(f"nubs{j}", cdoc, z=3 + j * 0.05, wc=0.3,
               motion=belly_gate(M.combine(lambda t: Tf(alpha=0.55), M.pulse(0.65, 1.0, 2.6 + 0.35 * j, 0.21 * j))))

    # God's light behind Jonah: s11's end state, growing to its fullest on '救恩属于耶和华'
    # (the warm 'ember' core of s11 is folded into the halo here, as a soft normal-blend glow: one layer)
    halo = S.svg_doc(
        f'<circle cx="{GX}" cy="{GY}" r="640" fill="url(#halo)"/>'
        f'<circle cx="{GX}" cy="{GY + 20}" r="430" fill="url(#emb)"/>',
        defs=S.rad_grad("halo", [(0, "#ffe6a6", 0.55), (0.22, "#fbd38a", 0.4), (0.52, "#f2ad5c", 0.2),
                                 (1, "#e8913f", 0)]) +
        S.rad_grad("emb", [(0, "#ffd890", 0.3), (0.35, "#f6b860", 0.2), (0.7, "#e89040", 0.07), (1, "#e89040", 0)]))
    sc.add("halo", halo, z=4, wc=0, motion=belly_gate(M.combine(
        M.keys([(T_SW, {"alpha": 0.8, "s": 1.0}), (t_vow, {"alpha": 0.82, "s": 1.02}),
                (t_sal - 0.2, {"alpha": 0.85, "s": 1.04}), (t_sal + 1.1, {"alpha": 1.0, "s": 1.22})],
               ["linear", "linear", "out"], pivot=(GX, GY)),
        M.breathe(0.03, 2.8, pivot=(GX, GY)))))
    rays = S.svg_doc(S.path(S.rays(GX, GY, 200, 760, n=14, width_deg=4.5), fill="url(#rayg)", stroke=False,
                            extra='filter="url(#blur-md)"'),
                     defs=f'<radialGradient id="rayg" gradientUnits="userSpaceOnUse" cx="{GX}" cy="{GY}" r="760">'
                          f'<stop offset="0.2" stop-color="#6e4c22"/><stop offset="1" stop-color="#6e4c22" '
                          f'stop-opacity="0"/></radialGradient>')
    sc.add("rays", rays, z=5, wc=0, blend="add", motion=belly_gate(M.combine(
        M.keys([(T_SW, {"alpha": 0.75, "s": 1.0}), (t_sal - 0.2, {"alpha": 0.78, "s": 1.0}),
                (t_sal + 1.0, {"alpha": 1.0, "s": 1.12})], ["linear", "out"], pivot=(GX, GY)),
        lambda t: Tf(rot=2.0 * t, px=GX, py=GY))))
    rim = S.svg_doc(f'<ellipse cx="{JX - 20}" cy="{JY - 230}" rx="215" ry="240" fill="url(#rim)"/>',
                    defs=S.rad_grad("rim", [(0, "#22404a"), (0.6, "#0e1c22"), (1, "#000000")]))
    sc.add("rim", rim, z=5.5, wc=0, blend="add", motion=belly_gate(lambda t: Tf(alpha=0.35)))
    beam_body = ""
    for wk in (1.0, 0.72, 0.46, 0.24):
        bx0, bx1 = TOP[0] - 10, GX - 15
        beam_body += (f'<path d="M{bx0 - 80 * wk:.0f},{TOP[1] - 160} L{bx0 + 80 * wk:.0f},{TOP[1] - 160} '
                      f'L{bx1 + 260 * wk:.0f},{JY + 10} L{bx1 - 260 * wk:.0f},{JY + 10} Z" fill="url(#beam)"/>')
    gold_top = (f'<ellipse cx="{TOP[0]}" cy="{TOP[1] - 30}" rx="420" ry="190" fill="url(#gt)"/>')
    beam = S.svg_doc(S.g(beam_body, filter="blur-lg") + gold_top,
                     defs=S.lin_grad("beam", [(0, "#4a3a20", 0.0), (0.15, "#4a3a20", 1), (0.75, "#3e2a14", 0.8),
                                              (1, "#3e2a14", 0.0)]) +
                     S.rad_grad("gt", [(0, "#9a7a40", 1), (0.45, "#7a5a28", 0.6), (1, "#6a4a20", 0)]))
    # the beam from above and the golden opening at the top (s11's end state), one additive layer
    sc.add("beam", beam, z=6, wc=0, blend="add", motion=belly_gate(M.combine(
        M.keys([(T_SW, {"alpha": 0.82}), (t_sal - 0.2, {"alpha": 0.82}), (t_sal + 1.0, {"alpha": 1.0})], "sine"),
        M.pulse(0.88, 1.0, 3.1))))

    # Jonah in the belly: thanks (hands raised) -> the vow (hands folded, a nod) -> praise (arms high)
    shadow = C.ground_shadow(JX + 10, JY, 1.0, width=320, opacity=0.4)
    thanks, _, _ = jfig(JX, JY, JS, "kneel_pray", expr="happy", **ARMS_V)
    vow, _, _ = jfig(JX, JY, JS, "kneel_pray", expr="peaceful")
    praise, _, pinfo = jfig(JX, JY, JS, "kneel_pray", expr="happy", h=-22, **ARMS_HIGH)
    sc.add("jonah_thanks", S.svg_doc(shadow + thanks), z=10, motion=M.combine(
        swap(T_SW, t_vow),
        M.keys([(L4.start + 0.15, {"sy": 1.0, "dy": 0}), (L4.start + 0.4, {"sy": 1.035, "dy": -6}),
                (L4.start + 0.8, {"sy": 1.0, "dy": 0}), (t_vow - 0.18, {"sy": 1.0, "dy": 0}),
                (t_vow, {"sy": 0.95, "dy": 4})], ["out", "inout", "linear", "inout"], pivot=(JX, JY)),
        lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * (t - T_SW) / 3.2), px=JX, py=JY),
        M.breathe(0.01, 3.0, pivot=(JX, JY))))
    sc.add("jonah_vow", S.svg_doc(shadow + vow), z=10.1, motion=M.combine(
        swap(t_vow, t_sal),
        M.keys([(t_vow, {"sy": 0.93, "sx": 1.03, "dy": 7}), (t_vow + 0.3, {"sy": 1.0, "sx": 1.0, "dy": 0}),
                (t_nod - 0.1, {"rot": 0}), (t_nod + 0.24, {"rot": 5.0, "dy": 5}), (t_nod + 0.7, {"rot": 0, "dy": 0}),
                (t_sal - 0.18, {"sy": 1.0, "dy": 0}), (t_sal, {"sy": 0.94, "dy": 5})],
               ["back", "linear", "inout", "inout", "linear", "inout"], pivot=(JX, JY)),
        M.breathe(0.01, 3.0, pivot=(JX, JY), phase=0.3)))
    sc.add("jonah_praise", S.svg_doc(shadow + praise), z=10.2, motion=M.combine(
        swap(t_sal, 1e9),
        M.keys([(t_sal, {"sy": 0.92, "sx": 1.03, "dy": 8}), (t_sal + 0.16, {"sy": 1.05, "sx": 0.98, "dy": -12}),
                (t_sal + 0.42, {"sy": 1.0, "sx": 1.0, "dy": 0}), (t_sal + 1.2, {"rot": -2.5})],
               ["out", "inout", "sine"], pivot=(JX, JY)),
        lambda t: Tf(rot=1.0 * math.sin(2 * math.pi * (t - t_sal) / 3.4), px=JX, py=JY),
        M.breathe(0.012, 2.8, pivot=(JX, JY))))

    for j, (x, y, s_, var, sw, deg, per, ph) in enumerate((
            (1860, 1075, 1.3, 0, 0.2, 2.4, 4.6, 0.0), (2010, 1095, 1.05, 2, -0.15, 3.0, 3.9, 0.35),
            (1710, 1090, 0.9, 1, 0.1, 2.0, 5.3, 0.6))):
        sc.add(f"weed{j}", S.svg_doc(V.dimmed(PR.seaweed(x, y, s_, variant=var, sway=sw), 0.72)), z=12 + j * 0.1,
               motion=belly_gate(M.sway(deg, per, (x, y), ph)))
    fishes = [("pink", 330, 986, 75, 19.0, 0.8), ("yellow", 440, 1010, 80, 20.0, 0.85),
              ("orange", 215, 1032, 80, 17.0, 0.5)]
    for i, (col, xc, yc, A, per, ph) in enumerate(fishes):
        frames = [S.svg_doc(V.dimmed(PR.small_fish(xc, yc, 0.85, fac, col, tail=tl), 0.84))
                  for fac in (1, -1) for tl in (-0.7, 0.7)]

        def fish_frame(t, per=per, ph=ph):
            right = math.cos(2 * math.pi * (t / per + ph)) >= 0
            return float((0 if right else 2) + int(t / 0.3 + ph * 3) % 2)

        def fish_motion(t, A=A, per=per, ph=ph):
            return Tf(dx=A * math.sin(2 * math.pi * (t / per + ph)), dy=4 * math.sin(2 * math.pi * (t / 2.2 + ph)))
        sc.add(f"bfish{i}", frames, z=13 + i * 0.1, frame_at=fish_frame, motion=belly_gate(fish_motion))
    surf = (f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX - 4}" ry="{PRY - 3}" fill="#6fb3bd" opacity="0.36"/>'
            + S.path(f"M{PX - 220},{PY - 30} q40,-10 80,0 t80,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.7"')
            + S.path(f"M{PX + 40},{PY + 24} q35,-9 70,0 t70,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.55"'))
    sc.add("pool_surface", S.svg_doc(surf), z=14, wc=0.4, motion=belly_gate(M.bob(3, 3.0, axis="x")))

    hx1, hx2 = 300.0, 1850.0
    hy1, hy2 = V._rib_top_y(NEAR_I, hx1), V._rib_top_y(NEAR_I, hx2)
    len1 = 300.0
    hang_l = (V.kelp_strand(hx1 - 30, hy1, 230, 34, "#5e7d3c", seed=1, curl=-1) +
              V.kelp_strand(hx1, hy1 + 4, len1, 40, P["olive"], seed=2) +
              V.kelp_strand(hx1 + 36, hy1 - 4, 170, 30, "#4f7a52", seed=3))
    SW_DEG, SW_PER = 2.0, 5.2

    def sway_l(t):
        return SW_DEG * math.sin(2 * math.pi * t / SW_PER)
    sc.add("hang_l", S.svg_doc(V.dimmed(S.g(hang_l, filter="wobble-fine"), 0.78)), z=15,
           motion=belly_gate(M.sway(SW_DEG, SW_PER, (hx1, hy1))))
    hang_r = (V.kelp_strand(hx2 - 24, hy2, 250, 36, P["olive"], seed=4) +
              V.kelp_strand(hx2 + 20, hy2 + 2, 190, 30, "#5e7d3c", seed=5, curl=-1))
    sc.add("hang_r", S.svg_doc(V.dimmed(S.g(hang_r, filter="wobble-fine"), 0.74)), z=15.1,
           motion=belly_gate(M.sway(-1.8, 4.4, (hx2, hy2), 0.3)))

    # drips from the kelp tip into the pool
    tipx, tipy = V.kelp_tip(hx1, hy1 + 4, len1, seed=2)
    DS = 1.2
    DX, DY0 = tipx, tipy + 8
    DTOP = DY0 - 16 * DS
    drips = (L4.start + 0.9, t_vow + 1.4, t_sal + 1.6)
    fall = 0.5

    def drop_motion(t):
        for td in drips:
            if td - 0.6 <= t < td:
                s = 0.3 + 0.7 * progress(t, td - 0.6, td, "out")
                th = sway_l(t)
                qx, qy = V._rot_pt(DX, DTOP, hx1, hy1, th)
                return Tf(dx=qx - DX, dy=qy - DTOP, rot=th, sx=s, sy=s, alpha=1.0, px=DX, py=DTOP)
            if td <= t < td + fall:
                u = (t - td) / fall
                qx, qy = V._rot_pt(DX, DTOP, hx1, hy1, sway_l(td))
                oy = qy - DTOP
                return Tf(dx=qx - DX, dy=oy + (PY - 4 - DY0 - oy) * u * u, alpha=1.0)
        return Tf(alpha=0.0)
    sc.add("drop", S.svg_doc(V.drop_shape(DX, DY0, DS)), z=16, wc=0, motion=belly_gate(drop_motion))

    def ripple_motion(delay):
        def m(t):
            for td in drips:
                ti = td + fall + delay
                if ti <= t < ti + 1.2:
                    u = (t - ti) / 1.2
                    s = 0.4 + 2.6 * M.ease("out")(u)
                    lx = V._rot_pt(DX, DTOP, hx1, hy1, sway_l(td))[0] - DX
                    return Tf(dx=lx, sx=s, sy=s, alpha=0.9 * (1 - u), px=DX, py=PY - 4)
            return Tf(alpha=0.0)
        return m
    ring = S.svg_doc(f'<ellipse cx="{DX:.1f}" cy="{PY - 4}" rx="26" ry="7" fill="none" stroke="{P["sea_pale"]}" '
                     f'stroke-width="3.5"/>')
    sc.add("ripple_a", ring, z=16.1, wc=0, motion=belly_gate(ripple_motion(0.0)))
    sc.add("ripple_b", ring, z=16.2, wc=0, motion=belly_gate(ripple_motion(0.28)))

    # ================================================================ THE DEEP (z 100+)
    def cam_deep(t):
        return deep_cam(t)

    # water + far peaks: parallax (they move down with 22% of the camera's descent)
    CAM_Y0 = 660.0
    sc.add("deep_far", deep_far(), z=100, wc=0.75, wc_edge=0.0,
           motion=deep_gate(lambda t: Tf(dy=0.22 * (cam_deep(t).y - CAM_Y0))))

    # little fish crossing the upper water; jellyfish drifting
    school = [doc(PR.small_fish(300, 430, 0.62, 1, "yellow", tail=tl) +
                  PR.small_fish(220, 480, 0.55, 1, "orange", tail=-tl) +
                  PR.small_fish(370, 500, 0.58, 1, "yellow", tail=-tl) +
                  PR.small_fish(150, 410, 0.5, 1, "orange", tail=tl)) for tl in (0.7, -0.7)]
    sc.add("school", school, z=102, frame_at=lambda t: float(int(t * 5) % 2),
           motion=deep_gate(M.combine(M.drift(vx=38), M.bob(9, 2.3))))

    def jelly_m(x, y, period, phase, rise):
        def m(t):
            u = (t / period + phase) % 1.0
            push = math.sin(math.pi * min(1.0, u / 0.35)) if u < 0.35 else 0.0
            return Tf(dx=8 * math.sin(t * 0.7 + phase * 6), dy=-rise * t - 10 * (t // period + min(1.0, u / 0.35)),
                      sx=1 + 0.07 * push, sy=1 - 0.09 * push, px=x, py=y)
        return m
    sc.add("jelly1", doc(jelly(470, 1000, 0.9, "#f0a8c0", seed=1)), z=102.1,
           motion=deep_gate(jelly_m(470, 1000, 2.4, 0.0, 6)))
    sc.add("jelly2", doc(jelly(1780, 760, 0.7, "#c8a8e8", seed=2)), z=102.2,
           motion=deep_gate(jelly_m(1780, 760, 2.1, 0.4, 5)))
    sc.add("jelly3", doc(jelly(1640, 1720, 0.75, "#f4b8a0", seed=3)), z=102.3,
           motion=deep_gate(jelly_m(1640, 1720, 2.7, 0.7, 4)))

    sc.add("near_mtn", near_mountains(), z=103, wc=0.9, motion=deep_gate())

    # glowing sea-lamps on the roots (pulse softly; light in the deep)
    for j, spots in enumerate(([(470, 2058, 0.8), (1800, 2040, 0.7)], [(640, 2150, 0.65), (1520, 2160, 0.75)])):
        sc.add(f"lamps{j}", glow_bulbs(spots), z=103.5 + j * 0.1, wc=0.3,
               motion=deep_gate(M.pulse(0.6, 1.0, 2.7 + 0.6 * j, 0.3 * j)))

    # ---------------------------------------------------------- light from above (prayer heard) + beam
    top_light = doc(f'<ellipse cx="{JXD - 20}" cy="700" rx="1000" ry="820" fill="url(#tl)"/>',
                    defs=S.rad_grad("tl", [(0, "#8a4c12", 1), (0.4, "#74380a", 0.7), (0.75, "#3e1c06", 0.25),
                                           (1, "#000000", 0)]))

    def top_light_m(t):
        a = 0.85 * progress(t, t_pr + 0.5, t_beam1, "sine") + 0.15 * progress(t, t_lift, t_wf0, "sine")
        return Tf(dy=cam_deep(t).y - 1300, alpha=a)
    sc.add("top_light", top_light, z=104, wc=0, blend="add", motion=deep_gate(top_light_m))

    # the beam: a cone of light fanning out from a narrow source above the picture (nested soft cones) with
    # three faint ray streaks fanning inside it — narrow at the top of the picture, wide at Jonah (additive)
    BX, AY, BOT = JXD - 20, 450, FLOOR + 60
    beam_d = ""
    for wk in (1.0, 0.6, 0.28):
        t0, b0 = 20 + 20 * wk, 660 * wk
        beam_d += (f'<path d="M{BX - t0:.0f},{AY} L{BX + t0:.0f},{AY} L{BX + b0:.0f},{BOT} '
                   f'L{BX - b0:.0f},{BOT} Z" fill="url(#dbeam)"/>')
    rays_d = ""
    for dxb, hwb in ((-420, 48), (50, 66), (440, 44)):
        rays_d += (f'<path d="M{BX + dxb * 0.08 - 7:.0f},{AY + 40} L{BX + dxb * 0.08 + 7:.0f},{AY + 40} '
                   f'L{BX + dxb + hwb:.0f},{BOT} L{BX + dxb - hwb:.0f},{BOT} Z" fill="url(#dray)"/>')
    beam_body = S.g(beam_d, filter="blur-lg") + S.g(rays_d, filter="blur-md")
    beam_defs = (
        f'<linearGradient id="dbeam" gradientUnits="userSpaceOnUse" x1="0" y1="{AY}" x2="0" y2="{BOT}">'
        f'<stop offset="0" stop-color="#8a4c12" stop-opacity="0.15"/>'
        f'<stop offset="0.3" stop-color="#8a4c12" stop-opacity="0.95"/>'
        f'<stop offset="0.8" stop-color="#744210" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="#744210" stop-opacity="0.45"/></linearGradient>'
        f'<linearGradient id="dray" gradientUnits="userSpaceOnUse" x1="0" y1="{AY}" x2="0" y2="{BOT}">'
        f'<stop offset="0" stop-color="#a8682a" stop-opacity="0"/>'
        f'<stop offset="0.35" stop-color="#a8682a" stop-opacity="0.85"/>'
        f'<stop offset="1" stop-color="#8a5418" stop-opacity="0.2"/></linearGradient>')
    # Cost: the engine's radial reveal mask is per-pixel over the layer's crop, so the beam is cut into two
    # complementary pieces (soft alpha ramps over SPLIT0..SPLIT1 that sum to exactly 1): only the lower piece
    # (all the camera can see before the lift: its top is at stage y >= ~1240 until then) carries the reveal;
    # the upper piece switches on at t_beam1, when the beam is fully open and that part is still off screen.
    SPLIT0, SPLIT1 = 1130, 1190

    def beam_piece(k, a0, a1):
        return doc(f'<g mask="url(#bm{k})">{beam_body}</g>', defs=beam_defs + (
            f'<linearGradient id="bs{k}" gradientUnits="userSpaceOnUse" x1="0" y1="{SPLIT0}" x2="0" y2="{SPLIT1}">'
            f'<stop offset="0" stop-color="#ffffff" stop-opacity="{a0}"/>'
            f'<stop offset="1" stop-color="#ffffff" stop-opacity="{a1}"/></linearGradient>'
            f'<mask id="bm{k}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="{W + 400}" height="{H + 400}">'
            f'<rect x="-200" y="-200" width="{W + 400}" height="{H + 400}" fill="url(#bs{k})"/></mask>'))

    # it reaches down from the source: a radial reveal centred on it, so the leading edge is a soft arc of
    # glow that travels down the picture (no flat edge); it ends fully open (r = maxd + soft / 2), and from
    # t_beam1 on the mask is skipped
    # R_MAX = the engine's radial maxd: the farthest corner of the lower piece's alpha bbox, measured as
    # (274, 1130)-(1806, 2280), from the source (BX, AY); re-measure it if the beam geometry changes
    R_MAX, R_SOFT = 1984.0, 420.0

    def beam_reveal(t):
        if t >= t_beam1:
            return {"mode": "down", "frac": 1.0}
        r = lerp(1200.0 - AY, R_MAX + R_SOFT / 2, progress(t, t_beam0, t_beam1, "sine"))
        return {"mode": "radial", "frac": r / R_MAX, "soft": R_SOFT, "cx": BX, "cy": AY}
    beam_m = M.combine(
        M.keys([(t_beam0, {"alpha": 0.0}), (t_beam0 + 0.5, {"alpha": 0.8}), (t_beam1, {"alpha": 0.9}),
                (t_lift + 0.8, {"alpha": 1.0})], ["sine", "inout", "sine"]),
        M.pulse(0.88, 1.0, 2.9))
    sc.add("deep_beam", beam_piece("l", 0, 1), z=104.2, wc=0, blend="add", reveal=beam_reveal,
           motion=deep_gate(beam_m))

    # warm glow around Jonah: a tiny light at his hands on '就想起了耶和华', fullest when he is lifted
    hands_k = jfig(JXD, FLOOR, JSD, "kneel_pray")[2]["hands"][1]
    jglow = doc(f'<circle cx="{hands_k[0]:.0f}" cy="{hands_k[1]:.0f}" r="420" fill="url(#jg)"/>',
                defs=S.rad_grad("jg", [(0, "#8c541a", 1), (0.3, "#6c3c12", 0.8), (0.65, "#361a06", 0.35),
                                       (1, "#000000", 0)]))

    # ---------------------------------------------------------- currents swirling around him (L0)
    def swirl_alpha(t):
        return (0.35 + 0.65 * progress(t, L0.start - 0.2, L0.start + 0.8, "sine")) * \
            (1 - 0.55 * progress(t, t_weed, L0.end, "sine")) * (1 - progress(t, t_sink0 + 0.3, t_sink0 + 1.8, "sine"))

    # ---------------------------------------------------------- Jonah in the deep
    # float (drifting, worried) -> lands: sit_faint (tired) -> kneel_pray (prays) -> rises in the light
    fl_mk, fl_chain, fl_info = jfig(0, 0, JSD, "float", expr="worried")
    bb = fl_info["bbox"]
    fcx, fcy = (bb[0] + bb[2]) / 2 * JSD, (bb[1] + bb[3]) / 2 * JSD
    FAX, FAY = JB0[0] - fcx, JB0[1] - fcy                  # anchor that puts the bbox centre on JB0
    fl_mk, fl_chain, fl_info = jfig(FAX, FAY, JSD, "float", expr="worried")
    LAND_C = (JXD + 22, FLOOR - (bb[3] * JSD - fcy) - 2)   # bbox centre when his feet reach the sand

    def float_pos(t):
        """(dx, dy, rot) of the drifting / sinking Jonah relative to JB0."""
        u = progress(t, t_sink0, t_land, "sine")
        drift_y = 46 * min(1.0, t / max(0.1, t_sink0))
        x = lerp(JB0[0], LAND_C[0], u) + 22 * math.sin(2 * math.pi * t / 6.0) * (1 - u)
        y = lerp(JB0[1], LAND_C[1] - 46, u) + drift_y + 9 * math.sin(2 * math.pi * t / 3.2) * (1 - u)
        rot = 5 * math.sin(2 * math.pi * t / 4.6) * (1 - 0.6 * u) - 6 * u
        return x - JB0[0], y - JB0[1], rot

    # he is kept above the frame through the opening cross-dissolve (so s11's kneeling Jonah never
    # double-exposes with this one) and plunges in from the top of the growing bubble's window on '丢进深海'
    # (~1.6-2.4 s), slowing as the water takes him; only his own layers follow (the swirls stay put: he
    # falls into them)
    ENTER0, ENTER1, ENTER_DY = T_GROW0 + 0.35, T_GROW1 + 0.6, 760.0

    def float_m(t):
        dx, dy, rot = float_pos(t)
        dy -= ENTER_DY * (1.0 - progress(t, ENTER0, ENTER1, "out"))
        return Tf(dx=dx, dy=dy, rot=rot, px=JB0[0], py=JB0[1])

    sc.add("jonah_float", doc(fl_mk), z=110, motion=deep_gate(M.combine(swap(-1, t_land), float_m)))

    # the seaweed ribbon: floats in and wraps over the head-cloth, then its tail waves while he sinks
    NWRAP = 18
    wrap_frames = []
    for k in range(NWRAP):
        p = k / (NWRAP - 1)
        wrap_frames.append(doc(fl_chain(weed_head(fl_info["R"], p, k * 0.75))))
    for k in range(4):
        wrap_frames.append(doc(fl_chain(weed_head(fl_info["R"], 1.0, NWRAP * 0.75 + k * math.pi / 2))))

    def wrap_idx(t):
        if t < t_w1:
            return float(int(round(progress(t, t_w0, t_w1, "inout") * (NWRAP - 1))))
        return float(NWRAP + int((t - t_w1) * 4.5) % 4)
    sc.add("weed_float", wrap_frames, z=110.5, frame_at=wrap_idx, motion=deep_gate(M.combine(
        swap(-1, t_land), float_m, lambda t: Tf(alpha=progress(t, t_w0 - 0.45, t_w0 + 0.05, "sine")))))

    # current swirls follow his drift and circle around him
    for j, (radii, spd, seed) in enumerate((((205, 275, 345), 26.0, 4), ((240, 315), -19.0, 9))):
        sw = swirl_svg(JB0[0], JB0[1], radii, seed)

        def swirl_m(t, spd=spd, j=j):
            dx, dy, _r = float_pos(t)
            return Tf(dx=dx, dy=dy, rot=spd * t, px=JB0[0], py=JB0[1],
                      alpha=swirl_alpha(t) * (0.8 + 0.2 * math.sin(t * 1.9 + j)))
        sc.add(f"swirl{j}", sw, z=109 + j * 0.2, wc=0.3, motion=deep_gate(swirl_m))

    # loose kelp leaves drifting through the current (L0) — the ribbon is one of them
    leaves = [(760, 360, 0.8, 30, P["olive"], 22, 26), (1420, 900, 0.7, -40, "#5e8a4a", -28, 18),
              (1500, 300, 0.6, 60, P["leaf_dark"], -18, 30), (620, 880, 0.65, -20, "#6a8f45", 25, -14)]
    for j, (x, y, s_, rot, col, vx, vr) in enumerate(leaves):
        sc.add(f"leaf{j}", doc(kelp_leaf(x, y, s_, rot, col)), z=108 + j * 0.05, wc=0.6, motion=deep_gate(
            lambda t, x=x, y=y, vx=vx, vr=vr, j=j: Tf(dx=vx * t + 14 * math.sin(t * 0.9 + j),
                                                     dy=10 * math.sin(t * 1.3 + j * 2) - 8 * t,
                                                     rot=vr * math.sin(t * 0.6 + j), px=x, py=y)))

    # landing: sit_faint (tired, slumped) at the foot of the mountains
    sf_mk, sf_chain, sf_info = jfig(JXD, FLOOR, JSD, "sit_faint", expr="tired", marks=False)
    sh_deep = C.ground_shadow(JXD + 10, FLOOR, JSD, width=260, opacity=0.35)
    faint_m = M.combine(
        M.keys([(t_land, {"sy": 0.9, "sx": 1.04, "dy": 6}), (t_land + 0.28, {"sy": 1.0, "sx": 1.0, "dy": 0}),
                (t_kneel - 0.16, {"sy": 1.0, "dy": 0}), (t_kneel, {"sy": 0.95, "dy": 4})],
               ["back", "linear", "inout"], pivot=(JXD, FLOOR)),
        M.breathe(0.014, 3.8, pivot=(JXD, FLOOR)))
    sc.add("jonah_faint", doc(sh_deep + sf_mk), z=110, motion=deep_gate(M.combine(swap(t_land, t_kneel), faint_m)))
    sf_weed = [doc(sf_chain(weed_head(sf_info["R"], 1.0, k * math.pi / 2))) for k in range(4)]
    sc.add("weed_faint", sf_weed, z=110.5, frame_at=lambda t: float(int(t * 3.5) % 4),
           motion=deep_gate(M.combine(swap(t_land, t_kneel), faint_m)))

    # kneels and prays
    kn_mk, kn_chain, kn_info = jfig(JXD, FLOOR, JSD, "kneel_pray")

    kneel_mm = M.combine(
        M.keys([(t_kneel, {"sy": 0.92, "sx": 1.03, "dy": 8}), (t_kneel + 0.16, {"sy": 1.04, "sx": 0.99, "dy": -10}),
                (t_kneel + 0.4, {"sy": 1.0, "sx": 1.0, "dy": 0}), (t_lift - 0.15, {"sy": 1.0, "dy": 0}),
                (t_lift, {"sy": 0.93, "dy": 6})], ["out", "inout", "linear", "inout"], pivot=(JXD, FLOOR)),
        lambda t: Tf(rot=1.0 * math.sin(2 * math.pi * (t - t_kneel) / 3.4) * progress(t, t_kneel + 0.4, t_kneel + 1.2),
                     px=JXD, py=FLOOR),
        M.breathe(0.01, 3.0, pivot=(JXD, FLOOR), phase=0.3))
    sc.add("jonah_kneel", doc(sh_deep + kn_mk), z=110, motion=deep_gate(M.combine(swap(t_kneel, t_lift), kneel_mm)))
    kn_weed = [doc(kn_chain(weed_head(kn_info["R"], 1.0, k * math.pi / 2))) for k in range(4)]
    sc.add("weed_kneel", kn_weed, z=110.5, frame_at=lambda t: float(int(t * 3.5) % 4),
           motion=deep_gate(M.combine(swap(t_kneel, t_lift), kneel_mm)))

    # the glow at his hands
    sc.add("jonah_glow", jglow, z=109.8, wc=0, blend="add", motion=deep_gate(M.combine(
        M.keys([(t_kneel + 0.2, {"alpha": 0, "s": 0.25}), (t_kneel + 1.2, {"alpha": 0.6, "s": 0.4}),
                (t_pr, {"alpha": 0.7, "s": 0.5}), (t_beam1, {"alpha": 0.85, "s": 0.8}),
                (t_lift + 0.6, {"alpha": 1.0, "s": 1.3})], ["sine", "linear", "inout", "out"],
               pivot=hands_k),
        M.breathe(0.04, 2.4, pivot=hands_k))))

    # lifted up: arms raised, happy, rising in the beam (seaweed slips off and drifts away)
    up_probe = jfig(0, 0, JSD, "float", expr="happy", **FLOAT_UP)[2]["bbox"]
    ucx, ucy = (up_probe[0] + up_probe[2]) / 2 * JSD, (up_probe[1] + up_probe[3]) / 2 * JSD
    UC = (JXD - 10, FLOOR - 150)                         # bbox centre at the start of the lift
    up_mk, up_chain, up_info = jfig(UC[0] - ucx, UC[1] - ucy, JSD, "float", expr="happy", **FLOAT_UP)
    up_head = up_info["head"]
    RISE = 1000.0

    def rise_y(t):
        """Front-loaded lift (he leaves the sand right after the squash-hop) that eases off smoothly under the
        white-out instead of stopping: RISE * tanh(raw / RISE) has the raw curve's start and no hard stop."""
        u = max(0.0, t - t_lift)
        return -RISE * math.tanh((160 * u + 120 * u * u) / RISE)

    def up_m(t):
        hop = M.keys([(t_lift, {"sy": 0.9, "sx": 1.04, "dy": 6}), (t_lift + 0.14, {"sy": 1.06, "sx": 0.97, "dy": -8}),
                      (t_lift + 0.4, {"sy": 1.0, "sx": 1.0, "dy": 0})], ["out", "inout"])(t)
        return Tf(dx=8 * math.sin(2 * math.pi * (t - t_lift) / 2.6), dy=rise_y(t) + hop.dy,
                  rot=3 * math.sin(2 * math.pi * (t - t_lift) / 3.0), sx=hop.sx, sy=hop.sy, px=UC[0], py=UC[1])
    sc.add("jonah_up", doc(up_mk), z=110, motion=deep_gate(M.combine(swap(t_lift, 1e9), up_m)))
    NOFF = 12
    off_frames = [doc(up_chain(weed_head(up_info["R"], 1.0 + k / (NOFF - 1), k * 0.8))) for k in range(NOFF)]
    t_off0, t_off1 = t_lift + 0.25, t_lift + 1.7

    def off_m(t):
        b = up_m(t)
        lag = 120 * max(0.0, t - t_off0) ** 1.5
        return Tf(dx=b.dx - 30 * max(0.0, t - t_off0), dy=b.dy + lag, rot=b.rot, sx=b.sx, sy=b.sy, px=b.px, py=b.py,
                  alpha=1 - progress(t, t_off1 - 0.5, t_off1 + 0.2, "sine"))
    sc.add("weed_off", off_frames, z=110.5,
           frame_at=lambda t: float(int(round(progress(t, t_off0, t_off1, "out") * (NOFF - 1)))),
           motion=deep_gate(M.combine(swap(t_lift, 1e9), off_m)))

    # sand puff where he lands
    puff = ""
    for k, (dx, rx, ry) in enumerate(((-120, 90, 34), (-40, 120, 44), (70, 110, 40), (160, 80, 30))):
        puff += f'<ellipse cx="{JXD + dx}" cy="{FLOOR - ry * 0.6:.0f}" rx="{rx}" ry="{ry}" fill="#b9c3dc" opacity="0.55"/>'
    sc.add("puff", doc(S.g(puff, filter="soft")), z=111, wc=0, motion=deep_gate(M.keys(
        [(t_land - 0.02, {"alpha": 0, "sx": 0.5, "sy": 0.4}), (t_land + 0.12, {"alpha": 0.9}),
         (t_land + 1.3, {"alpha": 0, "sx": 1.5, "sy": 1.25, "dy": -30})], ["out", "out"], pivot=(JXD, FLOOR))))

    # foreground: corner rocks and swaying weeds (quantised sway, no crossfades)
    sc.add("fg_rocks", foreground(), z=120, wc=0.8, motion=deep_gate())
    sways = [k / 4 - 1 for k in range(9)]
    weeds_l = [doc(PR.seaweed(90, H + 12, 1.35, 0, sway=s) + PR.seaweed(230, H + 12, 1.0, 2, sway=-s) +
                   PR.seaweed(10, H, 0.9, 3, sway=s * 0.5)) for s in sways]
    weeds_r = [doc(PR.seaweed(1900, H + 12, 0.95, 1, sway=-s) + PR.seaweed(2040, H + 12, 1.3, 0, sway=s) +
                   PR.seaweed(1790, H + 12, 0.8, 2, sway=-s * 0.5)) for s in sways]
    sc.add("weeds_l", weeds_l, z=121, motion=deep_gate(),
           frame_at=lambda t: float(round(4 + 4 * math.sin(2 * math.pi * t / 3.6))))
    sc.add("weeds_r", weeds_r, z=121.1, motion=deep_gate(),
           frame_at=lambda t: float(round(4 + 4 * math.sin(2 * math.pi * t / 3.2 + 1.0))))

    # the upper piece of the beam (see deep_beam above); added last so that the default per-layer seeds
    # (watercolour texture) of every layer added before it stay as they were
    sc.add("deep_beam_top", beam_piece("u", 1, 0), z=104.21, wc=0, blend="add",
           motion=deep_gate(M.combine(beam_m, lambda t: Tf(alpha=1.0 if t >= t_beam1 else 0.0))))

    # ================================================================ camera
    deep_keys = M.cam_keys([
        (0, Cam(1080, CAM_Y0, 1880)),
        (t_sink0 - 0.1, Cam(1076, CAM_Y0 + 30, 1820)),
        (t_land + 0.1, Cam(1066, 1790, 1880)),
        (t_kneel, Cam(1062, 1832, 1740)),
        (t_pr + 0.2, Cam(1062, 1832, 1720)),
        (L3.start, Cam(1066, 1770, 1880)),
        (t_wf0, Cam(1070, 1770, 1960)),
    ], ["sine", "sine", "sine", "linear", "sine", "inout"])
    # during the lift the camera is driven by his rise: his head climbs in frame on a sine curve from where it
    # is at the lift (~y 594 of 1080) to the upper third (YD1) at the white-out, so the camera starts from rest
    # and never outruns him (the squash-and-hop is left out of the follow, so it still reads)
    _c0 = deep_keys(t_lift)
    YD0 = (up_head[1] - _c0.y) * OUT_W / _c0.w + OUT_H / 2
    YD1 = 345.0

    def deep_cam(t):
        c = deep_keys(t)
        if t <= t_lift:
            return c
        yd = lerp(YD0, YD1, math.sin(0.5 * math.pi * progress(t, t_lift, t_wf0, "linear")))
        return Cam(c.x, up_head[1] + rise_y(t) - (yd - OUT_H / 2) * c.w / OUT_W, c.w, c.rot)
    belly_cam = M.cam_keys([(T_SW, Cam(955, 600, W * 0.86)), (T, Cam(930, 592, W * 0.8))], "sine")
    sc.camera = lambda t: deep_cam(t) if t < T_SW else belly_cam(t)

    # ================================================================ effects
    float_head = fl_info["head"]

    faint_head, kneel_head = sf_info["head"], kn_info["head"]

    # bubble emitters sit just in front of / beside the face (never on it) and drift a little to +x, so the
    # bubbles rise beside his face instead of across his eyes; bubble_fx also fades any bubble that wanders
    # over the current head (FACE_R*: stage px around the head centre)
    def jonah_mouth(t):
        if t < t_land:
            return apply_tf((float_head[0] + 75, float_head[1] + 35), float_m(t), JB0)
        if t < t_kneel:
            return faint_head[0] + 66, faint_head[1] + 12
        return kneel_head[0] + 64, kneel_head[1] + 24

    def up_mouth(t):
        b = up_m(t)
        return apply_tf((up_head[0] + 74, up_head[1] + 30), b, UC)

    HR = fl_info["R"] * JSD                             # head radius in stage px (~46)
    FACE_R0, FACE_R1 = 1.2 * HR, 1.55 * HR

    def head_now(t):
        if t < t_land:
            hx, hy = apply_tf(float_head, float_m(t), JB0)
        elif t < t_kneel:
            hx, hy = faint_head
        elif t < t_lift:
            hx, hy = kneel_head
        elif t < T_SW:
            hx, hy = apply_tf(up_head, up_m(t), UC)
        else:
            return None
        return hx, hy, FACE_R0, FACE_R1

    def light_level(t):          # prayer stream: rises on '我的祷告，一直达到了你的面前'; gone before the cut
        if t >= T_SW:
            return 0.0
        return (progress(t, t_pr - 0.1, t_pr + 1.6, "sine") * (1 - 0.5 * progress(t, t_lift, t_lift + 1.0)) *
                (1 - progress(t, t_wo0, t_wf0, "sine")))


    def mem_level(t):             # the soft memory vignette (a touch deeper while he is about to give up)
        if t >= T_SW:
            return 0.0
        return 0.5 + 0.18 * progress(t, t_land, t_faint + 0.8, "sine") * (1 - progress(t, t_kneel, t_pr + 1.0))

    # the memory bubble: the trail puffs pop up from where s11's Jonah kneels (late in the opening dissolve),
    # the bubble pops up beside them with the remembered picture in it and grows to fill the frame before he
    # plunges in; when the golden light fills the page the cloud ring opens out past the frame edges and fades
    # into the white-out, and the belly (the present) comes back without a frame
    t_mx0 = t_wo0 - 0.45

    def mem_bubble(t):
        if t < T_POP:
            return 0.0, MEM_C0[0], MEM_C0[1], 1.0
        if t < T_GROW1:
            # the pop (a little overshoot) runs on into the growth, which eases in from rest: no kink
            kp = MEM_K0 * (0.15 + 0.85 * progress(t, T_POP, T_POP + 0.34, "back"))
            u = progress(t, T_GROW0, T_GROW1, "sine")
            return lerp(kp, 1.0, u), lerp(MEM_C0[0], MEM_C[0], u), lerp(MEM_C0[1], MEM_C[1], u), 1.0
        u = progress(t, t_mx0, t_wf0, "inout")        # swells past the frame corners before it turns see-through
        return 1.0 + 0.7 * u, MEM_C[0], MEM_C[1], 1.0 - progress(t, t_wo0 + 0.05, t_wf0, "sine")

    def mem_trail(t):
        out = []
        for i in range(len(TRAIL)):
            ti, to = T_TRAIL + 0.08 * i, T_GROW0 + 0.4 + 0.05 * i
            k = (0.2 + 0.8 * progress(t, ti, ti + 0.24, "back")) if t >= ti else 0.0
            k *= 1 - 0.8 * progress(t, to, to + 0.26, "in")
            out.append((k, 1 - progress(t, to + 0.12, to + 0.26, "sine")))
        return out

    def warm_wash(t):
        return 0.14 * progress(t, t_lift - 0.2, t_wo0 + 0.4, "sine") if t < T_SW else 0.0

    def whiteout(t):
        return progress(t, t_wo0, t_wf0, "sine") * (1 - progress(t, t_wf1, t_wo1, "sine"))

    def belly_level(t):
        if t < T_SW:
            return 0.0
        return 0.45 + 0.2 * progress(t, L4.start, L4.start + 1.0) + 0.35 * progress(t, t_sal - 0.2, t_sal + 0.8, "sine")

    head_b = pinfo["head"]
    face_b = (head_b[0] - 8, head_b[1] - 2, 112, 118)
    sc.fx = [
        FX.motes((0, 0, W, H), count=70, t1=T_SW, color=(200, 236, 232), size=(3, 6), alpha=70, seed=5),
        FX.sparkles((300, 1700, 1850, 2150), count=14, t1=T_SW, color=(160, 245, 225), size=(4, 9),
                    period=2.2, drift=-6, seed=19),
        bubble_fx([
            (jonah_mouth, 0.2, t_land, 1.6, 95, (5, 12), 10, 190, 12),
            # the landing burst: two puffs beside him (out of the sand), not up through his face
            (lambda t: (JXD - 210, FLOOR - 30), t_land, t_land + 0.25, 22, 120, (5, 14), 40, 200),
            (lambda t: (JXD + 240, FLOOR - 30), t_land, t_land + 0.25, 22, 120, (5, 14), 40, 200),
            (jonah_mouth, t_land + 0.4, t_lift, 0.5, 70, (4, 9), 6, 150, 13),
            (up_mouth, t_lift, T_SW, 3.0, 160, (5, 12), 14, 200, 14),
            # a short trail of bubbles left behind (above) him as he plunges in from the top
            (lambda t: apply_tf((float_head[0] - 6, float_head[1] - 88), float_m(t), JB0),
             ENTER0 + 0.15, ENTER0 + 1.1, 17, 55, (4, 11), 24, 170, 4),
        ], t_end=T_SW, avoid=head_now),
        prayer_stream((hands_k[0], hands_k[1] - 20), hands_k[1] - 1250, light_level),
        V.twinkles((JXD - 360, 1250, JXD + 320, 2050), count=22, t0=t_beam1 - 0.4, color=(255, 236, 170),
                   size=(8, 18), drift=0, seed=23, face=None),
        FX.tint((255, 226, 168), warm_wash),
        memory_frame(mem_level, mem_bubble, mem_trail),
        # belly
        FX.motes((0, 100, W, 950), count=18, t0=T_SW, color=(160, 205, 200), size=(3, 6), alpha=55, seed=5),
        V.rising_sparkles(GX + 10, JY - 20, 150, 230, 40, belly_level, face=face_b),
        V.twinkles((GX - 330, GY - 360, GX + 330, GY + 180), count=22, t0=t_sal - 0.1, color=(255, 240, 190),
                   size=(8, 20), drift=-3, seed=17, face=face_b),
        FX.tint((255, 236, 186), whiteout),
    ]

    # ================================================================ sound
    # the same belly bed as s11 (underwater -12, heartbeat -12, drip -19): the deep is his memory, the water
    # sound runs on through it, so coming back to the belly sounds like the belly we left
    sc.sfx("underwater", 0, dur=T + 0.1, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("pop", T_POP, gain_db=-15, pan=0.3)            # the memory bubble pops up (as s19's bubbles do)
    sc.sfx("bubbles", 0.3, dur=t_land - 0.3, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_weed + 0.15, gain_db=-19)
    sc.sfx("whoosh", t_sink0 + 0.2, gain_db=-20, pan=0.0)
    sc.sfx("thud", t_land, gain_db=-19, duck_db=-5)     # on-picture landing: ducked less, so it is heard
    sc.sfx("bubbles", t_land, dur=1.0, gain_db=-17, fade_out=0.5)
    sc.sfx("cloth", t_kneel - 0.05, gain_db=-17)
    sc.sfx("chime", t_pr, gain_db=-11)
    sc.sfx("sparkle", t_beam1 - 0.3, gain_db=-11)
    sc.sfx("whoosh", t_lift + 0.1, gain_db=-12)
    sc.sfx("bubbles", t_lift + 0.1, dur=1.6, gain_db=-16, fade_out=0.6)
    sc.sfx("chime", t_wo0 + 0.3, gain_db=-10)
    sc.sfx("heartbeat", T_SW - 0.3, dur=T - T_SW + 0.4, gain_db=-12, fade_in=0.9, fade_out=0.9)
    sc.sfx("drip", T_SW - 0.3, dur=T - T_SW + 0.4, gain_db=-19, fade_in=0.9, fade_out=0.9, density=0.6)
    for td in drips:
        sc.sfx("pop", td + fall, gain_db=-20, pan=-0.45)
    sc.sfx("cloth", t_vow - 0.05, gain_db=-17)
    sc.sfx("cloth", t_sal - 0.05, gain_db=-17)
    sc.sfx("chime", t_sal, gain_db=-11)
    sc.sfx("sparkle", t_sal + 0.15, gain_db=-10)
    return sc
