"""Scene 5 - Luke 19:4. '有了！' Zacchaeus runs ahead down the road to a big sycamore-fig on Jesus's way and climbs it,
branch by branch, then peeks out of the leaves: a perfect view of the road, where Jesus is coming at the head of the crowd.

One long picture-book panorama of a Jericho street (W5 x H5 stage, shared with s06_call and s07_grumble so the two plain
fades s05 -> s06 -> s07 match pixel for pixel: same stage, same layers and seeds, global-clock breathing, sway, clouds
and particles). Left to right: Zacchaeus's fine house (s07 only), the town street with the crowd lining the road (the
wall of backs on the near side), the sycamore-fig on the far lane (the climbing route on its left side, the sitting
branch over the road), the road on to the right where Jesus comes from.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's beat();
nothing hard-coded to the take). Times are for the current take:
  0 .. 0.9      calm page (the page-dip from s04 lands here): Zacchaeus behind the wall of backs, a fist at his chin
                (think), the crowd shuffling, the far side lining the road
  '有' 0.94     the idea: finger up, a glowing light bulb pops over his head (pop + sparkle, a little hop)
  '撒该往前跑' 1.96  the comic run: robe hitched up, legs churning, dust puffs, down the road ahead of the crowd; the
                camera runs with him (footsteps_run)
  '路上' 5.04   he screeches to a halt by the tree (leaning back, a dust cloud)
  '那里' 6.18   he looks up at it, wide-eyed; the camera pulls back and up: the big sycamore-fig; '大大' 7.33 he spreads
                his arms ('so big!')
  '树枝' 9.00   he points up at the low branches; '低' 9.68 / '粗' 10.24 a soft golden glow runs along the low, thick limbs
  '正好可以爬' 10.78  a determined nod, three quick steps to the trunk; '爬' 11.67 hands on the fork (climb_a)
  '爬呀爬，爬呀爬，爬上了' 13.19 / 13.74 / 14.29 / 14.87 / 15.43  one climbing stage on every 爬 (a foot on the knob, a
                knee onto the low branch, standing on it, a foot on the stub, then the hoist onto the sitting branch); each
                stage holds ~0.35 s with an eased 0.2 s pull between them; the camera climbs with him
  '桑树' 16.07  he scoots along the branch to the sitting spot and settles, overjoyed
  '嘿嘿' 17.44  he leans out and pushes a twig of leaves aside: a big grin (two giggle bobs, a leaf flutters down)
  '这下看得清清楚楚了' 18.18  the camera glides right along his view: the road, the people lining it, and Jesus walking
                towards the tree at the head of the crowd with two disciples and the townsfolk behind him
  end           calm: the camera holds (CAM_HANDOFF); the last second is s06_call's first second

Shared with s06 / s07: the stage constants, add_world(), the Fig flipbook figure, the drawing helpers zac_svg /
jes_svg / folk_svg / disc_svg, the near-tree crowd (tree_crowd_markup) and the procession (procession()).
"""
import math
import random

from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.loader import context
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import beat
from stories.noah.scenes.s01_title import snap

INK = P["ink"]

# ================================================================== the place (one stage for s05, s06, s07)
W5, H5 = 5600, 1300
K = 0.8                                   # people and the tree (sycomore_points needs the same scale)
TIME = 0.15                               # warm afternoon
YR, ROAD_W = 990, 260                     # the road's centre line and width (x scale)
_STP = PR.jericho_street_points(0, W5, YR, K, ROAD_W)
YF, YN = _STP["far_edge"], _STP["near_edge"]      # 886 / 1094
HB = YF - 40 * K                          # the far-side house walls stand here
XT, YT = 3700, 955                        # the sycamore-fig: the foot of its trunk (on the far lane of the road)
SP = PR.sycomore_points(XT, YT, K, 1)
XU, YU = SP["under"]                      # where Jesus stops and looks up (3868, 955)
CY, CK = YF - 6, K * 0.9                  # the people lining the far edge (smaller: further away)
HOUSE_X, HOUSE_Y = 700, YF + 6            # Zacchaeus's house (s07)
SUN = (4950, 230)
G_REF = 94.0                              # global-clock reference for the drifting clouds
CAM_HANDOFF = Cam(4170, 612, 1780)        # s05's last camera = s06's first
ZREF = (SP["climb"][0]["anchor"][0], YT)   # Zacchaeus's drawing anchor in s05-s07 (the same raster in all three)

# z order
Z_SKY, Z_CLOUD, Z_FAR, Z_TOWN, Z_PALM, Z_HOUSE = 0, 1, 2, 3, 3.5, 3.8
Z_FARCROWD, Z_ROAD, Z_CANOPY, Z_TRUNK = 4, 5, 6, 7
Z_WALL, Z_FOLLOW, Z_ZAC, Z_FRONT, Z_TWIG = 8, 8.5, 9, 10, 10.5
Z_DISC, Z_JESUS, Z_FX, Z_FG = 11, 12, 13, 14


def doc(body, defs=""):
    return S.svg_doc(body, defs, W5, H5)


def f1(v):
    return f"{v:.1f}"


def clamp01(v):
    return 0.0 if v < 0 else 1.0 if v > 1 else v


def env(t, t0, t1, fin=0.4, fout=0.4):
    """0 -> 1 -> 0 envelope."""
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def gfx(make, g0, t0=-1e4, t1=1e9, **kw):
    """An engine.fx effect on the film's global clock (identical in two scenes joined by a plain fade)."""
    inner = make(t0=t0 + g0, t1=t1 + g0 if t1 < 1e8 else 1e9, **kw)
    return lambda frame, t, view: inner(frame, t + g0, view)


def clamp_cam(c):
    cw = min(c.w, W5, H5 * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), W5 - cw / 2 - 1), min(max(c.y, ch / 2 + 1), H5 - ch / 2 - 1), cw, c.rot)


