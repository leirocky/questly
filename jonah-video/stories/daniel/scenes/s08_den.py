"""Scene 8 — Daniel is put into the lions' den, the stone is rolled over it and sealed (Daniel 6:16-17).

One tall 2700 x 1500 stage: an evening sky over the plain outside Babylon (far skyline, hills, two torches on
poles beside the den) and, below the ground line, the den in dollhouse cross-section (props.lion_den, 'den
recipe'): the dim stone chamber with three big friendly lions, the shaft through the ceiling.

  line 0 '国王只好下令，把但以理带来，'   establishing dusk shot: the king stands sadly left of the den mouth
                                         (hand on his forehead); two guards bring Daniel in from the right
                                         (planted-foot walk), Daniel calm and unhurt.
         '放进狮子坑里。'                  at the rim the rope guard braces (pull_rope) and Daniel hops into the
                                         shaft holding the rope (hold_rope, hard cut at the top of the hop).
         '狮子坑很深，里面住着好多大狮子。' he is let down slowly; the camera goes down with him into the den:
                                         a lion lying on the left, a lioness sitting on the right, one asleep.
                                         He lands softly (squash, thud); the lion sits up, curious; the sleeper
                                         peeks. The guards coil up and walk off to the right.
  line 1 (K) '但以理，你一直敬拜的上帝，一定会救你！'  the king steps to the rim and calls down (call_out); the
                                         camera frames both: Daniel looks up at him, happy and calm, and nods.
  line 2 '人们搬来一块大石头，堵住坑口。'  the guards roll a big round stone in from the right (heave-ho surges,
                                         push pose, rolling flipbook); it drops onto the mouth (thud, dust puff);
                                         the evening light in the den goes out.
         '国王用自己的印，在石头上封了印，' a cord is stretched over the stone; the camera pushes in; the king
                                         steps up with his signet ring and presses it into the clay: the royal
                                         seal (pop, warm flash).
         '谁也不能打开。'                  the king steps back, sad; the guards stand watch; the camera pulls back:
                                         dusk turns to night, first stars, and below, in the dark den, Daniel
                                         sits and prays calmly among the lions. Calm hold for the dissolve.

Pose changes are hard cuts hidden at the bottom of a squash dip or at the top of a hop; walkers use the
planted-foot stride (s17 step_walk). All times come from the narration chunks.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import lut_tint, phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap, step_walk
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 2700, 1500
INK = P["ink"]
G = 760                    # ground line (top of the den slab)
HX = 1350                  # den anchor x (centre of the shaft)
DS = 0.8                   # den scale
PS = 0.8                   # people on the surface
FY = G + PR.DEN_FLOOR_Y * DS          # den floor (1240)
HOLE = PR.DEN_OPENING[1] * DS         # half-width of the shaft (112)
CEIL = G + PR.DEN_INNER[1] * DS       # chamber ceiling underside (837)
STEP = 85 * PS                        # one stride

KX0 = HX - 460             # the king's first spot (watching, sad)
KX1 = KX0 + 3 * STEP       # at the rim, calling down
KX2 = KX1 + STEP           # beside the stone, sealing it
DR = HX + 150              # Daniel stops at the right rim
G1X, G2X = HX + 350, HX + 530         # the rope guard and the spear guard stop here
RIM = (HX + HOLE, G + 2)              # the rope runs over this corner of the mouth
DFX = HX - 8                          # Daniel's x in the shaft and on the floor
STONE_R = PR.DEN_STONE_R[0] * DS      # 136
STONE_Y = G + 8 * DS


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


def swap(t_on, t_off):
    return lambda t: Tf(alpha=1.0 if t_on <= t < t_off else 0.0)


def clamp_cam(c, margin=4):
    h = c.w * 9 / 16
    return Cam(min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin),
               min(max(c.y, h / 2 + margin), SH - h / 2 - margin), c.w)


def rope(points, w=7.0, col="#c9a46a"):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in points)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 4}" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


# ============================================================================ backdrops


def sky_svg():
    defs = S.lin_grad("s8sky", [(0, "#36396a"), (0.32, "#5d4f86"), (0.58, "#a7709a"), (0.8, "#e79a7c"),
                                (1, "#f5c486")])
    defs += S.rad_grad("s8sun", [(0, "#ffe0a6", 0.9), (0.4, "#f8bb84", 0.45), (1, "#f19a78", 0)])
    body = f'<rect x="-20" y="-20" width="{SW + 40}" height="{G - 60}" fill="url(#s8sky)"/>'
    body += f'<ellipse cx="420" cy="{G - 150}" rx="900" ry="300" fill="url(#s8sun)"/>'
    return doc(body, defs)


def night_svg():
    """A deeper night sky laid over the dusk sky as the evening goes on."""
    defs = S.lin_grad("s8night", [(0, "#1f2547", 0.95), (0.45, "#2d3260", 0.85), (0.8, "#5a4b7a", 0.6),
                                  (1, "#8a6b86", 0.35)])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{G - 60}" fill="url(#s8night)"/>', defs)


def moon_svg():
    x, y = 2330, 250
    defs = S.rad_grad("s8moonglow", [(0, "#fff6da", 0.55), (0.5, "#f3e6c8", 0.18), (1, "#f3e6c8", 0)])
    body = f'<circle cx="{x}" cy="{y}" r="190" fill="url(#s8moonglow)"/>'
    body += S.g(f'<circle cx="{x}" cy="{y}" r="58" fill="#f8efd2" stroke="{P["ink_soft"]}" stroke-width="3"/>'
                f'<circle cx="{x - 18}" cy="{y - 12}" r="11" fill="#eadfc0"/>'
                f'<circle cx="{x + 16}" cy="{y + 18}" r="8" fill="#eadfc0"/>', filter="wobble-fine")
    return doc(body, defs)


def clouds_svg():
    body = ""
    for cx, cy, w, h, sd in ((600, 190, 420, 92, 1), (1500, 120, 380, 84, 2), (2150, 240, 340, 74, 3),
                             (1050, 330, 300, 64, 4)):
        body += S.cloud(cx, cy, w, h, fill="#b98aa6", seed=sd, puffs=5, sw=3, shade_fill="#8f6c92")
    return doc(S.g(body, filter="wobble", opacity=0.85))


def far_svg():
    """Hills, Babylon on the horizon (hazy violet), the plain up to the ground line."""
    hz = G - 175
    defs = S.lin_grad("s8plain", [(0, "#a98a8e"), (0.5, "#b99a86"), (1, "#c4a07a")])
    body = S.path(S.hill(-100, 1300, hz + 20, 120, seed=3, bottom=G), fill="#8f7393", sw=3)
    body += S.path(S.hill(1100, 2800, hz + 20, 90, seed=5, bottom=G), fill="#977897", sw=3)
    body += PR.nineveh_skyline(150, 1150, hz + 12, scale=0.42, seed=3, haze=0.62, tint="#9a7c9c")
    body += f'<rect x="-20" y="{hz}" width="{SW + 40}" height="{G - hz + 10}" fill="url(#s8plain)"/>'
    body += S.path(f"M-20,{hz} L{SW + 20},{hz}", sw=3)
    rng = random.Random(8)
    marks = ""
    for _ in range(120):
        x, y = rng.uniform(0, SW), rng.uniform(hz + 12, G - 6)
        w = rng.uniform(16, 44) * (0.45 + (y - hz) / 220)
        marks += f'<path d="M{f1(x)},{f1(y)} q{f1(w / 2)},-3 {f1(w)},0"/>'
    body += (f'<g stroke="#8e6f60" stroke-width="2.5" fill="none" opacity="0.45" stroke-linecap="round">'
             f'{marks}</g>')
    # palms and bushes on the plain, small and far
    deco = PR.palm_tree(260, hz + 40, 0.36, lean=0.06) + PR.palm_tree(2480, hz + 46, 0.4, lean=-0.08)
    deco += PR.palm_tree(2610, hz + 52, 0.3, lean=0.05) + PR.bush(560, hz + 60, 0.35) + PR.bush(2160, hz + 70, 0.38, 1)
    body += S.g(deco, opacity=0.9)
    return doc(S.g(body, filter="wobble"), defs)


def ground_front_svg():
    """Rocks and tufts on the plain near the den (behind the people), and the earth under the ground line."""
    defs = S.lin_grad("s8earth", [(0, "#a8805a"), (0.5, "#8d6748"), (1, "#6e5040")])
    rng = random.Random(21)
    body = f'<rect x="-20" y="{G}" width="{SW + 40}" height="{SH - G + 20}" fill="url(#s8earth)"/>'
    strata = ""
    for k, yy in enumerate(range(G + 70, SH, 80)):
        pts = [(-40, yy + rng.uniform(-10, 10))] + [(x, yy + rng.uniform(-14, 14)) for x in range(300, SW, 450)]
        pts.append((SW + 40, yy))
        strata += S.path(S.smooth_path(pts, closed=False), sw=3, extra=f'stroke="{S.shade("#8d6748", 0.15 if k % 2 else -0.15)}" opacity="0.8"')
    for _ in range(70):
        px, py = rng.uniform(0, SW), rng.uniform(G + 30, SH)
        r = rng.uniform(6, 14)
        strata += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r * 1.4)}" ry="{f1(r)}" '
                   f'fill="{S.shade("#8d6748", rng.choice((-0.2, 0.2)))}" stroke="{INK}" stroke-width="2.5" opacity="0.85"/>')
    body += strata
    body += S.path(f"M-20,{G} L{SW + 20},{G}", sw=4.5)
    deco = ""
    for x, y, s_, v in ((300, G - 30, 0.55, 0), (560, G - 12, 0.4, 1), (2150, G - 20, 0.5, 1), (2440, G - 36, 0.6, 0),
                        (2620, G - 14, 0.4, 2), (130, G - 10, 0.45, 2)):
        deco += PR.grass_tuft(x, y, s_, variant=v)
    for cx, cy, rx, ry in ((420, G - 22, 46, 24), (2300, G - 26, 52, 26), (2000, G - 12, 30, 16), (720, G - 8, 28, 14)):
        deco += S.path(S.blob(cx, cy, rx, ry, 0.12, 9, seed=int(cx)), fill="#b4a090", sw=3.5)
    body += deco
    return doc(S.g(body, filter="wobble"), defs)


TORCHES = ((HX - 640, G - 24), (HX + 720, G - 30))
TS = 0.8


def torch_pole(x, y, s):
    """A wooden pole with a bronze bowl on top (the flame is a separate flipbook)."""
    top = y - 330 * s
    body = (f'<path d="M{f1(x - 8 * s)},{f1(y)} L{f1(x - 6 * s)},{f1(top + 20 * s)} L{f1(x + 6 * s)},{f1(top + 20 * s)} '
            f'L{f1(x + 8 * s)},{f1(y)} Z" fill="{P["wood"]}" {S.STROKE}/>')
    body += (f'<path d="M{f1(x - 34 * s)},{f1(top)} Q{f1(x)},{f1(top + 44 * s)} {f1(x + 34 * s)},{f1(top)} Z" '
             f'fill="#b3833f" {S.STROKE}/>')
    body += f'<ellipse cx="{f1(x)}" cy="{f1(top)}" rx="{f1(34 * s)}" ry="{f1(8 * s)}" fill="#6d4a2a" {S.STROKE_THIN}/>'
    for yy in (y - 40 * s, y - 120 * s):
        body += f'<path d="M{f1(x - 9 * s)},{f1(yy)} L{f1(x + 9 * s)},{f1(yy + 6 * s)}" {S.STROKE_THIN}/>'
    return body


def flame(x, y, s, k):
    """Flame on top of a torch bowl, k = 0..2 (flicker frames)."""
    top = y - 330 * s
    h = (92, 80, 100)[k] * s
    lean = (-6, 7, -2)[k] * s
    w = (26, 30, 24)[k] * s
    outer = (f'<path d="M{f1(x - w)},{f1(top - 4 * s)} C{f1(x - w * 1.2)},{f1(top - h * 0.5)} {f1(x + lean - 4 * s)},'
             f'{f1(top - h * 0.8)} {f1(x + lean)},{f1(top - h)} C{f1(x + lean + 6 * s)},{f1(top - h * 0.7)} '
             f'{f1(x + w * 1.2)},{f1(top - h * 0.45)} {f1(x + w)},{f1(top - 4 * s)} Z" fill="#f4a03c" {S.STROKE_THIN}/>')
    inner = (f'<path d="M{f1(x - w * 0.5)},{f1(top - 4 * s)} C{f1(x - w * 0.6)},{f1(top - h * 0.4)} '
             f'{f1(x + lean * 0.6)},{f1(top - h * 0.55)} {f1(x + lean * 0.6)},{f1(top - h * 0.66)} '
             f'C{f1(x + w * 0.6)},{f1(top - h * 0.4)} {f1(x + w * 0.55)},{f1(top - h * 0.2)} {f1(x + w * 0.5)},'
             f'{f1(top - 4 * s)} Z" fill="#fde39a"/>')
    return outer + inner


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.line(0), ctx.line(1), ctx.line(2)

    # ---------------------------------------------------------------- key times (narration)
    t_put = L0.at("放进狮子坑")                           # '放进狮子坑里'
    t_lions = phrase_t(L0, "好多大狮子")
    t_call = L1.start                                    # the king calls down
    t_save = phrase_t(L1, "一定会救你")
    t_stone = L2.start                                   # '人们搬来一块大石头'
    t_block = phrase_t(L2, "堵住坑口")
    t_seal0 = L2.at("国王用自己的印")
    t_press = phrase_t(L2, "封了印", 0.3)
    t_none = L2.at("谁也不能打开")

    # Daniel and the guards walk in (period WP, all arriving together)
    WP = 0.27
    n_d = 15
    t_walk0 = snap(0.25)
    d_fa, d_dx, d_dy, t_arrive = step_walk(t_walk0, n_d, STEP, WP, PS)
    t_hop = snap(max(t_arrive + 0.2, t_put + 0.35))      # Daniel hops into the shaft (cut at the top of the hop)
    t_brace = snap(t_hop - 0.12)                         # the rope guard braces
    t_hang = t_hop + 0.32                                # caught by the rope, hanging at the top of the shaft
    t_d0, t_d1 = t_hang + 0.35, snap(t_lions + 0.55)     # let down slowly ... lands
    t_look = snap(t_call - 0.35)                         # Daniel looks up at the king
    t_rope_up0, t_rope_up1 = t_d1 + 0.35, t_d1 + 1.05     # the empty rope is pulled up
    g_go = snap(t_rope_up1 + 0.15)                       # the guards walk off to fetch the stone

    # ---------------------------------------------------------------- static backdrops
    sc.add("sky", sky_svg(), seed=3)
    sc.add("night", night_svg(), wc=0.6, motion=M.keys([(0, {"alpha": 0.0}), (t_stone, {"alpha": 0.35}),
                                                        (T, {"alpha": 0.8})], "sine"))
    sc.add("moon", moon_svg(), wc=0.4, motion=M.keys([(t_call, {"alpha": 0, "dy": 40}), (T, {"alpha": 1, "dy": 0})],
                                                     "sine"))
    sc.add("clouds", clouds_svg(), seed=5, motion=M.drift(6, 0))
    sc.add("far", far_svg(), seed=7)
    sc.add("ground", ground_front_svg(), seed=9)

    # torches: poles (static), flames (flicker flipbook) and warm glows (additive)
    poles = "".join(torch_pole(x, y, TS) for x, y in TORCHES)
    sc.add("poles", doc(S.g(poles, filter="wobble-fine")))
    glow_defs = S.rad_grad("s8tg", [(0, "#6a3a10", 1), (0.4, "#4a2a0c", 0.6), (1, "#000000", 0)])
    for i, (x, y) in enumerate(TORCHES):
        top = y - 330 * TS - 40 * TS
        sc.add(f"torch_glow{i}", doc(f'<circle cx="{x}" cy="{f1(top)}" r="300" fill="url(#s8tg)"/>', glow_defs),
               wc=0, blend="add", motion=M.combine(M.breathe(0.05, 0.9, pivot=(x, top), phase=0.3 * i),
                                                   M.pulse(0.75, 1.0, 0.7, 0.4 * i)))
        sc.add(f"flame{i}", [doc(S.g(flame(x, y, TS, k), filter="wobble-fine")) for k in range(3)], wc=0.4,
               frame_at=lambda t, i=i: float(int(t * 9 + 2 * i) % 3))

    # ---------------------------------------------------------------- the den (back part)
    sc.add("den_back", doc(PR.lion_den(HX, G, DS, part="back")), seed=13)

    # evening light falling through the mouth (goes out when the stone is on)
    o0, o1 = HX - HOLE, HX + HOLE
    beam = (f'<path d="M{o0 + 8},{G} L{o1 - 8},{G} L{o1 + 110},{FY + 8} L{o0 - 110},{FY + 8} Z" fill="url(#s8beam)" '
            f'filter="url(#soft)"/><ellipse cx="{HX}" cy="{FY + 8}" rx="230" ry="30" fill="#6a4a2a" filter="url(#soft)"/>')
    sc.add("beam", doc(beam, S.lin_grad("s8beam", [(0, "#7a5630", 0.9), (1, "#5a3a20", 0.35)])), wc=0, blend="add",
           motion=M.keys([(0, {"alpha": 0.7}), (t_block - 0.5, {"alpha": 0.7}), (t_block + 0.1, {"alpha": 0.0})],
                         "sine"))

    # ---------------------------------------------------------------- lions in the den
    LS = 0.62
    # the sleeper (upstage, behind the lioness): sleeps, peeks when Daniel lands, sleeps again
    sx_, sy_ = HX + 360, FY - 24
    sleeper = [doc(PR.lion(sx_, sy_, 0.55, -1, pose="sleep", tail=tl)) for tl in (-0.4, 0.4)]
    sleeper += [doc(PR.lion(sx_, sy_, 0.55, -1, pose="sleep", eyes="half"))]
    sc.add("sh_sleeper", doc(C.ground_shadow(sx_ - 20, sy_, 0.55, 420, 0.3)))
    sc.add("lion_sleeper", sleeper,
           frame_at=lambda t: 2.0 if t_d1 + 0.4 <= t < t_d1 + 2.6 else float(int(t / 1.7) % 2),
           motion=M.breathe(0.012, 3.2, pivot=(sx_, sy_)))
    # the lioness sits on the right, blinking now and then, tail swishing
    lx2 = HX + 300
    sc.add("sh_lioness", doc(C.ground_shadow(lx2 - 10, FY, LS, 300, 0.32)))
    lioness = [doc(PR.lion(lx2, FY, LS, -1, pose="sit", variant=1, tail=tl)) for tl in (-0.5, 0.0, 0.5)]
    lioness += [doc(PR.lion(lx2, FY, LS, -1, pose="sit", variant=1, eyes="closed"))]
    blinks = [2.3, 6.9, 12.4, 17.6, 22.0]
    sc.add("lioness", lioness,
           frame_at=lambda t: 3.0 if any(b <= t < b + 0.16 for b in blinks) else float(int(t / 0.6) % 3),
           motion=M.breathe(0.012, 3.0, pivot=(lx2, FY), phase=0.4))
    # the big lion lies on the left, sits up (curious) when Daniel lands
    lx1 = HX - 330
    t_lsit = snap(t_d1 + 0.5)
    sc.add("sh_lion", doc(C.ground_shadow(lx1, FY, LS, 380, 0.32)))
    lion1 = [doc(PR.lion(lx1, FY, LS, 1, pose="lie", tail=tl)) for tl in (-0.3, 0.3)]
    lion1 += [doc(PR.lion(lx1 + 40, FY, LS, 1, pose="sit", tail=tl)) for tl in (-0.4, 0.4)]
    lp = (lx1 + 30, FY)
    sc.add("lion1", lion1,
           frame_at=lambda t: (2.0 if t >= t_lsit else 0.0) + float(int(t / 0.8) % 2),
           motion=M.combine(dip(t_lsit, LS, lp, 8), M.breathe(0.012, 3.4, pivot=lp, phase=0.7)))

    # ---------------------------------------------------------------- Daniel
    # (1) walking in from the right with the guards (drawn where he stops, moved in by dx)
    dwalk = [doc(C.daniel(DR, G, PS, -1, pose=p, expr=e)) for p, e in
             (("walk_a", "neutral"), ("walk_b", "neutral"), ("stand", "peaceful"))]
    d_dist = n_d * STEP
    sc.add("sh_dwalk", doc(C.ground_shadow(DR, G, PS, 120, 0.3)),
           motion=M.combine(swap(-1, t_hop), lambda t: Tf(dx=d_dist - d_dx(t))))
    sc.add("daniel_walk", dwalk,
           frame_at=lambda t: d_fa(t) if d_fa(t) is not None else 2.0,
           motion=M.combine(swap(-1, t_hop), lambda t: Tf(dx=d_dist - d_dx(t), dy=d_dy(t)),
                            hop(t_hop, [(-0.3, {"sy": 1, "dy": 0}), (-0.08, {"sy": 0.9, "dy": 6}),
                                        (0.0, {"sy": 1.05, "dy": -20})], (DR, G), ["in", "out"])))

    # (2) on the rope in the shaft: hold_rope facing the guard, hop arc in, then let down slowly
    HY0 = G + 70                     # the anchor (lowest sole) while hanging at the top of the shaft
    hang = doc(C.daniel(DFX, HY0, PS, 1, pose="hold_rope", expr="peaceful"))
    hand = C.hand_positions(C.daniel, DFX, HY0, PS, 1, pose="hold_rope")[0]
    jump_dx, jump_dy = (DR - 40) - DFX, (G - 40) - HY0

    def descend(t):
        return (FY - HY0) * M.progress(t, t_d0, t_d1, "sine")

    def hang_m(t):
        u = M.progress(t, t_hop, t_hang, "linear")
        dx = jump_dx * (1 - M.ease("out")(u))
        dy = jump_dy * (1 - u) - 60 * math.sin(math.pi * u) * (1 - u) + descend(t)
        bounce = 0.0
        if t_hang <= t < t_hang + 0.5:
            bounce = 10 * math.sin(math.pi * (t - t_hang) / 0.5)
        sway = 2.2 * math.sin(2 * math.pi * (t - t_hang) / 2.6) * M.progress(t, t_hang, t_hang + 0.6, "sine")
        return Tf(dx=dx, dy=dy + bounce, rot=sway, px=hand[0], py=hand[1])
    sc.add("daniel_rope", hang, motion=M.combine(swap(t_hop, t_d1), hang_m))

    # the rope: guard's fist -> the corner of the mouth (static) and the corner -> Daniel's hand (stretching)
    g1_fist = C.hand_positions(C.guard, G1X, G, PS, -1, pose="pull_rope")[0]
    sc.add("rope_top", doc(rope([g1_fist, RIM])), wc=0.3,
           motion=M.keys([(t_hop - 0.05, {"alpha": 0}), (t_hop, {"alpha": 1}), (t_rope_up1, {"alpha": 1}),
                          (t_rope_up1 + 0.05, {"alpha": 0})], "linear"))
    LMAX = 1000.0
    sc.add("rope_down", doc(rope([RIM, (RIM[0], RIM[1] + LMAX)])), wc=0.3,
           motion=lambda t: rope_down_m(t))

    def hand_at(t):
        m = hang_m(t)
        return hand[0] + m.dx, hand[1] + m.dy

    def rope_down_m(t):
        if t < t_hop or t >= t_rope_up1:
            return Tf(alpha=0.0)
        if t < t_d1:
            hx, hy = hand_at(t)
        else:                                            # the rope end is pulled up out of the den
            hx, hy = hand_at(t_d1 - 0.001)
            hy = hy - (hy - RIM[1] - 20) * M.progress(t, t_rope_up0, t_rope_up1, "in")
        dx, dy = hx - RIM[0], hy - RIM[1]
        ln = max(4.0, math.hypot(dx, dy))
        ang = math.degrees(math.atan2(-dx, dy))
        return Tf(sy=ln / LMAX, rot=ang, px=RIM[0], py=RIM[1])

    # (3) on the den floor: lands (stand), looks up at the king (look_up), sits and prays in the dark
    dfloor = [doc(C.daniel(DFX, FY, PS, 1, pose="stand", expr="peaceful")),
              doc(C.daniel(DFX, FY, PS, -1, pose="look_up", expr="happy")),
              doc(C.daniel(DFX, FY, PS, -1, pose="sit_pray"))]
    t_dpray = snap(t_block + 0.9)
    fp = (DFX, FY)
    sc.add("sh_daniel", doc(C.ground_shadow(DFX, FY, PS, 150, 0.32)), motion=swap(t_d1, 1e9))
    sc.add("daniel_floor", dfloor, frame_at=cuts([(0, 0), (t_look, 1), (t_dpray, 2)]),
           motion=M.combine(swap(t_d1, 1e9),
                            hop(t_d1, [(0, {"sy": 0.88, "sx": 1.05}), (0.14, {"sy": 1.03, "sx": 0.99}),
                                       (0.32, {"sy": 1.0, "sx": 1.0})], fp, ["out", "sine"]),
                            dip(t_look, PS, fp, 7),
                            hop(t_save + 0.2, [(0, {"rot": 0}), (0.22, {"rot": -2.5}), (0.5, {"rot": 0}),
                                               (0.72, {"rot": -2.0}), (1.0, {"rot": 0})], (DFX, FY - 150)),
                            dip(t_dpray, PS, fp, 9),
                            M.breathe(0.01, 3.2, pivot=fp)))

    sc.add("den_front", doc(PR.lion_den(HX, G, DS, part="front")), seed=17)

    # the den grows dark once the stone is on (a soft multiply over the chamber only)
    dark_defs = S.lin_grad("s8dk", [(0, "#4a4870"), (1, "#3a3a62")])
    dark = (f'<path d="{PR._den_cave()}" transform="translate({HX},{G}) scale({DS})" fill="url(#s8dk)" '
            f'stroke="#3a3a62" stroke-width="22" filter="url(#soft)"/>')
    sc.add("den_dark", doc(dark, dark_defs), wc=0, blend="multiply",
           motion=M.keys([(0, {"alpha": 0.32}), (t_block - 0.3, {"alpha": 0.32}), (t_block + 0.6, {"alpha": 0.78})],
                         "sine"))
    # ...and a faint warm glow stays round Daniel (he is not alone)
    sc.add("daniel_glow", doc(f'<ellipse cx="{DFX}" cy="{FY - 90}" rx="200" ry="170" fill="url(#s8dg)"/>',
                              S.rad_grad("s8dg", [(0, "#4a3a1c", 1), (0.6, "#2a2010", 0.5), (1, "#000000", 0)])),
           wc=0, blend="add", motion=M.keys([(t_block, {"alpha": 0}), (t_none, {"alpha": 0.8})], "sine"))

    # ---------------------------------------------------------------- guards
    # guard 1: walks in behind Daniel, braces with the rope, lets him down, then walks off and pushes the stone
    g_fa, g_dx, g_dy, _ = step_walk(t_walk0, n_d, STEP, WP, PS)
    g_out_n = 11
    go_fa, go_dx, go_dy, _ = step_walk(g_go, g_out_n, STEP, 0.25, PS)

    def guard_track(name, gx, var, rope_job):
        frames = [doc(C.guard(gx, G, PS, -1, variant=var, pose=p)) for p in ("walk_a", "walk_b", "stand")]
        frames += [doc(C.guard(gx, G, PS, -1, variant=var, pose="pull_rope"))] if rope_job else [frames[2]]
        frames += [doc(C.guard(gx, G, PS, 1, variant=var, pose=p)) for p in ("walk_a", "walk_b")]

        def fa(t):
            if t < t_arrive:
                f = g_fa(t)
                return f if f is not None else 2.0
            if t < g_go:
                return 3.0 if (rope_job and t_brace <= t < t_rope_up1 + 0.1) else 2.0
            f = go_fa(t)
            return 4.0 + f if f is not None else 4.0

        def mv(t):
            if t < g_go:
                return Tf(dx=d_dist - g_dx(t), dy=g_dy(t))
            return Tf(dx=go_dx(t), dy=go_dy(t))
        pv = (gx, G)
        rock = (lambda t: Tf(rot=-1.6 * math.sin(2 * math.pi * (t - t_d0) / 0.9) * M.progress(t, t_d0, t_d0 + 0.4)
                             * (1 - M.progress(t, t_d1 - 0.3, t_d1)))) if rope_job else None
        sc.add("sh_" + name, doc(C.ground_shadow(gx, G, PS, 130, 0.3)), motion=lambda t: Tf(dx=mv(t).dx))
        sc.add(name, frames, frame_at=fa, motion=M.combine(mv, M.with_pivot(rock, pv) if rock else None,
                                                           dip(t_brace, PS, pv, 8) if rope_job else None,
                                                           dip(t_rope_up1 + 0.1, PS, pv, 6) if rope_job else None))
    guard_track("guard_rope", G1X, 1, True)
    guard_track("guard_spear", G2X, 2, False)

    # ---------------------------------------------------------------- the stone, rolled in from the right
    n_surge = 10
    s_end = snap(t_block + 0.05)
    s_go = s_end - n_surge * 0.42
    surge_t = [s_go + 0.42 * k for k in range(n_surge)]
    X_START = HX + 1250
    dist = X_START - HX

    def stone_x(t):
        x = X_START
        for k, tk in enumerate(surge_t):
            x -= dist / n_surge * M.progress(t, tk, tk + 0.34, "inout")
        return x
    NR = 24
    stones = [doc(PR.den_stone(HX, STONE_Y, DS, roll=-15 * k)) for k in range(NR)]
    RR = PR.DEN_STONE_R[1] * DS

    def stone_frame(t):
        ang = (X_START - stone_x(t)) / RR * 180 / math.pi
        return float(int(round(ang / 15)) % NR)

    def stone_m(t):
        x = stone_x(t)
        lift = -6 * (1 - M.progress(t, s_end - 0.25, s_end, "in"))      # rolls along the ground, drops in
        return Tf(dx=x - HX, dy=lift)
    sc.add("sh_stone", doc(C.ground_shadow(HX, G, DS, 330, 0.35)), motion=lambda t: Tf(dx=stone_x(t) - HX))
    sc.add("stone", stones, frame_at=stone_frame, motion=stone_m)
    # dusk shading on the (light) boulder: cool on the side away from the sky glow, warm torch-lit rim
    scy = STONE_Y - PR.DEN_STONE_R[1] * DS
    shade_defs = S.lin_grad("s8ss", [(0, "#fff6ea", 0), (0.45, "#d8c6d6", 0.6), (1, "#8f7aa0", 1)], 0.15, 0.1, 0.85, 1)
    sc.add("stone_shade", doc(f'<ellipse cx="{HX}" cy="{f1(scy)}" rx="{f1(166 * DS)}" ry="{f1(124 * DS)}" '
                              f'fill="url(#s8ss)"/>', shade_defs), wc=0, blend="multiply", motion=stone_m)

    # the cord over the stone (stretched across just before the king seals it) and the clay seal
    k = DS
    lp_, rp_ = (HX - 204 * k, STONE_Y - 30 * k), (HX + 204 * k, STONE_Y - 30 * k)
    SEAL = (HX - 86 * k, STONE_Y - 207 * k)
    pegs = ""
    for px_ in (lp_[0], rp_[0]):
        pegs += (f'<path d="M{f1(px_ - 5 * k)},{f1(STONE_Y + 2)} L{f1(px_ - 4 * k)},{f1(STONE_Y - 34 * k)} '
                 f'Q{f1(px_)},{f1(STONE_Y - 42 * k)} {f1(px_ + 4 * k)},{f1(STONE_Y - 34 * k)} L{f1(px_ + 5 * k)},'
                 f'{f1(STONE_Y + 2)} Z" fill="{P["wood"]}" {S.STROKE_THIN}/>')
    cord_d = (f"M{f1(lp_[0])},{f1(lp_[1])} Q{f1(HX - 196 * k)},{f1(STONE_Y - 170 * k)} {f1(SEAL[0])},{f1(SEAL[1])} "
              f"Q{f1(HX + 40 * k)},{f1(STONE_Y - 262 * k)} {f1(HX + 120 * k)},{f1(STONE_Y - 200 * k)} "
              f"Q{f1(HX + 200 * k)},{f1(STONE_Y - 130 * k)} {f1(rp_[0])},{f1(rp_[1])}")
    cord = (pegs + f'<path d="{cord_d}" fill="none" stroke="{INK}" stroke-width="{f1(8 * k)}" stroke-linecap="round"/>'
            f'<path d="{cord_d}" fill="none" stroke="#d8b878" stroke-width="{f1(4 * k)}" stroke-linecap="round"/>')
    t_cord0 = snap(s_end + 0.35)
    sc.add("cord", doc(S.g(cord, filter="wobble-fine")), wc=0.3,
           reveal=lambda t: dict(mode="left", frac=M.progress(t, t_cord0, t_cord0 + 0.6, "inout"), soft=30),
           motion=lambda t: Tf(alpha=1.0 if t >= t_cord0 else 0.0))
    t_seal = snap(t_press)
    sc.add("seal", doc(PR.royal_seal(SEAL[0], SEAL[1], 0.62 * k, kind="impression")), wc=0.3,
           motion=M.keys([(t_seal, {"alpha": 0, "s": 1.25}), (t_seal + 0.02, {"alpha": 1}), (t_seal + 0.25, {"s": 1.0})],
                         "out", pivot=SEAL))
    sc.add("seal_flash", doc(f'<circle cx="{f1(SEAL[0])}" cy="{f1(SEAL[1])}" r="90" fill="url(#s8sf)"/>',
                             S.rad_grad("s8sf", [(0, "#8a6a30", 1), (0.5, "#5a4020", 0.5), (1, "#000000", 0)])),
           wc=0, blend="add", motion=M.keys([(t_seal, {"alpha": 0, "s": 0.5}), (t_seal + 0.15, {"alpha": 0.9, "s": 1.0}),
                                             (t_seal + 1.1, {"alpha": 0, "s": 1.5})], ["out", "sine"], pivot=SEAL))

    # dust puff when the stone drops onto the mouth
    puff = ""
    for dx_, r in ((-170, 30), (-120, 22), (150, 28), (190, 20), (-210, 18)):
        puff += f'<circle cx="{HX + dx_}" cy="{G - 12}" r="{r}" fill="#d9c4a4" {S.STROKE_THIN} opacity="0.9"/>'
    sc.add("dust", doc(S.g(puff, filter="wobble-fine")), wc=0.3,
           motion=M.keys([(s_end - 0.02, {"alpha": 0, "s": 0.6}), (s_end + 0.08, {"alpha": 0.9, "s": 1.0}),
                          (s_end + 0.9, {"alpha": 0, "s": 1.35, "dy": -26})], ["out", "sine"], pivot=(HX, G)))

    # the guards push the stone (heave-ho shuffles, keeping their palms on it) then stand watch beside it
    def pusher(name, var, lane_dy, gs, push_back):
        gy = G + lane_dy
        hx_, hy_ = C.hand_positions(C.guard, 0, 0, gs, -1, pose="push")[0]
        ax = HX + push_back - hx_                       # drawn at the stone's final spot
        frames = [doc(C.guard(ax, gy, gs, -1, variant=var, pose="push")),
                  doc(C.guard(ax, gy, gs, -1, variant=var, pose="stand"))]
        t_stand = snap(s_end + 0.55)

        def mv(t):
            dx = stone_x(t) - HX
            lift = 0.0
            for tk in surge_t:
                if tk <= t <= tk + 0.34:
                    lift -= 9 * gs * math.sin(math.pi * (t - tk) / 0.34)
            return Tf(dx=dx, dy=lift)
        pv = (ax, gy)
        sc.add("sh_" + name, doc(C.ground_shadow(ax, gy, gs, 140, 0.3)),
               motion=M.combine(swap(s_go - 0.5, 1e9), lambda t: Tf(dx=stone_x(t) - HX)))
        sc.add(name, frames, frame_at=cuts([(0, 0), (t_stand, 1)]),
               motion=M.combine(swap(s_go - 0.5, 1e9), mv, dip(t_stand, gs, pv, 7)))
    pusher("pusher1", 1, 0, PS, 128)

    # guard 2 walks along behind (upstage) with his spear, and stands watch at the right
    g2s, g2y, g2x = 0.74, G - 40, HX + 440
    n2 = 20
    g2_fa, g2_dx, g2_dy, _ = step_walk(s_go, n2, dist / n2, 0.42 * n_surge / n2, g2s)
    g2 = [doc(C.guard(g2x, g2y, g2s, -1, variant=2, pose=p)) for p in ("walk_a", "walk_b", "stand")]
    z_st = next(l.z for l in sc.layers if l.name == "sh_stone")
    sc.add("sh_guard2b", doc(C.ground_shadow(g2x, g2y, g2s, 130, 0.28)), z=z_st - 0.6,
           motion=M.combine(swap(s_go - 0.5, 1e9), lambda t: Tf(dx=dist - g2_dx(t))))
    sc.add("guard2b", g2, z=z_st - 0.5,
           frame_at=lambda t: g2_fa(t) if g2_fa(t) is not None else (0.0 if t < s_go else 2.0),
           motion=M.combine(swap(s_go - 0.5, 1e9), lambda t: Tf(dx=dist - g2_dx(t), dy=g2_dy(t))))

    # ---------------------------------------------------------------- the king
    # A: sad at KX0 -> 3 steps to the rim -> calls down -> stands, sad
    k_fa, k_dx, k_dy, k_arr = step_walk(snap(t_call - 1.05), 3, STEP, 0.3, PS)
    kA = [doc(C.king(KX1, G, PS, 1, pose=p, attire="darius", expr=e)) for p, e in
          (("sad", None), ("walk_a", "worried"), ("walk_b", "worried"), ("call_out", "call"), ("stand", "sad"))]
    t_kstand = snap(L1.end + 0.25)
    t_kstep = snap(t_seal0 - 0.05)
    k2_fa, k2_dx, k2_dy, k2_arr = step_walk(t_kstep, 1, STEP, 0.36, PS)
    t_reach = snap(k2_arr + 0.02)
    t_back = snap(t_seal + 0.75)
    t_sad = snap(max(t_none - 0.05, t_back + 0.8))
    kA_base = cuts([(0, 0), (t_call, 3), (t_kstand, 4)])
    kp1 = (KX1, G)

    def kA_m(t):
        return Tf(dx=-3 * STEP + k_dx(t), dy=k_dy(t))
    sc.add("sh_kingA", doc(C.ground_shadow(KX1, G, PS, 130, 0.3)),
           motion=M.combine(swap(-1, t_kstep), lambda t: Tf(dx=kA_m(t).dx)))
    sc.add("kingA", kA, frame_at=lambda t: 1 + k_fa(t) if k_fa(t) is not None else kA_base(t),
           motion=M.combine(swap(-1, t_kstep), kA_m, dip(t_call, PS, kp1, 7), dip(t_kstand, PS, kp1, 6),
                            hop(t_save, [(0, {"rot": 0}), (0.3, {"rot": 2.0}), (0.9, {"rot": 0})], kp1),
                            M.breathe(0.01, 3.0, pivot=kp1)))
    # B: one step up to the stone -> reaches out with the signet ring and presses it -> steps back, sad
    ring_hand = C.hand_positions(C.king, KX2, G, PS, 1, pose="reach_out", attire="darius")[1]
    ring = PR.royal_seal(ring_hand[0] + 6, ring_hand[1] - 2, 0.42)
    kB = [doc(C.king(KX2, G, PS, 1, pose="walk_a", attire="darius", expr="sad")),
          doc(C.king(KX2, G, PS, 1, pose="reach_out", attire="darius", expr="neutral") + ring),
          doc(C.king(KX2, G, PS, 1, pose="stand", attire="darius", expr="sad")),
          doc(C.king(KX2 - 12, G, PS, 1, pose="stand", attire="darius", expr="sad"))]
    kp2 = (KX2, G)
    # press: lean in so the ring meets the seal spot, then ease back
    lean = M.keys([(max(t_reach + 0.25, t_seal - 0.6), {"rot": 0, "dx": 0, "dy": 0}),
                   (t_seal, {"rot": 4.5, "dx": SEAL[0] - ring_hand[0] - 8, "dy": SEAL[1] - ring_hand[1] + 2}),
                   (t_seal + 0.4, {"rot": 4.5, "dx": SEAL[0] - ring_hand[0] - 8, "dy": SEAL[1] - ring_hand[1] + 2}),
                   (t_back, {"rot": 0, "dx": 0, "dy": 0})], ["inout", "linear", "inout"], pivot=kp2)
    sc.add("sh_kingB", doc(C.ground_shadow(KX2, G, PS, 130, 0.3)),
           motion=M.combine(swap(t_kstep, 1e9), lambda t: Tf(dx=k2_dx(t) - STEP)))
    sc.add("kingB", kB,
           frame_at=lambda t: 0.0 if k2_fa(t) is not None else cuts([(0, 2), (t_reach, 1), (t_back, 2), (t_sad, 3)])(t),
           motion=M.combine(swap(t_kstep, 1e9), lambda t: Tf(dx=k2_dx(t) - STEP, dy=k2_dy(t)),
                            lean, dip(t_reach, PS, kp2, 6), dip(t_back, PS, kp2, 6), dip(t_sad, PS, kp2, 6),
                            M.breathe(0.01, 3.0, pivot=kp2, phase=0.2)))

    # ---------------------------------------------------------------- camera
    camA = Cam(1520, 640, 1900)                       # dusk, the den mouth, the guards coming
    camB = Cam(1350, 905, 1800)                       # down into the den
    camC = Cam(1300, 880, 1780)                       # the king at the rim and Daniel below
    camD = Cam(1470, 820, 1860)                       # the stone coming from the right
    camE = Cam(HX - 120, 610, 1320)                   # the seal
    camF = Cam(1330, 870, 1800)                       # pull back: sealed den at night
    keys = [(0, camA), (t_put + 0.2, camA), (t_d1 - 0.6, camB), (t_call - 0.3, camB), (t_call + 1.4, camC),
            (s_go + 0.6, camC), (t_stone + 0.4, camD), (t_block + 0.4, camD), (t_seal0 + 1.2, camE),
            (t_none - 0.2, camE), (min(T - 0.6, t_none + 2.4), camF)]
    base = M.cam_keys([(t, clamp_cam(c)) for t, c in keys], "sine")
    sc.camera = M.cam_shake(base, amp=3.0, t0=s_end, t1=s_end + 0.35, freq=11)

    # ---------------------------------------------------------------- fx
    def dusk(t):
        return 0.12 + 0.2 * M.progress(t, t_stone - 2, T, "sine")
    sc.fx = [
        lut_tint((205, 188, 225), dusk, mode="multiply"),
        FX.sparkles((200, 40, SW - 200, 420), count=22, t0=t_stone, color=(255, 246, 214), size=(4, 8), period=2.6,
                    drift=0, seed=31),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=T + 0.1, gain_db=-17, fade_in=0.8, fade_out=0.9)
    sc.sfx("fire", 0, dur=T + 0.1, gain_db=-19, fade_in=0.8, fade_out=0.9)
    sc.sfx("night", t_stone - 3, dur=T - t_stone + 3.1, gain_db=-17, fade_in=2.5, fade_out=0.9)
    sc.sfx("footsteps", t_walk0, dur=t_arrive - t_walk0 + 0.1, gain_db=-13, fade_in=0.4, fade_out=0.3)
    sc.sfx("cloth", t_hop - 0.1, gain_db=-14)
    sc.sfx("ship_creak", t_hang, dur=t_d1 - t_hang, gain_db=-17, fade_in=0.3, fade_out=0.4)
    sc.sfx("thud", t_d1, gain_db=-13)
    sc.sfx("footsteps", g_go, dur=2.7, gain_db=-19, fade_in=0.2, fade_out=0.8, pan=0.5)
    sc.sfx("footsteps", snap(t_call - 1.05), dur=1.0, gain_db=-17, pan=-0.3)
    for i, tk in enumerate(surge_t):
        sc.sfx("thud", tk + 0.2, gain_db=-20 + (2 if i > n_surge - 4 else 0), pan=0.4 - 0.04 * i)
    sc.sfx("thud", s_end, gain_db=-6, duck_db=-3)
    sc.sfx("cloth", t_cord0, gain_db=-14)
    sc.sfx("footsteps", t_kstep, dur=0.45, gain_db=-18, pan=-0.2)
    sc.sfx("pop", t_seal, gain_db=-10)
    sc.sfx("thud", t_seal, gain_db=-15)
    return sc
