"""Scene 4 — the giant (1 Samuel 17:4-11).  Also the SHARED VALLEY of s11_face, s12_sling and s13_victory.

"这时候，非利士人的营里，走出来一个人。咚！咚！咚！ 他的名字叫歌利亚。他好高好高，差不多有篮球架那么高！
他戴着铜头盔，穿着铜盔甲，手里的枪，粗得像一根大木头。
(歌利亚) 以色列人听着！派一个人出来跟我打！他要是赢了，我们就做你们的仆人。要是我赢了，你们就做我们的仆人！
以色列人听了，吓得腿都软了。连扫罗王，也不敢出来。"

THE VALLEY (one 3800 x 2138 stage shared by s04 / s11 / s12 / s13, same camera language):
  sky with drifting clouds -> props.valley_elah (far ridges, the brook, the two hills) -> the camps on the hill tops
  (Israel's goat-hair tents and blue banners on the LEFT, the Philistines' red peaked tents on the RIGHT, banners
  ripple) -> the soldiers on the hill brows (small, far away) -> a near meadow (the valley floor in front, where
  everything happens) -> a big red Philistine tent at the right edge of the meadow (Goliath comes out from behind
  it) -> foreground rocks and swaying grass.  Everyone in the meadow stands on one ground line GY at one scale K:
  Goliath ~634 px, the shield-bearer ~340, David ~250.  Goliath always comes from the right and faces left; David
  comes from the left and faces right.

  line 0  "这时候，非利士人的营里，走出来一个人。"  calm wide view of the valley; the shield-bearer walks out from
          behind the big tent, then Goliath's crest and spear pass along above the tent and he steps out (heavy
          planted-foot stride, a soft thud and dust on every footfall).
          "咚！咚！咚！"  three giant stomps, each on its spoken syllable (onsets found in the voice take): dust
          bursts at the planted foot, the camera jolts, pebbles in the meadow hop.
  line 1  "他的名字叫歌利亚。"  the camera moves in; he plants his spear and sneers.
          "他好高好高，"  the camera tilts up his full height, from his sandals to the crest of his helmet.
          "差不多有篮球架那么高！"  a ghosted picture-book basketball hoop pops up beside him (rim at his helmet), a
          little ball bounces; it pops away.
  line 2  "他戴着铜头盔，穿着铜盔甲，手里的枪，"  the camera glides from the helmet down the scale armour to the
          spear; a twinkle on each as it is named.
          "粗得像一根大木头。"  a ghosted log appears beside the shaft (it is just as thick).
  line 3  (Goliath)  the camera pulls back across the valley: spear raised he shouts (sound arcs roll across the
          valley to Israel's hill); "派一个人出来跟我打！" he points; "他要是赢了…" smug; "要是我赢了…" shouts again
          (the Philistines on their hill cheer him on), and he laughs.
  line 4  "以色列人听了，吓得腿都软了。"  the camera crosses to Israel's hill: the soldiers cower behind their shields,
          knees trembling.  "连扫罗王，也不敢出来。" King Saul, at the front, hops back among them and hides behind a
          shield too.  Calm-ish last second (trembling) for the page turn.

Shared API used by s11 / s12 / s13 (import from here): the stage constants, add_valley(), Valley people helpers,
the figure drawing helpers (Goliath / David / shield-bearer walk and run drawings on the planted-foot rig),
Actor (a sprite performer with squash-and-hop pose cuts, rotation and breathing), dust puffs, light rays,
sparkle twinkles and the scene clock offsets (toff) that keep the cross-dissolves s11 -> s12 -> s13 seamless.
"""
import math
import random

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_N, walk_pose
from art.scenes.s15_city import Sprite as _BaseSprite
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene

INK = P["ink"]
_ALL_SPRITES = []


