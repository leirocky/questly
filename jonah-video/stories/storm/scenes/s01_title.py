"""Scene 1 - title page: the little Galilean fishing boat with its square sail glides over a calm violet-gold lake at
sunset; Jesus sits at the stern with his friends around him (John waves to us, Peter holds the sail rope); far away
on the left, dark clouds gather over the hills - a hint of what is coming. Book title.

Beats (keyed to ctx.lines[0] '圣经绘本：耶稣平静风浪。'; phrase / syllable onsets are measured in the voice clip with the
Noah film's voice_marks helpers (fallback: proportions of the subtitle chunk), so a re-generated voice stays in sync):
  start        calm frame (the film fades in over it): the water shimmers, the sail breathes, the boat rocks gently,
               a dove glides across, the far dark clouds creep and swell, two little sailing boats drift far away
  ~1.0 s       John (near row) lifts his hand and waves to us from then on (pose cut hidden by a squash dip)
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime)
  '耶稣平静风浪' the six title characters pop in one by one on their syllables (pop)
  '风浪'        the far clouds darken and swell a little more, a faint glow flickers inside them, a far rumble
  end          calm hold with a slow push-in. s02_wind opens with a plain cross-dissolve on this very page: it calls
               title_page(..., toff) so its first second is exactly this scene's last second.

Shared with s02_wind / s15_end (same illustrator): ugrad(), compose(), zoom_about(), boxed(), iris_reveal(), the
evening-lake water drawing and the title helpers.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import load_story
from engine.scene import Scene
from stories.noah.scenes.s01_title import (char_times, cuts, dip, f1, heart_markup, mark, snap,  # noqa: F401
                                           title_char_svg, voice_marks)

INK = P["ink"]
CREAM = "#fff6e3"

LAKE_S, LAKE_Y = 0.6, 800                  # lake_galilee scale and (virtual) near shoreline
HZ = LAKE_Y - 250 * LAKE_S                 # the far shoreline = the horizon of the water (650)
SUN_X = 0.86
SUN = (W * SUN_X, HZ - 330 * LAKE_S)       # (1816, 452)
BX, BY, BS = 960, 962, 0.48               # the fishing boat: waterline anchor and scale (people at the same scale)
TITLE_Y, TITLE_SIZE, TITLE_STEP = 408, 160, 190
RIB_X, RIB_Y = W / 2, 160
TITLE_COLS = ("#fcd987", "#f2ae4c", "#d77f34")
WATER_STOPS = [(0.0, "#f7cf92"), (0.10, "#eeb08e"), (0.32, "#b98aa6"), (0.62, "#7d6ca2"), (1.0, "#4b4783")]
NPH = 6                                    # water shimmer frames

for _e in ("warm", "happy", "kind", "smile", "worried", "amazed", "awed", "peaceful"):
    C.EXPRS.setdefault(f"st_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def blink(expr):
    return f"st_blink_{expr}"


# ================================================================== shared helpers (s02 / s15 import these)

def ugrad(gid, y0, y1, stops, x0=0, x1=0):
    """A linear gradient in absolute stage coordinates (userSpaceOnUse), so split layers keep matching colours."""
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a[0] if a else 1}"/>' for o, c, *a in stops)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" x2="{x1}" '
            f'y2="{y1}">{s}</linearGradient>')


def tf_point(tf, x, y):
    """Where a layer transform sends stage point (x, y) (the pivot must be explicit)."""
    px, py = tf.px, tf.py
    r = math.radians(tf.rot)
    ux, uy = (x - px) * tf.sx, (y - py) * tf.sy
    return (px + tf.dx + ux * math.cos(r) - uy * math.sin(r), py + tf.dy + ux * math.sin(r) + uy * math.cos(r))


def compose(outer, inner):
    """outer(inner(p)) as one Tf with inner's pivot (exact at the pivot; exact everywhere for uniform scales)."""
    if inner.px is None:
        inner = Tf(inner.dx, inner.dy, inner.rot, inner.sx, inner.sy, inner.alpha, outer.px or 0.0, outer.py or 0.0)
    if outer.px is None:
        outer = Tf(outer.dx, outer.dy, outer.rot, outer.sx, outer.sy, outer.alpha, inner.px, inner.py)
    qx, qy = tf_point(outer, inner.px + inner.dx, inner.py + inner.dy)
    return Tf(qx - inner.px, qy - inner.py, outer.rot + inner.rot, outer.sx * inner.sx, outer.sy * inner.sy,
              outer.alpha * inner.alpha, inner.px, inner.py)


