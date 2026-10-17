"""Scene 16 — the people of Nineveh believe God (Jonah 3:5), v2.

"你猜怎么样？尼尼微的人听了，竟然都相信了上帝！ / 他们禁食，就是不吃饭。大人小孩都换上粗粗的麻布衣服，向上帝认错，
表示愿意改。"

One 2400 x 1350 stage: the market square of Nineveh in the late afternoon (the same square s15 ends in: Jonah on
his stone step on the left, townspeople on the right), a herald on a stone plinth at the back, a market stall
with bread and fruit on the right.

  line 0  "你猜怎么样？"          calm: the people (still in their bright robes) stand worried, facing Jonah;
                                  the camera pushes in gently.
          "尼尼微的人听了，"      faces turn thoughtful one after the other (hand to chin).
          "竟然都相信了上帝！"    the surprise: eyes go wide, then they nod and lower their eyes (sorry); a few
                                  golden twinkles over the crowd; Jonah is surprised too ("!").
  line 1  "他们禁食，"            the herald turns, blows his horn and proclaims the fast (sound arcs).
          "就是不吃饭。"          a little girl reaches for the bread; the merchant throws a cloth over all his
                                  food; she pulls her hand back and nods; the oven smoke at the back dies away.
          "大人小孩都换上粗粗的麻布衣服，"  in little cloth-puffs, grown-ups first (elder, herald, mother, merchant,
                                  the rows behind) then the children, everyone changes into burlap sackcloth and
                                  stands with bowed head; the child wriggles in the scratchy cloth.
          "向上帝认错，"          they kneel in a wave, palms together, eyes downcast;
          "表示愿意改。"          their faces become peaceful and a soft warm hopeful light opens in the sky.
                                  Calm hold for the dissolve.

Pose changes are hard cuts (no crossfades between different drawings) hidden at the bottom of a squash-and-hop
or under a cloth-puff; expression-only changes are cuts as well. All times come from the narration chunks.
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

SW, SH = 2400, 1350
INK = P["ink"]

# ------------------------------------------------------------------ layout (stage px)
BACK_Y = 770                # back edge of the square (house fronts)
STEP_X0, STEP_X1 = 220, 660  # Jonah's stone step (two tiers)
STEP_TOP = 1000
J_X, J_Y, J_S = 440, STEP_TOP - 3, 1.0
PLINTH_X, PLINTH_TOP, PLINTH_BASE = 1250, 778, 846   # herald's plinth at the back of the square
H_X, H_S = 1250, 0.66
# the market stall is drawn in local coordinates (designed around x 1420.., table front edge y 1110) and placed
# with TABLE_K / TABLE_ORG
TABLE_K = 1.08
TABLE_ORG = (1444, 1120)    # stage position of the local point (1420, 1110) = the table's front-left corner


def tpt(lx, ly):
    """Local stall point -> stage."""
    return TABLE_ORG[0] + (lx - 1420) * TABLE_K, TABLE_ORG[1] + (ly - 1110) * TABLE_K


def tplace(body):
    return (f'<g transform="translate({TABLE_ORG[0]},{TABLE_ORG[1]}) scale({TABLE_K}) translate(-1420,-1110)">'
            f'{body}</g>')


TABLE_X0, TABLE_X1, TABLE_TOP, TABLE_BACK = 1420, 1890, 1110, 1080   # (local) table front edge / back edge
TABLE_FLOOR = 1215
R_X, R_Y, R_S = tpt(1668, 1160)[0], tpt(1668, 1160)[1], 1.06   # merchant, behind his table
E_X, E_Y, E_S = 800, 1232, 1.12    # elder
W_X, W_Y, W_S = 1140, 1245, 1.12   # mother
K_X, K_Y, K_S = 1392, 1254, 1.12   # her little girl
OVEN_X, OVEN_Y = 560, 784

CROWD = {   # (kind, variant, x, y, scale, facing in line 0, facing when kneeling)
    "back_l": [("man", 2, 690, 852, 0.56, -1, -1), ("woman", 1, 768, 858, 0.56, -1, 1),
               ("elder", 3, 846, 850, 0.56, -1, -1), ("child", 1, 912, 860, 0.56, -1, -1),
               ("man", 3, 982, 852, 0.56, -1, -1), ("woman", 0, 1058, 856, 0.56, -1, -1)],
    "back_r": [("man", 0, 1996, 852, 0.56, -1, -1), ("child", 0, 2066, 860, 0.56, -1, -1),
               ("elder", 1, 2136, 850, 0.56, -1, -1), ("woman", 3, 2210, 856, 0.56, -1, 1),
               ("man", 1, 2290, 852, 0.56, -1, -1)],
    "mid_l": [("woman", 2, 712, 978, 0.74, -1, -1), ("man", 1, 842, 984, 0.74, -1, -1),
              ("child", 3, 950, 990, 0.74, -1, -1), ("man", 3, 1376, 980, 0.74, -1, -1)],
    "mid_r": [("woman", 1, 2040, 982, 0.74, -1, -1), ("man", 3, 2168, 976, 0.74, -1, -1),
              ("elder", 2, 2296, 986, 0.74, -1, -1)],
}


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


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


def dip(tc, s, pv, depth=8):
    """Squash-and-hop that hides a pose cut at tc (the cut happens at the bottom of the squash)."""
    return hop(tc, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": 0.955}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pv, ["in", "out", "sine"])


def nod(t0, pv, deg=3.0, n=2, period=0.42):
    """Gentle nods: the whole figure bows a little from the feet, n times."""
    ks = [(0, {"rot": 0})]
    for i in range(n):
        ks += [(i * period + period * 0.45, {"rot": deg}), ((i + 1) * period, {"rot": 0})]
    return hop(t0, ks, pv)


# ============================================================================ backgrounds


def sky_svg():
    defs = (S.lin_grad("s16sky", [(0, "#a9c3d8"), (0.34, "#cfd5d6"), (0.62, "#f1dcb6"), (0.9, "#f7cf9a"),
                                  (1, "#f6c58e")]) +
            S.rad_grad("s16sun", [(0, "#fff6d6", 1), (0.18, "#ffe9b0", 0.9), (0.5, "#ffd793", 0.35),
                                  (1, "#ffcf88", 0)]))
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{BACK_Y + 60}" fill="url(#s16sky)"/>'
            f'<ellipse cx="2080" cy="560" rx="820" ry="560" fill="url(#s16sun)"/>')
    return doc(body, defs)


def clouds_svg(items, fill="#fff3df", shade="#f2d2a6"):
    body = ""
    for cx, cy, w, h, seed in items:
        body += S.cloud(cx, cy, w, h, fill, seed=seed, sw=3.2, shade_fill=shade)
    return doc(S.g(body, filter="wobble"))


def far_svg():
    defs = S.lin_grad("s16haze", [(0, "#f6dfb8", 0), (1, "#f6dfb8", 0.6)])
    body = PR.nineveh_skyline(-90, 2490, BACK_Y - 6, scale=0.86, seed=5, haze=0.46)
    body += f'<rect x="-20" y="{BACK_Y - 230}" width="{SW + 40}" height="232" fill="url(#s16haze)"/>'
    return doc(body, defs)


def square_svg():
    """Paved square, the row of houses at its back, Jonah's step and the herald's plinth (static)."""
    defs = (S.lin_grad("s16pave", [(0, "#e9cf9f"), (0.3, "#e6c793"), (1, "#d7b07a")]) +
            S.lin_grad("s16stone", [(0, "#ead3a6"), (1, "#d2b07c")]) +
            S.lin_grad("s16stonef", [(0, "#cda874"), (1, "#b48f5d")]))
    body = ""
    # houses along the back of the square
    houses = ""
    for x, v, fc in ((140, 1, 1), (420, 0, 1), (790, 3, -1), (1700, 2, -1), (2010, 0, -1), (2310, 1, -1)):
        houses += PR.house(x, BACK_Y + 4, 0.42, variant=v, facing=fc)
    # a clay bread oven (tannur) by the house on the left; its smoke is a separate layer
    oven = (f'<path d="M{OVEN_X - 46},{OVEN_Y} C{OVEN_X - 50},{OVEN_Y - 50} {OVEN_X - 30},{OVEN_Y - 78} '
            f'{OVEN_X - 14},{OVEN_Y - 80} L{OVEN_X + 14},{OVEN_Y - 80} C{OVEN_X + 30},{OVEN_Y - 78} '
            f'{OVEN_X + 50},{OVEN_Y - 50} {OVEN_X + 46},{OVEN_Y} Z" fill="#c9845a" stroke="{INK}" '
            f'stroke-width="3.5" stroke-linejoin="round"/>'
            f'<ellipse cx="{OVEN_X}" cy="{OVEN_Y - 80}" rx="16" ry="5" fill="#6d4630" stroke="{INK}" '
            f'stroke-width="3"/>'
            f'<path d="M{OVEN_X - 18},{OVEN_Y} L{OVEN_X - 18},{OVEN_Y - 26} A18,18 0 0 1 {OVEN_X + 18},'
            f'{OVEN_Y - 26} L{OVEN_X + 18},{OVEN_Y} Z" fill="#7a4a30" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{OVEN_X - 12},{OVEN_Y - 4} Q{OVEN_X},{OVEN_Y - 22} {OVEN_X + 12},{OVEN_Y - 4}" '
            f'fill="#f2a24c" opacity="0.85"/>')
    oven += PR.jar(OVEN_X + 74, OVEN_Y - 26, 0.36) + PR.sack(OVEN_X - 80, OVEN_Y + 4, 0.34, seed=2)
    # paved square with perspective joints
    plaza = (f'<path d="M-30,{BACK_Y} L{SW + 30},{BACK_Y} L{SW + 30},{SH + 30} L-30,{SH + 30} Z" '
             f'fill="url(#s16pave)" stroke="{INK}" stroke-width="3"/>')
    joints = ""
    vx, vy = 1250, 420
    y, k = BACK_Y + 24, 0
    while y < SH + 20:
        joints += f'<path d="M-30,{f1(y)} L{SW + 30},{f1(y)}"/>'
        k += 1
        y += 20 + k * 9
    for i in range(-16, 24):
        xb = vx + i * 230
        t0 = (BACK_Y - vy) / (SH + 40 - vy)
        joints += f'<path d="M{f1(vx + (xb - vx) * t0)},{BACK_Y} L{f1(xb)},{SH + 40}"/>'
    plaza += (f'<g stroke="{P["ink_soft"]}" stroke-width="2" opacity="0.2" fill="none" '
              f'stroke-linecap="round">{joints}</g>')
    # soft warm light pooling on the square from the low sun (right) and long shadows of the houses
    plaza += (f'<path d="M-30,{BACK_Y + 2} L{SW + 30},{BACK_Y + 2} L{SW + 30},{BACK_Y + 40} '
              f'C1600,{BACK_Y + 52} 800,{BACK_Y + 36} -30,{BACK_Y + 48} Z" fill="{P["ink"]}" opacity="0.07"/>')
    # Jonah's stone step (two tiers, blue glazed band like the one in s15)
    st = ""
    x0, x1 = STEP_X0, STEP_X1
    st += (f'<path d="M{x0},{STEP_TOP + 32} L{x0 + 26},{STEP_TOP + 12} L{x1 + 26},{STEP_TOP + 12} L{x1},'
           f'{STEP_TOP + 32} Z" fill="url(#s16stone)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
           f'<rect x="{x0}" y="{STEP_TOP + 32}" width="{x1 - x0}" height="44" fill="url(#s16stonef)" '
           f'stroke="{INK}" stroke-width="4"/>'
           f'<rect x="{x0}" y="{STEP_TOP + 48}" width="{x1 - x0}" height="16" fill="#3f79a8" stroke="{INK}" '
           f'stroke-width="3"/>')
    st += "".join(f'<circle cx="{xx}" cy="{STEP_TOP + 56}" r="4.5" fill="#f3e3b8"/>'
                  for xx in range(x0 + 20, x1, 34))
    u0, u1 = x0 + 60, x1 - 60
    st += (f'<path d="M{u0},{STEP_TOP + 4} L{u0 + 20},{STEP_TOP - 12} L{u1 + 20},{STEP_TOP - 12} L{u1},'
           f'{STEP_TOP + 4} Z" fill="url(#s16stone)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
           f'<rect x="{u0}" y="{STEP_TOP + 4}" width="{u1 - u0}" height="28" fill="url(#s16stonef)" '
           f'stroke="{INK}" stroke-width="4"/>')
    # herald's plinth: a two-tier stone block with a glazed rosette band
    px, pt, pb = PLINTH_X, PLINTH_TOP, PLINTH_BASE
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
    body += houses + S.g(oven, filter="wobble-fine") + S.g(plaza, filter="wobble")
    body += S.g(st, filter="wobble-fine") + S.g(pl, filter="wobble-fine")
    # ground shadows of the plinth and the step
    body += (f'<ellipse cx="{px}" cy="{pb + 4}" rx="150" ry="12" fill="{INK}" opacity="0.12" filter="url(#soft)"/>'
             f'<ellipse cx="{(x0 + x1) / 2}" cy="{STEP_TOP + 78}" rx="{(x1 - x0) / 2 + 30}" ry="14" fill="{INK}" '
             f'opacity="0.12" filter="url(#soft)"/>')
    return doc(body, defs)


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
    r = random.Random(4)
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


def palm_svg(x, y, s, lean):
    return doc(PR.palm_tree(x, y, s, lean=lean))


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
    """A striped woven cloth thrown over all the food on the table (the fast): lumps of the bread stack, the
    pomegranates, the dates and the grapes show through it."""
    x0, x1 = TABLE_X0, TABLE_X1
    top = [(x0 - 8, 1142), (x0 - 4, 1100), (1444, 1062), (1470, 1040), (1500, 1028), (1534, 1036), (1566, 1060),
           (1604, 1040), (1642, 1032), (1682, 1042), (1714, 1062), (1748, 1050), (1786, 1048), (1818, 1062),
           (1846, 1046), (1874, 1056), (x1 + 6, 1094), (x1 + 10, 1140)]
    hem = []
    n = 14
    for i in range(1, n):
        xx = x1 + 10 - (x1 + 18 - x0) * i / n
        hem.append((xx, 1140 + (7 if i % 2 else 0)))
    d = S.smooth_path(top + hem, closed=True, tension=0.8)
    cid = "s16cover"
    inner = (f'<path d="M{x0 - 20},1112 L{x1 + 20},1112 L{x1 + 20},1122 L{x0 - 20},1122 Z" '
             f'fill="{P["terracotta"]}"/>'
             f'<path d="M{x0 - 20},1128 L{x1 + 20},1128 L{x1 + 20},1133 L{x0 - 20},1133 Z" fill="#3f79a8"/>')
    for cx, cy, rx, ry in ((1505, 1040, 60, 18), (1642, 1036, 52, 14), (1772, 1052, 50, 10)):
        inner += f'<ellipse cx="{cx - 10}" cy="{cy - 4}" rx="{rx * 0.7}" ry="{ry * 0.6}" fill="#fff6e2" opacity="0.7"/>'
    for xx in (1570, 1716, 1820):
        inner += f'<path d="M{xx},1050 Q{xx + 4},1080 {xx - 2},1110" stroke="#cdb88e" stroke-width="10" ' \
                 f'fill="none" opacity="0.5" stroke-linecap="round"/>'
    body = (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="#eee0bf"/>'
            f'<g clip-path="url(#{cid})">{inner}</g>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    fringe = "".join(f'<path d="M{f1(xx)},{1143 + (4 if k % 2 else 0)} l{(k % 3) - 1},12" stroke="#c9a978" '
                     f'stroke-width="3.5" stroke-linecap="round"/>'
                     for k, xx in enumerate(range(x0 + 2, x1 + 6, 14)))
    folds = "".join(f'<path d="M{xx},1100 Q{xx + 6},1120 {xx - 2},1138"/>' for xx in (1462, 1590, 1700, 1836))
    body += fringe + f'<g stroke="#bda67c" stroke-width="3" fill="none" stroke-linecap="round">{folds}</g>'
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


def person(kind, variant, x, y, s, facing, pose, attire="normal", expr=None, shadow=True):
    sw = {"kneel_pray": 170}.get(pose, 110)
    if kind == "child":
        sw = 120 if pose == "kneel_pray" else 86
    out = C.ground_shadow(x, y, s, sw, opacity=0.2) if shadow else ""
    return out + C.citizen(x, y, s, facing, kind=kind, variant=variant, pose=pose, attire=attire, expr=expr)


def stick_on_ground(x, y, s, facing):
    """The elder's walking stick lying on the ground beside him while he kneels."""
    x0, x1 = x + facing * 30 * s, x + facing * 190 * s
    yy = y + 14 * s
    return (f'<path d="M{f1(x0)},{f1(yy)} L{f1(x1)},{f1(yy - 6 * s)}" stroke="{INK}" stroke-width="{12 * s:.1f}" '
            f'stroke-linecap="round"/><path d="M{f1(x0)},{f1(yy)} L{f1(x1)},{f1(yy - 6 * s)}" stroke="{P["wood"]}" '
            f'stroke-width="{6 * s:.1f}" stroke-linecap="round"/>')


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


