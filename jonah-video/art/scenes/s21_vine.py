"""Scene 21 — the castor plant (Jonah 4:6).

The dry knoll east of Nineveh (the city small on the western horizon, left), Jonah in his little booth
facing the city — the same place, booth and look as v1 s11 / s20. Every time comes from the narration
(ctx.lines[i].at(phrase) / .start / .end), never fixed numbers.

Line 0 "上帝安排了一棵蓖麻。" — a hot afternoon; Jonah sits in the booth, tired and sweaty. God's warm light
        (light only, never a figure) shines down beside the booth; a little golden seed floats down the beam,
        lands, and a sprout pops up (sparkles). Jonah notices it (hop).
        "一夜之间，蓖麻就长起来了，又高又大。" — the sun sinks behind the city and night falls (stars, crescent
        moon); Jonah yawns and lies down to sleep (z's); the castor plant grows in the night, glowing softly
        with God's light — one continuous drawing per video frame; dawn breaks in the east as it reaches its
        full height ("又高又大").
Line 1 "它宽宽的叶子，像一把绿色的大伞，" — Jonah wakes and stretches, then sees the plant (hop); the camera tilts
        up to the wide leaves arching over the booth like a green umbrella; doves fly by; Jonah is pleased.
        "替约拿挡住了火辣辣的太阳。" — the sun climbs and blazes (flame rays, hot sky, heat shimmer on the open
        sand), but the canopy holds a cool shade over the booth: the ground shade and a cool tint on Jonah
        settle in, sunlight only glints on the top leaves; Jonah closes his eyes in relief.
Line 2 "这下，约拿非常非常高兴！" — hop into a delighted pose (legs out, arms open), rocking happily with little
        music notes; the camera pushes in and the scene settles on a calm, sunny frame.

Notes for maintainers
* Reuses the approved v1 s11_vine techniques (helpers imported from art.scenes_v1.s11_vine): the castor plant
  is ONE drawing per video frame with whole-number flipbook indices (never two plants alpha-blended), each
  leaf keeps its full-grown spin while it grows; Jonah's pose changes are 1-frame cuts hidden by a
  squash-and-hop (+ dust poof); expression-only changes crossfade softly; the shade is a ground multiply
  ellipse plus a cool multiply tint of Jonah's own silhouette.
* Night: the plant grows DURING the night, so a silhouette-mask grade (v1) would not match the growing plant.
  Instead the whole frame gets one uniform night grade (multiply + small blue lift); the night sky layer is
  painted pre-compensated for it, and the stars, the moon and God's glow on the plant are drawn AFTER the
  grade (post-grade overlay fx), only in clear sky, so they stay bright.
* Camera: few long sine-eased moves inside the 2112 x 1188 stage.
"""
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as CH
from art import props as PR
from art import style as S
from art.scenes_v1 import s11_vine as V
from art.style import P, W, H
from engine import compositor as CO
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine import watercolor as WC
from engine.motion import Cam, Tf
from engine.paths import FPS
from engine.scene import BOIL_TOKEN, Scene

# ------------------------------------------------------------------ layout (stage px)
GY = 962            # ground line of the knoll (plant root, booth, Jonah)
SP = 1.3            # plant / booth / Jonah scale (as v1)
XP = 830            # castor root
XB = XP + PR.CASTOR_BOOTH_DX * SP   # booth centre (the canopy arches over its roof)
XJ = XB + 28        # Jonah sitting, facing the city (left)
XJS = XB + 62       # Jonah lying asleep (head on the left, toward the plant)
HORIZON = 640
LIZ = (1606, 950)   # lizard basking on its stone

SUN_A = (330, 300)      # hot afternoon sun (west, over the city)
SUN_SET = (300, 790)    # where it sinks (behind the city)
SUN_E = (1890, 790)     # dawn sun start (east, hidden behind the hills)
SUN_HOT = (1720, 330)   # noon sun, high beside the canopy (right)
S_H = 0.74              # noon sun scale (rays reach ~250 px)
MOON = (1765, 300)

# night grade: frame * NIGHT_MUL + NIGHT_ADD (uniform over the frame)
NIGHT_MUL = np.array([0.50, 0.56, 0.88])
NIGHT_ADD = np.array([8.0, 12.0, 32.0])

INK = P["ink"]
CX, CY = W // 2, H // 2


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


_env = V._env


def _night_pre(c):
    """Sky colour to paint so that it looks like ``c`` after the night grade."""
    r, g_, b = S.hex_rgb(c)
    v = (np.array([r, g_, b], float) - NIGHT_ADD) / NIGHT_MUL
    return S.rgb_hex(*np.clip(v, 0, 255))


def _at(line, phrases, default):
    for ph in phrases:
        try:
            return line.at(ph)
        except KeyError:
            pass
    return default


def _castor_svgs(states):
    """SVG docs of PR.castor_plant(XP, GY, SP, side=1, seed=2, **state) for each state, every leaf held at its
    full-grown spin (see the v1 s11_vine docstring: a newly born leaf re-rolls later leaves' spins)."""
    spins = {}
    orig = PR._palmate

    def palmate(cx, cy, r, lobes, spin, tilt, hang, fill, vein, wither=0.0, seed=0, sw=4.0):
        return orig(cx, cy, r, lobes, spins.setdefault(seed, spin), tilt, hang, fill, vein, wither, seed, sw)

    PR._palmate = palmate
    try:
        PR.castor_plant(XP, GY, SP, growth=1.0, side=1, seed=2)          # records every leaf's spin
        return [S.svg_doc(PR.castor_plant(XP, GY, SP, side=1, seed=2, **st)) for st in states]
    finally:
        PR._palmate = orig


def _sun_svg(r, col, glow, glow_r):
    return S.svg_doc(
        f'<circle cx="{CX}" cy="{CY}" r="{glow_r}" fill="url(#sg)"/>' +
        S.g(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{col}" stroke="{S.shade(col, -0.25)}" stroke-width="4"/>'
            f'<circle cx="{CX - r * 0.3:.0f}" cy="{CY - r * 0.3:.0f}" r="{r * 0.35:.0f}" fill="#fffaf0" opacity="0.35"/>',
            filter="wobble"),
        defs=S.rad_grad("sg", [(0, glow, 0.85), (0.35, glow, 0.35), (1, glow, 0)]))


def _flame_rays_svg():
    """v1 hot sun: opaque wavy flame rays + short wedges (drawn at the document centre)."""
    ray_d = ""
    for i in range(14):
        a = 2 * math.pi * i / 14
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for j in range(7):
            r = 150 + j * 32
            off = 14 * math.sin(j * 1.6) * (1 - j / 7)
            w_ = 26 * (1 - j / 7) + 3
            pts.append((r, off, w_))
        left = [(CX + r * ca - (off - w_) * sa, CY + r * sa + (off - w_) * ca) for r, off, w_ in pts]
        right = [(CX + r * ca - (off + w_) * sa, CY + r * sa + (off + w_) * ca) for r, off, w_ in pts]
        ray_d += S.smooth_path(left + right[::-1], closed=True, tension=0.8) + " "
    short = S.rays(CX, CY, 120, 215, n=14, width_deg=11, rot=12.9)
    return S.svg_doc(S.g(
        f'<path d="{short}" fill="#ffd34d" stroke="#b9621c" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="{ray_d}" fill="#ffb83a" stroke="#b9621c" stroke-width="4.5" stroke-linejoin="round"/>',
        filter="wobble"))


