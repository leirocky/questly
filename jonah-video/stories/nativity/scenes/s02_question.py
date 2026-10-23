"""Scene 2 - the opening question, at home on a warm December evening: a little boy in a red Christmas jumper is
decorating the Christmas tree in the living room (night sky and moon in the window, the calendar on the wall showing
12月 with the 25th circled, presents, the little nativity set under the tree with its manger still empty - the baby is
put in on Christmas, in s12). The star for the top of the tree waits on his little step stool.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame (1 s cross-dissolve from the title page): the boy reaches forward and hangs a red bauble,
               the tree lights twinkle, the moon shines in the window
  '小朋友'      the bauble stays on the branch (pop); he turns round to us, smiling (squash-dip hides the cut)
  '你过生日的时候' a thought bubble rises from him (three little puffs, then the cloud): a birthday cake with candles
               (flames flicker) and balloons (they bob); he smiles up at it
  '最开心的是什么' a big happy face: he cheers with both arms up and a little hop (sparkle); the 0.8 s pause holds
               the joy; the bubble pops away as the pause starts
  pause        he turns back and picks the star up from the stool
  '圣诞节'      the 25 on the calendar twinkles; he holds the star up, hops onto the stool and reaches up: the star
               goes on the top of the tree and lights up (chime), warm light spreads
  '给耶稣过生日' little birthday-candle flames light one by one round the tree star (sparkle)
  '今天'        he turns to us on his stool, smiling; small nods on '我们就来听听'
  '耶稣是怎么出生的' he looks up at the star; the camera pushes gently toward the glowing star and holds a calm frame
               for the page turn into s03 (another illustrator)

Shared with s12_end (same illustrator, same room, props and boy): room geometry, boy(), topper_svg(), the drawings.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import (Fig, arc_jump, beat, breath, dip, doc, f1, glow_svg, hop, keyed,
                                               snap)

INK = P["ink"]

# ---------------------------------------------------------------- room geometry (shared with s12_end)
FLOOR = 985                         # the boy's / stool's floor line
TREE = (1200, 972, 1.15)            # christmas_tree anchor (tub bottom) and scale
TOP = (TREE[0] + PR.CHRISTMAS_TREE_TOP[0] * TREE[2], TREE[1] + PR.CHRISTMAS_TREE_TOP[1] * TREE[2])   # (1200, 475)
BOY_S = 1.65
STAR_R = 24                          # the star's radius in the boy's local units (r = 40 stage px)
STAR_OFF = (65.4, -193.3)            # star centre in 'decorate' (far hand (59.4, -177.3) + (6, -16)), local
STOOL_X = TOP[0] - STAR_OFF[0] * BOY_S                     # 1092: his anchor on the top step
STOOL_TOP = TOP[1] - STAR_OFF[1] * BOY_S                   # 794: the top step
STEP1 = (STOOL_X - 80, (FLOOR + STOOL_TOP) / 2)             # the lower step (his anchor there)
BOY_X, BOY_Y = STEP1                                       # he starts on the low step
WINDOW_X = 420
CAL = (1680, 300, 1.0)
CAL_25 = None                        # stage point of the circled 25 (computed below)
SET = (1300, 978, 0.55)              # the little nativity set under the tree
GIFTS = (1610, 984, 0.95)
SET_FIGS = ("star", "angel", "ox", "donkey", "joseph", "mary", "shepherd", "sheep")   # the manger still empty
FIG_K = 0.9                          # the baby-in-the-manger figurine's size relative to the set (it is the centrepiece)

# baubles already on the tree (tree-local positions and colours) and the one he hangs
BAUBLES = [(40, -100, "#e9c35c"), (130, -84, "#3f62a2"), (-50, -176, "#e9c35c"), (90, -190, "#d9453f"),
           (-70, -272, "#3f62a2"), (66, -280, "#e9c35c"), (-24, -340, "#f2ead8"),
           (34, -352, "#d9453f"), (150, -150, "#f2ead8")]
BAUBLE_R = 17                        # stage px (the held bauble is drawn the same size)
HANG_ARM = ("fk", 95, 100)           # his arm reaching forward to hang the bauble


def cal_25():
    """Stage point of the 25 on the calendar (same layout maths as props.calendar)."""
    x, y, s = CAL
    k = 25 - 1 + 2
    col, row = k % 7, k // 7
    return (x + (-103 + col * 34) * s, y + (150 + row * 40 - 7) * s)


# ================================================================== the boy (custom fronts for his items)

C.EXPRS.setdefault("nq_up", dict(C.EXPRS["joyful"], look=(-0.02, -0.12)))
C.EXPRS.setdefault("nq_us", dict(C.EXPRS["happy"], look=(0.0, 0.02)))
C.EXPRS.setdefault("nq_blink", dict(C.EXPRS["happy"], eyes="closed"))

_KH = dict(C._NC_POSES["kneel_look"])
_KH.update(arms=C._SC_POSES["hug_pillow"]["arms"], hands=("open", "open"), expr="joyful", h=2, look=(0.03, -0.04))
_PF = dict(C._NC_POSES["place"])
_PF.update(t=30, h=10, arms=(("fk", 80, 75), ("fk", 75, 70)), look=(0.04, 0.1))
_CUSTOM = {
    "kneel_hug": _KH,
    "place_far": _PF,
    "hang": C._P(t=8, h=-6, legs=((6, 2), (-5, -2)), arms=(HANG_ARM, ("fk", -10, -4)), hands=("fist", "fist"),
                 look=(0.05, -0.02), expr="happy"),
    "pick": C._P(t=12, h=10, legs=((6, 2), (-5, -2)), arms=(("fk", 62, 42), ("fk", 40, 30)), hands=("fist", "open"),
                 look=(0.05, 0.08), expr="happy"),
}


def _star4(c, r, lw=2.4, glow=0.0, key="nqs"):
    out = C._glow_disc(c, r * 3.2, r * 3.2, glow, key) if glow > 0 else ""
    out += C._sparkle(c, r, "#f2c94e", lw)
    out += f'<circle cx="{f1(c[0] - r * 0.12)}" cy="{f1(c[1] - r * 0.18)}" r="{f1(r * 0.14)}" fill="#fffaf0" opacity="0.8"/>'
    return out


def _bauble_local(c, col, r):
    """A bauble hanging under point c (its cap and loop at c), radius r (local px)."""
    x, y = c
    return (f'<path d="M{f1(x)},{f1(y)} l1,{f1(r * 0.7)}" stroke="{INK}" stroke-width="1.8" fill="none"/>'
            f'<rect x="{f1(x - r * 0.3)}" y="{f1(y + r * 0.62)}" width="{f1(r * 0.6)}" height="{f1(r * 0.42)}" rx="2" '
            f'fill="#e9c35c" stroke="{INK}" stroke-width="1.8"/>'
            f'<circle cx="{f1(x + 1)}" cy="{f1(y + r * 2)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="2.8"/>'
            f'<circle cx="{f1(x - r * 0.3)}" cy="{f1(y + r * 1.65)}" r="{f1(r * 0.28)}" fill="#fffaf0" opacity="0.8"/>')


def _front(D, pose, item):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        s = ""
        if pose in ("decorate", "hang", "pick"):
            if item == "star":
                if pose == "pick":
                    s += _star4((W0[0] + 10, W0[1] + 2), STAR_R)
                else:
                    s += _star4((W0[0] + 6, W0[1] - 16), STAR_R)
            elif item == "bauble":
                s += _bauble_local((W0[0] + 1, W0[1] + 4), "#d9453f", BAUBLE_R / BOY_S)
            s += C._fist(W0, hr, D["skin"])
        elif pose == "hold_star":
            c = ((W0[0] + W1[0]) / 2 + 12, min(W0[1], W1[1]) - 20)
            if item == "star":
                s += _star4(c, STAR_R, glow=0.55, key="nqhs")
            s += C._hand(W0, (0.5, -0.9), "open", D["skin"], hr) + C._hand(W1, (0.3, -1.0), "open", D["skin"], hr)
        elif pose in ("place", "place_far"):
            if item:
                c = ((W0[0] + W1[0]) / 2, max(W0[1], W1[1]) + 6)
                k = FIG_K * SET[2] / BOY_S         # the size it has in the set
                s += f'<g transform="translate({f1(c[0])},{f1(c[1])}) scale({k:.4f})">{PR._nativity_figure(item)}</g>'
            s += C._hand(W0, (0.3, 1.0), "open", D["skin"], hr) + C._hand(W1, (0.3, 1.0), "open", D["skin"], hr)
        return s
    return front


def boy(x, y, pose="stand", expr=None, facing=1, item=None, s=BOY_S, marks=True):
    """The jumper boy (characters.child(outfit='jumper')), with his own items drawn at matching sizes: 'hang' (arm
    forward with a bauble), 'pick' (lifting the star off the stool), 'decorate' / 'hold_star' / 'place' with
    item='star' / 'bauble' / a nativity figure / None (empty hands). Other poses: characters.child as is."""
    if pose in _CUSTOM or pose in C._NC_POSES:
        ps = dict(_CUSTOM.get(pose) or C._NC_POSES[pose])
        D, m = C._jumper_design(), C._metrics(C._CHILD, 1.0, 0.98)
        D["front"] = _front(D, pose, item)
        e = expr or ps["expr"]
        inner, _ = C._figure(D, m, ps, e, C._fsign(facing), marks)
        return C._wrap_out(inner, x, y, s, facing, f"nq-boy-{pose}-{item}")
    return C.child(x, y, s, facing, pose=pose, expr=expr, outfit="jumper", marks=marks)


def boy_points(x, y, pose, expr=None, facing=1, item=None, s=BOY_S):
    """characters.body_points for boy()."""
    return C.body_points(lambda x_, y_, s_, f_, **kw: boy(x_, y_, pose, expr, f_, item, s_), x, y, s, facing)


def boy_shadow(x, y, w=150):
    return (f'<ellipse cx="{f1(x)}" cy="{f1(y + 3)}" rx="{f1(w / 2)}" ry="14" fill="#6a4128" opacity="0.28" '
            f'filter="url(#soft)"/>')


# ================================================================== drawings

def room_svg(glow=0.7):
    out = PR.living_room(-40, W + 40, FLOOR, 1.0, glow=glow, window_x=WINDOW_X, time="night", seed=2)
    out += PR.calendar(*CAL, circled=1.0)
    return doc(out)


def tree_svg(k, n=4):
    x, y, s = TREE
    return doc(f'<ellipse cx="{x}" cy="{y + 4}" rx="150" ry="18" fill="#6a4128" opacity="0.3" filter="url(#soft)"/>' +
               PR.christmas_tree(x, y, s, 1, lights=1.0, twinkle=k / n, star=0.0, top_star=False, ornaments=0.0))


def tree_pt(lx, ly):
    x, y, s = TREE
    return (x + lx * s, y + ly * s)


def baubles_svg(extra=()):
    """The baubles already on the tree (their caps on the branch tips), plus ``extra`` stage points (hung ones)."""
    b = ""
    for lx, ly, col in BAUBLES:
        x, y = tree_pt(lx, ly)
        b += _bauble_local((x, y - BAUBLE_R * 1.7), col, BAUBLE_R)
    for (x, y), col in extra:
        b += _bauble_local((x, y), col, BAUBLE_R)
    return doc(S.g(b, filter="wobble-fine"))


def hang_point():
    """Where the bauble hangs from his hand in the 'hang' pose (stage)."""
    W0 = boy_points(BOY_X, BOY_Y, "hang", item="bauble")["hands"][0]
    return (W0[0] + 1 * BOY_S, W0[1] + 4 * BOY_S)


def hung_bauble_svg():
    return baubles_svg_only([(hang_point(), "#d9453f")])


def baubles_svg_only(items):
    b = ""
    for (x, y), col in items:
        b += _bauble_local((x, y), col, BAUBLE_R)
    return doc(S.g(b, filter="wobble-fine"))


def stool_body(x=None, y=FLOOR):
    """His little wooden two-step stool (side view: the low step on the left, the red top step on the right)."""
    x = STOOL_X if x is None else x
    top = STOOL_TOP + (y - FLOOR)
    mid = (y + top) / 2
    wood, dark = "#c08a58", "#9a6a42"
    st = f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"'
    out = f'<ellipse cx="{f1(x - 20)}" cy="{f1(y + 3)}" rx="120" ry="13" fill="#6a4128" opacity="0.3" filter="url(#soft)"/>'
    # back legs (behind), then the front frame
    out += f'<path d="M{f1(x + 46)},{f1(top + 8)} L{f1(x + 70)},{f1(y)} L{f1(x + 54)},{f1(y)} L{f1(x + 32)},{f1(top + 8)} Z" fill="{dark}" {st}/>'
    out += f'<path d="M{f1(x - 40)},{f1(top + 8)} L{f1(x - 118)},{f1(y)} L{f1(x - 100)},{f1(y)} L{f1(x - 24)},{f1(top + 8)} Z" fill="{dark}" {st}/>'
    out += f'<path d="M{f1(x + 56)},{f1(top + 8)} L{f1(x + 86)},{f1(y)} L{f1(x + 68)},{f1(y)} L{f1(x + 40)},{f1(top + 8)} Z" fill="{wood}" {st}/>'
    out += f'<path d="M{f1(x - 30)},{f1(top + 8)} L{f1(x - 106)},{f1(y)} L{f1(x - 88)},{f1(y)} L{f1(x - 14)},{f1(top + 8)} Z" fill="{wood}" {st}/>'
    # the low step (left) and a brace
    sx1 = x - (STOOL_X - STEP1[0])
    out += f'<rect x="{f1(sx1 - 54)}" y="{f1(mid - 4)}" width="104" height="16" rx="5" fill="#c8443e" {st}/>'
    out += f'<path d="M{f1(sx1 - 46)},{f1(mid + 1)} L{f1(sx1 + 30)},{f1(mid + 1)}" stroke="#e8766a" stroke-width="3.4" stroke-linecap="round" opacity="0.8"/>'
    out += f'<rect x="{f1(x - 20)}" y="{f1(mid + 40)}" width="84" height="11" rx="4" fill="{S.shade(wood, -0.1)}" {st}/>'
    # the top step
    out += f'<rect x="{f1(x - 62)}" y="{f1(top - 4)}" width="126" height="20" rx="7" fill="#c8443e" {st}/>'
    out += f'<path d="M{f1(x - 52)},{f1(top + 1)} L{f1(x + 34)},{f1(top + 1)}" stroke="#e8766a" stroke-width="4" stroke-linecap="round" opacity="0.8"/>'
    return S.g(out, filter="wobble-fine")


STOOL_STAR = (STOOL_X + 50, STOOL_TOP - 30)                 # the star waits on the top step


def stool_star_svg():
    x, y = STOOL_STAR
    r = STAR_R * BOY_S
    return doc(S.g(f'<g transform="rotate(-24 {f1(x)} {f1(y)})">{_star4((x, y), r, lw=2.4 * BOY_S)}</g>',
                   filter="wobble-fine"))


def topper_svg(level, rot=0.0):
    """The star on the top of the tree (the same star the boy carries), glowing at ``level`` 0..1."""
    x, y = TOP
    r = STAR_R * BOY_S
    out = ""
    if level > 0:
        out += PR._warm_glow(x, y, 230 * (0.6 + 0.4 * level), 230 * (0.6 + 0.4 * level), level, "nqtop",
                             PR.STAR_CORE, PR.STAR_GOLD)
        out += (f'<path d="{S.rays(x, y, 40, 150 + 60 * level, n=12, width_deg=5, rot=rot)}" fill="{PR.STAR_CORE}" '
                f'opacity="{0.32 * level:.2f}" filter="url(#soft)"/>')
    star = _star4((x, y), r, lw=2.4 * BOY_S)
    if level > 0:
        star += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.3)}" fill="#fffbea" opacity="{0.8 * level:.2f}"/>'
    return doc(S.g(out, filter="wobble") + S.g(star, filter="wobble-fine"))


def set_svg(figs=SET_FIGS, glow=0.0):
    return doc(PR.nativity_set(*SET, figures=figs, glow=glow))


def gifts_svg():
    x, y, s = GIFTS
    return doc(PR.presents(x, y, s, n=5, seed=1))


def box_svg():
    """A little cardboard box of decorations at his heels (tinsel and two baubles peeking out)."""
    x, y = STEP1[0] - 230, FLOOR + 16
    out = f'<ellipse cx="{x}" cy="{y + 3}" rx="96" ry="13" fill="#6a4128" opacity="0.3" filter="url(#soft)"/>'
    out += (f'<path d="M{x - 66},{y - 70} Q{x - 30},{y - 104} {x + 4},{y - 76} Q{x + 40},{y - 110} {x + 70},{y - 72}" '
            f'stroke="#e9c35c" stroke-width="9" fill="none" stroke-linecap="round"/>')
    out += _bauble_local((x - 24, y - 112), "#3f62a2", 15) + _bauble_local((x + 34, y - 104), "#e9c35c", 14)
    out += (f'<path d="M{x - 80},{y - 74} L{x + 80},{y - 74} L{x + 72},{y} L{x - 72},{y} Z" fill="#c99a62" stroke="{INK}" '
            f'stroke-width="3.6" stroke-linejoin="round"/>')
    out += (f'<path d="M{x - 80},{y - 74} L{x - 104},{y - 98} L{x - 60},{y - 92} Z M{x + 80},{y - 74} L{x + 104},{y - 96} '
            f'L{x + 58},{y - 90} Z" fill="#d8ab72" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    out += f'<path d="M{x - 40},{y - 40} L{x + 40},{y - 40}" stroke="#a87a48" stroke-width="3"/>'
    return doc(S.g(out, filter="wobble-fine"))


# ---- the thought bubble: a birthday cake with candles and balloons
BUB = (560, 372)


def bubble_svg():
    cx, cy = BUB
    out = S.cloud(cx, cy + 40, 470, 170, fill="#fff8ea", seed=17, puffs=6, sw=4)
    for i, (dx, dy, r) in enumerate(BUB_PUFFS):
        out += (f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" fill="#fff8ea" stroke="{INK}" stroke-width="3.6"/>')
    return doc(S.g(out, filter="wobble-fine"))


BUB_PUFFS = [(205, 118, 26), (290, 138, 18), (360, 146, 12)]


def puff_svg(i):
    cx, cy = BUB
    dx, dy, r = BUB_PUFFS[i]
    return doc(S.g(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" fill="#fff8ea" stroke="{INK}" stroke-width="3.6"/>',
                   filter="wobble-fine"))


def cloud_only_svg():
    cx, cy = BUB
    return doc(S.g(S.cloud(cx, cy + 30, 480, 200, fill="#fff8ea", seed=17, puffs=6, sw=4), filter="wobble-fine"))


def cake_svg():
    cx, cy = BUB[0] - 60, BUB[1] + 110
    out = f'<ellipse cx="{cx}" cy="{cy + 6}" rx="118" ry="16" fill="#e6d8c0" stroke="{INK}" stroke-width="3"/>'
    # bottom tier
    out += (f'<path d="M{cx - 96},{cy} L{cx - 96},{cy - 64} Q{cx},{cy - 82} {cx + 96},{cy - 64} L{cx + 96},{cy} '
            f'Q{cx},{cy + 14} {cx - 96},{cy} Z" fill="#f4d9a8" stroke="{INK}" stroke-width="3.4"/>')
    drip = f"M{cx - 96},{cy - 64} Q{cx},{cy - 82} {cx + 96},{cy - 64} L{cx + 96},{cy - 46} "
    for k in range(8):
        x1 = cx + 96 - (k + 1) * 24
        drip += f"Q{x1 + 12},{cy - 22 - 10 * (k % 2)} {x1},{cy - 46} "
    out += f'<path d="{drip} Z" fill="#f2a6b4" stroke="{INK}" stroke-width="3"/>'
    for k in range(5):
        out += f'<circle cx="{cx - 70 + k * 35}" cy="{cy - 26}" r="5" fill="#e9c35c"/>'
    # top tier
    out += (f'<path d="M{cx - 60},{cy - 70} L{cx - 60},{cy - 118} Q{cx},{cy - 132} {cx + 60},{cy - 118} L{cx + 60},{cy - 70} '
            f'Q{cx},{cy - 58} {cx - 60},{cy - 70} Z" fill="#fbe9c8" stroke="{INK}" stroke-width="3.4"/>')
    out += (f'<path d="M{cx - 60},{cy - 118} Q{cx},{cy - 132} {cx + 60},{cy - 118} L{cx + 60},{cy - 104} Q{cx + 45},{cy - 90} '
            f'{cx + 30},{cy - 104} Q{cx + 15},{cy - 88} {cx},{cy - 104} Q{cx - 15},{cy - 90} {cx - 30},{cy - 104} '
            f'Q{cx - 45},{cy - 88} {cx - 60},{cy - 104} Z" fill="#f7c0c8" stroke="{INK}" stroke-width="3"/>')
    for k, col in enumerate(("#7fb8d8", "#f2c94e", "#e98a8a")):
        x = cx - 32 + k * 32
        out += (f'<rect x="{x - 6}" y="{cy - 176}" width="12" height="50" rx="3" fill="{col}" stroke="{INK}" '
                f'stroke-width="2.6"/>')
        out += f'<path d="M{x - 6},{cy - 160} L{x + 6},{cy - 168} M{x - 6},{cy - 144} L{x + 6},{cy - 152}" stroke="#fffaf0" stroke-width="2.4"/>'
    return doc(S.g(out, filter="wobble-fine"))


def flames_svg(k):
    cx, cy = BUB[0] - 60, BUB[1] + 110
    out = ""
    for i in range(3):
        x = cx - 32 + i * 32
        ph = (k + i) % 3
        h = (22, 26, 19)[ph]
        lean = (-2, 2, 0)[ph]
        y = cy - 178
        out += f'<circle cx="{x}" cy="{y - 10}" r="18" fill="#ffe7a0" opacity="0.45"/>'
        out += (f'<path d="M{x},{y} Q{x - 9},{y - h * 0.4} {x + lean},{y - h} Q{x + 9},{y - h * 0.4} {x},{y} Z" fill="#ffb84a" '
                f'stroke="{INK}" stroke-width="2.2"/>')
        out += f'<path d="M{x},{y - 3} Q{x - 4},{y - h * 0.35} {x + lean * 0.5},{y - h * 0.6} Q{x + 4},{y - h * 0.35} {x},{y - 3} Z" fill="#fff2b8"/>'
    return doc(out)


def balloons_svg():
    cx, cy = BUB[0] + 130, BUB[1] - 20
    out = ""
    for dx, dy, col, r in ((-30, 10, "#e9585a", 40), (34, -18, "#f2c94e", 36), (10, 52, "#6fa3d8", 34)):
        x, y = cx + dx, cy + dy
        out += (f'<path d="M{x},{y + r} Q{x - 10},{y + r + 50} {cx - 10},{cy + 140}" stroke="{INK}" stroke-width="2.2" '
                f'fill="none"/>')
        out += (f'<ellipse cx="{x}" cy="{y}" rx="{r * 0.86}" ry="{r}" fill="{col}" stroke="{INK}" stroke-width="3.2"/>'
                f'<path d="M{x - 6},{y + r - 2} L{x + 6},{y + r - 2} L{x},{y + r + 8} Z" fill="{col}" stroke="{INK}" '
                f'stroke-width="2.4" stroke-linejoin="round"/>'
                f'<ellipse cx="{x - r * 0.3}" cy="{y - r * 0.38}" rx="{r * 0.18}" ry="{r * 0.28}" fill="#fffaf0" '
                f'opacity="0.7"/>')
    return doc(S.g(out, filter="wobble-fine"))


# ---- little birthday-candle flames round the tree star
CANDLES = [(-40, -175), (60, -190), (150, -150), (210, -75), (235, 15)]
CANDLE_K = 1.5


def candle_svg(i, k):
    x, y = TOP[0] + CANDLES[i][0], TOP[1] + CANDLES[i][1]
    return doc(f'<g transform="translate({x},{y}) scale({CANDLE_K}) translate({-x},{-y})">{_candle(x, y, i, k)}</g>')


def _candle(x, y, i, k):
    h = (26, 30, 23)[(k + i) % 3]
    lean = (-2, 2, 0)[(k + i) % 3]
    out = (f'<circle cx="{x}" cy="{y - 10}" r="22" fill="#fff0b8" opacity="0.5"/>'
           f'<rect x="{x - 5}" y="{y}" width="10" height="34" rx="3" fill="{("#f7c0c8", "#9fd0ff", "#fbe9a0", "#c8e6b0", "#f7c0c8")[i]}" '
           f'stroke="{INK}" stroke-width="2.4"/>'
           f'<path d="M{x},{y} Q{x - 9},{y - h * 0.4} {x + lean},{y - h} Q{x + 9},{y - h * 0.4} {x},{y} Z" fill="#ffb84a" '
           f'stroke="{INK}" stroke-width="2.2"/>'
           f'<path d="M{x},{y - 3} Q{x - 4},{y - h * 0.35} {x + lean * 0.5},{y - h * 0.6} Q{x + 4},{y - h * 0.35} {x},{y - 3} Z" '
           f'fill="#fff2b8"/>')
    return out


def warm_wash_svg():
    return glow_svg(TOP[0], TOP[1] + 60, 760, 520, "nqwash", "#ffe3a0", "#f6c46a", 0.42, 0.16)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_bday = beat(ctx, 0, "你过生日")
    t_happy = beat(ctx, 0, "开心")
    t_l1end = L[0].end
    t_xmas = beat(ctx, 1, "圣诞节")
    t_give = beat(ctx, 1, "给耶稣")
    t_bd2 = beat(ctx, 1, "过生日")
    t_today = beat(ctx, 1, "今天")
    t_we = beat(ctx, 1, "我们就来")
    t_listen = beat(ctx, 1, "听听")
    t_how = beat(ctx, 1, "耶稣是怎么")
    t_end = L[1].end

    # ---------------- the boy's timeline
    c_hang = snap(t_friend + 0.12)                   # the bauble stays on the branch; he turns to us
    c_up = snap(t_bday + 0.1)                        # smiles up at the bubble
    c_cheer = snap(t_happy - 0.05)                   # big happy face
    c_pick = snap(max(t_l1end + 0.22, c_cheer + 1.2))   # turns back and lifts the star off the stool
    c_hold = snap(c_pick + 0.5)                      # holds it up
    j0 = max(c_hold + 0.4, t_xmas + 0.15)            # hop up onto the top step
    j1 = j0 + 0.36
    c_reach = snap(j1 + 0.3)                         # reaches up with the star
    c_on = snap(c_reach + 0.5)                       # the star is on the tree
    c_us = snap(max(t_today - 0.05, c_on + 1.0))     # turns to us on his stool
    c_look = snap(t_how - 0.1)                       # looks up at the star

    fig = Fig(ctx, "boy", (BOY_X, BOY_Y), z=8, seed=91)
    X, Y = BOY_X, BOY_Y
    fig.at(0, boy(X, Y, "hang", "happy", 1, "bauble"))
    fig.at(c_hang, boy(X, Y, "stand", "nq_us", -1))
    fig.at(c_up, boy(X, Y, "smile_up", "nq_up", -1))
    fig.at(c_cheer, boy(X, Y, "cheer", "laugh", -1))
    fig.at(c_pick, boy(X, Y, "pick", "happy", 1, "star"))
    fig.at(c_hold, boy(X, Y, "hold_star", "joyful", 1, "star"))
    fig.at(c_reach, boy(X, Y, "decorate", "joyful", 1, "star"))
    fig.at(c_on, boy(X, Y, "smile_up", "nq_up", 1))
    fig.at(c_us, boy(X, Y, "stand", "nq_us", -1))
    fig.at(c_look, boy(X, Y, "smile_up", "nq_up", 1))
    hop1 = arc_jump(j0, j1, STOOL_X - BOY_X, STOOL_TOP - BOY_Y, 50)
    cheer_hop = hop(c_cheer, [(0, {"dy": 0}), (0.16, {"dy": -18}), (0.34, {"dy": 0}), (0.46, {"dy": 3}), (0.6, {"dy": 0})],
                    ["out", "in", "sine", "sine"])
    nods = [hop(tn, [(0, {"rot": 0}), (0.16, {"rot": 2.0}), (0.42, {"rot": 0})], ["sine", "sine"])
            for tn in (t_we, t_listen)]
    fig.move(dip(c_hang, 7), dip(c_up, 5), dip(c_pick, 16, 0.9), dip(c_hold, 6), dip(c_reach, 5), dip(c_on, 5),
             dip(c_us, 5), dip(c_look, 5), cheer_hop, hop1, breath(ctx, 0.008, 3.1), *nods)
    fig.add(sc)

    # ---------------- the room, tree, set, presents, stool
    sc.add("room", room_svg(), z=0, wc=0.8)
    sc.add("tree", [tree_svg(k) for k in range(4)] + [tree_svg(0)], z=2, seed=21,
           frame_at=lambda t: (t / 0.45) % 4)
    sc.add("baubles", baubles_svg(), z=2.1, seed=23)
    sc.add("hung", hung_bauble_svg(), z=2.2, seed=25, motion=lambda t: Tf(alpha=1.0 if t >= c_hang else 0.0))
    sc.add("set", set_svg(), z=3, seed=27)
    sc.add("gifts", gifts_svg(), z=3.1, seed=29)
    sc.add("box", box_svg(), z=9, seed=31)
    sc.add("stool", doc(stool_body()), z=7.5, seed=33)
    sc.add("stool_star", stool_star_svg(), z=7.6, seed=35, wc=0.5,
           motion=lambda t: Tf(alpha=1.0 if t < c_pick else 0.0))

    # ---------------- the star on the tree lights up; warm light spreads
    lit = keyed([(c_on, 0.0), (c_on + 0.5, 1.0)], "out")
    sc.add("topper", [topper_svg(0.0)] + [topper_svg(1.0, rot=r) for r in (0, 10, 20)], z=2.5, seed=37, wc=0.3,
           frame_at=lambda t: 0.0 if t < c_on else 1.0 + ((t - c_on) / 1.6) % 2.0,
           motion=lambda t: Tf(alpha=1.0 if t >= c_on else 0.0, sx=1 + 0.03 * math.sin(2 * math.pi * t / 2.2),
                               sy=1 + 0.03 * math.sin(2 * math.pi * t / 2.2), px=TOP[0], py=TOP[1]))
    sc.add("wash", warm_wash_svg(), z=1.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.85 * lit(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.7))))
    sc.add("topglow", glow_svg(TOP[0], TOP[1], 300, 300, "nqtg", "#fff6d0", "#ffd970", 0.9, 0.4), z=2.6, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=lit(t) * (0.7 + 0.3 * math.sin(2 * math.pi * t / 1.9))))

    # ---------------- the thought bubble
    b_in = snap(t_bday - 0.15)
    b_out = snap(max(t_l1end + 0.05, c_cheer + 0.9))
    bx, by = BUB

    def bub_m(delay=0.0, pivot=(bx, by + 60)):
        def m(t):
            t0 = b_in + delay
            if t < t0 or t > b_out + 0.22:
                return Tf(alpha=0.0)
            u = M.progress(t, t0, t0 + 0.45, "back")
            s = 0.3 + 0.7 * u
            a = min(1.0, (t - t0) / 0.12)
            if t > b_out:
                v = min(1.0, (t - b_out) / 0.22)
                s *= 1 - 0.45 * v
                a *= 1 - v * v
            return Tf(sx=s, sy=s, alpha=a, dy=3 * math.sin(2 * math.pi * t / 2.6), px=pivot[0], py=pivot[1])
        return m
    for i in range(3):
        dx, dy, r = BUB_PUFFS[2 - i]
        sc.add(f"puff{i}", puff_svg(2 - i), z=10 + i * 0.01, wc=0.4, motion=bub_m(-0.3 + 0.1 * i, (bx + dx, by + dy)))
    sc.add("cloud", cloud_only_svg(), z=10.1, wc=0.4, motion=bub_m(0.0))
    sc.add("cake", cake_svg(), z=10.2, wc=0.4, motion=bub_m(0.1))
    sc.add("flames", [flames_svg(k) for k in range(3)], z=10.3, wc=0, motion=bub_m(0.1),
           frame_at=lambda t: float(int(t / 0.11) % 3))
    sc.add("balloons", balloons_svg(), z=10.25, wc=0.4,
           motion=M.combine(bub_m(0.2), lambda t: Tf(dy=6 * math.sin(2 * math.pi * t / 1.9), rot=2 * math.sin(2 * math.pi * t / 2.3),
                                                      px=bx + 130, py=by + 160)))

    # ---------------- birthday-candle flames round the tree star
    c_times = [t_give + k * (t_bd2 + 0.25 - t_give) / 4 for k in range(5)]
    c_fade = max(t_today + 0.2, c_times[-1] + 1.0)
    for i, tc in enumerate(c_times):
        cx, cy = TOP[0] + CANDLES[i][0], TOP[1] + CANDLES[i][1]

        def cm(t, tc=tc, cx=cx, cy=cy, i=i):
            if t < tc:
                return Tf(alpha=0.0)
            u = M.progress(t, tc, tc + 0.35, "back")
            a = min(1.0, (t - tc) / 0.1) * (1 - M.progress(t, c_fade, c_fade + 0.5, "sine"))
            return Tf(sx=0.3 + 0.7 * u, sy=0.3 + 0.7 * u, alpha=a, dy=3 * math.sin(2 * math.pi * (t / 1.7 + i * 0.2)),
                      px=cx, py=cy + 30)
        sc.add(f"candle{i}", [candle_svg(i, k) for k in range(3)], z=2.7 + i * 0.01, wc=0, motion=cm,
               frame_at=lambda t, i=i: float(int(t / 0.12 + i) % 3))

    # ---------------- sparkles
    c25 = cal_25()
    sc.fx.append(FX.sparkles((c25[0] - 40, c25[1] - 40, c25[0] + 40, c25[1] + 30), count=4, t0=t_xmas - 0.05,
                             t1=t_xmas + 1.4, size=(10, 18), period=0.9, drift=0, seed=41))
    sc.fx.append(FX.sparkles((TOP[0] - 170, TOP[1] - 160, TOP[0] + 170, TOP[1] + 120), count=9, t0=c_on, size=(8, 16),
                             period=1.6, drift=-6, seed=43))
    sc.fx.append(FX.sparkles((BOY_X - 170, BOY_Y - 470, BOY_X + 110, BOY_Y - 300), count=6, t0=c_cheer, t1=c_pick,
                             size=(9, 16), period=1.0, drift=-20, seed=45))
    sc.fx.append(FX.motes((600, 200, 1900, 900), count=16, t0=c_on, color=(255, 240, 200), seed=47, alpha=90))

    # ---------------- camera
    c0 = Cam(1000, 652, 1790)
    c1 = Cam(960, 640, 1740)
    c2 = Cam(1060, 628, 1700)
    c3 = Cam(TOP[0] - 40, 548, 1000)
    sc.camera = M.cam_keys([(0, c0), (0.9, c0), (t_bday + 0.6, c1), (c_pick, c1), (c_reach, c2), (t_how - 0.3, c2),
                            (min(T - 0.9, t_end + 0.3), c3), (T, Cam(c3.x, c3.y - 4, c3.w - 20))], "sine")

    # ---------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-30, fade_in=1.0, fade_out=1.0)
    sc.sfx("pop", c_hang - 0.02, gain_db=-16, pan=0.0)
    for i in range(3):
        sc.sfx("pop", b_in - 0.3 + 0.1 * i, gain_db=-22 - 2 * i, pan=-0.3)
    sc.sfx("pop", b_in + 0.02, gain_db=-14, pan=-0.4)
    sc.sfx("sparkle", c_cheer + 0.05, gain_db=-16, pan=-0.2)
    sc.sfx("pop", b_out, gain_db=-20, pan=-0.4)
    sc.sfx("cloth", c_pick, gain_db=-18)
    sc.sfx("sparkle", t_xmas, gain_db=-20, pan=0.6)
    sc.sfx("thud", j1, gain_db=-20)
    sc.sfx("chime", c_on, gain_db=-11)
    sc.sfx("sparkle", c_on + 0.1, gain_db=-15)
    sc.sfx("sparkle", t_give + 0.1, gain_db=-17)
    sc.sfx("sparkle", t_how + 0.3, gain_db=-20)
    return sc
