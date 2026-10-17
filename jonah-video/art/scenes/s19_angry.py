"""Scene 19 — Jonah is angry (Jonah 4:1-4).

Outside Nineveh on a sunny afternoon, one 2800 x 1575 stage, no cuts. West (left): the great city, saved —
its mud-brick wall with the open gate, the ziggurat and rooftops behind. The townspeople are still in their
sackcloth from the fast (as s18 ends and s20 begins) but cheer on the wall walk and on the green plain outside
the gate (children hop, grown-ups wave); two sheep in sackcloth blankets; doves. No festival decorations: the
joy is in the people and the warm light. East (right): a dry rocky knoll where Jonah stands; his bundle of
booth sticks and rolled cloth lies beside him the whole time (s20 opens with it there and builds the booth).

  line 0  "大家都很高兴，" the joyful city (wide). "只有约拿一点儿也不高兴。" the camera glides right to Jonah:
          arms crossed, scowling, a grumpy huff (steam puffs). "他非常生气，" he stamps (anger mark, puffs);
          "对上帝说：" he lifts his face to heaven.
  line 1  "耶和华啊，" both arms up to heaven; "我早就知道会这样！" arms flung wide; "所以我才急忙逃到他施去。"
          a thought bubble pops up beside him: a flashback — tiny Jonah dashes in from the right along the pier
          at Joppa (planted run drawings, one stride per drawing), leaps aboard the striped-sail ship on "他施",
          and the ship sails off west, sliding out of the window under the bubble's ring.
  line 2  "因为我知道，" palms out (the flashback pops away); "你又慈爱，" a warm memory bubble with a glowing heart
          (God's kindness — never a figure) that beats on "慈爱" and "宽容"; "你说要降下的灾祸，" a little grey
          rain cloud with a lightning bolt gathers over a tiny Nineveh; "你就不忍心降下来。" three golden rays
          shoot from the heart onto the cloud: rain and bolt stop, the cloud turns gold, squashes and pops into a
          burst of white puffs, and a warm gold glow rises behind the little city (twinkles); Jonah crosses his
          arms and huffs.
  line 3  "原来，" he plops down on the knoll (thud, dust), sulking; the camera eases back to show the cheering
          city behind him (doves fly home over it); mid-sentence he re-crosses his arms tighter with a huff;
          "可是他不愿意上帝饶恕他们，" he hop-turns to glare at the cheering crowd (steam, anger mark);
          "所以当初才逃跑了。" he hops back with a "hmph!" — eyes shut, nose in the air — then sulks on.
  line 4  "于是，上帝问约拿：" the clouds above him part and gentle golden light pours down on him (chime,
          sparkles); the camera eases in and tilts up into the light.
  line 5  "约拿，你这样生气，对吗？" the light glows softly with the words; Jonah looks up into it, surprised —
          then turns his back to the light (a hop-turn) and sulks toward the city without answering. Calm hold.

Continuity: s20 (约拿没有回答) opens on this scene's last frame — Jonah seated facing west at output
(1060, 926), scale 1.2 * 1920 / 2066, the light coming from the cloud gap GAP, the bundle beside him — and
replays this file's fidget / breathing clock. Keep JX, JS, GAP, the last camera key, the final pose and
jonah_motion's sway unchanged unless s20 changes with them.

Pose changes are hard cuts hidden by a squash-and-hop (dust poof, pop lines) as in v1 s11, and the sit-down
is a "plop" (squash, cut, short drop, landing squash); nothing crossfades between two different drawings of
Jonah. While his arms are crossed he fidgets with a slow grumpy sway. Bubble contents move inside the bubble's
own pop transform, and the puffy ring is drawn ON TOP of the contents (window cut out). Layers that cross the
window edge while they move (the ship sailing out, tiny Jonah running in) carry a window clip that stays put
on stage: the run is a set of planted drawings, and the ship is a flipbook whose drawings have the clip
pre-shifted against its travel (one per 40 px), so the clip edge always lies under the ring. God's light: the
cloud bank drifts in from the east during line 3 (the thought bubbles use that sky before), then parts in
line 4. All timings come from ctx.lines / chunks (phrase positions inside a chunk are estimated from the
character index, so they follow a re-generated voice). Camera: few long sine moves, peak ~11 output px / frame.
"""
from contextlib import contextmanager
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
BX, BY, RX, RY = 2300, 528, 282, 170      # thought-bubble window (centre, radii)
GAP = (2230, 262)            # where the clouds part for God's light (s20 maps its opening light from here)
SUN = (560, 312)             # whole sun + rays inside the frame during the line-3 pull-back, off it when close
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


def phrase_t(line, phrase, frac=0.0):
    """Start of ``phrase`` inside its subtitle chunk, estimated by its character index in that chunk. If the
    narration was edited and the phrase is gone, fall back to ``frac`` of the way through the line (so the
    build never breaks; the beat just lands near where it used to be)."""
    for c in line.chunks:
        i = c.text.find(phrase)
        if i >= 0:
            n = max(1, len(c.text.rstrip("，。！？：；、")))
            return c.start + (c.end - c.start) * i / n
    return line.start + (line.end - line.start) * frac


# a scene-local face for the "hmph!" (eyes shut, chin up) — registered only while this scene's drawings are built
_EXTRA_EXPRS = {"hmph": dict(eyes="closed", brow=(0.12, -0.05, 0.04), mouth="grumpy")}


