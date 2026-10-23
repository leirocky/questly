"""Scene 6 — Mark 4:35-36. Evening on the lakeshore, violet-gold: the sun sinks toward the hills over the fishing
village, its path glitters on the lake, windows light up. The crowd walks home along the beach (mothers with baskets,
an old man with his stick, children), a few stay to wave goodbye. Jesus sits on the stern of the moored boat, tired
after the long day; he sighs, stands up on the stern deck, turns to his disciples and points across the lake: '我们渡到
湖的那一边去吧。' The disciples ready the boat: Andrew hauls the sail up, the rowers take the oars out, James and John
put their shoulders to the stern to push off.

Beats (syllable onsets measured in the voice clip, proportional fallback):
  0 .. 0.9      calm wide sunset page: people already walking home, wavers waving, the sun low, clouds drifting
  '天快黑了'     the sun sinks a little, windows glow; Jesus, sitting on the stern, closes his eyes and sighs (a slow
                slump of the shoulders)
  '耶稣对门徒说' he stands up on the stern deck and turns toward the disciples (camera eases in)
  Z '我们渡到'   he speaks; on '湖的那一边' he points across the lake; the disciples in the boat turn to look
  after '那一边' Andrew hauls the rope and the sail drops open from the yard (cloth, creak); the rowers take the oars
                out; James and John lean into the stern ready to push; calm hold
  The last 1.2 s are a held tableau: s07 opens with a plain cross-dissolve on exactly this picture (same stage,
  camera, boat and people; all ambient motion - water, clouds, the walkers, waving, the sun - runs on the film's
  global clock, so the dissolve has no ghosting).
The panorama set, the crew and the shore people are shared with s07_sleep.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, H
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.storm.scenes.s04_shore import Actor, blink, f1, on_boat, snap, timer

INK = P["ink"]
W7 = 3840                    # panorama stage (the boat rows out to the right in s07)
SHORE7 = 790
LS7 = 0.62
YF7 = SHORE7 - 250 * LS7
BX7, BY7, BK7 = 1420, 778, 0.6
BP7 = PR.boat_points(BX7, BY7, BK7, 1)
SUN = (700, 432)             # the low sun (it sinks on the global clock)
SUN_RATE = 6.2               # px / s
G_SUN = 75.0                 # global time at which the sun is at SUN
BEACH_END = 1760             # the beach curves away into open water right of here
DECK = (BX7 - 480 * BK7, BY7 - 172 * BK7)      # Jesus standing on the stern deck
STERN_SEAT7 = BP7["stern_seat"]
SLEEP7 = BP7["sleep"]
LANTERN7 = (BX7 - 760 * BK7, BY7 - 352 * BK7)
NIGHT_FILTER = ('<filter id="night7" x="-5%" y="-5%" width="110%" height="110%"><feColorMatrix type="matrix" '
                'values="0.42 0.08 0.06 0 0.02  0.05 0.46 0.1 0 0.035  0.08 0.12 0.66 0 0.09  0 0 0 1 0"/></filter>')


def doc7(body, defs="", night=False):
    if night == "dim":            # a little darker still (the big pale sail must not outshine the people)
        body = f'<g filter="url(#night7d)">{body}</g>'
        defs += NIGHT_FILTER.replace('id="night7"', 'id="night7d"').replace(
            "0.42 0.08 0.06 0 0.02  0.05 0.46 0.1 0 0.035  0.08 0.12 0.66 0 0.09",
            "0.34 0.07 0.05 0 0.02  0.04 0.37 0.08 0 0.03  0.07 0.1 0.55 0 0.08")
    elif night:
        body = f'<g filter="url(#night7)">{body}</g>'
        defs += NIGHT_FILTER
    return S.svg_doc(body, defs, W7, H)


def lake_cols(time):
    return PR._LT[time]


# ------------------------------------------------------------------ backdrop


def sky_svg():
    c0, c1, c2 = lake_cols("sunset")["sky"]
    defs = (S.lin_grad("e6sky", [(0, c0), (0.5, c1), (0.86, c2), (1, "#fbd894")]) +
            S.rad_grad("e6glow", [(0, "#fff0c0", 0.95), (0.25, "#ffd28a", 0.55), (0.6, "#f6a878", 0.18),
                                  (1, "#f6a878", 0)]))
    b = (f'<rect x="-20" y="-20" width="{W7 + 40}" height="{YF7 + 40}" fill="url(#e6sky)"/>'
         f'<circle cx="{SUN[0]}" cy="{SUN[1] + 30}" r="760" fill="url(#e6glow)"/>')
    return doc7(b, defs)


def sun_svg():
    x, y = SUN
    return doc7(f'<circle cx="{x}" cy="{y}" r="62" fill="#ffd27a" stroke="#f3a85a" stroke-width="5"/>'
                f'<circle cx="{x - 14}" cy="{y - 14}" r="24" fill="#fff0c4" opacity="0.7"/>')


def clouds_svg():
    rim, body, under = "#ffe2ac", "#e9b6c2", "#c995b6"
    b = ""
    for i, (x, y, w) in enumerate(((260, 190, 330), (1150, 110, 260), (1950, 240, 300), (2700, 150, 280),
                                   (3400, 250, 320), (500, 340, 170))):
        b += S.cloud(x, y, w, w * 0.28, body, seed=61 + i, sw=2.8, shade_fill=under)
        b += f'<path d="M{x - w * 0.42:.0f},{y + w * 0.12:.0f} Q{x:.0f},{y + w * 0.2:.0f} {x + w * 0.42:.0f},{y + w * 0.1:.0f}" ' \
             f'fill="none" stroke="{rim}" stroke-width="7" stroke-linecap="round" opacity="0.85"/>'
    return doc7(S.g(b, filter="wobble"))


def back_svg(time="sunset"):
    """Hills, the far village, the lake and (sunset) the sun's glittering path - no sky."""
    sx = (SUN[0] + 40) / (W7 + 80)
    return doc7(PR.lake_galilee(-40, W7 + 40, SHORE7, LS7, time=time, part="back", sky=False, boats=False, seed=7,
                                sun_x=sx))


