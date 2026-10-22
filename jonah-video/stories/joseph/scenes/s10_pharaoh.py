"""Scene 10 — Pharaoh's dream (Genesis 41:1-36).

N '过了两年，埃及的法老王做了一个奇怪的梦。七头肥肥的牛，被七头瘦瘦的牛吃掉了！' /
N '没有人能解这个梦。这时候，有人想起了约瑟。' /
Y '上帝告诉你，会有七年大丰收，接着是七年大饥荒。要趁丰收的时候，把粮食存起来。'

One 2600 x 1350 stage, two places joined by soft dissolves:
  * PHARAOH'S BEDROOM at night (page-turn dip in from s09): deep-blue walls with a frieze of gold stars, lotus
    columns, a tall window with the moon, stars and palms, linen curtains stirring, a standing lamp; Pharaoh asleep
    on his royal couch.
      line 0  '过了两年，'                      calm night, stars twinkle; the camera drifts in.
              '埃及的法老王做了一个奇怪的梦。'  Pharaoh snuggles in his sleep; a big dream bubble blooms over him:
                                                the Nile, its green banks, far pyramids.
              '七头肥肥的牛，'                  seven round happy cows climb up out of the river one after another
                                                (splash), counted 1-7 by little gold badges.
              '被七头瘦瘦的牛'                  seven skinny, big-eyed cows climb up out of the river after them.
              '吃掉了！'                        gulp-gulp-gulp: each thin cow opens wide and its fat cow vanishes in a
                                                puff (comic, never shown eating) — and the thin cows stay just as thin.
      Pharaoh wakes with a start, sitting up with his hands on his head, worried; the bubble pops.
  * THE THRONE HALL by day (dissolve): painted columns, a frieze, sunbeams, Pharaoh on his gilded throne.
      line 1  '没有人能解这个梦。'              three wise men shrug one after another ('?'); Pharaoh sighs.
              '这时候，有人想起了约瑟。'        the cupbearer starts — a gold idea-star bursts over his head — and he
                                                turns to Pharaoh; a thought bubble shows Joseph in the prison light.
      (soft dissolve: later, the same hall) Joseph — washed, in a clean white linen tunic — bows before the throne,
      the cupbearer behind him.
      line 2  '上帝告诉你，'                    Joseph points up (God gives the meaning: light only); Pharaoh listens.
              '会有七年大丰收，'                a picture panel opens above them: seven golden wheat fields pop up one
                                                by one; Pharaoh smiles.
              '接着是七年大饥荒。'              below them seven dry, cracked fields; Pharaoh is worried.
              '要趁丰收的时候，'                the golden row glows; Joseph explains.
              '把粮食存起来。'                  a granary appears; three sacks hop from the golden fields into it and
                                                its silos fill up; Pharaoh is delighted. Calm last frame (page-turn dip
                                                into s11).
"""
import math
import random

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine import watercolor as WC
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.daniel.scenes.s05_prays import clamp, fig
from stories.david.scenes.s08_saul import Actor, TightSprite, pop_k, pop_tf, pt, sparkle_dyn
from stories.joseph.scenes.s08_egypt import ShadowSprite, f1, jlib, mul_alpha, person_sprite, poly, rect

SW, SH = 2600, 1350
GY = 1060
KB = 1.05                       # bedroom scale
KH = 0.92                       # throne hall scale
INK = P["ink"]

# bedroom
COUCH_X = 700
MATT_Y = GY - 122 * KB          # mattress top
PH_X = COUCH_X + 14             # Pharaoh lying / sitting up on the couch
WIN = (1900, 140, 2380, 900)    # the tall window: x0, y0, x1, y1
# the dream bubble
DB = (1270, 440, 1560, 620)     # centre x, y, w, h
DX0, DY0, DPW, DPH = 440, 20, 1660, 960   # the dream canvas on the stage
BACK_Y, FRONT_Y = 500, 590      # cow rows (stage y)
RIVER_TOP = 604
CS = 0.52                       # cow scale
FAT_X = [670 + 200 * i for i in range(7)]
THIN_X = [x - 50 for x in FAT_X]
# throne hall
THRONE_X = 1760
WISE_X = [770, 950, 1130]
CUPB_X = 1420                   # the cupbearer (shot A)
JOS_X = 1235                    # Joseph before the throne (shot B)
CUPB_X2 = 905                   # the cupbearer behind Joseph (shot B)
PANEL = (1440, 390, 1300, 540)  # the explanation panel: centre x, y, w, h
TILE_W, TILE_H, TILE_GAP = 136, 110, 14
TILE_X0 = 916                  # the two rows are centred in the panel ...
ROW_Y = (268, 398)              # tile tops: good years, famine
GROUP_A, GROUP_K = (850, 390), 0.66   # ... then shrink toward the left to make room for the granary
GRAN = (1800, 540, 0.46)        # granary inside the panel: x, bottom y, scale


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


