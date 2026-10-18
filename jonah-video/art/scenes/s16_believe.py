"""Scene 16 — the people of Nineveh believe God (Jonah 3:5), v2.

"你猜怎么样？尼尼微的人听了，竟然都相信了上帝！ / 他们禁食，就是不吃饭。大人小孩都换上粗粗的麻布衣服，向上帝认错，
表示愿意改。"

One 2400 x 1350 stage: the market street of Nineveh that s15 ends in, in the late afternoon (s15's own houses,
palms, three striped stalls and skyline for the whole scene; Jonah on his stone step on the left, where s15's last
frame leaves him, stern; townspeople facing him), a herald (man variant 2 with his bronze horn at the hip, the same
man and horn as s17's horn-blower) on a stone plinth in front of the fruit stall, a market stall with bread,
pomegranates, dates and grapes on the right (merchant behind his table), a bread oven with soft smoke by the pot
stall, a well. Featured "from the greatest to the least": an elder with a stick, the merchant, a mother (woman
variant 2, as in s15) and her little girl.

  line 0  "你猜怎么样？"          calm: the people (still in bright robes) stand worried, facing a stern Jonah; a
                                  few turn to their neighbour; the camera pushes in gently.
          "尼尼微的人听了，"      faces turn thoughtful one after the other (hand to chin; the elder keeps his stick).
          "竟然都相信了上帝！"    the surprise: eyes go wide ('o'), Jonah is surprised too ("!"); on "相信" they lift
                                  their eyes to the sky (a lean back) as a warm golden patch of light opens in the sky
                                  above the crowd with a few big warm twinkles; on "上帝" they nod and lower their eyes
                                  (sorry). Jonah stays uneasy from here on (foreshadows ch. 4).
  line 1  (end of line 0)         the herald turns and blows his long bronze horn (toot marks; the sound ends with them);
          "他们禁食，"            he proclaims the fast (pointing, sound arcs); the little girl reaches for the bread;
                                  the merchant lifts a linen sheet by its corners behind him;
          "就是不吃饭。"          he throws it: a flat sheet flies forward and down and lands on the food (hard cut to
                                  the cloth moulded over it, small squash); she pulls her hand back and nods; the oven
                                  smoke dies away.
          "大人小孩都换上粗粗的麻布衣服，"  in burlap-coloured cloth-puffs the change runs across the square, grown-ups
                                  first and the little girl on "小孩"; they stand in sackcloth with bowed heads while the
                                  camera eases in a little; the girl wriggles and shrugs in the scratchy cloth (itch
                                  marks), her mother sighs.
          "向上帝认错，"          they kneel in a wave, palms together, eyes downcast, all turned to the right, toward the
                                  low sun and God's light (each goes down through a 4-frame one-knee in-between, the
                                  elder leaning on his stick, then leans it against his back; the five featured
                                  ones land tipped toward the light and rock back onto their heels); Jonah stands
                                  alone behind them;
          "表示愿意改。"          the solemn rosy dusk eases and a soft golden light with faint rays opens behind the
                                  cloud at the upper right, where they kneel facing (modest: s18's mercy is the big one);
                                  only the little girl's face turns peaceful (the grown-ups stay sorry - they do not yet
                                  know whether God will relent); the camera slowly settles on the whole kneeling square.
                                  Calm hold for the dissolve.

Hand-over from s15 (the 1 s cross-dissolve is the same moment in the same place): everything here is placed with
s15's final camera mapped onto camera A (m15). s15's street - its hazy skyline (far15) and its floor, back row of
houses, palms and three striped stalls (back15) - stays for the WHOLE scene: no backdrop is ever swapped or faded.
So do s15's clouds (they drift on gently; the right one drifts left over the low sun, where God's light later opens
behind it), its low sun (still turning) and its stone step under Jonah, who stands exactly where and as big as s15
leaves him. This scene's set pieces stand in front of that street and come in with the dissolve itself: the herald
on his plinth, the merchant's stall, the bread oven and the well. After the dissolve nothing fades: s15's
townspeople carry on by motion - the stroller and the boy at the fruit stall stay and listen (they are part of the
crowd from here on), the vendor leaves his pots and walks over behind Jonah, with two newcomers following him in
from the left edge, the bearded man walks off to the right with his two sheep trotting ahead, and two more groups hop
in from the right edge beside the merchant's stall, all before "尼尼微的人听了" ends. The mother, her little girl
and the elder (the same three people s15 ends on) start in s15's places and poses: the mother and the girl take
little steps forward to their places here, and the elder walks over in front of the square to Jonah's step
(planted-foot walk, s15's gait drawings with his stick) and stops on "竟然". s15's golden sky and warm light fade
slowly into this scene's sky before the golden patch on "相信", and s15's low sun stays at the upper right.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a squash-and-hop
or under a cloth-puff; expression-only changes are cuts as well. Crowd groups bow with a small vertical squash (no
rotation, so far figures keep their feet on the ground). All times come from the narration chunks (fractions only
inside one chunk). Puff, smoke, dove and light layers are small or only active briefly (render budget).
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from art.scenes import s15_city as S15
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 2400, 1350
INK = P["ink"]

# ------------------------------------------------------------------ the hand-over from s15
# s15's last frame (camera Cam(2228.4, 981, 1680): its market end, after its slow settle) and this scene's camera A
# (Cam(1105, 745, 1900)) show the same square at the same moment: s15 stage -> s16 stage is a scale and a shift.
M15_O15 = (1388.4, 508.5)        # top-left of s15's last frame (s15 stage px)
M15_O16 = (155.0, 210.625)       # top-left of camera A (s16 stage px)
M15_K = 1900 / 1680              # s15 stage px -> s16 stage px
M15_TF = (f"translate({M15_O16[0]},{M15_O16[1]}) scale({M15_K:.6f}) "
          f"translate({-M15_O15[0]},{-M15_O15[1]})")
T15 = 18.3                       # s15's duration: its sun, clouds and parallax as its last frame shows them
S15_CAM_X = 2228.4               # s15's final camera centre x (for its parallax layers)


def m15(x, y):
    """s15 stage point -> s16 stage point."""
    return M15_O16[0] + (x - M15_O15[0]) * M15_K, M15_O16[1] + (y - M15_O15[1]) * M15_K


# where s15's last frame leaves the three featured townspeople (s15 stage: feet, scale; all face Jonah)
S15_ELDER, S15_MOTHER, S15_GIRL = (2590, 1346, 0.84), (2330, 1352, 0.86), (2440, 1372, 0.86)
# the other people and animals in s15's last frame (s15 stage: kind, variant, feet, scale, facing, pose, expr)
S15_VENDOR = ("man", 2, 1395, 1188, 0.6, 1, "listen", None)            # the vendor by his pots
S15_STROLLER = ("man", 1, 2080, 1214, 0.62, -1, "listen", None)        # the stroller
S15_BOY = ("child", 2, 2250, 1200, 0.62, -1, "stand", "surprised")     # the boy at the fruit stall
S15_BEARD = ("man", 0, 2700, 1400, 0.9, -1, "listen", None)            # the bearded man on the right
S15_SHEEP = [(2760, 1420, 0.68, 160), (2960, 1430, 0.6, 140)]
PAR15 = S15_CAM_X - 1100                     # s15's parallax layers follow its camera
S15_CLOUD_DX = 9 * T15 + 0.6 * PAR15         # its clouds' drift + parallax at its last frame
S15_CLOUDS = [(640, 600, 250, 70, 31), (1420, 578, 210, 60, 33), (2250, 612, 270, 76, 35)]   # (two more lie
#                                                                                   off this stage to the right)
CLOUD_R0 = m15(S15_CLOUDS[2][0] + S15_CLOUD_DX, S15_CLOUDS[2][1])   # its right cloud (it drifts over the sun)
FG15_DX = -0.22 * (S15_CAM_X - (S15.STEP_X - 58 + 0.27 * 1720))   # s15's near things at its last frame
# s15's sun at its last frame: sun_pos(T) (camera-relative arc) and its slow spin (3 deg/s)
S15_SUN = (S15_CAM_X + 660, 981 - 1680 * 9 / 32 + 92 + 0.00017 * 660 ** 2)
S15_SUN_ROT = 3.0 * T15
S15_GOLD = "#fff6e6"             # s15's late-afternoon light (light_fx multiplies the frame by 255, 246, 230)

# ------------------------------------------------------------------ layout (stage px)
# s15's street mapped here: its house fronts stand on y ~902, its stalls' fronts on ~965; the floor runs below
SKY_BOT = 960               # the skies reach down behind the houses (narrow gaps between them show sky to ~870)
# Jonah stands on s15's stone step (s15's step_svg placed with m15), exactly where and as big as s15 leaves him
J_X, J_Y = m15(S15.STEP_X - 58, S15.STEP_TOP)
J_S = S15.JS * M15_K
# the herald's plinth stands on the street in front of s15's fruit stall (drawn around (1250, 846) at scale 1 and
# placed with PLINTH_K)
PLINTH_X, PLINTH_BASE, PLINTH_K = 1290, 992, 1.18
PLINTH_TOP = PLINTH_BASE - 68 * PLINTH_K
H_X, H_S = PLINTH_X, 0.72
# the market stall is drawn in local coordinates (designed around x 1420.., table front edge y 1110) and placed
# with TABLE_K / TABLE_ORG
TABLE_K = 1.08
TABLE_ORG = (1444, 1128)    # stage position of the local point (1420, 1110) = the table's front-left corner


def tpt(lx, ly):
    """Local stall point -> stage."""
    return TABLE_ORG[0] + (lx - 1420) * TABLE_K, TABLE_ORG[1] + (ly - 1110) * TABLE_K


def tplace(body):
    return (f'<g transform="translate({TABLE_ORG[0]},{TABLE_ORG[1]}) scale({TABLE_K}) translate(-1420,-1110)">'
            f'{body}</g>')


TABLE_X0, TABLE_X1, TABLE_TOP, TABLE_BACK = 1420, 1890, 1110, 1080   # (local) table front edge / back edge
TABLE_FLOOR = 1215
R_X, R_Y, R_S = tpt(1740, 1160)[0], tpt(1740, 1160)[1], 1.06   # merchant, behind his table
E_X, E_Y, E_S = 800, 1232, 1.12    # elder
W_X, W_Y, W_S = 1000, 1245, 1.12   # mother (left of the boy at the fruit stall, clear of the herald's plinth)
K_X, K_Y, K_S = 1392, 1240, 1.12   # her little girl
# the bread oven (drawn around (300, 784) at scale 1) stands on the street in front of s15's pot stall
OVEN_X, OVEN_Y, OVEN_K = 330, 978, 1.18
OVEN_TOP = OVEN_Y - 80 * OVEN_K


def s15_person(kind, v, x, y, s, fc, pose, expr):
    """(s15 stage) -> its place here: (kind, variant, x, y, scale, facing, pose, expr)."""
    return (kind, v) + m15(x, y) + (s * M15_K, fc, pose, expr)


VENDOR, STROLLER, BOY, BEARD = (s15_person(*p) for p in (S15_VENDOR, S15_STROLLER, S15_BOY, S15_BEARD))
# The vendor walks over from his pots to stand behind Jonah, two newcomers following him in from the left edge
# (one rigid group: planted-foot walk drawings, WALK_NL drawings of WALK_ADV px each)
WALK_NL = 42
WALK_D = 820 - VENDOR[2]                 # he stops at x 820
WALK_ADV = WALK_D / WALK_NL

CROWD = {   # (kind, variant, x, y, scale, facing in line 0, facing when kneeling)
    # everyone faces Jonah (left) while they listen; they kneel facing right, toward God's light (upper right)
    # the walkers (drawn where they stop): the vendor and the two newcomers (off the left edge when he sets off)
    "walk_l": [("man", 3, 820 - 160, 988, 0.69, -1, 1), ("woman", 0, 820 - 80, 984, 0.69, -1, 1),
               ("man", 2, 820, VENDOR[3], VENDOR[4], -1, 1)],
    # s15's stroller and the boy at the fruit stall, where s15 leaves them
    "c15": [("man", 1) + STROLLER[2:5] + (-1, 1), ("child", 2) + BOY[2:5] + (-1, 1)],
    # newcomers hopping in from the right edge, beside the merchant's stall
    "back_r": [("man", 0, 2076, 996, 0.7, -1, 1), ("child", 0, 2146, 1002, 0.7, -1, 1),
               ("elder", 1, 2214, 994, 0.7, -1, 1), ("woman", 3, 2290, 998, 0.7, -1, 1)],
    "mid_r": [("woman", 1, 2060, 1094, 0.83, -1, 1), ("man", 3, 2164, 1088, 0.83, -1, 1),
              ("elder", 2, 2268, 1098, 0.83, -1, 1)],
}
GLOW_C = (1880, 330)        # God's warm light opens here (upper right, behind s15's right cloud, over the low sun)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ s15's picture, placed with m15


def split15(d):
    """An s15 SVG document -> (its own defs, its body), without the shared filters (this doc has them)."""
    head = d.index(">") + 1
    inner = d[head:d.rindex("</svg>")]
    k = inner.index("</defs>")
    defs = inner[len("<defs>"):k].replace(S._filters(), "", 1)
    return defs, inner[k + len("</defs>"):]


def place15(*items):
    """Markup in s15 stage coordinates (s15 documents or plain markup) -> one s16 document, placed with m15."""
    defs, body = "", ""
    for it in items:
        if it.startswith("<svg"):
            d, b = split15(it)
            defs += d
            body += b
        else:
            body += it
    return doc(f'<g transform="{M15_TF}">{body}</g>', defs)


def sun15_markup():
    """s15's low sun as its last frame shows it (rays turned by its slow spin)."""
    defs, body = split15(S15.sun_svg(*S15_SUN))
    return defs, f'<g transform="rotate({S15_SUN_ROT:.2f} {f1(S15_SUN[0])} {f1(S15_SUN[1])})">{body}</g>'