class Sprite(_BaseSprite):
    """art.scenes.s15_city.Sprite that registers itself, so build() can rasterise and watercolour every drawing up
    front (preload) instead of on the first frame that shows it."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        _ALL_SPRITES.append(self)


def preload():
    for sp in _ALL_SPRITES:
        sp.load()
    _ALL_SPRITES.clear()

# ================================================================== the shared valley stage
SW, SH = 3800, 2138
GY = 1880                      # meadow ground line (everyone's feet in the valley)
K = 1.3                        # person scale in the meadow (Goliath 824, adult 440, David 328)
VX0, VX1, VY, VS = -200, 4000, 1250, 1.2       # props.valley_elah placement (floor line VY)
KH = 0.5                       # people on the hill brows (far away)
MEADOW_Y = 1430                # top of the near meadow (it hides the bottom of the hills)

XG = 2950                      # Goliath's place facing David (end of s04, s11, start of s12)
XB = XG - round(240 * K)       # his shield-bearer, in front of him
XD = 750                       # David's place in s11 / start of s12
XD2 = 1350                     # David slings from here
TENT_X = 3720                  # the big Philistine tent at the right edge of the meadow
TENT_S = 1.8

GOLIATH_A, GOLIATH_LK = 95, 1.85    # planted-foot stride: ankle travel per half step (figure px), leg length k
DAVID_A, DAVID_LK = 40, 0.68
ADULT_A = 56
STEP_G = 2 * GOLIATH_A * K          # stage px per Goliath step
STEP_D = 2 * DAVID_A * K
XG2 = XG - 2 * STEP_G          # Goliath stops here in s12 (two strides) and falls toward David

ISRAEL_TENTS = ((0.07, 0.34), (0.16, 0.30), (0.24, 0.26))
PHIL_TENTS = ((0.93, 0.34), (0.84, 0.30), (0.76, 0.26))
# soldiers on the hill brows: (x, variant); x from the inside of each plateau toward the valley
ISRAEL_MEN = [(150, 0), (262, 1), (372, 2), (488, 3), (600, 0), (708, 1), (815, 2), (918, 3), (205, 2), (430, 1),
              (655, 3)]
SAUL_X = 1035
PHIL_MEN = [(3650, 0), (3540, 1), (3430, 2), (3315, 3), (3205, 1), (3095, 2), (2990, 0), (2885, 3), (3595, 2),
            (3370, 0), (3150, 3)]


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ground(x):
    """Ground y on the hills / valley floor of the backdrop at stage x."""
    return PR.valley_ground(x, VX0, VX1, VY, VS)


def phrase_t(line, phrase, frac=0.0):
    """Start of ``phrase`` inside its subtitle chunk (by character position); falls back to ``frac`` of the line."""
    for c in line.chunks:
        i = c.text.find(phrase)
        if i >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、…")))
            return c.start + (c.end - c.start) * i / n
    return line.start + (line.end - line.start) * frac


def onsets(ctx, li, t0, t1, n):
    """The n strongest syllable onsets (scene s) of utterance li inside [t0, t1], from the voice take; evenly
    spaced over the window if the take is missing (voices may be re-generated)."""
    ln = ctx.lines[li]
    try:
        import soundfile as sf
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{li:02d}.wav"), dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        hop = int(sr * 0.01)
        e = np.sqrt(np.convolve(x * x, np.ones(hop) / hop, mode="same")[::hop])
        a, b = int((t0 - ln.start) / 0.01), int((t1 - ln.start) / 0.01)
        a, b = max(1, a), min(len(e) - 1, b)
        rise = np.maximum(0, e[a:b] - np.concatenate([[e[a - 1]], e[a:b - 1]]))
        cand = []
        for i in np.argsort(-rise):
            if all(abs(i - j) > 18 for j in cand):
                cand.append(i)
            if len(cand) == n:
                break
        if len(cand) < n:
            raise ValueError
        out = []
        for i in sorted(cand):          # walk back to the start of the rise
            j = a + i
            while j > a and e[j - 1] < e[j] and e[j - 1] > 0.08 * e[a + i]:
                j -= 1
            out.append(ln.start + j * 0.01)
        return out
    except Exception:
        return [t0 + (t1 - t0) * (k + 0.2) / n for k in range(n)]


def scene_clock(scene_id):
    """Time offset (s) of this scene's t=0 on the shared clock of s11 -> s12 -> s13 (each dissolve overlaps 1 s),
    so every cyclic motion (clouds, grass, banners, breathing) continues exactly across the cross-dissolves."""
    from engine.loader import context
    order = ["s11_face", "s12_sling", "s13_victory"]
    if scene_id not in order:
        return 0.0
    off = 0.0
    for sid in order[:order.index(scene_id)]:
        try:
            off += context(sid).duration - 1.0
        except Exception:
            off += {"s11_face": 38.37, "s12_sling": 24.9}[sid] - 1.0
    return off


# ================================================================== backdrop drawings
SKY_TOP, SKY_MID, SKY_LOW = "#8cc6dd", "#bfe0e6", "#f6e6c2"


def sky_svg():
    defs = S.lin_grad("vsky", [(0, SKY_TOP), (0.45, SKY_MID), (0.78, SKY_LOW), (1, SKY_LOW)])
    defs += S.rad_grad("vsun", [(0, "#fff6d8", 0.95), (0.35, "#fbe7b0", 0.55), (1, "#fbe7b0", 0)])
    body = f'<rect x="-40" y="-40" width="{SW + 80}" height="{VY + 80}" fill="url(#vsky)"/>'
    body += f'<ellipse cx="760" cy="300" rx="760" ry="560" fill="url(#vsun)"/>'
    return doc(body, defs)


CLOUDS = [(520, 330, 520, 150, 4.0), (1650, 210, 420, 120, 3.0), (2700, 360, 600, 160, 5.0),
          (3420, 200, 380, 110, 3.5), (1120, 520, 300, 80, 6.0), (2250, 560, 340, 90, 4.5)]


def cloud_svg(i):
    x, y, w, h, _ = CLOUDS[i]
    fill = "#fbf3e4" if i < 4 else S.mix("#fbf3e4", SKY_MID, 0.35)
    return doc(S.g(S.cloud(x, y, w, h, fill=fill, seed=40 + i, puffs=5 if w > 400 else 4, sw=3,
                           shade_fill=S.mix(fill, "#b9c7d6", 0.5)), filter="wobble"))


VBOT = SH + 520                # the valley's own bottom: far below the meadow, so the hills' front edges run
#                                down behind it (only the narrowing floor between them shows)


def valley_back_svg():
    out = PR.valley_elah(VX0, VX1, VY, VS, part="back", camps=False, seed=2, bottom=VBOT)
    # far olive groves on the ridges (hazy)
    deco = ""
    rng = random.Random(5)
    for i in range(16):
        x = rng.uniform(900, 2900)
        y = VY - VALLEY_H * (0.55 + 0.06 * math.sin(i * 1.7)) + rng.uniform(-10, 30)
        deco += PR.olive_tree(x, y, rng.uniform(0.16, 0.24), seed=i)
    out += PR._haze(deco, "#cfe2df", 0.55, 0.45)
    return doc(out)


VALLEY_H = PR.VALLEY_HILL_H * VS


def valley_hills_svg():
    out = PR.valley_elah(VX0, VX1, VY, VS, part="hills", camps=False, seed=2, bottom=VBOT)
    rng = random.Random(9)
    deco = ""
    # trees behind the camps and bushes / boulders down the slopes
    for x, s_, kind in ((40, 0.5, "o"), (1010, 0.42, "o"), (2870, 0.45, "o"), (3700, 0.52, "o"), (1250, 0.5, "b"),
                        (2580, 0.5, "b"), (1420, 0.38, "b"), (2400, 0.4, "b"), (720, 0.45, "b"), (3080, 0.46, "b")):
        y = ground(x) + 8
        deco += PR.olive_tree(x, y, s_, seed=int(x)) if kind == "o" else PR.bush(x, y, s_, variant=rng.choice((0, 2)))
    for x in (1160, 1330, 2470, 2660, 980, 2950):
        y = ground(x) + rng.uniform(40, 120)
        deco += (f'<path d="{S.blob(x, y, 30, 17, 0.14, 9, seed=int(x))}" fill="#cfbe9b" stroke="{INK}" '
                 f'stroke-width="3.2"/>')
    shade_ = ""
    for cx, cy, rx, ry in ((700, 1180, 520, 110), (3100, 1180, 520, 110), (250, 1000, 300, 60), (3550, 1000, 300, 60)):
        shade_ += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#6f9440" opacity="0.22" '
                   f'filter="url(#blur-lg)"/>')
    return doc(out + shade_ + S.g(deco, filter="wobble-fine"))


BACK_TENTS = ((0.025, 0.25, -26), (0.115, 0.22, -30), (0.195, 0.2, -24))


def camp_svg(side, wave):
    out = ""
    back = ""
    for u, sc_, dy in BACK_TENTS:
        u = u if side == "israel" else 1 - u
        x = VX0 + (VX1 - VX0) * u
        back += PR.tent(x, ground(x) + dy, sc_ * VS, 1 if side == "israel" else -1, side, wave=wave + 0.3 + u)
    out += PR._haze(back, "#d8e6e0", 0.3, 0.25)
    for u, sc_ in (ISRAEL_TENTS if side == "israel" else PHIL_TENTS):
        x = VX0 + (VX1 - VX0) * u
        out += PR.tent(x, ground(x) + 4 * VS, sc_ * VS, 1 if side == "israel" else -1, side, wave=wave + u)
    return doc(out)


def _grass_strokes(rng, x0, x1, y0, y1, n, col, sw=2.6, k=1.0):
    out = ""
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = k * (0.6 + 0.8 * (y - y0) / max(1, y1 - y0))
        out += (f'<path d="M{f1(x)},{f1(y)} q{f1(7 * s)},{f1(-9 * s)} {f1(15 * s)},{f1(-13 * s)} M{f1(x + 5 * s)},'
                f'{f1(y)} q{f1(3 * s)},{f1(-7 * s)} {f1(2 * s)},{f1(-15 * s)}" fill="none" stroke="{col}" '
                f'stroke-width="{sw * s:.1f}" stroke-linecap="round" opacity="0.6"/>')
    return out


def meadow_top(x):
    """Top edge of the near meadow: a gentle rise in the middle hides where the hills dive into the valley floor."""
    up = M.progress(x, 1300, 1720, "sine") * (1 - M.progress(x, 2080, 2500, "sine"))
    return MEADOW_Y + 22 * math.sin(x / 520 + 0.7) + 12 * math.sin(x / 190 + 2.0) - 175 * up


def meadow_svg():
    rng = random.Random(7)
    pts = [(x, meadow_top(x)) for x in range(-80, SW + 120, 40)]
    d = S.smooth_path(pts, closed=False) + f" L{SW + 80},{SH + 60} L-80,{SH + 60} Z"
    defs = S.lin_grad("vmead", [(0, "#b4cd73"), (0.35, "#a3c264"), (1, "#86a94d")])
    body = f'<path d="{d}" fill="url(#vmead)"/>'
    inner = _grass_strokes(rng, -40, SW + 40, MEADOW_Y - 20, SH + 40, 520, "#6f9441", 2.6, 1.3)
    # a trodden earth patch where the champions meet (soft, no outline)
    for cx, cy, rx, ry in ((1900, 1905, 1150, 70), (1300, 1935, 620, 45), (2600, 1925, 700, 50)):
        inner += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#c9b77f" opacity="0.38" '
                  f'filter="url(#soft)"/>')
    # small flowers and pebbles
    for _ in range(70):
        x, y = rng.uniform(-40, SW + 40), rng.uniform(MEADOW_Y + 30, SH + 20)
        if 600 < x < 3300 and 1840 < y < 1960:
            continue
        c = rng.choice(["#f6e7a8", "#fbf3e4", "#f2b8c4", "#f2cf5b"])
        r = 4 + 5 * (y - MEADOW_Y) / (SH - MEADOW_Y)
        inner += "".join(f'<circle cx="{f1(x + r * 1.1 * math.cos(a))}" cy="{f1(y + r * 1.1 * math.sin(a))}" '
                         f'r="{f1(r * 0.7)}" fill="{c}"/>' for a in (0, 1.26, 2.51, 3.77, 5.03))
        inner += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.45)}" fill="#e9a23c"/>'
    for _ in range(26):
        x, y = rng.uniform(0, SW), rng.uniform(MEADOW_Y + 60, SH)
        r = 10 + 14 * (y - MEADOW_Y) / (SH - MEADOW_Y)
        inner += (f'<path d="{S.blob(x, y, r, r * 0.55, 0.15, 8, seed=int(x))}" fill="#d6c6a4" stroke="{INK}" '
                  f'stroke-width="2.6"/>')
    for cx, cy, rx, ry, col, op in ((600, 1560, 700, 90, "#7d9f45", 0.22), (3200, 1540, 800, 100, "#7d9f45", 0.22),
                                    (2000, 2080, 1400, 120, "#6f9440", 0.25), (1400, 1720, 500, 70, "#d8e69a", 0.3),
                                    (2700, 1700, 600, 80, "#d8e69a", 0.28)):
        inner += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}" '
                  f'filter="url(#blur-lg)"/>')
    inner += brook_markup()
    body += f'<clipPath id="vmc"><path d="{d}"/></clipPath><g clip-path="url(#vmc)">{inner}</g>'
    body += f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{INK}" stroke-width="4" ' \
            f'stroke-linecap="round"/>'
    return doc(S.g(body, filter="wobble"), defs)


BROOK = [(1755, 0), (1650, 1488), (1400, 1534), (1080, 1562), (780, 1604), (450, 1668), (140, 1730), (-140, 1790)]


def brook_markup():
    """The little brook of the valley continues across the meadow, behind everyone (David's stones, s10)."""
    pts = [(x, meadow_top(x) + 6 if y == 0 else y) for x, y in BROOK]
    pts[0] = (pts[0][0], pts[0][1] - 30)
    n = len(pts)
    hw = [12 + 62 * (i / (n - 1)) ** 1.3 for i in range(n)]
    up = [(x - 0.25 * w, y - w * 0.95) for (x, y), w in zip(pts, hw)]
    dn = [(x + 0.25 * w, y + w * 0.95) for (x, y), w in zip(pts, hw)]
    d = S.smooth_path(up, closed=False) + " L" + S.smooth_path(dn[::-1], closed=False)[1:] + " Z"
    defs = S.lin_grad("vbrk", [(0, P["sea_pale"]), (1, P["sea"])], 0, 0, 0, 1)
    out = f'<defs>{defs}</defs><path d="{d}" fill="url(#vbrk)" stroke="{INK}" stroke-width="4"/>'
    rng = random.Random(4)
    for i in range(1, n - 1):
        (x, y), w = pts[i], hw[i]
        for k in (-0.3, 0.25):
            out += (f'<path d="M{f1(x - w * 0.5)},{f1(y + k * w)} q{f1(w * 0.3)},-6 {f1(w * 0.7)},0" fill="none" '
                    f'stroke="{P["foam"]}" stroke-width="3.5" stroke-linecap="round" opacity="0.85"/>')
    for i in range(n - 1):
        for side in (-1, 1):
            for _ in range(3):
                u = rng.random()
                x = M.lerp(pts[i][0], pts[i + 1][0], u)
                y = M.lerp(pts[i][1], pts[i + 1][1], u) + side * M.lerp(hw[i], hw[i + 1], u) * 1.02
                r = 5 + 9 * (y - MEADOW_Y) / 400
                out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.3)}" ry="{f1(r * 0.75)}" '
                        f'fill="{rng.choice(PR.STONE_COLS)}" stroke="{INK}" stroke-width="2.4"/>')
    for x, y, sc_ in ((1500, 1500, 0.55), (930, 1560, 0.7), (300, 1680, 0.85)):
        out += PR.reeds(x, y, sc_) if hasattr(PR, "reeds") else ""
    return out


