"""Scene 8 — Joseph in Egypt: Potiphar's house, then the prison (Genesis 39).

N '在埃及，约瑟做了奴隶。可是，上帝和约瑟同在。' / N '约瑟做事很认真，主人很信任他，让他管理全家的事。' /
N '后来，约瑟被人冤枉，关进了监牢。可是在监牢里，上帝还是和约瑟同在。'

Two places on one 2700 x 1300 stage, joined by a soft dissolve (the second one is s09's stage):
  * POTIPHAR'S COURTYARD (sunny Egypt): pyramids on the far bank of the Nile (a little sailboat drifts by), palms,
    Potiphar's columned villa, a pylon gate on the right with a guard, a pile of grain sacks.
      line 0  '在埃及，约瑟做了奴隶。'   Joseph (white linen slave tunic) carries a grain sack on his shoulder to the
                                          pile and drops it there (咚, a puff of dust; the pile grows by one sack).
              '可是，上帝和约瑟同在。'   soft golden rays fall on him from above (light only), sparkles; he looks up
                                          and smiles.
      line 1  '约瑟做事很认真，'         he sweeps the courtyard (broom strokes with dust puffs), then counts on a clay
                                          tablet, head down.
              '主人很信任他，'           Potiphar, smiling, walks over to him (planted-foot walk).
              '让他管理全家的事。'       Potiphar holds out the ring of big keys; Joseph takes them in both hands, then
                                          holds them up proudly (jingle).
      line 2  '后来，约瑟被人冤枉，'     a small grey cloud of whispers drifts over him (no accuser is shown); Joseph is
                                          shocked (the keys fall, clink), then sad; Potiphar turns away; the guard
                                          walks over from the gate.
              '关进了监牢。'             the guard leads him away to the right by the wrist (the camera follows) ...
  * THE PRISON CELL (dissolve): plain stone walls, a high barred window with a beam of daylight, straw, a water jar,
    a little sprout in the light; two prisoners (the king's cupbearer and baker) dozing on the right.
              ... Joseph steps in through the barred door, which clangs shut behind him (哐当: the gate shakes); the
                  guard walks off in the dark corridor.
              '可是在监牢里，'           Joseph stands sad, head bowed, in the middle of the cell.
              '上帝还是和约瑟同在。'     the window beam turns warm gold and grows, sparkles drift around him; he lifts
                                          his face into the light and smiles. Calm last frame: s09 opens on exactly this
                                          frame (plain cross-dissolve).

Shared with s09 (same stage): SW, SH, GY, the cell geometry (CELL_*), cell_*_svg drawings, the cell figures and the
clock helpers. Pose changes are hard cuts sold by a squash-and-hop (Actor); walks are planted-foot cycles; nothing
crossfades between two drawings of a figure.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_A, WALK_N, walk_pose
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.daniel.scenes.s05_prays import clamp, fig
from engine import fx as FX
from stories.david.scenes.s08_saul import Actor, TightSprite, WalkPath, pop_tf, pt, rays_svg, sparkle_dyn

SW, SH = 2700, 1300
GY = 1060                      # ground line (feet) in both places
K = 0.85                       # person scale in the courtyard
KC = 0.95                      # person scale in the cell (s09 too)
INK = P["ink"]
RATE = 20.0                    # walk drawings per second (~320 px/s)

# ---------------------------------------------------------------- courtyard geometry
VILLA_X, VILLA_Y = 700, 915
PILE_X, PILE_Y = 1545, 1012            # grain sacks (back plane)
GATE_X = 2330                          # pylon gate (prison side)
J0 = 1130                              # Joseph's start (carrying a sack)
JW = 1400                              # Joseph's work spot
POT0 = 760                             # Potiphar's start
POT1 = JW - 232                        # Potiphar giving the keys
GUARD0 = 2120                          # the guard at the gate
GAP = 196                              # guard ahead of Joseph when leading him
GUARD1 = JW + GAP                      # the guard beside Joseph

# ---------------------------------------------------------------- cell geometry (s09 shares it)
CAM_CELL = Cam(1600, 668, 1960)        # the cell framing (= the courtyard camera at the dissolve)
CAM_CELL2 = Cam(1596, 662, 1890)       # s08's last frame / s09's first frame
IX0 = 1600 - 1056                      # left edge of a nominal 2112-wide cell framing (544)
DOOR_X = IX0 + 406                     # barred door (centre)
DOOR_W, DOOR_H = 300 * KC, 400 * KC    # opening
WIN_X, WIN_Y = IX0 + 770, 292          # high window
WIN_S = 1.3
NICHE = (IX0 + 590, GY - 455)          # wall niche with a little oil lamp
JC = IX0 + 946                         # Joseph in the cell
CUP_X = IX0 + 1406                     # the cupbearer (prisoner)
BAK_X = IX0 + 1666                     # the baker (prisoner)
GLD_X = DOOR_X - 30                    # guard behind the gate
BEAM = ((WIN_X - 76, WIN_Y + 68), (WIN_X + 76, WIN_Y + 68), (JC + 160, GY + 4), (JC - 130, GY + 4))

WALL = "#bba98f"
WALL_DK = "#9d8b74"
FLOOR = "#a88d69"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def poly(pts, fill, sw=4, extra=""):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}" {st} {extra}/>'


def rect(x, y, w, h, fill, sw=4, rx=0, extra=""):
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" fill="{fill}" {st} {extra}/>'


def tube(pts, w, col, ow=3.4):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f1(w + 2 * ow)}" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{f1(w)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def keyed(keys_, curve="sine"):
    """Scalar keyframes [(t, v), ...] -> f(t)."""
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


def mul_alpha(m, a):
    """Multiply a motion's opacity by a(t)."""
    if m is None:
        return lambda t: Tf(alpha=a(t))
    return lambda t: (lambda v: Tf(v.dx, v.dy, v.rot, v.sx, v.sy, v.alpha * a(t), v.px, v.py))(m(t))


# ================================================================== figures
class ShadowSprite(TightSprite):
    """TightSprite whose drawings get a soft contact shadow under the anchor."""

    def __init__(self, cw, ch, ax, ay, wc=1.0, seed=0, shadow=None):
        super().__init__(cw, ch, ax, ay, wc, seed)
        self.shadow = shadow

    def add(self, markup, shadow=True):
        if shadow and self.shadow:
            s, w = self.shadow
            markup = C.ground_shadow(self.ax, self.ay - 2, s, width=w, opacity=0.2) + markup
        return super().add(markup)


def person_sprite(s, seed=0, wide=230, tall=420, shadow=130):
    cw, ch = 2 * wide * s + 80, tall * s + 120
    return ShadowSprite(cw, ch, cw / 2, ch - 40, seed=seed, shadow=(s, shadow) if shadow else None)


def jdesign(attire="slave", front=None, mid=None, behind=None):
    D = C._joseph_design(attire, None, 1.0, False, False, "stand")
    D["front"] = C._hooks(D.get("front"), front)
    D["mid"] = C._hooks(D.get("mid"), mid)
    D["behind"] = C._hooks(D.get("behind"), behind)
    return D


def jfig(sp, ps, expr, s, facing=1, attire="slave", front=None, mid=None, behind=None, label="j"):
    D = jdesign(attire, front, mid, behind)
    return sp.add(fig(D, C._JOSEPH_M, dict(ps), expr, sp.ax, sp.ay, s, facing, f"j-{attire}-{label}"))


def jlib(sp, pose, s, facing=1, attire="slave", expr=None, **kw):
    return sp.add(C.joseph(sp.ax, sp.ay, s, facing, pose=pose, expr=expr, attire=attire, coat=None, **kw))


def walk_set(sp, mk, label="w", **over):
    """2*WALK_N planted-foot walk drawings: mk(ps, k) -> markup at the sprite anchor."""
    idx = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k)
        ps.update(over)
        idx.append(sp.add(mk(ps, k)))
    return idx