# ================================================================== bedroom drawings
def bedroom_svg():
    defs = (S.lin_grad("s10bw", [(0, "#24325a"), (0.6, "#2f4170"), (1, "#3a4a72")])
            + S.lin_grad("s10bf", [(0, "#4a3f5c"), (1, "#3b3249")])
            + S.lin_grad("s10sky", [(0, "#16213e"), (1, "#2c3f6c")])
            + S.rad_grad("s10lamp", [(0, "#ffd98a", 0.55), (0.5, "#f3b860", 0.18), (1, "#f3b860", 0)])
            + S.rad_grad("s10moon", [(0, "#fff6d8", 0.6), (1, "#fff6d8", 0)]))
    b = S.rect_bg("url(#s10bw)", SW, SH)
    # star frieze along the top (Egyptian ceilings are painted with gold stars)
    b += rect(-40, -40, SW + 80, 150, "#1d2950", 0)
    rng = random.Random(4)
    for i in range(40):
        x, y = 30 + i * 66 + rng.uniform(-8, 8), 40 + (i % 2) * 34
        r = 12
        pts = []
        for k in range(10):
            a = math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((x + rr * math.cos(a), y - rr * math.sin(a)))
        b += poly(pts, "#e8b63c", 0)
    b += rect(-40, 108, SW + 80, 22, "#c9533f", 3) + rect(-40, 130, SW + 80, 14, "#e8b63c", 3)
    # a gold lotus frieze on the blue wall
    for i in range(34):
        x = 30 + i * 80
        b += (f'<path d="M{x},{GY - 300} Q{x - 22},{GY - 344} {x},{GY - 370} Q{x + 22},{GY - 344} {x},{GY - 300} Z" '
              f'fill="none" stroke="#c99b3c" stroke-width="4"/>')
        b += f'<circle cx="{x + 40}" cy="{GY - 322}" r="8" fill="#c99b3c"/>'
    b += rect(-40, GY - 392, SW + 80, 8, "#c99b3c", 0) + rect(-40, GY - 286, SW + 80, 8, "#c99b3c", 0)
    # window: night sky, moon, stars, palms
    x0, y0, x1, y1 = WIN
    win = rect(x0, y0, x1 - x0, y1 - y0, "url(#s10sky)", 5, rx=10)
    win += f'<circle cx="{x0 + 330}" cy="{y0 + 180}" r="130" fill="url(#s10moon)"/>'
    win += f'<circle cx="{x0 + 330}" cy="{y0 + 180}" r="52" fill="#fbf0c8" stroke="{INK}" stroke-width="4"/>'
    win += f'<circle cx="{x0 + 352}" cy="{y0 + 166}" r="44" fill="#22305a"/>'
    win += S.path(S.hill(x0, x1, y1 - 80, 40, seed=2, bumps=2, bottom=y1), fill="#1e2a48", sw=3)
    win += PR._haze(PR.pyramids(x0 + 250, y1 - 90, 0.22, n=2, ground=False), "#2a3a66", 0.55, 0.4)
    b += S.g(win, filter="wobble")
    b += PR._haze(PR.palm_tree(x1 - 60, y1 - 50, 0.55, lean=-0.2), "#1e2a48", 0.75, 0.6)
    # window frame + sill
    b += S.g(rect(x0 - 26, y0 - 26, x1 - x0 + 52, 30, "#c9b089", 4) + rect(x0 - 40, y1 - 6, x1 - x0 + 80, 34, "#c9b089", 4)
             + rect(x0 - 26, y0, 26, y1 - y0, "#b89e78", 4) + rect(x1, y0, 26, y1 - y0, "#b89e78", 4), filter="wobble-fine")
    # floor
    b += S.g(rect(-40, GY - 10, SW + 80, SH - GY + 60, "url(#s10bf)", 4), filter="wobble")
    for i in range(-2, 22):
        b += f'<path d="M{i * 140},{GY - 6} L{i * 140 - 60},{SH + 20}" stroke="#2f2840" stroke-width="3" opacity="0.5"/>'
    b += f'<ellipse cx="{COUCH_X}" cy="{GY + 70}" rx="520" ry="70" fill="#7a3f5c" opacity="0.75" stroke="{INK}" stroke-width="3"/>'
    b += f'<ellipse cx="{COUCH_X}" cy="{GY + 70}" rx="470" ry="52" fill="none" stroke="#e8b63c" stroke-width="5" opacity="0.8"/>'
    # columns
    out = S.g(b, filter=None)
    for x in (240, 1180, 1620):
        out += PR._haze(PR.egypt_column(x, GY + 4, 1.0, height=820), "#2a3a66", 0.45, 0.35)
    # standing lamp by the couch (warm glow) and a low table with a jug
    lx = COUCH_X + 420
    out += f'<ellipse cx="{lx}" cy="{GY - 420}" rx="420" ry="360" fill="url(#s10lamp)"/>'
    out += S.g(tube_d([(lx, GY), (lx, GY - 330)], 12, "#c9a24e") + rect(lx - 50, GY - 12, 100, 16, "#c9a24e", 3, rx=6)
               + f'<path d="M{lx - 46},{GY - 330} Q{lx},{GY - 300} {lx + 46},{GY - 330} Z" fill="#c9a24e" stroke="{INK}" stroke-width="3.4"/>',
               filter="wobble-fine")
    out += S.g(rect(COUCH_X - 520, GY - 110, 150, 18, P["wood"], 3.4, rx=6)
               + rect(COUCH_X - 505, GY - 92, 14, 92, P["wood_dark"], 3) + rect(COUCH_X - 399, GY - 92, 14, 92, P["wood_dark"], 3),
               filter="wobble-fine")
    out += PR.jar(COUCH_X - 465, GY - 110 - 82 * 0.5, 0.5)
    out += PR.couch(COUCH_X, GY, KB)
    return doc(out, defs)


def tube_d(pts, w, col, ow=3.4):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f1(w + 2 * ow)}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f1(w)}" stroke-linecap="round"/>')


def flame_svg(k):
    lx = COUCH_X + 420
    h = 34 + 6 * k
    return doc(S.g(f'<path d="M{lx},{GY - 340 - h} Q{lx + 16 - 4 * k},{GY - 352} {lx},{GY - 334} Q{lx - 16 + 3 * k},{GY - 352} '
                   f'{lx},{GY - 340 - h} Z" fill="#ffc94a" stroke="#d27a2a" stroke-width="3"/>', filter="wobble-fine"))


def curtain_svg(sw):
    x0, y0, x1, y1 = WIN
    out = ""
    for side, xx in ((-1, x0 + 10), (1, x1 - 10)):
        bot = y1 + 30
        d = (f"M{xx},{y0 - 24} L{xx - side * 120},{y0 - 24} Q{xx - side * (90 + 20 * sw)},{(y0 + bot) / 2} "
             f"{xx - side * (60 + 30 * sw)},{bot} L{xx + side * 6},{bot} Q{xx - side * 10 * sw},{(y0 + bot) / 2} {xx},{y0 - 24} Z")
        out += f'<path d="{d}" fill="#efe4c8" stroke="{INK}" stroke-width="4" opacity="0.92"/>'
        out += (f'<path d="M{xx - side * 40},{y0} Q{xx - side * (40 + 12 * sw)},{(y0 + bot) / 2} {xx - side * (30 + 18 * sw)},{bot - 10}" '
                f'fill="none" stroke="#cbbd9c" stroke-width="3"/>')
    return doc(S.g(out, filter="wobble-fine"))


def stars_body(seed=3):
    x0, y0, x1, y1 = WIN
    rng = random.Random(seed)
    out = ""
    for _ in range(18):
        x, y = rng.uniform(x0 + 30, x1 - 30), rng.uniform(y0 + 30, y1 - 200)
        if math.hypot(x - (x0 + 330), y - (y0 + 180)) < 90:
            continue
        r = rng.uniform(4, 8)
        out += f'<path d="M{f1(x)},{f1(y - r)} L{f1(x + r * 0.3)},{f1(y)} L{f1(x)},{f1(y + r)} L{f1(x - r * 0.3)},{f1(y)} Z" fill="#fff3c4"/>'
    return out


# ================================================================== the dream
def _loc(markup):
    return f'<g transform="translate({-DX0},{-DY0})">{markup}</g>'


