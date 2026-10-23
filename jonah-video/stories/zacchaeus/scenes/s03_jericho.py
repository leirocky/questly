"""Scene 3 - Luke 19:1-2. Jericho, the city of palms, on a warm hazy afternoon.

Shots (all on one tall 2112 x 1980 stage, hard cuts on phrase boundaries; s04_crowd uses the same stage so the street
page of the last shot matches its first frame exactly):
  A  the establishing view: the city of palms in the low desert valley (far striped cliffs, flat-roofed sandstone and
     terracotta houses among date palms, a market of striped stalls, balsam bushes), a road winding in from the left
     where Jesus and two disciples walk in; big date palms frame the page; the camera tilts up the tall palms.
  B  the tax booth on a market street: Zacchaeus counts coins, a queue of grumbling payers, his money chest; two tax
     collectors bring him bags of money; he gets up and takes an extra coin from the farmer.
  C  the street (wide): Zacchaeus struts along the near side of the road and people step out of his way.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity film's
Tm class, chunk fallback; nothing is hard-coded to the take):
  0 .. 0.9      calm wide page (the page dip from s02 lands here): Jesus and two disciples walk along the road toward
                the town (planted strides), palms sway, swifts glide, market folk bustle
  '耶利哥'       the camera has eased in on the walkers and the town
  '到处都是'     the camera tilts up the tall palms to their crowns against the turquoise sky (fronds sway, dates)
  '城里住着'     cut to the tax booth: Zacchaeus sits counting coins (one coin from the heap to the stacks every
                0.66 s, clinks), smug; the payers wait in a queue
  '撒该'         a name tag '撒该' pops over him (pop); '收税的人' he taps a coin (glint)
  '罗马皇帝'     a picture bubble pops above the booth: a silver coin with the emperor's laurel-crowned head and a
                Roman eagle standard (pop)
  '向大家收钱'   the first payer reaches over the table and drops three coins on the heap (clinks), frowns and walks
                off grumbling
  '管着好多'     two tax collectors walk in from the left with bags of money and tip them into his money chest one
                after the other (coins pour, clinks)
  '他很有钱'     the chest overflows (coins spill, golden shine, twinkles), Zacchaeus beams
  '可是'         he hops off his stool and struts out to the end of his table; '不喜欢' the queue frowns and folds arms
  '常常'         the farmer pays: a coin into his palm ('常'); '多收' with a sly look he snatches an extra coin
  '放进'         he slips both coins into his plum money pouch (clink, twinkle); the farmer frowns and stomps off
  '大家看见'     cut to the street: Zacchaeus struts along the near side of the road, chin up
  '躲得远远的'   the people in his way step back, turn away and whisper behind their hands; he slows, stops and his
                head drops (lonely); calm hold - s04 opens on exactly this frame (plain fade; ambient motion runs on
                the film's global clock).
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
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import snap

INK = P["ink"]
CREAM = "#fff6e3"
W, H = 2112, 1980                    # one tall stage for s03 and s04 (so the shared street page rasterises identically)
TIME = 0.0                           # Jericho's warm afternoon
PAL = PR._jr_pal(TIME)

for _e in ("smug", "sly", "delighted", "eager", "lonely", "worried", "frustrated", "determined", "kind", "neutral", "grumble",
           "cross", "mutter", "happy", "warm", "ponder", "sad", "surprised", "idea", "thoughtful"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"zq_b_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(e):
    return f"zq_b_{e}"


# ================================================================== small helpers (shared with s04_crowd)
def doc(body, defs=""):
    return S.svg_doc(body, defs, W, H)


def f1(v):
    return f"{v:.1f}"


def gate(t0, t1=1e9):
    return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)


def env(t, t0, t1, fin=0.4, fout=0.4):
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def clamp_cam(c):
    cw = min(c.w, W, H * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), W - cw / 2 - 1), min(max(c.y, ch / 2 + 1), H - ch / 2 - 1), cw, c.rot)


def cam_keys(keys, curves="sine"):
    f = M.cam_keys([(t, clamp_cam(c)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t))


def dipm(t0, s, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there); scales about the layer's pivot."""
    def m(t):
        u = t - t0
        if u < -0.14 or u > 0.3:
            return Tf()
        if u < 0:
            k = M.ease("in")((u + 0.14) / 0.14)
            return Tf(dy=depth * s * k, sy=1 - 0.05 * k)
        if u < 0.13:
            k = M.ease("out")(u / 0.13)
            return Tf(dy=depth * s * (1 - k) - 3 * s * k, sy=0.95 + 0.065 * k)
        k = M.ease("sine")((u - 0.13) / 0.17)
        return Tf(dy=-3 * s * (1 - k), sy=1.015 - 0.015 * k)
    return m


def hopm(t0, s, height=26.0, dur=0.38):
    """A little hop taking off at t0 (crouch, lift, land); a pose cut hides in the crouch just before t0."""
    def m(t):
        u = t - t0
        if u < -0.1 or u > dur + 0.16:
            return Tf()
        if u < 0:
            k = (u + 0.1) / 0.1
            return Tf(dy=4 * s * k, sy=1 - 0.05 * k)
        if u < dur:
            v = u / dur
            return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.04 * math.sin(math.pi * v))
        k = 1 - (u - dur) / 0.16
        return Tf(dy=3 * s * math.sin(math.pi * k), sy=1 - 0.035 * math.sin(math.pi * k))
    return m


def breathm(g0, period=3.0, amount=0.011, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start), so neighbouring scenes breathe in step."""
    def m(t):
        v = math.sin(2 * math.pi * ((t + g0) / period + phase))
        return Tf(sx=1 + 0.35 * amount * v, sy=1 + amount * v)
    return m


def popm(t0, piv, dur=0.35, t_out=None, out_dur=0.25, wob=True):
    """Pop in at t0 (back-ease scale), optionally pop out ending at t_out."""
    def m(t):
        if t < t0 or (t_out is not None and t > t_out):
            return Tf(alpha=0.0)
        u = min(1.0, (t - t0) / dur)
        k = 0.3 + 0.7 * M.ease("back")(u)
        a = min(1.0, (t - t0) / 0.1)
        if t_out is not None and t > t_out - out_dur:
            v = (t_out - t) / out_dur
            k *= 0.6 + 0.4 * v
            a *= v
        r = 3 * math.sin(2 * math.pi * (t - t0) / 2.2) if wob else 0.0
        return Tf(sx=k, sy=k, alpha=a, rot=r, dy=3 * math.sin(2 * math.pi * (t - t0) / 1.7), px=piv[0], py=piv[1])
    return m


class Loop:
    """A flipbook state that cycles keys on the film's global clock."""

    def __init__(self, keys, per, phase=0.0):
        self.keys, self.per, self.phase = tuple(keys), per, phase