def adv(s):
    return 2 * WALK_A / WALK_N * s


# scene-local Joseph poses
LOOK_UP = dict(C.POSES["look_up"], expr="happy")
LOOK_UP_SOFT = C._P(h=-20, arms=(("fk", 14, 22), ("fk", -12, -18)), hands=("open", "open"), look=(0.03, -0.10),
                    expr="happy")
SWEEP = [C._P(t=12, h=12, legs=((10, 3), (-8, -3)), arms=(("ik", "abs", 22, -205, 1), ("ik", "abs", 58, -150, 1)),
              hands=("fist", "fist"), look=(0.03, 0.06), expr="determined"),
         C._P(t=10, h=12, legs=((8, 3), (-9, -3)), arms=(("ik", "abs", -8, -200, 1), ("ik", "abs", 24, -146, 1)),
              hands=("fist", "fist"), look=(0.03, 0.06), expr="determined")]
WRITE = C._P(t=4, h=20, legs=((6, 2), (-5, -2)), arms=(("ik", "abs", 64, -164, 1), ("ik", "abs", 50, -184, 1)),
             hands=("fist", "fist"), look=(0.03, 0.10), expr="happy")
KEYS_UP = C._P(h=-8, legs=((7, 3), (-6, -3)), arms=(("fk", 16, 10), ("fk", 146, 168)), hands=("fist", "fist"),
               expr="proud")
SHOCK = C._P(h=-6, legs=((7, 3), (-6, -3)), arms=(("fk", 36, 112), ("fk", -34, -108)), hands=("open", "open"),
             expr="surprised")


def broom_hook(D):
    """A straw broom held in both hands, its head on the ground ahead (drawn over the body)."""
    def front(st):
        (_, _, W0), (_, _, W1) = st["arms"][0], st["arms"][1]
        hr, g = st["m"]["hr"], st["ground"]
        dx, dy = W1[0] - W0[0], W1[1] - W0[1]
        k = (g - 18 - W0[1]) / dy
        head = (W0[0] + dx * k, g - 18)
        top = (W0[0] - dx * 0.45, W0[1] - dy * 0.45)
        s = tube([top, head], 9, P["wood_light"], 3.0)
        ang = math.degrees(math.atan2(dy, dx)) - 90
        br = (f'<g transform="translate({f1(head[0])},{f1(head[1])}) rotate({ang:.1f})">'
              f'<path d="M-12,-6 L12,-6 L30,40 L-30,40 Z" fill="#dcb763" stroke="{INK}" stroke-width="3.4" '
              f'stroke-linejoin="round"/>'
              + "".join(f'<path d="M{xx * 0.45:.1f},0 L{xx:.1f},38" stroke="#a9843e" stroke-width="2"/>'
                        for xx in (-20, -10, 0, 10, 20))
              + f'<rect x="-14" y="-12" width="28" height="10" rx="3" fill="#b5523b" stroke="{INK}" '
                f'stroke-width="3"/></g>')
        s += br
        s += C._fist(W0, hr, D["skin"]) + C._fist(W1, hr, D["skin"])
        return s
    return front


def tablet_hook(D):
    """A clay tablet in the far hand and a reed stylus in the near hand (counting the sacks)."""
    def front(st):
        (_, _, W0), (_, _, W1) = st["arms"][0], st["arms"][1]
        hr = st["m"]["hr"]
        cx, cy = W0[0] + 14, W0[1] - 6
        s = (f'<g transform="translate({f1(cx)},{f1(cy)}) rotate(-24)">'
             f'<rect x="-26" y="-36" width="52" height="66" rx="8" fill="#d6b07e" stroke="{INK}" stroke-width="3.4"/>'
             + "".join(f'<path d="M-16,{yy} L{12 - 6 * (i % 2)},{yy}" stroke="#8d6a43" stroke-width="2.6" '
                       f'stroke-linecap="round"/>' for i, yy in enumerate((-22, -12, -2, 8, 18)))
             + '</g>')
        s += C._fist(W0, hr, D["skin"], 0, 2)
        s += tube([(W1[0] - 4, W1[1] + 10), (W1[0] + 18, W1[1] - 30)], 4, "#c9a86a", 2.2)
        s += C._fist(W1, hr, D["skin"])
        return s
    return front


def joseph_carry_hooks(D):
    b, mi, fr = C._carry_hooks(D, "carry", "sack")
    return b, mi, fr


# ================================================================== courtyard drawings
def ext_sky_svg():
    defs = (S.lin_grad("s8sky", [(0, "#86c2dc"), (0.45, "#bfe0e4"), (0.62, "#f6e7c2"), (1, "#f8e2b4")])
            + S.rad_grad("s8sun", [(0, "#fff6d6", 0.95), (0.35, "#fde6a8", 0.5), (1, "#fde6a8", 0)]))
    b = S.rect_bg("url(#s8sky)", SW, SH)
    b += '<circle cx="2330" cy="210" r="330" fill="url(#s8sun)"/>'
    b += (f'<circle cx="2330" cy="210" r="62" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
          f'stroke-width="4" filter="url(#wobble-fine)"/>')
    return b, defs


def ext_far_body():
    """Distant desert bank with pyramids and small palms (on the far side of the Nile)."""
    out = ""
    tint = "#e9e2c8"
    out += S.g(S.path(S.hill(-80, SW + 80, 776, 26, seed=5, bumps=6, bottom=820), fill="#e8cf98", sw=3),
               filter="wobble")
    out += PR._haze(PR.pyramids(1960, 778, 0.55, n=3, haze=0.25, ground=False), tint, 0.18, 0.3)
    out += PR._haze(PR.pyramids(380, 778, 0.33, n=2, haze=0.4, ground=False, facing=-1), tint, 0.3, 0.4)
    for x, s, ln in ((90, 0.26, 0.2), (640, 0.22, -0.3), (1130, 0.25, 0.1), (1290, 0.2, -0.2), (2520, 0.27, 0.3)):
        out += PR._haze(PR.palm_tree(x, 790, s, lean=ln), tint, 0.35, 0.45)
    out += S.g(f'<rect x="-40" y="786" width="{SW + 80}" height="40" fill="#d9c58d"/>', filter="wobble")
    return out


def nile_svg(ph):
    return doc(PR.nile(-80, SW + 80, 832, width=96, scale=0.8, phase=ph, seed=3, reeds=False))


