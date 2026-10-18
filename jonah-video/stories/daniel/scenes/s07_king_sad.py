"""Scene 7 — the king is very sad (Daniel 6:14-15).

"国王听了，非常难过。他很喜欢但以理，想尽办法要救他，一直想到太阳下山。可是那些官员又来说：'王啊，你知道，你签了名的
命令，是不能改的。'"

King Darius's hall in Babylon on one 3200 x 1560 stage (the same hall and framing s06 ends on): a cedar-beamed
ceiling, a frieze of friendly glazed lions and rosettes on blue brick, Persepolis columns with kneeling-bull
capitals, purple curtains tied back from three tall arched openings that look out over the hazy city and the
ziggurat, a long red carpet to the throne before a purple hanging. The afternoon light warms to sunset gold and
orange as the king thinks; the sun sinks behind the city in the left opening.

  line 0  "国王听了，非常难过。"           the king on his throne (s06's last frame) — his face falls: chin in hand,
                                            sad. The officials bow once more (smug) and walk out to the left.
          "他很喜欢但以理，想尽办法要救他，" he gets up and paces, hands behind his back, head bowed (planted-foot
                                            pacing); a thought bubble shows smiling Daniel with a little heart; then
                                            a hop-turn and he paces back, question marks over his head.
          "一直想到太阳下山。"             he stops at the left opening, hand on his forehead, and watches the sun go
                                            down behind the city: the sky turns orange, sunbeams slant across the
                                            floor, the hall glows.
  line 1  "可是那些官员又来说："           the officials walk back in from the left and stop before him.
  line 2  "王啊，你知道，你签了名的命令，"  they bow; the old official unrolls the decree and holds it up, seal
                                            showing (a little glint on the seal);
          "是不能改的。"                   the front official shakes his finger (smug); the king hangs his head.
          Calm last second: the king sad in the sunset light, the camera easing back — dissolves into s08 (evening
          at the lions' den).

palace_layers() / PALACE geometry are shared with s06 (its second half takes place here). Pose changes are hard
cuts sold by a squash-and-hop; walking and pacing are planted-foot cycles; the sky is a background, so its
day -> sunset colours crossfade.
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
from stories.daniel.scenes.s05_prays import (WALK_A, WALK_N, Perf, bubble_svg, clamp, f1, fig, phrase_t, poly,
                                             rect, sprite, walk_pose)

SW, SH = 3200, 1560
FY = 1300                      # floor line (feet)
WALL_BOT = 1170                # where the back wall meets the floor
KP = 0.8                       # person scale in the hall
INK = P["ink"]
OPENINGS = [(560, 360), (1180, 360), (2760, 340)]     # arched openings (centre x, width)
OPEN_TOP, OPEN_SILL = 470, 1010
HORIZON = 985
THRONE_X = 1960
SUN_X = 1180
SUN_Y0 = 640                   # the sun's drawn centre (palace_layers moves it with sun_y)
COLUMNS = [(250, 0.6), (870, 0.6), (2420, 0.6), (3080, 0.6)]
ROBE_COLS = ("#7b4f9d",)


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


# ------------------------------------------------------------------ outside, seen through the openings
def p_sky_svg(k):
    """k 0 = afternoon, 1 = sunset."""
    top = S.mix("#9bcde0", "#c27a8e", k)
    mid = S.mix("#cfe8e6", "#f2a35e", k)
    low = S.mix("#f6e8c4", "#fbd27c", k)
    defs = S.lin_grad(f"s7sky{int(k * 100)}", [(0, top), (0.45, mid), (0.62, low), (1, low)],
                      ) + S.rad_grad(f"s7sg{int(k * 100)}", [(0, S.mix("#fff6dc", "#ffe08a", k), 0.85), (1, "#ffe08a", 0)])
    body = S.rect_bg(f"url(#s7sky{int(k * 100)})", SW, SH)
    body += f'<ellipse cx="{SUN_X}" cy="{HORIZON - 40}" rx="700" ry="380" fill="url(#s7sg{int(k * 100)})"/>'
    return doc(body, defs)


def p_sun_svg():
    y = SUN_Y0
    return doc(S.g(f'<circle cx="{SUN_X}" cy="{y}" r="62" fill="#ffd56a" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
                   f'stroke-width="4"/><circle cx="{SUN_X - 18}" cy="{y - 18}" r="20" fill="#fff4cc" opacity="0.7"/>',
                   filter="wobble-fine"))


def p_city_svg(k):
    tint = S.mix("#e6e6dc", "#f0b07a", k)
    out = PR.nineveh_skyline(-80, SW + 80, HORIZON + 30, scale=0.8, seed=31, haze=0.55, tint=tint)
    return doc(out)


# ------------------------------------------------------------------ the hall
WALL = "#ecdcb8"
WALL_DARK = S.shade(WALL, -0.12)
BLUE = "#3f74a8"


def arch_d(cx, w, top=OPEN_TOP, sill=OPEN_SILL):
    r = w / 2
    return (f"M{cx - r},{sill} L{cx - r},{top + r} A{r},{r} 0 0 1 {cx + r},{top + r} L{cx + r},{sill} Z")


def lion_frieze(x0, x1, y, s, seed=0):
    out = ""
    x = x0
    i = 0
    while x < x1:
        out += PR.lion(x, y, s, 1 if i % 2 == 0 else -1, pose="walk_a" if i % 2 else "walk_b")
        x += 520 * s / 0.2 * 0.62
        i += 1
    return out


def hall_svg():
    """Back wall with the arched openings cut out, ceiling beams, glazed frieze, dado, curtain pelmets."""
    holes = " ".join(arch_d(cx, w) for cx, w in OPENINGS)
    wall_d = f"M-40,-40 L{SW + 40},-40 L{SW + 40},{WALL_BOT} L-40,{WALL_BOT} Z " + holes
    cid = "s7wall"
    out = f'<path d="{wall_d}" fill="{WALL}" fill-rule="evenodd"/>'
    inner = ""
    # glazed blue frieze band with a row of friendly lions and rosettes (Babylon), above the openings
    inner += rect(-40, 268, SW + 80, 150, BLUE, 4)
    inner += rect(-40, 250, SW + 80, 22, "#e8c062", 3.5)
    inner += rect(-40, 414, SW + 80, 22, "#e8c062", 3.5)
    for rx_ in range(40, SW, 64):
        inner += f'<circle cx="{rx_}" cy="261" r="7" fill="#fff3d0" stroke="{INK}" stroke-width="2"/>'
        inner += f'<circle cx="{rx_ + 32}" cy="425" r="7" fill="#fff3d0" stroke="{INK}" stroke-width="2"/>'
    # dado: blue glazed bricks with a rosette band
    inner += rect(-40, WALL_BOT - 150, SW + 80, 150, S.mix(BLUE, WALL, 0.25), 4)
    inner += rect(-40, WALL_BOT - 172, SW + 80, 24, "#e8c062", 3.5)
    for rx_ in range(30, SW, 110):
        inner += f'<circle cx="{rx_}" cy="{WALL_BOT - 76}" r="20" fill="#f6e7bf" stroke="{INK}" stroke-width="3"/>'
        for j in range(8):
            a = j * math.pi / 4
            inner += (f'<circle cx="{rx_ + 11 * math.cos(a):.1f}" cy="{WALL_BOT - 76 + 11 * math.sin(a):.1f}" r="5" '
                      f'fill="#e8b63c"/>')
    # soft shading near the ceiling and floor
    inner += f'<rect x="-40" y="436" width="{SW + 80}" height="70" fill="{INK}" opacity="0.06"/>'
    out += f'<clipPath id="{cid}"><path d="{wall_d}" clip-rule="evenodd"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'
    # arch frames: deep reveals + glazed rims + low balustrades
    for cx, w in OPENINGS:
        out += f'<path d="{arch_d(cx, w)}" fill="none" stroke="{INK}" stroke-width="5"/>'
        out += f'<path d="{arch_d(cx, w + 40)}" fill="none" stroke="#e8c062" stroke-width="14"/>'
        out += f'<path d="{arch_d(cx, w + 40)}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>'
        out += f'<path d="{arch_d(cx, w + 70)}" fill="none" stroke="{INK}" stroke-width="4"/>'
        out += rect(cx - w / 2 - 30, OPEN_SILL - 10, w + 60, 26, S.shade(WALL, 0.12), 4, 6)
        for bx in range(int(cx - w / 2 + 20), int(cx + w / 2 - 10), 44):
            out += rect(bx, OPEN_SILL - 92, 20, 84, S.shade(WALL, 0.08), 3, 9)
        out += rect(cx - w / 2 - 6, OPEN_SILL - 108, w + 12, 20, S.shade(WALL, 0.14), 3.5, 6)
    # ceiling: cedar beams
    out += rect(-40, -40, SW + 80, 270, "#7a4c2e", 5)
    for bx in range(-20, SW + 40, 150):
        out += rect(bx, 150, 90, 92, P["wood"], 4, 8)
        out += f'<circle cx="{bx + 45}" cy="196" r="20" fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="3"/>'
    out += rect(-40, 214, SW + 80, 36, P["wood_light"], 4)
    for gx in range(30, SW, 90):
        out += f'<path d="M{gx},220 l14,12 l14,-12" fill="none" stroke="#e8c062" stroke-width="4"/>'
    lions = S.g(lion_frieze(60, SW, 410, 0.19), extra="")
    body = S.g(out, filter="wobble") + lions
    return doc(body)


def curtain(cx, w, side, col="#6e3f8f"):
    """A purple curtain tied back at one side of an opening (side -1 left, +1 right)."""
    x_edge = cx + side * (w / 2 + 34)
    top = OPEN_TOP - 30
    tie_y = 790
    xo = x_edge + side * 40
    xi = x_edge - side * 60
    d = (f"M{xo},{top} L{xi},{top} C{xi + side * 10},{top + 160} {x_edge + side * 4},{tie_y - 80} {x_edge + side * 14},{tie_y} "
         f"C{x_edge},{tie_y + 90} {xi + side * 20},{OPEN_SILL + 60} {xi + side * 6},{WALL_BOT + 20} "
         f"L{xo + side * 30},{WALL_BOT + 20} C{xo + side * 30},{tie_y + 120} {xo + side * 20},{tie_y} {xo},{top} Z")
    out = f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    for k in (0.3, 0.62):
        fx_ = xo + (xi - xo) * k
        out += (f'<path d="M{fx_},{top + 20} C{fx_ + side * 10},{tie_y - 120} {x_edge + side * 26},{tie_y - 30} '
                f'{x_edge + side * 30},{tie_y}" fill="none" stroke="{S.shade(col, -0.25)}" stroke-width="3.5"/>')
    out += f'<ellipse cx="{x_edge + side * 22}" cy="{tie_y}" rx="34" ry="14" fill="#e8b63c" stroke="{INK}" stroke-width="3.5"/>'
    out += (f'<path d="M{x_edge + side * 22},{tie_y + 10} l-8,60 M{x_edge + side * 22},{tie_y + 10} l10,58" '
            f'stroke="#e8b63c" stroke-width="6" stroke-linecap="round"/>')
    return out


def throne_back_svg():
    """A purple hanging with a gold border behind the throne, a canopy, a low dais and the red carpet."""
    x = THRONE_X
    out = ""
    # hanging
    out += rect(x - 250, 470, 500, WALL_BOT - 470, "#5f3b80", 5, 10)
    out += rect(x - 226, 494, 452, WALL_BOT - 520, "#7b4f9d", 3.5, 8)
    for yy in range(540, WALL_BOT - 40, 70):
        for xx in range(int(x - 190), int(x + 200), 70):
            out += f'<circle cx="{xx + (35 if (yy // 70) % 2 else 0)}" cy="{yy}" r="7" fill="#e8c062" opacity="0.9"/>'
    out += rect(x - 250, 470, 500, 30, "#e8c062", 4, 6)
    # canopy
    out += (f'<path d="M{x - 300},440 L{x + 300},440 L{x + 280},520 Q{x + 210},560 {x + 140},520 Q{x + 70},560 {x},520 '
            f'Q{x - 70},560 {x - 140},520 Q{x - 210},560 {x - 280},520 Z" fill="#c9714a" stroke="{INK}" stroke-width="4"/>')
    out += rect(x - 310, 420, 620, 30, "#e8c062", 4, 6)
    # floor: tiles, carpet, dais
    return doc(S.g(out, filter="wobble"))


def floor_svg():
    defs = S.lin_grad("s7fl", [(0, "#d9bf92"), (1, "#c49c6a")])
    out = f'<rect x="-40" y="{WALL_BOT}" width="{SW + 80}" height="{SH - WALL_BOT + 40}" fill="url(#s7fl)" stroke="{INK}" stroke-width="4"/>'
    for i, yy in enumerate((WALL_BOT + 40, WALL_BOT + 100, WALL_BOT + 180, WALL_BOT + 290)):
        out += f'<path d="M-40,{yy} L{SW + 40},{yy}" stroke="{S.shade("#c49c6a", -0.15)}" stroke-width="{2 + i}" opacity="0.5"/>'
    rng = random.Random(3)
    for i in range(70):
        xx, yy = rng.uniform(0, SW), rng.uniform(WALL_BOT + 20, SH)
        out += f'<path d="M{xx:.0f},{yy:.0f} l{rng.uniform(40, 120):.0f},0" stroke="#e8d3a8" stroke-width="3" opacity="0.5"/>'
    # the long red carpet runner leading to the throne
    cx = THRONE_X
    out += (f'<path d="M-60,{FY - 30} L{cx + 40},{FY - 30} L{cx + 80},{FY + 70} L-60,{FY + 70} Z" fill="#b04a3c" '
            f'stroke="{INK}" stroke-width="4"/>')
    out += (f'<path d="M-60,{FY - 18} L{cx + 46},{FY - 18} M-60,{FY + 58} L{cx + 74},{FY + 58}" stroke="#e8c062" '
            f'stroke-width="6"/>')
    # the dais (two low steps) under the throne
    out += rect(cx - 210, FY - 50, 420, 40, "#e2cfa6", 4, 8)
    out += rect(cx - 250, FY - 16, 500, 36, "#d6bf92", 4, 8)
    return doc(S.g(out, filter="wobble"), defs)


DAIS_Y = FY - 50               # the throne stands on the dais top


def columns_svg():
    out = ""
    for x, s in COLUMNS:
        out += PR.persian_column(x, FY + 40, s, height=1100)
    return doc(out)


def curtains_svg():
    out = ""
    for cx, w in OPENINGS:
        out += curtain(cx, w, -1) + curtain(cx, w, 1)
    return doc(S.g(out, filter="wobble-fine"))


def throne_svg():
    return doc(PR.throne(THRONE_X, DAIS_Y, KP, -1))


def lamps_svg():
    out = ""
    for x in (1540, 2380):
        out += f'<path d="M{x},250 L{x},560" stroke="{P["wood_dark"]}" stroke-width="4"/>'
        out += PR.lantern(x, 560, 0.8, lit=True)
    return doc(out)


def sunbeams_svg():
    """Slanting sunset beams from the left opening across the floor (screen blend)."""
    defs = S.lin_grad("s7beam", [(0, "#ffd88a", 0.55), (1, "#ffcf7a", 0.0)], x1=0, y1=0, x2=1, y2=1)
    out = ""
    for cx, w in OPENINGS[:2]:
        x0, x1 = cx - w / 2 + 30, cx + w / 2 - 30
        out += (f'<path d="M{x0},{OPEN_TOP + 120} L{x1},{OPEN_TOP + 120} L{x1 + 900},{SH} L{x0 + 520},{SH} Z" '
                f'fill="url(#s7beam)" filter="url(#blur-md)"/>')
    return doc(out, defs)


def palace_layers(sc, warm, alpha=None, sun_y=None):
    """Add the whole hall (behind the figures) to sc. warm(t) 0..1: afternoon -> sunset. alpha(t): layer opacity
    (s06 dissolves the hall in). sun_y(t): the sinking sun's centre y."""
    A = alpha or (lambda t: 1.0)

    def am(m=None):
        if m is None:
            return None if alpha is None else (lambda t: Tf(alpha=A(t)))
        if alpha is None:
            return m
        return lambda t: (lambda v: Tf(v.dx, v.dy, v.rot, v.sx, v.sy, v.alpha * A(t), v.px, v.py))(m(t))

    sk = [p_sky_svg(k) for k in (0.0, 0.5, 1.0)]
    sc.add("p_sky", sk, wc=0.4, frame_at=lambda t: 2 * clamp(warm(t)), motion=am())
    sy = sun_y or (lambda t: SUN_Y0)
    sc.add("p_sun", p_sun_svg(), wc=0.3, motion=am(lambda t: Tf(dy=sy(t) - SUN_Y0)))
    sc.add("p_city", [p_city_svg(k) for k in (0.0, 1.0)], wc=0.6, frame_at=lambda t: clamp(warm(t)), motion=am())
    sc.add("p_hall", hall_svg(), wc=0.75, motion=am())
    sc.add("p_throne_back", throne_back_svg(), wc=0.7, motion=am())
    sc.add("p_floor", floor_svg(), wc=0.75, motion=am())
    sc.add("p_curtains", curtains_svg(), wc=0.7, motion=am())
    sc.add("p_columns", columns_svg(), wc=0.6, motion=am())
    sc.add("p_lamps", lamps_svg(), wc=0.5, motion=am())
    sc.add("p_beams", sunbeams_svg(), wc=0, blend="screen",
           motion=am(lambda t: Tf(alpha=0.25 + 0.75 * clamp(warm(t)))))
    sc.add("p_throne", throne_svg(), wc=0.6, motion=am())


