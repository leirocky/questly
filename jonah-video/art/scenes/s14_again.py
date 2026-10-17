"""Scene 14 (v2) — God speaks to Jonah a second time; this time he obeys (Jonah 3:1-3a).

(work in progress)
"""
import hashlib
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s02_call as V2
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 2600, 1188

# ------------------------------------------------------------------ Jonah rig (damp robe, walking staff)
STAFF_DX = 84.0          # figure px in front of the anchor where the staff stands while he kneels / stands
STAFF_LEN = 384.0        # figure px, tip to knob
STAFF_W = 11.0
WOOD = "#9a6236"
WOOD_DARK = "#74462a"
WRAP = P["jonah_sash"]


def _damp_marks(st):
    """A few drops (two from the hem, one from the beard) - he is only 'still a bit wet'."""
    hemp, um, Hm = st["hemp"], st["um"], st["Hm"]
    floor = st["ground"] - 2 if st["mode"] != "air" else None

    def drop(p, k):
        y = p[1] if floor is None else min(p[1], floor - 1.15 * k)
        return C._drop(p[0], y, k)
    out = ""
    chain = [p for p in hemp if C._dot(C._sub(p, Hm), um) > -2]
    chain = sorted(chain, key=lambda p: C._dot(p, (-um[1], um[0])))
    if chain:
        for i, k in enumerate((0.3, 0.78)):
            p = chain[int(k * (len(chain) - 1))]
            out += drop(C._add(p, C._mul(um, 13 + 7 * i)), 5.0)
    chin = st["hw"](0.16, 1.32)
    out += drop((chin[0], chin[1] + 4), 4.6)
    return out


def _damp_patches(st):
    """Darker soaked patches along the hem, clipped to the hem band of the robe."""
    hemp, um, Hm, m = st["hemp"], st["um"], st["Hm"], st["m"]
    cid = "dmp" + hashlib.md5(C._d(hemp).encode()).hexdigest()[:10]
    col = S.shade(S.shade(P["jonah_robe"], -0.08), -0.2)
    inner = ""
    for k, (fx, r) in enumerate(((-0.55, 14), (0.1, 17), (0.65, 12))):
        c = C._add(C._sub(Hm, C._mul(um, 8 + 6 * (k % 2))), C._mul((-um[1], um[0]), fx * m["ww"]))
        inner += f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{r * 1.3:.1f}" ry="{r:.1f}" fill="{col}" opacity="0.5"/>'
    return (f'<clipPath id="{cid}"><path d="{C._d(hemp)}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>')


def _damp_design(front=None):
    """Jonah's design 'still a bit wet': the robe ~8 % darker with soaked patches at the hem and a few drops, the
    head-cloth already dry, and no seaweed any more."""
    D = C._jonah_design(wet=False)
    D["robe"] = D["sleeve"] = S.shade(P["jonah_robe"], -0.08)
    D["hem_col"] = S.shade(P["jonah_robe_dark"], -0.06)
    D["mid"] = _damp_patches
    D["front"] = (lambda st: front(st) + _damp_marks(st)) if front else _damp_marks
    return D


def _fist_centre(st, i=1):
    """Centre of hand i's fist (body coords), as characters._hand draws it."""
    Sx, E, W = st["arms"][i]
    d = C._nrm(C._sub(W, E))
    return C._add(W, C._mul(d, 0.45 * st["m"]["hr"]))


def _staff_markup(tip, through, length=STAFF_LEN, w=STAFF_W):
    """A wooden walking staff from ``tip`` along the line through ``through`` (body coords), knob at the top."""
    d = C._nrm(C._sub(through, tip))
    top = C._add(tip, C._mul(d, length))
    n = (-d[1], d[0])
    w0, w1 = w * 0.42, w * 0.55
    pts = [C._add(tip, C._mul(n, w0)), C._add(top, C._mul(n, w1)), C._sub(top, C._mul(n, w1)),
           C._sub(tip, C._mul(n, w0))]
    body = (f'<path d="M{C._pt(pts[0])} L{C._pt(pts[1])} L{C._pt(pts[2])} L{C._pt(pts[3])} Z" fill="{WOOD}" '
            f'stroke="{P["ink"]}" stroke-width="3.4" stroke-linejoin="round"/>')
    # grain line, a knot and the round knob at the top
    g0, g1 = C._add(tip, C._mul(d, 40)), C._add(tip, C._mul(d, length - 30))
    body += C._line(f"M{C._pt(C._add(g0, C._mul(n, 1.5)))} L{C._pt(C._add(g1, C._mul(n, 1.5)))}", w=1.6,
                    col=WOOD_DARK, extra='opacity="0.7"')
    kn = C._add(tip, C._mul(d, length * 0.62))
    body += f'<ellipse cx="{kn[0]:.1f}" cy="{kn[1]:.1f}" rx="3.2" ry="2.2" fill="{WOOD_DARK}"/>'
    kb = C._add(top, C._mul(d, 4))
    body += (f'<circle cx="{kb[0]:.1f}" cy="{kb[1]:.1f}" r="{w * 0.95:.1f}" fill="{S.shade(WOOD, 0.1)}" '
             f'stroke="{P["ink"]}" stroke-width="3.4"/>'
             f'<circle cx="{kb[0] - 3:.1f}" cy="{kb[1] - 3:.1f}" r="2.6" fill="#f0d2a8" opacity="0.8"/>')
    # a teal cloth wrap just under the knob (ties it to Jonah's sash colour)
    a, b = C._add(top, C._mul(d, -22)), C._add(top, C._mul(d, -40))
    body += (f'<path d="M{C._pt(a)} L{C._pt(b)}" stroke="{P["ink"]}" stroke-width="{w + 6.8:.1f}" '
             f'stroke-linecap="butt"/>'
             f'<path d="M{C._pt(a)} L{C._pt(b)}" stroke="{WRAP}" stroke-width="{w + 1.6:.1f}" stroke-linecap="butt"/>')
    return body


def _grip(st, tip):
    """Front hook: the staff through the near fist, then the fist again on top so the fingers close round it."""
    c = _fist_centre(st)
    hr = st["m"]["hr"]
    return (_staff_markup(tip, c) +
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{hr:.1f}" fill="{P["skin"]}" stroke="{P["ink"]}" '
            f'stroke-width="3.2"/>'
            + C._line(f"M{c[0] - 0.55 * hr:.1f},{c[1] - 0.15 * hr:.1f} q{0.5 * hr:.1f},{0.35 * hr:.1f} "
                      f"{1.05 * hr:.1f},0", w=1.8))


