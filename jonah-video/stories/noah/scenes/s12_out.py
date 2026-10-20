"""Scene 12 — everybody comes out of the ark; the altar (Genesis 8:15-20).

One 2112 x 1188 stage, shared with s13 (which starts on this scene's last frame: same world, camera and cast,
plain dissolve; every idle motion runs on the film's global clock so the two scenes match during the dissolve).
A fresh morning on the green shoulder of Mount Ararat: the ark rests on the meadow with its ramp, an olive tree,
the washed valleys below with left-over lakes shining, the snowy peak far behind; soft golden light from the
upper left (God is light, never a figure).

  line 0  '上帝对挪亚说：'          the golden light grows over the ark.
  line 1  G '你和你的家人，还有所有的动物，都可以出来了。' the light pulses gently with the words; a golden rim of
          light glows round the closed door; little birds peek out of the small cabin windows.
  line 2  '门打开了！'               the big door swings open (the glow fades as it opens).
          '动物们一个接一个跑出来，' one after another: the elephants, then the giraffes (ducking through the door).
          '有的跳，'                  the rabbits hop out.
          '有的飞，'                  the high window opens and the little birds fly out into the sky.
          '有的跑，'                  horses and zebras gallop out.
          '开心极了！'               the monkeys cartwheel out, the elephants spray water for joy, Noah steps out
                                      and cheers on the landing, the family follows him down the ramp.
  line 3  '挪亚做的第一件事，就是筑了一座坛，' Noah and his sons gather at a spot below the ramp and put stones on a
          heap, one by one (a little thud each): a small stone altar.
          '感谢上帝。'               a little flame lights on the altar with a curl of smoke, everybody kneels to thank
                                      God, warm light. The turtles - last as always - are still crawling down the ramp.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s10_inside import stars_fx

INK = P["ink"]
KS = 0.5                         # everybody's scale (people, animals, ark)
AX, AY = 560, 790                # the ark (grounded, facing right, ramp down to the right)
PTS = PR.ark_points(AX, AY, KS, 1)
DOOR = PTS["door_box"]           # x0, top, x1, sill
SILL_Y = DOOR[3]
RAMP_TOP = PTS["ramp_top"]
RAMP_FOOT = PTS["ramp_bottom"]
WIN = PTS["window_box"]
RIDGE_Y = PTS["roof"][0][1]
HORIZON = 640
ALTAR = (1190, 984, 0.62)
FULL = Cam(W / 2, H / 2, W)      # the wide framing (s13 pulls back to it for the rainbow)
END_CAM = Cam(1230, 740, 1440)   # s12's last framing = s13's first

# where everyone ends up (feet), facing at rest
REST = {
    "elephant_m": (1530, 852, -1), "elephant_f": (1675, 838, -1),
    "giraffe_m": (1790, 822, -1), "giraffe_f": (1895, 808, -1),
    "zebra_m": (1600, 910, -1), "zebra_f": (1735, 898, -1),
    "horse_m": (1840, 924, -1), "horse_f": (1930, 908, -1),
    "rabbit_m": (1525, 988, -1), "rabbit_f": (1590, 976, -1),
    "monkey_m": (1705, 990, -1), "monkey_f": (1775, 978, -1),
    # the family round the altar: left side faces right, right side faces left
    "noah": (1092, 994, 1), "noah_wife": (1002, 986, 1), "shem": (1048, 948, 1), "daughter_in_law0": (958, 942, 1),
    "ham": (1292, 994, -1), "daughter_in_law1": (1382, 986, -1), "japheth": (1338, 948, -1),
    "daughter_in_law2": (1428, 942, -1),
}
BIRD_PERCH = [(420, "blue"), (505, "red"), (705, "yellow"), (790, "green")]
BIRD_S = 0.62


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


# ============================================================================ the world (shared with s13)


def sky_svg():
    """Sky with God's warm light from the upper left baked in (soft glow + broad rays)."""
    defs = S.lin_grad("s12sky", [(0, "#8cc6de"), (0.5, "#bfe0e8"), (0.85, "#f4ead2"), (1, "#f8e2b8")])
    defs += S.rad_grad("s12lb", [(0, "#fff3cc", 0.95), (0.35, "#fbe3a0", 0.5), (1, "#f8d98a", 0)])
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 140}" fill="url(#s12sky)"/>'
    body += f'<circle cx="160" cy="-60" r="1050" fill="url(#s12lb)"/>'
    body += S.g(S.path(S.rays(160, -60, 120, 1000, n=16, width_deg=5, rot=12), fill="#fff6dc", stroke=False),
                filter="blur-md", opacity=0.3)
    return doc(body, defs)


def light_svg():
    """Extra light while God speaks (screen-blended, alpha animated; 0 when idle)."""
    defs = S.rad_grad("s12lg", [(0, "#fff0c0", 1), (0.35, "#f8d98a", 0.55), (1, "#f2c14e", 0)])
    body = f'<circle cx="160" cy="-60" r="1050" fill="url(#s12lg)"/>'
    body += S.g(S.path(S.rays(160, -60, 120, 1000, n=16, width_deg=5, rot=12), fill="#fff3c8", stroke=False),
                filter="blur-md", opacity=0.55)
    return doc(body, defs)


def clouds_svg(seed=0):
    b = ""
    for i, (x, y, w, h) in enumerate(((560, 120, 420, 110), (1300, 80, 520, 120), (1880, 190, 380, 100),
                                      (980, 260, 300, 80))):
        b += S.cloud(x, y, w, h, fill="#fbf3e6", seed=seed + i, puffs=6, sw=3, shade_fill="#efe2cc")
    return doc(S.g(b, filter="wobble"))


def far_svg():
    """Far peaks, valleys with left-over lakes, green ridges (static)."""
    b = ""
    # the snowy peak far behind, right
    b += S.path(f"M1280,{HORIZON + 30} L1640,300 Q1700,250 1760,300 L2180,{HORIZON + 10} Z", fill="#c8c4cc", sw=3)
    b += S.path("M1640,300 Q1700,250 1760,300 L1800,336 L1760,350 L1720,330 L1680,356 L1640,334 L1602,350 Z",
                fill="#f6f1e6", sw=3)
    # hazy far ridges
    b += S.path(S.hill(-60, 900, HORIZON + 20, 120, seed=21, bottom=H, bumps=3), fill="#b6cbb0", sw=3)
    b += S.path(S.hill(700, 2180, HORIZON + 40, 90, seed=22, bottom=H, bumps=3), fill="#a9c6a0", sw=3)
    # valley floor with shining lakes
    b += f'<rect x="-40" y="{HORIZON + 30}" width="{W + 80}" height="200" fill="#9cc488"/>'
    for x, y, rx, ry in ((260, HORIZON + 66, 150, 16), (900, HORIZON + 58, 110, 12), (1500, HORIZON + 70, 180, 18),
                         (1950, HORIZON + 60, 120, 13)):
        b += (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#b9e0e3" {S.STROKE_THIN}/>'
              f'<path d="M{x - rx * 0.5},{y - 2} l{rx * 0.4},0" stroke="#fffaf0" stroke-width="3" stroke-linecap="round"/>')
    b += S.path(S.hill(-60, 1100, HORIZON + 110, 70, seed=23, bottom=H, bumps=3), fill="#8dbb6a", sw=3)
    b += S.path(S.hill(900, 2180, HORIZON + 120, 60, seed=24, bottom=H, bumps=3), fill="#93bf70", sw=3)
    rng = random.Random(6)
    for _ in range(26):
        x = rng.uniform(0, W)
        y = HORIZON + rng.uniform(70, 120)
        b += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="12" ry="9" fill="#5f9440" opacity="0.8"/>'
    return doc(S.g(b, filter="wobble"))


def meadow_svg():
    """The mountain's green shoulder where the ark rests (from y ~720 down), flowers, rocks, an olive tree."""
    defs = S.lin_grad("s12mead", [(0, "#a9cc74"), (0.5, "#93b85c"), (1, "#7ea84c")])
    top = [(-60, 740), (300, 724), (700, 744), (1100, 770), (1500, 790), (1900, 784), (2180, 770)]
    d = S.smooth_path(top, closed=False) + f" L{W + 60},{H + 60} L-60,{H + 60} Z"
    b = S.path(d, fill="url(#s12mead)", sw=4)
    rng = random.Random(12)
    for _ in range(90):
        x = rng.uniform(-20, W + 20)
        y = rng.uniform(800, 1180)
        b += f'<path d="M{f1(x)},{f1(y)} l-4,-12 M{f1(x + 5)},{f1(y)} l3,-14" stroke="#6f9a3e" stroke-width="3" stroke-linecap="round"/>'
    for _ in range(40):
        x = rng.uniform(0, W)
        y = rng.uniform(820, 1170)
        col = rng.choice(["#f2c14e", "#f0998a", "#fffaf0", "#c9a0dc", "#f6a43c"])
        b += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="6" fill="{col}" stroke="{INK}" stroke-width="2"/>'
              f'<circle cx="{f1(x)}" cy="{f1(y)}" r="2" fill="#e8a33c"/>')
    for x, y, r in ((120, 1060, 40), (1960, 1020, 34), (1480, 1100, 26)):
        b += S.path(S.blob(x, y, r, r * 0.7, 0.12, 8, seed=x), fill="#cbbfae", sw=3.5)
    b = S.g(b, filter="wobble")
    b += PR.olive_tree(150, 860, 0.62, seed=2) + PR.bush(350, 760, 0.45, 1) + PR.bush(1990, 800, 0.5, 0)
    return doc(b, defs)


