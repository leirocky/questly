"""Scene 23 — God's lesson (Jonah 4:10-11).

All four lines are God speaking, gently. Late afternoon, warm golden light. Adapted from the approved v1 lesson
scene (art/scenes_v1/s12_lesson.py: its 3800 x 1650 stage, land, city, people, animals, hearts, arc-length
camera glides and drawing helpers are reused), re-laid out on the right to continue the vine scenes s21/s22:

  * right: Jonah's dry knoll east of the city — a near, higher vantage point — with the withered castor plant on
    the LEFT and his little booth to its right, the dead canopy arching over the booth roof, and Jonah sitting
    UNDER the booth facing the city (same drawings, scale and arrangement as s21/s22; the knoll crest is lower
    than v1's so the opening camera can frame him exactly as s22 leaves him);
  * left / below: the green plain in front of Nineveh's hazy wall and open gate, full of life — families,
    many little children, elders, people walking in and out of the gate, a pasture with sheep, lambs, goats,
    cows and donkeys, and a goat and two sheep grazing on the lower slope of the knoll. Long soft shadows point
    east (the low sun is in the west, on the left).

Timing (every time comes from the narration: ctx chunk starts, or _at_in() for a phrase inside a chunk):
  opening  a match dissolve from s22: same framing relative to Jonah (s22's END_CAM), same pose (sit_sulk,
           angry), same booth, plant and veil cloud; the plant's sway is at rest through the dissolve.
  line 0   "约拿，" — he hears his name: a squash-and-hop cut to sitting up, looking up toward the light and the
           voice (up and to the right, under the veil cloud); the clouds part a little. "这棵蓖麻" — a pale, sun-
           bleached dry leaf wobbles on a broken leaf stub of the arching branch (the booth's pale back cloth behind
           it), swings out, sweeps left in front of his chest and drops into his open hand from above; his eyes
           follow it (blink cut), he bends his head over it and lifts it. "也不是你让它长大的" — he turns it.
  line 1   "它一夜长起来，" — a thought bubble scale-pops (opaque within 2 frames) out of a trail of puffs into the
           open sky up-left: a memory picture of the same spot at night (moon and stars) where the castor sprout
           springs up, step by step, into a tall green plant beside the booth; the moon sets at the upper left and
           the morning sun rises low on the right (east). "一夜又枯死了，" — night again, the plant droops and
           withers. "你都这么心疼它。" — the bubble shrinks back into the trail (3-frame alpha cut), the puffs pop out;
           Jonah turns tender and sorry (blink cut). The camera starts a slow pull-back.
  line 2   "尼尼微这座大城里，有十二万多人，" — a held wide view: the city, the plain, the pasture and Jonah under his
           booth (doves fly over). "就像分不清左右手的小孩子，" — a slow glide down to the children: two little ones
           point left and right with a '?' over each head and keep swapping sides (hops); two more play face to face
           behind them (clear of the ball game's arc). "不知道什么是对，什么是错。" — hearts rise over the people; the
           two children stop, hop, smile and get their hearts too.
  line 3   "还有许多牛羊。" — the camera glides over to the pasture and RESTS on it while the animals are named: a
           sheep bleats with a happy hop, hearts over the animals (all above the subtitle band).
           "我怎么能不心疼他们呢？" — the camera rises up the knoll and arrives on Jonah just before "心疼他们";
           his face softens through a blink into a thoughtful look down toward the city (raised brows, no smile,
           no blush — the Bible ends on God's question and s24 asks the child how Jonah answered); the warm light
           returns on him, a chime; slow push-in to a calm last frame.

Notes for maintainers
* Pose changes are hard cuts hidden by a squash-and-hop; every expression change goes through a closed-eye frame
  (blink -> new face, hard cuts), so two faces are never blended.
* The memory plant is one exact castor drawing per step (leaf spins pinned to the full-grown drawing, as in
  v1 s11), shown as a stepped time-lapse flipbook (whole indices only, never two plants blended).
* Camera: every move is re-parametrised by output-space arc length with soft ramps (v1 _cam_path / _glide);
  glide durations come from _cam_dur so the peak stays under ~19 output px / frame.
* The light on Jonah is clipped to his silhouette (two drawings: sulking / sitting); its rim is a thin, faint
  edge toward the light so his umber ink outline stays dark.
"""
import math
import random
from contextlib import contextmanager

import numpy as np

from art import characters as CH
from art import props as PR
from art import style as S
from art.scenes_v1 import s12_lesson as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = V.SW, V.SH
WALL_Y, GATE_X, SUN = V.WALL_Y, V.GATE_X, V.SUN
ABOX, HEAD_DX = V.ABOX, V.HEAD_DX
doc, f1, plain_scale = V.doc, V.f1, V.plain_scale
_clamp, _env = V._clamp, V._env
long_shadow, shdoc = V.long_shadow, V.shdoc
hop_sched, hop_h, hop_motion, hop_frame, shadow_motion = V.hop_sched, V.hop_h, V.hop_motion, V.hop_frame, V.shadow_motion
_cam_path, _glide = V._cam_path, V._glide
INK = P["ink"]

# ------------------------------------------------------------------ layout (stage px)
# Same arrangement as the vine scenes s21/s22 (v1 s11): the withered castor root on the LEFT, the booth to its
# right with the dead canopy arching over its roof, Jonah sitting UNDER the booth (XB + 28) facing the city.
# The knoll crest is lower than v1's (GY 830, not 710) so that the opening camera can frame Jonah exactly as
# s22's last frame does (same scale, same place in the picture) with the viewport inside the stage.
GY = 830                 # knoll crest: plant root, booth, Jonah
SP = V.SP                # 1.3, as in s21/s22
XJ = 2880                # Jonah (sitting under the booth, facing the city on the left)
XB = XJ - 28             # booth (s11/s22: XJ = XB + 28)
XP = XB - PR.CASTOR_BOOTH_DX * SP   # withered castor root (its dead canopy arches over the booth roof)
KDX = 200                # knoll detail sketch (v1) shifted right with Jonah


def kmap(x, y):
    """Map v1's knoll detail sketch (drawn for a crest at y 830) onto this knoll."""
    return (x - 160 + KDX, GY + (y - 830) * (SH + 80 - GY) / (SH + 80 - 830))


# knoll silhouette (top edge); the left slope runs down into (and over) the plain (v1's, with the lower crest)
KNOLL = [(1900, SH + 80), (2010, 1421), (2140, 1157), (2255, 985), (2335, 893), (2395, 852), (2450, 836),
         (2560, 831), (2800, 829), (3100, 825), (3400, 815), (3720, 803), (3900, 800)]

# s22 ends on END_CAM = Cam(1169, 704, 1600) with Jonah (sit_sulk, angry) at (1209, 962) under the same booth and
# plant: the same framing relative to Jonah here, so Jonah, plant and booth lie on top of each other in the dissolve
C_S22 = Cam(XJ - 40, GY - 258, 1600)

FIGS = []                # [(name, bbox, heart_spot)]
HEARTS = {}

# ------------------------------------------------------------------ the memory bubble (stage px)
BC = (XJ - 640, 320)     # bubble centre: open sky up-left of Jonah, left of the plant's crown
BRX, BRY = 300, 214      # outer radii
B_INSET = 20             # cream rim width
BUB_PIV = (BC[0] + 245, BC[1] + 130)     # it grows out of (and shrinks back into) the trail (lower right)
BPX, BPY, BPS = BC[0] - 63, BC[1] + 134, 0.46     # memory castor root + scale
TRAIL = [(XJ - 70, 526, 9), (XJ - 165, 498, 13), (XJ - 272, 470, 18)]    # from Jonah's head to the bubble

# the dry leaf that falls into Jonah's hand: it hangs from the broken leaf stub on the arching branch, just right
# of his head-cloth, with the booth's pale back cloth behind it
TWIG = (XP + 437, GY - 333)
HANG_DIR = -134          # direction of the hanging stalk from the leaf centre (deg; up and to the left)
LEAF_COL = "#c9a95e"     # sun-bleached straw: lighter than the plant's dead leaves so it reads against them

_PUNCT = "，。！？：；、,.!?:;…"


# ------------------------------------------------------------------ narration timing
def _at_in(line, phrase):
    """Start of ``phrase`` inside one subtitle chunk of ``line`` (chunk start + the share of the chunk's
    speaking time before it; punctuation weighs 1.5 characters, closing punctuation is not spoken), or None."""
    def wt(s):
        return sum(1.5 if ch in _PUNCT else 1.0 for ch in s)
    for c in line.chunks:
        i = c.text.find(phrase)
        if i < 0:
            continue
        tot = wt(c.text.rstrip(_PUNCT))
        return c.start + (c.end - c.start) * (wt(c.text[:i]) / tot if tot > 0 else 0.0)
    if phrase in line.text:
        i = line.text.find(phrase)
        return line.start + (line.end - line.start) * i / max(1, len(line.text))
    return None


def _when(ctx, phrases, default):
    """First line (in order) containing one of ``phrases`` -> that phrase's start; else ``default``."""
    for ln in ctx.lines:
        for ph in phrases:
            t = _at_in(ln, ph)
            if t is not None:
                return t
    return default


# ------------------------------------------------------------------ Jonah's extra expressions
_EXTRA_EXPRS = {
    # the voice is up and to the right (God's light): he looks up toward it, listening
    "hear": dict(eyes="dot", brow=(-0.07, 0.03, -0.04), mouth="flat", look=(-0.05, -0.11)),
    "hear_blink": dict(eyes="closed", brow=(-0.07, 0.03, -0.04), mouth="flat"),
    "leaf": dict(eyes="dot", brow=(-0.09, 0.04, 0.01), mouth="frown", look=(0.16, 0.14)),
    "leaf_blink": dict(eyes="closed", brow=(-0.09, 0.04, 0.01), mouth="frown"),
    "sorry_blink": dict(eyes="closed", brow=(-0.10, 0.05, 0.03), mouth="wobble", blush=True),
    # softened, but thoughtful (the Bible leaves Jonah's answer open; s24 asks the child): relaxed, slightly
    # raised brows, eyes down-left toward the city, no smile, no blush
    "soft": dict(eyes="dot", brow=(-0.05, 0.0, -0.04), mouth="flat", look=(0.12, 0.12)),
    "soft_blink": dict(eyes="closed", brow=(-0.05, 0.0, -0.04), mouth="flat"),
}


@contextmanager
def _exprs():
    added = [k for k in _EXTRA_EXPRS if k not in CH.EXPRS]
    for k in added:
        CH.EXPRS[k] = _EXTRA_EXPRS[k]
    try:
        yield
    finally:
        for k in added:
            CH.EXPRS.pop(k, None)


