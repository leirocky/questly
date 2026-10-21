"""Scene 9 - the flood (Genesis 7:10-24). 七天以后，下雨了 ... 外面的一切，都不见了。

A tall 3000 x 1690 stage: the closed ark (scale 0.34) on its green hill under heavy slate clouds; behind it a plain
and a range of mountains (the highest peak at the right). The water is two layers of flood_sea moved up in steps:
the FAR water rises in front of the plain and the mountains, the NEAR water in front of the hill (and in front of
the floating ark, hiding the keel). Nobody and no animal is ever outside: only weather and water.

  line 0  '七天以后，'  a little seven-day counter (suns popping one by one) in the sky corner.
          '下雨了。'  the clouds darken.   '滴答，滴答……'  on each 滴答 one big drop falls and splashes on the ark's roof
          (single drops start to fall).   '哗啦啦，哗啦啦！'  the rain pours (two surges of rain streaks), a soft
          lightning glow inside a cloud, the ark turns wet and shiny.
  line 1  '大雨下了四十天四十夜。'  a day counter plaque (sun and moon) counts 1 -> 40, landing on 40 with a pop.
          '水越涨越高，越涨越高。'  the water surges up in steps (two steps on each 越涨越高), flooding the plain and the
          foot of the hill.   '方舟浮起来了，'  the water reaches the keel: the ark lifts and floats, bobbing.
          '在水上漂啊漂。'  it drifts and rocks gently; the camera starts to pull back.
  line 2  '大水盖过了最高的山。'  wide shot: the far water climbs over the last mountain top.
          '外面的一切，都不见了。'  only the ark on a wide grey sea under the rain; calm hold (dip to black).
"""
import math
import random

import numpy as np
from PIL import Image

from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Tf
from engine.scene import Scene
from stories.noah.scenes.s07_animals import Spr, cam_at, cam_path, clamp, pt