def ext_near_body():
    """Near bank, courtyard floor, the villa, the pylon gate, jars and plants."""
    out = ""
    defs = S.lin_grad("s8yard", [(0, "#ead2a0"), (1, "#e2c48d")])
    out += S.g(S.path(S.hill(-80, SW + 80, 892, 18, seed=8, bumps=7, bottom=SH + 60), fill="#9dbb62", sw=3.5),
               filter="wobble")
    for x in range(-40, SW + 60, 150):
        out += PR.papyrus(x + 30 * math.sin(x), 902, 0.55 + 0.1 * math.sin(x * 0.7))
    out += S.g(f'<path d="M-60,915 L{SW + 60},915 L{SW + 60},{SH + 60} L-60,{SH + 60} Z" fill="url(#s8yard)" '
               f'stroke="{INK}" stroke-width="4"/>', filter="wobble")
    # paving: soft joints converging toward the villa
    rng = random.Random(3)
    for i, y in enumerate((952, 1000, 1060, 1135, 1225)):
        out += (f'<path d="M-40,{y} L{SW + 40},{y + rng.uniform(-3, 3):.0f}" stroke="#c9a46f" stroke-width="3" '
                f'opacity="0.55"/>')
    for i in range(-6, 26):
        x0 = 1350 + i * 130
        out += (f'<path d="M{x0 * 0.35 + 877:.0f},915 L{x0:.0f},{SH + 40}" stroke="#c9a46f" stroke-width="2.6" '
                f'opacity="0.4"/>')
    out = S.g(out, filter="wobble")
    # pylon gate (toward the prison)
    gx, gy = GATE_X, 935
    pyl = ""
    for side in (-1, 1):
        x0 = gx + side * 95
        x1 = gx + side * 255
        pts = [(x0, gy), (x1, gy), (x1 - side * 22, gy - 380), (x0 + side * 4, gy - 380)]
        pyl += poly(pts, "#e6cfa0", 4.5)
        pyl += poly([(x0 + side * 8, gy - 330), (x1 - side * 26, gy - 330), (x1 - side * 24, gy - 352),
                     (x0 + side * 6, gy - 352)], "#3f6fa8", 3)
        pyl += poly([(x0 + side * 10, gy - 300), (x1 - side * 30, gy - 300), (x1 - side * 29, gy - 316),
                     (x0 + side * 9, gy - 316)], "#c9533f", 3)
    pyl += rect(gx - 110, gy - 330, 220, 330, "#5a4636", 4)
    pyl += rect(gx - 130, gy - 372, 260, 50, "#e6cfa0", 4)
    pyl += rect(gx - 120, gy - 362, 240, 14, "#e8b63c", 2.5)
    pyl += f'<ellipse cx="{gx}" cy="{gy - 150}" rx="70" ry="120" fill="#7a6250" opacity="0.6"/>'
    out += S.g(pyl, filter="wobble-fine")
    out += PR.egypt_house(VILLA_X, VILLA_Y, 1.0, variant=1)
    # jars and a lotus planter by the porch
    for x, y, s in ((975, 956, 0.42), (1030, 964, 0.48), (275, 962, 0.45)):
        out += PR.jar(x, y - 82 * s, s)
    out += PR.bush(1100, 940, 0.45, variant=1) + PR.bush(360, 945, 0.5, variant=1)
    return out, defs


def ext_static_svg():
    sky, d1 = ext_sky_svg()
    return doc(sky + ext_far_body(), d1)


def ext_front_static_svg():
    near, d2 = ext_near_body()
    return doc(near, d2)


def palm_svg(x, y, s, sw, lean=0.0):
    return doc(PR.palm_tree(x, y, s, lean=lean, sway=sw))


def fg_ext_svg():
    out = ""
    for x, v, s in ((40, 2, 1.2), (150, 0, 1.0), (2600, 2, 1.15), (2700, 0, 1.0), (1980, 1, 0.8)):
        out += PR.grass_tuft(x, 1265, s, variant=v)
    out += PR.bush(-20, 1290, 1.1, variant=1) + PR.bush(2720, 1295, 1.0, variant=0)
    return doc(out)


def boat_svg():
    """A little Nile sailboat (felucca) on the far water."""
    x, y = 0, 0
    b = (f'<path d="M-62,-6 Q0,18 66,-10 L54,6 Q0,24 -50,8 Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M-2,-6 L-2,-120" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M0,-118 Q52,-60 44,-14 L0,-14 Z" fill="#f4ead2" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M-6,-104 Q-48,-62 -40,-16 L-6,-16 Z" fill="#efe0be" stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(f'<g transform="translate({1050},{824}) scale(0.62)">{b}</g>', filter="wobble-fine"))


def sacks_svg(n):
    return doc(PR.grain_sacks(PILE_X, PILE_Y, 0.78, n=n))


def whisper_svg():
    """A small grey cloud of whispers (squiggles, no faces) — someone told lies about Joseph."""
    cx, cy = 0, 0
    c = S.cloud(cx, cy, 250, 120, "#b8b4b0", seed=6, sw=3.5, shade_fill="#9c9792")
    sq = ""
    for i, (x, y) in enumerate(((-70, -6), (0, -24), (66, -2), (-30, 22), (40, 26))):
        sq += (f'<path d="M{x - 18},{y} q6,-10 12,0 t12,0 t12,0" fill="none" stroke="#6f6a66" stroke-width="4" '
               f'stroke-linecap="round"/>')
    for x, y, r in ((150, 40, 13), (178, 66, 9)):
        sq += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#b8b4b0" stroke="{INK}" stroke-width="3"/>'
    return S.g(c + sq, filter="wobble-fine")


def puff_body(x, y, s=1.0, col="#f8f0dc"):
    out = ""
    circ = ((-34, -8, 20), (-6, -18, 26), (26, -10, 22), (48, -2, 14), (-52, 0, 13))
    for dx, dy, r in circ:
        out += (f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s)}" fill="{col}" '
                f'stroke="#b89d70" stroke-width="{f1(5 * s)}"/>')
    for dx, dy, r in circ:
        out += f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s)}" fill="{col}"/>'
    return S.g(f'<g opacity="0.9">{out}</g>', filter="wobble-fine")


def puff_motion(t0, x, y, dur=0.7):
    def m(t):
        u = (t - t0) / dur
        if u < 0 or u > 1:
            return Tf(alpha=0.0)
        k = 0.6 + 0.8 * M.ease("out")(u)
        return Tf(sx=k, sy=k, dy=-14 * u, alpha=(1 - u) ** 1.4, px=x, py=y)
    return m


def keys_svg():
    """The ring of keys lying where they fall (local, anchor = ring centre)."""
    s = f'<circle cx="0" cy="0" r="11" fill="none" stroke="{INK}" stroke-width="7"/>'
    s += f'<circle cx="0" cy="0" r="11" fill="none" stroke="{P["gold"]}" stroke-width="3.2"/>'
    for ang, ln in ((20, 46), (60, 40), (100, 34)):
        a = math.radians(ang)
        p0 = (11 * math.cos(a), 11 * math.sin(a))
        p1 = (p0[0] + ln * math.cos(a), p0[1] + ln * math.sin(a))
        s += tube([p0, p1], 6, P["wood_light"], 2.4)
        s += tube([p1, (p1[0] + 9 * math.cos(a + 1.57), p1[1] + 9 * math.sin(a + 1.57))], 5, P["wood_light"], 2.2)
    return s


# ================================================================== the cell (shared with s09)
def _stones(x0, x1, y0, y1, seed, h=92, w=168):
    """Big irregular hand-cut stones in courses (mortar shows as the gaps)."""
    rng = random.Random(seed)
    out = ""
    r = 0
    y = y0
    while y < y1:
        hh = h * rng.uniform(0.85, 1.1)
        x = x0 - w * rng.uniform(0.2, 0.9)
        while x < x1 + w:
            ww = w * rng.uniform(0.7, 1.3)
            col = S.mix(WALL, rng.choice((WALL_DK, "#c9b89f", "#b09d84", "#c2ad8f", WALL)), rng.uniform(0.25, 0.75))
            pts = [(x + 4 + rng.uniform(-3, 3), y + 4 + rng.uniform(-3, 3)),
                   (x + ww - 4 + rng.uniform(-3, 3), y + 4 + rng.uniform(-3, 3)),
                   (x + ww - 4 + rng.uniform(-3, 3), y + hh - 4 + rng.uniform(-3, 3)),
                   (x + 4 + rng.uniform(-3, 3), y + hh - 4 + rng.uniform(-3, 3))]
            out += S.path(S.smooth_path(pts, tension=0.35), fill=col, sw=3)
            if rng.random() < 0.35:
                out += (f'<path d="M{f1(x + ww * rng.uniform(0.2, 0.6))},{f1(y + hh * 0.3)} q14,8 30,2" fill="none" '
                        f'stroke="{WALL_DK}" stroke-width="2.6" opacity="0.7"/>')
            if rng.random() < 0.3:
                out += (f'<ellipse cx="{f1(x + ww * 0.5)}" cy="{f1(y + hh * 0.7)}" rx="{f1(ww * 0.28)}" ry="{f1(hh * 0.12)}" '
                        f'fill="{WALL_DK}" opacity="0.25"/>')
            x += ww
        y += hh
        r += 1
    return out