@contextmanager
def _local_exprs():
    added = [k for k in _EXTRA_EXPRS if k not in CH.EXPRS]
    for k in added:
        CH.EXPRS[k] = _EXTRA_EXPRS[k]
    try:
        yield
    finally:
        for k in added:
            CH.EXPRS.pop(k, None)


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
    # arms re-crossed tighter and higher, chin sunk lower (the grumpy fidget in line 3)
    "sulk_b": CH._P(t=0, h=20, legs=(("ik", 76, 1), ("ik", 86, 1)),
                    arms=(("ik", "torso", -0.05, 0.48, 1), ("ik", "torso", 1.12, 0.44, 1)), far_front=True,
                    expr="angry", **CH._SEATED),
    # leaning toward the city, head up, glaring at it (use with facing -1)
    "sulk_glare": CH._P(t=5, h=-2, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True,
                        expr="angry", look=(0.08, -0.01), **CH._SEATED),
    # "hmph!": leaning back, nose in the air, eyes shut
    "sulk_hmph": CH._P(t=-7, h=-22, legs=(("ik", 76, 1), ("ik", 86, 1)), arms=_CROSS, far_front=True,
                       expr="hmph", **CH._SEATED),
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
    defs += S.rad_grad("hgc", [(0, "#fffef6", 0.92), (0.5, "#fff4cc", 0.6), (1, "#ffe9a8", 0)])
    body = f'<ellipse cx="{gx}" cy="{gy + 30}" rx="560" ry="330" fill="url(#hg)"/>'
    # a bright core inside the parted clouds, so the light visibly comes out of the gap
    body += f'<ellipse cx="{gx}" cy="{gy + 24}" rx="320" ry="170" fill="url(#hgc)"/>'
    body += f'<ellipse cx="{gx}" cy="{gy + 24}" rx="240" ry="125" fill="#fffaf0" opacity="0.8" filter="url(#blur-md)"/>'
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


def wall_svg():
    """The city wall with the open gate and the corner tower. No festival decorations: the city was spared,
    but the people are still in sackcloth (s18 / s20) — the joy is in their cheering and in the light."""
    body = PR.city_wall(-60, WX1, WY, WH, gate=(GX, GW), doors_open=1.0, seed=4)
    body += corner_tower(TOWER[0], WY + 4, WH + 76, TOWER[1])
    return doc(body)


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
    # (no bush right behind Jonah: it read as a pouch at his elbow / an earring when he sits)
    for x, y, s, v in [(1720, 1030, 0.36, 2), (2230, 990, 0.32, 0), (2380, 984, 0.3, 1)]:
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


# ------------------------------------------------------------------ Jonah's bundle (copied from s20_booth)
# s20 opens with this bundle lying beside him (its bundle_local(0), scale 1.25 on its stage, centre 210 px right
# of and 22 px above his anchor). Mapped through s20's matched opening view (s20 px per s19 px = 1.25 / 1.2)
# that is scale 1.2 here, centre (JX + 201.6, JY - 21.1).
ROPE = S.mix(P["sackcloth"], P["sand"], 0.3)
CLOTH = S.mix(P["headcloth"], P["sand"], 0.3)
BUN = (JX + 210 * 1.2 / 1.25, JY - 22 * 1.2 / 1.25)


def _btube(pts, w, col, sw=3.2):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * sw:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def bundle_local():
    """s20's bundle_local(state=0): booth sticks tied with rope plus the striped cloth rolled up, centred on
    (0, 0) at scale 1 (axis along x)."""
    rnd = random.Random(5)
    cols = [P["wood"], P["wood_dark"], P["wood_light"], P["wood"], S.shade(P["wood"], -0.12)]
    offs = [(-15, 0), (7, 1), (-5, 2), (15, 3), (2, 4)]
    out = ""
    for o, ci in offs:
        e0, e1, j = rnd.uniform(-0.05, 0.04), rnd.uniform(-0.06, 0.06), rnd.uniform(-2.5, 2.5)
        out += _btube([(-130 * (1 + e1), o), (0, o + j), (130 * (1 + e0), o)], 8.5, cols[ci], 3)
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
    for bx in (73, -47):
        out += _btube([(bx + 2, -23), (bx - 2, 50)], 6, ROPE, 3)
    return out


def bundle_svg():
    x, y = BUN
    k = 1.2 / 1.25
    sh = CH.ground_shadow(x, JY + 26 * k, k, width=300, opacity=0.22)
    return doc(sh + f'<g transform="translate({x:.1f},{y:.1f}) scale(1.2) rotate(180)"><g filter="url(#wobble-fine)">'
               f'{bundle_local()}</g></g>')


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


def win_clip(cid, inset=0, dx=0.0):
    """Clip to the bubble window (grown by -inset), optionally shifted right by dx (see flash_ship_frames)."""
    return (f'<clipPath id="{cid}"><ellipse cx="{f1(BX + dx)}" cy="{BY}" rx="{RX - inset}" ry="{RY - inset}"/>'
            f'</clipPath>')


# flashback (bubble 1): Joppa harbour, the ship to Tarshish, tiny Jonah dashing along the pier
SS = 0.28                                   # flashback scale (ship and tiny Jonah)
WL = BY + 108                               # the ship's waterline
SHIP_X = BX - 75                            # ship anchor (facing -1: sails west / left)
DECK_Y = WL + PR.SHIP_DECK_Y * SS           # feet of people standing on deck
PIER_Y = DECK_Y                             # pier planks level with the deck
PIER_X0 = SHIP_X + 182                      # pier end, just clear of the stern and the steering oar
RUN_STEP = 150 * SS                         # stage px per run drawing (one stride per drawing)
RUN_N = 5                                   # strides from under the ring (right) to the pier end
RUN_XS = [BX + 300 - k * RUN_STEP for k in range(RUN_N)]
RUN_DT = 0.16                               # s per stride: ~260 stage px / s — a real dash
LAND_X = BX - 32                            # where he lands on deck
CLIP_STEP = 40                              # the ship's window clip is re-centred every 40 px of travel...
SAIL_DX = 400                               # ...over its whole sail-off (it leaves the window completely)
N_CLIP = int(SAIL_DX / CLIP_STEP) + 2