def zoom_about(k, P_):
    return Tf(sx=k, sy=k, px=P_[0], py=P_[1])


def boxed(body, box, defs="", w=W, h=H):
    """A layer document whose rasterised crop is exactly ``box`` (x0, y0, x1, y1): two nearly invisible dots mark
    the corners, so reveal masks (computed on the crop) can be expressed in stage coordinates."""
    x0, y0, x1, y1 = box
    dots = (f'<rect x="{x0}" y="{y0}" width="4" height="4" fill="#fffaf0" opacity="0.02"/>'
            f'<rect x="{x1 - 4}" y="{y1 - 4}" width="4" height="4" fill="#fffaf0" opacity="0.02"/>')
    return S.svg_doc(body + dots, defs, w, h)


def iris_reveal(box, cx, cy, radius_fn, soft=90):
    """Radial reveal of a boxed layer: everything within radius_fn(t) stage px of (cx, cy) is visible. cx / cy may
    be functions of t (the iris centre in the layer's own, untransformed coordinates when the layer moves)."""
    x0, y0, x1, y1 = box

    def rv(t):
        r = radius_fn(t)
        if r is None:
            return {"mode": "up", "frac": 1.0}
        x = cx(t) if callable(cx) else cx
        y = cy(t) if callable(cy) else cy
        maxd = max(math.hypot(x - x0, y - y0), math.hypot(x1 - x, y - y0), math.hypot(x - x0, y1 - y),
                   math.hypot(x1 - x, y1 - y))
        return {"mode": "radial", "frac": r / maxd, "soft": soft, "cx": x, "cy": y}
    return rv


def loop_fa(period, n):
    """frame_at for an n-frame shimmer flipbook whose frame list ends with a copy of frame 0 (smooth crossfades)."""
    return lambda t: (t / period) % n


def evening_water(gid, y0, y1, x0=-30, x1=W + 30, stops=None, hz=HZ):
    """The violet-gold evening lake body (gradient from the horizon hz to the stage bottom) from y0 down to y1."""
    stops = stops or WATER_STOPS
    defs = ugrad(gid, hz, H, stops)
    return f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#{gid})"/>', defs


def water_ripples(k, n, rng_seed, y_top, y_bot, sun_x=None, avoid=(), x0=0, x1=W, count=70, lite="#ffe6b0",
                  lav="#d9c8ec", glitter=1.0):
    """Shimmer frame k of n: short light ripple strokes (perspective: short / thin near the horizon) whose opacity
    breathes with k, plus the sun's broken glitter path under sun_x. ``avoid`` = boxes to keep clear (hulls)."""
    rng = random.Random(rng_seed)
    out = ""
    for i in range(count):
        u = rng.random()
        yy = y_top + 8 + (y_bot - y_top) * u ** 1.5
        L = 18 + 120 * u
        xx = rng.uniform(x0 - 40, x1 + 40)
        ph = rng.random()
        a = (0.25 + 0.45 * u) * (0.5 + 0.5 * math.cos(2 * math.pi * (k / n + ph)))
        if any(bx0 < xx + L and xx < bx1 and by0 < yy < by1 for bx0, by0, bx1, by1 in avoid):
            continue
        col = lite if rng.random() < 0.55 else lav
        out += (f'<path d="M{f1(xx)},{f1(yy)} q{f1(L / 2)},{f1(-2 - 2 * u)} {f1(L)},0" stroke="{col}" '
                f'stroke-width="{f1(2 + 2.6 * u)}" fill="none" stroke-linecap="round" opacity="{a:.2f}"/>')
    if sun_x is not None and glitter > 0:
        for i in range(18):
            u = i / 17
            yy = y_top + 6 + (y_bot - y_top) * u ** 1.25
            w = (26 + 170 * u) * (0.55 + 0.45 * math.sin(i * 2.3 + 2 * math.pi * k / n))
            off = 14 * u * math.sin(i * 1.7 + 2 * math.pi * k / n)
            a = (0.85 - 0.45 * u) * glitter
            out += (f'<path d="M{f1(sun_x - w / 2 + off)},{f1(yy)} L{f1(sun_x + w / 2 + off)},{f1(yy)}" '
                    f'stroke="#fff0c0" stroke-width="{f1(3 + 4 * u)}" stroke-linecap="round" opacity="{a:.2f}"/>')
    return out