def glints_svg(seed, time="sunset"):
    lite = lake_cols(time)["lite"]
    rng = random.Random(seed)
    b = ""
    for _ in range(150):
        u = rng.random()
        y = YF7 + 14 + (SHORE7 - YF7 - 24) * u ** 1.2
        x = rng.uniform(-200, W7 + 200)
        L = (18 + 70 * u) * rng.uniform(0.7, 1.2)
        b += (f'<path d="M{f1(x)},{f1(y)} q{f1(L / 2)},{f1(-2 - 2 * u)} {f1(L)},0" fill="none" stroke="{lite}" '
              f'stroke-width="{f1(2 + 2.5 * u)}" stroke-linecap="round" opacity="{0.4 + 0.4 * u:.2f}"/>')
    for _ in range(60):                       # the open water in front, right of the beach
        y = rng.uniform(SHORE7 + 20, H + 20)
        x = rng.uniform(curve_x(y) + 40, W7 + 100)
        L = rng.uniform(60, 150)
        b += (f'<path d="M{f1(x)},{f1(y)} q{f1(L / 2)},-4 {f1(L)},0" fill="none" stroke="{lite}" stroke-width="4" '
              f'stroke-linecap="round" opacity="0.6"/>')
    return doc7(b)


def curve_x(y):
    """x of the shoreline where the beach curves away (right edge of the sand) at height y."""
    u = max(0.0, min(1.0, (y - SHORE7) / (H + 80 - SHORE7)))
    return BEACH_END + 440 * u ** 0.55


def band_svg(time="sunset"):
    return doc7(PR.lake_band(-40, W7 + 40, BY7 - 4, SHORE7 + 10, time, scale=LS7, seed=9))


