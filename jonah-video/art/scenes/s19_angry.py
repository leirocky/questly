"""Scene 19 — Jonah is angry (Jonah 4:1-4).

Outside Nineveh on a sunny afternoon, one 2800 x 1575 stage, no cuts. West (left): the great city, saved and
joyful — its mud-brick wall with the open gate, banners and bunting, the ziggurat and rooftops behind, people
cheering on the wall walk, children hopping and grown-ups waving on the green plain outside the gate, sheep,
doves. East (right): a dry rocky knoll where Jonah stands with his back to the city.

  line 0  "大家都很高兴，" the joyful city (wide). "只有约拿一点儿也不高兴。" the camera glides right to Jonah:
          arms crossed, scowling, a grumpy huff (steam puffs). "他非常生气，" he stamps (anger mark, puffs);
          "对上帝说：" he lifts his face to heaven.
  line 1  "耶和华啊，" both arms up to heaven; "我早就知道会这样！" arms flung wide; "所以我才急忙逃到他施去。"
          a thought bubble pops up beside him: a small flashback of himself running down the pier at Joppa and
          leaping aboard the striped-sail ship, which sails off west.
  line 2  "因为我知道，你又慈爱，又宽容，" palms out; a warm golden memory bubble with a glowing heart (God's
          kindness — never a figure) that beats on "慈爱" and "宽容"; "你说要降下的灾祸，" a little grey storm
          cloud gathers over a tiny Nineveh in the bubble; "只要人一认错，你就不忍心降下来。" the heart's light
          melts the cloud away and the tiny city glows; Jonah crosses his arms and huffs.
  line 3  "原来，" he plops down on the knoll (thud, dust), sulking; the camera eases back to show the happy city
          behind him (doves fly home over it); "可是他不愿意上帝饶恕他们，" he side-eyes the cheering city;
          "所以当初才逃跑了。" a huff, eyes front again.
  line 4  "于是，上帝问约拿：" the clouds above him part and gentle golden light pours down on him (chime,
          sparkles); the camera eases in and tilts up into the light.
  line 5  "约拿，你这样生气，对吗？" the light glows softly with the words; Jonah looks up into it, surprised —
          then turns his back to the light (a hop-turn) and sulks toward the city without answering. Calm hold.

Pose changes are hard cuts hidden by a squash-and-hop (dust poof, pop lines) as in v1 s11, and the sit-down
is a "plop" (squash, cut, short drop, landing squash); nothing crossfades between two different drawings of
Jonah. While his arms are crossed he fidgets with a slow grumpy sway. Bubble contents move inside the bubble's
own pop transform, and the puffy ring is drawn ON TOP of the contents (window cut out), so the flashback ship
can sail off behind it. God's light: the cloud bank drifts in from the east during line 3 (the thought
bubbles use that sky before), then parts in line 4. All timings come from ctx.lines / chunks (phrase
positions inside a chunk are estimated from the character index, so they follow a re-generated voice).
Camera: few long sine moves, peak ~11 output px / frame.
"""
import math
import random
import re

from art import characters as CH
from art import props as PR
from art import style as S
from art.style import P
from art.scenes_v1 import s02_call as V2
from art.scenes_v1 import s10_repent as V10
from art.scenes_v1 import s11_vine as V11
from art.scenes_v1 import s12_lesson as V12
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

# ------------------------------------------------------------------ layout (stage px)
SW, SH = 2800, 1575
HZ = 900                     # far horizon
WY, WH = 1030, 260           # city wall ground line, height
GX, GW = 860, 200            # gate centre, width
WX1 = 1540                   # right end of the wall; the corner tower stands there
TOWER = (WX1 + 50, 150)      # corner tower centre x, width
JX, JS = 1850, 1.2           # Jonah
BX, BY, RX, RY = 2300, 525, 262, 156      # thought-bubble window (centre, radii)
GAP = (2230, 262)            # where the clouds part for God's light
SUN = (330, 330)
INK = P["ink"]


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


KNOLL = [(1180, 1420), (1290, 1300), (1480, 1238), (1680, 1200), (1900, 1186), (2150, 1176), (2450, 1166),
         (2900, 1150)]


def knoll_y(x):
    for (x0, y0), (x1, y1) in zip(KNOLL, KNOLL[1:]):
        if x0 <= x <= x1:
            u = (x - x0) / (x1 - x0)
            u = 0.5 - 0.5 * math.cos(math.pi * u)
            return y0 + (y1 - y0) * u
    return KNOLL[-1][1]


JY = knoll_y(JX)


def phrase_t(line, phrase):
    """Start of ``phrase`` inside its subtitle chunk, estimated by its character index in that chunk."""
    for c in line.chunks:
        i = c.text.find(phrase)
        if i >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、")))
            return c.start + (c.end - c.start) * i / n
    raise KeyError(phrase)