SW, SH = 3000, 1690
S9 = 0.34
AX, GY = 1500, 1150                      # the ark on the hilltop (keel on GY)
DRAFT = PR.ARK_DRAFT * S9                # keel below the waterline when floating
WL0 = GY - DRAFT                         # the waterline that lifts the ark
INK = P["ink"]
FAR_FINAL = 560                          # far water level at the end (above the highest peak)
NEAR_FINAL = 985                         # near water level at the end


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ drawings
def sky_svg():
    defs = S.lin_grad("n9sky", [(0, "#4c5a70"), (0.35, "#6c7a8e"), (0.62, "#9aa5b0"), (1, "#b4b9b6")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#n9sky)"/>', defs)


BACK_PEAKS = [(-120, 900), (260, 770), (640, 840), (980, 730), (1330, 820), (1700, 760), (2150, 600), (2620, 740),
              (2960, 800), (3150, 900)]
FRONT_PEAKS = [(-120, 1040), (180, 930), (520, 980), (860, 900), (1180, 960), (1880, 950), (2380, 900), (2780, 960),
               (3150, 1000)]


def _ridge(peaks, base, seed, dip=150):
    """Ridge line through the peaks with valleys between (points), closed down to `base`."""
    rng = random.Random(seed)
    pts = []
    for (xa, ya), (xb, yb) in zip(peaks, peaks[1:]):
        pts.append((xa, ya))
        pts.append(((xa + xb) / 2 + rng.uniform(-40, 40), max(ya, yb) + dip * rng.uniform(0.7, 1.1)))
    pts.append(peaks[-1])
    return pts


def mountains_svg():
    """Two ranges of mountains behind the plain: a hazy back range with the highest snowy peak (x 2150), a greener
    front range; ridges, gullies and snow caps."""
    defs = S.lin_grad("n9mb", [(0, "#99a3ab"), (1, "#828e96")]) + S.lin_grad("n9mf", [(0, "#7f8e82"), (1, "#6a7c6a")])
    out = ""
    for peaks, fill, seed, dip, snow in ((BACK_PEAKS, "url(#n9mb)", 5, 170, 790), (FRONT_PEAKS, "url(#n9mf)", 9, 110, 0)):
        pts = _ridge(peaks, 1320, seed, dip)
        d = S.smooth_path(pts, closed=False, tension=0.55) + f" L{SW + 150},1330 L-150,1330 Z"
        out += S.path(d, fill, sw=3.5)
        rng = random.Random(seed + 1)
        for x, y in peaks:
            # gullies and a shady flank
            out += (f'<path d="M{f1(x)},{f1(y + 8)} L{f1(x + 120 + rng.uniform(0, 60))},1320 L{f1(x + 30)},1320 Z" '
                    f'fill="#4b3426" opacity="0.08"/>')
            for k in range(2):
                gx = x + rng.uniform(-50, 50)
                out += (f'<path d="M{f1(gx)},{f1(y + 50 + 30 * k)} q{f1(rng.uniform(-30, 30))},{f1(80)} '
                        f'{f1(rng.uniform(-50, 50))},{f1(160 + 60 * k)}" fill="none" stroke="#5f6e66" stroke-width="2.4" '
                        f'opacity="0.45"/>')
            if snow and y < snow:
                h = (snow - y) * 0.55 + 30
                cap = [(x - h * 0.75, y + h), (x - h * 0.35, y + h * 0.7), (x - h * 0.15, y + h * 0.95), (x, y - 2),
                       (x + h * 0.2, y + h * 0.8), (x + h * 0.45, y + h * 1.0), (x + h * 0.8, y + h * 1.1),
                       (x + h * 0.3, y + h * 0.2)]
                out += S.path(S.smooth_path(cap[:4] + [(x + h * 0.15, y + h * 0.15)] + cap[4:7], tension=0.5),
                              "#eef0ec", sw=2.5)
    return doc(S.g(out, filter="wobble"), defs)


def plain_svg():
    """The wide plain below the hill: fields, a river line, far trees and little empty houses."""
    defs = S.lin_grad("n9pl", [(0, "#7e8f72"), (1, "#6d8062")])
    out = S.path(S.wave_band(1250, 8, 900, 0.3, x0=-60, x1=SW + 60, bottom=SH + 60, seed=4), "url(#n9pl)", sw=3.5)
    rng = random.Random(7)
    for k in range(4):
        y = 1290 + k * 60
        out += (f'<path d="{S.wave_line(y, 6, 700, k * 1.1, x0=-60, x1=SW + 60)}" fill="none" stroke="#6f8660" '
                f'stroke-width="3" stroke-dasharray="40 26" opacity="0.6"/>')
    for _ in range(26):
        x = rng.uniform(0, SW)
        y = rng.uniform(1262, 1330)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(12, 22))}" ry="{f1(rng.uniform(9, 14))}" '
                f'fill="#5f7c55" stroke="{INK}" stroke-width="2"/>')
    for x, v in ((420, 0), (2700, 2), (2560, 1)):
        out += PR.house(x, 1300, 0.16, variant=v)
    return doc(S.g(out, filter="wobble"), defs)


HILL = [(-80, 1700), (420, 1560), (850, 1380), (1180, 1172), (1500, 1150), (1820, 1170), (2180, 1370), (2600, 1560),
        (3080, 1700)]


def hill_svg():
    defs = S.lin_grad("n9hill", [(0, "#7e9b5c"), (1, "#5f7f46")])
    d = S.smooth_path(HILL, closed=False, tension=0.8) + f" L{SW + 80},{SH + 60} L-80,{SH + 60} Z"
    out = S.path(d, "url(#n9hill)", sw=4.5)
    rng = random.Random(3)
    for x, y, s, sd in ((980, 1300, 0.32, 1), (2060, 1290, 0.3, 2)):
        out += PR.olive_tree(x, y, s, seed=sd)
    for x, y, s, v in ((1180, 1190, 0.35, 0), (1880, 1196, 0.32, 1), (760, 1440, 0.4, 3), (2380, 1460, 0.42, 0)):
        out += PR.bush(x, y, s, variant=v)
    for _ in range(40):
        x = rng.uniform(300, 2700)
        y = rng.uniform(1200, 1650)
        c = rng.choice(("#f6e27a", "#fff3d6", "#c9a7e0"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(4, 6.5))}" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    return doc(S.g(out, filter="wobble"), defs)


def ark_svg(wet):
    return doc(PR.ark(AX, WL0, S9, 1, door=0.0, window=0.0, ramp=False, floating=True, wet=wet))