def flash_back_svg():
    defs = (win_clip("w1") +
            S.lin_grad("fsky", [(0, "#a9d4e4"), (0.6, "#dcefe8"), (1, "#f6efd6")], 0, 0, 0, 1) +
            S.lin_grad("fsea", [(0, P["sea_light"]), (1, P["sea"])]))
    inner = f'<rect x="{BX - RX}" y="{BY - RY}" width="{2 * RX}" height="{2 * RY}" fill="url(#fsky)"/>'
    inner += S.cloud(BX - 175, BY - 122, 120, 40, "#fffaf0", seed=4, sw=2.5, shade_fill="#dbe9ee")
    inner += S.cloud(BX + 150, BY - 130, 90, 32, "#fffaf0", seed=6, sw=2.5, shade_fill="#dbe9ee")
    # Joppa's hill on the right (east), a few tiny houses
    inner += V2._ridge([(BX + 70, BY + 12), (BX + 170, BY - 46), (BX + 275, BY - 60), (BX + RX + 40, BY - 36)],
                       S.mix(P["grass"], P["sand"], 0.45), 2.5)
    for hx, hy, s in [(BX + 170, BY - 40, 0.075), (BX + 226, BY - 52, 0.085), (BX + 272, BY - 46, 0.07)]:
        inner += PR.house(hx, hy, s, variant=0)
    inner += (f'<path d="{S.wave_band(BY - 6, 3, 90, 0, BX - RX - 20, BX + RX + 20, BY + RY + 20)}" fill="url(#fsea)" '
              f'stroke="{INK}" stroke-width="2.5"/>')
    for i in range(6):
        x = BX - 250 + i * 84
        inner += (f'<path d="M{x},{BY + 26 + (i % 3) * 22} q14,-6 28,0" fill="none" stroke="{P["foam"]}" '
                  f'stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
    # pier (planks level with the ship's deck), a crate at its far end
    pier = ""
    for px in range(int(PIER_X0 + 14), int(BX + RX + 40), 46):
        pier += (f'<rect x="{px - 6}" y="{f1(PIER_Y)}" width="12" height="{f1(BY + RY + 10 - PIER_Y)}" '
                 f'fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="2.5"/>')
    pier += (f'<rect x="{f1(PIER_X0)}" y="{f1(PIER_Y - 2)}" width="{f1(BX + RX + 60 - PIER_X0)}" height="14" '
             f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>')
    pier += PR.crate(BX + 258, PIER_Y - 16, 0.26)
    inner += pier
    body = f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 30}" ry="{RY + 26}" fill="#fff8ea"/>'
    body += f'<g clip-path="url(#w1)">{S.g(inner, filter="wobble-fine")}</g>'
    halo = S.rad_grad("fh", [(0, "#fff7dc", 0.8), (0.6, "#fff0c8", 0.35), (1, "#ffe9b0", 0)])
    return doc(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 150}" ry="{RY + 120}" fill="url(#fh)"/>' + body, defs + halo)


def _ship_part(part):
    return PR.ship(SHIP_X, WL, SS, -1, sail="full", part=part, lantern=False)


def tiny_jonah(x, y, pose):
    return jfig(x, y, SS, -1, pose=pose, expr="worried")


def flash_ship_frames():
    """Frame 0: the ship (back part) before Jonah is aboard. Frames 1..N_CLIP: back part + Jonah standing on deck
    + front part, with the window clip pre-shifted k * CLIP_STEP to the right, so that while the layer has
    travelled about -k * CLIP_STEP (the sail-off) its clip sits on the window and the clip's edge stays under
    the ring (radius RX + 30 +- 20 px, the ring covers to beyond RX + 55)."""
    back, front = _ship_part("back"), _ship_part("front")
    frames = [doc(f'<g clip-path="url(#sc0)">{back}</g>', win_clip("sc0", -30))]
    aboard = back + tiny_jonah(LAND_X, DECK_Y, "stand") + front
    for k in range(N_CLIP):
        cid = f"sc{k + 1}"
        frames.append(doc(f'<g clip-path="url(#{cid})">{aboard}</g>', win_clip(cid, -30, k * CLIP_STEP)))
    return frames


def flash_ship_front_svg():
    return doc(f'<g clip-path="url(#w1b)">{_ship_part("front")}</g>', win_clip("w1b", -30))


def flash_run_frames():
    """Tiny Jonah's dash along the pier: one drawing per stride (run_a / run_b), each drawn where that stride
    lands (planted, nothing slides) and clipped to the window, so he comes out from under the ring."""
    out = []
    for k, x in enumerate(RUN_XS):
        cid = f"rn{k}"
        out.append(doc(f'<g clip-path="url(#{cid})">{tiny_jonah(x, PIER_Y, ("run_a", "run_b")[k % 2])}</g>',
                       win_clip(cid, -4)))
    return out


def flash_sea_front_svg():
    d = S.wave_band(WL + 4, 4, 70, 0.6, BX - RX - 30, BX + RX + 30, BY + RY + 30)
    body = f'<path d="{d}" fill="{S.mix(P["sea_light"], P["sea"], 0.45)}" stroke="{INK}" stroke-width="2.5"/>'
    body += (f'<path d="{S.wave_line(WL + 4, 4, 70, 0.6, BX - 270, BX + 270)}" fill="none" stroke="{P["foam"]}" '
             f'stroke-width="4" opacity="0.8"/>')
    return doc(f'<g clip-path="url(#w1c)">{S.g(body, filter="wobble-fine")}</g>', win_clip("w1c", -24))


# memory (bubble 2): God's kindness — a glowing heart; a grey cloud over a tiny Nineveh turns gold and pops
HEART = (BX - 112, BY - 52)
HEART_W = 112
MCLOUD = (BX + 104, BY - 14)
CITY_Y = BY + 134                           # the tiny city's ground line


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
    body = f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 30}" ry="{RY + 26}" fill="#fff0c8"/>'
    body += f'<g clip-path="url(#w2)">{S.g(inner, filter="wobble-fine")}</g>'
    return doc(f'<ellipse cx="{BX}" cy="{BY}" rx="{RX + 190}" ry="{RY + 160}" fill="url(#mh)"/>' + body, defs)


def memory_city_svg():
    """The tiny Nineveh on its plain — in front of the gold glow that rises behind it when the cloud pops."""
    inner = PR.nineveh_skyline(BX - RX + 10, BX + RX - 10, CITY_Y, 0.18, seed=2, haze=0.12, tint="#f6dcae")
    inner += V2._ridge([(BX - RX - 40, CITY_Y + 2), (BX, CITY_Y - 2), (BX + RX + 40, CITY_Y + 4)],
                       S.mix(P["grass"], P["sand"], 0.4), 2.5)
    return doc(f'<g clip-path="url(#w2c)">{S.g(inner, filter="wobble-fine")}</g>', win_clip("w2c"))


def city_glow_svg():
    """Warm gold sunrise-like glow in the sky BEHIND the tiny city (not a wash over its buildings)."""
    defs = (win_clip("w2g", 2) +
            S.rad_grad("cg", [(0, "#ffc83e", 0.95), (0.4, "#ffd25e", 0.6), (0.75, "#ffdc84", 0.22),
                              (1, "#ffe09a", 0)]))
    body = f'<ellipse cx="{BX + 20}" cy="{CITY_Y - 52}" rx="330" ry="160" fill="url(#cg)"/>'
    return doc(f'<g clip-path="url(#w2g)">{body}</g>', defs)


TWINKLES = [(BX - 160, CITY_Y - 96, 14), (BX + 6, CITY_Y - 124, 17), (BX + 168, CITY_Y - 88, 13),
            (BX + 86, CITY_Y - 168, 11), (BX - 70, CITY_Y - 150, 10)]


def star_d(x, y, r):
    k = 0.3 * r
    return (f"M{f1(x)},{f1(y - r)} Q{f1(x + k * 0.3)},{f1(y - k)} {f1(x + r)},{f1(y)} "
            f"Q{f1(x + k * 0.3)},{f1(y + k)} {f1(x)},{f1(y + r)} Q{f1(x - k * 0.3)},{f1(y + k)} {f1(x - r)},{f1(y)} "
            f"Q{f1(x - k * 0.3)},{f1(y - k)} {f1(x)},{f1(y - r)} Z")


def twinkle_svg(idx):
    out = ""
    for i in idx:
        x, y, r = TWINKLES[i]
        out += f'<path d="{star_d(x, y, r)}" fill="#fff4b8" stroke="#d99a2b" stroke-width="2.6" stroke-linejoin="round"/>'
    return doc(S.g(out, filter="wobble-fine"))


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


def beam_origin():
    """Where the heart's three rays start (its edge toward the cloud) and their direction."""
    hx, hy = HEART
    cx, cy = MCLOUD
    ang = math.degrees(math.atan2(cy + 8 - (hy + 6), cx - hx))
    ex = hx + HEART_W * 0.40 * math.cos(math.radians(ang))
    ey = hy + 6 + HEART_W * 0.40 * math.sin(math.radians(ang))
    return ex, ey, ang


def _wedge(x0, y0, ang, length, w0, w1):
    """A tapered ray from (x0, y0) along ``ang`` degrees: w0 wide at the start, w1 at the rounded far end."""
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    nx, ny = -s_, c
    x1, y1 = x0 + c * length, y0 + s_ * length
    tip = (x1 + c * w1 * 0.45, y1 + s_ * w1 * 0.45)
    return (f"M{f1(x0 + nx * w0 / 2)},{f1(y0 + ny * w0 / 2)} L{f1(x1 + nx * w1 / 2)},{f1(y1 + ny * w1 / 2)} "
            f"Q{f1(tip[0] + nx * w1 * 0.5)},{f1(tip[1] + ny * w1 * 0.5)} {f1(tip[0])},{f1(tip[1])} "
            f"Q{f1(tip[0] - nx * w1 * 0.5)},{f1(tip[1] - ny * w1 * 0.5)} {f1(x1 - nx * w1 / 2)},{f1(y1 - ny * w1 / 2)} "
            f"L{f1(x0 - nx * w0 / 2)},{f1(y0 - ny * w0 / 2)} Z")


def heart_beam_svg():
    """Three distinct golden rays fanning from the heart onto the grey cloud (drawn above the cloud): a warm
    glow, a gold body and a pale core in each, soft-edged like light."""
    ex, ey, ang = beam_origin()
    cx, cy = MCLOUD
    dist = math.hypot(cx - ex, cy - ey)
    rays = [(ang - 7.5, dist - 22), (ang, dist + 4), (ang + 7.5, dist - 22)]
    body_d = " ".join(_wedge(ex, ey, a, ln, 7, 26) for a, ln in rays)
    core_d = " ".join(_wedge(ex, ey, a, ln - 6, 2.5, 9) for a, ln in rays)
    defs = (f'<linearGradient id="hbm" gradientUnits="userSpaceOnUse" x1="{f1(ex)}" y1="{f1(ey)}" x2="{f1(cx)}" '
            f'y2="{f1(cy)}"><stop offset="0" stop-color="#ffc533"/><stop offset="1" stop-color="#ffdb5c"/>'
            f'</linearGradient>'
            f'<filter id="bglow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>'
            f'<filter id="bsoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6"/>'
            f'</filter>')
    body = (f'<path d="{body_d}" fill="#ffd34d" stroke="#ffd34d" stroke-width="16" stroke-linejoin="round" '
            f'opacity="0.55" filter="url(#bglow)"/>')
    body += f'<path d="{body_d}" fill="url(#hbm)" opacity="0.9" filter="url(#bsoft)"/>'
    body += f'<path d="{core_d}" fill="#fff6cf" opacity="0.9" filter="url(#bsoft)"/>'
    return doc(body, defs)


def rain_svg(phase):
    """Rain streaks and the lightning bolt under the grey cloud (own layer: it stops before the cloud turns
    gold). ``phase`` 0 / 1 shifts the streaks so the rain falls."""
    cx, cy = MCLOUD
    body = ""
    for i in range(5):
        x = cx - 60 + i * 30
        y0 = cy + 22 + (12 if (i + phase) % 2 else 0)
        body += (f'<path d="M{x},{y0} l-8,26" stroke="#7d8aa0" stroke-width="4" stroke-linecap="round" '
                 f'opacity="0.85"/>')
    body += (f'<path d="M{cx + 18},{cy + 22} l-14,22 l12,0 l-12,24" fill="none" stroke="{INK}" stroke-width="7" '
             f'stroke-linejoin="round" stroke-linecap="round"/>'
             f'<path d="M{cx + 18},{cy + 22} l-14,22 l12,0 l-12,24" fill="none" stroke="#f6d35a" stroke-width="3.5" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble-fine"))


def storm_cloud_svg(gold):
    """The memory cloud: grey (frame 0) or gold (frame 1) — the SAME outline, so the colour swap reads as the
    cloud changing, not as two clouds."""
    cx, cy = MCLOUD
    if gold:
        body = S.cloud(cx, cy, 136, 50, "#ffd970", seed=21, sw=3, shade_fill="#f2b64c")
        body += (f'<path d="M{cx - 40},{cy - 10} q18,-14 40,-8" fill="none" stroke="#fff4c8" stroke-width="5" '
                 f'stroke-linecap="round" opacity="0.9"/>')
    else:
        body = S.cloud(cx, cy, 136, 50, "#a9a7b3", seed=21, sw=3, shade_fill="#86849a")
        body += (f'<path d="M{cx - 30},{cy - 2} c8,-12 18,8 26,-4 s16,10 24,-2" fill="none" stroke="#6f6d7d" '
                 f'stroke-width="3.5" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble-fine"))


def melt_puffs_svg():
    """A ring of little white puffs: scaled up from the cloud's centre it bursts outward as the cloud pops."""
    cx, cy = MCLOUD
    out = ""
    for i, r in enumerate((17, 13, 15, 12, 16, 13, 14)):
        a = 2 * math.pi * i / 7 + 0.3
        x, y = cx + 64 * math.cos(a), cy + 34 * math.sin(a)
        out += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="#fffaf0" stroke="{P["ink_soft"]}" '
                f'stroke-width="3"/>')
    return doc(S.g(out, filter="wobble-fine"))


def trail_svg(i, cream="#fff8ea"):
    x, y, r = TRAIL[i]
    return doc(S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cream}" stroke="{INK}" stroke-width="5"/>',
                   filter="wobble-fine"))


