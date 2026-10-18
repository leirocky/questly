"""Scene 3 (v2) — Jonah runs away to Joppa, pays the fare and boards a ship for Tarshish (Jonah 1:3).

One wide panorama, west = left, east = right, no cuts (adapted from the approved v1 scene; its drawing helpers
are imported from art.scenes_v1.s03_flee):

  * line 0 '可是，约拿不愿意去。' — a sunny crossroads on the coastal road. The signpost shows 他施 pointing left
    (west) and 尼尼微 pointing right (east). The scene opens on s02's last picture of Jonah (same place and size
    on screen, arms folded, frowning) and holds it through the dissolve before the camera eases over to the
    signpost; on '约拿不愿意去' he puts his palm out and shakes his head. '他转过身，' — he turns round (a hard cut
    to the mirrored drawing on a quick squash, whoosh); '朝着相反的方向跑走了。' — he runs west
    (8-drawing run cycle driven by the distance run, so the planted sole stays on the road; footfalls on the
    footsteps_run beats); the camera follows.
  * line 1 '约拿为什么不想去呢？故事的后面，我们就会知道。' — the narrator's aside to the children. Jonah stops under
    an olive tree to catch his breath, then turns to look back east along the road with his arms folded and a
    stubborn frown (he knows why he ran — see s19); on '为什么' the narrator's question card pops up in the
    eastern sky above the road (a round storybook card, NOT a thought bubble: no tail), a big '？' over a faint,
    hazy Nineveh skyline. On '我们就会知道' the card pops away and he turns and runs on.
  * line 2 '他一路跑到海边的约帕城，' — he runs on past the hill town of Joppa onto the quay and the wooden pier;
    the camera reveals the harbour, where a porter tosses a jar up to the sailor by the mast while the captain
    watches from the bow (the toss is timed from Jonah's run, so it is over before he reaches the porters); the
    other porter, carrying a crate at hip height, glances up in surprise as Jonah dashes past and, once Jonah is
    clear, sets it down on the pier.
    '找到一条要开往他施的船。' — he stops on the pier by the ship (the berth sign on a post on the pier reads 他施
    with a west arrow), looks up, points at it; the captain walks aft along the deck (behind the mast sailor)
    to meet him and nods.
    '他施在很远很远的西边。' — the bow sailor points far out to sea, the captain and Jonah look west, a gull flies
    off that way and the camera drifts out over the open sea to the far horizon (a distant sail).
  * line 3 '约拿付了船钱，' — the camera pushes in on the two hands: Jonah takes coins from his sash and holds them
    out on his open palm, a little below and aft of the captain's open palm (the hands never overlap); one by
    one three coins hop up out of his hand and drop down into the captain's palm (gold glint, coins sfx); the
    captain holds the full palm a moment, closes his fist on the coins (gold peeking out of it), brings it in to
    his chest through an in-between and nods; meanwhile Jonah lowers his arm through an in-between.
    '上了船，' — Jonah crouches and hops up over the rail onto the deck (whoosh, thud) while the camera eases back
    and up. '想要逃到远方，' — the ties come off the furled sail (a striped roll lashed under the yard) and in three
    pulls of the mast sailor on the halyard it unrolls down from the yard and fills with wind; the captain faces
    the sea, the bow sailor points the way and the ship leaves the pier westward (bow wave, foam), gathering way.
    '躲开上帝。' — Jonah glances back at the shore and ducks behind the stern rail by the cargo, peeking; the
    camera follows the departing ship, leans in a little on him as he glances back, pulls back as he ducks (the
    receding pier behind) while the ship slows to a gentle drift, and ends on s04's opening picture of the ship
    (there before the dissolve starts): same size and place, rocking in step with s04's ship. Through the closing
    dissolve the ship, crew, Jonah and the cargo on deck (s04's opening layout of it all through this scene: see
    deck_cargo_svg) stay put and only the background changes from the harbour to the open sea (the sun settles
    onto s04's sun; the distant ship of line 2 has sailed on over the horizon).

Pose changes are hard cuts hidden by a small hop / squash or an in-between (no crossfades between poses). The crew is
the s04-s09 crew: the captain, sailor variant 1 (by the mast) and variant 0 (at the bow), same props.ship
(furled -> full striped sail); the men on the pier are Joppa porters in plain tunics (v1 'dockhand'), so nobody
in crew costume stays ashore.
All times come from the narration chunks (``at()``), nothing is hard-coded to the voice take.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s03_flee as V
from art.scenes import s04_storm as S4
from art.scenes_v1 import s04_storm as V4
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 6400, 1188
PAINT_R = SW - 6          # right edge of the painted stage (the camera never goes past it)

K = 0.8                   # person / ship scale
GY = 910                  # walking line: road, quay and pier planks (Jonah's feet)
BACK_Y = 896              # feet of cargo standing on the quay
PIER_Y = GY + 4           # feet of the porters (soles overlap the plank band)

# --- harbour (v1 layout moved 480 px right, so there is more open sea to the west)
DX1 = 480
SHIP_X, SHIP_WL = 1520 + DX1, 968
DECK = SHIP_WL + PR.SHIP_DECK_Y * K
RAIL = SHIP_WL - 220 * K
PIER_X0, PIER_X1 = 1420 + DX1, 2200 + DX1
QUAY_X = 2190 + DX1
SEA_RIGHT = 2260 + DX1
HZ = 560                  # horizon

MAST_SAILOR_LX = 72       # sailor 1 by the mast: hauls the halyard when they sail
BOW_SAILOR_LX = 270       # sailor 0 at the bow: points the way out to sea
CAP_LX0 = 150             # the captain watches the loading from here, then walks aft ...
CAP_LX = -60              # ... to meet Jonah, just aft of the mast


def lx2x(lx):
    return PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, lx, PR.SHIP_DECK_Y)[0]


CAP_X = lx2x(CAP_LX)
CAP_X0 = lx2x(CAP_LX0)
P1X, P2X = 2640, 2480     # porters: P1 holds a crate, P2 swings a jar up to the ship

# --- the road (Jonah runs right -> left)
JSTOP = 4000              # where he stops for the aside
JX0 = 5443                # his spot at the crossroads
SIGN_X = JX0 + 220
STOP_OLIVE = (3858, 874)

# parallax: far layers are drawn where they belong when the camera is on the harbour (X_REF); they slide
# k * (cam.x - X_REF) with the camera (so things meant for the crossroads view sit ~0.25 * 3100 px further west
# in the far layer than where they are seen).
X_REF = 2150
K_FAR, K_TOWN, K_CLOUD, K_SUN = 0.25, 0.1, 0.55, 0.85

# s04 opens on a static wide shot of this ship at sea; this scene ends on exactly that picture of the ship
XF = 1.0                                  # the closing cross-dissolve (s04 starts at T - XF)
S4_CAM = (1268.0, 690.0, 2170.0)          # s04's opening camera (static through the dissolve)
S4_K = 1920 / S4_CAM[2]                   # output px per s04 stage px
S4_SUN = (1980.0, 250.0, 84.0)            # s04's sun: centre, radius (its calm sky drifts right 9 px/s)

SHIP_SEED = 211
COIN = "#e9b949"
COIN_R = 10.5             # coin radius (stage px)
PALM_OFF = (6, -9)        # where the coins rest on the captain's open hand (from C.hand_positions' hand point)
HAND_OFF = (-4, -10)      # ... and on Jonah's open hand
COIN_ARC = 40             # each coin rises ~60 px above Jonah's hand, then drops into the captain's palm


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


f1 = V.f1
ugrad = V.ugrad


def at(line, phrase):
    """Time (s) the narrator reaches ``phrase``: the start of its subtitle chunk plus its share of the chunk
    (by characters) — commas inside a chunk are not chunk boundaries, so this finds '上了船' in
    '约拿付了船钱，上了船，想要逃到远方，'."""
    for c in (line.chunks or []):
        i = c.text.find(phrase)
        if i >= 0:
            return c.start + (c.end - c.start) * i / max(1, len(c.text))
    i = line.text.find(phrase)
    if i < 0:
        raise KeyError(phrase)
    return line.start + (line.end - line.start) * i / max(1, len(line.text))


def trapezoid(t, t0, t1, D, ta, td):
    """Distance covered at time t by a move of length D from t0 to t1 (accelerate over ta, cruise, brake over
    td). Returns (distance, cruise speed)."""
    T = t1 - t0
    v = D / (T - ta / 2 - td / 2)
    tau = min(max(t - t0, 0.0), T)
    if tau < ta:
        return v * tau * tau / (2 * ta), v
    d = v * ta / 2
    if tau < T - td:
        return d + v * (tau - ta), v
    d += v * (T - td - ta)
    r = tau - (T - td)
    return d + v * r - v * r * r / (2 * td), v


def bump(t, t0, dur):
    """0 -> 1 -> 0 half-sine over [t0, t0 + dur]."""
    if t0 <= t < t0 + dur:
        return math.sin(math.pi * (t - t0) / dur)
    return 0.0


# ============================================================================ figures
# Scene-local poses, built on the library rig so the figures match the library exactly.
J_POSES = {
    # fetching coins from the sash (near hand at the sash knot, looking down at it)
    "pay_fetch": C._P(h=12, arms=(("fk", 10, 5), ("fk", -6, 62)), hands=("fist", "fist"), expr="neutral"),
    # holding the coins out to the captain on the ship (near arm forward, a little up, open hand; the hand stays
    # below and aft of the captain's palm so the two never overlap)
    "pay_give": C._P(t=-8, h=-14, legs=((10, 3), (-12, -6)), arms=(("fk", 12, 6), ("fk", 110, 120)),
                     hands=("fist", "open"), expr="neutral"),
    # the in-between as he lowers that arm again once the captain has the coins (the smile gone: now he is on his
    # way to Tarshish)
    "pay_lower": C._P(t=-4, h=-6, legs=((7, 2), (-8, -4)), arms=(("fk", 11, 5), ("fk", 56, 64)),
                      hands=("fist", "open"), expr="worried"),
    # looking back east along the road during the aside: arms folded, chin down, a stubborn frown (he knows why
    # he will not go; the reason comes out in s19)
    "stubborn": C._P(t=-3, h=10, arms=(("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
                     far_front=True, expr="angry"),
    # vaulting up over the rail (near hand reaching for it, knees tucked)
    "hop": C._P(t=8, h=-6, legs=((80, -6), (44, -50)), arms=(("fk", -46, -20), ("fk", -34, -8)),
                hands=("open", "open"), hem=0.7, tail=-80, expr="worried"),
}
CAP_POSES = {
    # near arm held straight out forward, open palm (above and ahead of Jonah's hand, in the clear, well in front
    # of his beard so the coins never land on his face)
    "receive": C._P(t=6, h=6, arms=(("fk", 10, 4), ("fk", 78, 82)), hands=("fist", "open"), expr="happy"),
    # pointing up and away to the far horizon ('very, very far to the west'), clear of the mast sailor's head
    "point_far": C._P(t=-4, h=-14, arms=(("fk", 10, 4), ("fk", 124, 132)), hands=("fist", "point"), expr="happy"),
    # his hand closes on the coins where it caught them (they peek out of the top of his fist) ...
    "grab": C._P(t=6, h=6, arms=(("fk", 10, 4), ("fk", 78, 82)), hands=("fist", "fist"), expr="happy"),
    # ... the in-between as he brings the fist in ...
    "take_mid": C._P(t=5, h=6, arms=(("fk", 10, 4), ("fk", 50, 106)), hands=("fist", "fist"), expr="happy"),
    # ... and the coins tucked away: fist at the chest
    "take": C._P(t=4, h=6, arms=(("fk", 10, 4), ("fk", 24, 128)), hands=("fist", "fist"), expr="happy"),
}


def jonah_fig(x, y, scale=1.0, facing=1, pose="stand", expr=None):
    if pose in J_POSES:
        ps = dict(J_POSES[pose])
        inner, _ = C._figure(C._jonah_design(), C._ADULT, ps, expr or ps["expr"], C._fsign(facing), True)
        return C._wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")
    return V.jonah_fig(x, y, scale, facing, pose=pose, expr=expr)


def captain_fig(x, y, scale=1.0, facing=1, pose="stand", expr=None):
    if pose in CAP_POSES:
        ps = dict(CAP_POSES[pose])
        inner, _ = C._figure(C._captain_design(), C._CAPTAIN_M, ps, expr or ps["expr"], C._fsign(facing), True)
        return C._wrap_out(inner, x, y, scale, facing, f"captain-{pose}")
    return C.captain(x, y, scale, facing, pose=pose, expr=expr)


def coin_svg(x, y, r=7.5, tilt=0.0):
    """A small gold coin seen a little from above (ellipse with rim, stamp and highlight)."""
    ry = r * (0.62 + 0.25 * abs(math.cos(math.radians(tilt))))
    return (f'<g transform="rotate({tilt:.1f} {x:.1f} {y:.1f})">'
            f'<ellipse cx="{x:.1f}" cy="{y + 1.6:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="{S.shade(COIN, -0.35)}" '
            f'stroke="{P["ink"]}" stroke-width="2"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="{COIN}" stroke="{P["ink"]}" '
            f'stroke-width="2"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 0.5:.1f}" ry="{ry * 0.5:.1f}" fill="none" '
            f'stroke="{S.shade(COIN, -0.3)}" stroke-width="1.4"/>'
            f'<ellipse cx="{x - r * 0.35:.1f}" cy="{y - ry * 0.35:.1f}" rx="{r * 0.28:.1f}" ry="{ry * 0.2:.1f}" '
            f'fill="#fff6d6"/></g>')


# ============================================================================ background


SUN, SUN_R = (2560, 285), 62


def sun_svg():
    x, y = SUN
    defs = S.rad_grad("s3sunglow", [(0, "#fffbe6", 0.95), (0.3, "#fff1bf", 0.6), (1, "#fff1bf", 0)])
    body = (f'<circle cx="{x}" cy="{y}" r="330" fill="url(#s3sunglow)"/>' +
            S.g(f'<circle cx="{x}" cy="{y}" r="{SUN_R}" fill="{P["sun"]}" '
                f'stroke="{S.mix(P["sun_hot"], P["ink"], 0.2)}" stroke-width="3.5"/>'
                f'<circle cx="{x - 18}" cy="{y - 20}" r="22" fill="#fff3c4" opacity="0.7"/>', filter="wobble"))
    return doc(body, defs)


def clouds_svg():
    items = [(520, 250, 260, 85, 7), (1150, 190, 330, 105, 1), (1700, 330, 210, 70, 2), (2200, 150, 300, 95, 3),
             (2850, 230, 360, 115, 4), (3420, 125, 240, 80, 5), (3900, 300, 320, 100, 6), (4400, 180, 280, 92, 8),
             (4950, 290, 230, 76, 9)]
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, "#fffaf0", seed=seed, sw=3, shade_fill="#dbe9ee")
    return doc(S.g(body, filter="wobble"))


SEA_FAR_R = 3420          # the far sea ends behind the eastern hills


def far_svg(far_ship=True):
    """Open sea to the horizon (with a distant ship and the rocks off Joppa), the cape and the hazy hills to the
    east, the green hills with a grove and grazing sheep behind the road. ``far_ship=False``: the distant ship has
    sailed on over the horizon."""
    hz = HZ
    defs = (ugrad("s3farsea", 0, hz, 0, SH, [(0, S.mix(P["sea_pale"], "#eef6ee", 0.35)), (0.22, P["sea_pale"]),
                                             (0.6, P["sea_light"]), (1, S.mix(P["sea_light"], P["sea"], 0.5))]) +
            ugrad("s3hill1", 0, 420, 0, 700, [(0, S.mix(P["olive"], P["sky_day"], 0.62)),
                                               (1, S.mix(P["olive"], P["sky_day"], 0.45))]) +
            ugrad("s3hill2", 0, 560, 0, 900, [(0, S.mix(P["grass"], P["sky_day"], 0.32)),
                                               (1, S.mix(P["grass"], P["sand"], 0.35))]))
    # the sky is a purely vertical gradient, so it rides on this parallax layer (saves a full-frame layer)
    defs += ugrad("s3sky", 0, 0, 0, 760, [(0, "#7fc0dc"), (0.45, P["sky_day"]),
                                          (0.85, S.mix(P["sky_day"], "#fff6dc", 0.55)), (1, "#fbf1d6")])
    sea_w = SEA_FAR_R + 20
    body = f'<rect x="-1200" y="-20" width="{SW + 2400}" height="{SH + 40}" fill="url(#s3sky)"/>'
    body += f'<rect x="-20" y="{hz}" width="{sea_w}" height="{SH - hz + 40}" fill="url(#s3farsea)"/>'
    body += (f'<path d="M-20,{hz} L{SEA_FAR_R},{hz}" stroke="{P["ink"]}" stroke-width="2.2" opacity="0.5"/>'
             f'<rect x="-20" y="{hz - 30}" width="{sea_w}" height="40" fill="#fbf4dc" opacity="0.35" '
             f'filter="url(#soft)"/>')
    rng = random.Random(3)
    for i in range(90):                                  # sun glitter streaks
        x = rng.uniform(0, SEA_FAR_R - 150)
        y = hz + 12 + (rng.random() ** 1.6) * 280
        w = rng.uniform(16, 44) * (0.6 + (y - hz) / 300)
        body += (f'<path d="M{f1(x)},{f1(y)} l{f1(w)},0" stroke="#fbfdf6" stroke-width="2.6" '
                 f'stroke-linecap="round" opacity="{rng.uniform(0.35, 0.7):.2f}"/>')
    # a distant ship far out to the west (its hull below the waterline painted over with sea)
    for x, y, s, f in ((1300, 594, 0.07, -1),) if far_ship else ():   # seen on '很远很远的西边'
        body += PR.ship(x, y, s, f, sail="full", lantern=False)
        body += f'<rect x="{x - 70}" y="{y}" width="140" height="16" fill="url(#s3farsea)"/>'
    # the rocks off Joppa
    rocks = ""
    rock_c = S.mix(P["stone_dark"], P["sky_day"], 0.3)
    for x, base, w, h in ((640, 668, 120, 92), (730, 672, 80, 56), (565, 674, 60, 34), (810, 676, 44, 24)):
        pk = [(x - w / 2, base), (x - w * 0.36, base - h * 0.55), (x - w * 0.14, base - h * 0.82),
              (x + w * 0.04, base - h), (x + w * 0.22, base - h * 0.7), (x + w * 0.4, base - h * 0.45),
              (x + w / 2, base)]
        d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pk) + " Z"
        rocks += S.path(d, fill=rock_c, sw=2.8)
        rocks += (f'<path d="M{f1(x + w * 0.04)},{f1(base - h)} L{f1(x + w * 0.22)},{f1(base - h * 0.7)} '
                  f'L{f1(x + w * 0.4)},{f1(base - h * 0.45)} L{f1(x + w / 2)},{f1(base)} L{f1(x + w * 0.08)},'
                  f'{f1(base)} Z" fill="{S.shade(rock_c, -0.18)}" opacity="0.6"/>')
    rocks += (f'<path d="M540,676 q40,-9 80,0 t80,0 t80,0 t60,0" stroke="{P["foam"]}" stroke-width="5" '
              f'fill="none" stroke-linecap="round" opacity="0.85"/>')
    body += S.g(rocks, filter="wobble")
    # far hills to the east (toward Nineveh): a cape tapering into the sea on the west, then hills to the end
    rh = random.Random(11)
    n = 26
    hp = [(2480 + (SW + 60 - 2480) * i / n,
           600 - 150 * abs(math.sin(math.pi * i / 6.5)) * rh.uniform(0.75, 1.1)) for i in range(1, n)]
    top = [(2070, 614), (2200, 605), (2340, 596), (2480, 590)] + hp + [(SW + 60, 600)]
    far_d = (S.smooth_path(top, closed=False) + f" L{SW + 60},900 L2810,900 C2640,800 2400,694 2140,628 "
             "Q2095,620 2070,614 Z")
    far_hills = S.path(far_d, fill="url(#s3hill1)", sw=2.5)
    far_hills += (f'<path d="M2065,618 Q2120,626 2180,640 C2380,690 2530,740 2640,790" stroke="{P["foam"]}" '
                  f'stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>')
    body += S.g(far_hills, filter="wobble")
    ridge = _ridge_fn(top)
    trees = ""
    rt = random.Random(5)
    for i, x in enumerate(list(range(3000, SW, 210))):
        if rt.random() < 0.72:
            xx = x + rt.uniform(-40, 40)
            trees += V.tree(xx, ridge(xx) + rt.uniform(18, 46), rt.uniform(0.24, 0.32), seed=i, haze=0.45)
    body += S.g(trees, filter="wobble-fine")
    # the green hills behind the road (they start east of the town and run to the crossroads)
    hA, hB = (3330, 4560, 880, 250, 4, 3), (4400, SW + 60, 880, 300, 6, 4)
    near = ""
    grove = ""
    for (x0, x1, y, pk, sd, bm) in (hA, hB):
        near += S.path(S.hill(x0, x1, y, pk, seed=sd, bottom=1000, bumps=bm), fill="url(#s3hill2)", sw=3)
    rA, rB = _ridge_fn(_hill_pts(*hA)), _ridge_fn(_hill_pts(*hB))
    # terraces / field edges following the slopes of the near hills
    rterr = random.Random(9)
    terr = ""
    for (x0, x1, r) in ((3420, 4480, rA), (4520, SW, rB)):
        for off in (46, 92, 140):
            xa = x0 + rterr.uniform(20, 120)
            while xa < x1 - 200:
                xb = min(x1 - 60, xa + rterr.uniform(260, 520))
                pts = [(x, r(x) + off + 6 * math.sin(x / 90.0)) for x in np.linspace(xa, xb, 9)]
                if all(y < 868 for _, y in pts):
                    terr += (f'<path d="{S.smooth_path(pts, closed=False)}" stroke="{S.shade(P["grass"], -0.25)}" '
                             f'stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.5"/>')
                xa = xb + rterr.uniform(80, 220)
    near += terr
    # (no village on the far hills: seen above the signpost's 尼尼微 arrow it read as Nineveh, which is a huge
    # walled city far out of sight from here)
    for i, (x, dy, sc) in enumerate(((3520, 46, 0.56), (3580, 52, 0.46), (3800, 30, 0.55), (4160, 60, 0.5),
                                     (4430, 50, 0.58), (4492, 58, 0.46), (4990, 36, 0.6), (5230, 30, 0.52),
                                     (5600, 40, 0.6), (5670, 50, 0.48), (5960, 56, 0.58), (6140, 46, 0.5))):
        r = rA if x < 4480 else rB
        grove += V.tree(x, r(x) + dy, sc, seed=i + 10, haze=0.12)
    # sheep grazing on the slopes (seen behind Jonah at the crossroads and during the aside)
    for x, dy, f in ((4300, 70, 1), (4356, 64, -1), (3700, 84, -1), (5850, 80, 1)):
        r = rA if x < 4400 else rB
        grove += PR.animal(x, r(x) + dy, 0.2, f, kind="sheep")
    body += S.g(near, filter="wobble") + S.g(grove, filter="wobble-fine")
    return doc(body, defs)


def _hill_pts(x0, x1, y, peak, seed=0, bumps=3):
    """The points S.hill() puts its smooth top through (same random sequence)."""
    r = random.Random(seed)
    pts = [(x0, y)]
    for i in range(1, bumps * 2):
        u = i / (bumps * 2)
        pts.append((x0 + (x1 - x0) * u, y - peak * math.sin(math.pi * u) * r.uniform(0.75, 1.1)))
    pts.append((x1, y))
    return pts


def _ridge_fn(pts):
    xs = np.array([p[0] for p in pts], float)
    ys = np.array([p[1] for p in pts], float)
    return lambda x: float(np.interp(x, xs, ys))


def town_svg():
    """Joppa: a hill town above the harbour (v1, moved), stone walls, flat-roofed houses, palms."""
    o = DX1
    defs = (ugrad("s3hill", 0, 520, 0, 900, [(0, S.mix(P["grass"], P["sand_light"], 0.45)),
                                               (0.55, S.mix(P["sand"], P["grass"], 0.3)), (1, P["sand"])]) +
            f'<filter id="s3hazef" x="-2%" y="-2%" width="104%" height="104%">'
            f'<feFlood flood-color="{S.mix(P["sky_day"], "#fff6e0", 0.3)}" flood-opacity="0.26" result="f"/>'
            f'<feComposite in="f" in2="SourceGraphic" operator="in" result="h"/>'
            f'<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="h"/></feMerge></filter>')
    hill_pts = [(1660, 880), (1730, 846), (1850, 770), (1990, 672), (2160, 588), (2360, 545), (2560, 548),
                (2760, 590), (2950, 660), (3120, 735), (3300, 800), (3420, 830)]
    hill_pts = [(x + o, y) for x, y in hill_pts]
    hd = S.smooth_path(hill_pts, closed=False) + f" L{3420 + o},1000 L{1660 + o},1000 Z"
    town = S.g(S.path(hd, fill="url(#s3hill)", sw=3.2), filter="wobble")
    rows = (((2180, 612, 2, 0.17, 1), (2280, 578, 0, 0.18, -1), (2385, 566, 3, 0.17, 1), (2490, 566, 1, 0.16, 1),
             (2590, 574, 0, 0.17, -1), (2690, 596, 2, 0.16, 1), (2790, 626, 3, 0.16, -1)),
            ((2070, 662, 0, 0.19, 1), (2170, 650, 3, 0.2, -1), (2300, 636, 1, 0.19, 1), (2420, 632, 2, 0.2, -1),
             (2545, 636, 3, 0.19, 1), (2660, 648, 0, 0.2, -1), (2780, 668, 1, 0.18, 1), (2890, 696, 0, 0.18, -1)))
    for row in rows:
        for x, y, v, sc, f in row:
            town += PR.house(x + o, y, sc, v, f)
    town += PR.palm_tree(2236 + o, 664, 0.22) + PR.palm_tree(2604 + o, 650, 0.2, lean=-0.2)
    town += PR.palm_tree(2360 + o, 668, 0.24, lean=0.2) + PR.palm_tree(2840 + o, 690, 0.2, lean=0.1)

    def wtop(x):
        return 676 + 0.00012 * (x - 2420 - o) ** 2

    town += S.g(V.stone_wall(1930 + o, 2980 + o, wtop, 70, 7, towers=((1958 + o, 54, 46), (2250 + o, 58, 52),
                                                                      (2600 + o, 58, 52), (2960 + o, 50, 42)),
                             gate=(2430 + o, 50), uid="town"), filter="wobble-fine")
    town += S.g(f'<g transform="translate({o},0)"><rect x="2452" y="470" width="56" height="96" '
                f'fill="{P["stone_light"]}" stroke="{P["ink"]}" stroke-width="3"/><rect x="2446" y="458" width="68" '
                f'height="16" fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="3"/><path d="M2480,458 L2480,410" '
                f'stroke="{P["wood_dark"]}" stroke-width="4"/><path d="M2480,412 q22,6 40,0 q-12,10 0,20 q-20,-6 '
                f'-40,0 Z" fill="{P["terracotta"]}" stroke="{P["ink"]}" stroke-width="2.4"/>'
                f'<rect x="2472" y="494" width="12" height="22" rx="6" fill="{S.mix(P["wood_dark"], P["ink"], 0.4)}"/>'
                f'</g>', filter="wobble-fine")
    for x, y, v, sc, f in ((2235, 836, 2, 0.24, 1), (2350, 826, 0, 0.25, -1), (2475, 820, 3, 0.23, 1),
                           (2600, 818, 1, 0.22, -1), (2725, 824, 2, 0.22, 1), (2850, 836, 0, 0.21, -1)):
        town += PR.house(x + o, y, sc, v, f)
    town += PR.palm_tree(2300 + o, 840, 0.3, lean=-0.25) + PR.palm_tree(2790 + o, 840, 0.28, lean=0.2)
    town += S.g(V.olive(3080 + o, 760, 0.62, seed=2) + V.olive(1990 + o, 742, 0.5, seed=5), filter="wobble-fine")
    body = f'<g filter="url(#s3hazef)">{town}</g>'
    rocks = ""
    for i, (x, y, rx, ry) in enumerate(((1742, 848, 44, 24), (1800, 830, 50, 28), (1862, 840, 38, 22),
                                         (1690, 866, 34, 18))):
        rocks += S.path(S.blob(x + o, y, rx, ry, 0.15, 8, seed=i), fill=S.mix(P["stone"], P["stone_dark"], 0.3), sw=3)
    body += S.g(rocks, filter="wobble")
    return doc(body, defs)


HW_TOP = 775


def harbour_back_svg():
    """Harbour sea wall along the back of the basin, mooring rings, a moored fishing boat (v1, moved)."""
    o = DX1
    out = ""
    out += S.g(V.stone_wall(1872 + o, 2345 + o, lambda x: float(HW_TOP), 110, 3, uid="quay", merlons=False),
               filter="wobble-fine")
    out += S.g(f'<g transform="translate({o},0)"><rect x="1866" y="{HW_TOP - 9}" width="482" height="13" rx="4" '
               f'fill="{P["stone"]}" stroke="{P["ink"]}" stroke-width="2.8"/>'
               f'<path d="M1852,{HW_TOP + 70} L1852,{HW_TOP - 18} Q1872,{HW_TOP - 30} 1892,{HW_TOP - 18} '
               f'L1892,{HW_TOP + 70} Z" fill="{S.mix(P["stone_light"], P["stone"], 0.5)}" stroke="{P["ink"]}" '
               f'stroke-width="3"/>'
               f'<rect x="1878" y="{HW_TOP - 24}" width="12" height="90" fill="{P["stone_dark"]}" opacity="0.3"/>'
               f'</g>', filter="wobble-fine")
    rings = ""
    for x in (1960 + o, 2120 + o, 2250 + o):
        rings += (f'<rect x="{x - 6}" y="{HW_TOP + 14}" width="12" height="9" rx="2" fill="{P["wood_dark"]}"/>'
                  f'<circle cx="{x}" cy="{HW_TOP + 29}" r="8" fill="none" stroke="{P["ink"]}" stroke-width="2.8"/>')
    out += S.g(rings, filter="wobble-fine")
    by = 818
    out += S.g(f'<g transform="translate({o},0)">'
               f'<path d="M1985,{by} Q2040,{by + 40} 2110,{by} L2104,{by - 12} L1992,{by - 12} Z" '
               f'fill="{P["wood_light"]}" stroke="{P["ink"]}" stroke-width="3"/>'
               f'<path d="M1992,{by - 12} L2104,{by - 12}" stroke="{P["jonah_sash"]}" stroke-width="4"/>'
               f'<path d="M2048,{by - 12} L2048,{by - 70}" stroke="{P["wood_dark"]}" stroke-width="3.5"/>'
               f'<path d="M2048,{by - 66} L2080,{by - 24} L2048,{by - 24} Z" fill="{P["sail"]}" '
               f'stroke="{P["ink"]}" stroke-width="2.4"/>'
               f'<path d="M1990,{by - 8} Q1975,{by - 2} 1966,{HW_TOP + 36}" stroke="{P["sackcloth_dark"]}" '
               f'stroke-width="2.6" fill="none"/></g>', filter="wobble-fine")
    return doc(out)


def harbour_corner_svg():
    """Stone corner block where the harbour wall meets the quay, steps down to the water (v1, moved)."""
    x0, x1, top = 2228 + DX1, 2345 + DX1, 784
    out = S.g(V.stone_wall(x0, x1, lambda x: float(top), 112, 13, uid="corner", merlons=False), filter="wobble-fine")
    steps = ""
    for i, (sx, sy) in enumerate(((x0 - 18, top + 14), (x0 - 34, top + 28), (x0 - 48, top + 42))):
        steps += (f'<rect x="{sx}" y="{sy}" width="{x0 - sx + 4}" height="{896 - sy}" '
                  f'fill="{S.mix(P["stone_light"], P["stone"], 0.25 + 0.2 * i)}" stroke="{P["ink"]}" '
                  f'stroke-width="2.6"/>')
    out += S.g(steps, filter="wobble-fine")
    bx = 2300 + DX1
    out += S.g(f'<rect x="{x0 - 6}" y="{top - 8}" width="{x1 - x0 + 12}" height="12" rx="4" fill="{P["stone"]}" '
               f'stroke="{P["ink"]}" stroke-width="2.8"/>'
               f'<rect x="{bx}" y="{top - 46}" width="24" height="42" rx="8" fill="{P["wood_dark"]}" '
               f'stroke="{P["ink"]}" stroke-width="3"/>'
               f'<ellipse cx="{bx + 12}" cy="{top - 46}" rx="14" ry="6" fill="{P["wood"]}" stroke="{P["ink"]}" '
               f'stroke-width="2.8"/>', filter="wobble-fine")
    out += S.g(f'<path d="M{x0 - 62},830 q12,-6 24,0 t24,0 t20,0" stroke="{P["foam"]}" stroke-width="5" '
               f'fill="none" stroke-linecap="round" opacity="0.9"/>', filter="wobble-fine")
    return doc(out)


def sea_band_svg(y, amp, wl, phase, c_top, c_bot, foam_y, seed, foam_x=(), foam_op=0.75, x1=SEA_RIGHT, sw=3.0,
                 line=0.55, ticks=40):
    gid = f"s3sea{seed}"
    defs = ugrad(gid, 0, y - amp, 0, min(SH, y + 260), [(0, c_top), (1, c_bot)])
    edge = S.mix(P["ink"], c_top, 1 - line)
    body = (f'<path d="{S.wave_band(y, amp, wl, phase, x0=-140, x1=x1, bottom=SH + 60)}" fill="url(#{gid})" '
            f'stroke="{edge}" stroke-width="{sw}" stroke-linejoin="round"/>')
    for fx0, fx1, dy in foam_x:
        body += S.path(S.wave_line(y + foam_y + dy, amp * 0.8, wl, phase, x0=fx0, x1=fx1), stroke=False,
                       extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="{foam_op}"')
    rng = random.Random(seed)
    for i in range(ticks):
        tx = rng.uniform(-40, x1 - 60)
        ty = y + rng.uniform(26, 210)
        w = rng.uniform(22, 46)
        body += (f'<path d="M{f1(tx)},{f1(ty)} q{f1(w / 2)},{f1(-w * 0.32)} {f1(w)},0" stroke="{P["foam"]}" '
                 f'stroke-width="3.2" fill="none" stroke-linecap="round" opacity="{rng.uniform(0.45, 0.8):.2f}"/>')
    return doc(S.g(body, filter="wobble"), defs)


def glints_svg(x0, x1, y0, y1, n, seed):
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        k = 0.75 + 0.5 * (y - y0) / max(1.0, y1 - y0)
        w = rng.uniform(10, 24) * k
        out += (f'<path d="M{f1(x - w / 2)},{f1(y)} l{f1(w)},0" stroke="#fffbea" stroke-width="{2.4 * k:.1f}" '
                f'stroke-linecap="round" opacity="{rng.uniform(0.65, 0.95):.2f}"/>')
        if rng.random() < 0.2:
            s = rng.uniform(4, 6) * k
            out += (f'<path d="M{f1(x)},{f1(y - s)} L{f1(x)},{f1(y + s)} M{f1(x - s * 0.8)},{f1(y)} '
                    f'L{f1(x + s * 0.8)},{f1(y)}" stroke="#fffbea" stroke-width="1.6" stroke-linecap="round" '
                    f'opacity="0.85"/>')
    return doc(out)


BERTH = (2286, 788, 140, 52)   # the berth sign's board (x, y, w, h): on the pier between Jonah's spot and the
#                               porters, high enough to read above the subtitles in the close shots of the fare
#                               and the sail, and east of where the departing ship ends up (so it never crosses
#                               the ship in the closing dissolve)


def berth_board():
    """A painted board on a post at the ship's berth on the pier: '他施' with an arrow pointing west."""
    x, y, w, h = BERTH
    px = x + w - 30                # the post, standing on the planks
    body = (f'<path d="M{px - 7},{GY + 8} L{px - 7},{y - 10} Q{px},{y - 20} {px + 7},{y - 10} L{px + 7},{GY + 8} Z" '
            f'fill="{P["wood"]}" stroke="{P["ink"]}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M{px - 2},{y + h + 6} L{px - 2},{GY + 2}" stroke="{P["wood_dark"]}" stroke-width="2.2" '
            f'opacity="0.6"/>'
            f'<ellipse cx="{px}" cy="{GY + 8}" rx="16" ry="4" fill="{P["ink"]}" opacity="0.2"/>'
            f'<path d="M{x},{y + h / 2} L{x + 26},{y} L{x + w},{y} L{x + w},{y + h} L{x + 26},{y + h} Z" '
            f'fill="{P["wood_light"]}" stroke="{P["ink"]}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M{x + 30},{y + h * 0.78} L{x + w - 8},{y + h * 0.78}" stroke="{P["wood"]}" stroke-width="2" '
            f'opacity="0.6"/>'
            f'<circle cx="{px}" cy="{y + 9}" r="3" fill="{P["wood_dark"]}"/>'
            f'<circle cx="{px}" cy="{y + h - 9}" r="3" fill="{P["wood_dark"]}"/>')
    body = S.g(body, filter="wobble-fine")
    body += S.text(x + 26 + (w - 26) / 2 - 16, y + h - 13, "他施", size=34, fill=P["ink"])
    return body