class Actor:
    """One figure on its own flipbook layer. Drawings are keys -> markup (draw(key)), all drawn at the home anchor; the
    layer moves by the sum of the move functions (planted-foot walks), squash dips hide hard pose cuts, Loop states
    cycle on the global clock. Scaling (dips, breathing) pivots about the home anchor = the feet."""

    def __init__(self, name, home, s, draw, z, seed, g0, gatef=None, wc=1.0):
        self.name, (self.hx, self.hy), self.s, self.draw = name, home, s, draw
        self.z, self.seed, self.g0, self.gatef, self.wc = z, seed, g0, gatef, wc
        self.ents, self.moves, self.extra, self.dips = [], [], [], []

    def cut(self, t, key, dip=None):
        t = snap(t) if t > 0 else -1.0
        self.ents.append((t, key))
        if dip and t > 0:
            self.dips.append((t, dip))
        return self

    def loop(self, t, keys, per, phase=0.0, dip=None):
        return self.cut(t, Loop(keys, per, phase), dip)

    def key_at(self, t):
        cur = None
        for tk, k in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = k
        if isinstance(cur, Loop):
            cur = cur.keys[int((t + self.g0) / cur.per + cur.phase) % len(cur.keys)]
        return cur

    def off(self, t):
        x = y = 0.0
        for mv in self.moves:
            a, b = mv(t)
            x += a
            y += b
        return x, y

    def pos(self, t):
        x, y = self.off(t)
        return self.hx + x, self.hy + y

    def shift(self, dx, dy=0.0):
        self.moves.append(lambda t: (dx, dy))
        return self

    def walk(self, t0, cycle, n, per, facing=1, first_adv=None, slope=0.0, move=0.12):
        """Planted-foot walk: n cuts every per s from t0; cut i shows cycle[i % len][0] and advances the anchor by
        cycle[i % len][1] * s px toward facing (first_adv overrides the first advance). Returns the time of the last
        cut + per."""
        cts = [snap(t0 + per * i) for i in range(n)]
        ads = []
        for i, tc in enumerate(cts):
            key, adv = cycle[i % len(cycle)]
            if i == 0 and first_adv is not None:
                adv = first_adv
            self.ents.append((tc, key))
            ads.append(adv * self.s * facing)

        def mv(t, cts=cts, ads=ads):
            x = 0.0
            for tc, a in zip(cts, ads):
                x += a * M.progress(t, tc - move * 0.4, tc + move * 0.6, "sine")
            return x, x * slope
        self.moves.append(mv)
        return cts[-1] + per

    def walk_in(self, t0, cycle, n, per, facing=1, first_adv=None, slope=0.0, move=0.12):
        """Like walk(), but the walk ENDS at the home anchor (the drawings stay inside the canvas)."""
        d = self.walk_dist(cycle, n, first_adv) * facing
        self.shift(-d, -d * slope)
        return self.walk(t0, cycle, n, per, facing, first_adv, slope, move)

    def walk_dist(self, cycle, n, first_adv=None):
        d = 0.0
        for i in range(n):
            adv = cycle[i % len(cycle)][1]
            d += first_adv if (i == 0 and first_adv is not None) else adv
        return d * self.s

    def blinks(self, times, pairs):
        """0.13 s closed-eye frames: pairs {key: blink key}, only where no cut is within 0.3 s."""
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        for tb in times:
            tb = snap(tb)
            if any(abs(tb - tk) < 0.3 for tk in cut_ts):
                continue
            cur = None
            for tk, k in sorted(self.ents, key=lambda e: e[0]):
                if tk <= tb:
                    cur = k
            if not isinstance(cur, Loop) and cur in pairs:
                self.ents += [(tb, pairs[cur]), (snap(tb + 0.13), cur)]
        return self

    def build(self, sc):
        ents = sorted(self.ents, key=lambda e: e[0])
        keys = []
        for _, k in ents:
            for kk in (k.keys if isinstance(k, Loop) else (k,)):
                if kk not in keys:
                    keys.append(kk)
        frames = [doc(self.draw(k)) for k in keys]
        idx = {k: i for i, k in enumerate(keys)}
        g0 = self.g0

        def fa(t):
            cur = ents[0][1]
            for tk, k in ents:
                if t >= tk:
                    cur = k
                else:
                    break
            if isinstance(cur, Loop):
                cur = cur.keys[int((t + g0) / cur.per + cur.phase) % len(cur.keys)]
            return float(idx[cur])
        hx, hy = self.hx, self.hy

        def base(t):
            x, y = self.off(t)
            return Tf(dx=x, dy=y, px=hx, py=hy)
        mots = [base] + [dipm(td, self.s, d) for td, d in self.dips] + self.extra
        if self.gatef is not None:
            mots.append(self.gatef)
        sc.add(self.name, frames if len(frames) > 1 else frames[0], z=self.z, seed=self.seed, wc=self.wc,
               frame_at=fa if len(frames) > 1 else None, motion=M.combine(*mots))
        return self


# walk cycles: (drawing key, advance of the anchor when this drawing appears, px at scale 1) - the planted ankle stays put
ZAC_WALK = (("walk_a", 23), ("walk_c", 21), ("walk_b", 47), ("walk_c", 45))
ZAC_STRUT = (("strut_a", 73), ("strut_b", 73))
FOLK_ADV = {"man": 84, "woman": 81, "elder": 82, "child": 50, "fruit_seller": 84, "farmer": 86}
JESUS_ADV = 87
DISC_ADV = 87


def folk_walk(kind, a="walk_a", b="walk_b"):
    return ((a, FOLK_ADV[kind]), (b, FOLK_ADV[kind]))


def shadow(x, y, s, w=110, o=0.18):
    return C.ground_shadow(x, y, s, w, o)


def name_tag(x, y, text, size=46, col="#2a6e74"):
    """A cream name label with a little pointer under it (anchor = the pointer tip), LXGW WenKai."""
    w = size * (len(text) + 0.9)
    h = size * 1.45
    b = (f'<path d="M{f1(x - w / 2)},{f1(y - 18 - h)} h{f1(w)} q14,0 14,14 v{f1(h - 28)} q0,14 -14,14 h{f1(-w / 2 + 16)} '
         f'l-16,18 l-16,-18 h{f1(-w / 2 + 16)} q-14,0 -14,-14 v{f1(-h + 28)} q0,-14 14,-14 Z" fill="{CREAM}" '
         f'stroke="#c9a46a" stroke-width="4"/>')
    b = S.g(b, filter="wobble-fine")
    b += (f'<text x="{f1(x + 7)}" y="{f1(y - 18 - h * 0.30)}" font-family="LXGW WenKai" font-weight="bold" '
          f'font-size="{size}" fill="{col}" text-anchor="middle">{text}</text>')
    return b


def sparkle(x, y, r, col="#fff6d0"):
    return S.g(PR._sparkle_p(x, y, r, col), filter="wobble-fine")


def swift(x, y, k, flap):
    """A little swift (two arched wings); flap 0/1."""
    d = 10 * k if flap else -4 * k
    return (f'<path d="M{f1(x - 22 * k)},{f1(y + d)} Q{f1(x - 10 * k)},{f1(y - 10 * k)} {f1(x)},{f1(y)} '
            f'Q{f1(x + 10 * k)},{f1(y - 10 * k)} {f1(x + 22 * k)},{f1(y + d)}" fill="none" stroke="#4e5f66" '
            f'stroke-width="{f1(3.2 * k)}" stroke-linecap="round" stroke-linejoin="round"/>')


def add_swifts(sc, name, z, pts, k, g0, gatef, period=7.0, span=900.0, seed=3, flap=0.13):
    """A few swifts gliding across (on the global clock): pts [(x, y)] start points, drifting right over span px."""
    rng = random.Random(seed)
    for i, (x, y) in enumerate(pts):
        fr = [doc(swift(x, y, k * rng.uniform(0.85, 1.15), f)) for f in (0, 1)]
        ph = rng.uniform(0, 1)
        per = period * rng.uniform(0.85, 1.2)

        def mot(t, ph=ph, per=per, i=i):
            u = ((t + g0) / per + ph) % 1.0
            a = math.sin(math.pi * u)
            return Tf(dx=span * (u - 0.5), dy=26 * math.sin(2 * math.pi * (t + g0) / 2.3 + i), alpha=min(1.0, a * 3) * gatef(t).alpha)
        sc.add(f"{name}{i}", fr, z=z + 0.001 * i, wc=0.3, seed=seed * 10 + i,
               frame_at=lambda t, i=i: float(int((t + g0) / flap + i) % 2), motion=mot)


def add_palms(sc, name, items, z, seed, g0, gatef, deg=0.55, period=3.6, phase=0.0):
    """Date palms swaying in the breeze: each palm on its own layer, rocking smoothly about the foot of its trunk on the
    film's global clock (no flipbook crossfades, so the fronds never double up). The trunk leans with the breeze and the
    crown follows; a second, slower wave keeps neighbours out of step."""
    for i, it in enumerate(items):
        x, y, s_, f, h, lean, sd = it
        svg = doc(PR.date_palm(x, y, s_, f, height=h, lean=lean, sway=0.15 * (1 if i % 2 else -1), time=TIME, seed=sd))
        ph = phase + 0.29 * i
        per = period * (1 + 0.13 * i)

        def m(t, x=x, y=y, ph=ph, per=per):
            u = (t + g0) / per + ph
            r = deg * (math.sin(2 * math.pi * u) + 0.35 * math.sin(2 * math.pi * (1.7 * u + 0.3)))
            return Tf(rot=r, px=x, py=y)
        sc.add(f"{name}{i}", svg, z=z + 0.001 * i, seed=seed + i, motion=M.combine(m, gatef))


# ================================================================== SET A: the city of palms (establishing, tall)
HZ = 1250                            # foot of the far hills
AK = 0.40                            # Jesus and the disciples on the road
A_P0, A_P1 = (430, 1722), (1000, 1622)   # the walkers' path (Jesus's anchor) from the start to the town
A_SLOPE = (A_P1[1] - A_P0[1]) / (A_P1[0] - A_P0[0])


def a_back_svg():
    b = PR.jericho_sky(-10, -10, W + 10, HZ + 60, time=TIME, sun=(1660, 690), clouds=1.0, birds=0, seed=4, scale=1.1)
    b += S.g(PR._jr_far(-60, W + 60, HZ, 0.9, TIME, seed=3), filter="wobble")
    rng = random.Random(5)
    far = ""
    for i in range(24):
        px = -40 + i * 94 + rng.uniform(-30, 30)
        far += PR._place(PR._jr_palm(rng.uniform(0.7, 1.0), rng.uniform(-0.2, 0.2), 0.0, False, TIME, 30 + i, far=True),
                         px, HZ + 34, 0.30 * rng.uniform(0.9, 1.1), 1, filt=None)
    b += S.g(far, filter="wobble-fine")
    b += f'<rect x="-20" y="{HZ + 26}" width="{W + 40}" height="{H - HZ}" fill="{PAL["sand"]}"/>'
    return doc(b)