CLOUDS = [(260, 270, 1.45, 1), (1080, 200, 1.75, 2), (1930, 300, 1.5, 3), (2740, 250, 1.6, 4), (700, 470, 1.0, 5),
          (2380, 480, 1.05, 6), (1480, 430, 0.85, 7), (3350, 330, 1.5, 8), (3150, 520, 1.0, 9)]


BACK_CLOUDS = [(600, 120, 1.3, 21), (1500, 90, 1.5, 22), (2450, 140, 1.35, 23), (120, 520, 0.9, 24),
               (2900, 560, 0.95, 25), (1950, 600, 0.8, 26), (3250, 160, 1.3, 27)]


def back_clouds_svg():
    out = ""
    for x, y, s_, sd in BACK_CLOUDS:
        out += PR.dark_cloud(x, y, s_, seed=sd, light=0.75)
    return doc(S.g(out, opacity=0.9))


def clouds_svg(flash_i=None, k=0.0):
    out = ""
    for i, (x, y, s, sd) in enumerate(CLOUDS):
        out += PR.dark_cloud(x, y, s, seed=sd, light=0.25 + 0.08 * (i % 3), flash=k if i == flash_i else 0.0)
    return doc(out)


def splash_markup(cx, cy, k=1.0):
    """A little crown of water on the roof (a single drop landing)."""
    col = PR.RAIN_COL
    out = ""
    for a in (-160, -125, -55, -20):
        r = math.radians(a)
        x, y = cx + 22 * k * math.cos(r), cy + 16 * k * math.sin(r) - 4
        out += f'<path d="{PR._raindrop_d(x, y, 5.5 * k)}" fill="{col}" stroke="{S.shade(col, -0.4)}" stroke-width="1.6" ' \
               f'transform="rotate({a + 90:.0f} {f1(x)} {f1(y)})"/>'
    out += (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(16 * k)}" ry="{f1(5 * k)}" fill="none" '
            f'stroke="{S.shade(col, -0.2)}" stroke-width="2.4"/>')
    return out