def tufts_svg(phase):
    b = ""
    for i, (x, y, v) in enumerate(((60, 1150, 2), (330, 1140, 0), (620, 1160, 2), (880, 1150, 0), (1480, 1160, 2),
                                   (1760, 1150, 0), (2050, 1140, 2), (440, 1000, 0))):
        b += PR.grass_tuft(x, y, 0.8, variant=v, sway=0.5 * math.sin(phase * 2 * math.pi + i))
    return doc(b)


def ark_svg(door=1.0, window=1.0, glow=0.0):
    return doc(C.ground_shadow(AX, AY + 6, KS, 1700, 0.25) + PR.ark(AX, AY, KS, 1, door=door, window=window, glow=glow))


def occluder_svg(window=1.0):
    """The ark (door open) minus the doorway and everything on the ramp side below the lintel: drawn over people
    and animals still inside so they come out from behind the stern-side jamb."""
    x0, top, x1 = DOOR[0], DOOR[1], DOOR[2]
    clip = (f"M-40,-40 L{x1 + 6},-40 L{x1 + 6},{top} L{x0},{top} L{x0},{H + 40} L-40,{H + 40} Z")
    return doc(f'<clipPath id="s12occ"><path d="{clip}"/></clipPath>'
               f'<g clip-path="url(#s12occ)">{PR.ark(AX, AY, KS, 1, door=1.0, window=window)}</g>')