def dream_base_svg():
    x, y, w, h = DB
    defs = S.lin_grad("s10dsky", [(0, "#bfe2ea"), (0.8, "#f6ecc8"), (1, "#f8e2b4")])
    inner = f'<defs>{defs}</defs><rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="url(#s10dsky)"/>'
    inner += f'<circle cx="{x + 470}" cy="{y - 150}" r="44" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" stroke-width="4"/>'
    inner += S.cloud(x - 420, y - 170, 220, 60, "#fdf6e8", seed=3, sw=3)
    inner += PR._haze(PR.pyramids(x + 80, BACK_Y - 112, 0.3, n=3, ground=False), "#e9e2c8", 0.25, 0.3)
    inner += S.path(S.hill(x - w, x + w, BACK_Y - 110, 14, seed=5, bumps=5, bottom=BACK_Y - 80), fill="#e2cf98", sw=3)
    inner += S.path(S.hill(x - w, x + w, BACK_Y - 92, 10, seed=7, bumps=6, bottom=RIVER_TOP + 30), fill="#a9c76a", sw=3.5)
    inner += f'<rect x="{x - w}" y="{FRONT_Y - 50}" width="{2 * w}" height="70" fill="#9cbd5e"/>'
    for gx in range(x - w // 2, x + w // 2, 120):
        inner += PR.grass_tuft(gx + 40, BACK_Y + 8, 0.45, variant=(gx // 120) % 3)
    inner += river_body(0.0, back=True)
    return S.svg_doc(_loc(PR.dream_bubble(x, y, w, h, tail=(PH_X - 140, MATT_Y - 70), inner=inner, seed=12, glow=False)),
                     w=DPW, h=DPH)


def river_body(ph, back=False):
    x, y, w, h = DB
    top = RIVER_TOP + (0 if back else 4)
    d = S.wave_band(top, 5, 160, ph * 2 * math.pi, x - w, x + w, bottom=y + h + 40)
    out = f'<path d="{d}" fill="{"#4f97b8" if back else "#5aa3c2"}" stroke="{INK}" stroke-width="3.5"/>'
    nb = S.hill(x - w, x + w, RIVER_TOP + 96, 8, seed=9, bumps=7, bottom=y + h + 40)
    out += f'<path d="{nb}" fill="#93b85c" stroke="{INK}" stroke-width="3.5"/>'
    if not back:
        for gx in range(x - w // 2 + 30, x + w // 2, 150):
            out += PR.papyrus(gx, RIVER_TOP + 150, 0.5)
        out += f'<path d="{S.wave_line(top + 30, 4, 120, ph * 2 * math.pi + 1, x - w, x + w)}" fill="none" stroke="#bfe3ea" stroke-width="4" opacity="0.8"/>'
        for lx in (x - 520, x - 140, x + 300, x + 560):
            out += f'<ellipse cx="{lx}" cy="{top + 52}" rx="22" ry="8" fill="#7fb05a" stroke="{INK}" stroke-width="2.4"/>'
    return out


def river_front_svg(ph):
    return S.svg_doc(_loc(S.g(river_body(ph), filter="wobble-fine")), w=DPW, h=DPH)


def dream_mask_svg():
    x, y, w, h = DB
    inner = f'<rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="#ffffff"/>'
    return S.svg_doc(_loc(PR.dream_bubble(x, y, w, h, inner=inner, fill="#000000", glow=False, seed=12)), w=DPW, h=DPH)


def badge_markup(n, x, y):
    out = f'<circle cx="{x}" cy="{y}" r="26" fill="#f6d36a" stroke="{INK}" stroke-width="4"/>'
    out += S.text(x, y + 13, str(n), size=38, fill=INK)
    return S.g(out, filter="wobble-fine")


def puff_markup(x, y, s=1.0, col="#fffaf0", edge="#c9bfae"):
    out = ""
    circ = ((-30, -6, 22), (-4, -20, 28), (26, -8, 24), (46, 4, 15), (-48, 6, 14), (4, 10, 20))
    for dx, dy, r in circ:
        out += f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s)}" fill="{col}" stroke="{edge}" stroke-width="{f1(6 * s)}"/>'
    for dx, dy, r in circ:
        out += f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s)}" fill="{col}"/>'
    return S.g(out, filter="wobble-fine")


def splash_markup(x, y, s=1.0):
    out = ""
    for a, ln in ((-60, 34), (-90, 44), (-120, 34), (-75, 26), (-105, 26)):
        r = math.radians(a)
        out += (f'<path d="M{f1(x + 10 * math.cos(r))},{f1(y + 10 * math.sin(r))} L{f1(x + ln * s * math.cos(r))},'
                f'{f1(y + ln * s * math.sin(r))}" stroke="#e8f6f8" stroke-width="{f1(9 * s)}" stroke-linecap="round"/>')
    out += f'<ellipse cx="{x}" cy="{y + 4}" rx="{56 * s}" ry="{12 * s}" fill="#e8f6f8" stroke="#8cc4d6" stroke-width="3"/>'
    return S.g(out, filter="wobble-fine")