def glow15_markup(cx, cy, r, blend):
    """s15's warm 'screen' glow around the low sun (glow_image: alpha (1-d)^2.2 x 0.6, colour 255,214,140)."""
    stops = "".join(f'<stop offset="{d}" stop-color="#ffd68c" stop-opacity="{0.6 * (1 - d) ** 2.2:.3f}"/>'
                    for d in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
    defs = f'<radialGradient id="s16g15">{stops}</radialGradient>'
    style = ' style="mix-blend-mode:screen"' if blend else ""
    return defs, f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="url(#s16g15)"{style}/>'


def far15_svg():
    """s15's hazy far skyline (with its parallax as its last frame shows it); s15's sun glow lies over it."""
    return place15(f'<g transform="translate({0.4 * PAR15:.1f},0)">', S15.street_far_svg(), "</g>")


def back15_svg():
    """s15's street for the whole scene: its floor, the back row of flat-roofed houses, palms, doorstep props and
    the three striped stalls (pots, fruit, cloth), as its last frame shows them."""
    return place15(S15.street_back_svg())


def clouds15_svg(items):
    """Some of s15's clouds, where its last frame shows them."""
    return place15(f'<g transform="translate({S15_CLOUD_DX:.1f},0)">', S15.pano_clouds_svg(items), "</g>")


def fg15_markup():
    """s15's near things along the bottom edge (the flowering bush and grass at the lower right; its jars at the
    left lie off this stage's frames) as (defs, body) in this stage's coordinates."""
    d, b = split15(S15.street_fg_svg())
    return d, f'<g transform="{M15_TF}"><g transform="translate({FG15_DX:.2f},0)">{b}</g></g>'


def s15_fig_markup(kind, v, x, y, s, fc, pose, expr, dx=0.0):
    """A townsperson exactly as s15's last frame draws them (its own shadow and drawing, in s15 coordinates placed
    with m15), optionally shifted by dx stage px (for a layer that is drawn where its group ends up)."""
    x15, y15 = (x - M15_O16[0]) / M15_K + M15_O15[0], (y - M15_O16[1]) / M15_K + M15_O15[1]
    s15 = s / M15_K
    body = (C.ground_shadow(x15, y15, s15, 80 if kind == "child" else 110)
            + C.citizen(x15, y15, s15, fc, kind=kind, variant=v, pose=pose, expr=expr))
    return f'<g transform="translate({dx:.2f},0) {M15_TF}">{body}</g>'


def sheep15_markup(facing):
    """s15's two sheep in front of the bearded man (facing -1 as s15 leaves them, or +1 to trot off)."""
    body = ""
    for x, y, s, w in S15_SHEEP:
        body += C.ground_shadow(x, y, s, w) + PR.animal(x, y, s, facing, kind="sheep")
    return f'<g transform="{M15_TF}">{body}</g>'


def step15_svg():
    """s15's two-tier stone step with its glazed rosette band, where s15 leaves Jonah standing on it."""
    return place15(S15.step_svg())


def sky15_svg():
    """s15's golden late-afternoon sky (street_sky_eve: the same stops, its gradient span mapped with m15)."""
    y0, y1 = m15(0, 470)[1], m15(0, 1000)[1]
    stops = [(0, S.mix(S.mix(P["sky_dawn"], P["sky_warm"], 0.5), "#fff4e2", 0.3)),
             (0.45, S.mix(P["sky_warm"], P["sky_dawn"], 0.35)),
             (0.8, S.mix(P["sky_warm"], P["gold"], 0.3)), (1, S.mix(P["sky_warm"], P["gold"], 0.45))]
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    defs = (f'<linearGradient id="s16sky15" gradientUnits="userSpaceOnUse" x1="0" y1="{f1(y0)}" x2="0" '
            f'y2="{f1(y1)}">{st}</linearGradient>')
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SKY_BOT + 20}" fill="url(#s16sky15)"/>', defs)


def sun15_svg():
    sdefs, sun = sun15_markup()
    return doc(f'<g transform="{M15_TF}">{sun}</g>', sdefs)


def glow15_svg():
    cx, cy = m15(*S15_SUN)
    gdefs, glow = glow15_markup(cx, cy, 430 * M15_K, False)
    return doc(glow, gdefs)


# ------------------------------------------------------------------ timing helpers


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval so no frame is ambiguous."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    """[(t, idx), ...] -> frame_at with HARD cuts (integer frame indices, never a crossfade)."""
    entries = sorted(entries)

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


def hop(t0, keys, pivot, curves="sine"):
    """Additive keyed bump around t0: keys [(dt, {...})] that start and end at identity."""
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


def dip(tc, s, pv, depth=8, squash=0.955):
    """Squash-and-hop that hides a pose cut at tc (the cut happens at the bottom of the squash)."""
    return hop(tc, [(-0.16, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": squash}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pv, ["in", "out", "sine"])


HALF_HOLD = 4 / 30          # the one-knee in-between of kneeling down is held 4 frames (as s09's sailors)
KNEEL_TILT = 5.5            # the kneel starts tipped this far toward the light, then rocks upright (kneel_down)


def kneel_down(ta, pv, heights, tilt=0.0, vertical_only=False):
    """Kneeling down through the one-knee in-between (cuts at ta and ta + HALF_HOLD), a squash about the ground
    line, so feet and knees stay planted: the standing figure sinks until its head top is where the half-kneel's
    is; the half-kneel sinks on a little for its few frames; the kneeling drawing starts with its head where the
    half-kneel's ended and settles onto its knees with a soft landing squash.
    heights: head-top heights above the ground of the (standing, half-kneel, kneeling) drawings.
    tilt: degrees (+ = toward facing +1) the kneeling drawing starts tipped forward about the ground pivot, rocking
    upright over its first 0.24 s: the half-kneel leans its head well forward of where the kneel's sits, so the
    kneel picks the head up part of the way forward and the rest is a rock back onto the heels, not a snap (the
    knees, at the pivot, stay put). For one figure on its own layer, with the pivot under its knees.
    vertical_only: no widening with the squash (crowd layers: members far from the group pivot would slide)."""
    hs, hh, hk = heights
    tb = ta + HALF_HOLD
    r1 = hh / hs                                 # standing, squashed down to the half-kneel's head height
    r2 = 1 - 0.35 * (1 - hk / hh)                # the half-kneel sinks a third of the way toward the kneel
    r3 = hh * r2 / hk                            # the kneel starts where the half-kneel ended ...
    settle = 0.985                               # ... and lands with a small squash
    e_in, e_out, e_sine = M.ease("in"), M.ease("out"), M.ease("sine")
    ROCK = 0.24

    def m(t):
        if ta - 0.18 <= t < ta:
            sy = 1 + (r1 - 1) * e_in((t - ta + 0.18) / 0.18)
        elif ta <= t < tb:
            sy = 1 + (r2 - 1) * e_sine((t - ta) / HALF_HOLD)
        elif tb <= t < tb + 0.12:
            sy = r3 + (settle - r3) * e_out((t - tb) / 0.12)
        elif tb + 0.12 <= t < tb + 0.32:
            sy = settle + (1 - settle) * e_sine((t - tb - 0.12) / 0.2)
        else:
            sy = 1.0
        rot = tilt * (1 - e_sine((t - tb) / ROCK)) if tb <= t < tb + ROCK else 0.0
        return Tf(sx=1.0 if vertical_only else 1 + 0.35 * (1 - sy), sy=sy, rot=rot, px=pv[0], py=pv[1])
    return m


def nod(t0, pv, deg=3.0, n=2, period=0.42, facing=-1):
    """Gentle nods: the whole figure bows a little forward (toward ``facing``) from the feet, n times."""
    ks = [(0, {"rot": 0})]
    for i in range(n):
        ks += [(i * period + period * 0.45, {"rot": deg * facing}), ((i + 1) * period, {"rot": 0})]
    return hop(t0, ks, pv)


def look_up(t0, pv, facing=-1, deg=5.0, rise=7, hold=0.55):
    """Lift the eyes to the sky for a moment: the figure leans back a little (away from ``facing``) and rises."""
    return hop(t0, [(0, {"rot": 0, "dy": 0}), (0.22, {"rot": -deg * facing, "dy": -rise}),
                    (0.22 + hold, {"rot": -deg * facing * 0.8, "dy": -rise * 0.8}),
                    (0.5 + hold, {"rot": 0, "dy": 0})], pv)


def bow(t0, pv, amt=0.014, n=2, period=0.42):
    """A crowd group's nods: a small vertical squash from the ground line (no rotation, so the feet of figures
    far from the pivot stay on the ground)."""
    ks = [(0, {"sy": 1})]
    for i in range(n):
        ks += [(i * period + period * 0.45, {"sy": 1 - amt}), ((i + 1) * period, {"sy": 1})]
    return hop(t0, ks, pv)


def breathe_y(amount, period, pivot, phase=0.0):
    """Breathing as a vertical-only scale about the ground line (for wide crowd layers)."""
    return lambda t: Tf(sy=1 + amount * math.sin(2 * math.pi * (t / period + phase)), px=pivot[0], py=pivot[1])


def step_in(t0, frm, pivot, s_to, n=2, dur=0.32, gap=0.05, lift=9.0):
    """Little hop-steps from frm = (x, y, scale) (where s15 leaves a figure) to its place here (the drawing's own
    anchor ``pivot``, drawn at scale ``s_to``): n low hops, each stretching a little in the air and squashing as it
    lands; identity afterwards."""
    x0, y0, s0 = frm
    k0 = s0 / s_to

    def m(t):
        f, arc, sq = 0.0, 0.0, 1.0
        for i in range(n):
            ta = t0 + i * (dur + gap)
            if t < ta:
                break
            if t >= ta + dur:
                f = (i + 1) / n
                continue
            u = (t - ta) / dur
            a = min(1.0, u / 0.8)                 # in the air for 80% of the hop, then the landing squash
            f = (i + M.ease("sine")(a)) / n
            arc = lift * s_to * math.sin(math.pi * a)
            sq = 1 + 0.03 * math.sin(math.pi * a) - 0.045 * math.sin(math.pi * max(0.0, (u - 0.8) / 0.2))
            break
        k = k0 + (1 - k0) * f
        return Tf(dx=(x0 - pivot[0]) * (1 - f), dy=(y0 - pivot[1]) * (1 - f) - arc, sx=k / math.sqrt(sq),
                  sy=k * sq, px=pivot[0], py=pivot[1])
    return m


def gait_fig(x, y, s, kind, variant, facing, ps, expr="worried"):
    """A townsperson (same design as C.citizen) in one of s15's planted-foot walk drawings; an elder walks a little
    stooped with his stick in his near hand, as C.citizen draws him walking."""
    D = C._citizen_design(kind, variant, "normal")
    m = {"child": C._CHILD, "woman": C._metrics(C._ADULT, 0.96, 0.92),
         "elder": C._metrics(C._ADULT, 0.97, 1.0)}.get(kind, C._ADULT)
    ps = dict(ps)
    if kind == "elder":
        ps["t"] = ps["t"] + 8
        ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
        D["front"] = C._cane
    inner, _ = C._figure(D, m, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"{kind}{variant}-gait16")


def leg_k(kind):
    m = {"child": C._CHILD, "woman": C._metrics(C._ADULT, 0.96, 0.92),
         "elder": C._metrics(C._ADULT, 0.97, 1.0)}.get(kind, C._ADULT)
    return (m["th"] + m["sh"]) / (C._ADULT["th"] + C._ADULT["sh"])


# the in-between of kneeling down (s09's one-knee drawing): the near knee on the ground, the far foot planted in
# front, the hands open on their way from hanging at the sides to the palms-together of the kneel, head bowed
HALF_KNEEL = dict(C.POSES["kneel_pray"], t=6, h=12, legs=((70, 8), (2, -90)), arms=(("fk", 20, 40), ("fk", 10, 30)),
                  hands=("open", "open"))


def half_kneel_fig(x, y, s, kind, variant, facing, attire="sackcloth", expr="sorry"):
    """A townsperson (same design as C.citizen) in the half-kneel in-between, anchored like the kneel (under the
    hips); an elder lowers himself leaning on his stick, gripped in his trailing near hand so that it stands where
    his standing drawing holds it (x about -45 from the anchor, toward his heels) and the kneel then only tips it
    back against his shoulder. Returns (markup, {'head_top', 'pelvis'} in stage px)."""
    D = C._citizen_design(kind, variant, attire)
    m = {"child": C._CHILD, "woman": C._metrics(C._ADULT, 0.96, 0.92),
         "elder": C._metrics(C._ADULT, 0.97, 1.0)}.get(kind, C._ADULT)
    ps = dict(HALF_KNEEL)
    if kind == "elder":
        ps["arms"] = (ps["arms"][0], ("fk", -25, -15))
        ps["hands"] = (ps["hands"][0], "fist")
        D["front"] = C._cane
    f = C._fsign(facing)
    inner, _ = C._figure(D, m, ps, expr, f, True)
    pts = {k: (x + C._LAST[k][0] * s * f, y + C._LAST[k][1] * s) for k in ("head_top", "pelvis")}
    return C._wrap_out(inner, x, y, s, facing, f"{kind}{variant}-half16"), pts


def kneel_heights(kind, variant):
    """Head-top heights above the ground (scale 1) of a townsperson's standing 'sad' sackcloth drawing, the
    half-kneel and the kneel (for kneel_down)."""
    def top(pose):
        return -C.body_points(C.citizen, 0, 0, 1.0, 1, kind=kind, variant=variant, pose=pose,
                              attire="sackcloth")["head_top"][1]
    return top("sad"), -half_kneel_fig(0, 0, 1.0, kind, variant, 1)[1]["head_top"][1], top("kneel_pray")


# ============================================================================ backgrounds


def sky_svg():
    defs = (S.lin_grad("s16sky", [(0, "#a9c3d8"), (0.34, "#cfd5d6"), (0.62, "#f1dcb6"), (0.9, "#f7cf9a"),
                                  (1, "#f6c58e")]) +
            S.rad_grad("s16sun", [(0, "#fff6d6", 1), (0.18, "#ffe9b0", 0.9), (0.5, "#ffd793", 0.35),
                                  (1, "#ffcf88", 0)]))
    body = (f'<rect x="-20" y="800" width="{SW + 40}" height="{SKY_BOT - 780}" fill="#f6c58e"/>'
            f'<rect x="-20" y="-20" width="{SW + 40}" height="830" fill="url(#s16sky)"/>'
            f'<ellipse cx="2080" cy="560" rx="820" ry="560" fill="url(#s16sun)"/>')
    return doc(body, defs)


def plinth_svg():
    """The herald's plinth: a two-tier stone block with a glazed rosette band, on the street in front of s15's fruit
    stall (drawn around (1250, 846) and placed with PLINTH_K at (PLINTH_X, PLINTH_BASE))."""
    defs = (S.lin_grad("s16stone", [(0, "#ead3a6"), (1, "#d2b07c")]) +
            S.lin_grad("s16stonef", [(0, "#cda874"), (1, "#b48f5d")]))
    px, pt, pb = 1250, 778, 846
    l0, l1, u0, u1 = px - 130, px + 130, px - 92, px + 92
    pl = (f'<path d="M{l0},{pb} L{l0},{pb - 42} L{l1},{pb - 42} L{l1},{pb} Z" fill="url(#s16stonef)" '
          f'stroke="{INK}" stroke-width="3.5"/>'
          f'<path d="M{l0},{pb - 42} L{l0 + 16},{pb - 54} L{l1 + 16},{pb - 54} L{l1},{pb - 42} Z" '
          f'fill="url(#s16stone)" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
          f'<path d="M{u0},{pb - 48} L{u0},{pt + 6} L{u1},{pt + 6} L{u1},{pb - 48} Z" fill="url(#s16stonef)" '
          f'stroke="{INK}" stroke-width="3"/>'
          f'<path d="M{u0},{pt + 6} L{u0 + 12},{pt - 6} L{u1 + 12},{pt - 6} L{u1},{pt + 6} Z" '
          f'fill="url(#s16stone)" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
          f'<rect x="{l0}" y="{pb - 30}" width="{l1 - l0}" height="16" fill="#3f79a8" stroke="{INK}" '
          f'stroke-width="2.5"/>')
    pl += "".join(f'<circle cx="{xx}" cy="{pb - 22}" r="4" fill="#f3e3b8"/>' for xx in range(l0 + 14, l1, 26))
    body = (f'<ellipse cx="{px + 10}" cy="{pb + 4}" rx="160" ry="13" fill="{INK}" opacity="0.14" filter="url(#soft)"/>'
            + S.g(pl, filter="wobble-fine"))
    return doc(f'<g transform="translate({PLINTH_X},{PLINTH_BASE}) scale({PLINTH_K}) translate({-px},{-pb})">'
               f'{body}</g>', defs)


def oven_svg():
    """A clay bread oven (tannur) with a jar and a sack, on the street in front of s15's pot stall (drawn around
    (300, 784) and placed with OVEN_K at (OVEN_X, OVEN_Y)); its smoke is a separate layer."""
    ox, oy = 300, 784
    oven = (f'<path d="M{ox - 46},{oy} C{ox - 50},{oy - 50} {ox - 30},{oy - 78} '
            f'{ox - 14},{oy - 80} L{ox + 14},{oy - 80} C{ox + 30},{oy - 78} '
            f'{ox + 50},{oy - 50} {ox + 46},{oy} Z" fill="#c9845a" stroke="{INK}" '
            f'stroke-width="3.5" stroke-linejoin="round"/>'
            f'<ellipse cx="{ox}" cy="{oy - 80}" rx="16" ry="5" fill="#6d4630" stroke="{INK}" '
            f'stroke-width="3"/>'
            f'<path d="M{ox - 18},{oy} L{ox - 18},{oy - 26} A18,18 0 0 1 {ox + 18},'
            f'{oy - 26} L{ox + 18},{oy} Z" fill="#7a4a30" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{ox - 12},{oy - 4} Q{ox},{oy - 22} {ox + 12},{oy - 4}" '
            f'fill="#f2a24c" opacity="0.85"/>')
    oven += PR.jar(ox + 74, oy - 26, 0.36) + PR.sack(ox - 80, oy + 4, 0.34, seed=2)
    body = (f'<ellipse cx="{ox}" cy="{oy + 3}" rx="70" ry="9" fill="{INK}" opacity="0.14" filter="url(#soft)"/>'
            + S.g(oven, filter="wobble-fine"))
    return doc(f'<g transform="translate({OVEN_X},{OVEN_Y}) scale({OVEN_K}) translate({-ox},{-oy})">{body}</g>')


def well_svg(cx, by):
    """A round stone well in the front-left corner of the square, with a bucket on its rim."""
    rx, ry, h = 138, 34, 92
    ry0 = by - h
    stone, light, dark = "#d9bb8b", "#ead2a8", "#b89466"
    body = (f'<ellipse cx="{cx}" cy="{by + 6}" rx="{rx + 30}" ry="20" fill="{INK}" opacity="0.15" '
            f'filter="url(#soft)"/>')
    wall = (f'M{cx - rx},{ry0} L{cx - rx},{by} A{rx},{ry} 0 0 0 {cx + rx},{by} L{cx + rx},{ry0} '
            f'A{rx},{ry} 0 0 1 {cx - rx},{ry0} Z')
    cid = "s16well"
    courses = ""
    for k in range(1, 4):
        yy = ry0 + h * k / 4
        courses += f'<path d="M{cx - rx},{f1(yy)} A{rx},{ry} 0 0 0 {cx + rx},{f1(yy)}"/>'
        for j in range(7):
            u = (j + (0.5 if k % 2 else 0)) / 7
            xx = cx - rx + 2 * rx * u
            yb = yy + ry * math.sqrt(max(0, 1 - ((xx - cx) / rx) ** 2))
            courses += f'<path d="M{f1(xx)},{f1(yb)} l0,{f1(-h / 4)}"/>'
    body += (f'<clipPath id="{cid}"><path d="{wall}"/></clipPath><path d="{wall}" fill="{stone}"/>'
             f'<g clip-path="url(#{cid})"><path d="M{cx + 30},{ry0} L{cx + rx + 10},{ry0} L{cx + rx + 10},'
             f'{by + ry} L{cx + 50},{by + ry} Z" fill="{dark}" opacity="0.35"/>'
             f'<g stroke="{S.shade(stone, -0.3)}" stroke-width="2.5" fill="none" opacity="0.55">{courses}</g></g>'
             f'<path d="{wall}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    body += (f'<ellipse cx="{cx}" cy="{ry0}" rx="{rx}" ry="{ry}" fill="{light}" stroke="{INK}" stroke-width="4"/>'
             f'<ellipse cx="{cx}" cy="{ry0 + 3}" rx="{rx - 24}" ry="{ry - 10}" fill="#3e6170" stroke="{INK}" '
             f'stroke-width="3"/><ellipse cx="{cx - 30}" cy="{ry0 + 1}" rx="40" ry="6" fill="#8fbcc4" opacity="0.6"/>')
    # wooden bucket and a coil of rope on the rim
    bx, bt = cx + 70, ry0 - 50
    body += (f'<path d="M{bx - 26},{bt} L{bx + 26},{bt} L{bx + 20},{bt + 50} L{bx - 20},{bt + 50} Z" '
             f'fill="{P["wood_light"]}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<path d="M{bx - 24},{bt + 12} L{bx + 24},{bt + 12} M{bx - 21},{bt + 38} L{bx + 21},{bt + 38}" '
             f'stroke="{P["wood_dark"]}" stroke-width="5"/>'
             f'<path d="M{bx - 22},{bt + 2} Q{bx},{bt - 34} {bx + 22},{bt + 2}" stroke="{INK}" stroke-width="3.5" '
             f'fill="none"/>')
    body += PR.rope_coil(cx - 70, ry0 + 8, 0.55)
    return S.g(body, filter="wobble-fine")


# ============================================================================ the market stall


def stall_back_svg():
    """Back posts of the stall (behind the merchant)."""
    body = ""
    for x, y0, y1 in ((TABLE_X0 + 44, 760, TABLE_BACK + 6), (TABLE_X1 + 40, 752, TABLE_BACK + 6)):
        body += (f'<path d="M{x},{y0} L{x},{y1}" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
                 f'<path d="M{x},{y0} L{x},{y1}" stroke="{P["wood"]}" stroke-width="10" stroke-linecap="round"/>')
    return doc(S.g(tplace(body), filter="wobble-fine"))


def bread(cx, cy, r):
    return (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(r)}" ry="{f1(r * 0.36)}" fill="#e2a862" stroke="{INK}" '
            f'stroke-width="3"/><ellipse cx="{f1(cx - r * 0.1)}" cy="{f1(cy - r * 0.08)}" rx="{f1(r * 0.62)}" '
            f'ry="{f1(r * 0.18)}" fill="#f0c483" opacity="0.8"/>'
            + "".join(f'<circle cx="{f1(cx + dx * r)}" cy="{f1(cy + dy * r)}" r="2.2" fill="#9c5f2f"/>'
                      for dx, dy in ((-0.4, -0.05), (0.05, 0.02), (0.35, -0.06), (-0.12, 0.12))))


def basket(cx, by, w, h, fill="#c99a5a"):
    """Woven basket, bottom centre (cx, by)."""
    body = (f'<path d="M{f1(cx - w / 2)},{f1(by - h)} L{f1(cx + w / 2)},{f1(by - h)} L{f1(cx + w / 2 - 10)},{f1(by)} '
            f'L{f1(cx - w / 2 + 10)},{f1(by)} Z" fill="{fill}" stroke="{INK}" stroke-width="3.5" '
            f'stroke-linejoin="round"/>')
    weave = ""
    for i in range(1, 4):
        yy = by - h * i / 4
        weave += f'<path d="M{f1(cx - w / 2 + 6)},{f1(yy)} L{f1(cx + w / 2 - 6)},{f1(yy)}"/>'
    for i in range(1, 8):
        xx = cx - w / 2 + w * i / 8
        weave += f'<path d="M{f1(xx)},{f1(by - h + 3)} L{f1(xx - 3)},{f1(by - 3)}"/>'
    body += f'<g stroke="{S.shade(fill, -0.35)}" stroke-width="2" opacity="0.7" fill="none">{weave}</g>'
    body += (f'<path d="M{f1(cx - w / 2 - 3)},{f1(by - h)} L{f1(cx + w / 2 + 3)},{f1(by - h)}" stroke="{INK}" '
             f'stroke-width="9" stroke-linecap="round"/><path d="M{f1(cx - w / 2 - 3)},{f1(by - h)} '
             f'L{f1(cx + w / 2 + 3)},{f1(by - h)}" stroke="{S.shade(fill, 0.2)}" stroke-width="4" '
             f'stroke-linecap="round"/>')
    return body


def fruit(cx, cy, r, col, crown=False):
    out = (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="3"/>'
           f'<circle cx="{f1(cx - r * 0.35)}" cy="{f1(cy - r * 0.35)}" r="{f1(r * 0.25)}" fill="#fff1d8" '
           f'opacity="0.55"/>')
    if crown:
        out += (f'<path d="M{f1(cx - 5)},{f1(cy - r + 2)} l2,-9 l3,6 l3,-6 l2,9 Z" fill="{S.shade(col, -0.2)}" '
                f'stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
    return out


def table_svg():
    """The market table with bread, pomegranates, dates and grapes, and its front cloth skirt."""
    x0, x1, yt, yb = TABLE_X0, TABLE_X1, TABLE_TOP, TABLE_BACK
    top = (f'<path d="M{x0},{yt} L{x0 + 40},{yb} L{x1 + 40},{yb} L{x1},{yt} Z" fill="#b98352" stroke="{INK}" '
           f'stroke-width="4" stroke-linejoin="round"/>')
    goods = ""
    # bread basket (left)
    goods += basket(1505, 1102, 128, 40)
    for i, (dx, dy) in enumerate(((-34, -46), (12, -50), (40, -44), (-10, -60), (24, -66))):
        goods += bread(1505 + dx, 1102 + dy, 30)
    # pomegranates in a bowl
    goods += (f'<path d="M1585,1062 Q1640,1112 1700,1062 Z" fill="#3f79a8" stroke="{INK}" stroke-width="3.5"/>')
    for cx, cy in ((1606, 1050), (1642, 1044), (1678, 1052)):
        goods += fruit(cx, cy, 20, "#c2413f", crown=True)
    # dates (heap) and a bunch of grapes
    goods += basket(1770, 1100, 100, 34, fill="#b7874b")
    for i in range(16):
        r = random.Random(i)
        cx, cy = 1770 + r.uniform(-38, 38), 1062 - r.uniform(0, 22) + abs(r.uniform(-38, 38)) * 0.25
        goods += (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="9" ry="6" fill="#7b3d24" stroke="{INK}" '
                  f'stroke-width="2" transform="rotate({r.uniform(-40, 40):.0f} {f1(cx)} {f1(cy)})"/>')
    for i, (dx, dy) in enumerate(((0, 0), (14, 0), (28, 0), (7, 12), (21, 12), (14, 24), (-7, 12))):
        goods += (f'<circle cx="{1838 + dx}" cy="{1048 + dy}" r="9" fill="#7d5aa0" stroke="{INK}" '
                  f'stroke-width="2.2"/>')
    goods += f'<path d="M1852,1046 q4,-14 14,-16" stroke="{P["leaf_dark"]}" stroke-width="4" fill="none"/>'
    skirt = (f'<rect x="{x0}" y="{yt}" width="{x1 - x0}" height="78" fill="#e6d2a8" stroke="{INK}" '
             f'stroke-width="4"/>'
             f'<rect x="{x0}" y="{yt + 14}" width="{x1 - x0}" height="14" fill="{P["terracotta"]}"/>'
             f'<rect x="{x0}" y="{yt + 44}" width="{x1 - x0}" height="8" fill="#3f79a8"/>')
    skirt += "".join(f'<path d="M{xx},{yt + 78} l0,10" stroke="{P["terracotta"]}" stroke-width="4" '
                     f'stroke-linecap="round"/>' for xx in range(x0 + 10, x1, 18))
    legs = ""
    for x in (x0 + 16, x1 - 16):
        legs += (f'<path d="M{x},{yt + 78} L{x},{TABLE_FLOOR}" stroke="{INK}" stroke-width="15" '
                 f'stroke-linecap="round"/><path d="M{x},{yt + 78} L{x},{TABLE_FLOOR}" stroke="{P["wood_dark"]}" '
                 f'stroke-width="8" stroke-linecap="round"/>')
    shadow = (f'<ellipse cx="{(x0 + x1) / 2}" cy="{TABLE_FLOOR + 2}" rx="{(x1 - x0) / 2 + 30}" ry="16" '
              f'fill="{INK}" opacity="0.16" filter="url(#soft)"/>')
    # jars beside the table
    jars = PR.jar(x1 + 70, TABLE_FLOOR - 66, 0.8) + PR.jar(x1 + 130, TABLE_FLOOR - 44, 0.55, color="#b8643e")
    return doc(tplace(shadow + S.g(legs + top + goods + skirt, filter="wobble-fine") + jars))


def cover_svg():
    """A plain woven linen cloth (fringe only) thrown over all the food on the table (the fast): it hugs the bread
    stack, the pomegranates, the dates and the grapes, so their lumps show through, and hangs a little over the
    front."""
    x0, x1 = TABLE_X0, TABLE_X1
    top = [(x0 - 6, 1128), (x0 - 2, 1094), (1440, 1066), (1462, 1036), (1500, 1018), (1532, 1014), (1566, 1040),
           (1582, 1062), (1600, 1028), (1642, 1008), (1686, 1018), (1706, 1050), (1720, 1066), (1738, 1048),
           (1772, 1030), (1806, 1040), (1822, 1060), (1840, 1036), (1862, 1022), (1884, 1040), (x1 + 4, 1080),
           (x1 + 8, 1126)]
    hem = []
    n = 14
    for i in range(1, n):
        xx = x1 + 8 - (x1 + 14 - x0) * i / n
        hem.append((xx, 1126 + (5 if i % 2 else 0)))
    d = S.smooth_path(top + hem, closed=True, tension=0.75)
    cid = "s16cover"
    linen, shade_c, crease = LINEN, LINEN_SHADE, "#b39465"
    inner = ""
    # soft shade on the right flank of every lump (light comes from the low sun on the left of the stall)
    for cx, cy, rx, ry in ((1548, 1052, 26, 40), (1690, 1046, 24, 42), (1802, 1058, 20, 30), (1880, 1062, 14, 26)):
        inner += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{shade_c}" opacity="0.55"/>'
    for cx, cy, rx, ry in ((1494, 1030, 30, 9), (1634, 1022, 28, 8), (1766, 1042, 24, 7)):
        inner += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f4e6c4" opacity="0.8"/>'
    folds = ""
    for (xa, ya), (xb, yb) in (((1500, 1040), (1474, 1100)), ((1540, 1036), (1560, 1098)),
                               ((1630, 1030), (1612, 1100)), ((1676, 1036), (1700, 1098)),
                               ((1770, 1050), (1756, 1100)), ((1860, 1046), (1872, 1098))):
        folds += f'<path d="M{xa},{ya} Q{(xa + xb) / 2 + 6},{(ya + yb) / 2} {xb},{yb}"/>'
    inner += f'<g stroke="{crease}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8">{folds}</g>'
    body = (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{linen}"/>'
            f'<g clip-path="url(#{cid})">{inner}</g>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    body += "".join(f'<path d="M{f1(xx)},{1129 + (4 if k % 2 else 0)} l{(k % 3) - 1},11" stroke="#b9975f" '
                    f'stroke-width="3.5" stroke-linecap="round"/>'
                    for k, xx in enumerate(range(x0 + 2, x1 + 6, 14)))
    return doc(S.g(tplace(body), filter="wobble-fine"))


LINEN, LINEN_SHADE, LINEN_FRINGE = "#dfc48f", "#c1a06c", "#b08d55"
SHEET_C = (1656, 1062)      # (local) centre of the flying sheet as it lands over the food


def held_sheet_markup(h0, h1, s):
    """The linen sheet held up by its two top corners in the merchant's raised hands (h0, h1: stage hand centres),
    drawn BEHIND him: it billows up above his hands and hangs down behind his body, flaring out at the sides, so
    it shows between his arms and around his head and he clearly grips its corners."""
    (xa, ya), (xb, yb) = sorted((h0, h1))
    mx = (xa + xb) / 2
    drop = 250 * s
    top = [(xa - 6 * s, ya - 8 * s), (xa + 30 * s, ya - 44 * s), (mx, ya - 66 * s), (xb - 30 * s, yb - 44 * s),
           (xb + 6 * s, yb - 8 * s)]
    right = [(xb + 22 * s, yb + drop * 0.45), (xb + 40 * s, yb + drop)]
    low = []
    n = 6
    for k in range(n + 1):
        u = k / n
        xx = xb + 40 * s - (xb - xa + 80 * s) * u
        low.append((xx, (ya + yb) / 2 + drop + 12 * s * math.sin(math.pi * u * 2.5)))
    left = [(xa - 22 * s, ya + drop * 0.45)]
    d = S.smooth_path(top + right + low[1:-1] + [(xa - 40 * s, ya + drop)] + left, closed=True, tension=0.7)
    cid = "s16held"
    out = (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{LINEN}"/>'
           # his own soft shadow on the sheet behind him
           f'<g clip-path="url(#{cid})"><ellipse cx="{f1(mx + 14 * s)}" cy="{f1(ya + 150 * s)}" rx="{70 * s:.1f}" '
           f'ry="{150 * s:.1f}" fill="{LINEN_SHADE}" opacity="0.75" filter="url(#soft)"/></g>'
           f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{4 * s:.1f}" stroke-linejoin="round"/>')
    # soft folds falling from the held corners and the billow's shadow
    folds = ""
    for (x0_, y0_), (x1_, y1_) in (((xa + 4 * s, ya + 10 * s), (xa - 10 * s, ya + drop * 0.9)),
                                   ((xa + 40 * s, ya - 30 * s), (xa + 30 * s, ya + drop * 0.85)),
                                   ((xb - 40 * s, yb - 30 * s), (xb - 24 * s, yb + drop * 0.85)),
                                   ((xb - 4 * s, yb + 10 * s), (xb + 14 * s, yb + drop * 0.9))):
        folds += (f'<path d="M{f1(x0_)},{f1(y0_)} Q{f1((x0_ + x1_) / 2 + 8 * s)},{f1((y0_ + y1_) / 2)} '
                  f'{f1(x1_)},{f1(y1_)}"/>')
    out += (f'<g stroke="{S.shade(LINEN_SHADE, -0.08)}" stroke-width="{4.5 * s:.1f}" fill="none" '
            f'stroke-linecap="round">{folds}</g>'
            f'<path d="M{f1(xa + 40 * s)},{f1(ya - 26 * s)} Q{f1(mx)},{f1(ya - 52 * s)} {f1(xb - 40 * s)},'
            f'{f1(yb - 26 * s)}" stroke="#f4e6c4" stroke-width="{7 * s:.1f}" fill="none" stroke-linecap="round" '
            f'opacity="0.8"/>')
    return S.g(out, filter="wobble-fine")


def sheet_svg():
    """The flat linen sheet in flight (no food lumps): straight-ish top edge, billowing curved lower edge with a
    flutter, fringe; drawn at its landing place over the table (local coordinates, placed with tplace)."""
    x0, x1 = TABLE_X0 - 8, TABLE_X1 + 10
    cx, cy = SHEET_C
    top = [(x0 + 6, cy - 40), (x0 + 110, cy - 72), (cx, cy - 86), (x1 - 110, cy - 70), (x1 - 4, cy - 36)]
    low = []
    n = 9
    for i in range(n + 1):
        u = i / n
        xx = x1 + 14 - (x1 - x0 + 28) * u
        yy = cy + 54 + 22 * math.sin(math.pi * u * 3 + 0.6) + 14 * math.sin(math.pi * u)
        low.append((xx, yy))
    d = S.smooth_path(top + low, closed=True, tension=0.8)
    body = f'<path d="{d}" fill="{LINEN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    # soft billow shading and a few wind creases
    body += (f'<path d="M{x0 + 40},{cy + 26} Q{cx - 60},{cy + 58} {cx + 20},{cy + 30} Q{cx + 120},{cy + 6} {x1 - 40},'
             f'{cy + 34}" stroke="{LINEN_SHADE}" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.6"/>'
             f'<path d="M{x0 + 120},{cy - 52} Q{cx},{cy - 72} {x1 - 120},{cy - 50}" stroke="#f4e6c4" stroke-width="9" '
             f'fill="none" stroke-linecap="round" opacity="0.8"/>')
    body += "".join(f'<path d="M{xa},{cy - 56} Q{xa + 12},{cy - 10} {xa - 6},{cy + 40}" stroke="{LINEN_SHADE}" '
                    f'stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.9"/>'
                    for xa in (x0 + 90, cx - 70, cx + 80, x1 - 100))
    body += "".join(f'<path d="M{f1(xx)},{f1(yy)} l{(k % 3) - 1},11" stroke="{LINEN_FRINGE}" stroke-width="3.5" '
                    f'stroke-linecap="round"/>' for k, (xx, yy) in enumerate(low[1:-1]))
    return doc(S.g(tplace(body), filter="wobble-fine"))


def awning_svg():
    """Front posts and the striped awning of the stall (in front of the merchant)."""
    x0, x1 = TABLE_X0, TABLE_X1
    body = ""
    for x in (x0 + 4, x1 - 4):
        body += (f'<path d="M{x},780 L{x},{TABLE_FLOOR}" stroke="{INK}" stroke-width="19" stroke-linecap="round"/>'
                 f'<path d="M{x},780 L{x},{TABLE_FLOOR}" stroke="{P["wood"]}" stroke-width="11" '
                 f'stroke-linecap="round"/>')
    ax0, ax1, ay_back, ay_front = x0 - 40, x1 + 50, 714, 776
    top = f'M{ax0 + 60},{ay_back} L{ax1 + 40},{ay_back - 6} L{ax1},{ay_front} L{ax0},{ay_front} Z'
    body += f'<path d="{top}" fill="#f3e4c2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    n = 8
    stripes = ""
    for i in range(0, n, 2):
        u0, u1 = i / n, (i + 1) / n
        bx0, bx1 = ax0 + 60 + (ax1 + 40 - ax0 - 60) * u0, ax0 + 60 + (ax1 + 40 - ax0 - 60) * u1
        fx0, fx1 = ax0 + (ax1 - ax0) * u0, ax0 + (ax1 - ax0) * u1
        stripes += (f'<path d="M{f1(bx0)},{f1(ay_back - 6 * u0)} L{f1(bx1)},{f1(ay_back - 6 * u1)} L{f1(fx1)},'
                    f'{ay_front} L{f1(fx0)},{ay_front} Z" fill="{P["terracotta"]}"/>')
    body += stripes + f'<path d="{top}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    # scalloped valance
    val = f"M{ax0},{ay_front}"
    m = 12
    for i in range(m):
        xa = ax0 + (ax1 - ax0) * (i + 1) / m
        xm = ax0 + (ax1 - ax0) * (i + 0.5) / m
        val += f" Q{f1(xm)},{ay_front + 40} {f1(xa)},{ay_front}"
    val += " Z"
    body += f'<path d="{val}" fill="#f3e4c2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    for i in range(0, m, 2):
        xa, xb = ax0 + (ax1 - ax0) * i / m, ax0 + (ax1 - ax0) * (i + 1) / m
        xm = (xa + xb) / 2
        body += (f'<path d="M{f1(xa)},{ay_front} Q{f1(xm)},{ay_front + 40} {f1(xb)},{ay_front} Z" '
                 f'fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(tplace(body), filter="wobble-fine"))


# ============================================================================ characters


def held_stick(x, y, s, facing, pose):
    """The elder's walking stick in his far hand while the library pose has none ('listen': the near hand is at
    his chin), from the hand down to the ground beside his far foot, so the stick never pops out."""
    hx, hy = C.body_points(C.citizen, x, y, s, facing, kind="elder", variant=0, pose=pose)["hands"][0]
    top = (hx + facing * 2 * s, hy - 12 * s)
    bot = (hx - facing * 6 * s, y - 2 * s)
    d = f"M{f1(top[0])},{f1(top[1])} L{f1(bot[0])},{f1(bot[1])}"
    crook = f"M{f1(top[0])},{f1(top[1])} L{f1(top[0] + facing * 10 * s)},{f1(top[1] - 6 * s)}"
    return S.g(f'<path d="{d} {crook}" stroke="{INK}" stroke-width="{11.2 * s:.1f}" fill="none" '
               f'stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="{d} {crook}" stroke="{P["wood"]}" stroke-width="{6 * s:.1f}" fill="none" '
               f'stroke-linecap="round" stroke-linejoin="round"/>', filter="wobble-fine")


def person(kind, variant, x, y, s, facing, pose, attire="normal", expr=None, shadow=True):
    sw = {"kneel_pray": 170, "half_kneel": 140}.get(pose, 110)
    if kind == "child":
        sw = {"kneel_pray": 120, "half_kneel": 104}.get(pose, 86)
    out = C.ground_shadow(x, y, s, sw, opacity=0.2) if shadow else ""
    if pose == "half_kneel":
        return out + half_kneel_fig(x, y, s, kind, variant, facing, attire, expr or "sorry")[0]
    if kind == "elder" and pose == "listen":
        out += held_stick(x, y, s, facing, pose)
    return out + C.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, attire=attire, expr=expr)


def stick_leaning(x, y, s, facing):
    """The elder's walking stick leaning against his back while he kneels (drawn under him: it shows along his back
    from the ground behind his heels, with its crook above his shoulder)."""
    f = facing
    b = (x - f * 104 * s, y - 2 * s)
    t = (x - f * 50 * s, y - 238 * s)
    d = f"M{f1(b[0])},{f1(b[1])} L{f1(t[0])},{f1(t[1])} Q{f1(t[0] + f * 4 * s)},{f1(t[1] - 16 * s)} " \
        f"{f1(t[0] + f * 16 * s)},{f1(t[1] - 12 * s)}"
    return S.g(f'<path d="{d}" stroke="{INK}" stroke-width="{12 * s:.1f}" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/><path d="{d}" stroke="{P["wood"]}" stroke-width="{6.4 * s:.1f}" '
               f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>', filter="wobble-fine")


def horn_svg(hx, hy, s, facing=1):
    """A long bronze herald's horn from the mouth (hx, hy) up and forward, bell at the end."""
    f = facing
    pts = [(hx, hy), (hx + f * 52 * s, hy - 14 * s), (hx + f * 104 * s, hy - 40 * s), (hx + f * 146 * s, hy - 78 * s)]
    d = S.smooth_path(pts, closed=False)
    bx, by = pts[-1]
    body = (f'<path d="{d}" stroke="{INK}" stroke-width="{17 * s:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#d9a441" stroke-width="{10 * s:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#f5d78a" stroke-width="{3 * s:.1f}" fill="none" stroke-linecap="round" '
            f'opacity="0.8" transform="translate(0,{-2 * s:.1f})"/>'
            f'<g transform="translate({f1(bx)},{f1(by)}) rotate({-42 * f})">'
            f'<path d="M{-8 * f * s},{-9 * s} L{f * 30 * s},{-26 * s} Q{f * 40 * s},0 {f * 30 * s},{26 * s} '
            f'L{-8 * f * s},{9 * s} Z" fill="#d9a441" stroke="{INK}" stroke-width="{4 * s:.1f}" '
            f'stroke-linejoin="round"/><ellipse cx="{f * 33 * s}" cy="0" rx="{8 * s}" ry="{25 * s}" fill="#8c5a24" '
            f'stroke="{INK}" stroke-width="{3.5 * s:.1f}"/></g>')
    return S.g(body, filter="wobble-fine")