# ------------------------------------------------------------------ Jonah (library + scene-local poses)
_CROSS = (("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1))
LOCAL_POSES = {
    "cross": CH._P(h=10, legs=((6, 2), (-6, -2)), arms=_CROSS, far_front=True, expr="angry"),
    "cross_up": CH._P(t=-4, h=-14, legs=((6, 2), (-6, -2)), arms=_CROSS, far_front=True, expr="angry",
                      look=(0.03, -0.08)),
    "complain": CH._P(t=-6, h=-18, legs=((8, 3), (-7, -3)), arms=(("fk", 130, 160), ("fk", -125, -155)),
                      hands=("open", "open"), expr="angry", look=(0.02, -0.08)),
    "complain2": CH._P(t=-5, h=-16, legs=((8, 3), (-7, -3)), arms=(("fk", 100, 140), ("fk", -100, -140)),
                       hands=("open", "open"), expr="angry", look=(0.02, -0.08)),
    "shrug": CH._P(t=-2, h=-10, legs=((8, 3), (-7, -3)), arms=(("fk", 40, 110), ("fk", -40, -110)),
                   hands=("open", "open"), expr="angry"),
    "sulk_eye": CH._P(t=-2, h=8, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True, expr="angry",
                      look=(-0.06, 0.0), **CH._SEATED),
    "sulk_up": CH._P(t=-2, h=-14, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True,
                     expr="surprised", look=(0.03, -0.08), **CH._SEATED),
}


def jfig(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    if pose not in LOCAL_POSES:
        return CH.jonah(x, y, scale, facing, pose=pose, expr=expr, marks=marks)
    ps = dict(LOCAL_POSES[pose])
    CH._check_expr(expr, "jonah")
    inner, _ = CH._figure(CH._jonah_design(), CH._ADULT, ps, expr or ps["expr"], CH._fsign(facing), marks)
    return CH._wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")


# ------------------------------------------------------------------ sky
def sky_svg():
    defs = (S.lin_grad("sky", [(0, "#86c0da"), (0.3, "#b9dde3"), (0.5, "#e9ead2"), (0.58, "#f8e4b8"),
                               (1, "#f6d9a4")]) +
            S.rad_grad("cityglow", [(0, "#fff4cf", 0.9), (0.45, "#ffe4a6", 0.42), (1, "#ffd98a", 0)]) +
            S.rad_grad("sunglow", [(0, "#fffbe8", 0.95), (0.35, "#fff1c4", 0.5), (1, "#ffe9b0", 0)]))
    body = S.rect_bg("url(#sky)", SW, SH)
    body += '<ellipse cx="760" cy="600" rx="1100" ry="560" fill="url(#cityglow)"/>'
    body += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="330" fill="url(#sunglow)"/>'
    return doc(body, defs)


def sun_svg():
    x, y = SUN
    body = S.g(f'<circle cx="{x}" cy="{y}" r="66" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.25)}" '
               f'stroke-width="4"/><circle cx="{x - 20}" cy="{y - 20}" r="22" fill="#fff6d0" opacity="0.7"/>',
               filter="wobble")
    return doc(body)


def sun_rays_svg():
    x, y = SUN
    d = S.rays(x, y, 92, 150, n=12, width_deg=9)
    return doc(f'<path d="{d}" fill="#ffe7a0" opacity="0.75" filter="url(#soft)"/>')


def cloud_svg(cx, cy, w, h, seed):
    return doc(S.g(S.cloud(cx, cy, w, h, "#fdf6e8", seed=seed, sw=3, shade_fill="#efdcc4"), filter="wobble"))


LEFT_BANK = [(-330, 52, 54), (-262, 18, 76), (-170, -14, 96), (-72, 4, 84), (2, 34, 58), (-214, 52, 56),
             (-110, 50, 60)]
RIGHT_BANK = [(30, 40, 50), (104, 6, 74), (200, -24, 96), (300, -2, 82), (372, 34, 56), (160, 52, 56),
              (276, 52, 58)]


def bank_svg(rel, gold, uid):
    gx, gy = GAP
    circles = [(gx + dx, gy + dy, r) for dx, dy, r in rel]
    base = S.mix("#f7efe2", "#ffe2a0", 0.5 * gold)
    hi = S.mix("#fffaf0", "#fff4cf", 0.6 * gold)
    under = S.mix("#e2d3c8", "#f2c27a", 0.55 * gold)
    glow = (gx, gy + 20, 240, 0.75 * gold) if gold > 0 else None
    return doc(S.g(V2._cumulus(circles, base, hi, under, glow=glow, uid=f"{uid}{int(gold * 10)}"), filter="wobble"))


def heaven_glow_svg():
    gx, gy = GAP
    defs = S.rad_grad("hg", [(0, "#fffbec", 0.95), (0.25, "#fff0c0", 0.7), (0.6, "#ffd98a", 0.28), (1, "#ffd27a", 0)])
    body = f'<ellipse cx="{gx}" cy="{gy + 30}" rx="560" ry="330" fill="url(#hg)"/>'
    body += f'<ellipse cx="{gx}" cy="{gy + 30}" rx="200" ry="110" fill="#fffaf0" opacity="0.55" filter="url(#blur-md)"/>'
    return doc(body, defs)


# ------------------------------------------------------------------ land
def far_svg():
    far1, far2 = "#e7d8be", "#dccba9"
    body = V2._ridge([(-60, 905), (300, 866), (700, 882), (1100, 858), (1500, 878), (1900, 846), (2300, 870),
                      (2860, 852)], far1, 2.5, S.mix(INK, far1, 0.55), bottom=HZ + 120)
    body += V2._ridge([(1450, 925), (1800, 892), (2150, 906), (2500, 884), (2860, 896)], far2, 2.5,
                      S.mix(INK, far2, 0.5), bottom=HZ + 140)
    for x, y, s in [(1760, 905, 0.22), (1830, 910, 0.18), (2440, 898, 0.2), (2560, 903, 0.17)]:
        body += PR.palm_tree(x, y, s, dates=False)
    city = PR.nineveh_skyline(-80, 1680, 905, scale=1.0, seed=2, haze=0.3, tint="#f4e0bc")
    return doc(S.g(body, filter="wobble") + city)


def merlon_pts(mx, top, mw, k):
    st = 11 * k
    return [(mx, top), (mx, top - st), (mx + mw * 0.2, top - st), (mx + mw * 0.2, top - 2 * st),
            (mx + mw * 0.4, top - 2 * st), (mx + mw * 0.4, top - 3 * st), (mx + mw * 0.6, top - 3 * st),
            (mx + mw * 0.6, top - 2 * st), (mx + mw * 0.8, top - 2 * st), (mx + mw * 0.8, top - st),
            (mx + mw, top - st), (mx + mw, top)]


def corner_tower(cx, y, h, w):
    col = P["sand"]
    x0, x1, top = cx - w / 2, cx + w / 2, y - h
    st = f'stroke="{INK}" stroke-width="4" stroke-linejoin="round"'
    out = ""
    mw, n = 30, 4
    gap = (w - n * mw) / (n - 1)
    for i in range(n):
        pts = merlon_pts(x0 + i * (mw + gap), top, mw, 1.0)
        out += '<path d="M' + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + f' Z" fill="{S.shade(col, 0.06)}" {st}/>'
    out += (f'<path d="M{f1(x1)},{f1(y)} L{f1(x1 + 30)},{f1(y - 14)} L{f1(x1 + 30)},{f1(top - 14)} '
            f'L{f1(x1)},{f1(top)} Z" fill="{S.shade(col, -0.22)}" {st}/>')
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(w)}" height="{f1(h)}" fill="{S.shade(col, 0.06)}" {st}/>'
    out += f'<rect x="{f1(x0 + 2)}" y="{f1(y - 30)}" width="{f1(w - 4)}" height="28" fill="{S.shade(col, -0.12)}"/>'
    for j in range(9):
        yy = top + 34 + j * 40
        if yy > y - 34:
            break
        out += (f'<line x1="{f1(x0 + 4)}" y1="{f1(yy)}" x2="{f1(x1 - 4)}" y2="{f1(yy)}" '
                f'stroke="{S.shade(col, -0.2)}" stroke-width="2" opacity="0.5"/>')
    by = top + 44
    out += f'<rect x="{f1(x0)}" y="{f1(by)}" width="{f1(w)}" height="28" fill="#3f78b5" {st}/>'
    for i in range(4):
        rx = x0 + w * (i + 0.5) / 4
        out += (f'<circle cx="{f1(rx)}" cy="{f1(by + 14)}" r="8.5" fill="#fff6dc" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="{f1(rx)}" cy="{f1(by + 14)}" r="3.4" fill="{P["gold"]}"/>')
    for yy in (top + 104, top + 190):
        out += f'<rect x="{f1(cx - 8)}" y="{f1(yy)}" width="16" height="40" rx="8" fill="#4a3426" {st}/>'
    out += f'<rect x="{f1(x0)}" y="{f1(top)}" width="{f1(w)}" height="{f1(h)}" fill="none" {st}/>'
    return S.g(out, filter="wobble-fine")


GATE_TOWERS = (GX - GW / 2 - 60, GX + GW / 2 + 60)     # centres of the two gate towers
GT_TOP = WY - 1.45 * WH - 34                            # top of the gate towers


def banner(cx, top, w=56, h=150, col="#c0533a"):
    """Long festive banner hanging on a tower: swallow-tail end, gold sun disc."""
    x0, x1 = cx - w / 2, cx + w / 2
    d = (f"M{f1(x0)},{f1(top)} L{f1(x1)},{f1(top)} L{f1(x1)},{f1(top + h)} L{f1(cx)},{f1(top + h - 22)} "
         f"L{f1(x0)},{f1(top + h)} Z")
    out = (f'<rect x="{f1(x0 - 8)}" y="{f1(top - 8)}" width="{f1(w + 16)}" height="10" rx="4" fill="{P["wood"]}" '
           f'stroke="{INK}" stroke-width="3"/>')
    out += S.path(d, fill=col, sw=3.5)
    out += f'<path d="M{f1(x0 + 6)},{f1(top + 6)} L{f1(x0 + 6)},{f1(top + h - 12)}" stroke="{S.shade(col, 0.3)}" stroke-width="4" opacity="0.6"/>'
    out += (f'<circle cx="{f1(cx)}" cy="{f1(top + h * 0.38)}" r="{f1(w * 0.26)}" fill="{P["gold"]}" stroke="{INK}" '
            f'stroke-width="2.5"/>')
    out += f'<path d="M{f1(x0)},{f1(top + 16)} L{f1(x1)},{f1(top + 16)}" stroke="{P["gold"]}" stroke-width="4"/>'
    return out


def wall_svg():
    body = PR.city_wall(-60, WX1, WY, WH, gate=(GX, GW), doors_open=1.0, seed=4)
    body += corner_tower(TOWER[0], WY + 4, WH + 76, TOWER[1])
    ban = ""
    for i, cx in enumerate(GATE_TOWERS):
        ban += banner(cx, GT_TOP + 150, col=("#c0533a", "#3f78b5")[i % 1])
    ban += banner(TOWER[0], WY - WH - 76 + 92, w=48, h=124, col="#3b8b89")
    # garland over the gate arch
    gy = WY - 0.62 * WH - GW / 2 - 6
    pts = [(GX - GW / 2 - 4, gy + 30), (GX - 50, gy - 6), (GX, gy - 18), (GX + 50, gy - 6), (GX + GW / 2 + 4, gy + 30)]
    gd = S.smooth_path(pts, closed=False)
    ban += f'<path d="{gd}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
    ban += f'<path d="{gd}" fill="none" stroke="{P["leaf"]}" stroke-width="10" stroke-linecap="round"/>'
    rnd = random.Random(3)
    for i in range(9):
        u = (i + 0.5) / 9
        x = pts[0][0] + (pts[-1][0] - pts[0][0]) * u
        y = gy + 30 - 48 * math.sin(math.pi * u) + rnd.uniform(-2, 2)
        c = ("#f3a0a8", "#f6d36b", "#fffaf0", "#e45e52")[i % 4]
        ban += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="9" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="{f1(x)}" cy="{f1(y)}" r="3" fill="#e7a73d"/>')
    body += S.g(ban, filter="wobble-fine")
    return doc(body)


BUNT_COLS = ("#e45e52", "#f2c14e", "#3f78b5", "#f3a0a8", "#3b8b89", "#fff3d6")


def bunting_svg():
    """Strings of little triangular flags swagging along the wall face and between the gate towers."""
    out = ""
    top = WY - WH + 18
    spans = [(-40, 205), (322, 628), (1084, 1300), (1300, WX1 - 18)]
    spans += [(GATE_TOWERS[0] + 40, GATE_TOWERS[1] - 40)]
    k = 0
    for si, (x0, x1) in enumerate(spans):
        y0 = top if si < 4 else GT_TOP + 120
        sag = 40 if si < 4 else 52
        n = max(5, int((x1 - x0) / 34))
        pts = [(x0 + (x1 - x0) * i / 40, y0 + sag * math.sin(math.pi * i / 40)) for i in range(41)]
        out += S.path(S.smooth_path(pts, closed=False), sw=2.5)
        for i in range(n):
            u = (i + 0.5) / n
            x = x0 + (x1 - x0) * u
            y = y0 + sag * math.sin(math.pi * u)
            c = BUNT_COLS[k % len(BUNT_COLS)]
            k += 1
            out += (f'<path d="M{f1(x - 11)},{f1(y)} L{f1(x + 11)},{f1(y)} L{f1(x + 1)},{f1(y + 26)} Z" fill="{c}" '
                    f'stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def pennant_svg(phase):
    """Small flags on poles on top of the gate towers and the corner tower; ``phase`` flutters them."""
    out = ""
    tops = [(GATE_TOWERS[0], GT_TOP - 30), (GATE_TOWERS[1], GT_TOP - 30), (TOWER[0], WY - WH - 76 - 40)]
    for i, (x, y) in enumerate(tops):
        out += f'<path d="M{f1(x)},{f1(y + 34)} L{f1(x)},{f1(y - 70)}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        out += f'<path d="M{f1(x)},{f1(y + 34)} L{f1(x)},{f1(y - 70)}" stroke="{P["wood"]}" stroke-width="3.5" stroke-linecap="round"/>'
        ph = phase + i * 0.9
        L = 78
        pts_top = [(x + L * j / 4, y - 66 + 6 * math.sin(ph + j * 1.3) * j / 4) for j in range(5)]
        pts_bot = [(x + L * j / 4, y - 30 - 14 * j / 4 + 6 * math.sin(ph + j * 1.3 + 0.4) * j / 4) for j in range(5)]
        tip = (x + L + 6, y - 52 + 7 * math.sin(ph + 5.5))
        poly = pts_top + [tip] + pts_bot[::-1]
        col = ("#e45e52", "#e45e52", "#f2c14e")[i]
        out += S.path(S.smooth_path(poly, tension=0.6), fill=col, sw=3)
    return doc(S.g(out, filter="wobble-fine"))


def plain_svg():
    """Green plain in front of the wall: fields, the road out of the gate, palms, bushes, flowers."""
    g1 = S.mix(P["grass"], "#e6dc96", 0.38)
    defs = (S.lin_grad("plain", [(0, S.shade(g1, 0.18)), (0.4, g1), (1, S.mix(g1, P["grass_dark"], 0.25))]))
    body = V2._ridge([(-60, WY - 4), (1200, WY - 4), (1560, 1012), (1900, 960), (2300, 930), (2860, 912)],
                     "url(#plain)", 3, bottom=SH + 60)
    # fields (furrowed patches) on the plain
    body += V2._field([(40, 1060), (230, 1046), (360, 1056), (330, 1084), (70, 1090)], S.mix("#e4cf7e", g1, 0.3),
                      S.mix(P["earth"], g1, 0.4))
    body += V2._field([(1700, 952), (1850, 940), (1990, 944), (1960, 962), (1730, 966)],
                      S.mix("#e4cf7e", g1, 0.35), S.mix(P["earth"], g1, 0.4))
    body += V2._field([(2150, 958), (2400, 944), (2620, 950), (2580, 972), (2190, 978)],
                      S.mix(P["grass_dark"], g1, 0.45), S.mix(P["grass_dark"], g1, 0.15))
    road = S.mix(P["sand_light"], P["sand"], 0.35)
    body += V2._dirt_path("rd", [(GX, WY + 2), (GX + 10, 1070), (GX - 30, 1140), (GX - 110, 1240), (GX - 230, 1360),
                                  (GX - 360, 1500), (GX - 440, 1640)],
                          [150, 170, 200, 250, 300, 360, 420], 1640, WY, road, ink_w=3.2, fade=(0.97, 0.95, 0.92),
                          pebbles=[(GX - 60, 1180, 6), (GX - 250, 1330, 8), (GX + 30, 1100, 5)], seed=4)
    body += V2._dirt_path("rd2", [(GX + 30, 1110), (GX + 160, 1134), (GX + 330, 1164), (GX + 470, 1200),
                                   (GX + 580, 1250)],
                          [70, 62, 56, 50, 46], 1250, 1100, road, ink_w=2.4, fade=(0.9, 0.85, 0.7), ruts=False, seed=5)
    for x, y, s in [(520, WY + 6, 0.6), (1468, WY + 10, 0.62), (30, WY + 12, 0.56)]:
        body += PR.palm_tree(x, y, s)
    # the open plain east of the city (behind Jonah): a hamlet of palms, a shepherd's hut, bushes
    for x, y, s in [(1985, 958, 0.34), (2045, 962, 0.28), (2560, 946, 0.36), (2625, 950, 0.3)]:
        body += PR.palm_tree(x, y, s)
    body += PR.house(2110, 966, 0.13, variant=0) + PR.house(2490, 950, 0.12, variant=2, facing=-1)
    for x, y, s, v in [(1720, 1030, 0.36, 2), (2230, 990, 0.32, 0), (2380, 984, 0.3, 1), (1880, 1010, 0.3, 3)]:
        body += PR.bush(x, y, s, variant=v)
    for x, y, s, v in [(560, 1046, 0.45, 1), (1190, 1044, 0.42, 3), (300, 1070, 0.4, 0), (1420, 1060, 0.4, 1)]:
        body += PR.bush(x, y, s, variant=v)
    body += V2._flowers(260, 1200, 16, 220, 4) + V2._flowers(620, 1330, 12, 200, 6) + V2._flowers(1100, 1240, 9, 120, 8)
    body += V2._flowers(160, 1420, 12, 160, 9)
    for x, y, v in [(100, 1260, 0), (420, 1180, 2), (980, 1170, 0), (700, 1430, 2), (1180, 1350, 0)]:
        body += PR.grass_tuft(x, y, 0.9, variant=v)
    return doc(S.g(body, filter="wobble"), defs)


def no_olive_dots(markup):
    """PR.olive_tree's small dark olives read as eyes at this scale (as in v1 s03): drop them."""
    return re.sub(r'<ellipse[^>]*fill="#5c4a63"[^>]*/>', "", markup)


def knoll_svg():
    """Jonah's dry rocky knoll east of the gate (s11's hillside palette): cracked earth, stones, dry shrubs."""
    defs = S.lin_grad("kn", [(0, "#e9c88c"), (0.25, "#dfb172"), (1, "#c79659")])
    pts = [(x, knoll_y(x)) for x in range(1180, 2950, 60)]
    kd = S.smooth_path(pts, closed=False) + f" L{SW + 80},{SH + 80} L1100,{SH + 80} Z"
    body = S.path(kd, fill="url(#kn)", sw=4)
    rim = [(x, knoll_y(x) + 16) for x in range(1300, 2900, 60)]
    body += f'<path d="{S.smooth_path(rim, closed=False)}" fill="none" stroke="#f3d7a0" stroke-width="13" opacity="0.6"/>'
    for (x, y) in [(1500, 1330), (2100, 1300), (2500, 1360), (1800, 1440), (2300, 1480)]:
        body += (f'<path d="M{x - 80},{y} q80,-18 160,0" fill="none" stroke="#c4935a" stroke-width="4" '
                 f'opacity="0.45" stroke-linecap="round"/>')
    for (x, y, s_, sd) in [(1640, 1290, 60, 1), (2240, 1250, 70, 2), (2560, 1320, 55, 3), (1980, 1400, 64, 4)]:
        body += V11._cracks(x, y, s_, seed=sd)
    # a worn footpath from the road up onto the knoll (the way Jonah came out of the city)
    fp = [(1400, 1290), (1520, 1262), (1640, 1236), (1740, 1220), (1800, 1212)]
    body += V2._dirt_path("fp", fp, [44, 40, 34, 28, 22], 1290, 1212, "#f0d5a2", ink_w=2.2,
                          fade=(0.85, 0.75, 0.3), ruts=False, pebbles=[(1530, 1262, 4), (1660, 1234, 3.5)], seed=7)
    # warm soft shading at the knoll's front edge and a few sandy ripples
    body += (f'<ellipse cx="2050" cy="{SH + 20}" rx="900" ry="140" fill="#b8844c" opacity="0.25" '
             f'filter="url(#blur-md)"/>')
    land = S.g(body, filter="wobble")
    # stones, pebbles, dry shrubs and tufts on and behind the crest
    st = ""
    st += PR.bush(1560, knoll_y(1560) + 6, 0.55, variant=2)
    st += V11._stone(2190, knoll_y(2190) + 6, 170, 92, seed=41, sw=4, crack=True)
    st += V11._stone(2300, knoll_y(2300) + 8, 86, 48, seed=43, sw=4)
    st += V11._stone(1640, knoll_y(1640) + 4, 70, 34, seed=45, sw=3.5)
    st += V11._pebbles(1720, knoll_y(1720) + 22, 1.0, seed=3) + V11._pebbles(2080, knoll_y(2080) + 30, 0.9, seed=5, n=2)
    st += V11._pebbles(2450, knoll_y(2450) + 40, 1.1, seed=6)
    for x, s in [(1450, 0.7), (1760, 0.55), (2380, 0.6), (2540, 0.7)]:
        st += PR.grass_tuft(x, knoll_y(x) + 8, s, variant=1)
    st += no_olive_dots(PR.olive_tree(2690, knoll_y(2690) + 6, 0.9, seed=3))
    # the knoll's front: a dry shrub, pebbles, small desert flowers
    st += PR.bush(2440, 1420, 0.7, variant=2) + PR.bush(1520, 1470, 0.6, variant=2)
    st += V11._pebbles(1760, 1360, 1.2, seed=8) + V11._pebbles(2240, 1400, 1.3, seed=9, n=4)
    st += V11._pebbles(2620, 1450, 1.1, seed=10)
    for x, y, s in [(1660, 1400, 0.8), (2120, 1340, 0.75), (2330, 1470, 0.85), (1940, 1470, 0.7)]:
        st += PR.grass_tuft(x, y, s, variant=1)
    st += V2._flowers(2000, 1300, 6, 90, 11, colors=("#f6d36b", "#f3a0a8", "#fffaf0"))
    st += V2._flowers(2560, 1330, 5, 70, 12, colors=("#f6d36b", "#fffaf0"))
    return doc(land + S.g(st, filter="wobble-fine"), defs)


def foreground_svg():
    fg = V11._rock(1330, 1560, 260, 120, seed=31) + V11._rock(2650, 1570, 330, 140, seed=33)
    fg += V11._rock(2440, 1590, 160, 70, seed=34)
    return doc(S.g(fg, filter="wobble"))


# ------------------------------------------------------------------ thought bubbles
def ring_body(cream, under, rim_glow=None, seed=11):
    r = random.Random(seed)
    puffs = []
    n = 18
    for i in range(n):
        a = 2 * math.pi * i / n + 0.12
        rr = r.uniform(50, 70) * (0.85 if math.sin(a) < -0.3 else 1.0)
        puffs.append((BX + (RX + 30) * math.cos(a), BY + (RY + 26) * math.sin(a), rr))
    ring = ""
    for x, y, rr in puffs:
        ring += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr)}" fill="{cream}" stroke="{INK}" stroke-width="8"/>'
    for x, y, rr in puffs:
        fill = under if y > BY + RY * 0.55 else cream
        ring += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr - 1)}" fill="{fill}"/>'
    ring += f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 30}" ry="{RY + 26}" fill="{cream}"/>'
    return S.g(ring, filter="wobble")


