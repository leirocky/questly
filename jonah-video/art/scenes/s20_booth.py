"""Scene 20 — the booth (Jonah 4:5).

One wide 3100 x 1300 stage on a hot afternoon. Left: Nineveh's east wall with its open gate (mid-distance, hazy),
saved and joyful as in s18 / s19: townspeople in their own colourful clothes on the wall walk and in the
gateway (two children hop and cheer), banners, bunting and fluttering pennants on the gate towers, sheep
grazing by the watered fields; a road runs from the gate across the plain onto a dry ochre ridge. Right of
the gate the ridge rises into a low knoll where Jonah builds his booth (the same props.booth drawing as
s21 / v1 s11, split into its building stages). A blazing sun (s21's flame sun) hangs over the city.

Line 0 "约拿没有回答。" — opens exactly where s19 ends: Jonah sits on the ground, arms crossed, scowling at the
        city, his back to the soft golden light of God's question (light only, never a figure, from the
        upper right as in s19), his bundle of sticks and rolled cloth lying beside him. The light fades as
        he answers nothing: a grumpy "hmph" (eyes shut, chin up, steam puffs above and behind his head).
        He hops up, then swings the bundle up over his head onto his back.
        "他出了城，坐在城的东边，" — he trudges east along the ridge (a planted-foot walk cycle: the drawing
        follows the distance walked; a footstep sound on every footfall), the camera following; he plants
        both feet on the knoll and, with a shrug of the shoulder, tosses the bundle down beside him (thud).
        "为自己搭了一座小棚子。" — with a stone he knocks the front post in, the other posts go up on the next
        knocks of the 'hammer' sound (the cue time is chosen so the sound has 4 knocks and the knock onsets are
        read from it); he lifts the frame (tie bar, rafters, ridge) above his head and it drops onto the posts;
        he throws the striped cloth over the ridge (it unrolls downward and settles); leafy branches pop on
        top. The bundle on the ground shrinks as he uses it. He stands under the roof, hot and panting.
Line 1 "他坐在棚子下面的阴凉里，" — he sits down in the booth's thin shade (hop + dust), a cool tint settles on him,
        eyes closed with relief and a big sigh; the camera pushes in a little.
        "要看看这座城到底会怎么样。" — chin on fist, a sulky eye on the city; two doves flutter up from a bush
        and fly off toward the gate as the camera pulls back to reveal the city he is watching. He drops his
        hands to his knees (plain seated pose, facing the city) and the scene settles on s21's opening framing.

Continuity (1.0 s cross-dissolves)
* Start = s19's last frame: s19 ends with Jonah (sit_sulk, facing left) anchored at output (1060, 926) at
  1.2 * 1920/2066 scale, God's light coming down from its cloud gap at output (1414, 66). The opening camera
  is computed so that Jonah's anchor and size match, the light is mapped through the same transform, and his
  grumpy fidget / breathing run on s19's clock (read from the timeline) so the two drawings coincide.
* End = s21's first frame: s21 opens with its booth anchor at output (1064, 895), booth scale 1.3 * 1920/1960,
  Jonah sitting ('sit', facing left) 28 px right of it, and its afternoon flame sun at output (230, 246). The
  final camera puts this booth on exactly that spot at the same size, the sun (same drawing, scale, turning
  and breathing phase) on s21's, and Jonah ends in the plain 'sit' pose at the same place.

Notes for maintainers
* Every time comes from ctx.lines[i].at(phrase) / .start / .end (never fixed numbers).
* Pose changes are hard cuts hidden by a squash-and-hop (v1 technique); expression-only changes are cuts too
  (blinks). Jonah's custom poses use characters' rig (C._P / C._figure) with the standard Jonah design; two
  extra expressions are added to characters.EXPRS only while a drawing is built (removed again right after).
* The bundle is ONE local drawing (bundle_local) used both on his back (via the design's 'behind' hook) and on
  the ground, so the pick-up ends and the toss starts exactly where it is on his back.
* Booth parts stay separate layers for the whole scene (no swap to a combined drawing, so nothing pops). Each
  part carries an invisible spacer the size of the whole booth: the 'wobble-fine' filter region is the
  objectBoundingBox +-10 %, which would otherwise crop a lone, nearly straight stick to a sliver.
* Sky, sun, clouds and far dunes have a little parallax against the camera (zero at the final view).
"""
import math
import random
from contextlib import contextmanager

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]

# ------------------------------------------------------------------ Jonah: custom poses
SJ = 1.25                      # Jonah / booth scale
SB = SJ
WALK_A = 50                    # figure px the planted ankle moves per half step (stance from +A to -A)
WALK_N = 8                     # drawings per step (two steps per cycle)

_EXTRA_EXPRS = {
    # eyes shut, chin up: "hmph!" (not answering)
    "hmph": dict(eyes="closed", brow=(0.12, -0.05, 0.04), mouth="grumpy"),
    # keeping a sulky eye on the city
    "watch": dict(eyes="dot", brow=(0.08, -0.04, 0.03), mouth="flat"),
    "watch_blink": dict(eyes="closed", brow=(0.08, -0.04, 0.03), mouth="flat"),
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


def _tube(pts, w, col, sw=3.2):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * sw:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


ROPE = S.mix(P["sackcloth"], P["sand"], 0.3)
CLOTH = S.mix(P["headcloth"], P["sand"], 0.3)


_BACK = {}     # anchor-relative placement (x, y, rotation) of the bundle on Jonah's back, per drawing label
_LABEL = [""]


def bundle_local(state=0):
    """The bundle (scale 1, centred on (0, 0)): booth sticks tied with rope plus the striped cloth rolled up and
    seen end-on. Axis along x; the 'base' end is +x, local +y is the side away from the carrier's back.
    state 0 full, 1 fewer sticks (posts used), 2 one stick + the cloth roll (frame used), 3 leftovers (cloth used)."""
    rnd = random.Random(5)
    cols = [P["wood"], P["wood_dark"], P["wood_light"], P["wood"], S.shade(P["wood"], -0.12)]
    offs = [(-15, 0), (7, 1), (-5, 2), (15, 3), (2, 4)]
    keep = {0: (0, 1, 2, 3, 4), 1: (1, 3, 4), 2: (4,), 3: (1, 4)}[state]
    out = ""
    for i, (o, ci) in enumerate(offs):
        e0, e1, j = rnd.uniform(-0.05, 0.04), rnd.uniform(-0.06, 0.06), rnd.uniform(-2.5, 2.5)
        if i not in keep:
            continue
        if state == 3:          # leftovers: two short sticks lying across each other
            a_ = math.radians(-9 if i == 1 else 7)
            k, cx_ = (0.5, -40) if i == 1 else (0.7, 20)
            ca, sa = math.cos(a_), math.sin(a_)
            out += _tube([(cx_ - 130 * k * ca, 4 - 130 * k * sa), (cx_ + 130 * k * ca, 4 + 130 * k * sa)], 8.5,
                         cols[ci], 3)
            continue
        oy = o if state <= 1 else o * 0.4 + 2
        out += _tube([(-130 * (1 + e1), oy), (0, oy + j), (130 * (1 + e0), oy)], 8.5, cols[ci], 3)
    if state <= 2:      # the striped cloth, rolled up lengthwise and tied on with the sticks
        y0, r = 30, 17
        x0, x1 = -88, 84
        out += (f'<rect x="{x0}" y="{y0 - r}" width="{x1 - x0}" height="{2 * r}" rx="{r}" fill="{CLOTH}" '
                f'stroke="{INK}" stroke-width="3.4"/>')
        for xs in (-58, -40, 44, 62):
            out += (f'<path d="M{xs},{y0 - r + 2} q-5,{r - 2} 0,{2 * r - 4}" fill="none" stroke="{P["sail_stripe"]}" '
                    f'stroke-width="6" stroke-linecap="round"/>')
        out += (f'<ellipse cx="{x1 - 8}" cy="{y0}" rx="8" ry="{r - 2}" fill="{S.shade(CLOTH, -0.12)}" stroke="{INK}" '
                f'stroke-width="2.6"/><path d="M{x1 - 9},{y0 - 6} q5,6 0,12" fill="none" stroke="{INK}" '
                f'stroke-width="2"/>')
    if state <= 1:
        for bx in (73, -47):
            out += _tube([(bx + 2, -23), (bx - 2, 50)], 6, ROPE, 3)
    elif state == 2:
        out += _tube([(42, -10), (38, 50)], 6, ROPE, 3)
    return out


def _bundle_back(st):
    """The bundle slung on Jonah's back (body coords; drawn behind him)."""
    tp, m = st["tp"], st["m"]
    bx = -m["shw"] - 4
    base, top = tp(bx, -14), tp(bx - 58, 236)
    c = ((base[0] + top[0]) / 2, (base[1] + top[1]) / 2)
    vx, vy = top[0] - base[0], top[1] - base[1]
    ang = math.degrees(math.atan2(-vy, -vx))           # local +x (the base end) points from top to base
    _BACK[_LABEL[0]] = (c[0], c[1] - st["ground"], ang)
    return f'<g transform="translate({c[0]:.1f},{c[1]:.1f}) rotate({ang:.2f})">{bundle_local(0)}</g>'


def _strap(st):
    """Rope strap of the bundle over the near shoulder (drawn on the robe, under the near arm)."""
    tp, m = st["tp"], st["m"]
    p = [tp(-m["shw"] + 4, m["T"] - 2), tp(-6, m["T"] + 4), tp(m["shw"] * 0.42, m["T"] - 26)]
    return _tube(p, 5.5, ROPE, 2.8)


def _stone_in_hand(st):
    """A grey stone in the far hand (the 'hammer')."""
    Sx, E, Wr = st["arms"][0]
    dx, dy = Wr[0] - E[0], Wr[1] - E[1]
    ln = math.hypot(dx, dy) or 1.0
    cx, cy = Wr[0] + dx / ln * 15, Wr[1] + dy / ln * 15
    a = math.degrees(math.atan2(dy, dx))
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="17" ry="12.5" fill="#bcb2a2" stroke="{INK}" stroke-width="3.4" '
            f'transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"/>'
            f'<ellipse cx="{cx - 4:.1f}" cy="{cy - 4:.1f}" rx="6" ry="3.6" fill="#e2dccf" opacity="0.8" '
            f'transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"/>')


def jonah_fig(x, y, scale, facing, ps, expr, bundle=False, stone=False, label="j"):
    """Jonah (same design as characters.jonah) in a scene-local pose record; optionally with the bundle on his
    back or a stone in his far hand. Returns (markup, body points dict in stage px)."""
    D = dict(C._jonah_design())
    if bundle:
        D["behind"] = _bundle_back
        D["mid"] = _strap
    if stone:
        D["front"] = _stone_in_hand
    _LABEL[0] = label
    with _exprs():
        inner, _ = C._figure(D, C._ADULT, dict(ps), expr, C._fsign(facing))
    L = C._LAST
    sx = scale * (1 if facing >= 0 else -1)

    def stp(p):
        return (x + p[0] * sx, y + p[1] * scale)
    pts = {"head": stp(L["head"]), "head_top": stp(L["head_top"]), "hands": [stp(p) for p in L["hands"]],
           "feet": [stp(p) for p in L["feet"]]}
    return C._wrap_out(inner, x, y, scale, facing, f"jonah-{label}"), pts