def big_tent_svg(wave=0.0):
    """The big Philistine tent at the right edge (its pennant flies from a separate pole beside it, clear of
    Goliath's face when he walks out from behind the tent)."""
    pole = PR._flag_pole(0, -470, 0, PR.CREST_RED, "#3f7f86", "pennant", wave)
    pole = f'<g filter="url(#wobble-fine)" transform="translate({TENT_X + 330},{GY + 20}) scale({K * 1.25})">{pole}</g>'
    return doc(pole + PR.tent(TENT_X, GY + 30, TENT_S, -1, "philistine", flag=False, wave=wave)
               + PR.bush(TENT_X - 380, GY + 40, 0.8, variant=1))


def fg_rocks_svg():
    """Foreground framing at the left edge: rocks and a bush (the right edge has the tent)."""
    out = ""
    out += f'<path d="{S.blob(70, 2050, 190, 110, 0.12, 11, seed=3)}" fill="#cdbb98" stroke="{INK}" stroke-width="5"/>'
    out += f'<path d="{S.blob(250, 2100, 120, 70, 0.14, 9, seed=5)}" fill="#bfae8b" stroke="{INK}" stroke-width="5"/>'
    out += f'<path d="M-20,2010 Q60,1975 150,1995" fill="none" stroke="#e7dcc2" stroke-width="7" opacity="0.7" ' \
           f'stroke-linecap="round"/>'
    out += PR.bush(-10, 1980, 1.2, variant=0)
    return doc(S.g(out, filter="wobble"))


def fg_grass_svg(sway):
    out = ""
    for i, (x, s, v) in enumerate(((140, 1.5, 0), (420, 1.2, 2), (1240, 1.1, 0), (1980, 1.25, 1), (2700, 1.1, 0),
                                   (3300, 1.4, 2), (3700, 1.5, 0), (900, 1.0, 1), (2350, 0.95, 2))):
        out += PR.grass_tuft(x, SH + 10, s, variant=v, sway=sway * (1 if i % 2 else 0.8))
    return doc(out)


# ================================================================== the valley as layers
Z = dict(sky=0, cloud=1, back=2, hills=3, camps=4, hill_men=5, meadow=10, shadow=11, bearer_back=12, goliath=13,
         bearer=14, david=15, prop=16, tent=20, fg=21, fx=30)


def _sh(m, toff):
    return m if not toff else (lambda t: m(t + toff))


def add_valley(sc, toff=0.0):
    """The shared backdrop of the four valley scenes. toff = scene_clock(id) for seamless dissolves."""
    sc.add("sky", sky_svg(), z=Z["sky"], wc=0.45)
    for i, (_, _, _, _, v) in enumerate(CLOUDS):
        sc.add(f"cloud{i}", cloud_svg(i), z=Z["hills"] + 0.5 + 0.01 * i, wc=0.6,
               motion=_sh(M.combine(M.drift(vx=v), M.bob(3, 9 + i, 0.2 * i)), toff))
    sc.add("valley_back", valley_back_svg(), z=Z["back"], wc=0.8)
    sc.add("valley_hills", valley_hills_svg(), z=Z["hills"], wc=0.8)
    for side in ("israel", "philistine"):
        frames = [camp_svg(side, w) for w in (0.0, 0.25, 0.5, 0.75)]
        sc.add(f"camp_{side}", frames, z=Z["camps"] + (0.0 if side == "israel" else 0.01), wc=0.7,
               frame_at=lambda t, ph=(0.0 if side == "israel" else 0.4): 1.5 + 1.5 * math.sin(
                   2 * math.pi * ((t + toff) / 2.4 + ph)))
    # the meadow never overlaps the clouds, camps or hill people, so it sits right after the hills: sky, valley and
    # meadow flatten into one static picture
    sc.add("meadow", meadow_svg(), z=Z["hills"] + 0.1, wc=0.8)
    frames = [big_tent_svg(w) for w in (0.0, 0.33, 0.66)]
    sc.add("big_tent", frames, z=Z["tent"], wc=0.7,
           frame_at=lambda t: 1 + math.sin(2 * math.pi * (t + toff) / 2.2))
    sc.add("fg_rocks", fg_rocks_svg(), z=Z["fg"], wc=0.7)
    frames = [fg_grass_svg(s) for s in (-0.6, 0.0, 0.6)]
    sc.add("fg_grass", frames, z=Z["fg"] + 0.1, wc=0.6, frame_at=lambda t: 1 + math.sin(2 * math.pi * (t + toff) / 3.1))


# ================================================================== figure drawings (planted-foot rig)
def _out(D, m, ps, expr, x, y, s, facing, label, marks=True):
    inner, _ = C._figure(D, m, ps, expr, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


def goliath_rig(ps, expr, x, y, s=K, facing=-1, items="stand", bump=False, spear=True, marks=True):
    """Goliath (same design as C.goliath) in any rig pose; ``items`` picks how the spear is held (stand / stride:
    upright in the near hand, laugh / mock_point: in the far hand, shout: raised)."""
    D = C._goliath_design(items, bump, spear, True)
    return _out(D, C._GIANT, ps, expr, x, y, s, facing, "goliath-x", marks)


def goliath_walk_ps(k):
    ps = walk_pose(k, A=GOLIATH_A, lk=GOLIATH_LK)
    sw = 30 * math.cos(math.pi * (k % (2 * WALK_N)) / WALK_N)
    ps["arms"] = (("fk", -sw - 4, -sw + 10), ("fk", 62, 92))
    ps["t"] = 6
    return ps


def david_design(staff=False, bag=True):
    D = C._david_design(False, bag)
    D["mid"] = C._bag_mid if bag else None
    if staff:
        D["front"] = C._staff_near(D)
    return D


def david_rig(ps, expr, x, y, s=K, facing=1, staff=False, staff_far=False, front=None, marks=True):
    D = david_design(staff)
    if staff_far:
        D["behind"] = C._staff_far
    if front is not None:
        D["front"] = front
    return _out(D, C._BOY, ps, expr, x, y, s, facing, "david-x", marks)


def david_walk_ps(k, staff=True):
    ps = walk_pose(k, A=DAVID_A, lk=DAVID_LK)
    if staff:
        sw = 34 * math.cos(math.pi * (k % (2 * WALK_N)) / WALK_N)
        ps["arms"] = (("fk", -sw, -sw + 20), ("fk", 40, 76))
    return ps


RUN_N = 4            # drawings per running step


def run_pose(k, A, lk, lean=16):
    """Planted-foot run drawing k (RUN_N per step): long strides, high knees, pumping bent arms, leaning in."""
    ph = (k % (2 * RUN_N)) / RUN_N
    step, u = divmod(ph, 1.0)
    pdx = A * (1 - 2 * u)
    sdx = -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u))
    plant = ("ik", pdx, 1)
    swing = ("ik", sdx, 1, 64 * lk * math.sin(math.pi * u) + 8 * lk)
    sw = 62 * math.cos(math.pi * ph)
    far, near = ("fk", -sw + 6, -sw + 92), ("fk", sw + 6, sw + 92)
    drop = (18 + 8 * math.cos(2 * math.pi * u)) * lk
    return C._P(t=lean, h=-6, legs=(plant, swing) if int(step) == 0 else (swing, plant), arms=(far, near),
                hands=("fist", "fist"), drop=drop, hem=0.66, flare=-4)