def land_svg():
    """Quay, the long coastal road, the olive tree where Jonah stops, the crossroads with the signpost, grassy
    verge, the pier with cargo."""
    defs = (ugrad("s3ground", 0, 840, 0, 1188, [(0, S.mix(P["grass"], P["leaf_light"], 0.3)), (0.35, P["grass"]),
                                                  (1, S.mix(P["grass"], P["grass_dark"], 0.6))]) +
            ugrad("s3road", 0, 878, 0, 950, [(0, P["sand_light"]), (1, S.mix(P["sand"], P["sand_light"], 0.4))]))
    R = SW + 40
    out = ""
    gpts = [(QUAY_X - 10, 892), (2900, 868), (3300, 858), (3800, 860), (4300, 854), (4800, 852), (5300, 856),
            (5800, 850), (R, 852)]
    gd = S.smooth_path(gpts, closed=False) + f" L{R},{SH + 40} L{QUAY_X - 10},{SH + 40} Z"
    out += S.g(S.path(gd, fill="url(#s3ground)", sw=3.5), filter="wobble")
    out += V._grass_strokes(QUAY_X + 230, R, 856, 880, 230, 5, P["grass_dark"], 0.5)
    rd = (f"M{QUAY_X - 10},884 C3100,878 3700,882 4300,880 C4900,879 5500,882 {R},880 "
          f"L{R},948 C5500,952 4500,950 3500,948 L{QUAY_X - 10},946 Z")
    out += S.g(S.path(rd, fill="url(#s3road)", sw=3), filter="wobble")
    rng = random.Random(21)
    for i in range(260):
        x = rng.uniform(QUAY_X + 20, R - 40)
        y = rng.uniform(890, 942)
        r = rng.uniform(2, 5)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(r * 1.6)}" ry="{f1(r)}" fill="{P["sand_dark"]}" '
                f'opacity="0.5"/>')
    out += (f'<path d="M{QUAY_X + 420},934 C3600,929 4600,935 {R},931" stroke="{P["sand_dark"]}" '
            f'stroke-width="2.4" fill="none" opacity="0.4"/>')
    # stone paving on the quay
    out += (f'<path d="M{QUAY_X - 10},884 L{QUAY_X + 380},879 L{QUAY_X + 392},947 L{QUAY_X - 10},946 Z" '
            f'fill="{P["stone_light"]}" stroke="{P["ink"]}" stroke-width="3"/>')
    for i in range(9):
        x = QUAY_X + 20 + i * 44
        out += f'<path d="M{x},884 L{x - 6},946" stroke="{P["stone_dark"]}" stroke-width="2" opacity="0.6"/>'
    out += (f'<path d="M{QUAY_X - 6},915 L{QUAY_X + 386},913" stroke="{P["stone_dark"]}" stroke-width="2" '
            f'opacity="0.5"/>')
    out += S.g(V.stone_wall(QUAY_X - 10, QUAY_X + 300, lambda x: 946.0, 260, 9, uid="front", merlons=False),
               filter="wobble-fine")
    bank = (f"M{QUAY_X + 290},946 C{QUAY_X + 330},990 {QUAY_X + 340},1060 {QUAY_X + 330},{SH + 40} "
            f"L{R},{SH + 40} L{R},946 Z")
    out += S.g(S.path(bank, fill="url(#s3ground)", sw=3), filter="wobble")
    stones = ""
    rng = random.Random(33)
    x = QUAY_X + 420
    while x < R:
        w = rng.uniform(34, 56)
        h = rng.uniform(20, 28)
        stones += S.path(S.blob(x + w / 2, 960, w / 2, h / 2, 0.12, 7, seed=int(x)),
                         fill=S.mix(P["stone"], P["stone_light"], rng.uniform(0, 0.6)), sw=2.6)
        x += w + rng.uniform(-6, 2)
    out += S.g(stones, filter="wobble-fine")
    out += V._grass_strokes(QUAY_X + 360, R, 990, 1180, 640, 7, P["grass_dark"], 0.5)
    out += V._grass_strokes(QUAY_X + 360, R, 980, 1150, 220, 8, S.mix(P["leaf_light"], "#fffaf0", 0.2), 0.6)
    out += V._flowers(QUAY_X + 400, R, 1000, 1170, 170, 9)
    # trees and bushes along the road (olives without their dark olives: they read as faces)
    out += V.no_olive_dots(PR.olive_tree(3350, 872, 0.62, seed=4))
    out += V.no_olive_dots(PR.olive_tree(*STOP_OLIVE, 0.78, seed=7))           # Jonah stops in its shade
    out += V.no_olive_dots(PR.olive_tree(4720, 870, 0.58, seed=2))
    out += PR.bush(3040, 874, 0.5, 3) + PR.bush(3560, 874, 0.55, 1) + PR.bush(4200, 872, 0.5, 0)
    out += PR.bush(4560, 872, 0.55, 3) + PR.bush(5163, 874, 0.55, 1) + PR.bush(5883, 870, 0.55, 0)
    out += PR.bush(6260, 872, 0.5, 3)
    out += PR.signpost(SIGN_X, 898, 1.0)
    for x, v in ((3180, 0), (3470, 2), (3740, 0), (4060, 2), (4380, 0), (4650, 2), (4950, 0), (5250, 2),
                 (5420, 0), (5560, 2), (5783, 0), (6000, 1), (6200, 0), (6340, 2)):
        out += PR.grass_tuft(x, 880, 0.6, v)
    # a milestone by the olive tree
    out += S.g(f'<path d="M{STOP_OLIVE[0] + 200},888 L{STOP_OLIVE[0] + 202},846 Q{STOP_OLIVE[0] + 218},828 '
               f'{STOP_OLIVE[0] + 234},846 L{STOP_OLIVE[0] + 236},888 Z" fill="{P["stone_light"]}" stroke="{P["ink"]}" '
               f'stroke-width="3"/><path d="M{STOP_OLIVE[0] + 208},866 l20,0" stroke="{P["stone_dark"]}" '
               f'stroke-width="2.4"/>', filter="wobble-fine")
    # the pier, with the berth board of the ship for Tarshish on its front beam
    out += PR.harbor_dock(PIER_X0, PIER_X1, GY, depth=230, scale=K)
    out += berth_board()
    # cargo waiting on the quay
    o = DX1
    out += (PR.crate(2390 + o, BACK_Y - 44, 0.62) + PR.crate(2445 + o, BACK_Y - 44, 0.62)
            + PR.crate(2417 + o, BACK_Y - 108, 0.58) + PR.jar(2238 + o, BACK_Y - 52, 0.55)
            + PR.jar(2272 + o, BACK_Y - 46, 0.48, rot=8)
            + PR.sack(2505 + o, BACK_Y - 2, 0.55, seed=2) + PR.sack(2548 + o, BACK_Y, 0.48, seed=5))
    out += PR.rope_coil(1520 + o, BACK_Y + 8, 0.6)
    out += (f'<g filter="url(#wobble-fine)"><rect x="{2606 + o}" y="842" width="30" height="52" rx="10" '
            f'fill="{P["wood_dark"]}" stroke="{P["ink"]}" stroke-width="3.2"/>'
            f'<ellipse cx="{2621 + o}" cy="844" rx="17" ry="7" fill="{P["wood"]}" stroke="{P["ink"]}" '
            f'stroke-width="3"/></g>')
    out += PR.gull(2622 + o, 805, 0.55, -1, pose="stand")
    return doc(out, defs)


