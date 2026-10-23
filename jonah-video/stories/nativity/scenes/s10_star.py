"""Scene 10 — far away in the East, the wise men see the star and set off (Matthew 2:1-2, 9).

N '在很远很远的东方，住着几位博士。博士，就是很有学问、会研究星星的人。' / N '有一天，他们看见天上出现了一颗特别的星星。' /
W '这颗星告诉我们，有一位王出生了。我们去拜他吧！' / N '他们出发了。走啊走，走啊走，走了好久好久。'

One 4000 x 1480 stage at dusk (s11_gifts shares it): violet-rose sky with the first stars, far violet hills, a ziggurat,
dunes with palms and a trader's tent on the left, the Eastern city (mud-brick houses with blue tiles and turquoise
domes, lit windows that flicker, a city wall with a blue glazed gate and gold rosettes), and in front the wise men's
rooftop observatory (props.observatory, clipped at a corner pier) with a stepped tower, an armillary sphere, a table
with charts and a lamp, a striped rug and the three treasures on cushions. Beats (character onsets measured on the
voice clip with the speech recogniser, see syllables(); nothing is hard-coded to the take):
  line 0  '在很远很远的东方'  a slow pan from the dunes across the gate to the city ...
          '住着几位博士'       ... arriving on the roof terrace with the three wise men (facing left, toward the city);
          '很有'  Melchior lifts his star chart (study);  '学问'  Balthasar unrolls a scroll;  '研究'  Caspar holds up
          his astrolabe and sights the sky;  '星星'  Balthasar points out a constellation and golden dotted lines join
          its stars one by one (sparkle) until '的人'.
  line 1  '看见'  they look up (Caspar first, then Melchior over his chart, then Balthasar), the camera eases in;
          '出现'  the special star rises from behind the far hills over the city (rising sweep);  '特别'  it flares to
          full brightness with a sparkle burst and a chime, and keeps pulsing.
  line 2  '这颗星'  Melchior points up at it;  '王'  Caspar (astrolabe raised) and Balthasar cheer (sparkle);
          '我们去'  all three bend to their treasures;  '拜'  they stand holding them (carry_gift) - the cushions are empty.
  line 3  a page-turn dip through the paper colour (no two shots' people overlap) to THE JOURNEY: the three camels with
          their riders (props.camel saddles + wise_men 'ride') walk in place while their ground strip scrolls with the
          planted feet; '走' '走' '走' '走' '走' each land a footfall (soft thud); the day-phase sky runs from night through
          dawn, a smiling sun with clouds, evening and night again twice (sun and moon on their own arcs, a light tint
          follows the sky); the landscape changes on the 走 beats: dunes with the city far behind -> rose rocky mesas ->
          dunes past a palm oasis -> the night road with dark hills and olive trees ahead. The star does not lead them
          (Matthew 2:9: it appears again in s11).
  end     the caravan on the night road, still walking. s11_gifts draws the same layers (add_journey(late=True)) at
          journey time t + (this duration - 1 s), so the 1 s cross-dissolve is pixel-identical.
Pose changes are hard cuts sold by squash-and-hop (Actor); camels are planted-foot walk cycles (16 drawings).
"""
import difflib
import math
import random
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene
from stories.david.scenes.s08_saul import Actor, TightSprite, sparkle_dyn
from stories.noah.scenes.s01_title import char_times, snap, voice_marks

# ================================================================== stage and geometry (s11_gifts shares the stage)
SW, SH = 4000, 1480
INK = P["ink"]
HZ = 1040                       # East panorama: foot of the far ridges (the horizon)
OBS_X, FY, KO = 3080, 1180, 1.0  # the rooftop observatory (prop anchor = terrace floor), its scale
OBS_CUT = 2434                  # the observatory building's left corner (the prop is clipped there)
K = 1.0                         # the wise men on the roof
MEN_Y = FY - 22
MEN_X = (2690, 3110, 3520)      # Melchior (gold), Caspar (frankincense), Balthasar (myrrh); all face left
GIFT_X = (2560, 2980, 3390)
CAM0 = Cam(1210, 730, 2400)     # first frame: the dunes and the city
CAM_J = Cam(2840, 825, 2112)    # the roof framing = the journey framing (s11 starts on it)
JX0, JY0 = CAM_J.x - 1056, CAM_J.y - 594   # top-left of the journey view on the stage
STAR_UP = (2230, 560)           # where the special star stands after rising (over the city, beyond the corner)
CONST = [(2560, 470), (2700, 400), (2850, 455), (2990, 380), (3120, 470), (3010, 560)]   # the constellation

# journey (view-local coordinates u, v in 0..2112 x 0..1188 of CAM_J)
GV = 1010                       # ground line under the camels
CS = 0.72                       # camel / rider scale
CAR_U = (1420, 1030, 640)        # Melchior leads, then Caspar, then Balthasar
SADDLES = ("red", "green", "purple")
STRIDE = 113 * CS               # stage px the ground passes per walk cycle (planted feet)
NPH = 16                        # camel walk drawings per cycle
XF = 1.0                        # the film's cross-dissolve


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def jdoc(body, defs=""):
    """A journey-view drawing given in view-local coordinates, placed on the stage at the journey framing."""
    return doc(f'<g transform="translate({JX0:.0f},{JY0:.0f})">{body}</g>', defs)


def keyed(keys_, curve="sine"):
    """Scalar keyframes [(t, v), ...] -> f(t), eased between keys."""
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


def alpha_m(fn):
    return lambda t: Tf(alpha=clamp(fn(t)))


# ================================================================== voice timing (shared with s11_gifts)
PUNCT = "，。？！：；、…,.?!:;“”‘’（）《》 　"
_ASR = [None]
_SYL = {}


def _recognizer():
    if _ASR[0] is None:
        import sherpa_onnx as so
        from engine.paths import MODELS
        d = MODELS / "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17"
        _ASR[0] = so.OfflineRecognizer.from_sense_voice(model=str(d / "model.int8.onnx"), tokens=str(d / "tokens.txt"),
                                                         language="zh", use_itn=False, num_threads=1)
    return _ASR[0]


def _spoken(text):
    return "".join(ch for ch in text if ch not in PUNCT)