def puff_svg(cx, cy, rx, ry, seed=0, k=1.0):
    """Cartoon 'quick change' poof (from v1 s10): soft dust clouds hugging the sides and feet of a figure and a
    few short whoosh lines at its sides (never over the face)."""
    rng = random.Random(seed)
    dust = ""
    for i, deg in enumerate((-25, 8, 40, 72, 108, 140, 172, 205)):
        a = math.radians(deg + rng.uniform(-6, 6))
        px, py = cx + rx * 0.92 * math.cos(a), cy + ry * 0.95 * math.sin(a)
        w = k * rng.uniform(62, 84)
        dust += S.cloud(px, py, w, w * 0.62, "#ecdcb8", seed=seed * 17 + i, puffs=3, sw=2.4 * min(1, k + 0.2),
                        shade_fill="#d2bb8f")
    lines = ""
    for a0, span, rr in ((-48, 40, 1.22), (-8, 34, 1.32), (188, -40, 1.22), (148, -34, 1.32)):
        pts = [(cx + rx * rr * math.cos(math.radians(a0 + span * j / 6)),
                cy + ry * rr * 0.92 * math.sin(math.radians(a0 + span * j / 6))) for j in range(7)]
        lines += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["ink_soft"]}" '
                  f'stroke-width="{4.5 * k:.1f}" stroke-linecap="round" opacity="0.75"/>')
    return S.g(lines, filter="wobble-fine") + S.g(dust, filter="wobble-fine", opacity=0.92)