class Dream:
    """Dynamic: the dream bubble with the river, the fat cows climbing out (counted), the thin cows after them and the
    comic gulps, everything inside the bubble (masked by its interior), popping in and out about its centre."""

    def __init__(self, t_in, t_out, fat_t, thin_t, gulp_t, seed=61):
        self.t_in, self.t_out, self.fat_t, self.thin_t, self.gulp_t = t_in, t_out, fat_t, thin_t, gulp_t
        self.seed = seed
        self._ready = False
        sp = TightSprite(460, 380, 230, 310, seed=seed)
        self.sp = sp
        ax, ay = sp.ax, sp.ay
        self.fat_walk = [sp.add(PR.cow(ax, ay, CS, 1, "fat", "walk", phase=k / 8)) for k in range(8)]
        self.fat_stand = sp.add(PR.cow(ax, ay, CS, 1, "fat", "stand"))
        self.fat_graze = sp.add(PR.cow(ax, ay, CS, 1, "fat", "graze"))
        self.thin_walk = [sp.add(PR.cow(ax, ay, CS, 1, "thin", "walk", phase=k / 8)) for k in range(8)]
        self.thin_stand = sp.add(PR.cow(ax, ay, CS, 1, "thin", "stand"))
        self.thin_open = sp.add(PR.cow(ax, ay, CS, 1, "thin", "stand", mouth=0.85))
        self.puff = sp.add(puff_markup(ax, ay - 40, 1.25))
        self.splash = sp.add(splash_markup(ax, ay, 1.5))
        self.badges = [sp.add(badge_markup(n + 1, ax, ay - 30)) for n in range(7)]

    def _prep(self):
        if self._ready:
            return
        base = raster.rasterize(dream_base_svg(), DPW, DPH)
        self.base = WC.watercolor(base, seed=self.seed, strength=0.45)
        m = raster.rasterize(dream_mask_svg(), DPW, DPH)
        a = np.asarray(m).astype(np.float32)
        self.mask = (np.clip((a[..., 0] - 60) / 150, 0, 1) * (a[..., 3] / 255.0)).astype(np.float32)
        self.front = []
        for ph in (0.0, 0.5):
            im = raster.rasterize(river_front_svg(ph), DPW, DPH)
            self.front.append(WC.watercolor(im, seed=self.seed + 1, strength=0.35))
        self._ready = True

    def _put(self, canvas, idx, x, y, sx=1.0, sy=1.0, dy=0.0, alpha=1.0):
        out = self.sp.place(idx, x - DX0, y - DY0, sx, sy, dy, alpha)
        if out is None:
            return
        im, (l, tp) = out
        _paste(canvas, im, l, tp)

    def __call__(self, t):
        if t < self.t_in or t > self.t_out + 0.3:
            return None
        self._prep()
        k, a = pop_k(t, self.t_in, self.t_out, 0.45, 0.25)
        cv = Image.new("RGBA", (DPW, DPH), (0, 0, 0, 0))
        # fat cows: climb out of the river, then stand (a gentle nod), then vanish in a puff when gulped
        for i in range(7):
            ts, tg = self.fat_t[i], self.gulp_t[i]
            if t < ts or t >= tg:
                continue
            u = clamp((t - ts) / 0.5)
            e = M.ease("out")(u)
            y = M.lerp(RIVER_TOP + 132, BACK_Y, e)
            x = FAT_X[i] - 26 * (1 - e)
            if u < 1:
                idx = self.fat_walk[int((t - ts) / 0.07) % 8]
            else:
                idx = self.fat_graze if (int((t - ts + i * 0.37) / 1.1) % 3 == 2) else self.fat_stand
            self._put(cv, idx, x, y, dy=-2 * math.sin(2 * math.pi * (t * 0.8 + i * 0.13)))
        # thin cows: climb out after them into the front row
        for i in range(7):
            ts, tg = self.thin_t[i], self.gulp_t[i]
            if t < ts:
                continue
            u = clamp((t - ts) / 0.5)
            e = M.ease("out")(u)
            y = M.lerp(RIVER_TOP + 140, FRONT_Y, e)
            x = THIN_X[i] - 24 * (1 - e)
            sx = sy = 1.0
            if u < 1:
                idx = self.thin_walk[int((t - ts) / 0.07) % 8]
            elif tg - 0.2 <= t < tg + 0.08:
                idx = self.thin_open
                sy = 1.06
                sx = 0.97
            else:
                idx = self.thin_stand
                v = t - tg - 0.08
                if 0 <= v < 0.35:                    # gulp: a squash and a little hop
                    q = math.sin(math.pi * v / 0.35)
                    sy, sx = 1 - 0.1 * q, 1 + 0.08 * q
            self._put(cv, idx, x, y, sx, sy)
        # splashes where the cows climb out
        for ts, xs in [(self.fat_t[i], FAT_X[i]) for i in range(7)] + [(self.thin_t[i], THIN_X[i]) for i in range(7)]:
            v = t - ts
            if 0 <= v < 0.45:
                q = v / 0.45
                self._put(cv, self.splash, xs - 10, RIVER_TOP + 8, 0.7 + 0.6 * q, 0.7 + 0.6 * q, alpha=1 - q * q)
        # the river in front (hides the cows still under water)
        fr = self.front[int(t / 0.5) % 2]
        cv.alpha_composite(fr)
        # puffs where the fat cows vanish, count badges
        for i in range(7):
            v = t - self.gulp_t[i]
            if 0 <= v < 0.5:
                q = v / 0.5
                self._put(cv, self.puff, FAT_X[i] + 10, BACK_Y - 30, 0.6 + 0.7 * q, 0.6 + 0.7 * q, -20 * q,
                          alpha=(1 - q) ** 1.3)
            tb = self.fat_t[i] + 0.3
            tb_out = self.thin_t[0] - 0.1
            if tb <= t < tb_out + 0.25:
                kb, ab = pop_k(t, tb, tb_out, 0.25, 0.25)
                self._put(cv, self.badges[i], FAT_X[i] + 14, BACK_Y - 112, kb, kb, alpha=ab)
        arr = np.asarray(cv).copy()
        arr[..., 3] = (arr[..., 3].astype(np.float32) * self.mask).astype(np.uint8)
        out = self.base.copy()
        out.alpha_composite(Image.fromarray(arr, "RGBA"))
        x0, y0 = DX0, DY0
        if abs(k - 1) > 1e-3 or a < 0.999:
            cx, cy = DB[0] - DX0, DB[1] + 120 - DY0
            nw, nh = max(1, int(DPW * k)), max(1, int(DPH * k))
            out = out.resize((nw, nh), Image.BILINEAR)
            x0, y0 = DX0 + cx - cx * k, DY0 + cy - cy * k
            if a < 0.999:
                o = np.asarray(out).copy()
                o[..., 3] = (o[..., 3].astype(np.float32) * a).astype(np.uint8)
                out = Image.fromarray(o, "RGBA")
        return out, (x0, y0)


def _paste(base, im, x, y):
    x, y = int(round(x)), int(round(y))
    bw, bh = base.size
    x0, y0, x1, y1 = max(0, x), max(0, y), min(bw, x + im.width), min(bh, y + im.height)
    if x1 <= x0 or y1 <= y0:
        return
    base.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


