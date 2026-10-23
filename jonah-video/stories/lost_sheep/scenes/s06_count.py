"""Scene 6 - Luke 15:4 / Matthew 18:12. Sunset on the same hillside. It opens on exactly the last frame of s05 (a plain
fade = a time-lapse from morning to a rose-gold evening: the little lamb still alone beyond the rise); the camera tilts
up to the big orange sun sinking behind the hills. Cut to the shepherd at the flock: the sheep hop past him one by
one, he taps each with his crook and a number pops up; the count races on, slows to 97, 98, 99 ... and stops. He is
puzzled, counts again (pointing along the resting flock, numbers flicking), still 99: the little lamb is missing. He
looks to the hills, lifts his lantern and sets off up the path into the dusk, leaving the ninety-nine resting together
on the open hillside (no sheepfold).

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Storm film's
Beats class; nothing hard-coded to the take):
  0 .. 1.0      identical to the end of s05 at sunset (the lamb looks around, alone)
  '太阳'         the lamb looks back over its shoulder; the camera tilts up to the sun, which sinks toward the hills
  '回家以前'     cut to the shepherd at the flock: he calls the sheep (hands cupped, call arcs)
  '牧羊人'       the first sheep come hopping in from the right; '数羊' he holds out his crook over the line
  '一只/两只/三只' a sheep passes under the crook on each number: tap + a number bubble (1, 2, 3) on the syllable
  '数啊数'       the line trots faster, one hop per sheep, the taps and numbers race (12, 25, ... 91, 96)
  '九十七/八/九'  slower again: 97, 98, 99 on each '九'
  '咦'           no more sheep: he scratches his head ('?'), the bubble shows '99?'
  '我再数一遍'   he turns to the resting flock, leaning forward, finger pointing
  '数啊数'       quick jabs, little numbers pop over the resting sheep one after another
  '还是九十九只'  a big '99' on '九十九'
  '少了一只小羊'  hands on his cheeks, worried; a thought bubble with the little lamb and a '?' on '小羊'
  '我的小羊呢'   he peers toward the hills, a hand at his brow, then bends to the lantern on the grass in front of
                him and lifts it into his hand; '我要' he straightens up with it
  '我要去找它'   on '去' he lifts it high, lit (its light blooms), and sets off - always facing right, the way he goes
  '牧羊人把'     the camera pulls back over the whole hillside at dusk: the ninety-nine rest together, he walks up the
                path toward the hills, smaller and smaller, the lantern glowing
  end           s07 opens on exactly this frame (the same clock: he keeps walking), then goes to the lamb
"""
import bisect
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import snap
from stories.storm.scenes.s03_friends import Beats
from stories.lost_sheep.scenes.s05_flock import (CAM_END, GY, H5, HS, HX0, HX1, HSEED, INK, K, KL, LAMB_END,
                                                 REST_POSES, STREAM_X, W5, X_LAND, X_SNIFF, YL, YS, Fig, add_clouds, blink,
                                                 cam_path, doc, env, f1, flock_band_markup, flower_frame, flowers_svg, gate,
                                                 knoll_markup, lamb_fig_draw, lone_tree_markup, persp, pop_motion,
                                                 question_markup, sheep_markup, shepherd_markup, sky_svg, squash,
                                                 sun_markup)

# ------------------------------------------------------------------ geometry (shared with s07)
TIMES6 = (0.35, 0.45, 0.55, 0.62)          # backdrop frames, cross-faded by tod(t)
SX = 1650                                   # the shepherd's counting spot
CX = SX + 270 * K                           # the crook taps the passing sheep here
YW = YS - 14                                # the counting line (just behind him)
GAP = 215 * persp(YW)                       # spacing of the sheep in the line
NUMS = (1, 2, 3, 4, 12, 25, 38, 52, 66, 80, 91, 96, 97, 98, 99)
BUB = (CX - 40, YS - 345 * K)               # where the count bubbles pop (above the tapped sheep)
LANTERN0 = (SX + 99 * K, YS + 8)            # the lantern waiting on the grass, in front of him (under his far hand
                                            # when he bends to it)
PATH = [(SX, YS), (SX + 150, YS - 36), (SX + 250, YS - 100), (SX + 390, YS - 160), (SX + 530, YS - 206),
        (SX + 610, YS - 262), (SX + 650, YS - 320), (SX + 720, YS - 372), (SX + 820, YS - 414), (SX + 900, YS - 462),
        (SX + 950, YS - 515)]