def jonah_fig(x, y, s, ps, expr=None, facing=1, marks=True, staff=None, label="j"):
    """Damp Jonah in pose dict ``ps``. staff=(tip_x, lift) in figure px (x forward of the anchor, lift above the
    ground) draws the walking staff held in the near hand."""
    ps = dict(C.POSES[ps]) if isinstance(ps, str) else dict(ps)
    e = expr or ps["expr"]
    front = None
    if staff is not None:
        tx, lift = staff
        front = lambda st: _grip(st, (tx, st["ground"] - lift))   # noqa: E731
    inner, _ = C._figure(_damp_design(front), C._ADULT, ps, e, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


def _jfn(x, y, scale=1.0, facing=1, ps=None, expr=None, marks=True, staff=None):
    return jonah_fig(x, y, scale, ps, expr, facing, marks, staff)


def staff_alone(x, y, s):
    """The staff standing planted in the ground at stage (x, y) (while Jonah kneels beside it)."""
    body = _staff_markup((0.0, 0.0), (0.0, -10.0)) + \
        f'<ellipse cx="0" cy="2" rx="20" ry="4" fill="{P["ink"]}" opacity="0.18"/>'
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><g filter="url(#wobble-fine)">{body}</g></g>'


# poses ------------------------------------------------------------------------------------------
_KNEEL = C.POSES["kneel_pray"]
KNEEL_UP = dict(_KNEEL, look=(0.03, -0.08))                        # eyes open, looking up into the light
KNEEL_LISTEN = dict(_KNEEL, h=-18, look=(0.03, -0.08), marks=("sound",),
                    arms=(("ik", "torso", 0.9, 0.42, 1), ("ik", "head", -0.66, 0.16, -1)),
                    hands=("open", "cup"))
KNEEL_CHEST = dict(_KNEEL, h=-8, look=(0.02, -0.05),
                   arms=(("ik", "torso", 0.9, 0.42, 1), ("ik", "torso", 0.55, 0.74, 1)),
                   hands=("open", "open"))
KNEEL_NOD = dict(KNEEL_CHEST, h=14, look=(0.0, 0.04))
KNEEL_CITY = dict(KNEEL_CHEST, h=-2, look=(0.08, -0.01))           # hand on chest, looking far east (right)
KNEEL_LOOK = dict(_KNEEL, h=-3, look=(0.08, -0.01))                 # praying hands, gazing far east (right)
RISE = C._P(t=4, h=-8, drop=70, legs=(("ik", 60, 1), (0, -92)),
            arms=(("fk", 30, 40), ("ik", "abs", STAFF_DX - 6, -205, 1)),
            hands=("open", "fist"), feet=(None, 100))
STAND_STAFF = C._P(arms=(("fk", 14, 8), ("ik", "abs", STAFF_DX - 6, -168, 1)), hands=("fist", "fist"))


def walk_staff_pose(k, A=40.0, N=5, swing=34, lift=20, drop=10):
    """Planted-foot walk drawing k (N drawings per step, two steps per cycle, the s02 rig) holding the staff in the
    near hand. The staff tip is planted together with the FAR foot (step 0) and moves back with it, so it never
    slides on the road; during step 1 it swings forward through the air. Returns (pose, (tip_x, tip_lift))."""
    ph = (k % (2 * N)) / N
    step, u = divmod(ph, 1.0)
    plant = ("ik", A * (1 - 2 * u), 1)
    swing_leg = ("ik", -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, lift * math.sin(math.pi * u))
    sw = swing * math.cos(math.pi * ph)
    c = STAFF_DX - A
    if step == 0:
        tip = (c + A * (1 - 2 * u), 0.0)
    else:
        tip = (c - A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 16 * math.sin(math.pi * u))
    hx = STAFF_DX - 26 + 22 * math.cos(math.pi * ph)
    ps = C._P(t=4, h=-3, legs=(plant, swing_leg) if step == 0 else (swing_leg, plant),
              arms=(("fk", -sw, -sw + 16), ("ik", "abs", hx, -166 + 4 * math.sin(math.pi * ph), 1)),
              hands=("fist", "fist"), drop=drop + 0.4 * drop * math.cos(2 * math.pi * u))
    return ps, tip


# ====================================================================== layout (stage px)
HORIZON = 590
JX, JS = 640.0, 1.15                      # Jonah's kneeling spot on the coast road (y = road centre)
GAP = (690, 170)                          # where the clouds part (God's light comes from here)
CITY = (1380, 1880, 598, 0.36)            # the distant Nineveh skyline: x0, x1, ground y, scale
CITY_C = (1630, 505)                      # its middle (glow / trail target)
SIGN = (1572, 812, 0.7)                   # the signpost of s03 (他施 west, 尼尼微 east) on the far verge
ROAD_X = [-60, 300, 640, 1000, 1300, 1550, 1700, 1800]
ROAD_TOP = [990, 955, 932, 905, 872, 828, 770, 708]
ROAD_BOT = [1260, 1140, 1045, 990, 950, 900, 812, 716]
SHORE = [(-60, 1010), (150, 900), (380, 790), (600, 700), (780, 640), (930, 600), (980, 592)]
INNER = [(-60, 1120), (200, 990), (430, 870), (640, 782), (820, 708), (960, 646), (1060, 612), (1120, 600)]
CREST = [(980, 592), (1100, 622), (1400, 658), (1800, 700), (2200, 690), (2680, 680)]

A_W, N_W, HOLD_W = 40.0, 5, 0.12         # walk rig: stride half-length, drawings per step, s per drawing

PUNCT = "，、。：；！？,.!?:;"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def _interp(xs, ys, x):
    if x <= xs[0]:
        return ys[0]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            u = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + (ys[i + 1] - ys[i]) * u
    return ys[-1]


def road_y(x):
    """Centre line of the road (where Jonah walks)."""
    return 0.5 * (_interp(ROAD_X, ROAD_TOP, x) + _interp(ROAD_X, ROAD_BOT, x))


JY = road_y(JX)


def walk_scale(x):
    """Jonah gets a little smaller as the road leads away toward the east."""
    return JS * (1.0 - 0.18 * max(0.0, x - JX) / 860.0)


# ====================================================================== timing helpers (as in s02 v2)
def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def _when(ctx, phrases, k=0.0, default=None, after=0.0):
    """Estimated time at which ``phrase`` is spoken: its subtitle chunk's start plus its share of the chunk by
    character position (k = 1 is the end of the phrase). Chunks starting before ``after`` are skipped."""
    if isinstance(phrases, str):
        phrases = (phrases,)
    for ph in phrases:
        for ln in ctx.lines:
            for c in (ln.chunks or [ln]):
                if c.start < after - 1e-6 or ph not in c.text:
                    continue
                txt = c.text.rstrip(PUNCT)
                i = c.text.index(ph) + k * len(ph)
                return c.start + (c.end - c.start) * _clamp(i / max(1, len(txt)))
    return default


def _hop(t, t0, h=10.0, dur=0.3):
    if t0 is None or not (t0 <= t <= t0 + dur):
        return 0.0
    return -h * math.sin(math.pi * (t - t0) / dur)


def _squash(t, t0, k=0.04, dur=0.32):
    if t0 is None or not (t0 <= t <= t0 + dur):
        return 1.0, 1.0
    u = (t - t0) / dur
    q = math.sin(math.pi * min(1.0, u * 1.6)) * (1 - u)
    return 1 + 0.6 * k * q, 1 - k * q


def _sched(events):
    ev = sorted(events, key=lambda e: e[0])

    def f(t):
        v = ev[0][1]
        for te, val in ev:
            if t >= te:
                v = val
            else:
                break
        return float(v)
    return f


# ====================================================================== painting
def sky_svg():
    defs = S.lin_grad("s14sky", [(0, P["sky_day_top"]), (0.30, P["sky_day"]),
                                 (0.47, S.mix(P["sky_day"], P["sky_warm"], 0.6)), (0.52, P["sky_warm"]),
                                 (1, P["sky_warm"])])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s14sky)"/>', defs)


