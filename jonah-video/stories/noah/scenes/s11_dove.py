"""Scene 11 — the water goes down; the dove (Genesis 8:1-12).

Two shots of the same morning, joined by a soft dissolve in the pause after line 0:

A  (wide)  the flood has stopped: a grey sky clearing, the snowy top of Mount Ararat above a wide calm sea and the
           little ark floating beside it. '后来，上帝叫风吹过大地，' — soft gold-white wind swirls sweep over the sea
           and the clouds roll away; '水慢慢地退下去了。' — the water drops in gentle steps (the smaller peak and far
           ridges appear); '方舟停在了亚拉拉特山上。' — the ark rides down with the water and settles on the mountain's
           saddle with a soft bump; the water keeps going down below it. The camera eases in toward the ark.
B  (close) the ark resting on the rocky ledge, the snowy mountain behind, the sea far below on the left with far
           hills on the horizon. Noah at the high window:
  line 1  '挪亚打开窗户，'      the shutters swing open, Noah pushes them (open_window);
          '放出一只鸽子。'      he lifts the dove and lets it go (release_dove);
          '鸽子飞啊飞，找不到落脚的地方，' it flies out over the water, circles, finds only sea;
          '又飞回来了。'        it comes back, tired (slow flaps), into his hands; he takes it in.
  line 2  '过了七天，'          a row of seven suns fills in (the day counter), the sea is a little lower;
          '挪亚又放出鸽子。'    he lets the dove go again; it flies far away;
          '到了晚上，鸽子飞回来了，' the sky turns to evening gold, the dove comes back from far away ...
          '嘴里叼着一片新鲜的橄榄叶！' ... with an olive leaf in its beak; it lands on the sill and Noah holds the
                                      twig up, amazed (hold_leaf), a sparkle on the leaf.
  line 3  '挪亚就知道，地上的水退了！' he laughs for joy; little green shoots pop up on the rocks.
  line 4  '又过了七天，挪亚再放出鸽子。' seven more suns, morning again, the far hills are green; he lets the dove go;
          '这一次，鸽子再也没有回来。' it flies off toward the green hills far away and is gone; Noah waves and smiles.
  Calm last frame (page dip into s12).
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import lut_tint, phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s10_inside import stars_fx

INK = P["ink"]

# ---------------------------------------------------------------- shot A geometry (wide)
AR = (1000, 1330, 1.0)                        # Ararat anchor x, y, scale
KA = 0.25                                     # ark scale in the wide shot (ARARAT_LEDGE note)
LEDGE_Y = AR[1] + PR.ARARAT_LEDGE[1] * AR[2]  # 570
LVL_LAND = LEDGE_Y - PR.ARK_DRAFT * KA        # waterline when the keel touches the saddle
LVL0 = LVL_LAND - 122                         # start level (only the big peak shows)
LVL_END = 900
A_LAST = Cam(1006, 652, 1420)                 # shot A's framing when the dissolve starts
SEA_REF = 520                                 # level the sea layer is drawn at (moved by dy)

# ---------------------------------------------------------------- shot B geometry (close)
KB = 0.82
AX, AY = 1480, 1020
PTS = PR.ark_points(AX, AY, KB, 1)
WIN = PTS["window_box"]
NX, NY = PTS["window_stand"]
NF = -1                                       # Noah looks out to the left, over the sea
HZ = 560                                      # horizon (B)
SEA_B = [560, 590, 622]                       # sea level in B: first visit, after 7 days, after 14 days
SILL = (WIN[0] + 52, WIN[3] - 2)              # where the dove stands on the sill (feet)
DS = 0.72 * KB                                # dove scale (= the dove in Noah's hands)


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


# ============================================================================ shot A art


def a_sky_svg(clear):
    if clear:
        defs = S.lin_grad("s11sa", [(0, "#9fcde3"), (0.55, "#cfe6ea"), (1, "#f4ead2")])
    else:
        defs = S.lin_grad("s11sg", [(0, "#7d8aa0"), (0.6, "#a3aebb"), (1, "#c7cbc8")])
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#{"s11sa" if clear else "s11sg"})"/>'
    return doc(body, defs)


def a_clouds_svg(grey):
    fill, sh = ("#8e98a8", "#77839a") if grey else ("#fbf3e6", "#e6dccb")
    b = ""
    spots = ((260, 150, 520, 150), (980, 90, 640, 160), (1720, 170, 600, 150), (2040, 330, 380, 110),
             (520, 380, 380, 100))
    for i, (x, y, w, h) in enumerate(spots):
        b += S.cloud(x, y, w, h, fill=fill, seed=40 + i, puffs=6, sw=3, shade_fill=sh)
    return doc(S.g(b, filter="wobble"))


def a_land_svg():
    """Far ridges and Mount Ararat (static; the sea covers them and uncovers them)."""
    b = ""
    b += S.path(S.hill(-60, 760, 760, 70, seed=3, bottom=H + 60, bumps=3), fill="#a9b7b4", sw=3)
    b += S.path(S.hill(1450, 2180, 770, 80, seed=5, bottom=H + 60, bumps=3), fill="#aab8b2", sw=3)
    b += S.path(S.hill(200, 900, 810, 50, seed=8, bottom=H + 60, bumps=2), fill="#9fb0a6", sw=3)
    b = S.g(b, filter="wobble")
    b += PR.ararat(AR[0], AR[1], AR[2], snow=True, green=0.0, seed=1)
    return doc(b)


def a_wind_svg():
    b = ""
    rng = random.Random(4)
    for i in range(7):
        x = rng.uniform(-300, 1800)
        y = rng.uniform(300, 880)
        ln = rng.uniform(300, 520)
        b += (f'<path d="M{f1(x)},{f1(y)} q{f1(ln * 0.3)},-30 {f1(ln * 0.62)},-4 t{f1(ln * 0.3)},-8 '
              f'q40,-12 28,-42 q-16,-18 -34,4" fill="none" stroke="#fff6dc" stroke-width="7" stroke-linecap="round" '
              f'opacity="0.85"/>')
    return doc(b)


# ============================================================================ shot B art


def b_sky_svg(kind):
    if kind == "day":
        defs = S.lin_grad("s11bd", [(0, "#8fcbe0"), (0.6, "#c4e3ea"), (1, "#f2ecd6")])
    else:
        defs = S.lin_grad("s11be", [(0, "#8a7fb0"), (0.45, "#e7a38a"), (0.8, "#f6c98a"), (1, "#f8e0a8")])
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="{HZ + 120}" fill="url(#{"s11bd" if kind == "day" else "s11be"})"/>'
    return doc(body, defs)


def b_clouds_svg(seed0, warm=False):
    fill, sh = ("#fbe6cf", "#f0c6a6") if warm else ("#fbf3e6", "#e6dccb")
    b = ""
    for i, (x, y, w, h) in enumerate(((330, 210, 420, 110), (860, 120, 380, 95), (120, 470, 300, 80),
                                      (700, 400, 260, 70))):
        b += S.cloud(x, y, w, h, fill=fill, seed=seed0 + i, puffs=5, sw=3, shade_fill=sh)
    return doc(S.g(b, filter="wobble"))


def b_sun_svg(warm):
    x, y = 0, 0
    col, glow = ("#f6a43c", "#f8c070") if warm else ("#fbd46b", "#fff2c4")
    defs = S.rad_grad(f"s11sun{int(warm)}", [(0, glow, 0.9), (0.5, glow, 0.35), (1, glow, 0)])
    body = (f'<circle cx="{x}" cy="{y}" r="190" fill="url(#s11sun{int(warm)})"/>'
            f'<circle cx="{x}" cy="{y}" r="62" fill="{col}" {S.STROKE}/>')
    return S.svg_doc(f'<g transform="translate(420,250)">{body}</g>', defs)


def b_far_svg(green):
    """Far hills on the horizon (the sea covers their feet); green 0..1 (bare grey-brown .. fresh green)."""
    c1 = S.mix("#a7a99a", "#8fbf6a", green)
    c2 = S.mix("#9a9c8e", "#7aae58", green)
    c3 = S.mix("#b4b4a6", "#a2cc80", green)
    b = S.path(S.hill(-60, 420, HZ + 4, 64, seed=11, bottom=HZ + 120, bumps=2), fill=c3, sw=2.5)
    b += S.path(S.hill(240, 760, HZ + 8, 46, seed=12, bottom=HZ + 120, bumps=2), fill=c1, sw=2.5)
    b += S.path(S.hill(-80, 220, HZ + 22, 34, seed=13, bottom=HZ + 120, bumps=1), fill=c2, sw=2.5)
    if green > 0.3:
        rng = random.Random(7)
        for _ in range(int(14 * green)):
            x = rng.uniform(40, 700)
            y = HZ - rng.uniform(0, 30)
            b += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="8" ry="6" fill="{S.shade(c2, -0.15)}"/>'
    return doc(S.g(b, filter="wobble"))


def b_mountain_svg():
    """The big snowy mountain rising behind the ark (right), hazy."""
    rock, shadow, snow = "#b3a59a", "#9a8c84", "#f6f1e6"
    d = (f"M600,{H + 40} L940,640 Q1080,470 1250,330 L1560,120 Q1640,60 1720,40 L1860,90 Q1960,150 2040,170 "
         f"L{W + 60},230 L{W + 60},{H + 40} Z")
    b = S.path(d, fill=rock, sw=4)
    b += S.path(f"M1720,40 L1760,300 Q1840,520 1900,{H + 40} L{W + 60},{H + 40} L{W + 60},230 L2040,170 "
                f"Q1960,150 1860,90 Z", fill=shadow, stroke=False, extra='opacity="0.6"')
    b += S.path("M1250,330 L1560,120 Q1640,60 1720,40 L1860,90 Q1960,150 2040,170 L2130,226 L2060,262 L1990,236 "
                "L1920,290 L1850,250 L1770,320 L1690,262 L1600,330 L1520,280 L1430,360 L1350,322 Z", fill=snow, sw=4)
    for x0, y0, x1, y1 in ((1030, 560, 1120, 700), (1300, 420, 1380, 560), (1840, 360, 1900, 520)):
        b += f'<path d="M{x0},{y0} Q{(x0 + x1) / 2 + 20},{(y0 + y1) / 2} {x1},{y1}" fill="none" stroke="#8a7c74" stroke-width="3"/>'
    return doc(S.g(b, filter="wobble"))


def slope_y(x):
    """Top edge of the mountain's flank that runs down to the left into the sea (B)."""
    return 606 + (x + 60) / 900 * 400