def syllables(ctx, li):
    """Onset (s from scene start) of every spoken character of line li (punctuation dropped). Measured on the voice clip
    with the speech recogniser's per-character timestamps (the recogniser voice/tts.py times the subtitle chunks with),
    aligned to the script so misheard characters (星 heard as 心, 伯利恒 as 柏利横) are interpolated. Fallback: the
    energy-pause phrase marks of the Noah film (voice_marks / char_times)."""
    key = (ctx.id, li)
    if key in _SYL:
        return _SYL[key]
    ln = ctx.lines[li]
    ref = _spoken(ln.text)
    out = None
    try:
        import soundfile as sf
        from math import gcd
        from scipy import signal
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{li:02d}.wav"), dtype="float32")
        if x.ndim > 1:
            x = x.mean(1)
        if abs(len(x) / sr - (ln.end - ln.start)) > 0.4:
            raise ValueError("clip length does not match the timeline")
        g = gcd(16000, sr)
        y = signal.resample_poly(x, 16000 // g, sr // g).astype(np.float32)
        rec = _recognizer()
        st = rec.create_stream()
        st.accept_waveform(16000, y)
        rec.decode_stream(st)
        hyp, hyp_t = "", []
        for tk, tm in zip(st.result.tokens, st.result.timestamps):
            for ch in tk.strip():
                hyp += ch
                hyp_t.append(float(tm))
        anchors = {}
        sm = difflib.SequenceMatcher(None, hyp, ref, autojunk=False)
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                anchors[b + k] = hyp_t[a + k]
        if len(anchors) < max(2, len(ref) // 2):
            raise ValueError(f"recognised {hyp!r}")
        xs = sorted(anchors)
        vals = list(np.interp(range(len(ref)), xs, [anchors[k] for k in xs]))
        for i in range(len(ref)):                  # extrapolate outside the first / last match (0.2 s per syllable)
            if i < xs[0]:
                vals[i] = anchors[xs[0]] - 0.2 * (xs[0] - i)
            elif i > xs[-1]:
                vals[i] = anchors[xs[-1]] + 0.2 * (i - xs[-1])
        for i in range(1, len(vals)):
            vals[i] = max(vals[i], vals[i - 1] + 0.02)
        out = [ln.start + max(0.0, v) for v in vals]
    except Exception as ex:                        # no model / no clip: energy-pause marks
        print(f"[{ctx.id}] line {li}: recogniser timing unavailable ({ex}); using voice_marks", file=sys.stderr)
        out = []
        for ent in voice_marks(ctx, li):
            out += char_times(ent)
        if len(out) != len(ref):
            out = [ln.start + (ln.end - ln.start) * i / max(1, len(ref)) for i in range(len(ref))]
    _SYL[key] = out
    return out


def ct(ctx, li, phrase, k=0, occ=0, frac=0.0):
    """Onset of character k of the occ-th occurrence of ``phrase`` in line li (an edited script falls back to ``frac``
    of the line, so it never breaks the build)."""
    ref = _spoken(ctx.lines[li].text)
    i = -1
    try:
        for _ in range(occ + 1):
            i = ref.index(phrase, i + 1)
    except ValueError:
        ln = ctx.lines[li]
        print(f"[{ctx.id}] phrase {phrase!r} not in line {li}", file=sys.stderr)
        return ln.start + (ln.end - ln.start) * frac
    return syllables(ctx, li)[min(len(ref) - 1, i + k)]


# ================================================================== figures (shared with s11_gifts)
_P = C._P
_MZ = C._MZ
MAGI_POSES = dict(C._MZ)
MAGI_POSES.update(
    cheer=_P(t=-4, h=-10, legs=((6, 2), (-6, -2)), arms=(("fk", 148, 166), ("fk", -148, -166)), hands=("open", "open"),
             look=(0.03, -0.06), expr="joyful"),
    cheer_astro=_P(t=-4, h=-10, legs=((6, 2), (-6, -2)), arms=(("fk", 148, 166), ("fk", 132, 158)), hands=("open", "fist"),
                   look=(0.03, -0.06), expr="joyful"),
    measure=_P(h=-18, legs=((5, 2), (-5, -2)), arms=(("fk", 14, 8), ("fk", 100, 132)), hands=("fist", "fist"),
               look=(0.03, -0.10), expr="thoughtful"),
    look_hold=_P(h=-24, arms=(("fk", 24, 56), ("fk", -6, -2)), hands=("open", "fist"), look=(0.03, -0.10), expr="amazed"),
    chart_look=dict(_MZ["study"], h=-22, look=(0.03, -0.10), expr="amazed"),
    point_out=_P(h=-16, legs=((5, 2), (-5, -2)), arms=(("fk", 118, 128), ("fk", -6, -2)), hands=("point", "fist"),
                 look=(0.03, -0.09), expr="happy"),
    point_chart=_P(h=-20, legs=((5, 2), (-5, -2)), arms=(("fk", 140, 166), ("fk", -6, -2)), hands=("point", "fist"),
                   look=(0.03, -0.10), expr="awed"),
    read=_P(h=16, arms=(("ik", "torso", 2.2, 0.55, 1), ("ik", "torso", 0.6, 0.50, 1)), hands=("fist", "fist"),
            look=(0.03, 0.07), expr="thoughtful"),
    reach_down=_P(t=26, h=8, drop=24, legs=(("ik", 30, 1), ("ik", -24, 1)), arms=(("ik", "abs", 96, -66, 1),
                  ("ik", "abs", 80, -62, 1)), hands=("open", "open"), expr="joyful"),
    ride_cheer=dict(_MZ["ride"], arms=(("fk", 140, 160), ("fk", -140, -160)), hands=("open", "open"), expr="joyful", h=-8),
    ride_point=dict(_MZ["ride"], arms=(("fk", 130, 150), ("ik", "body", 40, -24, 1)), hands=("point", "fist"),
                    expr="awed", h=-14, look=(0.03, -0.08)),
    ride_look=dict(_MZ["ride"], h=-14, look=(0.03, -0.08), expr="amazed"),
)


def blink(e):
    """An eyes-closed copy of expression e (registered once)."""
    name = f"n10_blink_{e}"
    C.EXPRS.setdefault(name, dict(C.EXPRS[e], eyes="closed"))
    return name


def _hang_astrolabe(W, sc=0.5):
    return f'<g transform="translate({f1(W[0])},{f1(W[1] + 86 * sc - 4)}) scale({sc})">{PR._astrolabe()}</g>'


def _rolled(W, ang=-60):
    return (f'<g transform="translate({f1(W[0])},{f1(W[1])}) rotate({ang}) scale(0.42)">{PR._scroll(False)}</g>')


def _items_front(D, items, gift_kind=None, gift_open=0.0, gift_glow=0.0, pose=None):
    """Things held in the hands, drawn over the arms: 'chart' (open star chart between the hands), 'scroll' (open scroll),
    'astro_near' / 'astro_far' (an astrolabe hanging from that hand), 'rolled_near' (a rolled chart), 'gift'."""
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        skin = D["skin"]
        s = ""
        fists = set()
        for it in items:
            if it in ("chart", "scroll"):
                c = ((W0[0] + W1[0]) / 2, (W0[1] + W1[1]) / 2 - 4)
                ang = math.degrees(math.atan2(W0[1] - W1[1], W0[0] - W1[0]))
                if it == "chart":
                    s += (f'<g transform="translate({f1(c[0])},{f1(c[1])}) rotate({f1(ang)}) scale(0.62)">'
                          f'{C._star_chart_svg()}</g>')
                else:
                    ln = math.hypot(W0[0] - W1[0], W0[1] - W1[1])
                    s += (f'<g transform="translate({f1(c[0])},{f1(c[1])}) rotate({f1(ang)}) '
                          f'scale({0.36 * ln / 60:.3f},0.5)">{PR._scroll(True)}</g>')
                fists |= {0, 1}
            elif it == "astro_near":
                s += _hang_astrolabe(W1)
                fists.add(1)
            elif it == "astro_far":
                s += _hang_astrolabe(W0)
                fists.add(0)
            elif it == "rolled_near":
                s += _rolled(W1)
                fists.add(1)
            elif it == "gift":
                k = C._GIFT_HELD.get(pose, 0.62)
                c = ((W0[0] + W1[0]) / 2, max(W0[1], W1[1]) + 10 * k)
                s += (f'<g transform="translate({f1(c[0])},{f1(c[1])}) scale({k})">'
                      f'{PR._gift(gift_kind, gift_open, gift_glow)}</g>')
                s += C._hand(W1, (0.25, 1.0), "open", skin, hr) + C._hand(W0, (-0.2, 1.0), "open", skin, hr)
        for i in sorted(fists):
            s += C._fist((W0, W1)[i], hr, skin)
        return s
    return front


def magus(x, y, s, facing, v, pose, expr=None, items=(), gift_open=0.0, gift_glow=0.0, label="", ps=None):
    """A wise man (characters.wise_men's design and rig) in any MAGI_POSES pose (or an explicit pose record ``ps``,
    e.g. a planted-foot walk drawing, with ``pose`` naming how the gift is held), holding ``items``."""
    d = C._MAGI[v]
    D, m = C._magi_design(v)
    D["behind"] = C._mantle_drape(d["cape"])
    ps = dict(MAGI_POSES[pose]) if ps is None else dict(ps)
    if d.get("old") and pose in ("stand", "walk_a", "walk_b"):
        ps["t"] = ps["t"] + 4
    its = list(items)
    if pose in C._GIFT_HELD and "gift" not in its:
        its.append("gift")
    if pose == "study" and "chart" not in its:
        its.append("chart")
    if its:
        D["front"] = _items_front(D, its, d["gift"], gift_open, gift_glow, pose)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, m, ps, e, C._fsign(facing), True)
    if ps.get("lap"):
        sx, sy = C._seat_point(m)
        inner = C._reanchor(inner, sx, sy)
    return C._wrap_out(inner, x, y, s, facing, f"magus{v}-{pose}{label}")


def fig_sprite(scale, seed, wide=280, tall=480):
    cw, ch = 2 * wide * scale + 80, tall * scale + 130
    return TightSprite(cw, ch, cw / 2, ch - 40, seed=seed)


class Tinted:
    """Wraps a Dynamic fn (t -> (image, xy)) and multiplies its colours toward ``col`` by k(t) (moonlight), cached."""

    def __init__(self, fn, kfn, col=(104, 122, 178)):
        self.fn, self.kfn, self.col = fn, kfn, np.array(col, np.float32) / 255.0
        self._c = {}

    def __call__(self, t):
        out = self.fn(t)
        if out is None:
            return None
        k = round(clamp(self.kfn(t)) * 20) / 20
        if k <= 0:
            return out
        im, xy = out
        key = (id(im), k)
        if key not in self._c:
            if len(self._c) > 300:
                self._c.clear()
            a = np.asarray(im).astype(np.float32)
            a[..., :3] *= (1 - k + k * self.col)
            self._c[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
        return self._c[key], xy


# ================================================================== East panorama drawings
DUSK = "dusk"


def nt(col, k=1.0):
    return PR._nt(col, DUSK, k)


def _house(x, base, w, h, col, seed, dome=None, lit=0.6, tiles=True, s=1.0, lit_out=None):
    """A flat-roofed mud-brick house of the Eastern city (bottom centre x, base), optional dome, arched windows."""
    rng = random.Random(seed)
    out = PR._rect(x - w / 2, base - h, w, h, col, 3.4 * s)
    out += PR._rect(x - w / 2 - 6 * s, base - h - 10 * s, w + 12 * s, 14 * s, S.shade(col, 0.12), 3 * s)
    if tiles:
        out += PR._rect(x - w / 2, base - h + 12 * s, w, 12 * s, nt("#3a6aa8", 0.8), 0)
        for k in range(int(w / (26 * s))):
            out += PR._circ(x - w / 2 + 13 * s + k * 26 * s, base - h + 18 * s, 3.4 * s, nt("#e8b84e", 0.5), 0)
    if dome:
        r = w * 0.32
        out += PR._p(f"M{f1(x - r)},{f1(base - h - 4 * s)} A{f1(r)},{f1(r * 1.05)} 0 0 1 {f1(x + r)},{f1(base - h - 4 * s)} Z",
                     nt(dome, 0.7), 3.2 * s)
        out += PR._p(f"M{f1(x - r * 0.5)},{f1(base - h - r * 0.7)} Q{f1(x - r * 0.1)},{f1(base - h - r * 0.98)} "
                     f"{f1(x + r * 0.3)},{f1(base - h - r * 0.95)}", sw=3 * s, stroke=S.shade(nt(dome, 0.7), 0.35),
                     extra='opacity="0.7"')
        out += PR._line(x, base - h - r * 1.05, x, base - h - r * 1.05 - 16 * s, sw=3 * s)
        out += PR._circ(x, base - h - r * 1.05 - 18 * s, 4 * s, nt("#e8b84e", 0.4), 2 * s)
    nwin = max(1, int(w / (60 * s)))
    for k in range(nwin):
        wx = x - w / 2 + (k + 0.5) * w / nwin
        wy = base - h * rng.uniform(0.45, 0.62)
        on = rng.random() < lit
        fill = PR.LAMP if on else nt("#5a4a5a", 0.6)
        if on and lit_out is not None:
            lit_out.append((wx, wy + 4 * s, s))
        out += PR._p(f"M{f1(wx - 9 * s)},{f1(wy + 14 * s)} L{f1(wx - 9 * s)},{f1(wy - 4 * s)} "
                     f"A{f1(9 * s)},{f1(9 * s)} 0 0 1 {f1(wx + 9 * s)},{f1(wy - 4 * s)} L{f1(wx + 9 * s)},{f1(wy + 14 * s)} Z",
                     fill, 2.4 * s)
    if rng.random() < 0.5:
        dx = rng.uniform(-0.25, 0.25) * w
        out += PR._p(f"M{f1(x + dx - 12 * s)},{f1(base)} L{f1(x + dx - 12 * s)},{f1(base - 26 * s)} "
                     f"A{f1(12 * s)},{f1(12 * s)} 0 0 1 {f1(x + dx + 12 * s)},{f1(base - 26 * s)} L{f1(x + dx + 12 * s)},{f1(base)} Z",
                     nt("#6a4a3a", 0.6), 2.4 * s)
    return out


def _palm(x, y, s, lean=0.0, sway=0.0):
    return PR._place(PR._palm(lean, sway, True, True), x, y, s)


def east_sky_svg():
    sky = PR.starry_sky(-20, -20, SW + 20, HZ + 60, density=0.9, time=DUSK, seed=21, milky_way=True)
    # a few long thin violet clouds low over the horizon
    cl = ""
    rng = random.Random(5)
    for i in range(7):
        cx, cy = rng.uniform(100, SW - 100), rng.uniform(760, 940)
        w = rng.uniform(260, 520)
        cl += (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(w)}" ry="{f1(rng.uniform(9, 16))}" fill="#c48aa6" '
               f'opacity="0.35"/>')
    return doc(sky + f'<g filter="url(#soft)">{cl}</g>')


def east_far_svg():
    out = ""
    # two bands of far dunes / low hills along the horizon (cool violet)
    for k, (yy, amp, col) in enumerate(((HZ - 40, 110, "#b590ae"), (HZ + 0, 70, "#c49aa4"), (HZ + 40, 50, "#cfa69a"))):
        rng = random.Random(30 + k)
        pts = [(-60, yy)]
        x = -60
        while x < SW + 60:
            x += rng.uniform(300, 560)
            pts.append((x - rng.uniform(120, 200), yy - amp * rng.uniform(0.55, 1.0)))
            pts.append((x, yy - amp * rng.uniform(0.0, 0.25)))
        d = PR._sm(pts, closed=False) + f" L{SW + 80},{HZ + 260} L-80,{HZ + 260} Z"
        out += PR._p(d, col, 3)
    # the ziggurat (a stepped temple tower) far behind the city
    zx, zb = 1905, HZ + 70
    zc = nt("#c8a27a", 1.2)
    for i, (w, h) in enumerate(((420, 70), (330, 64), (240, 60), (160, 56))):
        yb = zb - sum(hh for _, hh in ((420, 70), (330, 64), (240, 60), (160, 56))[:i])
        out += PR._rect(zx - w / 2, yb - h, w, h, S.shade(zc, 0.04 * i), 3.2)
        out += PR._rect(zx - w / 2, yb - h + 8, w, 9, nt("#4a74ac", 1.0), 0)
    out += PR._p(f"M{zx - 26},{zb} L{zx - 14},{zb - 250} L{zx + 14},{zb - 250} L{zx + 26},{zb} Z", S.shade(zc, -0.1), 2.6)
    out += PR._rect(zx - 34, zb - 300, 68, 50, S.shade(zc, 0.1), 3)
    out += PR._p(f"M{zx - 10},{zb - 250} L{zx - 10},{zb - 272} A10,10 0 0 1 {zx + 10},{zb - 272} L{zx + 10},{zb - 250} Z",
                 PR.LAMP, 2.2)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


CITY_COLS = ("#dcb98a", "#d0a676", "#e6caa0", "#c99a68", "#d8b48c")
CITY_LIT = []          # lit windows of the front row of houses (filled by east_city_svg; their glows flicker)
DOMES = ("#3f8f9a", "#4a78b0", "#2f7a8a")


def east_city_svg():
    """Rows of houses climbing behind the city wall, palms between them (x 1330 .. SW)."""
    out = ""
    rng = random.Random(77)
    for row, (base, sc, step) in enumerate(((HZ + 40, 0.42, 110), (HZ + 95, 0.5, 130), (HZ + 150, 0.6, 150))):
        x = 1360 + rng.uniform(0, 60)
        while x < SW + 60:
            w = rng.uniform(110, 200) * sc / 0.5
            h = rng.uniform(120, 230) * sc / 0.5
            col = nt(rng.choice(CITY_COLS), 1.0 + 0.25 * (2 - row))
            dome = rng.choice(DOMES) if rng.random() < 0.28 else None
            out += _house(x, base, w, h, col, seed=row * 100 + int(x), dome=dome, lit=0.55, tiles=rng.random() < 0.5, s=sc / 0.5,
                          lit_out=CITY_LIT if row == 2 and 1420 < x < OBS_CUT - 60 else None)
            if rng.random() < 0.18:
                out += _palm(x + w / 2 + 14, base, 0.38 * sc / 0.5, lean=rng.uniform(-0.1, 0.1))
            x += w + rng.uniform(-10, 30)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


GATE_X = 1720
WALL_TOP, WALL_BASE = HZ + 130, HZ + 245


def city_glow_svgs(n=3):
    """n variants of soft glows over the city's lit windows (crossfaded: the lamps inside flicker gently)."""
    out = []
    for k in range(n):
        rng = random.Random(100 + k)
        b = ""
        for i, (x, y, s) in enumerate(CITY_LIT):
            a = rng.uniform(0.2, 0.75)
            b += PR._warm_glow(x, y, 46 * s, 40 * s, a, f"n10cw{k}_{i}")
        out.append(doc(b))
    return out


def east_clouds_svg():
    """Long thin dusk clouds that drift slowly across the sky."""
    rng = random.Random(15)
    cl = ""
    for i in range(9):
        cx, cy = rng.uniform(-200, SW + 200), rng.uniform(260, 880)
        w = rng.uniform(220, 460)
        cl += (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(w)}" ry="{f1(rng.uniform(10, 18))}" fill="#d6a0b8" '
               f'opacity="{rng.uniform(0.25, 0.4):.2f}"/>')
    return doc(f'<g filter="url(#soft)">{cl}</g>')


