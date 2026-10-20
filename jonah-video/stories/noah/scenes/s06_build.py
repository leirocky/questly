"""Scene 6 — Noah and his sons build the ark (Genesis 6:14-16, 22).

"挪亚和儿子们开始造方舟。锯木头，嘎吱嘎吱！钉钉子，叮叮当当！" / "方舟好长好长，比一个足球场还要长！它有三层，旁边开一个门，上面
开一个窗户。" / "他们造啊造，造啊造，一天又一天……" / "终于，方舟造好了！"

One 2800 x 1575 stage: a sunny building yard on a wide meadow below the hills. The ark (props.ark, scale 0.72) stands
in the middle on its cradle blocks and grows through the scene; Noah and his three sons work beside it at the SAME
scale on one ground line: Noah saws at a sawhorse by the log pile (left), Shem and Ham hammer nails into the ribs and
planks in front of the hull, Japheth saws at a second sawhorse (right). Pitch bucket, nails, plank piles around.

  line 0  "挪亚和儿子们开始造方舟。"  the keel grows on its blocks and the ribs rise; everyone is at work.
          "锯木头，嘎吱嘎吱！"        close on Noah: a big saw stroke on each 嘎吱 with a sawdust puff and a 嘎吱 word.
          "钉钉子，叮叮当当！"        close on Shem and Ham: one strike per 叮 / 叮 / 当 / 当, a gold clang star and the
                                       sound word at the nail each time.
  line 1  "方舟好长好长，比一个足球场还要长！"  a picture-book panel opens in the sky: a football pitch with the finished
          ark drawn above it at the true ratio (ark 137 m : pitch 100 m, props docstring formula) and length arrows -
          the ark's arrow sticks out past the pitch on both ends.
          "它有三层，"                the three decks light up on the panel's ark, counted 1, 2, 3;
          "旁边开一个门，"            the side door glows; "上面开一个窗户。" the high window glows. Panel closes.
  line 2  "他们造啊造，……一天又一天……"  days rush by: the sun and the moon arc over the sky, the light goes from day
          to night and back, a day counter fills up, the workers work faster and the ark grows to its roof.
  line 3  "终于，方舟造好了！"        at the last dawn the whole family stands by the finished ark (door, window
          shutters and ramp appear), they cheer, sparkles; calm last second.
Workers are sprites with phase flipbooks (saw 4 phases, hammer 4 phases); poses change by squash-and-hop.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.daniel.scenes.s05_prays import clamp
from stories.david.scenes.s08_saul import Actor, clamp_cam, pop_tf, pt, sparkle_dyn, sprite, voice_segs
from stories.noah.scenes.s04_noah import fam, flowers, glow_svg, grass_strokes

INK = P["ink"]
SW, SH = 2800, 1575
GY = 1240
A = 0.72                       # ark AND person scale
ARK_X = 1500
NOAH_X, SHEM_X, HAM_X, JAP_X = 330, 1170, 1840, 2520
GROUP_X = 1060                 # the family at the end (noah_family anchor)


def f1(v):
    return f"{v:.1f}"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def char_beats(ctx, i, phrase, offsets, snap=0.18):
    """Times of characters (offsets inside phrase) of line i, estimated by character position inside the subtitle
    chunk, each snapped to the start of a voiced burst of the take if one starts within ``snap`` s."""
    line = ctx.lines[i]
    segs = voice_segs(ctx, i) or []
    for c in line.chunks:
        j = c.text.find(phrase)
        if j >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、…")))
            out = []
            for o in offsets:
                est = c.start + (c.end - c.start) * (j + o) / n
                near = [s_[0] for s_ in segs if abs(s_[0] - est) <= snap]
                out.append(min(near, key=lambda v: abs(v - est)) if near else est)
            for k in range(1, len(out)):
                out[k] = max(out[k], out[k - 1] + 0.18)
            return out
    return [line.start + 0.3 * k for k in range(len(offsets))]


# ================================================================== backdrop
def sky_svg(sun=True):
    defs = (S.lin_grad("s6sky", [(0, "#8cc8e2"), (0.55, "#c4e4ea"), (1, "#f7ecca")])
            + S.rad_grad("s6sun", [(0, "#fff8dc", 0.9), (0.4, "#fdeec6", 0.4), (1, "#fdeec6", 0)]))
    body = S.rect_bg("url(#s6sky)", SW, SH)
    return doc(body, defs)


def sun_svg(x, y, r=86, uid="s6s"):
    defs = S.rad_grad(uid, [(0, "#fff8dc", 0.9), (0.4, "#fdeec6", 0.4), (1, "#fdeec6", 0)])
    body = f'<circle cx="{x}" cy="{y}" r="{r * 5}" fill="url(#{uid})"/>'
    body += S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
                f'stroke-width="5"/><circle cx="{x - r * 0.3}" cy="{y - r * 0.3}" r="{r * 0.3}" fill="#fff4cc" '
                f'opacity="0.7"/>', filter="wobble-fine")
    return doc(body, defs)


def moon_svg(x, y, r=60):
    defs = S.rad_grad("s6mg", [(0, "#f4f2e0", 0.7), (1, "#f4f2e0", 0)])
    d = (f"M{x + r * 0.3},{y - r} A{r},{r} 0 1 0 {x + r * 0.3},{y + r} A{r * 0.75},{r * 0.75} 0 1 1 "
         f"{x + r * 0.3},{y - r} Z")
    body = f'<circle cx="{x}" cy="{y}" r="{r * 3}" fill="url(#s6mg)"/>'
    body += S.g(f'<path d="{d}" fill="#f8f0c8" stroke="{S.mix("#c9b46a", INK, 0.3)}" stroke-width="4"/>',
                filter="wobble-fine")
    return doc(body, defs)


def far_svg():
    ridge = S.mix("#9fb8c8", "#ece6d6", 0.35)
    body = S.path(S.hill(-200, 1400, 900, 260, seed=7, bumps=3, bottom=1300), fill=ridge, sw=2.6)
    body += S.path(S.hill(1100, 3000, 890, 230, seed=3, bumps=3, bottom=1300), fill=S.mix(ridge, "#c9dcc0", 0.3),
                   sw=2.6)
    out = S.g(body, filter="wobble")
    out += S.g(S.path(S.hill(-200, 3000, 950, 90, seed=5, bumps=5, bottom=1400), fill="#bcd096", sw=2.6),
               filter="wobble")
    rng = random.Random(6)
    far = ""
    for i in range(12):
        far += PR.olive_tree(rng.uniform(0, SW), 955 + rng.uniform(-20, 20), rng.uniform(0.13, 0.19), seed=i)
    for i in range(3):        # Noah's village on the far hill
        far += PR.house(2250 + i * 120, 905 + 8 * i, 0.15, variant=i, facing=1)
    out += PR._haze(far, "#dfeaf0", 0.45, 0.4)
    return doc(out)


def meadow_svg():
    defs = S.lin_grad("s6m", [(0, "#a9cc68"), (0.5, "#94ba58"), (1, "#7fa64a")])
    pts = [(-60, 1000), (500, 985), (1100, 1000), (1700, 990), (2300, 1000), (2860, 985)]
    d = S.smooth_path(pts, closed=False) + f" L2860,{SH + 40} L-60,{SH + 40} Z"
    out = f'<path d="{d}" fill="url(#s6m)" stroke="{INK}" stroke-width="5"/>'
    rng = random.Random(3)
    out += grass_strokes(rng, 70, 0, SW, 1010, SH, P["grass_dark"])
    # the trampled sandy yard under the ark and the workers
    out += f'<ellipse cx="{ARK_X - 80}" cy="{GY + 20}" rx="1450" ry="120" fill="#dcc690" opacity="0.75"/>'
    out += f'<ellipse cx="{ARK_X - 80}" cy="{GY + 10}" rx="1250" ry="70" fill="#e6d4a4" opacity="0.6"/>'
    # wood shavings scattered on the yard
    for _ in range(70):
        x, y = rng.uniform(150, 2700), rng.uniform(GY - 30, GY + 110)
        out += (f'<path d="M{f1(x)},{f1(y)} q6,-6 12,0" fill="none" stroke="#c99a5c" stroke-width="3" '
                f'stroke-linecap="round" opacity="0.8"/>')
    out += flowers(rng, 24, 0, SW, 1020, 1120, 1.0)
    return doc(S.g(out, filter="wobble"), defs)


def yard_svg():
    """Timber piles, the nail box, the pitch bucket, a few planks: static, behind the workers."""
    out = PR.timber_pile(110, GY - 20, A * 1.05, 1, kind="logs")
    out += PR.timber_pile(2690, GY - 18, A, -1, kind="planks")
    out += PR.pitch_bucket(2140, GY + 6, A)
    out += PR.nails(ARK_X - 30, GY + 30, A)
    out += PR.plank(720, GY + 40, A, rot=4, length=300, seed=2)
    out += PR.plank(2280, GY + 50, A, rot=-3, length=260, seed=5)
    return doc(out)


def fg_svg(sway=0.0):
    out = ""
    for x, y, s, v in ((60, SH + 20, 1.6, 2), (420, SH + 40, 1.3, 0), (1480, SH + 40, 1.4, 2), (2150, SH + 30, 1.5, 0),
                       (2720, SH + 30, 1.4, 2)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sway)
    return doc(out)


# ================================================================== little overlays
def word_svg(x, y, s, size=64, col="#e07a3c"):
    return doc(S.text(x, y, s, size=size, fill="#fff4dc",
                      extra=f'stroke="{col}" stroke-width="10" stroke-linejoin="round" paint-order="stroke"'))


def clang_svg(cx, cy, s=1.0):
    pts = []
    for i in range(16):
        r = (40 if i % 2 == 0 else 15) * s
        a = math.radians(-90 + 22.5 * i)
        pts.append(f"{f1(cx + r * math.cos(a))},{f1(cy + r * math.sin(a))}")
    return doc(S.g(f'<path d="M{" L".join(pts)} Z" fill="#fff1b0" stroke="{S.mix(P["sun_hot"], INK, 0.4)}" '
                   f'stroke-width="3.5" stroke-linejoin="round"/>', filter="wobble-fine"))


# the comparison panel (line 1)
PANEL = (880, 24, 1920, 742)   # x0, y0, x1, y1
PC = (PANEL[0] + PANEL[2]) / 2
PITCH_S = 0.55
PITCH_Y = 690
PARK_S = PITCH_S * 1.37 * PR.FOOTBALL_LEN / PR.ARK_LEN      # true ratio: ark 137 m, pitch 100 m
PARK_Y = 455                   # keel of the panel ark


def panel_bg_svg():
    x0, y0, x1, y1 = PANEL
    defs = S.lin_grad("s6pb", [(0, "#d9eef3"), (0.65, "#eef5e8"), (1, "#f4ecd2")])
    out = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="60" fill="url(#s6pb)" stroke="{INK}" '
           f'stroke-width="7"/><rect x="{x0 + 14}" y="{y0 + 14}" width="{x1 - x0 - 28}" height="{y1 - y0 - 28}" rx="48" '
           f'fill="none" stroke="#e8c062" stroke-width="5"/>')
    return doc(S.g(out, filter="wobble-fine"), defs)


def panel_pitch_svg():
    return doc(PR.football_field(PC, PITCH_Y, PITCH_S))


def panel_ark_svg():
    return doc(PR.ark(PC, PARK_Y, PARK_S, ramp=False))


def arrow_d(xa, xb, y):
    return (f"M{f1(xa)},{f1(y)} L{f1(xb)},{f1(y)} M{f1(xa + 22)},{f1(y - 16)} L{f1(xa)},{f1(y)} L{f1(xa + 22)},{f1(y + 16)} "
            f"M{f1(xb - 22)},{f1(y - 16)} L{f1(xb)},{f1(y)} L{f1(xb - 22)},{f1(y + 16)}")


def pitch_arrow_svg():
    half = PR.FOOTBALL_LEN * PITCH_S / 2
    y = PITCH_Y + 26
    col = "#3f7f3a"
    d = arrow_d(PC - half, PC + half, y)
    guides = (f'<path d="M{f1(PC - half)},{PITCH_Y - 10} L{f1(PC - half)},{PARK_Y - 330} M{f1(PC + half)},{PITCH_Y - 10} '
              f'L{f1(PC + half)},{PARK_Y - 330}" stroke="{col}" stroke-width="4" stroke-dasharray="12 12" opacity="0.8"/>')
    return doc(guides + f'<path d="{d}" fill="none" stroke="#fffaf0" stroke-width="13" stroke-linecap="round" '
               f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="6" '
               f'stroke-linecap="round" stroke-linejoin="round"/>')


def ark_arrow_svg():
    half = PR.ARK_LEN * PARK_S / 2
    y = PARK_Y + 42
    col = "#c8622f"
    d = arrow_d(PC - half, PC + half, y)
    return doc(f'<path d="{d}" fill="none" stroke="#fffaf0" stroke-width="15" stroke-linecap="round" '
               f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="7" '
               f'stroke-linecap="round" stroke-linejoin="round"/>')


def ark_local(lx, ly):
    return PC + lx * PARK_S, PARK_Y + ly * PARK_S


DECKS = ((-300, 0, 0.62), (-605, -300, 0.93), (-868, -605, 0.62))   # local y range and width share of each deck


def deck_svg(i):
    """Deck i (0 bottom .. 2 cabin) glowing on the panel ark, with its number badge."""
    y0, y1, wk = DECKS[i]
    half = PR.ARK_LEN / 2 * wk
    xa, ya = ark_local(-half, y1 + 18)
    xb, yb = ark_local(half, y0 - 18)
    cols = ("#f6c34a", "#f08a5d", "#7cc0d8")
    out = (f'<rect x="{f1(xa)}" y="{f1(ya)}" width="{f1(xb - xa)}" height="{f1(yb - ya)}" rx="18" fill="{cols[i]}" '
           f'fill-opacity="0.35" stroke="{cols[i]}" stroke-width="7"/>')
    bx, by = xa - 30, (ya + yb) / 2
    out += (f'<circle cx="{f1(bx)}" cy="{f1(by)}" r="34" fill="#fff6dc" stroke="{S.mix(cols[i], INK, 0.4)}" '
            f'stroke-width="5"/>')
    return doc(S.g(out, filter="wobble-fine") + S.text(bx, by + 17, str(i + 1), size=46,
                                                      fill=S.mix(cols[i], INK, 0.55)))


def ring_svg(box, col="#ffd65a"):
    x0, t0, x1, b0 = box
    xa, ya = ark_local(x0, t0)
    xb, yb = ark_local(x1, b0)
    pad = 14
    return doc(f'<rect x="{f1(xa - pad)}" y="{f1(ya - pad)}" width="{f1(xb - xa + 2 * pad)}" height="{f1(yb - ya + 2 * pad)}" '
               f'rx="16" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="8"/>'
               f'<rect x="{f1(xa - pad)}" y="{f1(ya - pad)}" width="{f1(xb - xa + 2 * pad)}" height="{f1(yb - ya + 2 * pad)}" '
               f'rx="16" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>')


# ================================================================== sawdust and timing helpers
class Dust:
    """Sawdust specks falling from the saw cut (a stage-space Dynamic): small puffs on every push, big ones on
    the keyed beats."""

    def __init__(self, cut, pushes, big, t_off=1e9):
        self.cut, self.pushes, self.big, self.t_off = cut, pushes, set(round(b, 3) for b in big), t_off
        self.rng = np.random.default_rng(int(cut[0]))
        self.parts = []
        for tp in pushes:
            n = 22 if round(tp, 3) in self.big else 5
            for _ in range(n):
                vx = self.rng.uniform(-90, 90) * (2.2 if n > 10 else 1.0)
                vy = self.rng.uniform(-160, -20) * (1.6 if n > 10 else 1.0)
                r = self.rng.uniform(2.5, 5.5) * (1.3 if n > 10 else 1.0)
                c = (232, 200, 144) if self.rng.random() < 0.6 else (210, 168, 108)
                self.parts.append((tp, vx, vy, r, c))
        self.W, self.H = 360, 300

    def __call__(self, t):
        if t > self.t_off:
            return None
        live = [p for p in self.parts if 0 <= t - p[0] <= 0.9]
        if not live:
            return None
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ox, oy = self.cut[0] - self.W / 2, self.cut[1] - 60
        for tp, vx, vy, r, c in live:
            u = t - tp
            x = self.cut[0] + vx * u - ox
            y = self.cut[1] + vy * u + 520 * u * u - oy
            a = int(255 * (1 - u / 0.9))
            if 0 <= x < self.W and 0 <= y < self.H:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(*c, a))
        return im, (ox, oy)


def hammer_phase(strikes):
    """t -> hammer phase 0 (raised) .. 1 (strike) from a sorted list of strike times."""
    strikes = sorted(strikes)

    def f(t):
        prev = max([s for s in strikes if s <= t], default=None)
        nxt = min([s for s in strikes if s > t], default=None)
        p = 0.0
        if prev is not None:
            u = t - prev
            p = 1.0 if u < 0.07 else 1 - clamp((u - 0.07) / 0.14)
        if nxt is not None:
            gap = nxt - (prev if prev is not None else nxt - 1.0)
            down = min(0.13, 0.4 * gap)
            if nxt - t < down:
                p = max(p, 1 - (nxt - t) / down)
        return p
    return f


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines

    # ------------------------------------------------------------ beats
    t_start = L[0].start
    t_saw = pt(ctx, 0, "锯木头")
    gz = char_beats(ctx, 0, "嘎吱嘎吱", (0, 2))                 # 嘎吱 / 嘎吱
    t_nail = pt(ctx, 0, "钉钉子")
    dd = char_beats(ctx, 0, "叮叮当当", (0, 1, 2, 3))           # 叮 叮 当 当
    t_long = L[1].start
    t_field = pt(ctx, 1, "比一个足球场")
    t_decks = pt(ctx, 1, "它有三层")
    t_door = pt(ctx, 1, "旁边开一个门")
    t_win = pt(ctx, 1, "上面开一个窗户")
    t_days = L[2].start
    t_days_end = L[2].end
    t_final = L[3].start
    t_done = pt(ctx, 3, "方舟造好了")
    t_done = max(t_done, t_final + 0.5)

    # ------------------------------------------------------------ day / night montage
    DAY0 = t_days + 0.05
    PD = (t_days_end + 0.1 - DAY0) / 3.0                     # three days and nights
    n_days = 3
    nights = [DAY0 + PD * (k + 0.75) for k in range(n_days)]
    t_swap = nights[-1]                                      # the workers become the family in the last night
    t_dawn = DAY0 + PD * n_days

    def night(t):
        a = 0.0
        for tn in nights:
            a = max(a, math.exp(-((t - tn) / (0.2 * PD)) ** 2))
        return a

    # ------------------------------------------------------------ the ark's progress
    def prog(t):
        keys = [(0.0, 0.06), (t_start, 0.06), (t_saw - 0.1, 0.2), (t_long - 0.3, 0.33), (t_days, 0.42),
                (t_dawn - 0.25, 0.95), (t_done - 0.35, 0.95), (t_done, 1.0)]
        for (ta, a), (tb, b) in zip(keys, keys[1:]):
            if t <= tb:
                return a + (b - a) * clamp((t - ta) / max(1e-6, tb - ta))
        return 1.0
    PROGS = [round(0.05 * k, 2) for k in range(1, 21)]
    ark_frames = [doc(PR.ark(ARK_X, GY, A, progress=p, ramp=True)) for p in PROGS]

    def ark_frame(t):
        p = prog(t)
        f = (p - 0.05) / 0.05
        f = max(0.0, min(len(PROGS) - 1.0, f))
        if p >= 0.999:
            return float(len(PROGS) - 1)
        if f > len(PROGS) - 2:
            f = len(PROGS) - 2.0          # no crossfade into the finished ark (the door / ramp appear on the beat)
        return f

    # ------------------------------------------------------------ backdrop
    sc.add("sky", sky_svg(), wc=0.45)
    sc.add("far", far_svg(), wc=0.7)
    sc.add("meadow", meadow_svg(), wc=0.8)
    for i, (cx, cy, w, h, sd, v) in enumerate(((600, 260, 360, 96, 3, 6), (1500, 160, 300, 86, 7, 5),
                                                (2350, 420, 280, 76, 11, 7), (300, 560, 220, 60, 5, 4))):
        sc.add(f"cloud{i}", doc(S.g(S.cloud(cx, cy, w, h, "#fdf6e8", seed=sd, sw=3, shade_fill="#efe2d0"),
                                    filter="wobble")), wc=0.7,
               motion=lambda t, v=v, i=i: Tf(dx=-v * t - (90 * clamp((t - DAY0) / (t_dawn - DAY0)) if t > DAY0 else 0),
                                             dy=3 * math.sin(t / (1.1 + 0.2 * i))))
    # the day sun (fades out while the days rush by, back at the last dawn)
    day_sun_a = lambda t: 1 - M.progress(t, DAY0 - 0.3, DAY0 + 0.1, "sine") + M.progress(t, t_dawn - 0.1, t_dawn + 0.5,
                                                                                         "sine")
    sc.add("sun", sun_svg(2450, 230), wc=0.3, motion=lambda t: Tf(alpha=clamp(day_sun_a(t))))

    def arc(t, off):
        u = (t - DAY0) / PD - off
        k, v = math.floor(u), u - math.floor(u)
        if k < 0 or k >= n_days or v > 0.5:
            return None
        w = v / 0.5
        return 150 + 2500 * w, 820 - 640 * math.sin(math.pi * w)
    SX0, SY0 = 1000, 500

    def sun_m(t, off, ox, oy):
        p = arc(t, off)
        if p is None:
            return Tf(alpha=0.0)
        return Tf(dx=p[0] - ox, dy=p[1] - oy)
    sc.add("sun_arc", sun_svg(SX0, SY0, uid="s6sa"), wc=0.3, motion=lambda t: sun_m(t, 0.0, SX0, SY0))
    sc.add("moon_arc", moon_svg(SX0, SY0), wc=0.3, motion=lambda t: sun_m(t, 0.5, SX0, SY0))
    sc.add("yard", yard_svg(), wc=0.7)
    sc.add("ark", ark_frames, wc=0.8, frame_at=ark_frame)

    # ------------------------------------------------------------ the workers
    # saw rhythm: a push (phase .5) exactly on both 嘎吱 beats; quicker while the days rush by
    P_SAW = max(0.32, min(0.62, gz[1] - gz[0]))
    t_fast = DAY0

    def saw_phase_fn(t0, off=0.0):
        def f(t):
            if t < t_fast:
                return (0.5 + (t - t0) / P_SAW + off) % 1.0
            base = 0.5 + (t_fast - t0) / P_SAW + off
            return (base + (t - t_fast) / (P_SAW * 0.6)) % 1.0
        return f

    def pushes(phase_fn, t_a, t_b):
        out, t = [], t_a
        last = phase_fn(t_a)
        while t < t_b:
            t += 1 / 60
            p = phase_fn(t)
            if (last < 0.5 <= p) or (last > p and p >= 0.5):
                out.append(t)
            last = p
        return out

    actors = []
    hops = {}
    for name, x, facing, off, seed in (("noah", NOAH_X, 1, 0.0, 61), ("japheth", JAP_X, -1, 0.5, 62)):
        sp = sprite(760, 440, 380, 400, seed=seed)
        frames = [fam(sp, name, "saw", s=A, facing=facing, phase=ph) for ph in (0.0, 0.25, 0.5, 0.75)]
        phf = saw_phase_fn(gz[0], off)
        alpha = lambda t: 1.0 if t < t_swap else 0.0
        walk = lambda t, phf=phf, frames=frames: frames[int(phf(t) * 4 + 0.5) % 4] if t < t_swap else None
        sched = [(0, frames[0], 0)]
        actors.append((name, Actor(sp, sched, lambda t, x=x: (x, GY), walk=walk, alpha=alpha, breathe=0.0)))
        cut = (x + facing * 209 * A, GY - 104 * A)
        big = gz if name == "noah" else []
        pl = pushes(phf, 0.0, t_swap)
        big = [min(pl, key=lambda v: abs(v - b)) for b in big] if pl else []
        sc_dust = Dust(cut, pl, big, t_off=t_swap)
        actors.append((name + "_dust", sc_dust))
        hops[name] = cut

    # hammer strikes: a steady rhythm, then one strike per 叮 叮 当 当 (Shem 1 + 3, Ham 2 + 4), faster in the montage
    def strikes(first, period, keyed, t_end):
        out, t = [], first
        while t < t_end:
            if all(abs(t - k) > 0.5 for k in keyed):
                out.append(t)
            t += period if t < t_fast else period * 0.5
        return sorted(out + keyed)
    s_shem = strikes(t_start + 0.4, 0.9, [dd[0], dd[2]], t_swap - 0.1)
    s_ham = strikes(t_start + 0.85, 0.9, [dd[1], dd[3]], t_swap - 0.1)
    HPH = (0.0, 0.35, 0.7, 1.0)
    for name, x, facing, sts, seed in (("shem", SHEM_X, 1, s_shem, 63), ("ham", HAM_X, -1, s_ham, 64)):
        sp = sprite(560, 480, 260, 440, seed=seed)
        frames = [fam(sp, name, "hammer", s=A, facing=facing, phase=ph) for ph in HPH]
        hp = hammer_phase(sts)

        def walk(t, hp=hp, frames=frames):
            if t >= t_swap:
                return None
            p = hp(t)
            return frames[min(range(4), key=lambda i: abs(HPH[i] - p))]
        actors.append((name, Actor(sp, [(0, frames[0], 0)], lambda t, x=x: (x, GY), walk=walk,
                                   alpha=lambda t: 1.0 if t < t_swap else 0.0, breathe=0.0)))
        hops[name] = (x + facing * C.NOAH_NAIL[0] * A * (1.04 if name == "shem" else 1.05),
                      GY + C.NOAH_NAIL[1] * A * (1.04 if name == "shem" else 1.05))

    # shadows (static under the workers; the family gets its own)
    sh = ""
    for x in (NOAH_X, SHEM_X, HAM_X, JAP_X):
        sh += C.ground_shadow(x, GY, A, width=150, opacity=0.24)
    sc.add("sh_work", doc(sh), wc=0, motion=lambda t: Tf(alpha=1.0 if t < t_swap else 0.0))
    # the sawhorses stay in the yard when the saws stop
    horses = (PR.sawhorse(NOAH_X + 236 * A, GY, A * 0.72, 1) + PR.sawhorse(JAP_X - 236 * A, GY, A * 0.72, -1))
    sc.add("horses", doc(horses), wc=0.6, motion=lambda t: Tf(alpha=1.0 if t >= t_swap else 0.0))
    for name, a in actors:
        sc.add_dynamic(name, a)

    # ------------------------------------------------------------ the family at the end
    spF = sprite(900, 470, 450, 430, seed=70)
    f_stand = spF.add(C.noah_family(spF.ax, spF.ay, A, 1, pose="stand", expr="happy"))
    f_cheer = spF.add(C.noah_family(spF.ax, spF.ay, A, 1, pose="cheer"))
    sc.add("sh_fam", doc(C.ground_shadow(GROUP_X, GY, A, width=900, opacity=0.2)), wc=0,
           motion=lambda t: Tf(alpha=1.0 if t >= t_swap else 0.0))
    sc.add_dynamic("family", Actor(spF, [(0, f_stand, 0), (t_done + 0.05, f_cheer, 1.2)], lambda t: (GROUP_X, GY),
                                   alpha=lambda t: 1.0 if t >= t_swap else 0.0, bper=2.6))

    # ------------------------------------------------------------ sound words and clangs
    nx, ny = hops["noah"]
    for k, tb in enumerate(gz):
        wx, wy = nx + 40 + 60 * k, ny - 250 - 40 * k
        sc.add(f"gz{k}", word_svg(wx, wy, "嘎吱", 70), wc=0,
               motion=lambda t, tb=tb, wx=wx, wy=wy: pop_tf(t, tb, tb + 0.75, wx, wy - 20, dur_in=0.2, bob=3))
    for k, tb in enumerate(dd):
        who = "shem" if k % 2 == 0 else "ham"
        hx, hy = hops[who]
        sc.add(f"clang{k}", clang_svg(hx, hy, 1.0), wc=0,
               motion=lambda t, tb=tb, hx=hx, hy=hy: pop_tf(t, tb, tb + 0.28, hx, hy, dur_in=0.08, dur_out=0.15, bob=0))
        wx, wy = hx + (1 if who == "shem" else -1) * 30, hy - 150 - 30 * (k // 2)
        sc.add(f"ding{k}", word_svg(wx, wy, "叮" if k < 2 else "当", 76, col="#d4a020"), wc=0,
               motion=lambda t, tb=tb, wx=wx, wy=wy: pop_tf(t, tb, tb + 0.6, wx, wy - 26, dur_in=0.15, bob=2))

    # ------------------------------------------------------------ the comparison panel (line 1)
    t_p_in, t_p_out = t_long + 0.1, t_days - 0.45
    pmo = lambda t, d=0.0: pop_tf(t, t_p_in + d, t_p_out, PC, (PANEL[1] + PANEL[3]) / 2, bob=2)
    sc.add("panel_bg", panel_bg_svg(), wc=0.3, motion=lambda t: pmo(t))
    sc.add("panel_pitch", panel_pitch_svg(), wc=0.5, motion=lambda t: pmo(t, 0.15))
    sc.add("pitch_arrow", pitch_arrow_svg(), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_field - 0.2, t_field + 0.3, "out"), "soft": 30},
           motion=lambda t: pmo(t, 0.15))

    def ark_in(t):
        b = pmo(t, 0.15)
        u = M.progress(t, t_long + 0.6, t_long + 1.3, "out")
        return Tf(dx=b.dx, dy=b.dy - 60 * (1 - u), sx=b.sx, sy=b.sy, alpha=b.alpha * u, px=b.px, py=b.py)
    sc.add("panel_ark", panel_ark_svg(), wc=0.5, motion=ark_in)
    sc.add("ark_arrow", ark_arrow_svg(), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_field + 0.35, t_field + 1.2, "out"), "soft": 30},
           motion=lambda t: pmo(t, 0.15))
    for i in range(3):
        td = t_decks + 0.15 + 0.32 * i
        sc.add(f"deck{i}", deck_svg(i), wc=0,
               motion=lambda t, td=td: (lambda b, k: Tf(dx=b.dx, dy=b.dy, sx=b.sx, sy=b.sy, px=b.px, py=b.py,
                                                        alpha=b.alpha * k))(pmo(t, 0.15),
                                                                            M.progress(t, td, td + 0.15, "sine") *
                                                                            (1 - M.progress(t, t_door - 0.1, t_door + 0.2,
                                                                                            "sine"))))
    for nm, box, tb in (("door", PR.ARK_DOOR, t_door), ("win", PR.ARK_WINDOW, t_win)):
        sc.add(f"ring_{nm}", ring_svg(box), wc=0,
               motion=lambda t, tb=tb: (lambda b, k: Tf(dx=b.dx, dy=b.dy, sx=b.sx, sy=b.sy, px=b.px, py=b.py,
                                                        alpha=b.alpha * k))(pmo(t, 0.15),
                                                                            M.progress(t, tb + 0.1, tb + 0.3, "sine") *
                                                                            (0.75 + 0.25 * math.sin(2 * math.pi * (t - tb) / 0.6))))

    # ------------------------------------------------------------ the day counter (line 2)
    DCX, DCY = 1400, 150
    DC_N = n_days
    dcs = [doc(PR.day_counter(DCX, DCY, 1.15, n=DC_N, filled=k * 0.5, icons="pair", gap=90)) for k in range(2 * DC_N + 1)]

    def dc_frame(t):
        if t < DAY0:
            return 0.0
        return float(min(2 * DC_N, int((t - DAY0) / (PD / 2) + 0.5)))
    sc.add("days", dcs, wc=0, frame_at=dc_frame,
           motion=lambda t: Tf(alpha=M.progress(t, DAY0 - 0.3, DAY0, "sine") * (1 - M.progress(t, t_done - 0.6,
                                                                                               t_done - 0.1, "sine"))))
    sc.add("night", doc(S.rect_bg("#5d6aa6", SW, SH)), wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=0.62 * night(t)))
    sc.add_dynamic("night_stars", sparkle_dyn((100, 60, 2700, 560), count=16, t0=DAY0, t1=t_dawn, color=(255, 248, 220),
                                              size=(5, 10), period=0.7, drift=0, seed=3, fade=0.2))

    # ------------------------------------------------------------ the finished ark
    sc.add_dynamic("done_sparkle", sparkle_dyn((ARK_X - 760, GY - 820, ARK_X + 700, GY - 200), count=22, t0=t_done,
                                               t1=T + 1, size=(9, 18), period=1.3, drift=-8, seed=6))
    sc.add("fg", [fg_svg(sw) for sw in (-0.5, 0.0, 0.5)], wc=0.7,
           frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.4))

    # ------------------------------------------------------------ CAMERA
    def cam_at(x, w):
        return Cam(x, GY - 340 * w / 1920, w)
    c0 = cam_at(1350, 2500)
    c_saw = cam_at(590, 1350)
    c_ham = cam_at(1505, 1400)
    c_full = Cam(1400, 787, 2800)
    c_end = cam_at(1450, 2450)
    keys = [(0.0, c0), (t_saw - 0.9, c0), (t_saw + 0.1, c_saw), (t_nail - 0.6, c_saw), (t_nail + 0.25, c_ham),
            (L[0].end + 0.1, c_ham), (t_long + 0.5, c_full), (t_done - 0.3, c_full), (t_done + 1.2, c_end),
            (T, cam_at(1452, 2440))]
    sc.camera = clamp_cam(M.cam_keys(keys, "sine"), SW, SH)

    # ------------------------------------------------------------ SOUND
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-25, fade_in=0.8, fade_out=1.0)
    for tb in gz:
        sc.sfx("ship_creak", tb - 0.02, dur=0.45, gain_db=-8, fade_in=0.02, fade_out=0.1, pan=-0.4)
    for k, tb in enumerate(dd):
        sc.sfx("hammer", tb - 0.02, dur=0.35, gain_db=-6, fade_out=0.15, pan=-0.1 if k % 2 == 0 else 0.25)
        sc.sfx("coins", tb, gain_db=-16, pan=-0.1 if k % 2 == 0 else 0.25)
    for tb in s_shem + s_ham:          # the steady background knocks, soft
        if all(abs(tb - d) > 0.3 for d in dd) and tb < t_swap:
            sc.sfx("hammer", tb - 0.02, dur=0.25, gain_db=-24, fade_out=0.1, pan=0.0)
    sc.sfx("pop", t_p_in, gain_db=-13)
    sc.sfx("whoosh", t_field + 0.35, gain_db=-18)
    for i in range(3):
        sc.sfx("pop", t_decks + 0.15 + 0.32 * i, gain_db=-14)
    sc.sfx("pop", t_door + 0.1, gain_db=-14)
    sc.sfx("pop", t_win + 0.1, gain_db=-14)
    sc.sfx("pop", t_p_out, gain_db=-16)
    for k in range(n_days):
        sc.sfx("whoosh", DAY0 + PD * (k + 0.5), gain_db=-22)
        sc.sfx("night", nights[k] - 0.35, dur=0.7, gain_db=-18, fade_in=0.2, fade_out=0.3)
    sc.sfx("rooster", t_dawn - 0.1, gain_db=-16, pan=0.5)
    sc.sfx("chime", t_done, gain_db=-11)
    sc.sfx("cheer", t_done + 0.05, dur=T - t_done + 0.8, gain_db=-15, fade_in=0.1, fade_out=1.0)
    return sc
