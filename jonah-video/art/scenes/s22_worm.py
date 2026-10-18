"""Scene 22 — the worm, the sun and the hot east wind (Jonah 4:7-9).

The same dry hillside east of Nineveh as the v1 vine scene (art/scenes_v1/s11_vine.py, whose layout, land,
props and drawing helpers are reused): the city small on the western horizon (left), Jonah in his little
booth facing it, the full-grown castor plant arching over the booth roof.

Line 0  "第二天天刚亮，" — the scene opens on s21's last framing (same stage) in the cool lilac of the last minutes of
        night (crescent moon, stars twinkling IN the sky - a looping flipbook behind the clouds and the plant -,
        Jonah asleep sitting up, little z's rising); dawn breaks: the sky blushes pink and the eastern horizon
        glows (the sun itself stays below the hills until line 1), the stars fade, and two doves that roosted in
        the plant fly out from behind its leaves up through the clear sky toward the glow; the lizard, which
        spent the night in the plant's shade by the booth's right post (where s21 leaves it, same drawing),
        turns and scurries back to its stone. Jonah opens in s21's last pose and breathes only after the
        dissolve, so the dissolve lays him, the booth and the lizard over themselves.
        "上帝又安排了一条小虫子。" — a small golden glimmer by the pebble at the foot of the stem (God's doing, light
        only) and the little worm inches out from behind it (three planted inchworm steps) while the camera
        pushes in to the stem.
        "小虫子咬了蓖麻，蓖麻就枯死了。" — chomp, chomp (crumbs fly, the notch deepens, the plant leans); then the plant
        withers as ONE continuous drawing (v1 per-frame flipbook, never two plants blended), dry leaves drop
        and Jonah wakes with a start (hop) and turns sad. The camera pulls back slowly through the wither.
Line 1  "太阳出来以后，" — the sun's rim breaks the eastern hills and it climbs high over the booth, grows and blazes
        (flame rays, hot ochre sky); the worm turns and creeps back (three steps) right behind its pebble, ducks
        and is gone.
        "上帝安排了又热又干的东风。" — the hot east wind arrives from the right: wind swirls, blowing sand, dead leaves
        torn off and whirled toward the city, grass and plant bending, the lizard runs for the shade; Jonah
        squints and rocks in the gusts; a gust blows the cloth of the booth's right roof slope up off the
        rafters (it streams and flaps from the ridge pole), so the roof is open to the sun.
        "太阳晒在约拿的头上，约拿热极了，" — hot sunbeams slant from the sun through the open roof onto Jonah's head
        (light streaks travel down them, a hot spot on his head-cloth), he pants and sweats; on "热极了" he slumps
        back on one hand fanning himself (hop), sweat drops fly, heat waves rise from his head.
        "头都发昏了，又难过又生气。" — spiral eyes, little stars orbit his head, he wobbles; "又难过" head bowed
        (hop); "又生气" arms crossed, angry, steam puffs and an anger mark (hop).
Line 2  "上帝又问约拿：" — as line 1 ends the wind drops: the flame rays shrink into the disc and fade, the hot disc
        turns a soft gold, the sunbeam fades and the roof cloth flops back down; a small lumpy cumulus (golden
        rim on the sun side, ink only on its top contour) fades in right of the sun, clear of the disc, and
        drifts slowly left over the right part of the disc; behind it a slow glory of pale rays (fading out
        long before their tips) turns, and soft golden shafts fan down from the sun's lower-left edge onto
        Jonah (a warm glow clipped to his silhouette), sparkles and motes. He glances up over his shoulder at
        the light behind him, grumpy, listening (hop). God is shown only as this light.
Line 3  (God) "约拿，你因为这棵蓖麻生气，对吗？" — the light breathes gently; on "这棵蓖麻" the rest of the picture dims a
        little while the withered plant gets a warm rim and a glow round its own silhouette (gently pulsing),
        a small burst of sparkles comes out of it and Jonah's eyes go to it; on "对吗" he looks up again
        (blinks while listening).
Line 4  (Jonah) "对！我就是生气！" — he bounces up on his seat with both fists in the air, shouting (big hop, dust,
        pop lines); stamps on "我就是生气"; "我气极了！" — arms crossed, chin up, eyes shut (hop + stamp) with two
        grumpy puffs of steam and an anger mark (pale halos keep them readable over the dark leaf clumps). As
        the line ends he slumps back into the sulk pose (s23's first pose) and huffs more and more quietly in
        the golden light, and the camera settles on END_CAM = s23's opening framing, so the 1.0 s dissolve
        lays Jonah, booth and plant over themselves.

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
  Nothing is drawn over the plant during it (the stars are a sky layer).
* Light layers (sunbeam, God's shafts) sit BEHIND the plant and Jonah so they stay crisp; only small, clipped
  or local glows (hot spot on his head-cloth, glow on his silhouette, glow on the plant at "这棵蓖麻") are on top.
* The cloud only ever overlaps the sun disc at full opacity, and only after the flame rays have shrunk into
  the disc; the wind swirls stop before it appears.
* The roof cloth's lift and landing are one drawing per video frame (_roof_cloth: lying cloth m=0 <-> the
  streaming flap m=1, turned about the ridge), never a swap or a blend of the two: top-face in-betweens are
  booth flipbook frames (cloth in its place under the rafters - over the back rafters once it has swung up),
  underside ones are booth_flap frames over the open booth.
* The particles of God's light are drawn on their own canvas and faded out of a fixed zone round Jonah's head
  (off_face), so sparkles and motes never sit on his face or head-cloth in any of his poses.
* Closures read build()-level names at call time: never reuse a name that a motion function reads (the swirl
  loop once overwrote the sunbeam's length).
* Camera: few long sine-eased moves: s21's last framing held through the opening dissolve, push-in to the stem
  for the worm, one long pull-back through the wither and the sunrise, a slow push toward Jonah in the heat, a
  gentle pull-back for God's light, a small push for the shout, then END_CAM (s23's first framing) held for the
  last 1.1 s; the viewport always stays inside the painted 2112 x 1188 stage (max pan ~90 output px/s, max
  zoom ~20 %/s).
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
LIZ_TO = (1395, 976)      # = s21.LIZ_TO: where s21 leaves the lizard (in the shade, before the booth's right post)
LIZ_S = 0.82              # = s21's lizard scale
XF = 1.0                  # cross-dissolve from s21 (build/timeline.json 'xfade')
SUN_E = (1830, 604)       # dawn: the sun's rim just over the eastern hills (crest y~570 there)
SUN_HOT = (1490, 225)     # blazing sun, high over the booth
CX, CY = W // 2, H // 2   # centre-drawn layers (suns, pop lines) are moved into place by their motion
MOON = (330, 300)
VEIL = (1650, 302)        # final centre of the soft cloud that drifts over the right part of the softened sun
VEIL_DX = 200             # ... it drifts in from this far to the right (its left edge then clears the sun disc)
GAP = (1436, 344)         # God's light fans down from the sun's lower-left edge, beside the cloud
END_CAM = Cam(1169, 704, 1600)   # last framing = s23's opening one (Jonah 'sit_sulk' at the same output place)

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
    # glancing up over his shoulder at the light behind him (upper right; he faces left): pupils back and up
    "lookup": dict(eyes="dot", brow=(0.09, -0.04, 0.02), mouth="grumpy", look=(-0.075, -0.11)),
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
    "sulk_up": C._P(t=-6, h=-18, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True, **_SEAT),
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


_CU_LUMPS = ((-150, 38, 42), (-85, 44, 50), (-10, 46, 54), (70, 44, 50), (140, 38, 42),     # base row
             (-115, -5, 58), (-40, -45, 72), (50, -55, 66), (120, -10, 52))                  # crown


def _cumulus(cx, cy, k, sun, uid="cu", ink=3.5):
    """Lumpy picture-book cumulus about 375*k x 220*k stage px around (cx, cy): a scalloped, flat-ish base and
    a crown of big lumps, lit from ``sun`` (x, y): warm cream toward it, peach-gold underside and soft lump
    undersides, a bright golden rim on the sun side, umber ink on the top contour only (it fades out down the
    sides). Returns (glow, body, defs): ``glow`` is the warm haze bleeding past its edges (keep it outside any
    wobble filter so its blur is not clipped)."""
    lumps = [(cx + x * k, cy + y * k, r * k) for x, y, r in _CU_LUMPS]
    sx, sy = sun

    def shapes(attrs, grow=0.0):
        return ("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + grow:.1f}" {attrs}/>' for x, y, r in lumps) +
                f'<rect x="{cx - 150 * k - grow:.1f}" y="{cy - 10 * k - grow:.1f}" width="{290 * k + 2 * grow:.1f}" '
                f'height="{70 * k + 2 * grow:.1f}" {attrs}/>')
    full = f'x="0" y="0" width="{W}" height="{H}"'
    defs = (f'<radialGradient id="{uid}-f" gradientUnits="userSpaceOnUse" cx="{sx:.0f}" cy="{sy:.0f}" r="{460 * k:.0f}">'
            f'<stop offset="0" stop-color="#fffdf5"/><stop offset="0.5" stop-color="#fff6e0"/>'
            f'<stop offset="0.85" stop-color="#fbe6c2"/><stop offset="1" stop-color="#f5d6a6"/></radialGradient>'
            f'<radialGradient id="{uid}-rim" gradientUnits="userSpaceOnUse" cx="{sx:.0f}" cy="{sy:.0f}" r="{330 * k:.0f}">'
            f'<stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{uid}-rimm" maskUnits="userSpaceOnUse" {full}><rect {full} fill="url(#{uid}-rim)"/></mask>'
            f'<linearGradient id="{uid}-ink" gradientUnits="userSpaceOnUse" x1="0" y1="{cy - 120 * k:.0f}" x2="0" '
            f'y2="{cy + 25 * k:.0f}"><stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="{uid}-inkm" maskUnits="userSpaceOnUse" {full}><rect {full} fill="url(#{uid}-ink)"/></mask>'
            f'<clipPath id="{uid}-sil">{shapes("")}</clipPath>'
            f'<filter id="{uid}-glow" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="{26 * k:.1f}"/></filter>'
            f'<filter id="{uid}-s" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feGaussianBlur stdDeviation="{4 * k:.1f}"/></filter>'
            f'<filter id="{uid}-m" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feGaussianBlur stdDeviation="{12 * k:.1f}"/></filter>')
    glow = f'<g filter="url(#{uid}-glow)" opacity="0.8">{shapes(_fill("#ffe49a"), grow=24 * k)}</g>'
    stroke = f'fill="none" stroke="{INK}" stroke-width="{2 * ink:.1f}"'
    out = ""
    # bright golden rim on the sun side: a slightly bigger silhouette under the cloud, masked toward the sun
    out += (f'<g mask="url(#{uid}-rimm)"><g filter="url(#{uid}-s)">{shapes(_fill("#ffcf55"), grow=9 * k)}</g>'
            f'{shapes(_fill("#fff2b8"), grow=4 * k)}</g>')
    # ink on the top contour only (a wider stroked silhouette under the fill, faded out down the sides)
    out += f'<g mask="url(#{uid}-inkm)">{shapes(stroke)}</g>'
    # body: light falls from the sun side
    out += shapes(_fill(f"url(#{uid}-f)"))
    # modelling (clipped to the cloud): peach underside, soft undersides of the crown lumps, a sunlit sheen
    mod = (f'<ellipse cx="{cx + 20 * k:.1f}" cy="{cy + 92 * k:.1f}" rx="{200 * k:.1f}" ry="{58 * k:.1f}" '
           f'fill="#eab37c" opacity="0.55" filter="url(#{uid}-m)"/>')
    for x, y, r in lumps[5:]:
        mod += (f'<path d="M{x - 0.72 * r:.1f},{y + 0.69 * r:.1f} A{r:.1f},{r:.1f} 0 0 0 {x + 0.72 * r:.1f},'
                f'{y + 0.69 * r:.1f}" fill="none" stroke="#efc493" stroke-width="{0.13 * r:.1f}" opacity="0.4" '
                f'filter="url(#{uid}-s)"/>')
    ang = math.atan2(sy - cy, sx - cx)
    mod += (f'<ellipse cx="{cx + 90 * k * math.cos(ang):.1f}" cy="{cy - 40 * k + 50 * k * math.sin(ang):.1f}" '
            f'rx="{120 * k:.1f}" ry="{70 * k:.1f}" fill="#fffef8" opacity="0.6" filter="url(#{uid}-m)"/>')
    out += f'<g clip-path="url(#{uid}-sil)">{mod}</g>'
    return glow, out, defs


def _fill(c):
    return f'fill="{c}"'


def _cut(s, start, end_tag):
    """Remove the substring of ``s`` from ``start`` (must occur once) through the next ``end_tag``."""
    i = s.index(start)
    assert s.count(start) == 1, start[:60]
    j = s.index(end_tag, i) + len(end_tag)
    return s[:i] + s[j:]


def _booth_open(x, y, scale):
    """PR.booth(x, y, scale, facing=1) with the cloth of its RIGHT roof slope blown up off the rafters by the hot
    east wind: that panel, its front hem and the leafy branch lying on it are left out, so the shady underside
    of the roof shows through the open frame (the rafters and the ridge pole are drawn over it as before).
    The markup is cut out of PR.booth's own output by the ids it derives (asserted to be found)."""
    m = PR.booth(x, y, scale, facing=1)
    for prefix, end in (("boothsl", "/>"), ("boothhem", "/>")):
        cid = PR._uid(prefix, 1)
        d = m[m.index(f'<clipPath id="{cid}"><path d="') + len(f'<clipPath id="{cid}"><path d="'):]
        d = d[:d.index('"')]
        # fill path, clip group and the ink outline of that panel all share the path data d
        i = m.index(f'<path d="{d}"')
        j = m.index(f'<path d="{d}" fill="none"', m.index(f'<clipPath id="{cid}">'))
        j = m.index(end, j) + len(end)
        m = m[:i] + m[j:]
    return _cut(m, '<g transform="translate(60,-360) rotate(28)"', "</g>")


