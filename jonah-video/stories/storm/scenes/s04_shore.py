"""Scene 4 — Mark 4:1-2. The lakeshore of Galilee by day: a fishing village of dark basalt houses with a palm, nets
drying on a pole frame, green hills round the lake, little boats far out. A fishing boat is moored in the shallows
with a gangplank down to the beach; four disciples stand in it. Jesus stands at the water's edge and teaches; people
come walking from the village, more and more of them; when the crowd is too big Jesus walks up the plank into the
boat, sits on the stern and tells his stories; everybody sits down on the sand and listens quietly, the children in
front leaning forward.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers, proportional fallback):
  0 .. 0.9      calm medium shot: Jesus teaching a few people by the boat; water glints, clouds drift, the pennant
                flutters, little boats sail far out
  '耶稣'         a teaching gesture (hard pose cuts are hidden in small squash dips everywhere)
  '耶稣在'       the first villagers walk in from the left (planted-foot strides)
  '教导很多很多人' the camera pulls back to the whole beach; on each '很多' a new wave of people walks in from the
                village side (children hurrying in front)
  '人太多了'     the people at the front press closer; Jesus turns and walks up the plank (footsteps)
  '坐'           he sits down on the stern (the boat dips under him: a little splash); '讲' he starts telling,
                the open hand out
  '大家都安安静静' everybody sits down in a ripple from Jesus outward (cloth), the crowd murmur and the breeze hush,
                two little birds fly in and settle on the yard of the boat
  '连小孩子'     the camera moves down to the children in the front row; on '听得' they lean forward, on '认真' they
                nod; calm hold (page dip to s05)
The geometry, backdrop drawings and the Actor / timing helpers are shared with s05_seed.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, cuts, dip, snap, voice_marks

INK = P["ink"]

# ------------------------------------------------------------------ geometry (shared with s05_seed)
SHORE = 770                  # near shoreline (lake_galilee y)
LS = 0.66                    # lake / landscape scale
YF = SHORE - 250 * LS        # far shoreline
BX, BY, BK = 1530, 758, 0.6  # the fishing boat: waterline anchor, scale (people at the same scale)
BPTS = PR.boat_points(BX, BY, BK, 1)
SEAT = BPTS["stern_seat"]    # Jesus sits here (facing -1, toward the crowd)
JB = (966, 848)              # Jesus on the beach (next to the foot of the plank)
PLANK0, PLANK1 = (1003, 848), (1282, 666)   # gangplank: foot on the beach, top on the stern gunwale
YARD_Y = BY + PR.BOAT_YARD_Y * BK            # the furled sail's yard (birds perch on it)
DAY_SKY = ("#8fc4dc", "#bfe0e8", "#e6f2ec")
STRIDE = {"jesus": 87, "man": 84, "woman": 81, "child": 50, "elder": 83, "disciple": 88}

for _e in ("warm", "kind", "happy", "smile", "neutral", "calm", "worried", "awed", "peaceful"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"sb_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"sb_blink_{expr}"


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def f1(v):
    return f"{v:.1f}"


# ------------------------------------------------------------------ voice timing


def timer(ctx):
    """at(li, text, k=0): onset of character k of ``text`` in line li, measured in the voice clip (voice_marks), with
    a proportional fallback inside the line (a re-generated voice stays in sync)."""
    marks = [voice_marks(ctx, i) for i in range(len(ctx.lines))]

    def at(li, text, k=0):
        for m in marks[li]:
            if text in m[0]:
                ct = char_times(m)
                return ct[min(m[0].index(text) + k, len(ct) - 1)]
        ln = ctx.lines[li]
        i = max(0, ln.text.find(text)) + k
        return ln.start + (ln.end - ln.start) * i / max(1, len(ln.text))
    return at


# ------------------------------------------------------------------ actors


def on_boat(local, boat):
    """Compose a figure's own motion (rotations / scales about its own pivot) with the boat's motion (rotation about
    the boat's anchor + translation) as a single Tf: M.combine would rotate everything about one pivot only."""
    def m(t):
        L = local(t) if local is not None else Tf()
        B = boat(t)
        r = math.radians(B.rot)
        c, s_ = math.cos(r), math.sin(r)
        bpx, bpy = (B.px, B.py) if B.px is not None else (0.0, 0.0)
        if L.px is None:
            vx, vy = L.dx, L.dy
            return Tf(dx=c * vx - s_ * vy + B.dx, dy=s_ * vx + c * vy + B.dy, rot=B.rot + L.rot, sx=L.sx, sy=L.sy,
                      alpha=L.alpha * B.alpha, px=bpx, py=bpy)
        qx, qy = L.px + L.dx - bpx, L.py + L.dy - bpy
        return Tf(dx=c * qx - s_ * qy + bpx + B.dx - L.px, dy=s_ * qx + c * qy + bpy + B.dy - L.py, rot=B.rot + L.rot,
                  sx=L.sx, sy=L.sy, alpha=L.alpha * B.alpha, px=L.px, py=L.py)
    return m


class Actor:
    """One character on its own layer: named drawings shown with hard cuts (each hidden in a small squash dip),
    optional blinks, extra motions. ``draw(name)`` returns the markup of drawing ``name``."""

    def __init__(self, name, draw, piv, s, z, seed=0, docf=None, carrier=None):
        self.name, self.draw, self.piv, self.s, self.z, self.seed = name, draw, piv, s, z, seed
        self.docf = docf or doc
        self.carrier = carrier          # a boat motion the figure rides on (see on_boat)
        self.names, self.ents, self.dips, self.mots = [], [], [], []

    def _idx(self, n):
        if n not in self.names:
            self.names.append(n)
        return self.names.index(n)

    def cut(self, t, n, dip_=True, depth=7.0):
        t = snap(t) if t > 0 else 0.0
        self.ents.append((t, n))
        self._idx(n)
        if dip_ and t > 0:
            self.dips.append((t, depth))
        return self

    def state_at(self, t):
        cur = None
        for tk, n in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = n
        return cur

    def add_blinks(self, pairs, T, rng, every=(2.3, 4.2), t_from=0.5):
        """pairs: {open drawing: closed-eye drawing}; 0.13 s blinks while an open drawing shows, never near a cut."""
        t = t_from + rng.uniform(0.2, 2.0)
        extra = []
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < T - 0.5:
            cur = self.state_at(t)
            if cur in pairs and all(abs(t - tk) > 0.35 for tk in cut_ts):
                extra += [(snap(t), pairs[cur]), (snap(t + 0.13), cur)]
                self._idx(pairs[cur])
            t += rng.uniform(*every)
        self.ents += extra
        return self

    def build(self, sc, wc=1.0):
        ents = sorted(self.ents, key=lambda e: e[0])
        fr = [self.docf(self.draw(n)) for n in self.names]
        mots = [dip(td, self.s, self.piv, depth) for td, depth in self.dips] + self.mots
        fa = cuts([(tk, self.names.index(n)) for tk, n in ents]) if len(fr) > 1 else None
        piv = self.piv
        local = M.combine(lambda t: Tf(px=piv[0], py=piv[1]), *mots)
        motion = on_boat(local, self.carrier) if self.carrier is not None else (M.combine(*mots) if mots else None)
        sc.add(self.name, fr if len(fr) > 1 else fr[0], frame_at=fa, z=self.z, seed=self.seed, wc=wc, motion=motion)
        return self


def walk_path(t0, steps, period, s=0.5, lift=6.0, move=0.15, first=0):
    """Planted-foot walk with two stride drawings. steps: list of (dx, dy) per stride; the anchor advances one stride
    across each cut. Returns ([(t, 'walk_a'|'walk_b')], offset(t) -> (dx, dy) from the start, t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(len(steps))]
    t_end = snap(t0 + len(steps) * period)
    ents = [(tc, "walk_a" if (k + first) % 2 == 0 else "walk_b") for k, tc in enumerate(cut_t)]

    def off(t):
        x = y = 0.0
        for tk, (sx, sy) in zip(cut_t, steps):
            u = M.progress(t, tk - move * 0.45, tk + move * 0.55, "sine")
            x += sx * u
            y += sy * u
            if tk - move * 0.45 <= t <= tk + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - tk + move * 0.45) / move)
        return x, y
    return ents, off, t_end


def boat_motion(t_dips=(), amp=2.0, rot=0.4, period=4.2, g0=0.0):
    """The moored boat bobbing gently on the water (rotation about its waterline anchor); a dip when someone steps
    in. g0 = the scene's global start time, so neighbouring scenes rock in step."""
    def m(t):
        g = t + g0
        dy = amp * math.sin(2 * math.pi * g / period)
        r = rot * math.sin(2 * math.pi * (g / period + 0.3))
        for td in t_dips:
            u = t - td
            if 0 <= u < 0.9:
                dy += 6 * math.sin(math.pi * u / 0.9) * (1 - u / 0.9) * 1.6
        return Tf(dy=dy, rot=r, px=BX, py=BY)
    return m


# ------------------------------------------------------------------ backdrop (day)


def sky_svg():
    defs = (S.lin_grad("s4sky", [(0, DAY_SKY[0]), (0.55, DAY_SKY[1]), (1, DAY_SKY[2])]) +
            S.rad_grad("s4sun", [(0, "#fff8dc", 0.9), (0.5, "#fff2c8", 0.35), (1, "#fff2c8", 0)]))
    b = S.rect_bg("url(#s4sky)") + '<circle cx="1830" cy="120" r="460" fill="url(#s4sun)"/>'
    return doc(b, defs)


def clouds_svg():
    sh = S.mix(DAY_SKY[1], "#ffffff", 0.2)
    fill = S.mix("#fbf4ea", "#d8ecee", 0.3)
    b = (S.cloud(300, 150, 330, 104, fill, seed=41, sw=3.2, shade_fill=sh) +
         S.cloud(1120, 96, 270, 86, fill, seed=42, sw=3.0, shade_fill=sh) +
         S.cloud(1840, 250, 220, 72, fill, seed=43, sw=2.8, shade_fill=sh) +
         S.cloud(700, 330, 170, 54, fill, seed=44, sw=2.4, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def lake_back_svg(time="day"):
    return doc(PR.lake_galilee(-40, W + 40, SHORE, LS, time=time, part="back", sky=False, boats=False, seed=3))


def far_boat_svg(x, y, k, f, variant):
    return doc(PR.small_boat(x, y, k, f, variant=variant, sail="full" if variant == 1 else "none"))


def glints_svg(seed, time="day"):
    """Short light ripple strokes over the lake (two such layers drift and pulse: the water glitters)."""
    lite = {"day": "#eef8f6", "sunset": "#ffe2a8"}[time]
    rng = random.Random(seed)
    b = ""
    for _ in range(70):
        u = rng.random()
        y = YF + 14 + (SHORE - YF - 24) * u ** 1.2
        x = rng.uniform(-200, W + 200)
        L = (18 + 70 * u) * rng.uniform(0.7, 1.2)
        b += (f'<path d="M{f1(x)},{f1(y)} q{f1(L / 2)},{f1(-2 - 2 * u)} {f1(L)},0" fill="none" stroke="{lite}" '
              f'stroke-width="{f1(2 + 2.5 * u)}" stroke-linecap="round" opacity="{0.45 + 0.4 * u:.2f}"/>')
    return doc(b)


def band_svg(time="day", phase=0.0):
    return doc(PR.lake_band(-40, W + 40, BY - 4, SHORE + 8, time, phase=phase, scale=LS, seed=5))


def shore_svg(time="day"):
    """The beach with the village (left), reeds and pebbles, nets drying on a pole frame (right)."""
    b = PR.lake_galilee(-40, W + 40, SHORE, LS, time=time, part="shore", village="left", nets=False, boats=False,
                        bottom=H + 60, seed=3)
    b += PR.fishing_net(2000, 848, 0.6, kind="pole", time=time)
    return doc(b)


def plank_svg():
    """A sturdy gangplank from the beach up to the stern gunwale: a thick board (top face + darker side), wood grain,
    cleats for the feet, a rope lashing at the top."""
    (x0, y0), (x1, y1) = PLANK0, PLANK1
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    wood, side = "#c09060", "#8a6040"
    b = f'<g transform="translate({f1(x0)},{f1(y0)}) rotate({a:.2f})">'
    b += (f'<path d="M-10,0 L{f1(L + 8)},0 L{f1(L + 8)},22 Q{f1(L / 2)},26 -10,22 Z" fill="{side}" stroke="{INK}" '
          f'stroke-width="3.4" stroke-linejoin="round"/>')
    b += (f'<path d="M-14,-12 L{f1(L + 4)},-12 Q{f1(L + 14)},-6 {f1(L + 8)},2 L-8,2 Q-20,-4 -14,-12 Z" fill="{wood}" '
          f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>')
    b += (f'<path d="M6,-6 Q{f1(L * 0.3)},-8 {f1(L * 0.55)},-5 M{f1(L * 0.35)},-3 Q{f1(L * 0.6)},-1 {f1(L - 10)},-4" '
          f'fill="none" stroke="{S.shade(wood, -0.3)}" stroke-width="2" stroke-linecap="round" opacity="0.8"/>')
    k = 30
    while k < L - 30:
        b += (f'<rect x="{k}" y="-19" width="10" height="9" rx="2.5" fill="{S.shade(wood, -0.12)}" stroke="{INK}" '
              f'stroke-width="2.4"/>')
        k += 42
    rope = f'M{f1(L - 6)},-14 q8,20 0,34 M{f1(L - 16)},-14 q8,20 0,34'
    b += (f'<path d="{rope}" fill="none" stroke="#c9b48a" stroke-width="5" stroke-linecap="round"/>'
          f'<path d="{rope}" fill="none" stroke="{INK}" stroke-width="1.6" opacity="0.6"/>')
    b += "</g>"
    return doc(S.g(b, filter="wobble-fine"))


def tufts_svg(k, time="day"):
    """Foreground grass tufts and reeds in the bottom corners; k = sway frame (0, 1, 2)."""
    sw = (-0.5, 0.0, 0.5)[k]
    b = ""
    for x, y, s, v in ((40, 1180, 1.25, 0), (150, 1196, 1.0, 1), (2070, 1190, 1.2, 2), (1960, 1200, 0.95, 0),
                       (1180, 1196, 0.8, 1)):
        b += PR.grass_tuft(x, y, s, v, sway=sw)
    for x, y, s in ((95, 1160, 0.75), (2020, 1150, 0.7)):
        b += PR.reeds(x, y, s, 1, sway=sw * 0.8)
    return doc(b)


def bird_frames(color, facing=1, scale=0.34, cx=200, cy=200):
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    fly = [doc(PR.songbird(cx, cy, scale, facing, wing=w, color=color)) for w in wings]
    perch = doc(PR.songbird(cx, cy, scale, facing, pose="perch", color=color))
    return fly + [perch]


# ------------------------------------------------------------------ people


def villager_draw(kind, variant, x, y, s, facing, rider=None):
    """draw(name) for a villager: name = 'pose|expr' (expr may be '' = the pose's own)."""
    def d(n):
        pose, expr = n.split("|")
        kw = dict(kind=kind, variant=variant, pose=pose, expr=expr or None)
        if pose == "shoulders":
            kw["rider"] = rider
        sh = C.ground_shadow(x, y, s, 120 if kind != "child" else 84, 0.16) if not pose.startswith("sit") else \
            C.ground_shadow(x + 20 * s * facing, y, s, 170 if kind != "child" else 120, 0.15)
        return sh + C.villager(x, y, s, facing, **kw)
    return d


# id, kind, variant, x, y, scale, facing, standing pose, expression, sitting pose (None: stays up), arrival
# arrival: None (there from the start) or (t_key, start_x, period) - walks in from start_x
CROWD = [
    ("X1", "man", 2, 175, 812, 0.54, 1, "stand", "happy", None, ("w3", -60, 0.30)),
    ("X2", "woman", 3, 300, 816, 0.54, 1, "listen", "kind", None, ("w2", -40, 0.29)),
    ("X3", "man", 5, 548, 810, 0.54, 1, "listen", "kind", None, ("rise", "m1")),
    ("X4", "woman", 4, 672, 814, 0.54, 1, "stand", "happy", None, ("rise", "m2")),
    ("X5", "elder", 0, 792, 810, 0.54, 1, "listen", "kind", None, ("rise", "m3")),
    ("B1", "man", 3, 110, 846, 0.58, 1, "stand", "happy", None, ("w3", -80, 0.28)),
    ("B2", "woman", 1, 230, 852, 0.58, 1, "listen", "kind", None, ("w3", -50, 0.27)),
    ("B3", "elder", 2, 350, 842, 0.58, 1, "listen", "kind", None, ("w2", -50, 0.30)),
    ("B4", "man", 4, 480, 850, 0.58, 1, "shoulders", "kind", None, None),
    ("B5", "woman", 5, 610, 846, 0.58, 1, "listen", "kind", None, ("w1", 328, 0.28)),
    ("B6", "man", 0, 735, 852, 0.58, 1, "listen", "kind", None, None),
    ("B7", "elder", 1, 852, 844, 0.58, 1, "stand", "happy", None, None),
    ("M1", "woman", 2, 170, 938, 0.62, 1, "stand", "happy", "sit", ("w3", -90, 0.27)),
    ("M2", "man", 5, 300, 944, 0.62, 1, "stand", "happy", "sit_listen", ("w2", -60, 0.26)),
    ("M3", "woman", 4, 430, 936, 0.62, 1, "listen", "kind", "sit", ("w2", -50, 0.24)),
    ("M4", "man", 1, 560, 942, 0.62, 1, "stand", "happy", "sit", ("w1", 300, 0.27)),
    ("M5", "woman", 0, 690, 938, 0.62, 1, "listen", "kind", "sit_listen", None),
    ("M6", "man", 2, 820, 944, 0.62, 1, "stand", "happy", "sit", None),
    ("F1", "child", 0, 250, 1020, 0.66, 1, "stand", "happy", "sit_listen", ("w3", -40, 0.18)),
    ("F2", "child", 1, 370, 1026, 0.66, 1, "stand", "happy", "sit_listen", ("w2", -30, 0.17)),
    ("F3", "woman", 3, 520, 1018, 0.66, 1, "stand", "happy", "sit", ("w1", 253, 0.27)),
    ("F4", "child", 3, 640, 1024, 0.66, 1, "stand", "happy", "sit_listen", None),
    ("F5", "child", 2, 760, 1020, 0.66, 1, "stand", "happy", "sit_listen", None),
    ("F6", "child", 5, 880, 1026, 0.66, 1, "stand", "happy", "sit_listen", None),
    ("R1", "woman", 5, 1440, 952, 0.62, -1, "listen", "kind", "sit", None),
    ("R2", "child", 4, 1536, 1012, 0.64, -1, "stand", "happy", "sit_listen", None),
    ("R3", "elder", 3, 1578, 900, 0.6, -1, "listen", "kind", None, None),
    ("R4", "man", 1, 1668, 976, 0.63, -1, "stand", "happy", "sit", None),
    ("R5", "woman", 2, 1780, 918, 0.6, -1, "listen", "kind", None, None),
    ("R6", "child", 1, 1810, 1016, 0.64, -1, "stand", "happy", "sit_listen", None),
]
PRESS = {"B7": 26, "M6": 24, "F6": 20, "M5": 14}        # step closer to Jesus on '人太多了'
KIDS = ("F1", "F2", "F4", "F5", "F6")


def add_crowd(sc, T, times, rng, seated_from=None, extra=None):
    """The beach crowd as Actors. times: dict with w1/w2/w3 (arrival waves), press, sit0/sit1 (the sitting ripple),
    lean, nod (children) - any may be None. seated_from: everybody already seated (s05)."""
    actors = {}
    order = sorted([c for c in CROWD if c[9]], key=lambda c: abs(c[3] - JB[0]))
    sit_t = {}
    if times.get("sit0") is not None:
        for k, c in enumerate(order):
            sit_t[c[0]] = times["sit0"] + (times["sit1"] - times["sit0"]) * k / max(1, len(order) - 1)
    for i, (cid, kind, v, x, y, s, f, pose, expr, spose, arr) in enumerate(CROWD):
        dx_press = PRESS.get(cid, 0) if times.get("press") else 0
        xx = x + dx_press
        d = villager_draw(kind, v, xx, y, s, f, rider=1)
        a = Actor(f"crowd_{cid}", d, (xx, y), s, 20 + y / 100 + i * 0.001, seed=200 + 7 * i)
        st = f"{pose}|{expr}"
        sexpr = "kind" if spose == "sit_listen" else "happy"
        sst = f"{spose}|{sexpr}" if spose else None
        if seated_from is not None:
            a.cut(0, sst or st)
        else:
            a.cut(0, st)
            if arr is not None and arr[0] == "rise":
                tr = times[arr[1]]
                a.mots.append(lambda t, tr=tr, s=s: Tf(
                    dy=60 * s * (1 - M.progress(t, tr, tr + 0.38, "out")) - 14 * s * math.sin(math.pi * min(
                        1.0, max(0.0, (t - tr - 0.25) / 0.3))), alpha=M.progress(t, tr, tr + 0.16, "linear")))
            elif arr is not None:
                key, x0, per = arr
                stride = STRIDE[kind] * s
                n = max(2, round((x - x0) / stride))
                ents, off, t_end = walk_path(times[key] + rng.uniform(0, 0.25), [(stride, 0.0)] * n, per, s)
                ents = [(tk, f"{n_}|happy") for tk, n_ in ents]
                total = n * stride
                a.ents = [(0.0, ents[0][1])] + ents[1:] + [(t_end, st)]
                for _, n_ in ents:
                    a._idx(n_)
                a._idx(st)
                a.dips.append((t_end, 5.0))
                t_in = ents[0][0]

                def walk_m(t, off=off, total=total, t_in=t_in, t_end=t_end):
                    if t < t_in - 0.05:
                        return Tf(dx=-total, alpha=0.0)
                    if t >= t_end + 0.2:
                        return Tf()
                    ox, oy = off(t)
                    return Tf(dx=ox - total, dy=oy)
                a.mots.append(walk_m)
            if dx_press and times.get("press"):
                tp = times["press"] + rng.uniform(0.0, 0.2)
                a.mots.append(lambda t, tp=tp, dxp=dx_press, s=s: Tf(
                    dx=-dxp * (1 - M.progress(t, tp, tp + 0.32, "inout")),
                    dy=-9 * s * math.sin(math.pi * min(1.0, max(0.0, (t - tp) / 0.32)))))
            if cid in sit_t:
                a.cut(sit_t[cid], sst, depth=10.0)
            elif pose == "stand" and times.get("sit0") is not None:
                a.cut(times["sit0"] + 0.5 + rng.uniform(0, 0.6), f"listen|kind")
        if extra:
            extra(cid, a)
        pairs = {}
        for n in list(a.names):
            p_, e_ = n.split("|")
            if not p_.startswith("walk") and e_ in ("happy", "kind", "awed"):
                pairs[n] = f"{p_}|{blink(e_)}"
        a.add_blinks(pairs, T, rng)
        a.mots.append(M.breathe(0.012, 2.6 + 0.37 * (i % 5), pivot=(xx, y), phase=0.17 * i))
        actors[cid] = a
    return actors


def add_shore(sc, T, rng, bm, calm=None):
    """The day shore set (s04 / s05): sky, drifting clouds, the lake with glints and two far boats, the moored boat
    (bm = its motion) with four disciples standing in it, the water band, the beach with the village, the gangplank,
    foreground tufts. Jesus on the stern goes at z=12 (between the disciples and the boat's near side)."""
    calm = calm or (lambda t: 1.0)
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg(), z=1, motion=M.drift(vx=5))
    sc.add("lake", lake_back_svg(), z=3)
    for i, (x, y, k, f, v, vx) in enumerate(((560, 640, 0.13, 1, 1, 5.0), (220, 676, 0.15, -1, 0, -3.0))):
        sc.add(f"farboat{i}", far_boat_svg(x, y, k, f, v), z=3.2, motion=M.combine(
            M.drift(vx=vx), M.bob(1.5, 3.1 + i, 0.2 * i)))
    for i, (vx, per) in enumerate(((7.0, 2.6), (-5.0, 3.3))):
        sc.add(f"glints{i}", glints_svg(11 + i), z=3.5, wc=0, motion=M.combine(
            M.drift(vx=vx), lambda t, per=per, i=i: Tf(alpha=calm(t) * (0.55 + 0.45 * math.sin(2 * math.pi * (
                t / per + 0.5 * i))))))
    flutter = lambda t: float(int(t * 5) % 3)
    sc.add("boat_back", [doc(PR.fishing_boat(BX, BY, BK, 1, part="back", sail="furled", phase=ph))
                         for ph in (0.0, 0.33, 0.66)], z=10, frame_at=flutter, motion=bm, seed=31)
    for j, (i, v, ex) in enumerate(((2, 0, "happy"), (3, 1, "kind"), (4, 2, "happy"), (5, 3, "happy"))):
        px, py = BPTS["far_stand"][i]
        d = (lambda px=px, py=py, v=v: lambda n: C.disciples(px, py, BK, -1, variant=v, pose=n.split("|")[0],
                                                            expr=n.split("|")[1] or None))()
        a = Actor(f"disc{j}", d, (px, py), BK, 11 + 0.01 * j, seed=60 + j, carrier=bm)
        a.cut(0, f"stand|{ex}")
        a.add_blinks({f"stand|{ex}": f"stand|{blink(ex)}"}, T, rng)
        a.mots += [M.breathe(0.01, 2.8 + 0.3 * j, pivot=(px, py), phase=0.2 * j)]
        a.build(sc)
    sc.add("boat_front", doc(PR.fishing_boat(BX, BY, BK, 1, part="front", sail="furled")), z=13, motion=bm, seed=33)
    sc.add("band", band_svg(), z=14)
    sc.add("shore", shore_svg(), z=15)
    sc.add("plank", plank_svg(), z=16)


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    at = timer(ctx)
    rng = random.Random(4)
    t_jesus = at(0, "耶稣")
    t_teach = at(0, "教导")
    t_many1 = at(0, "很多")
    t_many2 = at(0, "很多很多", 2)
    t_too = at(0, "人太多了")
    t_sit = snap(at(0, "坐"))
    t_tell = at(0, "讲故事")
    t_all = at(1, "大家")
    t_quiet = at(1, "安安静静")
    t_kids = at(1, "小孩子")
    t_hear = at(1, "听得")
    t_serious = at(1, "认真")

    # ------------------------------------------------------------ backdrop, the boat and the disciples in it
    bm = boat_motion((t_sit,), g0=0.0)
    calm = lambda t: 1 - 0.45 * M.progress(t, t_quiet - 0.3, t_quiet + 1.6, "sine")
    add_shore(sc, T, rng, bm, calm)
    # Jesus on the stern (from '坐')
    jbd = lambda n: C.jesus(SEAT[0], SEAT[1], BK, -1, pose=n.split("|")[0], expr=n.split("|")[1])
    jb = Actor("jesus_boat", jbd, SEAT, BK, 12, seed=71, carrier=bm)
    jb.cut(0, "sit|warm", dip_=False)
    jb.cut(t_sit, "sit|warm", depth=10)
    jb.cut(t_tell - 0.05, "teach|smile")
    jb.cut(t_all + 0.6, "sit|warm")
    jb.cut(t_kids - 0.25, "teach|smile")
    jb.add_blinks({"sit|warm": f"sit|{blink('warm')}"}, T, rng, t_from=t_sit + 0.4)
    jb.mots += [lambda t: Tf(alpha=1.0 if t >= t_sit else 0.0), M.breathe(0.01, 3.0, pivot=SEAT)]
    jb.build(sc)

    # ------------------------------------------------------------ Jesus on the beach, then up the plank
    jx, jy = JB
    jd = lambda n: (C.ground_shadow(jx, jy, BK, 120, 0.16) * (n.split("|")[0] != "walk_a" and n.split("|")[0] != "walk_b")
                    + C.jesus(jx, jy, BK, int(n.split("|")[2]), pose=n.split("|")[0], expr=n.split("|")[1]))
    ja = Actor("jesus_beach", jd, JB, BK, 20 + jy / 100 + 0.005, seed=73)
    ja.cut(0, "teach_stand|smile|-1")
    ja.cut(t_jesus - 0.05, "stand|warm|-1")
    ja.cut(t_teach - 0.05, "teach_stand|smile|-1")
    ja.cut(t_too - 0.3, "stand|warm|-1")
    t_turn = snap(t_too + 0.12)
    ja.cut(t_turn, "stand|warm|1")
    # up the plank from its foot to its top
    (px0, py0), (px1, py1) = PLANK0, PLANK1
    n_up = 6
    steps = [((px1 - 12 - jx) / n_up, (py1 + 4 - jy) / n_up)] * n_up
    t_w0 = snap(t_turn + 0.16)
    period = max(0.16, min(0.27, (t_sit - 0.1 - t_w0) / len(steps)))
    wents, woff, t_w1 = walk_path(t_w0, steps, period, BK, lift=5)
    for tk, n_ in wents:
        ja.cut(tk, f"{n_}|warm|1", dip_=False)
    if t_sit - t_w1 > 0.1:
        ja.cut(t_w1, "stand|warm|1", depth=4)
    ja.add_blinks({"stand|warm|-1": f"stand|{blink('warm')}|-1"}, T, rng, t_from=0.3)
    lean = lambda t: -5.0 * M.progress(t, t_w0 - 0.05, t_w0 + period * 0.8, "sine") * \
        (1 - M.progress(t, t_w1 - 0.1, t_w1 + 0.1, "sine"))

    def jwalk(t):
        if t >= t_sit:
            return Tf(alpha=0.0)
        ox, oy = woff(t)
        return Tf(dx=ox, dy=oy, rot=lean(t), px=jx, py=jy)
    ja.mots += [jwalk, lambda t: Tf(sx=1 + 0.01 * math.sin(2 * math.pi * t / 3.0), sy=1 + 0.01 * math.sin(
        2 * math.pi * t / 3.0), px=jx, py=jy) if t < t_w0 else Tf()]
    ja.build(sc)

    # ------------------------------------------------------------ the crowd
    times = dict(w1=t_jesus + 0.05, w2=t_many1 - 0.05, w3=t_many2 - 0.05, press=t_too - 0.12, sit0=t_all - 0.05,
                 sit1=t_quiet + 0.75, m1=at(0, "很多", 1) - 0.04, m2=at(0, "很多很多", 3) - 0.04,
                 m3=at(0, "很多很多人", 4) - 0.04)
    lean0, lean1 = t_hear - 0.2, t_hear + 0.35

    def kid_extra(cid, a):
        if cid in KIDS:
            x, y = a.piv
            ph = rng.uniform(0, 0.12)
            a.mots.append(lambda t, x=x, y=y, ph=ph: Tf(
                rot=6.5 * M.progress(t, lean0 + ph, lean1 + ph, "sine") + 5.0 * math.sin(math.pi * min(1.0, max(
                    0.0, (t - t_serious - ph) / 0.4))), px=x, py=y))
            if cid in ("F2", "F4", "F6"):
                a.cut(lean0 + ph, "sit_listen|awed", depth=3)
    actors = add_crowd(sc, T, times, rng, extra=kid_extra)
    for a in actors.values():
        a.build(sc)

    # ------------------------------------------------------------ birds: two cross the sky early, two settle on the yard
    for i, (col, y0, vx, t0, f) in enumerate((("yellow", 330, 95, 0.4, 1), ("blue", 270, -80, 3.2, -1))):
        fr = bird_frames(col, f, 0.3)
        x_start = -150 if vx > 0 else W + 150

        def fly(t, y0=y0, vx=vx, t0=t0, xs=x_start, i=i):
            return Tf(dx=xs + vx * (t - t0) - 200, dy=y0 - 200 + 20 * math.sin(2 * math.pi * (t / 1.9 + 0.3 * i)),
                      alpha=1.0 if t >= t0 else 0.0)
        sc.add(f"sky_bird{i}", fr[:8], z=2, motion=fly, wc=0.3,
               frame_at=lambda t, i=i: float(int(t / 0.07 + 3 * i) % 8))
    yard0, yard1 = BPTS["yard"]
    for i, (col, lx, t0) in enumerate((("red", 0.3, t_all + 0.3), ("yellow", 0.72, t_all + 0.75))):
        fr = bird_frames(col, -1, 0.36)
        tx = yard0[0] + (yard1[0] - yard0[0]) * lx
        ty = YARD_Y - 30 * 0.36 - 9
        sx0, sy0 = W + 160, ty - 240
        t_land = snap(t0 + 1.25)

        def bird_m(t, tx=tx, ty=ty, sx0=sx0, sy0=sy0, t0=t0, t_land=t_land):
            if t < t0:
                return Tf(alpha=0.0)
            if t < t_land:
                u = (t - t0) / (t_land - t0)
                e = 1 - (1 - u) ** 2
                x = sx0 + (tx - sx0) * e
                y = sy0 + (ty - sy0) * e - 70 * math.sin(math.pi * e)
                return Tf(dx=x - 200, dy=y - 200)
            hop = 0.0
            for th in (t_land + 1.6, t_land + 3.1):
                if th <= t < th + 0.22:
                    hop = -8 * math.sin(math.pi * (t - th) / 0.22)
            return Tf(dx=tx - 200, dy=ty - 200 + hop)
        sc.add(f"yard_bird{i}", fr, z=10.5, wc=0.3, motion=M.combine(bird_m, bm),
               frame_at=lambda t, t_land=t_land, i=i: 8.0 if t >= t_land else float(int(t / 0.06 + 2 * i) % 8))

    sc.add("tufts", [tufts_svg(k) for k in range(3)], z=40,
           frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.55) % 4]) if t < t_quiet + 0.5 else 1.0)

    # ------------------------------------------------------------ camera
    sc.camera = M.cam_keys([
        (0.0, Cam(1220, 606, 1500)), (t_teach - 0.1, Cam(1190, 615, 1560)),
        (t_many2 + 0.9, Cam(1056, 600, 2060)), (t_too + 0.1, Cam(1056, 600, 2060)),
        (t_sit + 0.4, Cam(1150, 630, 1760)), (t_all - 0.2, Cam(1130, 630, 1800)),
        (t_quiet + 1.0, Cam(1010, 630, 1960)), (t_kids - 0.1, Cam(1000, 640, 1940)),
        (t_hear + 0.6, Cam(880, 795, 1320)), (T, Cam(872, 798, 1300))],
        ["sine", "inout", "sine", "inout", "sine", "inout", "sine", "inout", "sine"])

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-15, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=t_quiet + 1.5, gain_db=-24, fade_in=0.8, fade_out=1.4)
    sc.sfx("crowd", t_jesus, dur=t_quiet + 1.0 - t_jesus, gain_db=-21, fade_in=2.5, fade_out=1.3)
    sc.sfx("footsteps", t_jesus, dur=t_many2 + 2.0 - t_jesus, gain_db=-22, fade_in=0.6, fade_out=0.8, pan=-0.5)
    sc.sfx("footsteps", t_w0, dur=t_w1 - t_w0 + 0.1, gain_db=-17, pan=0.1)
    sc.sfx("splash_small", t_sit + 0.05, gain_db=-20, pan=0.2)
    sc.sfx("ship_creak", t_sit, dur=1.6, gain_db=-22, fade_in=0.1, fade_out=0.8, pan=0.2)
    sc.sfx("cloth", t_all, gain_db=-17, pan=-0.2)
    sc.sfx("cloth", t_quiet + 0.4, gain_db=-19, pan=-0.5)
    return sc
