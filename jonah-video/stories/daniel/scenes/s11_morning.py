"""Scene 11 — first light: the king hurries to the den and Daniel answers from below (Daniel 6:19-22).

One tall 2800 x 2000 stage, the lions' den in dollhouse cross-section (props.lion_den view='cutaway'): above the
ground line a dawn meadow with Babylon far away on the left and the sun coming up on the right; below it the cut
earth and the den chamber, where Daniel spent the night among the lions. No cuts.

  opening        a clear new view after s10's dark den: the sealed stone on the den's mouth at dawn, two palace
                 guards dozing beside it (eyes closed), the sky warming from lilac to gold, the sun rising, doves.
  '第二天天刚亮'  a rooster crows (off screen); the guards wake with a start (hop).
  '国王就急忙跑到' the king hurries in from the left (planted-foot strides on a quick cadence, leaning forward,
                 worried) and stops at the left rim. The guards see him, snap the king's seal off the stone (puff,
                 pop) and haul on a rope over the top of the stone: it rolls aside to the right in four heave-ho
                 tugs (each tug moves stone, rope and guards together; the stone's cracks turn with it).
  '大声喊'        morning light pours down the shaft into the den (the chamber's darkness lifts).
  K line         the king leans over the hole and calls down (call_out, sound arcs going down); the camera tilts
                 down through the earth so the page shows both levels: the king above, the den below.
                 '你的上帝救了你吗？' — his face turns anxious.
  '坑里传来…'     Daniel, sitting peacefully among the lying lions in the shaft of light, gets up (hop) and looks up
                 happily; the king's face changes to surprise.
  D line 1       '王啊，愿你万岁！' Daniel answers, one hand raised (sound arcs rising); '我的上帝派天使…' the
                 camera eases in on the den, a warm golden glow blooms in the beam (chime: the angel's light, never a
                 figure) and Daniel turns his open hand toward the big lion beside him, which sits up with a happy,
                 closed-mouth smile; '狮子没有伤害我' Daniel throws his arms up (hop), the lioness opens a sleepy
                 eye and swishes her tail; the king beams.
  D line 2       '因为在上帝面前，我是无罪的' Daniel looks up into the light; the camera eases back out to both
                 levels; '在王面前' he bows to the king; '我也没有做错事' he raises his open hand to the king again,
                 the king reaches down with both hands, happy. Calm hold for the dissolve.

Pose and face changes are hard cuts sold by a small squash / hop (never two drawings crossfaded); the den light,
the sky and the chamber's darkness are lighting changes (crossfades). Every beat is keyed to the subtitle chunks.
Lions stay friendly (closed mouths, smiles). God / the angel is light only.
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

SW, SH = 2800, 2000
INK = P["ink"]
G = 1020                     # ground surface (the den's anchor y)
DX = 1400                    # centre of the den opening
DS = 1.0                     # den scale
FL = G + PR.DEN_FLOOR_Y      # 1620: floor inside the den
HORIZON = 930
KS = 1.0                     # king scale
KX = 1110                    # the king's spot at the left rim
DNX = 1430                   # Daniel inside, in the beam
GS = 0.95                    # guard scale
SX0, TUG = 1400, 92          # stone start x and the distance of one heave-ho tug
N_TUGS = 4
G1_OFF, G2_OFF = 335, 525    # guard anchors relative to the stone

PUNCT = "，。；：？！、,.;:?!"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ timing helpers


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


def when(ctx, phrase):
    """Start time of ``phrase``: its chunk start, or its character position inside the chunk."""
    for ln in ctx.lines:
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


def clamp_cam(c, margin=4):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), SH - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys):
    """[(t, Cam)] eased moves; the viewport's bottom edge is interpolated so the clamp never kinks a move."""
    keys = [(t, clamp_cam(c)) for t, c in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a), (t1, b) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
        return keys[-1][1]
    return cam