def _booth_flap(phase):
    """The blown-up cloth of the booth's right roof slope, in booth-local coords (PR._place it like the booth):
    hinged on the ridge pole (front apex (0, -374) to back apex (54, -402)), standing up and streaming to the
    left (downwind of the east wind), rippling; ``phase`` 0..1 shifts the ripple."""
    cloth = S.mix(P["headcloth"], P["sand"], 0.3)
    under = S.shade(cloth, -0.06)
    stripe = P["sail_stripe"]
    FA, BA = (0.0, -374.0), (54.0, -402.0)
    L = 150.0

    def edge(p0, ln, ph, spread):
        """One side edge: rises from the ridge, curling downwind (left) as it goes, rippling."""
        pts, x, y = [], p0[0], p0[1]
        for j in range(8):
            u = j / 7
            ang = math.radians(-106 - 26 * u + 9 * math.sin(2 * math.pi * (0.8 * u - phase) + ph))
            if j:
                x, y = x + math.cos(ang) * ln / 7, y + math.sin(ang) * ln / 7
            pts.append((x + spread * u, y + 0.3 * spread * u))
        return pts
    fr, bk = edge(FA, L, 0.0, -10.0), edge(BA, L * 0.94, 0.6, 16.0)
    hem = []                                   # ragged, scalloped free end
    for j in range(1, 6):
        u = j / 6
        p = PR._lerp2(fr[-1], bk[-1], u)
        ex, ey = fr[-1][0] - fr[-2][0], fr[-1][1] - fr[-2][1]
        el = math.hypot(ex, ey) or 1.0
        k_ = 9 if j % 2 else 0
        hem.append((p[0] + ex / el * k_, p[1] + ey / el * k_))
    outline = fr + hem + bk[::-1]
    d = S.smooth_path(outline, closed=True, tension=0.6)
    inner = ""
    for k in (0.72, 0.84):                     # the two terracotta stripes, now near the free end
        a, b = fr[round(k * 7)], bk[round(k * 7)]
        inner += PR._line(a[0], a[1], b[0], b[1], sw=7, color=stripe, extra='opacity="0.85"')
    inner += PR._p(S.smooth_path([PR._lerp2(fr[j], bk[j], 0.5) for j in range(8)], closed=False), sw=3,
                   stroke=S.shade(under, -0.15), extra='opacity="0.45"')
    inner += PR._p(S.smooth_path([PR._lerp2(fr[j], bk[j], 0.15) for j in range(8)], closed=False), sw=14,
                   stroke=S.shade(under, -0.12), extra='opacity="0.35" filter="url(#soft)"')
    return PR._p(d, under, 0) + PR._clip(PR._uid("flap22", round(phase * 100)), d, inner) + PR._p(d, sw=4)


# ------------------------------------------------------------------ the roof cloth lifting off / flopping back
# In-betweens of the right roof slope's cloth (booth-local coords) between lying on the rafters exactly as
# PR._booth draws it (m=0) and _booth_flap's blown-up cloth (m=1), so the gust and the landing are animated
# drawings instead of a one-frame swap. The cloth is hinged on the ridge FA-BA; the booth is drawn in an oblique
# view whose depth axis is the ridge, so turning the cloth about the ridge turns its cross-section in the picture
# plane: each of the seven steps of its front / back edge turns (and changes length) from the lying cloth's
# to the flap's, and the cloth swings up over the ridge, shows its edge and then its underside.
_CL_FA, _CL_BA = (0.0, -374.0), (54.0, -402.0)          # front / back apex (PR._booth)
_CL_FR, _CL_BR = (178.0, -240.0), (232.0, -268.0)       # front / back right eave
_CL_STEP = (184.0 / 6, 138.0 / 6)                       # lying: six steps from the apex to the eave corner +(6,4)
_CL_DRAPE = ((8.0, 26.0), (4.0, 22.0))                  # ... then the hem hanging over the eave (front, back)
_CL_FLAP = ((150.0, 0.0, -10.0), (141.0, 0.6, 16.0))    # _booth_flap: edge length, ripple phase, spread
_CL_HEM0 = 90.0 - math.degrees(math.atan2(26.0, 8.0))   # lying: hem scallops point straight down
_CL_BRANCH = '<g transform="translate(60,-360) rotate(28)"'