def shore_svg(time="sunset"):
    """The beach with the village (left), reeds and pebbles; right of BEACH_END the open water curves in front."""
    t = lake_cols(time)
    b = PR.lake_galilee(-40, BEACH_END + 520, SHORE7, LS7, time=time, part="shore", village="left", nets=False,
                        boats=False, bottom=H + 60, seed=7)
    b += PR.fishing_net(150, 846, 0.55, kind="pole", time=time) + PR.fishing_net(250, 872, 0.5, kind="pile", time=time)
    l0, l1, l2 = t["lake"]
    pts = [(curve_x(y), y) for y in range(SHORE7 - 6, H + 90, 40)]
    d = f"M{BEACH_END - 30},{SHORE7 - 6} " + " ".join(f"L{f1(x)},{f1(y)}" for x, y in pts)
    d += f" L{W7 + 60},{H + 90} L{W7 + 60},{SHORE7 - 6} Z"
    gid = f"e6near{time}"
    defs = S.lin_grad(gid, [(0, S.mix(l1, l2, 0.45)), (1, S.shade(l2, -0.12))])
    b += f'<path d="{d}" fill="url(#{gid})"/>'
    edge = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts)
    b += f'<path d="{edge}" fill="none" stroke="{S.mix(PR.STORM_FOAM, t["tint"], 0.3)}" stroke-width="7" ' \
         f'stroke-dasharray="44 22" opacity="0.85"/>'
    b += f'<path d="{edge}" fill="none" stroke="{S.mix(INK, t["tint"], 0.3)}" stroke-width="3"/>'
    wet = "M" + " L".join(f"{f1(x - 26 - 30 * (y - SHORE7) / 400)},{f1(y)}" for x, y in pts)
    b += f'<path d="{wet}" fill="none" stroke="{S.shade(t["sand"], -0.18)}" stroke-width="30" opacity="0.35"/>'
    rng = random.Random(3)
    for k, (yy, r) in enumerate(((SHORE7 + 30, 26), (SHORE7 + 120, 34), (SHORE7 + 70, 18), (SHORE7 + 230, 30))):
        xx = curve_x(yy) - 10 + rng.uniform(-10, 10)
        c = PR._tint(PR.BASALT_LIGHT if k % 2 else "#a39484", time)
        b += S.path(S.blob(xx, yy, r * 1.4, r * 0.75, 0.15, 8, seed=80 + k), fill=c, sw=3)
    for yy, sc_ in ((SHORE7 + 50, 0.34), (SHORE7 + 170, 0.4), (SHORE7 + 330, 0.5)):
        b += PR.reeds(curve_x(yy) - 60, yy, sc_, 0, 0.1)
    # the beach running out to the point: footprints to the water, tufts, stones, a coil of rope, driftwood
    for k in range(9):
        fx_, fy_ = 1280 + 52 * k, 905 + 22 * k + (8 if k % 2 else -8)
        b += f'<ellipse cx="{fx_}" cy="{fy_}" rx="11" ry="5" fill="{S.shade(t["sand"], -0.16)}" opacity="0.7"/>'
    for x_, y_, s_, v_ in ((1500, 1010, 0.8, 1), (1700, 930, 0.7, 0), (1380, 1120, 0.9, 2), (1880, 1060, 0.75, 1)):
        b += PR.grass_tuft(x_, y_, s_, v_)
    b += PR.rope_spiral(1620, 1000, 0.6)
    drift = "M1440,1070 q60,-18 150,-6 q30,4 46,-8"
    b += (f'<path d="{drift}" fill="none" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
          f'<path d="{drift}" fill="none" stroke="{PR._tint(P["wood_light"], time)}" stroke-width="11" '
          f'stroke-linecap="round"/>')
    return doc7(S.g(b, filter="wobble"), defs)


def small_boat_svg(x, y, k, f, variant, time="sunset", lantern=True, night=False):
    """A small boat on the water with a little strip of lake hiding its keel."""
    t = lake_cols(time)
    l1, l2 = t["lake"][1], t["lake"][2]
    w = 300 * k
    patch = (f'<path d="M{f1(x - w)},{f1(y + 1)} q{f1(w / 4)},-5 {f1(w / 2)},0 t{f1(w / 2)},0 t{f1(w / 2)},0 '
             f't{f1(w / 2)},0 L{f1(x + w)},{f1(y + 40 * k)} L{f1(x - w)},{f1(y + 40 * k)} Z" '
             f'fill="{S.mix(l1, l2, 0.55)}"/>'
             f'<path d="M{f1(x - w * 0.8)},{f1(y + 2)} q{f1(w * 0.4)},-4 {f1(w * 0.8)},0 t{f1(w * 0.8)},0" fill="none" '
             f'stroke="{t["lite"]}" stroke-width="{f1(4 * k + 1)}" opacity="0.8"/>')
    b = PR.small_boat(x, y, k, f, variant=variant, sail="full" if variant == 1 else "none", lantern=lantern,
                      time=time) + patch
    return doc7(S.g(b), night=night)