def east_wall_svg():
    """The city wall with a blue glazed gate (gold rosettes) and the sandy ground before it."""
    wc = nt("#d4a874", 1.0)
    out = ""
    x0 = 1330
    out += PR._rect(x0, WALL_TOP, SW + 40 - x0, WALL_BASE - WALL_TOP, wc, 4)
    for k in range(int((SW - x0) / 46) + 1):                       # merlons
        out += PR._rect(x0 + 8 + k * 46, WALL_TOP - 24, 28, 26, wc, 3)
    rng = random.Random(4)
    for _ in range(90):                                              # brick lines
        bx, by = rng.uniform(x0 + 10, SW), rng.uniform(WALL_TOP + 12, WALL_BASE - 12)
        out += PR._line(bx, by, bx + 30, by, sw=2, color=S.shade(wc, -0.18), extra='opacity="0.6"')
    out += PR._rect(x0, WALL_TOP + 26, SW + 40 - x0, 16, nt("#3a6aa8", 0.8), 0)
    # end tower at the left
    out += PR._rect(x0 - 50, WALL_TOP - 60, 110, WALL_BASE - WALL_TOP + 60, S.shade(wc, 0.05), 4)
    for k in range(3):
        out += PR._rect(x0 - 46 + k * 38, WALL_TOP - 84, 26, 26, S.shade(wc, 0.05), 3)
    # the gate: two towers and a deep-blue glazed arch with gold rosettes
    gb, gw, gh = WALL_BASE, 230, 300
    blue = nt("#2f5fa8", 0.6)
    for side in (-1, 1):
        tx = GATE_X + side * (gw / 2 + 50)
        out += PR._rect(tx - 55, gb - gh - 40, 110, gh + 40, blue, 4)
        for k in range(3):
            out += PR._rect(tx - 50 + k * 38, gb - gh - 64, 26, 26, blue, 3)
        for k in range(4):
            out += PR._circ(tx, gb - gh + 30 + k * 64, 10, nt("#e8b84e", 0.3), 2.4)
    out += PR._rect(GATE_X - gw / 2, gb - gh, gw, gh, blue, 4)
    out += PR._p(f"M{GATE_X - 70},{gb} L{GATE_X - 70},{gb - 150} A70,70 0 0 1 {GATE_X + 70},{gb - 150} L{GATE_X + 70},{gb} Z",
                 "#f4c46e", 4)
    out += PR._p(f"M{GATE_X - 70},{gb - 150} A70,70 0 0 1 {GATE_X + 70},{gb - 150}", sw=10, stroke=nt("#e8b84e", 0.3))
    for k in range(5):
        out += PR._circ(GATE_X - 90 + k * 45, gb - gh + 34, 9, nt("#e8b84e", 0.3), 2.4)
    out += PR._rect(GATE_X - gw / 2, gb - gh + 56, gw, 10, nt("#e8b84e", 0.3), 0)
    # sand before the wall, a road to the gate
    sand = nt("#e2bd86", 0.9)
    out += PR._p(f"M1180,{WALL_BASE - 4} L{SW + 40},{WALL_BASE - 4} L{SW + 40},{SH + 40} L1180,{SH + 40} Z", sand, 0)
    out += PR._line(1230, WALL_BASE - 4, SW + 40, WALL_BASE - 4, sw=3.4)
    out += PR._p(f"M{GATE_X - 70},{WALL_BASE} L{GATE_X + 70},{WALL_BASE} L{GATE_X + 260},{SH + 40} L{GATE_X - 420},{SH + 40} Z",
                 nt("#ecd0a0", 0.8), 0)
    for k in range(18):
        rx, ry = rng.uniform(1250, SW), rng.uniform(WALL_BASE + 30, SH)
        out += PR._p(f"M{f1(rx - 40)},{f1(ry)} Q{f1(rx)},{f1(ry - 10)} {f1(rx + 40)},{f1(ry)}", sw=2.4,
                     stroke=S.shade(sand, -0.14), extra='opacity="0.7"')
    # palms by the gate
    out += _palm(GATE_X - 260, WALL_BASE + 20, 0.62, lean=-0.08) + _palm(GATE_X + 300, WALL_BASE + 26, 0.55, lean=0.1)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def east_dunes_svg():
    """Dunes in front on the left, sloping down into the sand before the city."""
    out = ""
    rows = (   # (base, crest profile, ground y the tail settles on, colour)
        (HZ + 40, [(-80, 30), (240, -70), (560, -10), (860, -90), (1160, -30), (1420, 60)], WALL_BASE + 6, "#e9c48a"),
        (HZ + 150, [(-80, 10), (300, -110), (620, -30), (900, -120), (1160, -40)], WALL_BASE + 70, "#e2b676"),
        (HZ + 290, [(-80, -20), (260, -120), (620, -50), (980, -140), (1240, -40)], WALL_BASE + 150, "#dcac6c"),
    )
    for i, (by, prof, gy, col) in enumerate(rows):
        lit, shd = nt(col), nt(S.shade(col, -0.2))
        pts = [(x, by + dy) for x, dy in prof]
        ex = pts[-1][0]
        tail = [(ex + 260, gy - 6), (ex + 520, gy), (ex + 900, gy + 4)]
        d = PR._sm(pts + tail, closed=False) + f" L{tail[-1][0]},{SH + 40} L-80,{SH + 40} Z"
        out += PR._p(d, lit, 0)
        sh = ""
        for j in range(1, len(pts) - 1):
            a, b = pts[j], pts[j + 1]
            if a[1] < b[1]:
                dx = b[0] - a[0]
                sh += PR._p(f"M{f1(a[0])},{f1(a[1])} Q{f1(a[0] + dx * 0.5)},{f1(a[1] + 60)} {f1(a[0] + dx * 0.45)},{SH + 40} "
                            f"L{f1(b[0] + dx * 0.3)},{SH + 40} L{f1(b[0])},{f1(b[1])} Z", shd, 0)
            for k in range(3):
                yy = a[1] + 40 + 34 * k
                sh += PR._p(f"M{f1(a[0] - 140)},{f1(yy + 20)} Q{f1(a[0] - 70)},{f1(yy)} {f1(a[0] - 10)},{f1(yy + 16)}",
                            sw=2.2, stroke=nt(S.shade(col, -0.12)), extra='opacity="0.7"')
        line = PR._sm(pts + tail, closed=False)
        fade = f"n10dl{i}"
        out += PR._clip(f"n10dune{i}", d, sh)
        out += (f'<defs><linearGradient id="{fade}" gradientUnits="userSpaceOnUse" x1="{ex}" y1="0" x2="{ex + 600}" y2="0">'
                f'<stop offset="0" stop-color="{INK}" stop-opacity="1"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/>'
                f'</linearGradient></defs>'
                f'<path d="{line}" fill="none" stroke="url(#{fade})" stroke-width="3.4" stroke-linecap="round"/>')
    out += _palm(420, HZ + 120, 0.5, lean=0.06) + _palm(980, HZ + 190, 0.42, lean=-0.05)
    # a resting trader's caravan outside the gate (two loaded camels and a striped tent)
    tx, ty = 1290, WALL_BASE + 60
    tent = (f"M{tx - 120},{ty} L{tx - 20},{ty - 150} L{tx + 90},{ty} Z")
    out += PR._p(tent, nt("#c9714a", 0.8), 3.4)
    for k in range(3):
        out += PR._p(f"M{tx - 20},{ty - 150} L{tx - 100 + k * 70},{ty}", sw=6, stroke=nt("#f0dcb4", 0.8))
    out += PR._p(f"M{tx - 34},{ty} L{tx - 20},{ty - 70} L{tx - 6},{ty} Z", nt("#5a3a2a", 0.6), 2.6)
    out += PR._line(tx - 20, ty - 150, tx - 20, ty - 176, sw=3) + PR._p(f"M{tx - 20},{ty - 176} l26,8 l-26,8 Z", nt("#3a6aa8", 0.6), 2)
    out += PR.camel(tx + 170, ty + 26, 0.36, -1, pose="stand", load=True, bridle=False)
    out += PR.camel(tx + 300, ty + 44, 0.38, 1, pose="stand", load=True, bridle=False)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def obs_clip(markup, key):
    return (f'<clipPath id="n10oc{key}"><rect x="{OBS_CUT}" y="-10" width="{SW}" height="{SH + 20}"/></clipPath>'
            f'<g clip-path="url(#n10oc{key})">{markup}</g>')


