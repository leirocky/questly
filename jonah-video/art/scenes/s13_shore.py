"""Scene 13 (v2) — the great fish spits Jonah out onto dry land (Jonah 2:10).

Adapted from the approved v1 shore scene (art/scenes_v1/s08_shore.py): the same sunny beach painting, fish,
spit arc, landing, gull, crab and particles, on a wider stage (the v1 shore painting is shifted DX px to the
right and open sea is added on the left) so the fish can swim in to the shore first.

Iris-open into the scene: the centre of the first frame is the far fish's sleeping face (closed eye, pink
cheek), its bow wave just right of it, so the growing circle shows the face from its first frames.

  start           the great fish drifts out at sea, back and head above the water (the rest of its body is a
                  teal shape under the surface), eye closed, tail wagging lazily.
  '上帝吩咐'       God speaks (never a figure): the clouds right above the fish part, gold on their inner edges, and
                  warm golden rays pour down from the gap onto the fish's head (the visual language of s02 / s14;
                  the sun stays plain sunshine); a gold glow and top rim light settle on it (one pulse on '吩咐'),
                  sparkles twinkle round it.
  '那条大鱼'       the fish opens its eye with a little hop and gives a nod — and sets off for the shore.
  '大鱼就游到岸边' it swims in (bow wave, wake, spray; the camera pans with it) and on '岸边' surges up out of the
                  water in the shallows (water streams off its back, a ripple ring).
  '张开大嘴'       it opens its mouth wide: Jonah is seen sitting inside, wide-eyed (the fish blinks once).
  '把约拿吐'       a big heave... and on '吐' it spits him out in a spray of water: he somersaults through the air
  '陆地上'         and lands on his bottom on the sand (puff of sand, bounce), dizzy, stars circling his head; the
                  standing gull takes off. The fish closes its mouth with a happy smile, watches him a moment,
                  then ducks under as a big opaque splash erupts; behind it (hard cut, no in-betweens) it is
                  swapped for the turned drawing, which bobs up as the water falls and swims away out to sea.
  '约拿浑身湿漉漉的' the camera moves in first and holds still; he shakes himself like a wet puppy (drops flung off
                  his silhouette, shake arcs by his head) and looks at himself, dripping all over.
  '可是他又看见了太阳' sunlight streams down onto him; on '看见' he opens his arms to the warm sun (hop cut); faint
                  steam rises from his drying robe; the sun pulses on '太阳'.
  '他得救了！'      he springs up (rocks forward, squats onto his feet, half-crouch, pushes up: in-between
                  drawings) into a jump with his arms raised, golden sparkles round him; once he has landed, far
                  out at sea the fish's tail waves goodbye and sinks gently.
  end             calm hold: Jonah in the sunshine, waves lapping, palms swaying.

Pose changes are hard cuts hidden by a squash-and-hop / shake, or carried by in-between drawings (no
crossfaded doubles). All times are keyed to the narration chunks (word_t() estimates a phrase's time inside
its chunk).
"""
import math

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s08_shore as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.paths import FPS
from engine.scene import Scene

W, H = 2600, 1188
DX = 480                                   # the v1 shore painting is drawn this much further right
HORIZON = V.HORIZON                        # 472
WATER_Y = V.WATER_Y                        # 786: top of the near water band
SUN = (1460, 188)
FX0, FY0, FS = V.FX0 + DX, 600, V.FS       # (1040, 600, 0.9): the fish resting in the shallows
FDY = FY0 - V.FY0                          # fish-relative v1 layers are shifted by (DX, FDY)
LAND = (V.LAND[0] + DX, V.LAND[1])         # (1764, 955): Jonah's seat on the sand
JS, JS_MOUTH = V.JS, V.JS_MOUTH
GULL0 = (V.GULL0[0] + DX, V.GULL0[1])
CRAB0 = (V.CRAB0[0] + DX, V.CRAB0[1])
RIPPLE = (V.RIPPLE[0] + DX, V.RIPPLE[1])
FAR = (700.0, 560.0, 0.5)                  # the fish out at sea at the start: anchor x, y and absolute scale
YW_SWIM = 10.0                             # waterline (fish-local px) while swimming: the mouth at the surface
YW_REST = (WATER_Y - FY0) / FS             # ~207: the near water band's top when resting at the shore
VEIL_BOX = (236, 170, 1604, 994)           # pinned crop of the underwater veil layer (reference placement)
FISH_BOX = (240, 160, 1610, 990)           # pinned crop of the fish_back layer (encloses every fish frame)
SEAT_IN = (400.0, 186.0)                   # Jonah's seat inside the open mouth, on the tongue (fish-local px)
JS_SIT_IN = 0.8                            # ... and his scale there
HEAD_L = (330.0, -150.0)                   # the fish's head / eye region (fish-local px)
JONAH_X = LAND[0]
# God's light comes from a gap in the clouds above the fish (as in s02_call / s14_again), never from the sun
CLOUD_VX = 12.0                            # all clouds drift right this fast (px/s)
CL = (760, 160, 300, 80, 21)               # the parting cloud pair (cx, cy, w, h, seed), touching at rest
CR = (1045, 150, 290, 78, 22)
PART_L, PART_R = -80.0, 105.0              # how far each cloud moves aside when they part
GAP = (910.0, 150.0)                       # middle of the gap once parted (at rest, before the drift)
RAY_SRC = (GAP[0], GAP[1] - 40)            # the rays start just inside the gap (behind the cloud edges)
RAY_TGT = (885.0, 485.0)                   # ...and end on the far fish's head (rays layer drifts with the clouds)
TURN_DIP = 300.0                           # how far the fish ducks under behind the turn splash (stage px)
TURN_BACK, TURN_OUT = 120.0, 60.0          # ...backing off from the shore as it ducks; the turned one further out

# In-between drawings for springing up from sitting (sit_happy -> arms_up) on '他得救了': he rocks forward
# drawing his feet in (lean_a, lean_b), rises onto them in a deep squat (squat_up) and a forward-leaning
# half-crouch (crouch_up) and pushes up (push_up), arms swinging higher each drawing. Built with the library's
# own pose record and figure rig (same design as C.jonah), but kept local to this scene so the shared character
# library (and every other scene's render) stays unchanged.
GETUP_POSES = {
    "lean_a": C._P(t=4, h=-8, legs=(("ik", 92, 1), ("ik", 100, 1)), arms=(("fk", 122, 148), ("fk", -116, -143)),
                   hands=("open", "open"), expr="happy", **C._SEATED),
    "lean_b": C._P(t=20, h=-10, legs=(("ik", 62, 1), ("ik", 70, 1)), arms=(("fk", 128, 152), ("fk", -122, -147)),
                   hands=("open", "open"), expr="happy", **C._SEATED),
    "squat_up": C._P(t=26, h=-12, drop=56, legs=(("ik", 52, 1), ("ik", 18, 1)),
                     arms=(("fk", 132, 154), ("fk", -126, -149)), hands=("open", "open"), expr="happy"),
    "crouch_up": C._P(t=14, h=-8, drop=28, legs=(("ik", 40, 1), ("ik", -14, 1)),
                      arms=(("fk", 136, 156), ("fk", -130, -152)), hands=("open", "open"), expr="happy"),
    "push_up": C._P(t=6, h=-8, drop=10, legs=(("ik", 22, 1), ("ik", -8, 1)),
                    arms=(("fk", 144, 163), ("fk", -140, -160)), hands=("open", "open"), expr="happy"),
}
STANDING_GETUP = ("squat_up", "crouch_up", "push_up")


def jonah_fig(x, y, scale=1.0, facing=1, pose="stand", expr=None, wet=False, marks=True):
    """C.jonah(), plus this scene's get-up in-betweens (GETUP_POSES). Works with C.body_points()."""
    if pose not in GETUP_POSES:
        return C.jonah(x, y, scale, facing, pose=pose, expr=expr, wet=wet, marks=marks)
    ps = dict(GETUP_POSES[pose])
    inner, _ = C._figure(C._jonah_design(wet), C._ADULT, ps, expr or ps["expr"], 1 if facing >= 0 else -1, marks)
    return C._wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


def shifted(v1doc, dx=DX, dy=0.0, under="", extra_defs=""):
    """Re-wrap a v1 layer document (2112 wide) into this stage, translated by (dx, dy). ``under`` is markup
    drawn below it, untransformed."""
    i, j = v1doc.index("<defs>") + 6, v1doc.index("</defs>")
    defs, body = v1doc[i:j], v1doc[j + 7:v1doc.rindex("</svg>")]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}{extra_defs}</defs>{under}<g transform="translate({dx},{dy})">{body}</g></svg>')


def chunk_of(line, phrase):
    for c in line.chunks:
        if phrase in c.text:
            return c
    return line


def word_t(line, phrase, k=0.0):
    """Approximate time a phrase is spoken: its chunk's start + its character offset (plus k of its length)
    as a fraction of the chunk text, times the chunk duration."""
    c = chunk_of(line, phrase)
    txt = c.text.rstrip("。，！？：；、")
    if phrase not in txt:
        return c.start
    i = txt.index(phrase) + k * len(phrase)
    return c.start + (c.end - c.start) * i / max(1, len(txt))


def bump(t, t0, t1):
    """0 -> 1 -> 0 (sine) between t0 and t1."""
    if t <= t0 or t >= t1:
        return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0))


# ============================================================================ painting