def fix_seeds(sc):
    """Watercolour seeds from the layer NAME (not its index) so s12's last frame and s13's first match."""
    import zlib
    for L in sc.layers:
        L.seed = zlib.crc32(L.name.encode()) % 997


def g_fx(fx, g, offset=200.0):
    """Run an engine fx on the film's clock (so the dissolve between s12 and s13 matches)."""
    return lambda frame, t, view: fx(frame, g(t) - offset, view)


def gtime(ctx):
    return lambda t: ctx.start + t


def g_breathe(g, pivot, amount=0.012, period=3.0, phase=0.0, on=None):
    def m(t):
        k = 1.0 if on is None else on(t)
        s = 1 + k * amount * math.sin(2 * math.pi * (g(t) / period + phase))
        return Tf(sx=s, sy=s, px=pivot[0], py=pivot[1])
    return m


def add_world(sc, g, light_alpha, door_frames=None, door_fa=None, occ_fa=None):
    """Sky, light, clouds, far land, meadow, the ark (+ its occluder), grass. Returns nothing."""
    # sky and far land are static and adjacent (one flattened item); the light and clouds go over them
    sc.add("sky", sky_svg(), seed=3, wc=0.6)
    sc.add("far", far_svg(), seed=5)
    sc.add("light", light_svg(), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=max(0.0, light_alpha(t))))
    sc.add("clouds", clouds_svg(70), motion=lambda t: Tf(dx=-60 + 9 * ((g(t) - 200) % 60)))


def add_ground(sc, g):
    sc.add("meadow", meadow_svg(), seed=7)


# ============================================================================ actors


def pathf(pts):
    """Polyline -> (length, f(d) -> (x, y, facing))."""
    segs = []
    tot = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        segs.append((tot, ln, x0, y0, x1, y1))
        tot += ln
    def f(d):
        d = clamp(d, 0, tot)
        fac = 1
        for s0, ln, x0, y0, x1, y1 in segs:
            if abs(x1 - x0) > 1:
                fac = 1 if x1 > x0 else -1
            if d <= s0 + ln or (s0, ln) == segs[-1][:2]:
                u = 0 if ln == 0 else (d - s0) / ln
                return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, fac
        return pts[-1][0], pts[-1][1], fac
    return tot, f


def exit_path(x_in, rest):
    """Inside the hold -> through the door -> down the ramp -> to the rest spot."""
    return [(x_in, SILL_Y), (RAMP_TOP[0], RAMP_TOP[1]), (RAMP_FOOT[0], RAMP_FOOT[1]), (rest[0], rest[1])]