# ================================================================== drawings

def sky_svg():
    """Sky (violet-gold gradient), the low sun and the lake body behind everything (lake_galilee, sunset)."""
    return doc(PR.lake_galilee(-40, W + 40, LAKE_Y, LAKE_S, time="sunset", shore=None, part="back", boats=False,
                               far_shore=False, top=-40, sun_x=(SUN[0] + 40) / (W + 80)))


def hills_svg():
    return doc(PR.lake_galilee(-40, W + 40, LAKE_Y, LAKE_S, time="sunset", shore=None, part="back", boats=False,
                               sky=False, sun_x=(SUN[0] + 40) / (W + 80)))


def far_storm_svg(dark=0.0):
    """Dark clouds gathering over the far hills on the left (drawn behind the hills); dark 0..1 deepens them."""
    base = S.mix("#5d6488", "#454a70", dark)
    shade_ = S.mix("#4b5176", "#363b5e", dark)
    rim = S.mix("#b4b4cc", "#9ea0bc", dark)
    b = ""
    for cx, cy, w, h, sd in ((120, 605, 280, 110, 3), (300, 588, 310, 136, 4), (500, 612, 280, 100, 5),
                             (400, 556, 180, 88, 6), (670, 632, 220, 76, 7)):
        b += S.cloud(cx, cy, w, h, base, seed=sd + 60, puffs=6, sw=3.0, shade_fill=shade_)
        b += (f'<path d="M{cx - w * 0.3:.0f},{cy - h * 0.38:.0f} q{w * 0.2:.0f},{-h * 0.2:.0f} {w * 0.4:.0f},'
              f'{-h * 0.05:.0f}" stroke="{rim}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # a soft grey rain veil under them, mostly hidden by the hills
    veil = ""
    for i in range(12):
        x = 70 + i * 50
        veil += (f'<path d="M{x},{615} l-22,80" stroke="#8f84ae" stroke-width="5" opacity="0.4" '
                 f'stroke-linecap="round"/>')
    return doc(S.g(PR._haze(veil + b, "#a08ab4", 0.14, 0.5, 0.75), filter="wobble"))


def storm_glow_svg():
    defs = S.rad_grad("st1glow", [(0, "#f4e8ff", 0.85), (0.5, "#cbb8e8", 0.35), (1, "#cbb8e8", 0)])
    return doc(f'<ellipse cx="330" cy="585" rx="210" ry="90" fill="url(#st1glow)"/>', defs)


def sunset_clouds_svg():
    b = ""
    for cx, cy, w, h, sd in ((300, 150, 360, 66, 11), (1830, 210, 400, 70, 12), (1540, 112, 200, 42, 13)):
        b += S.cloud(cx, cy, w, h, "#f8cdb0", seed=sd, puffs=5, sw=3, shade_fill="#e3a2b2")
        b += (f'<path d="M{cx - w * 0.3:.0f},{cy - h * 0.3:.0f} q{w * 0.25:.0f},{-h * 0.25:.0f} {w * 0.5:.0f},0" '
              f'stroke="#fff3d6" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.85"/>')
    return doc(S.g(PR._haze(b, "#c99ab2", 0.08, 0.5, 0.75), filter="wobble"))


HULL_AVOID = (BX - 330, BY - 100, BX + 330, BY + 6)


def water_back_svg():
    body, defs = evening_water("st1water", HZ - 2, H + 40)
    # the far shoreline highlight
    body += (f'<path d="M-30,{HZ + 1} L{W + 30},{HZ + 1}" stroke="#ffe0a8" stroke-width="4" opacity="0.8"/>')
    body += boat_reflection()
    return doc(S.g(body, filter="wobble"), defs)


def boat_reflection():
    """The boat's soft dark reflection right under the hull, and the long wobbly line of the mast."""
    hw = 300 * BS / 0.42
    d = (f"M{BX - hw},{BY + 2} Q{BX},{BY + 26} {BX + hw},{BY + 2} Q{BX + hw * 0.7},{BY + 70} {BX},{BY + 78} "
         f"Q{BX - hw * 0.7},{BY + 70} {BX - hw},{BY + 2} Z")
    out = f'<path d="{d}" fill="#3b376c" opacity="0.38"/>'
    mx = BX + PR.BOAT_MAST_X * BS
    out += (f'<path d="M{mx},{BY + 34} q6,30 0,60 q-6,30 0,60" stroke="#3b376c" stroke-width="4" fill="none" '
            f'opacity="0.2"/>')
    return out


def ripples_svg(k):
    sail_x0, sail_x1 = BX - 115 * BS, BX + 575 * BS
    out = water_ripples(k % NPH, NPH, 21, HZ, H + 20, sun_x=SUN[0], avoid=(HULL_AVOID,))
    # the sail's pale reflection, broken into shimmering dashes
    rng = random.Random(5)
    for i in range(16):
        u = i / 15
        yy = BY + 40 + 190 * u
        w = (sail_x1 - sail_x0) * (0.85 - 0.3 * u) * (0.6 + 0.4 * math.sin(i * 1.9 + 2 * math.pi * k / NPH))
        cx = (sail_x0 + sail_x1) / 2 + 12 * math.sin(i * 2.4 + 2 * math.pi * k / NPH) + rng.uniform(-6, 6)
        out += (f'<path d="M{f1(cx - w / 2)},{f1(yy)} L{f1(cx + w / 2)},{f1(yy)}" stroke="#f8e6d0" '
                f'stroke-width="{f1(4 + 3 * u)}" stroke-linecap="round" opacity="{0.32 - 0.18 * u:.2f}"/>')
    return doc(S.g(out, filter="wobble-fine"))


def front_strip_svg():
    """Water in front of the hull below the waterline (same gradient as the lake), with a little foam line."""
    x0, x1 = BX - 330, BX + 330
    top = S.wave_line(BY - 3, 2.2, 90, 0.6, x0=x0, x1=x1)
    d = top + f" L{x1},{BY + 60} L{x0},{BY + 60} Z"
    defs = ugrad("st1strip", HZ, H, WATER_STOPS)
    body = f'<path d="{d}" fill="url(#st1strip)"/>'
    body += f'<g clip-path="url(#st1sclip)">{boat_reflection()}</g>'
    defs += f'<clipPath id="st1sclip"><path d="{d}"/></clipPath>'
    body += (f'<path d="{S.wave_line(BY - 1, 2.2, 90, 0.6, x0=BX - 280 * BS / 0.42, x1=BX + 290 * BS / 0.42)}" '
             f'stroke="#ffe4c0" stroke-width="3.5" fill="none" opacity="0.85"/>')
    # fade the strip's ends into the lake (no hard edge)
    mask = (f'<linearGradient id="st1sm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" '
            f'stop-opacity="0"/><stop offset="0.12" stop-color="#fff"/><stop offset="0.88" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="st1mask"><rect x="{x0}" y="{BY - 20}" width="{x1 - x0}" height="100" fill="url(#st1sm)"/></mask>')
    return doc(f'<g mask="url(#st1mask)">{S.g(body, filter="wobble-fine")}</g>', defs + mask)


def far_boats_svg(i):
    x, y, k, f = ((330, 676, 0.12, 1), (1500, 668, 0.10, -1))[i]
    return doc(PR.small_boat(x, y, k, f, variant=1, sail="full", time="sunset"))


def dove_svg(wing):
    return doc(PR.dove(200, 200, 0.85, 1, wing=wing))


# ---- the boat and the people in it (same x, y, scale, facing for all)

def bpts():
    return PR.boat_points(BX, BY, BS, 1)


def boat_back_svg(k):
    return doc(PR.fishing_boat(BX, BY, BS, 1, sail="none", phase=k / 4, lantern=False, nets=True))


def sail_svg():
    sv, cl, cr = PR._boat_sail("full", 0.0, "st1sail")
    rig = max(3.4, 2.4 / BS)
    stay = S.shade(INK, 0.12)
    sheets = (f'<path d="M{cl[0]:.1f},{cl[1]:.1f} L-440,-165" stroke="{stay}" stroke-width="{rig:.1f}" fill="none"/>'
              f'<path d="M{cr[0]:.1f},{cr[1]:.1f} L650,-195" stroke="{stay}" stroke-width="{rig:.1f}" fill="none"/>')
    return doc(PR._place(sheets + sv, BX, BY, BS, 1))


SAIL_PIV = (BX + PR.BOAT_MAST_X * BS, BY + PR.BOAT_YARD_Y * BS)


def boat_front_svg():
    return doc(PR.fishing_boat(BX, BY, BS, 1, sail="none", part="front", nets=True))


FAR = [(4, 1, "stand", "happy"), (6, 2, "stand", "kind"), (2, 3, "stand", "happy"), (7, 4, "stand", "happy"),
       (9, 5, "stand", "kind")]


def crew_far_svg(blinks=False):
    p = bpts()["far_stand"]
    out = ""
    for v, i, pose, e in FAR:
        x, y = p[i]
        f = -1 if i >= 4 else 1
        out += C.disciples(x, y, BS, f, variant=v, pose=pose, expr=blink(e) if blinks and i in (1, 4) else e)
    return doc(out)


JES = None


def jesus_svg(blinks=False):
    x, y = bpts()["stern_seat"]
    return doc(C.jesus(x, y, BS, 1, pose="sit", expr=blink("warm") if blinks else "warm"))


def crew_near_svg(john="stand", ph=0.0, blinks=False):
    p = bpts()
    out = ""
    x, y = p["stand"][1]
    out += C.disciples(x - 10 * BS, y, BS, 1, variant=1, pose="sit", expr=blink("happy") if blinks else "happy")
    x, y = p["stand"][4]
    out += C.disciples(x, y, BS, 1, variant=0, pose="pull_rope", expr="happy")
    x, y = p["stand"][2]
    if john == "wave":
        out += C.disciples(x, y, BS, -1, variant=3, pose="wave", phase=ph, expr="happy")
    else:
        out += C.disciples(x, y, BS, -1, variant=3, pose="stand", expr="happy")
    return doc(out)


JOHN_PIV = (BX + 10 * BS, BY)


def ribbon_svg(text, cx=RIB_X, cy=RIB_Y, hw=360, h=80, band_col="#3f6f92"):
    tail_col, fold_col = S.shade(band_col, -0.16), S.shade(band_col, -0.38)
    b = ""
    for sd in (-1, 1):
        ex = cx + sd * hw
        top, bot = cy - h / 2 + 26, cy + h / 2 + 26
        pts = [(ex - sd * 30, top), (ex + sd * 95, top), (ex + sd * 66, (top + bot) / 2), (ex + sd * 95, bot),
               (ex - sd * 30, bot)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z", fill=tail_col, sw=3.5)
        fold = [(ex, cy + h / 2 + 6), (ex - sd * 30, bot), (ex - sd * 30, cy + h / 2 + 6)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in fold) + " Z", fill=fold_col, sw=3)
    band = (f"M{cx - hw},{cy - h / 2 + 8} Q{cx},{cy - h / 2 - 12} {cx + hw},{cy - h / 2 + 8} "
            f"L{cx + hw},{cy + h / 2 + 6} Q{cx},{cy + h / 2 - 14} {cx - hw},{cy + h / 2 + 6} Z")
    b += S.path(band, fill=band_col, sw=3.5)
    for yy, q in ((cy - h / 2 + 18, cy - h / 2), (cy + h / 2 - 4, cy + h / 2 - 22)):
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#f2cf86" stroke-width="3" '
              f'fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="46" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">{text}</text>')
    return doc(body)