# ================================================================== throne hall drawings
def hall_svg():
    defs = (S.lin_grad("s10hw", [(0, "#e9cf9c"), (0.7, "#f1dcae"), (1, "#e3c48e")])
            + S.lin_grad("s10hf", [(0, "#d7b47c"), (1, "#c9a26a")])
            + S.lin_grad("s10sun", [(0, "#fff4d0", 0.55), (1, "#fff4d0", 0)], 0, 0, 0.35, 1))
    b = S.rect_bg("url(#s10hw)", SW, SH)
    # painted frieze bands
    b += rect(-40, -40, SW + 80, 120, "#3f6fa8", 0)
    for i in range(44):
        x = i * 62
        b += f'<path d="M{x},80 L{x + 31},40 L{x + 62},80 Z" fill="#e8b63c" stroke="{INK}" stroke-width="2.4"/>'
    b += rect(-40, 80, SW + 80, 26, "#c9533f", 3) + rect(-40, 106, SW + 80, 16, "#e8b63c", 3)
    # high windows with sunbeams
    for wx in (560, 1440, 2240):
        b += rect(wx - 70, 190, 140, 120, "#a9d6e6", 4, rx=8)
        for k in range(3):
            b += rect(wx - 52 + k * 42, 190, 10, 120, "#c9a26a", 2.4)
    # a painted lotus frieze and hanging banners
    for i in range(30):
        x = 40 + i * 90
        b += (f'<path d="M{x},{GY - 236} Q{x - 26},{GY - 290} {x},{GY - 320} Q{x + 26},{GY - 290} {x},{GY - 236} Z" '
              f'fill="#3f8f8a" stroke="{INK}" stroke-width="2.6"/>')
        b += f'<circle cx="{x + 45}" cy="{GY - 262}" r="11" fill="#e8b63c" stroke="{INK}" stroke-width="2.4"/>'
    b += rect(-40, GY - 340, SW + 80, 10, "#c9533f", 2.4) + rect(-40, GY - 222, SW + 80, 10, "#c9533f", 2.4)
    for bx in (300, 960, 1950, 2560):
        ban = rect(bx - 54, 140, 108, 380, "#f4ead2", 4, rx=6)
        for k, col in enumerate(("#3f6fa8", "#e8b63c", "#c9533f", "#3f6fa8", "#e8b63c")):
            ban += rect(bx - 54, 170 + k * 66, 108, 22, col, 2.4)
        ban += f'<path d="M{bx - 54},520 L{bx},556 L{bx + 54},520 Z" fill="#f4ead2" stroke="{INK}" stroke-width="4"/>'
        ban += rect(bx - 70, 128, 140, 16, P["wood_dark"], 3, rx=6)
        b += ban
    # dado
    b += rect(-40, GY - 190, SW + 80, 190, "#d9b884", 4)
    for i in range(30):
        b += rect(i * 96 + 10, GY - 160, 60, 120, "#c9a26a", 2.4, rx=6)
    b += rect(-40, GY - 196, SW + 80, 16, "#3f6fa8", 3)
    # floor
    fl = rect(-40, GY - 8, SW + 80, SH - GY + 60, "url(#s10hf)", 4)
    for i in range(-3, 26):
        fl += f'<path d="M{i * 120},{GY - 4} L{i * 120 - 70},{SH + 20}" stroke="#b58d58" stroke-width="3" opacity="0.6"/>'
    for y in (GY + 60, GY + 140, GY + 240):
        fl += f'<path d="M-40,{y} L{SW + 40},{y}" stroke="#b58d58" stroke-width="3" opacity="0.6"/>'
    fl += f'<ellipse cx="{THRONE_X - 150}" cy="{GY + 60}" rx="760" ry="72" fill="#b5523b" opacity="0.85" stroke="{INK}" stroke-width="3"/>'
    fl += f'<ellipse cx="{THRONE_X - 150}" cy="{GY + 60}" rx="700" ry="52" fill="none" stroke="#e8b63c" stroke-width="6"/>'
    out = S.g(b, filter="wobble") + S.g(fl, filter="wobble")
    for wx in (560, 1440, 2240):
        out += f'<path d="M{wx - 70},{310} L{wx + 70},{310} L{wx + 330},{GY} L{wx + 90},{GY} Z" fill="url(#s10sun)" filter="url(#soft)"/>'
    for x in (180, 2470):
        out += PR.egypt_column(x, GY + 4, 1.05, height=900)
    for x, s_ in ((380, 0.8), (2260, 0.8)):
        out += PR.palm_tree(x, GY - 150, 0.42) + S.g(rect(x - 60, GY - 150, 120, 150, "#b5523b", 4, rx=14), filter="wobble-fine")
    return doc(out, defs)


# ================================================================== idea / panel drawings
def thought_svg():
    """The cupbearer remembers: Joseph in the prison light."""
    x, y, w, h = 1560, 385, 460, 320
    inner = f'<rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="#bba98f"/>'
    for r in range(6):
        for c in range(8):
            inner += rect(x - w / 2 - 40 + c * 70 + (35 if r % 2 else 0), y - h / 2 + r * 48, 66, 44, "#c4b29a", 2.4, rx=8)
    inner += f'<path d="M{x - 30},{y - 120} L{x + 30},{y - 120} L{x + 80},{y + 140} L{x - 70},{y + 140} Z" fill="#fff0c0" opacity="0.6"/>'
    inner += PR.prison_window(x, y - 120, 0.55, light=0.0, wall=False)
    inner += C.joseph(x, y + 130, 0.6, 1, pose="stand", attire="prisoner", expr="kind", coat=None)
    return doc(PR.dream_bubble(x, y, w, h, tail=(CUPB_X + 10, GY - 330 * KH), inner=inner, seed=14))


