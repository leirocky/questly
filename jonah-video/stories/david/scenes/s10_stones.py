"""Scene 10 — five smooth stones (1 Samuel 17:40).

"大卫拿起放羊的杖，来到小溪边。他弯下腰，挑了五块光滑的石头。一块，两块，三块，四块，五块，都放进口袋里。他手里还拿
着一样东西：甩石头用的机弦。那是一根长长的带子，能把石头甩得又快又远。"

One 3000 x 1688 stage: a sunny morning in the Valley of Elah. Far away the two camps sit tiny on their hills (Israel
left, the Philistines right) with the valley floor between; from there a brook winds toward us and widens across
the meadow to the lower right, with reeds, pebbles, flat stepping stones and a dragonfly over the water.

  line 0  "大卫拿起放羊的杖，来到小溪边。"  David (staff in hand) walks in from the left across the meadow to the
                                            near bank (planted-foot walk), the camera following him in.
  line 1  "他弯下腰，"                     a hop down onto one knee at the water's edge, the staff laid on the bank;
          "挑了五块光滑的石头。"           his hands swish in the shallows, ripple rings, smooth stones glinting;
          "一块，两块，三块，四块，五块，"  one per counted word: he lifts a stone (it glints, a number badge 1..5 pops
                                            above it), then pops it into his bag; a row of five stone slots fills up.
          "都放进口袋里。"                 he pats the bag; the five little stones in the row bounce.
  line 2  "他手里还拿着一样东西："         he stands up, staff in one hand and the sling hanging from the other;
          "甩石头用的机弦。"               a round picture-book inset pops up showing the sling close: strap + pouch;
          "那是一根长长的带子，"           the strap swings in the inset and a length arrow runs along it;
          "能把石头甩得又快又远。"         the inset pops away; one gentle test swing (sling_spin), then the release
                                            sends a whoosh line far across the valley (an empty pouch - only air).
          Then he hops across the stepping stones and walks out of frame to the right, toward the valley; the
          brook stays calm (last second: no figure).
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
from stories.david.scenes import s08_saul as A
from stories.david.scenes.s08_saul import (INK, WALK_A, WALK_N, Actor, WalkPath, _P, clamp, f1, pop_k, pop_tf, pt,
                                           sprite, walk_adv, walk_drawings, walk_pose)

SW, SH = 3000, 1688
FY = 1390                      # David's ground line on the near bank
K = 1.4                        # person scale
VY = 780                       # far valley floor line (valley_elah)
VS = 0.42                      # far valley scale
D_A = A.DAVID_A
D_LK = A.DAVID_LK


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


# ------------------------------------------------------------------ the brook (perspective ribbon)
BROOK = [(1500, VY + 18), (1560, 880), (1700, 980), (1960, 1110), (2230, 1240), (2450, 1370), (2700, 1520),
         (2960, 1700), (3150, 1800)]


def _brook_w(i, n):
    u = i / (n - 1)
    return 22 + 470 * u ** 1.5


def brook_edges():
    pts = BROOK
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = _brook_w(i, n) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left, right


def brook_center(u):
    """Point on the centre line at parameter u 0..1 (piecewise linear)."""
    n = len(BROOK) - 1
    f = clamp(u) * n
    i = min(n - 1, int(f))
    k = f - i
    (x0, y0), (x1, y1) = BROOK[i], BROOK[i + 1]
    return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, _brook_w(i + k, n + 1)


def bank_x_at(y):
    """x of the brook's left (near-left) bank at stage y."""
    left, right = brook_edges()
    # left list here is the bank on the viewer's left (normal points right->left?) choose the smaller x
    edge = [min(l_, r_, key=lambda p: p[0]) for l_, r_ in zip(left, right)]
    for (x0, y0), (x1, y1) in zip(edge, edge[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return edge[-1][0]


def brook_svg(phase=0.0):
    left, right = brook_edges()
    poly = left + right[::-1]
    d = S.smooth_path(poly, closed=True, tension=0.8)
    defs = S.lin_grad("s10w", [(0, "#8cc9d6"), (0.5, "#4f9fbf"), (1, "#3c88ad")], x1=0, y1=0, x2=0.3, y2=1)
    out = f'<path d="{d}" fill="url(#s10w)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    # pebbly shallows along both edges
    rng = random.Random(4)
    for side in (left, right):
        for (x0, y0), (x1, y1) in zip(side, side[1:]):
            for k in range(3):
                u = rng.random()
                x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                s = 0.25 + 0.55 * (y - VY) / (SH - VY)
                out += (f'<ellipse cx="{f1(x + rng.uniform(-14, 14) * s)}" cy="{f1(y)}" rx="{f1(16 * s)}" '
                        f'ry="{f1(9 * s)}" fill="{S.mix("#b9b2a6", "#4f9fbf", 0.35)}" opacity="0.8"/>')
    return doc(S.g(out, filter="wobble"), defs)


RIP_N = 8                      # ripple flipbook frames (a loop)


def ripples_svg(k):
    """Foam ripple lines, loop frame k of RIP_N: each ripple drifts a little downstream while it fades in and out."""
    left, right = brook_edges()
    d = S.smooth_path(left + right[::-1], closed=True, tension=0.8)
    rip = ""
    rng = random.Random(9)
    for j in range(60):
        u0 = rng.random() * 0.97
        off = rng.uniform(-0.36, 0.36)
        ph = (k / RIP_N + rng.random()) % 1.0
        u = u0 + 0.045 * ph
        x, y, w = brook_center(u)
        s = 0.3 + 0.9 * u
        a = math.sin(math.pi * ph)
        rip += (f'<path d="M{f1(x + off * w - 26 * s)},{f1(y)} q{f1(26 * s)},{f1(-9 * s)} {f1(52 * s)},0" fill="none" '
                f'stroke="#eef8f5" stroke-width="{f1(3 + 3 * s)}" stroke-linecap="round" opacity="{0.9 * a:.2f}"/>')
    return doc(f'<clipPath id="s10wc"><path d="{d}"/></clipPath><g clip-path="url(#s10wc)">{rip}</g>')


def brook_span(y):
    """(left x, right x) of the water at stage y."""
    left, right = brook_edges()
    xs = []
    for side in (left, right):
        for (x0, y0), (x1, y1) in zip(side, side[1:]):
            if min(y0, y1) <= y <= max(y0, y1) and y1 != y0:
                xs.append(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
                break
    return (min(xs), max(xs)) if len(xs) == 2 else (bank_x_at(y), bank_x_at(y) + 300)


# ------------------------------------------------------------------ backdrop
def sky_svg():
    defs = (S.lin_grad("s10sky", [(0, "#8fcbe0"), (0.55, "#cbe7e6"), (1, "#f6ecc8")]) +
            S.rad_grad("s10sun", [(0, "#fff6d6", 0.9), (0.45, "#fdebc4", 0.35), (1, "#fdebc4", 0)]))
    body = S.rect_bg("url(#s10sky)", SW, SH)
    body += '<ellipse cx="520" cy="300" rx="760" ry="460" fill="url(#s10sun)"/>'
    body += S.g(f'<circle cx="520" cy="260" r="84" fill="{P["sun"]}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
                f'stroke-width="5"/><circle cx="492" cy="232" r="26" fill="#fff4cc" opacity="0.7"/>', filter="wobble-fine")
    return doc(body, defs)


def cloud_svg(i):
    items = [(1150, 200, 330, 92, 3), (2150, 140, 300, 84, 7), (2800, 330, 260, 74, 11), (300, 520, 230, 64, 5)]
    cx, cy, w, h, sd = items[i]
    return doc(S.g(S.cloud(cx, cy, w, h, "#fdf6e8", seed=sd, sw=3, shade_fill="#efe2d0"), filter="wobble"))


def far_svg():
    """Hazy blue ridges, then the Valley of Elah small and far away: both camps tiny on their hills."""
    ridge = S.mix("#a9bfd0", "#e9e3d6", 0.35)
    body = S.path(S.hill(-200, 1700, VY - 60, 190, seed=3, bumps=3, bottom=VY + 200), fill=ridge, sw=2.6)
    body += S.path(S.hill(1300, 3200, VY - 50, 170, seed=8, bumps=3, bottom=VY + 200), fill=ridge, sw=2.6)
    out = S.g(body, filter="wobble")
    out += PR._haze(PR.valley_elah(-300, 3300, VY, VS, seed=2, brook=False), S.mix(P["sky_day"], "#f6ecc8", 0.5),
                    0.22, 0.12)
    return doc(out)


def meadow_svg():
    defs = S.lin_grad("s10m", [(0, "#a9c86a"), (0.45, "#93b85c"), (1, "#7ea24c")])
    top = 905
    pts = [(-60, top + 30), (400, top - 10), (900, top + 6), (1300, top - 4), (1700, top + 2), (2300, top - 14),
           (2800, top + 10), (3060, top)]
    d = S.smooth_path(pts, closed=False) + f" L3060,{SH + 40} L-60,{SH + 40} Z"
    out = f'<path d="{d}" fill="url(#s10m)" stroke="{INK}" stroke-width="5"/>'
    rng = random.Random(21)
    for i in range(70):
        x, y = rng.uniform(0, SW), rng.uniform(top + 30, SH)
        s = 0.4 + 0.8 * (y - top) / (SH - top)
        out += (f'<path d="M{f1(x)},{f1(y)} q{f1(6 * s)},{f1(-16 * s)} {f1(12 * s)},0 m{f1(6 * s)},0 '
                f'q{f1(5 * s)},{f1(-12 * s)} {f1(10 * s)},0" fill="none" stroke="{P["grass_dark"]}" '
                f'stroke-width="{f1(2 + 2 * s)}" opacity="0.6"/>')
    # a path of trodden earth toward the valley
    out += (f'<path d="M-60,{FY + 70} C500,{FY + 40} 1100,{FY - 60} 1500,{FY - 180} C1700,{FY - 240} 1550,{VY + 140} '
            f'1480,{VY + 60}" fill="none" stroke="#d8c08a" stroke-width="70" stroke-linecap="round" opacity="0.35"/>')
    return doc(S.g(out, filter="wobble"), defs)


STEPS = []                     # stepping stones across the brook (x, y, scale), filled in by bank_svg()


def bank_svg():
    """Pebbles on both banks, the picking spot's shallows, flat stepping stones, reeds and flowers."""
    out = ""
    rng = random.Random(5)
    left, right = brook_edges()
    for side, sgn in ((left, -1), (right, 1)):
        for (x0, y0), (x1, y1) in zip(side, side[1:]):
            for k in range(4):
                u = rng.random()
                x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                s = 0.25 + 1.1 * (y - VY) / (SH - VY)
                x += sgn * rng.uniform(4, 30) * s
                out += PR.stone(x, y + 6 * s, s * rng.uniform(0.7, 1.2), seed=rng.randint(0, 4))
    STEPS.clear()
    lx, rx = brook_span(FY + 6)
    for j in range(3):
        x = lx + (rx - lx) * (j + 1) / 4
        STEPS.append((x, FY + 6))
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(FY + 10)}" rx="58" ry="22" fill="#cfc6b6" stroke="{INK}" stroke-width="4"/>'
                f'<ellipse cx="{f1(x - 14)}" cy="{f1(FY + 2)}" rx="24" ry="6" fill="#fffaf0" opacity="0.6"/>')
    return doc(out)


def plants_svg(sway=0.0):
    out = ""
    for x, y, s, v in ((1905, 1080, 0.55, 0), (2140, 1215, 0.75, 1), (2870, 1290, 0.9, 0), (2420, 1140, 0.5, 1)):
        out += PR.reeds(x, y, s, variant=v, sway=sway)
    for x, y, s, v in ((150, 1180, 1.0, 2), (620, 1090, 0.8, 0), (980, 1250, 1.1, 2), (1500, 1060, 0.7, 2),
                       (1740, 1330, 1.0, 0), (2620, 1050, 0.6, 2)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sway * 0.6)
    out += PR.bush(420, 1010, 0.7, variant=0)
    out += PR.olive_tree(260, 990, 0.9, seed=4)
    return doc(out)


def fg_svg():
    out = ""
    for x, y, s, v in ((60, SH + 10, 1.6, 2), (330, SH + 30, 1.4, 0), (1250, SH + 40, 1.5, 2), (2000, SH + 30, 1.3, 0)):
        out += PR.grass_tuft(x, y, s, variant=v)
    out += S.g(S.path(S.blob(820, SH - 20, 150, 70, 0.12, 9, seed=3), fill="#c9bba2", sw=5)
               + f'<ellipse cx="790" cy="{SH - 66}" rx="60" ry="16" fill="#fffaf0" opacity="0.5"/>', filter="wobble")
    return doc(out)



# ------------------------------------------------------------------ little drawings
def dragonfly(x, y, s=1.0, wing=0):
    """A small blue dragonfly (wing 0 / 1 = two flap frames), body pointing right."""
    out = ""
    wa = 18 if wing == 0 else -12
    for dx, ln, a in ((-6, 46, -wa - 10), (-6, 46, wa + 10), (6, 40, -wa), (6, 40, wa)):
        r = math.radians(a)
        cx, cy = x + dx * s, y
        ex, ey = cx + ln * s * math.sin(r) * 0.35, cy - ln * s * math.cos(r)
        out += (f'<ellipse cx="{f1((cx + ex) / 2)}" cy="{f1((cy + ey) / 2)}" rx="{f1(9 * s)}" ry="{f1(ln * s / 2)}" '
                f'transform="rotate({a * 0.35 + (180 if a < 0 else 0):.1f} {f1((cx + ex) / 2)} {f1((cy + ey) / 2)})" '
                f'fill="#e6f4f6" fill-opacity="0.75" stroke="{INK}" stroke-width="{1.8 * s}"/>')
    out += (f'<path d="M{f1(x - 70 * s)},{f1(y + 2 * s)} L{f1(x + 4 * s)},{f1(y)}" stroke="#3f86b8" '
            f'stroke-width="{7 * s}" stroke-linecap="round"/>')
    out += f'<path d="M{f1(x - 70 * s)},{f1(y + 2 * s)} L{f1(x + 4 * s)},{f1(y)}" stroke="{INK}" stroke-width="{1.6 * s}" opacity="0.6"/>'
    out += f'<circle cx="{f1(x + 14 * s)}" cy="{f1(y)}" r="{f1(9 * s)}" fill="#3f86b8" stroke="{INK}" stroke-width="{2 * s}"/>'
    out += f'<circle cx="{f1(x + 18 * s)}" cy="{f1(y - 3 * s)}" r="{f1(3 * s)}" fill="{INK}"/>'
    return S.g(out, filter="wobble-fine")


def bird(x, y, s=1.0, up=True):
    k = -1 if up else 0.4
    return (f'<path d="M{f1(x - 22 * s)},{f1(y + 10 * s * k)} Q{f1(x - 10 * s)},{f1(y - 4 * s)} {f1(x)},{f1(y + 4 * s)} '
            f'Q{f1(x + 10 * s)},{f1(y - 4 * s)} {f1(x + 22 * s)},{f1(y + 10 * s * k)}" fill="none" stroke="{P["ink_soft"]}" '
            f'stroke-width="{4 * s}" stroke-linecap="round"/>')


def badge(cx, cy, n, r=40):
    """A round cream number badge (picture-book count)."""
    out = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff6dc" stroke="{S.mix(P["sun_hot"], INK, 0.4)}" stroke-width="5"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r - 9}" fill="none" stroke="#f2c14e" stroke-width="4"/>')
    return S.g(out, filter="wobble-fine") + S.text(cx, cy + r * 0.42, str(n), size=int(r * 1.3),
                                                    fill=S.mix(P["sun_hot"], INK, 0.55))


def ring(cx, cy, rx, ry):
    return (f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="none" stroke="#eef8f5" '
            f'stroke-width="5"/>')


def sling_far(D, stone=False):
    """The sling hanging from the FAR hand (characters.david draws it in the near hand in hold_sling)."""
    def f(st):
        W, R, hr = st["arms"][0][2], st["m"]["R"], st["m"]["hr"]
        L = 2.4 * R
        d = (0.119, 0.993)
        return C._sling_cords(W, (W[0] + d[0] * 0.8 * L, W[1] + d[1] * 0.8 * L), d, stone) + C._fist(W, hr, D["skin"])
    return f


def both(*hooks):
    hs = [h for h in hooks if h]
    return lambda st: "".join(h(st) for h in hs)


def stone_hand(D, seed):
    def f(st):
        W = st["arms"][1][2]
        return PR.stone(W[0] + 2, W[1] + 12, 1.0, seed=seed) + C._fist(W, st["m"]["hr"], D["skin"])
    return f


KP = dict(C.POSES["dv_kneel_pick"])


def kp(**kw):
    d = dict(KP)
    d.update(kw)
    return d


K_SWISH = kp(arms=(("ik", "knee", 0, 0.25, 1), ("ik", "abs", 116, -2, 1)))
K_SHOW = kp(t=10, h=-4, arms=(("ik", "knee", 0, 0.25, 1), ("fk", 60, 140)), look=(0.05, -0.02))
K_BAG = kp(t=12, h=4, arms=(("ik", "knee", 0, 0.25, 1), ("fk", -30, -10)), hands=("fist", "open"))
K_PAT = kp(t=6, h=-6, arms=(("ik", "knee", 0, 0.25, 1), ("ik", "body", -30, -40, 1)), hands=("fist", "open"))
D_ST = A.D_ST
HOLD_UP = _P(h=-6, legs=((8, 3), (-7, -3)), arms=(("fk", 92, 128), D_ST), hands=("fist", "fist"), look=(0.03, -0.02))
HOLD_DOWN = _P(h=-4, legs=((8, 3), (-7, -3)), arms=(("fk", 14, 8), D_ST), hands=("fist", "fist"))


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    from stories.david.scenes.s09_armor import split_chunk

    # ------------------------------------------------------------ beats
    t_walk = L[0].start + 0.05                         # "大卫拿起放羊的杖，来到小溪边。"
    t_bend = pt(ctx, 1, "他弯下腰")
    t_pick = pt(ctx, 1, "挑了五块")
    counts = split_chunk(ctx, 1, 1, 6)                 # 一块 两块 三块 四块 五块 都放进口袋里
    t_all = counts[5]
    counts = counts[:5]
    t_hold = pt(ctx, 2, "他手里还拿着")
    t_sling = pt(ctx, 2, "甩石头用的机弦")
    t_strap = pt(ctx, 2, "那是一根长长的带子")
    t_far = pt(ctx, 2, "能把石头甩得")
    t_spin0 = t_far + 0.05
    t_rel = t_spin0 + 1.25
    t_out = t_rel + 0.55

    # ------------------------------------------------------------ positions
    lx_hand, _ = brook_span(FY - 84)
    KX = lx_hand - 66                                  # where David kneels (hands at the water's edge)
    X0 = 330                                           # where he enters
    adv = walk_adv(D_A, K)
    D0 = C._david_design(False, True)
    hands_k = C.body_points(lambda x, y, s_, f_: C.david(x, y, s_, f_, pose="kneel_pick"), KX, FY, K, 1)["hands"]
    HX, HY = (hands_k[0][0] + hands_k[1][0]) / 2, (hands_k[0][1] + hands_k[1][1]) / 2
    show_fn = A.david_fig(K_SHOW, "happy", front=stone_hand(D0, 0))
    SHX, SHY = C.body_points(show_fn, KX, FY, K, 1)["hands"][1]

    # ------------------------------------------------------------ SKY, FAR, MEADOW, BROOK
    sc.add("sky", sky_svg(), wc=0.45)
    for i, v in enumerate((6, 4, 5, 3.5)):
        sc.add(f"cloud{i}", cloud_svg(i), wc=0.7, motion=M.combine(M.drift(vx=-v), M.bob(3, 7 + i, i * 0.3)))
    birds = [doc(bird(1900, 420, 1.1, up) + bird(1990, 450, 0.9, not up) + bird(2060, 400, 0.8, up)) for up in (True, False)]
    sc.add("birds", birds, wc=0, frame_at=lambda t: float(int(t * 4) % 2), motion=M.drift(vx=-22))
    sc.add("far", far_svg(), wc=0.7)
    sc.add("meadow", meadow_svg(), wc=0.8)
    sc.add("brook", brook_svg(), wc=0.6)
    rip = [ripples_svg(k) for k in range(RIP_N)] + [ripples_svg(0)]
    sc.add("ripples", rip, wc=0, frame_at=lambda t: (t / 1.8 * RIP_N) % RIP_N)
    sc.add("bank", bank_svg(), wc=0.6)
    reed_fr = [plants_svg(sw) for sw in (-0.4, 0.0, 0.4)]
    sc.add("plants", reed_fr, wc=0.7, frame_at=lambda t: 1 + math.sin(2 * math.pi * t / 3.4))

    # ripple rings where his hands swish in the shallows
    for j in range(4):
        t0 = t_pick + 0.1 + 0.55 * j
        sc.add(f"ring{j}", doc(ring(HX + 30, HY + 14, 34, 11)), wc=0,
               motion=lambda t, t0=t0: Tf(sx=0.4 + 1.6 * M.progress(t, t0, t0 + 0.9, "out"),
                                          sy=0.4 + 1.6 * M.progress(t, t0, t0 + 0.9, "out"),
                                          alpha=(1.0 if t >= t0 else 0.0) * (1 - M.progress(t, t0 + 0.2, t0 + 0.9, "sine")),
                                          px=HX + 30, py=HY + 14))

    # the staff laid on the bank while he kneels
    staff_k = lambda t: t_bend <= t < t_hold
    sc.add("staff_down", doc(PR.staff(KX - 150, FY + 22, 1.1 * K, 1, rot=-84)), wc=0.6,
           motion=lambda t: Tf(alpha=1.0 if staff_k(t) else 0.0))

    # ------------------------------------------------------------ DAVID
    spD = sprite(560, 560, 280, 500, seed=90)
    walk_mk = lambda ps: A.david_fig(ps, "happy", front=C._staff_near(D0))
    w_in = walk_drawings(spD, walk_mk, K, 1, D_A, lk=D_LK, arm=(None, (D_ST, "fist")))
    walk_mk2 = lambda ps: A.david_fig(ps, "brave", front=both(sling_far(D0), C._staff_near(D0)))
    w_out = walk_drawings(spD, walk_mk2, K, 1, D_A, lk=D_LK, arm=(None, (D_ST, "fist")))
    stand_staff = spD.add(walk_mk(_P(arms=(("fk", 14, 8), D_ST)))(spD.ax, spD.ay, K, 1))
    kneel = spD.add(C.david(spD.ax, spD.ay, K, 1, pose="kneel_pick"))
    swish = spD.add(A.david_fig(K_SWISH, "happy")(spD.ax, spD.ay, K, 1))
    shows = [spD.add(A.david_fig(K_SHOW, "happy", front=stone_hand(D0, i))(spD.ax, spD.ay, K, 1)) for i in range(5)]
    bag = spD.add(A.david_fig(K_BAG, "happy")(spD.ax, spD.ay, K, 1))
    pat = spD.add(A.david_fig(K_PAT, "laugh")(spD.ax, spD.ay, K, 1))
    hold_up = spD.add(A.david_fig(HOLD_UP, "brave", front=both(sling_far(D0), C._staff_near(D0)))(spD.ax, spD.ay, K, 1))
    hold_dn = spD.add(A.david_fig(HOLD_DOWN, "happy", front=both(sling_far(D0), C._staff_near(D0)))(spD.ax, spD.ay, K, 1))
    spins = []
    for ph in [i / 8 for i in range(8)]:
        D = C._david_design(False, True)
        behind, front = C._sling_spin_hooks(D, ph, False)
        D["behind"], D["mid"], D["front"] = behind, C._bag_mid, both(front, C._staff_near(D))
        ps = dict(C.POSES["dv_sling_spin"])
        ps["arms"] = (ps["arms"][0], D_ST)
        ps["hands"] = ("fist", "fist")
        spins.append(spD.add(fig_(D, C._BOY, ps, "brave", spD.ax, spD.ay, K, 1)))
    D = C._david_design(False, True)
    D["mid"], D["front"] = C._bag_mid, both(C._sling_front(D, "release"), C._staff_near(D))
    ps = dict(C.POSES["dv_sling_release"])
    ps["arms"] = (ps["arms"][0], D_ST)
    release = spD.add(fig_(D, C._BOY, ps, "brave", spD.ax, spD.ay, K, 1))

    t_arr_in = None
    n_in = int(round((KX - 60 - X0) / adv))
    rate_in = n_in / max(0.5, (t_bend - 0.35) - t_walk)
    rate_in = min(rate_in, 34.0)
    path_in = WalkPath([(t_walk, X0, KX - 60, rate_in)], w_in, adv)
    t_arr_in = path_in.end(0)
    lx_s, rx_s = brook_span(FY + 6)
    x_exit = SW + 120
    path_out = WalkPath([(t_out, KX, x_exit, 34.0)], w_out, adv)

    def d_pos(t):
        if t < t_bend - 0.05:
            return path_in.x(t), FY
        if t < t_out:
            return KX, FY
        x = path_out.x(t)
        # little hops over the stepping stones
        dy = 0.0
        if lx_s - 30 < x < rx_s + 30:
            ph = (x - (lx_s - 30)) / ((rx_s - lx_s + 60) / 3.0)
            dy = -26 * abs(math.sin(math.pi * ph))
        return x, FY + dy

    def walk_fr(t):
        if t < t_bend - 0.05:
            return path_in.frame(t)
        return path_out.frame(t)

    sched = [(0, stand_staff, 0), (t_arr_in, stand_staff, 0.4), (t_bend, kneel, 1.1), (t_pick, swish, 0.4)]
    for j in range(4):
        sched.append((t_pick + 0.55 * j + 0.27, kneel if j % 2 else swish, 0.25))
    for i, tc in enumerate(counts):
        sched += [(tc - 0.12, kneel, 0.4), (tc + 0.06, shows[i], 0.8), (tc + 0.5, bag, 0.6)]
    sched += [(t_all, pat, 0.8), (t_hold, hold_up, 1.2), (t_strap + 0.6, hold_dn, 0.4)]
    sched += [(t_spin0, spins[0], 0.8)]
    sched += [(t_rel, release, 1.0), (t_rel + 0.5, hold_dn, 0.5), (t_out - 0.02, w_out[0], 0.3)]

    def spin_fr(t):
        if t_spin0 + 0.05 <= t < t_rel:
            return spins[int((t - t_spin0) / 0.06) % 8]
        return walk_fr(t)

    sc.add("shD", doc(C.ground_shadow(0, FY, K, width=110, opacity=0.24)), wc=0,
           motion=lambda t: Tf(dx=d_pos(t)[0], alpha=1.0 if t < t_out + 0.1 or d_pos(t)[0] < lx_s - 40 or
                               d_pos(t)[0] > rx_s + 40 else 0.0))
    sc.add_dynamic("david", Actor(spD, sched, d_pos, walk=spin_fr, bper=2.6, phase=0.2))

    # stones in the bag: a little pop on the bag each time
    # ------------------------------------------------------------ count badges and the five-stone row
    for i, tc in enumerate(counts):
        bx, by = SHX + 10, SHY - 120
        sc.add(f"badge{i}", doc(badge(bx, by, i + 1, 42)), wc=0,
               motion=lambda t, tc=tc, bx=bx, by=by: pop_tf(t, tc + 0.06, tc + 0.62, bx, by, dur_in=0.25, dur_out=0.18,
                                                            bob=2.0))
    ROW_Y = 905
    row_x = [KX - 260 + 120 * i for i in range(5)]
    slots = "".join(f'<circle cx="{x}" cy="{ROW_Y}" r="44" fill="#fff6dc" fill-opacity="0.75" stroke="{P["ink_soft"]}" '
                    f'stroke-width="4" stroke-dasharray="10 8"/>' for x in row_x)
    row_a = lambda t: M.progress(t, counts[0] - 0.6, counts[0] - 0.1, "sine") * (1 - M.progress(t, t_hold - 0.2,
                                                                                                  t_hold + 0.4, "sine"))
    sc.add("slots", doc(S.g(slots, filter="wobble-fine")), wc=0, motion=lambda t: Tf(alpha=row_a(t)))
    for i, (x, tc) in enumerate(zip(row_x, counts)):
        t_in = tc + 0.5
        mk = doc(PR.stone(x, ROW_Y + 18, 2.1, seed=i) + S.text(x, ROW_Y + 96, str(i + 1), size=46,
                                                               fill=S.mix(P["sun_hot"], INK, 0.55)))

        def st_m(t, t_in=t_in, x=x, i=i):
            if t < t_in:
                return Tf(alpha=0.0)
            k = M.ease("back")(clamp((t - t_in) / 0.3))
            bounce = -14 * abs(math.sin(math.pi * clamp((t - t_all - 0.08 * i) / 0.35)))
            return Tf(sx=max(0.01, k), sy=max(0.01, k), dy=bounce, alpha=row_a(t), px=x, py=ROW_Y + 18)
        sc.add(f"rowstone{i}", mk, wc=0.4, motion=st_m)

    # ------------------------------------------------------------ the sling inset (picture-book magnifier)
    IX, IY, IR = KX + 400, 930, 170
    hold_h = C.body_points(A.david_fig(HOLD_UP, "brave", front=both(sling_far(D0), C._staff_near(D0))), KX, FY, K,
                           1)["hands"][0]
    t_ins_in, t_ins_out = t_sling - 0.1, t_far - 0.15
    defs = S.rad_grad("s10ins", [(0, "#fffaf0"), (1, "#f4e6c4")])
    ins_bg = (f'<circle cx="{IX}" cy="{IY}" r="{IR}" fill="url(#s10ins)" stroke="{INK}" stroke-width="7"/>'
              f'<circle cx="{IX}" cy="{IY}" r="{IR - 12}" fill="none" stroke="#e8c062" stroke-width="5"/>')
    tail = "".join(f'<circle cx="{f1(M.lerp(IX - IR * 0.7, hold_h[0], k))}" cy="{f1(M.lerp(IY + IR * 0.7, hold_h[1] - 20, k))}" '
                   f'r="{r}" fill="#fffaf0" stroke="{INK}" stroke-width="3.5"/>' for k, r in ((0.35, 14), (0.6, 10), (0.82, 7)))
    sc.add("inset_bg", doc(S.g(tail + ins_bg, filter="wobble-fine"), defs), wc=0.3,
           motion=lambda t: pop_tf(t, t_ins_in, t_ins_out, IX, IY, bob=3.0))
    swings = []
    for a in (-22, -11, 0, 11, 22):
        g = PR.sling(IX, IY - IR + 46, 2.6, 1, angle=a, length=96, stone=False)
        g += (f'<circle cx="{IX}" cy="{IY - IR + 46}" r="18" fill="{C.DAVID_SKIN}" stroke="{INK}" stroke-width="4"/>')
        swings.append(doc(g))
    sc.add("inset_sling", swings, wc=0.4,
           frame_at=lambda t: 2 + 2 * math.sin(2 * math.pi * max(0.0, t - t_strap) / 1.6) if t > t_strap else 2.0,
           motion=lambda t: pop_tf(t, t_ins_in + 0.08, t_ins_out, IX, IY, bob=3.0))
    arrow = (f'<path d="M{IX + 70},{IY - IR + 60} L{IX + 70},{IY + IR - 70}" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" '
             f'stroke-width="7" stroke-linecap="round" stroke-dasharray="4 14"/>'
             f'<path d="M{IX + 54},{IY - IR + 78} L{IX + 70},{IY - IR + 56} L{IX + 86},{IY - IR + 78}" fill="none" '
             f'stroke="{S.mix(P["sun_hot"], INK, 0.3)}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M{IX + 54},{IY + IR - 92} L{IX + 70},{IY + IR - 70} L{IX + 86},{IY + IR - 92}" fill="none" '
             f'stroke="{S.mix(P["sun_hot"], INK, 0.3)}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    sc.add("inset_arrow", doc(arrow), wc=0,
           motion=lambda t: Tf(alpha=pop_k(t, t_strap + 0.05, t_ins_out)[1], sy=max(0.01, M.progress(t, t_strap + 0.05,
                                                                                                     t_strap + 0.5, "out")),
                               px=IX + 70, py=IY))

    # ------------------------------------------------------------ the whoosh far across the valley
    rel_h = C.body_points(lambda x, y, s_, f_: fig_(D, C._BOY, ps, "brave", x, y, s_, f_), KX, FY, K, 1)["hands"][0]
    wx0, wy0 = rel_h
    wx1, wy1 = 2720, 650
    pts = [(M.lerp(wx0, wx1, u), M.lerp(wy0, wy1, u) - 260 * math.sin(math.pi * u) * (1 - 0.3 * u)) for u in
           [k / 20 for k in range(21)]]
    wd = S.smooth_path(pts, closed=False)
    wh = (f'<path d="{wd}" fill="none" stroke="#fffaf0" stroke-width="16" stroke-linecap="round" opacity="0.8"/>'
          f'<path d="{wd}" fill="none" stroke="{P["ink_soft"]}" stroke-width="6" stroke-linecap="round" '
          f'stroke-dasharray="26 18"/>')
    for k in range(3):
        u = 0.15 + 0.08 * k
        x, y = pts[int(u * 20)]
        wh += (f'<path d="M{f1(x - 40)},{f1(y + 22 + 10 * k)} q30,-10 60,-26" fill="none" stroke="{P["ink_soft"]}" '
               f'stroke-width="4" stroke-linecap="round" opacity="0.6"/>')
    sc.add("whoosh", doc(S.g(wh, filter="wobble-fine")), wc=0,
           reveal=lambda t: {"mode": "left", "frac": M.progress(t, t_rel + 0.02, t_rel + 0.5, "out"), "soft": 80},
           motion=lambda t: Tf(alpha=(1.0 if t >= t_rel else 0.0) * (1 - M.progress(t, t_rel + 1.2, t_rel + 1.9, "sine"))))
    sc.add("twinkle", doc(S.g(clank_star(wx1, wy1), filter="wobble-fine")), wc=0,
           motion=lambda t: pop_tf(t, t_rel + 0.45, t_rel + 1.2, wx1, wy1, dur_in=0.2, dur_out=0.3, bob=0))

    # ------------------------------------------------------------ dragonfly
    dfs = [doc(dragonfly(0, 0, 0.9, w)) for w in (0, 1)]

    def df_m(t):
        x = 2250 + 260 * math.sin(2 * math.pi * t / 9.0) + 40 * math.sin(2 * math.pi * t / 2.3)
        y = 1120 + 60 * math.sin(2 * math.pi * t / 5.3) + 18 * math.sin(2 * math.pi * t / 1.1)
        return Tf(dx=x, dy=y)
    sc.add("dragonfly", dfs, wc=0.2, frame_at=lambda t: float(int(t * 14) % 2), motion=df_m)

    sc.add("fg", fg_svg(), wc=0.7)

    # ------------------------------------------------------------ CAMERA
    c_wide = Cam(1560, 960, 2600)
    c_bank = Cam(KX + 40, 1095, 1500)
    c_close = Cam(KX + 60, 1135, 1250)
    c_sling = Cam(KX + 170, 1085, 1450)
    c_out = Cam(KX + 380, 1060, 1700)
    sc.camera = M.cam_keys([(0.0, c_wide), (t_walk + 0.3, c_wide), (t_arr_in + 0.4, c_bank), (t_pick, c_bank),
                            (counts[0] - 0.3, c_close), (t_all + 0.6, c_close), (t_sling - 0.2, c_sling),
                            (t_rel + 0.2, c_sling), (t_out + 1.2, c_out), (T, Cam(KX + 386, 1060, 1690))], "sine")

    # ------------------------------------------------------------ FX
    sc.fx = [
        FX.motes((200, 300, 2900, 1500), count=24, color=(255, 248, 220), size=(3, 6), alpha=80),
        FX.sparkles((KX + 40, HY - 30, KX + 240, HY + 40), count=10, t0=t_pick, t1=t_all + 0.5,
                    color=(255, 250, 220), size=(6, 12), period=1.1, drift=0, seed=4),
        FX.sparkles((2200, 1200, 2900, 1650), count=14, t0=0, t1=T + 1, color=(250, 252, 240), size=(6, 12),
                    period=1.7, drift=0, seed=6),
    ]

    # ------------------------------------------------------------ SOUND
    sc.sfx("waves_calm", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0, pan=0.3)
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_walk, dur=t_arr_in - t_walk, gain_db=-14, fade_in=0.1, fade_out=0.2)
    sc.sfx("cloth", t_bend, gain_db=-14)
    sc.sfx("splash_small", t_pick + 0.1, gain_db=-16, pan=0.2)
    sc.sfx("splash_small", t_pick + 1.2, gain_db=-18, pan=0.2)
    for i, tc in enumerate(counts):
        sc.sfx("splash_small", tc - 0.1, gain_db=-20, pan=0.2)
        sc.sfx("pop", tc + 0.08, gain_db=-12, pan=0.1)
        sc.sfx("coins", tc + 0.52, gain_db=-17, pan=-0.05)
    sc.sfx("sparkle", t_all + 0.05, gain_db=-15)
    sc.sfx("cloth", t_hold, gain_db=-14)
    sc.sfx("pop", t_ins_in, gain_db=-12, pan=0.3)
    sc.sfx("pop", t_ins_out, gain_db=-15, pan=0.3)
    for k in range(3):
        sc.sfx("whoosh", t_spin0 + 0.12 + 0.4 * k, gain_db=-17 + 2 * k)
    sc.sfx("whoosh", t_rel, gain_db=-9, pan=0.4)
    sc.sfx("sparkle", t_rel + 0.45, gain_db=-17, pan=0.6)
    sc.sfx("footsteps", t_out, dur=T - t_out, gain_db=-15, fade_in=0.1, fade_out=0.6, pan=0.4)
    sc.sfx("splash_small", t_out + 0.55, gain_db=-20, pan=0.5)
    return sc


def fig_(D, m, ps, expr, x=None, y=None, s=None, f=None):
    """characters figure from a design (anchored on the sprite canvas when x is None)."""
    from stories.daniel.scenes.s05_prays import fig
    if x is None:
        raise ValueError("fig_ needs coordinates")
    return fig(D, m, dict(ps), expr, x, y, s, f, "dv-x")


def clank_star(cx, cy, s=1.0):
    pts = []
    for i in range(10):
        r = (30 if i % 2 == 0 else 12) * s
        a = math.radians(-90 + 36 * i)
        pts.append(f"{f1(cx + r * math.cos(a))},{f1(cy + r * math.sin(a))}")
    return f'<path d="M{" L".join(pts)} Z" fill="#fff1b0" stroke="{S.mix(P["sun_hot"], INK, 0.4)}" stroke-width="3.5"/>'
