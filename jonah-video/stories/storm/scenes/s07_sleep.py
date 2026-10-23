"""Scene 7 — Mark 4:36-38. Out onto the evening lake. It opens on the very picture s06 ends with (a plain
cross-dissolve: same panorama stage, camera, boat and people, and all ambient motion on the film's global clock). James
and John give the boat a last shove and jump in, the rowers pull, and the boat glides out along the shore (the camera
travels with it, the beach curving away into open water). Jesus, tired after the whole day, yawns, sits down on the
stern and lies down with his head on the cushion; soft z's float up. Little boats with lanterns set off behind them.
The boat rocks gently on each '摇', violet dusk deepens into a blue night, and the stars come out one by one.

Beats (syllable onsets measured in the voice clip, proportional fallback):
  0 .. 1.0      exactly s06's last picture (the dissolve)
  '门徒们'       James and John lean into the push and the boat slides off (splash); they jump in at the stern
  '划'           the rowers pull: oars dip and sweep (8-phase strokes, the boat surging a little on each), the camera
                follows the boat out
  '累了'         Jesus yawns and stretches on the stern deck; '一整天' he sits down on the stern; '船尾' he lies down
                with his head on the cushion; '睡着了' soft z's float up; the disciples smile at him
  '还有别的小船'  the camera looks back: two little boats with lanterns are rowing after them, a small sailing boat
                beyond; the boat lantern is lit
  '摇啊摇' x4    the boat rocks to one side and back on each '摇' (creak); dusk fades into night
  '星星一颗一颗'  stars appear a few at a time on each syllable, the moon glows, a few twinkle
  end           a calm moonlit frame, the boat gliding slowly (dip to black into s08)
"""
import math
import random

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, voice_marks
from stories.storm.scenes import s06_evening as E
from stories.storm.scenes.s04_shore import Actor, blink, f1, on_boat, snap, timer

INK = P["ink"]
W7, BX7, BY7, BK7, BP7 = E.W7, E.BX7, E.BY7, E.BK7, E.BP7
doc7 = E.doc7
V1, V2 = 80.0, 44.0          # boat speed rowing / at night (px/s)
MOON = (3060, 236)
NIGHT_P = (0.0, 0.03, 0.06, 0.1, 0.17, 0.25, 0.33, 0.42, 0.51, 0.6, 0.7, 0.8, 0.9, 1.0)


def nth_phrase_char(ctx, li, pi, k, fallback):
    """Onset of character k of the pi-th measured phrase of line li."""
    try:
        m = voice_marks(ctx, li)[pi]
        return char_times(m)[k]
    except Exception:
        return fallback


def night_sky_svg(p):
    return doc7(PR.night_sky(-20, -20, W7 + 20, E.YF7 + 40, moon=MOON, moon_r=54, stars=86, progress=p,
                             twinkle=0.3, seed=5))


def moon_path_svg(y0, y1, seed):
    """The moon's broken silver column on the water under MOON (short horizontal strokes widening downward)."""
    rng = random.Random(seed)
    b = ""
    n = int((y1 - y0) / 13)
    for i in range(n):
        u = i / max(1, n - 1)
        y = y0 + (y1 - y0) * u
        w = (30 + 150 * u) * rng.uniform(0.5, 1.1)
        x = MOON[0] + rng.uniform(-24, 24) * (0.4 + u)
        b += (f'<path d="M{f1(x - w / 2)},{f1(y)} L{f1(x + w / 2)},{f1(y)}" stroke="#eef0dc" stroke-width="'
              f'{f1(3 + 3 * u)}" stroke-linecap="round" opacity="{0.85 - 0.35 * u:.2f}"/>')
    return doc7(b)