def tufts_svg(k, time="sunset"):
    sw = (-0.5, 0.0, 0.5)[k]
    b = ""
    for x, y, s, v in ((50, 1180, 1.2, 0), (170, 1196, 0.95, 1), (980, 1200, 0.8, 2), (1900, 1196, 1.0, 0),
                       (2010, 1186, 1.15, 1)):
        b += PR.grass_tuft(x, y, s, v, sway=sw)
    for x, y, s in ((110, 1160, 0.75), (2120, 1150, 0.7)):
        b += PR.reeds(x, y, s, 1, sway=sw * 0.8)
    return doc7(b)


# ------------------------------------------------------------------ the boat


def boat_back_markup(oars="in", sail="furled"):
    return PR.fishing_boat(BX7, BY7, BK7, 1, part="back", sail=sail, oars=oars)


def sail_clip_markup():
    """Only the full sail (clipped from the boat's back part): it drops open from the yard over the furled one."""
    yard_y = BY7 + PR.BOAT_YARD_Y * BK7
    x0, x1 = BX7 + (-150) * BK7, BX7 + 610 * BK7
    clip = (f'<clipPath id="e6sail"><rect x="{f1(x0)}" y="{f1(yard_y - 30)}" width="{f1(x1 - x0)}" '
            f'height="{f1(420 * BK7)}"/></clipPath>')
    return f'<defs>{clip}</defs><g clip-path="url(#e6sail)">{boat_back_markup("in", "full")}</g>'


def boat_front_markup(oars="in", row=0.0):
    return PR.fishing_boat(BX7, BY7, BK7, 1, part="front", sail="none", oars=oars, row=row)


def rope_markup():
    """Andrew's halyard: from his top fist (pull_rope) on up to the yard, continuing the rope he holds."""
    ax, ay = ANDREW[1]
    fx, fy = ax + 70 * BK7, ay - 299 * BK7
    dx, dy = 27, -59
    k = (fy - (BY7 + PR.BOAT_YARD_Y * BK7 + 6)) / -dy
    x1, y1 = fx + dx * k, fy + dy * k
    return (f'<path d="M{f1(fx)},{f1(fy)} L{f1(x1)},{f1(y1)}" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>'
            f'<path d="M{f1(fx)},{f1(fy)} L{f1(x1)},{f1(y1)}" stroke="#c9b48a" stroke-width="2.2" stroke-linecap="round"/>')


def lantern_motion(bm, g0, tilt=None, lit_t=None):
    """The stern lantern: its hook rides with the boat, the lantern itself hangs plumb and sways a little (global
    clock); lit_t fades a lit copy in."""
    hook = LANTERN7

    def m(t):
        b = bm(t)
        r = math.radians(b.rot)
        hx, hy = hook[0] - BX7, hook[1] - BY7
        nx = BX7 + hx * math.cos(r) - hy * math.sin(r) + b.dx
        ny = BY7 + hx * math.sin(r) + hy * math.cos(r) + b.dy
        sw = 2.0 * math.sin(2 * math.pi * (t + g0) / 2.3)
        if tilt is not None:
            sw -= 0.7 * tilt(t - 0.35)
        a = 1.0 if lit_t is None else M.progress(t, lit_t, lit_t + 0.5, "sine")
        return Tf(dx=nx - hook[0], dy=ny - hook[1], rot=sw, alpha=a, px=hook[0], py=hook[1])
    return m


def lantern_svg(lit, swing=0.0, night=False):
    return doc7(PR.hanging_lantern(LANTERN7[0], LANTERN7[1], 0.8 * BK7, swing=swing, lit=lit), night=night)


# disciples in the boat: (name, variant, spot key, index, facing)
FAR_ROW = [("Matthew", 6, 2), ("Thomas", 7, 3), ("Philip", 4, 4), ("Bartholomew", 5, 5)]   # far_stand 0/1: John, James
ROWERS = [("JamesA", 8, 0), ("Thaddaeus", 9, 1)]
ANDREW = (1, BP7["stand"][3])
SIMON = (10, BP7["stand"][4])
PETER = (0, BP7["stand"][5])
JUDAS = (11, BP7["stand"][1])
JAMES_BEACH = (2, (1150, 848))
JOHN_BEACH = (3, (1262, 880))
CREW_SEED = {"simon": 57, "peter": 58, "judas": 56}
MOORED = [(3, 700, 752, 0.42, 1), (0, 905, 746, 0.38, 1)]     # small boats moored by the village (variant, x, y, k, f)


