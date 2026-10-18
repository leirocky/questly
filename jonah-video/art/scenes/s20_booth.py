"""Scene 20 — the booth (Jonah 4:5).

One wide 3100 x 1300 stage on a hot afternoon: the dry plain east of Nineveh, the city small and hazy on the
western horizon (s21's far skyline, same drawing and place), a road from it across the plain onto a dry ochre
ridge that rises into a low knoll, where Jonah builds his booth (the same props.booth drawing as s21 / v1 s11,
split into its building stages). A blazing sun (s21's flame sun) hangs over the city.

The scene OPENS ON S19'S WORLD: an opening plate draws s19's own sky, clouds, city (wall, gate, corner tower,
skyline), green plain and rocky knoll through the matched opening view (m19), with s19's townspeople still in
their sackcloth on the wall walk and in front of the gate, cheering on s19's clock (no festival decorations),
the golden cloud gap and God's light (s19's own light drawings). So the s19 -> s20 dissolve changes nothing but
time. After it the townspeople go home (down from the wall walk, off to the left), and as Jonah walks out east
("他出了城") a soft-edged wipe sweeps s19's world away from right to left while the camera follows him: the hot
desert is behind it, and the far city and the sun come out once it has passed them (nothing is cross-faded
as a whole, so the two cities never show at once).

Line 0 "约拿没有回答。" — opens exactly where s19 ends: Jonah sits on the ground, arms crossed, scowling at the
        city, his back to the soft golden light of God's question (light only, never a figure, from the
        upper right as in s19), his bundle of sticks and rolled cloth lying beside him. The light fades as
        he answers nothing (the gold leaves the clouds, which drift a little closer together): a grumpy
        "hmph" (eyes shut, chin up, steam puffs above and behind his head).
        He hops up, then swings the bundle up over his head onto his back.
        "他出了城，坐在城的东边，" — he trudges east along the ridge (a planted-foot walk cycle: the drawing
        follows the distance walked; a footstep sound on every footfall), the camera following, and the wipe
        sweeps s19's green fields and big near city away to the dry plain, with the city far behind on the
        horizon; the little lizard (on s19's big stone beside the bundle) scurries out of his way, hops down
        and runs over to its own stone further east. He plants both feet on the knoll and, with a shrug of the shoulder,
        tosses the bundle down beside him (thud).
        "为自己搭了一座小棚子。" — with a stone he knocks the front post in; the other three posts (a stick
        leaving the bundle for each) drop into their holes on the next knocks of the 'hammer' sound (the cue
        time is chosen so the sound has 4 knocks and the knock onsets are read from it) as he leans toward each;
        he raises his arms and the frame goes up piece by piece — tie bar, front-left rafter,
        front-right rafter, then the ridge with the back rafters — each dropping into place (a soft knock) as
        the sticks leave the bundle; he throws the striped cloth over the ridge (it unrolls downward and
        settles); leafy branches pop on top. The bundle on the ground shrinks as he uses it. He stands under
        the roof, hot and panting.
Line 1 "他坐在棚子下面的阴凉里，" — he sits down in the booth's thin shade (hop + dust), a cool tint settles on him,
        eyes closed with relief and a big sigh; the camera pushes in a little.
        "要看看这座城到底会怎么样。" — chin on fist, a sulky eye on the city; two doves flutter up from a bush
        and fly off toward the city as the camera pulls back to reveal the city he is watching. He drops his
        hands to his knees (plain seated pose, facing the city) and the scene settles on s21's opening framing.

Continuity (1.0 s cross-dissolves)
* Start = s19's last frame: s19 ends with Jonah (sit_sulk, facing left) anchored at output (1060, 926) at
  1.2 * 1920/2066 scale, God's light coming down from its cloud gap at output (1414, 66). The opening camera
  is computed so that Jonah's anchor and size match; s19's background, people, lizard and light are drawn
  through the same transform (m19 / at19, from s19_angry's own drawing functions), and his grumpy fidget /
  breathing, the people's hops, the clouds, the lizard's push-ups and the light's shimmer run on s19's clock
  (read from the timeline) so the two scenes coincide. Nothing of s20's own world (sun, desert, foreground
  rocks and grass, heat shimmer, vignette) shows before the wipe (t_w0 .. t_w1) has passed it.
* End = s21's first frame: s21 opens with its booth anchor at output (1064, 895), booth scale 1.3 * 1920/1960,
  Jonah sitting ('sit', facing left) 28 px right of it, its lizard on its stone, its afternoon flame sun at
  output (230, 246) and its far city nineveh_skyline(20, 560, 644, 0.42, seed 2) on the horizon at the left.
  The final camera puts this booth on exactly that spot at the same size, the sun (same drawing, scale,
  turning and breathing phase) on s21's, the far city through KF / TXF / TYF on s21's, and Jonah ends in the
  plain 'sit' pose at the same place.

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
* Sky, sun, clouds, far dunes and the far city have a little parallax against the camera (zero at the final
  view). The opening plate has none (s19's background is static on its stage); its right edge is feathered
  (mask m19) where s19's stage ends, which never comes into view: the camera holds until the wipe has swept
  past it.
* The wipe is a reveal mask on each plate layer (and its complement on this scene's foreground). Reveal edges
  are in the layer's cropped pixels, so those layers carry span() dots that make the crop the full stage width.
  Layer seeds (watercolour texture) come from the layer index: add new layers at the end (as the crowd's extra
  shadows are) so the first and last frames keep their texture.
* The plate reuses s19_angry's functions and constants (far_svg, wall_svg, plain_svg, knoll_svg, sky_svg,
  bank_svg, heaven_glow_svg, light_pool_svg, rays_svg, warm_svg, WALK_PEOPLE, CROWD, thin_hops, knoll_y), so
  it follows s19's drawings; the few motion clocks copied from s19's build (people's hop schedules, clouds,
  cloud banks, light shimmer, lizard) are marked "as s19" and must change with it.
"""
import math
import random
import re
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


# the bundle as he uses it up: (sticks kept, sticks packed closer, ropes); state 5 = the leftovers
BUNDLE_STATES = [
    ((0, 1, 2, 3, 4), False, 2),     # 0 full
    ((0, 1, 3, 4), False, 2),        # 1-3 one stick fewer for each post that goes in after the first
    ((1, 3, 4), False, 2),
    ((3, 4), False, 2),
    ((4,), True, 1),                 # 4 the frame is up: one stick and the cloth roll
    ((1, 4), False, 0),              # 5 the cloth is up: two short leftover sticks
]


