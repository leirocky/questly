"""Scene 14 - Mark 5:1. The next morning: the little fishing boat arrives safely on the far shore of the lake. It
starts exactly where s13 ends (a plain cross-dissolve: the same dawn lake, boat, crew and camera at the cut), the
sail drops open in the morning breeze, the boat glides across the pink-gold lake and noses gently onto a rocky beach
below a wooded headland; the sun rises over the headland, the water sparkles. Then the disciples step off the bow
one after another onto the beach, look back at Jesus and at each other, wondering; Jesus steps ashore last, smiling.

Beats (syllable onsets measured in the voice clip, see s03_friends.Beats; nothing hard-coded to the take):
  0 .. 1       identical to the end of s13 (dawn, the crew looking at Jesus with awe, his soft glow fading)
  '第二天早上'  the disciples turn to look ahead toward the shore (squash-dip pose cuts); on '早上' the sail drops
               open from the yard (cloth, whoosh) and the boat starts to glide (soft wake)
  '平平安安'    the boat glides on, the camera travels with it; the far shore with its boulders and trees comes in
  '那一边'      the bow touches the beach on '边' (a little jolt through the crew, foam at the bow, thud)
  '太阳出来了'  the sun rises over the headland (rays, warm light, birds)
  '亮晶晶的'    sparkles dance on the water (sparkle)
  line 2       '门徒们一边走下船': the disciples walk forward along the boat and hop off the bow onto the beach one
               after another (planted-foot strides, footsteps), each walks to a spot and turns back to look at Jesus
               (squash-dip cuts); Jesus stands up and follows behind them
  '到底是谁呢'  two question marks pop up over two disciples' heads (pop)
  end          Jesus steps ashore last and stops, smiling at his friends; calm last frame (page dip to s15)
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
from stories.noah.scenes.s01_title import cuts, snap
from stories.storm.scenes.s03_friends import Beats, blink, blink_entries, disc, f1, jes, squash

INK = P["ink"]
WS, HS = 3640, 1188            # panorama stage shared with s13
LY2, LS2 = 725, 0.5            # lake_galilee near-shore reference and scale
YF2 = LY2 - 250 * LS2          # far shoreline (600)
K = 0.55                       # boat and people
BY = 905                       # the boat's waterline (= the near row's floor)
X_LAND = 2250                  # boat x when the bow rests on the beach
X_START = 1150                 # boat x at the start of s14 (u = 0)
V0 = 25.0                      # drift speed (px/s) at the s13 -> s14 cut
U_A0 = 1.25                    # the glide never accelerates before this (u <= 1 stays a pure drift for the dissolve)
SUN_X = 3170
SUN_LOW, SUN_HIGH = 585, 335
SAIL_PH = 0.0

# crew in the boat (local boat x, variant); near row on the floor (y 0), far row behind (y -40)
NEAR = [(-215, 6), (-75, 7), (70, 9), (222, 3), (386, 1), (548, 0)]
FAR = [(-300, 5), (-150, 8), (-5, 10), (148, 11), (306, 4), (468, 2)]
JESUS_SIT = PR.STERN_SEAT            # (-455, -100)
JESUS_STAND = (-410, -20)            # where he stands up, between the rows

# explicit watercolour seeds for every layer shared with s13 (identical pixels across the dissolve)
SEED = {"sky": 1401, "glowpre": 1402, "clouds": 1403, "hills": 1404, "water": 1405, "land": 1406, "boat_back": 1410,
        "furled": 1411, "jesus": 1412, "jglow": 1413, "boat_front": 1414, "lantern": 1415, "band": 1416,
        "wline": 1417}


def crew_seed(v):
    return 1500 + 7 * v


def doc(body, defs=""):
    return S.svg_doc(body, defs, WS, HS)


def lp(lx, ly):
    """Boat-local point -> stage point with the boat landed (all crew frames are drawn there)."""
    return (X_LAND + lx * K, BY + ly * K)


# ================================================================== the boat's path and the camera


def boat_x(u, u_touch=5.4, u_a=U_A0):
    """Boat x at s14 time u: a constant drift (also used by s13 for u < 0), then a smooth glide that comes to rest
    on the beach at u_touch (cubic Hermite: starts at the drift speed, ends at speed 0)."""
    u_a = max(U_A0, u_a)
    xa = X_START + V0 * u_a
    if u <= u_a:
        return X_START + V0 * u
    if u >= u_touch:
        return X_LAND
    T = u_touch - u_a
    s = (u - u_a) / T
    D = X_LAND - xa
    m0 = V0 * T / D
    h = (s ** 3 - 2 * s * s + s) * m0 + (-2 * s ** 3 + 3 * s * s)
    return xa + D * h


def boat_bob(u, u_touch=5.4):
    """Gentle bob of the floating boat (it settles once beached)."""
    k = 1.0 - M.progress(u, u_touch - 0.3, u_touch + 1.2, "sine")
    a = 2 * math.pi * u / 3.6
    return 2.6 * k * math.sin(a), 0.7 * k * math.sin(a + 1.1)


def follow_cam(u, u_touch=5.4, u_a=U_A0):
    """The camera that travels with the boat (s14's opening framing; s13 ends on it)."""
    return Cam(boat_x(u, u_touch, u_a) + 60, 650, 1720)


def clamp_cam(c):
    cw = min(c.w, WS, HS * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2), WS - cw / 2), min(max(c.y, ch / 2), HS - ch / 2), cw, c.rot)