TRAIL = [(1915, 760, 12), (1960, 726, 17), (2008, 698, 21)]


# ------------------------------------------------------------------ God's light
RAY_TARGET = (JX, JY - 140)       # Jonah's head / chest: he sits in the middle of the beam
RAY_GRAD_Y1 = JY + 130            # where the rays' gradient ends (the ground)


def ray_defs():
    gy = GAP[1]
    return (f'<linearGradient id="rayg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{RAY_GRAD_Y1}">'
            f'<stop offset="0" stop-color="#fff6d2" stop-opacity="0.92"/>'
            f'<stop offset="0.6" stop-color="#ffeaa8" stop-opacity="0.6"/>'
            f'<stop offset="1" stop-color="#ffe08e" stop-opacity="0.16"/></linearGradient>')


def ray_main():
    gx, gy = GAP
    tx, ty = RAY_TARGET
    return math.degrees(math.atan2(ty - gy, tx - gx)), math.hypot(tx - gx, ty - gy) + 330


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
            f'<linearGradient id="coneg" gradientUnits="userSpaceOnUse" x1="0" y1="{gy}" x2="0" y2="{RAY_GRAD_Y1}">'
            f'<stop offset="0" stop-color="#fff2c4" stop-opacity="0.6"/>'
            f'<stop offset="1" stop-color="#ffe39a" stop-opacity="0.22"/></linearGradient>' +
            S.rad_grad("pool", [(0, "#fff1c0", 0.85), (0.6, "#ffe39a", 0.35), (1, "#ffd77e", 0)]) +
            S.rad_grad("halo", [(0, "#fff6d6", 0.75), (0.6, "#ffe7a4", 0.32), (1, "#ffe0a0", 0)]))
    body = f'<path d="{V2._fan(gx, gy + 10, length, [main], [13])}" fill="url(#coneg)" filter="url(#blur-lg)"/>'
    body += f'<ellipse cx="{JX + 20}" cy="{f1(JY - 125 * JS)}" rx="{f1(200 * JS)}" ry="{f1(190 * JS)}" fill="url(#halo)"/>'
    body += f'<ellipse cx="{JX + 20}" cy="{JY + 2}" rx="{f1(260 * JS)}" ry="{f1(58 * JS)}" fill="url(#pool)"/>'
    return doc(body, defs)