def cell_back_svg():
    """Everything behind the door gate and the guard: the dark corridor beyond the door."""
    x0, x1 = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2
    yt = GY - DOOR_H
    defs = S.lin_grad("s8cor", [(0, "#5a4a3c"), (1, "#3a2f27")])
    b = rect(x0 - 200, yt - 60, DOOR_W + 400, DOOR_H + 80, "url(#s8cor)", 0)
    b += rect(x0 - 200, GY - 14, DOOR_W + 400, 40, "#4d3f33", 0)
    # a far torch glow in the corridor (warm, friendly)
    b += f'<ellipse cx="{f1(x0 + 40)}" cy="{f1(yt + 120)}" rx="150" ry="120" fill="#f0b45a" opacity="0.22" filter="url(#soft)"/>'
    return doc(S.g(b, filter="wobble"), defs)


def cell_wall_body(hole=True):
    x0, x1 = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2
    yt = GY - DOOR_H
    defs = (S.lin_grad("s8wall", [(0, "#8f7f6a"), (0.25, "#b3a189"), (1, "#bcaa90")])
            + S.rad_grad("s8wlight", [(0, "#fff3d6", 0.5), (1, "#fff3d6", 0)])
            + S.lin_grad("s8dado", [(0, "#a48d70"), (1, "#8f785e")])
            + S.rad_grad("s8lamp", [(0, "#ffd98a", 0.55), (1, "#ffd98a", 0)]))
    if hole:
        defs += (f'<mask id="s8hole" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{SW + 100}" height="{SH + 100}">'
                 f'<rect x="-50" y="-50" width="{SW + 100}" height="{SH + 100}" fill="#fff"/>'
                 f'<rect x="{f1(x0)}" y="{f1(yt)}" width="{f1(DOOR_W)}" height="{f1(DOOR_H + 30)}" rx="6" fill="#000"/>'
                 f'</mask>')
    dado = GY - 150
    w = rect(-40, -40, SW + 80, GY + 40, "url(#s8wall)", 0)
    w += _stones(-40, SW + 40, 96, dado, seed=21)
    # plastered lower band
    w += S.path(S.wave_line(dado + 4, 5, 260, 0.6, -60, SW + 60), fill="none", sw=4)
    w += (f'<path d="{S.wave_line(dado + 4, 5, 260, 0.6, -60, SW + 60)} L{SW + 60},{GY + 10} L-60,{GY + 10} Z" '
          f'fill="url(#s8dado)"/>')
    rng = random.Random(5)
    for _ in range(26):
        cx, cy = rng.uniform(0, SW), rng.uniform(dado + 30, GY - 20)
        w += f'<path d="M{f1(cx)},{f1(cy)} q{rng.uniform(10, 30):.0f},{rng.uniform(-6, 6):.0f} {rng.uniform(30, 60):.0f},{rng.uniform(-4, 8):.0f}" fill="none" stroke="#7d6850" stroke-width="2.4" opacity="0.5"/>'
    w += f'<ellipse cx="{WIN_X + 90}" cy="{GY - 330}" rx="760" ry="460" fill="url(#s8wlight)"/>'
    # ceiling beams across the top
    beams = rect(-40, 30, SW + 80, 70, "#7a5536", 4)
    for bx in range(-20, SW + 60, 260):
        beams += rect(bx, 12, 66, 104, "#8a6240", 4, rx=8)
        beams += f'<circle cx="{bx + 33}" cy="62" r="12" fill="#6e4a2e" stroke="{INK}" stroke-width="2.4" opacity="0.8"/>'
    beams += rect(-40, -40, SW + 80, 72, "#5f4630", 0)
    # door frame: heavy lintel and posts
    fr = rect(x0 - 34, yt - 46, DOOR_W + 68, 50, "#8f7d68", 4, rx=6)
    fr += rect(x0 - 30, yt - 2, 28, DOOR_H + 2, "#8f7d68", 4, rx=4) + rect(x1 + 2, yt - 2, 28, DOOR_H + 2, "#8f7d68", 4, rx=4)
    # wall niche with a little lamp (warm, friendly light)
    nx, ny = NICHE
    ni = f'<ellipse cx="{nx}" cy="{ny - 40}" rx="170" ry="140" fill="url(#s8lamp)"/>'
    ni += (f'<path d="M{nx - 62},{ny + 40} L{nx - 62},{ny - 40} Q{nx - 62},{ny - 100} {nx},{ny - 100} Q{nx + 62},{ny - 100} '
           f'{nx + 62},{ny - 40} L{nx + 62},{ny + 40} Z" fill="#5c4836" stroke="{INK}" stroke-width="4"/>')
    ni += rect(nx - 74, ny + 36, 148, 18, "#9a8670", 4, rx=4)
    # tally marks scratched by the prisoners' corner
    tm = ""
    tx, ty = BAK_X + 150, GY - 330
    for g_ in range(3):
        for i in range(5 if g_ < 2 else 3):
            xx = tx + g_ * 70 + i * 11
            if i == 4:
                tm += f'<path d="M{xx - 50},{ty + 34} L{xx + 4},{ty + 4}" stroke="#6d5a46" stroke-width="3.4" stroke-linecap="round"/>'
            else:
                tm += f'<path d="M{xx},{ty} L{xx - 3},{ty + 40}" stroke="#6d5a46" stroke-width="3.4" stroke-linecap="round"/>'
    body = (S.g(w, filter="wobble") + S.g(beams, filter="wobble") + S.g(fr + ni, filter="wobble-fine")
            + S.g(tm, filter="wobble-fine"))
    body += PR.oil_lamp(nx - 14, ny + 36, 0.75, lit=True)
    if hole:
        body = f'<g mask="url(#s8hole)">{body}</g>'
    return body, defs


def cell_wall_svg():
    body, defs = cell_wall_body(True)
    # window (bars, a glimpse of sky and green) and a little sprout under it
    body += PR.prison_window(WIN_X, WIN_Y, WIN_S, light=0.0, wall=False)
    return doc(body, defs)


def cell_floor_svg():
    defs = S.lin_grad("s8floor", [(0, "#9b8162"), (1, "#b49a76")])
    rng = random.Random(9)
    b = rect(-40, GY - 6, SW + 80, SH - GY + 60, "url(#s8floor)", 4)
    b += f'<path d="M-40,{GY + 2} L{SW + 40},{GY + 2}" stroke="#6f5a45" stroke-width="5" opacity="0.6"/>'
    straw = ""
    for cx, cy, w in ((CUP_X - 20, GY + 26, 330), (BAK_X + 20, GY + 30, 330), (JC + 30, GY + 46, 240),
                      (IX0 + 160, GY + 60, 200), (IX0 + 1950, GY + 70, 220)):
        straw += f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="22" fill="#d9bd73" opacity="0.75"/>'
        for _ in range(int(w / 9)):
            x = cx + rng.uniform(-w / 2, w / 2) * 0.95
            y = cy + rng.uniform(-14, 16)
            a = rng.uniform(-0.5, 0.5)
            straw += (f'<path d="M{f1(x)},{f1(y)} l{f1(26 * math.cos(a))},{f1(26 * math.sin(a))}" '
                      f'stroke="{rng.choice(("#c9a24e", "#e6cc84", "#b88f3e"))}" stroke-width="3" stroke-linecap="round"/>')
    for _ in range(40):
        x, y = rng.uniform(0, SW), rng.uniform(GY + 30, SH)
        b += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{rng.uniform(4, 10):.1f}" ry="3" fill="#8a7155" opacity="0.5"/>'
    b += f'<rect x="-40" y="{GY + 120}" width="{SW + 80}" height="{SH}" fill="#6e5a44" opacity="0.18"/>'
    b += f'<rect x="-40" y="{GY + 190}" width="{SW + 80}" height="{SH}" fill="#6e5a44" opacity="0.18"/>'
    out = S.g(b, filter="wobble") + S.g(straw, filter="wobble-fine")
    # water jar and bowl by the right wall, a sprout in the light
    out += PR.jar(IX0 + 1930, GY - 40, 0.48, color="#b8774a")
    out += S.g(f'<path d="M{IX0 + 2010},{GY - 4} q34,26 68,0 Z" fill="#a8693f" stroke="{INK}" stroke-width="3.4"/>',
               filter="wobble-fine")
    sx, sy = JC - 190, GY + 2
    sprout = (f'<path d="M{sx},{sy} q-4,-26 4,-46" fill="none" stroke="{P["leaf_dark"]}" stroke-width="4"/>'
              f'<path d="M{sx + 3},{sy - 30} q22,-18 36,-6 q-18,14 -36,6 Z" fill="{P["leaf"]}" stroke="{INK}" stroke-width="2.6"/>'
              f'<path d="M{sx + 1},{sy - 22} q-22,-14 -32,0 q16,10 32,0 Z" fill="{P["leaf_light"]}" stroke="{INK}" stroke-width="2.6"/>'
              f'<circle cx="{sx + 4}" cy="{sy - 50}" r="7" fill="#f2c14e" stroke="{INK}" stroke-width="2.4"/>')
    out += S.g(sprout, filter="wobble-fine")
    return doc(out, defs)