def bundle_local(state=0):
    """The bundle (scale 1, centred on (0, 0)): booth sticks tied with rope plus the striped cloth rolled up and
    seen end-on. Axis along x; the 'base' end is +x, local +y is the side away from the carrier's back.
    State (BUNDLE_STATES): 0 full, 1-3 a stick fewer per post, 4 one stick + the cloth roll (frame used),
    5 leftovers (cloth used)."""
    rnd = random.Random(5)
    cols = [P["wood"], P["wood_dark"], P["wood_light"], P["wood"], S.shade(P["wood"], -0.12)]
    offs = [(-15, 0), (7, 1), (-5, 2), (15, 3), (2, 4)]
    keep, packed, ropes = BUNDLE_STATES[state]
    leftovers = state == len(BUNDLE_STATES) - 1
    out = ""
    for i, (o, ci) in enumerate(offs):
        e0, e1, j = rnd.uniform(-0.05, 0.04), rnd.uniform(-0.06, 0.06), rnd.uniform(-2.5, 2.5)
        if i not in keep:
            continue
        if leftovers:           # leftovers: two short sticks lying across each other
            a_ = math.radians(-9 if i == 1 else 7)
            k, cx_ = (0.5, -40) if i == 1 else (0.7, 20)
            ca, sa = math.cos(a_), math.sin(a_)
            out += _tube([(cx_ - 130 * k * ca, 4 - 130 * k * sa), (cx_ + 130 * k * ca, 4 + 130 * k * sa)], 8.5,
                         cols[ci], 3)
            continue
        oy = o * 0.4 + 2 if packed else o
        out += _tube([(-130 * (1 + e1), oy), (0, oy + j), (130 * (1 + e0), oy)], 8.5, cols[ci], 3)
    if not leftovers:   # the striped cloth, rolled up lengthwise and tied on with the sticks
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
    if ropes == 2:
        for bx in (73, -47):
            out += _tube([(bx + 2, -23), (bx - 2, 50)], 6, ROPE, 3)
    elif ropes == 1:
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
    # in-between from the throw (arms up) to standing tired (arms down): arms forward, coming down
    "throw_down": C._P(t=-5, h=-6, arms=(("fk", 90, 100), ("fk", 80, 92)), hands=("open", "open")),
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
    Keys in back-to-front order: post_bl, post_br, under, post_fl, post_fr, tiebar, cloth, frame, lash, branches.
    'frame' (ridge + rafters) is also split into the pieces Jonah puts up one by one: frame_back (the ridge and
    the two back rafters), rafter_fl, rafter_fr (frame = frame_back + rafter_fl + rafter_fr)."""
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
    parts["frame_back"] = fr
    parts["rafter_fl"] = _stick([(-176, -228), (-80, -300), (30, -400)], 10, wd, 3.5)
    parts["rafter_fr"] = _stick([(174, -232), (84, -298), (-26, -394)], 10, wd, 3.5)
    parts["frame"] = fr + parts["rafter_fl"] + parts["rafter_fr"]
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
# s21's stage (2112 x 1188) -> this stage, through the matched final view (s21's opening Cam(1075, 600, 1960))
KF = WF / 1960
TXF = CAM_END.x - WF / 2 - (1075 - 1960 / 2) * KF
TYF = CAM_END.y - WF * 9 / 32 - (600 - 1960 * 9 / 32) * KF
# s19's stage -> this stage, through the matched opening view (anchored on Jonah): p20 = (TX19, TY19) + R19 * p19
R19 = SJ / 1.2
TX19, TY19 = XJ0 - S19_JX * R19, GY - S19_JY * R19
# the plate's feathered right edge: just outside the opening view, and fully faded before s19's far ridges and
# plain end (their outlines close at s19 x 2860, here about x 2288)
X19_FADE = (CAM_START.x + CAM_START.w / 2 + 6, CAM_START.x + CAM_START.w / 2 + 64)
WIPE_SOFT = 420                   # width (stage px) of the soft edge that sweeps s19's world away, right to left
WIPE_DUR = 1.6                    # ...from just outside the right of the view to just outside its left
LIZ_S = 0.82 * (1920 / 1960) * WF / 1920                  # the lizard's scale here (s21's at its opening view)

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
    return (TX19 + x * R19, TY19 + y * R19)


def at19(markup):
    """Markup drawn in s19's stage coordinates, placed on this stage through the matched opening view."""
    return f'<g transform="translate({TX19:.3f},{TY19:.3f}) scale({R19:.6f})">{markup}</g>'


def _svg_inner(d):
    """The content of a full s19 <svg> document (its own <defs> included), without the outer element."""
    return d[d.index(">") + 1: d.rindex("</svg>")]


# feathered right edge of the opening plate (s19's stage ends at about x 2310 here; never in view, see the wipe)
M19_DEFS = (f'<linearGradient id="m19g" gradientUnits="userSpaceOnUse" x1="{X19_FADE[0]:.0f}" y1="0" '
            f'x2="{X19_FADE[1]:.0f}" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>'
            f'</linearGradient><mask id="m19" maskUnits="userSpaceOnUse" x="-1500" y="-800" width="{SW + 3000}" '
            f'height="{SH + 1600}"><rect x="-1500" y="-800" width="{SW + 3000}" height="{SH + 1600}" '
            f'fill="url(#m19g)"/></mask>')


def span(y):
    """Two faint 2 px dots at the far left and right edges of the stage (never in view: the camera stays within
    x 40 .. 2430). They make the compositor crop the layer to the full stage width, so a reveal's edge at
    w * frac is the stage x SW * frac (the wipe below needs stage coordinates)."""
    return "".join(f'<rect x="{x}" y="{y:.0f}" width="2" height="2" fill="#000" fill-opacity="0.05"/>'
                   for x in (0, SW - 2))


def doc19(*docs, feather=True, span_y=None):
    """One layer document holding s19 drawings (full s19 documents) mapped onto this stage (full stage width
    with ``span_y``)."""
    body = "".join(at19(_svg_inner(d)) for d in docs)
    sp = span(span_y) if span_y is not None else ""
    if feather:
        return doc(f'<g mask="url(#m19)">{body}</g>{sp}', M19_DEFS)
    return doc(body + sp)


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


