"""Scene 4 — Joseph's dream of the sheaves (Genesis 37:5-8).

One 2112 x 1188 page in Jacob's camp on the hills of Canaan: on the left the family's big open-fronted goat-hair
tent, on the right the meadow where the brothers stand in the morning; a dream bubble floats over the middle.

  line 0  '有一天晚上，约瑟做了一个梦。'  night: stars, a crescent moon, the oil lamp glowing in the tent; Joseph asleep
          on the rug, smiling in his sleep (z's). '做了一个梦' - three little dream dots rise from his head and the
          dream bubble pops open: a golden stubble field under a dawn sky. The camera follows up into the bubble.
  line 1  '我梦见我们在田里捆麦子。'  (Joseph telling it) '捆麦子' - eleven bound sheaves pop onto the field one by one
          (each with a puff of straw), lying down.  '我的那一捆站了起来，'  Joseph's sheaf in the middle stands up
          (rise 0 -> 1 with a bounce) and glows gold (halo + sparkles). Meanwhile, around the bubble, the night sky
          turns to morning.  '你们的麦捆都围过来，'  the camera pulls back: it is morning, Joseph (in his coat) tells his
          ten brothers excitedly (talk, proud) under the bubble; inside it the brothers' sheaves stand up and hop in
          round his sheaf.  '向我的麦捆下拜！'  they bow to it (bow 0 -> 1); the brothers' faces turn jealous.
  line 2  '哥哥们听了，更生气了。'  the bubble pops away; '更生气了' - the brothers cross their arms with a stomp
          (dust puffs, grumble clouds) and glare; Joseph's proud smile drops (surprised).
  line 3  '难道你还想做王，管我们吗？'  the front brother (Simeon) steps toward Joseph and points, scolding (sound
          arcs); Joseph shrinks a little (worried). Calm hold to the page turn.

Hard pose cuts hide in dips / hops (or off-camera while the camera is inside the bubble); all times come from the
narration chunks. Shared helpers for s05-s07 live at the top of this file.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import (arcs_markup, cuts, dip, grumble_markup, happy_hop, hop, nod, puff_markup,
                                 puff_motion, snap, step_walk)
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s06_shepherd import blink_expr, cam_at, make_cam, when, with_blinks

SW, SH = 2112, 1188
INK = P["ink"]
GY = 1030                 # ground line
SC = 0.9                  # figure scale (Joseph ~292 px, brothers ~310)
WALK_P = 0.26


def doc(body, defs="", w=SW, h=SH):
    return S.svg_doc(body, defs, w=w, h=h)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ shared helpers (s04-s07)


def sprite(sc, name, z, frames, anchor, base=(), bumps=(), breathe=(0.01, 3.0, 0.0), extra=None, walks=(),
           period=WALK_P, s=SC, start_off=0.0, docf=None, wc=1.0):
    """A character / prop layer: ``frames`` (markup or full docs) drawn at ``anchor``; ``base`` [(t, idx)] hard
    cuts; ``walks`` [(t0, n, step, pair_idx)] planted-foot walks (pair_idx = that walk's walk_a frame, walk_b
    follows it); ``bumps`` extra motions; ``extra`` added last. Returns dx(t) (walk offset)."""
    docf = docf or doc
    ws = [step_walk(w[0], w[1], w[2], period, s) for w in walks]
    pairs = [w[3] for w in walks]
    fb = cuts(list(base) or [(0, 0)])

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
    frs = [f if f.startswith("<svg") else docf(f) for f in frames]
    sc.add(name, frs, z=z, frame_at=fa, motion=M.combine(*mot), wc=wc)
    return dx


def show(t0, t1=1e9, fade=0.0):
    """Alpha window (hard or faded)."""
    if fade <= 0:
        return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)
    return M.visible(t0, t1, fade)


def pop_in(t0, pivot, dur=0.32, over=1.1):
    return M.keys([(t0 - 0.01, {"alpha": 0, "s": 0.2}), (t0 + 0.04, {"alpha": 1}), (t0 + dur * 0.65, {"s": over}),
                   (t0 + dur, {"s": 1.0})], ["out", "out", "sine"], pivot=pivot)


def pop_out(t0, pivot, dur=0.3):
    return M.keys([(t0, {"s": 1.0, "alpha": 1}), (t0 + dur * 0.35, {"s": 1.08}), (t0 + dur, {"s": 0.15, "alpha": 0})],
                  ["sine", "in"], pivot=pivot)


def stomp(t0, s, pivot, depth=10.0):
    """A cross little stomp: up, then down hard (squash), settle."""
    return hop(t0, [(-0.2, {"dy": 0, "sy": 1}), (-0.08, {"dy": -12 * s, "sy": 1.03}), (0, {"dy": depth * s, "sy": 0.94}),
                    (0.14, {"dy": -2 * s, "sy": 1.01}), (0.3, {"dy": 0, "sy": 1})], pivot, ["out", "in", "out", "sine"])


def dust_markup(cx, cy, w, seed=0, k=1.0):
    """A little ground dust puff (stomp / landing)."""
    rng = random.Random(seed)
    out = ""
    for i in range(5):
        x = cx + (i - 2) * w * 0.22 + rng.uniform(-6, 6)
        r = w * rng.uniform(0.16, 0.24) * (1.15 - abs(i - 2) * 0.15)
        out += S.cloud(x, cy - r * 0.35, r * 2.0, r * 1.2, "#efe2c6", seed=seed * 7 + i, puffs=3, sw=2.2 * k,
                       shade_fill="#dccaa4")
    return S.g(out, filter="wobble-fine", opacity=0.92)


def dust_motion(t0, pivot, dur=0.6):
    return M.keys([(t0 - 0.01, {"alpha": 0, "s": 0.5}), (t0 + 0.05, {"alpha": 0.95, "s": 0.85}),
                   (t0 + dur, {"alpha": 0, "s": 1.35, "dy": -14})], ["out", "sine"], pivot=pivot)


def sky_svg(gid, stops, w=SW, h=SH):
    return doc(f'<rect x="-20" y="-20" width="{w + 40}" height="{h + 40}" fill="url(#{gid})"/>',
               S.lin_grad(gid, stops), w, h)


def stars_markup(seed, x0, x1, y0, y1, n=60):
    rng = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(2.2, 4.8)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fff6d8"/>'
        if r > 4.2:
            out += (f'<path d="M{f1(x - 3 * r)},{f1(y)} L{f1(x + 3 * r)},{f1(y)} M{f1(x)},{f1(y - 3 * r)} '
                    f'L{f1(x)},{f1(y + 3 * r)}" stroke="#fff6d8" stroke-width="1.6" opacity="0.7"/>')
    return out


def moon_markup(x, y, r=46):
    return (f'<circle cx="{x}" cy="{y}" r="{r * 2.3:.0f}" fill="#fff2c4" opacity="0.18" filter="url(#blur-md)"/>'
            f'<path d="M{x},{y - r} a{r},{r} 0 1,0 {r * 0.87:.1f},{r * 1.5:.1f} a{r * 0.78:.1f},{r * 0.78:.1f} 0 1,1 '
            f'{-r * 0.87:.1f},{-r * 1.5:.1f} Z" fill="#fff0c4" stroke="{P["ink_soft"]}" stroke-width="3"/>')


def sun_markup(x, y, r=74):
    return S.g(f'<circle cx="{x}" cy="{y}" r="{r * 2.6:.0f}" fill="#fff1c8" opacity="0.35" filter="url(#blur-md)"/>'
               f'<path d="{S.rays(x, y, r * 1.25, r * 2.6, 12, 9)}" fill="#fbd46b" opacity="0.45"/>'
               f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fbcf6a" stroke="#e9925a" stroke-width="5"/>'
               f'<circle cx="{x - r * 0.28:.0f}" cy="{y - r * 0.3:.0f}" r="{r * 0.25:.0f}" fill="#fde7a8"/>',
               filter="wobble")


def clouds_markup(items, fill="#fbf4e6", shade_fill="#e3e3dc"):
    out = ""
    for cx, cy, w, h, sd in items:
        out += S.cloud(cx, cy, w, h, fill=fill, seed=sd, sw=3, shade_fill=shade_fill)
    return S.g(out, filter="wobble")


def far_hills_markup(w=SW, base=760, seed=3, tents=True):
    """Hazy far ridges of Canaan with a few olive trees and (optionally) tiny far tents."""
    out = S.path(S.hill(-80, w + 80, base, 150, seed=seed, bumps=5), "#bfd2c4", sw=3)
    out += S.path(S.hill(-80, w + 80, base + 70, 120, seed=seed + 5, bumps=4), "#adc9a2", sw=3.5)
    rng = random.Random(seed)
    for i in range(int(w / 260)):
        x = 120 + i * 260 + rng.uniform(-60, 60)
        out += PR.olive_tree(x, base + 70 - rng.uniform(40, 80), rng.uniform(0.16, 0.22), seed=i)
    if tents:
        for x, y, s in ((w * 0.62, base + 2, 0.12), (w * 0.67, base - 4, 0.11)):
            out += PR.tent(x, y, s, 1, side="israel", flag=False)
    return S.g(out, filter="wobble")


def meadow_markup(x0, x1, y_top, y_bot, seed=5, col_top="#a9c873", col_bot="#8fb35e"):
    """Rolling meadow band with darker grass strokes and a few flowers."""
    gid = f"mdw{seed}"
    defs = S.lin_grad(gid, [(0, col_top), (1, col_bot)])
    out = f"<defs>{defs}</defs>" + S.path(S.hill(x0, x1, y_top + 60, 70, seed=seed, bottom=y_bot + 60, bumps=3),
                                          f"url(#{gid})", sw=4)
    rng = random.Random(seed)
    for _ in range(int((x1 - x0) / 22)):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y_top + 80, y_bot)
        h = rng.uniform(10, 20)
        out += (f'<path d="M{f1(x)},{f1(y)} q{f1(rng.uniform(-4, 4))},{f1(-h * 0.6)} {f1(rng.uniform(-6, 6))},{f1(-h)}" '
                f'stroke="#6f9446" stroke-width="2.6" fill="none" stroke-linecap="round" opacity="0.7"/>')
    for _ in range(int((x1 - x0) / 120)):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y_top + 90, y_bot - 20)
        c = rng.choice(("#f3d36b", "#f6efe0", "#e99a8f"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="5" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
    return out


def tuft_row(items, phase):
    out = ""
    for x, y, s, v in items:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.45 * math.sin(phase + x * 0.013))
    return out


def family_tent(cx, gy, s=1.0, lamp=True, inner=""):
    """Jacob's family tent: a wide black-goat-hair tent with cream stripes, the front opened up on two poles so the
    rug inside shows (``inner``: markup drawn inside, e.g. a sleeping Joseph). Anchor = ground at the centre of the
    opening. Width ~ 980*s; roof top ~ -425*s."""
    def p(x, y):
        return f"{f1(cx + x * s)},{f1(gy + y * s)}"
    hair, hair_d, stripe = "#5b4537", "#463429", "#e9dcc0"
    roof = (f"M{p(-470, -245)} Q{p(-430, -320)} {p(-380, -365)} Q{p(-190, -430)} {p(0, -428)} "
            f"Q{p(190, -430)} {p(380, -365)} Q{p(430, -320)} {p(470, -245)} "
            f"L{p(380, -318)} Q{p(285, -270)} {p(190, -292)} Q{p(95, -320)} {p(0, -352)} "
            f"Q{p(-95, -320)} {p(-190, -292)} Q{p(-285, -270)} {p(-380, -318)} Z")
    opening = (f"M{p(-380, -318)} Q{p(-285, -270)} {p(-190, -292)} Q{p(-95, -320)} {p(0, -352)} "
               f"Q{p(95, -320)} {p(190, -292)} Q{p(285, -270)} {p(380, -318)} L{p(400, 6)} L{p(-400, 6)} Z")
    gid = f"tin{int(cx)}{int(gy)}"
    defs = S.lin_grad(gid, [(0, "#3f2c22"), (0.55, "#5e4230"), (1, "#7d5a3e")])
    out = f"<defs>{defs}</defs>"
    # interior (back wall + floor), the middle pole at the back
    out += S.path(opening, f"url(#{gid})", sw=0, extra="")
    out += (f'<path d="M{p(-360, -40)} L{p(360, -40)}" stroke="#2f2119" stroke-width="{5 * s:.1f}" opacity="0.5"/>')
    out += S.path(f"M{p(-8, -350)} L{p(-8, -40)} L{p(8, -40)} L{p(8, -350)} Z", "#6b4a32", sw=3 * s)
    # hanging bundles / water skin on the back wall
    out += S.path(f"M{p(-250, -250)} q{25 * s:.1f},{40 * s:.1f} 0,{90 * s:.1f} q{-30 * s:.1f},{-10 * s:.1f} "
                  f"{-28 * s:.1f},{-50 * s:.1f} Z", "#a0764e", sw=3 * s)
    out += S.path(f"M{p(230, -250)} q{36 * s:.1f},{20 * s:.1f} {30 * s:.1f},{80 * s:.1f} "
                  f"q{-40 * s:.1f},{12 * s:.1f} {-56 * s:.1f},{-20 * s:.1f} Z", "#8c6a44", sw=3 * s)
    # rug
    rug = f"M{p(-360, -46)} L{p(360, -46)} L{p(395, 10)} L{p(-395, 10)} Z"
    out += S.path(rug, "#b4553f", sw=3.5 * s)
    out += S.path(f"M{p(-340, -34)} L{p(340, -34)} L{p(368, 0)} L{p(-368, 0)} Z", "none", sw=2.5 * s,
                  extra=f'stroke-dasharray="{10 * s:.0f} {7 * s:.0f}" opacity="0.7"')
    for k in range(-3, 4):
        x = k * 100
        out += (f'<path d="M{p(x - 22, -18)} L{p(x, -32)} L{p(x + 22, -18)} L{p(x, -4)} Z" fill="#e8b63c" '
                f'stroke="{INK}" stroke-width="{2.2 * s:.1f}"/>')
    out += inner
    # cushions and the lamp
    out += PR.cushion(cx - 330 * s, gy - 30 * s, 0.55 * s, color="#4f86a6")
    if lamp:
        out += PR.oil_lamp(cx + 300 * s, gy - 34 * s, 0.75 * s, lit=True)
    out += PR.jar(cx + 350 * s, gy - 60 * s, 0.6 * s)
    # roof cloth with stripes
    cid = f"troof{int(cx)}{int(gy)}"
    stripes = ""
    for k in range(-5, 6):
        x = k * 90
        stripes += S.path(f"M{p(x - 14, -450)} L{p(x + 14, -450)} L{p(x * 1.04 + 14, -230)} L{p(x * 1.04 - 14, -230)} Z",
                          stripe, sw=0, extra='opacity="0.85"')
    out += S.path(roof, hair, sw=4.5 * s)
    out += f'<clipPath id="{cid}"><path d="{roof}"/></clipPath><g clip-path="url(#{cid})">{stripes}</g>'
    out += S.path(roof, "none", sw=4.5 * s)
    # side walls pulled down to the ground
    for sg in (-1, 1):
        wall = f"M{p(sg * 470, -245)} L{p(sg * 380, -318)} L{p(sg * 400, 6)} L{p(sg * 500, 6)} Z"
        out += S.path(wall, hair_d, sw=4 * s)
        for j in range(3):
            x0 = sg * (395 + j * 30)
            out += S.path(f"M{p(x0, -300 + j * 22)} L{p(x0 + sg * 10, 0)}", "none", sw=3 * s,
                          extra=f'stroke="{stripe}" opacity="0.55"')
    # front poles, guy ropes and pegs
    for sg in (-1, 1):
        out += S.path(f"M{p(sg * 380 - 9, -330)} L{p(sg * 380 + 9, -330)} L{p(sg * 384 + 9, 8)} L{p(sg * 384 - 9, 8)} Z",
                      P["wood"], sw=3 * s)
        out += (f'<path d="M{p(sg * 380, -365)} L{p(sg * 640, 4)}" stroke="#7a5a40" stroke-width="{3.4 * s:.1f}" '
                f'fill="none"/>')
        out += S.path(f"M{p(sg * 640 - 6, -14)} L{p(sg * 640 + 6, -14)} L{p(sg * 641, 8)} Z", P["wood_dark"], sw=2.5 * s)
    return S.g(out, filter="wobble-fine")


def tent_glow_markup(x, y, r):
    gid = f"tglow{int(x)}{int(y)}"
    return (f'<defs>{S.rad_grad(gid, [(0, "#ffd88a", 0.85), (0.45, "#f6b25c", 0.35), (1, "#f6b25c", 0)])}</defs>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.75:.0f}" fill="url(#{gid})"/>')


def bros_markup(items):
    """items: [(variant, x, gy, s, facing, pose, expr)] drawn in order (back first), with shadows."""
    out = ""
    for v, x, gy, s, f, pose, expr in items:
        out += C.ground_shadow(x, gy, s, 120) + C.brothers(x, gy, s, f, variant=v, pose=pose, expr=expr, staff=False)
    return out


def compose_tf(local, outer, piv_l, piv_o):
    """Compose two scale/translate transforms (local applied first, then outer) into one Tf with pivot (0, 0)."""
    def m(t):
        a, b = local(t), outer(t)
        plx = a.px if a.px is not None else piv_l[0]
        ply = a.py if a.py is not None else piv_l[1]
        pox = b.px if b.px is not None else piv_o[0]
        poy = b.py if b.py is not None else piv_o[1]
        # p' = pl + (p - pl) * sa + da ; p'' = po + (p' - po) * sb + db
        sx, sy = a.sx * b.sx, a.sy * b.sy
        ox = pox + (plx - plx * a.sx + a.dx - pox) * b.sx + b.dx
        oy = poy + (ply - ply * a.sy + a.dy - poy) * b.sy + b.dy
        return Tf(dx=ox, dy=oy, sx=sx, sy=sy, alpha=a.alpha * b.alpha, px=0.0, py=0.0)
    return m


# ============================================================================ this scene's drawings

TENT_X = 560
LAMP = PR.local_to_stage(560, GY, 0.85, 1, 300, -34)
JS_X = 600                # Joseph sleeping (anchor under the hip), inside the tent
JS_Y = GY - 16
J_X = 1000                # Joseph standing in the morning
BUB = (1185, 360)         # dream bubble centre
BW, BH = 1000, 600
RING = (1185, 562)        # Joseph's sheaf
SHEAF_S = 0.66
FRONT = [(1, 1400), (0, 1545), (3, 1690), (6, 1835), (9, 1980)]      # front row (speaker first)
BACK = [(4, 1470), (8, 1615), (2, 1760), (5, 1905)]                  # back row
GY_B = GY - 26


def bubble_inner():
    """The dream landscape (stage coords, clipped by the bubble): dawn sky, far wheat field, stubble field."""
    x0, x1 = BUB[0] - BW / 2 - 60, BUB[0] + BW / 2 + 60
    y0 = BUB[1] - BH / 2 - 60
    hz = 445
    defs = S.lin_grad("s4dsky", [(0, "#a9d3e3"), (0.45, "#cfe6e4"), (0.8, "#f8e3b6"), (1, "#fbd9a4")])
    defs += S.lin_grad("s4dgnd", [(0, "#e9cb84"), (1, "#d2a75c")])
    defs += S.rad_grad("s4dsun", [(0, "#fff3c8", 1), (0.4, "#fbe39a", 0.6), (1, "#fbe39a", 0)])
    out = f"<defs>{defs}</defs>"
    out += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{hz - y0 + 20}" fill="url(#s4dsky)"/>'
    out += f'<circle cx="{BUB[0] + 250}" cy="{hz - 40}" r="170" fill="url(#s4dsun)"/>'
    out += f'<circle cx="{BUB[0] + 250}" cy="{hz - 40}" r="52" fill="#fbd46b" stroke="#e9a45a" stroke-width="4"/>'
    out += S.g(S.cloud(BUB[0] - 250, 190, 230, 60, "#fbf6ea", seed=31, sw=3) +
               S.cloud(BUB[0] + 120, 150, 180, 48, "#fbf6ea", seed=32, sw=3) +
               S.cloud(BUB[0] + 380, 240, 150, 40, "#fbf6ea", seed=33, sw=3), filter="wobble")
    for bx, by in ((BUB[0] - 60, 230), (BUB[0] - 20, 250), (BUB[0] + 10, 222)):
        out += (f'<path d="M{bx - 14},{by} q7,-9 14,0 q7,-9 14,0" fill="none" stroke="{INK}" stroke-width="3" '
                f'stroke-linecap="round"/>')
    out += S.path(S.hill(x0, x1, hz + 6, 60, seed=12, bottom=BUB[1] + BH, bumps=3), "#c3d6a0", sw=3)
    out += PR.field(x0, x1, hz + 4, depth=40, scale=0.55, ripe=1.0, seed=4)
    out += S.path(f"M{x0},{hz + 14} Q{BUB[0]},{hz} {x1},{hz + 14} L{x1},{BUB[1] + BH} L{x0},{BUB[1] + BH} Z",
                  "url(#s4dgnd)", sw=3.5)
    rng = random.Random(9)
    for _ in range(180):
        x = rng.uniform(x0, x1)
        y = rng.uniform(hz + 22, BUB[1] + BH / 2 + 40)
        h = 6 + (y - hz) * 0.06
        out += (f'<path d="M{f1(x)},{f1(y)} l{f1(rng.uniform(-3, 3))},{f1(-h)}" stroke="#b08a48" '
                f'stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>')
    return out


def dream_cloud(x, y, w, h, inner, seed=0, nb=18, fill="#fbf6ea"):
    """PR.dream_bubble with more, closer scallops (no deep notches at wide aspect ratios), no tail."""
    rng = random.Random(seed)
    m = min(w, h)
    circles = []
    for i in range(nb):
        a = 2 * math.pi * i / nb
        rr = m * rng.uniform(0.15, 0.18)
        circles.append((x + (w / 2 - rr * 0.6) * math.cos(a), y + (h / 2 - rr * 0.6) * math.sin(a), rr))
    rx, ry = w / 2 - m * 0.08, h / 2 - m * 0.08
    core = PR._ell(x, y, rx, ry, fill, 0)
    shape = "".join(PR._circ(cx, cy, r, fill, 0) for cx, cy, r in circles) + core
    outline = "".join(PR._circ(cx, cy, r, fill, 9) for cx, cy, r in circles)
    gid = f"dcg{seed}"
    gl = (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.8), (0.7, P["gold"], 0.25), (1, P["gold"], 0)])}</defs>'
          + PR._ell(x, y, w * 0.68, h * 0.72, f"url(#{gid})", 0))
    clipd = "".join(f"M{f1(cx - r)},{f1(cy)} a{f1(r)},{f1(r)} 0 1 0 {f1(2 * r)},0 a{f1(r)},{f1(r)} 0 1 0 {f1(-2 * r)},0 Z "
                    for cx, cy, r in circles)
    clipd += f"M{f1(x - rx)},{f1(y)} a{f1(rx)},{f1(ry)} 0 1 0 {f1(2 * rx)},0 a{f1(rx)},{f1(ry)} 0 1 0 {f1(-2 * rx)},0 Z"
    body = gl + outline + shape + PR._clip(f"dcc{seed}", clipd, inner)
    return f'<g filter="url(#wobble-fine)">{body}</g>'


def bubble_svg():
    return doc(dream_cloud(BUB[0], BUB[1], BW, BH, S.g(bubble_inner(), filter="wobble"), seed=4))


def bubble_dots_markup(tx, ty, i):
    x, y = BUB
    t = (0.25, 0.55, 0.8)[i]
    px = x + (tx - x) * (0.55 + t * 0.45)
    py = (y + BH * 0.3) + (ty - (y + BH * 0.3)) * t
    r = 22 - i * 6
    return (f'<g filter="url(#wobble-fine)"><circle cx="{f1(px)}" cy="{f1(py)}" r="{r}" fill="#fbf6ea" '
            f'stroke="{INK}" stroke-width="3.4"/></g>'), (px, py)


def ring_positions():
    """Brothers' sheaves: (x_ring, y_ring, x_spread, y_spread, scale, facing) for 10 sheaves, back ones first."""
    out = []
    for a in (110, 145, 180, 215, 250, 70, 35, 0, -35, -70):
        r = math.radians(a)
        sn = math.sin(r)
        xr, yr = RING[0] + 255 * math.cos(r), RING[1] + 40 * sn
        xs, ys = RING[0] + 360 * math.cos(r), RING[1] + 4 + 46 * sn
        s = 0.54 + 0.07 * sn
        f = 1 if xr < RING[0] - 1 else (-1 if xr > RING[0] + 1 else 1)
        out.append((xr, yr, xs, ys, s, f))
    return sorted(out, key=lambda e: e[1])


