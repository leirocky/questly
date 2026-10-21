"""Scene 11 — Pharaoh makes Joseph ruler over Egypt; the chariot; the seven good years (Genesis 41:37-49).

One wide 4300 x 1188 stage, one continuous take: on the left Pharaoh's columned throne hall (a cut-away hall with a
star ceiling, painted walls and a red runner), then outside a sunny street of white houses and palms with people
along the far side, then golden fields, the storehouses and the grain heaps on the right, pyramids on the horizon.

  opening        calm: Pharaoh on his throne, Joseph (clean white linen) standing before him; the chariot waits
                 outside the hall, the fan-bearer's fan sways.
  P '上帝和你同在' a soft golden beam from the high window settles round Joseph (light only).
  '没有人比你更聪明' Joseph bows politely, hand on his chest.
  '我要让你…'      Pharaoh rises from the throne (hop-cut, step forward) ...
  '管理全埃及'     ... and holds out the signet ring (glint); Joseph holds out his hands; the ring flies into them.
  N '漂亮的衣服'   a sparkle burst round Joseph hides the change into the ruler's white-and-gold robes (squash-hop).
  '金链子'         a second twinkle at his neck: the gold chain; he bows, hand on the pendant, proud.
  '坐上了大马车'   he turns, walks out to the chariot and hops in (whoosh); the horse trots off with a herald's horn,
                 wheels turning, dust puffs; the people along the street bow as he passes. The camera rides along.
  '七年丰收…'      the fields ripen to gold, sheaves pop up in rows; workers carry sacks to the storehouses.
  '存进仓库'       the granary silos fill step by step.
  '像山一样高'     the grain heaps grow up taller than the houses (soft whoosh / rising sound); the camera eases back.
  ending         calm: Joseph waving from his chariot beside the mountains of grain.

Pose changes are hard cuts hidden by squash-hops (never crossfades between poses). Helpers here are reused by
s12_brothers and s13_forgive.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 4400, 1188
INK = P["ink"]
G = 960                     # ground line of the hall and the street (everybody's feet)
HZ = 770                    # horizon outside
PX = 420                    # Pharaoh's throne
PX_STAND = PX + 92          # where he stands after rising
JX = 860                    # Joseph before Pharaoh
CX0, CX1 = 1272, 2350       # the chariot (ground under the wheel): waiting, and stopped at the storehouses
J_STOP = 1146               # Joseph's last walking step before he hops into the chariot
HALL_R = 1236               # the hall's open right edge
GRAN_X, GRAN_Y = 3530, 878  # the storehouses
HEAPS = [(2990, 892, 1.9, 3), (3945, 894, 2.1, 5)]   # (x, y, final size, seed)

PUNCT = "，。；：？！、,.;:?!"


# ============================================================================ shared helpers (s12 / s13 too)


def f1(v):
    return f"{v:.1f}"


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


def with_blinks(entries, blink_of, times, dur=0.13, guard=0.35):
    """Add blinks (hard cuts to an eyes-closed copy of the held drawing) at ``times`` unless a cut is near."""
    entries = sorted(entries, key=lambda e: e[0])
    out = list(entries)
    for tb in times:
        tb = snap(tb)
        if any(abs(tb - tk) < guard or abs(tb + dur - tk) < guard for tk, _ in entries):
            continue
        cur = None
        for tk, i in entries:
            if tk <= tb:
                cur = i
        if cur is None or cur not in blink_of:
            continue
        out += [(tb, blink_of[cur]), (snap(tb + dur), cur)]
    return sorted(out, key=lambda e: e[0])


def when(ctx, phrase, line=None):
    """Start time of ``phrase``: its chunk start, or its character position inside the chunk."""
    lines = ctx.lines if line is None else [ctx.lines[line]]
    for ln in lines:
        for ch in ln.chunks:
            if phrase in ch.text:
                k = ch.text.index(phrase)
                if k == 0:
                    return ch.start
                body = ch.text.rstrip(PUNCT)

                def w(s):
                    return sum(0.5 if c in PUNCT else 1.0 for c in s)
                return ch.start + (ch.end - ch.start) * w(ch.text[:k]) / max(1.0, w(body))
    raise KeyError(phrase)


def hop(t0, keys, pivot, curves="sine"):
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


def dip(t0, s, pivot, depth=9.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": 0.95}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pivot, ["in", "out", "sine"])


def happy_hop(t0, s, pivot, h=18.0):
    """Squash at t0 (cut there), then a little jump."""
    return hop(t0, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5 * s, "sy": 0.94}), (0.17, {"dy": -h * s, "sy": 1.04}),
                    (0.34, {"dy": 0, "sy": 0.97}), (0.46, {"dy": 0, "sy": 1})], pivot,
               ["in", "out", "in", "sine"])


def step_walk(t0, n, step, period, s, move=0.12, lift=7.0):
    """Planted-foot walk with two stride drawings: each drawing holds its anchor still; as the next cuts in, the
    anchor advances one stride with a short ease and a little lift. Returns (frame_at -> 0/1 or None, dx, dy, t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]
    t_end = snap(t0 + n * period)

    def fa(t):
        if t < cut_t[0] or t >= t_end:
            return None
        k = min(n - 1, int((t - t0) / period))
        return float(k % 2)

    def dx(t):
        return sum(step * M.progress(t, ck - move * 0.45, ck + move * 0.55, "sine") for ck in cut_t)

    def dy(t):
        y = 0.0
        for ck in cut_t:
            if ck - move * 0.45 <= t <= ck + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - ck + move * 0.45) / move)
        return y
    return fa, dx, dy, t_end


def trap(a=0.3):
    """Ease with a trapezoid velocity profile (sine ramps over the first and last ``a``, cruise between)."""
    def f(u):
        if u <= 0:
            return 0.0
        if u >= 1:
            return 1.0
        if u < a:
            s = u / 2 - a / (2 * math.pi) * math.sin(math.pi * u / a)
        elif u <= 1 - a:
            s = a / 2 + (u - a)
        else:
            w = 1 - u
            s = (1 - a) - (w / 2 - a / (2 * math.pi) * math.sin(math.pi * w / a))
        return s / (1 - a)
    return f


def clamp_cam(c, sw, sh, margin=4):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), sw - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), sh - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys, sw, sh):
    """[(t, Cam[, curve])]: eased moves (bottom edge interpolated, clamped to the stage)."""
    keys = [(k[0], clamp_cam(k[1], sw, sh), k[2] if len(k) > 2 else "sine") for k in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, cv), (t1, b, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, cv)
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w), sw, sh)
        return keys[-1][1]
    return cam