def boat_motion(U, u_touch=5.4, u_a=U_A0, jolt=None):
    """Motion of everything drawn in landed coordinates that rides in the boat. U maps scene time -> s14 time."""
    piv = (X_LAND, BY)

    def m(t):
        u = U(t)
        dy, rot = boat_bob(u, u_touch)
        if jolt is not None:
            v = u - jolt
            if 0 <= v < 0.5:
                rot += -1.2 * math.sin(math.pi * v / 0.5) * (1 - v / 0.5)
                dy += 2.0 * math.sin(math.pi * v / 0.5)
        return Tf(dx=boat_x(u, u_touch, u_a) - X_LAND, dy=dy, rot=rot, px=piv[0], py=piv[1])
    return m


# ================================================================== backdrop drawings (dawn; s13 also uses them)


def sky_svg():
    """Dawn sky (lake_galilee 'dawn' colours and clouds), its own sun hidden: ours rises on its own layer."""
    return doc(PR.lake_galilee(-20, WS + 20, LY2, LS2, time="dawn", part="back", far_shore=False, boats=False,
                               top=-60, sun_x=-9.0))


def preglow_svg():
    """The warm glow behind the headland before (and while) the sun rises."""
    defs = S.rad_grad("s14pg", [(0, "#fff0c8", 0.85), (0.35, "#fbd9a6", 0.45), (1, "#f8c6a0", 0)])
    return doc(f'<ellipse cx="{SUN_X}" cy="{YF2 - 60}" rx="700" ry="380" fill="url(#s14pg)"/>', defs)


def hills_svg():
    return doc(PR.lake_galilee(-20, WS + 20, LY2, LS2, time="dawn", part="back", sky=False, boats=False, top=-60))


def water_svg(time="dawn"):
    return doc(PR.calm_lake(-20, WS + 20, YF2 + 2, time=time, scale=0.62, sparkle=0.4, seed=7, bottom=HS + 60))


def sun_svg():
    x, y, r = SUN_X, SUN_LOW, 40
    defs = S.rad_grad("s14sun", [(0, "#fff6d6", 0.95), (0.3, "#fde6a2", 0.55), (1, "#fbd78a", 0)])
    b = f'<circle cx="{x}" cy="{y}" r="{r * 4.6}" fill="url(#s14sun)"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff1c4" stroke="{S.mix(INK, "#fbd46b", 0.55)}" stroke-width="3"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r * 0.78}" fill="#fde7a0" opacity="0.7"/>'
    return doc(S.g(b, filter="wobble"), defs)


def rays_svg():
    defs = S.rad_grad("s14ray", [(0, "#fff3cc", 0.55), (0.6, "#ffe9b0", 0.18), (1, "#ffe9b0", 0)])
    d = S.rays(SUN_X, SUN_HIGH, 70, 900, n=14, width_deg=6)
    return doc(f'<path d="{d}" fill="url(#s14ray)"/>', defs)


# the water's edge of the far shore (top right -> bottom left); the bow rests at (2646, 905)
EDGE = [(2862, 800), (2760, 842), (2690, 882), (2648, 905), (2616, 945), (2566, 1030), (2508, 1120), (2462, 1215)]
HEAD = [(2862, 800), (2900, 720), (2960, 640), (3050, 560), (3150, 505), (3260, 478), (3360, 466), (3480, 470),
        (3580, 482), (3680, 492)]


def _inside(px, py, poly):
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-9) + x1:
            c = not c
    return c