# resting sheep near the camera (own layers: they breathe; the recount numbers pop over them)
REST_HEROES = [(1270, 1338, "lie", 1, 1), (1080, 1395, "graze", -1, 3), (905, 1318, "lie", -1, 0),
               (760, 1410, "stand", 1, 5), (600, 1340, "lie", 1, 2), (1180, 1468, "lie", -1, 4)]
REST_BAND_MEAD = (40, 1260, 1128, 1400, 50, 32)
REST_BAND_MID = (90, 1500, 905, 1092, 40, 31)
CAM_COUNT = Cam(1770, 1190, 1560)
CAM_WIDE = Cam(1640, 870, 2950)
WALK_ADV = (26.1, 59.3, 56.8, 28.7)          # parable_shepherd walk_a -> c -> b -> c planted advances (scale 1)
WALK_SEQ = ("walk_a", "walk_c", "walk_b", "walk_c")
WALK_PER = 0.24


def path_len():
    out = [0.0]
    for (xa, ya), (xb, yb) in zip(PATH, PATH[1:]):
        out.append(out[-1] + math.hypot(xb - xa, yb - ya))
    return out


_PL = path_len()


def path_at(d):
    """Stage point at arc length d along the path."""
    d = max(0.0, min(_PL[-1], d))
    i = min(len(PATH) - 2, bisect.bisect_right(_PL, d) - 1)
    u = (d - _PL[i]) / max(1e-6, _PL[i + 1] - _PL[i])
    (xa, ya), (xb, yb) = PATH[i], PATH[i + 1]
    return xa + (xb - xa) * u, ya + (yb - ya) * u


def tod_index(tm):
    """Fractional frame index of time-of-day tm in TIMES6."""
    if tm <= TIMES6[0]:
        return 0.0
    for i in range(len(TIMES6) - 1):
        if TIMES6[i] <= tm <= TIMES6[i + 1]:
            return i + (tm - TIMES6[i]) / (TIMES6[i + 1] - TIMES6[i])
    return len(TIMES6) - 1.0


def q05(tm):
    return round(tm * 20) / 20


# ------------------------------------------------------------------ drawings
def path_markup(time):
    pal = PR._ls_pal(time)
    col = S.mix(PR._lt("#e8d6a6", time, 0.9), pal["near2"], 0.35)
    edge = S.mix(PR._lt("#c9a56e", time, 0.9), pal["near"], 0.3)
    left, right = [], []
    n = 40
    for i in range(n + 1):
        d = _PL[-1] * i / n
        x, y = path_at(d)
        x2, y2 = path_at(min(_PL[-1], d + 4))
        x1, y1 = path_at(max(0.0, d - 4))
        tx, ty = x2 - x1, y2 - y1
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = 27 * persp(y) * (1.0 + 0.2 * math.sin(i * 0.9))
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    body = S.path(S.smooth_path(pts, closed=True, tension=0.7), fill=col, sw=2.2, extra='stroke-opacity="0.7"')
    rng = random.Random(9)
    for i in range(26):
        d = rng.uniform(0, _PL[-1])
        x, y = path_at(d)
        s = persp(y)
        body += (f'<ellipse cx="{f1(x + rng.uniform(-12, 12) * s)}" cy="{f1(y + rng.uniform(-5, 5) * s)}" '
                 f'rx="{f1(rng.uniform(3, 7) * s)}" ry="{f1(rng.uniform(2, 4) * s)}" fill="{edge}" opacity="0.7"/>')
    for i in range(14):
        d = rng.uniform(0, _PL[-1])
        x, y = path_at(d)
        s = persp(y)
        body += PR.wildflower(x + rng.choice((-1, 1)) * rng.uniform(34, 50) * s, y + rng.uniform(-4, 8) * s, 0.9 * s,
                              kind=rng.choice(PR.LS_FLOWERS), time=time)
    return S.g(body, filter="wobble")


def sky6_svg(time):
    return sky_svg(time)