def a_city_svg():
    rng = random.Random(12)
    b = ""
    rows = ((HZ + 52, 0.30, 10, -40, 0.9), (HZ + 104, 0.37, 8, 10, 0.95), (HZ + 168, 0.45, 6, -90, 1.0))
    for r, (yy, sc_, n, x0, k) in enumerate(rows):
        for i in range(n):
            hx = x0 + (i + 0.5) * (W + 160) / n + rng.uniform(-40, 40)
            if r == 2 and 900 < hx < 1260:
                continue                              # the market street opens here
            b += PR.jericho_house(hx, yy, sc_ * rng.uniform(0.92, 1.05), 1 if (i + r) % 2 else -1, variant=(i * 3 + r) % 4,
                                  time=TIME, seed=i + 10 * r, awning=(i + r) % 3 != 0)
            if (i + r) % 3 == 0 and not (820 < hx < 1340 and r == 2):
                b += PR.date_palm(hx + rng.choice((-1, 1)) * 150 * sc_, yy + 6, sc_ * 0.95, 1, height=rng.uniform(0.95, 1.15),
                                  lean=rng.uniform(-0.25, 0.25), time=TIME, seed=i + 7 * r)
    # the market at the edge of town: striped stalls either side of the street
    for i, (mx, my, s_) in enumerate(((560, HZ + 262, 0.46), (800, HZ + 252, 0.44), (1330, HZ + 252, 0.44),
                                      (1580, HZ + 266, 0.47))):
        b += PR.market_stall(mx, my, s_, 1, time=TIME, seed=i + 1)
    # palms along the market
    for i, (px, py, s_, h_) in enumerate(((380, HZ + 280, 0.52, 1.15), (1790, HZ + 290, 0.55, 1.1))):
        b += PR.date_palm(px, py, s_, 1, height=h_, lean=(-0.15, 0.2)[i], time=TIME, seed=60 + i)
    # balsam gardens along the town's edge
    for i in range(9):
        bx = 80 + i * 240 + rng.uniform(-40, 40)
        if 880 < bx < 1300:
            continue
        b += PR.balsam_bush(bx, HZ + 330 + rng.uniform(-6, 10), 0.55, 1 if i % 2 else -1, time=TIME, seed=i)
    return doc(b)


def a_road_svg():
    """The packed-earth road winding in from the lower left to the market street, dry tufts and stones."""
    lite = S.mix(PAL["sand_lt"], "#fff2d8", 0.25)
    edge = S.shade(PAL["sand"], -0.2)
    d = ("M-80,1680 C300,1655 700,1610 1000,1582 C1070,1566 1108,1515 1124,1446 Q1140,1436 1156,1446 "
         "C1170,1515 1196,1556 1240,1574 C1150,1612 1060,1640 1000,1652 C700,1712 300,1800 -80,1862 Z")
    b = S.path(d, fill=lite, sw=3, extra=f'stroke="{edge}"')
    rng = random.Random(8)
    for i in range(70):
        x, y = rng.uniform(-40, W + 40), rng.uniform(HZ + 360, H + 10)
        b += PR._ell(x, y, rng.uniform(3, 7), rng.uniform(2, 4), S.shade(PAL["sand"], rng.choice((-0.15, 0.12))), 0,
                     extra='opacity="0.8"')
    for i in range(22):
        x, y = rng.uniform(-40, W + 40), rng.uniform(HZ + 420, H)
        b += PR._jr_tuft(x, y, rng.uniform(0.8, 1.4), TIME, rng.randrange(9))
    for x, y, r in ((1640, 1830, 34), (1720, 1860, 22), (520, 1950, 30), (1280, 1700, 20), (1330, 1712, 14)):
        b += PR._ell(x, y, r, r * 0.55, S.mix(PAL["stone"], "#d8c8a8", 0.4), 3)
    out = S.g(b, filter="wobble")
    for i, (x, y, s_) in enumerate(((1380, 1660, 0.62), (1250, 1690, 0.5), (860, 1560, 0.45))):
        out += PR.balsam_bush(x, y, s_, 1 if i % 2 else -1, time=TIME, seed=20 + i)
    return doc(out)


def a_folk_svg(k):
    """Tiny market folk at the stalls (2-frame bustle)."""
    b = ""
    for i, (x, y, kind, v, f, poses) in enumerate((
            (520, HZ + 300, "woman", 1, 1, ("stand", "point")), (650, HZ + 296, "man", 2, -1, ("look", "stand")),
            (850, HZ + 290, "child", 1, 1, ("wave", "stand")), (1290, HZ + 292, "fruit_seller", 0, 1, ("smile", "point")),
            (1460, HZ + 300, "woman", 4, -1, ("stand", "mutter")), (1640, HZ + 306, "elder", 0, -1, ("stand", "look")))):
        p = poses[(k + i) % 2]
        b += C.jericho_folk(x, y, 0.27, f, kind=kind, variant=v, pose=p, phase=0.3 * k + 0.2 * i)
    return doc(b)


A_FRONT_L = [(130, H + 70, 1.32, 1, 1.5, 0.08, 91)]
A_FRONT_R = [(1985, H + 90, 1.28, -1, 1.55, 0.06, 92), (1640, H - 120, 0.72, 1, 1.35, 0.14, 94)]


def a_front_svg():
    b = ""
    rng = random.Random(21)
    for i in range(10):
        x = rng.choice((rng.uniform(-40, 420), rng.uniform(1650, W + 40)))
        b += PR._jr_tuft(x, rng.uniform(1880, H), rng.uniform(1.4, 2.0), TIME, rng.randrange(9))
    b += PR._place(PR._date_basket(), 1840, 1950, 1.25, 1, filt=None)
    return doc(S.g(b, filter="wobble-fine"))


def walker_markup(who, key):
    pose = key
    if who == "jesus":
        return shadow(*A_P0, AK, 100, 0.16) + C.jesus(*A_P0, AK, 1, pose=pose, expr="kind")
    v = {"d0": 0, "d1": 3}[who]
    x0 = A_P0[0] - {"d0": 78, "d1": 150}[who] * AK / 0.4
    y0 = A_P0[1] - A_SLOPE * (A_P0[0] - x0)
    return shadow(x0, y0, AK, 100, 0.16) + C.disciples(x0, y0, AK, 1, variant=v, pose=pose, expr="kind")


# ================================================================== SET B: the tax booth on a market street
BK = 1.08                            # people / booth scale
BX, BY = 840, 935                    # tax_booth anchor (floor under the middle of the table front)
B_RY, B_SS = 640, 0.78               # the street behind: road centre, scale
SEAT = PR.local_to_stage(BX, BY, BK, 1, *PR.TAX_BOOTH_SEAT)
ZST_Y = BY - PR.TAX_TABLE_DEPTH * BK         # Zacchaeus standing behind the table
ZEND = (BX + 300, BY - 10)                   # ... and at the right end of it (line 5)
CHEST = (470, 942, 0.82)
P1 = (BX + 300, BY + 14)
FARMER = (BX + 505, BY + 16)
QUEUE = [("woman", 2, BX + 640, BY + 22, "frown"), ("elder", 4, BX + 770, BY + 18, "stand")]
COL1 = (300, BY + 26)                        # where the two tax collectors stop (left of the chest)
COL2 = (160, BY + 34)
HEAP = (BX - 11, BY - 128)                   # the coin heap on the table


def b_back_svg():
    b = PR.jericho_sky(-10, -10, W + 10, 520, time=TIME, sun=None, clouds=0.8, birds=0, seed=9, scale=1.0)
    b += PR.jericho_street(-220, W + 220, B_RY, B_SS, part="back", time=TIME, seed=21)
    b += PR.jericho_street(-220, W + 220, B_RY, B_SS, part="road", time=TIME, seed=21, bottom=1240)
    return doc(b)


def b_far_folk_svg(k):
    """People on the far side of the street (small, 2-frame shuffle): a mother and child at a stall, two men chatting."""
    fe = B_RY - 150 * B_SS
    b = ""
    for i, (x, kind, v, f, poses) in enumerate(((1250, "woman", 0, 1, ("stand", "look")), (1310, "child", 2, -1, ("stand", "point")),
                                                (1720, "man", 3, 1, ("mutter", "mutter")), (1815, "man", 5, -1, ("mutter", "stand")),
                                                (300, "elder", 1, 1, ("stand", "stand")))):
        b += C.jericho_folk(x, fe + 8, 0.66, f, kind=kind, variant=v, pose=poses[(k + i) % 2], phase=0.25 * k + 0.3 * i)
    return doc(b)


def b_booth_svg(part):
    return doc(PR.tax_booth(BX, BY, BK, 1, part=part, time=TIME))


def chest_svg(coins, glow, spill=False):
    x, y, s = CHEST
    b = shadow(x, y, s, 260, 0.16) + PR.money_chest(x, y, s, 1, open=1.0, coins=coins, glow=glow)
    if spill:
        b += PR.coin_pile(x - 120 * s, y + 4, s, n=7, style="spill", seed=3)
        b += PR.coin_pile(x + 130 * s, y + 6, s, n=6, style="spill", seed=5)
        b += PR.coin(x + 70 * s, y - 2, s, tilt=0.3) + PR.coin(x - 60 * s, y + 6, s * 0.9, tilt=0.4)
    return doc(b)


