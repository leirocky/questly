"""Scene 6 - Mark 6:39-40, John 6:10, Matthew 14:21. Jesus has everyone sit down on the green grass; the crowd settles
in colourful groups, row after row and group after group (a hundred here, fifty there); seen from high above the
groups look like little garden beds; a picture-book count: five thousand men, and many mothers and children; the
whole hillside full.

One stage (2560 x 1440) holds two pictures: the emerald hillside above the lake in golden light (time .6; galilee_sky +
lake_hillside + teaching_rock, the seated groups on their own layers) - also the first picture of s07_bless, which
starts with a plain 1 s fade from this scene's last second (s07 builds its world and cast with the helpers below) -
and, for the high view, props.hillside_high + characters.garden_beds drawn on a box 1/1.5 of the stage and scaled up
(bigger heads), gated to its shot. Jesus holds the boy's open basket the whole time (custom arm poses on the library
rig: at the chest, at the far hip, on his lap); the one-handed sit-down gesture is sit_down_gesture's near arm + phase.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's
beat(); nothing is hard-coded to the take). Times are for the current take:
  0 .. 0.9      calm medium shot (after s05's page turn): Jesus by the teaching rock holds the boy's open basket at his
                chest and smiles down at the boy on his left; Peter, John, Andrew, Philip and James stand by with their
                empty baskets; the crowd stands on the slope; a slow camera drift
  '耶稣' 0.94   Jesus turns to the disciples; '门徒' 1.56 the basket goes to his far hip (the near hand is free)
  '叫' 3.22     '叫大家都坐下来吧': the near hand goes forward, palm down, and pats down on '坐' 4.08 and '来' 4.52
  4.98 ..       the disciples go out to the people: Andrew, Philip and James walk off among the families (planted-foot
                strides, footsteps), Peter and John turn and call / point to the groups nearby
  '那里' 5.87   '那里有好多青草': the camera pulls back over the green grass; a breeze runs over the slope (soft light
                bands sweep across, the flowers sway faster, wind)
  '一排' 8.13 / 8.52   the far rows sit down row after row (squash dips hide the stand -> sit cuts; cloth rustles)
  '一组' 9.04 .. '坐下' 10.29   the nearer groups sit one after another
  '一百' 11.70  the big front group sits with a pop and a '100' tag (sparkle burst)
  '五十' 13.64  the smaller group beside it sits with a '50' tag; then the boy (14.2) and Jesus (14.6, the basket on his
                lap) sit down by the rock
  '从' 15.52    hard cut on the phrase start to the high view (the camera was already rising): Jesus and the boy on the
                rock in a soft warm glow, the camera rises and pulls back over the beds; '一块一块的小花园' 18.9-20.6 the
                beds pop one after another like flowers opening (chime); cloud shadows drift, swallows cross
  '光是男人' 21.48  a picture-book counter (a little man in a cream roundel + a big gold number) rolls up from 0 and lands
                on 5000 on '五千' 23.14 with a sparkle burst (grow, sparkle, chime)
  '还有' 24.04  hard cut back to the hillside, close on the families at the front: on '妈妈' 24.77 the mothers rock their
                babies (little hearts float up), on '小朋友' 25.39 three children pop up, wave and hop, then sit again
  '整个山坡' 26.55  the camera pulls back to the whole hillside, every group seated, Jesus on his rock with the basket on
                his lap, the boy beside him, Peter and John with their empty baskets; settles 28.7, calm hold (2.6 s) to
                the end = s07_bless's first second (pixel-identical: END_* keys, shared layers, film-clock motion and crop
                markers)

Shared with s07_bless: the world (add_world), the groups (add_groups), the featured front-row people (FEATURED, incl.
the three who take the bread in s07: RECEIVERS), Actor, jesus_svg, the END_* keys and CAM_END.
"""
import math
import random

from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import Twinkle, beat
from stories.noah.scenes.s01_title import f1, heart_markup, snap

INK = "#4b3426"
W, H = 2560, 1440
TOD = 0.6                                     # golden light
HX0, HX1, HY, HS, HSEED = -60, W + 60, 1300, 1.3, 3
PK = 0.71                                     # people scale = PK x the hillside's own perspective scale
PTS = PR.lake_hillside_points(HX0, HX1, HY, HS, seed=HSEED)
LAKE_Y, FAR_Y = PTS["lake_y"], PTS["far_y"]
SUN = (1880, 352)
G_REF = 160.0                                 # film-time reference for drifting clouds / birds (s06 and s07 share them)


def doc(body, defs=""):
    return S.svg_doc(body, defs, W, H)


def d_of_y(y):
    return max(0.0, min(1.0, ((HY - y) / (HY - LAKE_Y)) ** (1 / 0.85)))


def k_of_y(y):
    """Figure scale at ground height y (the hillside's perspective)."""
    return PK * HS * (1.0 - 0.62 * d_of_y(y))


def ground_y(d, x):
    y, _ = PTS["depth"](d)
    return y - PTS["shoulder"]((x - HX0) / (HX1 - HX0)) * d ** 1.4


def zy(y, dz=0.0):
    """z for something standing / sitting on the ground at y (nearer = in front)."""
    return 10 + y * 0.01 + dz


def clamp_cam(c):
    w = min(c.w, W)
    h = w * 9 / 16
    return Cam(min(max(c.x, w / 2), W - w / 2), min(max(c.y, h / 2), H - h / 2), w, c.rot)


def cam_path(keys, curves):
    for tk, c in keys:
        cc = clamp_cam(c)
        assert abs(cc.x - c.x) < 0.5 and abs(cc.y - c.y) < 0.5 and abs(cc.w - c.w) < 0.5, f"camera key {tk:.2f} leaves the stage: {c}"
    f = M.cam_keys(keys, curves)
    return lambda t: clamp_cam(f(t))