# ------------------------------------------------------------------ drawing helpers
def _castor_docs(x, y, s, states):
    """PR.castor_plant(x, y, s, side=1, seed=2, **state) markup for each state, every leaf held at its
    full-grown spin (props re-rolls later leaves' spins as new ones are born; see v1 s11 _castor_svgs)."""
    spins = {}
    orig = PR._palmate

    def palmate(cx, cy, r, lobes, spin, tilt, hang, fill, vein, wither=0.0, seed=0, sw=4.0):
        return orig(cx, cy, r, lobes, spins.setdefault(seed, spin), tilt, hang, fill, vein, wither, seed, sw)

    PR._palmate = palmate
    try:
        PR.castor_plant(x, y, s, growth=1.0, side=1, seed=2)
        return [PR.castor_plant(x, y, s, side=1, seed=2, **st) for st in states]
    finally:
        PR._palmate = orig


def _scallop(cx, cy, rx, ry, n=13, k=0.62, rot=-0.3):
    """A thought-bubble cloud: arcs bulging outward between n points on an ellipse (clockwise)."""
    pts = [(cx + rx * math.cos(rot + 2 * math.pi * i / n), cy + ry * math.sin(rot + 2 * math.pi * i / n))
           for i in range(n)]
    d = f"M{f1(pts[0][0])},{f1(pts[0][1])}"
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        r = math.hypot(b[0] - a[0], b[1] - a[1]) * k
        d += f" A{f1(r)},{f1(r)} 0 0 1 {f1(b[0])},{f1(b[1])}"
    return d + " Z"


def _star4(x, y, r, col="#fff3c8", op=0.95):
    w = r * 0.28
    return (f'<path d="M{f1(x)},{f1(y - r)} L{f1(x + w)},{f1(y - w)} L{f1(x + r)},{f1(y)} L{f1(x + w)},{f1(y + w)} '
            f'L{f1(x)},{f1(y + r)} L{f1(x - w)},{f1(y + w)} L{f1(x - r)},{f1(y)} L{f1(x - w)},{f1(y - w)} Z" '
            f'fill="{col}" opacity="{op}"/>')


def _cam_dur(cams, r, peak=19.0):
    """Shortest glide time (s) through ``cams`` with ramp fraction ``r`` that keeps the peak camera speed at
    ``peak`` output px per frame (30 fps)."""
    _, tot, _ = _cam_path(cams)
    return tot / (peak * 30.0 * (1 - r))


def _qmark(x, y, s=1.0):
    """A hand-lettered '?' (cream fill, umber ink rim) centred at (x, y), ~70*s px tall."""
    body = (S.text(f1(x), f1(y + 25 * s), "?", size=round(78 * s), fill="#fff4dc",
                   extra=f'stroke="{INK}" stroke-width="{f1(9 * s)}" stroke-linejoin="round" paint-order="stroke"'))
    return S.g(body, filter="wobble-fine")


def _place_hearts(names, rise=72, half=27, extra_obstacles=()):
    """Heart spot above each named figure; nudged sideways (or dropped) if its rising column would cross
    another figure (hearts are drawn over everything). Same rule as v1."""
    boxes = {n: b for n, b, _ in FIGS}
    obstacles = [(n, b) for n, b in boxes.items()] + list(extra_obstacles)
    out = []
    for name, _, spot in FIGS:
        if name not in names or spot is None:
            continue
        x0, y0 = spot
        for dx in (0, -16, 16, -32, 32, -48, 48):
            x = x0 + dx
            col = (x - half, y0 - rise - half, x + half, y0 + 20)
            hit = any(n != name and col[0] < b[2] - 4 and col[2] > b[0] + 4 and col[1] < b[3] - 4 and col[3] > b[1] + 4
                      for n, b in obstacles)
            if not hit:
                out.append((x, y0))
                break
    return out


def _rot_pt(p, c, deg):
    r = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))