def coin_sack(x, y, s, empty=False):
    """A plump burlap money bag tied with a red cord (anchor = its bottom centre); empty = slumped flat."""
    sack, dk = "#c9a46a", "#9a7444"
    if empty:
        d = (f"M{f1(x - 46 * s)},{f1(y)} Q{f1(x - 50 * s)},{f1(y - 26 * s)} {f1(x - 20 * s)},{f1(y - 30 * s)} L{f1(x + 34 * s)},"
             f"{f1(y - 22 * s)} Q{f1(x + 52 * s)},{f1(y - 18 * s)} {f1(x + 50 * s)},{f1(y)} Z")
        b = S.path(d, fill=sack, sw=3.2 * s)
        b += PR._line(x - 10 * s, y - 24 * s, x + 22 * s, y - 20 * s, sw=2.2 * s, color=dk)
        return S.g(b, filter="wobble-fine")
    d = (f"M{f1(x - 40 * s)},{f1(y)} Q{f1(x - 56 * s)},{f1(y - 52 * s)} {f1(x - 22 * s)},{f1(y - 74 * s)} "
         f"L{f1(x - 12 * s)},{f1(y - 82 * s)} Q{f1(x - 20 * s)},{f1(y - 100 * s)} {f1(x - 4 * s)},{f1(y - 102 * s)} "
         f"Q{f1(x + 6 * s)},{f1(y - 92 * s)} {f1(x + 14 * s)},{f1(y - 102 * s)} Q{f1(x + 24 * s)},{f1(y - 96 * s)} "
         f"{f1(x + 14 * s)},{f1(y - 82 * s)} L{f1(x + 24 * s)},{f1(y - 74 * s)} Q{f1(x + 58 * s)},{f1(y - 50 * s)} "
         f"{f1(x + 42 * s)},{f1(y)} Z")
    b = S.path(d, fill=sack, sw=3.4 * s)
    b += PR._p(f"M{f1(x - 16 * s)},{f1(y - 80 * s)} Q{f1(x)},{f1(y - 74 * s)} {f1(x + 18 * s)},{f1(y - 80 * s)}", sw=5 * s,
               stroke="#c63d3d")
    b += PR._p(f"M{f1(x - 20 * s)},{f1(y - 40 * s)} q8,10 16,4 M{f1(x + 10 * s)},{f1(y - 30 * s)} q10,6 16,-4", sw=2.2 * s,
               stroke=dk)
    b += PR._jcoin(x + 2 * s, y - 96 * s, 8 * s, 0.4)
    return S.g(b, filter="wobble-fine")


def emperor_bubble(cx, cy, r, tail):
    """A round picture bubble: a silver coin with the emperor's laurel-crowned head, and a little Roman eagle standard.
    tail = (x, y) where the trail of little bubbles points."""
    b = ""
    tx, ty = tail
    for k, rr in enumerate((0.11, 0.075, 0.05)):
        u = 0.62 + 0.15 * k
        b += PR._circ(cx + (tx - cx) * u, cy + (ty - cy) * u, r * rr, "#fffaf0", 3)
    b += PR._circ(cx, cy, r, "#fffaf0", 4.5)
    b += PR._circ(cx, cy, r * 0.93, "none", 2, stroke="#e6d2a8", extra='stroke-dasharray="9 7"')
    # the coin
    kx, ky, kr = cx - r * 0.24, cy + r * 0.02, r * 0.5
    silver, sdk, slt = "#cfcfc4", "#9c9c90", "#ecece2"
    b += PR._circ(kx + 4, ky + 6, kr, sdk, 0, extra='opacity="0.5"')
    b += PR._circ(kx, ky, kr, silver, 4)
    b += PR._circ(kx, ky, kr * 0.84, "none", 2.2, stroke=sdk, extra='stroke-dasharray="3 5"')
    # the profile head (facing right), raised in the metal
    hr = kr * 0.36
    hx, hy = kx - kr * 0.04, ky - kr * 0.06
    head = (f"M{f1(hx - hr * 0.9)},{f1(hy + hr * 0.2)} Q{f1(hx - hr * 1.05)},{f1(hy - hr * 1.05)} {f1(hx + hr * 0.1)},"
            f"{f1(hy - hr * 1.0)} Q{f1(hx + hr * 0.9)},{f1(hy - hr * 0.9)} {f1(hx + hr * 0.95)},{f1(hy - hr * 0.1)} "
            f"L{f1(hx + hr * 1.25)},{f1(hy + hr * 0.18)} L{f1(hx + hr * 0.92)},{f1(hy + hr * 0.3)} Q{f1(hx + hr * 0.95)},"
            f"{f1(hy + hr * 0.62)} {f1(hx + hr * 0.6)},{f1(hy + hr * 0.78)} L{f1(hx + hr * 0.5)},{f1(hy + hr * 1.35)} "
            f"Q{f1(hx + hr * 0.1)},{f1(hy + hr * 1.6)} {f1(hx - hr * 0.9)},{f1(hy + hr * 1.45)} L{f1(hx - hr * 0.55)},"
            f"{f1(hy + hr * 0.9)} Q{f1(hx - hr * 0.95)},{f1(hy + hr * 0.7)} {f1(hx - hr * 0.9)},{f1(hy + hr * 0.2)} Z")
    b += PR._p(head, "#a8a89a", 3.0, stroke="#6c6c62")
    b += PR._p(head, "none", 1.6, stroke=slt, extra=f'transform="translate(-2,-2)" opacity="0.8"')
    b += PR._circ(hx + hr * 0.45, hy - hr * 0.28, hr * 0.09, "#5c5c52", 0)
    for j in range(7):                                   # the laurel wreath round the back of the head
        a = math.radians(-160 + j * 26)
        lx, ly = hx - hr * 0.05 + math.cos(a) * hr * 0.98, hy - hr * 0.2 + math.sin(a) * hr * 0.9
        b += PR._ell(lx, ly, hr * 0.24, hr * 0.11, "#7f9a52", 1.8, stroke="#4f6a32",
                     extra=f'transform="rotate({f1(math.degrees(a) + 90)} {f1(lx)} {f1(ly)})"')
    b += PR._p(f"M{f1(hx - hr * 1.0)},{f1(hy + hr * 0.1)} q{f1(-hr * 0.3)},{f1(hr * 0.3)} {f1(-hr * 0.2)},{f1(hr * 0.6)} "
               f"M{f1(hx - hr * 0.95)},{f1(hy + hr * 0.15)} q{f1(-hr * 0.1)},{f1(hr * 0.4)} {f1(hr * 0.05)},{f1(hr * 0.65)}",
               sw=2.2, stroke="#6f7f4a")
    b += PR._ell(kx - kr * 0.45, ky - kr * 0.55, kr * 0.18, kr * 0.08, "#fbfbf4", 0, extra='opacity="0.8"')
    # the eagle standard
    ex, ey = cx + r * 0.52, cy + r * 0.62
    pole_top = cy - r * 0.62
    b += PR._line(ex, ey, ex, pole_top + r * 0.12, sw=5, color="#8a5a36")
    b += PR._rect(ex - r * 0.17, cy - r * 0.18, r * 0.34, r * 0.34, "#c0392f", 2.6)
    for j in range(5):                                   # the gold fringe
        fx_ = ex - r * 0.15 + j * r * 0.075
        b += PR._line(fx_, cy + r * 0.16, fx_, cy + r * 0.22, sw=2.6, color="#e8b746")
    b += PR._p(f"M{f1(ex - r * 0.17)},{f1(cy + r * 0.16)} l{f1(r * 0.34)},0", sw=4, stroke="#e8b746")
    b += PR._circ(ex, cy - r * 0.01, r * 0.07, "#e8b746", 2)
    b += PR._line(ex - r * 0.21, cy - r * 0.18, ex + r * 0.21, cy - r * 0.18, sw=4, color="#e8b746")
    gold = "#e8b746"
    wy = pole_top + r * 0.06
    wing = (f"M{f1(ex)},{f1(wy)} Q{f1(ex - r * 0.12)},{f1(wy - r * 0.16)} {f1(ex - r * 0.26)},{f1(wy - r * 0.2)} "
            f"Q{f1(ex - r * 0.2)},{f1(wy - r * 0.06)} {f1(ex - r * 0.24)},{f1(wy + r * 0.02)} Q{f1(ex - r * 0.1)},{f1(wy - r * 0.02)} "
            f"{f1(ex)},{f1(wy + r * 0.06)} Q{f1(ex + r * 0.1)},{f1(wy - r * 0.02)} {f1(ex + r * 0.24)},{f1(wy + r * 0.02)} "
            f"Q{f1(ex + r * 0.2)},{f1(wy - r * 0.06)} {f1(ex + r * 0.26)},{f1(wy - r * 0.2)} Q{f1(ex + r * 0.12)},"
            f"{f1(wy - r * 0.16)} {f1(ex)},{f1(wy)} Z")
    b += PR._p(wing, gold, 2.6)
    b += PR._circ(ex, wy - r * 0.07, r * 0.045, gold, 2.2)
    b += PR._p(f"M{f1(ex + r * 0.04)},{f1(wy - r * 0.08)} l{f1(r * 0.05)},{f1(r * 0.015)}", sw=2.4, stroke="#c48f2c")
    return S.g(b, filter="wobble-fine")