def small_puff(x, y, h, seed=0):
    """A light cloth-poof for a small figure in the crowd: a few dust clouds at the feet and hips and two
    whoosh arcs at the sides, sized to the figure height h (never over the face)."""
    rng = random.Random(seed)
    dust = ""
    for i, (dx, dy, w) in enumerate(((-0.30, -0.02, 0.36), (0.30, -0.03, 0.34), (0.0, 0.03, 0.40),
                                     (-0.36, -0.36, 0.24), (0.36, -0.40, 0.24))):
        ww = h * w * rng.uniform(0.85, 1.15)
        dust += S.cloud(x + dx * h, y + dy * h, ww, ww * 0.6, "#ecdcb8", seed=seed * 13 + i, puffs=3,
                        sw=max(1.6, h / 120), shade_fill="#d2bb8f")
    lines = ""
    for side in (-1, 1):
        pts = [(x + side * h * (0.34 + 0.04 * math.sin(j / 2)), y - h * (0.30 + 0.08 * j)) for j in range(5)]
        lines += (f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{P["ink_soft"]}" '
                  f'stroke-width="{max(2.2, h / 70):.1f}" stroke-linecap="round" opacity="0.7"/>')
    return S.g(lines, filter="wobble-fine") + S.g(dust, filter="wobble-fine", opacity=0.85)