def cam_path(keys, curves):
    f = M.cam_keys([(t, clamp_cam(c)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t))


# ================================================================== the track and the flipbook figure
class Track:
    """Anchor position over time: holds, eased moves, hop arcs and paths. pos(t) -> (x, y)."""

    def __init__(self, x, y):
        self.moves = []
        self.cur = (x, y)
        self.x0, self.y0 = x, y

    def to(self, t0, t1, x, y, lift=0.0, curve="sine"):
        self.moves.append(("lin", t0, t1, self.cur, (x, y), lift, curve))
        self.cur = (x, y)
        return self

    def along(self, t0, t1, pts, speed):
        """Move along the polyline pts (starting at the current point) between t0 and t1; speed(u) -> 0..1 progress."""
        pts = [self.cur] + list(pts)
        cum = [0.0]
        for a, b in zip(pts, pts[1:]):
            cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        self.moves.append(("path", t0, t1, pts, cum, speed))
        self.cur = pts[-1]
        return self

    def __call__(self, t):
        x, y = self.x0, self.y0
        for mv in self.moves:
            t0, t1 = mv[1], mv[2]
            if t < t0:
                break
            if mv[0] == "lin":
                _, _, _, a, b, lift, curve = mv
                if t >= t1:
                    x, y = b
                    continue
                u = M.progress(t, t0, t1, curve)
                v = (t - t0) / max(1e-6, t1 - t0)
                return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - lift * math.sin(math.pi * v)
            _, _, _, pts, cum, speed = mv
            if t >= t1:
                x, y = pts[-1]
                continue
            s = speed((t - t0) / max(1e-6, t1 - t0)) * cum[-1]
            for i in range(len(pts) - 1):
                if cum[i + 1] >= s:
                    u = (s - cum[i]) / max(1e-6, cum[i + 1] - cum[i])
                    return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u
            return pts[-1]
        return x, y


def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def bump(t0, s, piv, height=14.0, dur=0.26):
    """A little hop / bob up whose take-off is at t0."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf()
        v = u / dur
        return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.02 * math.sin(math.pi * v), px=piv[0], py=piv[1])
    return m


def breath(piv, g0, period=3.0, amount=0.011, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start), so neighbouring scenes breathe in step."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


class Fig:
    """One figure on its own flipbook layer. States are hashable keys drawn by draw(key[, i]) at the reference anchor
    ``ref``; cut() switches with a hard cut (hidden in a squash dip unless dip=False); the Track moves the drawing;
    loops[key] = (n, period) cycles sub-frames draw(key, i) on the film's global clock; mots are extra motions (pivot
    = the moving anchor)."""

    def __init__(self, name, draw, ref, z, g0, seed=0, loops=None, wc=1.0, k=K):
        self.name, self.draw, self.ref, self.z, self.g0, self.seed, self.wc, self.k = name, draw, ref, z, g0, seed, wc, k
        self.loops = loops or {}
        self.ents, self.dips, self.mots, self.amots = [], [], [], []
        self.track = Track(*ref)
        self.alpha = None

    def cut(self, t, key, dip=True, depth=7.0):
        t = snap(t) if t > 0 else -1e4
        self.ents = [e for e in self.ents if e[0] != t]
        self.ents.append((t, key))
        if dip and t > 0:
            self.dips.append((t, depth))
        return self

    def key_at(self, t):
        cur = None
        for tk, n in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = n
        return cur

    def blinks(self, pairs, t_from, t_to, rng, every=(2.3, 4.0), avoid=()):
        """pairs(key) -> closed-eye key or None; no blink within 0.35 s of another cut or inside an avoid window."""
        t = t_from + rng.uniform(0.3, 1.2)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.25:
            cur = self.key_at(t)
            bk = pairs(cur) if cur is not None else None
            if bk and all(abs(t - tk) > 0.35 for tk in cut_ts) and not any(a - 0.2 <= t <= b for a, b in avoid):
                self.ents += [(snap(t), bk), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def pos(self, t):
        return self.track(t)

    def motion(self):
        px, py = self.ref
        tr = self.track

        def base(t):
            x, y = tr(t)
            return Tf(dx=x - px, dy=y - py, px=px, py=py)
        mots = [base] + [squash(td, self.k, self.ref, depth) for td, depth in self.dips] + self.mots
        al = self.alpha
        if al is not None:
            mots.append(lambda t: Tf(alpha=al(t)))
        return M.combine(*mots)

    def build(self, sc, blend="normal"):
        ents = sorted(self.ents, key=lambda e: e[0])
        names = []
        for _, n in ents:
            if n not in names:
                names.append(n)
        frames, index = [], {}
        for n in names:
            nl, _ = self.loops.get(n, (1, 1.0))
            for i in range(nl):
                index[(n, i)] = len(frames)
                frames.append(doc(self.draw(n, i) if n in self.loops else self.draw(n)))
        g0, loops = self.g0, self.loops

        def fa(t):
            cur = ents[0][1]
            for tk, n in ents:
                if t >= tk:
                    cur = n
            if cur in loops:
                nl, per = loops[cur]
                return float(index[(cur, int(math.floor((t + g0) / per)) % nl)])
            return float(index[(cur, 0)])
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=self.wc, motion=self.motion(), blend=blend)
        return self


# ================================================================== people (drawing helpers with small overrides)
def blink_expr(e):
    """A closed-eye variant of expression e (registered once in characters.EXPRS)."""
    name = f"zq_blink_{e}"
    if name not in C.EXPRS and e in C.EXPRS:
        C.EXPRS[name] = dict(C.EXPRS[e], eyes="closed")
    return name


def _apply(ps, mod):
    ps = dict(ps)
    if not mod:
        return ps
    for k_, v in mod.items():
        if k_ in ("h", "t"):
            ps[k_] = ps.get(k_, 0) + v
        else:
            ps[k_] = v
    return ps


# Zacchaeus: named pose modifications (base pose, overrides)
ZMODS = {
    "look_up": dict(h=-26, look=(0.03, -0.12)),                                          # stand: looking up at the tree
    "big": dict(h=-20, arms=(("fk", 104, 124), ("fk", -104, -126)), hands=("open", "open"), look=(0.03, -0.10)),
    "point_up": dict(h=-22, arms=(("fk", 128, 150), ("ik", "torso", 0.30, 0.04, -1)), hands=("point", "fist"),
                     look=(0.03, -0.12)),
    "nod": dict(h=12, arms=(("ik", "torso", 0.95, 0.04, -1), ("ik", "torso", 0.95, 0.04, -1))),
    "heart": dict(h=-6, arms=(("ik", "torso", 0.62, 0.70, 1), ("ik", "torso", 0.52, 0.76, 1)), hands=("open", "open")),
    "self": dict(h=10, look=(0.03, 0.09), arms=(("ik", "body", 40, 12, 1), ("ik", "torso", 0.36, 0.70, 1)),
                 hands=("fist", "point")),
    "sit_cheer": dict(h=-10, arms=(("fk", 130, 152), ("fk", -134, -156)), hands=("open", "open")),
    "sit_up": dict(h=-8, look=(0.03, 0.02)),
    "sit_down": dict(h=18, t=6, look=(0.03, 0.10)),
    "back_look": dict(h=4),
    "glance": dict(h=-4, look=(0.04, -0.02)),
    "up_to": dict(h=-16, look=(0.03, -0.10)),
    "push": dict(h=-4, arms=(("fk", 70, 82), ("fk", 40, 60)), hands=("palm", "open")),
}


def zk(pose, f=1, expr=None, phase=0.0, mod=None, marks=True):
    """Hashable key of a Zacchaeus drawing."""
    return ("Z", pose, f, expr, round(phase, 3), mod, marks)


def zac_svg(x, y, k, key):
    _, pose, f, expr, phase, mod, marks = key
    ps, pk = C._zac_pose(pose, phase)
    ps = _apply(ps, ZMODS.get(mod))
    D = C._zac_design(pk, lap=bool(ps["lap"]), purse=True)
    fronts = []
    if marks:
        fronts.append(C._zac_marks(pk, phase))
    D["front"] = C._hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, C._ZAC_M, ps, e, C._fsign(f), marks)
    if pk in C.ZAC_SEAT_POSES:
        sx, sy = C._seat_point(C._ZAC_M)
        inner = C._reanchor(inner, sx, sy)
    elif pk == "climb_down":
        h0, h1 = C._LAST["hands"]
        inner = C._reanchor(inner, (h0[0] + h1[0]) / 2, (h0[1] + h1[1]) / 2)
    return C._wrap_out(inner, x, y, k, f, f"zq-zac-{pk}-{mod}")


def zac_blink(key):
    if key is None or key[0] != "Z":
        return None
    _, pose, f, expr, phase, mod, marks = key
    ps, _ = C._zac_pose(pose, phase)
    e = expr or ps["expr"]
    if C.EXPRS.get(e, {}).get("eyes") in ("closed", "arc"):
        return None
    return ("Z", pose, f, blink_expr(e), phase, mod, marks)


JMODS = {
    "down": dict(h=14, look=(0.03, 0.08)),             # looking down at Zacchaeus beside him
    "down_more": dict(h=20, look=(0.02, 0.10)),
    "nod": dict(h=10),
}


def jk(pose, f=-1, expr=None, mod=None, phase=0.0, arms=None):
    return ("J", pose, f, expr, mod, round(phase, 3), arms)


def jes_svg(x, y, k, key):
    _, pose, f, expr, mod, phase, arms = key
    if pose in C.JESUS_ZACCHAEUS_POSES:
        ps = dict(C._JZ_ZAC[pose])
    elif pose in C.JESUS_POSES:
        ps = dict(C._jesus_pose(pose, phase))
    else:
        return C.jesus(x, y, k, f, pose=pose, expr=expr)
    ps = _apply(ps, JMODS.get(mod))
    if arms is not None:
        ps["arms"] = arms[0]
        ps["hands"] = arms[1]
    D = C._jesus_design(pose, 0.0, True, 0.0, True)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, C._JESUS_M, ps, e, C._fsign(f), True)
    return C._wrap_out(inner, x, y, k, f, f"zq-jesus-{pose}-{mod}")


def jes_blink(key):
    if key is None or key[0] != "J":
        return None
    _, pose, f, expr, mod, phase, arms = key
    if pose in C.JESUS_ZACCHAEUS_POSES:
        e = expr or C._JZ_ZAC[pose]["expr"]
    elif pose in C.JESUS_POSES:
        e = expr or C._jesus_pose(pose, phase)["expr"]
    else:
        return None
    if C.EXPRS.get(e, {}).get("eyes") in ("closed", "arc"):
        return None
    return ("J", pose, f, blink_expr(e), mod, phase, arms)


def dk(variant, pose, f=-1, expr=None, phase=0.0):
    return ("D", variant, pose, f, expr, round(phase, 3))


def disc_svg(x, y, k, key):
    _, v, pose, f, expr, phase = key
    return C.disciples(x, y, k, f, variant=v, pose=pose, expr=expr, phase=phase)


FMODS = {
    "up": dict(h=-22, look=(0.03, -0.12)),                                          # looking up at the tree
    "up_point": dict(h=-22, arms=(("fk", 14, 8), ("fk", 132, 140)), hands=("fist", "point"), look=(0.03, -0.12)),
    "up_hands": dict(h=-20, arms=(("ik", "head", 0.55, 0.72, 1), ("ik", "head", 0.70, 0.66, 1)), hands=("open", "open"),
                     look=(0.03, -0.11)),                                         # hands to the cheeks: a gasp
    "turn": dict(h=2, look=(0.05, 0.0)),
}


def fk(kind, v, pose, f=1, expr=None, phase=0.0, mod=None, item=None):
    return ("F", kind, v, pose, f, expr, round(phase, 3), mod, item)


def folk_svg(x, y, k, key):
    """characters.jericho_folk with an optional pose modification (FMODS)."""
    _, kind, v, pose, f, expr, phase, mod, item = key
    if not mod:
        return C.jericho_folk(x, y, k, f, kind=kind, variant=v, pose=pose, expr=expr, phase=phase, item=item)
    ps = C._jr_pose(pose, phase, back_v=v + (2 if kind == "woman" else 0))
    D, m, c = C._jr_design(kind, int(v), False)
    if item is None:
        item = {"fruit_seller": "dates", "farmer": "hoe"}.get(kind)
    fronts = [C._jr_items(D, pose, item if "arms" not in FMODS[mod] else None, phase, True)]
    if kind == "elder" and pose in ("stand", "walk_a", "walk_b", "frown", "look", "smile"):
        ps["t"] = ps["t"] + 7
    ps = _apply(ps, FMODS[mod])
    D["front"] = C._hooks(*fronts)
    e = expr or ps["expr"]
    if kind in ("woman", "child") and e in ("cross", "grumble", "mutter") and expr is None:
        e = {"cross": "worried", "grumble": "cross", "mutter": "mutter"}[e]
    inner, _ = C._figure(D, m, ps, e, C._fsign(f), True)
    return C._wrap_out(inner, x, y, k, f, f"zq-folk-{kind}{int(v) % 6}-{pose}-{mod}")


def draw_key(key, x, y, k):
    """Dispatch any person key."""
    if key[0] == "Z":
        return zac_svg(x, y, k, key)
    if key[0] == "J":
        return jes_svg(x, y, k, key)
    if key[0] == "D":
        return disc_svg(x, y, k, key)
    if key[0] == "F":
        return folk_svg(x, y, k, key)
    raise ValueError(key)


# ================================================================== the world
def _palm_spots():
    """Swaying date palms (each its own little flipbook): (x, y, scale, height, seed)."""
    return [(2010, HB + 4, K * 0.80, 1.0, 11), (3060, HB + 4, K * 0.86, 1.08, 12), (4330, HB + 4, K * 0.84, 1.05, 13),
            (5090, HB + 4, K * 0.80, 1.0, 14), (1290, HB + 4, K * 0.82, 1.02, 15)]


def _far_svg():
    pal = PR._jr_pal(TIME)
    out = PR._jr_far(-40, W5 + 40, YF - 300 * K, K, TIME, seed=4)
    rng = random.Random(5)
    for i in range(int(W5 / (300 * K)) + 2):
        px = (i + 0.6) * 300 * K + rng.uniform(-60, 60) * K
        out += PR._place(PR._jr_palm(rng.uniform(0.75, 0.95), rng.uniform(-0.2, 0.2), 0.0, False, TIME, 50 + i, far=True),
                         px, HB - 120 * K, K * 0.62, 1, filt=None)
    out += (f'<path d="M-40,{f1(HB - 60 * K)} L{W5 + 40},{f1(HB - 60 * K)} L{W5 + 40},{f1(YF + 4)} L-40,{f1(YF + 4)} Z" '
            f'fill="{pal["sand"]}"/>')
    return doc(S.g(out, filter="wobble-fine"))


def _garden_wall(x0, x1, y, h=70):
    """A low mud-brick garden wall with a rounded coping (local stage px)."""
    pal = PR._jr_pal(TIME)
    col = S.mix(pal["stone"], pal["sand_dk"], 0.25)
    hk = h * K
    out = (f'<path d="M{f1(x0)},{f1(y)} L{f1(x0)},{f1(y - hk)} Q{f1(x0 + 6)},{f1(y - hk - 10 * K)} '
           f'{f1(x0 + 20)},{f1(y - hk - 10 * K)} '
           f'L{f1(x1 - 20)},{f1(y - hk - 10 * K)} Q{f1(x1 - 6)},{f1(y - hk - 10 * K)} {f1(x1)},{f1(y - hk)} L{f1(x1)},{f1(y)} Z" '
           f'fill="{col}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>')
    rng = random.Random(int(x0))
    for row in range(3):
        yy = y - hk * (row + 0.5) / 3
        xx = x0 + (row % 2) * 30 * K
        while xx < x1 - 30:
            w = rng.uniform(46, 66) * K
            out += (f'<rect x="{f1(xx + 4)}" y="{f1(yy - 8 * K)}" width="{f1(w - 8)}" height="{f1(15 * K)}" rx="4" '
                    f'fill="{S.shade(col, rng.choice((-0.07, 0.06, 0.0)))}" opacity="0.8"/>')
            xx += w
    out += (f'<path d="M{f1(x0 + 10)},{f1(y - hk - 4 * K)} L{f1(x1 - 10)},{f1(y - hk - 4 * K)}" stroke="{S.shade(col, 0.3)}" '
            f'stroke-width="{f1(6 * K)}" stroke-linecap="round" opacity="0.7"/>')
    return out


def _town_svg():
    """Houses, stalls, garden walls, balsam bushes and static palms along the far side of the road."""
    pal = PR._jr_pal(TIME)
    out = ""
    # the town street (behind the crowd)
    for i, (hx, v, f) in enumerate(((1480, 1, -1), (1860, 2, 1), (2240, 0, -1), (2620, 3, 1), (2930, 1, -1))):
        out += PR.jericho_house(hx, HB, K * (0.95 + 0.04 * (i % 2)), f, variant=v, time=TIME, seed=i)
    out += PR.date_palm(2430, HB + 4, K * 0.76, 1, height=0.96, time=TIME, seed=21)
    out += PR.date_palm(1680, HB + 4, K * 0.74, -1, height=0.94, time=TIME, seed=22)
    for k_, (sx, f) in enumerate(((1660, 1), (2430, -1), (2780, 1))):
        out += PR.market_stall(sx, YF - 6 * K, K * 0.82, f, time=TIME, seed=k_)
    # at the sycamore: a low garden wall with balsam bushes and a gate post, palms behind
    out += S.g(_garden_wall(3140, 4420, HB + 24), filter="wobble-fine")
    for k_, bx in enumerate((3220, 3420, 3990, 4180, 4370)):
        out += PR.balsam_bush(bx, HB + 26, K * 0.9, 1 if k_ % 2 else -1, time=TIME, seed=k_)
    # on towards the right (where Jesus comes from)
    out += PR.jericho_house(4640, HB, K * 0.95, -1, variant=2, time=TIME, seed=7)
    out += PR.market_stall(4940, YF - 6 * K, K * 0.82, -1, time=TIME, seed=4, goods="dates")
    out += PR.jericho_house(5420, HB, K * 0.97, 1, variant=3, time=TIME, seed=8)
    # beyond Zacchaeus's house (left)
    out += S.g(_garden_wall(-30, 250, HB + 30, 80) + _garden_wall(1150, 1330, HB + 30, 80), filter="wobble-fine")
    return doc(out)


def _road_svg():
    out = PR.jericho_street(0, W5, YR, K, part="road", time=TIME, road_w=ROAD_W, bottom=H5 + 30)
    pal = PR._jr_pal(TIME)
    rng = random.Random(77)
    extra = ""
    # a few stones and footprints on the road, dry tufts and pebbles along the near verge
    for _ in range(46):
        px, py = rng.uniform(0, W5), rng.uniform(YN + 20, H5 - 10)
        extra += PR._jr_tuft(px, py, K * rng.uniform(0.9, 1.3), TIME, rng.randrange(9))
    for _ in range(30):
        px, py = rng.uniform(0, W5), rng.uniform(YF + 30, YN - 20)
        extra += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(rng.uniform(6, 11))}" ry="{f1(rng.uniform(3, 5))}" '
                  f'fill="{S.shade(pal["sand"], -0.12)}" opacity="0.55"/>')
    out += S.g(extra, filter="wobble-fine")
    # near-verge props (framing the bottom of the frame)
    out += PR.balsam_bush(3060, H5 - 22, K * 1.15, 1, time=TIME, seed=31)
    out += PR.balsam_bush(4720, H5 - 16, K * 1.1, -1, time=TIME, seed=32)
    out += PR.balsam_bush(1560, H5 - 18, K * 1.12, 1, time=TIME, seed=33)
    out += PR.balsam_bush(5330, H5 - 26, K * 1.0, 1, time=TIME, seed=34)
    out += PR._place(PR._date_basket(), 2860, H5 - 34, K * 1.15, 1)
    out += PR._place(PR._date_basket(), 4300, H5 - 26, K * 1.05, -1)
    return doc(out)


def _clouds_svg():
    pal = PR._jr_pal(TIME)
    rng = random.Random(21)
    out = ""
    for i in range(12):
        cx = -300 + i * 560 + rng.uniform(-120, 120)
        cy = rng.uniform(90, 300)
        out += PR._jr_wisp(cx, cy, rng.uniform(300, 460) * K, rng.uniform(26, 38) * K, pal["cloud"], pal["cloud_sh"], 30 + i)
    return doc(out)


def tree_canopy_trunk(sway):
    full = PR._sycomore("back", sway, TIME, True, 0)
    canopy = PR._syco_canopy(TIME, sway, 0, "back")
    if not full.startswith(canopy):                      # (the library draws the crown first; keep it all if not)
        return full, ""
    return PR._place(canopy, XT, YT, K, 1), PR._place(full[len(canopy):], XT, YT, K, 1)


SWAY = (-0.5, 0.0, 0.5)              # the crown (crossfaded on the global clock)
SWAY_FRONT = (-0.32, 0.0, 0.32)      # the leaf sprays in front
SWAY_PALM = (-0.28, 0.0, 0.28)       # the date palms


def sway_fa(g0, period=3.7, phase=0.0):
    return lambda t: 1.0 + math.sin(2 * math.pi * ((t + g0) / period + phase))


def add_world(sc, g0, house_door=None, branch_glow=None, leaf_shake=None):
    """The shared panorama. house_door: None (gate closed, static) or (doors, frame_at) for s07. branch_glow: optional
    alpha function for the golden glow along the low limbs (s05). leaf_shake: optional t -> dx (px) rustling the crown
    and the leaf sprays (s06)."""
    sc.add("w_sky", doc(PR.jericho_sky(0, 0, W5, YF + 10, TIME, sun=SUN, clouds=0.0, birds=0, seed=3, scale=K)), z=Z_SKY,
           seed=101)
    sc.add("w_clouds", _clouds_svg(), z=Z_CLOUD, seed=103, wc=0.6,
           motion=lambda t: Tf(dx=4.0 * (t + g0 - G_REF)))
    sc.add("w_far", _far_svg(), z=Z_FAR, seed=107)
    sc.add("w_town", _town_svg(), z=Z_TOWN, seed=109)
    for i, (px, py, pk, hh, sd) in enumerate(_palm_spots()):
        frames = [doc(PR.date_palm(px, py, pk, 1, height=hh, sway=s_, time=TIME, seed=sd)) for s_ in SWAY_PALM]
        sc.add(f"w_palm{i}", frames, z=Z_PALM, seed=113 + i, frame_at=sway_fa(g0, 4.3 + 0.4 * i, 0.21 * i))
    if house_door is None:
        sc.add("w_house", doc(PR.zacchaeus_house(HOUSE_X, HOUSE_Y, K, 1, view="exterior", time=TIME, door=0.0)), z=Z_HOUSE,
               seed=127)
    else:
        doors, fa = house_door
        sc.add("w_house", [doc(PR.zacchaeus_house(HOUSE_X, HOUSE_Y, K, 1, view="exterior", time=TIME, door=d)) for d in doors],
               z=Z_HOUSE, seed=127, frame_at=fa)
    sc.add("w_road", _road_svg(), z=Z_ROAD, seed=131)
    canopies, trunk = [], ""
    for s_ in SWAY:
        cnp, tr = tree_canopy_trunk(s_)
        canopies.append(doc(cnp))
        if s_ == 0.0:
            trunk = tr
    lm = (lambda t: Tf(dx=leaf_shake(t))) if leaf_shake is not None else None
    sc.add("w_canopy", canopies, z=Z_CANOPY, seed=137, frame_at=sway_fa(g0, 3.7), motion=lm)
    if trunk:
        sc.add("w_trunk", doc(trunk), z=Z_TRUNK, seed=139)
    if branch_glow is not None:
        sc.add("w_glow", doc(_branch_glow_svg(), _GLOW_DEFS), z=Z_TRUNK + 0.1, wc=0, blend="screen",
               motion=lambda t: Tf(alpha=branch_glow(t)))
    fronts = [doc(PR.sycomore(XT, YT, K, 1, part="front", sway=s_, time=TIME)) for s_ in SWAY_FRONT]
    lm2 = (lambda t: Tf(dx=1.4 * leaf_shake(t + 0.03))) if leaf_shake is not None else None
    sc.add("w_front", fronts, z=Z_FRONT, seed=149, frame_at=sway_fa(g0, 3.3, 0.37), motion=lm2)


_GLOW_DEFS = ('<filter id="zqglow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>')


def _branch_glow_svg():
    """A soft golden glow along the low, thick limbs and the knob (the climbing route)."""
    P_ = lambda lx, ly: PR.local_to_stage(XT, YT, K, 1, lx, ly)  # noqa: E731
    out = ""
    for pts, w in ((PR._SYCO_L1[:4], 46), (PR._SYCO_R1[:4], 46), (PR._SYCO_L2[:3], 40), (PR._SYCO_L0[:2], 52)):
        sp = [P_(*p) for p in pts]
        d = S.smooth_path(sp, closed=False)
        out += f'<path d="{d}" fill="none" stroke="#ffe7a0" stroke-width="{f1(w * K)}" stroke-linecap="round" opacity="0.75"/>'
    kx, ky = P_(-80, -62)
    out += f'<circle cx="{f1(kx)}" cy="{f1(ky)}" r="{f1(26 * K)}" fill="#ffe7a0" opacity="0.8"/>'
    return f'<g filter="url(#zqglow)">{out}</g>'


# ================================================================== ambient life (global clock)
class Swifts:
    """Little swifts gliding across the sky in loose pairs (output space, stage coords, global clock)."""

    def __init__(self, g0, n=7, seed=3, y=(120, 420)):
        rng = random.Random(seed)
        self.g0 = g0
        self.b = [(rng.uniform(0, W5), rng.uniform(*y), rng.uniform(40, 75) * rng.choice((-1, 1)), rng.uniform(0, 6.28),
                   rng.uniform(0.8, 1.15)) for _ in range(n)]

    def __call__(self, frame, t, view):
        g = t + self.g0
        ov = None
        for x0, y0, v, ph, s in self.b:
            x = (x0 + v * (g - G_REF)) % (W5 + 400) - 200
            y = y0 + 22 * math.sin(g * 0.6 + ph)
            ox, oy = view.to_out(x, y)
            if not (-40 < ox < frame.size[0] + 40 and -40 < oy < frame.size[1] * 0.6):
                continue
            if ov is None:
                ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(ov)
            r = 13 * s * view.scale
            flap = 0.5 + 0.5 * math.sin(g * 9 + ph * 3)
            wy = r * (0.25 + 0.35 * flap)
            sg = 1 if v > 0 else -1
            pts = [(ox - r, oy - wy), (ox - r * 0.4, oy - wy * 0.4), (ox, oy), (ox + r * 0.4, oy - wy * 0.4), (ox + r, oy - wy)]
            d.line(pts, fill=(92, 74, 66, 200), width=max(2, int(2.6 * view.scale)), joint="curve")
            d.ellipse([ox - 2.5 + sg, oy - 2, ox + 2.5 + sg, oy + 2.5], fill=(92, 74, 66, 200))
        if ov is not None:
            frame.alpha_composite(ov)
        return frame


class LeafFall:
    """Heart-shaped sycamore-fig leaves fluttering down from points (output space, stage coords). drops: list of
    (t0, x, y, n, spread) - each releases n leaves at t0."""

    def __init__(self, drops, seed=5, fall=150.0, life=2.6, ground=YT):
        rng = random.Random(seed)
        self.leaves = []
        for t0, x, y, n, spread in drops:
            for _ in range(n):
                self.leaves.append((t0 + rng.uniform(0, 0.25), x + rng.uniform(-spread, spread),
                                    y + rng.uniform(-spread * 0.4, spread * 0.4),
                                    rng.uniform(0.75, 1.2) * fall, rng.uniform(0, 6.28), rng.uniform(0.8, 1.2),
                                    rng.choice(((122, 168, 82), (95, 154, 72), (140, 191, 90))), rng.uniform(-60, 60)))
        self.life, self.ground = life, ground

    def __call__(self, frame, t, view):
        ov = None
        for t0, x, y, v, ph, s, col, vx in self.leaves:
            u = t - t0
            if u < 0 or u > self.life:
                continue
            yy = y + v * u + 18 * u * u
            if yy > self.ground + 10:
                continue
            xx = x + vx * u + 26 * math.sin(u * 3.1 + ph)
            a = 1.0 - max(0.0, (u - self.life * 0.7) / (self.life * 0.3))
            ox, oy = view.to_out(xx, yy)
            if not (-30 < ox < frame.size[0] + 30 and -30 < oy < frame.size[1] + 30):
                continue
            if ov is None:
                ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(ov)
            r = 15 * s * view.scale * K
            rot = u * 4.2 + ph
            flat = 0.35 + 0.65 * abs(math.cos(u * 3.3 + ph))
            pts = []
            for i in range(10):
                ang = 2 * math.pi * i / 10
                rr = r * (1.0 if i != 0 else 1.25) * (0.85 + 0.15 * math.cos(2 * ang))
                px_, py_ = rr * math.cos(ang) * flat, rr * math.sin(ang) * 0.75
                pts.append((ox + px_ * math.cos(rot) - py_ * math.sin(rot), oy + px_ * math.sin(rot) + py_ * math.cos(rot)))
            d.polygon(pts, fill=(*col, int(240 * a)), outline=(75, 52, 38, int(235 * a)), width=max(1, int(2 * view.scale)))
            d.line([((pts[0][0] + pts[5][0]) / 2, (pts[0][1] + pts[5][1]) / 2), pts[0]], fill=(75, 52, 38, int(160 * a)), width=1)
        if ov is not None:
            frame.alpha_composite(ov)
        return frame


def add_ambient(sc, g0, motes_rect=(0, 300, W5, 1200)):
    sc.fx.append(Swifts(g0, n=8, seed=3))
    sc.fx.append(gfx(FX.motes, g0, rect=motes_rect, count=34, color=(255, 240, 200), size=(3, 6), seed=17, alpha=120))


# ================================================================== the crowds (shared)
def add_town_crowds(sc, g0, wall=True, line=True):
    """s05: the wall of backs on the near side (where Zacchaeus can't see) and the people lining the far side."""
    if line:
        frames = [doc(C.jericho_crowd(2290, CY, CK, 1, n=11, pose="line", rows=1, width=1250, seed=1, phase=p))
                  for p in (0.0, 0.25, 0.5, 0.75)]
        sc.add("c_line", frames, z=Z_FARCROWD, seed=151,
               frame_at=lambda t: float(int(math.floor((t + g0) / 0.42)) % 4))
    if wall:
        frames = [doc(C.jericho_crowd(2150, 1062, K, 1, n=22, pose="back", rows=2, width=1000, seed=2, phase=p))
                  for p in (0.0, 0.25, 0.5, 0.75)]
        sc.add("c_wall", frames, z=Z_WALL, seed=157,
               frame_at=lambda t: float(int(math.floor((t + g0) / 0.36)) % 4))


def add_right_crowd(sc, g0):
    """The people lining the far side of the road to the right of the tree (watching Jesus come)."""
    frames = [doc(C.jericho_crowd(5020, CY, CK, -1, n=10, pose="line", rows=1, width=1050, seed=5, phase=p))
              for p in (0.0, 0.25, 0.5, 0.75)]
    sc.add("c_right", frames, z=Z_FARCROWD, seed=163, frame_at=lambda t: float(int(math.floor((t + g0) / 0.4)) % 4))


# The people at the tree (far edge): kind, variant, x0 (gathered, s05) -> x1 (parted, s06), and their drawing per state:
# (pose, facing, expr, mod); facing 'mid' = towards Jesus under the tree, 'zj' = towards Jesus and Zacchaeus walking off
# to the left (s07).
TREE_CROWD = [
    dict(kind="woman", v=1, x0=3140, x1=3140, idle=("look", 1), open=("smile", 1), gasp=("stand", 1, "surprised", "up_hands"),
         murmur=("mutter", 1, "surprised"), watch=("look", 1, "surprised"), see=("stand", -1, "surprised"),
         frown=("arms_folded", -1), mutter=("mutter", 1), hmph=("frown", -1, "cross"), glare=("arms_folded", -1)),
    dict(kind="man", v=2, x0=3212, x1=3212, idle=("point", 1), open=("cheer", 1), gasp=("stand", 1, "surprised", "up_point"),
         murmur=("mutter", -1, "surprised"), watch=("stand", 1, "surprised"), see=("stand", -1, "surprised"),
         frown=("frown", -1), mutter=("mutter", -1), hmph=("point", -1, "grumble"), glare=("arms_folded", -1)),
    dict(kind="man", v=4, x0=3790, x1=3640, idle=("look", 1), open=("smile", 1), gasp=("look", 1, "surprised", "up"),
         murmur=("look", 1, "surprised", "up"), watch=("stand", 1, "surprised"), see=("stand", -1, "surprised"),
         frown=("arms_folded", -1), mutter=("mutter", 1), hmph=("arms_folded", -1), glare=("frown", -1)),
    dict(kind="woman", v=3, x0=3858, x1=4252, idle=("point", 1), open=("wave", -1), gasp=("stand", -1, "surprised", "up_hands"),
         murmur=("mutter", 1, "surprised"), watch=("stand", -1, "surprised"), see=("stand", -1, "surprised"),
         frown=("frown", -1), mutter=("mutter", -1), hmph=("frown", -1, "cross"), glare=("arms_folded", -1)),
    dict(kind="child", v=1, x0=4390, x1=4390, idle=("wave", 1), open=("wave", -1), gasp=("look", -1, "surprised", "up"),
         murmur=("mutter", -1, "surprised"), watch=("stand", -1, "surprised"), see=("stand", -1, "surprised"),
         frown=("frown", -1), mutter=("mutter", 1), hmph=("arms_folded", -1), glare=("frown", -1)),
    dict(kind="elder", v=5, x0=4462, x1=4462, idle=("look", 1), open=("smile", -1), gasp=("stand", -1, "surprised", "up_hands"),
         murmur=("look", -1, "surprised", "up"), watch=("stand", -1, "surprised"), see=("stand", -1, "surprised"),
         frown=("frown", -1), mutter=("mutter", -1), hmph=("point", -1, "grumble"), glare=("arms_folded", -1)),
]
STEPS = 6                                         # the parting: steps from x0 to x1


def tree_crowd_markup(state, phase=0.0):
    """The people at the tree in a state: 'closed' (gathered, looking down the road for Jesus; phase idles them),
    'step1'..'step5' (stepping aside), 'open' (parted, welcoming), 'gasp', 'murmur', 'watch' (s06); 'see', 'frown',
    'mutter', 'hmph', 'glare' (s07)."""
    out = ""
    rng = random.Random(9)
    for i, p in enumerate(TREE_CROWD):
        dy = rng.uniform(-4, 4)
        kind, v, x0, x1 = p["kind"], p["v"], p["x0"], p["x1"]
        moving = abs(x1 - x0) > 1
        if state == "closed":
            pose, f = p["idle"]
            key = fk(kind, v, pose, f, None, phase + 0.3 * i)
            x = x0
        elif state.startswith("step"):
            k_ = int(state[4:])
            x = x0 + (x1 - x0) * k_ / STEPS
            if moving:
                key = fk(kind, v, ("walk_a", "walk_b")[(k_ + i) % 2], 1 if x1 >= x0 else -1, "happy")
            else:
                pose, f = p["idle"]
                key = fk(kind, v, pose, f, None, 0.3 * i)
        else:
            x = x1
            ent = p[state]
            pose, f = ent[0], ent[1]
            expr = ent[2] if len(ent) > 2 else None
            mod = ent[3] if len(ent) > 3 else None
            key = fk(kind, v, pose, f, expr, phase + 0.3 * i, mod)
        out += draw_key(key, x, CY + dy, CK)
    return out


def tree_crowd_layer(sc, g0, ents, z=Z_FARCROWD + 0.1, idle=(0.0, 0.25, 0.5, 0.75)):
    """The people at the tree as one flipbook: ents = [(t, state)] (hard cuts); 'closed' idles on the global clock."""
    states = []
    for _, s_ in ents:
        if s_ not in states:
            states.append(s_)
    frames, index = [], {}
    for s_ in states:
        if s_ == "closed":
            for j, p in enumerate(idle):
                index[(s_, j)] = len(frames)
                frames.append(doc(tree_crowd_markup(s_, p)))
        else:
            index[(s_, 0)] = len(frames)
            frames.append(doc(tree_crowd_markup(s_)))
    ents = sorted((snap(t) if t > 0 else -1e4, s_) for t, s_ in ents)

    def fa(t):
        cur = ents[0][1]
        for tk, s_ in ents:
            if t >= tk:
                cur = s_
        if cur == "closed":
            return float(index[(cur, int(math.floor((t + g0) / 0.45)) % len(idle))])
        return float(index[(cur, 0)])
    sc.add("c_tree", frames if len(frames) > 1 else frames[0], z=z, seed=171, frame_at=fa if len(frames) > 1 else None)


# ================================================================== the procession (shared with s06)
STRIDE = {"jesus": 87, "disc": 88, "man": 84, "woman": 81, "child": 49, "elder": 82, "fruit_seller": 84, "farmer": 84}
FOLLOWERS = [   # kind, variant, gap behind Jesus at the stop (px), walking period (s), y
    ("man", 3, 560, 0.33, YU - 18),
    ("woman", 0, 660, 0.35, YU - 22),
    ("child", 2, 735, 0.24, YU - 14),
    ("elder", 1, 850, 0.36, YU - 20),
    ("farmer", 4, 960, 0.34, YU - 16),
]


def walk_cuts(t_stop, x_stop, f, stride, per, t_from, stop_step=0.4):
    """Planted-foot walk ending with a stop at (t_stop, x_stop): [(t, x, 'walk_a'|'walk_b'|'stop')] from t_from on,
    moving in direction f (the anchor advances one stride on each cut)."""
    out = [(t_stop, x_stop, "stop")]
    x = x_stop - f * stride * stop_step
    t = t_stop - per
    i = 0
    while t > t_from - per:
        out.append((t, x, ("walk_b", "walk_a")[i % 2]))
        x -= f * stride
        t -= per
        i += 1
    return sorted(out)


def schedule_walk(fig, cuts, keyf, move=0.12):
    """Put walk cuts on a Fig: hard cuts at each time, the anchor advancing in a quick eased step around each cut."""
    first = True
    for t, x, fr in cuts:
        if first:
            fig.track = Track(x, fig.ref[1])
            fig.cut(0, keyf(fr), dip=False)
            fig._last_x = x
            first = False
            continue
        fig.cut(t, keyf(fr), dip=False)
        fig.track.to(t - move * 0.45, t + move * 0.55, x, fig.ref[1])
    return fig


def procession(sc, g0, c6):
    """Jesus, two disciples and the townsfolk walking to the tree, timed by s06's narration (c6 = s06 context) and
    placed in this scene's time: t_here = t06 + (c6.start - g0). Every cut is snapped on s06's frame grid first, so s05
    and s06 cut on exactly the same film frames. Returns the Figs (not yet built) and the stop time (this scene's time)."""
    off = c6.start - g0
    t_stop = snap(beat(c6, 0, "停") - 0.06)                         # s06 time
    t_from = t_stop - 26 * 0.34

    def shift(cuts):
        return [(snap(t) + off, x, fr) for t, x, fr in cuts]
    figs = {}
    # Jesus
    jf = Fig("p_jesus", lambda key: jes_svg(XU, YU, K, key), (XU, YU), Z_JESUS, g0, seed=211)
    schedule_walk(jf, shift(walk_cuts(t_stop, XU, -1, STRIDE["jesus"] * K, 0.34, t_from)),
                  lambda fr: jk("stand" if fr == "stop" else fr, -1, "warm"))
    jf.mots.append(breath((XU, YU), g0, 3.2, 0.010))
    figs["jesus"] = jf
    # the disciples (Peter and John), a little behind, stopping just after him
    for name, v, gap, per, dt, y in (("peter", "peter", 168, 0.33, 0.27, YU - 6), ("john", "john", 292, 0.35, 0.47, YU - 10)):
        df = Fig(f"p_{name}", lambda key, y=y: disc_svg(XU + 200, y, K, key), (XU + 200, y), Z_DISC, g0,
                 seed=223 + len(figs))
        schedule_walk(df, shift(walk_cuts(t_stop + dt, XU + gap, -1, STRIDE["disc"] * K, per, t_from)),
                      lambda fr, v=v: dk(v, "stand" if fr == "stop" else fr, -1, "happy"))
        df.mots.append(breath((XU + 200, y), g0, 3.0 + 0.2 * len(figs), 0.010, 0.3 * len(figs)))
        figs[name] = df
    # the townsfolk following
    for j, (kind, v, gap, per, y) in enumerate(FOLLOWERS):
        ff = Fig(f"p_folk{j}", lambda key, y=y: folk_svg(XU + 600, y, K * 0.97, key), (XU + 600, y), Z_FOLLOW, g0,
                 seed=241 + j)
        schedule_walk(ff, shift(walk_cuts(t_stop + 0.35 + 0.17 * j, XU + gap, -1, STRIDE[kind] * K * 0.97, per, t_from)),
                      lambda fr, kind=kind, v=v: fk(kind, v, "look" if fr == "stop" else fr, -1,
                                                    "eager" if fr == "stop" else "happy"))
        ff.mots.append(breath((XU + 600, y), g0, 2.8 + 0.15 * j, 0.011, 0.2 * j))
        figs[f"folk{j}"] = ff
    return figs, t_stop + off


# ================================================================== the twig he pushes aside
TWIG_BASE = (3936, 384)
TWIG_PUSH = 42.0


def _twig_svg():
    pal = PR._jr_pal(TIME)
    rng = random.Random(4)
    bx, by = TWIG_BASE
    body = PR._leaf_spray(bx, by, 94, 175 * K, 6, (pal["leaf_lt"], S.shade(pal["leaf_lt"], 0.12), pal["leaf_lt"]), rng, 0.0,
                          size=29 * K)
    return doc(S.g(body, filter="wobble-fine"))


def add_twig(sc, g0, push):
    """The twig of leaves by the sitting spot; push(t) = how far it is pushed aside (degrees, negative = away from
    his face); it sways on the global clock."""
    tbx, tby = TWIG_BASE
    sc.add("twig", _twig_svg(), z=Z_TWIG, seed=191,
           motion=lambda t: Tf(rot=2.2 * math.sin(2 * math.pi * (t + g0) / 2.9) + push(t), px=tbx, py=tby))


# ================================================================== the scene
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(5)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731

    # ---- beats
    t_you = b(0, "有")
    t_run = b(0, "撒该往前跑")
    t_lu = b(0, "路上")
    t_nali = b(1, "那里")
    t_dada = b(1, "大大")
    t_shuzhi = b(1, "树枝")
    t_di = b(1, "低")
    t_cu = b(1, "粗")
    t_zh = b(1, "正好")
    t_pa0 = b(1, "爬")
    t_pa = [b(2, "爬", k) for k in range(5)]
    t_sang = b(2, "桑")
    t_l2e = ctx.lines[2].end
    t_hei = b(3, "嘿")
    t_hei2 = b(3, "嘿", 1)
    t_zx = b(3, "这下")
    t_qing = b(3, "清清楚楚")
    t_l3e = ctx.lines[3].end

    # ---- the world
    def glow(t):
        return 0.85 * env(t, t_di - 0.15, t_zh + 0.9, 0.35, 0.8) * (0.8 + 0.2 * math.sin(2 * math.pi * (t - t_di) / 1.1))
    add_world(sc, g0, branch_glow=glow)
    add_town_crowds(sc, g0)
    add_right_crowd(sc, g0)
    tree_crowd_layer(sc, g0, [(0, "closed")])

    # ---- Zacchaeus
    X0, Y0 = 2560, 1150
    st = SP["climb"]
    REF = ZREF
    zac = Fig("zac", lambda key, i=0: zac_svg(REF[0], REF[1], K, key) if key[1] != "run" else
              zac_svg(REF[0], REF[1], K, zk("run", 1, None, 0.25 + 0.5 * i)), REF, Z_ZAC, g0, seed=181,
              loops={zk("run"): (2, 0.15)})
    zac.track = Track(X0, Y0)
    zac.cut(0, zk("think", 1))
    # '有了！'
    t_idea = snap(t_you - 0.04)
    zac.cut(t_idea, zk("idea", 1), depth=6)
    zac.mots.append(bump(t_idea + 0.02, K, REF, 16, 0.3))
    # the run
    t_r0 = snap(t_run - 0.14)
    X_STOP = 3478
    t_r1 = snap(max(t_lu + 0.15, t_r0 + 3.0))
    zac.cut(t_r0, zk("run"), depth=5)
    path = [(2760, Y0), (2980, Y0 - 18), (3180, YT + 75), (3340, YT + 12), (X_STOP, YT)]
    def run_speed(u):
        # accelerate over the first 10 %, steady, then brake over the last 12 %
        a, bb = 0.10, 0.12
        vmax = 1.0 / (1 - a / 2 - bb / 2)
        if u < a:
            return vmax * u * u / (2 * a)
        if u < 1 - bb:
            return vmax * (a / 2 + (u - a))
        w = 1 - u
        return 1 - vmax * w * w / (2 * bb)
    zac.track.along(t_r0 + 0.02, t_r1, path, run_speed)
    # the halt (leaning back, a dust cloud)
    zac.cut(t_r1 - 0.02, zk("bumped", 1, "eager", marks=False), depth=8)
    t_halt = t_r1
    # look up at the big tree, 'so big!'
    t_look = snap(max(t_halt + 0.55, t_nali - 0.1))
    zac.cut(t_look, zk("stand", 1, "surprised", mod="look_up"), depth=5)
    zac.cut(snap(t_dada - 0.05), zk("stand", 1, "eager", mod="big"), depth=6)
    zac.cut(snap(t_shuzhi - 0.05), zk("stand", 1, "eager", mod="point_up"), depth=5)
    zac.cut(snap(t_cu + 0.05), zk("stand", 1, "determined", mod="nod"), depth=7)
    # three quick steps to the trunk (planted-foot walk a, c, b, c)
    xa = st[0]["anchor"][0]
    t_w0 = snap(t_zh + 0.12)
    adv = (20.8, 47.2, 45.3, 22.8)
    frames_w = ("walk_c", "walk_b", "walk_c", "walk_a")
    tot = sum(adv)
    x = X_STOP
    per = 0.13
    for i in range(4):
        tk = snap(t_w0 + i * per)
        zac.cut(tk, zk(frames_w[i], 1, "determined"), dip=False)
        x += (xa - X_STOP) * adv[i] / tot
        zac.track.to(tk - 0.05, tk + 0.07, x, YT)
    t_atr = snap(t_w0 + 4 * per)
    # '爬': hands on the fork
    zac.cut(snap(t_pa0 - 0.04), zk("climb_a", 1, "determined"), depth=5)
    # the climb: one stage on every 爬 (the anchor slides up in an eased 0.2 s pull)
    stages = [("climb_b", st[1]["anchor"]), ("climb_c", st[2]["anchor"]), ("climb_d", st[3]["anchor"]),
              ("climb_c", st[4]["anchor"])]
    exprs = ("determined", "determined", "eager", "determined")
    for i, (pose, (ax, ay)) in enumerate(stages):
        tc = snap(t_pa[i] - 0.06)
        zac.cut(tc, zk(pose, 1, exprs[i]), dip=False)
        zac.track.to(tc, tc + 0.2, ax, ay, curve="out")
        zac.mots.append(squash(tc + 0.22, K, REF, 4.0))
    # '爬上了': the hoist onto the sitting branch, then a scoot along it to the sitting spot on '桑树'
    LX = lambda lx, ly: PR.local_to_stage(XT, YT, K, 1, lx, ly)   # noqa: E731
    seat_a = LX(48, -470)
    tc = snap(t_pa[4] - 0.06)
    zac.cut(tc, zk("sit_branch", 1, "determined", mod="sit_up"), dip=False)
    zac.track.to(tc - 0.001, tc, seat_a[0] - 26, seat_a[1] + 70)
    zac.track.to(tc + 0.001, tc + 0.26, seat_a[0], seat_a[1], curve="out")
    zac.mots.append(squash(tc + 0.28, K, REF, 6.0))
    t_sc = snap(max(t_sang - 0.05, tc + 0.5))
    sx, sy = SP["sit"]
    zac.cut(t_sc, zk("sit_branch", 1, "overjoyed"), dip=False)
    mid = ((seat_a[0] + sx) / 2, (seat_a[1] + sy) / 2)
    zac.track.to(t_sc, t_sc + 0.2, mid[0], mid[1], lift=8 * K)
    zac.track.to(t_sc + 0.22, t_sc + 0.42, sx, sy, lift=8 * K)
    zac.mots.append(squash(t_sc + 0.44, K, REF, 5.0))
    # settled, a happy wiggle
    zac.mots.append(bump(t_l2e + 0.15, K, REF, 8, 0.24))
    zac.mots.append(bump(t_l2e + 0.42, K, REF, 6, 0.22))
    # '嘿嘿': peek out with a big grin, two giggle bobs; then eager, watching the road
    t_pk = snap(t_hei - 0.06)
    zac.cut(t_pk, zk("peek", 1, "laugh"), depth=6)
    zac.mots.append(bump(t_hei2 - 0.02, K, REF, 7, 0.2))
    zac.mots.append(bump(t_hei2 + 0.24, K, REF, 6, 0.2))
    zac.cut(snap(t_zx + 0.35), zk("peek", 1, "eager"), dip=False)
    zac.cut(snap(t_qing + 0.1), zk("peek", 1, "happy"), dip=False)
    zac.cut(snap(t_l3e + 0.1), zk("peek", 1, "eager"), dip=False)
    # blinks (none in the last 1.2 s: the fade into s06 must match)
    zac.blinks(zac_blink, 1.6, T - 1.25, rng, avoid=[(t_r0 - 0.3, t_atr + 0.2), (t_pa0 - 0.4, t_sc + 0.6)])
    zac.mots.append(breath(REF, g0, 2.6, 0.012))
    zac.build(sc)

    # the light bulb's extra glow
    bp = C.body_points(C.zacchaeus, X0, Y0, K, 1, pose="idea")
    bx, by = bp["head"][0] + 0.15 * 40 * K, bp["head"][1] - 2.05 * 40 * K
    gid = "zq5bulb"
    defs = S.rad_grad(gid, [(0, "#fff6c8", 0.95), (0.4, "#ffe08a", 0.5), (1, "#ffe08a", 0)])
    sc.add("bulb_glow", doc(f'<circle cx="{f1(bx)}" cy="{f1(by)}" r="110" fill="url(#{gid})"/>', defs), z=Z_FX, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=env(t, t_idea, t_r0 + 0.05, 0.12, 0.2) * (0.75 + 0.25 * math.sin(t * 9)),
                                                sx=0.8 + 0.25 * M.progress(t, t_idea, t_idea + 0.3, "back"),
                                                sy=0.8 + 0.25 * M.progress(t, t_idea, t_idea + 0.3, "back"), px=bx,
                                                py=by - 12 * K))
    sc.fx.append(FX.sparkles((bx - 90, by - 80, bx + 90, by + 50), count=7, t0=t_idea, t1=t_r0 + 0.2, color=(255, 236, 160),
                             size=(6, 12), period=0.9, drift=-20, seed=51))

    # the dust cloud of the halt
    hx = X_STOP - 20
    dust = ""
    for k_, (dx, r) in enumerate(((-40, 26), (-90, 20), (10, 18), (-135, 14), (-62, 15))):
        dust += (f'<ellipse cx="{f1(hx + dx * K)}" cy="{f1(YT - r * K * 0.7)}" rx="{f1(r * 1.35 * K)}" ry="{f1(r * K)}" '
                 f'fill="#efe0bf" stroke="{S.shade("#efe0bf", -0.35)}" stroke-width="2.4"/>')
    sc.add("dust", doc(S.g(dust, filter="wobble-fine")), z=Z_ZAC - 0.1, wc=0.5,
           motion=lambda t: Tf(alpha=env(t, t_halt - 0.05, t_halt + 0.9, 0.08, 0.5),
                               sx=0.7 + 0.5 * M.progress(t, t_halt - 0.05, t_halt + 0.9, "out"),
                               sy=0.7 + 0.5 * M.progress(t, t_halt - 0.05, t_halt + 0.9, "out"),
                               dx=-30 * M.progress(t, t_halt, t_halt + 0.9, "out"), px=hx, py=YT))

    # the twig he pushes aside on '嘿嘿' (sways in the breeze on the global clock)
    tbx, tby = TWIG_BASE
    add_twig(sc, g0, lambda t: -TWIG_PUSH * M.progress(t, t_pk - 0.04, t_pk + 0.2, "out")
             + 7 * math.sin(math.pi * clamp01((t - t_pk - 0.2) / 0.45)) * (t > t_pk + 0.2))
    leaves = LeafFall([(t_pa[1] + 0.05, XT - 40, YT - 330, 2, 50), (t_pa[3] + 0.05, XT + 30, YT - 420, 2, 50),
                       (t_pk + 0.1, tbx + 10, tby + 90, 3, 30), (t_sc + 0.3, sx + 60, sy - 60, 1, 30)], seed=7)
    sc.fx.append(leaves)

    # ---- the procession (from s06's timing)
    c6 = context("s06_call")
    figs, _ = procession(sc, g0, c6)
    for f_ in figs.values():
        f_.build(sc)

    add_ambient(sc, g0)

    # ---- camera
    c_open = Cam(2470, 832, 1420)
    c_arrive = Cam(3420, 760, 1760)
    c_tree = Cam(3700, 650, 2311)
    c_branch = Cam(3660, 700, 1800)
    c_climb0 = Cam(3690, 690, 1640)
    c_climb1 = Cam(3760, 580, 1460)
    c_peek = Cam(3860, 510, 1260)
    sc.camera = cam_path([(0.0, c_open), (t_r0 + 0.1, c_open), (t_halt + 0.35, c_arrive), (t_nali, c_arrive),
                          (t_nali + 1.9, c_tree), (t_shuzhi - 0.2, c_tree), (t_di + 0.8, c_branch),
                          (t_pa0, c_climb0), (t_pa[1], c_climb0), (t_sc + 0.4, c_climb1), (t_hei - 0.35, c_climb1),
                          (t_hei + 0.55, c_peek), (t_zx + 0.15, c_peek), (min(T - 1.25, t_l3e + 0.3), CAM_HANDOFF),
                          (T, CAM_HANDOFF)],
                         ["linear", "sine", "linear", "inout", "linear", "inout", "linear", "inout", "linear", "inout",
                          "linear", "inout", "linear", "inout", "linear"])

    # ---- sound
    sc.sfx("crowd", 0, dur=t_r0 + 2.5, gain_db=-17, fade_in=0.6, fade_out=1.8, pan=-0.3)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 4.0, dur=T - 3.5, gain_db=-22, fade_in=1.5, fade_out=1.0, pan=0.2)
    sc.sfx("pop", t_idea, gain_db=-9)
    sc.sfx("sparkle", t_idea + 0.05, gain_db=-15)
    sc.sfx("footsteps_run", t_r0 + 0.05, dur=t_r1 - t_r0, gain_db=-14, pan=0.1)
    sc.sfx("whoosh", t_halt - 0.12, gain_db=-16, pan=0.2)
    sc.sfx("thud", t_halt, gain_db=-16)
    sc.sfx("sparkle", t_di - 0.1, gain_db=-17, pan=0.1)
    sc.sfx("footsteps", t_w0, dur=4 * per + 0.1, gain_db=-20)
    for i, tp in enumerate([t_pa0] + t_pa[:4]):
        sc.sfx("cloth", tp - 0.04, gain_db=-15 - (i % 2), pan=0.05)
    sc.sfx("cloth", t_pa[4] - 0.04, gain_db=-14)
    sc.sfx("pop", t_sc + 0.42, gain_db=-14)
    sc.sfx("cloth", t_pk, gain_db=-16, pan=0.2)
    sc.sfx("crowd", t_zx - 0.6, dur=T - t_zx + 1.6, gain_db=-19, fade_in=1.6, fade_out=0.4, pan=0.5)
    sc.sfx("footsteps", t_zx + 0.4, dur=T - t_zx, gain_db=-25, fade_in=1.0, fade_out=0.3, pan=0.5)
    return sc
