"""Scene 9 - the disciples are terrified (Mark 4:37-38): 门徒们吓坏了。他们好多人是打鱼的，可是从来没见过这么大的
风浪！ / M 抓紧！快把水舀出去！ / 他们拼命地舀水，可是水越舀越多。小船摇来摇去，好像就要沉下去了。

The shared boat world of s08_storm (same stage, boat, crew, sky and lake; everything that moves through a dissolve
keyed to film time). It opens on exactly s08's last frame (plain cross-dissolve) and ends on the steady storm that
s10_wake opens with (sail brailed up, water at .8).

Beats (voice-measured phrase marks of the take):
  start          the full storm, wide (= s08's end): Peter clings to the mast, John holds the sail rope, the others
                 scared, arms up; the sail flapping; water .5 inside.
  '门徒们吓坏了'  the camera moves in close on the crew: faces go panicked (trembling); John hauls on the rope three
                 times and the flapping sail is brailed up to the yard, tied (furled).
  '他们好多人是打鱼的' a little memory bubble pops up over the stern: the same fishermen on a sunny day on the
                 lake - Peter laughing as he hauls a net full of flapping fish, John casting his net, Andrew waving.
  '可是从来没见过这么大的风浪' the bubble pops away; the camera pulls back: a huge swell lifts the waves round the
                 boat (back and front rows rise), the boat lurches, spray bursts at bow and stern, a big gust.
  M '抓紧！'      Peter lets go of the mast and shouts, an arm flung out.
  '快把水舀出去！' they grab buckets and bowls: Andrew, James, Thomas, Simon, Peter, Matthew, Judas, Philip start
                 bailing (scoop - lift - throw cycles, water arcs flying over the side).
  '他们拼命地舀水' bailing hard, the camera close on the bailers.
  '可是水越舀越多' two more waves slop in over the gunwale: the water inside rises .5 -> .65 -> .8.
  '小船摇来摇去'  the camera pulls back; the boat rocks hard (tilt up to +-7.6); everybody drops the buckets and
                 holds on, scared again.
  '好像就要沉下去了' a big dip: the boat sinks low between rising waves, then rides up again.
  end            the steady storm, wide (= s10's first frame).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from engine.motion import Cam, Tf
from engine.scene import Scene

from .s08_storm import CAM_END as S8_CAM_END
from .s08_storm import (BP, CREW, K, SH, STORM_BOB, STORM_TILT, SW, TREMBLE, Actor, Rain,
                        Rock, Wind, add_boat, add_sail, add_spray, add_storm_lake, add_storm_sky, beat, breath,
                        cam_path, dip, disciple, doc, flinch, foot_of, gframe, hop, jesus_body, jitter, keyed,
                        seed_of, snap, storm_body)

# the memory bubble over the stern
IX, IY, IRX, IRY = 2150, 680, 290, 190
MEM_PIVOT = (IX - 230, IY + 185)      # the bubble pops from the end of its thought-dot trail

BAILERS = {   # name: (facing, item, cycle offset, start delay); all throw downwind, toward the bow (never on Jesus)
    "andrew": (1, "bucket", 0, 0.20), "james": (1, "bucket", 3, 0.30), "thomas": (1, "bowl", 1, 0.36),
    "simon": (1, "bowl", 4, 0.42), "peter": (1, "bucket", 2, 0.56), "matthew": (1, "bowl", 5, 0.30),
    "judas": (1, "bucket", 2, 0.46), "philip": (1, "bowl", 4, 0.52),
}
BAIL_PH = [0.0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6]
CAM_END = Cam(1600, 935, 2400)        # s09's last camera = s10's first


def memory_body(k):
    """The sunny memory: a little oval picture of the fishermen on a bright day (k = animation phase 0..3)."""
    x0, x1, y0, y1 = IX - IRX - 10, IX + IRX + 10, IY - IRY - 10, IY + IRY + 10
    out = PR.lake_galilee(x0, x1, y1 - 4, scale=0.5, time="day", shore=None, part="back", boats=False, top=y0,
                          bottom=y1, phase=k / 4, seed=3)
    # the sun with soft rays
    sx, sy = IX + 175, IY - 105
    out += (f'<defs>{S.rad_grad("s9sun", [(0, "#fff6d0", 0.95), (0.4, "#fbe08a", 0.5), (1, "#fbe08a", 0)])}</defs>'
            f'<circle cx="{sx}" cy="{sy}" r="120" fill="url(#s9sun)"/>')
    out += S.path(S.rays(sx, sy, 48, 88, n=10, width_deg=9, rot=8 + 6 * k), "#f6d36a", stroke=False,
                  extra='opacity="0.7"')
    out += PR._circ(sx, sy, 32, "#fbd46b", 3.2)
    # the boat (sail furled: they are fishing) with four happy fishermen
    bx, by, k2 = IX - 10, IY + 188, 0.45
    bp = PR.boat_points(bx, by, k2, 1)
    out += PR.fishing_boat(bx, by, k2, 1, sail="furled", phase=k / 4, part="back", nets=False)
    out += C.disciples(*bp["far_stand"][1], k2, 1, variant="james", pose="stand", expr="laugh")
    out += C.disciples(*bp["stand"][1], k2, -1, variant="john", pose="cast_net", phase=(0.15, 0.5, 0.9, 1.0)[k])
    out += C.disciples(*bp["stand"][2], k2, 1, variant="andrew", pose="wave", phase=k / 4, expr="smile")
    out += C.disciples(*bp["stand"][4], k2, 1, variant="peter", pose="haul_net", phase=k / 4)
    out += PR.fishing_boat(bx, by, k2, 1, sail="furled", phase=k / 4, part="front", nets=False)
    out += PR.lake_band(x0, x1, by - 3, y1 + 4, time="day", phase=k / 4, scale=0.5)
    for i, (fx, fy, fl) in enumerate(((IX + 215, IY + 150, 1), (IX - 235, IY + 160, -1))):
        jump = (0, 1, 0.6, 0)[(k + i * 2) % 4]
        if jump:
            out += PR.lake_fish(fx, fy - 30 * jump, 0.6, 1 if i else -1, flap=0.8 * fl * (1 if k % 2 else -1),
                                rot=-30 * jump if i else 30 * jump)
    cid = "s9memclip"
    ell = f"M{IX - IRX},{IY} a{IRX},{IRY} 0 1 0 {2 * IRX},0 a{IRX},{IRY} 0 1 0 {-2 * IRX},0 Z"
    body = f'<clipPath id="{cid}"><path d="{ell}"/></clipPath><g clip-path="url(#{cid})">{out}</g>'
    frame = (f'<ellipse cx="{IX + 8}" cy="{IY + 12}" rx="{IRX + 14}" ry="{IRY + 14}" fill="#1c2232" opacity="0.35" '
             f'filter="url(#soft)"/>'
             f'<ellipse cx="{IX}" cy="{IY}" rx="{IRX + 13}" ry="{IRY + 13}" fill="#f7efdc" stroke="{PR.INK}" '
             f'stroke-width="4"/>')
    ring = f'<ellipse cx="{IX}" cy="{IY}" rx="{IRX}" ry="{IRY}" fill="none" stroke="{PR.INK}" stroke-width="3.5"/>'
    # thought-bubble dots down toward the fishermen in the storm (Peter at the mast, John)
    dots = ""
    for dx, dy, r in ((-200, 172, 21), (-236, 206, 15), (-260, 232, 10)):
        dots += PR._circ(IX + dx, IY + dy, r, "#f7efdc", 3.5)
    return S.g(frame, filter="wobble-fine") + body + S.g(ring + dots, filter="wobble-fine")


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration

    t_scared = beat(ctx, 0, "吓坏")
    t_fish = beat(ctx, 0, "他们好多")
    t_never = beat(ctx, 0, "可是")
    t_big = beat(ctx, 0, "这么大")
    t_waves = beat(ctx, 0, "风浪")
    t_hold = beat(ctx, 1, "抓紧")
    t_bail = beat(ctx, 1, "快把")
    t_scoop = beat(ctx, 1, "舀出去")
    t_hard = beat(ctx, 2, "拼命")
    t_more = beat(ctx, 2, "越舀越多")
    t_more2 = beat(ctx, 2, "越多")
    t_rock = beat(ctx, 2, "小船")
    t_rock2 = beat(ctx, 2, "摇来摇去")
    t_sink = beat(ctx, 2, "沉下去")
    t_end = ctx.lines[2].end
    t_calm = min(t_sink + 0.55, T - 1.4)                # everything back to the steady storm before the dissolve
    t_mem_out = t_never - 0.18

    # ---------------- camera
    C1 = S8_CAM_END                            # = s08's last camera
    C9a = Cam(1640, 975, 1500)                 # close on the scared faces
    C9m = Cam(1700, 925, 1700)                 # room for the memory bubble
    C9b = Cam(1600, 935, 2460)                 # the big waves
    C9c = Cam(1610, 970, 1560)                 # the bailers
    C9d = CAM_END                              # the boat rocking (= s10's first camera)
    sc.camera = cam_path([(0, C1), (max(1.02, t_scared - 0.5), C1), (t_scared + 0.85, C9a), (t_fish - 0.45, C9a),
                          (t_fish + 0.2, C9m), (t_never - 0.05, C9m), (t_big + 0.2, C9b), (t_waves + 0.9, C9b),
                          (t_hold + 0.1, C9c), (t_rock - 0.1, C9c), (t_rock2 + 0.6, C9d), (T, C9d)],
                         bumps=[(t_big + 0.1, 12, 0.8), (t_waves, 10, 0.7), (t_more + 0.1, 7, 0.5),
                                (t_sink + 0.2, 10, 0.9)])

    # ---------------- the boat's motion: storm swell, a lurch on the big wave, hard rocking, a deep dip
    amp = keyed([(0, STORM_TILT), (t_rock, STORM_TILT), (t_rock2 + 0.3, 7.6), (t_sink, 7.0),
                 (T - 1.1, STORM_TILT)])
    bob = keyed([(0, STORM_BOB), (t_rock, STORM_BOB), (t_rock2 + 0.3, 10.0), (T - 1.1, STORM_BOB)])

    def dip_extra(t):
        u = keyed([(t_sink - 0.4, 0.0), (t_sink + 0.2, 1.0), (t_sink + 0.5, 1.0), (T - 1.1, 0.0)], "sine")(t)
        return (0.0, 11.0 * u)
    rock = Rock(ctx, amp, bob, kicks=[(t_big + 0.05, 4.0, -8.0), (t_waves, -3.5, 6.0), (t_more + 0.05, 2.5, 4.0),
                                     (t_more2 + 0.45, -2.5, 4.0)], extra=dip_extra)

    # ---------------- sky (the storm, steady) and the waves (a huge swell, then the dip)
    add_storm_sky(sc, ctx, lambda t: 1.0)
    swell = keyed([(t_big - 0.3, 0.0), (t_big + 0.35, 0.65), (t_waves + 0.5, 0.65), (t_waves + 1.4, 0.0),
                   (t_sink - 0.4, 0.0), (t_sink + 0.25, 1.0), (t_sink + 0.55, 1.0), (T - 1.1, 0.0)], "sine")
    add_storm_lake(sc, ctx, [1.0, 1.2], lambda t: min(1.0, swell(t) * 1.4), back_dy=lambda t: -30 * swell(t),
                   front_dy=lambda t: -48 * swell(t))

    # ---------------- the boat (sail brailed up by John's three hauls)
    t_tug = [snap(t_scared - 0.35 + 0.42 * i) for i in range(3)]
    t_furl = snap(t_tug[2] + 0.42)
    hauls = [0.3, 0.6, 0.85]
    wl = [0.5, 0.65, 0.8]
    water = keyed([(t_more - 0.05, 0.0), (t_more + 0.3, 1.0), (t_more2 + 0.45, 1.0), (t_more2 + 0.8, 2.0)])
    add_boat(sc, ctx, rock, lambda t: 1.0, wl, water, lantern_amp=lambda t: 18.0)
    def haul_at(t):
        h = hauls[0]
        for tt, hv in zip(t_tug, hauls):
            if t >= tt:
                h = hv
        return h
    add_sail(sc, ctx, rock, [(0, "flap"), (t_tug[0], "haul", hauls, haul_at), (t_furl, "furled", 3)])

    # ---------------- the crew
    panic = {"andrew", "james", "thomas", "philip", "matthew", "jamesa", "judas"}
    for k, name in enumerate(CREW):
        foot = BP["cling"] if name == "peter" else foot_of(name)
        a = Actor(ctx, name, foot, rock)
        base = storm_body(name)
        a.at(0, base)
        cuts = []
        if name in panic:
            tp = snap(t_scared + 0.05 + 0.05 * (k % 4))
            a.at(tp, storm_body(name, expr="panicked"))
            cuts.append(tp)
        if name == "john":
            for tt in t_tug:   # three hauls: lean back, then forward again
                a.move(hop(tt - 0.05, [(0, {"dx": 0, "rot": 0, "dy": 0}), (0.12, {"dx": 9 * K, "rot": 3.5, "dy": 3 * K}),
                                       (0.36, {"dx": 0, "rot": 0, "dy": 0})], ["out", "sine"]))
        if name == "peter":
            a.at(snap(t_hold), disciple(name, "shout", wet=True, wind=1.0, facing=1))
            cuts.append(snap(t_hold))
        if name in BAILERS:
            fc, item, off, dl = BAILERS[name]
            tb = snap(t_bail + dl)
            a.cycle(tb, [disciple(name, "bail", phase=p, item=item, wet=True, wind=1.0, facing=fc) for p in BAIL_PH],
                    step=3, offset=off)
            cuts.append(tb)
            tr = snap(t_rock + 0.12 + 0.04 * (k % 4))
            a.at(tr, base if name != "peter" else storm_body(name))
            cuts.append(tr)
        ts = snap(t_sink - 0.1 + 0.03 * (k % 3))
        a.at(ts, storm_body(name, expr="panicked") if name not in ("john",) else base)
        cuts.append(ts)
        a.at(snap(t_calm + 0.03 * (k % 4)), base)
        cuts.append(snap(t_calm + 0.03 * (k % 4)))
        for tc in cuts:
            a.move(dip(tc, 6.0))
        lx = CREW[name][1]
        a.move(breath(ctx, 0.007, 3.0 + 0.2 * k, k * 0.13), jitter(ctx, -1.0, 1e9, TREMBLE[name], seed=k + 1),
               flinch(t_big + 0.08, dx=-8.0 if lx > 0 else 8.0, depth=7.0),
               flinch(t_more + 0.08, dx=6.0, depth=4.0))
        a.add(sc)
    jz = Actor(ctx, "jesus", BP["sleep"], rock, z=12.0)
    jz.at(0, jesus_body("sleep")).move(breath(ctx, 0.012, 3.6)).add(sc)

    # ---------------- spray: the big swell, water slopping in, the dip
    add_spray(sc, ctx, rock, "spray_big0", t_big + 0.05, 560, seed=21, side=-1, scale=1.05)
    add_spray(sc, ctx, rock, "spray_big1", t_waves - 0.02, -480, seed=22, side=1, scale=0.95)
    add_spray(sc, ctx, rock, "spray_more0", t_more - 0.02, -60, seed=23, side=1, scale=0.85)
    add_spray(sc, ctx, rock, "spray_more1", t_more2 + 0.42, 380, seed=24, side=-1, scale=0.85)
    add_spray(sc, ctx, rock, "spray_sink", t_sink + 0.15, 120, seed=25, side=1, scale=1.0)

    # ---------------- the memory bubble
    pop_in, pop_out = snap(t_fish - 0.05), t_mem_out

    def mem(t):
        if t < pop_in or t > pop_out + 0.3:
            return Tf(alpha=0.0)
        if t < pop_in + 0.4:
            u = (t - pop_in) / 0.4
            s = 0.35 + 0.65 * (1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2)
            return Tf(sx=s, sy=s, alpha=min(1.0, u / 0.35), px=MEM_PIVOT[0], py=MEM_PIVOT[1])
        if t > pop_out:
            u = (t - pop_out) / 0.3
            s = 1 - 0.4 * u
            return Tf(sx=s, sy=s, alpha=1 - u, px=MEM_PIVOT[0], py=MEM_PIVOT[1])
        return Tf(px=MEM_PIVOT[0], py=MEM_PIVOT[1], dy=4 * math.sin(2 * math.pi * (t - pop_in) / 2.0))
    sc.add("memory", [doc(memory_body(k)) for k in range(4)], z=30, wc=0.8, seed=seed_of("memory"),
           frame_at=lambda t: float((gframe(ctx, t) // 7) % 4), motion=mem)

    # ---------------- weather
    mem_on = lambda t: mem(t).alpha                              # no rain / wind streaks over the sunny memory
    sc.fx.append(Rain(ctx, lambda t: 0.62, bubble=((IX, IY, IRX + 16, IRY + 16), mem_on)))
    sc.fx.append(Wind(ctx, lambda t: 0.95, gusts=[(t_waves - 0.15, 1.0, 0.9), (t_rock2 - 0.1, 1.0, 0.8)],
                      avoid=((IX, IY, IRX + 40, IRY + 40), mem_on)))

    # ---------------- sound
    for nm, g in (("storm_wind", -17), ("waves_storm", -15), ("rain", -19), ("ship_creak", -21)):
        sc.sfx(nm, 0.0, dur=T, gain_db=g, fade_in=0.8, fade_out=0.8)
    for tt in t_tug:
        sc.sfx("cloth", tt, gain_db=-15)
    sc.sfx("chime", pop_in, gain_db=-16)
    sc.sfx("birds", pop_in + 0.1, dur=pop_out - pop_in, gain_db=-24, fade_in=0.3, fade_out=0.3)
    sc.sfx("pop", pop_out, gain_db=-16)
    sc.sfx("whoosh", t_big - 0.1, gain_db=-10)
    sc.sfx("splash", t_big + 0.05, gain_db=-7, pan=0.4)
    sc.sfx("splash", t_waves - 0.02, gain_db=-8, pan=-0.4)
    sc.sfx("splash_small", t_more - 0.02, gain_db=-11)
    sc.sfx("splash_small", t_more2 + 0.42, gain_db=-11, pan=0.3)
    sc.sfx("splash", t_sink + 0.15, gain_db=-8)
    sc.sfx("whoosh", t_rock2 - 0.1, gain_db=-12)
    sc.sfx("splash_small", t_scoop + 0.6, gain_db=-16, pan=-0.3)
    sc.sfx("splash_small", t_hard + 0.2, gain_db=-16, pan=0.3)
    sc.sfx("splash_small", t_hard + 0.8, gain_db=-17, pan=-0.2)
    return sc