def warm_svg():
    defs = S.rad_grad("warm", [(0, "#3a2a0c", 1), (0.5, "#1e1505", 0.85), (1, "#100800", 0)])
    return doc(f'<ellipse cx="{GAP[0] - 200}" cy="700" rx="800" ry="700" fill="url(#warm)"/>', defs)


# ------------------------------------------------------------------ people & creatures
WALL_TOP = WY - WH
WALK_PEOPLE = [  # (x, feet y, kind, variant, facing) on the wall walk / tower tops (feet behind the parapet)
    (262, WY - WH - 90 + 76, "man", 0, 1), (352, WY - WH + 30, "child", 2, 1), (800, WY - WH + 26, "woman", 1, 1),
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


def thin_hops(hops, a, b, gap):
    """Keep at most one hop group every ``gap`` s inside [a, b]: the crowd cheers less while Jonah speaks."""
    out, last, prev_end, keep = [], -99.0, -99.0, True
    for t0, d in hops:
        if t0 - prev_end > 0.1:                         # a new group of hops starts
            inside = a <= t0 <= b
            keep = (not inside) or (t0 - last >= gap)
            if keep and inside:
                last = t0
        if keep:
            out.append((t0, d))
        prev_end = t0 + d
    return out


def sheep_parts_sack(x, y, s, f):
    """V2._sheep_parts for a sheep in its sackcloth blanket (as in s18 / s20): (body markup, head markup)."""
    full = PR.animal(x, y, s, f, kind="sheep", sackcloth=True)
    i = full.find("rotate(-24 54 -110)")
    j = full.rfind("<ellipse", 0, i) if i >= 0 else -1
    k = full.find("<g transform=")
    k = full.find(">", k) + 1 if k >= 0 else 0
    if j <= k or not full.endswith("</g></g>"):
        return full, ""
    return full[:j] + "</g></g>", full[:k] + full[j:]


# ------------------------------------------------------------------ build
def build(ctx):
    with _local_exprs():            # the scene-local "hmph" face exists only while the drawings are built
        return _build(ctx)


def _build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    L0, L1, L2, L3, L4, L5 = L[0], L[1], L[2], L[3], L[4], L[5]

    # ---------------------------------------------------------------- beats (all from the narration)
    t_pan0 = L0.chunks[1].start - 0.3               # "只有约拿…" the camera glides to Jonah
    t_pan1 = L0.chunks[1].start + 2.6
    t_huff0 = L0.chunks[1].start + 1.5              # grumpy huff while the camera arrives
    t_stamp = L0.chunks[2].start + 0.12             # "他非常生气" stamps, anger mark
    t_lookup = phrase_t(L0, "对上帝说", 0.75)       # lifts his face to heaven
    t_arms = L1.start + 0.02                        # "耶和华啊" arms up
    t_wide = phrase_t(L1, "我早就知道", 0.12)       # arms flung wide
    t_b1 = L1.chunks[1].start - 0.32                # flashback bubble pops up ("所以我才急忙逃到他施去")
    t_watch = L1.chunks[1].start + 0.05             # Jonah looks up at it, arms crossed
    t_b1_out = L2.start + 0.3                       # the flashback pops away on "因为我知道"
    # tiny Jonah dashes along the pier on "急忙", leaps aboard on "他施", the ship sails off right after
    t_run0 = min(max(phrase_t(L1, "急忙", 0.65) - 0.1, t_b1 + 0.55), t_b1_out - 2.1)
    t_leap = t_run0 + RUN_N * RUN_DT
    t_land = t_leap + 0.4
    t_sail0, t_sail1 = t_land + 0.12, t_b1_out + 0.3
    t_shrug = L2.start + 0.02                       # "因为我知道" palms out
    t_b2 = max(phrase_t(L2, "你又慈爱", 0.15) - 0.15, t_b1_out + 0.45)   # memory bubble
    t_beat1 = phrase_t(L2, "慈爱", 0.2)
    t_beat2 = phrase_t(L2, "宽容", 0.28)
    t_wide2 = L2.chunks[1].start + 0.02             # "不轻易生气" arms wide again
    t_grey = phrase_t(L2, "你说要降下", 0.45)       # grey cloud gathers over the tiny city
    t_shrug2 = L2.chunks[2].start + 0.02            # "只要人一认错"
    t_melt = phrase_t(L2, "你就不忍心", 0.78)       # three golden rays shoot from the heart onto the cloud
    t_gold = t_melt + 0.15                          # the rain stops, the cloud turns gold...
    t_pop = t_melt + 0.75                           # ...and pops into white puffs; gold glow behind the city
    t_cross = t_pop + 0.45                          # arms crossed + huff
    t_b2_out = L2.end + 0.2
    t_sit = L3.start + 0.05                         # "原来" plops down, sulking
    c1 = L3.chunks[1]
    t_fidget = c1.start + 0.5 * (c1.end - c1.start)  # re-crosses his arms tighter, with a huff
    t_eye = L3.chunks[2].start + 0.05               # "可是他不愿意…" hop-turn: glares at the cheering city
    t_front = L3.chunks[3].start + 0.05             # "所以当初才逃跑了" hops back: "hmph!", nose in the air
    t_unhmph = min(t_front + 1.1, L4.start - 0.3)   # eyes open, chin down again
    t_light = L4.start - 0.1                        # "于是，上帝问约拿" clouds part, light pours down
    t_glance = L5.start + 0.08                      # "约拿，" he looks up into the light
    t_turn = min(phrase_t(L5, "对吗", 0.8) + 0.2, T - 1.6)  # turns his back to the light without answering

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
    quiet = (L1.start - 0.3, L2.end + 0.4)          # the crowd cheers less while Jonah complains

    # people on the wall walk (behind the parapet), in sackcloth, cheering now and then
    for i, (x, fy, kind, var, fc) in enumerate(WALK_PEOPLE):
        s = 0.42
        frames = [doc(CH.citizen(x, fy, s, fc, kind=kind, variant=var, pose=p, attire="sackcloth",
                                 expr="happy" if p == "stand" else None)) for p in ("stand", "cheer")]
        hops = thin_hops(V12.hop_sched(70 + i, T, n=(1, 2), dur=(0.5, 0.8), rest=(1.0, 2.6)), *quiet, 5.0)
        sc.add(f"walk{i}", frames, frame_at=V12.hop_frame(hops, 0.12, 0.25), wc=0.5,
               motion=V12.hop_motion(x, fy, hops, 9))

    sc.add("wall", wall_svg(), wc=0.8)
    sc.add("plain", plain_svg(), wc=0.8)

    # sheep in their sackcloth blankets grazing by the wall (hooves planted, heads nod)
    for i, (x, y, s, f) in enumerate(SHEEP):
        body, head = sheep_parts_sack(x, y, s, f)
        br = M.breathe(0.012, 2.6 + 0.3 * i, pivot=(x, y), phase=0.3 * i)
        sc.add(f"sheep{i}", doc(CH.ground_shadow(x, y, s, width=180, opacity=0.2) + body), motion=br)
        if head:
            nx, ny = PR.local_to_stage(x, y, s, f, *V2.SHEEP_NECK)
            ang = (lambda t, i=i: -7 * (0.5 + 0.5 * math.sin(2 * math.pi * t / (2.9 + 0.6 * i) - 1.3 * i)))
            sc.add(f"sheep{i}_head", doc(head), motion=lambda t, ang=ang, br=br, f=f, ny=ny, nx=nx, y=y: Tf(
                dy=-(br(t).sy - 1) * (y - ny), rot=-ang(t) * f, px=nx, py=ny))

    # the cheering crowd (still in sackcloth, happy faces)
    for i, (x, y, kind, var, fc, s, style) in enumerate(CROWD):
        frames = [doc(CH.citizen(x, y, s, fc, kind=kind, variant=var, pose=p, attire="sackcloth",
                                 expr="happy" if p == "stand" else None)) for p in ("stand", "cheer")]
        sc.add(f"crowd_sh{i}", doc(CH.ground_shadow(x, y, s, width=110 if kind == "child" else 120, opacity=0.2)),
               wc=0)
        if style == "hop":
            hops = thin_hops(V12.hop_sched(10 + i, T, n=(2, 3), dur=(0.4, 0.52), rest=(0.6, 1.3)), *quiet, 6.0)
            sc.add(f"crowd{i}", frames, frame_at=V12.hop_frame(hops), wc=0.5,
                   motion=V12.hop_motion(x, y, hops, 26 * s / 0.6))
        else:
            hops = thin_hops(V12.hop_sched(30 + i, T, n=(1, 1), dur=(0.9, 1.4), rest=(0.7, 1.6)), *quiet, 7.0)
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
    sc.add("bundle", bundle_svg(), wc=0.6)           # his booth sticks and cloth (s20 builds the booth)

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
            alpha=light_in(t) * (0.78 + 0.22 * (0.5 + 0.5 * math.sin(2 * math.pi * (t - t_light) / 2.2 + k * math.pi)))))

    # ---------------------------------------------------------------- JONAH
    # frames: 0 cross, 1 cross_up, 2 complain, 3 complain2, 4 shrug, 5 sit_sulk, 6 sulk_b (arms re-crossed),
    #         7 sulk looking up, 8 sit_sulk facing the city (the last frame; s20 starts on it), 9 glaring at
    #         the city, 10 "hmph!". (No blinks: the library's closed-eye faces 'sleepy' / 'peaceful' have a
    #         yawning / smiling mouth, which would flash a wrong mood.)
    jdefs = [("cross", None, 1), ("cross_up", None, 1), ("complain", None, 1), ("complain2", None, 1),
             ("shrug", None, 1), ("sit_sulk", None, 1), ("sulk_b", None, 1), ("sulk_up", None, 1),
             ("sit_sulk", None, -1), ("sulk_glare", None, -1), ("sulk_hmph", None, 1)]
    jframes = [doc(jfig(JX, JY, JS, f, pose=p, expr=e)) for p, e, f in jdefs]
    SIT0 = 5
    CROSSED = (0, 1, 5, 6, 8, 9, 10)
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
             (t_fidget, 6, 0.5, False, False),
             (t_eye, 9, 1.0, True, False),
             (t_front, 10, 0.9, False, True),
             (t_unhmph, 5, 0.35, False, False),
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

    # (time, anger mark?) grumpy huffs: steam puffs from his head, the anger mark on the angriest ones
    huffs = [(t_huff0, True), (t_stamp, True), (t_cross + 0.25, True), (t_fidget + 0.06, False),
             (t_eye + 0.12, True), (t_front + 0.1, False)]
    stamps = [t_stamp]

    def jonah_motion(t):
        s = 1 + 0.011 * math.sin(2 * math.pi * t / 3.1)
        sy = s
        rot = 0.0
        dy = 0.0
        for th, _a in huffs:                   # grumpy huff: a little squash
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
        # glaring at the cheering city: he leans toward it
        rot -= 2.2 * M.progress(t, t_eye + 0.15, t_eye + 0.5, "sine") * (1 - M.progress(t, t_front - 0.12, t_front - 0.01, "sine"))
        if base_frame(t) in CROSSED:           # grumpy fidget while his arms are crossed (s20 replays it)
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

    # grumpy steam puffs (+ anger mark on the angriest huffs), placed by the head of the drawing at that time
    for hi, (th, anger) in enumerate(huffs):
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
        if not anger:
            continue
        ax, ay = hx0 + 52 * f, hy0 - 62            # on the face side of the head

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

    def ship_dx(t):
        return -SAIL_DX * M.progress(t, t_sail0, t_sail1, "sine")

    def ship_dy(t):
        dip = 4 * math.sin(math.pi * _clamp((t - t_land) / 0.35)) if t >= t_land else 0.0   # he lands: it dips
        return 3 * math.sin(2 * math.pi * t / 1.7) + dip

    def ship_local(t):
        return Tf(dx=ship_dx(t), dy=ship_dy(t), rot=1.2 * math.sin(2 * math.pi * t / 2.3), px=SHIP_X, py=WL)

    def ship_frame(t):
        if t < t_land:
            return 0.0
        return float(1 + min(N_CLIP - 1, int(round(-ship_dx(t) / CLIP_STEP))))

    sc.add("b1_ship", flash_ship_frames(), frame_at=ship_frame, motion=in_bubble(t_b1, t_b1_out, ship_local), wc=0.4)

    # tiny Jonah: planted strides along the pier, then the last stride's drawing flies on an arc onto the deck;
    # on landing the ship's own drawing (with him on deck) takes over
    def run_frame(t):
        return float(min(RUN_N - 1, max(0, int((t - t_run0) / RUN_DT))))

    def run_local(t):
        if t < t_run0 or t >= t_land:
            return Tf(alpha=0.0)
        if t < t_leap:
            u = ((t - t_run0) / RUN_DT) % 1.0
            return Tf(dy=-5 * math.sin(math.pi * u))
        u = (t - t_leap) / (t_land - t_leap)
        return Tf(dx=(LAND_X - RUN_XS[-1]) * u, dy=-52 * math.sin(math.pi * u) + (DECK_Y - PIER_Y) * u + u * ship_dy(t))

    sc.add("b1_jonah", flash_run_frames(), frame_at=run_frame, wc=0.3, motion=in_bubble(t_b1, t_b1_out, run_local))
    sc.add("b1_ship_front", flash_ship_front_svg(), wc=0.4, motion=in_bubble(
        t_b1, t_b1_out, lambda t: Tf(alpha=0.0) if t >= t_land else ship_local(t)))
    sc.add("b1_sea", flash_sea_front_svg(), wc=0.4,
           motion=in_bubble(t_b1, t_b1_out, lambda t: Tf(dx=6 * math.sin(2 * math.pi * t / 2.5))))
    sc.add("b1_ring", ring_front_svg("#fff8ea", "#f4e2c3", "#bfe0ea", 11), motion=in_bubble(t_b1, t_b1_out), wc=0.5)

    # bubble 2: God's kindness
    sc.add("b2_back", memory_back_svg(), motion=in_bubble(t_b2, t_b2_out), wc=0.5)
    sc.add("b2_cityglow", city_glow_svg(), wc=0, motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(
        alpha=M.progress(t, t_pop + 0.05, t_pop + 0.7, "sine") * (0.9 + 0.1 * math.sin(2 * math.pi * (t - t_pop) / 1.6)),
        sy=0.8 + 0.2 * M.progress(t, t_pop, t_pop + 0.9, "out"), px=BX, py=CITY_Y)))
    sc.add("b2_city", memory_city_svg(), motion=in_bubble(t_b2, t_b2_out), wc=0.5)
    for k, idx in enumerate(((0, 2, 4), (1, 3))):       # twinkles over the saved city
        sc.add(f"b2_twinkle{k}", twinkle_svg(idx), wc=0, motion=in_bubble(t_b2, t_b2_out, lambda t, k=k: Tf(
            alpha=M.progress(t, t_pop + 0.2 + 0.2 * k, t_pop + 0.4 + 0.2 * k, "sine") *
            (0.6 + 0.4 * math.cos(2 * math.pi * (t - t_pop - 0.2 - 0.2 * k) / 0.9)))))

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

    def cloud_dx(t):
        return 40 * (1 - M.progress(t, t_grey, t_grey + 0.9, "out")) + 3 * math.sin(t * 2.2)

    # rain + bolt on their own layer: they stop as the rays reach the cloud
    sc.add("b2_rain", [rain_svg(0), rain_svg(1)], wc=0.3, frame_at=lambda t: float(int(t * 8) % 2),
           motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(dx=cloud_dx(t), alpha=M.progress(
               t, t_grey + 0.25, t_grey + 0.8, "sine") * (1 - M.progress(t, t_melt, t_gold + 0.15, "sine")))))

    def storm_local(t):
        a = M.progress(t, t_grey, t_grey + 0.6, "sine")
        sx = sy = 1.0
        if t >= t_pop - 0.12:
            if t < t_pop:                   # anticipation squash
                v = M.progress(t, t_pop - 0.12, t_pop, "sine")
                sx, sy = 1 + 0.14 * v, 1 - 0.2 * v
            else:                           # pop: gone in 0.15 s (opaque all the way, never a see-through cloud)
                v = (t - t_pop) / 0.15
                if v >= 1:
                    return Tf(alpha=0.0)
                k = 1 - M.ease("sine")(v)
                sx, sy = 1.14 * k, 0.8 * k
        return Tf(dx=cloud_dx(t), sx=sx, sy=sy, alpha=a, px=mx_, py=my_)

    # grey -> gold: the same cloud outline in two colours
    sc.add("b2_storm", [storm_cloud_svg(False), storm_cloud_svg(True)], wc=0.4,
           frame_at=lambda t: M.progress(t, t_gold, t_gold + 0.35, "sine"),
           motion=in_bubble(t_b2, t_b2_out, storm_local))
    bx_, by_, _ba = beam_origin()
    sc.add("b2_beam", heart_beam_svg(), wc=0, motion=in_bubble(t_b2, t_b2_out, lambda t: Tf(
        sx=0.1 + 0.9 * M.progress(t, t_melt - 0.05, t_melt + 0.2, "out"),
        sy=0.1 + 0.9 * M.progress(t, t_melt - 0.05, t_melt + 0.2, "out"),
        alpha=M.progress(t, t_melt - 0.05, t_melt + 0.05, "sine") * (1 - M.progress(t, t_pop + 0.2, t_pop + 0.65, "sine"))
        * (0.9 + 0.1 * math.sin(t * 9)), px=bx_, py=by_)))

    def melt_local(t):
        u = t - t_pop
        if u < 0 or u > 0.75:
            return Tf(alpha=0.0)
        k = 0.4 + 1.1 * M.ease("out")(min(1.0, u / 0.55))
        return Tf(dx=cloud_dx(t), dy=-10 * M.ease("out")(u / 0.75), sx=k, sy=k,
                  alpha=1 - M.progress(u, 0.3, 0.75, "sine"), px=mx_, py=my_)

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

    # ---------------------------------------------------------------- CAMERA (the last key is s20's first view)
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
    # the cheering city: a very low bed under the whole scene (the crowd keeps cheering on the left), louder
    # while the city fills the frame
    sc.sfx("cheer", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0, pan=-0.45)
    sc.sfx("cheer", 0, dur=t_pan1 + 0.5, gain_db=-14, fade_in=0.8, fade_out=1.5, pan=-0.3)
    sc.sfx("cheer", L3.chunks[1].start + 0.5, dur=t_front - L3.chunks[1].start, gain_db=-19, fade_in=1.2,
           fade_out=1.2, pan=-0.4)
    sc.sfx("thud", t_stamp + 0.28, gain_db=-12, pan=0.2)
    sc.sfx("cloth", t_arms, gain_db=-14, pan=0.2)
    sc.sfx("cloth", t_shrug, gain_db=-15, pan=0.2)
    sc.sfx("pop", t_b1, gain_db=-11, pan=0.4)
    sc.sfx("footsteps_run", t_run0, dur=t_leap - t_run0, gain_db=-17, pan=0.45)
    sc.sfx("whoosh", t_leap, gain_db=-17, pan=0.4)
    sc.sfx("thud", t_land, gain_db=-21, pan=0.35)
    sc.sfx("pop", t_b1_out + 0.1, gain_db=-14, pan=0.4)
    sc.sfx("pop", t_b2, gain_db=-11, pan=0.4)
    sc.sfx("sparkle", t_b2 + 0.1, gain_db=-12, pan=0.4)
    sc.sfx("sparkle", t_melt, gain_db=-12, pan=0.45)
    sc.sfx("pop", t_pop, gain_db=-11, pan=0.45)
    sc.sfx("sparkle", t_pop + 0.15, gain_db=-14, pan=0.4)
    sc.sfx("pop", t_b2_out + 0.1, gain_db=-14, pan=0.4)
    sc.sfx("thud", t_sit + 0.08, gain_db=-8, pan=0.2)
    sc.sfx("cloth", t_fidget, gain_db=-16, pan=0.1)
    sc.sfx("thud", t_eye + 0.06, gain_db=-15, pan=0.1)
    sc.sfx("cloth", t_front, gain_db=-14, pan=0.1)
    sc.sfx("chime", L4.start, gain_db=-6, pan=0.2)
    sc.sfx("sparkle", L5.start + 0.2, gain_db=-13, pan=0.2)
    sc.sfx("cloth", t_turn, gain_db=-14, pan=0.2)
    return sc