def bearer_design(variant=0):
    D, _ = C._soldier_design("philistine", variant)
    D["front"] = C._big_shield_front(D)
    return D


def bearer_walk_ps(k):
    ps = walk_pose(k, A=ADULT_A)
    ps["arms"] = C.POSES["sb_walk_a"]["arms"]
    ps["hands"] = C.POSES["sb_walk_a"]["hands"]
    return ps


# ================================================================== performers
class Actor:
    """A figure on a Sprite, placed per frame by a Dynamic layer.

    sched : [(t, drawing index, hop)] pose changes (hard cuts sold by a squash-and-hop when hop > 0)
    pos   : t -> (x, y) anchor in stage px
    walk  : t -> drawing index or None (overrides sched while moving)
    rot   : t -> degrees (about the anchor, e.g. a giant's wobble), alpha : t -> 0..1
    breathe / bper / phase : idle breathing (scale y about the feet), on clock t + toff."""

    def __init__(self, sp, sched, pos, walk=None, rot=None, alpha=None, breathe=0.010, bper=3.0, phase=0.0,
                 toff=0.0, lift=None):
        self.sp, self.sched, self.pos, self.walk = sp, sorted(sched, key=lambda e: e[0]), pos, walk
        self.rot, self.alpha, self.breathe, self.bper, self.phase, self.toff = rot, alpha, breathe, bper, phase, toff
        self.lift = lift
        self._rc = {}

    def frame(self, t):
        if self.walk:
            w = self.walk(t)
            if w is not None:
                return w
        f = self.sched[0][1]
        for ts, fr, *_ in self.sched:
            if t >= ts:
                f = fr
        return f

    def hop(self, t):
        sy, dy = 1.0, 0.0
        for ts, fr, amp in self.sched:
            if amp <= 0:
                continue
            u = t - ts
            if -0.09 <= u <= 0.22:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.22, "sine")
                dy = -12 * amp * math.sin(math.pi * clamp((u + 0.01) / 0.23))
        return sy, dy

    def __call__(self, t):
        a = 1.0 if self.alpha is None else self.alpha(t)
        if a <= 0.002:
            return None
        x, y = self.pos(t)
        hs, hd = self.hop(t)
        if self.lift is not None:
            hd += self.lift(t)
        walking = self.walk is not None and self.walk(t) is not None
        b = 1 + self.breathe * math.sin(2 * math.pi * ((t + self.toff) / self.bper + self.phase))
        sy = round(hs * (1.0 if walking else b) / 0.004) * 0.004       # quantised: the resized drawings are cached
        sx = round((1 + 0.5 * (1 - hs)) / 0.004) * 0.004
        idx = self.frame(t)
        r = self.rot(t) if self.rot else 0.0
        if abs(r) < 0.05:
            return self.sp.place(idx, x, y, sx, sy, hd, a)
        out = self.sp.place(idx, x, y, sx, sy, hd, a)
        if out is None:
            return None
        im, (ox, oy) = out
        key = (idx, round(r * 4), im.size)
        if key not in self._rc:
            if len(self._rc) > 120:
                self._rc.clear()
            px, py = x - ox, y + hd - oy
            self._rc[key] = im.rotate(-round(r * 4) / 4, resample=Image.BICUBIC, center=(px, py))
        return self._rc[key], (ox, oy)


def person_sprite(left, top, right, bottom=30, seed=0, wc=1.0):
    """Canvas for one figure: room (stage px) left / above / right / below the anchor."""
    cw, ch = int(left + right), int(top + bottom)
    return Sprite(cw, ch, left, top, wc, seed)


def steps_walk(footfalls, x0, step, facing, n_draw=WALK_N, cycle=None):
    """A walk on explicit footfall times: step i runs footfalls[i] -> footfalls[i+1]; the anchor advances one step
    length per step (planted-foot drawings: the sole stays put). Returns (walk_fn(t)->k or None, pos_x(t))."""
    cycle = cycle or 2 * n_draw
    ends = list(footfalls)

    def u_of(t):
        if t < ends[0] or t >= ends[-1]:
            return None
        for i in range(len(ends) - 1):
            if ends[i] <= t < ends[i + 1]:
                return i + (t - ends[i]) / (ends[i + 1] - ends[i])
        return None

    def walk(t):
        u = u_of(t)
        if u is None:
            return None
        return int(u * n_draw) % cycle

    def px(t):
        if t < ends[0]:
            return x0
        u = u_of(t)
        if u is None:
            return x0 + facing * step * (len(ends) - 1)
        k = int(u * n_draw)
        return x0 + facing * step * k / n_draw
    return walk, px


# ================================================================== little picture-book effects
def puff_sprite(seed=0, col="#e3cf9f"):
    """Six growth stages of a dust puff (a cluster of soft round clouds), for dust_fn()."""
    sp = Sprite(420, 260, 210, 220, wc=0.6, seed=seed)
    rng = random.Random(seed)
    blobs = [(rng.uniform(-1, 1), rng.uniform(0.2, 1.0), rng.uniform(0.55, 1.0)) for _ in range(7)]
    for g in range(6):
        k = 0.35 + 0.65 * g / 5
        out = ""
        circ = [(bx * 150 * k, -by * 95 * k, (36 + 30 * rr) * (0.6 + 0.4 * k)) for bx, by, rr in blobs]
        out += "".join(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="5"/>'
                       for x, y, r in circ)
        out += "".join(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}"/>' for x, y, r in circ)
        out += "".join(f'<circle cx="{f1(x - r * 0.25)}" cy="{f1(y - r * 0.3)}" r="{f1(r * 0.45)}" fill="#f6ead0" '
                       f'opacity="0.7"/>' for x, y, r in circ[:4])
        sp.add(f'<g transform="translate({sp.ax},{sp.ay})" opacity="0.92">{out}</g>')
    return sp


class Dust:
    """Dust puffs: events (t0, x, y, scale, flip); each grows over ~0.35 s and fades by ``dur``."""

    def __init__(self, sp, events, dur=1.1):
        self.sp, self.ev, self.dur = sp, events, dur
        self._c = {}

    def __call__(self, t):
        act = [e for e in self.ev if e[0] <= t <= e[0] + self.dur]
        if not act:
            return None
        ims = []
        for t0, x, y, s, flip in act:
            u = (t - t0) / self.dur
            g = min(5, int(u * 3.2 * 6))
            a = 1.0 if u < 0.45 else 1 - (u - 0.45) / 0.55
            ss = round(s * (1 + 0.5 * u) / 0.02) * 0.02
            res = self.sp.place(g, x + flip * 90 * s * u, y - 70 * s * u ** 0.7, ss, ss * 0.95, 0, max(0.0, a))
            if res:
                ims.append(res)
        if not ims:
            return None
        if len(ims) == 1:
            return ims[0]
        x0 = min(p[0] for _, p in ims)
        y0 = min(p[1] for _, p in ims)
        x1 = max(p[0] + im.size[0] for im, p in ims)
        y1 = max(p[1] + im.size[1] for im, p in ims)
        x0i, y0i = int(math.floor(x0)), int(math.floor(y0))
        can = Image.new("RGBA", (int(x1 - x0i) + 2, int(y1 - y0i) + 2), (0, 0, 0, 0))
        for im, (px, py) in ims:
            can.alpha_composite(im, (int(round(px - x0i)), int(round(py - y0i))))
        return can, (x0i, y0i)