def _cl_solve(p):
    """Lying-cloth coordinates (j = steps along the edge, s = 0 front .. 1 back) of booth-local point p."""
    (ax, ay), (bx, by) = _CL_STEP, (_CL_BA[0] - _CL_FA[0], _CL_BA[1] - _CL_FA[1])
    px, py = p[0] - _CL_FA[0], p[1] - _CL_FA[1]
    det = ax * by - ay * bx
    return (px * by - py * bx) / det, (ax * py - ay * px) / det


def _cl_edges(m, ph=0.0, rip=0.0, sw=0.0, bend=0.0):
    """Front and back edge (8 points each, ridge -> free edge) of the right roof cloth. m=0 (rip=sw=bend=0):
    lying on the right slope as PR._booth draws it; m=1 (rip=1, sw=bend=0): exactly _booth_flap(ph). ``sw``
    turns the whole cloth about the ridge (deg, - = up / over to the left), ``bend`` turns its free part
    (deg at the free edge, growing along the cloth)."""
    rest = [(math.degrees(math.atan2(_CL_STEP[1], _CL_STEP[0])), math.hypot(*_CL_STEP))] * 6
    edges = []
    for p0, drape, (ln, ph_e, spread) in zip((_CL_FA, _CL_BA), _CL_DRAPE, _CL_FLAP):
        steps = rest + [(math.degrees(math.atan2(drape[1], drape[0])), math.hypot(*drape))]
        x, y = p0
        pts = [p0]
        for j in range(1, 8):
            u = j / 7
            ra, rl = steps[j - 1]
            fa = -106 - 26 * u
            ang = ((1 - m) * ra + m * fa + rip * 9 * math.sin(2 * math.pi * (0.8 * u - ph) + ph_e) + sw +
                   bend * u ** 1.5)
            ll = (1 - m) * rl + m * ln / 7
            x, y = x + math.cos(math.radians(ang)) * ll, y + math.sin(math.radians(ang)) * ll
            pts.append((x + m * spread * u, y + 0.3 * m * spread * u))
        edges.append(pts)
    return edges


def _cl_at(edge, j):
    j = min(max(j, 0.0), 7.0)
    i = min(int(j), 6)
    return PR._lerp2(edge[i], edge[i + 1], j - i)


def _roof_cloth(m, ph=0.0, rip=0.0, sw=0.0, bend=0.0, branch=""):
    """The right roof cloth in an in-between state (see _cl_edges) -> (panel, front hem, branch, top face?):
    booth-local markup of the cloth, of its front edge folded down over the front rafter (only while it is
    still close to the rafters; '' after) and of the leafy branch ``branch`` lying on its top face, carried
    along ('' once the underside shows: it is round the back). m=0 reproduces PR._booth's right slope, front
    hem and branch exactly; m=1 (rip=1) _booth_flap."""
    cloth = S.mix(P["headcloth"], P["sand"], 0.3)
    cloth_d = S.shade(cloth, -0.18)
    under = S.shade(cloth, -0.06)
    stripe = P["sail_stripe"]
    fr, bk = _cl_edges(m, ph, rip, sw, bend)

    def at(j, s):
        return PR._lerp2(_cl_at(fr, j), _cl_at(bk, j), s)

    def mp(p):
        return at(*_cl_solve(p))

    # free edge: ragged, scalloped (lying: the scallops hang straight down)
    ex, ey = fr[7][0] - fr[6][0], fr[7][1] - fr[6][1]
    a = math.atan2(ey, ex) + math.radians((1 - m) * _CL_HEM0)
    el = (1 - m) * 10 + m * 9
    hem = []
    for i in range(1, 6):
        p = PR._lerp2(fr[7], bk[7], i / 6)
        k_ = el if i % 2 else 0.0
        hem.append((p[0] + math.cos(a) * k_, p[1] + math.sin(a) * k_))
    outline = fr + hem + bk[::-1]
    d = S.smooth_path(outline, closed=True, tension=0.6 * m)
    # which face shows: the lying cloth's cross product (step x ridge) is negative
    dj = (at(4, 0.5)[0] - at(3, 0.5)[0], at(4, 0.5)[1] - at(3, 0.5)[1])
    ds = (at(3.5, 1)[0] - at(3.5, 0)[0], at(3.5, 1)[1] - at(3.5, 0)[1])
    top = dj[0] * ds[1] - dj[1] * ds[0] < 0
    k_top = 1 - PR._smooth(m / 0.4)
    k_under = PR._smooth((m - 0.45) / 0.4)
    FA, BA, FR, BR = _CL_FA, _CL_BA, _CL_FR, _CL_BR
    inner = ""
    if top and k_top > 0.01:      # PR._booth's soft highlight of the sagging cloth
        sag = PR._lerp2(PR._lerp2(FA, BA, 0.5), PR._lerp2(FR, BR, 0.5), 0.55)
        sag = (sag[0], sag[1] + 12)
        hl = [PR._lerp2(FR, FA, 0.6), sag, PR._lerp2(BR, BA, 0.6), BA, FA]
        inner += PR._p(PR._poly([mp(p) for p in hl]), S.shade(cloth, 0.12), 0,
                       extra=f'opacity="{0.6 * k_top:.3f}" filter="url(#soft)"')
    for k, jf in ((0.18, 6), (0.3, 5)):       # the two terracotta stripes (lying: along the hem)
        (ja, sa), (jb, sb) = (_cl_solve((p[0], p[1] + 8)) for p in (PR._lerp2(FR, FA, k), PR._lerp2(BR, BA, k)))
        a_ = at(ja + (jf - ja) * m, sa * (1 - m))
        b_ = at(jb + (jf - jb) * m, sb + (1 - sb) * m)
        inner += PR._line(a_[0], a_[1], b_[0], b_[1], sw=7, color=stripe, extra='opacity="0.85"')
    if top and k_top > 0.01:      # PR._booth's sag line
        q0, q1, q2 = mp(FA), mp(sag), mp(BR)
        inner += PR._p(f"M{q0[0]:.1f},{q0[1]:.1f} Q{q1[0]:.1f},{q1[1]:.1f} {q2[0]:.1f},{q2[1]:.1f}", sw=3,
                       stroke=cloth_d, extra=f'opacity="{0.6 * k_top:.3f}"')
    if not top and k_under > 0.01:     # _booth_flap's fold lines on the underside
        inner += PR._p(S.smooth_path([PR._lerp2(fr[j], bk[j], 0.5) for j in range(8)], closed=False), sw=3,
                       stroke=S.shade(under, -0.15), extra=f'opacity="{0.45 * k_under:.3f}"')
        inner += PR._p(S.smooth_path([PR._lerp2(fr[j], bk[j], 0.15) for j in range(8)], closed=False), sw=14,
                       stroke=S.shade(under, -0.12), extra=f'opacity="{0.35 * k_under:.3f}" filter="url(#soft)"')
    uid = PR._uid("cloth22", round(m, 4), round(ph, 3), round(rip, 3), round(sw, 2), round(bend, 2))
    panel = PR._p(d, cloth if top else under, 0) + PR._clip(uid, d, inner) + PR._p(d, sw=4)
    on = ""
    if top and branch:            # the leafy branch on its top face, carried along (affine about its middle)
        c = (60 + 64 * math.cos(math.radians(28)) + 4 * math.sin(math.radians(28)),
             -360 + 64 * math.sin(math.radians(28)) - 4 * math.cos(math.radians(28)))
        jc, sc_ = _cl_solve(c)
        o, pj, ps = at(jc, sc_), at(jc + 0.5, sc_), at(jc, sc_ + 0.5)
        (ax, ay), (bx, by) = _CL_STEP, (BA[0] - FA[0], BA[1] - FA[1])
        cj, cs = ((pj[0] - o[0]) * 2, (pj[1] - o[1]) * 2), ((ps[0] - o[0]) * 2, (ps[1] - o[1]) * 2)
        det = ax * by - ay * bx                            # M = [cj cs] @ inv([step ridge])
        ia, ib, ic, id_ = by / det, -bx / det, -ay / det, ax / det
        ma, mb = cj[0] * ia + cs[0] * ic, cj[1] * ia + cs[1] * ic
        mc, md = cj[0] * ib + cs[0] * id_, cj[1] * ib + cs[1] * id_
        me, mf = o[0] - (ma * c[0] + mc * c[1]), o[1] - (mb * c[0] + md * c[1])
        if abs(ma - 1) + abs(mb) + abs(mc) + abs(md - 1) + abs(me) + abs(mf) < 1e-6:
            on = branch
        else:
            on = f'<g transform="matrix({ma:.5f},{mb:.5f},{mc:.5f},{md:.5f},{me:.3f},{mf:.3f})">{branch}</g>'
    # the front edge folded down over the front rafter: it turns with the cloth and is pulled straight
    fold = 1 - PR._smooth(m / 0.22)
    if fold <= 0.01:
        return panel, "", on, top
    jfr = (FR[0] - FA[0]) / _CL_STEP[0]               # the eave lies (almost) on the lying edge's line

    def hang(u, off):
        """lerp(FA, FR, u) + off of the lying cloth, carried along by the front edge (turning with its step
        there); ``off`` (the fold hanging below the edge) is pulled straight where the edge has lifted off the
        rafter, and everywhere as the cloth swings up."""
        j = u * jfr
        base = _cl_at(fr, j)
        i = min(max(int(math.ceil(j)), 1), 6)
        rot = (math.atan2(fr[i][1] - fr[i - 1][1], fr[i][0] - fr[i - 1][0]) -
               math.atan2(_CL_STEP[1], _CL_STEP[0]))
        f = fold * (1 - PR._smooth(abs(rot) / math.radians(20)))
        vx = u * (FR[0] - FA[0]) - j * _CL_STEP[0] + f * off[0]      # (the eave is 0.5 px off the step line)
        vy = u * (FR[1] - FA[1]) - j * _CL_STEP[1] + f * off[1]
        cr, sr = math.cos(rot), math.sin(rot)
        return base[0] + cr * vx - sr * vy, base[1] + sr * vx + cr * vy

    h9 = [hang(i / 8, (0.0, 14 + (8 if i % 2 else 0) + 6 * (i / 8))) for i in range(9)]
    hd = PR._poly([hang(0, (0.0, 0.0)), hang(1, (8.0, 2.0))] + h9[::-1])
    s0, s1 = hang(0, (0.0, 10.0)), hang(1, (0.0, 12.0))
    strip = (PR._p(hd, cloth_d, 0) +
             PR._clip(PR._uid("clothhem22", uid), hd,
                      PR._line(s0[0], s0[1], s1[0], s1[1], sw=6, color=stripe, extra='opacity="0.8"')) +
             PR._p(hd, sw=3.5))
    return panel, strip, on, top