def obs_back_svg():
    """The observatory building: its facade below the terrace, the clipped terrace (back part) and the corner pier."""
    tile = PR._nt("#dcc29a", DUSK, 0.6)
    out = ""
    # facade under the terrace (the building is in the foreground; its base is below the frame)
    fy0 = FY + 150 * KO
    out += PR._rect(OBS_CUT, fy0 - 10, SW + 40 - OBS_CUT, SH - fy0 + 60, S.shade(tile, -0.08), 4)
    out += PR._rect(OBS_CUT, fy0 + 30, SW + 40 - OBS_CUT, 22, PR._nt("#2f5f9a", DUSK, 0.5), 3)
    for k in range(9):
        wx = OBS_CUT + 140 + k * 190
        out += PR._p(f"M{wx - 30},{SH + 20} L{wx - 30},{fy0 + 110} A30,30 0 0 1 {wx + 30},{fy0 + 110} L{wx + 30},{SH + 20} Z",
                     PR.LAMP if k % 3 != 1 else PR._nt("#6a4a3a", DUSK, 0.6), 3)
    out = f'<g filter="url(#wobble)">{out}</g>'
    out += obs_clip(PR.observatory(OBS_X, FY, KO, 1, time=DUSK, part="back", lamp=1.0), "b")
    return doc(out)


def obs_corner_svg():
    """The terrace's left end (a corner pier with the parapets' tile bands) - in front of the people near it."""
    tile = PR._nt("#dcc29a", DUSK, 0.6)
    blue, gold = PR._nt("#2f5f9a", DUSK, 0.5), PR._nt("#e3b44f", DUSK, 0.3)
    x0, x1 = OBS_CUT - 30, OBS_CUT + 34
    top = FY - 300 * KO
    out = PR._rect(x0, top, x1 - x0, SH + 40 - top, tile, 4)
    out += PR._rect(x0 - 8, top - 22, x1 - x0 + 16, 26, S.shade(tile, 0.12), 3.4, rx=4)
    for yy, hh in ((FY - 230 * KO, 34 * KO), (FY + 64 * KO, 30 * KO), (FY + 180 * KO, 22)):
        out += PR._rect(x0, yy, x1 - x0, hh, blue, 3)
        out += PR._circ((x0 + x1) / 2, yy + hh / 2, 6, gold, 1.8)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def obs_front_svg():
    return doc(obs_clip(PR.observatory(OBS_X, FY, KO, 1, time=DUSK, part="front"), "f"))


def obs_deco_svg():
    """Details on the observatory: lit arched windows on the tower, a striped rug on the terrace floor."""
    out = ""
    for (x, y, w, h) in ((3640, 930, 34, 60), (3712, 930, 34, 60), (3395, 690, 32, 56), (3525, 690, 32, 56),
                         (3460, 520, 44, 80)):
        out += PR._warm_glow(x, y - h * 0.3, w * 1.8, h * 1.2, 0.5, f"n10tw{x}{y}")
        out += PR._p(f"M{x - w / 2},{y} L{x - w / 2},{y - h + w / 2} A{w / 2},{w / 2} 0 0 1 {x + w / 2},{y - h + w / 2} "
                     f"L{x + w / 2},{y} Z", PR.LAMP, 3)
    red, gold, blue = PR._nt("#a8323c", DUSK, 0.4), PR._nt("#e3b44f", DUSK, 0.3), PR._nt("#2f4f8a", DUSK, 0.4)
    q = [(2640, 1108), (3590, 1108), (3650, 1196), (2580, 1196)]

    def inset(k):
        return [(q[0][0] + k * 1.2, q[0][1] + k * 0.5), (q[1][0] - k * 1.2, q[1][1] + k * 0.5),
                (q[2][0] - k * 1.3, q[2][1] - k * 0.5), (q[3][0] + k * 1.3, q[3][1] - k * 0.5)]
    for k, col, sw in ((0, red, 3.4), (10, gold, 0), (16, blue, 0), (24, red, 0)):
        out += PR._p(PR._poly(inset(k)), col, sw)
    for i in range(5):
        cx = 2760 + i * 205
        out += PR._p(f"M{cx - 40},1152 L{cx},1134 L{cx + 40},1152 L{cx},1170 Z", gold, 2.2)
        out += PR._circ(cx, 1152, 6, blue, 1.6)
    for x in range(2590, 3650, 26):
        out += PR._line(x, 1197, x - 2, 1208, sw=2.2, color=gold)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def lamp_glow_svg(k=1.0):
    lx, ly = OBS_X + (640 - 100) * KO, FY - 250 * KO
    return doc(PR._warm_glow(lx, ly, 300, 230, 0.55 * k, "n10lamp"))


def cushion_gift_svg(i):
    x = GIFT_X[i]
    y = FY - 6
    col = ("#9b2f3c", "#2f6e5a", "#5b3a8a")[i]
    c = PR._p(f"M{x - 52},{y} Q{x - 56},{y - 26} {x},{y - 28} Q{x + 56},{y - 26} {x + 52},{y} Q{x},{y + 8} {x - 52},{y} Z",
              PR._nt(col, DUSK, 0.3), 3.2)
    c += PR._circ(x - 50, y - 4, 5, PR._nt("#e3b44f", DUSK, 0.3), 1.8) + PR._circ(x + 50, y - 4, 5, PR._nt("#e3b44f", DUSK, 0.3), 1.8)
    return doc(PR._place(c, 0, 0, 1.0) + PR.gift(x, y - 14, 0.62 * K, 1, kind=PR.GIFT_KINDS[i]))