def zac_b_markup(key):
    """Zacchaeus at the booth: ('count', ph[, expr]) seated; ('stand' / 'strut_a' / ...,  expr) standing behind the
    table (home = his standing spot behind the table)."""
    if isinstance(key, str):
        key = (key, "smug")
    pose = key[0]
    if pose == "count":
        return C.zacchaeus(*SEAT, BK, 1, pose="count", phase=key[1], expr=key[2] if len(key) > 2 else None)
    expr = key[1] if len(key) > 1 else None
    x, y = SEAT[0], ZST_Y
    kw = {"coins": False} if pose == "give" else {}
    return C.zacchaeus(x, y, BK, 1, pose=pose, expr=expr, **kw)


def folk_markup(x, y, s, kind, v, key, facing, sh=True):
    pose, expr = key[0], (key[1] if len(key) > 1 else None)
    f = key[2] if len(key) > 2 else facing
    ph = key[3] if len(key) > 3 else 0.0
    item = key[4] if len(key) > 4 else None
    m = C.jericho_folk(x, y, s, f, kind=kind, variant=v, pose=pose, expr=expr, phase=ph, item=item, coins=pose != "pay"
                       or (len(key) > 5 and key[5]))
    return (shadow(x, y, s, 120, 0.16) if sh else "") + m


# ================================================================== SET C: the street (wide; shared with s04_crowd)
SK = 0.78                            # people / street scale
SRY = 700                            # road centre
SFE, SNE = SRY - 150 * SK, SRY + 150 * SK     # far edge 583, near edge 817
ZY = 985                             # Zacchaeus walks along the near verge
Z_C0 = 420                           # his strut starts here (home x)
C_STRUT_N = 8                        # strut steps
C_WALK_N, C_WALK_FIRST = 3, 30       # then a few slowing walk steps


def c_back_svg():
    b = PR.jericho_sky(-10, -10, W + 10, 660, time=TIME, sun=None, clouds=1.0, birds=0, seed=17, scale=1.0)
    b += PR.jericho_street(-240, W + 240, SRY, SK, part="back", time=TIME, seed=7)
    return doc(b)


def c_road_svg():
    return doc(PR.jericho_street(-240, W + 240, SRY, SK, part="road", time=TIME, seed=7, bottom=1300))


C_PALMS = [(330, SFE - 26, 0.66, 1, 1.12, -0.12, 41), (1390, SFE - 30, 0.68, -1, 1.18, 0.1, 43)]
C_FRONT = [(2050, 1300, 1.05, -1, 1.25, 0.1, 45)]


def c_front_svg():
    b = PR._place(PR._date_basket(), 120, 1160, 1.1, 1, filt=None)
    rng = random.Random(31)
    for i in range(6):
        b += PR._jr_tuft(rng.uniform(-20, 2130), rng.uniform(1100, 1180), rng.uniform(1.2, 1.6), TIME, rng.randrange(9))
    return doc(S.g(b, filter="wobble-fine"))


# The people in the street at the end of s03 (s04_crowd starts from exactly these): name -> dict(kind, variant, home,
# end offset, final key). Keys are folk_markup keys (pose, expr, facing, phase).
STREET_FOLK = {
    # near verge (in Zacchaeus's way)
    "mum":   dict(kind="woman", v=3, home=(1200, 1000), f=-1),
    "kid":   dict(kind="child", v=1, home=(1272, 1012), f=-1),
    "men1":  dict(kind="man", v=2, home=(1565, 975), f=-1),
    "men2":  dict(kind="farmer", v=0, home=(1680, 982), f=-1),
    "elder": dict(kind="elder", v=1, home=(770, 880), f=1),
    # far side
    "w1":    dict(kind="woman", v=5, home=(720, SFE + 8), f=1),
    "w2":    dict(kind="woman", v=1, home=(830, SFE + 10), f=-1),
    "fs":    dict(kind="fruit_seller", v=0, home=(1250, SFE + 4), f=-1),
    "m3":    dict(kind="man", v=4, home=(1830, SFE + 12), f=-1),
}


def street_folk_markup(name, key):
    d = STREET_FOLK[name]
    x, y = d["home"]
    return folk_markup(x, y, SK, d["kind"], d["v"], key, d["f"])


def zac_c_markup(key):
    pose, expr = key[0], (key[1] if len(key) > 1 else None)
    f = key[2] if len(key) > 2 else 1
    return shadow(Z_C0, ZY, SK, 100, 0.18) + C.zacchaeus(Z_C0, ZY, SK, f, pose=pose, expr=expr)


def street_cam_end():
    return Cam(1010, 640, 1780)


