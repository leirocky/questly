"""Scene 3 - Luke 15:1-2. The outer story: a warm, earthy courtyard meal. An arched gate on the left opens onto a sunny
street; the long low table stands in front of the ochre wall (vine on the pergola, a lamp niche, a striped door curtain,
a window); a big fig tree on the right. Jesus welcomes the guests, the tax collectors (one counting his coins) and the
people nobody liked, and eats with them; at the edge, by the fig tree, three Pharisees frown and grumble.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity film's
Tm class, chunk fallback; nothing is hard-coded to the take):
  0 .. 0.9      calm wide page (the page-dip lands here): Jesus stands at his place behind the table, two tax
                collectors have just come in at the gate, the third already sits counting coins; townsfolk chat in the
                street outside the gate; clouds drift, sparrows hop on the wall, the fig tree stirs
  '有一天'       the two tax collectors walk in along the wall (planted-foot strides, footsteps)
  '好多人来'     Jesus opens his arms wide in welcome; they reach their cushions
  '讲道'         they sit down (squash-hop), Jesus sits and begins to teach (sit_tell); the guests listen
  '来的人里'     the camera moves along the table to the tax collectors
  '收税'         the tax collector with the ledger looks up with a sly little grin
  '常常'         he counts coins onto a stack on the table (a clink on each '常')
  '多收'         two extra coins hop onto the stack, it grows tall; sly sideways glance
  '别人的钱'     he sweeps them into his fat money bag, which bulges (coins), with a sly little grin
  '还有一些人'   the camera eases back and over to the gate: three people nobody liked come along the street,
                heads down
  '做过很多错事' they walk in through the gate, timid and sorry, and stop just inside
  '大家都不喜欢'  outside the gate the townsfolk turn their backs, noses up with a 'hmph' puff; one points and
                mutters (on '不'); the woman looks back, a tear in her eye
  '可是耶稣'     wide: Jesus gets up (hop) ...
  '很欢迎'       ... and opens his arms wide to them; they look up, touched
  '欢迎他们'     they walk to the empty cushions at the table
  '还和他们'     they sit down, Jesus sits; '一起吃' he breaks the bread (crumbs)
  '饭'           everyone laughs together (sit_laugh / laugh / toast)
  '旁边站着'     the camera pans right to three Pharisees standing by the fig tree, frowning
  '守'           the elder brings out the scroll of the law and unrolls it, reverent; the others nod; just before
               '看不起' he rolls it up again and tucks it away
  '看不起'       they fold their arms, chin up, looking down on the guests (disdain)
  '皱着眉头'     closer: frowns; '小声说' two lean in and whisper behind a hand
  P '哼'         the elder turns to the table with a 'hmph' puff and grumbles, gesturing at the meal, his head
                shaking ('这个人怎么...')
  end          calm hold, the camera eases back to Jesus and the Pharisees: the last second is identical to s04's
               first (plain cross-dissolve; all ambient motion runs on the film's global clock)
The courtyard set, the cast and the helpers below are shared with s04_story and s11_meaning.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s07_shepherds import Fig, Tm, clamp_cam, env, snap

INK = P["ink"]

# ------------------------------------------------------------------ the courtyard stage (shared with s04 / s11)
W3, H3 = 3200, 1188
K = 1.05                              # people scale
SY = 955                              # the floor line under the cushions (the meal recipe's table_y - DEPTH*s)
SEAT_Y = SY - PR.CUSHION_TOP * K      # seated guests' anchor
TY = SY + PR.LOW_TABLE_DEPTH * K      # low_table anchor (floor under its front edge)
WY = SY - 120 * K                     # the back wall's base
WTOP = SY - 760 * K                   # the top of the wall
BACK_Y = SY - 42                      # the walking line behind the seated row
STAND_Y = SY - 14                     # Jesus standing at his place (the table hides his shins)
GX, GW = 380, 210                     # the street gate: centre, half-width of the opening
G_SPRING, G_RISE = WY - 430, 150      # arch: the spring line and its rise
G_FRAME = 44                          # stone frame width
G_RIGHT = GX + GW + G_FRAME           # the frame's outer right edge (the wall overlay ends here)
STREET_Y = WY - 72                    # the far side of the street outside (townsfolk)
OUT_Y = WY - 14                       # the near side of the street (people walking to the gate)
DOOR_X, NICHE_X, NICHE2_X, WIN_X, WIN2_X = 860, 1240, 2250, 1700, 2640
TREE = (3010, WY + 34)
TABLE_X, TABLE_W = 1460, 1270
SEATS = {"labourer": 1010, "young": 1160, "woman": 1310, "tax2": 1460, "tax1": 1610, "jesus": 1760, "tax0": 1910}
PH = {2: (2575, SY + 22), 1: (2715, SY + 28), 0: (2440, SY + 38)}     # the Pharisees (variant: anchor), back to front
TOWN = {"elder": (GX - 140, STREET_Y + 4), "woman": (GX + 15, STREET_Y + 7), "man": (GX + 140, STREET_Y)}
TK = 0.82                             # townsfolk scale factor (across the street)
COINS = (2030, 906)                   # the coin stack on the table beside the ledger
POUCH = (2082, 921)

WALL_C = {"day": "#e6bb80", "evening": "#d9a070"}
SKY_C = {"day": ("#f2d2a0", "#fbe8c6"), "evening": ("#e0926e", "#f4c892")}

BLINKABLE = ("neutral", "kind", "warm", "happy", "smile", "touched", "sorry", "sad", "worried", "stern", "disdain",
             "mutter", "ponder", "softened", "sly", "smug", "surprised", "teary", "calm", "determined")


def f1(v):
    return f"{v:.1f}"


def doc3(body, defs=""):
    return S.svg_doc(body, defs, W3, H3)


def bexpr(e):
    """The closed-eye version of expression e (registered once)."""
    n = f"ls3b_{e}"
    if n not in C.EXPRS:
        C.EXPRS[n] = dict(C.EXPRS[e], eyes="closed")
    return n


def cam3(keys, curves):
    f = M.cam_keys([(t, clamp_cam(c, W3, H3)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), W3, H3)


def cam_seq(keys):
    """keys [(t, Cam[, curve])]: holds are linear, moves 'sine' unless a curve is given for the segment arriving at
    the key; clamped to the stage."""
    keys = sorted(keys, key=lambda k: k[0])
    curves = []
    for i in range(1, len(keys)):
        if len(keys[i]) > 2:
            curves.append(keys[i][2])
        else:
            curves.append("linear" if keys[i][1] == keys[i - 1][1] else "sine")
    return cam3([(k[0], k[1]) for k in keys], curves or "linear")


def log_push(t0, t1, c0, c1, curve="sine"):
    """A zoom between two framings in log space about their common fixed point (the page stays put on screen while
    the camera flies into / out of it): constant visual zoom speed."""
    r = c1.w / c0.w
    fx = (c1.x - r * c0.x) / (1 - r) if abs(1 - r) > 1e-6 else c0.x
    fy = (c1.y - r * c0.y) / (1 - r) if abs(1 - r) > 1e-6 else c0.y

    def cam(t):
        u = M.progress(t, t0, t1, curve)
        w = c0.w * r ** u
        k = w / c0.w
        return Cam(fx + (c0.x - fx) * k, fy + (c0.y - fy) * k, w)
    return cam


def splice(base, t0, t1, mid):
    """Camera = base outside [t0, t1], mid inside."""
    return lambda t: mid(t) if t0 <= t <= t1 else base(t)


def breath(piv, g0, period=3.2, amount=0.011, phase=0.0):
    return lambda t: Tf(sx=1 + 0.3 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def lean(t_on, t_off, deg, piv, fin=0.35, fout=0.4):
    """A gentle lean (rotation about the feet / seat) between t_on and t_off."""
    return lambda t: Tf(rot=deg * env(t, t_on, t_off, fin, fout), px=piv[0], py=piv[1])


# ------------------------------------------------------------------ the backdrop
def sky_svg(time="day"):
    a, b = SKY_C[time]
    defs = S.lin_grad(f"ls3sky{time}", [(0, a), (1, b)])
    return doc3(f'<rect x="-20" y="-20" width="{W3 + 40}" height="{f1(WTOP + 60)}" fill="url(#ls3sky{time})"/>', defs)


def clouds_svg(time="day"):
    fill = "#fbf1de" if time == "day" else "#f6c9a8"
    sh = "#f0d6b0" if time == "day" else "#e3a283"
    rng = random.Random(31)
    b = ""
    x = -500
    while x < W3 + 700:
        w = rng.uniform(150, 230)
        b += S.cloud(x, rng.uniform(62, 92), w, w * 0.32, fill, seed=int(x) % 97, sw=3.0, shade_fill=sh)
        x += w + rng.uniform(300, 520)
    return doc3(S.g(b, filter="wobble"))


def _stones(rng, x0, x1, y0, y1, wall, n):
    b = ""
    for _ in range(n):
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        b += PR._ell(px, py, rng.uniform(16, 30) * K, rng.uniform(9, 15) * K, S.shade(wall, -0.10), 2 * K,
                     stroke=S.shade(wall, -0.3), extra='opacity="0.55"')
    return b


def _arch_d(x0, x1, ybase, yspring, rise):
    """A round-topped opening from ybase up to the spring line and an elliptical arch of height rise."""
    rx = (x1 - x0) / 2
    return (f"M{f1(x0)},{f1(ybase)} L{f1(x0)},{f1(yspring)} A{f1(rx)},{f1(rise)} 0 0 1 {f1(x1)},{f1(yspring)} "
            f"L{f1(x1)},{f1(ybase)} Z")


GATE_D = _arch_d(GX - GW, GX + GW, WY + 2, G_SPRING, G_RISE)


def wall_body(time="day"):
    """The ochre wall, pergola and vine, the striped door curtain, the lamp niche, two windows, jars and the floor
    (the same recipe and colours as props.courtyard, laid out for this stage around the street gate)."""
    s = K
    wall = WALL_C[time]
    rng = random.Random(3)
    b = PR._rect(-20, WTOP, W3 + 40, WY - WTOP + 6, wall, 4 * s)
    b += _stones(rng, -20, W3 + 20, WTOP + 30 * s, WY - 30 * s, wall, int(W3 / (110 * s)) * 3)
    b += PR._rect(-20, WTOP - 26 * s, W3 + 40, 30 * s, S.shade(wall, -0.15), 3.4 * s)
    for bx in range(-20, W3 + 20, int(70 * s)):
        b += PR._circ(bx + 20 * s, WTOP + 10 * s, 8 * s, "#8a5a36", 2.4 * s)
    # the striped door curtain (into the house)
    dx, wy = DOOR_X, WY
    b += PR._p(f"M{f1(dx - 110 * s)},{f1(wy)} L{f1(dx - 110 * s)},{f1(wy - 300 * s)} Q{f1(dx)},{f1(wy - 380 * s)} "
               f"{f1(dx + 110 * s)},{f1(wy - 300 * s)} L{f1(dx + 110 * s)},{f1(wy)} Z", "#5a3a30", 4 * s)
    for k in range(5):
        cx0 = dx - 100 * s + k * 40 * s
        col = ("#c8693e", "#e8b65a", "#c8693e", "#7a8a3a", "#c8693e")[k]
        b += PR._p(f"M{f1(cx0)},{f1(wy - 330 * s + abs(k - 2) * 14 * s)} L{f1(cx0 + 40 * s)},"
                   f"{f1(wy - 330 * s + abs(k - 1.5) * 14 * s)} L{f1(cx0 + 44 * s)},{f1(wy - 10 * s)} "
                   f"L{f1(cx0 - 4 * s)},{f1(wy - 10 * s)} Z", col, 2.4 * s)
    # windows
    for wx, top in ((WIN_X, 560), (WIN2_X, 600)):
        b += PR._p(f"M{f1(wx - 60 * s)},{f1(wy - (top - 180) * s)} L{f1(wx - 60 * s)},{f1(wy - (top - 60) * s)} "
                   f"Q{f1(wx)},{f1(wy - top * s)} {f1(wx + 60 * s)},{f1(wy - (top - 60) * s)} "
                   f"L{f1(wx + 60 * s)},{f1(wy - (top - 180) * s)} Z", "#6a4a3a", 3.6 * s)
        b += PR._rect(wx - 76 * s, wy - (top - 174) * s, 152 * s, 16 * s, S.shade(wall, -0.2), 3 * s)
    # the lamp niche
    nx = NICHE_X
    b += PR._p(f"M{f1(nx - 40 * s)},{f1(wy - 300 * s)} L{f1(nx - 40 * s)},{f1(wy - 380 * s)} Q{f1(nx)},{f1(wy - 420 * s)} "
               f"{f1(nx + 40 * s)},{f1(wy - 380 * s)} L{f1(nx + 40 * s)},{f1(wy - 300 * s)} Z", "#9a6a4a", 3 * s)
    b += PR._g(PR._oil_lamp(True, f"ls3lamp{time}"), f"translate({f1(nx)},{f1(wy - 302 * s)}) scale({f1(0.7 * s)})")
    b += PR._ls_glow(nx, wy - 330 * s, 120 * s, 100 * s, 0.5 if time == "day" else 0.9, f"ls3n{time}")
    nx = NICHE2_X
    b += PR._p(f"M{f1(nx - 40 * s)},{f1(wy - 330 * s)} L{f1(nx - 40 * s)},{f1(wy - 410 * s)} Q{f1(nx)},{f1(wy - 450 * s)} "
               f"{f1(nx + 40 * s)},{f1(wy - 410 * s)} L{f1(nx + 40 * s)},{f1(wy - 330 * s)} Z", "#9a6a4a", 3 * s)
    b += PR._g(PR._oil_lamp(True, f"ls3lamp2{time}"), f"translate({f1(nx)},{f1(wy - 332 * s)}) scale({f1(0.7 * s)})")
    b += PR._ls_glow(nx, wy - 360 * s, 120 * s, 100 * s, 0.45 if time == "day" else 0.9, f"ls3n2{time}")
    # the soft shade under the pergola
    b += (f'<rect x="-20" y="{f1(WTOP + 52 * s)}" width="{W3 + 40}" height="{f1(110 * s)}" fill="{INK}" opacity="0.07" '
          f'filter="url(#blur-md)"/>')
    # the pergola beam and the vine
    b += PR._rect(-20, WTOP + 40 * s, W3 + 40, 18 * s, "#9a6236", 3 * s)
    for vx, ln, sd in ((1020, 210, 1), (1500, 150, 2), (2090, 240, 3), (2870, 190, 4)):
        r2 = random.Random(sd)
        pts = [(vx + 18 * math.sin(k * 1.3 + sd), WTOP + 50 * s + ln * k / 6) for k in range(7)]
        b += PR._p(S.smooth_path(pts, closed=False), sw=3 * s, stroke="#5f7a3a")
        for k in range(1, 7):
            lx, ly = pts[k]
            b += PR._fig_leaf(lx + (14 if k % 2 else -14), ly, (17 - k) * s, r2.uniform(-40, 40) + (25 if k % 2 else -25),
                              "#6f9a48" if k % 2 else "#86b05a")
            if k == 4 and sd % 2:
                b += PR._g(PR._meal_food("grapes"), f"translate({f1(lx)},{f1(ly + 40)}) scale({f1(0.8 * s)})")
    for i in range(int(W3 / (60 * s)) + 1):
        vx = -10 + i * 60 * s + rng.uniform(-10, 10) * s
        vy = WTOP + 50 * s + rng.uniform(-10, 30) * s
        b += PR._fig_leaf(vx, vy, 22 * s, rng.uniform(-30, 30), "#6f9a48" if i % 2 else "#86b05a")
        if i % 5 == 2:
            b += PR._g(PR._meal_food("grapes"), f"translate({f1(vx)},{f1(vy + 52 * s)}) scale({f1(0.9 * s)})")
    # the floor: packed earth with a band of terracotta tiles along the wall
    fg = f"ls3fl{time}"
    floor = ("#d6ac78", "#bf8f5c") if time == "day" else ("#c99868", "#a8784c")
    b += (f'<defs>{S.lin_grad(fg, [(0, floor[0]), (1, floor[1])])}</defs>'
          f'<rect x="-20" y="{f1(wy)}" width="{W3 + 40}" height="{f1(H3 - wy + 30)}" fill="url(#{fg})"/>')
    b += PR._line(-20, wy, W3 + 20, wy, sw=4 * s)
    for i in range(int(W3 / (90 * s)) + 2):
        tx = -20 + i * 90 * s
        b += PR._p(f"M{f1(tx)},{f1(wy)} L{f1(tx + 90 * s)},{f1(wy)} L{f1(tx + 96 * s)},{f1(wy + 40 * s)} "
                   f"L{f1(tx + 4 * s)},{f1(wy + 40 * s)} Z", S.mix(PR.TERRA, "#d98a5a", 0.4 * (i % 2)), 2.4 * s)
    for i in range(int(W3 / (40 * s))):
        px, py = rng.uniform(-20, W3 + 20), rng.uniform(wy + 60 * s, H3 + 10)
        b += PR._ell(px, py, rng.uniform(4, 9) * s, rng.uniform(2, 4) * s, "#b08050", 0, extra='opacity="0.5"')
    # jars by the gate and under the far window, a basket by the fig tree
    for jx, jk, col in ((GX + GW + 92, 1.25, "#c98a5a"), (GX + GW + 150, 0.95, "#b8603e"), (2850, 1.2, "#c98a5a")):
        b += PR._g(PR._water_jar(col), f"translate({f1(jx)},{f1(wy + 8 * s)}) scale({f1(jk * s)})")
    for px_, col in ((2925, "#c8693e"), (3110, "#b5553a")):
        b += PR._p(f"M{f1(px_ - 30)},{f1(wy - 40)} L{f1(px_ + 30)},{f1(wy - 40)} L{f1(px_ + 22)},{f1(wy + 10)} "
                   f"L{f1(px_ - 22)},{f1(wy + 10)} Z", col, 3.4)
        for k in range(7):
            a = -150 + k * 20
            ex, ey = px_ + 46 * math.cos(math.radians(a)), wy - 40 + 54 * math.sin(math.radians(a))
            b += PR._p(f"M{f1(px_)},{f1(wy - 40)} Q{f1((px_ + ex) / 2)},{f1(ey - 10)} {f1(ex)},{f1(ey)}", sw=4,
                       stroke="#5f8a3a")
            b += PR._circ(ex, ey, 6, ("#f2c14e", "#e8705a", "#fbf3e0")[k % 3], 2)
    return f'<g filter="url(#wobble)">{b}</g>'


def cushions_body():
    b = ""
    for i, (who, x) in enumerate(SEATS.items()):
        b += PR.floor_cushion(x, SY, K, variant=(i * 3 + 1) % 4)
    return b


def wall_svg(time="day"):
    return doc3(wall_body(time) + cushions_body())


def outside_svg(time="day"):
    """The sunny street seen through the gate: sky, the houses across the street, a tree, the dusty road."""
    x0, x1 = GX - GW - 30, GX + GW + 30
    sky = ("#d9ebe6", "#f7ead0") if time == "day" else ("#e7a37c", "#f6d3a0")
    defs = S.lin_grad(f"ls3osky{time}", [(0, sky[0]), (1, sky[1])], 0, 0, 0, 1)
    b = f'<rect x="{f1(x0)}" y="{f1(G_SPRING - G_RISE - 10)}" width="{f1(x1 - x0)}" height="{f1(WY - G_SPRING + G_RISE + 20)}" fill="url(#ls3osky{time})"/>'
    tint = (lambda c: c) if time == "day" else (lambda c: S.mix(c, "#e09a70", 0.25))
    # a round tree behind the houses and a far hill line
    b += PR._p(S.hill(x0 - 40, x1 + 40, STREET_Y - 150, 40, seed=5, bottom=STREET_Y), tint("#c9d6a0"), 3)
    b += PR._p(f"M{f1(GX + 120)},{f1(STREET_Y - 150)} L{f1(GX + 124)},{f1(STREET_Y - 250)}", sw=10, stroke=INK)
    b += PR._p(f"M{f1(GX + 120)},{f1(STREET_Y - 150)} L{f1(GX + 124)},{f1(STREET_Y - 250)}", sw=5, stroke="#8f7a66")
    puffs = [(GX + 124, STREET_Y - 300, 64), (GX + 70, STREET_Y - 280, 46), (GX + 176, STREET_Y - 278, 48),
             (GX + 110, STREET_Y - 352, 44)]
    b += "".join(PR._circ(x_, y_, r_, tint("#86b05a"), 7) for x_, y_, r_ in puffs)
    b += "".join(PR._circ(x_, y_, r_, tint("#86b05a"), 0) for x_, y_, r_ in puffs)
    b += PR._circ(GX + 96, STREET_Y - 330, 22, tint("#a6cc72"), 0)
    # the houses across the street
    houses = ((x0 - 20, 150, 230, "#f1dfbd"), (x0 + 120, 210, 300, "#e9cfa2"), (x0 + 320, 160, 250, "#f4e6cc"),
              (x0 + 470, 140, 280, "#ecd6ae"))
    for hx, hw, hh, col in houses:
        top = STREET_Y - hh
        b += PR._rect(hx, top, hw, hh + 6, tint(col), 3.4)
        b += PR._rect(hx - 6, top - 10, hw + 12, 14, tint(S.shade(col, -0.18)), 3)
        for k in range(int(hw / 40)):
            b += PR._circ(hx + 18 + 40 * k, top + 4, 4.5, "#8a5a36", 1.8)
    b += PR._p(_arch_d(x0 + 168, x0 + 232, STREET_Y + 2, STREET_Y - 92, 26), "#6b4a38", 3)        # a door
    b += PR._rect(x0 + 360, STREET_Y - 180, 40, 46, "#6b4a38", 3, rx=6)                            # windows
    b += PR._rect(x0 + 40, STREET_Y - 170, 36, 40, "#6b4a38", 3, rx=6)
    # a striped stall awning with fruit baskets
    ax = x0 + 330
    for k in range(4):
        col = ("#c8693e", "#f3e3c2")[k % 2]
        b += PR._p(f"M{f1(ax + k * 36)},{f1(STREET_Y - 120)} L{f1(ax + k * 36 + 36)},{f1(STREET_Y - 120)} "
                   f"L{f1(ax + k * 40 + 46)},{f1(STREET_Y - 82)} L{f1(ax + k * 40 + 6)},{f1(STREET_Y - 82)} Z",
                   tint(col), 2.6)
    b += PR._g(PR._meal_food("grapes") + PR._g(PR._meal_food("figs"), "translate(46,4)"),
               f"translate({f1(ax + 52)},{f1(STREET_Y - 26)}) scale(0.9)")
    b += PR._rect(ax + 10, STREET_Y - 30, 120, 32, tint("#b98a5a"), 3, rx=4)
    # the dusty street
    b += PR._rect(x0, STREET_Y, x1 - x0, WY - STREET_Y + 10, tint("#ead2a2"), 0)
    b += PR._line(x0, STREET_Y, x1, STREET_Y, sw=3)
    rng = random.Random(4)
    for _ in range(14):
        b += PR._ell(rng.uniform(x0, x1), rng.uniform(STREET_Y + 14, WY), rng.uniform(4, 8), 2.5, "#c9a878", 0,
                     extra='opacity="0.6"')
    clip = f'<clipPath id="ls3gc"><path d="{GATE_D}"/></clipPath>'
    return doc3(f'{clip}<g clip-path="url(#ls3gc)" filter="url(#wobble)">{b}</g>', defs)


def gate_frame_body(time="day"):
    """The stone frame of the gate (jambs, arch with keystone, threshold) and the open plank door leaf on the left."""
    st = "#dcc39a" if time == "day" else "#cfa983"
    std = S.shade(st, -0.18)
    x0, x1 = GX - GW, GX + GW
    b = ""
    # door leaf swung back against the wall
    lx1 = x0 - G_FRAME - 6
    lx0 = lx1 - 200
    wood = "#8a5a36"
    b += PR._p(_arch_d(lx0, lx1, WY + 4, G_SPRING + 40, 90), wood, 4)
    for k in range(1, 5):
        xx = lx0 + k * 40
        b += PR._line(xx, WY, xx, G_SPRING + 40 - 70 * math.sin(math.pi * k / 5), sw=2.4, color=S.shade(wood, -0.3))
    for yy in (WY - 90, G_SPRING + 70):
        b += PR._rect(lx0 + 8, yy, 184, 16, "#5a4a42", 2.6, rx=4)
        for k in range(5):
            b += PR._circ(lx0 + 22 + k * 38, yy + 8, 3.4, "#cdb48a", 1.4)
    # jambs
    for jx in (x0 - G_FRAME, x1):
        b += PR._rect(jx, G_SPRING, G_FRAME, WY - G_SPRING + 4, st, 4)
        for k in range(1, 5):
            yy = G_SPRING + k * (WY - G_SPRING) / 5
            b += PR._line(jx, yy, jx + G_FRAME, yy, sw=2.4, color=std)
    # the arch ring with voussoirs and a keystone
    rx, ry = GW, G_RISE
    ring = (f"M{f1(x0 - G_FRAME)},{f1(G_SPRING)} A{f1(rx + G_FRAME)},{f1(ry + G_FRAME)} 0 0 1 {f1(x1 + G_FRAME)},"
            f"{f1(G_SPRING)} L{f1(x1)},{f1(G_SPRING)} A{f1(rx)},{f1(ry)} 0 0 0 {f1(x0)},{f1(G_SPRING)} Z")
    b += PR._p(ring, st, 4)
    for k in range(1, 9):
        a = math.pi * k / 9
        ix, iy = GX - rx * math.cos(a), G_SPRING - ry * math.sin(a)
        ox, oy = GX - (rx + G_FRAME) * math.cos(a), G_SPRING - (ry + G_FRAME) * math.sin(a)
        b += PR._line(ix, iy, ox, oy, sw=2.4, color=std)
    b += PR._p(f"M{f1(GX - 18)},{f1(G_SPRING - ry + 4)} L{f1(GX + 18)},{f1(G_SPRING - ry + 4)} "
               f"L{f1(GX + 26)},{f1(G_SPRING - ry - G_FRAME - 8)} L{f1(GX - 26)},{f1(G_SPRING - ry - G_FRAME - 8)} Z",
               S.shade(st, 0.15), 3.4)
    # threshold slab and a soft shadow inside the opening
    b += PR._rect(x0 - G_FRAME - 6, WY - 6, 2 * (GW + G_FRAME) + 12, 20, std, 3.4, rx=4)
    return b


def gate_overlay_svg(time="day"):
    """The wall round the gate drawn again ABOVE the street people (the opening cut out), so the townsfolk and the
    people walking along the street pass behind the jambs; then the stone frame and the door leaf."""
    region = (f"M-40,{f1(WTOP - 40)} L{f1(G_RIGHT)},{f1(WTOP - 40)} L{f1(G_RIGHT)},{f1(WY + 3)} L-40,{f1(WY + 3)} Z "
              + GATE_D)
    clip = f'<clipPath id="ls3gw"><path d="{region}" clip-rule="evenodd"/></clipPath>'
    return doc3(f'{clip}<g clip-path="url(#ls3gw)">{wall_body(time)}</g>'
                + S.g(gate_frame_body(time), filter="wobble"))


def tree_svg(sway, time="day"):
    return doc3(PR.fig_tree(TREE[0], TREE[1], 1.12 * K, sway=sway))


def table_svg():
    return doc3(PR.low_table(TABLE_X, TY, K, width=TABLE_W) + table_shadow())


def table_shadow():
    return (f'<ellipse cx="{TABLE_X}" cy="{f1(TY + 8)}" rx="{f1(TABLE_W * 0.52)}" ry="18" fill="{INK}" opacity="0.16" '
            f'filter="url(#blur-md)"/>')


def front_svg(time="day"):
    """Fig leaves at the near corners, a big jar and a bread basket on the floor at the right."""
    b = ""
    for cx_, sg in ((0, 1), (W3, -1)):
        for j in range(6):
            b += PR._fig_leaf(cx_ + sg * (20 + 52 * j) * K, H3 + 30 - (60 + 46 * (j % 3)) * K, 50 * K,
                              -30 * sg + 15 * j, PR.FIG_LEAF if j % 2 else "#7ab05a")
    b += PR._g(PR._water_jar("#b8603e"), f"translate({f1(W3 - 150)},{f1(H3 + 20)}) scale({f1(2.0 * K)})")
    b += PR.bread_basket(TABLE_X + TABLE_W / 2 + 110, TY + 46, 0.75 * K)
    return doc3(f'<g filter="url(#wobble)">{b}</g>')


def cat_svg(tail):
    """A ginger cat asleep on the warm floor by the gate; tail 0 / 1 flicks."""
    x, y = 650, 1078
    fur, dark = "#e2954e", "#b86a30"
    b = PR._ell(x, y + 6, 70, 12, INK, 0, extra='opacity="0.15"')
    tip = (x - 80, y - 30) if tail else (x - 92, y - 8)
    b += PR._tube(f"M{x - 40},{y} Q{x - 86},{y + 4} {f1(tip[0])},{f1(tip[1])}", 14, fur, 3)
    b += PR._p(S.blob(x, y - 18, 60, 30, 0.04, 10, seed=2), fur, 3.4)
    for k in range(3):
        b += PR._p(f"M{x - 20 + 18 * k},{y - 44} q6,12 0,22", sw=4, stroke=dark)
    hx, hy = x + 44, y - 30
    b += PR._p(f"M{hx - 22},{hy - 8} L{hx - 18},{hy - 34} L{hx - 4},{hy - 18} Z M{hx + 6},{hy - 18} L{hx + 22},{hy - 34} "
               f"L{hx + 24},{hy - 6} Z", fur, 3)
    b += PR._circ(hx, hy, 24, fur, 3.4)
    b += PR._p(f"M{hx - 13},{hy - 2} q5,4 10,0 M{hx + 4},{hy - 2} q5,4 10,0", sw=2.6)
    b += PR._ell(hx - 1, hy + 7, 3, 2, "#c9706a", 0) + PR._ell(hx - 14, hy + 8, 5, 3, "#f0a090", 0, extra='opacity="0.6"')
    b += PR._ell(hx + 12, hy + 8, 5, 3, "#f0a090", 0, extra='opacity="0.6"')
    return doc3(f'<g filter="url(#wobble-fine)">{b}</g>')


def sparrow_svg(x, y, facing, pose):
    """A little brown sparrow on the wall coping: pose 'perch' / 'peck' (head down) / 'hop'."""
    if pose == "peck":
        return doc3(PR._place(PR._songbird(0.0, "perch", "brown"), x, y, 0.42, facing, rot=24 * facing))
    return doc3(PR.songbird(x, y - (14 if pose == "hop" else 0), 0.42, facing, pose="perch", color="brown"))


def flyer_svg(wing):
    return doc3(PR.songbird(80, 80, 0.36, 1, wing=wing, pose="fly", color="brown"))


# ------------------------------------------------------------------ light
def sunlight_svg(time="day"):
    """A warm light wash from the upper right (screen layer)."""
    if time == "day":
        defs = S.rad_grad("ls3sun", [(0, "#fff0c8", 0.55), (0.5, "#ffe2a8", 0.18), (1, "#ffe2a8", 0)])
        b = f'<ellipse cx="2200" cy="200" rx="1900" ry="900" fill="url(#ls3sun)"/>'
        b += S.path(S.rays(2900, -300, 300, 2200, n=7, width_deg=3.2, rot=104), fill="#fff3d0", stroke=False,
                    extra='opacity="0.10" filter="url(#blur-md)"')
    else:
        defs = S.rad_grad("ls3sun", [(0, "#ffd9a0", 0.55), (0.5, "#f6b878", 0.2), (1, "#f6b878", 0)])
        b = f'<ellipse cx="2600" cy="120" rx="2000" ry="800" fill="url(#ls3sun)"/>'
    return doc3(b, defs)


# ------------------------------------------------------------------ the cast
def guest_fn(who):
    if who.startswith("tax"):
        v = int(who[3])
        return lambda x, y, s, f, **kw: C.tax_collector(x, y, s, f, variant=v, **kw)
    kind = {"woman": "woman", "young": "young_man", "labourer": "labourer"}[who]
    return lambda x, y, s, f, **kw: C.sinner(x, y, s, f, kind=kind, variant=0, **kw)


def town_fn(who):
    kind, var = {"elder": ("elder", 2), "man": ("man", 4), "woman": ("woman", 3)}[who]
    return lambda x, y, s, f, **kw: C.neighbour(x, y, s, f, kind=kind, variant=var, **kw)


def ph_fn(v):
    return lambda x, y, s, f, **kw: C.pharisee(x, y, s, f, variant=v, **kw)


def jesus_fn(x, y, s, f, **kw):
    return C.jesus(x, y, s, f, **kw)


TOWN_FILTER = ('<filter id="ls3town" x="-20%" y="-20%" width="140%" height="140%">'
               '<feColorMatrix type="saturate" values="0.42"/>'
               '<feComponentTransfer><feFuncR type="linear" slope="0.80" intercept="0.17"/>'
               '<feFuncG type="linear" slope="0.78" intercept="0.13"/>'
               '<feFuncB type="linear" slope="0.72" intercept="0.08"/></feComponentTransfer></filter>')


class Actor:
    """A figure on its own flipbook layer. A state is (pose, expr, facing, phase, ox, oy[, extra]) drawn at base +
    (ox, oy); fn(x, y, scale, facing, pose=, expr=, phase=, **extra) draws it. Hard cuts hide in squash dips
    (Nativity Fig), blinks are added automatically for blinkable expressions, breathing runs on the global clock.
    ``path`` (t -> (dx, dy, k)) moves / scales the figure about its current anchor (walks)."""

    def __init__(self, name, fn, base, z, g0, piv=None, scale=K, seed=0, shadow=None, wrap=None, kw=None, oy0=0.0):
        self.name, self.fn, self.base, self.s, self.g0 = name, fn, base, scale, g0
        self.oy0 = oy0                  # added to every state's oy (s04 / s11 reuse s03's drawing positions)
        self.piv = piv or base
        self.shadow = shadow            # width of a ground shadow under standing states (None = none)
        self.wrap = wrap                # (prefix, suffix, defs) round the markup (the townsfolk tint)
        self.kw = kw or {}
        self.fig = Fig(name, self.draw, self.piv, scale, z, g0, seed=seed, docf=self.doc)
        self.path = None
        self.extra = []
        self.alpha = None
        self.breathe = True
        self.bphase = random.Random(name).uniform(0, 1)

    def doc(self, body):
        if self.wrap:
            pre, suf, defs = self.wrap
            return doc3(pre + body + suf, defs)
        return doc3(body)

    def draw(self, st):
        pose, expr, f, ph, ox, oy = st[:6]
        extra = dict(st[6]) if len(st) > 6 and st[6] else {}
        x, y = self.base[0] + ox, self.base[1] + oy + self.oy0
        out = ""
        if self.shadow and not pose.startswith("sit") and pose not in C.GUEST_POSES[5:12]:
            out += C.ground_shadow(x, y, self.s, self.shadow, 0.2)
        return out + self.fn(x, y, self.s, f, pose=pose, expr=expr, phase=ph, **self.kw, **extra)

    def cut(self, t, st, dip=True, depth=7.0):
        self.fig.cut(t, st, dip=dip, depth=depth)
        return self

    def blinks(self, t_from, t_to, rng, every=(2.3, 4.3)):
        pairs = {}
        for _, st in self.fig.ents:
            e = st[1]
            if e in BLINKABLE:
                pairs[st] = (st[0], bexpr(e)) + tuple(st[2:])
        self.fig.add_blinks(pairs, t_from, t_to, rng, every)
        return self

    def build(self, sc, wc=1.0):
        mots = []
        if self.breathe:
            mots.append(breath(self.piv, self.g0, phase=self.bphase))
        if self.path is not None:
            path, base, piv = self.path, self.base, self.piv

            def pm(t):
                dx, dy, k = path(t)
                return Tf(dx=dx + (1 - k) * (base[0] - piv[0]), dy=dy + (1 - k) * (base[1] - piv[1]), sx=k, sy=k)
            mots.append(pm)
        if self.alpha is not None:
            al = self.alpha
            mots.append(lambda t: Tf(alpha=al(t)))
        mots += self.extra
        self.fig.mots = list(mots)
        self.fig.build(sc, wc)
        return self


def walk_plan(t0, pts, stride, period=0.27, move=0.15, lift=5.0, kfn=None):
    """Planted-foot walk along the polyline pts [(x, y), ...] from pts[0]: equal strides of about ``stride`` px; the
    anchor advances one stride across each cut (walk_a / walk_b alternate). kfn(y) = perspective scale.
    Returns (cuts [(t, 'walk_a'|'walk_b', facing)], path(t) -> (dx, dy, k), t_end)."""
    seg = [(pts[i], pts[i + 1], math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    L = sum(s_[2] for s_ in seg)
    kf = kfn or (lambda y: 1.0)
    n = max(1, round(L / (stride * kf((pts[0][1] + pts[-1][1]) / 2))))

    def at_len(d):
        for a, b, l in seg:
            if d <= l or (a, b, l) == seg[-1]:
                u = 0 if l == 0 else min(1.0, d / l)
                return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            d -= l
        return pts[-1]
    nodes = [at_len(L * i / n) for i in range(n + 1)]
    cut_t = [snap(t0 + i * period) for i in range(n)]
    cuts = []
    f = 1
    for i in range(n):
        ddx = nodes[i + 1][0] - nodes[i][0]
        if abs(ddx) > 2:
            f = 1 if ddx > 0 else -1
        cuts.append((cut_t[i], "walk_a" if i % 2 == 0 else "walk_b", f))
    t_end = snap(t0 + n * period)
    x0, y0 = pts[0]

    def path(t):
        x, y = nodes[0]
        bob = 0.0
        for i, tk in enumerate(cut_t):
            u = M.progress(t, tk - move * 0.45, tk + move * 0.55, "sine")
            x += (nodes[i + 1][0] - nodes[i][0]) * u
            y += (nodes[i + 1][1] - nodes[i][1]) * u
            if tk - move * 0.45 <= t <= tk + move * 0.55:
                bob -= lift * math.sin(math.pi * (t - tk + move * 0.45) / move)
        return x - x0, y - y0 + bob, kf(y)
    return cuts, path, t_end


def chain(p1, off1, t_sw, p2, off2):
    """Two walk paths as one (offsets relative to the actor's base): p1 (+ off1) until t_sw, then p2 (+ off2)."""
    def path(t):
        p, o = (p1, off1) if t < t_sw else (p2, off2)
        dx, dy, k = p(t)
        return dx + o[0], dy + o[1], k
    return path


# ------------------------------------------------------------------ shared scene pieces
def add_set(sc, g0, time="day", tree=True, outside=True):
    """Sky, clouds, the wall and floor, the street through the gate (the overlay goes in with add_gate_overlay)."""
    sc.add("sky", sky_svg(time), z=0, wc=0.6)
    w = W3 + 1400
    sc.add("clouds", clouds_svg(time), z=1, wc=0.7,
           motion=lambda t: Tf(dx=((t + g0) * 9.0) % 1000 - 500))
    sc.add("wall", wall_svg(time), z=2)
    if outside:
        sc.add("outside", outside_svg(time), z=3, wc=0.8)
    if tree:
        frames = [tree_svg(sw, time) for sw in (-1.0, 0.0, 1.0)]
        sc.add("figtree", frames, z=30, frame_at=lambda t: 1 + math.sin(2 * math.pi * (t + g0) / 5.2) * 0.98)
    sc.add("table", table_svg(), z=60)
    sc.add("dapple", [dapple_svg(0, time), dapple_svg(1, time)], z=12.2, blend="multiply", wc=0,
           frame_at=lambda t: 0.5 + 0.5 * math.sin(2 * math.pi * (t + g0) / 4.4))


def dapple_svg(k, time="day"):
    """Soft leaf shadows from the vine on the pergola, dappling the top of the wall (multiply layer)."""
    rng = random.Random(77)
    col = "#b98a64" if time == "day" else "#a8745a"
    b = ""
    for _ in range(70):
        x = rng.uniform(G_RIGHT + 40, W3 + 40)
        y = rng.uniform(WTOP + 70, WTOP + 290) ** 1.0
        rx, ry = rng.uniform(22, 58), rng.uniform(12, 26)
        dx, dy = (7 * k, 3 * k) if rng.random() < 0.6 else (-5 * k, 2 * k)
        b += (f'<ellipse cx="{f1(x + dx)}" cy="{f1(y + dy)}" rx="{f1(rx)}" ry="{f1(ry)}" '
              f'transform="rotate({rng.uniform(-40, 40):.0f} {f1(x + dx)} {f1(y + dy)})" fill="{col}" '
              f'opacity="{rng.uniform(0.25, 0.5) * (1 - (y - WTOP - 70) / 330):.2f}"/>')
    return doc3(f'<g filter="url(#soft)">{b}</g>')


def add_gate_overlay(sc, time="day"):
    sc.add("gate", gate_overlay_svg(time), z=12, wc_edge=0.0)


def add_front(sc, g0, time="day"):
    sc.add("front", front_svg(time), z=90)
    sc.add("cat", [cat_svg(0), cat_svg(1)], z=89,
           frame_at=lambda t: 1.0 if (math.sin(2 * math.pi * (t + g0) / 4.6) > 0.55) else 0.0)


def add_sparrows(sc, g0, seed=7):
    """Three sparrows on the wall coping and two pecking crumbs by the bread basket: peck and hop now and then."""
    rng = random.Random(seed)
    for i, (x, f, y) in enumerate(((1130, 1, WTOP - 26 * K), (1205, -1, WTOP - 26 * K), (2290, 1, WTOP - 26 * K),
                                   (2720, -1, TY + 44), (2790, 1, TY + 58))):
        frames = [sparrow_svg(x, y, f, p) for p in ("perch", "peck", "hop")]
        per = rng.uniform(2.6, 3.6)
        ph = rng.uniform(0, 1)

        def fa(t, per=per, ph=ph):
            u = ((t + g0) / per + ph) % 1.0
            return 1.0 if u < 0.18 else (2.0 if 0.5 < u < 0.56 else 0.0)
        sc.add(f"sparrow{i}", frames, z=8, frame_at=fa, wc=0.6)


def add_flyers(sc, g0, n=2, seed=9):
    """Little birds flitting across the sky strip on the global clock (4-frame wing flap)."""
    frames = [flyer_svg(w) for w in (0.0, 0.33, 0.66, 1.0)]
    rng = random.Random(seed)
    for i in range(n):
        per = rng.uniform(13, 18)
        ph = rng.uniform(0, 1)
        y0 = rng.uniform(60, 120)

        def mot(t, per=per, ph=ph, y0=y0):
            u = ((t + g0) / per + ph) % 1.0
            x = -200 + u * (W3 + 400)
            return Tf(dx=x - 80, dy=y0 - 80 + 18 * math.sin(u * 12))
        sc.add(f"flyer{i}", frames, z=1.5, motion=mot, wc=0.5,
               frame_at=lambda t, ph=ph: float(int((t + g0 + ph) * 14) % 4))


def coin_stack_svg(n, pouch=0.0):
    """The coins counted out on the table in a wobbly stack of n, and the leather money bag (pouch 0..1 bulges)."""
    x, y = COINS
    b = ""
    for i in range(n):
        b += PR._coin(x + 3 * math.sin(i * 1.7), y - i * 8, 13, 0.62)
    k = 1 + 0.22 * pouch
    b += PR._g(PR._coin_pouch(open_=True), f"translate({f1(POUCH[0])},{f1(POUCH[1])}) scale({0.62 * k:.3f},{0.62 * (1 + 0.12 * pouch):.3f})")
    return doc3(f'<g filter="url(#wobble-fine)">{b}</g>')


def scroll_markup(x, y, rot=-70, opened=False, k=0.42):
    return PR.scroll(x, y, k * K, rot=rot, opened=opened)


def puff_svg(x, y, f):
    """A little 'hmph' puff from the nose."""
    b = ""
    for i, (dx, dy, r) in enumerate(((18, 4, 9), (34, -2, 12), (54, -10, 15))):
        b += PR._circ(x + f * dx, y + dy, r, "#f7efdc", 2.4, stroke=P["ink_soft"])
    return doc3(f'<g filter="url(#wobble-fine)">{b}</g>')


# the closing tableau of s03 = the opening of s04 (states drawn at the seat / standing anchor)
END3 = {
    "jesus": ("sit_eat", "smile", 1, 1.0, 0, 0),
    "tax0": ("smile", "happy", -1, 0, 0, 0),
    "tax1": ("smile", "happy", 1, 0, 0, 0),
    "tax2": ("smile", "happy", 1, 0, 0, 0),
    "labourer": ("smile", "happy", 1, 0, 0, 0),
    "woman": ("smile", "happy", 1, 0, 0, 0),
    "young": ("sit_eat", "happy", 1, 0, 0, 0, (("item", "cup"),)),
    "ph0": ("arms_folded", "disdain", -1, 0, 0, 0),
    "ph2": ("arms_folded", "disdain", -1, 0, 0, 0),
    "ph1": ("stand_frown", "disdain", -1, 0, 0, 0),
}


# where s03 draws the guests who walk in (their layer base) and the offset their walk leaves them at: s04 / s11 draw
# the seated figures from the same base, so the rasters (and the plain dissolve s03 -> s04) are identical
SINNER_STOP = {"woman": 845, "young": 725, "labourer": 600}
BASES = {"tax1": ((575, BACK_Y), (SEATS["tax1"] - 575, 0.0)), "tax2": ((445, BACK_Y - 6), (SEATS["tax2"] - 445, 6.0))}
BASES.update({w: ((x, BACK_Y), (SEATS[w] - x, 0.0)) for w, x in SINNER_STOP.items()})


def add_air(sc, g0, time="day", t0=-1e9, t1=1e9):
    """Warm motes drifting in the light, on the film's global clock (so a plain dissolve has no ghosting); t0 / t1
    (scene time) fade them in / out over 0.8 s."""
    col = (255, 240, 200) if time == "day" else (255, 214, 160)
    fx = FX.motes((1100, 200, 3100, 900), count=26, color=col, size=(2, 5), alpha=110, seed=33, t0=g0 + t0,
                  t1=g0 + t1)
    sc.fx.append(lambda frame, t, view: fx(frame, t + g0, view))


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=W3, H=H3)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    at = tm.at
    rng = random.Random(30)

    t_youtian = at(0, "有一天")
    t_hao = at(0, "好多人")
    t_lai = at(0, "来听")
    t_jiang = at(0, "讲道")
    t_l1 = at(1, "来的人里")
    t_shui = at(1, "收税")
    t_cc1, t_cc2 = at(1, "常常"), at(1, "常常", 1)
    t_duo, t_shou = at(1, "多收"), at(1, "多收", 1)
    t_bie, t_qian = at(1, "别人"), at(1, "的钱", 1)
    t_l2 = at(2, "还有一些人")
    t_cuo = at(2, "做过")
    t_dajia = at(2, "大家")
    t_bu = at(2, "不喜欢")
    t_keshi = at(3, "可是")
    t_huan = at(3, "很欢迎", 1)
    t_ying = at(3, "很欢迎", 2)
    t_hai = at(3, "还和")
    t_yiqi = at(3, "一起吃")
    t_chi = at(3, "吃饭")
    t_fan = at(3, "吃饭", 1)
    t_l4 = at(4, "旁边")
    t_fa = at(4, "法利赛人")
    t_shou4 = at(4, "很守", 1)
    t_gui = at(4, "规矩")
    t_kan = at(4, "看不起")
    t_zhou = at(4, "皱着")
    t_xiao = at(4, "小声说")
    t_heng = at(5, "哼")
    t_zhe = at(5, "这个人")
    t_p_end = ctx.lines[5].end
    t_fin = min(t_p_end - 0.02, T - 1.45)          # the closing tableau starts here (its dips end before T - 1)
    t_hold = t_fin + 0.4

    add_set(sc, g0, "day")
    add_gate_overlay(sc)
    add_front(sc, g0)
    add_sparrows(sc, g0)
    add_flyers(sc, g0)
    sc.add("sun", sunlight_svg("day"), z=95, blend="screen", wc=0)

    actors = []

    # ---------------------------------------------------------------- the townsfolk across the street
    twrap = ('<g filter="url(#ls3town)">', "</g>", TOWN_FILTER)
    town = {}
    for i, (who, (x, y)) in enumerate(TOWN.items()):
        a = Actor(f"town_{who}", town_fn(who), (x, y), 5 + i * 0.1, g0, scale=K * TK, seed=200 + i, shadow=90,
                  wrap=twrap)
        town[who] = a
        actors.append(a)
    town["elder"].cut(0, ("stand", "neutral", 1, 0, 0, 0))
    town["man"].cut(0, ("stand", "happy", -1, 0, 0, 0))
    town["woman"].cut(0, ("laugh", "happy", 1, 0, 0, 0))
    town["woman"].cut(3.0, ("stand", "happy", 1, 0, 0, 0))
    town["man"].cut(6.2, ("laugh", "happy", -1, 0, 0, 0))
    town["man"].cut(8.0, ("stand", "neutral", -1, 0, 0, 0))
    # they notice the newcomers in the street, then turn away from them
    town["elder"].cut(t_cuo - 0.3, ("stand", "stern", 1, 0, 0, 0))
    town["woman"].cut(t_cuo + 0.4, ("stand", "stern", 1, 0, 0, 0))
    town["man"].cut(t_cuo + 0.2, ("stand", "stern", 1, 0, 0, 0))
    town["woman"].cut(t_dajia, ("stand", "disdain", -1, 0, 0, 0))
    town["elder"].cut(t_dajia + 0.25, ("stand", "disdain", -1, 0, 0, 0))
    town["man"].cut(t_bu, ("point", "mutter", 1, 0, 0, 0))
    town["man"].cut(t_bu + 1.6, ("stand", "disdain", -1, 0, 0, 0))
    town["man"].cut(t_l4 + 1.0, ("stand", "neutral", -1, 0, 0, 0))
    town["woman"].cut(t_l4 + 1.4, ("stand", "neutral", 1, 0, 0, 0))
    puff_at = [(t_dajia + 0.05, TOWN["woman"], -1), (t_dajia + 0.3, TOWN["elder"], -1)]

    # ---------------------------------------------------------------- Jesus
    jx = SEATS["jesus"]
    jes = Actor("jesus", jesus_fn, (jx, SEAT_Y), 50, g0, seed=101)
    sto = STAND_Y - SEAT_Y
    jes.cut(0, ("look_kind", "kind", -1, 0, 0, sto))
    jes.cut(t_hao - 0.1, ("welcome", "smile", -1, 0, 0, sto))
    jes.cut(t_jiang + 0.25, ("sit_tell", "smile", -1, 0, 0, 0), depth=10)
    jes.cut(t_l1 + 1.2, ("sit_look_kind", "warm", -1, 0, 0, 0))
    jes.cut(t_cc1, ("sit_tell", "smile", -1, 0, 0, 0))
    jes.cut(t_l2 + 0.6, ("sit_look_kind", "warm", -1, 0, 0, 0))
    # he gets up and welcomes the people nobody liked
    jes.cut(t_keshi + 0.15, ("look_kind", "kind", -1, 0, 0, sto), depth=10)
    jes.cut(t_huan - 0.12, ("welcome", "smile", -1, 0, 0, sto))
    jes.cut(t_hai + 0.1, ("sit_eat", "smile", -1, 0.0, 0, 0), depth=10)
    for i, ph in enumerate((0.25, 0.5, 0.75, 1.0)):
        jes.cut(t_yiqi + 0.1 + i * 0.1, ("sit_eat", "smile", -1, ph, 0, 0), dip=False)
    jes.cut(t_fan + 0.25, ("sit_laugh", "laugh", -1, 0, 0, 0))
    jes.cut(t_l4 + 1.5, ("sit_eat", "smile", 1, 1.0, 0, 0))
    jes.cut(t_shou4, ("sit_offer", "warm", 1, 0, 0, 0))
    jes.cut(t_zhou, ("sit_laugh", "laugh", 1, 0, 0, 0))
    jes.cut(t_heng - 0.6, ("sit_eat", "smile", 1, 1.0, 0, 0))
    jes.blinks(0.4, t_fin - 0.2, rng)
    actors.append(jes)

    # ---------------------------------------------------------------- the tax collectors
    tax0 = Actor("tax0", guest_fn("tax0"), (SEATS["tax0"], SEAT_Y), 52, g0, seed=111)
    tax0.cut(0, ("sit_count", "neutral", 1, 0, 0, 0))
    tax0.cut(t_hao + 0.3, ("smile", "happy", -1, 0, 0, 0))
    tax0.cut(t_jiang + 0.4, ("listen", "kind", -1, 0, 0, 0))
    tax0.cut(t_shui, ("sit_count", "sly", 1, 0, 0, 0))
    tax0.cut(t_duo, ("sit_count", "smug", 1, 0, 0, 0), depth=4)
    tax0.cut(t_bie + 0.1, ("sit_count", "sly", 1, 0, 0, 0), depth=4)
    tax0.cut(t_l2 + 1.0, ("listen", "kind", -1, 0, 0, 0))
    tax0.cut(t_fan, ("laugh", "laugh", -1, 0, 0, 0))
    tax0.cut(t_l4 + 1.8, ("sit_eat", "happy", -1, 0, 0, 0, (("item", "cup"),)))
    tax0.cut(t_shou4 + 0.3, ("warm", "touched", -1, 0, 0, 0))
    tax0.cut(t_zhou + 0.2, ("toast", "cheery", -1, 0, 0, 0))
    tax0.cut(t_heng - 0.4, ("smile", "happy", -1, 0, 0, 0))
    tax0.blinks(0.4, t_fin - 0.2, rng)
    actors.append(tax0)

    kfn = lambda y: 1.0
    for who, start, t_go, seat in (("tax1", (575, BACK_Y), 0.45, SEATS["tax1"]), ("tax2", (445, BACK_Y - 6), 0.75,
                                                                                 SEATS["tax2"])):
        a = Actor(who, guest_fn(who), start, 51 + (0.1 if who == "tax2" else 0.2), g0, piv=(seat, SEAT_Y),
                  seed=120 + int(who[3]), shadow=100)
        cuts, path, t_end = walk_plan(t_go, [start, (seat, BACK_Y)], 85 * K, period=0.27)
        a.cut(0, ("stand", "happy", 1, 0, 0, 0))
        for tc, pose, f in cuts:
            a.cut(tc, (pose, "happy", f, 0, 0, 0), dip=False)
        oy = SEAT_Y - BACK_Y
        a.cut(t_end + 0.08, ("sit", "happy", 1, 0, 0, oy), depth=12)
        a.path = path
        a.cut(max(t_end + 0.9, t_l1), ("listen", "kind", 1, 0, 0, oy))
        if who == "tax1":
            a.cut(t_shui + 0.15, ("smile", "happy", 1, 0, 0, oy))
            a.cut(t_cc2 + 0.4, ("listen", "kind", 1, 0, 0, oy))
            a.cut(t_fan + 0.1, ("laugh", "laugh", -1, 0, 0, oy))
            a.cut(t_l4 + 1.2, ("sit_eat", "happy", 1, 0, 0, oy, (("item", "cup"),)))
            a.cut(t_zhou - 0.2, ("toast", "cheery", 1, 0, 0, oy))
            a.cut(t_heng - 0.2, ("smile", "happy", 1, 0, 0, oy))
        else:
            a.cut(t_shui + 0.3, ("smile", "happy", 1, 0, 0, oy))
            a.cut(t_cc2 + 0.6, ("listen", "kind", 1, 0, 0, oy))
            a.cut(t_fan + 0.2, ("toast", "cheery", -1, 0, 0, oy))
            a.cut(t_l4 + 0.9, ("sit_eat", "happy", -1, 0, 0, oy, (("item", "bread"),)))
            a.cut(t_kan + 0.4, ("laugh", "laugh", -1, 0, 0, oy))
            a.cut(t_xiao, ("smile", "happy", 1, 0, 0, oy))
        a.blinks(0.4, t_fin - 0.2, rng)
        actors.append(a)
        sc.sfx("footsteps", t_go, dur=t_end - t_go + 0.1, gain_db=-24 if who == "tax2" else -22, pan=-0.3,
               fade_out=0.3)
        sc.sfx("cloth", t_end + 0.05, gain_db=-24)

    # ---------------------------------------------------------------- the people nobody liked
    ylo, yhi = OUT_Y, BACK_Y
    kfn = lambda y: 0.86 + 0.14 * min(1.0, max(0.0, (y - ylo) / (yhi - ylo)))
    sinners = {}
    for i, (who, delay) in enumerate((("woman", 0.0), ("young", 0.55), ("labourer", 1.05))):
        stop_x = SINNER_STOP[who]
        seat = SEATS[who]
        start = (GX - GW - 150 - 120 * i, OUT_Y)
        pts = [start, (GX - 40, OUT_Y), (GX + 70, WY + 34), (stop_x, BACK_Y)]
        t_go = t_l2 + 0.15 + delay
        cuts, path1, t_end1 = walk_plan(t_go, pts, 84 * K, period=0.3, kfn=kfn)
        # after Jesus' welcome: on to the cushion
        t_go2 = t_huan + 0.05 + 0.18 * i
        cuts2, path2, t_end2 = walk_plan(t_go2, [(stop_x, BACK_Y), (seat, BACK_Y)], 85 * K, period=0.26)
        base = (stop_x, BACK_Y)            # drawings sit here (inside the canvas); the path carries them
        path = chain(path1, (start[0] - base[0], start[1] - base[1]), t_go2 - 0.2, path2, (0.0, 0.0))
        # the switch from 'behind the gate wall' to 'in the courtyard': when fully inside the opening
        t_sw = t_go
        for k in range(400):
            tt = t_go + k * 0.02
            dx, dy, kk = path(tt)
            if base[0] + dx > GX - GW + 112 * kk * K:
                t_sw = snap(tt)
                break
        oy = SEAT_Y - BACK_Y
        sad = "sorry" if who != "labourer" else "sad"
        for layer in ("out", "in"):
            a = Actor(f"{who}_{layer}", guest_fn(who), base, (6 + 0.1 * i) if layer == "out" else 49 + 0.1 * (2 - i),
                      g0, piv=(seat, SEAT_Y), seed=140 + i, shadow=100)
            a.cut(0, ("walk_a", sad, 1, 0, 0, 0))
            for tc, pose, f in cuts:
                a.cut(tc, (pose, sad, f, 0, 0, 0), dip=False)
            a.path = path
            if layer == "out":
                a.alpha = lambda t, ts=t_sw: 1.0 if t < ts else 0.0
                a.breathe = False
                a.fig.ents = [e for e in a.fig.ents if e[0] <= t_sw + 0.4]
                actors.append(a)
                continue
            a.alpha = lambda t, ts=t_sw: 0.0 if t < ts else 1.0
            a.cut(t_end1 + 0.05, ("stand", sad, 1, 0, 0, 0), depth=5)
            if who == "woman":
                a.cut(t_bu + 0.25, ("stand", "teary", -1, 0, 0, 0), depth=5)
            a.cut(t_keshi + 0.55 + 0.15 * i, ("stand", "touched", 1, 0, 0, 0), depth=6)
            for tc, pose, f in cuts2:
                a.cut(tc, (pose, "happy", f, 0, 0, 0), dip=False)
            a.cut(t_end2 + 0.06, ("sit", "happy", 1, 0, 0, oy), depth=12)
            a.cut(max(t_end2 + 0.5, t_fan), ("laugh", "laugh", 1, 0, 0, oy))
            if who == "woman":
                a.cut(t_l4 + 1.1, ("sit_eat", "happy", 1, 0, 0, oy, (("item", "bread"),)))
                a.cut(t_kan, ("toast", "cheery", 1, 0, 0, oy))
                a.cut(t_xiao - 0.3, ("smile", "happy", 1, 0, 0, oy))
            elif who == "young":
                a.cut(t_l4 + 0.7, ("smile", "happy", -1, 0, 0, oy))
                a.cut(t_shou4 + 0.6, ("laugh", "laugh", -1, 0, 0, oy))
                a.cut(t_zhou + 0.5, ("sit_eat", "happy", 1, 0, 0, oy, (("item", "cup"),)))
            else:
                a.cut(t_l4 + 1.4, ("sit_eat", "happy", 1, 0, 0, oy, (("item", "cup"),)))
                a.cut(t_kan + 0.9, ("laugh", "laugh", 1, 0, 0, oy))
                a.cut(t_heng - 0.8, ("smile", "happy", 1, 0, 0, oy))
            a.blinks(0.4, t_fin - 0.2, rng)
            sinners[who] = a
            actors.append(a)
            sc.sfx("cloth", t_end2 + 0.05, gain_db=-25)
        sc.sfx("footsteps", t_go, dur=t_end1 - t_go, gain_db=-25, pan=-0.6, fade_out=0.3)
        sc.sfx("footsteps", t_go2, dur=t_end2 - t_go2, gain_db=-25, pan=-0.3, fade_out=0.2)

    # ---------------------------------------------------------------- the Pharisees by the fig tree
    phs = {}
    for v, (x, y) in PH.items():
        a = Actor(f"ph{v}", ph_fn(v), (x, y), 70 + (0.2 if v == 0 else (0.1 if v == 2 else 0.0)), g0, seed=160 + v,
                  shadow=110)
        phs[v] = a
        actors.append(a)
    phs[0].cut(0, ("stand", "ponder", -1, 0, 0, 0))
    phs[1].cut(0, ("stand_frown", "stern", -1, 0, 0, 0))
    phs[2].cut(0, ("arms_folded", "stern", -1, 0, 0, 0))
    # '很守上帝的规矩': the elder reads the scroll of the law (its own layer in his hands); the others nod
    phs[2].cut(t_shou4 + 0.15, ("stand", "stern", -1, 0, 0, 0))
    phs[1].cut(t_shou4 + 0.35, ("stand", "stern", -1, 0, 0, 0))
    # '看不起这些人'
    phs[0].cut(t_kan, ("stand_frown", "disdain", -1, 0, 0, 0))
    phs[1].cut(t_kan + 0.2, ("arms_folded", "disdain", -1, 0, 0, 0))
    phs[2].cut(t_kan + 0.35, ("stand_frown", "disdain", -1, 0, 0, 0))
    # '皱着眉头，小声说'
    phs[0].cut(t_zhou, ("stand_frown", "mutter", -1, 0, 0, 0))
    phs[2].cut(t_zhou + 0.15, ("arms_folded", "mutter", -1, 0, 0, 0))
    phs[1].cut(t_zhou + 0.3, ("arms_folded", "mutter", -1, 0, 0, 0))
    phs[0].cut(t_xiao - 0.05, ("whisper", "mutter", 1, 0, 0, 0))
    phs[2].cut(t_xiao + 0.1, ("whisper", "mutter", -1, 0, 0, 0))
    # P '哼！...'
    phs[0].cut(t_heng - 0.04, ("grumble", "disdain", -1, 0.0, 0, 0))
    gr_n = 6
    t = t_heng + 0.4
    i = 1
    while t < t_fin - 0.06:
        phs[0].cut(t, ("grumble", "disdain", -1, (i % gr_n) / gr_n, 0, 0), dip=False)
        t += 0.12
        i += 1
    phs[0].cut(t_fin, ("arms_folded", "disdain", -1, 0, 0, 0))
    phs[2].cut(t_heng + 0.2, ("arms_folded", "disdain", -1, 0, 0, 0))
    phs[1].cut(t_zhe + 0.4, ("stand_frown", "disdain", -1, 0, 0, 0))
    for a in phs.values():
        a.blinks(0.4, t_fin - 0.2, rng)
    # the scroll: in the elder's clasped hands while '很守上帝的规矩'
    hp0 = C.body_points(C.pharisee, PH[0][0], PH[0][1], K, -1, variant=0, pose="stand")["hands"]
    hx, hy = (hp0[0][0] + hp0[1][0]) / 2 - 6, (hp0[0][1] + hp0[1][1]) / 2 - 26
    t_sc0, t_sc1 = t_shou4 - 0.15, t_kan
    def scroll_m(t):
        """He brings the rolled scroll up into his hands and unrolls it (0.45 s); before '看不起' he rolls it up again
        and tucks it away as his hands go behind his back (the pose cut)."""
        if t < t_sc0 or t > t_sc1 + 0.14:
            return Tf(alpha=0.0, px=hx, py=hy)
        a_in = M.progress(t, t_sc0, t_sc0 + 0.18, "sine")
        a_out = 1 - M.progress(t, t_sc1 - 0.04, t_sc1 + 0.14, "sine")
        unroll = M.progress(t, t_sc0 + 0.1, t_sc0 + 0.45, "inout") - M.progress(t, t_sc1 - 0.44, t_sc1 - 0.08, "inout")
        dy = 24 * (1 - a_in) + 30 * (1 - a_out)
        return Tf(dy=dy, sx=0.13 + 0.87 * unroll, alpha=a_in * a_out, px=hx, py=hy)
    sc.add("scroll", doc3(scroll_markup(hx, hy, rot=-8, opened=True, k=0.5)), z=70.3,
           motion=M.combine(scroll_m, breath((PH[0][0], PH[0][1]), g0, phase=phs[0].bphase)))
    sc.add("scroll_glow", doc3(PR._ls_glow(hx - 4, hy - 30, 90, 110, 0.6, "ls3scr", "#fff6d8", "#f6d27a")), z=70.25,
           blend="screen", wc=0, motion=lambda t: Tf(alpha=0.8 * env(t, t_sc0 + 0.3, t_sc1 - 0.15, 0.3, 0.25)))
    for tp, (x, y), f in puff_at:
        sc.add(f"puff{tp:.2f}", puff_svg(x + f * 40 * K * TK, y - 290 * K * TK, f), z=11,
               motion=lambda t, tp=tp: Tf(alpha=env(t, tp, tp + 0.9, 0.1, 0.35), dy=-14 * M.progress(t, tp, tp + 0.9)))
    hp = C.body_points(C.pharisee, PH[0][0], PH[0][1], K, -1, variant=0, pose="grumble")["head"]
    sc.add("puff_heng", puff_svg(hp[0] - 34 * K, hp[1] + 8 * K, -1), z=72,
           motion=lambda t: Tf(alpha=env(t, t_heng, t_heng + 1.0, 0.08, 0.4), dy=-16 * M.progress(t, t_heng, t_heng + 1.0)))

    # ---------------------------------------------------------------- the coins
    stack = [(0.0, 3, 0.0), (t_cc1, 4, 0.0), (t_cc2, 5, 0.0), (t_duo, 7, 0.0), (t_shou, 9, 0.0), (t_bie + 0.15, 2, 0.6),
             (t_qian, 0, 1.0)]
    frames = [coin_stack_svg(n, p) for _, n, p in stack]
    sc.add("coins", frames, z=61, seed=301, frame_at=lambda t: float(max(i for i, (tk, _, _) in enumerate(stack) if t >= tk)),
           motion=M.combine(*[_pop_bump(tk, COINS) for tk, _, _ in stack[1:]]))
    for tk, _, _ in stack[1:]:
        sc.sfx("coins", tk, gain_db=-14, pan=0.35)

    # the closing tableau (identical to s04's first second): every seated figure in its END3 state
    for a in actors:
        st = END3.get(a.name.replace("_in", ""))
        if st is None:
            continue
        cur = a.fig.state_at(t_fin)
        oy = (SEAT_Y - BACK_Y) if a.path is not None else 0.0
        want = st[:5] + (st[5] + oy,) + st[6:]
        if cur != want:
            a.cut(t_fin, want, depth=5)
    for a in actors:
        a.build(sc)

    # ---------------------------------------------------------------- the light and the air
    add_air(sc, g0, "day")

    # ---------------------------------------------------------------- camera
    c_wide = Cam(1100, 654, 1900)
    c_tax = Cam(1700, 830, 1150)
    c_coin = Cam(1920, 828, 860)
    c_gate = Cam(700, 640, 1400)
    c_wel = Cam(1150, 654, 1900)
    c_meal = Cam(1430, 770, 1380)
    c_ph = Cam(2380, 720, 1500)
    c_law = Cam(2560, 760, 1100)
    c_frown = Cam(2540, 740, 920)
    c_heng = Cam(2280, 730, 1500)
    c_end = END_CAM
    c_mid = Cam(1300, 700, 1700)
    sc.camera = cam_seq([
        (0.0, c_wide), (0.5, c_wide), (t_jiang + 0.3, Cam(1220, 680, 1820)), (t_shui + 0.2, c_tax),
        (t_cc1, c_tax), (t_shou + 0.3, c_coin), (t_qian + 0.1, c_coin), (t_l2 + 0.55, c_mid), (t_cuo + 0.35, c_gate),
        (t_bu + 1.0, c_gate), (t_huan, c_wel), (t_hai - 0.3, c_wel), (t_chi + 0.3, c_meal), (t_l4 - 0.3, c_meal),
        (t_fa + 0.9, c_ph), (t_shou4 - 0.1, c_ph), (t_gui + 0.4, c_law), (t_zhou - 0.4, c_law),
        (t_zhou + 0.7, c_frown), (t_heng - 0.25, c_frown), (t_heng + 1.5, c_heng), (t_p_end - 0.3, c_heng),
        (T - 1.0, c_end), (T, c_end)])

    # ---------------------------------------------------------------- sound
    sc.sfx("crowd", 0, dur=T, gain_db=-27, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T, gain_db=-25, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_hao, gain_db=-23)
    sc.sfx("cloth", t_keshi + 0.15, gain_db=-22)
    sc.sfx("cloth", t_hai + 0.1, gain_db=-23)
    sc.sfx("crunch", t_yiqi + 0.1, gain_db=-20)
    sc.sfx("cheer", t_fan + 0.2, dur=1.4, gain_db=-24, fade_in=0.1, fade_out=0.7)
    sc.sfx("cloth", t_kan, gain_db=-24, pan=0.5)
    return sc


def _pop_bump(t0, piv, amp=0.08):
    return lambda t: (Tf(sx=1 + amp * math.sin(math.pi * (t - t0) / 0.22), sy=1 + amp * math.sin(math.pi * (t - t0) / 0.22),
                         px=piv[0], py=piv[1] + 10) if 0 <= t - t0 <= 0.22 else Tf())


END_CAM = Cam(2150, 738, 1600)