def star_svg(intensity, pulse=0.0):
    return doc(PR.the_star(STAR_UP[0], STAR_UP[1], 0.5, intensity=intensity, pulse=pulse))


# ================================================================== journey drawings (view-local u, v)
def _sky_cols(ph):
    return PR._sky_at(ph % 1.0)


def jsky_svg(ph):
    cols = _sky_cols(ph)
    gid = f"n10js{int(round((ph % 1.0) * 1000))}"
    return jdoc(f'<rect x="-60" y="-60" width="2232" height="1100" fill="url(#{gid})"/>',
                S.lin_grad(gid, [(0, cols[0]), (0.32, cols[1]), (0.62, cols[2]), (0.86, cols[3]), (1, cols[4])]))


def jstars_svg():
    rng = random.Random(91)
    dots = ""
    for i in range(140):
        u, v = rng.uniform(-40, 2150), rng.random() ** 1.4 * 700
        dots += f'<circle cx="{f1(u)}" cy="{f1(v)}" r="{f1(rng.uniform(1.3, 3.0))}"/>'
    tw = ""
    for i in range(14):
        tw += PR._twinkle(rng.uniform(0, 2112), rng.uniform(20, 600), rng.uniform(7, 13), "#fff6d6")
    return jdoc(f'<g fill="#fff6d2">{dots}</g>{tw}')


def jclouds_svg():
    out = ""
    for i, (u, v, w) in enumerate(((300, 210, 300), (900, 130, 220), (1450, 260, 340), (2050, 170, 260), (2600, 230, 300))):
        out += S.cloud(u, v, w, w * 0.42, fill="#fbf6ea", seed=70 + i, puffs=5, sw=3.2, shade_fill="#dfe6ee")
    return jdoc(out)


def _arc(a):
    """Sun / moon path across the journey sky (a 0..1 from the left horizon to the right horizon)."""
    return 1056 + 930 * math.cos(math.pi * (1 - a)), 860 - 640 * math.sin(math.pi * a)


def jsun_svg():
    return jdoc(PR._warm_glow(0, 0, 170, 170, 0.75, "n10sun", "#fff6d2", P["sun"]) + PR._g(PR._sun_icon(46), None))


def jmoon_svg():
    r = 40
    d = (f"M{f1(r * 0.2)},{f1(-r)} A{r},{r} 0 1 0 {f1(r * 0.2)},{f1(r)} A{f1(r * 0.78)},{f1(r * 0.86)} 0 1 1 {f1(r * 0.2)},{f1(-r)} Z")
    return jdoc(PR._warm_glow(0, 0, 120, 120, 0.35, "n10moon", "#f6f0dc", "#c8d4f0") +
                PR._p(d, "#f6eed2", 3.2, extra='filter="url(#wobble-fine)"'))


def _ridge(y, amp, n, seed, col, x0=-80, x1=2200, bottom=1260, sw=3.2, smooth=True):
    rng = random.Random(seed)
    pts = [(x0, y + rng.uniform(-amp, 0) * 0.3)]
    for i in range(1, n + 1):
        pts.append((x0 + (x1 - x0) * i / n, y - amp * rng.uniform(0.2, 1.0)))
    d = PR._sm(pts, closed=False) + f" L{x1},{bottom} L{x0},{bottom} Z"
    return PR._p(d, col, sw)


def card_far_svg(kind):
    """The far landscape of one journey card (static), down to just below the top of its ground strip."""
    out = ""
    if kind == "A":                 # leaving the city: dunes, the city's skyline far behind on the left
        out += _ridge(760, 40, 6, 3, "#d8c0a0")
        sk = ""
        for (u, w, h, dome) in ((150, 70, 60, False), (215, 60, 90, True), (285, 90, 50, False), (360, 50, 70, True),
                                (430, 80, 45, False)):
            sk += PR._rect(u - w / 2, 745 - h, w, h, "#b89aa0", 2.6)
            if dome:
                sk += PR._p(f"M{u - w * 0.3},{745 - h} A{w * 0.3},{w * 0.32} 0 0 1 {u + w * 0.3},{745 - h} Z", "#8aa0b8", 2.4)
        for i, (w, h) in enumerate(((150, 30), (110, 28), (70, 26))):         # the little ziggurat
            yb = 745 - sum(hh for _, hh in ((150, 30), (110, 28), (70, 26))[:i])
            sk += PR._rect(520 - w / 2, yb - h, w, h, "#c0a08c", 2.4)
        out += sk
        out += PR.desert_dunes(-80, 2200, 900, 0.62, time="day", seed=11, bottom=1100)
    elif kind == "B":               # rocky hills, rose and ochre mesas
        out += _ridge(700, 60, 5, 21, "#d9b2a2")
        for (u, w, h, col) in ((260, 380, 210, "#c98a6a"), (820, 300, 150, "#d49a78"), (1460, 460, 250, "#c07e62"),
                               (1980, 300, 170, "#cf9474")):
            top = 820 - h
            pts = [(u - w / 2 - 50, 840), (u - w / 2, top + 30), (u - w / 2 + 30, top), (u + w / 2 - 30, top),
                   (u + w / 2, top + 26), (u + w / 2 + 60, 840)]
            out += PR._p("M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z", col, 3.2)
            for k in range(3):
                yy = top + 40 + k * (h - 40) / 3
                out += PR._line(u - w / 2 + 10 + k * 6, yy, u + w / 2 - 10 - k * 6, yy, sw=2.4, color=S.shade(col, -0.18),
                                extra='opacity="0.6"')
            out += PR._p(f"M{f1(u + w / 2 - 30)},{f1(top)} L{f1(u + w / 2)},{f1(top + 26)} L{f1(u + w / 2 + 60)},840 "
                         f"L{f1(u + w / 2 - 20)},840 Z", S.shade(col, -0.16), 0)
        out += _ridge(860, 70, 7, 25, "#e0b48a", bottom=1100)
        rng = random.Random(8)
        for i in range(12):
            u, v = rng.uniform(0, 2112), rng.uniform(840, 900)
            out += S.cloud(u, v, 70, 34, fill="#9aa064", seed=i, puffs=3, sw=2.6, shade_fill="#7a8048")
    elif kind == "C":               # dunes in the evening light; the oasis is on its own (moving) layer
        out += _ridge(740, 50, 6, 31, "#e2c49a")
        out += PR.desert_dunes(-80, 2200, 920, 0.6, time="day", seed=17, bottom=1100)
    elif kind == "D":               # night: the road goes on toward dark rounded hills ahead (right)
        out += _ridge(720, 40, 5, 41, PR._nt("#8a9a7a", "night", 1.1))
        out += PR._p(PR._sm([(-80, 860), (400, 830), (900, 790), (1300, 700), (1700, 600), (2200, 560)], closed=False) +
                     " L2200,1100 L-80,1100 Z", PR._nt("#7f9466", "night"), 3.2)
        out += PR._p(PR._sm([(1100, 860), (1500, 760), (1850, 640), (2200, 620)], closed=False) + " L2200,1100 L1100,1100 Z",
                     PR._nt("#6e8a58", "night"), 3.2)
        rng = random.Random(44)
        for i in range(9):          # olive trees on the slopes
            u = rng.uniform(250, 2100)
            v = 860 - (u - 200) * 0.14 + rng.uniform(-10, 30)
            k = 0.6 + 0.4 * (v - 600) / 300
            out += PR._tube(f"M{f1(u)},{f1(v)} Q{f1(u + 6 * k)},{f1(v - 34 * k)} {f1(u - 4 * k)},{f1(v - 60 * k)}", 9 * k,
                            PR._nt(PR.NAT_WOOD_DARK, "night"), 2.2)
            out += S.cloud(u, v - 78 * k, 120 * k, 66 * k, fill=PR._nt("#7f9a5a", "night"), seed=60 + i, puffs=4, sw=2.6,
                           shade_fill=PR._nt("#5f7a42", "night"))
    return jdoc(f'<g filter="url(#wobble)">{out}</g>')


STRIP_V0, STRIP_H, STRIP_X0 = 880, 330, 100    # ground strip sprites: view-local v 880 .. 1210, u from -100


def ground_strip(kind, seed):
    """A card's ground strip as a sprite (it scrolls further than the stage canvas reaches): anchor = view-local (0, 880)."""
    sp = TightSprite(2192 + 700 + 2 * STRIP_X0, STRIP_H, STRIP_X0, 0, seed=seed)
    sp.add(f'<g transform="translate({STRIP_X0},{-STRIP_V0})">{card_ground_svg(kind)}</g>')
    return sp


