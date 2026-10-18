"""Scene 9 (v2) — the sailors throw Jonah into the sea; at once the sea is calm; they fear the LORD, offer a
sacrifice and make vows (Jonah 1:15-16).

Two shots joined by a dip through the blank page in the pause after line 1:

  A (lines 0-1)  the approved v1 wide shot (art/scenes_v1/s06_fish.py, surface half): the ship (bow LEFT, torn
                 striped sail) rocking in the storm. It OPENS on s08's end framing: the camera is sized and placed so
                 this ship sits on s08's (art/scenes/s08_row.py: ship at SX0 + 262 / SY, scale .92, end camera
                 (1682, 670, 1600) on its 2640 stage), the crew kneel with raised hands, eyes closed and mouths a
                 small 'o' (s08's END_EXPR 'sleepy'), in s08's order and places (sailor 0, sailor 1, Jonah, sailor 2,
                 sailor 3, the captain on the raised stern under the lantern, where s08 ends him) under s08's prayer
                 light as it ends (a small warm opening in the clouds and four narrow golden shafts, redrawn in s08's
                 coordinates), which fades as they get up, so the incoming dissolve lines up instead of doubling.
  B (line 2)     on the calm deck (bulwark with painted shields, mast and torn sail on the left): the crew kneel in two
                 staggered rows, spread out so every face stays clear; a small bronze brazier on the right. God's
                 presence is only light: a warm glowing break in the clouds above and right of the brazier (the sun
                 stays hidden behind the clouds), soft rays and sparkles. The offering smoke rises BESIDE that light.

Narration (every key time comes from the chunks; a phrase inside a chunk is placed by its characters and snapped
to a pause in the voice take, see Cues):
  line 0 '于是，'    the crew get up one after another, the lifters first, 0.17 s apart (low kneel -> upright kneel ->
                    one knee -> standing, 4 frames per drawing; the captain on the stern goes straight from the upright
                    kneel to standing; each cut eased so heads never pop, then a quick stretch-and-settle about the
                    feet as follow-through) while the camera holds s08's framing;
         '他们'     the two lifters (sailors 1 and 2, either side of Jonah) crouch and take hold of him; once all are
                    up a lightning flash (camera still), then one slow pull-out to the v1 wide shot (zoom <= ~19 %/s)
                    that has settled before the launch;
         '抬起来'   they hoist him overhead: both face the stern with their arms stretched up, s1's hands under his
                    feet and knees, both of s2's under his shoulder, the palms drawn over his robe; he lies (hands
                    folded on his chest, head-cloth flap tucked behind his back) with his underside just above their
                    heads, never behind one; his head reaches past s2's with sky between them; the cut is sold
                    by a push-up (the new drawings start low and rise home with a small overshoot, Jonah riding on
                    their hands); the captain points over the stern at the sea;
                    '扔进了' heave (dip, push) and launch: he flies over the stern in a high arc (computed to clear the
                    heads of sailor 3 and the captain);
         '大海'     splash crown, drops, ripples, a burst of bubbles; the captain (on the stern, nearest the splash)
                    leans over the rail pointing DOWN at the ripples, sailors 2 and 3 lean over and look down.
  line 1 '一下子，'  the rain stops at once, the storm banks slide away, the sky turns blue;
         '海就平静了' the storm crests sink and the sea flattens; the sun emerges at full size from behind a
                    clearing cloud that drifts off to the right once the storm sky is nearly gone (its glow fades in
                    round the cloud), and a golden sunbeam; the crew (pose cut) lift their hands in awe, sailor 3
                    raises an arm toward the light;
         '风停了，'  the curly wind marks fade away and the pennant sags (12 / 25 / 45 deg in-betweens) to hang slack
                    behind the yard, swaying slowly; gulls glide in;
         '浪也静了。' the last swell settles, the ship lies still, glints sparkle on the water.
  pause          the push-in on the ship continues while the picture dips to the blank page and the deck appears
                 from it (no double exposure of the two shots).
  line 2 '水手们看见了，' standing on the calm deck they turn three-quarters toward the light, heads up; sailor 0
                    lifts his hands in wonder, sailor 3 raises an arm toward the light;
         '心里对耶和华又敬又怕。' one after another (0.3 s apart) they kneel: stand -> one knee (held 4 frames) ->
                    kneel with a small settle; heads bowed, palms together;
         '他们向耶和华献上祭物，' the captain lifts a bowl of grain over the brazier; at '献上' he pours it in: the
                    flame flares, sparks rise and a golden billow climbs the smoke; he sets the empty bowl down;
                    the others raise their heads;
         '还许下了诺言。' the sailors lift their hands toward the light (an open V, so hands go up, not forward
                    over the next face), the captain beside the altar lifts open palms at shoulder height; the rays
                    brighten, warm sparkles in the cloud break.
  The scene ends on a held, calm frame (the camera has drifted left and up a little): s10's sinking Jonah appears at
  output x 1040-1310, y 330-650 in the outgoing dissolve, and there the frame holds only sea and sky - no hands,
  faces, fire or smoke.

Pose changes are hard cuts (never crossfaded) sold by squash-and-hops, or by easing the new drawing in from half way
when the head height changes a lot; every pose is held >= 0.5 s (in-betweens 3-4 frames). Stage 2112 x 1188; the
camera stays inside the painted area.
"""
import math
import random
from dataclasses import replace

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s05_lots as V5
from art.scenes_v1 import s06_fish as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.paths import BUILD, OUT_W
from engine.scene import Scene

W, H = 2112, 1188
HORIZON, WL = V.HORIZON, V.WL          # 690, 880 (v1 wide shot)
SX, SS, SF = V.SX, V.SS, V.SF          # ship anchor x, scale, facing (-1: bow left)
SPLASH = V.SPLASH
JS = V.JS
PAPER_RGB = (243, 233, 210)            # the compositor's blank-page colour (paper grain is multiplied on top)


def deck_y(lx):
    """Deck (feet) line at ship-local x (the stern deck rises), un-rocked."""
    return WL + PR._hull_top(lx) * SS


def ship_x(lx):
    return SX - lx * SS                # SF = -1: local +x (toward the bow) is to the LEFT


# ---- shot A cast: s08's order and end places on the same ship (s08_row.py's End frame: sailors kneel at 274 / 132 /
#      -116 / -250, Jonah stands at JON_LX -4, the captain ends on the raised stern deck at CAPT_KNEEL_LX -436 on the
#      deck height at CAPT_KNEEL_DECK_LX -400, the lantern in front of his chest)
A_LX = dict(s0=274, s1=132, jon=-4, s2=-116, s3=-250, capt=-436)
A_POS = {k: (ship_x(lx), deck_y(-400 if k == "capt" else lx)) for k, lx in A_LX.items()}
A_F0 = dict(s0=1, s1=1, s2=-1, s3=-1, capt=-1)          # facings at the start (toward Jonah, as in s08)
DECK = A_POS["s1"][1]
L1X, L2X = A_POS["s1"][0], A_POS["s2"][0]                # the two lifters
JAIR_ROT = V.JAIR_ROT
PEN = PR.local_to_stage(SX, WL, SS, SF, -10, -930)           # masthead (pennant root)
SUN_A = (1700, 215)                                          # v1 sun (removed from V.background, own layer)

# s08's end framing in this stage: its ship (anchor SX0 + 262 = 1622, SY 1130, scale .92) seen by its end camera
# (1682, 670, 1600) maps onto this ship (SX, WL, scale .8) with the camera below; S08_TF maps s08 stage coordinates
# onto this stage the same way (its prayer light is redrawn through it).
_O08 = OUT_W / 1600                                          # s08's end camera: output px per s08 stage px
_K08 = 0.92 * _O08 / SS                                      # ...and per stage px here, for the matched camera
CAM_S08 = Cam(SX - (1622 - 1682) * _O08 / _K08, WL - (1130 - 670) * _O08 / _K08, OUT_W / _K08)
_S08 = SS / 0.92                                             # s08 stage px -> stage px here
S08_TF = f"translate({SX - 1622 * _S08:.2f},{WL - 1130 * _S08:.2f}) scale({_S08:.5f})"
S08_EXPR = "sleepy"                                          # s08's END_EXPR: eyes closed, a small 'o' mouth

# ---- shot B: the deck seen from on board
B_HOR, B_RAIL, B_DBACK = 560, 780, 872
GAP = (1730, 365)                      # the glowing break in the clouds (God's presence shown only as light)
MAST_B = 500
ALT = (1490, 1004)                     # brazier: foot line centre
RIM_Y = ALT[1] - 140                   # bowl rim
FLAME_B = (ALT[0], RIM_Y - 6)          # flame base
SMOKE_O = (ALT[0] + 2, RIM_Y - 64)     # smoke origin (the flame tip)
# two staggered rows, 160 px apart: every back-row face sits between two front-row figures
B_S3 = (605, 1046, 1.06)               # variant 3 (ginger beard), front row left
B_S1 = (765, 952, 0.88)                # variant 1, back row
B_S2 = (925, 1040, 1.04)               # variant 2, front row
B_S0 = (1085, 954, 0.88)               # variant 0, back row
B_CAPT = (1245, 1034, 1.02)            # the captain, front row, beside the brazier
GULL_B = (1835, B_RAIL - 26)           # gull perched on the rail

PUNCT = "，。！？：；、,.!?:;"


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


# ============================================================================ narration timing


def _nchar(s):
    return max(1, sum(1 for ch in s if ch not in PUNCT and not ch.isspace()))