def exclaim_svg(x, y, s=1.0):
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
    return doc(S.g(body, filter="wobble-fine"))


def smoke_svg(cx, cy, r, seed):
    return doc(f'<path d="{S.blob(cx, cy, r, r * 0.8, 0.18, 9, seed)}" fill="#efe6da" stroke="{P["ink_soft"]}" '
               f'stroke-width="2.5" opacity="0.75" filter="url(#wobble-fine)"/>')


def glaze_svg(kind):
    if kind == "dusk":      # solemn evening: rosy-lilac sky, slightly dimmer square (multiply)
        stops = [(0, "#bfa0c4", 0.42), (0.4, "#dcb4b4", 0.26), (0.62, "#e9bfa8", 0.16), (1, "#efc6a2", 0.1)]
        defs = S.lin_grad("s16dusk", stops)
        return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s16dusk)"/>', defs)
    # hope: a warm golden glow opening in the sky above the kneeling people (screen)
    defs = S.rad_grad("s16hope", [(0, "#ffe9b0", 0.95), (0.3, "#ffd98e", 0.6), (0.62, "#ffcf80", 0.22),
                                  (1, "#ffcf80", 0)])
    return doc(f'<ellipse cx="1220" cy="120" rx="1500" ry="980" fill="url(#s16hope)"/>', defs)


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
    t_believe = c0b.start + 0.95             # "都相信了上帝": they nod and lower their eyes
    t_horn = snap(c0b.end - 0.1)             # the herald turns and lifts his horn
    t_call = snap(c1a.start + 0.25)          # "他们禁食": he proclaims the fast
    t_reach = snap(c1a.start + 0.55)         # the little girl reaches for the bread
    t_nofood = within(c1a, 0.49)             # "就是不吃饭": the cloth goes over the food
    t_cover = snap(t_nofood)
    t_back = snap(t_cover + 0.42)            # she pulls her hand back
    t_okay = snap(t_back + 0.7)              # and nods
    t_change = c1b.start + 0.1               # "大人小孩都换上…": sackcloth wave (grown-ups first)
    t_kid = within(c1b, 0.22)                # "小孩": the children
    t_rough = within(c1b, 0.55)              # "粗粗的麻布衣服": scratchy!
    t_kneel = c1c.start + 0.12               # "向上帝认错": kneel in a wave
    t_hope = within(c1c, 0.54)               # "表示愿意改": peaceful faces, hopeful light

    # ---- sky, sun, clouds, far city ----
    # sky + far city are one static group; the clouds drift in front of it, high above the skyline
    sc.add("sky", sky_svg(), z=0, wc=0.6)
    sc.add("far", far_svg(), z=0.5)
    sc.add("clouds_hi", clouds_svg([(380, 150, 420, 120, 3), (1180, 90, 340, 100, 4), (1960, 170, 380, 110, 5)]),
           z=1, motion=M.drift(vx=6))
    sc.add("clouds_lo", clouds_svg([(930, 250, 250, 74, 6), (1640, 290, 230, 70, 7)], "#fbead2", "#efc9a0"),
           z=1.2, motion=M.drift(vx=-4))

    # doves gliding far over the roofs (sparse, slow)
    fr_r, fr_l = dove_frames(1), dove_frames(-1)
    for i, (fc, x0, y0, x1, y1, ta, tb, rate, ph) in enumerate((
            (1, -80, 330, 900, 250, 0.0, 9.0, 9, 0.0),
            (1, -200, 380, 700, 300, 1.0, 10.5, 10, 0.4),
            (-1, 2500, 280, 1500, 200, 8.0, T + 0.5, 9, 0.2))):
        def mot(t, x0=x0, y0=y0, x1=x1, y1=y1, ta=ta, tb=tb, ph=ph):
            u = (t - ta) / (tb - ta)
            a = 1.0 if ta <= t <= tb else 0.0
            return Tf(dx=x0 + (x1 - x0) * u - DOVE_REF[0], dy=y0 + (y1 - y0) * u - DOVE_REF[1]
                      + 10 * math.sin(t * 2.2 + ph * 6), alpha=a)
        sc.add(f"dove{i}", fr_r if fc > 0 else fr_l, z=2.5 + 0.01 * i, seed=700 + i,
               frame_at=wing_cycle(rate, ph, glide=(ta + 1.5, ta + 3.2)), motion=mot)

    # ---- square (static), palms (gentle sway), oven smoke (dies away at the fast) ----
    sc.add("square", square_svg(), z=3)
    for i, (x, s, ln) in enumerate(((640, 0.5, -0.1), (1480, 0.46, 0.08), (2170, 0.52, -0.06))):
        sc.add(f"palm{i}", palm_svg(x, BACK_Y + 2, s, ln), z=2.8,
               motion=M.sway(0.7, 4.2 + i * 0.6, pivot=(x, BACK_Y), phase=i * 0.3))

    smoke_stop = t_cover + 0.3
    for i in range(4):
        per, ph = 3.2, i / 4

        def smot(t, per=per, ph=ph, i=i):
            u = (t / per + ph) % 1.0
            born = t - u * per
            if born > smoke_stop:
                return Tf(alpha=0)
            return Tf(dx=18 * u + 8 * math.sin(t * 1.3 + i), dy=-170 * u, sx=0.6 + 0.8 * u, sy=0.6 + 0.8 * u,
                      alpha=0.85 * math.sin(math.pi * u), px=OVEN_X, py=OVEN_Y - 90)
        sc.add(f"smoke{i}", smoke_svg(OVEN_X, OVEN_Y - 96, 22, 50 + i), z=2.9, wc=0.4, motion=smot)

    # ---- crowd groups: stand worried -> listen -> sorry (believe) -> sackcloth (sad) -> kneel sorry -> peaceful
    def group_frames(members, turn):
        out = []
        for st in range(7):
            body = ""
            for j, (kind, v, x, y, s, f0, f1_) in enumerate(members):
                if st == 0:
                    body += person(kind, v, x, y, s, f0, "stand", expr="worried")
                elif st == 1:       # "你猜怎么样？": some turn to their neighbour
                    body += person(kind, v, x, y, s, -f0 if j % 2 == turn else f0, "stand", expr="worried")
                elif st == 2:
                    body += person(kind, v, x, y, s, f0, "listen")
                elif st == 3:
                    body += person(kind, v, x, y, s, f0, "stand", expr="sorry")
                elif st == 4:
                    body += person(kind, v, x, y, s, f0, "sad", "sackcloth")
                elif st == 5:
                    body += person(kind, v, x, y, s, f1_, "kneel_pray", "sackcloth", "sorry")
                else:
                    body += person(kind, v, x, y, s, f1_, "kneel_pray", "sackcloth", "peaceful")
            out.append(doc(body))
        return out

    gtimes = {   # (turn to the neighbour or None, listen, sorry, sackcloth, kneel, peaceful)
        "back_l": (c0a.start + 0.45, t_heard + 0.25, t_believe + 0.15, t_change + 0.66, t_kneel + 0.42,
                   t_hope + 0.2),
        "back_r": (c0a.start + 0.75, t_heard + 0.4, t_believe + 0.3, t_change + 1.1, t_kneel + 0.62, t_hope + 0.3),
        "mid_l": (None, t_heard + 0.1, t_believe + 0.05, t_change + 0.46, t_kneel + 0.3, t_hope + 0.1),
        "mid_r": (c0a.start + 0.6, t_heard + 0.5, t_believe + 0.35, t_change + 1.3, t_kneel + 0.78, t_hope + 0.4),
    }
    zrow = {"back_l": 10, "back_r": 10.1, "mid_l": 12, "mid_r": 12.1}
    puffs_at = []
    group_puffs = []
    for name, members in CROWD.items():
        frames = group_frames(members, 1 if name != "mid_r" else 0)
        gx = sum(m[2] for m in members) / len(members)
        gy = max(m[3] for m in members)
        s = members[0][4]
        tt, a, b, c, d, e = (snap(x) if x is not None else None for x in gtimes[name])
        sched = [(0, 0)] + ([(tt, 1)] if tt is not None else []) + [(a, 2), (b, 3), (c, 4), (d, 5), (e, 6)]
        parts = [dip(a, s, (gx, gy), 4), nod(b + 0.05, (gx, gy), 1.2, 2), dip(d, s, (gx, gy)),
                 M.breathe(0.007, 3.4, pivot=(gx, gy), phase=len(name) * 0.13)]
        if tt is not None:
            parts.append(dip(tt, s, (gx, gy), 3))
        sc.add(f"crowd_{name}", frames, z=zrow[name], frame_at=cuts(sched), motion=M.combine(*parts))
        body = ""
        for j, (kind, v, x, y, s_, f0, _) in enumerate(members):
            hh = {"child": 215, "elder": 320}.get(kind, 330) * s_
            body += small_puff(x, y, hh, seed=40 + j + 7 * len(name))
        group_puffs.append((name, c, body, (gx, gy - 150 * s)))

    # ---- Jonah on his step: watches; surprised at "竟然" ----
    jp = (J_X, J_Y)
    jsh = C.ground_shadow(J_X, J_Y, J_S, 120)
    jfr = [doc(jsh + C.jonah(J_X, J_Y, J_S, 1, pose="stand")),
           doc(jsh + C.jonah(J_X, J_Y, J_S, 1, pose="stand", expr="surprised"))]
    tj1, tj2 = snap(t_wow + 0.1), snap(t_wow + 1.5)
    sc.add("jonah", jfr, z=9, frame_at=cuts([(0, 0), (tj1, 1), (tj2, 0)]),
           motion=M.combine(hop(tj1, [(0, {"dy": 0}), (0.1, {"dy": -8}), (0.24, {"dy": 0})], jp),
                            M.breathe(0.008, 3.1, pivot=jp, phase=0.2)))
    jh = C.body_points(C.jonah, J_X, J_Y, J_S, 1, pose="stand")["head_top"]
    exx, exy = jh[0] + 60, jh[1] + 10
    sc.add("jonah_wow", exclaim_svg(exx, exy, 0.9), z=30, wc=0, motion=M.keys(
        [(tj1 - 0.02, {"alpha": 0, "s": 0.4}), (tj1 + 0.25, {"alpha": 1, "s": 1}), (tj2 - 0.3, {"alpha": 1}),
         (tj2, {"alpha": 0})], ["back", "linear", "sine"], pivot=(exx, exy)))

    # ---- the herald on his plinth ----
    hp = (H_X, PLINTH_TOP)
    hsh = C.ground_shadow(H_X, PLINTH_TOP, H_S, 110)

    def herald(facing, pose, attire="normal", expr=None, extra=""):
        return doc(hsh + C.citizen(H_X, PLINTH_TOP, H_S, facing, kind="man", variant=0, pose=pose, attire=attire,
                                   expr=expr) + extra)
    hhead = C.body_points(C.citizen, H_X, PLINTH_TOP, H_S, 1, kind="man", variant=0, pose="listen")["head"]
    horn = horn_svg(hhead[0] + 15 * H_S, hhead[1] + 20 * H_S, H_S, 1)
    hfr = [herald(-1, "stand", expr="worried"), herald(-1, "listen"), herald(-1, "stand", expr="sorry"),
           herald(1, "listen", expr="neutral", extra=horn), herald(1, "point", expr="call"),
           herald(1, "sad", "sackcloth"), herald(1, "kneel_pray", "sackcloth", "sorry"),
           herald(1, "kneel_pray", "sackcloth", "peaceful")]
    th = [snap(t_heard + 0.3), snap(t_believe + 0.2), t_horn, t_call, snap(t_change + 0.36), snap(t_kneel + 0.52),
          snap(t_hope + 0.25)]
    sc.add("herald", hfr, z=11, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(th)]),
           motion=M.combine(dip(th[0], H_S, hp, 4), nod(th[1] + 0.05, hp, 1.5, 2), dip(t_horn, H_S, hp),
                            hop(t_horn + 0.3, [(0, {"rot": 0}), (0.4, {"rot": -2.5}), (0.9, {"rot": -2.5}),
                                               (1.1, {"rot": 0})], hp),
                            dip(t_call, H_S, hp), dip(th[5], H_S, hp),
                            M.breathe(0.009, 2.9, pivot=hp, phase=0.4)))
    hb = C.body_points(C.citizen, H_X, PLINTH_TOP, H_S, 1, kind="man", variant=0, pose="point")["head"]
    sc.add("herald_arcs", [arcs_svg(hb[0] + 34 * H_S, hb[1] + 14 * H_S, 1, k, 1.0) for k in (1, 2, 3)], z=30, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(t_call, {"alpha": 0}), (t_call + 0.15, {"alpha": 1}), (t_change - 0.25, {"alpha": 1}),
                          (t_change, {"alpha": 0})], "sine"))
    puffs_at.append((th[4], H_X, PLINTH_TOP - 110 * H_S * 1.4, 0.45 * 310 * H_S, 0.6 * 310 * H_S, H_S))

    # ---- market stall: back posts, merchant, table with food, the cover cloth, awning ----
    sc.add("stall_back", stall_back_svg(), z=13)
    rp = (R_X, R_Y)

    def merchant(pose, attire="normal", expr=None):
        return doc(C.citizen(R_X, R_Y, R_S, -1, kind="man", variant=1, pose=pose, attire=attire, expr=expr))
    rfr = [merchant("stand", expr="worried"), merchant("listen"), merchant("listen", expr="surprised"),
           merchant("stand", expr="sorry"), merchant("point", expr="neutral"), merchant("stand", expr="sorry"),
           merchant("sad", "sackcloth"), merchant("kneel_pray", "sackcloth", "sorry"),
           merchant("kneel_pray", "sackcloth", "peaceful")]
    tr = [snap(t_heard + 0.05), snap(t_wow + 0.05), snap(t_believe), snap(t_cover - 0.12), snap(t_cover + 0.55),
          snap(t_change + 0.9), snap(t_kneel + 0.36), snap(t_hope + 0.15)]
    sc.add("merchant", rfr, z=14, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tr)]),
           motion=M.combine(dip(tr[0], R_S, rp, 4), nod(tr[2] + 0.05, rp, 2.0, 2), dip(tr[3], R_S, rp),
                            dip(tr[4], R_S, rp, 4), dip(tr[6], R_S, rp), M.breathe(0.008, 3.3, pivot=rp, phase=0.7)))
    puffs_at.append((tr[5], R_X, R_Y - 200, 120, 150, R_S))
    sc.add("table", table_svg(), z=15)
    cp = tpt((TABLE_X0 + TABLE_X1) / 2, TABLE_TOP)
    ap = tpt((TABLE_X0 + TABLE_X1) / 2, 714)
    sc.add("cover", cover_svg(), z=15.5, motion=M.keys(
        [(t_cover - 0.02, {"alpha": 0, "dy": -70, "sx": 0.9, "sy": 0.7}),
         (t_cover + 0.06, {"alpha": 1}),
         (t_cover + 0.32, {"dy": 0, "sx": 1.0, "sy": 1.0}),
         (t_cover + 0.42, {"sx": 1.02, "sy": 0.95}),
         (t_cover + 0.58, {"sx": 1.0, "sy": 1.0})], ["linear", "in", "out", "sine"], pivot=cp))
    sc.add("awning", awning_svg(), z=16, motion=lambda t: Tf(sy=1 + 0.006 * math.sin(t * 2.3), px=ap[0], py=ap[1]))

    # ---- the four in front: the elder, the mother, her little girl (and the merchant behind his table) ----
    ep = (E_X, E_Y)

    def elder(pose, attire="normal", expr=None, stick=False):
        st = stick_on_ground(E_X, E_Y, E_S, -1) if stick else ""
        return doc(st + person("elder", 0, E_X, E_Y, E_S, -1, pose, attire, expr))
    efr = [elder("stand", expr="worried"), elder("listen"), elder("listen", expr="surprised"),
           elder("stand", expr="sorry"), elder("sad", "sackcloth"),
           elder("kneel_pray", "sackcloth", "sorry", True), elder("kneel_pray", "sackcloth", "peaceful", True)]
    te = [snap(t_heard - 0.1), snap(t_wow), snap(t_believe - 0.05), snap(t_change), snap(t_kneel),
          snap(t_hope)]
    sc.add("elder", efr, z=20, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(te)]),
           motion=M.combine(dip(te[0], E_S, ep, 5), hop(te[1], [(0, {"dy": 0}), (0.1, {"dy": -7}), (0.22, {"dy": 0})],
                                                         ep),
                            nod(te[2] + 0.05, ep, 2.4, 2), dip(te[4], E_S, ep, 10),
                            M.breathe(0.008, 3.6, pivot=ep, phase=0.1)))
    puffs_at.append((te[3], E_X, E_Y - 160, 130, 180, E_S))

    wp = (W_X, W_Y)

    def mother(pose, attire="normal", expr=None):
        return doc(person("woman", 3, W_X, W_Y, W_S, -1, pose, attire, expr))
    wfr = [mother("stand", expr="worried"), mother("listen"), mother("listen", expr="surprised"),
           mother("stand", expr="sorry"), mother("sad", "sackcloth"), mother("kneel_pray", "sackcloth", "sorry"),
           mother("kneel_pray", "sackcloth", "peaceful")]
    tw = [snap(t_heard + 0.15), snap(t_wow + 0.08), snap(t_believe + 0.1), snap(t_change + 0.23),
          snap(t_kneel + 0.2), snap(t_hope + 0.05)]
    sc.add("mother", wfr, z=20.5, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tw)]),
           motion=M.combine(dip(tw[0], W_S, wp, 5), hop(tw[1], [(0, {"dy": 0}), (0.1, {"dy": -7}), (0.22, {"dy": 0})],
                                                         wp),
                            nod(tw[2] + 0.05, wp, 2.4, 2), dip(tw[4], W_S, wp, 10),
                            M.breathe(0.009, 3.2, pivot=wp, phase=0.5)))
    puffs_at.append((tw[3], W_X, W_Y - 160, 125, 175, W_S))

    kp = (K_X, K_Y)

    def kid(pose, facing=-1, attire="normal", expr=None):
        return doc(person("child", 1, K_X, K_Y, K_S, facing, pose, attire, expr))
    kfr = [kid("stand", expr="worried"), kid("listen"), kid("listen", expr="surprised"), kid("stand", expr="sorry"),
           kid("point", 1, expr="happy"), kid("stand", 1, expr="surprised"), kid("stand", 1, expr="sorry"),
           kid("sad", -1, "sackcloth"), kid("kneel_pray", -1, "sackcloth", "sorry"),
           kid("kneel_pray", -1, "sackcloth", "peaceful")]
    tk = [snap(t_heard + 0.3), snap(t_wow + 0.15), snap(t_believe + 0.2), t_reach, t_back, t_okay, snap(t_kid),
          snap(t_kneel + 0.28), snap(t_hope + 0.12)]
    sc.add("kid", kfr, z=21, frame_at=cuts([(0, 0)] + [(tt, i + 1) for i, tt in enumerate(tk)]),
           motion=M.combine(dip(tk[0], K_S, kp, 4), hop(tk[1], [(0, {"dy": 0}), (0.1, {"dy": -8}), (0.22, {"dy": 0})],
                                                         kp),
                            nod(tk[2] + 0.05, kp, 3, 2), dip(t_reach, K_S, kp, 5),
                            hop(t_back, [(0, {"dy": 0, "rot": 0}), (0.08, {"dy": -10, "rot": -3}),
                                         (0.22, {"dy": 0, "rot": 0})], kp),
                            nod(t_okay + 0.05, kp, 4, 2, 0.36),
                            # scratchy sackcloth: a little wriggle
                            hop(t_rough, [(0, {"rot": 0}), (0.12, {"rot": 3}), (0.24, {"rot": -3}),
                                          (0.36, {"rot": 2.5}), (0.48, {"rot": -2}), (0.6, {"rot": 0})], kp),
                            dip(tk[7], K_S, kp, 8), M.breathe(0.012, 2.6, pivot=kp, phase=0.3)))
    puffs_at.append((tk[6], K_X, K_Y - 110, 90, 120, K_S))

    # ---- cloth-puffs over every sackcloth change ----
    for i, (tp, x, y, rx, ry, s) in enumerate(puffs_at):
        sc.add(f"puff{i}", doc(puff_svg(x, y, rx, ry, seed=i + 3, k=max(0.6, s))), z=25 + 0.01 * i, wc=0.5,
               motion=puff_motion(tp, (x, y)))

    for name, tp, body, pv in group_puffs:
        sc.add(f"puffs_{name}", doc(body), z=25.5, wc=0.5, motion=hop(tp, [
            (-0.06, {"alpha": 0, "s": 0.97, "dy": 0}), (0.02, {"alpha": 1, "s": 0.99, "dy": -3}),
            (0.16, {"alpha": 0.85, "s": 1.015, "dy": -9}), (0.38, {"alpha": 0, "s": 1.03, "dy": -18})], pv,
            ["out", "sine", "in"]))

    # ---- foreground framing ----
    fg = (well_svg(450, 1312) + PR.grass_tuft(40, SH + 4, 1.1, variant=2) + PR.jar(150, SH - 40, 0.9)
          + PR.jar(232, SH - 20, 0.62)
          + PR.grass_tuft(2330, SH + 6, 1.0, variant=0) + PR.bush(2410, SH + 10, 0.9, variant=1))
    sc.add("fg", doc(fg), z=29)

    # ---- light: solemn dusk glaze while they change and kneel, then a soft hopeful glow ----
    sc.add("dusk", glaze_svg("dusk"), z=40, wc=0, blend="multiply",
           motion=M.keys([(t_change - 0.4, {"alpha": 0}), (t_kneel + 0.5, {"alpha": 1}),
                          (t_hope, {"alpha": 1}), (t_hope + 1.6, {"alpha": 0.55})], "sine"))
    sc.add("hope", glaze_svg("hope"), z=41, wc=0, blend="screen",
           motion=M.combine(M.keys([(t_hope - 0.2, {"alpha": 0}), (t_hope + 1.4, {"alpha": 1})], "sine"),
                            M.pulse(0.85, 1.0, 3.0)))

    # ---- camera ----
    A = Cam(1130, 815, 1800)
    B = Cam(1080, 850, 1640)
    Cw = Cam(1160, 800, 1860)
    D = Cam(1060, 880, 1560)
    E = Cam(1180, 750, 2120)
    sc.camera = M.cam_keys([
        (0, A), (c0a.start, A), (t_believe + 0.6, B), (t_horn - 0.2, B), (t_cover + 0.9, Cw), (t_change + 1.2, Cw),
        (t_rough + 0.75, D), (t_kneel + 0.3, D), (t_hope + 0.6, E), (T, Cam(1186, 748, 2100)),
    ], ["sine", "sine", "sine", "inout", "sine", "inout", "sine", "inout", "sine"])

    # ---- effects ----
    sc.fx = [
        FX.motes((0, 300, SW, 1200), count=26, t0=-1, t1=T + 1, color=(255, 238, 200), size=(3, 6), alpha=110,
                 seed=31),
        FX.sparkles((600, 560, 2000, 900), count=14, t0=t_believe - 0.2, t1=t_believe + 1.6, color=(255, 236, 170),
                    size=(8, 16), drift=-14, seed=33),
        FX.sparkles((700, 240, 1800, 760), count=12, t0=t_hope + 0.3, t1=T + 1, color=(255, 232, 160),
                    size=(7, 14), drift=-10, period=2.2, seed=37),
    ]

    # ---- sound ----
    sc.sfx("crowd", 0, dur=t_change + 1.0, gain_db=-20, fade_in=0.8, fade_out=1.4)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("sparkle", t_believe, gain_db=-15)
    sc.sfx("horn", t_horn + 0.15, gain_db=-13, pan=0.1)
    sc.sfx("cloth", t_cover, gain_db=-9, pan=0.4)
    sc.sfx("cloth", t_change + 0.05, gain_db=-12, pan=-0.2)
    sc.sfx("cloth", t_kid, gain_db=-12, pan=0.2)
    sc.sfx("sparkle", t_hope + 0.3, gain_db=-14)
    return sc