def ring_front_svg(cream, under, glow_col, seed):
    """The bubble's puffy cloud ring, drawn ON TOP of the bubble contents with the window cut out (even-odd
    clip), plus the window's ink rim: anything moving inside the bubble that strays past the window edge
    (the ship sailing off, the pop scale) is simply covered by the ring."""
    ell = f"M{BX - RX + 2},{BY} a{RX - 2},{RY - 2} 0 1 0 {2 * (RX - 2)},0 a{RX - 2},{RY - 2} 0 1 0 {-2 * (RX - 2)},0 Z"
    cid = f"ringout{seed}"
    defs = (f'<clipPath id="{cid}"><path clip-rule="evenodd" d="M-10,-10 H{SW + 10} V{SH + 10} H-10 Z {ell}"/>'
            f'</clipPath>')
    body = f'<g clip-path="url(#{cid})">{ring_body(cream, under, seed=seed)}</g>'
    body += (f'<ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}" fill="none" stroke="{glow_col}" stroke-width="10" '
             f'opacity="0.55" filter="url(#soft)"/>')
    body += S.g(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX}" ry="{RY}" fill="none" stroke="{INK}" stroke-width="4.5"/>',
                filter="wobble")
    return doc(body, defs)


def win_clip(cid, inset=0):
    return f'<clipPath id="{cid}"><ellipse cx="{BX}" cy="{BY}" rx="{RX - inset}" ry="{RY - inset}"/></clipPath>'