def twinkle(points, color=(255, 240, 190)):
    """Big four-point glints [(t0, x, y, size)] that flash (grow, spin, shrink) over 0.7 s, with tiny satellites."""
    def fx(frame, t, view):
        live = [p for p in points if p[0] <= t <= p[0] + 0.75]
        if not live:
            return frame
        from PIL import ImageDraw
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for t0, x, y, size in live:
            u = (t - t0) / 0.75
            k = math.sin(math.pi * u) ** 0.7
            ox, oy = view.to_out(x, y)
            r = size * view.scale * k
            rot = 0.8 * u
            for j, (rr, aa) in enumerate(((r, 255), (r * 0.45, 200))):
                pts = []
                for q in range(8):
                    ang = rot + q * math.pi / 4 + (math.pi / 4 if j else 0)
                    rad = rr if q % 2 == 0 else rr * 0.18
                    pts.append((ox + rad * math.cos(ang), oy + rad * math.sin(ang)))
                d.polygon(pts, fill=(*color, int(aa * k)))
            g = r * 0.35
            d.ellipse([ox - g, oy - g, ox + g, oy + g], fill=(255, 252, 235, int(230 * k)))
            for q in range(3):
                ang = 1.3 + q * 2.1 + u * 2
                sx_, sy_ = ox + 1.25 * r * math.cos(ang), oy + 1.25 * r * math.sin(ang)
                s2 = r * 0.18
                d.polygon([(sx_, sy_ - s2), (sx_ + s2 * 0.25, sy_), (sx_, sy_ + s2), (sx_ - s2 * 0.25, sy_)],
                          fill=(*color, int(220 * k)))
                d.polygon([(sx_ - s2, sy_), (sx_, sy_ - s2 * 0.25), (sx_ + s2, sy_), (sx_, sy_ + s2 * 0.25)],
                          fill=(*color, int(220 * k)))
        frame.alpha_composite(ov)
        return frame
    return fx


def light_svg(cx, top, bottom, w0, w1, uid, n=7):
    """Soft golden light falling from above onto (cx, bottom): a glow column with rays (screen blend)."""
    defs = S.lin_grad(uid + "g", [(0, "#fff4c8", 0.0), (0.2, "#fff1bc", 0.6), (0.75, "#ffe39a", 0.45), (1, "#ffe39a", 0.3)])
    defs += S.rad_grad(uid + "p", [(0, "#fff3c4", 0.9), (0.6, "#ffe7a6", 0.35), (1, "#ffe7a6", 0)])
    body = (f'<path d="M{cx - w0},{top} L{cx + w0},{top} L{cx + w1},{bottom} L{cx - w1},{bottom} Z" '
            f'fill="url(#{uid}g)" filter="url(#blur-md)"/>')
    for i in range(n):
        u = (i + 0.5) / n - 0.5
        xt, xb = cx + u * 2 * w0, cx + u * 2.2 * w1
        ww = 0.35 * w1 / n * (1.4 if i % 2 else 0.9)
        body += (f'<path d="M{f1(xt - ww * 0.4)},{top} L{f1(xt + ww * 0.4)},{top} L{f1(xb + ww)},{bottom} '
                 f'L{f1(xb - ww)},{bottom} Z" fill="#fff2c0" opacity="0.45" filter="url(#soft)"/>')
    body += f'<ellipse cx="{cx}" cy="{bottom - 20}" rx="{w1 * 1.3}" ry="{w1 * 0.28}" fill="url(#{uid}p)"/>'
    return doc(body, defs)


# ================================================================== the people on the hills
def israel_fig(sp, v, pose, expr=None, shake=0.0, facing=1):
    return sp.add(C.soldier(sp.ax, sp.ay, KH, facing, side="israel", variant=v, pose=pose, expr=expr, shake=shake))


def phil_fig(sp, v, pose, expr=None, facing=-1):
    return sp.add(C.soldier(sp.ax, sp.ay, KH, facing, side="philistine", variant=v, pose=pose, expr=expr))


def hill_sprite(seed):
    return person_sprite(150, 300, 150, 24, seed=seed)


def saul_cower(sp, shake=0.0, facing=1):
    """King Saul crouching behind a raised shield (the soldiers' cower pose) - 'he did not dare'."""
    D = C._saul_design("stand", False)
    f = C._shield_up(D, "israel")
    D["front"] = lambda st: f(st) + C._tremble_lines(st, shake)
    inner, _ = C._figure(D, C._SAUL_M, dict(C.POSES["so_cower"]), "scared", C._fsign(facing), True)
    if shake:
        inner = f'<g transform="translate({f1(3.5 * math.sin(2 * math.pi * shake))},0)">{inner}</g>'
    return sp.add(C._wrap_out(inner, sp.ax, sp.ay, KH, facing, "saul-cower"))


# ================================================================== shared cast helpers (s11 / s12 / s13)
def hill_cast(side, poses, seed0=0):
    """The soldiers on one hill: [(x, y, sprite, {name: index or [indices]})], back row first.
    poses: {name: (pose, expr)} or {name: (pose, expr, [shakes])} for a trembling flipbook."""
    men = ISRAEL_MEN if side == "israel" else PHIL_MEN
    out = []
    for j, (x, v) in enumerate(men):
        sp = hill_sprite(seed0 + j)
        d = {}
        for name, spec in poses.items():
            pose, expr = spec[0], spec[1]
            f = israel_fig if side == "israel" else phil_fig
            if len(spec) > 2:
                d[name] = [sp.add(C.soldier(sp.ax, sp.ay, KH, 1 if side == "israel" else -1, side=side, variant=v,
                                            pose=pose, expr=expr, shake=s_)) for s_ in spec[2]]
            else:
                d[name] = f(sp, v, pose, expr)
        out.append((x, ground(x) + (6 if j < 8 else -20), sp, d))
    return out


class Group:
    """Several sprite performers composited onto one canvas per frame (one dynamic layer instead of many: the
    per-layer cost of a dynamic is mostly fixed). Members are drawn in list order."""

    def __init__(self, members):
        self.members = members

    def __call__(self, t):
        ims = [r for r in (m(t) for m in self.members) if r]
        if not ims:
            return None
        if len(ims) == 1:
            return ims[0]
        x0 = int(math.floor(min(p[0] for _, p in ims)))
        y0 = int(math.floor(min(p[1] for _, p in ims)))
        x1 = int(math.ceil(max(p[0] + im.size[0] for im, p in ims))) + 1
        y1 = int(math.ceil(max(p[1] + im.size[1] for im, p in ims))) + 1
        can = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        for im, (px, py) in ims:
            can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
        return can, (x0, y0)


def add_hill_actors(sc, actors):
    """Hill people drawn back (higher on the hill) to front, as two groups (one per hill)."""
    order = sorted(range(len(actors)), key=lambda k: actors[k].pos(0)[1])
    left = [actors[k] for k in order if actors[k].pos(0)[0] < SW / 2]
    right = [actors[k] for k in order if actors[k].pos(0)[0] >= SW / 2]
    sc.add_dynamic("hill_israel", Group(left), z=Z["hill_men"])
    sc.add_dynamic("hill_philistine", Group(right), z=Z["hill_men"] + 0.01)


def saul_sprite(poses, seed=70):
    """King Saul on the hill: poses {name: (pose, expr)}; pose 'cower' = behind a raised shield."""
    sp = person_sprite(160, 330, 170, 24, seed=seed)
    d = {}
    for name, (pose, expr) in poses.items():
        if pose == "cower":
            d[name] = saul_cower(sp)
        else:
            d[name] = sp.add(C.king(sp.ax, sp.ay, KH, 1, pose=pose, attire="saul", expr=expr))
    return sp, d


TALK_STAFF = dict(C.POSES["dv_talk"], arms=(("fk", 26, 66), ("fk", 34, 86)), hands=("fist", "open"))
POINT_STAFF = dict(C.POSES["dv_point_up"], arms=(("fk", 132, 162), ("fk", 40, 76)), hands=("point", "fist"))


def david_sprite(seed=41):
    return person_sprite(200 * K, 400 * K, 280 * K, 40, seed=seed)


def giant_sprite(seed=31):
    return person_sprite(270 * K, 1180 * K, 270 * K, 40, seed=seed)


def bearer_sprite(seed=33):
    return person_sprite(200 * K, 390 * K, 200 * K, 30, seed=seed)


def dove_sprite(seed=90):
    sp = Sprite(250, 220, 125, 110, wc=0.4, seed=seed)
    for f in (1, -1):
        for w in (1.0, 0.33, -0.33, -1.0, -0.33, 0.33):
            sp.add(PR.dove(125, 116, 0.8, f, wing=w))
    return sp


class Birds:
    """Little doves circling on an ellipse (cx, cy, rx, ry) between t0 and t1 (fading in / out)."""

    def __init__(self, sp, n, cx, cy, rx, ry, t0, t1, period=4.2, phase=0.0, scale=1.0):
        self.sp, self.n, self.c, self.r, self.t0, self.t1 = sp, n, (cx, cy), (rx, ry), t0, t1
        self.period, self.phase, self.scale = period, phase, scale

    def one(self, t, i):
        a = 2 * math.pi * ((t - self.t0) / self.period + i / self.n + self.phase)
        x = self.c[0] + self.r[0] * math.cos(a) * (1 + 0.08 * i)
        y = self.c[1] + self.r[1] * math.sin(a) + 18 * math.sin(3 * a + i)
        vx = -math.sin(a)
        wing = int((t * 9 + i * 1.7)) % 6
        idx = wing + (0 if vx > 0 else 6)
        k = self.scale * (0.85 + 0.25 * (0.5 + 0.5 * math.sin(a)))     # nearer at the bottom of the circle
        al = min(M.progress(t, self.t0, self.t0 + 0.5, "sine"), 1 - M.progress(t, self.t1 - 0.5, self.t1, "sine"))
        return self.sp.place(idx, x, y, k, k, 0, al)

    def __call__(self, t):
        if t < self.t0 or t > self.t1:
            return None
        ims = [r for r in (self.one(t, i) for i in range(self.n)) if r]
        if not ims:
            return None
        x0 = int(min(p[0] for _, p in ims))
        y0 = int(min(p[1] for _, p in ims))
        x1 = int(max(p[0] + im.size[0] for im, p in ims)) + 2
        y1 = int(max(p[1] + im.size[1] for im, p in ims)) + 2
        can = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        for im, (px, py) in ims:
            can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
        return can, (x0, y0)