def _dips(path):
    """Low-energy stretches (>= 40 ms) inside a voice take: [(start, end)] s from the take's start."""
    try:
        import soundfile as sf
        x, sr = sf.read(str(path), dtype="float32")
    except Exception:
        return []
    if x.ndim == 2:
        x = x.mean(axis=1)
    hop = sr // 100
    nb = len(x) // hop
    if nb < 10:
        return []
    e = np.sqrt((x[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1))
    e = np.convolve(e, np.ones(3) / 3, mode="same")
    low = e < 0.06 * e.max()
    out, i = [], 0
    while i < nb:
        if low[i]:
            j = i
            while j < nb and low[j]:
                j += 1
            if j - i >= 4 and i > 0 and j < nb:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


class Cues:
    """Times of phrases in the narration. A phrase at the start of a subtitle chunk starts with the chunk; one
    inside a chunk is placed by its characters and snapped to the end of a nearby pause in the voice take."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.dips = []
        for i, ln in enumerate(ctx.lines):
            for a, b in _dips(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"):
                self.dips.append((ln.start + a, ln.start + b))

    def at(self, phrase, default, snap=True):
        for ln in self.ctx.lines:
            spans = [(c.text, c.start, c.end) for c in ln.chunks] or [(ln.text, ln.start, ln.end)]
            for text, c0, c1 in spans:
                k = text.find(phrase)
                if k < 0:
                    continue
                if not any(ch not in PUNCT for ch in text[:k]):
                    return c0
                est = c0 + (c1 - c0) * _nchar(text[:k]) / _nchar(text)
                best, score = None, -1.0
                for a, b in (self.dips if snap else ()):
                    if c0 < a and b < c1 and abs(b - est) < 0.45:
                        sc_ = (b - a) - 0.15 * abs(b - est)
                        if sc_ > score:
                            best, score = b, sc_
                return best if best is not None else est
        return default


def hermite(keys):
    """Smooth path through (t, value, slope) keys with continuous velocity (cubic Hermite)."""
    keys = sorted(keys)

    def f(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1] + keys[-1][2] * (t - keys[-1][0])
        for (t0, v0, s0), (t1, v1, s1) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                h = t1 - t0
                u = (t - t0) / h
                h00 = 2 * u ** 3 - 3 * u ** 2 + 1
                h10 = u ** 3 - 2 * u ** 2 + u
                h01 = -2 * u ** 3 + 3 * u ** 2
                h11 = u ** 3 - u ** 2
                return h00 * v0 + h10 * h * s0 + h01 * v1 + h11 * h * s1
        return keys[-1][1]
    return f


def bump(t, ts, w=0.07):
    """0..1..0 triangle centred just after ts (a 3-4 frame hop that sells a pose cut)."""
    return max(0.0, 1 - abs(t - ts - 0.03) / w)


def stretch(u, amp=0.045):
    """Stretch-and-settle after a pose cut at u = 0 (s): +amp (taller) on the cut frame, a small squash ~0.1 s later,
    gone by 0.25 s. Used as sy = 1 + k, sx = 1 - k / 2 about the feet."""
    if u < 0 or u >= 0.25:
        return 0.0
    return amp * math.exp(-u / 0.07) * math.cos(2 * math.pi * u / 0.2)


def steps(keys):
    """Hard-cut flipbook index: keys = [(t, idx), ...]."""
    keys = sorted(keys)

    def f(t):
        idx = keys[0][1]
        for tk, i in keys:
            if t >= tk:
                idx = i
        return float(idx)
    return f


def cut_plan(heads, sched, min_dy=12.0):
    """For a hard-cut flipbook: each cut whose drawing moves the head by >= min_dy px is eased instead of popped
    (the new drawing starts half way and slides home, with a small settle when it lands); smaller cuts get a hop.
    heads: head y (stage px) of each frame; sched: [(t, idx)]. Returns (hop times, offset events)."""
    sched = sorted(sched)
    hops, offs = [], []
    for k in range(1, len(sched)):
        (_, i0), (t1, i1) = sched[k - 1], sched[k]
        d = heads[i1] - heads[i0]
        if abs(d) < min_dy:
            hops.append(t1)
            continue
        nxt = sched[k + 1][0] if k + 1 < len(sched) else 1e9
        dur = min(0.2, max(0.08, nxt - t1))
        offs.append((t1, -0.5 * d, dur, "out" if nxt - t1 < 0.3 else "back"))
    return hops, offs


def offset_dy(t, offs):
    v = 0.0
    for t0, dy0, dur, curve in offs:
        if t0 <= t < t0 + dur:
            v += dy0 * (1 - M.ease(curve)((t - t0) / dur))
    return v


# ============================================================================ figures

KNEEL = C.POSES["kneel_pray"]
STAND = C.POSES["stand"]
# s08's last drawing: kneeling low (sitting back on the heels), hands raised in an open V
K_LOWUP = dict(KNEEL, arms=(("fk", 146, 164), ("fk", -140, -160)), hands=("open", "open"), h=-24,
               look=(0.02, -0.06), legs=((86, -100), (88, -100)), t=0)
K_UPR = dict(KNEEL, t=2, h=4, arms=(("fk", 24, 46), ("fk", 12, 34)), hands=("open", "open"))   # upright kneel
HALF = dict(KNEEL, t=6, h=10, legs=((70, 8), (2, -90)), arms=(("fk", 20, 40), ("fk", 10, 30)),
            hands=("open", "open"))                                    # one knee down (in-between)
GAZE = dict(STAND, h=-16, look=(0.05, -0.07))                          # head up toward the light
DIAG_UP = dict(STAND, h=-16, arms=(("fk", 138, 146), ("ik", "torso", 1.2, 0.7, 1)), hands=("open", "open"),
               look=(0.05, -0.07))                                     # one arm raised toward the light
LEAN_POINT = dict(STAND, t=12, h=18, arms=(("fk", 60, 52), ("fk", 20, 30)), hands=("point", "open"),
                  look=(0.05, 0.06))                                   # leaning over, pointing DOWN at the water
LEAN_LOOK = dict(STAND, t=14, h=20, arms=(("fk", 30, 40), ("fk", 10, 30)), hands=("open", "open"),
                 look=(0.05, 0.07))                                    # leaning over, looking down
CAPT_SEA = dict(C.POSES["point"], t=4, h=6, arms=(("fk", 74, 80), ("fk", -10, -4)), look=(0.05, 0.03))
                                                                       # the captain points over the stern: there!
PRAY = C.POSES["pray"]
P_BOW = dict(KNEEL, t=6, h=16)                                         # palms together, head bowed
P_UP = dict(KNEEL)                                                     # palms together, head tilted up
P_VOW = dict(KNEEL, t=-4, h=-20, arms=(("fk", 156, 170), ("fk", -140, -160)), hands=("open", "open"),
             look=(0.02, -0.06))                                       # hands lifted in an open V (up, not forward)
P_VOW_LOW = dict(KNEEL, t=-3, h=-20, arms=(("fk", 20, 150), ("fk", -20, 160)), hands=("open", "open"),
                 look=(0.03, -0.06))                                   # the captain: open palms at shoulder height
P_OFFER = dict(KNEEL, t=2, h=2, arms=(("ik", "abs", 150, -196, 1), ("ik", "abs", 126, -186, 1)),
               hands=("open", "open"))                                 # holding the bowl out over the brazier
P_POUR = dict(KNEEL, t=4, h=10, arms=(("ik", "abs", 150, -214, 1), ("ik", "abs", 128, -204, 1)),
              hands=("open", "open"))                                  # ...tipping it into the fire
POUR_TILT = 48


def kfig(kind, variant, x, y, s, ps, expr, facing=1):
    """A sailor / the captain in any rig pose: (markup, hand points, head point) in stage px."""
    if kind == "capt":
        design, met = C._captain_design(), C._CAPTAIN_M
    else:
        design, met = C._sailor_design(variant), C._SAILOR_M
    f = 1 if facing >= 0 else -1
    inner, _ = C._figure(design, met, dict(ps), expr, f, True)
    hands = [(x + hx * s * f, y + hy * s) for hx, hy in C._LAST["hands"]]
    head = (x + C._LAST["head"][0] * s * f, y + C._LAST["head"][1] * s)
    return C._wrap_out(inner, x, y, s, f, f"{kind}{variant}"), hands, head


# ---- the hoist ('抬起来'): Jonah lies flat on the two lifters' raised hands with his underside just above their
#      heads (never behind a head). Both lifters face the stern; s1 holds his feet and knees, s2 his shoulders (both
#      hands up-left under the robe at his shoulder: his head reaches past s2's, with sky between them, and no hand
#      sits on s2's own crown). Each wrist sits just under his robe, so the palm (drawn over him) grips its edge.
JCAR_ARMS = (("ik", "torso", 0.35, 0.66, 1), ("ik", "torso", 0.5, 0.62, 1))   # Jonah's hands folded on his chest
HOIST_REACH = dict(s1=1.24, s2=1.30)   # arms stretched up (the 'throw' pose uses 1.12); s2 reaches across his head
HOIST_SHIFT = -10.0                    # Jonah carried this far toward the bow, so both lifters' hands are under him
HOIST_CLEAR = 6.0                      # his underside this far above the lifters' head tops
HOIST_GRIP = 4.0                       # wrists this far below his underside (the palms overlap his robe)
HOIST_DX = dict(s1=((36, 1, 0), (-38, -1, 0)), s2=((-34, 1, -2), (-58, -1, 0)))
                                       # (far, near) wrist (x from the anchor, elbow bend, extra dy)


def _hoist_pose(name, wy):
    return dict(C.POSES["lift"], reach=HOIST_REACH[name], hands=("open", "open"),
                arms=tuple(("ik", "abs", dx / SS, (wy + dy) / SS, bend) for dx, bend, dy in HOIST_DX[name]))


def _hoist_geometry():
    """(underside y of carried Jonah, {lifter: pose}) for the hoist, from the lifters' head tops."""
    tops = []
    for name, var in (("s1", 1), ("s2", 2)):
        x, y = A_POS[name]
        kfig("s", var, x, y, SS, _hoist_pose(name, -300.0), "worried", 1)
        tops.append(y + C._LAST["head_top"][1] * SS)
    u = min(tops) - HOIST_CLEAR
    return u, {name: _hoist_pose(name, u + HOIST_GRIP - A_POS[name][1]) for name in ("s1", "s2")}


HOIST_U, HOIST_POSES = _hoist_geometry()


def jonah_carried(x, y):
    """Jonah lying on his back on raised hands (the library's 'carried' pose with both hands on his chest, so no
    arm dangles down between the lifters' heads); anchor (x, y) is the middle of his underside."""
    ps = dict(C.POSES["carried"], arms=JCAR_ARMS, tail=(80, 95))   # head-cloth flap tucked behind his back
    inner, _ = C._figure(C._jonah_design(), C._ADULT, ps, ps["expr"], -1, True)
    return C._wrap_out(inner, x, y, JS, -1, "jonah-carried")


JCAR = ((L1X + L2X) / 2 - 20 * JS + HOIST_SHIFT, HOIST_U)    # carried Jonah: anchor (facing -1, head to the stern)
JCAR_C = (JCAR[0] + 20 * JS, JCAR[1] - 39.5 * JS)            # ...and his centre
JAIR_C = JCAR_C
JAIR = (JAIR_C[0] + 1 * JS, JAIR_C[1] + 135.5 * JS)          # 'fall' anchor


# ============================================================================ shot A painting


def a_background():
    """v1 calm sky / far sea, with its sun taken out (the sun gets its own layer so it never shows through the
    half-faded storm sky as a dark disc)."""
    b = V.background()
    for sub in ('<circle cx="1700" cy="215" r="360" fill="url(#s6sun)"/>',
                '<circle cx="1700" cy="215" r="88" fill="#fbd46b" stroke="#e49839" stroke-width="4"/>'):
        b = b.replace(sub, "")
    return b


def a_sun(part):
    """The v1 sun as two layers: its glow (fades in round the veil cloud) and its disc (always full size and opaque,
    hidden behind the storm sky and then the veil cloud, so a half-faded yellow disc is never seen over the blue /
    storm sky as an olive smudge)."""
    x, y = SUN_A
    if part == "glow":
        defs = S.rad_grad("s9sun", [(0, "#fff6d6", 0.95), (0.3, "#fff0c0", 0.6), (1, "#ffe9b0", 0)])
        return doc(f'<circle cx="{x}" cy="{y}" r="360" fill="url(#s9sun)"/>', defs)
    return doc(S.g(f'<circle cx="{x}" cy="{y}" r="88" fill="{P["sun"]}" stroke="{S.shade(P["sun_hot"], -0.1)}" '
                   f'stroke-width="4"/>', filter="wobble"))


SUN_VEIL = (1715, 262, 220, 150, 1)   # the clearing cloud in front of the sun: centre, size, seed (its silhouette
                                     # covers the disc + 4 px; it uncovers the disc between 24 and 236 px to the right)
VEIL_DX = 280.0                      # how far it drifts off to the right as the sky clears


def a_sun_veil():
    """The cloud the sun emerges from behind: a calm-weather cloud like V.clouds_clear's."""
    cx, cy, w, h, seed = SUN_VEIL
    return doc(S.g(S.cloud(cx, cy, w, h, "#fbf6ec", seed=seed, sw=3, shade_fill="#d8e6ea"), filter="wobble"))


def a_prayer_light(part):
    """s08's prayer light as it ends (art/scenes/s08_row.py gap_svg, its 'gap_through' glow and rays_svg), drawn in
    s08's stage coordinates and mapped onto this stage by S08_TF, so it lies on itself in the dissolve:
      'gap'      the small pale-gold opening in the clouds at s08 (2040, 350), a soft warm wash round it (normal);
      'through'  the light shining through the break (screen, sky level: it never lifts the sail);
      'rays'     four narrow golden shafts from the break passing BETWEEN the kneeling heads and fading on the deck,
                 and a faint warm pool on the deck (screen, over the crew)."""
    gx, gy = 2040.0, 350.0                                   # s08's cloud break (s08 stage px)
    if part == "gap":
        defs = (S.rad_grad("s9gap", [(0, "#fff7de", 1.0), (0.4, "#fdeab8", 0.95), (0.7, "#f7d995", 0.55),
                                     (0.88, "#f2cc80", 0.18), (1, "#f0c878", 0.0)])
                + S.rad_grad("s9gapw", [(0, "#f6d796", 0.32), (0.6, "#f0c880", 0.12), (1, "#f0c070", 0.0)]))
        b = (f'<ellipse cx="{gx}" cy="{gy}" rx="520" ry="300" fill="url(#s9gapw)"/>'
             f'<ellipse cx="{gx + 10}" cy="{gy + 4}" rx="300" ry="190" fill="url(#s9gap)"/>')
    elif part == "through":
        defs = S.rad_grad("s9gt", [(0, "#ffe7b0", 0.45), (0.45, "#f8d898", 0.2), (1, "#f0c880", 0.0)])
        b = f'<ellipse cx="{gx + 10}" cy="{gy}" rx="360" ry="220" fill="url(#s9gt)"/>'
    else:
        def x8(lx):                                          # s08's kneeling places (its ship at the end place)
            return 1622.0 - lx * 0.92

        def y8(lx):
            return 1130.0 + PR._hull_top(lx) * 0.92
        sx, sy = gx + 10, gy + 60
        head_y = y8(0) - 225
        k = (y8(0) - 10 - sy) / (head_y - sy)
        defs = ('<filter id="s9rb" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/>'
                '</filter><filter id="s9rc" x="-30%" y="-30%" width="160%" height="160%">'
                '<feGaussianBlur stdDeviation="3.5"/></filter>')
        shafts, cores = "", ""
        for i, (la, lb, w) in enumerate(((274, 132, 78), (132, -4, 74), (-4, -116, 76), (-116, -250, 70))):
            tx, ty = sx + ((x8(la) + x8(lb)) / 2 - sx) * k, y8(0) - 10      # between two heads, out on the deck
            L = math.hypot(tx - sx, ty - sy)
            nx, ny = -(ty - sy) / L, (tx - sx) / L
            for kind, ww, col, stops in (
                    ("s", w, "#ffe3a0", ((0, 0), (0.1, 0.42), (0.5, 0.28), (0.8, 0.12), (1, 0))),
                    ("c", w * 0.3, "#fff4d2", ((0, 0), (0.12, 0.62), (0.5, 0.36), (0.8, 0.12), (1, 0)))):
                gid = f"s9r{kind}{i}"
                defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{sx:.1f}" y1="{sy:.1f}" '
                         f'x2="{tx:.1f}" y2="{ty:.1f}">'
                         + "".join(f'<stop offset="{o}" stop-color="{col}" stop-opacity="{a}"/>' for o, a in stops)
                         + '</linearGradient>')
                w0 = ww * 0.12
                p = [(sx + nx * w0, sy + ny * w0), (tx + nx * ww / 2, ty + ny * ww / 2),
                     (tx - nx * ww / 2, ty - ny * ww / 2), (sx - nx * w0, sy - ny * w0)]
                d = '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in p) + f' Z" fill="url(#{gid})"/>'
                if kind == "s":
                    shafts += d
                else:
                    cores += d
        b = (f'<g filter="url(#s9rb)">{shafts}</g><g filter="url(#s9rc)">{cores}</g>'
             f'<ellipse cx="1622" cy="{y8(0) - 60:.1f}" rx="380" ry="120" fill="#ffe2a0" opacity="0.1" '
             f'filter="url(#blur-lg)"/>')
    return doc(f'<g transform="{S08_TF}">{b}</g>', defs)


def pennant(ang, L, curl=0.0, ripple=0.0, ph=0.0):
    """The masthead pennant (terracotta streamer, root at the masthead, flying toward the bow = LEFT).
    ang(s) is the direction along its length in degrees (0 = straight out to the left, 90 = hanging down)."""
    x0, y0 = PEN
    n = 16
    cx, cy = x0 - 4, y0 + 14
    top, bot = [], []

    def a_(s):
        return math.radians(ang(s) + ripple * s * math.sin(2 * math.pi * (1.4 * s - ph)) +
                            curl * max(0.0, (s - 0.62) / 0.38) ** 2)
    for i in range(n + 1):
        s = i / n
        a = a_(s)
        w = 22 * (1 - s) + 3
        nx, ny = -math.sin(a), -math.cos(a)      # normal of the direction (-cos a, sin a)
        top.append((cx + nx * w / 2, cy + ny * w / 2))
        bot.append((cx - nx * w / 2, cy - ny * w / 2))
        cx += -math.cos(a) * L / n
        cy += math.sin(a) * L / n
    pts = top + [(cx - math.cos(a_(1)) * 6, cy + math.sin(a_(1)) * 6)] + bot[::-1]
    d = S.smooth_path(pts, closed=True, tension=0.8)
    return doc(S.g(S.path(d, fill=P["sail_stripe"], sw=3.2), filter="wobble-fine"))


def pennant_frames():
    """0-3 storm (stretched out, rippling), 4-6 sagging in-betweens (12 / 25 / 45 deg), 7 calm (hanging slack down
    the mast with a soft curl at the tip; it sways by rotation, never by toggling drawings)."""
    fr = [pennant(lambda s: 4.0, 168, ripple=16, ph=k / 4) for k in range(4)]
    for base, L in ((12, 164), (25, 158), (45, 150)):
        fr.append(pennant(lambda s, b=base: b + 0.35 * b * s, L, ripple=8, ph=0.1))
    fr.append(pennant(lambda s: 78 + 6 * s, 140, curl=-38))
    return fr


SWIRL_O = (60, 80)      # where a wind mark is drawn inside its layer


def wind_swirl(k):
    """A picture-book wind mark (a long curly stroke with one loop), drawn at the stage origin; one of 3 shapes."""
    d = ["M0,0 C60,-26 130,-30 175,-4 C205,16 190,48 162,40 C138,32 146,4 176,0 C230,-6 290,8 350,-2",
         "M0,0 C70,-14 120,-10 160,6 C190,20 176,50 150,42 C126,34 136,6 168,2 C220,-4 260,-2 300,-12",
         "M0,0 C50,-20 110,-22 150,-2 C176,12 166,40 142,34 C120,28 128,4 156,0 C200,-4 240,4 280,0"][k % 3]
    return doc(f'<g transform="translate({SWIRL_O[0]},{SWIRL_O[1]})">'
               f'<path d="{d}" fill="none" stroke="#5d6b83" stroke-width="14" stroke-linecap="round" '
               f'opacity="0.35"/><path d="{d}" fill="none" stroke="#eef2f0" stroke-width="8" stroke-linecap="round" '
               f'opacity="0.9"/></g>')


# ============================================================================ shot B painting


def b_world():
    """Calm sky (warmer toward the cloud break), the glow behind the clouds, a far headland and the sea."""
    gx, gy = GAP
    defs = (S.lin_grad("bsky", [(0, "#78b8d6"), (0.45, "#a8d5e4"), (0.8, "#e4ecd8"), (1, "#f6e2b6")]) +
            S.rad_grad("bgapw", [(0, "#fff2c8", 1), (0.2, "#ffe2a0", 0.9), (0.45, "#f9d27e", 0.55),
                                 (0.75, "#f4c870", 0.18), (1, "#f0c070", 0.0)]) +
            S.rad_grad("bgapc", [(0, "#fffaf0", 1), (0.5, "#fff3d6", 0.75), (1, "#fbe9c0", 0.0)]) +
            S.lin_grad("bsea", [(0, "#cfe8e0"), (0.3, "#9ed0d6"), (0.75, "#62a9c0"), (1, "#4a98b6")]))
    b = f'<rect x="-40" y="-40" width="{W + 80}" height="{B_HOR + 60}" fill="url(#bsky)"/>'
    # warm light behind the clouds: no rim, no disc - a golden glow with a pale bright heart in the break
    b += f'<ellipse cx="{gx}" cy="{gy + 20}" rx="700" ry="400" fill="url(#bgapw)"/>'
    b += f'<ellipse cx="{gx}" cy="{gy + 10}" rx="230" ry="170" fill="url(#bgapc)"/>'
    # a hazy headland far away on the left horizon (as in the v1 calm)
    b += S.g(S.path(S.hill(-140, 620, B_HOR + 4, 74, seed=4, bottom=B_HOR + 12, bumps=2),
                    fill=S.mix(P["sea_light"], "#c9d9cf", 0.5), sw=2.5), filter="wobble", opacity=0.85)
    b += S.g(S.path(S.hill(380, 760, B_HOR + 4, 30, seed=9, bottom=B_HOR + 12, bumps=1),
                    fill=S.mix(P["sea_light"], "#d6e2d8", 0.6), sw=2), filter="wobble", opacity=0.7)
    # the sea
    b += f'<rect x="-40" y="{B_HOR}" width="{W + 80}" height="{B_RAIL - B_HOR + 60}" fill="url(#bsea)"/>'
    b += S.g(S.path(f"M-40,{B_HOR} L{W + 40},{B_HOR}", sw=3), filter="wobble", opacity=0.55)
    # the light's glitter path on the water, under the cloud break
    r = random.Random(5)
    gl = ""
    for i in range(15):
        y = B_HOR + 7 + i * 12 + i * i * 0.45
        w = 22 + i * 9 + r.uniform(-8, 8)
        x = gx + r.uniform(-14, 14) - i * 3
        gl += (f'<path d="M{x - w / 2:.0f},{y:.0f} L{x + w / 2:.0f},{y:.0f}" stroke="#fff7dc" '
               f'stroke-width="{3 + i * 0.4:.1f}" stroke-linecap="round" opacity="{0.7 - i * 0.03:.2f}"/>')
    b += S.g(gl, filter="wobble")
    # long calm swells
    sw_ = ""
    for i, (y, a, lam, ph) in enumerate([(B_HOR + 30, 2, 260, 0.3), (B_HOR + 66, 3, 330, 1.4),
                                         (B_HOR + 110, 4, 420, 2.2), (B_HOR + 160, 5, 520, 0.8)]):
        sw_ += S.path(S.wave_line(y, a, lam, ph, x0=-60, x1=W + 60), stroke=False,
                      extra=f'stroke="#e6f3ee" stroke-width="{2.5 + i}" fill="none" opacity="0.45" '
                            f'stroke-dasharray="{120 + 60 * i} {70 + 40 * i}" stroke-dashoffset="{37 * i}"')
    b += S.g(sw_, filter="wobble")
    return doc(b, defs)


def _halo(cloud_markup, col="#f6c95e"):
    """A golden rim light behind a cloud lit from behind: the same cloud, a little larger, in gold, blurred."""
    return cloud_markup.replace(f'stroke="{S.INK}"', f'stroke="{col}"').replace('fill="#fbf4e6"', f'fill="{col}"')


def b_clouds(drifting):
    gx, gy = GAP
    if drifting:          # one small cloud drifts by (the others are part of the background)
        return doc(S.g(S.cloud(1000, 492, 170, 52, "#fbf6ec", seed=12, sw=2.5, shade_fill="#dbe7ea"),
                       filter="wobble"))
    # the cloud bank round the break: a cap over the hidden sun, two lids either side of the gap, all with a
    # golden rim where the light behind them shines round their edges
    lids = [(gx + 20, gy - 190, 700, 190, 16, 6), (gx - 268, gy + 6, 400, 118, 14, 5),
            (gx + 300, gy - 12, 470, 146, 15, 6)]
    halo, body = "", ""
    for x, y, w, h, seed, puffs in lids:
        halo += _halo(S.cloud(x, y + 4, w * 1.07, h * 1.16, "#fbf4e6", seed=seed, sw=7, puffs=puffs))
        body += S.cloud(x, y, w, h, "#fbf4e6", seed=seed, sw=3, puffs=puffs, shade_fill="#f1e2c2")
    b = f'<g filter="url(#soft)" opacity="0.9">{halo}</g>' + S.g(body, filter="wobble")
    b += S.g(S.cloud(-60, 420, 380, 110, "#fbf6ec", seed=3, sw=3, shade_fill="#dbe7ea") +
             S.cloud(860, 372, 300, 92, "#fbf6ec", seed=5, sw=3, shade_fill="#dbe7ea"), filter="wobble")
    return doc(b)


def inner(d):
    """The content of an svg_doc (its <defs> and body) for nesting several paintings into one layer."""
    return d[d.index(">") + 1:d.rindex("</svg>")]


def b_background():
    """Shot B's static backdrop in ONE layer (cheap to composite): sky, glow, sea, clouds, deck and rig."""
    return doc(inner(b_world()) + inner(b_clouds(False)) + inner(b_deck()))


def b_sea_lines(k):
    """Soft foam ripple strokes on the calm water."""
    b = ""
    r = random.Random(20 + k)
    for i in range(9):
        y = B_HOR + 22 + i * 22 + r.uniform(-4, 4)
        x = r.uniform(-100, W)
        w = 120 + i * 22
        b += S.path(S.wave_line(y, 2 + i * 0.3, w / 1.5, r.uniform(0, 6), x0=x, x1=x + w), stroke=False,
                    extra=f'stroke="#f4faf4" stroke-width="{2.5 + i * 0.35:.1f}" fill="none" opacity="0.55" '
                          f'stroke-linecap="round"')
    return doc(S.g(b, filter="wobble"))


def b_glints(k):
    """Twinkling glints on the light's path on the water (one of four phases)."""
    rng = random.Random(40 + k)
    b = ""
    for i in range(14):
        u = rng.random()
        y = B_HOR + 12 + u * (B_RAIL - B_HOR - 20)
        x = GAP[0] - 30 * u + rng.uniform(-1, 1) * (40 + 200 * u)
        rr = 5 + 9 * rng.random()
        w = rr * 0.24
        b += (f'<path d="M{x:.1f},{y - rr:.1f} L{x + w:.1f},{y - w:.1f} L{x + rr * 1.3:.1f},{y:.1f} L{x + w:.1f},'
              f'{y + w:.1f} L{x:.1f},{y + rr:.1f} L{x - w:.1f},{y + w:.1f} L{x - rr * 1.3:.1f},{y:.1f} '
              f'L{x - w:.1f},{y - w:.1f} Z" fill="#fffbe8" opacity="0.9"/>')
    return doc(b)


def b_rig():
    """Mast, shrouds and the torn striped sail (v1 deck rig), hanging calm."""
    mx = MAST_B
    base = B_DBACK + 70
    b = ""
    for xr in (mx - 360, mx + 120):
        b += f'<path d="M{mx},-200 L{xr},{B_RAIL + 6}" stroke="{P["ink_soft"]}" stroke-width="5" fill="none"/>'
    b += f'<rect x="{mx - 29}" y="-60" width="58" height="{base + 60}" fill="url(#bmast)" {S.STROKE}/>'
    for yy in (640, 690):
        b += f'<rect x="{mx - 35}" y="{yy}" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<path d="M{mx - 57},{base} Q{mx},{base - 32} {mx + 57},{base} Z" fill="{P["wood_dark"]}" {S.STROKE}/>'
    b += f'<path d="M{mx + 29},610 L{mx + 76},610" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linecap="round"/>'
    k, y_yard = 0.84, 196
    base_y = y_yard + 848 * k
    sail = PR._sail("torn", "s9sail")
    b += (f'<g transform="rotate(3 {mx} {y_yard})"><g transform="translate({mx},{base_y}) scale({-k},{k}) '
          f'translate(10,0)">{sail}</g></g>')
    sx = mx - k * 290
    b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} L{sx - 230:.0f},{B_RAIL + 4}" stroke="{P["ink_soft"]}" '
          f'stroke-width="4" fill="none"/>')
    sx = mx + k * 310
    b += (f'<path d="M{sx:.0f},{base_y - 585 * k:.0f} Q{mx + 120:.0f},{base_y - 470 * k:.0f} {mx + 30},600" '
          f'stroke="{P["ink_soft"]}" stroke-width="4" fill="none"/>')
    defs = S.lin_grad("bmast", [(0, P["wood_dark"]), (0.4, P["wood_light"]), (1, P["wood"])], x1=0, y1=0, x2=1, y2=0)
    return S.g(b, filter="wobble"), defs