def land_svg(time):
    """Everything static on the hillside at ``time``: hills, the resting ninety-nine, the path, the rise, flowers."""
    gaps_m = [(SX, YS - 20, 260), (SX + 300, YS - 40, 300), (CX + 200, YW - 20, 380)]
    gaps_m += [(x, y - 10, 150) for x, y, *_ in REST_HEROES]
    body = PR.spring_hills(HX0, HX1, GY, HS, time=time, part="back", seed=HSEED, stream_x=STREAM_X)
    body += PR.spring_hills(HX0, HX1, GY, HS, time=time, part="mid", seed=HSEED, stream_x=STREAM_X)
    body += lone_tree_markup(time)
    body += flock_band_markup(REST_BAND_MID, time, 0.0, poses=REST_POSES, on_mid=True)
    body += PR.spring_hills(HX0, HX1, GY, HS, time=time, part="front", seed=HSEED, stream_x=STREAM_X)
    body += path_markup(time)
    body += flock_band_markup(REST_BAND_MEAD, time, 0.0, poses=REST_POSES, gaps=gaps_m, on_mid=False)
    body += PR.wildflower(X_SNIFF + 76 * KL, YL, 0.9 * KL, kind="poppy", sway=0.3, time=time)   # the poppy it sniffed
    kb, kd = knoll_markup(time)
    body += kb
    return doc(body, kd)


def add_flowers(sc, g0, sets, set_fn, gate_m=None):
    """The swaying foreground flowers (the same sway on the film's clock as in s05), one set of 3 sway frames per
    time of day in ``sets``; set_fn(t) picks the set (switch it while they are off screen)."""
    frames = [flowers_svg(k, tm) for tm in sets for k in range(3)]
    sway = flower_frame(g0)
    sc.add("flowers", frames, z=9, seed=520, frame_at=lambda t: float(3 * set_fn(t)) + sway(t), motion=gate_m)


def bubble_svg(n, x=BUB[0], y=BUB[1], s=1.6):
    return doc(PR.count_bubble(x, y, n, s * K, pop=1.0))


def thought_svg(x, y, time):
    """A thought bubble with the little lamb and a '?' (the one that is missing)."""
    r = 120
    b = ""
    for i, (u, rr) in enumerate(((0.0, 11), (0.45, 17))):
        px, py = x - 150 + 95 * u, y + 175 - 120 * u
        b += f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{rr}" fill="#fffaf0" stroke="{INK}" stroke-width="3.4"/>'
    circ = [(x - 70, y + 18, 70), (x + 62, y + 20, 72), (x, y - 40, 88), (x - 95, y - 30, 56), (x + 98, y - 34, 58),
            (x, y + 48, 70)]
    b += "".join(f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(cr + 3.5)}" fill="{INK}"/>' for cx, cy, cr in circ)
    b += "".join(f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(cr)}" fill="#fffaf0"/>' for cx, cy, cr in circ)
    b += PR.little_lamb(x - 18, y + 70, 0.95, 1, pose="look_around", time=0.0)
    b += question_markup(x + 92, y - 40, 1.6)
    return doc(S.g(b, filter="wobble-fine"))


def walker_draw(variant, time):
    def d(st, k=None):
        pose, ph = st
        if k is not None:
            ph = k / 4.0
        return sheep_markup(CX, YW, pose, ph, -1, variant, time=time)
    return d


# ------------------------------------------------------------------ the count schedule
def pchip(xs, ys):
    """Monotone cubic interpolation (Fritsch-Carlson) through (xs, ys); returns f(x)."""
    n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    dl = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = dl[0], dl[-1]
    for i in range(1, n - 1):
        if dl[i - 1] * dl[i] <= 0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / dl[i - 1] + w2 / dl[i])

    def f(x):
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        i = bisect.bisect_right(xs, x) - 1
        t = (x - xs[i]) / h[i]
        h00, h10 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t
        h01, h11 = -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        return h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]
    return f


def count_plan(b):
    """Tap times of the 15 sheep (k = 1..15) and the line position P(t) (= k when sheep k is under the crook)."""
    t1, t2, t3 = b.at(1, "一只"), b.at(1, "两只"), b.at(1, "三只")
    sh = [b.at(2, "数啊数"), b.at(2, "数啊数", 1), b.at(2, "数啊数", 2)]
    m2 = b.marks[2]
    second = m2[1] if len(m2) > 1 else None
    if second is not None:
        from stories.noah.scenes.s01_title import char_times
        ct = char_times(second)
        sh2 = [ct[0], ct[1], ct[2]]
    else:
        sh2 = [sh[2] + 0.7, sh[2] + 0.95, sh[2] + 1.2]
    fast = [sh[0], sh[1], sh[2], (sh[2] + sh2[0]) / 2, sh2[0], sh2[1], sh2[2]]
    t97, t98, t99 = b.at(3, "九十七"), b.at(3, "九十八"), b.at(3, "九十九")
    t4 = (t3 + fast[0]) / 2 + 0.1
    t96 = (fast[-1] + t97) / 2 + 0.05
    taps = [t1, t2, t3, t4] + fast + [t96, t97, t98, t99]
    xs = [t1 - 2.75] + taps + [t99 + 1.2, t99 + 2.9]
    ys = [-2.6] + [float(k) for k in range(1, 16)] + [16.4, 20.6]
    return taps, pchip(xs, ys)


