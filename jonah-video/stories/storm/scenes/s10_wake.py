"""Scene 10 - Jesus still asleep; they wake him (Mark 4:38): 可是，耶稣还在睡觉。门徒们赶快叫醒他：
M 老师！老师！我们快要淹死了，你不管吗？

The shared boat world of s08_storm. Opens on s09's last frame (plain cross-dissolve), ends on the frame s11_calm
opens with (Jesus just woken, propped on his elbow; Andrew's hands still on his shoulder).

Beats (voice-measured phrase marks of the take):
  start          the steady storm, wide (= s09's end).
  '可是'          the camera glides to the stern.
  '耶稣还在睡觉'  close on Jesus, peacefully asleep on the cushion in the middle of the storm: a small bubble of
                 warm, calm light grows round him (no rain falls inside it, a few warm motes), he breathes slowly.
  '门徒们赶快叫醒他' the disciples crowd round: Andrew hurries two steps to him and grabs his shoulder; James comes
                 behind him, calling; Philip and Bartholomew turn and lean toward him.
  M '老师！' '老师！' Andrew shakes him on each 老师 (wake_shake, jitter bursts), James and Philip shout.
  '我们快要淹死了' a wave slops in at the stern; panicked faces.
  '你不管吗'      at the end of the line Jesus wakes: up on one elbow, calm (wake pose); they freeze, amazed.
  end            hold (= s11's first frame).
"""
import math
import random

from PIL import Image, ImageDraw

from engine.motion import Cam, Tf
from engine.scene import Scene

from .s09_scared import CAM_END as S9_CAM_END
from .s08_storm import (BP, CREW, K, SH, STORM_BOB, STORM_TILT, SW, TREMBLE, Actor, Rain, Rock, Wind,
                        add_boat, add_sail, add_spray, add_storm_lake, add_storm_sky, beat, breath, cam_path, dip,
                        disciple, doc, foot_of, gtime, hop, jesus_body, jitter, keyed, on_boat, seed_of, snap,
                        storm_body)

LYING_GLOW = (1140, 930, 300, 196)        # centre and radii of the warm bubble round Jesus asleep
GLOW_SLEEP = 1.0
ANDREW_DX = BP["wake"][0] + 24 * K - foot_of("andrew")[0]     # Andrew by the wake spot, hands on Jesus' shoulder
JAMES_DX = (-300 - CREW["james"][1]) * K                       # James right behind him
CAM_END = Cam(1225, 985, 1230)        # s10's last camera = s11's first


def glow_body(cx, cy, rx, ry, gid):
    from art import style as S
    grad = S.rad_grad(gid, [(0, "#fff4cf", 1.0), (0.38, "#f8d77a", 0.55), (0.75, "#f2c14e", 0.16), (1, "#f2c14e", 0)])
    return f'<defs>{grad}</defs><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>'


def add_glow(sc, ctx, rock, name, box, alpha, z=10.7):
    """A warm light round Jesus (screen-blended, breathing slowly), riding with the boat."""
    cx, cy, rx, ry = box

    def own(t):
        a = alpha(t)
        if a <= 0.003:
            return Tf(alpha=0.0)
        p = 1 + 0.035 * math.sin(2 * math.pi * gtime(ctx, t) / 3.6)
        return Tf(alpha=a * (0.92 + 0.08 * math.sin(2 * math.pi * gtime(ctx, t) / 2.7)), sx=p, sy=p)
    sc.add(name, doc(glow_body(cx, cy, rx, ry, "s10" + name)), z=z, wc=0.0, blend="screen", seed=seed_of(name),
           motion=on_boat(rock, (cx, cy), own))