def land_svg():
    """The rocky far shore (Mark 5:1): a wooded headland on the right, a pebbly beach below it with boulders at the
    water's edge, where the boat lands. Dawn-tinted (the same tint as lake_galilee 'dawn')."""
    tint = lambda c, k=0.12: PR._tint(c, "dawn", k)          # noqa: E731
    rng = random.Random(14)
    out = ""
    # the headland
    head = HEAD + [(3680, 915), (3500, 900), (3300, 890), (3120, 872), (2960, 850), (2880, 825)]
    hd = S.smooth_path(head, closed=True, tension=0.8)
    out += S.path(hd, fill=tint("#a8987a"), sw=4)
    strata = S.smooth_path([(2930, 700), (3040, 640), (3180, 600), (3320, 590), (3480, 600), (3680, 610)], closed=False)
    out += S.path(strata + " L3680,905 L2930,905 Z", fill=tint("#978a6c"), sw=3)
    for i in range(9):                                   # rock outcrops
        rx = 2950 + 75 * i + rng.uniform(-20, 20)
        ry = 620 + 28 * (i % 4) + rng.uniform(-8, 8) + (0 if rx > 3050 else 60)
        r = rng.uniform(26, 40)
        c = tint(PR.BASALT_LIGHT if i % 2 else "#b0a088")
        out += S.path(S.blob(rx, ry, r * 1.4, r * 0.8, 0.18, 7, seed=60 + i), fill=c, sw=3)
        out += S.path(f"M{f1(rx - r * 0.8)},{f1(ry - r * 0.3)} q{f1(r * 0.5)},{f1(-r * 0.3)} {f1(r * 1.0)},{f1(-r * 0.1)}",
                      stroke=False, extra=f'stroke="{S.shade(c, 0.4)}" stroke-width="3" fill="none" opacity="0.7"')
    for i in range(14):                                  # grass patches on the slope
        gx = 2940 + rng.uniform(0, 700)
        gy = 560 + rng.uniform(0, 280) + max(0, 3000 - gx) * 0.8
        if _inside(gx, gy, head):
            out += PR._place(PR._grass(i % 3, 0.0), gx, gy, 0.42, 1, filt=None)
    # trees: terebinths with round dark crowns along the crest
    for i, (tx, ty, k) in enumerate(((2985, 640, 0.62), (3075, 575, 0.72), (3230, 520, 0.8), (3345, 505, 0.7),
                                     (3440, 510, 0.66), (3140, 560, 0.55), (3550, 520, 0.74), (3630, 530, 0.6))):
        out += PR._tube(f"M{tx},{ty} Q{tx - 6 * k},{ty - 50 * k} {tx + 6 * k},{ty - 100 * k}", 15 * k,
                        tint(P["wood_dark"]), 3 * k)
        out += PR._tube(f"M{tx + 2 * k},{ty - 60 * k} L{tx + 40 * k},{ty - 100 * k}", 8 * k, tint(P["wood_dark"]), 3 * k)
        for j, (dx, dy, w) in enumerate(((-30, -120, 120), (40, -112, 100), (6, -160, 110))):
            out += S.cloud(tx + dx * k, ty + dy * k, w * k, w * 0.62 * k, fill=tint(("#5f8a4a", "#6f9a52", "#557f42")[j]),
                           seed=140 + i * 3 + j, puffs=4, sw=3 * k, shade_fill=tint("#46703a"))
    # the beach
    sand = EDGE + [(3680, 1215), (3680, 915), (3500, 900), (3300, 890), (3120, 872), (2960, 850), (2880, 825)]
    sd = S.smooth_path(EDGE, closed=False, tension=0.9) + " L3680,1215 L3680,915 " + \
        S.smooth_path([(3680, 915), (3500, 900), (3300, 890), (3120, 872), (2960, 850), (2880, 826), (2862, 800)],
                      closed=False).replace("M", "L", 1) + " Z"
    defs = S.lin_grad("s14sand", [(0, tint("#efd7ae")), (0.5, tint("#e6c99a")), (1, tint("#d6b483"))], 0, 0, 0, 1)
    out += f'<path d="{sd}" fill="url(#s14sand)"/>'
    out += S.path(S.smooth_path([(3680, 915), (3500, 900), (3300, 890), (3120, 872), (2960, 850), (2880, 826)], closed=False),
                  stroke=False, extra=f'stroke="{S.shade(tint("#d6b483"), -0.15)}" stroke-width="3" fill="none" opacity="0.6"')
    ed = S.smooth_path(EDGE, closed=False, tension=0.9)
    cid = "s14sandclip"
    wet = (f'<path d="{ed}" fill="none" stroke="{tint("#c9a878")}" stroke-width="34" opacity="0.55"/>'
           f'<path d="{ed}" fill="none" stroke="{tint("#b89668")}" stroke-width="12" opacity="0.4"/>')
    out += f'<clipPath id="{cid}"><path d="{sd}"/></clipPath><g clip-path="url(#{cid})">{wet}</g>'
    out += f'<path d="{ed}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    foam = S.smooth_path([(x - 10, y - 5) for x, y in EDGE], closed=False, tension=0.9)
    out += f'<path d="{foam}" fill="none" stroke="#fff6ea" stroke-width="5" stroke-dasharray="40 24" opacity="0.85"/>'
    # pebbles
    peb = ""
    for _ in range(110):
        px, py = rng.uniform(2470, 3660), rng.uniform(880, 1190)
        if not _inside(px, py, sand) or _inside(px, py, head):
            continue
        r = rng.uniform(4, 9)
        peb += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r * 1.3)}" ry="{f1(r)}" '
                f'fill="{tint(rng.choice(("#b8ab98", "#8f8a84", "#c9b9a0", PR.BASALT_LIGHT)))}" stroke="{INK}" '
                f'stroke-width="1.8"/>')
    out += peb
    # boulders at the water's edge (clear of the landing spot and the path up the beach)
    for i, (bx, by, r) in enumerate(((2858, 812, 42), (2800, 832, 30), (2560, 1040, 50), (2520, 1120, 38),
                                     (2600, 1150, 30), (3520, 1080, 46), (3580, 1010, 32), (2930, 842, 26), (3460, 1150, 28))):
        c = tint((PR.BASALT, PR.BASALT_LIGHT, "#a39484")[i % 3])
        out += S.path(S.blob(bx, by - r * 0.5, r * 1.3, r * 0.7, 0.14, 8, seed=80 + i), fill=c, sw=3.4)
        out += S.path(f"M{f1(bx - r * 0.7)},{f1(by - r * 0.8)} q{f1(r * 0.4)},{f1(-r * 0.25)} {f1(r * 0.9)},{f1(-r * 0.1)}",
                      stroke=False, extra=f'stroke="{S.shade(c, 0.35)}" stroke-width="3" fill="none" opacity="0.7"')
    for i, (gx, gy, s_, v) in enumerate(((2700, 905, 0.38, 0), (2840, 860, 0.34, 1), (3420, 1170, 0.6, 2),
                                          (3250, 1196, 0.5, 0), (2985, 870, 0.3, 2), (3600, 1120, 0.5, 1))):
        out += PR._place(PR._grass(v, 0.0), gx, gy, s_, 1, filt=None)
    out += PR._place(PR._reeds(1, 0.1), 2805, 845, 0.3, 1, filt=None)
    return doc(S.g(out, filter="wobble"), defs)