def build(ctx):
    sc = Scene(ctx, W=W7, H=H)
    T = ctx.duration
    g0 = ctx.start
    at = timer(ctx)
    rng = random.Random(7)
    t_men = at(0, "门徒们")
    t_row = snap(at(0, "划开"))
    t_tired = at(0, "累了")
    t_day = at(0, "一整天")
    t_wei = at(0, "船尾", 1)
    t_sleep = at(0, "睡着")
    t_others = at(1, "还有")
    t_set = at(1, "出发")
    L2 = ctx.lines[2]
    rocks = [nth_phrase_char(ctx, 2, 0, 8, L2.start + 1.7), nth_phrase_char(ctx, 2, 0, 10, L2.start + 2.1),
             nth_phrase_char(ctx, 2, 1, 0, L2.start + 2.7), nth_phrase_char(ctx, 2, 1, 2, L2.start + 3.3)]
    try:
        star_ts = char_times([m for m in voice_marks(ctx, 2) if "星星" in m[0]][0])
    except Exception:
        star_ts = [L2.chunks[-1].start + 0.24 * k for k in range(11)]

    # ------------------------------------------------------------ the boat's path (push, then rowing strokes)
    t_push0 = snap(max(1.02, t_men + 0.08))
    t_push1 = t_push0 + 0.9
    t_slow0, t_slow1 = rocks[0] - 2.2, rocks[3] + 0.4
    dt = 1 / 120
    ts = np.arange(0, T + 1.0, dt)
    v = np.where(ts < t_row, 0.0, V1 * np.clip((ts - t_row) / 1.2, 0, 1))
    v = np.where(ts > t_slow0, V1 + (V2 - V1) * np.clip((ts - t_slow0) / (t_slow1 - t_slow0), 0, 1), v)
    rate = np.where(ts < t_slow0, 1 / 0.96,
                    1 / 0.96 + (1 / 1.35 - 1 / 0.96) * np.clip((ts - t_slow0) / (t_slow1 - t_slow0), 0, 1))
    rate = np.where(ts < t_row, 0.0, rate)
    strokes = np.cumsum(rate) * dt
    v_eff = v * (1 + 0.22 * np.sin(2 * math.pi * (strokes - 0.1)))
    glide = np.cumsum(v_eff) * dt

    def bx(t):
        i = min(len(ts) - 1, max(0, int(t / dt)))
        return 45.0 * M.progress(t, t_push0, t_push1, "inout") + float(glide[i])

    def row_k(t):
        if t < t_row:
            return 0.0
        i = min(len(ts) - 1, max(0, int(t / dt)))
        return float(int(8 * strokes[i]) % 8)

    tilt = M.keys([(rocks[0] - 0.3, {"rot": 0}), (rocks[0] + 0.12, {"rot": 3.0}), (rocks[1] + 0.12, {"rot": -2.8}),
                   (rocks[2] + 0.14, {"rot": 2.8}), (rocks[3] + 0.14, {"rot": -2.6}), (rocks[3] + 0.8, {"rot": 1.2}),
                   (rocks[3] + 1.6, {"rot": -0.6}), (rocks[3] + 2.5, {"rot": 0.0})], "sine")
    bm = E.boat_bob(g0, extra=lambda t: (bx(t), tilt(t).rot, 0.0))
    night = lambda t: M.progress(t, t_set - 0.3, rocks[3] + 0.6, "sine")
    day_off = lambda t: Tf(alpha=1.0 if night(t) < 0.999 else 0.0)
    night_on = lambda t: Tf(alpha=night(t))

    # ------------------------------------------------------------ backdrop: the sunset set, the night fading in on top
    E.add_backdrop(sc, g0)
    for lay in sc.layers:
        if lay.name in ("clouds",) or lay.name.startswith("glints"):
            base = lay.motion
            lay.motion = (lambda base: lambda t: Tf(dx=base(t).dx, dy=base(t).dy,
                                                    alpha=base(t).alpha * (1 - night(t))))(base)
    star_entries = [(0.0, 0), (rocks[0] - 1.3, 1), (rocks[1] + 0.3, 2), (rocks[3] + 0.1, 3)]
    for k in range(min(len(star_ts), len(NIGHT_P) - 4)):
        star_entries.append((star_ts[k] - 0.04, 4 + k))
    star_entries.sort()

    def star_fa(t):
        f = 0.0
        for tk, i in star_entries:
            if t >= tk:
                f = i - 1 + min(1.0, (t - tk) / 0.22) if i > 0 else 0.0
        return max(0.0, f)
    sc.add("night_sky", [night_sky_svg(p) for p in NIGHT_P], z=0.7, wc=0.5, frame_at=star_fa, motion=night_on)
    sc.add("night_back", E.back_svg("night"), z=2.1, motion=night_on)
    for i, (vx, per) in enumerate(((5.0, 2.9), (-4.0, 3.6))):
        sc.add(f"nglints{i}", E.glints_svg(31 + i, "night"), z=3.1, wc=0, motion=lambda t, vx=vx, per=per, i=i: Tf(
            dx=vx * ((t + g0) - 80.0), alpha=night(t) * (0.5 + 0.45 * math.sin(2 * math.pi * ((t + g0) / per +
                                                                                              0.5 * i)))))
    moon_on = lambda t: Tf(alpha=night(t) ** 2 * (0.75 + 0.25 * math.sin(2 * math.pi * (t + g0) / 2.1)))
    sc.add("moon_path_far", [moon_path_svg(E.YF7 + 8, BY7 - 6, 3 + k) for k in range(3)], z=3.2, wc=0,
           frame_at=lambda t: float(int((t + g0) / 0.4) % 3), motion=moon_on)
    sc.add("night_band", E.band_svg("night"), z=14.1, motion=night_on)
    sc.add("night_shore", E.shore_svg("night"), z=15.1, motion=night_on)
    sc.add("moon_path_near", [moon_path_svg(BY7 + 14, H + 10, 7 + k) for k in range(3)], z=15.2, wc=0,
           frame_at=lambda t: float(int((t + g0) / 0.4 + 1) % 3), motion=moon_on)

    # ------------------------------------------------------------ the boat (day layers continue s06; night versions)
    back_m = E.boat_back_markup("out", "furled")
    sc.add("boat_back", doc7(back_m), z=10, motion=bm, seed=41)
    sc.add("boat_back_n", doc7(back_m, night=True), z=10.05, motion=M.combine(bm, night_on), seed=41)
    sc.add("sail", doc7(E.sail_clip_markup()), z=10.2, motion=bm, seed=43)
    sc.add("sail_n", doc7(E.sail_clip_markup(), night="dim"), z=10.25, motion=M.combine(bm, night_on), seed=43)
    front = [E.boat_front_markup("out", k / 8) for k in range(8)]
    sc.add("boat_front", [doc7(m) for m in front], z=13, frame_at=row_k, motion=M.combine(bm, day_off), seed=59)
    sc.add("boat_front_n", [doc7(m, night=True) for m in front], z=13.05, frame_at=row_k,
           motion=M.combine(bm, night_on), seed=59)

    # far row: they watch where they are going, then turn to smile at Jesus asleep
    t_turn = [snap(t_wei + 0.35 + 0.15 * j) for j in range(4)]
    far_draw = lambda n: E.far_row_markup([1 if c == "1" else -1 for c in n.split("|")[0]],
                                          ["happy" if n.split("|")[1] == "h" else "kind"] * 4)
    far = Actor("crew_far", far_draw, (BX7, BY7), BK7, 11, seed=47, docf=doc7, carrier=bm)
    far.cut(0, "1111|h")
    for j in range(4):
        far.cut(t_turn[j], "".join("0" if k <= j else "1" for k in range(4)) + ("|h" if j < 3 else "|k"), dip_=False)
    far.build(sc)
    sc.add("crew_far_n", doc7(far_draw("0000|k"), night=True), z=11.05, motion=M.combine(bm, night_on), seed=47)

    # Jesus: yawns, sits on the stern, lies down on the cushion and falls asleep
    def jd(n):
        pose, expr, f = n.split("|")
        x, y = {"sit": E.STERN_SEAT7, "sleep": E.SLEEP7}.get(pose, E.DECK)
        return C.jesus(x, y, BK7, int(f), pose=pose, expr=expr, marks=False)
    ja = Actor("jesus", jd, E.DECK, BK7, 12, seed=49, docf=doc7, carrier=bm)
    ja.cut(0, "stand|warm|1")
    t_yawn = snap(t_tired - 0.04)
    ja.cut(t_yawn, "stand|sleepy|1", dip_=False)
    t_sit = snap(t_day + 0.3)
    ja.cut(t_sit, "sit|warm|1", depth=8)
    t_lie = snap(t_wei - 0.02)
    ja.cut(t_lie, "sleep|peaceful|1", depth=6)
    ja.cut(snap(t_sleep), "sleep|sleepy|1", dip_=False)
    ja.add_blinks({"stand|warm|1": f"stand|{blink('warm')}|1", "sit|warm|1": f"sit|{blink('warm')}|1"},
                  t_lie - 0.3, rng, t_from=1.3)
    stretch = lambda t: Tf(sy=1 + 0.035 * math.sin(math.pi * min(1.0, max(0.0, (t - t_yawn) / max(0.3, t_sit - t_yawn)))),
                           px=E.DECK[0], py=E.DECK[1])
    sink = lambda t: Tf(dy=-(E.STERN_SEAT7[1] - E.DECK[1]) * 0.5 * (1 - M.progress(t, t_sit, t_sit + 0.3, "out"))
                        if t_sit <= t < t_lie else 0.0)
    settle = lambda t: Tf(dy=-12 * (1 - M.progress(t, t_lie, t_lie + 0.35, "out")) if t >= t_lie else 0.0)
    sleep_breath = lambda t: Tf(sy=1 + (0.022 * math.sin(2 * math.pi * (t + g0) / 3.6) if t >= t_lie else 0.0),
                                px=E.SLEEP7[0], py=E.SLEEP7[1])
    ja.mots += [stretch, sink, settle, E.breathe_g(g0, 0.009, 3.2, E.DECK), sleep_breath]
    ja.build(sc)
    sc.add("jesus_n", doc7(jd("sleep|sleepy|1"), night=True), z=12.05, seed=49,
           motion=on_boat(M.combine(sleep_breath, lambda t: Tf(alpha=night(t) if t >= t_lie + 0.5 else 0.0)), bm))

    # the rowers (phase 0 = s06's last drawing)
    for j in range(2):
        px, py = BP7["seats"][E.ROWERS[j][2]]
        fr = [E.rower_markup(j, "row", k / 8) for k in range(8)]
        br = E.breathe_g(g0, 0.01, 2.9 + 0.3 * j, (px, py), 0.3 * j)
        sc.add(f"rower{j}", [doc7(m) for m in fr], z=12.5 + 0.01 * j, frame_at=row_k, seed=51 + j,
               motion=on_boat(M.combine(br, day_off), bm))
        sc.add(f"rower{j}_n", [doc7(m, night=True) for m in fr], z=12.505 + 0.01 * j, frame_at=row_k, seed=51 + j,
               motion=on_boat(M.combine(br, night_on), bm))

    # Andrew lets go of the halyard (tied off); Simon, Peter, Judas
    av, (ax, ay) = E.ANDREW
    t_tie = snap(t_tired - 0.5)
    an = Actor("andrew", lambda n: E.disc(ax, ay, av, n.split("|")[0], int(n.split("|")[2]), n.split("|")[1]),
               (ax, ay), BK7, 12.7, seed=55, docf=doc7, carrier=bm)
    an.cut(0, "pull_rope|determined|1")
    an.cut(t_tie, "stand|happy|-1", depth=6)
    an.cut(snap(t_wei + 0.5), "stand|kind|-1", dip_=False)
    an.add_blinks({"stand|happy|-1": f"stand|{blink('happy')}|-1", "stand|kind|-1": f"stand|{blink('kind')}|-1"},
                  T, rng, t_from=t_tie + 0.4)
    an.build(sc)
    sc.add("andrew_n", doc7(E.disc(ax, ay, av, "stand", -1, "kind"), night=True), z=12.705, seed=55,
           motion=M.combine(bm, night_on))
    sc.add("halyard", doc7(E.rope_markup()), z=12.69, wc=0.3, motion=M.combine(bm, lambda t: Tf(
        alpha=1.0 if t < t_tie else 0.0)))
    for nm, (v, (px, py)), f, ex, ex2 in (("simon", E.SIMON, -1, "kind", "kind"), ("peter", E.PETER, 1, "happy", "happy"),
                                          ("judas", E.JUDAS, -1, "happy", "kind")):
        a = Actor(nm, lambda n, px=px, py=py, v=v, f=f: E.disc(px, py, v, "stand", f, n), (px, py), BK7, 12.7,
                  seed=E.CREW_SEED[nm], docf=doc7, carrier=bm)
        a.cut(0, ex)
        if ex2 != ex:
            a.cut(snap(t_wei + 0.6), ex2, dip_=False)
        a.add_blinks({ex: blink(ex), ex2: blink(ex2)}, T, rng, t_from=1.4)
        br = E.breathe_g(g0, 0.01, 3.1, (px, py), 0.4)
        a.mots += [br]
        a.build(sc)
        sc.add(f"{nm}_n", doc7(E.disc(px, py, v, "stand", f, ex2), night=True), z=12.705, seed=E.CREW_SEED[nm],
               motion=on_boat(M.combine(br, night_on), bm))

    # James and John: the last shove, then a jump into the boat (far row spots 1 and 0)
    for k, ((v, (px, py)), spot, t_hop) in enumerate(((E.JAMES_BEACH, BP7["far_stand"][1], snap(t_push1 + 0.02)),
                                                       (E.JOHN_BEACH, BP7["far_stand"][0], snap(t_push1 + 0.16)))):
        nm = ("james", "john")[k]
        br = E.breathe_g(g0, 0.01, 2.8 + 0.4 * k, (px, py), 0.2 * k)
        a = Actor(nm, lambda n, px=px, py=py, v=v: C.ground_shadow(px, py, BK7, 120, 0.15) * (n.startswith("push")) +
                  E.disc(px, py, v, n.split("|")[0], 1, n.split("|")[1]), (px, py), BK7, 20 + py / 100, seed=61 + k,
                  docf=doc7)
        a.cut(0, "push|determined")
        a.cut(t_hop, "walk_b|happy", depth=4)
        lx, ly = spot
        t_land = snap(t_hop + 0.36)

        def hop_m(t, px=px, py=py, lx=lx, ly=ly, t_hop=t_hop, t_land=t_land):
            lean = 4.0 * M.progress(t, t_push0, t_push0 + 0.3, "sine") * (1 - M.progress(t, t_push1 - 0.2, t_push1,
                                                                                           "sine"))
            if t < t_hop:
                return Tf(rot=lean, px=px, py=py)
            if t >= t_land:
                return Tf(alpha=0.0)
            u = (t - t_hop) / (t_land - t_hop)
            tx = lx + bx(t_land) - px
            return Tf(dx=tx * u, dy=(ly - py) * u - 70 * math.sin(math.pi * u))
        a.mots += [hop_m, br]
        a.build(sc)
        inb = lambda n, lx=lx, ly=ly, v=v: E.disc(lx, ly, v, "stand", 1 if n == "h" else -1, "happy" if n == "h" else "kind")
        b = Actor(nm + "_in", inb, (lx, ly), BK7, 11.01 + 0.01 * k, seed=63 + k, docf=doc7, carrier=bm)
        b.cut(0, "h")
        b.cut(snap(t_wei + 0.45 + 0.2 * k), "k", dip_=False)
        b.mots += [lambda t, t_land=t_land: Tf(alpha=1.0 if t >= t_land else 0.0),
                   lambda t, t_land=t_land, lx=lx, ly=ly: Tf(
                       dy=0.0 if t < t_land else 4 * math.sin(math.pi * min(1.0, (t - t_land) / 0.25)),
                       sy=1.0 if t < t_land else 1 - 0.05 * math.sin(math.pi * min(1.0, (t - t_land) / 0.25)),
                       px=lx, py=ly)]
        b.build(sc)
        sc.add(nm + "_in_n", doc7(inb("k"), night=True), z=11.015 + 0.01 * k, seed=63 + k,
               motion=M.combine(bm, night_on))

    # the boat lantern: lit as dusk falls; it hangs plumb while the boat rocks
    t_light = t_others - 0.7
    tilt_deg = lambda t: tilt(t).rot
    sc.add("lantern", E.lantern_svg(False), z=13.5, seed=45, motion=E.lantern_motion(bm, g0, tilt_deg))
    sc.add("lantern_lit", E.lantern_svg(True), z=13.55, seed=46, wc=0.4,
           motion=E.lantern_motion(bm, g0, tilt_deg, lit_t=t_light))

    # z's floating up from Jesus asleep
    head = (E.SLEEP7[0] - 142 * BK7, E.SLEEP7[1] - 78 * BK7)
    t_z0 = snap(t_sleep + 0.1)
    for i in range(3):
        zs = 40 + 10 * i
        zsvg = doc7(S.text(head[0] + 30, head[1] - 20, "z", size=zs, fill="#fff2d6", weight="bold",
                           extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"'))

        def z_m(t, i=i):
            if t < t_z0 + 0.6 * i:
                return Tf(alpha=0.0)
            u = ((t - t_z0 - 0.6 * i) / 1.8) % 1.0
            b = bm(t)
            k = 0.6 + 0.6 * u
            a = math.sin(math.pi * u) * (1 - 0.35 * night(t))
            return Tf(dx=b.dx + 18 * u + 12 * math.sin(4 * u), dy=b.dy - 70 * u, sx=k, sy=k, alpha=a,
                      px=head[0] + 30, py=head[1] - 20)
        sc.add(f"zz{i}", zsvg, z=13.7, wc=0, motion=z_m)

    # the shore people (global clock) and the small boats that follow
    E.add_shore_people(sc, g0, T)
    followers = [(E.MOORED[0], t_others - 1.0, 100.0), (E.MOORED[1], t_others - 0.6, 95.0),
                 ((1, -260, 712, 0.3, 1), t_others + 0.3, 150.0)]
    for i, ((var, x, y, k, f), t_go, vmax) in enumerate(followers):
        def fx_(t, t_go=t_go, vmax=vmax):
            if t < t_go:
                return 0.0
            u = t - t_go
            return vmax * (u - 1.0 * (1 - math.exp(-u / 1.0)))
        ff = 1 if i < 2 else f
        mot = lambda t, i=i, fx_=fx_: Tf(dx=fx_(t), dy=1.5 * math.sin(2 * math.pi * ((t + g0) / 3.3 + 0.4 * i)))
        if i < 2:
            sc.add(f"smallboat{i}", [E.small_boat_svg(x, y, k, f, var, lantern=False),
                                     E.small_boat_svg(x, y, k, ff, var, lantern=True)], z=9 + 0.01 * i, seed=70 + i,
                   frame_at=lambda t, t_go=t_go: M.progress(t, t_go - 0.4, t_go, "sine"), motion=M.combine(mot, day_off))
        else:
            sc.add(f"smallboat{i}", E.small_boat_svg(x, y, k, ff, var, lantern=True), z=8.9, seed=72,
                   motion=M.combine(mot, day_off))
        sc.add(f"smallboat{i}_n", E.small_boat_svg(x, y, k, ff, var, time="night", lantern=True), z=9.005 + 0.01 * i,
               seed=75 + i, motion=M.combine(mot, night_on))
    sc.add("tufts", [E.tufts_svg(k) for k in range(3)], z=40,
           frame_at=lambda t: float((0, 1, 2, 1)[int((t + g0) / 0.6) % 4]))

    # twinkles once the stars are out; a soft glow on the moon's path
    sc.fx.append(FX.sparkles((MOON[0] - 1200, 40, MOON[0] + 500, 420), count=10, t0=star_ts[-1] - 0.4, t1=T + 1,
                             color=(250, 244, 214), size=(8, 15), period=1.7, drift=0, seed=91))

    # ------------------------------------------------------------ camera: travels with the boat
    keys = M.cam_keys([
        (0.0, Cam(10, 588, 1780)), (1.0, Cam(10, 588, 1780)), (t_row + 0.2, Cam(20, 600, 1660)),
        (t_sit, Cam(-200, 632, 1100)), (t_sleep + 0.4, Cam(-235, 636, 1050)),
        (t_others + 1.6, Cam(-430, 572, 1800)), (t_set + 0.2, Cam(-390, 566, 1820)),
        (rocks[0] - 0.2, Cam(-150, 590, 1640)), (star_ts[0] - 0.3, Cam(-60, 540, 1720)),
        (star_ts[-1], Cam(20, 520, 1700)), (T, Cam(30, 520, 1690))],
        ["linear", "sine", "inout", "sine", "inout", "inout", "inout", "inout", "sine", "linear"])

    def cam(t):
        c = keys(t)
        w = c.w
        x = BX7 + bx(t) + c.x if t >= 1.0 else E.BX7 + c.x
        x = min(max(x, w / 2 + 2), W7 - w / 2 - 2)
        hh = w * 9 / 32
        y = min(max(c.y, hh + 2), H - hh - 2)
        return Cam(x, y, w)
    sc.camera = cam

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-15, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", 0, dur=t_others, gain_db=-26, fade_in=0.8, fade_out=2.5)
    sc.sfx("splash_small", t_push0 + 0.1, gain_db=-16, pan=-0.2)
    sc.sfx("splash_small", t_push1 + 0.4, gain_db=-19, pan=-0.1)
    sc.sfx("thud", t_push1 + 0.4, gain_db=-20)
    sc.sfx("oars", t_row, dur=t_slow1 - t_row + 1.0, gain_db=-17, fade_in=0.4, fade_out=1.5)
    sc.sfx("cloth", t_sit, gain_db=-20)
    sc.sfx("cloth", t_lie, gain_db=-19)
    sc.sfx("oars", t_others, dur=5.0, gain_db=-24, fade_in=0.8, fade_out=1.5, pan=-0.5)
    for k, tr in enumerate(rocks):
        sc.sfx("ship_creak", tr, dur=1.0, gain_db=-21 - k, fade_in=0.1, fade_out=0.5, pan=0.15 * (-1) ** k)
    sc.sfx("night", rocks[0] - 1.0, dur=T - rocks[0] + 1.3, gain_db=-21, fade_in=2.0, fade_out=1.0)
    sc.sfx("sparkle", star_ts[0], gain_db=-21)
    sc.sfx("sparkle", star_ts[min(7, len(star_ts) - 1)], gain_db=-22)
    return sc