# ============================================================================ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    t_seven = pt(ctx, 0, "七天")
    t_rain = pt(ctx, 0, "下雨了")
    t_di = [pt(ctx, 0, "滴答", k) for k in range(2)]
    t_hua = [pt(ctx, 0, "哗啦啦", k) for k in range(2)]
    t_40 = pt(ctx, 1, "四十天")
    t_40n = pt(ctx, 1, "四十夜")
    t_up = [pt(ctx, 1, "越涨越高", k) for k in range(2)]
    t_float = pt(ctx, 1, "方舟浮")
    t_drift = pt(ctx, 1, "漂啊漂")
    t_high = pt(ctx, 2, "最高的山")
    t_gone = pt(ctx, 2, "都不见了")

    # ---------------- water levels (stage y of the surfaces), stepping up on the narration
    d_up = 0.55
    near_keys = [(0, 1830), (t_up[0] - 0.05, 1830), (t_up[0] + d_up, 1600), (t_up[0] + 0.62, 1600),
                 (t_up[0] + 0.62 + d_up, 1470), (t_up[1] - 0.05, 1470), (t_up[1] + d_up, 1330),
                 (t_up[1] + 0.62, 1330), (t_up[1] + 0.62 + d_up, 1215), (t_float - 0.35, WL0 + 18),
                 (t_float + 0.9, WL0 - 34), (t_drift, WL0 - 50), (t_high, NEAR_FINAL + 25), (T - 1.0, NEAR_FINAL)]
    far_keys = [(0, 1760), (t_up[0] - 0.05, 1760), (t_up[0] + d_up, 1330), (t_up[0] + 0.62, 1330),
                (t_up[0] + 0.62 + d_up, 1230), (t_up[1] - 0.05, 1230), (t_up[1] + d_up, 1110),
                (t_up[1] + 0.62, 1110), (t_up[1] + 0.62 + d_up, 1030), (t_float + 1.0, 960), (L1.end + 0.3, 880),
                (L2.start + 0.1, 840), (t_high - 0.2, 735), (t_high + 0.8, 592), (t_gone, 575), (T - 1.0, FAR_FINAL)]

    def level(keys):
        def f(t):
            if t <= keys[0][0]:
                return keys[0][1]
            for (ta, a), (tb, b) in zip(keys, keys[1:]):
                if t <= tb:
                    return a + (b - a) * M.progress(t, ta, tb, "inout" if b != a else "linear")
            return keys[-1][1]
        return f
    near = level(near_keys)
    far = level(far_keys)

    # ---------------- camera: close on the ark on its hill, then wider as the water rises, then the whole sea
    BOT = SH - 2
    C0 = cam_at(1500, 1800, 1430)
    C1 = cam_at(1520, 2050, 1500)
    C2 = cam_at(1530, 2380, 1560)
    CW = cam_at(1500, 2990, BOT)
    sc.camera = cam_path([(0, C0), (t_up[0] - 0.4, C0), (t_float - 0.2, C1), (t_drift + 0.2, C1), (L2.start - 0.2, C2),
                          (t_high + 0.9, CW), (T, CW)], sw=SW, sh=SH)

    # ---------------- sky, mountains, plain, far water, hill
    sc.add("sky", sky_svg(), z=0, wc=0.45)
    sc.add("mountains", mountains_svg(), z=1, wc=0.7)
    sc.add("plain", plain_svg(), z=1.5, wc=0.7)
    phases = 6
    far_fr = [doc(PR.flood_sea(-80, SW + 80, FAR_FINAL, phase=k / phases, bottom=1130, storm=0.55, seed=3,
                               scale=0.55)) for k in range(phases)]
    sc.add("far_sea", far_fr, z=2, wc=0.6, frame_at=lambda t: float(int(t * 5) % phases),
           motion=lambda t: Tf(dy=far(t) - FAR_FINAL))
    sc.add("hill", hill_svg(), z=3, wc=0.8)

    # ---------------- the ark: on the hill, then lifted by the water, bobbing and drifting
    t_wet = t_hua[0] + 0.2

    def ark_motion(t):
        y = min(0.0, near(t) - WL0)
        fl = clamp((WL0 - near(t)) / 20.0)
        bob = fl * (6 * math.sin(2 * math.pi * t / 2.6) + 2.5 * math.sin(2 * math.pi * t / 1.15))
        rot = fl * (1.6 * math.sin(2 * math.pi * t / 3.1) + 0.6 * math.sin(2 * math.pi * t / 1.7))
        dx = 70 * M.progress(t, t_drift - 0.6, T, "sine")
        return Tf(dx=dx, dy=y + bob, rot=rot, px=AX, py=WL0)
    sc.add("ark_dry", ark_svg(False), z=4, motion=lambda t: Tf(alpha=1 - M.progress(t, t_wet, t_wet + 1.2, "sine")))
    sc.add("ark", ark_svg(True), z=4.05, motion=lambda t: (lambda v: Tf(v.dx, v.dy, v.rot, alpha=M.progress(
        t, t_wet, t_wet + 1.2, "sine"), px=v.px, py=v.py))(ark_motion(t)))
    sc.layers[-2].motion = (lambda t: (lambda v: Tf(v.dx, v.dy, v.rot, alpha=1 - M.progress(t, t_wet, t_wet + 1.2, "sine"),
                                                    px=v.px, py=v.py))(ark_motion(t)))
    near_fr = [doc(PR.flood_sea(-80, SW + 80, NEAR_FINAL, phase=k / phases, bottom=SH + 60, storm=0.6, seed=9,
                                scale=0.9)) for k in range(phases)]
    sc.add("near_sea", near_fr, z=5, wc=0.6, frame_at=lambda t: float(int(t * 5 + 3) % phases),
           motion=lambda t: Tf(dy=near(t) - NEAR_FINAL))

    # ---------------- clouds (one soft lightning glow inside a cloud on the first 哗啦啦)
    t_fl = t_hua[0] + 0.05
    sc.add("back_clouds", back_clouds_svg(), z=0.5, wc=0.6, motion=lambda t: Tf(dx=12 * math.sin(t / 5.0), sx=1.03, sy=1.03, px=SW / 2, py=300))
    cl = [clouds_svg(), clouds_svg(1, 1.0)]
    sc.add("clouds", cl, z=6, wc=0.7,
           frame_at=lambda t: 1.0 - clamp(abs(t - t_fl - 0.12) / 0.35) if abs(t - t_fl - 0.12) < 0.35 else 0.0,
           motion=lambda t: Tf(dx=-22 * math.sin(t / 4.0), dy=3 * math.sin(t / 3.0), sx=1.03, sy=1.03, px=SW / 2,
                               py=300))
    sc.fx.append(FX.lightning([t_fl], dur=0.5, strength=0.22, color=(236, 240, 255)))

    # ---------------- the two single drops on 滴答 (falling, a splash on the roof)
    pts = PR.ark_points(AX, WL0, S9, 1, floating=True)
    roof = pts["roof"]
    hit = [(roof[0][0] + 150, roof[0][1] + 2), (roof[1][0] - 130, roof[1][1] + 2)]
    dsp = Spr(120, 140, 60, 100, wc=0.3, seed=21)
    dsp.add(f'<path d="{PR._raindrop_d(60, 100, 26)}" fill="{PR.RAIN_COL}" stroke="{S.shade(PR.RAIN_COL, -0.45)}" '
            f'stroke-width="3.2"/><ellipse cx="51" cy="88" rx="5" ry="9" fill="#fffaf0" opacity="0.85"/>')
    ssp = Spr(260, 160, 130, 110, wc=0.3, seed=22)
    for k in (1.3, 2.1, 2.7):
        ssp.add(splash_markup(130, 110, k))
    for i, (tb, (hx, hy)) in enumerate(zip(t_di, hit)):
        t0 = tb - 0.42

        def dstate(t, t0=t0, tb=tb, hx=hx, hy=hy):
            if t < t0 or t >= tb:
                return None
            u = (t - t0) / (tb - t0)
            y = hy - 620 * (1 - u) ** 1.6 - 6
            im, ax, ay = dsp.get(0, 1, 1 + 0.25 * u, 0)
            return im, (hx - ax, y - ay)

        def sstate(t, tb=tb, hx=hx, hy=hy):
            v = t - tb
            if v < 0 or v > 0.5:
                return None
            k = 0 if v < 0.06 else 1 if v < 0.2 else 2
            im, ax, ay = ssp.get(k, 1, 1, 0)
            a = 1 - clamp((v - 0.25) / 0.25)
            if a < 0.998:
                arr = np.asarray(im).copy()
                arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
                im = Image.fromarray(arr, "RGBA")
            return im, (hx - ax, hy - ay)
        sc.add_dynamic(f"drop{i}", dstate, z=4.5)
        sc.add_dynamic(f"splash{i}", sstate, z=4.6)
    # scattered single drops after 滴答, then the pouring rain
    drops = [doc(PR.rain(phase=k / 6, intensity=0.18, x0=0, y0=0, x1=SW, y1=SH, angle=8, seed=5, drops=True,
                         scale=0.8)) for k in range(6)]
    sc.add("drops", drops, z=7, wc=0.3, frame_at=lambda t: float(int(t * 14) % 6),
           motion=lambda t: Tf(alpha=(0.35 * M.progress(t, t_di[0] + 0.1, t_di[0] + 0.5, "sine") +
                                      0.65 * M.progress(t, t_di[1] + 0.05, t_hua[0], "sine")) *
                               (1 - M.progress(t, t_hua[0], t_hua[1] + 0.8, "sine"))))
    sc.fx.append(FX.rain(t0=t_hua[0] - 0.1, density=0.55, angle=12, length=44, speed=1500, alpha=95, seed=5))
    sc.fx.append(FX.rain(t0=t_hua[1] - 0.1, density=0.55, angle=14, length=56, speed=1800, alpha=105, seed=8))

    # ---------------- day counters
    add_seven(sc, t_seven, t_rain)
    add_forty(sc, t_40, t_40n, t_up[0])

    # ---------------- light
    # (the rainy gloom is painted into the backdrop colours: a full-frame multiply costs ~100 ms per frame)

    # ---------------- sound
    sc.sfx("storm_wind", 0.0, dur=T, gain_db=-24, fade_in=0.8, fade_out=1.0)
    for k, tb in enumerate(t_di):
        sc.sfx("drip", tb - 0.02, dur=0.5, gain_db=-10 + k, pan=-0.2 + 0.4 * k)
    sc.sfx("rain", t_di[0] + 0.2, dur=t_hua[0] - t_di[0], gain_db=-24, fade_in=0.4, fade_out=0.3)
    sc.sfx("rain", t_hua[0] - 0.1, dur=T - t_hua[0] + 0.1, gain_db=-14, fade_in=0.5, fade_out=1.0)
    sc.sfx("thunder", t_fl, gain_db=-17, pan=-0.3)
    sc.sfx("pop", t_40n + 0.15, gain_db=-12)
    sc.sfx("waves_storm", t_up[0] - 0.2, dur=T - t_up[0] + 0.2, gain_db=-19, fade_in=1.5, fade_out=1.0)
    for tu in t_up:
        sc.sfx("splash", tu, gain_db=-16, pan=0.2)
    sc.sfx("ship_creak", t_float - 0.1, dur=T - t_float + 0.1, gain_db=-20, fade_in=0.6, fade_out=1.0)
    return sc