# ---------------------------------------------------------------- blink expressions (closed-eye twins)
for _e in ("warm", "smile", "happy", "call_warm", "kind", "awed", "thanks", "neutral", "hopeful", "delighted", "amazed"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"lf6b_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"lf6b_{expr}"


# ---------------------------------------------------------------- the cast (positions shared with s07)
ROCK = (560, 1158)                            # the teaching rock's anchor = Jesus's seated anchor (floor under his feet)
JS = k_of_y(1160)
JSTAND = (572, 1162)                          # Jesus standing in front of the rock
BOY_STAND = (440, 1182)                       # the boy stands / sits on Jesus's left, facing him
BOY_SIT = (418, 1192)
BS = k_of_y(1172)
PETER = (968, 1166)
JOHN = (1088, 1180)
DISC = {"peter": (0, PETER), "john": (3, JOHN)}
WALKERS = [  # variant, start, end
    (1, (1196, 1150), (1468, 1150)),           # Andrew
    (4, (1300, 1172), (1712, 1172)),           # Philip
    (2, (1400, 1146), (2206, 1146)),           # James
]
DISC_ADV = 87                                 # Storm disciples' walk: the planted ankle moves 87 px per cut (scale 1)
BASKET_K = C.DISCIPLE_BASKET_K                # the disciples' big baskets (carry size)


def basket_spot(x, y, s, f):
    """Where a disciple's empty basket stands on the grass beside him (facing f: just toward f, a little behind)."""
    return x + f * 64 * s, y - 6 * s


def ground_basket_svg(x, y, s, f, seed=11):
    bx, by = basket_spot(x, y, s, f)
    return PR.wicker_basket(bx, by, BASKET_K * s, f, fill=0.0, time=TOD, seed=seed) + C.ground_shadow(bx, by, s * 0.6, 150, 0.18)


# ---------------------------------------------------------------- Jesus with the boy's basket (custom arm poses)
def _jesus_custom(x, y, s, f, ps, expr, item_pose=None, phase=0.0, item=None, extra=None, glow=0.0, pre=None):
    D = C._jesus_design("stand", glow, True, 0.0, True)
    fronts = [D["front"], pre]
    if item_pose:
        fronts.append(C._jesus_lf_items(item_pose, phase, item, True))
    if extra:
        fronts.append(extra)
    D["front"] = C._hooks(*[h for h in fronts if h])
    inner, _ = C._figure(D, C._JESUS_M, ps, expr or ps["expr"], C._fsign(f), True)
    return C._wrap_out(inner, x, y, s, f, "jesus-lf6")


LAP_PS = dict(t=-2, arms=(("ik", "abs", 64, -112, 1), ("ik", "abs", 36, -106, 1)), hands=("open", "open"))


def _lap_centre():
    """Where the basket sits in the 'lap' drawing (the look_up_bless item hook's placement), so the breaking and giving
    drawings keep it on his lap."""
    got = {}
    ps = C._P(expr="warm", look=(0.03, 0.0), **LAP_PS, **C._SEAT)
    D = C._jesus_design("stand", 0.0, True, 0.0, True)

    def cap(st):
        got["w"] = (st["arms"][0][2], st["arms"][1][2])
        return ""
    D["front"] = C._hooks(D["front"], cap)
    C._figure(D, C._JESUS_M, ps, "warm", 1, True)
    (a, b), (c, d) = got["w"]
    return ((a + c) / 2, (b + d) / 2 - 2)


LAP_C = _lap_centre()


def _lap_basket(st):
    return C._lf_held(st, PR._boy_basket("open", handle=False), LAP_C, -4, 0.78)


def _basket_at_far_hand(st):
    W0, hr = st["arms"][0][2], st["m"]["hr"]
    k = 0.78
    b = C._lf_held(st, PR._boy_basket("open", time=TOD, handle=True), (W0[0] - 4, W0[1] + 40 * k + 6), 0, k)
    return b + C._fist(W0, hr, C.JESUS_SKIN, 0, 2)


SEAT = C._SEAT


def jesus_svg(key, x=None, y=None, s=JS, f=1):
    """Jesus drawings by key: ('hold', expr, look) basket at the chest | ('ready', expr, look) basket at the far hip |
    ('gesture', phase) the near hand palm down | ('lap', expr, look) seated on the rock, the basket on his lap |
    ('lift', expr, look) seated, lifting the basket to the chest | ('bless', expr) seated, basket raised to heaven |
    ('break', phase, item) seated breaking a loaf / fish | ('give', item, expr) seated, handing it forward."""
    kind = key[0]
    if kind in ("hold", "ready", "gesture"):
        x = JSTAND[0] if x is None else x
        y = JSTAND[1] if y is None else y
    else:
        x = ROCK[0] if x is None else x
        y = ROCK[1] if y is None else y
    if kind == "hold":
        expr, look = key[1], key[2]
        f = key[3] if len(key) > 3 else f
        ps = C._P(t=2, h=10 if look[1] > 0.02 else 2, legs=((6, 2), (-5, -2)),
                  arms=(("ik", "abs", 82, -196, 1), ("ik", "abs", 50, -190, 1)), hands=("open", "open"), expr=expr, look=look)
        return _jesus_custom(x, y, s, f, ps, expr, "look_up_bless")
    if kind == "ready":
        _, expr, look = key
        ps = C._P(t=2, h=4, legs=((8, 3), (-7, -3)), arms=(("ik", "abs", 40, -150, 1), ("fk", -6, -2)),
                  hands=("fist", "open"), expr=expr, look=look)
        return _jesus_custom(x, y, s, f, ps, expr, extra=_basket_at_far_hand)
    if kind == "gesture":
        ph = key[1]
        lo = 14 * math.sin(math.pi * ph)
        expr = key[2] if len(key) > 2 else "call_warm"
        ps = C._P(t=4, h=4, legs=((8, 3), (-7, -3)), arms=(("ik", "abs", 40, -150, 1), ("fk", 42 - lo, 64 - lo)),
                  hands=("fist", "open"), expr=expr, look=(0.03, 0.02))
        return _jesus_custom(x, y, s, f, ps, expr, extra=_basket_at_far_hand)
    if kind == "lap":
        _, expr, look = key
        ps = C._P(h=4 if look[1] > 0.02 else 0, expr=expr, look=look, **LAP_PS, **SEAT)
        return _jesus_custom(x, y, s, f, ps, expr, "look_up_bless")
    if kind == "lift":
        _, expr, look = key
        ps = C._P(t=-3, h=2, arms=(("ik", "abs", 84, -160, 1), ("ik", "abs", 52, -154, 1)), hands=("open", "open"), expr=expr,
                  look=look, **SEAT)
        return _jesus_custom(x, y, s, f, ps, expr, "look_up_bless")
    if kind == "bless":
        expr = key[1]
        glow = key[2] if len(key) > 2 else 0.0
        ps = dict(C._jesus_lf_pose("look_up_bless", 0))
        ps.update(SEAT)
        ps["arms"] = (("ik", "abs", 100, -232, 1), ("ik", "abs", 66, -226, 1))
        return _jesus_custom(x, y, s, f, ps, expr, "look_up_bless", glow=glow)
    if kind == "break":
        _, ph, item = key[:3]
        expr = key[3] if len(key) > 3 else "smile"
        ps = dict(C._jesus_lf_pose("break_bread", ph))
        ps.update(SEAT)
        ps["arms"] = tuple((a[0], a[1], a[2], a[3] + 56, a[4]) for a in ps["arms"])
        return _jesus_custom(x, y, s, f, ps, expr, "break_bread", phase=ph, item=item, pre=_lap_basket)
    if kind == "give":
        _, item, expr = key
        ps = dict(C._jesus_lf_pose("give_bread", 0))
        ps.update(SEAT)
        ps["arms"] = tuple((a[0], a[1], a[2], a[3] + 56, a[4]) for a in ps["arms"])
        return _jesus_custom(x, y, s, f, ps, expr, "give_bread", item=item, pre=_lap_basket)
    raise ValueError(key)


def disc_svg(v, x, y, s, key):
    """('stand' | 'talk' | 'point' | 'walk_a' | 'walk_b' | ..., facing, expr)."""
    pose, f, expr = key
    return C.disciples(x, y, s, f, variant=v, pose=pose, expr=expr)


# ---------------------------------------------------------------- the seated groups
KINDS = ("man", "woman", "child", "mother", "man", "child", "elder", "woman", "child", "man", "mother", "woman")
FOCUS = ROCK[0]


def make_group(gx, d, n, cols, fam, seed, kinds=KINDS):
    gy = ground_y(d, gx)
    sk = k_of_y(gy)
    rng = random.Random(seed)
    prow = -(-n // cols)
    out = []
    for i in range(n):
        rr, cc = divmod(i, cols)
        px = gx + (cc - (cols - 1) / 2) * 68 * sk + (rr % 2) * 26 * sk + rng.uniform(-9, 9) * sk
        py = gy + (rr - (prow - 1) / 2) * 31 * sk + rng.uniform(-4, 4) * sk
        kind = kinds[(i * 5 + seed) % len(kinds)]
        v = fam + 6 * ((i + seed) % 3)
        out.append(dict(i=i, x=px, y=py, k=k_of_y(py), kind=kind, v=v, f=1 if px < FOCUS else -1, row=rr))
    out.sort(key=lambda p: p["y"])
    return dict(x=gx, y=gy, k=sk, n=n, people=out, fam=fam, d=d)


SIT_MIX = ("sit_listen", "sit", "sit_listen", "sit_listen", "sit")
STAND_MIX = ("stand_listen", "stand", "stand_listen", "stand", "stand_listen", "wave")


def person_pose(p, mode):
    i, kind = p["i"], p["kind"]
    if mode == "sit":
        return SIT_MIX[i % 5]
    if mode == "stand":
        pose = STAND_MIX[(i * 3 + p["v"]) % 6]
        if kind in ("mother", "elder") and pose == "wave":
            pose = "stand"
        return pose
    if mode == "eat":
        pose = ("sit_eat", "sit_eat", "sit_laugh", "sit_eat", "sit_receive", "sit_eat")[(i + p["v"]) % 6]
        if kind == "elder" and pose == "sit_receive":
            pose = "sit_eat"
        return pose
    return mode


def person_svg(p, mode, pose=None, expr=None, phase=0.0, food=None):
    k = p["k"]
    kind = p["kind"]
    if mode in ("sit", "eat") and pose is None and k < 0.33:
        c = C._gl_colours(p["v"])
        mk = kind if kind in ("man", "woman", "child") else ("woman" if kind == "mother" else "man")
        mp = "eat" if mode == "eat" and p["i"] % 3 != 2 else "sit"
        body = C._mini_sitter(c, k, p["f"], mp, mk, p["i"])
        return f'<g transform="translate({p["x"]:.1f},{p["y"]:.1f}) scale({k:.4f})" filter="url(#wobble-fine)">{body}</g>'
    pose = pose or person_pose(p, mode)
    if kind == "mother" and pose in ("sit_eat", "sit_receive", "sit_laugh"):
        kind = "woman"
    if kind == "elder" and pose == "wave":
        pose = "stand"
    return C.galilee_folk(p["x"], p["y"], k, p["f"], kind=kind, variant=p["v"], pose=pose, expr=expr, phase=phase, food=food)


def group_svg(g, mode, skip=()):
    return "".join(person_svg(p, mode) for p in g["people"] if p["i"] not in skip)


TREES = [(HX0 + (HX1 - HX0) * u, d) for u, d in ((0.04, 0.75), (0.12, 0.58), (0.90, 0.70), (0.97, 0.40), (0.56, 0.92))]


def path_x(y):
    pts = PTS["path"]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if yb <= y <= ya:
            u = (ya - y) / max(1e-6, ya - yb)
            return xa + (xb - xa) * u
    return pts[-1][0]


ROWS = [  # depth, x list (None = every `spacing` px from x0), spacing, x0, n big / small, cols big / small
    (0.97, None, 250, 70, 14, 9, 6, 5),
    (0.84, None, 280, 160, 14, 9, 5, 4),
    (0.68, None, 330, 120, 14, 9, 5, 4),
    (0.53, [930, 1270, 1890, 2270], 0, 0, 14, 8, 5, 4),
    (0.38, [1060, 1400, 2010, 2420], 0, 0, 14, 9, 5, 4),
    (0.10, [1960, 2420], 0, 0, 18, 10, 6, 4),
]


def _all_groups():
    gs = []
    gi = 0
    for r, (d, xs, sp, x0, nb, ns, cb, cs) in enumerate(ROWS):
        y0, _ = PTS["depth"](d)
        sk = k_of_y(y0)
        if xs is None:
            xs = list(range(x0, W + 40, sp))
        for j, x in enumerate(xs):
            big = (j + r) % 2 == 0 if d > 0.2 else j == 0
            cols = cb if big else cs
            half = cols * 34 * sk + 30
            pw = (10 + 50 * (1 - d)) * HS + 40
            ok = abs(x - path_x(y0)) > half + pw
            for tx, td in TREES:
                ty, tk = PTS["depth"](td)
                if abs(td - d) < 0.12 and abs(x - tx) < half + 120 * tk * HS:
                    ok = False
            if d < 0.62 and 260 < x < 860:
                ok = False
            if d > 0.9 and x > 2440:
                ok = False
            if ok:
                kinds = KINDS
                if r >= 4:     # the families at the front: more mothers and children
                    kinds = ("man", "mother", "child", "woman", "child", "elder", "mother", "child", "man", "woman", "child", "mother")
                gs.append(dict(make_group(x, d, nb if big else ns, cols, (gi * 5 + 1) % 6, 11 + gi * 7, kinds), row=r, big=big, gi=gi))
                gi += 1
    return gs


GROUPS = _all_groups()
FRONT = [g for g in GROUPS if g["row"] == 5]
G100 = FRONT[0]                                # the big front group (on '一百')
G50 = FRONT[1]                                 # the smaller one (on '五十')


def _front_row(g):
    mx = max(p["row"] for p in g["people"])
    return sorted([p for p in g["people"] if p["row"] == mx], key=lambda p: p["x"])


def _edge(g, side, kind):
    """The front-row person at the group's left (side -1) or right (+1) edge, made a `kind` (the one who takes the bread)."""
    row = _front_row(g)
    p = row[0] if side < 0 else row[-1]
    p["kind"] = kind
    return p


R4A = min((g for g in GROUPS if g["row"] == 4), key=lambda g: abs(g["x"] - 2010))
# s07: the people who take the bread from the disciples, the disciple who serves each one and the side he stands on
RECEIVERS = [("philip", G100, _edge(G100, -1, "child"), 1), ("peter", G100, _edge(G100, 1, "woman"), -1),
             ("andrew", R4A, _edge(R4A, -1, "man"), 1)]


def _featured():
    """Front-row people drawn on their own layers in s06 AND s07 (so the group drawings match at the fade): the mothers
    who rock their babies and the children who pop up and wave (s06), the people who take the bread (s07).
    [(group, person, role)]."""
    out = [(g, p, "recv") for _, g, p, _ in RECEIVERS]
    taken = {id(p) for _, _, p, _ in RECEIVERS}
    for g, roles in ((G100, {"mother": 2, "child": 2}), (G50, {"mother": 1, "child": 1})):
        front = sorted(g["people"], key=lambda p: -p["y"])[: max(4, int(g["n"] * 0.7))]
        for kind, n in roles.items():
            cand = sorted([p for p in front if p["kind"] == kind and id(p) not in taken], key=lambda p: p["x"])
            if len(cand) > n:
                step = len(cand) / n
                cand = [cand[int(i * step)] for i in range(n)]
            out += [(g, p, kind) for p in cand[:n]]
    return out


FEATURED = _featured()
FEAT_IDS = {id(g): {p["i"] for gg, p, _ in FEATURED if gg is g} for g in GROUPS}


# ---------------------------------------------------------------- small drawings
def flowers_svg(x0, x1, y0, y1, density, seed, s, sway):
    return f'<g filter="url(#wobble-fine)">{PR._lf_flowers(x0, x1, y0, y1, density, seed, TOD, s, sway=sway)}</g>'


def swallow_svg(x, y, s, wing):
    """A swallow gliding / flapping (wing 0 up .. 1 down), facing +x."""
    a = -16 + 26 * wing
    body = (f'<path d="M{f1(x - 20 * s)},{f1(y + 2 * s)} Q{f1(x)},{f1(y - 5 * s)} {f1(x + 16 * s)},{f1(y)} '
            f'Q{f1(x)},{f1(y + 5 * s)} {f1(x - 20 * s)},{f1(y + 2 * s)} Z" fill="#3c3a52" stroke="{INK}" stroke-width="{f1(1.6 * s)}"/>')
    tail = f'<path d="M{f1(x - 18 * s)},{f1(y + 2 * s)} l{f1(-12 * s)},{f1(-6 * s)} M{f1(x - 18 * s)},{f1(y + 2 * s)} l{f1(-12 * s)},{f1(5 * s)}" stroke="#3c3a52" stroke-width="{f1(2.4 * s)}" stroke-linecap="round"/>'
    wing_ = (f'<path d="M{f1(x - 2 * s)},{f1(y)} Q{f1(x - 14 * s)},{f1(y + a * s * 0.6)} {f1(x - 26 * s)},{f1(y + a * s)} '
             f'Q{f1(x - 8 * s)},{f1(y + a * s * 0.3)} {f1(x + 6 * s)},{f1(y)} Z" fill="#4a4866" stroke="{INK}" stroke-width="{f1(1.4 * s)}"/>')
    return tail + body + wing_


def tag_svg(x, y, label, s=1.0):
    """A picture-book number tag ('100' / '50') on a little cream flag."""
    w = (52 + 34 * len(label)) * s
    h = 84 * s
    defs = S.lin_grad(f"lf6tg{label}", [(0, "#f7c95a"), (0.6, "#e0913a"), (1, "#c86e2c")])
    b = (f'<rect x="{f1(x - w / 2 + 6 * s)}" y="{f1(y - h + 8 * s)}" width="{f1(w)}" height="{f1(h)}" rx="{f1(26 * s)}" '
         f'fill="{INK}" opacity="0.22"/>')
    b += (f'<rect x="{f1(x - w / 2)}" y="{f1(y - h)}" width="{f1(w)}" height="{f1(h)}" rx="{f1(26 * s)}" fill="#fff6e3" '
          f'stroke="{INK}" stroke-width="{f1(4 * s)}"/>')
    b += f'<path d="M{f1(x - 14 * s)},{f1(y - 2 * s)} L{f1(x)},{f1(y + 22 * s)} L{f1(x + 14 * s)},{f1(y - 2 * s)} Z" fill="#fff6e3" stroke="{INK}" stroke-width="{f1(4 * s)}" stroke-linejoin="round"/>'
    b += f'<rect x="{f1(x - 16 * s)}" y="{f1(y - 8 * s)}" width="{f1(32 * s)}" height="{f1(9 * s)}" fill="#fff6e3"/>'
    b += (f'<text x="{f1(x)}" y="{f1(y - 22 * s)}" font-family="LXGW WenKai" font-weight="bold" font-size="{f1(62 * s)}" '
          f'text-anchor="middle" fill="url(#lf6tg{label})" stroke="{INK}" stroke-width="{f1(2.6 * s)}" '
          f'stroke-linejoin="round">{label}</text>')
    return doc(S.g(b, filter="wobble-fine"), defs)


def pop_hold(t0, piv, hold=1.3, out=0.35, rise=10.0):
    def m(t):
        if t < t0 - 0.01 or t > t0 + hold + out:
            return Tf(alpha=0.0)
        s = 0.25 + 0.75 * M.progress(t, t0, t0 + 0.3, "back")
        a = M.progress(t, t0, t0 + 0.1, "sine") * (1 - M.progress(t, t0 + hold, t0 + hold + out, "sine"))
        return Tf(sx=s, sy=s, px=piv[0], py=piv[1], alpha=a, dy=-rise * M.progress(t, t0, t0 + hold + out, "out"))
    return m


def dipm(t0, s, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there); scales about the layer's pivot."""
    def m(t):
        u = t - t0
        if u < -0.14 or u > 0.3:
            return Tf()
        if u < 0:
            k = M.ease("in")((u + 0.14) / 0.14)
            return Tf(dy=depth * s * k, sy=1 - 0.05 * k)
        if u < 0.13:
            k = M.ease("out")(u / 0.13)
            return Tf(dy=depth * s * (1 - k) - 3 * s * k, sy=0.95 + 0.065 * k)
        k = M.ease("sine")((u - 0.13) / 0.17)
        return Tf(dy=-3 * s * (1 - k), sy=1.015 - 0.015 * k)
    return m


def hopm(t0, s, height=26.0, dur=0.4):
    def m(t):
        u = t - t0
        if u < -0.1 or u > dur + 0.16:
            return Tf()
        if u < 0:
            k = (u + 0.1) / 0.1
            return Tf(dy=4 * s * k, sy=1 - 0.05 * k)
        if u < dur:
            v = u / dur
            return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.04 * math.sin(math.pi * v))
        k = 1 - (u - dur) / 0.16
        return Tf(dy=3 * s * math.sin(math.pi * k), sy=1 - 0.035 * math.sin(math.pi * k))
    return m


def breath_g(g0, period=3.0, amount=0.008, phase=0.0):
    return lambda t: Tf(sy=1 + amount * math.sin(2 * math.pi * ((g0 + t) / period + phase)),
                        sx=1 - 0.3 * amount * math.sin(2 * math.pi * ((g0 + t) / period + phase)))


def gate(t0, t1):
    """Visible only outside [t0, t1) (hard cut)."""
    return lambda t: Tf(alpha=0.0 if t0 <= t < t1 else 1.0)


def only(t0, t1):
    return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)