def puff_motion(t0, pivot):
    return hop(t0, [(-0.06, {"alpha": 0, "s": 0.8, "dy": 0}), (0.02, {"alpha": 1, "s": 0.97, "dy": -4}),
                    (0.16, {"alpha": 0.85, "s": 1.06, "dy": -12}), (0.38, {"alpha": 0, "s": 1.14, "dy": -24})],
               pivot, ["out", "sine", "in"])


def arcs_svg(x, y, facing, k, s=1.0):
    """Little 'speaking' sound arcs in front of a mouth (k = 1..3 for a gentle flicker)."""
    out = ""
    for i in range(3):
        r = (13 + 13 * i + (k - 2) * 2) * s
        sx, sy = x + facing * r * 0.45, y - r * 0.85
        qx, qy = x + facing * r * 1.2, y
        ex, ey = x + facing * r * 0.45, y + r * 0.85
        out += (f'<path d="M{f1(sx)},{f1(sy)} Q{f1(qx)},{f1(qy)} {f1(ex)},{f1(ey)}" '
                f'fill="none" stroke="{INK}" stroke-width="{5 * s:.1f}" stroke-linecap="round" opacity="0.85"/>')
    return doc(S.g(out, filter="wobble-fine"))


def toot_svg(x, y, k):
    """Three short burst strokes fanning out of the horn's bell (k = 0..2 flicker)."""
    out = ""
    for i, a in enumerate((-70, -40, -10)):
        aa = math.radians(a + (k - 1) * 3)
        r0, r1 = 14 + 4 * ((i + k) % 2), 40 + 6 * ((i + k) % 3)
        out += (f'<path d="M{f1(x + r0 * math.cos(aa))},{f1(y + r0 * math.sin(aa))} L{f1(x + r1 * math.cos(aa))},'
                f'{f1(y + r1 * math.sin(aa))}" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def exclaim_svg(x, y, s=1.0):
    """A '!' with burst ticks; a cream halo under the ink keeps it readable on any wall."""
    body = (f'<path d="M{x - 9 * s},{y - 70 * s} L{x + 9 * s},{y - 70 * s} L{x + 5 * s},{y - 20 * s} '
            f'L{x - 5 * s},{y - 20 * s} Z" fill="#c9714a" stroke="{INK}" stroke-width="{4 * s}" '
            f'stroke-linejoin="round"/><circle cx="{x}" cy="{y - 4 * s}" r="{8 * s}" fill="#c9714a" '
            f'stroke="{INK}" stroke-width="{4 * s}"/>')
    for a in (-60, -30, 30, 60):
        r0, r1 = 52 * s, 72 * s
        aa = math.radians(a - 90)
        body += (f'<path d="M{f1(x + r0 * math.cos(aa))},{f1(y - 36 * s + r0 * math.sin(aa))} '
                 f'L{f1(x + r1 * math.cos(aa))},{f1(y - 36 * s + r1 * math.sin(aa))}" stroke="{INK}" '
                 f'stroke-width="{4 * s}" stroke-linecap="round"/>')
    halo = (body.replace(f'stroke="{INK}"', 'stroke="#fff3dc"').replace(f'stroke-width="{4 * s}"',
                                                                    f'stroke-width="{13 * s}"')
            .replace('fill="#c9714a"', 'fill="#fff3dc"'))
    return doc(S.g(halo, filter="wobble-fine", opacity=0.9) + S.g(body, filter="wobble-fine"))


def hip_horn_markup(px, py, s, facing=1):
    """The horn hanging at the hip on a cord before it is blown (same drawing as s17's messenger)."""
    f = facing
    pts = [(px - f * 34 * s, py - 6 * s), (px + f * 2 * s, py + 26 * s), (px + f * 40 * s, py + 30 * s)]
    d = S.smooth_path(pts, closed=False)
    return S.g(f'<path d="M{f1(px - f * 30 * s)},{f1(py - 62 * s)} L{f1(px - f * 30 * s)},{f1(py - 8 * s)}" '
               f'stroke="{P["wood_dark"]}" stroke-width="{3 * s:.1f}"/>'
               f'<path d="{d}" stroke="{INK}" stroke-width="{14 * s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<path d="{d}" stroke="#d9a441" stroke-width="{8 * s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<ellipse cx="{f1(px + f * 44 * s)}" cy="{f1(py + 29 * s)}" rx="{6 * s:.1f}" ry="{13 * s:.1f}" '
               f'fill="#8c5a24" stroke="{INK}" stroke-width="{3 * s:.1f}"/>', filter="wobble-fine")


def scratch_svg(pts, k, s=1.0):
    """Tiny 'itchy' marks: a short zigzag at each point (k = 0..2 flicker)."""
    out = ""
    for i, (x, y, side) in enumerate(pts):
        j = (k + i) % 3
        x += side * 3 * j
        zz = f"M{f1(x)},{f1(y - 12 * s)}"
        for n in range(4):
            zz += f" L{f1(x + side * (9 if n % 2 == 0 else 0) * s)},{f1(y - 12 * s + (n + 1) * 7 * s)}"
        out += (f'<path d="{zz}" stroke="{P["ink_soft"]}" stroke-width="{3.6 * s:.1f}" fill="none" '
                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>')
    return doc(S.g(out, filter="wobble-fine"))


def smoke_svg(cx, cy, r, seed):
    """One soft round smoke puff: no ink outline, soft edge, a lighter core."""
    d = S.blob(cx, cy, r, r * 0.86, 0.07, 16, seed)
    return doc(f'<path d="{d}" fill="#c4bcbd"/>'
               f'<path d="{S.blob(cx - r * 0.14, cy - r * 0.16, r * 0.6, r * 0.48, 0.06, 12, seed + 1)}" '
               f'fill="#ddd7d3" opacity="0.85"/>'
               f'<path d="{d}" fill="none" stroke="{P["ink_soft"]}" stroke-width="2" opacity="0.3"/>', )


def glaze_svg(kind):
    if kind == "dusk":      # solemn evening: rosy-lilac sky and city, fading out over the square (multiply)
        h = 1080
        stops = [(0, "#bfa0c4", 0.42), (0.5, "#dcb4b4", 0.26), (0.8, "#e9bfa8", 0.13), (1, "#efc6a2", 0)]
        defs = S.lin_grad("s16dusk", stops)
        return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{h + 20}" fill="url(#s16dusk)"/>', defs)
    if kind == "believe":   # a brief warm golden patch in the sky above the crowd (normal blend, behind the city)
        defs = S.rad_grad("s16bel", [(0, "#ffe6a6", 0.95), (0.35, "#ffd88a", 0.7), (0.7, "#ffcf7a", 0.28),
                                     (1, "#ffcf7a", 0)])
        return doc('<ellipse cx="1240" cy="450" rx="640" ry="250" fill="url(#s16bel)"/>', defs)
    if kind == "gleam":     # golden light behind the cloud at the upper right (normal blend, behind the city)
        cx, cy = GLOW_C
        defs = S.rad_grad("s16glm", [(0, "#fff0c0", 1), (0.3, "#ffe09a", 0.9), (0.62, "#ffd27a", 0.45),
                                     (1, "#ffcf7a", 0)])
        return doc(f'<ellipse cx="{cx}" cy="{cy + 10}" rx="560" ry="330" fill="url(#s16glm)"/>', defs)
    # hope: a warm golden glow opening in the sky at the upper right, where the kneeling people look (screen)
    cx, cy = GLOW_C
    defs = S.rad_grad("s16hope", [(0, "#ffd27a", 0.7), (0.32, "#ffd27a", 0.42), (0.66, "#ffcf80", 0.14),
                                  (1, "#ffcf80", 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="700" ry="500" fill="url(#s16hope)"/>', defs)


def rays_svg(src, a_mid, spread, n=3, length=950, seed=4):
    """A few very faint soft sunbeams fanning from behind a cloud (no hard apex: they start transparent)."""
    sx, sy = src
    defs = (f'<radialGradient id="s16ray" gradientUnits="userSpaceOnUse" cx="{sx}" cy="{sy}" r="{length}">'
            f'<stop offset="0" stop-color="#ffe2a0" stop-opacity="0"/>'
            f'<stop offset="0.15" stop-color="#ffe2a0" stop-opacity="0.62"/>'
            f'<stop offset="0.55" stop-color="#ffd27a" stop-opacity="0.3"/>'
            f'<stop offset="1" stop-color="#ffc864" stop-opacity="0"/></radialGradient>')
    rng = random.Random(seed)
    d = ""
    for i in range(n):
        a = math.radians(a_mid - spread / 2 + spread * i / max(1, n - 1) + rng.uniform(-2.0, 2.0))
        wa = math.radians(rng.uniform(2.6, 3.6))
        r0, r1 = 40, length * rng.uniform(0.8, 1.0)
        pts = [(sx + r0 * math.cos(a - wa / 4), sy + r0 * math.sin(a - wa / 4)),
               (sx + r1 * math.cos(a - wa), sy + r1 * math.sin(a - wa)),
               (sx + r1 * math.cos(a + wa), sy + r1 * math.sin(a + wa)),
               (sx + r0 * math.cos(a + wa / 4), sy + r0 * math.sin(a + wa / 4))]
        d += "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z "
    return doc(f'<path d="{d}" fill="url(#s16ray)" filter="url(#blur-md)"/>', defs)


DOVE_REF = (300, 300)
WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)


def dove_frames(facing, s=0.55):
    return [doc(PR.dove(DOVE_REF[0], DOVE_REF[1], s, facing, wing=w)) for w in WINGS]


def wing_cycle(rate, phase, glide=(0, 0)):
    seq = (0, 1, 2, 3, 4, 3, 2, 1)

    def fa(t):
        if glide[0] <= t < glide[1]:
            return 2.0
        return float(seq[int(t * rate + phase * 8) % 8])
    return fa


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]

    def chunk(line, phrase):
        return next(c for c in line.chunks if phrase in c.text)

    def within(c, u):
        return c.start + (c.end - c.start) * u

    # ---- key times (all from the narration chunks) ----
    c0a, c0b = chunk(L0, "你猜"), chunk(L0, "竟然")
    c1a, c1b, c1c = chunk(L1, "禁食"), chunk(L1, "大人"), chunk(L1, "认错")
    t_heard = within(c0a, 0.50)              # "尼尼微的人听了": faces turn thoughtful (staggered)
    t_wow = c0b.start + 0.12                 # "竟然": eyes wide
    t_up = within(c0b, 0.30)                 # "都相信了": they lift their eyes to the sky (warm light, twinkles)
    t_believe = within(c0b, 0.70)            # "上帝！": they nod and lower their eyes (sorry)
    hold_up = max(0.2, t_believe - t_up - 0.62)   # the look-up is over just before the 'sorry' cuts
    t_horn = snap(c0b.end - 0.1)             # the herald turns and blows his horn
    t_call = snap(c1a.start + 0.25)          # "他们禁食": he proclaims the fast
    t_reach = snap(c1a.start + 0.35)         # the little girl reaches for the bread
    t_nofood = within(c1a, 0.49)             # "就是不吃饭": the cloth goes over the food
    t_hold = snap(t_nofood - 0.5)            # the merchant lifts the folded cloth over his head
    t_rel = snap(t_nofood - 0.02)            # ... and throws it: a flat sheet flies forward and down
    t_land = snap(t_rel + 0.34)              # it lands and hugs the food
    t_back = snap(t_land + 0.08)             # she pulls her hand back
    t_okay = snap(t_back + 0.5)              # and nods
    t_change = c1b.start + 0.1               # "大人小孩都换上…": sackcloth wave (grown-ups first)
    t_kid = within(c1b, 0.22)                # "小孩": the children
    t_rough = within(c1b, 0.52)              # "粗粗的麻布衣服": scratchy!
    t_kneel = c1c.start + 0.12               # "向上帝认错": kneel in a wave, toward the light
    t_hope = within(c1c, 0.54)               # "表示愿意改": a soft warm light opens at the upper right
    # the hand-over from s15: its street stays for the whole scene; its golden sky and warm light fade slowly into
    # this scene's sky, before the golden patch
    T_SKY0, T_SKY1 = 1.0, min(4.4, t_up - 0.1)

    def sky15_a(t):
        return Tf(alpha=1 - M.progress(t, T_SKY0, T_SKY1, "sine"))

    # ---- sky, sun, clouds, s15's skyline and street ----
    sc.add("sky", sky_svg(), z=0, wc=0.6)
    sc.add("sky15", sky15_svg(), z=0.05, wc=0.6, motion=sky15_a)
    # s15's low sun stays (they kneel toward it and God's light later), its rays still turning slowly as in s15
    sun_c = m15(*S15_SUN)
    sc.add("sun15", sun15_svg(), z=0.3, wc=0, motion=lambda t: Tf(rot=3.0 * t, px=sun_c[0], py=sun_c[1]))
    # s15's clouds drift on gently; the right one drifts left over the low sun and is where God's light opens
    # behind it ("gleam", "rays") at the end
    vr = (CLOUD_R0[0] - GLOW_C[0]) / (t_hope + 0.8)

    def cloud_r(t):
        return Tf(dx=-vr * t)

    def with_cloud(t):          # the gleam and rays (drawn round GLOW_C) ride with the right cloud
        return Tf(dx=CLOUD_R0[0] - vr * t - GLOW_C[0])
    sc.add("clouds15", clouds15_svg(S15_CLOUDS[:2]), z=1, motion=M.drift(vx=4))
    sc.add("cloud15_r", clouds15_svg(S15_CLOUDS[2:]), z=1.05, motion=cloud_r)
    sc.add("far15", far15_svg(), z=1.25, wc=0.8)
    sc.add("glow15", glow15_svg(), z=1.3, wc=0, blend="screen", motion=sky15_a)
    sc.add("back15", back15_svg(), z=2)

    # doves gliding far over the roofs (sparse, slow; they set off outside the frame)
    fr_r, fr_l = dove_frames(1), dove_frames(-1)
    for i, (fc, x0, y0, x1, y1, ta, tb, rate, ph) in enumerate((
            (1, -80, 400, 900, 330, 0.0, 9.0, 9, 0.0),
            (1, -200, 440, 700, 380, 1.0, 10.5, 10, 0.4),
            (-1, 2500, 480, 1300, 430, 8.0, T + 0.5, 9, 0.2))):
        def mot(t, x0=x0, y0=y0, x1=x1, y1=y1, ta=ta, tb=tb, ph=ph):
            u = (t - ta) / (tb - ta)
            a = 1.0 if ta <= t <= tb else 0.0
            return Tf(dx=x0 + (x1 - x0) * u - DOVE_REF[0], dy=y0 + (y1 - y0) * u - DOVE_REF[1]
                      + 10 * math.sin(t * 2.2 + ph * 6), alpha=a)
        sc.add(f"dove{i}", fr_r if fc > 0 else fr_l, z=2.5 + 0.01 * i, seed=700 + i,
               frame_at=wing_cycle(rate, ph, glide=(ta + 1.5, ta + 3.2)), motion=mot)

    # ---- this scene's set on s15's street (they come in with the dissolve): the herald's plinth, the bread oven
    # with its smoke (it dies away at the fast) ----
    sc.add("plinth", plinth_svg(), z=3)
    sc.add("oven", oven_svg(), z=3.05)
    smoke_stop = t_land
    n_smoke, per = 5, 4.6
    sm_y = OVEN_TOP - 16 * OVEN_K
    for i in range(n_smoke):
        ph = i / n_smoke

        def smot(t, ph=ph, i=i):
            u = (t / per + ph) % 1.0
            born = t - u * per
            if born > smoke_stop:
                return Tf(alpha=0)
            fade = 1 - M.progress(t, smoke_stop, smoke_stop + 1.4, "sine")    # the oven goes cold
            k = 0.7 + 1.2 * u
            return Tf(dx=30 * u + 6 * math.sin(t * 0.9 + i), dy=-170 * u, sx=k, sy=k,
                      alpha=0.5 * math.sin(math.pi * min(1.0, u * 1.15)) * fade, px=OVEN_X, py=sm_y + 6)
        sc.add(f"smoke{i}", smoke_svg(OVEN_X, sm_y, 26 * OVEN_K, 50 + i), z=3.1, wc=0.4, motion=smot)

    # ---- the crowd: stand worried -> listen -> sorry (believe) -> sackcloth (sad) -> kneel sorry, facing the light.
    # s15's townspeople carry on (nothing fades): the stroller and the boy stay where s15 leaves them; the vendor
    # walks over behind Jonah with two newcomers following him in from the left edge; two groups hop in from the
    # right edge beside the merchant's stall (held at alpha 0 until each sets off, outside the frame)
    def state_fig(m, st, turned=False):
        kind, v, x, y, s, f0, f1_ = m
        if st == 0:
            return person(kind, v, x, y, s, f0, "stand", expr="worried")
        if st == 1:         # "你猜怎么样？": some turn to their neighbour
            return person(kind, v, x, y, s, -f0 if turned else f0, "stand", expr="worried")
        if st == 2:
            return person(kind, v, x, y, s, f0, "listen")
        if st == 3:
            return person(kind, v, x, y, s, f0, "stand", expr="sorry")
        if st == 4:
            return person(kind, v, x, y, s, f0, "sad", "sackcloth")
        if st == 5:
            return person(kind, v, x, y, s, f1_, "kneel_pray", "sackcloth", "sorry")
        # the one-knee in-between of kneeling down (already turned toward the light)
        return person(kind, v, x, y, s, f1_, "half_kneel", "sackcloth", "sorry")

    def group_frames(members, turn):
        return [doc("".join(state_fig(m, st, j % 2 == turn) for j, m in enumerate(members))) for st in range(7)]

    # the walkers: the vendor sets off from his pots just after the dissolve and they stop, turn to Jonah and listen
    # as "竟然" begins (planted-foot walk: s15's gait drawings, the group advancing one drawing's stride per drawing)
    t_wl0 = snap(0.92)
    t_wl1 = snap(c0b.start) - 0.5 / 30
    rate_wl = WALK_NL / (t_wl1 - t_wl0)

    def wl_i(t):
        return min(WALK_NL, int((t - t_wl0) * rate_wl + 1e-6))
    gtimes = {   # (turn to the neighbour or None, listen, sorry, sackcloth, kneel)
        "walk_l": (None, t_wl1, t_believe + 0.1, t_change + 0.56, t_kneel + 0.22),
        "c15": (c0a.start + 0.45, t_heard + 0.2, t_believe + 0.15, t_change + 0.66, t_kneel + 0.42),
        "back_r": (None, t_heard + 0.4, t_believe + 0.3, t_change + 1.1, t_kneel + 0.62),
        "mid_r": (None, t_heard + 0.5, t_believe + 0.35, t_change + 1.3, t_kneel + 0.78),
    }
    zrow = {"walk_l": 10.6, "c15": 11.5, "back_r": 10.1, "mid_r": 12.1}
    arrive = {"back_r": (snap(1.0), 300, 3), "mid_r": (snap(1.28), 330, 3)}   # (t0, from dx, hops)
    puffs_at = []
    group_puffs = []
    for name, members in CROWD.items():
        frames = group_frames(members, 0)
        gx = sum(m[2] for m in members) / len(members)
        gy = max(m[3] for m in members)
        s = members[0][4]
        tt, a, b, c, d = (snap(x) if x is not None else None for x in gtimes[name])
        sched = ([(tt, 1)] if tt is not None else []) + [(a, 2), (b, 3), (c, 4), (d, 6), (d + HALF_HOLD, 5)]
        lift = t_up + 0.08 * len(name) % 0.2
        hts = [kneel_heights(m[0], m[1]) for m in members]
        parts = [dip(a, s, (gx, gy), 4),
                 hop(lift, [(0, {"dy": 0}), (0.25, {"dy": -4 * s}), (0.6, {"dy": -3 * s}), (0.85, {"dy": 0})],
                     (gx, gy)),
                 bow(b + 0.05, (gx, gy), 0.016, 2),
                 kneel_down(d, (gx, gy), [sum(h[k] for h in hts) / len(hts) for k in range(3)],
                            vertical_only=True),
                 breathe_y(0.007, 3.4, (gx, gy), phase=len(name) * 0.13)]
        if tt is not None:
            parts.append(dip(tt, s, (gx, gy), 3))
        if name == "walk_l":
            # [s15's vendor at his pots (newcomers off the left edge)] + 12 walk drawings + the 7 states
            ph = (0, 6, 0)                      # gait phases: everyone sets off and arrives on a passing drawing
            order = sorted(range(len(members)), key=lambda j: members[j][3])

            def gait_body(k, members=members, ph=ph, order=order):
                body = ""
                for j in order:
                    kind, v, x, y, s_, _, _ = members[j]
                    ps = S15.walk_pose((k + ph[j]) % 12, A=WALK_ADV * S15.WALK_N / (2 * s_), lk=leg_k(kind))
                    body += C.ground_shadow(x, y, s_, 110, opacity=0.2) + gait_fig(x, y, s_, kind, v, 1, ps)
                return body
            pre = ""
            for j in order:
                kind, v, x, y, s_, _, _ = members[j]
                if kind == "man" and v == VENDOR[1] and abs(y - VENDOR[3]) < 1e-6:
                    pre += s15_fig_markup(*VENDOR, dx=WALK_D)
                else:
                    ps = S15.walk_pose((3 + ph[j]) % 12, A=WALK_ADV * S15.WALK_N / (2 * s_), lk=leg_k(kind))
                    pre += C.ground_shadow(x, y, s_, 110, opacity=0.2) + gait_fig(x, y, s_, kind, v, 1, ps)
            frames = [doc(pre)] + [doc(gait_body(k)) for k in range(12)] + frames
            cut = cuts([(0, 0)] + [(tk, 13 + i) for tk, i in sched])

            def fa(t, cut=cut):
                if t < t_wl0:
                    return 0.0
                if t < t_wl1:
                    return float(1 + (3 + wl_i(t)) % 12)
                return cut(t)

            def walk_mot(t):
                return Tf(dx=-WALK_D + (WALK_ADV * wl_i(t) if t >= t_wl0 else 0.0))
            parts += [walk_mot, dip(t_wl0, s, (gx, gy), 3)]
            sc.add(f"crowd_{name}", frames, z=zrow[name], frame_at=fa, motion=M.combine(*parts))
        elif name == "c15":
            # [s15's stroller and boy exactly as s15 leaves them] + the 7 states (the stroller turns to the boy)
            pre = s15_fig_markup(*BOY) + s15_fig_markup(*STROLLER)
            sc.add(f"crowd_{name}", [doc(pre)] + frames, z=zrow[name],
                   frame_at=cuts([(0, 0)] + [(tk, 1 + i) for tk, i in sched]), motion=M.combine(*parts))
        else:
            t0, dx0, n = arrive[name]
            parts.append(step_in(t0, (gx + dx0, gy, s), (gx, gy), s, n=n, dur=0.3, gap=0.05, lift=8.0))
            parts.append(lambda t, t0=t0: Tf(alpha=1.0 if t >= t0 else 0.0))
            sc.add(f"crowd_{name}", frames, z=zrow[name], frame_at=cuts([(0, 0)] + sched),
                   motion=M.combine(*parts))
        body = ""
        for j, (kind, v, x, y, s_, f0, _) in enumerate(members):
            hh = {"child": 215, "elder": 320}.get(kind, 330) * s_
            body += small_puff(x, y, hh, seed=40 + j + 7 * len(name))
        group_puffs.append((name, c, body, (gx, gy - 150 * s)))

    # ---- s15's bearded man walks off to the right in front of the merchant's stall, his two sheep trotting ahead
    # (they turn round just after the dissolve; once out of the frame they are hidden) ----
    _, _, bx, by, bs, _, _, _ = BEARD
    A_B, N_B, RATE_B = 60.0, 26, 12.5
    adv_b = 2 * A_B / S15.WALK_N * bs
    t_b0 = snap(1.02)
    bfr = [doc(s15_fig_markup(*BEARD))] + [
        doc(C.ground_shadow(bx, by, bs, 110) + gait_fig(bx, by, bs, "man", 0, 1, S15.walk_pose(k, A=A_B)))
        for k in range(12)]

    def b_i(t):
        return min(N_B, int((t - t_b0) * RATE_B + 1e-6))
    sc.add("beard15", bfr, z=16.4, frame_at=lambda t: 0.0 if t < t_b0 else float(1 + (3 + b_i(t)) % 12),
           motion=M.combine(lambda t: Tf(dx=adv_b * b_i(t) if t >= t_b0 else 0.0,
                                         alpha=0.0 if t >= t_b0 + N_B / RATE_B else 1.0),
                            dip(t_b0, bs, (bx, by), 4)))
    t_s0 = snap(0.95)

    def sheep_mot(t):
        if t < t_s0:
            return Tf()
        u = t - t_s0
        if u > 1.9:
            return Tf(alpha=0)
        w = max(0.0, u - 0.12)                         # they turn with a little hop, then trot off
        run = 320 * (w * w / 0.4 if w < 0.2 else w - 0.1)
        hopf = 14 * math.sin(math.pi * u / 0.24) if u < 0.24 else 9 * abs(math.sin(math.pi * 2.6 * (u - 0.24)))
        return Tf(dx=run, dy=-hopf)
    sc.add("sheep15", [doc(sheep15_markup(-1)), doc(sheep15_markup(1))], z=16.45,
           frame_at=cuts([(0, 0), (t_s0 + 0.1, 1)]), motion=sheep_mot)
    sc.add("step", step15_svg(), z=17.4)

    # ---- Jonah on his step: stern (as s15 leaves him); surprised at "竟然"; then uneasy (foreshadows ch. 4) ----
    jp = (J_X, J_Y)
    jsh = C.ground_shadow(J_X, J_Y, J_S, 120)
    jfr = [doc(jsh + C.jonah(J_X, J_Y, J_S, 1, pose="stand", expr="angry")),       # stern, as s15 ends
           doc(jsh + C.jonah(J_X, J_Y, J_S, 1, pose="stand", expr="surprised")),
           doc(jsh + C.jonah(J_X, J_Y, J_S, 1, pose="stand", expr="worried"))]     # uneasy (foreshadows ch. 4)
    tj1, tj2 = snap(t_wow + 0.1), snap(t_wow + 1.5)
    sc.add("jonah", jfr, z=17.5, frame_at=cuts([(0, 0), (tj1, 1), (tj2, 2)]),
           motion=M.combine(hop(tj1, [(0, {"dy": 0}), (0.1, {"dy": -8}), (0.24, {"dy": 0})], jp),
                            M.breathe(0.008, 3.1, pivot=jp, phase=0.2)))
    jh = C.body_points(C.jonah, J_X, J_Y, J_S, 1, pose="stand")["head_top"]
    exx, exy = jh[0] - 74, jh[1] + 34
    sc.add("jonah_wow", exclaim_svg(exx, exy, 1.1), z=30, wc=0, motion=M.keys(
        [(tj1 - 0.02, {"alpha": 0, "s": 0.4}), (tj1 + 0.25, {"alpha": 1, "s": 1}), (tj2 - 0.3, {"alpha": 1}),
         (tj2, {"alpha": 0})], ["back", "linear", "sine"], pivot=(exx, exy - 30)))

    # ---- the herald on his plinth (man variant 2 with his bronze horn at the hip, like s17's horn-blower) ----
    hp = (H_X, PLINTH_TOP)
    hsh = C.ground_shadow(H_X, PLINTH_TOP, H_S, 110)
    HV = 2

    def herald(facing, pose, attire="normal", expr=None, horn_at_hip=True, extra=""):
        if pose == "half_kneel":            # the in-between of kneeling down
            fig, pts = half_kneel_fig(H_X, PLINTH_TOP, H_S, "man", HV, facing, attire, expr)
            pel = pts["pelvis"]
        else:
            fig = C.citizen(H_X, PLINTH_TOP, H_S, facing, kind="man", variant=HV, pose=pose, attire=attire, expr=expr)
            pel = C.body_points(C.citizen, H_X, PLINTH_TOP, H_S, facing, kind="man", variant=HV, pose=pose,
                                attire=attire)["pelvis"]
        if horn_at_hip:
            extra += hip_horn_markup(pel[0] - facing * 6 * H_S, pel[1] + 4 * H_S, H_S, -facing)
        return doc(hsh + fig + extra)
    hhead = C.body_points(C.citizen, H_X, PLINTH_TOP, H_S, 1, kind="man", variant=HV, pose="listen")["head"]
    horn = horn_svg(hhead[0] + 15 * H_S, hhead[1] + 20 * H_S, H_S, 1)
    hfr = [herald(-1, "stand", expr="worried"), herald(-1, "listen"), herald(-1, "listen", expr="surprised"),
           herald(-1, "stand", expr="sorry"), herald(1, "listen", expr="neutral", horn_at_hip=False, extra=horn),
           herald(1, "point", expr="call"), herald(1, "sad", "sackcloth"),
           herald(1, "half_kneel", "sackcloth", "sorry"), herald(1, "kneel_pray", "sackcloth", "sorry")]
    th = [snap(t_heard + 0.3), snap(t_wow + 0.1), snap(t_believe + 0.2), t_horn, t_call, snap(t_change + 0.36),
          snap(t_kneel + 0.52)]
    th.append(th[6] + HALF_HOLD)
    sc.add("herald", hfr, z=11, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(th)]),
           motion=M.combine(dip(th[0], H_S, hp, 4), hop(th[1], [(0, {"dy": 0}), (0.1, {"dy": -5}), (0.22, {"dy": 0})],
                                                         hp),
                            look_up(t_up + 0.08, hp, -1, 3.0, 4, hold_up),
                            dip(th[2], H_S, hp, 4), nod(th[2] + 0.05, hp, 1.5, 2), dip(t_horn, H_S, hp),
                            hop(t_horn + 0.3, [(0, {"rot": 0}), (0.4, {"rot": -2.5}), (0.9, {"rot": -2.5}),
                                               (1.1, {"rot": 0})], hp),
                            dip(t_call, H_S, hp), kneel_down(th[6], hp, kneel_heights("man", HV), KNEEL_TILT),
                            M.breathe(0.009, 2.9, pivot=hp, phase=0.4)))
    bell = (hhead[0] + 15 * H_S + 146 * H_S + 26 * H_S, hhead[1] + 20 * H_S - 78 * H_S - 22 * H_S)
    sc.add("horn_toot", [toot_svg(bell[0], bell[1], k) for k in (0, 1, 2)], z=30, wc=0,
           frame_at=lambda t: float(int(t * 9) % 3),
           motion=M.keys([(t_horn + 0.12, {"alpha": 0}), (t_horn + 0.22, {"alpha": 1}), (t_call - 0.12, {"alpha": 1}),
                          (t_call, {"alpha": 0})], "sine"))
    hb = C.body_points(C.citizen, H_X, PLINTH_TOP, H_S, 1, kind="man", variant=HV, pose="point")["head"]
    sc.add("herald_arcs", [arcs_svg(hb[0] + 34 * H_S, hb[1] + 14 * H_S, 1, k, 1.0) for k in (1, 2, 3)], z=30, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_call, {"alpha": 0}), (t_call + 0.15, {"alpha": 1}), (t_change - 0.25, {"alpha": 1}),
                          (t_change, {"alpha": 0})], "sine"))
    puffs_at.append((th[5], H_X, PLINTH_TOP - 110 * H_S * 1.4, 0.45 * 310 * H_S, 0.6 * 310 * H_S, H_S))

    # ---- market stall: back posts, merchant, table with food, the thrown cloth, awning ----
    sc.add("stall_back", stall_back_svg(), z=13)
    rp = (R_X, R_Y)

    def merchant(pose, attire="normal", expr=None, facing=-1, under=""):
        return doc(under + C.citizen(R_X, R_Y, R_S, facing, kind="man", variant=1, pose=pose, attire=attire,
                                     expr=expr))
    rhands = C.body_points(C.citizen, R_X, R_Y, R_S, -1, kind="man", variant=1, pose="cheer")["hands"]
    rfr = [merchant("stand", expr="worried"), merchant("listen"), merchant("listen", expr="surprised"),
           merchant("stand", expr="sorry"),
           merchant("cheer", expr="neutral", under=held_sheet_markup(rhands[0], rhands[1], R_S)),   # lifts the cloth
           merchant("cheer", expr="neutral"),                                                 # ... throws it
           merchant("stand", expr="sorry"), merchant("sad", "sackcloth"),
           doc(half_kneel_fig(R_X, R_Y, R_S, "man", 1, 1)[0]),            # kneeling down (in-between)
           merchant("kneel_pray", "sackcloth", "sorry", facing=1)]
    tr = [snap(t_heard + 0.05), snap(t_wow + 0.05), snap(t_believe), t_hold, t_rel, snap(t_land + 0.12),
          snap(t_change + 0.9), snap(t_kneel + 0.36)]
    tr.append(tr[7] + HALF_HOLD)
    m_motion = M.combine(dip(tr[0], R_S, rp, 4), look_up(t_up + 0.04, rp, -1, 4.0, 6, hold_up),
                         dip(tr[2], R_S, rp, 4), nod(tr[2] + 0.05, rp, 2.0, 2), dip(t_hold, R_S, rp, 6),
                         hop(t_rel - 0.06, [(0, {"dy": 0, "rot": 0}), (0.08, {"dy": -6, "rot": -1.5}),
                                            (0.26, {"dy": 0, "rot": 0})], rp),
                         dip(tr[5], R_S, rp, 4), kneel_down(tr[7], rp, kneel_heights("man", 1), KNEEL_TILT),
                         M.breathe(0.008, 3.3, pivot=rp, phase=0.7))
    sc.add("merchant", rfr, z=14, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tr)]),
           motion=m_motion)
    puffs_at.append((tr[6], R_X, R_Y - 200, 120, 150, R_S))
    sc.add("table", table_svg(), z=15)
    ap = tpt((TABLE_X0 + TABLE_X1) / 2, 714)
    # the flat sheet flies forward and down out of his hands (no fade: it appears as the roll leaves his hands);
    # on landing it is cut to the cloth moulded over the food, with a small squash
    sc_ = tpt(*SHEET_C)
    hmid = ((rhands[0][0] + rhands[1][0]) / 2, (rhands[0][1] + rhands[1][1]) / 2)
    fly = M.keys([(t_rel, {"dx": hmid[0] - sc_[0], "dy": hmid[1] - 50 - sc_[1], "sx": 0.5, "sy": 0.62, "rot": -5}),
                  (t_rel + 0.14, {"dx": (hmid[0] - sc_[0]) * 0.5, "dy": (hmid[1] - sc_[1]) * 0.55 - 30, "sx": 0.8,
                                  "sy": 0.85, "rot": 3}),
                  (t_land, {"dx": 0, "dy": 0, "sx": 1.0, "sy": 1.0, "rot": 0})], ["out", "in"], pivot=sc_)
    sc.add("sheet", sheet_svg(), z=15.4,
           motion=lambda t: fly(t) if t_rel <= t < t_land else Tf(alpha=0))
    hem = tpt((TABLE_X0 + TABLE_X1) / 2, 1150)
    squash = M.keys([(t_land, {"sx": 1.035, "sy": 0.9}), (t_land + 0.16, {"sx": 1.0, "sy": 1.0})], "out", pivot=hem)
    sc.add("cover", cover_svg(), z=15.5, motion=lambda t: squash(t) if t >= t_land else Tf(alpha=0))
    sc.add("awning", awning_svg(), z=16, motion=lambda t: Tf(sy=1 + 0.006 * math.sin(t * 2.3), px=ap[0], py=ap[1]))

    # ---- the four in front: the elder, the mother, her little girl (and the merchant behind his table) ----
    # The three start where s15's last frame leaves them (m15), in its poses (the mother and the elder listening,
    # hand to chin; the girl sad). The mother and the girl take two little steps forward to their places; the elder
    # walks over in front of the square to Jonah's step and stops, surprised, on "竟然".
    ep = (E_X, E_Y)

    def elder(pose, attire="normal", expr=None, facing=-1, stick=False):
        st = stick_leaning(E_X, E_Y, E_S, facing) if stick else ""
        return doc(st + person("elder", 0, E_X, E_Y, E_S, facing, pose, attire, expr))
    efr = [elder("stand", expr="worried"), elder("listen"), elder("listen", expr="surprised"),
           elder("stand", expr="sorry"), elder("sad", "sackcloth"),
           elder("half_kneel", "sackcloth", "sorry", facing=1),          # kneeling down, leaning on his stick
           elder("kneel_pray", "sackcloth", "sorry", facing=1, stick=True)]
    te = [snap(t_heard - 0.1), snap(t_wow), snap(t_believe - 0.05), snap(t_change), snap(t_kneel)]
    te.append(te[4] + HALF_HOLD)
    e_cut = cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(te)])
    # his walk (s15's planted-foot gait: one drawing advances 2 A / WALK_N figure px, so the planted sole stays put;
    # he sets off from and arrives at a passing drawing, feet together like his standing drawing)
    ex0, ey0 = m15(*S15_ELDER[:2])
    es0 = S15_ELDER[2] * M15_K
    t_ea, t_eb = snap(0.92), te[1]
    NW, K0 = 42, 3

    def e_at(u):
        """His path (u: 0..1 across the square): he keeps behind the mother and the girl (his head shows over
        theirs) and comes forward only once past them; his scale follows his depth."""
        y = ey0 + (E_Y - ey0) * u ** 2.5
        return ex0 + (E_X - ex0) * u, y, es0 + (E_S - es0) * (y - ey0) / (E_Y - ey0)
    # equal figure-px strides: drawing i sits at 1/NW-th steps of the distance walked in figure px (stage px / scale)
    us = [j / 2000 for j in range(2001)]
    dist = [0.0]
    for ua, ub in zip(us, us[1:]):
        dist.append(dist[-1] + abs(E_X - ex0) * (ub - ua) / e_at((ua + ub) / 2)[2])
    epath, j = [], 0
    for i in range(NW + 1):
        d = dist[-1] * i / NW
        while j < 1999 and dist[j + 1] < d:
            j += 1
        u = us[j] + (us[j + 1] - us[j]) * (d - dist[j]) / max(1e-9, dist[j + 1] - dist[j])
        epath.append(e_at(min(1.0, u)))
    A_e = dist[-1] / NW * S15.WALK_N / 2
    lk_e = leg_k("elder")
    esh = C.ground_shadow(E_X, E_Y, E_S, 110, opacity=0.2)
    egait = [doc(esh + gait_fig(E_X, E_Y, E_S, "elder", 0, -1, S15.walk_pose(k, A=A_e, lk=lk_e)))
             for k in range(12)]

    def e_walk_i(t):
        return min(NW, int((t - t_ea) * NW / (t_eb - t_ea) + 1e-6))

    def e_frame(t):
        if t < t_ea:
            return 0.0                                       # listening, as s15 leaves him
        if t < t_eb:
            return float(1 + (K0 + e_walk_i(t)) % 12)
        return 13.0 + e_cut(t)

    def e_path(t):
        x, y, s = epath[0 if t < t_ea else (e_walk_i(t) if t < t_eb else NW)]
        return Tf(dx=x - E_X, dy=y - E_Y, sx=s / E_S, sy=s / E_S, px=E_X, py=E_Y)
    sc.add("elder", [efr[1]] + egait + efr, z=20, frame_at=e_frame,
           motion=M.combine(e_path, dip(t_ea, E_S, ep, 3),
                            hop(te[1], [(0, {"dy": 0}), (0.1, {"dy": -7}), (0.22, {"dy": 0})], ep),
                            look_up(t_up, ep, -1, hold=hold_up), dip(te[2], E_S, ep, 4),
                            nod(te[2] + 0.05, ep, 2.4, 2), kneel_down(te[4], ep, kneel_heights("elder", 0), KNEEL_TILT),
                            M.breathe(0.008, 3.6, pivot=ep, phase=0.1)))
    puffs_at.append((te[3], E_X, E_Y - 160, 130, 180, E_S))

    wp = (W_X, W_Y)

    def mother(pose, attire="normal", expr=None, facing=-1):
        return doc(person("woman", 2, W_X, W_Y, W_S, facing, pose, attire, expr))
    wfr = [mother("listen"), mother("listen"), mother("listen", expr="surprised"),      # listening, as s15 ends
           mother("stand", expr="sorry"), mother("sad", "sackcloth"), mother("half_kneel", "sackcloth", "sorry", 1),
           mother("kneel_pray", "sackcloth", "sorry", 1)]
    tw = [snap(t_heard + 0.15), snap(t_wow + 0.08), snap(t_believe + 0.1), snap(t_change + 0.23),
          snap(t_kneel + 0.2)]
    tw.append(tw[4] + HALF_HOLD)
    t_sigh = t_rough + 0.55
    wx0, wy0 = m15(*S15_MOTHER[:2])
    sc.add("mother", wfr, z=20.5, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tw)]),
           motion=M.combine(step_in(snap(1.12), (wx0, wy0, S15_MOTHER[2] * M15_K), wp, W_S, n=3, dur=0.3),
                            hop(tw[1], [(0, {"dy": 0}), (0.1, {"dy": -7}), (0.22, {"dy": 0})], wp),
                            look_up(t_up + 0.06, wp, -1, hold=hold_up), dip(tw[2], W_S, wp, 4),
                            nod(tw[2] + 0.05, wp, 2.4, 2), kneel_down(tw[4], wp, kneel_heights("woman", 2), KNEEL_TILT),
                            # a sigh: the chest rises, then the shoulders drop and the head dips
                            hop(t_sigh, [(0, {"sy": 1, "dy": 0}), (0.45, {"sy": 1.03, "dy": 0}),
                                         (0.95, {"sy": 0.978, "dy": 2}), (1.4, {"sy": 1, "dy": 0})], wp),
                            M.breathe(0.009, 3.2, pivot=wp, phase=0.5)))
    puffs_at.append((tw[3], W_X, W_Y - 160, 125, 175, W_S))

    kp = (K_X, K_Y)

    def kid(pose, facing=-1, attire="normal", expr=None):
        return doc(person("child", 1, K_X, K_Y, K_S, facing, pose, attire, expr))
    kfr = [kid("sad"),                                                    # sad, as s15 leaves her
           kid("listen"), kid("listen", expr="surprised"), kid("stand", expr="sorry"),
           kid("point", 1, expr="happy"), kid("stand", 1, expr="surprised"), kid("stand", 1, expr="sorry"),
           kid("sad", -1, "sackcloth"), kid("half_kneel", 1, "sackcloth", "sorry"),
           kid("kneel_pray", 1, "sackcloth", "sorry"), kid("kneel_pray", 1, "sackcloth", "peaceful")]
    tk = [snap(t_heard + 0.3), snap(t_wow + 0.15), snap(t_believe + 0.2), t_reach, t_back, t_okay, snap(t_kid),
          snap(t_kneel + 0.28)]
    tk += [tk[7] + HALF_HOLD, snap(t_hope + 0.12)]
    t_wrig = t_rough + 0.02
    wrig = [(0, {"rot": 0, "sy": 1})]
    for j, r in enumerate((6, -6, 5, -5, 3)):
        wrig.append((0.13 * (j + 1), {"rot": r, "sy": 0.97 if j % 2 == 0 else 0.985}))
    wrig.append((0.13 * 6 + 0.06, {"rot": 0, "sy": 1}))
    kx0, ky0 = m15(*S15_GIRL[:2])
    sc.add("kid", kfr, z=21, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tk)]),
           motion=M.combine(step_in(snap(1.3), (kx0, ky0, S15_GIRL[2] * M15_K), kp, K_S, dur=0.28, lift=11.0),
                            dip(tk[0], K_S, kp, 4), hop(tk[1], [(0, {"dy": 0}), (0.1, {"dy": -8}), (0.22, {"dy": 0})],
                                                         kp),
                            look_up(t_up + 0.1, kp, -1, 6.0, 8, hold_up), dip(tk[2], K_S, kp, 4),
                            nod(tk[2] + 0.05, kp, 3, 2),
                            dip(t_reach, K_S, kp, 5),
                            hop(t_back, [(0, {"dy": 0, "rot": 0}), (0.08, {"dy": -10, "rot": -3}),
                                         (0.22, {"dy": 0, "rot": 0})], kp),
                            nod(t_okay + 0.05, kp, 4, 2, 0.34, facing=1),
                            # scratchy sackcloth: a wriggle with shrugging shoulders
                            hop(t_wrig, wrig, kp),
                            kneel_down(tk[7], kp, kneel_heights("child", 1), KNEEL_TILT),
                            M.breathe(0.012, 2.6, pivot=kp, phase=0.3)))
    puffs_at.append((tk[6], K_X, K_Y - 110, 90, 120, K_S))
    ksh = C.body_points(C.citizen, K_X, K_Y, K_S, -1, kind="child", variant=1, pose="sad", attire="sackcloth")
    kb = ksh["bbox"]
    marks = [(kb[0] - 20, K_Y - 142 * K_S, -1), (kb[0] - 30, K_Y - 84 * K_S, -1)]   # her open side (post on the right)
    sc.add("kid_itch", [scratch_svg(marks, k, 1.5) for k in range(3)], z=30, wc=0,
           frame_at=lambda t: float(int(t * 8) % 3),
           motion=M.keys([(t_wrig, {"alpha": 0}), (t_wrig + 0.08, {"alpha": 1}), (t_wrig + 0.7, {"alpha": 1}),
                          (t_wrig + 0.9, {"alpha": 0})], "sine"))

    # ---- cloth-puffs over every sackcloth change ----
    for i, (tp, x, y, rx, ry, s) in enumerate(puffs_at):
        sc.add(f"puff{i}", doc(puff_svg(x, y, rx, ry, seed=i + 3, k=max(0.6, s))), z=25 + 0.01 * i, wc=0.5,
               motion=puff_motion(tp, (x, y)))

    for name, tp, body, pv in group_puffs:
        sc.add(f"puffs_{name}", doc(body), z=25.5, wc=0.5, motion=hop(tp, [
            (-0.06, {"alpha": 0, "s": 0.97, "dy": 0}), (0.02, {"alpha": 1, "s": 0.99, "dy": -3}),
            (0.16, {"alpha": 0.85, "s": 1.015, "dy": -9}), (0.38, {"alpha": 0, "s": 1.03, "dy": -18})], pv,
            ["out", "sine", "in"]))

    # ---- foreground framing: the well in the front-left corner, clear of Jonah's step, and s15's own near things
    # (its flowering bush and grass at the lower right) ----
    fg15_defs, fg15 = fg15_markup()
    fg = (well_svg(236, 1318) + PR.grass_tuft(60, SH + 4, 1.1, variant=2) + PR.jar(420, SH - 26, 0.78) + fg15)
    sc.add("fg", doc(fg, fg15_defs), z=16.9)

    # ---- light: a brief warm patch in the sky as they believe; the solemn dusk while they change and kneel;
    # then a soft warm glow and faint rays from behind the cloud at the upper right, where they kneel facing ----
    sc.add("believe_glow", glaze_svg("believe"), z=0.45, wc=0,
           motion=M.keys([(t_up - 0.15, {"alpha": 0}), (t_up + 0.45, {"alpha": 1}), (c0b.end - 0.1, {"alpha": 0.8}),
                          (c0b.end + 0.45, {"alpha": 0})], "sine"))
    sc.add("dusk", glaze_svg("dusk"), z=40, wc=0, blend="multiply",
           motion=M.keys([(t_change - 0.4, {"alpha": 0}), (t_kneel + 0.5, {"alpha": 1}),
                          (t_hope, {"alpha": 1}), (t_hope + 1.6, {"alpha": 0.6})], "sine"))
    sc.add("gleam", glaze_svg("gleam"), z=0.46, wc=0,
           motion=M.combine(with_cloud, M.keys([(t_hope - 0.3, {"alpha": 0}), (t_hope + 1.6, {"alpha": 1})], "sine"),
                            M.pulse(0.9, 1.0, 3.6)))
    sc.add("hope", glaze_svg("hope"), z=41, wc=0, blend="screen",
           motion=M.combine(M.keys([(t_hope - 0.2, {"alpha": 0}), (t_hope + 1.5, {"alpha": 1})], "sine"),
                            M.pulse(0.88, 1.0, 3.2)))
    # s15's late-afternoon light (its light_fx multiplies its frame by this gold) eases off with its sky
    sc.add("gold15", doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="{S15_GOLD}"/>'), z=45,
           wc=0, blend="multiply", motion=sky15_a)
    ray_src = (GLOW_C[0] - 20, 345)
    sc.add("rays", rays_svg(ray_src, 118, 46, n=3), z=40.8, wc=0, blend="screen",
           motion=M.combine(with_cloud, M.keys([(t_hope + 0.1, {"alpha": 0}), (t_hope + 1.9, {"alpha": 0.8})],
                                                 "sine"), M.pulse(0.75, 1.0, 4.1, 0.3)))

    # ---- camera: a slow push in (line 0), a gentle widening for the horn, the fast and the sackcloth wave, a
    # small push toward the mother and girl, then one slow pull-out to the whole kneeling square (calm hold) ----
    A = Cam(1105, 745, 1900)      # Jonah lands where s15 leaves him (~output x 420, feet ~835)
    B = Cam(1110, 800, 1700)
    Cw = Cam(1180, 785, 1960)
    D = Cam(1150, 805, 1820)
    E = Cam(1190, 785, 2000)
    sc.camera = M.cam_keys([
        (0, A), (c0a.start, A), (t_believe + 0.3, B), (t_horn - 0.1, B), (t_change + 0.4, Cw), (t_change + 0.7, Cw),
        (t_rough + 1.4, D), (t_kneel + 0.1, D), (t_kneel + 3.0, E), (T, E),
    ], ["sine", "sine", "sine", "inout", "sine", "inout", "sine", "inout", "sine"])

    # ---- effects ----
    sc.fx = [
        FX.motes((0, 300, SW, 1200), count=26, t0=-1, t1=T + 1, color=(255, 238, 200), size=(3, 6), alpha=110,
                 seed=31),
        # (sparkles drift up by 14 px/s of absolute time; the rect is placed for t ~ 5)
        FX.sparkles((760, 400, 1760, 720), count=8, t0=t_up - 0.1, t1=t_up + 1.9, color=(255, 212, 120),
                    size=(20, 32), drift=-14, seed=33),
        FX.sparkles((1480, 380, 2260, 760), count=8, t0=t_hope + 0.4, t1=T + 1, color=(255, 214, 130),
                    size=(14, 24), drift=-10, period=2.2, seed=37),
    ]

    # ---- sound ----
    sc.sfx("crowd", 0, dur=t_change + 1.0, gain_db=-20, fade_in=0.8, fade_out=1.4)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("sparkle", t_up - 0.05, gain_db=-15)
    sc.sfx("horn", t_horn + 0.12, dur=t_call - t_horn + 0.05, gain_db=-14, pan=0.1, fade_out=0.35)
    sc.sfx("cloth", t_rel - 0.04, gain_db=-9, pan=0.4)
    sc.sfx("cloth", t_change + 0.05, gain_db=-12, pan=-0.2)
    sc.sfx("cloth", t_kid, gain_db=-12, pan=0.2)
    sc.sfx("sparkle", t_hope + 0.3, gain_db=-14)
    return sc
