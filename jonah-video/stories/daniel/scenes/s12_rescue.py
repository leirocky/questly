"""Scene 12 — Daniel is pulled up into the sunshine; not a scratch on him (Daniel 6:23-24).

One wide 3800 x 1200 sunny-morning stage seen from ground level (a clear new view after s11's cutaway): the pit
mouth (props.lion_den view='outside') with the den stone rolled aside, a wooden A-frame with a pulley wheel over
the pit, the king and some townsfolk on the left, two guards hauling on the right; along a sandy path further right
the jealous officials and two more guards, Babylon on the horizon. No cuts.

  opening        calm: the king at the rim, reaching out happily (as s11 ended); the guards ready on the rope.
  '国王高兴极了'  the king throws his arms up for joy (hop).
  '马上叫人…'     he waves the guards on; they haul hand over hand (each heave rocks them back, the wheel turns)
                 and Daniel rises out of the dark pit holding the rope, smiling, in five steady tugs.
  (pause)        he springs out onto the grass beside the king (whoosh, thud), and the king hugs him.
  '大家看了又看'  everyone leans in to look him over: the king, the guards, the townsfolk; Daniel turns round and
                 back (hops) to show himself.
  '一点伤也没有'  arms up, not a scratch! little twinkles round his robe and hands (never on his face), the king
                 throws his arms up, the townsfolk cheer, the guards hop.
  '因为他信靠…'   Daniel kneels with his arms lifted in thanks; God's warm light slants down from the sky onto him
                 (light only).
  L2             the camera glides right along the path to the officials (who had been watching, first scheming,
                 then surprised, then worried): '那些想害但以理的官员' they hang their heads; '后来自己受到了惩罚'
                 the guards turn and calmly lead them away toward the city (walking, sad faces; nothing scary, no
                 lions). The camera drifts with them, ending on the procession and Babylon on the horizon.

Daniel coming up out of the pit: the figure moves (one layer); the pit's near rim and the meadow in front of it are
repainted over him by an occluder layer that is an exact clipped copy of the backdrop (same seed), so he is only
seen above the rim and inside the hole. Pose and face changes are hard cuts sold by squashes / hops.
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

SW, SH = 3800, 1200
INK = P["ink"]
HORIZON = 560
G = 940                      # ground line by the pit (feet)
G2 = 860                     # the path further back on the right (officials)
HX = 1250                    # pit centre
DSO = 1.0                    # pit scale
ROPE_X = HX - 20             # the hanging rope (left edge of the wheel)
WHEEL_R = 34
WHEEL_Y = G - 480
DAN_X = ROPE_X + 66          # Daniel's anchor on the rope (facing left: fists at x - 66)
DAN_Y0, DAN_Y1 = G + 470, G - 25
KS = 1.0
KX = 860                     # the king
HUG_DX = KX + 95             # Daniel in the king's hug
SHOW_DX = 80                 # after the hug he hops a step to the right (onto the rim stones) to be looked over
DAN_SPOT = HUG_DX + SHOW_DX
GS = 0.95                    # rope guards
OS = 0.88                    # officials / escort scale

FAR_SEED = 41

PUNCT = "，。；：？！、,.;:?!"

def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ timing helpers


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


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


def when(ctx, phrase):
    """Start time of ``phrase``: its chunk start, or its character position inside the chunk."""
    for ln in ctx.lines:
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


def hop(t0, keys, pivot, curves="sine"):
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


def dip(t0, s, pivot, depth=9.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": 0.95}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pivot, ["in", "out", "sine"])


def happy_hop(t0, s, pivot, h=18.0):
    return hop(t0, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5 * s, "sy": 0.94}), (0.17, {"dy": -h * s, "sy": 1.04}),
                    (0.34, {"dy": 0, "sy": 0.97}), (0.46, {"dy": 0, "sy": 1})], pivot,
               ["in", "out", "in", "sine"])


def step_walk(t0, n, step, period, s, move=0.12, lift=7.0):
    """Planted-foot walk with two stride drawings: each drawing holds its anchor still; as the next cuts in, the
    anchor advances one stride with a short ease and a little lift. Returns (frame_at -> 0/1 or None, dx, dy, t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]
    t_end = snap(t0 + n * period)

    def fa(t):
        if t < cut_t[0] or t >= t_end:
            return None
        k = min(n - 1, int((t - t0) / period))
        return float(k % 2)

    def dx(t):
        return sum(step * M.progress(t, ck - move * 0.45, ck + move * 0.55, "sine") for ck in cut_t)

    def dy(t):
        y = 0.0
        for ck in cut_t:
            if ck - move * 0.45 <= t <= ck + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - ck + move * 0.45) / move)
        return y
    return fa, dx, dy, t_end