def _hot_disc_svg():
    return S.svg_doc(
        f'<circle cx="{CX}" cy="{CY}" r="185" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{CX}" cy="{CY}" r="118" fill="#ffd94f" stroke="#c9741f" stroke-width="6"/>'
            f'<circle cx="{CX}" cy="{CY}" r="90" fill="#fff1a8"/>'
            f'<circle cx="{CX}" cy="{CY}" r="58" fill="#fffae0"/>'
            f'<circle cx="{CX - 34}" cy="{CY - 34}" r="26" fill="#fffef6" opacity="0.9"/>', filter="wobble"),
        defs=S.rad_grad("hg", [(0, "#fffef4", 1), (0.6, "#fff6cf", 0.85), (0.8, "#ffeaa0", 0.4), (1, "#ffe08a", 0)]))


def _zed(x, y, s):
    d = f"M{x - s / 2:.1f},{y - s / 2:.1f} h{s:.1f} l{-s:.1f},{s:.1f} h{s:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{s * 0.34 + 6:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#e9eefc" stroke-width="{s * 0.34:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _note(x, y, s, col):
    """A little music note (eighth note) with ink outline and a soft cream halo; (x, y) = centre of its head."""
    stem_d = (f"M{x + 11 * s:.1f},{y - 2 * s:.1f} L{x + 11 * s:.1f},{y - 52 * s:.1f} q{4 * s:.1f},{14 * s:.1f} "
              f"{20 * s:.1f},{20 * s:.1f} q{6 * s:.1f},{6 * s:.1f} {2 * s:.1f},{16 * s:.1f}")
    ell = (f'cx="{x:.1f}" cy="{y:.1f}" rx="{13 * s:.1f}" ry="{9.5 * s:.1f}" '
           f'transform="rotate(-24 {x:.1f} {y:.1f})"')
    halo = (f'<path d="{stem_d}" fill="none" stroke="#fff6dc" stroke-width="{14 * s:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0.75"/><ellipse {ell} fill="#fff6dc" stroke="#fff6dc" '
            f'stroke-width="{10 * s:.1f}" opacity="0.75"/>')
    head = f'<ellipse {ell} fill="{col}" stroke="{INK}" stroke-width="{3.6 * s:.1f}"/>'
    stem = (f'<path d="{stem_d}" fill="none" stroke="{INK}" stroke-width="{4.2 * s:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')
    return S.g(halo + stem + head, filter="wobble-fine")


def _seed_svg(x, y):
    return S.svg_doc(
        f'<circle cx="{x}" cy="{y}" r="70" fill="url(#sgl)"/>' +
        S.g(f'<ellipse cx="{x}" cy="{y}" rx="19" ry="13" fill="#d9a23c" stroke="{INK}" stroke-width="3.6" '
            f'transform="rotate(-30 {x} {y})"/>'
            f'<path d="M{x - 12},{y + 4} q12,-3 22,-14" fill="none" stroke="#a8742a" stroke-width="2.6" '
            f'stroke-linecap="round"/>'
            f'<ellipse cx="{x - 6}" cy="{y - 5}" rx="6" ry="3.4" fill="#fff4cf" transform="rotate(-30 {x} {y})"/>',
            filter="wobble-fine"),
        defs=S.rad_grad("sgl", [(0, "#fff6cf", 1.0), (0.35, "#ffe9a0", 0.6), (1, "#ffe08a", 0)]))