def foreground_svg():
    out = ""
    out += S.g(S.path(S.blob(QUAY_X + 20, 1150, 130, 74, 0.12, 9, seed=8),
                      fill=S.mix(P["stone"], P["stone_dark"], 0.35), sw=4) +
               S.path(S.blob(QUAY_X + 150, 1176, 110, 56, 0.12, 9, seed=9), fill=P["stone"], sw=4), filter="wobble")
    out += PR.reeds(QUAY_X - 60, 1140, 0.7, 0) + PR.reeds(QUAY_X + 230, 1192, 0.6, 1)
    rng = random.Random(44)
    x = QUAY_X + 520
    while x < SW + 40:
        out += PR.grass_tuft(x, 1192, rng.uniform(0.9, 1.1), rng.choice((0, 2, 2)))
        x += rng.uniform(170, 230)
    for bx, sd in ((3500, 3), (4520, 4), (5480, 5), (6150, 6)):
        out += S.g(S.path(S.blob(bx, 1180, 120, 56, 0.15, 9, seed=sd), fill=S.mix(P["stone"], P["sand"], 0.3), sw=4),
                   filter="wobble")
    out += PR.bush(4080, 1196, 0.9, 3) + PR.bush(5960, 1196, 0.9, 1)
    return doc(out)


# ============================================================================ ship group


def ship_svg(part, sail):
    return doc(PR.ship(SHIP_X, SHIP_WL, K, -1, sail=sail, part=part, lantern=True))


def ship_back_bare_svg():
    """ship(part='back') with just the bare yard where the library draws its furled sail: in this scene the
    furled sail is the sail_roll layer, the same drawing that later drops open (one sail, one drawing)."""
    svg = PR.ship(SHIP_X, SHIP_WL, K, -1, sail="furled", part="back", lantern=True)
    bundle = PR._sail("furled", None)
    yard = PR._tube("M-318,-848 Q-10,-866 298,-848", 14, P["wood"])
    assert bundle.startswith(yard) and svg.count(bundle) == 1, "props.ship's furled sail has changed"
    return doc(svg.replace(bundle, yard))


def gaskets_svg():
    """The rope ties that hold the furled sail roll up under the yard (cast off when the sail is set); the
    library's tie positions, in local ship coordinates."""
    cy, r = V.ROLL_CY, V.ROLL_R
    rope = S.mix(P["sackcloth"], P["wood_light"], 0.4)
    body = ""
    for x in (-210, -60, 90, 220):
        body += (f'<rect x="{x - 6}" y="-854" width="12" height="{cy + r + 5 + 854}" rx="5" fill="{rope}" '
                 f'stroke="{P["ink"]}" stroke-width="3"/>'
                 f'<path d="M{x - 6},{cy - 4} L{x + 6},{cy + 2}" stroke="{S.shade(rope, -0.35)}" stroke-width="2"/>')
    return doc(ship_place(body))


def sail_band_svg():
    pts = " ".join(f"{f1(SHIP_X - x * K)},{f1(SHIP_WL + y * K)}" for x, y in V.SAIL_CLIP_LOCAL)
    clip = f'<clipPath id="s3sailband"><polygon points="{pts}"/></clipPath>'
    return doc(f'<g clip-path="url(#s3sailband)">{PR.ship(SHIP_X, SHIP_WL, K, -1, sail="full", part="back")}</g>',
               clip)


def ship_place(body):
    return (f'<g filter="url(#wobble-fine)"><g transform="translate({SHIP_X},{SHIP_WL}) scale({-K},{K})">'
            f'{body}</g></g>')


def sail_roll_svg():
    cx, cy, hw, r = -10, V.ROLL_CY, V.ROLL_W / 2, V.ROLL_R
    shape = f"M{cx - hw + r},{cy - r} L{cx + hw - r},{cy - r} A{r},{r} 0 0 1 {cx + hw - r},{cy + r} " \
            f"L{cx - hw + r},{cy + r} A{r},{r} 0 0 1 {cx - hw + r},{cy - r} Z"
    inner = ""
    for u0, u1 in ((1 / 7, 2 / 7), (3 / 7, 4 / 7), (5 / 7, 6 / 7)):
        a, b = cx - hw + V.ROLL_W * u0, cx - hw + V.ROLL_W * u1
        inner += f'<rect x="{f1(a)}" y="{cy - r - 2}" width="{f1(b - a)}" height="{2 * r + 4}" fill="{P["sail_stripe"]}"/>'
    inner += (f'<rect x="{cx - hw}" y="{cy + r * 0.25}" width="{V.ROLL_W}" height="{r}" '
              f'fill="{S.shade(P["sail"], -0.35)}" opacity="0.45"/>'
              f'<rect x="{cx - hw}" y="{cy - r * 0.7}" width="{V.ROLL_W}" height="{r * 0.45}" fill="#fffaf0" '
              f'opacity="0.35"/>')
    for i in range(1, 9):
        x = cx - hw + V.ROLL_W * i / 9
        inner += (f'<path d="M{f1(x - 8)},{cy - r + 2} Q{f1(x + 2)},{cy} {f1(x - 6)},{cy + r - 2}" '
                  f'stroke="{S.shade(P["sail"], -0.4)}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    body = (f'<path d="{shape}" fill="{P["sail"]}"/>'
            f'<clipPath id="s3rollc"><path d="{shape}"/></clipPath><g clip-path="url(#s3rollc)">{inner}</g>'
            f'<path d="{shape}" fill="none" stroke="{P["ink"]}" stroke-width="4.5" stroke-linejoin="round"/>')
    for ex in (cx - hw + r * 0.7, cx + hw - r * 0.7):
        body += (f'<ellipse cx="{f1(ex)}" cy="{cy}" rx="7" ry="{r - 3}" fill="{S.shade(P["sail"], -0.15)}" '
                 f'stroke="{P["ink"]}" stroke-width="3"/>'
                 f'<path d="M{f1(ex)},{cy - 6} q4,4 0,8" stroke="{P["ink"]}" stroke-width="2.2" fill="none"/>')
    return doc(ship_place(body))


