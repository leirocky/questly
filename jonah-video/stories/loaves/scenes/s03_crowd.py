"""Scene 3 - Mark 6:30-34 (Luke 9:11). Jesus and the twelve are so busy they cannot even eat; they sail off for a quiet
place across the lake; the people see them, run along the shore and get there first; Jesus steps out of the boat, looks
at the crowd with love (like sheep without a shepherd), teaches them on the hillside and heals the sick.

One 2600 x 1462 stage, two worlds (hard cuts on phrase boundaries; a page dip from s02 at the start; a plain 1 s
cross-dissolve into s04, which opens on exactly this scene's last frame - the hillside world below is shared with it):
  S  the lakeshore path by a fishing village (props.lakeshore_path, warm afternoon): the busy day, the boat pushing off,
     the people pointing, the crowd running along the shore while the far boat glides;
  E  the emerald hillside above the lake (props.galilee_sky + lake_hillside, golden-ish light .4): the crowd arrives
     before the boat, Jesus steps ashore, walks up to them and looks at them with love; a thought bubble of sheep
     without a shepherd;
  F  the same hillside wide: Jesus teaches on the teaching rock, the crowd sits in colourful groups; then closer: he
     heals the man with the crutch and the feverish child.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's Tm;
nothing is hard-coded to the take):
  0 .. 1.0     calm: Jesus and the twelve on the path by the village, villagers about, the moored boat
  '耶稣有十二个' numbers 1..12 pop over the disciples' heads one by one (each gives a tiny bob)
  '叫做门徒'     the numbers fade; two disciples wave, the others smile
  '好忙好忙'     people come and go: walkers cross, a mother brings her little girl to Jesus (he blesses her),
               an old man asks John the way (John points), a man calls to Andrew
  '连吃饭'       Peter lifts a barley loaf to his mouth ...; '时间' a boy runs up and tugs at him - he turns, the loaf
               comes down; '都没有' a little sigh (sweat drop)
  '耶稣说'       Jesus turns to his friends; '安静的地方' he points to the boat; '休息' - Peter finally takes his bite
  line 3       cut: the boat (far_boat) pushes off, the sail opens on '坐船', it glides away on '那一边'; the villagers
               wave; '可是' they turn, '看见了' they point (! marks)
  '大家沿着湖边' they run along the shore path, the crowd streams in from the village; a stride accent and dust on
               every '跑'; the boat glides slowly behind them
  '比船还先到了' cut to the hillside: the runners pour in and stop, panting and pointing at the boat still out on the
               lake (comic beat)
  '耶稣下了船'   cut closer: the boat at the shore; on '下' Jesus steps off the bow and walks down the path to the
               people, who turn to him
  '疼爱他们'     he stops and looks at them with love (a soft warm glow on his face, chime)
  '没有牧羊人的羊' a thought bubble: a few sheep wander on a little hill, no shepherd; '不知道该往哪里去' they stop and
               look this way and that ('?' marks, a bleat)
  line 5       cut wide: Jesus teaching on the rock, the crowd sitting in groups; '讲' his gesture changes
  '还把生病的人' cut closer: Jesus has risen, his palm resting on the head of the man with the crutch; the mother
               with her feverish child beside him
  '治好了'       soft glow, sparkles: the man jumps up, crutch high; the child sits up laughing; Jesus smiles at them;
               calm end (the plain dissolve into s04 starts on this frame)
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
from stories.zacchaeus.scenes.s03_jericho import Actor as _ZActor
from stories.zacchaeus.scenes.s03_jericho import Loop, breathm, dipm, hopm, popm

INK = P["ink"]
CREAM = "#fff6e3"
W, H = 2600, 1462

for _e in ("warm", "kind", "smile", "happy", "awed", "worried", "concerned", "tired", "teach", "neutral", "joyful", "eager",
           "delighted", "surprised", "amazed", "ponder", "doubtful", "count", "sad"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"lf3_b_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(e):
    return f"lf3_b_{e}"


# ================================================================== small helpers (shared with s04_evening)
def doc(body, defs=""):
    return S.svg_doc(body, defs, W, H)


def f1(v):
    return f"{v:.1f}"


def gate(t0, t1=1e9):
    return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)


def clamp_cam(c):
    cw = min(c.w, W, H * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), W - cw / 2 - 1), min(max(c.y, ch / 2 + 1), H - ch / 2 - 1), cw, c.rot)


def cam_inside(c):
    return c.w <= W and c.x - c.w / 2 >= 0 and c.x + c.w / 2 <= W and c.y - c.w * 9 / 32 >= 0 and c.y + c.w * 9 / 32 <= H


def cam_keys(keys, curves="sine"):
    for tk, c in keys:
        assert cam_inside(c), f"camera key at {tk:.2f}s leaves the {W}x{H} stage: {c}"
    f = M.cam_keys(keys, curves)
    return lambda t: clamp_cam(f(t))


def shadow(x, y, s, w=110, o=0.18):
    return C.ground_shadow(x, y, s, w, o)


class Actor(_ZActor):
    """The Zacchaeus film's Actor (flipbook of keyed drawings at a home anchor, planted moves, dips, global-clock loops)
    on this scene's stage."""

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


def swallow(x, y, k, flap, col="#4e5a66"):
    d = 10 * k if flap else -4 * k
    return (f'<path d="M{f1(x - 22 * k)},{f1(y + d)} Q{f1(x - 10 * k)},{f1(y - 10 * k)} {f1(x)},{f1(y)} '
            f'Q{f1(x + 10 * k)},{f1(y - 10 * k)} {f1(x + 22 * k)},{f1(y + d)}" fill="none" stroke="{col}" '
            f'stroke-width="{f1(3.2 * k)}" stroke-linecap="round" stroke-linejoin="round"/>')


def add_birds(sc, name, z, pts, k, g0, gatef, period=9.0, span=1100.0, seed=3, flap=0.14, col="#4e5a66"):
    """A few swallows gliding across on the film's global clock (fading in and out at the ends of their glide)."""
    rng = random.Random(seed)
    for i, (x, y) in enumerate(pts):
        fr = [doc(swallow(x, y, k * rng.uniform(0.85, 1.15), f, col)) for f in (0, 1)]
        ph = rng.uniform(0, 1)
        per = period * rng.uniform(0.85, 1.2)

        def mot(t, ph=ph, per=per, i=i):
            u = ((t + g0) / per + ph) % 1.0
            a = math.sin(math.pi * u)
            return Tf(dx=span * (u - 0.5), dy=24 * math.sin(2 * math.pi * (t + g0) / 2.6 + i),
                      alpha=min(1.0, a * 3) * gatef(t).alpha)
        sc.add(f"{name}{i}", fr, z=z + 0.001 * i, wc=0.3, seed=seed * 10 + i,
               frame_at=lambda t, i=i: float(int((t + g0) / flap + i) % 2), motion=mot)


def add_clouds(sc, name, z, items, time, g0, gatef, seed, vx=4.0):
    """Soft lit cumulus banks (props._lf_cloud) on their own layers drifting slowly on the global clock."""
    pal = PR._lf_pal(time)
    for i, (cx, cy, cw, sd) in enumerate(items):
        svg = doc(PR._lf_cloud(cx, cy, cw, cw * 0.3, pal, sd, rim_k=0.4 + 0.6 * time))
        v = vx * (0.8 + 0.25 * (i % 3))

        def m(t, v=v):
            return Tf(dx=v * (t + g0) - 250.0)
        sc.add(f"{name}{i}", svg, z=z + 0.001 * i, seed=seed + i, wc=0.7, motion=M.combine(m, gatef))


def glint_svg(x0, x1, y0, y1, k, time, seed, n=46, size=1.0):
    """Sun glints on the lake: short soft light dashes (variant k of 3)."""
    pal = PR._lf_pal(time)
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        x = rng.uniform(x0, x1)
        y = y0 + (y1 - y0) * rng.random() ** 0.8
        w = rng.uniform(14, 34) * size * (0.5 + 0.5 * (y - y0) / max(1, y1 - y0))
        on = (i + k) % 3 != 0
        if not on:
            continue
        a = rng.uniform(0.45, 0.9)
        out += (f'<path d="M{f1(x - w / 2)},{f1(y)} Q{f1(x)},{f1(y - 3 * size)} {f1(x + w / 2)},{f1(y)}" fill="none" '
                f'stroke="{pal["glit"]}" stroke-width="{f1(3.0 * size)}" stroke-linecap="round" opacity="{a:.2f}"/>')
    return doc(out)


def add_glints(sc, name, z, rect, time, g0, gatef, seed, n=46, size=1.0):
    frames = [glint_svg(*rect, k, time, seed, n, size) for k in range(3)] + [glint_svg(*rect, 0, time, seed, n, size)]

    def fa(t):
        u = ((t + g0) / 2.4) % 1.0 * 3
        i = math.floor(u)
        fr = u - i
        return i + (0.0 if fr < 0.55 else (fr - 0.55) / 0.45)
    sc.add(name, frames, z=z, wc=0.0, seed=seed, frame_at=fa, motion=gatef)


def sway_corner(sc, name, svg_body, clip_rect, pivot, z, seed, g0, gatef, deg=0.5, period=3.8, phase=0.0):
    """One bottom corner of a 'front' layer (clipped) rocking gently in the breeze about its foot."""
    x, y, w, h = clip_rect
    cid = f"lf3clip{name}"
    svg = doc(f'<clipPath id="{cid}"><rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}"/></clipPath>'
              f'<g clip-path="url(#{cid})">{svg_body}</g>')

    def m(t):
        u = (t + g0) / period + phase
        return Tf(rot=deg * (math.sin(2 * math.pi * u) + 0.35 * math.sin(2 * math.pi * (1.7 * u + 0.3))), px=pivot[0],
                  py=pivot[1])
    sc.add(name, svg, z=z, seed=seed, motion=M.combine(m, gatef))