def card_ground_svg(kind, extra=700):
    """The near ground strip markup a card's caravan walks on (view-local u from -80 to 2192 + extra; it scrolls
    left)."""
    rng = random.Random({"A": 1, "B": 2, "C": 3, "D": 4}[kind])
    x0, x1 = -80, 2192 + extra
    top = GV - 70
    out = ""
    if kind in ("A", "C"):
        col = "#efcf98" if kind == "A" else "#ecc690"
        out += PR._p(PR._sm([(x0, top + 10), (600, top - 6), (1300, top + 8), (2000, top - 4), (x1, top + 6)], closed=False) +
                     f" L{x1},1300 L{x0},1300 Z", col, 3.2)
        for i in range(int((x1 - x0) / 60)):
            u, v = rng.uniform(x0, x1), rng.uniform(top + 30, 1180)
            w = 30 + (v - top) * 0.15
            out += PR._p(f"M{f1(u - w)},{f1(v)} Q{f1(u)},{f1(v - 9)} {f1(u + w)},{f1(v)}", sw=2.4, stroke=S.shade(col, -0.15),
                         extra='opacity="0.75"')
        for i in range(int((x1 - x0) / 220)):
            u, v = rng.uniform(x0, x1), rng.uniform(top + 60, 1160)
            out += PR._ell(u, v, 16, 9, "#c9a27a", 2.4)
        if kind == "C":
            for i in range(int((x1 - x0) / 160)):
                u, v = rng.uniform(x0, x1), rng.uniform(top + 20, 1150)
                out += PR._p(f"M{f1(u - 12)},{f1(v)} l5,-22 l5,18 l5,-28 l5,24 l5,-18", sw=2.6, stroke="#5f8a3e")
    elif kind == "B":
        col = "#d9a87a"
        out += PR._p(PR._sm([(x0, top + 4), (700, top - 8), (1500, top + 6), (x1, top)], closed=False) +
                     f" L{x1},1300 L{x0},1300 Z", col, 3.2)
        for i in range(int((x1 - x0) / 70)):
            u, v = rng.uniform(x0, x1), rng.uniform(top + 30, 1180)
            r = 6 + (v - top) * 0.05 * rng.uniform(0.5, 1.4)
            out += PR._ell(u, v, r * 1.6, r, rng.choice(("#b48a6a", "#c49a7a", "#a87e60")), 2.2)
        for i in range(int((x1 - x0) / 260)):
            u, v = rng.uniform(x0, x1), rng.uniform(top + 30, 1120)
            out += S.cloud(u, v - 16, 70, 36, fill="#9aa064", seed=200 + i, puffs=3, sw=2.4, shade_fill="#7a8048")
    else:                           # D: the road at night
        grass = PR._nt("#7a9a58", "night")
        out += PR._p(PR._sm([(x0, top - 10), (800, top - 18), (1600, top - 6), (x1, top - 14)], closed=False) +
                     f" L{x1},1300 L{x0},1300 Z", grass, 3.2)
        road = PR._nt("#e0c69a", "night")
        out += PR._p(f"M{x0},{GV - 34} L{x1},{GV - 30} L{x1},{GV + 70} L{x0},{GV + 66} Z", road, 3.2)
        for i in range(int((x1 - x0) / 90)):
            u = rng.uniform(x0, x1)
            out += PR._ell(u, GV + rng.uniform(-20, 50), 9, 4, PR._nt("#bfa278", "night"), 0)
        for i in range(int((x1 - x0) / 50)):
            u, v = rng.uniform(x0, x1), rng.uniform(GV + 90, 1180)
            k = 0.7 + (v - GV) / 300
            out += PR._p(f"M{f1(u - 8 * k)},{f1(v)} l{f1(5 * k)},{f1(-16 * k)} l{f1(5 * k)},{f1(13 * k)} l{f1(5 * k)},{f1(-18 * k)} "
                         f"l{f1(5 * k)},{f1(15 * k)}", sw=2.2, stroke=PR._nt("#4f7a36", "night"))
            if rng.random() < 0.15:
                out += PR._circ(u + 14 * k, v - 8 * k, 4.5 * k, PR._nt(rng.choice(("#f2c94e", "#f2e8d4")), "night"), 1.6)
        for i in range(int((x1 - x0) / 300)):
            u, v = rng.uniform(x0, x1), rng.uniform(top + 10, GV - 50)
            out += PR._ell(u, v, 26, 13, PR._nt("#b4aa98", "night"), 2.4)
    return f'<g filter="url(#wobble)">{out}</g>'


def card_oasis_svg():
    """Card C's oasis on the middle plane (it slides past behind the caravan)."""
    return jdoc(PR.oasis(1800, 905, 0.62, 1, time="day") + PR._place(PR._palm(-0.1, 0, True, True), 1230, 925, 0.45))


# ================================================================== the caravan (shared with s11_gifts)
def camel_sprite(i, cs=CS):
    sp = TightSprite(560 * cs + 80, 520 * cs + 100, 160 * cs + 40, 400 * cs + 60, seed=300 + i)
    idx = [sp.add(PR.camel(sp.ax, sp.ay, cs, 1, pose="walk", phase=k / NPH, saddle=SADDLES[i], bridle=False, load=False))
           for k in range(NPH)]
    idx.append(sp.add(PR.camel(sp.ax, sp.ay, cs, 1, pose="stand", saddle=SADDLES[i], bridle=False, load=False)))
    return sp, idx


RIDER_POSES = ("ride", "ride_look", "ride_cheer", "ride_point", "ride_happy", "ride_blink")


def rider_sprite(i, cs=CS):
    sp = fig_sprite(cs, 320 + i, wide=240, tall=470)
    sp.ay = sp.ch - 140 * cs - 20      # the seat; the legs hang below it
    idx = {}
    for name in RIDER_POSES:
        if name == "ride_happy":
            idx[name] = sp.add(magus(sp.ax, sp.ay, cs, 1, i, "ride", expr="happy"))
        elif name == "ride_blink":
            idx[name] = sp.add(magus(sp.ax, sp.ay, cs, 1, i, "ride", expr=blink("kind")))
        else:
            idx[name] = sp.add(magus(sp.ax, sp.ay, cs, 1, i, name))
    return sp, idx


def gait(ctx10):
    """Walk phase of the caravan (cycles) as a function of journey time: the footfalls land on the spoken 走 of
    '走啊走，走啊走，走了好久好久' (near pair at whole cycles, far pair at half cycles), then a steady pace on (s11)."""
    li = 3
    try:
        steps = [ct(ctx10, li, "走啊走", 0, 0), ct(ctx10, li, "走啊走", 2, 0), ct(ctx10, li, "走啊走", 0, 1),
                 ct(ctx10, li, "走啊走", 2, 1), ct(ctx10, li, "走了", 0)]
    except Exception:
        ln = ctx10.lines[li]
        steps = [ln.start + (ln.end - ln.start) * f for f in (0.28, 0.39, 0.5, 0.6, 0.72)]
    for i in range(1, len(steps)):
        steps[i] = max(steps[i], steps[i - 1] + 0.3)
    r0 = 0.5 / (steps[1] - steps[0])
    r1 = 1 / 0.9

    def ph(t):
        if t <= steps[0]:
            return (t - steps[0]) * r0
        for i in range(len(steps) - 1):
            if t <= steps[i + 1]:
                return 0.5 * i + 0.5 * (t - steps[i]) / (steps[i + 1] - steps[i])
        return 0.5 * (len(steps) - 1) + (t - steps[-1]) * r1
    return ph, steps


def qphase(p):
    """The walk phase quantised to the drawings (camel frame and the rider's seat bob agree)."""
    return math.floor((p % 1.0) * NPH + 1e-6) / NPH


def add_camels(sc, tag, cs, base, us, phase, dx=None, stand=None, rider_sched=None, tint=None, alpha=None, z=60.0,
               bphase=0.0):
    """Three camels with their riders. Camel i stands on stage (base[0] + us[i] + dx(t), base[1]); phase(t) = walk phase
    (cycles; None = stand); rider_sched(i) -> [(t, rider pose, hop amp)] in scene time; tint(t) 0..1 moonlight;
    bphase shifts the riders' breathing clock (s11 matches s10's)."""
    for i in range(3):
        csp, cidx = camel_sprite(i, cs)
        rsp, ridx = rider_sprite(i, cs)
        u = us[i]

        def at(t, u=u):
            return base[0] + u + (dx(t) if dx else 0.0), base[1]

        def frame(t, cidx=cidx):
            p = phase(t)
            if p is None or (stand is not None and stand(t)):
                return cidx[-1], 0.0
            q = qphase(p)
            return cidx[int(round(q * NPH)) % NPH], q

        def camel_fn(t, csp=csp, frame=frame, at=at):
            a = 1.0 if alpha is None else alpha(t)
            if a <= 0.002:
                return None
            x, y = at(t)
            return csp.place(frame(t)[0], x, y, alpha=a)

        def pos(t, frame=frame, at=at):
            fr, q = frame(t)
            x, y = at(t)
            bob = -4 * math.sin(4 * math.pi * q) if q else 0.0
            return x + PR.CAMEL_SEAT[0] * cs, y + (PR.CAMEL_SEAT[1] + bob) * cs
        sched = rider_sched(i) if rider_sched else [(-10, "ride", 0)]
        act = Actor(rsp, [(ts, ridx[n], amp) for ts, n, amp in sched], pos, alpha=alpha, breathe=0.008, bper=2.6,
                    phase=0.3 * i + bphase / 2.6)
        x0, y0 = base[0] + u + 30 * cs, base[1]
        sc.add(f"{tag}_shadow{i}", doc(C.ground_shadow(x0, y0, cs, 330, 0.2)), z=z - 0.05 + 0.1 * i, wc=0,
               motion=lambda t: Tf(dx=(dx(t) if dx else 0.0), alpha=(1.0 if alpha is None else alpha(t))))
        sc.add_dynamic(f"{tag}_camel{i}", camel_fn if tint is None else Tinted(camel_fn, tint), z=z + 0.1 * i)
        sc.add_dynamic(f"{tag}_rider{i}", act if tint is None else Tinted(act, tint), z=z + 0.1 * i + 0.05)


# ================================================================== the journey (shared with s11_gifts)
def journey_plan(ctx10):
    """Card timing and the sky's day phase as functions of JOURNEY time (= s10 scene time; s11 adds its offset)."""
    ph, steps = gait(ctx10)
    li = 3
    t_go = ct(ctx10, li, "出发")
    t_in = min(t_go - 0.3, ctx10.lines[3].start - 0.05)           # middle of the page-turn dip roof -> journey
    tA = t_in
    tB = steps[2] - 0.22
    tC = steps[4] - 0.22
    tD = min(ctx10.lines[3].end - 0.1, ctx10.duration - XF - 0.6)   # card D is complete before the dissolve to s11
    sky = keyed([(tA, 0.80), (tB, 1.45), (tC, 1.85), (tD, 2.55), (tD + 0.5, 2.75)], "linear")
    return dict(ph=ph, steps=steps, t_in=t_in, tA=tA, tB=tB, tC=tC, tD=tD, sky=sky)


