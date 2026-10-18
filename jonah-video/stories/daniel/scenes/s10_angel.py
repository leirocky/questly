"""Scene 10 — the night in the lions' den: God's angel shuts the lions' mouths (Daniel 6:22).

Inside the den (one 2112 x 1188 stage, drawn here): a vault of rounded field stones, the mouth in the ceiling
sealed by the stone (thin slivers of moonlight round its edge), a straw-strewn sandy floor, boulders framing the
corners. Daniel sits in the middle; three big friendly picture-book lions.

  line 0 '狮子坑里黑黑的。'          very dim blue-violet darkness; Daniel sits quietly in the middle; three lions
                                      lie in the shadows at the sides.
         '大狮子们慢慢地走过来，'   one after the other the lions get up (squash, pose cut) and pad slowly toward
                                      him (planted-paw strides); Daniel folds his hands and prays (calm).
         '围在但以理身边。'          they stand round him: the lioness in front-left, a big lion behind him (he
                                      walked round behind Daniel), another in front-right; two open their mouths a
                                      little (tense, never scary: blunt teeth, round friendly faces).
  line 1 '可是，上帝派了天使来，'    God's angel comes as light: a warm glow blooms above Daniel, soft rays turn,
                                      and two soft wing-shaped lights unfold (no figure); the den turns warm.
         '封住了狮子的口。'          a soft gleam touches each open mouth in turn and it closes into a smile.
  line 2 '狮子们一个个乖乖地趴下来，' one by one the lions lie down like big sleepy cats (squash, pose cut).
         '一口也没有咬但以理。'      Daniel opens his eyes and smiles; the lions blink happily, one dozes off.
  line 3 '但以理在上帝的保护中，'    the wing-lights come down and fold round them all like a shelter of light.
         '平平安安地过了一夜。'      Daniel leans back against the big lion's side and closes his eyes; the lions
                                      sleep (little z's); the moonlight slivers fade (the night goes by). Calm,
                                      softly lit hold for the dissolve into dawn (s11).

God is never drawn: the angel is only light and soft wing shapes. Sparkles stay above the faces.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import lut_tint, phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap, step_walk
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]
FY = 985                    # Daniel's seat on the floor
DX = 1030                   # Daniel (sitting, facing left, his back to the right)
DS = 1.25
AX, AY = 1090, 350          # the angel's light
HOLE = (700, 96)            # the sealed mouth in the ceiling


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


def swap(t_on, t_off):
    return lambda t: Tf(alpha=1.0 if t_on <= t < t_off else 0.0)


# ============================================================================ the den


STONE_COLS = ["#6a5e74", "#5f566e", "#726478", "#6c5e60", "#5a5266", "#74665e", "#625a70"]


def den_svg():
    """Back wall (rounded field stones), the vaulted ceiling with the sealed mouth, the floor (static)."""
    rng = random.Random(10)
    defs = S.lin_grad("s10bg", [(0, "#241e30"), (1, "#3a3046")])
    defs += S.lin_grad("s10floor", [(0, "#6e5e56"), (0.5, "#80705e"), (1, "#8a7660")])
    defs += S.lin_grad("s10vault", [(0, "#140f1c", 0.85), (0.55, "#1a1424", 0.35), (1, "#1a1424", 0)])
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#s10bg)"/>'
    stones = ""
    yy = -30
    row = 0
    while yy < 900:
        h = rng.uniform(56, 96)
        xx = -80 - rng.uniform(0, 60)
        while xx < W + 80:
            w = rng.uniform(80, 200)
            col = rng.choice(STONE_COLS)
            hh = h * rng.uniform(0.8, 1.0)
            stones += S.path(S.blob(xx + w / 2, yy + h / 2 + rng.uniform(-4, 4), w / 2 - 5, hh / 2 - 5, 0.12, 9,
                                    seed=int(xx * 3 + yy * 7)),
                             fill=col, sw=0, extra=f'stroke="#2e2638" stroke-width="4"')
            # a soft highlight on top of each stone
            stones += (f'<path d="M{f1(xx + w * 0.25)},{f1(yy + h * 0.3)} Q{f1(xx + w / 2)},{f1(yy + h * 0.16)} '
                       f'{f1(xx + w * 0.72)},{f1(yy + h * 0.3)}" stroke="{S.shade(col, 0.2)}" stroke-width="4" '
                       f'fill="none" stroke-linecap="round" opacity="0.7"/>')
            xx += w + rng.uniform(3, 8)
        yy += h + 4
        row += 1
    body += stones
    # bigger rocks along the foot of the wall
    for i, x in enumerate(range(-40, W + 80, 230)):
        rx, ry = rng.uniform(80, 130), rng.uniform(40, 62)
        body += S.path(S.blob(x + rng.uniform(-40, 40), 880 - ry * 0.4, rx, ry, 0.12, 10, seed=50 + i), fill="#584e60",
                       sw=0, extra='stroke="#2e2638" stroke-width="4"')
    # vault shading toward the ceiling and the side walls curving in
    body += f'<rect x="-20" y="-20" width="{W + 40}" height="560" fill="url(#s10vault)"/>'
    body += (f'<path d="M-20,-20 L380,-20 Q120,200 90,900 L-20,900 Z" fill="#1a1424" opacity="0.55" '
             f'filter="url(#blur-md)"/>'
             f'<path d="M{W + 20},-20 L{W - 380},-20 Q{W - 120},200 {W - 90},900 L{W + 20},900 Z" fill="#1a1424" '
             f'opacity="0.55" filter="url(#blur-md)"/>')
    # the sealed mouth in the ceiling: the dark shaft, the underside of the stone, a sliver of moonlight
    hx, hy = HOLE
    body += f'<ellipse cx="{hx}" cy="{hy}" rx="170" ry="62" fill="#120e18" stroke="{INK}" stroke-width="4"/>'
    body += f'<ellipse cx="{hx + 6}" cy="{hy - 4}" rx="150" ry="50" fill="#6c6470" stroke="{INK}" stroke-width="3"/>'
    body += (f'<path d="M{hx - 120},{hy + 12} Q{hx},{hy + 40} {hx + 130},{hy + 8}" stroke="#4e4858" stroke-width="10" '
             f'fill="none" stroke-linecap="round"/>')
    # floor
    floor = (f"M-20,880 Q500,858 {W / 2},862 Q{W - 500},858 {W + 20},880 L{W + 20},{H + 20} L-20,{H + 20} Z")
    body += S.path(floor, fill="url(#s10floor)", sw=4)
    straw = ""
    for _ in range(170):
        px, py = rng.uniform(0, W), rng.uniform(880, H)
        a = rng.uniform(-0.6, 0.6) + (math.pi if rng.random() < 0.5 else 0)
        ln = rng.uniform(18, 36) * (0.7 + (py - 880) / 600)
        col = S.mix(P["leaf_dry"], P["sand"], rng.uniform(0, 0.6))
        straw += (f'<path d="M{f1(px)},{f1(py)} L{f1(px + ln * math.cos(a))},{f1(py + ln * math.sin(a) * 0.4)}" '
                  f'stroke="{col}" stroke-width="3.2" stroke-linecap="round" opacity="0.85"/>')
    for _ in range(18):
        px, py = rng.uniform(0, W), rng.uniform(890, H)
        r = rng.uniform(6, 13)
        straw += (f'<path d="{S.blob(px, py, r * 1.6, r, 0.15, 7, seed=int(px))}" fill="#6a5c58" '
                  f'stroke="{INK}" stroke-width="2.5"/>')
    body += straw
    return doc(S.g(body, filter="wobble"), defs)


def moon_slivers_svg():
    """Thin moonlight round the edge of the sealing stone (additive)."""
    hx, hy = HOLE
    body = (f'<path d="M{hx - 156},{hy - 2} Q{hx - 150},{hy - 50} {hx - 40},{hy - 58}" stroke="#4a5a7a" '
            f'stroke-width="10" fill="none" stroke-linecap="round" filter="url(#soft)"/>'
            f'<path d="M{hx + 60},{hy - 58} Q{hx + 150},{hy - 50} {hx + 160},{hy}" stroke="#4a5a7a" stroke-width="8" '
            f'fill="none" stroke-linecap="round" filter="url(#soft)"/>'
            f'<path d="M{hx - 150},{hy} L{hx - 260},{H * 0.7} L{hx - 120},{H * 0.7} Z" fill="#1c2232" '
            f'filter="url(#blur-lg)"/>')
    return doc(body)


def front_svg():
    """Boulders and straw in the bottom corners (in front of everyone)."""
    body = ""
    for cx, cy, rx, ry, sd in ((60, 1120, 170, 110, 1), (240, 1170, 110, 64, 2), (W - 60, 1110, 180, 120, 3),
                               (W - 250, 1175, 100, 56, 4), (-30, 960, 120, 160, 5), (W + 30, 950, 120, 170, 6)):
        body += S.path(S.blob(cx, cy, rx, ry, 0.1, 10, seed=sd), fill="#5e5466", sw=4.5)
        body += (f'<path d="M{f1(cx - rx * 0.5)},{f1(cy - ry * 0.5)} Q{f1(cx)},{f1(cy - ry * 0.85)} '
                 f'{f1(cx + rx * 0.45)},{f1(cy - ry * 0.55)}" stroke="#7a7082" stroke-width="5" fill="none" '
                 f'stroke-linecap="round"/>')
    rng = random.Random(3)
    for _ in range(18):
        px = rng.choice((rng.uniform(150, 420), rng.uniform(W - 420, W - 150)))
        py = H - rng.uniform(10, 40)
        for _j in range(3):
            a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
            ln = rng.uniform(18, 34)
            body += (f'<path d="M{f1(px)},{f1(py)} L{f1(px + ln * math.cos(a))},{f1(py + ln * math.sin(a))}" '
                     f'stroke="{S.mix(P["leaf_dry"], P["sand"], 0.3)}" stroke-width="3.4" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble"))


def wing_svg(side):
    """One soft wing of light rising from beside the glow (no figure): a rounded leading edge, five scalloped
    feather tips, a few feather lines. Drawn for the right wing (side=1) and mirrored for the left."""
    sx0, sy0 = AX + side * 34, AY + 24
    outline = ("M0,0 C40,-170 150,-330 300,-430 C340,-458 376,-420 352,-372 Q384,-330 336,-300 Q372,-250 316,-228 "
               "Q348,-170 284,-160 Q302,-100 236,-98 Q238,-40 170,-44 Q160,10 100,4 Q70,40 30,30 Q8,22 0,0 Z")
    lines = ("M20,-10 Q160,-200 330,-380 M30,0 Q170,-150 320,-300 M40,8 Q180,-100 296,-200 M46,16 Q160,-50 250,-120 "
             "M46,24 Q130,-10 190,-60")
    tf = f"translate({sx0},{sy0}) scale({side},1)"
    body = (f'<g transform="{tf}"><path d="{outline}" fill="url(#s10wing)" filter="url(#soft)"/>'
            f'<path d="{outline}" fill="none" stroke="#7a6038" stroke-width="5"/>'
            f'<path d="{lines}" fill="none" stroke="#3e2e18" stroke-width="4" stroke-linecap="round" '
            f'filter="url(#soft)"/></g>')
    defs = (f'<radialGradient id="s10wing" gradientUnits="userSpaceOnUse" cx="40" cy="0" r="520">'
            f'<stop offset="0" stop-color="#9a7a44"/><stop offset="0.55" stop-color="#7a5e34"/>'
            f'<stop offset="1" stop-color="#4a3820"/></radialGradient>')
    return doc(body, defs)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2, L3 = (ctx.line(i) for i in range(4))

    t_come = L0.at("大狮子们")                       # '大狮子们慢慢地走过来'
    t_round = L0.at("围在但以理身边")
    t_angel = phrase_t(L1, "上帝派了天使来")
    t_shut = phrase_t(L1, "封住了狮子的口")
    t_down = L2.start                               # '狮子们一个个乖乖地趴下来'
    t_nobite = L2.at("一口也没有咬")
    t_safe = L3.start                               # '但以理在上帝的保护中'
    t_night = L3.at("平平安安地过了一夜")

    # ---------------------------------------------------------------- the den
    sc.add("den", den_svg(), seed=5)
    sc.add("slivers", moon_slivers_svg(), wc=0, blend="add",
           motion=M.keys([(0, {"alpha": 1.0}), (t_angel, {"alpha": 1.0}), (t_angel + 1.5, {"alpha": 0.5}),
                          (T - 1.0, {"alpha": 0.15})], "sine"))

    # warm pool of light on the floor and wall round the group (comes with the angel)
    pool = (f'<ellipse cx="{DX + 80}" cy="{FY - 20}" rx="760" ry="200" fill="url(#s10pool)"/>'
            f'<ellipse cx="{AX}" cy="{AY + 260}" rx="760" ry="560" fill="url(#s10wall)"/>')
    pdefs = (S.rad_grad("s10pool", [(0, "#5a4224", 1), (0.6, "#3a2a14", 0.6), (1, "#000000", 0)]) +
             S.rad_grad("s10wall", [(0, "#4a361c", 1), (0.5, "#2e2010", 0.6), (1, "#000000", 0)]))
    sc.add("pool", doc(pool, pdefs), wc=0, blend="add",
           motion=M.keys([(t_angel - 0.2, {"alpha": 0}), (t_angel + 1.6, {"alpha": 0.9}), (t_safe, {"alpha": 0.9}),
                          (t_safe + 1.5, {"alpha": 1.0}), (T, {"alpha": 0.85})], "sine"))

    # ---------------------------------------------------------------- the angel: light, rays, wings
    core_defs = S.rad_grad("s10core", [(0, "#fff0c8", 1), (0.12, "#f8d890", 0.85), (0.4, "#d8a050", 0.35),
                                       (1, "#a06020", 0)])
    sc.add("core", doc(f'<circle cx="{AX}" cy="{AY}" r="300" fill="url(#s10core)"/>', core_defs), wc=0, blend="add",
           motion=M.combine(M.keys([(t_angel - 0.1, {"alpha": 0, "s": 0.2}), (t_angel + 0.9, {"alpha": 0.95, "s": 1.0}),
                                    (t_safe, {"alpha": 0.9}), (T, {"alpha": 0.7, "s": 0.9})],
                                   ["out", "linear", "sine"], pivot=(AX, AY)),
                            M.breathe(0.04, 2.6, pivot=(AX, AY))))
    rays = S.path(S.rays(AX, AY, 70, 620, n=16, width_deg=5), fill="url(#s10ray)", stroke=False,
                  extra='filter="url(#blur-md)"')
    ray_defs = (f'<radialGradient id="s10ray" gradientUnits="userSpaceOnUse" cx="{AX}" cy="{AY}" r="620">'
                f'<stop offset="0.1" stop-color="#7a5a2a"/><stop offset="1" stop-color="#7a5a2a" stop-opacity="0"/>'
                f'</radialGradient>')
    sc.add("rays", doc(rays, ray_defs), wc=0, blend="add", motion=M.combine(
        M.keys([(t_angel + 0.1, {"alpha": 0, "s": 0.6}), (t_angel + 1.3, {"alpha": 0.6, "s": 1.0}),
                (T, {"alpha": 0.35})], ["out", "sine"], pivot=(AX, AY)),
        lambda t: Tf(rot=3.0 * t, px=AX, py=AY)))
    # wings: unfold from folded (tips down) on the angel's coming; come down round everyone on '保护中'
    for side in (-1, 1):
        sp = (AX + side * 34, AY + 24)
        sc.add(f"wing{side}", wing_svg(side), wc=0, blend="add", motion=M.combine(
            M.keys([(t_angel + 0.3, {"alpha": 0, "rot": side * 70, "s": 0.5}),
                    (t_angel + 1.8, {"alpha": 0.95, "rot": 0, "s": 1.0}),
                    (t_safe + 0.2, {"alpha": 0.95, "rot": 0, "s": 1.0, "dy": 0}),
                    (t_safe + 2.6, {"alpha": 0.72, "rot": side * 76, "s": 1.32, "dy": 70, "dx": -side * 46}),
                    (T, {"alpha": 0.64, "rot": side * 78, "s": 1.34, "dy": 74, "dx": -side * 48})],
                   ["out", "linear", "inout", "sine"], pivot=sp),
            lambda t, side=side: Tf(rot=side * 2.5 * math.sin(2 * math.pi * t / 3.6), px=sp[0], py=sp[1])))

    # ---------------------------------------------------------------- lions
    # name: (variant, scale, lane y, facing, x start (lying), x end, t get-up, n strides, mouth opens?)
    lions = {
        "lioness": (1, 1.0, FY + 22, 1, 130, 565, t_come + 0.05, 8, True),
        "lionB": (0, 1.0, FY - 52, 1, 520, 1110, t_come + 0.3, 11, False),
        "lionA": (0, 1.08, FY + 36, -1, 1990, 1660, t_come + 0.75, 6, True),
    }
    shut_t = {"lionA": t_shut + 0.15, "lioness": t_shut + 0.85, "lionB": t_shut + 0.5}
    lie_t = {"lioness": t_down + 0.25, "lionA": t_down + 1.0, "lionB": t_down + 1.75}
    doze_t = {"lionA": t_nobite + 0.9, "lioness": t_night + 0.4, "lionB": t_night + 0.9}
    open_t = {"lionA": t_round + 0.55, "lioness": t_round + 0.95}
    lion_heads = {}
    for name, (var, ls, ly, fc, x0, x1, t_get, n, opens) in lions.items():
        LP = 0.3
        step = abs(x1 - x0) / n
        w_fa, w_dx, w_dy, w_end = step_walk(snap(t_get + 0.3), n, step, LP, ls)
        frames = [doc(PR.lion(x1, ly, ls, fc, pose="lie", variant=var)),                     # 0 lying, start
                  doc(PR.lion(x1, ly, ls, fc, pose="stand", variant=var)),                   # 1
                  doc(PR.lion(x1, ly, ls, fc, pose="walk_a", variant=var)),                  # 2
                  doc(PR.lion(x1, ly, ls, fc, pose="walk_b", variant=var)),                  # 3
                  doc(PR.lion(x1, ly, ls, fc, pose="stand", variant=var, mouth=0.33)),       # 4 mouth open a bit
                  doc(PR.lion(x1, ly, ls, fc, pose="stand", variant=var, eyes="happy")),     # 5 mouth shut, smiling
                  doc(PR.lion(x1, ly, ls, fc, pose="lie", variant=var, eyes="happy")),       # 6 lying, content
                  doc(PR.lion(x1, ly, ls, fc, pose="sleep", variant=var, tail=0.3))]         # 7 asleep
        t_stand_end = w_end
        base = [(0, 0), (snap(t_get), 1), (t_stand_end, 1)]
        if opens:
            base.append((snap(open_t[name]), 4))
        base += [(snap(shut_t[name]), 5), (snap(lie_t[name]), 6), (snap(doze_t[name]), 7)]
        base_fa = cuts(base)

        def fa(t, w_fa=w_fa, base_fa=base_fa):
            f = w_fa(t)
            return 2.0 + f if f is not None else base_fa(t)
        D0 = x0 - x1
        sgn = 1 if x1 > x0 else -1

        def mv(t, D0=D0, sgn=sgn, w_dx=w_dx, w_dy=w_dy):
            return Tf(dx=D0 + sgn * w_dx(t), dy=w_dy(t))
        pv = (x1, ly)
        sc.add("sh_" + name, doc(C.ground_shadow(x1, ly, ls, 430, 0.35)), motion=lambda t, mv=mv: Tf(dx=mv(t).dx))
        sc.add(name, frames, frame_at=fa, motion=M.combine(
            mv, dip(snap(t_get), ls, pv, 10), dip(snap(lie_t[name]), ls, pv, 12), dip(snap(doze_t[name]), ls, pv, 6),
            hop(snap(shut_t[name]), [(0, {"sy": 1.0}), (0.12, {"sy": 1.03}), (0.3, {"sy": 1.0})], pv),
            M.breathe(0.014, 2.6 + 0.25 * var + ls, pivot=pv, phase=x1 / 997.0)))
        lion_heads[name] = (x1 + fc * 150 * ls, ly - 240 * ls)

    # ---------------------------------------------------------------- Daniel
    t_pray = snap(t_come + 1.1)
    t_smile = snap(t_nobite + 0.1)
    t_lean = snap(t_night + 0.15)
    dframes = [doc(C.daniel(DX, FY, DS, -1, pose="sit", expr="neutral")),
               doc(C.daniel(DX, FY, DS, -1, pose="sit_pray")),
               doc(C.daniel(DX, FY, DS, -1, pose="sit", expr="happy")),
               doc(C.daniel(DX, FY, DS, -1, pose="sit", expr="peaceful"))]
    dp = (DX + 10, FY)
    lean = M.keys([(t_lean, {"rot": 0}), (t_lean + 0.5, {"rot": 5.0})], "out", pivot=dp)
    sc.add("sh_daniel", doc(C.ground_shadow(DX, FY, DS, 230, 0.4)))
    sc.add("daniel", dframes, frame_at=cuts([(0, 0), (t_pray, 1), (t_smile, 2), (t_lean, 3)]),
           motion=M.combine(lean, dip(t_pray, DS, dp, 7), dip(t_smile, DS, dp, 6), dip(t_lean, DS, dp, 6),
                            M.breathe(0.01, 3.4, pivot=dp)))
    # z-order: lioness and lionA in front of Daniel, lionB behind him
    zd = next(l.z for l in sc.layers if l.name == "sh_daniel")
    for l in sc.layers:
        if l.name in ("lionB", "sh_lionB"):
            l.z = zd - (0.2 if l.name == "lionB" else 0.3)
        if l.name in ("lioness", "sh_lioness", "lionA", "sh_lionA"):
            l.z += 10

    # gleams on the lions' mouths ('封住了狮子的口'): a soft warm touch, then the smile
    for name in ("lionA", "lioness"):
        var, ls, ly, fc, x0, x1, *_ = lions[name]
        mx_, my_ = x1 + fc * 168 * ls, ly - 196 * ls
        g = doc(f'<circle cx="{f1(mx_)}" cy="{f1(my_)}" r="70" fill="url(#s10gl)"/>',
                S.rad_grad("s10gl", [(0, "#a08048", 1), (0.5, "#6a5028", 0.5), (1, "#000000", 0)]))
        ts = shut_t[name]
        sc.add("gleam_" + name, g, wc=0, blend="add", z=30,
               motion=M.keys([(ts - 0.35, {"alpha": 0, "s": 0.4}), (ts, {"alpha": 1.0, "s": 1.0}),
                              (ts + 0.9, {"alpha": 0, "s": 1.3})], ["out", "sine"], pivot=(mx_, my_)))

    # little z's over the dozing lions
    for name, dx_ in (("lionA", -10), ("lioness", 20)):
        var, ls, ly, fc, x0, x1, *_ = lions[name]
        hx_, hy_ = x1 + fc * 150 * ls + dx_, ly - 200 * ls
        tz = doze_t[name] + 0.4
        zs = "".join(S.text(hx_ + 22 * i, hy_ - 34 * i, "z", size=34 + 8 * i, fill="#e8dcc0",
                            extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"') for i in range(3))
        sc.add("z_" + name, doc(zs), wc=0, z=31, motion=M.combine(
            M.keys([(tz, {"alpha": 0}), (tz + 0.5, {"alpha": 0.9})], "sine"), M.bob(5, 2.4, 0.3)))

    sc.add("front", front_svg(), z=40, seed=21)

    # ---------------------------------------------------------------- camera: a slow, continuous push-in
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W)), (t_angel, Cam(1090, 615, 1920)),
                            (T, Cam(1115, 640, 1800))], "sine")

    # ---------------------------------------------------------------- light and fx
    def dark(t):
        return 0.62 - 0.42 * M.progress(t, t_angel - 0.1, t_angel + 1.8, "sine") + 0.06 * M.progress(t, t_night, T)

    def warm(t):
        return 0.16 * M.progress(t, t_angel, t_angel + 1.8, "sine") - 0.04 * M.progress(t, t_night, T)

    faces_top = FY - 300
    sc.fx = [
        lut_tint((96, 92, 150), dark, mode="multiply"),
        lut_tint((255, 214, 150), warm, mode="screen"),
        FX.vignette(lambda t: 0.75 - 0.3 * M.progress(t, t_angel, t_angel + 1.8, "sine")),
        FX.sparkles((AX - 520, AY - 230, AX + 520, faces_top - 80), count=22, t0=t_angel + 0.3,
                    color=(255, 238, 180), size=(8, 18), period=1.8, drift=-6, seed=19),
        FX.motes((300, 150, W - 300, faces_top - 60), count=16, t0=t_angel + 1.0, color=(255, 236, 190),
                 size=(3, 6), alpha=110, seed=8),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("drip", 0, dur=T + 0.1, gain_db=-21, fade_in=0.8, fade_out=0.9, density=0.5)
    sc.sfx("night", 0, dur=T + 0.1, gain_db=-24, fade_in=0.8, fade_out=0.9)
    for name, (var, ls, ly, fc, x0, x1, t_get, n, opens) in lions.items():
        sc.sfx("cloth", snap(t_get), gain_db=-21, pan=(x0 - W / 2) / W)
        sc.sfx("footsteps", snap(t_get + 0.3), dur=n * 0.3, gain_db=-23, fade_in=0.2, fade_out=0.3,
               pan=(x0 - W / 2) / W * 0.8)
    sc.sfx("chime", t_angel - 0.05, gain_db=-8)
    sc.sfx("grow", t_angel + 0.2, gain_db=-16)
    for name in ("lionA", "lionB", "lioness"):
        sc.sfx("sparkle", shut_t[name] - 0.1, gain_db=-17)
    for name in ("lioness", "lionA", "lionB"):
        sc.sfx("thud", snap(lie_t[name]), gain_db=-21)
    sc.sfx("chime", t_safe + 0.1, gain_db=-15)
    sc.sfx("snore", doze_t["lionA"] + 0.3, dur=T - doze_t["lionA"] - 0.2, gain_db=-24, fade_in=1.0, fade_out=0.9)
    return sc