# blink drawings (eyes-closed copies of the expressions that blink); setdefault keeps the shared table intact
for _e in ("happy", "neutral", "worried", "surprised", "call"):
    C.EXPRS.setdefault(f"d11_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


# ============================================================================ backdrops


SKY_PRE = [(0, "#a796bf"), (0.4, "#c8a9c4"), (0.75, "#eab6a6"), (1, "#f4cba0")]
SKY_DAWN = [(0, "#9fbfdc"), (0.38, "#d4c9d8"), (0.72, "#f6d2a8"), (1, "#fbe1a8")]


def sky_svg(stops, key):
    defs = S.lin_grad(f"sky{key}", stops, 0, 0, 0, 1)
    body = f'<rect x="-20" y="-20" width="{SW + 40}" height="{HORIZON + 80}" fill="url(#sky{key})"/>'
    return doc(body, defs)


def sun_svg():
    cx, cy = 2180, HORIZON - 10
    defs = S.rad_grad("sunglow", [(0, "#fff4cf", 0.95), (0.35, "#fde3a0", 0.55), (1, "#fbd99a", 0.0)])
    body = (f'<circle cx="{cx}" cy="{cy}" r="420" fill="url(#sunglow)"/>'
            f'<path d="{S.rays(cx, cy, 120, 520, 14, 6, rot=-8)}" fill="#fff1c8" opacity="0.32"/>'
            f'<circle cx="{cx}" cy="{cy}" r="88" fill="{P["sun"]}" stroke="#f0a95a" stroke-width="5"/>'
            f'<circle cx="{cx - 22}" cy="{cy - 24}" r="40" fill="#fde69a" opacity="0.7"/>')
    return doc(S.g(body, filter="wobble"), defs)


CLOUDS = [(380, 260, 380, 110, 1), (1150, 170, 300, 90, 2), (1750, 330, 420, 120, 3), (2550, 210, 330, 96, 4),
          (2950, 420, 260, 80, 5), (-200, 470, 300, 84, 6), (800, 480, 240, 70, 7)]


def clouds_svg():
    out = ""
    for cx, cy, w, h, sd in CLOUDS:
        out += S.cloud(cx, cy, w, h, fill="#fbe6d6", seed=sd, sw=3, shade_fill="#efc0b4")
    return doc(S.g(out, filter="wobble"))


def far_svg():
    """Far hills, Babylon on the left (hazy), palms and bushes on the meadow, the ground strip."""
    out = ""
    # far lavender hills
    out += S.path(S.hill(-100, 1200, HORIZON + 10, 70, seed=3, bottom=G + 10, bumps=3), "#c9b4c6", sw=3)
    out += S.path(S.hill(1300, 2950, HORIZON + 10, 90, seed=5, bottom=G + 10, bumps=4), "#cdb7c2", sw=3)
    # Babylon: walls, towers and a ziggurat, hazed toward the dawn
    out += PR.nineveh_skyline(-60, 1160, HORIZON + 22, 0.55, seed=4, haze=0.55, tint="#efc9b8")
    # near meadow (seen a little from above) down to the cut ground line
    defs = S.lin_grad("meadow", [(0, "#b9b97a"), (1, "#9aab5e")])
    out += S.path(S.wave_line(HORIZON + 30, 6, 700, 0, -40, SW + 40) +
                  f" L{SW + 40},{G + 4} L-40,{G + 4} Z", "url(#meadow)", sw=3.5)
    rng = random.Random(11)
    for _ in range(70):           # little meadow strokes
        x = rng.uniform(0, SW)
        y = rng.uniform(HORIZON + 45, G - 12)
        out += (f'<path d="M{f1(x)},{f1(y)} q4,-12 8,0" fill="none" stroke="{S.shade(P["grass_dark"], -0.1)}" '
                f'stroke-width="2.5" opacity="0.6"/>')
    out += PR.palm_tree(330, G - 30, 0.62, lean=0.15)
    out += PR.palm_tree(560, G - 55, 0.42, lean=-0.25)
    out += PR.palm_tree(2520, G - 40, 0.58, lean=-0.2)
    # two spears leaning against the right palm (the guards' spears while they work)
    for k, (bx, tx) in enumerate(((2440, 2500), (2470, 2515))):
        out += (f'<path d="M{bx},{G - 6} L{tx},{G - 330}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
                f'<path d="M{bx},{G - 6} L{tx},{G - 330}" stroke="#9a6a40" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M{tx},{G - 372} q12,22 3,42 l-10,0 q-9,-20 7,-42 z" fill="#c9c2b4" stroke="{INK}" '
                f'stroke-width="3"/>')
    out += PR.bush(760, G - 6, 0.5, variant=1)
    out += PR.bush(2140, G - 4, 0.45, variant=0)
    for x, v in ((640, 2), (980, 0), (1880, 2), (2280, 1), (2700, 0), (140, 0)):
        out += PR.grass_tuft(x, G + 2, 0.75, variant=v)
    return doc(out, defs)


def earth_svg():
    """Cut earth under the whole stage (the den's own section sits on top of it in the middle)."""
    defs = S.lin_grad("earthbg", [(0, "#c49a6c"), (1, "#8f6646")])
    out = f'<rect x="-20" y="{G}" width="{SW + 40}" height="{SH - G + 20}" fill="url(#earthbg)"/>'
    rng = random.Random(5)
    for k, yy in enumerate(range(G + 60, SH, 75)):
        pts = [(-60 + 300 * i, yy + rng.uniform(-14, 14)) for i in range(11)]
        out += S.path(S.smooth_path(pts, closed=False), sw=3,
                      extra=f'stroke="{S.shade("#b88e62", -0.14 if k % 2 else 0.12)}" opacity="0.8"')
    for _ in range(140):
        x, y = rng.uniform(0, SW), rng.uniform(G + 30, SH)
        r = rng.uniform(6, 16)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.4)}" ry="{f1(r)}" '
                f'fill="{S.shade("#b88e62", rng.choice((-0.22, 0.16)))}" stroke="{INK}" stroke-width="2.4" '
                f'opacity="0.85"/>')
    # roots hanging from the meadow
    for x in (250, 420, 2380, 2560, 900, 2050):
        out += (f'<path d="M{x},{G + 4} q-10,40 6,80 q14,30 -4,70" fill="none" stroke="#7a5a3c" stroke-width="4" '
                f'stroke-linecap="round" opacity="0.8"/>')
    out += f'<path d="M-20,{G} L{SW + 20},{G}" stroke="{INK}" stroke-width="5"/>'
    return doc(S.g(out, filter="wobble"), defs)