# ================================================================== the page (shared with s02)


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    if len(marks) == 1:                       # fallback: the title is the last 6 characters
        ch = ch[-6:]
    return t_rib, ch


def boat_motion(t):
    """The boat's gentle rocking on the calm lake (pivot = the waterline anchor)."""
    return Tf(dy=3.2 * math.sin(2 * math.pi * (t / 4.4 + 0.2)), rot=0.9 * math.sin(2 * math.pi * t / 4.4),
              px=BX, py=BY)


def title_page(sc, ctx, toff=0.0, gate=None, title_gate=None):
    """Add the whole title page to ``sc``. Times inside are s01's; ``toff`` is added to the host scene's clock
    (s02 passes the offset between the two scene starts). ``gate(t_host)`` multiplies every layer's alpha (s02
    hides the page once covered); ``title_gate`` multiplies the lettering only. Returns (camera(t_host), fx, info)."""
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_storm = onsets[4] if len(onsets) > 4 else onsets[-1]          # '风'
    t_wave = snap(1.0)

    def add(name, svg, motion=None, title=False, **kw):
        m0 = motion
        g1 = gate
        g2 = title_gate if title else None

        def mot(th):
            tf = m0(th + toff) if m0 is not None else Tf()
            a = tf.alpha * (g1(th) if g1 else 1.0) * (g2(th) if g2 else 1.0)
            return Tf(tf.dx, tf.dy, tf.rot, tf.sx, tf.sy, a, tf.px, tf.py)
        need = m0 is not None or g1 is not None or g2 is not None
        fa = kw.pop("frame_at", None)
        sc.add(f"st1_{name}", svg, motion=mot if need else None,
               frame_at=(lambda th, fa=fa: fa(th + toff)) if fa else None, **kw)

    add("sky", sky_svg(), wc=0.6)
    add("sclouds", sunset_clouds_svg(), motion=M.drift(vx=4.5), wc=0.8)

    def storm_m(t):
        k = M.progress(t, t_storm - 0.2, t_storm + 1.6, "sine")
        s = 1.0 + 0.012 * t + 0.05 * k
        return Tf(dx=5.5 * t, sx=s, sy=s, px=360, py=660)
    add("storm", [far_storm_svg(0.0), far_storm_svg(1.0)], motion=storm_m,
        frame_at=lambda t: M.progress(t, t_storm - 0.2, t_storm + 1.4, "sine"))

    def glow_m(t):
        a = 0.0
        for t0, amp in ((t_storm + 0.25, 0.55), (t_storm + 0.55, 0.35)):
            u = t - t0
            if 0 <= u < 0.6:
                a = max(a, amp * math.exp(-u / 0.12) * (1 - math.exp(-u / 0.02)))
        return Tf(dx=5.5 * t, alpha=a)
    add("sglow", storm_glow_svg(), motion=glow_m, wc=0, blend="screen")
    add("hills", hills_svg())
    add("water", water_back_svg(), wc=0.7)
    for i in range(2):
        add(f"farboat{i}", far_boats_svg(i), motion=M.drift(vx=(3.0, -2.4)[i]), wc=0.5)

    # the dove gliding across the sky
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    def fly(t):
        x = 150 + 92 * t
        return Tf(dx=x - 200, dy=400 - 26 * t + 12 * math.sin(2 * math.pi * t / 2.3))
    add("dove", [dove_svg(w) for w in wings], motion=fly, wc=0.3,
        frame_at=lambda t: float(int(t / 0.075) % 8) if (t % 3.2) < 1.6 else 2.0)

    # ---- the boat and the people in it, all rocking together
    bm = boat_motion
    add("boat_back", [boat_back_svg(k) for k in range(4)], motion=bm, frame_at=lambda t: float(int(t / 0.14) % 4),
        seed=41)
    add("sail", sail_svg(), seed=43,
        motion=lambda t: compose(bm(t), Tf(sx=1 + 0.006 * math.sin(2 * math.pi * t / 2.9),
                                           sy=1 + 0.014 * math.sin(2 * math.pi * t / 2.9), px=SAIL_PIV[0],
                                           py=SAIL_PIV[1])))
    fents = [(0, 0)]
    for tb in (1.4, 3.9, 5.2):
        fents += [(snap(tb), 1), (snap(tb + 0.13), 0)]
    add("crew_far", [crew_far_svg(), crew_far_svg(True)], motion=bm, frame_at=cuts(sorted(fents)), seed=45)
    jents = [(0, 0)]
    for tb in (2.2, 4.8):
        jents += [(snap(tb), 1), (snap(tb + 0.14), 0)]
    add("jesus", [jesus_svg(), jesus_svg(True)], motion=bm, frame_at=cuts(sorted(jents)), seed=47)
    # near row: John lifts his hand and waves from ~1 s (a squash dip hides the cut)
    nfr = [crew_near_svg(), crew_near_svg(blinks=True)] + [crew_near_svg("wave", ph) for ph in (0, .25, .5, .75)]

    def near_fa(t):
        if t < t_wave:
            return 1.0 if 0.5 <= t < 0.63 else 0.0
        return 2.0 + float(int((t - t_wave) / 0.17) % 4)
    jdip = dip(t_wave, BS, JOHN_PIV, 7)
    add("crew_near", nfr, motion=lambda t: compose(bm(t), jdip(t)), frame_at=near_fa, seed=49)
    add("boat_front", boat_front_svg(), motion=bm, seed=51)
    add("strip", front_strip_svg(), wc=0.5)
    add("ripples", [ripples_svg(k) for k in range(NPH)] + [ripples_svg(0)], frame_at=loop_fa(0.42, NPH), wc=0.3)

    # ---- title lettering
    story = load_story()

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=RIB_X, py=RIB_Y)
    add("ribbon", ribbon_svg(story.SUBTITLE), motion=unfurl, title=True, wc=0)
    title = story.TITLE
    x0 = W / 2 - TITLE_STEP * (len(title) - 1) / 2
    for i, ch in enumerate(title):
        x = x0 + i * TITLE_STEP
        t0 = onsets[min(i, len(onsets) - 1)] - 0.06

        def pop(t, t0=t0, x=x, i=i):
            if t < t0:
                return Tf(alpha=0)
            a = min(1.0, (t - t0) / 0.12)
            u = min(1.0, (t - t0) / 0.42)
            s = 0.45 + 0.55 * M.ease("back")(u)
            dy = 30 * (1 - M.ease("out")(u)) + 2.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.16))
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 60)
        add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, grad_id=f"st1tg{i}", colors=TITLE_COLS),
            motion=pop, title=True, wc=0)

    cam0 = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 + 8, H / 2 + 10, W * 0.935))], "sine")
    cam = lambda th: cam0(th + toff)                                          # noqa: E731
    t_done = onsets[-1] + 0.45

    def gated(f):
        def fx(frame, th, view):
            if gate is not None and gate(th) <= 0:
                return frame
            return f(frame, th + toff, view)
        return fx
    fxs = [
        gated(FX.sparkles((SUN[0] - 160, HZ + 20, SUN[0] + 160, H - 60), count=8, color=(255, 240, 200),
                          size=(7, 14), period=1.7, drift=0, seed=4)),
        gated(FX.sparkles((520, 250, 1600, 430), count=6, t0=t_done, color=(255, 236, 180), size=(9, 16),
                          period=2.0, drift=0, seed=9)),
    ]
    info = dict(t_rib=t_rib, onsets=onsets, t_done=t_done, t_storm=t_storm)
    return cam, fxs, info


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    cam, fxs, info = title_page(sc, ctx)
    sc.camera = cam
    sc.fx = fxs
    sc.subtitles = False
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-17, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-25, fade_in=1.0, fade_out=1.3)
    sc.sfx("chime", info["t_rib"], gain_db=-10)
    for t in info["onsets"]:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", info["t_done"], gain_db=-17)
    sc.sfx("thunder", info["t_storm"] + 0.2, gain_db=-31, pan=-0.6)
    return sc