# flashback (bubble 1): Joppa harbour, the ship to Tarshish, Jonah running down the pier
SHIP = (BX - 108, BY + 96, 0.24)            # ship waterline anchor, scale (facing -1: sails west / left)
PIER_Y = BY + 96 - 165 * 0.24               # pier planks level with the ship's deck
PIER_X0 = BX + 22


def flash_back_svg():
    defs = (win_clip("w1") +
            S.lin_grad("fsky", [(0, "#a9d4e4"), (0.6, "#dcefe8"), (1, "#f6efd6")], 0, 0, 0, 1) +
            S.lin_grad("fsea", [(0, P["sea_light"]), (1, P["sea"])]))
    inner = f'<rect x="{BX - RX}" y="{BY - RY}" width="{2 * RX}" height="{2 * RY}" fill="url(#fsky)"/>'
    inner += S.cloud(BX - 150, BY - 110, 120, 40, "#fffaf0", seed=4, sw=2.5, shade_fill="#dbe9ee")
    inner += S.cloud(BX + 140, BY - 128, 90, 32, "#fffaf0", seed=6, sw=2.5, shade_fill="#dbe9ee")
    # Joppa's hill on the right (east), a few tiny houses
    inner += V2._ridge([(BX + 40, BY + 12), (BX + 150, BY - 40), (BX + 260, BY - 54), (BX + RX + 40, BY - 30)],
                       S.mix(P["grass"], P["sand"], 0.45), 2.5)
    for hx, hy, s in [(BX + 150, BY - 34, 0.07), (BX + 205, BY - 46, 0.08), (BX + 250, BY - 40, 0.065)]:
        inner += PR.house(hx, hy, s, variant=0)
    inner += f'<path d="{S.wave_band(BY - 6, 3, 90, 0, BX - RX - 20, BX + RX + 20, BY + RY + 20)}" fill="url(#fsea)" stroke="{INK}" stroke-width="2.5"/>'
    for i in range(6):
        x = BX - 230 + i * 80
        inner += (f'<path d="M{x},{BY + 30 + (i % 3) * 22} q14,-6 28,0" fill="none" stroke="{P["foam"]}" '
                  f'stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    # pier
    pier = ""
    for px in range(int(PIER_X0 + 14), int(BX + RX + 40), 46):
        pier += (f'<rect x="{px - 6}" y="{f1(PIER_Y)}" width="12" height="{f1(BY + 140 - PIER_Y)}" fill="{P["wood_dark"]}" '
                 f'stroke="{INK}" stroke-width="2.5"/>')
    pier += (f'<rect x="{f1(PIER_X0)}" y="{f1(PIER_Y - 2)}" width="{f1(BX + RX + 60 - PIER_X0)}" height="14" '
             f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>')
    pier += PR.jar(BX + 240, PIER_Y - 22, 0.24) + PR.crate(BX + 196, PIER_Y - 16, 0.26)
    inner += pier
    body = f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 30}" ry="{RY + 26}" fill="#fff8ea"/>'
    body += f'<g clip-path="url(#w1)">{S.g(inner, filter="wobble-fine")}</g>'
    halo = S.rad_grad("fh", [(0, "#fff7dc", 0.8), (0.6, "#fff0c8", 0.35), (1, "#ffe9b0", 0)])
    return doc(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 150}" ry="{RY + 120}" fill="url(#fh)"/>' + body, defs + halo)


def flash_ship_svg(part):
    x, y, s = SHIP
    body = PR.ship(x, y, s, -1, sail="full", part=part, lantern=False)
    return doc(f'<g clip-path="url(#w1b)">{body}</g>', win_clip("w1b", -24))


def flash_sea_front_svg():
    x, y, s = SHIP
    d = S.wave_band(y + 4, 4, 70, 0.6, BX - RX - 30, BX + RX + 30, BY + RY + 30)
    body = f'<path d="{d}" fill="{S.mix(P["sea_light"], P["sea"], 0.45)}" stroke="{INK}" stroke-width="2.5"/>'
    body += (f'<path d="{S.wave_line(y + 4, 4, 70, 0.6, BX - 260, BX + 260)}" fill="none" stroke="{P["foam"]}" '
             f'stroke-width="4" opacity="0.8"/>')
    return doc(f'<g clip-path="url(#w1c)">{S.g(body, filter="wobble-fine")}</g>', win_clip("w1c", -24))


# memory (bubble 2): God's kindness — a glowing heart; a grey cloud over a tiny Nineveh melts away
HEART = (BX - 100, BY - 46)
HEART_W = 108
MCLOUD = (BX + 98, BY - 6)


def heart_path(cx, cy, w):
    pts = []
    for i in range(72):
        a = 2 * math.pi * i / 72
        hx = 16 * math.sin(a) ** 3
        hy = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + hx * w / 34, cy + hy * w / 34))
    return "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"