def blink(e):
    """Name of an eyes-closed copy of expression ``e`` (registered in the shared table once)."""
    key = f"jx_blink_{e}"
    C.EXPRS.setdefault(key, dict(C.EXPRS[e], eyes="closed"))
    return key


def joseph_bare(x, y, scale=1.0, facing=1, pose="stand", expr=None, chain=True, ring=True, marks=True):
    """Joseph in the ruler's robes WITHOUT the court headcloth (his own dark curls: '我就是约瑟')."""
    D = C._joseph_design("ruler", "colours", 1.0, chain, ring, pose)
    D.update(hat=("custom", C._joseph_curls), hat_h=0.12, hair=C.JOSEPH_HAIR)
    D.pop("ears", None)
    ps = C._js_pose(pose)
    if pose in C._JS_ADULT_NATURAL:
        ps["expr"] = C._JS_ADULT_NATURAL[pose]
    elif pose in C._JS_NATURAL:
        ps["expr"] = C._JS_NATURAL[pose]
    inner, _ = C._figure(D, C._JOSEPH_M, ps, expr or ps["expr"], C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, scale, facing, f"joseph-bare-{pose}")


def star_path(x, y, r, w=0.24):
    w = r * w
    return (f"M{f1(x)},{f1(y - r)} L{f1(x + w)},{f1(y - w)} L{f1(x + r)},{f1(y)} L{f1(x + w)},{f1(y + w)} "
            f"L{f1(x)},{f1(y + r)} L{f1(x - w)},{f1(y + w)} L{f1(x - r)},{f1(y)} L{f1(x - w)},{f1(y - w)} Z")


def burst_markup(cx, cy, k, n_frames=6, r0=60, r1=230, n=12, seed=1, size=24):
    """Frame k of an expanding ring of twinkling stars (a 'sparkle burst' hiding a costume change)."""
    rng = random.Random(seed)
    u = k / (n_frames - 1)
    out = ""
    for i in range(n):
        a = 2 * math.pi * (i + 0.5 * (i % 2)) / n + rng.uniform(-0.15, 0.15)
        rr = (r0 + (r1 - r0) * u) * rng.uniform(0.75, 1.1)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a) * 1.25
        sz = size * rng.uniform(0.7, 1.2) * (1.0 - 0.55 * u)
        out += (f'<path d="{star_path(x, y, sz)}" fill="#fff1b8" stroke="{P["ink_soft"]}" stroke-width="2.2"/>')
    return S.g(out, filter="wobble-fine")


def twinkles_markup(pts, k):
    out = ""
    for i, (x, y, r) in enumerate(pts):
        r = r * (0.65 + 0.35 * ((i + k) % 3) / 2)
        out += f'<path d="{star_path(x, y, r)}" fill="#ffe9a0" stroke="{P["ink_soft"]}" stroke-width="2"/>'
    return S.g(out, filter="wobble-fine")


def arcs_markup(x, y, dirx, diry, k, s=1.0):
    """'Speaking' sound arcs travelling along (dirx, diry) from a mouth (k = 1..3 flicker)."""
    out = ""
    ang = math.atan2(diry, dirx)
    for i in range(3):
        r = (16 + 16 * i + (k - 2) * 2.5) * s
        a0, a1 = ang - 0.75, ang + 0.75
        p0 = (x + r * math.cos(a0), y + r * math.sin(a0))
        p1 = (x + 1.25 * r * math.cos(ang), y + 1.25 * r * math.sin(ang))
        p2 = (x + r * math.cos(a1), y + r * math.sin(a1))
        d = f"M{f1(p0[0])},{f1(p0[1])} Q{f1(p1[0])},{f1(p1[1])} {f1(p2[0])},{f1(p2[1])}"
        out += (f'<path d="{d}" fill="none" stroke="#fff6e2" stroke-width="{11 * s:.1f}" stroke-linecap="round" '
                f'opacity="0.55"/><path d="{d}" fill="none" stroke="{INK}" stroke-width="{5 * s:.1f}" '
                f'stroke-linecap="round" opacity="0.85"/>')
    return S.g(out, filter="wobble-fine")


def puff_markup(cx, cy, rx, ry, seed=0, col="#efe0c6"):
    rng = random.Random(seed)
    out = ""
    for i in range(7):
        a = 2 * math.pi * i / 7
        out += (f'<circle cx="{f1(cx + rx * 0.7 * math.cos(a))}" cy="{f1(cy + ry * 0.6 * math.sin(a))}" '
                f'r="{f1(ry * rng.uniform(0.4, 0.6))}" fill="{col}" stroke="{INK}" stroke-width="3" opacity="0.9"/>')
    return S.g(out, filter="wobble-fine")


def speaking(intervals, fps=8):
    """frame_at for speaking arcs: frames 0..2 flicker inside the intervals; alpha via speaking_alpha."""
    return lambda t: float(int(t * fps) % 3)


def speaking_alpha(intervals, fade=0.15):
    def m(t):
        a = 0.0
        for t0, t1 in intervals:
            a = max(a, min(M.progress(t, t0, t0 + fade, "sine"), 1 - M.progress(t, t1 - fade, t1, "sine")))
        return Tf(alpha=a)
    return m


# ============================================================================ backdrop


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def sky_svg():
    defs = S.lin_grad("sky11", [(0, "#8cc4dc"), (0.6, "#c6e3e8"), (1, "#f7e5bd")])
    defs += S.rad_grad("sun11", [(0, "#fff6d6", 0.95), (0.35, "#fde7a8", 0.45), (1, "#fde7a8", 0)])
    body = f'<rect x="-20" y="-20" width="{SW + 40}" height="{HZ + 80}" fill="url(#sky11)"/>'
    body += (f'<circle cx="3900" cy="170" r="420" fill="url(#sun11)"/>'
             f'<circle cx="3900" cy="170" r="74" fill="{P["sun"]}" stroke="#f0b062" stroke-width="5" filter="url(#wobble)"/>')
    return doc(body, defs)


CLOUDS = [(1500, 150, 300, 86, 1), (2150, 90, 260, 74, 2), (2800, 200, 340, 92, 3), (3450, 110, 280, 80, 4),
          (4150, 330, 240, 66, 5), (1900, 330, 200, 54, 6), (3100, 380, 210, 56, 7)]


def clouds_svg():
    out = "".join(S.cloud(cx, cy, w, h, fill="#fdf6ea", seed=sd, sw=3, shade_fill="#e3e6e2")
                  for cx, cy, w, h, sd in CLOUDS)
    return doc(S.g(out, filter="wobble"))