# ============================================================================ counters
def add_seven(sc, t_seven, t_rain):
    """'七天以后': seven little suns pop into a row, one by one, then the row fades."""
    cx, cy = 960, 700
    sp = Spr(820, 200, 410, 100, wc=0.3, seed=31)
    for k in range(8):
        sp.add(PR.day_counter(410, 100, 1.45, n=7, filled=k, icons="sun", gap=64))
    t0, t1 = t_seven + 0.05, t_rain - 0.15
    t_out = t_rain + 1.2

    def st(t):
        if t < t0 - 0.3 or t > t_out + 0.45:
            return None
        k = int(clamp((t - t0) / max(0.2, t1 - t0)) * 7 + 0.999) if t >= t0 else 0
        a = M.progress(t, t0 - 0.3, t0, "sine") * (1 - M.progress(t, t_out, t_out + 0.45, "sine"))
        im, ax, ay = sp.get(min(7, k), 1, 1, 0)
        if a < 0.998:
            arr = np.asarray(im).copy()
            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
            im = Image.fromarray(arr, "RGBA")
        return im, (cx - ax, cy - ay)
    sc.add_dynamic("seven", st, z=30)


def plaque_markup(x, y):
    """A cream board for the day counter: a sun on the left, a moon on the right."""
    out = (f'<rect x="{x - 190}" y="{y - 70}" width="380" height="140" rx="40" fill="#fbf1dc" stroke="{INK}" '
           f'stroke-width="5"/>')
    out += PR._g(PR._sun_icon(26), f"translate({x - 130},{y})") + PR._g(PR._moon_icon(24), f"translate({x + 132},{y})")
    return S.g(out, filter="wobble-fine")