def b_deck():
    """Far bulwark with shields, the sunlit deck (puddles left by the storm), the rig, crate, jar and rope."""
    defs = (S.lin_grad("bdeck", [(0, "#c69259"), (0.45, "#d9a56b"), (1, "#b07a48")]) +
            S.lin_grad("bbulw", [(0, P["wood"]), (1, "#80502f")]) +
            S.rad_grad("bwarm", [(0, "#fff1c4", 0.5), (1, "#fff1c4", 0)]))
    b = ""
    b += (f'<rect x="-40" y="{B_RAIL + 14}" width="{W + 80}" height="{B_DBACK - B_RAIL - 4}" fill="url(#bbulw)" '
          f'{S.STROKE}/>')
    b += V5.plank_lines(-40, W + 40, [B_RAIL + 42, B_RAIL + 68], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += (f'<rect x="{x - 12}" y="{B_RAIL + 4}" width="24" height="{B_DBACK - B_RAIL}" fill="{P["wood_dark"]}" '
              f'{S.STROKE_THIN}/>')
    for xr in (MAST_B - 360, MAST_B + 120):
        b += f'<circle cx="{xr}" cy="{B_RAIL + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += V5.shield(x, B_RAIL + 52, 33, cols[i % 4])
    b += (f'<path d="M-40,{B_RAIL} L{W + 40},{B_RAIL} L{W + 40},{B_RAIL + 18} L-40,{B_RAIL + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    b += (f'<path d="M-40,{B_RAIL + 5} L{W + 40},{B_RAIL + 5}" stroke="#f6dca6" stroke-width="5" opacity="0.8"/>')
    b += f'<rect x="-40" y="{B_DBACK}" width="{W + 80}" height="{H - B_DBACK + 40}" fill="url(#bdeck)" {S.STROKE}/>'
    ys, y, gap = [], B_DBACK + 14, 15
    while y < H + 40:
        ys.append(y)
        y += gap
        gap *= 1.17
    b += V5.plank_lines(-40, W + 40, ys, seed=7, opacity=0.42, joint_every=(260, 620))
    # puddles left by the storm, mirroring the sky
    for (x, y, rx, ry) in [(560, 1122, 120, 15), (1130, 1160, 110, 13), (1700, 1104, 130, 15), (1930, 1004, 80, 10)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#bfe0e6" opacity="0.6"/>'
        b += (f'<path d="M{x - rx * 0.55},{y - 3} l{rx * 0.5},0 M{x + rx * 0.1},{y + 4} l{rx * 0.3},0" '
              f'stroke="#fbfdf6" stroke-width="3.5" stroke-linecap="round" opacity="0.8"/>')
    # warm light pooled on the deck where the rays fall
    b += '<ellipse cx="1180" cy="1010" rx="640" ry="120" fill="url(#bwarm)"/>'
    rig, rdefs = b_rig()
    b = S.g(b, filter="wobble") + rig
    b += PR.crate(380, 905, 1.0) + PR.jar(290, 930, 0.62, rot=-6) + C.ground_shadow(380, 958, 1.0, width=150,
                                                                                      opacity=0.16)
    b += PR.rope_coil(MAST_B + 70, B_DBACK + 82, 0.9)
    return doc(b, defs + rdefs)


def b_foreground():
    return doc(PR.rope_coil(430, 1158, 1.4) + V5.bucket(1800, 1132, 1.05) +
               C.ground_shadow(1800, 1134, 1.0, width=120, opacity=0.18))


def b_gap_through():
    """The light shining through / round the cloud edges at the break (screen-blended over the clouds)."""
    gx, gy = GAP
    defs = S.rad_grad("bgt", [(0, "#fff0c0", 0.95), (0.3, "#fbdc96", 0.55), (0.65, "#f6d08a", 0.18),
                              (1, "#f6d08a", 0.0)])
    return doc(f'<ellipse cx="{gx}" cy="{gy + 6}" rx="460" ry="320" fill="url(#bgt)"/>', defs)


def b_rays():
    """Soft golden rays fanning down from the cloud break over the deck and the crew (thin blurred wedges with a
    radial falloff: none at the break itself, strongest a little below it), and a faint warm pool on the crew."""
    gx, gy = GAP[0], GAP[1] + 26
    defs = (f'<radialGradient id="brg" gradientUnits="userSpaceOnUse" cx="{gx}" cy="{gy}" r="1300">'
            '<stop offset="0" stop-color="#ffefc0" stop-opacity="0"/>'
            '<stop offset="0.1" stop-color="#ffe6a6" stop-opacity="0.85"/>'
            '<stop offset="0.45" stop-color="#ffdc94" stop-opacity="0.55"/>'
            '<stop offset="0.85" stop-color="#ffd488" stop-opacity="0.16"/>'
            '<stop offset="1" stop-color="#ffd488" stop-opacity="0"/></radialGradient>'
            '<filter id="brb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/>'
            '</filter>')
    b = ""
    for ang, wa in ((82, 1.8), (96, 2.6), (110, 2.0), (123, 3.0), (135, 2.2), (146, 2.8), (156, 2.2), (165, 1.8)):
        a, w = math.radians(ang), math.radians(wa)
        R = 1400
        p = [(gx + 8 * math.cos(a + 1.57), gy + 8 * math.sin(a + 1.57)),
             (gx + R * math.cos(a - w), gy + R * math.sin(a - w)),
             (gx + R * math.cos(a + w), gy + R * math.sin(a + w)),
             (gx - 8 * math.cos(a + 1.57), gy - 8 * math.sin(a + 1.57))]
        b += '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in p) + '" fill="url(#brg)"/>'
    b = f'<g filter="url(#brb)">{b}</g>'
    b += '<ellipse cx="1000" cy="900" rx="560" ry="210" fill="#ffe6ac" opacity="0.24" filter="url(#blur-lg)"/>'
    return doc(b, defs)


# ---------------------------------------------------------------- the offering: brazier, flame, smoke


def brazier():
    """Small bronze tripod brazier with glowing coals (anchor ALT on the deck)."""
    x, y = ALT
    br, dk, lt = "#b9853f", "#7d5226", "#e4b46c"
    defs = S.lin_grad("bbowl", [(0, lt), (0.45, br), (1, dk)], x1=0, y1=0, x2=1, y2=0.4)
    b = C.ground_shadow(x, y + 2, 1.0, width=210, opacity=0.24)
    leg = ""
    leg += (f'<path d="M{x + 10},{RIM_Y + 34} Q{x + 18},{y - 60} {x + 14},{y - 16}" stroke="{S.INK}" '
            f'stroke-width="17" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x + 10},{RIM_Y + 34} Q{x + 18},{y - 60} {x + 14},{y - 16}" stroke="{dk}" '
            f'stroke-width="9" fill="none" stroke-linecap="round"/>')
    for sgn in (-1, 1):
        leg += (f'<path d="M{x + sgn * 44},{RIM_Y + 30} Q{x + sgn * 58},{y - 70} {x + sgn * 70},{y - 8}" '
                f'stroke="{S.INK}" stroke-width="19" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x + sgn * 44},{RIM_Y + 30} Q{x + sgn * 58},{y - 70} {x + sgn * 70},{y - 8}" '
                f'stroke="{br}" stroke-width="11" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x + sgn * 47},{RIM_Y + 40} Q{x + sgn * 58},{y - 72} {x + sgn * 66},{y - 20}" '
                f'stroke="{lt}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>'
                f'<ellipse cx="{x + sgn * 74}" cy="{y - 4}" rx="16" ry="9" fill="{br}" {S.STROKE_THIN}/>')
    leg += (f'<ellipse cx="{x + 4}" cy="{y - 58}" rx="60" ry="9" fill="none" stroke="{S.INK}" stroke-width="10"/>'
            f'<ellipse cx="{x + 4}" cy="{y - 58}" rx="60" ry="9" fill="none" stroke="{br}" stroke-width="5"/>')
    b += S.g(leg, filter="wobble-fine")
    bowl = ""
    bowl += (f'<path d="M{x - 84},{RIM_Y} Q{x - 78},{RIM_Y + 50} {x},{RIM_Y + 52} Q{x + 78},{RIM_Y + 50} '
             f'{x + 84},{RIM_Y} Z" fill="url(#bbowl)" {S.STROKE}/>')
    bowl += (f'<path d="M{x - 72},{RIM_Y + 18} Q{x},{RIM_Y + 34} {x + 72},{RIM_Y + 18}" stroke="{dk}" '
             f'stroke-width="5" fill="none" opacity="0.7"/>')
    for i in range(7):
        u = -0.75 + i * 0.25
        bowl += f'<circle cx="{x + u * 68:.1f}" cy="{RIM_Y + 26 + 6 * (1 - u * u):.1f}" r="4" fill="{lt}" opacity="0.9"/>'
    coals = ""
    rr = random.Random(3)
    for i in range(9):
        cx = x - 58 + i * 14.5 + rr.uniform(-4, 4)
        cy = RIM_Y - 4 - 9 * math.sin(math.pi * (i + 0.5) / 9) + rr.uniform(-2, 2)
        r = rr.uniform(10, 15)
        coals += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#5e2c1e" {S.STROKE_THIN}/>'
        coals += (f'<path d="M{cx - r * 0.5:.1f},{cy:.1f} q{r * 0.4:.1f},{-r * 0.3:.1f} {r * 0.8:.1f},{r * 0.1:.1f}" '
                  f'stroke="#f39a3c" stroke-width="3" fill="none" stroke-linecap="round"/>')
    bowl += coals
    bowl += (f'<path d="M{x - 84},{RIM_Y} Q{x},{RIM_Y + 15} {x + 84},{RIM_Y}" stroke="{S.INK}" stroke-width="13" '
             f'fill="none" stroke-linecap="round"/>'
             f'<path d="M{x - 84},{RIM_Y} Q{x},{RIM_Y + 15} {x + 84},{RIM_Y}" stroke="{lt}" stroke-width="6" '
             f'fill="none" stroke-linecap="round"/>')
    b += S.g(bowl, filter="wobble-fine")
    return doc(b, defs)


def flame(i):
    """One of six hand-drawn flicker frames of the altar flame (base at FLAME_B, ~100 px tall)."""
    rr = random.Random(70 + i)
    bx, by = FLAME_B

    def tongue(cx, h, w, lean):
        pts = [(cx - w, by), (cx - w * 0.85, by - h * 0.32), (cx - w * 0.35 + lean * 0.35, by - h * 0.7),
               (cx + lean, by - h), (cx + w * 0.3 + lean * 0.5, by - h * 0.62), (cx + w * 0.85, by - h * 0.3),
               (cx + w, by)]
        return S.smooth_path(pts, closed=False, tension=0.9) + f" Q{cx},{by + w * 0.5:.1f} {cx - w:.1f},{by} Z"

    outer = [tongue(bx - 26, 64 + rr.uniform(-10, 12), 26, rr.uniform(-16, 4)),
             tongue(bx + 4, 102 + rr.uniform(-12, 14), 40, rr.uniform(-12, 12)),
             tongue(bx + 30, 58 + rr.uniform(-10, 10), 24, rr.uniform(-4, 16))]
    mid = [tongue(bx - 6, 62 + rr.uniform(-8, 10), 26, rr.uniform(-10, 10)),
           tongue(bx + 18, 40 + rr.uniform(-6, 8), 16, rr.uniform(-6, 10))]
    core = tongue(bx + 2, 30 + rr.uniform(-4, 6), 14, rr.uniform(-5, 5))
    b = "".join(f'<path d="{d}" fill="#f08c38" stroke="{S.INK}" stroke-width="7" stroke-linejoin="round"/>'
                for d in outer)
    b += "".join(f'<path d="{d}" fill="#f08c38"/>' for d in outer)
    b += "".join(f'<path d="{d}" fill="#f7cd55"/>' for d in mid)
    b += f'<path d="{core}" fill="#fff3cc"/>'
    return doc(S.g(b, filter="wobble-fine"))


def glow():
    x, y = FLAME_B
    defs = S.rad_grad("bglow", [(0, "#ffd27a", 0.75), (0.45, "#ffc56a", 0.3), (1, "#ffc56a", 0)])
    return doc(f'<circle cx="{x}" cy="{y - 40}" r="240" fill="url(#bglow)"/>', defs)


SMOKE_L = 370          # height of the smoke column (it has faded out before the cloud bank)
SMOKE_LEAN = 60        # it leans a little toward the light, rising beside it (never over it)
SMOKE_N = 11           # puffs along the column
SMOKE_INK_A = 0.6      # opacity of its thin umber outline


def smoke_xy(s):
    """Centre line of the smoke column at height fraction s (0 = flame tip): a gentle S-curve leaning toward the
    light. Static: the puffs travel along it, so the drawing cycle loops seamlessly."""
    ox, oy = SMOKE_O
    return (ox + SMOKE_LEAN * s ** 1.5 + 12 * s * math.sin(2 * math.pi * (0.9 * s - 0.15)), oy - SMOKE_L * s)


def _puffs_svg(circles, sw=2.4):
    """Picture-book smoke from circles [(x, y, r, fill)]: ONE thin umber outline round the whole silhouette (all
    rims first in a translucent group, then all fills), a soft shade low on the right of the bigger puffs and pale
    highlights. No blur."""
    rim = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + sw:.1f}" fill="{S.INK}"/>' for x, y, r, _ in circles)
    body = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}"/>' for x, y, r, c in circles)
    big = [c for c in circles if c[2] > 13]
    shade = "".join(f'<circle cx="{x + r * 0.22:.1f}" cy="{y + r * 0.26:.1f}" r="{r * 0.7:.1f}" fill="#ddd5d2" '
                    f'opacity="0.4"/>' for x, y, r, _ in big)
    body2 = "".join(f'<circle cx="{x - r * 0.1:.1f}" cy="{y - r * 0.12:.1f}" r="{r * 0.72:.1f}" fill="{c}"/>'
                    for x, y, r, c in big)
    hi = "".join(f'<path d="M{x - r * 0.62:.1f},{y - r * 0.05:.1f} q{r * 0.12:.1f},{-r * 0.5:.1f} {r * 0.58:.1f},'
                 f'{-r * 0.58:.1f}" fill="none" stroke="#fffaf0" stroke-width="{max(2.0, r * 0.11):.1f}" '
                 f'stroke-linecap="round" opacity="0.7"/>' for x, y, r, _ in big[::2])
    return f'<g opacity="{SMOKE_INK_A}">{rim}</g>{body}{shade}{body2}{hi}'


def _smoke_col(s):
    return S.mix("#fbf7ef", "#f8e2a8", min(1.0, s * 1.2))     # cream low down, pale gold in the light


def smoke_column(ph):
    """The smoke rising from the flame, phase ph (0..1) of its rise: billowy little clusters (3 lobes each) that
    grow and speed up as they climb a gentle S-curve, cream to pale gold, one thin umber wobble line, fading in
    above the flame and out well below the clouds. Everything depends on the height only, so the 12-drawing
    cycle loops seamlessly."""
    ox, oy = SMOKE_O
    circ = []
    n = 14
    for i in range(-1, n + 2):
        u = (i + ph) / n
        if u < 0 or u > 1.08:
            continue
        s_ = u ** 1.3
        x, y = smoke_xy(min(1.0, s_))
        x += (3 + 12 * s_) * math.sin(2 * math.pi * (1.6 * s_ + 0.15))
        r = 10 + 30 * s_
        a = 2 * math.pi * 1.3 * s_
        col = _smoke_col(s_)
        circ += [(x - 0.5 * r * math.cos(a), y + 0.22 * r, 0.72 * r, col),
                 (x + 0.48 * r * math.cos(a), y - 0.12 * r, 0.66 * r, col),
                 (x, y - 0.18 * r, r, col)]
    gid, mid_ = f"smg{int(ph * 1000)}", f"smm{int(ph * 1000)}"
    defs = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{ox}" y1="{oy + 8}" x2="{ox}" '
            f'y2="{oy - SMOKE_L - 30}"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="0.07" stop-color="#fff" stop-opacity="0.95"/>'
            f'<stop offset="0.45" stop-color="#fff" stop-opacity="0.88"/>'
            f'<stop offset="0.86" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="{mid_}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/></mask>')
    return doc(f'<g mask="url(#{mid_})" opacity="0.92">{S.g(_puffs_svg(circ), filter="wobble-fine")}</g>', defs)


def smoke_billow():
    """The golden billow released at the flare (centred on SMOKE_O; it is moved up the column)."""
    x, y = SMOKE_O
    circ = [(x - 22, y + 6, 24, "#fbe6b0"), (x + 4, y - 14, 30, "#fbe3a6"), (x + 28, y + 4, 22, "#fbe6b0"),
            (x + 2, y + 14, 22, "#fcebc0")]
    return doc(S.g(_puffs_svg(circ, sw=2.2), filter="wobble-fine", opacity=0.92))


def offering_bowl(cx, cy, s=1.0, tilt=0.0, full=True):
    """Small terracotta bowl heaped with grain (the offering), centred on its rim (cx, cy)."""
    rx, d = 34 * s, 26 * s
    sw = 3.2 * s
    st = f'stroke="{S.INK}" stroke-width="{sw:.1f}" stroke-linejoin="round"'
    b = ""
    if full:
        b += (f'<path d="M{cx - rx * 0.9:.1f},{cy:.1f} Q{cx - rx * 0.6:.1f},{cy - 22 * s:.1f} {cx:.1f},{cy - 24 * s:.1f} '
              f'Q{cx + rx * 0.6:.1f},{cy - 22 * s:.1f} {cx + rx * 0.9:.1f},{cy:.1f} Z" fill="{P["sand"]}" {st}/>')
        rr = random.Random(9)
        for _ in range(9):
            gx, gy = cx + rr.uniform(-0.6, 0.6) * rx, cy - rr.uniform(3, 17) * s
            b += f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{2.6 * s:.1f}" ry="{1.7 * s:.1f}" fill="{P["sand_dark"]}"/>'
    b += (f'<path d="M{cx - rx:.1f},{cy:.1f} Q{cx - rx * 0.92:.1f},{cy + d * 1.2:.1f} {cx:.1f},{cy + d:.1f} '
          f'Q{cx + rx * 0.92:.1f},{cy + d * 1.2:.1f} {cx + rx:.1f},{cy:.1f} Z" fill="{P["terracotta"]}" {st}/>')
    b += (f'<path d="M{cx - rx * 0.86:.1f},{cy + d * 0.38:.1f} Q{cx:.1f},{cy + d * 0.62:.1f} {cx + rx * 0.86:.1f},'
          f'{cy + d * 0.38:.1f}" stroke="{P["headcloth"]}" stroke-width="{4 * s:.1f}" fill="none"/>')
    b += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{6 * s:.1f}" fill="none" {st}/>')
    if tilt:
        b = f'<g transform="rotate({tilt:.1f} {cx:.1f} {cy:.1f})">{b}</g>'
    return S.g(b, filter="wobble-fine")


def b_frames(kind, variant, pos, poses):
    """Flipbook docs for one crew member on the deck. poses: [(pose dict, expr, extra)], extra None | 'bowl' |
    'pour' | 'down' (the empty bowl set on the deck). Returns (docs, head y per frame, hands per frame)."""
    x, y, s = pos
    out, heads, hand_l = [], [], []
    for ps, ex, extra in poses:
        kneeling = ps.get("legs") == KNEEL["legs"]
        body = C.ground_shadow(x + (-14 if kneeling else 0) * s, y, s, width=200 if kneeling else 130, opacity=0.2)
        fig, hands, head = kfig(kind, variant, x, y, s, ps, ex)
        body += fig
        if extra in ("bowl", "pour"):
            hx = (hands[0][0] + hands[1][0]) / 2
            hy = min(hands[0][1], hands[1][1])
            body += offering_bowl(hx + 4 * s, hy - 22 * s, s * 0.95, tilt=POUR_TILT if extra == "pour" else 0,
                                  full=extra == "bowl")
        elif extra == "down":
            bx = x + 128 * s
            body = (C.ground_shadow(bx, y + 2, s * 0.5, width=110, opacity=0.18) +
                    offering_bowl(bx, y - 29 * s, s * 0.95, full=False) + body)
        out.append(doc(body))
        heads.append(head[1])
        hand_l.append(hands)
    return out, heads, hand_l


def grains(k, lip):
    """Falling grain (3 phases) from the tipped bowl's lip into the coals."""
    x0, y0 = lip
    x1, y1 = FLAME_B[0] - 12, RIM_Y - 8
    b = ""
    for i in range(9):
        u = ((i + k / 3) / 9) % 1.0
        gx = lerp(x0, x1, u) + 4 * math.sin(i * 2.1)
        gy = lerp(y0, y1, u) + 10 * u * u
        b += (f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="4.6" ry="3.2" fill="{P["sand"]}" stroke="{S.INK}" '
              f'stroke-width="1.6"/>')
    return doc(S.g(b, filter="wobble-fine"))


# ============================================================================ effects


def sparks_fx(src, t0, t1, rate, seed=4):
    """Little rising sparks from the flame (output space)."""
    rng = np.random.default_rng(seed)
    n = max(1, int((t1 - t0) * rate))
    ts = t0 + (np.arange(n) + rng.uniform(0, 1, n)) / rate
    xs = rng.uniform(-30, 30, n)
    vx = rng.uniform(-25, 55, n)
    vy = rng.uniform(140, 260, n)
    life = rng.uniform(0.7, 1.4, n)
    ph = rng.uniform(0, 6.3, n)
    sz = rng.uniform(2.5, 4.5, n)

    def fx(frame, t, view):
        live = np.nonzero((ts <= t) & (t < ts + life))[0]
        if not len(live):
            return frame
        pts = []
        for i in live:
            age = t - ts[i]
            x = src[0] + xs[i] + vx[i] * age + 9 * math.sin(age * 7 + ph[i])
            y = src[1] - vy[i] * age + 40 * age * age
            ox, oy = view.to_out(x, y)
            r = sz[i] * view.scale * (1 - 0.5 * age / life[i])
            pts.append((ox, oy, r, int(235 * (1 - age / life[i]))))
        x0 = int(max(0, min(p[0] - 3 * p[2] for p in pts) - 2))
        y0 = int(max(0, min(p[1] - 3 * p[2] for p in pts) - 2))
        x1 = int(min(frame.size[0], max(p[0] + 3 * p[2] for p in pts) + 2))
        y1 = int(min(frame.size[1], max(p[1] + 3 * p[2] for p in pts) + 2))
        if x1 <= x0 or y1 <= y0:
            return frame
        ov = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ox, oy, r, a in pts:
            ox, oy = ox - x0, oy - y0
            d.ellipse([ox - r * 2.2, oy - r * 2.2, ox + r * 2.2, oy + r * 2.2], fill=(255, 190, 90, a // 4))
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(255, 226, 140, a))
        frame.alpha_composite(ov, dest=(x0, y0))
        return frame
    return fx


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[0], ctx.lines[1], ctx.lines[2]
    cue = Cues(ctx)

    # ---- timing, all from the narration
    t_rise = L0.start + 0.02                               # '于是' the crew get up
    t_grab = cue.at("他们", L0.start + 0.7) + 0.12          # the lifters crouch and take hold of Jonah
    t_grab = max(t_grab, t_rise + 0.75)
    t_lift = max(cue.at("抬起来", L0.start + 1.8) - 0.12, t_grab + 0.5)   # ...hoist him overhead
    t_up = t_lift + 0.34
    t_heave0 = max(cue.at("扔进", L0.start + 2.6) - 0.3, t_up + 0.2)      # dip...
    t_launch = t_heave0 + 0.52                             # ...and heave him over the stern
    t_watch = t_launch + 0.42
    t_impact = t_launch + 0.72                             # '大海'
    # '于是': the crew get up one after another, lifters first (each: upright kneel -> one knee -> standing, held
    # 4 frames per drawing), with the camera still; once they are all up a lightning flash; then the camera pulls out
    rise_at = dict(s1=0.0, s2=0.17, s0=0.34, s3=0.51, capt=0.68)
    RISE_STEP = 0.13
    t_risen = t_rise + rise_at["capt"] + RISE_STEP         # (the captain stands in one step, see rising())
    t_flash = max(t_grab, t_risen) + 0.1
    t_calm0 = L1.start                                     # '一下子'
    t_calm1 = t_calm0 + 1.1                                # '海就平静了'
    t_awe = max(cue.at("海就", t_calm0 + 0.6) + 0.15, t_watch + 0.6)
    t_wind = cue.at("风停了", L1.start + 2.4)                # '风停了'
    t_still = cue.at("浪也", L1.start + 3.3)                 # '浪也静了'
    # the dip through the blank page in the pause after line 1
    t_d0 = L1.end + 0.06
    t_c1 = t_d0 + 0.45                                     # the page fully covers the ship
    t_c3 = max(t_c1 + 0.35, L2.start - 0.1)                # the deck fully revealed
    t_c2 = max(t_c1 + 0.04, t_c3 - 0.5)                    # ...starting here
    t_sw = (t_c1 + t_c2) / 2                               # shot A -> shot B under the blank page
    c2a, c2b = L2.chunks[0], L2.chunks[-1]
    t_see2 = max(c2a.start + 0.55, t_c3 + 0.2)             # sailor 0 lifts his hands in wonder
    t_kn = max(cue.at("心里", c2a.start + 1.7), t_see2 + 0.9)   # '心里对耶和华又敬又怕' they kneel one by one
    t_off0 = c2b.start + 0.15                              # '他们向耶和华' the captain lifts the bowl
    t_pour = max(cue.at("献上", c2b.start + 1.6, snap=False) - 0.05, t_off0 + 0.6)   # '献上祭物' he pours
    t_flare = t_pour + 0.22
    t_cdown = t_pour + 0.75                                # he sets the empty bowl down, looks up
    t_look = t_flare + 0.25                                # the others raise their heads to the smoke
    lk = [t_look + 0.08 * i for i in range(4)]             # look up: S2, S0, S3, S1
    t_vow = max(cue.at("还许", c2b.end - 1.5) + 0.05, lk[-1] + 0.6, t_cdown + 0.5)   # '还许下了诺言'

    def storm(t):          # 1 = full storm, 0 = calm
        return 1 - progress(t, t_calm0, t_calm1, "inout")

    def storm_fast(t):     # storm crests / banks: gone before the blue sky dominates
        return 1 - progress(t, t_calm0, t_calm0 + 0.6, "sine")

    def stillness(t):      # '浪也静了': the last swell settles
        return progress(t, t_still, t_still + 1.3, "sine")

    def a_only(m):
        return lambda t: m(t) if t < t_sw else Tf(alpha=0.0)

    def b_only(m=None):
        def f(t):
            if t < t_sw:
                return Tf(alpha=0.0)
            return m(t) if m else Tf()
        return f

    # ================================================================ shot A
    def rock(t):           # s08 ends with its rocking eased: start there, build up to the full storm by '他们'
        return (0.05 + 0.13 * (1 - stillness(t)) + 0.82 * storm(t)) * lerp(0.4, 1.0, progress(t, 0.7, 2.0, "sine"))

    def ship_tf(t):
        a = rock(t)
        return Tf(dx=8 * a * math.sin(2 * math.pi * t / 3.1), dy=12 * a * math.sin(2 * math.pi * t / 2.2 + 0.6),
                  rot=4.2 * a * math.sin(2 * math.pi * t / 2.6), px=SX, py=WL)

    heave = M.keys([(t_heave0, {"dy": 0}), (t_heave0 + 0.24, {"dy": 14}), (t_launch, {"dy": -34}),
                    (t_launch + 0.35, {"dy": 0})], ["inout", "out", "inout"])

    def lifter_dy(t):
        return 0.45 * heave(t).dy

    # the hoist is a hard cut (crouched grip -> arms up, Jonah on their hands) sold by a push-up: the lifters' new
    # drawings start 24 px low and rise home with a little overshoot, Jonah riding on their hands (same offset; their
    # feet are hidden behind the bulwark)
    hoist_offs = [(t_lift, 24.0, 0.24, "back")]

    def carried_m(t):      # rides on the lifters' hands; pushed off them by the heave
        s = ship_tf(t)
        return Tf(dx=s.dx, dy=s.dy + lifter_dy(t) + offset_dy(t, hoist_offs) + 0.55 * min(0.0, heave(t).dy),
                  rot=s.rot, alpha=float(t_lift <= t < t_launch), px=SX, py=WL)

    # the calm-weather background is completely covered by the storm overlays until the calm: skip it till then
    def under_storm(t):
        return Tf(alpha=progress(t, t_calm0 - 0.9, t_calm0, "sine"))
    sc.add("a_background", a_background(), z=0, wc=0.8, motion=a_only(under_storm))
    # the sun emerges at full size from behind the clearing cloud: its disc sits (opaque, never scaled) behind the
    # storm sky and the veil cloud from the calm on; the glow fades in round the cloud, and once the storm sky is
    # nearly gone (storm < ~0.1) the cloud drifts off to the right, uncovering the disc (~6.2 -> 7.0 s)
    t_v0, t_v1 = t_calm0 + 0.5, t_calm0 + 1.9
    sc.add("a_sun_glow", a_sun("glow"), z=0.5, wc=0,
           motion=a_only(lambda t: Tf(alpha=progress(t, t_calm0 + 0.45, t_calm0 + 1.4, "sine"))))
    sc.add("a_sun", a_sun("disc"), z=0.6, wc=0.8, motion=a_only(lambda t: Tf(alpha=float(t >= t_calm0 - 0.1))))

    def veil_m(t):         # (its layer is added last, after shot B, so every other layer keeps its watercolour seed)
        return Tf(dx=VEIL_DX * progress(t, t_v0, t_v1, "sine") + 6 * (t - t_calm0), alpha=float(t >= t_calm0 - 0.1))
    sc.add("a_shafts", V.light_shafts(), z=1, wc=0, motion=a_only(under_storm))
    sc.add("a_clouds", V.clouds_clear(), z=2,
           motion=a_only(M.combine(M.visible(t_calm0 + 0.55, fade=0.45), M.drift(vx=6, t0=t_calm0))))
    sc.add("a_sunbeams", V.sunbeams(), z=3, wc=0,
           motion=a_only(lambda t: Tf(alpha=progress(t, t_calm0 + 0.6, t_calm1 + 0.5, "sine") *
                                      (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.7)))))
    t_gull = t_wind - 0.3
    gull_frames = [doc(PR.gull(1900, 470, 0.55, -1, wing=w) + PR.gull(2030, 540, 0.45, -1, wing=-w * 0.8))
                   for w in (1.0, 0.0, -1.0, 0.0)]
    sc.add("a_gulls", gull_frames, z=4,
           motion=a_only(M.combine(M.drift(vx=-110, vy=-8, t0=t_gull), M.visible(t_gull, fade=0.5))),
           frame_at=lambda t: float(int(t * 7) % 4))
    sc.add("a_storm", V.storm_overlay(), z=5, motion=a_only(lambda t: Tf(alpha=storm(t))))
    for side in (-1, 1):
        sc.add(f"a_storm_bank{side}", V.storm_bank(side), z=6,
               motion=a_only(lambda t, s=side: Tf(dx=s * 1250 * progress(t, t_calm0 - 0.1, t_calm0 + 0.65, "sine") +
                                                  s * 8 * math.sin(t * 1.3), alpha=storm_fast(t))))
    # s08's prayer light as it ends (its opening ~0.82 opaque, shafts ~0.83), fading as they get up
    def prayer_m(t):
        return Tf(alpha=0.83 * (1 - progress(t, t_rise, t_rise + 1.3, "sine")))
    sc.add("a_prayer_gap", a_prayer_light("gap"), z=6.6, wc=0, motion=a_only(prayer_m))
    sc.add("a_prayer_through", a_prayer_light("through"), z=6.7, wc=0, blend="screen", motion=a_only(prayer_m))
    sc.add("a_prayer_rays", a_prayer_light("rays"), z=12.6, wc=0, blend="screen", motion=a_only(prayer_m))

    # pennant: whipping in the storm; at '风停了' it sags (in-betweens) and hangs slack behind the yard and sail,
    # swaying slowly by rotation about its root (composed with the ship's rocking)
    t_slack = t_wind + 0.36

    def pen_idx(t):
        if t < t_wind:
            return float(int(t * 11) % 4)
        if t < t_slack:
            return 4.0 + min(2.0, float(int((t - t_wind) / 0.12)))
        return 7.0

    def pen_m(t):
        s = ship_tf(t)
        r2 = 4.0 * math.sin(2 * math.pi * (t - t_slack) / 3.4) * progress(t, t_slack, t_slack + 1.2, "sine")
        th = math.radians(s.rot)
        qx, qy = PEN[0] - SX, PEN[1] - WL
        px_ = SX + qx * math.cos(th) - qy * math.sin(th) + s.dx
        py_ = WL + qx * math.sin(th) + qy * math.cos(th) + s.dy
        return Tf(dx=px_ - PEN[0], dy=py_ - PEN[1], rot=s.rot + r2, px=PEN[0], py=PEN[1])
    sc.add("a_pennant", pennant_frames(), z=9.9, motion=a_only(pen_m), frame_at=pen_idx)

    # wind marks blowing across the sky toward the bow: strong in the storm, a breeze after the calm, gone at '风停了'
    def wind_k(t):
        return (0.55 + 0.45 * storm(t)) * (1 - progress(t, t_wind - 0.1, t_wind + 0.45, "sine"))

    swirls = [(0, 1500, 300, 0.0, 1.3), (1, 900, 470, 0.37, 1.05), (2, 1900, 560, 0.62, 1.15), (0, 400, 210, 0.81, 1.0),
              (1, 1200, 170, 0.2, 1.1)]
    span = 2400.0
    for i, (kind, x0, y0, ph, sc_) in enumerate(swirls):
        def sw_m(t, x0=x0, y0=y0, ph=ph, sc_=sc_, i=i):
            k = wind_k(t)
            if k <= 0.003:
                return Tf(alpha=0.0)
            u = (t * (0.32 + 0.1 * storm(t)) + ph) % 1.0      # position along its path (right -> left)
            x = 2250 - span * u
            env = math.sin(math.pi * u) ** 0.6
            return Tf(dx=x - SWIRL_O[0], dy=y0 - SWIRL_O[1] + 14 * math.sin(t * 2.3 + i), sx=sc_,
                      sy=sc_ * (1 + 0.1 * math.sin(t * 3 + i)), alpha=k * env, px=SWIRL_O[0], py=SWIRL_O[1])
        sc.add(f"a_wind{i}", wind_swirl(kind), z=6.5, wc=0, motion=a_only(sw_m))

    sc.add("a_ship_back", doc(PR.ship(SX, WL, SS, SF, sail="torn", part="back", flag=False)), z=10,
           motion=a_only(ship_tf))
    sc.add("a_jonah_carried", doc(jonah_carried(*JCAR)), z=10.5, motion=a_only(carried_m))

    # ---- the crew: one flipbook layer each (hard cuts; big head-height changes eased, small ones hopped; the rise
    #      cuts also get a quick stretch-and-settle about the feet, starting one frame after the cut so the cut frame
    #      itself shows the new drawing half way, as cut_plan intends)
    def rising(name):      # the captain skips the one-knee drawing (on the curved stern its foot pokes out) and
        tr = t_rise + rise_at[name]   # stands one step after kneeling upright, 4 frames before the lifters' grab
        if name == "capt":
            return [(0, 0), (tr, 1), (tr + RISE_STEP, 3)]
        return [(0, 0), (tr, 1), (tr + RISE_STEP, 2), (tr + 2 * RISE_STEP, 3)]

    f0 = A_F0
    a_specs = {
        "s0": ("s", 0, [(K_LOWUP, S08_EXPR, f0["s0"]), (K_UPR, "worried", 1), (HALF, "worried", 1),
                        (STAND, "worried", 1), (C.POSES["scared"], "scared", 1), (dict(STAND, h=8), "worried", 1),
                        (PRAY, "surprised", 1)],
               rising("s0") + [(t_lift, 4), (t_watch, 5), (t_awe, 6)]),
        "s1": ("s", 1, [(K_LOWUP, S08_EXPR, f0["s1"]), (K_UPR, "worried", 1), (HALF, "worried", 1),
                        (STAND, "worried", 1), (C.POSES["carry"], "worried", 1), (HOIST_POSES["s1"], "worried", 1),
                        (dict(STAND, h=8), "worried", 1), (PRAY, "surprised", 1)],
               rising("s1") + [(t_grab, 4), (t_lift, 5), (t_watch, 6), (t_awe, 7)]),
        "s2": ("s", 2, [(K_LOWUP, S08_EXPR, f0["s2"]), (K_UPR, "worried", -1), (HALF, "worried", -1),
                        (STAND, "worried", -1), (C.POSES["carry"], "worried", -1), (HOIST_POSES["s2"], "worried", 1),
                        (LEAN_LOOK, "worried", 1), (PRAY, "surprised", 1)],
               rising("s2") + [(t_grab, 4), (t_lift, 5), (t_watch, 6), (t_awe, 7)]),
        "s3": ("s", 3, [(K_LOWUP, S08_EXPR, f0["s3"]), (K_UPR, "worried", -1), (HALF, "worried", -1),
                        (STAND, "worried", -1), (C.POSES["scared"], "scared", -1), (LEAN_LOOK, "worried", 1),
                        (DIAG_UP, "surprised", 1)],
               rising("s3") + [(t_lift, 4), (t_watch, 5), (t_awe + 0.08, 6)]),
        "capt": ("capt", None, [(K_LOWUP, S08_EXPR, f0["capt"]), (K_UPR, "worried", -1), (HALF, "worried", -1),
                                (STAND, "worried", -1), (CAPT_SEA, "worried", 1),
                                (LEAN_POINT, "worried", 1), (GAZE, "surprised", 1)],
                 rising("capt") + [(t_lift + 0.06, 4), (t_watch + 0.05, 5), (t_awe + 0.14, 6)]),
    }
    a_heads = {}
    for i, (name, (kind, var, frames, sched)) in enumerate(a_specs.items()):
        x, y = A_POS[name]
        docs, heads = [], []
        for ps, ex, f in frames:
            mk, _, hd = kfig(kind, var, x, y, SS, ps, ex, f)
            docs.append(doc(mk))
            heads.append(hd[1])
        a_heads[name] = heads
        hops, offs = cut_plan(heads, sched, min_dy=10.0)
        lifter = name in ("s1", "s2")
        if lifter:
            offs = [o for o in offs if abs(o[0] - t_lift) > 1e-6] + hoist_offs
        cuts = [tk for tk, _ in rising(name)[1:]]           # the rise cuts stretch and settle

        def person_m(t, hops=hops, offs=offs, lifter=lifter, cuts=cuts, foot=(x, y)):
            s = ship_tf(t)
            dy = -6 * sum(bump(t, c) for c in hops) + offset_dy(t, offs) + (lifter_dy(t) if lifter else 0.0)
            k = sum(stretch(t - c - 1 / 30) for c in cuts)   # from the frame after the cut: follow-through
            if abs(k) < 1e-4:
                return Tf(dx=s.dx, dy=s.dy + dy, rot=s.rot, px=SX, py=WL)
            # stretch / squash about the feet, then the ship's rocking about (SX, WL): one Tf pivoted on the feet
            th = math.radians(s.rot)
            qx, qy = foot[0] - SX, foot[1] - WL
            ex = SX + qx * math.cos(th) - qy * math.sin(th) - foot[0]
            ey = WL + qx * math.sin(th) + qy * math.cos(th) - foot[1]
            return Tf(dx=s.dx + ex, dy=s.dy + dy + ey, rot=s.rot, sx=1 - 0.5 * k, sy=1 + k, px=foot[0], py=foot[1])
        sc.add(f"a_{name}", docs, z=11 + 0.01 * i, motion=a_only(person_m), frame_at=steps(sched))

    jx, jy = A_POS["jon"]
    sc.add("a_jonah_stand", doc(C.jonah(jx, jy, SS, -1, pose="confess")), z=11.5,
           motion=a_only(lambda t: replace(ship_tf(t), dy=ship_tf(t).dy + 4 * bump(t, t_grab),
                                           alpha=float(t < t_lift))))
    sc.add("a_ship_front", doc(PR.ship(SX, WL, SS, SF, sail="torn", part="front")), z=12, motion=a_only(ship_tf))

    # Jonah's flight: launched from the carried centre at the top of the heave, a ballistic arc with a tumble,
    # high enough to clear the heads of sailor 3 and the captain on the stern
    c_l = carried_m(t_launch - 1e-3)
    th = math.radians(c_l.rot)
    rx, ry = JAIR_C[0] - SX, JAIR_C[1] - WL
    p0 = (SX + rx * math.cos(th) - ry * math.sin(th) + c_l.dx,
          WL + rx * math.sin(th) + ry * math.cos(th) + c_l.dy)
    p1 = (SPLASH[0], SPLASH[1] - 6)
    half_h = 125 * JS                                          # Jonah's half height while tumbling (+ margin)
    peak = 230.0
    for name, idx in (("s3", 4), ("capt", 4)):
        hx = A_POS[name][0]
        u = (hx - p0[0]) / (p1[0] - p0[0])
        if 0 < u < 1:
            top = a_heads[name][idx] - 52 * SS                 # top of the head (cap)
            need = lerp(p0[1], p1[1], u) - (top - 26 - half_h)
            peak = max(peak, need / (4 * u * (1 - u)))

    def jonah_air(t):
        if t < t_launch or t >= t_sw:
            return Tf(alpha=0.0)
        u = min(1.0, (t - t_launch) / (t_impact - t_launch))
        x = lerp(p0[0], p1[0], u)
        y = lerp(p0[1], p1[1], u) - 4 * peak * u * (1 - u)
        rot = c_l.rot + 60 * progress(u, 0.1, 1.0, "inout")
        a = 1 - progress(t, t_impact - 0.04, t_impact + 0.06, "linear")
        return Tf(dx=x - JAIR_C[0], dy=y - JAIR_C[1], rot=rot, alpha=a, px=JAIR_C[0], py=JAIR_C[1])

    sc.add("a_jonah_air", doc(S.g(C.jonah(JAIR[0], JAIR[1], JS, 1, pose="fall"),
                                  transform=f"rotate({JAIR_ROT} {JAIR_C[0]:.1f} {JAIR_C[1]:.1f})")),
           z=13, motion=jonah_air)

    def wave_m(storm_layer):
        def m(t):
            a = storm(t)
            f = storm_fast(t)
            amp = a if storm_layer else (0.1 + 0.25 * (1 - stillness(t)) + 0.65 * a)
            return Tf(dx=(46 if storm_layer else 30) * amp * math.sin(2 * math.pi * t / 2.9),
                      dy=(16 if storm_layer else 5) * amp * math.sin(2 * math.pi * t / 1.7 + 0.8) +
                      (40 * (1 - f) if storm_layer else 0),
                      alpha=f if storm_layer else (1 - 0.85 * f) * progress(t, t_calm0 - 0.35, t_calm0, "linear"))
        return m

    sc.add("a_waves_calm", V.near_waves(False), z=20, motion=a_only(wave_m(False)))
    sc.add("a_waves_storm", V.near_waves(True), z=21, motion=a_only(wave_m(True)))

    px_, py_ = SPLASH[0], SPLASH[1] + 10
    sc.add("a_ripples", V.ripples(), z=22, motion=a_only(M.keys(
        [(t_impact + 0.15, {"sx": 0.3, "sy": 0.3, "alpha": 0}), (t_impact + 0.35, {"alpha": 0.9}),
         (t_impact + 3.4, {"sx": 1.45, "sy": 1.45, "alpha": 0})], ["out", "sine"], pivot=(px_, py_))))
    sc.add("a_splash", V.splash_crown(), z=23, motion=a_only(M.keys(
        [(t_impact - 0.04, {"sx": 0.6, "sy": 0.15, "alpha": 0}), (t_impact + 0.02, {"alpha": 1}),
         (t_impact + 0.2, {"sx": 1.0, "sy": 1.0}), (t_impact + 0.75, {"sx": 1.15, "sy": 0.55, "alpha": 0.8}),
         (t_impact + 1.05, {"sx": 1.2, "sy": 0.3, "alpha": 0})], ["out", "out", "in", "linear"], pivot=(px_, py_))))
    sc.add("a_drops", V.splash_drops(), z=24, motion=a_only(M.keys(
        [(t_impact, {"s": 0.25, "alpha": 0, "dy": 0}), (t_impact + 0.06, {"alpha": 1}),
         (t_impact + 0.5, {"s": 1.05, "dy": -10}), (t_impact + 0.95, {"s": 1.25, "dy": 70, "alpha": 0})],
        ["out", "linear", "in"], pivot=(px_, py_))))

    # ================================================================ shot B (appears from the blank page)
    sc.add("b_background", b_background(), z=100, wc=0.85, motion=b_only())
    sc.add("b_cloud", b_clouds(True), z=101, motion=b_only(M.drift(vx=9)))
    sc.add("b_sea_lines", b_sea_lines(0), z=102, wc=0,
           motion=b_only(lambda t: Tf(dx=22 * math.sin(2 * math.pi * t / 7.0), alpha=0.85)))
    sc.add("b_glints", [b_glints(k) for k in range(4)], z=103, wc=0, motion=b_only(),
           frame_at=lambda t: float(int(t * 2.6) % 4))

    # gulls gliding across the sky (left of the light)
    gb = [doc(PR.gull(1500, 470, 0.5, -1, wing=w) + PR.gull(1630, 520, 0.42, -1, wing=-w * 0.8))
          for w in (1.0, 0.5, 0.0, -0.5, -1.0, -0.5, 0.0, 0.5)]
    t_gb = t_sw
    sc.add("b_gulls", gb, z=104, motion=b_only(lambda t: Tf(dx=-96 * (t - t_gb), dy=-9 * (t - t_gb) +
                                                         10 * math.sin(t * 0.9))),
           frame_at=lambda t: float(int(t * 8) % 8) if (t // 3) % 2 == 0 else 2.0)

    # the perched gull on the rail turns its head once while they gaze, once in the final hold (hop)
    g_turns = [t_see2 + 0.5, t_vow + 1.0]
    sc.add("b_gull_perch", [doc(PR.gull(GULL_B[0], GULL_B[1], 0.62, f, pose="stand")) for f in (-1, 1)], z=106,
           motion=b_only(lambda t: Tf(dy=-9 * sum(bump(t, g, 0.09) for g in g_turns))),
           frame_at=lambda t: float(sum(t >= g for g in g_turns) % 2))

    # God's presence: the light through the cloud break glows and pulses gently; at the vows it swells and the
    # rays brighten
    def vow_k(t):
        return progress(t, t_vow - 0.2, t_vow + 1.3, "sine")
    sc.add("b_gap_glow", b_gap_through(), z=107, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=min(1.0, 0.6 + 0.1 * math.sin(2 * math.pi * t / 3.7) + 0.3 * vow_k(t)),
                                      sx=1 + 0.03 * math.sin(2 * math.pi * t / 3.7) + 0.08 * vow_k(t),
                                      sy=1 + 0.03 * math.sin(2 * math.pi * t / 3.7) + 0.08 * vow_k(t),
                                      px=GAP[0], py=GAP[1])))
    sc.add("b_rays", b_rays(), z=107.5, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=(0.62 + 0.38 * vow_k(t)) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 3.1)))))

    # ---- crew
    def b_motion(pos, hops, offs, phase):
        x, y, s = pos

        def m(t):
            br = 1 + 0.011 * math.sin(2 * math.pi * (t / 3.3 + phase))
            dy = -7 * sum(bump(t, c) for c in hops) + offset_dy(t, offs)
            return Tf(dy=dy, sx=br, sy=br, px=x, py=y)
        return b_only(m)

    kn = [t_kn + 0.04 + 0.3 * i for i in range(5)]      # kneel order: captain, S0, S2, S3, S1
    vw = [t_vow + 0.13 * i for i in range(5)]           # vows: captain, S2, S0, S3, S1
    HOLD_HALF = 0.13                                    # the one-knee in-between (4 frames)
    sur = "surprised"

    def add_b(name, kind, var, pos, poses, sched, z, phase):
        docs, heads, _ = b_frames(kind, var, pos, poses)
        hops, offs = cut_plan(heads, sched)
        sc.add(name, docs, z=z, motion=b_motion(pos, hops, offs, phase), frame_at=steps(sched))

    # back row
    add_b("b_s1", "s", 1, B_S1, [(GAZE, sur, None), (HALF, "sorry", None), (P_BOW, "sorry", None),
                                 (P_UP, "peaceful", None), (P_VOW, "happy", None)],
          [(0, 0), (kn[4], 1), (kn[4] + HOLD_HALF, 2), (lk[3], 3), (vw[4], 4)], 110, 0.1)
    add_b("b_s0", "s", 0, B_S0, [(GAZE, sur, None), (PRAY, sur, None), (HALF, "peaceful", None),
                                 (P_BOW, "peaceful", None), (P_UP, "peaceful", None), (P_VOW, "peaceful", None)],
          [(0, 0), (t_see2, 1), (kn[1], 2), (kn[1] + HOLD_HALF, 3), (lk[1], 4), (vw[2], 5)], 111, 0.45)

    # ---- the brazier, flame, glow, smoke
    sc.add("b_brazier", brazier(), z=112, motion=b_only())

    def flame_k(t):        # size of the fire: small, flares when the offering goes in, settles a little bigger
        return 0.72 + 0.62 * progress(t, t_flare, t_flare + 0.22, "out") - \
            0.3 * progress(t, t_flare + 0.3, t_flare + 1.6, "sine")

    def flame_m(t):
        k = flame_k(t)
        fl = math.sin(t * 13.0) * 0.5 + math.sin(t * 7.3 + 1) * 0.5
        kx = 1 + 0.35 * (k - 0.72)
        return Tf(sx=0.8 * kx * (1 + 0.03 * fl), sy=k * (1 + 0.06 * fl), px=FLAME_B[0], py=FLAME_B[1] + 4)
    sc.add("b_flame", [flame(i) for i in range(6)], z=113, wc=0.5, motion=b_only(flame_m),
           frame_at=lambda t: float(int(t * 9) % 6))

    capt_poses = [(GAZE, sur, None), (HALF, "peaceful", None), (P_BOW, "peaceful", None),
                  (P_OFFER, "peaceful", "bowl"), (P_POUR, "peaceful", "pour"), (P_UP, "peaceful", "down"),
                  (P_VOW_LOW, "peaceful", "down")]
    add_b("b_capt", "capt", None, B_CAPT, capt_poses,
          [(0, 0), (kn[0], 1), (kn[0] + HOLD_HALF, 2), (t_off0, 3), (t_pour, 4), (t_cdown, 5), (vw[0], 6)], 114, 0.7)
    # grain pouring from the tipped bowl's lip into the coals (only while the bowl is tipped)
    _, hands, _ = kfig("capt", None, *B_CAPT, P_POUR, "peaceful")
    sk = B_CAPT[2]
    hx, hy = (hands[0][0] + hands[1][0]) / 2 + 4 * sk, min(hands[0][1], hands[1][1]) - 22 * sk
    at = math.radians(POUR_TILT)
    lip = (hx + 34 * sk * 0.95 * math.cos(at), hy + 34 * sk * 0.95 * math.sin(at))
    t_grain1 = min(t_pour + 0.8, t_cdown - 0.04, vw[0] - 0.05)
    sc.add("b_grain", [grains(k, lip) for k in range(3)], z=114.5,
           motion=b_only(lambda t: Tf(alpha=float(t_pour + 0.04 <= t < t_grain1))),
           frame_at=lambda t: float(int(t * 10) % 3))
    sc.add("b_glow", glow(), z=115, wc=0, blend="screen",
           motion=b_only(lambda t: Tf(alpha=min(1.0, (0.5 + 0.08 * math.sin(t * 9.1)) * flame_k(t)),
                                      sx=0.8 + 0.3 * flame_k(t), sy=0.8 + 0.3 * flame_k(t),
                                      px=FLAME_B[0], py=FLAME_B[1] - 40)))

    # smoke: a picture-book chain of puffs climbing beside the light (12 drawings at 8 fps, hard cuts, the puffs
    # move ~3 px per drawing), thicker after the offering; one golden billow climbs it at the flare
    def smoke_k(t):
        return progress(t, t_flare, t_flare + 0.9, "sine")

    NPH = 12
    sc.add("b_smoke", [smoke_column(k / NPH) for k in range(NPH)], z=116, wc=0.3,
           motion=b_only(lambda t: Tf(sx=0.92 + 0.14 * smoke_k(t), sy=0.94 + 0.08 * smoke_k(t),
                                      px=SMOKE_O[0], py=SMOKE_O[1])),
           frame_at=lambda t: float(int(t * 8) % NPH))

    def billow_m(t):       # climbs the column, grows, fades well below the clouds
        u = (t - t_flare + 0.05) / 2.6
        if u <= 0 or u >= 1:
            return Tf(alpha=0.0)
        s = 0.4 + 1.1 * u ** 0.7
        env = min(1.0, u / 0.08) * (1 - progress(u, 0.4, 1.0, "sine"))
        x, y = smoke_xy(min(1.0, 0.95 * u ** 0.8))
        return Tf(dx=x - SMOKE_O[0], dy=y - SMOKE_O[1], rot=-10 * u, sx=s, sy=s, alpha=env,
                  px=SMOKE_O[0], py=SMOKE_O[1])
    sc.add("b_billow", smoke_billow(), z=116.5, wc=0.3, motion=b_only(billow_m))

    # ---- front row
    add_b("b_s2", "s", 2, B_S2, [(GAZE, sur, None), (HALF, "peaceful", None), (P_BOW, "peaceful", None),
                                 (P_UP, "peaceful", None), (P_VOW, "happy", None)],
          [(0, 0), (kn[2], 1), (kn[2] + HOLD_HALF, 2), (lk[0], 3), (vw[1], 4)], 120, 0.25)
    add_b("b_s3", "s", 3, B_S3, [(GAZE, sur, None), (DIAG_UP, sur, None), (HALF, "sorry", None),
                                 (P_BOW, "sorry", None), (P_UP, "peaceful", None), (P_VOW, "peaceful", None)],
          [(0, 0), (t_see2 + 0.35, 1), (kn[3], 2), (kn[3] + HOLD_HALF, 3), (lk[2], 4), (vw[3], 5)], 121, 0.6)
    sc.add("b_fore", b_foreground(), z=130, motion=b_only())
    sc.add("a_sun_veil", a_sun_veil(), z=2.5, motion=a_only(veil_m))     # shot A: the cloud in front of the sun

    # ================================================================ camera
    # A: s08's end framing -> (after the rise and the lightning) eases out to the v1 wide shot before the launch ->
    #    holds -> pushes in on the ship and keeps pushing while the page covers it.
    # B: starts moving, drifts right / in, stops before the dissolve.
    A0 = (1000.0, 590.0, 1700.0)
    A1 = (945.0, 634.0, 1560.0)
    C08 = (CAM_S08.x, CAM_S08.y, CAM_S08.w)
    # held on s08's end framing all through the 1.0 s incoming dissolve, the crew's rise and the lightning; then
    # one slow pull-out (zoom ~19 %/s at its peak) that has settled before the launch
    t_ca0 = max(1.0, t_flash + 0.3)
    t_ca1 = max(t_ca0 + 1.5, t_launch - 0.05)
    t_p0 = t_still - 0.2
    vd = [1.4 * (A1[i] - A0[i]) / max(0.5, t_d0 - t_p0) for i in range(3)]
    cam_a = [hermite([(0.0, C08[i], 0.0), (t_ca0, C08[i], 0.0), (t_ca1, A0[i], 0.0), (t_p0, A0[i], 0.0),
                      (t_d0, A1[i], vd[i])]) for i in range(3)]
    # B1: the area where s10's sinking Jonah appears in the outgoing dissolve (output x 1040-1310, y 330-650)
    # holds only sea and sky - between the captain's head / S0's hands and the brazier and smoke
    B0 = (1185.0, 668.0, 1600.0)
    B1 = (1110.0, 600.0, 1640.0)
    tE = min(T - 1.0, c2b.end + 0.3)
    vb = [0.8 * (B1[i] - B0[i]) / (tE - t_sw) for i in range(3)]
    cam_b = [hermite([(t_sw, B0[i], vb[i]), (tE, B1[i], 0.0)]) for i in range(3)]

    def camera(t):
        if t < t_sw:
            a = storm(t) * progress(t, 0.8, 2.0, "sine")       # no camera sway while s08 dissolves in
            x, y, w = (f(t) for f in cam_a)
            return Cam(x + 6 * a * math.sin(2 * math.pi * t / 3.3), y + 7 * a * math.sin(2 * math.pi * t / 2.4),
                       w, 0.45 * a * math.sin(2 * math.pi * t / 2.9))
        return Cam(*(f(t) for f in cam_b))
    sc.camera = camera

    # ================================================================ effects
    def card(t):           # the blank page between the shots
        return min(progress(t, t_d0, t_c1, "sine"), 1 - progress(t, t_c2, t_c3, "sine"))

    sc.fx = [
        FX.lightning([t_flash], strength=0.22),
        FX.rain(t0=-1, t1=t_calm0 + 0.45, density=0.85, angle=16, alpha=105),
        V.bubble_fx([(lambda t: (SPLASH[0], WL + 110), t_impact + 0.03, t_impact + 0.45, 60, 170, (6, 18), 70, 210)]),
        # '浪也静了': glints on the flat sea (away from the ship), gone under the page
        FX.sparkles((1260, 720, 2050, 870), count=16, t0=t_still, t1=t_sw, color=(255, 250, 226),
                    size=(5, 11), period=1.2, drift=0, seed=31),
        # deck: dust motes in the rays, sparks at the flare, sparkles in the cloud break (a few all along, more
        # at the vows)
        FX.motes((800, 360, 1800, 1000), count=34, t0=t_sw, color=(255, 244, 206), size=(2.5, 5.5), alpha=120,
                 seed=17),
        sparks_fx((FLAME_B[0], FLAME_B[1] - 70), t_flare - 0.05, t_flare + 1.3, 22),
        sparks_fx((FLAME_B[0], FLAME_B[1] - 50), t_sw, T + 1, 1.6, seed=9),
        FX.sparkles((GAP[0] - 200, GAP[1] - 60, GAP[0] + 190, GAP[1] + 150), count=7, t0=t_sw, t1=T + 2,
                    color=(255, 238, 180), size=(5, 11), period=1.9, drift=-4, seed=43),
        FX.sparkles((GAP[0] - 300, GAP[1] - 90, GAP[0] + 230, GAP[1] + 260), count=18, t0=t_vow - 0.1, t1=T + 2,
                    color=(255, 236, 170), size=(7, 16), period=1.6, drift=-6, seed=41),
        FX.tint(PAPER_RGB, card),                         # last: the page covers everything
    ]

    # ================================================================ sound
    sc.sfx("storm_wind", 0, dur=t_wind + 0.2, gain_db=-14, fade_in=0.8, fade_out=1.6)
    sc.sfx("rain", 0, dur=t_calm0 + 0.6, gain_db=-16, fade_in=0.8, fade_out=0.6)
    sc.sfx("waves_storm", 0, dur=t_calm1 + 0.3, gain_db=-12, fade_in=0.8, fade_out=1.5)
    sc.sfx("ship_creak", 0, dur=t_calm1, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_rise + 0.02, gain_db=-17, pan=-0.1)
    sc.sfx("thunder", t_flash - 0.02, gain_db=-18, pan=-0.3)
    sc.sfx("cloth", t_grab - 0.05, gain_db=-15, pan=0.0)
    sc.sfx("cloth", t_lift - 0.05, gain_db=-12, pan=0.05)
    sc.sfx("whoosh", t_launch + 0.02, gain_db=-11, pan=0.3)
    # the impact: 0.02 s before t_impact, i.e. on the frame where he hits the water (audio/picture.py reads the
    # score's hit point back as this cue + 0.02 s); ducked only 3 dB under the narration so it lands
    sc.sfx("splash", t_impact - 0.02, gain_db=-8, pan=0.4, duck_db=-3)
    sc.sfx("bubbles", t_impact + 0.08, dur=0.9, gain_db=-17, pan=0.4, fade_out=0.4)
    sc.sfx("waves_calm", t_calm0 - 0.2, dur=T - t_calm0 + 1.0, gain_db=-14, fade_in=0.9, fade_out=0.8)
    sc.sfx("chime", t_calm0 + 0.3, gain_db=-15)
    sc.sfx("gull", t_gull + 0.4, gain_db=-18, pan=0.5)
    sc.sfx("fire", t_sw, dur=T - t_sw + 0.8, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("fire", t_flare - 0.05, dur=2.4, gain_db=-12, fade_in=0.1, fade_out=1.4)
    sc.sfx("cloth", kn[0] - 0.05, gain_db=-17)
    sc.sfx("cloth", kn[3] - 0.05, gain_db=-18)
    sc.sfx("sparkle", t_flare - 0.02, gain_db=-14, pan=0.3)
    sc.sfx("chime", t_vow, gain_db=-14, pan=0.4)
    return sc