CAM0 = Cam(1905, 935, 1580)    # the hall framing s06 ends on and s07 starts from (unshifted hall coordinates)


def palace_flat_svg(k=0.08, sun_y=SUN_Y0, dx=0):
    """The whole hall at a fixed time of day as ONE layer (s06 dissolves it in: one moving layer instead of ten)."""
    sky = p_sky_svg(0.0 if k < 0.25 else (0.5 if k < 0.75 else 1.0))
    sun = p_sun_svg().replace(f'cy="{SUN_Y0}"', f'cy="{sun_y}"').replace(f'cy="{SUN_Y0 - 18}"', f'cy="{sun_y - 18}"')
    parts = [sky, sun, p_city_svg(round(k)), hall_svg(), throne_back_svg(), floor_svg(), curtains_svg(), columns_svg(),
             lamps_svg(), throne_svg()]
    return doc(f'<g transform="translate({dx},0)">' + "".join(parts) + "</g>")


# ------------------------------------------------------------------ figures
def king_fig(sp, pose=None, expr=None, facing=-1, ps=None):
    if ps is not None:
        D = C._king_design("darius", "stand", False, False)
        return sp.add(fig(D, C._KING_M, dict(ps), expr or ps["expr"], sp.ax, sp.ay, KP, facing, "king-x"))
    return sp.add(C.king(sp.ax, sp.ay, KP, facing, pose=pose, attire="darius", expr=expr, throne=False))