def clouds_svg(items):
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, "#fdf6e8", seed=seed, sw=3, shade_fill="#e9dccb")
    return doc(S.g(body, filter="wobble"))


def cloud_rim_svg(item, gx, gy, rx, ry, uid):
    """Soft gold light on the inner edge of a parting cloud, masked to the cloud's own silhouette (v1 s09)."""
    cx, cy, w, h, seed = item
    sil = S.cloud(cx, cy, w, h, "#ffffff", seed=seed, sw=0)
    defs = (f'<mask id="s14rm{uid}" maskUnits="userSpaceOnUse" x="-50" y="-300" width="{SW}" height="900">'
            f'<g filter="url(#wobble)">{sil}</g></mask>'
            + S.rad_grad(f"s14rg{uid}", [(0, "#f6c25a", 0.9), (0.55, "#f0b040", 0.5), (1, "#f0b040", 0)]))
    body = (f'<g mask="url(#s14rm{uid})"><ellipse cx="{gx}" cy="{gy}" rx="{rx}" ry="{ry}" '
            f'fill="url(#s14rg{uid})"/></g>')
    return doc(body, defs)


def rays_svg(src, target, spread=30, n=6, length=1250, kind="add"):
    """A fan of thin golden rays from src toward target plus a warm glow on the target (v1 s09 technique: a
    multiply pass takes blue out of the sky, an add pass brightens without clipping)."""
    sx, sy = src
    a0 = math.degrees(math.atan2(target[1] - sy, target[0] - sx))
    if kind == "mul":
        stops = (("#ffd890", 0.42), ("#ffdc9c", 0.3), ("#ffe0a8", 0.1))
    else:
        stops = (("#f0a848", 0.22), ("#f0a040", 0.15), ("#f0a040", 0.05))
    defs = (f'<radialGradient id="s14ray{kind}" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="{length}">'
            f'<stop offset="0" stop-color="{stops[0][0]}" stop-opacity="{stops[0][1]}"/>'
            f'<stop offset="0.65" stop-color="{stops[1][0]}" stop-opacity="{stops[1][1]}"/>'
            f'<stop offset="1" stop-color="{stops[2][0]}" stop-opacity="{stops[2][1]}"/></radialGradient>'
            + S.rad_grad("s14glow", [(0, "#f6c25a", 0.36), (0.5, "#f0b040", 0.14), (1, "#f0b040", 0)]))
    d = ""
    rng = random.Random(4)
    for i in range(n):
        a = math.radians(a0 - spread / 2 + spread * i / (n - 1) + rng.uniform(-1.5, 1.5))
        wa = math.radians(rng.uniform(1.1, 1.9))
        r0, r1 = 40, length
        pts = [(sx + r0 * math.cos(a - wa / 4), sy + r0 * math.sin(a - wa / 4)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 4), sy + r0 * math.sin(a + wa / 4))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    tx, ty = target
    body = f'<path d="{d}" fill="url(#s14ray{kind})" filter="url(#soft)"/>'
    if kind == "add":
        body += (f'<ellipse cx="{tx}" cy="{ty - 40}" rx="230" ry="260" fill="url(#s14glow)"/>'
                 f'<ellipse cx="{tx}" cy="{JY + 8}" rx="240" ry="44" fill="url(#s14glow)"/>')
    return doc(body, defs)


def warm_svg():
    """A broad warm wash around the light (additive) - the whole page warms while God speaks."""
    defs = S.rad_grad("s14warm", [(0, "#5a3a08", 1), (0.45, "#3a2406", 0.7), (1, "#000000", 0)])
    return doc(f'<ellipse cx="{GAP[0]}" cy="{GAP[1] + 420}" rx="1250" ry="980" fill="url(#s14warm)"/>', defs)


def far_svg():
    """Hazy hills on the eastern horizon, the far plain and the great city of Nineveh far away."""
    haze = S.mix(P["stone"], P["sky_day"], 0.55)
    haze2 = S.mix(P["stone"], P["sky_day"], 0.42)
    defs = S.lin_grad("s14plain", [(0, S.mix(P["sand_light"], P["sky_warm"], 0.5)), (1, P["sand_light"])])
    hills = (S.path(S.hill(820, 1420, HORIZON + 8, 40, seed=3, bumps=2, bottom=800), fill=haze, sw=2.4)
             + S.path(S.hill(1900, 2900, HORIZON + 8, 70, seed=8, bumps=3, bottom=800), fill=haze, sw=2.4)
             + S.path(S.hill(1250, 2050, HORIZON + 10, 30, seed=5, bumps=2, bottom=800), fill=haze2, sw=2.4))
    plain = (f'<path d="M600,{HORIZON + 4} C900,{HORIZON + 2} 1400,{HORIZON + 6} 1800,{HORIZON + 8} '
             f'S2600,{HORIZON + 8} 2950,{HORIZON + 6} L2950,860 L600,860 Z" '
             f'fill="url(#s14plain)" stroke="{P["ink"]}" stroke-width="2.2"/>')
    x0, x1, y, sc_ = CITY
    city = PR.nineveh_skyline(x0, x1, y, scale=sc_, seed=21, haze=0.3)
    palms = ""
    for x, yy, s_, ln in ((1330, 616, 0.17, 0.2), (1372, 622, 0.14, -0.2), (1930, 618, 0.18, -0.1),
                          (1985, 626, 0.15, 0.25), (2350, 630, 0.16, 0.1), (1100, 612, 0.13, 0.0)):
        palms += PR.palm_tree(x, yy, s_, lean=ln, dates=False)
    fields = ""
    for x, yy, w_, h_ in ((1240, 640, 220, 20), (2100, 650, 300, 26), (2500, 640, 220, 20), (1700, 660, 260, 22)):
        fields += (f'<ellipse cx="{x}" cy="{yy}" rx="{w_ / 2}" ry="{h_ / 2}" '
                   f'fill="{S.mix(P["grass"], P["sand_light"], 0.5)}" opacity="0.8"/>')
    body = S.g(hills, filter="wobble") + S.g(plain + fields, filter="wobble") + city + \
        f'<g opacity="0.85">{palms}</g>'
    return doc(body, defs)