def disc(px, py, v, pose, facing, expr=None, phase=0.0, wind=0.0):
    return C.disciples(px, py, BK7, facing, variant=v, pose=pose, expr=expr, phase=phase, wind=wind)


def far_row_markup(facings=None, exprs=None):
    b = ""
    for j, (_, v, i) in enumerate(FAR_ROW):
        px, py = BP7["far_stand"][i]
        f = (facings or [-1] * 4)[j]
        e = (exprs or [None] * 4)[j]
        b += disc(px, py, v, "stand", f, e)
    return b


def rower_markup(j, pose="sit", phase=0.0):
    _, v, i = ROWERS[j]
    px, py = BP7["seats"][i]
    return disc(px, py, v, pose, -1, "happy", phase)


# ------------------------------------------------------------------ shore people (global clock)


def g_steps(g, g_start, period, step, s, move=0.15, lift=6.0):
    """Planted-foot stepping on the global clock: (offset along the walk, stride drawing 0/1, lift dy)."""
    if g < g_start - 0.45 * move:
        return 0.0, 0, 0.0
    j = int(math.floor((g - g_start + 0.45 * move) / period))
    tc = g_start + j * period
    u = M.progress(g, tc - 0.45 * move, tc + 0.55 * move, "sine")
    dy = 0.0
    if tc - 0.45 * move <= g <= tc + 0.55 * move:
        dy = -lift * s * math.sin(math.pi * (g - tc + 0.45 * move) / move)
    fr = j % 2 if g >= tc else (j - 1) % 2
    return step * (j + u), fr, dy


# walkers going home (left): kind, variant, x at G_WALK, y, scale, period, carry
G_WALK = 74.0
WALKERS = [("woman", 2, 1180, 952, 0.62, 0.34, True), ("child", 1, 1290, 990, 0.64, 0.22, False),
           ("man", 3, 1420, 944, 0.62, 0.33, False), ("elder", 0, 1010, 960, 0.62, 0.40, False),
           ("woman", 4, 1580, 1002, 0.64, 0.35, False), ("man", 5, 1720, 960, 0.62, 0.32, True),
           ("child", 3, 1830, 1010, 0.64, 0.21, False), ("woman", 0, 820, 980, 0.63, 0.34, True),
           ("man", 1, 640, 944, 0.62, 0.33, False)]
STRIDE7 = {"man": 84, "woman": 81, "child": 50, "elder": 83}
# wavers by the water (facing the boat), leave at G_LEAVE
WAVERS = [("woman", 5, 330, 872, 0.6, 0.0), ("child", 4, 410, 900, 0.62, 0.3), ("man", 2, 498, 868, 0.6, 0.55),
          ("elder", 3, 575, 884, 0.6, 0.15)]
G_LEAVE = 91.6


def add_shore_people(sc, g0, T, time="sunset"):
    """The crowd going home and the wavers; everything on the global clock (g = g0 + t)."""
    for i, (kind, v, x0, y, s, per, carry) in enumerate(WALKERS):
        stride = STRIDE7[kind] * s * (0.9 if kind == "elder" else 1.0)
        names = ("carry_walk_a", "carry_walk_b") if carry else ("walk_a", "walk_b")
        fr = [doc7(C.ground_shadow(x0, y, s, 110, 0.14) + C.villager(x0, y, s, -1, kind=kind, variant=v, pose=n))
              for n in names]
        gs = G_WALK + 0.07 * i

        def fa(t, gs=gs, per=per, stride=stride, s=s):
            return float(g_steps(g0 + t, gs, per, stride, s)[1])

        def m(t, gs=gs, per=per, stride=stride, s=s):
            off, _, dy = g_steps(g0 + t, gs, per, stride, s)
            return Tf(dx=-off, dy=dy)
        sc.add(f"walker{i}", fr, z=20 + y / 100 + 0.001 * i, frame_at=fa, motion=m, seed=300 + i)
    for i, (kind, v, x, y, s, ph) in enumerate(WAVERS):
        stride = STRIDE7[kind] * s
        fr = [doc7(C.ground_shadow(x, y, s, 110, 0.14) + C.villager(x, y, s, 1, kind=kind, variant=v, pose="wave",
                                                                    phase=p_)) for p_ in (0.0, 0.33, 0.66, 1.0)]
        fr += [doc7(C.villager(x, y, s, -1, kind=kind, variant=v, pose=n)) for n in ("walk_a", "walk_b")]
        gl = G_LEAVE + 0.4 * i
        per = 0.34 if kind != "child" else 0.22

        def fa(t, ph=ph, gl=gl, per=per, stride=stride, s=s):
            g = g0 + t
            if g >= gl:
                return 4.0 + g_steps(g, gl, per, stride, s)[1]
            return float((0, 1, 2, 3, 2, 1)[int(g / 0.13 + ph * 6) % 6])

        def m(t, gl=gl, per=per, stride=stride, s=s, x=x, y=y, i=i):
            g = g0 + t
            br = 1 + 0.01 * math.sin(2 * math.pi * (g / 2.7 + 0.2 * i))
            if g >= gl:
                off, _, dy = g_steps(g, gl, per, stride, s)
                return Tf(dx=-off, dy=dy)
            return Tf(sy=br, px=x, py=y)
        sc.add(f"waver{i}", fr, z=20 + y / 100 + 0.0015 * i, frame_at=fa, motion=m, seed=320 + i)