def official_fig(sp, v, pose=None, expr=None, facing=1, ps=None):
    if ps is not None:
        return sp.add(fig(C._official_design(v), C._OFFICIAL_M, dict(ps), expr or ps["expr"], sp.ax, sp.ay, KP,
                          facing, f"off{v}-x"))
    return sp.add(C.official(sp.ax, sp.ay, KP, facing, variant=v, pose=pose, expr=expr))


# scene-local poses
_PACE = C.POSES["pace_a"]
WAG_A = C._P(h=-4, legs=((6, 2), (-6, -2)), arms=(("fk", 8, 3), ("fk", 120, 168)), hands=("fist", "point"),
             expr="smug")
WAG_B = C._P(h=-4, legs=((6, 2), (-6, -2)), arms=(("fk", 8, 3), ("fk", 132, 192)), hands=("fist", "point"),
             expr="smug")
PRESENT = C._P(h=-6, legs=((6, 2), (-6, -2)), arms=(("fk", 112, 128), ("fk", 98, 116)), hands=("fist", "fist"),
               expr="smug")


def heart_d(cx, cy, w):
    h = w * 0.9
    return (f"M{cx},{cy + h * 0.45} C{cx - w * 0.9},{cy - h * 0.1} {cx - w * 0.5},{cy - h * 0.75} {cx},{cy - h * 0.3} "
            f"C{cx + w * 0.5},{cy - h * 0.75} {cx + w * 0.9},{cy - h * 0.1} {cx},{cy + h * 0.45} Z")


