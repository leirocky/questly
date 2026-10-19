"""Scene 6 — Bethlehem: David the shepherd boy; Jesse sends him to his brothers (1 Samuel 17:12-20).

One wide 3300 x 1300 stage, no cuts: on the left Jesse's small stone house (flat roof, ladder, clay oven, jars) under
an olive tree, a dry-stone sheepfold wall, then the green pasture with the flock; behind them the rolling hills of
Bethlehem (little village, olive trees) and, very far away on the right, the tiny tents and blue banners of Saul's
army on a hazy ridge, with the path winding toward them.

  line 0  '在伯利恒的山坡上，有一个放羊的男孩，'  wide pastoral page; David with his staff among grazing sheep; the
          camera eases in.        '名叫大卫。'  he gives a happy hop; a lamb bleats.
  line 1  '大卫是家里最小的孩子。'  a thought bubble rises from David's head (three little circles, then the
          bubble): a picture-book family line-up - Eliab, two more brothers and little David, the smallest (a heart
          pops over him).
          '他的三个哥哥，'  the three brothers bounce one by one (counting 1, 2, 3, pop).
          '都在扫罗王的军队里。'  little David puffs out of the bubble and an army tent with a blue banner pops up
          behind the brothers; the far camp on the ridge sparkles; the bubble then pops away.
  line 2  '有一天，爸爸耶西对大卫说：'  the camera glides left; Jesse steps out of his door and calls (sound arcs);
          David turns (he plants his staff in the pasture) and walks over to his father (planted-foot strides).
  line 3  '大卫，你带上这些饼和奶酪，'  Jesse holds out the basket of bread and cheese; David hops for joy and takes
          it (cut on a shared squash).   '去看看你的哥哥们，看他们好不好。'  Jesse talks and nods; David nods.
  gap     night falls for a moment (deep blue wash, stars), then dawn: the sky turns pink-gold, the sun rises
          behind the house, a rooster crows.
  line 4  '大卫一大早就起来，'  David stands ready with the basket; a helper shepherd walks in from the right.
          '把羊交给别人看管，'  the helper pulls David's staff out of the ground and nods; a sheep bleats.
          '出发了。'  David sets off to the right along the path (planted-foot walk), the camera follows; the sheep
          and the helper watch him go.

Pose changes are hard cuts hidden in squashes (dips / hops); walks use planted-foot step_walk; the night / dawn is
a lighting crossfade. All times derive from the narration chunks.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import (arcs_markup, cuts, dip, happy_hop, hop, nod, puff_markup, puff_motion, snap,
                                 step_walk)
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3300, 1300
INK = P["ink"]
GY = 1130                 # ground line for every figure in the shot
SC = 1.1                  # figure scale (David ~277 px, Jesse ~360 px)
HOUSE = (330, 830)        # house wall x-range
DOOR_X = 600
JX = 800                  # Jesse's talking spot
DX_HOME = 1010            # David's spot in front of Jesse
DX_FIELD = 2110           # David in the pasture
WALK_P = 0.27
DWALK_P = 0.25         # David's quicker strides
PUNCT = "，。；：？！、,.;:?!"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ shared helpers (also used by s07/s14)


def when(ctx, phrase, line=None):
    """Start time of ``phrase``: its chunk start, or its character position inside the chunk."""
    lines = [ctx.lines[line]] if line is not None else ctx.lines
    for ln in lines:
        for ch in ln.chunks:
            if phrase in ch.text:
                k = ch.text.index(phrase)
                if k == 0:
                    return ch.start
                body = ch.text.rstrip(PUNCT)

                def w(s):
                    return sum(0.5 if c in PUNCT else 1.0 for c in s)
                return ch.start + (ch.end - ch.start) * w(ch.text[:k]) / max(1.0, w(body))
    raise KeyError(phrase)


def with_blinks(entries, blink_of, times, dur=0.13, guard=0.35):
    """Add blinks (hard cuts to an eyes-closed copy of the held drawing) at ``times`` unless a cut is near."""
    entries = sorted(entries, key=lambda e: e[0])
    out = list(entries)
    for tb in times:
        tb = snap(tb)
        if any(abs(tb - tk) < guard or abs(tb + dur - tk) < guard for tk, _ in entries):
            continue
        cur = None
        for tk, i in entries:
            if tk <= tb:
                cur = i
        if cur is None or cur not in blink_of:
            continue
        out += [(tb, blink_of[cur]), (snap(tb + dur), cur)]
    return sorted(out, key=lambda e: e[0])


def blink_expr(e):
    """Register (once) and return the name of an eyes-closed copy of expression ``e``."""
    name = f"dv6_blink_{e}"
    C.EXPRS.setdefault(name, dict(C.EXPRS[e], eyes="closed"))
    return name


def make_cam(sw, sh):
    def clamp(c, margin=4):
        h = c.w * 9 / 16
        x = min(max(c.x, c.w / 2 + margin), sw - c.w / 2 - margin)
        y = min(max(c.y, h / 2 + margin), sh - h / 2 - margin)
        return Cam(x, y, c.w)

    def path(keys):
        """[(t, Cam[, curve])]: eased moves between key cameras (bottom edge interpolated, clamped to the stage)."""
        ks = [(k[0], clamp(k[1]), k[2] if len(k) > 2 else "sine") for k in sorted(keys, key=lambda k: k[0])]

        def bottom(c):
            return c.y + c.w * 9 / 32

        def cam(t):
            if t <= ks[0][0]:
                return ks[0][1]
            if t >= ks[-1][0]:
                return ks[-1][1]
            for (t0, a, cv), (t1, b, _) in zip(ks, ks[1:]):
                if t0 <= t <= t1:
                    u = M.progress(t, t0, t1, cv)
                    w = M.lerp(a.w, b.w, u)
                    yb = M.lerp(bottom(a), bottom(b), u)
                    return clamp(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
            return ks[-1][1]
        return cam
    return clamp, path


def cam_at(x, w, bottom):
    """Camera centred on x whose viewport bottom edge is at ``bottom``."""
    return Cam(x, bottom - w * 9 / 32, w)


def actor(sc, name, z, frames, anchor, s, base, walks=(), bumps=(), breathe=(0.01, 3.0, 0.0), extra=None,
          start_off=0.0, docf=None, period=WALK_P):
    """A character layer (see Daniel s02): ``frames`` are drawings at ``anchor``; ``base`` [(t, idx)] hard cuts;
    ``walks`` [(t0, n, step, pair)] planted-foot walks (``pair`` = index of that walk's walk_a frame);
    ``start_off`` shifts the figure at t=0. Returns dx(t)."""
    docf = docf or doc
    ws = [step_walk(w[0], w[1], w[2], period, s) for w in walks]
    pairs = [w[3] for w in walks]
    fb = cuts(base)

    def fa(t):
        for w, pb in zip(ws, pairs):
            v = w[0](t)
            if v is not None:
                return v + pb
        return fb(t)

    def dx(t):
        return start_off + sum(w[1](t) for w in ws)

    def dy(t):
        return sum(w[2](t) for w in ws)
    mot = [M.with_pivot(lambda t: Tf(dx=dx(t), dy=dy(t)), anchor)] + list(bumps)
    if breathe:
        mot.append(M.breathe(breathe[0], breathe[1], pivot=anchor, phase=breathe[2]))
    if extra:
        mot.append(extra)
    sc.add(name, [docf(f) for f in frames], z=z, frame_at=fa, motion=M.combine(*mot))
    return dx


def heart_markup(x, y, r, fill="#e98a8a"):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.2)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.2)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} "
         f"{f1(x)},{f1(y + r * 0.9)} Z")
    return S.g(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{max(2.5, r * 0.15):.1f}" '
               f'stroke-linejoin="round"/><ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.3)}" '
               f'rx="{f1(r * 0.18)}" ry="{f1(r * 0.12)}" fill="#fbd0c4"/>', filter="wobble-fine")


def scallop_path(cx, cy, rx, ry, n=16, bulge=0.55, rot=0.0):
    """A thought-bubble outline: an ellipse made of outward bumps."""
    pts = [(cx + rx * math.cos(2 * math.pi * i / n + rot), cy + ry * math.sin(2 * math.pi * i / n + rot))
           for i in range(n)]
    d = f"M{f1(pts[0][0])},{f1(pts[0][1])}"
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ox, oy = mx - cx, my - cy
        ln = math.hypot(ox, oy) or 1
        ch = math.hypot(b[0] - a[0], b[1] - a[1])
        qx, qy = mx + ox / ln * ch * bulge, my + oy / ln * ch * bulge
        d += f" Q{f1(qx)},{f1(qy)} {f1(b[0])},{f1(b[1])}"
    return d + " Z"


def tuft_row(items, phase):
    out = ""
    for x, y, s, v in items:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.45 * math.sin(phase + x * 0.013))
    return out


def sheep_layer(sc, name, z, x, y, s, facing, variant=0, lamb=False, seed=0, bleats=(), T=30.0, docf=None,
                extra_cuts=(), frames_extra=()):
    """A flock sheep that grazes / looks up now and then (cuts hidden in tiny squashes), breathes, and bleats at
    ``bleats`` times. Frames: 0 stand, 1 graze, 2 bleat (+ frames_extra)."""
    docf = docf or doc
    fr = [docf(C.ground_shadow(x, y, s, 190 if not lamb else 130, 0.18) +
               PR.sheep(x, y, s, facing, variant=variant, pose=p, lamb=lamb)) for p in ("stand", "graze", "bleat")]
    fr += [docf(f) for f in frames_extra]
    rng = random.Random(seed)
    entries = [(0, rng.choice((0, 1)))]
    t = rng.uniform(1.5, 3.5)
    while t < T:
        if not any(abs(t - b) < 1.6 for b in bleats):
            entries.append((snap(t), 1 - entries[-1][1] if entries[-1][1] in (0, 1) else 0))
        t += rng.uniform(2.4, 4.6)
    for b in bleats:
        prev = [e for e in entries if e[0] <= b]
        back = prev[-1][1] if prev else 0
        entries += [(snap(b), 2), (snap(b + 0.9), back if back in (0, 1) else 0)]
    entries += list(extra_cuts)
    entries.sort(key=lambda e: e[0])
    bumps = [hop(tk, [(-0.06, {"sy": 1, "dy": 0}), (0.0, {"sy": 0.96, "dy": 2 * s}), (0.16, {"sy": 1.0, "dy": 0})],
                 (x, y)) for tk, _ in entries[1:]]
    sc.add(name, fr, z=z, frame_at=cuts(entries),
           motion=M.combine(M.breathe(0.012, 2.6 + rng.uniform(0, 0.8), pivot=(x, y), phase=rng.uniform(0, 1)),
                            *bumps))


# ============================================================================ drawings


def sky_day_svg():
    defs = S.lin_grad("s6sky", [(0, "#8ec6df"), (0.55, "#bfe2ea"), (1, "#f2ead0")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s6sky)"/>', defs)


def sky_dawn_svg():
    defs = S.lin_grad("s6dawn", [(0, "#b9a6d3"), (0.35, "#f1b8b0"), (0.7, "#f8cf98"), (1, "#fbe6bd")])
    defs += S.rad_grad("s6sunglow", [(0, "#fff1c8", 0.95), (0.35, "#fbd38e", 0.5), (1, "#f8c58e", 0)])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#s6dawn)"/>'
               f'<circle cx="420" cy="640" r="620" fill="url(#s6sunglow)"/>', defs)


def sun_svg():
    x, y = 420, 600
    out = (f'<path d="{S.rays(x, y, 95, 210, 12, 9)}" fill="#fbd46b" opacity="0.55"/>'
           f'<circle cx="{x}" cy="{y}" r="78" fill="#fbcf6a" stroke="#e9925a" stroke-width="5"/>'
           f'<circle cx="{x - 22}" cy="{y - 24}" r="20" fill="#fde7a8"/>')
    return doc(S.g(out, filter="wobble"))


def stars_svg():
    rng = random.Random(6)
    out = ""
    for _ in range(70):
        x, y = rng.uniform(0, SW), rng.uniform(20, 820)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(2.5, 5))}" fill="#fff6d8"/>'
    out += (f'<path d="M2300,170 a46,46 0 1,0 40,70 a36,36 0 1,1 -40,-70 Z" fill="#fff0c4" stroke="{P["ink_soft"]}" '
            f'stroke-width="3"/>')
    return doc(out)


def clouds_svg():
    out = ""
    for cx, cy, w, h, sd in ((420, 210, 360, 84, 1), (1250, 140, 300, 70, 2), (1900, 260, 420, 92, 3),
                             (2700, 170, 340, 76, 4), (3200, 300, 260, 60, 5), (-100, 330, 280, 60, 6)):
        out += S.cloud(cx, cy, w, h, fill="#fbf4e6", seed=sd, sw=3, shade_fill="#dbe5ea")
    return doc(S.g(out, filter="wobble"))


def far_svg():
    """Hazy far ridges; on the right the tiny camp of Saul's army; the path winding up toward it."""
    out = ""
    out += S.path(S.hill(-60, SW + 60, 760, 170, seed=3, bumps=5), "#b9cfc6", sw=3)
    out += S.path(S.hill(1700, SW + 80, 700, 120, seed=8, bumps=3), "#aac4b8", sw=3)
    # far camp on the right ridge: small striped tents with blue banners
    for x, y, s in ((3020, 646, 0.12), (3100, 640, 0.13), (3190, 648, 0.12), (3270, 656, 0.11)):
        out += PR.tent(x, y, s, 1, side="israel")
    out += S.path(S.hill(-60, SW + 60, 860, 130, seed=12, bumps=4), "#a3c49a", sw=3.5)
    return doc(S.g(out, filter="wobble"))


def mid_svg():
    """Rolling green hills of Bethlehem: a little village, olive groves, terraces, a few far sheep."""
    out = ""
    defs = S.lin_grad("s6mid", [(0, "#a9cb78"), (1, "#86ad5a")])
    out += S.path(S.hill(-80, 1900, 960, 260, seed=21, bumps=2), "url(#s6mid)", sw=4)
    out += S.path(S.hill(1300, SW + 80, 980, 200, seed=24, bumps=3), "url(#s6mid)", sw=4)
    # terraces
    for k, (x0, x1, y) in enumerate(((150, 900, 840), (300, 1250, 900), (1700, 2600, 900), (2100, 3000, 940))):
        out += (f'<path d="M{x0},{y} Q{(x0 + x1) / 2},{y - 26} {x1},{y}" fill="none" stroke="#6f9446" '
                f'stroke-width="4" stroke-dasharray="18 10" opacity="0.7"/>')
    # village of Bethlehem on the left hill
    for x, y, s, v, f in ((360, 790, 0.22, 0, 1), (520, 770, 0.25, 2, -1), (690, 772, 0.2, 3, 1),
                          (230, 805, 0.2, 1, 1)):
        out += PR.house(x, y, s, variant=v, facing=f)
    for x, y, s, sd in ((860, 830, 0.32, 1), (980, 860, 0.36, 2), (1560, 860, 0.3, 3), (2050, 880, 0.34, 4),
                        (2480, 860, 0.3, 5), (120, 840, 0.3, 6)):
        out += PR.olive_tree(x, y, s, seed=sd)
    # far sheep dots on the slope
    for x, y in ((1750, 905), (1820, 915), (2280, 925), (2340, 918), (1180, 925)):
        out += PR.sheep(x, y, 0.28, 1 if x % 2 else -1, variant=x % 4, pose="graze")
    return doc(S.g(out, filter="wobble"), defs)


def stone_texture(x0, x1, y0, y1, seed, col):
    rng = random.Random(seed)
    out = ""
    y = y0 + 16
    row = 0
    while y < y1 - 10:
        x = x0 + (row % 2) * 26 + 8
        while x < x1 - 30:
            w = rng.uniform(40, 66)
            h = rng.uniform(26, 34)
            c = S.mix(col, S.shade(col, -0.2 if rng.random() < 0.5 else 0.12), rng.uniform(0.2, 0.7))
            out += (f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(min(w, x1 - 10 - x))}" height="{f1(h)}" rx="11" '
                    f'fill="{c}" stroke="{S.shade(col, -0.35)}" stroke-width="2.5"/>')
            x += w + rng.uniform(4, 9)
        y += 36
        row += 1
    return out


