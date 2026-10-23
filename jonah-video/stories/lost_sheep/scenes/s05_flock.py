"""Scene 5 - Jesus's story begins (Luke 15:4). A bright spring morning on a wide hillside: mint and sage hills, a
stream, buttercups and poppies, round clouds drifting. The shepherd of the parable leads his sheep, pats one and
smiles; the camera pulls back to show the whole flock of a hundred filling the hillside; he leads them down to the
stream to graze. One little lamb (curl, tiny bell) nibbles, steps away bit by bit, sniffs a poppy, chases a butterfly
over a grassy rise - and looks up: everyone is gone.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Storm film's
Beats class; nothing hard-coded to the take):
  0 .. 0.9      calm spring morning (the page turns in over it): the shepherd stands with two sheep, clouds drift,
                butterflies flutter, the flock nibbles
  '耶稣'         he sets off leading (crook pointing the way, the far hand waving 'come along', planted strides), the
                two sheep trot after him in little hops; '牧羊人' he arrives
  '他有一百只羊'  he waves to his flock
  '每一只'       he bends down to a sheep that looks up at him; '很' / '爱' two gentle pats, a little heart pops on '爱'
                (baa); the camera has eased in on him
  '一百只羊'     the camera pulls back over '好多好多' to the whole hillside: a hundred sheep fill the hills (baas)
  '每天早上'     the sun glints; '牧羊人' he leads them on toward the stream (planted strides, the sheep hop after
                him); '吃青草' they stop by the water and graze
  '有一只小羊'   the camera finds the little lamb at the edge of the flock; on '小羊' it lifts its head (bell)
  '吃着'         it nibbles; '走着走着' two little steps on each '走'; '越走越远' it trots on and on toward a rise
  '闻闻'         it sniffs a poppy where a yellow butterfly sits; '追' the butterfly flutters up, on the second '追' the
                lamb bounds after it, up and over the grassy rise
  '一抬头'       it lands, lifts its head, the butterfly flies away up; '咦' big worried eyes (bell); '大家' it looks
                back over its shoulder: nobody; '不见了' it turns forward again, alone on the empty slope
  end           calm hold; s06 opens on exactly this frame at sunset (a plain fade = a time-lapse to evening)

Shared with s06_count / s07_alone: the stage (W5 x H5), the hills, the flock, the knoll, the clouds, the lamb's last
pose and the figure helpers below.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import heart_markup, snap
from stories.storm.scenes.s03_friends import Beats

INK = P["ink"]

# ------------------------------------------------------------------ stage (shared with s06 / s07)
W5, H5 = 4300, 1700
GY = 1160                    # spring_hills near ground line
HS = 1.45                    # hills scale
HX0, HX1 = -60, W5 + 60
HSEED = 2
STREAM_X = 520
SKY_Y1 = 980                 # bottom of the sky box (hidden behind the hills)
YS = 1400                    # the shepherd's ground line
YL = 1432                    # the little lamb's ground line
REF = 60.0                   # global-clock origin for drifting clouds (continuous across s05 -> s06)

# the grassy rise the lamb bounds over: a soft mound in the foreground, its ridge crossing the lamb's line at KX0 / KX1
KC, KHW, KYT, KYBOT = 3140, 780, 1336, H5 + 90

# the lamb's journey
LX0 = 2330                   # grazing at the edge of the flock
X_SNIFF = 2690               # sniffs the poppy here
X_LAND = 3470                # lands beyond the rise; stays here to the end (and at the start of s06)

# the shepherd (s05)
X_START, X_PAT, X_STREAM = 2240, 1660, 1170

CAM_END = Cam(3420, 1236, 1420)    # s05's last frame = s06's first frame


def persp(y):
    """Figure scale for a figure standing on stage line y (1.0 on the shepherd's line)."""
    return 1.0 + (y - YS) * 0.75 / 650.0


K = persp(YS)
KL = persp(YL)


def doc(body, defs=""):
    return S.svg_doc(body, defs, W5, H5)


def f1(v):
    return f"{v:.1f}"


def clamp01(v):
    return max(0.0, min(1.0, v))


# ------------------------------------------------------------------ timing / motion helpers
def env(t, t0, t1, fin=0.4, fout=0.4):
    """0 -> 1 -> 0 envelope."""
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def clamp_cam(c, w=W5, h=H5):
    cw = min(c.w, w, h * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), w - cw / 2 - 1), min(max(c.y, ch / 2 + 1), h - ch / 2 - 1), cw, c.rot)


def cam_path(keys, curves, w=W5, h=H5):
    f = M.cam_keys([(t, clamp_cam(c, w, h)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), w, h)


def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def breath(piv, g0, period=3.0, amount=0.012, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start), so neighbouring scenes breathe in step."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def gate(t0=-1e9, t1=1e9):
    """Visible only in [t0, t1) (hard cuts)."""
    return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)


def pop_motion(t0, piv, dur=0.45, t1=None, out=0.4, rise=0.0):
    """Scale-pop in at t0 (and fade out at t1), optionally drifting up ``rise`` px over its life."""
    def m(t):
        if t < t0:
            return Tf(alpha=0.0)
        u = M.progress(t, t0, t0 + dur, "back")
        a = M.progress(t, t0, t0 + dur * 0.6, "sine")
        if t1 is not None:
            a *= 1 - M.progress(t, t1 - out, t1, "sine")
        s = 0.3 + 0.7 * u
        dy = -rise * M.progress(t, t0, t1 if t1 is not None else t0 + 2.0, "out")
        return Tf(alpha=a, sx=s, sy=s, dy=dy, px=piv[0], py=piv[1])
    return m