def city_glow_svg():
    defs = S.rad_grad("s14cg", [(0, "#f6c25a", 0.85), (0.45, "#f0b040", 0.4), (1, "#f0b040", 0)])
    cx, cy = CITY_C
    return doc(f'<ellipse cx="{cx}" cy="{cy + 20}" rx="470" ry="210" fill="url(#s14cg)"/>', defs)


def _pts_path(pts):
    return "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts)


def _road_d():
    top = list(zip(ROAD_X, ROAD_TOP))
    bot = list(zip(ROAD_X, ROAD_BOT))
    return (S.smooth_path(top, closed=False, tension=0.8) + " L" +
            S.smooth_path(list(reversed(bot)), closed=False, tension=0.8)[1:] + " Z")


def land_svg():
    """Sea, beach, the golden meadow and the coast road (one static painting)."""
    ink = P["ink"]
    defs = (S.lin_grad("s14sea", [(0, S.mix(P["sea_pale"], P["sky_warm"], 0.2)), (0.22, P["sea_light"]),
                                  (1, P["sea"])])
            + S.lin_grad("s14mead", [(0, S.mix(P["grass"], P["sand_light"], 0.45)),
                                     (0.3, S.mix(P["grass"], P["sand"], 0.3)), (1, S.mix(P["grass"], P["sand"], 0.16))],
                         y1=0.0, y2=1.0)
            + S.lin_grad("s14road", [(0, "#f8ecd2"), (1, S.mix(P["sand_light"], "#fffaf0", 0.35))])
            + S.lin_grad("s14beach", [(0, S.mix(P["sand"], P["sky_warm"], 0.3)), (1, P["sand"])]))
    sea = (f'<rect x="-40" y="{HORIZON}" width="1120" height="{SH - HORIZON + 40}" fill="url(#s14sea)"/>'
           f'<path d="M-40,{HORIZON} L1060,{HORIZON}" stroke="{ink}" stroke-width="2.6"/>')
    rng = random.Random(7)
    dashes = ""
    for _ in range(70):
        y = HORIZON + 10 + (rng.random() ** 1.5) * 420
        k = (y - HORIZON) / 420
        x = rng.uniform(-40, 1000)
        if y > _shore_y_at(x) - 22:
            continue
        ln = 18 + 64 * k
        dashes += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln / 2)},{f1(-3 - 4 * k)} {f1(ln)},0" stroke="{P["foam"]}" '
                   f'stroke-width="{f1(2.0 + 2.6 * k)}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    land = S.smooth_path(SHORE + CREST[1:], closed=False, tension=0.85) + \
        f" L{SW + 60},{SH + 60} L-60,{SH + 60} Z"
    land_p = f'<path d="{land}" fill="url(#s14mead)" stroke="{ink}" stroke-width="3"/>'
    beach = S.smooth_path(SHORE, closed=False, tension=0.85)
    beach += " L" + " L".join(f"{f1(x)},{f1(y)}" for x, y in reversed(INNER)) + " Z"
    beach_p = f'<path d="{beach}" fill="url(#s14beach)" stroke="none"/>'
    wet = S.smooth_path([(x + 6, y + 9) for x, y in SHORE[:-1]], closed=False, tension=0.85)
    wet_p = f'<path d="{wet}" stroke="{S.mix(P["sand_dark"], P["sea_light"], 0.35)}" stroke-width="14" ' \
            f'fill="none" opacity="0.6"/>'
    inner_line = S.smooth_path(INNER, closed=False, tension=0.85)
    beach_edge = f'<path d="{inner_line}" stroke="{P["ink"]}" stroke-width="2.2" fill="none" opacity="0.55"/>'
    grass = ""
    for _ in range(190):
        x = rng.uniform(0, SW)
        y = rng.uniform(620, SH)
        if y < _land_top(x) + 12 or _near_road(x, y, 14) or y < _beach_inner_y(x) + 8:
            continue
        k = (y - 600) / 600
        h_ = 7 + 18 * k
        col = S.mix(P["grass_dark"], P["olive"], rng.random())
        grass += (f'<path d="M{f1(x)},{f1(y)} l{f1(-3 * k)},{f1(-h_)} M{f1(x + 5)},{f1(y)} l{f1(3 * k)},'
                  f'{f1(-h_ * 0.8)}" stroke="{col}" stroke-width="{f1(1.5 + 1.6 * k)}" stroke-linecap="round" '
                  f'opacity="0.6"/>')
    road_p = f'<path d="{_road_d()}" fill="url(#s14road)" stroke="{ink}" stroke-width="3"/>'
    peb = ""
    for _ in range(80):
        x = rng.uniform(-40, 1700)
        t0, b0 = _interp(ROAD_X, ROAD_TOP, x), _interp(ROAD_X, ROAD_BOT, x)
        y = rng.uniform(t0 + 8, b0 - 8)
        k = max(0.1, (y - 760) / 450)
        r = rng.uniform(2.5, 6.0) * (0.4 + k)
        peb += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.5)}" ry="{f1(r)}" fill="{P["sand_dark"]}" ' \
               f'opacity="0.45"/>'
    ruts = ""
    for off in (-0.24, 0.24):
        pts = []
        for x in range(-40, 1760, 40):
            t0, b0 = _interp(ROAD_X, ROAD_TOP, x), _interp(ROAD_X, ROAD_BOT, x)
            pts.append((x, (t0 + b0) / 2 + off * (b0 - t0)))
        ruts += f'<path d="{S.smooth_path(pts, closed=False)}" stroke="{S.mix(P["sand"], P["sand_light"], 0.4)}" ' \
                f'stroke-width="5" fill="none" opacity="0.6" stroke-linecap="round"/>'
    # a row of rounded edge stones along the near side of the road (as on the coastal road of s03)
    stones = ""
    x = -40.0
    while x < 1640:
        b0 = _interp(ROAD_X, ROAD_BOT, x)
        k = max(0.25, (b0 - 700) / 520)
        rx, ry = 20 * k + 6, 10 * k + 3
        stones += S.path(S.blob(x, b0 + ry * 0.5, rx, ry, 0.12, 8, int(x)), fill=S.mix(P["stone"], P["sand_light"], 0.3),
                         sw=2 + 1.2 * k)
        x += 2 * rx + 4
    body = (S.g(sea + dashes, filter="wobble") + S.g(land_p + beach_p + wet_p + beach_edge + grass, filter="wobble")
            + S.g(road_p + ruts + peb, filter="wobble") + S.g(stones, filter="wobble-fine"))
    deco = ""
    for x, y, s_, v in ((470, 860, 0.42, 0), (860, 700, 0.3, 1), (90, 1000, 0.5, 2)):
        deco += PR.reeds(x, y, s_, v)
    for x, y, s_, v in ((1060, 892, 0.42, 1), (1520, 808, 0.36, 3), (1850, 730, 0.3, 0), (2250, 720, 0.34, 2),
                        (2500, 790, 0.48, 3), (1980, 960, 0.62, 1), (2420, 1040, 0.7, 0)):
        deco += PR.bush(x, y, s_, v)
    for x, y, s_, v in ((900, 900, 0.5, 2), (1200, 880, 0.42, 1), (1640, 800, 0.38, 2), (2080, 770, 0.42, 0),
                        (2300, 880, 0.6, 2), (1600, 1010, 0.7, 2), (2150, 1060, 0.75, 0), (420, 1180, 0.8, 1),
                        (1100, 1110, 0.75, 1), (1350, 1050, 0.7, 2), (2560, 960, 0.7, 2), (1820, 900, 0.55, 1)):
        deco += PR.grass_tuft(x, y, s_, v)
    rocks = ""
    for x, y, rx, ry, seed in ((420, 922, 34, 18, 1), (458, 930, 18, 11, 2), (1250, 1090, 46, 24, 3),
                               (1880, 840, 28, 15, 4), (2300, 950, 50, 26, 5)):
        rocks += S.path(S.blob(x, y, rx, ry, 0.15, 8, seed), fill=P["stone_dark"], sw=3)
        rocks += f'<ellipse cx="{x - rx * 0.3}" cy="{y - ry * 0.35}" rx="{rx * 0.35}" ry="{ry * 0.22}" ' \
                 f'fill="{P["stone_light"]}" opacity="0.7"/>'
    shells = ""
    for x, y, c in ((260, 905, P["cheek"]), (520, 790, "#f4e3c8"), (80, 1040, "#f4e3c8"), (700, 724, P["cheek"])):
        shells += (f'<path d="M{x - 10},{y} Q{x},{y - 18} {x + 10},{y} Z" fill="{c}" stroke="{ink}" '
                   f'stroke-width="2.2"/><path d="M{x},{y} L{x},{y - 11} M{x - 5},{y} L{x - 3},{y - 9} '
                   f'M{x + 5},{y} L{x + 3},{y - 9}" stroke="{ink}" stroke-width="1.4"/>')
    flowers = ""
    cols = ("#e8706a", "#f2c14e", "#f4e3c8", "#c98ac0")
    for i in range(80):
        x = rng.uniform(700, SW)
        y = rng.uniform(690, 1150)
        if _near_road(x, y, 22) or y < _land_top(x) + 20 or y < _beach_inner_y(x) + 20:
            continue
        r = 2.5 + 4.5 * (y - 690) / 460
        flowers += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{cols[i % 4]}" stroke="{ink}" ' \
                   f'stroke-width="1.3"/>'
    sign = PR.signpost(SIGN[0], SIGN[1], SIGN[2])
    body += deco + S.g(rocks + shells + flowers, filter="wobble-fine") + sign
    return doc(body, defs)