def b_slope_svg(green):
    """Mid-ground: the mountain's flank running down-left from the ledge toward the sea; green 0..1."""
    rock = S.mix("#a4927f", "#8fb466", green * 0.85)
    rock2 = S.mix("#b8a690", "#a6c77c", green * 0.85)
    pts = [(-60, slope_y(-60)), (120, slope_y(120) - 8), (330, slope_y(330) + 6), (560, slope_y(560) - 6),
           (840, slope_y(840))]
    d = S.smooth_path(pts, closed=False) + f" L900,{H + 60} L-60,{H + 60} Z"
    b = S.path(d, fill=rock, sw=4)
    rng = random.Random(3)
    for _ in range(18):
        x = rng.uniform(-40, 820)
        y = slope_y(x) + rng.uniform(40, 300)
        b += f'<path d="M{f1(x)},{f1(y)} q30,-10 60,-2" fill="none" stroke="{S.shade(rock, -0.2)}" stroke-width="3"/>'
    for x, r in ((60, 30), (300, 40), (520, 26), (700, 34)):
        y = slope_y(x) + 18
        b += S.path(S.blob(x, y, r, r * 0.65, 0.12, 8, seed=x), fill=rock2, sw=3.5)
    if green > 0.3:
        for _ in range(10):
            x = rng.uniform(-20, 800)
            y = slope_y(x) + rng.uniform(30, 260)
            b += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="26" ry="15" fill="#6ea84b" {S.STROKE_THIN}/>'
                  f'<ellipse cx="{f1(x - 6)}" cy="{f1(y - 5)}" rx="10" ry="5" fill="#9ccc6a"/>')
    return doc(S.g(b, filter="wobble"))