def add_forty(sc, t_40, t_40n, t_hide):
    """'四十天四十夜': a plaque counts the days 1 -> 40 and lands on 40 with a pop."""
    cx, cy = 930, 700
    psp = Spr(580, 260, 290, 130, wc=0.4, seed=33)
    psp.add(S.g(plaque_markup(0, 0), extra='transform="translate(290,130) scale(1.3)"'))
    nsp = Spr(240, 150, 120, 66, wc=0, seed=34)
    for n in range(1, 41):
        nsp.add(S.text(120, 100, str(n), size=100, fill="#d9893c",
                       extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
    t0, t1 = t_40 - 0.05, t_40n + 0.2
    t_out = t_hide - 0.1

    def frac(t):
        u = clamp((t - t0) / (t1 - t0))
        return 1 - (1 - u) ** 1.7

    def pa(t):
        return M.progress(t, t0 - 0.4, t0, "sine") * (1 - M.progress(t, t_out, t_out + 0.4, "sine"))

    def pst(t):
        a = pa(t)
        if a <= 0.002:
            return None
        k = 1 + 0.06 * math.exp(-max(0.0, t - t1) / 0.15) * (t >= t1)
        im, ax, ay = psp.get(0, k, k, 0)
        if a < 0.998:
            arr = np.asarray(im).copy()
            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
            im = Image.fromarray(arr, "RGBA")
        return im, (cx - ax, cy - ay)

    def nst(t):
        a = pa(t)
        if a <= 0.002:
            return None
        n = max(1, min(40, int(1 + frac(t) * 39.999)))
        pop = 1 + 0.35 * math.exp(-max(0.0, t - t1) / 0.12) * math.sin(min(math.pi, (t - t1) / 0.25 * math.pi)) \
            if t >= t1 else 1.0
        im, ax, ay = nsp.get(n - 1, pop, pop, 0)
        if a < 0.998:
            arr = np.asarray(im).copy()
            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
            im = Image.fromarray(arr, "RGBA")
        return im, (cx - ax, cy - ay)
    sc.add_dynamic("plaque", pst, z=30)
    sc.add_dynamic("plaque_n", nst, z=30.1)