def band_svg(time="dawn"):
    """The lake again, clipped to the strip in front of the hull along its whole path (and never over the beach):
    it hides the keel below the waterline."""
    top = S.wave_line(BY - 3, 2.5, 120, 0.0, x0=300, x1=2700)
    d = top + f" L2700,{BY - 3} L2648,{BY} L2616,945 L2600,{BY + 60} L300,{BY + 60} Z"
    cid = f"s14band{time}"
    lake = PR.calm_lake(-20, WS + 20, YF2 + 2, time=time, scale=0.62, sparkle=0.0, seed=7, bottom=HS + 60)
    return doc(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{lake}</g>')


def waterline_svg():
    """A light waterline along the hull and soft ripples round it (rides with the boat)."""
    b = ""
    for x0, x1, dy, w, op in ((-760, 700, 2, 4, 0.75), (-700, 600, 12, 3, 0.45), (-560, 420, 22, 2.6, 0.3)):
        b += (f'<path d="{S.wave_line(BY + dy, 2.4, 70, 0.0, x0=X_LAND + x0 * K, x1=X_LAND + x1 * K)}" fill="none" '
              f'stroke="#fff3dc" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"))


def wake_svg(k):
    """V-shaped wake ripples trailing from the stern while the boat glides (k 0..2 shifts them back)."""
    b = ""
    sx = X_LAND - 760 * K
    for i in range(3):
        d = 40 + 70 * i + 23 * k
        a = 0.6 - 0.17 * i
        b += (f'<path d="M{f1(sx - d)},{f1(BY + 6 + d * 0.12)} q{f1(-30)},{f1(5)} {f1(-70)},{f1(4)}" fill="none" '
              f'stroke="#fff3dc" stroke-width="3.4" opacity="{a:.2f}" stroke-linecap="round"/>'
              f'<path d="M{f1(sx - d * 0.7)},{f1(BY + 18 + d * 0.22)} q{f1(-26)},{f1(6)} {f1(-60)},{f1(8)}" fill="none" '
              f'stroke="#fff3dc" stroke-width="3" opacity="{a * 0.8:.2f}" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"))


# ================================================================== the boat and crew drawings


def boat_back_svg(wet=False):
    return doc(PR.fishing_boat(X_LAND, BY, K, 1, sail="none", part="back", oars="in", cushion=True, wet=wet))


def furled_svg():
    return doc(PR._place(PR._boat_sail("furled", 0.0, "s14furl"), X_LAND, BY, K, 1))


def sail_svg():
    sv, cl, cr = PR._boat_sail("full", SAIL_PH, "s14sail")
    stay = S.shade(INK, 0.12)
    rig = max(3.4, 2.4 / K)
    sheets = (f'<path d="M{f1(cl[0])},{f1(cl[1])} L-440,-165" stroke="{stay}" stroke-width="{rig:.1f}" fill="none"/>'
              f'<path d="M{f1(cr[0])},{f1(cr[1])} L650,-195" stroke="{stay}" stroke-width="{rig:.1f}" fill="none"/>')
    return doc(PR._place(sheets + sv, X_LAND, BY, K, 1))


def boat_front_svg(wet=False):
    out = PR.fishing_boat(X_LAND, BY, K, 1, sail="none", part="front", oars="in", nets=True, wet=wet)
    out += PR._place(f'<path d="M-752,-372 L-760,-352" stroke="{INK}" stroke-width="3" fill="none"/>', X_LAND, BY, K, 1)
    return doc(out)


def lantern_svg(lit):
    x, y = lp(-760, -352)
    return doc(PR.hanging_lantern(x, y, K * 0.8, 0.0, lit=lit))


def jglow_svg():
    x, y = lp(JESUS_SIT[0] + 20, JESUS_SIT[1] - 170)
    defs = S.rad_grad("s14jg", [(0, "#fff4cf", 0.95), (0.35, "#ffe6a8", 0.55), (0.7, "#ffe0a0", 0.18),
                                (1, "#ffe0a0", 0)])
    return doc(f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(330 * K)}" ry="{f1(390 * K)}" fill="url(#s14jg)"/>', defs)


def crew_members():
    """[(variant, row 'near' / 'far', local x, local floor y)]"""
    out = [(v, "near", lx, 0) for lx, v in NEAR] + [(v, "far", lx, -40) for lx, v in FAR]
    return out


def crew_svg(v, lx, ly, facing, pose, expr, wet=False, h=0.0, phase=0.0):
    x, y = lp(lx, ly)
    return doc(disc(x, y, K * (0.97 if ly < 0 else 1.0), facing, v, pose, expr, phase=phase, wet=wet, h=h))


def crew_start_svg(v, lx, ly, wet=False):
    """The pose shared across the s13 -> s14 cut: standing, turned toward Jesus at the stern, in awe."""
    return crew_svg(v, lx, ly, -1, "stand", "awed", wet=wet)


def jesus_sit_svg(expr="warm", glow=0.0):
    x, y = lp(*JESUS_SIT)
    return doc(jes(x, y, K, 1, "sit", expr))


def qmark_svg(x, y, size=70):
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b = (f'<circle cx="{f1(x)}" cy="{f1(y - size * 0.32)}" r="{f1(size * 0.62)}" fill="#fffaf0" stroke="{INK}" '
         f'stroke-width="3.4" opacity="0.92"/>')
    b = S.g(b, filter="wobble-fine")
    b += (f'<text x="{f1(x)}" y="{f1(y)}" {font} fill="#4f8aa8" stroke="{INK}" stroke-width="3" '
          f'paint-order="stroke">？</text>')
    return doc(b)


# ================================================================== the shared opening page (also built by s13)


def add_dawn_backdrop(sc, toff=0.0, z0=0.0):
    """Static dawn backdrop + drifting clouds; motions use u = t + toff."""
    sc.add("d_sky", sky_svg(), z=z0, wc=0.8, seed=SEED["sky"])
    sc.add("d_preglow", preglow_svg(), z=z0 + 0.1, wc=0, seed=SEED["glowpre"])
    sc.add("d_clouds", doc(S.g(S.cloud(900, 150, 260, 74, "#fbf0ea", seed=91, sw=3, shade_fill="#e9cfd8") +
                               S.cloud(2050, 230, 200, 60, "#fbf0ea", seed=92, sw=2.8, shade_fill="#e9cfd8") +
                               S.cloud(2900, 120, 230, 64, "#fbf0ea", seed=93, sw=2.8, shade_fill="#e9cfd8"),
                               filter="wobble")),
           z=z0 + 0.3, seed=SEED["clouds"], motion=lambda t: Tf(dx=6.0 * (t + toff)))
    sc.add("d_hills", hills_svg(), z=z0 + 0.4, wc=0.8, seed=SEED["hills"])
    sc.add("d_water", water_svg("dawn"), z=z0 + 0.5, wc=0.9, seed=SEED["water"])
    sc.add("d_land", land_svg(), z=z0 + 0.6, wc=1.0, seed=SEED["land"])


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=WS, H=HS)
    T = ctx.duration
    B = Beats(ctx)
    U = lambda t: t                                          # noqa: E731

    t_zao = B.at(0, "早上")
    t_bian = B.at(0, "那一边", 2)
    t_sun = B.at(0, "太阳出来了")
    t_chu = B.at(0, "太阳出来了", 2)
    t_spark = B.at(0, "亮晶晶")
    t_l2 = ctx.lines[1].start
    t_who = B.at(1, "到底是谁呢")

    t_unfurl = snap(t_zao + 0.05)
    u_a = max(U_A0, t_unfurl + 0.15)
    u_touch = snap(t_bian + 0.05)
    bm = boat_motion(U, u_touch, u_a, jolt=u_touch)

    # ------------------------------------------------------------ backdrop
    add_dawn_backdrop(sc)
    t_rise0, t_rise1 = snap(t_sun - 0.1), snap(t_chu + 0.9)
    sc.add("sun", sun_svg(), z=0.2, wc=0.3,
           motion=lambda t: Tf(dy=(SUN_HIGH - SUN_LOW) * M.progress(t, t_rise0, t_rise1, "out")))
    sc.add("rays", rays_svg(), z=0.25, wc=0, blend="screen",
           motion=lambda t: Tf(rot=4 * math.sin(2 * math.pi * t / 9.0), px=SUN_X, py=SUN_HIGH,
                               alpha=0.8 * M.progress(t, t_rise1 - 0.5, t_rise1 + 0.8, "sine") *
                               (0.85 + 0.15 * math.sin(2 * math.pi * t / 2.7))))
    # sparkles dancing on the water ('亮晶晶的'), in front of the hills / water, behind the boat
    # (only over open water: never over the boat or the people)
    sc.fx.append(FX.sparkles((1250, BY + 30, 2560, HS - 40), count=22, t0=t_spark - 0.1, color=(255, 246, 214),
                             size=(9, 19), period=1.4, drift=0, seed=141))
    sc.fx.append(FX.sparkles((1250, YF2 + 12, 2140, YF2 + 80), count=11, t0=t_spark - 0.05, color=(255, 246, 214),
                             size=(6, 13), period=1.6, drift=0, seed=143))
    sc.fx.append(FX.sparkles((2610, YF2 + 12, 2840, YF2 + 70), count=4, t0=t_rise1 - 0.4, color=(255, 240, 200),
                             size=(5, 10), period=1.9, drift=0, seed=142))
    # warm morning light once the sun is up
    sc.fx.append(FX.tint((255, 214, 150), lambda t: 0.10 * M.progress(t, t_rise0 + 0.3, t_rise1 + 0.6, "sine"),
                         mode="screen"))

    # birds across the morning sky
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (col, y0, vx, ph_, t0) in enumerate((("yellow", 260, -75, 0.0, t_rise1 - 0.2), ("blue", 310, -68, 0.4,
                                                                                            t_rise1 + 0.3))):
        def fly(t, y0=y0, vx=vx, ph_=ph_, t0=t0, i=i):
            x = 3500 + 120 * i + vx * (t - t0)
            return Tf(dx=x - 200, dy=y0 - 200 + 18 * math.sin(2 * math.pi * (t / 2.2 + ph_)),
                      alpha=1.0 if t >= t0 else 0.0)
        sc.add(f"bird{i}", [doc(PR.songbird(200, 200, 0.34, -1, wing=w, color=col)) for w in wings], z=0.35 + 0.01 * i,
               motion=fly, wc=0.3, frame_at=lambda t, ph_=ph_: float(int(t / 0.07 + ph_ * 8) % 8))

    # ------------------------------------------------------------ the boat
    sc.add("boat_back", boat_back_svg(), z=2, motion=bm, seed=SEED["boat_back"])
    sc.add("furled", furled_svg(), z=2.1, motion=M.combine(bm, lambda t: Tf(alpha=1.0 if t < t_unfurl else 0.0)),
           seed=SEED["furled"])
    sc.add("sail", sail_svg(), z=2.15, motion=M.combine(bm, lambda t: Tf(alpha=1.0 if t >= t_unfurl else 0.0)),
           reveal=lambda t: {"mode": "down", "frac": M.progress(t, t_unfurl, t_unfurl + 0.55, "out"), "soft": 40},
           seed=1420)

    # ------------------------------------------------------------ crew: who leaves when
    members = crew_members()
    order = sorted(members, key=lambda m: -m[2])               # bow first
    exit0 = snap(t_l2 + 0.35)
    gap = 0.36
    stride, period = 46.0, 0.27
    bow_x = 640                                                 # local x where they step over the bow
    entry = (2740, 918)                                         # where they land on the beach
    far_targets = [(3340, 926), (3255, 933), (3170, 926), (3085, 931), (3000, 924), (2915, 930)]
    near_targets = [(3420, 964), (3315, 978), (3225, 963), (3135, 979), (3045, 963), (2955, 977)]
    fi = ni = 0
    plan = []
    for k, (v, row, lx, ly) in enumerate(order):
        if row == "far":
            tgt = far_targets[fi]
            fi += 1
        else:
            tgt = near_targets[ni]
            ni += 1
        plan.append((k, v, row, lx, ly, tgt))
    e_t = {v: snap(exit0 + gap * k) for k, v, *_ in plan}

    # turning to look ahead at '第二天早上' (staggered), looking at the sun, then the walk-off
    t_look = {v: snap(t_zao - 0.25 + 0.06 * (i % 6)) for i, (v, *_r) in enumerate(members)}
    t_sunlook = {v: snap(t_chu + 0.1 + 0.05 * (i % 5)) for i, (v, *_r) in enumerate(members)}

    def walker_path(lx, ly, tgt, t_exit):
        """(position(t) in landed stage coords, frame(t) 'walk' index 0/1 or None) for one walker."""
        p0 = lp(lx, ly)
        p1 = lp(bow_x, ly)
        d_boat = max(0.0, p1[0] - p0[0])
        n_boat = max(1, int(round(d_boat / stride))) if d_boat > 8 else 0
        t_hop0 = t_exit - 0.05
        t_start = snap(t_hop0 - n_boat * period)
        boat_cuts = [snap(t_start + i * period) for i in range(n_boat)]
        hop_d = 0.42
        t_hop1 = snap(t_hop0 + hop_d)
        dx, dy = tgt[0] - entry[0], tgt[1] - entry[1]
        dist = math.hypot(dx, dy)
        n_beach = max(1, int(round(dist / stride)))
        beach_cuts = [snap(t_hop1 + i * period) for i in range(n_beach)]
        t_arrive = snap(t_hop1 + n_beach * period)

        def pos(t):
            if t < t_start:
                return p0, 0.0
            if t < t_hop0:
                k = sum(M.progress(t, c - 0.06, c + 0.09, "sine") for c in boat_cuts)
                x = p0[0] + (d_boat / max(1, n_boat)) * k
                lift = 0.0
                for c in boat_cuts:
                    if c - 0.06 <= t <= c + 0.09:
                        lift = -4 * K * math.sin(math.pi * (t - c + 0.06) / 0.15)
                return (x, p0[1] + lift), 0.0
            if t < t_hop1:
                u = (t - t_hop0) / hop_d
                e = M.ease("sine")(u)
                x = p1[0] + (entry[0] - p1[0]) * e
                y = p1[1] + (entry[1] - p1[1]) * e - 30 * math.sin(math.pi * u)
                return (x, y), 0.0
            if t < t_arrive:
                k = sum(M.progress(t, c - 0.06, c + 0.09, "sine") for c in beach_cuts)
                f = k / n_beach
                lift = 0.0
                for c in beach_cuts:
                    if c - 0.06 <= t <= c + 0.09:
                        lift = -4 * K * math.sin(math.pi * (t - c + 0.06) / 0.15)
                return (entry[0] + dx * f, entry[1] + dy * f + lift), 0.0
            return tgt, 0.0

        def frame(t):
            if t_start <= t < t_hop0:
                return int((t - t_start) / period) % 2
            if t_hop0 <= t < t_hop1:
                return 0
            if t_hop1 <= t < t_arrive:
                return int((t - t_hop1) / period) % 2
            return None
        return pos, frame, t_start, t_arrive, t_hop0

    q_who = {}                      # variant -> question-mark time
    for idx, (k, v, row, lx, ly, tgt) in enumerate(plan):
        kk = K * (0.97 if row == "far" else 1.0)
        p0 = lp(lx, ly)
        A = p0                       # every frame of this walker is drawn at its spot in the boat
        pos, wframe, t_start, t_arrive, t_hop0 = walker_path(lx, ly, tgt, e_t[v])
        turn_pose = "wonder" if v in (1, 7, 2) else "stand"
        turn_expr = "awed" if v % 3 else "amazed"
        turn_f = -1                                             # back toward Jesus ...
        if v in (3, 11):                                        # ... or to a friend: John and Judas whisper
            turn_pose, turn_expr, turn_f = "whisper", "awed", 1
        fr = [doc(disc(A[0], A[1], kk, -1, v, "stand", "awed")),             # 0 start (shared with s13)
              doc(disc(A[0], A[1], kk, 1, v, "stand", "happy")),             # 1 looking ahead
              doc(disc(A[0], A[1], kk, 1, v, "stand", blink("happy"))),      # 2
              doc(disc(A[0], A[1], kk, 1, v, "stand", "awed")),              # 3 looking at the sun
              doc(disc(A[0], A[1], kk, 1, v, "walk_a", "happy")),            # 4 walk
              doc(disc(A[0], A[1], kk, 1, v, "walk_b", "happy")),            # 5
              doc(disc(A[0], A[1], kk, turn_f, v, turn_pose, turn_expr)),     # 6 turned back on the beach
              doc(disc(A[0], A[1], kk, turn_f, v, turn_pose, blink(turn_expr) if f"st_blink_{turn_expr}" in C.EXPRS
                       else turn_expr)),                                      # 7
              doc(disc(A[0], A[1], kk, -1, v, "stand", "smile"))]             # 8 smiling at Jesus at the end
        t_turn = snap(t_arrive + 0.02)
        ents = [(-1, 0), (t_look[v], 1), (t_sunlook[v], 3), (snap(t_sun + 1.9 + 0.07 * (idx % 4)), 1),
                (t_turn, 6)]
        ents = blink_entries(ents, [t_look[v] + 1.3 + 0.21 * (idx % 5), t_turn + 0.6 + 0.31 * (idx % 5)], None,
                             {1: 2, 6: 7})
        base = cuts(ents)

        def fa(t, base=base, wframe=wframe):
            w = wframe(t)
            if w is not None:
                return 4.0 + w
            return base(t)

        def mot(t, pos=pos, A=A, t_start=t_start):
            if t < t_start:
                return bm(t)
            (x, y), _ = pos(t)
            return Tf(dx=x - A[0], dy=y - A[1])
        piv_m = lambda t, pos=pos: pos(t)[0]                    # noqa: E731
        dips = [t_look[v], t_sunlook[v], t_turn]
        mots = [mot] + [squash_at(dp, kk, piv_m, 6) for dp in dips]
        mots.append(breath_at(piv_m, 2.6 + 0.15 * (idx % 4), 0.13 * idx))
        z = (3.0 if row == "far" else 5.0) + 0.01 * idx
        sc.add(f"crew{v}", fr, frame_at=fa, z=z, seed=crew_seed(v), motion=M.combine(*mots))
        if v in (7, 1):
            q_who[v] = (tgt, kk)

    # ------------------------------------------------------------ Jesus: seated, stands, walks ashore last
    js = lp(*JESUS_SIT)
    jst = lp(*JESUS_STAND)
    j_exit = snap(e_t[plan[-1][1]] + 0.5)
    j_tgt = (2790, 942)
    jpos, jframe, j_start, j_arrive, _ = walker_path(JESUS_STAND[0], JESUS_STAND[1], j_tgt, j_exit)
    t_jstand = snap(j_start - 0.55)
    jfr = [doc(jes(js[0], js[1], K, 1, "sit", "warm")),                           # 0 seated (shared with s13)
           doc(jes(js[0], js[1], K, 1, "sit", "smile")),                          # 1
           doc(jes(js[0], js[1], K, 1, "sit", blink("warm"))),                    # 2
           doc(jes(jst[0], jst[1], K, 1, "stand", "warm")),                       # 3 standing in the boat
           doc(jes(jst[0], jst[1], K, 1, "walk_a", "warm")),                      # 4
           doc(jes(jst[0], jst[1], K, 1, "walk_b", "warm")),                      # 5
           doc(jes(jst[0], jst[1], K, 1, "stand", "smile")),                      # 6 ashore, smiling
           doc(jes(jst[0], jst[1], K, 1, "stand", blink("smile")))]               # 7
    j_stop = snap(j_arrive + 0.02)
    jents = [(-1, 0), (snap(t_sun + 0.3), 1), (snap(t_spark + 0.9), 0), (t_jstand, 3), (j_stop, 6)]
    jents = blink_entries(jents, [3.1, t_l2 + 0.4, j_stop + 0.8], None, {0: 2, 6: 7})
    jbase = cuts(jents)

    def j_fa(t):
        w = jframe(t)
        if w is not None and t >= j_start:
            return 4.0 + w
        return jbase(t)

    def j_mot(t):
        if t < t_jstand:
            return bm(t)
        if t < j_start:
            return Tf()
        (x, y), _ = jpos(t)
        return Tf(dx=x - jst[0], dy=y - jst[1])
    jpiv = lambda t: (js if t < t_jstand else jpos(t)[0])      # noqa: E731
    sc.add("jesus", jfr, frame_at=j_fa, z=4.0, seed=SEED["jesus"],
           motion=M.combine(j_mot, squash_at(t_jstand, K, jpiv, 7), squash_at(j_stop, K, jpiv, 5),
                            breath_at(jpiv, 3.0, 0.0)))
    # his soft glow from s13 fades away in the morning light
    sc.add("jglow", jglow_svg(), z=3.9, wc=0, seed=SEED["jglow"], blend="screen",
           motion=M.combine(bm, lambda t: Tf(alpha=jglow_alpha(t))))

    sc.add("boat_front", boat_front_svg(), z=6, motion=bm, seed=SEED["boat_front"])
    sc.add("lantern", lantern_svg(False), z=6.1, motion=bm, seed=SEED["lantern"])
    sc.add("band", band_svg("dawn"), z=6.5, wc=0.9, wc_edge=0.0, seed=SEED["water"])
    sc.add("wline", waterline_svg(), z=6.6, wc=0, seed=SEED["wline"], motion=bm)
    spd = lambda t: (boat_x(t + 0.05, u_touch, u_a) - boat_x(t - 0.05, u_touch, u_a)) / 0.1     # noqa: E731
    sc.add("wake", [wake_svg(k) for k in range(3)], z=6.55, wc=0, frame_at=lambda t: float(int(t / 0.18) % 3),
           motion=M.combine(bm, lambda t: Tf(alpha=min(1.0, max(0.0, (spd(t) - 30) / 140)))))
    # foam at the bow when it touches the beach
    fx_, fy_ = 2650, BY + 4
    foam = doc(S.g("".join(
        f'<ellipse cx="{f1(fx_ - 30 + 22 * i)}" cy="{f1(fy_ - 6 * (i % 2))}" rx="{f1(16 + 4 * (i % 3))}" ry="9" '
        f'fill="#fff6ea" stroke="{S.shade("#9cb8cc", -0.3)}" stroke-width="2.4"/>' for i in range(5)), filter="wobble-fine"))
    sc.add("bowfoam", foam, z=6.7, wc=0,
           motion=lambda t: Tf(alpha=max(0.0, 1 - max(0.0, t - u_touch) / 0.9) if t >= u_touch - 0.02 else 0.0,
                               sx=1 + 0.5 * M.progress(t, u_touch, u_touch + 0.9), sy=1 + 0.3 * M.progress(t, u_touch,
                                                                                                          u_touch + 0.9),
                               px=fx_, py=fy_))

    # question marks on '到底是谁呢'
    for j, (v, (tgt, kk)) in enumerate(sorted(q_who.items())):
        qx, qy = tgt[0] + 6, tgt[1] - 440 * kk
        tq = snap(t_who + 0.05 + 0.35 * j)
        sc.add(f"q{v}", qmark_svg(qx, qy, 52), z=20 + j, wc=0,
               motion=lambda t, tq=tq, qx=qx, qy=qy: _pop(t, tq, (qx, qy)))

    # ------------------------------------------------------------ camera
    def cam(t):
        f = follow_cam(t, u_touch, u_a)
        land = Cam(2480, 640, 1800)
        sunc = Cam(2620, 580, 1800)
        walk = Cam(2760, 700, 1640)
        endc = Cam(2880, 704, 1520)
        k1 = M.progress(t, u_touch - 1.6, u_touch + 0.4, "inout")
        c = Cam(M.lerp(f.x, land.x, k1), M.lerp(f.y, land.y, k1), M.lerp(f.w, land.w, k1))
        k2 = M.progress(t, t_sun - 0.2, t_chu + 1.0, "inout")
        c = Cam(M.lerp(c.x, sunc.x, k2), M.lerp(c.y, sunc.y, k2), c.w)
        k3 = M.progress(t, t_spark + 0.6, t_l2 + 1.4, "inout")
        c = Cam(M.lerp(c.x, walk.x, k3), M.lerp(c.y, walk.y, k3), M.lerp(c.w, walk.w, k3))
        k4 = M.progress(t, j_stop - 0.5, T, "sine")
        c = Cam(M.lerp(c.x, endc.x, k4), M.lerp(c.y, endc.y, k4), M.lerp(c.w, endc.w, k4))
        return clamp_cam(c)
    sc.camera = cam

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-16, fade_in=0.8, fade_out=1.2)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-24, fade_in=0.8, fade_out=1.2)
    sc.sfx("cloth", t_unfurl, gain_db=-11)
    sc.sfx("whoosh", t_unfurl + 0.05, gain_db=-15)
    sc.sfx("ship_creak", t_unfurl + 0.2, dur=u_touch - t_unfurl, gain_db=-22, fade_in=0.4, fade_out=0.6)
    sc.sfx("thud", u_touch, gain_db=-12, pan=0.4)
    sc.sfx("splash_small", u_touch - 0.03, gain_db=-14, pan=0.4)
    sc.sfx("chime", t_rise0 + 0.2, gain_db=-16)
    sc.sfx("birds", t_rise1 - 0.4, dur=T - t_rise1 + 0.7, gain_db=-17, fade_in=1.0, fade_out=1.0)
    sc.sfx("sparkle", t_spark, gain_db=-14)
    sc.sfx("sparkle", t_spark + 0.6, gain_db=-17)
    first_hop = min(e_t.values())
    sc.sfx("footsteps", first_hop - 0.4, dur=j_stop - first_hop + 0.5, gain_db=-17, pan=0.3, fade_in=0.3)
    for v, tq in ((v, snap(t_who + 0.05 + 0.35 * j)) for j, v in enumerate(sorted(q_who))):
        sc.sfx("pop", tq, gain_db=-14, pan=0.4)
    sc.sfx("cloth", t_jstand, gain_db=-17, pan=-0.2)
    return sc


def jglow_alpha(u):
    """Jesus' soft glow: full at the s13 -> s14 cut, fading away in the first seconds of the morning."""
    return 0.85 * (1 - M.progress(u, 0.6, 2.6, "sine"))


def squash_at(t0, s, piv_fn, depth=8.0):
    """squash() with a pivot that may move: piv_fn(t) -> (x, y)."""
    def m(t):
        if t < t0 - 0.15 or t > t0 + 0.3:
            return Tf()
        px, py = piv_fn(t)
        v = squash(t0, s, (px, py), depth)(t)
        return v
    return m


def breath_at(piv_fn, period=2.8, phase=0.0, amount=0.011):
    def m(t):
        px, py = piv_fn(t)
        return Tf(sy=1 + amount * math.sin(2 * math.pi * (t / period + phase)), px=px, py=py)
    return m


def _pop(t, t0, piv, dur=0.35):
    if t < t0:
        return Tf(alpha=0)
    u = min(1.0, (t - t0) / dur)
    k = 0.3 + 0.7 * M.ease("back")(u)
    return Tf(sx=k, sy=k, alpha=min(1.0, (t - t0) / 0.1), dy=4 * math.sin(2 * math.pi * (t - t0) / 1.8),
              rot=6 * math.sin(2 * math.pi * (t - t0) / 2.4), px=piv[0], py=piv[1])