def add_journey(sc, ctx10, toff=0.0, rider_sched=None, z0=50.0, late=False, alpha=None):
    """All journey layers (cards A-D, sky, sun, moon, stars, caravan, light) keyed to journey time jt = t + toff.
    late=True (s11): only the night road of card D, whose drawings, seeds and order are the same as s10's, so s11's
    first second is s10's last second; alpha(t) then hides it all (after s11's page-turn dip)."""
    J = journey_plan(ctx10)
    ph, sky = J["ph"], J["sky"]
    jt = lambda t: t + toff                                   # noqa: E731
    dA, dX, dD = 0.55, 0.28, 0.5

    def card_alpha(name):
        if name == "A":
            return lambda t: 1.0 if jt(t) >= J["tA"] else 0.0
        t0, d = {"B": (J["tB"], dX), "C": (J["tC"], dX), "D": (J["tD"], dD)}[name]
        return lambda t: M.progress(jt(t), t0, t0 + d, "sine")
    aA, aB, aC, aD = (card_alpha(n) for n in "ABCD")
    aD_raw = aD
    if alpha is not None:
        aA0, aD0 = aA, aD
        aA = lambda t: aA0(t) * alpha(t)                      # noqa: E731
        aD = lambda t: aD0(t) * alpha(t)                      # noqa: E731
    # the sky: a day-phase flipbook (the sun and the moon travel on their own layers)
    NS = 24
    if late:                                                  # night (phase .75 = frame 18 of the flipbook)
        sc.add("j_sky", jsky_svg(18 / NS), z=z0, motion=alpha_m(aA), wc=0.6, seed=501)
    else:
        sky_frames = [jsky_svg(k / NS) for k in range(NS)]

        def sky_fa(t):
            return min((sky(jt(t)) % 1.0) * NS, NS - 1.0)
        sc.add("j_sky", sky_frames, z=z0, frame_at=sky_fa, motion=alpha_m(aA), wc=0.6, seed=501)

    def night(t):
        p = sky(jt(t)) % 1.0
        return clamp(1 - abs(p - 0.75) / 0.17) if 0.55 < p < 0.95 else 0.0
    sc.add("j_stars", jstars_svg(), z=z0 + 0.1, wc=0, seed=503,
           motion=lambda t: Tf(alpha=aA(t) * night(t) * (0.85 + 0.15 * math.sin(jt(t) * 3.1))))

    def body_motion(lo, hi):
        def m(t):
            p = sky(jt(t)) % 1.0
            if not (lo <= p <= hi):
                return Tf(alpha=0.0)
            a = (p - lo) / (hi - lo)
            u, v = _arc(a)
            edge = clamp(min(a, 1 - a) / 0.06)
            return Tf(dx=u, dy=v, alpha=aA(t) * edge)
        return m
    if not late:
        sc.add("j_sun", jsun_svg(), z=z0 + 0.2, wc=0.3, seed=505, motion=body_motion(0.0, 0.5))
    sc.add("j_moon", jmoon_svg(), z=z0 + 0.25, wc=0.3, seed=507, motion=body_motion(0.5, 1.0))

    def day(t):
        p = sky(jt(t)) % 1.0
        return clamp(min(p - 0.06, 0.46 - p) / 0.08)
    if not late:
        sc.add("j_clouds", jclouds_svg(), z=z0 + 0.3, wc=0.6, seed=509,
               motion=lambda t: Tf(dx=-14 * jt(t), alpha=aA(t) * day(t)))
    # cards: far (static) + ground strip (scrolls with the walk)
    gx = lambda t: -(ph(jt(t)) * STRIDE)                       # noqa: E731
    for n, a, z in (("A", aA, 1.0), ("B", aB, 2.0), ("C", aC, 3.0), ("D", aD, 4.0)):
        if late and n != "D":
            continue
        nxt = {"A": aB, "B": aC, "C": aD, "D": None}[n]
        vis = (lambda t, a=a, nxt=nxt: a(t) if nxt is None or nxt(t) < 0.999 else 0.0)
        sc.add(f"j_far{n}", card_far_svg(n), z=z0 + z, seed=511 + int(z) * 10, motion=alpha_m(vis))
        if n == "C":
            sc.add("j_oasis", card_oasis_svg(), z=z0 + z + 0.1, seed=545,
                   motion=lambda t, vis=vis: Tf(dx=0.8 * (gx(t) + J["ph"](J["tC"]) * STRIDE), alpha=clamp(vis(t))))
        g0 = ph(J[f"t{n}"]) * STRIDE                          # the strip starts at its painted position
        strip = ground_strip(n, 513 + int(z) * 10)
        sc.add_dynamic(f"j_ground{n}", lambda t, sp=strip, vis=vis, g0=g0: (
            None if vis(t) <= 0.002 else sp.place(0, JX0 + gx(t) + g0, JY0 + STRIP_V0, alpha=clamp(vis(t)))),
            z=z0 + z + 0.2)

    # light: the day phase tints cards A-C (card D is painted at night; the riders then get their own moonlight)
    def light(t):
        k = aA(t) * (1 - aD(t))
        if k <= 0.003:
            return None
        p = sky(jt(t)) % 1.0
        nn = clamp(1 - abs(p - 0.75) / 0.2) if 0.55 < p < 0.95 else 0.0
        warm = max(clamp(1 - abs(p - 0.5) / 0.09), clamp(1 - min(p, 1 - p) / 0.09))
        f = ((1 - 0.52 * nn) * (1 - 0.02 * warm), (1 - 0.42 * nn) * (1 - 0.15 * warm), (1 - 0.12 * nn) * (1 - 0.28 * warm))
        return tuple(1 - k * (1 - c) for c in f)
    if not late:
        sc.fx.append(mult_fx(light))
    add_camels(sc, "car", CS, (JX0, JY0 + GV), CAR_U, lambda t: ph(jt(t)), rider_sched=rider_sched,
               tint=lambda t: 0.42 * aD_raw(t),
               alpha=aA, z=z0 + 10, bphase=toff)
    return J


def paper_dip(t_mid, half=0.32):
    """A page-turn dip through the cream paper colour centred on t_mid (the film's own transition between places)."""
    col = (247, 240, 226)

    def fx(frame, t, view):
        a = 1 - M.progress(abs(t - t_mid), 0.0, half, "sine")
        if a <= 0.003:
            return frame
        ov = Image.new("RGBA", frame.size, (*col, int(255 * a)))
        return Image.alpha_composite(frame, ov)
    return fx


def mult_fx(fn):
    """Per-channel multiply over the whole frame: fn(t) -> (r, g, b) factors or None."""
    def fx(frame, t, view):
        r = fn(t)
        if r is None:
            return frame
        a = np.asarray(frame)
        out = cv2.multiply(a, (float(r[0]), float(r[1]), float(r[2]), 1.0))
        return Image.fromarray(out, "RGBA")
    return fx