def _prev_scene(ctx):
    """The previous scene (s19): its clock at this scene's t = 0 (its last cross-dissolve second), its duration
    and its narration-keyed times this scene replays (crowd 'quiet' window, God's light), so the opening runs in
    step with s19's last frames. Falls back to the values of the current script if the timeline can't be read."""
    try:
        from engine.loader import load_timeline
        from engine.scene import SceneContext
        tl = load_timeline()
        ids = [s["id"] for s in tl["scenes"]]
        prev = tl["scenes"][ids.index(ctx.id) - 1]
        c19 = SceneContext.from_timeline(prev)
        L = c19.lines
        return dict(T19=float(ctx.start - prev["start"]), D19=float(c19.duration),
                    quiet=(L[1].start - 0.3, L[2].end + 0.4), t_light=L[4].start - 0.1)
    except Exception:
        return dict(T19=42.733, D19=43.733, quiet=(7.9, 26.097), t_light=36.767)


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


# ================================================================== build
def build(ctx):
    from PIL import Image, ImageDraw

    from art.scenes import s19_angry as S19
    from art.scenes_v1 import s11_vine as V11
    from art.scenes_v1 import s12_lesson as V12

    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]
    prev = _prev_scene(ctx)
    T19 = prev["T19"]                          # s19's clock at t = 0
    D19, quiet19, t_light19 = prev["D19"], prev["quiet"], prev["t_light"]

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
    t_lift = knocks[-1] + 0.16                    # ...arms up: the frame goes up piece by piece...
    PIECES = (("tiebar", 0.0), ("rafter_fl", 0.11), ("rafter_fr", 0.22), ("frame_back", 0.33))
    PIECE_DROP = 0.17                             # each piece comes down this long, then settles
    t_frame_on = t_lift + 0.50                    # ...the last one (ridge + back rafters) lands on the posts
    t_throw = t_lift + 0.76                       # ...the cloth thrown over the ridge
    t_cloth0, t_cloth1 = t_throw + 0.05, t_throw + 0.42
    t_branch = t_throw + 0.55
    t_tired = t_throw + 0.62                      # phew, hot! (sweat)
    t_sit = L1.start + 0.12                       # "他坐在棚子下面的阴凉里"
    t_chin = L1.at("要看看") + 0.22               # chin on fist, eyes on the city
    t_dove = t_chin + 0.1                         # doves fly off toward the city
    t_rest = min(L1.end + 0.05, T - 1.35)         # hands back on the knees: s21's opening pose
    blinks = [t_chin + 1.0, t_chin + 2.0]
    a_fade = lambda t: 1 - M.progress(t, t_fade, t_fade + 1.1, "sine")    # God's light fades: no answer
    # s19's world (the opening plate) is swept away right to left (the wipe, below) as he walks out east
    t_w0 = t_walk0 - 0.1
    t_w1 = t_w0 + WIPE_DUR
    t_liz0 = t_walk0                              # the lizard scurries out of his way (off s19's stone first)...
    LIZ_RUN = 0.82                                # ...hop down, run, hop up onto its own stone

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
    c_hold = Cam(c0.x + 3, c0.y, c0.w - 4)
    cam = M.cam_keys([
        (0.0, c0),
        (1.0, c0),                                          # still through the dissolve from s19...
        (t_up - 0.05, c_hold),                              # ...and nearly so through the hmph...
        (t_walk0, c_hold),                                  # ...until he walks (the plate's cut-off out of view)
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

    # ------------------------------------------------------------ the wipe: s19's world -> the desert
    # A soft vertical edge (WIPE_SOFT wide) sweeps s19's world away from right to left while he walks out east:
    # it comes in from just outside the right of the view (so the plate's own cut-off at X19_FADE never shows:
    # the camera holds until he walks) and leaves just outside the left, so each spot changes in ~0.3 s. Nothing
    # is cross-faded as a whole: s19's townspeople have gone (down from the wall walk, off to the left) before it
    # reaches them, and the sun and the far city come out only once it has passed where they are.
    def view_x(t, side):
        c = cam(t)
        return c.x + side * c.w / 2
    W_E0 = view_x(t_w0, 1) + WIPE_SOFT / 2 + 4
    W_E1 = view_x(t_w1, -1) - WIPE_SOFT / 2 - 4

    def wipe_e(t):
        """Stage x of the middle of the wipe's soft edge (s19's world is left of it, the desert right of it)."""
        return W_E0 + (W_E1 - W_E0) * M.progress(t, t_w0, t_w1, "linear")

    e_lin = lambda t: W_E0 + (W_E1 - W_E0) * (t - t_w0) / WIPE_DUR      # (the same, carried on past t_w1)

    def plate_at(x, t):
        """How much of s19's world is still there at stage x."""
        if t <= t_w0:
            return 1.0
        if t >= t_w1:
            return 0.0
        return min(1.0, max(0.0, (wipe_e(t) - x) / WIPE_SOFT + 0.5))

    def wipe_gone(x):
        """First time the wipe has fully passed stage x (or x(t), a function of time)."""
        xf = x if callable(x) else (lambda t: x)
        n = int(WIPE_DUR * 120)
        for i in range(n + 1):
            t = t_w0 + WIPE_DUR * i / n
            if wipe_e(t) + WIPE_SOFT / 2 <= xf(t):
                return t
        return t_w1

    plate_on = lambda t: 1.0 if t < t_w1 else 0.0

    def wipe_out(dx=None):
        """reveal for a plate layer drawn with span(): hide it right of the wipe (``dx``: the layer's own shift)."""
        def rv(t):
            if t <= t_w0 or t >= t_w1:
                return {"mode": "left", "frac": 1.0}
            e = wipe_e(t) - (dx(t) if dx else 0.0)
            return {"mode": "left", "frac": min(0.9999, e / SW), "soft": WIPE_SOFT}
        return rv

    def wipe_in(t):
        """reveal for a layer of this scene's own world drawn above the plate (with span()): the complement."""
        if t <= t_w0 or t >= t_w1:
            return {"mode": "right", "frac": 1.0}
        return {"mode": "right", "frac": min(0.9999, max(0.0, 1 - wipe_e(t) / SW)), "soft": WIPE_SOFT}

    world = lambda t: Tf(alpha=1.0 if t > t_w0 else 0.0)   # (with wipe_in)

    def wipe_trail(dx):
        """reveal for this scene's clouds (under the plate, drawn with span()): they come in only where s19's world
        has fully gone, on a soft edge of their own just behind the wipe's (so a cloud of s19 and one of this
        scene never show at the same spot)."""
        def rv(t):
            e = e_lin(t) + WIPE_SOFT - dx(t)
            if t <= t_w0 or e + WIPE_SOFT / 2 < view_x(t, -1) - dx(t) - 20:
                return {"mode": "right", "frac": 1.0}
            return {"mode": "right", "frac": min(0.9999, max(0.0, 1 - e / SW)), "soft": WIPE_SOFT}
        return rv

    # =========================================================== SKY
    sky = doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="820" fill="url(#g)"/>',
              S.lin_grad("g", [(0, "#8cc4d9"), (0.4, "#bfdfdc"), (0.72, "#f0deb4"), (1, "#f6d49d")]))
    sc.add("sky", sky, wc=0.5)
    # the sun: s21's flame sun, turning and breathing on s21's clock so the end dissolve matches. It is not there
    # in the s19 dissolve: it comes out (rays unfurling) in the clear desert sky once the wipe has swept s19's
    # world (towers and all) away from where it is; full long before the s21 dissolve.
    tz = T - 1.0                                   # s21's t = 0
    at_sun = lambda t: Tf(dx=SUN[0] - CX, dy=SUN[1] - CY)
    t_sun0 = wipe_gone(lambda t: SUN[0] + 0.6 * (cam(t).x - CAM_REF[0]) - 400 * SUN_S - 20)   # its left tips
    a_sun = lambda t: M.progress(t, t_sun0, t_sun0 + 0.6, "sine")
    g_sun = lambda t: 0.7 + 0.3 * M.progress(t, t_sun0, t_sun0 + 1.0, "out")
    sc.add("sun_rays", flame_rays_svg(), wc=0.3, motion=par(0.6, M.combine(
        at_sun, lambda t: Tf(rot=7 * (t - tz), px=CX, py=CY), M.breathe(0.03, 1.1, pivot=(CX, CY), phase=-tz / 1.1),
        lambda t: Tf(sx=SUN_S * g_sun(t), sy=SUN_S * g_sun(t), px=CX, py=CY, alpha=a_sun(t)))))
    sc.add("sun_disc", hot_disc_svg(), wc=0.4, motion=par(0.6, M.combine(
        at_sun, M.breathe(0.03, 1.4, pivot=(CX, CY), phase=-tz / 1.4),
        lambda t: Tf(sx=SUN_S, sy=SUN_S, px=CX, py=CY, alpha=a_sun(t)))))
    clouds = doc(S.g(S.cloud(260, 150, 230, 70, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(1330, 170, 210, 64, "#fdf1e2", seed=6, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2240, 250, 260, 80, "#fdf3e4", seed=8, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2930, 200, 220, 66, "#fdf1e2", seed=9, sw=3, shade_fill="#f0d6c4"), filter="wobble") +
                 span(200))
    m_clouds = par(0.5, M.drift(vx=-6))
    sc.add("clouds", clouds, wc=0.7, motion=m_clouds, reveal=wipe_trail(lambda t: m_clouds(t).dx))

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
    # Nineveh, small and hazy on the western horizon: s21's far city (same drawing, s21's HORIZON + 4), mapped
    # from s21's opening view so it is exactly s21's at the end; it moves with the far dunes. It comes out of the
    # haze only once the wipe has passed it (never seen through s19's big city)
    t_city0 = wipe_gone(lambda t: TXF + 10 * KF + 0.25 * (cam(t).x - CAM_REF[0]))
    sc.add("city_far", doc(PR._place(PR.nineveh_skyline(20, 560, 644, scale=0.42, seed=2, haze=0.42,
                                                        tint="#efdcbc"), TXF, TYF, KF, filt=None)),
           wc=0.6, motion=par(0.25, lambda t: Tf(alpha=M.progress(t, t_city0, t_city0 + 0.5, "sine"))))

    # =========================================================== PLAIN (static, flattened)
    pl = (f'<rect x="-40" y="722" width="{SW + 80}" height="{SH - 700}" fill="url(#pl)"/>'
          f'<path d="M-40,722 L{SW + 40},722" stroke="{INK}" stroke-width="3" opacity="0.45"/>')
    rnd = random.Random(7)
    for i in range(40):        # far shrubs dotting the dry plain east of the city
        x = rnd.uniform(1150, SW)
        y = rnd.uniform(734, 900)
        k = 0.6 + (y - 730) / 260
        pl += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{9 * k:.1f}" ry="{4.5 * k:.1f}" fill="#b7a274" opacity="0.6"/>'
    rnd = random.Random(17)
    for i in range(16):        # ...and the plain between the city and the ridge
        x = rnd.uniform(-40, 1150)
        y = rnd.uniform(740, 900)
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
    # the road from the far city across the plain to the ridge (s21's road, mapped like the city); on the ridge
    # it becomes Jonah's footpath east
    road = S.smooth_path([(470, 724), (520, 760), (470, 812), (600, 880), (720, 960), (640, 960), (520, 885),
                          (410, 812), (468, 760), (440, 726)])
    pl += PR._place(f'<path d="{road}" fill="#f5e2b6" opacity="0.85"/>', TXF, TYF, KF, filt=None)
    # a distant oasis to the east
    for (x, y, s_, ln) in [(2620, 742, 0.16, 0.1), (2668, 746, 0.13, -0.1), (2715, 744, 0.15, 0.05)]:
        pl += PR.palm_tree(x, y, s_, lean=ln)
    pl += PR.bush(2560, 750, 0.22, variant=0) + PR.bush(2760, 752, 0.2, variant=0)
    plain_defs = S.lin_grad("pl", [(0, "#efdcb2"), (0.3, "#ead1a0"), (1, "#dcb57c")])
    sc.add("plain", doc(S.g(pl, filter="wobble"), plain_defs), wc=0.8)

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

    # =========================================================== THE OPENING PLATE: s19's world
    # s19's own sky, clouds, cloud gap, city, people, green plain and knoll, drawn through the matched opening view
    # above this scene's sky and land (which it hides), so the s19 dissolve changes nothing but time. Everything
    # moving in it runs on s19's clock (t + T19). Once the dissolve is over the townspeople leave (the ones on the
    # wall walk go down behind the parapet, the crowd in front of the gate walks off to the left); then, as Jonah
    # walks out east, the wipe sweeps the rest away right to left: the hot desert behind it, the far city and the
    # sun coming out once it has passed them. (The layers it sweeps are drawn full stage width, see span().)
    def mot19(fn19, alpha=plate_on):
        """A motion of s19's stage on s19's clock, mapped onto this stage, times ``alpha(t)``."""
        def m(t):
            v = fn19(t + T19) if fn19 else Tf()
            px, py = m19(v.px, v.py) if v.px is not None else (None, None)
            return Tf(dx=v.dx * R19, dy=v.dy * R19, rot=v.rot, sx=v.sx, sy=v.sy, alpha=v.alpha * alpha(t),
                      px=px, py=py)
        return m

    def on19(f):
        return lambda t: f(t + T19)

    def add19(name, svgs, motion, **kw):
        """A plate layer the wipe sweeps away (its documents drawn with span())."""
        sc.add(name, svgs, motion=motion, reveal=wipe_out(lambda t: motion(t).dx), **kw)

    def in_s19(hops):
        """s19's hop schedule, ending with s19: hops already under way at its last frame finish, no new ones."""
        return [h for h in hops if h[0] < D19]

    sky19 = re.sub(r'<rect x="[-\d.]+" y="([-\d.]+)" width="[\d.]+" height="([\d.]+)" fill="url\(#sky\)"/>',
                   lambda mm: f'<rect x="-1600" y="{mm.group(1)}" width="6000" height="{mm.group(2)}" '
                              f'fill="url(#sky)"/>', S19.sky_svg(), count=1)   # widened (its gradient is vertical)
    add19("p19_sky", doc19(sky19, feather=False, span_y=4), mot19(None), wc=0.45)
    for i, (cx_, cy_, w_, h_, sd, v) in enumerate([(640, 150, 300, 90, 3, 6), (1210, 300, 220, 70, 5, 4.5),
                                                   (60, 420, 200, 62, 9, 5), (1620, 450, 170, 54, 8, 3.5)]):
        add19(f"p19_cloud{i}", doc19(S19.cloud_svg(cx_, cy_, w_, h_, sd), feather=False, span_y=m19(cx_, cy_)[1]),
              mot19(M.combine(M.drift(vx=v), M.bob(3, 7 + i, i * 0.3))), wc=0.7)    # as s19
    # God's question still hangs in the air at the start: the heavenly glow in the parted cloud gap (as s19),
    # fading as he answers nothing (gone before the wipe); the gold leaves the cloud banks and they drift a little
    # closer together
    glow19 = lambda t19: (M.progress(t19, t_light19, t_light19 + 0.9, "sine") *
                          (0.86 + 0.14 * math.sin(2 * math.pi * (t19 - t_light19) / 2.3)))
    sc.add("p19_heaven_glow", doc19(S19.heaven_glow_svg(), feather=False), wc=0,
           motion=mot19(lambda t19: Tf(alpha=glow19(t19)), a_fade))
    gap_y = m19(*S19.GAP)[1]
    for name, rel, d0, d1 in [("bankL", S19.LEFT_BANK, 70, -170), ("bankR", S19.RIGHT_BANK, -66, 150)]:   # as s19
        frames = [doc19(S19.bank_svg(rel, g_, name), feather=False, span_y=gap_y) for g_ in (0.0, 1.0)]
        close = lambda t, d0=d0, d1=d1: Tf(dx=R19 * (d1 + (d0 - d1) * 0.3 * M.progress(t, t_fade, t_w1, "inout")))
        add19(f"p19_{name}", frames, M.combine(close, mot19(M.bob(4, 6.0, 0.3 if d1 > 0 else 0.0))), wc=0.7,
              frame_at=a_fade)
    add19("p19_far", doc19(S19.far_svg(), span_y=m19(0, S19.HZ)[1]), mot19(None), wc=0.7)
    # s19's townspeople on the wall walk: still in their sackcloth, cheering now and then (as s19); after the
    # dissolve they go down from the wall walk one after another (sinking behind the parapet, then gone)
    WALL_DOWN = [1.2, 1.2, 2.0, 1.85, 1.7, 1.4, 1.55, 1.3]        # when each starts down (s19 ends at t = 1)
    for i, (x, fy, kind, var, fc) in enumerate(S19.WALK_PEOPLE):
        frames = [doc(at19(C.citizen(x, fy, 0.42, fc, kind=kind, variant=var, pose=p, attire="sackcloth",
                                     expr="happy" if p == "stand" else None))) for p in ("stand", "cheer")]
        hops = in_s19(S19.thin_hops(V12.hop_sched(70 + i, D19, n=(1, 2), dur=(0.5, 0.8), rest=(1.0, 2.6)),
                                    *quiet19, 5.0))
        td = WALL_DOWN[i]
        sc.add(f"p19_walk{i}", frames, frame_at=on19(V12.hop_frame(hops, 0.12, 0.25)), wc=0.5,
               motion=M.combine(mot19(V12.hop_motion(x, fy, hops, 9), lambda t, td=td: float(t < td + 0.56)),
                                lambda t, td=td: Tf(dy=280 * M.progress(t, td, td + 0.55, "sine"))))
    add19("p19_ground", doc19(S19.wall_svg(), S19.plain_svg(), span_y=m19(0, S19.WY)[1]), mot19(None), wc=0.8)
    # the cheering crowd in front of the gate, in sackcloth with happy faces (as s19); after the dissolve they
    # turn and walk off to the left, out of the picture (and their layers end) before the wipe gets there
    CROWD_GO = [(1.15, 150), (1.45, 170), (1.25, 190), (1.18, 200), (1.2, 190), (1.26, 230), (1.35, 190)]
    late_shadows = []
    STEP = 0.2                                     # s per step of their walk (walk_a / walk_b)
    for i, (x, y, kind, var, fc, s_, style) in enumerate(S19.CROWD):
        t_go, v = CROWD_GO[i]
        x20 = m19(x, y)[0]
        hw = 80 * s_ / 0.6                         # half their width, stage px (with arms out)

        def dist(t, t_go=t_go, v=v):
            u = t - t_go
            return 0.0 if u <= 0 else v * (u * u / 0.4 if u < 0.2 else u - 0.1)

        def here(t, x20=x20, hw=hw, dist=dist):
            """Still in the picture (and swept with the wipe should it ever catch them)."""
            xc = x20 - dist(t)
            return 0.0 if xc + hw < view_x(t, -1) - 4 else plate_at(xc, t)

        # (one shadow layer per person, all at the old single shadow layer's place in the stack: the others are
        # added at the very end, so no later layer's index - and watercolour seed - changes)
        sh_layer = (f"p19_crowd_sh{i}", doc(at19(C.ground_shadow(x, y, s_, width=110 if kind == "child" else 120,
                                                                  opacity=0.2))),
                    lambda t, dist=dist, here=here: Tf(dx=-dist(t), alpha=here(t)))
        if i == 0:
            z_sh = len(sc.layers) + len(sc.dynamics)
            sc.add(sh_layer[0], sh_layer[1], wc=0, motion=sh_layer[2], z=z_sh)
        else:
            late_shadows.append(sh_layer)
        frames = [doc(at19(C.citizen(x, y, s_, fc if p in ("stand", "cheer") else -1, kind=kind, variant=var,
                                     pose=p, attire="sackcloth", expr="happy" if p != "cheer" else None)))
                  for p in ("stand", "cheer", "walk_a", "walk_b")]
        if style == "hop":
            hops = in_s19(S19.thin_hops(V12.hop_sched(10 + i, D19, n=(2, 3), dur=(0.4, 0.52), rest=(0.6, 1.3)),
                                        *quiet19, 6.0))
            f19, m19_ = V12.hop_frame(hops), V12.hop_motion(x, y, hops, 26 * s_ / 0.6)
        else:
            hops = in_s19(S19.thin_hops(V12.hop_sched(30 + i, D19, n=(1, 1), dur=(0.9, 1.4), rest=(0.7, 1.6)),
                                        *quiet19, 7.0))
            f19 = V12.hop_frame(hops, 0.0, 0.0)
            m19_ = M.combine(V12.hop_motion(x, y, hops, 5), M.breathe(0.01, 2.8, pivot=(x, y), phase=i * 0.2))

        def c_frame(t, t_go=t_go, f19=f19):
            if t < t_go:
                return f19(t + T19)
            return 2.0 + int((t - t_go) / STEP) % 2

        def c_motion(t, t_go=t_go, m_=mot19(m19_), dist=dist, here=here):
            if t < t_go:
                return m_(t)
            u = t - t_go
            return Tf(dx=-dist(t), dy=-4 * abs(math.sin(math.pi * u / STEP)), alpha=here(t))
        sc.add(f"p19_crowd{i}", frames, frame_at=c_frame, wc=0.5, motion=c_motion)
    add19("p19_knoll", doc19(S19.knoll_svg(), span_y=m19(0, S19.knoll_y(2000))[1]), mot19(None), wc=0.85)

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
    KNOCK_LEAN = [("post_br", 3.0), ("post_bl", -3.0), ("post_fl", -3.0)]   # (toward its side, deg)

    POST_DROP = 0.12                               # a post comes down this long before its knock

    def post_motion(name):
        tp_ = pop_t[name]
        bx, by = bstage(*POST_BASE[name])
        knocked = name == "post_fr"                # the one beside him: driven in with a squash

        def m(t):
            if not knocked:                        # the others (a stick from the bundle each) drop into their
                t0 = tp_ - POST_DROP               # holes as the frame pieces do, landing exactly on the knock
                if t < t0:
                    return Tf(alpha=0.0)
                a = min(1.0, (t - t0) / 0.05)
                if t < tp_:
                    return Tf(dy=-70 * (1 - M.ease("in")((t - t0) / POST_DROP)), alpha=a)
                u = t - tp_
                sy = 1 - 0.08 * math.sin(math.pi * u / 0.1) if u < 0.1 else 1.0
                return Tf(sx=1 + 0.5 * (1 - sy), sy=sy, px=bx, py=by)
            if t < tp_ - 0.05:
                return Tf(alpha=0.0)
            u = t - (tp_ - 0.05)
            a = min(1.0, u / 0.05)
            if u < 0.08:
                sy = 0.5 + 0.58 * M.ease("out")(u / 0.08)
            else:
                sy = 1.08 - 0.08 * M.progress(u, 0.08, 0.24, "sine")
            sx = 1 + 0.5 * (1 - sy) if sy < 1 else 1 - 0.35 * (sy - 1)
            return Tf(sx=sx, sy=sy, alpha=a, px=bx, py=by)
        return m

    def piece_motion(t0):
        """One piece of the frame, put up by his raised hands: it fades in over 4 frames 50 px above its place,
        comes down onto the posts and settles with a little bounce (the pieces follow each other 0.11 s apart,
        so no frame adds more than one stick)."""
        t1 = t0 + PIECE_DROP

        def m(t):
            if t < t0:
                return Tf(alpha=0.0)
            a = M.progress(t, t0, t0 + 0.12, "sine")
            if t < t1:
                dy = -50 * (1 - M.ease("in")(M.progress(t, t0, t1, "linear")))
            else:
                v = t - t1
                dy = -6 * math.sin(math.pi * v / 0.12) if v < 0.12 else 0.0
            return Tf(dy=dy, alpha=a)
        return m

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
    t_piece = {k: t_lift + d for k, d in PIECES}
    sc.add("tiebar", bdoc(["tiebar"]), motion=piece_motion(t_piece["tiebar"]), wc=0.8)
    sc.add("cloth", bdoc(["cloth"]), motion=cloth_motion, reveal=cloth_reveal(), wc=0.8)
    for k in ("frame_back", "rafter_fl", "rafter_fr"):
        sc.add(k, bdoc([k]), motion=piece_motion(t_piece[k]), wc=0.8)
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
    F_MID = jadd("tired_mid", POSE["throw_down"], 1, "tired", tint=True)   # in-between: arms coming down
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
        if t < t_lift:                             # (after the last knock he keeps the stone down until the lift)
            hit = any(kn - 0.05 <= t < kn + 0.1 for kn in knocks) or t >= knocks[-1] - 0.05
            return F_HDN if hit else F_HUP
        if t < t_throw:
            return F_LIFT
        if t < t_tired - 0.1:
            return F_THROW
        if t < t_tired:
            return F_MID
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
        for kn in knocks:                          # the whole body jolts on each knock...
            u = t - kn
            if 0 <= u < 0.16:
                sy *= 1 - 0.025 * math.sin(math.pi * u / 0.16)
        for name, lean in KNOCK_LEAN:              # ...leaning a little toward each post that drops in
            u = t - (pop_t[name] - POST_DROP)
            if 0 <= u < 0.3:
                rot += lean * math.sin(math.pi * u / 0.3)
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
               f'{bundle_local(k)}</g></g>') for k in range(len(BUNDLE_STATES))]
    # a stick leaves it as each of the posts after the first comes down, then the frame pieces, then the cloth
    t_used = [pop_t[k] - POST_DROP for k in ("post_br", "post_bl", "post_fl")] + [t_lift, t_cloth0]

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

    sc.add("bundle", bfr, frame_at=bun_frame, motion=bun_motion, wc=0.6)

    # =========================================================== LIZARD (s19's; scurries over to its own stone)
    # It starts exactly where s19 leaves it: on s19's big stone beside the bundle (part of the opening plate),
    # doing push-ups on s19's clock. As Jonah comes walking toward that spot it scurries out of his way: hops down,
    # runs east and hops up onto its own stone (LIZ_STONE, as s21's), where it basks with push-ups on this scene's
    # clock (in step with s21 at the end).
    LIZ0 = m19(2200, S19.knoll_y(2190) + 6 - 90)      # as s19's lizard (scale 0.62 on its stage)
    S_LIZ0 = 0.62 * R19
    LIZ_A = (LIZ0[0] + 120, LIZ0[1] + 92)             # down on the ground right of s19's stone
    LIZ_B = (LIZ_STONE[0] - LIZ_STONE[2] / 2 - 10, LIZ_STONE[1] - 3)   # at the foot of its own stone
    SEG = (0.22, 0.64, LIZ_RUN)                        # hop down | run | hop up (s after t_liz0)
    t_liz1 = t_liz0 + LIZ_RUN
    liz = [doc(V11._lizard(LIZ[0], LIZ[1], LIZ_S, legs=lg)) for lg in (0, 1)]

    def liz_frame(t):
        u = t - t_liz0
        return float(int(u * 16) % 2) if 0 <= u < LIZ_RUN else 0.0

    def liz_motion(t):
        u = t - t_liz0
        rot, sq = 0.0, 1.0
        if u < 0:                                  # on s19's stone: s19's push-ups (as s19)
            x, y, s = LIZ0[0], LIZ0[1], S_LIZ0
            v = (t + T19 + 0.7) % 3.1
            b = abs(math.sin(math.pi * v / 0.2)) if v < 0.4 else 0.0
        elif u < LIZ_RUN:                          # the scurry
            b = 0.0
            s = S_LIZ0 + (LIZ_S - S_LIZ0) * M.progress(u, 0.0, LIZ_RUN, "sine")
            if u < SEG[0]:
                f = u / SEG[0]
                x = LIZ0[0] + (LIZ_A[0] - LIZ0[0]) * f
                y = LIZ0[1] + (LIZ_A[1] - LIZ0[1]) * f * f - 34 * math.sin(math.pi * f)
                rot = 14 * math.sin(math.pi * f)
            elif u < SEG[1]:
                f = (u - SEG[0]) / (SEG[1] - SEG[0])
                x = LIZ_A[0] + (LIZ_B[0] - LIZ_A[0]) * f
                y = LIZ_A[1] + (LIZ_B[1] - LIZ_A[1]) * f - 3 * abs(math.sin(4 * math.pi * f))
                rot = 3 * math.sin(8 * math.pi * f)
            else:
                f = (u - SEG[1]) / (LIZ_RUN - SEG[1])
                x = LIZ_B[0] + (LIZ[0] - LIZ_B[0]) * f
                y = LIZ_B[1] + (LIZ[1] - LIZ_B[1]) * math.sqrt(f) - 20 * math.sin(math.pi * f)
                rot = -16 * math.sin(math.pi * f)
        else:                                      # on its own stone: push-ups on this scene's clock
            x, y, s = LIZ[0], LIZ[1], LIZ_S
            v = (t + 0.4) % 2.6
            b = abs(math.sin(math.pi * v / 0.2)) if (v < 0.4 and t - v >= t_liz1 + 0.3) else 0.0
            w = t - t_liz1
            if w < 0.14:                           # landing squash
                sq = 1 - 0.1 * math.sin(math.pi * w / 0.14)
        k = s / LIZ_S
        return Tf(dx=x - LIZ[0], dy=y - LIZ[1], rot=rot, sx=k * (1 - 0.03 * b) / sq ** 0.5, sy=k * (1 + 0.13 * b) * sq,
                  px=LIZ[0], py=LIZ[1])
    sc.add("lizard", liz, frame_at=liz_frame, motion=liz_motion, wc=0.5)

    # God's light of s19's last frame on Jonah, the bundle and the lizard (s19's own drawings, shimmering on s19's
    # clock, as s19); it fades as he answers nothing
    light_in19 = lambda t19: M.progress(t19, t_light19 + 0.1, t_light19 + 0.8, "sine")
    sc.add("p19_light_pool", doc19(S19.light_pool_svg(), feather=False), wc=0, motion=mot19(
        lambda t19: Tf(alpha=light_in19(t19) * (0.85 + 0.15 * math.sin(2 * math.pi * (t19 - t_light19) / 2.6))),
        a_fade))
    for k in range(2):
        sc.add(f"p19_rays{k}", doc19(S19.rays_svg(k), feather=False), wc=0, motion=mot19(
            lambda t19, k=k: Tf(alpha=light_in19(t19) * (0.78 + 0.22 * (0.5 + 0.5 * math.sin(
                2 * math.pi * (t19 - t_light19) / 2.2 + k * math.pi)))), a_fade))

    sc.add("jonah_shadow", doc(C.ground_shadow(AX, GY, SJ, width=150, opacity=0.26)), motion=shadow_motion, wc=0)
    sc.add("jonah", frames, frame_at=lambda t: float(j_frame(t)), motion=j_motion, wc=0.6)

    # shade on Jonah: a cool flat copy of his own silhouette, multiplied (only under the finished roof)
    shade_amt = lambda t: 0.24 * M.progress(t, t_cloth1, t_cloth1 + 0.4, "sine") + \
        0.16 * M.progress(t, t_sit, t_sit + 0.5, "sine")
    sc.add("jonah_shade", flat, frame_at=lambda t: float(tint_idx.get(j_frame(t), 0)), wc=0, blend="multiply",
           motion=M.combine(j_motion, lambda t: Tf(alpha=shade_amt(t) if j_frame(t) in tint_idx else 0.0)))
    # s19's warm glow from the light (additive, over Jonah too, as s19), fading with it
    sc.add("p19_warm", doc19(S19.warm_svg(), feather=False), wc=0, blend="add", motion=mot19(
        lambda t19: Tf(alpha=0.45 * M.progress(t19, t_light19 + 0.2, t_light19 + 1.2, "sine") *
                       (0.8 + 0.2 * math.sin(2 * math.pi * (t19 - t_light19) / 2.3))), a_fade))

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
    # this scene's own foreground comes in with the wipe (the complement of the plate's edge)
    sc.add("fg_rocks", doc(S.g(fg, filter="wobble") + span(1240)), wc=0.9, motion=world, reveal=wipe_in)

    def grass_fn(ph):
        return lambda t: 1.5 + 1.4 * math.sin(2 * math.pi * (t / 2.6 + ph))

    for gi, tufts in enumerate([[(300, 1215, 1.1, 1), (560, 1250, 0.9, 1), (90, 1255, 1.0, 1)],
                                [(2620, 1215, 1.0, 1), (2850, 1200, 0.9, 1), (3040, 1250, 1.0, 1)],
                                [(1950, 1080, 0.7, 1), (2420, 1075, 0.7, 1), (1000, 1060, 0.65, 1)],
                                [(1720, 1210, 0.9, 1), (2150, 1190, 0.8, 1), (820, 1180, 0.85, 1)]]):
        gframes = [doc("".join(PR.grass_tuft(x, y, s_, variant=v, sway=sw_) for x, y, s_, v in tufts) +
                       span(tufts[0][1] - 20)) for sw_ in (0.5, 0.0, -0.5, -1.0)]
        sc.add(f"grass{gi}", gframes, frame_at=grass_fn(gi * 0.23), wc=0.7, motion=world, reveal=wipe_in)

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
            heat = 1 - plate_at(bx, t)             # (no heat shimmer over s19's green plain)
            if heat <= 0.01:
                continue
            u = (t * 0.55 + i * 0.37) % 1.0
            ox, oy = view.to_out(bx, by - 80 * u)
            if not (-60 < ox < frame.size[0] + 60):
                continue
            a = int(95 * heat * math.sin(math.pi * u))
            for j in range(3):
                x0 = ox + (j - 1) * 22 * sc_
                pts = [(x0 + 7 * sc_ * math.sin(q * 1.1 + t * 7 + i), oy - q * 9 * sc_) for q in range(9)]
                d.line(pts, fill=(255, 248, 226, a), width=max(2, int(4 * sc_)), joint="curve")
        frame.alpha_composite(ov)
        return frame

    # warm heat vignette (as FX.vignette(0.16) but precomputed); it comes in with the desert (none in s19)
    _vg = {}

    def vignette(frame, t, view):
        kv = M.progress(t, t_w0, t_w1, "sine")
        if kv <= 0.002:
            return frame
        if "k" not in _vg:
            Hh, Ww = frame.size[1], frame.size[0]
            yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
            rr = np.sqrt(((xx - Ww / 2) / (Ww / 2)) ** 2 + ((yy - Hh / 2) / (Hh / 2)) ** 2)
            a = np.clip(np.clip((rr - 0.35) / 0.95, 0, 1) ** 1.6 * 0.16, 0, 1)
            _vg["k"] = cv2.merge([np.round((1 - a) * 255).astype(np.uint8)] * 3)
            _vg["c"] = cv2.merge([np.round(a * c).astype(np.uint8) for c in (150, 82, 30)])
        kk, cc = _vg["k"], _vg["c"]
        if kv < 0.998:
            kk = cv2.addWeighted(kk, kv, np.full_like(kk, 255), 1 - kv, 0)
            cc = cv2.convertScaleAbs(cc, alpha=kv)
        arr = np.array(frame)
        arr[..., :3] = cv2.add(cv2.multiply(arr[..., :3], kk, scale=1 / 255.0), cc)
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

    for i, (name, svg, mo) in enumerate(late_shadows):     # the crowd's other shadows (see above)
        sc.add(name, svg, wc=0, motion=mo, z=z_sh + 0.01 * (i + 1))

    # =========================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("heat", 0, dur=T, gain_db=-19, fade_in=0.8, fade_out=0.8)
    # s19's cheering city carries on, low, dying away as the people go home and the city is left behind
    sc.sfx("cheer", 0, dur=t_w1, gain_db=-26, fade_in=0.8, fade_out=t_w1 - 1.2, pan=-0.45)
    sc.sfx("cloth", t_up - 0.05, gain_db=-15, pan=-0.2)
    sc.sfx("whoosh", t_grab - 0.02, gain_db=-17, pan=-0.2)
    sc.sfx("thud", t_on - 0.02, gain_db=-15, pan=-0.2)
    for tc in contacts:                          # one footstep on every footfall of the walk cycle
        sc.sfx("footsteps", round(tc - STEP_LEAD, 3), dur=STEP_DUR, rate=0.5, gain_db=-10, fade_in=0.01,
               fade_out=0.08, pan=-0.1)
    sc.sfx("cloth", t_toss, gain_db=-14, pan=-0.1)
    sc.sfx("thud", t_land - 0.02, gain_db=-8, pan=-0.1)
    sc.sfx("hammer", hammer_at, gain_db=-6, pan=0.15)
    for k, d in PIECES[:-1]:                    # a soft knock as each frame piece lands...
        sc.sfx("thud", t_lift + d + PIECE_DROP - 0.02, gain_db=-18, pan=0.05)
    sc.sfx("thud", t_frame_on - 0.02, gain_db=-11, pan=0.05)    # ...and the ridge, last
    sc.sfx("cloth", t_cloth0 - 0.03, gain_db=-6)
    sc.sfx("pop", t_branch, gain_db=-14)
    sc.sfx("thud", t_sit + 0.02, gain_db=-13)
    sc.sfx("birds", t_dove - 0.1, dur=min(3.2, T - t_dove), gain_db=-17, fade_in=0.3, fade_out=0.9, pan=-0.3)
    return sc