def _shore_y_at(x):
    xs = [p[0] for p in SHORE]
    ys = [p[1] for p in SHORE]
    if x > xs[-1]:
        return HORIZON
    return _interp(xs, ys, x)


def _land_top(x):
    pts = SHORE + CREST[1:]
    pts = sorted(pts)
    return _interp([p[0] for p in pts], [p[1] for p in pts], x)


def _beach_inner_y(x):
    return _interp([p[0] for p in INNER], [p[1] for p in INNER], x)


def _near_road(x, y, m=0):
    if x > ROAD_X[-1]:
        return False
    return _interp(ROAD_X, ROAD_TOP, x) - m <= y <= _interp(ROAD_X, ROAD_BOT, x) + m


def sea_glints_svg(phase):
    rng = random.Random(40 + phase)
    body = ""
    for _ in range(16):
        x = rng.uniform(0, 960)
        y = rng.uniform(HORIZON + 8, 980)
        if y > _shore_y_at(x) - 24:
            continue
        k = (y - HORIZON) / 400
        ln = 14 + 30 * k
        body += (f'<path d="M{f1(x)},{f1(y)} l{f1(ln)},0" stroke="#fffaf0" stroke-width="{f1(2.4 + 2 * k)}" '
                 f'stroke-linecap="round" opacity="0.9"/>')
    return doc(body)


def swash_svg(k):
    """Foam line where the little waves run up the beach (two drawings that alternate softly)."""
    pts = [(x - 6 - 10 * k, y - 8 - 8 * k) for x, y in SHORE]
    d = S.smooth_path(pts, closed=False, tension=0.85)
    sc_ = ""
    for i in range(len(SHORE) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        for j in range(4):
            u = (j + 0.5) / 4
            x, y = xa + (xb - xa) * u, ya + (yb - ya) * u
            sc_ += f'<circle cx="{f1(x)}" cy="{f1(y + 2)}" r="{f1(9 - 4 * (y < 700))}" fill="{P["foam"]}"/>'
    body = (f'<path d="{d}" stroke="{P["ink"]}" stroke-width="2.6" fill="none"/>'
            f'<path d="{d}" stroke="{P["foam"]}" stroke-width="9" fill="none" stroke-linecap="round"/>' + sc_)
    return doc(S.g(body, filter="wobble-fine"))


def palm_svg(x, y, s_, lean, sway=0.0):
    return doc(PR.palm_tree(x, y, s_, lean=lean, sway=sway))


def tuft_svg(x, y, s_, v):
    return doc(PR.grass_tuft(x, y, s_, v))


def gull_frames(x, y, s_, facing):
    return [doc(PR.gull(x, y, s_, facing, wing=w)) for w in (1.0, 0.5, 0.0, -0.5, -1.0)]


BFLY = (1180, 800)


def butterfly_svg(open_k):
    """Small pale-yellow butterfly seen from above, wings opened by open_k (0..1) (as in s02)."""
    x, y = BFLY
    ink = P["ink"]
    k = max(0.12, open_k)
    out = ""
    for side in (-1, 1):
        ux, lx = x + side * 15 * k, x + side * 11 * k
        out += (f'<ellipse cx="{f1(ux)}" cy="{f1(y - 7)}" rx="{f1(15 * k)}" ry="13" fill="#f7d978" stroke="{ink}" '
                f'stroke-width="2.4" transform="rotate({-side * 18} {f1(ux)} {f1(y - 7)})"/>')
        out += (f'<ellipse cx="{f1(lx)}" cy="{f1(y + 9)}" rx="{f1(10 * k)}" ry="9" fill="#f3b45e" stroke="{ink}" '
                f'stroke-width="2.2"/>')
        out += f'<circle cx="{f1(x + side * 17 * k)}" cy="{f1(y - 9)}" r="{f1(3.2 * k + 1)}" fill="#e98a52"/>'
    out += f'<ellipse cx="{x}" cy="{y + 1}" rx="3.4" ry="13" fill="{P["ink_soft"]}" stroke="{ink}" stroke-width="1.6"/>'
    out += (f'<path d="M{x - 1},{y - 11} q-6,-10 -11,-12 M{x + 1},{y - 11} q6,-10 11,-12" fill="none" '
            f'stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def orb_svg(x, y):
    defs = S.rad_grad("s14orb", [(0, "#fffbe8", 1), (0.28, "#ffe48a", 0.9), (0.6, "#ffcf5a", 0.35),
                                 (1, "#ffc850", 0)])
    star = _star(x, y, 22, "#fff6d6")
    return doc(f'<circle cx="{x}" cy="{y}" r="78" fill="url(#s14orb)"/>' + star, defs)


def _star(cx, cy, r, fill, inner=0.26):
    w = r * inner
    pts = [(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r), (cx - w, cy + w),
           (cx - r, cy), (cx - w, cy - w)]
    return f'<path d="{_pts_path(pts)} Z" fill="{fill}"/>'


def _bez(p0, p1, p2, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])


TRAIL = ((JX + 60, JY - 245), (1150, 230), (CITY_C[0] - 30, CITY_C[1] - 30))


def trail_svg():
    """A dotted golden path from Jonah to the far city: 'tell the people in the city'."""
    defs = S.rad_grad("s14dot", [(0, "#fff3c0", 1), (0.5, "#ffd56a", 0.8), (1, "#ffc850", 0)])
    body = ""
    n = 34
    for i in range(n):
        u = (i + 0.5) / n
        x, y = _bez(*TRAIL, u)
        r = 9 - 3.5 * u
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 2.2)}" fill="url(#s14dot)"/>'
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.75)}" fill="#fff4cc"/>'
    return doc(body, defs)