def add_street_set(sc, gatef, g0, z=50.0):
    """The street page (sky, houses, swaying palms, road, foreground) - identical layers in s03 and s04."""
    sc.add("c_back", c_back_svg(), z=z, seed=701, motion=gatef)
    add_palms(sc, "c_palms", C_PALMS, z + 0.1, 703, g0, gatef, 0.45, 3.6, 0.1)
    sc.add("c_road", c_road_svg(), z=z + 0.2, seed=705, motion=gatef)
    add_swifts(sc, "c_swift", z + 0.05, [(700, 150), (900, 210), (1500, 120)], 1.0, g0, gatef, period=9.0, span=1400, seed=7)
    add_palms(sc, "c_fpalm", C_FRONT, z + 5.0, 707, g0, gatef, 0.5, 3.1, 0.4)
    sc.add("c_front", c_front_svg(), z=z + 5.1, seed=709, motion=gatef)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    L = ctx.lines

    t_cutB = snap(L[2].start - 0.3)
    t_cutC = snap(L[6].start - 0.28)
    gA, gB, gC = gate(-1, t_cutB), gate(t_cutB, t_cutC), gate(t_cutC, 1e9)

    # ------------------------------------------------------------ SHOT A: the city of palms
    t_tilt0 = L[1].start - 0.25
    t_tilt1 = t_cutB - 0.25
    sc.add("a_back", a_back_svg(), z=1.0, seed=101, motion=gA)
    add_swifts(sc, "a_swift", 1.05, [(600, 820), (760, 900), (1200, 760), (1400, 980)], 1.1, g0, gA, period=8.0, span=1600,
               seed=3)
    sc.add("a_city", a_city_svg(), z=1.1, seed=103, motion=gA)
    sc.add("a_road", a_road_svg(), z=1.2, seed=105, motion=gA)
    sc.add("a_folk", [a_folk_svg(k) for k in (0, 1)], z=1.25, seed=107, motion=gA,
           frame_at=lambda t: float(int((t + g0) / 0.7) % 2))
    # Jesus and two disciples walking in (planted strides; they grow a little smaller as the road recedes)
    n_steps = 19
    per = (t_cutB - 0.45) / n_steps
    for i, who in enumerate(("d1", "d0", "jesus")):
        a = Actor(f"a_{who}", (0, 0), AK, lambda k, who=who: walker_markup(who, k), 1.3 + 0.01 * i, 111 + i, g0, gA)
        if who == "jesus":
            a.hx, a.hy = A_P0
        else:
            x0 = A_P0[0] - {"d0": 78, "d1": 150}[who]
            a.hx, a.hy = x0, A_P0[1] - A_SLOPE * (A_P0[0] - x0)
        cyc = (("walk_a", JESUS_ADV), ("walk_b", JESUS_ADV)) if who == "jesus" else (("walk_b", DISC_ADV), ("walk_a", DISC_ADV))
        if who == "d0":
            cyc = cyc[::-1]
        a.cut(0, cyc[-1][0])
        a.walk(0.25 + 0.06 * i, cyc, n_steps, per, 1, slope=A_SLOPE)
        hx, hy = a.hx, a.hy
        a.extra.append(lambda t, a=a: Tf(sx=1 - 0.16 * (a.off(t)[0] / 750), sy=1 - 0.16 * (a.off(t)[0] / 750)))
        a.build(sc)
    add_palms(sc, "a_palms_l", A_FRONT_L, 1.5, 121, g0, gA, 0.5, 3.4, 0.0)
    add_palms(sc, "a_palms_r", A_FRONT_R, 1.51, 123, g0, gA, 0.5, 3.8, 0.35)
    sc.add("a_front", a_front_svg(), z=1.6, seed=125, motion=gA)
    camA = cam_keys([(0, Cam(1010, 1420, 1960)), (t_tilt0, Cam(1060, 1420, 1900)), (t_tilt1, Cam(1056, 640, 2112))],
                    ["sine", "sine"])

    # ------------------------------------------------------------ SHOT B: the tax booth
    sc.add("b_back", b_back_svg(), z=10.0, seed=201, motion=gB)
    sc.add("b_far", [b_far_folk_svg(k) for k in (0, 1)], z=10.05, seed=203, motion=gB,
           frame_at=lambda t: float(int((t + g0) / 0.9) % 2))
    sc.add("b_booth_back", b_booth_svg("back"), z=10.1, seed=205, motion=gB)
    # beats
    t_name = tm.at(2, "撒该", 0)
    t_shou = tm.at(2, "收税的人", 0)
    t_rome = tm.at(3, "罗马皇帝", 0)
    t_xiang = tm.at(3, "向大家收钱的人", 0)
    t_guan = tm.at(4, "撒该管着好多收税的人", 2)
    t_shui4 = tm.at(4, "撒该管着好多收税的人", 6)
    t_ren4 = tm.at(4, "撒该管着好多收税的人", 9)
    t_rich = tm.at(4, "他很有钱", 1)
    t_keshi = tm.at(5, "可是", 0)
    t_bu = tm.at(5, "大家都不喜欢撒该", 3)
    t_yin = tm.at(5, "因为他常常多收别人的钱", 0)
    t_chang = tm.at(5, "因为他常常多收别人的钱", 3)
    t_duo = tm.at(5, "因为他常常多收别人的钱", 5)
    t_fang = tm.at(5, "放进自己的口袋", 0)
    t_kou = tm.at(5, "放进自己的口袋", 5)

    # Zacchaeus: counting, then up and out to the end of his table
    zb = Actor("b_zac", (SEAT[0], ZST_Y), BK, zac_b_markup, 10.15, 211, g0, gB)
    count_keys = [("count", k / 6) for k in range(6)]
    zb.loop(0, count_keys, 0.11)
    t_glint = snap(t_shou + 0.15)
    zb.cut(t_rich - 0.08, ("count", 0.5, "delighted"), dip=5)
    zb.loop(t_rich + 0.75, [("count", k / 6, "delighted") for k in range(6)], 0.11)
    t_up = snap(t_keshi + 0.02)
    zb.cut(t_up, ("stand", "smug"))
    zb.extra.append(hopm(t_up, BK, 24, 0.32))
    n_strut = 5
    first = (ZEND[0] - SEAT[0]) / BK - (n_strut - 1) * ZAC_STRUT[0][1]
    t_s0 = t_up + 0.42
    zb.walk(t_s0, ZAC_STRUT, n_strut, 0.25, 1, first_adv=first, slope=(ZEND[1] - ZST_Y) / (ZEND[0] - SEAT[0]))
    t_arrive = snap(t_s0 + 0.25 * n_strut)
    zb.cut(t_arrive, ("stand", "smug"), dip=5)
    t_give = snap(t_yin + 0.2)
    zb.cut(t_give, ("give", "smug"), dip=5)
    t_sly = snap(t_duo - 0.12)
    zb.cut(t_sly, ("give", "sly"))
    t_pocket = snap(t_fang + 0.02)
    zb.cut(t_pocket, ("stand", "sly"), dip=5)
    zb.cut(snap(t_kou + 0.35), ("stand", "smug"))
    zb.extra.append(breathm(g0, 2.9, 0.010))
    zb.blinks([t_arrive + 0.5, t_pocket + 1.2], {("stand", "smug"): ("stand", blink("smug"))})
    zb.build(sc)
    sc.add("b_booth_front", b_booth_svg("front"), z=10.2, seed=207, motion=gB)

    # the first payer: reaches over the table corner, drops three coins, frowns, walks off grumbling (down-right)
    p1 = Actor("b_p1", P1, BK, lambda k: folk_markup(*P1, BK, "man", 1, k, -1), 10.4, 221, g0, gB)
    p1.cut(0, ("stand", "grumble"))
    t_pay1 = snap(t_xiang - 0.05)
    p1.cut(t_pay1, ("pay", "grumble", -1, 0.0, None, True), dip=5)
    p1.cut(t_pay1 + 0.35 + 0.22 * 2 + 0.02, ("pay", "grumble", -1, 0.0, None, False))
    t_p1f = snap(t_pay1 + 1.25)
    p1.cut(t_p1f, ("frown", "cross"), dip=5)
    t_p1w = snap(t_p1f + 0.55)
    p1.walk(t_p1w, (("grumble_walk_a", 84), ("grumble_walk_b", 84)), 14, 0.3, 1, first_adv=40, slope=0.1)
    p1.ents = [(tk, (k if isinstance(k, tuple) else (k, "grumble", 1))) for tk, k in p1.ents]
    p1.extra.append(breathm(g0, 3.1, 0.01, 0.3))
    p1.build(sc)
    # coins hopping from his palm onto the heap
    hp1 = C.body_points(C.jericho_folk, *P1, BK, -1, kind="man", variant=1, pose="pay")["hands"][1]
    for j in range(3):
        tc = t_pay1 + 0.35 + 0.22 * j
        cs = doc(PR.coin(*hp1, BK * 0.8, tilt=0.3))
        dxh, dyh = HEAP[0] + 14 * (j - 1) - hp1[0], HEAP[1] - 4 * j - hp1[1]

        def cm(t, tc=tc, dxh=dxh, dyh=dyh):
            if t < tc - 0.2 or t > tc + 0.32:
                return Tf(alpha=0.0)
            if t < tc:
                return Tf(alpha=1.0)
            u = (t - tc) / 0.3
            return Tf(dx=dxh * u, dy=dyh * u - 70 * math.sin(math.pi * u), alpha=1.0 if u < 1 else 0.0)
        sc.add(f"b_coin{j}", cs, z=10.42, wc=0.4, seed=230 + j, motion=M.combine(cm, gB))
        sc.sfx("coins", tc + 0.3, gain_db=-14, pan=-0.1)

    # the farmer (the one he overcharges) and the rest of the queue
    fm = Actor("b_farmer", FARMER, BK, lambda k: folk_markup(*FARMER, BK, "farmer", 0, k, -1), 10.38, 241, g0, gB)
    fm.cut(0, ("stand", "grumble"))
    fm.cut(snap(t_bu + 0.05), ("frown", "cross"), dip=5)
    t_fpay = snap(t_yin + 0.05)
    fm.cut(t_fpay, ("pay", "grumble", -1, 0.0, None, True), dip=5)
    t_coinA = t_chang
    t_surp = snap(t_duo + 0.25)
    fm.cut(t_surp, ("pay", "surprised", -1, 0.0, None, False), dip=4)
    t_fcross = snap(t_surp + 0.75)
    fm.cut(t_fcross, ("frown", "cross"), dip=5)
    t_fwalk = snap(max(t_kou + 0.15, t_fcross + 0.6))
    fm.walk(t_fwalk, (("grumble_walk_a", 86), ("grumble_walk_b", 86)), 7, 0.3, 1, first_adv=40, slope=0.1)
    fm.ents = [(tk, (k if isinstance(k, tuple) else (k, "grumble", 1))) for tk, k in fm.ents]
    fm.extra.append(breathm(g0, 3.0, 0.01, 0.6))
    fm.blinks([4.0 + t_cutB, t_cutB + 7.3], {("stand", "grumble"): ("stand", blink("grumble"))})
    fm.build(sc)
    for i, (kind, v, x, y, p0) in enumerate(QUEUE):
        q = Actor(f"b_q{i}", (x, y), BK, lambda k, kind=kind, v=v, x=x, y=y: folk_markup(x, y, BK, kind, v, k, -1),
                  10.36 - 0.01 * i, 251 + i, g0, gB)
        q.cut(0, (p0, "grumble"))
        q.cut(snap(t_bu + 0.15 + 0.2 * i), ("arms_folded", "grumble", 1 if i == 0 else -1), dip=5)
        q.cut(snap(t_kou + 0.1 + 0.25 * i), ("mutter", "mutter", 1 if i == 0 else -1), dip=4)
        q.extra.append(breathm(g0, 3.2 + 0.3 * i, 0.01, 0.2 * i))
        q.blinks([t_cutB + 2.1 + i, t_cutB + 6.4 + i, t_cutB + 10.8], {(p0, "grumble"): (p0, blink("grumble"))})
        q.build(sc)

    # coins in Zacchaeus's hand: A from the farmer ('常'), B snatched ('多收'), both into the pouch ('放进')
    def zpts(pose):
        x, y = ZEND
        return C.zacchaeus_points(x, y, BK, 1, pose=pose, coins=False)
    zh = zpts("give")["hands"][0]
    zpurse = zpts("stand")["purse"]
    fh = C.body_points(C.jericho_folk, *FARMER, BK, -1, kind="farmer", variant=0, pose="pay")["hands"][1]
    for j, (t_on, src) in enumerate(((t_coinA, fh), (t_duo + 0.02, fh))):
        land = (zh[0] + 2 + 12 * j, zh[1] - 6 - 4 * j)
        cs = doc(PR.coin(*land, BK * 0.8, tilt=0.4))

        def cm(t, t_on=t_on, src=src, land=land, j=j):
            dur = 0.24 if j == 0 else 0.16
            t_p0 = t_pocket + 0.02
            if t < t_on:
                return Tf(alpha=0.0)
            if t < t_on + dur:
                u = M.ease("out")((t - t_on) / dur)
                return Tf(dx=(src[0] - land[0]) * (1 - u), dy=(src[1] - land[1]) * (1 - u) - 40 * math.sin(math.pi * u))
            if t < t_p0:
                return Tf()
            u = (t - t_p0) / 0.3
            if u >= 1:
                return Tf(alpha=0.0)
            return Tf(dx=(zpurse[0] - land[0]) * M.ease("inout")(u), dy=(zpurse[1] - land[1]) * M.ease("inout")(u) -
                      30 * math.sin(math.pi * u), sx=1 - 0.4 * u, sy=1 - 0.4 * u, px=land[0], py=land[1])
        sc.add(f"b_zcoin{j}", cs, z=10.17 if j else 10.171, wc=0.4, seed=260 + j, motion=M.combine(cm, gB))
        sc.sfx("coins", t_on + (0.24 if j == 0 else 0.16), gain_db=-12)
    sc.sfx("coins", t_pocket + 0.3, gain_db=-11)
    sc.add("b_purse_tw", doc(sparkle(zpurse[0] + 6, zpurse[1] - 10, 20)), z=10.19, wc=0, seed=265,
           motion=M.combine(popm(snap(t_pocket + 0.32), (zpurse[0] + 6, zpurse[1] - 10), 0.3, t_out=t_pocket + 1.1,
                                 out_dur=0.3), gB))
    # a glint on the coin he taps on '收税的人'
    sc.add("b_glint", doc(sparkle(HEAP[0] + 54, HEAP[1] - 30, 22)), z=10.21, wc=0, seed=266,
           motion=M.combine(popm(t_glint, (HEAP[0] + 54, HEAP[1] - 30), 0.3, t_out=t_glint + 0.9, out_dur=0.3), gB))

    # the money chest and the two tax collectors bringing bags of money
    chest_fr = [chest_svg(0.45, 0.0), chest_svg(0.7, 0.0), chest_svg(1.0, 0.0), chest_svg(1.0, 0.5, True),
                chest_svg(1.0, 1.0, True)]
    t_pour1 = snap(t_guan + 0.35)
    t_pour2 = snap(min(t_pour1 + 0.75, t_rich - 1.25))
    t_over = snap(t_rich - 0.05)

    def chest_fa(t):
        if t < t_pour1 + 0.4:
            return 0.0
        if t < t_pour2 + 0.4:
            return 1.0
        if t < t_over:
            return 2.0
        return 3.0 + 0.5 + 0.5 * math.sin(2 * math.pi * (t - t_over) / 1.1 - math.pi / 2)
    sc.add("b_chest", chest_fr, z=10.3, seed=271, frame_at=chest_fa,
           motion=M.combine(lambda t: Tf(px=CHEST[0], py=CHEST[1]), dipm(t_over, CHEST[2], 6), gB))
    sc.fx.append(lambda frame, t, view, f=FX.sparkles((CHEST[0] - 110, CHEST[1] - 260, CHEST[0] + 110, CHEST[1] - 130),
                                                      count=12, t0=t_over, t1=t_cutC, seed=31, size=(8, 16)):
                 f(frame, t, view) if t_cutB <= t < t_cutC else frame)
    sc.sfx("sparkle", t_over, gain_db=-12)
    for ci, (cpos, t_arr, kind, v, t_pour) in enumerate(((COL1, t_pour1 - 0.45, "man", 3, t_pour1),
                                                        (COL2, t_pour2 - 0.45, "man", 5, t_pour2))):
        cyc = folk_walk(kind)
        nst = 6
        a = Actor(f"b_col{ci}", cpos, BK, None, 10.5 + 0.01 * ci, 281 + ci, g0, gB)
        a.draw = (lambda k, cpos=cpos, kind=kind, v=v:
                  folk_markup(*cpos, BK, kind, v, k if isinstance(k, tuple) else (k, "neutral", 1, 0.0, "sack"), 1))
        t_w0 = t_arr - nst * 0.27 - 0.1
        a.cut(0, "walk_b")
        a.walk_in(t_w0, cyc, nst, 0.27, 1)
        t_stop = snap(t_w0 + nst * 0.27)
        a.cut(t_stop, ("stand", "smug", 1, 0.0, "sack"), dip=5)
        a.cut(t_pour - 0.05, ("point", "smug", 1), dip=5)
        a.cut(t_pour + 0.6, ("smile", "happy", 1), dip=4)
        t_off = snap(t_over + 0.7 + 0.3 * ci)
        a.walk(t_off, (("walk_a", FOLK_ADV[kind]), ("walk_b", FOLK_ADV[kind])), 9, 0.27, -1, first_adv=30)
        a.ents = [(tk, (k, "happy", -1) if isinstance(k, str) and tk >= t_off else k) for tk, k in a.ents]
        a.extra.append(breathm(g0, 3.0, 0.01, 0.4 * ci))
        a.build(sc)
        # the bag flies from his hand to the chest, tips (coins pour) and drops empty beside it
        hand = C.body_points(C.jericho_folk, *cpos, BK, 1, kind=kind, variant=v, pose="stand", item="sack")["hands"][1]
        sx0, sy0 = hand[0] - 4, hand[1] + 44
        rim = (CHEST[0] - 30 + 30 * ci, CHEST[1] - 150 * CHEST[2])
        rest = (CHEST[0] - 150 - 40 * ci, CHEST[1] + 8 + 6 * ci)
        full = doc(coin_sack(sx0, sy0, BK * 0.55))

        def bag_m(t, t_pour=t_pour, sx0=sx0, sy0=sy0, rim=rim, rest=rest):
            if t < t_pour - 0.05:
                return Tf(alpha=0.0)
            u = t - (t_pour - 0.05)
            if u < 0.3:                          # the toss up to the rim
                v_ = M.ease("out")(u / 0.3)
                return Tf(dx=(rim[0] - sx0) * v_, dy=(rim[1] - sy0) * v_ - 90 * math.sin(math.pi * v_ * 0.9),
                          rot=110 * v_, px=sx0, py=sy0 - 28)
            if u < 0.75:                         # pouring
                return Tf(dx=rim[0] - sx0, dy=rim[1] - sy0 + 4 * math.sin(u * 30), rot=110 + 15 * math.sin((u - 0.3) * 14),
                          px=sx0, py=sy0 - 28)
            if u < 1.05:                         # drops beside the chest
                v_ = M.ease("in")((u - 0.75) / 0.3)
                return Tf(dx=rim[0] - sx0 + (rest[0] - rim[0]) * v_, dy=rim[1] - sy0 + (rest[1] - rim[1]) * v_,
                          rot=110 + (250 - 110) * v_, px=sx0, py=sy0 - 28, alpha=0.0)
            return Tf(alpha=0.0)
        sc.add(f"b_bag{ci}", full, z=10.55, seed=291 + ci, motion=M.combine(bag_m, gB))
        rest_svg = doc(coin_sack(*rest, BK * 0.6, empty=True))
        sc.add(f"b_bagrest{ci}", rest_svg, z=10.29, seed=293 + ci,
               motion=M.combine(lambda t, t_pour=t_pour: Tf(alpha=1.0 if t >= t_pour + 1.0 else 0.0),
                                dipm(t_pour + 1.0, BK, 4), gB))
        # coins tumbling out of the bag into the chest
        for j in range(5):
            tj = t_pour + 0.3 + 0.08 * j
            cx_, cy_ = rim[0] + 30 - 12 * j, rim[1] - 20
            cs = doc(PR.coin(cx_, cy_, BK * 0.75, tilt=0.2 + 0.1 * j))

            def ccm(t, tj=tj, j=j):
                if t < tj or t > tj + 0.35:
                    return Tf(alpha=0.0)
                u = (t - tj) / 0.35
                return Tf(dx=(j - 2) * 10 * u, dy=40 * u * u + 10 * u, rot=200 * u)
            sc.add(f"b_pour{ci}_{j}", cs, z=10.56, wc=0.3, seed=300 + 10 * ci + j, motion=M.combine(ccm, gB))
        sc.sfx("coins", t_pour + 0.32, gain_db=-11, pan=-0.4)
        sc.sfx("coins", t_pour + 0.5, gain_db=-14, pan=-0.4)
        sc.sfx("thud", t_pour + 1.0, gain_db=-16, pan=-0.4)
    sc.sfx("footsteps", t_guan - 1.8, dur=2.6, gain_db=-20, pan=-0.5)

    # the name tag and the emperor bubble
    head = C.body_points(C.zacchaeus, *SEAT, BK, 1, pose="count")["head"]
    tag_tip = (head[0] + 4, head[1] - 82)
    t_tag = snap(t_name - 0.05)
    sc.add("b_tag", doc(name_tag(*tag_tip, "撒该")), z=10.8, wc=0, seed=310,
           motion=M.combine(popm(t_tag, (tag_tip[0], tag_tip[1] - 40), t_out=tm.end(2, "撒该是收税的人") + 0.4), gB))
    sc.sfx("pop", t_tag, gain_db=-10)
    bub = (1270, 300, 190)
    t_bub = snap(t_rome - 0.05)
    t_bub_out = tm.end(3, "向大家收钱的人") + 0.35
    sc.add("b_bubble", doc(emperor_bubble(*bub, (head[0] + 60, head[1] - 60))), z=10.81, wc=0.3, seed=312,
           motion=M.combine(popm(t_bub, (bub[0], bub[1] + 60), 0.4, t_out=t_bub_out), gB))
    sc.sfx("pop", t_bub, gain_db=-9)
    sc.sfx("chime", t_bub + 0.05, gain_db=-19)
    # foreground palm
    bp = [(2060, 1240, 1.0, -1, 1.25, 0.08, 51)]
    add_palms(sc, "b_palm", bp, 10.9, 320, g0, gB, 0.45, 3.3, 0.2)
    camB = cam_keys([(t_cutB, Cam(1000, 610, 1980)), (t_name + 0.6, Cam(940, 630, 1820)),
                     (t_rome - 0.8, Cam(940, 630, 1820)), (t_rome + 0.3, Cam(1040, 590, 1900)),
                     (t_guan - 1.2, Cam(1040, 590, 1900)), (t_guan + 0.2, Cam(900, 610, 1880)),
                     (t_keshi + 0.2, Cam(900, 610, 1880)), (t_yin, Cam(1170, 640, 1700)),
                     (t_cutC, Cam(1180, 645, 1680))],
                    ["sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear"])

    # ------------------------------------------------------------ SHOT C: the street
    add_street_set(sc, gC, g0, z=50.0)
    t_see = tm.at(6, "大家看见撒该", 0)
    t_duo3 = tm.at(6, "都躲得远远的", 0)
    t_yuan = tm.at(6, "都躲得远远的", 3)
    zc = Actor("c_zac", (Z_C0, ZY), SK, zac_c_markup, 52.0, 401, g0, gC)
    t_c0 = t_cutC + 0.05
    zc.cut(0, ("strut_b", "smug"))
    end_t = zc.walk(t_c0, ZAC_STRUT, C_STRUT_N, 0.27, 1)
    t_slow = snap(end_t)
    zc.walk(t_slow, ZAC_WALK, C_WALK_N, 0.26, 1, first_adv=C_WALK_FIRST)
    t_lonely = snap(t_slow + C_WALK_N * 0.26 + 0.05)
    zc.cut(t_lonely, ("lonely", "lonely"), dip=4)
    zc.ents = [(tk, (k if isinstance(k, tuple) else (k, "smug" if k.startswith("strut") else "worried")))
               for tk, k in zc.ents]
    zc.extra.append(breathm(g0, 3.0, 0.010))
    zc.build(sc)
    assert abs(zc.off(T)[0] - street_final()["zac"][1][0]) < 0.5
    zc_end_x = zc.pos(T)[0]
    sc.sfx("footsteps", t_c0, dur=t_lonely - t_c0, gain_db=-19)
    # the people stepping aside: (name, step-aside time, offset (dx, dy), steps, pose sequence)
    folk_plan = add_street_folk(sc, g0, gC, t_cutC, t_see, t_duo3, t_yuan, zc_end_x)
    del folk_plan

    # ------------------------------------------------------------ camera
    camC = cam_keys([(t_cutC, Cam(1000, 610, 1960)), (t_lonely, street_cam_end()), (T, street_cam_end())], "sine")

    def cam(t):
        if t < t_cutB:
            return camA(t)
        if t < t_cutC:
            return camB(t)
        return camC(t)
    sc.camera = cam

    # ------------------------------------------------------------ sound
    sc.sfx("birds", 0, dur=t_cutB + 0.3, gain_db=-22, fade_in=0.8, fade_out=0.4)
    sc.sfx("wind_soft", 0, dur=t_cutB + 0.3, gain_db=-24, fade_in=0.8, fade_out=0.4)
    sc.sfx("footsteps", 0.3, dur=t_cutB - 0.5, gain_db=-26, fade_in=0.5)
    sc.sfx("crowd", t_cutB, dur=T - t_cutB + 0.5, gain_db=-21, fade_in=0.2, fade_out=1.0)
    sc.sfx("birds", t_cutB, dur=T - t_cutB + 0.5, gain_db=-27, fade_out=1.0)
    for k in range(int((t_rich - t_cutB) / 1.32)):
        tc = t_cutB + 0.3 + 1.32 * k
        if abs(tc - t_xiang) > 0.6:
            sc.sfx("coins", tc, gain_db=-22, pan=-0.1)
    sc.sfx("pop", t_up, gain_db=-17)
    return sc