def sky():
    defs = (S.lin_grad("s13sky", [(0, "#6fb6dc"), (0.45, "#9dd2e8"), (0.85, "#d2ecef"), (1, "#e9f5ec")]) +
            S.rad_grad("s13sunglow", [(0, "#fff8da", 1), (0.25, "#fff1c2", 0.75), (0.6, "#fde9b4", 0.25),
                                      (1, "#fde9b4", 0)]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 60}" fill="url(#s13sky)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="470" fill="url(#s13sunglow)"/>'
    b += S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="86" fill="{P["sun"]}" '
             f'stroke="{S.shade(P["sun_hot"], -0.15)}" stroke-width="4"/>'
             f'<circle cx="{SUN[0] - 24}" cy="{SUN[1] - 26}" r="34" fill="#fde49a" opacity="0.8"/>',
             filter="wobble")
    return doc(b, defs)


def sun_rays():
    """The sun's soft ray crown (rotates slowly; pulses when Jonah sees the sun)."""
    b = S.g(f'<path d="{S.rays(SUN[0], SUN[1], 106, 228, n=14, width_deg=9, rot=8)}" fill="#fff3c8" '
            f'opacity="0.72"/>'
            f'<path d="{S.rays(SUN[0], SUN[1], 112, 236, n=7, width_deg=4, rot=34)}" fill="#fff6d8" '
            f'opacity="0.45"/>', filter="wobble")
    return doc(b)


def clouds():
    sh = "#d9e6ee"
    b = (S.cloud(390, 172, 320, 96, "#fbf6ec", seed=11, sw=3, shade_fill=sh) +
         S.cloud(1960, 130, 330, 100, "#fbf6ec", seed=13, sw=3, shade_fill=sh) +
         S.cloud(60, 330, 260, 80, "#fbf6ec", seed=14, sw=3, shade_fill=sh) +
         S.cloud(2480, 268, 200, 64, "#fbf6ec", seed=16, sw=3, shade_fill=sh) +
         S.cloud(2120, 262, 220, 70, "#fbf6ec", seed=15, sw=3, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def cloud_one(item):
    """One cloud of the parting pair (same look as clouds())."""
    cx, cy, w, h, seed = item
    return doc(S.g(S.cloud(cx, cy, w, h, "#fbf6ec", seed=seed, sw=3, shade_fill="#d9e6ee"), filter="wobble"))


def cloud_rim(item, gx, gy, rx, ry, uid):
    """Soft gold light on the inner edge of a parting cloud, masked to the cloud's own silhouette (the s14_again
    / v1 s09 technique)."""
    cx, cy, w, h, seed = item
    sil = S.cloud(cx, cy, w, h, "#ffffff", seed=seed, sw=0)
    defs = (f'<mask id="s13rm{uid}" maskUnits="userSpaceOnUse" x="0" y="-100" width="{W}" height="500">'
            f'<g filter="url(#wobble)">{sil}</g></mask>'
            + S.rad_grad(f"s13rg{uid}", [(0, "#f8cc66", 0.95), (0.55, "#f2b848", 0.55), (1, "#f2b848", 0)]))
    return doc(f'<g mask="url(#s13rm{uid})"><ellipse cx="{gx}" cy="{gy}" rx="{rx}" ry="{ry}" '
               f'fill="url(#s13rg{uid})"/></g>', defs)


def landscape():
    """v1 coast, beach and grassy bank (shifted), with open sea and wave glints added on the left."""
    defs = S.lin_grad("s13sea", [(0, "#b9e3e2"), (0.1, "#86cbd6"), (0.42, "#55acc5"), (0.75, "#4bb0c3"),
                                 (1, "#5fc3c4")])
    u = f'<rect x="-20" y="{HORIZON}" width="{DX + 60}" height="{H - HORIZON + 20}" fill="url(#s13sea)"/>'
    u += S.g(S.path(f"M-20,{HORIZON} L{DX + 40},{HORIZON}", sw=3), filter="wobble", opacity=0.5)
    # a second tiny far island on the left horizon
    u += S.g(S.path(S.hill(60, 300, HORIZON + 3, 26, seed=27, bottom=HORIZON + 6, bumps=2), fill="#afd3d1",
                    sw=2), filter="wobble", opacity=0.85)
    hl = ""
    for i, (x, y, w) in enumerate([(20, 492, 130), (230, 504, 160), (60, 545, 210), (300, 580, 120),
                                   (10, 640, 230), (250, 690, 180), (40, 760, 240), (300, 820, 140)]):
        hl += S.path(S.wave_line(y, 3 + i % 3, w / 1.6, i + 7, x0=x, x1=x + w), stroke=False,
                     extra=f'stroke="{P["foam"]}" stroke-width="{3 + (y - 480) / 70:.1f}" fill="none" '
                           f'stroke-linecap="round" opacity="0.75"')
    u += S.g(hl, filter="wobble")
    return shifted(V.landscape(), under=u, extra_defs=defs)


def mid_waves():
    """Foam crest lines on the open water behind the fish (moving layer)."""
    b = ""
    for i, (x, y, w) in enumerate([(440, 742, 420), (910, 760, 360), (600, 668, 300), (1240, 690, 260),
                                   (1460, 748, 200), (780, 600, 220), (1640, 612, 110), (-60, 712, 380),
                                   (40, 626, 260), (230, 772, 220), (-20, 560, 200), (330, 540, 150)]):
        b += S.path(S.wave_line(y, 6, w / 2.2, i * 1.7, x0=x, x1=x + w), stroke=False,
                    extra=f'stroke="{P["foam"]}" stroke-width="{5 + (y - 600) / 40:.1f}" fill="none" '
                          f'stroke-linecap="round" opacity="0.8"')
    return doc(S.g(b, filter="wobble"))


CORNER = (1240 + DX, 786)                  # where the near water band's top meets the beach


def _near_top_pts():
    pts = []
    x = -222
    while x <= CORNER[0] - 4:
        pts.append((x, WATER_Y + 8 * math.sin(x / 95.0) + 4 * math.sin(x / 31.0)))
        x += 34
    return pts


def near_water():
    """Water band in front of the fish's belly, running up onto the sand along the shoreline (v1, widened).
    Its top ink line is a separate layer (near_ink); the scallop foam fades out before the shore corner and
    the shoreline lace curls round the corner over the join."""
    defs = S.lin_grad("s13near", [(0, "#62c5c7", 0.8), (0.22, "#52b6c3", 0.94), (1, "#3d9bb7", 1)])
    cx, cy = CORNER
    defs += (f'<linearGradient id="s13scal" gradientUnits="userSpaceOnUse" x1="{cx - 120}" y1="0" x2="{cx - 50}" '
             f'y2="0"><stop offset="0" stop-color="{P["foam"]}" stop-opacity="0.85"/>'
             f'<stop offset="1" stop-color="{P["foam"]}" stop-opacity="0"/></linearGradient>')
    pts = _near_top_pts()
    top = S.smooth_path(pts, closed=False)
    sh = [(905 + DX, 1270), (968 + DX, 1110), (1040 + DX, 985), (1130 + DX, 872), CORNER]
    d = top + f" L{cx},{cy} L{1130 + DX},872 L{1040 + DX},985 L{968 + DX},1110 L{905 + DX},1270 L-222,1270 Z"
    body = S.path(d, fill="url(#s13near)", stroke=False)
    body += S.path(S.smooth_path(sh, closed=False), sw=4)          # ink along the shore side (under the lace)
    foam = f'<path d="{V._scallop_band([p for p in pts if p[0] < cx - 40], 14, 22)}" fill="url(#s13scal)"/>'
    for i, (x, y, w) in enumerate([(40 + DX, 870, 240), (420 + DX, 905, 280), (760 + DX, 858, 190),
                                   (150 + DX, 985, 300), (560 + DX, 1015, 250), (60 + DX, 1100, 260),
                                   (520 + DX, 1135, 230), (-60, 880, 300), (130, 960, 260), (-20, 1060, 280),
                                   (260, 1120, 200)]):
        foam += S.path(S.wave_line(y, 5, w / 2.0, i, x0=x, x1=x + w), stroke=False,
                       extra=f'stroke="#c4ece8" stroke-width="{4 + (y - 850) / 70:.1f}" fill="none" '
                             f'stroke-linecap="round" opacity="0.7"')
    lace = S.smooth_path(sh, closed=False)
    foam += (f'<path d="{lace}" fill="none" stroke="{P["foam"]}" stroke-width="18" stroke-linecap="round" '
             f'opacity="0.92"/>')
    # the lace curls round the corner and runs a little way along the band's top, tapering, over the join
    foam += (f'<path d="M{cx + 4},{cy - 2} Q{cx - 34},{cy + 6} {cx - 92},{cy + 4}" fill="none" '
             f'stroke="{P["foam"]}" stroke-width="15" stroke-linecap="round" opacity="0.9"/>'
             f'<path d="M{cx - 60},{cy + 6} Q{cx - 100},{cy + 9} {cx - 138},{cy + 7}" fill="none" '
             f'stroke="{P["foam"]}" stroke-width="8" stroke-linecap="round" opacity="0.75"/>')
    return doc(S.g(body + foam, filter="wobble"), defs)


def near_ink():
    """The near water band's top ink line (its own layer so it can soften once the fish has gone), fading out
    over the last ~90 px before the shore corner so it never pokes into the shoreline lace."""
    cx = CORNER[0]
    defs = (f'<linearGradient id="s13nink" gradientUnits="userSpaceOnUse" x1="{cx - 150}" y1="0" x2="{cx - 60}" '
            f'y2="0"><stop offset="0" stop-color="{S.INK}" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="{S.INK}" stop-opacity="0"/></linearGradient>')
    pts = [p for p in _near_top_pts() if p[0] < cx - 50]
    b = (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="url(#s13nink)" stroke-width="4" '
         f'stroke-linecap="round" stroke-linejoin="round"/>')
    return doc(S.g(b, filter="wobble"), defs)


def gull_pair(wa, wb):
    return doc(PR.gull(330, 330, 0.4, 1, wing=wa) + PR.gull(470, 392, 0.32, 1, wing=wb))


def gull_far(wa, wb):
    return doc(PR.gull(2330, 318, 0.26, -1, wing=wa) + PR.gull(2440, 360, 0.21, -1, wing=wb))


# ============================================================================ the fish: swimming in


def veil(tail):
    """The fish's silhouette tinted with sea colour (drawn over the fish; the reveal mask keeps only the part
    below the waterline): the submerged body seen through the water."""
    fishm = PR.fish(FX0, FY0, FS, 1, mouth=0.0, eye="open", tail=tail)
    yw = FY0 + FS * YW_SWIM
    defs = ('<filter id="s13white" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            '<feFlood flood-color="#ffffff"/><feComposite in2="SourceAlpha" operator="in"/></filter>'
            f'<mask id="s13vm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<g filter="url(#s13white)">{fishm}</g></mask>'
            f'<linearGradient id="s13vg" gradientUnits="userSpaceOnUse" x1="0" y1="{yw}" x2="0" y2="{yw + 330}">'
            f'<stop offset="0" stop-color="#8fd0da"/><stop offset="0.1" stop-color="#7ac5d3"/>'
            f'<stop offset="1" stop-color="#55abc4"/></linearGradient>')
    x0, y0, x1, y1 = VEIL_BOX
    b = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#s13vg)" mask="url(#s13vm)" ' \
        f'opacity="0.93"/>'
    # pins: fix the layer's crop box so the waterline maps to a known reveal fraction
    b += (f'<rect x="{x0}" y="{y0}" width="2" height="2" fill="#6fbdd0" opacity="0.03"/>'
          f'<rect x="{x1 - 2}" y="{y1 - 2}" width="2" height="2" fill="#6fbdd0" opacity="0.03"/>')
    return doc(b, defs)


def wake(seed):
    """Foam along the waterline of the swimming fish, a curling bow wave at the snout, ripples on the water over
    its submerged body and a trail of foam behind the tail (reference placement; it moves with the fish, which
    is drawn ~0.55x this size while far out)."""
    rng = np.random.default_rng(seed)
    yw = FY0 + FS * YW_SWIM
    xs, xe = FX0 + FS * -720, FX0 + FS * 612
    # pale water lit just under the surface, and ripple lines over the submerged body
    b = (f'<path d="M{xs - 30:.0f},{yw + 16:.0f} L{xe + 20:.0f},{yw + 16:.0f}" stroke="#e6f6f2" stroke-width="30" '
         f'stroke-linecap="round" opacity="0.32"/>')
    for i, (dy_, x0f, x1f, sw_, op) in enumerate(((52, 0.12, 0.8, 7, 0.6), (108, 0.25, 0.7, 6, 0.5),
                                                  (160, 0.35, 0.62, 5, 0.38))):
        x0_, x1_ = lerp(xs, xe, x0f), lerp(xs, xe, x1f)
        b += S.path(S.wave_line(yw + dy_, 5, 70, i + seed, x0=x0_, x1=x1_), stroke=False,
                    extra=f'stroke="#dff3f0" stroke-width="{sw_}" fill="none" stroke-linecap="round" '
                          f'opacity="{op}"')
    # broken foam: clumps along the waterline, bigger toward the head, with gaps
    blobs = []
    x = xs + 10
    while x < xe - 60:
        k = (x - xs) / (xe - xs)
        n = int(rng.integers(3, 6))
        for j in range(n):
            r = (8 + 11 * k ** 1.3) * rng.uniform(0.7, 1.3)
            blobs.append((x, yw - r * rng.uniform(0.0, 0.55) + rng.uniform(-3, 3), r))
            x += r * rng.uniform(0.9, 1.4)
        x += rng.uniform(18, 46) * (1.2 - 0.6 * k)
    # bow: a heaped mound of foam pushed up against the snout
    bx = xe
    for dx_, dy_, r in ((-70, -6, 20), (-40, -18, 26), (-8, -30, 30), (26, -24, 27), (52, -8, 22), (76, 6, 15),
                        (-20, -2, 24), (14, 2, 22), (44, 8, 16), (8, -50, 17), (-26, -40, 15), (38, -44, 13)):
        blobs.append((bx + dx_, yw + dy_, r * rng.uniform(0.9, 1.1)))
    c = "".join(f'<circle cx="{a:.1f}" cy="{b_:.1f}" r="{r:.1f}"/>' for a, b_, r in blobs)
    b += f'<g fill="{P["foam"]}" stroke="{S.INK}" stroke-width="6.5">{c}</g><g fill="{P["foam"]}">{c}</g>'
    b += "".join(f'<circle cx="{a - r * 0.3:.1f}" cy="{b_ - r * 0.35:.1f}" r="{r * 0.28:.1f}" fill="#ffffff" '
                 f'opacity="0.6"/>' for a, b_, r in blobs[::3])
    # spray thrown up and ahead of the bow
    cx, cy = bx + 30, yw - 40
    for dx_, dy_, r, ang in ((70, -40, 8, -40), (98, -6, 6.5, -20), (40, -74, 6.5, -65), (118, -48, 5, -35),
                             (14, -92, 5, -80), (84, -84, 4.5, -55)):
        b += S.path(V._teardrop(cx + dx_, cy + dy_, r, ang), fill="#d8f2ef", sw=3)
    # wake trail behind the tail: foam streaks on the water, fading to the left
    tx = xs - 20
    for i, (dx_, dy_, w_, op) in enumerate(((0, 4, 160, 0.9), (-150, -8, 190, 0.75), (-80, 22, 170, 0.7),
                                           (-320, 6, 210, 0.5), (-260, 30, 150, 0.45), (-470, -4, 200, 0.3))):
        x0_ = tx + dx_ - w_
        b += S.path(S.wave_line(yw + dy_, 4, w_ / 2.2, i + seed, x0=x0_, x1=x0_ + w_), stroke=False,
                    extra=f'stroke="{P["foam"]}" stroke-width="{9 - i:.1f}" fill="none" '
                          f'stroke-linecap="round" opacity="{op}"')
    return doc(S.g(b, filter="wobble-fine"))


def god_rays(src, head):
    """God's light: warm rays pouring down from the gap in the clouds and ending on the far fish's head, a glow
    in the gap itself and a halo round the head. Drawn below the parting clouds, so the rays come out from
    between them."""
    sx, sy = src
    hx, hy = head
    a0 = math.degrees(math.atan2(hy - sy, hx - sx))
    dist = math.hypot(hx - sx, hy - sy)
    b = ""
    for da, wdt, k in ((-20, 4.5, 0.88), (-10, 6.0, 1.0), (0, 7.5, 1.08), (10, 5.5, 1.0), (19.5, 4.0, 0.88)):
        r0, r1 = 30, dist * k + 40
        p0, p1 = math.radians(a0 + da - wdt / 2), math.radians(a0 + da + wdt / 2)
        pts = [(sx + r0 * math.cos(p0), sy + r0 * math.sin(p0)),
               (sx + r1 * math.cos(p0 - 0.03), sy + r1 * math.sin(p0 - 0.03)),
               (sx + r1 * math.cos(p1 + 0.03), sy + r1 * math.sin(p1 + 0.03)),
               (sx + r0 * math.cos(p1), sy + r0 * math.sin(p1))]
        b += f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="url(#s13ray)"/>'
    defs = (f'<linearGradient id="s13ray" gradientUnits="userSpaceOnUse" x1="{sx}" y1="{sy}" '
            f'x2="{hx}" y2="{hy}"><stop offset="0" stop-color="#fff4c4" stop-opacity="0.95"/>'
            f'<stop offset="0.5" stop-color="#ffe48a" stop-opacity="0.75"/>'
            f'<stop offset="0.88" stop-color="#ffe08a" stop-opacity="0.45"/>'
            f'<stop offset="1" stop-color="#ffe08a" stop-opacity="0.15"/></linearGradient>')
    defs += S.rad_grad("s13halo", [(0, "#fff2b8", 0.75), (0.45, "#ffe9a0", 0.35), (1, "#ffe9a0", 0)])
    defs += S.rad_grad("s13gap", [(0, "#fff6d0", 0.95), (0.5, "#ffe9a8", 0.5), (1, "#ffe9a8", 0)])
    glow = (f'<ellipse cx="{sx}" cy="{sy + 50}" rx="170" ry="120" fill="url(#s13gap)"/>'
            f'<ellipse cx="{hx - 10}" cy="{hy - 20}" rx="300" ry="230" fill="url(#s13halo)"/>')
    return doc(S.g(b, filter="soft") + glow, defs)


def head_rim():
    """Gold rim light along the top edges of the fish's head, back and dorsal fin, lit from the cloud gap
    right above it (adapted from v1 head_rim(), whose light came from the upper left): the silhouette minus
    itself shifted down, softened, kept inside the silhouette, faded out away from the head."""
    hx, hy = FX0 + HEAD_L[0], FY0 + HEAD_L[1]
    fishm = PR.fish(FX0, FY0, FS, 1, mouth=0.0, eye="open", tail=0.0)
    defs = ('<filter id="s13rim" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            '<feOffset in="SourceAlpha" dx="5" dy="26" result="o"/>'
            '<feComposite in="SourceAlpha" in2="o" operator="out" result="r"/>'
            '<feGaussianBlur in="r" stdDeviation="6" result="rb"/>'
            '<feComposite in="rb" in2="SourceAlpha" operator="in" result="ri"/>'
            '<feFlood flood-color="#fff4c4"/>'
            '<feComposite in2="ri" operator="in"/></filter>' +
            S.rad_grad("s13rimfade", [(0, "#ffffff", 1), (0.55, "#ffffff", 0.85), (1, "#ffffff", 0)]) +
            f'<mask id="s13rimmask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<ellipse cx="{hx - 60}" cy="{hy - 40}" rx="520" ry="380" fill="url(#s13rimfade)"/></mask>')
    return doc(f'<g mask="url(#s13rimmask)"><g filter="url(#s13rim)">{fishm}</g></g>', defs)


def sun_beam(target):
    """Sunlight streaming down onto Jonah: a soft fan of warm rays from the sun to the target point."""
    hx, hy = target
    a0 = math.degrees(math.atan2(hy - SUN[1], hx - SUN[0]))
    dist = math.hypot(hx - SUN[0], hy - SUN[1])
    b = ""
    for da, wdt, k in ((-7, 3.0, 1.05), (-2.5, 5.0, 1.12), (3, 3.5, 1.08), (7.5, 2.6, 1.0)):
        r0, r1 = 110, dist * k
        p0, p1 = math.radians(a0 + da - wdt / 2), math.radians(a0 + da + wdt / 2)
        pts = [(SUN[0] + r0 * math.cos(p0), SUN[1] + r0 * math.sin(p0)),
               (SUN[0] + r1 * math.cos(p0 - 0.03), SUN[1] + r1 * math.sin(p0 - 0.03)),
               (SUN[0] + r1 * math.cos(p1 + 0.03), SUN[1] + r1 * math.sin(p1 + 0.03)),
               (SUN[0] + r0 * math.cos(p1), SUN[1] + r0 * math.sin(p1))]
        b += f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)} Z" fill="url(#s13beam)"/>'
    defs = (f'<linearGradient id="s13beam" gradientUnits="userSpaceOnUse" x1="{SUN[0]}" y1="{SUN[1]}" '
            f'x2="{hx}" y2="{hy}"><stop offset="0" stop-color="#fff6d0" stop-opacity="0.85"/>'
            f'<stop offset="0.6" stop-color="#ffeaa6" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#ffe7a0" stop-opacity="0.12"/></linearGradient>')
    return doc(S.g(b, filter="blur-md"), defs)


def warm_pool():
    """Warm sunlight on Jonah and the sand round him (additive)."""
    x, y = LAND[0] - 10, LAND[1] - 40
    defs = S.rad_grad("s13pool", [(0, "#3a2e12", 1), (0.5, "#2c220c", 0.6), (1, "#201806", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="330" ry="190" fill="url(#s13pool)"/>', defs)


def steam(emitters):
    """Soft warm wisps of steam rising from the given points (his head-cloth and shoulders) as he dries in the
    sun: wide, well-blurred strokes, so they read as vapour rather than scratches."""
    b = ""
    for i, (x, y, h_) in enumerate(emitters):
        ph = 1.7 * i
        pts = [(x + 9 * math.sin(ph + k * 1.4) * (0.4 + 0.6 * k / 4), y - h_ * k / 4) for k in range(5)]
        b += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="#fffaf0" stroke-width="13" '
              f'stroke-linecap="round" opacity="0.85"/>')
    return doc(f'<g filter="url(#s13stm)">{b}</g>',
               '<filter id="s13stm" x="-80%" y="-50%" width="260%" height="200%"><feGaussianBlur stdDeviation="5"/>'
               '</filter>')


def tongue_mound(seat):
    """The back of the fish's tongue rising under Jonah inside the open mouth (stage px at the reference fish
    placement; drawn inside the mouth clip), with a soft contact shadow under his seat. Continues the props
    tongue (#e48a8c), whose own top dips below the waterline just left of his seat."""
    loc = [(300, 182), (340, 186), (380, 185), (420, 186), (465, 192), (510, 206), (560, 236)]
    top = [PR.local_to_stage(FX0, FY0, FS, 1, *p) for p in loc]
    low = [PR.local_to_stage(FX0, FY0, FS, 1, *p) for p in ((600, 360), (280, 360), (290, 240))]
    tc = "#e48a8c"
    d = S.smooth_path(top, closed=False) + "".join(f" L{x:.1f},{y:.1f}" for x, y in low) + " Z"
    b = f'<path d="{d}" fill="{tc}"/>'
    b += (f'<path d="{S.smooth_path(top[1:], closed=False)}" fill="none" stroke="{S.INK}" stroke-width="3.2" '
          f'stroke-linecap="round"/>')
    hx, hy = PR.local_to_stage(FX0, FY0, FS, 1, 455, 200)
    b += f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="34" ry="6" fill="{S.shade(tc, 0.35)}" opacity="0.6"/>'
    b += (f'<ellipse cx="{seat[0] - 6:.1f}" cy="{seat[1] + 3:.1f}" rx="66" ry="9" fill="#5a1a24" opacity="0.4"/>')
    return S.g(b, filter="wobble-fine")


TS_Y = WATER_Y + 10                        # base line of the turn splash
TS_CX = 910.0                              # ...and its middle (pivot), over the ducked fish's dorsal fin
# The turn splash: a dome of water (the core, shaped to hide all of the ducked fish the camera sees at the swap,
# both drawings) with two lobed sheets of thrown-up water in front of it, lobes fanning outward (x, top y, lean)
TS_CORE = [(486, TS_Y + 4), (522, 700), (600, 652), (690, 602), (760, 512), (830, 462), (905, 438), (985, 446),
           (1050, 482), (1115, 535), (1200, 568), (1300, 578), (1385, 600), (1450, 668), (1490, TS_Y + 4)]
TS_BACK = [(566, 636, -44), (668, 566, -38), (772, 462, -26), (875, 384, -10), (978, 392, 10), (1082, 462, 26),
           (1188, 524, 36), (1292, 536, 42), (1394, 582, 44), (1462, 672, 36)]
TS_FRONT = [(604, 692, -42), (718, 616, -32), (842, 546, -14), (962, 548, 4), (1082, 596, 22), (1206, 636, 34),
            (1330, 652, 40), (1430, 708, 36)]


def _sheet(lobes, y0, k_valley):
    """A water sheet: rounded lobes (leaning outward) joined by valleys at k_valley of the lower neighbour's
    height, tapering down to the base line at both ends. Returns (closed fill path, open outline path: the
    outline has no ink along the base)."""
    x0, top0, lean0 = lobes[0]
    w0 = 26 + 0.07 * (y0 - top0)
    pts = [(x0 + lean0 - w0 * 1.7, y0 + 2)]
    for i, (x, top, lean) in enumerate(lobes):
        h = y0 - top
        w = 26 + 0.07 * h                       # rounded crown: two shoulders either side of the tip
        tx = x + lean
        pts += [(tx - w * 1.05, top + w * 0.55), (tx - w * 0.2, top + 1), (tx + w * 0.55, top + w * 0.3),
                (tx + w * 1.0, top + w * 0.95)]
        if i + 1 < len(lobes):
            x2, top2, lean2 = lobes[i + 1]
            pts.append(((tx + x2 + lean2) / 2, y0 - min(h, y0 - top2) * k_valley))
    x1, top1, lean1 = lobes[-1]
    pts.append((x1 + lean1 + (26 + 0.07 * (y0 - top1)) * 1.7, y0 + 2))
    line = S.smooth_path(pts, closed=False)
    return line + " Z", line


def _drop(x, y, r, ang):
    """A plump water drop of radius r at (x, y), its short tail trailing opposite the flight angle (deg)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tx, ty = x - ux * r * 1.9, y - uy * r * 1.9
    return (f"M{tx:.1f},{ty:.1f} Q{x - ux * r * 0.2 + px * r * 1.45:.1f},{y - uy * r * 0.2 + py * r * 1.45:.1f} "
            f"{x + ux * r:.1f},{y + uy * r:.1f} Q{x - ux * r * 0.2 - px * r * 1.45:.1f},"
            f"{y - uy * r * 0.2 - py * r * 1.45:.1f} {tx:.1f},{ty:.1f} Z")


def turn_splash():
    """The big splash the fish turns behind: a dome of water with two sheets of thrown-up water in front (white
    crests, sea-teal below), lobes fanning outward, white streaks up each lobe and plump drops flying off the
    crests. Opaque everywhere, so it hides the hard cut to the turned fish drawing."""
    y0 = TS_Y

    def vgrad(id_, stops, y1):
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="0" y1="{y1}" x2="0" y2="{y0}">'
                f'{st}</linearGradient>')

    def shape(fill_d, line_d, fill, sw):
        return (f'<path d="{fill_d}" fill="{fill}"/>'
                f'<path d="{line_d}" fill="none" stroke="{S.INK}" stroke-width="{sw}" stroke-linecap="round" '
                f'stroke-linejoin="round"/>')
    defs = (vgrad("s13tsc", [(0, "#e6f6f2"), (0.35, "#b4e0df"), (1, "#7cc3cc")], 430) +
            vgrad("s13tsb", [(0, "#f4fbf7"), (0.16, "#d3efeb"), (0.5, "#a3d9db"), (1, "#74bfca")], 370) +
            vgrad("s13tsf", [(0, P["foam"]), (0.22, "#e4f5f1"), (0.6, "#b9e3e2"), (1, "#93cfd4")], 530))
    core = S.smooth_path(TS_CORE, closed=False)
    b = shape(core + " Z", core, "url(#s13tsc)", 4)
    b += shape(*_sheet(TS_BACK, y0, 0.74), "url(#s13tsb)", 4.5)
    # streaks of white water up the lobes
    for x, top, lean in TS_BACK:
        h = y0 - top
        b += (f'<path d="M{x - 6:.1f},{y0 - h * 0.3:.1f} Q{x + lean * 0.35 - 14:.1f},{y0 - h * 0.62:.1f} '
              f'{x + lean * 0.8 - 8:.1f},{top + 34 + 0.05 * h:.1f}" stroke="#fbfdf8" stroke-width="{7 + h / 80:.1f}" '
              f'fill="none" stroke-linecap="round" opacity="0.8"/>')
    b += shape(*_sheet(TS_FRONT, y0, 0.7), "url(#s13tsf)", 4)
    for x, top, lean in TS_FRONT[1:-1]:
        h = y0 - top
        b += (f'<path d="M{x + 4:.1f},{y0 - h * 0.18:.1f} Q{x + lean * 0.4:.1f},{y0 - h * 0.55:.1f} '
              f'{x + lean * 0.8 - 4:.1f},{top + 28:.1f}" stroke="#ffffff" stroke-width="7" fill="none" '
              f'stroke-linecap="round" opacity="0.85"/>')
    # plump drops thrown up and outward off the crests
    for k, (x, top, lean) in enumerate(TS_BACK[1:-1]):
        side = -1 if x < TS_CX else 1
        for j, (ox, oy, r) in enumerate(((26, -42, 9), (60, -14, 7))):
            if (k + j) % 2 == 1:
                continue
            x_, y_ = x + lean + side * ox, top + oy
            ang = math.degrees(math.atan2(-1.4, side * (0.35 + abs(x - TS_CX) / 400)))
            b += S.path(_drop(x_, y_, r, ang), fill="#e4f5f2", sw=2.6)
    return doc(S.g(b, filter="wobble"), defs)


def turn_foam():
    """Heaped foam on the water at the foot of the turn splash: ink-edged clumps of puffs, big heaps in the middle
    breaking up into smaller clumps with gaps toward the ends (covers the sheets' feet)."""
    rng = np.random.default_rng(37)
    y0 = TS_Y
    blobs = []
    x = 452.0
    while x < 1556:
        near = max(0.0, 1 - abs(x - TS_CX) / 620)
        n = int(rng.integers(3, 6)) + int(3 * near)
        big = 13 + 26 * near ** 0.7
        for j in range(n):
            u = (j + 0.5) / n
            r = big * (0.55 + 0.6 * math.sin(math.pi * u)) * rng.uniform(0.8, 1.15)
            blobs.append((x, y0 - r * rng.uniform(0.2, 0.75) + rng.uniform(-3, 6), r))
            if j % 2 == 1:                       # a smaller puff in front, lower down
                blobs.append((x - r * 0.5, y0 + 10 + rng.uniform(-3, 3), r * 0.62))
            x += r * rng.uniform(0.75, 1.1)
        x += rng.uniform(4, 10) + 34 * (1 - near) ** 2 * rng.uniform(0.4, 1.0)     # gaps toward the ends
    c = "".join(f'<circle cx="{a:.1f}" cy="{b_:.1f}" r="{r:.1f}"/>' for a, b_, r in blobs)
    b = f'<g fill="{P["foam"]}" stroke="{S.INK}" stroke-width="7">{c}</g><g fill="{P["foam"]}">{c}</g>'
    b += "".join(f'<circle cx="{a - r * 0.3:.1f}" cy="{b_ - r * 0.35:.1f}" r="{r * 0.28:.1f}" fill="#ffffff" '
                 f'opacity="0.65"/>' for a, b_, r in blobs[::3])
    return doc(S.g(b, filter="wobble-fine"))


def tail_wave(tail):
    """Far out at sea the fish's tail sticks up out of the water and waves goodbye (small; clipped at the
    waterline, with a foam ring)."""
    x, y, s = 960, 548, 0.27
    yw = y + 4
    fishm = PR.fish(0, 0, 1.0, 1, mouth=0.0, eye="happy", tail=tail)
    clip = (f'<clipPath id="s13tw"><rect x="{x - 300}" y="{yw - 400}" width="600" height="400"/></clipPath>')
    body = (f'<g clip-path="url(#s13tw)"><g transform="translate({x + 30},{y + 110}) rotate(78) scale({s})">'
            f'{fishm}</g></g>')
    foam = (f'<ellipse cx="{x + 4}" cy="{yw + 2}" rx="46" ry="8" fill="{P["foam"]}" stroke="{S.INK}" '
            f'stroke-width="2.5"/>'
            f'<path d="M{x - 70},{yw + 8} q20,-6 40,0 M{x + 40},{yw + 9} q20,-6 40,0" stroke="{P["foam"]}" '
            f'stroke-width="3" fill="none" stroke-linecap="round"/>')
    return doc(f'<defs>{clip}</defs>' + body + S.g(foam, filter="wobble-fine"))


# ============================================================================ build


CALM = [-0.3, -0.15, 0.0, 0.15, 0.3]
SWIM = [-0.7, -0.35, 0.0, 0.35, 0.7]
WAG = [0, 1, 2, 3, 4, 3, 2, 1]


def fish_frames():
    """(mouth, eye, tail) per flipbook frame."""
    fr = [(0.0, "closed", tl) for tl in CALM]                              # 0-4   drifting, eye closed
    fr += [(0.0, "open", tl) for tl in CALM]                               # 5-9   listening / resting
    fr += [(0.0, "open", tl) for tl in SWIM]                               # 10-14 swimming
    fr += [(k / 8, "open", 0.0) for k in range(1, 9)]                      # 15-22 opening wide
    fr += [(1.0, "closed", 0.0)]                                           # 23    blink (wide open)
    fr += [(m, e, 0.0) for m, e in ((0.9, "surprised"), (0.78, "surprised"), (0.65, "open"), (0.5, "open"),
                                    (0.36, "happy"), (0.22, "happy"), (0.1, "happy"))]   # 24-30 closing
    fr += [(0.0, "happy", tl) for tl in CALM]                              # 31-35 happy, watching
    fr += [(0.0, "happy", tl) for tl in SWIM]                              # 36-40 happy, swimming away
    return fr


F_REST, F_LISTEN, F_SWIM, F_OPEN, F_BLINK, F_CLOSE, F_HAPPY, F_AWAY = 0, 5, 10, 15, 23, 24, 31, 36


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]

    # ---- timing, keyed to the words of the narration
    t_light0 = L0.start                                   # 上帝吩咐… golden rays
    t_pulse = word_t(L0, "吩咐") + 0.1                    # …吩咐: the glow pulses once
    t_wake = word_t(L0, "那条")                           # 那条大鱼: the fish opens its eye (little hop)
    t_nod = word_t(L0, "大鱼")                            # …and nods
    t_swim0 = t_nod + 0.28                                # sets off (still inside the first chunk)
    t_arrive = word_t(L0, "岸边", 0.5)                    # 游到岸边: surges up in the shallows
    t_open0 = word_t(L0, "张开") - 0.08                   # 张开大嘴
    t_open1 = t_open0 + 0.62
    t_spit = word_t(L0, "吐") + 0.1                       # 吐
    t_heave = t_spit - 0.42
    t_blink = (t_open1 + t_heave) / 2 - 0.1
    t_land = max(t_spit + 0.68, word_t(L0, "陆地") + 0.04)  # 陆地上
    t_hop = t_land + 0.30
    t_close0 = t_spit + 0.16
    t_close1 = t_close0 + 7 / FPS
    t_turn0 = max(t_land + 0.8, L0.end + 0.08)            # the fish turns round (behind a splash)...
    t_turn1 = t_turn0 + 0.26
    t_swap = t_turn0 + 0.13                               # hard cut to the turned drawing, at the splash's peak
    t_fall0, t_fall1 = t_swap + 0.04, t_swap + 0.44       # the splash falls back into the water
    t_away = t_turn1 - 0.04                               # ...and swims away
    t_out = t_spit + 0.15                                 # Jonah has cleared the lips
    t_shake = word_t(L1, "浑身") + 0.08                   # 浑身湿漉漉的: shakes himself
    t_shake1 = t_shake + 0.62
    t_cut1 = t_shake + 0.3                                # dizzy -> surprised (inside the shake)
    t_sun0 = L1.at("太阳")                                # 可是他又看见了太阳: sunlight streams onto him
    t_look = word_t(L1, "看见")                           # opens his arms to the sun (hop cut)
    t_sunword = word_t(L1, "太阳")                        # the sun pulses
    t_joy = word_t(L1, "得救") - 0.02                     # 他得救了: springs up, arms raised
    t_tail = min(t_joy + 0.55, T - 1.75)                  # after he lands: the fish's tail waves goodbye

    # ---- painting
    # sky + landscape are consecutive static layers (flattened into one image); the sun's ray crown (kept above
    # the horizon) and the clouds are drawn over them
    sc.add("sky", sky(), z=0, wc=0.6)
    sc.add("landscape", landscape(), z=0.1)
    # the sun is plain sunshine: it only swells a little when Jonah sees it again (God's light comes from the
    # parting clouds above the fish, as in s02 / s14)
    sc.add("sun_rays", sun_rays(), z=0.5, wc=0.4,
           motion=lambda t: Tf(rot=2.0 * t, sx=1 + 0.11 * bump(t, t_sunword - 0.25, t_sunword + 1.2)
                               + 0.05 * progress(t, t_sun0, t_look),
                               sy=1 + 0.11 * bump(t, t_sunword - 0.25, t_sunword + 1.2)
                               + 0.05 * progress(t, t_sun0, t_look),
                               alpha=0.85 + 0.15 * math.sin(2 * math.pi * t / 3.1), px=SUN[0], py=SUN[1]))
    sc.add("clouds", clouds(), z=1, motion=M.drift(vx=CLOUD_VX))
    pal = [shifted(V.palms(s)) for s in (-0.35, 0.0, 0.35)]
    sc.add("palms", pal, z=3, frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.6))

    HEADF = (FAR[0] + 22 * 1.4 + FAR[2] * HEAD_L[0], FAR[1] + FAR[2] * HEAD_L[1])
    t_light1 = t_swim0 + 0.15

    def light_env(t):
        return progress(t, t_light0 + 0.25, t_light0 + 0.6, "sine") * (1 - progress(t, t_light1, t_light1 + 0.9,
                                                                                     "sine"))
    reveal_t1 = t_light0 + 0.75

    # ---- God speaks: the clouds above the fish part (gold on their inner edges) and rays pour down onto it
    def part(t):
        return progress(t, t_light0 - 0.1, t_light0 + 1.1, "inout")
    cl_m = lambda t: Tf(dx=PART_L * part(t) + CLOUD_VX * t)    # noqa: E731
    cr_m = lambda t: Tf(dx=PART_R * part(t) + CLOUD_VX * t)    # noqa: E731
    rim_a = lambda t: Tf(alpha=light_env(t) * (0.9 + 0.1 * math.exp(-((t - t_pulse) / 0.2) ** 2)))   # noqa: E731
    sc.add("cloud_l", cloud_one(CL), z=4.2, motion=cl_m)
    sc.add("cloud_r", cloud_one(CR), z=4.25, motion=cr_m)
    sc.add("rim_l", cloud_rim(CL, CL[0] + 140, CL[1] + 12, 150, 105, "l"), z=4.22, wc=0,
           motion=M.combine(cl_m, rim_a))
    sc.add("rim_r", cloud_rim(CR, CR[0] - 135, CR[1] + 12, 145, 100, "r"), z=4.27, wc=0,
           motion=M.combine(cr_m, rim_a))

    def rays_reveal(t):
        if t >= reveal_t1:
            return {"mode": "down", "frac": 1.0}
        return {"mode": "radial", "frac": progress(t, t_light0, reveal_t1, "out"), "soft": 140,
                "cx": RAY_SRC[0], "cy": RAY_SRC[1]}
    sc.add("god_rays", god_rays(RAY_SRC, RAY_TGT), z=4, wc=0, reveal=rays_reveal,
           motion=lambda t: Tf(dx=CLOUD_VX * t,
                               alpha=(1 - progress(t, t_light1 - 0.1, t_light1 + 0.6, "sine")) * float(t >= t_light0)))
    sc.add("mid_waves", mid_waves(), z=5, wc=0.5, wc_edge=0,
           motion=M.combine(M.bob(5, 3.1), M.bob(14, 4.7, 0.2, axis="x")))
    sc.add("swash", shifted(V.swash()), z=6,
           motion=lambda t: Tf(dx=-9 * math.sin(2 * math.pi * t / 3.4), dy=7 * math.sin(2 * math.pi * t / 3.4),
                               alpha=0.75 + 0.25 * math.sin(2 * math.pi * t / 3.4 + 0.6)))

    gw = [1.0, 0.5, 0.0, -0.5, -1.0]
    GF = [0, 1, 2, 3, 4, 3, 2, 1]
    sc.add("gulls", [gull_pair(w, gw[(i + 2) % 5]) for i, w in enumerate(gw)], z=7,
           motion=M.combine(M.drift(vx=34, vy=-3), M.bob(10, 2.2)), frame_at=lambda t: float(GF[int(t * 9) % 8]))
    sc.add("gulls_far", [gull_far(w, gw[(i + 3) % 5]) for i, w in enumerate(gw)], z=7.1,
           motion=M.combine(M.drift(vx=-38, vy=2), M.bob(7, 2.6, 0.3)),
           frame_at=lambda t: float(GF[int(t * 10 + 3) % 8]))

    # ---- the great fish: path, swim, surge, mouth, heave, spit, close, turn, swim away
    frames = fish_frames()
    open_set = {i for i, f in enumerate(frames) if f[0] > 0}

    def fish_idx(t):
        if t < t_wake:
            return float(F_REST + WAG[int(t * 6) % 8])
        if t < t_swim0 - 0.1:
            return float(F_LISTEN + WAG[int(t * 7) % 8])
        if t < t_arrive + 0.25:
            return float(F_SWIM + WAG[int(t * 12) % 8])
        if t < t_open0:
            return float(F_LISTEN + WAG[int(t * 7) % 8])
        if t < t_close0:
            if t >= t_open1 and t_blink <= t < t_blink + 0.13:
                return float(F_BLINK)
            return float(F_OPEN + min(7, int(8 * progress(t, t_open0, t_open1, "sine"))))
        if t < t_close1:
            return float(F_CLOSE + min(6, int(7 * (t - t_close0) / (t_close1 - t_close0))))
        if t < t_turn0:
            return float(F_HAPPY + WAG[int(t * 7) % 8])
        return float(F_AWAY + WAG[int(t * 11) % 8])

    x_s0 = FAR[0] + 22 * t_swim0

    def fish_pose(t):
        """(anchor x, anchor y, absolute scale x, absolute scale y, rot) of the fish."""
        if t < t_swim0:
            ax, ay, s = FAR[0] + 22 * t, FAR[1], FAR[2]
        else:
            u = progress(t, t_swim0, t_arrive, "inout")
            ax, ay, s = lerp(x_s0, FX0, u), lerp(FAR[1], FY0, u), lerp(FAR[2], FS, u)
        sw = progress(t, t_swim0 - 0.1, t_swim0 + 0.3) * (1 - progress(t, t_arrive - 0.2, t_arrive + 0.3))
        ay += 6 * s * math.sin(2 * math.pi * t / 2.7) * (1 - sw)
        rot = 0.8 * math.sin(2 * math.pi * t / 3.3) + 1.4 * sw * math.sin(2 * math.pi * 1.4 * t)
        ay += 5 * s * sw * math.sin(2 * math.pi * 1.4 * t + 1.2)
        sx = sy = s
        # eye opens: a little hop and stretch; then a nod ("yes!")
        k = bump(t, t_wake - 0.02, t_wake + 0.3)
        ay -= 20 * s * k
        sy *= 1 + 0.03 * k
        sx *= 1 - 0.015 * k
        rot += 5.5 * bump(t, t_nod - 0.05, t_nod + 0.35) - 1.5 * bump(t, t_nod + 0.3, t_nod + 0.55)
        # surge up in the shallows on arrival, with a small forward push
        ay -= 26 * bump(t, t_arrive - 0.3, t_arrive + 0.45)
        ax += 18 * bump(t, t_arrive - 0.2, t_arrive + 0.5)
        rot -= 2.5 * bump(t, t_arrive - 0.3, t_arrive + 0.4)
        # heave before the spit: leans back, cheeks puff, then the spit recoil
        hv = bump(t, t_heave, t_spit - 0.02) ** 0.8
        rot -= 4.5 * hv
        sx *= 1 + 0.07 * hv
        sy *= 1 - 0.05 * hv
        ax -= 14 * hv
        ay += 10 * hv
        if t > t_spit - 0.05:
            k = progress(t, t_spit - 0.05, t_spit + 0.05, "out") * (1 - progress(t, t_spit + 0.08, t_spit + 0.6))
            ax -= 45 * k
            rot -= 4 * k
            sy *= 1 + 0.03 * k
        if t > t_close1:
            w = math.exp(-(t - t_close1) / 0.4) * (1 - progress(t, t_turn0 - 0.1, t_turn0))
            rot += 2.5 * w * math.sin(2 * math.pi * 3.0 * (t - t_close1))
        # the turn: the fish ducks under (squash), backing off from the shore, as a big splash erupts in front of
        # it; behind the splash at its peak (opaque, hiding all of the fish the camera sees) the drawing is
        # swapped for the turned one (mirrored, a little smaller, a little further out): a hard cut, no
        # in-betweens. It bobs part way up as the water falls (stretch), then swims away left, sinking
        if t > t_turn0 - 0.08:
            back = progress(t, t_turn0 - 0.06, t_swap, "inout")
            dip = back * (1 - 0.55 * progress(t, t_fall0 - 0.03, t_fall0 + 0.45, "inout"))
            ay += TURN_DIP * dip
            ax -= TURN_BACK * back + TURN_OUT * float(t >= t_swap)
            q = bump(t, t_turn0 - 0.06, t_swap + 0.01)                  # squash while ducking
            st = bump(t, t_fall0, t_fall0 + 0.5)                        # stretch as it bobs up
            sx *= (1 + 0.05 * q) * (1 - 0.025 * st)
            sy *= (1 - 0.07 * q) * (1 + 0.04 * st)
        if t >= t_swap:
            sx *= -V.AWAY_S
            sy *= V.AWAY_S
        v = max(0.0, t - t_away)
        ax -= 60 * v + 700 * v * v
        ay += 50 * v + 230 * v * v
        rot -= 7 * progress(t, t_away, t_away + 0.8, "sine")
        rot += 1.6 * math.sin(2 * math.pi * 1.6 * v) * progress(t, t_away, t_away + 0.2)
        return ax, ay, sx, sy, rot

    def fish_tf(t):
        ax, ay, sx, sy, rot = fish_pose(t)
        if t > t_away + 1.6:
            return Tf(alpha=0.0)
        return Tf(dx=ax - FX0, dy=ay - FY0, rot=rot, sx=sx / FS, sy=sy / FS, px=FX0, py=FY0)

    def yw_local(t):
        """Waterline on the fish (local px): at the mouth while swimming, down to the near band on arrival."""
        return lerp(YW_SWIM, YW_REST + 4, progress(t, t_arrive - 0.42, t_arrive + 0.22, "inout"))

    # pins: fix fish_back's crop box (FISH_BOX) so its waterline clip maps to a known reveal fraction
    x0_, y0_, x1_, y1_ = FISH_BOX
    pins = (f'<rect x="{x0_}" y="{y0_}" width="2" height="2" fill="#4f8fb0" opacity="0.03"/>'
            f'<rect x="{x1_ - 2}" y="{y1_ - 2}" width="2" height="2" fill="#4f8fb0" opacity="0.03"/>')
    back, front = [], []
    for i, (mo, ey, tl) in enumerate(frames):
        if i in open_set:
            back.append(doc(PR.fish(FX0, FY0, FS, 1, mouth=mo, eye=ey, tail=tl, part="back") + pins))
            front.append(doc(PR.fish(FX0, FY0, FS, 1, mouth=mo, eye=ey, tail=tl, part="front")))
        else:
            back.append(doc(PR.fish(FX0, FY0, FS, 1, mouth=mo, eye=ey, tail=tl) + pins))
            front.append(doc(""))

    def fish_clip(t):
        """From the turn on, the fish is cut off a little below the waterline (the line rises from below the
        fish as it ducks), so its ducked body never shows through the water band: no see-through outlines that
        change at the swap."""
        if t < t_turn0 - 0.08:
            return {"mode": "down", "frac": 1.0}
        f = fish_tf(t)
        y_clip = lerp(FISH_BOX[3] + 40, WATER_Y + 40 + 9 * abs(f.rot), progress(t, t_turn0 - 0.08, t_turn0 + 0.06,
                                                                               "sine"))
        ly = FY0 + (y_clip - FY0 - f.dy) / f.sy
        return {"mode": "down", "frac": (ly - FISH_BOX[1]) / (FISH_BOX[3] - FISH_BOX[1]), "soft": 16}
    sc.add("fish_back", back, z=10, motion=fish_tf, frame_at=fish_idx, reveal=fish_clip)

    # the submerged part of the swimming fish (veil, revealed below the waterline) and its foam
    veils = [veil(tl) for tl in CALM + SWIM]
    t_veil_off = t_arrive + 0.3

    def veil_idx(t):
        i = int(fish_idx(t))
        return float(5 + (i - F_SWIM)) if F_SWIM <= i < F_SWIM + 5 else float(i % 5)

    def veil_reveal(t):
        yw = FY0 + FS * yw_local(t)
        return {"mode": "up", "frac": max(0.0, min(1.0, (VEIL_BOX[3] - yw) / (VEIL_BOX[3] - VEIL_BOX[1]))),
                "soft": 10}
    sc.add("veil", veils, z=10.2, wc=0, motion=lambda t: Tf(alpha=0.0) if t > t_veil_off else fish_tf(t),
           frame_at=veil_idx, reveal=veil_reveal)

    def wake_m(t):
        if t > t_arrive + 0.3:
            return Tf(alpha=0.0)
        f = fish_tf(t)
        d = FS * (yw_local(t) - YW_SWIM)
        r = math.radians(f.rot)
        ox, oy = -math.sin(r) * d * f.sy, math.cos(r) * d * f.sy
        a = (0.8 + 0.2 * progress(t, t_swim0, t_swim0 + 0.5)) * (1 - progress(t, t_arrive - 0.05, t_arrive + 0.3))
        return Tf(dx=f.dx + ox, dy=f.dy + oy, rot=f.rot, sx=f.sx, sy=f.sy, alpha=a, px=f.px, py=f.py)
    sc.add("wake", [wake(s) for s in (1, 2, 3)], z=10.3, wc=0.4, motion=wake_m,
           frame_at=lambda t: float(int(t * 8) % 3))

    # ---- God's light on the fish: glow + rim light above it, moving with it; a pulse on "吩咐"
    def glow_m(peak, pulse):
        def m(t):
            a = light_env(t)
            if a <= 0:
                return Tf(alpha=0.0)
            f = fish_tf(t)
            k = peak + pulse * math.exp(-((t - t_pulse) / 0.16) ** 2)
            return Tf(dx=f.dx, dy=f.dy, rot=f.rot, sx=f.sx, sy=f.sy, alpha=a * k, px=f.px, py=f.py)
        return m
    sc.add("head_glow", shifted(V.head_glow(), DX, FDY), z=10.5, wc=0, motion=glow_m(0.3, 0.1))
    sc.add("head_light", shifted(V.head_light(), DX, FDY), z=10.55, wc=0, blend="add", motion=glow_m(0.8, 0.25))
    sc.add("head_rim", head_rim(), z=10.6, wc=0, motion=glow_m(0.85, 0.15))

    # ---- Jonah: sitting inside the open mouth, spat out, somersaults, lands on the sand
    piv = (LAND[0], LAND[1] - 132 * JS)          # body centre of the 'fall' figure drawn at LAND
    end = (LAND[0] + 4, LAND[1] - 120 * JS)
    ROT0, ROT1 = -312.0, 46.0
    in_centre_l = (SEAT_IN[0] + 8, SEAT_IN[1] - 92)  # centre of the seated figure inside the mouth (local)

    def in_mouth_centre(t):
        f = fish_tf(t)
        rest = PR.local_to_stage(FX0, FY0, FS, 1, *in_centre_l)
        x, y = V.apply(V.tf_matrix(f), rest)
        return (x, y), f.rot

    B0, r0f = in_mouth_centre(t_spit)
    R0, S0 = r0f + ROT0, JS_SIT_IN
    B = [B0, (B0[0] + 330, B0[1] - 120), (end[0] - 40, 40), end]

    def warp(v):
        return 0.62 * (1 - (1 - v) ** 2.2) + 0.38 * v ** 2.4 if v < 1 else 1.0

    def flight(t):
        v = min(1.0, max(0.0, (t - t_spit) / (t_land - t_spit)))
        u = warp(v)
        c = [(1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3]
        x = sum(k * p[0] for k, p in zip(c, B))
        y = sum(k * p[1] for k, p in zip(c, B))
        rot = lerp(R0, ROT1, 0.5 * u + 0.5 * v)
        s = lerp(S0, JS, M.ease("sine")(v))
        return x, y, rot, s

    def hop(t, tc, h, up=0.13, down=0.14, pre=0.09, post=0.14, sq=0.08, sq_pre=None):
        """Squash-and-hop centred on tc (peak). Returns (dy, sx, sy). ``sq_pre`` overrides the take-off squash
        (default ``sq``, same as the landing squash)."""
        dy, sx, sy = 0.0, 1.0, 1.0
        if tc - up - pre <= t < tc - up:
            k = math.sin(math.pi * (t - (tc - up - pre)) / pre)
            q = sq if sq_pre is None else sq_pre
            sx, sy = 1 + q * k, 1 - q * 1.2 * k
        elif tc - up <= t < tc:
            u = (t - (tc - up)) / up
            dy = -h * (1 - (1 - u) ** 2)
            sx, sy = 1 - 0.03 * (1 - u), 1 + 0.05 * (1 - u)
        elif tc <= t < tc + down:
            u = (t - tc) / down
            dy = -h * (1 - u * u)
        elif tc + down <= t < tc + down + post:
            k = math.sin(math.pi * (t - tc - down) / post)
            sx, sy = 1 + sq * k, 1 - sq * 1.2 * k
        return dy, sx, sy

    t_joy_peak = t_joy + 0.2

    def jonah_tf(t):
        if t < t_land:
            x, y, rot, s = flight(t)
            k = s / JS
            sq = 1 + 0.06 * math.sin(t * 30)
            return Tf(dx=x - piv[0], dy=y - piv[1], rot=rot, sx=k, sy=k * sq, px=piv[0], py=piv[1])
        u = t - t_land
        sx = sy = 1.0
        dy = dx_sh = 0.0
        rot = 0.0
        if u < 0.08:
            k = math.sin(math.pi * u / 0.16)
            sx, sy = 1 + 0.16 * k, 1 - 0.2 * k
        elif u < t_hop - t_land:
            v = (u - 0.08) / (t_hop - t_land - 0.08)
            dy = -52 * 4 * v * (1 - v)
            sx, sy = 1 - 0.04 * (1 - v), 1 + 0.06 * (1 - v)
        elif t < t_hop + 0.6:
            w = u - (t_hop - t_land)
            k = math.exp(-w / 0.12) * math.cos(2 * math.pi * w / 0.3)
            sx, sy = 1 + 0.07 * k, 1 - 0.09 * k
        # woozy sway while dizzy
        rot += 3.5 * math.sin(2 * math.pi * (t - t_land) / 1.2) * progress(t, t_land + 0.3, t_land + 0.7) * \
            (1 - progress(t, t_shake - 0.15, t_shake))
        # the wet-puppy shake
        if t_shake <= t < t_shake1:
            v = (t - t_shake) / (t_shake1 - t_shake)
            env = min(1.0, v / 0.12) * (1 - progress(v, 0.6, 1.0, "sine"))
            ph = 2 * math.pi * 5.2 * (t - t_shake)
            rot += 11 * env * math.sin(ph)
            dx_sh = 7 * env * math.sin(ph + 0.6)
            sy *= 1 - 0.04 * env
            sx *= 1 + 0.025 * env
        # sees the sun: a small hop (pose cut at its peak)
        d1, a1, b1 = hop(t, t_look, 18)
        # saved: springs up (rocks forward, half-crouch, push up: in-between drawings, see jonah_idx), then one
        # little joy bounce. The crouch drawing is the take-off anticipation, so its extra squash is small.
        d2, a2, b2 = hop(t, t_joy_peak, 76, up=0.18, down=0.17, pre=0.12, post=0.16, sq=0.1, sq_pre=0.05)
        d3, a3, b3 = hop(t, t_joy_peak + 0.62, 12, up=0.12, down=0.12, pre=0.07, post=0.1, sq=0.04)
        dy += d1 + d2 + d3
        sx *= a1 * a2 * a3
        sy *= b1 * b2 * b3
        # breathing, and a happy little sway at the end
        sy *= 1 + 0.012 * math.sin(2 * math.pi * t / 2.2)
        rot += 1.6 * math.sin(2 * math.pi * (t - t_joy) / 2.4) * progress(t, t_joy_peak + 0.9, t_joy_peak + 1.6)
        return Tf(dx=dx_sh, dy=dy, rot=rot, sx=sx, sy=sy, px=LAND[0], py=LAND[1])

    t_cut_look = t_look                       # at the hop's peak
    t_cut_joy = t_joy_peak - 0.18             # start of the rise
    # springing up: sit_happy -> lean_a (2 frames) -> lean_b (2) -> squat_up (1) -> crouch_up (2) (these two
    # during the take-off squash) -> push_up (1, at take-off) -> arms_up (rising)
    t_lean_a = t_cut_joy - 7 / FPS
    t_lean_b = t_cut_joy - 5 / FPS
    t_squat = t_cut_joy - 3 / FPS
    t_crouch = t_cut_joy - 2 / FPS
    t_stand = t_cut_joy + 1 / FPS

    def jonah_idx(t):
        if t < t_land:
            return 0.0
        if t < t_cut1:
            return 1.0
        if t < t_cut_look:
            return 2.0
        if t < t_lean_a:
            return 3.0
        if t < t_lean_b:
            return 5.0
        if t < t_squat:
            return 6.0
        if t < t_crouch:
            return 7.0
        if t < t_cut_joy:
            return 8.0
        if t < t_stand:
            return 9.0
        return 4.0

    j_fall = C.jonah(LAND[0], LAND[1], JS, -1, pose="fall", expr="surprised", wet=True)
    # indices 0-4 as before; 5-9 are the get-up in-betweens
    J_POSES = [("fall", "surprised"), ("sit", "dizzy"), ("sit", "surprised"), ("sit_happy", "happy"),
               ("arms_up", "happy"), ("lean_a", "happy"), ("lean_b", "happy"), ("squat_up", "happy"),
               ("crouch_up", "happy"), ("push_up", "happy")]
    j_frames = [doc(j_fall)] + [doc(jonah_fig(LAND[0], LAND[1], JS, -1, pose=p, expr=e, wet=True))
                                for p, e in J_POSES[1:]]

    wetpatch = (f'<ellipse cx="{LAND[0] - 15}" cy="{LAND[1] + 6}" rx="150" ry="30" fill="#c99d63" opacity="0.55"/>'
                f'<ellipse cx="{LAND[0] + 95}" cy="{LAND[1] + 16}" rx="30" ry="8" fill="#c99d63" opacity="0.5"/>'
                f'<ellipse cx="{LAND[0] - 160}" cy="{LAND[1] + 14}" rx="22" ry="6" fill="#c99d63" opacity="0.5"/>')
    sc.add("wetpatch", doc(S.g(wetpatch, filter="wobble")), z=15.4,
           motion=lambda t: Tf(alpha=progress(t, t_land, t_land + 0.5, "out") *
                               (1 - 0.35 * progress(t, t_look, T, "sine"))))
    sc.add("shadow", doc(C.ground_shadow(LAND[0] - 10, LAND[1], JS, width=230, opacity=0.25)), z=15.5,
           motion=lambda t: Tf(alpha=progress(t, t_land - 0.25, t_land, "in"),
                               sx=lerp(0.4, 1.0, progress(t, t_land - 0.25, t_land, "in")) *
                               (1 - 0.3 * bump(t, t_joy_peak - 0.18, t_joy_peak + 0.17)),
                               px=LAND[0], py=LAND[1]))

    # Inside the mouth Jonah sits between fish(part='back') and fish(part='front'), clipped by the opening;
    # the layer moves with the fish. One frame per mouth step, then one per video frame while he leaves.
    seat = PR.local_to_stage(FX0, FY0, FS, 1, *SEAT_IN)
    j_sit_in = C.jonah(seat[0], seat[1], JS_SIT_IN, 1, pose="sit", expr="surprised", wet=True)
    tongue = tongue_mound(seat)
    in_frames = [doc(PR.in_fish_mouth(tongue + j_sit_in, FX0, FY0, FS, 1, mouth=k / 8)) for k in range(1, 9)]
    n0 = int(math.ceil(t_spit * FPS - 1e-6))
    n1 = int(math.ceil(t_out * FPS - 1e-6))
    spit_times = [n / FPS for n in range(n0, n1)]
    for tk in spit_times:
        x, y, r, s = flight(tk)
        k = s / JS
        Jm = V.tf_matrix(Tf(dx=x - piv[0], dy=y - piv[1], rot=r, sx=k, sy=k, px=piv[0], py=piv[1]))
        loc = np.linalg.inv(V.tf_matrix(fish_tf(tk))) @ Jm
        fig = f'<g transform="{V.svg_matrix(loc)}">{j_fall}</g>'
        in_frames.append(doc(PR.in_fish_mouth(tongue + fig, FX0, FY0, FS, 1, mouth=1.0)))

    def jin_idx(t):
        if t < t_spit:
            i = int(fish_idx(t))
            return float(7 if i == F_BLINK else max(0, min(7, i - F_OPEN)))
        return float(min(len(in_frames) - 1, 8 + max(0, int(round((t - spit_times[0]) * FPS)))))

    def jin_motion(t):
        """Moves with the fish; while he sits inside he breathes (a ~1.5 px vertical scale about his seat,
        composed with the fish's transform)."""
        if t < t_open0 or t >= t_out:
            return Tf(alpha=0.0)
        f = fish_tf(t)
        if t >= t_spit:
            return f
        sb = 1 + 0.009 * math.sin(2 * math.pi * (t - t_open0) / 1.7)
        r = math.radians(f.rot)
        oy = f.sy * (1 - sb) * (seat[1] - FY0)           # keeps the seat fixed: R S (0, (1 - sb)(seat_y - FY0))
        return Tf(dx=f.dx - math.sin(r) * oy, dy=f.dy + math.cos(r) * oy, rot=f.rot, sx=f.sx, sy=f.sy * sb,
                  alpha=f.alpha, px=f.px, py=f.py)
    sc.add("jonah_in", in_frames, z=12, motion=jin_motion, frame_at=jin_idx)
    sc.add("jonah", j_frames, z=16, motion=lambda t: Tf(alpha=0.0) if t < t_out else jonah_tf(t),
           frame_at=jonah_idx)
    sc.add("fish_front", front, z=13, motion=fish_tf, frame_at=fish_idx)

    near_m = M.combine(M.bob(5, 2.9, 0.1), M.bob(10, 4.1, axis="x"))
    sc.add("near_water", near_water(), z=14, motion=near_m)
    # its top ink line softens once the fish has gone (otherwise it reads like a ledge across the open sea)
    sc.add("near_ink", near_ink(), z=14.05, wc=0.5,
           motion=M.combine(near_m, lambda t: Tf(alpha=1 - 0.6 * progress(t, t_away + 1.3, t_away + 2.4, "sine"))))

    # ripple rings: the arrival surge (at the bow), the spit and the turn
    def ring(tc, k, dx0, dy0=0.0):
        def m(t):
            u = (t - tc) / 1.2
            if u < 0 or u > 1:
                return Tf(alpha=0.0)
            sc_ = lerp(0.5, 1.3, 1 - (1 - u) ** 2) * k
            return Tf(dx=dx0, dy=dy0, sx=sc_, sy=sc_, alpha=math.sin(math.pi * min(1, u * 1.6)) * (1 - u),
                      px=RIPPLE[0], py=RIPPLE[1])
        return m
    rip = shifted(V.ripples())
    sc.add("ripple0", rip, z=14.9, wc=0, motion=ring(t_arrive - 0.05, 1.2, 170, -6))
    sc.add("ripple1", rip, z=15, wc=0, motion=ring(t_spit + 0.02, 1.0, fish_tf(t_spit + 0.02).dx))
    sc.add("ripple2", rip, z=15.05, wc=0, motion=ring(t_turn0 + 0.1, 1.35, TS_CX - RIPPLE[0]))

    # the turn splash: erupts as the fish ducks, is fully up (opaque) a frame before the swap and stays up a few
    # frames after it, then falls back into the water (squashing down onto its foot, never fading while it
    # still stands in front of the fish); the foam at its foot lingers and melts away
    def splash_m(t):
        if t < t_turn0 - 0.03 or t > t_fall1:
            return Tf(alpha=0.0)
        rise = progress(t, t_turn0 - 0.03, t_swap - 0.025, "out")
        fall = progress(t, t_fall0, t_fall1, lambda u: u ** 1.6)
        over = bump(t, t_swap - 0.06, t_fall0 + 0.06)
        return Tf(sx=lerp(0.8, 1.0, rise) * (1 + 0.01 * over) * (1 + 0.1 * fall),
                  sy=max(0.002, lerp(0.1, 1.0, rise) * (1 + 0.03 * over) * (1 - fall)),
                  alpha=1 - progress(fall, 0.85, 1.0, "linear"), px=TS_CX, py=TS_Y)
    sc.add("splash", turn_splash(), z=14.6, wc=0.5, motion=splash_m)

    def foam_m(t):
        if t < t_turn0 - 0.03 or t > t_fall1 + 0.35:
            return Tf(alpha=0.0)
        rise = progress(t, t_turn0 - 0.03, t_swap - 0.04, "out")
        melt = progress(t, t_fall1 - 0.15, t_fall1 + 0.35, "sine")
        return Tf(sx=lerp(0.7, 1.0, rise) * (1 + 0.08 * melt), sy=lerp(0.3, 1.0, rise) * (1 - 0.6 * melt),
                  alpha=1 - melt, px=TS_CX, py=TS_Y + 6)
    sc.add("splash_foam", turn_foam(), z=14.65, wc=0.3, motion=foam_m)

    # sand puffs on landing (+ smaller ones on the bounce)
    def puff(tc, big, side):
        def m(t):
            u = (t - tc) / 0.42
            if u < 0 or u > 1:
                return Tf(alpha=0.0)
            e = 1 - (1 - u) ** 3
            s = lerp(0.35, 1.05, e) * big
            a = 0.55 * min(1.0, u * 8) * (1 - progress(u, 0.25, 1.0, "sine"))
            return Tf(dx=side * (60 if side > 0 else 28) * e * big, dy=-24 * e, sx=s, sy=s, alpha=a,
                      px=LAND[0] + side * 40, py=LAND[1])
        return m
    for i, (tc, big) in enumerate(((t_land, 1.0), (t_hop, 0.6), (t_joy_peak + 0.17, 0.5))):
        for side in (-1, 1):
            sc.add(f"puff{i}{side}", shifted(V.sand_puff(side)), z=16.5 + i * 0.1 + side * 0.01, wc=0,
                   motion=puff(tc, big, side))

    grains = V.ballistic((LAND[0], LAND[1] - 10), t_land, 30, (-165, -15), (250, 650), (1.6, 2.6), (0.3, 0.55),
                         2400, 82, spread=(70, 10))

    def grains_dyn(t):
        pts = list(V.live_particles(grains, t, LAND[1] + 30))
        if not pts:
            return None
        ov = V.Overlay([(p[1], p[2]) for p in pts], 24, w_max=W, h_max=H)
        if not ov.ok:
            return None
        for i, x, y, vx, vy, fr in pts:
            a = 1 - fr ** 3
            r = grains["r"][i]
            ov.polyline([(x - vx * 0.009, y - vy * 0.009), (x, y)], (176, 134, 82, int(150 * a)), 2 * r * 0.8)
            ov.circle(x, y, r, (168, 124, 72, int(235 * a)))
        return ov.image(), (ov.x0, ov.y0)
    sc.add_dynamic("grains", grains_dyn, z=15.9)

    # sunlight on Jonah: a fan of warm rays from the sun, a warm pool of light, steam as he dries
    jtarget = (LAND[0] - 20, LAND[1] - 150)
    beam_t1 = t_sun0 + 1.0

    def beam_reveal(t):
        if t >= beam_t1:
            return {"mode": "down", "frac": 1.0}
        return {"mode": "radial", "frac": progress(t, t_sun0, beam_t1, "out"), "soft": 200,
                "cx": SUN[0], "cy": SUN[1]}
    sc.add("sun_beam", sun_beam(jtarget), z=8, wc=0, reveal=beam_reveal,
           motion=lambda t: Tf(alpha=float(t >= t_sun0) * (0.75 + 0.25 * bump(t, t_sunword - 0.2, t_sunword + 1.3)
                                                           + 0.08 * math.sin(2 * math.pi * t / 2.6))))
    sc.add("warm_pool", warm_pool(), z=16.8, wc=0, blend="add",
           motion=lambda t: Tf(alpha=progress(t, t_sun0 + 0.3, t_look + 0.3, "sine") *
                               (0.85 + 0.15 * bump(t, t_sunword - 0.2, t_sunword + 1.3)
                                + 0.2 * bump(t, t_joy_peak - 0.2, t_joy_peak + 1.4))))

    # steam rises from the top of his head-cloth and his front shoulder (not across the head-cloth flap at the
    # back of his head); it follows him when he springs up
    st_sit = C.body_points(C.jonah, LAND[0], LAND[1], JS, -1, pose="sit_happy", wet=True)
    htx, hty = st_sit["head_top"]
    shx, shy = st_sit["shoulders"][0]
    # where his head top is in each later drawing (arms_up and the get-up in-betweens), relative to sit_happy
    ht_off = {}
    for i, (p, _) in enumerate(J_POSES):
        if i >= 4:
            hx_, hy_ = C.body_points(jonah_fig, LAND[0], LAND[1], JS, -1, pose=p, wet=True)["head_top"]
            ht_off[i] = (hx_ - htx, hy_ - hty)
    sx0, sy0 = htx, hty
    stm_a = steam([(htx - 20, hty + 8, 58), (htx + 24, hty + 12, 50), (shx - 32, shy - 6, 46)])
    stm_b = steam([(htx + 2, hty + 6, 64), (shx - 44, shy - 2, 42)])

    def steam_m(ph):
        def m(t):
            if t < t_look:
                return Tf(alpha=0.0)
            u = ((t - t_look) / 2.6 + ph) % 1.0
            env = progress(t, t_look + 0.2, t_look + 1.2, "sine") * (1 - 0.4 * progress(t, T - 1.5, T, "sine"))
            jt = jonah_tf(t)
            ox, oy = ht_off.get(int(jonah_idx(t)), (0.0, 0.0))
            return Tf(dx=4 * math.sin(2 * math.pi * (u * 1.2 + ph)) + ox,
                      dy=-55 * u + oy + jt.dy,
                      sx=0.85 + 0.3 * u, sy=0.85 + 0.35 * u, alpha=0.9 * env * math.sin(math.pi * u) ** 1.2,
                      px=sx0, py=sy0)
        return m
    sc.add("steam_a", stm_a, z=16.2, wc=0, motion=steam_m(0.0))
    sc.add("steam_b", stm_b, z=16.21, wc=0, motion=steam_m(0.5))

    # far out at sea, the fish's tail waves goodbye
    tw_frames = [tail_wave(v) for v in (-1.0, -0.4, 0.4, 1.0)]
    TWF = [0, 1, 2, 3, 2, 1]

    def tail_m(t):
        if t < t_tail or t > t_tail + 1.3:
            return Tf(alpha=0.0)
        u = t - t_tail
        up = progress(u, 0.0, 0.35, "out") * (1 - progress(u, 0.85, 1.3, "sine"))      # rises, waves, sinks gently
        return Tf(dy=60 * (1 - up), alpha=min(1.0, u / 0.08) * (1 - progress(u, 1.15, 1.3)))
    sc.add("tail_wave", tw_frames, z=5.5, motion=tail_m, frame_at=lambda t: float(TWF[int(t * 9) % 6]))

    # the standing gull takes fright and flies off when Jonah lands
    g_fr = [doc(PR.gull(*GULL0, 0.72, -1, pose="stand"))] + \
        [doc(PR.gull(GULL0[0], GULL0[1] - 40 * 0.72, 0.72, 1, wing=w)) for w in gw]
    t_g = t_land + 0.12

    def gull_idx(t):
        if t < t_g:
            return 0.0
        return 1.0 + GF[int((t - t_g) * 12) % 8]

    def gull_tf(t):
        if t < t_g:
            return Tf(dy=-4 * abs(math.sin(math.pi * t / 0.9)) * progress(t, 0.0, 0.1))
        u = t - t_g
        if u > 2.0:
            return Tf(alpha=0.0)
        return Tf(dx=210 * u + 160 * u * u, dy=-500 * u - 420 * u * u, rot=-16 * min(1, u * 4))

    crab_m = lambda t: Tf(dx=-34 * math.sin(2 * math.pi * t / 5.0), dy=-5 * math.sin(2 * math.pi * t / 5.0))
    sc.add("crab", [doc(V.crab(*CRAB0, 0.52, k)) for k in (0, 1)], z=18, motion=crab_m,
           frame_at=lambda t: float(int(t * 8) % 2))
    sc.add("gull_stand", g_fr, z=18.5, motion=gull_tf, frame_at=gull_idx)
    sc.add("foreground", shifted(V.foreground()), z=19)

    # ---- camera: on the fish out at sea (the iris opens from the frame centre on its sleeping face, the bow
    # wave just right of it; the frame eases back a little while God speaks), pans with it to the shore, holds
    # wide for the spit, then moves in on Jonah for the second line and settles before the dissolve.
    # The push-in happens BEFORE the wet-puppy shake (it is over by t_shake - 0.05) and the frame holds still
    # (a few px of drift) through the shake, so the shake reads clearly; the fish's turn and splash stay on its
    # left side.
    t_push0 = t_land + 0.5
    t_push1 = max(t_push0 + 0.8, t_shake - 0.05)
    t_hold1 = max(t_push1 + 0.3, t_sun0)
    cam = M.cam_keys([(0, Cam(925, 548, 1840)), (t_swim0, Cam(1010, 592, 1920)),
                      (t_arrive + 0.4, Cam(1450, 600, 1960)), (t_spit - 0.3, Cam(1468, 598, 1990)),
                      (t_land + 0.3, Cam(1480, 600, 1985)), (t_push0, Cam(1483, 601, 1981)),
                      (t_push1, Cam(1680, 700, 1680)), (t_hold1, Cam(1686, 702, 1670)),
                      (t_sunword + 0.2, Cam(1642, 606, 1860)), (T, Cam(1638, 603, 1870))],
                     ["sine", "sine", "sine", "sine", "sine", "sine", "linear", "sine", "linear"])
    sc.camera = M.cam_shake(cam, amp=7, t0=t_land, t1=t_land + 0.35, freq=14, seed=5)

    # ---- particles (output space): bow spray, arrival drops, spit spray, turn spray, shake drops, speed
    # lines, dizzy stars, drips
    def fish_pt(t, lx, ly):
        return V.apply(V.tf_matrix(fish_tf(t)), PR.local_to_stage(FX0, FY0, FS, 1, lx, ly))

    bow_sets = []
    te = t_swim0 + 0.15
    k = 0
    while te < t_arrive - 0.1:
        bow_sets.append(V.ballistic(fish_pt(te, 640, YW_SWIM - 6), te, 3, (-85, -25), (160, 420), (2.0, 4.2),
                                    (0.28, 0.42), 1700, 300 + k, spread=(10, 6)))
        te += 0.09
        k += 1
    arr_pts = [fish_pt(t_arrive, lx, YW_REST - 30) for lx in np.linspace(-520, 560, 10)]
    arrive_drops = V.ballistic(arr_pts, t_arrive - 0.12, 36, (-120, -60), (150, 420), (2.2, 5.0), (0.35, 0.6),
                               1800, 91, spread=(30, 10))
    lip_a = PR.local_to_stage(FX0, FY0, FS, 1, *PR.fish_mouth_points(1.0)["upper"])
    lip_b = PR.local_to_stage(FX0, FY0, FS, 1, *PR.fish_mouth_points(1.0)["lower"])
    Fspit = V.tf_matrix(fish_tf(t_spit))
    mouth_line = [V.apply(Fspit, (lerp(lip_a[0], lip_b[0], u), lerp(lip_a[1], lip_b[1], u)))
                  for u in np.linspace(0.12, 0.7, 9)]
    spray = V.ballistic(mouth_line, t_spit - 0.03, 40, (-55, -5), (380, 950), (2.2, 6.0), (0.3, 0.5), 1900, 81,
                        spread=(10, 10))
    turn_line = [(TS_CX + dx, WATER_Y - 6) for dx in np.linspace(-300, 300, 9)]
    turn_spray = V.ballistic(turn_line, t_turn0 + 0.02, 34, (-125, -55), (300, 760), (2.2, 5.5), (0.35, 0.55),
                             1900, 83, spread=(16, 6))
    # drops thrown off the splash's crests at its peak, raining down as it falls
    crest = [(x + lean, top + 24) for x, top, lean in TS_BACK[2:7]]
    crest_drops = V.ballistic(crest, t_swap - 0.03, 24, (-128, -52), (200, 470), (3.0, 6.0), (0.5, 0.8), 1900, 84,
                              spread=(40, 10))
    sets = [(s_, False, WATER_Y + 12) for s_ in bow_sets] + [(arrive_drops, False, WATER_Y + 12),
                                                            (spray, True, WATER_Y + 12),
                                                            (turn_spray, False, WATER_Y + 12),
                                                            (crest_drops, False, WATER_Y + 12)]

    # the wet-puppy shake flings drops off his silhouette edge (head-cloth sides and top, arms, back, hem),
    # outward, in time with the swings (a swing to the right throws drops right, then left...). Drawn as
    # ink-edged teardrops stretched along their flight.
    sp = C.body_points(C.jonah, LAND[0], LAND[1], JS, -1, pose="sit", wet=True)
    jhx, jhy = sp["head"]
    bl, bt, br, bb = sp["bbox"]
    EDGE = {-1: [((jhx - 56, jhy - 2), (-210, -150)), ((jhx - 26, jhy - 46), (-150, -105)),
                 ((bl + 52, jhy + 78), (-205, -150)), ((bl + 18, bb - 30), (-190, -150))],
            1: [((jhx + 58, jhy + 4), (-40, 10)), ((jhx + 28, jhy - 44), (-80, -35)),
                ((br - 18, jhy + 70), (-40, 5)), ((br - 4, bb - 28), (-30, -5))]}
    tear_sets = []
    for k, (dt_, side, n) in enumerate(((0.05, 1, 3), (0.145, -1, 3), (0.24, 1, 3), (0.335, -1, 3),
                                        (0.43, 1, 2))):
        tb = t_shake + dt_
        Jb = V.tf_matrix(jonah_tf(tb))
        for e, (pt, ang) in enumerate(EDGE[side]):
            tear_sets.append(V.ballistic(V.apply(Jb, pt), tb - 0.02, n, ang, (260, 540), (5.0, 9.0), (0.32, 0.5),
                                         1900, 700 + 10 * k + e, spread=(5, 5)))

    def tear_poly(ox, oy, ux, uy, r, ln):
        phi = math.atan2(uy, ux)
        pts = [(ox + r * math.cos(phi + math.radians(-105 + 21 * j)), oy + r * math.sin(phi + math.radians(-105 + 21 * j)))
               for j in range(11)]
        return pts + [(ox - ux * (r + ln), oy - uy * (r + ln))]

    # drips: drops forming and falling from Jonah's beard, hands and hem (pose-dependent emitters)
    def emitters(pose):
        bp = C.body_points(jonah_fig, LAND[0], LAND[1], JS, -1, pose=pose, wet=True)
        hx, hy = bp["head"]
        pts = [(hx - 14 * JS, hy + 44 * JS), bp["hands"][0], bp["hands"][1], bp["feet"][0]]
        if pose == "arms_up" or pose in STANDING_GETUP:      # hands held high: no drips falling past his face
            pts = [(hx - 14 * JS, hy + 44 * JS), (bp["pelvis"][0] - 40, LAND[1] - 30),
                   (bp["pelvis"][0] + 30, LAND[1] - 26), (bp["shoulders"][0][0] - 6, bp["shoulders"][0][1] + 30)]
        return pts
    EMIT = {i: emitters(p) for i, (p, _) in enumerate(J_POSES) if i > 0}
    drip_rng = np.random.default_rng(17)
    drip_per = drip_rng.uniform(0.75, 1.25, 4)
    drip_ph = drip_rng.uniform(0, 1, 4)
    t_drip0 = t_land + 0.5

    def drips(t):
        if t < t_drip0:
            return []
        ji = int(jonah_idx(t))
        Jm = V.tf_matrix(jonah_tf(t))
        out = []
        for e, (ex, ey) in enumerate(EMIT[ji]):
            per = drip_per[e]
            cyc = (t - t_drip0) / per + drip_ph[e]
            n = int(cyc)
            if (n * 7 + e * 3) % 5 == 4:          # skip some cycles
                continue
            if t > t_look and (n + e) % 2 == 1:     # drying in the sun: fewer drips
                continue
            a = (cyc - n) * per
            hang = 0.4 * per
            x, y = V.apply(Jm, (ex, ey))
            if a < hang:
                r = 1.5 + 2.5 * a / hang
                out.append((x, y + r, r, 0.0))
            else:
                fa = a - hang
                yy = y + 4 + 0.5 * 1800 * fa * fa
                if yy > LAND[1] + 8:
                    continue
                out.append((x, yy, 4.0, 1800 * fa))
        return out

    jhead = C.body_points(C.jonah, LAND[0], LAND[1], JS, -1, pose="sit", wet=True)["head_top"]

    def jonah_box(t):
        if t < t_spit or t > t_land + 0.6:
            return None
        if t < t_land:
            x, y, _, s = flight(t)
            r = 125 * s
            return (x - r, y - r, x + r, y + r)
        return (LAND[0] - 130, LAND[1] - 240, LAND[0] + 90, LAND[1] + 10)

    def particles(frame, t, view):
        drops = []
        lip_x = fish_pt(t, 560, 0)[0] if t < t_turn0 else -1e9
        box = jonah_box(t)
        for P_, cull_lip, floor in sets:
            for i, x, y, vx, vy, fr in V.live_particles(P_, t, floor):
                if cull_lip and x < lip_x:
                    continue
                if box and box[0] < x < box[2] and box[1] < y < box[3]:
                    continue
                ox, oy = view.to_out(x, y)
                tx, ty = view.to_out(x - vx * 0.012, y - vy * 0.012)
                drops.append((ox, oy, P_["r"][i] * view.scale, 1 - fr ** 3, tx, ty))
        for x, y, r, vy in drips(t):
            ox, oy = view.to_out(x, y)
            tx, ty = view.to_out(x, y - vy * 0.012 - r * 0.8)
            drops.append((ox, oy, r * view.scale, 1.0, tx, ty))
        tears = []
        if t_shake <= t < t_shake1 + 0.6:
            for P_ in tear_sets:
                for i, x, y, vx, vy, fr in V.live_particles(P_, t, LAND[1] + 20):
                    if t - P_["t0"][i] < 0.1 and math.hypot(x - jhx, y - jhy) < 64:
                        continue                         # never a drop on his face while it is being flung
                    ox, oy = view.to_out(x, y)
                    spd = math.hypot(vx, vy) or 1.0
                    r = P_["r"][i] * view.scale
                    tears.append((ox, oy, vx / spd, vy / spd, r, r * (1.2 + min(1.4, spd / 420)), 1 - fr ** 3))
        arcs = []
        if t_shake <= t < t_shake1:
            v = (t - t_shake) / (t_shake1 - t_shake)
            env = min(1.0, v / 0.12) * (1 - progress(v, 0.6, 1.0, "sine"))
            for side in (-1, 1):
                c0 = 180.0 if side < 0 else 0.0
                for R, span, w in ((86, 40, 1.0), (106, 26, 0.75)):
                    arcs.append(([view.to_out(jhx + R * math.cos(math.radians(c0 + a)),
                                              jhy - 4 + R * math.sin(math.radians(c0 + a)))
                                  for a in np.linspace(-span / 2, span / 2, 7)], env * w))
        lines = []
        if t_spit + 0.04 < t < t_land:
            jx, jy, _, js = flight(t)
            jr = 125 * js                                # keep the speed lines off Jonah himself
            for off in (-26, 0, 26):
                seg = []
                for kk in range(7):
                    tt = t - 0.07 - kk * 0.022
                    if tt < t_spit:
                        break
                    x, y, _, _ = flight(tt)
                    if x < lip_x + 60:
                        break
                    x2, y2, _, _ = flight(tt + 0.01)
                    nx, ny = -(y2 - y), (x2 - x)
                    n = math.hypot(nx, ny) or 1
                    px_, py_ = x + off * nx / n, y + off * ny / n
                    if math.hypot(px_ - jx, py_ - jy) < jr:
                        continue
                    seg.append(view.to_out(px_, py_))
                if len(seg) > 2:
                    lines.append(seg)
        stars = []
        if t_land + 0.05 < t < t_shake + 0.3:
            tf = jonah_tf(t)
            k = progress(t, t_land + 0.05, t_land + 0.3, "out") * (1 - progress(t, t_shake, t_shake + 0.25))
            for i in range(3):
                ang = 2 * math.pi * (t * 1.05 + i / 3)
                sx_ = jhead[0] + 62 * math.cos(ang)
                sy_ = jhead[1] - 14 + 15 * math.sin(ang)
                stars.append((view.to_out(sx_, sy_ + tf.dy), (11 + 3 * math.sin(ang)) * view.scale, k,
                              0.6 + 0.4 * math.sin(ang)))
        allpts = [(p[0], p[1]) for p in drops] + [(p[4], p[5]) for p in drops] + [q for s_ in lines for q in s_] + \
            [s_[0] for s_ in stars] + [(p[0], p[1]) for p in tears] + \
            [(p[0] - p[2] * (p[4] + p[5]), p[1] - p[3] * (p[4] + p[5])) for p in tears] + [q for a_ in arcs for q in a_[0]]
        if not allpts:
            return frame
        ov = V.Overlay(allpts, 40)
        if not ov.ok:
            return frame
        for seg in lines:
            ov.polyline(seg, (252, 248, 236, 170), 5 * view.scale)
        for ox, oy, r, a, tx, ty in drops:
            ov.polyline([(tx, ty), (ox, oy)], (196, 228, 238, int(70 * a)), max(1.0, r * 1.1))
            ov.circle(ox, oy, r, (186, 224, 238, int(170 * a)))
            ov.circle(ox - r * 0.32, oy - r * 0.32, max(0.6, r * 0.34), (255, 255, 252, int(220 * a)))
        for seg, a in arcs:
            ov.polyline(seg, (110, 80, 54, int(150 * a)), 3.6 * view.scale)
        for ox, oy, ux, uy, r, ln, a in tears:
            e = 2.0 * view.scale
            ov.poly(tear_poly(ox, oy, ux, uy, r + e, ln + e * 1.2), (92, 62, 40, int(215 * a)))
            ov.poly(tear_poly(ox, oy, ux, uy, r, ln), (198, 232, 243, int(250 * a)))
            ov.circle(ox - r * 0.3, oy - r * 0.32, max(0.8, r * 0.3), (255, 255, 252, int(235 * a)))
        for (ox, oy), r, k, front_ in stars:
            star = []
            for j in range(10):
                a = -math.pi / 2 + j * math.pi / 5
                rr = r if j % 2 == 0 else r * 0.45
                star.append((ox + rr * math.cos(a), oy + rr * math.sin(a)))
            ov.poly([(x + 1.5, y + 1.5) for x, y in star], (110, 75, 45, int(150 * k)))
            ov.poly(star, (255, 214, 92, int(255 * k * (0.55 + 0.45 * front_))))
        return ov.paste(frame)

    sc.fx = [
        # sun glints on the open water, kept off the fish (far left of it; nearer ones only once it has gone)
        FX.sparkles((20, 600, 320, 780), count=4, color=(255, 252, 236), size=(5, 10), period=1.4, drift=0,
                    seed=86),
        FX.sparkles((850, 560, 1500, 770), count=7, t0=t_away + 1.0, color=(255, 252, 236), size=(5, 10),
                    period=1.4, drift=0, seed=88),
        FX.sparkles((500, 840, 1600, 1000), count=12, color=(255, 252, 236), size=(5, 11), period=1.5, drift=0,
                    seed=87),
        FX.sparkles((HEADF[0] - 230, HEADF[1] - 190, HEADF[0] + 200, HEADF[1] + 120), count=18, t0=t_light0 + 0.3,
                    t1=t_light1 + 0.5, color=(255, 222, 120), size=(10, 20), period=1.5, drift=-12, seed=89),
        FX.sparkles((LAND[0] - 230, LAND[1] - 420, LAND[0] + 200, LAND[1] - 60), count=16, t0=t_joy_peak - 0.1,
                    color=(255, 224, 128), size=(10, 22), period=1.6, drift=-14, seed=90),
        particles,
    ]

    # ---- sound
    sc.sfx("waves_calm", 0, dur=T, gain_db=-10, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_light0 + 0.2, gain_db=-12)
    sc.sfx("gull", t_swim0 + 0.6, gain_db=-17, pan=0.4)
    sc.sfx("whoosh", t_swim0 + 0.1, gain_db=-17, pan=-0.3)
    sc.sfx("splash_small", t_arrive - 0.12, gain_db=-13, pan=-0.1)
    sc.sfx("gulp", t_heave + 0.05, gain_db=-15, pan=-0.1)
    sc.sfx("spit", t_spit - 0.12, gain_db=-9, pan=-0.05)
    sc.sfx("whoosh", t_spit + 0.04, gain_db=-13, pan=0.15)
    sc.sfx("thud", t_land - 0.01, gain_db=-8, pan=0.3)
    sc.sfx("thud", t_hop - 0.01, gain_db=-13, pan=0.3)
    sc.sfx("gull", t_g + 0.6, gain_db=-15, pan=0.6)
    sc.sfx("splash", t_turn0 + 0.02, gain_db=-12, pan=-0.45)
    sc.sfx("cloth", t_shake + 0.05, gain_db=-12, pan=0.3)
    sc.sfx("splash_small", t_shake + 0.12, gain_db=-19, pan=0.3)
    sc.sfx("drip", t_land + 0.6, dur=t_look - t_land, gain_db=-20, pan=0.3, fade_in=0.4, fade_out=0.8)
    sc.sfx("sparkle", t_joy_peak - 0.15, gain_db=-12, pan=0.25)
    sc.sfx("birds", t_look - 0.5, dur=T - t_look + 0.5, gain_db=-20, fade_in=1.0, fade_out=0.8)
    sc.sfx("splash_small", t_tail + 0.05, gain_db=-22, pan=-0.5)
    return sc