def far_svg():
    """Horizon outside: pyramids, desert, far palms, the fields and the far houses."""
    out = ""
    defs = S.lin_grad("land11", [(0, "#e7cf98"), (1, "#d9b878")])
    out += S.path(S.hill(1100, 2600, HZ + 6, 34, seed=3, bottom=HZ + 60, bumps=3), "#ecd7a6", sw=3)
    out += PR.pyramids(2050, HZ + 8, 0.42, n=3, haze=0.45, ground=False)
    out += PR.pyramids(3560, HZ + 4, 0.26, n=2, haze=0.6, ground=False, facing=-1)
    out += S.path(S.wave_line(HZ, 4, 700, 0, 1100, SW + 40) + f" L{SW + 40},{SH + 30} L1100,{SH + 30} Z", "url(#land11)", sw=3)
    for x, s, ln in ((1420, 0.42, 0.1), (2620, 0.38, -0.1), (2780, 0.33, 0.15), (4020, 0.36, -0.12), (4240, 0.3, 0.1)):
        out += PR.palm_tree(x, HZ + 12, s, lean=ln)
    # the far houses beyond the fields (the fields hide their feet)
    out += PR.egypt_house(2620, HZ + 10, 0.42, variant=0)
    out += PR.egypt_house(4330, HZ + 18, 0.46, variant=0, facing=-1)
    return doc(out, defs)


def field_svg(ripe):
    return doc(PR.field(2330, SW + 60, HZ - 6, depth=120, ripe=ripe, seed=4))


def street_svg():
    """The street: houses and palms on the far side, the sandy road in front, the yard of the storehouses."""
    out = ""
    # houses along the street, the hall's side wall hides the first one's left edge
    out += PR.egypt_house(1560, 852, 0.6, variant=0)
    out += PR.palm_tree(1800, 846, 0.62, lean=-0.08)
    out += PR.egypt_house(2090, 852, 0.62, variant=1)
    out += PR.palm_tree(2420, 860, 0.58, lean=0.12)
    out += PR.bush(1350, 862, 0.5, variant=1) + PR.bush(2560, 866, 0.45, variant=2)
    # the road: a sand band from the hall to the right edge, with a pale track and stones along its edge
    road = (f"M{HALL_R - 20},{858} C1800,{850} 2600,{872} {SW + 40},{868} L{SW + 40},{SH + 30} L{HALL_R - 20},{SH + 30} Z")
    out += S.path(road, "#efd9a8", sw=3.5)
    track = f"M{HALL_R},{935} C1900,{928} 2900,{948} {SW + 40},{940} L{SW + 40},{1000} C2900,{1006} 1900,{990} {HALL_R},{996} Z"
    out += S.path(track, "#f6e6c2", stroke=False)
    rng = random.Random(8)
    for i in range(40):
        x = HALL_R + 30 + i * 78 + rng.uniform(-10, 10)
        y = 858 + 6 * math.sin(x / 300) + rng.uniform(-2, 4)
        out += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(14, 24))}" ry="7" fill="#d9c08c" stroke="{INK}" stroke-width="2.5"/>'
    for i in range(70):
        x = rng.uniform(HALL_R + 20, SW)
        y = rng.uniform(880, SH - 10)
        out += f'<path d="M{f1(x)},{f1(y)} q7,-3 14,0" fill="none" stroke="#c8a66e" stroke-width="2.4" opacity="0.6"/>'
    for x, y, v in ((1290, 1080, 0), (2240, 1110, 2), (3020, 1095, 1), (3900, 1120, 0), (4230, 1060, 2)):
        out += PR.grass_tuft(x, y, 0.8, variant=v)
    return doc(S.g(out))