class Actor:
    """One figure on its own layer. ``draw(key, facing)`` returns markup at the REST anchor; the layer is moved
    along an exit path. Frames: walk cycle (by distance), then scheduled poses after arrival."""

    def __init__(self, sc, g, name, draw, rest, t0=None, speed=200.0, walk=("walk_a", "walk_b"), stride=40.0,
                 x_in=None, schedule=(), pauses=(), s=KS, pose_in=None, extra_motion=None, roll=None,
                 breathe=(0.012, 3.0, 0.0), dip_depth=6, z=None, inside_until=None, keys_extra=()):
        xr, yr, fr = rest
        self.rest = (xr, yr)
        keys = []
        frames = []

        def key_idx(k):
            if k not in keys:
                keys.append(k)
                frames.append(doc(draw(k[0], k[1])))
            return keys.index(k)
        moving = t0 is not None
        if moving:
            tot, pf = pathf(exit_path(x_in, (xr, yr)))
        else:
            tot, pf = 0.0, (lambda d: (xr, yr, fr))
        # distance vs time with pauses [(d_at, dur, key)]
        pz = sorted(pauses)

        def dist(t):
            if not moving or t < t0:
                return 0.0
            tt = t - t0
            d = 0.0
            for d_at, dur, _ in pz:
                t_reach = (d_at - d) / speed
                if tt <= t_reach:
                    return min(tot, d + tt * speed)
                tt -= t_reach
                d = d_at
                if tt <= dur:
                    return d
                tt -= dur
            return min(tot, d + tt * speed)
        t_arr = None
        if moving:
            t_arr = t0 + tot / speed + sum(p[1] for p in pz)
        self.t_arr = t_arr
        walk_idx = {f: [key_idx((w, f)) for w in walk] for f in (-1, 1)}
        rest_idx = key_idx((schedule[0][1] if schedule else "stand", fr))
        sched = [(ts, key_idx((k, f_ if f_ is not None else fr))) for ts, k, *rest_f in schedule
                 for f_ in [rest_f[0] if rest_f else None]]
        pause_idx = [(d_at, dur, key_idx((k, 1))) for d_at, dur, k in pz]
        in_idx = {f: key_idx((pose_in, f)) for f in (1,)} if pose_in else None
        for k in keys_extra:
            key_idx(k)
        self.key_idx = key_idx
        cut_fa = cuts([(-1e9, rest_idx)] + sched)

        def fa(t):
            if moving and t < t_arr:
                d = dist(t)
                for d_at, dur, ki in pause_idx:
                    if abs(d - d_at) < 1e-6 and t >= t0:
                        return float(ki)
                x, y, f = pf(d)
                if in_idx and inside_until is not None and x < inside_until:
                    return float(in_idx[1])
                return float(walk_idx[f][int(d / stride) % len(walk)])
            return cut_fa(t)

        def mo(t):
            if moving and t < t0:
                return Tf(alpha=0.0)
            d = dist(t)
            x, y, f = pf(d)
            lift = 0.0
            if moving and t < t_arr:
                lift = -3 * s * abs(math.sin(math.pi * d / stride))
            rot = 0.0
            px_, py_ = xr, yr
            if roll is not None and moving and t < t_arr:
                rot = roll(d)
                px_, py_ = xr, yr - 80 * s
            return Tf(dx=x - xr, dy=y - yr + lift, rot=rot, px=px_, py=py_)
        arrived = (lambda t: 1.0) if not moving else (lambda t: M.progress(t, t_arr, t_arr + 0.6))
        dips = [dip(ts, s, (xr, yr), dip_depth) for ts, _ in sched if ts > 0]
        if moving:
            dips.append(dip(snap(t_arr), s, (xr, yr), dip_depth * 0.6))
        motion = M.combine(mo, *dips, g_breathe(g, (xr, yr), breathe[0], breathe[1], breathe[2], on=arrived),
                           extra_motion)
        self.layer_name = name
        self.frames = frames
        self.fa = fa
        self.dist = dist
        self.pf = pf
        sc.add(name, frames, frame_at=fa, motion=motion, z=z, wc=0.8)


def fam_draw(name, xr, yr, s=KS):
    def draw(key, f):
        pose, *opts = key.split(":")
        kw = dict(pose=pose)
        for o in opts:
            kw["expr"] = o
        if name.startswith("daughter_in_law"):
            return C.daughter_in_law(xr, yr, s, f, variant=int(name[-1]), **kw)
        return C.family_member(name, xr, yr, s, f, **kw)
    return draw


def animal_draw(kind, xr, yr, female=False, s=KS, shadow=180):
    def draw(key, f):
        pose, *opts = key.split(":")
        kw = dict(eyes=opts[0]) if opts else {}
        ph = 0.0
        if pose.startswith("hop"):
            ph = float(pose[3:])
            pose = "hop"
        return (C.ground_shadow(xr, yr + 2, s, shadow, 0.2) +
                PR.ark_animal(xr, yr, s, f, kind, pose, female, phase=ph, **kw))
    return draw


def bird_frames(color, x, y, s, f):
    return [doc(PR.songbird(x, y, s, f, wing=w, color=color)) for w in (1.0, 0.5, 0.0, -0.5, -1.0)]


def perched_bird(color, x, s=BIRD_S):
    return doc(PR.songbird(x, RIDGE_Y - 30 * s, s, 1 if x < 600 else -1, pose="perch", color=color))


# ---------------------------------------------------------------- end state helpers (used by s13 too)


def altar_frames():
    """0 empty, 1 a few stones, 2 more, 3 the altar heap (no fire), 4.. burning (flicker)."""
    x, y, s = ALTAR
    fr = [doc("")]
    st = [(-40, 0, 0), (0, 0, 1), (40, 0, 2), (-20, -24, 3), (22, -24, 4), (0, -46, 1)]
    fr.append(doc(S.g("".join(PR.stone(x + dx * s, y + dy * s, s * 1.6, seed=k) for dx, dy, k in st[:3]))))
    fr.append(doc(S.g("".join(PR.stone(x + dx * s, y + dy * s, s * 1.6, seed=k) for dx, dy, k in st))))
    fr.append(doc(PR.altar(x, y, s, fire=0.0, smoke=False)))
    for ph in (0.0, 0.33, 0.66):
        fr.append(doc(PR.altar(x, y, s, fire=1.0, phase=ph, smoke=True)))
    return fr


def flicker_fa(g):
    return lambda t: 4.0 + (int(g(t) / 0.13) % 3)