# blink variants of the expressions used here (closed eyes, same mouth / brows)
for _e in ("warm", "happy", "kind", "worried", "determined", "puzzled", "joyful"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"ls5_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"ls5_blink_{expr}"


def tint_filter(time, k=0.85):
    """(defs, filter id) tinting a character toward the spring world's light at ``time`` exactly like the props do
    (PR._lt: a mix toward the time's tint colour); None when there is no tint (day)."""
    col, a = PR._ls_pal(time)["tint"]
    a *= k
    if a <= 0.002:
        return "", None
    r, g, b = (c / 255.0 for c in S.hex_rgb(col))
    fid = f"lstint{int(round(a * 1000))}{col[1:]}"
    vals = (f"{1 - a:.4f} 0 0 0 {a * r:.4f} 0 {1 - a:.4f} 0 0 {a * g:.4f} 0 0 {1 - a:.4f} 0 {a * b:.4f} "
            f"0 0 0 1 0")
    return (f'<filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">'
            f'<feColorMatrix type="matrix" values="{vals}"/></filter>'), fid


def tinted(markup, time, k=0.85):
    """(body, defs): the markup wrapped in the time-of-day tint."""
    defs, fid = tint_filter(time, k)
    if fid is None:
        return markup, ""
    return f'<g filter="url(#{fid})">{markup}</g>', defs


class Fig:
    """One figure on its own flipbook layer. States are hashable keys, ``draw(state)`` -> markup or (markup, defs).
    ``cut`` switches state with a hard cut, hidden in a squash dip unless dip=False. ``loops[state] = (n, fn)`` gives a
    state n sub-frames chosen by fn(t) -> int (``draw(state, k)``). ``pivot(state)`` is where the state's drawing
    stands (squash / rotation pivot; default the anchor); motions in ``mots`` return Tf whose dx / dy / rot / sx / sy /
    alpha are combined about that pivot."""

    def __init__(self, name, draw, anchor, s, z, g0, seed=0, docf=doc, loops=None, pivot=None):
        self.name, self.draw, self.anchor, self.s, self.z, self.g0 = name, draw, anchor, s, z, g0
        self.seed, self.docf = seed, docf
        self.loops = loops or {}
        self.pivot = pivot
        self.ents, self.dips, self.mots = [], [], []

    def cut(self, t, state, dip=True, depth=7.0):
        t = snap(t) if t > 0 else 0.0
        self.ents.append((t, state))
        if dip and t > 0:
            self.dips.append((t, depth))
        return self

    def state_at(self, t):
        cur = None
        for tk, n in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = n
        return cur

    def add_blinks(self, pairs, t_from, t_to, rng, every=(2.4, 4.2)):
        """pairs: {state: closed-eye state}: 0.13 s blinks where no other cut is within 0.35 s."""
        t = t_from + rng.uniform(0.3, 1.4)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.3:
            cur = self.state_at(t)
            if cur in pairs and all(abs(t - tk) > 0.35 for tk in cut_ts):
                self.ents += [(snap(t), pairs[cur]), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def _doc(self, res):
        if isinstance(res, tuple):
            return self.docf(*res)
        return self.docf(res)

    def build(self, sc, wc=1.0):
        ents = sorted(self.ents, key=lambda e: e[0])
        names = []
        for _, n in ents:
            if n not in names:
                names.append(n)
        frames, index = [], {}
        for n in names:
            nl = self.loops[n][0] if n in self.loops else 1
            for k in range(nl):
                index[(n, k)] = len(frames)
                frames.append(self._doc(self.draw(n, k) if n in self.loops else self.draw(n)))
        loops = self.loops
        times = [tk for tk, _ in ents]

        def cur_state(t):
            cur = ents[0][1]
            for tk, n in ents:
                if t >= tk:
                    cur = n
                else:
                    break
            return cur

        def fa(t):
            cur = cur_state(t)
            if cur in loops:
                nl, fn = loops[cur]
                return float(index[(cur, int(fn(t)) % nl)])
            return float(index[(cur, 0)])
        sq = [squash(td, self.s, (0, 0), depth) for td, depth in self.dips]
        mots = list(self.mots)
        pivf = self.pivot
        anchor = self.anchor

        def motion(t):
            piv = pivf(cur_state(t)) if pivf else anchor
            dx = dy = rot = 0.0
            sx = sy = al = 1.0
            for m in sq + mots:
                v = m(t)
                dx += v.dx
                dy += v.dy
                rot += v.rot
                sx *= v.sx
                sy *= v.sy
                al *= v.alpha
            return Tf(dx, dy, rot, sx, sy, al, piv[0], piv[1])
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=wc, motion=motion)
        return self


def clock_loop(g0, period):
    """Sub-frame chooser on the film's global clock."""
    return lambda t: int((t + g0) / period)


# ------------------------------------------------------------------ the backdrop (time 0 day .. .35 sunset .. .62 dusk)
def sky_svg(time):
    return doc(PR.spring_sky(-10, -10, W5 + 10, SKY_Y1, time=time, clouds=0, seed=3, scale=HS))


def hills_svg(time, part):
    return doc(PR.spring_hills(HX0, HX1, GY, HS, time=time, part=part, seed=HSEED, stream_x=STREAM_X))


def hill_points():
    return PR.spring_hills_points(HX0, HX1, GY, HS, stream_x=STREAM_X, seed=HSEED)


def sun_markup(x, y, time, sc=HS, k=1.0):
    """The round storybook sun (the same drawing as spring_sky's), white-gold by day, a big orange one at sunset."""
    warm = clamp01(PR._ls_t(time) / 0.35)
    core = S.mix("#fff6cc", "#ffb066", warm)
    r = (62 + 30 * warm) * sc
    out = PR._ls_glow(x, y, r * 4.2, r * 4.2, 0.75 * k, "s5sun", "#fffbe2", S.mix("#fff0b0", "#ffb878", warm))
    out += (f'<path d="{S.rays(x, y, r * 1.25, r * 2.1, n=14, width_deg=6, rot=7)}" fill="{S.mix("#fff3c4", "#ffd090", warm)}" '
            f'opacity="{0.55 * k * (1 - 0.6 * warm):.2f}"/>')
    out += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{core}" stroke="{S.mix(INK, core, 0.55)}" '
            f'stroke-width="{f1(3.4 * sc)}" opacity="{k:.2f}"/>')
    out += f'<circle cx="{f1(x - r * 0.28)}" cy="{f1(y - r * 0.3)}" r="{f1(r * 0.32)}" fill="#fffbe8" opacity="{0.6 * k:.2f}"/>'
    return S.g(out, filter="wobble")