def street_folk_entries(t_cutC, t_see, t_duo3, t_yuan, zc_end_x):
    """Per person: list of (t, key) cuts, list of (t0, cycle, n, per, facing, slope) walks. The final state is what
    s04_crowd starts from (it uses the same tables)."""
    plans = {}
    tg = t_duo3                                    # '躲' - they step out of his way (all done 1.3 s before the end)
    # mother and child: she pulls the child back (two steps up toward the road) and both turn away and whisper
    plans["mum"] = dict(cuts=[(0, ("smile", "happy", 1)), (tg - 0.4, ("frown", "worried", 1)), (tg + 0.55, ("walk_a", "worried", 1)),
                              (tg + 1.15, ("mutter", "mutter", 1))],
                        walks=[(tg + 0.55, (("walk_a", 81), ("walk_b", 81)), 2, 0.28, 1, -0.55)])
    plans["kid"] = dict(cuts=[(0, ("look", "kind", -1)), (tg - 0.2, ("frown", "worried", 1)), (tg + 0.6, ("walk_a", "worried", 1)),
                              (tg + 1.1, ("frown", "worried", 1))],
                        walks=[(tg + 0.6, (("walk_a", 50), ("walk_b", 50)), 2, 0.24, 1, -0.6)])
    # the two men: turn their backs and mutter
    plans["men1"] = dict(cuts=[(0, ("mutter", "mutter", 1)), (tg - 0.1, ("frown", "cross", 1)), (tg + 0.45, ("walk_b", "cross", 1)),
                               (tg + 1.05, ("mutter", "mutter", 1))],
                         walks=[(tg + 0.45, (("walk_b", 84), ("walk_a", 84)), 2, 0.28, 1, -0.45)])
    plans["men2"] = dict(cuts=[(0, ("mutter", "mutter", -1)), (tg + 0.05, ("frown", "cross", -1)), (tg + 0.5, ("walk_a", "cross", 1)),
                               (tg + 1.15, ("mutter", "mutter", -1))],
                         walks=[(tg + 0.5, (("walk_a", 86), ("walk_b", 86)), 2, 0.28, 1, -0.2)])
    plans["elder"] = dict(cuts=[(0, ("stand", "kind", 1)), (t_see + 0.5, ("frown", "grumble", 1)), (tg + 0.2, ("arms_folded", "grumble", -1))],
                          walks=[])
    plans["w1"] = dict(cuts=[(0, ("mutter", "mutter", 1)), (t_see + 0.9, ("look", "worried", 1)), (tg + 0.3, ("mutter", "mutter", 1))],
                       walks=[])
    plans["w2"] = dict(cuts=[(0, ("mutter", "mutter", -1)), (t_see + 0.6, ("look", "worried", 1)), (tg + 0.15, ("mutter", "mutter", -1))],
                       walks=[])
    plans["fs"] = dict(cuts=[(0, ("smile", "happy", -1)), (t_see + 1.2, ("frown", "worried", -1)), (tg + 0.45, ("arms_folded", "grumble", 1))],
                       walks=[])
    plans["m3"] = dict(cuts=[(0, ("stand", "kind", -1)), (tg + 0.5, ("frown", "cross", 1))], walks=[])
    del t_yuan, zc_end_x
    return plans