def turtle_state(g, idx):
    """The turtles crawl down the ramp on the film's clock (so s12 -> s13 matches): (x, y, frame 0/1/2=stand)."""
    g0 = TURTLE_G0[idx]
    speed = 26.0
    rest = TURTLE_REST[idx]
    tot, pf = pathf(exit_path(DOOR[0] - 70, rest))
    d = clamp((g - g0) * speed, 0, tot)
    x, y, f = pf(d)
    fr = 2 if d >= tot else int(d / 14) % 2
    return x, y, fr, d, tot


TURTLE_REST = [(872, 874), (806, 860)]
TURTLE_G0 = [0.0, 0.0]            # set from the timeline in build() (global seconds when each starts)


def turtle_layers(sc, g):
    for i, (xr, yr) in enumerate(TURTLE_REST):
        draw = animal_draw("turtle", xr, yr, female=(i == 1), shadow=110)
        frames = [doc(draw("walk_a", 1)), doc(draw("walk_b", 1)), doc(draw("stand", 1))]

        def fa(t, i=i):
            return float(turtle_state(g(t), i)[2])

        def mo(t, i=i, xr=xr, yr=yr):
            x, y, fr, d, tot = turtle_state(g(t), i)
            return Tf(dx=x - xr, dy=y - yr, alpha=1.0 if g(t) >= TURTLE_G0[i] else 0.0)
        sc.add(f"turtle{i}", frames, frame_at=fa, motion=mo, z=30 + yr / 100)


FAMILY_ORDER = ["noah", "noah_wife", "shem", "daughter_in_law0", "ham", "daughter_in_law1", "japheth",
                "daughter_in_law2"]


def fam_starts(ctx):
    """When each family member starts out of the door (scene seconds) — also used by s13 for the turtles."""
    t_joy = phrase_t(ctx.lines[2], "开心极了")
    tf0 = snap(t_joy - 0.1)
    return tf0, {nm: snap(tf0 + 0.3 * k + (0.45 if k > 0 else 0)) for k, nm in enumerate(FAMILY_ORDER)}