def halo_svg():
    x, y = RING[0], RING[1] - 100
    defs = S.rad_grad("s4halo", [(0, "#fff1b8", 0.95), (0.4, "#f6cf5e", 0.6), (1, "#f2c14e", 0)])
    rays = S.rays(x, y, 95, 165, 14, 6)
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="160" ry="150" fill="url(#s4halo)"/>'
               f'<path d="{rays}" fill="#f2c14e" opacity="0.55"/>', defs)


def tent_svg():
    return doc(family_tent(TENT_X, GY, 0.85, lamp=False) + PR.oil_lamp(LAMP[0], LAMP[1], 0.64, lit=False))


def background_svg():
    out = S.g(far_hills_markup(base=770, seed=3), filter="wobble")
    out += S.g(S.path(S.hill(-80, SW + 80, 905, 120, seed=21, bumps=3), "#a3c47c", sw=4), filter="wobble")
    # a far sheepfold with sheep on the slope
    for x, y, s, f, v in ((1180, 905, 0.36, 1, 0), (1255, 912, 0.34, -1, 2), (1320, 902, 0.33, 1, 3),
                          (300, 900, 0.3, -1, 1), (1600, 892, 0.3, 1, 0)):
        out += PR.sheep(x, y, s, f, variant=v, pose="graze")
    out += S.g(meadow_markup(-80, SW + 80, 905, SH + 20, seed=5), filter="wobble")
    out += PR.olive_tree(2040, 960, 0.75, seed=2)
    out += PR.bush(1130, 985, 0.5, variant=1)
    return doc(out)