def street_final():
    """The street page's end state (s04_crowd starts from it): {name: (key, (dx, dy))} for the people and 'zac'."""
    plans = street_folk_entries(0.0, 0.0, 0.0, 0.0, 0.0)
    out = {}
    for name, plan in plans.items():
        dx = dy = 0.0
        for (t0, cyc, n, per, f, slope) in plan["walks"]:
            d = sum(cyc[i % len(cyc)][1] for i in range(n)) * SK * f
            dx += d
            dy += d * slope
        out[name] = (plan["cuts"][-1][1], (dx, dy))
    zd = (C_STRUT_N * ZAC_STRUT[0][1] + C_WALK_FIRST + sum(ZAC_WALK[i % 4][1] for i in range(1, C_WALK_N))) * SK
    out["zac"] = (("lonely", "lonely"), (zd, 0.0))
    return out


def street_z(name):
    y = STREET_FOLK[name]["home"][1]
    return 51.0 + y / 10000.0 + (1.2 if y > ZY else 0.0)


def street_folk_actor(name, g0, gatef, z, seed, plan, tshift=0.0):
    d = STREET_FOLK[name]
    a = Actor(f"c_{name}", d["home"], SK, lambda k, name=name: street_folk_markup(name, k), z, seed, g0, gatef)
    for t, k in plan["cuts"]:
        a.cut(t - tshift if t > 0 else 0, k, dip=4 if t > 0 and not k[0].startswith("walk") else None)
    for (t0, cyc, n, per, f, slope) in plan["walks"]:
        a.walk(t0 - tshift, [((c[0], plan_expr(plan, t0), f), c[1]) for c in cyc], n, per, f, slope=slope)
    return a


def plan_expr(plan, t0):
    e = "neutral"
    for t, k in plan["cuts"]:
        if t <= t0 + 1e-6:
            e = k[1]
    return e


def street_breath(g0, i):
    return breathm(g0, 3.0 + 0.2 * (i % 4), 0.010, 0.17 * i)


def street_folk_order():
    return sorted(STREET_FOLK, key=lambda n: STREET_FOLK[n]["home"][1])


def add_street_folk(sc, g0, gatef, t_cutC, t_see, t_duo3, t_yuan, zc_end_x):
    plans = street_folk_entries(t_cutC, t_see, t_duo3, t_yuan, zc_end_x)
    for i, name in enumerate(street_folk_order()):
        a = street_folk_actor(name, g0, gatef, street_z(name), 410 + i, plans[name])
        a.extra.append(street_breath(g0, i))
        a.build(sc)
    return plans