def house_markup():
    """Jesse's small stone house with a flat roof, a ladder, a clay oven and jars."""
    x0, x1 = HOUSE
    top = GY - 470
    col = "#d9c39b"
    out = ""
    # olive tree behind the house
    out += PR.olive_tree(250, GY - 30, 0.95, seed=11)
    out += S.path(f"M{x0},{top} L{x1},{top} L{x1},{GY + 4} L{x0},{GY + 4} Z", col, sw=5)
    out += f'<clipPath id="s6wall"><rect x="{x0}" y="{top}" width="{x1 - x0}" height="{GY - top}"/></clipPath>'
    out += f'<g clip-path="url(#s6wall)">{stone_texture(x0, x1, top, GY, 4, col)}</g>'
    out += S.path(f"M{x0},{top} L{x1},{top} L{x1},{GY + 4} L{x0},{GY + 4} Z", "none", sw=5)
    # roof slab with beam ends and a parapet
    out += S.path(f"M{x0 - 26},{top - 30} L{x1 + 26},{top - 30} L{x1 + 26},{top + 6} L{x0 - 26},{top + 6} Z",
                  "#b89067", sw=4.5)
    for x in range(x0 - 4, x1 + 10, 62):
        out += f'<circle cx="{x}" cy="{top - 12}" r="9" fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="2.5"/>'
    out += S.path(f"M{x0 - 20},{top - 30} L{x0 - 20},{top - 66} L{x1 + 20},{top - 66} L{x1 + 20},{top - 30}",
                  "#cdb48c", sw=4)
    out += PR.jar(x1 - 40, top - 108, 0.5) + PR.bush(x0 + 70, top - 66, 0.35, variant=1)
    # door (round-topped, dark inside) with a wooden frame
    dw, dh = 150, 400
    dl = DOOR_X - dw / 2
    out += (f'<path d="M{dl - 14},{GY + 2} L{dl - 14},{GY - dh} Q{DOOR_X},{GY - dh - 90} {dl + dw + 14},{GY - dh} '
            f'L{dl + dw + 14},{GY + 2} Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="4.5"/>'
            f'<path d="M{dl},{GY + 2} L{dl},{GY - dh + 6} Q{DOOR_X},{GY - dh - 72} {dl + dw},{GY - dh + 6} '
            f'L{dl + dw},{GY + 2} Z" fill="#5c4033" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{dl + 8},{GY - 30} L{dl + dw - 8},{GY - 30}" stroke="#4a3328" stroke-width="5"/>')
    # small window with a wooden shutter
    wx, wy = x0 + 90, GY - 330
    out += (f'<rect x="{wx}" y="{wy}" width="86" height="80" rx="10" fill="#5c4033" stroke="{INK}" '
            f'stroke-width="4.5"/><rect x="{wx - 38}" y="{wy - 4}" width="40" height="88" rx="6" fill="{P["wood_light"]}"'
            f' stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{wx - 10},{wy + 84} L{wx + 96},{wy + 84}" stroke="{INK}" stroke-width="5"/>')
    # flower pot on the sill
    out += (f'<path d="M{wx + 24},{wy + 80} L{wx + 62},{wy + 80} L{wx + 58},{wy + 52} L{wx + 28},{wy + 52} Z" '
            f'fill="{P["terracotta"]}" stroke="{INK}" stroke-width="3"/>')
    for k in range(3):
        out += f'<circle cx="{wx + 30 + 13 * k}" cy="{wy + 40 - 6 * (k % 2)}" r="10" fill="#f0998a" stroke="{INK}" stroke-width="2.5"/>'
    # a low wooden bench against the wall
    bx = x1 - 150
    out += (f'<rect x="{bx - 70}" y="{GY - 78}" width="150" height="20" rx="6" fill="{P["wood_light"]}" stroke="{INK}" '
            f'stroke-width="3.5"/><path d="M{bx - 55},{GY - 58} L{bx - 55},{GY + 2} M{bx + 65},{GY - 58} L{bx + 65},{GY + 2}" '
            f'stroke="{P["wood_dark"]}" stroke-width="9" stroke-linecap="round"/>')
    # clay oven and jars by the wall
    ox = x0 - 10
    out += (f'<path d="M{ox - 70},{GY + 4} Q{ox - 70},{GY - 120} {ox},{GY - 124} Q{ox + 70},{GY - 120} {ox + 70},{GY + 4} '
            f'Z" fill="#c98f62" stroke="{INK}" stroke-width="4.5"/>'
            f'<path d="M{ox - 24},{GY + 2} Q{ox - 24},{GY - 50} {ox},{GY - 52} Q{ox + 24},{GY - 50} {ox + 24},{GY + 2} Z" '
            f'fill="#5c4033" stroke="{INK}" stroke-width="3.5"/>')
    out += PR.jar(x1 + 30, GY - 70, 0.75) + PR.jar(x1 - 30, GY - 56, 0.6, color="#b77a52")
    return out


