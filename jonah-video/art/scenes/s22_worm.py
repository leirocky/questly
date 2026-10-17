"""Scene 22 — the worm, the sun and the hot east wind (Jonah 4:7-9).

The same dry hillside east of Nineveh as the v1 vine scene (art/scenes_v1/s11_vine.py, whose layout, land,
props and drawing helpers are reused): the city small on the western horizon (left), Jonah in his little
booth facing it, the full-grown castor plant arching over the booth roof.

Line 0  "第二天天刚亮，" — the scene opens in the cool lilac of the last minutes of night (crescent moon, twinkling
        stars, Jonah asleep sitting up, little z's rising); dawn breaks: the sky blushes pink, the sun's rim
        peeks over the eastern hills (right), the stars fade, two doves fly out toward the sunrise.
        "上帝又安排了一条小虫子。" — a small golden glimmer by the pebble at the foot of the stem (God's doing, light
        only) and the little worm inches out from behind it (two planted inchworm steps) while the camera
        pushes in to the stem.
        "小虫子咬了蓖麻，蓖麻就枯死了。" — chomp, chomp (crumbs fly, the notch deepens, the plant leans); then the plant
        withers as ONE continuous drawing (v1 per-frame flipbook, never two plants blended), dry leaves drop
        and Jonah wakes with a start (hop) and turns sad. The camera pulls back slowly through the wither.
Line 1  "太阳出来以后，" — the sun climbs from the eastern hills high over the booth, grows and blazes (flame rays,
        hot ochre sky); the worm turns and creeps back behind its pebble to hide from the heat.
        "上帝安排了又热又干的东风。" — the hot east wind arrives from the right: wind swirls, blowing sand, dead leaves
        torn off and whirled toward the city, grass and plant bending, the lizard runs for the shade; Jonah
        squints and rocks in the gusts.
        "太阳晒在约拿的头上，约拿热极了，" — hot sunbeams slant from the sun onto Jonah's head (light streaks travel
        down them, a hot spot on his head-cloth), he pants and sweats; on "热极了" he slumps back on one hand
        fanning himself (hop), sweat drops fly, heat waves rise from his head.
        "头都发昏了，又难过又生气。" — spiral eyes, little stars orbit his head, he wobbles; "又难过" head bowed
        (hop); "又生气" arms crossed, angry, steam puffs and an anger mark (hop).
Line 2  "上帝又问约拿：" — the wind drops; a soft cloud drifts over the blazing sun (its flame rays fade) and the
        harsh light turns a gentle gold: a slow glory of pale rays behind the cloud, soft golden shafts fanning
        down from under it onto Jonah (a warm glow clipped to his silhouette), sparkles and motes; he looks up,
        grumpy, listening (hop). God is shown only as this light.
Line 3  (God) "约拿，你因为这棵蓖麻生气，对吗？" — the light breathes gently; on "这棵蓖麻" a soft glow and sparkles
        settle on the withered plant and Jonah's eyes go to it; on "对吗" he looks up again (blinks while
        listening).
Line 4  (Jonah) "对！我就是生气！" — he bounces up on his seat with both fists in the air, shouting (big hop, dust,
        pop lines); stamps on "我就是生气"; "我气极了！" — arms crossed, chin up, eyes shut (hop + stamp) with two
        grumpy puffs of steam and an anger mark. He then sits sulking and huffing more and more quietly in the
        golden light (calm last second for the dissolve into God's answer, s23).

Notes for maintainers
* Every time comes from the narration: ctx.lines[i].start / .at(phrase), or _at(line, phrase) for a phrase
  INSIDE a subtitle chunk (chunk start + the share of the chunk's characters before the phrase, punctuation
  counting as a short pause) - never fixed numbers.
* Pose changes are hard cuts hidden by a squash-and-hop (+ dust poof / pop lines); only expression changes of
  the SAME pose crossfade (adjacent flipbook frames). Blinks are 4-frame cuts.
* The castor bite / wither is one exact drawing per video frame (v1 technique, via V._castor_svgs) and the
  flipbook index is always whole, so two different plants are never blended.
* Pre-dawn grade: the land (everything in front of the sky) gets a cool blue-lilac multiply through a land
  silhouette mask, the sky a gentler one (v1 night technique); the plant does not sway while the mask is on.
* Light layers (sunbeam, God's shafts) sit BEHIND the plant and Jonah so they stay crisp; only small, clipped
  or local glows (hot spot on his head-cloth, glow on his silhouette, glow on the plant at "这棵蓖麻") are on top.
* Closures read build()-level names at call time: never reuse a name that a motion function reads (the swirl
  loop once overwrote the sunbeam's length).
* Camera: few long sine-eased moves: drift, push-in to the stem for the worm, one long pull-back through the
  wither and the sunrise, a slow push toward Jonah in the heat, a gentle pull-back for God's light, a small
  push for the shout; the viewport always stays inside the painted 2112 x 1188 stage (max pan ~90 output
  px/s, max zoom ~20 %/s).
"""
import math
import random
from contextlib import contextmanager

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s11_vine as V
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine.motion import Cam, Tf
from engine.paths import FPS
from engine.scene import BOIL_TOKEN, Scene

INK = P["ink"]

# ------------------------------------------------------------------ layout (same as v1 s11_vine)
GY, SP, XP, XB, XJ = V.GY, V.SP, V.XP, V.XB, V.XJ
SW, XW, NOTCH, HORIZON, LIZ = V.SW, V.XW, V.NOTCH, V.HORIZON, V.LIZ
SUN_E = (1830, 604)       # dawn: the sun's rim just over the eastern hills (crest y~570 there)
SUN_HOT = (1490, 225)     # blazing sun, high over the booth
CX, CY = W // 2, H // 2   # centre-drawn layers (suns, pop lines) are moved into place by their motion
MOON = (330, 300)
VEIL = (1500, 274)        # the soft cloud that drifts over the sun when God speaks
GAP = (1340, 364)         # God's light fans down from under its lower-left edge

_env, _clamp = V._env, V._clamp
_PUNCT = "，。！？：；、,.!?:;…"


def _at(line, phrase):
    """Start (s from scene start) of ``phrase`` inside one subtitle chunk of ``line``: the chunk start plus
    the share of the chunk's speaking time taken by the text before it (characters weigh 1, punctuation 1.5
    for its pause; the chunk's closing punctuation is not spoken)."""
    def wt(s):
        return sum(1.5 if ch in _PUNCT else 1.0 for ch in s)
    for c in line.chunks:
        i = c.text.find(phrase)
        if i < 0:
            continue
        tot = wt(c.text.rstrip(_PUNCT))
        return c.start + (c.end - c.start) * (wt(c.text[:i]) / tot if tot > 0 else 0.0)
    return line.at(phrase)


# ------------------------------------------------------------------ Jonah: poses and expressions
_EXTRA_EXPRS = {
    "doze": dict(eyes="closed", brow=(-0.02, 0.02, 0.03), mouth="small_o"),
    "squint": dict(eyes="droop", brow=(0.07, -0.03, 0.03), mouth="flat"),
    "sob": dict(eyes="down", brow=(-0.12, 0.06, 0.02), mouth="frown"),
    "lookup": dict(eyes="dot", brow=(0.09, -0.04, 0.02), mouth="grumpy", look=(0.02, -0.1)),
    "lookup_blink": dict(eyes="closed", brow=(0.09, -0.04, 0.02), mouth="grumpy"),
    "lookplant": dict(eyes="dot", brow=(-0.07, 0.04, 0.0), mouth="frown", look=(0.08, 0.08)),
    "ashout": dict(eyes="dot", brow=(0.13, -0.06, 0.03), mouth="shout", blush=True),
    "hmph": dict(eyes="closed", brow=(0.12, -0.05, 0.04), mouth="grumpy", blush=True),
}


@contextmanager
def _exprs():
    added = [k for k in _EXTRA_EXPRS if k not in C.EXPRS]
    for k in added:
        C.EXPRS[k] = _EXTRA_EXPRS[k]
    try:
        yield
    finally:
        for k in added:
            C.EXPRS.pop(k, None)