def markers(box):
    """Four faint 3 px dots at a box's corners: every frame of a layer shared by s06 and s07 gets the same crop box, so
    the compositor's crop / downscale is identical in both scenes and the 1 s fade matches pixel for pixel."""
    x0, y0 = max(0, round(box[0])), max(0, round(box[1]))
    x1, y1 = min(W, round(box[2])), min(H, round(box[3]))
    return "".join(f'<rect x="{x}" y="{y}" width="3" height="3" fill="{INK}" opacity="0.04"/>' for x in (x0, x1 - 3) for y in (y0, y1 - 3))


# ---------------------------------------------------------------- one figure on its own flipbook layer
class Loop:
    def __init__(self, keys, per, phase=0.0):
        self.keys, self.per, self.phase = tuple(keys), per, phase


class Actor:
    """A figure on its own flipbook layer: drawings by key (draw(key) -> markup at the home anchor), hard cuts (cut),
    film-clock loops (loop), planted-foot walks (walk: the layer moves), squash dips hiding cuts, extra motions, an
    optional visibility gate. Scaling pivots about the home anchor (the feet)."""

    def __init__(self, name, home, s, draw, z, seed, g0, wc=1.0):
        self.name, (self.hx, self.hy), self.s, self.draw = name, home, s, draw
        self.z, self.seed, self.g0, self.wc = z, seed, g0, wc
        self.ents, self.moves, self.extra, self.dips, self.gates = [], [], [], [], []
        hx, hy = home
        self.box = (hx - 300 * s, hy - 470 * s, hx + 300 * s, hy + 90 * s)

    def cut(self, t, key, dip=None):
        t = snap(t) if t > 0 else -1.0
        self.ents.append((t, key))
        if dip and t > 0:
            self.dips.append((t, dip))
        return self

    def loop(self, t, keys, per, phase=0.0, dip=None):
        return self.cut(t, Loop(keys, per, phase), dip)

    def key_at(self, t):
        cur = None
        for tk, k in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = k
        if isinstance(cur, Loop):
            cur = cur.keys[int((t + self.g0) / cur.per + cur.phase) % len(cur.keys)]
        return cur

    def off(self, t):
        x = y = 0.0
        for mv in self.moves:
            a, b = mv(t)
            x += a
            y += b
        return x, y

    def walk(self, t0, keys, n, per, adv, facing, last_adv=None, move=0.12):
        """n planted-foot strides from t0, one cut every per s (keys alternate), the anchor advancing adv px per cut
        (last_adv for the final settling cut). Returns the time of the last cut."""
        cts = [snap(t0 + per * i) for i in range(n)]
        ads = []
        for i, tc in enumerate(cts):
            self.ents.append((tc, keys[i % len(keys)]))
            a = last_adv if (i == n - 1 and last_adv is not None) else adv
            ads.append(a * facing)

        def mv(t, cts=cts, ads=ads):
            x = 0.0
            for tc, a in zip(cts, ads):
                x += a * M.progress(t, tc - move * 0.4, tc + move * 0.6, "sine")
            return x, 0.0
        self.moves.append(mv)
        return cts[-1]

    def blinks(self, times, pairs):
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        for tb in times:
            tb = snap(tb)
            if any(abs(tb - tk) < 0.3 for tk in cut_ts):
                continue
            cur = None
            for tk, k in sorted(self.ents, key=lambda e: e[0]):
                if tk <= tb:
                    cur = k
            if not isinstance(cur, Loop) and cur in pairs:
                self.ents += [(tb, pairs[cur]), (snap(tb + 0.13), cur)]
        return self

    def build(self, sc):
        ents = sorted(self.ents, key=lambda e: e[0])
        keys = []
        for _, k in ents:
            for kk in (k.keys if isinstance(k, Loop) else (k,)):
                if kk not in keys:
                    keys.append(kk)
        mk = markers(self.box) if self.box else ""
        frames = [doc(self.draw(k) + mk) for k in keys]
        idx = {k: i for i, k in enumerate(keys)}
        g0 = self.g0

        def fa(t):
            cur = ents[0][1]
            for tk, k in ents:
                if t >= tk:
                    cur = k
                else:
                    break
            if isinstance(cur, Loop):
                cur = cur.keys[int((t + g0) / cur.per + cur.phase) % len(cur.keys)]
            return float(idx[cur])
        hx, hy = self.hx, self.hy

        def base(t):
            x, y = self.off(t)
            return Tf(dx=x, dy=y, px=hx, py=hy)
        mots = [base] + [dipm(td, self.s, d) for td, d in self.dips] + self.extra + self.gates
        sc.add(self.name, frames if len(frames) > 1 else frames[0], z=self.z, seed=self.seed, wc=self.wc,
               frame_at=fa if len(frames) > 1 else None, motion=M.combine(*mots))
        return self