def hall_svg():
    """Pharaoh's throne hall, cut away: star ceiling, painted back wall with a high window, columns, a red runner."""
    out = ""
    R = HALL_R
    defs = S.lin_grad("wall11", [(0, "#efd9a9"), (1, "#e0c38e")])
    defs += S.lin_grad("floor11", [(0, "#d9b98a"), (1, "#c9a576")])
    defs += S.lin_grad("ceil11", [(0, "#2f4f86"), (1, "#3c62a0")])
    defs += S.lin_grad("win11", [(0, "#a9d6e6"), (1, "#f4e2b8")])
    wall_top, wall_bot = 175, 790
    out += f'<rect x="-30" y="{wall_top}" width="{R + 30}" height="{wall_bot - wall_top + 4}" fill="url(#wall11)"/>'
    # the high window (sky and a far pyramid), its golden beam is a separate layer
    wx0, wx1, wy0, wy1 = 860, 1010, 300, 470
    out += (f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="url(#win11)" '
            f'stroke="{INK}" stroke-width="5"/>')
    out += f'<path d="M{wx0 + 20},{wy1} L{wx0 + 75},{wy1 - 60} L{wx0 + 130},{wy1} Z" fill="#e8cf96" stroke="{INK}" stroke-width="3"/>'
    for k in range(1, 4):
        xx = wx0 + k * (wx1 - wx0) / 4
        out += f'<rect x="{f1(xx - 5)}" y="{wy0}" width="10" height="{wy1 - wy0}" fill="#b8915c" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="{wx0 - 14}" y="{wy1}" width="{wx1 - wx0 + 28}" height="18" fill="#cdae78" stroke="{INK}" stroke-width="4"/>'
    # painted friezes: a block band under the ceiling and a lotus band above the floor
    cols = ["#3f6fa8", "#c9533f", "#e8c25a", "#4f8a6a"]
    for i, x in enumerate(range(-30, R, 46)):
        out += f'<rect x="{x}" y="{wall_top + 6}" width="40" height="34" fill="{cols[i % 4]}" opacity="0.85"/>'
        out += f'<rect x="{x + 14}" y="{wall_top + 12}" width="12" height="22" fill="#f6e7c0" opacity="0.8"/>'
    out += f'<path d="M-30,{wall_top + 44} L{R},{wall_top + 44}" stroke="{INK}" stroke-width="4"/>'
    for i, x in enumerate(range(-10, R, 64)):
        y0 = wall_bot - 74
        out += (f'<path d="M{x},{y0 + 50} Q{x - 18},{y0 + 18} {x - 8},{y0} Q{x},{y0 + 14} {x + 8},{y0} '
                f'Q{x + 18},{y0 + 18} {x},{y0 + 50} Z" fill="{"#3f6fa8" if i % 2 else "#4f8a6a"}" stroke="{INK}" stroke-width="2.6"/>')
        out += f'<circle cx="{x + 32}" cy="{y0 + 30}" r="9" fill="#c9533f" stroke="{INK}" stroke-width="2.4"/>'
    out += f'<path d="M-30,{wall_bot - 82} L{R},{wall_bot - 82}" stroke="{INK}" stroke-width="3" opacity="0.7"/>'
    # wall paintings: tall papyrus clumps and two big painted lotus flowers
    for x in (230, 600, 1120):
        for j, dx in enumerate((-26, 0, 26)):
            h = 250 - 30 * abs(dx) / 26
            out += f'<path d="M{x + dx * 0.4},{wall_bot - 90} L{x + dx},{wall_bot - 90 - h}" stroke="#4f8a6a" stroke-width="7"/>'
            out += (f'<path d="M{x + dx},{wall_bot - 90 - h} l-22,-34 q22,-12 44,0 Z" fill="#6fa86a" stroke="{INK}" '
                    f'stroke-width="2.6" opacity="0.9"/>')
    # columns along the back wall
    for x in (110, 420, 760, 1130):
        out += PR.egypt_column(x, wall_bot + 2, 1.2, height=500)
    # the star ceiling and its cornice
    out += f'<rect x="-30" y="-30" width="{R + 30}" height="{wall_top + 30}" fill="url(#ceil11)"/>'
    rng = random.Random(2)
    for i in range(46):
        x, y = rng.uniform(0, R - 20), rng.uniform(10, wall_top - 40)
        out += f'<path d="{star_path(x, y, 9, 0.3)}" fill="#f2c14e"/>'
    out += f'<rect x="-30" y="{wall_top - 34}" width="{R + 50}" height="34" fill="#e8c25a" stroke="{INK}" stroke-width="4"/>'
    for x in range(-20, R + 20, 30):
        out += f'<rect x="{x}" y="{wall_top - 28}" width="12" height="22" fill="{"#3f6fa8" if (x // 30) % 2 else "#c9533f"}"/>'
    # the floor and the red runner from the throne to the door
    out += f'<rect x="-30" y="{wall_bot}" width="{R + 30}" height="{SH - wall_bot + 30}" fill="url(#floor11)"/>'
    for k, y in enumerate((812, 846, 890, 945, 1010, 1085)):
        out += f'<path d="M-30,{y} L{R},{y}" stroke="#b38e5e" stroke-width="2.5" opacity="0.6"/>'
    for x in range(-60, R + 200, 150):
        out += f'<path d="M{x},{wall_bot} L{x - (x - 600) * 0.45},{SH + 30}" stroke="#b38e5e" stroke-width="2.5" opacity="0.5"/>'
    out += f'<path d="M-30,{wall_bot} L{R},{wall_bot}" stroke="{INK}" stroke-width="4"/>'
    run = f"M{PX - 40},{918} L{R + 4},{912} L{R + 4},{1012} L{PX - 70},{1018} Z"
    out += S.path(run, "#b8433a", sw=3.5)
    out += f'<path d="M{PX - 50},{930} L{R},{924} M{PX - 62},{1004} L{R},{999}" stroke="#e8c25a" stroke-width="6"/>'
    # the hall's cut-away side wall at the right edge (sandstone slab, its top under the cornice)
    out += f'<rect x="{R - 30}" y="{wall_top - 40}" width="44" height="{wall_bot - wall_top + 44}" fill="#e3c792" stroke="{INK}" stroke-width="4"/>'
    out += f'<rect x="{R - 30}" y="{wall_top - 60}" width="60" height="30" fill="#d9b878" stroke="{INK}" stroke-width="4"/>'
    out += f'<path d="M{R + 14},{wall_bot} L{R + 14},{SH + 30}" stroke="{INK}" stroke-width="3" opacity="0.6"/>'
    return doc(S.g(out, filter="wobble"), defs)


def front_svg():
    """Foreground frame: a big column at the hall's left edge and a potted palm in the street corner."""
    out = PR.egypt_column(30, SH + 40, 1.9, height=520)
    out += PR.papyrus(1325, 1180, 1.2) + PR.papyrus(4170, 1180, 1.1)
    # by the storehouses: full sacks, a jar and a sheaf waiting at the roadside
    out += PR.grain_sacks(3640, 1150, 1.05, n=3, open_=True) + PR.grain_sacks(3830, 1160, 0.9, n=2)
    out += PR.jar(2480, 1150, 1.0) + PR.wheat_sheaf(2620, 1160, 0.75, -1, seed=4)
    out += PR.grass_tuft(2900, 1150, 0.9, variant=1) + PR.grass_tuft(4020, 1140, 0.8, variant=2)
    return doc(out)


def fan_markup(x, y):
    """A big feather fan on a pole (the fan-bearer's), its handle end at (x, y)."""
    top = (x + 20, y - 300)
    out = (f'<path d="M{x},{y} L{top[0]},{top[1]}" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
           f'<path d="M{x},{y} L{top[0]},{top[1]}" stroke="{P["gold"]}" stroke-width="7" stroke-linecap="round"/>')
    fx, fy = top
    for i, (a, col) in enumerate(zip(range(-70, 71, 20), ["#f6efe0", "#3f6fa8", "#f6efe0", "#e8c25a",
                                                          "#f6efe0", "#3f6fa8", "#f6efe0", "#e8c25a"])):
        r = math.radians(a - 90)
        ex, ey = fx + 120 * math.cos(r), fy + 120 * math.sin(r)
        out += (f'<path d="M{f1(fx)},{f1(fy)} Q{f1(fx + 70 * math.cos(r - 0.25))},{f1(fy + 70 * math.sin(r - 0.25))} '
                f'{f1(ex)},{f1(ey)} Q{f1(fx + 70 * math.cos(r + 0.25))},{f1(fy + 70 * math.sin(r + 0.25))} {f1(fx)},{f1(fy)} Z" '
                f'fill="{col}" stroke="{INK}" stroke-width="3"/>')
    out += f'<circle cx="{f1(fx)}" cy="{f1(fy)}" r="14" fill="{P["gold"]}" stroke="{INK}" stroke-width="3.5"/>'
    return S.g(out, filter="wobble-fine")