def memory_back_svg():
    defs = (win_clip("w2") +
            S.lin_grad("msky", [(0, "#fbe7bd"), (0.55, "#fdf0d2"), (1, "#f8e2b4")]) +
            S.rad_grad("mglow", [(0, "#fff8dc", 1), (0.35, "#ffe7a0", 0.75), (1, "#ffd27a", 0)]) +
            S.rad_grad("mh", [(0, "#fff3c8", 0.95), (0.6, "#ffe3a0", 0.5), (1, "#ffd98a", 0)]))
    inner = f'<rect x="{BX - RX}" y="{BY - RY}" width="{2 * RX}" height="{2 * RY}" fill="url(#msky)"/>'
    inner += f'<circle cx="{HEART[0]}" cy="{HEART[1]}" r="230" fill="url(#mglow)"/>'
    gy = BY + 128
    inner += PR.nineveh_skyline(BX - RX + 10, BX + RX - 10, gy, 0.18, seed=2, haze=0.12, tint="#f6dcae")
    inner += V2._ridge([(BX - RX - 40, gy + 2), (BX, gy - 2), (BX + RX + 40, gy + 4)],
                       S.mix(P["grass"], P["sand"], 0.4), 2.5)
    body = f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 30}" ry="{RY + 26}" fill="#fff0c8"/>'
    body += f'<g clip-path="url(#w2)">{S.g(inner, filter="wobble-fine")}</g>'
    return doc(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 190}" ry="{RY + 160}" fill="url(#mh)"/>' + body, defs)


def heart_rays_svg():
    cx, cy = HEART
    d = S.rays(cx, cy, 64, 128, n=14, width_deg=10)
    defs = (f'<radialGradient id="hr" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="130">'
            f'<stop offset="0.45" stop-color="#ffd25e" stop-opacity="0.9"/>'
            f'<stop offset="1" stop-color="#ffe7a0" stop-opacity="0"/></radialGradient>')
    return doc(f'<path d="{d}" fill="url(#hr)"/>', defs)


def heart_svg():
    cx, cy = HEART
    d = heart_path(cx, cy + 4, HEART_W)
    body = f'<path d="{d}" fill="#ec7478" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    body += f'<path d="{heart_path(cx + 6, cy + 10, HEART_W * 0.62)}" fill="#f39a9a" opacity="0.6"/>'
    body += (f'<ellipse cx="{f1(cx - HEART_W * 0.22)}" cy="{f1(cy - HEART_W * 0.12)}" rx="{f1(HEART_W * 0.09)}" '
             f'ry="{f1(HEART_W * 0.06)}" fill="#fff3e6" opacity="0.9" transform="rotate(-30 {f1(cx - HEART_W * 0.22)} '
             f'{f1(cy - HEART_W * 0.12)})"/>')
    return doc(S.g(body, filter="wobble-fine"))


def heart_beam_svg():
    """Warm light shining from the heart onto the grey cloud and the little city below it."""
    hx, hy = HEART
    cx, cy = MCLOUD
    ang = math.degrees(math.atan2(cy + 20 - hy, cx - hx))
    hx += HEART_W * 0.42 * math.cos(math.radians(ang))
    hy += HEART_W * 0.42 * math.sin(math.radians(ang))
    d = V2._fan(hx, hy, math.hypot(cx - hx, cy - hy) + 90, [ang - 7, ang + 3, ang + 12], [7, 9, 6])
    defs = (f'<radialGradient id="hbm" gradientUnits="userSpaceOnUse" cx="{hx}" cy="{hy}" r="300">'
            f'<stop offset="0.15" stop-color="#fff2b8" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="#ffe08a" stop-opacity="0.15"/></radialGradient>')
    return doc(f'<path d="{d}" fill="url(#hbm)" filter="url(#soft)"/>', defs)


def storm_svg():
    cx, cy = MCLOUD
    body = ""
    for i in range(5):
        x = cx - 60 + i * 30
        body += (f'<path d="M{x},{cy + 24} l-8,26" stroke="#7d8aa0" stroke-width="4" stroke-linecap="round" '
                 f'opacity="0.8"/>')
    body += (f'<path d="M{cx + 18},{cy + 22} l-14,22 l12,0 l-12,24" fill="none" stroke="{INK}" stroke-width="7" '
             f'stroke-linejoin="round" stroke-linecap="round"/>'
             f'<path d="M{cx + 18},{cy + 22} l-14,22 l12,0 l-12,24" fill="none" stroke="#f6d35a" stroke-width="3.5" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    body += S.cloud(cx, cy, 136, 50, "#a9a7b3", seed=21, sw=3, shade_fill="#86849a")
    body += (f'<path d="M{cx - 30},{cy - 2} c8,-12 18,8 26,-4 s16,10 24,-2" fill="none" stroke="#6f6d7d" '
             f'stroke-width="3.5" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble-fine"))


def city_glow_svg():
    defs = (win_clip("w2g", 4) +
            S.rad_grad("cg", [(0, "#fff6d0", 0.85), (0.5, "#ffe7a6", 0.45), (1, "#ffdc90", 0)]))
    body = f'<ellipse cx="{BX + 40}" cy="{BY + 100}" rx="260" ry="90" fill="url(#cg)"/>'
    return doc(f'<g clip-path="url(#w2g)">{body}</g>', defs)


def melt_puffs_svg():
    cx, cy = MCLOUD
    out = ""
    for dx, dy, r in [(-50, -10, 16), (0, -24, 20), (46, -8, 15), (20, 14, 12)]:
        out += f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" fill="#fffaf0" stroke="{P["ink_soft"]}" stroke-width="3"/>'
    return doc(S.g(out, filter="wobble-fine"))


def trail_svg(i, cream="#fff8ea"):
    x, y, r = TRAIL[i]
    return doc(S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cream}" stroke="{INK}" stroke-width="5"/>',
                   filter="wobble-fine"))


TRAIL = [(1915, 760, 12), (1962, 722, 17), (2024, 686, 23)]


# ------------------------------------------------------------------ God's light
RAY_TARGET = (JX + 20, JY + 30)


def ray_defs():
    gy, ty = GAP[1], RAY_TARGET[1]
    return (f'<linearGradient id="rayg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{ty + 100}">'
            f'<stop offset="0" stop-color="#fff6d2" stop-opacity="0.85"/>'
            f'<stop offset="0.6" stop-color="#ffeaa8" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#ffe08e" stop-opacity="0.12"/></linearGradient>')


def ray_main():
    gx, gy = GAP
    tx, ty = RAY_TARGET
    return math.degrees(math.atan2(ty - gy, tx - gx)), math.hypot(tx - gx, ty - gy) + 160


def rays_svg(which):
    """Soft separate shafts fanning down from the cloud gap onto Jonah; two interleaved sets (``which`` 0 / 1)
    that pulse in turn so the light gently shimmers."""
    gx, gy = GAP
    main, length = ray_main()
    offs = [(-15, 2.6), (-9, 3.4), (-3.5, 2.2), (2, 3.8), (7.5, 2.4), (13, 3.0)] if which == 0 else \
           [(-12, 2.0), (-6.2, 2.6), (-0.5, 1.8), (4.8, 2.2), (10.2, 2.0), (16, 1.8)]
    d = V2._fan(gx, gy + 8, length, [main + o for o, _w in offs], [w for _o, w in offs])
    return doc(f'<path d="{d}" fill="url(#rayg)" filter="url(#soft)"/>', ray_defs())


def light_pool_svg():
    gx, gy = GAP
    main, length = ray_main()
    defs = (ray_defs() +
            f'<linearGradient id="coneg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{RAY_TARGET[1] + 100}">'
            f'<stop offset="0" stop-color="#fff2c4" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#ffe39a" stop-opacity="0.2"/></linearGradient>' +
            S.rad_grad("pool", [(0, "#fff1c0", 0.85), (0.6, "#ffe39a", 0.35), (1, "#ffd77e", 0)]) +
            S.rad_grad("halo", [(0, "#fff6d6", 0.75), (0.6, "#ffe7a4", 0.32), (1, "#ffe0a0", 0)]))
    body = f'<path d="{V2._fan(gx, gy + 10, length, [main], [20])}" fill="url(#coneg)" filter="url(#blur-lg)"/>'
    body += f'<ellipse cx="{JX + 20}" cy="{f1(JY - 125 * JS)}" rx="{f1(200 * JS)}" ry="{f1(190 * JS)}" fill="url(#halo)"/>'
    body += f'<ellipse cx="{JX + 20}" cy="{JY + 2}" rx="{f1(260 * JS)}" ry="{f1(58 * JS)}" fill="url(#pool)"/>'
    return doc(body, defs)


def warm_svg():
    defs = S.rad_grad("warm", [(0, "#3a2a0c", 1), (0.5, "#1e1505", 0.85), (1, "#100800", 0)])
    return doc(f'<ellipse cx="{GAP[0] - 200}" cy="700" rx="800" ry="700" fill="url(#warm)"/>', defs)


# ------------------------------------------------------------------ people & creatures
WALL_TOP = WY - WH
WALK_PEOPLE = [  # (x, feet y, kind, variant, facing) on the wall walk / tower tops (feet behind the parapet)
    (262, WY - WH - 90 + 28, "man", 0, 1), (352, WY - WH + 30, "child", 2, 1), (800, WY - WH + 26, "woman", 1, 1),
    (915, WY - WH + 26, "child", 1, -1), (1118, WY - WH + 30, "man", 3, -1), (1212, WY - WH + 30, "woman", 3, 1),
    (1300, WY - WH + 30, "elder", 0, -1), (1590, WY - WH - 72 + 26, "child", 0, -1),
]
CROWD = [  # (x, y, kind, variant, facing, scale, style) on the plain in front of the gate
    (560, 1064, "elder", 1, 1, 0.56, "wave"), (690, 1080, "woman", 2, 1, 0.58, "wave"),
    (770, 1104, "child", 0, 1, 0.6, "hop"), (1000, 1094, "child", 1, -1, 0.6, "hop"),
    (1105, 1072, "man", 2, -1, 0.57, "wave"), (1205, 1104, "woman", 0, -1, 0.6, "hop"),
    (845, 1036, "child", 3, 1, 0.48, "hop"),
]
SHEEP = [(300, 1100, 0.5, 1), (400, 1124, 0.55, -1)]


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    L0, L1, L2, L3, L4, L5 = L[0], L[1], L[2], L[3], L[4], L[5]

    # ---------------------------------------------------------------- beats (all from the narration)
    t_pan0 = L0.chunks[1].start - 0.3               # "只有约拿…" the camera glides to Jonah
    t_pan1 = L0.chunks[1].start + 2.6
    t_huff0 = L0.chunks[1].start + 1.5              # grumpy huff while the camera arrives
    t_stamp = L0.chunks[2].start + 0.12             # "他非常生气" stamps, anger mark
    t_lookup = phrase_t(L0, "对上帝说")             # lifts his face to heaven
    t_arms = L1.start + 0.02                        # "耶和华啊" arms up
    t_wide = phrase_t(L1, "我早就知道")             # arms flung wide
    t_b1 = L1.chunks[1].start - 0.32                # flashback bubble pops up ("所以我才急忙逃到他施去")
    t_watch = L1.chunks[1].start + 0.05             # Jonah looks up at it, arms crossed
    t_run0 = t_b1 + 0.55
    t_leap = L1.chunks[1].end - 0.75
    t_land = t_leap + 0.42
    t_sail1 = L2.start - 0.25
    t_b1_out = L2.start - 0.42
    t_shrug = L2.start + 0.02                       # "因为我知道" palms out
    t_b2 = L2.start + 0.3                           # memory bubble
    t_beat1 = phrase_t(L2, "慈爱")
    t_beat2 = phrase_t(L2, "宽容")
    t_wide2 = L2.chunks[1].start + 0.02             # "不轻易生气" arms wide again
    t_grey = phrase_t(L2, "你说要降下")             # grey cloud gathers over the tiny city
    t_shrug2 = L2.chunks[2].start + 0.02            # "只要人一认错"
    t_melt = phrase_t(L2, "你就不忍心")             # the heart's light melts the cloud
    t_cross = t_melt + 0.75                         # arms crossed + huff
    t_b2_out = L2.end + 0.2
    t_sit = L3.start + 0.05                         # "原来" plops down, sulking
    t_eye = L3.chunks[2].start + 0.05               # "可是他不愿意…" side-eye at the cheering city
    t_front = L3.chunks[3].start + 0.05             # "所以当初才逃跑了" huff, eyes front
    t_light = L4.start - 0.1                        # "于是，上帝问约拿" clouds part, light pours down
    t_glance = L5.start + 0.08                      # "约拿，" he looks up into the light
    t_turn = min(phrase_t(L5, "对吗") + 0.2, T - 1.6)  # turns his back to the light without answering

    # ---------------------------------------------------------------- SKY
    sc.add("sky", sky_svg(), wc=0.45)
    sun_c = SUN
    sc.add("sun_rays", sun_rays_svg(), wc=0, motion=M.combine(lambda t: Tf(rot=4 * t, px=sun_c[0], py=sun_c[1]),
                                                              M.pulse(0.6, 1.0, 3.4)))
    sc.add("sun", sun_svg(), wc=0.4, motion=M.breathe(0.025, 3.0, pivot=sun_c))
    for i, (cx, cy, w, h, sd, v) in enumerate([(640, 150, 300, 90, 3, 6), (1210, 300, 220, 70, 5, 4.5),
                                               (60, 420, 200, 62, 9, 5), (1620, 450, 170, 54, 8, 3.5)]):
        sc.add(f"cloud{i}", cloud_svg(cx, cy, w, h, sd), wc=0.7, motion=M.combine(M.drift(vx=v), M.bob(3, 7 + i, i * 0.3)))

    # heavenly glow + the cloud banks that part (line 4)
    glow_a = lambda t: M.progress(t, t_light, t_light + 0.9, "sine") * (0.86 + 0.14 * math.sin(2 * math.pi * (t - t_light) / 2.3))
    sc.add("heaven_glow", heaven_glow_svg(), wc=0, motion=lambda t: Tf(alpha=glow_a(t)))
    for name, rel, d0, d1 in [("bankL", LEFT_BANK, 70, -170), ("bankR", RIGHT_BANK, -66, 150)]:
        frames = [bank_svg(rel, g, name) for g in (0.0, 1.0)]
        # off stage (right) while the thought bubbles fill that sky; the bank drifts in during line 3, then
        # parts for the light
        mv = M.combine(M.keys([(0, {"dx": d0 + 950}), (L3.start + 0.2, {"dx": d0 + 950}), (t_light - 0.4, {"dx": d0}),
                               (t_light, {"dx": d0}), (t_light + 1.5, {"dx": d1})], ["linear", "out", "linear", "inout"]),
                       M.bob(4, 6.0, 0.3 if d1 > 0 else 0.0))
        sc.add(name, frames, motion=mv, wc=0.7, frame_at=lambda t: M.progress(t, t_light + 0.1, t_light + 1.2, "sine"))

    # ---------------------------------------------------------------- CITY
    sc.add("far", far_svg(), wc=0.7)

    # people on the wall walk (behind the parapet), waving now and then
    for i, (x, fy, kind, var, fc) in enumerate(WALK_PEOPLE):
        s = 0.42
        frames = [doc(CH.citizen(x, fy, s, fc, kind=kind, variant=var, pose=p)) for p in ("stand", "cheer")]
        hops = V12.hop_sched(70 + i, T, n=(1, 2), dur=(0.5, 0.8), rest=(1.0, 2.6))
        sc.add(f"walk{i}", frames, frame_at=V12.hop_frame(hops, 0.12, 0.25), wc=0.5,
               motion=V12.hop_motion(x, fy, hops, 9))

    sc.add("wall", wall_svg(), wc=0.8)
    sc.add("bunting", bunting_svg(), wc=0.5, boil=4)
    pen = [pennant_svg(ph) for ph in (0.0, 2.1, 4.2)]
    sc.add("pennants", pen, wc=0.5, frame_at=lambda t: float(int(t * 5) % 3))

    sc.add("plain", plain_svg(), wc=0.8)

    # sheep grazing by the wall (hooves planted, heads nod)
    for i, (x, y, s, f) in enumerate(SHEEP):
        body, head = V2._sheep_parts(x, y, s, f)
        br = M.breathe(0.012, 2.6 + 0.3 * i, pivot=(x, y), phase=0.3 * i)
        sc.add(f"sheep{i}", doc(CH.ground_shadow(x, y, s, width=180, opacity=0.2) + body), motion=br)
        if head:
            nx, ny = PR.local_to_stage(x, y, s, f, *V2.SHEEP_NECK)
            ang = (lambda t, i=i: -7 * (0.5 + 0.5 * math.sin(2 * math.pi * t / (2.9 + 0.6 * i) - 1.3 * i)))
            sc.add(f"sheep{i}_head", doc(head), motion=lambda t, ang=ang, br=br, f=f, ny=ny, nx=nx, y=y: Tf(
                dy=-(br(t).sy - 1) * (y - ny), rot=-ang(t) * f, px=nx, py=ny))

    # the joyful crowd
    for i, (x, y, kind, var, fc, s, style) in enumerate(CROWD):
        frames = [doc(CH.citizen(x, y, s, fc, kind=kind, variant=var, pose=p)) for p in ("stand", "cheer")]
        sc.add(f"crowd_sh{i}", doc(CH.ground_shadow(x, y, s, width=110 if kind == "child" else 120, opacity=0.2)),
               wc=0)
        if style == "hop":
            hops = V12.hop_sched(10 + i, T, n=(2, 3), dur=(0.4, 0.52), rest=(0.6, 1.3))
            sc.add(f"crowd{i}", frames, frame_at=V12.hop_frame(hops), wc=0.5,
                   motion=V12.hop_motion(x, y, hops, 26 * s / 0.6))
        else:
            hops = V12.hop_sched(30 + i, T, n=(1, 1), dur=(0.9, 1.4), rest=(0.7, 1.6))
            sc.add(f"crowd{i}", frames, frame_at=V12.hop_frame(hops, 0.0, 0.0), wc=0.5,
                   motion=M.combine(V12.hop_motion(x, y, hops, 5), M.breathe(0.01, 2.8, pivot=(x, y), phase=i * 0.2)))

    # doves over the city: a flock circling up at the start, another flying home over it in line 3
    dref = (1000, 500)
    dfr = {f: [doc(PR.dove(dref[0], dref[1], 0.55, f, wing=w)) for w in (1.0, 0.5, 0.0, -0.5, -1.0)] for f in (1, -1)}
    flights = [
        (1, [(-1.0, 600, 640), (2.0, 820, 520), (5.0, 1240, 380), (8.0, 1700, 160), (10.0, 2100, -120)], 0.0),
        (1, [(-0.6, 520, 700), (2.4, 760, 600), (5.4, 1180, 460), (8.4, 1640, 240), (10.4, 2050, -60)], 0.4),
        (1, [(-0.2, 690, 690), (2.8, 900, 570), (5.8, 1320, 420), (8.6, 1760, 200), (10.6, 2150, -80)], 0.7),
        (-1, [(L3.start - 0.5, 2950, 520), (L3.start + 3.0, 2300, 470), (L3.start + 6.5, 1400, 430),
              (L3.start + 9.5, 700, 520), (L3.start + 12.0, 300, 640)], 0.2),
        (-1, [(L3.start + 0.0, 3000, 600), (L3.start + 3.5, 2360, 540), (L3.start + 7.0, 1450, 500),
              (L3.start + 10.0, 760, 580), (L3.start + 12.5, 360, 700)], 0.6),
    ]
    for i, (f, pts, ph) in enumerate(flights):
        t0, t1 = pts[0][0], pts[-1][0]
        sc.add(f"dove{i}", dfr[f], wc=0.5, frame_at=V10.wing_cycle(9.0, ph),
               motion=M.combine(V10.flight(pts, dref), M.bob(10, 1.1, ph),
                                lambda t, t0=t0, t1=t1: Tf(alpha=1.0 if t0 < t < t1 else 0.0)))

    # ---------------------------------------------------------------- KNOLL + light on it
    sc.add("knoll", knoll_svg(), wc=0.85)

    # the little lizard from s11 basking on the big stone, doing push-ups
    LIZ = (2200, knoll_y(2190) + 6 - 90)
    liz = doc(V11._lizard(LIZ[0], LIZ[1], 0.62, legs=0))

    def liz_motion(t):
        u = (t + 0.7) % 3.1
        b = abs(math.sin(math.pi * u / 0.2)) if u < 0.4 else 0.0
        return Tf(sx=1 - 0.03 * b, sy=1 + 0.13 * b, px=LIZ[0], py=LIZ[1] + 2)

    sc.add("lizard", liz, motion=liz_motion, wc=0.5)

    light_in = lambda t: M.progress(t, t_light + 0.1, t_light + 0.8, "sine")
    reveal = lambda t: {"mode": "down", "frac": M.progress(t, t_light + 0.1, t_light + 1.1, "out"), "soft": 160}
    sc.add("light_pool", light_pool_svg(), wc=0, reveal=reveal, motion=lambda t: Tf(
        alpha=light_in(t) * (0.85 + 0.15 * math.sin(2 * math.pi * (t - t_light) / 2.6))))
    for k in range(2):
        sc.add(f"rays{k}", rays_svg(k), wc=0, reveal=reveal, motion=lambda t, k=k: Tf(
            alpha=light_in(t) * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(2 * math.pi * (t - t_light) / 2.2 + k * math.pi)))))

    # ---------------------------------------------------------------- JONAH
    # frames: 0 cross, 1 cross_up, 2 complain, 3 complain2, 4 shrug, 5 sit_sulk, 6 sulk side-eye,
    #         7 sulk looking up, 8 sit_sulk facing the city. (No blinks: the library's closed-eye faces
    #         'sleepy' / 'peaceful' have a yawning / smiling mouth, which would flash a wrong mood.)
    jdefs = [("cross", None, 1), ("cross_up", None, 1), ("complain", None, 1), ("complain2", None, 1),
             ("shrug", None, 1), ("sit_sulk", None, 1), ("sulk_eye", None, 1), ("sulk_up", None, 1),
             ("sit_sulk", None, -1)]
    jframes = [doc(jfig(JX, JY, JS, f, pose=p, expr=e)) for p, e, f in jdefs]
    SIT0 = 5
    # (time, frame, hop amplitude, dust, pop lines)
    sched = [(0.0, 0, 0, False, False),
             (t_lookup, 1, 0.6, False, False),
             (t_arms, 2, 1.0, False, True),
             (t_wide, 3, 0.8, False, False),
             (t_watch, 1, 0.6, False, False),
             (t_shrug, 4, 0.8, False, True),
             (t_wide2, 3, 0.8, False, False),
             (t_shrug2, 4, 0.7, False, False),
             (t_cross, 0, 0.8, False, False),
             (t_sit, 5, 1.4, True, False),
             (t_eye, 6, 0.4, False, False),
             (t_front, 5, 0.6, False, False),
             (t_glance, 7, 0.6, False, True),
             (t_turn, 8, 1.0, True, False)]

    def base_frame(t):
        f = 0
        for ts, fr, *_ in sched:
            if t >= ts:
                f = fr
        return f

    def jonah_frame(t):
        return float(base_frame(t))

    def hop(t):
        sy, dy = 1.0, 0.0
        for ts, fr, amp, *_r in sched:
            if amp <= 0:
                continue
            u = t - ts
            if ts == t_sit and -0.12 <= u <= 0.3:
                # plop: squash while still standing, cut, the seated figure drops the last bit onto the
                # ground and squashes on landing
                if u < 0:
                    sy = 1 - 0.07 * M.progress(u, -0.12, -0.01, "sine")
                elif u < 0.1:
                    dy = -26 * (1 - M.ease("in")(u / 0.1))
                    sy = 1.04
                else:
                    sy = 1 - 0.08 * math.sin(math.pi * _clamp((u - 0.1) / 0.2))
                continue
            if -0.09 <= u <= 0.2:
                if u < -0.01:
                    sy = 1 - 0.06 * amp * M.progress(u, -0.09, -0.01, "sine")
                elif u < 0.06:
                    sy = 1 - 0.06 * amp + 0.10 * amp * M.progress(u, -0.01, 0.06, "sine")
                else:
                    sy = 1 + 0.04 * amp - 0.04 * amp * M.progress(u, 0.06, 0.2, "sine")
                dy = -14 * amp * math.sin(math.pi * _clamp((u + 0.01) / 0.2))
        return sy, dy

    huffs = [t_huff0, t_stamp, t_cross + 0.25, t_front + 0.3]
    stamps = [t_stamp]

    def jonah_motion(t):
        s = 1 + 0.011 * math.sin(2 * math.pi * t / 3.1)
        sy = s
        rot = 0.0
        dy = 0.0
        for th in huffs:                       # grumpy huff: a little squash
            u = t - th
            if 0 <= u < 0.45:
                sy *= 1 - 0.035 * math.sin(math.pi * u / 0.45)
        for ts in stamps:                      # stamp: a quick bounce
            u = t - ts
            if 0 <= u < 0.32:
                dy -= 10 * math.sin(math.pi * u / 0.32)
        for ts in (t_arms, t_wide, t_wide2):   # shaking his arms at heaven
            u = t - ts
            if 0.15 <= u < 1.1:
                rot += 1.3 * math.sin(2 * math.pi * u * 3.2) * (1 - M.progress(u, 0.6, 1.1, "sine"))
        # side-eye at the cheering city: he leans back toward it a little
        rot -= 2.6 * M.progress(t, t_eye - 0.05, t_eye + 0.3, "sine") * (1 - M.progress(t, t_front - 0.1, t_front, "sine"))
        if base_frame(t) in (0, 1, 5, 6, 8):   # grumpy fidget while his arms are crossed
            rot += 0.7 * math.sin(2 * math.pi * t / 2.7) + 0.3 * math.sin(2 * math.pi * t / 1.3)
        hsy, hdy = hop(t)
        sy *= hsy
        sx = s * (1 + 0.5 * (1 - hsy))
        return Tf(dy=dy + hdy, rot=rot, sx=sx, sy=sy, px=JX, py=JY)

    jsh = [doc(CH.ground_shadow(JX, JY, JS, width=w, opacity=0.25)) for w in (130, 215)]
    sc.add("jonah_shadow", jsh, wc=0, frame_at=lambda t: 1.0 if base_frame(t) >= SIT0 else 0.0,
           motion=lambda t: Tf(sx=1 + 0.25 * hop(t)[1] / 30, px=JX, py=JY))
    sc.add("jonah", jframes, frame_at=jonah_frame, motion=jonah_motion, wc=0.6)

    # pose-change pop: little dust poofs + emphasis lines around his head
    CX, CY = SW // 2, SH // 2
    dust_svg = ""
    for bx, sgn in ((JX - 175, -1), (JX + 170, 1)):
        circ = [(0, 0, 17), (sgn * 20, -6, 13), (-sgn * 16, -4, 12), (sgn * 4, -16, 12)]
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{JY - 6 + dy}" r="{r}" fill="#f3e4c4" stroke="{P["ink_soft"]}" '
                            f'stroke-width="6"/>' for dx, dy, r in circ)
        dust_svg += "".join(f'<circle cx="{bx + dx}" cy="{JY - 6 + dy}" r="{r}" fill="#f3e4c4"/>' for dx, dy, r in circ)
    dust_ts = [ts for ts, _f, _a, dust, _l in sched if dust]

    def poof_motion(t):
        for ts in dust_ts:
            u = t - ts
            if 0 <= u < 0.45:
                k = 0.5 + 0.7 * M.ease("out")(u / 0.45)
                return Tf(dy=-6 * M.ease("out")(u / 0.45), sx=k, sy=k,
                          alpha=0.9 * (1 - M.progress(u, 0.12, 0.45, "sine")), px=JX, py=JY)
        return Tf(alpha=0.0)

    sc.add("jpop_dust", doc(S.g(dust_svg, filter="wobble-fine")), motion=poof_motion, wc=0.3)

    lines_svg = ""
    for k in range(5):
        a = math.radians(-160 + k * 35)
        lines_svg += (f'<path d="M{CX + 96 * math.cos(a):.1f},{CY + 96 * math.sin(a):.1f} '
                      f'L{CX + 132 * math.cos(a):.1f},{CY + 132 * math.sin(a):.1f}" stroke="{P["ink_soft"]}" '
                      f'stroke-width="7" stroke-linecap="round"/>')
    pop_pts = []
    for ts, fr, _a, _d, lines in sched:
        if lines:
            p, e, f = jdefs[fr]
            pop_pts.append((ts, CH.body_points(jfig, JX, JY, JS, f, pose=p)["head"]))

    def lines_motion(t):
        for ts, (px_, py_) in pop_pts:
            u = t - ts
            if 0 <= u < 0.34:
                k = 0.82 + 0.3 * M.ease("out")(u / 0.34)
                return Tf(dx=px_ - CX, dy=py_ - CY, sx=k, sy=k, alpha=1 - M.progress(u, 0.12, 0.34, "sine"),
                          px=CX, py=CY)
        return Tf(alpha=0.0)

    sc.add("jpop_lines", doc(S.g(lines_svg, filter="wobble-fine")), motion=lines_motion, wc=0.2)

    # grumpy steam puffs + anger mark on each huff
    for hi, th in enumerate(huffs):
        p, e, f = jdefs[base_frame(th + 0.01)]
        hx0, hy0 = CH.body_points(jfig, JX, JY, JS, f, pose=p)["head"]
        for side_, (ox, oy) in enumerate([(-96, 4), (94, 12)]):
            cx, cy = hx0 + ox * JS / 1.3, hy0 + oy
            sgn = -1 if side_ == 0 else 1

            def puff_motion(t, cx=cx, cy=cy, sgn=sgn, th=th, ph=side_ * 0.07):
                u = t - th - ph
                if 0 <= u < 0.8:
                    a = min(1.0, u / 0.05) * (1 - M.progress(u, 0.4, 0.8, "sine"))
                    k = 0.3 + 0.8 * M.ease("out")(u / 0.12) if u < 0.12 else 1.1 - 0.1 * M.progress(u, 0.12, 0.3, "sine")
                    e_ = M.ease("out")(min(1.0, u / 0.8))
                    return Tf(dx=sgn * 26 * e_, dy=-46 * e_, sx=k, sy=k, alpha=a, px=cx, py=cy)
                return Tf(alpha=0.0)

            sc.add(f"puff{hi}_{side_}", doc(V11._puff(cx, cy, 25)), motion=puff_motion, wc=0.3)
        ax, ay = hx0 + 52, hy0 - 62

        def anger_motion(t, th=th, ax=ax, ay=ay):
            u = t - th + 0.04
            if 0 <= u < 0.95:
                k = 1.25 * M.ease("out")(u / 0.1) if u < 0.1 else (
                    1.25 - 0.25 * M.progress(u, 0.1, 0.24, "sine") + 0.06 * math.sin(u * 30) * (1 - u))
                return Tf(sx=k, sy=k, alpha=1 - M.progress(u, 0.65, 0.95, "sine"), px=ax, py=ay)
            return Tf(alpha=0.0)

        sc.add(f"anger{hi}", doc(V11._anger(ax, ay, 21)), motion=anger_motion, wc=0.2)

    # ---------------------------------------------------------------- THOUGHT BUBBLES
    def pop_scale(t, t_in, t_out):
        if t < t_in or t > t_out + 0.32:
            return 0.0
        if t < t_in + 0.5:
            return 0.15 + 0.85 * M.progress(t, t_in, t_in + 0.5, "back")
        if t > t_out:
            u = (t - t_out) / 0.32
            return 1.0 + 0.06 * math.sin(math.pi * min(1.0, u / 0.35)) if u < 0.35 else max(0.0, 1.0 - M.ease("in")((u - 0.35) / 0.65) * 0.85)
        return 1.0

    def pop_alpha(t, t_in, t_out):
        return M.progress(t, t_in, t_in + 0.18, "sine") * (1 - M.progress(t, t_out + 0.12, t_out + 0.32, "sine"))

    def in_bubble(t_in, t_out, local=None):
        """Bubble pop (scale about the window centre, gentle float) composed with a local motion that is
        scaled with the bubble."""
        def m(t):
            k = pop_scale(t, t_in, t_out)
            a = pop_alpha(t, t_in, t_out)
            if a <= 0.002 or k <= 0.01:
                return Tf(alpha=0.0)
            fl = 4 * math.sin(2 * math.pi * (t - t_in) / 4.2)
            if local is None:
                return Tf(dy=fl, sx=k, sy=k, alpha=a, px=BX, py=BY)
            v = local(t)
            # local transform (about its own pivot) then the bubble scale about B: fold into one Tf
            px_ = v.px if v.px is not None else BX
            py_ = v.py if v.py is not None else BY
            return Tf(dx=(px_ + v.dx - BX) * k + BX - px_, dy=(py_ + v.dy - BY) * k + BY - py_ + fl,
                      rot=v.rot, sx=v.sx * k, sy=v.sy * k, alpha=a * v.alpha, px=px_, py=py_)
        return m

    def trail_motion(i, t_in, t_out):
        def m(t):
            ti = t_in - 0.36 + 0.1 * i
            to = t_out + 0.1 * (2 - i)
            if t < ti or t > to + 0.25:
                return Tf(alpha=0.0)
            k = 0.2 + 0.8 * M.progress(t, ti, ti + 0.22, "back")
            k *= 1 - 0.8 * M.progress(t, to, to + 0.25, "in")
            x, y, _r = TRAIL[i]
            return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + i), sx=k, sy=k, px=x, py=y,
                      alpha=1 - M.progress(t, to + 0.1, to + 0.25, "sine"))
        return m

    # the little trail of thought puffs stays from the first bubble to the end of the second
    for i in range(3):
        sc.add(f"trail_{i}", trail_svg(i), motion=trail_motion(i, t_b1, t_b2_out), wc=0.3)

    # bubble 1: the flashback to Joppa
    sc.add("b1_back", flash_back_svg(), motion=in_bubble(t_b1, t_b1_out), wc=0.5)
    sx_, sy_, ss_ = SHIP
    ship_bob = lambda t: M.progress(t, t_land + 0.05, t_sail1, "inout") * -70
    ship_local = lambda t: Tf(dx=ship_bob(t), dy=3 * math.sin(2 * math.pi * t / 1.7),
                              rot=1.2 * math.sin(2 * math.pi * t / 2.3), px=sx_, py=sy_)
    sc.add("b1_ship", flash_ship_svg("back"), motion=in_bubble(t_b1, t_b1_out, ship_local), wc=0.4)
    # tiny Jonah: runs down the pier, leaps aboard
    run_frames = [doc(jfig(BX + 200, PIER_Y, ss_, -1, pose=p)) for p in ("run_a", "run_b", "stand")]
    x_run0, x_run1, x_land = BX + 200, BX + 50, BX - 44
    deck_y = SHIP[1] - 165 * ss_

    def tiny_state(t):
        if t < t_run0:
            return 0.0, 0.0, 0.0
        if t < t_leap:
            u = (t - t_run0) / (t_leap - t_run0)
            return float(int((t - t_run0) / 0.12) % 2), (x_run1 - x_run0) * u, 0.0
        if t < t_land:
            u = (t - t_leap) / (t_land - t_leap)
            return 1.0, (x_run1 - x_run0) + (x_land - x_run1) * u, -46 * math.sin(math.pi * u) + (deck_y - PIER_Y) * u
        return 2.0, (x_land - x_run0) + ship_bob(t), (deck_y - PIER_Y) + 3 * math.sin(2 * math.pi * t / 1.7)

    sc.add("b1_jonah", run_frames, frame_at=lambda t: tiny_state(t)[0], wc=0.3,
           motion=in_bubble(t_b1, t_b1_out, lambda t: Tf(dx=tiny_state(t)[1], dy=tiny_state(t)[2],
                                                          alpha=M.progress(t, t_run0 - 0.25, t_run0, "sine"))))
    sc.add("b1_ship_front", flash_ship_svg("front"), motion=in_bubble(t_b1, t_b1_out, ship_local), wc=0.4)
    sc.add("b1_sea", flash_sea_front_svg(), wc=0.4,
           motion=in_bubble(t_b1, t_b1_out, lambda t: Tf(dx=6 * math.sin(2 * math.pi * t / 2.5))))
    sc.add("b1_ring", ring_front_svg("#fff8ea", "#f4e2c3", "#bfe0ea", 11), motion=in_bubble(t_b1, t_b1_out), wc=0.5)

    # bubble 2: God's kindness
    sc.add("b2_back", memory_back_svg(), motion=in_bubble(t_b2, t_b2_out), wc=0.5)
    sc.add("b2_cityglow", city_glow_svg(), wc=0, motion=in_bubble(
        t_b2, t_b2_out, lambda t: Tf(alpha=M.progress(t, t_melt + 0.7, t_melt + 1.5, "sine"))))

    hx_, hy_ = HEART
    beats = [t_beat1, t_beat2, t_melt]

    def beat(t):
        k = 0.0
        for tb in beats:
            u = t - tb
            if 0 <= u < 0.5:
                k = max(k, math.sin(math.pi * u / 0.5) * (1 - u))
        return k

    sc.add("b2_rays", heart_rays_svg(), wc=0, motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(
        rot=10 * t, sx=1 + 0.08 * beat(t) + 0.15 * M.progress(t, t_melt, t_melt + 0.6, "sine"),
        sy=1 + 0.08 * beat(t) + 0.15 * M.progress(t, t_melt, t_melt + 0.6, "sine"),
        alpha=0.85 + 0.15 * math.sin(t * 3), px=hx_, py=hy_)))
    sc.add("b2_heart", heart_svg(), wc=0.4, motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(
        sx=1 + 0.03 * math.sin(2 * math.pi * t / 1.1) + 0.12 * beat(t),
        sy=1 + 0.03 * math.sin(2 * math.pi * t / 1.1) + 0.12 * beat(t), px=hx_, py=hy_ + 30)))
    mx_, my_ = MCLOUD

    def storm_local(t):
        a = M.progress(t, t_grey, t_grey + 0.6, "sine")
        k = 1 - 0.75 * M.progress(t, t_melt + 0.3, t_melt + 1.2, "in")
        a *= 1 - M.progress(t, t_melt + 0.8, t_melt + 1.25, "sine")
        dx = 40 * (1 - M.progress(t, t_grey, t_grey + 0.9, "out")) + 3 * math.sin(t * 2.2)
        return Tf(dx=dx, sx=k, sy=k, alpha=a, px=mx_, py=my_)

    sc.add("b2_storm", storm_svg(), wc=0.4, motion=in_bubble(t_b2, t_b2_out, storm_local))
    sc.add("b2_beam", heart_beam_svg(), wc=0, motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(
        alpha=M.progress(t, t_melt - 0.1, t_melt + 0.4, "sine") * (1 - M.progress(t, t_melt + 1.3, t_melt + 2.0, "sine"))
        * (0.85 + 0.15 * math.sin(t * 7)))))

    def melt_local(t):
        u = t - (t_melt + 0.85)
        if u < 0 or u > 1.1:
            return Tf(alpha=0.0)
        return Tf(dy=-40 * M.ease("out")(u / 1.1), sx=0.6 + 0.6 * u, sy=0.6 + 0.6 * u,
                  alpha=min(1.0, u / 0.1) * (1 - M.progress(u, 0.5, 1.1, "sine")), px=mx_, py=my_)

    sc.add("b2_melt", melt_puffs_svg(), wc=0.3, motion=in_bubble(t_b2, t_b2_out, melt_local))
    sc.add("b2_ring", ring_front_svg("#fff0c8", "#f6d9a0", "#f3c860", 12), motion=in_bubble(t_b2, t_b2_out), wc=0.5)

    # ---------------------------------------------------------------- FOREGROUND
    sc.add("warm", warm_svg(), wc=0, blend="add",
           motion=lambda t: Tf(alpha=0.45 * M.progress(t, t_light + 0.2, t_light + 1.2, "sine") *
                               (0.8 + 0.2 * math.sin(2 * math.pi * (t - t_light) / 2.3))))
    for i, (x, y, v, s) in enumerate([(60, 1520, 2, 1.5), (230, 1545, 0, 1.4), (560, 1560, 2, 1.3),
                                      (1500, 1500, 1, 1.2), (2120, 1530, 1, 1.4), (2760, 1480, 1, 1.3)]):
        sc.add(f"tuft{i}", doc(PR.grass_tuft(x, y, s, variant=v)), wc=0.7,
               motion=M.sway(2.4 + 0.3 * (i % 3), 3.4 + 0.25 * (i % 4), pivot=(x, y), phase=0.17 * i))
    sc.add("fg", foreground_svg(), wc=0.8)

    # ---------------------------------------------------------------- CAMERA
    sc.camera = M.cam_keys([
        (0.0, Cam(1240, 860, 2400)),
        (t_pan0, Cam(1275, 852, 2370)),
        (t_pan1, Cam(1745, 800, 2000)),
        (t_b1 - 0.4, Cam(1755, 796, 2000)),
        (L2.end, Cam(1765, 792, 1990)),
        (L3.start + 0.6, Cam(1765, 792, 1990)),
        (L3.chunks[1].start + 3.0, Cam(1530, 838, 2330)),
        (t_light - 0.2, Cam(1545, 832, 2310)),
        (L4.end + 0.7, Cam(1730, 772, 2110)),
        (T, Cam(1742, 772, 2066)),
    ], "sine")

    # ---------------------------------------------------------------- FX
    sc.fx = [
        FX.motes((0, 300, SW, 1300), count=28, color=(255, 246, 214), size=(3, 6), alpha=110),
        FX.sparkles((200, 420, 1600, 900), count=22, t0=0, t1=L0.chunks[1].start + 1.2, color=(255, 238, 170),
                    size=(8, 18), period=1.5, drift=-8, seed=5),
        FX.sparkles((1620, 380, 2420, 1150), count=30, t0=t_light + 0.3, color=(255, 238, 170), size=(8, 20),
                    period=1.6, drift=-6, seed=21),
    ]

    # ---------------------------------------------------------------- SOUND
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("cheer", 0, dur=t_pan1 + 0.5, gain_db=-13, fade_in=0.8, fade_out=1.5, pan=-0.3)
    sc.sfx("cheer", L3.chunks[1].start + 0.5, dur=t_front - L3.chunks[1].start, gain_db=-19, fade_in=1.2,
           fade_out=1.2, pan=-0.4)
    sc.sfx("thud", t_stamp + 0.28, gain_db=-12, pan=0.2)
    sc.sfx("cloth", t_arms, gain_db=-14, pan=0.2)
    sc.sfx("cloth", t_shrug, gain_db=-15, pan=0.2)
    sc.sfx("pop", t_b1, gain_db=-11, pan=0.4)
    sc.sfx("footsteps_run", t_run0, dur=t_leap - t_run0, gain_db=-18, pan=0.4)
    sc.sfx("whoosh", t_leap, gain_db=-17, pan=0.4)
    sc.sfx("pop", t_b1_out + 0.1, gain_db=-14, pan=0.4)
    sc.sfx("pop", t_b2, gain_db=-11, pan=0.4)
    sc.sfx("sparkle", t_b2 + 0.1, gain_db=-12, pan=0.4)
    sc.sfx("sparkle", t_melt + 0.2, gain_db=-11, pan=0.4)
    sc.sfx("pop", t_b2_out + 0.1, gain_db=-14, pan=0.4)
    sc.sfx("thud", t_sit + 0.08, gain_db=-8, pan=0.2)
    sc.sfx("chime", L4.start, gain_db=-6, pan=0.2)
    sc.sfx("sparkle", L5.start + 0.2, gain_db=-13, pan=0.2)
    sc.sfx("cloth", t_turn, gain_db=-14, pan=0.2)
    return sc