_SEAT = dict(C._SEATED)
_CROSS = (("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1))
POSE = {
    # s19's last drawing (characters 'sit_sulk', facing left) and its "hmph!" (chin up, eyes shut)
    "sulk": dict(C.POSES["sit_sulk"]),
    "sulk_hmph": C._P(t=-5, h=-16, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True,
                      look=(0.02, -0.06), **_SEAT),
    # swinging the bundle up over his head onto his back
    "heave": C._P(t=-10, h=-8, legs=(("ik", 30, 1), ("ik", -24, 1)), drop=6, near_back=True,
                  arms=(("ik", "abs", -20, -410, 1), ("ik", "abs", -60, -388, 1)), hands=("fist", "fist")),
    # shrugging it off: near shoulder dipped back, near arm flung back after it, torso twisted toward the throw
    "toss": C._P(t=-10, h=6, legs=(("ik", 34, 1), ("ik", -30, 1)), drop=10, look=(-0.05, 0.02),
                 arms=(("fk", 34, 86), ("fk", -64, -34)), hands=("fist", "open")),
    "stand": C._P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "ham_up": C._P(t=-4, h=-8, legs=(("ik", 26, 1), ("ik", -22, 1)), drop=6,
                   arms=(("ik", "abs", 30, -430, 1), ("ik", "abs", 92, -198, 1)), hands=("fist", "fist")),
    "ham_dn": C._P(t=6, h=4, legs=(("ik", 26, 1), ("ik", -22, 1)), drop=12,
                   arms=(("ik", "abs", 104, -316, 1), ("ik", "abs", 92, -192, 1)), hands=("fist", "fist")),
    "lift": C._P(t=-6, h=-16, legs=((10, 2), (-8, -2)), near_back=True,
                 arms=(("ik", "abs", 6, -372, 1), ("ik", "abs", -14, -366, -1)), hands=("fist", "fist")),
    "throw": C._P(t=-12, h=-14, legs=(("ik", 30, 1), ("ik", -30, 1)), near_back=True,
                  arms=(("fk", 168, 196), ("fk", 158, 186)), hands=("open", "open")),
    "sit": dict(C.POSES["sit"]),
    "sit_chin": C._P(t=8, h=-4, legs=(("ik", 70, 1), ("ik", 80, 1)),
                     arms=(("ik", "head", 0.15, 1.12, 1), ("ik", "head", 0.35, 1.12, 1)), hands=("fist", "fist"),
                     **_SEAT),
}


def walk_pose(k):
    """Drawing k of Jonah's planted-foot walk (WALK_N drawings per step, two steps per cycle). In drawing k the
    planted ankle sits at WALK_A * (1 - 2u) figure px from the anchor while the other foot swings through; so
    advancing the anchor 2 * WALK_A / WALK_N * scale stage px per drawing keeps the planted sole on one spot."""
    ph = (k % (2 * WALK_N)) / WALK_N
    step, u = divmod(ph, 1.0)
    A = WALK_A
    plant = ("ik", A * (1 - 2 * u), 1)
    swing = ("ik", -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, 22 * math.sin(math.pi * u))
    sw = 32 * math.cos(math.pi * ph)
    return C._P(t=5, h=6, legs=(plant, swing) if step == 0 else (swing, plant),
                arms=(("fk", -sw, -sw + 14), ("fk", sw, sw + 14)), drop=12 + 4 * math.cos(2 * math.pi * u))


# ------------------------------------------------------------------ the booth in building stages
def booth_parts():
    """props.booth (Jonah 4:5) split into its building stages, as local markup (anchor = bottom centre between
    the front posts, scale 1, facing right). Same drawing as props._booth when every part is shown.
    Keys in back-to-front order: post_bl, post_br, under, post_fl, post_fr, tiebar, cloth, frame, lash, branches."""
    _stick, _lashing, _p, _poly, _ell, _line, _lerp2, _clip, _uid, _g, _f = (
        PR._stick, PR._lashing, PR._p, PR._poly, PR._ell, PR._line, PR._lerp2, PR._clip, PR._uid, PR._g, PR._f)
    wood, wd = P["wood"], P["wood_dark"]
    cloth = CLOTH
    cloth_d = S.shade(cloth, -0.18)
    under = S.mix(S.shade(cloth, -0.45), P["ink_soft"], 0.15)
    stripe = P["sail_stripe"]
    DX, DY = PR.BOOTH_DEPTH
    FL, FR, FA = (-178, -236), (178, -240), (0, -374)
    BL, BR, BA = (FL[0] + DX, FL[1] + DY), (FR[0] + DX, FR[1] + DY), (FA[0] + DX, FA[1] + DY)
    parts = {}
    parts["post_bl"] = _stick([(-112 + DX * 0.9, -16), (-115 + DX, -150), (-110 + DX, -258 + DY)], 9,
                              S.shade(wd, 0.05), 3)
    parts["post_br"] = _stick([(146 + DX * 0.9, -18), (149 + DX, -140), (146 + DX, -262 + DY)], 9,
                              S.shade(wd, 0.05), 3)
    gid = _uid("boothund", 0)
    u = f'<defs>{S.lin_grad(gid, [(0, S.shade(under, -0.1)), (0.7, under), (1, S.mix(under, cloth, 0.4))])}</defs>'
    u += _p(_poly([FL, FA, (FR[0] - 4, FR[1] - 4), (BR[0] - 8, BR[1] + 8), (BL[0] + 8, BL[1] + 8)]), f"url(#{gid})", 0)
    back_curtain = [(BL[0] + 10, BL[1] + 2), (BR[0] - 10, BR[1] + 2), (BR[0] - 14, -196), (BR[0] - 60, -188),
                    (BA[0] + 20, -198), (BA[0] - 40, -190), (BL[0] + 60, -200), (BL[0] + 14, -192)]
    u += _p(_poly(back_curtain), S.mix(under, cloth, 0.45), 3)
    for xx in (-60, 20, 100):
        u += _line(xx + DX * 0.5, -246, xx + DX * 0.5 + 3, -200, sw=2.5, color=S.shade(under, -0.15),
                   extra='opacity="0.5"')
    parts["under"] = u
    stones = {}
    for bx, by in ((-158, 0), (146, 0)):
        stones[bx] = _ell(bx - 14, by - 2, 15, 7, P["stone"], 3) + _ell(bx + 14, by - 1, 11, 6, P["stone_dark"], 3)
    parts["post_fl"] = _stick([(-158, 2), (-162, -120), (-156, -200), (-160, -292)], 13, wood, 3.5,
                              knots=(0.45,)) + stones[-158]
    parts["post_fr"] = _stick([(146, 2), (150, -110), (146, -205), (152, -284)], 13, wood, 3.5,
                              knots=(0.62,)) + stones[146]
    parts["tiebar"] = _stick([(-196, -256), (-40, -260), (194, -254)], 9, S.shade(wood, -0.1), 3)

    def slope(e_front, e_back, sgn):
        hem = []
        for i in range(7):
            uu = i / 6
            p = _lerp2((e_front[0] + sgn * 14, e_front[1] + 30), (e_back[0] + sgn * 10, e_back[1] + 26), uu)
            hem.append((p[0], p[1] + (10 if i % 2 else 0)))
        sag = _lerp2(_lerp2(FA, BA, 0.5), _lerp2(e_front, e_back, 0.5), 0.55)
        sag = (sag[0], sag[1] + 12)
        pts = [FA, BA] + [_lerp2(BA, e_back, 0.5), (e_back[0] + sgn * 6, e_back[1] + 4)] + list(reversed(hem)) + \
            [(e_front[0] + sgn * 6, e_front[1] + 4), _lerp2(e_front, FA, 0.5)]
        d = _poly(pts)
        inner = _p(_poly([_lerp2(e_front, FA, 0.6), sag, _lerp2(e_back, BA, 0.6), BA, FA]), S.shade(cloth, 0.12), 0,
                   extra='opacity="0.6" filter="url(#soft)"')
        for k in (0.18, 0.3):
            a_ = _lerp2(e_front, FA, k)
            b_ = _lerp2(e_back, BA, k)
            inner += _line(a_[0], a_[1] + 8, b_[0], b_[1] + 8, sw=7, color=stripe, extra='opacity="0.85"')
        inner += _p(f"M{_f(FA[0])},{_f(FA[1])} Q{_f(sag[0])},{_f(sag[1])} {_f(e_back[0])},{_f(e_back[1])}", sw=3,
                    stroke=cloth_d, extra='opacity="0.6"')
        return _p(d, cloth, 0) + _clip(_uid("boothsl", sgn), d, inner) + _p(d, sw=4)
    c = slope(FL, BL, -1) + slope(FR, BR, 1)
    for e, sgn in ((FL, -1), (FR, 1)):
        hem = []
        for i in range(9):
            uu = i / 8
            p = _lerp2(FA, e, uu)
            hem.append((p[0], p[1] + 14 + (8 if i % 2 else 0) + 6 * uu))
        d = _poly([FA, (e[0] + sgn * 8, e[1] + 2)] + list(reversed(hem)))
        c += _p(d, cloth_d, 0) + _clip(_uid("boothhem", sgn), d, _line(FA[0], FA[1] + 10, e[0], e[1] + 12, sw=6,
                                                                       color=stripe, extra='opacity="0.8"'))
        c += _p(d, sw=3.5)
    parts["cloth"] = c
    fr = _stick([(BA[0] - 2, BA[1] - 4), (FA[0] + 2, FA[1] - 2)], 9, wd, 3.2)
    fr += _stick([(BL[0] + 4, BL[1]), (BA[0] + 26, BA[1] - 22)], 8, S.shade(wd, 0.05), 3)
    fr += _stick([(BR[0] - 4, BR[1]), (BA[0] - 22, BA[1] - 20)], 8, S.shade(wd, 0.05), 3)
    fr += _stick([(-176, -228), (-80, -300), (30, -400)], 10, wd, 3.5)
    fr += _stick([(174, -232), (84, -298), (-26, -394)], 10, wd, 3.5)
    parts["frame"] = fr
    parts["lash"] = (_lashing(0, -372) + _lashing(BA[0], BA[1] + 2, 0.8) + _lashing(-158, -262, 0.85) +
                     _lashing(148, -260, 0.85))
    br = ""
    for sx, sy, ang in ((-130, -284, -30), (60, -360, 28)):
        br += _g(_p("M0,0 Q60,-6 128,-2", sw=4, stroke=P["leaf_dark"]) +
                 "".join(_ell(16 + 24 * i, -5 - (i % 2) * 8, 14, 6, P["leaf"] if i % 2 else P["leaf_dark"], 2.5,
                              extra=f'transform="rotate({-30 + 60 * (i % 2)} {16 + 24 * i} {-5 - (i % 2) * 8})"')
                          for i in range(5)), f"translate({sx},{sy}) rotate({ang})")
    parts["branches"] = br
    return parts




# ================================================================== layout (stage px)
SW, SH = 3100, 1300
GY = 1040                         # Jonah's ground line on the ridge path (booth base too)
XB = 1584                         # booth anchor (bottom centre between the front posts)
X_C = XB + 27                     # Jonah hammers, lifts, throws the cloth and sits here (s21: 28 px at its scale)
WALK_STEPS = 3
ADV = 2 * WALK_A / WALK_N * SJ    # stage px the anchor advances per walk drawing (planted sole stays put)
NWALK = WALK_STEPS * WALK_N       # walk drawings from where s19 left him to the booth site
XJ0 = X_C - NWALK * ADV           # where he sits at the start (east of the gate, on the ridge)
AX = 1500                         # every Jonah drawing is made at (AX, GY) and moved by its layer motion
WALL_Y, WALL_H = 790, 250         # Nineveh's east wall (mid-distance)
GATE_X, GATE_W = 780, 150
WALL_X1 = 1180                    # corner tower closing the wall
KW = WALL_H / 260                 # city_wall detail scale
GATE_TOWERS = (GATE_X - GATE_W / 2 - 60 * KW, GATE_X + GATE_W / 2 + 60 * KW)
GT_TOP = WALL_Y - 1.45 * WALL_H - 34 * KW
XBS, YBS = XJ0 + 210, GY - 22     # the bundle lying beside him at the start (centre of the lying bundle)
XBUN, YBUN = XB - 265, GY + 6     # where he tosses it down at the booth site
LIZ = (1992.8, 1028.5)            # lizard anchor (on screen where s21 draws its lizard at the end)
LIZ_STONE = (1988.9, 1070.8, 133, 48)   # ...and its stone (same drawing and seed as s21's)
CX, CY = SW // 2, SH // 2

# --- continuity with the neighbouring scenes (output px of their first / last frames; see the docstring)
S19_J = (1060.4, 926.3)           # s19's last frame: Jonah's anchor on screen ...
S19_S = 1.2 * 1920 / 2066         # ... and his on-screen scale
S19_JX, S19_JY = 1850, 1187.7     # ... and his anchor on s19's stage (to map its light into this stage)
W0 = 1920 * SJ / S19_S
CAM_START = Cam(XJ0 - S19_J[0] * W0 / 1920 + W0 / 2, GY - S19_J[1] * W0 / 1920 + W0 * 9 / 32, W0)
S21_B = (1063.8, 894.6)           # s21's first frame: booth anchor on screen (booth scale 1.3 * 1920/1960)
WF = 1920 * SB / (1.3 * 1920 / 1960)
CAM_END = Cam(XB - S21_B[0] * WF / 1920 + WF / 2, GY - S21_B[1] * WF / 1920 + WF * 9 / 32, WF)
S21_SUN = (230.2, 246.1)          # s21's afternoon sun on screen (flame sun at scale 0.62 * 1920/1960)
SUN = (CAM_END.x - WF / 2 + S21_SUN[0] * WF / 1920, CAM_END.y - WF * 9 / 32 + S21_SUN[1] * WF / 1920)
SUN_S = 0.62 * (1920 / 1960) * WF / 1920
CAM_REF = (CAM_END.x, CAM_END.y)  # sky parallax offsets are zero at the final view

POST_BASE = {"post_fl": (-158, 2), "post_fr": (146, 2), "post_bl": (-112 + PR.BOOTH_DEPTH[0] * 0.9, -16),
             "post_br": (146 + PR.BOOTH_DEPTH[0] * 0.9, -18)}
# invisible spacer the size of the whole booth (local coords): every part layer gets the same filter region
BOOTH_BOX = '<rect x="-262" y="-470" width="566" height="500" fill="none" stroke="none"/>'


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def bstage(lx, ly):
    return (XB + lx * SB, GY + ly * SB)


def m19(x, y):
    """A point of s19's stage -> this stage, through the matched opening view (anchored on Jonah)."""
    r = SJ / 1.2
    return (XJ0 + (x - S19_JX) * r, GY + (y - S19_JY) * r)


def _ease_walk(u, a=0.18):
    """0..1 with a soft start and stop and a constant pace in between (peak speed 1 / (1 - a))."""
    u = min(1.0, max(0.0, u))
    v = 1.0 / (1.0 - a)
    if u < a:
        return v * u * u / (2 * a)
    if u > 1 - a:
        w = 1 - u
        return 1 - v * w * w / (2 * a)
    return v * (u - a / 2)


def _ease_walk_inv(f):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _ease_walk(mid) < f:
            lo = mid
        else:
            hi = mid
    return hi


def _env(t, a, b, c, d):
    if t <= a or t >= d:
        return 0.0
    if t < b:
        return M.progress(t, a, b, "sine")
    if t <= c:
        return 1.0
    return 1 - M.progress(t, c, d, "sine")


def _prev_clock(ctx):
    """The previous scene's (s19's) clock at this scene's t = 0 (its last cross-dissolve second), so the
    opening fidget and breathing run in step with s19's last frames. 0 if the timeline can't be read."""
    try:
        from engine.loader import load_timeline
        tl = load_timeline()
        ids = [s["id"] for s in tl["scenes"]]
        prev = tl["scenes"][ids.index(ctx.id) - 1]
        return float(ctx.start - prev["start"])
    except Exception:
        return 0.0


def _hammer_knocks(t_cue, scene_id):
    """Pick the hammer cue time (near t_cue) whose sound has 4 knocks and return (cue time, knock times).
    audio/mix.py seeds every cue with crc32('scene:name:at'); the knock onsets are read from the rendered sound,
    so the posts pop exactly on the knocks heard. Falls back to the nominal ~0.24 s rhythm."""
    import zlib
    try:
        import numpy as np
        from audio import sfx
        at = round(t_cue, 2)
        for i in range(40):
            cand = round(t_cue + 0.01 * i, 2)
            seed = zlib.crc32(f"{scene_id}:hammer:{cand}".encode()) & 0xFFFF
            rng = sfx._rng("hammer", seed)
            rng.uniform(380, 480)
            if int(rng.integers(3, 5)) == 4:
                at = cand
                break
        seed = zlib.crc32(f"{scene_id}:hammer:{at}".encode()) & 0xFFFF
        x = sfx.make("hammer", None, 48000, seed=seed)
        e = np.abs(x).max(1)
        k = int(0.004 * 48000)
        env = np.convolve(e, np.ones(k) / k, "same")
        thr = env.max()
        on, armed = [], True
        for i, v in enumerate(env):
            if armed and v > 0.45 * thr:
                on.append(i / 48000)
                armed = False
            elif not armed and v < 0.2 * thr and i / 48000 - on[-1] > 0.08:
                armed = True
        if len(on) >= 4:
            return at, [at + o for o in on[:4]]
        if len(on) == 3:
            return at, [at + o for o in on] + [at + on[-1] + 0.24]
    except Exception:
        pass
    at = round(t_cue, 2)
    return at, [at + 0.02 + 0.24 * i for i in range(4)]


# A single footstep: a 'footsteps' loop of 0.45 s at rate 0.5 holds exactly one step, and the loop is rotated
# to start on its quiet point, which puts the step's onset ~0.11 s into the cue (measured over many seeds).
STEP_DUR, STEP_LEAD = 0.45, 0.112


# ------------------------------------------------------------------ little drawings
def _puff(cx, cy, r):
    """Cartoon puff of grumpy steam (as in s11): warm grey with a hot pink-red rim."""
    pts = [(-0.55, 0.1, 0.55), (0.0, -0.25, 0.7), (0.55, 0.05, 0.55), (0.05, 0.32, 0.5)]
    body = "".join(f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#ddd0cb" '
                   f'stroke="#b8473f" stroke-width="8"/>' for dx, dy, k in pts)
    body += "".join(f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{k * r:.1f}" fill="#ddd0cb"/>'
                    for dx, dy, k in pts)
    body += f'<circle cx="{cx - 0.15 * r:.1f}" cy="{cy - 0.42 * r:.1f}" r="{0.17 * r:.1f}" fill="#f8f1ea"/>'
    return S.g(body, filter="wobble-fine")


def _dust(cx, cy, k=1.0, n=4, seed=0):
    """A little poof of dust (outlined cream puffs) sitting on the ground at (cx, cy)."""
    rnd = random.Random(seed)
    circ = [(rnd.uniform(-26, 26) * k, rnd.uniform(-14, 0) * k, rnd.uniform(10, 17) * k) for _ in range(n)]
    out = "".join(f'<circle cx="{cx + dx:.1f}" cy="{cy + dy:.1f}" r="{r:.1f}" fill="#f3e4c4" stroke="{P["ink_soft"]}" '
                  f'stroke-width="5"/>' for dx, dy, r in circ)
    out += "".join(f'<circle cx="{cx + dx:.1f}" cy="{cy + dy:.1f}" r="{r:.1f}" fill="#f3e4c4"/>' for dx, dy, r in circ)
    return S.g(out, filter="wobble-fine")


def _palm(x, y, s, lean=0.0):
    return PR.palm_tree(x, y, s, lean=lean)


# --- s21's afternoon sun (v1 hot sun: wavy flame rays + short wedges, bright disc), drawn at the doc centre
def flame_rays_svg():
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
        left = [(CX + r * ca - (off - w_) * sa, CY + r * sa + (off - w_) * ca) for r, off, w_ in pts]
        right = [(CX + r * ca - (off + w_) * sa, CY + r * sa + (off + w_) * ca) for r, off, w_ in pts]
        ray_d += S.smooth_path(left + right[::-1], closed=True, tension=0.8) + " "
    short = S.rays(CX, CY, 120, 215, n=14, width_deg=11, rot=12.9)
    return doc(S.g(
        f'<path d="{short}" fill="#ffd34d" stroke="#b9621c" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="{ray_d}" fill="#ffb83a" stroke="#b9621c" stroke-width="4.5" stroke-linejoin="round"/>',
        filter="wobble"))


def hot_disc_svg():
    return doc(
        f'<circle cx="{CX}" cy="{CY}" r="185" fill="url(#hg)"/>' +
        S.g(f'<circle cx="{CX}" cy="{CY}" r="118" fill="#ffd94f" stroke="#c9741f" stroke-width="6"/>'
            f'<circle cx="{CX}" cy="{CY}" r="90" fill="#fff1a8"/>'
            f'<circle cx="{CX}" cy="{CY}" r="58" fill="#fffae0"/>'
            f'<circle cx="{CX - 34}" cy="{CY - 34}" r="26" fill="#fffef6" opacity="0.9"/>', filter="wobble"),
        S.rad_grad("hg", [(0, "#fffef4", 1), (0.6, "#fff6cf", 0.85), (0.8, "#ffeaa0", 0.4), (1, "#ffe08a", 0)]))


# --- the joyful city's decorations (as s19's, scaled to this wall)
BUNT_COLS = ("#e45e52", "#f2c14e", "#3f78b5", "#f3a0a8", "#3b8b89", "#fff3d6")


def _banner(cx, top, w, h, col):
    """Long festive banner hanging on a tower: swallow-tail end, gold sun disc (s19)."""
    x0, x1 = cx - w / 2, cx + w / 2
    d = f"M{x0:.1f},{top:.1f} L{x1:.1f},{top:.1f} L{x1:.1f},{top + h:.1f} L{cx:.1f},{top + h - 0.15 * h:.1f} L{x0:.1f},{top + h:.1f} Z"
    out = (f'<rect x="{x0 - 6:.1f}" y="{top - 6:.1f}" width="{w + 12:.1f}" height="8" rx="3" fill="{P["wood"]}" '
           f'stroke="{INK}" stroke-width="2.5"/>')
    out += S.path(d, fill=col, sw=3)
    out += (f'<circle cx="{cx:.1f}" cy="{top + h * 0.38:.1f}" r="{w * 0.26:.1f}" fill="{P["gold"]}" stroke="{INK}" '
            f'stroke-width="2"/>')
    out += f'<path d="M{x0:.1f},{top + 12:.1f} L{x1:.1f},{top + 12:.1f}" stroke="{P["gold"]}" stroke-width="3"/>'
    return out


def _bunting(spans, k=1.0):
    out = ""
    n_ = 0
    for (x0, x1, y0, sag) in spans:
        n = max(4, int((x1 - x0) / (30 * k)))
        pts = [(x0 + (x1 - x0) * i / 30, y0 + sag * math.sin(math.pi * i / 30)) for i in range(31)]
        out += S.path(S.smooth_path(pts, closed=False), sw=2.2)
        for i in range(n):
            u = (i + 0.5) / n
            x = x0 + (x1 - x0) * u
            y = y0 + sag * math.sin(math.pi * u)
            c = BUNT_COLS[n_ % len(BUNT_COLS)]
            n_ += 1
            out += (f'<path d="M{x - 9 * k:.1f},{y:.1f} L{x + 9 * k:.1f},{y:.1f} L{x + 1:.1f},{y + 22 * k:.1f} Z" '
                    f'fill="{c}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    return out


def _pennants(phase, tops, k=1.0):
    """Little flags on poles on the gate towers (s19); ``phase`` flutters them."""
    out = ""
    for i, (x, y, col) in enumerate(tops):
        out += (f'<path d="M{x:.1f},{y + 30 * k:.1f} L{x:.1f},{y - 62 * k:.1f}" stroke="{INK}" stroke-width="6" '
                f'stroke-linecap="round"/><path d="M{x:.1f},{y + 30 * k:.1f} L{x:.1f},{y - 62 * k:.1f}" '
                f'stroke="{P["wood"]}" stroke-width="3" stroke-linecap="round"/>')
        ph = phase + i * 0.9
        L = 68 * k
        top = [(x + L * j / 4, y - 58 * k + 5 * k * math.sin(ph + j * 1.3) * j / 4) for j in range(5)]
        bot = [(x + L * j / 4, y - 26 * k - 12 * k * j / 4 + 5 * k * math.sin(ph + j * 1.3 + 0.4) * j / 4)
               for j in range(5)]
        tip = (x + L + 5 * k, y - 46 * k + 6 * k * math.sin(ph + 5.5))
        out += S.path(S.smooth_path(top + [tip] + bot[::-1], tension=0.6), fill=col, sw=2.6)
    return out


HAZE = ('<filter id="hz" x="-2%" y="-8%" width="104%" height="116%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="saturate" values="0.75"/>'
        '<feColorMatrix type="matrix" values="0.78 0 0 0 0.2  0 0.78 0 0 0.183  0 0 0.78 0 0.15  0 0 0 1 0"/>'
        '</filter>')


def hazed(body):
    """A document whose body is hazed like the distant city (colour-only filter, so layers can be split)."""
    return doc(f'<g filter="url(#hz)">{body}</g>', HAZE)


# ================================================================== build
def build(ctx):
    from PIL import Image, ImageDraw

    from art.scenes_v1 import s02_call as V2
    from art.scenes_v1 import s11_vine as V11
    from art.scenes_v1 import s12_lesson as V12

    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]
    T19 = _prev_clock(ctx)                     # s19's clock at t = 0

    # ------------------------------------------------------------ key times (from the narration chunks)
    t_fade = L0.at("没有回答")                    # God's light fades: no answer...
    t_hmph = L0.at("没有回答") + 0.25             # ..."hmph!" (still sitting, arms crossed)
    t_up = t_hmph + 0.58                          # hops to his feet, facing east
    t_grab = t_up + 0.28                          # swings the bundle up over his head...
    t_on = t_grab + 0.27                          # ...onto his back
    t_walk0 = max(t_on + 0.1, L0.at("出了城") - 0.05)    # "他出了城，坐在城的东边" trudges east
    t_ham = L0.at("搭了")                         # "为自己搭了一座小棚子": posts knocked in...
    t_arr = t_ham - 0.75                          # arrives on the knoll (both feet planted)...
    t_plant = t_arr - 0.1
    t_toss, t_land = t_arr, t_arr + 0.34          # ...shrugs the bundle off: it lands beside him
    t_down = t_arr + 0.3                          # back to standing
    hammer_at, knocks = _hammer_knocks(t_ham + 0.13, ctx.id)
    t_lift = knocks[-1] + 0.3                     # ...the frame lifted above his head...
    t_frame_on = t_lift + 0.36                    # ...drops onto the posts
    t_throw = t_lift + 0.62                       # ...the cloth thrown over the ridge
    t_cloth0, t_cloth1 = t_throw + 0.05, t_throw + 0.42
    t_branch = t_throw + 0.55
    t_tired = t_throw + 0.62                      # phew, hot! (sweat)
    t_sit = L1.start + 0.12                       # "他坐在棚子下面的阴凉里"
    t_chin = L1.at("要看看") + 0.22               # chin on fist, eyes on the city
    t_dove = t_chin + 0.1                         # doves fly off toward the city
    t_rest = min(L1.end + 0.05, T - 1.35)         # hands back on the knees: s21's opening pose
    blinks = [t_chin + 1.0, t_chin + 2.0]

    def walk_k(t):
        if t <= t_walk0:
            return 0
        if t >= t_plant:
            return NWALK
        return min(NWALK, int(_ease_walk((t - t_walk0) / (t_plant - t_walk0)) * NWALK + 1e-6))

    # footfalls: the swing foot lands on every contact drawing (k = WALK_N, 2 WALK_N, ...)
    contacts = [t_walk0 + (t_plant - t_walk0) * _ease_walk_inv(m / WALK_STEPS) for m in range(1, WALK_STEPS + 1)]

    # ------------------------------------------------------------ camera (built first: parallax uses it)
    c0 = CAM_START
    cam = M.cam_keys([
        (0.0, c0),
        (1.0, c0),                                          # still through the dissolve from s19...
        (t_up - 0.05, Cam(c0.x + 3, c0.y, c0.w - 4)),       # ...and nearly so through the hmph
        (t_ham + 0.25, Cam(XB - 130, 736, 1800)),
        (t_tired + 0.3, Cam(XB - 110, 738, 1780)),
        (L1.at("要看看") + 0.1, Cam(XB - 20, 770, 1600)),
        (min(T - 1.1, L1.at("要看看") + 2.9), CAM_END),     # settles on s21's framing before the dissolve
        (T, CAM_END),
    ], "sine")
    sc.camera = cam

    def par(k, extra=None):
        """Parallax: shift a distant layer by k * (camera offset from the final view)."""
        def m(t):
            c = cam(t)
            return Tf(dx=k * (c.x - CAM_REF[0]), dy=k * (c.y - CAM_REF[1]))
        return M.combine(m, extra) if extra else m

    # =========================================================== SKY
    sky = doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="820" fill="url(#g)"/>',
              S.lin_grad("g", [(0, "#8cc4d9"), (0.4, "#bfdfdc"), (0.72, "#f0deb4"), (1, "#f6d49d")]))
    sc.add("sky", sky, wc=0.5)
    # the sun: s21's flame sun, turning and breathing on s21's clock so the end dissolve matches
    tz = T - 1.0                                   # s21's t = 0
    at_sun = lambda t: Tf(dx=SUN[0] - CX, dy=SUN[1] - CY)
    sc.add("sun_rays", flame_rays_svg(), wc=0.3, motion=par(0.6, M.combine(
        at_sun, lambda t: Tf(rot=7 * (t - tz), px=CX, py=CY), M.breathe(0.03, 1.1, pivot=(CX, CY), phase=-tz / 1.1),
        lambda t: Tf(sx=SUN_S, sy=SUN_S, px=CX, py=CY))))
    sc.add("sun_disc", hot_disc_svg(), wc=0.4, motion=par(0.6, M.combine(
        at_sun, M.breathe(0.03, 1.4, pivot=(CX, CY), phase=-tz / 1.4),
        lambda t: Tf(sx=SUN_S, sy=SUN_S, px=CX, py=CY))))
    clouds = doc(S.g(S.cloud(260, 150, 230, 70, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(1330, 170, 210, 64, "#fdf1e2", seed=6, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2240, 250, 260, 80, "#fdf3e4", seed=8, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2930, 200, 220, 66, "#fdf1e2", seed=9, sw=3, shade_fill="#f0d6c4"), filter="wobble"))
    sc.add("clouds", clouds, wc=0.7, motion=par(0.5, M.drift(vx=-6)))

    # =========================================================== FAR DUNES (parallax)
    far = S.path(S.smooth_path([(-140, 716), (220, 690), (560, 702), (940, 680), (1320, 664), (1700, 688),
                                (2080, 660), (2480, 682), (2860, 656), (3260, 676)], closed=False) +
                 " L3260,820 L-140,820 Z", fill="#ead8b8", sw=3, extra='stroke-opacity="0.55"')
    far += S.path(S.smooth_path([(1150, 740), (1500, 712), (1900, 726), (2300, 704), (2700, 720), (3260, 702)],
                                closed=False) + " L3260,820 L1150,820 Z", fill="#e5cda2", sw=3,
                  extra='stroke-opacity="0.55"')
    for (x, y, s_) in [(1640, 690, 0.1), (1680, 694, 0.08), (2560, 682, 0.1), (2960, 668, 0.09)]:
        far += PR.palm_tree(x, y, s_, lean=0.1)
    sc.add("far_dunes", doc(S.g(far, filter="wobble")), wc=0.6, motion=par(0.25))

    # =========================================================== PLAIN, CITY (static, flattened)
    pl = (f'<rect x="-40" y="722" width="{SW + 80}" height="{SH - 700}" fill="url(#pl)"/>'
          f'<path d="M-40,722 L{SW + 40},722" stroke="{INK}" stroke-width="3" opacity="0.45"/>')
    rnd = random.Random(7)
    for i in range(40):        # far shrubs dotting the dry plain east of the city
        x = rnd.uniform(1150, SW)
        y = rnd.uniform(734, 900)
        k = 0.6 + (y - 730) / 260
        pl += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{9 * k:.1f}" ry="{4.5 * k:.1f}" fill="#b7a274" opacity="0.6"/>'
    for (x, y, w_) in [(1500, 860, 160), (2100, 820, 200), (2700, 880, 180), (1320, 930, 140), (2500, 930, 160)]:
        pl += (f'<path d="M{x - w_ / 2},{y} q{w_ / 2},-12 {w_},0" fill="none" stroke="#d6b582" stroke-width="4" '
               f'opacity="0.6" stroke-linecap="round"/>')

    def band(x0, x1, y, h, amp, seed):
        """Soft dune swell: sunlit crest and shaded trough across the dry plain."""
        r_ = random.Random(seed)
        n = 7
        top = [(x0 + (x1 - x0) * i / n, y - amp * math.sin(math.pi * i / n) + r_.uniform(-6, 6)) for i in range(n + 1)]
        bot = [(x1 - (x1 - x0) * i / n, y + h - 0.5 * amp * math.sin(math.pi * i / n) + r_.uniform(-5, 5))
               for i in range(n + 1)]
        return S.smooth_path(top + bot, closed=True, tension=0.8)
    for (x0, x1, y, h, amp, col, op, sd) in [(1180, 2300, 770, 26, 12, "#f6e7c4", 0.7, 1),
                                            (2050, 3180, 790, 30, 16, "#f6e7c4", 0.7, 2),
                                            (1250, 2150, 850, 40, 10, "#d8b47e", 0.32, 3),
                                            (2200, 3180, 880, 46, 12, "#d8b47e", 0.32, 4),
                                            (1500, 2600, 940, 34, 8, "#f3e0b6", 0.5, 5)]:
        pl += f'<path d="{band(x0, x1, y, h, amp, sd)}" fill="{col}" opacity="{op}"/>'
    # green, watered fields along the wall (the city side) fading into the dry desert to the east
    pl += '<rect x="-40" y="790" width="1500" height="200" fill="url(#gf)"/>'
    xs = [-60, 200, 430, 640, 900, 1110, 1330]
    cols = ["#c9cc7e", "#b5c271", "#dcc47c", "#c3cf86", "#b9c777", "#d8c986"]
    for i in range(len(xs) - 1):
        pl += V12._field(xs[i] + 10, xs[i + 1] - 10, WALL_Y + 14, WALL_Y + 56 + 18 * (i % 3), cols[i], seed=40 + i)
    # the road out of the gate, across the plain to the ridge
    road = S.smooth_path([(GATE_X - 46, WALL_Y + 2), (GATE_X - 30, 850), (900, 930), (1040, 1000),
                          (1210, 1000), (1060, 930), (GATE_X + 70, 852), (GATE_X + 46, WALL_Y + 2)],
                         closed=True, tension=0.8)
    pl += f'<path d="{road}" fill="#f3e2b6" stroke="{INK}" stroke-width="3" opacity="0.95"/>'
    pl += (f'<path d="M{GATE_X},{WALL_Y + 20} Q{GATE_X + 60},900 1110,995" fill="none" stroke="#dcc28c" '
           f'stroke-width="5" stroke-dasharray="2 24" stroke-linecap="round"/>')
    # a distant oasis to the east; sheep grazing by the fields (the fast is over: no sackcloth any more)
    for (x, y, s_, ln) in [(2620, 742, 0.16, 0.1), (2668, 746, 0.13, -0.1), (2715, 744, 0.15, 0.05)]:
        pl += PR.palm_tree(x, y, s_, lean=ln)
    pl += PR.bush(2560, 750, 0.22, variant=0) + PR.bush(2760, 752, 0.2, variant=0)
    for (x, y, s_, f_) in [(470, 900, 0.3, 1), (560, 912, 0.27, -1), (1030, 905, 0.26, -1)]:
        pl += PR.animal(x, y, s_, f_, kind="sheep")
    plain_defs = (S.lin_grad("pl", [(0, "#efdcb2"), (0.3, "#ead1a0"), (1, "#dcb57c")]) +
                  S.lin_grad("gf", [(0, "#c9cf86", 0.55), (0.6, "#d6cf8c", 0.3), (1, "#e0d29a", 0)], x2=1, y2=0))
    sc.add("plain", doc(S.g(pl, filter="wobble"), plain_defs), wc=0.8)

    # Nineveh, saved and glad: skyline behind the east wall, people in their own clothes on the wall walk
    # (two children hop and cheer), the open gate with banners, bunting and pennants (hazy with distance)
    walk_y = WALL_Y - WALL_H + 28
    walkers = ""
    for i, (x, kind, pose, expr) in enumerate([(120, "man", "stand", "happy"), (150, "woman", "cheer", None),
                                               (520, "man", "stand", None), (545, "woman", "stand", "happy"),
                                               (980, "elder", "stand", "happy")]):
        walkers += C.citizen(x, walk_y, 0.2, 1 if i % 2 else -1, kind=kind, variant=i % 4, pose=pose, expr=expr)
    city = PR.nineveh_skyline(-80, 1140, WALL_Y - 18, scale=0.72, seed=2, haze=0.35, tint="#f3dcb4")
    sc.add("city_back", hazed(city + walkers), wc=0.7)
    # cheering children: on the wall walk and in the gateway (hop-and-wave flipbooks, as s19's crowd)
    cheer = [(330, walk_y - 16, 0.22, 1, 2, 70, 12), (1010, walk_y - 16, 0.22, -1, 3, 71, 12)]
    for i, (x, y, s_, f_, var, seed, hh) in enumerate(cheer):
        frames = [hazed(C.citizen(x, y, s_, f_, kind="child", variant=var, pose=p)) for p in ("stand", "cheer")]
        hops = V12.hop_sched(seed, T, n=(2, 3), dur=(0.4, 0.52), rest=(0.5, 1.2))
        sc.add(f"wall_child{i}", frames, frame_at=V12.hop_frame(hops), motion=V12.hop_motion(x, y, hops, hh), wc=0.5)
    wall = PR.city_wall(-80, WALL_X1, WALL_Y, WALL_H, gate=(GATE_X, GATE_W), doors_open=1.0, seed=4, ink=0.7)
    wall += V12._end_tower(WALL_X1, WALL_Y, WALL_H / 260, ink=0.7)
    deco = ""
    for i, cx in enumerate(GATE_TOWERS):
        deco += _banner(cx, GT_TOP + 140 * KW, 50 * KW, 136 * KW, ("#c0533a", "#3f78b5")[i])
    deco += _bunting([(GATE_TOWERS[0] + 36 * KW, GATE_TOWERS[1] - 36 * KW, GT_TOP + 112 * KW, 44 * KW),
                      (60, 470, WALL_Y - WALL_H + 20, 34), (1000, WALL_X1 - 20, WALL_Y - WALL_H + 20, 26)], KW)
    gateway = C.citizen(GATE_X - 30, WALL_Y - 2, 0.36, 1, kind="woman", variant=3, pose="stand", expr="happy")
    trees = ""
    for (x, y, s_, ln) in [(60, WALL_Y + 12, 0.36, 0.1), (410, WALL_Y + 14, 0.34, -0.1), (1010, WALL_Y + 10, 0.38, 0.15),
                           (1290, WALL_Y + 22, 0.42, -0.12), (1385, WALL_Y + 30, 0.34, 0.1)]:
        trees += _palm(x, y, s_, ln)
    trees += PR.olive_tree(1160, WALL_Y + 40, 0.3, seed=1) + PR.olive_tree(560, WALL_Y + 36, 0.28, seed=2)
    sc.add("city_wall", hazed(wall + S.g(deco, filter="wobble-fine") + gateway), wc=0.7)
    gx_, gy_ = GATE_X + 28, WALL_Y - 2
    frames = [hazed(C.citizen(gx_, gy_, 0.32, -1, kind="child", variant=1, pose=p)) for p in ("stand", "cheer")]
    hops = V12.hop_sched(77, T, n=(2, 3), dur=(0.42, 0.54), rest=(0.6, 1.3))
    sc.add("gate_child", frames, frame_at=V12.hop_frame(hops), motion=V12.hop_motion(gx_, gy_, hops, 16), wc=0.5)
    tops = [(GATE_TOWERS[0], GT_TOP - 26 * KW, "#e45e52"), (GATE_TOWERS[1], GT_TOP - 26 * KW, "#f2c14e")]
    sc.add("pennants", [hazed(S.g(_pennants(ph, tops, KW), filter="wobble-fine")) for ph in (0.0, 2.1, 4.2)],
           frame_at=lambda t: float(int(t * 5) % 3), wc=0.5)
    sc.add("city_trees", hazed(trees), wc=0.7)

    # mid-plain: bushes and stones on the dry ground east of the city
    mid = ""
    for (x, y, s_, v) in [(1450, 905, 0.5, 2), (1790, 872, 0.45, 2), (2240, 900, 0.52, 2), (2680, 870, 0.46, 2),
                          (2950, 915, 0.5, 2), (860, 960, 0.5, 0), (300, 945, 0.55, 3)]:
        mid += PR.bush(x, y, s_, variant=v)
    for (x, y, w_, h_, sd) in [(1240, 925, 90, 44, 3), (1300, 930, 40, 20, 13), (2420, 915, 76, 38, 4),
                               (2830, 940, 96, 48, 6), (1040, 965, 60, 30, 7)]:
        mid += V11._stone(x, y, w_, h_, seed=sd, sw=3)
    sc.add("mid", doc(mid), wc=0.8)

    # =========================================================== THE RIDGE (rising into the booth's knoll)
    ridge_pts = [(-80, 1012), (250, 1004), (600, 998), (900, 994), (1150, 982), (1380, 942), (1600, 912),
                 (1830, 918), (2070, 940), (2350, 958), (2650, 974), (2900, 986), (3180, 992)]
    kd = S.smooth_path(ridge_pts, closed=False) + f" L{SW + 80},{SH + 80} L-80,{SH + 80} Z"
    rg = S.path(kd, fill="url(#kn)", sw=4)
    rp = [(x, y + 16) for x, y in ridge_pts[1:-1]]
    rg += f'<path d="{S.smooth_path(rp, closed=False)}" fill="none" stroke="#f2d39b" stroke-width="14" opacity="0.5"/>'
    # the road climbs onto the ridge and becomes Jonah's footpath east
    path_d = S.smooth_path([(1060, 992), (1200, 990), (1330, 1018), (1700, 1014), (2150, 1012), (2420, 1024),
                            (2560, 1046), (2380, 1070), (2000, 1074), (1500, 1074), (1230, 1072), (1120, 1040),
                            (1020, 1000)], closed=True, tension=0.8)
    rg += f'<path d="{path_d}" fill="#f2deb0" opacity="0.9"/>'
    for (x, y) in [(300, 1100), (700, 1150), (1400, 1120), (2300, 1130), (2750, 1100), (1050, 1230), (2600, 1240)]:
        rg += (f'<path d="M{x - 80},{y} q80,-16 160,0" fill="none" stroke="#c4935a" stroke-width="4" '
               f'opacity="0.45" stroke-linecap="round"/>')
    for (x, y, s_, sd) in [(500, 1080, 70, 1), (900, 1110, 54, 2), (1300, 1150, 60, 3), (2250, 1110, 64, 4),
                           (2620, 1070, 50, 5), (2950, 1130, 60, 6), (1750, 1170, 56, 8)]:
        rg += V11._cracks(x, y, s_, seed=sd)
    sc.add("ridge", doc(S.g(rg, filter="wobble"),
                        S.lin_grad("kn", [(0, "#e7bf80"), (0.25, "#ddad6b"), (1, "#c58e57")])), wc=0.9)
    # the doves start hidden behind the bush on the ridge (layer just under the rocks / bushes)
    DOVE0 = (1232, 968)
    z_doves = len(sc.layers) + len(sc.dynamics) - 0.5
    rocks = ""
    for (x, y, s_, sd, n) in [(1290, 1006, 0.9, 3, 3), (2480, 1000, 1.0, 4, 2), (760, 1030, 0.8, 5, 2),
                              (1580, 1100, 0.9, 6, 2), (2860, 1040, 1.0, 7, 3)]:
        rocks += V11._pebbles(x, y, s_, seed=sd, n=n)
    for (x, y, s_, v) in [(1235, 1000, 0.62, 2), (2560, 985, 0.72, 2), (420, 1004, 0.6, 2)]:
        rocks += PR.bush(x, y, s_, variant=v)
    rocks += V11._stone(*LIZ_STONE, seed=41, sw=4, crack=True)
    sc.add("ridge_rocks", doc(S.g(rocks, filter="wobble-fine")), wc=0.8)

    # God's question still hangs in the air at the start: the soft golden light of s19's last frame, coming
    # down from the upper right onto Jonah (mapped from s19's stage); it fades as he answers nothing.
    gx, gy = m19(2230, 262)
    tx, ty = m19(S19_JX + 20, S19_JY + 30)
    r19 = SJ / 1.2
    main = math.degrees(math.atan2(ty - gy, tx - gx))
    length = math.hypot(tx - gx, ty - gy) + 160 * r19
    hx, hy = m19(S19_JX + 20, S19_JY - 125 * 1.2)
    gdef = (f'<linearGradient id="rayg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy:.0f}" x2="0" y2="{ty + 100:.0f}">'
            f'<stop offset="0" stop-color="#fff6d2" stop-opacity="0.85"/>'
            f'<stop offset="0.6" stop-color="#ffeaa8" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#ffe08e" stop-opacity="0.12"/></linearGradient>'
            f'<linearGradient id="coneg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy:.0f}" x2="0" y2="{ty + 100:.0f}">'
            f'<stop offset="0" stop-color="#fff2c4" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#ffe39a" stop-opacity="0.2"/></linearGradient>' +
            S.rad_grad("hg", [(0, "#fffbec", 0.95), (0.25, "#fff0c0", 0.7), (0.6, "#ffd98a", 0.28), (1, "#ffd27a", 0)]) +
            S.rad_grad("pool", [(0, "#fff1c0", 0.85), (0.6, "#ffe39a", 0.35), (1, "#ffd77e", 0)]) +
            S.rad_grad("halo", [(0, "#fff6d6", 0.75), (0.6, "#ffe7a4", 0.32), (1, "#ffe0a0", 0)]))
    offs = [(-15, 2.6), (-9, 3.4), (-3.5, 2.2), (2, 3.8), (7.5, 2.4), (13, 3.0),
            (-12, 2.0), (-6.2, 2.6), (-0.5, 1.8), (4.8, 2.2), (10.2, 2.0), (16, 1.8)]
    light = (f'<ellipse cx="{gx:.0f}" cy="{gy + 30 * r19:.0f}" rx="{560 * r19:.0f}" ry="{330 * r19:.0f}" fill="url(#hg)"/>'
             f'<path d="{V2._fan(gx, gy + 10, length, [main], [20])}" fill="url(#coneg)" filter="url(#blur-lg)"/>'
             f'<path d="{V2._fan(gx, gy + 8, length, [main + o for o, _w in offs], [w for _o, w in offs])}" '
             f'fill="url(#rayg)" opacity="0.8" filter="url(#soft)"/>'
             f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{200 * 1.2 * r19:.0f}" ry="{190 * 1.2 * r19:.0f}" fill="url(#halo)"/>'
             f'<ellipse cx="{tx:.0f}" cy="{GY + 2:.0f}" rx="{260 * 1.2 * r19:.0f}" ry="{58 * 1.2 * r19:.0f}" '
             f'fill="url(#pool)"/>')
    a_light = lambda t: 0.85 * (1 - M.progress(t, t_fade, t_fade + 1.1, "sine"))
    sc.add("god_light", doc(light, gdef), wc=0,
           motion=lambda t: Tf(alpha=a_light(t) * (0.92 + 0.08 * math.sin(2 * math.pi * (t + T19) / 2.6))))

    # =========================================================== THE BOOTH (built in stages)
    parts = booth_parts()

    def bdoc(keys):
        return doc(PR._place("".join(parts[k] for k in keys) + BOOTH_BOX, XB, GY, SB, 1))

    # ground shade under the roof (thin cloth: a soft cool shadow), appears with the cloth
    a_roof = lambda t: M.progress(t, t_cloth0 + 0.1, t_cloth1 + 0.3, "sine")
    sc.add("booth_gshade", doc(f'<ellipse cx="{XB + 14 * SB:.0f}" cy="{GY - 4}" rx="{196 * SB:.0f}" ry="{34 * SB:.0f}" '
                               f'fill="#8f7c8a" opacity="0.6" filter="url(#soft)"/>'),
           wc=0, blend="multiply", motion=lambda t: Tf(alpha=a_roof(t)))

    pop_t = {"post_fr": knocks[0], "post_br": knocks[1], "post_bl": knocks[2], "post_fl": knocks[3]}

    def post_motion(name):
        tp_ = pop_t[name]
        bx, by = bstage(*POST_BASE[name])
        knocked = name == "post_fr"                # the one beside him: driven in with a squash

        def m(t):
            if t < tp_ - 0.05:
                return Tf(alpha=0.0)
            u = t - (tp_ - 0.05)
            a = min(1.0, u / 0.05)
            if not knocked:                        # the others rise softly out of the ground on the knocks
                sy = 0.2 + 0.8 * M.ease("out")(min(1.0, u / 0.24))
                return Tf(sy=sy, alpha=a, px=bx, py=by)
            if u < 0.08:
                sy = 0.5 + 0.58 * M.ease("out")(u / 0.08)
            else:
                sy = 1.08 - 0.08 * M.progress(u, 0.08, 0.24, "sine")
            sx = 1 + 0.5 * (1 - sy) if sy < 1 else 1 - 0.35 * (sy - 1)
            return Tf(sx=sx, sy=sy, alpha=a, px=bx, py=by)
        return m

    def frame_motion(t):
        """Appears in his raised hands on the lift cut, goes up a little more, then drops onto the posts."""
        if t < t_lift - 0.01:
            return Tf(alpha=0.0)
        u = t - t_lift
        a = 1.0                                    # appears in his hands on the (hop-hidden) pose cut
        if u < 0.16:
            dy = -26 - 30 * M.ease("out")(u / 0.16)
        elif t < t_frame_on:
            dy = -56 * (1 - M.ease("in")(M.progress(t, t_lift + 0.16, t_frame_on, "linear")))
        else:
            v = t - t_frame_on
            dy = -10 * math.sin(math.pi * min(1.0, v / 0.16)) if v < 0.16 else 0.0
        return Tf(dy=dy, alpha=a)

    def lash_motion(t):
        if t < t_frame_on + 0.08:
            return Tf(alpha=0.0)
        return Tf(alpha=M.progress(t, t_frame_on + 0.08, t_frame_on + 0.2, "sine"))

    apex = bstage(0, -374)

    def cloth_reveal(delay=0.0):
        return lambda t: {"mode": "down", "frac": M.progress(t, t_cloth0 + delay, t_cloth1 + delay, "out"),
                          "soft": 50}

    def cloth_motion(t):
        if t < t_cloth0:
            return Tf(alpha=0.0)
        u = t - t_cloth0
        sy = 1 + 0.06 * math.exp(-u / 0.25) * math.cos(u * 14)
        # then it just breathes a little in the warm air
        k = M.progress(u, 0.6, 1.4, "sine")
        sy += k * (0.011 * math.sin(2 * math.pi * t / 2.1) + 0.004 * math.sin(2 * math.pi * t / 0.83))
        return Tf(sy=sy, rot=k * 0.25 * math.sin(2 * math.pi * t / 2.9), px=apex[0], py=apex[1])

    def branch_motion(t):
        if t < t_branch:
            return Tf(alpha=0.0)
        u = t - t_branch
        s = 0.8 + 0.2 * M.ease("back")(min(1.0, u / 0.22))
        return Tf(sx=s, sy=s, alpha=min(1.0, u / 0.08), px=apex[0], py=apex[1] + 40)

    sc.add("post_bl", bdoc(["post_bl"]), motion=post_motion("post_bl"), wc=0.8)
    sc.add("post_br", bdoc(["post_br"]), motion=post_motion("post_br"), wc=0.8)
    sc.add("under", bdoc(["under"]), motion=lambda t: Tf(alpha=1.0 if t >= t_cloth0 else 0.0),
           reveal=cloth_reveal(0.04), wc=0.8)
    sc.add("post_fl", bdoc(["post_fl"]), motion=post_motion("post_fl"), wc=0.8)
    sc.add("post_fr", bdoc(["post_fr"]), motion=post_motion("post_fr"), wc=0.8)
    sc.add("tiebar", bdoc(["tiebar"]), motion=frame_motion, wc=0.8)
    sc.add("cloth", bdoc(["cloth"]), motion=cloth_motion, reveal=cloth_reveal(), wc=0.8)
    sc.add("frame", bdoc(["frame"]), motion=frame_motion, wc=0.8)
    sc.add("lash", bdoc(["lash"]), motion=lash_motion, wc=0.6)
    sc.add("branches", bdoc(["branches"]), motion=branch_motion, wc=0.7)

    # dust where each post goes in
    for name in ("post_fl", "post_fr", "post_bl", "post_br"):
        bx, by = bstage(*POST_BASE[name])
        tp_ = pop_t[name]

        def dmo(t, tp_=tp_, bx=bx, by=by):
            u = t - tp_
            if not 0 <= u < 0.45:
                return Tf(alpha=0.0)
            s = 0.5 + 0.7 * M.ease("out")(u / 0.45)
            return Tf(dy=-5 * M.ease("out")(u / 0.45), sx=s, sy=s, alpha=0.9 * (1 - M.progress(u, 0.1, 0.45, "sine")),
                      px=bx, py=by)
        sc.add(f"dust_{name}", doc(_dust(bx, by, 0.85, 4, seed=len(name) + int(bx))), motion=dmo, wc=0.3)

    # =========================================================== JONAH (drawings)
    frames, flat, tint_idx = [], [], {}
    FLAT = (f'<filter id="flat" filterUnits="userSpaceOnUse" x="0" y="0" width="{SW}" height="{SH}" '
            f'color-interpolation-filters="sRGB"><feColorMatrix type="matrix" '
            f'values="0 0 0 0 0.62  0 0 0 0 0.6  0 0 0 0 0.8  0 0 0 1 0"/></filter>')

    def jadd(label, ps, facing, expr, bundle=False, stone=False, tint=False):
        m, _ = jonah_fig(AX, GY, SJ, facing, ps, expr, bundle=bundle, stone=stone, label=label)
        frames.append(doc(m))
        if tint:
            tint_idx[len(frames) - 1] = len(flat)
            flat.append(doc(S.g(m, filter="flat"), FLAT))
        return len(frames) - 1

    F_SULK = jadd("sulk", POSE["sulk"], -1, "angry")
    F_HMPH = jadd("hmph", POSE["sulk_hmph"], -1, "hmph")
    F_STAND = jadd("stand", POSE["stand"], 1, "angry")
    F_HEAVE = jadd("heave", POSE["heave"], 1, "angry")
    F_WALK = [jadd(f"walk{k}", walk_pose(k), 1, "angry", bundle=True) for k in range(2 * WALK_N)]
    bx0_, by0_, ang0_ = _BACK["walk0"]
    BACK0 = (XJ0 + bx0_ * SJ, GY + by0_ * SJ, ang0_)         # where the bundle sits once it is on his back
    bx_, by_, ang_ = _BACK[f"walk{NWALK % (2 * WALK_N)}"]
    BACK = (X_C + bx_ * SJ, GY + by_ * SJ, ang_)             # ...and where it is when he arrives
    F_TOSS = jadd("toss", POSE["toss"], 1, "angry")
    F_HUP = jadd("ham_up", POSE["ham_up"], 1, "angry", stone=True)
    F_HDN = jadd("ham_dn", POSE["ham_dn"], 1, "angry", stone=True)
    F_LIFT = jadd("lift", POSE["lift"], 1, "angry")
    F_THROW = jadd("throw", POSE["throw"], 1, "angry", tint=True)
    F_TIRED = jadd("tired", POSE["stand"], 1, "tired", tint=True)
    F_SIT = jadd("sit", POSE["sit"], -1, "peaceful", tint=True)
    F_CHIN = jadd("chin", POSE["sit_chin"], -1, "watch", tint=True)
    F_BLINK = jadd("blink", POSE["sit_chin"], -1, "watch_blink", tint=True)
    F_REST = jadd("rest", POSE["sit"], -1, "watch", tint=True)

    def j_frame(t):
        if t < t_hmph:
            return F_SULK
        if t < t_up:
            return F_HMPH
        if t < t_grab:
            return F_STAND
        if t < t_on:
            return F_HEAVE
        if t < t_arr:
            return F_WALK[walk_k(t) % (2 * WALK_N)]
        if t < t_down:
            return F_TOSS
        if t < t_ham:
            return F_STAND
        if t < t_lift:
            return F_HDN if any(kn - 0.05 <= t < kn + 0.1 for kn in knocks) else F_HUP
        if t < t_throw:
            return F_LIFT
        if t < t_tired:
            return F_THROW
        if t < t_sit:
            return F_TIRED
        if t < t_chin:
            return F_SIT
        if t < t_rest:
            return F_BLINK if any(b <= t < b + 0.14 for b in blinks) else F_CHIN
        return F_REST

    def j_x(t):
        if t < t_walk0:
            return XJ0
        if t < t_arr:
            return XJ0 + walk_k(t) * ADV
        return X_C

    # pose cuts are hidden by a squash-and-hop (as in the v1 scenes)
    hops = [(t_hmph, 0.45), (t_up, 1.0), (t_grab, 0.6), (t_on, 0.4), (t_arr, 0.6), (t_down, 0.45), (t_ham, 0.55),
            (t_lift, 0.8), (t_throw, 0.6), (t_tired, 0.7), (t_sit, 1.0), (t_chin, 0.7), (t_rest, 0.5)]

    def hop(t):
        sy, dy = 1.0, 0.0
        for ts, amp in hops:
            u = t - ts
            if -0.09 <= u <= 0.17:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.17, "sine")
                dy = -16 * amp * math.sin(math.pi * min(1.0, max(0.0, (u + 0.01) / 0.18)))
        return sy, dy

    def j_motion(t):
        walking = t_walk0 <= t < t_arr
        rot = 0.0
        if t < t_up:                               # s19's grumpy fidget and breathing, on s19's clock
            t19 = t + T19
            s = 1 + 0.011 * math.sin(2 * math.pi * t19 / 3.1)
            rot = 0.7 * math.sin(2 * math.pi * t19 / 2.7) + 0.3 * math.sin(2 * math.pi * t19 / 1.3)
            rot *= 1 - M.progress(t, t_up - 0.2, t_up - 0.09, "sine")
        else:
            s = 1 + (0.0 if walking else 0.011 * math.sin(2 * math.pi * t / 2.8))
        sy = s
        u = t - t_hmph                             # "hmph!": a little huff
        if 0 <= u < 0.42:
            sy *= 1 - 0.03 * math.sin(math.pi * u / 0.42)
        for kn in knocks:                          # the whole body jolts on each knock
            u = t - kn
            if 0 <= u < 0.16:
                sy *= 1 - 0.025 * math.sin(math.pi * u / 0.16)
        u = t - (t_sit + 0.55)                     # a big contented sigh in the cool shade
        if 0 <= u < 1.3:
            sy *= 1 + 0.022 * math.sin(math.pi * u / 1.3)
        if t_tired <= t < t_sit:                   # panting in the sun
            sy *= 1 + 0.012 * math.sin(2 * math.pi * t / 0.55)
        hsy, hdy = hop(t)
        sy *= hsy
        sx = s * (1 + 0.5 * (1 - hsy))
        return Tf(dx=j_x(t) - AX, dy=hdy, rot=rot, sx=sx, sy=sy, px=AX, py=GY)

    def seated(t):
        return t < t_up or t >= t_sit

    def shadow_motion(t):
        _, hdy = hop(t)
        se = seated(t)
        return Tf(dx=j_x(t) - AX - (22 if se else 0), sx=1.45 if se else 1.0, sy=1.0,
                  alpha=1 + hdy / 60.0, px=AX, py=GY)

    # =========================================================== THE BUNDLE (picked up, tossed down, used up)
    bfr = [doc(f'<g transform="translate({XBUN},{YBUN}) scale({SJ}) rotate(180)"><g filter="url(#wobble-fine)">'
               f'{bundle_local(k)}</g></g>') for k in range(4)]
    t_used = [knocks[1], t_frame_on, t_cloth0]

    def bun_frame(t):
        return float(sum(1 for tu in t_used if t >= tu))

    def _turn(ang):
        """Extra rotation from the lying drawing (rotate 180) to the drawing on his back (angle ang)."""
        return (ang % 360) - 180

    def bun_motion(t):
        if t < t_grab:                             # lying beside him at the start
            return Tf(dx=XBS - XBUN, dy=YBS - YBUN)
        if t < t_on:                               # swung up over his head onto his back
            u = M.progress(t, t_grab, t_on, "linear")
            bx, by, ang = BACK0
            x = XBS + (bx - XBS) * M.ease("sine")(u)
            y = YBS + (by - YBS) * u - 320 * math.sin(math.pi * u)
            return Tf(dx=x - XBUN, dy=y - YBUN, rot=_turn(ang) * M.ease("sine")(u), px=XBUN, py=YBUN)
        if t < t_toss:                             # on his back (part of his drawing)
            return Tf(alpha=0.0)
        if t < t_land:                             # shrugged off: it lands beside him
            u = (t - t_toss) / (t_land - t_toss)
            bx, by, ang = BACK
            dx0, dy0 = bx - XBUN, by - YBUN
            return Tf(dx=dx0 * (1 - u), dy=dy0 * (1 - u) - 70 * math.sin(math.pi * u) * (1 - 0.3 * u),
                      rot=_turn(ang) * (1 - M.ease("out")(u)), px=XBUN, py=YBUN)
        u = t - t_land
        sq = 0.0
        if u < 0.2:
            sq = 0.08 * math.sin(math.pi * u / 0.2)
        for tu in t_used:                          # a little hop each time something is taken from it
            v = t - tu
            if 0 <= v < 0.18:
                sq = -0.05 * math.sin(math.pi * v / 0.18)
        return Tf(sx=1 + sq * 0.6, sy=1 - sq, px=XBUN, py=YBUN + 14 * SJ)

    def bun_shadow(t):
        if t < t_grab:
            return Tf(dx=XBS - XBUN, alpha=1 - M.progress(t, t_grab - 0.04, t_grab + 0.04))
        return Tf(alpha=M.progress(t, t_land - 0.12, t_land, "sine"))

    sc.add("bundle_shadow", doc(C.ground_shadow(XBUN, GY + 26, 1.0, width=300, opacity=0.22)), motion=bun_shadow,
           wc=0)

    sc.add("jonah_shadow", doc(C.ground_shadow(AX, GY, SJ, width=150, opacity=0.26)), motion=shadow_motion, wc=0)
    sc.add("bundle", bfr, frame_at=bun_frame, motion=bun_motion, wc=0.6)
    sc.add("jonah", frames, frame_at=lambda t: float(j_frame(t)), motion=j_motion, wc=0.6)

    # shade on Jonah: a cool flat copy of his own silhouette, multiplied (only under the finished roof)
    shade_amt = lambda t: 0.24 * M.progress(t, t_cloth1, t_cloth1 + 0.4, "sine") + \
        0.16 * M.progress(t, t_sit, t_sit + 0.5, "sine")
    sc.add("jonah_shade", flat, frame_at=lambda t: float(tint_idx.get(j_frame(t), 0)), wc=0, blend="multiply",
           motion=M.combine(j_motion, lambda t: Tf(alpha=shade_amt(t) if j_frame(t) in tint_idx else 0.0)))

    # --- "hmph!": grumpy steam puffs rising above and behind his head (two little bursts, all before he walks)
    _, hp = jonah_fig(AX, GY, SJ, -1, POSE["sulk_hmph"], "hmph", label="hmph_pts")
    hx0, hy0 = hp["head"][0] - AX + XJ0, hp["head"][1]
    # (the later pair sits further back so it is clear of him when he stands up at t_up)
    for i_, (ox, oy, r_, ph) in enumerate([(58, -84, 30, 0.03), (124, -36, 21, 0.1),
                                           (156, -98, 24, 0.3), (100, -148, 18, 0.37)]):
        cx, cy = hx0 + ox, hy0 + oy

        def puff_motion(t, cx=cx, cy=cy, ph=ph):
            u = t - t_hmph - ph
            if 0 <= u < 0.5:
                a = min(1.0, u / 0.05) * (1 - M.progress(u, 0.26, 0.5, "sine"))
                s = 0.3 + 0.8 * M.ease("out")(u / 0.12) if u < 0.12 else 1.1 - 0.1 * M.progress(u, 0.12, 0.3)
                e = M.ease("out")(min(1.0, u / 0.5))
                return Tf(dx=20 * e, dy=-46 * e, sx=s, sy=s, alpha=a, px=cx, py=cy)
            return Tf(alpha=0.0)
        sc.add(f"puff{i_}", doc(_puff(cx, cy, r_)), motion=puff_motion, wc=0.3)

    # --- dust poofs: getting up, bundle landing, the toss, sitting down -------------------------------------
    for i, (t0, x, y, k) in enumerate([(t_up, XJ0, GY, 0.8), (t_land, XBUN, GY + 30, 1.2), (t_arr, X_C - 10, GY, 0.8),
                                       (t_sit, X_C - 30, GY, 1.2)]):
        dsvg = doc(_dust(x - 120 * k, y, k, 4, seed=10 + i) + _dust(x + 110 * k, y, k, 4, seed=20 + i))

        def dmo2(t, t0=t0, x=x, y=y):
            u = t - t0
            if not 0 <= u < 0.5:
                return Tf(alpha=0.0)
            s = 0.5 + 0.7 * M.ease("out")(u / 0.5)
            return Tf(dy=-6 * M.ease("out")(u / 0.5), sx=s, sy=s, alpha=0.9 * (1 - M.progress(u, 0.12, 0.5, "sine")),
                      px=x, py=y)
        sc.add(f"poof{i}", dsvg, motion=dmo2, wc=0.3)

    # =========================================================== LIZARD (basks, does push-ups)
    liz = [doc(V11._lizard(LIZ[0], LIZ[1], 0.82 * (1920 / 1960) * WF / 1920, legs=0))]

    def liz_motion(t):
        u = (t + 0.4) % 2.6
        b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
        return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)
    sc.add("lizard", liz, motion=liz_motion, wc=0.5)

    # =========================================================== DOVES: up from the bush, off toward the city
    dove_frames = [doc(PR.dove(DOVE0[0], DOVE0[1], 0.62, -1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    t_dove_end = T - 1.15
    for i, (t0, dx, dy, ph) in enumerate([(t_dove, 0, 0, 0), (t_dove + 0.22, 40, 22, 2)]):
        dur = t_dove_end - t0
        path = M.keys([(t0, {"dx": dx, "dy": dy}), (t0 + 0.35 * dur, {"dx": dx - 190, "dy": dy - 180, "s": 0.9}),
                       (t0 + dur, {"dx": dx - 430 - 30 * i, "dy": dy - 320 + 20 * i, "s": 0.55})],
                      ["out", "linear"], pivot=DOVE0)
        sc.add(f"dove{i}", dove_frames, frame_at=flap(12, ph), wc=0.4, z=z_doves + 0.01 * i, motion=M.combine(
            path, M.bob(6, 0.6, ph * 0.1),
            lambda t, t0=t0, dur=dur: Tf(alpha=M.progress(t, t0, t0 + 0.12) *
                                         (1 - M.progress(t, t0 + dur - 0.5, t0 + dur)))))

    # =========================================================== FOREGROUND (rocks; swaying dry grass)
    fg = ""
    fg += V11._rock(170, 1290, 330, 140, seed=31) + V11._rock(430, 1305, 170, 74, seed=32)
    fg += V11._rock(2960, 1290, 300, 130, seed=33) + V11._rock(2740, 1310, 150, 64, seed=34)
    fg += V11._rock(1210, 1300, 180, 70, seed=35)
    fg += PR.bush(40, 1180, 1.0, variant=2) + PR.bush(3080, 1170, 1.0, variant=2)
    sc.add("fg_rocks", doc(S.g(fg, filter="wobble")), wc=0.9)

    def grass_fn(ph):
        return lambda t: 1.5 + 1.4 * math.sin(2 * math.pi * (t / 2.6 + ph))

    for gi, tufts in enumerate([[(300, 1215, 1.1, 1), (560, 1250, 0.9, 1), (90, 1255, 1.0, 1)],
                                [(2620, 1215, 1.0, 1), (2850, 1200, 0.9, 1), (3040, 1250, 1.0, 1)],
                                [(1950, 1080, 0.7, 1), (2420, 1075, 0.7, 1), (1000, 1060, 0.65, 1)],
                                [(1720, 1210, 0.9, 1), (2150, 1190, 0.8, 1), (820, 1180, 0.85, 1)]]):
        gframes = [doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts))
                   for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", gframes, frame_at=grass_fn(gi * 0.23), wc=0.7)

    # =========================================================== FX
    import cv2
    import numpy as np

    rng = np.random.default_rng(13)
    NM = 30                                   # drifting warm dust motes (as FX.motes)
    m_x, m_y = rng.uniform(100, 3000, NM), rng.uniform(150, 1100, NM)
    m_vx, m_vy = rng.uniform(-12, 12, NM), rng.uniform(-14, 6, NM)
    m_r, m_ph = rng.uniform(3, 7, NM), rng.uniform(0, 6.28, NM)
    HEAT = [(1450, 960), (2250, 950), (2750, 960), (1000, 980), (600, 960), (2500, 1110), (1900, 1120)]

    def atmos(frame, t, view):
        """Dust motes and heat shimmer rising off the hot ground, drawn on one overlay. Motes fade out around
        Jonah so they never smudge his face or hands."""
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        sc_ = view.scale
        jx = j_x(t)
        bx0, bx1, by0, by1 = jx - 175, jx + 175, GY - 480, GY + 30
        for i in range(NM):
            xx = 100 + (m_x[i] - 100 + m_vx[i] * t + 8 * math.sin(t * 0.7 + m_ph[i])) % 2900
            yy = 150 + (m_y[i] - 150 + m_vy[i] * t) % 950
            out_d = max(bx0 - xx, xx - bx1, by0 - yy, yy - by1)
            k = min(1.0, out_d / 40.0)
            if k <= 0:
                continue
            ox, oy = view.to_out(xx, yy)
            r = m_r[i] * sc_
            a = int(100 * k * (0.6 + 0.4 * math.sin(t * 1.3 + m_ph[i])))
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(255, 246, 214, a))
        for i, (bx, by) in enumerate(HEAT):
            u = (t * 0.55 + i * 0.37) % 1.0
            ox, oy = view.to_out(bx, by - 80 * u)
            if not (-60 < ox < frame.size[0] + 60):
                continue
            a = int(95 * math.sin(math.pi * u))
            for j in range(3):
                x0 = ox + (j - 1) * 22 * sc_
                pts = [(x0 + 7 * sc_ * math.sin(q * 1.1 + t * 7 + i), oy - q * 9 * sc_) for q in range(9)]
                d.line(pts, fill=(255, 248, 226, a), width=max(2, int(4 * sc_)), joint="curve")
        frame.alpha_composite(ov)
        return frame

    # warm heat vignette (constant; as FX.vignette(0.16) but precomputed)
    _vg = {}

    def vignette(frame, t, view):
        if "k" not in _vg:
            Hh, Ww = frame.size[1], frame.size[0]
            yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
            rr = np.sqrt(((xx - Ww / 2) / (Ww / 2)) ** 2 + ((yy - Hh / 2) / (Hh / 2)) ** 2)
            a = np.clip(np.clip((rr - 0.35) / 0.95, 0, 1) ** 1.6 * 0.16, 0, 1)
            _vg["k"] = cv2.merge([np.round((1 - a) * 255).astype(np.uint8)] * 3)
            _vg["c"] = cv2.merge([np.round(a * c).astype(np.uint8) for c in (150, 82, 30)])
        arr = np.array(frame)
        arr[..., :3] = cv2.add(cv2.multiply(arr[..., :3], _vg["k"], scale=1 / 255.0), _vg["c"])
        return Image.fromarray(arr, "RGBA")

    sx0, sy0 = m19(1620, 380)
    sx1, sy1 = m19(2420, 1150)
    sc.fx = [
        # s19's sparkles in God's light (already at full strength at t = 0), fading with the light
        FX.sparkles((sx0, sy0, sx1, sy1), count=26, t0=-1.0, t1=t_fade + 1.1, color=(255, 238, 170), size=(8, 20),
                    seed=5),
        atmos,
        vignette,
    ]

    # =========================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("heat", 0, dur=T, gain_db=-19, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_up - 0.05, gain_db=-15, pan=-0.2)
    sc.sfx("whoosh", t_grab - 0.02, gain_db=-17, pan=-0.2)
    sc.sfx("thud", t_on - 0.02, gain_db=-15, pan=-0.2)
    for tc in contacts:                          # one footstep on every footfall of the walk cycle
        sc.sfx("footsteps", round(tc - STEP_LEAD, 3), dur=STEP_DUR, rate=0.5, gain_db=-10, fade_in=0.01,
               fade_out=0.08, pan=-0.1)
    sc.sfx("cloth", t_toss, gain_db=-14, pan=-0.1)
    sc.sfx("thud", t_land - 0.02, gain_db=-8, pan=-0.1)
    sc.sfx("hammer", hammer_at, gain_db=-6, pan=0.15)
    sc.sfx("thud", t_frame_on - 0.02, gain_db=-11, pan=0.05)
    sc.sfx("cloth", t_cloth0 - 0.03, gain_db=-6)
    sc.sfx("pop", t_branch, gain_db=-14)
    sc.sfx("thud", t_sit + 0.02, gain_db=-13)
    sc.sfx("birds", t_dove - 0.1, dur=min(3.2, T - t_dove), gain_db=-17, fade_in=0.3, fade_out=0.9, pan=-0.3)
    return sc