def idea_star_svg(x, y):
    pts = []
    for k in range(16):
        a = -math.pi / 2 + k * math.pi / 8
        rr = 46 if k % 2 == 0 else 22
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    out = poly(pts, "#f6d04a", 4)
    out += f'<path d="M{x - 3},{y - 22} L{x + 5},{y - 22} L{x + 3},{y + 6} L{x - 1},{y + 6} Z" fill="{INK}"/>'
    out += f'<circle cx="{x + 1}" cy="{y + 16}" r="5" fill="{INK}"/>'
    for a in (-150, -110, -70, -30):
        r = math.radians(a)
        out += (f'<path d="M{f1(x + 62 * math.cos(r))},{f1(y + 62 * math.sin(r))} L{f1(x + 88 * math.cos(r))},{f1(y + 88 * math.sin(r))}" '
                f'stroke="#e8a83a" stroke-width="7" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def panel_svg():
    x, y, w, h = PANEL
    defs = S.lin_grad("s10pn", [(0, "#fbf3df"), (1, "#f6e6c4")])
    inner = f'<defs>{defs}</defs><rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="url(#s10pn)"/>'
    return doc(PR.dream_bubble(x, y, w, h, tail=(JOS_X + 30, GY - 345 * KH), inner=inner, seed=21))


def tile_svg(i, row):
    x = TILE_X0 + i * (TILE_W + TILE_GAP)
    y = ROW_Y[row]
    cid = f"s10t{row}{i}"
    clip = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>'
    sky = "#cfe7ee" if row == 0 else "#f3d7a6"
    body = f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" fill="{sky}"/>'
    body += PR.field(x - 10, x + TILE_W + 10, y + TILE_H * 0.5, depth=TILE_H * 0.6, scale=0.5,
                     ripe=1.0, dry=0.0 if row == 0 else 1.0, seed=10 + i + 7 * row)
    if row == 1:
        body += f'<circle cx="{x + TILE_W - 22}" cy="{y + 18}" r="11" fill="#f6a43c" stroke="{INK}" stroke-width="2.4"/>'
    else:
        body += f'<circle cx="{x + TILE_W - 22}" cy="{y + 18}" r="10" fill="{P["sun"]}" stroke="{INK}" stroke-width="2.4"/>'
    out = f'<defs>{clip}</defs><g clip-path="url(#{cid})">{body}</g>'
    out += f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="14" fill="none" stroke="{INK}" stroke-width="4"/>'
    return doc(S.g(out, filter="wobble-fine"))


def row_glow_svg():
    x0 = TILE_X0 - 26
    x1 = TILE_X0 + 7 * (TILE_W + TILE_GAP) + 12
    y = ROW_Y[0] + TILE_H / 2
    defs = S.rad_grad("s10rg", [(0, "#ffe9a0", 0.85), (0.6, "#ffe9a0", 0.35), (1, "#ffe9a0", 0)])
    return doc(f'<ellipse cx="{(x0 + x1) / 2}" cy="{y}" rx="{(x1 - x0) / 2 + 40}" ry="{TILE_H}" fill="url(#s10rg)"/>', defs)


def granary_svg(fill):
    gx, gy, gs = GRAN
    return doc(PR.granary(gx, gy, gs, fill=fill))


SACK0 = (200, 300)


def sack_svg():
    return doc(PR.grain_sacks(SACK0[0], SACK0[1], 0.4, n=1))


# ================================================================== people
def wise_sprite(v, seed):
    sp = person_sprite(KH, seed=seed)
    d = dict(stand=sp.add(C.egyptian(sp.ax, sp.ay, KH, 1, kind="wise", variant=v, pose="stand", expr="worried")),
             shrug=sp.add(C.egyptian(sp.ax, sp.ay, KH, 1, kind="wise", variant=v, pose="shrug")),
             sad=sp.add(C.egyptian(sp.ax, sp.ay, KH, 1, kind="wise", variant=v, pose="sad")))
    return sp, d


WAKE = dict(C.POSES["wake"], arms=(("ik", "head", 0.80, -0.78, 1), ("ik", "head", -0.80, -0.75, -1)),
            hands=("open", "open"), expr="worried")


def pharaoh_fig(sp, ps, expr, s, facing, label):
    D = C._pharaoh_design("stand", False)
    return sp.add(fig(D, C._PHARAOH_M, dict(ps), expr, sp.ax, sp.ay, s, facing, label))


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    # ---------------------------------------------------------------- beats
    t_snug = pt(ctx, 0, "法老王") + 0.1             # Pharaoh snuggles in his sleep
    t_dream = pt(ctx, 0, "奇怪的梦") - 0.15         # the dream bubble blooms
    t_fat = pt(ctx, 0, "七头肥") - 0.05             # fat cows climb out, 1-7
    fat_t = [t_fat + 0.2 * i for i in range(7)]
    t_thin = pt(ctx, 0, "被七头") + 0.05            # thin cows climb out after them
    thin_t = [t_thin + 0.17 * i for i in range(7)]
    t_gulp = pt(ctx, 0, "吃掉了") + 0.05            # gulp-gulp-gulp
    gulp_t = [t_gulp + 0.08 * i for i in range(7)]
    t_dream_out = gulp_t[-1] + 0.4
    t_wake = t_dream_out - 0.05                     # Pharaoh wakes, worried
    t_h0 = L1.start + 0.22                          # dissolve to the throne hall
    t_h1 = t_h0 + 0.7
    t_shrug = [pt(ctx, 1, "没有人") + 0.72 + 0.2 * i for i in range(3)]
    t_sigh = t_shrug[-1] + 0.4
    t_idea = pt(ctx, 1, "这时候") + 0.05            # the cupbearer starts: idea-star
    t_think = pt(ctx, 1, "有人想起") + 0.0          # thought bubble: Joseph
    t_turn = t_think + 0.1
    t_think_out = L1.end + 0.12
    t_b0 = L1.end + 0.2                             # dissolve: later, Joseph before the throne
    t_b1 = t_b0 + 0.7
    t_up = pt(ctx, 2, "上帝告诉") - 0.08            # Joseph points up
    t_explain = pt(ctx, 2, "会有") - 0.05
    t_good = pt(ctx, 2, "七年大丰") - 0.1           # seven golden fields
    t_panel = t_good - 0.4
    good_t = [t_good + 0.11 * i for i in range(7)]
    t_bad = pt(ctx, 2, "七年大饥") - 0.1            # seven dry fields
    bad_t = [t_bad + 0.11 * i for i in range(7)]
    t_store = pt(ctx, 2, "要趁") + 0.0              # the golden row glows
    t_gran = pt(ctx, 2, "把粮食") - 0.1             # granary appears, sacks hop in, it fills
    sack_t = [t_gran + 0.35 + 0.28 * i for i in range(3)]
    t_fill0 = t_gran + 0.5
    t_happy = pt(ctx, 2, "存起来") + 0.1

    bed_a = lambda t: 1.0 - M.progress(t, t_h0, t_h1, "sine")
    hall_a = lambda t: M.progress(t, t_h0, t_h1, "sine")
    A_a = lambda t: hall_a(t) * (1.0 - M.progress(t, t_b0, t_b1, "sine"))
    B_a = lambda t: M.progress(t, t_b0, t_b1, "sine")

    # ================================================================ THE THRONE HALL (underneath)
    sc.add("hall", hall_svg(), wc=0.8)
    # Pharaoh on his throne (one performer through both hall shots)
    tsp = person_sprite(KH, seed=71, wide=260, shadow=150)
    th = dict(worried=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="worried")),
              sigh=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="sad")),
              surprised=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="surprised")),
              neutral=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="neutral")),
              happy=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="happy")),
              amazed=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="amazed")),
              proud=tsp.add(C.pharaoh(tsp.ax, tsp.ay, KH, -1, pose="sit_throne", expr="proud")))
    tsched = [(0, th["worried"], 0), (t_sigh, th["sigh"], 0.4), (t_turn + 0.25, th["surprised"], 0.5),
              (t_up + 0.3, th["neutral"], 0.3), (t_good + 0.5, th["happy"], 0.5), (t_bad + 0.4, th["worried"], 0.5),
              (t_store + 0.3, th["neutral"], 0.3), (t_happy, th["proud"], 0.7)]
    sc.add_dynamic("pharaoh_throne", Actor(tsp, tsched, lambda t: (THRONE_X, GY), alpha=hall_a, breathe=0.010,
                                           bper=3.3))
    # shot A: the wise men and the cupbearer
    for i, (x, v) in enumerate(zip(WISE_X, (1, 0, 2))):
        sp, d = wise_sprite(v, 72 + i)
        sched = [(0, d["stand"], 0), (t_shrug[i], d["shrug"], 0.8), (t_idea + 0.3 + 0.1 * i, d["stand"], 0.3)]
        sc.add_dynamic(f"wise{i}", Actor(sp, sched, lambda t, x=x: (x, GY), alpha=A_a, breathe=0.011,
                                         bper=2.8 + 0.3 * i, phase=0.2 * i))
    csp = person_sprite(KH, seed=76)
    cu = dict(stand=csp.add(C.egyptian(csp.ax, csp.ay, KH, -1, kind="cupbearer", pose="stand", expr="worried")),
              start=csp.add(C.egyptian(csp.ax, csp.ay, KH, -1, kind="cupbearer", pose="amazed", expr="surprised",
                                       marks=False)),
              talk=csp.add(C.egyptian(csp.ax, csp.ay, KH, 1, kind="cupbearer", pose="talk", expr="happy")),
              point=csp.add(C.egyptian(csp.ax, csp.ay, KH, 1, kind="cupbearer", pose="point", expr="happy")))
    csched = [(0, cu["stand"], 0), (t_idea, cu["start"], 1.0), (t_turn, cu["talk"], 0.7)]
    sc.add_dynamic("cupbearer", Actor(csp, csched, lambda t: (CUPB_X, GY), alpha=A_a, breathe=0.011, bper=3.0))
    # shot B: the cupbearer behind Joseph, Joseph before the throne
    csp2 = person_sprite(KH, seed=77)
    c2 = csp2.add(C.egyptian(csp2.ax, csp2.ay, KH, 1, kind="cupbearer", pose="stand", expr="happy"))
    sc.add_dynamic("cupbearer2", Actor(csp2, [(0, c2, 0)], lambda t: (CUPB_X2, GY), alpha=B_a, breathe=0.011, bper=3.1))
    jsp = person_sprite(KH, seed=78)
    jj = dict(bow=jlib(jsp, "bow", KH, 1, attire="slave", expr="kind"),
              up=jlib(jsp, "point_up", KH, 1, attire="slave", expr="kind"),
              explain=jlib(jsp, "explain", KH, 1, attire="slave", expr="kind"),
              happy=jlib(jsp, "explain", KH, 1, attire="slave", expr="happy"),
              worried=jlib(jsp, "explain", KH, 1, attire="slave", expr="worried"),
              talk=jlib(jsp, "talk", KH, 1, attire="slave", expr="determined"),
              point=jlib(jsp, "point", KH, 1, attire="slave", expr="happy"))
    jsched = [(0, jj["bow"], 0), (t_up, jj["up"], 0.9), (t_explain, jj["explain"], 0.6), (t_good + 0.3, jj["happy"], 0.3),
              (t_bad, jj["worried"], 0.4), (t_store, jj["talk"], 0.5), (t_gran, jj["point"], 0.7),
              (t_happy + 0.4, jj["happy"], 0.4)]
    sc.add_dynamic("joseph", Actor(jsp, jsched, lambda t: (JOS_X, GY), alpha=B_a, breathe=0.011, bper=3.0))
    sc.add_dynamic("up_sparkles", sparkle_dyn((JOS_X - 120, GY - 560, JOS_X + 200, GY - 300), count=10, t0=t_up + 0.1,
                                              t1=t_explain + 0.6, color=(255, 236, 160), size=(8, 16), seed=55))

    # cupbearer's idea and thought bubble
    ix, iy = CUPB_X - 10, GY - 395 * KH
    sc.add("idea", idea_star_svg(ix, iy), wc=0.3, motion=lambda t: Tf(**_mul(pop_tf(t, t_idea, t_think - 0.05, ix, iy), A_a(t))))
    sc.add("thought", thought_svg(), wc=0.4, motion=lambda t: Tf(**_mul(pop_tf(t, t_think, t_think_out, 1560, 520, 0.4), A_a(t))))

    # the explanation panel (shot B)
    px_, py_ = PANEL[0], PANEL[1]
    pan_m = lambda t: pop_tf(t, t_panel, 1e8, px_, py_ + 200, 0.45, bob=0.0)
    sc.add("panel", panel_svg(), wc=0.4, motion=pan_m)
    grp = lambda t: M.lerp(1.0, GROUP_K, M.progress(t, t_gran - 0.1, t_gran + 0.45, "inout"))

    def in_group(tf, c, t):
        g = grp(t)
        ax, ay = GROUP_A
        return Tf(dx=tf.dx + (g - 1) * (c[0] - ax), dy=tf.dy + (g - 1) * (c[1] - ay), sx=tf.sx * g, sy=tf.sy * g,
                  alpha=tf.alpha, px=c[0], py=c[1])

    def gpt(x, y, t):
        g = grp(t)
        return GROUP_A[0] + g * (x - GROUP_A[0]), GROUP_A[1] + g * (y - GROUP_A[1])
    rg_c = (TILE_X0 + 3.5 * (TILE_W + TILE_GAP) - TILE_GAP / 2, ROW_Y[0] + TILE_H / 2)
    sc.add("row_glow", row_glow_svg(), wc=0, blend="screen",
           motion=lambda t: in_group(Tf(alpha=M.progress(t, t_store, t_store + 0.5, "sine")
                                        * (0.7 + 0.3 * math.sin(2 * math.pi * (t - t_store) / 1.2))
                                        * (1 - 0.6 * M.progress(t, t_happy, t_happy + 1.0, "sine"))), rg_c, t))
    for row, tts in ((0, good_t), (1, bad_t)):
        for i in range(7):
            cxp = TILE_X0 + i * (TILE_W + TILE_GAP) + TILE_W / 2
            cyp = ROW_Y[row] + TILE_H / 2
            sc.add(f"tile{row}{i}", tile_svg(i, row), wc=0.4,
                   motion=lambda t, ts=tts[i], c=(cxp, cyp): in_group(pop_tf(t, ts, 1e8, c[0], c[1], 0.3, bob=0.0), c, t))
    gx, gy, gs = GRAN
    sc.add("granary", [granary_svg(v / 10) for v in range(11)], wc=0.5,
           frame_at=lambda t: float(min(10, max(0, int((t - t_fill0) / 0.14)))),
           motion=lambda t: pop_tf(t, t_gran, 1e8, gx, gy, 0.4, bob=0.0))
    for i, ts in enumerate(sack_t):
        x0s, y0s = gpt(TILE_X0 + (4 + i) * (TILE_W + TILE_GAP) + TILE_W / 2, ROW_Y[0] + TILE_H - 6, 1e9)
        x1s, y1s = gx - 80 + 60 * i, gy - 24

        def sk(t, ts=ts, x0s=x0s, y0s=y0s, x1s=x1s, y1s=y1s):
            u = (t - ts) / 0.55
            if u < 0 or u > 1.15:
                return Tf(alpha=0.0)
            uu = min(1.0, u)
            x = M.lerp(x0s, x1s, uu)
            y = M.lerp(y0s, y1s, uu) - 130 * math.sin(math.pi * uu)
            a = 1.0 if u < 1 else 1 - (u - 1) / 0.15
            k = min(1.0, u / 0.15)
            return Tf(dx=x - SACK0[0], dy=y - SACK0[1], rot=200 * uu, sx=k, sy=k, alpha=a, px=SACK0[0], py=SACK0[1] - 20)
        sc.add(f"sack{i}", sack_svg(), wc=0.4, motion=sk)

    # ================================================================ THE BEDROOM (on top; dissolves away)
    ba = lambda m=None: mul_alpha(m, bed_a)
    sc.add("bedroom", bedroom_svg(), wc=0.75, motion=ba())
    sc.add("stars", [doc(stars_body(3)), doc(stars_body(8))], wc=0, motion=ba(),
           frame_at=lambda t: 0.5 + 0.5 * math.sin(2 * math.pi * t / 2.4))
    sc.add("curtains", [curtain_svg(s_) for s_ in (-1.0, 0.0, 1.0)], wc=0.6, motion=ba(),
           frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 4.2))
    sc.add("flame", [flame_svg(0), flame_svg(1)], wc=0.3, motion=ba(),
           frame_at=lambda t: 0.5 + 0.5 * math.sin(2 * math.pi * t * 1.7))
    # Pharaoh asleep on the couch, then waking up worried
    bsp = ShadowSprite(760, 620, 380, 520, seed=79)
    p_sleep = bsp.add(C.pharaoh(bsp.ax, bsp.ay, KB, 1, pose="sleep", expr="sleepy"))
    p_dream = bsp.add(C.pharaoh(bsp.ax, bsp.ay, KB, 1, pose="sleep", expr="sleepy", marks=False))
    p_wake = pharaoh_fig(bsp, WAKE, "worried", KB, 1, "wake")
    bsched = [(0, p_sleep, 0), (t_snug, p_sleep, 0.35), (t_dream, p_dream, 0.0), (t_wake, p_wake, 1.2)]
    sc.add_dynamic("pharaoh_bed", Actor(bsp, bsched, lambda t: (PH_X, MATT_Y + 4), alpha=bed_a, breathe=0.016, bper=3.6))
    # the dream
    sc.add_dynamic("dream", Dream(t_dream, t_dream_out, fat_t, thin_t, gulp_t))
    # '!' when he wakes
    wx, wy = PH_X - 40, MATT_Y - 330 * KB
    sc.add("wake_marks", doc(S.g(
        f'<path d="M{wx - 10},{wy - 70} L{wx + 10},{wy - 70} L{wx + 4},{wy} L{wx - 4},{wy} Z" fill="#f2c14e" stroke="{INK}" stroke-width="4"/>'
        f'<circle cx="{wx}" cy="{wy + 22}" r="9" fill="#f2c14e" stroke="{INK}" stroke-width="4"/>'
        + "".join(f'<path d="M{wx + 40 * math.cos(math.radians(a))},{wy - 20 + 40 * math.sin(math.radians(a))} '
                  f'L{wx + 70 * math.cos(math.radians(a))},{wy - 20 + 70 * math.sin(math.radians(a))}" stroke="{P["ink_soft"]}" '
                  f'stroke-width="6" stroke-linecap="round"/>' for a in (-20, 200, -60, 240)), filter="wobble-fine")),
           wc=0, motion=lambda t: Tf(**_mul(pop_tf(t, t_wake + 0.05, t_h0 + 0.2, wx, wy + 20, 0.25), bed_a(t))))

    # ---------------------------------------------------------------- camera
    cam0 = Cam(1100, 640, 2000)
    camP = Cam(880, 760, 1440)                       # Pharaoh asleep
    camD = Cam(1270, 545, 1840)                      # the dream
    camA = Cam(1330, 700, 1760)                      # wise men, cupbearer, Pharaoh
    camA2 = Cam(1560, 640, 1660)                     # the cupbearer remembers
    camB = Cam(1450, 612, 2040)                      # Joseph before the throne, the panel above
    camBc = Cam(1500, 730, 1600)                     # closer: Joseph bows, points up
    sc.camera = M.cam_keys([(0.0, cam0), (L0.start - 0.2, cam0), (t_snug + 0.3, camP), (t_dream - 1.2, camP),
                            (t_fat + 0.15, camD), (t_dream_out - 0.1, camD), (t_shrug[0] + 0.4, camA), (t_idea, camA),
                            (t_think + 0.4, camA2), (t_b0, camA2), (t_b1 + 0.5, camBc), (t_panel - 0.3, camBc),
                            (t_panel + 0.9, camB), (T, Cam(1450, 618, 2010))],
                           "sine")
    sc.fx = [FX.vignette(lambda t: 0.35 * bed_a(t), color=(14, 18, 40))]

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=t_h1, gain_db=-18, fade_in=0.8, fade_out=0.6)
    sc.sfx("snore", 0.3, dur=t_dream - 0.3, gain_db=-22, fade_in=0.6, fade_out=0.6)
    sc.sfx("cloth", t_snug, gain_db=-18)
    sc.sfx("chime", t_dream, gain_db=-13)
    sc.sfx("waves_calm", t_dream + 0.3, dur=t_dream_out - t_dream, gain_db=-22, fade_in=0.5, fade_out=0.4)
    for i, ts in enumerate(fat_t):
        sc.sfx("splash_small", ts, gain_db=-17 + (i % 2), pan=-0.4 + 0.13 * i)
        sc.sfx("pop", ts + 0.3, gain_db=-16, pan=-0.4 + 0.13 * i)
    for i, ts in enumerate(thin_t):
        sc.sfx("splash_small", ts, gain_db=-19, pan=-0.45 + 0.13 * i)
    for i, ts in enumerate(gulp_t):
        if i % 2 == 0:
            sc.sfx("gulp", ts - 0.05, gain_db=-12 - i * 0.5, pan=-0.4 + 0.13 * i)
        sc.sfx("pop", ts, gain_db=-12, pan=-0.4 + 0.13 * i)
    sc.sfx("pop", t_dream_out, gain_db=-12)
    sc.sfx("cloth", t_wake, gain_db=-12, duck_db=-3)
    sc.sfx("birds", t_h0, dur=T - t_h0, gain_db=-22, fade_in=0.8, fade_out=0.8)
    for i, ts in enumerate(t_shrug):
        sc.sfx("cloth", ts, gain_db=-17, pan=-0.4 + 0.1 * i)
    sc.sfx("sparkle", t_idea, gain_db=-12, pan=0.1)
    sc.sfx("pop", t_think, gain_db=-12, pan=0.2)
    sc.sfx("pop", t_think_out, gain_db=-17, pan=0.2)
    sc.sfx("cloth", t_b1, gain_db=-18)
    sc.sfx("chime", t_up + 0.1, gain_db=-13)
    sc.sfx("pop", t_panel, gain_db=-12)
    for i, ts in enumerate(good_t):
        sc.sfx("pop", ts, gain_db=-17, pan=-0.3 + 0.08 * i)
    sc.sfx("sparkle", t_good + 0.5, gain_db=-16)
    for i, ts in enumerate(bad_t):
        sc.sfx("pop", ts, gain_db=-18, pan=-0.3 + 0.08 * i)
    sc.sfx("wither", t_bad + 0.2, gain_db=-20)
    sc.sfx("sparkle", t_store, gain_db=-16)
    sc.sfx("pop", t_gran, gain_db=-12, pan=0.3)
    for ts in sack_t:
        sc.sfx("whoosh", ts, gain_db=-19, pan=0.2)
        sc.sfx("thud", ts + 0.55, gain_db=-14, pan=0.35)
    sc.sfx("grow", t_fill0, gain_db=-17, pan=0.3)
    return sc


def _mul(tf, a):
    return dict(dx=tf.dx, dy=tf.dy, rot=tf.rot, sx=tf.sx, sy=tf.sy, alpha=tf.alpha * a, px=tf.px, py=tf.py)
