"""Scene 2 (v2) — God calls Jonah (Jonah 1:1-2).

Jonah's home village in the green-gold hills of Israel on a fresh morning (the approved v1 village, art and
helpers imported from art.scenes_v1.s02_call): flat-roofed houses, olive trees, grazing sheep, a dirt road over
the ridge to the village on the hill and on to the east (right).

  * "很久很久以前…有一个先知" — wide establishing shot; Jonah steps out of his door and strolls across the yard
    (planted-foot walk cycle driven by the distance walked); a neighbour and her little girl stand on the path.
    "名叫约拿" — Jonah gives a happy hop and waves.
  * "先知，就是替上帝传话的人" — a little golden light drops out of the clouds to Jonah (he cups his ear,
    smiling); on "传话" he turns to the neighbours, arm raised, and a speech bubble carrying the same golden
    star goes to them; they listen and nod. As the bubble melts the girl skips off past her mother, who follows:
    over the crest and up across the far meadow (planted-foot walk, shrinking with distance) to the village,
    where they slip behind the front house (a cut-out of that house's own pixels covers them).
  * "有一天，上帝对约拿说" — Jonah kneels to pray; the clouds above him part and warm golden rays pour down
    (God is never drawn — only light, sparkles and his voice).
  * "约拿，你起来" — he opens his eyes, then rises (one-knee in-between, hop) and listens; "到尼尼微…" — a vision
    opens far to the EAST (upper right): the great city of Nineveh; Jonah turns his face up toward it.
  * "城里的人做了许多坏事" — a grey cloud of wrongdoing gathers over the city, Jonah becomes worried; "我都看见了"
    — the heavenly light swells once; "你要去大声警告他们" — hand on his chest: "me?" (a few blinks in the holds)
  * "尼尼微在很远的东方" — the camera widens, a dashed road draws itself over the hills eastward to the vision,
    Jonah points up at the vision; "那里的人很凶" — stern Assyrian soldiers, spear in fist and shield on arm,
    rise into the vision and the gloom over the city deepens; Jonah drops his arm, uneasy (worried, no fear);
    "是以色列人的敌人" — he folds his arms, grumpy brow, chin down, eyes away from the vision: displeased, not
    afraid (his real reason is told later in the story, Jonah 4:2; s03 opens on his angry refusal). As the
    line ends the vision closes gently (fade + slight shrink, gone before mid-dissolve, so it never ghosts over
    s03); calm hold to the end. The God-light sparkles keep out of Jonah's head column (never on his face).

Pose / face changes are HARD switches (never crossfaded doubles), each sold by a small squash or hop and held
>= 0.5 s. Every beat is keyed to the subtitle chunk that contains its phrase (``_when``), never to fixed times.
"""
import bisect
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s02_call as V
from art.style import P
from engine import motion as M
from engine import fx as FX
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = V.SW, V.SH                 # 2400 x 1350 (the v1 village stage)
JX, JY, JS = V.JX, V.JY, V.JS       # Jonah's spot in the yard (the light lands here): 960, 1150, 1.2
DOOR = (392, 1100)                  # Jonah in his doorway at the start
GAP = V.GAP                         # where the clouds part (990, 215)
BX, BY, RX, RY = V.BX, V.BY, V.RX, V.RY   # the vision window

# neighbours (stand on the dirt path, facing Jonah): mother (woman, variant 3) and her daughter (child, variant 1)
MOM = dict(kind="woman", var=3, x=1296, y=1040, s=1.0, h=321)
GIRL = dict(kind="child", var=1, x=1220, y=1082, s=1.08, h=224)
NEAR_SEED = 57                      # watercolour seed of the near-ground layer

# the neighbours' way home: over the crest of the near ridge, up across the far meadow (beside the painted
# village road) and behind the front village house (v1 mid-hills art: house variant 3 at (1225, 884) x0.15,
# with its little bush at the right corner). Figure scale follows a simple perspective: 1 at the start,
# K_CREST on the ridge line, then ~ (y - HORIZON_Y) up the far meadow.
CREST_Y = 1018
HORIZON_Y = 856
K_CREST, K_MIN = 0.88, 0.12
K_STEP = 0.5                        # below this scale steps stop being planted exactly (invisible that small)
BEHIND = [(1298, 880), (1278, 877), (1250, 875)]
MOM_ROUTE = [(MOM["x"], MOM["y"]), (1300, 1012), (1302, 980), (1304, 950), (1305, 920), (1307, 898), (1308, 887),
             (1307, 884)] + BEHIND
# the girl (ahead of her mother) keeps to the road side, right of her mother's line, so she is not hidden by her;
# from her corner she passes in front of the tall house before slipping behind the front one
GIRL_ROUTE = [(GIRL["x"], GIRL["y"]), (1250, 1062), (1278, 1042), (1298, 1024), (1322, 1012), (1340, 1000),
              (1346, 975), (1347, 945), (1347, 915), (1346, 895), (1345, 887), (1344, 884), (1324, 881)] + BEHIND
HOUSE_FRONT_Y = 884.6               # feet above this line = behind the front village house
HIDDEN_X = 1272                     # fully behind its wall (and bush) from here on (checked at 4x)
VILLAGE_HOUSE = (1225, 884, 0.15, 3)
MID_SEED = 17                       # watercolour seed of the mid-hills layer (= its default; the cut-out reuses it)
HOUSE_BOX = (1168, 776, 1302, 894)

PUNCT = "，、。：；！？,.!?:;"
SUB_TOP = 940                       # output y where the subtitle band begins

# closed-eye blink faces that keep the brow and mouth of the face they blink from. Added to the shared
# expression table under s02-only names at import (no existing entry is changed).
for _nm in ("worried", "surprised", "angry"):
    _e = dict(C.EXPRS[_nm])
    _e["eyes"] = "closed"
    C.EXPRS.setdefault(f"s02_blink_{_nm}", _e)


def _doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def _f(v):
    return f"{v:.1f}"


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


# ------------------------------------------------------------------ timing helpers
def _when(ctx, phrases, k=0.0, default=None, after=0.0):
    """Estimated time (s from scene start) at which ``phrase`` is spoken: the start of the subtitle chunk that
    contains it plus its share of the chunk's duration by character position (punctuation inside counts as one
    character of pause). k shifts within the phrase (1 = its end). Tries each alternative; chunks starting
    before ``after`` are skipped."""
    if isinstance(phrases, str):
        phrases = (phrases,)
    for ph in phrases:
        for ln in ctx.lines:
            for c in (ln.chunks or [ln]):
                if c.start < after - 1e-6 or ph not in c.text:
                    continue
                txt = c.text.rstrip(PUNCT)
                i = c.text.index(ph) + k * len(ph)
                return c.start + (c.end - c.start) * _clamp(i / max(1, len(txt)))
    return default


def _chunk_start(ctx, phrases, after=0.0):
    """Start of the first subtitle chunk (starting at or after ``after``) that contains one of the phrases."""
    if isinstance(phrases, str):
        phrases = (phrases,)
    for ph in phrases:
        for ln in ctx.lines:
            for c in (ln.chunks or [ln]):
                if c.start >= after - 1e-6 and ph in c.text:
                    return c.start
    return None


def _hop(t, t0, h=10.0, dur=0.3):
    if t0 is None or not (t0 <= t <= t0 + dur):
        return 0.0
    return -h * math.sin(math.pi * (t - t0) / dur)


def _squash(t, t0, k=0.04, dur=0.32):
    """(sx, sy) of a quick landing squash that recovers."""
    if t0 is None or not (t0 <= t <= t0 + dur):
        return 1.0, 1.0
    u = (t - t0) / dur
    q = math.sin(math.pi * min(1.0, u * 1.6)) * (1 - u)
    return 1 + 0.6 * k * q, 1 - k * q


def _sched(events):
    """[(t, value), ...] -> f(t) = value of the last event at or before t (hard switches)."""
    ev = sorted(events, key=lambda e: e[0])

    def f(t):
        v = ev[0][1]
        for te, val in ev:
            if t >= te:
                v = val
            else:
                break
        return float(v)
    return f