def halyard_svg(hauling, hands):
    mx = SHIP_X + 10 * K + 15
    top = SHIP_WL - 846 * K
    rope = S.mix(P["sackcloth"], P["wood_light"], 0.4)
    block = (f'<ellipse cx="{f1(mx)}" cy="{f1(top + 10)}" rx="6" ry="8" fill="{P["wood_dark"]}" '
             f'stroke="{P["ink"]}" stroke-width="2.4"/>')
    if not hauling:
        d = f"M{f1(mx)},{f1(top + 12)} L{f1(mx + 2)},{f1(RAIL - 16)}"
    else:
        (fx, fy), (nx, ny) = hands
        d = (f"M{f1(mx)},{f1(top + 12)} L{f1(mx)},{f1(fy - 14)} L{f1(fx)},{f1(fy)} L{f1(nx)},{f1(ny)} "
             f"Q{f1(nx - 22)},{f1(ny + 8)} {f1(nx - 26)},{f1(ny + 46)}")
    body = (f'<path d="{d}" stroke="{P["ink"]}" stroke-width="6.4" fill="none" stroke-linejoin="round" '
            f'stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{rope}" stroke-width="3.2" fill="none" stroke-linejoin="round" '
            f'stroke-linecap="round"/>' + block)
    if not hauling:
        body += (f'<rect x="{f1(mx - 8)}" y="{f1(RAIL - 22)}" width="18" height="7" rx="3" fill="{P["wood_dark"]}" '
                 f'stroke="{P["ink"]}" stroke-width="2"/>')
    return doc(S.g(body, filter="wobble-fine"))


def hull_cover_svg():
    y0 = SHIP_WL - 175 * K
    clip = f'<clipPath id="s3hullclip"><rect x="0" y="{f1(y0)}" width="{SW}" height="{SH}"/></clipPath>'
    return doc(f'<g clip-path="url(#s3hullclip)">{PR.ship(SHIP_X, SHIP_WL, K, -1, sail="furled", part="back")}</g>',
               clip)


def s04_to_here(x, y):
    """A point on s04's stage (its ship at rest, V4.SX / SY / SS / SF) -> the same ship-local spot on this ship."""
    return PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, (x - V4.SX) / (V4.SS * V4.SF), (y - V4.SY) / V4.SS)


def deck_cargo_svg(part):
    """The cargo on deck, laid out as s04 shows it at its t = 0 for the whole scene: this scene ends on s04's
    opening picture of the ship, so the loads must stay put through the dissolve. These are the six loads s04's
    sailors later heave overboard, at the spots s04_storm.build gives them (a_cr, a_jar, d_sack, c_jar, b_jar,
    b_sack, with their scales, seeds and colours: keep the two in step), moved to the same ship-local spots on
    this ship and scaled by K / SS.
      part 'fore': the crate and jar by the bow sailor and the sack at the mast sailor's feet (behind the crew,
                   as in s04);
      part 'aft':  the jar and sack just forward of Jonah's spot on the stern deck and the tall jar just aft of
                   it, drawn in front of him (s04 draws its cargo in front of its Jonah)."""
    d, k = V4.deck_y_at, K / V4.SS

    def carry_x(sx, variant):
        """x of a sailor's carrying hands (s04's carry_over)."""
        hc = C.hand_positions(C.sailor, sx, V4.DECK, V4.SS, 1, variant=variant, pose="carry")
        return (hc[0][0] + hc[1][0]) / 2

    def put(prop, x, y, s, **kw):
        return prop(*s04_to_here(x, y), s * k, **kw)

    if part == "fore":
        ax, dx = S4.AX, S4.DX
        out = (put(PR.crate, ax + 45, d(ax + 45) - 37, 0.78) + put(PR.jar, ax + 112, d(ax + 112) - 51, 0.62)
               + put(PR.sack, dx + 44, d(dx + 44) + 2, 0.6, seed=9))
    else:
        cx, bx = carry_x(S4.CX, 3) - 8, carry_x(S4.BX, 1)
        out = (put(PR.jar, cx, d(cx) - 50, 0.6, color=S.mix(P["terracotta"], P["sand"], 0.15))
               + put(PR.jar, bx, d(bx) - 53, 0.66, color=S.mix(P["terracotta"], P["sand"], 0.35))
               + put(PR.sack, S4.BX - 52, d(S4.BX - 52) + 2, 0.62, seed=6))
    return doc(out)


def hull_shadow_svg():
    c = S.mix(P["sea"], P["sea_deep"], 0.55)
    return doc(f'<ellipse cx="{SHIP_X - 20}" cy="{SHIP_WL + 16}" rx="{390 * K}" ry="17" fill="{c}" opacity="0.38" '
               f'filter="url(#soft)"/>'
               f'<ellipse cx="{SHIP_X - 40}" cy="{SHIP_WL + 8}" rx="{300 * K}" ry="8" fill="{c}" opacity="0.3" '
               f'filter="url(#soft)"/>')


BOW_X = SHIP_X - 425 * K
STERN_X = SHIP_X + 470 * K


def wake_svg():
    y = 950
    bow, stern = BOW_X, STERN_X
    fo = "#fbf8ee"
    sh = S.mix(P["sea"], P["sea_deep"], 0.35)

    def stroke(d, w, op=0.95):
        return (f'<path d="{d}" stroke="{sh}" stroke-width="{w + 4}" fill="none" stroke-linecap="round" '
                f'opacity="{op * 0.35:.2f}" transform="translate(0,3)"/>'
                f'<path d="{d}" stroke="{fo}" stroke-width="{w}" fill="none" stroke-linecap="round" '
                f'stroke-linejoin="round" opacity="{op:.2f}"/>')

    out = ""
    out += stroke(f"M{f1(bow - 46)},{f1(y + 8)} Q{f1(bow - 30)},{f1(y - 10)} {f1(bow - 6)},{f1(y - 6)} "
                  f"Q{f1(bow + 14)},{f1(y - 2)} {f1(bow + 40)},{f1(y + 2)}", 10)
    out += stroke(f"M{f1(bow - 30)},{f1(y + 8)} Q{f1(bow + 70)},{f1(y + 8)} {f1(bow + 220)},{f1(y + 4)}", 8)
    out += stroke(f"M{f1(bow - 36)},{f1(y + 12)} Q{f1(bow + 40)},{f1(y + 30)} {f1(bow + 180)},{f1(y + 46)}", 7)
    out += stroke(f"M{f1(bow + 70)},{f1(y + 34)} q40,10 90,16", 5, 0.8)
    for dx, dy, r in ((-58, -6, 5), (-44, -18, 4), (-66, 6, 3.5)):
        out += (f'<circle cx="{f1(bow + dx)}" cy="{f1(y + dy)}" r="{r}" fill="{fo}" stroke="{sh}" '
                f'stroke-width="1.5" opacity="0.9"/>')
    out += stroke(f"M{f1(bow + 230)},{f1(y + 5)} C{f1(bow + 360)},{f1(y + 10)} {f1(stern - 250)},{f1(y + 10)} "
                  f"{f1(stern - 60)},{f1(y + 5)}", 5, 0.75)
    for i in range(5):
        x = stern - 60 + i * 70
        yy = y + 6 + i * 7
        out += stroke(f"M{f1(x)},{f1(yy)} q{34 + i * 8},-10 {70 + i * 14},0", 7 - i * 1.0, 0.9 - i * 0.14)
        out += stroke(f"M{f1(x + 20)},{f1(yy + 16 + i * 3)} q{30 + i * 6},-8 {60 + i * 12},0", 4.5 - i * 0.6,
                      0.7 - i * 0.1)
    return doc(S.g(out, filter="wobble-fine"))


# ============================================================================ the narrator's question card

QCARD = (JSTOP + 270, 380)    # in the eastern sky above the road (toward Nineveh), clear of Jonah's head
QR = 112                      # card radius
SKY_SEED = 2                  # the nineveh_skyline seed s02 uses for its vision of the city


def qcard_svg():
    """The narrator's question to the children ('约拿为什么不想去呢？') — NOT Jonah's thought: a round storybook card
    with no tail, floating free in the eastern sky. Inside it, faint and hazy, the skyline of Nineveh (the answer
    has to do with that city); the big '？' is a separate layer on top."""
    x, y, r = QCARD[0], QCARD[1], QR
    defs = (f'<clipPath id="s3qclip"><circle cx="{x}" cy="{y}" r="{r - 6}"/></clipPath>' +
            ugrad("s3qsky", 0, y - r, 0, y + r, [(0, "#fffaf0"), (0.55, S.mix("#fffaf0", P["sky_warm"], 0.35)),
                                                 (1, S.mix("#fffaf0", P["sand"], 0.45))]) +
            S.rad_grad("s3qglow", [(0, "#fffbe6", 0.85), (0.6, "#fff4cf", 0.35), (1, "#fff4cf", 0)]))
    body = f'<circle cx="{x}" cy="{y}" r="{r * 1.55:.0f}" fill="url(#s3qglow)"/>'
    body += (f'<circle cx="{x + 5}" cy="{y + 9}" r="{r}" fill="{P["ink"]}" opacity="0.14" filter="url(#soft)"/>'
             f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#s3qsky)"/>')
    city = PR.nineveh_skyline(x - r - 40, x + r + 40, y + r * 0.62, 0.3, seed=SKY_SEED, haze=0.72)
    body += f'<g clip-path="url(#s3qclip)" opacity="0.5">{city}</g>'
    body += S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{P["ink"]}" stroke-width="4.5"/>'
                f'<circle cx="{x}" cy="{y}" r="{r - 11}" fill="none" stroke="{P["terracotta"]}" stroke-width="2.6" '
                f'stroke-dasharray="3 9" stroke-linecap="round" opacity="0.7"/>', filter="wobble-fine")
    return doc(body, defs)