def gate_svg(open_):
    """The barred gate only (frame and corridor are drawn separately), hinge on the left."""
    w, h = DOOR_W, DOOR_H
    x0, yb = DOOR_X - w / 2, GY
    gate = ""
    for k in range(7):
        xx = x0 + 13 + k * (w - 26) / 6
        gate += rect(xx - 6, yb - h + 4, 12, h - 6, "#6e6a66", 3, rx=4)
    for yy in (yb - h + 28, yb - h / 2, yb - 40):
        gate += rect(x0 + 4, yy, w - 8, 12, "#6e6a66", 3, rx=4)
    gate += rect(x0 + w - 40, yb - h / 2 - 22, 26, 34, "#8e8a86", 3, rx=4)
    k = 1 - 0.86 * clamp(open_)
    return doc(S.g(f'<g transform="translate({f1(x0)},0) scale({k:.3f},1) translate({f1(-x0)},0)">{gate}</g>',
                   filter="wobble-fine"))


def beam_svg(gold=0.0, uid="s8beam", alpha=1.0):
    """The daylight beam from the window down to Joseph's place (gold > 0: warmer, wider, God's presence)."""
    (ax, ay), (bx, by), (cx_, cy_), (dx, dy) = BEAM
    wid = 1 + 0.35 * gold
    mx = (cx_ + dx) / 2
    c2 = (mx + (cx_ - mx) * wid, cy_)
    d2 = (mx + (dx - mx) * wid, dy)
    col = S.mix("#fff6dc", "#ffe08a", gold)
    k = 1 + 0.45 * gold
    defs = S.lin_grad(uid, [(0, col, 0.55 * alpha * k), (0.7, col, 0.30 * alpha * k), (1, col, 0.12 * alpha * k)], 0, 0, 0.3, 1)
    defs += S.rad_grad(uid + "p", [(0, col, 0.7 * alpha), (0.6, col, 0.25 * alpha), (1, col, 0)])
    b = f'<path d="M{ax},{ay} L{bx},{by} L{f1(c2[0])},{f1(c2[1])} L{f1(d2[0])},{f1(d2[1])} Z" fill="url(#{uid})" filter="url(#soft)"/>'
    b += f'<ellipse cx="{f1(mx)}" cy="{GY + 10}" rx="{f1(200 * wid)}" ry="46" fill="url(#{uid}p)"/>'
    return doc(b, defs)


def glow_svg(x, y, rx, ry, uid, col="#ffe7a0", a=0.75):
    defs = S.rad_grad(uid, [(0, col, a), (0.55, col, a * 0.35), (1, col, 0)])
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#{uid})"/>', defs)


def prisoner_fig(sp, kind, pose, expr=None, facing=-1, marks=True, s=KC):
    return sp.add(C.egyptian(sp.ax, sp.ay, s, facing, kind=kind, pose=pose, expr=expr, prisoner=True, marks=marks))


CELL_BREATHE = {"cup": (0.012, 3.1, 0.15), "bak": (0.013, 3.5, 0.55), "jos": (0.011, 3.0, 0.0)}


def add_cell(sc, alpha=None, toff=0.0, s9=False):
    """Static cell layers (corridor, wall with the door hole, floor). The gate, guard and figures are added by the
    scenes. alpha(t) fades the cell in (s08)."""
    al = (lambda m: mul_alpha(m, alpha)) if alpha is not None else (lambda m: m)
    sc.add("cell_back", cell_back_svg(), wc=0.6, motion=al(None) if alpha else None)


def add_cell_front(sc, alpha=None):
    al = (lambda m: mul_alpha(m, alpha)) if alpha is not None else (lambda m: m)
    sc.add("cell_wall", cell_wall_svg(), wc=0.8, motion=al(None) if alpha else None)


def add_cell_floor(sc, alpha=None):
    al = (lambda m: mul_alpha(m, alpha)) if alpha is not None else (lambda m: m)
    sc.add("cell_floor", cell_floor_svg(), wc=0.8, motion=al(None) if alpha else None)


def beam_base_alpha(t):
    return 0.85 + 0.15 * math.sin(2 * math.pi * t / 4.3)


def gold_env(t, t_gold):
    """0 -> 1 golden presence in the cell (s09 continues it with the shifted clock)."""
    return M.progress(t, t_gold, t_gold + 1.2, "sine")