# ------------------------------------------------------------------ the shepherd walking away up the path (shared with s07)
def walk_away(t_go):
    """Planted-foot walk up the path from t_go (scene time): returns (state_fn(t) -> (pose index 0..3 or None),
    pos(t) -> (x, y, scale)). The anchor advances at each cut by the planted stride for the current scale."""
    cuts = []
    d = 0.0
    t = t_go
    k = 0
    while d < _PL[-1] - 1 and k < 80:
        x, y = path_at(d)
        s = persp(y)
        cuts.append((t, k % 4, d))
        d += WALK_ADV[(k + 1) % 4] * s * 1.05
        t += WALK_PER
        k += 1
    ts = [c[0] for c in cuts]

    def state(t):
        if t < t_go:
            return None
        i = bisect.bisect_right(ts, t) - 1
        return cuts[min(i, len(cuts) - 1)][1]

    def pos(t):
        if t < t_go:
            x, y = path_at(0.0)
            return x, y, persp(y)
        i = bisect.bisect_right(ts, t) - 1
        i = min(i, len(cuts) - 1)
        d0 = cuts[i][2]
        if i + 1 < len(cuts):
            d1 = cuts[i + 1][2]
            u = M.progress(t, cuts[i + 1][0] - 0.05, cuts[i + 1][0] + 0.05, "sine")
            dd = d0 + (d1 - d0) * u if t > cuts[i + 1][0] - 0.05 else d0
        else:
            dd = d0
        x, y = path_at(dd)
        return x, y, persp(y)
    return state, pos


def beats6(ctx):
    b = Beats(ctx)
    return dict(b=b, t_tai=b.at(0, "太阳快下山了"), t_xia=b.at(0, "太阳快下山了", 3), t_hui=b.at(0, "回家以前"),
                t_mu=b.at(0, "牧羊人在山坡上数羊"), t_shu=b.at(0, "牧羊人在山坡上数羊", 7),
                t_yi=b.at(3, "咦"), t_zai=b.at(3, "我再数一遍"),
                t_rs=b.at(4, "数啊数"), t_rs2=b.at(4, "数啊数", 2), t_hai=b.at(4, "还是九十九只"),
                t_99=b.at(4, "还是九十九只", 2), t_shao=b.at(4, "少了一只小羊"), t_xy=b.at(4, "少了一只小羊", 4),
                t_wd=b.at(5, "我的小羊呢"), t_wy=b.at(5, "我要去找它"), t_qu=b.at(5, "我要去找它", 2),
                t_ba=b.at(6, "牧羊人把九十九只羊留在山坡上"), t_zj=b.at(6, "自己去找那一只"))


def plan6(ctx):
    """Times shared by s06 and s07: the walk-away start, the time of day curve."""
    B = beats6(ctx)
    t_go = snap(B["t_qu"] + 0.95)
    T = ctx.duration

    def tod(t):
        v = 0.35
        v += 0.10 * M.progress(t, B["t_yi"], B["t_shao"], "sine")
        v += 0.10 * M.progress(t, B["t_wd"] - 0.5, B["t_ba"], "sine")
        v += 0.07 * M.progress(t, B["t_ba"], T - 1.2, "sine")
        return v
    return B, t_go, tod