def blink_times(t0, t1, rng, avg=3.2):
    out = []
    t = t0 + rng.uniform(0.4, avg)
    while t < t1:
        out.append(t)
        t += rng.uniform(avg * 0.7, avg * 1.4)
    return out


# ---------------------------------------------------------------- the hillside world (shared with s07)
def backdrop_svg():
    sky = PR.galilee_sky(-40, -40, W + 40, LAKE_Y, time=TOD, sun=SUN, clouds=0.0, seed=5, scale=HS)
    back = PR.lake_hillside(HX0, HX1, HY, HS, time=TOD, part="back", seed=HSEED, bottom=H + 80)
    mid = PR.lake_hillside(HX0, HX1, HY, HS, time=TOD, part="mid", seed=HSEED, bottom=H + 80, rock=False)
    return doc(sky + back + mid)


CLOUDS = [(380, 150, 520, 6, 9.0), (1180, 205, 400, 11, 7.0), (2010, 120, 560, 17, 10.5), (2480, 230, 360, 23, 8.0)]
BIRDS = [(-200, 250, 1.0, 64.0, 0.0), (300, 190, 0.8, 52.0, 0.4), (-700, 300, 0.9, 58.0, 0.7)]


def gust_band_svg(cx, cy, rx, ry):
    defs = S.rad_grad("lf6gust", [(0, "#eaffb0", 0.42), (0.55, "#d8f290", 0.18), (1, "#d8f290", 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#lf6gust)"/>', defs)


def add_world(sc, g0, vis=None, gust=None):
    """The hillside picture: backdrop, drifting clouds, swallows, the teaching rock, the front grass and swaying
    flowers, glints on the lake. vis(t) -> alpha multiplier (None = always)."""
    vm = [vis] if vis else []
    sc.add("backdrop", backdrop_svg(), z=1, seed=101, motion=M.combine(*vm) if vm else None)
    pal = PR._lf_pal(TOD)
    for i, (cx, cy, w, sd, v) in enumerate(CLOUDS):
        body = PR._lf_cloud(cx, cy, w, w * 0.3, pal, seed=sd, rim_k=0.75)
        sc.add(f"cloud{i}", doc(body), z=2 + i * 0.01, seed=131 + i,
               motion=M.combine(lambda t, v=v: Tf(dx=v * (g0 + t - G_REF)), *vm))
    for i, (x0, y0, s, v, ph) in enumerate(BIRDS):
        frames = [doc(swallow_svg(x0, y0, s * 1.3, w)) for w in (0.0, 0.5, 1.0, 0.5)]

        def bm(t, x0=x0, y0=y0, v=v, ph=ph):
            u = g0 + t - G_REF
            span = W + 1400
            dx = (v * u + ph * span) % span
            return Tf(dx=dx, dy=26 * math.sin(u * 0.7 + ph * 6))
        sc.add(f"bird{i}", frames, z=3 + i * 0.01, seed=141 + i, wc=0.6,
               frame_at=lambda t, ph=ph: float(int((g0 + t) * 7 + ph * 4) % 4), motion=M.combine(bm, *vm))
    sc.add("rock", doc(PR.teaching_rock(ROCK[0], ROCK[1], JS, 1, time=TOD, seed=2)), z=zy(ROCK[1], -0.3), seed=107,
           motion=M.combine(*vm) if vm else None)
    sc.add("front", doc(PR.lake_hillside(HX0, HX1, HY, HS, time=TOD, part="front", seed=HSEED, bottom=H + 80)), z=40,
           seed=111, motion=M.combine(*vm) if vm else None)
    # flowers in the breeze at the bottom corners and by the rock (4 sway drawings, ping-pong on the film clock)
    clumps = [(-20, 520, H - 150, H - 30, 2.4, 61, 1.5), (W - 560, W + 10, H - 160, H - 30, 2.4, 63, 1.5),
              (250, 470, 1170, 1230, 1.6, 65, 0.9), (1150, 1420, 1245, 1300, 1.2, 67, 1.0)]
    for i, (x0, x1, y0, y1, dens, sd, s) in enumerate(clumps):
        frames = [doc(flowers_svg(x0, x1, y0, y1, dens, sd, s, sw)) for sw in (-1.0, -0.35, 0.35, 1.0)]

        def fa(t, i=i):
            extra = 1.0 * M.progress(t, gust[0] + 0.25 * i, gust[1] + 0.25 * i, "sine") if gust else 0.0   # whole cycles: s07 matches
            u = ((g0 + t) / 2.6 + i * 0.27 + extra) % 1.0
            v = 1.5 - 1.5 * math.cos(2 * math.pi * u)          # 0 .. 3 .. 0
            return v
        sc.add(f"flowers{i}", frames, z=41 + i * 0.01 if i < 2 else zy(y1, 0.2), seed=151 + i, frame_at=fa,
               motion=M.combine(*vm) if vm else None)
    if gust:                                     # a breeze runs over the grass: soft light bands sweep across the slope
        ga, gb = gust
        for k, (cy, ry, dl) in enumerate(((1010, 70, 0.0), (1150, 95, 0.35), (880, 50, 0.2))):
            def gm(t, dl=dl):
                u = (t - ga - dl) / (gb - ga)
                if u < 0 or u > 1:
                    return Tf(alpha=0.0)
                return Tf(dx=-1300 + (W + 1400) * u, alpha=math.sin(math.pi * u))
            sc.add(f"gust{k}", gust_band_svg(600, cy, 520, ry), z=zy(cy, 0.5) if k else 9.5, wc=0, blend="screen",
                   motion=M.combine(gm, *vm))
    stars = [(1640 + 380 * random.Random(70 + j).random(), 600 + 130 * random.Random(90 + j).random(), 5 + 4 * random.Random(j).random())
             for j in range(14)]
    sc.fx.append(GlobalFx(Twinkle(stars, color=(255, 240, 200), seed=7, base=0.6, period=(1.2, 2.6)), g0, vis))


class GlobalFx:
    """Run an output-space effect on the film clock (so s06's last second and s07's first second match); vis(t) gates it."""

    def __init__(self, fx, g0, vis=None):
        self.fx, self.g0, self.vis = fx, g0, vis

    def __call__(self, frame, t, view):
        if self.vis is not None and self.vis(t).alpha <= 0.01:
            return frame
        return self.fx(frame, self.g0 + t - G_REF, view)


def add_groups(sc, g0, plan, vis=None, prefix="g"):
    """Every seated group on its own flipbook layer. plan(g) -> [(t, mode, dip)] (first entry t <= 0 = the start
    state); featured people (FEATURED) are left out of the group drawings. Returns {gi: layer name}."""
    names = {}
    for g in GROUPS:
        ents = plan(g)
        modes = []
        for _, m_, _ in ents:
            if m_ not in modes:
                modes.append(m_)
        skip = FEAT_IDS[id(g)]
        xs = [p["x"] for p in g["people"]]
        ys = [p["y"] for p in g["people"]]
        mk = markers((min(xs) - 170 * g["k"], min(ys) - 420 * g["k"], max(xs) + 170 * g["k"], max(ys) + 80 * g["k"]))
        frames = [doc(group_svg(g, m_, skip) + mk) for m_ in modes]
        idx = {m_: i for i, m_ in enumerate(modes)}
        cuts = [(snap(t) if t > 0 else -1.0, idx[m_]) for t, m_, _ in ents]

        def fa(t, cuts=cuts):
            v = cuts[0][1]
            for tk, i in cuts:
                if t >= tk:
                    v = i
            return float(v)
        mots = [breath_g(g0, 3.0 + 0.37 * (g["gi"] % 5), 0.006, 0.13 * g["gi"])]
        mots += [dipm(snap(t), g["k"], dp) for t, _, dp in ents if t > 0 and dp]
        if vis:
            mots.append(vis)
        name = f"{prefix}{g['gi']}"
        sc.add(name, frames if len(frames) > 1 else frames[0], z=zy(g["y"]), seed=200 + g["gi"],
               frame_at=fa if len(frames) > 1 else None, motion=M.with_pivot(M.combine(*mots), (g["x"], g["y"])))
        names[g["gi"]] = name
    return names


def feat_end(p, role):
    """The featured person's drawing key at the end of s06 (= s07's start)."""
    sp = person_pose(p, "sit")
    return (sp, "happy", 0.0) if role == "child" else (sp, None, 0.0)


def heart_svg(x, y, r):
    return doc(heart_markup(x, y, r, "#f08c9a"))


def feat_svg(p, key):
    """A featured front-row person: key = (pose, expr, phase)."""
    pose, expr, ph = key
    mode = "sit" if pose.startswith("sit") else "stand"
    return person_svg(p, mode, pose=pose, expr=expr, phase=ph)


# ---------------------------------------------------------------- the end state (s07_bless starts from it)
END_JESUS = ("lap", "warm", (0.03, 0.0))
END_BOY = ("sit", "happy")
END_DISC = {"peter": ("stand", -1, "happy"), "john": ("stand", -1, "happy")}
END_WALK = [("talk", 1, "happy"), ("stand", -1, "happy"), ("talk", -1, "happy")]
CAM_END = Cam(W / 2, H / 2, W)


def boy_svg(key, x, y):
    pose, expr = key[:2]
    ph = key[2] if len(key) > 2 else 0.0
    return C.the_boy(x, y, BS, 1, pose=pose, expr=expr, basket=False, phase=ph)


def walker_end(j):
    v, a, b = WALKERS[j]
    return b


# ---------------------------------------------------------------- the high view
HV_K = 1.5                                    # the high view is drawn on a smaller box and scaled up (bigger, brighter heads)
HV_BOX = (0, 0, W / HV_K, H / HV_K)
HV_PTS = PR.hillside_high_points(*HV_BOX, rows=4, seed=HSEED, rock=False)


def hv_doc(body, defs=""):
    return doc(f'<g transform="scale({HV_K})">{body}</g>', defs)


def _hv_rock_bed():
    """The bed in the third row nearest the middle: its patch becomes Jesus's rock (well above the subtitles)."""
    beds = HV_PTS["beds"]
    ks = sorted({round(b[4], 4) for b in beds})
    k2 = ks[2]
    cand = [i for i, b in enumerate(beds) if round(b[4], 4) == k2]
    return min(cand, key=lambda i: abs(beds[i][0] - HV_BOX[2] / 2))


HV_ROCK_BED = _hv_rock_bed()
HV_BEDS = [b for i, b in enumerate(HV_PTS["beds"]) if i != HV_ROCK_BED]
_rb = HV_PTS["beds"][HV_ROCK_BED]
HV_ROCK = (_rb[0], _rb[1] + 0.05 * _rb[3], _rb[4] * 1.15)
HV_ROCK_STAGE = (HV_ROCK[0] * HV_K, HV_ROCK[1] * HV_K)


def hv_rock_svg():
    """The teaching rock seen from above with Jesus (cream and red) and the boy (marigold) sitting on it, the boy's
    basket between them; Peter and John beside it with their baskets; Andrew, Philip and James among the beds (the
    style of garden_beds' figures)."""
    pal = PR._lf_pal(TOD)
    rx, ry, rk = HV_ROCK
    out = S.path(S.blob(rx + 14 * rk, ry + 14 * rk, 70 * rk, 34 * rk, 0.2, 9, 3), fill=pal["shadow"], stroke=False, extra='opacity="0.25"')
    out += S.path(S.blob(rx, ry, 60 * rk, 32 * rk, 0.22, 9, HSEED + 7), fill=S.mix(pal["rock"], pal["rock_dk"], 0.35), sw=3.0)
    out += S.path(S.blob(rx - 12 * rk, ry - 8 * rk, 34 * rk, 13 * rk, 0.2, 7, HSEED + 8), fill=pal["rock_lt"], stroke=False, extra='opacity="0.8"')
    out += f'<circle cx="{rx + 26 * rk:.1f}" cy="{ry + 8 * rk:.1f}" r="{6 * rk:.1f}" fill="#a8b07a" opacity="0.6"/>'
    jx, jy = rx - 10 * rk, ry - 2 * rk
    out += C._ell(jx, jy - 2 * rk, 13 * rk, 9 * rk, C.JESUS_ROBE, sw=1.8)
    out += f'<path d="M{jx - 11 * rk:.1f},{jy - 6 * rk:.1f} L{jx + 9 * rk:.1f},{jy + 4 * rk:.1f}" stroke="{C.JESUS_MANTLE}" stroke-width="{4.5 * rk:.2f}"/>'
    out += f'<circle cx="{jx:.1f}" cy="{jy - 9 * rk:.1f}" r="{6.2 * rk:.2f}" fill="{C.JESUS_HAIR}" stroke="{INK}" stroke-width="1.4"/>'
    out += C._ell(jx + 3 * rk, jy + 7 * rk, 6.5 * rk, 5 * rk, "#d9a250", sw=1.4) + C._ell(jx + 3 * rk, jy + 6 * rk, 4.2 * rk, 3 * rk, "#efc678")
    bx, by = rx - 36 * rk, ry + 8 * rk
    out += C._ell(bx, by + 2 * rk, 7 * rk, 5 * rk, C.BOY_TUNIC, sw=1.4)
    out += f'<circle cx="{bx:.1f}" cy="{by - 3 * rk:.1f}" r="{4.4 * rk:.2f}" fill="{C.BOY_HAIR}" stroke="{INK}" stroke-width="1.2"/>'
    spots = [(rx + 84 * rk, ry + 4 * rk, 0, True), (rx + 116 * rk, ry + 22 * rk, 3, True)]
    beds = HV_BEDS
    for j, bi in enumerate((6, 9, 13)):
        cx, cy, w_, h_, k = beds[bi % len(beds)]
        spots.append((cx + w_ / 2 + 18 * k, cy + 0.15 * h_, (1, 4, 2)[j], False))
    for px, py, v, bsk in spots:
        k = rk
        col = C._DISCIPLES[v]["tunic"]
        hair = C._DISCIPLES[v]["hair"]
        out += C._ell(px, py + 3 * k, 9.5 * k, 7 * k, col, sw=1.6)
        out += f'<circle cx="{px:.1f}" cy="{py - 2.4 * k:.1f}" r="{5.4 * k:.2f}" fill="{hair}" stroke="{INK}" stroke-width="1.4"/>'
        if bsk:
            out += C._ell(px + 15 * k, py + 7 * k, 8.5 * k, 7.5 * k, "#d4a35a", sw=1.6) + C._ell(px + 15 * k, py + 5.5 * k, 5.6 * k, 4.4 * k, "#8a6236")
    return f'<g filter="url(#wobble-fine)">{out}</g>'


def hv_bed_svg(i):
    """One garden bed (index into HV_BEDS) with its own colour family (garden_beds cycles families by bed index)."""
    full_i = HV_PTS["beds"].index(HV_BEDS[i])
    fam = (full_i * 5 + HSEED) % 6
    return C.garden_beds(*HV_BOX, seed=fam + 6 * (full_i + 1), beds=[HV_BEDS[i]], jesus_=False, helpers=False, rock=False)


def counter_svg(n, cx, cy, s=1.0):
    """The picture-book counter: a big number in warm gold with a cream halo and an ink outline."""
    txt = f"{n}"
    defs = (S.lin_grad("lf6cg", [(0, "#ffe9a0"), (0.45, "#f7c24e"), (1, "#d9822e")]) +
            '<filter id="lf6csh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="8"/></filter>')
    size = 190 * s
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{f1(size)}" text-anchor="start"'
    b = (f'<text x="{f1(cx + 7 * s)}" y="{f1(cy + 12 * s)}" {font} fill="{INK}" opacity="0.3" filter="url(#lf6csh)" '
         f'stroke="{INK}" stroke-width="{f1(20 * s)}" stroke-linejoin="round">{txt}</text>')
    b += (f'<text x="{f1(cx)}" y="{f1(cy)}" {font} fill="#fff6e3" stroke="#fff6e3" stroke-width="{f1(26 * s)}" '
          f'stroke-linejoin="round">{txt}</text>')
    b += (f'<text x="{f1(cx)}" y="{f1(cy)}" {font} fill="url(#lf6cg)" stroke="{INK}" stroke-width="{f1(4.5 * s)}" '
          f'stroke-linejoin="round">{txt}</text>')
    return doc(b, defs)


def counter_icon_svg(cx, cy, s=1.0):
    """A little man (head and shoulders) beside the number: 'the men alone'."""
    man = C.galilee_folk(cx, cy, 0.62 * s, 1, kind="man", variant=8, pose="stand", expr="happy")
    halo = f'<circle cx="{f1(cx)}" cy="{f1(cy - 150 * s)}" r="{f1(118 * s)}" fill="#fff6e3" stroke="{INK}" stroke-width="{f1(4.5 * s)}"/>'
    cid = "lf6icon"
    clip = f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy - 150 * s)}" r="{f1(114 * s)}"/></clipPath>'
    return doc(S.g(halo, filter="wobble-fine") + clip + f'<g clip-path="url(#{cid})">{man}</g>')


COUNT_VALUES = [0, 30, 80, 150, 260, 400, 580, 800, 1050, 1350, 1650, 1950, 2300, 2650, 2950, 3250, 3550, 3800, 4050, 4250,
                4450, 4600, 4730, 4830, 4910, 4960, 5000]


class Burst:
    """A ring of sparkles flung out from (x, y) at t0 (stage px), fading over dur."""

    def __init__(self, x, y, t0, n=14, r=(80, 260), dur=1.1, color=(255, 236, 160), seed=3, size=(10, 20)):
        rng = random.Random(seed)
        self.x, self.y, self.t0, self.dur, self.color = x, y, t0, dur, color
        self.p = [(rng.uniform(0, 2 * math.pi), rng.uniform(*r), rng.uniform(*size), rng.uniform(0, 1)) for _ in range(n)]

    def __call__(self, frame, t, view):
        u = (t - self.t0) / self.dur
        if u < 0 or u > 1:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        e = 1 - (1 - u) ** 3
        for a, r, sz, ph in self.p:
            ox, oy = view.to_out(self.x + math.cos(a) * r * e, self.y + math.sin(a) * r * e * 0.8 + 30 * u * u)
            tw = 0.6 + 0.4 * math.sin(2 * math.pi * (u * 3 + ph))
            rr = sz * view.scale * (1 - 0.6 * u) * tw
            al = int(240 * (1 - u) ** 1.2)
            w = rr * 0.22
            d.polygon([(ox, oy - rr), (ox + w, oy - w), (ox + rr, oy), (ox + w, oy + w), (ox, oy + rr), (ox - w, oy + w),
                       (ox - rr, oy), (ox - w, oy - w)], fill=(*self.color, al))
        frame.alpha_composite(ov)
        return frame


# ================================================================== the scene
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(6)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731

    # ---- beats
    t_ye = b(0, "耶稣")
    t_mt = b(0, "门徒")
    t_jiao = b(1, "叫")
    t_zuo = b(1, "坐")
    t_lai = b(1, "来")
    t_l1e = ctx.lines[1].end
    t_nali = b(2, "那里")
    t_qc = b(2, "青草")
    t_pai1 = b(2, "一排", 0)
    t_pai2 = b(2, "一排", 1)
    t_zu1 = b(2, "一组", 0)
    t_zu2 = b(2, "一组", 1)
    t_zx = b(2, "坐下")
    t_100 = b(2, "一百")
    t_50 = b(2, "五十")
    t_l2e = ctx.lines[2].end
    t_cong = b(3, "从高处看")
    t_kuai = b(3, "一块", 0)
    t_hy = b(3, "花园")
    t_l3e = ctx.lines[3].end
    t_gs = b(4, "光是")
    t_5k = b(4, "五千")
    t_hai = b(4, "还有")
    t_mama = b(4, "妈妈")
    t_xpy = b(4, "小朋友")
    t_zg = b(4, "整个山坡")
    t_l4e = ctx.lines[4].end

    T_HV = snap(t_cong - 0.12)                 # cut to the high view
    T_BACK = snap(t_hai - 0.12)                # cut back to the hillside
    side_vis = gate(T_HV, T_BACK)
    hv_vis = only(T_HV, T_BACK)

    # ---- the hillside world
    add_world(sc, g0, side_vis, gust=(t_nali - 0.1, t_nali + 2.4))

    # ---- the groups: stand, then sit (rows on '一排', groups on '一组', the front two on '一百' / '五十')
    sit_t = {}
    rows = {}
    for g in GROUPS:
        rows.setdefault(g["row"], []).append(g)
    for g in rows[0]:
        sit_t[g["gi"]] = t_pai1 + 0.04 + 0.03 * (g["x"] / W)
    for g in rows[1]:
        sit_t[g["gi"]] = t_pai2 + 0.02 + 0.05 * (g["x"] / W)
    for g in rows[2]:
        sit_t[g["gi"]] = t_pai2 + 0.42 + 0.08 * (g["x"] / W)
    mid = sorted(rows[3], key=lambda g: g["x"]) + sorted(rows[4], key=lambda g: g["x"])
    span = max(0.6, (t_zx + 0.15) - t_zu1)
    for j, g in enumerate(mid):
        sit_t[g["gi"]] = t_zu1 + 0.02 + span * j / max(1, len(mid) - 1)
    sit_t[G100["gi"]] = t_100 - 0.04
    sit_t[G50["gi"]] = t_50 - 0.04

    def plan(g):
        return [(-1, "stand", None), (sit_t[g["gi"]], "sit", 7 if g["row"] >= 3 else 5)]
    add_groups(sc, g0, plan, side_vis)

    # featured front-row people follow their group's sit cut; C1: mothers rock, children pop up and wave
    for j, (g, p, role) in enumerate(FEATURED):
        ts = sit_t[g["gi"]]
        a = Actor(f"feat{j}", (p["x"], p["y"]), p["k"], lambda key, p=p: feat_svg(p, key), zy(p["y"], 0.001), 300 + j, g0)
        sit_pose = person_pose(p, "sit")
        a.cut(-1, (person_pose(p, "stand"), None, 0.0))
        a.cut(ts, (sit_pose, None, 0.0), dip=7)
        if role == "recv":
            pass
        elif role == "mother":
            a.cut(t_mama - 0.05, (sit_pose, "kind", 0.0))

            def rock_m(t, t0=t_mama + 0.05 * j, k=p["k"]):
                u = t - t0
                if u < 0 or u > 2.6:
                    return Tf()
                env = min(1.0, u / 0.3, (2.6 - u) / 0.5)
                return Tf(rot=3.2 * env * math.sin(2 * math.pi * u / 1.0))
            a.extra.append(rock_m)
            a.cut(t_mama + 2.7, feat_end(p, role))
            for q in range(2):                                     # little hearts float up from the mother
                hx, hy = p["x"] + p["f"] * 14 * p["k"], p["y"] - 205 * p["k"]
                t0h = t_mama + 0.25 + 0.7 * q + 0.1 * j
                sc.add(f"heart{j}_{q}", heart_svg(hx, hy, 15 * p["k"]), z=zy(p["y"], 0.002), wc=0.3, seed=330 + j * 3 + q,
                       motion=M.combine(pop_hold(t0h, (hx, hy), 0.9, 0.5, 70 * p["k"]), side_vis,
                                        lambda t, t0h=t0h: Tf(dx=8 * math.sin(3 * (t - t0h)))))
        else:
            tu = t_xpy - 0.06 + 0.12 * (j % 3)
            a.loop(tu, [("wave", "delighted", ph) for ph in (0.0, 0.33, 0.67)], 0.36, dip=None)
            a.extra.append(hopm(tu, p["k"], 30, 0.36))
            a.cut(tu + 1.25, feat_end(p, role), dip=7)
        a.blinks(blink_times(1.0, T - 1.3, rng, 3.4), {})
        a.gates.append(side_vis)
        a.build(sc)

    # ---- the 100 / 50 tags
    for g, t0, lab in ((G100, t_100, "100"), (G50, t_50, "50")):
        top = min(p["y"] - 250 * p["k"] for p in g["people"])
        tx, ty = g["x"] + 10, top - 6
        sc.add(f"tag{lab}", tag_svg(tx, ty, lab, 1.6), z=60, wc=0, motion=pop_hold(t0 - 0.02, (tx, ty), 1.5))
        sc.fx.append(Burst(tx, ty - 48, t0 + 0.05, n=10, r=(60, 150), dur=0.9, seed=hash(lab) % 97))

    # ---- Jesus
    t_up = snap(t_ye + 0.05)
    t_hip = snap(t_mt + 0.15)
    t_g0 = snap(t_jiao - 0.1)
    t_rest = snap(t_l1e + 0.25)
    t_boy_sit = snap(t_50 + 0.55)
    t_j_sit = snap(t_50 + 0.95)
    jes = Actor("jesus", JSTAND, JS, lambda key: jesus_svg(key), zy(JSTAND[1]), 109, g0)
    jes.cut(-1, ("hold", "kind", (0.04, 0.06), -1))                 # smiling down at the boy on his left
    jes.cut(t_up, ("hold", "warm", (0.03, 0.0)), dip=5)            # '耶稣对门徒说': he turns to the disciples
    jes.cut(t_hip, ("ready", "warm", (0.03, 0.0)), dip=4)
    jes.cut(t_g0, ("gesture", 0.0), dip=4)
    # pats on '坐' and '来' (phase 0 -> 1 lowers and lifts the near hand)
    for tp_ in (t_zuo - 0.12, t_lai - 0.1):
        for q, ph in enumerate((0.25, 0.5, 0.75, 0.0)):
            jes.cut(tp_ + 0.1 * q, ("gesture", ph))
    jes.cut(t_rest, ("ready", "smile", (0.03, 0.0)), dip=4)
    jes.cut(snap(t_rest + 1.1), ("ready", "warm", (0.03, 0.0)))
    jes.cut(snap(t_pai1 - 0.3), ("ready", "kind", (0.04, -0.02)))
    jes.cut(t_j_sit, END_JESUS, dip=10)
    jes.blinks(blink_times(0.6, T - 1.3, rng, 3.0), {
        ("hold", "warm", (0.03, 0.0)): ("hold", blink("warm"), (0.03, 0.0)),
        ("ready", "smile", (0.03, 0.0)): ("ready", blink("smile"), (0.03, 0.0)),
        ("ready", "warm", (0.03, 0.0)): ("ready", blink("warm"), (0.03, 0.0)),
        ("ready", "kind", (0.04, -0.02)): ("ready", blink("kind"), (0.04, -0.02)),
        END_JESUS: ("lap", blink("warm"), (0.03, 0.0))})
    jes.extra.append(lambda t: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.4)))
    jes.gates.append(side_vis)
    jes.build(sc)

    # ---- the boy
    boy = Actor("boy", BOY_STAND, BS, lambda key: boy_svg(key, *(BOY_SIT if key[0] == "sit" else BOY_STAND)),
                zy(BOY_STAND[1]), 113, g0)
    boy.cut(-1, ("smile", "happy"))
    boy.cut(snap(t_ye + 0.25), ("stand", "happy"), dip=3)
    boy.cut(snap(t_zu1 + 0.3), ("watch", "awed"), dip=4)
    boy.cut(t_boy_sit, END_BOY, dip=9)
    boy.blinks(blink_times(0.8, T - 1.3, rng, 2.8), {("stand", "happy"): ("stand", blink("happy")),
                                                     END_BOY: ("sit", blink("happy"))})
    boy.extra.append(lambda t: Tf(sy=1 + 0.008 * math.sin(2 * math.pi * (g0 + t) / 2.6 + 1)))
    boy.gates.append(side_vis)
    boy.build(sc)

    # ---- Peter and John: they turn and call to the families nearby, then turn back to Jesus
    for name, (v, (x, y)) in DISC.items():
        s = k_of_y(y)
        d = Actor(name, (x, y), s, lambda key, v=v, x=x, y=y, s=s: disc_svg(v, x, y, s, key), zy(y), 120 + v, g0)
        dj = 0.0 if name == "peter" else 0.18
        d.cut(-1, ("stand", -1, "happy"))
        d.cut(snap(t_jiao + 0.3 + dj), ("stand", -1, "awed"))
        d.cut(snap(t_l1e + 0.1 + dj), ("talk", 1, "happy"), dip=4)
        d.cut(snap(t_qc + 0.2 + dj), ("point" if name == "john" else "talk", 1, "happy"), dip=3)
        d.cut(snap(t_zu2 + 0.3 + dj), ("stand", 1, "happy"), dip=3)
        d.cut(snap(t_50 + 1.1 + dj), END_DISC[name], dip=4)
        d.blinks(blink_times(0.7, T - 1.3, rng, 3.3), {("stand", -1, "happy"): ("stand", -1, blink("happy")),
                                                       ("stand", 1, "happy"): ("stand", 1, blink("happy"))})
        d.extra.append(lambda t, v=v: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.1 + v)))
        d.gates.append(side_vis)
        d.build(sc)
        bx, by = basket_spot(x, y, s, -1)
        sc.add(f"{name}_basket", doc(ground_basket_svg(x, y, s, -1, seed=11 + v)), z=zy(by, -0.004), seed=125 + v, motion=side_vis)

    # ---- Andrew, Philip and James go out to the people (planted-foot strides), then call the groups to sit
    for j, (v, (x0, y0), (x1, y1)) in enumerate(WALKERS):
        s = k_of_y(y0)
        d = Actor(f"walker{j}", (x0, y0), s, lambda key, v=v, x0=x0, y0=y0, s=s: disc_svg(v, x0, y0, s, key), zy(y0), 130 + v, g0)
        t0 = snap(t_l1e + 0.2 + 0.22 * j)
        stride = DISC_ADV * s
        n = max(1, int(round((x1 - x0) / stride)))
        adv = (x1 - x0) / n
        d.cut(-1, ("stand", -1, "happy"))
        d.cut(snap(t_jiao + 0.25 + 0.1 * j), ("stand", -1, "awed"))
        d.cut(snap(t0 - 0.32), ("stand", 1, "happy"), dip=4)
        t_last = d.walk(t0, [("walk_a", 1, "happy"), ("walk_b", 1, "happy")], n, 0.3, adv, 1)
        d.cut(t_last + 0.3, END_WALK[j] if j != 1 else ("talk", 1, "happy"), dip=4)
        if j == 1:
            d.cut(snap(t_zx + 0.4), END_WALK[1], dip=3)
        d.extra.append(lambda t, v=v: Tf(sy=1 + 0.006 * math.sin(2 * math.pi * (g0 + t) / 3.2 + v)))
        d.gates.append(side_vis)
        d.build(sc)
        # every cut of the walk moves the layer; the drawings are made at the start anchor

    # ---- the high view
    sc.add("hv_back", hv_doc(PR.hillside_high(*HV_BOX, time=TOD, seed=HSEED, rock=False)), z=60, seed=401, motion=hv_vis)
    beds = HV_BEDS
    order = sorted(range(len(beds)), key=lambda i: (beds[i][0] - HV_BOX[2] / 2) * 0.6 + beds[i][1] * 1.0)
    pop0, pop1 = t_kuai - 0.05, t_hy + 0.25
    for rank, bi in enumerate(order):
        cx, cy, w_, h_, k = beds[bi]
        tp_ = pop0 + (pop1 - pop0) * rank / max(1, len(order) - 1)

        def bed_pop(t, tp_=tp_):
            u = t - tp_
            if u < 0 or u > 0.55:
                return Tf()
            e = math.sin(math.pi * u / 0.55)
            return Tf(sx=1 + 0.07 * e, sy=1 + 0.07 * e, dy=-6 * e)
        sc.add(f"bed{bi}", hv_doc(hv_bed_svg(bi)), z=61 + 0.001 * bi, seed=420 + bi,
               motion=M.with_pivot(M.combine(bed_pop, hv_vis), (cx * HV_K, cy * HV_K)))
    gx_, gy_ = HV_ROCK[0], HV_ROCK[1]
    sc.add("hv_glow", hv_doc(f'<ellipse cx="{gx_:.1f}" cy="{gy_:.1f}" rx="{120 * HV_ROCK[2]:.1f}" ry="{70 * HV_ROCK[2]:.1f}" '
                             f'fill="url(#lf6hg)"/>', S.rad_grad("lf6hg", [(0, "#fff2c4", 0.75), (0.5, "#ffe39a", 0.35), (1, "#ffe39a", 0)])),
           z=61.9, wc=0, blend="screen", motion=M.combine(hv_vis, lambda t: Tf(alpha=0.8 + 0.2 * math.sin(2 * math.pi * (g0 + t) / 2.4))))
    sc.add("hv_rock", hv_doc(hv_rock_svg()), z=62, seed=451, motion=hv_vis)
    # soft cloud shadows drifting over the meadow
    for i, (cx, cy, rx, ry, v) in enumerate(((600, 500, 520, 260, 26.0), (1900, 1050, 600, 280, 22.0))):
        defs = S.rad_grad(f"lf6cs{i}", [(0, "#2f4a2a", 0.22), (0.7, "#2f4a2a", 0.12), (1, "#2f4a2a", 0)])
        sc.add(f"cshadow{i}", doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#lf6cs{i})"/>', defs), z=63 + 0.01 * i,
               wc=0, seed=461 + i, motion=M.combine(lambda t, v=v: Tf(dx=v * (t - T_HV)), hv_vis))
    lake_stars = [(200 + 2160 * random.Random(500 + j).random(), 40 + 190 * random.Random(600 + j).random(),
                   8 + 6 * random.Random(700 + j).random()) for j in range(16)]
    sc.fx.append(Twinkle(lake_stars, alpha_fn=lambda t: hv_vis(t).alpha, color=(255, 244, 214), seed=9, base=0.6, period=(1.1, 2.4)))
    for i, (y0, v, ph) in enumerate(((330, 150.0, 0.0), (420, 120.0, 0.5))):
        frames = [doc(swallow_svg(0, y0, 2.0, w)) for w in (0.0, 0.5, 1.0, 0.5)]
        sc.add(f"hv_bird{i}", frames, z=64 + 0.01 * i, seed=471 + i, wc=0.6,
               frame_at=lambda t, ph=ph: float(int((g0 + t) * 7 + ph * 4) % 4),
               motion=M.combine(lambda t, v=v, ph=ph: Tf(dx=-300 + v * (t - T_HV) + 700 * ph, dy=14 * math.sin(t * 0.9 + ph * 5)), hv_vis))

    # ---- the counter (光是男人，就有五千个！)
    CX, CY = W / 2 - 150, 300                  # the number starts here (left-aligned, it grows to the right)
    c0, c1 = t_gs + 0.12, t_5k + 0.05
    nvals = len(COUNT_VALUES)
    cframes = [counter_svg(v_, CX, CY, 1.0) for v_ in COUNT_VALUES]

    def cfa(t):
        u = (t - c0) / max(0.3, c1 - c0)
        u = max(0.0, min(1.0, u))
        return float(min(nvals - 1, int((1 - (1 - u) ** 1.6) * (nvals - 1) + 1e-6)))

    def cmot(t):
        if t < c0 - 0.3 or t >= T_BACK:
            return Tf(alpha=0.0)
        a = M.progress(t, c0 - 0.3, c0, "sine")
        u = t - c1
        s_ = 1.0 + (0.18 * math.sin(math.pi * min(1.0, u / 0.35)) if 0 <= u <= 0.35 else 0.0)
        return Tf(alpha=a, sx=s_, sy=s_, px=CX + 200, py=CY - 60)
    sc.add("counter", cframes, z=80, wc=0, frame_at=cfa, motion=cmot)
    ix, iy = CX - 150, CY + 80
    sc.add("counter_icon", counter_icon_svg(ix, iy, 0.95), z=80.1, wc=0.4, seed=481,
           motion=lambda t: Tf(alpha=0.0) if (t < c0 - 0.3 or t >= T_BACK) else
           Tf(alpha=M.progress(t, c0 - 0.3, c0, "sine"), sx=0.6 + 0.4 * M.progress(t, c0 - 0.3, c0 + 0.1, "back"),
              sy=0.6 + 0.4 * M.progress(t, c0 - 0.3, c0 + 0.1, "back"), px=ix, py=iy - 140))
    sc.fx.append(Burst(CX + 220, CY - 70, c1, n=18, r=(120, 420), dur=1.2, seed=17, size=(12, 24)))
    sc.fx.append(FX.sparkles((CX - 200, CY - 220, CX + 640, CY + 60), count=16, t0=c1, t1=T_BACK, color=(255, 236, 160),
                             size=(8, 15), period=1.2, drift=-10, seed=19))

    # ---- camera
    c_a0 = Cam(980, 880, 1500)
    c_a1 = Cam(940, 868, 1440)
    c_wide = Cam(1440, 805, 2240)
    c_wide2 = Cam(1420, 800, 2180)
    c_rise = Cam(1420, 760, 2080)
    side_a = cam_path([(0.0, c_a0), (t_l1e + 0.3, c_a1), (t_qc + 1.5, c_wide), (t_l2e - 0.2, c_wide2), (T_HV, c_rise)],
                      ["sine", "inout", "linear", "in"])
    rx, ry = HV_ROCK_STAGE
    h0 = Cam(rx + 40, ry - 40, 1380)
    h1 = Cam(W / 2 + 30, H / 2 + 20, 2440)
    h2 = Cam(W / 2 - 30, H / 2 + 8, 2440)
    high = cam_path([(T_HV, h0), (t_hy + 0.4, h1), (T_BACK, h2)], ["inout", "linear"])
    c_c1 = Cam(1955, 1000, 1150)
    c_c1b = Cam(1915, 992, 1210)
    side_c = cam_path([(T_BACK, c_c1), (t_zg - 0.05, c_c1b), (t_zg + 2.15, CAM_END), (T, CAM_END)], ["sine", "inout", "linear"])

    def camera(t):
        if t < T_HV:
            return side_a(t)
        if t < T_BACK:
            return high(t)
        return side_c(t)
    sc.camera = camera

    # ---- sound
    sc.sfx("crowd", 0, dur=T + 0.5, gain_db=-19, fade_in=0.6, fade_out=1.0, pan=0.2)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("cloth", t_hip, gain_db=-20, pan=-0.4)
    sc.sfx("cloth", t_g0 + 0.05, gain_db=-19, pan=-0.4)
    sc.sfx("footsteps", t_l1e + 0.2, dur=3.6, gain_db=-21, fade_in=0.3, fade_out=0.5, pan=0.3)
    sc.sfx("wind_soft", t_nali - 0.2, dur=2.6, gain_db=-15, fade_in=0.6, fade_out=1.2)
    for k_, tc in enumerate((t_pai1, t_pai2, t_pai2 + 0.42, t_zu1 + 0.1, t_zu2 + 0.1, t_zx)):
        sc.sfx("cloth", tc + 0.02, gain_db=-17 - (k_ % 2) * 2, pan=0.3 - 0.1 * k_)
    sc.sfx("crowd", t_pai1 - 0.2, dur=3.6, gain_db=-15, fade_in=0.5, fade_out=1.2, pan=0.2)
    sc.sfx("pop", t_100, gain_db=-13, pan=0.5)
    sc.sfx("cloth", t_100 + 0.03, gain_db=-15, pan=0.5)
    sc.sfx("pop", t_50, gain_db=-14, pan=0.7)
    sc.sfx("cloth", t_50 + 0.03, gain_db=-16, pan=0.7)
    sc.sfx("cloth", t_boy_sit, gain_db=-19, pan=-0.3)
    sc.sfx("cloth", t_j_sit, gain_db=-18, pan=-0.4)
    sc.sfx("whoosh", T_HV - 0.25, gain_db=-17)
    sc.sfx("chime", t_hy - 0.3, gain_db=-17)
    sc.sfx("grow", c0, gain_db=-16)
    sc.sfx("sparkle", c1, gain_db=-11)
    sc.sfx("chime", c1 + 0.05, gain_db=-15)
    sc.sfx("crowd", T_BACK, dur=T - T_BACK + 0.5, gain_db=-16, fade_in=0.2, fade_out=1.0, pan=0.3)
    sc.sfx("pop", t_xpy, gain_db=-17, pan=0.4)
    sc.sfx("cheer", t_xpy, dur=1.6, gain_db=-20, fade_in=0.15, fade_out=0.8, pan=0.4)
    sc.sfx("crowd", t_zg, dur=2.6, gain_db=-14, fade_in=0.6, fade_out=1.5)
    return sc