def set_turtle_starts(ctx12):
    _, f0 = fam_starts(ctx12)
    TURTLE_G0[0] = ctx12.start + snap(f0["daughter_in_law2"] + 0.8)
    TURTLE_G0[1] = ctx12.start + snap(f0["daughter_in_law2"] + 1.6)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]
    g = gtime(ctx)

    # ---------------------------------------------------------------- beats
    t_say = L0.start
    t_god = L1.start
    t_all = phrase_t(L1, "所有的动物")
    t_door = L2.start + 0.05
    t_one = L2.at("动物们一个接一个")
    t_jump = phrase_t(L2, "有的跳")
    t_fly = phrase_t(L2, "有的飞")
    t_run = phrase_t(L2, "有的跑")
    t_joy = phrase_t(L2, "开心极了")
    t_first = L3.start
    t_thank = L3.at("感谢上帝")

    # God's light: grows while God speaks, then settles at a warm base (same base as s13's start)
    def light_alpha(t):
        up = M.progress(t, t_say - 0.2, t_god + 0.6, "sine")
        down = M.progress(t, L1.end, L1.end + 1.5, "sine")
        pulse = 0.07 * math.sin(2 * math.pi * (t - t_god) / 1.7) * (M.progress(t, t_god, t_god + 0.5) -
                                                                      M.progress(t, L1.end - 0.3, L1.end))
        return 0.42 * up * (1 - down) + pulse
    add_world(sc, g, light_alpha)
    add_ground(sc, g)

    # ---------------------------------------------------------------- the ark: glow while God speaks, door opens,
    # then the high window opens for the birds
    t_win = snap(t_fly - 0.45)
    states = [(0, 0, 0), (0, 0, 0.5), (0, 0, 1.0), (0.25, 0, 1.0), (0.5, 0, 0.7), (0.75, 0, 0.4), (1, 0, 0.15),
              (1, 0, 0), (1, 0.5, 0), (1, 1, 0)]
    ark_frames = [ark_svg(d, w, gl) for d, w, gl in states]
    t_glow = snap(t_all - 0.2)

    def ark_fa(t):
        if t < t_glow:
            return 0.0
        if t < t_door:
            return min(2.0, (t - t_glow) / 0.5)
        if t < t_win:
            return 2.0 + min(5.0, float(int((t - t_door) / 0.11)))
        return 7.0 + min(2.0, float(int((t - t_win) / 0.12)))
    sc.add("ark", ark_frames, frame_at=ark_fa, seed=11)

    ag = S.rad_grad("s12ag", [(0, "#ffe7a0", 0.8), (0.5, "#f7cf78", 0.35), (1, "#f2c14e", 0)])
    sc.add("ark_glow", doc(f'<ellipse cx="{AX + 60}" cy="{AY - 300}" rx="760" ry="520" fill="url(#s12ag)"/>', ag),
           wc=0, blend="screen", z=19, motion=lambda t: Tf(alpha=0.55 * M.progress(t, t_god - 0.4, t_god + 0.8, "sine") *
                                                          (1 - M.progress(t, t_door, t_door + 1.6, "sine")) *
                                                          (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.7))))
    # birds peeking out of the small cabin windows on '所有的动物'
    peek = ""
    for i, (wbox, col) in enumerate(zip([PTS["windows"][k] for k in (0, 2, 4)], ("blue", "yellow", "red"))):
        cx = (wbox[0] + wbox[2]) / 2
        cy = (wbox[1] + wbox[3]) / 2 + 4
        peek += PR.in_ark_porthole(PR.songbird(cx, cy, 0.34, 1 if i % 2 else -1, pose="perch", color=col),
                                   (0, 2, 4)[i], AX, AY, KS, 1)
    sc.add("peek", doc(peek), wc=0.4, motion=M.combine(
        M.keys([(t_all - 0.1, {"alpha": 0, "dy": 14}), (t_all + 0.3, {"alpha": 1, "dy": 0}),
                (t_fly - 0.3, {"alpha": 1}), (t_fly, {"alpha": 0})], "sine"),
        lambda t: Tf(dy=2 * math.sin(2 * math.pi * t / 0.9))))


    # ---------------------------------------------------------------- animals come out one after another
    actors = {}
    door_in = DOOR[0]

    def A(name, kind, female, t0, speed, stride, walk=("walk_a", "walk_b"), front=150, **kw):
        xr, yr, fr = REST[name]
        draw = animal_draw(kind, xr, yr, female, shadow=kw.pop("shadow", 200))
        actors[name] = Actor(sc, g, name, draw, (xr, yr, fr), t0=t0, speed=speed, stride=stride, walk=walk,
                             x_in=door_in - front * KS, z=20 + yr / 100, **kw)
        return actors[name]

    te = snap(t_door + 0.42)
    A("elephant_m", "elephant", False, te, 240, 64, front=300,
      schedule=[(0, "stand"), (snap(t_joy + 0.1), "spray"), (snap(t_joy + 1.6), "trunk_up"),
                (snap(t_joy + 2.6), "stand")], shadow=380)
    A("elephant_f", "elephant", True, snap(te + 0.6), 240, 62, front=290,
      schedule=[(0, "stand"), (snap(t_joy + 0.9), "spray"), (snap(t_joy + 2.3), "stand")], shadow=360)
    tg = snap(max(t_one + 0.9, te + 1.5))
    A("giraffe_m", "giraffe", False, tg, 270, 66, front=340, pose_in="bow", inside_until=DOOR[2] + 80,
      schedule=[(0, "stand")], shadow=260)
    A("giraffe_f", "giraffe", True, snap(tg + 0.6), 270, 64, front=330, pose_in="bow",
      inside_until=DOOR[2] + 80, schedule=[(0, "stand")], shadow=250)
    hops = tuple(f"hop{p}" for p in (0.0, 0.25, 0.5, 0.75))
    tr = snap(t_jump - 0.35)
    A("rabbit_m", "rabbit", False, tr, 230, 17, walk=hops, front=70, schedule=[(0, "stand")], shadow=120)
    A("rabbit_f", "rabbit", True, snap(tr + 0.3), 230, 17, walk=hops, front=70, schedule=[(0, "stand")], shadow=120)
    th = snap(t_run - 0.3)
    for k, (nm, kind, fem) in enumerate((("horse_m", "horse", False), ("zebra_m", "zebra", False),
                                          ("horse_f", "horse", True), ("zebra_f", "zebra", True))):
        A(nm, kind, fem, snap(th + 0.24 * k), 470, 44, front=210, schedule=[(0, "stand")], shadow=260)
    tm = snap(t_joy - 0.55)
    for k, nm in enumerate(("monkey_m", "monkey_f")):
        A(nm, "monkey", k == 1, snap(tm + 0.25 * k), 300, 1e9, walk=("stand",), front=50,
          roll=lambda d: (d / 150.0 * 360.0) % 360.0,
          schedule=[(0, "stand"), (snap(t_first + 1.0 + 0.5 * k), "wave"), (snap(t_first + 2.6 + 0.5 * k), "stand")],
          shadow=110)

    # ---------------------------------------------------------------- the family: Noah first (cheers on the landing)
    order = FAMILY_ORDER
    tf0, fam_t0 = fam_starts(ctx)
    men = ["shem", "noah", "ham", "japheth"]
    # building beats: each man puts a stone on the heap after he arrives
    t_kneel = snap(t_thank + 0.05)
    for k, nm in enumerate(order):
        xr, yr, fr = REST[nm]
        sched = [(0, "stand:happy")]
        if nm in men:
            pass
        sched.append((snap(t_kneel + 0.07 * k), "kneel_pray"))
        pauses = [(RAMP_TOP[0] - (door_in - 60 * KS) - 10, 0.55, "cheer")] if nm == "noah" else []
        actors[nm] = Actor(sc, g, nm, fam_draw(nm, xr, yr), (xr, yr, fr), t0=fam_t0[nm], speed=280, stride=44,
                           walk=("walk_a:laugh", "walk_b:laugh"), x_in=door_in - 60 * KS, schedule=sched,
                           pauses=pauses, z=40 + yr / 100, breathe=(0.012, 2.6 + 0.2 * k, 0.13 * k),
                           keys_extra=[("release_dove", fr)])
    # the stone beats: when each man has arrived, a short 'put the stone down' pose, then happy
    arr = {nm: actors[nm].t_arr for nm in men}
    beats = []
    tb = max(arr["shem"] + 0.15, t_first + 1.2)
    for k, nm in enumerate(sorted(men, key=lambda n: arr[n])):
        tb = snap(max(tb, arr[nm] + 0.15))
        beats.append((nm, tb))
        tb += 0.55
    last_beat = beats[-1][1]
    if last_beat > t_kneel - 0.5:          # squeeze them in before the thanksgiving
        sp = (t_kneel - 0.55 - beats[0][1]) / max(1, len(beats) - 1)
        beats = [(nm, snap(beats[0][1] + sp * i)) for i, (nm, _) in enumerate(beats)]
    # rebuild the men's frame schedule with the beats (cuts layered over the actor's frame_at)
    for nm, tbk in beats:
        a = actors[nm]
        lay = next(L for L in sc.layers if L.name == nm)
        fr = REST[nm][2]
        ki_put = a.key_idx(("release_dove", fr))
        ki_st = a.key_idx(("stand:happy", fr))
        base = lay.frame_at
        t_put, t_back = tbk, snap(tbk + 0.45)

        def fa2(t, base=base, t_put=t_put, t_back=t_back, ki_put=ki_put, ki_st=ki_st):
            if t_put <= t < t_back:
                return float(ki_put)
            return base(t)
        lay.frame_at = fa2
        lay.motion = M.combine(lay.motion, dip(t_put, KS, REST[nm][:2], 5), dip(t_back, KS, REST[nm][:2], 4))

    # ---------------------------------------------------------------- the altar grows stone by stone, then burns
    alt = altar_frames()
    stage_t = [beats[0][1] + 0.12, beats[1][1] + 0.12, beats[3][1] + 0.12]
    t_fire = snap(t_thank - 0.05)

    def alt_fa(t):
        if t >= t_fire:
            return flicker_fa(g)(t)
        if t >= stage_t[2]:
            return 3.0
        if t >= stage_t[1]:
            return 2.0
        if t >= stage_t[0]:
            return 1.0
        return 0.0
    ax_, ay_ = ALTAR[:2]
    sc.add("altar", alt, frame_at=alt_fa, z=40 + ay_ / 100 - 0.005, wc=0.7,
           motion=M.combine(*[hop(ts, [(0, {"sy": 1.0}), (0.06, {"sy": 0.94}), (0.2, {"sy": 1.0})], (ax_, ay_))
                              for ts in stage_t]))
    fg = S.rad_grad("s12fg", [(0, "#ffd890", 0.9), (0.4, "#f6b860", 0.4), (1, "#f2c14e", 0)])
    sc.add("fire_glow", doc(f'<ellipse cx="{ax_}" cy="{ay_ - 90}" rx="430" ry="330" fill="url(#s12fg)"/>', fg), wc=0,
           blend="screen", z=60, motion=M.combine(
               M.keys([(t_fire, {"alpha": 0}), (t_fire + 0.8, {"alpha": 0.75})], "sine"),
               lambda t: Tf(alpha=0.88 + 0.12 * math.sin(2 * math.pi * g(t) / 0.7))))

    # ---------------------------------------------------------------- turtles: last, slowly down the ramp
    set_turtle_starts(ctx)
    turtle_layers(sc, g)

    # ---------------------------------------------------------------- the occluder (door jamb, hull, lintel)
    t_occ = snap(t_door + 0.6)
    occ = [occluder_svg(0.0), occluder_svg(0.5), occluder_svg(1.0)]
    sc.add("occluder", occ, z=55, seed=11, wc_edge=0.0,
           frame_at=lambda t: min(2.0, float(int(max(0.0, t - t_win) / 0.12))) if t >= t_win else 0.0,
           motion=lambda t: Tf(alpha=1.0 if t >= t_occ else 0.0))

    # ---------------------------------------------------------------- birds: out of the high window, circle, perch
    wx, wy = (WIN[0] + WIN[2]) / 2, (WIN[1] + WIN[3]) / 2
    for i, (px, col) in enumerate(BIRD_PERCH):
        t0 = snap(t_fly - 0.1 + 0.18 * i)
        dur = 3.4 + 0.5 * i
        t1 = t0 + dur
        ex, ey = px, RIDGE_Y - 30 * BIRD_S
        ang0 = 0.9 * i

        def pos(t, t0=t0, t1=t1, ex=ex, ey=ey, ang0=ang0, i=i):
            u = clamp((t - t0) / (t1 - t0))
            # out of the window, up and round a loop in the sky, then down onto the ridge
            cx_, cy_ = 620 + 260 * i, 170 + 30 * (i % 2)
            r = 150 + 30 * i
            a = ang0 + 2 * math.pi * 1.1 * u
            lx, ly = cx_ + r * math.cos(a), cy_ + 0.55 * r * math.sin(a)
            w_in = 1 - M.progress(u, 0, 0.25)
            w_out = M.progress(u, 0.72, 1.0, "inout")
            x = lx * (1 - w_in) + wx * w_in
            y = ly * (1 - w_in) + wy * w_in
            x = x * (1 - w_out) + ex * w_out
            y = y * (1 - w_out) + ey * w_out
            return x, y
        fl = {f: bird_frames(col, 300, 300, BIRD_S, f) for f in (-1, 1)}
        for f in (-1, 1):
            def bm(t, f=f, pos=pos, t0=t0, t1=t1):
                if t < t0 or t >= t1:
                    return Tf(alpha=0.0)
                x, y = pos(t)
                x2, _ = pos(t + 0.04)
                ff = 1 if x2 >= x else -1
                if ff != f:
                    return Tf(alpha=0.0)
                return Tf(dx=x - 300, dy=y - 300, alpha=M.progress(t, t0, t0 + 0.15))
            sc.add(f"bird{i}_{'l' if f < 0 else 'r'}", fl[f], z=70, wc=0.3, motion=bm,
                   frame_at=lambda t, t0=t0: float((0, 1, 2, 3, 4, 3, 2, 1)[int((t - t0) / 0.06) % 8]))
        sc.add(f"bird{i}_perch", perched_bird(col, px), z=70, wc=0.3, motion=M.combine(
            lambda t, t1=t1: Tf(alpha=1.0 if t >= t1 else 0.0),
            lambda t, px=px, i=i: Tf(rot=4 * max(0.0, math.sin(2 * math.pi * (g(t) / 2.3 + 0.27 * i))) ** 4,
                                     px=px, py=RIDGE_Y)))

    # ---------------------------------------------------------------- grass in front
    tuf = [tufts_svg(p) for p in (0.0, 0.25, 0.5, 0.75)]
    sc.add("tufts", tuf, z=90, frame_at=lambda t: float(round(1.5 + 1.5 * math.sin(2 * math.pi * g(t) / 2.8))))

    # ---------------------------------------------------------------- fx
    door_c = ((DOOR[0] + DOOR[2]) / 2, (DOOR[1] + DOOR[3]) / 2)
    cues = [(door_c[0] + dx, door_c[1] + dy, t_door + dt, 14) for dx, dy, dt in
            ((-40, -60, 0.1), (50, -20, 0.25), (-10, 40, 0.4))]
    cues += [(ax_ + dx, ay_ - 140 + dy, t_fire + dt, 16) for dx, dy, dt in ((-30, 0, 0.1), (40, -30, 0.35), (0, -70, 0.6))]
    sc.fx = [FX.sparkles((300, 120, 1100, 620), count=16, t0=t_god - 0.3, t1=L1.end + 0.8, size=(7, 15), drift=-10,
                         seed=31),
             stars_fx(cues, life=1.8),
             g_fx(FX.motes((0, 200, W, 900), count=24, color=(255, 240, 200), size=(3, 6), seed=17, alpha=110), g)]

    # ---------------------------------------------------------------- camera: on the ark while God speaks, then wide
    c_ark = Cam(800, 560, 1560)
    keys = [(0, c_ark), (t_door - 0.2, Cam(830, 570, 1600)), (t_jump + 0.4, Cam(1000, 600, 1900)),
            (t_joy + 0.4, Cam(1060, 610, 1960)), (t_first + 0.3, Cam(1060, 610, 1960)), (t_first + 2.6, END_CAM),
            (T, END_CAM)]
    sc.camera = M.cam_keys(keys, "sine")

    # ---------------------------------------------------------------- sound
    fix_seeds(sc)
    sc.sfx("birds", 0, dur=T + 0.1, gain_db=-22, fade_in=0.8, fade_out=0.9)
    sc.sfx("wind_soft", 0, dur=T + 0.1, gain_db=-24, fade_in=0.8, fade_out=0.9)
    sc.sfx("chime", t_god - 0.3, gain_db=-12)
    sc.sfx("ship_creak", t_door, dur=0.9, gain_db=-12, fade_out=0.3)
    sc.sfx("thud", t_door + 0.62, gain_db=-14)
    sc.sfx("footsteps", te, dur=2.4, gain_db=-14, pan=0.2, fade_out=0.6)
    sc.sfx("footsteps", tg, dur=2.0, gain_db=-17, pan=0.3, fade_out=0.6)
    sc.sfx("pop", tr + 0.3, gain_db=-16)
    sc.sfx("pop", tr + 0.6, gain_db=-17)
    sc.sfx("whoosh", t_fly - 0.05, gain_db=-14, pan=-0.3)
    sc.sfx("footsteps_run", th, dur=2.6, gain_db=-13, pan=0.4, fade_out=0.8)
    sc.sfx("splash_small", t_joy + 0.15, gain_db=-12, pan=0.4)
    sc.sfx("cheer", tf0 - 0.1, dur=3.0, gain_db=-14, fade_in=0.3, fade_out=1.2)
    for nm, tbk in beats:
        sc.sfx("thud", tbk + 0.1, gain_db=-14, pan=0.1)
    sc.sfx("fire", t_fire, dur=T - t_fire + 0.1, gain_db=-18, fade_in=0.4, fade_out=0.9)
    sc.sfx("chime", t_thank, gain_db=-12)
    return sc