def _catmull(pts, u):
    """Point at u (0..1, uniform per segment) on a Catmull-Rom curve through pts."""
    n = len(pts) - 1
    f = _clamp(u) * n
    i = min(n - 1, int(f))
    v = f - i
    p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(n, i + 2)]
    v2, v3 = v * v, v * v * v
    return tuple(0.5 * (2 * p1[j] + (p2[j] - p0[j]) * v + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * v2 +
                        (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * v3) for j in range(2))


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    FIGS.clear()
    HEARTS.clear()

    def when(phrases, default):
        return _when(ctx, phrases if isinstance(phrases, (list, tuple)) else [phrases], default)

    # --- key times (all from the narration) ---------------------------------------------------------
    l_first = L[0]
    t_still = 1.0                                             # the dissolve from s22: nothing starts before
    t_name = max(t_still + 0.12, l_first.start + 0.3)         # "约拿，" -> he looks up, listening (hop)
    t_plant = when("这棵蓖麻", l_first.start + 1.0)          # a dry leaf wobbles loose ...
    t_fall0 = t_plant + 0.35
    t_catch = t_fall0 + 1.75                                   # ... and lands in his hand
    t_grow_line = when(["也不是你", "长大"], t_catch + 1.2)    # "也不是你让它长大的" -> turns the leaf
    t_night1 = when(["一夜长起来", "一夜长"], t_grow_line + 3.5)
    t_night2 = when(["一夜又", "又枯", "又干"], t_night1 + 1.8)
    t_dead = when(["枯死了", "干死了", "枯死", "干死"], t_night2 + 0.8)
    t_tender = when(["你都这么", "你尚且", "心疼它", "爱惜它"], t_dead + 1.0)        # "你都这么心疼它" -> sorry, tender
    t_city = when(["尼尼微"], t_tender + 2.5)
    t_many = when(["十二万"], t_city + 1.5)
    t_kids = when(["分不清左右", "左右手", "不能分辨"], t_many + 2.0)
    t_lr = when(["左右手"], t_kids + 0.6)
    t_dunno = when(["不知道"], t_kids + 3.5)
    t_wrong = when(["什么是错"], t_dunno + 1.8)
    t_beasts = when(["还有许多", "牛羊", "牲畜"], t_dunno + 3.6)
    t_how = when(["我怎么能", "我怎能", "怎么能"], t_beasts + 2.4)
    t_care = when(["心疼他们", "爱惜他们", "不心疼", "不爱惜"], t_how + 1.0)

    # bubble
    t_trail = t_night1 - 0.75
    t_bin = t_night1 - 0.42                                    # the cloud pops in
    t_g0 = t_night1 + 0.05                                     # the sprout springs up ...
    t_g1 = max(t_g0 + 0.9, t_night2 - 0.8)                     # ... to a tall plant; morning in the bubble
    t_w0 = max(t_night2 + 0.35, t_dead - 0.35)                 # night again: it droops ...
    t_w1 = t_w0 + 1.1                                          # ... and withers
    t_bout = max(t_w1 + 0.55, t_tender + 0.35)                 # the bubble shrinks back into the trail
    # children: '?' and left/right swaps
    t_q0 = t_lr - 0.05
    lr_hops = [t_q0 - 0.12 + 0.95 * k for k in range(4)]        # into pointing, then swaps
    t_lr_end = max(lr_hops[-1] + 0.95, t_wrong - 0.6)          # hop back to standing, smiling

    # camera (views; every glide's duration is checked against the speed limit with _cam_dur)
    C0 = C_S22                          # as s22 leaves him: same scale, same place in the frame
    C0b = Cam(XJ - 14, 556, 1410)       # slow push-in on Jonah and the leaf while God speaks
    Cb = Cam(BC[0] + 290, 452, 1520)    # room for the memory bubble on the left
    Cb2 = Cam(BC[0] + 302, 458, 1494)
    Cw = Cam(1880, 840, 2800)           # held wide view: the city, the plain, the pasture, Jonah under his booth
    Cw2 = Cam(1856, 852, 2760)
    C1 = Cam(820, 1100, 1440)           # the children
    C1b = Cam(930, 1092, 1440)
    C2 = Cam(1650, 1080, 2000)          # the pasture (the children still at its left edge)
    C2h = Cam(1690, 1070, 1984)         # a slow drift while the animals are named
    C3 = Cam(2560, 770, 2160)           # Jonah under his booth, looking down at the city and the pasture
    Cf = Cam(XJ - 10, 600, 1430)        # slow push-in: a calm last frame on Jonah's face
    t_pull0 = t_bout + 0.25
    t_pull1 = max(t_city + 1.7, t_pull0 + 3.6)                 # settled on the wide city
    t_down0 = max(t_pull1 + 0.9, t_many + 0.1)                 # glide down to the people and the children
    t_down1 = max(t_down0 + 3.5, t_lr + 0.9)
    t_c2 = t_beasts + 0.15                                     # settled on the animals as they are named
    t_go = max(t_down1 + 0.5, min(t_c2 - _cam_dur([C1b, C2], 0.3), t_lr_end + 0.1))   # leave the children
    t_baa = t_beasts + 0.5                                     # a sheep bleats (camera at rest)
    dur_rise = _cam_dur([C2h, C3], 0.3)
    t_back = max(t_care - 0.1, t_c2 + 1.0 + dur_rise)          # arrive on Jonah just before "心疼他们"
    t_rise = t_back - dur_rise                                 # rise from the pasture to Jonah
    t_soft = max(t_back + 0.15, t_care - 0.1)                  # his face softens
    t_hearts_p0, t_hearts_p1 = t_dunno - 0.2, t_beasts + 0.2
    t_hearts_a0, t_hearts_a1 = t_beasts - 0.1, t_rise + 0.2

    # =============================================================== SKY
    sky = doc(
        S.rect_bg("url(#sky)", SW, SH) +
        f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="760" fill="url(#sunglow)"/>',
        defs=S.lin_grad("sky", [(0, "#bfc3d8"), (0.16, "#e6c6b6"), (0.3, "#f6d2a2"), (0.42, "#fbe0ad"),
                                (1, "#fbe6b8")]) +
        S.rad_grad("sunglow", [(0, "#fff6d2", 0.95), (0.25, "#ffe6a4", 0.6), (0.6, "#fbd08a", 0.22),
                               (1, "#f8c784", 0)]))
    sc.add("sky", sky, z=0, wc=0.5)
    sun = doc(S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="92" fill="#fcd877" stroke="#eaa951" stroke-width="5"/>'
                  f'<circle cx="{SUN[0] - 26}" cy="{SUN[1] - 26}" r="34" fill="#fffaf0" opacity="0.45"/>',
                  filter="wobble"))
    sc.add("sun", sun, z=1, wc=0.4)

    far_clouds = doc(S.g(
        S.cloud(980, 190, 360, 100, "#fdf0e0", seed=4, sw=3, shade_fill="#f2cdb6") +
        S.cloud(1660, 112, 300, 86, "#fdeedd", seed=6, sw=3, shade_fill="#f2cdb6") +
        S.cloud(150, 120, 260, 80, "#fdf0e0", seed=7, sw=3, shade_fill="#f2cdb6"), filter="wobble"))
    sc.add("far_clouds", far_clouds, z=2, wc=0.6)
    # left clouds: well clear of the memory bubble (BC +- (300, 214)) the whole time
    cl_l = doc(S.g(S.cloud(BC[0] - 560, 236, 420, 116, "#fdf1e2", seed=11, sw=3.5, shade_fill="#f0c9b0") +
                   S.cloud(BC[0] - 900, 330, 220, 66, "#fdf1e2", seed=14, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    # right: s22's soft veil cloud (same drawing, same place relative to Jonah as s22's last frame), God's light
    # fans down from under its lower-left edge; a second cloud further east
    VEIL = (XJ + 241, GY - 688)          # (s22's veil has drifted 50 px left by its end)
    GAP = (XJ + 131, GY - 598)
    cl_r = doc(S.g(S.cloud(VEIL[0], VEIL[1] - 4, 610, 214, "#fff2b8", seed=12, sw=0), filter="blur-md") +
               S.g(S.cloud(VEIL[0], VEIL[1], 520, 170, "#fff6e2", seed=12, sw=3.5, shade_fill="#f8d596") +
                   S.cloud(XJ + 760, 330, 280, 84, "#fdf1e2", seed=13, sw=3, shade_fill="#f0c9b0"), filter="wobble"))
    part = lambda t: M.progress(t, t_name - 0.1, t_name + 2.2, "inout")
    sc.add("cloud_l", cl_l, z=5.2, wc=0.6, motion=lambda t: Tf(dx=-70 * part(t) - 4 * t))
    sc.add("cloud_r", cl_r, z=5.3, wc=0.6, motion=M.combine(lambda t: Tf(dx=70 * part(t) - 4 * t), M.bob(5, 4.2, 0.21)))

    # =============================================================== LAND (static, flattened; as v1)
    FAR_INK = 'stroke="#9a7a60" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"'
    far = ""
    far += S.path(S.smooth_path([(-80, 560), (200, 520), (520, 540), (820, 505), (1150, 530), (1500, 500),
                                 (1850, 525), (2150, 470), (2450, 500), (2750, 455), (3050, 490), (3350, 440),
                                 (3650, 470), (3900, 450)],
                                closed=False) + " L3900,900 L-80,900 Z", fill="#e6cbb8", stroke=False, extra=FAR_INK)
    far += S.path(S.smooth_path([(-80, 640), (400, 610), (900, 630), (1600, 600), (2300, 600), (2600, 575),
                                 (2950, 600), (3250, 565), (3550, 590), (3900, 570)], closed=False) +
                  " L3900,900 L-80,900 Z", fill="#e8d2aa", stroke=False, extra=FAR_INK)
    far += S.path(S.smooth_path([(2200, 612), (2450, 580), (2700, 604), (2950, 566), (3250, 592), (3550, 556),
                                 (3900, 574)], closed=False) + " L3900,900 L2200,900 Z", fill="#ecd3a0", stroke=False,
                  extra=FAR_INK)
    for (x, y, w_) in [(2480, 622, 140), (2900, 608, 180), (3300, 596, 150), (3680, 604, 120)]:
        far += (f'<path d="M{x - w_ / 2},{y} q{w_ / 2},-14 {w_},0" fill="none" stroke="#d9b98a" stroke-width="4" '
                f'opacity="0.6" stroke-linecap="round"/>')
    for (x, y, s) in [(2330, 604, 0.12), (2380, 608, 0.1), (3060, 576, 0.11)]:
        far += PR.palm_tree(x, y, s, lean=0.1)
    sc.add("far_hills", doc(S.g(far, filter="wobble")), z=3, wc=0.6)
    city = PR.nineveh_skyline(-60, 2240, 668, scale=0.62, seed=3, haze=0.45, tint="#f6dcb0")
    sc.add("city", doc(city), z=3.1, wc=0.6)

    pl = f'<rect x="-40" y="{WALL_Y - 40}" width="2560" height="{SH - WALL_Y + 120}" fill="url(#plain)"/>'
    pl += (f'<rect x="2000" y="{WALL_Y - 40}" width="{SW - 1900}" height="{SH - WALL_Y + 120}" fill="url(#plainfade)"/>')
    rng = np.random.default_rng(7)
    past = S.smooth_path([(1180, 1040), (1450, 990), (1800, 985), (2150, 1000), (2420, 1040), (2470, 1300),
                          (2360, SH + 60), (900, SH + 60), (1000, 1300)], closed=True, tension=0.9)
    pl += f'<path d="{past}" fill="url(#past)" stroke="{INK}" stroke-width="3"/>'
    play = S.blob(820, 1140, 520, 140, wobble=0.06, n=12, seed=5)
    pl += f'<path d="{play}" fill="#ead39a" opacity="0.75"/>'
    road = S.smooth_path([(GATE_X - 58, WALL_Y + 2), (GATE_X - 90, 900), (GATE_X - 200, 1080), (GATE_X - 330, 1300),
                          (GATE_X - 420, SH + 60), (GATE_X - 120, SH + 60), (GATE_X - 60, 1300), (GATE_X - 20, 1080),
                          (GATE_X + 30, 900), (GATE_X + 58, WALL_Y + 2)], closed=True, tension=0.8)
    pl += f'<path d="{road}" fill="#f2e0b2" stroke="{INK}" stroke-width="3"/>'
    pl += (f'<path d="M{GATE_X - 40},{WALL_Y + 40} Q{GATE_X - 120},1050 {GATE_X - 250},1500" fill="none" '
           f'stroke="#dcc28c" stroke-width="5" stroke-dasharray="2 26" stroke-linecap="round"/>')
    flowers = ""
    for _ in range(140):
        x, y = rng.uniform(1050, 2380), rng.uniform(1040, SH)
        col = ["#f7f0d8", "#f3c34f", "#ef9d8f", "#d6b2e0"][int(rng.integers(0, 4))]
        r = 3 + (y - 1000) / 160
        flowers += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="0.9"/>'
    for _ in range(110):
        x, y = rng.uniform(-40, 2400), rng.uniform(900, SH)
        ln = 8 + (y - 900) / 40
        flowers += (f'<path d="M{x:.0f},{y:.0f} l{-ln * 0.3:.1f},{-ln:.1f} M{x + 5:.0f},{y:.0f} l{ln * 0.25:.1f},{-ln * 0.9:.1f}" '
                    f'stroke="#8faa52" stroke-width="2.4" stroke-linecap="round" opacity="0.7"/>')
    pl += flowers
    pl += '<ellipse cx="1150" cy="1080" rx="1350" ry="560" fill="url(#cg)"/>'
    pl += f'<rect x="-40" y="{WALL_Y - 40}" width="2600" height="{SH - WALL_Y + 120}" fill="url(#late)"/>'
    plain_defs = (S.lin_grad("plain", [(0, "#e4cf8c"), (0.25, "#d4cd84"), (1, "#b3bf6b")]) +
                  S.lin_grad("plainfade", [(0, "#ecd3a0", 0), (0.2, "#ecd3a0", 1), (1, "#ecd3a0", 1)], x2=1, y2=0) +
                  S.lin_grad("past", [(0, "#b0cb6c"), (0.5, "#9dbf60"), (1, "#8ab156")]) +
                  S.rad_grad("cg", [(0, "#fff0c0", 0.32), (0.55, "#ffe6a8", 0.14), (1, "#ffe0a0", 0)]) +
                  S.lin_grad("late", [(0, "#ffd98a", 0.24), (0.45, "#ffe2a2", 0.1), (1, "#ffe2a2", 0)], x2=1, y2=0))
    field_cols = ["#c9cc7e", "#e6cf88", "#b5c271", "#dcc47c", "#c3cf86"]
    xs = [-60, 260, 560, 900, 1180, 1560, 1860, 2140, 2420]
    fields = ""
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + 10, xs[i + 1] - 10
        fields += V._field(x0, x1, WALL_Y + 10, WALL_Y + 58 + 20 * (i % 3), field_cols[i % len(field_cols)], seed=40 + i)
    sc.add("plain", doc(S.g(pl, filter="wobble") + S.g(fields, filter="wobble-strong"), plain_defs), z=4, wc=0.8)

    WALL_TOP = WALL_Y - 170
    walkers_top = ""
    for i, (x, kind, pose) in enumerate([(390, "man", "stand"), (420, "woman", "stand"), (720, "child", "cheer"),
                                         (745, "man", "stand"), (1010, "woman", "cheer"), (1180, "man", "stand"),
                                         (1205, "child", "stand"), (1610, "woman", "stand"), (1640, "man", "cheer"),
                                         (1840, "elder", "stand"), (2060, "man", "stand"), (2085, "woman", "cheer")]):
        sc_ = 0.15 if kind != "child" else 0.17
        walkers_top += CH.citizen(x, WALL_TOP + (22 if kind != "child" else 8), sc_, 1 if i % 2 else -1, kind=kind,
                                  variant=i % 4, pose=pose, expr="happy")
    wall = PR.city_wall(-60, 2320, WALL_Y, height=170, gate=(GATE_X, 140), doors_open=1.0, seed=2, ink=0.55)
    wall += V._end_tower(2320, WALL_Y, 170 / 260, ink=0.55)
    gateway = (CH.citizen(GATE_X - 40, WALL_Y - 2, 0.28, 1, kind="woman", variant=3, pose="stand", expr="happy") +
               CH.citizen(GATE_X + 42, WALL_Y - 2, 0.25, -1, kind="child", variant=1, pose="stand", expr="happy"))
    haze = ('<filter id="hz" x="-2%" y="-8%" width="104%" height="116%" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="saturate" values="0.72"/>'
            '<feColorMatrix type="matrix" values="0.74 0 0 0 0.251  0 0.74 0 0 0.229  0 0 0.74 0 0.195  0 0 0 1 0"/>'
            '</filter>')
    sc.add("wall", doc(f'<g filter="url(#hz)">{walkers_top}{wall}{gateway}</g>', haze), z=4.1, wc=0.7)

    mid = ""
    for (x, y, s, ln) in [(120, 812, 0.4, -0.1), (470, 806, 0.36, 0.15), (1060, 812, 0.34, 0.1),
                          (1700, 810, 0.38, -0.12), (2050, 818, 0.42, 0.1), (2240, 830, 0.34, -0.2)]:
        mid += PR.palm_tree(x, y, s, lean=ln)
    for (x, y, s, sd) in [(760, 860, 0.32, 1), (1880, 880, 0.34, 2)]:
        mid += PR.olive_tree(x, y, s, seed=sd)
    for (x, y, s, v) in [(30, 960, 0.5, 0), (190, 905, 0.4, 1), (1700, 965, 0.42, 3), (2120, 1000, 0.5, 0),
                         (1215, 990, 0.4, 1), (60, 1300, 0.7, 1)]:
        mid += PR.bush(x, y, s, variant=v)
    mid += V._well(470, 1040, 0.62)
    sc.add("mid", doc(mid), z=4.2, wc=0.8)

    # Jonah's knoll (as v1)
    kd = S.smooth_path(KNOLL, closed=False) + f" L{SW + 80},{SH + 80} L{KNOLL[0][0]},{SH + 80} Z"
    knoll = S.path(kd, fill="url(#kn)", sw=4.5)
    rp = [(x + 12, y + 18) for x, y in KNOLL[2:]]
    knoll += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f7dfaa" stroke-width="18" opacity="0.6"/>'
    terr = [(1890, 1640), (2060, 1470)] + [kmap(x, y) for x, y in [(2450, 1330), (2800, 1250), (3200, 1215),
                                                                    (3550, 1190), (3900, 1170)]] + [(3900, 1095)]
    knoll += S.path(S.smooth_path(terr, closed=False) + f" L3900,{SH + 80} L1880,{SH + 80} Z", fill="url(#kn2)", sw=4)
    knoll += (f'<path d="{S.smooth_path([(x + 10, y + 16) for x, y in terr[1:]], closed=False)}" fill="none" '
              f'stroke="#ecc98e" stroke-width="12" opacity="0.5"/>')
    fp = S.smooth_path([kmap(x, y) for x, y in [(2330, SH + 60), (2420, 1450), (2560, 1300), (2700, 1180), (2760, 1050),
                                                (2700, 930), (2760, 862), (2800, 858), (2790, 935), (2840, 1050),
                                                (2790, 1190), (2650, 1320), (2540, 1460), (2480, SH + 60)]],
                       closed=True, tension=0.8)
    knoll += f'<path d="{fp}" fill="#f2d9a6" opacity="0.85"/>'
    for (x, y, w_) in [(2900, 960, 200), (3300, 900, 240), (3600, 1000, 180), (3050, 1110, 220), (2600, 1050, 120),
                       (3400, 1090, 200), (2950, 1350, 260), (3500, 1330, 220), (2500, 1180, 110), (3200, 1500, 260)]:
        x, y = kmap(x, y)
        knoll += (f'<path d="M{x - w_ / 2:.0f},{y:.0f} q{w_ / 2},-16 {w_},0" fill="none" stroke="#c4935a" stroke-width="4" '
                  f'opacity="0.42" stroke-linecap="round"/>')
    for (x, y, r) in [(2660, 852, 9), (3180, 846, 8), (3220, 852, 6), (3560, 842, 9), (2540, 935, 7), (2470, 1010, 8),
                      (2380, 1150, 9), (2960, 1240, 8), (3380, 1265, 7)]:
        x, y = kmap(x, y)
        knoll += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.4}" ry="{r}" fill="{P["stone"]}" stroke="{INK}" stroke-width="3"/>'
    knoll += V._rock(*kmap(2330, 1260), 130, 58, seed=43, sw=4) + V._rock(*kmap(3540, 1010), 110, 50, seed=44, sw=4)
    knoll += (PR.bush(*kmap(2560, 1120), 0.6, variant=2) + PR.bush(*kmap(3700, 900), 0.7, variant=2) +
              PR.bush(*kmap(3080, 1235), 0.75, variant=2))
    for (x, y, s_) in [(2600, 880, 0.7), (3150, 845, 0.6), (2430, 1080, 0.75), (3330, 1000, 0.7), (2880, 1200, 0.8),
                       (3700, 1180, 0.9)]:
        knoll += PR.grass_tuft(*kmap(x, y), s_, variant=1)
    sc.add("knoll", doc(S.g(knoll, filter="wobble"),
                        S.lin_grad("kn", [(0, "#ebc68a"), (0.3, "#e2b679"), (1, "#d09c62")]) +
                        S.lin_grad("kn2", [(0, "#d3a065"), (1, "#bb8652")])), z=5, wc=0.9)

    booth = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{INK}" opacity="0.16" '
             f'filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    booth += PR.jar(XB + 372, GY - 50, 0.6) + PR.sack(XB + 444, GY + 3, 0.62, seed=3)    # beside the booth
    sc.add("booth", doc(booth), z=5.6, wc=0.8)

    # =============================================================== PEOPLE on the plain
    ground_sh = []

    def register(name, bbox, heart):
        FIGS.append((name, bbox, heart))

    def person(name, x, y, kind, variant, pose="stand", facing=1, expr="happy", motion=None, frames=None,
               frame_at=None, s=None, hops=None, H=0):
        """frames: [(pose, expr)] or [(pose, expr, facing)] for a flipbook."""
        s = s or plain_scale(y)
        if frames is None:
            frames = [(pose, expr, facing)]
        frames = [f if len(f) == 3 else (f[0], f[1], facing) for f in frames]
        svg = [doc(CH.citizen(x, y, s, fc, kind=kind, variant=variant, pose=p, expr=e)) for p, e, fc in frames]
        sc.add(name, svg if len(svg) > 1 else svg[0], z=6 + y / 1000, wc=0.6, motion=motion, frame_at=frame_at)
        width, height = (90, 224) if kind == "child" else (120, 330)
        sh = long_shadow(x, y, s, width, height)
        if hops:
            sc.add(name + "_sh", shdoc(sh), z=5.95 + y / 100000, wc=0, motion=shadow_motion(x, y, hops))
        else:
            ground_sh.append(sh)
        bbs = [CH.body_points(CH.citizen, x, y, s, fc, kind=kind, variant=variant, pose=p) for p, _, fc in frames]
        bb = (min(b["bbox"][0] for b in bbs), min(b["bbox"][1] for b in bbs) - H,
              max(b["bbox"][2] for b in bbs), y + 4)
        top = bbs[0]["head_top"]
        register(name, bb, (top[0], top[1] - 25 - H))
        return s

    def breathe(x, y, ph, amt=0.012, per=2.8):
        return M.breathe(amt, per, pivot=(x, y), phase=ph)

    def nod(x, y, ph, deg=1.2, per=2.6):
        return M.sway(deg, per, pivot=(x, y), phase=ph)

    # elders by the well, talking across it
    person("elder0", 380, 1010, "elder", 0, "stand", 1, "happy", motion=M.combine(nod(380, 1010, 0.1), breathe(380, 1010, 0.3)))
    person("elder1", 600, 990, "elder", 1, "stand", -1, "peaceful", motion=M.combine(nod(600, 990, 0.6, 1.0, 3.1),
                                                                                    breathe(600, 990, 0.7)))
    # families: father, mother and child together
    person("father0", 650, 1060, "man", 2, "stand", 1, "happy", motion=M.combine(nod(650, 1060, 0.35, 1.0, 3.3),
                                                                                breathe(650, 1060, 0.6)))
    person("mother0", 700, 1072, "woman", 1, "stand", 1, "happy", motion=M.combine(nod(700, 1072, 0.2, 1.5, 3.0),
                                                                                  breathe(700, 1072, 0.1)))
    person("girl0", 736, 1088, "child", 1, "stand", -1, "happy", motion=M.combine(M.bob(2.5, 1.7, 0.2),
                                                                                  breathe(736, 1088, 0.5)))
    person("mother1", 1180, 940, "woman", 3, "stand", -1, "happy", motion=M.combine(nod(1180, 940, 0.4, 1.2, 2.7),
                                                                                    breathe(1180, 940, 0.9)))
    person("father1", 1226, 934, "man", 1, "stand", -1, "happy", motion=M.combine(nod(1226, 934, 0.75, 1.0, 3.4),
                                                                                  breathe(1226, 934, 0.4)))
    person("child_g", 1157, 952, "child", 2, "stand", 1, "happy", motion=M.combine(M.bob(2.5, 1.5, 0.3),
                                                                                   breathe(1157, 952, 0.2)))
    person("grandpa", 300, 1290, "elder", 2, "stand", 1, "happy", motion=M.combine(nod(300, 1290, 0.15, 1.2, 2.8),
                                                                                   breathe(300, 1290, 0.4)))
    person("mother2", 430, 1322, "woman", 2, "stand", 1, "happy", motion=M.combine(nod(430, 1322, 0.55, 1.4, 3.2),
                                                                                   breathe(430, 1322, 0.2)))

    # children playing (hops with rests: stand <-> cheer)
    for (nm, x, y, v, fc, seed, H, s_) in [("kid2", 1005, 1295, 3, 1, 5, 22, None), ("kid3", 560, 1185, 1, 1, 6, 18, None),
                                           ("toddler", 470, 1338, 0, -1, 7, 13, 0.56),
                                           # (two more little ones playing face to face, between the family and the
                                           # wall - clear of the ball's arc between kid0 and kid1)
                                           ("kid4", 830, 975, 0, 1, 11, 16, None),
                                           ("kid5", 884, 966, 3, -1, 12, 16, None)]:
        hops = hop_sched(seed, T + 1)
        person(nm, x, y, "child", v, facing=fc, frames=[("stand", "happy"), ("cheer", "happy")],
               frame_at=hop_frame(hops), motion=hop_motion(x, y, hops, H), s=s_, hops=hops, H=H)

    # two children tossing a ball (as v1)
    PB = 1.25
    BALL_H = 14
    kidA, kidB = (962, 1200, 0, 1), (1222, 1215, 2, -1)
    catch_pts = []
    for i, (x, y, v, fc) in enumerate((kidA, kidB)):
        arrivals = [PB * (2 * k + i) for k in range(int(T / (2 * PB)) + 3)]
        hops = [(ta - 0.15, 0.45) for ta in arrivals]

        def arms(t, arrivals=arrivals):
            return 1.0 if any(ta - 0.38 <= t <= ta + 0.3 for ta in arrivals) else 0.0
        s_ = person(f"kid{i}", x, y, "child", v, facing=fc, frames=[("stand", "happy"), ("cheer", "happy")],
                    frame_at=arms, motion=hop_motion(x, y, hops, BALL_H), hops=hops, H=BALL_H)
        hand = CH.body_points(CH.citizen, x, y, s_, fc, kind="child", variant=v, pose="cheer")["hands"][0]
        lift = BALL_H * math.sin(math.pi * 0.15 / 0.45)
        catch_pts.append((hand[0] + 4 * fc, hand[1] - 22 * s_ - lift))
    (xa, ya), (xb, yb) = catch_pts
    ARC = 175
    ball_svg = doc(S.g(f'<circle cx="1060" cy="900" r="15" fill="#e2683f" stroke="{INK}" stroke-width="3.5"/>'
                       f'<path d="M1046,895 Q1060,884 1074,895" fill="none" stroke="#f6d36a" stroke-width="4"/>'
                       f'<path d="M1048,908 Q1060,916 1072,906" fill="none" stroke="#3b8b89" stroke-width="4"/>',
                       filter="wobble-fine"))

    def ball(t):
        u = (t / PB) % 2.0
        if u < 1:
            x0, y0, x1, y1, v = xa, ya, xb, yb, u
        else:
            x0, y0, x1, y1, v = xb, yb, xa, ya, u - 1
        x = x0 + (x1 - x0) * v
        y = y0 + (y1 - y0) * v - ARC * 4 * v * (1 - v)
        return Tf(dx=x - 1060, dy=y - 900, rot=360 * v, px=1060, py=900)
    sc.add("ball", ball_svg, z=7.5, wc=0.4, motion=ball)
    ball_zone = []
    for k in range(11):
        v = k / 10
        x_, y_ = xa + (xb - xa) * v, ya + (yb - ya) * v - ARC * 4 * v * (1 - v)
        ball_zone.append(("ball", (x_ - 20, y_ - 20, x_ + 20, y_ + 20)))

    # the two little ones who can't tell left from right: side by side they both point "this way!" (left),
    # then hop and point "that way!" (right), back and forth, a '?' over each head; then they hop back to
    # face each other, smiling
    LR = [("lr_a", 690, 1262, 1, 1), ("lr_b", 822, 1254, 2, -1)]
    q_spots = []
    for j, (nm, x, y, v, fc) in enumerate(LR):
        hops = [(th + 0.12 * j, 0.36) for th in lr_hops] + [(t_lr_end + 0.12 * j, 0.42)]
        # frames: 0 stand (happy, facing the other), 1 point left, 2 point right, 3 stand smiling
        frames = [("stand", "happy", fc), ("point", "worried", -1), ("point", "worried", 1), ("stand", "happy", fc)]
        cuts = [h[0] + 0.03 for h in hops]

        def lr_frame(t, cuts=cuts):
            k = sum(1 for c in cuts if t >= c)
            if k == 0:
                return 0.0
            if k >= len(cuts):
                return 3.0
            return 1.0 if k % 2 == 1 else 2.0
        s_ = person(nm, x, y, "child", v, frames=frames, frame_at=lr_frame,
                    motion=M.combine(hop_motion(x, y, hops, 15), breathe(x, y, 0.3 * j)), hops=hops, H=15)
        top = CH.body_points(CH.citizen, x, y, s_, fc, kind="child", variant=v, pose="stand")["head_top"]
        q_spots.append((top[0], top[1] - 50, j))

    for (qx, qy, j) in q_spots:
        tq = t_q0 + 0.15 * j
        sc.add(f"q{j}", doc(_qmark(qx, qy, 1.0)), z=9.2, wc=0.2, motion=lambda t, qx=qx, qy=qy, tq=tq: Tf(
            dy=-4 * math.sin(2 * math.pi * (t - tq) / 1.1),
            rot=8 * math.sin(2 * math.pi * (t - tq) / 1.9),
            sx=0.4 + 0.6 * M.progress(t, tq, tq + 0.3, "back"), sy=0.4 + 0.6 * M.progress(t, tq, tq + 0.3, "back"),
            alpha=_env(t, tq, tq + 0.12, t_lr_end - 0.15, t_lr_end + 0.15), px=qx, py=qy + 30))

    # men and women near the gate and along the wall (far, small)
    person("man0", GATE_X - 140, 838, "man", 0, "stand", 1, "happy", motion=breathe(GATE_X - 140, 838, 0.2))
    person("woman0", GATE_X + 120, 842, "woman", 0, "stand", -1, "happy", motion=breathe(GATE_X + 120, 842, 0.6))
    person("man1", GATE_X + 210, 852, "man", 2, "cheer", -1, "happy",
           motion=M.combine(nod(GATE_X + 210, 852, 0.3, 2.0, 1.6), breathe(GATE_X + 210, 852, 0.1)))
    person("man2", 250, 868, "man", 1, "stand", 1, "happy", motion=breathe(250, 868, 0.4))
    person("woman1", 940, 880, "woman", 2, "cheer", 1, "happy",
           motion=M.combine(nod(940, 880, 0.1, 2.0, 1.8), breathe(940, 880, 0.3)))

    # people walking in and out of the gate (2-frame walk flipbook while x / y move)
    def walker(name, kind, variant, p0, p1, facing, step=0.36, phase=0.0):
        (x0, y0), (x1, y1) = p0, p1
        s0 = plain_scale(y0)
        w_, h_ = (90, 224) if kind == "child" else (120, 330)
        frames = [shdoc(long_shadow(x0, y0, s0, w_, h_) +
                        CH.citizen(x0, y0, s0, facing, kind=kind, variant=variant, pose=p, expr="happy"))
                  for p in ("walk_a", "walk_b")]
        ta, tb = -1.0, T + 1.0

        def m(t):
            u = _clamp((t - ta) / (tb - ta))
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            k = plain_scale(y) / s0
            return Tf(dx=x - x0, dy=y - y0, sx=k, sy=k, px=x0, py=y0)
        sc.add(name, frames, z=6 + (y0 + y1) / 2000, wc=0.6, motion=m,
               frame_at=lambda t: float(int(t / step + phase) % 2))

    walker("walk0", "man", 3, (GATE_X + 12, WALL_Y + 6), (GATE_X - 170, 1070), -1, 0.38)
    walker("walk0c", "child", 0, (GATE_X + 60, WALL_Y + 14), (GATE_X - 96, 1062), -1, 0.3, 0.5)
    walker("walk1", "woman", 2, (780, 818), (1290, 818), 1, 0.36, 0.5)
    walker("walk2", "elder", 3, (1760, 812), (1470, 800), -1, 0.42)

    # =============================================================== ANIMALS in the pasture
    def beast(name, x, y, kind, facing, s, motion=None, hops=None, H=0):
        sc.add(name, doc(PR.animal(x, y, s, facing, kind=kind)), z=6 + y / 1000, wc=0.6, motion=motion)
        l, t_, r, b = ABOX[kind]
        width = (r - l) * 0.85
        sh = long_shadow(x, y, s, width, (b - t_) * 0.75)
        if hops:
            sc.add(name + "_sh", shdoc(sh), z=5.95 + y / 100000, wc=0, motion=shadow_motion(x, y, hops))
        else:
            ground_sh.append(sh)
        if facing < 0:
            l, r = -r, -l
        register(name, (x + l * s, y + t_ * s - H, x + r * s, y + b * s),
                 (x + HEAD_DX[kind] * s * facing, y + t_ * s - 25 - H))

    sheep = [(1380, 1245, 1, 0.6), (1640, 1292, -1, 0.62), (1760, 1225, -1, 0.58), (1480, 1395, 1, 0.66),
             (1840, 1390, 1, 0.64)]
    for i, (x, y, fc, s) in enumerate(sheep):
        mot = M.combine(M.bob(2.5, 2.2 + 0.3 * i, i * 0.27), nod(x, y, i * 0.31, 1.2, 2.9))
        hops = None
        if i == 1:     # the one who bleats: a happy little hop
            hops = [(t_baa - 0.12, 0.38)]
            mot = M.combine(mot, hop_motion(x, y, hops, 16))
        beast(f"sheep{i}", x, y, "sheep", fc, s, mot, hops=hops, H=16 if hops else 0)
    for i, (x, y, fc) in enumerate([(1300, 1445, 1), (1740, 1465, -1)]):
        hops = hop_sched(20 + i, T + 1, dur=(0.34, 0.44), rest=(0.7, 1.3))
        beast(f"lamb{i}", x, y, "sheep", fc, 0.4, hop_motion(x, y, hops, 18), hops=hops, H=18)
    beast("goat0", 1840, 1110, "goat", -1, 0.55, M.combine(nod(1840, 1110, 0.2, 1.8, 2.3), M.bob(2, 2.0, 0.1)))
    beast("goat1", 2000, 1285, "goat", -1, 0.6, M.combine(nod(2000, 1285, 0.7, 1.5, 2.6), M.bob(2, 2.4, 0.4)))
    beast("cow0", 1590, 1062, "cow", 1, 0.5, M.combine(nod(1590, 1062, 0.5, 0.8, 3.6), breathe(1590, 1062, 0.2)))
    beast("cow1", 1150, 1385, "cow", 1, 0.66, M.combine(nod(1150, 1385, 0.1, 0.8, 3.9), breathe(1150, 1385, 0.6)))
    beast("donkey0", 2060, 1100, "donkey", -1, 0.5, M.combine(nod(2060, 1100, 0.4, 1.4, 3.0), breathe(2060, 1100, 0.3)))
    beast("donkey1", 1290, 1110, "donkey", 1, 0.5, M.combine(nod(1290, 1110, 0.8, 1.2, 3.3), breathe(1290, 1110, 0.5)))
    hops = hop_sched(9, T + 1, n=(2,), dur=(0.5, 0.6), rest=(1.0, 1.6))
    person("shepherd", 1940, 1180, "child", 0, facing=-1, frames=[("stand", "happy"), ("cheer", "happy")],
           frame_at=hop_frame(hops), motion=hop_motion(1940, 1180, hops, 14), s=0.56, hops=hops, H=14)

    # one static layer with every grounded figure's long shadow, flattened with the land (render cost)
    sc.add("ground_shadows", shdoc("".join(ground_sh)), z=4.15, wc=0.3)

    # a few more grazing on the lower slope of Jonah's knoll: they fill the bare slope beside the pasture and lead
    # the eye up toward Jonah as the camera rises (their shadows sit on the knoll, above its layer)
    knoll_sh = []
    for (nm, x, y, kind, fc, s_, ph) in [("goat2", 2330, 1215, "goat", 1, 0.6, 0.3),
                                         ("sheep5", 2235, 1380, "sheep", -1, 0.64, 0.6),
                                         ("sheep6", 2450, 1330, "sheep", 1, 0.62, 0.1)]:
        sc.add(nm, doc(PR.animal(x, y, s_, fc, kind=kind)), z=6 + y / 1000, wc=0.6,
               motion=M.combine(nod(x, y, ph, 1.3, 2.8), M.bob(2, 2.3, ph)))
        l, t_, r, b = ABOX[kind]
        knoll_sh.append(long_shadow(x, y, s_, (r - l) * 0.85, (b - t_) * 0.75))
        if fc < 0:
            l, r = -r, -l
        register(nm, (x + l * s_, y + t_ * s_, x + r * s_, y + b * s_), (x + HEAD_DX[kind] * s_ * fc, y + t_ * s_ - 25))
    sc.add("knoll_shadows", shdoc("".join(knoll_sh)), z=5.05, wc=0.3)

    bx, by = 1640 - 0.62 * 112, 1292 - 0.62 * 100
    sc.add("baa", doc(V._baa(bx, by, 0.9)), z=9, wc=0.3, motion=lambda t: Tf(
        alpha=_env(t, t_baa - 0.05, t_baa + 0.1, t_baa + 0.7, t_baa + 1.0),
        sx=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"),
        sy=0.7 + 0.3 * M.progress(t, t_baa - 0.05, t_baa + 0.3, "out"), px=bx, py=by))

    # (no heart for man0: the woman walking to the gate passes right behind him)
    people = {"elder0", "elder1", "father0", "mother0", "girl0", "mother1", "father1", "child_g", "grandpa",
              "mother2", "kid2", "kid3", "toddler", "kid0", "kid1", "kid4", "kid5", "woman0", "man1", "man2",
              "woman1"}
    beasts = {n for n, _, _ in FIGS if n.startswith(("sheep", "lamb", "goat", "cow", "donkey"))} | {"shepherd"}
    q_zone = [("q", (qx - 40, qy - 50, qx + 40, qy + 50)) for qx, qy, _ in q_spots]
    HEARTS["people"] = _place_hearts(people, extra_obstacles=ball_zone + q_zone)
    HEARTS["animals"] = _place_hearts(beasts)
    HEARTS["lr"] = _place_hearts({"lr_b"}, extra_obstacles=ball_zone)
    # lr_a's column above the head is blocked by the family behind him: his heart starts beside his head, on the
    # open side, and rises less
    top_a = next(sp for n, _, sp in FIGS if n == "lr_a")
    HEARTS["lr_a"] = [(top_a[0] - 38, top_a[1] + 30)]

    # =============================================================== WITHERED PLANT + JONAH
    def castor_rot(t):
        """Gentle sway; at rest through the opening dissolve so it lies on s22's plant."""
        k = M.progress(t, t_still - 0.2, t_still + 1.2, "sine")
        return k * (0.6 * math.sin(2 * math.pi * t / 3.6) + 0.25 * math.sin(2 * math.pi * t / 1.7))

    plant = doc(PR.castor_plant(XP, GY, SP, growth=1, wither=1, bite=1, side=1, seed=2))
    sc.add("castor", plant, z=10, wc=0.9, motion=lambda t: Tf(rot=castor_rot(t), px=XP, py=GY))

    # God's golden light on Jonah: on from the start (as s22 leaves him), brighter at his name, fading as
    # the camera pulls back to the city, and back on him as his face softens. It falls from under the veil
    # cloud up to the right (as in s22).
    a_light = lambda t: (0.72 + 0.28 * M.progress(t, t_name - 0.2, t_name + 1.0, "sine")) * \
        (1 - M.progress(t, t_pull0 + 0.4, t_pull0 + 2.2, "sine"))
    a_end = lambda t: 0.6 * M.progress(t, t_soft - 0.3, t_soft + 1.2, "sine")
    beam = doc(
        S.g(f'<path d="M{GAP[0] - 70},{GAP[1]} L{GAP[0] + 70},{GAP[1]} L{XJ + 150},{GY + 30} L{XJ - 230},{GY + 30} Z" '
            f'fill="url(#bm)"/>', filter="blur-md") +
        f'<ellipse cx="{XJ}" cy="{GY - 170}" rx="240" ry="270" fill="url(#jg)"/>',
        S.lin_grad("bm", [(0, "#ffe6a8", 0.22), (0.6, "#ffdc96", 0.12), (1, "#ffd68a", 0.05)]) +
        S.rad_grad("jg", [(0, "#ffe2a0", 0.26), (0.5, "#ffd890", 0.1), (1, "#ffd080", 0)]))
    sc.add("god_light", beam, z=10.5, wc=0, blend="add",
           motion=lambda t: Tf(alpha=max(a_light(t), a_end(t)) * (0.85 + 0.15 * math.sin(t * 2.6))))
    rays = doc(S.g(V._ray_fan(GAP[0], GAP[1] - 30, 700, [96, 103, 110, 117, 124, 131], w0=8, w1=44,
                              fill="#ffe2a0", opacity=0.3), filter="soft"))
    sc.add("rays", rays, z=10.6, wc=0, blend="add", motion=lambda t: Tf(
        alpha=max(a_light(t), 0.8 * a_end(t)) * (0.75 + 0.25 * math.sin(t * 1.9)),
        rot=2.0 * math.sin(t * 0.45), px=GAP[0], py=GAP[1] - 30))

    # Jonah: flipbook of (pose, expression). Every expression change goes through a closed-eye frame (hard
    # cuts: blink -> new face), so two faces are never blended; the pose change is a hard cut hidden by a hop.
    JF = [("sit_sulk", "angry"),      # 0 as s22 leaves him: sulking, arms crossed
          ("sit", "hear_blink"),      # 1
          ("sit", "hear"),            # 2 sitting up, looking up toward the voice and the light
          ("sit", "leaf_blink"),      # 3
          ("sit", "leaf"),            # 4 looking at the dry leaf in his hand
          ("sit", "sorry_blink"),     # 5
          ("sit", "sorry"),           # 6 tender, sorry
          ("sit", "soft_blink"),      # 7
          ("sit", "soft")]            # 8 softened and thoughtful, eyes toward the city
    jshadow = CH.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)

    def jfig(p, e):
        """(markup, head centre in stage px)"""
        mk = CH.jonah(XJ, GY, SP, -1, pose=p, expr=e)
        return mk, CH.body_points(CH.jonah, XJ, GY, SP, -1, pose=p)["head"]

    with _exprs():
        jfigs = [jfig(p, e) for p, e in JF]
    jframes = [doc(jshadow + mk) for mk, _ in jfigs]

    def blinks(t, times, a, b, d=0.13):
        return b if any(tb <= t < tb + d for tb in times) else a

    BL = 0.13                                        # a blink / an expression change through closed eyes
    t_look_leaf = t_fall0 + 0.7                      # a blink, and his eyes follow the leaf down into his hand
    hear_blinks = [b for b in (t_name + 1.15,) if b < t_look_leaf - 0.6]
    leaf_blinks = [t_grow_line + 0.9, t_night1 + 1.25, t_dead + 0.2]
    sorry_blinks = [b for b in (t_tender + 1.9 + 3.3 * k for k in range(8)) if b < t_soft - 0.5]
    soft_blinks = [t_soft + 1.7]

    def jonah_frame(t):
        if t < t_name:
            return 0.0
        if t < t_look_leaf:
            return blinks(t, hear_blinks, 2.0, 1.0)
        if t < t_look_leaf + BL:
            return 1.0
        if t < t_tender:
            return blinks(t, leaf_blinks, 4.0, 3.0)
        if t < t_tender + BL:
            return 5.0
        if t < t_soft:
            return blinks(t, sorry_blinks, 6.0, 5.0)
        if t < t_soft + BL:
            return 7.0
        return blinks(t, soft_blinks, 8.0, 7.0)

    HOP_H, HOP_D = 16, 0.34

    def jonah_tf(t):
        """Rotations are about the seat (XJ, GY), so he stays planted; + = leans back / looks up."""
        s = 1 + 0.011 * math.sin(2 * math.pi * t / 3.2)
        sy = 1.0
        rot = 0.0
        dy = 0.0
        # hears his name: squash, hop (the pose cut hides at take-off), land with a little squash
        u = t - (t_name - 0.08)
        if 0 <= u < 0.08:
            sy *= 1 - 0.05 * math.sin(math.pi * u / 0.16)
        elif 0.08 <= u < 0.08 + HOP_D:
            dy -= HOP_H * math.sin(math.pi * (u - 0.08) / HOP_D)
            sy *= 1.03
        elif 0.08 + HOP_D <= u < 0.08 + HOP_D + 0.14:
            sy *= 1 - 0.04 * math.sin(math.pi * (u - 0.08 - HOP_D) / 0.14)
        # sits up and looks up toward the voice and the light while listening
        rot += 2.6 * _env(t, t_name + 0.1, t_name + 0.7, t_look_leaf - 0.1, t_look_leaf + 0.5)
        # the leaf lands in his hand: a tiny bump
        uc = t - t_catch
        if 0 <= uc < 0.25:
            dy += 3 * math.sin(math.pi * uc / 0.25)
        # bends his head over the leaf, looking at it
        rot -= 2.6 * _env(t, t_look_leaf + 0.1, t_catch + 0.4, t_pull0, t_pull0 + 0.8)
        # a soft sigh at "你都这么心疼它"
        us = t - t_tender
        if 0 <= us < 1.6:
            s *= 1 - 0.012 * math.sin(math.pi * us / 1.6)
        # leans a little toward the city below while God speaks of it, relaxing as his face softens
        rot -= 2.2 * M.progress(t, t_pull0, t_pull0 + 1.0, "sine") * (1 - M.progress(t, t_soft - 0.1, t_soft + 1.0, "sine"))
        # softened: a slow, deep, relaxed breath
        k = M.progress(t, t_soft - 0.1, t_soft + 0.8, "sine")
        s *= 1 + k * 0.008 * math.sin(2 * math.pi * (t - t_soft) / 2.4)
        return Tf(dy=dy, rot=rot, sx=s, sy=s * sy, px=XJ, py=GY)

    sc.add("jonah", jframes, z=11, frame_at=jonah_frame, motion=jonah_tf, wc=0.6)

    def carry(j, p):
        """Where Jonah's transform j carries the stage point p."""
        r = math.radians(j.rot)
        x, y = (p[0] - XJ) * j.sx, (p[1] - GY) * j.sy
        return (XJ + x * math.cos(r) - y * math.sin(r) + j.dx, GY + x * math.sin(r) + y * math.cos(r) + j.dy)

    # --- the dry leaf: hangs from a broken leaf stub on the arching branch just right of his head-cloth (the
    # booth's pale back cloth behind it), wobbles loose, swings out, sweeps left in front of his chest and drops
    # into his open (near) hand from above; he lifts it to look at it and turns it in his fingers
    hand = CH.body_points(CH.jonah, XJ, GY, SP, -1, pose="sit")["hands"][1]
    LCX, LCY = hand[0] - 58, hand[1] - 62
    SE = (hand[0] - 2, hand[1] + 4)                       # stalk end (in the hand)
    leaf = doc(V._dry_leaf(LCX, LCY, 50, rot=-30, col=LEAF_COL, stalk=SE))
    HANG_ROT = HANG_DIR - math.degrees(math.atan2(SE[1] - LCY, SE[0] - LCX))   # turns the stalk up to the stub

    def held_tf(t):
        j = jonah_tf(t)
        hx, hy = carry(j, hand)
        catch = 1 - M.progress(t, t_catch, t_catch + 0.75, "inout")           # caught tipped down, then lifted
        lift = M.progress(t, t_catch + 0.3, t_catch + 1.0, "inout") * (1 - M.progress(t, t_pull0, t_pull0 + 0.8))
        twirl = 5 * math.sin(2 * math.pi * (t - t_grow_line) / 2.3) * _env(t, t_grow_line, t_grow_line + 0.5,
                                                                         t_tender - 0.2, t_tender + 0.4)
        rot = j.rot - 38 * catch + 10 * lift + twirl + 1.5 * math.sin(2 * math.pi * t / 1.3)
        return Tf(dx=hx - hand[0], dy=hy - hand[1] - 8 * lift, rot=rot, sx=j.sx, sy=j.sy, px=hand[0], py=hand[1])

    def map_pt(tf, p):
        """Where Tf (with its pivot) carries the drawing point p."""
        r = math.radians(tf.rot)
        x, y = (p[0] - tf.px) * tf.sx, (p[1] - tf.py) * tf.sy
        return (tf.px + tf.dx + x * math.cos(r) - y * math.sin(r), tf.py + tf.dy + x * math.sin(r) + y * math.cos(r))

    def twig_at(t):
        return _rot_pt(TWIG, (XP, GY), castor_rot(t))

    t_wob = t_fall0 - 0.45

    def hang_tf(t):
        rot = HANG_ROT + castor_rot(t) + 2.5 * math.sin(2 * math.pi * t / 2.1)
        rot += 10 * math.sin(2 * math.pi * (t - t_wob) / 0.22) * _env(t, t_wob, t_wob + 0.08, t_fall0 - 0.08, t_fall0)
        tw = twig_at(t)
        # rotate about the stalk end, which sits on the twig
        return Tf(dx=tw[0] - SE[0], dy=tw[1] - SE[1], rot=rot, px=SE[0], py=SE[1])

    H0 = hang_tf(t_fall0)
    p_start = map_pt(H0, (LCX, LCY))
    HC = held_tf(t_catch)
    p_end = map_pt(HC, (LCX, LCY))
    hx0, hy0 = hand
    path = [p_start,
            (p_start[0] + 24, p_start[1] + 46),          # drops off the stub, swinging out to the right
            (p_start[0] + 6, p_start[1] + 90),           # turns back
            (XJ + 24, hy0 - 78),                         # sweeps left in front of his chest
            (hx0 - 72, hy0 - 112),                       # rises a little at the end of the swing
            (p_end[0] + 6, p_end[1] - 44),               # and drops into his hand from above
            p_end]
    # arc-length table of the Catmull-Rom path, so the leaf's speed follows the easing, not the knot spacing
    samp = [_catmull(path, k / 240) for k in range(241)]
    acc = [0.0]
    for a_, b_ in zip(samp, samp[1:]):
        acc.append(acc[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))

    def path_at(f):
        d = _clamp(f) * acc[-1]
        i = min(239, max(0, next((k for k in range(1, 241) if acc[k] >= d), 240) - 1))
        seg = acc[i + 1] - acc[i]
        v = (d - acc[i]) / seg if seg > 0 else 0.0
        return (samp[i][0] + (samp[i + 1][0] - samp[i][0]) * v, samp[i][1] + (samp[i + 1][1] - samp[i][1]) * v)

    def fall_tf(t):
        u = M.progress(t, t_fall0, t_catch, "linear")
        e = 0.62 * (0.5 - 0.5 * math.cos(math.pi * u)) + 0.38 * u    # starts from rest, slows into his hand
        x, y = path_at(e)
        swing = math.sin(2 * math.pi * 1.25 * u) * (1 - u) * min(1.0, u / 0.1)
        rot = H0.rot + (HC.rot - H0.rot) * (0.5 - 0.5 * math.cos(math.pi * u)) + 28 * swing
        flip = abs(math.cos(math.pi * u * 2.2))
        sy = 1 - 0.5 * (1 - flip) * (1 - u) ** 0.6
        return Tf(dx=x - LCX, dy=y - LCY, rot=rot, sx=HC.sx, sy=HC.sy * sy, px=LCX, py=LCY)

    def leaf_tf(t):
        if t < t_fall0:
            return hang_tf(t)
        if t < t_catch:
            return fall_tf(t)
        return held_tf(t)

    sc.add("leaf", leaf, z=11.2, wc=0.5, motion=leaf_tf)

    # warm light ON Jonah (God's light, and again as his face softens), clipped to his silhouette: a glow on
    # his head and shoulders plus a thin, faint rim on his upper-right edge (toward the light). Two drawings:
    # the sulking pose (until he hears his name) and the sitting pose, cut with Jonah's own pose cut.
    jl_defs = (
        '<filter id="jwhite" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>'
        '<filter id="jblack" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>' +
        S.rad_grad("jl", [(0, "#ffe2a0", 1), (0.55, "#ffdc96", 0.5), (1, "#ffd890", 0)]) +
        S.rad_grad("jr", [(0, "#fff0c8", 1), (0.6, "#ffe6b0", 0.7), (1, "#ffe0a0", 0)]))
    with _exprs():
        J_sil = [CH.jonah(XJ, GY, SP, -1, pose="sit_sulk", expr="angry"), CH.jonah(XJ, GY, SP, -1, pose="sit", expr="sad")]
    jl_docs = []
    for Jm, (_, (hx_, hy_)) in zip(J_sil, (jfigs[0], jfigs[2])):
        masks = (f'<mask id="jsil" maskUnits="userSpaceOnUse" x="0" y="0" width="{SW}" height="{SH}">'
                 f'<g filter="url(#jwhite)">{Jm}</g></mask>'
                 f'<mask id="jrim" maskUnits="userSpaceOnUse" x="0" y="0" width="{SW}" height="{SH}">'
                 f'<g filter="url(#jwhite)">{Jm}</g><g transform="translate(-4,5)" filter="url(#jblack)">{Jm}</g></mask>')
        body = (f'<g mask="url(#jsil)"><ellipse cx="{f1(hx_ + 10)}" cy="{f1(hy_ + 50)}" rx="200" ry="230" '
                f'fill="url(#jl)" opacity="0.42"/></g>'
                f'<g mask="url(#jrim)"><ellipse cx="{f1(hx_ + 50)}" cy="{f1(hy_ - 20)}" rx="250" ry="260" '
                f'fill="url(#jr)" opacity="0.5"/></g>')
        jl_docs.append(doc(body, jl_defs + masks))
    j_light = lambda t: max(a_light(t), a_end(t))
    sc.add("jonah_light", jl_docs, z=11.27, wc=0, blend="add", frame_at=lambda t: 0.0 if t < t_name else 1.0,
           motion=lambda t: (lambda j: Tf(j.dx, j.dy, j.rot, j.sx, j.sy, 0.38 * j_light(t), j.px, j.py))(jonah_tf(t)))

    # =============================================================== THE MEMORY BUBBLE
    outer = _scallop(BC[0], BC[1], BRX, BRY)
    inner = _scallop(BC[0], BC[1], BRX - B_INSET, BRY - B_INSET)
    clip = f'<clipPath id="bubin"><path d="{inner}"/></clipPath>'

    t_bgone = t_bout + 0.3                                     # the shrunken bubble is gone

    def bub_tf(t):
        """A scale pop out of the trail (opaque within 2 frames) and, at the end, a quick shrink back into the
        trail with a 3-frame alpha cut: the bubble's separate layers are never see-through for long."""
        a = M.progress(t, t_bin, t_bin + 0.067, "linear") * (1 - M.progress(t, t_bgone - 0.1, t_bgone, "linear"))
        k = 0.22 + 0.78 * M.progress(t, t_bin, t_bin + 0.4, "back")
        k *= 1 - 0.75 * M.progress(t, t_bout, t_bgone, "in")
        bob = 4 * math.sin(2 * math.pi * (t - t_bin) / 2.7)
        return Tf(dy=bob, sx=k, sy=k, alpha=a, px=BUB_PIV[0], py=BUB_PIV[1])

    def night_amt(t):
        day = _env(t, t_g1 - 0.15, t_g1 + 0.2, t_night2 - 0.05, t_night2 + 0.3)
        return 1 - day

    x0b, y0b = BC[0] - BRX, BC[1] - BRY
    wb, hb_ = 2 * BRX, 2 * BRY
    BSUN = (BC[0] + 215, BPY - 22)       # morning: the sun rises low on the bubble's right (east) horizon
    # night sky with stars
    stars = ""
    srng = random.Random(5)
    for _ in range(16):
        sx_, sy_ = srng.uniform(x0b + 30, x0b + wb - 30), srng.uniform(y0b + 25, BC[1] + 40)
        stars += _star4(sx_, sy_, srng.uniform(4, 8))
    night = doc(f'<g clip-path="url(#bubin)"><rect x="{x0b}" y="{y0b}" width="{wb}" height="{hb_}" fill="url(#bnight)"/>'
                f'{stars}</g>',
                clip + S.lin_grad("bnight", [(0, "#4a5690"), (0.5, "#7a76ac"), (0.8, "#bf98b2"), (1, "#e2b3a6")]))
    day = doc(f'<g clip-path="url(#bubin)"><rect x="{x0b}" y="{y0b}" width="{wb}" height="{hb_}" fill="url(#bday)"/>'
              f'<circle cx="{BSUN[0]}" cy="{BSUN[1]}" r="72" fill="#fff2c0" opacity="0.4"/>'
              f'<circle cx="{BSUN[0]}" cy="{BSUN[1]}" r="32" fill="#fcd877" stroke="#eaa951" stroke-width="3"/></g>',
              clip + S.lin_grad("bday", [(0, "#a9d4e6"), (0.6, "#e8e6c4"), (1, "#fbe2a8")]))
    moon = doc(S.g(f'<path d="M{BC[0] - 150},{BC[1] - 120} a34,34 0 1 0 30,52 a26,26 0 1 1 -30,-52 Z" '
                   f'fill="#fbeec0" stroke="{INK}" stroke-width="3"/>', filter="wobble-fine"))
    ground = (S.path(S.smooth_path([(x0b - 10, BPY + 30), (BC[0] - 190, BPY - 8), (BPX, BPY - 4),
                                    (BC[0] + 120, BPY + 6), (x0b + wb + 10, BPY - 14)], closed=False) +
                     f" L{x0b + wb + 10},{y0b + hb_ + 10} L{x0b - 10},{y0b + hb_ + 10} Z", fill="url(#bgr)", sw=3) +
              PR.booth(BPX + PR.CASTOR_BOOTH_DX * BPS, BPY, BPS, facing=1) +
              PR.grass_tuft(BC[0] - 200, BPY + 10, 0.4, variant=1) + PR.grass_tuft(BC[0] + 210, BPY - 2, 0.35, variant=1))
    gdoc = doc(f'<g clip-path="url(#bubin)">{S.g(ground, filter="wobble-fine")}</g>',
               clip + S.lin_grad("bgr", [(0, "#e4b878"), (1, "#c58f58")]))
    veil = doc(f'<g clip-path="url(#bubin)"><rect x="{x0b}" y="{y0b}" width="{wb}" height="{hb_}" fill="#33407a" '
               f'opacity="0.32"/></g>', clip)
    rim = doc(S.g(f'<path d="{outer} {inner}" fill="#fff6e2" fill-rule="evenodd"/>'
                  f'<path d="{inner}" fill="none" stroke="#d9bf9a" stroke-width="3"/>'
                  f'<path d="{outer}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>',
                  filter="wobble-fine"))
    sc.add("bub_night", night, z=12.0, wc=0.5, motion=bub_tf)
    sc.add("bub_day", day, z=12.05, wc=0.5, motion=lambda t: (lambda b: Tf(
        b.dx, b.dy, b.rot, b.sx, b.sy, b.alpha * (1 - night_amt(t)), b.px, b.py))(bub_tf(t)))

    def moon_tf(t):
        """Each night the moon crosses the top of the bubble from east to west (right to left) and fades out
        at the upper left as morning comes, well away from where the sun rises."""
        b = bub_tf(t)
        if t < t_g1 + 0.3:
            u = M.progress(t, t_bin, t_g1 + 0.2, "linear")
        else:
            u = 0.45 + 0.55 * M.progress(t, t_night2 - 0.1, t_w1 + 0.4, "linear")   # (left of the grown crown)
        cx = BC[0] + 70 - 265 * u
        cy = BC[1] - 150 + 55 * u - 18 * math.sin(math.pi * u)
        mx, my = cx - (BC[0] - 140), cy - (BC[1] - 94)          # the crescent drawing is centred near there
        return Tf(b.dx + mx * b.sx, b.dy + my * b.sy, 0, b.sx, b.sy, b.alpha * night_amt(t), b.px, b.py)
    sc.add("bub_moon", moon, z=12.07, wc=0.4, motion=moon_tf)
    sc.add("bub_ground", gdoc, z=12.1, wc=0.5, motion=bub_tf)

    # the memory castor: a stepped time-lapse, one exact drawing per step
    NG, NW = 12, 10
    states = [dict(growth=k / NG) for k in range(NG + 1)] + [dict(growth=1.0, wither=k / NW) for k in range(1, NW + 1)]
    pframes = [doc(m) for m in _castor_docs(BPX, BPY, BPS, states)]

    def plant_frame(t):
        if t < t_w0:
            return float(round(NG * M.progress(t, t_g0, t_g1, "linear")))
        return float(NG + round(NW * M.progress(t, t_w0, t_w1, "linear")))
    sc.add("bub_plant", pframes, z=12.15, wc=0.5, motion=bub_tf, frame_at=plant_frame)
    sc.add("bub_veil", veil, z=12.2, wc=0, motion=lambda t: (lambda b: Tf(
        b.dx, b.dy, b.rot, b.sx, b.sy, b.alpha * night_amt(t), b.px, b.py))(bub_tf(t)))
    sc.add("bub_rim", rim, z=12.3, wc=0.4, motion=bub_tf)
    # the trail of little puffs from Jonah's head to the bubble
    # (they pop in from his head outward; at the end they pop out from the bubble's end back to his head)
    for i, (tx, ty, tr) in enumerate(TRAIL):
        ti = t_trail + 0.11 * i
        to = t_bgone + 0.02 + 0.09 * (len(TRAIL) - 1 - i)
        pd = doc(S.g(f'<circle cx="{tx}" cy="{ty}" r="{tr}" fill="#fff6e2" stroke="{INK}" stroke-width="3.5"/>',
                     filter="wobble-fine"))
        sc.add(f"bub_trail{i}", pd, z=12.3, wc=0.3, motion=lambda t, ti=ti, to=to, tx=tx, ty=ty, i=i: Tf(
            dy=2.5 * math.sin(2 * math.pi * (t - ti) / 1.9 + i),
            sx=(0.3 + 0.7 * M.progress(t, ti, ti + 0.22, "back")) * (1 - 0.5 * M.progress(t, to - 0.12, to, "in")),
            sy=(0.3 + 0.7 * M.progress(t, ti, ti + 0.22, "back")) * (1 - 0.5 * M.progress(t, to - 0.12, to, "in")),
            alpha=M.progress(t, ti, ti + 0.067, "linear") * (1 - M.progress(t, to - 0.067, to, "linear")),
            px=tx, py=ty))

    # =============================================================== DOVES
    def flock(name, birds, t0, t1, dx, dy, z, fade_in=0.4):
        frames = []
        wings = (-1.0, -0.35, 0.35, 1.0)
        for k in range(4):
            body = ""
            for i, (x, y, sc_) in enumerate(birds):
                body += PR.dove(x, y, sc_, -1, wing=wings[(k + 2 * i) % 4])
            frames.append(doc(body))
        seq = [0, 1, 2, 3, 2, 1]
        sc.add(name, frames, z=z, wc=0.4, frame_at=lambda t: float(seq[int(t * 9) % len(seq)]),
               motion=M.combine(M.keys([(t0, {"dx": 0, "dy": 0}), (t1, {"dx": dx, "dy": dy})], "linear"),
                                M.bob(6, 0.9), lambda t: Tf(alpha=_env(t, t0, t0 + fade_in, t1 - 0.3, t1))))

    flock("doves_a", [(3300, 300, 0.42), (3390, 266, 0.36), (3430, 330, 0.34)], t_pull0 - 0.4, t_down0 + 1.0,
          -2300, -240, 5.4)
    flock("doves_b", [(3250, 300, 0.42), (3340, 260, 0.36), (3390, 335, 0.34)], t_back - 2.2, T + 2.5, -1100, -40,
          5.45)

    # =============================================================== FOREGROUND (static)
    fg = ""
    for (x, y, s, v) in [(3560, 1120, 1.2, 1), (3720, 1090, 1.0, 1), (2620, 1300, 1.0, 1), (3150, 1400, 1.1, 1),
                         (2990, 1190, 0.9, 2), (3300, 1250, 0.8, 1), (3250, 1262, 0.7, 2)]:
        fg += PR.grass_tuft(*kmap(x, y), s, variant=v)
    fg += V._rock(*kmap(3420, 1160), 220, 96, seed=51) + V._rock(*kmap(3700, 1385), 260, 120, seed=52)
    sc.add("fg", doc(S.g(fg)), z=20, wc=0.9)

    # =============================================================== CAMERA
    # (views and key times are set with the narration timing above)
    t_tob = t_bin - 0.3 - max(1.6, _cam_dur([C0b, Cb], 0.5))   # make room for the bubble before it pops
    moves = []
    for (ta, tb, cams, r) in [(t_still, t_tob, [C0, C0b], 0.45),
                              (t_tob, t_bin + 0.3, [C0b, Cb], 0.5),
                              (t_bin + 0.3, t_pull0, [Cb, Cb2], 0.5),
                              (t_pull0, t_pull1, [Cb2, Cw], 0.3),
                              (t_pull1, t_down0, [Cw, Cw2], 0.5),
                              (t_down0, t_down1, [Cw2, C1], 0.32),
                              (t_down1, t_go, [C1, C1b], 0.5),
                              (t_go, t_c2, [C1b, C2], 0.3),          # over to the pasture ...
                              (t_c2, t_rise, [C2, C2h], 0.5),        # ... a slow drift while the animals are named
                              (t_rise, t_back, [C2h, C3], 0.3),      # up the knoll to Jonah
                              (t_back, T - 0.35, [C3, Cf], 0.45)]:   # slow push-in to the last frame
        fn, _, knots = _cam_path(cams)
        moves.append((ta, tb, fn, r, knots))

    def camera(t):
        for (ta, tb, fn, r, _) in moves:
            if t < ta:
                return fn(0.0)
            if t <= tb:
                return fn(_glide((t - ta) / (tb - ta), r))
        return moves[-1][2](1.0)

    sc.camera = camera

    # =============================================================== FX
    sc.fx = [
        FX.sparkles((XJ - 330, GY - 520, XJ + 150, GY - 40), count=22, t0=t_name, t1=t_pull0 + 1.6,
                    color=(255, 238, 175), size=(9, 20), drift=-10, seed=21),
        FX.motes((XJ - 500, 0, XJ + 300, GY), count=30, t0=0.0, t1=t_pull0 + 2.0, color=(255, 244, 205), seed=22),
        FX.sparkles((BC[0] - 220, BC[1] - 150, BC[0] + 220, BC[1] - 10), count=8, t0=t_bin + 0.3, t1=t_g1,
                    color=(255, 244, 200), size=(5, 10), drift=0, period=1.2, seed=25),
        FX.sparkles((BC[0] - 220, BC[1] - 150, BC[0] + 220, BC[1] - 10), count=8, t0=t_night2 + 0.2, t1=t_bout,
                    color=(255, 244, 200), size=(5, 10), drift=0, period=1.2, seed=26),
        FX.sparkles((200, 700, 2300, 1150), count=34, t0=t_city, t1=t_care, color=(255, 238, 175),
                    size=(8, 18), drift=-8, seed=23),
        V.hearts_fx(HEARTS["people"], t_hearts_p0, t_hearts_p1, seed=31),
        V.hearts_fx(HEARTS["lr"], t_lr_end + 0.35, t_hearts_p1 + 0.3, period=3.0, seed=33),
        V.hearts_fx(HEARTS["lr_a"], t_lr_end + 0.5, t_hearts_p1 + 0.3, rise=40, period=3.0, seed=34),
        V.hearts_fx(HEARTS["animals"], t_hearts_a0, t_hearts_a1, life=2.4, seed=32),
        FX.sparkles((XJ - 300, GY - 420, XJ + 150, GY - 60), count=16, t0=t_soft, t1=T + 1, color=(255, 240, 190),
                    size=(8, 16), drift=-6, seed=24),
    ]

    # =============================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("birds", 0, dur=T + 0.6, gain_db=-18, fade_in=0.8, fade_out=0.8, pan=-0.2)
    sc.sfx("pop", t_bin, gain_db=-15, pan=-0.3)
    sc.sfx("grow", t_g0, gain_db=-15, pan=-0.3)
    sc.sfx("wither", t_w0, gain_db=-15, pan=-0.3)
    sc.sfx("crowd", t_city - 0.5, dur=t_back - t_city + 0.5, gain_db=-24, fade_in=1.0, fade_out=1.2, pan=-0.1)
    sc.sfx("pop", t_q0, gain_db=-17, pan=-0.2)
    sc.sfx("sheep", t_baa, gain_db=-11, pan=-0.2)
    sc.sfx("chime", t_soft, gain_db=-11)
    return sc