def qmark_svg():
    x, y = QCARD
    return doc(S.text(x + 2, y + 38, "？", size=124, fill=P["terracotta"],
                      extra=f'stroke="{P["ink"]}" stroke-width="3.2" paint-order="stroke"'))


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = (ctx.line(i) for i in range(4))

    # ---------------------------------------------------------------- key times (from the narration)
    T_REFUSE = at(L0, "约拿不愿意") + 0.1                  # palm out, head shake
    T_TURN = at(L0, "他转过身") + 0.12                     # turns round (whoosh; the cut is 0.1 s later)
    T_RUN1 = T_TURN + 0.2
    T_STOP1 = L1.start - 0.45                            # stops under the olive tree, panting
    T_LOOKBACK = L1.start + 0.25                         # turns to look back east (the cut)
    T_BUB = at(L1, "为什么") + 0.15                         # the narrator's '？' card pops up
    T_POP = at(L1, "我们就会知道") - 0.05                    # ... and pops away
    T_TURN2 = T_POP + 0.22                               # turns west again (the cut is 0.1 s later)
    T_RUN2 = T_TURN2 + 0.2
    T_ARR = L2.chunks[1].start - 0.12 if len(L2.chunks) > 1 else at(L2, "找到")   # on the pier
    T_ASK = at(L2, "要开往") - 0.2                           # points at the ship
    T_ASK_END = T_ASK + 1.6
    T_CAP_WALK = T_ARR - 0.1                             # the captain walks aft to meet him ...
    T_CAP_TURN = T_ARR + 0.85                            # ... and greets him
    T_NOD = T_ASK + 0.75                                 # ... and nods
    T_WEST = at(L2, "他施在") + 0.05                         # the captain points west
    T_FETCH = L3.start - 0.45                            # Jonah takes coins from his sash
    T_CAP_BACK = T_FETCH - 0.1                           # the captain turns back to Jonah
    T_GIVE = T_FETCH + 0.45                              # Jonah holds the coins out on his open palm
    T_RECV = T_GIVE - 0.05                               # ... and the captain holds out his palm
    T_DROP = T_GIVE + 0.25                               # the first coin hops out of Jonah's hand ...
    COIN_GAP, COIN_FLY = 0.18, 0.42                      # ... one after another, each in a little arc
    T_COIN_LAND = T_DROP + COIN_FLY                      # the first coin lands in the captain's palm
    T_LAST_COIN = T_COIN_LAND + 2 * COIN_GAP
    T_TAKE = T_LAST_COIN + 0.35                          # the full palm is held a moment, then he closes his hand
    T_JDONE = T_TAKE + 0.2                               # only then Jonah lowers his arm
    T_LEAP = max(at(L3, "上了船"), T_JDONE + 0.3)          # hops aboard
    T_LAND = T_LEAP + 0.42
    T_SWAP = T_LEAP + 0.56 * (T_LAND - T_LEAP)
    T_SAIL = at(L3, "想要逃到") - 0.05                       # deck sailor hauls, the sail unrolls
    N_HAUL, STROKE = 3, 0.3                              # ... in three pulls on the halyard ...
    T_FOOT = T_SAIL + N_HAUL * STROKE                    # ... down to its foot corners ...
    T_SAIL_SET = T_FOOT + 0.2                            # ... and the wind fills it
    T_SAIL_DONE = T_SAIL + 0.64                          # (anchor of the camera's sail shot, see T_BACK1)
    T_BELAY = T_SAIL_DONE + 0.9                          # the mast sailor makes the halyard fast
    T_CAP_FWD = T_SAIL - 0.35                            # the captain turns to face the open sea
    T_BOWPOINT = T_SAIL + 0.5                            # the bow sailor points the way
    T_DEPART = T_SAIL + 0.15                             # the ship leaves the pier
    T_HIDE = L3.chunks[1].start if len(L3.chunks) > 1 else at(L3, "躲开")
    T_LOOK = T_HIDE - 0.6                                # Jonah looks back at the shore ...
    T_DUCK = T_HIDE + 0.03                               # ... and ducks behind the stern rail on '躲开'
    # the jar hand-off while the camera arrives at the harbour
    T_SWING = None                                       # set below from Jonah's run (before he reaches P2)
    T_P2POINT = T_DEPART + 1.2                           # porter 2 points after the ship

    # ---------------------------------------------------------------- hand positions for the fare
    cap_xy = (CAP_X, DECK)
    cap_palm = C.hand_positions(captain_fig, *cap_xy, K, 1, pose="receive")[1]
    give0 = C.hand_positions(jonah_fig, 0, GY, K, -1, pose="pay_give")[1]
    # Jonah stands so that his hand is about 45 px aft of and 40 px below the captain's palm: the two hands never
    # overlap, the palm is in the clear (sky / coat behind it, never Jonah's head) and the coins visibly travel
    # from one hand UP and then DOWN into the other
    jpay = cap_palm[0] + 45 - give0[0]
    give = (jpay + give0[0], give0[1])
    # he hops up over the rail onto the deck at the ship-local spot s04 starts him at (local x 239, by the cargo)
    BOARD_X = round(lx2x(-239))

    # ---------------------------------------------------------------- Jonah's path
    D1 = JX0 - JSTOP
    D2 = JSTOP - jpay
    TA, TD1, TD2 = 0.3, 0.45, 0.4

    def run_dist(t):
        """Distance run since the crossroads (both legs)."""
        if t < T_RUN2:
            return trapezoid(t, T_RUN1, T_STOP1, D1, TA, TD1)[0]
        return D1 + trapezoid(t, T_RUN2, T_ARR, D2, TA, TD2)[0]

    V1 = trapezoid(T_RUN1, T_RUN1, T_STOP1, D1, TA, TD1)[1]
    V2 = trapezoid(T_RUN2, T_RUN2, T_ARR, D2, TA, TD2)[1]
    H_LEAP = 125

    def jpos(t):
        if t < T_LEAP:
            return JX0 - run_dist(t), GY
        u = min(1.0, (t - T_LEAP) / (T_LAND - T_LEAP))
        x = jpay + (BOARD_X - jpay) * (1 - (1 - u) ** 1.6)
        y = GY + (DECK - GY) * u - 4 * H_LEAP * u * (1 - u)
        return x, y

    def running(t):
        return (T_TURN + 0.1 <= t < T_STOP1) or (T_TURN2 + 0.1 <= t < T_ARR)

    def t_pass(x):
        tt = T_RUN2
        while tt < T_ARR and jpos(tt)[0] > x:
            tt += 0.01
        return tt

    T_SWING = max(L2.start + 0.2, t_pass(P2X + 680))     # the toss is done before Jonah reaches the porters
    T_THROWF = T_SWING + 0.07
    T_REL = T_SWING + 0.16
    T_CATCH = T_REL + 0.5
    T_STOW = T_CATCH + 0.85

    # ---------------------------------------------------------------- run cycle, footfalls on the sound
    RUN_DD = V.RUN_ANKLE_STEP * K          # px per drawing; one step = 4 drawings
    RUN_STEP = 4 * RUN_DD
    rate1, rate2 = V1 / RUN_STEP, V2 / RUN_STEP          # steps per second while cruising

    def mid_beat(at_s, dur, rate):
        """Time (s after the cue starts) of the footfall nearest the middle of the footsteps_run cue the mix will
        render for this cue (same seed rule as audio/mix.py), so the contact drawings land on the sound."""
        try:
            import zlib
            from audio import sfx as SFX
            seed = zlib.crc32(f"{ctx.id}:footsteps_run:{float(at_s)}".encode()) & 0xFFFF
            x = SFX.make("footsteps_run", dur, 48000, seed=seed, rate=rate)
            e = np.abs(x).mean(axis=1)
            hop = 240
            env = np.convolve(e, np.ones(hop) / hop, mode="same")[::hop]
            per = 48000 / rate / hop
            c = int(dur / 2 * 48000 / hop)
            lo, hi = max(0, int(c - 0.6 * per)), min(len(env), int(c + 0.6 * per))
            # onset = steepest rise in the window
            dv = np.diff(env[lo:hi + 1])
            return (lo + int(np.argmax(dv))) * hop / 48000
        except Exception:
            return dur / 2

    LEG1_AT, LEG1_DUR = T_RUN1, T_STOP1 - T_RUN1 + 0.05
    LEG2_AT, LEG2_DUR = T_RUN2, T_ARR - T_RUN2 + 0.05
    # a contact drawing (0 or 4 of RUN_SEQ) is exact when the distance run = DF + k * RUN_STEP / 2
    DF1 = run_dist(LEG1_AT + mid_beat(LEG1_AT, LEG1_DUR, rate1))
    DF2 = run_dist(LEG2_AT + mid_beat(LEG2_AT, LEG2_DUR, rate2))

    def run_idx(t):
        d = run_dist(t)
        df = DF1 if t < T_RUN2 else DF2
        k = int(math.floor((d - df) / RUN_DD + 0.5))
        return k % 8

    pelvis_h = {p: -C.body_points(V.jonah_fig, 0, 0, K, 1, pose=p)["pelvis"][1] for p in V.RUN_SEQ}
    peak_h = pelvis_h["run_push_n"] + 12 * K
    RUN_LIFT = {i: -(peak_h - pelvis_h[V.RUN_SEQ[i]]) for i in V.RUN_FLIGHT}

    def leap_lift(t):
        return 0.0

    # ---------------------------------------------------------------- ship motion
    # the ship gathers way, cruises, and as Jonah hides it slows to a gentle drift (never a dead stop), so the
    # closing shot (s04's opening picture of the ship, see the camera) is nearly still
    T_SLOW0 = T_HIDE - 0.4
    T_PUSH1 = T - 1.0                    # the ship has slowed to its drift by here (the closing dissolve starts)
    DIST = 500                           # distance sailed by T_PUSH1 (the stern is then clear of the pier)
    V_END = 0.08                         # drift speed at the end, as a fraction of the cruising speed
    RISE = 36                            # sailing away it shrinks 10 % and its waterline rises toward the horizon
    #                                      (perspective; this also keeps the closing framing inside the stage)
    T_IN = T_DUCK - 0.25                 # the camera has leaned in on Jonah as he glances back, and pulls back as
    T_OUT = T - XF - 0.1                 # he ducks: it is on s04's framing 0.1 s before the dissolve starts, so
    #                                      the ship never doubles in it (the pull-back keeps its 1.44 s and its
    #                                      ~30 %/s peak zoom); meanwhile the ship's rocking turns into s04's, so
    #                                      they rock as one
    _st = np.arange(T_DEPART, T + 1.01, 1 / 240)
    _sv = np.array([M.progress(t, T_DEPART, T_DEPART + 0.9, "sine")
                    * (1 - (1 - V_END) * M.progress(t, T_SLOW0, T_PUSH1, "sine")) for t in _st])
    _sd = np.concatenate([[0.0], np.cumsum((_sv[1:] + _sv[:-1]) / 2) / 240])
    V_SHIP = DIST / float(np.interp(T_PUSH1, _st, _sd))      # cruising speed (stage px/s)
    _sd *= V_SHIP

    def ship_d(t):
        return float(np.interp(t, _st, _sd)) if t > T_DEPART else 0.0

    def ship_way(t):
        """0..1: how fast the ship is moving (for the bow foam and the wake)."""
        return float(np.interp(t, _st, _sv)) if t > T_DEPART else 0.0

    def ship_rise(t):
        return RISE * ship_d(t) / DIST

    def s04_rock(t):
        """s04's opening rocking at this scene's time t: roll (deg) about a pivot 40 px below its waterline and bob
        (dx, dy) in its stage px (pitch 1.3 deg, bob 5 px, one rock per 4 s from s04's t = -1)."""
        ph = 2 * math.pi * (t - (T - XF) + 1.0) / 4.0
        rot = 1.3 * math.sin(ph)
        return rot, 1.75 * math.sin(0.5 * ph + 0.4) + 40 * math.sin(math.radians(rot)), 5.0 * math.sin(ph - 1.3)

    def ship_tf(t):
        u = ship_d(t) / DIST
        s = 1 - 0.1 * u
        dx, dy = 0.0, 3.0 * math.sin(2 * math.pi * t / 3.1) + 1.5 * math.sin(2 * math.pi * t / 1.7 + 1)
        rot = (0.45 + 0.5 * u) * math.sin(2 * math.pi * (t / 3.6 + 0.2))
        g = M.progress(t, T_IN, T_OUT, "sine")
        if g > 0.0:
            r4, dx4, dy4 = s04_rock(t)
            k = K * s / V4.SS
            rot, dx, dy = M.lerp(rot, r4, g), g * dx4 * k, M.lerp(dy, dy4 * k, g)
        return Tf(dx=dx - ship_d(t), dy=dy - ship_rise(t), rot=rot, sx=s, sy=s, px=SHIP_X, py=SHIP_WL)

    def ship_anchor(t):
        """The ship's anchor (hull centre on the waterline) on stage, without the bob and roll."""
        return SHIP_X - ship_d(t), SHIP_WL - ship_rise(t)

    # ---------------------------------------------------------------- camera
    # every move uses 'sine' easing (peak speed 1.57x the average): zoom stays under ~30 %/s and pans under
    # ~300 output px/s (checked at 30 fps), gentle enough for 3-8 year olds
    # matches s02's last frame, Cam(1200, 752.5, 2040) on its 2400 x 1350 stage, which s02 holds from T - 1 on
    # (Jonah, arms folded, at output x ~735 with his feet at y ~914, clear of the subtitle box that fades in at
    # ~0.8 s), so the dissolve shows one Jonah. Keep the two in step:
    # s02 y = 1150 - (GY - this y) * 2040 / 1360
    OPEN_CAM = (5603.0, 645.0, 1360.0)
    T_OPEN_HOLD, T_OPEN_END = 1.05, T_TURN + 0.55
    T_OPEN_UP = 1.9                            # the tilt / widening part of the opening move is done by here
    W_CROSS, Y_CROSS = 1600, 640
    X_CROSS = min(JX0 + 110, PAINT_R - W_CROSS / 2 - 8)
    X_PIER = 2190
    X_WEST, W_WEST, Y_WEST = 1950, 1780, 600
    T_WEST_END = min(T_WEST + 1.8, L2.end)
    # '约拿付了船钱': pushed in on the two hands (from T_WEST_END, finished by T_GIVE)
    X_PAY = (cap_palm[0] + give[0]) / 2 + 10
    W_PAY, Y_PAY = 1220, 650
    # '上了船': eases back a little and tilts up so the sail unrolling from the yard is in the picture ...
    T_BACK0, T_BACK1 = T_LEAP - 0.25, T_SAIL_DONE + 0.1
    W_SAIL, Y_SAIL = 1360, 578
    X_SAIL = SHIP_X + 60 - ship_d(T_BACK1)
    # '躲开上帝' and the closing dissolve. s04 opens on a static wide shot of this ship at sea, so this scene ends
    # on exactly that picture of the ship (s04's opening camera, ship anchor and scale: art.scenes_v1.s04_storm):
    # from the sail shot the camera picks up the departing ship and follows it (a follow pan of up to ~570 output
    # px/s, like the run-follows above: the ship stays steady on screen while the pier slides away), tilts down
    # and leans in a little on Jonah as he glances back, then pulls back as he ducks behind the stern rail until
    # the ship has s04's size and place (0.1 s before the dissolve starts), and tracks the drifting ship through
    # the dissolve. Ship, sail, crew, Jonah, deck cargo, stern scroll and lantern stay put through the dissolve;
    # only the backgrounds (the pier and Joppa -> the open sea) and the clouds cross-fade.
    W_IN = 1290                             # leaned in on Jonah at T_IN, back at s04's framing by T_OUT
    LEAD = 0.13

    def s04_ship_out(t):
        """Output px of s04's ship anchor (hull centre on the waterline, no bob) at this scene's time t; s04's ship
        drifts west 120 px over its first ~6.5 s (its sail_dx)."""
        ax = V4.SX + 120 * (1 - M.progress(t - (T - XF), 0, 6.5, "sine"))
        return (ax - S4_CAM[0]) * S4_K + 960, (V4.SY - S4_CAM[1]) * S4_K + 540

    def match_w(t):
        """Camera width that shows this ship at s04's size."""
        return S4_CAM[2] * K * (1 - 0.1 * ship_d(t) / DIST) / V4.SS

    def hermite(t, t0, t1, p0, v0, p1, v1):
        d = t1 - t0
        u = min(max((t - t0) / d, 0.0), 1.0)
        return ((2 * u ** 3 - 3 * u ** 2 + 1) * p0 + (u ** 3 - 2 * u ** 2 + u) * d * v0
                + (3 * u ** 2 - 2 * u ** 3) * p1 + (u ** 3 - u ** 2) * d * v1)

    # where the ship's anchor is on screen: at T_BACK1 (camera at rest on the sail shot) it moves with the ship;
    # from there it glides to where s04 shows its ship, arriving at T_OUT
    _a0, _a1 = ship_anchor(T_BACK1 - 0.01), ship_anchor(T_BACK1 + 0.01)
    _k0 = 1920 / W_SAIL
    O0 = ((_a0[0] + _a1[0]) / 2 - X_SAIL) * _k0 + 960, ((_a0[1] + _a1[1]) / 2 - Y_SAIL) * _k0 + 540
    OV0 = (_a1[0] - _a0[0]) / 0.02 * _k0, (_a1[1] - _a0[1]) / 0.02 * _k0
    O1 = s04_ship_out(T_OUT)
    OV1 = [(q - p) / 0.02 for p, q in zip(s04_ship_out(T_OUT - 0.01), s04_ship_out(T_OUT + 0.01))]

    def end_cam(t):
        """(x, y, w) from the sail shot (T_BACK1) to s04's framing of the ship (T_OUT) and on to the end."""
        if t < T_IN:
            w = W_SAIL * (W_IN / W_SAIL) ** M.progress(t, T_BACK1, T_IN, "sine")
        else:
            w = W_IN * (match_w(t) / W_IN) ** M.progress(t, T_IN, T_OUT, "sine")
        if t < T_OUT:
            ox, oy = (hermite(t, T_BACK1, T_OUT, O0[i], OV0[i], O1[i], OV1[i]) for i in (0, 1))
        else:
            ox, oy = s04_ship_out(t)
        ax, ay = ship_anchor(t)
        return ax - (ox - 960) * w / 1920, ay - (oy - 540) * w / 1920, w

    cam_w_f = M.keys([(0, {"dx": W_CROSS}), (T_TURN, {"dx": 1560}), (T_RUN1 + 1.2, {"dx": 1760}),
                      (T_STOP1, {"dx": 1700}), (T_BUB + 0.4, {"dx": 1560}), (T_RUN2, {"dx": 1580}),
                      (T_RUN2 + 1.8, {"dx": 1900}), (T_ARR + 0.6, {"dx": 1840}), (T_WEST, {"dx": 1720}),
                      (T_WEST_END, {"dx": W_WEST}), (T_GIVE, {"dx": W_PAY}), (T_BACK0, {"dx": W_PAY}),
                      (T_BACK1, {"dx": W_SAIL})], "sine")
    cam_y_f = M.keys([(0, {"dy": Y_CROSS}), (T_TURN, {"dy": 648}), (T_RUN1 + 1.2, {"dy": 612}),
                      (T_STOP1, {"dy": 612}), (T_BUB + 0.4, {"dy": 600}), (T_RUN2 + 1.8, {"dy": 606}),
                      (T_WEST, {"dy": 606}), (T_WEST_END, {"dy": Y_WEST}), (T_GIVE, {"dy": Y_PAY}),
                      (T_BACK0, {"dy": Y_PAY}), (T_BACK1, {"dy": Y_SAIL})], "sine")
    cam_x_after = M.keys([(T_ARR, {"dx": X_PIER}), (T_WEST, {"dx": X_PIER}), (T_WEST_END, {"dx": X_WEST}),
                          (T_GIVE, {"dx": X_PAY}), (T_BACK0, {"dx": X_PAY}), (T_BACK1, {"dx": X_SAIL})], "sine")

    def cam_x_raw(t):
        if t >= T_BACK1:
            return end_cam(t)[0]
        w = cam_w_f(t).dx
        if t < T_ARR:
            jx = jpos(t)[0]
            return max(min(X_CROSS, jx - LEAD * w), X_PIER)
        return cam_x_after(t).dx

    DT = 1 / 120
    ts = np.arange(-1.0, T + 1.0, DT)
    raw = np.array([cam_x_raw(min(max(t, 0.0), T)) for t in ts])
    # the follow part only ever pans west (no back-and-forth from the stop / run speed changes)
    i_arr = int((T_ARR + 1.0) / DT)
    raw[:i_arr] = np.minimum.accumulate(raw[:i_arr])
    sig = 0.16
    kk = np.arange(-int(3 * sig / DT), int(3 * sig / DT) + 1) * DT
    ker = np.exp(-0.5 * (kk / sig) ** 2)
    ker /= ker.sum()
    xs = np.convolve(np.pad(raw, len(kk) // 2, mode="edge"), ker, mode="valid")
    # the closing move is smooth already: hand over to it exactly so the ship lines up with s04's in the dissolve
    r = np.array([M.progress(t, T_BACK1, T_BACK1 + 3 * sig, "sine") for t in ts])
    xs = xs * (1 - r) + raw * r
    tc = [min(max(t, 0.0), T) for t in ts]
    ws = np.array([end_cam(t)[2] if t >= T_BACK1 else cam_w_f(t).dx for t in tc])
    ys = np.array([end_cam(t)[1] if t >= T_BACK1 else cam_y_f(t).dy for t in tc])
    hs = ws * 9 / 16
    xs = np.clip(xs, ws / 2 + 4, PAINT_R - ws / 2 - 4)
    ys = np.clip(ys, hs / 2 + 4, SH - hs / 2 - 4)
    # the opening dissolve: s02 ends on Jonah, arms folded, at the left of its frame; this scene opens on him in
    # the same place and size (s02's end framing, in this stage's px), holds it through the dissolve, then eases
    # to the follow framing (Jonah right of centre, the road west ahead of him) by the time he turns to run.
    # His feet are above the first subtitle's box from the first frame on. The widening (and the small tilt) go
    # first, on a quicker ease right after the dissolve (zoom peaks at ~26 %/s); the pan west takes until the turn.
    # Both framings lie inside the painted stage, and the frame stays inside it in between (checked).
    g = np.array([M.progress(t, T_OPEN_HOLD, T_OPEN_END, "sine") for t in ts])
    gy = np.array([M.progress(t, T_OPEN_HOLD - 0.05, T_OPEN_UP, "sine") for t in ts])
    xs = OPEN_CAM[0] + (xs - OPEN_CAM[0]) * g
    ys = OPEN_CAM[1] + (ys - OPEN_CAM[1]) * gy
    ws = OPEN_CAM[2] + (ws - OPEN_CAM[2]) * gy

    def cam(t):
        return Cam(float(np.interp(t, ts, xs)), float(np.interp(t, ts, ys)), float(np.interp(t, ts, ws)))

    sc.camera = cam

    # the opening framing sits low (Jonah's feet above the subtitle box), so the sky things near the top of it
    # (the sun, the clouds, gull1) are lowered by the same amount through the dissolve and the hold: they keep
    # their earlier, uncropped place in the frame (the camera opened at y 578 before), and settle back onto
    # their stage places as the camera widens; from T_OPEN_UP on the offset is 0
    SKY_DY = OPEN_CAM[1] - 578.0

    def sky_dy(t):
        return SKY_DY * (1.0 - M.progress(t, T_OPEN_HOLD - 0.05, T_OPEN_UP, "sine"))

    def parallax(k, vx=0.0):
        return lambda t: Tf(dx=k * (cam(t).x - X_REF) + vx * t)

    # ---------------------------------------------------------------- sky / far / town
    # the distant ship (seen on '他施在很远很远的西边') has sailed on over the horizon by the closing shot; it goes
    # while it is off screen (the camera is on the pier and the hands then), so the dissolve shows no second ship
    sc.add("far", [far_svg(), far_svg(far_ship=False)], motion=parallax(K_FAR), wc=0.8,
           frame_at=lambda t: 0.0 if t < T_LEAP else 1.0)

    # the sun: in the pull-back it settles onto s04's sun (same place and size), so the dissolve shows one sun
    def sun_tf(t):
        dx = K_SUN * (cam(t).x - X_REF)
        g = M.progress(t, T_IN, T_OUT, "sine")
        if g <= 0.0:
            return Tf(dx=dx, dy=sky_dy(t))
        c = cam(t)
        k = c.w / 1920
        ox = (S4_SUN[0] + 9 * max(0.0, t - (T - XF)) - S4_CAM[0]) * S4_K + 960
        oy = (S4_SUN[1] - S4_CAM[1]) * S4_K + 540
        tx, ty = c.x + (ox - 960) * k, c.y + (oy - 540) * k
        s_ = 1 + g * (S4_SUN[2] * S4_K * k / SUN_R - 1)
        return Tf(dx=dx + g * (tx - SUN[0] - dx), dy=g * (ty - SUN[1]), sx=s_, sy=s_, px=SUN[0], py=SUN[1])

    sc.add("sun", sun_svg(), motion=sun_tf, wc=0.4)
    sc.add("clouds", clouds_svg(), motion=lambda t: Tf(dx=K_CLOUD * (cam(t).x - X_REF) + 7.0 * t, dy=sky_dy(t)),
           wc=0.6)
    sc.add("town", town_svg(), motion=parallax(K_TOWN))
    sc.add("harbour_back", harbour_back_svg())

    sea_mid_m = M.combine(M.bob(3, 3.4), M.bob(14, 5.2, axis="x"))
    sc.add("sea_mid", sea_band_svg(824, 5, 280, 0.4, S.mix(P["sea_light"], P["sea_pale"], 0.3), P["sea_light"], 8, 31,
                                   foam_x=((-100, 700, 0), (1100, 1800, 6), (2100, 2600, 2)), foam_op=0.6),
           motion=sea_mid_m)

    def twinkle(rate, phase):
        def f(t):
            v = (t * rate + phase) % 6.0
            return v if v <= 3.0 else 6.0 - v
        return f

    sc.add("glints_mid", [glints_svg(-100, SEA_RIGHT - 40, 838, 940, 50, 100 + i) for i in range(4)],
           motion=sea_mid_m, frame_at=twinkle(2.2, 0.0), wc=0.25)
    sc.add("harbour_corner", harbour_corner_svg())

    # ---------------------------------------------------------------- ship group
    # the furled sail is the sail roll lashed under the bare yard (one drawing for the bundle and the roll); the
    # back of the ship switches to its full sail only once the unrolled band shows all of it
    sc.add("ship_back", [ship_back_bare_svg(), ship_svg("back", "full")], motion=ship_tf,
           frame_at=lambda t: 1.0 if t >= T_SAIL_SET else 0.0, seed=SHIP_SEED)

    d1 = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, MAST_SAILOR_LX, PR.SHIP_DECK_Y)
    catch_hands = V.mid(C.hand_positions(C.sailor, *d1, K, 1, variant=1, pose="carry"))
    pull_hands = C.hand_positions(C.sailor, *d1, K, 1, variant=1, pose="pull")

    def haul_phase(t):
        """(stroke index, 0..1 within it) of the haul, or None outside it."""
        if not (T_SAIL <= t < T_FOOT):
            return None
        k, f = divmod((t - T_SAIL) / STROKE, 1.0)
        return int(k), f

    def haul_u(t):
        """0..1: how far the sail has come down from the yard to its foot corners. Each pull on the halyard
        brings it down a step (the first 70 % of a stroke); while the sailor reaches up for the next grip it
        only sags a little."""
        if t <= T_SAIL:
            return 0.0
        if t >= T_FOOT:
            return 1.0
        k, f = haul_phase(t)
        stair = (k + M.progress(f, 0.0, 0.7, "inout")) / N_HAUL
        return 0.85 * stair + 0.15 * (t - T_SAIL) / (T_FOOT - T_SAIL)

    def haul_dip(t):
        """How far (stage px) the mast sailor's body sinks into each pull, and comes back up for the next."""
        hp = haul_phase(t)
        if hp is None:
            return 0.0
        f = hp[1]
        return 6.0 * (math.sin(0.5 * math.pi * f / 0.7) if f < 0.7 else math.cos(0.5 * math.pi * (f - 0.7) / 0.3))

    def mast_sailor_local(t):
        """(dy, sy) of the mast sailor about his feet, before the ship's motion."""
        sy = 1.0
        if T_SAIL <= t < T_SAIL + 0.16:
            sy = 0.93 + 0.07 * M.progress(t, T_SAIL, T_SAIL + 0.16, "out")      # springs into the haul
        sy *= 1 - 0.004 * haul_dip(t)
        dy = (deck_dip(t) - 6 * bump(t, T_STOW + 0.4, 0.2) - 6 * bump(t, T_ARR + 0.25, 0.2)
              - 6 * bump(t, T_BELAY - 0.05, 0.2) + 1.3 * math.sin(2 * math.pi * t / 2.4 + 1) + haul_dip(t))
        return dy, sy

    # while he hauls, the halyard runs from the masthead block to his fists: stretch it (about the block) so its
    # lower end follows his hands down on each pull
    HAL_TOP = (SHIP_X + 10 * K + 15, SHIP_WL - 846 * K + 10)
    HAND_Y = (pull_hands[0][1] + pull_hands[1][1]) / 2

    def halyard_tf(t):
        if not (T_SAIL <= t < T_BELAY):
            return ship_tf(t)
        dy, sy = mast_sailor_local(t)
        shift = dy + (sy - 1) * (HAND_Y - d1[1])
        return V.compose(ship_tf(t), HAL_TOP, sy=1 + shift / (HAND_Y - HAL_TOP[1]))

    sc.add("halyard", [halyard_svg(False, pull_hands), halyard_svg(True, pull_hands)], motion=halyard_tf,
           frame_at=lambda t: 1.0 if T_SAIL <= t < T_BELAY else 0.0, wc=0.4)

    BB_TOP = SHIP_WL - 948 * K
    BB_BOT = SHIP_WL - 200 * K

    def sail_edge_l(t):
        if t < T_FOOT:
            return M.lerp(V.SAIL_TOP_L, V.SAIL_FOOT_L, haul_u(t))
        return M.lerp(V.SAIL_FOOT_L, -200, M.progress(t, T_FOOT, T_SAIL_SET - 0.02, "sine"))

    def sail_reveal(t):
        ey = SHIP_WL + sail_edge_l(t) * K
        return {"mode": "down", "frac": min(1.0, max(0.0, (ey - BB_TOP) / (BB_BOT - BB_TOP))), "soft": 10}

    def sail_tf(t):
        b = ship_tf(t)
        return Tf(b.dx, b.dy, b.rot, b.sx, b.sy, 1.0 if t >= T_SAIL else 0.0, b.px, b.py)

    sc.add("sail", sail_band_svg(), motion=sail_tf, reveal=sail_reveal, seed=SHIP_SEED)
    ROLL_PIV = (SHIP_X + 10 * K, SHIP_WL + V.ROLL_CY * K)

    def roll_tf(t):
        """The furled sail: lashed under the yard until the haul, then it rides the sail's lower edge down,
        unrolling (it follows the sail's width and gets thinner as the cloth comes off it); at the foot it is
        used up: it flattens into the hem (and is gone) as the wind fills the sail."""
        if t >= T_FOOT + 0.14:
            return Tf(alpha=0.0)
        v = haul_u(t)
        wv, _ = V.sail_width(v)
        dy = (sail_edge_l(min(t, T_FOOT)) - V.SAIL_TOP_L) * K
        sy = (1 - 0.5 * v) * (1 - 0.8 * M.progress(t, T_FOOT, T_FOOT + 0.14, "sine"))
        a = 1 - M.progress(t, T_FOOT + 0.07, T_FOOT + 0.14, "linear")
        return V.compose(ship_tf(t), ROLL_PIV, dy=dy, sx=(wv + 16) / (V.ROLL_W - 4), sy=sy, alpha=a)

    sc.add("sail_roll", sail_roll_svg(), motion=roll_tf, wc=0.6)
    Z_ROLL = sc.layers[-1].z
    sc.add("deck_cargo", deck_cargo_svg("fore"), motion=ship_tf)

    # bow sailor (variant 0): watches the pier; on '他施在很远很远的西边' he points far out to sea (west), then
    # looks ahead, and points the way again as they sail
    b0 = PR.local_to_stage(SHIP_X, SHIP_WL, K, -1, BOW_SAILOR_LX, PR.SHIP_DECK_Y)
    T_BOW_DOWN = L2.end + 0.1

    def bow_frame(t):
        if t >= T_BOWPOINT:
            return 1.0
        if t >= T_BOW_DOWN:
            return 2.0
        return 1.0 if t >= T_WEST else 0.0

    sc.add("bow_sailor", [doc(C.sailor(*b0, K, 1, variant=0, pose="stand", expr="neutral")),
                          doc(C.sailor(*b0, K, -1, variant=0, pose="point", expr="happy")),
                          doc(C.sailor(*b0, K, -1, variant=0, pose="stand", expr="happy"))],
           motion=lambda t: V.compose(ship_tf(t), b0, dy=sum(-6 * bump(t, c - 0.05, 0.2)
                                                              for c in (T_WEST, T_BOW_DOWN, T_BOWPOINT))
                                      + 1.4 * math.sin(2 * math.pi * t / 2.6 + 2)),
           frame_at=bow_frame)

    # mast sailor (variant 1): catches the porter's jar and stows it, smiles at the new passenger, hauls the
    # halyard to set sail, then makes it fast
    def deck_dip(t):
        return 9 * bump(t, T_CATCH, 0.25) + 16 * bump(t, T_STOW, 0.34)

    def mast_sailor_tf(t):
        # the same local motion as the halyard's lower end, so the rope stays in his fists on every pull
        dy, sy = mast_sailor_local(t)
        return V.compose(ship_tf(t), d1, dy=dy, sy=sy)

    def mast_sailor_frame(t):
        if t >= T_BELAY:
            return 2.0
        if t >= T_SAIL:
            return 3.0
        if t >= T_ARR + 0.3:
            return 2.0
        return 1.0 if t >= T_STOW + 0.45 else 0.0

    sc.add("mast_sailor", [doc(C.sailor(*d1, K, 1, variant=1, pose="carry", expr="neutral")),
                           doc(C.sailor(*d1, K, 1, variant=1, pose="stand", expr="neutral")),
                           doc(C.sailor(*d1, K, 1, variant=1, pose="stand", expr="happy")),
                           doc(C.sailor(*d1, K, 1, variant=1, pose="pull", expr="neutral"))],
           motion=mast_sailor_tf, frame_at=mast_sailor_frame)
    Z_MAST = sc.layers[-1].z

    JAR_S = 0.45
    jd = (catch_hands[0], catch_hands[1] - 22)

    def jar_deck_tf(t):
        if t < T_CATCH or t >= T_STOW + 0.4:
            return Tf(alpha=0.0)
        low = 118 * M.progress(t, T_STOW, T_STOW + 0.34, "inout")
        return V.compose(ship_tf(t), jd, dy=deck_dip(t) + low)

    sc.add("jar_deck", doc(PR.jar(*jd, JAR_S)), motion=jar_deck_tf)

    # the captain: watches the loading from the bow, walks aft to meet Jonah, nods, points west, takes the
    # fare, then faces the open sea
    # taking the fare: his open hand closes on the coins where they landed (gold peeking out of the fist), then
    # the fist comes in to his chest through an in-between drawing, tucking them away, and he nods
    T_TAKE_MID = T_TAKE + 0.22
    T_TAKE_IN = T_TAKE_MID + 0.08

    def cap_frame(t):
        if t < T_CAP_TURN:
            return 0.0
        if t < T_WEST:
            return 1.0
        if t < T_CAP_BACK:
            return 2.0
        if t < T_RECV:
            return 1.0
        if t < T_TAKE:
            return 3.0
        if t < T_TAKE_MID:
            return 4.0
        if t < T_TAKE_IN:
            return 5.0
        if t < T_CAP_FWD:
            return 6.0
        return 7.0

    cap_frames = [doc(captain_fig(*cap_xy, K, 1, pose="stand", expr="neutral")),
                  doc(captain_fig(*cap_xy, K, 1, pose="stand", expr="happy")),
                  doc(captain_fig(*cap_xy, K, -1, pose="stand", expr="happy")),
                  doc(captain_fig(*cap_xy, K, 1, pose="receive")),
                  doc(captain_fig(*cap_xy, K, 1, pose="grab")),
                  doc(captain_fig(*cap_xy, K, 1, pose="take_mid")),
                  doc(captain_fig(*cap_xy, K, 1, pose="take")),
                  doc(captain_fig(*cap_xy, K, -1, pose="stand", expr="neutral"))]
    CAP_CUTS = (T_CAP_TURN, T_WEST, T_CAP_BACK, T_RECV, T_CAP_FWD)
    CAP_WALK = CAP_X0 - CAP_X                       # (negative) offset of his starting spot near the bow

    def cap_dx(t):
        return CAP_WALK * (1 - M.progress(t, T_CAP_WALK, T_CAP_TURN - 0.05, "sine"))

    def cap_dy(t):
        dy = sum(-7 * bump(t, c - 0.05, 0.2) for c in CAP_CUTS)              # little hop hides each pose cut
        dy += 4 * bump(t, T_TAKE - 0.03, 0.18)                               # squeezes the coins in his fist
        dy += 6 * bump(t, T_NOD, 0.3) + 6 * bump(t, T_TAKE_IN + 0.04, 0.26)  # nods
        if T_CAP_WALK <= t < T_CAP_TURN:                                       # steps (legs are behind the rail)
            dy -= 5 * abs(math.sin(math.pi * (t - T_CAP_WALK) / 0.3))
        return dy + 1.2 * math.sin(2 * math.pi * t / 2.9)

    def cap_tf(t):
        return V.compose(ship_tf(t), cap_xy, dx=cap_dx(t), dy=cap_dy(t))

    sc.add("captain", cap_frames, motion=cap_tf, frame_at=cap_frame, z=Z_MAST - 0.5)   # behind the mast sailor


    # Jonah on deck
    def jship_frame(t):
        if t < T_LAND + 0.06:
            return 0.0
        if t < T_LOOK:
            return 1.0
        if t < T_DUCK:
            return 2.0
        return 3.0

    jship = [doc(jonah_fig(BOARD_X, DECK, K, -1, pose="hop")),
             doc(jonah_fig(BOARD_X, DECK, K, -1, pose="stand", expr="worried")),
             doc(jonah_fig(BOARD_X, DECK, K, 1, pose="stand", expr="worried")),
             doc(jonah_fig(BOARD_X, DECK, K, 1, pose="stand", expr="scared"))]

    def jship_tf(t):
        b = ship_tf(t)
        if t < T_SWAP:
            return Tf(alpha=0.0)
        if t < T_LAND:
            x, y = jpos(t)
            ox, oy = x - BOARD_X, y - DECK + leap_lift(t)
        else:
            ox = 0.0
            oy = 5 * math.sin(math.pi * min(1.0, (t - T_LAND) / 0.18))
            oy -= 8 * bump(t, T_LOOK - 0.05, 0.2)
            oy += 104 * M.progress(t, T_DUCK, T_DUCK + 0.3, "inout")
            oy -= 14 * M.progress(t, T_DUCK + 0.9, T_DUCK + 1.25, "inout")
            oy += 2.0 * math.sin(2 * math.pi * t * 1.3)
        return V.compose(b, (BOARD_X, DECK), dx=ox, dy=oy)

    sc.add("jonah_ship", jship, motion=jship_tf, frame_at=jship_frame)
    sc.add("hull_cover", hull_cover_svg(), motion=ship_tf)
    sc.add("ship_front", ship_svg("front", "furled"), motion=ship_tf)
    Z_FRONT = sc.layers[-1].z

    sea_front_m = M.combine(M.bob(4, 2.9, 0.3), M.bob(-18, 4.4, axis="x"))
    sc.add("sea_front", sea_band_svg(950, 7, 360, 1.3, P["sea_light"], S.mix(P["sea"], P["sea_deep"], 0.3), 12, 41,
                                     foam_x=((-100, 600, 0), (900, 1500, 4), (1900, 2300, 0), (2400, 2700, 3))),
           motion=sea_front_m)
    sc.add("glints_front", [glints_svg(-100, SEA_RIGHT - 120, 962, 1046, 44, 200 + i) for i in range(4)],
           motion=sea_front_m, frame_at=twinkle(2.0, 1.3), wc=0.25)

    def water_tf(alpha_fn):
        """On the water with the ship: its bob damped, its rise (perspective) in full."""
        def m(t):
            b, r = ship_tf(t), ship_rise(t)
            return Tf(b.dx, (b.dy + r) * 0.4 - r, 0, b.sx, b.sy, alpha_fn(t), b.px, b.py)
        return m

    sc.add("hull_shadow", hull_shadow_svg(), motion=water_tf(lambda t: 1.0), wc=0.2)
    sc.add("wake", wake_svg(), motion=water_tf(lambda t: M.progress(t, T_DEPART, T_DEPART + 0.8, "sine")
                                               * (0.3 + 0.7 * ship_way(t))), wc=0.2)

    rngf = random.Random(77)
    FOAM_LIFE = 1.7
    foam = []
    tt = T_DEPART + 0.35
    while tt < T + 0.1:
        way = ship_way(tt)                  # less bow foam as the ship slows to a drift
        if way > 0.08:
            foam.append((tt, rngf.uniform(10, 60), rngf.uniform(2, 30), rngf.uniform(26, 58) * (0.5 + 0.5 * way),
                         rngf.uniform(0.7, 1.0) * min(1.0, 0.25 + way)))
        tt += rngf.uniform(0.07, 0.12)

    def bow_x(t):
        b = ship_tf(t)
        return SHIP_X + b.dx - 425 * K * b.sx

    foam = [(ts_, bow_x(ts_) + ox, SHIP_WL - ship_rise(ts_) - 14 + oy, ln, op) for ts_, ox, oy, ln, op in foam]

    def foam_fn(t):
        live = [(t - ts_, x, y, ln, op) for ts_, x, y, ln, op in foam if 0 <= t - ts_ <= FOAM_LIFE]
        if not live:
            return None
        x0 = int(min(x for _, x, _, _, _ in live) - 20)
        x1 = int(max(x + ln for _, x, _, ln, _ in live) + 40)
        y0, y1 = int(min(y for _, _, y, _, _ in live) - 10), int(max(y for _, _, y, _, _ in live) + 26)
        ss = 2
        im = Image.new("RGBA", (max(1, x1 - x0) * ss, (y1 - y0) * ss), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for age, x, y, ln, op in live:
            a = op * min(1.0, age / 0.15) * (1 - age / FOAM_LIFE) ** 1.3
            xx = (x - x0 + 14 * age) * ss
            yy = (y - y0 + 3 * age) * ss
            r = (3.0 if age < 0.6 else 2.4) * ss
            L = ln * (1 - 0.3 * age / FOAM_LIFE) * ss
            d.rounded_rectangle([xx, yy - r, xx + L, yy + r], radius=r, fill=(251, 248, 238, int(235 * a)))
        im = im.resize((im.width // ss, im.height // ss), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
        return im, (x0, y0)

    sc.add_dynamic("foam", foam_fn)

    # ---------------------------------------------------------------- land, quay, pier
    sc.add("land", land_svg())
    sc.add("sea_near", sea_band_svg(1054, 9, 440, 2.4, S.mix(P["sea"], P["sea_light"], 0.35), P["sea_deep"], 14, 51,
                                    foam_x=((-100, 800, 0), (1200, 2000, 0), (2200, 2560, 0)), x1=QUAY_X - 25),
           motion=M.combine(M.bob(5, 2.5, 0.6), M.bob(22, 3.9, axis="x")))

    # ---------------------------------------------------------------- porters (loading)
    p1 = (P1X, PIER_Y)
    p2 = (P2X, PIER_Y)
    sc.add("pier_shadows", doc(C.ground_shadow(p1[0] + 4, p1[1], K, 120, 0.24) +
                               C.ground_shadow(p2[0] - 8, p2[1], K, 130, 0.24)))

    # porter 1 carries a crate at hip height (shifting it, a little out of breath); as Jonah dashes past he
    # glances up in surprise, and once Jonah is clear he sets it down on the pier (so the set-down is not hidden
    # behind the running Jonah)
    tp1 = t_pass(p1[0] + 40)
    CRATE_DOWN_X = p1[0] - 108
    T_CRATE = max(tp1 + 0.3, t_pass(CRATE_DOWN_X - 140))

    def p1_bob(t):
        k = 1 - M.progress(t, T_CRATE - 0.2, T_CRATE + 0.1, "sine")
        k2 = M.progress(t, T_CRATE + 0.6, T_CRATE + 1.2, "sine")
        return Tf(dy=-4 * abs(math.sin(math.pi * t * 1.4)) * k - 1.5 * math.sin(2 * math.pi * t / 2.7) ** 2 * k2
                  - 6 * bump(t, T_CRATE + 0.17, 0.2) - 6 * bump(t, T_P2POINT + 0.25, 0.2),
                  rot=0.9 * math.sin(math.pi * t * 1.4) * k, px=p1[0], py=p1[1])

    CRATE_S = 0.62
    c_carry = V.mid(C.hand_positions(V.dockhand, *p1, K, -1, variant=0, pose="carry"))
    crate_hip = (c_carry[0] - 4, c_carry[1] - 6)
    crate_down = (CRATE_DOWN_X, PIER_Y - 49 * CRATE_S + 2)

    def crate_tf(t):
        if t < T_CRATE:
            bx, by = V.apply_tf(p1_bob(t), *crate_hip, p1)
        else:
            u = M.progress(t, T_CRATE, T_CRATE + 0.24, "in")
            bx, by = M.lerp(crate_hip[0], crate_down[0], u), M.lerp(crate_hip[1], crate_down[1], u)
        return Tf(dx=bx - crate_hip[0], dy=by - crate_hip[1])

    def p1_frame(t):
        if t >= T_P2POINT + 0.3:
            return 3.0
        if t >= T_CRATE + 0.22:
            return 2.0
        return 1.0 if t >= tp1 - 0.1 else 0.0

    sc.add("crate1", doc(PR.crate(*crate_hip, CRATE_S)), motion=crate_tf)
    sc.add("dockhand1", [doc(V.dockhand(*p1, K, -1, variant=0, pose="carry", expr="worried")),
                         doc(V.dockhand(*p1, K, -1, variant=0, pose="carry", expr="surprised")),
                         doc(V.dockhand(*p1, K, -1, variant=0, pose="stand", expr="neutral")),
                         doc(V.dockhand(*p1, K, -1, variant=0, pose="stand", expr="happy"))],
           frame_at=p1_frame, motion=p1_bob)

    def p2_bob(t):
        k = 1 - M.progress(t, T_SWING - 0.3, T_SWING, "sine")
        k2 = M.progress(t, T_REL + 0.4, T_REL + 1.0, "sine")
        return Tf(dy=-3 * abs(math.sin(math.pi * t * 1.7 + 0.6)) * k - 1.5 * math.sin(2 * math.pi * t / 2.3) ** 2 * k2
                  - 6 * bump(t, T_P2POINT - 0.05, 0.2),
                  rot=0.9 * math.sin(math.pi * t * 1.7 + 0.6) * k, px=p2[0], py=p2[1])

    j_carry = V.mid(C.hand_positions(V.dockhand, *p2, K, -1, variant=1, pose="carry"))
    j_carry = (j_carry[0], j_carry[1] - 22)
    j_throw = V.mid(C.hand_positions(V.dockhand, *p2, K, -1, variant=1, pose="throw"))
    j_throw = (j_throw[0] - 4, j_throw[1] - 28)
    tp2 = t_pass(p2[0] + 40)

    def p2_frame(t):
        if t < T_THROWF:
            return 0.0
        if t < T_REL + 0.32:
            return 1.0
        if t >= T_P2POINT:
            return 4.0
        return 3.0 if tp2 <= t < tp2 + 1.2 else 2.0

    sc.add("dockhand2", [doc(V.dockhand(*p2, K, -1, variant=1, pose="carry", expr="neutral")),
                         doc(V.dockhand(*p2, K, -1, variant=1, pose="throw", expr="happy")),
                         doc(V.dockhand(*p2, K, -1, variant=1, pose="stand", expr="neutral")),
                         doc(V.dockhand(*p2, K, -1, variant=1, pose="stand", expr="surprised")),
                         doc(V.dockhand(*p2, K, -1, variant=1, pose="point", expr="happy"))],
           frame_at=p2_frame, motion=p2_bob)

    catch_at = V.apply_tf(V.compose(ship_tf(T_CATCH), jd), *jd, jd)

    def jar_pier_tf(t):
        if t >= T_CATCH:
            return Tf(alpha=0.0)
        if t < T_SWING:
            b = p2_bob(t)
            x, y = V.apply_tf(b, *j_carry, p2)
            rot = b.rot
        elif t < T_REL:
            u = M.progress(t, T_SWING, T_REL, "inout")
            b = p2_bob(t)
            x = M.lerp(j_carry[0], j_throw[0], u) + b.dx
            y = M.lerp(j_carry[1], j_throw[1], u) - 30 * math.sin(math.pi * u) + b.dy
            rot = -14 * math.sin(math.pi * u)
        else:
            u = (t - T_REL) / (T_CATCH - T_REL)
            b = p2_bob(T_REL)
            sx0, sy0 = j_throw[0] + b.dx, j_throw[1] + b.dy
            x = M.lerp(sx0, catch_at[0], u)
            y = M.lerp(sy0, catch_at[1], u) - 120 * 4 * u * (1 - u)
            rot = 28 * math.sin(math.pi * u)
        return Tf(dx=x - j_carry[0], dy=y - j_carry[1], rot=rot, px=j_carry[0], py=j_carry[1])

    sc.add("jar_pier", doc(PR.jar(*j_carry, JAR_S)), motion=jar_pier_tf)

    # ---------------------------------------------------------------- Jonah on land
    # He opens on s02's last picture of him (arms folded, frowning, facing east), refuses, turns and runs west,
    # stops under the olive tree, looks back east (arms folded again), turns and runs on to the pier, asks, pays
    # (arm out, then lowered through an in-between) and hops aboard.
    jl = ([("stubborn", jonah_fig(JX0, GY, K, 1, pose="stubborn")),
           ("refuse", jonah_fig(JX0, GY, K, 1, pose="refuse", expr="angry"))] +
          [(f"run{i}", jonah_fig(JX0, GY, K, -1, pose=p, expr="worried")) for i, p in enumerate(V.RUN_SEQ)] +
          [("tired", jonah_fig(JX0, GY, K, -1, pose="stand", expr="tired")),
           ("arrived", jonah_fig(JX0, GY, K, -1, pose="stand", expr="surprised")),
           ("point", jonah_fig(JX0, GY, K, -1, pose="point", expr="neutral")),
           ("stand", jonah_fig(JX0, GY, K, -1, pose="stand", expr="neutral")),
           ("fetch", jonah_fig(JX0, GY, K, -1, pose="pay_fetch")),
           ("give", jonah_fig(JX0, GY, K, -1, pose="pay_give")),
           ("lower", jonah_fig(JX0, GY, K, -1, pose="pay_lower")),
           ("worried", jonah_fig(JX0, GY, K, -1, pose="stand", expr="worried")),
           ("hop", jonah_fig(JX0, GY, K, -1, pose="hop"))])
    FI = {name: float(i) for i, (name, _) in enumerate(jl)}
    jland = [doc(svg) for _, svg in jl]
    T_LOWER = T_JDONE - 0.1                              # Jonah's arm comes down through an in-between drawing

    def jland_frame(t):
        if t < T_REFUSE:
            return FI["stubborn"]
        if t < T_TURN + 0.1:
            return FI["refuse"]
        if running(t):
            return FI["run0"] + run_idx(t)
        if t < T_LOOKBACK and t < T_RUN2:
            return FI["tired"]
        if t < T_TURN2 + 0.1:
            return FI["stubborn"]
        if t >= T_LEAP:
            return FI["hop"]
        if t < T_ASK:
            return FI["arrived"]
        if t < T_ASK_END:
            return FI["point"]
        if t < T_FETCH:
            return FI["stand"]
        if t < T_GIVE:
            return FI["fetch"]
        if t < T_LOWER:
            return FI["give"]
        if t < T_JDONE:
            return FI["lower"]
        return FI["worried"]

    # facing changes are hard cuts to the mirrored drawing (at the times jland_frame switches), sold by a quick
    # squash on planted feet: he dips into the turn, the new drawing lands squashed and springs back
    TURNS = (T_TURN + 0.1, T_LOOKBACK, T_TURN2 + 0.1)
    CUTS = (T_REFUSE, T_STOP1, T_ARR, T_ASK, T_ASK_END, T_FETCH, T_GIVE)   # pose cuts: a small hop

    def turn_squash(t, tc, k=0.075):
        """How much he is squashed (0..k, negative = a slight stretch) around a turn cut at tc."""
        if tc - 0.08 <= t < tc:
            return k * math.sin(0.5 * math.pi * (t - tc + 0.08) / 0.08)
        if tc <= t < tc + 0.24:
            u = (t - tc) / 0.24
            return k * math.cos(math.pi * u) * (1 - u)
        return 0.0

    def jland_tf(t):
        if t >= T_SWAP:
            return Tf(alpha=0.0)
        x, y = jpos(t)
        rot = 0.0
        sx = sy = 1.0
        dy = 0.0
        if not running(t) and t < T_LEAP:
            pant = 1 + 2.2 * (1 - M.progress(t, T_STOP1, T_STOP1 + 3.0, "linear")) * (T_STOP1 <= t < T_RUN2)
            per = 2.4 / pant
            sy = 1 + 0.012 * pant * math.sin(2 * math.pi * t / per)
        if T_REFUSE + 0.08 < t < T_REFUSE + 1.3:
            env = min(1.0, (t - T_REFUSE - 0.08) / 0.15, (T_REFUSE + 1.3 - t) / 0.25)
            rot = 2.6 * env * math.sin(2 * math.pi * 3.0 * (t - T_REFUSE))
        for tc in TURNS:
            q = turn_squash(t, tc)
            sx *= 1 + 0.5 * q
            sy *= 1 - q
        for tc in CUTS:
            if tc - 0.06 <= t < tc + 0.16:
                u = (t - tc + 0.06) / 0.22
                dy -= 9 * math.sin(math.pi * u)
                sy *= 1 - 0.04 * math.sin(math.pi * u)
        # paying: the arm comes down through the in-between, he settles onto his heels with a little squash
        for tc, k in ((T_LOWER, 0.025), (T_JDONE, 0.045)):
            if tc <= t < tc + 0.26:
                u = (t - tc) / 0.26
                q = k * math.sin(math.pi * min(1.0, u * 1.6)) * (1 - u)
                sx *= 1 + 0.5 * q
                sy *= 1 - q
        if T_LEAP - 0.16 <= t < T_LEAP:                  # crouch before the hop
            sy *= 1 - 0.1 * math.sin(math.pi * (t - T_LEAP + 0.16) / 0.32)
        if running(t):
            dy += RUN_LIFT.get(run_idx(t), 0.0)
        elif t >= T_LEAP:
            dy = leap_lift(t)
        return Tf(dx=x - JX0, dy=y - GY + dy, rot=rot, sx=sx, sy=sy, px=JX0, py=GY)

    # dust puffs where a foot pushes off the dirt road
    puffs = []
    for leg, (d0, d1_, df) in enumerate(((0.0, D1, DF1), (D1, D1 + D2, DF2))):
        j = math.floor((d0 - df) / RUN_STEP)
        while True:
            d_fall = df + j * RUN_STEP
            j += 1
            if d_fall < d0 + 40:
                continue
            if d_fall > d1_ - 40:
                break
            x_sole = JX0 - d_fall - 48 * K
            if x_sole < QUAY_X + 430:
                continue
            target = d_fall + 2 * RUN_DD
            tt_ = T_RUN1 if leg == 0 else T_RUN2
            tend = T_STOP1 if leg == 0 else T_ARR
            while tt_ < tend and run_dist(tt_) < target:
                tt_ += 0.01
            if tt_ < tend:
                puffs.append((tt_, x_sole, 1.0))
    # skid puffs at the stop under the olive tree
    puffs.append((T_STOP1 - 0.12, JSTOP - 30, 1.4))
    PUFF_LIFE = 0.5

    def dust(t):
        live = [(t - ts_, x, s) for ts_, x, s in puffs if 0 <= t - ts_ <= PUFF_LIFE * s]
        if not live:
            return None
        x0 = min(x for _, x, _ in live) - 90
        x1 = max(x for _, x, _ in live) + 140
        y0, y1 = GY - 100, GY + 30
        im = Image.new("RGBA", (int(x1 - x0), int(y1 - y0)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for age, x, s in live:
            u = age / (PUFF_LIFE * s)
            a = int(215 * (1 - u) ** 1.2)
            for j, (ox, oy, r) in enumerate(((0, -10, 16), (22, -18, 13), (-16, -16, 11), (12, -32, 9))):
                rr = r * (0.7 + 1.1 * u) * s
                cx = x - x0 + ox * (1 + u) * s + 40 * u
                cy = GY - y0 + oy * (1 + 0.8 * u) - 14 * u
                d.ellipse([cx - rr * 1.3, cy - rr, cx + rr * 1.3, cy + rr], fill=(232, 210, 164, a),
                          outline=(150, 112, 74, int(a * 0.55)), width=2)
        return im.filter(ImageFilter.GaussianBlur(0.8)), (x0, y0)

    sc.add_dynamic("dust", dust)
    sc.add("jonah_shadow", doc(C.ground_shadow(JX0, GY + 2, K, 130, 0.25)),
           motion=lambda t: Tf(dx=jpos(min(t, T_LEAP))[0] - JX0,
                               alpha=1 - M.progress(t, T_LEAP, T_LEAP + 0.2, "linear")))
    sc.add("jonah_land", jland, motion=jland_tf, frame_at=jland_frame)

    # coins: three on Jonah's open palm; one by one each hops UP out of his hand (about 60 px) and drops DOWN into
    # the captain's open palm, 45 px ahead of and 40 px above it. All coin layers are drawn above both figures.
    palm = (cap_palm[0] + PALM_OFF[0], cap_palm[1] + PALM_OFF[1])
    coin_rest = [(palm[0] - 9, palm[1] + 2, -8), (palm[0] + 9, palm[1] + 1, 10), (palm[0], palm[1] - 7, 2)]
    for i, (cx, cy, tilt) in enumerate(coin_rest):
        t_land = T_COIN_LAND + COIN_GAP * i

        def coin_palm_tf(t, t_land=t_land):
            if t < t_land or t >= T_TAKE:
                return Tf(alpha=0.0)
            return V.compose(ship_tf(t), cap_xy, dy=cap_dy(t) + 3 * bump(t, t_land, 0.15))

        sc.add(f"coin_palm{i}", doc(coin_svg(cx, cy, COIN_R, tilt)), motion=coin_palm_tf, wc=0.3)

    hand0 = (give[0] + HAND_OFF[0], give[1] + HAND_OFF[1])     # where the coins sit on Jonah's palm
    for i, (cx, cy, tilt) in enumerate(coin_rest):
        hand_c = (hand0[0] + (i - 1) * 8, hand0[1] - (i == 2) * 7)
        t0 = T_DROP + COIN_GAP * i
        t_land = t0 + COIN_FLY

        def coin_fly_tf(t, hand_c=hand_c, t0=t0, t_land=t_land, dst=(cx, cy), i=i):
            if t < T_GIVE or t >= t_land:
                return Tf(alpha=0.0)
            jt = jland_tf(t)                                # rides Jonah's hand while he holds them
            hx, hy = V.apply_tf(jt, hand_c[0] - (jpay - JX0), hand_c[1], (JX0, GY))
            if t < t0:
                return Tf(dx=hx - hand_c[0], dy=hy - hand_c[1])
            u = (t - t0) / (t_land - t0)
            b = V.compose(ship_tf(t), cap_xy, dy=cap_dy(t))
            ex, ey = V.apply_tf(b, *dst, cap_xy)
            x = M.lerp(hx, ex, u)
            y = M.lerp(hy, ey, u) - COIN_ARC * 4 * u * (1 - u)
            return Tf(dx=x - hand_c[0], dy=y - hand_c[1], rot=320 * u * (1 if i % 2 else -1),
                      px=hand_c[0], py=hand_c[1])

        sc.add(f"coin_fly{i}", doc(coin_svg(hand_c[0], hand_c[1], COIN_R, tilt)), motion=coin_fly_tf, wc=0.3)

    # ---------------------------------------------------------------- the narrator's question card with '？'
    def card_tf(t):
        if t < T_BUB or t >= T_POP + 0.25:
            return Tf(alpha=0.0)
        if t < T_POP:
            s_ = max(0.02, M.progress(t, T_BUB, T_BUB + 0.4, "back"))
            a = 1.0
        else:
            s_ = 1 + 0.18 * M.progress(t, T_POP, T_POP + 0.2)
            a = 1 - M.progress(t, T_POP + 0.04, T_POP + 0.24, "linear")
        return Tf(dy=-7 * math.sin(2 * math.pi * (t - T_BUB) / 2.2),
                  rot=2.0 * math.sin(2 * math.pi * (t - T_BUB) / 3.0), sx=s_, sy=s_, alpha=a,
                  px=QCARD[0], py=QCARD[1])

    def qmark_tf(t):
        b = card_tf(t)
        if b.alpha <= 0:
            return b
        rot = b.rot + 7 * math.sin(2 * math.pi * (t - T_BUB) / 1.5) * M.progress(t, T_BUB + 0.35, T_BUB + 0.9)
        return Tf(b.dx, b.dy, rot, b.sx, b.sy, b.alpha * M.progress(t, T_BUB + 0.14, T_BUB + 0.32, "linear"),
                  b.px, b.py)

    sc.add("qcard", qcard_svg(), motion=card_tf, wc=0.35)
    sc.add("qmark", qmark_svg(), motion=qmark_tf, wc=0)

    # butterfly by the signpost
    BFX, BFY = SIGN_X + 140, 820
    sc.add("butterfly", [doc(_butterfly(BFX, BFY, True)), doc(_butterfly(BFX, BFY, False))],
           frame_at=lambda t: float(int(t * 11) % 2), wc=0.4,
           motion=lambda t: Tf(dx=-60 * math.sin(t * 0.9) + 25 * math.sin(t * 2.3) - 90 * max(0.0, t - 3.2),
                               dy=-30 * math.sin(t * 1.3 + 0.5) - 12 * abs(math.sin(t * 5.5))
                               - 70 * max(0.0, t - 3.2)))
    # a second butterfly near the olive tree for the aside
    BX2, BY2 = JSTOP - 260, 800
    sc.add("butterfly2", [doc(_butterfly(BX2, BY2, True, "#f0a0a8")), doc(_butterfly(BX2, BY2, False, "#f0a0a8"))],
           frame_at=lambda t: float(int(t * 10) % 2), wc=0.4,
           motion=lambda t: Tf(dx=50 * math.sin(t * 0.8) + 20 * math.sin(t * 2.1),
                               dy=-26 * math.sin(t * 1.1 + 0.5) - 10 * abs(math.sin(t * 5.0))))

    # ---------------------------------------------------------------- foreground + gulls
    sc.add("foreground", foreground_svg())

    wing = (1, 0.5, 0, -0.5, -1, -0.5, 0, 0.5)

    def gull_layer(name, x, y, s, f, vx, vy, fps, phase, t0=0.0, t_vis=-1.0, dy_f=lambda t: 0.0):
        frames = [doc(PR.gull(x, y, s, f, wing=w)) for w in wing]
        sc.add(name, frames, frame_at=lambda t: float(int(t * fps + phase) % len(wing)),
               motion=lambda t: Tf(dx=vx * (t - t0), dy=vy * (t - t0) + 10 * math.sin(t * 1.7 + phase) + dy_f(t),
                                   alpha=1.0 if t >= t_vis else 0.0), wc=0.6)

    gull_layer("gull1", 5700, 300, 0.6, -1, -100, 2, 9, 0, dy_f=sky_dy)
    gull_layer("gull2", 3300, 350, 0.55, -1, -140, 3, 8, 3, t0=8.0)
    # flies off west, high above the masthead, as the captain points (enters from beyond the right edge)
    gull_layer("gull3", 3080, 150, 0.55, -1, -230, 0, 9, 5, t0=T_WEST - 2.0)

    # sparkles: the coins glint as they land in the captain's palm
    sc.fx.append(_glint_fx(lambda t: V.apply_tf(cap_tf(t), palm[0], palm[1] - 4, cap_xy), T_COIN_LAND,
                           T_TAKE + 0.02))
    sc.fx.append(_glint_fx(lambda t: V.apply_tf(jland_tf(t), hand0[0] - (jpay - JX0), hand0[1] - 4, (JX0, GY)),
                           T_GIVE + 0.05, T_DROP + 0.1, n=3))

    # ---------------------------------------------------------------- added last, so that every other layer keeps
    # its default watercolour seed; their z puts them where they belong
    # the ties are cast off as the haul starts: they slip down off the roll (riding it once it moves) and fade
    T_GASK0, T_GASK1 = T_SAIL - 0.08, T_SAIL + 0.1

    def gaskets_tf(t):
        if t < T_GASK0:
            return ship_tf(t)
        if t >= T_GASK1:
            return Tf(alpha=0.0)
        u = (t - T_GASK0) / (T_GASK1 - T_GASK0)
        drop = max(16 * u * u, (sail_edge_l(t) - V.SAIL_TOP_L) * K)
        return V.compose(ship_tf(t), ROLL_PIV, dy=drop, alpha=1 - M.progress(t, T_GASK0, T_GASK1, "sine"))

    sc.add("gaskets", gaskets_svg(), motion=gaskets_tf, wc=0.5, z=Z_ROLL + 0.1)
    # the coins in his closed fist: just behind the captain, so the fist covers their lower half and only gold
    # rims show above it (once the fist is at his chest they are behind his coat: tucked away)
    def fist_coins_svg(pose):
        fx, fy = C.hand_positions(captain_fig, *cap_xy, K, 1, pose=pose)[1]
        return doc(coin_svg(fx - 6, fy - 9, COIN_R * 0.9, -28) + coin_svg(fx + 6, fy - 11, COIN_R * 0.9, 24)
                   + coin_svg(fx, fy - 7, COIN_R * 0.9, 4))

    sc.add("fist_coins", [fist_coins_svg("grab"), fist_coins_svg("take_mid")], wc=0.3, z=Z_MAST - 0.6,
           frame_at=lambda t: 0.0 if t < T_TAKE_MID else 1.0,
           motion=lambda t: (V.compose(ship_tf(t), cap_xy, dy=cap_dy(t)) if T_TAKE <= t < T_TAKE_IN
                             else Tf(alpha=0.0)))
    # the cargo by Jonah's spot on the stern deck (s04's layout, see deck_cargo_svg): in front of him and behind
    # the ship's rail, as s04 draws it, so the two pictures match through the closing dissolve
    sc.add("deck_cargo_aft", deck_cargo_svg("aft"), motion=ship_tf, z=Z_FRONT - 0.5)

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=L2.start + 0.6, gain_db=-18, fade_in=0.8, fade_out=1.4)
    sc.sfx("waves_calm", L2.start - 1.0, dur=T - L2.start + 1.8, gain_db=-13, fade_in=1.6, fade_out=0.8)
    sc.sfx("birds", 0, dur=L2.start + 0.4, gain_db=-19, fade_in=0.8, fade_out=1.0, pan=0.3)
    sc.sfx("whoosh", T_TURN - 0.05, gain_db=-9, pan=0.2)
    sc.sfx("footsteps_run", LEG1_AT, dur=LEG1_DUR, gain_db=-9, fade_in=0.05, fade_out=0.25, rate=rate1)
    sc.sfx("whoosh", T_LOOKBACK - 0.12, gain_db=-16, pan=0.1)
    sc.sfx("pop", T_BUB, gain_db=-12)
    sc.sfx("pop", T_POP, gain_db=-15)
    sc.sfx("whoosh", T_TURN2 - 0.05, gain_db=-11, pan=0.0)
    sc.sfx("footsteps_run", LEG2_AT, dur=LEG2_DUR, gain_db=-9, fade_in=0.05, fade_out=0.25, rate=rate2)
    sc.sfx("gull", L2.start + 0.6, gain_db=-15, pan=-0.3)
    sc.sfx("ship_creak", L2.start + 1.0, dur=T - L2.start - 0.2, gain_db=-17, fade_in=1.0, fade_out=0.8)
    sc.sfx("gull", T_WEST + 0.3, gain_db=-17, pan=-0.5)
    sc.sfx("coins", T_COIN_LAND - 0.02, gain_db=-6)
    sc.sfx("thud", T_CRATE + 0.24, gain_db=-16, pan=0.3, duck_db=-5)     # on picture: heard over waves + score
    sc.sfx("whoosh", T_LEAP, gain_db=-13, pan=-0.1)
    sc.sfx("thud", T_LAND, gain_db=-13)
    sc.sfx("cloth", T_SAIL, gain_db=-13)
    sc.sfx("gull", T_DUCK + 0.4, gain_db=-17, pan=0.4)
    return sc


def _butterfly(x, y, open_, wing=None):
    k = 1.0 if open_ else 0.35
    wing = wing or P["gold"]
    return S.g(f'<ellipse cx="{f1(x - 9 * k)}" cy="{y - 6}" rx="{f1(11 * k)}" ry="9" fill="{wing}" '
               f'stroke="{P["ink"]}" stroke-width="2.2"/>'
               f'<ellipse cx="{f1(x + 9 * k)}" cy="{y - 6}" rx="{f1(11 * k)}" ry="9" fill="{S.shade(wing, 0.2)}" '
               f'stroke="{P["ink"]}" stroke-width="2.2"/>'
               f'<ellipse cx="{f1(x - 6 * k)}" cy="{y + 5}" rx="{f1(7 * k)}" ry="6" fill="{P["sun_hot"]}" '
               f'stroke="{P["ink"]}" stroke-width="2"/>'
               f'<ellipse cx="{f1(x + 6 * k)}" cy="{y + 5}" rx="{f1(7 * k)}" ry="6" fill="{P["sun_hot"]}" '
               f'stroke="{P["ink"]}" stroke-width="2"/>'
               f'<path d="M{x},{y - 12} L{x},{y + 10}" stroke="{P["ink"]}" stroke-width="3.2" stroke-linecap="round"/>'
               f'<path d="M{x},{y - 12} q-4,-10 -9,-12 M{x},{y - 12} q4,-10 9,-12" stroke="{P["ink"]}" '
               f'stroke-width="1.8" fill="none"/>', filter="wobble-fine")


def _glint_fx(pos_fn, t0, t1, n=5, seed=4):
    """Tiny gold four-point twinkles around a moving stage point (coins catching the sun)."""
    rng = random.Random(seed)
    pts = [(rng.uniform(-16, 16), rng.uniform(-18, 6), rng.uniform(0, 1), rng.uniform(7, 12)) for _ in range(n)]
    col = (255, 240, 180)

    def fx(frame, t, view):
        if not (t0 <= t <= t1):
            return frame
        env = min(1.0, (t - t0) / 0.12, (t1 - t) / 0.2)
        px, py = pos_fn(t)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ox, oy, ph, sz in pts:
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t / 0.7 + ph))
            if tw < 0.2:
                continue
            cx, cy = view.to_out(px + ox, py + oy)
            r = sz * view.scale * (0.5 + 0.6 * tw)
            a = int(235 * env * tw)
            w = r * 0.22
            g = r * 0.6
            d.ellipse([cx - g, cy - g, cx + g, cy + g], fill=(*col, a // 4))
            d.polygon([(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r),
                       (cx - w, cy + w), (cx - r, cy), (cx - w, cy - w)], fill=(*col, a))
        frame.alpha_composite(ov)
        return frame
    return fx