def _glow_pm(R=320, col=(255, 220, 140)):
    yy, xx = np.mgrid[0:2 * R, 0:2 * R].astype(np.float32)
    r = np.sqrt((xx - R) ** 2 + (yy - R) ** 2) / R
    a = np.clip(1 - r, 0, 1) ** 1.8
    pm = np.zeros((2 * R, 2 * R, 4), np.uint8)
    for c in range(3):
        pm[..., c] = (a * col[c]).astype(np.uint8)
    pm[..., 3] = (a * 255).astype(np.uint8)
    return pm


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    def find(*keys):
        for ln in L:
            if any(k in ln.text for k in keys):
                return ln
        return None

    l0 = L[0]
    l1 = find("叶子", "大伞", "挡住", "太阳") or L[min(1, len(L) - 1)]
    l2 = find("高兴", "喜乐") or L[-1]
    c0 = l0.chunks[0] if l0.chunks else l0

    # --- key times (all from the narration) -------------------------------------------------------
    t_beam0 = l0.start + 0.1                        # God's light shines beside the booth
    t_seed0 = l0.start + 0.3                        # a golden seed floats down the beam
    t_land = c0.start + 0.55 * (c0.end - c0.start)  # ... lands ("…一棵蓖麻")
    t_pop = t_land + 0.08                           # the sprout pops up
    t_notice = t_pop + 0.45                         # Jonah notices it
    t_n0 = _at(l0, ["一夜之间"], l0.start + 0.35 * (l0.end - l0.start))   # dusk begins ("一夜之间")
    t_tw = t_n0 + 0.55                              # violet twilight (between sunset and night)
    t_n1 = t_n0 + 1.0                               # full night
    t_yawn = t_n0 + 0.15
    t_sleep = t_yawn + 0.65                         # lies down to sleep
    t_g0 = t_n0 + 0.55                              # the plant grows in the night ...
    t_g1 = max(t_g0 + 2.2, l0.end - 0.4)            # ... to its full height on "又高又大"
    t_d0 = t_g1 - 0.35                              # dawn breaks
    t_d1 = t_d0 + 0.9
    t_wake = max(t_d0 + 0.6, l0.end + 0.1)          # wakes up and stretches
    t_look = max(t_wake + 0.95, l1.start + 0.45)    # sees the big plant ("它宽宽的叶子")
    t_glad = t_look + 1.3                           # pleased
    t_morning = t_d1 + 1.6                          # dawn sky has become a clear morning sky
    t_hot0 = _at(l1, ["挡住", "太阳"], l1.start + 0.5 * (l1.end - l1.start))   # "替约拿挡住了火辣辣的太阳"
    t_relief = t_hot0 + 0.95                        # eyes closed: cool shade
    t_happy = max(l2.start + 0.45, t_relief + 1.0)  # "这下，约拿非常非常高兴！"
    t_calm = min(T - 1.1, l2.end + 0.3)             # rocking settles for the dissolve

    # =============================================================== SKY (day / hot / gold / night / dawn)
    sky_h = 665
    a_hot = lambda t: (1 - M.progress(t, t_n0 + 0.4, t_n0 + 0.5)) + M.progress(t, t_hot0 - 0.1, t_hot0 + 0.7, "sine")
    a_gold = lambda t: _env(t, t_n0 - 0.05, t_n0 + 0.35, t_tw - 0.05, t_tw)
    a_tw = lambda t: _env(t, t_n0 + 0.25, t_tw, t_n1 - 0.05, t_n1)
    a_night = lambda t: _env(t, t_tw - 0.05, t_n1, t_d1 - 0.05, t_d1 + 0.05)
    a_dawn = lambda t: _env(t, t_d0, t_d1, t_morning - 1.2, t_morning)

    def covered(t):
        return max(min(1.0, a_hot(t)), a_gold(t), a_tw(t), a_night(t), a_dawn(t)) >= 0.999

    sc.add("sky_day", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>',
        defs=S.lin_grad("g", [(0, "#8fc4dc"), (0.5, "#c9e3df"), (0.82, "#f4e2b8"), (1, "#f6dcab")])),
        wc=0.5, motion=lambda t: Tf(alpha=0.0 if covered(t) else 1.0))
    sc.add("sky_hot", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>',
        defs=S.lin_grad("g", [(0, "#9cc8d6"), (0.45, "#e3e2bc"), (0.8, "#f6dca4"), (1, "#f8dca8")])),
        wc=0.5, motion=lambda t: Tf(alpha=min(1.0, a_hot(t)) * (0.0 if max(a_gold(t), a_tw(t), a_night(t)) >= 0.999 else 1.0)))
    sc.add("sky_gold", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_SET[0]}" cy="{HORIZON}" rx="900" ry="330" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#a98fb8"), (0.45, "#f0b98a"), (0.8, "#f8cf8c"), (1, "#fbdc9c")]) +
        S.rad_grad("r", [(0, "#ffe9a8", 0.9), (0.5, "#fbc77a", 0.4), (1, "#f3a873", 0)])),
        wc=0.5, motion=lambda t: Tf(alpha=a_gold(t)))
    sc.add("sky_twilight", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_SET[0]}" cy="{HORIZON}" rx="800" ry="260" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#5e5a9c"), (0.45, "#9a77ac"), (0.82, "#de9a98"), (1, "#eeb08e")]) +
        S.rad_grad("r", [(0, "#ffd9a0", 0.8), (0.5, "#f6b48c", 0.35), (1, "#e89a90", 0)])),
        wc=0.5, motion=lambda t: Tf(alpha=a_tw(t)))
    sc.add("sky_night", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>',
        defs=S.lin_grad("g", [(0, _night_pre("#1f2b4c")), (0.55, _night_pre("#34466e")),
                              (1, _night_pre("#5f6896"))])),
        wc=0.4, motion=lambda t: Tf(alpha=a_night(t)))
    sc.add("sky_dawn", S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="900" ry="360" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#b3b0da"), (0.45, "#e8c4cc"), (0.8, "#f8d6aa"), (1, "#f9ddb0")]) +
        S.rad_grad("r", [(0, "#fff0c4", 0.9), (0.5, "#fcd3a0", 0.45), (1, "#f6c7a0", 0)])),
        wc=0.5, motion=lambda t: Tf(alpha=a_dawn(t)))

    # --- suns (drawn at the document centre, moved into place) --------------------------------------
    def at(pos, m=None):
        base = lambda t: Tf(dx=pos[0] - CX, dy=pos[1] - CY)
        return M.combine(base, m) if m else base

    rays = _flame_rays_svg()
    hot = _hot_disc_svg()
    S_A = 0.62          # the afternoon sun is a little smaller (lower and further west)
    a_sunA = lambda t: 1 - M.progress(t, t_n0 - 0.05, t_n0 + 0.35, "sine")
    sc.add("sunA_rays", rays, wc=0.3, motion=at(SUN_A, M.combine(
        lambda t: Tf(rot=7 * t, px=CX, py=CY), M.breathe(0.03, 1.1, pivot=(CX, CY)),
        lambda t: Tf(sx=S_A, sy=S_A, px=CX, py=CY, alpha=a_sunA(t)))))
    sc.add("sunA_disc", hot, wc=0.4, motion=at(SUN_A, M.combine(
        M.breathe(0.03, 1.4, pivot=(CX, CY)), lambda t: Tf(sx=S_A, sy=S_A, px=CX, py=CY, alpha=a_sunA(t)))))
    sink = M.keys([(t_n0 - 0.1, {"dx": 0, "dy": 0}), (t_tw + 0.2, {"dx": SUN_SET[0] - SUN_A[0],
                                                                     "dy": SUN_SET[1] - SUN_A[1]})], "in")
    sc.add("sun_set", _sun_svg(74, "#f59a52", "#ffd08a", 320), wc=0.4, motion=at(SUN_A, M.combine(
        sink, lambda t: Tf(alpha=_env(t, t_n0 - 0.1, t_n0 + 0.3, t_tw + 0.1, t_tw + 0.25)))))

    S_HOT = 118 * S_H / 82   # the dawn disc grows to exactly the noon disc as it arrives
    climb = M.keys([(t_d0, {"dx": 0, "dy": 0}), (t_d1, {"dx": -10, "dy": -225}),
                    (t_hot0 - 0.2, {"dx": -110, "dy": -380}),
                    (t_hot0 + 0.5, {"dx": SUN_HOT[0] - SUN_E[0], "dy": SUN_HOT[1] - SUN_E[1], "s": S_HOT})],
                   ["out", "linear", "inout"], pivot=(CX, CY))
    sc.add("sun_dawn", _sun_svg(82, "#f8c070", "#ffe0b0", 330), wc=0.5, motion=at(SUN_E, M.combine(
        climb, lambda t: Tf(alpha=_env(t, t_d0, t_d0 + 0.3, t_hot0 + 0.45, t_hot0 + 0.75)))))
    sc.add("sun_rays", rays, wc=0.3, motion=at(SUN_HOT, M.combine(
        lambda t: Tf(rot=8 * t, px=CX, py=CY), M.breathe(0.03, 0.9, pivot=(CX, CY)),
        lambda t: Tf(sx=S_H * (0.45 + 0.55 * M.progress(t, t_hot0 + 0.05, t_hot0 + 0.6, "back")),
                     sy=S_H * (0.45 + 0.55 * M.progress(t, t_hot0 + 0.05, t_hot0 + 0.6, "back")),
                     px=CX, py=CY, alpha=M.progress(t, t_hot0 + 0.05, t_hot0 + 0.35, "sine")))))
    sc.add("sun_hot", hot, wc=0.4, motion=at(SUN_HOT, M.combine(
        M.breathe(0.035, 1.3, pivot=(CX, CY)),
        lambda t: Tf(sx=S_H, sy=S_H, px=CX, py=CY, alpha=M.progress(t, t_hot0 + 0.25, t_hot0 + 0.65, "sine")))))

    # --- clouds: drift; they fade into the dark at night (stars are drawn only in clear sky) ----------
    clouds = S.svg_doc(S.g(
        S.cloud(640, 108, 250, 78, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
        S.cloud(1250, 92, 250, 76, "#fdf1e2", seed=5, sw=3, shade_fill="#f0d6c4"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=M.combine(
        M.drift(vx=-6), lambda t: Tf(alpha=1 - _env(t, t_n0 + 0.1, t_n1 - 0.1, t_d0, t_d1 + 0.3))))

    # =============================================================== LAND (static, flattened) — v1 layout
    far = ""
    far += S.path(S.smooth_path([(-80, HORIZON + 8), (150, 600), (420, 585), (700, 610), (950, 590),
                                 (1250, 560), (1550, 585), (1850, 570), (2200, 600)], closed=False) +
                  f" L{W + 80},{HORIZON + 30} L-80,{HORIZON + 30} Z", fill="#e3d3c0", sw=3)
    far += S.path(S.smooth_path([(1000, HORIZON + 6), (1300, 612), (1600, 598), (1900, 615), (2200, 605)],
                                closed=False) + f" L{W + 80},{HORIZON + 30} L1000,{HORIZON + 30} Z", fill="#dfcbb0", sw=3)
    sc.add("far_hills", S.svg_doc(S.g(far, filter="wobble")), wc=0.7)
    sc.add("city", S.svg_doc(PR.nineveh_skyline(20, 560, HORIZON + 4, scale=0.42, seed=2, haze=0.42,
                                                tint="#efdcbc")), wc=0.6)

    plain = S.path(f"M-80,{HORIZON} L{W + 80},{HORIZON} L{W + 80},{H + 80} L-80,{H + 80} Z", fill="url(#pl)", sw=0)
    plain += f'<path d="M-80,{HORIZON + 2} L{W + 80},{HORIZON + 2}" stroke="{INK}" stroke-width="3" opacity="0.55"/>'
    for i in range(26):
        x = (i * 263) % 2100 + 20
        y = HORIZON + 14 + (i * 37) % 60
        plain += f'<ellipse cx="{x}" cy="{y}" rx="{9 + i % 4}" ry="5" fill="#b7a274" opacity="0.6"/>'
    plain += V._dune([(-80, 742), (200, 718), (480, 734), (760, 786), (980, 856), (1150, 932), (1270, 1010)], "da",
                     rim="#f6e2b4")
    path_d = S.smooth_path([(470, 724), (520, 760), (470, 812), (600, 880), (720, 960), (640, 960), (520, 885),
                            (410, 812), (468, 760), (440, 726)])
    plain += f'<path d="{path_d}" fill="#f5e2b6" opacity="0.85"/>'
    plain += V._dune([(960, 1020), (1100, 930), (1300, 836), (1550, 760), (1800, 726), (2000, 718), (2200, 732)],
                     "db", rim="#f6e0ae")
    defs = (S.lin_grad("pl", [(0, "#efdfb6"), (0.3, "#ead19f"), (1, "#e0bb82")]) +
            S.lin_grad("da", [(0, "#eed4a0"), (0.4, "#e6c48c"), (1, "#d8ad72")]) +
            S.lin_grad("db", [(0, "#ecd09a"), (0.4, "#e3bf86"), (1, "#d4a86c")]))
    sc.add("plain", S.svg_doc(S.g(plain, filter="wobble"), defs=defs), wc=0.8)

    mid = ""
    for (x, y, s, v) in [(260, 740, 0.4, 2), (640, 772, 0.42, 2), (1600, 768, 0.45, 2), (1880, 742, 0.4, 2),
                         (130, 760, 0.32, 2), (1010, 884, 0.38, 2)]:
        mid += PR.bush(x, y, s, variant=v)
    for (x, y, s) in [(1950, 728, 0.3), (2050, 734, 0.24)]:
        mid += PR.palm_tree(x, y, s, lean=-0.2)
    for (x, y, s) in [(318, 796, 0.42), (1668, 866, 0.5), (1452, 905, 0.42), (950, 838, 0.36)]:
        mid += PR.grass_tuft(x, y, s, variant=1)
    for (x, y, w_, h_, sd) in [(1712, 866, 128, 64, 3), (1792, 872, 62, 34, 13), (1650, 874, 30, 16, 23),
                               (370, 794, 86, 42, 6), (424, 800, 40, 22, 16),
                               (1380, 906, 70, 36, 4), (1426, 910, 34, 17, 14),
                               (905, 842, 46, 24, 7)]:
        mid += V._stone(x, y, w_, h_, seed=sd, sw=3, crack=(w_ > 100))
    sc.add("mid", S.svg_doc(mid), wc=0.8)

    knoll_pts = [(-80, 1035), (200, 1010), (480, 980), (760, 964), (1100, 959), (1450, 962), (1700, 954),
                 (1920, 930), (2200, 905)]
    kd = S.smooth_path(knoll_pts, closed=False) + f" L{W + 80},{H + 80} L-80,{H + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4)
    rp = [(x, y + 16) for x, y in knoll_pts[1:-1]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f0cf95" stroke-width="14" opacity="0.5"/>'
    for (x, y) in [(260, 1050), (1660, 1040), (1960, 1000), (1000, 1035), (760, 1080)]:
        knoll += (f'<path d="M{x - 70},{y} q70,-16 140,0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.45" stroke-linecap="round"/>')
    for (x, y, s_, sd) in [(400, 1012, 70, 1), (640, 990, 50, 2), (1520, 1012, 60, 3), (1870, 990, 55, 4),
                           (1090, 1040, 46, 5)]:
        knoll += V._cracks(x, y, s_, seed=sd)
    sc.add("knoll", S.svg_doc(S.g(knoll, filter="wobble"),
                              defs=S.lin_grad("kn", [(0, "#e6bc7c"), (0.3, "#dcab69"), (1, "#c38c55")])), wc=0.9)
    pebbles = (V._pebbles(470, 1000, 1.0, seed=3) + V._pebbles(1790, 996, 1.1, seed=4, n=2) +
               V._pebbles(640, 986, 0.8, seed=5, n=2) + V._pebbles(1460, 1016, 0.9, seed=6, n=2))
    sc.add("pebbles", S.svg_doc(S.g(pebbles, filter="wobble-fine")), wc=0.8)
    sc.add("liz_rock", S.svg_doc(S.g(V._stone(LIZ[0] - 4, 994, 138, 50, seed=41, sw=4, crack=True),
                                     filter="wobble-fine")), wc=0.8)

    # =============================================================== DOVES fly by in the morning (behind the plant)
    dove_frames = [S.svg_doc(PR.dove(1900, 330, 0.62, -1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    for i, (t0, dy, ph) in enumerate([(l1.start + 0.2, 0, 0), (l1.start + 0.55, 70, 2)]):
        dur = 3.0
        sc.add(f"dove{i}", dove_frames, frame_at=flap(10, ph), wc=0.4, motion=M.combine(
            M.keys([(t0, {"dx": 330, "dy": dy - 30}), (t0 + dur, {"dx": -2200, "dy": dy - 110})], "linear"),
            M.bob(10, 0.6, ph * 0.1)))

    # =============================================================== LIZARD (basks; hot feet; runs into the shade)
    LIZ_TO = (1478, 970)                       # its new spot in the canopy's shade

    def liz_svg(legs, facing):
        body = V._lizard(LIZ[0], LIZ[1], 0.82, legs=legs)
        if facing < 0:
            body = f'<g transform="translate({2 * LIZ[0]},0) scale(-1,1)">{body}</g>'
        return S.svg_doc(body)

    liz_frames = [liz_svg(0, 1), liz_svg(0, -1), liz_svg(1, -1)]
    t_liz_hot = t_hot0 + 1.2                   # hot feet on the sun-baked stone
    t_liz = t_hot0 + 1.75                      # turns and scurries into the shade
    LIZ_RUN = 0.6

    def liz_frame(t):
        if t < t_liz:
            return 0.0
        if t < t_liz + LIZ_RUN:
            return 1.0 + float(int((t - t_liz) * 16) % 2)
        return 1.0

    def liz_motion(t):
        if t_n0 < t < t_d1:
            return Tf()
        if t < t_liz_hot:
            u = (t + 0.9) % 2.8                # lizard "push-ups"
            b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
            return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)
        if t < t_liz:                          # hot feet: quick little hops
            u = t - t_liz_hot
            return Tf(dy=-9 * abs(math.sin(u * 2 * math.pi * 3.2)), rot=4 * math.sin(u * 2 * math.pi * 3.2),
                      px=LIZ[0], py=LIZ[1])
        u = _clamp((t - t_liz) / LIZ_RUN)
        dx = (LIZ_TO[0] - LIZ[0]) * M.ease("out")(u)
        dy = (LIZ_TO[1] - LIZ[1]) * u - 16 * math.sin(math.pi * min(1.0, u * 1.6))
        if t > t_liz + LIZ_RUN:                # happy slow push-ups in the cool shade
            v = (t - t_liz - LIZ_RUN) % 2.2
            b = abs(math.sin(math.pi * v / 0.25)) if v < 0.5 else 0.0
            return Tf(dx=dx, dy=dy, sx=1 - 0.03 * b, sy=1 + 0.1 * b, px=LIZ[0], py=LIZ[1] + 2)
        return Tf(dx=dx, dy=dy)

    sc.add("lizard", liz_frames, frame_at=liz_frame, motion=liz_motion, wc=0.5)
    sc.add("liz_rock2", S.svg_doc(S.g(V._stone(LIZ[0] + 150, 1002, 104, 58, seed=43, sw=4), filter="wobble-fine")),
           wc=0.8)

    # =============================================================== GOD'S LIGHT beside the booth (light only)
    beam = S.svg_doc(
        S.g(f'<path d="M{XP - 150},-60 L{XP + 120},-60 L{XP + 150},{GY + 10} L{XP - 160},{GY + 10} Z" fill="url(#bg)"/>',
            filter="blur-md") +
        S.g(f'<path d="M{XP - 45},-60 L{XP + 25},-60 L{XP + 35},{GY} L{XP - 45},{GY} Z" fill="#fff8de" '
            f'opacity="0.55"/>', filter="blur-md") +
        f'<ellipse cx="{XP}" cy="{GY - 40}" rx="300" ry="170" fill="url(#rg)"/>',
        defs=S.lin_grad("bg", [(0, "#fff4c8", 0.1), (0.3, "#ffeaa8", 0.5), (1, "#ffe08a", 0.78)]) +
        S.rad_grad("rg", [(0, "#fff8dc", 0.95), (0.45, "#ffeaa8", 0.5), (1, "#ffe08a", 0)]))
    sc.add("god_light", beam, wc=0,
           motion=lambda t: Tf(alpha=_env(t, t_beam0 - 0.1, t_beam0 + 0.5, t_n0 + 0.1, t_n1) *
                               (0.88 + 0.12 * math.sin(t * 4))))

    # booth (with its own thin shade) + soft contact shadow
    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{INK}" opacity="0.14" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1, shade=True))
    sc.add("booth", S.svg_doc(booth), wc=0.8)

    # =============================================================== CANOPY SHADE (ground) + sun flecks
    shade_amt = lambda t: (0.3 * M.progress(t, t_d1, t_d1 + 1.5, "sine") +
                           0.7 * M.progress(t, t_hot0 + 0.55, t_hot0 + 1.2, "sine"))
    blobs = [(640, 976, 110, 24), (760, 970, 140, 28), (900, 968, 150, 30), (1050, 970, 160, 32),
             (1210, 972, 170, 32), (1360, 974, 140, 28), (1470, 978, 100, 22)]
    flecks = [(712, 978, 20, 6), (845, 966, 16, 5), (985, 984, 22, 6), (1150, 990, 18, 5), (1318, 984, 22, 6),
              (1435, 972, 14, 4), (560, 984, 14, 4)]
    pool = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#6c6898"/>' for x, y, rx, ry in blobs)
    holes = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="black"/>' for x, y, rx, ry in flecks)
    def gshade(pool_op, wash_op):
        return S.svg_doc(
            f'<mask id="fl" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>{holes}</mask>'
            f'<g mask="url(#fl)"><g opacity="{pool_op}" filter="url(#soft)">{pool}</g></g>'
            f'<ellipse cx="{XP + 380}" cy="{GY - 150}" rx="330" ry="200" fill="#a79fc4" opacity="{wash_op}" '
            f'filter="url(#blur-md)"/>')

    sh0, sh1 = t_hot0 + 0.15, t_hot0 + 1.35     # the noon shade spreads from the stem over the booth
    # weak morning shade; retired (cost) once the stronger noon shade has spread over it
    sc.add("ground_shade_am", gshade(0.62, 0.4), wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=0.3 * M.progress(t, t_d1, t_d1 + 1.5, "sine") *
                               (1 - M.progress(t, sh1, sh1 + 0.6, "sine"))))
    sc.add("ground_shade", gshade(0.72, 0.46), wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=0.0 if t < sh0 else 1.0),
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, sh0, sh1, "sine"), "soft": 160})

    # =============================================================== CASTOR PLANT (one exact drawing per video frame)
    def gcurve(u):
        return (0.5 - 0.5 * math.cos(math.pi * u)) ** 0.55

    k0 = math.floor(t_g0 * FPS)
    k1 = math.ceil(t_g1 * FPS)
    g_vals = [gcurve(_clamp((k / FPS - t_g0) / (t_g1 - t_g0))) for k in range(k0, k1 + 1)]
    plant_frames, plant_ids, seen = [], [], {}
    for svg in _castor_svgs([dict(growth=round(g, 4)) for g in g_vals]):
        if svg not in seen:
            seen[svg] = len(plant_frames)
            plant_frames.append(svg)
        plant_ids.append(seen[svg])

    def plant_frame(t):
        return float(plant_ids[min(max(round(t * FPS) - k0, 0), len(plant_ids) - 1)])

    def plant_growth(t):
        return gcurve(_clamp((t - t_g0) / (t_g1 - t_g0)))

    def plant_motion(t):
        a = M.progress(t, t_pop - 0.05, t_pop + 0.12, "sine")
        s = 0.35 + 0.65 * M.progress(t, t_pop - 0.05, t_pop + 0.35, "back")
        rot = 0.6 * math.sin(2 * math.pi * t / 3.4)
        # a morning breeze rustles the wide leaves as they are described ("它宽宽的叶子")
        br = _env(t, l1.start, l1.start + 0.8, t_hot0 - 1.0, t_hot0)
        rot += br * (0.6 * math.sin(2 * math.pi * t / 1.5) + 0.25 * math.sin(t * 7.3))
        return Tf(rot=rot, sx=s, sy=s, alpha=a, px=XP, py=GY)

    sc.add("castor", plant_frames, frame_at=plant_frame, motion=plant_motion, wc=0.9)

    # the golden seed floating down the beam
    sx0, sy0 = XP - 20, 150
    seed_svg = _seed_svg(XP, GY - 10)

    def seed_motion(t):
        if t < t_seed0 or t > t_pop + 0.3:
            return Tf(alpha=0.0)
        u = _clamp((t - t_seed0) / (t_land - t_seed0))
        e = M.ease("sine")(u)
        dx = (sx0 - XP) * (1 - e) + 46 * math.sin(u * 6.5) * (1 - u)
        dy = (sy0 - (GY - 10)) * (1 - e)
        a = M.progress(t, t_seed0, t_seed0 + 0.25, "sine") * (1 - M.progress(t, t_pop, t_pop + 0.25, "sine"))
        sq = 1 - 0.5 * M.progress(t, t_land, t_pop + 0.2, "sine")
        return Tf(dx=dx, dy=dy, rot=40 * math.sin(u * 5), sx=1 / max(sq, 0.5) ** 0.3, sy=sq, alpha=a,
                  px=XP, py=GY - 10)

    sc.add("seed", seed_svg, motion=seed_motion, wc=0.2)

    # earth crumbs popping as the sprout breaks the ground
    crumbs = ""
    for dx, dy, r in ((-34, -8, 7), (30, -10, 6), (-16, -20, 5), (18, -24, 5), (44, -2, 5), (-46, -1, 5)):
        crumbs += f'<circle cx="{XP + dx}" cy="{GY + dy}" r="{r}" fill="{P["earth"]}" stroke="{INK}" stroke-width="2.4"/>'

    def crumb_motion(t):
        u = t - t_pop
        if u < 0 or u > 0.5:
            return Tf(alpha=0.0)
        s = 0.6 + 0.8 * M.ease("out")(u / 0.5)
        return Tf(dy=-26 * math.sin(math.pi * u / 0.5), sx=s, sy=s, alpha=1 - M.progress(u, 0.25, 0.5),
                  px=XP, py=GY)

    sc.add("crumbs", S.svg_doc(S.g(crumbs, filter="wobble-fine")), motion=crumb_motion, wc=0.3)

    # =============================================================== JONAH (flipbook of poses)
    # (pose, expr, x, facing, shadow width)
    poses = [("sit", "tired", XJ, -1, 210), ("sit", "surprised", XJ, -1, 210), ("sit", "sleepy", XJ, -1, 210),
             ("sleep", None, XJS, 1, 330), ("wake", None, XJ, -1, 220), ("sit", "surprised", XJ, -1, 210),
             ("sit", "happy", XJ, -1, 210), ("sit", "peaceful", XJ, -1, 210), ("sit_happy", "happy", XJ, -1, 250)]

    def jdraw(p, e, x, f):
        return CH.jonah(x, GY, SP, f, pose=p, expr=e, marks=(p != "sleep"))

    jframes = [S.svg_doc(CH.ground_shadow(x, GY, SP, width=sw_, opacity=0.25) + jdraw(p, e, x, f))
               for p, e, x, f, sw_ in poses]
    # (time, kind, hop strength, pop lines, dust poof)
    switch = [(t_notice, "pose", 0.7, True, False),     # tired -> surprised (notices the sprout)
              (t_yawn, "pose", 0.35, False, False),     # -> big yawn
              (t_sleep, "pose", 0.6, False, True),      # -> lies down to sleep
              (t_wake, "pose", 0.8, False, True),       # -> wakes and stretches at dawn
              (t_look, "pose", 0.9, True, True),        # -> sees the big plant
              (t_glad, "expr", 0, False, False),        # surprised -> happy
              (t_relief, "expr", 0, False, False),      # happy -> peaceful (cool shade)
              (t_happy, "pose", 1.0, True, True)]       # -> delighted, arms open

    def jonah_frame(t):
        f = 0.0
        for i, (ts, kind, *_r) in enumerate(switch):
            if kind == "pose":
                if t >= ts:
                    f = float(i + 1)
            elif t >= ts:
                f = i + M.progress(t, ts, ts + 0.22, "sine")
        return f

    def hop(t):
        sy, dy = 1.0, 0.0
        for ts, kind, amp, *_r in switch:
            if kind != "pose":
                continue
            u = t - ts
            if -0.09 <= u <= 0.17:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.17, "sine")
                dy = -14 * amp * math.sin(math.pi * _clamp((u + 0.01) / 0.18))
        return sy, dy

    def jonah_motion(t):
        s = 1 + 0.012 * math.sin(2 * math.pi * t / 3.0)
        sy, rot, dy = s, 0.0, 0.0
        px = XJ
        if t < t_notice:                       # hot: quick shallow panting
            sy *= 1 + 0.012 * math.sin(2 * math.pi * t / 0.75)
        if t_yawn <= t < t_sleep:              # the yawn: a slow stretch up
            sy *= 1 + 0.03 * math.sin(math.pi * _clamp((t - t_yawn) / (t_sleep - t_yawn)))
        if t_sleep <= t < t_wake:              # asleep: slow deep breaths
            px = XJS
            sy = 1 + 0.02 * math.sin(2 * math.pi * (t - t_sleep) / 2.4)
            s = 1.0
        if t_relief <= t < t_happy:            # a big relieved sigh, then calm breathing
            u = t - t_relief
            sy *= 1 + 0.025 * math.sin(math.pi * _clamp(u / 1.4))
        if t >= t_happy:                       # happy rocking, settling for the dissolve
            k = M.progress(t, t_happy, t_happy + 0.4) * (1 - 0.6 * M.progress(t, t_calm - 0.6, t_calm + 0.4))
            rot = k * 1.8 * math.sin(2 * math.pi * (t - t_happy) / 1.1)
            dy = -k * 5 * abs(math.sin(2 * math.pi * (t - t_happy) / 1.1))
        hsy, hdy = hop(t)
        sy *= hsy
        sx = s * (1 + 0.5 * (1 - hsy))
        return Tf(dy=dy + hdy, rot=rot, sx=sx, sy=sy, px=px, py=GY)

    sc.add("jonah", jframes, frame_at=jonah_frame, motion=jonah_motion, wc=0.6)

    # canopy shade ON JONAH ONLY: a cool flat-colour copy of his own silhouette, multiplied
    tint_frames = [S.svg_doc(S.g(jdraw(p, e, x, f), filter="flat"), defs=V.FLAT_DEFS) for p, e, x, f, _w in poses]
    sc.add("jonah_shade", tint_frames, frame_at=jonah_frame, wc=0, blend="multiply",
           motion=M.combine(jonah_motion, lambda t: Tf(alpha=0.46 * shade_amt(t))))

    # --- pose-change pop: dust poofs + emphasis lines --------------------------------------------------
    dust_svg = ""
    for bx, sgn in ((XJ - 178, -1), (XJ + 168, 1)):
        circ = [(0, 0, 17), (sgn * 20, -6, 13), (-sgn * 16, -4, 12), (sgn * 4, -16, 12)]
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{GY - 6 + dy}" r="{r}" fill="#f3e4c4" stroke="{P["ink_soft"]}" '
                            f'stroke-width="6"/>' for dx, dy, r in circ)
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{GY - 6 + dy}" r="{r}" fill="#f3e4c4"/>' for dx, dy, r in circ)
    dust_ts = [ts for ts, kind, _a, _l, dust in switch if kind == "pose" and dust]

    def poof_motion(t):
        for ts in dust_ts:
            u = t - ts
            if 0 <= u < 0.45:
                s = 0.5 + 0.7 * M.ease("out")(u / 0.45)
                return Tf(dy=-6 * M.ease("out")(u / 0.45), sx=s, sy=s,
                          alpha=0.9 * (1 - M.progress(u, 0.12, 0.45, "sine")), px=XJ, py=GY)
        return Tf(alpha=0.0)

    sc.add("jpop_dust", S.svg_doc(S.g(dust_svg, filter="wobble-fine")), motion=poof_motion, wc=0.3)

    lines_svg = ""
    for k in range(5):
        a = math.radians(-160 + k * 35)
        r0, r1 = 96, 132
        lines_svg += (f'<path d="M{CX + r0 * math.cos(a):.1f},{CY + r0 * math.sin(a):.1f} '
                      f'L{CX + r1 * math.cos(a):.1f},{CY + r1 * math.sin(a):.1f}" stroke="{P["ink_soft"]}" '
                      f'stroke-width="7" stroke-linecap="round"/>')
    pop_pts = []
    for i, (ts, kind, _a, lines, _d) in enumerate(switch):
        if lines:
            p, e, x, f, _w = poses[i + 1]
            pop_pts.append((ts, CH.body_points(CH.jonah, x, GY, SP, f, pose=p)["head"]))

    def lines_motion(t):
        for ts, (px_, py_) in pop_pts:
            u = t - ts
            if 0 <= u < 0.34:
                s = 0.82 + 0.3 * M.ease("out")(u / 0.34)
                return Tf(dx=px_ - CX, dy=py_ - CY, sx=s, sy=s,
                          alpha=1 - M.progress(u, 0.12, 0.34, "sine"), px=CX, py=CY)
        return Tf(alpha=0.0)

    sc.add("jpop_lines", S.svg_doc(S.g(lines_svg, filter="wobble-fine")), motion=lines_motion, wc=0.2)

    # --- z's rising from the sleeper ------------------------------------------------------------------
    zh = CH.body_points(CH.jonah, XJS, GY, SP, 1, pose="sleep")["head"]
    zx, zy = zh[0] + 20, zh[1] - 70
    for i, s_ in enumerate((26, 34, 42)):
        def z_motion(t, i=i):
            if t < t_sleep + 0.3 or t > t_wake:
                return Tf(alpha=0.0)
            u = ((t - t_sleep - 0.3 - i * 0.5) % 1.5) / 1.5
            if t - t_sleep - 0.3 < i * 0.5:
                return Tf(alpha=0.0)
            k = 1 - M.progress(t, t_wake - 0.3, t_wake)
            return Tf(dx=-30 * u + 10 * math.sin(u * 6), dy=-95 * u, alpha=k * math.sin(math.pi * u) ** 0.7,
                      sx=0.7 + 0.4 * u, sy=0.7 + 0.4 * u, px=zx, py=zy)
        sc.add(f"zed{i}", S.svg_doc(S.g(_zed(zx, zy, s_), filter="wobble-fine")), motion=z_motion, wc=0.2)

    # --- happy music notes ---------------------------------------------------------------------------
    hh = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit_happy")["head"]
    for i, (ox, oy, col, s_) in enumerate(((-120, -40, "#3b8b89", 1.6), (115, -60, "#e0a03a", 1.4),
                                           (-30, -150, "#c9714a", 1.5))):
        nx, ny = hh[0] + ox, hh[1] + oy

        def note_motion(t, i=i, nx=nx, ny=ny):
            t0 = t_happy + 0.25 + i * 0.45
            if t < t0:
                return Tf(alpha=0.0)
            u = ((t - t0) % 1.6) / 1.6
            fade = 1 - M.progress(t, t_calm - 0.8, t_calm)
            return Tf(dx=18 * math.sin(u * 5 + i), dy=-110 * u, rot=12 * math.sin(u * 6 + i),
                      alpha=fade * math.sin(math.pi * u) ** 0.6, sx=0.8 + 0.3 * u, sy=0.8 + 0.3 * u, px=nx, py=ny)
        sc.add(f"note{i}", S.svg_doc(_note(nx, ny, s_, col)), motion=note_motion, wc=0.3)

    # =============================================================== FOREGROUND (static rocks + swaying grass)
    fg = ""
    fg += V._rock(150, 1160, 290, 130, seed=31) + V._rock(360, 1180, 160, 72, seed=32)
    fg += V._rock(1960, 1165, 250, 115, seed=33) + V._rock(1790, 1185, 140, 64, seed=34)
    fg += V._stone(40, 925, 150, 84, seed=35, sw=4) + PR.bush(92, 912, 1.2, variant=2)
    fg += PR.bush(2072, 1062, 1.05, variant=2)
    sc.add("fg_rocks", S.svg_doc(S.g(fg, filter="wobble")), wc=0.9)

    def grass_frame_fn(ph):
        return lambda t: 1 + 0.7 * math.sin(2 * math.pi * (t / 2.6 + ph))

    for gi, tufts in enumerate([[(40, 1115, 1.15, 1), (265, 1105, 0.95, 1), (450, 1160, 1.0, 0)],
                                [(1720, 1140, 1.0, 1), (1870, 1108, 0.95, 1)],
                                [(560, 1000, 0.65, 1), (196, 928, 0.8, 1)],
                                [(1520, 990, 0.65, 1), (1700, 985, 0.6, 1)]]):
        frames = [S.svg_doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts))
                  for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", frames, frame_at=grass_frame_fn(gi * 0.23), wc=0.7)

    # =============================================================== CAMERA
    sc.camera = M.cam_keys([
        (0.0, Cam(1075, 600, 1960)),
        (t_beam0 + 0.1, Cam(1072, 598, 1956)),
        (t_notice + 0.1, Cam(1012, 638, 1770)),        # closer: the seed lands, the sprout pops
        (t_n0 + 0.2, Cam(1010, 640, 1762)),
        (t_g0 + 1.7, Cam(1050, 592, 1960)),            # back out as night falls and the plant shoots up
        (t_g1, Cam(1052, 592, 1960)),
        (l1.start + 0.2, Cam(1052, 592, 1960)),
        (t_hot0 - 0.3, Cam(1072, 540, 1720)),          # tilt up to the umbrella of leaves
        (t_hot0 + 1.7, Cam(1150, 648, 1880)),          # ... back to show the blazing sun and the shade
        (l2.start + 0.1, Cam(1152, 646, 1870)),
        (t_calm, Cam(1176, 618, 1580)),                # push in on the happy Jonah
        (T, Cam(1178, 619, 1570)),
    ], "sine")

    # =============================================================== FX
    k_night = lambda t: _env(t, t_tw - 0.05, t_n1, t_d0, t_d1)

    def grade(frame, t, view):
        mul = np.array([1.0, 1.0, 1.0])
        add = np.zeros(3)
        k_hot = 0.5 * (1 - M.progress(t, t_n0, t_n0 + 0.5, "sine")) + \
            0.55 * M.progress(t, t_hot0 + 0.1, t_hot0 + 0.9, "sine")
        for col, k in [((255, 224, 184), k_hot),
                       ((255, 206, 160), _env(t, t_n0 - 0.05, t_n0 + 0.35, t_n0 + 0.45, t_tw + 0.1)),
                       ((236, 204, 226), 0.6 * _env(t, t_n0 + 0.3, t_tw, t_tw + 0.1, t_n1)),
                       ((246, 220, 230), 0.8 * _env(t, t_d0, t_d1, t_d1 + 0.5, t_morning))]:
            if k > 0:
                mul *= 1 - (1 - np.array(col, float) / 255.0) * k
        kn = k_night(t)
        if kn > 0:
            mul *= 1 - (1 - NIGHT_MUL) * kn
            add = NIGHT_ADD * kn
        if (mul >= 0.998).all() and kn <= 0.003:
            return frame
        arr = cv2.multiply(np.asarray(frame), (float(mul[0]), float(mul[1]), float(mul[2]), 1.0))
        if kn > 0:
            arr = cv2.add(arr, (float(add[0]), float(add[1]), float(add[2]), 0.0))
        return Image.fromarray(arr, "RGBA")

    # --- post-grade night overlay: stars, moon and God's glow on the growing plant ------------------
    rng = np.random.default_rng(4)
    stars = []
    while len(stars) < 46:
        x, y = rng.uniform(30, W - 30), rng.uniform(30, 560)
        if 500 < x < 1530 and y > 110:            # the full-grown canopy
            continue
        if x < 640 and y > 400:                   # the city skyline
            continue
        if math.hypot(x - MOON[0], y - MOON[1]) < 120:
            continue
        stars.append((x, y, rng.uniform(4, 10), rng.uniform(0, 1), rng.uniform(1.2, 2.4)))

    moon_svg = S.svg_doc(
        f'<circle cx="{MOON[0] - 15}" cy="{MOON[1]}" r="170" fill="url(#mh)"/>' + S.g(
            f'<path d="M{MOON[0]},{MOON[1] - 55} A55,55 0 1 1 {MOON[0]},{MOON[1] + 55} '
            f'A42,55 0 1 0 {MOON[0]},{MOON[1] - 55} Z" fill="#fbf1cf" stroke="{INK}" stroke-width="3"/>',
            filter="wobble-fine"),
        defs=S.rad_grad("mh", [(0, "#fbf1cf", 0.5), (0.3, "#f3ead0", 0.24), (0.65, "#c9c9dc", 0.07),
                               (1, "#a9aecb", 0)]))
    moon_im = WC.watercolor(raster.rasterize(moon_svg.replace(BOIL_TOKEN, "1"), W, H), seed=77, strength=0.4)
    mbb = moon_im.getchannel("A").getbbox()
    moon_pm = CO.to_pm(moon_im.crop(mbb))
    glow = _glow_pm()
    GR = glow.shape[0] / 2

    def night_overlay(frame, t, view):
        kn = k_night(t)
        kg = _env(t, t_g0 - 0.3, t_g0 + 0.3, t_g1, t_d1 + 0.3)
        if kn <= 0.01 and kg <= 0.01:
            return frame
        arr = np.array(frame.convert("RGB"))
        if kg > 0.01:     # God's warm glow around the growing plant (screen)
            g = plant_growth(t)
            hgt = PR.castor_height(g) * SP
            cy = GY - 0.55 * hgt - 20
            r = 150 + 0.75 * hgt
            Mx = view.M @ CO._T(XP + 0.18 * hgt - r, cy - r) @ CO._S(r / GR, r / GR)
            CO.draw_image(arr, glow, Mx, 0.5 * kg * (0.9 + 0.1 * math.sin(t * 5)), "screen")
        if kn > 0.01:
            CO.draw_image(arr, moon_pm, view.M @ CO._T(mbb[0], mbb[1]), kn ** 1.5)
        im = Image.fromarray(arr).convert("RGBA")
        if kn > 0.01:
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            for x, y, r0, ph, per in stars:
                tw = 0.55 + 0.45 * math.sin(2 * math.pi * (t / per + ph))
                ox, oy = view.to_out(x, y)
                r = r0 * view.scale * (0.75 + 0.25 * tw)
                a = int(235 * kn ** 1.5 * tw)
                w_ = r * 0.26
                d.ellipse([ox - r * 0.5, oy - r * 0.5, ox + r * 0.5, oy + r * 0.5], fill=(255, 246, 210, a // 4))
                d.polygon([(ox, oy - r), (ox + w_, oy - w_), (ox + r, oy), (ox + w_, oy + w_), (ox, oy + r),
                           (ox - w_, oy + w_), (ox - r, oy), (ox - w_, oy - w_)], fill=(255, 248, 214, a))
            im.alpha_composite(ov)
        return im

    def shimmer(frame, t, view):
        k = 0.7 * (1 - M.progress(t, t_n0 - 0.2, t_n0 + 0.3, "sine")) + \
            M.progress(t, t_hot0 + 0.3, t_hot0 + 1.1, "sine")
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i, (bx, by) in enumerate([(300, 930), (1600, 900), (1880, 870), (420, 860), (1790, 1030), (180, 1060)]):
            u = ((t * 0.6 + i * 0.37) % 1.0)
            ox, oy = view.to_out(bx, by - 70 * u)
            a = int(150 * k * math.sin(math.pi * u))
            sc_ = view.scale
            for j in range(3):
                x0 = ox + (j - 1) * 20 * sc_
                pts = [(x0 + 7 * sc_ * math.sin(q * 1.1 + t * 7 + i), oy - q * 9 * sc_) for q in range(9)]
                d.line(pts, fill=(255, 248, 226, a), width=max(2, int(4 * sc_)), joint="curve")
        frame.alpha_composite(ov)
        return frame

    sc.fx = [
        grade,
        night_overlay,
        # God's sparkles around the plant column and (once it has grown) above the canopy, never on Jonah
        FX.sparkles((XP - 300, GY - 760, XP + 190, GY - 20), count=24, t0=t_beam0 + 0.2, t1=t_d1 + 0.2,
                    color=(255, 238, 160), size=(10, 24), period=1.3, drift=-10, seed=3),
        FX.sparkles((XP + 190, GY - 860, XP + 650, GY - 520), count=10, t0=t_g0 + 1.4, t1=t_d1 + 0.2,
                    color=(255, 238, 160), size=(10, 22), period=1.4, drift=-8, seed=5),
        FX.sparkles((XP - 200, GY - 830, XP + 640, GY - 560), count=9, t0=t_hot0 + 0.4, t1=T + 1,
                    color=(255, 250, 220), size=(8, 16), period=1.7, drift=0, seed=21),
        FX.motes((200, 200, 1900, 900), count=24, t0=t_d1, t1=T + 1, color=(255, 246, 214), alpha=100),
        shimmer,
    ]

    # =============================================================== SOUND
    sc.sfx("heat", 0, dur=t_n0 + 0.6, gain_db=-15, fade_in=0.8, fade_out=0.6)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_beam0, gain_db=-9)
    sc.sfx("sparkle", t_land - 0.1, gain_db=-11)
    sc.sfx("pop", t_pop, gain_db=-9)
    sc.sfx("night", t_n0 + 0.3, dur=t_d1 - t_n0, gain_db=-14, fade_in=0.5, fade_out=0.6)
    sc.sfx("grow", t_g0, gain_db=-7)
    sc.sfx("sparkle", t_g1 - 0.3, gain_db=-12, pan=0.2)
    sc.sfx("snore", t_sleep + 0.4, dur=t_wake - t_sleep - 0.4, gain_db=-18, fade_in=0.3, fade_out=0.3)
    sc.sfx("rooster", l0.end - 0.05, gain_db=-13, pan=-0.5)
    sc.sfx("birds", t_d1, dur=T - t_d1 + 0.8, gain_db=-16, fade_in=0.6, fade_out=0.8, pan=-0.2)
    sc.sfx("heat", t_hot0, dur=T - t_hot0 + 0.8, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("sparkle", t_happy, gain_db=-12)
    return sc