def dim_svg():
    """The chamber's night darkness (fades as the light comes in)."""
    return doc(f'<g transform="translate({DX},{G}) scale({DS})"><path d="{PR._den_cave()}" fill="#20182a"/></g>')


def beam_glow_svg():
    """A warm golden bloom in the light beam (the angel's light, remembered)."""
    o0, o1 = PR.DEN_OPENING
    top = PR.DEN_INNER[1]
    defs = S.lin_grad("bg11", [(0, "#ffe9a8", 0.85), (1, "#ffd27a", 0.25)])
    defs += S.rad_grad("bf11", [(0, "#fff0bf", 0.8), (1, "#ffe0a0", 0)])
    body = (f'<path d="M{DX + o0 * DS},{G + top * DS} L{DX + o1 * DS},{G + top * DS} L{DX + (o1 + 150) * DS},{FL + 10} '
            f'L{DX + (o0 - 150) * DS},{FL + 10} Z" fill="url(#bg11)" filter="url(#soft)"/>'
            f'<ellipse cx="{DX}" cy="{FL - 120}" rx="420" ry="300" fill="url(#bf11)"/>')
    return doc(body, defs)


def rope_markup(sx, guard_xs, variants, slack=False, dropped=False):
    """The haul rope: over the top of the stone (centre sx) and through the guards' fists; or lying slack."""
    st0 = (sx - 60, G - 256)
    st1 = (sx + 110, G - 228)
    if dropped:          # let go: it hangs down the stone's side and lies along the ground past their feet
        pts = [st0, (sx + 40, G - 268), st1, (sx + 168, G - 120), (sx + 200, G - 8), (guard_xs[0] - 60, G - 3),
               (guard_xs[0] + 20, G - 10), (guard_xs[1] - 40, G - 3), (guard_xs[1] + 80, G - 6)]
        d = S.smooth_path(pts, closed=False)
    elif slack:
        pts = [st0, (sx + 40, G - 268), st1, (sx + 175, G - 100), (sx + 230, G - 6), (guard_xs[0] - 30, G - 4),
               (guard_xs[0] + 60, G - 12), (guard_xs[1] - 10, G - 4), (guard_xs[1] + 90, G - 8)]
        d = S.smooth_path(pts, closed=False)
    else:
        pts = [st0, (sx + 40, G - 268), st1]
        for gx, v in zip(guard_xs, variants):
            far, near = C.hand_positions(C.guard, gx, G, GS, -1, variant=v, pose="pull_rope")
            pts += [far, near]
        d = S.smooth_path(pts[:3], closed=False) + "".join(f" L{f1(x)},{f1(y)}" for x, y in pts[3:])
        lx, ly = pts[-1]
        d += f" Q{f1(lx + 60)},{f1(ly + 40)} {f1(lx + 70)},{f1(G - 4)} L{f1(lx + 150)},{f1(G - 2)}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#c8a46a" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#a9834e" stroke-width="2" stroke-dasharray="6 9"/>')


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