def beam_svg():
    """God's presence: a soft golden beam from the high window onto Joseph (light only)."""
    defs = S.rad_grad("gl11", [(0, "#fff3c4", 0.95), (0.55, "#ffe39a", 0.4), (1, "#ffe39a", 0)])
    body = (f'<path d="M870,300 L1000,300 L{JX + 150},{G + 10} L{JX - 170},{G + 10} Z" fill="#fff0bf" opacity="0.55" '
            f'filter="url(#blur-md)"/>'
            f'<ellipse cx="{JX}" cy="{G - 170}" rx="230" ry="260" fill="url(#gl11)"/>')
    return doc(body, defs)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]
    s = 1.0

    # ---- key times ----
    t_god = snap(L0.start + 0.15)                       # '上帝和你同在': the golden beam
    t_bow = snap(when(ctx, "没有人比你更聪明") + 0.2)     # Joseph bows politely
    t_rise = snap(L0.at("我要让你") - 0.1)               # Pharaoh rises
    t_ring = snap(when(ctx, "管理全埃及") - 0.05)         # holds out the ring
    t_hands = snap(t_ring + 0.4)                        # Joseph holds out his hands
    t_fly0 = snap(t_ring + 0.95)                        # the ring flies into them
    t_fly1 = t_fly0 + 0.45
    t_clothes = snap(when(ctx, "漂亮的衣服") - 0.05)      # sparkle burst: the ruler's robes
    t_chain = snap(when(ctx, "金链子") - 0.05)            # twinkle: the gold chain
    t_turn = snap(t_chain + 0.55)                       # he turns to go
    WALK_P = 0.24
    n_steps = 3
    step = (J_STOP - JX) / n_steps
    t_walk0 = snap(t_turn + 0.16)
    fa_w, dxw, dyw, t_walk1 = step_walk(t_walk0, n_steps, step, WALK_P, s)
    t_jump = snap(max(t_walk1 + 0.04, L1.at("坐上了") + 0.35))
    t_land = snap(t_jump + 0.36)
    t_go = snap(t_land + 0.3)                           # the horse sets off (horn)
    t_stop = t_go + 3.3
    t_ripe = L2.start + 0.05                            # '七年丰收的时候'
    t_sheaf = L2.start + 1.2
    t_store = snap(when(ctx, "存进仓库") - 0.15)          # the silos fill
    t_heap = snap(L2.at("粮食堆得") + 0.05)               # the heaps grow ...
    t_high = when(ctx, "像山一样高")                      # ... like mountains

    ease_drive = trap(0.32)

    def cx_at(t):
        return CX0 + (CX1 - CX0) * ease_drive((t - t_go) / (t_stop - t_go))

    def speed_at(t):
        return abs(cx_at(t + 0.02) - cx_at(t - 0.02)) / 0.04

    # ---- camera ----
    CA = Cam(1000, 600, 1950)
    CB = Cam(1240, 600, 1950)
    C_END = Cam(3100, 600, 1980)
    C_WIDE = Cam(3130, 594, 2100)

    t_pan0, t_pan1 = t_turn + 0.1, t_stop + 0.45
    ease_pan = trap(0.34)

    def cam(t):
        # one long, calm glide from the hall to the storehouses (it starts as Joseph walks out; the chariot,
        # quicker in the middle, stays in the frame all the way)
        u = ease_pan((t - t_pan0) / (t_pan1 - t_pan0))
        c = Cam(M.lerp(CA.x, C_END.x, u), 600, M.lerp(CA.w, C_END.w, u))
        kz = M.progress(t, t_heap - 0.2, t_heap + 2.2, "sine")
        c = Cam(M.lerp(c.x, C_WIDE.x, kz), M.lerp(c.y, C_WIDE.y, kz), M.lerp(c.w, C_WIDE.w, kz))
        return clamp_cam(c, SW, SH)
    sc.camera = cam

    # ---- backdrop ----
    sc.add("sky", sky_svg(), z=0, wc=0.5, seed=11)
    sc.add("clouds", clouds_svg(), z=0.5, wc=0.6, motion=M.drift(vx=-6), seed=12)
    sc.add("far", far_svg(), z=1, seed=13)
    # the fields ripen from green to gold ('七年丰收')
    ripes = [0.3, 0.5, 0.7, 0.85, 1.0]
    sc.add("field", [field_svg(r) for r in ripes], z=1.2, seed=14,
           frame_at=lambda t: float(min(len(ripes) - 1, max(0, int((t - t_ripe) / 0.22) + 1))) if t >= t_ripe else 0.0)
    # harvest: sheaves pop up in rows in the field
    sheaves = []
    rng = random.Random(5)
    for row, (y, sz) in enumerate(((812, 0.34), (842, 0.4))):
        for i in range(9):
            x = 2420 + i * 205 + row * 100 + rng.uniform(-20, 20)
            if 3120 < x < 3940:
                continue
            sheaves.append((x, y, sz, rng.randint(0, 9)))
    for i, (x, y, sz, sd) in enumerate(sheaves):
        t_pop = t_sheaf + 0.09 * i
        sc.add(f"sheaf{i}", doc(PR.wheat_sheaf(x, y, sz, 1 if i % 2 else -1, seed=sd)), z=1.3, seed=200 + i,
               motion=M.combine(hop(t_pop, [(0, {"s": 0.01}), (0.25, {"s": 1.08}), (0.4, {"s": 1.0})], (x, y),
                                    ["out", "sine"]),
                                lambda t, i=i, x=x, y=y: Tf(rot=1.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.13)),
                                                            px=x, py=y)))
    # the storehouses fill step by step ('存进仓库')
    fills = [round(0.1 * k, 1) for k in range(11)]
    sc.add("granary", [doc(PR.granary(GRAN_X, GRAN_Y, 0.95, fill=f)) for f in fills], z=1.4, seed=15,
           frame_at=lambda t: float(min(10, max(0, int((t - t_store) / 0.13) + 1))) if t >= t_store else 0.0)
    # grain heaps 'like mountains': growing from small mounds, taller than the houses
    for i, (x, y, size, sd) in enumerate(HEAPS):
        t0 = t_heap + 0.25 * i
        t1 = t_high + 0.6 + 0.2 * i

        def heap_m(t, x=x, y=y, size=size, t0=t0, t1=t1):
            u = M.progress(t, t0, t1, "out")
            k = (0.28 + 0.72 * u) + 0.03 * math.sin(math.pi * M.progress(t, t1 - 0.1, t1 + 0.35, "linear"))
            return Tf(sx=0.62 + 0.16 * k, sy=k, px=x, py=y)
        sc.add(f"heap{i}", doc(PR.grain_heap(x, y, 1.0, size=size, seed=sd)), z=1.5 + 0.01 * i, motion=heap_m,
               seed=30 + i)
    sc.add("street", street_svg(), z=1.7, seed=16)

    # workers carrying sacks to the storehouses (walking all the time on the yard path)
    WS = 0.82
    for i, (x0, v) in enumerate(((2500, 0), (2300, 2), (2100, 1))):
        yy = 902
        fa_c, dxc, dyc, _ = step_walk(12.0 + 0.11 * i, 40, 58 * WS, 0.34, WS)
        fr = [doc(C.ground_shadow(x0, yy, WS, 110) + C.egyptian(x0, yy, WS, 1, kind="servant", variant=v,
                                                                 pose=p, item="sack"))
              for p in ("carry_walk_a", "carry_walk_b")]
        sc.add(f"worker{i}", fr, z=1.8 + 0.01 * i, seed=60 + i,
               frame_at=lambda t, fa_c=fa_c: fa_c(t) or 0.0,
               motion=lambda t, dxc=dxc, dyc=dyc: Tf(dx=dxc(t), dy=dyc(t)))

    # the hall over the outside
    sc.add("hall", hall_svg(), z=2, seed=17)
    sc.add("beam", beam_svg(), z=2.1, wc=0, blend="screen", motion=lambda t: Tf(
        alpha=0.9 * M.progress(t, t_god - 0.1, t_god + 1.2, "sine") * (1 - 0.6 * M.progress(t, t_rise, t_rise + 1.5, "sine"))
        * (1 - M.progress(t, t_turn, t_turn + 1.0, "sine")) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.5))))

    # ---- the hall people: fan-bearer and guard ----
    BS = 0.94
    fbx, fby = 230, G - 40
    sc.add("fanbearer", doc(C.ground_shadow(fbx, fby, BS, 110) + C.egyptian(fbx, fby, BS, 1, kind="servant", variant=3,
                                                                           pose="stand")),
           z=2.2, seed=40, motion=M.breathe(0.012, 2.7, pivot=(fbx, fby)))
    hands = C.hand_positions(C.egyptian, fbx, fby, BS, 1, kind="servant", variant=3, pose="stand")
    hx, hy = hands[1]
    sc.add("fan", doc(fan_markup(hx, hy)), z=2.25, seed=41,
           motion=lambda t: Tf(rot=7 * math.sin(2 * math.pi * t / 2.2), px=hx, py=hy))
    gx = 1040
    sc.add("guard", doc(C.ground_shadow(gx, G - 46, BS, 110) + C.egyptian(gx, G - 46, BS, -1, kind="guard", variant=1,
                                                                         pose="stand")),
           z=2.15, seed=42, motion=M.breathe(0.012, 3.1, pivot=(gx, G - 46), phase=0.4))

    # ---- Pharaoh ----
    sc.add("throne", doc(C.ground_shadow(PX + 30, G, s, 200) + PR.egypt_throne(PX, G, s, 1)), z=2.3, seed=43)

    def PH(pose, expr=None, x=PX):
        return doc((C.ground_shadow(x, G, s, 130) if pose != "sit_throne" else "") +
                   C.pharaoh(x, G, s, 1, pose=pose, expr=expr, throne=False))
    pfr = [PH("sit_throne", "kind"), PH("sit_throne", blink("kind")),           # 0, 1
           PH("talk", "kind", PX_STAND), PH("give_ring", "kind", PX_STAND),       # 2, 3
           PH("talk", "happy", PX_STAND), PH("talk", blink("happy"), PX_STAND),   # 4, 5
           PH("stand", "happy", PX_STAND), PH("stand", blink("happy"), PX_STAND)]  # 6, 7
    t_pgive_end = snap(t_fly0 + 0.05)
    p_entries = [(0, 0), (t_rise, 2), (t_ring, 3), (t_pgive_end, 4), (snap(t_chain + 1.0), 6)]
    pv_seat, pv_st = (PX, G), (PX_STAND, G)
    sc.add("pharaoh", pfr, z=2.4, seed=44,
           frame_at=cuts(with_blinks(p_entries, {0: 1, 4: 5, 6: 7}, [2.2, 3.7, 7.4, 9.6, 12.0, 14.5])),
           motion=M.combine(
               lambda t: Tf(rot=(1.2 * math.sin(2 * math.pi * t / 1.3) if L0.start < t < t_rise else 0.0),
                            px=PX, py=G),
               M.breathe(0.01, 3.0, pivot=pv_st),
               happy_hop(t_rise, s, pv_st, 10), dip(t_ring, s, pv_st, 6), dip(t_pgive_end, s, pv_st, 5),
               dip(snap(t_chain + 1.0), s, pv_st, 4)))
    # speaking arcs at his mouth
    hp_seat = C.body_points(C.pharaoh, PX, G, s, 1, pose="sit_throne", throne=False)["head"]
    hp_st = C.body_points(C.pharaoh, PX_STAND, G, s, 1, pose="talk")["head"]
    arcs_seat = [doc(arcs_markup(hp_seat[0] + 62, hp_seat[1] + 14, 1, -0.15, k)) for k in (1, 2, 3)]
    arcs_st = [doc(arcs_markup(hp_st[0] + 62, hp_st[1] + 14, 1, -0.15, k)) for k in (1, 2, 3)]
    sc.add("arcs_seat", arcs_seat, z=2.45, wc=0, frame_at=speaking(None),
           motion=speaking_alpha([(L0.start, min(t_rise - 0.05, L0.at("我要让你") - 0.1))]))
    sc.add("arcs_st", arcs_st, z=2.45, wc=0, frame_at=speaking(None),
           motion=speaking_alpha([(t_rise + 0.2, L0.end)]))

    # ---- the chariot (waiting; then the drive) ----
    def wheel_idx(t):
        dist = cx_at(t) - CX0
        return int(dist / (2 * math.pi * 80) * 6 * 3) % 3

    def horse_idx(t):
        if t < t_go + 0.05 or t > t_stop - 0.1:
            return 0
        return int((t - t_go) / 0.13) % 2

    back_fr = [doc(C.ground_shadow(CX0 + 220, G, s, 560) + PR.chariot(CX0, G, s, 1, part="back", wheel=w / 3, phase=h * 0.5 + 0.1))
               for h in (0, 1) for w in (0, 1, 2)]
    front_fr = [doc(PR.chariot(CX0, G, s, 1, part="front", wheel=w / 3)) for w in (0, 1, 2)]

    def ch_motion(t):
        return Tf(dx=cx_at(t) - CX0)
    sc.add("chariot_back", back_fr, z=3.0, seed=50, frame_at=lambda t: float(horse_idx(t) * 3 + wheel_idx(t)),
           motion=M.combine(ch_motion, lambda t: Tf(dy=-2.5 * abs(math.sin(math.pi * (t - t_go) / 0.26))
                                                    * min(1.0, speed_at(t) / 300))))
    sc.add("chariot_front", front_fr, z=3.2, seed=51, frame_at=lambda t: float(wheel_idx(t)), motion=ch_motion)
    # dust puffs behind the wheel while driving
    puffs = [doc(puff_markup(CX0 - 70 - 60 * k, G - 16 - 6 * k, 46 + 14 * k, 30 + 8 * k, seed=k)) for k in range(3)]
    sc.add("dust", puffs, z=3.25, wc=0.6, seed=52, frame_at=lambda t: float(int(t * 9) % 3),
           motion=lambda t: Tf(dx=cx_at(t) - CX0, alpha=0.8 * min(1.0, speed_at(t) / 350)))

    # ---- Joseph in the hall: slave tunic -> ruler; then walks to the chariot ----
    def J(pose, expr=None, attire="slave", chain=False, ring=False, f=-1, x=JX):
        sh = C.ground_shadow(x, G, s, 120)
        if attire == "slave":
            return doc(sh + C.joseph(x, G, s, f, pose=pose, expr=expr, attire="slave"))
        return doc(sh + C.joseph(x, G, s, f, pose=pose, expr=expr, attire="ruler", chain=chain, ring=ring))
    jfr = [J("stand", "kind"), J("stand", blink("kind")),                          # 0, 1
           J("bow", "kind"),                                                       # 2
           J("give", "amazed"), J("give", "happy"),                                # 3, 4
           J("stand", "proud", "ruler", ring=True), J("stand", blink("happy"), "ruler", ring=True),   # 5, 6
           J("bow", "proud", "ruler", chain=True, ring=True),                     # 7
           J("stand", "happy", "ruler", True, True), J("stand", blink("happy"), "ruler", True, True),  # 8, 9
           J("walk_a", "happy", "ruler", True, True, 1), J("walk_b", "happy", "ruler", True, True, 1)]  # 10, 11
    j_entries = [(0, 0), (t_bow, 2), (snap(t_bow + 1.3), 0), (t_hands, 3), (snap(t_fly1 + 0.1), 4),
                 (t_clothes, 5), (t_chain, 7), (snap(t_chain + 0.55), 8)]
    jbase = cuts(with_blinks(j_entries, {0: 1, 5: 6, 8: 9}, [0.6, 3.9, 9.6]))

    def j_fa(t):
        if t >= t_turn:
            w = fa_w(t)
            if w is not None:
                return 10.0 + w
            return 11.0 if t >= t_walk1 else 10.0
        return jbase(t)
    pvj = (JX, G)

    def j_motion(t):
        if t >= t_land:
            return Tf(alpha=0.0)
        tf = Tf(dx=dxw(t), dy=dyw(t))
        if t >= t_jump:
            u = (t - t_jump) / (t_land - t_jump)
            ex, ey = CX0 + PR.CHARIOT_STAND[0] * s - J_STOP, PR.CHARIOT_STAND[1] * s
            tf = Tf(dx=dxw(t) + ex * M.ease("inout")(u), dy=ey * u - 70 * math.sin(math.pi * u),
                    rot=4 * math.sin(math.pi * u), px=JX, py=G)
        return tf
    sc.add("joseph", jfr, z=3.1, seed=53, frame_at=j_fa,
           motion=M.combine(j_motion, M.breathe(0.01, 3.0, pivot=pvj),
                            dip(t_bow, s, pvj, 6), dip(snap(t_bow + 1.3), s, pvj, 4), dip(t_hands, s, pvj, 5),
                            happy_hop(t_clothes, s, pvj, 26), happy_hop(t_chain, s, pvj, 14), dip(t_turn, s, pvj, 6),
                            hop(t_jump - 0.1, [(0, {"sy": 1}), (0.1, {"sy": 0.92}), (0.2, {"sy": 1.04}), (0.4, {"sy": 1})],
                                (J_STOP, G))))
    # Joseph riding: waves from the chariot
    rx, ry = PR.local_to_stage(CX0, G, s, 1, *PR.CHARIOT_STAND)
    rfr = [doc(C.joseph(rx, ry, s, 1, pose="ride_wave", expr="proud", attire="ruler")),
           doc(C.joseph(rx, ry, s, 1, pose="ride_wave", expr="happy", attire="ruler")),
           doc(C.joseph(rx, ry, s, 1, pose="ride_wave", expr=blink("happy"), attire="ruler"))]
    sc.add("rider", rfr, z=3.15, seed=54,
           frame_at=cuts(with_blinks([(0, 0), (snap(t_stop + 0.6), 1)], {1: 2}, [17.0, 19.4])),
           motion=M.combine(lambda t: Tf(dx=cx_at(t) - CX0, alpha=1.0 if t >= t_land else 0.0),
                            hop(t_land, [(0, {"sy": 0.9, "dy": 4}), (0.16, {"sy": 1.03, "dy": -3}), (0.3, {"sy": 1, "dy": 0})],
                                (rx, ry)),
                            lambda t: Tf(dy=-2.5 * abs(math.sin(math.pi * (t - t_go) / 0.26)) * min(1.0, speed_at(t) / 300)),
                            # his waving arm side sways a little
                            lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * t / 0.9), px=rx, py=ry)))

    # the ring: glints in Pharaoh's fingers, flies into Joseph's hands, rests there until the robes come
    rp = C.body_points(C.pharaoh, PX_STAND, G, s, 1, pose="give_ring")["hands"][1]
    rs_ = (rp[0] + 6 * s, rp[1] - 10 * s)
    jh = C.body_points(C.joseph, JX, G, s, -1, pose="give", attire="slave")["hands"]
    rd = ((jh[0][0] + jh[1][0]) / 2, (jh[0][1] + jh[1][1]) / 2 - 22)
    sc.add("ring", doc(PR.signet_ring(rs_[0], rs_[1] - 18 * 0.32, 0.32)), z=3.12, seed=55, motion=lambda t: Tf(
        dx=(rd[0] - rs_[0]) * M.progress(t, t_fly0, t_fly1, "inout"),
        dy=(rd[1] - rs_[1]) * M.progress(t, t_fly0, t_fly1, "inout") - 90 * math.sin(math.pi * M.progress(t, t_fly0, t_fly1, "linear"))
        + (2 * math.sin(2 * math.pi * t / 1.4) if t > t_fly1 else 0.0),
        rot=360 * M.progress(t, t_fly0, t_fly1, "inout"), px=rs_[0], py=rs_[1],
        sx=1 + 0.6 * math.sin(math.pi * M.progress(t, t_fly0, t_fly1, "linear")),
        sy=1 + 0.6 * math.sin(math.pi * M.progress(t, t_fly0, t_fly1, "linear")),
        alpha=1.0 if t_fly0 <= t < t_clothes else 0.0))
    glint = [doc(twinkles_markup([(rs_[0] + 22, rs_[1] - 30, 16)], k)) for k in range(3)]
    sc.add("ring_glint", glint, z=3.13, wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_ring, t_ring + 0.15) * (1 - M.progress(t, t_fly0 - 0.1, t_fly0))))
    glint2 = [doc(twinkles_markup([(rd[0] + 26, rd[1] - 26, 15), (rd[0] - 30, rd[1] - 8, 10)], k)) for k in range(3)]
    sc.add("ring_glint2", glint2, z=3.13, wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_fly1, t_fly1 + 0.2) * (1 - M.progress(t, t_clothes - 0.15, t_clothes))))

    # sparkle bursts: the robes, then the chain
    jc = (JX, G - 175)
    bfr = [doc(burst_markup(jc[0], jc[1], k, r0=70, r1=250, n=14, seed=3)) for k in range(6)]

    def burst_fa(t0, n=6, dur=0.5):
        return lambda t: float(min(n - 1, max(0, int((t - t0 + 0.12) / dur * n))))
    sc.add("burst", bfr, z=3.3, wc=0, frame_at=burst_fa(t_clothes),
           motion=lambda t: Tf(alpha=1.0 if t_clothes - 0.12 <= t < t_clothes + 0.42 else 0.0))
    defs_f = S.rad_grad("fl11", [(0, "#fffbe8", 1), (0.5, "#fff1c0", 0.6), (1, "#fff1c0", 0)])
    sc.add("flash", doc(f'<ellipse cx="{jc[0]}" cy="{jc[1]}" rx="190" ry="260" fill="url(#fl11)"/>', defs_f), z=3.29,
           wc=0, blend="screen", motion=lambda t: Tf(
               alpha=math.exp(-((t - t_clothes) / 0.16) ** 2) * 0.95 + 0.5 * math.exp(-((t - t_chain) / 0.12) ** 2)))
    nk = (JX - 14 * -1, G - 236)
    cfr = [doc(burst_markup(nk[0], nk[1], k, r0=20, r1=110, n=8, seed=7, size=16)) for k in range(6)]
    sc.add("chain_burst", cfr, z=3.3, wc=0, frame_at=burst_fa(t_chain, dur=0.45),
           motion=lambda t: Tf(alpha=1.0 if t_chain - 0.12 <= t < t_chain + 0.36 else 0.0))

    # ---- people along the street: they bow as the chariot passes ----
    PS = 0.86
    folk = [("woman", 0, 1400), ("servant", 2, 1535), ("wise", 1, 1680), ("woman", 3, 1815), ("servant", 1, 1945),
            ("guard", 2, 2060)]
    yy = 868
    ts = [t_go + 0.02 * k for k in range(300)]
    for i, (kind, v, x) in enumerate(folk):
        # bow when the horse's head is ~120 px short of them
        t_b = next((tt for tt in ts if cx_at(tt) + 560 * s >= x - 120), t_stop)
        t_b = snap(t_b)
        t_up = snap(t_b + 2.6 + 0.1 * i)

        def F(pose, expr=None, kind=kind, v=v, x=x):
            kw = dict(spear=False) if kind == "guard" else {}
            return doc(C.ground_shadow(x, yy, PS, 110) + C.egyptian(x, yy, PS, -1, kind=kind, variant=v, pose=pose,
                                                                     expr=expr, **kw))
        fr = [F("stand", "amazed"), F("stand", blink("happy")), F("bow"), F("cheer", "happy"), F("stand", "happy")]
        pv = (x, yy)
        sc.add(f"folk{i}", fr, z=2.6 + 0.01 * i, seed=70 + i,
               frame_at=cuts(with_blinks([(0, 0), (t_b, 2), (t_up, 3), (snap(t_up + 1.2), 4)], {4: 1}, [6.0 + i, 19.0])),
               motion=M.combine(M.breathe(0.012, 2.6 + 0.15 * i, pivot=pv, phase=0.2 * i), dip(t_b, PS, pv, 7),
                                happy_hop(t_up, PS, pv, 14), dip(snap(t_up + 1.2), PS, pv, 4)))

    # ---- foreground frame ----
    sc.add("front", front_svg(), z=5, seed=18)
    # warm motes in the hall light and the fields
    sc.fx.append(FX.sparkles((JX - 180, G - 420, JX + 180, G - 40), count=14, t0=t_god, t1=t_rise + 1.2, seed=21,
                             size=(6, 13)))
    sc.fx.append(FX.sparkles((3000, 380, 4300, 760), count=14, t0=t_heap + 0.6, t1=T + 1, seed=22, size=(7, 15)))

    # ---- sound ----
    sc.sfx("crowd", 0.0, dur=T, gain_db=-24, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_god, gain_db=-14)
    sc.sfx("sparkle", t_ring, gain_db=-14)
    sc.sfx("whoosh", t_fly0, gain_db=-16)
    sc.sfx("pop", t_fly1, gain_db=-12)
    sc.sfx("sparkle", t_clothes - 0.05, gain_db=-9)
    sc.sfx("cloth", t_clothes, gain_db=-12)
    sc.sfx("sparkle", t_chain - 0.05, gain_db=-13)
    sc.sfx("coins", t_chain + 0.05, gain_db=-16)
    sc.sfx("footsteps", t_walk0, dur=t_walk1 - t_walk0 + 0.1, gain_db=-16)
    sc.sfx("whoosh", t_jump, gain_db=-13)
    sc.sfx("thud", t_land, gain_db=-12)
    sc.sfx("horn", t_go - 0.1, gain_db=-11)
    sc.sfx("footsteps_run", t_go, dur=t_stop - t_go, gain_db=-14, fade_out=0.6)
    sc.sfx("cheer", t_go + 0.8, dur=3.2, gain_db=-17, fade_in=0.5, fade_out=1.0)
    sc.sfx("birds", t_go + 1.5, dur=T - t_go - 1.5, gain_db=-17, fade_in=1.0, fade_out=0.8)
    sc.sfx("pop", t_sheaf, gain_db=-17)
    sc.sfx("grow", t_store, gain_db=-13)
    sc.sfx("grow", t_heap, gain_db=-10)
    sc.sfx("sparkle", t_high + 0.6, gain_db=-14)
    return sc