# ------------------------------------------------------------------ figures
def _fig(design, metrics, x, y, s, facing, ps, expr, label, marks=True):
    inner, _ = C._figure(design, metrics, ps, expr, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


def _jfig(x, y, s, ps, expr, label, facing=1, marks=True):
    return _fig(C._jonah_design(), C._ADULT, x, y, s, facing, ps, expr, label, marks)


def _walk_pose(k, A, N, t=4, swing=36, lift=20, drop=10, off=0.0, fall=0.0):
    """Planted-foot walk drawing k (N drawings per step, two steps per cycle): the planted ankle goes from +A to
    -A figure px while the other foot swings through, so advancing the anchor 2*A*scale/N per drawing keeps the
    planted sole on one spot of the ground (same rig as the v1 captain walk). ``off`` shifts the drawings along
    the cycle by that fraction of a drawing (0.5 with an odd N: the middle drawing of each step is the passing
    position, feet together under the body). ``fall``: figure px the anchor moves DOWN per step (walking a
    little downstage); the planted foot is raised by what the anchor has dropped since mid-step (lowered before
    it), so its sole stays on its spot in y too and is on the anchor's ground line in the passing position,
    and the swing foot comes down onto the lower spot."""
    ph = ((k + off) % (2 * N)) / N
    step, u = divmod(ph, 1.0)
    plant = ("ik", A * (1 - 2 * u), 1, fall * (u - 0.5)) if fall else ("ik", A * (1 - 2 * u), 1)
    swing_leg = ("ik", -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 1,
                 lift * math.sin(math.pi * u) + fall * (u - 0.5 + math.cos(math.pi * u)))
    sw = swing * math.cos(math.pi * ph)
    return C._P(t=t, h=-3, legs=(plant, swing_leg) if step == 0 else (swing_leg, plant),
                arms=(("fk", -sw, -sw + 16), ("fk", sw, sw + 16)),
                drop=drop + 0.4 * drop * math.cos(2 * math.pi * u))


WAVE_A = C._P(h=-6, arms=(("fk", 14, 8), ("fk", -150, -160)), hands=("fist", "open"), expr="happy")
WAVE_B = C._P(h=-6, arms=(("fk", 14, 8), ("fk", -146, -184)), hands=("fist", "open"), expr="happy")
EXPLAIN = C._P(h=-4, arms=(("fk", 60, 120), ("fk", -8, -3)), hands=("open", "fist"))   # telling, palm up
RISE = C._P(t=4, h=-8, drop=70, legs=(("ik", 60, 1), (0, -92)), arms=(("fk", 30, 40), ("fk", 20, 50)),
            hands=("open", "open"), feet=(None, 100))
# listening with the face turned up toward the vision (upper right): head tilted further up, eyes up-forward
LOOK = dict(C.POSES["listen"], h=-22, look=(0.09, -0.07))
# pointing up at the vision: the pointing (far) arm raised ~30 deg above level, head and eyes following it
POINT_UP = dict(C.POSES["point"], h=-10, arms=(("fk", 116, 122), ("fk", -8, -3)), look=(0.07, -0.06))
# uneasy: standing, arms down, still looking toward the vision
UNEASY = dict(C.POSES["stand"], h=-6, look=(0.06, -0.05))
# displeased: arms folded (sit_sulk's arms on a standing figure), chin down, eyes away from the vision
CROSSED = C._P(t=-2, h=10, arms=(("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
               far_front=True, look=(-0.07, 0.03))


def _neighbour(n, pose_kw, expr, facing, x=None, y=None, label=""):
    """A neighbour figure from the citizens' rig (Israelite villagers: veil / tunic, no Assyrian beard)."""
    d = C._citizen_design(n["kind"], n["var"], "normal")
    m = C._CHILD if n["kind"] == "child" else C._metrics(C._ADULT, 0.96, 0.92)
    return _fig(d, m, n["x"] if x is None else x, n["y"] if y is None else y, n["s"], facing, pose_kw, expr,
                f"{n['kind']}-{label}")


def _shadow(x, y, s, w=120, op=0.24):
    return C.ground_shadow(x, y, s, width=w, opacity=op)


class _Cut:
    """A rectangle of a static layer's OWN pixels (rasterised and watercoloured exactly as the compositor does
    it: same svg, seed and strength), optionally masked to the silhouette drawn by ``mask_svg``. Drawn right
    after a figure that has walked behind that part of the layer, so the layer hides it."""

    def __init__(self, svg, seed, box, mask_svg=None):
        self.svg, self.seed, self.box = svg.replace(S.BOIL_TOKEN, "1"), seed, box
        self.mask_svg = mask_svg.replace(S.BOIL_TOKEN, "1") if mask_svg else None
        self.res = None

    def image(self):
        if self.res is None:
            from PIL import ImageChops
            from engine import raster
            from engine import watercolor as WC
            im = WC.watercolor(raster.rasterize(self.svg, SW, SH), seed=self.seed, strength=1.0, edge=1.0)
            im = im.crop(self.box)
            if self.mask_svg:
                mask = raster.rasterize(self.mask_svg, SW, SH).crop(self.box).getchannel("A")
                im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
            self.res = (im, self.box[:2])
        return self.res


def _route(pts, y0, step=0.5):
    """Dense samples (x, y, k, w, facing) along a walking route: k = relative figure scale (1 at the start,
    K_CREST on the ridge line, then shrinking toward HORIZON_Y up the far meadow), w = distance walked in
    figure px at relative scale 1 (a planted-foot step advances a fixed w), facing = walking direction."""
    def kf(y):
        if y >= CREST_Y:
            return 1 - (1 - K_CREST) * _clamp((y0 - y) / max(1.0, y0 - CREST_Y))
        return max(K_MIN, K_CREST * (y - HORIZON_Y) / (CREST_Y - HORIZON_Y))
    out, w, face = [], 0.0, 1
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        seg = math.hypot(bx - ax, by - ay)
        if bx - ax > 2:
            face = 1
        elif bx - ax < -2:
            face = -1
        n = max(1, int(seg / step))
        for j in range(n):
            x, y = ax + (bx - ax) * j / n, ay + (by - ay) * j / n
            k = kf(y)
            out.append((x, y, k, w, face))
            w += seg / n / max(k, K_STEP)
    out.append((pts[-1][0], pts[-1][1], kf(pts[-1][1]), w, face))
    return out


# ------------------------------------------------------------------ static art
def _house_svg():
    """Jonah's house (v1 art) without v1's baked-in shadow at his spot (he walks there in this version)."""
    hx, hy, hs = V.HOUSE
    body = PR.house(hx, hy, hs, variant=3)
    body += V._house_details()
    jx, jy = V._hp(640, 1062)
    body += PR.jar(jx, jy, 0.6)
    jx, jy = V._hp(700, 1076)
    body += PR.jar(jx, jy, 0.46, color=S.mix(P["terracotta"], P["sand"], 0.3))
    body += PR.bush(-10, 1124, 0.9, variant=1)
    body += S.g(V._flowers(330, 1200, 8, 170, 9), filter="wobble")
    return _doc(body)


def _star(cx, cy, r, fill, inner=0.24):
    w = r * inner
    pts = [(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r), (cx - w, cy + w),
           (cx - r, cy), (cx - w, cy - w)]
    return f'<path d="M{" L".join(f"{_f(x)},{_f(y)}" for x, y in pts)} Z" fill="{fill}"/>'


ORB0 = (GAP[0] + 10, GAP[1] + 70)          # the little light leaves the clouds here...
ORB1 = (JX + 44, JY - 386)                 # ...and reaches Jonah just above-front of his head


def _orb_svg():
    x, y = ORB0
    defs = S.rad_grad("orbg", [(0, "#fffbe8", 1), (0.28, "#ffe48a", 0.85), (0.6, "#ffcf5a", 0.32),
                               (1, "#ffc850", 0)])
    body = f'<circle cx="{x}" cy="{y}" r="105" fill="url(#orbg)"/>'
    body += f'<circle cx="{x}" cy="{y}" r="22" fill="#fffaf0"/>'
    body += _star(x, y, 48, "#ffe9a0", 0.22)
    body += _star(x, y, 30, "#fffdf2", 0.26)
    return _doc(body, defs)


def _orb_pos(u):
    """Point on the orb's gentle S-curve, u 0..1."""
    p0, p3 = ORB0, ORB1
    p1 = (p0[0] + 170, p0[1] + 190)
    p2 = (p3[0] - 150, p3[1] - 170)
    a = 1 - u
    x = a ** 3 * p0[0] + 3 * a * a * u * p1[0] + 3 * a * u * u * p2[0] + u ** 3 * p3[0]
    y = a ** 3 * p0[1] + 3 * a * a * u * p1[1] + 3 * a * u * u * p2[1] + u ** 3 * p3[1]
    return x, y


SB = (1136, 606)          # speech bubble centre
SB_R = (122, 84)
SB_TIP = (1034, 778)      # tail tip, just off Jonah's face


def _speech_svg():
    cx, cy = SB
    rx, ry = SB_R
    ink = P["ink"]
    defs = S.rad_grad("sbg", [(0, "#fff3c6", 0.95), (0.55, "#ffe39a", 0.45), (1, "#ffe08e", 0)])
    bub = S.blob(cx, cy, rx, ry, wobble=0.05, n=12, seed=4)
    tx, ty = SB_TIP
    tail = (f"M{_f(cx - 70)},{_f(cy + 52)} Q{_f(cx - 92)},{_f(cy + 110)} {_f(tx)},{_f(ty)} "
            f"Q{_f(cx - 46)},{_f(cy + 96)} {_f(cx - 20)},{_f(cy + 70)} Z")
    body = f'<path d="{tail}" fill="#fff8e6" stroke="{ink}" stroke-width="8" stroke-linejoin="round"/>'
    body += f'<path d="{bub}" fill="#fff8e6" stroke="{ink}" stroke-width="5"/>'
    body += f'<path d="{tail}" fill="#fff8e6"/>'
    body += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 0.8}" ry="{ry * 0.78}" fill="url(#sbg)"/>'
    return _doc(S.g(body, filter="wobble-fine"), defs)


def _speech_star_svg():
    cx, cy = SB
    body = _star(cx, cy, 46, "#f2c14e", 0.26)
    body += f'<path d="{_star_path(cx, cy, 46, 0.26)}" fill="none" stroke="{S.shade(P["gold"], -0.35)}" stroke-width="3"/>'
    body += _star(cx, cy, 24, "#fff4c4", 0.3)
    for ox, oy, r in [(-70, -34, 15), (66, -40, 12), (72, 30, 14), (-62, 36, 10)]:
        body += _star(cx + ox, cy + oy, r, "#f6cd5c", 0.3)
    return _doc(S.g(body, filter="wobble-fine"))


def _star_path(cx, cy, r, inner):
    w = r * inner
    pts = [(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r), (cx - w, cy + w),
           (cx - r, cy), (cx - w, cy - w)]
    return "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in pts) + " Z"


# the dashed road east (line 5): from Jonah's feet along the yard path, over the ridge, along the village road's
# eastern fork and up over the hills to the horizon under the vision. y decreases monotonically, so a bottom-up
# reveal draws it from Jonah outward.
TRAIL = [(1032, 1168), (1104, 1142), (1186, 1094), (1258, 1052), (1314, 1022), (1336, 990), (1396, 962),
         (1480, 934), (1566, 914), (1648, 900), (1716, 882), (1786, 858), (1800, 830), (1752, 806), (1706, 784),
         (1708, 760), (1756, 738), (1792, 716), (1776, 694), (1742, 676), (1748, 656), (1768, 640)]
TRAIL_Y = (TRAIL[0][1] + 14, TRAIL[-1][1] - 8)     # bottom / top of the drawn road (for the reveal)


def _catmull(pts, n=12):
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(len(pts) - 1, i + 2)]
        for j in range(n):
            u = j / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 +
                                    (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def _trail_svg():
    pts = _catmull(TRAIL)
    seg = [0.0]
    for a, b in zip(pts, pts[1:]):
        seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = seg[-1]

    def at(sv):
        for i in range(len(seg) - 1):
            if seg[i] <= sv <= seg[i + 1]:
                u = (sv - seg[i]) / max(1e-6, seg[i + 1] - seg[i])
                return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u
        return pts[-1]
    y0, y1 = TRAIL[0][1], TRAIL[-1][1]
    col = S.mix(P["ink_soft"], P["terracotta"], 0.3)
    dashes, under = "", ""
    sv = 0.0
    while sv < total:
        p = at(sv)
        k = 0.3 + 0.7 * _clamp((p[1] - y1) / (y0 - y1)) ** 1.3      # perspective: big near, small far
        ln, gap = 26 * k, 17 * k
        q = at(min(total, sv + ln))
        seg_d = f"M{_f(p[0])},{_f(p[1])} L{_f(q[0])},{_f(q[1])}"
        under += f'<path d="{seg_d}" stroke="#fff7e2" stroke-width="{_f(16 * k)}" stroke-linecap="round" fill="none"/>'
        dashes += f'<path d="{seg_d}" stroke="{col}" stroke-width="{_f(8 * k)}" stroke-linecap="round" fill="none"/>'
        sv += ln + gap
    return _doc(f'<g opacity="0.75">{under}</g>' + dashes)


# ------------------------------------------------------------------ the fierce soldiers in the vision
SOLDIERS = [(1548, 0.50, 0), (1672, 0.56, 2), (1800, 0.50, 0)]   # (x, scale, citizen variant)
SOLDIER_FEET = 640


def _helmet(hx, hy, R):
    """Pointed Assyrian helmet over a head of radius R centred at (hx, hy) (facing left)."""
    ink = P["ink"]
    metal, metal_d = "#c9b48a", "#9c8862"
    d = (f"M{_f(hx - R * 1.06)},{_f(hy - R * 0.18)} C{_f(hx - R * 1.0)},{_f(hy - R * 1.1)} "
         f"{_f(hx - R * 0.3)},{_f(hy - R * 1.55)} {_f(hx + R * 0.12)},{_f(hy - R * 2.05)} "
         f"C{_f(hx + R * 0.4)},{_f(hy - R * 1.5)} {_f(hx + R * 1.05)},{_f(hy - R * 1.05)} "
         f"{_f(hx + R * 1.08)},{_f(hy - R * 0.2)} Z")
    out = f'<path d="{d}" fill="{metal}" stroke="{ink}" stroke-width="{_f(R * 0.12)}" stroke-linejoin="round"/>'
    out += (f'<path d="M{_f(hx - R * 0.2)},{_f(hy - R * 1.4)} Q{_f(hx + 0.05 * R)},{_f(hy - R * 1.0)} '
            f'{_f(hx + 0.2 * R)},{_f(hy - R * 0.4)}" stroke="#ece0c2" stroke-width="{_f(R * 0.14)}" fill="none" '
            f'stroke-linecap="round" opacity="0.8"/>')
    out += (f'<rect x="{_f(hx - R * 1.12)}" y="{_f(hy - R * 0.32)}" width="{_f(R * 2.24)}" height="{_f(R * 0.3)}" '
            f'rx="{_f(R * 0.12)}" fill="{metal_d}" stroke="{ink}" stroke-width="{_f(R * 0.1)}"/>')
    return out


# a soldier's stance: the near arm brought forward across the chest so its fist grips an upright spear just
# outside the body's front edge (the shaft never hides behind the torso or head); the far arm carries the shield
SPEAR_P = C._P(arms=(("fk", 14, 8), ("ik", "torso", 2.25, 0.60, 1)), hands=("fist", "fist"), expr="angry")


def _soldier(x, y, s, var):
    design, metrics = C._citizen_design("man", var, "normal"), C._ADULT

    def draw(x_, y_, s_, f_, label="soldier"):
        return _fig(design, metrics, x_, y_, s_, f_, SPEAR_P, "angry", label)
    fig = draw(x, y, s, -1, f"soldier{var}")
    bp = C.body_points(draw, x, y, s, -1)
    hx, hy = bp["head"]
    R = 44 * s
    nh = bp["hands"][1]
    ink = P["ink"]
    # spear held upright in the near fist, drawn over the figure: shaft from the ground to well above the
    # helmet, bronze leaf tip; then the fist again on top, so the shaft runs through the closed hand
    sx_ = nh[0]
    top = hy - 300 * s
    spear = (f'<path d="M{_f(sx_)},{_f(y + 10)} L{_f(sx_)},{_f(top)}" stroke="{ink}" '
             f'stroke-width="{_f(13 * s)}" stroke-linecap="round"/>'
             f'<path d="M{_f(sx_)},{_f(y + 10)} L{_f(sx_)},{_f(top)}" stroke="{P["wood"]}" '
             f'stroke-width="{_f(7 * s)}" stroke-linecap="round"/>')
    tip = (f'<path d="M{_f(sx_)},{_f(top - 62 * s)} C{_f(sx_ + 16 * s)},{_f(top - 30 * s)} '
           f'{_f(sx_ + 14 * s)},{_f(top - 4 * s)} {_f(sx_)},{_f(top + 6 * s)} '
           f'C{_f(sx_ - 14 * s)},{_f(top - 4 * s)} {_f(sx_ - 16 * s)},{_f(top - 30 * s)} '
           f'{_f(sx_)},{_f(top - 62 * s)} Z" fill="#d9b25e" stroke="{ink}" stroke-width="{_f(4 * s)}"/>')
    skin = C._CIT_COL[var % 4]["skin"]
    fist = (f'<circle cx="{_f(nh[0])}" cy="{_f(nh[1])}" r="{_f(12 * s)}" fill="{skin}" stroke="{ink}" '
            f'stroke-width="{_f(3.4 * s)}"/>'
            f'<path d="M{_f(nh[0] - 5 * s)},{_f(nh[1] - 7 * s)} q{_f(5 * s)},{_f(5 * s)} 0,{_f(14 * s)}" fill="none" '
            f'stroke="{ink}" stroke-width="{_f(2.2 * s)}" stroke-linecap="round"/>')
    # round shield on the far arm
    fh = bp["hands"][0]
    sh = (f'<circle cx="{_f(fh[0] + 14 * s)}" cy="{_f(fh[1] - 40 * s)}" r="{_f(62 * s)}" fill="#b5653f" '
          f'stroke="{ink}" stroke-width="{_f(5 * s)}"/>'
          f'<circle cx="{_f(fh[0] + 14 * s)}" cy="{_f(fh[1] - 40 * s)}" r="{_f(44 * s)}" fill="none" '
          f'stroke="#e0b25a" stroke-width="{_f(7 * s)}"/>'
          f'<circle cx="{_f(fh[0] + 14 * s)}" cy="{_f(fh[1] - 40 * s)}" r="{_f(13 * s)}" fill="#e0b25a" '
          f'stroke="{ink}" stroke-width="{_f(3.5 * s)}"/>')
    return fig + S.g(_helmet(hx, hy, R) + sh + spear + tip + fist, filter="wobble-fine")


def _soldiers_svg(rises):
    """The three soldiers risen by ``rises`` (0..1 each), clipped to the vision window."""
    defs = f'<clipPath id="winS"><ellipse cx="{BX}" cy="{BY}" rx="{RX - 3}" ry="{RY - 3}"/></clipPath>'
    body = ""
    order = [0, 2, 1]                      # the middle (nearest) one in front
    for i in order:
        x, s, var = SOLDIERS[i]
        r = rises[i]
        if r <= 0:
            continue
        y = SOLDIER_FEET + (1 - r) * 330 * s
        body += _soldier(x, y, s, var)
    # a dim reddish dusk behind them so they read as a separate, nearer plane
    return _doc(f'<g clip-path="url(#winS)">{body}</g>', defs)


# ------------------------------------------------------------------ a butterfly over the meadow
BFLY = (1560, 985)


def _butterfly_svg(open_k):
    """Small pale-yellow butterfly seen from above, wings opened by open_k (0..1)."""
    x, y = BFLY
    ink = P["ink"]
    k = max(0.12, open_k)
    out = ""
    for side in (-1, 1):
        ux, lx = x + side * 15 * k, x + side * 11 * k
        out += (f'<ellipse cx="{_f(ux)}" cy="{_f(y - 7)}" rx="{_f(15 * k)}" ry="13" fill="#f7d978" stroke="{ink}" '
                f'stroke-width="2.4" transform="rotate({-side * 18} {_f(ux)} {_f(y - 7)})"/>')
        out += (f'<ellipse cx="{_f(lx)}" cy="{_f(y + 9)}" rx="{_f(10 * k)}" ry="9" fill="#f3b45e" stroke="{ink}" '
                f'stroke-width="2.2"/>')
        out += f'<circle cx="{_f(x + side * 17 * k)}" cy="{_f(y - 9)}" r="{_f(3.2 * k + 1)}" fill="#e98a52"/>'
    out += f'<ellipse cx="{x}" cy="{y + 1}" rx="3.4" ry="13" fill="{P["ink_soft"]}" stroke="{ink}" stroke-width="1.6"/>'
    out += (f'<path d="M{x - 1},{y - 11} q-6,-10 -11,-12 M{x + 1},{y - 11} q6,-10 11,-12" fill="none" '
            f'stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>')
    return _doc(S.g(out, filter="wobble-fine"))


def _butterfly_motion(t):
    x = 140 * math.sin(2 * math.pi * t / 13.0) + 45 * math.sin(2 * math.pi * t / 4.1 + 1.0)
    y = 46 * math.sin(2 * math.pi * t / 7.3 + 0.6) + 12 * math.sin(2 * math.pi * t * 1.6)
    return Tf(dx=x, dy=y, rot=8 * math.sin(2 * math.pi * t / 2.2))


# ------------------------------------------------------------------ fx: the orb's sparkle trail
def _orb_trail(t0, t1, ease_fn):
    def fx(frame, t, view):
        if not (t0 <= t <= t1 + 0.6):
            return frame
        from PIL import Image, ImageDraw
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for k in range(1, 9):
            tk = t - k * 0.07
            if tk < t0 or tk > t1:
                continue
            u = ease_fn(_clamp((tk - t0) / (t1 - t0)))
            x, y = _orb_pos(u)
            x += 14 * math.sin(k * 2.1)
            y += 10 * math.cos(k * 1.7)
            ox, oy = view.to_out(x, y)
            r = (15 - k * 1.3) * view.scale
            a = int(220 * (1 - k / 9))
            w = r * 0.25
            d.ellipse([ox - r * 0.6, oy - r * 0.6, ox + r * 0.6, oy + r * 0.6], fill=(255, 236, 170, a // 3))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(255, 240, 180, a))
        frame.alpha_composite(ov)
        return frame
    return fx


# ------------------------------------------------------------------ build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    nL = len(L)
    w = lambda ph, k=0.0, d=None, after=0.0: _when(ctx, ph, k, d, after)   # noqa: E731

    # ---------------------------------------------------------------- beats (all from the narration)
    l0 = L[0]
    t_walk0 = max(1.0, l0.start + 0.2)                                   # Jonah steps out of his door
    t_name = w(("名叫约拿", "约拿"), d=l0.start + 3.5)                   # "名叫约拿": hop + wave
    l1 = L[1] if nL > 1 else l0
    t_l1 = l1.start
    t_god1 = w("替上帝", 0.33, d=t_l1 + 1.4)                             # "...替上帝..."
    t_say = w("传话", d=t_god1 + 0.5)                                    # "传话": speech bubble
    t_l1_end = l1.end
    l2 = L[2] if nL > 2 else l1
    t_god2 = w(("上帝对约拿", "上帝对他", "对约拿说"), d=l2.start + 0.9, after=l2.start - 0.01)
    t_light = t_god2 - 0.05                                             # the clouds part
    t_kneel = min(t_light - 0.5, max(l2.start + 0.6, t_l1_end + 0.9))   # Jonah kneels to pray
    l3 = L[3] if nL > 3 else l2
    t_call = l3.start                                                    # "约拿，" — eyes open
    t_rise = w("你起来", d=t_call + 1.0)                                 # "你起来" — he rises
    t_nin = w("尼尼微", d=t_rise + 1.2, after=l3.start - 0.01)
    t_vis = max(t_rise + 0.8, t_nin - 0.35)                              # the vision opens
    t_bad0 = w(("城里的人", "坏事", "恶行"), d=t_vis + 3.2, after=t_vis)    # the grey cloud gathers
    t_bad = w(("坏事", "恶行"), d=t_bad0 + 1.6, after=t_vis)
    t_worry = t_bad - 0.1                                                # Jonah becomes worried
    t_seen = w(("看见", "面前"), d=t_bad + 1.0, after=t_vis)              # "我都看见了": light swells
    t_me = w(("你要去", "警告", "呼喊"), d=t_seen + 1.6, after=t_vis)      # hand on chest: "me?"
    t_me = max(t_me + 0.1, t_worry + 0.8)
    t_east0 = _chunk_start(ctx, ("很远的东方", "东方"), after=t_me)        # chunk "尼尼微在很远的东方"
    if t_east0 is not None:
        t_east0 = max(t_east0, t_me + 0.8)
        t_point = max(t_east0 + 0.5, w("很远", 0.5, d=t_east0 + 1.0, after=t_me) - 0.2)
        t_fierce = w("很凶", d=None, after=t_east0)
        t_enemy = w("敌人", d=None, after=t_east0)
    else:
        t_point = None
        t_fierce = t_enemy = None
    t_uneasy = t_fierce + 0.15 if t_fierce is not None else None
    t_soldiers = t_fierce - 0.45 if t_fierce is not None else None
    t_fold = t_enemy - 0.1 if t_enemy is not None else None

    # ---------------------------------------------------------------- backdrop (static, flattened)
    sc.add("sky", V._sky_svg(), wc=0.45)
    sc.add("far_hills", V._far_hills_svg(), wc=0.8)
    mid_svg = V._mid_hills_svg()
    sc.add("mid_hills", mid_svg, seed=MID_SEED)

    # ---------------------------------------------------------------- neighbours (built here, added below)
    N_W = 5
    mom_A, girl_A = 40, 30
    # stand facing Jonah; listen (hand to chin, smiling); the girl first looks at the sheep
    mom_frames = [_doc(_shadow(MOM["x"], MOM["y"], MOM["s"]) +
                       _neighbour(MOM, dict(C.POSES["stand"]), "happy", -1, label="st")),
                  _doc(_shadow(MOM["x"], MOM["y"], MOM["s"]) +
                       _neighbour(MOM, dict(C.POSES["listen_chin"]), "happy", -1, label="li"))]
    girl_frames = [_doc(_shadow(GIRL["x"], GIRL["y"], GIRL["s"], 90) +
                        _neighbour(GIRL, dict(C.POSES["stand"]), "happy", 1, label="sr")),
                   _doc(_shadow(GIRL["x"], GIRL["y"], GIRL["s"], 90) +
                        _neighbour(GIRL, dict(C.POSES["stand"]), "happy", -1, label="sl")),
                   _doc(_shadow(GIRL["x"], GIRL["y"], GIRL["s"], 90) +
                        _neighbour(GIRL, dict(C.POSES["listen_chin"]), "happy", -1, label="li"))]
    nmom, ngirl = len(mom_frames), len(girl_frames)
    for fc in (1, -1):        # walk cycles: right (up the slope), then left (round the house corner)
        mom_frames += [_doc(_shadow(MOM["x"], MOM["y"], MOM["s"]) +
                            _neighbour(MOM, _walk_pose(k, mom_A, N_W), "happy", fc, label=f"w{fc}{k}"))
                       for k in range(2 * N_W)]
        girl_frames += [_doc(_shadow(GIRL["x"], GIRL["y"], GIRL["s"], 90) +
                             _neighbour(GIRL, _walk_pose(k, girl_A, N_W, swing=34, lift=18, drop=3), "happy", fc,
                                        label=f"w{fc}{k}"))
                        for k in range(2 * N_W)]

    t_turn_girl = max(t_walk0 + 1.8, (t_name or 4.0) - 1.2)             # the girl turns from the sheep to Jonah
    t_listen = t_say + 0.35
    t_leave = t_l1_end + 0.02                                           # as the speech bubble melts

    def walker(n, A, hold, n_std, base_events, route, t_go):
        """Frame index + motion of a neighbour: hard-switched standing poses, then a planted-foot walk along
        ``route`` (see _route: shrinking with distance up the far meadow), ending behind the front village
        house (a cut-out of its own pixels is drawn right after the figure). Returns (frame_at, motion,
        behind(t), t_gone)."""
        sx0, sy0, s0 = n["x"], n["y"], n["s"]
        smp = _route(route, sy0)
        ws = [p[3] for p in smp]
        stride = 2 * A * s0 / N_W                      # distance per drawing at relative scale 1
        n_draw = int(math.ceil(ws[-1] / stride))
        std = _sched(base_events)

        def pos(i):
            j = min(len(smp) - 1, bisect.bisect_left(ws, i * stride))
            return smp[j]

        gone = next((i for i in range(n_draw + 1) if pos(i)[1] < HOUSE_FRONT_Y and pos(i)[0] < HIDDEN_X),
                    n_draw + 1)

        def idx(t):
            return int(math.floor((t - t_go) / hold)) if t >= t_go else -1

        def fa(t):
            i = idx(t)
            if i < 0:
                return std(t)
            return float(n_std + (0 if pos(i)[4] > 0 else 2 * N_W) + (i % (2 * N_W)))

        def mot(t):
            i = idx(t)
            br = 1 + 0.011 * math.sin(2 * math.pi * (t / 2.7 + 0.3 * n_std))
            if i < 0:
                nod = 0.0
                if t_listen <= t <= t_l1_end + 0.1:
                    nod = 1.6 * max(0.0, math.sin(2 * math.pi * (t - t_listen) / 1.1))
                return Tf(dy=_hop(t, t_turn_girl if n is GIRL else -9, 7, 0.26) + _hop(t, t_listen, 5, 0.26),
                          sy=br, rot=-nod, px=sx0, py=sy0)
            if i >= gone:
                return Tf(alpha=0.0)
            x, y, k, _, _ = pos(i)
            return Tf(dx=x - sx0, dy=y - sy0, sx=k, sy=k * br, px=sx0, py=sy0)

        def behind(t):
            i = idx(t)
            return 0 <= i < gone and pos(i)[1] < HOUSE_FRONT_Y

        return fa, mot, behind, t_go + gone * hold

    # the girl skips off first, passing just behind her mother, who turns and follows her
    girl_fa, girl_m, girl_behind, t_girl_gone = walker(
        GIRL, girl_A, 0.05, ngirl, [(0, 0), (t_turn_girl, 1), (t_listen + 0.12, 2)], GIRL_ROUTE, t_leave)
    mom_fa, mom_m, mom_behind, t_mom_gone = walker(
        MOM, mom_A, 0.075, nmom, [(0, 0), (t_listen, 1)], MOM_ROUTE, t_leave + 0.45)

    hx_, hy_, hs_, hv_ = VILLAGE_HOUSE
    house_cut = _Cut(mid_svg, MID_SEED, HOUSE_BOX,
                     mask_svg=_doc(S.g(PR.house(hx_, hy_, hs_, variant=hv_), filter="wobble")))

    near_svg = V._near_ground_svg()
    sc.add("near_ground", near_svg, seed=NEAR_SEED)

    # the dashed road east draws itself from Jonah's feet outward, over the ridge and the hills to the vision
    if t_east0 is not None:
        # its first stretch lies under the subtitle band, so the reveal starts where the road comes out from
        # under it (measured with the camera of that moment) and grows fastest at first: the visible road
        # grows from the start of "尼尼微在很远的东方"
        t_tr0, t_tr1 = t_east0 + 0.05, t_east0 + 2.4
        span = TRAIL_Y[0] - TRAIL_Y[1]
        f0_box = []

        def trail_frac(t):
            if not f0_box:
                cam = sc.camera(t_tr0)
                y_band = cam.y + (SUB_TOP - 540) * cam.w / 1920
                f0_box.append(_clamp((TRAIL_Y[0] - y_band) / span, 0.0, 0.5))
            f0 = f0_box[0]
            u = 1 - (1 - M.progress(t, t_tr0, t_tr1, "linear")) ** 2
            return _clamp(f0 + (1 - f0) * u + 10 / span * u)
        sc.add("trail", _trail_svg(), wc=0.3,
               motion=lambda t: Tf(alpha=M.progress(t, t_tr0 - 0.1, t_tr0 + 0.2, "sine")),
               reveal=lambda t: {"mode": "up", "soft": 30, "frac": trail_frac(t)})

    # ---------------------------------------------------------------- sky things
    for i, (cx, cy, cw, ch, sd, v) in enumerate([(232, 132, 280, 86, 5, 5), (2150, 160, 260, 84, 6, 6),
                                                  (1700, 540, 200, 62, 8, 9)]):
        sc.add(f"cloud_small{i}", _doc(S.g(S.cloud(cx, cy, cw, ch, "#fdf6e8", seed=sd, sw=3, shade_fill="#efdcc4"),
                                           filter="wobble")), motion=M.drift(vx=v))

    # the little message light (line 1): leaves the cloud bank and drifts down to Jonah, behind the clouds first
    t_orb0, t_orb1 = t_l1 + 0.05, max(t_l1 + 1.2, t_god1 + 0.15)
    orb_ease = M.ease("inout")

    def orb_m(t):
        if t < t_orb0 or t > t_orb1 + 0.45:
            return Tf(alpha=0.0)
        u = orb_ease(_clamp((t - t_orb0) / (t_orb1 - t_orb0)))
        x, y = _orb_pos(u)
        a = M.progress(t, t_orb0, t_orb0 + 0.3, "sine")
        s = 1 + 0.08 * math.sin(2 * math.pi * t / 0.7)
        if t > t_orb1:                                  # it flares softly and melts into him
            v = (t - t_orb1) / 0.45
            s *= 1 + 0.6 * v
            a *= 1 - v
        return Tf(dx=x - ORB0[0], dy=y - ORB0[1], sx=s, sy=s, alpha=a, px=ORB0[0], py=ORB0[1])
    sc.add("orb", _orb_svg(), wc=0, motion=orb_m)

    # heavenly glow + the parting cloud bank (v1)
    pulse = lambda t, lo: lo + (1 - lo) * (0.5 + 0.5 * math.sin(2 * math.pi * (t - t_light) / 2.4 - 1.2))  # noqa
    g_lines = [ln for ln in L if ln.speaker == "G"]
    t_god_end = g_lines[-1].end if g_lines and g_lines[-1] is not L[-1] else T + 5   # God has finished speaking
    after = lambda t: 1 - 0.3 * M.progress(t, t_god_end + 0.3, t_god_end + 2.3, "sine")  # noqa
    swell = lambda t: math.sin(math.pi * _clamp((t - t_seen) / 1.8)) ** 2 if t_seen <= t <= t_seen + 1.8 else 0.0  # noqa
    glow_alpha = lambda t: min(1.0, M.progress(t, t_light, t_light + 0.7, "sine") * pulse(t, 0.82) * after(t) + 0.2 * swell(t))  # noqa
    sc.add("glow", V._glow_svg(), wc=0, motion=lambda t: Tf(alpha=glow_alpha(t), sx=1 + 0.14 * swell(t),
                                                          sy=1 + 0.14 * swell(t), px=GAP[0], py=GAP[1]))
    for name, circles, d0, d1 in [("cloudL", V.LEFT_CL, 70, -200), ("cloudR", V.RIGHT_CL, -70, 150)]:
        frames = [_doc(V._cloud_bank(circles, g, name)) for g in (0.0, 1.0)]
        mv = M.combine(M.keys([(0, {"dx": d0}), (t_light, {"dx": d0}), (t_light + 1.3, {"dx": d1})], "inout"),
                       M.drift(vx=2.5), M.bob(4, 6.0, 0.3 if d1 > 0 else 0.0))
        sc.add(name, frames, motion=mv, wc=0.7,
               frame_at=lambda t: M.progress(t, t_light + 0.15, t_light + 1.1, "sine"))

    # ---------------------------------------------------------------- Jonah's house (in front of the sky)
    sc.add("house", _house_svg())

    # ---------------------------------------------------------------- the vision in the eastern sky (v1 art)
    # it closes gently (fade + slight shrink) once the last line is spoken, so it is nearly gone when the
    # 1.0 s dissolve into s03 begins and never ghosts over s03's signposts and sky (gloom, grey cloud and
    # soldiers all ride on ``vis`` and close with it)
    t_vis_c0 = max(t_vis + 2.0, min(L[-1].end, T - 1.4))
    t_vis_c1 = max(t_vis_c0 + 0.3, T - 0.8)
    vis = M.combine(
        M.keys([(t_vis, {"s": 0.18, "dx": -330, "dy": 60}), (t_vis + 0.95, {"s": 1.0, "dx": 0, "dy": 0})], "back",
               pivot=(BX, BY)),
        M.keys([(t_vis, {"alpha": 0}), (t_vis + 0.45, {"alpha": 1})], "sine"),
        M.keys([(t_vis_c0, {"alpha": 1, "s": 1.0}), (t_vis_c1, {"alpha": 0, "s": 0.9})], "sine"),
        lambda t: Tf(dy=5 * math.sin(2 * math.pi * (t - t_vis - 0.95) / 4.6)) if t > t_vis + 0.95 else Tf())
    sc.add("vision", V._bubble_svg(), motion=vis, wc=0.7)
    darker = (lambda t: 1.0 + 0.36 * M.progress(t, t_soldiers, t_soldiers + 1.0, "sine")) if t_soldiers else (lambda t: 1.0)  # noqa
    sc.add("gloom", V._gloom_svg(), wc=0, motion=M.combine(
        vis, lambda t: Tf(alpha=min(1.0, 0.74 * M.progress(t, t_bad0, t_bad0 + 1.6, "sine") * darker(t)))))
    sc.add("grey_cloud", V._grey_cloud_svg(), motion=M.combine(
        vis, M.keys([(t_bad0, {"alpha": 0, "dy": 26}), (t_bad0 + 1.4, {"alpha": 1, "dy": 0})], "out"),
        lambda t: Tf(dx=6 * math.sin(2 * math.pi * t / 5.0))), wc=0.6)
    if t_soldiers is not None:
        # 15 drawings at 1/25 s: each soldier rises over 8 drawings (eased in and out), staggered by 3
        steps, sol_hold = 15, 0.04
        sol_frames = []
        for i in range(1, steps + 1):
            rises = [M.ease("sine")(_clamp((i - d) / 8.0)) for d in (0, 3.0, 6.0)]
            rises = [rises[0], rises[2], rises[1]]           # left, then right, then the middle one
            sol_frames.append(_soldiers_svg(rises))
        sc.add("soldiers", sol_frames, wc=0.6, motion=M.combine(
            vis, lambda t: Tf(alpha=1.0 if t >= t_soldiers else 0.0)),
            frame_at=lambda t: float(min(steps - 1, max(0, int((t - t_soldiers) / sol_hold)))))

    sc.add("smoke", V._smoke_svg(), wc=0, motion=M.combine(
        M.sway(3.0, 4.2, pivot=(1252, 812)), M.pulse(0.6, 1.0, 3.1),
        M.keys([(0, {"sy": 0.96}), (T, {"sy": 1.06})], "linear", pivot=(1252, 812))))

    # ---------------------------------------------------------------- the neighbours (each followed by the
    # near-ground cut-out that hides them once they are over the crest)
    # standing, the girl (nearer) is in front of her mother; walking, she is ahead of her (farther away), so
    # her walk drawings go behind the mother. The swap happens on her first walk drawing (a hard pose change).
    sc.add("girl_walk", girl_frames[ngirl:], frame_at=lambda t: max(0.0, girl_fa(t) - ngirl),
           motion=lambda t: girl_m(t) if t >= t_leave else Tf(alpha=0.0), seed=301)
    sc.add_dynamic("girl_cut", lambda t: house_cut.image() if girl_behind(t) else None)
    sc.add("mom", mom_frames, frame_at=mom_fa, motion=mom_m, seed=303)
    sc.add_dynamic("mom_cut", lambda t: house_cut.image() if mom_behind(t) else None)
    sc.add("girl", girl_frames[:ngirl], frame_at=lambda t: min(float(ngirl - 1), girl_fa(t)),
           motion=lambda t: girl_m(t) if t < t_leave else Tf(alpha=0.0), seed=301)

    # ---------------------------------------------------------------- sheep (v1): planted hooves, turning heads
    # the sheep bleats in the narrator's first pause (after "很久很久以前，"), not on the words
    t_bleat = w("很久很久以前", 1.0, d=t_walk0 + 1.2) + 0.06
    def head_angle(i):
        if i == 0:
            return lambda t: 11 * (M.progress(t, t_bleat - 0.2, t_bleat + 0.05, "out") -
                                   M.progress(t, t_bleat + 0.95, t_bleat + 1.3, "inout"))
        if i == 1:
            return lambda t: -7 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 2.9 - 1.3))
        return lambda t: 4 * math.sin(2 * math.pi * t / 4.4 + 0.6)

    for i, (x, y, s, f) in enumerate(V.SHEEP):
        body, head = V._sheep_parts(x, y, s, f)
        br = M.breathe(0.012, 2.6 + 0.3 * i, pivot=(x, y), phase=0.3 * i)
        sc.add(f"sheep{i}", _doc(C.ground_shadow(x, y, s, width=180, opacity=0.2) + body), motion=br)
        if head:
            nx, ny = PR.local_to_stage(x, y, s, f, *V.SHEEP_NECK)
            ang = head_angle(i)
            sc.add(f"sheep{i}_head", _doc(head), motion=lambda t, ang=ang, br=br, f=f, ny=ny, nx=nx, y=y: Tf(
                dy=-(br(t).sy - 1) * (y - ny), rot=-ang(t) * f, px=nx, py=ny))

    # a butterfly flutters over the meadow the whole time (wing flipbook, wandering path)
    sc.add("butterfly", [_butterfly_svg(k) for k in (1.0, 0.55, 0.15)], wc=0.4, motion=_butterfly_motion,
           frame_at=lambda t: float((0, 1, 2, 1)[int(t * 14) % 4]))

    # ---------------------------------------------------------------- golden rays behind Jonah (v1)
    rays_alpha = lambda t: min(1.0, M.progress(t, t_light + 0.05, t_light + 0.65, "sine") * pulse(t, 0.75) * after(t) + 0.2 * swell(t))  # noqa
    sc.add("rays", V._rays_svg(), wc=0, motion=lambda t: Tf(alpha=rays_alpha(t)),
           reveal=lambda t: {"mode": "down", "frac": M.progress(t, t_light + 0.05, t_light + 0.85, "out"), "soft": 160})

    # ---------------------------------------------------------------- neighbours in front of the ridge

    # ---------------------------------------------------------------- Jonah walking out of his door
    # planted-foot walk: 7 drawings per step (14 per cycle), each held exactly 2 frames (even timing at 30 fps),
    # so the leg spread, robe hem and head bob change in small even steps. The drawings sit half a drawing off
    # the contacts, so the middle drawing of every step is the passing position (feet together under the body,
    # swing foot lifted): the walk starts on it out of the doorway stand and would end on it at his spot, whole
    # steps later, so neither end jumps between a wide stride and the stand. At his spot that last passing
    # drawing is replaced by a stop drawing (see STOP below) that eases him into the front-facing stand.
    A_J, N_J = 40.0, 7
    NW_J = 2 * N_J                                                       # walk drawings per cycle
    K0_J = (N_J - 1) // 2                                                # the passing drawing of the first step
    dist = math.hypot(JX - DOOR[0], JY - DOOR[1])
    n_draw = int(round(dist / (2 * A_J * JS / N_J) / N_J)) * N_J        # whole steps, passing to passing
    A_J = (JX - DOOR[0]) * N_J / (2 * JS * n_draw)                      # ankle travel is horizontal
    fall_j = (JY - DOOR[1]) / (n_draw / N_J) / JS                        # the path runs a little downstage
    hold_j = 2.0 / ctx.fps
    t_arrive = t_walk0 + n_draw * hold_j
    # he stops on an in-between drawing at his spot (in place of the last passing drawing, held 3 frames), half
    # way from the last walk drawing to the front-facing stand: the swing (near) foot comes down where the
    # stand has it, the planted (far) foot eases half way to its stand spot, torso tilt and hip drop are small,
    # the arms hang nearly at his sides. It splits the head move (~7 px forward, then ~3 px back, ~4 px up each
    # time) and the growth of the robe outline into two small steps; the jonah layer's stand takes over at t_stop.
    t_stop = t_arrive + 3.0 / ctx.fps
    walk_frames = [_doc(_shadow(DOOR[0], DOOR[1], JS) +
                        _jfig(DOOR[0], DOOR[1], JS, _walk_pose(k, A_J, N_J, off=0.5, fall=fall_j), "happy", f"jw{k}"))
                   for k in range(NW_J)]
    walk_frames.append(_doc(_shadow(DOOR[0], DOOR[1], JS) + C.jonah(DOOR[0], DOOR[1], JS, 1, expr="happy")))
    walk_frames.append(_doc(_shadow(DOOR[0], DOOR[1], JS) + C.jonah(DOOR[0], DOOR[1], JS, 1, expr="peaceful")))
    STOP = C._P(t=1.5, h=-1.5, drop=3, legs=(("ik", 0.2 * A_J, 1), ("ik", -0.4 * A_J, 1)),
                arms=(("fk", 8, 7), ("fk", 2, 10)))
    walk_frames.append(_doc(_shadow(DOOR[0], DOOR[1], JS) + _jfig(DOOR[0], DOOR[1], JS, STOP, "happy", "jstop")))

    def jw_i(t):
        return int(math.floor((t - t_walk0) / hold_j + 1e-6))

    def jw_fa(t):
        if t < t_walk0:
            return float(NW_J + 1) if 0.55 <= t <= 0.68 else float(NW_J)     # a blink in the doorway
        if t >= t_arrive - 1e-6:
            return float(NW_J + 2)                                           # the stop drawing
        return float((K0_J + min(jw_i(t), n_draw)) % NW_J)

    def jw_m(t):
        if t >= t_stop - 1e-6:
            return Tf(alpha=0.0)
        br = 1 + 0.008 * math.sin(2 * math.pi * t / 3.2)
        if t < t_walk0:
            return Tf(sy=br, px=DOOR[0], py=DOOR[1])
        i = min(jw_i(t), n_draw)
        u = i / n_draw
        return Tf(dx=(JX - DOOR[0]) * u, dy=(JY - DOOR[1]) * u)
    sc.add("jonah_walk", walk_frames, frame_at=jw_fa, motion=jw_m, seed=211)

    # ---------------------------------------------------------------- Jonah at his spot: hard-switched poses
    def jdoc(body, sw=120):
        return _doc(_shadow(JX, JY, JS, sw) + body)
    J = {}
    jf = []

    def addf(key, svg):
        J[key] = len(jf)
        jf.append(svg)
    addf("stand", jdoc(C.jonah(JX, JY, JS, 1)))
    addf("blink", jdoc(C.jonah(JX, JY, JS, 1, expr="peaceful")))
    addf("happy", jdoc(C.jonah(JX, JY, JS, 1, expr="happy")))
    addf("wave_a", jdoc(_jfig(JX, JY, JS, WAVE_A, "happy", "wa")))
    addf("wave_b", jdoc(_jfig(JX, JY, JS, WAVE_B, "happy", "wb")))
    addf("listen_h", jdoc(C.jonah(JX, JY, JS, 1, pose="listen", expr="happy")))
    addf("preach", jdoc(_jfig(JX, JY, JS, EXPLAIN, "call", "explain")))
    addf("kneel", jdoc(C.jonah(JX, JY, JS, 1, pose="kneel_pray"), 200))
    addf("kneel_s", jdoc(C.jonah(JX, JY, JS, 1, pose="kneel_pray", expr="surprised"), 200))
    addf("rise", jdoc(_jfig(JX, JY, JS, RISE, "surprised", "rise"), 170))
    addf("rise_n", jdoc(_jfig(JX, JY, JS, RISE, "peaceful", "rise_n"), 170))
    addf("listen_s", jdoc(C.jonah(JX, JY, JS, 1, pose="listen", expr="surprised")))
    addf("look_s", jdoc(_jfig(JX, JY, JS, LOOK, "surprised", "look_s")))
    addf("look_s_b", jdoc(_jfig(JX, JY, JS, LOOK, "s02_blink_surprised", "look_s_b")))
    addf("look_w", jdoc(_jfig(JX, JY, JS, LOOK, "worried", "look_w", marks=False)))
    addf("look_w_b", jdoc(_jfig(JX, JY, JS, LOOK, "s02_blink_worried", "look_w_b", marks=False)))
    addf("confess", jdoc(C.jonah(JX, JY, JS, 1, pose="confess", expr="worried")))
    addf("confess_b", jdoc(C.jonah(JX, JY, JS, 1, pose="confess", expr="s02_blink_worried")))
    addf("point", jdoc(_jfig(JX, JY, JS, POINT_UP, "worried", "point_up")))
    addf("uneasy", jdoc(_jfig(JX, JY, JS, UNEASY, "worried", "uneasy")))
    addf("uneasy_b", jdoc(_jfig(JX, JY, JS, UNEASY, "s02_blink_worried", "uneasy_b")))
    addf("crossed", jdoc(_jfig(JX, JY, JS, CROSSED, "angry", "crossed")))
    addf("crossed_b", jdoc(_jfig(JX, JY, JS, CROSSED, "s02_blink_angry", "crossed_b")))

    ev = [(0.0, J["stand"]), (t_stop - 1e-6, J["happy"]), (t_arrive + 0.75, J["blink"]),   # keeps the walk's smile
          (t_arrive + 0.88, J["happy"])]
    hops = []        # (t, height) little hops that sell a switch
    squashes = []    # (t, k) landing squashes
    if t_name is not None:
        tw = t_name + 0.05
        ev += [(tw, J["wave_a"]), (tw + 0.24, J["wave_b"]), (tw + 0.48, J["wave_a"]), (tw + 0.72, J["wave_b"]),
               (tw + 0.96, J["wave_a"]), (tw + 1.2, J["happy"])]
        hops.append((tw, 12))
        squashes.append((tw + 1.2, 0.025))
    t_look = t_orb1 - 0.55
    t_gaze = min(t_vis + 1.2, t_worry - 0.6)          # he turns his face up toward the vision once it has landed
    ev += [(t_look - 0.9, J["blink"]), (t_look - 0.77, J["happy"]), (t_look, J["listen_h"]),
           (t_say - 0.05, J["preach"]), (t_l1_end + 0.1, J["happy"]),
           (t_kneel - 0.14, J["rise_n"]), (t_kneel, J["kneel"]),
           (t_call + 0.05, J["kneel_s"]),
           (t_rise, J["rise"]), (t_rise + 0.2, J["listen_s"]),
           (t_gaze, J["look_s"]), (t_worry, J["look_w"]), (t_me, J["confess"])]
    hops += [(t_look, 8), (t_say - 0.05, 10), (t_rise + 0.2, 16)]
    squashes += [(t_l1_end + 0.1, 0.02), (t_kneel, 0.05), (t_call + 0.05, 0.03), (t_gaze, 0.02), (t_worry, 0.03),
                 (t_me, 0.035)]
    holds = [(t_gaze, t_worry, "look_s"), (t_worry, t_me, "look_w")]
    t_end_conf = t_point if t_point is not None else T
    holds.append((t_me, t_end_conf, "confess"))
    if t_point is not None:
        ev += [(t_point, J["point"])]
        hops.append((t_point, 9))
    if t_uneasy is not None:                          # "很凶": arm drops, uneasy (no fear, no step back)
        ev += [(t_uneasy, J["uneasy"])]
        squashes.append((t_uneasy, 0.03))
        holds.append((t_uneasy, t_fold if t_fold is not None else T, "uneasy"))
    if t_fold is not None:                            # "敌人": arms folded, grumpy, eyes away; held to the end
        ev += [(t_fold, J["crossed"])]
        squashes.append((t_fold, 0.04))
        holds.append((t_fold, T - 1.05, "crossed"))
    # blinks (0.13 s) in the long holds: one every ~1.6-2 s, never within 0.5 s of a pose change
    for a_, b_, key in holds:
        n_bl = int((b_ - a_ - 0.8) / 1.5)
        if b_ - a_ >= 1.25:
            n_bl = max(1, n_bl)
        for j_ in range(n_bl):
            tb = a_ + (b_ - a_) * (j_ + 1) / (n_bl + 1) + (0.15 if j_ % 2 else -0.1)
            tb = min(max(tb, a_ + 0.55), b_ - 0.6)
            ev += [(tb, J[key + "_b"]), (tb + 0.13, J[key])]
    j_fa = _sched(ev)

    def j_m(t):
        if t < t_stop - 1e-6:
            return Tf(alpha=0.0)
        sx = sy = 1.0
        for ts, k in squashes:
            a, b = _squash(t, ts, k)
            sx, sy = sx * a, sy * b
        if t_stop - 1e-6 <= t <= t_stop + 0.5:      # settle after the walk (light: the stop drawing has eased
            a, b = _squash(t, t_stop - 1e-6, 0.015)   # him in, so a deeper dip would read as a rise-and-dip bob)
            sx, sy = sx * a, sy * b
        dy = sum(_hop(t, th, h) for th, h in hops)
        # breathing eases in after the walk (the walk drawings do not breathe), so it adds no jump on the switch
        br = 1 + 0.008 * M.progress(t, t_stop, t_stop + 0.8, "sine") * math.sin(2 * math.pi * t / 3.2)
        return Tf(dy=dy, sx=sx, sy=sy * br, px=JX, py=JY)
    sc.add("jonah", jf, frame_at=j_fa, motion=j_m, seed=213)

    # ---------------------------------------------------------------- the speech bubble with God's golden word
    t_sb0, t_sb1 = t_say + 0.05, t_l1_end + 0.02

    def sb_m(t):
        if t < t_sb0 or t > t_sb1 + 0.3:
            return Tf(alpha=0.0)
        s = M.lerp(0.15, 1.0, M.progress(t, t_sb0, t_sb0 + 0.45, "back"))
        a = M.progress(t, t_sb0, t_sb0 + 0.12, "sine")
        if t > t_sb1:
            v = M.progress(t, t_sb1, t_sb1 + 0.3, "in")
            s *= 1 - 0.5 * v
            a *= 1 - v
        return Tf(dy=3 * math.sin(2 * math.pi * t / 1.6), sx=s, sy=s, alpha=a, px=SB_TIP[0], py=SB_TIP[1])
    sc.add("speech", _speech_svg(), motion=sb_m, wc=0.5)
    sc.add("speech_star", _speech_star_svg(), wc=0.3, motion=M.combine(
        sb_m, lambda t: Tf(rot=6 * math.sin(2 * math.pi * t / 1.3))))

    # ---------------------------------------------------------------- foreground grass
    tufts = list(V.FG_TUFTS) + [(800, 1172, 0, 0.95)]
    for i, (x, y, v, s) in enumerate(tufts):
        sc.add(f"tuft{i}", V._tuft_svg(x, y, v, s), motion=M.sway(2.4 + 0.3 * (i % 3), 3.4 + 0.25 * (i % 4),
                                                                     pivot=(x, y), phase=0.17 * i))

    # ---------------------------------------------------------------- birds (v1): two doves cross the sky early,
    # one far away later; a dove on the roof turns with little hops
    glide0 = t_walk0 + 1.6
    for i, (x0, y0, s, ph, keys_) in enumerate([
            (1000, 400, 0.62, 0.0, [(0.0, {"dx": -150, "dy": 20}), (t_name or 5.0, {"dx": 520, "dy": -50}),
                                    (t_l1 + 1.6, {"dx": 1300, "dy": -720})]),
            (1000, 470, 0.52, 3.0, [(0.3, {"dx": -110, "dy": 10}), ((t_name or 5.0) + 0.2, {"dx": 380, "dy": -40}),
                                    (t_l1 + 1.8, {"dx": 1100, "dy": -740})]),
            (2200, 770, 0.34, 1.5, [(t_bad0, {"dx": 300, "dy": 0}), (T, {"dx": -560, "dy": -30})])]):
        facing = 1 if i < 2 else -1
        sc.add(f"dove{i}", V._dove_frames(x0, y0, s, facing),
               motion=M.combine(M.keys(keys_, ["linear", "in"]), M.bob(14, 1.3, ph / 8)),
               frame_at=V._flap(9.0 if i < 2 else 7.0, ph,
                                glide=(glide0 + i * 0.4, glide0 + 1.0 + i * 0.4) if i < 2 else None),
               wc=0.6)
    rx_, ry_ = V._hp(585, 497)
    pd = [_doc(PR.dove(rx_, ry_, 0.6, f, pose="stand")) for f in (1, -1)]
    roof_hops = [x for x in [t_walk0 + 1.4, (t_name or 5) + 0.9, t_light + 0.7, t_vis + 1.4, t_bad + 2.0,
                             t_me + 1.6, (t_fierce or T + 5) + 0.3] if x < T - 1.2]
    hop_keys = [(0, {"dy": 0})]
    for h in roof_hops:
        hop_keys += [(h, {"dy": 0}), (h + 0.14, {"dy": -16}), (h + 0.3, {"dy": 0})]
    sc.add("dove_roof", pd, wc=0.6, frame_at=lambda t: float(sum(t >= h + 0.12 for h in roof_hops) % 2),
           motion=M.keys(hop_keys, "sine"))

    # warm golden light over everything once the light comes (additive)
    warm_alpha = lambda t: min(0.75, 0.5 * M.progress(t, t_light + 0.15, t_light + 1.1, "sine") * pulse(t, 0.7) * after(t) + 0.3 * swell(t))  # noqa
    sc.add("warm", V._warm_svg(), wc=0, blend="add", motion=lambda t: Tf(alpha=warm_alpha(t)))

    # ---------------------------------------------------------------- camera
    keys_ = [(0.0, Cam(1200, 690, 2340)),
             (t_arrive + 0.4, Cam(1095, 712, 2010)),
             (t_l1 - 0.1, Cam(1082, 700, 1960)),
             (t_kneel - 0.4, Cam(1078, 694, 1950)),
             (t_light + 1.1, Cam(1050, 652, 2000)),
             (t_vis - 0.2, Cam(1062, 650, 2020)),
             (t_vis + 1.4, Cam(1165, 650, 1930)),
             (max(t_vis + 1.5, (t_east0 or T) - 0.6), Cam(1158, 652, 1890))]
    if t_east0 is not None:
        keys_ += [(t_east0 + 2.4, Cam(1220, 660, 2120)),
                  (max(t_east0 + 2.5, (t_fierce or T) + 0.4), Cam(1218, 659, 2112)),
                  (T, Cam(1200, 652, 2040))]
    else:
        keys_ += [(T, Cam(1160, 646, 1900))]
    sc.camera = M.cam_keys(keys_, "sine")

    # ---------------------------------------------------------------- effects
    sc.fx = [
        FX.motes((0, 300, SW, 1200), count=26, color=(255, 246, 214), size=(3, 6), alpha=110),
        _orb_trail(t_orb0, t_orb1, orb_ease),
        FX.sparkles((ORB1[0] - 90, ORB1[1] - 80, ORB1[0] + 90, ORB1[1] + 60), count=10, t0=t_orb1 - 0.1,
                    t1=t_orb1 + 0.9, color=(255, 238, 170), size=(7, 14), period=0.9, drift=-10, seed=17),
        # God-light sparkles in the beam: never over Jonah's head (head box x 850-1060, y 715-935 incl. the
        # kneel, the hops and the hand-to-ear pose; a star reaches 18 stage px; the drift is upward), so they
        # fill the beam above him and beside his body. Keep the head column x 825-1085 free and the top set's
        # lower edge at or above y 690 if Jonah's poses or spot change. The right set's seed is one whose stars
        # also stay off his raised pointing hand (checked against his drawn figure at every frame).
        FX.sparkles((825, GAP[1] + 150, 1085, 690), count=6, t0=t_light + 0.3,              # above his head
                    color=(255, 238, 170), size=(8, 18), period=1.7, drift=-6, seed=21),
        FX.sparkles((GAP[0] - 300, GAP[1] + 150, 825, JY - 60), count=7, t0=t_light + 0.3,   # left of him
                    color=(255, 238, 170), size=(8, 18), period=1.7, drift=-6, seed=22),
        FX.sparkles((1085, GAP[1] + 150, GAP[0] + 330, JY - 60), count=13, t0=t_light + 0.3,  # right of him
                    color=(255, 238, 170), size=(8, 18), period=1.7, drift=-6, seed=37),
        FX.sparkles((BX - RX - 80, BY - RY - 60, BX + RX + 80, BY + RY + 60), count=16, t0=t_vis + 0.3,
                    t1=t_vis + 2.6, color=(255, 240, 180), size=(9, 20), period=1.2, drift=0, seed=31),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T + 0.8, gain_db=-14, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", t_walk0, dur=t_arrive - t_walk0 + 0.1, gain_db=-17, pan=-0.2)
    sc.sfx("sheep", t_bleat, gain_db=-19, pan=0.35)
    sc.sfx("sparkle", t_orb1 - 0.1, gain_db=-13)
    sc.sfx("pop", t_sb0, gain_db=-12, pan=0.15)
    sc.sfx("footsteps", t_leave, dur=max(1.0, t_mom_gone - t_leave - 0.3), gain_db=-23, pan=0.3)
    sc.sfx("cloth", t_kneel, gain_db=-14)
    sc.sfx("chime", t_light - 0.15, gain_db=-9)          # starts in the pause before "上帝对约拿说"
    sc.sfx("cloth", t_rise, gain_db=-15)
    sc.sfx("sparkle", t_vis + 0.1, gain_db=-10, pan=0.5)
    sc.sfx("chime", t_seen, gain_db=-15)
    if t_soldiers is not None:
        sc.sfx("thud", t_soldiers + 0.25, gain_db=-14, pan=0.5)
    return sc