def clamp_cam(c, margin=4):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), SH - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys):
    """[(t, Cam)] eased moves; the viewport's bottom edge is interpolated so the clamp never kinks a move."""
    keys = [(t, clamp_cam(c)) for t, c in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a), (t1, b) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
        return keys[-1][1]
    return cam


# blink drawings (eyes-closed copies of the expressions that blink); setdefault keeps the shared table intact
for _e in ("happy", "neutral", "worried", "surprised", "call"):
    C.EXPRS.setdefault(f"d11_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))



# ============================================================================ backdrops


def sky_svg():
    defs = S.lin_grad("sky12", [(0, "#8fc6df"), (0.55, "#c4e2ea"), (1, "#f6e6c0")])
    body = f'<rect x="-20" y="-20" width="{SW + 40}" height="{HORIZON + 60}" fill="url(#sky12)"/>'
    # the morning sun high on the left, soft
    defs += S.rad_grad("sun12", [(0, "#fff6d6", 0.9), (0.4, "#fdeab0", 0.4), (1, "#fdeab0", 0)])
    body += (f'<circle cx="260" cy="150" r="360" fill="url(#sun12)"/>'
             f'<circle cx="260" cy="150" r="70" fill="{P["sun"]}" stroke="#f0b062" stroke-width="5" '
             f'filter="url(#wobble)"/>')
    return doc(body, defs)


CLOUDS = [(700, 150, 330, 96, 1), (1500, 90, 280, 80, 2), (2250, 180, 380, 104, 3), (3050, 110, 300, 86, 4),
          (3700, 210, 280, 80, 5), (1100, 300, 200, 56, 6), (2700, 330, 220, 60, 7)]


def clouds_svg():
    out = "".join(S.cloud(cx, cy, w, h, fill="#fdf6ea", seed=sd, sw=3, shade_fill="#dfe6ea")
                  for cx, cy, w, h, sd in CLOUDS)
    return doc(S.g(out, filter="wobble"))


def rays_svg():
    """God's warm light: golden rays slanting down from behind the clouds onto Daniel (never a figure)."""
    cx, cy = DAN_SPOT + 120, -260
    defs = S.rad_grad("rg12", [(0, "#fff1c0", 0.9), (0.6, "#ffe39a", 0.35), (1, "#ffe39a", 0)])
    body = (f'<path d="{S.rays(cx, cy, 120, 1250, 9, 5.5, rot=62)}" fill="#fff0bf" opacity="0.55" filter="url(#soft)"/>'
            f'<ellipse cx="{DAN_SPOT}" cy="{G - 180}" rx="260" ry="300" fill="url(#rg12)"/>')
    return doc(body, defs)


def far_svg():
    out = ""
    defs = S.lin_grad("ground12", [(0, "#c9c98a"), (0.5, "#b9bf74"), (1, "#a7b464")])
    # far hills and Babylon on the right horizon (the palace the officials are led back to)
    out += S.path(S.hill(-100, 1900, HORIZON + 8, 60, seed=2, bottom=HORIZON + 60, bumps=3), "#b9c7b4", sw=3)
    out += S.path(S.hill(1700, SW + 100, HORIZON + 8, 80, seed=7, bottom=HORIZON + 60, bumps=4), "#c2cdb6", sw=3)
    out += PR.nineveh_skyline(2500, SW + 60, HORIZON + 20, 0.62, seed=9, haze=0.42, tint="#e6e2cf")
    out += PR.nineveh_skyline(-80, 900, HORIZON + 24, 0.4, seed=3, haze=0.55, tint="#e6e2cf")
    # the meadow
    out += S.path(S.wave_line(HORIZON + 26, 5, 800, 0, -40, SW + 40) + f" L{SW + 40},{SH + 30} L-40,{SH + 30} Z",
                  "url(#ground12)", sw=3.5)
    # a sandy path from the den across to the city on the right
    path_d = (f"M{1150},{SH + 30} C{1400},{G + 40} {1900},{G - 20} {2300},{G2 + 30} C{2800},{G2 - 40} {3300},{G2 - 60} "
              f"{SW + 40},{G2 - 80} L{SW + 40},{G2 + 10} C{3300},{G2 + 20} {2800},{G2 + 60} {2400},{G2 + 110} "
              f"C{2000},{G + 70} {1650},{G + 160} {1500},{SH + 30} Z")
    out += S.path(path_d, P["sand_light"], sw=3)
    rng = random.Random(4)
    for _ in range(90):
        x = rng.uniform(0, SW)
        y = rng.uniform(HORIZON + 40, SH - 20)
        out += (f'<path d="M{f1(x)},{f1(y)} q4,-12 8,0" fill="none" stroke="{S.shade(P["grass_dark"], -0.1)}" '
                f'stroke-width="2.5" opacity="0.5"/>')
    out += PR.palm_tree(150, G - 70, 0.7, lean=0.2)
    out += PR.palm_tree(2050, HORIZON + 90, 0.45, lean=-0.15)
    out += PR.palm_tree(3480, HORIZON + 110, 0.5, lean=0.1)
    out += PR.bush(470, G - 40, 0.55, variant=1)
    out += PR.bush(1980, G - 10, 0.45, variant=3)
    out += PR.bush(3150, G2 - 30, 0.42, variant=0)
    for x, y, v in ((700, G + 20, 2), (1560, G + 30, 0), (2180, G2 + 50, 2), (2950, G2 + 70, 1), (3600, G2 + 90, 2),
                    (60, G + 120, 0), (1020, G + 140, 0)):
        out += PR.grass_tuft(x, y, 0.75, variant=v)
    return doc(out, defs)


def frame_svg():
    """The wooden A-frame with a pulley wheel over the pit (they haul Daniel up with it)."""
    wx, wy = ROPE_X, WHEEL_Y
    out = ""
    for bx in (HX - 290, HX + 262):
        out += (f'<path d="M{bx},{G - 6} L{wx},{wy - 70}" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
                f'<path d="M{bx},{G - 6} L{wx},{wy - 70}" stroke="{P["wood"]}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M{bx + 4},{G - 20} L{wx + 3},{wy - 60}" stroke="{P["wood_light"]}" stroke-width="3" '
                f'opacity="0.7"/>')
    # lashing at the top, the axle bar and the wheel
    out += (f'<path d="M{wx - 26},{wy - 86} L{wx + 26},{wy - 54} M{wx - 26},{wy - 60} L{wx + 26},{wy - 86}" '
            f'stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{wx - 26},{wy - 86} L{wx + 26},{wy - 54} M{wx - 26},{wy - 60} L{wx + 26},{wy - 86}" '
            f'stroke="#c8a46a" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{wx},{wy - 70} L{wx},{wy - 26}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M{wx},{wy - 70} L{wx},{wy - 26}" stroke="{P["wood_dark"]}" stroke-width="6" stroke-linecap="round"/>')
    return doc(S.g(out, filter="wobble-fine"))


def wheel_markup(rot):
    wx, wy = ROPE_X + WHEEL_R, WHEEL_Y
    out = f'<circle cx="{wx}" cy="{wy}" r="{WHEEL_R + 6}" fill="{P["wood"]}" stroke="{INK}" stroke-width="4"/>'
    out += f'<circle cx="{wx}" cy="{wy}" r="{WHEEL_R - 6}" fill="{P["wood_light"]}" stroke="{INK}" stroke-width="3"/>'
    for k in range(4):
        a = math.radians(rot + 45 * k)
        out += (f'<path d="M{f1(wx - (WHEEL_R - 6) * math.cos(a))},{f1(wy - (WHEEL_R - 6) * math.sin(a))} '
                f'L{f1(wx + (WHEEL_R - 6) * math.cos(a))},{f1(wy + (WHEEL_R - 6) * math.sin(a))}" stroke="{INK}" '
                f'stroke-width="3"/>')
    out += f'<circle cx="{wx}" cy="{wy}" r="8" fill="{P["gold"]}" stroke="{INK}" stroke-width="3"/>'
    return S.g(out, filter="wobble-fine")


def rope_d(pts):
    return "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts)


def rope_svg(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" '
            f'stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#c8a46a" stroke-width="6.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#a9834e" stroke-width="2" stroke-dasharray="6 9"/>')


def sparkle_markup(pts, k):
    out = ""
    for i, (x, y, r) in enumerate(pts):
        r = r * (0.7 + 0.3 * ((i + k) % 3) / 2)
        w = r * 0.22
        out += (f'<path d="M{x},{y - r} L{x + w},{y - w} L{x + r},{y} L{x + w},{y + w} L{x},{y + r} L{x - w},{y + w} '
                f'L{x - r},{y} L{x - w},{y - w} Z" fill="#ffe9a0" stroke="{P["ink_soft"]}" stroke-width="2"/>')
    return S.g(out, filter="wobble-fine")


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    # ---- key times ----
    t_joy = snap(L0.start + 0.1)                       # "国王高兴极了": arms up
    t_order = snap(L0.at("马上叫人") + 0.05)            # "马上叫人…": he waves the guards on
    t_pull0 = t_order + 0.3                            # the guards haul (hand over hand)
    PULL_P = 0.38
    N_PULL = 5
    pulls = [t_pull0 + k * PULL_P for k in range(N_PULL)]
    t_top = pulls[-1] + 0.3                            # Daniel's feet are clear of the pit
    t_jump = snap(t_top + 0.12)                        # he springs out onto the ground...
    t_land = snap(t_jump + 0.42)
    t_hug = snap(t_land + 0.1)                         # ...and the king hugs him
    t_look = snap(L1.start + 0.2)                      # "大家看了又看"
    t_turn1 = snap(L1.start + 0.55)                    # Daniel turns round to show himself...
    t_turn2 = snap(L1.start + 1.15)                    # ...and back
    t_safe = snap(L1.at("但以理身上") + 0.1)            # "但以理身上一点伤也没有": arms up, sparkles
    t_trust = snap(L1.at("因为他") + 0.05)              # "因为他信靠他的上帝": kneels, thanks, God's light
    t_off = snap(L2.start + 0.1)                       # "那些想害但以理的官员" (camera already there)
    t_sad = snap(L2.start + 0.5)                       # they hang their heads
    t_lead = snap(L2.at("后来") + 0.05)                 # "后来自己受到了惩罚": led away
    t_pan0, t_pan1 = L1.end + 0.05, L2.start + 1.7

    # ---- camera ----
    C0 = Cam(1300, 610, 1800)
    C1 = Cam(1080, 676, 1400)
    C2 = Cam(2560, 560, 1720)
    C3 = Cam(2700, 560, 1720)
    sc.camera = cam_path([(0, C0), (t_top - 0.4, C0), (t_look + 0.6, C1), (t_pan0, C1), (t_pan1, C2),
                          (t_lead + 0.3, C2), (T, C3)])

    # ---- backdrop ----
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg(), z=0.5, wc=0.6, motion=M.drift(vx=-7))
    sc.add("far", far_svg(), z=1, seed=FAR_SEED)
    sc.add("rays", rays_svg(), z=1.5, wc=0, blend="screen", motion=lambda t: Tf(
        alpha=0.85 * M.progress(t, t_trust - 0.3, t_trust + 0.7, "sine") * (1 - M.progress(t, t_pan0 + 0.4, t_pan0 + 1.8, "sine"))))

    # doves flying over in the sunshine
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = (0, 1, 2, 3, 4, 3, 2, 1)
    for i, (x0, y0, x1, y1, ta, tb, s) in enumerate(((300, 260, 1900, 200, 6.6, 13.0, 0.5),
                                                     (2100, 330, 3500, 230, 12.6, T + 0.5, 0.45))):
        fr = [doc(PR.dove(x0, y0, s, 1, wing=w)) for w in wings]

        def mv(t, x0=x0, y0=y0, x1=x1, y1=y1, ta=ta, tb=tb, i=i):
            u = (t - ta) / (tb - ta)
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            a = min(1.0, u / 0.06, (1 - u) / 0.06)
            return Tf(dx=(x1 - x0) * u, dy=(y1 - y0) * u + 12 * math.sin(2 * math.pi * t / 1.6 + i), alpha=a)
        sc.add(f"dove{i}", fr, z=1.6, frame_at=lambda t, i=i: float(cyc[int(t * 10 + i * 3) % 8]), motion=mv,
               seed=800 + i)

    # ---- the pit (outside view), the stone rolled aside, the A-frame ----
    sc.add("stone", doc(PR.den_stone(HX + 300, G - 34, 0.8, roll=160)), z=2)
    sc.add("den_back", doc(PR.lion_den(HX, G, DSO, view="outside", part="back")), z=2.2)

    # Daniel hauled up: he rises in tugs (one per haul) on the rope hanging from the wheel
    rise_total = DAN_Y0 - DAN_Y1

    def rise(t):
        return sum(rise_total / N_PULL * M.progress(t, tk, tk + 0.28, "inout") for tk in pulls)
    rope_hang = rope_d([(ROPE_X, WHEEL_Y), (ROPE_X, G + 120)])
    sc.add("rope_hang", doc(PR.in_den_hole(rope_svg(rope_hang), HX, G, DSO)), z=2.3)
    def dan_in_motion(t):
        if t >= t_jump:
            return Tf(alpha=0.0)
        return Tf(dy=rise_total - rise(t))
    # (drawn at the TOP of the haul and moved down: the layer is rasterised inside the stage)
    sc.add("dan_hole", [doc(C.daniel(DAN_X, DAN_Y1, 1.0, -1, pose="hold_rope")),
                        doc(C.daniel(DAN_X, DAN_Y1, 1.0, -1, pose="hold_rope", expr="d11_blink_happy"))],
           z=2.4, frame_at=cuts(with_blinks([(0, 0)], {0: 1}, [t_pull0 + 1.2, t_top - 0.4])), motion=dan_in_motion)
    # the occluder: the backdrop below the pit's centre line, minus the hole's lower half, repainted over him
    rx, ry = PR.DEN_HOLE[0] * DSO, PR.DEN_HOLE[1] * DSO
    occ = (f"M{HX - 420},{G} L{HX + 420},{G} L{HX + 420},{G + 640} L{HX - 420},{G + 640} Z "
           f"M{HX - rx},{G} A{rx},{ry} 0 0 0 {HX + rx},{G} Z")
    far_doc = far_svg()
    i0 = far_doc.index("</defs>") + len("</defs>")
    occ_doc = (far_doc[:i0] + f'<clipPath id="occ12"><path d="{occ}" clip-rule="evenodd"/></clipPath>'
               f'<g clip-path="url(#occ12)">' + far_doc[i0:-len("</svg>")] + "</g></svg>")
    sc.add("occluder", occ_doc, z=2.5, seed=FAR_SEED, wc_edge=0.0)
    sc.add("den_front", doc(PR.lion_den(HX, G, DSO, view="outside", part="front")), z=2.6)
    sc.add("frame", frame_svg(), z=2.7)
    wheel_fr = [doc(wheel_markup(r)) for r in (0, 15, 30)]
    sc.add("wheel", wheel_fr, z=2.75, frame_at=lambda t: float(int(rise(t) / 14) % 3))

    # the guards haul: rope from the wheel down through their fists, the end trailing behind
    gx = (HX + 480, HX + 670)
    gv = (0, 2)
    pts = [(ROPE_X + 2 * WHEEL_R, WHEEL_Y)]
    for x, v in zip(gx, gv):
        far, near = C.hand_positions(C.guard, x, G, GS, -1, variant=v, pose="pull_rope")
        pts += [far, near]
    tail = [(pts[-1][0] + 50, pts[-1][1] + 60), (pts[-1][0] + 70, G - 4), (pts[-1][0] + 170, G + 4)]
    haul_d = rope_d(pts) + " " + S.smooth_path([pts[-1]] + tail, closed=False).replace("M", "L", 1)
    # after they let go: rope tied off, hanging slack from the wheel to a peg
    slack_d = S.smooth_path([(ROPE_X + 2 * WHEEL_R, WHEEL_Y), (ROPE_X + 2 * WHEEL_R + 90, G - 230),
                             (gx[0] - 140, G - 10), (gx[0] - 40, G + 6), (gx[1] + 40, G + 8)], closed=False)
    t_let = snap(t_top + 0.25)
    sc.add("rope_haul", [doc(rope_svg(haul_d)), doc(rope_svg(slack_d))], z=2.8, frame_at=cuts([(0, 0), (t_let, 1)]))
    for i, (x, v) in enumerate(zip(gx, gv)):
        def G_(pose, expr=None, x=x, v=v, f=-1):
            return doc(C.ground_shadow(x, G, GS, 130) + C.guard(x, G, GS, f, variant=v, pose=pose, expr=expr,
                                                                   spear=False))
        fr = [G_("pull_rope", "tired"), G_("stand", "surprised"), G_("stand", "happy"),
              G_("stand", "d11_blink_happy"), G_("pull_rope", "happy")]
        pv = (x, G)
        gc = with_blinks([(0, 4), (t_pull0 - 0.2, 0), (t_let, 1), (snap(t_safe + 0.1 + 0.08 * i), 2)], {2: 3},
                         [8.6 + i, 11.3 - i * 0.4, 14.0, 16.5 + i * 0.5])
        sc.add(f"guard{i}", fr, z=3 + 0.01 * i, frame_at=cuts(gc), motion=M.combine(
            M.breathe(0.012, 2.8, pivot=pv, phase=0.3 * i),
            lambda t, x=x: Tf(rot=sum(5 * math.sin(math.pi * M.progress(t, tk - 0.04, tk + 0.32, "linear"))
                                      for tk in pulls), px=x, py=G),
            dip(t_let, GS, pv, 6), happy_hop(snap(t_safe + 0.1 + 0.08 * i), GS, pv, 12),
            # they lean in to look him over
            hop(t_look + 0.1 * i, [(0, {"rot": 0}), (0.4, {"rot": -5}), (1.1, {"rot": -5}), (1.5, {"rot": 0})], pv)))

    # ---- onlookers at the left (palace servants and townsfolk who came with the king) ----
    crowd = [("man", 1, 300, G - 60, 0.82), ("woman", 0, 455, G - 40, 0.82), ("child", 2, 560, G - 10, 0.85)]
    for i, (kind, v, x, y, s) in enumerate(crowd):
        def P_(pose, expr=None, kind=kind, v=v, x=x, y=y, s=s):
            return doc(C.ground_shadow(x, y, s, 110) + C.citizen(x, y, s, 1, kind=kind, variant=v, pose=pose,
                                                                    expr=expr))
        fr = [P_("listen"), P_("stand", "surprised"), P_("cheer"), P_("stand", "happy"),
              P_("stand", "d11_blink_happy")]
        pv = (x, y)
        t_s = snap(t_land + 0.15 + 0.1 * i)
        t_c = snap(t_safe + 0.15 + 0.12 * i)
        t_r = snap(t_trust + 0.5 + 0.1 * i)
        cc = with_blinks([(0, 0), (t_s, 1), (t_c, 2), (t_r, 3)], {3: 4}, [2.0 + i, 13.0 + i * 0.6, 16.2])
        sc.add(f"crowd{i}", fr, z=3.2 + 0.01 * i, frame_at=cuts(cc), motion=M.combine(
            M.breathe(0.012, 2.6 + 0.2 * i, pivot=pv), dip(t_s, s, pv, 5), happy_hop(t_c, s, pv, 16),
            hop(t_c + 0.5, [(0, {"dy": 0}), (0.17, {"dy": -12 * s}), (0.34, {"dy": 0})], pv),
            dip(t_r, s, pv, 5),
            hop(t_look + 0.15 * i, [(0, {"rot": 0}), (0.4, {"rot": 4}), (1.1, {"rot": 4}), (1.5, {"rot": 0})], pv)))

    # ---- Daniel free: springs out, hugged, looked over, arms up, kneels in thanks ----
    dx_ = HUG_DX
    D = lambda pose, expr=None, f=-1: doc(C.ground_shadow(dx_, G, 1.0, 140) +        # noqa: E731
                                          C.daniel(dx_, G, 1.0, f, pose=pose, expr=expr))
    dfr = [doc(C.daniel(DAN_X, DAN_Y1, 1.0, -1, pose="arms_up")),     # 0 leaping out of the pit for joy
           D("stand", "happy"),                                        # 1 hugged
           D("stand", "happy", 1),                                     # 2 turned round
           D("arms_up", "happy"),                                      # 3 not a scratch!
           D("kneel_up", "happy"),                                     # 4 thanks to God
           D("stand", "d11_blink_happy"), D("arms_up", "d11_blink_happy"), D("kneel_up", "d11_blink_happy")]
    jx, jy = dx_ - DAN_X, G - DAN_Y1

    def dan_free_motion(t):
        if t < t_jump - 0.001:
            return Tf(alpha=0.0)
        if t < t_land:
            u = (t - t_jump) / (t_land - t_jump)
            ue = M.ease("inout")(u)
            return Tf(dx=jx * ue, dy=jy * u - 110 * math.sin(math.pi * u), rot=-6 * math.sin(math.pi * u),
                      px=DAN_X, py=DAN_Y1)
        return Tf(dx=SHOW_DX * M.progress(t, t_look - 0.05, t_look + 0.3, "inout"),
                  dy=-26 * math.sin(math.pi * M.progress(t, t_look - 0.05, t_look + 0.3, "linear")))
    pvd = (dx_ + SHOW_DX, G)
    d_entries = [(0, 0), (t_land, 1), (t_turn1, 2), (t_turn2, 1), (t_safe, 3), (snap(t_safe + 1.6), 1), (t_trust, 4)]
    sc.add("daniel", dfr, z=3.5, frame_at=cuts(with_blinks(d_entries, {1: 5, 3: 6, 4: 7}, [7.9, 11.6, 14.6, 17.3])),
           motion=M.combine(dan_free_motion, M.breathe(0.01, 3.0, pivot=pvd),
                            hop(t_land, [(0, {"sy": 0.9, "dy": 4}), (0.18, {"sy": 1.02, "dy": 0}),
                                         (0.32, {"sy": 1, "dy": 0})], pvd),
                            happy_hop(t_turn1, 1.0, pvd, 12), happy_hop(t_turn2, 1.0, pvd, 12),
                            happy_hop(t_safe, 1.0, pvd, 20), dip(snap(t_safe + 1.6), 1.0, pvd, 5),
                            dip(t_trust, 1.0, pvd, 8)))
    # the king: happy at the rim, arms up, waves them on, hugs Daniel, looks him over, rejoices
    kx = KX
    K = lambda pose, expr=None: doc(C.ground_shadow(kx, G, KS, 130) +                  # noqa: E731
                                    C.king(kx, G, KS, 1, pose=pose, attire="darius", expr=expr))
    kfr = [K("reach_out", "happy"),      # 0 (as s11 ended)
           K("arms_up", "happy"),        # 1 "高兴极了"
           K("reach_out", "call"),       # 2 "马上叫人…"
           K("stand", "happy"),          # 3 watching him come up
           K("hug", "happy"),            # 4
           K("stand", "surprised"),      # 5 looking him over
           K("arms_up", "happy"),        # 6 not a scratch!
           K("stand", "happy"),          # 7
           K("stand", "d11_blink_happy"), K("reach_out", "d11_blink_happy")]   # 8, 9
    k_entries = [(0, 0), (t_joy, 1), (t_order, 2), (snap(t_order + 1.3), 3), (t_hug, 4), (t_look, 5),
                 (t_safe, 6), (snap(t_safe + 1.6), 7)]
    pvk = (kx, G)
    sc.add("king", kfr, z=3.6, frame_at=cuts(with_blinks(k_entries, {0: 9, 3: 8, 7: 8}, [0.5, 4.0, 11.2, 13.8, 16.7])),
           motion=M.combine(M.breathe(0.01, 3.1, pivot=pvk), happy_hop(t_joy, KS, pvk, 22), dip(t_order, KS, pvk, 6),
                            dip(snap(t_order + 1.3), KS, pvk, 4), dip(t_hug, KS, pvk, 8),
                            # a happy rock during the hug
                            hop(t_hug, [(0.1, {"rot": 0}), (0.45, {"rot": -3}), (0.8, {"rot": 2}), (1.1, {"rot": 0})],
                                pvk),
                            dip(t_look, KS, pvk, 5),
                            hop(t_look, [(0.15, {"rot": 0}), (0.5, {"rot": 6}), (1.2, {"rot": 6}), (1.6, {"rot": 0})],
                                pvk),
                            happy_hop(t_safe, KS, pvk, 18), dip(snap(t_safe + 1.6), KS, pvk, 5)))

    # little twinkles round Daniel's robe and hands (never on his face): "not a scratch on him"
    sx_ = dx_ + SHOW_DX
    tw = [(sx_ + 115, G - 350, 20), (sx_ + 140, G - 210, 16), (sx_ - 85, G - 130, 16), (sx_ + 85, G - 60, 18),
          (sx_ - 60, G - 40, 13), (sx_ + 60, G - 150, 12)]
    sc.add("twinkles", [doc(sparkle_markup(tw, k)) for k in range(3)], z=3.7, wc=0,
           frame_at=lambda t: float(int(t * 6) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_safe, t_safe + 0.25) * (1 - M.progress(t, t_safe + 1.6, t_safe + 2.0))))

    # ---- the officials, and the guards who lead them away ----
    OF = [(0, 2330), (1, 2490), (2, 2650)]
    ESC = [(1, 2170), (3, 2830)]
    t_seen = snap(t_safe + 0.3)
    WALK_P = 0.36
    n_steps = int((T - t_lead) / WALK_P) + 2
    for i, (v, x) in enumerate(OF):
        fa_w, dxw, dyw, _ = step_walk(t_lead + 0.12 * i, n_steps, 80 * OS, WALK_P, OS)
        O = lambda pose, expr=None, f=-1, x=x, v=v: doc(C.ground_shadow(x, G2, OS, 120) +   # noqa: E731
                                                        C.official(x, G2, OS, f, variant=v, pose=pose, expr=expr))
        fr = [O("scheme", "sly"), O("stand", "surprised"), O("sad"), O("walk_a", "sad", 1), O("walk_b", "sad", 1),
              O("stand", "worried"), O("stand", "d11_blink_worried")]
        base = cuts(with_blinks([(0, 0), (t_seen + 0.1 * i, 1), (snap(t_safe + 2.2 + 0.1 * i), 5),
                                 (t_sad + 0.1 * i, 2)], {5: 6}, [11.4 + 0.3 * i, 13.4 - 0.2 * i]))

        def fa(t, base=base, fa_w=fa_w):
            w = fa_w(t)
            return base(t) if w is None else 3.0 + w
        pv = (x, G2)
        sc.add(f"official{i}", fr, z=2.9 + 0.01 * i, frame_at=fa, motion=M.combine(
            lambda t, dxw=dxw, dyw=dyw: Tf(dx=dxw(t), dy=dyw(t)), M.breathe(0.012, 2.7, pivot=pv, phase=0.2 * i),
            hop(t_seen + 0.1 * i, [(-0.08, {"dy": 0}), (0.1, {"dy": -12 * OS}), (0.25, {"dy": 0})], pv),
            dip(t_sad + 0.1 * i, OS, pv, 6)))
    for i, (v, x) in enumerate(ESC):
        fa_w, dxw, dyw, _ = step_walk(t_lead + (0.3 if i == 0 else -0.1), n_steps, 80 * OS, WALK_P, OS)
        Gd = lambda pose, expr=None, f=-1, x=x, v=v: doc(C.ground_shadow(x, G2, OS, 120) +  # noqa: E731
                                                         C.guard(x, G2, OS, f, variant=v, pose=pose, expr=expr))
        frames = [Gd("stand"), Gd("stand", "d11_blink_neutral"), Gd("stand", None, 1), Gd("walk_a", None, 1),
                  Gd("walk_b", None, 1)]
        t_face = snap(t_lead - 0.4 + 0.1 * i)  # the guards turn round to lead them off (squash)
        base = cuts(with_blinks([(0, 0), (t_face, 2)], {0: 1}, [9.5 + i, 12.0 + i]))

        def fa(t, base=base, fa_w=fa_w):
            w = fa_w(t)
            if w is None:
                return base(t)
            return 3.0 + w
        pv = (x, G2)
        sc.add(f"escort{i}", frames, z=2.85 + 0.01 * i, frame_at=fa, motion=M.combine(
            lambda t, dxw=dxw, dyw=dyw: Tf(dx=dxw(t), dy=dyw(t)), M.breathe(0.012, 2.9, pivot=pv, phase=0.5 * i),
            dip(t_face, OS, pv, 6)))

    # ---- sound ----
    sc.sfx("birds", 0.0, dur=T, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-20, fade_in=0.8, fade_out=0.8)
    for k, tk in enumerate(pulls):
        sc.sfx("cloth", tk + 0.05, gain_db=-15, pan=0.2)
    sc.sfx("ship_creak", t_pull0, dur=t_top - t_pull0 + 0.2, gain_db=-14)
    sc.sfx("whoosh", t_jump, gain_db=-12)
    sc.sfx("thud", t_land, gain_db=-9)
    sc.sfx("cheer", t_land + 0.1, dur=t_pan0 + 1.0 - t_land, gain_db=-13, fade_in=0.4, fade_out=1.2)
    sc.sfx("sparkle", t_safe + 0.05, gain_db=-10)
    sc.sfx("chime", t_trust, gain_db=-12)
    sc.sfx("footsteps", t_lead, dur=T - t_lead, gain_db=-14, pan=0.35, fade_out=0.8)
    return sc