class Motes:
    """A few warm motes drifting up inside Jesus' calm bubble (film-time keyed); alpha(t)."""

    def __init__(self, ctx, box, alpha, n=12, seed=3):
        rng = random.Random(seed)
        self.ctx, self.box, self.alpha = ctx, box, alpha
        self.items = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(3, 6), rng.uniform(0, 1),
                       rng.uniform(10, 22)) for _ in range(n)]

    def __call__(self, frame, t, view):
        a0 = self.alpha(t)
        if a0 <= 0.01:
            return frame
        cx, cy, rx, ry = self.box
        g = gtime(self.ctx, t)
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ux, uy, r, ph, sp in self.items:
            u = (ph + g * sp / (2 * ry)) % 1.0
            x = cx + ux * rx * 0.7 + 8 * math.sin(g * 1.3 + ph * 6)
            y = cy + ry * 0.6 - u * ry * 1.3
            ox, oy = view.to_out(x, y)
            rr = r * view.scale
            a = int(170 * a0 * math.sin(math.pi * u))
            d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=(255, 238, 180, a))
        frame.alpha_composite(ov)
        return frame


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration

    t_but = beat(ctx, 0, "可是")
    t_sleep = beat(ctx, 0, "还在睡觉")
    t_disc = beat(ctx, 0, "门徒们")
    t_quick = beat(ctx, 0, "赶快")
    t_wake = beat(ctx, 0, "叫醒")
    t_m1 = beat(ctx, 1, "老师", 0)
    t_m2 = beat(ctx, 1, "老师", 1)
    t_drown = beat(ctx, 1, "淹死")
    t_care = beat(ctx, 1, "你不管")
    t_up = snap(min(ctx.lines[1].end - 0.12, T - 1.5))  # Jesus wakes at the end of the line

    # ---------------- camera: from the wide storm to the stern, a slow push in on the waking
    C9d = S9_CAM_END
    C10 = Cam(1235, 985, 1270)
    C10b = CAM_END                                      # = s11's first camera
    sc.camera = cam_path([(0, C9d), (max(1.02, t_but), C9d), (t_sleep + 0.85, C10), (t_m1 - 0.2, C10),
                          (t_up - 0.3, C10b), (T, C10b)],
                         bumps=[(t_drown + 0.12, 6, 0.5)])

    rock = Rock(ctx, lambda t: STORM_TILT, lambda t: STORM_BOB, kicks=[(t_drown + 0.1, -2.2, 4.0)])

    # ---------------- the steady storm
    add_storm_sky(sc, ctx, lambda t: 1.0)
    add_storm_lake(sc, ctx, [1.0], lambda t: 0.0)
    add_boat(sc, ctx, rock, lambda t: 1.0, [0.8], lambda t: 0.0, lantern_amp=lambda t: 18.0)
    add_sail(sc, ctx, rock, [(0, "furled", 3)])

    # ---------------- Jesus asleep in his bubble of light, then waking
    glow_a = keyed([(t_sleep - 0.25, 0.0), (t_sleep + 0.9, GLOW_SLEEP)], "sine")
    add_glow(sc, ctx, rock, "glow_lying", LYING_GLOW, glow_a)
    jz = Actor(ctx, "jesus", BP["sleep"], rock, z=12.0)
    jz.at(0, jesus_body("sleep")).at(t_up, jesus_body("wake"))
    jz.move(jitter(ctx, t_m1 + 0.02, t_m1 + 0.55, 1.4, step=2, seed=96, ramp=0.08),     # shaken a little on 老师
            jitter(ctx, t_m2 + 0.02, t_m2 + 0.55, 1.4, step=2, seed=97, ramp=0.08))
    jz.move(breath(ctx, 0.012, 3.6), hop(t_up, [(-0.1, {"dy": 0}), (0, {"dy": 3 * K}), (0.14, {"dy": -4 * K}),
                                               (0.32, {"dy": 0})], ["in", "out", "sine"]))
    jz.add(sc)

    # ---------------- the crew: most hold on, trembling; Andrew, James, Philip, Bartholomew crowd round
    a_dx, j_dx = ANDREW_DX, JAMES_DX
    t_a = [snap(t_disc + 0.08), snap(t_disc + 0.32), snap(t_disc + 0.56)]
    t_j = [snap(t_quick + 0.0), snap(t_quick + 0.24), snap(t_quick + 0.48)]
    for k, name in enumerate(CREW):
        foot = BP["cling"] if name == "peter" else foot_of(name)
        a = Actor(ctx, name, foot, rock)
        base = storm_body(name)
        a.at(0, base)
        trem_end = 1e9
        if name == "andrew":
            a.at(t_a[0], disciple(name, "walk_a", expr="panicked", wet=True, wind=1.0, facing=-1))
            a.at(t_a[1], disciple(name, "walk_b", expr="panicked", wet=True, wind=1.0, facing=-1))
            a.at(t_a[2], disciple(name, "wake_shake", wet=True, wind=1.0, facing=-1, at=foot))
            a.at(snap(t_up + 0.06), disciple(name, "wake_shake", expr="amazed", wet=True, wind=1.0, facing=-1,
                                             at=foot, marks=False))
            a.move(lambda t, a_dx=a_dx: Tf(dx=a_dx * (0.5 * keyed([(t_a[1] - 0.06, 0), (t_a[1] + 0.06, 1)], "sine")(t)
                                                        + 0.5 * keyed([(t_a[2] - 0.06, 0), (t_a[2] + 0.06, 1)],
                                                                      "sine")(t))),
                   hop(t_a[0], [(0, {"dy": 0}), (0.1, {"dy": -6 * K}), (0.22, {"dy": 0}), (0.34, {"dy": -6 * K}),
                                (0.46, {"dy": 0})]),
                   dip(t_a[2], 7.0), dip(snap(t_up + 0.06), 4.0))
            # shaking him: bursts on each 老师, smaller in between, stopping as he wakes
            a.move(jitter(ctx, t_a[2] + 0.2, t_up, 2.0, step=2, seed=91),
                   jitter(ctx, t_m1 - 0.05, t_m1 + 0.6, 4.5, step=2, seed=92, ramp=0.08),
                   jitter(ctx, t_m2 - 0.05, t_m2 + 0.6, 4.5, step=2, seed=93, ramp=0.08))
            trem_end = t_a[0]
        elif name == "james":
            a.at(t_j[0], disciple(name, "walk_a", expr="panicked", wet=True, wind=1.0, facing=-1))
            a.at(t_j[1], disciple(name, "walk_b", expr="panicked", wet=True, wind=1.0, facing=-1))
            a.at(t_j[2], disciple(name, "shout", wet=True, wind=1.0, facing=-1))
            a.at(snap(t_up + 0.08), disciple(name, "shout", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.move(lambda t, j_dx=j_dx: Tf(dx=j_dx * (0.5 * keyed([(t_j[1] - 0.06, 0), (t_j[1] + 0.06, 1)], "sine")(t)
                                                        + 0.5 * keyed([(t_j[2] - 0.06, 0), (t_j[2] + 0.06, 1)],
                                                                      "sine")(t))),
                   hop(t_j[0], [(0, {"dy": 0}), (0.1, {"dy": -6 * K}), (0.22, {"dy": 0}), (0.34, {"dy": -6 * K}),
                                (0.46, {"dy": 0})]),
                   dip(t_j[2], 6.0), dip(snap(t_up + 0.08), 4.0))
            a.move(jitter(ctx, t_m1 - 0.05, t_m1 + 0.5, 2.5, step=3, seed=94, ramp=0.08),
                   jitter(ctx, t_m2 - 0.05, t_m2 + 0.5, 2.5, step=3, seed=95, ramp=0.08))
            trem_end = t_j[0]
        elif name in ("philip", "bartholomew"):
            tc = snap(t_wake + (0.0 if name == "philip" else 0.18))
            a.at(tc, disciple(name, "shout", wet=True, wind=1.0, facing=-1))
            a.at(snap(t_up + 0.1), disciple(name, "shout", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.move(dip(tc, 6.0), dip(snap(t_up + 0.1), 4.0))
            trem_end = tc
        elif name in ("thomas", "matthew"):
            tc = snap(t_drown + 0.1 + 0.06 * (name == "matthew"))
            a.at(tc, storm_body(name, expr="panicked"))
            a.at(snap(t_up - 0.3), base)
            a.move(dip(tc, 5.0), dip(snap(t_up - 0.3), 4.0))
        a.move(breath(ctx, 0.007, 3.0 + 0.2 * k, k * 0.13), jitter(ctx, -1.0, trem_end, TREMBLE[name], seed=k + 1))
        a.add(sc)

    add_spray(sc, ctx, rock, "spray_stern", t_drown + 0.05, -560, seed=31, side=1, scale=0.75)

    # ---------------- weather (no rain inside the bubble)
    sc.fx.append(Rain(ctx, lambda t: 0.62, bubble=(LYING_GLOW, lambda t: min(1.0, glow_a(t) / GLOW_SLEEP))))
    sc.fx.append(Wind(ctx, lambda t: 0.95))
    sc.fx.append(Motes(ctx, LYING_GLOW, keyed([(t_sleep, 0.0), (t_sleep + 0.8, 1.0), (t_disc + 0.3, 1.0),
                                                (t_disc + 1.2, 0.0)], "sine")))

    # ---------------- sound
    for nm, g in (("storm_wind", -17), ("waves_storm", -15), ("rain", -19), ("ship_creak", -21)):
        sc.sfx(nm, 0.0, dur=T, gain_db=g, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_sleep - 0.1, gain_db=-17)
    sc.sfx("snore", t_sleep + 0.1, dur=t_disc - t_sleep + 0.4, gain_db=-23, fade_in=0.4, fade_out=0.4, pan=-0.3)
    sc.sfx("footsteps_run", t_a[0], dur=0.7, gain_db=-17, fade_out=0.2, pan=-0.2)
    sc.sfx("cloth", t_a[2], gain_db=-14)
    sc.sfx("cloth", t_m1, gain_db=-15)
    sc.sfx("cloth", t_m2, gain_db=-15)
    sc.sfx("splash", t_drown + 0.05, gain_db=-9, pan=-0.3)
    sc.sfx("cloth", t_up, gain_db=-14)
    return sc
