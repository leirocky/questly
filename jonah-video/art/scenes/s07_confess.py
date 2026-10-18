"""Scene 7 (v2) — the sea grows wilder; Jonah tells the sailors to throw him in (Jonah 1:11-12).

Medium shot on the rainy deck of s06 (the v1 lots deck: bulwark with painted shields, mast, torn striped sail, open
hatch, far coast, curling breaker beyond the starboard rail). The scene OPENS ON s06's CLOSING FRAME: same camera
(and roll phase), same sky / coast / sea phases, the crew on s06's final marks and poses (the captain, the
red-striped and the teal sailor bunched left of Jonah with their hands at their heads, the ginger sailor in front
with his arms spread toward Jonah, the blue-striped sailor 0 behind Jonah on the right), the crate with the lots
jar, the two plain lots dropped on the deck, Jonah bowed in his 'confess' pose holding the glowing marked lot, and
the last of the warm light on him. So the 1 s cross-dissolve changes nothing but the rain. The crew keep s06's
grouping for the whole scene (no line-up, nobody between the asker and Jonah).

Line 0 (N) '海浪越来越大，' the storm grows: big dark swells rise up beyond the rail, the breaker towers higher, the
        sky darkens under a heavy cloud bank (the far coast vanishes), the rain thickens, the horizon rocks harder
        and the camera pulls back; the crew stay scared (hands at their heads). '越来越凶。' lightning, a breaker
        bursts over the rail between the ginger sailor and Jonah and showers the deck, the camera jolts: everyone
        flinches (hard pose cuts sold by squash-and-hop), sailor 0 hops away from the rail. '水手们问约拿：' they turn
        to Jonah; the ginger sailor walks up to him (planted steps); Jonah lifts his head.
Line 1 (S) '我们该拿你怎么办，' the ginger sailor holds out both hands, palms up, pleading (open mouth: he is the
        one talking); '海才会平静下来呢？' he spreads his arms helplessly; Jonah lowers his eyes.
Line 2 (J) '你们把我抬起来，' Jonah, sorry but brave, lays his hand on his chest; '扔进海里吧，' he turns like a paper
        cut-out and points up over the rail at the towering sea — a breaker bursts right beyond his fingertip; the
        sailors gasp. '海就会平静下来。' he turns back to them with a gentle open hand (no smile).
Line 3 (J) '我知道，' hand on chest again ('sorry'); '这场大风浪，' he looks up at the storm (a far flash); '都是因为我。'
        he bows his head; the crew lower their heads, sad; the camera slowly pushes in. Then it rises over their
        bowed heads to the towering storm (dark cloud bank, the breaker's curl, the torn sail at the left) and
        eases to rest there: s08 dissolves in its wide shot of the ship in this storm, so the two crews never
        overlap (no double Jonah) and the cut reads as one move from the deck out to the sea.

Every key time comes from the narration: a phrase that starts a subtitle chunk starts with the chunk; one after a
punctuation mark inside a chunk starts at the end of the voice's pause at that mark (the voice pipeline widens
those pauses to 0.3 s+, see Cues). Pose changes are hard cuts (never crossfaded); every pose is held >= 0.5 s.
Stage 2112 x 2120 (the v1 lots stage; the camera stays on the deck world, y < 1190).
"""
import math
import random
import re

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

# ---- s06's closing marks (art/scenes/s06_lots.py at the end of its line 6) — keep in step with that file
CAPT = (1046, 1018, 1.02)          # the captain, 'worried' (hands on his head)
SV1 = (1157.6, 952, 0.90)          # variant 1 (red stripes, blue cap), behind the captain's shoulder
SV2 = (1246, 930, 0.86)            # variant 2 (teal stripes), behind the crate
SV3 = (1290, 1014, 1.0)            # variant 3 (ginger beard), in front: the one who asks ('dismay' in s06)
SV0 = (1834, 928, 0.86)            # variant 0 (blue stripes, red headband), behind Jonah on the right
JON = (1592, 1000, 1.0)            # Jonah, in front of the open hatch, facing the crew
X_C, Y_CRATE, CRATE_S = 1232, 992, 1.15                  # s06's crate with the lots jar (two sticks left)
CRATE_A = (X_C, Y_CRATE - 46 * CRATE_S)
JAR = (X_C + 9 * CRATE_S, CRATE_A[1] - 48 * CRATE_S)
DROPPED = [(1151.3, 1044, 0.85, 12), (1746, 950, 0.731, -13)]   # the plain lots dropped at the reveal
PHASE = dict(capt=0.65, sv1=0.8, sv2=0.55, sv3=0.4, sv0=0.2, jon=0.1)   # s06's breathing phases
OFF_DEFAULT = 44.833                # s06's local time at this scene's t = 0 (s06 duration - cross-dissolve)