def b_ledge_svg():
    """The rocky saddle under the ark (in front of the hull's keel)."""
    rock, rock2, dark = "#a89484", "#bfae9c", "#8a7666"
    top = [(560, 1100), (700, 1004), (900, 1010), (1150, 1016), (1400, 1022), (1650, 1016), (1900, 1024),
           (2180, 1012)]
    d = S.smooth_path(top, closed=False) + f" L{W + 60},{H + 60} L520,{H + 60} Z"
    b = S.path(d, fill=rock, sw=4)
    band = S.smooth_path([(x, y + 6) for x, y in top[1:]], closed=False)
    b += f'<path d="{band}" fill="none" stroke="{rock2}" stroke-width="14" stroke-linecap="round"/>'
    rng = random.Random(9)
    for _ in range(16):
        x = rng.uniform(600, W)
        y = rng.uniform(1050, 1100)
        b += f'<path d="M{f1(x)},{f1(y)} l{f1(rng.uniform(-30, 30))},{f1(rng.uniform(-30, -12))}" stroke="{dark}" stroke-width="3"/>'
    for x, y, r in ((690, 1004, 36), (780, 1000, 24), (1980, 1018, 52), (2070, 1008, 34)):
        b += S.path(S.blob(x, y, r, r * 0.7, 0.12, 8, seed=int(x)), fill=rock2, sw=4)
        b += f'<ellipse cx="{x - r * 0.3}" cy="{y - r * 0.3}" rx="{r * 0.35}" ry="{r * 0.18}" fill="#d8cbbb" opacity="0.7"/>'
    b += (f'<ellipse cx="1000" cy="1030" rx="70" ry="12" fill="#b9e0e3" {S.STROKE_THIN}/>'
          f'<path d="M965,1028 l35,0 M1010,1033 l26,0" stroke="#fffaf0" stroke-width="3" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"))


def sprouts_svg(seed=3):
    """Little green shoots and flowers on the rocks (pop in on '地上的水退了')."""
    rng = random.Random(seed)
    b = ""
    spots = [(40, 700), (210, 800), (380, 840), (500, 890), (640, 950), (760, 1006), (880, 1014), (1080, 1022),
             (1330, 1026), (1560, 1022), (1780, 1024), (1940, 1030)]
    for x, y in spots:
        for k in range(rng.randint(3, 5)):
            a = rng.uniform(-0.5, 0.5)
            ln = rng.uniform(18, 34)
            b += (f'<path d="M{x + k * 6 - 12},{y} q{f1(6 * a)},{f1(-ln * 0.6)} {f1(ln * a)},{f1(-ln)}" fill="none" '
                  f'stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
                  f'<path d="M{x + k * 6 - 12},{y} q{f1(6 * a)},{f1(-ln * 0.6)} {f1(ln * a)},{f1(-ln)}" fill="none" '
                  f'stroke="#7fb34e" stroke-width="4" stroke-linecap="round"/>')
        if rng.random() < 0.6:
            col = rng.choice(["#f2c14e", "#f0998a", "#fffaf0", "#c9a0dc"])
            b += (f'<circle cx="{x + 10}" cy="{y - 30}" r="7" fill="{col}" {S.STROKE_THIN}/>'
                  f'<circle cx="{x + 10}" cy="{y - 30}" r="2.5" fill="#e8a33c"/>')
    return b, spots


# ============================================================================ motion helpers


def spline(keys):
    """keys [(t, x, y, s, facing)] -> f(t) -> (x, y, s, facing): Catmull-Rom through the points (time-param)."""
    keys = sorted(keys, key=lambda k: k[0])

    def f(t):
        if t <= keys[0][0]:
            return keys[0][1:]
        if t >= keys[-1][0]:
            return keys[-1][1:]
        for i in range(len(keys) - 1):
            if keys[i][0] <= t <= keys[i + 1][0]:
                break
        k0 = keys[max(0, i - 1)]
        k1, k2 = keys[i], keys[i + 1]
        k3 = keys[min(len(keys) - 1, i + 2)]
        u = (t - k1[0]) / (k2[0] - k1[0])
        out = []
        for j in (1, 2, 3):
            p0, p1, p2, p3 = k0[j], k1[j], k2[j], k3[j]
            m1 = (p2 - p0) / 2
            m2 = (p3 - p1) / 2
            h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
            out.append(h00 * p1 + h10 * m1 + h01 * p2 + h11 * m2)
        return (*out, k1[4])
    return f


WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)
CYCLE = (0, 1, 2, 3, 4, 3, 2, 1)
DREF = (300, 300)          # where the flying dove is drawn on its layer


