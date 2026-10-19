"""Scene 3 — the valley of Elah (1 Samuel 17:1-3): Israel's camp on the hill on the left, the Philistine camp on the
hill on the right, a valley with a little brook between.

One wide 2640 x 1485 stage: props.valley_elah (camps=False) as the static backdrop, a morning sky, our own tents
(with waving banners / pennants) and small soldiers on the two plateaus (valley_points / valley_ground), so they
can move. s05_forty reuses this stage (see the shared helpers below).

Beats (keyed to the narration chunks):
  start        calm wide establishing frame, doves gliding, clouds drifting, banners waving
  line 0       "很久以前，" -> slow push-in over the whole valley
               "以色列人和非利士人要打仗了。" -> a horn sounds; on both hills the soldiers stand ready (a little
               squash-dip down each line), spear tips glint, the flags flap harder
  line 1       "以色列人站在这边的山上，" -> the camera eases left; warm light on the left hill; the Israelites
               (blue tunics, blue banners) bob up one after another
               "非利士人站在那边的山上，" -> the camera eases right; light on the right hill; the Philistines (reed
               crowns, red pennants) bob up one after another
               "中间隔着一道山谷。" -> the camera settles back to the middle and down; a soft light runs along the
               valley floor and the brook sparkles
  end          calm wide hold (page dip to s04)
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]
SW, SH = 3000, 1485
VX0, VX1, VY, VS = 300, 2700, 1130, 1.25      # valley_elah placement (the stage edges are filled by valley_svg)
VBOT = VY + 320 * VS
FS = 0.58                                     # figure scale (soldiers, Goliath) on this stage
ISR_TENTS = ((400, 0.48), (650, 0.42))
PHI_TENTS = ((2350, 0.42), (2600, 0.48))
ISR_MEN = (350, 442, 534, 626, 718)            # soldier x on the left plateau (facing right)
PHI_MEN = (2280, 2372, 2464, 2556, 2648)       # on the right plateau (facing left)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def ground(x):
    return PR.valley_ground(x, VX0, VX1, VY, VS)


# ================================================================== shared drawings (also used by s05_forty)


def sky_svg(kind="morning"):
    if kind == "morning":
        stops = [(0, "#8cc3dc"), (0.5, "#b9dde6"), (0.85, "#e6eed8"), (1, "#f3e8c8")]
    elif kind == "dawn":
        stops = [(0, "#9fa8d4"), (0.45, "#e2bccd"), (0.8, "#f7d3a8"), (1, "#fbe6b8")]
    elif kind == "evening":
        stops = [(0, "#5b5a92"), (0.45, "#b0789a"), (0.8, "#ee9c72"), (1, "#f6c487")]
    else:   # night
        stops = [(0, "#1f2b4a"), (0.6, "#33466e"), (1, "#4f5f86")]
    defs = S.lin_grad(f"v3sky{kind}", stops)
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{VY + 40}" fill="url(#v3sky{kind})"/>', defs)


def clouds_svg(tint="#fbf6ec", shade_fill="#d6e6ee", seed=0):
    b = (S.cloud(560, 260, 420, 130, tint, seed=51 + seed, sw=3.5, shade_fill=shade_fill) +
         S.cloud(1430, 170, 360, 112, tint, seed=52 + seed, sw=3.5, shade_fill=shade_fill) +
         S.cloud(2230, 300, 460, 140, tint, seed=53 + seed, sw=3.5, shade_fill=shade_fill) +
         S.cloud(2950, 160, 300, 96, tint, seed=54 + seed, sw=3, shade_fill=shade_fill) +
         S.cloud(-60, 200, 300, 96, tint, seed=55 + seed, sw=3, shade_fill=shade_fill))
    return doc(S.g(b, filter="wobble"))


def valley_svg():
    """valley_elah, plus the plateaus continued out to the stage edges (same gradient, same top line)."""
    W_ = VX1 - VX0
    strips, defs = "", ""
    for side, xa, xb, ua, ub in ((-1, -30, VX0 - 0.04 * W_ + 55, -0.04, 0.46), (1, VX1 + 0.04 * W_ - 55, SW + 30, 0.54, 1.04)):
        top = min(ground(VX0 + W_ * (ua + (ub - ua) * i / 60)) for i in range(61))
        gid = f"v3ext{side + 1}"
        defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{top:.1f}" x2="0" '
                 f'y2="{VBOT:.1f}"><stop offset="0" stop-color="#b8cf7a"/><stop offset="0.5" stop-color="#9cbb5e"/>'
                 f'<stop offset="1" stop-color="#7fa24a"/></linearGradient>')
        pts = [(xa + (xb - xa) * i / 12, ground(xa + (xb - xa) * i / 12)) for i in range(13)]
        line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        strips += f'<path d="{line} L{xb:.1f},{VBOT + 40} L{xa:.1f},{VBOT + 40} Z" fill="url(#{gid})"/>'
        strips += f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="{4 * VS}" stroke-linecap="round"/>'
    xa, xb = VX0 - 0.04 * W_ + 45, VX1 + 0.04 * W_ - 45
    defs += f'<clipPath id="v3vc"><rect x="{xa:.0f}" y="-50" width="{xb - xa:.0f}" height="{SH + 100}"/></clipPath>'
    return doc(S.g(PR.valley_elah(VX0, VX1, VY, VS, camps=False), extra='clip-path="url(#v3vc)"') +
               S.g(strips, filter="wobble"), defs)


def tents_svg(wave):
    out = ""
    for x, s in ISR_TENTS:
        out += PR.tent(x, ground(x) - 4, s, 1, side="israel", wave=wave)
    for x, s in PHI_TENTS:
        out += PR.tent(x, ground(x) - 4, s, -1, side="philistine", wave=wave)
    return doc(out)


def soldier_svg(x, side, variant, pose="stand", facing=None, shake=0.0, expr=None, spear=None):
    f = facing if facing is not None else (1 if side == "israel" else -1)
    y = ground(x) + 6
    return doc(C.ground_shadow(x, y, FS, 120, 0.2) +
               C.soldier(x, y, FS, f, side=side, variant=variant, pose=pose, shake=shake, expr=expr, spear=spear))


def glow_svg(cx, cy, rx, ry, gid, col="#fff1c4"):
    defs = S.rad_grad(gid, [(0, col, 0.9), (0.5, col, 0.45), (1, col, 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>', defs)


def tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((240, 1480, 1.3, 2), (480, 1470, 1.0, 0), (800, 1485, 1.1, 2), (2230, 1485, 1.1, 0),
                       (2510, 1470, 1.2, 2), (2770, 1485, 1.3, 1), (360, 1320, 0.8, 0), (2650, 1330, 0.8, 0)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


def dove_layers(sc, y0, x_start, speed, scale, t0=0.0, n=2, name="dove"):
    ref = (1000, 600)
    frames = [doc(PR.dove(ref[0], ref[1], scale, 1 if speed > 0 else -1, wing=w))
              for w in (1.0, 0.4, -0.5, -1.0, -0.4, 0.3)]
    for i in range(n):
        def path(t, i=i):
            x = x_start + speed * (t - t0) - 90 * i * (1 if speed > 0 else -1)
            return Tf(dx=x - ref[0], dy=y0 + 40 * i - ref[1] - 16 * math.sin(1.6 * t + i))
        sc.add(f"{name}{i}", frames, wc=0.5, motion=path,
               frame_at=lambda t, i=i: float(int(t * 10 + 3 * i) % 6) if (t + i) % 2.4 < 1.4 else 0.0)


def cam_path(keys):
    """keys [(t, Cam, bump)]: sine-eased moves between key cameras; ``bump`` widens the view by that many px in the
    middle of the move starting at that key (sin^2 profile), which keeps long pans calm on screen."""
    def c(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, bump), (t1, b, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                v = (t - t0) / (t1 - t0)
                w = a.w + (b.w - a.w) * u + bump * math.sin(math.pi * v) ** 2
                x = a.x + (b.x - a.x) * u
                y = a.y + (b.y - a.y) * u
                hw, hh = w / 2, w * 9 / 32
                x = min(max(x, hw), SW - hw)
                y = min(max(y, hh), SH - hh)
                return Cam(x, y, w)
    return c


def hop_m(times, s=1.0, h=16.0, pivot=None):
    """Additive little hops (squash on take-off and landing) at the given times."""
    def m(t):
        dy, sy = 0.0, 1.0
        for t0 in times:
            u = t - t0
            if -0.1 <= u < 0:
                k = (u + 0.1) / 0.1
                dy += 3 * s * k
                sy *= 1 - 0.05 * k
            elif 0 <= u < 0.34:
                v = u / 0.34
                dy += -h * s * math.sin(math.pi * v) + 3 * s * (1 - v) * (v < 0.15)
                sy *= 1 + 0.03 * math.sin(math.pi * v)
            elif 0.34 <= u < 0.46:
                k = math.sin(math.pi * (u - 0.34) / 0.12)
                sy *= 1 - 0.04 * k
        return Tf(dy=dy, sy=sy, px=pivot[0] if pivot else None, py=pivot[1] if pivot else None)
    return m


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines
    t_war = L0.at("要打仗了")
    c1 = L1.at("以色列人站在")
    c2 = L1.at("非利士人站在")
    c3 = L1.at("中间隔着")

    sc.add("sky", sky_svg("morning"), wc=0.6)
    sc.add("sun_glow", glow_svg(600, 180, 700, 420, "v3sg", "#fff6d8"), wc=0, motion=M.pulse(0.75, 0.95, 4.0))
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=10))
    dove_layers(sc, 330, 0, 120, 0.42)
    sc.add("valley", valley_svg())
    sc.add("tents", [tents_svg(w) for w in (0.0, 0.33, 0.66)],
           frame_at=lambda t: float(int(t / (0.16 if t > t_war else 0.28)) % 3))

    # soldiers: idle breathing; a ready-dip on "要打仗了"; a hop wave when their hill is named
    for side, xs, t_wave in (("israel", ISR_MEN, c1), ("philistine", PHI_MEN, c2)):
        for i, x in enumerate(xs):
            y = ground(x) + 6
            piv = (x, y)
            order = i if side == "israel" else len(xs) - 1 - i
            sc.add(f"{side}{i}", soldier_svg(x, side, i), seed=60 + i + (10 if side == "philistine" else 0),
                   motion=M.combine(M.breathe(0.015, 2.6, pivot=piv, phase=i * 0.21),
                                    hop_m([t_war + 0.35 + 0.06 * order], FS, 6, piv),
                                    hop_m([t_wave + 0.35 + 0.14 * order], FS, 30, piv)))

    # highlights (warm light on the named hill / the valley)
    def hl(t0, t1):
        return lambda t: Tf(alpha=0.8 * M.progress(t, t0, t0 + 0.6, "sine") * (1 - M.progress(t, t1, t1 + 0.7, "sine")))
    sc.add("hl_isr", glow_svg(540, 700, 520, 300, "v3h1"), wc=0, blend="screen", motion=hl(c1 + 0.05, c2))
    sc.add("hl_phi", glow_svg(2470, 715, 520, 300, "v3h2"), wc=0, blend="screen", motion=hl(c2 + 0.05, c3))
    sc.add("hl_val", glow_svg(1500, 1150, 380, 300, "v3h3", "#fff6dc"), wc=0, blend="screen",
           motion=hl(c3 + 0.05, T + 5))
    sc.add("tufts", [tufts_svg(k) for k in range(3)], frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.55) % 4]))

    # camera: wide establishing push, pan left (with a slight pull-back mid-move), pan right, settle on the middle
    keys = [
        (0.0, Cam(1500, 742, 2636), 0),
        (c1 - 0.15, Cam(1500, 730, 2420), 0),
        (c1 + 1.5, Cam(870, 680, 1640), 0),
        (c2 - 0.1, Cam(860, 678, 1620), 300),
        (c2 + 1.75, Cam(2130, 685, 1640), 0),
        (c3 - 0.1, Cam(2140, 687, 1620), 250),
        (c3 + 1.6, Cam(1500, 812, 2260), 0),
        (T, Cam(1500, 822, 2190), 0),
    ]
    sc.camera = cam_path(keys)

    sc.fx = [
        FX.sparkles((1430, 1180, 1600, 1470), count=12, t0=c3 + 0.2, color=(240, 252, 255), size=(7, 14),
                    period=1.4, drift=0, seed=31),
        FX.sparkles((320, 360, 740, 480), count=5, t0=t_war + 0.3, t1=t_war + 2.4, color=(255, 246, 214),
                    size=(6, 11), period=1.1, drift=0, seed=32),
        FX.sparkles((2250, 370, 2680, 490), count=5, t0=t_war + 0.3, t1=t_war + 2.4, color=(255, 246, 214),
                    size=(6, 11), period=1.1, drift=0, seed=33),
        FX.motes((0, 500, SW, 1300), count=22, color=(255, 246, 214), size=(2, 5), alpha=100, seed=34),
    ]

    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("horn", t_war + 0.25, gain_db=-12)
    sc.sfx("crowd", c1 + 0.2, dur=1.6, gain_db=-21, pan=-0.6, fade_in=0.3, fade_out=0.6)
    sc.sfx("crowd", c2 + 0.2, dur=1.6, gain_db=-21, pan=0.6, fade_in=0.3, fade_out=0.6)
    sc.sfx("sparkle", c3 + 0.3, gain_db=-17)
    return sc