def add_walk_away(sc, t_go, g0, tod_end, gate_m=None, z=6.6, offset=0.0, name="shep_walk"):
    """The shepherd walking up the path with his lantern (frames drawn at the path's start, moved and scaled along
    it), plus the lantern's light. ``offset``: scene time of the caller minus s06's scene time (s07 passes the dissolve
    offset so the walk continues seamlessly)."""
    state, pos = walk_away(t_go)
    x0, y0 = path_at(0.0)
    frames = []
    for p in ("walk_a", "walk_c", "walk_b"):
        body, defs = shepherd_markup(x0, y0, p, "determined", 1, time=tod_end, lantern=True, glow=0.0)
        frames.append(doc(body, defs))
    idx = {0: 0, 1: 1, 2: 2, 3: 1}

    def fa(t):
        s = state(t + offset)
        return float(idx[s if s is not None else 0])

    def mot(t):
        tt = t + offset
        if tt < t_go:
            return Tf(alpha=0.0)
        x, y, s = pos(tt)
        k = s / K
        a = 1.0 if gate_m is None else gate_m(t).alpha
        dip = M.keys([(t_go, {"dy": 6 * K, "sy": 0.96}), (t_go + 0.13, {"dy": -2 * K, "sy": 1.012}),
                      (t_go + 0.28, {"dy": 0, "sy": 1})], ["out", "sine"])(tt)
        return Tf(dx=x - x0, dy=y - y0 + dip.dy, sx=k, sy=k * dip.sy * (1 + 0.008 * math.sin(2 * math.pi * (t + g0) / 0.48)),
                  px=x0, py=y0, alpha=a)
    sc.add(name, frames, z=z, seed=611, frame_at=fa, motion=mot)
    # the lantern light: follows the far hand (lantern handle offsets per drawing, scale 1)
    hand = {0: (73.6, -127.8), 1: (67.3, -130.1), 2: (65.5, -126.4)}
    lx, ly = x0, y0
    glow = doc(PR.lantern_light(lx, ly, 1.0, radius=200, k=1.0))

    def gmot(t):
        tt = t + offset
        if tt < t_go:
            return Tf(alpha=0.0)
        x, y, s = pos(tt)
        st = state(tt)
        hx, hy = hand[idx[st if st is not None else 0]]
        fl = 0.72 + 0.09 * math.sin(2 * math.pi * (t + g0) / 0.37) + 0.05 * math.sin(2 * math.pi * (t + g0) / 0.13)
        a = (1.0 if gate_m is None else gate_m(t).alpha) * fl
        return Tf(dx=x + hx * s - lx, dy=y + (hy + 45) * s - ly, sx=s * 1.1, sy=s * 1.1, px=lx, py=ly, alpha=a)
    sc.add(name + "_light", glow, z=z + 0.05, wc=0, blend="screen", seed=612, motion=gmot)


SEED6 = {"sky": 501, "land": 503}


def add_rest_heroes(sc, g0, times, frame_at=None, gate_m=None):
    """The resting sheep near the camera (breathing on the film's clock)."""
    for i, (x, y, pose, f, v) in enumerate(REST_HEROES):
        frames = [doc(sheep_markup(x, y, pose, 0.0, f, v, time=tm)) for tm in times]
        mot = lambda t, x=x, y=y, i=i: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * ((t + g0) / 2.6 + 0.3 * i)), px=x, py=y)
        sc.add(f"rest{i}", frames if len(frames) > 1 else frames[0], z=4 + y / 1000, seed=640 + i,
               frame_at=frame_at if len(frames) > 1 else None, motion=M.combine(mot, gate_m) if gate_m else mot)


def add_dusk_hillside(sc, g0, gate_m, offset, t_go):
    """s06's last frame (the ninety-nine resting at dusk, the shepherd walking up the path) for s07's first shot.
    offset = the caller's scene time -> s06 scene time."""
    tm = TIMES6[-1]
    sc.add("sky6", sky6_svg(tm), z=0, seed=SEED6["sky"], motion=gate_m)
    add_clouds(sc, g0, [tm], gate_m=gate_m, g_draw=g0 - offset)
    sc.add("land6", land_svg(tm), z=1, seed=SEED6["land"], motion=gate_m)
    add_rest_heroes(sc, g0, [tm], gate_m=gate_m)
    add_flowers(sc, g0, [tm], lambda t: 0, gate_m)
    add_walk_away(sc, t_go, g0, 0.6, gate_m=gate_m, offset=offset)