def shadow_sprite():
    """Contact shadows: 0 Goliath, 1 adult, 2 David, 3 Goliath lying (anchor = his feet, body toward -x)."""
    sp = Sprite(900, 120, 700, 60, wc=0.0)
    for rx, ry, cx in ((230, 26, 0), (120, 16, 0), (80, 12, 0), (360, 30, -340)):
        sp.add(f'<ellipse cx="{700 + cx * K}" cy="62" rx="{rx * K}" ry="{ry * K}" fill="{INK}" opacity="0.2" '
               f'filter="url(#soft)"/>')
    return sp


def valley_motes(toff=0.0):
    """Drifting warm light motes over the valley, on the shared clock."""
    m = FX.motes((0, 300, SW, 1800), count=26, color=(255, 246, 214), size=(3, 6), alpha=80)
    return lambda frame, t, view: m(frame, t + toff, view)


def light_motion(windows, peak=0.6):
    """Opacity of God's light: [(t_in, t_out)] with soft fades and a gentle shimmer."""
    def m(t):
        a = 0.0
        for t0, t1 in windows:
            a = max(a, min(M.progress(t, t0, t0 + 0.8, "sine"), 1 - M.progress(t, t1 - 0.9, t1, "sine")))
        return Tf(alpha=peak * a * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.3)))
    return m


# ================================================================== drawings used by s04 only
def hoop_svg(x, rim_y):
    """A ghosted picture-book basketball hoop (pole on the ground line, the rim at rim_y facing left)."""
    col, line = "#fff7e4", "#b5523b"
    st = f'stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"'
    out = f'<rect x="{x - 9}" y="{rim_y - 150}" width="18" height="{GY - rim_y + 150}" rx="8" fill="#9db4c4" {st}/>'
    out += f'<path d="M{x - 6},{rim_y - 70} L{x - 70},{rim_y - 70}" stroke="#9db4c4" stroke-width="14" ' \
           f'stroke-linecap="round"/>'
    out += f'<path d="M{x - 6},{rim_y - 70} L{x - 70},{rim_y - 70}" fill="none" {st} opacity="0.6"/>'
    bx = x - 82
    out += f'<rect x="{bx - 10}" y="{rim_y - 170}" width="24" height="190" rx="6" fill="{col}" {st}/>'
    out += f'<rect x="{bx - 4}" y="{rim_y - 92}" width="10" height="70" fill="none" stroke="{line}" stroke-width="4"/>'
    rx = bx - 70
    for k in range(6):
        u = k / 5
        xt, xb = rx - 56 + 112 * u, rx - 36 + 72 * u
        out += f'<path d="M{f1(xt)},{rim_y} L{f1(xb)},{rim_y + 82}" stroke="#f3ead8" stroke-width="4"/>'
    for k in range(3):
        yy = rim_y + 24 + 26 * k
        w = 56 - 7 * k
        out += f'<path d="M{rx - w},{yy} Q{rx},{yy + 8} {rx + w},{yy}" fill="none" stroke="#f3ead8" stroke-width="3.6"/>'
    out += f'<ellipse cx="{rx}" cy="{rim_y}" rx="60" ry="13" fill="none" stroke="{INK}" stroke-width="12"/>'
    out += f'<ellipse cx="{rx}" cy="{rim_y}" rx="60" ry="13" fill="none" stroke="#ef7d3a" stroke-width="6"/>'
    out += f'<path d="M{rx + 60},{rim_y} L{bx - 8},{rim_y}" stroke="{INK}" stroke-width="6"/>'
    return doc(S.g(f'<g opacity="0.9">{out}</g>', filter="wobble-fine"))


def ball_svg(x, y, r=34):
    st = f'stroke="{INK}" stroke-width="4"'
    return doc(S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ef8a3c" {st}/>'
                   f'<path d="M{x - r},{y} L{x + r},{y} M{x},{y - r} L{x},{y + r}" stroke="{INK}" stroke-width="3"/>'
                   f'<path d="M{x - r * 0.7},{y - r * 0.7} Q{x - r * 0.2},{y} {x - r * 0.7},{y + r * 0.7} '
                   f'M{x + r * 0.7},{y - r * 0.7} Q{x + r * 0.2},{y} {x + r * 0.7},{y + r * 0.7}" fill="none" '
                   f'stroke="{INK}" stroke-width="3"/>'
                   f'<circle cx="{x - r * 0.4}" cy="{y - r * 0.45}" r="{r * 0.18}" fill="#ffd9a8"/>',
                   filter="wobble-fine"))


def log_svg(x, y0, y1, w=64):
    """A ghosted log standing beside the spear shaft ('as thick as a big log')."""
    bark, wood = "#9a6a43", "#e9c48f"
    st = f'stroke="{INK}" stroke-width="4" stroke-linejoin="round"'
    out = f'<rect x="{x - w / 2}" y="{y0}" width="{w}" height="{y1 - y0}" rx="10" fill="{bark}" {st}/>'
    for k in range(7):
        yy = y0 + 40 + (y1 - y0 - 70) * k / 6
        out += f'<path d="M{x - w * 0.3},{yy} q{w * 0.25},{-14} {w * 0.55},{-4}" fill="none" stroke="#6f4a2c" ' \
               f'stroke-width="3.5" stroke-linecap="round"/>'
    out += f'<ellipse cx="{x}" cy="{y0 + 4}" rx="{w / 2}" ry="{w * 0.2}" fill="{wood}" {st}/>'
    out += f'<ellipse cx="{x}" cy="{y0 + 4}" rx="{w * 0.3}" ry="{w * 0.11}" fill="none" stroke="#b98a55" stroke-width="3"/>'
    out += f'<path d="M{x + w / 2 - 4},{(y0 + y1) / 2} q22,-18 30,-40 q-24,6 -30,22" fill="#7fae4d" {st}/>'
    return doc(S.g(f'<g opacity="0.92">{out}</g>', filter="wobble-fine"))


def sound_arc_svg(x, y, r, facing=-1, sw=26):
    """A comic sound-wave arc ')' opening away from the speaker (centre x, y, radius r)."""
    a = math.radians(42)
    sx = facing
    p0 = (x + sx * r * math.cos(a), y - r * math.sin(a))
    p1 = (x + sx * r * math.cos(a), y + r * math.sin(a))
    sweep = 0 if facing < 0 else 1
    d = f"M{f1(p0[0])},{f1(p0[1])} A{r},{r} 0 0 {sweep} {f1(p1[0])},{f1(p1[1])}"
    out = ""
    for k, rr in enumerate((r, r * 1.45, r * 1.9)):
        p0 = (x + sx * rr * math.cos(a), y - rr * math.sin(a))
        p1 = (x + sx * rr * math.cos(a), y + rr * math.sin(a))
        dd = f"M{f1(p0[0])},{f1(p0[1])} A{rr},{rr} 0 0 {sweep} {f1(p1[0])},{f1(p1[1])}"
        w = sw - 5 * k
        out += (f'<path d="{dd}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
                f'<path d="{dd}" fill="none" stroke="#fff4dc" stroke-width="{w - 9}" stroke-linecap="round"/>')
    return doc(S.g(out,
                   filter="wobble-fine"))