def add_dove_flight(sc, name, path, t0, t1, leaf=False, flap=0.075, tired=None, z=None, vis=None):
    """A flying dove along ``path`` between t0 and t1: two flipbooks (facing left / right) of the wing cycle."""
    frames = {f: [doc(PR.dove(DREF[0], DREF[1], DS * 1.4, f, wing=w, leaf=leaf)) for w in WINGS] for f in (-1, 1)}

    def wing_idx(t):
        per = flap if tired is None else flap * (1 + 0.7 * clamp((t - tired[0]) / max(0.01, tired[1] - tired[0])))
        return float(CYCLE[int((t - t0) / per) % len(CYCLE)])

    for f in (-1, 1):
        def mo(t, f=f):
            if t < t0 or t > t1:
                return Tf(alpha=0.0)
            x, y, s, fc = path(t)
            if fc != f:
                return Tf(alpha=0.0)
            a = 1.0 if vis is None else vis(t)
            # bank a little with the vertical speed
            x2, y2, _, _ = path(min(t1, t + 0.05))
            rot = clamp((y2 - y) * 0.6, -14, 14) * (-f)
            return Tf(dx=x - DREF[0], dy=y - DREF[1], sx=s / (DS * 1.4), sy=s / (DS * 1.4), rot=rot, px=DREF[0], py=DREF[1], alpha=a)
        sc.add(f"{name}_{'l' if f < 0 else 'r'}", frames[f], frame_at=wing_idx, motion=mo, wc=0.4, z=z)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]

    # ---------------------------------------------------------------- beats
    t_wind = L0.start + 0.1
    t_recede = L0.at("水慢慢地退下去了")
    t_rest = L0.at("方舟停在了")
    t_land = t_rest + 0.45
    t_xa, t_xb = L0.end + 0.02, L0.end + 0.6          # dissolve A -> B
    t_open = L1.at("挪亚打开窗户") + 0.12
    t_rel1 = snap(phrase_t(L1, "放出一只鸽子") - 0.05)
    t_fly1 = snap(t_rel1 + 0.55)
    t_back = L1.at("又飞回来了")
    t_home1 = snap(max(t_back + 0.9, L1.end - 0.1))
    t_in1 = snap(t_home1 + 0.75)
    t_days1 = L2.start + 0.05
    t_rel2 = snap(phrase_t(L2, "又放出鸽子") - 0.05)
    t_fly2 = snap(t_rel2 + 0.5)
    t_eve = L2.at("到了晚上")
    t_ret2 = phrase_t(L2, "鸽子飞回来了")
    t_leafc = L2.at("嘴里叼着")
    t_sill = snap(t_leafc + 0.15)
    t_take = snap(phrase_t(L2, "橄榄叶") - 0.1)
    t_know = snap(L3.start + 0.1)
    t_dry = phrase_t(L3, "地上的水退了")
    t_days2 = L4.start + 0.05
    t_stand2 = snap(t_days2 + 0.2)
    t_rel3 = snap(phrase_t(L4, "再放出鸽子") - 0.05)
    t_fly3 = snap(t_rel3 + 0.5)
    t_never = L4.at("这一次")
    t_wave = snap(t_never + 0.5)
    t_smile = snap(L4.end - 0.3)

    # ================================================================ SHOT A
    a_out = lambda t: Tf(alpha=1 - M.progress(t, t_xa, t_xb, "sine"))          # noqa: E731

    def level(t):
        """Water level (stage y): gentle steps down. Lands the ark at t_land."""
        steps = [(t_wind + 1.2, 18), (t_recede + 0.0, 26), (t_recede + 0.75, 26), (t_recede + 1.5, 26),
                 (t_land - 0.55, 26)]
        lv = LVL0
        for ts, d in steps:
            lv += d * M.progress(t, ts, ts + 0.55, "inout")
        lv = min(lv, LVL_LAND) if t <= t_land else LVL_LAND
        after = [(t_land + 0.2, 34), (t_land + 0.85, 34), (t_land + 1.5, 34), (t_land + 2.15, LVL_END - LVL_LAND - 102)]
        for ts, d in after:
            lv += d * M.progress(t, ts, ts + 0.55, "inout")
        return lv
    # make the steps before landing add up exactly to the landing level
    pre = 18 + 26 * 4
    assert abs(LVL0 + pre - LVL_LAND) < 1e-6 + 2.0, (LVL0 + pre, LVL_LAND)

    sc.add("a_sky_grey", a_sky_svg(False), motion=a_out, wc=0.6)
    sc.add("a_sky_clear", a_sky_svg(True), wc=0.6, motion=lambda t: Tf(
        alpha=M.progress(t, t_wind - 0.2, t_recede + 1.5, "sine") * (1 - M.progress(t, t_xa, t_xb, "sine"))))
    sc.add("a_clouds_grey", a_clouds_svg(True), motion=lambda t: Tf(
        dx=40 * t + 900 * M.progress(t, t_wind, t_recede + 2.2, "in"), dy=-60 * M.progress(t, t_wind, t_recede + 2.2),
        alpha=(1 - M.progress(t, t_wind + 0.4, t_recede + 1.8, "sine"))))
    sc.add("a_clouds_white", a_clouds_svg(False), motion=lambda t: Tf(
        dx=-260 + 30 * t, alpha=M.progress(t, t_recede - 0.5, t_rest, "sine") * (1 - M.progress(t, t_xa, t_xb, "sine"))))
    sc.add("a_land", a_land_svg(), motion=a_out, seed=7)

    ark_a = doc(PR.ark(AR[0], SEA_REF, KA, 1, floating=True, wet=True, ramp=False))

    def ark_a_m(t):
        lv = level(t)
        if t < t_land:
            bob = 3.0 * math.sin(2 * math.pi * t / 2.6)
            rot = 1.0 * math.sin(2 * math.pi * t / 3.1 + 0.6)
        else:
            u = t - t_land
            bob = 4.0 * math.exp(-u / 0.12) * math.sin(u * 30) if u < 0.6 else 0.0
            rot = (1.0 * math.sin(2 * math.pi * t_land / 3.1 + 0.6)) * math.exp(-u / 0.25) + \
                (-1.2 * math.sin(u * 14) * math.exp(-u / 0.3) if u < 1.2 else 0.0)
        a = a_out(t).alpha
        return Tf(dy=lv - SEA_REF + bob, rot=rot, px=AR[0], py=SEA_REF + 30, alpha=a)
    sc.add("a_ark", ark_a, motion=ark_a_m, seed=11)

    sea_frames = [doc(PR.flood_sea(-60, W + 60, SEA_REF, phase=k / 4, bottom=H + 40, storm=0.15, seed=2))
                  for k in range(4)]
    sea_frames.append(sea_frames[0])
    sc.add("a_sea", sea_frames, frame_at=lambda t: (t / 0.7) % 4,
           motion=lambda t: Tf(dy=level(t) - SEA_REF, alpha=a_out(t).alpha), seed=13)
    # a soft splash ring where the keel touches
    lx, ly = AR[0], LEDGE_Y
    spl = ""
    for sx_ in (-1, 1):
        spl += (f'<path d="M{lx + sx_ * 70},{ly - 6} q{sx_ * 30},-40 {sx_ * 70},-20" fill="none" stroke="#fffaf0" '
                f'stroke-width="6" stroke-linecap="round"/>'
                f'<circle cx="{lx + sx_ * 150}" cy="{ly - 30}" r="7" fill="#fffaf0" {S.STROKE_THIN}/>'
                f'<circle cx="{lx + sx_ * 120}" cy="{ly - 52}" r="5" fill="#fffaf0" {S.STROKE_THIN}/>')
    sc.add("a_splash", doc(spl), wc=0, motion=M.keys(
        [(t_land - 0.02, {"alpha": 0, "s": 0.5}), (t_land + 0.1, {"alpha": 1, "s": 1.0}),
         (t_land + 0.7, {"alpha": 0, "s": 1.3, "dy": -10})], ["out", "sine"], pivot=(lx, ly)))
    # God's wind: soft gold-white swirls sweeping over the sea from the left (two passes)
    wind = a_wind_svg()
    for i, tw in enumerate((t_wind, t_wind + 1.4)):
        sc.add(f"a_wind{i}", wind, wc=0, motion=M.keys(
            [(tw, {"dx": -1500, "dy": 40 * i, "alpha": 0}), (tw + 0.4, {"alpha": 0.9}), (tw + 2.0, {"alpha": 0.8}),
             (tw + 2.6, {"dx": 1500, "alpha": 0})], "linear"))

    # ================================================================ SHOT B
    b_in = lambda t: Tf(alpha=M.progress(t, t_xa, t_xb, "sine"))               # noqa: E731
    eve = lambda t: M.progress(t, t_eve - 0.2, t_eve + 1.4, "sine") * (1 - M.progress(t, t_days2, t_days2 + 1.4, "sine"))  # noqa: E731
    grn = lambda t: 0.5 * M.progress(t, t_days1 + 0.2, t_days1 + 1.6) + 0.5 * M.progress(t, t_days2 + 0.2, t_days2 + 1.8)  # noqa: E731

    def sea_b(t):
        return (SEA_B[0] + (SEA_B[1] - SEA_B[0]) * M.progress(t, t_days1 + 0.2, t_days1 + 1.6) +
                (SEA_B[2] - SEA_B[1]) * M.progress(t, t_days2 + 0.2, t_days2 + 1.8))

    sc.add("b_sky_day", b_sky_svg("day"), motion=b_in, wc=0.6)
    sc.add("b_sky_eve", b_sky_svg("eve"), wc=0.6, motion=lambda t: Tf(alpha=eve(t) * b_in(t).alpha))

    # the sun: high morning sun; it sinks warm in the evening; next morning it is back up
    def sun_m(warm):
        def m(t):
            e = eve(t)
            if warm:
                y = 420 * M.progress(t, t_eve - 0.2, t_eve + 2.5, "sine")
                return Tf(dx=60 * M.progress(t, t_eve - 0.2, t_eve + 2.5), dy=y, alpha=e * b_in(t).alpha)
            return Tf(dx=8 * math.sin(t / 3), dy=0, alpha=(1 - e) * b_in(t).alpha)
        return m
    sc.add("b_sun", b_sun_svg(False), wc=0.3, motion=sun_m(False))
    sc.add("b_sun_eve", b_sun_svg(True), wc=0.3, motion=sun_m(True))
    sc.add("b_clouds", b_clouds_svg(60), motion=lambda t: Tf(dx=-80 + 14 * t, alpha=(1 - 0.6 * eve(t)) * b_in(t).alpha))
    sc.add("b_clouds_eve", b_clouds_svg(60, True), motion=lambda t: Tf(dx=-80 + 14 * t, alpha=0.8 * eve(t) * b_in(t).alpha))
    sc.add("b_mountain", b_mountain_svg(), motion=b_in, seed=17)
    sc.add("b_far0", b_far_svg(0.0), motion=b_in, seed=19)
    sc.add("b_far1", b_far_svg(1.0), motion=lambda t: Tf(alpha=grn(t) * b_in(t).alpha), seed=19)
    sea_bf = [doc(PR.flood_sea(-60, W + 60, SEA_B[0], phase=k / 4, bottom=H + 40, seed=5, scale=0.45))
              for k in range(4)]
    sea_bf.append(sea_bf[0])
    sc.add("b_sea", sea_bf, frame_at=lambda t: (t / 0.8) % 4,
           motion=lambda t: Tf(dy=sea_b(t) - SEA_B[0], alpha=b_in(t).alpha), seed=23)
    sc.add("b_slope0", b_slope_svg(0.0), motion=b_in, seed=25)
    sc.add("b_slope1", b_slope_svg(1.0), motion=lambda t: Tf(alpha=grn(t) * b_in(t).alpha), seed=25)

    # the ark: shutters open on '挪亚打开窗户'
    wv = (0.0, 0.25, 0.5, 0.75, 1.0)
    ark_b = [doc(PR.ark(AX, AY, KB, 1, window=w, ramp=False, wet=False)) for w in wv]
    sc.add("b_ark", ark_b, frame_at=lambda t: float(clamp((t - t_open) / 0.12, 0, 4) // 1), motion=b_in, seed=29)

    # Noah at the window (clipped to the opening)
    def nf(**kw):
        return doc(PR.in_ark_window(C.noah(NX, NY, KB, NF, **kw), AX, AY, KB, 1))
    nfr = {
        "open": nf(pose="open_window"),
        "dove": nf(pose="release_dove", dove=True),
        "free": nf(pose="release_dove"),
        "stand": nf(pose="stand", expr="happy"),
        "look": nf(pose="stand", expr="amazed"),
        "leaf": nf(pose="hold_leaf"),
        "leaf_joy": nf(pose="hold_leaf", expr="laugh"),
        "smile": nf(pose="stand", expr="kind"),
    }
    waves = [nf(pose="wave", phase=p) for p in (0.0, 0.25, 0.5, 0.75)]
    names = list(nfr)
    frames = [nfr[k] for k in names] + waves
    idx = {k: i for i, k in enumerate(names)}
    W0 = len(names)
    t_show = t_open + 0.25                       # shutters half open: Noah appears
    sched = [(t_show, idx["open"]), (t_rel1, idx["dove"]), (t_fly1, idx["free"]), (t_home1, idx["dove"]),
             (t_in1, idx["stand"]), (t_rel2, idx["dove"]), (t_fly2, idx["free"]), (t_sill, idx["look"]),
             (t_take, idx["leaf"]), (t_know, idx["leaf_joy"]), (t_stand2, idx["stand"]), (t_rel3, idx["dove"]),
             (t_fly3, idx["free"]), (t_smile, idx["smile"])]
    base_fa = cuts([(0, idx["stand"])] + sched)

    def noah_fa(t):
        if t_wave <= t < t_smile:
            return float(W0 + int((t - t_wave) / 0.13) % 4)
        return base_fa(t)
    npiv = (NX, NY)
    dips = [dip(ts, KB, npiv, 6) for ts, _ in sched if ts != t_fly1 and ts != t_fly2 and ts != t_fly3]
    dips.append(dip(t_wave, KB, npiv, 4))
    sc.add("noah", frames, frame_at=noah_fa, z=None, motion=M.combine(
        lambda t: Tf(alpha=0.0 if t < t_show else 1.0), *dips,
        hop(t_know + 0.25, [(0, {"dy": 0}), (0.16, {"dy": -10 * KB}), (0.32, {"dy": 0}), (0.48, {"dy": -7 * KB}),
                            (0.64, {"dy": 0})], npiv),
        M.breathe(0.012, 2.8, pivot=npiv)))

    # ---------------------------------------------------------------- the dove
    hand_dove = (NX + NF * 100 * KB, NY - 312 * KB)            # where the dove=True drawing has the bird
    hx, hy = hand_dove
    # flight 1: out over the water, circling, finds nowhere to land, comes back tired into his hands
    d1 = t_back - t_fly1
    p1 = spline([(t_fly1, hx, hy, DS, -1), (t_fly1 + 0.6, hx - 170, hy - 100, DS * 1.05, -1),
                 (t_fly1 + 0.3 * d1, 700, 230, DS, -1), (t_fly1 + 0.55 * d1, 380, 330, DS * 0.9, -1),
                 (t_fly1 + 0.75 * d1, 230, 470, DS * 0.85, 1), (t_fly1 + 0.92 * d1, 420, 560, DS * 0.9, 1),
                 (t_back + 0.1, 640, 470, DS * 0.95, 1), (t_home1 - 0.6, 880, 400, DS, 1),
                 (t_home1, hx, hy, DS, 1)])
    add_dove_flight(sc, "dove1", p1, t_fly1, t_home1 - 0.001, flap=0.07, tired=(t_back - 0.4, t_home1))
    # flight 2: far away (out of sight), then back in the evening with the olive leaf, landing on the sill
    p2 = spline([(t_fly2, hx, hy, DS, -1), (t_fly2 + 0.5, hx - 200, hy - 100, DS, -1),
                 (t_fly2 + 1.2, 560, 200, DS * 0.75, -1), (t_eve + 0.2, 120, 260, DS * 0.45, -1)])
    add_dove_flight(sc, "dove2", p2, t_fly2, t_eve + 0.2, flap=0.07,
                    vis=lambda t: 1 - M.progress(t, t_eve - 0.3, t_eve + 0.2, "sine"))
    sx, sy = SILL
    p3 = spline([(t_ret2 - 0.2, 60, 300, DS * 0.45, 1), (t_ret2 + 0.6, 380, 340, DS * 0.7, 1),
                 (t_leafc - 0.5, 800, 360, DS * 0.95, 1), (t_sill, sx, sy - 38 * DS, DS, 1)])
    add_dove_flight(sc, "dove3", p3, t_ret2 - 0.2, t_sill - 0.001, leaf=True, flap=0.075,
                    vis=lambda t: M.progress(t, t_ret2 - 0.2, t_ret2 + 0.3, "sine"))
    # on the sill: with the leaf, then without (Noah has it), until he picks the dove up again
    sill = [doc(PR.dove(sx, sy - 38 * DS, DS, 1, pose="stand", leaf=True)),
            doc(PR.dove(sx, sy - 38 * DS, DS, 1, pose="stand", leaf=False))]
    sc.add("dove_sill", sill, frame_at=cuts([(0, 0), (t_take, 1)]), wc=0.4, motion=M.combine(
        lambda t: Tf(alpha=1.0 if t_sill <= t < t_rel3 else 0.0),
        dip(t_sill + 0.02, DS, (sx, sy), 7),
        lambda t: Tf(rot=5 * math.sin(2 * math.pi * t / 1.7) if math.sin(2 * math.pi * t / 5.1) > 0.6 else 0.0,
                     px=sx, py=sy)))
    # flight 3: away toward the far green hills, and gone
    p4 = spline([(t_fly3, hx, hy, DS, -1), (t_fly3 + 0.5, hx - 200, hy - 120, DS, -1),
                 (t_fly3 + 1.4, 640, 240, DS * 0.8, -1), (t_fly3 + 2.4, 330, 420, DS * 0.55, -1),
                 (t_fly3 + 3.3, 150, 540, DS * 0.35, -1)])
    add_dove_flight(sc, "dove4", p4, t_fly3, t_fly3 + 3.3, flap=0.07,
                    vis=lambda t: 1 - M.progress(t, t_fly3 + 2.6, t_fly3 + 3.3, "sine"))

    # ---------------------------------------------------------------- the rocky ledge (in front of the hull) + sprouts
    sc.add("b_ledge", b_ledge_svg(), motion=b_in, seed=31)
    spr, spots = sprouts_svg()
    sc.add("b_sprouts", doc(S.g(spr, filter="wobble-fine")), wc=0.5, motion=M.combine(
        M.keys([(t_dry - 0.05, {"sy": 0.0, "alpha": 0}), (t_dry + 0.1, {"alpha": 1}), (t_dry + 0.55, {"sy": 1.0})],
               ["sine", "back"], pivot=(W / 2, 1030)),
        lambda t: Tf(sx=1 + 0.01 * math.sin(2 * math.pi * t / 2.2), px=W / 2, py=1030)))

    # ---------------------------------------------------------------- day counters ('过了七天' x 2)
    cx_, cy_, cs_ = 470, 170, 0.85
    cnt = [doc(PR.day_counter(cx_, cy_, cs_, n=7, filled=k, icons="sun")) for k in range(8)]
    for i, td in enumerate((t_days1, t_days2)):
        fill_t = [snap(td + 0.35 + 0.2 * k) for k in range(7)]
        t_off = (t_rel2 if i == 0 else t_rel3) + 0.4
        sc.add(f"counter{i}", cnt, wc=0.2, frame_at=lambda t, ft=fill_t: float(sum(1 for x in ft if t >= x)),
               motion=M.combine(
                   M.keys([(td - 0.05, {"alpha": 0, "dy": 20}), (td + 0.3, {"alpha": 1, "dy": 0}),
                           (t_off, {"alpha": 1}), (t_off + 0.5, {"alpha": 0, "dy": -16})], "sine"),
                   *[hop(ft, [(0, {"s": 1.0}), (0.08, {"s": 1.035}), (0.2, {"s": 1.0})], (cx_, cy_)) for ft in fill_t]))

    # ---------------------------------------------------------------- light / fx
    leaf_pt = C.body_points(C.noah, NX, NY, KB, NF, pose="hold_leaf")["hands"][0]
    cues = [(leaf_pt[0] + dx, leaf_pt[1] + dy, t_take + dt, s) for dx, dy, dt, s in
            ((-10, -30, 0.05, 20), (24, -8, 0.3, 14), (-30, 10, 0.55, 12), (10, -50, 0.9, 16))]
    cues += [(x, y - 40, t_dry + 0.1 + 0.07 * k, 11) for k, (x, y) in enumerate(spots[::2])]
    sc.fx = [lut_tint((255, 196, 150), lambda t: 0.22 * eve(t), mode="multiply"),
             stars_fx(cues),
             FX.sparkles((200, 300, 1400, 800), count=14, t0=t_wind, t1=t_recede + 1.0, size=(6, 12), drift=-10,
                         seed=21, color=(255, 240, 190))]

    # ---------------------------------------------------------------- camera
    a0 = Cam(1000, 540, 1800)
    a1 = Cam(1010, 640, 1500)
    b0 = Cam(940, 560, 1640)
    b_close = Cam(1060, 520, 1400)
    b_wide = Cam(900, 560, 1720)
    keys = [(0, a0), (t_wind, a0), (t_land + 0.6, a1), (t_xa, A_LAST),
            (t_xa + 0.01, b0), (t_rel2, b0), (t_leafc - 0.3, Cam(1000, 540, 1520)), (t_take + 0.6, b_close),
            (L3.end, b_close), (t_rel3 - 0.2, b_wide), (T, Cam(905, 560, 1700))]
    camf = M.cam_keys(keys, "sine")

    def cam(t):
        # the dissolve hides the change of shot: shot A's camera keeps pushing in while B appears, then B is still
        if t_xa <= t < t_xb:
            return b0
        return camf(t)
    # during the dissolve both shots are drawn through one camera: keep A's push and B's framing compatible by
    # holding B's camera and scaling A's layers instead (A layers zoom a little more as they fade)
    sc.camera = cam
    zoom_a = lambda t: 1 + 0.08 * M.progress(t, t_xa, t_xb, "sine")              # noqa: E731
    for lay in sc.layers:
        if lay.name.startswith("a_"):
            m0 = lay.motion
            pa = (A_LAST.x, A_LAST.y)
            # map A's last framing onto B's camera b0 during the dissolve
            s_ab = b0.w / A_LAST.w

            def mm(t, m0=m0, pa=pa, s_ab=s_ab):
                v = m0(t) if m0 else Tf()
                if t < t_xa:
                    return v
                z = s_ab * zoom_a(t)
                # first apply A's own motion, then the framing map (approximated: translate + uniform scale)
                px_ = v.px if v.px is not None else pa[0]
                py_ = v.py if v.py is not None else pa[1]
                return Tf(dx=(pa[0] + (px_ + v.dx - pa[0]) * z) - px_ + (b0.x - pa[0]),
                          dy=(pa[1] + (py_ + v.dy - pa[1]) * z) - py_ + (b0.y - pa[1]),
                          rot=v.rot, sx=v.sx * z, sy=v.sy * z, alpha=v.alpha, px=px_, py=py_)
            lay.motion = mm

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_calm", 0, dur=T + 0.1, gain_db=-19, fade_in=0.8, fade_out=0.9)
    sc.sfx("wind_soft", t_wind - 0.2, dur=4.8, gain_db=-14, fade_in=0.6, fade_out=1.4)
    sc.sfx("chime", t_wind, gain_db=-16)
    sc.sfx("thud", t_land, gain_db=-9, duck_db=-3)
    sc.sfx("splash_small", t_land + 0.02, gain_db=-14)
    sc.sfx("ship_creak", t_land + 0.05, dur=1.4, gain_db=-17, fade_out=0.8)
    sc.sfx("birds", t_xb, dur=T - t_xb + 0.1, gain_db=-26, fade_in=1.5, fade_out=0.9)
    sc.sfx("cloth", t_open, gain_db=-14)
    sc.sfx("whoosh", t_fly1, gain_db=-15, pan=-0.3)
    sc.sfx("whoosh", t_home1 - 0.4, gain_db=-18, pan=-0.1)
    for k in range(7):
        sc.sfx("pop", t_days1 + 0.35 + 0.2 * k, gain_db=-20, pan=-0.5)
        sc.sfx("pop", t_days2 + 0.35 + 0.2 * k, gain_db=-20, pan=-0.5)
    sc.sfx("whoosh", t_fly2, gain_db=-15, pan=-0.3)
    sc.sfx("night", t_eve, dur=t_days2 - t_eve, gain_db=-24, fade_in=1.0, fade_out=1.0)
    sc.sfx("whoosh", t_sill - 0.35, gain_db=-17, pan=-0.1)
    sc.sfx("sparkle", t_take + 0.05, gain_db=-12)
    sc.sfx("chime", t_dry, gain_db=-15)
    sc.sfx("rooster", t_days2 + 0.2, gain_db=-24, pan=-0.6)
    sc.sfx("whoosh", t_fly3, gain_db=-15, pan=-0.4)
    return sc