# clouds: (x at REF, y, width, seed, speed px/s)
CLOUDS = [(280, 300, 500, 11, 9.0), (820, 160, 400, 12, 7.0), (1330, 380, 450, 13, 10.0), (1900, 200, 540, 14, 8.0),
          (2460, 390, 420, 15, 11.0), (3000, 180, 500, 16, 8.5), (3520, 340, 460, 17, 10.0), (3980, 210, 420, 18, 9.0)]


def cloud_x(i, g):
    return CLOUDS[i][0] + CLOUDS[i][4] * (g - REF)


def cloud_svg(i, time, g0):
    """Cloud i drawn where it is at global time g0 (a scene's start), so nothing is clipped at the stage edge."""
    _, y, w, seed, _ = CLOUDS[i]
    x = cloud_x(i, g0)
    pal = PR._ls_pal(time)
    t = PR._ls_t(time)
    h = w * 0.46
    body = PR._ls_cloud(x, y, w, h, pal["cloud"], pal["cloud_sh"], pal["rim"], 0.6 * clamp01((t - 0.3) * 2), seed,
                        3.2 * HS)
    return doc(S.g(body, filter="wobble"))


def add_clouds(sc, g0, times, frame_at=None, z=0.3, gate_m=None, g_draw=None):
    """The drifting clouds (one layer each; a flipbook over ``times`` if several). Positions follow the film's global
    clock, so two scenes joined by a plain fade show them in the same place; ``g_draw`` (default g0) is the global time
    at which the drawings are placed - pass the earlier scene's g0 to reproduce its exact drawings (wobble, texture)."""
    g_draw = g0 if g_draw is None else g_draw
    for i in range(len(CLOUDS)):
        x = cloud_x(i, g_draw)
        w = CLOUDS[i][2]
        if x + w * 0.6 < 0 or x - w * 0.6 > W5:
            continue
        frames = [cloud_svg(i, tm, g_draw) for tm in times]
        v = CLOUDS[i][4]
        mot = (lambda v: lambda t: Tf(dx=v * (t + g0 - g_draw)))(v)
        if gate_m is not None:
            mot = M.combine(mot, gate_m)
        sc.add(f"cloud{i}", frames if len(frames) > 1 else frames[0], z=z + 0.001 * i, seed=300 + i, motion=mot,
               frame_at=frame_at if len(frames) > 1 else None)


# ---- the flock: on the mid hill and in the meadow (positions fixed by the seeds; poses / time vary)
FLOCK_POSES = ("graze", "graze", "graze", "stand", "graze", "look_up", "lie", "graze", "stand", "stand")
REST_POSES = ("lie", "lie", "graze", "lie", "stand", "lie", "lie", "graze", "lie", "look_up")
MID_BAND = (90, 2420, 905, 1092, 44, 21)       # x0, x1, y_far, y_near, n, seed
MEAD_BAND = (60, 2400, 1128, 1352, 56, 22)


def stream_gaps(y0, y1):
    out = []
    for x, y, w in hill_points()["stream"]:
        if y0 - 80 <= y <= y1 + 60:
            out.append((x, y, w + 70))
    # densify between the stream points
    pts = hill_points()["stream"]
    for (xa, ya, wa), (xb, yb, wb) in zip(pts, pts[1:]):
        xm, ym, wm = (xa + xb) / 2, (ya + yb) / 2, (wa + wb) / 2
        if y0 - 80 <= ym <= y1 + 60:
            out.append((xm, ym, wm + 70))
    return out


def flock_band_markup(band, time=0.0, phase=0.0, poses=FLOCK_POSES, gaps=(), on_mid=None):
    """A band of the flock (x0, x1, y_far, y_near, n, seed) with perspective scale, kept off the stream."""
    x0, x1, yf, yn, n, seed = band
    s = persp(yn)
    kf = persp(yf) / s
    if on_mid is None:
        on_mid = yn < GY - 40
    top = hill_points()["mid_top"] if on_mid else None
    g = list(stream_gaps(yf, yn)) + list(gaps)
    return PR.flock(x0, x1, yf, yn, n=n, scale=s, k_far=kf, seed=seed, phase=phase, time=time, top=top, gaps=g,
                    poses=poses)


def flock_band_svg(band, time=0.0, phase=0.0, poses=FLOCK_POSES, gaps=()):
    return doc(flock_band_markup(band, time, phase, poses, gaps))


# a lane of open grass along the shepherd's walks (the sheep stay a little behind him) and room round the lamb
MEAD_GAPS5 = ([(x, YS - 20, 150) for x in range(X_STREAM - 120, X_START + 560, 90)] +
              [(LX0, YL - 40, 190), (LX0 + 160, YL - 40, 150)])


# ---- the knoll (the rise the lamb bounds over)
def knoll_y(x):
    d = abs(x - KC) / KHW
    if d >= 1:
        return KYBOT
    b = math.cos(math.pi / 2 * d) ** 2
    return KYBOT - (KYBOT - KYT) * b


def lamb_ground(x):
    return min(YL, knoll_y(x))


def ridge_tufts(pal, seed=35, step=58):
    """Little grass tufts standing on the knoll's ridge line."""
    rng = random.Random(seed)
    col = S.mix(pal["near"], pal["dark"], 0.35)
    d = ""
    x = KC - KHW * 0.86
    while x < KC + KHW * 0.86:
        y = knoll_y(x) + 3
        h = rng.uniform(14, 24) * HS
        lean = rng.uniform(-4, 4)
        d += (f'<path d="M{f1(x - 9)},{f1(y)} Q{f1(x - 7 + lean)},{f1(y - h * 0.6)} {f1(x - 4 + lean * 1.5)},{f1(y - h)} '
              f'Q{f1(x - 1)},{f1(y - h * 0.45)} {f1(x + 1)},{f1(y)} M{f1(x)},{f1(y)} Q{f1(x + 4 + lean)},{f1(y - h * 0.7)} '
              f'{f1(x + 10 + lean * 1.3)},{f1(y - h * 0.82)} Q{f1(x + 7)},{f1(y - h * 0.35)} {f1(x + 9)},{f1(y)} Z" '
              f'fill="{col}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>')
        x += step * rng.uniform(0.7, 1.4)
    return d