def breathe_g(g0, amount, period, pivot, phase=0.0):
    return lambda t: Tf(sx=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=pivot[0], py=pivot[1])


def boat_bob(g0, extra=None):
    """The boat bobbing on the global clock (+ optional extra(t) -> (dx, tilt, dy))."""
    def m(t):
        g = t + g0
        dy = 2.0 * math.sin(2 * math.pi * g / 4.2)
        r = 0.4 * math.sin(2 * math.pi * (g / 4.2 + 0.3))
        dx = 0.0
        if extra is not None:
            ex, er, ey = extra(t)
            dx, r, dy = dx + ex, r + er, dy + ey
        return Tf(dx=dx, dy=dy, rot=r, px=BX7, py=BY7)
    return m


def add_backdrop(sc, g0, night=None):
    """Sky, sun, clouds, hills and lake, glints, the band, the beach + open water (sunset). night: t -> 0..1 fades
    the night versions in on top (s07)."""
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("sun", sun_svg(), z=0.5, wc=0.3, motion=lambda t: Tf(dy=SUN_RATE * (t + g0 - G_SUN)))
    sc.add("clouds", clouds_svg(), z=1, motion=lambda t: Tf(dx=4.0 * (t + g0 - 80.0)))
    sc.add("back", back_svg("sunset"), z=2)
    for i, (vx, per) in enumerate(((6.0, 2.7), (-4.5, 3.4))):
        sc.add(f"glints{i}", glints_svg(21 + i), z=3, wc=0, motion=lambda t, vx=vx, per=per, i=i: Tf(
            dx=vx * ((t + g0) - 80.0), alpha=0.5 + 0.45 * math.sin(2 * math.pi * ((t + g0) / per + 0.5 * i))))
    sc.add("band", band_svg("sunset"), z=14)
    sc.add("shore", shore_svg("sunset"), z=15)


def add_boat_static(sc, bm, oars_t=None, sail_t=None, g0=0.0):
    """Boat back (oars in -> out at oars_t), the full sail dropping open (reveal) at sail_t=(t0, t1), boat front
    added by the caller (it depends on the rowing)."""
    fr = [doc7(boat_back_markup("in", "furled")), doc7(boat_back_markup("out", "furled"))]
    fa = (lambda t: 1.0 if t >= oars_t else 0.0) if oars_t is not None else (lambda t: 1.0)
    sc.add("boat_back", fr, z=10, frame_at=fa, motion=bm, seed=41)
    s0, s1 = sail_t if sail_t else (-2.0, -1.0)
    sc.add("sail", doc7(sail_clip_markup()), z=10.2, motion=bm, seed=43,
           reveal=lambda t: {"mode": "down", "frac": max(0.0, min(1.0, M.progress(t, s0, s1, "out"))), "soft": 50})


# ------------------------------------------------------------------ build