def s08_clock():
    """(s08 duration, time of the golden light in the cell) — s09 continues the cell clocks from s08."""
    try:
        from engine.loader import context
        c8 = context("s08_egypt")
        return c8.duration, pt(c8, 2, "上帝还是") - 0.15
    except Exception:
        return 22.03, 18.19


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    # ---------------------------------------------------------------- beats (from the narration)
    t_walk1 = L0.start + 0.3                        # '在埃及' carries the sack to the pile
    t_drop = pt(ctx, 0, "约瑟做了") + 0.45          # 咚 — the sack onto the pile
    t_turn = pt(ctx, 0, "可是") + 0.05              # turns toward the villa
    t_light = pt(ctx, 0, "上帝") - 0.2              # golden rays
    t_look = t_light + 0.3                          # looks up, smiles
    t_light_off = L0.end + 0.6
    t_sweep = pt(ctx, 1, "约瑟做事") + 0.05         # sweeping
    t_write = pt(ctx, 1, "主人") - 0.25             # counting on a tablet
    t_pot_walk = pt(ctx, 1, "很信任") - 0.3         # Potiphar walks over
    t_give = pt(ctx, 1, "让他") + 0.05              # keys held out
    t_take = t_give + 0.3                           # Joseph takes them
    t_keys_up = t_give + 0.85                       # holds them up
    t_whisp = pt(ctx, 2, "后来") + 0.5              # grey cloud of whispers drifts in
    t_shock = pt(ctx, 2, "约瑟被") + 0.05           # shocked, keys fall
    t_sad = pt(ctx, 2, "冤枉") + 0.1                # sad
    t_pot_turn = t_shock + 0.55                     # Potiphar turns away
    t_g_walk = pt(ctx, 2, "后来") + 0.35            # the guard walks over
    t_lead = pt(ctx, 2, "关进") - 0.32              # hop: led away
    t_lead_walk = t_lead + 0.16
    t_x0 = pt(ctx, 2, "监牢。") - 0.42              # dissolve to the cell
    t_x1 = t_x0 + 0.6
    t_in = t_x0 - 0.1                               # Joseph walking in through the door (cell)
    t_clang = pt(ctx, 2, "监牢。") + 0.35           # 哐当 — the gate shuts
    t_gold = pt(ctx, 2, "上帝还是") - 0.15          # golden light in the cell
    t_lookc = t_gold + 0.45                         # he lifts his face

    ext_a = lambda t: 1.0 - M.progress(t, t_x0, t_x1, "sine")
    int_a = lambda t: M.progress(t, t_x0, t_x1, "sine")

    # ================================================================ THE CELL (underneath; revealed by the dissolve)
    sc.add("cell_back", cell_back_svg(), wc=0.6)
    # guard behind the gate (in the corridor)
    gsp = person_sprite(KC, seed=81)
    Dg, mg = C._egyptian_design("guard", 1, False, True, "stand")
    g_stand_r = gsp.add(C.egyptian(gsp.ax, gsp.ay, KC, 1, kind="guard", variant=1, pose="stand"))
    g_stand_l = gsp.add(C.egyptian(gsp.ax, gsp.ay, KC, -1, kind="guard", variant=1, pose="stand"))
    gw_l = walk_set(gsp, lambda ps, k: fig(Dg, mg, dict(ps, arms=(ps["arms"][0], ("fk", 48, 80))), "neutral",
                                           gsp.ax, gsp.ay, KC, -1, "g-in"))
    g_t_turn = t_clang + 0.45
    g_t_go = g_t_turn + 0.3
    gwp = WalkPath([(g_t_go, GLD_X, GLD_X - 520, 16.0)], gw_l, adv(KC))
    sc.add_dynamic("guard_in", Actor(gsp, [(0, g_stand_r, 0), (g_t_turn, g_stand_l, 0.6)],
                                     lambda t: (gwp.x(t), GY), walk=gwp.frame, alpha=lambda t: int_a(t) if t < g_t_go + 2.5 else 0.0,
                                     breathe=0.010, bper=2.9))
    sc.add("cell_wall", cell_wall_svg(), wc=0.8)
    sc.add("cell_floor", cell_floor_svg(), wc=0.8)
    # the gate: open while Joseph comes in, then it clangs shut and shakes
    gframes = [gate_svg(v) for v in (1.0, 0.75, 0.5, 0.25, 0.0)]
    t_shut0 = t_clang - 0.28

    def gate_fa(t):
        return min(4.0, max(0.0, (t - t_shut0) / 0.28 * 4))

    def gate_m(t):
        u = t - t_clang
        if 0 <= u < 0.5:
            return Tf(dx=5 * math.sin(u * 60) * (1 - u / 0.5))
        return Tf()
    sc.add("gate", gframes, wc=0.4, frame_at=lambda t: float(int(gate_fa(t) + 1e-6)), motion=gate_m)
    # daylight beam (always) + the golden presence (last chunk)
    sc.add("beam", beam_svg(0.0, "s8b0"), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=beam_base_alpha(t) * (1 - 0.6 * gold_env(t, t_gold))))
    sc.add("beam_gold", beam_svg(1.0, "s8b1"), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=gold_env(t, t_gold) * (0.88 + 0.12 * math.sin(2 * math.pi * (t - t_gold) / 2.6))))
    sc.add("jglow", glow_svg(JC + 10, GY - 180, 300, 290, "s8jg", a=0.85), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=gold_env(t, t_gold + 0.3) * (0.8 + 0.2 * math.sin(2 * math.pi * (t - t_gold) / 2.6))))

    # the prisoners, dozing on the straw (s09 wakes them)
    for name, kind, x, seed in (("cup", "cupbearer", CUP_X, 83), ("bak", "baker", BAK_X, 84)):
        sp = person_sprite(KC, seed=seed, shadow=200)
        i0 = prisoner_fig(sp, kind, "sit", "sleepy", marks=False)
        amp, per, ph = CELL_BREATHE[name]
        sc.add_dynamic(name, Actor(sp, [(0, i0, 0)], lambda t, x=x: (x, GY), alpha=int_a, breathe=amp, bper=per,
                                   phase=ph))

    # Joseph in the cell
    jsp = person_sprite(KC, seed=85)
    jw_in = walk_set(jsp, lambda ps, k: fig(jdesign(), C._JOSEPH_M, dict(ps, h=16), "sad", jsp.ax, jsp.ay, KC, 1, "jin"))
    j_sad = jlib(jsp, "sad", KC, 1)
    j_up = jfig(jsp, LOOK_UP_SOFT, "happy", KC, 1, label="lookup")
    x_in0 = DOOR_X - 40
    n_in = int(round((JC - x_in0) / adv(KC)))
    x_in0 = JC - n_in * adv(KC)
    jwp = WalkPath([(t_in, x_in0, JC, 18.0)], jw_in, adv(KC))
    t_arrive = jwp.end(0)
    amp, per, ph = CELL_BREATHE["jos"]
    sc.add_dynamic("joseph_in", Actor(jsp, [(0, jw_in[0], 0), (t_arrive, j_sad, 0.5), (t_lookc, j_up, 0.8)],
                                      lambda t: (jwp.x(t), GY), walk=jwp.frame, alpha=int_a, breathe=amp, bper=per,
                                      phase=ph))
    sc.add_dynamic("cell_sparkles", sparkle_dyn((JC - 260, GY - 520, JC + 260, GY - 60), count=16, t0=t_gold + 0.4,
                                                t1=1e9, color=(255, 236, 160), size=(8, 17), period=1.7, drift=-9,
                                                seed=31))

    # ================================================================ THE COURTYARD (on top; dissolves away)
    ea = lambda m=None: mul_alpha(m, ext_a)
    sc.add("ext_far", ext_static_svg(), wc=0.6, motion=ea())
    sc.add("clouds", doc(S.cloud(560, 190, 360, 90, "#fbf3e6", seed=2, sw=3) + S.cloud(1460, 120, 300, 80, "#fbf3e6", seed=5, sw=3)
                         + S.cloud(2050, 300, 260, 64, "#fbf3e6", seed=8, sw=3)), wc=0.6,
           motion=ea(M.combine(M.drift(vx=-6), M.bob(3, 9))))
    sc.add("nile", [nile_svg(p) for p in (0.0, 0.25, 0.5, 0.75, 1.0)], wc=0.5, motion=ea(),
           frame_at=lambda t: (t / 0.6) % 4)
    sc.add("boat", boat_svg(), wc=0.5, motion=ea(M.combine(M.drift(vx=16), M.bob(2.5, 3.2))))
    sc.add("ext_near", ext_front_static_svg(), wc=0.75, motion=ea())
    for i, (x, y, s_, ln) in enumerate(((170, 985, 0.95, 0.1), (2470, 975, 0.92, -0.15))):
        fr = [palm_svg(x, y, s_, sw, ln) for sw in (-0.4, 0.0, 0.4)]
        sc.add(f"palm{i}", fr, wc=0.7, motion=ea(),
               frame_at=lambda t, i=i: 1 + math.sin(2 * math.pi * (t / (3.4 + 0.6 * i) + 0.3 * i)))
    # the sack pile grows by one at the drop
    sc.add("sacks", sacks_svg(4), wc=0.7, motion=ea())
    # the dropped sack: falls from Joseph's shoulder onto the ground beside the pile (咚)
    dsx, dsy = PILE_X - 118, GY - 6
    sk_y0 = GY - 290 * K

    def drop_m(t):
        if t < t_drop - 0.16:
            return Tf(alpha=0.0)
        u = M.progress(t, t_drop - 0.16, t_drop, "in")
        sq = 0.0
        if t > t_drop:
            v = t - t_drop
            sq = 0.16 * math.exp(-v / 0.07) * math.cos(v * 40)
        return Tf(dx=-34 * (1 - u), dy=(sk_y0 - dsy) * (1 - u), sx=1 + sq, sy=1 - sq, alpha=ext_a(t), px=dsx, py=dsy)
    sc.add("sack_drop", doc(PR.sack(dsx, dsy, 0.62, rot=-8, seed=4)), wc=0.6, motion=drop_m)

    # ---------------------------------------------------------------- Potiphar
    psp = person_sprite(K, seed=91)
    Dp, mp = C._egyptian_design("potiphar", 0, False, None, "walk_a")
    p_stand = psp.add(C.egyptian(psp.ax, psp.ay, K, 1, kind="potiphar", pose="stand"))
    p_give = psp.add(C.egyptian(psp.ax, psp.ay, K, 1, kind="potiphar", pose="give"))
    p_talk = psp.add(C.egyptian(psp.ax, psp.ay, K, 1, kind="potiphar", pose="talk", expr="happy"))
    p_sad = psp.add(C.egyptian(psp.ax, psp.ay, K, 1, kind="potiphar", pose="stand", expr="sad"))
    p_away = psp.add(C.egyptian(psp.ax, psp.ay, K, -1, kind="potiphar", pose="sad"))
    pw = walk_set(psp, lambda ps, k: fig(Dp, mp, ps, "happy", psp.ax, psp.ay, K, 1, "pw"))
    n_p = int(round((POT1 - POT0) / adv(K)))
    pot0 = POT1 - n_p * adv(K)
    pwp = WalkPath([(t_pot_walk, pot0, POT1, 17.0)], pw, adv(K))
    p_arr = pwp.end(0)
    psched = [(0, p_stand, 0), (t_sweep + 0.9, p_stand, 0.35), (t_write, p_talk, 0.4),
              (p_arr, p_stand, 0.4), (t_give, p_give, 0.7), (t_keys_up, p_talk, 0.5),
              (t_shock + 0.1, p_sad, 0.4), (t_pot_turn, p_away, 0.7)]
    sc.add_dynamic("potiphar", Actor(psp, psched, lambda t: (pwp.x(t), GY), walk=pwp.frame, alpha=ext_a,
                                     breathe=0.011, bper=3.2, phase=0.3))

    # ---------------------------------------------------------------- Joseph (courtyard)
    jx = person_sprite(K, seed=93, wide=260)
    Dj = jdesign()
    cb, cm, cf = joseph_carry_hooks(Dj)
    Dc = dict(Dj, behind=cb, mid=C._hooks(Dj.get("mid"), cm), front=C._hooks(Dj.get("front"), cf))
    carry_ps = C._carry_pose("carry", "sack")
    c_stand = jx.add(fig(Dc, C._JOSEPH_M, dict(carry_ps, expr="determined"), "determined", jx.ax, jx.ay, K, 1, "carry"))
    cw = walk_set(jx, lambda ps, k: fig(Dc, C._JOSEPH_M, dict(ps, arms=(ps["arms"][0], carry_ps["arms"][1]),
                                                                hands=("fist", "fist")), "determined",
                                        jx.ax, jx.ay, K, 1, "cw"))
    j_stand_r = jlib(jx, "stand", K, 1, expr="happy")
    j_stand_l = jlib(jx, "stand", K, -1, expr="happy")
    j_look = jfig(jx, LOOK_UP, "happy", K, -1, label="look")
    j_sweep = [jx.add(fig(jdesign(front=broom_hook(Dj)), C._JOSEPH_M, dict(SWEEP[i]), "determined", jx.ax, jx.ay, K, -1,
                          f"sw{i}")) for i in (0, 1)]
    j_write = jx.add(fig(jdesign(front=tablet_hook(Dj)), C._JOSEPH_M, dict(WRITE), "happy", jx.ax, jx.ay, K, -1, "wr"))
    j_take = jlib(jx, "give", K, -1, expr="amazed")
    j_keys = jx.add(fig(jdesign(front=C._keys_front(Dj)), C._JOSEPH_M, dict(KEYS_UP), "proud", jx.ax, jx.ay, K, -1, "ku"))
    j_shock = jfig(jx, SHOCK, "surprised", K, -1, label="shock")
    j_sad_l = jlib(jx, "sad", K, -1)
    j_sad_r = jlib(jx, "sad", K, 1)

    # led away: the guard's near hand holds Joseph's wrist (both in step)
    Dg2, mg2 = C._egyptian_design("guard", 1, False, False, "lead")
    spear_far = C._spear_front(dict(Dg2))
    Dg2["behind"] = lambda st: spear_far(dict(st, arms=[st["arms"][1], st["arms"][0]]))
    Dg2["front"] = None
    lead_arms = (("fk", 40, 72), ("fk", -42, -26))
    ld_ps = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k)
        ps["arms"], ps["hands"] = lead_arms, ("fist", "fist")
        ld_ps.append(ps)
    jl = []
    for k, ps in enumerate(ld_ps):
        hand = C.body_points(lambda x, y, s, f, ps=ps: fig(Dg2, mg2, ps, "neutral", x, y, s, f, "probe"), 0, 0, 1.0, 1)["hands"][1]
        hx, hy = hand[0] + GAP / K * 1.0, hand[1]        # in Joseph's figure coordinates (Joseph at -GAP)
        jps = walk_pose(k)
        jps["arms"] = (("ik", "abs", hx - 4, hy + 4, 1), jps["arms"][1])
        jps["hands"] = ("fist", "fist")
        jps["h"] = 16
        jl.append(jx.add(fig(jdesign(), C._JOSEPH_M, jps, "sad", jx.ax, jx.ay, K, 1, f"led{k}")))

    n_c = int(round((JW - J0) / adv(K)))
    j0 = JW - n_c * adv(K)
    lead_x0 = JW
    n_l = 40
    jwalk = WalkPath([(t_walk1, j0, JW, RATE), (t_lead_walk, JW, JW + n_l * adv(K), RATE)], [cw, jl], adv(K))
    sw_sched = []
    tt, i = t_sweep, 0
    while tt < t_write - 0.15:
        sw_sched.append((tt, j_sweep[i % 2], 0.5 if i == 0 else 0.0))
        tt += 0.34
        i += 1
    jsched = ([(0, c_stand, 0), (t_drop - 0.16, j_stand_r, 0.8), (t_turn, j_stand_l, 0.5), (t_look, j_look, 0.6),
               (t_look + 2.0, j_stand_l, 0.3)] + sw_sched +
              [(t_write, j_write, 0.6), (t_take, j_take, 0.6), (t_keys_up, j_keys, 0.9), (t_shock, j_shock, 1.0),
               (t_sad, j_sad_l, 0.4), (t_lead, j_sad_r, 0.6)])
    sc.add_dynamic("joseph", Actor(jx, jsched, lambda t: (jwalk.x(t), GY), walk=jwalk.frame, alpha=ext_a,
                                   breathe=0.011, bper=3.0))

    # ---------------------------------------------------------------- the guard (courtyard)
    gx = person_sprite(K, seed=95, wide=260)
    Dg1, mg1 = C._egyptian_design("guard", 1, False, True, "stand")
    gs_l = gx.add(C.egyptian(gx.ax, gx.ay, K, -1, kind="guard", variant=1, pose="stand"))
    gwl = walk_set(gx, lambda ps, k: fig(Dg1, mg1, dict(ps, arms=(ps["arms"][0], ("fk", 48, 80))), "neutral",
                                         gx.ax, gx.ay, K, -1, "gw"))
    g_lead_stand = gx.add(fig(Dg2, mg2, dict(ld_ps[0]), "neutral", gx.ax, gx.ay, K, 1, "gls"))
    g_ld = [gx.add(fig(Dg2, mg2, dict(ps), "neutral", gx.ax, gx.ay, K, 1, f"gl{k}")) for k, ps in enumerate(ld_ps)]
    n_g = int(round((GUARD0 - GUARD1) / adv(K)))
    g0 = GUARD1 + n_g * adv(K)
    gwalk = WalkPath([(t_g_walk, g0, GUARD1, RATE), (t_lead_walk, GUARD1, GUARD1 + n_l * adv(K), RATE)], [gwl, g_ld],
                     adv(K))
    gsched = [(0, gs_l, 0), (gwalk.end(0), gs_l, 0.4), (t_lead, g_lead_stand, 0.6)]
    sc.add_dynamic("guard", Actor(gx, gsched, lambda t: (gwalk.x(t), GY), walk=gwalk.frame, alpha=ext_a,
                                  breathe=0.010, bper=2.7, phase=0.4))

    # ---------------------------------------------------------------- small things
    sc.add("drop_puff", doc(puff_body(dsx, GY - 8, 1.2)), wc=0, motion=ea(puff_motion(t_drop, dsx, GY - 8, 0.8)))
    for i in range(4):
        tp = t_sweep + 0.17 + 0.68 * i
        if tp < t_write - 0.2:
            px_ = JW - 135 - 8 * i
            sc.add(f"sweep_puff{i}", doc(puff_body(px_, GY - 2, 0.7)), wc=0, motion=ea(puff_motion(tp, px_, GY - 2, 0.6)))
    # the keys fall when he is shocked
    kx0, ky0 = C.body_points(lambda x, y, s, f: fig(jdesign(front=C._keys_front(Dj)), C._JOSEPH_M, dict(KEYS_UP),
                                                          "proud", x, y, s, f, "kp"), JW, GY, K, -1)["hands"][1]
    keys_m = lambda t: (Tf(alpha=0.0) if t < t_shock else
                        Tf(dx=-30 * M.progress(t, t_shock, t_shock + 0.4, "linear"),
                           dy=(GY - 12 - ky0) * M.progress(t, t_shock, t_shock + 0.38, "in"),
                           rot=-80 * M.progress(t, t_shock, t_shock + 0.38, "linear"), px=kx0, py=ky0))
    sc.add("keys_fall", doc(S.g(f'<g transform="translate({f1(kx0)},{f1(ky0 + 16)}) scale({K})">{keys_svg()}</g>',
                                filter="wobble-fine")), wc=0.4, motion=ea(keys_m))
    # golden rays on Joseph (light only)
    def light_a(t):
        return 0.95 * M.progress(t, t_light, t_light + 0.9, "sine") * (1 - M.progress(t, t_light_off, t_light_off + 1.2, "sine"))
    sc.add("rays", rays_svg(JW - 260, -80, JW, GY - 150, 9, "s8r", n=6, wk=1.6, pool=(230, 60), w=SW, h=SH),
           wc=0, blend="screen", motion=lambda t: Tf(alpha=light_a(t) * ext_a(t)))
    sc.add_dynamic("ext_sparkles", sparkle_dyn((JW - 230, GY - 470, JW + 230, GY - 80), count=14, t0=t_light + 0.3,
                                               t1=t_light_off + 1.0, color=(255, 236, 160), size=(8, 16), seed=17))
    # grey cloud of whispers
    wx, wy = JW - 10, GY - 470
    def whisp_m(t):
        if t < t_whisp or t > t_lead + 0.8:
            return Tf(alpha=0.0)
        u = M.progress(t, t_whisp, t_whisp + 1.0, "out")
        a = M.progress(t, t_whisp, t_whisp + 0.5, "sine") * (1 - M.progress(t, t_lead + 0.1, t_lead + 0.8, "sine"))
        return Tf(dx=260 * (1 - u) + 6 * math.sin(3 * t), dy=-60 * (1 - u) + 5 * math.sin(2.3 * t),
                  sx=0.8 + 0.2 * u, sy=0.8 + 0.2 * u, alpha=a * ext_a(t), px=wx, py=wy)
    sc.add("whispers", doc(f'<g transform="translate({wx},{wy})">{whisper_svg()}</g>'), wc=0.5, motion=whisp_m)
    sc.add("fg", fg_ext_svg(), wc=0.6, motion=ea())

    # ---------------------------------------------------------------- camera
    cam0 = Cam(1300, 650, 2270)
    camA = Cam(1200, 690, 1980)                     # Joseph and the villa
    camB = Cam(1190, 712, 1740)                     # Potiphar and Joseph (keys)
    camC = Cam(1350, 700, 1860)                     # the guard comes
    sc.camera = M.cam_keys([(0.0, cam0), (L0.start + 0.2, cam0), (t_look + 0.6, camA), (t_pot_walk, camA),
                            (t_give + 0.2, camB), (t_whisp, camB), (t_lead, camC), (t_x0 + 0.2, CAM_CELL),
                            (t_lookc, CAM_CELL), (T - 1.3, CAM_CELL2), (T, CAM_CELL2)], "sine")

    # birds over the courtyard
    for i, (bx, by, v, col) in enumerate(((300, 330, 55, "brown"), (-120, 250, 62, "blue"))):
        fr = [doc(PR.songbird(bx, by, 0.55, 1, wing=w, color=col)) for w in (1, 0.5, 0, -0.5, -1)]
        sc.add(f"bird{i}", fr, wc=0.4, frame_at=lambda t, i=i: 2 + 2 * math.sin(2 * math.pi * (t * 2.6 + 0.3 * i)),
               motion=ea(M.combine(M.drift(vx=v), M.bob(10, 2.2, 0.4 * i))))
    sc.fx = [FX.vignette(lambda t: 0.42 * int_a(t), color=(46, 32, 22)),
             FX.tint((255, 214, 120), lambda t: 0.13 * gold_env(t, t_gold), mode="screen")]

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=t_x1, gain_db=-17, fade_in=0.8, fade_out=0.6)
    sc.sfx("wind_soft", 0, dur=t_x1, gain_db=-21, fade_in=0.8, fade_out=0.6)
    sc.sfx("footsteps", t_walk1, dur=jwalk.end(0) - t_walk1, gain_db=-17, pan=0.05)
    sc.sfx("thud", t_drop, gain_db=-6, pan=0.15)
    sc.sfx("cloth", t_turn, gain_db=-17)
    sc.sfx("chime", t_light, gain_db=-11)
    sc.sfx("sparkle", t_light + 0.5, gain_db=-14)
    for i in range(len(sw_sched)):
        if i % 2 == 0:
            sc.sfx("cloth", sw_sched[i][0], gain_db=-19, pan=-0.05)
    sc.sfx("footsteps", t_pot_walk, dur=p_arr - t_pot_walk, gain_db=-18, pan=-0.2)
    sc.sfx("coins", t_give + 0.05, gain_db=-14, pan=-0.1)
    sc.sfx("coins", t_keys_up, gain_db=-12)
    sc.sfx("crowd", t_whisp, dur=1.7, gain_db=-27, fade_in=0.4, fade_out=0.6)
    sc.sfx("coins", t_shock + 0.36, gain_db=-14, pan=0.05)
    sc.sfx("footsteps", t_g_walk, dur=gwalk.end(0) - t_g_walk, gain_db=-17, pan=0.4)
    sc.sfx("cloth", t_lead, gain_db=-15)
    sc.sfx("footsteps", t_lead_walk, dur=t_x1 - t_lead_walk + 0.2, gain_db=-16, pan=0.3)
    sc.sfx("drip", t_x0, dur=T - t_x0, gain_db=-21, fade_in=0.6, fade_out=0.8)
    sc.sfx("footsteps", t_in + 0.2, dur=t_arrive - t_in - 0.2, gain_db=-18, pan=-0.2)
    sc.sfx("thud", t_clang, gain_db=-5, pan=-0.4, duck_db=-3)
    sc.sfx("coins", t_clang + 0.02, gain_db=-11, pan=-0.4)
    sc.sfx("footsteps", g_t_go, dur=1.4, gain_db=-23, pan=-0.6)
    sc.sfx("chime", t_gold, gain_db=-10)
    sc.sfx("sparkle", t_gold + 0.6, gain_db=-14)
    return sc