# ---- this scene's new marks
SV3_ASK_X = 1336                   # the ginger sailor steps up to Jonah at '水手们问约拿' (plea ends ~65 px short)
SV0_HOP = (1928, 930, 0.86)        # sailor 0 hops away from the rail at the crash
POINT_X = 1792                     # the breaker that answers Jonah's pointing finger ('扔进海里')
# the breaker rears up during the closing rise (extra scale about a point on the sea line left of its foot): its curl
# ends over s08's sky right of the stern (output ~(1600, 500)), not over s08's stern crew, in the dissolve's middle
REAR_K, REAR_FOOT = 0.35, (950, 880)

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
    """Times of phrases in the narration.

    A phrase at the start of a subtitle chunk starts with the chunk. Inside a chunk, the voice pipeline widens the
    pause at every punctuation mark to >= 0.3 s (voice/tts.py stretch_pauses), so with k marks inside a chunk the
    k longest pauses (>= 120 ms) in it are those marks' pauses, in time order: a phrase after the n-th mark starts
    where the n-th of them ends. Short consonant dips are ignored; a natural breath pause without punctuation is
    shorter than the stretched ones. Only with too few pauses does a mark fall back to the nearest pause or the
    character-proportional estimate."""

    MIN_PAUSE = 0.12

    def __init__(self, ctx):
        self.ctx = ctx
        self.pauses = []
        for i, ln in enumerate(ctx.lines):
            for a, b in _dips(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"):
                self.pauses.append((ln.start + a, ln.start + b))

    def bounds(self, text, c0, c1):
        """[(time the phrase after each inner punctuation mark starts)] for a chunk."""
        body = text.rstrip(PUNCT + " ")
        marks = [k for k, ch in enumerate(body) if ch in PUNCT]
        if not marks:
            return []
        ests = [c0 + (c1 - c0) * _nchar(text[:k + 1]) / _nchar(text) for k in marks]
        cands = [(a, b) for a, b in self.pauses if c0 + 0.08 < a and b < c1 - 0.05 and b - a >= self.MIN_PAUSE]
        if len(cands) >= len(marks):
            best = sorted(sorted(cands, key=lambda p: p[1] - p[0], reverse=True)[:len(marks)])
            return [b for _, b in best]
        out, last = [], c0
        for e in ests:
            pick = None
            for a, b in cands:
                if a > last and abs(b - e) < 0.6 and (pick is None or abs(b - e) < abs(pick[1] - e)):
                    pick = (a, b)
            last = pick[1] if pick else max(e, last + 0.2)
            out.append(last)
        return out

    def at(self, phrases, default):
        for ph in ([phrases] if isinstance(phrases, str) else phrases):
            for ln in self.ctx.lines:
                spans = [(c.text, c.start, c.end) for c in ln.chunks] or [(ln.text, ln.start, ln.end)]
                for text, c0, c1 in spans:
                    k = text.find(ph)
                    if k < 0:
                        continue
                    n = sum(1 for ch in text[:k] if ch in PUNCT)
                    if n == 0:
                        if _nchar(text[:k]) <= 1 and not any(ch not in PUNCT for ch in text[:k]):
                            return c0
                        return c0 + (c1 - c0) * _nchar(text[:k]) / _nchar(text)
                    b = self.bounds(text, c0, c1)
                    base = b[n - 1]
                    j = max(i for i, ch in enumerate(text[:k]) if ch in PUNCT)
                    lead = _nchar(text[j + 1:k]) if text[j + 1:k].strip() else 0
                    if lead:       # the phrase starts some characters after the mark
                        nxt = b[n] if n < len(b) else c1
                        seg = text[j + 1:]
                        seg = seg[:min([i for i, ch in enumerate(seg) if ch in PUNCT] or [len(seg)])]
                        base += (nxt - base) * lead / _nchar(seg)
                    return base
        return default

    def end(self, phrases, default):
        """End of the voice inside the chunk holding the phrase (= start of the pause after it)."""
        for ph in ([phrases] if isinstance(phrases, str) else phrases):
            for ln in self.ctx.lines:
                for c in ln.chunks:
                    if ph in c.text:
                        return c.end
        return default


def prev_offset(ctx):
    """s06's local time at this scene's t = 0 (its last second plays under our first one in the dissolve)."""
    try:
        from engine.loader import load_timeline
        scs = load_timeline()["scenes"]
        i = [s["id"] for s in scs].index(ctx.id)
        off = ctx.start - scs[i - 1]["start"]
        return off if 5 < off < 400 else OFF_DEFAULT
    except Exception:
        return OFF_DEFAULT


def xfade_len():
    """The cross-dissolve length (build/timeline.json 'xfade')."""
    try:
        from engine.loader import load_timeline
        return float(load_timeline().get("xfade", 1.0))
    except Exception:
        return 1.0


# ============================================================== painting

def s06_sky_dx(tau):
    """s06's drifting sky (art/scenes/s06_lots.py sky_clouds_layer motion) at its local time tau."""
    return 22 + 22 * math.sin(2 * math.pi * tau / 40 - 1.2)


def sky_markup(dark, dx0):
    """V5's storm sky (dark=False) or the same sky under a heavy storm cover (dark=True: a slate wash and a bank
    of dark storm clouds over the warm cloud break). The V5 part is shifted by dx0, where s06's drifting sky is
    when this scene starts. The far sea is its own (rocking) layer."""
    sfx = "d" if dark else "l"
    defs = (S.lin_grad(f"dsky{sfx}", [(0, "#36415a"), (0.42, "#4f5d77"), (0.77, "#7f8da2"), (1, "#9eaab8")]) +
            S.rad_grad(f"dbreak{sfx}", [(0, "#f6e2b4", 0.75), (0.5, "#e7cf9c", 0.3), (1, "#d9cdb4", 0)]) +
            S.lin_grad(f"curtain{sfx}", [(0, "#c9d3dc", 0.0), (0.3, "#c9d3dc", 0.22), (1, "#c9d3dc", 0.0)]))
    body = f'<rect x="-60" y="-20" width="{W + 120}" height="800" fill="url(#dsky{sfx})"/>'
    v5 = f'<ellipse cx="1650" cy="300" rx="430" ry="170" fill="url(#dbreak{sfx})"/>'
    soft = ""
    for (cx, cy, rx, ry, col) in [(250, 170, 520, 150, "#323c52"), (900, 110, 640, 150, "#36415a"),
                                  (2000, 150, 420, 140, "#323c52"), (620, 300, 360, 80, "#465370")]:
        soft += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}"/>'
    v5 += S.g(soft, filter="blur-md")
    for (x0, x1) in [(180, 420), (860, 1080)]:
        v5 += S.g(f'<path d="M{x0},300 L{x1},300 L{x1 - 90},600 L{x0 - 90},600 Z" fill="url(#curtain{sfx})"/>',
                  filter="soft")
    bank = ""
    for i, (cx, cy, w, h, col) in enumerate([(120, 250, 560, 150, "#59667f"), (760, 210, 600, 140, "#55627b"),
                                              (1240, 200, 420, 120, "#5c6982"), (2080, 205, 520, 150, "#55627b")]):
        bank += S.cloud(cx, cy, w, h, col, seed=10 + i, sw=2.5)
    v5 += S.g(bank, filter="wobble")
    body += f'<g transform="translate({dx0:.1f},0)">{v5}</g>'
    if dark:
        defs += S.lin_grad("s7gl", [(0, "#1d2536", 0.8), (0.55, "#27324a", 0.5), (1, "#3a4760", 0.12)])
        body += f'<rect x="-30" y="-30" width="{W + 60}" height="{RAIL_TOP + 40}" fill="url(#s7gl)"/>'
        heavy = ""
        for i, (cx, cy, w, h) in enumerate([(1560, 150, 760, 250), (2090, 210, 560, 220), (1020, 70, 660, 200),
                                             (420, 120, 720, 230), (-60, 200, 420, 200)]):
            heavy += V4.storm_cloud(cx, cy, w, h, seed=70 + i, fill="#3c4860", under="#262f42", rim="#8390a6", sw=4)
        body += S.g(heavy, filter="wobble")
    return body, defs