FG = [(40, 1150, 1.2, 0), (210, 1175, 1.0, 2), (1010, 1170, 1.1, 0), (1250, 1168, 0.9, 2), (2060, 1165, 1.15, 0),
      (1600, 1182, 1.0, 0)]


def fg_svg(k):
    return doc(tuft_row(FG, k * 2.1))


def jos(pose, expr=None, x=J_X, facing=1):
    return C.ground_shadow(x, GY, SC, 110) + C.joseph(x, GY, SC, facing, pose=pose, expr=expr)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]
    clamp, cam_path = make_cam(SW, SH)

    t_dream = when(ctx, "做了一个梦")                       # dream dots + bubble
    t_bub = t_dream + 0.45
    t_bind = when(ctx, "捆麦子") - 0.15                     # sheaves pop in
    t_rise = when(ctx, "站了起来")                           # Joseph's sheaf stands up
    t_glow = t_rise + 0.75
    t_all = when(ctx, "你们的麦捆")                          # brothers' sheaves stand
    t_gather = when(ctx, "围过来")                           # hop in round
    t_bow = when(ctx, "下拜") - 0.25                         # bow
    t_pop = snap(L1.end + 0.35)                             # bubble pops away
    t_angry = snap(when(ctx, "更生气了"))
    t_scold = snap(L3.start - 0.1)
    t_swap = snap(t_bind + 0.5)                             # off-camera: night -> morning cast change
    t_wide0, t_wide1 = t_all - 0.2, t_all + 1.5             # camera pulls back

    # ---------------- camera
    C_N = Cam(700, 800, 1300)
    C_B = Cam(BUB[0], 392, 1110)
    C_M = Cam(1185, 560, 1700)
    C_W = Cam(SW / 2, SH / 2, SW)
    C_S = Cam(1262, 700, 1700)
    sc.camera = cam_path([(0, C_N), (t_dream - 0.1, C_N), (t_bub + 1.35, C_B, "sine"), (t_wide0, C_B),
                          (t_wide1, C_M), (t_pop + 0.2, C_M), (t_pop + 1.8, C_S), (T, C_S)])

    # ---------------- sky: night -> dawn -> day (while the camera is inside the bubble)
    t_dawn0, t_dawn1 = t_bind - 0.2, t_rise + 1.0
    night = lambda t: 1 - M.progress(t, t_dawn0, t_dawn1, "sine")  # noqa: E731
    sc.add("sky", sky_svg("s4sky", [(0, "#8ec6df"), (0.55, "#bfe2ea"), (1, "#f2ead0")]), z=0, wc=0.5)
    sc.add("sky_dawn", sky_svg("s4dawn", [(0, "#b9a6d3"), (0.4, "#f1b8b0"), (0.75, "#f8cf98"), (1, "#fbe6bd")]),
           z=0.05, wc=0.4,
           motion=lambda t: Tf(alpha=min(1 - night(t), 1 - M.progress(t, t_dawn1, t_dawn1 + 2.5, "sine")) * 0.9))
    sc.add("sky_night", sky_svg("s4night", [(0, "#16203a"), (0.6, "#2b3a62"), (1, "#4a5a84")]), z=0.1, wc=0.4,
           motion=lambda t: Tf(alpha=night(t)))
    sc.add("stars", doc(stars_markup(3, 0, SW, 10, 760, 70)), z=0.15, wc=0.0,
           motion=lambda t: Tf(alpha=night(t) * (0.85 + 0.15 * math.sin(t * 2.3))))
    sc.add("moon", doc(moon_markup(260, 170)), z=0.16, wc=0.2, motion=lambda t: Tf(alpha=night(t), dy=-6 * t))
    sc.add("sun", doc(sun_markup(1880, 300)), z=0.17, wc=0.3,
           motion=lambda t: Tf(dy=260 * (1 - M.progress(t, t_dawn0 + 0.6, t_dawn1 + 1.5, "out")),
                               alpha=M.progress(t, t_dawn0 + 0.5, t_dawn1, "sine")))
    sc.add("clouds", doc(clouds_markup(((520, 190, 330, 76, 1), (1450, 120, 280, 64, 2), (1840, 205, 300, 70, 3),
                                        (-60, 330, 260, 60, 6), (980, 260, 220, 50, 7)))), z=0.2, wc=0.6,
           motion=lambda t: Tf(dx=-8 * t, alpha=0.35 + 0.65 * (1 - night(t))))
    sc.add("bg", background_svg(), z=1)
    sc.add("tent", tent_svg(), z=2)

    # ---------------- Joseph: asleep in the tent -> (off camera) up in the morning, telling the dream
    sleep_fr = doc(C.joseph(JS_X, JS_Y, SC, 1, pose="dream"))
    sleep_fr2 = doc(C.joseph(JS_X, JS_Y, SC, 1, pose="dream", marks=False))
    sc.add("jsleep", [sleep_fr, sleep_fr2], z=2.5, frame_at=lambda t: 0.0 if (t % 2.4) < 1.6 else 1.0,
           motion=M.combine(M.breathe(0.018, 2.4, pivot=(JS_X, JS_Y)), show(0, t_swap)))
    e_p = "proud"
    jfr = [jos("talk", e_p), jos("explain", e_p), jos("stand", e_p), jos("stand", "surprised"),
           jos("stand", "worried"), jos("stand", blink_expr("worried")), jos("talk", "happy"),
           jos("stand", blink_expr("surprised"))]
    t_explain = snap(when(ctx, "向我的麦捆") - 0.05)
    t_jstand = snap(L1.end + 0.15)
    t_jsurp = snap(t_angry + 0.25)
    t_jworry = snap(t_scold + 0.55)
    jbase = [(0, 6), (t_swap, 0), (t_explain, 1), (t_jstand, 2), (t_jsurp, 3), (t_jworry, 4)]
    jbase = with_blinks(jbase, {4: 5, 3: 7}, [t_jsurp + 1.1, t_jworry + 1.6, T - 0.8])
    sprite(sc, "joseph", 3.0, jfr, (J_X, GY), base=jbase,
           bumps=[happy_hop(snap(t_bow + 0.25), SC, (J_X, GY), 16), dip(t_explain, SC, (J_X, GY), 5),
                  dip(t_jstand, SC, (J_X, GY), 4), dip(t_jsurp, SC, (J_X, GY), 7), dip(t_jworry, SC, (J_X, GY), 9),
                  nod(t_all + 0.3, (J_X, GY), 3, 0.5), nod(t_explain + 0.6, (J_X, GY), 3, 0.5),
                  hop(t_jworry + 0.1, [(0, {"sy": 1}), (0.4, {"sy": 0.975}), (T, {"sy": 0.975})], (J_X, GY))],
           breathe=(0.012, 2.6, 0.1), extra=show(t_swap))
    jh = C.body_points(C.joseph, J_X, GY, SC, 1, pose="talk")["head"]
    sc.add("jarcs", [doc(arcs_markup(jh[0] + 62, jh[1] + 16, 1, k, 1.2)) for k in (1, 2, 3)], z=3.05, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_wide0 + 0.4, L1.end - 0.1))

    # ---------------- the brothers (appear off camera; listen; jealous at the bow; cross arms; Simeon scolds)
    t_jeal = snap(t_bow + 0.35)
    vs_back = [(v, x, GY_B, SC * 0.95, -1) for v, x in BACK]
    vs_front = [(v, x, GY, SC, -1) for v, x in FRONT[1:]]
    sp_v, sp_x = FRONT[0]
    rows = []
    for name, vs, z, ph in (("bros_back", vs_back, 3.3, 0.3), ("bros_front", vs_front, 3.5, 0.6)):
        fr = [bros_markup([(v, x, gy, s, f, "stand", "neutral") for v, x, gy, s, f in vs]),
              bros_markup([(v, x, gy, s, f, "stand", "jealous") for v, x, gy, s, f in vs]),
              bros_markup([(v, x, gy, s, f, "cross_arms", "angry") for v, x, gy, s, f in vs]),
              bros_markup([(v, x, gy, s, f, "stand", blink_expr("neutral")) for v, x, gy, s, f in vs]),
              bros_markup([(v, x, gy, s, f, "cross_arms", blink_expr("angry")) for v, x, gy, s, f in vs])]
        cx = sum(x for _, x, *_ in vs) / len(vs)
        d_ang = t_angry + (0.0 if name == "bros_front" else 0.12)
        base = with_blinks([(0, 0), (t_jeal + ph * 0.3, 1), (snap(d_ang), 2)], {0: 3, 2: 4},
                           [t_wide1 + 0.3 + ph, d_ang + 1.6 + ph, T - 1.0 - ph])
        sprite(sc, name, z, fr, (cx, GY), base=base,
               bumps=[stomp(snap(d_ang), SC, (cx, GY), 9), dip(snap(t_jeal + ph * 0.3), SC, (cx, GY), 4),
                      nod(t_scold + 0.5 + ph, (cx, GY), -2, 0.6)],
               breathe=(0.008, 2.9, ph), extra=show(t_swap, fade=0.4))
        rows.append(cx)
    # the speaker (Simeon): steps toward Joseph and points
    n_st = 2
    st = -80.0
    sp_end = sp_x + n_st * st

    def spk(pose, expr):
        return C.ground_shadow(sp_end, GY, SC, 120) + C.brothers(sp_end, GY, SC, -1, variant=sp_v, pose=pose,
                                                                  expr=expr, staff=False)
    sfr = [spk("walk_a", "angry"), spk("walk_b", "angry"), spk("stand", "neutral"), spk("stand", "jealous"),
           spk("cross_arms", "angry"), spk("point", "angry"), spk("stand", blink_expr("neutral")),
           spk("cross_arms", blink_expr("angry")), spk("talk", "angry")]
    t_step = snap(t_scold - 0.05)
    t_point = snap(t_step + n_st * WALK_P)
    t_talk2 = snap(when(ctx, "管我们") - 0.1)
    t_sp_back = snap(L3.end + 0.45)
    sbase = [(0, 2), (t_jeal, 3), (t_angry, 4), (t_point, 5), (t_talk2, 8), (t_sp_back, 4)]
    sbase = with_blinks(sbase, {2: 6, 4: 7}, [t_wide1 + 0.7, t_angry + 1.2, T - 0.7])
    sprite(sc, "speaker", 3.7, sfr, (sp_end, GY), base=sbase, walks=[(t_step, n_st, st, 0)],
           start_off=-n_st * st,
           bumps=[stomp(t_angry, SC, (sp_end, GY), 9), dip(t_jeal, SC, (sp_end, GY), 4), dip(t_point, SC, (sp_end, GY), 8),
                  dip(t_talk2, SC, (sp_end, GY), 6), dip(t_sp_back, SC, (sp_end, GY), 5),
                  nod(t_point + 0.45, (sp_end, GY), -4, 0.4), nod(t_point + 1.0, (sp_end, GY), -4, 0.4)],
           breathe=(0.01, 2.7, 0.45), extra=show(t_swap, fade=0.4))
    sh = C.body_points(C.brothers, sp_end, GY, SC, -1, variant=sp_v, pose="point")["head"]
    sc.add("sarcs", [doc(arcs_markup(sh[0] - 58, sh[1] + 18, -1, k, 1.2)) for k in (1, 2, 3)], z=3.75, wc=0,
           frame_at=lambda t: float(int(t * 7) % 3), motion=show(t_point + 0.05, L3.end))
    # dust at the stomp, grumble clouds over the rows
    for i, (x, gy) in enumerate(((sp_end - n_st * st, GY), (rows[1], GY), (rows[0], GY_B))):
        sc.add(f"dust{i}", doc(dust_markup(x, gy + 4, 220 if i else 120, seed=i + 3)), z=3.8, wc=0.3,
               motion=dust_motion(t_angry + 0.02 + 0.06 * i, (x, gy)))
    for i, (x, y) in enumerate(((1610, 640), (1870, 630), (sp_end + 10, 665))):
        sc.add(f"grumble{i}", [doc(grumble_markup(x, y, 0.62, seed=k + 3 * i)) for k in range(3)], z=3.9, wc=0.2,
               frame_at=lambda t: float(int(t * 6) % 3),
               motion=M.combine(pop_in(t_angry + 0.15 + 0.1 * i, (x, y)), pop_out(t_scold + 0.3 + 0.1 * i, (x, y)),
                                M.bob(4, 1.3, i * 0.3)))

    # ---------------- foreground
    sc.add("fg", [fg_svg(k) for k in range(3)], z=4.5, frame_at=lambda t: float(int(t * 2.2) % 3))

    # ---------------- night: shade everything below the bubble; lamp glow in the tent
    sc.add("night_shade", doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="#4a5590"/>'), z=5,
           wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.78 * night(t)))
    sc.add("lamp_lit", doc(PR.oil_lamp(LAMP[0], LAMP[1], 0.64, lit=True)), z=5.05, wc=0.5,
           motion=lambda t: Tf(alpha=night(t)))
    lamp = (LAMP[0] + 30, LAMP[1] - 30)
    sc.add("lamp_glow", doc(tent_glow_markup(lamp[0] - 90, lamp[1] - 30, 300)), z=5.1, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=night(t) * (0.42 + 0.06 * math.sin(t * 7.3) + 0.06 * math.sin(t * 11.1))))

    # ---------------- the dream bubble
    def bub_tf(t):
        a = pop_in(t_bub, (BUB[0], BUB[1] + 120), 0.42, 1.06)(t)
        b = pop_out(t_pop, (BUB[0], BUB[1]), 0.34)(t)
        k = a.sx * b.sx
        piv = (BUB[0], BUB[1] + 120) if t < t_pop else BUB
        return Tf(dy=4 * math.sin(2 * math.pi * t / 3.2), sx=k, sy=k, alpha=a.alpha * b.alpha, px=piv[0], py=piv[1])
    sc.add("bubble", bubble_svg(), z=7, wc=0.35, motion=bub_tf)
    # dream dots: from the sleeper at night, from the standing Joseph in the morning
    head_s = C.body_points(C.joseph, JS_X, JS_Y, SC, 1, pose="dream")["head"]
    for i in range(3):
        mk, (px, py) = bubble_dots_markup(head_s[0] + 20, head_s[1] - 60, i)
        t0 = t_dream + 0.12 * (2 - i)
        sc.add(f"ndot{i}", doc(mk), z=6.9, wc=0.2,
               motion=M.combine(pop_in(t0, (px, py)), pop_out(t_bind - 0.6 + 0.1 * i, (px, py)), M.bob(3, 2.1, i * 0.3)))
        mk, (px, py) = bubble_dots_markup(jh[0] + 30, jh[1] - 70, i)
        t0 = t_wide1 - 0.4 + 0.12 * (2 - i)
        sc.add(f"mdot{i}", doc(mk), z=6.9, wc=0.2,
               motion=M.combine(pop_in(t0, (px, py)), pop_out(t_pop - 0.1 + 0.08 * (2 - i), (px, py)),
                                M.bob(3, 2.1, i * 0.3)))

    piv_b = (BUB[0], BUB[1] + 120)
    # Joseph's sheaf: lies -> rises (bounce) -> glows
    sc.add("halo", halo_svg(), z=7.05, wc=0,
           motion=compose_tf(lambda t: Tf(alpha=M.progress(t, t_glow, t_glow + 0.6, "sine") *
                                          (0.85 + 0.15 * math.sin(t * 3.1)),
                                          sx=1 + 0.03 * math.sin(t * 2.2), sy=1 + 0.03 * math.sin(t * 2.2),
                                          px=RING[0], py=RING[1] - 100), bub_tf, (RING[0], RING[1] - 100), piv_b))
    rises = [0.0, 0.25, 0.5, 0.75, 1.0]
    jsf = [doc(PR.wheat_sheaf(RING[0], RING[1], SHEAF_S, 1, rise=r, seed=11)) for r in rises]
    jsf.append(doc(PR.wheat_sheaf(RING[0], RING[1], SHEAF_S, 1, rise=1.0, glow=0.6, seed=11)))
    t_r = snap(t_rise + 0.15)
    jse = [(0, 0)] + [(snap(t_r + 0.09 * k), k) for k in range(1, 5)] + [(snap(t_glow), 5)]
    local = M.combine(pop_in(t_bind, RING, 0.3, 1.15),
                      hop(t_r + 0.36, [(0, {"sy": 1, "sx": 1}), (0.1, {"sy": 1.12, "sx": 0.94}),
                                       (0.24, {"sy": 0.95, "sx": 1.04}), (0.4, {"sy": 1, "sx": 1})], RING),
                      lambda t: Tf(rot=1.5 * math.sin(t * 2.0) * M.progress(t, t_glow, t_glow + 0.5), px=RING[0],
                                   py=RING[1]))
    sc.add("jsheaf", jsf, z=7.3, frame_at=cuts(jse), motion=compose_tf(local, bub_tf, RING, piv_b), wc=0.8)
    sc.fx.append(FX.sparkles((RING[0] - 170, RING[1] - 280, RING[0] + 170, RING[1] - 40), count=12, t0=t_glow,
                             t1=t_pop, size=(7, 15), drift=-6, seed=41))
    # puff of straw when each sheaf is tied
    sc.add("jpuff", doc(puff_markup(RING[0], RING[1] - 40, 70, 40, seed=2, k=0.45)), z=7.35, wc=0,
           motion=compose_tf(puff_motion(t_bind, (RING[0], RING[1] - 40)), bub_tf, (RING[0], RING[1] - 40), piv_b))

    # brothers' sheaves: pop in lying (spread out) -> stand up -> hop in round -> bow
    ring = ring_positions()
    bows = [0.25, 0.5, 0.75, 1.0]
    for i, (xr, yr, xs, ys, s, f) in enumerate(ring):
        fr = [doc(PR.wheat_sheaf(xr, yr, s, f, rise=r, seed=i)) for r in (0.0, 0.33, 0.67, 1.0)]
        fr += [doc(PR.wheat_sheaf(xr, yr, s, f, bow=b, seed=i)) for b in bows]
        order = [0.0, 0.5, 0.25, 0.75, 0.1, 0.6, 0.35, 0.85, 0.2, 0.7][i]
        tp = t_bind + 0.15 + 0.85 * order
        ts = snap(t_all + 0.12 + 0.35 * order)
        tg = t_gather + 0.45 * order
        tb = snap(t_bow + 0.18 * (abs(xr - RING[0]) / 255))
        ent = [(0, 0), (ts, 1), (snap(ts + 0.09), 2), (snap(ts + 0.18), 3)]
        ent += [(snap(tb + 0.08 * k), 4 + k) for k in range(4)]
        dxs, dys = xs - xr, ys - yr

        def loc(t, tp=tp, tg=tg, dxs=dxs, dys=dys, xr=xr, yr=yr, s=s):
            u = M.progress(t, tg, tg + 0.7, "inout")
            hopy = -26 * s * abs(math.sin(2 * math.pi * min(1.0, max(0.0, (t - tg) / 0.7))))
            a = pop_in(tp, (xr, yr), 0.28, 1.15)(t)
            return Tf(dx=dxs * (1 - u), dy=dys * (1 - u) + hopy, sx=a.sx, sy=a.sy, alpha=a.alpha, px=xr + dxs * (1 - u),
                      py=yr + dys * (1 - u))

        def loc2(t, loc=loc, xr=xr, yr=yr):
            v = loc(t)
            # rewrite as scale about the (moving) base: p' = base + (p - xr)*s + d   ->  pivot (xr, yr) scale, shift
            return Tf(dx=v.dx, dy=v.dy, sx=v.sx, sy=v.sy, alpha=v.alpha, px=xr, py=yr)
        sc.add(f"sheaf{i}", fr, z=7.1 + 0.02 * i + (0.3 if yr > RING[1] else 0.0), frame_at=cuts(ent),
               motion=compose_tf(loc2, bub_tf, (xr, yr), piv_b), wc=0.8)
        sc.add(f"spuff{i}", doc(puff_markup(xs, ys - 30, 60, 32, seed=10 + i, k=0.4)), z=7.6, wc=0,
               motion=compose_tf(puff_motion(tp, (xs, ys - 30)), bub_tf, (xs, ys - 30), piv_b))
    # pop sparkle when the bubble bursts
    sc.add("bub_puff", doc(puff_markup(BUB[0], BUB[1], BW * 0.42, BH * 0.4, seed=5, k=1.0)), z=7.9, wc=0,
           motion=puff_motion(t_pop + 0.12, BUB))
    sc.fx.append(FX.sparkles((BUB[0] - 420, BUB[1] - 220, BUB[0] + 420, BUB[1] + 220), count=18, t0=t_pop + 0.05,
                             t1=t_pop + 1.2, size=(8, 16), drift=-20, seed=43))
    sc.fx.append(FX.sparkles((BUB[0] - 300, BUB[1] - 200, BUB[0] + 300, BUB[1] + 120), count=10, t0=t_bub,
                             t1=t_bub + 1.6, size=(6, 12), drift=-10, seed=44))

    # ---------------- sound
    sc.sfx("night", 0.0, dur=t_dawn1, gain_db=-17, fade_in=0.6, fade_out=1.2)
    sc.sfx("snore", 0.4, dur=t_dream - 0.4, gain_db=-24, fade_in=0.4, fade_out=0.5)
    for i in range(3):
        sc.sfx("pop", t_dream + 0.12 * i, gain_db=-17 + i)
    sc.sfx("chime", t_bub, gain_db=-13)
    sc.sfx("pop", t_bind, gain_db=-12)
    for i, (xr, *_r) in enumerate(ring):
        order = [0.0, 0.5, 0.25, 0.75, 0.1, 0.6, 0.35, 0.85, 0.2, 0.7][i]
        if i % 2 == 0:
            sc.sfx("pop", t_bind + 0.15 + 0.85 * order, gain_db=-15, pan=(xr - RING[0]) / 600)
    sc.sfx("grow", t_r - 0.05, gain_db=-12)
    sc.sfx("sparkle", t_glow, gain_db=-12)
    sc.sfx("birds", t_dawn0 + 1.0, dur=T - t_dawn0 - 1.0, gain_db=-21, fade_in=1.5, fade_out=1.0)
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-23, fade_in=0.8, fade_out=1.0)
    sc.sfx("whoosh", t_gather, gain_db=-17)
    sc.sfx("chime", t_bow, gain_db=-15)
    sc.sfx("pop", t_pop + 0.12, gain_db=-10)
    sc.sfx("thud", t_angry, gain_db=-9, pan=0.4)
    sc.sfx("cloth", t_angry + 0.05, gain_db=-14, pan=0.4)
    sc.sfx("footsteps", t_step, dur=n_st * WALK_P + 0.1, gain_db=-17, pan=0.3)
    return sc