def build(ctx):
    sc = Scene(ctx, W=W7, H=H)
    T = ctx.duration
    g0 = ctx.start
    at = timer(ctx)
    rng = random.Random(6)
    t_dark = at(0, "天快黑了")
    t_said = at(0, "耶稣对门徒说")
    t_we = at(1, "我们")
    t_lake = at(1, "湖的")
    t_side = at(1, "那一边")
    t_hold = T - 1.25                      # from here on nothing changes (the dissolve into s07)

    add_backdrop(sc, g0)
    bm = boat_bob(g0)
    t_oars = snap(min(t_hold - 0.25, at(1, "去吧") + 0.05))
    t_sail0, t_sail1 = t_side + 0.25, min(t_hold - 0.1, t_side + 1.25)
    add_boat_static(sc, bm, oars_t=t_oars, sail_t=(t_sail0, t_sail1), g0=g0)
    sc.add("lantern", lantern_svg(False), z=13.5, motion=lantern_motion(bm, g0), seed=45)

    # far row: they turn to look where Jesus points
    t_look = [snap(t_lake + 0.25 + 0.12 * j) for j in range(4)]
    far = Actor("crew_far", lambda n: far_row_markup([1 if c == "1" else -1 for c in n.split("|")[0]],
                                                     ["happy"] * 4 if n.split("|")[1] == "h" else None),
                (BX7, BY7), BK7, 11, seed=47, docf=doc7, carrier=bm)
    far.cut(0, "0000|k")
    for j in range(4):
        far.cut(t_look[j], "".join("1" if k <= j else "0" for k in range(4)) + "|h", dip_=False)
    far.build(sc)

    # Jesus: sitting tired on the stern, sighs, stands on the deck, turns, points across the lake
    def jd(n):
        pose, expr, f = n.split("|")
        x, y = (STERN_SEAT7 if pose == "sit" else DECK)
        return C.jesus(x, y, BK7, int(f), pose=pose, expr=expr)
    ja = Actor("jesus", jd, DECK, BK7, 12, seed=49, docf=doc7, carrier=bm)
    ja.cut(0, "sit|warm|-1")
    t_sigh = snap(t_dark + 0.15)
    ja.cut(t_sigh, "sit|peaceful|-1", dip_=False)
    ja.cut(snap(t_sigh + 1.0), "sit|warm|-1", dip_=False)
    t_up = snap(t_said - 0.12)
    ja.cut(t_up, "stand|warm|1", depth=6)
    ja.cut(snap(t_we - 0.1), "stand|warm|1", dip_=False)
    t_point = snap(t_lake - 0.12)
    ja.cut(t_point, "point|warm|1", depth=6)
    ja.cut(snap(min(t_hold - 0.2, t_side + 0.95)), "stand|warm|1", depth=5)
    ja.add_blinks({"stand|warm|1": f"stand|{blink('warm')}|1", "sit|warm|-1": f"sit|{blink('warm')}|-1"},
                  t_hold - 0.2, rng, t_from=0.4)
    sigh = lambda t: Tf(sy=1 - 0.035 * math.sin(math.pi * min(1.0, max(0.0, (t - t_sigh) / 1.0))),
                        px=STERN_SEAT7[0], py=STERN_SEAT7[1])
    rise = lambda t: Tf(dy=(STERN_SEAT7[1] - DECK[1]) * 0.55 * (1 - M.progress(t, t_up, t_up + 0.28, "out"))
                        if t >= t_up else 0.0)
    ja.mots += [sigh, rise, breathe_g(g0, 0.009, 3.2, DECK)]
    ja.build(sc)

    # the rowers: sitting, then oars out (phase 0, the catch) - s07 rows on
    for j in range(2):
        px, py = BP7["seats"][ROWERS[j][2]]
        a = Actor(f"rower{j}", lambda n, j=j: rower_markup(j, *(("sit", 0.0) if n == "sit" else ("row", 0.0))),
                  (px, py), BK7, 12.5 + 0.01 * j, seed=51 + j, docf=doc7, carrier=bm)
        a.cut(0, "sit")
        a.cut(t_oars, "row", depth=5)
        a.mots += [breathe_g(g0, 0.01, 2.9 + 0.3 * j, (px, py), 0.3 * j)]
        a.build(sc)

    # Andrew hauls the sail up; Simon and Peter
    av, (ax, ay) = ANDREW
    an = Actor("andrew", lambda n: disc(ax, ay, av, n.split("|")[0], 1, n.split("|")[1]), (ax, ay), BK7, 12.7,
               seed=55, docf=doc7, carrier=bm)
    an.cut(0, "stand|happy")
    an.cut(snap(t_sail0 - 0.15), "pull_rope|determined", depth=6)
    an.add_blinks({"stand|happy": f"stand|{blink('happy')}"}, t_hold - 0.2, rng)
    haul = lambda t: Tf(rot=-3.0 * math.sin(math.pi * min(1.0, max(0.0, (t - t_sail0) / 0.5))) -
                        2.0 * math.sin(math.pi * min(1.0, max(0.0, (t - t_sail0 - 0.5) / 0.5))), px=ax, py=ay)
    an.mots += [haul]
    an.build(sc)
    sc.add("halyard", doc7(rope_markup()), z=12.69, wc=0.3, motion=on_boat(M.combine(haul, lambda t: Tf(
        alpha=1.0 if t >= snap(t_sail0 - 0.15) else 0.0)), bm))
    for nm, (v, (px, py)), f, ex in (("simon", SIMON, -1, "kind"), ("peter", PETER, 1, "happy"),
                                     ("judas", JUDAS, -1, "happy")):
        a = Actor(nm, lambda n, px=px, py=py, v=v, f=f: disc(px, py, v, "stand", f, n), (px, py), BK7, 12.7,
                  seed=CREW_SEED[nm], docf=doc7, carrier=bm)
        a.cut(0, ex)
        a.add_blinks({ex: blink(ex)}, t_hold - 0.2, rng)
        a.mots += [breathe_g(g0, 0.01, 3.1, (px, py), 0.4)]
        a.build(sc)
    fr = [doc7(boat_front_markup("in")), doc7(boat_front_markup("out", 0.0))]
    sc.add("boat_front", fr, z=13, frame_at=lambda t: 1.0 if t >= t_oars else 0.0, motion=bm, seed=59)

    # James and John on the beach at the stern: watching, then leaning in to push
    t_push = [snap(t_side + 0.55), snap(t_side + 0.7)]
    for k, (v, (px, py)) in enumerate((JAMES_BEACH, JOHN_BEACH)):
        a = Actor(("james", "john")[k], lambda n, px=px, py=py, v=v: C.ground_shadow(px, py, BK7, 120, 0.15) + disc(
            px, py, v, n.split("|")[0], 1, n.split("|")[1]), (px, py), BK7, 20 + py / 100, seed=61 + k, docf=doc7)
        a.cut(0, "stand|happy")
        a.cut(min(t_push[k], t_hold - 0.3), "push|determined", depth=6)
        a.add_blinks({"stand|happy": f"stand|{blink('happy')}"}, t_hold - 0.2, rng)
        a.mots.append(breathe_g(g0, 0.01, 2.8 + 0.4 * k, (px, py), 0.2 * k))
        a.build(sc)

    add_shore_people(sc, g0, T)
    for i, (v, x, y, k, f) in enumerate(MOORED):
        sc.add(f"smallboat{i}", small_boat_svg(x, y, k, f, v, lantern=False), z=9 + 0.01 * i, seed=70 + i,
               motion=lambda t, i=i: Tf(dy=1.5 * math.sin(2 * math.pi * ((t + g0) / 3.3 + 0.4 * i))))
    sc.add("tufts", [tufts_svg(k) for k in range(3)], z=40,
           frame_at=lambda t: float((0, 1, 2, 1)[int((t + g0) / 0.6) % 4]))

    # ------------------------------------------------------------ camera (static for the last 1.25 s)
    end = Cam(1430, 588, 1780)
    sc.camera = M.cam_keys([
        (0.0, Cam(1050, 600, 2080)), (t_dark, Cam(1060, 600, 2060)), (t_said - 0.1, Cam(1140, 600, 1900)),
        (t_we + 0.2, Cam(1240, 600, 1640)), (t_lake, Cam(1260, 600, 1620)), (t_hold - 0.05, end), (T, end)],
        ["sine", "inout", "sine", "inout", "inout", "linear"])

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-15, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", 0, dur=T + 0.3, gain_db=-25, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", 0, dur=T + 0.3, gain_db=-25, fade_in=0.8, fade_out=1.0, pan=-0.5)
    sc.sfx("birds", 0, dur=T * 0.7, gain_db=-25, fade_in=0.8, fade_out=2.0)
    sc.sfx("cloth", t_up, gain_db=-19, pan=-0.1)
    sc.sfx("ship_creak", t_sail0, dur=1.6, gain_db=-20, fade_in=0.1, fade_out=0.6, pan=0.2)
    sc.sfx("cloth", t_sail0 + 0.3, gain_db=-15, pan=0.3)
    sc.sfx("thud", t_oars, gain_db=-20, pan=0.1)
    return sc