def sky_layer(dark, dx0):
    body, defs = sky_markup(dark, dx0)
    return doc(body, defs)


def coast_layer():
    """s06's faint far coast on the horizon between the sail and the big wave (it vanishes as the storm grows)."""
    d = S.hill(960, 1500, 606, 96, seed=4, bottom=650, bumps=3)
    d2 = S.hill(1120, 1430, 606, 62, seed=9, bottom=650, bumps=2)
    body = S.path(d, fill="#93a09a", sw=3, extra='opacity="0.95"')
    body += S.path(d2, fill="#7f9288", sw=2.5)
    for x, y in ((1060, 560), (1300, 548), (1380, 572)):
        body += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="13" fill="#6f8478" stroke="{S.INK}" stroke-width="2"/>'
    return doc(S.g(body, filter="wobble"))


def surge_cap(f, xc, wl, amp, seed, size=1.0, sw=3.0):
    """V4.foam_cap without its curled bead lip and spray dots, and without puffs running down the slopes (behind the
    rail those chains of white balls read as thought bubbles over the sailors' heads): a compact bubbly crown on the
    crest with lace below."""
    r = random.Random(seed)
    half = 0.1 * wl * size
    rb = (9 + 0.2 * amp) * size
    circ = []
    n = max(5, int(2 * half / (rb * 0.7)))
    for i in range(n):
        u = -1 + 2 * i / (n - 1)
        x = xc + u * half
        rad = rb * (0.62 + 0.38 * (1 - abs(u)) ** 0.7) * r.uniform(0.88, 1.1)
        # a compact crown sitting ON the crest (only loosely following the slopes, so it never trails down them)
        circ.append((x, f(xc) + 0.3 * (f(x) - f(xc)) + 0.45 * rad, rad))
    out = V4.puffs(circ, P["foam"], sw, shade=(P["sea_pale"], (xc, f(xc) + rb * 1.3, half * 1.1, rb * 0.8), 0.8),
                   cid=f"s7fc{seed}")
    lace = ""
    for k, off in enumerate((0.55, 1.05)):
        xa, xb = xc - half * (1.3 + 0.4 * k), xc + half * (1.1 + 0.3 * k)
        pts = [(x, f(x) + amp * off + 10 + 6 * math.sin(x * 0.05 + seed)) for x in np.linspace(xa, xb, 9)]
        lace += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["foam"]}" '
                 f'stroke-width="{4.5 * size:.1f}" stroke-dasharray="{30 * size:.0f} {16 * size:.0f}" '
                 f'stroke-linecap="round" opacity="{0.55 - 0.15 * k}"/>')
    return lace + out


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
        caps += surge_cap(f, xc, 620, 84, 300 + i, 1.15)
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
    """The deck of s06 (V5.deck_layer without the rig and the cut-away): bulwark with shields, deck planks,
    puddles and the open hatch."""
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
    for (x, y, rx, ry) in [(660, 1062, 130, 16), (1180, 1112, 160, 18), (1600, 1150, 120, 14), (420, 1150, 90, 12)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9fb3bd" opacity="0.45"/>'
        b += f'<path d="M{x - rx * 0.5},{y - 3} l{rx * 0.5},0" stroke="#e8eef0" stroke-width="3" opacity="0.6"/>'
    hm, hdefs = V5.hatch_markup()
    b += hm
    return doc(S.g(b, filter="wobble"), defs + hdefs)


def lot_svg(x, y, s, rot, marked=False):
    """A lot stick; the marked one keeps its gold mark but loses the built-in halo (the glow is its own layer)."""
    m = PR.lot(x, y, s, rot=rot, marked=marked)
    if marked:
        m = re.sub(r'<ellipse cx="0" cy="0" rx="78" ry="56"[^>]*/>', "", m)
    return m


def stick_in(pts, hand=1, s=1.0, marked=True, out=26):
    """A lot held in a fist, sticking out of it along the shoulder -> hand direction (as in s06)."""
    hx, hy = pts["hands"][hand]
    sx_, sy_ = pts["shoulders"][hand]
    d = math.atan2(hy - sy_, hx - sx_)
    cx, cy = hx + out * s * math.cos(d), hy + out * s * math.sin(d)
    return lot_svg(cx, cy, s, math.degrees(d), marked), (cx, cy)


# ============================================================== people

_P = C._P
POSE = {
    "stand": C.POSES["stand"],
    "scared": C.POSES["scared"],
    "worried": C.POSES["worried"],
    "walk_a": C.POSES["walk_a"],
    "walk_b": C.POSES["walk_b"],
    "sad": C.POSES["sad"],
    "confess": C.POSES["confess"],
    # s06's crew poses
    "dismay": _P(t=-4, h=-4, arms=(("fk", 62, 112), ("fk", -58, -10)), hands=("open", "open"), expr="scared"),
    "chin": _P(t=8, h=4, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
               expr="worried"),
    "palm": _P(t=4, h=-2, arms=(("fk", 72, 96), ("fk", -8, -3)), hands=("open", "fist"), expr="worried"),
    "nod": _P(h=18, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="worried"),
    # the ginger sailor's plea: both hands held out at chest height, palms up, leaning in toward Jonah
    "ask": _P(t=9, h=-6, legs=((6, 2), (-5, -2)), arms=(("fk", 66, 104), ("fk", 52, 98)), hands=("open", "open"),
              expr="call"),
    # ...and the helpless shrug
    "shrug": _P(t=-2, h=-8, legs=((6, 2), (-5, -2)), arms=(("fk", 42, 118), ("fk", -38, -112)),
                hands=("open", "open"), expr="worried"),
    # Jonah (the marked lot always in his near hand)
    "j_stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "j_down": _P(h=14, arms=(("fk", 14, 8), ("fk", -8, -3))),
    "j_chest": _P(t=2, h=-2, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open")),
    "j_chest_up": _P(t=0, h=-14, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
                     look=(0.02, -0.08)),
    # '扔进海里吧' — pointing up and back over the rail at the towering sea (hand above the shoulder)
    "j_point": _P(t=-5, h=-12, legs=((8, 3), (-7, -3)), arms=(("fk", 126, 136), ("fk", -16, -6)),
                  hands=("point", "fist"), look=(0.03, -0.07)),
    # '海就会平静下来' — a gentle open hand toward the crew
    "j_calm": _P(t=2, h=4, arms=(("fk", 56, 86), ("fk", -8, -3)), hands=("open", "fist")),
}


def figure(who, x, y, s, facing, pose, expr=None, variant=0):
    """(markup, points) of a person in a POSE entry. points: hands [far, near], shoulders, head (stage px)."""
    ps = dict(POSE[pose])
    if who == "jonah":
        D, m = C._jonah_design(), C._ADULT
    elif who == "captain":
        D, m = C._captain_design(), C._CAPTAIN_M
    else:
        D, m = C._sailor_design(variant), C._SAILOR_M
    inner, _ = C._figure(D, m, ps, expr or ps["expr"], C._fsign(facing))
    L = dict(C._LAST)
    sx = s * (1 if facing >= 0 else -1)

    def st(p):
        return (x + p[0] * sx, y + p[1] * s)
    pts = {"hands": [st(p) for p in L["hands"]], "shoulders": [st(p) for p in L["shoulders"]],
           "head": st(L["head"])}
    return C._wrap_out(inner, x, y, s, facing, f"s7{who}{variant}-{pose}"), pts


def apply_tf(tf, p, pivot):
    """Where stage point p goes under a layer transform tf (pivot = the layer's default pivot)."""
    px = tf.px if tf.px is not None else pivot[0]
    py = tf.py if tf.py is not None else pivot[1]
    x, y = (p[0] - px) * tf.sx, (p[1] - py) * tf.sy
    a = math.radians(tf.rot)
    return (px + tf.dx + x * math.cos(a) - y * math.sin(a), py + tf.dy + x * math.sin(a) + y * math.cos(a))


class Track:
    """One person on their own flipbook layer(s) (s06's Track, with s06's breathing phase continued).

    moves: (t0, t1, (x, y, s) from, (x, y, s) to, 'hop' | 'walk'); keys: (t, markup, home, pop, points, facing).
    Every key is drawn at the person's home at its time; pose switches are hard cuts sold by a squash-and-hop."""

    def __init__(self, name, who, start, z, variant=0, phase=0.0, amp=0.011, off=0.0):
        self.name, self.who, self.start, self.z = name, who, start, z
        self.variant, self.phase, self.amp, self.off = variant, phase, amp, off
        self.moves, self.keys, self.turns = [], [], []
        self.jiggle = None

    def move(self, t0, t1, to, kind="hop"):
        frm = self.rest(t0)
        to = (to[0], to[1], to[2] if len(to) > 2 else frm[2])
        self.moves.append((t0, t1, frm, to, kind))
        self.moves.sort(key=lambda m: m[0])

    def rest(self, t):
        p = self.start
        for (t0, t1, a, b, k) in self.moves:
            if t0 <= t:
                p = b
        return p

    def pos(self, t):
        for (t0, t1, a, b, k) in self.moves:
            if t0 <= t < t1:
                u = (t - t0) / (t1 - t0) if k == "walk" else M.progress(t, t0, t1, "sine")
                return tuple(M.lerp(a[i], b[i], u) for i in range(3))
        return self.rest(t)

    def key(self, t, pose, facing, expr=None, props=None, pop=True):
        x, y, s = self.rest(t + 1e-6)
        mk, pts = figure(self.who, x, y, s, facing, pose, expr, self.variant)
        sh = C.ground_shadow(x, y + 2, s, width=136 if self.who == "captain" else 120)
        extra = "".join(fn(pts, s, facing) for fn in (props or []))
        self.keys.append((t, sh + mk + extra, (x, y, s), pop, pts, facing))
        self.keys.sort(key=lambda k: k[0])
        return pts

    def walk(self, t0, t1, to, facing, expr=None, props=None, step=0.15, pose_after="stand"):
        """Planted walk: alternate walk_a / walk_b every ``step`` s while moving to ``to``."""
        self.move(t0, t1, to, "walk")
        n = max(2, round((t1 - t0) / step))
        for i in range(n):
            self.key(t0 + i * (t1 - t0) / n, "walk_a" if i % 2 == 0 else "walk_b", facing, expr, props, pop=False)
        if pose_after:
            self.key(t1, pose_after, facing, expr, props, pop=True)

    def idx(self, t):
        i = 0
        for j, k in enumerate(self.keys):
            if t >= k[0]:
                i = j
        return i

    def motion(self):
        switches = [k[0] for k in self.keys[1:] if k[3]]

        def m(t):
            i = self.idx(t)
            hx, hy, hs = self.keys[i][2]
            x, y, s = self.pos(t)
            k = s / hs
            dy = y - hy
            for (t0, t1, a, b, kind) in self.moves:
                if t0 <= t < t1:
                    if kind == "hop":
                        dist = math.hypot(b[0] - a[0], b[1] - a[1])
                        dy -= min(26.0, 6 + 0.12 * dist) * math.sin(math.pi * (t - t0) / (t1 - t0))
                    else:
                        dy -= 5 * abs(math.sin(math.pi * (t - t0) / 0.15))
            sy = 1 + self.amp * math.sin(2 * math.pi * ((t + self.off) / 3.1 + self.phase))
            sx = 1.0
            for ts in switches:
                u = (t - ts) / 0.24
                if 0 <= u <= 1:
                    bmp = math.sin(math.pi * u) * (1 - u)
                    sy *= 1 - 0.08 * bmp
                    sx *= 1 + 0.045 * bmp
                    dy -= 7 * math.sin(math.pi * min(1.0, u * 1.6)) * (u < 0.62)
            rot = 0.0
            if self.jiggle:
                jd = self.jiggle(t)
                dy += jd[0]
                rot += jd[1]
            for ts in self.turns:      # paper cut-out turn around a facing flip
                v = abs(t - ts) / 0.09
                if v < 1:
                    sx *= 1 - 0.7 * (1 - v)
            return Tf(x - hx, dy, rot, sx * k, sy * k, 1.0, hx, hy)
        return m

    def add_to(self, sc, seed=None):
        """One layer per stretch of keys drawn near the same spot, shown only while its keys are current."""
        segs, cur = [], []
        for k in self.keys:
            if cur and abs(k[2][0] - cur[0][2][0]) + abs(k[2][1] - cur[0][2][1]) > 70:
                segs.append(cur)
                cur = []
            cur.append(k)
        segs.append(cur)
        mot = self.motion()
        for si, seg in enumerate(segs):
            uniq, idx_of = [], []
            for k in seg:
                if k[1] not in uniq:
                    uniq.append(k[1])
                idx_of.append(uniq.index(k[1]))
            times = [k[0] for k in seg]
            t_on = times[0] if si > 0 else -1e9
            t_off = segs[si + 1][0][0] if si + 1 < len(segs) else 1e9

            def at(t, times=times, idx_of=idx_of):
                i = 0
                for j, tk in enumerate(times):
                    if t >= tk:
                        i = j
                return float(idx_of[i])

            def m(t, t_on=t_on, t_off=t_off):
                return mot(t) if t_on <= t < t_off else Tf(alpha=0.0)
            svgs = [doc(b) for b in uniq]
            sc.add(f"{self.name}_{si}", svgs if len(svgs) > 1 else svgs[0], z=self.z + 0.001 * si, motion=m,
                   frame_at=at if len(svgs) > 1 else None, seed=seed)


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
    OFF = prev_offset(ctx)            # s06's clock: tau = t + OFF continues every s06 motion through the dissolve
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
    p3b = cue.at(["这场大风浪", "你们遇到这场大风浪", "大风浪"], line_frac(3, 0.2))   # looks up at the storm
    p3c = cue.at(["都是因为我"], line_frac(3, 0.55))                           # bows his head
    # keep the order sane if a voice take changes a lot
    p0b = max(p0b, p0 + 1.0)
    p0c = max(p0c, p0b + 0.9)
    p3 = max(p3, p2c + 1.2)
    p3b = max(p3b, p3 + 0.55)
    p3c = max(p3c, p3b + 0.6)
    t_crash = p0b + 0.02
    t_strike = p0b - 0.03
    t_far_strike = p3b + 0.08
    t_point_splash = p2b + 0.17              # the breaker answers right on '海里'
    # the closing rise over the bowed heads to the storm (camera below) ends by the middle of the dissolve into s08,
    # so from there on only sky and breaker show under s08's crew (a rise still running at the midpoint left the
    # tops of our crew's heads along the bottom of the frame). 1.75 s keeps its peak speed at ~550 px/s.
    t_rise1 = T - xfade_len() / 2 - 0.05
    t_rise0 = t_rise1 - 1.75
    rear = lambda t: M.progress(t, t_rise0, t_rise1, "sine")      # noqa: E731  (the breaker rears up meanwhile)

    # storm growth 0..1: s06's sea at the start, rising through '海浪越来越大', full at '越来越凶'
    grow = V4.keyc([(p0, 0.0), (p0b, 0.62), (p0b + 0.9, 1.0)], ["inout", "out"])
    calm = lambda t: 1 - grow(t)            # noqa: E731  (what is left of s06's light)

    def sea_rot(t):                          # s06's horizon rock (V5.sea_rot), growing with the storm
        return (1.45 + 1.25 * grow(t)) * math.sin(2 * math.pi * (t + OFF) / 5.4 + 0.6)

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

    # ---------------------------------------------------------------- outboard world
    dx0 = s06_sky_dx(OFF)
    # s06's sky (with its cloud bank along the top of the frame) keeps drifting under the cross-dissolve: follow it
    # exactly while s06 is still showing, then settle back to the painted position during the pull-back (so the
    # rest of the scene is unchanged). Without this the cloud-bank outline over the breaker doubles by 2-4 px.
    xf = xfade_len()

    def sky_drift(t):
        return (s06_sky_dx(t + OFF) - dx0) * (1 - M.progress(t, xf, xf + 2.4, "sine"))
    sc.add("sky", sky_layer(True, dx0), z=0, wc=0.7, motion=lambda t: Tf(dx=sky_drift(t)))
    sc.add("sky_light", sky_layer(False, dx0), z=0.2, wc=0.7, motion=lambda t: Tf(dx=sky_drift(t), alpha=calm(t)))
    # lightning: one bold bolt at '越来越凶', a smaller far one at '这场大风浪'
    sc.add("bolt0", doc(V4.bolt_svg(1170, 130, 600, seed=17, sway=1, w0=34), V4.BOLT_DEFS), z=0.3, wc=0,
           motion=lambda t: Tf(alpha=V4.bolt_alpha(t - t_strike)))
    sc.add("bolt1", doc(V4.bolt_svg(1460, 210, 590, seed=23, sway=-1, w0=22), V4.BOLT_DEFS), z=0.35, wc=0,
           motion=lambda t: Tf(alpha=0.85 * V4.bolt_alpha(t - t_far_strike)))
    sc.add("coast", coast_layer(), z=0.4, wc=0.8, motion=tilted(lambda t: Tf(alpha=calm(t))))
    sc.add("sea_far", V5.sea_far_layer(), z=0.5, wc=0.9, motion=tilted())
    # the golden cloud-break of s06 fades as the storm cover closes in
    bdefs = S.rad_grad("brk", [(0, "#ffd77e", 0.85), (0.45, "#ffbf55", 0.42), (1, "#ffbf55", 0)])
    rays = "".join(S.rays(1650, 290, 60, 470, n=26, width_deg=5, rot=8).split(" Z ")[i] + " Z "
                   for i in range(26) if 1 <= i <= 12)
    brk = (S.g('<ellipse cx="1650" cy="300" rx="400" ry="180" fill="url(#brk)"/>', filter="soft") +
           S.g(S.path(rays, fill="#ffd27a", stroke=False, extra='opacity="0.4"'), filter="blur-md") +
           S.g('<ellipse cx="1650" cy="318" rx="250" ry="70" fill="#ffe2a0" opacity="0.5"/>', filter="blur-md"))
    sc.add("break_glow", doc(brk, bdefs), z=0.6, wc=0, motion=lambda t: Tf(
        alpha=0.22 * calm(t) * (0.92 + 0.08 * math.sin(2 * math.pi * (t + OFF) / 2.3))))
    sc.add("clouds", V5.clouds_layer(), z=1, wc=0.8,
           motion=lambda t: Tf(dx=s06_sky_dx(t + OFF) + 22 * max(0.0, t - p0)))

    # the swells rise up from behind the rail one after another and keep heaving
    # (crests at x 1270 + 618 k in the painting: shifted so that, once risen, they ride between the heads — over
    # the mast, in the gap between the ginger sailor and Jonah, and right of sailor 0; risen 45 px less than the
    # full swell so the foam crowns stay above the heads)
    def surge_m(t):
        g = grow(t)
        up = 300 * (1 - g) + 45 * g
        heave = (14 + 30 * g) * math.sin(2 * math.pi * t / 3.6 + 0.4)
        return Tf(dx=200 + 28 * math.sin(2 * math.pi * t / 7.2) - 20 * g, dy=up + heave)
    sc.add("surge", surge_layer(), z=2, motion=tilted(surge_m), wc=0.9)

    lift_pt = lambda t: 50 * math.sin(math.pi * M.progress(t, p2b - 0.1, p2b + 1.6, "linear"))   # noqa: E731

    def bigwave_m(t):                # s06's bob continued (tau), then the breaker towers higher
        g, tau, u = grow(t), t + OFF, rear(t)
        k = 1 + REAR_K * u           # ...and rears up while the camera rises to it (its heave settles)
        dx = 18 * math.sin(2 * math.pi * tau / 6.8) - 30 * g
        dy = -70 * g + (26 + 6 * g) * math.sin(2 * math.pi * (tau / 3.4 + 0.1)) * (1 - u) - lift_pt(t)
        s = (1 + 0.12 * g) * k
        return Tf(dx=dx * k + (REAR_FOOT[0] - 1760) * (1 - k), dy=dy * k + (REAR_FOOT[1] - 880) * (1 - k),
                  sx=s, sy=s, px=1760, py=880)
    sc.add("big_wave", V5.big_wave_layer(), z=3, motion=tilted(bigwave_m))
    sc.add("sea_mid", V5.sea_mid_layer(), z=4, motion=tilted(
        lambda t: Tf(dx=(46 + 20 * grow(t)) * math.sin(2 * math.pi * (t + OFF) / 6.0),
                     dy=(20 + 16 * grow(t)) * math.sin(2 * math.pi * ((t + OFF) / 3.4 + 0.35)))))

    # spray bursts over the rail (behind the bulwark): ambient ones left of the mast (clear of faces), the crash
    # at '越来越凶' between the ginger sailor and Jonah, and the one right beyond Jonah's fingertip ('扔进海里')
    splashes = [(p0 + 0.75, 730, 0.8, 3, "small"), (t_crash, 1450, 1.4, 7, "big"),
                (t_crash + 0.12, 660, 1.0, 5, None), (p1b + 0.75, 700, 0.75, 9, "small"),
                (t_point_splash, POINT_X, 1.25, 11, "big"), (p2c + 1.05, 690, 0.8, 15, "small"),
                (min(p3b + 0.3, T - 2.6), 740, 0.7, 13, "small")]

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
        pan = max(-0.8, min(0.8, (sx_ - 1300) / 900))
        if snd == "big":
            sc.sfx("splash", ts, gain_db=-9, pan=pan)
        elif snd == "small":
            sc.sfx("splash_small", ts, gain_db=-15, pan=pan)

    # ---------------------------------------------------------------- ship (s06's deck)
    sc.add("deck", deck_layer(), z=10)
    hg_defs = S.rad_grad("hg", [(0, "#ffcf86", 0.75), (0.5, "#f6a956", 0.28), (1, "#f2a95a", 0)])
    sc.add("hatch_glow", doc(f'<ellipse cx="{V5.HX}" cy="{V5.HATCH_F[2] - 30}" rx="190" ry="120" fill="url(#hg)"/>',
                             hg_defs), z=10.2, blend="add", wc=0,
           motion=lambda t: Tf(alpha=0.85 + 0.15 * math.sin(2 * math.pi * (t + OFF) / 1.7)))
    sc.add("rig", rig_layer(), z=10.5)

    def sail_m(t):                   # the torn sail billows and shivers in the gusts (stronger as the storm grows)
        g = grow(t)
        k = M.progress(t, 0.6, 1.4, "sine")          # still under the dissolve (s06's sail is a still painting)
        gust = math.sin(2 * math.pi * t / 1.3) + 0.5 * math.sin(2 * math.pi * t / 0.57 + 1.0)
        return Tf(rot=(0.15 * k + 0.55 * g) * gust,
                  sy=1 + (0.004 * k + 0.014 * g) * math.sin(2 * math.pi * t / 1.9), px=MX, py=SAIL_YARD)
    sc.add("sail", sail_layer(), z=10.6, motion=sail_m)
    sc.add("deck_props", V5.deck_props_layer(), z=11)
    mlx, mly = MX + 47, 610
    sc.add("deck_lantern", doc(PR.lantern(mlx, mly, 0.8)), z=11.5,
           motion=lambda t: Tf(rot=(9 + 6 * grow(t)) * math.sin(2 * math.pi * (t + OFF) / 2.9), px=mlx, py=mly))

    # the last of s06's warm light on Jonah's spot (fades as the storm cover closes in)
    jx, jy, js = JON
    wdefs = (S.lin_grad("beamw", [(0, "#ffbf55", 0.5), (0.35, "#ffcb6a", 0.32), (0.8, "#ffd98a", 0.12),
                                   (1, "#ffd98a", 0.0)]) +
             S.lin_grad("beamh", [(0, "#fff0c0", 0.0), (0.25, "#ffe7a8", 0.3), (0.85, "#ffe29a", 0.1),
                                  (1, "#ffe39a", 0.0)]) +
             S.rad_grad("jg", [(0, "#ffe2a0", 0.55), (0.45, "#ffd27a", 0.25), (1, "#ffd27a", 0)]) +
             S.rad_grad("pool", [(0, "#ffc85e", 0.5), (1, "#ffc85e", 0)]) +
             S.rad_grad("lotg", [(0, "#fff2c4", 0.95), (0.35, "#ffd27a", 0.6), (1, "#ffbf55", 0)]))
    sc.add("beam_wash", doc(S.g(f'<path d="M1500,250 L1800,250 L{jx + 230},1010 L{jx - 240},1010 Z" '
                                f'fill="url(#beamw)"/>', filter="blur-md") +
                            S.g(f'<path d="M1580,260 L1720,260 L{jx + 110},990 L{jx - 120},990 Z" '
                                f'fill="url(#beamh)"/>', filter="blur-md") +
                            f'<ellipse cx="{jx}" cy="{jy + 4}" rx="230" ry="46" fill="url(#pool)"/>', wdefs),
           z=19, wc=0, motion=lambda t: Tf(alpha=0.22 * calm(t)))

    # ---------------------------------------------------------------- s06's props: the lots crate, dropped lots
    for i, (x, y, s, r) in enumerate(DROPPED):
        sc.add(f"dropped{i}", doc(lot_svg(x, y, s, r)), z=19.5 + 0.01 * i)
    sc.add("crate", doc(C.ground_shadow(X_C + 8, Y_CRATE - 2, 1.0, width=170, opacity=0.2) +
                        PR.crate(CRATE_A[0], CRATE_A[1], CRATE_S)), z=21)
    sc.add("jar", doc(PR.lots_jar(JAR[0], JAR[1], 1.0, sticks=2)), z=21.2)

    # ---------------------------------------------------------------- people (s06's final marks and poses first)
    CP = Track("captain", "captain", CAPT, z=22, phase=PHASE["capt"], off=OFF)
    S1 = Track("s1", "sailor", SV1, z=20.5, variant=1, phase=PHASE["sv1"], off=OFF)
    S2 = Track("s2", "sailor", SV2, z=20, variant=2, phase=PHASE["sv2"], off=OFF)
    S3 = Track("s3", "sailor", SV3, z=24, variant=3, phase=PHASE["sv3"], off=OFF)
    S0 = Track("s0", "sailor", SV0, z=23, variant=0, phase=PHASE["sv0"], off=OFF)
    JN = Track("jonah", "jonah", JON, z=25, phase=PHASE["jon"], amp=0.009, off=OFF)
    lot = lambda pts, s, f: stick_in(pts, 1, s, True, 26)[0]      # noqa: E731  (the marked lot, near hand)

    def jolt(k):
        return lambda t: (-k * 6 * bump(t, t_crash, 0.1), 0.0)
    for tr, k in ((CP, 1.0), (S1, 1.0), (S2, 1.0), (S3, 1.0), (S0, 1.0), (JN, 0.6)):
        tr.jiggle = jolt(k)

    # ---- line 0: s06's closing poses; they stay scared while the sea rises; the crash makes everyone flinch
    CP.key(0, "worried", 1, "scared")
    S1.key(0, "scared", 1, "scared")
    S2.key(0, "scared", 1, "scared")
    S3.key(0, "dismay", 1, "scared")
    S0.key(0, "scared", -1, "scared")
    JN.key(0, "confess", -1, "sorry", props=[lot])
    CP.key(t_crash + 0.12, "worried", 1, "scared")              # clutches his cap harder (pop)
    S1.key(t_crash + 0.14, "scared", 1, "scared")
    S2.key(t_crash + 0.1, "scared", 1, "scared")
    S3.key(t_crash + 0.06, "scared", 1, "scared")               # arms in from 'dismay': hands to his face
    S0.move(t_crash + 0.08, t_crash + 0.4, SV0_HOP)             # hops away from the rail
    S0.key(t_crash + 0.08, "scared", -1, "scared")
    # '水手们问约拿：' — they turn to Jonah; the ginger sailor walks up to him (planted steps); Jonah lifts his head
    t_w0 = p0c + 0.1
    t_w1 = t_w0 + 0.32
    S3.walk(t_w0, t_w1, (SV3_ASK_X, SV3[1], SV3[2]), 1, "worried", step=0.16)
    S2.key(p0c + 0.22, "stand", 1, "worried")
    S1.key(p0c + 0.34, "chin", 1, "worried")
    CP.key(p0c + 0.46, "palm", 1, "worried")
    S0.key(p0c + 0.28, "stand", -1, "worried")
    t_jup = p0c + 0.62
    JN.key(t_jup, "j_stand", -1, "worried", props=[lot])

    # ---- line 1: '我们该拿你怎么办，' the plea (he is the one talking); '海才会平静下来呢？' the shrug
    S3.key(p1 - 0.05, "ask", 1, "call")
    CP.key(p1 + 0.2, "stand", 1, "worried")
    S3.key(p1b - 0.04, "shrug", 1, "worried")
    for tr, dt, f in ((CP, 0.12, 1), (S1, 0.3, 1), (S2, 0.2, 1), (S0, 0.42, -1)):   # nods with the question
        base_pose = "chin" if tr is S1 else "stand"
        tr.key(p1b + dt, "nod", f, "worried", pop=False)
        tr.key(p1b + dt + 0.36, base_pose, f, "worried", pop=False)
    JN.key(p1b + 0.35, "j_down", -1, "sad", props=[lot])          # lowers his eyes
    S3.key(p1e + 0.3, "stand", 1, "worried")

    # ---- line 2: hand on chest; turn and point at the sea (a breaker answers, they gasp); back with an open hand
    JN.key(p2 - 0.05, "j_chest", -1, "worried", props=[lot])
    JN.key(p2b, "j_point", 1, "call", props=[lot])
    JN.turns.append(p2b)
    for tr, dt, pose, f in ((S3, 0.12, "stand", 1), (S2, 0.2, "scared", 1), (S0, 0.24, "scared", -1),
                            (CP, 0.28, "worried", 1), (S1, 0.34, "scared", 1)):
        tr.key(t_point_splash + dt, pose, f, "surprised" if tr is not CP else "scared")
    JN.key(p2c, "j_calm", -1, "worried", props=[lot])
    JN.turns.append(p2c)
    for tr, dt, pose, f in ((S3, 0.35, "stand", 1), (S2, 0.3, "stand", 1), (S0, 0.45, "stand", -1),
                            (CP, 0.5, "stand", 1), (S1, 0.55, "chin", 1)):
        tr.key(p2c + dt, pose, f, "worried")

    # ---- line 3: '我知道，' chest; '这场大风浪，' looks up at the storm; '都是因为我。' bows his head; they grieve
    JN.key(p3 - 0.05, "j_chest", -1, "sorry", props=[lot])
    JN.key(p3b - 0.02, "j_chest_up", -1, "worried", props=[lot])
    JN.key(p3c - 0.04, "confess", -1, "sorry", props=[lot])
    for tr, dt, pose, f in ((S3, 0.25, "sad", 1), (CP, 0.12, "nod", 1), (S1, 0.4, "nod", 1), (S2, 0.3, "nod", 1),
                            (S0, 0.5, "stand", -1)):
        tr.key(p3c + dt, pose, f, "sad")

    for tr, seed in ((S2, 201), (S1, 202), (CP, 203), (S0, 204), (S3, 205), (JN, 206)):
        tr.add_to(sc, seed)

    # the lot's warm glow (s06's: follows the lot through Jonah's poses and turns)
    jm = JN.motion()
    LG0 = (400, 400)

    def lot_pos(t):
        k = JN.keys[JN.idx(t)]
        _, c = stick_in(k[4], 1, 1.0, True, 26)
        return apply_tf(jm(t), c, (k[2][0], k[2][1]))
    lot_env = V4.keyc([(0, 0.45), (p2b, 0.4), (T, 0.32)], "sine")

    def lot_glow_m(t):
        p = lot_pos(t)
        a = lot_env(t) * (0.85 + 0.15 * math.sin(2 * math.pi * (t + OFF) / 1.1))
        return Tf(dx=p[0] - LG0[0], dy=p[1] - LG0[1], alpha=a, px=LG0[0], py=LG0[1])
    sc.add("lot_glow", doc(f'<ellipse cx="{LG0[0]}" cy="{LG0[1]}" rx="120" ry="100" fill="url(#lotg)"/>', wdefs),
           z=25.3, wc=0, blend="add", motion=lot_glow_m)
    sc.add("jonah_glow", doc(f'<ellipse cx="{jx}" cy="{jy - 200}" rx="210" ry="270" fill="url(#jg)"/>', wdefs),
           z=24.9, wc=0, blend="add", motion=lambda t: Tf(
               alpha=0.22 * calm(t) * (0.8 + 0.2 * math.sin(2 * math.pi * (t + OFF) / 1.3))))

    sc.add("deck_fg", V5.deck_foreground(), z=30)

    # ---------------------------------------------------------------- camera
    A = Cam(1372, 664, 1450)       # s06's closing framing
    B = Cam(1250, 640, 1690)       # pulled back and up: the waves tower behind the rail
    Cc = Cam(1330, 690, 1460)      # the question
    D = Cam(1334, 688, 1480)       # Jonah answers
    E = Cam(1312, 680, 1560)       # ...includes the breaker beyond his finger
    F = Cam(1352, 700, 1460)
    G = Cam(1440, 716, 1300)       # slow push-in on Jonah and the crew at the end
    keys = [(0.0, A), (p0, A), (p0b + 0.9, B), (p0c + 0.5, B), (p1 + 0.6, Cc), (p2 - 0.3, D),
            (p2b - 0.25, D), (p2b + 0.3, E), (p2c + 0.8, E), (p3 + 0.2, F), (T, G)]
    push = M.cam_keys(keys, "sine")
    # ...then, as the crew bow their heads, the camera rises over them to the towering storm (t_rise0..t_rise1,
    # done by the dissolve's midpoint; the breaker rears up meanwhile, see bigwave_m). s08 opens
    # on a wide shot of the whole ship in that storm (its crew in a different order, about 0.8x the size), so a
    # dissolve from the deck group would pile two crews and two Jonahs on top of each other; this way our crew
    # slide out at the bottom of the frame while s08's fade in at mid-height. R shows no heads at all (its bottom
    # edge, y + w * 9/32, stays above the tallest cap) and sits at the clamp's top edge (y = w * 9/32 + 6).
    R = Cam(1520, 324, 1130)

    def base(t):
        c, u = push(t), M.progress(t, t_rise0, t_rise1, "sine")
        return Cam(M.lerp(c.x, R.x, u), M.lerp(c.y, R.y, u), M.lerp(c.w, R.w, u), c.rot)
    shake1 = M.shake(9, t_crash - 0.02, t_crash + 0.7, freq=8, seed=4)
    shake2 = M.shake(4, t_point_splash, t_point_splash + 0.45, freq=8, seed=9)

    def cam(t):
        c = base(t)
        a, b = shake1(t), shake2(t)
        roll = (0.25 + 0.15 * grow(t)) * math.sin(2 * math.pi * (t + OFF) / 5.4 + 2.2)   # s06's roll, continued
        hw, hh = c.w / 2 + 6, c.w * 9 / 32 + 6            # keep the view (with its roll and shake) on the painting
        x = min(max(c.x + a.dx + b.dx, hw), W - hw)
        y = min(max(c.y + a.dy + b.dy, hh), DECK_CUT - hh)
        return Cam(x, y, c.w, roll + a.rot + b.rot)
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    sc.fx = [
        rain_fx(lambda t: 0.62 + 0.38 * grow(t)),
        spray_fx([(t_crash + 0.08, 1450, 220, 26), (t_crash + 0.2, 680, 150, 12),
                  (t_point_splash + 0.08, POINT_X, 150, 18)]),
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
    sc.sfx("cloth", t_crash + 0.08, gain_db=-15, pan=0.6)
    sc.sfx("footsteps", t_w0, dur=t_w1 - t_w0 + 0.1, gain_db=-17, pan=0.1, fade_out=0.15)
    sc.sfx("cloth", p2b - 0.04, gain_db=-14, pan=0.3)
    sc.sfx("cloth", p2c - 0.04, gain_db=-15, pan=0.3)
    sc.sfx("thunder", t_far_strike, dur=2.6, gain_db=-16, pan=0.3, fade_out=1.2)

    # key times, for reviewers (seconds from scene start)
    sc.events = {
        "swells rise ('海浪越来越大')": p0, "lightning + crash, flinch ('越来越凶')": p0b,
        "turn to Jonah, ginger walks up ('水手们问约拿')": (p0c, t_w0, t_w1), "Jonah lifts his head": t_jup,
        "plea ('我们该拿你怎么办')": p1, "shrug ('海才会平静下来呢')": p1b, "Jonah lowers his eyes": p1b + 0.35,
        "hand on chest ('你们把我抬起来')": p2, "turn + point ('扔进海里')": p2b, "breaker answers": t_point_splash,
        "back, open hand ('海就会平静下来')": p2c, "chest ('我知道')": p3, "look up + far flash ('这场大风浪')": p3b,
        "bow, crew sad ('都是因为我')": p3c, "camera rises to the storm": (t_rise0, t_rise1),
    }
    return sc