_SEAT = dict(C._SEATED)
_KNEES = (("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1))
_CROSS = (("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1))
POSE = {
    "doze": C._P(t=2, h=18, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=_KNEES, **_SEAT),
    "sit": dict(C.POSES["sit"]),
    "faint": dict(C.POSES["sit_faint"]),
    "gloom": C._P(t=6, h=26, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=_KNEES, **_SEAT),
    "sulk": dict(C.POSES["sit_sulk"]),
    "sulk_up": C._P(t=-4, h=-12, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True, **_SEAT),
    # "对！": bounces up on his seat with both fists in the air; "我气极了！": arms crossed, chin up
    "shout": C._P(t=4, h=-14, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=(("fk", 140, 165), ("fk", -140, -165)),
                  hands=("fist", "fist"), **_SEAT),
    "hmph": C._P(t=-5, h=-20, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True, **_SEAT),
}
# flipbook order: expression changes of one pose are ADJACENT frames (they may crossfade)
JP = [("doze", "doze"),            # 0 asleep, sitting up
      ("sit", "surprised"),        # 1 woken by the falling leaves
      ("sit", "sad"),              # 2 his plant is dead
      ("sit", "squint"),           # 3 squinting into the hot wind
      ("sit", "tired"),            # 4 the sun beats on his head (panting, sweat)
      ("faint", "tired"),          # 5 "热极了": slumped back on one hand, fanning
      ("faint", "dizzy"),          # 6 "头都发昏了"
      ("gloom", "sob"),            # 7 "又难过": head bowed
      ("sulk", "angry"),           # 8 "又生气": arms crossed
      ("sulk_up", "lookup"),       # 9 listening to God, grumpy
      ("sulk_up", "lookplant"),    # 10 "这棵蓖麻": eyes on the plant
      ("sulk_up", "lookup_blink"),  # 11 blink
      ("shout", "ashout"),         # 12 "对！我就是生气！"
      ("hmph", "hmph")]            # 13 "我气极了！"
F_LOOK, F_BLINK = 9, 11


def jonah_fig(ps, expr, x=XJ, y=GY, scale=SP, facing=-1, marks=True):
    """Jonah (characters.jonah's design) in a scene-local pose record -> (markup, points in stage px)."""
    with _exprs():
        inner, _ = C._figure(C._jonah_design(), C._ADULT, dict(ps), expr, C._fsign(facing), marks)
    L = C._LAST
    sx = scale * (1 if facing >= 0 else -1)

    def stp(p):
        return (x + p[0] * sx, y + p[1] * scale)
    pts = {"head": stp(L["head"]), "head_top": stp(L["head_top"])}
    return C._wrap_out(inner, x, y, scale, facing, f"jonah22-{ps.get('t')}-{expr}"), pts


# ------------------------------------------------------------------ small drawings
def _ray_fan(cx, cy, length, angles, w0=10, w1=90, fill="#ffe9b5", opacity=0.5):
    """Soft light shafts fanning from (cx, cy); angles in degrees (90 = straight down). (v1 s12)"""
    d = ""
    for i, a in enumerate(angles):
        r = math.radians(a)
        ux, uy = math.cos(r), math.sin(r)
        nx, ny = -uy, ux
        ln = length * (0.85 + 0.15 * math.sin(i * 2.3))
        ww = w1 * (0.7 + 0.3 * math.cos(i * 1.7))
        p = [(cx + nx * w0, cy + ny * w0), (cx + ux * ln + nx * ww, cy + uy * ln + ny * ww),
             (cx + ux * ln - nx * ww, cy + uy * ln - ny * ww), (cx - nx * w0, cy - ny * w0)]
        d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in p) + " Z "
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def _heat_wave(cx, cy, n=3, h=70, col="#fff3d6"):
    """Little wavy heat lines rising (drawn around (cx, cy), bottom at cy)."""
    out = ""
    for j in range(n):
        x0 = cx + (j - (n - 1) / 2) * 26
        pts = [(x0 + 7 * math.sin(q * 1.15 + j), cy - q * h / 8) for q in range(9)]
        d = S.smooth_path(pts, closed=False)
        out += (f'<path d="{d}" fill="none" stroke="{P["ink_soft"]}" stroke-width="9" stroke-linecap="round" '
                f'opacity="0.35"/><path d="{d}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def _pop_lines(cx, cy, r0=96, r1=132, n=5, a0=-160, step=35, w=7):
    out = ""
    for k in range(n):
        a = math.radians(a0 + k * step)
        out += (f'<path d="M{cx + r0 * math.cos(a):.1f},{cy + r0 * math.sin(a):.1f} '
                f'L{cx + r1 * math.cos(a):.1f},{cy + r1 * math.sin(a):.1f}" stroke="{P["ink_soft"]}" '
                f'stroke-width="{w}" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def _dust_poof(x, y, k=1.0):
    """Two little dust clouds at the sides of (x, y) (v1 pose-change poof)."""
    out = ""
    for bx, sgn in ((x - 178 * k, -1), (x + 168 * k, 1)):
        circ = [(0, 0, 17), (sgn * 20, -6, 13), (-sgn * 16, -4, 12), (sgn * 4, -16, 12)]
        out += "".join(f'<circle cx="{bx + dx * k:.1f}" cy="{y - 6 + dy * k:.1f}" r="{r * k:.1f}" fill="#f3e4c4" '
                       f'stroke="{P["ink_soft"]}" stroke-width="6"/>' for dx, dy, r in circ)
        out += "".join(f'<circle cx="{bx + dx * k:.1f}" cy="{y - 6 + dy * k:.1f}" r="{r * k:.1f}" fill="#f3e4c4"/>'
                       for dx, dy, r in circ)
    return S.g(out, filter="wobble-fine")


FLAT_DEFS = V.FLAT_DEFS


# ------------------------------------------------------------------ scene
def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines
    L0, L1, L2, L3, L4 = L[0], L[1], L[2], L[3], L[4]

    # =============================================================== key times (from the narration)
    t_dawn0 = L0.at("天刚亮")                          # "第二天天刚亮"
    t_dawn1 = t_dawn0 + 1.7                            # dawn colours complete
    t_godw = L0.at("安排了一条")                        # "上帝又安排了一条小虫子。"
    t_worm0 = t_godw + 0.45                            # the worm inches out from behind the pebble
    t_worm1 = t_worm0 + 1.6
    t_bite0 = _at(L0, "咬了") - 0.15                    # "小虫子咬了蓖麻"
    t_bite1 = t_bite0 + 1.35                           # the notch is complete
    t_with0 = _at(L0, "蓖麻就枯死")                      # "蓖麻就枯死了"
    t_with1 = t_with0 + 1.9
    t_chomp1 = t_with0 + 0.25
    t_wake = t_with0 + 0.62                            # leaves drop round him: he wakes with a start
    t_sad0 = t_wake + 0.95
    t_sun0 = L1.at("太阳出来")                          # "太阳出来以后"
    t_sun1 = t_sun0 + 1.6                              # the sun stands high and blazes
    t_wormx = t_sun0 + 0.5                             # the worm turns and creeps back behind its pebble
    t_wind = _at(L1, "又热又干") - 0.3                   # "上帝安排了又热又干的东风"
    t_liz = t_wind + 1.0                               # the lizard runs for the shade
    t_beam = L1.at("晒在") + 0.05                       # "太阳晒在约拿的头上"
    t_tired = t_beam + 0.55
    t_hot = _at(L1, "约拿热极了")                        # "约拿热极了"
    t_dizzy = L1.at("发昏")                             # "头都发昏了"
    t_sad = _at(L1, "又难过")                           # "又难过"
    t_ang = _at(L1, "又生气")                           # "又生气"
    t_calm0 = L2.start - 0.45                          # wind drops, the light turns gentle and golden
    t_light0 = L2.start                                # "上帝又问约拿："
    t_listen = L2.start + 0.55                         # Jonah looks up toward the light
    t_plant = _at(L3, "这棵蓖麻")                       # "这棵蓖麻"
    t_plant_back = _at(L3, "对吗")                      # "对吗？"
    t_shout = L4.start                                 # "对！"
    t_stamp = _at(L4, "我就是") + 0.25                 # stamps on "我就是生气！"
    t_hmph = L4.at("我气极了")                          # "我气极了！"

    def a_gold(t):
        return M.progress(t, t_calm0, t_light0 + 1.4, "sine")

    def wind(t):
        return M.progress(t, t_wind - 0.3, t_wind + 0.5, "sine") * (1 - 0.8 * a_gold(t))

    # =============================================================== SKY
    sky_h = 665
    a_dawn = lambda t: M.progress(t, t_dawn0, t_dawn1, "sine")
    a_hot = lambda t: M.progress(t, t_sun0 + 0.1, t_sun1 + 0.3, "sine")

    stars = ""
    rng = np.random.default_rng(22)
    for i in range(46):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, 470)
        if math.hypot(x - MOON[0], y - MOON[1]) < 120:
            continue
        stars += V._star(x, y, rng.uniform(3, 7.5), "#fbf0c8", sw=0)
    moon = (f'<path d="M{MOON[0]},{MOON[1] - 52} A52,52 0 1 1 {MOON[0]},{MOON[1] + 52} '
            f'A40,52 0 1 0 {MOON[0]},{MOON[1] - 52} Z" fill="#fbf1cf" stroke="{INK}" stroke-width="3"/>')
    sky_pre = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="760" ry="250" fill="url(#r)"/>' + stars +
        f'<circle cx="{MOON[0] - 12}" cy="{MOON[1]}" r="160" fill="url(#mh)"/>' + S.g(moon, filter="wobble-fine"),
        defs=S.lin_grad("g", [(0, "#46507e"), (0.5, "#6f6c9c"), (0.85, "#b49ab4"), (1, "#d6b1b4")]) +
        S.rad_grad("r", [(0, "#f2c2a8", 0.75), (0.55, "#d9a6b0", 0.3), (1, "#b49ab4", 0)]) +
        S.rad_grad("mh", [(0, "#fbf1cf", 0.42), (0.3, "#f3ead0", 0.2), (0.65, "#c9c9dc", 0.06), (1, "#a9aecb", 0)]))
    sc.add("sky_pre", sky_pre, wc=0.4, motion=lambda t: Tf(alpha=0.0 if a_dawn(t) >= 0.999 else 1.0))

    sky_dawn = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="980" ry="380" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#a9b4dc"), (0.42, "#e6c3cf"), (0.8, "#f8d6aa"), (1, "#f9ddb0")]) +
        S.rad_grad("r", [(0, "#fff0c4", 0.95), (0.45, "#fcd3a0", 0.5), (1, "#f6c7a0", 0)]))
    sc.add("sky_dawn", sky_dawn, wc=0.5,
           motion=lambda t: Tf(alpha=0.0 if a_hot(t) >= 0.999 else a_dawn(t)))

    sky_hot = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="900" fill="url(#r)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="420" fill="url(#c)"/>',
        defs=S.lin_grad("g", [(0, "#f0bf62"), (0.5, "#f6d488"), (1, "#fae0a6")]) +
        S.rad_grad("r", [(0, "#fffbe6", 1), (0.25, "#fff1bf", 0.8), (0.6, "#fbd98c", 0.25), (1, "#f6c46a", 0)]) +
        S.rad_grad("c", [(0, "#fffef6", 1), (0.3, "#fff8dc", 0.9), (0.62, "#fff0b8", 0.4), (1, "#ffe9a6", 0)]))
    sc.add("sky_hot", sky_hot, wc=0.5, motion=lambda t: Tf(alpha=0.0 if a_gold(t) >= 0.999 else a_hot(t)))

    # gentle golden sky for God's question: softer and calmer, a warm glow round the veiled sun
    sky_gold = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<circle cx="{SUN_HOT[0]}" cy="{SUN_HOT[1]}" r="620" fill="url(#c)"/>'
        f'<ellipse cx="{GAP[0] - 200}" cy="{GAP[1] + 260}" rx="760" ry="330" fill="url(#r)"/>',
        defs=S.lin_grad("g", [(0, "#e5a64c"), (0.5, "#f1cd86"), (1, "#f7e0ae")]) +
        S.rad_grad("r", [(0, "#fffaea", 0.95), (0.4, "#fff3cf", 0.55), (1, "#ffeab8", 0)]) +
        S.rad_grad("c", [(0, "#fffcf0", 0.9), (0.4, "#fff4d0", 0.5), (1, "#ffefc0", 0)]))
    sc.add("sky_gold", sky_gold, wc=0.5, motion=lambda t: Tf(alpha=a_gold(t)))

    # --- suns (drawn at the document centre, moved into place) ------------------------------------
    def at(pos, m=None):
        base = lambda t: Tf(dx=pos[0] - CX, dy=pos[1] - CY)
        return M.combine(base, m) if m else base

    def sun_svg(r, col, glow, glow_r):
        return S.svg_doc(
            f'<circle cx="{CX}" cy="{CY}" r="{glow_r}" fill="url(#sg)"/>' +
            S.g(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{col}" stroke="{S.shade(col, -0.25)}" stroke-width="4"/>'
                f'<circle cx="{CX - r * 0.3:.0f}" cy="{CY - r * 0.3:.0f}" r="{r * 0.35:.0f}" fill="#fffaf0" '
                f'opacity="0.35"/>', filter="wobble"),
            defs=S.rad_grad("sg", [(0, glow, 0.85), (0.35, glow, 0.35), (1, glow, 0)]))

    S_HOT = 118 / 82
    climb = M.keys([(t_dawn0 - 0.2, {"dx": 0, "dy": 64}), (t_dawn1 + 0.4, {"dx": 0, "dy": 0}),
                    (t_sun0, {"dx": -14, "dy": -30}),
                    (t_sun1, {"dx": SUN_HOT[0] - SUN_E[0], "dy": SUN_HOT[1] - SUN_E[1], "s": S_HOT})],
                   ["out", "linear", "inout"], pivot=(CX, CY))
    sc.add("sun_dawn", sun_svg(82, "#f8c070", "#ffe0b0", 330),
           motion=at(SUN_E, M.combine(climb, lambda t: Tf(alpha=1 - M.progress(t, t_sun1 - 0.05, t_sun1 + 0.3,
                                                                               "sine")))))
    # blazing noon sun: flame rays (turning) behind a bright disc (v1)
    hx, hy = CX, CY
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
        left = [(hx + r * ca - (off - w_) * sa, hy + r * sa + (off - w_) * ca) for r, off, w_ in pts]
        right = [(hx + r * ca - (off + w_) * sa, hy + r * sa + (off + w_) * ca) for r, off, w_ in pts]
        ray_d += S.smooth_path(left + right[::-1], closed=True, tension=0.8) + " "
    short = S.rays(hx, hy, 120, 215, n=14, width_deg=11, rot=12.9)
    rays = S.svg_doc(S.g(
        f'<path d="{short}" fill="#ffd34d" stroke="#b9621c" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="{ray_d}" fill="#ffb83a" stroke="#b9621c" stroke-width="4.5" stroke-linejoin="round"/>',
        filter="wobble"))
    sc.add("sun_rays", rays, wc=0.3,
           motion=at(SUN_HOT, M.combine(lambda t: Tf(rot=12 * t - 5 * a_gold(t) * (t - t_calm0), px=hx, py=hy),
                                        M.breathe(0.03, 0.9, pivot=(hx, hy)),
                                        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.05, t_sun1 + 0.45, "sine") *
                                                     (1 - a_gold(t))))))
    hot = S.svg_doc(
        f'<circle cx="{hx}" cy="{hy}" r="185" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{hx}" cy="{hy}" r="118" fill="#ffd94f" stroke="#c9741f" stroke-width="6"/>'
            f'<circle cx="{hx}" cy="{hy}" r="90" fill="#fff1a8"/>'
            f'<circle cx="{hx}" cy="{hy}" r="58" fill="#fffae0"/>'
            f'<circle cx="{hx - 34}" cy="{hy - 34}" r="26" fill="#fffef6" opacity="0.9"/>', filter="wobble"),
        defs=S.rad_grad("hg", [(0, "#fffef4", 1), (0.6, "#fff6cf", 0.85), (0.8, "#ffeaa0", 0.4), (1, "#ffe08a", 0)]))
    sc.add("sun_hot", hot, wc=0.4, motion=at(SUN_HOT, M.combine(
        M.breathe(0.035, 1.3, pivot=(hx, hy)),
        lambda t: Tf(alpha=M.progress(t, t_sun1 - 0.1, t_sun1 + 0.3, "sine")))))

    # --- clouds: pink-lit at dawn, burnt away as the sun climbs ------------------------------------
    clouds = S.svg_doc(S.g(
        S.cloud(700, 150, 290, 88, "#fdf3e4", seed=3, sw=3, shade_fill="#efcdd0") +
        S.cloud(1640, 290, 240, 76, "#fdf1e2", seed=5, sw=3, shade_fill="#efcdd0") +
        S.cloud(1870, 118, 300, 92, "#fdf3e4", seed=8, sw=3, shade_fill="#efcdd0") +
        S.cloud(700, 330, 170, 56, "#fdf1e2", seed=9, sw=3, shade_fill="#efcdd0"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=M.combine(
        M.drift(vx=-7), lambda t: Tf(alpha=(0.55 + 0.45 * a_dawn(t)) *
                                     (1 - M.progress(t, t_sun0 - 0.3, t_sun0 + 1.0, "sine")))))

    # a soft golden-edged cloud drifts over the blazing sun as God speaks; behind it a gentle glory of pale
    # light shafts turns slowly (warm light only - never a figure)
    glory = S.svg_doc(S.g(f'<path d="{S.rays(CX, CY, 150, 700, n=14, width_deg=10)}" fill="#fffbe8"/>',
                          filter="soft") +
                      f'<circle cx="{CX}" cy="{CY}" r="330" fill="url(#gg)"/>',
                      defs=S.rad_grad("gg", [(0, "#fffbea", 0.95), (0.5, "#fff2c8", 0.5), (1, "#ffe9b0", 0)]))
    sc.add("glory", glory, wc=0, motion=at(VEIL, M.combine(
        lambda t: Tf(rot=4 * t, px=CX, py=CY),
        lambda t: Tf(alpha=0.8 * M.progress(t, t_light0 - 0.2, t_light0 + 1.6, "sine") *
                     (0.85 + 0.15 * math.sin(t * 1.7)))), ))
    veil = S.svg_doc(
        f'<ellipse cx="{VEIL[0]}" cy="{VEIL[1] - 10}" rx="400" ry="210" fill="url(#vg)"/>' +
        S.g(S.cloud(VEIL[0], VEIL[1] - 4, 610, 214, "#fff2b8", seed=12, sw=0), filter="blur-md") +
        S.g(S.cloud(VEIL[0], VEIL[1], 520, 170, "#fff6e2", seed=12, sw=3.5, shade_fill="#f8d596"),
            filter="wobble"),
        defs=S.rad_grad("vg", [(0, "#fff8dc", 1.0), (0.45, "#ffe9a8", 0.6), (1, "#ffdc90", 0)]))
    sc.add("veil", veil, wc=0.6, motion=M.combine(
        lambda t: Tf(dx=820 * (1 - M.progress(t, t_calm0 - 0.3, t_light0 + 0.8, "out")),
                     alpha=M.progress(t, t_calm0 - 0.3, t_calm0 + 0.2)),
        M.combine(M.bob(5, 4.2), lambda t: Tf(dx=-4 * max(0.0, t - t_light0)))))

    # =============================================================== LAND (static, flattened; v1 drawing)
    far = ""
    far += S.path(S.smooth_path([(-80, HORIZON + 8), (150, 600), (420, 585), (700, 610), (950, 590),
                                 (1250, 560), (1550, 585), (1850, 570), (2200, 600)], closed=False) +
                  f" L{W + 80},{HORIZON + 30} L-80,{HORIZON + 30} Z", fill="#e3d3c0", sw=3)
    far += S.path(S.smooth_path([(1000, HORIZON + 6), (1300, 612), (1600, 598), (1900, 615), (2200, 605)],
                                closed=False) + f" L{W + 80},{HORIZON + 30} L1000,{HORIZON + 30} Z", fill="#dfcbb0", sw=3)
    far_svg = S.svg_doc(S.g(far, filter="wobble"))
    sc.add("far_hills", far_svg, wc=0.7)

    city_svg = S.svg_doc(PR.nineveh_skyline(20, 560, HORIZON + 4, scale=0.42, seed=2, haze=0.42, tint="#efdcbc"))
    sc.add("city", city_svg, wc=0.6)

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
    plain_svg = S.svg_doc(S.g(plain, filter="wobble"), defs=defs)
    sc.add("plain", plain_svg, wc=0.8)

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
    mid_svg = S.svg_doc(mid)
    sc.add("mid", mid_svg, wc=0.8)

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

    fg = ""
    fg += V._rock(150, 1160, 290, 130, seed=31) + V._rock(360, 1180, 160, 72, seed=32)
    fg += V._rock(1960, 1165, 250, 115, seed=33) + V._rock(1790, 1185, 140, 64, seed=34)
    fg += V._stone(40, 925, 150, 84, seed=35, sw=4) + PR.bush(92, 912, 1.2, variant=2)
    fg += PR.bush(2072, 1062, 1.05, variant=2)
    sc.add("fg_rocks", S.svg_doc(S.g(fg, filter="wobble")), wc=0.9)
    sc.add("liz_rock", S.svg_doc(S.g(V._stone(LIZ[0] - 4, 994, 138, 50, seed=41, sw=4, crack=True),
                                     filter="wobble-fine")), wc=0.8)

    # =============================================================== DOVES fly out toward the sunrise
    dove_frames = [S.svg_doc(PR.dove(-120, 330, 0.6, 1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    for i, (t0, dy, ph) in enumerate([(t_dawn0 + 0.35, 0, 0), (t_dawn0 + 0.7, -70, 2)]):
        dur = 3.2
        sc.add(f"dove{i}", dove_frames, frame_at=flap(11, ph), wc=0.4, motion=M.combine(
            M.keys([(t0, {"dx": 0, "dy": dy + 40}), (t0 + dur, {"dx": 2350, "dy": dy - 70})], "linear"),
            M.bob(10, 0.6, ph * 0.1),
            lambda t, t0=t0, dur=dur: Tf(alpha=1.0 if t0 <= t <= t0 + dur else 0.0)))

    # =============================================================== LIZARD (basks, runs from the hot wind)
    liz_frames = [S.svg_doc(V._lizard(LIZ[0], LIZ[1], 0.72, legs=k)) for k in (0, 1)]

    def liz_frame(t):
        return 0.0 if t < t_liz else float(int((t - t_liz) * 16) % 2)

    def liz_motion(t):
        if t < t_liz:
            u = (t + 0.9) % 2.8
            b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
            return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)
        v = t - t_liz
        return Tf(dx=158 * M.ease("out")(min(1.0, v / 0.5)), dy=38 * M.progress(v, 0.08, 0.4, "sine"),
                  alpha=1 - M.progress(v, 0.4, 0.62, "sine"))

    sc.add("lizard", liz_frames, frame_at=liz_frame, motion=liz_motion, wc=0.5)
    sc.add("liz_rock2", S.svg_doc(S.g(V._stone(LIZ[0] + 150, 1002, 104, 58, seed=43, sw=4), filter="wobble-fine")),
           wc=0.8)

    # booth + its contact shadow
    booth_svg = S.svg_doc(f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{INK}" '
                          f'opacity="0.16" filter="url(#soft)"/>' + PR.booth(XB, GY, SP, facing=1))
    sc.add("booth", booth_svg, wc=0.8)

    # canopy shade on the ground (morning light), gone as the plant withers
    shade_amt = lambda t: (0.35 + 0.65 * a_dawn(t)) * (1 - M.progress(t, t_with0 + 0.2, t_with1, "sine"))
    sc.add("ground_shade", S.svg_doc(f'<ellipse cx="{XP + 330}" cy="{GY + 8}" rx="560" ry="40" fill="#8f7c8a" '
                                     f'opacity="0.55" filter="url(#soft)"/>'),
           wc=0, blend="multiply", motion=lambda t: Tf(alpha=shade_amt(t)))

    # =============================================================== God appoints the worm: a small glimmer
    gx, gy = XW - 150, GY - 30
    glim = S.svg_doc(f'<ellipse cx="{gx}" cy="{gy}" rx="190" ry="120" fill="url(#gl)"/>',
                     defs=S.rad_grad("gl", [(0, "#fff4c8", 0.95), (0.45, "#ffe9a6", 0.45), (1, "#ffe08a", 0)]))
    sc.add("worm_glow", glim, wc=0, blend="add",
           motion=lambda t: Tf(alpha=0.75 * _env(t, t_godw - 0.1, t_godw + 0.5, t_worm1 - 0.3, t_worm1 + 0.6) *
                               (0.85 + 0.15 * math.sin(t * 5))))

    # Jonah's drawings (needed early: the light layers behind the plant aim at his head)
    jshadow = C.ground_shadow(XJ, GY, SP, width=210, opacity=0.25)
    jdocs, jpts = [], []
    for p, e in JP:
        mk, pts = jonah_fig(POSE[p], e)
        jdocs.append(S.svg_doc(jshadow + mk))
        jpts.append(pts)
    # =============================================================== SUN ON HIS HEAD (behind him; a hot spot on top)
    bx0, by0 = SUN_HOT
    ht_sit, ht_faint = jpts[4]["head_top"], jpts[5]["head_top"]
    tx, ty = ht_sit[0] + 6, ht_sit[1] + 16
    b_ang = math.atan2(ty - by0, tx - bx0)
    b_len = math.hypot(tx - bx0, ty - by0)
    ux, uy = math.cos(b_ang), math.sin(b_ang)
    nx, ny = -uy, ux
    beam_d = ""
    for k, (off, w0, w1) in enumerate([(-70, 14, 46), (0, 22, 80), (70, 14, 46)]):
        ox, oy = nx * off * 0.3, ny * off * 0.3
        ex, ey = tx + nx * off, ty + ny * off
        beam_d += (f"M{bx0 + ox + nx * w0:.1f},{by0 + oy + ny * w0:.1f} L{ex + nx * w1:.1f},{ey + ny * w1:.1f} "
                   f"L{ex - nx * w1:.1f},{ey - ny * w1:.1f} L{bx0 + ox - nx * w0:.1f},{by0 + oy - ny * w0:.1f} Z ")
    beam = S.svg_doc(
        S.g(f'<path d="{beam_d}" fill="url(#bm)"/>', filter="soft") +
        f'<ellipse cx="{tx}" cy="{ty + 30}" rx="190" ry="150" fill="url(#hs)"/>',
        defs=(f'<linearGradient id="bm" gradientUnits="userSpaceOnUse" x1="{bx0}" y1="{by0}" x2="{tx:.0f}" '
              f'y2="{ty:.0f}"><stop offset="0" stop-color="#fff2b0" stop-opacity="0"/>'
              f'<stop offset="0.3" stop-color="#ffe48a" stop-opacity="0.35"/>'
              f'<stop offset="1" stop-color="#ffd26a" stop-opacity="0.7"/></linearGradient>') +
        S.rad_grad("hs", [(0, "#fff0b0", 0.85), (0.5, "#ffd77a", 0.4), (1, "#ffc860", 0)]))
    # aimed at his head in the faint pose after "热极了" (rotate / stretch about the sun)
    tx2, ty2 = ht_faint[0] + 6, ht_faint[1] + 16
    b_ang2 = math.atan2(ty2 - by0, tx2 - bx0)
    b_len2 = math.hypot(tx2 - bx0, ty2 - by0)
    a_beam = lambda t: _env(t, t_beam - 0.1, t_beam + 0.5, t_calm0, t_light0 + 0.9)

    def beam_aim(t):
        return M.progress(t, t_hot - 0.05, t_hot + 0.15, "sine")

    def beam_motion(t):
        k = beam_aim(t)
        return Tf(rot=math.degrees(b_ang2 - b_ang) * k, sx=1 + (b_len2 / b_len - 1) * k, sy=1 + (b_len2 / b_len - 1) * k,
                  px=bx0, py=by0, alpha=a_beam(t) * (0.8 + 0.2 * math.sin(2 * math.pi * t / 0.7)))

    sc.add("sunbeam", beam, wc=0, blend="add", motion=beam_motion)

    # =============================================================== GOD'S GENTLE LIGHT (never a figure)
    # soft shafts fan down from under the cloud that veils the sun, onto Jonah and the withered plant
    a_light = lambda t: M.progress(t, t_light0 + 0.1, t_light0 + 1.5, "sine")
    shafts = S.svg_doc(
        S.g(_ray_fan(GAP[0], GAP[1], 820, [100, 108, 116, 124, 132, 140], w0=12, w1=70, fill="url(#sh)",
                     opacity=0.5), filter="blur-md") +
        f'<ellipse cx="{XJ - 30}" cy="{GY - 210}" rx="300" ry="270" fill="url(#jg)"/>',
        defs=S.rad_grad("jg", [(0, "#ffe6a8", 0.3), (0.5, "#ffdc96", 0.12), (1, "#ffd68a", 0)]) +
        f'<linearGradient id="sh" gradientUnits="userSpaceOnUse" x1="0" y1="{GAP[1]}" x2="0" y2="{GY + 80}">'
        f'<stop offset="0" stop-color="#fff0c0" stop-opacity="0.95"/>'
        f'<stop offset="0.6" stop-color="#ffe6ac" stop-opacity="0.75"/>'
        f'<stop offset="1" stop-color="#ffe0a0" stop-opacity="0.1"/></linearGradient>')
    sc.add("god_light", shafts, wc=0, blend="add",
           motion=lambda t: Tf(alpha=a_light(t) * (0.82 + 0.18 * math.sin(t * 2.2)),
                               rot=1.5 * math.sin(t * 0.45), px=GAP[0], py=GAP[1]))

    # =============================================================== CASTOR PLANT (one exact drawing per frame)
    def per_frame(t0, t1, curve):
        k0 = math.floor(t0 * FPS)
        return k0, [M.progress(k / FPS, t0, t1, curve) for k in range(k0, math.ceil(t1 * FPS) + 1)]

    kb, b_vals = per_frame(t_bite0, t_bite1, "linear")
    kw, w_vals = per_frame(t_with0, t_with1, "sine")
    states = ([dict(growth=1.0)] + [dict(growth=1.0, bite=b) for b in b_vals] +
              [dict(growth=1.0, bite=1.0, wither=w) for w in w_vals])
    plant_frames, plant_ids, seen = [], [], {}
    for svg in V._castor_svgs(states):
        if svg not in seen:
            seen[svg] = len(plant_frames)
            plant_frames.append(svg)
        plant_ids.append(seen[svg])
    NB = len(b_vals)
    plant_full = plant_frames[plant_ids[0]]
    phases = [(kb, plant_ids[1:1 + NB]), (kw, plant_ids[1 + NB:])]

    def plant_frame(t):
        if t < t_bite0:
            return float(plant_ids[0])
        k0, ids = phases[0 if t < t_with0 else 1]
        return float(ids[min(max(round(t * FPS) - k0, 0), len(ids) - 1)])

    def plant_motion(t):
        calm = 0.7 * math.sin(2 * math.pi * t / 3.4) * M.progress(t, t_dawn0 + 0.6, t_dawn1 + 0.6, "sine")
        w = wind(t)
        gust = -2.0 + 1.4 * math.sin(2 * math.pi * t / 0.95) + 0.5 * math.sin(t * 9.1)
        return Tf(rot=calm * (1 - w) + w * gust, px=XP, py=GY)

    sc.add("castor", plant_frames, frame_at=plant_frame, motion=plant_motion, wc=0.9)

    # the plant glows softly as God names it ("这棵蓖麻")
    pglow = S.svg_doc(f'<ellipse cx="{XP + 120}" cy="{GY - 330}" rx="380" ry="420" fill="url(#pg)"/>',
                      defs=S.rad_grad("pg", [(0, "#fff0c0", 0.55), (0.55, "#ffe3a0", 0.25), (1, "#ffd890", 0)]))
    sc.add("plant_glow", pglow, wc=0, blend="add",
           motion=lambda t: Tf(alpha=0.8 * _env(t, t_plant - 0.15, t_plant + 0.5, t_plant_back + 0.3,
                                                t_plant_back + 1.2) * (0.85 + 0.15 * math.sin(t * 3.1))))

    # --- hot east wind swirls (behind Jonah, in bands clear of his head) ---------------------------
    for i, (y, sw_len, ph) in enumerate([(470, 360, 0.0), (880, 320, 0.45), (300, 260, 0.8), (600, 230, 1.15)]):
        sw_svg = S.svg_doc(S.g(V._swirl(1700, y, sw_len), filter="wobble-fine"))

        def swirl_motion(t, ph=ph):
            if t < t_wind - 0.2:
                return Tf(alpha=0.0)
            u = ((t - t_wind + 0.2 + ph) % 1.6) / 1.6
            a = math.sin(math.pi * u) * M.progress(t, t_wind - 0.2, t_wind + 0.3) * (1 - a_gold(t))
            return Tf(dx=500 - 1500 * u, dy=12 * math.sin(6 * u), alpha=0.9 * a)

        sc.add(f"swirl{i}", sw_svg, motion=swirl_motion, wc=0.2)

    # =============================================================== JONAH
    # (time, frame, kind, hop strength, pop lines, dust poof); fades only between adjacent frames
    EV = [(t_wake, 1, "cut", 1.0, True, True),
          (t_sad0, 2, "fade", 0.3, False, False),
          (t_wind + 0.25, 3, "fade", 0.3, False, False),
          (t_tired, 4, "fade", 0.35, False, False),
          (t_hot, 5, "cut", 0.75, False, True),
          (t_dizzy + 0.05, 6, "fade", 0.25, False, False),
          (t_sad, 7, "cut", 0.6, False, False),
          (t_ang, 8, "cut", 1.0, True, True),
          (t_listen, 9, "cut", 0.7, True, False),
          (t_plant + 0.1, 10, "fade", 0.3, False, False),
          (t_plant_back, 9, "fade", 0.3, False, False),
          (t_shout, 12, "cut", 1.4, True, True),
          (t_hmph, 13, "cut", 0.8, True, True)]
    prev = 0
    for ev in EV:
        assert ev[2] != "fade" or abs(ev[1] - prev) == 1, ev
        prev = ev[1]
    blinks = [t_listen + 1.7, t_plant - 0.9, t_plant_back + 0.9]

    def jonah_frame(t):
        f, prev = 0.0, 0
        for ts, idx, kind, d, *_ in EV:
            if t < ts:
                break
            if kind == "fade" and t < ts + d:
                f = prev + (idx - prev) * M.progress(t, ts, ts + d, "sine")
            else:
                f = float(idx)
            prev = idx
        if f == F_LOOK and any(b <= t < b + 0.13 for b in blinks):
            f = float(F_BLINK)
        return f

    cuts = [(ts, amp) for ts, idx, kind, amp, *_ in EV if kind == "cut"]

    def hop(t):
        """Squash (before the cut) -> stretch + little hop (after it) -> settle, ~0.26 s (v1)."""
        sy, dy = 1.0, 0.0
        for ts, amp in cuts:
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

    stamps = [t_stamp, t_hmph + 0.32]

    def jonah_motion(t):
        asleep = t < t_wake
        per, amp = (3.6, 0.016) if asleep else (3.0, 0.012)
        if t >= t_shout:                       # huffing after the shout, calming down
            k = 1 - M.progress(t, t_hmph + 0.5, T - 0.6, "sine")
            per, amp = 1.4 + 1.4 * (1 - k), 0.012 + 0.012 * k
        s = 1 + amp * math.sin(2 * math.pi * t / per)
        sx, sy = s, s
        rot, dx, dy = 0.0, 0.0, 0.0
        # rocked by the gusts while he squints into the hot wind
        g = _env(t, t_wind, t_wind + 0.7, t_hot - 0.3, t_hot)
        rot += g * (1.1 * math.sin(2 * math.pi * t / 1.25) + 0.4 * math.sin(t * 7.3))
        # dizzy wobble
        k = _env(t, t_dizzy, t_dizzy + 0.5, t_sad - 0.25, t_sad)
        rot += k * 2.6 * math.sin(2 * math.pi * (t - t_dizzy) / 1.6)
        # sobbing shoulders ("又难过")
        u = t - t_sad
        if 0.2 <= u < t_ang - t_sad:
            sy *= 1 - 0.012 * abs(math.sin(u * 9))
        # angry trembling ("又生气", "对！")
        for ta, d in ((t_ang + 0.12, 0.8), (t_shout + 0.15, 0.6)):
            u = t - ta
            if 0 <= u < d:
                dx += 3.0 * math.sin(u * 62) * (1 - u / d)
        # stamps: a quick dip and pop
        for ts in stamps:
            u = t - ts
            if 0 <= u < 0.3:
                dy += 9 * math.sin(math.pi * u / 0.3)
                sy *= 1 - 0.025 * math.sin(math.pi * u / 0.3)
        hsy, hdy = hop(t)
        sy *= hsy
        sx *= 1 + 0.5 * (1 - hsy)
        return Tf(dx=dx, dy=dy + hdy, rot=rot, sx=sx, sy=sy, px=XJ, py=GY)

    sc.add("jonah", jdocs, frame_at=jonah_frame, motion=jonah_motion, wc=0.6)

    # canopy shade ON JONAH ONLY (cool flat copy of his silhouette, multiplied; only the early poses need it)
    blank = S.svg_doc("")
    tint_frames = [S.svg_doc(S.g(jonah_fig(POSE[p], e)[0], filter="flat"), defs=FLAT_DEFS) if i <= 2 else blank
                   for i, (p, e) in enumerate(JP)]
    sc.add("jonah_shade", tint_frames, frame_at=jonah_frame, wc=0, blend="multiply",
           motion=M.combine(jonah_motion, lambda t: Tf(alpha=0.42 * shade_amt(t) if t < t_with1 + 0.1 else 0.0)))

    # God's warm light ON Jonah (from "上帝又问约拿"): a glow on his head and shoulders plus a thin rim on his
    # upper-right edge (toward the light), both clipped to his silhouette; same flipbook + motion as Jonah (v1 s12)
    jl_frames = []
    for i, (p, e) in enumerate(JP):
        if i < F_LOOK:
            jl_frames.append(blank)
            continue
        J = jonah_fig(POSE[p], e)[0]
        hx_, hy_ = jpts[i]["head"]
        jl_defs = (
            '<filter id="jwhite" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>'
            '<filter id="jblack" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>'
            f'<mask id="jsil" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<g filter="url(#jwhite)">{J}</g></mask>'
            f'<mask id="jrim" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<g filter="url(#jwhite)">{J}</g><g transform="translate(-9,11)" filter="url(#jblack)">{J}</g></mask>' +
            S.rad_grad("jl", [(0, "#ffe2a0", 1), (0.55, "#ffdc96", 0.5), (1, "#ffd890", 0)]) +
            S.rad_grad("jr", [(0, "#fff0c8", 1), (0.6, "#ffe6b0", 0.7), (1, "#ffe0a0", 0)]))
        jl_body = (f'<g mask="url(#jsil)"><ellipse cx="{hx_ + 10:.1f}" cy="{hy_ + 50:.1f}" rx="200" ry="230" '
                   f'fill="url(#jl)" opacity="0.42"/></g>'
                   f'<g mask="url(#jrim)"><ellipse cx="{hx_ + 50:.1f}" cy="{hy_ - 20:.1f}" rx="250" ry="260" '
                   f'fill="url(#jr)"/></g>')
        jl_frames.append(S.svg_doc(jl_body, defs=jl_defs))
    sc.add("jonah_light", jl_frames, frame_at=jonah_frame, wc=0, blend="add",
           motion=M.combine(jonah_motion, lambda t: Tf(alpha=0.38 * a_light(t) if jonah_frame(t) >= F_LOOK else 0.0)))

    # the hot spot where the sun beats on his head-cloth
    hs_svg = S.svg_doc(f'<ellipse cx="{CX}" cy="{CY}" rx="80" ry="46" fill="url(#hh)"/>',
                       defs=S.rad_grad("hh", [(0, "#fff6c8", 0.95), (0.5, "#ffe08a", 0.45), (1, "#ffd070", 0)]))
    sc.add("hotspot", hs_svg, wc=0, blend="add", motion=lambda t: Tf(
        dx=tx + (tx2 - tx) * beam_aim(t) - CX, dy=ty + 6 + (ty2 - ty) * beam_aim(t) - CY,
        alpha=0.75 * a_beam(t) * (0.75 + 0.25 * math.sin(2 * math.pi * t / 0.7)) *
        (1 - M.progress(t, t_sad - 0.1, t_sad + 0.1)), px=CX, py=CY))

    # --- sleeping z's (rise from his nodding head until he wakes) ------------------------------------
    zx, zy = jpts[0]["head"]
    zx, zy = zx - 70, zy - 40
    for i in range(3):
        zsvg = S.svg_doc(S.g(C._zglyph(CX, CY, 46, w=8.5, col=P["ink"]) +
                             C._zglyph(CX, CY, 46, w=3.4, col="#fbf4e6"), filter="wobble-fine"))

        def zmo(t, i=i):
            if t >= t_wake + 0.15:
                return Tf(alpha=0.0)
            u = ((t / 2.4) + i / 3) % 1.0
            s = 0.55 + 0.6 * u
            a = math.sin(math.pi * u) ** 0.8 * (1 - M.progress(t, t_wake - 0.25, t_wake + 0.1))
            return Tf(dx=zx - CX - 90 * u - 14 * math.sin(u * 6), dy=zy - CY - 130 * u, sx=s, sy=s, alpha=a,
                      px=CX, py=CY)

        sc.add(f"z{i}", zsvg, motion=zmo, wc=0.2)

    # --- pose-change pops: dust poofs at his sides + emphasis lines round his head -------------------
    dust_ts = [ts for ts, idx, kind, amp, lines, dust in EV if kind == "cut" and dust] + stamps
    sc.add("jpop_dust", S.svg_doc(_dust_poof(XJ, GY)), wc=0.3, motion=lambda t: next(
        (Tf(dy=-6 * M.ease("out")(min(1, (t - ts) / 0.45)), sx=0.5 + 0.7 * M.ease("out")(min(1, (t - ts) / 0.45)),
            sy=0.5 + 0.7 * M.ease("out")(min(1, (t - ts) / 0.45)),
            alpha=0.9 * (1 - M.progress(t - ts, 0.12, 0.45, "sine")), px=XJ, py=GY)
         for ts in dust_ts if 0 <= t - ts < 0.45), Tf(alpha=0.0)))
    pop_pts = [(ts, jpts[idx]["head"]) for ts, idx, kind, amp, lines, dust in EV if lines]
    big = {t_shout, t_hmph}
    sc.add("jpop_lines", S.svg_doc(_pop_lines(CX, CY)), wc=0.2, motion=lambda t: next(
        (Tf(dx=hp[0] - CX, dy=hp[1] - CY, sx=(0.82 + 0.3 * M.ease("out")(min(1, (t - ts) / 0.34))) * (1.25 if ts in big else 1),
            sy=(0.82 + 0.3 * M.ease("out")(min(1, (t - ts) / 0.34))) * (1.25 if ts in big else 1),
            alpha=1 - M.progress(t - ts, 0.12, 0.34, "sine"), px=CX, py=CY)
         for ts, hp in pop_pts if 0 <= t - ts < 0.34), Tf(alpha=0.0)))

    # --- grumpy steam puffs + anger mark ("又生气", "我气极了") -----------------------------------------
    def huff_layers(name, head, times, r=27, spread=(96, 94), mark=22):
        hx0, hy0 = head
        for side_, (ox, oy) in enumerate([(-spread[0], 4), (spread[1], 12)]):
            cx, cy = hx0 + ox, hy0 + oy
            sgn = -1 if side_ == 0 else 1

            def puff_motion(t, cx=cx, cy=cy, sgn=sgn, ph=side_ * 0.07):
                for th in times:
                    u = t - th - ph
                    if 0 <= u < 0.8:
                        a = min(1.0, u / 0.05) * (1 - M.progress(u, 0.4, 0.8, "sine"))
                        s = 0.3 + 0.8 * M.ease("out")(u / 0.12) if u < 0.12 else \
                            1.1 - 0.1 * M.progress(u, 0.12, 0.3, "sine")
                        e = M.ease("out")(min(1.0, u / 0.8))
                        return Tf(dx=sgn * 26 * e, dy=-46 * e, sx=s, sy=s, alpha=a, px=cx, py=cy)
                return Tf(alpha=0.0)

            sc.add(f"{name}_puff{side_}", S.svg_doc(V._puff(cx, cy, r)), motion=puff_motion, wc=0.3)
        ax, ay = hx0 + 56, hy0 - 60

        def anger_motion(t):
            for th in times:
                u = t - th + 0.04
                if 0 <= u < 0.95:
                    s = 1.25 * M.ease("out")(u / 0.1) if u < 0.1 else \
                        1.25 - 0.25 * M.progress(u, 0.1, 0.24, "sine") + 0.06 * math.sin(u * 30) * (1 - u)
                    return Tf(sx=s, sy=s, alpha=1 - M.progress(u, 0.65, 0.95, "sine"), px=ax, py=ay)
            return Tf(alpha=0.0)

        sc.add(f"{name}_anger", S.svg_doc(V._anger(ax, ay, mark)), motion=anger_motion, wc=0.2)

    huff_layers("sulk", jpts[8]["head"], [t_ang + 0.08, t_ang + 0.95])
    huff_layers("hmph", jpts[13]["head"], [t_hmph + 0.05, t_hmph + 0.5], r=32, mark=26)

    # =============================================================== WORM (v1 inchworm steps + chomp)
    worm_frames = [S.svg_doc(PR.worm(XW, GY + 2, SW, 1, crawl=c, chomp=ch))
                   for c, ch in [(1.0, 0), (0.5, 0), (0, 0), (0, 0.5), (0, 1.0)]]
    worm_frames += [S.svg_doc(PR.worm(XW, GY + 2, SW, -1, crawl=c)) for c in (1.0, 0.5, 0.0)]   # 5..7 going home
    NCYC, STRIDE = 2, 75.0
    X_START = -NCYC * STRIDE
    t_wx1 = t_wormx + 1.5

    def worm_state(t):
        if t < t_worm0:
            return 2.0, X_START
        if t < t_worm1:
            v = (t - t_worm0) / (t_worm1 - t_worm0) * NCYC
            k, u = int(v), v - int(v)
            return float((1, 0, 1, 2)[min(3, int(u * 4))]), X_START + STRIDE * (k + M.progress(u, 0.6, 1.0, "sine"))
        if t < t_bite0:
            return 2.0, 0.0
        back = -7.0 * M.progress(t, t_bite0 - 0.1, t_bite0 + 0.05, "sine")
        if t < t_chomp1:
            frame = (2, 3, 4, 3)[int((t - t_bite0) * 6.0) % 4]
            return float(frame), back + (2.5 if frame == 4 else 0.0)
        if t < t_wormx:
            return 2.0, -7.0 * (1 - M.progress(t, t_chomp1, t_chomp1 + 0.3, "sine"))
        # turns round (cut hidden by a tiny hop) and inches back behind its pebble, away from the sun
        v = min(0.999, (t - t_wormx) / (t_wx1 - t_wormx)) * NCYC
        k, u = int(v), v - int(v)
        return float(5 + (1, 0, 1, 2)[min(3, int(u * 4))]), -STRIDE * (k + M.progress(u, 0.6, 1.0, "sine"))

    def worm_motion(t):
        _f, dx = worm_state(t)
        dy = 0.0
        if t_chomp1 + 0.3 < t < t_wormx:
            dy = -3 * abs(math.sin(t * 6)) * M.progress(t, t_chomp1 + 0.3, t_chomp1 + 0.6)
        if t_worm1 + 0.1 < t < t_bite0 - 0.15:     # wiggles, looking up at the big stem
            dy = -4 * abs(math.sin((t - t_worm1) * 7))
        u = t - t_wormx
        if 0 <= u < 0.2:
            dy -= 10 * math.sin(math.pi * u / 0.2)
        a = M.progress(t, t_worm0, t_worm0 + 0.2, "sine") * (1 - M.progress(t, t_wx1 - 0.35, t_wx1, "sine"))
        return Tf(dx=dx, dy=dy, alpha=a)

    sc.add("worm", worm_frames, frame_at=lambda t: worm_state(t)[0], motion=worm_motion, wc=0.5)
    sc.add("pebble", S.svg_doc(S.g(V._rock(XW + X_START - 40, GY + 16, 130, 62, seed=21, sw=4),
                                   filter="wobble-fine")), wc=0.8)

    # crumbs nibbled out of the notch (a little spray each time the mouth opens; v1)
    CR_K = 3
    cbx0, cby0 = int(NOTCH[0] - 150), int(NOTCH[1] - 80)
    cw, ch = 230, int(GY + 24 - cby0)
    crumbs = []
    nb = int((t_chomp1 - t_bite0) * 6.0 / 4) + 1
    for c in range(nb):
        tc = t_bite0 + (4 * c + 2) / 6.0
        if tc > t_chomp1:
            break
        for j in range(3):
            rnd = random.Random(100 + c * 10 + j)
            vx, vy = rnd.uniform(-25, 85), rnd.uniform(150, 230)
            g_ = 1100.0
            drop = GY + 3 - NOTCH[1]
            u_land = (vy + math.sqrt(vy * vy + 2 * g_ * drop)) / g_
            crumbs.append((tc + j * 0.05, vx, vy, g_, u_land, rnd.uniform(3.6, 6.0),
                           ("#f4eecb", "#9ccc6a", "#6ea84b")[j % 3]))

    def crumb_fn(t):
        if t < t_bite0 + 0.2 or t > t_chomp1 + 1.6:
            return None
        im = Image.new("RGBA", (cw * CR_K, ch * CR_K), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        any_ = False
        for t0, vx, vy, g_, ul, r, col in crumbs:
            u = t - t0
            if u < 0 or u > ul + 0.9:
                continue
            uu = min(u, ul)
            x = NOTCH[0] - 4 + vx * uu
            y = NOTCH[1] - vy * uu + 0.5 * g_ * uu * uu
            a = 1 - M.progress(u, ul + 0.4, ul + 0.9)
            if a <= 0.02:
                continue
            any_ = True
            px_, py_ = (x - cbx0) * CR_K, (y - cby0) * CR_K
            rr = r * CR_K
            ia = int(255 * a)
            d.ellipse([px_ - rr - 5, py_ - rr * 0.8 - 5, px_ + rr + 5, py_ + rr * 0.8 + 5], fill=(75, 52, 38, ia))
            rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
            d.ellipse([px_ - rr, py_ - rr * 0.8, px_ + rr, py_ + rr * 0.8], fill=(*rgb, ia))
        if not any_:
            return None
        return im.resize((cw, ch), Image.LANCZOS), (cbx0, cby0)

    sc.add_dynamic("crumbs", crumb_fn)

    # =============================================================== HEAT on his head
    h_sit = jpts[4]["head"]
    h_faint = jpts[5]["head"]

    # heat waves rising off his head-cloth ("热极了")
    hw_svg = S.svg_doc(_heat_wave(CX, CY))
    for i in range(2):
        def hw_motion(t, i=i):
            k = _env(t, t_hot + 0.1, t_hot + 0.4, t_sad - 0.2, t_sad)
            if k <= 0:
                return Tf(alpha=0.0)
            u = ((t - t_hot) / 1.1 + i * 0.5) % 1.0
            hp = h_faint if t < t_dizzy else jpts[6]["head"]
            return Tf(dx=hp[0] - CX + (i * 2 - 1) * 26, dy=hp[1] - 70 - CY - 50 * u,
                      alpha=k * math.sin(math.pi * u), px=CX, py=CY)
        sc.add(f"heatwave{i}", hw_svg, motion=hw_motion, wc=0.2)

    # sweat drops flicked off his head while he is hot
    drop_svg = S.svg_doc(S.g(C._drop(CX, CY, 9), filter="wobble-fine"))
    for i in range(4):
        def drop_motion(t, i=i):
            k = _env(t, t_tired + 0.3, t_tired + 0.5, t_dizzy + 0.6, t_dizzy + 0.8)
            if k <= 0:
                return Tf(alpha=0.0)
            per = 0.9
            u = ((t - t_tired) / per + i * 0.27) % 1.0
            hp = h_sit if t < t_hot else h_faint
            sgn = 1 if i % 2 == 0 else -1
            vx = sgn * (110 + 30 * (i // 2))
            x = hp[0] + sgn * 50 + vx * u
            y = hp[1] - 30 - 260 * u + 520 * u * u
            return Tf(dx=x - CX, dy=y - CY, rot=sgn * 40 * u, alpha=k * (1 - M.progress(u, 0.65, 1.0)),
                      px=CX, py=CY)
        sc.add(f"sweat{i}", drop_svg, motion=drop_motion, wc=0.2)

    # dizzy stars orbiting his head
    ftop = jpts[6]["head_top"]
    ocx, ocy = ftop[0] + 4, ftop[1] - 26
    for i in range(3):
        def orbit(t, ph=i / 3):
            a = 2 * math.pi * (t * 0.9 + ph)
            k = _env(t, t_dizzy + 0.15, t_dizzy + 0.6, t_sad - 0.25, t_sad - 0.02)
            s = 0.85 + 0.2 * math.sin(a)
            return Tf(dx=80 * math.cos(a), dy=20 * math.sin(a), sx=s, sy=s, alpha=k, px=ocx, py=ocy)
        sc.add(f"dizzy{i}", S.svg_doc(S.g(V._star(ocx, ocy, 22, "#ffd84a", sw=4), filter="wobble-fine")),
               motion=orbit, wc=0.3)

    # =============================================================== FOREGROUND grass (sways; bends in the wind)
    def grass_frame_fn(ph):
        def f(t):
            w = wind(t)
            calm = 1 + 0.7 * math.sin(2 * math.pi * (t / 2.6 + ph))
            gust = 2.4 + 0.6 * math.sin(2 * math.pi * (t / 0.8 + ph))
            return calm * (1 - w) + gust * w
        return f

    for gi, tufts in enumerate([[(40, 1115, 1.15, 1), (265, 1105, 0.95, 1), (450, 1160, 1.0, 0)],
                                [(1720, 1140, 1.0, 1), (1870, 1108, 0.95, 1)],
                                [(560, 1000, 0.65, 1), (196, 928, 0.8, 1)],
                                [(1520, 990, 0.65, 1), (1700, 985, 0.6, 1)]]):
        frames = [S.svg_doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts))
                  for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", frames, frame_at=grass_frame_fn(gi * 0.23), wc=0.7)

    # --- withered leaves: three drop round Jonah (and wake him), then the wind whirls them off ----------
    for i, (lx, ly, land_dx, tdrop) in enumerate([(XP + 250, GY - 560, -70, 0.05), (XP + 100, GY - 420, -60, 0.35),
                                                   (XP + 560, GY - 520, 50, 0.2)]):
        col = [P["leaf_dry"], "#a7834a", P["leaf_dead"]][i]
        leaf = S.svg_doc(V._dead_leaf(lx, ly, 28, col, curl=0.2 * i))
        tf0 = t_with0 + tdrop
        tb0 = t_wind + 0.05 + 0.3 * i
        fall_y = GY - 10 - ly

        def drop_leaf(t, tf0=tf0, tb0=tb0, i=i, land_dx=land_dx, fall_y=fall_y):
            if t < tf0:
                return Tf(alpha=0.0)
            u = min(1.0, (t - tf0) / 1.5)
            k = M.ease("in")(u) * 0.6 + 0.4 * u
            dx = land_dx * u + 40 * math.sin(u * 7 + i) * (1 - u)
            dy = fall_y * k
            rot = 90 * u + 35 * math.sin(u * 8 + i) * (1 - u)
            a = min(1.0, (t - tf0) / 0.15)
            if t > tb0:
                v = t - tb0
                dx += -900 * v - 150 * v * v
                dy += -60 * math.sin(min(v, 1.2) * 2.6) - 30 * v
                rot += -300 * v
                a *= 1 - M.progress(v, 1.8, 2.3)
            return Tf(dx=dx, dy=dy, rot=rot, alpha=a)

        sc.add(f"drop{i}", leaf, motion=drop_leaf, wc=0.5)

    n_leaves = 10
    for i in range(n_leaves):
        col = [P["leaf_dead"], P["leaf_dry"], "#a7834a"][i % 3]
        sx0, sy0 = XP + 160 + (i * 97) % 420, GY - 640 + (i * 61) % 260
        leaf = S.svg_doc(V._dead_leaf(sx0, sy0, 26 + (i % 3) * 5, col, curl=0.25 * (i % 2)))
        tl0 = t_wind + 0.1 + i * (t_ang - t_wind - 0.6) / n_leaves

        def leaf_motion(t, tl0=tl0, i=i, sx0=sx0, sy0=sy0):
            u = t - tl0
            if u < 0 or u > 2.6:
                return Tf(alpha=0.0)
            dx = -850 * u - 120 * u * u
            dy = 150 * u + 45 * math.sin(u * 5 + i)
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 2.2, 2.6))
            return Tf(dx=dx, dy=dy, rot=-260 * u * (1 + 0.2 * (i % 2)), alpha=a, px=sx0, py=sy0)

        sc.add(f"leaf{i}", leaf, motion=leaf_motion, wc=0.5)

    # =============================================================== CAMERA
    # drift -> push in to the stem for the worm -> one long pull-back through the wither and the sunrise ->
    # slow push toward Jonah in the heat -> gentle pull-back for God's light -> small push for the shout
    t_push0, t_push1 = t_godw - 0.4, t_worm1 + 0.6
    t_pull0, t_pull1 = t_bite1 + 0.1, t_sun1 + 0.35
    sc.camera = M.cam_keys([
        (0.0, Cam(1070, 600, 1990)),
        (t_push0, Cam(1062, 606, 1960)),
        (t_push1, Cam(985, 728, 1340)),
        (t_pull0, Cam(990, 724, 1324)),
        (t_pull1, Cam(1110, 592, 1960)),
        (t_beam - 0.1, Cam(1114, 594, 1940)),
        (t_dizzy + 0.6, Cam(1190, 640, 1580)),
        (t_light0 - 0.1, Cam(1194, 644, 1560)),
        (L3.start + 0.3, Cam(1110, 604, 1840)),
        (t_shout - 0.35, Cam(1118, 608, 1810)),
        (t_shout + 0.95, Cam(1160, 626, 1700)),
        (T, Cam(1166, 628, 1684)),
    ], "sine")

    # =============================================================== FX
    _nm = {}
    mask_svgs = [far_svg, city_svg, plain_svg, mid_svg, booth_svg, plant_full]

    def land_mask():
        """Stage-space alpha of everything standing in front of the sky (same SVGs as the layers, so the
        raster cache is hit). Built on first use."""
        if "m" not in _nm:
            acc = None
            for svg in mask_svgs:
                im = raster.rasterize(svg.replace(BOIL_TOKEN, "1"), W, H)
                a = np.asarray(im.getchannel("A"), np.float32) / 255.0
                acc = a if acc is None else np.maximum(acc, a)
            _nm["m"] = cv2.GaussianBlur(acc, (0, 0), 1.0)
        return _nm["m"]

    t_pre1 = t_dawn0 + 1.3

    def grade(frame, t, view):
        mul = np.array([1.0, 1.0, 1.0])
        k_hot = M.progress(t, t_sun0 + 0.2, t_sun1 + 0.4, "sine") * (1 - 0.65 * a_gold(t))
        for col, k in [((246, 214, 226), 0.8 * _env(t, t_dawn0 + 0.2, t_dawn1, t_bite0, t_sun1)),
                       ((255, 224, 184), k_hot),
                       ((255, 212, 168), 0.55 * _env(t, t_beam, t_beam + 1.2, t_ang, t_calm0 + 1.2)),
                       ((255, 236, 204), 0.6 * a_gold(t))]:
            if k > 0:
                mul *= 1 - (1 - np.array(col, float) / 255.0) * k
        kn = 1 - M.progress(t, t_dawn0 - 0.1, t_pre1, "sine")
        if kn <= 0.003 and (mul >= 0.998).all():
            return frame
        arr = np.asarray(frame)
        if kn <= 0.003:
            arr = cv2.multiply(arr, (float(mul[0]), float(mul[1]), float(mul[2]), 1.0))
            return Image.fromarray(arr, "RGBA")
        f_sky = (mul * (1 - (1 - np.array((205, 200, 235), float) / 255.0) * 0.55 * kn)).astype(np.float32)
        f_land = (mul * (1 - (1 - np.array((112, 120, 186), float) / 255.0) * 0.82 * kn)).astype(np.float32)
        A = view.M[:2].astype(np.float64).copy()
        A[:, 2] += 0.5 * (A[:, 0] + A[:, 1]) - 0.5
        m = cv2.warpAffine(land_mask(), A, (arr.shape[1], arr.shape[0]), flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)
        rgb = arr[..., :3].astype(np.float32)
        rgb *= f_sky + m[..., None] * (f_land - f_sky)
        out = arr.copy()
        out[..., :3] = np.clip(rgb + 0.5, 0, 255).astype(np.uint8)
        return Image.fromarray(out, "RGBA")

    rng2 = np.random.default_rng(17)
    NDUST = 150
    dx0 = rng2.uniform(0, 1, NDUST)
    dy0 = rng2.uniform(0.2, 1.0, NDUST)
    dsp = rng2.uniform(0.7, 1.4, NDUST)
    dln = rng2.uniform(24, 100, NDUST)
    dal = rng2.uniform(80, 170, NDUST)
    SH = 4

    def dust(frame, t, view):
        """Anti-aliased blowing sand (v1), thinner over Jonah; dies down to a breeze for God's question."""
        k = M.progress(t, t_wind - 0.4, t_wind + 0.6, "sine") * (1 - 0.85 * a_gold(t))
        if k <= 0.01:
            return frame
        arr = np.array(frame)
        Hf, Wf = arr.shape[:2]
        ov = np.zeros((Hf, Wf, 4), np.uint8)
        jx_, jy_ = view.to_out(XJ - 10, GY - 150)
        rx, ry = 230 * view.scale, 240 * view.scale
        for i in range(NDUST):
            x = (dx0[i] * (Wf + 300) - t * 1100 * dsp[i]) % (Wf + 300) - 150
            y = dy0[i] * Hf + 18 * math.sin(t * 3 + i)
            dd = math.hypot((x - jx_) / rx, (y - jy_) / ry)
            fig = 0.25 + 0.75 * _clamp((dd - 0.75) / 0.6)
            a = dal[i] * k * (0.5 + 0.5 * dy0[i]) * fig
            if a < 4:
                continue
            if i % 3 == 0:
                col = (214, 172, 112)
                r = 2 + (i % 4)
                cv2.circle(ov, (int(x * 16), int(y * 16)), int(r * 16),
                           tuple(c * a / 255 for c in col) + (a,), -1, cv2.LINE_AA, SH)
            else:
                col = (250, 230, 188)
                cv2.line(ov, (int(x * 16), int(y * 16)), (int((x + dln[i]) * 16), int((y - dln[i] * 0.08) * 16)),
                         tuple(c * a / 255 for c in col) + (a,), 2 + i % 3, cv2.LINE_AA, SH)
        inv = cv2.merge([255 - ov[..., 3]] * 3)
        arr[..., :3] = cv2.add(cv2.multiply(arr[..., :3], inv, scale=1 / 255.0), ov[..., :3])
        return Image.fromarray(arr, "RGBA")

    def shimmer(frame, t, view):
        k = M.progress(t, t_sun1 - 0.2, t_sun1 + 0.6, "sine") * (1 - 0.6 * a_gold(t))
        if k <= 0.01:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i, (bx, by) in enumerate([(300, 930), (1600, 900), (1880, 870), (560, 860), (1380, 1010), (180, 1060),
                                      (760, 1040)]):
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

    def streaks(frame, t, view):
        """Little sparks of sunlight travelling down the sunbeam onto his head (additive, anti-aliased)."""
        k = a_beam(t) * (1 - M.progress(t, t_calm0 - 0.4, t_calm0 + 0.3, "sine"))
        if k <= 0.01:
            return frame
        kk = beam_aim(t)
        tgx = tx + (tx2 - tx) * kk
        tgy = ty + (ty2 - ty) * kk
        ddx, ddy = tgx - bx0, tgy - by0
        dl = math.hypot(ddx, ddy)
        pnx, pny = -ddy / dl, ddx / dl
        arr = np.array(frame)
        ov = np.zeros(arr.shape[:2] + (3,), np.uint8)
        for i in range(6):
            u = (t * 0.85 + i / 6) % 1.0
            off = ((i * 37) % 7 - 3) * 14
            sx_ = bx0 + ddx * (0.3 + 0.6 * u) + pnx * off * u
            sy_ = by0 + ddy * (0.3 + 0.6 * u) + pny * off * u
            p0 = view.to_out(sx_, sy_)
            p1 = view.to_out(sx_ + ddx / dl * 34, sy_ + ddy / dl * 34)
            a = k * math.sin(math.pi * u) ** 1.5
            cv2.line(ov, (int(p0[0] * 16), int(p0[1] * 16)), (int(p1[0] * 16), int(p1[1] * 16)),
                     (int(235 * a), int(200 * a), int(110 * a)), max(2, int(6 * view.scale)), cv2.LINE_AA, SH)
        arr[..., :3] = cv2.add(arr[..., :3], ov)
        return Image.fromarray(arr, "RGBA")

    sc.fx = [
        grade,
        FX.sparkles((60, 30, 2050, 470), count=26, t0=-1, t1=t_dawn0 + 1.0, color=(255, 250, 225), size=(4, 9),
                    period=2.2, drift=0, seed=4),
        FX.sparkles((XW - 330, GY - 210, XW + 40, GY - 10), count=12, t0=t_godw - 0.1, t1=t_worm1 + 0.3,
                    color=(255, 238, 160), size=(8, 18), period=1.1, drift=-10, seed=5),
        FX.motes((200, 200, 1900, 900), count=24, t0=t_dawn0 + 0.5, t1=t_sun1, color=(255, 240, 220), alpha=100),
        shimmer,
        dust,
        streaks,
        FX.vignette(lambda t: (0.27 * M.progress(t, t_sun1, t_dizzy, "sine") * (1 - 0.6 * a_gold(t))) *
                    (0.85 + 0.15 * math.sin(t * 3.2)), color=(150, 72, 24)),
        FX.sparkles((XJ - 520, GY - 760, XJ + 160, GY - 60), count=26, t0=t_light0 + 0.2, t1=T + 1,
                    color=(255, 238, 170), size=(9, 20), period=1.5, drift=-8, seed=8),
        FX.sparkles((XP - 160, GY - 560, XP + 400, GY - 40), count=14, t0=t_plant - 0.1, t1=t_plant_back + 1.0,
                    color=(255, 236, 160), size=(9, 18), period=1.2, drift=-6, seed=9),
        FX.motes((300, 0, 1700, 900), count=28, t0=t_light0, t1=T + 1, color=(255, 244, 205), alpha=120, seed=22),
    ]

    # =============================================================== SOUND
    sc.sfx("night", 0, dur=t_dawn0 + 1.4, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=t_wind + 0.2, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("rooster", t_dawn0 + 0.25, gain_db=-15, pan=-0.6)
    sc.sfx("birds", t_dawn0 + 0.6, dur=t_sun0 - t_dawn0, gain_db=-16, fade_in=0.6, fade_out=0.8, pan=0.3)
    sc.sfx("chime", t_godw, gain_db=-15)
    sc.sfx("sparkle", t_godw + 0.1, gain_db=-14, pan=-0.2)
    sc.sfx("crunch", t_bite0, gain_db=-7, pan=-0.2)
    sc.sfx("wither", t_with0, gain_db=-8)
    sc.sfx("pop", t_wake, gain_db=-13)
    sc.sfx("heat", t_sun0 + 0.3, dur=T - t_sun0 + 0.6, gain_db=-14, fade_in=0.8, fade_out=0.8)
    sc.sfx("whoosh", t_wind - 0.2, gain_db=-11, pan=0.6)
    sc.sfx("wind_hot", t_wind - 0.4, dur=t_light0 + 1.2 - (t_wind - 0.4), gain_db=-11, fade_in=0.6, fade_out=1.6)
    sc.sfx("wind_soft", t_light0 + 0.4, dur=T - t_light0 + 0.4, gain_db=-18, fade_in=1.0, fade_out=0.8)
    sc.sfx("pop", t_hot, gain_db=-15)
    sc.sfx("pop", t_ang, gain_db=-14)
    sc.sfx("chime", t_light0, gain_db=-11)
    sc.sfx("sparkle", t_plant, gain_db=-15, pan=-0.3)
    sc.sfx("thud", t_shout + 0.02, gain_db=-11)
    sc.sfx("thud", t_stamp, gain_db=-13)
    sc.sfx("thud", t_hmph + 0.32, gain_db=-13)
    sc.sfx("whoosh", t_hmph + 0.05, gain_db=-16)
    return sc