# ------------------------------------------------------------------ the scene
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    B, t_go, tod = plan6(ctx)
    b = B["b"]
    rng = random.Random(6)
    t_cut = snap(B["t_hui"] - 0.12)
    shot1 = gate(-1e9, t_cut)
    shot2 = gate(t_cut, 1e9)
    taps, Pf = count_plan(b)

    # ================================================================ the sky, the sun, the clouds (both shots)
    tfa = lambda t: tod_index(tod(t))
    sc.add("sky", [sky6_svg(tm) for tm in TIMES6], z=0, frame_at=tfa, seed=SEED6["sky"])
    sun = (3760, 520)
    sun_y = lambda t: 70 * M.progress(t, 0.0, t_cut + 0.5, "sine") + 260 * M.progress(t, t_cut, T, "sine")
    sc.add("sun", doc(sun_markup(*sun, 0.35)), z=0.2, wc=0.5, motion=lambda t: Tf(
        dy=sun_y(t), rot=1.2 * (t + g0), px=sun[0], py=sun[1], alpha=1 - M.progress(t, T * 0.6, T - 2.0)))
    add_clouds(sc, g0, TIMES6, frame_at=tfa)

    # ================================================================ shot 1: the lamb beyond the rise at sunset
    sc.add("land", [land_svg(tm) for tm in TIMES6], z=1, frame_at=tfa, seed=SEED6["land"])
    add_flowers(sc, g0, [TIMES6[0], TIMES6[-1]], lambda t: 1 if t >= B["t_wd"] - 0.5 else 0)
    lamb = Fig("lamb", lamb_fig_draw(0.35), (X_LAND, YL), KL, 8.5, g0, seed=121, pivot=lambda st: (st[2], st[3]))
    lamb.cut(0, LAMB_END)
    lamb.cut(B["t_tai"] + 0.05, ("look_around", 0.6, X_LAND, YL, 1, "open"), depth=4)
    lamb.cut(B["t_xia"], LAMB_END, depth=4)
    lamb.mots += [lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * (t + g0) / 2.1)), shot1]
    lamb.build(sc)

    # ================================================================ shot 2: the counting
    # the resting heroes (breathing; the recount numbers pop over them)
    tm_c = 0.37
    add_rest_heroes(sc, g0, TIMES6, tfa, shot2)
    # the counting line: 15 sheep hopping past (k = 1..15), a little out of step with each other
    hop_len = GAP / 2
    variants = (1, 3, 0, 4, 2)
    for k in range(1, 16):
        v = variants[k % len(variants)]
        draw = walker_draw(v, tm_c)
        hop_st = ("hop", 0.0)

        def x_of(t, k=k):
            return CX + (k - Pf(t)) * GAP

        def fn(t, k=k):
            dist = Pf(t) * GAP
            return int(((dist / hop_len) + 0.37 * k) % 1.0 * 4)
        fig = Fig(f"walker{k}", draw, (CX, YW), persp(YW), 6.0 + 0.01 * k, g0, seed=650 + v,
                  loops={hop_st: (4, fn)})
        fig.cut(0, hop_st)

        def mot(t, k=k, x_of=x_of):
            x = x_of(t)
            vis = 1.0 if (t >= t_cut and 890 < x < 2900) else 0.0
            return Tf(dx=x - CX, alpha=vis)
        fig.mots.append(mot)
        fig.build(sc)

    # the shepherd
    def shep(pose, expr, f=1, ph=0.0, tm=0.35, lantern=False):
        return (pose, expr, f, ph, q05(tm), lantern)

    def shep_draw(st, k=None):
        pose, expr, f, ph, tm, lan = st
        if k is not None:
            ph = (k / 4.0 + 0.5) % 1.0
        return shepherd_markup(SX, YS, pose, expr, f, ph, tm, lantern=lan, glow=0.0)

    sh = Fig("shepherd", shep_draw, (SX, YS), K, 6.5, g0, seed=601)
    sh.cut(0, shep("stand", "warm"))
    sh.cut(B["t_hui"] - 0.02, shep("call", "happy"), depth=5)
    sh.cut(B["t_mu"] + 0.1, shep("stand", "happy"), depth=4)
    cnt = shep("count", "happy")
    sh.loops[cnt] = (4, lambda t: int(((Pf(t) % 1.0)) * 4))
    sh.cut(B["t_shu"] - 0.1, cnt, depth=5)
    sh.cut(B["t_yi"] - 0.04, shep("puzzled", "puzzled", tm=tod(B["t_yi"])), depth=6)
    sh.cut(B["t_zai"] - 0.05, shep("count_again", "determined", -1, tm=tod(B["t_zai"])), depth=6)
    sh.cut(B["t_hai"] + 0.1, shep("count_again", "puzzled", -1, tm=tod(B["t_hai"])), dip=False)
    sh.cut(B["t_shao"] - 0.05, shep("worried", "worried", 1, tm=tod(B["t_shao"])), depth=6)
    # '我的小羊呢': he peers toward the hills (facing right, the way he will go: no more turning from here on) ...
    t_peer = snap(B["t_wd"] - 0.05)
    sh.cut(t_peer, shep("look_around", "worried", 1, 0.0, tod(B["t_wd"])), depth=5)
    # ... bends to the lantern waiting on the grass in front of him and lifts it into his far hand ...
    t_up = snap(B["t_qu"] - 0.05)
    t_pick = snap(max(t_peer + 0.55, t_up - 1.25))
    t_stand = snap(t_pick + 0.62)
    sh.cut(t_pick, shep("count_again", "determined", 1, 0.0, tod(B["t_wd"])), depth=6)
    # ... straightens up with it hanging from his hand (the figure's own lantern, 36 px from the bent hand) ...
    sh.cut(t_stand, shep("stand", "determined", 1, 0.0, tod(B["t_wy"]), True), depth=6)
    # ... and on '去' lifts it high, lit (the light blooms); the walk away starts facing the same way
    sh.cut(t_up, shep("look_around", "determined", 1, 0.0, tod(B["t_qu"]), True), depth=7)
    sh.add_blinks({shep("stand", "warm"): shep("stand", blink("warm")),
                   shep("stand", "happy"): shep("stand", blink("happy"))}, t_cut, B["t_shu"], rng)
    # recount jabs: little rocks forward on each count
    jabs = [B["t_rs"] + (B["t_rs2"] - B["t_rs"] + 0.25) * i / 4 for i in range(5)]
    sh.mots.append(lambda t: Tf(rot=sum(2.5 * env(t, tj - 0.06, tj + 0.16, 0.06, 0.1) for tj in jabs)))
    sh.mots.append(lambda t: Tf(sy=1 + 0.01 * math.sin(2 * math.pi * (t + g0) / 3.1)))
    sh.mots.append(lambda t: Tf(alpha=1.0 if t_cut <= t < t_go else 0.0))
    sh.build(sc)
    hand_b = C.shepherd_points(SX, YS, K, 1, pose="count_again")["hands"][0]     # his far hand when he bends
    lx0, ly0 = LANTERN0[0], LANTERN0[1] - 64 * K

    def lantern_mot(t):
        """The lantern on the grass; lifted into his hand while he bends; from t_stand the figure draws it (hanging
        from his far hand, then raised on '去')."""
        if not (t_cut <= t < t_stand):
            return Tf(alpha=0.0)
        u = M.progress(t, t_pick + 0.1, t_pick + 0.32, "out")
        sw = 3 * math.sin(2 * math.pi * (t - t_pick) / 0.6) * M.progress(t, t_pick + 0.3, t_pick + 0.4)
        return Tf(dx=(hand_b[0] - lx0) * u, dy=(hand_b[1] - ly0) * u, rot=sw, px=lx0, py=ly0)
    sc.add("lantern0", doc(PR.ls_lantern(lx0, ly0, K, lit=0.0, glow=False)), z=6.45, seed=605, motion=lantern_mot)
    # the lantern's light blooming when he lifts it (raised in look_around), then the walk away
    lx, ly = SX + 133 * K, YS - 222 * K + 40 * K
    sc.add("lift_light", doc(PR.lantern_light(lx, ly, 1.0, radius=230)), z=6.55, wc=0, blend="screen", seed=606,
           motion=lambda t: Tf(alpha=env(t, B["t_qu"], t_go + 0.02, 0.35, 0.02) *
                               (0.78 + 0.12 * math.sin(2 * math.pi * (t + g0) / 0.37))))
    add_walk_away(sc, t_go, g0, 0.6)

    # count bubbles: one per tap (pop up, drift up, fade by the next number or so)
    for k, (tk, n) in enumerate(zip(taps, NUMS)):
        nxt = taps[k + 1] if k + 1 < len(taps) else B["t_yi"]
        t_out = min(tk + 1.0, nxt + 0.05) if n != 99 else B["t_yi"] + 0.05
        rise = 0.0 if n == 99 else 90.0 * (t_out - tk) / max(0.3, nxt - tk + 0.05)
        sc.add(f"num{k}", bubble_svg(n), z=7 + 0.01 * k, wc=0, seed=670 + k,
               motion=pop_motion(tk, BUB, 0.26, t_out, min(0.22, 0.5 * (t_out - tk)), rise=rise))
        sc.sfx("pop", tk, gain_db=-20 if n not in (97, 98, 99) else -17)
    sc.add("num99q", bubble_svg("99?"), z=7.2, wc=0, seed=690,
           motion=pop_motion(B["t_yi"], BUB, 0.3, B["t_zai"] - 0.1, 0.3))
    sc.add("shep_q", doc(question_markup(SX + 70 * K, YS - 420 * K, 1.4)), z=7.21, wc=0, seed=691,
           motion=pop_motion(B["t_yi"] + 0.1, (SX + 70 * K, YS - 410 * K), 0.3, B["t_zai"] - 0.1, 0.3))
    # the recount: little numbers over the resting sheep, then the big 99
    rs_items = [(REST_HEROES[0], 12), (REST_HEROES[1], 35), (REST_HEROES[2], 58), (REST_HEROES[3], 80),
                (REST_HEROES[4], 96)]
    for i, ((x, y, pose, f, v), n) in enumerate(rs_items):
        bx, by = x, y - 190 * persp(y)
        sc.add(f"rnum{i}", bubble_svg(n, bx, by, 1.25), z=7.3 + 0.01 * i, wc=0, seed=692 + i,
               motion=pop_motion(jabs[i], (bx, by), 0.22, jabs[i] + 0.55, 0.2, rise=24))
        sc.sfx("pop", jabs[i], gain_db=-22)
    bx, by = SX - 40 * K, YS - 440 * K
    sc.add("num99b", bubble_svg(99, bx, by, 1.8), z=7.4, wc=0, seed=699,
           motion=pop_motion(B["t_99"], (bx, by), 0.35, B["t_shao"] + 0.2, 0.3))
    sc.sfx("pop", B["t_99"], gain_db=-16)
    th = (SX + 330 * K, YS - 440 * K)
    sc.add("thought", thought_svg(*th, 0.45), z=7.5, wc=0.3, seed=700,
           motion=M.combine(pop_motion(B["t_xy"] - 0.1, (th[0] - 150, th[1] + 175), 0.45, B["t_wd"] + 0.3, 0.35),
                            lambda t: Tf(dy=5 * math.sin(2 * math.pi * (t + g0) / 2.0))))

    # ================================================================ camera
    # every move eased with 'sine' and long enough to stay under ~0.6 frame-widths/s (fastest frame corner)
    shot1_cam = cam_path([(0.0, CAM_END), (1.0, CAM_END), (t_cut - 0.05, Cam(3470, 800, 1660)), (t_cut, Cam(3470, 800, 1660))],
                         ["linear", "sine", "linear"])
    shot2_cam = cam_path([
        (t_cut, CAM_COUNT), (B["t_yi"] - 0.4, CAM_COUNT), (B["t_yi"] + 0.9, Cam(1720, 1210, 1380)),
        (B["t_zai"] - 0.4, Cam(1720, 1210, 1380)), (B["t_rs"] - 0.05, Cam(1240, 1160, 1900)),
        (B["t_99"] + 0.35, Cam(1240, 1160, 1900)), (B["t_xy"] + 0.3, Cam(1640, 1190, 1460)),
        (B["t_wd"] - 0.2, Cam(1640, 1190, 1460)), (B["t_wy"], Cam(1760, 1180, 1560)),
        (t_go + 0.2, Cam(1760, 1180, 1560)), (B["t_zj"] + 0.5, CAM_WIDE), (T, CAM_WIDE)],
        ["linear", "sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear"])
    sc.camera = lambda t: shot1_cam(t) if t < t_cut else shot2_cam(t)

    # ================================================================ sound
    sc.sfx("wind_soft", 0, dur=T + 0.4, gain_db=-22, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=t_cut + 6.0, gain_db=-21, fade_in=0.8, fade_out=3.0)
    sc.sfx("sparkle", B["t_tai"] + 0.1, gain_db=-24, root=91, pan=0.3)
    sc.sfx("sheep", taps[0] + 0.35, gain_db=-19, pan=0.4, pitch=1.05)
    sc.sfx("sheep", taps[6] + 0.1, gain_db=-21, pan=0.3, pitch=1.2)
    sc.sfx("sheep", taps[13] + 0.3, gain_db=-20, pan=0.2, pitch=0.95)
    sc.sfx("cloth", B["t_zai"] - 0.05, gain_db=-21)
    sc.sfx("cloth", B["t_shao"] - 0.05, gain_db=-22)
    sc.sfx("sparkle", B["t_qu"], gain_db=-20, pan=0.1)
    sc.sfx("footsteps", t_go, dur=T - t_go + 0.6, gain_db=-24, pan=0.3, fade_out=1.2)
    sc.sfx("night", B["t_ba"] - 1.0, dur=T - B["t_ba"] + 1.5, gain_db=-24, fade_in=2.5, fade_out=0.8)
    return sc
