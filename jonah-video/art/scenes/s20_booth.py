"""Scene 20 — the booth (Jonah 4:5).

One wide 3100 x 1300 stage on a hot, cloudless-ish afternoon. Left: Nineveh's east wall with its open gate
(mid-distance, hazy, little townspeople in sackcloth on the wall and in the gateway, sheep in sackcloth by the
watered fields), a road running from the gate across the plain onto a dry ochre ridge. Right: the bare knoll on
the ridge where Jonah builds his booth (the same props.booth drawing as s11 / s12 v1, split into its stages).
A high hot sun hangs over the booth the whole time.

Line 0 "约拿没有回答。" — Jonah stands outside the gate, arms crossed, his bundle of sticks and rolled cloth on his
        back, still bathed in the soft golden light of God's question (light only, never a figure). He turns
        his back on it with a squash-hop and a grumpy "hmph" (eyes shut, chin up, steam puffs); the light fades.
        "他出了城，坐在城的东边，" — he marches east along the road (a planted-foot walk cycle: the drawing follows
        the distance walked), the camera tracking him, stops on the knoll and tosses the bundle down (thud).
        "为自己搭了一座小棚子。" — with a stone he knocks the four posts in, one per knock of the 'hammer' sound
        (the cue time is chosen so the sound has 4 knocks and the knock onsets are read from it); lifts the
        frame (tie bar, rafters, ridge) which drops into place; throws the striped cloth over the ridge (it
        unrolls downward and settles); leafy branches pop on top. The bundle on the ground shrinks as he uses it.
        He stands under the roof, hot and panting (sweat).
Line 1 "他坐在棚子下面的阴凉里，" — he sits down in the booth's thin shade (hop + dust), a cool tint settles on him,
        eyes closed with relief and a big sigh; the camera pushes in a little; two doves fly toward the city.
        "要看看这座城到底会怎么样。" — chin on fist, a sulky eye on the city; the camera pulls back to reveal the
        city he is watching and settles on a calm wide view (blinks, breathing, the cloth stirring).

Notes for maintainers
* Every time comes from ctx.lines[i].at(phrase) / .start (never fixed numbers).
* Pose changes are hard cuts hidden by a squash-and-hop (v1 technique); expression-only changes are cuts too
  (blinks). Jonah's custom poses use characters' rig (C._P / C._figure) with the standard Jonah design; two
  extra expressions are added to characters.EXPRS only while a drawing is built (removed again right after).
* The bundle is ONE local drawing (bundle_local) used both on his back (via the design's 'behind' hook) and on
  the ground, so the toss starts exactly where it was on his back.
* Booth parts are separate layers while it goes up; once Jonah sits, three layers (back / cloth / front) take
  over, and the cloth alone breathes gently.
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
WALK_N = 5                     # drawings per step (two steps per cycle)

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
POSE = {
    "cross": C._P(h=6, look=(0.02, -0.07), arms=(("ik", "torso", -0.2, 0.62, 1), ("ik", "torso", 1.25, 0.58, 1)),
                  far_front=True),
    "hmph": C._P(t=-3, h=-14, arms=(("ik", "torso", -0.2, 0.62, 1), ("ik", "torso", 1.25, 0.58, 1)),
                 far_front=True),
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
XB = 1900                         # booth anchor (bottom centre between the front posts)
X_C = XB + 40                     # Jonah hammers, lifts, throws the cloth and sits here
WALK_STEPS = 6
ADV = 2 * WALK_A / WALK_N * SJ    # stage px the anchor advances per walk drawing (planted sole stays put)
NWALK = WALK_STEPS * WALK_N       # walk drawings from the gate road to the booth
XJ0 = X_C - NWALK * ADV           # where he stands outside the gate
AX = 1500                         # every Jonah drawing is made at (AX, GY) and moved by its layer motion
WALL_Y, WALL_H = 790, 250         # Nineveh's east wall (mid-distance)
GATE_X, GATE_W = 780, 150
WALL_X1 = 1180                    # corner tower closing the wall
XBUN, YBUN = XB - 450, GY - 22    # where the bundle lands (centre of the lying bundle)
CAM_REF = (1450, 668)             # final camera centre: sky parallax offsets are zero there
SUN = (1700, 300)
LIZ = (2330, 1088)
CX, CY = SW // 2, SH // 2

POST_BASE = {"post_fl": (-158, 2), "post_fr": (146, 2), "post_bl": (-112 + PR.BOOTH_DEPTH[0] * 0.9, -16),
             "post_br": (146 + PR.BOOTH_DEPTH[0] * 0.9, -18)}


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def bstage(lx, ly):
    return (XB + lx * SB, GY + ly * SB)


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


def _env(t, a, b, c, d):
    if t <= a or t >= d:
        return 0.0
    if t < b:
        return M.progress(t, a, b, "sine")
    if t <= c:
        return 1.0
    return 1 - M.progress(t, c, d, "sine")


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


def sun_svg():
    glow = (f'<circle cx="{CX}" cy="{CY}" r="400" fill="url(#sg)"/>')
    return doc(glow,
               S.rad_grad("sg", [(0, "#fffbe4", 0.95), (0.22, "#fff3c2", 0.7), (0.55, "#fde6a6", 0.22),
                                 (1, "#f8dc98", 0)]))


def rays_svg():
    d = S.rays(CX, CY, 84, 136, n=14, width_deg=12)
    return doc(S.g(f'<path d="{d}" fill="#ffcf55" stroke="#c9821f" stroke-width="4" stroke-linejoin="round"/>',
                   filter="wobble"))


# ================================================================== build
def build(ctx):
    from PIL import Image, ImageDraw

    from art.scenes_v1 import s11_vine as V11
    from art.scenes_v1 import s12_lesson as V12

    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]

    # ------------------------------------------------------------ key times (from the narration chunks)
    t_turn = L0.at("没有回答") + 0.5              # turns his back on the question: "hmph!"
    t_walk0 = L0.at("出了城") - 0.1               # marches out along the road east of the city
    t_arr = L0.at("搭了") - 0.5                   # arrives on the ridge, tosses the bundle down
    t_toss = t_arr
    t_land = t_toss + 0.36
    t_ham = L0.at("搭了")                         # "为自己搭了一座小棚子": posts knocked in...
    hammer_at, knocks = _hammer_knocks(t_ham + 0.13, ctx.id)
    t_lift = knocks[-1] + 0.3                     # ...the frame lifted onto them...
    t_frame = t_lift + 0.08                       # frame drops in
    t_frame_on = t_frame + 0.24                   # ...and lands
    t_throw = t_lift + 0.62                       # ...and the cloth thrown over the ridge
    t_cloth0, t_cloth1 = t_throw + 0.05, t_throw + 0.42
    t_branch = t_throw + 0.55
    t_tired = t_throw + 0.62                      # phew, hot! (sweat)
    t_sit = L1.start + 0.12                       # "他坐在棚子下面的阴凉里"
    t_chin = L1.at("要看看") + 0.22               # chin on fist, eyes on the city
    blinks = [t_chin + 1.4, t_chin + 2.6]
    t_full = t_sit                                # the booth parts are swapped for one booth layer here

    # ------------------------------------------------------------ camera (built first: parallax uses it)
    cam = M.cam_keys([
        (0.0, Cam(990, 724, 1800)),
        (t_walk0 - 0.15, Cam(1010, 724, 1790)),
        (t_ham + 0.25, Cam(1770, 736, 1800)),
        (t_tired + 0.3, Cam(1790, 738, 1780)),
        (L1.at("要看看") + 0.1, Cam(1880, 770, 1600)),
        (min(T - 1.3, L1.at("要看看") + 2.9), Cam(1490, 690, 1880)),
        (T, Cam(1482, 688, 1892)),
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
    sc.add("sun", sun_svg(), wc=0.4, motion=par(0.6, M.combine(
        lambda t: Tf(dx=SUN[0] - CX, dy=SUN[1] - CY), M.breathe(0.02, 2.2, pivot=(CX, CY)))))
    sc.add("sun_rays", rays_svg(), wc=0.3, z=None, motion=par(0.6, M.combine(
        lambda t: Tf(dx=SUN[0] - CX, dy=SUN[1] - CY), lambda t: Tf(rot=5 * t, px=CX, py=CY),
        M.breathe(0.03, 1.6, pivot=(CX, CY)))))
    sc.add("sun_disc", doc(S.g(f'<circle cx="{CX}" cy="{CY}" r="68" fill="#ffd64a" stroke="#c9741f" '
                               f'stroke-width="5"/><circle cx="{CX}" cy="{CY}" r="52" fill="#ffeb98"/>'
                               f'<circle cx="{CX}" cy="{CY}" r="32" fill="#fff8d6"/>'
                               f'<circle cx="{CX - 23}" cy="{CY - 23}" r="14" fill="#fffef4" opacity="0.85"/>',
                               filter="wobble")),
           wc=0.3, motion=par(0.6, M.combine(lambda t: Tf(dx=SUN[0] - CX, dy=SUN[1] - CY),
                                             M.breathe(0.025, 1.3, pivot=(CX, CY)))))
    clouds = doc(S.g(S.cloud(560, 370, 250, 76, "#fdf3e4", seed=3, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(1230, 300, 200, 62, "#fdf1e2", seed=6, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2330, 350, 270, 82, "#fdf3e4", seed=8, sw=3, shade_fill="#f0d6c4") +
                     S.cloud(2930, 270, 220, 66, "#fdf1e2", seed=9, sw=3, shade_fill="#f0d6c4"), filter="wobble"))
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
    # soft dune swells: sunlit crests and shaded troughs across the dry plain
    def band(x0, x1, y, h, amp, seed):
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
    pl += f'<rect x="-40" y="790" width="1500" height="200" fill="url(#gf)"/>'
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
    # a distant oasis to the east; sheep in sackcloth (Jonah 3:8) grazing by the fields
    for (x, y, s_, ln) in [(2620, 742, 0.16, 0.1), (2668, 746, 0.13, -0.1), (2715, 744, 0.15, 0.05)]:
        pl += PR.palm_tree(x, y, s_, lean=ln)
    pl += PR.bush(2560, 750, 0.22, variant=0) + PR.bush(2760, 752, 0.2, variant=0)
    for (x, y, s_, f_) in [(470, 900, 0.3, 1), (560, 912, 0.27, -1), (1030, 905, 0.26, -1)]:
        pl += PR.animal(x, y, s_, f_, kind="sheep", sackcloth=True)
    plain_defs = (S.lin_grad("pl", [(0, "#efdcb2"), (0.3, "#ead1a0"), (1, "#dcb57c")]) +
                  S.lin_grad("gf", [(0, "#c9cf86", 0.55), (0.6, "#d6cf8c", 0.3), (1, "#e0d29a", 0)], x2=1, y2=0))
    sc.add("plain", doc(S.g(pl, filter="wobble"), plain_defs), wc=0.8)

    # Nineveh: skyline behind the east wall, the open gate, little people (hazy with distance, thin ink)
    walkers = ""
    for i, (x, kind, pose) in enumerate([(120, "man", "stand"), (150, "woman", "stand"), (330, "child", "stand"),
                                         (520, "man", "stand"), (545, "woman", "stand"), (980, "elder", "stand"),
                                         (1010, "child", "stand")]):
        s_ = 0.2 if kind != "child" else 0.22
        walkers += C.citizen(x, WALL_Y - WALL_H + (28 if kind != "child" else 12), s_, 1 if i % 2 else -1, kind=kind,
                             variant=i % 4, pose=pose, attire="sackcloth")
    wall = PR.city_wall(-80, WALL_X1, WALL_Y, WALL_H, gate=(GATE_X, GATE_W), doors_open=1.0, seed=4, ink=0.7)
    wall += V12._end_tower(WALL_X1, WALL_Y, WALL_H / 260, ink=0.7)
    gateway = (C.citizen(GATE_X - 30, WALL_Y - 2, 0.36, 1, kind="woman", variant=3, pose="stand", attire="sackcloth") +
               C.citizen(GATE_X + 26, WALL_Y - 2, 0.32, -1, kind="child", variant=1, pose="stand",
                         attire="sackcloth"))
    haze = ('<filter id="hz" x="-2%" y="-8%" width="104%" height="116%" color-interpolation-filters="sRGB">'
            '<feColorMatrix type="saturate" values="0.75"/>'
            '<feColorMatrix type="matrix" values="0.78 0 0 0 0.2  0 0.78 0 0 0.183  0 0 0.78 0 0.15  0 0 0 1 0"/>'
            '</filter>')
    city = PR.nineveh_skyline(-80, 1140, WALL_Y - 18, scale=0.72, seed=2, haze=0.35, tint="#f3dcb4")
    trees = ""
    for (x, y, s_, ln) in [(60, WALL_Y + 12, 0.36, 0.1), (410, WALL_Y + 14, 0.34, -0.1), (1010, WALL_Y + 10, 0.38, 0.15),
                           (1290, WALL_Y + 22, 0.42, -0.12), (1385, WALL_Y + 30, 0.34, 0.1)]:
        trees += _palm(x, y, s_, ln)
    trees += PR.olive_tree(1160, WALL_Y + 40, 0.3, seed=1) + PR.olive_tree(560, WALL_Y + 36, 0.28, seed=2)
    sc.add("city", doc(f'<g filter="url(#hz)">{city}{walkers}{wall}{gateway}{trees}</g>', haze), wc=0.7)

    # mid-plain: bushes and stones on the dry ground east of the city
    mid = ""
    for (x, y, s_, v) in [(1450, 905, 0.5, 2), (1760, 880, 0.45, 2), (2240, 900, 0.52, 2), (2680, 870, 0.46, 2),
                          (2950, 915, 0.5, 2), (860, 960, 0.5, 0), (300, 945, 0.55, 3)]:
        mid += PR.bush(x, y, s_, variant=v)
    for (x, y, w_, h_, sd) in [(1600, 925, 90, 44, 3), (1660, 930, 40, 20, 13), (2420, 915, 76, 38, 4),
                               (2830, 940, 96, 48, 6), (1040, 965, 60, 30, 7)]:
        mid += V11._stone(x, y, w_, h_, seed=sd, sw=3)
    sc.add("mid", doc(mid), wc=0.8)

    # =========================================================== THE RIDGE (Jonah's path, the booth's knoll)
    ridge_pts = [(-80, 1012), (250, 1004), (600, 998), (900, 994), (1150, 988), (1450, 968), (1750, 954),
                 (2050, 950), (2350, 958), (2650, 974), (2900, 986), (3180, 992)]
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
    rocks = ""
    for (x, y, s_, sd, n) in [(1290, 1006, 0.9, 3, 3), (2480, 1000, 1.0, 4, 2), (760, 1030, 0.8, 5, 2),
                              (1580, 1100, 0.9, 6, 2), (2860, 1040, 1.0, 7, 3)]:
        rocks += V11._pebbles(x, y, s_, seed=sd, n=n)
    for (x, y, s_, v) in [(1235, 1000, 0.62, 2), (2560, 985, 0.72, 2), (420, 1004, 0.6, 2)]:
        rocks += PR.bush(x, y, s_, variant=v)
    rocks += V11._stone(LIZ[0] - 4, LIZ[1] + 8, 140, 52, seed=41, sw=4, crack=True)
    sc.add("ridge_rocks", doc(S.g(rocks, filter="wobble-fine")), wc=0.8)

    # God's question still hangs in the air at the start: soft warm light from the upper left, fading as Jonah
    # turns his back on it (never a figure: only light)
    ox, oy = 200, -150                         # off-frame, upper left
    jx, jy = XJ0 - 20, GY - 200

    def fan(length, angles, widths):
        d = ""
        for a, w in zip(angles, widths):
            a0, a1, am = math.radians(a - w / 2), math.radians(a + w / 2), math.radians(a)
            p0 = (ox + 18 * math.cos(am - 1.2), oy + 18 * math.sin(am - 1.2))
            p3 = (ox + 18 * math.cos(am + 1.2), oy + 18 * math.sin(am + 1.2))
            p1 = (ox + length * math.cos(a0), oy + length * math.sin(a0))
            p2 = (ox + length * math.cos(a1), oy + length * math.sin(a1))
            d += f"M{p0[0]:.0f},{p0[1]:.0f} L{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f} L{p3[0]:.0f},{p3[1]:.0f} Z "
        return d
    gdef = (f'<linearGradient id="rayg" gradientUnits="userSpaceOnUse" x1="{ox}" y1="{oy}" x2="{jx}" y2="{jy + 300}">'
            f'<stop offset="0" stop-color="#fff4cc" stop-opacity="0.85"/>'
            f'<stop offset="0.6" stop-color="#ffe7a0" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#ffdf8c" stop-opacity="0.12"/></linearGradient>'
            f'<linearGradient id="coneg" gradientUnits="userSpaceOnUse" x1="{ox}" y1="{oy}" x2="{jx}" y2="{jy + 300}">'
            f'<stop offset="0" stop-color="#fff2c4" stop-opacity="0.6"/>'
            f'<stop offset="1" stop-color="#ffe39a" stop-opacity="0.1"/></linearGradient>' +
            S.rad_grad("halo", [(0, "#fff6d6", 0.75), (0.6, "#ffe7a4", 0.32), (1, "#ffe0a0", 0)]) +
            S.rad_grad("pool", [(0, "#fff1c0", 0.8), (0.6, "#ffe39a", 0.3), (1, "#ffd77e", 0)]))
    ln = math.hypot(jx - ox, jy - oy) + 260
    aim = math.degrees(math.atan2(jy - oy, jx - ox))
    light = doc(f'<path d="{fan(ln, [aim], [13])}" fill="url(#coneg)" filter="url(#blur-lg)"/>'
                f'<path d="{fan(ln, [aim - 7, aim - 3.5, aim, aim + 3.6, aim + 7.5], [2.6, 1.8, 3.0, 1.9, 2.5])}" '
                f'fill="url(#rayg)" filter="url(#soft)"/>'
                f'<ellipse cx="{jx}" cy="{GY - 210}" rx="210" ry="290" fill="url(#halo)"/>'
                f'<ellipse cx="{jx + 10}" cy="{GY - 4}" rx="260" ry="62" fill="url(#pool)"/>', gdef)
    a_light = lambda t: 0.85 * (1 - M.progress(t, t_turn - 0.1, t_turn + 1.1, "sine"))
    sc.add("god_light_sky", light, wc=0, motion=lambda t: Tf(alpha=a_light(t) * (0.9 + 0.1 * math.sin(t * 3))))


    # =========================================================== THE BOOTH (built in stages)
    parts = booth_parts()

    def bdoc(keys):
        return doc(PR._place("".join(parts[k] for k in keys), XB, GY, SB, 1))

    # ground shade under the roof (thin cloth: a soft cool shadow), appears with the cloth
    a_roof = lambda t: M.progress(t, t_cloth0 + 0.1, t_cloth1 + 0.3, "sine")
    sc.add("booth_gshade", doc(f'<ellipse cx="{XB + 14 * SB:.0f}" cy="{GY - 4}" rx="{196 * SB:.0f}" ry="{34 * SB:.0f}" '
                               f'fill="#8f7c8a" opacity="0.6" filter="url(#soft)"/>'),
           wc=0, blend="multiply", motion=lambda t: Tf(alpha=a_roof(t)))

    pop_t = {"post_fr": knocks[0], "post_br": knocks[1], "post_bl": knocks[2], "post_fl": knocks[3]}
    live = lambda t: t < t_full                   # the parts are drawn until the whole booth takes over

    def post_motion(name):
        tp_ = pop_t[name]
        bx, by = bstage(*POST_BASE[name])

        def m(t):
            if t < tp_ - 0.05 or not live(t):
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

    def frame_motion(t):
        if t < t_frame - 0.06 or not live(t):
            return Tf(alpha=0.0)
        a = M.progress(t, t_frame - 0.06, t_frame + 0.02, "sine")
        if t < t_frame_on:
            dy = -120 * (1 - M.ease("in")(M.progress(t, t_frame - 0.06, t_frame_on, "linear")))
        else:
            u = t - t_frame_on
            dy = -12 * math.sin(math.pi * min(1.0, u / 0.16)) if u < 0.16 else 0.0
        return Tf(dy=dy, alpha=a)

    def lash_motion(t):
        if t < t_frame_on + 0.08 or not live(t):
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
        if t < t_branch or not live(t):
            return Tf(alpha=0.0)
        u = t - t_branch
        s = 0.8 + 0.2 * M.ease("back")(min(1.0, u / 0.22))
        return Tf(sx=s, sy=s, alpha=min(1.0, u / 0.08), px=apex[0], py=apex[1] + 40)

    sc.add("post_bl", bdoc(["post_bl"]), motion=post_motion("post_bl"), wc=0.8)
    sc.add("post_br", bdoc(["post_br"]), motion=post_motion("post_br"), wc=0.8)
    sc.add("under", bdoc(["under"]), motion=lambda t: Tf(alpha=1.0 if (t >= t_cloth0 and live(t)) else 0.0),
           reveal=cloth_reveal(0.04), wc=0.8)
    sc.add("post_fl", bdoc(["post_fl"]), motion=post_motion("post_fl"), wc=0.8)
    sc.add("post_fr", bdoc(["post_fr"]), motion=post_motion("post_fr"), wc=0.8)
    sc.add("tiebar", bdoc(["tiebar"]), motion=frame_motion, wc=0.8)
    full = lambda t: Tf(alpha=0.0 if live(t) else 1.0)
    sc.add("booth_back", bdoc(["post_bl", "post_br", "under", "post_fl", "post_fr", "tiebar"]), motion=full, wc=0.8)
    sc.add("cloth", bdoc(["cloth"]), motion=cloth_motion, reveal=cloth_reveal(), wc=0.8)
    sc.add("frame", bdoc(["frame"]), motion=frame_motion, wc=0.8)
    sc.add("lash", bdoc(["lash"]), motion=lash_motion, wc=0.6)
    sc.add("branches", bdoc(["branches"]), motion=branch_motion, wc=0.7)
    sc.add("booth_front", bdoc(["frame", "lash", "branches"]), motion=full, wc=0.8)


    # dust where each post goes in and where the frame lands
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

    # =========================================================== THE BUNDLE (tossed down, used up)
    bfr = [doc(f'<g transform="translate({XBUN},{YBUN}) scale({SJ}) rotate(180)"><g filter="url(#wobble-fine)">'
               f'{bundle_local(k)}</g></g>') for k in range(4)]
    t_used = [knocks[1], t_frame_on, t_cloth0]

    def bun_frame(t):
        return float(sum(1 for tu in t_used if t >= tu))

    def bun_motion(t):
        if t < t_toss:
            return Tf(alpha=0.0)
        if t < t_land:
            u = (t - t_toss) / (t_land - t_toss)
            bx, by, ang = BACK
            dx0, dy0 = bx - XBUN, by - YBUN
            rot0 = ((ang - 180 + 180) % 360) - 180
            return Tf(dx=dx0 * (1 - u), dy=dy0 * (1 - u) - 70 * math.sin(math.pi * u) * (1 - 0.3 * u),
                      rot=rot0 * (1 - M.ease("out")(u)), px=XBUN, py=YBUN)
        u = t - t_land
        sq = 0.0
        if u < 0.2:
            sq = 0.08 * math.sin(math.pi * u / 0.2)
        for tu in t_used:                          # a little hop each time something is taken from it
            v = t - tu
            if 0 <= v < 0.18:
                sq = -0.05 * math.sin(math.pi * v / 0.18)
        return Tf(sx=1 + sq * 0.6, sy=1 - sq, px=XBUN, py=YBUN + 14 * SJ)

    sc.add("bundle_shadow", doc(C.ground_shadow(XBUN, GY - 2, 1.0, width=300, opacity=0.22)),
           motion=lambda t: Tf(alpha=M.progress(t, t_land - 0.12, t_land, "sine")), wc=0)

    # =========================================================== JONAH
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

    F_CROSS = jadd("cross", POSE["cross"], -1, "angry", bundle=True)
    F_HMPH = jadd("hmph", POSE["hmph"], 1, "hmph", bundle=True)
    F_WALK = [jadd(f"walk{k}", walk_pose(k), 1, "angry", bundle=True) for k in range(2 * WALK_N)]
    bx_, by_, ang_ = _BACK["walk0"]
    BACK = (X_C + bx_ * SJ, GY + by_ * SJ, ang_)
    F_STAND = jadd("stand", POSE["stand"], 1, "angry")
    F_HUP = jadd("ham_up", POSE["ham_up"], 1, "angry", stone=True)
    F_HDN = jadd("ham_dn", POSE["ham_dn"], 1, "angry", stone=True)
    F_LIFT = jadd("lift", POSE["lift"], 1, "angry")
    F_THROW = jadd("throw", POSE["throw"], 1, "angry", tint=True)
    F_TIRED = jadd("tired", POSE["stand"], 1, "tired", tint=True)
    F_SIT = jadd("sit", POSE["sit"], -1, "peaceful", tint=True)
    F_CHIN = jadd("chin", POSE["sit_chin"], -1, "watch", tint=True)
    F_BLINK = jadd("blink", POSE["sit_chin"], -1, "watch_blink", tint=True)

    def walk_k(t):
        u = (t - t_walk0) / (t_arr - t_walk0)
        return min(NWALK, int(_ease_walk(u) * NWALK + 1e-6))

    def j_frame(t):
        if t < t_turn:
            return F_CROSS
        if t < t_walk0:
            return F_HMPH
        if t < t_arr:
            return F_WALK[walk_k(t) % (2 * WALK_N)]
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
        return F_BLINK if any(b <= t < b + 0.14 for b in blinks) else F_CHIN

    def j_x(t):
        if t < t_walk0:
            return XJ0
        if t < t_arr:
            return XJ0 + walk_k(t) * ADV
        return X_C

    # pose cuts are hidden by a squash-and-hop (as in the v1 scenes)
    hops = [(t_turn, 1.0), (t_walk0, 0.35), (t_arr, 0.7), (t_ham, 0.55), (t_lift, 0.8), (t_throw, 0.6),
            (t_tired, 0.7), (t_sit, 1.0), (t_chin, 0.7)]

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
        s = 1 + (0.0 if walking else 0.011 * math.sin(2 * math.pi * t / 2.8))
        sy = s
        for kn in knocks:                          # the whole body jolts on each knock
            u = t - kn
            if 0 <= u < 0.16:
                sy *= 1 - 0.025 * math.sin(math.pi * u / 0.16)
        u = t - (t_sit + 0.55)                     # a big contented sigh in the cool shade
        if 0 <= u < 1.3:
            sy *= 1 + 0.022 * math.sin(math.pi * u / 1.3)
        if t >= t_tired and t < t_sit:             # panting in the sun
            sy *= 1 + 0.012 * math.sin(2 * math.pi * t / 0.55)
        hsy, hdy = hop(t)
        sy *= hsy
        sx = s * (1 + 0.5 * (1 - hsy))
        return Tf(dx=j_x(t) - AX, dy=hdy, sx=sx, sy=sy, px=AX, py=GY)

    def shadow_motion(t):
        _, hdy = hop(t)
        seated = t >= t_sit
        return Tf(dx=j_x(t) - AX - (22 if seated else 0), sx=1.5 if seated else 1.0, sy=1.0,
                  alpha=1 + hdy / 60.0, px=AX, py=GY)

    sc.add("jonah_shadow", doc(C.ground_shadow(AX, GY, SJ, width=150, opacity=0.26)), motion=shadow_motion, wc=0)
    sc.add("bundle", bfr, frame_at=bun_frame, motion=bun_motion, wc=0.6)
    sc.add("jonah", frames, frame_at=lambda t: float(j_frame(t)), motion=j_motion, wc=0.6)

    # shade on Jonah: a cool flat copy of his own silhouette, multiplied (only under the finished roof)
    shade_amt = lambda t: 0.24 * M.progress(t, t_cloth1, t_cloth1 + 0.4, "sine") + \
        0.16 * M.progress(t, t_sit, t_sit + 0.5, "sine")
    sc.add("jonah_shade", flat, frame_at=lambda t: float(tint_idx.get(j_frame(t), 0)), wc=0, blend="multiply",
           motion=M.combine(j_motion, lambda t: Tf(alpha=shade_amt(t) if j_frame(t) in tint_idx else 0.0)))

    # --- "hmph!": grumpy steam puffs as he turns his back ------------------------------------------------
    _, hp = jonah_fig(AX, GY, SJ, 1, POSE["hmph"], "hmph", bundle=True, label="hmph_pts")
    hx0, hy0 = hp["head"][0] - AX + XJ0, hp["head"][1]
    for side_, (ox, oy, sgn) in enumerate([(-112, 6, -1), (104, 14, 1)]):
        cx, cy = hx0 + ox, hy0 + oy

        def puff_motion(t, cx=cx, cy=cy, sgn=sgn, ph=side_ * 0.07):
            for th in (t_turn + 0.06, t_turn + 0.62):
                u = t - th - ph
                if 0 <= u < 0.8:
                    a = min(1.0, u / 0.05) * (1 - M.progress(u, 0.4, 0.8, "sine"))
                    s = 0.3 + 0.8 * M.ease("out")(u / 0.12) if u < 0.12 else 1.1 - 0.1 * M.progress(u, 0.12, 0.3)
                    e = M.ease("out")(min(1.0, u / 0.8))
                    return Tf(dx=sgn * 28 * e, dy=-50 * e, sx=s, sy=s, alpha=a, px=cx, py=cy)
            return Tf(alpha=0.0)
        sc.add(f"puff{side_}", doc(_puff(cx, cy, 30)), motion=puff_motion, wc=0.3)

    # --- dust poofs: bundle landing, stopping on arrival, sitting down -----------------------------------
    for i, (t0, x, y, k) in enumerate([(t_land, XBUN, GY + 2, 1.3), (t_arr, X_C - 10, GY, 0.9),
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
    liz = [doc(V11._lizard(LIZ[0], LIZ[1] - 40, 0.72, legs=0))]

    def liz_motion(t):
        u = (t + 0.4) % 2.6
        b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
        return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] - 38)
    sc.add("lizard", liz, motion=liz_motion, wc=0.5)

    # =========================================================== DOVES crossing the sky toward the city
    dove_frames = [doc(PR.dove(2700, 470, 0.6, -1, wing=w)) for w in (-1.0, -0.35, 0.35, 1.0)]

    def flap(fps, ph):
        seq = [0, 1, 2, 3, 2, 1]
        return lambda t: float(seq[int(t * fps + ph) % len(seq)])

    for i, (t0, dy, ph) in enumerate([(t_sit + 0.3, 0, 0), (t_sit + 0.75, 70, 2)]):
        dur = 4.6
        sc.add(f"dove{i}", dove_frames, frame_at=flap(10, ph), wc=0.4, z=5.5 + 0.01 * i, motion=M.combine(
            M.keys([(t0, {"dx": 0, "dy": dy - 30}), (t0 + dur, {"dx": -1800, "dy": dy + 40})], "linear"),
            M.bob(9, 0.7, ph * 0.1),
            lambda t, t0=t0: Tf(alpha=M.progress(t, t0, t0 + 0.3) * (1 - M.progress(t, t0 + dur - 0.4, t0 + dur)))))

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
                                [(1330, 1080, 0.7, 1), (2420, 1075, 0.7, 1), (1000, 1060, 0.65, 1)],
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
    HEAT = [(1450, 960), (2250, 950), (2750, 960), (1000, 980), (600, 960), (2500, 1110), (1600, 1120)]

    def atmos(frame, t, view):
        """Dust motes and heat shimmer rising off the hot ground, drawn on one overlay."""
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        sc_ = view.scale
        for i in range(NM):
            xx = 100 + (m_x[i] - 100 + m_vx[i] * t + 8 * math.sin(t * 0.7 + m_ph[i])) % 2900
            yy = 150 + (m_y[i] - 150 + m_vy[i] * t) % 950
            ox, oy = view.to_out(xx, yy)
            r = m_r[i] * sc_
            a = int(100 * (0.6 + 0.4 * math.sin(t * 1.3 + m_ph[i])))
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

    sc.fx = [
        FX.sparkles((520, 240, 1400, 880), count=16, t0=0.0, t1=t_turn + 0.9, color=(255, 240, 180), size=(8, 18),
                    period=1.4, drift=-8, seed=5),
        atmos,
        vignette,
    ]

    # =========================================================== SOUND
    sc.sfx("wind_soft", 0, dur=T, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("heat", 0, dur=T, gain_db=-19, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_turn - 0.05, gain_db=-14, pan=-0.3)
    sc.sfx("footsteps", t_walk0, dur=t_arr - t_walk0 + 0.1, gain_db=-11, fade_in=0.05, fade_out=0.15, pan=-0.2)
    sc.sfx("thud", t_land - 0.02, gain_db=-8, pan=-0.1)
    sc.sfx("hammer", hammer_at, gain_db=-6, pan=0.15)
    sc.sfx("thud", t_frame_on - 0.02, gain_db=-11, pan=0.05)
    sc.sfx("cloth", t_cloth0 - 0.03, gain_db=-6)
    sc.sfx("pop", t_branch, gain_db=-14)
    sc.sfx("thud", t_sit + 0.02, gain_db=-13)
    sc.sfx("birds", t_sit + 0.3, dur=4.4, gain_db=-17, fade_in=0.5, fade_out=0.8, pan=0.3)
    return sc