def pebbles_svg(pts, seed):
    rng = random.Random(seed)
    out = ""
    for x, y, r in pts:
        out += (f'<path d="{S.blob(x, y - r * 0.5, r, r * 0.6, 0.15, 8, seed=rng.randint(0, 99))}" '
                f'fill="{rng.choice(["#d8c9a8", "#c9b893", "#e2d6bb"])}" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(out, filter="wobble-fine"))


def arc_motion(i, n, windows, ox, oy, period=0.42, travel=1.5, dist=900, facing=-1):
    """Sound arc i of n: emitted every period*n s (staggered) during each (a, b) window, flying ``dist`` px
    toward ``facing`` while growing and fading over ``travel`` s."""
    def m(t):
        best = None
        for a, b in windows:
            if t < a:
                continue
            k = math.floor((t - a) / (period * n) - i / n)
            e = a + period * (n * k + i)
            if e < a:
                continue
            if e > b:
                kk = math.floor((b - a) / (period * n) - i / n)
                e = a + period * (n * kk + i)
                if e < a:
                    continue
            u = (t - e) / travel
            if 0 <= u <= 1:
                best = u
        if best is None:
            return Tf(alpha=0.0)
        u = best
        s = 0.55 + 1.6 * u
        return Tf(dx=facing * dist * (1 - (1 - u) ** 1.6), sx=s, sy=s, px=ox, py=oy,
                  alpha=min(1.0, u / 0.08) * (1 - u) ** 1.2)
    return m


# ================================================================== s04 build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]
    add_valley(sc)

    # ---------------------------------------------------------------- beats
    c_dong = L0.chunks[-1]
    beats = onsets(ctx, 0, c_dong.start - 0.15, c_dong.end, 3)          # 咚！咚！咚！
    t_out = phrase_t(L0, "走出来", 0.6)                                  # "走出来一个人"
    t_name = L1.start
    t_tall = phrase_t(L1, "他好高", 0.4)
    t_hoop = phrase_t(L1, "篮球架", 0.75) - 0.15
    t_hoop_out = min(L1.end + 0.45, L2.start - 0.1)
    t_helm = phrase_t(L2, "铜头盔", 0.1) - 0.1
    t_armr = phrase_t(L2, "穿着", 0.35)
    t_spear = phrase_t(L2, "手里的枪", 0.6)
    t_log = phrase_t(L2, "大木头", 0.85) - 0.2
    t_log_out = L2.end + 0.5
    lc = L3.chunks
    t_sh1 = L3.start - 0.25                    # spear up: shout
    t_pt = lc[1].start - 0.1 if len(lc) > 1 else L3.start + 2.0          # "派一个人出来跟我打！"
    t_smug = lc[2].start - 0.1 if len(lc) > 2 else L3.start + 4.6        # "他要是赢了…"
    t_sh2 = lc[3].start - 0.15 if len(lc) > 3 else L3.start + 9.3        # "要是我赢了…"
    t_laugh = L3.end + 0.05
    t_stand = L4.start + 1.2
    t_fear = L4.start + 0.35                    # "以色列人听了，吓得腿都软了"
    t_saul = phrase_t(L4, "连扫罗王", 0.6) + 0.15
    t_saul2 = t_saul + 0.75

    # ---------------------------------------------------------------- the shield-bearer and Goliath walk out
    n_b = 11
    b_t0, b_t1 = L0.start + 0.45, beats[1] + 0.25
    b_ff = [b_t0 + (b_t1 - b_t0) * i / n_b for i in range(n_b + 1)]
    step_b = 2 * ADULT_A * K
    b_x0 = XB + n_b * step_b
    b_walk, b_px = steps_walk(b_ff, b_x0, step_b, -1)
    g_ff = [t_out - 1.45, t_out - 0.75, t_out - 0.05, beats[0], beats[1], beats[2]]
    g_ff = [g_ff[0] - 0.7] + g_ff
    n_g = len(g_ff) - 1
    g_x0 = XG + n_g * STEP_G
    g_walk, g_px = steps_walk(g_ff, g_x0, STEP_G, -1)

    # Goliath sprite: walk drawings + poses
    gsp = giant_sprite()
    GW = [gsp.add(goliath_rig(goliath_walk_ps(k), "angry", gsp.ax, gsp.ay, items="stride_a"))
          for k in range(2 * WALK_N)]
    gi = dict(stand=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="stand")),
              stand_sneer=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="stand")),
              shout=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="shout")),
              point=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="mock_point", expr="roar")),
              smug=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="laugh", expr="sneer")),
              laugh=gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, pose="laugh")))
    g_sched = [(0, GW[0], 0), (beats[2], gi["stand"], 0.0), (t_name + 0.2, gi["stand_sneer"], 0.6),
               (t_sh1, gi["shout"], 1.0), (t_pt, gi["point"], 0.8), (t_smug, gi["smug"], 0.7),
               (t_sh2, gi["shout"], 1.0), (t_laugh, gi["laugh"], 0.8), (t_stand + 1.0, gi["stand"], 0.6)]

    def g_lift(t):          # the heavy body sinks a little on each footfall
        d = 0.0
        for f in g_ff[1:]:
            u = t - f
            if 0 <= u < 0.3:
                d = max(d, 7 * math.sin(math.pi * u / 0.3))
        return d
    g_act = Actor(gsp, g_sched, lambda t: (g_px(t), GY), walk=g_walk, breathe=0.008, bper=3.6, lift=g_lift)
    sc.add_dynamic("goliath", g_act, z=Z["goliath"])
    # the champion stamps: squash on the last stomp
    g_act.sched.append((beats[2] + 0.001, gi["stand"], 0.9))
    g_act.sched.sort(key=lambda e: e[0])

    bsp = bearer_sprite()
    BW = [bsp.add(_out(bearer_design(0), C._ADULT, bearer_walk_ps(k), "neutral", bsp.ax, bsp.ay, K, -1, "sb"))
          for k in range(2 * WALK_N)]
    b_stand = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand"))
    b_proud = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand", expr="smug"))
    sc.add_dynamic("bearer", Actor(bsp, [(0, BW[0], 0), (b_ff[-1], b_stand, 0.4), (t_smug + 0.3, b_proud, 0.4)],
                                   lambda t: (b_px(t), GY), walk=b_walk, breathe=0.012, bper=2.9, phase=0.3),
                   z=Z["bearer_back"])

    # contact shadows (follow the walkers)
    shadow = shadow_sprite()
    sc.add_dynamic("g_shadow", lambda t: shadow.place(0, g_px(t), GY, 1, 1, 0, 1.0), z=Z["shadow"])
    sc.add_dynamic("b_shadow", lambda t: shadow.place(1, b_px(t), GY, 1, 1, 0, 1.0), z=Z["shadow"] + 0.01)

    # ---------------------------------------------------------------- dust on the footfalls, pebbles hop
    dsp = puff_sprite(3)
    dev = []
    for i, f in enumerate(g_ff[1:]):
        x = g_x0 - STEP_G * (i + 1) - GOLIATH_A * K + 10
        big = f in beats
        dev.append((f, x, GY + 8, 0.95 if big else 0.55, -1))
        if big:
            dev.append((f + 0.03, x + 120, GY + 10, 0.75, 1))
    sc.add_dynamic("dust", Dust(dsp, dev, dur=1.2), z=Z["goliath"] + 0.5)

    def hop_fn(amp, delay):
        def m(t):
            d = 0.0
            for b in beats:
                u = t - b - delay
                if 0 <= u < 0.42:
                    d = min(d, -amp * abs(math.sin(math.pi * u / 0.42 * 1.0)) * (1 - u / 0.42) ** 0.5)
            return Tf(dy=d)
        return m
    peb = [[(1950, 1985, 14), (1990, 1992, 10), (2030, 1984, 12)], [(1180, 2010, 16), (1215, 2016, 11)],
           [(2560, 2020, 15), (2600, 2025, 10), (2520, 2024, 9)], [(1600, 1960, 10), (1630, 1962, 8)]]
    for i, pts in enumerate(peb):
        sc.add(f"pebbles{i}", pebbles_svg(pts, 50 + i), z=Z["prop"] + 0.1 * i, wc=0.4,
               motion=hop_fn(26 + 8 * (i % 2), 0.02 * i))

    # ---------------------------------------------------------------- the people on the hills
    Hs = []
    i_cower = {}
    for j, (x, v) in enumerate(ISRAEL_MEN):
        sp = hill_sprite(60 + j)
        d = dict(stand=israel_fig(sp, v, "stand"), worry=israel_fig(sp, v, "stand", "worried"),
                 cower=[israel_fig(sp, v, "cower", shake=s_) for s_ in (0.0, 0.25, 0.5, 0.75)])
        y = ground(x) + (6 if j < 8 else -20)
        t_c = t_fear + 0.12 * (j % 4) + 0.05 * j
        sched = [(0, d["stand"], 0), (t_sh2 + 0.6 + 0.15 * (j % 3), d["worry"], 0.0), (t_c, d["cower"][0], 0.8)]

        def tremble(t, t_c=t_c, d=d, j=j):
            if t < t_c + 0.22:
                return None
            return d["cower"][int((t * 11 + j * 0.37)) % 4]
        Hs.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), walk=tremble, breathe=0.012, bper=2.6 + 0.2 * j,
                        phase=0.13 * j))
        i_cower[j] = t_c
    # King Saul at the front of his men: worried, then he hops back and hides behind a shield too
    ssp = person_sprite(160, 330, 170, 24, seed=70)
    s_st = ssp.add(C.king(ssp.ax, ssp.ay, KH, 1, pose="stand", attire="saul", expr="worried"))
    s_sc = ssp.add(C.king(ssp.ax, ssp.ay, KH, 1, pose="stand", attire="saul", expr="scared"))
    s_cw = [saul_cower(ssp, s_) for s_ in (0.0, 0.25, 0.5, 0.75)]
    sx0, sx1 = SAUL_X, SAUL_X - 110

    def saul_pos(t):
        u = M.progress(t, t_saul2 - 0.05, t_saul2 + 0.3, "inout")
        x = M.lerp(sx0, sx1, u)
        return x, ground(x) + 6 - 26 * math.sin(math.pi * u)

    def saul_tr(t):
        if t < t_saul2 + 0.3:
            return None
        return s_cw[int(t * 11 + 0.5) % 4]
    Hs.append(Actor(ssp, [(0, s_st, 0), (t_saul, s_sc, 0.9), (t_saul2, s_cw[0], 0.0)], saul_pos, walk=saul_tr,
                    breathe=0.012, bper=3.1))
    # the Philistines: proud, then they cheer their champion on
    for j, (x, v) in enumerate(PHIL_MEN):
        sp = hill_sprite(80 + j)
        d = dict(stand=phil_fig(sp, v, "stand"), cheer=phil_fig(sp, v, "cheer", "happy"),
                 point=phil_fig(sp, v, "point", "happy"))
        y = ground(x) + (6 if j < 8 else -20)
        tc = t_sh2 + 1.0 + 0.17 * j
        sched = [(0, d["stand"], 0), (t_pt + 0.6 + 0.2 * j, d["point"] if j % 2 else d["stand"], 0.5 * (j % 2)),
                 (tc, d["cheer"], 0.8), (t_laugh + 1.6 + 0.1 * j, d["stand"], 0.5)]

        def jump(t, tc=tc, j=j):
            if tc + 0.25 < t < t_laugh + 1.5:
                return -14 * abs(math.sin(math.pi * (t - tc) / (0.45 + 0.03 * j)))
            return 0.0
        Hs.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), breathe=0.012, bper=2.7 + 0.2 * j, phase=0.17 * j,
                        lift=jump))
    add_hill_actors(sc, Hs)

    # ---------------------------------------------------------------- the basketball hoop and the log
    hx = XG + 300
    rim = GY - round(650 * K)
    pop = lambda t, a, b, px, py: _pop(t, a, b, px, py)       # noqa: E731
    sc.add("hoop", hoop_svg(hx, rim), z=Z["prop"] + 1, wc=0.3, motion=lambda t: pop(t, t_hoop, t_hoop_out, hx, GY))
    bx0, by0 = hx - 260, GY - 34

    def ball_m(t):
        u = t - t_hoop - 0.35
        if u < 0 or t > t_hoop_out + 0.2:
            return Tf(alpha=0.0)
        hgt = 150 * abs(math.cos(math.pi * u / 0.55)) * math.exp(-u * 0.9)
        return Tf(dx=-30 * min(u, 1.5), dy=-hgt, alpha=1 - M.progress(t, t_hoop_out - 0.1, t_hoop_out + 0.15))
    sc.add("ball", ball_svg(bx0, by0), z=Z["prop"] + 1.1, wc=0.3, motion=ball_m)
    sh_pt = C.body_points(C.goliath, XG, GY, K, -1, pose="stand")["hands"][1]
    lx = sh_pt[0] - 110
    sc.add("log", log_svg(lx, GY - 980, GY - 220, 80), z=Z["prop"] + 1, wc=0.3,
           motion=lambda t: pop(t, t_log, t_log_out, lx, GY - 170))

    # ---------------------------------------------------------------- the shout: sound arcs across the valley
    head = C.body_points(C.goliath, XG, GY, K, -1, pose="shout")["head"]
    mo = (head[0] - 70, head[1] + 40)
    win = [(lc[0].start, lc[0].end), (t_sh2 + 0.15, L3.end - 0.1)]
    if len(lc) > 1:
        win.insert(1, (lc[1].start + 0.1, lc[1].end - 0.2))
    for i in range(3):
        sc.add(f"arc{i}", sound_arc_svg(mo[0], mo[1], 60), z=Z["fx"] - 1, wc=0.2,
               motion=arc_motion(i, 3, win, mo[0], mo[1], period=0.55, travel=1.9, dist=1600))

    # ---------------------------------------------------------------- camera
    wide = Cam(1900, 1110, 3500)
    right = Cam(2330, 1200, 2900)
    feet = Cam(2930, 1660, 1500)
    top = Cam(2930, 1090, 1500)
    hoopc = Cam(2950, 1330, 1700)
    helm = Cam(2930, 1180, 1450)
    armr = Cam(2910, 1470, 1450)
    spr = Cam(2860, 1130, 1500)
    logc = Cam(2870, 1300, 1800)
    shout = Cam(2150, 1150, 3200)
    ptc = Cam(2560, 1330, 2300)
    sh2 = Cam(2300, 1200, 2800)
    israel = Cam(720, 800, 1440)
    keys = [(0, wide), (L0.start + 0.2, wide), (beats[0] - 0.4, right), (beats[2] + 0.5, right),
            (t_name + 0.1, right), (t_tall - 0.05, feet), (t_tall + 0.15, feet),
            (t_hoop - 0.05, top), (t_hoop + 0.9, hoopc), (t_hoop_out + 0.1, hoopc), (t_helm + 0.1, helm),
            (t_armr - 0.6, helm), (t_armr + 0.7, armr), (t_spear - 0.5, armr), (t_spear + 0.8, spr),
            (t_log, logc), (L2.end - 0.3, logc), (L3.start + 0.7, shout), (t_pt - 0.1, shout),
            (t_pt + 1.2, ptc), (t_sh2 - 0.4, ptc), (t_sh2 + 0.9, sh2), (L3.end - 0.3, sh2),
            (L4.start - 0.2, wide), (t_fear + 2.0, israel), (T, Cam(730, 810, 1400))]
    cam = M.cam_keys(keys, "sine")
    for k_, b in enumerate(beats):
        cam = M.cam_shake(cam, amp=14 if k_ == 2 else 10, t0=b, t1=b + 0.38, freq=16, seed=3 + k_)
    for f in g_ff[1:4]:
        cam = M.cam_shake(cam, amp=4, t0=f, t1=f + 0.3, freq=14, seed=11)
    cam = M.cam_shake(cam, amp=3, t0=t_sh2 + 0.2, t1=t_sh2 + 1.6, freq=10, seed=7)
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    hp = C.body_points(C.goliath, XG, GY, K, -1, pose="stand")
    sc.fx = [twinkle([(t_helm + 0.25, hp["head_top"][0] - 20, hp["head_top"][1] + 40, 60),
                      (t_armr + 0.45, XG - 40, GY - 520, 80), (t_armr + 0.7, XG + 60, GY - 430, 50),
                      (t_spear + 0.5, sh_pt[0] + 14, GY - 1150, 80), (t_spear + 0.75, sh_pt[0], GY - 800, 50)]),
             valley_motes()]

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("crowd", 0, dur=T, gain_db=-24, fade_in=0.8, fade_out=0.8)
    sc.sfx("horn", L0.start + 0.3, gain_db=-16, pan=0.5)
    sc.sfx("footsteps", b_ff[2], dur=b_ff[-1] - b_ff[2], gain_db=-20, pan=0.4)
    for f in g_ff[1:]:
        big = f in beats
        sc.sfx("thud", f, gain_db=-5 if big else -13, pan=0.25, duck_db=-2 if big else None)
    sc.sfx("pop", t_hoop + 0.02, gain_db=-12)
    sc.sfx("pop", t_hoop_out, gain_db=-16)
    for tt in (t_helm + 0.25, t_armr + 0.45, t_spear + 0.5):
        sc.sfx("sparkle", tt, gain_db=-15)
    sc.sfx("pop", t_log + 0.02, gain_db=-13)
    sc.sfx("cloth", t_sh1, gain_db=-14, pan=0.3)
    sc.sfx("cheer", t_sh2 + 1.0, dur=L3.end - t_sh2 + 0.5, gain_db=-20, pan=0.6, fade_in=0.4, fade_out=0.8)
    sc.sfx("cloth", t_fear + 0.1, gain_db=-14, pan=-0.5)
    sc.sfx("cloth", t_saul2, gain_db=-13, pan=-0.5)
    sc.sfx("pop", t_saul2 + 0.05, gain_db=-16, pan=-0.5)
    preload()
    return sc


def _pop(t, t_in, t_out, px, py):
    """Pop-in with overshoot and pop-out (a quick puff up and vanish), scaled about (px, py)."""
    if t < t_in or t > t_out + 0.2:
        return Tf(alpha=0.0)
    if t < t_out:
        k = M.ease("back")(clamp((t - t_in) / 0.35))
        return Tf(sx=max(0.01, k), sy=max(0.01, k), px=px, py=py)
    u = (t - t_out) / 0.2
    return Tf(sx=1 + 0.12 * u, sy=1 + 0.12 * u, alpha=1 - u, px=px, py=py)