def warm_glow_svg(cx, cy, rx, ry, col="#fff0b8", a=0.85, key="g"):
    gid = f"lf3glow{key}{int(cx)}{int(cy)}"
    return doc(f'<defs>{S.rad_grad(gid, [(0, col, a), (0.45, col, a * 0.45), (1, col, 0)])}</defs>'
               f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>')


def env(t, t0, t1, fin=0.5, fout=0.5):
    if t < t0 or t > t1:
        return 0.0
    return min(1.0, M.progress(t, t0, t0 + fin, "sine"), 1 - M.progress(t, t1 - fout, t1, "sine"))


def badge_svg(x, y, n, r=34, col="#c8643c"):
    b = PR._circ(x, y, r, CREAM, 4.0)
    b = S.g(b, filter="wobble-fine")
    b += (f'<text x="{f1(x)}" y="{f1(y + r * 0.42)}" font-family="LXGW WenKai" font-weight="bold" font-size="{f1(r * 1.25)}" '
          f'fill="{col}" text-anchor="middle">{n}</text>')
    return doc(b)


def mark_svg(x, y, text="!", size=78, col="#c8643c"):
    return doc(f'<text x="{f1(x)}" y="{f1(y)}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" '
               f'fill="{col}" stroke="{INK}" stroke-width="4" paint-order="stroke" text-anchor="middle">{text}</text>')


def sweat_svg(x, y, k=1.0):
    d = (f"M{f1(x)},{f1(y - 16 * k)} Q{f1(x + 10 * k)},{f1(y - 2 * k)} {f1(x + 8 * k)},{f1(y + 6 * k)} "
         f"Q{f1(x)},{f1(y + 14 * k)} {f1(x - 8 * k)},{f1(y + 6 * k)} Q{f1(x - 10 * k)},{f1(y - 2 * k)} {f1(x)},{f1(y - 16 * k)} Z")
    return doc(S.g(f'<path d="{d}" fill="#bfe4f0" stroke="{INK}" stroke-width="{f1(3 * k)}"/>', filter="wobble-fine"))


def puff_svg(x, y, r, n=3, dirx=1):
    """Little panting / dust puffs (soft cream circles)."""
    b = ""
    for j, (dx, dy, rr) in enumerate(((0, 0, 1.0), (r * 0.9, -r * 0.5, 0.75), (r * 1.6, -r * 1.1, 0.5))[:n]):
        b += PR._circ(x + dirx * dx, y + dy, r * rr, "#fffaf0", 2.6, extra='opacity="0.92"')
    return doc(S.g(b, filter="wobble-fine"))


def dust_svg(x, y, r, col="#e8d2a6"):
    b = ""
    for dx, dy, rr in ((0, 0, 1.0), (-r * 1.1, -r * 0.3, 0.7), (r * 0.9, -r * 0.2, 0.6)):
        b += PR._circ(x + dx, y + dy, r * rr, col, 0, extra='opacity="0.75"')
    return doc(b)


def puffm(t0, piv, dur=0.7, dx=30.0, dy=-24.0):
    """A puff that appears at t0, drifts and fades."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf(alpha=0.0)
        k = u / dur
        return Tf(dx=dx * k, dy=dy * k, sx=0.6 + 0.6 * k, sy=0.6 + 0.6 * k, alpha=min(1.0, u / 0.08) * (1 - k ** 1.5),
                  px=piv[0], py=piv[1])
    return m


# ---- figures
def jes(x, y, s, f, pose="stand", expr=None, glow=0.0, item=None):
    if pose in C.JESUS_LOAVES_POSES:
        return C.jesus(x, y, s, f, pose=pose, expr=expr, glow=glow, item=item)
    return C.jesus(x, y, s, f, pose=pose, expr=expr, glow=glow)


def disc(x, y, s, f, v, pose="stand", expr=None, phase=0.0, marks=True):
    return C.disciples(x, y, s, f, variant=v, pose=pose, expr=expr, phase=phase, marks=marks)


def disc_bread(x, y, s, f, v, hand, expr="happy", rot=0.0, state="whole", look=None, h=0.0):
    """A disciple standing with a barley loaf in his near hand at ``hand`` (body coords at scale 1): near the mouth =
    about to eat, at the hip = holding it."""
    vi = C._disciple_index(v)
    D, m = C._disciple_design(vi, 0.0, False)
    ps, _ = C._disciple_pose("stand", 0.0)
    ps = dict(ps)
    ps["arms"] = (ps["arms"][0], ("ik", "abs", hand[0], hand[1], 1))
    ps["hands"] = (ps["hands"][0], "fist")
    ps["h"] = ps.get("h", 0) + h
    if look is not None:
        ps["look"] = look
    skin = D["skin"]

    def front(st):
        W1, hr = st["arms"][1][2], st["m"]["hr"]
        loaf = PR._barley_loaf(state, 0.25)
        return C._lf_held(st, loaf, (W1[0] + 6, W1[1] - 14), rot, 1.05) + C._fist(W1, hr, skin)
    D["front"] = C._hooks(D.get("front"), front)
    inner, _ = C._figure(D, m, ps, expr, C._fsign(f), True)
    return C._wrap_out(inner, x, y, s, f, f"lf3bread{vi}-{hand[0]}-{hand[1]}-{expr}-{h}")


def folk(x, y, s, f, kind="man", v=0, pose="stand", expr=None, phase=0.0, marks=True, food=None):
    return C.galilee_folk(x, y, s, f, kind=kind, variant=v, pose=pose, expr=expr, phase=phase, marks=marks, food=food)


# ================================================================== SET S: the lakeshore path by the village
S_TIME = 0.25
SS, YS = 1.15, 1160                    # lakeshore_path scale and the middle of the path
S_SHORE = YS - 120 * SS
S_FAR = S_SHORE - 260 * SS
KA = 0.9                               # people on the path
LANE_F, LANE_B = YS + 62, YS - 14      # the near lane (walkers in front of the group) and the group's own line
SEED_S = 3310
BOAT_MOOR = (2060, S_SHORE - 26)
S_SUN = (2160, 445)


def house(x, base, k, v, time):
    """A Galilean village house (pale limestone, flat roof with a parapet and beam ends, a wooden door, a small window;
    variants add an outside stair, a striped awning or clay jars)."""
    pal = PR._lf_pal(time)
    wall = (pal["town"], S.mix(pal["town"], pal["town_dk"], 0.32), S.mix(pal["town"], "#f2d4a8", 0.35),
            S.mix(pal["town"], pal["town_dk"], 0.16))[v % 4]
    dk = S.shade(wall, -0.2)
    wood = PR._lft("#8a5a36", time, 0.5)
    w = (250, 200, 290, 220)[v % 4] * k
    h = (180, 215, 160, 200)[v % 4] * k
    sw = 3.4 * k
    x0, y0 = x - w / 2, base - h
    rng = random.Random(90 + v)
    out = PR._p(f"M{f1(x0)},{f1(base)} L{f1(x0 + 3 * k)},{f1(y0)} L{f1(x0 + w - 2 * k)},{f1(y0 + 2 * k)} L{f1(x0 + w)},{f1(base)} Z",
                wall, sw)
    for i in range(7):
        sx_, sy_ = x0 + rng.uniform(0.08, 0.85) * w, y0 + rng.uniform(0.15, 0.85) * h
        out += PR._p(f"M{f1(sx_)},{f1(sy_)} h{f1(rng.uniform(18, 34) * k)} v{f1(12 * k)} h{f1(-rng.uniform(18, 34) * k)} Z",
                     dk, 0, extra='opacity="0.22"')
    out += PR._p(f"M{f1(x0 - 8 * k)},{f1(y0 - 16 * k)} L{f1(x0 + w + 8 * k)},{f1(y0 - 14 * k)} L{f1(x0 + w + 8 * k)},{f1(y0 + 2 * k)} "
                 f"L{f1(x0 - 8 * k)},{f1(y0 + 2 * k)} Z", S.shade(wall, -0.08), sw)
    for j in range(int(w / (40 * k))):
        out += PR._circ(x0 + 22 * k + j * 40 * k, y0 + 12 * k, 5.5 * k, wood, 2.0 * k)
    dx_ = x0 + w * (0.30 if v % 2 else 0.64)
    dw, dh = 50 * k, 92 * k
    out += PR._p(f"M{f1(dx_ - dw / 2)},{f1(base)} L{f1(dx_ - dw / 2)},{f1(base - dh + dw / 2)} Q{f1(dx_)},{f1(base - dh - 8 * k)} "
                 f"{f1(dx_ + dw / 2)},{f1(base - dh + dw / 2)} L{f1(dx_ + dw / 2)},{f1(base)} Z", PR._lft("#6a4630", time, 0.5), sw)
    out += PR._p(f"M{f1(dx_)},{f1(base - dh + 6 * k)} L{f1(dx_)},{f1(base)}", sw=2.2 * k, stroke=S.shade(wood, -0.3))
    wx = x0 + w * (0.72 if v % 2 else 0.24)
    out += PR._p(f"M{f1(wx - 16 * k)},{f1(y0 + 46 * k)} h{f1(32 * k)} v{f1(30 * k)} h{f1(-32 * k)} Z", PR._lft("#5a4232", time, 0.5), sw * 0.8)
    out += PR._p(f"M{f1(wx - 22 * k)},{f1(y0 + 78 * k)} h{f1(44 * k)}", sw=5 * k, stroke=wood)
    if v % 4 == 0:      # outside stair to the roof
        for j in range(6):
            sy2 = base - (j + 1) * h / 7
            sx2 = x0 + w + 4 * k + (5 - j) * 9 * k
            out += PR._p(f"M{f1(x0 + w)},{f1(sy2)} L{f1(sx2 + 26 * k)},{f1(sy2)} L{f1(sx2 + 26 * k)},{f1(sy2 + h / 7)} L{f1(x0 + w)},{f1(sy2 + h / 7)} Z",
                         S.mix(wall, dk, 0.4), 2.4 * k)
    if v % 4 == 1:      # a striped awning over the door
        ax0, ax1 = dx_ - 70 * k, dx_ + 80 * k
        ay = base - dh - 22 * k
        stripes = ""
        for j in range(6):
            c = PR._lft("#c9714a" if j % 2 else "#f2e2c0", time, 0.5)
            u0, u1 = j / 6, (j + 1) / 6
            stripes += PR._p(f"M{f1(ax0 + (ax1 - ax0) * u0)},{f1(ay)} L{f1(ax0 + (ax1 - ax0) * u1)},{f1(ay)} "
                             f"L{f1(ax0 + (ax1 - ax0) * u1 + 6 * k)},{f1(ay + 40 * k)} L{f1(ax0 + (ax1 - ax0) * u0 + 6 * k)},{f1(ay + 40 * k)} Z", c, 0)
        out += stripes + PR._p(f"M{f1(ax0)},{f1(ay)} L{f1(ax1)},{f1(ay)} L{f1(ax1 + 6 * k)},{f1(ay + 40 * k)} L{f1(ax0 + 6 * k)},{f1(ay + 40 * k)} Z",
                               sw=2.6 * k)
        for px_ in (ax0 + 6 * k, ax1 + 6 * k):
            out += PR._p(f"M{f1(px_)},{f1(ay + 40 * k)} L{f1(px_ + 4 * k)},{f1(base)}", sw=4 * k, stroke=wood)
    if v % 4 in (2, 3):  # clay jars by the door
        for j, jx in enumerate((dx_ + dw / 2 + 26 * k, dx_ + dw / 2 + 58 * k)):
            jh = (46, 36)[j] * k
            out += PR._p(f"M{f1(jx - 12 * k)},{f1(base)} Q{f1(jx - 22 * k)},{f1(base - jh * 0.6)} {f1(jx - 8 * k)},{f1(base - jh)} "
                         f"L{f1(jx + 8 * k)},{f1(base - jh)} Q{f1(jx + 22 * k)},{f1(base - jh * 0.6)} {f1(jx + 12 * k)},{f1(base)} Z",
                         PR._lft("#c9805a", time, 0.5), 2.6 * k)
    return S.g(out, filter="wobble")


def net_rack(x, base, k, time):
    """Two poles with a fishing net hung to dry (cork floats along the top)."""
    wood = PR._lft("#8a5a36", time, 0.5)
    net = PR._lft("#b89a6a", time, 0.5)
    out = ""
    for px_ in (x - 110 * k, x + 110 * k):
        out += PR._p(f"M{f1(px_)},{f1(base)} L{f1(px_ + 3 * k)},{f1(base - 190 * k)}", sw=8 * k, stroke=wood)
    top = base - 178 * k
    out += PR._p(f"M{f1(x - 112 * k)},{f1(top)} Q{f1(x)},{f1(top + 26 * k)} {f1(x + 112 * k)},{f1(top)}", sw=4 * k, stroke=wood)
    for i in range(11):
        u = i / 10
        xx = x - 104 * k + 208 * k * u
        yy = top + 26 * k * 4 * u * (1 - u)
        out += PR._p(f"M{f1(xx)},{f1(yy)} Q{f1(xx + 6 * k)},{f1(yy + 60 * k)} {f1(xx - 2 * k)},{f1(base - 50 * k + 8 * math.sin(i) * k)}",
                     sw=1.8 * k, stroke=net)
        if i % 2 == 0:
            out += PR._circ(xx, yy + 4 * k, 6 * k, PR._lft("#d9a24e", time, 0.5), 1.8 * k)
    for j in range(4):
        yy = top + 34 * k + j * 26 * k
        out += PR._p(f"M{f1(x - 100 * k)},{f1(yy)} Q{f1(x)},{f1(yy + 18 * k)} {f1(x + 100 * k)},{f1(yy)}", sw=1.6 * k, stroke=net)
    return S.g(out, filter="wobble-fine")


def s_sky_svg():
    return doc(PR.galilee_sky(-10, -10, W + 10, S_FAR + 80, time=S_TIME, sun=S_SUN, clouds=0, birds=0, seed=SEED_S, scale=1.1))


def s_back_svg():
    return doc(PR.lakeshore_path(-40, W + 40, YS, SS, time=S_TIME, part="back", seed=4, bottom=H + 40, towns=True))


def s_path_svg():
    b = PR.lakeshore_path(-40, W + 40, YS, SS, time=S_TIME, part="path", seed=4, bottom=H + 40, towns=False)
    base = S_SHORE + 62
    b += PR._lf_tree(980, base - 6, 1.05, S_TIME, 3, "olive")
    b += net_rack(1240, base - 2, 0.95, S_TIME)
    for (hx, v, k) in ((120, 0, 1.45), (430, 1, 1.4), (700, 2, 1.35)):
        b += house(hx, base + (v % 2) * 4, k, v, S_TIME)
    b += PR._lf_tree(2590, base - 2, 0.95, S_TIME, 7, "olive")
    return doc(b)


def s_front_body():
    return PR.lakeshore_path(-40, W + 40, YS, SS, time=S_TIME, part="front", seed=4, bottom=H + 40)


def far_boat_svg(x, y, k, sail, crew=True, time=S_TIME):
    return doc(PR.far_boat(x, y, k, 1, sail=sail, crew=crew, time=time))


# the group in shot A: (name, variant (None = Jesus), x, y, scale, facing)
A_GROUP = [
    ("d5", 5, 905, LANE_B - 40, KA * 0.95, 1), ("d9", 9, 1045, LANE_B - 44, KA * 0.95, 1), ("d8", 8, 1185, LANE_B - 42, KA * 0.95, 1),
    ("d10", 10, 1455, LANE_B - 42, KA * 0.95, -1), ("d11", 11, 1595, LANE_B - 44, KA * 0.95, -1), ("d4", 4, 1735, LANE_B - 40, KA * 0.95, -1),
    ("d6", 6, 835, LANE_B, KA, 1), ("d7", 7, 975, LANE_B + 2, KA, 1), ("d1", 1, 1120, LANE_B, KA, 1),
    ("jesus", None, 1320, LANE_B + 6, KA, 1),
    ("d0", 0, 1520, LANE_B, KA, -1), ("d2", 2, 1665, LANE_B + 2, KA, -1), ("d3", 3, 1805, LANE_B, KA, -1),
]
# counting order (left to right, back and front rows interleaved)
COUNT_ORDER = ["d6", "d5", "d7", "d9", "d1", "d8", "d10", "d0", "d11", "d2", "d4", "d3"]


# ================================================================== the HILLSIDE world (E, F and all of s04)
HS, HY = 1.25, 1338
HX0, HX1 = -40, W + 40
H_TIME = 0.4
RX = 1000                               # the teaching rock (facing -1: Jesus faces left, the hump behind him on the right)
HP = PR.lake_hillside_points(HX0, HX1, HY, HS, rock_x=RX)
LY, FY = HP["lake_y"], HP["far_y"]
RY = HP["rock"][1]
JK = HS * HP["rock"][2]                 # Jesus / the rock scale on the rock's line
SUN0 = (2150, 330)
SEED_H = 3400
Z_H = 30.0


def hk(y):
    """Person scale on the hillside at ground line y."""
    d = max(0.0, (HY - y) / (HY - LY)) ** (1 / 0.85)
    return HS * (1 - 0.62 * min(1.0, d))


def hy_d(d, x=None):
    """Ground y (with the shoulder's rise at x) and scale for a depth fraction d (0 front .. 1 shore)."""
    y, k = HP["depth"](d)
    if x is not None:
        y -= HP["shoulder"]((x - HX0) / (HX1 - HX0)) * d ** 1.4
    return y, HS * k


def sun_svg(time, x, y):
    pal = PR._lf_pal(time)
    r = (58 + 22 * time) * HS
    out = PR._ls_glow(x, y, r * 6.5, r * 5.0, 0.8, "lfsun", pal["sun"], pal["sun_halo"])
    out += PR._circ(x, y, r, pal["sun"], 0)
    out += PR._circ(x, y, r, "none", 2.6 * HS, stroke=S.mix(pal["sun"], "#e89a4a", 0.5), extra='opacity="0.55"')
    return doc(out)


def h_sky_svg(time):
    return doc(PR.galilee_sky(-10, -10, W + 10, FY + 60, time=time, sun=None, clouds=0, birds=0, seed=SEED_H, scale=HS))


def h_part_svg(time, part):
    return doc(PR.lake_hillside(HX0, HX1, HY, HS, time=time, part=part, seed=0, bottom=H + 40, rock_x=RX, rock=False))


def h_rock_svg(time):
    return doc(PR.teaching_rock(RX, RY, JK, -1, time=time, seed=2))


H_CLOUDS = [(260, 200, 470, 11), (900, 150, 540, 13), (1540, 230, 440, 17), (2140, 170, 500, 19), (2580, 260, 360, 23)]
H_BIRDS = [(600, 200), (1250, 140), (1800, 250)]


def add_hill(sc, gatef, g0, times=(H_TIME,), u=None):
    """The hillside backdrop (sky, sun, clouds, far hills and lake, slope, teaching rock, front corners) on layers with
    explicit seeds so s03 and s04 rasterise identically. times: one time (static) or two (a cross-fade driven by u(t)
    0..1); the sun is drawn for each time and moved by sun_m (s04 lets it sink)."""
    two = len(times) > 1

    def lay(name, fn, z, seed, motion=None, wc=1.0):
        svgs = [fn(t) for t in times]
        mo = M.combine(*(m for m in (motion, gatef) if m is not None))
        if two:
            sc.add(name, svgs, z=z, seed=seed, wc=wc, frame_at=lambda t: float(min(1.0, max(0.0, u(t)))), motion=mo)
        else:
            sc.add(name, svgs[0], z=z, seed=seed, wc=wc, motion=mo)
    lay("h_sky", h_sky_svg, Z_H, SEED_H)
    lay("h_back", lambda t: h_part_svg(t, "back"), Z_H + 1, SEED_H + 2)
    lay("h_mid", lambda t: h_part_svg(t, "mid"), Z_H + 3, SEED_H + 3)
    lay("h_rock", h_rock_svg, Z_H + 3.5, SEED_H + 4)
    add_glints(sc, "h_glint", Z_H + 1.5, (60, W - 300, FY + 26, LY - 12), times[0], g0, gatef, SEED_H + 5, n=60, size=1.1)
    add_clouds(sc, "h_cloud", Z_H + 0.6, H_CLOUDS, times[0], g0, gatef, SEED_H + 10, vx=3.0)
    add_birds(sc, "h_bird", Z_H + 0.7, H_BIRDS, 1.1, g0, gatef, seed=SEED_H + 20)
    # front corners rocking in the breeze (one layer per corner)
    for side in (0, 1):
        body = [PR.lake_hillside(HX0, HX1, HY, HS, time=t, part="front", seed=0, bottom=H + 40, rock_x=RX) for t in times]
        x0 = 0 if side == 0 else W - 700
        cid = f"lf3hfc{side}"
        clipped = [doc(f'<clipPath id="{cid}"><rect x="{x0}" y="{H - 420}" width="700" height="460"/></clipPath>'
                       f'<g clip-path="url(#{cid})">{b_}</g>') for b_ in body]
        piv = (x0 + (200 if side == 0 else 500), H + 30)

        def m(t, side=side, piv=piv):
            uu = (t + g0) / 3.9 + 0.37 * side
            return Tf(rot=0.45 * (math.sin(2 * math.pi * uu) + 0.35 * math.sin(2 * math.pi * (1.7 * uu + 0.3))), px=piv[0], py=piv[1])
        mo = M.combine(m, gatef)
        if two:
            sc.add(f"h_front{side}", clipped, z=Z_H + 9 + 0.01 * side, seed=SEED_H + 30 + side,
                   frame_at=lambda t: float(min(1.0, max(0.0, u(t)))), motion=mo)
        else:
            sc.add(f"h_front{side}", clipped[0], z=Z_H + 9 + 0.01 * side, seed=SEED_H + 30 + side, motion=mo)


def add_sun(sc, gatef, times=(H_TIME,), u=None, pos=None):
    """The sun on its own layer behind the far hills; pos(t) -> (dx, dy) lets it sink (s04)."""
    svgs = [sun_svg(t, *SUN0) for t in times]
    mo = M.combine(*(m for m in ((lambda t: Tf(dx=pos(t)[0], dy=pos(t)[1])) if pos else None, gatef) if m is not None))
    if len(svgs) > 1:
        sc.add("h_sun", svgs, z=Z_H + 0.5, seed=SEED_H + 1, wc=0.4, frame_at=lambda t: float(min(1.0, max(0.0, u(t)))), motion=mo)
    else:
        sc.add("h_sun", svgs[0], z=Z_H + 0.5, seed=SEED_H + 1, wc=0.4, motion=mo)


# ---- the seated groups (F and s04): (x, depth, n, family seed)
F_GROUPS = [
    (170, 0.93, 11, 0), (540, 0.95, 9, 1), (740, 0.97, 8, 2), (1260, 0.95, 10, 3), (1980, 0.93, 9, 4), (2380, 0.92, 11, 5),
    (330, 0.78, 12, 6), (700, 0.80, 8, 7), (2160, 0.77, 12, 8), (2520, 0.70, 8, 9),
    (120, 0.60, 10, 10), (470, 0.62, 12, 11), (2340, 0.52, 12, 12),
    (2470, 0.30, 12, 14),
]


def group_svg(i):
    x, d, n, fs = F_GROUPS[i]
    y, k = hy_d(d, x)
    return doc(C.galilee_groups(0, 0, 0, 0, 1.0, groups=[(x, y, k)], focus=RX, seed=fs, per_group=(n, n), rows=1))


def add_groups(sc, gatef, g0, z=Z_H + 4.0):
    """The seated groups, each on its own layer breathing gently on the global clock (the crowd stays alive)."""
    for i, (x, d, n, fs) in enumerate(F_GROUPS):
        y, k = hy_d(d, x)
        ph = (i * 0.37) % 1.0
        per = 3.2 + 0.4 * (i % 4)

        def m(t, ph=ph, per=per, x=x, y=y, k=k):
            v = math.sin(2 * math.pi * ((t + g0) / per + ph))
            w = math.sin(2 * math.pi * ((t + g0) / (per * 2.3) + ph * 1.7))
            return Tf(dx=1.6 * k * w, sx=1 + 0.002 * v, sy=1 + 0.006 * v, px=x, py=y + 20 * k)
        sc.add(f"h_grp{i}", group_svg(i), z=z + y / 10000.0, seed=SEED_H + 100 + i, motion=M.combine(m, gatef))


# ---- the people near Jesus (F and s04)
LAME = (RX - 140 * JK, RY)              # the man with the crutch (facing +1)
LAME_V = 4
MOTHER = (RX - 360 * JK, RY + 34)       # the mother with her feverish child (facing +1)
SICK_WIDE_DX = -120                     # in the wide teaching shot the sick sit a little further from the rock
MOTHER_V = 9
# the hungry family at the front left (s04's tummies): (kind, variant, x, y-offset, facing)
FAMILY = [("man", 13, 250, 0), ("woman", 7, 345, 12), ("child", 2, 165, 28), ("child", 9, 420, 30), ("elder", 3, 70, 4)]
FAMILY_Y = 1262
# the disciples (F positions; they walk to Jesus in s04): (name, variant, x, y)
DISC_F = [("p4", 4, 1480, RY + 40), ("p0", 0, 1620, RY + 12), ("p1", 1, 1760, RY - 14), ("p2", 2, 1900, RY + 30), ("p3", 3, 2040, RY - 4)]
DISC_FB = []


def family_member_markup(j, key):
    kind, v, x, dy = FAMILY[j]
    y = FAMILY_Y + dy
    pose, expr = key[0], key[1]
    ph = key[2] if len(key) > 2 else 0.0
    return folk(x, y, hk(y), 1, kind=kind, v=v, pose=pose, expr=expr, phase=ph)


def lame_markup(key):
    pose, expr = key[0], key[1]
    x, y = LAME
    if pose == "healed":
        x -= 62 * JK
    return folk(x, y, JK, 1, kind="lame", v=LAME_V, pose=pose, expr=expr)


def mother_markup(key):
    pose, expr = key[0], key[1]
    x, y = MOTHER
    return folk(x, y, hk(y), 1, kind="fever_mother", v=MOTHER_V, pose=pose, expr=expr)


def jesus_f_markup(key):
    pose, expr = key[0], key[1]
    f = key[2] if len(key) > 2 else -1
    return jes(RX, RY, JK, f, pose=pose, expr=expr)


def disc_f_markup(v, x, y, key):
    pose, expr = key[0], key[1]
    f = key[2] if len(key) > 2 else -1
    ph = key[3] if len(key) > 3 else 0.0
    mk = key[4] if len(key) > 4 else True
    return shadow(x, y, hk(y), 100, 0.14) + disc(x, y, hk(y), f, v, pose=pose, expr=expr, phase=ph, marks=mk)


def add_f_people(sc, gatef, g0, z, keys=None, seed=SEED_H + 200):
    """The family, the healed (or sick) and the disciples at their F places, as they are at the end of s03 - the
    shared first frame of s04. keys: dict name -> list of (t, key) cuts (default: s03's end state); returns the actors
    (unbuilt) so s04 can add moves before building them."""
    acts = {}
    for j, (kind, v, x, dy) in enumerate(FAMILY):
        y = FAMILY_Y + dy
        a = Actor(f"fam{j}", (x, y), hk(y), lambda k, j=j: family_member_markup(j, k), z + y / 10000.0, seed + j, g0, gatef)
        a.extra.append(breathm(g0, 2.9 + 0.3 * j, 0.010, 0.21 * j))
        acts[f"fam{j}"] = a
    a = Actor("lame", LAME, JK, lame_markup, z + LAME[1] / 10000.0 + 0.00001, seed + 10, g0, gatef)
    a.extra.append(breathm(g0, 3.1, 0.010, 0.4))
    acts["lame"] = a
    a = Actor("mother", MOTHER, hk(MOTHER[1]), mother_markup, z + MOTHER[1] / 10000.0, seed + 11, g0, gatef)
    a.extra.append(breathm(g0, 3.3, 0.010, 0.7))
    acts["mother"] = a
    a = Actor("jesus", (RX, RY), JK, jesus_f_markup, z + RY / 10000.0, seed + 12, g0, gatef)
    a.extra.append(breathm(g0, 3.4, 0.008, 0.1))
    acts["jesus"] = a
    for i, (nm, v, x, y) in enumerate(DISC_F + DISC_FB):
        a = Actor(nm, (x, y), hk(y), lambda k, v=v, x=x, y=y: disc_f_markup(v, x, y, k), z + y / 10000.0, seed + 20 + i, g0,
                  gatef)
        a.extra.append(breathm(g0, 2.8 + 0.17 * i, 0.010, 0.13 * i))
        acts[nm] = a
    return acts


def f_end_keys():
    """Every F actor's key at the end of s03 (= the first frame of s04)."""
    k = {f"fam{j}": ("sit_listen" if j % 2 == 0 else "sit", "kind") for j in range(len(FAMILY))}
    k["fam2"] = ("sit_laugh", "delighted")
    k.update(lame=("healed", "overjoyed"), mother=("healed", "joyful"), jesus=("look_kind", "smile"))
    for nm, v, x, y in DISC_F:
        k[nm] = ("stand", "awed" if v % 2 else "happy")
    for nm, v, x, y in DISC_FB:
        k[nm] = ("stand", "happy")
    return k


CAM_F_END = Cam(950, 905, 1720)         # the last frame of s03 = the first frame of s04


# ================================================================== E: the crowd arrives, Jesus steps ashore
E_D_BACK, E_D_FRONT = 0.74, 0.64
# (kind, variant, x, row): the crowd that ran round the lake, standing on the slope right of the path, facing Jesus
E_CROWD = [("man", 0, 1420, 0), ("woman", 7, 1545, 0), ("elder", 3, 1670, 0), ("man", 10, 1795, 0), ("woman", 4, 1920, 0),
           ("man", 13, 2045, 0), ("woman", 11, 2170, 0), ("man", 14, 2295, 0),
           ("child", 2, 1360, 1), ("mother", 5, 1480, 1), ("child", 9, 1600, 1), ("man", 8, 1720, 1), ("woman", 1, 1840, 1),
           ("child", 6, 1960, 1), ("man", 15, 2080, 1), ("elder", 9, 2200, 1), ("child", 4, 2320, 1)]
E_JESUS_STOP = 1120                      # x where Jesus stops (y from depth .66)
E_BOAT = (430, LY - 6)                   # the boat at the shore (fishing_boat, bow to the right)
KB = HS * 0.38                           # the boat and its crew at the shore line
E_BUB = (1580, 410)
E1_BOAT = (900, 686)                     # the far boat in the arrival shot (waterline, mid-lake, left of the crowd)
E_POINTERS = {(0, 0), (2, 1)}            # (variant, row) of the runners who point back at it (the leftmost two)                      # the thought bubble's centre
E_BUB_R = (300, 196)


def e_member(kind, v, x, row, key, side):
    d = E_D_BACK if row == 0 else E_D_FRONT
    y, k = hy_d(d + 0.01 * ((v * 7) % 3), x)
    pose = key[0]
    q = key[1] if len(key) > 1 else 0
    j = (v * 5 + row) % 7
    if pose == "run":
        p_ = ("run_a" if (j + q) % 2 == 0 else "run_b") if kind != "elder" else ("walk_a" if q % 2 == 0 else "walk_b")
        return shadow(x, y, k, 100, 0.14) + folk(x, y, k, 1, kind=kind, v=v, pose=p_, expr="eager")
    if pose == "arrive":
        p_ = ("arrive", "point", "arrive", "wave", "arrive", "point", "cheer")[j]
        if kind == "elder":
            p_ = "arrive"
        f = 1
        if (v, row) in E_POINTERS:            # these two turn back and point at the boat still out on the lake
            p_, f = "point", -1
        elif p_ == "point":
            p_ = "wave"
        expr = "tired" if p_ == "arrive" else "eager"
        return shadow(x, y, k, 100, 0.14) + folk(x, y, k, f, kind=kind, v=v, pose=p_, expr=expr, phase=0.25 * q)
    # listen: facing Jesus; a couple of people change pose per variant q (shuffling, waving, pointing)
    f = -1
    p_ = ("stand_listen", "stand", "stand_listen", "point", "stand", "stand_listen", "wave")[j]
    if (j + q) % 5 == 0 and p_ == "stand":
        p_ = "stand_listen"
    expr = key[2] if len(key) > 2 else ("happy" if j % 2 else "kind")
    if kind == "elder" and p_ not in ("stand", "stand_listen"):
        p_ = "stand"
    return shadow(x, y, k, 100, 0.14) + folk(x, y, k, f, kind=kind, v=v, pose=p_, expr=expr, phase=0.33 * q)


def e_cluster_markup(members, side, key):
    out = ""
    for (kind, v, x, row) in sorted(members, key=lambda m_: (m_[3], m_[2])):
        out += e_member(kind, v, x, row, key, side)
    return out


def e_boat_part(part):
    return doc(PR.fishing_boat(*E_BOAT, KB, 1, sail="furled", part=part, oars="in", cushion=False, nets=True))


def e_crew_markup(key):
    """Peter, Andrew and John standing in the boat (between its back and front)."""
    bx, by = E_BOAT
    out = ""
    for (v, dx, pose, expr) in ((3, -230, "stand", "happy"), (0, -90, key[0], key[1]), (1, 40, "stand", "awed")):
        out += disc(bx + dx * KB / 0.475, by, KB, 1, v, pose=pose, expr=expr)
    return out


def sheep_bubble_frame(cx, cy, rx, ry):
    """The thought bubble's frame and its little picture background (a green hill under a warm sky)."""
    rng = random.Random(5)
    n = 18
    puffs = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = 44 * rng.uniform(0.85, 1.15)
        puffs.append((cx + (rx + rr * 0.3) * math.cos(a), cy + (ry + rr * 0.3) * math.sin(a), rr))
    out = ""
    for x, y, rr in puffs:
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr)}" fill="#fffaf0" stroke="{INK}" stroke-width="8"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 10}" ry="{ry + 10}" fill="#fffaf0" stroke="{INK}" stroke-width="8"/>'
    for x, y, rr in puffs:
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rr)}" fill="#fffaf0"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 10}" ry="{ry + 10}" fill="#fffaf0"/>'
    pal = PR._lf_pal(0.3)
    clip = f'<clipPath id="lf3bubc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>'
    inner = f'<rect x="{cx - rx - 10}" y="{cy - ry - 10}" width="{2 * rx + 20}" height="{2 * ry + 20}" fill="{S.mix(pal["sky"][3], "#fffaf0", 0.2)}"/>'
    inner += PR._p(S.hill(cx - rx - 40, cx + rx + 40, cy + ry * 0.05, 60, seed=4, bottom=cy + ry + 40, bumps=2),
                   S.mix(pal["grass"][3], pal["grass"][0], 0.5), 3.0)
    inner += PR._p(S.hill(cx - rx - 40, cx + rx + 40, cy + ry * 0.45, 40, seed=7, bottom=cy + ry + 40, bumps=3), pal["grass"][0], 3.0)
    for j in range(7):
        fx_ = cx - rx * 0.8 + rx * 1.6 * rng.random()
        fy_ = cy + ry * (0.35 + 0.5 * rng.random())
        inner += PR._circ(fx_, fy_, 5, PR.ANEMONE if j % 2 else PR.CROWN_DAISY, 1.6)
    out += clip + f'<g clip-path="url(#lf3bubc)">{inner}</g>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#d9c095" stroke-width="3.5"/>'
    return doc(S.g(out, filter="wobble-fine"))