# ====================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    L0, L1, L2 = L[0], L[1], L[2]
    w = lambda ph, k=0.0, d=None, after=0.0: _when(ctx, ph, k, d, after)   # noqa: E731

    # ---------------------------------------------------------------- beats (all from the narration)
    t_light = L0.start                                         # "上帝第二次...": the clouds part, light pours down
    t_open = w("对约拿说", 0.2, d=L0.start + 1.2)               # Jonah opens his eyes and looks up
    t_call = L1.start                                          # "约拿，": he cups his ear and listens
    t_city = w("尼尼微", 0.0, d=L1.start + 1.8, after=L1.start - 0.01) - 0.1   # the far city lights up
    t_look = t_city + 0.25                                     # ... and he looks over at it
    t_word = L1.at("把我告诉你的话")                             # God's word: a little light comes down to him
    t_orb1 = t_word + 1.0                                      # ... and melts into his heart
    # "说给城里的人听": a golden path to the city. God's voice lingers on this half of the chunk (the comma pause
    # sits at ~40 % of it on the voice take), so a character-count estimate would be late here.
    c_word = next(c for c in L1.chunks if "把我告诉你的话" in c.text) if L1.chunks else L1
    t_tell = c_word.start + 0.41 * (c_word.end - c_word.start) if "说给" in c_word.text else \
        w("说给", 0.0, d=t_word + 1.6, after=t_word)
    t_trail1 = t_tell + 1.5
    t_quiet = L1.end + 0.2                                     # God has finished speaking: the light softens
    t_obey = w("听话", 0.0, d=L2.start + 1.3, after=L2.start - 0.01) - 0.12   # "约拿听话了": he nods
    t_rise = L2.at("他起来") + 0.05                              # "他起来": he gets up, staff in hand
    t_stand = t_rise + 0.3
    t_walk = max(t_stand + 0.6, w("照着", 0.0, d=t_rise + 0.9, after=t_rise) - 0.05)   # sets off east
    t_end = T

    # ---------------------------------------------------------------- camera
    CAM0 = Cam(1000, 600, 2000)
    CAM_L1 = Cam(1010, 598, 1900)
    CAM_W = Cam(940, 604, 1780)
    cam = M.cam_keys([
        (0.0, CAM0),
        (t_call - 0.2, Cam(990, 600, 1940)),
        (t_word, CAM_L1),
        (t_quiet + 0.4, Cam(1000, 600, 1860)),
        (t_rise - 0.2, CAM_W),
        (t_walk + 0.3, Cam(960, 604, 1780)),
        (T, Cam(1250, 604, 1860)),
    ], ["sine", "sine", "sine", "sine", "sine", "inout"])
    sc.camera = cam
    cam_x0 = CAM_L1.x

    def par(k):
        return lambda t: Tf(dx=k * (cam(t).x - cam_x0))

    # ---------------------------------------------------------------- sky, clouds, God's light
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg([(1450, 105, 380, 105, 3), (2150, 75, 330, 95, 5), (2500, 170, 300, 90, 7),
                                 (110, 70, 300, 88, 9), (1850, 255, 220, 66, 11)]), z=1.0,
           motion=M.combine(M.drift(vx=6), par(0.35)))
    part = M.progress
    CL = (450, 185, 460, 138, 21)
    CR = (940, 150, 420, 126, 22)
    cl_m = lambda t: Tf(dx=-140 * part(t, t_light - 0.2, t_light + 1.5, "inout") + 3 * t)   # noqa: E731
    cr_m = lambda t: Tf(dx=150 * part(t, t_light - 0.2, t_light + 1.5, "inout") + 3 * t)    # noqa: E731
    sc.add("cloud_l", clouds_svg([CL]), z=1.1, motion=cl_m)
    sc.add("cloud_r", clouds_svg([CR]), z=1.2, motion=cr_m)

    def light_a(lo_after=0.35):
        def f(t):
            a = part(t, t_light, t_light + 1.1, "sine")
            a *= 1 - (1 - lo_after) * part(t, t_quiet, t_quiet + 1.6, "sine")
            a *= 1 - part(t, t_walk + 0.5, T, "sine") * 0.6
            return a * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.6))
        return f
    ray_alpha = light_a(0.35)
    ray_a = lambda t: Tf(alpha=ray_alpha(t))   # noqa: E731
    sc.add("rim_l", cloud_rim_svg(CL, GAP[0] - 10, 185, 150, 110, "l"), z=1.15, wc=0, motion=M.combine(cl_m, ray_a))
    sc.add("rim_r", cloud_rim_svg(CR, GAP[0] + 30, 160, 140, 100, "r"), z=1.25, wc=0, motion=M.combine(cr_m, ray_a))

    # ---------------------------------------------------------------- the far east: hills and Nineveh
    sc.add("far", far_svg(), z=2, wc=0.8, motion=par(0.3))
    city_a = lambda t: (part(t, t_city, t_city + 0.9, "sine") * (0.75 + 0.25 * math.sin(2 * math.pi * (t - t_city) / 2.2))
                        + 0.35 * math.sin(math.pi * _clamp((t - t_trail1 + 0.2) / 1.2))) * \
        (1 - 0.6 * part(t, L2.start, L2.start + 2.0, "sine"))   # noqa: E731
    sc.add("city_glow", city_glow_svg(), z=2.1, wc=0, blend="add",
           motion=M.combine(par(0.3), lambda t: Tf(alpha=min(0.85, 0.85 * city_a(t)))))

    # ---------------------------------------------------------------- the coast (static) + living water
    sc.add("land", land_svg(), z=3)
    for ph in (0, 1):
        sc.add(f"glint{ph}", sea_glints_svg(ph), z=3.1 + ph * 0.01, wc=0,
               motion=(lambda ph_: lambda t: Tf(alpha=0.5 + 0.5 * math.sin(t * 2.4 + math.pi * ph_)))(ph))
    sc.add("swash", [swash_svg(0.0), swash_svg(1.0)], z=3.2, wc=0.6,
           frame_at=lambda t: 0.5 - 0.5 * math.cos(2 * math.pi * t / 3.4))

    # gulls over the sea
    for i, (x, y, s_, f, vx, ph) in enumerate(((160, 330, 0.42, 1, 18, 0.0), (300, 280, 0.34, 1, 14, 0.4),
                                                (820, 420, 0.24, -1, -10, 0.2))):
        flap = (2, 1, 0, 1, 2, 3, 4, 3)
        sc.add(f"gull{i}", gull_frames(x, y, s_, f), z=3.3 + i * 0.01, wc=0.5,
               frame_at=(lambda ph_: lambda t: float(flap[int(t * 8 + ph_ * 8) % 8]) if (t + ph_ * 3) % 4.0 < 1.6
                         else 2.0)(ph),
               motion=M.combine(M.drift(vx=vx), M.bob(10, 2.2, ph)))

    # palms along the coast road
    palms = [(250, 905, 1.0, -0.3, 4.6), (930, 878, 0.6, 0.15, 5.0), (1010, 872, 0.5, -0.12, 4.2),
             (2080, 760, 0.52, 0.1, 4.8), (2180, 752, 0.45, -0.2, 5.2), (2440, 742, 0.48, 0.15, 4.4)]
    for i, (x, y, s_, ln, per) in enumerate(palms):
        sc.add(f"palm{i}", palm_svg(x, y, s_, ln), z=3.5 + i * 0.01,
               motion=M.sway(0.8, per, (x, y), phase=i * 0.21))

    # sheep grazing in the meadow (planted hooves, the heads dip to the grass: v1 s02 split)
    for i, (x, y, s_, f, per, ph) in enumerate(((1830, 965, 0.5, -1, 4.2, 0.0), (1975, 1000, 0.56, -1, 5.1, 0.45))):
        body, head = V2._sheep_parts(x, y, s_, f)
        br = M.breathe(0.012, 2.6 + 0.3 * i, pivot=(x, y), phase=0.3 * i)
        sc.add(f"sheep{i}", doc(C.ground_shadow(x, y, s_, width=180, opacity=0.2) + body), z=3.45 + i * 0.01,
               motion=br)
        if head:
            nx, ny = PR.local_to_stage(x, y, s_, f, *V2.SHEEP_NECK)

            def head_m(t, br=br, f=f, nx=nx, ny=ny, y=y, per=per, ph=ph):
                dip = 16 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / per + ph))) ** 3
                return Tf(dy=-(br(t).sy - 1) * (y - ny), rot=dip * f, px=nx, py=ny)
            sc.add(f"sheep{i}_head", doc(head), z=3.455 + i * 0.01, motion=head_m)

    # a butterfly over the flowers by the road
    sc.add("butterfly", [butterfly_svg(k) for k in (1.0, 0.55, 0.15)], z=7.5, wc=0.4,
           frame_at=lambda t: float((0, 1, 2, 1)[int(t * 14) % 4]),
           motion=lambda t: Tf(dx=120 * math.sin(2 * math.pi * t / 11.0) + 40 * math.sin(2 * math.pi * t / 3.9 + 1),
                               dy=40 * math.sin(2 * math.pi * t / 6.7 + 0.6) + 10 * math.sin(2 * math.pi * t * 1.6),
                               rot=8 * math.sin(2 * math.pi * t / 2.2)))

    # ---------------------------------------------------------------- golden rays (behind Jonah)
    src = (GAP[0] + 10, -220)
    tgt = (JX + 20, JY - 140)
    ray_m = M.combine(M.sway(0.8, 5.0, src), ray_a)
    sc.add("rays_mul", rays_svg(src, tgt, kind="mul"), z=4.0, wc=0, blend="multiply", motion=ray_m)
    sc.add("rays", rays_svg(src, tgt, kind="add"), z=4.1, wc=0, blend="add", motion=ray_m,
           reveal=lambda t: {"mode": "down", "frac": part(t, t_light, t_light + 0.9, "out"), "soft": 200})

    # ---------------------------------------------------------------- Jonah
    jdocs, J = [], {}

    def addf(key, svg):
        J[key] = len(jdocs)
        jdocs.append(svg)

    def jd(body, sw=120):
        return doc(C.ground_shadow(JX, JY, JS, sw) + body)
    kneel = lambda ps, e, **kw: jd(jonah_fig(JX, JY, JS, ps, e, **kw), 200)   # noqa: E731
    addf("pray", kneel(_KNEEL, "peaceful"))
    addf("up", kneel(KNEEL_UP, "neutral"))
    addf("listen", kneel(KNEEL_LISTEN, "happy"))
    addf("listen_b", kneel(KNEEL_LISTEN, "peaceful"))
    addf("look", kneel(KNEEL_LOOK, "happy"))
    addf("look_b", kneel(KNEEL_LOOK, "peaceful"))
    addf("chest", kneel(KNEEL_CHEST, "happy"))
    addf("chest_p", kneel(KNEEL_CHEST, "peaceful"))
    addf("city", kneel(KNEEL_CITY, "happy"))
    addf("city_b", kneel(KNEEL_CITY, "peaceful"))
    addf("nod", kneel(KNEEL_NOD, "happy"))
    addf("rise", jd(jonah_fig(JX, JY, JS, RISE, "happy", staff=(STAFF_DX, 0)), 170))
    addf("stand", jd(jonah_fig(JX, JY, JS, STAND_STAFF, "happy", staff=(STAFF_DX, 0))))
    addf("stand_b", jd(jonah_fig(JX, JY, JS, STAND_STAFF, "peaceful", staff=(STAFF_DX, 0))))
    w0 = len(jdocs)
    for k in range(2 * N_W):
        ps, tip = walk_staff_pose(k, A_W, N_W)
        addf(f"w{k}", jd(jonah_fig(JX, JY, JS, ps, "happy", staff=tip)))

    blink = 0.13
    ev = [(0.0, J["pray"]), (t_open, J["up"]), (t_call, J["listen"]),
          (t_call + 1.3, J["listen_b"]), (t_call + 1.3 + blink, J["listen"]),
          (t_look, J["look"]), (t_look + 1.0, J["look_b"]), (t_look + 1.0 + blink, J["look"]),
          (t_word, J["chest"]), (t_orb1 - 0.05, J["chest_p"]), (t_tell, J["city"]),
          (t_tell + 1.6, J["city_b"]), (t_tell + 1.6 + blink, J["city"]),
          (L2.start + 0.2, J["chest"]),
          (t_obey, J["nod"]), (t_obey + 0.26, J["chest"]), (t_obey + 0.52, J["nod"]),
          (min(t_obey + 0.82, t_rise - 0.12), J["chest"]),
          (t_rise, J["rise"]), (t_stand, J["stand"]), (t_stand + 0.35, J["stand_b"]),
          (t_stand + 0.35 + blink, J["stand"])]
    hops = [(t_call, 8), (t_rise, 10), (t_stand, 14)]
    squashes = [(t_open, 0.02), (t_look, 0.02), (t_word, 0.025), (t_tell, 0.02), (t_stand + 0.28, 0.04)]
    nods = [t_obey, t_obey + 0.52]
    n_draw = int(math.ceil((T + 0.2 - t_walk) / HOLD_W))
    xs = [JX]
    for i in range(n_draw + 1):
        xs.append(xs[-1] + 2 * A_W * walk_scale(xs[-1]) / N_W)
    stand_fa = _sched(ev)

    def j_fa(t):
        if t >= t_walk:
            i = int((t - t_walk) / HOLD_W)
            return float(w0 + (i % (2 * N_W)))
        return stand_fa(t)

    def j_m(t):
        sx = sy = 1.0
        for ts, k in squashes:
            a, b = _squash(t, ts, k)
            sx, sy = sx * a, sy * b
        dy = sum(_hop(t, th, h) for th, h in hops)
        if t >= t_walk:
            i = min(int((t - t_walk) / HOLD_W), len(xs) - 1)
            x = xs[i]
            s_ = walk_scale(x) / JS
            return Tf(dx=x - JX, dy=road_y(x) - JY, sx=s_, sy=s_, px=JX, py=JY)
        br = 1 + 0.008 * math.sin(2 * math.pi * t / 3.2)
        nod = sum(5 * math.sin(math.pi * _clamp((t - tn) / 0.3)) for tn in nods if tn <= t <= tn + 0.3)
        return Tf(dy=dy + nod, sx=sx, sy=sy * br, px=JX, py=JY)
    sc.add("staff", doc(staff_alone(JX + STAFF_DX * JS, JY, JS)), z=4.9,
           motion=lambda t: Tf(alpha=1.0 if t < t_rise else 0.0))
    sc.add("jonah", jdocs, z=5, frame_at=j_fa, motion=j_m, seed=141)

    # God's word: the little light that comes down to him, then the golden path to the city
    orb0 = (GAP[0] - 10, 300)
    orb1 = (JX + 30, JY - 222)
    t_orb0 = t_word + 0.05

    def orb_m(t):
        if t < t_orb0 or t > t_orb1 + 0.5:
            return Tf(alpha=0.0)
        u = M.ease("inout")(_clamp((t - t_orb0) / (t_orb1 - t_orb0)))
        x = orb0[0] + (orb1[0] - orb0[0]) * u + 60 * math.sin(math.pi * u)
        y = orb0[1] + (orb1[1] - orb0[1]) * u
        a = part(t, t_orb0, t_orb0 + 0.3, "sine")
        s_ = 0.8 + 0.08 * math.sin(2 * math.pi * t / 0.7)
        if t > t_orb1:
            v = (t - t_orb1) / 0.5
            s_ *= 1 + 0.7 * v
            a *= 1 - v
        return Tf(dx=x - orb0[0], dy=y - orb0[1], sx=s_, sy=s_, alpha=a, px=orb0[0], py=orb0[1])
    sc.add("orb", orb_svg(*orb0), z=6, wc=0, motion=orb_m)
    trail_alpha = lambda t: part(t, t_tell, t_tell + 0.2, "sine") * (1 - part(t, L2.start - 0.3, L2.start + 0.5, "sine"))   # noqa
    sc.add("trail", trail_svg(), z=6.1, wc=0, motion=lambda t: Tf(alpha=trail_alpha(t)),
           reveal=lambda t: {"mode": "left", "frac": part(t, t_tell, t_trail1, "inout"), "soft": 60})

    # ---------------------------------------------------------------- foreground
    for i, (x, y, s_, v) in enumerate(((200, 1180, 1.0, 0), (980, 1192, 0.95, 2), (1500, 1186, 1.0, 0),
                                       (1950, 1190, 1.05, 2), (2400, 1180, 1.0, 1))):
        sc.add(f"tuft{i}", tuft_svg(x, y, s_, v), z=8.1 + i * 0.01,
               motion=M.sway(2.2, 3.2 + 0.3 * i, (x, y), phase=0.19 * i))

    # warm wash over everything while the light is there (additive)
    sc.add("warm", warm_svg(), z=9, wc=0, blend="add", motion=lambda t: Tf(alpha=0.55 * ray_alpha(t)))

    # ---------------------------------------------------------------- effects
    sc.fx = [
        FX.motes((0, 200, SW, 1150), count=24, color=(255, 246, 214), size=(3, 6), alpha=100),
        # golden sparkles round Jonah while God speaks (three boxes that keep clear of his face)
        FX.sparkles((JX - 260, 280, JX + 300, JY - 420), count=14, t0=t_light + 0.4, t1=t_quiet + 1.0,
                    color=(255, 238, 170), size=(8, 18), period=1.7, drift=-8, seed=19),
        FX.sparkles((JX - 300, JY - 400, JX - 125, JY - 50), count=7, t0=t_light + 0.5, t1=t_quiet + 1.0,
                    color=(255, 238, 170), size=(7, 15), period=1.5, drift=-6, seed=23),
        FX.sparkles((JX + 75, JY - 400, JX + 300, JY - 50), count=7, t0=t_light + 0.6, t1=t_quiet + 1.0,
                    color=(255, 238, 170), size=(7, 15), period=1.9, drift=-6, seed=29),
        FX.sparkles((CITY[0] - 40, CITY_C[1] - 150, CITY[1] + 40, CITY[2] + 10), count=16, t0=t_city + 0.3,
                    t1=L2.start + 0.8, color=(255, 240, 180), size=(8, 16), period=1.3, drift=0, seed=31),
        FX.sparkles((orb1[0] - 90, orb1[1] - 80, orb1[0] + 90, orb1[1] + 60), count=10, t0=t_orb1 - 0.1,
                    t1=t_orb1 + 1.0, color=(255, 238, 170), size=(7, 14), period=0.9, drift=-10, seed=17),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-15, fade_in=0.8, fade_out=1.0, pan=-0.3)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-19, fade_in=0.8, fade_out=1.0)
    sc.sfx("gull", 0.4, gain_db=-20, pan=-0.6)
    sc.sfx("chime", t_light, gain_db=-7)
    sc.sfx("sparkle", t_city + 0.1, gain_db=-13, pan=0.5)
    sc.sfx("sparkle", t_orb1 - 0.1, gain_db=-12)
    sc.sfx("sparkle", t_trail1 - 0.3, gain_db=-14, pan=0.5)
    sc.sfx("cloth", t_rise, gain_db=-13)
    sc.sfx("footsteps", t_walk, dur=T - t_walk + 0.6, gain_db=-14, fade_in=0.1, fade_out=0.8,
           rate=1.0 / (N_W * HOLD_W))
    return sc