def ground_svg():
    """Near meadow, the sheepfold wall, the sandy path and the house."""
    out = ""
    defs = S.lin_grad("s6gr", [(0, "#9cc062"), (0.5, "#8db456"), (1, "#7ea54c")])
    defs += S.lin_grad("s6path", [(0, "#ecd5a3"), (1, "#dfc08a")])
    out += S.path(S.wave_band(1010, 14, 900, 0.6, x0=-60, x1=SW + 60, bottom=SH + 60, seed=2), "url(#s6gr)", sw=4)
    # dry-stone sheepfold wall (behind the path)
    rng = random.Random(9)
    wall = ""
    for x in range(1060, 1520, 46):
        for row in range(3):
            yy = 1068 - row * 30 + rng.uniform(-3, 3)
            xx = x + (row % 2) * 20 + rng.uniform(-4, 4)
            c = S.mix("#d6c6a8", "#b9a685", rng.uniform(0, 1))
            wall += (f'<ellipse cx="{f1(xx)}" cy="{f1(yy)}" rx="{f1(rng.uniform(22, 28))}" ry="{f1(rng.uniform(14, 18))}" '
                     f'fill="{c}" stroke="{INK}" stroke-width="3"/>')
    out += wall
    # sandy path along the front, toward the right
    out += (f'<path d="M-60,1120 C400,1100 800,1150 1300,1132 C1800,1114 2300,1150 2700,1100 C2900,1075 3100,1040 '
            f'{SW + 60},1020 L{SW + 60},1090 C3100,1120 2900,1170 2700,1185 C2300,1220 1800,1190 1300,1205 '
            f'C800,1222 400,1182 -60,1196 Z" fill="url(#s6path)" stroke="{INK}" stroke-width="3.5" opacity="0.95"/>')
    for _ in range(40):
        x = rng.uniform(0, SW)
        y = rng.uniform(1135, 1185)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(6, 13))}" ry="{f1(rng.uniform(3, 6))}" '
                f'fill="#c9a874" opacity="0.8"/>')
    # meadow flowers
    for _ in range(60):
        x = rng.uniform(900, SW)
        y = rng.uniform(1030, 1090) if rng.random() < 0.6 else rng.uniform(1215, 1290)
        c = rng.choice(("#f6e27a", "#fff3d6", "#f0998a", "#c9a7e0"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(rng.uniform(5, 8))}" fill="{c}" stroke="{INK}" stroke-width="2"/>'
    out += house_markup()
    out += PR.bush(2950, 1075, 0.55, variant=1) + PR.bush(1580, 1060, 0.4, variant=0)
    out += PR.olive_tree(2850, 1050, 0.75, seed=7)
    return doc(S.g(out, filter="wobble"), defs)


FG_TUFTS = [(40, 1300, 1.3, 2), (210, 1290, 1.0, 0), (1140, 1300, 1.1, 0), (1420, 1295, 0.9, 2), (2120, 1300, 1.2, 0),
            (2380, 1290, 1.0, 2), (2600, 1300, 1.1, 1), (3000, 1295, 1.2, 2), (3220, 1300, 1.0, 0),
            (1760, 1300, 0.9, 0), (720, 1300, 1.0, 2)]


def fg_svg(k):
    return doc(tuft_row(FG_TUFTS, k * 2.1))


# ---------------------------------------------------------------- the thought bubble (line 1)
BUB = (2650, 480, 360, 240)     # cx, cy, rx, ry
BUB_FLOOR = 620                 # the little figures' ground inside the bubble
BS = 0.5                       # their scale
MINI_X = (2440, 2570, 2690, 2840)


def bubble_svg():
    cx, cy, rx, ry = BUB
    defs = S.lin_grad("s6bub", [(0, "#d8eef2"), (0.75, "#f6f0dc"), (1, "#f6f0dc")])
    body = (f'<path d="{scallop_path(cx, cy, rx, ry, 18, 0.45)}" fill="#fffaf0" stroke="{INK}" stroke-width="5"/>'
            f'<clipPath id="s6bclip"><ellipse cx="{cx}" cy="{cy}" rx="{rx - 12}" ry="{ry - 12}"/></clipPath>'
            f'<g clip-path="url(#s6bclip)"><rect x="{cx - rx}" y="{cy - ry}" width="{2 * rx}" height="{2 * ry}" '
            f'fill="url(#s6bub)"/><path d="{S.hill(cx - rx, cx + rx, BUB_FLOOR + 6, 30, seed=2, bottom=cy + ry, bumps=2)}"'
            f' fill="#a9cb78" stroke="{INK}" stroke-width="3"/></g>')
    return doc(S.g(body, filter="wobble-fine"), defs)


BDOTS = ((2195, 830, 15), (2255, 770, 22), (2335, 705, 30))


def bubble_dots_svg(i):
    pts = BDOTS[i]
    x, y, r = pts
    return doc(S.g(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffaf0" stroke="{INK}" stroke-width="4"/>',
                   filter="wobble-fine"))


def mini_brother(i):
    x = MINI_X[i]
    if i == 0:
        m = C.eliab(x, BUB_FLOOR, BS, 1, pose="stand", expr="happy")
    else:
        m = C.soldier(x, BUB_FLOOR, BS, 1 if i == 1 else -1, side="israel", variant=i, pose="stand", expr="happy")
    return doc(C.ground_shadow(x, BUB_FLOOR, BS, 120) + m)


def mini_david_svg():
    x = MINI_X[3]
    return doc(C.ground_shadow(x, BUB_FLOOR, BS, 100) + C.david(x, BUB_FLOOR, BS, -1, pose="stand", expr="happy") +
               heart_markup(x + 4, BUB_FLOOR - 140, 16))


def mini_tent_svg():
    return doc(PR.tent(2750, BUB_FLOOR - 4, 0.46, 1, side="israel"))


def number_svg(i):
    x = MINI_X[i] + (6 if i else -8)
    y = BUB_FLOOR - (182 if i == 0 else 196)
    return doc(S.text(x, y, str(i + 1), size=46, fill="#fff3d6",
                      extra=f'stroke="{INK}" stroke-width="7" paint-order="stroke"'))


def camp_glow_svg():
    defs = S.rad_grad("s6cg", [(0, "#fff2c4", 0.8), (0.6, "#ffe9b0", 0.25), (1, "#ffe9b0", 0)])
    return doc('<ellipse cx="3140" cy="620" rx="240" ry="110" fill="url(#s6cg)"/>', defs)


# ---------------------------------------------------------------- figures


def dav(x, pose, facing, expr=None, **kw):
    return C.ground_shadow(x, GY, SC, 110) + C.david(x, GY, SC, facing, pose=pose, expr=expr, **kw)


def jes(x, pose, facing=1, expr=None):
    return C.ground_shadow(x, GY, SC, 130) + C.jesse(x, GY, SC, facing, pose=pose, expr=expr)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3, L4 = ctx.lines[:5]
    _, cam_path = make_cam(SW, SH)
    BOT = SH - 4

    t_name = when(ctx, "名叫大卫") + 0.15
    t_bub = L1.start + 0.05
    t_small = when(ctx, "最小") + 0.1
    t_three = when(ctx, "三个哥哥")
    t_army = when(ctx, "都在扫罗王")
    t_bub_out = L1.end + 0.25
    t_call = when(ctx, "爸爸耶西") + 0.3
    t_turn = snap(t_call + 0.55)
    n1 = 10
    step1 = -(DX_FIELD - DX_HOME) / n1
    t_walk1 = snap(t_turn + 0.3)
    t_arrive = snap(t_walk1 + n1 * DWALK_P)
    t_give = snap(max(when(ctx, "这些饼") + 0.1, t_arrive + 0.5))
    t_yay = snap(t_give + 0.55)
    t_take = snap(min(L3.chunks[0].end - 0.1, t_give + 1.6))
    t_go_see = when(ctx, "去看看")
    t_ok = when(ctx, "看他们好不好")
    t_night = L3.end + 0.15            # quick night
    t_dark = snap(t_night + 0.45)
    t_dawn = L4.start
    t_help0 = snap(t_dawn - 0.25)      # helper walks in (off-screen at first)
    t_hand = when(ctx, "把羊交给") + 0.35
    t_off = snap(when(ctx, "出发了") - 0.05)

    # ---------------- camera
    C0 = cam_at(2080, 1660, BOT)
    C1 = cam_at(2110, 1520, BOT)
    CB = cam_at(2330, 2000, BOT)
    CJ = cam_at(1460, 2200, BOT)
    CH = cam_at(960, 1500, BOT)
    CH2 = cam_at(920, 1360, BOT)
    CW = cam_at(1560, 2000, BOT)
    CE = cam_at(1900, 1960, BOT)
    sc.camera = cam_path([(0, C0), (L0.start + 0.3, C0), (L0.end, C1), (t_bub - 0.2, C1), (t_bub + 1.2, CB),
                          (t_bub_out, CB), (t_call - 0.1, CJ), (t_walk1 + 0.6, CJ), (t_arrive + 0.5, CH),
                          (t_give + 0.3, CH), (L3.end, CH2), (t_dawn, CH2), (t_hand + 0.4, CW), (t_off, CW),
                          (T, CE)])

    # ---------------- sky, lighting
    night = lambda t: M.progress(t, t_night, t_dark, "sine") * (1 - M.progress(t, t_dawn - 0.1, t_dawn + 0.9, "sine"))  # noqa: E731
    dawn = lambda t: M.progress(t, t_dawn - 0.2, t_dawn + 1.4, "sine")  # noqa: E731
    sc.add("sky", sky_day_svg(), z=0, wc=0.5)
    sc.add("sky_dawn", sky_dawn_svg(), z=0.1, wc=0.4, motion=lambda t: Tf(alpha=dawn(t)))
    sc.add("sun", sun_svg(), z=0.15, wc=0.3,
           motion=lambda t: Tf(dy=170 * (1 - M.progress(t, t_dawn, t_dawn + 3.2, "out")), alpha=dawn(t)))
    sc.add("stars", stars_svg(), z=0.2, wc=0.2, motion=lambda t: Tf(alpha=night(t)))
    sc.add("clouds", clouds_svg(), z=0.3, wc=0.6, motion=M.drift(vx=-9))
    sc.add("far", far_svg(), z=1)
    sc.add("camp_glow", camp_glow_svg(), z=1.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, t_army, t_army + 0.5, "sine") *
                               (1 - M.progress(t, t_bub_out, t_bub_out + 0.8, "sine"))))
    sc.add("mid", mid_svg(), z=2)
    sc.add("ground", ground_svg(), z=3)
    sc.fx.append(FX.sparkles((2960, 560, 3290, 680), count=9, t0=t_army, t1=t_bub_out + 0.6, size=(6, 13), drift=-4,
                             seed=61))
    # birds over the hills
    for i, (y, t0, t1, s) in enumerate(((330, 1.0, 13.0, 0.42), (380, 1.6, 14.0, 0.36), (300, 25.0, 33.0, 0.4))):
        ref = (1600, 400)
        fr = [doc(PR.dove(ref[0], ref[1], s, 1 if i < 2 else -1, wing=w)) for w in (1.0, 0.4, -0.5, -1.0, -0.4, 0.3)]
        x0, x1 = (900, 3200) if i < 2 else (2800, 600)

        def mv(t, x0=x0, x1=x1, y=y, t0=t0, t1=t1, ph=i * 0.3):
            u = (t - t0) / (t1 - t0)
            return Tf(dx=x0 + (x1 - x0) * u - ref[0], dy=y + 16 * math.sin(2 * math.pi * (u * 2 + ph)) - ref[1],
                      alpha=1.0 if t0 <= t <= t1 else 0.0)
        sc.add(f"bird{i}", fr, z=1.5, wc=0.5, frame_at=lambda t, i=i: float(int(t * 10 + 2 * i) % 6), motion=mv)

    # ---------------- sheep (behind the people) and the planted staff
    SHEEP = [  # name, x, y, s, facing, variant, lamb, bleats, z
        ("sh1", 1560, 1095, 0.92, 1, 0, False, (), 3.3),
        ("sh4", 1720, 1052, 0.78, 1, 3, False, (), 3.2),
        ("sh2", 2420, 1112, 1.0, -1, 1, False, (t_hand + 0.5,), 3.4),
        ("sh3", 2660, 1070, 0.86, -1, 2, False, (), 3.3),
        ("sh5", 2950, 1050, 0.78, 1, 0, False, (t_off + 1.0,), 3.2),
        ("sh6", 1930, 1080, 0.85, 1, 2, False, (), 3.3),
        ("lamb1", 2270, 1140, 1.0, -1, 0, True, (t_name + 0.3,), 3.45),
        ("lamb2", 1440, 1128, 0.95, 1, 3, True, (), 3.45),
    ]
    for i, (nm, x, y, s, f, v, lamb, bl, z) in enumerate(SHEEP):
        sheep_layer(sc, nm, z, x, y, s, f, v, lamb, seed=40 + i, bleats=bl, T=T)

    # David's staff: in his hand (pasture) -> planted where he stood when he turned -> the helper's
    st_x = C.hand_positions(C.david, DX_FIELD, GY, SC, 1, pose="stand", staff=True)[1][0] + 1
    t_grab = snap(t_hand)
    sc.add("staff", doc(PR.staff(st_x, GY - 3, SC * 0.955, 1)), z=3.5,
           motion=lambda t: Tf(alpha=1.0 if t_turn <= t < t_grab else 0.0))

    # ---------------- helper shepherd (walks in at dawn, takes the staff)
    hf = -1
    HX = st_x + 30                          # his anchor when he stands at the staff (near hand on it)
    hx_near = C.hand_positions(C.citizen, HX, GY, SC, hf, kind="man", variant=3, pose="stand")[1][0]
    HX += st_x - hx_near
    n_h = 8
    step_h = -95.0

    def helper(pose, expr=None, staff=False):
        out = C.ground_shadow(HX, GY, SC, 120)
        if staff:
            out += PR.staff(st_x, GY - 3, SC * 0.955, 1)
        return out + C.citizen(HX, GY, SC, hf, kind="man", variant=3, pose=pose, expr=expr)
    hfr = [helper("walk_a"), helper("walk_b"), helper("stand", "happy"), helper("stand", "happy", True),
           helper("stand", blink_expr("happy"), True)]
    t_help_end = snap(t_help0 + n_h * WALK_P)
    actor(sc, "helper", 3.6, hfr, (HX, GY), SC,
          base=with_blinks([(0, 2), (t_grab, 3)], {3: 4}, [t_grab + 1.4, T - 0.9]),
          walks=[(t_help0, n_h, step_h, 0)], start_off=-n_h * step_h,
          bumps=[dip(t_help_end, SC, (HX, GY), 5), dip(t_grab, SC, (HX, GY), 7), nod(t_grab + 0.25, (HX, GY), -3, 0.6),
                 nod(t_off + 0.4, (HX, GY), -3, 0.6)],
          extra=lambda t: Tf(alpha=1.0 if t >= t_help0 - 0.05 else 0.0))

    # ---------------- Jesse
    jd = JX - DOOR_X
    t_j0 = snap(L2.start + 0.35)
    jfr = [jes(JX, "walk_a"), jes(JX, "walk_b"), jes(JX, "stand", 1, "happy"), jes(JX, "talk"), jes(JX, "give"),
           jes(JX, "talk", 1, blink_expr("happy")), jes(JX, "stand", 1, blink_expr("happy"))]
    t_jtalk = snap(t_call)
    t_j_end = snap(t_j0 + 2 * WALK_P)
    jbase = [(0, 2), (t_jtalk, 3), (t_give, 4), (t_take, 3), (snap(L3.end + 0.3), 2), (t_off, 3)]
    actor(sc, "jesse", 4.0, jfr, (JX, GY), SC, base=with_blinks(jbase, {2: 6, 3: 5}, [L3.end - 1.2, t_dawn + 1.6,
                                                                                     T - 0.7]),
          walks=[(t_j0, 2, jd / 2, 0)], start_off=-jd,
          bumps=[dip(t_j_end, SC, (JX, GY), 5), dip(t_jtalk, SC, (JX, GY), 6), dip(t_give, SC, (JX, GY), 8),
                 dip(t_take, SC, (JX, GY), 8), nod(t_go_see + 0.3, (JX, GY), 3, 0.6), nod(t_ok + 0.4, (JX, GY), 3, 0.6),
                 dip(snap(L3.end + 0.3), SC, (JX, GY), 4), dip(t_off, SC, (JX, GY), 5),
                 nod(t_off + 0.6, (JX, GY), 4, 0.5), nod(t_off + 1.2, (JX, GY), 4, 0.5)],
          extra=lambda t: Tf(alpha=M.progress(t, t_j0 - 0.25, t_j0 + 0.05, "sine")))
    # Jesse's calling arcs
    jm = C.body_points(C.jesse, JX, GY, SC, 1, pose="talk")["head"]
    sc.add("jarcs", [doc(arcs_markup(jm[0] + 60, jm[1] + 14, 1, k, 1.4)) for k in (1, 2, 3)], z=4.05, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3),
           motion=lambda t: Tf(alpha=1.0 if t_jtalk + 0.1 <= t < t_jtalk + 1.3 else 0.0))

    # ---------------- David
    H = DX_HOME
    e_h = "happy"
    dfr = [dav(H, "walk_a", -1), dav(H, "walk_b", -1),                     # 0 1 walk to Jesse
           dav(H, "walk_a", 1, basket=True), dav(H, "walk_b", 1, basket=True),   # 2 3 setting off
           dav(H, "stand", 1, staff=True),                                    # 4 pasture
           dav(H, "stand", 1, blink_expr(e_h), staff=True),                   # 5
           dav(H, "stand", -1, "surprised"),                                  # 6 turns at the call
           dav(H, "stand", -1, e_h), dav(H, "stand", -1, blink_expr(e_h)),    # 7 8 at Jesse
           dav(H, "carry_basket", -1), dav(H, "carry_basket", -1, blink_expr("happy")),   # 9 10
           dav(H, "stand", 1, e_h, basket=True), dav(H, "stand", 1, blink_expr(e_h), basket=True),  # 11 12 dawn
           dav(H, "stand", 1, "kind", staff=True)]                            # 13 thinking of his brothers
    t_d_dawn = snap(t_dark + 0.1)
    dbase = [(0, 4), (snap(t_bub - 0.05), 13), (snap(t_bub_out + 0.2), 4), (t_turn, 6), (t_arrive, 7),
             (t_take, 9), (t_d_dawn, 11)]
    dbase = with_blinks(dbase, {4: 5, 7: 8, 9: 10, 11: 12}, [2.6, 12.8, 20.6, 23.0, 26.0, 27.4])
    n2 = 9
    actor(sc, "david", 4.5, dfr, (H, GY), SC, base=dbase,
          walks=[(t_walk1, n1, step1, 0), (t_off, n2, 98.0, 2)], start_off=DX_FIELD - DX_HOME,
          bumps=[happy_hop(snap(t_name), SC, (H, GY), 20), dip(snap(t_bub - 0.05), SC, (H, GY), 5),
                 dip(snap(t_bub_out + 0.2), SC, (H, GY), 5), dip(t_turn, SC, (H, GY), 8),
                 dip(t_arrive, SC, (H, GY), 6), happy_hop(t_yay, SC, (H, GY), 18), dip(t_take, SC, (H, GY), 9),
                 nod(t_ok + 1.2, (H, GY), -4, 0.5), happy_hop(snap(t_ok + 1.9), SC, (H, GY), 12),
                 dip(t_d_dawn, SC, (H, GY), 5), nod(t_grab + 0.45, (H, GY), 4, 0.5),
                 happy_hop(snap(t_grab + 1.1), SC, (H, GY), 12)],
          breathe=(0.012, 2.8, 0.2), period=DWALK_P)

    # ---------------- the thought bubble (line 1)
    bcx, bcy = BUB[0], BUB[1]
    pop_in = lambda t0, piv: M.keys([(t0 - 0.01, {"alpha": 0, "s": 0.3}), (t0 + 0.05, {"alpha": 1}),  # noqa: E731
                                     (t0 + 0.28, {"s": 1.06}), (t0 + 0.42, {"s": 1.0})], ["out", "out", "sine"],
                                    pivot=piv)
    pop_out = lambda t0, piv: M.keys([(t0, {"s": 1.0, "alpha": 1}), (t0 + 0.1, {"s": 1.08}),  # noqa: E731
                                      (t0 + 0.3, {"s": 0.2, "alpha": 0})], ["sine", "in"], pivot=piv)
    for i in range(3):
        x, y = BDOTS[i][:2]
        sc.add(f"bdot{i}", bubble_dots_svg(i), z=6, wc=0.3,
               motion=M.combine(pop_in(t_bub + 0.12 * i, (x, y)), pop_out(t_bub_out + 0.25 - 0.08 * i, (x, y)),
                                M.bob(3, 2.2, i * 0.3)))
    tb_main = t_bub + 0.4
    bub_m = lambda: M.combine(pop_in(tb_main, (bcx, bcy + 120)), pop_out(t_bub_out, (bcx, bcy + 120)),  # noqa: E731
                              M.bob(4, 3.0))
    sc.add("bubble", bubble_svg(), z=6.1, wc=0.3, motion=bub_m())
    sc.add("mini_tent", mini_tent_svg(), z=6.15, wc=0.5,
           motion=M.combine(bub_m(), M.keys([(t_army + 0.25, {"alpha": 0, "sy": 0.3}), (t_army + 0.45, {"alpha": 1, "sy": 1.1}),
                                             (t_army + 0.6, {"sy": 1.0})], "out", pivot=(2750, BUB_FLOOR))))
    for i in range(3):
        tc = t_three + 0.35 * i + 0.15
        x = MINI_X[i]
        sc.add(f"bro{i}", mini_brother(i), z=6.2, wc=0.5,
               motion=M.combine(bub_m(), happy_hop(tc, BS, (x, BUB_FLOOR), 22),
                                hop(t_army + 0.55, [(0, {"dy": 0}), (0.15, {"dy": -10}), (0.3, {"dy": 0})],
                                    (x, BUB_FLOOR))))
        sc.add(f"num{i}", number_svg(i), z=6.3, wc=0,
               motion=M.combine(bub_m(), M.keys([(tc - 0.01, {"alpha": 0, "s": 0.4}), (tc + 0.15, {"alpha": 1, "s": 1.1}),
                                                 (tc + 0.3, {"s": 1.0}), (t_army - 0.1, {"alpha": 1}),
                                                 (t_army + 0.2, {"alpha": 0})], "out", pivot=(x, BUB_FLOOR - 200))))
    mdx = MINI_X[3]
    sc.add("mini_david", mini_david_svg(), z=6.2, wc=0.5,
           motion=M.combine(bub_m(), happy_hop(t_small, BS, (mdx, BUB_FLOOR), 26),
                            lambda t: Tf(alpha=1.0 if t < t_army + 0.05 else 0.0)))
    sc.add("mini_puff", doc(puff_markup(mdx, BUB_FLOOR - 60, 60, 70, seed=6, k=0.6)), z=6.25, wc=0,
           motion=M.combine(bub_m(), puff_motion(t_army + 0.05, (mdx, BUB_FLOOR - 60))))

    # ---------------- foreground grass
    sc.add("fg", [fg_svg(k) for k in range(3)], z=8, frame_at=lambda t: float(int(t * 2.2) % 3))

    # ---------------- night / dawn washes
    sc.fx.append(FX.tint((40, 52, 96), lambda t: 0.7 * night(t), mode="multiply"))
    sc.fx.append(FX.tint((255, 214, 184), lambda t: 0.22 * dawn(t) * (1 - 0.5 * M.progress(t, t_dawn + 2, T)),
                         mode="multiply"))

    # ---------------- sound
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0.0, dur=t_night + 0.4, gain_db=-19, fade_in=0.8, fade_out=0.6)
    sc.sfx("birds", t_dawn + 0.8, dur=T - t_dawn - 0.8, gain_db=-19, fade_in=1.0, fade_out=1.0)
    sc.sfx("sheep", t_name + 0.3, gain_db=-11, pan=0.2)
    sc.sfx("pop", tb_main, gain_db=-12)
    sc.sfx("sparkle", t_small, gain_db=-16)
    for i in range(3):
        sc.sfx("pop", t_three + 0.35 * i + 0.15, gain_db=-14 + i)
    sc.sfx("pop", t_army + 0.05, gain_db=-11)
    sc.sfx("sparkle", t_army + 0.3, gain_db=-15, pan=0.5)
    sc.sfx("pop", t_bub_out + 0.1, gain_db=-14)
    sc.sfx("footsteps", t_walk1, dur=n1 * DWALK_P, gain_db=-17, pan=-0.2)
    sc.sfx("cloth", t_give, gain_db=-15)
    sc.sfx("night", t_night, dur=t_dawn - t_night + 0.6, gain_db=-18, fade_in=0.3, fade_out=0.5)
    sc.sfx("rooster", t_dawn + 0.3, gain_db=-12, pan=-0.4)
    sc.sfx("footsteps", t_help0, dur=n_h * WALK_P, gain_db=-18, pan=0.4)
    sc.sfx("sheep", t_hand + 0.5, gain_db=-12, pan=0.3)
    sc.sfx("footsteps", t_off, dur=T - t_off, gain_db=-16, fade_out=0.6)
    sc.sfx("sheep", t_off + 1.0, gain_db=-14, pan=0.5)
    return sc