# sheep in the bubble: (start x, y, facing, variant, step px)
SHEEP_B = [(-180, 70, 1, 0, 22), (-40, 120, -1, 1, 20), (90, 60, 1, 2, 18), (190, 130, -1, 3, 22), (-120, 150, 1, 1, 16)]
SHEEP_K = 0.38


def sheep_frame(step, confused=None):
    """All bubble sheep at walk step ``step`` (alternating walk_a / walk_b, each a little further along its way), or
    stopped and looking about (confused = 0 / 1: which way they look)."""
    cx, cy = E_BUB
    rx, ry = E_BUB_R
    out = ""
    for i, (sx_, sy_, f, v, stp) in enumerate(sorted(SHEEP_B, key=lambda s_: s_[1])):
        if confused is None:
            x = cx + sx_ + f * stp * step
            pose = "walk_a" if (step + i) % 2 == 0 else "walk_b"
            ff = f
        else:
            x = cx + sx_ + f * stp * 7
            pose = ("stand", "look_up", "bleat", "stand", "look_up")[i] if confused == 0 else ("look_up", "stand", "stand", "bleat", "stand")[i]
            ff = f if (confused + i) % 2 == 0 else -f
        y = cy + sy_
        out += C.ground_shadow(x, y, SHEEP_K, 120, 0.16) + PR.sheep(x, y, SHEEP_K, ff, variant=v, pose=pose)
    clip = f'<clipPath id="lf3bubs"><ellipse cx="{cx}" cy="{cy}" rx="{rx - 2}" ry="{ry - 2}"/></clipPath>'
    return doc(clip + f'<g clip-path="url(#lf3bubs)">{out}</g>')


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    L = ctx.lines

    # ---- shot boundaries (hard cuts on phrase boundaries)
    t_B = snap(L[3].start - 0.12)
    t_E1 = snap(tm.at(3, "比船还先到了", 0) - 0.12)
    t_E2 = snap(L[4].start - 0.1)
    t_F = snap(L[5].start - 0.08)
    t_FM = snap(tm.at(5, "还把生病的人", 0) - 0.14)
    gA, gS, gHill = gate(-1, t_B), gate(-1, t_E1), gate(t_E1, 1e9)
    gBD = gate(t_B, t_E1)
    gE1, gE2, gE, gF = gate(t_E1, t_E2), gate(t_E2, t_F), gate(t_E1, t_F), gate(t_F, 1e9)

    # ================================================================ SET S
    sc.add("s_sky", s_sky_svg(), z=10.0, seed=SEED_S, motion=gS)
    add_clouds(sc, "s_cloud", 10.01, [(300, 440, 380, 31), (980, 400, 440, 33), (1640, 450, 360, 35), (2360, 410, 400, 37)],
               S_TIME, g0, gS, SEED_S + 10, vx=5.0)
    sc.add("s_back", s_back_svg(), z=10.05, seed=SEED_S + 6, motion=gS)
    add_birds(sc, "s_bird", 10.2, [(600, 420), (1300, 400), (1900, 440)], 1.0, g0, gS, seed=SEED_S + 20)
    add_glints(sc, "s_glint", 10.3, (40, W - 40, S_FAR + 30, S_SHORE - 14), S_TIME, g0, gS, SEED_S + 5, n=70, size=1.1)
    sc.add("s_path", s_path_svg(), z=11.0, seed=SEED_S + 1, motion=gS)
    front = s_front_body()
    sway_corner(sc, "s_front_l", front, (0, YS - 300, 520, 640), (200, H + 30), 19.0, SEED_S + 2, g0, gS)
    sway_corner(sc, "s_front_r", front, (W - 520, YS - 300, 520, 640), (W - 200, H + 30), 19.01, SEED_S + 3, g0, gS, phase=0.4)

    # ---- the boat: moored (A), the crew aboard pushes off and sails away (B..D)
    t_zuo = tm.at(3, "他们坐船", 2)
    t_bian = tm.at(3, "到湖的那一边去", 5)
    t_sail = snap(t_zuo + 0.05)
    bx0, by0 = BOAT_MOOR
    sc.add("s_boat_moor", far_boat_svg(bx0, by0, 0.22, "furled", crew=False), z=10.5, seed=SEED_S + 40, wc=0.6,
           motion=M.combine(lambda t: Tf(dy=2.5 * math.sin(2 * math.pi * (t + g0) / 3.1), rot=0.5 * math.sin(2 * math.pi * (t + g0) / 3.7),
                                         px=bx0, py=by0), gA))
    boat_frames = [far_boat_svg(bx0, by0, 0.22, "furled"), far_boat_svg(bx0, by0, 0.22, "full")]

    def boat_m(t):
        u = M.progress(t, t_sail - 0.2, t_E1 + 1.0, lambda q: q ** 1.4)
        sk = 1 - 0.18 * u
        return Tf(dx=300 * u, dy=-60 * u + 2.5 * math.sin(2 * math.pi * (t + g0) / 3.1), sx=sk, sy=sk,
                  rot=0.6 * math.sin(2 * math.pi * (t + g0) / 3.7), px=bx0, py=by0)
    sc.add("s_boat", boat_frames, z=10.5, seed=SEED_S + 41, wc=0.6, frame_at=lambda t: 1.0 if t >= t_sail else 0.0,
           motion=M.combine(boat_m, gBD))
    sc.sfx("cloth", t_sail, gain_db=-12)
    sc.sfx("splash_small", t_zuo - 0.2, gain_db=-20)

    # ---- shot A: the group, numbers, busy people, the bread
    t_count0 = tm.at(0, "耶稣有十二个好朋友", 1)
    t_count1 = tm.at(0, "耶稣有十二个好朋友", 8)
    t_jiao = tm.at(0, "叫做门徒", 0)
    t_youyitian = tm.at(1, "有一天", 0)
    t_mang = tm.at(1, "耶稣和门徒们好忙好忙", 6)
    t_mang2 = tm.at(1, "耶稣和门徒们好忙好忙", 8)
    t_lian = tm.at(1, "连吃饭的时间都没有", 0)
    t_fan = tm.at(1, "连吃饭的时间都没有", 2)
    t_shi = tm.at(1, "连吃饭的时间都没有", 4)
    t_dou = tm.at(1, "连吃饭的时间都没有", 6)
    t_ysay = tm.at(1, "耶稣说", 0)
    t_an = tm.at(2, "我们到安静的地方", 3)
    t_xiu = tm.at(2, "去休息一下吧", 1)

    gpos = {nm: (x, y, s_, f) for nm, v, x, y, s_, f in A_GROUP}
    gvar = {nm: v for nm, v, x, y, s_, f in A_GROUP}
    n_order = {nm: i for i, nm in enumerate(COUNT_ORDER)}
    step_c = (t_count1 + 0.15 - t_count0) / 11.0
    t_num = {nm: snap(t_count0 + step_c * i) for nm, i in n_order.items()}
    t_num_out = snap(tm.end(0, "叫做门徒") + 0.35)

    def disc_a_markup(nm, key):
        x, y, s_, f = gpos[nm]
        v = gvar[nm]
        pose, expr = key[0], key[1]
        ff = key[2] if len(key) > 2 else f
        if pose == "bread":
            return shadow(x, y, s_, 100, 0.15) + disc_bread(x, y, s_, ff, v, key[3], expr, rot=key[4] if len(key) > 4 else 0.0,
                                                           h=key[5] if len(key) > 5 else 0.0)
        ph = key[3] if len(key) > 3 else 0.0
        return shadow(x, y, s_, 100, 0.15) + disc(x, y, s_, ff, v, pose=pose, expr=expr, phase=ph)

    actors = {}
    for i, (nm, v, x, y, s_, f) in enumerate(A_GROUP):
        if v is None:
            continue
        a = Actor(f"a_{nm}", (x, y), s_, lambda k, nm=nm: disc_a_markup(nm, k), 12.0 + y / 10000.0 + 0.00001 * i, SEED_S + 100 + i,
                  g0, gA)
        a.cut(0, ("stand", "happy" if i % 3 else "kind"))
        a.extra.append(breathm(g0, 2.8 + 0.13 * i, 0.010, 0.17 * i))
        if nm in t_num:
            a.extra.append(hopm(t_num[nm] + 0.02, s_, 10, 0.22))
        actors[nm] = a
    # '叫做门徒': two wave, the rest smile
    t_wave = snap(t_jiao + 0.1)
    for nm in ("d7", "d11"):
        actors[nm].loop(t_wave, [("wave", "happy", gpos[nm][3], q / 4) for q in range(4)], 0.12, dip=4)
        actors[nm].cut(snap(t_wave + 1.25), ("stand", "happy"), dip=4)
    # busy: heads turn this way and that
    busy = [("d1", -1, t_mang - 0.4), ("d10", 1, t_mang), ("d6", -1, t_mang + 0.25), ("d2", 1, t_mang2), ("d5", -1, t_mang2 + 0.3),
            ("d9", 1, t_mang - 0.15)]
    for nm, ff, tb in busy:
        f0 = gpos[nm][3]
        actors[nm].cut(snap(tb), ("stand", "tired" if ff != f0 else "worried", ff), dip=4)
        actors[nm].cut(snap(tb + 1.3), ("stand", "neutral", f0), dip=4)
    # John points the way for the old man
    t_old_stop = snap(t_youyitian + 1.5)
    actors["d3"].cut(snap(t_old_stop + 0.35), ("point", "kind", 1), dip=4)
    actors["d3"].cut(snap(t_old_stop + 1.6), ("stand", "happy", -1), dip=4)
    # Peter and his bread: holds it, lifts it to his mouth, the boy tugs, it comes down, the sigh; the bite on '休息'
    pe = actors["d0"]
    HAND_HIP, HAND_MOUTH = (34, -150), (36, -262)
    pe.cut(0, ("bread", "happy", -1, HAND_HIP, -8))
    t_lift = snap(t_lian - 0.05)
    pe.cut(t_lift, ("bread", "happy", -1, HAND_MOUTH, -18, -6), dip=3)
    t_tug = snap(t_shi + 0.02)
    pe.cut(t_tug, ("bread", "surprised", 1, HAND_HIP, -8), dip=5)
    t_sigh = snap(t_dou + 0.05)
    pe.cut(t_sigh, ("bread", "tired", -1, HAND_HIP, -8, 8), dip=4)
    t_peter_ok = snap(t_ysay + 0.2)
    pe.cut(t_peter_ok, ("bread", "neutral", -1, HAND_HIP, -8), dip=3)
    t_bite = snap(t_xiu - 0.05)
    pe.cut(t_bite, ("bread", "happy", -1, HAND_MOUTH, -18, -6), dip=3)
    pe.cut(snap(t_bite + 0.7), ("bread", "yum", -1, HAND_MOUTH, -18, -6), dip=2)
    sc.add("a_sweat", sweat_svg(gpos["d0"][0] - 52, gpos["d0"][1] - 305 * KA, 1.1), z=12.9, wc=0.3, seed=SEED_S + 150,
           motion=M.combine(lambda t: Tf(dy=14 * M.progress(t, t_sigh, t_sigh + 0.9, "in"),
                                         alpha=env(t, t_sigh + 0.05, t_sigh + 1.2, 0.12, 0.3)), gA))
    # the disciples hearing '休息' are glad
    for nm in ("d1", "d2", "d6", "d10", "d4"):
        actors[nm].cut(snap(t_xiu + 0.1 + 0.05 * n_order[nm] / 3), ("stand", "happy", gpos[nm][3]), dip=3)
    for nm in ("d7", "d8", "d9", "d11", "d5", "d3"):
        actors[nm].cut(snap(t_an + 0.2 + 0.04 * n_order[nm]), ("stand", "happy" if n_order[nm] % 2 else "delighted", gpos[nm][3]), dip=3)
    for nm, a in actors.items():
        a.blinks([1.4 + 0.37 * n_order.get(nm, 0), 6.0 + 0.53 * n_order.get(nm, 0), 12.1 + 0.29 * n_order.get(nm, 0)],
                 {("stand", "happy"): ("stand", blink("happy")), ("stand", "kind"): ("stand", blink("kind")),
                  ("stand", "neutral", gpos[nm][3]): ("stand", blink("neutral"), gpos[nm][3])})
        a.build(sc)

    # number badges over the heads
    for nm, tn in t_num.items():
        x, y, s_, f = gpos[nm]
        hx_, hy_ = x + 2 * s_ * f, y - 370 * s_
        sc.add(f"a_num_{nm}", badge_svg(hx_, hy_, n_order[nm] + 1, r=32), z=13.0, wc=0.0, seed=SEED_S + 200 + n_order[nm],
               motion=M.combine(popm(tn, (hx_, hy_), 0.25, t_out=t_num_out + 0.03 * n_order[nm], out_dur=0.3, wob=False), gA))
        sc.sfx("pop", tn, gain_db=-24 + (2 if n_order[nm] == 11 else 0), pan=(x - 1300) / 1600)

    # Jesus in A
    jx, jy, js, jf = gpos["jesus"]

    def jesus_a_markup(key):
        pose, expr, f = key[0], key[1], key[2]
        return shadow(jx, jy, js, 110, 0.16) + jes(jx, jy, js, f, pose=pose, expr=expr)
    ja = Actor("a_jesus", (jx, jy), js, jesus_a_markup, 12.0 + jy / 10000.0 + 0.0002, SEED_S + 120, g0, gA)
    ja.cut(0, ("stand", "warm", 1))
    t_mom_stop = snap(t_youyitian + 1.15)
    ja.cut(snap(t_mom_stop + 0.25), ("bless", "kind", -1), dip=3)
    ja.cut(snap(t_mom_stop + 2.2), ("stand", "warm", -1), dip=3)
    t_jturn = snap(t_ysay - 0.1)
    ja.cut(t_jturn, ("turn_kind", "kind", 1), dip=3)
    t_jpoint = snap(t_an - 0.1)
    ja.cut(t_jpoint, ("point", "warm", 1), dip=3)
    t_jopen = snap(t_xiu - 0.25)
    ja.cut(t_jopen, ("open_hands", "smile", 1), dip=3)
    ja.extra.append(breathm(g0, 3.4, 0.008, 0.1))
    ja.blinks([2.3, 4.6, 8.0, 10.2, 13.9], {("stand", "warm", 1): ("stand", blink("warm"), 1),
                                            ("stand", "warm", -1): ("stand", blink("warm"), -1),
                                            ("turn_kind", "kind", 1): ("turn_kind", blink("kind"), 1)})
    ja.build(sc)

    # people coming and going (planted walks along the near lane)
    def add_walker(name, kind, v, y, x_from, x_to, t0, per, s_=KA, z=12.5, expr="kind", stop_key=None, then=None, run=False):
        """A villager walking (or running) along a lane from x_from to x_to starting at t0 (planted feet; FOLK_ADV-like
        strides). stop_key: the pose when he arrives; then: [(t, key)] later cuts (and ('walk', x2, t2) to walk on).
        The drawings are made at a home inside the canvas (the arrival point when it is on the stage) and moved."""
        f = 1 if x_to > x_from else -1
        adv = (84 if kind in ("man", "elder", "lame") else 81 if kind in ("woman", "mother") else 50) * (1.9 if run else 1.0)
        home = x_to if 80 < x_to < W - 80 else (x_from if 80 < x_from < W - 80 else W / 2)

        def draw(key, kind=kind, v=v, y=y, s_=s_):
            pose, ex, ff = key[0], key[1], key[2]
            ph = key[3] if len(key) > 3 else 0.0
            return shadow(home, y, s_, 100, 0.15) + folk(home, y, s_, ff, kind=kind, v=v, pose=pose, expr=ex, phase=ph)
        a = Actor(name, (home, y), s_, draw, z + y / 10000.0, SEED_S + 300 + sum(map(ord, name)) % 97, g0, gA)
        a.shift(x_from - home)
        dist = abs(x_to - x_from)
        n = max(2, int(round(dist / (adv * s_))))
        cyc = ((("run_a" if run else "walk_a"), dist / n / s_), (("run_b" if run else "walk_b"), dist / n / s_))
        a.cut(0, ("walk_a" if not run else "run_a", expr, f))
        a.walk(t0, [((k, expr, f), ad) for k, ad in cyc], n, per, f)
        t_end = snap(t0 + n * per)
        if stop_key is not None:
            a.cut(t_end, stop_key, dip=4)
        if then:
            for item in then:
                if item[0] == "walk":
                    _, x2, t2, ex2 = item
                    f2 = 1 if x2 > x_to else -1
                    d2 = abs(x2 - x_to)
                    n2 = max(2, int(round(d2 / (adv * s_))))
                    cyc2 = ((("walk_a"), d2 / n2 / s_), (("walk_b"), d2 / n2 / s_))
                    a.walk(snap(t2), [((k, ex2, f2), ad) for k, ad in cyc2], n2, per, f2)
                else:
                    a.cut(snap(item[0]), item[1], dip=item[2] if len(item) > 2 else 4)
        a.extra.append(breathm(g0, 3.0, 0.010, 0.3))
        return a, t_end
    # (the walkers' drawings are made at x_from; the Actor moves them)
    # a mother and her little girl come to Jesus from the left and stand before him
    mom, t_ms = add_walker("a_mom", "woman", 1, LANE_F, -160, 1170, snap(t_youyitian - 1.2), 0.24, stop_key=("stand_listen", "happy", 1),
                           then=[(t_mom_stop + 2.4, ("stand", "happy", 1))])
    mom.build(sc)
    girl, _ = add_walker("a_girl", "child", 3, LANE_F + 18, -60, 1240, snap(t_youyitian - 1.2), 0.24,
                         stop_key=("stand", "delighted", 1), then=[(t_mom_stop + 0.4, ("wave", "delighted", 1, 0.3)),
                                                                  (t_mom_stop + 1.6, ("stand", "happy", 1))])
    girl.build(sc)
    # an old man comes from the right and asks John the way, then walks on to the left
    old, _ = add_walker("a_old", "elder", 3, LANE_F - 4, W + 140, 1930, snap(t_youyitian - 0.7), 0.3, stop_key=("stand", "kind", -1),
                        then=[("walk", W + 300, t_old_stop + 1.7, "happy")])
    old.build(sc)
    # walkers crossing in both directions
    w1, _ = add_walker("a_w1", "man", 14, LANE_F + 30, W + 120, -220, snap(t_youyitian - 1.0), 0.22, expr="neutral")
    w1.build(sc)
    w2, _ = add_walker("a_w2", "woman", 10, LANE_F + 24, -200, W + 200, snap(t_xiu - 1.0), 0.26, expr="happy")
    w2.build(sc)
    # the boy who tugs at Peter: runs in from the right, stops, points back, runs off
    bx_stop = gpos["d0"][0] + 85
    boy, t_bs = add_walker("a_boy", "child", 0, LANE_F + 10, W + 100, bx_stop, snap(t_shi - 1.95), 0.13, run=True,
                           stop_key=("point", "eager", 1), then=[("walk", W + 200, t_shi + 1.0, "eager")])
    boy.build(sc)
    sc.sfx("footsteps_run", t_shi - 1.95, dur=1.7, gain_db=-20, pan=0.5)
    sc.sfx("cloth", t_tug, gain_db=-14)
    for (t_, dur, pan) in ((t_youyitian - 1.2, 3.0, -0.5), (t_mang - 1.0, 4.5, 0.4), (t_lian - 1.3, 5.0, -0.3)):
        sc.sfx("footsteps", t_, dur=dur, gain_db=-24, pan=pan)

    # ================================================================ B / C / D: the boat leaves; they see; they run
    t_keshi = tm.at(3, "可是", 0)
    t_kan = tm.at(3, "好多人看见了", 3)
    t_dajia = tm.at(3, "大家沿着湖边", 0)
    pao = [tm.at(3, "跑啊跑", 0), tm.at(3, "跑啊跑", 2)]
    m2 = [m for m in tm.marks[3] if m and m[0] == "跑啊跑"]
    if len(m2) >= 2:
        from stories.noah.scenes.s01_title import char_times
        ct = char_times(m2[1])
        pao += [ct[0], ct[2]]
    else:
        pao += [pao[1] + 0.55, pao[1] + 1.1]
    # villagers on the path (B, C): wave at the boat, turn and point; then run (D)
    VILL = [("man", 14, 520, LANE_F + 10), ("woman", 1, 700, LANE_F - 6), ("child", 3, 800, LANE_F + 26), ("elder", 3, 980, LANE_F),
            ("man", 8, 1180, LANE_F + 14), ("child", 0, 1330, LANE_F + 28), ("woman", 10, 1480, LANE_F + 4), ("man", 2, 1650, LANE_F + 16)]
    t_run0 = snap(t_dajia + 0.05)
    for i, (kind, v, x, y) in enumerate(VILL):
        def draw(key, kind=kind, v=v, x=x, y=y):
            pose, ex, ff = key[0], key[1], key[2]
            ph = key[3] if len(key) > 3 else 0.0
            return shadow(x, y, KA, 100, 0.15) + folk(x, y, KA, ff, kind=kind, v=v, pose=pose, expr=ex, phase=ph)
        a = Actor(f"b_v{i}", (x, y), KA, draw, 14.0 + y / 10000.0 + 0.00001 * i, SEED_S + 400 + i, g0, gBD)
        if i % 3 == 0:
            a.loop(t_B, [("wave", "happy", 1, q / 4) for q in range(4)], 0.13, phase=0.3 * i)
        else:
            a.cut(t_B, ("stand", "happy", 1))
        t_turn = snap(t_keshi + 0.06 * i)
        a.cut(t_turn, ("stand", "surprised", 1), dip=4)
        t_pt = snap(t_kan - 0.15 + 0.07 * i)
        a.cut(t_pt, ("point" if kind != "elder" else "stand", "eager" if kind != "elder" else "surprised", 1), dip=5)
        # run
        t_r = snap(t_run0 + 0.09 * (i % 4))
        run = kind != "elder"
        per = 0.14 if run else 0.24
        nrun = int((t_E1 - t_r) / per) + 1
        for q in range(nrun):
            p_ = ("run_a" if q % 2 == 0 else "run_b") if run else ("walk_a" if q % 2 == 0 else "walk_b")
            a.cut(t_r + q * per, (p_, "eager", 1))
        speed = (560 + 40 * (i % 3)) if run else 230
        a.moves.append(lambda t, t_r=t_r, sp=speed: (sp * max(0.0, t - t_r) * min(1.0, max(0.0, t - t_r) / 0.35) ** 0.5, 0.0))
        bob_t = list(pao)
        a.extra.append(lambda t, bt=bob_t: Tf(dy=-sum(16 * KA * math.sin(math.pi * min(1.0, max(0.0, (t - b) / 0.22)))
                                                      for b in bt if b <= t <= b + 0.22)))
        a.extra.append(breathm(g0, 3.0, 0.010, 0.2 * i))
        a.build(sc)
        if i % 2 == 0:
            sc.add(f"b_ex{i}", mark_svg(x + 30, y - 340 * KA, "!", 70), z=14.9, wc=0.0, seed=SEED_S + 450 + i,
                   motion=M.combine(popm(snap(t_pt + 0.08), (x + 30, y - 360 * KA), 0.25, t_out=t_run0 + 0.4, out_dur=0.25), gBD))
    sc.sfx("pop", t_kan, gain_db=-16)
    # the crowd streaming in from the village behind the villagers (two rows on their own layers)
    for r, (yy, n, seed, dt) in enumerate(((LANE_B + 4, 9, 3, 0.25), (LANE_F + 36, 8, 7, 0.55))):
        frames = [doc(C.galilee_crowd(760, yy, KA, 1, n=n, pose="run", width=1300 / KA, rows=1, seed=seed, phase=ph))
                  for ph in (0.0, 0.5)]
        t_c0 = t_run0 + dt
        sc.add(f"d_crowd{r}", frames, z=13.5 + 1.0 * r, seed=SEED_S + 500 + r,
               frame_at=lambda t, t_c0=t_c0: float(int(max(0.0, t - t_c0) / 0.14) % 2),
               motion=M.combine(lambda t, t_c0=t_c0: Tf(dx=620 * max(0.0, t - t_c0) - 1500,
                                                        dy=-sum(14 * KA * math.sin(math.pi * min(1.0, max(0.0, (t - b) / 0.22)))
                                                                for b in pao if b <= t <= b + 0.22)),
                                gate(t_c0, t_E1)))
    for b in pao:
        for j, xx in enumerate((900, 1500, 2100)):
            sc.add(f"d_dust{int(b * 100)}_{j}", dust_svg(xx, LANE_F + 50, 22), z=13.4, wc=0.3, seed=SEED_S + 600 + j,
                   motion=M.combine(puffm(b + 0.04 + 0.05 * j, (xx, LANE_F + 50), 0.6, -40, -18), gBD))
    sc.sfx("footsteps_run", t_run0, dur=t_E1 - t_run0 + 0.6, gain_db=-12, fade_out=0.5)
    sc.sfx("crowd", t_keshi, dur=t_E1 - t_keshi + 0.5, gain_db=-20, fade_in=0.6, fade_out=0.4)

    # ================================================================ HILLSIDE (E and F)
    add_hill(sc, gHill, g0)
    add_sun(sc, gHill)

    # ---- E1: the runners arrive (they pour in from the left and stop on the slope right of the path, panting and
    # pointing at the boat that is still out on the lake)
    t_dao = tm.at(3, "比船还先到了", 4)
    t_arr = snap(t_dao - 0.12)
    # the boat is still far out on the lake (small, mid-lake, left of where the crowd stops), gliding slowly to the shore
    sc.add("e_farboat", [doc(PR.far_boat(E1_BOAT[0], E1_BOAT[1], 0.13, -1, sail="full", crew=True, time=H_TIME))], z=Z_H + 1.6,
           seed=SEED_H + 60, wc=0.6,
           motion=M.combine(lambda t: Tf(dx=-140 * M.progress(t, t_E1, t_E2 + 0.4, lambda q: q),
                                         dy=6 * M.progress(t, t_E1, t_E2 + 0.4, lambda q: q) + 1.5 * math.sin(2 * math.pi * t / 3.1)),
                            gE1))
    back = [m for m in E_CROWD if m[3] == 0]
    front = [m for m in E_CROWD if m[3] == 1]
    clusters = [("B", back, 700, 0.0), ("Fa", front[:5], 760, 0.08), ("Fb", front[5:], 820, 0.16)]
    e_acts = []
    for ci, (nm, mem, travel, dt) in enumerate(clusters):
        hx0 = sum(m[2] for m in mem) / len(mem)
        y_ref, _ = hy_d(E_D_FRONT if mem[0][3] else E_D_BACK, hx0)
        a = Actor(f"e_{nm}", (hx0, y_ref), HS * 0.6, lambda k, mem=mem: e_cluster_markup(mem, "R", k),
                  Z_H + 5.0 + (0.2 if mem[0][3] else 0.0) + 0.01 * ci, SEED_H + 70 + ci, g0, gE)
        t0r = t_E1 + dt
        q = 0
        a.cut(0, ("run", 0))
        while t0r + q * 0.13 < t_arr:
            a.cut(t0r + q * 0.13, ("run", q % 2))
            q += 1
        a.moves.append(lambda t, tr=travel, t0r=t0r, t1r=t_arr: (-tr * (1 - M.progress(t, t0r - 0.45, t1r, lambda u: 1 - (1 - u) ** 2)), 0.0))
        a.loop(t_arr, [("arrive", qq) for qq in range(4)], 0.32, phase=0.3 * ci)
        a.dips.append((t_arr, 6))
        # E2: they stand facing Jesus, shuffling a little
        a.loop(t_E2, [("listen", qq) for qq in range(3)], 0.9 + 0.13 * ci, phase=0.4 * ci)
        e_acts.append(a)
    sc.sfx("footsteps_run", t_E1, dur=t_arr - t_E1 + 0.2, gain_db=-14, fade_in=0.05)
    sc.sfx("crowd", t_E1, dur=t_F - t_E1, gain_db=-22, fade_in=0.3, fade_out=0.8)
    for j, x_ in enumerate((1480, 1840, 2200)):
        y_, k_ = hy_d(E_D_FRONT, x_)
        px_, py_ = x_ + 50 * k_, y_ - 250 * k_
        for rep in range(2):
            tp = snap(t_arr + 0.1 + 0.55 * rep + 0.12 * j)
            sc.add(f"e_puff{j}_{rep}", puff_svg(px_, py_, 12), z=Z_H + 5.9, wc=0.3, seed=SEED_H + 80 + j,
                   motion=M.combine(puffm(tp, (px_, py_), 0.6, -26, -20), gE1))

    # ---- E2: the boat at the shore; Jesus steps off and walks down to the people
    t_xia = tm.at(4, "耶稣下了船", 2)
    t_kanjian = tm.at(4, "看见这么多人", 0)
    t_xin = tm.at(4, "心里好疼爱他们", 0)
    t_teng = tm.at(4, "心里好疼爱他们", 3)
    t_tamen = tm.at(4, "他们就像一群没有牧羊人的羊", 0)
    t_buzhi = tm.at(4, "不知道该往哪里去", 0)
    t_qu = tm.at(4, "不知道该往哪里去", 7)
    sc.add("e_boat_back", e_boat_part("back"), z=Z_H + 2.0, seed=SEED_H + 61, motion=gE2)
    crew = Actor("e_crew", E_BOAT, KB, e_crew_markup, Z_H + 2.1, SEED_H + 62, g0, gE2)
    crew.cut(0, ("stand", "happy"))
    crew.cut(snap(t_kanjian + 0.4), ("wave", "happy"), dip=3)
    crew.cut(snap(t_teng), ("stand", "awed"), dip=3)
    crew.extra.append(breathm(g0, 3.0, 0.008))
    crew.build(sc)
    # Jesus in the boat: two short steps to the bow, a crouch, a hop over the gunwale on '下' (a planted landing on the
    # sand by the bow on '船'), then he walks down the grass to the people. Boat part on a layer between the hull's back
    # and front (so the near hull hides his legs inside the boat); once he stands on the sand he hands over, in the same
    # pose, place and scale, to a layer in front of the slope for the walk.
    bx, by = E_BOAT
    jb_x = bx + 250 * KB / 0.475                  # where he stands in the boat
    jb_bow = bx + 285 * KB / 0.475                # by the bow after two short steps
    t_step = snap(t_xia)
    p_land = (bx + 420 * KB / 0.475, LY + 5)      # on the beach strip, clear of the slope's edge
    t_s1 = snap(max(t_E2 + 0.12, t_step - 0.6))
    t_s2 = snap(t_step - 0.34)
    t_hop = snap(t_step - 0.06)                   # the crouch's bottom; take-off just after
    t_h0, t_h1 = t_hop + 0.05, snap(t_hop + 0.5)  # airborne
    HOP_H = 120.0 * KB / 0.475

    def jb_markup(key):
        pose, expr = key[0], key[1]
        return jes(jb_x, by, KB, 1, pose=pose, expr=expr)

    def jb_ground(t):
        """(x, ground y, lift) of his feet."""
        if t < t_h0:
            x = jb_x + (jb_bow - jb_x) * (0.5 * M.progress(t, t_s1 - 0.05, t_s1 + 0.09, "sine") +
                                           0.5 * M.progress(t, t_s2 - 0.05, t_s2 + 0.09, "sine"))
            return x, by, 0.0
        u = M.progress(t, t_h0, t_h1, "linear")
        x = jb_bow + (p_land[0] - jb_bow) * (u * (1.35 - 0.35 * u))
        y = by + (p_land[1] - by) * u
        return x, y, HOP_H * 4 * u * (1 - u)

    def jb_motion(t):
        x, y, lift = jb_ground(t)
        k = hk(y) / KB
        land = 0.0
        if t_h1 <= t <= t_h1 + 0.26:
            land = math.sin(math.pi * (t - t_h1) / 0.26)
        return Tf(dx=x - jb_x, dy=y - by - lift + 5 * KB * land, sx=k, sy=k * (1 - 0.055 * land), px=jb_x, py=by)
    t_sw = snap(t_h1 + 0.3)                       # the hand-over to the land layer (both 'stand', same place)
    jb = Actor("e_jesus_boat", (jb_x, by), KB, jb_markup, Z_H + 2.2, SEED_H + 63, g0,
               lambda t: Tf(alpha=gE2(t).alpha * (1.0 if t < t_sw else 0.0)))
    jb.cut(0, ("walk_b", "warm"))
    jb.cut(t_s1, ("walk_a", "warm"))
    jb.cut(t_s2, ("walk_b", "warm"))
    jb.dips.append((t_hop, 9))
    jb.cut(t_h1, ("stand", "warm"))
    jb.extra.append(jb_motion)
    jb.extra.append(breathm(g0, 3.4, 0.008))
    jb.build(sc)
    sc.sfx("whoosh", t_h0, gain_db=-24)
    sc.add("e_boat_front", e_boat_part("front"), z=Z_H + 2.3, seed=SEED_H + 64, motion=gE2)
    # on land: walks down the grass to the people (growing as he comes nearer)
    y_stop, k_stop = hy_d(0.66, E_JESUS_STOP)
    p_stop = (E_JESUS_STOP, y_stop)
    n_w = 6
    w_per = 0.24
    t_w0 = snap(t_h1 + 0.36)
    t_w1 = snap(t_w0 + n_w * w_per)

    def jesus_e_markup(key):
        pose, expr = key[0], key[1]
        return shadow(*p_stop, k_stop, 110, 0.16) + jes(*p_stop, k_stop, 1, pose=pose, expr=expr)
    je = Actor("e_jesus", p_stop, k_stop, jesus_e_markup, Z_H + 5.5, SEED_H + 65, g0,
               lambda t: Tf(alpha=gE2(t).alpha * (1.0 if t >= t_sw else 0.0)))
    je.cut(0, ("stand", "warm"))
    for q in range(n_w):
        je.cut(t_w0 + q * w_per, ("walk_a" if q % 2 == 0 else "walk_b", "warm"))
    t_lk = snap(t_xin - 0.05)
    if t_lk - t_w1 >= 0.5:
        je.cut(t_w1, ("stand", "warm"), dip=3)
    else:                                         # no time for a stand: from the last stride into the kind look
        t_lk = t_w1
    je.cut(t_lk, ("look_kind", "kind"), dip=3)
    je.cut(snap(t_tamen + 0.2), ("look_kind", "warm"), dip=2)

    def je_pos(t):
        # a stride per cut from the landing spot to the stop
        u = 0.0
        for q in range(n_w):
            u += M.progress(t, t_w0 + q * w_per - 0.05, t_w0 + q * w_per + 0.09, "sine") / n_w
        return p_land[0] + (p_stop[0] - p_land[0]) * u, p_land[1] + (p_stop[1] - p_land[1]) * u

    def je_motion(t):
        x, y = je_pos(t)
        k = hk(y) / k_stop
        return Tf(dx=x - p_stop[0], dy=y - p_stop[1], sx=k, sy=k, px=p_stop[0], py=p_stop[1])
    je.extra.append(je_motion)
    je.extra.append(breathm(g0, 3.4, 0.008))
    je.blinks([t_w1 + 0.6, t_teng + 1.1, t_buzhi + 0.3], {("stand", "warm"): ("stand", blink("warm")),
                                                          ("look_kind", "warm"): ("look_kind", blink("warm"))})
    je.build(sc)
    sc.sfx("thud", t_h1, gain_db=-22)
    sc.sfx("splash_small", t_h0, gain_db=-22)
    sc.sfx("footsteps", t_w0, dur=n_w * w_per, gain_db=-20)
    # the soft warm light on his face (a wide soft glow over his face and chest, never a halo)
    head_x, head_y = p_stop[0] + 10 * k_stop, p_stop[1] - 270 * k_stop
    sc.add("e_glow", warm_glow_svg(head_x, head_y + 50 * k_stop, 240 * k_stop, 280 * k_stop, "#ffdc90", 0.75, "je"), z=Z_H + 5.6,
           wc=0.0, seed=SEED_H + 66, blend="screen",
           motion=M.combine(lambda t: Tf(alpha=env(t, t_teng - 0.35, t_buzhi + 0.7, 0.8, 1.0) *
                                         (0.85 + 0.15 * math.sin(2 * math.pi * t / 2.1))), gE2))
    sc.sfx("chime", t_teng - 0.2, gain_db=-17)
    for a in e_acts:
        a.build(sc)
    # the thought bubble of sheep without a shepherd (rising from his head)
    t_bub = snap(t_tamen + 0.15)
    t_bub_out = snap(min(t_F - 0.25, t_qu + 0.55))
    bub_piv = (E_BUB[0] - 160, E_BUB[1] + 160)
    bub_m = popm(t_bub, bub_piv, 0.4, t_out=t_bub_out, out_dur=0.3, wob=False)
    tx0, ty0 = head_x + 60 * k_stop, head_y - 90 * k_stop
    tx1, ty1 = E_BUB[0] - E_BUB_R[0] * 0.7, E_BUB[1] + E_BUB_R[1] * 0.75
    for k_, (u_, r_) in enumerate(((0.15, 11), (0.4, 17), (0.68, 25))):
        x_, y_ = tx0 + (tx1 - tx0) * u_, ty0 + (ty1 - ty0) * u_
        sc.add(f"e_trail{k_}", doc(S.g(PR._circ(x_, y_, r_, "#fffaf0", 3.4), filter="wobble-fine")), z=Z_H + 6.0, wc=0.3,
               seed=SEED_H + 90 + k_, motion=M.combine(popm(snap(t_bub - 0.3 + 0.1 * k_), (x_, y_), 0.25, t_out=t_bub_out, out_dur=0.25,
                                                            wob=False), gE2))
    sc.add("e_bubble", sheep_bubble_frame(*E_BUB, *E_BUB_R), z=Z_H + 6.1, wc=0.5, seed=SEED_H + 95, motion=M.combine(bub_m, gE2))
    n_steps = 9
    t_s0 = snap(t_bub + 0.35)
    s_per = max(0.2, min(0.32, (t_buzhi - 0.1 - t_s0) / n_steps))
    frames = [sheep_frame(i) for i in range(n_steps)] + [sheep_frame(0, 0), sheep_frame(0, 1)]

    def sheep_fa(t):
        if t < t_buzhi - 0.05:
            return float(min(n_steps - 1, max(0, int((t - t_s0) / s_per))))
        return float(n_steps + int((t - t_buzhi + 0.05) / 0.45) % 2)
    sc.add("e_sheep", frames, z=Z_H + 6.2, wc=0.5, seed=SEED_H + 96, frame_at=sheep_fa, motion=M.combine(bub_m, gE2))
    for j, (sx_, sy_) in enumerate(((E_BUB[0] - 120, E_BUB[1] + 10), (E_BUB[0] + 150, E_BUB[1] + 30))):
        sc.add(f"e_q{j}", mark_svg(sx_, sy_, "?", 60, "#6a8ac8"), z=Z_H + 6.3, wc=0.0, seed=SEED_H + 97 + j,
               motion=M.combine(popm(snap(t_buzhi + 0.15 + 0.3 * j), (sx_, sy_ - 20), 0.25, t_out=t_bub_out, out_dur=0.25), gE2))
    sc.sfx("pop", t_bub, gain_db=-12)
    sc.sfx("sheep", t_buzhi + 0.2, gain_db=-15)
    sc.sfx("sheep", t_buzhi + 1.0, gain_db=-19, pan=0.3)

    # ================================================================ F: teaching and healing
    add_groups(sc, gF, g0)
    t_jiang = tm.at(5, "耶稣就给大家讲上帝的事", 6)
    t_sheng = tm.at(5, "还把生病的人", 2)
    t_zhi = tm.at(5, "都治好了", 1)
    acts = add_f_people(sc, gF, g0, Z_H + 6.5)
    ek = f_end_keys()
    for j in range(len(FAMILY)):
        acts[f"fam{j}"].cut(0, ("sit_listen" if j % 2 == 0 else "sit", "kind"))
    acts["fam2"].cut(snap(t_zhi + 0.35), ("sit_laugh", "delighted"), dip=3)
    acts["lame"].cut(0, ("sick_sit", "tired"))
    acts["lame"].moves.append(lambda t: (SICK_WIDE_DX * JK if t < t_FM else 0.0, 0.0))
    acts["mother"].moves.append(lambda t: (SICK_WIDE_DX * 0.8 if t < t_FM else 0.0, 0.0))
    t_heal = snap(t_zhi - 0.04)
    acts["lame"].cut(t_heal, ek["lame"], dip=7)
    acts["lame"].extra.append(hopm(t_heal + 0.02, JK, 26, 0.34))
    acts["mother"].cut(0, ("sick_sit", "worried"))
    t_heal2 = snap(t_zhi + 0.16)
    acts["mother"].cut(t_heal2, ek["mother"], dip=5)
    jf = acts["jesus"]
    jf.cut(0, ("sit_teach", "teach"))
    jf.cut(snap(t_jiang - 0.05), ("teach", "smile"), dip=2)
    jf.cut(t_FM, ("heal", "kind"))
    jf.cut(snap(t_zhi + 0.3), ek["jesus"], dip=3)
    for nm, v, x, y in DISC_F + DISC_FB:
        acts[nm].cut(0, ("stand", "happy"))
        acts[nm].cut(snap(t_zhi + 0.25 + 0.04 * v), ek[nm], dip=3)
    for nm, a in acts.items():
        a.build(sc)
    # the healing light
    for (gx, gy, r, key) in ((LAME[0] + 40 * JK, LAME[1] - 150 * JK, 230, "lm"), (MOTHER[0] + 60, MOTHER[1] - 110, 210, "mo")):
        sc.add(f"f_glow_{key}", warm_glow_svg(gx, gy, r, r * 0.9, "#fff2c0", 0.8, key), z=Z_H + 6.49, wc=0.0, seed=SEED_H + 300,
               blend="screen", motion=M.combine(lambda t: Tf(alpha=env(t, t_zhi - 0.35, min(T - 1.05, t_zhi + 2.0), 0.35, 0.9)), gF))
    sc.fx.append(FX.sparkles((LAME[0] - 260, LAME[1] - 380, LAME[0] + 120, LAME[1] - 60), count=16, t0=t_zhi - 0.1,
                             t1=min(T - 1.05, t_zhi + 1.8),
                             size=(8, 16), period=1.2, drift=-20, seed=31))
    sc.sfx("sparkle", t_zhi - 0.05, gain_db=-11)
    sc.sfx("chime", t_zhi - 0.25, gain_db=-16)
    sc.sfx("cheer", t_zhi + 0.4, dur=1.6, gain_db=-24, fade_in=0.3, fade_out=0.8)
    sc.sfx("crowd", t_F, dur=T - t_F + 0.4, gain_db=-28, fade_in=0.2, fade_out=1.0)
    sc.sfx("birds", t_E1, dur=T - t_E1 + 0.4, gain_db=-30, fade_in=0.4, fade_out=1.0)

    # ================================================================ camera
    camA = cam_keys([(0, Cam(1250, 905, 1900)), (t_ysay, Cam(1290, 902, 1880)), (t_B, Cam(1300, 900, 1860))], "sine")
    camB = cam_keys([(t_B, Cam(1450, 890, 2000)), (t_dajia, Cam(1430, 895, 2000)), (t_E1, Cam(1560, 898, 2000))], ["sine", "linear"])
    camE1 = cam_keys([(t_E1, Cam(1590, 830, 2000)), (t_E2, Cam(1570, 836, 1960))], "sine")
    camE2 = cam_keys([(t_E2, Cam(1120, 720, 1720)), (t_w1, Cam(1230, 750, 1640)), (t_teng + 0.6, Cam(1300, 770, 1480)),
                      (t_tamen, Cam(1310, 760, 1500)), (t_bub + 0.4, Cam(1440, 700, 1820)), (t_F, Cam(1450, 702, 1840))],
                     ["sine", "sine", "sine", "sine", "linear"])
    camF = cam_keys([(t_F, Cam(1300, 731, 2598)), (t_FM, Cam(1220, 770, 2400))], "sine")
    camFM = cam_keys([(t_FM, Cam(960, 905, 1740)), (T - 1.0, CAM_F_END), (T, CAM_F_END)], ["sine", "linear"])

    def cam(t):
        if t < t_B:
            return camA(t)
        if t < t_E1:
            return camB(t)
        if t < t_E2:
            return camE1(t)
        if t < t_F:
            return camE2(t)
        if t < t_FM:
            return camF(t)
        return camFM(t)
    sc.camera = cam

    # ================================================================ ambience
    sc.sfx("waves_calm", 0, dur=t_E1 + 0.4, gain_db=-24, fade_in=0.8, fade_out=0.4)
    sc.sfx("waves_calm", t_E1, dur=T - t_E1 + 0.4, gain_db=-28, fade_in=0.3, fade_out=1.0)
    sc.sfx("crowd", 0, dur=t_B + 0.3, gain_db=-21, fade_in=0.8, fade_out=0.4)
    sc.sfx("birds", 0, dur=t_E1, gain_db=-29, fade_in=0.8, fade_out=0.4)
    return sc