def walk_set(sp, D, m, facing, expr, arm_ps=None, A_=WALK_A, **over):
    out = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k, A=A_)
        if arm_ps is not None:
            ps["arms"], ps["hands"] = arm_ps["arms"], arm_ps["hands"]
        ps.update(over)
        out.append(sp.add(fig(D, m, ps, expr, sp.ax, sp.ay, KP, facing, "w")))
    return out


class Walker:
    """Planted-foot walking along x on the floor: legs [(t0, x0, x1, facing)]; between legs the figure stands."""

    def __init__(self, legs, adv, rate, y, sets):
        self.legs, self.adv, self.rate, self.y, self.sets = legs, adv, rate, y, sets

    def _leg(self, t):
        for i, (t0, x0, x1, f) in enumerate(self.legs):
            n = int(abs(x1 - x0) / self.adv)
            t1 = t0 + n / self.rate
            if t0 <= t < t1:
                return i, int((t - t0) * self.rate + 1e-6), n
        return None

    def frame(self, t):
        g = self._leg(t)
        if g is None:
            return None
        i, k, n = g
        return self.sets[self.legs[i][3]][k % (2 * WALK_N)]

    def x(self, t):
        x = self.legs[0][1]
        for t0, x0, x1, f in self.legs:
            n = int(abs(x1 - x0) / self.adv)
            if t < t0:
                return x
            k = min(n, int((t - t0) * self.rate + 1e-6))
            x = x0 + (1 if x1 > x0 else -1) * k * self.adv
        return x

    def end(self, i):
        t0, x0, x1, f = self.legs[i]
        return t0 + int(abs(x1 - x0) / self.adv) / self.rate


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    # ---------------------------------------------------------------- beats (all from the narration)
    t_sad = phrase_t(L0, "非常难过", 0.2) - 0.1          # chin in hand, very sad
    t_off_up = L0.start + 0.5                           # the officials straighten up (smug) ...
    t_off_go = L0.start + 1.1                           # ... and walk out to the left
    t_rise = L0.chunks[1].start + 0.05                  # "他很喜欢但以理" the king gets up
    t_bub = L0.chunks[1].start + 0.35                   # bubble: smiling Daniel + heart
    t_bub_out = phrase_t(L0, "想尽办法", 0.5) - 0.05
    t_q = phrase_t(L0, "想尽办法", 0.5) + 0.1          # "?" marks while he paces back
    t_sun = L0.chunks[2].start + 0.0                    # "一直想到太阳下山" he stops at the opening, the sun sets
    t_set = L0.end + 0.3                                # the sun is down
    t_in = L1.start - 0.1                               # "可是那些官员又来说" they walk back in
    t_turn = L1.start + 0.6                             # the king turns to them
    t_bow = L2.start + 0.02                             # "王啊" they bow
    t_decree = phrase_t(L2, "你签了名", 0.55) - 0.15    # the old official holds up the decree
    t_glint = t_decree + 0.6
    t_wag = L2.chunks[1].start + 0.0                    # "是不能改的" finger wag
    t_wag_end = t_wag + 0.9
    t_hang = L2.chunks[1].start + 0.35                  # the king hangs his head
    t_calm = min(L2.end + 0.2, T - 1.3)

    warm = lambda t: 0.08 + 0.92 * M.progress(t, t_rise - 0.5, t_set, "sine")
    sun_y = lambda t: SUN_Y0 + (HORIZON + 120 - SUN_Y0) * M.progress(t, t_rise, t_set, "sine")
    palace_layers(sc, warm, sun_y=sun_y)

    # ---------------------------------------------------------------- the king
    ks = sprite(560, 500, 280, 450, seed=70)
    D_k = C._king_design("darius", "pace_a", False, False)
    k_worry = king_fig(ks, "sit_throne", "worried")
    k_sitsad = king_fig(ks, "sit_sad")
    k_stand = king_fig(ks, "stand", "sad")
    k_stand_r = king_fig(ks, "stand", "sad", facing=1)
    k_worry_l = king_fig(ks, "stand", "worried")
    k_sad = king_fig(ks, "sad")
    pace = {f: walk_set(ks, D_k, C._KING_M, f, "sad", arm_ps=_PACE, t=6, h=14) for f in (1, -1)}
    k_adv = 2 * WALK_A / WALK_N * KP
    k_rate = 13.0                                       # a slow, thoughtful pace
    X_DOWN = THRONE_X - 290                             # where he lands off the dais
    t_land = t_rise + 0.42
    legs = [(t_land + 0.25, X_DOWN, X_DOWN - 300, -1)]
    kw = Walker(legs, k_adv, k_rate, FY, pace)
    t_back = kw.end(0) + 0.15
    kw.legs.append((t_back + 0.12, kw.x(t_back), kw.x(t_back) + 150, 1))
    t_stop2 = kw.end(1)
    k_sched = [(0, k_worry, 0), (t_sad, k_sitsad, 0.6), (t_rise, k_stand, 1.0), (t_land, k_stand, 0.5),
               (t_land + 0.13, pace[-1][0], 0.2),
               (t_back, k_stand_r, 0.6), (t_back + 0.02, pace[1][0], 0.0),
               (t_stop2 + 0.02, k_stand, 0.6), (t_sun, k_sad, 0.7),
               (t_turn, k_worry_l, 0.5), (t_hang, k_sad, 0.6)]

    def k_pos(t):
        if t < t_rise:
            return THRONE_X, DAIS_Y
        if t < t_land:                                  # a little hop down off the dais
            u = M.progress(t, t_rise, t_land, "linear")
            x = THRONE_X + (X_DOWN - THRONE_X) * M.ease("inout")(u)
            y = DAIS_Y + (FY - DAIS_Y) * u - 60 * math.sin(math.pi * u)
            return x, y
        return kw.x(t), FY

    k_perf = Perf(ks, k_sched, k_pos, walk=kw.frame, breathe=0.010, bper=3.4)
    k_shadow = doc(C.ground_shadow(0, FY, KP, width=130, opacity=0.22))
    sc.add("k_shadow", k_shadow, wc=0, motion=lambda t: Tf(dx=k_pos(t)[0], alpha=1.0 if t >= t_land else 0.0))
    sc.add_dynamic("king", k_perf)

    # ---------------------------------------------------------------- the officials
    OX0 = {1: 1330, 2: 1480, 0: 1640}                  # bowing (s06's last frame)
    OX1 = {1: 1060, 2: 1185, 0: 1315}                  # where they stop when they come back
    o_adv = 2 * WALK_A / WALK_N * KP
    o_rate = 17.0
    for i, v in enumerate((1, 2, 0)):
        sp = sprite(600, 500, 300, 450, seed=75 + v)
        D = C._official_design(v)
        bow = official_fig(sp, v, "bow")
        stand_l = official_fig(sp, v, "stand", "smug", facing=-1)
        stand_r = official_fig(sp, v, "scheme", "smug")
        out = walk_set(sp, D, C._OFFICIAL_M, -1, "smug")
        back = walk_set(sp, D, C._OFFICIAL_M, 1, "sly")
        go = t_off_go + 0.18 * (2 - i)                  # the one nearest the door goes first
        come = t_in + 0.2 * (2 - i)
        dist_in = 900
        legs_ = [(go, OX0[v], OX0[v] - 900, -1)]
        x_start = OX1[v] - dist_in
        # come back: start off-frame on the left so the last drawing lands on OX1
        n_in = int(dist_in / o_adv)
        x_start = OX1[v] - n_in * o_adv
        legs_.append((come, x_start, OX1[v] + 0.5, 1))
        wk = Walker(legs_, o_adv, o_rate, FY, {-1: out, 1: back})
        t_arr = wk.end(1)
        sched = [(0, bow, 0), (t_off_up + 0.15 * i, stand_r, 0.7), (go - 0.1, out[0], 0.3),
                 (t_arr + 0.02, stand_r, 0.5), (t_bow + 0.1 * i, bow, 0.6)]
        if v == 2:
            pres = sp.add(fig(D, C._OFFICIAL_M, dict(PRESENT), "smug", sp.ax, sp.ay, KP, 1, "pres") +
                          PR.decree(sp.ax + 118 * KP, sp.ay - 255 * KP, 0.62 * KP))
            sched += [(t_decree, pres, 0.9), (t_calm + 0.3, stand_r, 0.4)]
        if v == 0:
            wa = sp.add(fig(D, C._OFFICIAL_M, dict(WAG_A), "smug", sp.ax, sp.ay, KP, 1, "wa"))
            wb = sp.add(fig(D, C._OFFICIAL_M, dict(WAG_B), "smug", sp.ax, sp.ay, KP, 1, "wb"))
            sched += [(t_wag, wa, 0.8)]
            tt = t_wag + 0.14
            j = 0
            while tt < t_wag_end:
                sched.append((tt, wb if j % 2 == 0 else wa, 0.0))
                tt += 0.14
                j += 1
            sched.append((t_wag_end + 0.05, stand_r, 0.5))

        def pos(t, wk=wk, v=v, come=come):
            return wk.x(t), FY

        def alpha(t, wk=wk, go=go, come=come):
            x = wk.x(t)
            return 0.0 if (go < t < come and x < 600) else 1.0
        sc.add_dynamic(f"off{v}", Perf(sp, sched, pos, walk=wk.frame, breathe=0.012, bper=2.8 + 0.3 * i,
                                       phase=0.25 * i, alpha=alpha))

    # ---------------------------------------------------------------- bubble, marks, glint
    def k_head(t):
        x, y = k_pos(t)
        return x, y - 300 * KP

    bx, by = X_DOWN - 120, 560
    content = C.daniel(bx - 40, by + 105, 0.5, 1, pose="stand", expr="happy")
    content += S.g(f'<path d="{heart_d(bx + 70, by - 20, 52)}" fill="#e8707a" stroke="{INK}" stroke-width="4"/>',
                   filter="wobble-fine")
    cid = "s7bub"
    content = (f'<clipPath id="{cid}"><ellipse cx="{bx}" cy="{by}" rx="180" ry="128"/></clipPath>'
               f'<g clip-path="url(#{cid})">{content}</g>')
    tail_to = (X_DOWN - 200, FY - 330)
    sc.add("bubble", doc(bubble_svg(bx, by, 185, 132, tail_to, content)), wc=0.4,
           motion=lambda t: _pop(t, t_bub, t_bub_out, bx, by + 70))

    q_svg = []
    for j in range(3):
        q_svg.append(doc(S.text(0, 0, "?", size=84, fill=P["ink_soft"]) if False else
                         f'<text x="0" y="0" font-family="LXGW WenKai" font-weight="bold" font-size="86" '
                         f'fill="{P["ink_soft"]}" text-anchor="middle" transform="translate({200 + j * 10},{200}) '
                         f'rotate({(-14, 6, 18)[j]})">?</text>'))
    for j in range(3):
        tj = t_q + 0.32 * j

        def q_m(t, tj=tj, j=j):
            u = t - tj
            if u < 0 or u > 1.6:
                return Tf(alpha=0.0)
            hx, hy = k_head(t)
            k = M.ease("back")(clamp(u / 0.22))
            ox = (-70, 0, 70)[j]
            return Tf(dx=hx + ox - 200, dy=hy - 150 - 30 * u - 200 + 8 * math.sin(6 * u), sx=max(0.01, k),
                      sy=max(0.01, k), alpha=1 - M.progress(u, 1.2, 1.6, "sine"), px=200, py=200)
        sc.add(f"q{j}", q_svg[j], wc=0, motion=q_m)

    # the seal glints on "签了名的命令"
    gx, gy = OX1[2] + 118 * KP, FY - 255 * KP + 76 * 0.62 * KP
    glint = doc(f'<path d="M{gx},{gy - 46} L{gx + 9},{gy - 9} L{gx + 46},{gy} L{gx + 9},{gy + 9} L{gx},{gy + 46} '
                f'L{gx - 9},{gy + 9} L{gx - 46},{gy} L{gx - 9},{gy - 9} Z" fill="#fff4c4" stroke="#e8b63c" stroke-width="3"/>')
    sc.add("glint", glint, wc=0, motion=lambda t: _glint(t, t_glint, gx, gy))

    # ---------------------------------------------------------------- CAMERA
    camA = Cam(1500, 930, 1640)
    camS = Cam(1400, 910, 1600)
    camO = Cam(1340, 925, 1640)
    camEnd = Cam(1360, 915, 1700)
    sc.camera = M.cam_keys([(0.0, CAM0), (t_rise - 0.3, CAM0), (t_back, camA), (t_set, camS), (t_in + 0.6, camS),
                            (t_bow, camO), (t_calm, camO), (T, camEnd)], "sine")

    # ---------------------------------------------------------------- FX
    sc.fx = [
        FX.motes((300, 450, 3000, 1300), count=24, color=(255, 236, 196), size=(3, 6), alpha=90),
        FX.tint((255, 178, 120), lambda t: 0.22 * M.progress(warm(t), 0.3, 1.0, "sine"), mode="multiply"),
        FX.vignette(lambda t: 0.18 + 0.2 * M.progress(warm(t), 0.4, 1.0, "sine"), color=(60, 30, 30)),
    ]

    # ---------------------------------------------------------------- SOUND
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-23, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=t_set + 0.5, gain_db=-24, fade_in=0.8, fade_out=2.0, pan=-0.4)
    sc.sfx("night", t_set - 1.5, dur=T - t_set + 2.3, gain_db=-24, fade_in=2.0, fade_out=1.0, pan=-0.3)
    sc.sfx("cloth", t_sad, gain_db=-16)
    sc.sfx("footsteps", t_off_go, dur=2.2, gain_db=-19, fade_out=0.6, pan=-0.4)
    sc.sfx("cloth", t_rise, gain_db=-14)
    sc.sfx("thud", t_land, gain_db=-17)
    sc.sfx("pop", t_bub, gain_db=-12, pan=-0.1)
    sc.sfx("pop", t_bub_out, gain_db=-15, pan=-0.1)
    sc.sfx("footsteps", t_land + 0.25, dur=t_stop2 - t_land - 0.2, gain_db=-17, fade_out=0.4)
    for j in range(3):
        sc.sfx("pop", t_q + 0.32 * j, gain_db=-17, pan=-0.1)
    sc.sfx("footsteps", t_in, dur=2.0, gain_db=-17, fade_in=0.3, fade_out=0.4, pan=-0.4)
    sc.sfx("cloth", t_bow, gain_db=-15, pan=-0.3)
    sc.sfx("cloth", t_decree, gain_db=-14, pan=-0.3)
    sc.sfx("sparkle", t_glint, gain_db=-15, pan=-0.3)
    sc.sfx("cloth", t_hang, gain_db=-16)
    return sc


def _pop(t, t_in, t_out, px, py):
    if t < t_in or t > t_out + 0.2:
        return Tf(alpha=0.0)
    if t < t_out:
        u = t - t_in
        k = M.ease("back")(clamp(u / 0.35))
        return Tf(sx=max(0.01, k), sy=max(0.01, k), dy=-4 * math.sin(2 * math.pi * u / 2.0), px=px, py=py)
    u = (t - t_out) / 0.2
    return Tf(sx=1 + 0.15 * u, sy=1 + 0.15 * u, alpha=1 - u, px=px, py=py)


def _glint(t, t0, x, y):
    u = t - t0
    if u < 0 or u > 0.8:
        return Tf(alpha=0.0)
    k = math.sin(math.pi * u / 0.8)
    return Tf(sx=max(0.01, k), sy=max(0.01, k), rot=60 * u, alpha=k, px=x, py=y)