def knoll_svg(time):
    return doc(*knoll_markup(time))


def knoll_markup(time):
    """(body, defs) of the grassy rise."""
    pal = PR._ls_pal(time)
    pts = [(KC - KHW + 2 * KHW * i / 60, knoll_y(KC - KHW + 2 * KHW * i / 60)) for i in range(61)]
    d = S.smooth_path(pts, closed=False) + f" L{f1(KC + KHW)},{H5 + 100} L{f1(KC - KHW)},{H5 + 100} Z"
    gid, cid, rid = "knollg", "knollc", "knollr"
    defs = (S.lin_grad(gid, [(0, S.mix(pal["near2"], pal["rim"], 0.15)), (0.3, pal["near2"]), (0.75, pal["near"]),
                             (1, S.mix(pal["near"], pal["dark"], 0.3))], y1=KYT / H5, y2=1.0) +
            f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
    defs = defs.replace(f'id="{gid}" x1="0" y1="{KYT / H5}" x2="0" y2="1.0"',
                        f'id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{KYT}" x2="0" y2="{H5}"')
    body = f'<path d="{d}" fill="url(#{gid})"/>'
    inner = PR._grass_strokes(KC - KHW, KC + KHW, KYT + 10, H5 + 40, 70, 31, S.mix(pal["near"], pal["dark"], 0.55), HS)
    inner += PR._flower_band(KC - KHW + 80, KC + KHW - 80, KYT + 26, H5 + 30, 1.1, 33, time, HS)
    body += f'<g clip-path="url(#{cid})">{inner}</g>'
    ridge = S.smooth_path(pts, closed=False)
    body += (f'<g clip-path="url(#{cid})"><path d="{ridge}" fill="none" stroke="{pal["rim"]}" stroke-width="{f1(10 * HS)}" '
             f'opacity="0.4" transform="translate(0,9)"/></g>')
    body += f'<path d="{ridge}" fill="none" stroke="{INK}" stroke-width="{f1(3.6 * HS)}" stroke-linecap="round"/>'
    body += ridge_tufts(pal)
    return S.g(body, filter="wobble"), defs


# ---- swaying flowers on the knoll's ridge and in the near meadow (3 frames)
RIDGE_FLOWERS = [(2790, "buttercup", 1.1), (2905, "daisy", 1.0), (3050, "poppy", 1.15), (3235, "buttercup", 1.1),
                 (3360, "clover", 1.0), (3480 + 95, "daisy", 1.05)]
NEAR_FLOWERS = [(140, 1655, "poppy", 1.9), (420, 1690, "buttercup", 2.0), (1240, 1680, "daisy", 1.9),
                (1890, 1665, "buttercup", 2.1), (2360, 1690, "poppy", 2.0), (3760, 1660, "buttercup", 2.0),
                (4020, 1690, "poppy", 2.1), (4220, 1650, "daisy", 1.8)]


def flowers_svg(k, time):
    return doc(flowers_markup(k, time))


def flowers_markup(k, time):
    sw = (-1.0, 0.0, 1.0)[k]
    b = ""
    for x, kind, sc in RIDGE_FLOWERS:
        b += PR.wildflower(x, knoll_y(x) + 4, sc * HS * 0.9, kind=kind, sway=0.7 * sw, time=time)
    for x, y, kind, sc in NEAR_FLOWERS:
        b += PR.wildflower(x, y, sc * HS * 0.9, kind=kind, sway=0.8 * sw, time=time)
    return b


def flower_frame(g0):
    return lambda t: float((0, 1, 2, 1)[int((t + g0) / 0.55) % 4])


def lone_tree_markup(time):
    """A big round tree on the empty slope beyond the rise (it frames the lamb's lonely last shot)."""
    return S.g(PR._round_tree(3920, GY - 6, 1.55 * HS, PR._ls_t(time), seed=7), filter="wobble")


def lone_tree_svg(time):
    return doc(lone_tree_markup(time))


# ------------------------------------------------------------------ figures
def shepherd_markup(x, y, pose, expr=None, facing=-1, phase=0.0, time=0.0, s=K, shadow=True, **kw):
    sh = C.ground_shadow(x, y, s, 150, 0.2) if shadow else ""
    body = C.parable_shepherd(x, y, s, facing, pose=pose, expr=expr, phase=phase, **kw)
    body, defs = tinted(body, time)
    return sh + body, defs


def lamb_markup(x, y, pose, phase=0.0, facing=1, eyes="open", time=0.0, s=KL, shadow=True):
    sh = C.ground_shadow(x, y, s, 105, 0.2) if shadow else ""
    return sh + PR.little_lamb(x, y, s, facing, pose=pose, phase=phase, eyes=eyes, time=time)


def sheep_markup(x, y, pose, phase=0.0, facing=1, variant=0, eyes="open", time=0.0, s=None, shadow=True):
    s = persp(y) if s is None else s
    sh = C.ground_shadow(x, y, s, 170, 0.18) if shadow else ""
    return sh + PR.cloud_sheep(x, y, s, facing, variant=variant, pose=pose, phase=phase, eyes=eyes, time=time)


def butterfly_svg(x, y, color, flap, s=1.0, rot=0.0):
    return doc(PR.spring_butterfly(x, y, s, flap=flap, color=color, rot=rot))


def question_markup(x, y, s=1.0):
    return S.g(f'<path d="M{f1(x - 9 * s)},{f1(y - 14 * s)} q0,-14 12,-14 q13,0 13,12 q0,9 -10,13 q-4,2 -4,9" '
               f'fill="none" stroke="{P["ink_soft"]}" stroke-width="{f1(4.2 * s)}" stroke-linecap="round"/>'
               f'<circle cx="{f1(x + 2 * s)}" cy="{f1(y + 18 * s)}" r="{f1(3 * s)}" fill="{P["ink_soft"]}"/>',
               filter="wobble-fine")


# ------------------------------------------------------------------ walking helpers
LEAD_ADV = 85.5              # parable_shepherd lead_a <-> lead_b planted advance (scale 1)


def planted_walk(t0, t1, x0, x1, adv, poses=("lead_a", "lead_b")):
    """Planted-foot walk from x0 to x1 between t0 and t1, one drawing per cut; the anchor advances quickly at each cut
    (the planted foot stays put between cuts). Returns ([(t, pose)], dx(t) relative to x0, t_end): at t_end the
    figure has arrived (dx = x1 - x0) and the caller switches to a drawing at x1."""
    n = max(1, round(abs(x1 - x0) / adv))
    step = (x1 - x0) / n
    per = (t1 - t0) / n
    cts = [snap(t0 + per * i) for i in range(n)]
    t_end = snap(t0 + per * n)

    def dx(t):
        x = 0.0
        for tc in cts[1:]:
            x += step * M.progress(t, tc - 0.06, tc + 0.06, "sine")
        x += step * M.progress(t, t_end - 0.12, t_end - 0.01, "sine")
        return x
    ents = [(tc, poses[i % len(poses)]) for i, tc in enumerate(cts)]
    return ents, dx, t_end


# ------------------------------------------------------------------ the little lamb (shared with s06)
def lamb_fig_draw(time=0.0):
    """Lamb states: (pose, phase, x, y, facing, eyes)."""
    def d(st, k=None):
        pose, ph, x, y, f, eyes = st
        if k is not None:
            ph = k / LAMB_LOOPS[pose]
        return lamb_markup(x, y, pose, ph, f, eyes, time)
    return d


LAMB_LOOPS = {"graze": 4, "sniff_flower": 3, "chase": 4}
LAMB_END = ("look_around", 0.0, X_LAND, YL, 1, "open")      # the lamb at the end of s05 (= the start of s06)


def sheep_fig_draw(variant, time=0.0):
    """Hero sheep states: (pose, phase, x, y, facing, eyes)."""
    def d(st, k=None):
        pose, ph, x, y, f, eyes = st
        if k is not None:
            ph = k / 5.0
        return sheep_markup(x, y, pose, ph, f, variant, eyes, time)
    return d


def follower(name, variant, x_of, t_moves, y, spots, g0, z, seed, idle, rng, T, hop_len=118.0):
    """A sheep hopping after the shepherd: x_of(t) its x along the walk (continuous), t_moves [(t0, t1, x0, x1)]; the
    hop drawing's phase follows the distance hopped (no sliding); spots: states at rest [(t, pose, facing)]."""
    s = persp(y)
    hop_k = {}
    ents = []
    for t0, t1, x0, x1 in t_moves:
        n = max(1, round(abs(x1 - x0) / (hop_len * s)))
        hop_k[(t0, t1)] = (n, x0, x1)
    fig = Fig(name, sheep_fig_draw(variant), (spots[0][3], y), s, z, g0, seed=seed,
              loops={}, pivot=lambda st: (st[2], st[3]))
    for (t, pose, f, x) in spots:
        fig.cut(t, (pose, 0.0, x, y, f, "open"), depth=4)
    for (t0, t1, x0, x1) in t_moves:
        n, _, _ = hop_k[(t0, t1)]
        f = -1 if x1 < x0 else 1
        st = ("hop", 0.0, x0, y, f, "open")

        def fn(t, t0=t0, t1=t1, n=n):
            u = clamp01((t - t0) / (t1 - t0))
            return int(min(n - 1e-6, u * n) % 1.0 * 5)
        fig.loops[st] = (5, fn)
        fig.cut(t0, st, dip=False)

    def mot(t):
        st = fig.state_at(t)
        if st is None:
            return Tf()
        for (t0, t1, x0, x1) in t_moves:
            if st[0] == "hop" and st[2] == x0 and t0 - 0.01 <= t <= t1 + 0.2:
                u = clamp01((t - t0) / (t1 - t0))
                return Tf(dx=(x1 - x0) * u)
        return Tf()
    fig.mots.append(mot)
    fig.mots.append(lambda t: Tf(sy=1 + 0.018 * math.sin(2 * math.pi * ((t + g0) / 2.3 + seed * 0.37))))
    return fig


# ------------------------------------------------------------------ the scene
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    b = Beats(ctx)
    L = ctx.lines
    rng = random.Random(5)

    # ---- beats
    t_ye = b.at(0, "耶稣的故事里")
    t_mu = b.at(0, "有一个牧羊人", 3)
    t_ta = b.at(0, "他有一百只羊")
    t_mei = b.at(0, "每一只他都很爱")
    t_hen = b.at(0, "每一只他都很爱", 5)
    t_ai = b.at(0, "每一只他都很爱", 6)
    t_yb = L[1].start
    t_hd = b.at(1, "好多好多")
    t_zhan = b.at(1, "站满了整个山坡")
    t_shan = b.at(1, "站满了整个山坡", 5)
    t_mt = b.at(2, "每天早上")
    t_mu2 = b.at(2, "牧羊人带着羊群")
    t_chi = b.at(2, "到山坡上吃青草", 4)
    t_you = b.at(3, "有一只小羊")
    t_xy = b.at(3, "有一只小羊", 3)
    t_c1 = b.at(3, "吃着吃着")
    t_c2 = b.at(3, "吃着吃着", 2)
    t_z = [b.at(3, "走着走着", k) for k in range(4)]
    t_yue = b.at(3, "越走越远")
    t_wen = b.at(4, "它闻闻小花", 1)
    t_zhui1 = b.at(4, "追追蝴蝶")
    t_zhui2 = b.at(4, "追追蝴蝶", 1)
    t_tai = b.at(4, "一抬头")
    t_yi = b.at(4, "咦")
    t_da = b.at(4, "大家都不见了")
    t_bu = b.at(4, "大家都不见了", 3)

    # ---- backdrop
    sc.add("sky", sky_svg(0.0), z=0)
    sun = (3700, 250)
    glint = lambda t: env(t, t_mt - 0.1, t_mt + 1.3, 0.3, 0.8)
    sc.add("sun", doc(sun_markup(*sun, 0.0)), z=0.2, wc=0.5, motion=lambda t: Tf(
        rot=1.2 * (t + g0) + 8 * glint(t), sx=1 + 0.07 * glint(t), sy=1 + 0.07 * glint(t), px=sun[0], py=sun[1]))
    add_clouds(sc, g0, [0.0])
    sc.add("hills_back", hills_svg(0.0, "back"), z=1)
    sc.add("hills_mid", hills_svg(0.0, "mid"), z=1.1)
    sc.add("lone_tree", lone_tree_svg(0.0), z=1.15)
    sc.add("flock_mid", [flock_band_svg(MID_BAND, 0.0, k / 4) for k in range(4)], z=1.2, seed=41,
           frame_at=lambda t: float(int((t + g0) / 0.32) % 4))
    sc.add("meadow", hills_svg(0.0, "front"), z=1.3)
    sc.add("flock_mead", [flock_band_svg(MEAD_BAND, 0.0, k / 4, gaps=MEAD_GAPS5) for k in range(4)], z=1.4,
           seed=43, frame_at=lambda t: float(int((t + g0) / 0.3 + 2) % 4))
    sc.add("knoll", knoll_svg(0.0), z=8)
    sc.add("flowers", [flowers_svg(k, 0.0) for k in range(3)], z=9, frame_at=flower_frame(g0))

    # ================================================================ the shepherd
    def shep(pose, expr, x, phase=0.0):
        return (pose, x, expr, phase)

    sh = Fig("shepherd", lambda st: shepherd_markup(st[1], YS, st[0], st[2], -1, st[3]), (X_PAT, YS), K,
             5 + YS / 1000, g0, seed=101, pivot=lambda st: (st[1], YS))
    w1_ents, w1_dx, w1_end = planted_walk(t_ye + 0.05, t_mu + 0.35, X_START, X_PAT, LEAD_ADV * K)
    sh.cut(0, shep("stand", "warm", X_START))
    for tk, p in w1_ents:
        sh.cut(tk, shep(p, "happy", X_START), dip=False)
    sh.cut(w1_end, shep("stand", "happy", X_PAT), depth=5)
    t_wave = t_ta - 0.05
    for k in range(4):
        sh.cut(t_wave + 0.33 * k, shep("wave", "happy", X_PAT, 0.5 * (k % 2)), depth=4 if k == 0 else 0, dip=k == 0)
    t_bend = t_mei - 0.08
    sh.cut(t_bend, shep("count_again", "happy", X_PAT), depth=6)
    t_up = t_yb + 0.3
    sh.cut(t_up, shep("stand", "happy", X_PAT), depth=5)
    w2_ents, w2_dx, w2_end = planted_walk(t_mu2 - 0.05, t_mu2 + 2.2, X_PAT, X_STREAM, LEAD_ADV * K)
    for tk, p in w2_ents:
        sh.cut(tk, shep(p, "happy", X_PAT), dip=False)
    sh.cut(w2_end, shep("stand", "warm", X_STREAM), depth=5)
    sh.add_blinks({shep("stand", "warm", X_START): shep("stand", blink("warm"), X_START),
                   shep("stand", "happy", X_PAT): shep("stand", blink("happy"), X_PAT),
                   shep("stand", "warm", X_STREAM): shep("stand", blink("warm"), X_STREAM)}, 0.2, T, rng)

    def sh_x(t):
        """The shepherd's anchor x (continuous)."""
        if t < w1_ents[0][0]:
            return X_START
        if t < w1_end:
            return X_START + w1_dx(t)
        if t < w2_ents[0][0]:
            return X_PAT
        if t < w2_end:
            return X_PAT + w2_dx(t)
        return X_STREAM

    def sh_walk(t):
        if w1_ents[0][0] - 0.1 <= t < w1_end:
            return Tf(dx=w1_dx(t))
        if w2_ents[0][0] - 0.1 <= t < w2_end:
            return Tf(dx=w2_dx(t))
        return Tf()

    def pat(t):
        """Two gentle pats: the bent figure rocks about its feet so the hand bobs down onto the sheep's head."""
        a = 0.0
        for tp in (t_hen, t_ai):
            a += -3.0 * env(t, tp - 0.12, tp + 0.2, 0.1, 0.12)
        return Tf(rot=a)
    sh.mots += [sh_walk, pat, lambda t: Tf(sy=1 + 0.01 * math.sin(2 * math.pi * (t + g0) / 3.2))]
    sh.build(sc)
    sc.sfx("footsteps", w1_ents[0][0], dur=w1_end - w1_ents[0][0] + 0.2, gain_db=-24, pan=0.1)
    sc.sfx("footsteps", w2_ents[0][0], dur=w2_end - w2_ents[0][0] + 0.2, gain_db=-25, pan=-0.1)

    # ================================================================ the sheep around him
    # H1: the one he pats (in front of him, facing him, looking up), then it hops ahead of him to the stream
    h1y = YS + 16
    h1x = X_PAT - 156 * K
    h1x2 = h1x - (X_PAT - X_STREAM)
    s1 = persp(h1y)
    h1 = follower("sheep_h1", 2, None, [(w2_ents[0][0] + 0.15, w2_end + 0.1, h1x, h1x2)], h1y,
                  [(0, "graze", 1, h1x), (t_bend - 0.25, "look_up", 1, h1x), (t_ai + 0.05, "look_up", 1, h1x),
                   (t_up + 0.5, "graze", 1, h1x), (w2_ents[0][0], "stand", -1, h1x), (w2_end + 0.1, "stand", -1, h1x2),
                   (t_chi, "graze", -1, h1x2)],
                  g0, 5 + h1y / 1000, 111, None, rng, T)
    # happy closed eyes after the pats
    h1.ents = [(tk, (st[0], st[1], st[2], st[3], st[4], "happy") if (abs(tk - snap(t_ai + 0.05)) < 1e-6) else st)
               for tk, st in h1.ents]
    h1.mots.append(lambda t: Tf(dy=sum(4 * s1 * env(t, tp - 0.1, tp + 0.22, 0.1, 0.12) for tp in (t_hen, t_ai)),
                                sy=1 - sum(0.03 * env(t, tp - 0.1, tp + 0.22, 0.1, 0.12) for tp in (t_hen, t_ai))))
    h1.build(sc)
    # H2 / H3: hop after him in both walks (they lag a little), graze when he stops
    for name, var, ox, oy, lag, seed in (("sheep_h2", 4, 215, 34, 0.25, 113), ("sheep_h3", 0, 405, -14, 0.45, 115)):
        y = YS + oy
        xa, xb, xc = X_START + ox, X_PAT + ox, X_STREAM + ox
        moves = [(w1_ents[0][0] + lag, w1_end + lag, xa, xb), (w2_ents[0][0] + lag, w2_end + lag, xb, xc)]
        spots = [(0, "graze" if var else "stand", -1, xa), (w1_ents[0][0] + lag - 0.2, "stand", -1, xa),
                 (w1_end + lag, "stand", -1, xb), (w1_end + lag + 0.8, "graze", -1, xb),
                 (t_hd + (0.2 if var else 0.6), "look_up", -1 if var else 1, xb), (t_mt, "graze", -1, xb),
                 (w2_ents[0][0] + lag - 0.2, "stand", -1, xb), (w2_end + lag, "stand", -1, xc),
                 (t_chi + (0.0 if var else 0.25), "graze", -1, xc)]
        fl = follower(name, var, None, moves, y, spots, g0, 5 + y / 1000, seed, None, rng, T)
        fl.build(sc)

    # the heart on the pat
    hx, hy = h1x + 40 * s1, h1y - 215 * s1
    sc.add("heart", doc(heart_markup(hx, hy, 36 * K)), z=7.5, wc=0.3,
           motion=M.combine(pop_motion(t_ai + 0.02, (hx, hy), 0.4, t_ai + 1.5, 0.5, rise=50),
                            lambda t: Tf(rot=8 * math.sin(2 * math.pi * t / 1.1), px=hx, py=hy)))

    # ================================================================ the little lamb
    # steps: two on each '走着', then trotting on through '越走越远' up to the poppy
    steps = [t_z[0], t_z[0] + 0.17, t_z[2], t_z[2] + 0.17] + [t_yue + 0.15 * k for k in range(8)]
    step_dx = (X_SNIFF - LX0) / len(steps)
    t_walk_end = steps[-1] + 0.12
    # the chase: bounds from the poppy over the rise to the landing spot
    t_land = t_tai + 0.02
    nb = 5
    t_b0 = t_zhui2
    db = (t_land - t_b0) / nb
    bx = [X_SNIFF + (X_LAND - X_SNIFF) * i / nb for i in range(nb + 1)]

    def lamb_path(t):
        """(x, y, tilt) of the lamb's anchor."""
        if t < t_b0:
            x = LX0 + sum(step_dx * M.progress(t, ts - 0.02, ts + 0.1, "sine") for ts in steps)
            y = YL - sum(5 * KL * math.sin(math.pi * clamp01((t - ts + 0.02) / 0.14)) for ts in steps
                         if ts - 0.02 <= t <= ts + 0.12)
            return x, y, 0.0
        if t < t_land:
            i = min(nb - 1, int((t - t_b0) / db))
            u = (t - t_b0 - i * db) / db
            x = bx[i] + (bx[i + 1] - bx[i]) * u
            y = lamb_ground(x) - 46 * KL * math.sin(math.pi * u)
            sl = (lamb_ground(x + 30) - lamb_ground(x - 30)) / 60
            return x, y, max(-20.0, min(20.0, math.degrees(math.atan(sl)) * 0.8))
        return X_LAND, YL, 0.0

    def lst(pose, x=LX0, ph=0.0, eyes="open", y=YL):
        return (pose, ph, x, y, 1, eyes)

    lamb = Fig("lamb", lamb_fig_draw(0.0), (LX0, YL), KL, 8.5, g0, seed=121, pivot=lambda st: (st[2], st[3]))
    graze = lst("graze")
    lamb.loops[graze] = (4, clock_loop(g0, 0.22))
    lamb.cut(0, graze)
    lamb.cut(t_xy - 0.05, lst("stand"), depth=5)                 # '小羊': it lifts its head
    lamb.cut(t_c1 - 0.08, graze, depth=4)                       # '吃着吃着'
    for i, ts in enumerate(steps):
        lamb.cut(ts - 0.02, lst("walk_a" if i % 2 == 0 else "walk_b"), dip=False)
        if i in (1, 3):
            lamb.cut(ts + 0.2, lst("stand"), dip=False)
    lamb.cut(t_walk_end, lst("stand"), dip=False)
    sniff = lst("sniff_flower")
    lamb.loops[sniff] = (3, clock_loop(g0, 0.12))
    lamb.cut(t_wen - 0.06, sniff, depth=4)                     # '闻闻小花'
    lamb.cut(t_zhui1 + 0.04, lst("stand"), depth=5)            # the butterfly flutters up
    for i in range(nb):
        st = lst("chase", ph=i * 0.001)

        def fn(t, i=i):
            return int(clamp01((t - t_b0 - i * db) / db) * 4 - 1e-6)
        lamb.loops[st] = (4, fn)
        lamb.cut(t_b0 + i * db, st, dip=False)
    lamb.cut(t_land, lst("stand", X_LAND), depth=9)            # lands, '一抬头'
    lamb.cut(t_yi - 0.04, lst("look_around", X_LAND), depth=4)  # '咦'
    lamb.cut(t_da - 0.02, lst("look_around", X_LAND, 0.6), depth=4)   # '大家': looks back
    lamb.cut(t_bu, LAMB_END, depth=6)                          # '不见了'
    lamb.add_blinks({lst("stand"): lst("stand", eyes="closed"),
                     lst("stand", X_LAND): lst("stand", X_LAND, eyes="closed")}, 0.5, t_tai + 0.9, rng)

    def lamb_mot(t):
        x, y, tilt = lamb_path(t)
        st = lamb.state_at(t)
        return Tf(dx=x - st[2], dy=y - st[3], rot=tilt)
    lamb.mots += [lamb_mot, lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * (t + g0) / 2.1))]
    lamb.build(sc)
    sc.add("lamb_q", doc(question_markup(X_LAND + 18 * KL, YL - 175 * KL, 1.3 * KL)), z=8.6, wc=0,
           motion=pop_motion(t_yi + 0.05, (X_LAND + 18 * KL, YL - 160 * KL), 0.35, t_da + 0.1, 0.3))
    # the poppy it sniffs (the same flower as the one in the sniff drawing)
    pop_x = X_SNIFF + 76 * KL
    sc.add("poppy", doc(PR.wildflower(pop_x, YL, 0.9 * KL, kind="poppy", sway=0.3)), z=8.45)

    # ================================================================ butterflies
    flap_frames = lambda color, x, y, s: [butterfly_svg(x, y, color, f, s) for f in (0.0, 0.25, 0.5, 0.75)]
    bs = 0.9 * KL
    # the yellow one: resting on the poppy, fluttering up when sniffed, flying off over the rise, then up and away
    pxh, pyh = pop_x + 1.6 * KL, YL - 31 * KL - 10 * bs

    def bf_path(t):
        if t < t_wen:
            return pxh, pyh, 0.0
        if t < t_zhui1:
            u = M.progress(t, t_wen, t_wen + 0.5, "out")
            return pxh + 10 * u, pyh - 60 * u + 6 * math.sin(2 * math.pi * t / 0.7), 8 * math.sin(2 * math.pi * t / 0.9)
        if t < t_land:
            lx, ly, _ = lamb_path(t)
            u = clamp01((t - t_zhui1) / (t_land - t_zhui1))
            ahead = 60 + 120 * u
            return (lx + ahead, ly - 170 * KL - 30 * math.sin(2 * math.pi * t / 0.55), 10 * math.sin(2 * math.pi * t / 0.5))
        u = M.progress(t, t_land, t_land + 1.6, "in")
        x0, y0 = X_LAND + 180, YL - 170 * KL
        return (x0 + 380 * u + 20 * math.sin(2 * math.pi * t / 0.6), y0 - 720 * u - 15 * math.sin(2 * math.pi * t / 0.45),
                -15 * u)

    def bf_frame(t):
        if t < t_wen:
            return float((0, 1, 2, 1)[int((t + g0) / 0.4) % 4] if int((t + g0) / 2.0) % 2 else 0)
        return float(int((t + g0) / 0.06) % 4)
    sc.add("butterfly", flap_frames("yellow", pxh, pyh, bs), z=8.7, wc=0.4, frame_at=bf_frame,
           motion=lambda t: (lambda p: Tf(dx=p[0] - pxh, dy=p[1] - pyh, rot=p[2], px=pxh, py=pyh,
                                         alpha=1 - M.progress(t, t_land + 1.2, t_land + 1.6)))(bf_path(t)))
    # two more wander over the meadow
    for i, (color, cx, cy, ax, ay, per) in enumerate((("blue", 1300, 1220, 260, 70, 7.0), ("pink", 2050, 1180, 300, 90, 8.5))):
        sc.add(f"butterfly{i}", flap_frames(color, cx, cy, 0.5), z=7.0 + 0.01 * i, wc=0.4,
               frame_at=lambda t, i=i: float(int((t + g0) / 0.07 + i) % 4),
               motion=lambda t, ax=ax, ay=ay, per=per, cx=cx, cy=cy, i=i: Tf(
                   dx=ax * math.sin(2 * math.pi * (t + g0) / per + i), dy=ay * math.sin(4 * math.pi * (t + g0) / per + 0.5 * i)
                   + 12 * math.sin(2 * math.pi * (t + g0) / 0.8), rot=10 * math.sin(2 * math.pi * (t + g0) / 1.3), px=cx, py=cy))

    # ================================================================ sound
    sc.sfx("birds", 0, dur=T + 0.4, gain_db=-15, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.4, gain_db=-22, fade_in=0.8, fade_out=1.0)
    sc.sfx("sheep", t_ai + 0.12, gain_db=-15, pan=-0.2)
    sc.sfx("pop", t_ai + 0.02, gain_db=-20)
    sc.sfx("sheep", t_hd + 0.05, gain_db=-18, pan=-0.45, pitch=1.06)
    sc.sfx("sheep", t_zhan + 0.25, gain_db=-19, pan=0.4, pitch=0.94)
    sc.sfx("sheep", t_shan + 0.1, gain_db=-21, pan=-0.1, pitch=1.12)
    sc.sfx("sparkle", t_mt - 0.05, gain_db=-24, pan=0.6)
    sc.sfx("sheep", t_chi + 0.05, gain_db=-20, pan=-0.3)
    bell = dict(gain_db=-23, root=91)
    sc.sfx("sparkle", t_xy, pan=0.2, **bell)
    sc.sfx("crunch", t_c1, gain_db=-25, pan=0.1)
    sc.sfx("sparkle", t_land, pan=0.3, **bell)
    sc.sfx("sparkle", t_yi, pan=0.3, **dict(bell, gain_db=-22))
    sc.sfx("sparkle", t_da, pan=0.3, **dict(bell, gain_db=-24))

    # ================================================================ camera
    sc.camera = cam_path([
        (0.0, Cam(1900, 1137, 2000)), (t_ye, Cam(1900, 1137, 2000)), (t_mu + 0.5, Cam(1700, 1170, 1750)),
        (t_mei + 0.2, Cam(1560, 1205, 1480)), (t_yb - 0.2, Cam(1560, 1205, 1480)), (t_shan + 0.3, Cam(1440, 900, 2900)),
        (t_mu2, Cam(1440, 900, 2900)), (t_mu2 + 2.4, Cam(1420, 1110, 2300)), (t_you - 0.6, Cam(1420, 1110, 2300)),
        (t_xy + 0.4, Cam(2440, 1270, 1320)), (t_wen - 0.3, Cam(2700, 1270, 1320)), (t_tai + 0.4, CAM_END),
        (T, CAM_END)],
        ["linear", "sine", "inout", "linear", "inout", "linear", "inout", "linear", "inout", "sine", "inout", "linear"])
    return sc