# ================================================================== build
def build(ctx):
    T = ctx.duration
    sc = Scene(ctx, W=SW, H=SH)
    L = ctx.lines

    # ---------------------------------------------------------------- beats
    t_east = ct(ctx, 0, "东方")
    t_live = ct(ctx, 0, "住着")
    t_boshi = ct(ctx, 0, "博士", occ=1)
    t_hen = ct(ctx, 0, "很有")
    t_xue = ct(ctx, 0, "学问")
    t_yan = ct(ctx, 0, "研究")
    t_xx1 = ct(ctx, 0, "星星", 0)
    t_xx2 = ct(ctx, 0, "星星", 1)
    t_ren = ct(ctx, 0, "的人", 1)
    t_day = ct(ctx, 1, "有一天")
    t_see = ct(ctx, 1, "看见")
    t_out = ct(ctx, 1, "出现")
    t_spec = ct(ctx, 1, "特别")
    t_star2 = ct(ctx, 1, "星星", 1)
    t_this = ct(ctx, 2, "这颗星")
    t_king = ct(ctx, 2, "王")
    t_born = ct(ctx, 2, "出生")
    t_we = ct(ctx, 2, "我们去")
    t_bai = ct(ctx, 2, "拜")
    J = journey_plan(ctx)
    t_in = J["t_in"]

    # ---------------------------------------------------------------- camera
    cam_a = M.cam_keys([(0.0, CAM0), (t_boshi + 0.75, Cam(2800, 815, 2150)), (t_ren + 1.0, CAM_J),
                        (max(t_see, t_ren + 1.1), CAM_J), (t_spec + 1.2, Cam(2775, 800, 2050))], "sine")
    sc.camera = lambda t: cam_a(t) if t < t_in else CAM_J      # the cut hides in the page-turn dip

    # ---------------------------------------------------------------- the East (dusk, then night)
    east_vis = lambda t: 1.0 if t < t_in else 0.0             # noqa: E731
    sc.add("e_sky", east_sky_svg(), z=0)
    sc.add("e_clouds", east_clouds_svg(), z=0.3, wc=0, motion=lambda t: Tf(dx=7 * t, alpha=east_vis(t)))
    sc.add_dynamic("e_twinkle", sparkle_dyn((60, 60, SW - 60, 820), count=26, t0=-1, t1=t_in, size=(7, 13),
                                            period=2.2, drift=0, seed=17), z=0.5)
    # the special star: rises from behind the far dunes and brightens (behind the land while it is low)
    star_int = [0.25, 0.45, 0.7, 1.0]
    sfr = [star_svg(k) for k in star_int] + [star_svg(1.0, 0.5)]
    rise0, rise1 = t_out - 0.05, t_spec + 0.1

    def star_fa(t):
        if t < t_spec:
            return 2.0 * M.progress(t, rise0, t_spec, "sine")
        u = M.progress(t, t_spec, t_spec + 0.25, "out")
        if u < 1:
            return 2.0 + u
        return 3.0 + 0.5 + 0.5 * math.sin(2 * math.pi * (t - t_spec) / 2.4)

    sc.add("e_star", sfr, z=1.0, frame_at=star_fa,
           motion=lambda t: Tf(dy=560 * (1 - M.progress(t, rise0, rise1, "out")), alpha=(1.0 if t >= rise0 else 0.0) * east_vis(t)))
    sc.add("e_far", east_far_svg(), z=2)
    CITY_LIT.clear()
    sc.add("e_city", east_city_svg(), z=3)
    sc.add("e_cityglow", city_glow_svgs(3), z=3.05, wc=0,
           frame_at=lambda t: 1.0 + 0.95 * math.sin(t * 1.7) * math.cos(t * 0.63),
           motion=lambda t: Tf(alpha=east_vis(t)))
    sc.add("e_wall", east_wall_svg(), z=4)
    sc.add("e_dunes", east_dunes_svg(), z=5)
    sc.add("e_obs", obs_back_svg(), z=6)
    sc.add("e_deco", obs_deco_svg(), z=6.02)
    sc.add("e_lamp", [lamp_glow_svg(0.8), lamp_glow_svg(1.0), lamp_glow_svg(0.9)], z=6.1, wc=0,
           frame_at=lambda t: 1.0 + 0.9 * math.sin(t * 7.3) * math.sin(t * 2.9))

    # constellation lines drawn star to star while '会研究星星的人' is said
    sc.add_dynamic("e_const", constellation_dyn(t_xx1, t_ren + 0.5, t_day + 0.2), z=0.8)

    # ---------------------------------------------------------------- the wise men on the roof
    men = [None, None, None]
    sched = [None, None, None]
    # Melchior: stand -> study (chart) -> chart_look -> point_chart -> reach_down -> carry_gift
    sp = fig_sprite(K, 401)
    names = [("stand", "stand", (), None), ("stand_b", "stand", (), blink("kind")), ("study", "study", (), None),
             ("study_b", "study", (), blink("thoughtful")), ("chart_look", "chart_look", ("chart",), None),
             ("point_chart", "point_chart", ("rolled_near",), None), ("reach_down", "reach_down", (), None),
             ("carry", "carry_gift", (), "joyful")]
    idx0 = {n: sp.add(magus(sp.ax, sp.ay, K, -1, 0, p, items=it, expr=e)) for n, p, it, e in names}
    s0 = [(0, "stand", 0), (1.6, "stand_b", 0), (1.73, "stand", 0), (t_hen, "study", 1), (t_hen + 1.6, "study_b", 0),
          (t_hen + 1.73, "study", 0), (t_see + 0.12, "chart_look", 1), (t_this, "point_chart", 1),
          (t_we, "reach_down", 1), (t_bai, "carry", 1)]
    men[0] = (sp, idx0, s0)
    # Caspar: stand -> measure (astrolabe) -> look_hold -> cheer_astro -> reach_down -> carry_gift
    sp = fig_sprite(K, 402)
    names = [("stand", "stand", (), None), ("stand_b", "stand", (), blink("kind")),
             ("measure", "measure", ("astro_near",), None), ("look_hold", "look_hold", ("astro_near",), None),
             ("cheer", "cheer_astro", ("astro_near",), None), ("reach_down", "reach_down", (), None),
             ("carry", "carry_gift", (), "joyful")]
    idx1 = {n: sp.add(magus(sp.ax, sp.ay, K, -1, 1, p, items=it, expr=e)) for n, p, it, e in names}
    s1 = [(0, "stand", 0), (2.3, "stand_b", 0), (2.43, "stand", 0), (t_yan, "measure", 1), (t_see, "look_hold", 1),
          (t_king, "cheer", 1.2), (t_we + 0.08, "reach_down", 1), (t_bai + 0.06, "carry", 1)]
    men[1] = (sp, idx1, s1)
    # Balthasar: stand -> read (scroll) -> point_out -> look_up -> cheer -> reach_down -> carry_gift
    sp = fig_sprite(K, 403)
    names = [("stand", "stand", (), None), ("stand_b", "stand", (), blink("kind")), ("read", "read", ("scroll",), None),
             ("point", "point_out", ("rolled_near",), None), ("look", "look_up", (), None), ("cheer", "cheer", (), None),
             ("reach_down", "reach_down", (), None), ("carry", "carry_gift", (), "joyful")]
    idx2 = {n: sp.add(magus(sp.ax, sp.ay, K, -1, 2, p, items=it, expr=e)) for n, p, it, e in names}
    s2 = [(0, "stand", 0), (0.9, "stand_b", 0), (1.03, "stand", 0), (t_xue, "read", 1), (t_xx1, "point", 1),
          (t_see + 0.22, "look", 1), (t_king + 0.12, "cheer", 1.2), (t_we + 0.16, "reach_down", 1),
          (t_bai + 0.12, "carry", 1)]
    men[2] = (sp, idx2, s2)
    for i, (sp, idx, s_) in enumerate(men):
        sch = [(snap(ts), idx[n], amp) for ts, n, amp in s_]
        act = Actor(sp, sch, (lambda t, i=i: (MEN_X[i], MEN_Y)), alpha=lambda t: east_vis(t), breathe=0.010, bper=2.9,
                    phase=0.31 * i)
        sc.add(f"shadow{i}", doc(C.ground_shadow(MEN_X[i], MEN_Y, K, 150, 0.2)), z=6.5, wc=0)
        sc.add_dynamic(f"man{i}", act, z=7 + 0.1 * i)
    # the treasures on their cushions until they are picked up
    for i in range(3):
        t_pick = snap(t_bai + 0.06 * i)
        sc.add(f"gift{i}", cushion_gift_svg(i), z=6.8, motion=lambda t, tp=t_pick: Tf(alpha=1.0 if t < tp else 0.0))
    sc.add("e_front", obs_front_svg(), z=8)
    sc.add("e_corner", obs_corner_svg(), z=8.1)
    # the star's sparkle burst and soft twinkles round it
    sc.add_dynamic("star_sparks", sparkle_dyn((STAR_UP[0] - 230, STAR_UP[1] - 200, STAR_UP[0] + 230, STAR_UP[1] + 200),
                                              count=16, t0=t_spec, t1=t_in, size=(9, 18), period=1.3, drift=-8,
                                              seed=23), z=8.5)

    # ---------------------------------------------------------------- the journey
    tA = J["tA"]
    blinks = {0: (tA + 1.7, tA + 4.1), 1: (tA + 2.6, tA + 4.7), 2: (tA + 1.1, tA + 3.5)}

    def rsched(i):
        out = [(-10, "ride", 0)]
        for tb in blinks[i]:
            if tb < T - 1.3:
                out += [(snap(tb), "ride_blink", 0), (snap(tb + 0.13), "ride", 0)]
        return out
    add_journey(sc, ctx, 0.0, rider_sched=rsched, z0=50.0)
    sc.fx.append(paper_dip(t_in))

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0.0, dur=t_in + 0.6, gain_db=-23, fade_in=0.8, fade_out=0.6)
    sc.sfx("night", 0.0, dur=t_in + 0.6, gain_db=-21, fade_in=1.0, fade_out=0.6)
    sc.sfx("sparkle", t_xx1 + 0.05, gain_db=-19, pan=0.1)
    sc.sfx("grow", t_out - 0.1, gain_db=-20, pan=-0.4)
    sc.sfx("chime", t_spec, gain_db=-13, pan=-0.4)
    sc.sfx("sparkle", t_king, gain_db=-18, pan=-0.3)
    sc.sfx("cloth", t_we, gain_db=-18, pan=0.2)
    sc.sfx("whoosh", t_in + 0.05, gain_db=-20)
    sc.sfx("wind_hot", t_in, dur=J["tD"] + 0.4 - t_in, gain_db=-22, fade_in=0.6, fade_out=0.5)
    for k, ts in enumerate(J["steps"]):
        sc.sfx("thud", ts, gain_db=-19 + (k == 4), pan=0.1)
    sc.sfx("night", J["tD"], dur=T - J["tD"] + 0.3, gain_db=-22, fade_in=0.6, fade_out=0.8)
    return sc


def constellation_dyn(t0, t1, t_off):
    """Golden lines drawn from star to star of a constellation (t0 .. t1), fading out at t_off; the stars brighten."""
    pts = CONST
    pad = 40
    x0 = min(p[0] for p in pts) - pad
    y0 = min(p[1] for p in pts) - pad
    w = int(max(p[0] for p in pts) - x0 + pad)
    h = int(max(p[1] for p in pts) - y0 + pad)
    segs = list(zip(pts, pts[1:]))

    def fn(t):
        if t < t0 - 0.2 or t > t_off + 0.6:
            return None
        fade = 1 - M.progress(t, t_off, t_off + 0.6, "sine")
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        u = M.progress(t, t0, t1, "linear") * len(segs)
        col = (255, 226, 140, int(210 * fade))
        for k, (a, b) in enumerate(segs):
            f = clamp(u - k)
            if f <= 0:
                break
            ax, ay = a[0] - x0, a[1] - y0
            bx, by = ax + (b[0] - a[0]) * f, ay + (b[1] - a[1]) * f
            n = int(math.hypot(bx - ax, by - ay) / 14)
            for j in range(n + 1):           # dotted line
                px, py = ax + (bx - ax) * j / max(1, n), ay + (by - ay) * j / max(1, n)
                dr.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4], fill=col)
        for k, p in enumerate(pts):
            on = clamp(u - k + 1) if k else clamp(u * 3)
            if on <= 0:
                continue
            px, py = p[0] - x0, p[1] - y0
            r = 5 + 4 * on
            a = int(255 * fade * (0.5 + 0.5 * on))
            dr.ellipse([px - r * 2, py - r * 2, px + r * 2, py + r * 2], fill=(255, 240, 190, a // 5))
            dr.polygon([(px, py - r * 1.8), (px + r * 0.4, py - r * 0.4), (px + r * 1.8, py), (px + r * 0.4, py + r * 0.4),
                        (px, py + r * 1.8), (px - r * 0.4, py + r * 0.4), (px - r * 1.8, py), (px - r * 0.4, py - r * 0.4)],
                       fill=(255, 246, 210, a))
        return im, (x0, y0)
    return fn