def _booth_cloth(x, y, scale, m, ph=0.0, rip=0.0, sw=0.0, bend=0.0):
    """PR.booth(x, y, scale, facing=1) with its right roof cloth in an in-between state, drawn in its own place
    in the booth (under the ridge pole, rafters and lashings), with its front hem and the branch lying on it in
    theirs - or, once it has swung up off the rafters (m >= 0.1), over the ridge pole and the back rafters it
    has lifted off (still under the front rafters and lashings). Returns (markup, top face?)."""
    m0 = PR.booth(x, y, scale, facing=1)
    i = m0.index(_CL_BRANCH)
    j = m0.index("</g>", i) + 4
    panel, strip, on, top = _roof_cloth(m, ph, rip, sw, bend, m0[i:j])
    m0 = m0[:i] + on + m0[j:]            # the branch is drawn last (over the back rafter), as in PR._booth
    if m >= 0.1:
        dd = PR._poly([(_CL_BR[0] - 4, _CL_BR[1]), (_CL_BA[0] - 22, _CL_BA[1] - 20)], closed=False)
        k = m0.index(f'<path d="{dd}"')
        k = m0.index("/>", m0.index(f'<path d="{dd}"', k + 1)) + 2       # after the back-right rafter
        m0, panel = m0[:k] + panel + m0[k:], ""
    for prefix, end, new in (("boothsl", "/>", panel), ("boothhem", "/>", strip)):
        cid = PR._uid(prefix, 1)
        key = f'<clipPath id="{cid}"><path d="'
        d = m0[m0.index(key) + len(key):]
        d = d[:d.index('"')]
        a = m0.index(f'<path d="{d}"')
        b = m0.index(f'<path d="{d}" fill="none"', m0.index(f'<clipPath id="{cid}">'))
        b = m0.index(end, b) + len(end)
        m0 = m0[:a] + new + m0[b:]
    return m0, top


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
    t_worm1 = t_worm0 + 2.1                            # (three inchworm steps)
    t_bite0 = _at(L0, "咬了") - 0.15                    # "小虫子咬了蓖麻"
    t_bite1 = t_bite0 + 1.35                           # the notch is complete
    t_with0 = _at(L0, "蓖麻就枯死")                      # "蓖麻就枯死了"
    t_with1 = t_with0 + 1.9
    t_chomp1 = t_with0 + 0.25
    t_wake = t_with0 + 0.62                            # leaves drop round him: he wakes with a start
    t_sad0 = t_wake + 0.95
    t_sun0 = L1.at("太阳出来")                          # "太阳出来以后": the rim breaks the eastern hills
    t_sun1 = t_sun0 + 2.6                              # the sun stands high and blazes
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
    t_rays1 = L2.start - 0.05                          # the flame rays have shrunk into the disc ...
    t_rays0 = min(L1.end - 0.15, t_rays1 - 0.7)        # ... starting as "又生气" ends
    t_cl0 = t_rays1 - 0.15                             # the soft cloud fades in right of the sun, then drifts
    t_cl1 = t_cl0 + 0.4                                #   slowly left over the right part of the disc
    t_cl2 = t_cl1 + 3.5
    t_listen = L2.start + 0.55                         # Jonah looks up toward the light
    t_plant = _at(L3, "这棵蓖麻")                       # "这棵蓖麻"
    t_plant_back = _at(L3, "对吗")                      # "对吗？"
    t_shout = L4.start                                 # "对！"
    t_stamp = _at(L4, "我就是") + 0.25                 # stamps on "我就是生气！"
    t_hmph = L4.at("我气极了")                          # "我气极了！"
    t_settle = min(max(L4.end + 0.06, t_hmph + 1.0), T - 1.2)  # slumps back into s23's opening sulk pose

    def a_gold(t):
        return M.progress(t, t_calm0, t_light0 + 1.4, "sine")

    def wind(t):
        return M.progress(t, t_wind - 0.3, t_wind + 0.5, "sine") * (1 - 0.8 * a_gold(t))

    # =============================================================== SKY
    sky_h = 665
    a_dawn = lambda t: M.progress(t, t_dawn0, t_dawn1, "sine")
    a_hot = lambda t: M.progress(t, t_sun0 + 0.1, t_sun1 + 0.3, "sine")

    stars = []
    rng = np.random.default_rng(22)
    for i in range(46):
        x, y = rng.uniform(20, W - 20), rng.uniform(20, 470)
        r_ = rng.uniform(3, 7.5)
        if math.hypot(x - MOON[0], y - MOON[1]) < 120:
            continue
        stars.append((x, y, r_, (i * 0.618) % 1.0))
    moon = (f'<path d="M{MOON[0]},{MOON[1] - 52} A52,52 0 1 1 {MOON[0]},{MOON[1] + 52} '
            f'A40,52 0 1 0 {MOON[0]},{MOON[1] - 52} Z" fill="#fbf1cf" stroke="{INK}" stroke-width="3"/>')
    sky_pre = S.svg_doc(
        f'<rect x="-20" y="-20" width="{W + 40}" height="{sky_h + 20}" fill="url(#g)"/>'
        f'<ellipse cx="{SUN_E[0]}" cy="{HORIZON}" rx="760" ry="250" fill="url(#r)"/>'
        f'<circle cx="{MOON[0] - 12}" cy="{MOON[1]}" r="160" fill="url(#mh)"/>' + S.g(moon, filter="wobble-fine"),
        defs=S.lin_grad("g", [(0, "#46507e"), (0.5, "#6f6c9c"), (0.85, "#b49ab4"), (1, "#d6b1b4")]) +
        S.rad_grad("r", [(0, "#f2c2a8", 0.75), (0.55, "#d9a6b0", 0.3), (1, "#b49ab4", 0)]) +
        S.rad_grad("mh", [(0, "#fbf1cf", 0.42), (0.3, "#f3ead0", 0.2), (0.65, "#c9c9dc", 0.06), (1, "#a9aecb", 0)]))
    sc.add("sky_pre", sky_pre, wc=0.4, motion=lambda t: Tf(alpha=0.0 if a_dawn(t) >= 0.999 else 1.0))

    # twinkling stars: part of the night sky (behind the clouds, the hills and the plant), a looping 4-frame
    # flipbook (frame 3 = frame 0) whose neighbouring frames crossfade - each star swells and shrinks in turn
    def star_frame(k):
        out = ""
        for x, y, r_, ph in stars:
            tw = 0.5 + 0.5 * math.cos(2 * math.pi * (k / 3 + ph))
            out += V._star(x, y, r_ * (0.45 + 0.7 * tw), "#fbf0c8", sw=0)
            if tw > 0.8:
                out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_ * 1.9:.1f}" fill="#fbf0c8" opacity="0.22"/>'
        return S.svg_doc(out)
    star_docs = [star_frame(k) for k in range(3)]
    sc.add("stars", star_docs + [star_docs[0]], wc=0, frame_at=lambda t: (t * 1.25) % 3.0,
           motion=lambda t: Tf(alpha=1 - a_dawn(t)))

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
        S.rad_grad("c", [(0, "#fffcf0", 0.55), (0.4, "#fff4d0", 0.3), (1, "#ffefc0", 0)]))
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

    # dawn shows only the bright horizon glow (sky_dawn) and the sun's halo over the hills; its rim breaks the
    # crest (y ~571 at x 1830) on "太阳出来以后" and it climbs high over the booth
    S_HOT = 118 / 82
    climb = M.keys([(t_sun0 - 0.15, {"dx": 0, "dy": 571 - SUN_E[1] + 82 + 6}),
                    (t_sun1, {"dx": SUN_HOT[0] - SUN_E[0], "dy": SUN_HOT[1] - SUN_E[1], "s": S_HOT})],
                   "sine", pivot=(CX, CY))
    sc.add("sun_dawn", sun_svg(82, "#f8c070", "#ffe0b0", 330),
           motion=at(SUN_E, M.combine(climb, lambda t: Tf(alpha=1 - M.progress(t, t_sun1 - 0.05, t_sun1 + 0.3,
                                                                               "sine")))))
    # blazing noon sun: flame rays (turning) behind a bright disc (v1); before God speaks the rays shrink into
    # the disc and fade, and a soft pale-gold disc covers the hot one (the same circle and wobble, so only the
    # colour changes); both share one breathing motion that calms down
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
    def ray_shrink(t):
        k = M.progress(t, t_rays0, t_rays1, "inout")
        s = 1 - 0.72 * k
        return Tf(sx=s, sy=s, alpha=M.progress(t, t_sun1 - 0.05, t_sun1 + 0.45, "sine") *
                  (1 - M.progress(t, t_rays0 + 0.25, t_rays1, "sine")), px=hx, py=hy)

    sc.add("sun_rays", rays, wc=0.3,
           motion=at(SUN_HOT, M.combine(lambda t: Tf(rot=12 * t, px=hx, py=hy),
                                        M.breathe(0.03, 0.9, pivot=(hx, hy)), ray_shrink)))
    a_soft = lambda t: M.progress(t, t_rays0, t_rays1 + 0.8, "sine")

    def sun_breath(t):
        k = a_soft(t)
        s = 1 + 0.035 * (1 - k) * math.sin(2 * math.pi * t / 1.3) + 0.012 * k * math.sin(2 * math.pi * t / 3.2)
        return Tf(sx=s, sy=s, px=hx, py=hy)
    hot = S.svg_doc(
        f'<circle cx="{hx}" cy="{hy}" r="185" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{hx}" cy="{hy}" r="118" fill="#ffd94f" stroke="#c9741f" stroke-width="6"/>'
            f'<circle cx="{hx}" cy="{hy}" r="90" fill="#fff1a8"/>'
            f'<circle cx="{hx}" cy="{hy}" r="58" fill="#fffae0"/>'
            f'<circle cx="{hx - 34}" cy="{hy - 34}" r="26" fill="#fffef6" opacity="0.9"/>', filter="wobble"),
        defs=S.rad_grad("hg", [(0, "#fffef4", 1), (0.6, "#fff6cf", 0.85), (0.8, "#ffeaa0", 0.4), (1, "#ffe08a", 0)]))
    sc.add("sun_hot", hot, wc=0.4, motion=at(SUN_HOT, M.combine(
        sun_breath, lambda t: Tf(alpha=0.0 if a_soft(t) >= 0.999 else M.progress(t, t_sun1 - 0.1, t_sun1 + 0.3,
                                                                                    "sine")))))
    soft_sun = S.svg_doc(
        f'<circle cx="{hx}" cy="{hy}" r="300" fill="url(#sg)"/>' +
        S.g(f'<circle cx="{hx}" cy="{hy}" r="118" fill="url(#sd)" stroke="#d99a40" stroke-width="5"/>'
            f'<circle cx="{hx - 36}" cy="{hy - 36}" r="40" fill="#fffef8" opacity="0.5"/>', filter="wobble"),
        defs=S.rad_grad("sg", [(0, "#fffbea", 1.0), (0.42, "#fff1c0", 0.85), (0.7, "#ffe6a0", 0.35),
                               (1, "#ffe09a", 0)]) +
        S.rad_grad("sd", [(0, "#fffef4"), (0.55, "#fff3c0"), (1, "#ffd970")], cx=0.45, cy=0.45))
    sc.add("sun_soft", soft_sun, wc=0.3, motion=at(SUN_HOT, M.combine(sun_breath, lambda t: Tf(alpha=a_soft(t)))))

    # --- clouds: pink-lit at dawn, burnt away as the sun climbs ------------------------------------
    clouds = S.svg_doc(S.g(
        S.cloud(700, 150, 290, 88, "#fdf3e4", seed=3, sw=3, shade_fill="#efcdd0") +
        S.cloud(1640, 290, 240, 76, "#fdf1e2", seed=5, sw=3, shade_fill="#efcdd0") +
        S.cloud(1870, 118, 300, 92, "#fdf3e4", seed=8, sw=3, shade_fill="#efcdd0") +
        S.cloud(700, 330, 170, 56, "#fdf1e2", seed=9, sw=3, shade_fill="#efcdd0"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=M.combine(
        M.drift(vx=-7), lambda t: Tf(alpha=(0.55 + 0.45 * a_dawn(t)) *
                                     (1 - M.progress(t, t_sun0 - 0.3, t_sun0 + 1.0, "sine")))))
    z_sky = sc.layers[-1].z + 0.5          # doves fly in the sky: in front of the clouds, behind hills and plant

    # God's gentle light (warm light only - never a figure): behind the softened sun a slow glory of pale rays
    # turns (filled with a radial gradient, so every ray melts away long before its tip); a small lumpy cumulus
    # fades in RIGHT of the sun (clear of the disc - the flame rays are already gone) and drifts slowly left
    # over the right part of the disc (opaque whenever it overlaps it), its sun side rimmed with gold
    glory = S.svg_doc(S.g(f'<path d="{S.rays(CX, CY, 130, 700, n=12, width_deg=11)}" fill="url(#gr)"/>',
                          filter="soft") +
                      f'<circle cx="{CX}" cy="{CY}" r="360" fill="url(#gg)"/>',
                      defs=f'<radialGradient id="gr" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="700">'
                           f'<stop offset="0" stop-color="#fffbe8" stop-opacity="0.9"/>'
                           f'<stop offset="0.2" stop-color="#fffbe8" stop-opacity="0.9"/>'
                           f'<stop offset="0.5" stop-color="#fff6d8" stop-opacity="0.5"/>'
                           f'<stop offset="0.85" stop-color="#fff2c8" stop-opacity="0"/></radialGradient>' +
                           S.rad_grad("gg", [(0, "#fffbea", 0.8), (0.5, "#fff2c8", 0.4), (1, "#ffe9b0", 0)]))
    sc.add("glory", glory, wc=0, motion=at(SUN_HOT, M.combine(
        lambda t: Tf(rot=2.5 * t, px=CX, py=CY),
        lambda t: Tf(alpha=M.progress(t, t_cl1, t_cl1 + 2.2, "sine") * (0.85 + 0.15 * math.sin(t * 1.7))))))
    cu_glow, cu_body, cu_defs = _cumulus(VEIL[0], VEIL[1], 1.0, SUN_HOT, uid="veil")
    veil = S.svg_doc(cu_glow + S.g(cu_body, filter="wobble"), defs=cu_defs)

    def veil_motion(t):
        u = M.progress(t, t_cl1, t_cl2, "sine")
        return Tf(dx=VEIL_DX * (1 - u) - 3.0 * max(0.0, t - t_cl2), dy=4 * math.sin(2 * math.pi * t / 4.4),
                  alpha=M.progress(t, t_cl0, t_cl1 + 0.1, "sine"))

    sc.add("veil", veil, wc=0.5, motion=veil_motion)

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
    # two doves that roosted in the castor plant take off from behind its leaves and fly up and away to the
    # right through clear sky toward the glowing eastern horizon; they are part of the sky (behind the plant)
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    wing_cycle = (0, 1, 2, 3, 4, 3, 2, 1)

    def flap(rate, ph):
        return lambda t: float(wing_cycle[int(t * rate + ph) % len(wing_cycle)])

    def dove_motion(t0, dur, ex, ey, ph, acc=0.7):
        ln = math.hypot(ex, ey)
        v = ln / (dur - acc / 2)               # take-off: speeds up over ``acc`` s, then flies on steadily

        def m(t):
            u = t - t0
            if u < 0 or u > dur:
                return Tf(alpha=0.0)
            d = v * (u * u / (2 * acc) if u < acc else u - acc / 2)
            return Tf(dx=ex * d / ln, dy=ey * d / ln - 50 * math.sin(math.pi * d / ln) +
                      9 * math.sin(2 * math.pi * (u / 0.62 + ph / 8)))
        return m

    for i, (x0, y0, s_, t0, ph) in enumerate([(1080, 420, 0.62, t_dawn0 + 0.3, 0.0),
                                              (990, 400, 0.54, t_dawn0 + 0.7, 3.0)]):
        sc.add(f"dove{i}", [S.svg_doc(PR.dove(x0, y0, s_, 1, wing=w)) for w in wings], z=z_sky + 0.1 * (i + 1),
               frame_at=flap(9.0, ph), wc=0.5, motion=dove_motion(t0, 4.4, 1240, -300, ph))

    # =============================================================== LIZARD (back to its stone at dawn; basks;
    # runs from the hot wind). It is s21's lizard (same drawing and scale) and opens where s21 leaves it - in the
    # plant's shade in front of the booth's right post (LIZ_TO, facing left) - so the dissolve lays it over
    # itself; as dawn breaks it turns and scurries back to its stone, before the camera pushes in to the worm.
    def liz_body(legs, facing):
        b = V._lizard(LIZ[0], LIZ[1], LIZ_S, legs=legs)
        return b if facing > 0 else f'<g transform="translate({2 * LIZ[0]},0) scale(-1,1)">{b}</g>'

    liz_frames = [S.svg_doc(liz_body(lg, f)) for lg, f in ((0, 1), (1, 1), (0, -1), (1, -1))]
    F_LIZ_LEFT = 2.0                                  # legs 0, facing left = s21's last lizard frame
    t_lizret = max(t_dawn0 + 0.5, XF + 0.1)           # after the dissolve, as the sky starts to blush
    LIZ_RET = 0.7
    assert t_lizret + LIZ_RET <= t_godw - 0.4, "the lizard must be home before the push-in to the worm"
    ldx, ldy = LIZ_TO[0] - LIZ[0], LIZ_TO[1] - LIZ[1]
    LIZ_HIDE = 154                                    # its dash ends centred behind liz_rock2 (and the grass)

    LIZ_TURN = 0.12       # it turns round in place (squeezes through edge-on) before scurrying home

    def liz_frame(t):
        if t < t_lizret - LIZ_TURN / 2:
            return F_LIZ_LEFT
        if t < t_lizret:
            return 0.0
        if t < t_lizret + LIZ_RET:
            return float(int((t - t_lizret) * 16) % 2)
        return 0.0 if t < t_liz else float(int((t - t_liz) * 16) % 2)

    def liz_motion(t):
        if t_lizret - LIZ_TURN <= t < t_lizret:
            w = (t - (t_lizret - LIZ_TURN)) / LIZ_TURN
            return Tf(dx=ldx, dy=ldy, sx=max(0.08, abs(math.cos(math.pi * w))), px=LIZ[0], py=LIZ[1])
        if t < t_lizret + LIZ_RET:
            u = _clamp((t - t_lizret) / LIZ_RET)
            return Tf(dx=ldx * (1 - M.ease("out")(u)), dy=ldy * (1 - u) - 14 * math.sin(math.pi * u))
        if t < t_liz:
            u = (t + 0.9) % 2.8
            b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
            return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)
        v = t - t_liz
        return Tf(dx=LIZ_HIDE * M.ease("out")(min(1.0, v / 0.5)), dy=38 * M.progress(v, 0.08, 0.4, "sine"),
                  alpha=1 - M.progress(v, 0.22, 0.36, "sine"))   # gone while it slips behind the stone

    sc.add("lizard", liz_frames, frame_at=liz_frame, motion=liz_motion, wc=0.5)
    liz_layers = [sc.layers[-1]]
    sc.add("liz_rock2", S.svg_doc(S.g(V._stone(LIZ[0] + 150, 1002, 104, 58, seed=43, sw=4), filter="wobble-fine")),
           wc=0.8)
    liz_layers.append(sc.layers[-1])

    # booth + its contact shadow
    booth_shadow = (f'<ellipse cx="{XB + 60}" cy="{GY + 8}" rx="{340 * SP}" ry="30" fill="{INK}" '
                    f'opacity="0.16" filter="url(#soft)"/>')
    booth_svg = S.svg_doc(booth_shadow + PR.booth(XB, GY, SP, facing=1))
    # a gust of the hot east wind lifts the cloth of the right roof slope off the rafters just before the sun
    # beats on Jonah's head (so the sunbeam comes in through the open roof): air gets under it (its free edge
    # puffs up twice), then it whips up over the ridge pole (its free part trailing), overshoots and settles
    # into streaming and flapping from the ridge; when the wind drops it tips back over the ridge, falls faster
    # and faster, lands on the rafters and its free edge bounces once. Every in-between is its own drawing
    # (_roof_cloth, one per video frame): while its top face shows it is drawn in its place inside the booth
    # (under the rafters, with its front fold and the branch lying on it), once its underside shows it is the
    # flap layer over the open booth, like the streaming flap (_booth_flap) it turns into.
    t_rip = t_beam - 0.55                 # the cloth whips up
    t_shut = t_rays1 - 0.1                # the wind has dropped: it tips back over
    CL_A, CL_UP = 0.40, 0.80              # puffs before t_rip; whip + overshoot + settle after it
    CL_FALL, CL_LAND = 0.38, 0.30         # fall from t_shut; landing bounce after it
    CL_SWING, CL_LAG = 143.0, 0.03        # deg from lying to streaming; trailing of its free part (s)
    ZETA, OMEGA = 0.62, 11.0              # the whip: a damped swing (overshoot ~8 %)

    def flap_ph(t):
        return (0.0, 0.33, 0.67)[int(t * 9) % 3]

    def cloth_state(t):
        """(m, ph, rip, sw, bend) of the roof cloth's in-between at t (see _roof_cloth)."""
        u = t - t_rip
        if u < 0:                                  # air gets under it: the free edge puffs up twice
            bil = (14 * math.sin(math.pi * _clamp((u + CL_A) / 0.24)) if u < -0.16 else
                   24 * PR._smooth((u + 0.16) / 0.16))
            return 0.0, 0.0, 0.0, 0.0, -bil
        if u < CL_UP:                              # whips up over the ridge: damped swing to the flap
            wd = OMEGA * math.sqrt(1 - ZETA * ZETA)
            e = math.exp(-ZETA * OMEGA * u)
            th = 1 - e * (math.cos(wd * u) + ZETA * OMEGA / wd * math.sin(wd * u))
            dth = OMEGA * OMEGA / wd * e * math.sin(wd * u)
            w = 1 - PR._smooth((u - 0.5) / 0.3)    # (settled exactly by CL_UP)
            th, dth = 1 + (th - 1) * w, dth * w
            m = min(th, 1.0)
            return (m, flap_ph(t), m, -CL_SWING * max(th - 1, 0.0),
                    -24 * (1 - PR._smooth(u / 0.15)) + CL_LAG * CL_SWING * dth)
        s = t - t_shut
        if s < CL_FALL:                            # tips back over the ridge and falls, free part trailing
            q = max(s, 0.0) / CL_FALL
            m = 1 - q * q
            return m, flap_ph(t), m, 0.0, -CL_LAG * CL_SWING * 2 * q / CL_FALL
        s -= CL_FALL                               # lands; its free edge flops down past and settles
        b0 = -CL_LAG * CL_SWING * 2 / CL_FALL
        return (0.0, 0.0, 0.0, 0.0,
                b0 * math.exp(-s / 0.08) * math.cos(2 * math.pi * s / 0.3) * (1 - PR._smooth((s - 0.18) / 0.12)))

    booth_frames = [booth_svg, S.svg_doc(booth_shadow + _booth_open(XB, GY, SP))]
    flap_docs = [S.svg_doc(PR._place(_booth_flap(ph), XB, GY, SP, 1)) for ph in (0.0, 0.33, 0.67)]
    cl_seen = {}

    def cl_frame(t):
        st = cloth_state(t)
        mk, top = _booth_cloth(XB, GY, SP, *st)
        if top:
            doc, frames = S.svg_doc(booth_shadow + mk), booth_frames
        else:
            doc, frames = S.svg_doc(PR._place(_roof_cloth(*st)[0], XB, GY, SP, 1)), flap_docs
        if doc not in cl_seen:
            cl_seen[doc] = len(frames)
            frames.append(doc)
        return (cl_seen[doc], None) if top else (1, cl_seen[doc])

    cl_win = []                                    # (first video frame, [(booth frame, flap frame)])
    for w0, w1 in ((t_rip - CL_A, t_rip + CL_UP), (t_shut, t_shut + CL_FALL + CL_LAND)):
        k0, k1 = math.ceil(w0 * FPS - 1e-6), math.ceil(w1 * FPS - 1e-6)
        cl_win.append((k0, [cl_frame(k / FPS) for k in range(k0, k1)]))
    k_open, k_shut = cl_win[0][0] + len(cl_win[0][1]), cl_win[1][0]

    def cl_lookup(t):
        k = round(t * FPS)
        for k0, ids in cl_win:
            if k0 <= k < k0 + len(ids):
                return ids[k - k0]
        return (1, -1) if k_open <= k < k_shut else (0, None)     # -1: the streaming flap

    sc.add("booth", booth_frames, wc=0.8, frame_at=lambda t: float(cl_lookup(t)[0]))
    hinge = (XB + 27 * SP, GY - 388 * SP)            # middle of the ridge pole (stage px)

    def flap_frame(t):
        f = cl_lookup(t)[1]
        return float((0, 1, 2)[int(t * 9) % 3] if f in (None, -1) else f)

    def flap_motion(t):
        f = cl_lookup(t)[1]
        if f is None:
            return Tf(alpha=0.0)
        if f >= 0:                                 # an in-between drawing (already in place)
            return Tf()
        k = M.progress(t, t_rip + CL_UP, t_rip + CL_UP + 0.5, "sine") * (1 - M.progress(t, t_shut - 0.4, t_shut,
                                                                                         "sine"))
        return Tf(rot=5 * math.sin(2 * math.pi * t / 0.55) * wind(t) * k, px=hinge[0], py=hinge[1])

    sc.add("booth_flap", flap_docs, frame_at=flap_frame, motion=flap_motion, wc=0.6)
    # the lizard (and the stone it hides behind) are drawn in front of the booth, as in s21, so it is in front
    # of the right post at LIZ_TO; still under the canopy's ground shade (added next). Only z moves: the layers'
    # insertion order (and so their watercolour seeds) stays as it was.
    for i, lyr in enumerate(liz_layers):
        lyr.z = sc.layers[-1].z + 0.1 * (i + 1)

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
    a_beam = lambda t: _env(t, t_beam - 0.1, t_beam + 0.5, t_rays0, t_shut - 0.02)   # gone before the roof shuts

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
        S.g(_ray_fan(GAP[0], GAP[1], 860, [104, 111, 118, 125, 133, 141], w0=10, w1=62, fill="url(#sh)",
                     opacity=0.62), filter="godsoft") +
        f'<ellipse cx="{XJ - 10}" cy="{GY - 230}" rx="300" ry="280" fill="url(#jg)"/>',
        defs=S.rad_grad("jg", [(0, "#ffe6a8", 0.36), (0.5, "#ffdc96", 0.15), (1, "#ffd68a", 0)]) +
        '<filter id="godsoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="11"/>'
        '</filter>'
        f'<linearGradient id="sh" gradientUnits="userSpaceOnUse" x1="0" y1="{GAP[1]}" x2="0" y2="{GY + 80}">'
        f'<stop offset="0" stop-color="#fff0c0" stop-opacity="0.95"/>'
        f'<stop offset="0.6" stop-color="#ffe6ac" stop-opacity="0.8"/>'
        f'<stop offset="1" stop-color="#ffe0a0" stop-opacity="0.1"/></linearGradient>')
    sc.add("god_light", shafts, wc=0, blend="add",
           motion=lambda t: Tf(alpha=a_light(t) * (0.85 + 0.15 * math.sin(t * 2.2)),
                               rot=1.2 * math.sin(t * 0.45), px=GAP[0], py=GAP[1]))

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

    # "这棵蓖麻": God points out the withered plant with light - everything round it dims a little, the plant
    # itself glows (warm light clipped to its own silhouette, a bright rim on the edges toward the light, a soft
    # halo just around it) and gently pulses; a small burst of sparkles comes out of it (fx below)
    a_pl = lambda t: _env(t, t_plant - 0.2, t_plant + 0.35, t_plant_back + 0.2, t_plant_back + 1.2)
    dead = plant_frames[plant_ids[-1]]
    P_IN = dead[dead.index("</defs>") + 7: dead.rindex("</svg>")]
    PCX, PCY = XP + 170, GY - 330                    # middle of the withered canopy
    pl_defs = (
        '<filter id="pwhite" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>'
        '<filter id="pblack" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>'
        '<filter id="phalo" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.86  0 0 0 0 0.52  0 0 0 0.75 0"/>'
        '<feGaussianBlur stdDeviation="16"/></filter>'
        f'<mask id="psil" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<g filter="url(#pwhite)">{P_IN}</g></mask>'
        f'<mask id="pout" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/><g filter="url(#pblack)">{P_IN}</g></mask>'
        f'<mask id="prim" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<g filter="url(#pwhite)">{P_IN}</g><g transform="translate(-7,9)" filter="url(#pblack)">{P_IN}</g></mask>' +
        S.rad_grad("pgl", [(0, "#ffe9a8", 1), (0.6, "#ffd98c", 0.6), (1, "#ffd080", 0.15)]) +
        S.rad_grad("prm", [(0, "#fff4cc", 1), (0.7, "#ffe8a8", 0.85), (1, "#ffe0a0", 0.3)]))
    pl_body = (f'<g mask="url(#pout)"><g filter="url(#phalo)" opacity="0.6">{P_IN}</g></g>'
               f'<g mask="url(#psil)"><ellipse cx="{PCX}" cy="{PCY}" rx="460" ry="520" fill="url(#pgl)" '
               f'opacity="0.12"/></g>'
               f'<g mask="url(#prim)"><ellipse cx="{PCX + 80}" cy="{PCY - 60}" rx="520" ry="560" fill="url(#prm)" '
               f'opacity="0.8"/></g>')
    sc.add("plant_glow", S.svg_doc(pl_body, defs=pl_defs), wc=0, blend="add", motion=M.combine(
        plant_motion, lambda t: Tf(alpha=a_pl(t) * (0.8 + 0.2 * math.sin(2 * math.pi * (t - t_plant) / 1.1)))))
    # ... and the rest of the picture dims a little round it (a warm multiply, clear over the plant)
    dim = S.svg_doc(f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#dm)"/>',
                    defs=f'<radialGradient id="dm" gradientUnits="userSpaceOnUse" cx="{PCX}" cy="{PCY + 40}" '
                         f'r="900"><stop offset="0" stop-color="#ffffff"/><stop offset="0.38" stop-color="#ffffff"/>'
                         f'<stop offset="0.75" stop-color="#cfa77a"/><stop offset="1" stop-color="#b98c60"/>'
                         f'</radialGradient>')
    sc.add("plant_dim", dim, wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.6 * a_pl(t)))

    # --- hot east wind swirls (behind Jonah, in bands clear of his head) ---------------------------
    for i, (y, sw_len, ph) in enumerate([(470, 360, 0.0), (880, 320, 0.45), (300, 260, 0.8), (600, 230, 1.15)]):
        sw_svg = S.svg_doc(S.g(V._swirl(1700, y, sw_len), filter="wobble-fine"))

        def swirl_motion(t, ph=ph):
            if t < t_wind - 0.2:
                return Tf(alpha=0.0)
            if t > t_calm0:                  # the wind has dropped before the cloud and God's light come
                return Tf(alpha=0.0)
            u = ((t - t_wind + 0.2 + ph) % 1.6) / 1.6
            a = math.sin(math.pi * u) * M.progress(t, t_wind - 0.2, t_wind + 0.3) * \
                (1 - M.progress(t, t_calm0 - 0.7, t_calm0, "sine"))
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
          (t_plant + 0.1, 10, "cut", 0.3, False, False),     # cuts: a crossfade doubled his eyes and brows
          (t_plant_back, 9, "cut", 0.3, False, False),
          (t_shout, 12, "cut", 1.4, True, True),
          (t_hmph, 13, "cut", 0.8, True, True),
          (t_settle, 8, "cut", 0.45, False, False)]   # slumps back, sulking (= s23's first pose)
    prev = 0
    for ev in EV:
        assert ev[2] != "fade" or abs(ev[1] - prev) == 1, ev
        prev = ev[1]
    # blink cuts: his eyes close just before the look-at-the-plant cut and right after the look-back cut
    blinks = [t_listen + 1.7, t_plant - 0.9, t_plant_back + 0.9, t_plant + 0.1 - 0.067, t_plant_back]

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
        # asleep he starts breathing only after the dissolve (scale 1 there, like s21's resting Jonah), so his
        # head is not doubled by a breathing mismatch in the cross-dissolve
        s = 1 + amp * math.sin(2 * math.pi * (max(0.0, t - XF) if asleep else t) / per)
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
    F_LIT = 8                     # the sulk pose too: he slumps back into it at the end, still in the light
    jl_frames = []
    for i, (p, e) in enumerate(JP):
        if i < F_LIT:
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
           motion=M.combine(jonah_motion, lambda t: Tf(alpha=0.38 * a_light(t) if jonah_frame(t) >= F_LIT else 0.0)))

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

            # a soft pale halo behind each puff keeps it readable over the dark withered leaf clumps
            halo = f'<circle cx="{cx}" cy="{cy}" r="{r * 1.75:.0f}" fill="#fff6e0" opacity="0.6" filter="url(#soft)"/>'
            sc.add(f"{name}_puff{side_}", S.svg_doc(halo + V._puff(cx, cy, r)), motion=puff_motion, wc=0.3)
        ax, ay = hx0 + 56, hy0 - 60

        def anger_motion(t):
            for th in times:
                u = t - th + 0.04
                if 0 <= u < 0.95:
                    s = 1.25 * M.ease("out")(u / 0.1) if u < 0.1 else \
                        1.25 - 0.25 * M.progress(u, 0.1, 0.24, "sine") + 0.06 * math.sin(u * 30) * (1 - u)
                    return Tf(sx=s, sy=s, alpha=1 - M.progress(u, 0.65, 0.95, "sine"), px=ax, py=ay)
            return Tf(alpha=0.0)

        halo = f'<circle cx="{ax}" cy="{ay}" r="{mark * 1.9:.0f}" fill="#fff6e0" opacity="0.6" filter="url(#soft)"/>'
        sc.add(f"{name}_anger", S.svg_doc(halo + V._anger(ax, ay, mark)), motion=anger_motion, wc=0.2)

    huff_layers("sulk", jpts[8]["head"], [t_ang + 0.08, t_ang + 0.95])
    huff_layers("hmph", jpts[13]["head"], [t_hmph + 0.05, t_hmph + 0.5], r=32, mark=26)

    # =============================================================== WORM (v1 inchworm steps + chomp)
    worm_frames = [S.svg_doc(PR.worm(XW, GY + 2, SW, 1, crawl=c, chomp=ch))
                   for c, ch in [(1.0, 0), (0.5, 0), (0, 0), (0, 0.5), (0, 1.0)]]
    worm_frames += [S.svg_doc(PR.worm(XW, GY + 2, SW, -1, crawl=c)) for c in (1.0, 0.5, 0.0)]   # 5..7 going home
    # three inchworm steps out from behind its pebble and three back; it starts and ends centred behind the
    # pebble, then ducks down behind it (only its antennae could show above the stone) before it fades
    NCYC, STRIDE = 3, 66.0
    X_START = -NCYC * STRIDE
    STRIDE_B = 188.0 / NCYC                # facing left its body sits 16 px further left of the anchor
    PEB_X = XW - 190
    t_wx1 = t_wormx + 2.1

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
        return float(5 + (1, 0, 1, 2)[min(3, int(u * 4))]), -STRIDE_B * (k + M.progress(u, 0.6, 1.0, "sine"))

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
        duck = M.progress(t, t_wx1 + 0.05, t_wx1 + 0.4, "sine")
        dy += 30 * duck
        a = M.progress(t, t_worm0 - 0.25, t_worm0, "sine") * (1 - M.progress(t, t_wx1 + 0.2, t_wx1 + 0.45, "sine"))
        return Tf(dx=dx, dy=dy, alpha=a)

    sc.add("worm", worm_frames, frame_at=lambda t: worm_state(t)[0], motion=worm_motion, wc=0.5)
    sc.add("pebble", S.svg_doc(S.g(V._rock(PEB_X, GY + 16, 130, 62, seed=21, sw=4),
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
        (0.0, Cam(1070, 600, 1990)),            # = s21's last framing (same stage): a same-place dissolve ...
        (1.0, Cam(1070, 600, 1990)),            # ... held through it
        (t_push0, Cam(1062, 606, 1960)),
        (t_push1, Cam(985, 728, 1340)),
        (t_pull0, Cam(990, 724, 1324)),
        (t_pull1, Cam(1110, 592, 1960)),
        (t_beam - 0.1, Cam(1114, 594, 1940)),
        (t_dizzy + 0.6, Cam(1190, 640, 1580)),
        (t_light0 - 0.1, Cam(1194, 644, 1560)),
        (L3.start + 0.3, Cam(1110, 604, 1840)),
        (t_shout - 0.35, Cam(1118, 608, 1810)),
        (t_shout + 0.95, Cam(1152, 650, 1690)),
        (T - 1.1, END_CAM),                     # = s23's opening framing: Jonah over Jonah in the dissolve
        (T, END_CAM),
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

    rng3 = np.random.default_rng(31)
    NBU = 11
    bu_ang = rng3.uniform(-math.pi * 0.95, math.pi * 0.15, NBU)          # mostly upward and outward
    bu_dist = rng3.uniform(150, 330, NBU)
    bu_size = rng3.uniform(11, 21, NBU)
    bu_del = rng3.uniform(0.0, 0.25, NBU)

    def burst(frame, t, view):
        """A small burst of golden sparkles out of the withered plant on "这棵蓖麻"."""
        u0 = t - t_plant
        if u0 < 0 or u0 > 1.6:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(NBU):
            u = (u0 - bu_del[i]) / 1.25
            if not 0 <= u <= 1:
                continue
            e = M.ease("out")(u)
            x = PCX + 20 + math.cos(bu_ang[i]) * bu_dist[i] * e
            y = PCY + 10 + math.sin(bu_ang[i]) * bu_dist[i] * e * 0.8 - 30 * u
            ox, oy = view.to_out(x, y)
            r = bu_size[i] * view.scale * (0.4 + 0.8 * math.sin(math.pi * min(1.0, u * 1.6)) ** 0.5) * (1 - 0.4 * u)
            a = int(235 * min(1.0, u / 0.08) * (1 - M.progress(u, 0.55, 1.0, "sine")))
            w, g_ = r * 0.22, r * 0.6
            d.ellipse([ox - g_, oy - g_, ox + g_, oy + g_], fill=(255, 236, 160, a // 3))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(255, 244, 196, a))
        frame.alpha_composite(ov)
        return frame

    # the particles of God's light (sparkles, the plant's burst, motes) never sit on Jonah's face or head: drawn
    # on their own canvas, they fade out inside a soft capsule round his head that covers it in every pose (and
    # hop) he takes in the light - one fixed zone, so nothing pops when his pose changes
    HZ_A, HZ_B = jpts[8]["head"], jpts[9]["head"]                    # sulk / sulk_up (shout, hmph lie between)
    HZ_A, HZ_B = (HZ_A[0] - 4, HZ_A[1] - 12), (HZ_B[0] + 4, HZ_B[1] - 12)
    HZ_R, HZ_SOFT = 80.0, 40.0                                       # clear inside, faded in over (stage px)

    def off_face(*fxs):
        def fx(frame, t, view):
            ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            for f in fxs:
                ov = f(ov, t, view)
            if ov.getchannel("A").getbbox() is None:
                return frame
            (ax_, ay_), (bx_, by_) = view.to_out(*HZ_A), view.to_out(*HZ_B)
            r0, r1 = HZ_R * view.scale, (HZ_R + HZ_SOFT) * view.scale
            x0, y0 = max(0, int(min(ax_, bx_) - r1)), max(0, int(min(ay_, by_) - r1))
            x1, y1 = min(ov.width, int(max(ax_, bx_) + r1) + 1), min(ov.height, int(max(ay_, by_) + r1) + 1)
            if x1 > x0 and y1 > y0:
                arr = np.array(ov)
                yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
                vx, vy = bx_ - ax_, by_ - ay_
                u = np.clip(((xx - ax_) * vx + (yy - ay_) * vy) / max(vx * vx + vy * vy, 1e-6), 0, 1)
                dist = np.hypot(xx - ax_ - u * vx, yy - ay_ - u * vy)
                k = np.clip((dist - r0) / (r1 - r0), 0, 1)
                k = k * k * (3 - 2 * k)
                arr[y0:y1, x0:x1, 3] = (arr[y0:y1, x0:x1, 3] * k + 0.5).astype(np.uint8)
                ov = Image.fromarray(arr, "RGBA")
            frame.alpha_composite(ov)
            return frame
        return fx

    sc.fx = [
        grade,
        FX.sparkles((XW - 330, GY - 210, XW + 40, GY - 10), count=12, t0=t_godw - 0.1, t1=t_worm1 + 0.3,
                    color=(255, 238, 160), size=(8, 18), period=1.1, drift=-10, seed=5),
        FX.motes((200, 200, 1900, 900), count=24, t0=t_dawn0 + 0.5, t1=t_sun1, color=(255, 240, 220), alpha=100),
        shimmer,
        dust,
        streaks,
        FX.vignette(lambda t: (0.27 * M.progress(t, t_sun1, t_dizzy, "sine") * (1 - 0.6 * a_gold(t))) *
                    (0.85 + 0.15 * math.sin(t * 3.2)), color=(150, 72, 24)),
        off_face(
            FX.sparkles((XJ - 520, GY - 760, XJ + 160, GY - 60), count=26, t0=t_light0 + 0.2, t1=T + 1,
                        color=(255, 238, 170), size=(9, 20), period=1.5, drift=-8, seed=8),
            FX.sparkles((XP - 60, GY - 620, XP + 520, GY - 60), count=16, t0=t_plant - 0.1, t1=t_plant_back + 1.0,
                        color=(255, 238, 168), size=(10, 20), period=1.2, drift=-6, seed=9),
            burst,
            FX.motes((300, 0, 1700, 900), count=28, t0=t_light0, t1=T + 1, color=(255, 244, 205), alpha=120,
                     seed=22)),
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
    sc.sfx("heat", t_sun0 + 0.3, dur=t_calm0 + 1.5 - (t_sun0 + 0.3), gain_db=-14, fade_in=0.8, fade_out=1.5)
    sc.sfx("whoosh", t_wind - 0.2, gain_db=-11, pan=0.6)
    sc.sfx("cloth", t_rip, gain_db=-10, pan=0.25)
    sc.sfx("cloth", t_shut + CL_FALL - 0.05, gain_db=-14, pan=0.25)     # it lands back on the rafters
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