def puff_markup(cx, cy, rx, ry, seed=0):
    rng = random.Random(seed)
    out = ""
    for i in range(7):
        a = 2 * math.pi * i / 7
        out += (f'<circle cx="{f1(cx + rx * 0.7 * math.cos(a))}" cy="{f1(cy + ry * 0.6 * math.sin(a))}" '
                f'r="{f1(ry * rng.uniform(0.4, 0.6))}" fill="#efe0c6" stroke="{INK}" stroke-width="3" opacity="0.9"/>')
    return S.g(out, filter="wobble-fine")


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]

    # ---- key times (from the narration) ----
    t_dawn = L0.start                                   # "第二天天刚亮"
    t_rooster = L0.start + 0.25
    t_wake = snap(L0.start + 1.05)                      # guards wake with a start
    t_run = when(ctx, "国王就急忙") + 0.05               # the king hurries in
    RUN_P, RUN_N = 0.165, 10
    t_notice = snap(t_run + 0.5)                        # guards see him coming
    t_seal = snap(t_run + RUN_N * RUN_P - 0.05)         # as the king arrives the seal snaps off (puff)
    t_pull = snap(t_seal + 0.3)                         # they haul on the rope
    TUG_P = 0.44
    tug_t = [t_pull + 0.2 + k * TUG_P for k in range(N_TUGS)]
    t_open = tug_t[-1] + 0.3                            # stone off the hole
    t_light0, t_light1 = tug_t[1], t_open + 1.2         # light pours in
    t_call = snap(max(L1.start - 0.3, t_open + 0.05))    # the king leans over the hole and calls
    t_worry = snap(L1.at("你的上帝") + 0.1)              # "你的上帝救了你吗？" anxious
    t_down0, t_down1 = L1.start + 3.3, L2.start + 0.4   # camera tilts down to both levels
    t_voice = L2.start                                  # "坑里传来但以理的声音"
    t_kneel = snap(L2.start + 0.15)                     # Daniel gets up on his knees, arms lifted...
    t_dan_up = snap(L2.start + 0.85)                    # ...stands and looks up
    t_king_wow = snap(L2.start + 0.9)                   # the king hears him (surprised)
    t_answer = snap(L3.start - 0.15)                    # "王啊，愿你万岁！"
    t_angel = when(ctx, "天使")                          # "我的上帝派天使"
    t_explain = snap(L3.at("我的上帝") + 0.05)
    t_lion_up = snap(when(ctx, "封住") + 0.1)            # the lion sits up, mouth closed, smiling
    t_king_joy = snap(t_explain + 0.5)
    t_nohurt = snap(L3.at("狮子没有") + 0.05)            # "狮子没有伤害我": arms up
    t_god = snap(L4.start + 0.05)                       # "因为在上帝面前": looks up into the light
    t_bow = snap(when(ctx, "在王面前") + 0.05)           # bows to the king
    t_done = snap(L4.at("我也没有") + 0.05)              # "我也没有做错事": hand raised to the king
    t_reach = snap(t_done + 0.6)                        # the king reaches down with both hands
    t_rest = snap(min(L4.end + 0.3, T - 1.3))

    # ---- camera ----
    C0 = Cam(1470, 765, 1720)                 # dawn on the surface
    C1 = Cam(1400, 1250, 2400)                # both levels: the king above, the den below
    C2 = Cam(1405, 1446, 1400)                # close-up inside the den (Daniel and the lions)
    sc.camera = cam_path([(0, C0), (t_down0, C0), (t_down1, C1), (t_explain - 0.4, C1), (t_explain + 2.4, C2),
                          (t_god + 0.2, C2), (t_bow - 0.1, C1), (T, C1)])

    # ---- sky ----
    sc.add("sky", [sky_svg(SKY_PRE, 0), sky_svg(SKY_DAWN, 1)], z=0, wc=0.5,
           frame_at=lambda t: M.progress(t, 0.2, 5.0, "sine"))
    sc.add("sun", sun_svg(), z=0.5, wc=0.4, motion=M.combine(
        M.keys([(0, {"dy": 95}), (7.0, {"dy": 0})], "out"),
        M.breathe(0.015, 4.0, pivot=(2180, HORIZON - 10))))
    sc.add("clouds", clouds_svg(), z=1, wc=0.6, motion=M.drift(vx=-6))
    # doves crossing the dawn sky
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = (0, 1, 2, 3, 4, 3, 2, 1)
    for i, (x0, y0, x1, y1, ta, tb, s) in enumerate(((2500, 420, 900, 300, 0.0, 9.0, 0.42),
                                                     (2650, 520, 1150, 390, 1.0, 10.5, 0.36))):
        fr = [doc(PR.dove(x0, y0, s, -1, wing=w)) for w in wings]

        def mv(t, x0=x0, y0=y0, x1=x1, y1=y1, ta=ta, tb=tb, i=i):
            u = (t - ta) / (tb - ta)
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            a = min(1.0, u / 0.08, (1 - u) / 0.08)
            return Tf(dx=(x1 - x0) * u, dy=(y1 - y0) * u + 12 * math.sin(2 * math.pi * t / 1.6 + i), alpha=a)
        sc.add(f"dove{i}", fr, z=1.2, frame_at=lambda t, i=i: float(cyc[int(t * 10 + i * 3) % 8]), motion=mv,
               seed=700 + i)

    sc.add("far", far_svg(), z=2)
    sc.add("earth", earth_svg(), z=2.5)

    # ---- the den (back), light coming in as the stone rolls away ----
    lights = (0.0, 0.35, 0.7, 1.0)
    sc.add("den_back", [doc(PR.lion_den(DX, G, DS, part="back", light=v)) for v in lights], z=3,
           frame_at=lambda t: 3 * M.progress(t, t_light0, t_light1, "sine"))

    # ---- lions ----
    LA = dict(x=1105, s=0.8, f=1)              # big lion lying beside Daniel (sits up on "封住")
    LB = dict(x=1800, s=0.78, f=-1)            # lioness asleep on the right
    LC = dict(x=905, s=0.66, f=1)              # a third lion asleep at the back left (shows when A sits up)
    lc_tail = (-0.5, 0.2, 0.8)
    lc = [doc(PR.lion(LC["x"], FL - 14, LC["s"], LC["f"], pose="sleep", tail=tl)) for tl in lc_tail]
    sc.add("lionC", lc, z=3.4, frame_at=lambda t: float(1 + round(math.sin(2 * math.pi * t / 3.4 + 1.0))),
           motion=M.breathe(0.016, 3.6, pivot=(LC["x"], FL - 14)))
    # lioness B: asleep, opens a sleepy eye and swishes her tail at "狮子没有伤害我"
    lb_tail = (-0.6, 0.0, 0.6)
    lb = [doc(PR.lion(LB["x"], FL, LB["s"], LB["f"], pose="sleep", variant=1, tail=tl, eyes=e))
          for e in ("closed", "half") for tl in lb_tail]
    t_peek = snap(t_nohurt + 0.5)

    def lb_fa(t):
        eye = 1 if t_peek <= t < snap(t_peek + 3.2) else 0
        swish = 1 + round(math.sin(2 * math.pi * t / 2.6))
        return float(eye * 3 + swish)
    sc.add("lionB", lb, z=3.5, frame_at=lb_fa, motion=M.breathe(0.014, 3.2, pivot=(LB["x"], FL), phase=0.4))
    # lion A: lying, chin on paws, eyes half; on "封住" it sits up (hop) with a happy closed-mouth smile
    la = [doc(PR.lion(LA["x"], FL, LA["s"], LA["f"], pose="lie", eyes="half", tail=0.3)),     # 0
          doc(PR.lion(LA["x"], FL, LA["s"], LA["f"], pose="lie", eyes="closed", tail=0.3)),   # 1
          doc(PR.lion(LA["x"] - 40, FL, LA["s"], LA["f"], pose="sit", eyes="happy")),         # 2
          doc(PR.lion(LA["x"] - 40, FL, LA["s"], LA["f"], pose="sit", eyes="open")),          # 3
          doc(PR.lion(LA["x"] - 40, FL, LA["s"], LA["f"], pose="sit", eyes="closed"))]        # 4
    la_cuts = with_blinks([(0, 0), (t_lion_up, 2), (snap(t_lion_up + 1.6), 3), (snap(t_nohurt + 0.15), 2),
                           (snap(t_god + 1.0), 3)], {0: 1, 3: 4}, [4.0, 12.6, 17.8, 26.0, 29.6, 32.2])
    pva = (LA["x"], FL)
    sc.add("lionA", la, z=3.6, frame_at=cuts(la_cuts),
           motion=M.combine(M.breathe(0.012, 3.0, pivot=pva), happy_hop(t_lion_up, LA["s"], pva, 14),
                            happy_hop(snap(t_nohurt + 0.15), LA["s"], pva, 8)))

    # ---- Daniel ----
    dsh = C.ground_shadow(DNX, FL, 1.0, 150, opacity=0.25)
    D = lambda pose, expr=None: doc(dsh + C.daniel(DNX, FL, 1.0, -1, pose=pose, expr=expr))   # noqa: E731
    dfr = [D("sit", "peaceful"),          # 0 asleep sitting among the lions
           D("sit", "happy"),             # 1 awake (hears the king)
           D("sit", "d11_blink_happy"),   # 2
           D("look_up", "happy"),         # 3 standing, looking up
           D("look_up", "d11_blink_happy"),  # 4
           D("answer", "call"),           # 5 "王啊，愿你万岁！"
           D("explain", "happy"),         # 6 hand open toward the lion
           D("explain", "d11_blink_happy"),  # 7
           D("arms_up", "happy"),         # 8 "狮子没有伤害我"
           D("bow", "peaceful"),          # 9 "在王面前"
           D("answer", "happy"),          # 10 "我也没有做错事"
           D("answer", "d11_blink_happy"),   # 11
           D("kneel_up", "happy")]        # 12 getting up (in-between, held as its own beat)
    t_wake_d = snap(L1.start + 1.2)
    t_look2 = snap(t_god + 0.0)
    d_cuts = with_blinks([(0, 0), (t_wake_d, 1), (t_kneel, 12), (t_dan_up, 3), (t_answer, 5), (t_explain, 6), (t_nohurt, 8),
                          (t_look2, 3), (t_bow, 9), (t_done, 10), (t_rest, 3)],
                         {1: 2, 3: 4, 6: 7, 10: 11}, [10.2, 12.4, 16.0, 21.4, 26.4, 31.2, 32.8])
    pvd = (DNX, FL)
    sc.add("daniel", dfr, z=3.7, frame_at=cuts(d_cuts), motion=M.combine(
        M.breathe(0.01, 3.0, pivot=pvd),
        dip(t_wake_d, 1.0, pvd, 5), dip(t_kneel, 1.0, pvd, 7), happy_hop(t_dan_up, 1.0, pvd, 16), dip(t_answer, 1.0, pvd, 6),
        dip(t_explain, 1.0, pvd, 6), happy_hop(t_nohurt, 1.0, pvd, 22), dip(t_look2, 1.0, pvd, 6),
        dip(t_bow, 1.0, pvd, 7), dip(t_done, 1.0, pvd, 6), dip(t_rest, 1.0, pvd, 5)))

    # the warm golden bloom in the beam: the angel's light, remembered ("天使"), and again "在上帝面前"
    sc.add("beam_glow", beam_glow_svg(), z=3.05, wc=0, blend="screen", motion=lambda t: Tf(alpha=(
        0.75 * M.progress(t, t_angel - 0.2, t_angel + 0.6, "sine") * (1 - M.progress(t, t_nohurt + 0.6, t_nohurt + 1.8, "sine"))
        + 0.6 * M.progress(t, t_god, t_god + 0.8, "sine") * (1 - M.progress(t, t_bow + 0.2, t_bow + 1.4, "sine")))))

    # the chamber's night darkness lifts as the light pours in
    sc.add("dim", dim_svg(), z=3.9, wc=0,
           motion=lambda t: Tf(alpha=0.5 - 0.42 * M.progress(t, t_light0, t_light1, "sine")))
    sc.add("den_front", doc(PR.lion_den(DX, G, DS, part="front")), z=4)

    # ---- the stone and the guards ----
    def tug(t):
        return sum(TUG * M.progress(t, tk, tk + 0.3, "inout") for tk in tug_t)

    def tug_lift(t, s=GS):
        y = 0.0
        for tk in tug_t:
            if tk <= t <= tk + 0.3:
                y -= 6 * s * math.sin(math.pi * (t - tk) / 0.3)
        return y
    total = TUG * N_TUGS
    rolls = list(range(0, int(total / (128 * DS) * 180 / math.pi) + 11, 10))
    sfr = [doc(PR.den_stone(SX0, G + 8 * DS, DS, sealed=True))]
    sfr += [doc(PR.den_stone(SX0, G + 8 * DS, DS, sealed=False, roll=r)) for r in rolls]

    def stone_fa(t):
        if t < t_seal:
            return 0.0
        ang = tug(t) / (128 * DS) * 180 / math.pi
        return float(1 + min(len(rolls) - 1, int(round(ang / 10))))
    sc.add("stone", sfr, z=5, frame_at=stone_fa, motion=lambda t: Tf(dx=tug(t)))
    sc.add("seal_puff", doc(puff_markup(SX0, G - 250, 70, 46, 3)), z=5.1, wc=0.4,
           motion=hop(t_seal, [(-0.02, {"alpha": 0, "s": 0.6, "dy": 0}), (0.06, {"alpha": 1, "s": 1}),
                               (0.55, {"alpha": 0, "s": 1.35, "dy": -40})], (SX0, G - 250), ["out", "sine"]))
    sc.add("roll_dust", doc(puff_markup(SX0 + total + 120, G - 20, 110, 40, 8)), z=5.1, wc=0.4,
           motion=hop(t_open - 0.05, [(-0.02, {"alpha": 0, "s": 0.6}), (0.08, {"alpha": 0.9, "s": 1}),
                                      (0.7, {"alpha": 0, "s": 1.4, "dy": -30})], (SX0 + total + 120, G - 20),
                      ["out", "sine"]))

    gxs = (SX0 + G1_OFF, SX0 + G2_OFF)
    gvar = (0, 2)
    t_let = snap(t_open + 0.35)
    sc.add("rope", [doc(rope_markup(SX0, gxs, gvar, slack=True)), doc(rope_markup(SX0, gxs, gvar)),
                    doc(rope_markup(SX0, gxs, gvar, dropped=True))], z=5.2,
           frame_at=cuts([(0, 0), (t_pull, 1), (t_let, 2)]), motion=lambda t: Tf(dx=tug(t)))
    for i, (gx, v) in enumerate(zip(gxs, gvar)):
        def G_(pose, expr=None, gx=gx, v=v):
            return doc(C.ground_shadow(gx, G, GS, 130) + C.guard(gx, G, GS, -1, variant=v, pose=pose, expr=expr,
                                                                    spear=False))
        gfr = [G_("stand", "sleepy"), G_("stand", "surprised"), G_("stand", "neutral"), G_("pull_rope", "tired"),
               G_("stand", "worried"), G_("stand", "surprised"), G_("stand", "happy"),
               G_("stand", "d11_blink_neutral"), G_("stand", "d11_blink_worried"), G_("stand", "d11_blink_happy")]
        dt = 0.07 * i
        g_cuts = with_blinks([(0, 0), (snap(t_wake + dt), 1), (snap(t_wake + 0.9 + dt), 2), (snap(t_notice + dt), 1),
                              (t_pull, 3), (t_let, 4), (snap(t_king_wow + 0.2 + dt), 5),
                              (snap(t_king_joy + 0.3 + dt), 6)],
                             {2: 7, 4: 8, 6: 9}, [2.9 + i * 0.4, 8.5 + i * 0.6, 11.5 - i * 0.3, 20.5 + i, 26.0 + i,
                                                  30.5 - i * 0.5])
        pv = (gx, G)
        sc.add(f"guard{i}", gfr, z=5.3 + 0.01 * i, frame_at=cuts(g_cuts), motion=M.combine(
            lambda t: Tf(dx=tug(t), dy=tug_lift(t)),
            M.breathe(0.012, 2.8, pivot=pv, phase=0.3 * i),
            happy_hop(snap(t_wake + dt), GS, pv, 12), dip(t_pull, GS, pv, 8), dip(t_let, GS, pv, 6),
            dip(snap(t_king_wow + 0.2 + dt), GS, pv, 5), happy_hop(snap(t_king_joy + 0.3 + dt), GS, pv, 10),
            # lean back on each heave
            lambda t: Tf(rot=sum(4 * math.sin(math.pi * M.progress(t, tk - 0.05, tk + 0.35, "linear"))
                                 for tk in tug_t), px=gx, py=G)))
    sc.add("zz", [doc(f'<g opacity="0.8">' + "".join(
        f'<text x="{gx - 60 + k * 6}" y="{G - 380 - k * 8}" font-family="LXGW WenKai" font-size="{34 + 4 * k}" '
        f'fill="{P["ink_soft"]}">z</text>' for gx in gxs) + '</g>') for k in range(3)], z=5.4, wc=0,
           frame_at=lambda t: float(int(t * 2.5) % 3),
           motion=lambda t: Tf(alpha=1 - M.progress(t, t_wake - 0.25, t_wake, "sine")))

    # ---- the king ----
    run_fa, run_dx, run_dy, t_arrive = step_walk(t_run, RUN_N, 85 * KS, RUN_P, KS, move=0.1, lift=9)
    x_start = KX - RUN_N * 85 * KS
    ksh = C.ground_shadow(KX, G, KS, 130)
    K = lambda pose, expr=None, x=KX: doc(C.ground_shadow(x, G, KS, 130) + C.king(          # noqa: E731
        x, G, KS, 1, pose=pose, attire="darius", expr=expr))
    kfr = [K("walk_a", "worried", x_start), K("walk_b", "worried", x_start),              # 0, 1 (hurrying)
           K("stand", "worried"),                                                          # 2 arrives
           K("call_out", "call"),                                                          # 3 calls down
           K("call_out", "worried"),                                                       # 4 "你的上帝救了你吗？"
           K("call_out", "surprised"),                                                     # 5 hears Daniel
           K("call_out", "happy"),                                                         # 6 relief
           K("reach_out", "happy"),                                                        # 7 reaches down
           K("stand", "d11_blink_worried"), K("call_out", "d11_blink_worried"),            # 8, 9
           K("call_out", "d11_blink_happy"), K("reach_out", "d11_blink_happy")]            # 10, 11
    del ksh
    t_hold = t_arrive

    def king_fa(t):
        if t < t_hold:
            v = run_fa(t)
            return 0.0 if v is None else v
        return base_fa(t)
    base_fa = cuts(with_blinks([(0, 0), (t_hold, 2), (t_call, 3), (t_worry, 4), (t_king_wow, 5), (t_king_joy, 6),
                                (t_reach, 7)], {2: 8, 4: 9, 6: 10, 7: 11},
                               [5.6, 14.9, 21.0, 24.4, 27.1, 29.6, 32.6]))
    pvk = (KX, G)

    def king_move(t):
        if t < t_hold:
            # (the walk drawings sit at x_start; they move by the planted-foot stride offsets)
            lean = 3.0
            return Tf(dx=run_dx(t), dy=run_dy(t), rot=lean, px=x_start, py=G)
        return Tf()
    sc.add("king", kfr, z=6, frame_at=king_fa, motion=M.combine(
        king_move, dip(t_hold, KS, pvk, 9), dip(t_call, KS, pvk, 6), dip(t_worry, KS, pvk, 4),
        hop(t_king_wow, [(-0.08, {"dy": 0, "sy": 1}), (0, {"dy": 4, "sy": 0.96}), (0.15, {"dy": -12, "sy": 1.03}),
                         (0.32, {"dy": 0, "sy": 1})], pvk, ["in", "out", "sine"]),
        happy_hop(t_king_joy, KS, pvk, 10), dip(t_reach, KS, pvk, 6),
        lambda t: Tf(sx=1 + 0.01 * math.sin(2 * math.pi * t / 3.1), sy=1 + 0.01 * math.sin(2 * math.pi * t / 3.1),
                     px=KX, py=G) if t >= t_hold else Tf()))

    # ---- sound arcs: the king calling down, Daniel answering up ----
    kh = C.body_points(C.king, KX, G, KS, 1, pose="call_out", attire="darius")["head"]
    ka = (kh[0] + 70, kh[1] + 70)
    sc.add("king_arcs", [doc(arcs_markup(ka[0], ka[1], 0.55, 1.0, k, 1.1)) for k in (1, 2, 3)], z=6.5, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, L1.start, L1.start + 0.2) * (1 - M.progress(t, L1.end - 0.2, L1.end))))
    dh = C.body_points(C.daniel, DNX, FL, 1.0, -1, pose="explain")["head"]
    da = (dh[0] - 58, dh[1] - 6)

    def d_arcs_alpha(t):
        a = 0.0
        for ln in (L3, L4):
            a = max(a, M.progress(t, ln.start, ln.start + 0.2) * (1 - M.progress(t, ln.end - 0.2, ln.end)))
        # (not over his face while he bows / looks straight up)
        if t_bow - 0.1 <= t < t_done - 0.1:
            a = 0.0
        return Tf(alpha=a)
    sc.add("dan_arcs", [doc(arcs_markup(da[0], da[1], -0.75, -0.65, k, 0.95)) for k in (1, 2, 3)], z=6.5, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=d_arcs_alpha)

    # ---- fx: dust motes high in the beam (above every head), a few gold sparkles at the shaft for the angel ----
    sc.fx.append(FX.motes((DX - 120, G + 110, DX + 120, G + 290), count=14, t0=t_light0, color=(255, 240, 200),
                          alpha=120, seed=21))
    sc.fx.append(FX.sparkles((DX - 150, G + 100, DX + 150, G + 260), count=10, t0=t_angel - 0.1,
                             t1=t_nohurt + 1.2, color=(255, 230, 150), size=(9, 18), drift=10, seed=31))

    # ---- sound ----
    sc.sfx("birds", 0.0, dur=T, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-19, fade_in=0.8, fade_out=0.8)
    sc.sfx("rooster", t_rooster, gain_db=-7, pan=-0.4)
    sc.sfx("footsteps_run", t_run, dur=t_arrive - t_run + 0.1, gain_db=-9, pan=-0.3)
    sc.sfx("pop", t_seal, gain_db=-10)
    for k, tk in enumerate(tug_t):
        sc.sfx("thud", tk + 0.22, gain_db=-14, pan=0.2)
    sc.sfx("ship_creak", t_pull, dur=t_open - t_pull + 0.3, gain_db=-14, pan=0.25)
    sc.sfx("thud", t_open - 0.02, gain_db=-6, pan=0.25)
    sc.sfx("drip", t_down0, dur=T - t_down0, gain_db=-20, fade_in=1.5, fade_out=0.8)
    sc.sfx("chime", t_angel - 0.1, gain_db=-11)
    sc.sfx("sparkle", t_god + 0.1, gain_db=-15)
    return sc
