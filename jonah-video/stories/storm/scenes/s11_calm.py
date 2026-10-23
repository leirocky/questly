"""Scene 11 - Jesus calms the storm (Mark 4:39): 耶稣醒了，站起来，对着风和海说： / Z 住了吧！静了吧！ /
风立刻停了，湖面变得平平静静的，一点浪也没有了。月亮出来了，星星又亮了。

The shared boat world of s08_storm. Opens on s10's last frame (plain cross-dissolve); ends on the calm moonlit
lake that s12_question opens with. The storm is undone with the props' storm-to-calm recipe: pre-rendered steps
of every 0..1 option (waves 1 -> .5 -> .2 -> .05, wind streaks and rain fading, cloud banks slowing and thinning,
the swell and the lantern settling, the flag stilling), then cross-fades to calm_lake and the night sky.

Beats (voice-measured phrase marks of the take):
  start          close on the stern (= s10's end): Jesus just woken on his elbow, calm, in his warm light.
  '耶稣醒了'      Andrew and James jump back, amazed.
  '站起来'        Jesus stands up on the stern deck (the camera lifts and widens with him).
  '对着风和海说'   he turns to face the wind and the waves and raises his hand, palm out; his red mantle streams
                 in the wind; a warm light round him; the disciples stare up at him.
  Z '住了吧！'     the wind drops at once: the streaks and the rain stop, the clouds slow, the mantle falls still,
                 the waves shrink (1 -> .5); the kerchiefs stop streaming, the trembling stops.
  '静了吧！'      the waves fall flat (.5 -> .05), the boat stops rocking, the flag and the lantern hang still;
                 the camera pulls back; Jesus lowers his hand.
  '风立刻停了'    stillness: the low cloud bank melts away; the disciples, dripping wet, open their hands in wonder
                 (Peter lets go of the mast, John of the rope).
  '湖面变得平平静静的' the grey water turns into the smooth silver calm lake; the water inside the boat lies still.
  '一点浪也没有了' mirror-calm; Simon kneels.
  '月亮出来了'    the storm sky fades into the night: silver-edged clouds part and the moon comes out; its path
                 shines on the lake; the far hills reappear.
  '星星又亮了'    the stars come out one by one and twinkle.
  end            the calm, wide (= s12's first frame).
"""
import math

from art import props as PR
from art import style as S
from engine.motion import Cam, Tf
from engine.scene import Scene

from .s08_storm import (BP, CALM_BOB, CALM_TILT, CREW, DECK_X, DECK_Y, K, MOON, SH, STORM_BOB, STORM_TILT, SW,
                        TREMBLE, Actor, Rain, Rock, Twinkle, Wind, add_boat, add_calm_lake, add_moon,
                        add_night, add_sail, add_storm_lake, add_storm_sky, beat, breath, cam_path, dip, disciple, doc,
                        foot_of, gtime, hop, jesus_body, jitter, keyed, seed_of, snap, storm_body,
                        storm_crew_pose)
from .s10_wake import ANDREW_DX, GLOW_SLEEP, JAMES_DX, LYING_GLOW, add_glow
from .s10_wake import CAM_END as S10_CAM_END

STAND_GLOW = (DECK_X, DECK_Y - 150, 230, 300)      # the warm light round Jesus standing on the stern deck
GLOW_CALM = 0.45
NIGHT_CLOUDS = [   # (cx, cy, w, side): silver-edged clouds over the moon that part at '月亮出来了'
    (MOON[0] - 140, MOON[1] + 40, 540, -1), (MOON[0] - 520, MOON[1] + 140, 620, -1),
    (MOON[0] + 170, MOON[1] + 0, 500, 1), (MOON[0] + 500, MOON[1] + 120, 580, 1),
]
PART = 430.0
CAM_END = Cam(1600, 910, 2440)        # s11's last camera = s12's first (no downscaling at the seam)
# the end state of the calm (s11's last frame = s12's first)
CALM_POSES = {   # name: (pose, facing, expr)
    "andrew": ("wonder", -1, None), "james": ("wonder", -1, None), "thomas": ("wonder", -1, None),
    "peter": ("wonder", -1, None), "john": ("stand", -1, "awed"), "simon": ("kneel", -1, None),
    "philip": ("wonder", -1, None), "bartholomew": ("stand", -1, "awed"), "matthew": ("wonder", -1, None),
    "thaddaeus": ("stand", -1, "awed"), "jamesa": ("stand", -1, "awed"), "judas": ("stand", 1, "awed"),
}


def calm_body(name):
    pose, fc, ex = CALM_POSES[name]
    return disciple(name, pose, expr=ex, wet=True, wind=0.0, facing=fc)


def night_cloud_body(side):
    col = S.mix(PR.NIGHT_COLS[1], "#6a6f9a", 0.5)
    out = ""
    for i, (cx, cy, w, sd) in enumerate(NIGHT_CLOUDS):
        if sd != side:
            continue
        out += S.cloud(cx, cy, w, w * 0.34, fill=col, seed=60 + i, puffs=6, sw=3.4, shade_fill=S.shade(col, -0.2))
        out += (f'<path d="M{cx - w * 0.38:.0f},{cy - w * 0.16:.0f} q{w * 0.3:.0f},{-w * 0.12:.0f} {w * 0.6:.0f},'
                f'{-w * 0.02:.0f}" fill="none" stroke="#e8e6f4" stroke-width="4" stroke-linecap="round" '
                f'opacity="0.75"/>')
    return S.g(out, filter="wobble")


def add_night_clouds(sc, ctx, alpha, part):
    """The parting night clouds (z 2.8): part(t) 0 = over the moon, 1 = parted; a slow film-time drift."""
    for side in (-1, 1):
        def mo(t, side=side):
            g = gtime(ctx, t)
            return Tf(dx=side * PART * part(t) + 7 * math.sin(2 * math.pi * g / 11.0 + side), alpha=alpha(t))
        sc.add(f"nightcloud{side}", doc(night_cloud_body(side)), z=2.8 + 0.01 * side, wc=0.6,
               seed=seed_of(f"nightcloud{side}"), motion=mo)


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration

    t_woke = beat(ctx, 0, "耶稣醒了")
    t_up = beat(ctx, 0, "站起来")
    t_face = beat(ctx, 0, "对着")
    t_zhu = beat(ctx, 1, "住了吧")
    t_jing = beat(ctx, 1, "静了吧")
    t_feng = beat(ctx, 2, "风立刻")
    t_lake = beat(ctx, 2, "湖面")
    t_flat = beat(ctx, 2, "平平静静")
    t_nowave = beat(ctx, 2, "一点浪")
    t_moon = beat(ctx, 2, "月亮")
    t_star = beat(ctx, 2, "星星")
    t_end = ctx.lines[2].end

    t_back = snap(t_woke + 0.5)
    t_sit = snap(t_up - 0.04)                         # rises to sit on the stern seat ...
    t_stand = snap(t_up + 0.42)                       # ... and stands up on the stern deck
    t_cmd = snap(t_face + 0.04)
    t_w1, t_w2 = snap(t_zhu + 0.22), snap(t_zhu + 0.48)
    t_low = snap(t_jing + 0.75)

    # ---------------- camera: the stern -> up with Jesus standing -> wide on the calm
    C10b = S10_CAM_END
    C11a = Cam(1330, 890, 1720)
    C11b = CAM_END                                       # = s12's first camera
    sc.camera = cam_path([(0, C10b), (t_stand - 0.35, C10b), (t_cmd + 0.45, C11a), (t_jing + 0.1, C11a),
                          (t_feng + 1.0, C11b), (T, C11b)])

    # ---------------- the boat settling
    amp = keyed([(0, STORM_TILT), (t_zhu, STORM_TILT), (t_zhu + 0.5, 2.2), (t_jing, 2.2), (t_jing + 1.3, CALM_TILT)])
    bob = keyed([(0, STORM_BOB), (t_zhu, STORM_BOB), (t_zhu + 0.5, 4.5), (t_jing, 4.5), (t_jing + 1.3, CALM_BOB)])
    rock = Rock(ctx, amp, bob)

    # ---------------- sky: storm -> night (moon out, stars back)
    storm_a = keyed([(t_moon - 0.35, 1.0), (t_moon + 0.45, 0.0)], "sine")
    stars = keyed([(t_star - 0.1, 0.0), (t_star + 1.1, 1.0)], "linear")
    add_night(sc, ctx, progress=stars)
    add_moon(sc, halo=keyed([(t_moon + 0.3, 0.0), (t_moon + 1.3, 1.0)], "sine"),
             disc=lambda t: 1.0 if t >= t_moon - 0.05 else 0.0,
             hills=keyed([(t_moon - 0.2, 0.0), (t_moon + 0.7, 1.0)], "sine"))

    def slow(t):                                         # the clouds slow to a drift once the wind stops
        d = 1.4
        u = t - t_zhu
        if u <= 0:
            return 0.0
        if u <= d:
            return 0.8 * u * u / (2 * d)
        return 0.8 * (d / 2 + (u - d))
    add_storm_sky(sc, ctx, storm_a, slow=slow,
                  banks_alpha={"low": keyed([(t_feng, 1.0), (t_feng + 1.2, 0.0)], "sine"),
                               "high": keyed([(t_feng, 1.0), (t_feng + 1.2, 0.55), (t_moon - 0.35, 0.55),
                                              (t_moon + 0.3, 0.0)], "sine")})
    add_night_clouds(sc, ctx, keyed([(t_moon - 0.45, 0.0), (t_moon - 0.08, 1.0), (t_moon + 1.2, 1.0),
                                     (t_moon + 2.0, 0.85)], "sine"),
                     keyed([(t_moon + 0.05, 0.0), (t_moon + 1.15, 1.0)], "inout"))
    sc.fx.append(Twinkle(ctx, keyed([(t_star, 0.0), (t_star + 0.6, 1.0)], "sine"), progress=stars))

    # ---------------- the lake: the waves fall, then the silver calm (the moon's path when it comes out)
    # small steps between the wave sizes (cross-fades between near-identical drawings never ghost)
    levels = [0.05, 0.1, 0.17, 0.25, 0.35, 0.45, 0.55, 0.68, 0.82, 1.0]
    lvl = keyed([(t_zhu + 0.05, 9.0), (t_zhu + 0.45, 5.0), (t_jing, 5.0), (t_jing + 0.75, 0.0)], "out")

    def wave_slow(t):                                    # the rows slow down and stop as the water flattens
        d = 1.8
        u = t - t_jing
        if u <= 0:
            return 0.0
        if u <= d:
            return u * u / (2 * d)
        return d / 2 + (u - d)
    storm_out = keyed([(t_lake, 1.0), (t_lake + 1.1, 0.0)], "sine")
    calm_in = keyed([(t_lake, 0.0), (t_lake + 1.1, 1.0)], "sine")
    moon_in = keyed([(t_moon + 0.35, 0.0), (t_moon + 1.35, 1.0)], "sine")
    add_storm_lake(sc, ctx, levels, lvl, alpha=storm_out, slow=wave_slow, full_back=(0.05, 0.1, 0.17),
                   heave=keyed([(t_jing, 1.0), (t_jing + 1.2, 0.12)], "sine"))
    add_calm_lake(sc, ctx, alpha=lambda t: 1.0 if (t_lake - 0.1 <= t and moon_in(t) < 0.999) else 0.0,
                  front_alpha=lambda t: calm_in(t) * (1.0 - moon_in(t)) if moon_in(t) < 0.999 else 0.0,
                  glow=0.0, name="calm")
    add_calm_lake(sc, ctx, alpha=moon_in, glow=1.0, name="calm_moon", z=4.1,
                  front_alpha=lambda t: moon_in(t) * calm_in(t))

    # ---------------- the boat
    add_boat(sc, ctx, rock, lambda t: 1.0, [0.8], lambda t: 0.0, slosh=lambda t: t < t_jing + 1.0,
             lantern_amp=keyed([(t_zhu, 18.0), (t_jing + 1.2, 1.5)], "sine"))
    add_sail(sc, ctx, rock, [(0, "furled", 3), (t_w1, "furled", 7), (t_low, "furled", 0)])

    # ---------------- Jesus: wakes, stands up, commands the wind and the waves
    lying = Actor(ctx, "jesus", BP["sleep"], rock, z=12.0)
    lying.at(0, jesus_body("wake")).move(breath(ctx, 0.012, 3.6), lambda t: Tf(alpha=0.0 if t >= t_sit else 1.0))
    lying.add(sc)
    sit = Actor(ctx, "jesus_sit", BP["stern_seat"], rock, z=12.0)
    sit.at(0, jesus_body("sit", expr="calm", at=BP["stern_seat"]))
    sit.move(lambda t: Tf(alpha=1.0 if t_sit <= t < t_stand else 0.0),
             hop(t_sit, [(0, {"dy": 14 * K, "sy": 0.93}), (0.15, {"dy": -4 * K, "sy": 1.02}), (0.3, {"dy": 0, "sy": 1})],
                 ["out", "sine"]))
    sit.add(sc)
    up = Actor(ctx, "jesus_up", (DECK_X, DECK_Y), rock, z=12.0)
    up.at(0, jesus_body("stand", expr="calm"))
    up.at(t_cmd, jesus_body("stand_command", wind=1.0, facing=-1))
    up.at(t_w1, jesus_body("stand_command", wind=0.5, facing=-1))
    up.at(t_w2, jesus_body("stand_command", wind=0.0, facing=-1))
    up.at(t_low, jesus_body("stand", expr="kind", facing=-1))
    up.move(lambda t: Tf(alpha=1.0 if t >= t_stand else 0.0),
            hop(t_stand, [(0, {"dy": 26 * K, "sy": 0.9}), (0.16, {"dy": -5 * K, "sy": 1.03}),
                          (0.32, {"dy": 0, "sy": 1.0})], ["out", "sine"]),
            dip(t_cmd, 7.0), dip(t_low, 5.0), breath(ctx, 0.008, 3.4, 0.2))
    up.add(sc)
    add_glow(sc, ctx, rock, "glow_lying", LYING_GLOW, keyed([(t_sit, GLOW_SLEEP), (t_stand + 0.25, 0.0)]))
    add_glow(sc, ctx, rock, "glow_stand", STAND_GLOW,
             keyed([(t_sit, 0.0), (t_stand + 0.4, 0.55), (t_cmd, 0.55), (t_cmd + 0.5, 0.95),
                    (t_jing + 0.8, 0.95), (t_feng + 1.4, GLOW_CALM)], "sine"))

    # ---------------- the crew
    look = {"thomas": 0.0, "matthew": 0.08, "peter": 0.16, "simon": 0.24, "jamesa": 0.32, "thaddaeus": 0.4,
            "judas": 0.48, "john": 0.56}
    final_t = {"andrew": 0.12, "philip": 0.2, "james": 0.28, "bartholomew": 0.36, "thomas": 0.44, "matthew": 0.52,
               "peter": 0.62, "thaddaeus": 0.7, "john": 0.8, "jamesa": 0.9, "judas": 1.0, "simon": 1.1}
    for k, name in enumerate(CREW):
        foot = BP["cling"] if name == "peter" else foot_of(name)
        a = Actor(ctx, name, foot, rock)
        trem_end = 1e9
        tw = snap(t_zhu + 0.3 + 0.05 * (k % 5))           # the wind drops: kerchief tails fall, no more trembling
        tf = snap(t_feng + final_t[name])
        if name == "andrew":
            a.at(0, disciple(name, "wake_shake", expr="amazed", wet=True, wind=1.0, facing=-1, marks=False))
            a.at(t_back, disciple(name, "scared", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.at(tw, disciple(name, "scared", expr="amazed", wet=True, wind=0.0, facing=-1))
            a.move(lambda t: Tf(dx=ANDREW_DX * (1 - keyed([(t_back, 0.0), (t_back + 0.26, 1.0)], "out")(t))),
                   hop(t_back, [(0, {"dy": 0}), (0.13, {"dy": -14 * K}), (0.26, {"dy": 0})], ["out", "in"]))
            trem_end = -1.0
        elif name == "james":
            a.at(0, disciple(name, "shout", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.at(t_back + 0.1, disciple(name, "scared", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.at(tw, disciple(name, "scared", expr="amazed", wet=True, wind=0.0, facing=-1))
            a.move(lambda t: Tf(dx=JAMES_DX * (1 - keyed([(t_back + 0.1, 0.0), (t_back + 0.36, 1.0)], "out")(t))),
                   hop(t_back + 0.1, [(0, {"dy": 0}), (0.13, {"dy": -12 * K}), (0.26, {"dy": 0})], ["out", "in"]))
            trem_end = -1.0
        elif name in ("philip", "bartholomew"):
            a.at(0, disciple(name, "shout", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.at(snap(t_cmd + 0.3), disciple(name, "scared", expr="amazed", wet=True, wind=1.0, facing=-1))
            a.at(tw, disciple(name, "scared", expr="amazed", wet=True, wind=0.0, facing=-1))
            a.move(dip(snap(t_cmd + 0.3), 4.0))
            trem_end = -1.0
        else:
            pose, fc = storm_crew_pose(name)
            at = BP["cling"] if pose == "cling" else None
            sh = 0.25 if pose in ("scared", "cling") else 0.0
            a.at(0, storm_body(name))
            tl = snap(t_cmd + 0.35 + look[name])
            a.at(tl, disciple(name, pose, expr="amazed", shake=sh, wet=True, wind=1.0, facing=fc, at=at))
            a.at(tw, disciple(name, pose, expr="amazed", shake=0.0, wet=True, wind=0.0, facing=fc, at=at))
            a.move(dip(tl, 3.5))
            trem_end = tw
        if name == "simon":                               # stands in awe, then kneels when the lake is mirror-calm
            a.at(tf, disciple(name, "stand", expr="awed", wet=True, wind=0.0, facing=-1))
            a.at(snap(t_nowave + 0.3), calm_body(name))
            a.move(dip(snap(t_nowave + 0.3), 9.0))
        else:
            a.at(tf, calm_body(name))
        a.move(dip(tf, 7.0), dip(tw, 2.5), breath(ctx, 0.007, 3.0 + 0.2 * k, k * 0.13),
               jitter(ctx, -1.0, trem_end, TREMBLE[name], seed=k + 1))
        a.add(sc)

    # ---------------- weather going away
    rain = keyed([(t_zhu + 0.05, 0.62), (t_jing + 0.45, 0.0)], "sine")
    bub = keyed([(t_stand - 0.1, 1.0), (t_stand + 0.25, 0.0)])
    sc.fx.append(Rain(ctx, rain, bubble=(LYING_GLOW, bub)))
    sc.fx.append(Wind(ctx, keyed([(t_zhu, 0.95), (t_zhu + 0.5, 0.0)], "sine")))

    # ---------------- sound
    end_storm = t_jing + 0.9
    for nm, g in (("storm_wind", -17), ("rain", -19)):
        sc.sfx(nm, 0.0, dur=t_zhu + 0.45, gain_db=g, fade_in=0.8, fade_out=0.45)
    sc.sfx("waves_storm", 0.0, dur=end_storm, gain_db=-15, fade_in=0.8, fade_out=1.2)
    sc.sfx("ship_creak", 0.0, dur=end_storm, gain_db=-21, fade_in=0.8, fade_out=1.0)
    sc.sfx("waves_calm", t_jing + 0.3, dur=T - t_jing - 0.3, gain_db=-20, fade_in=1.5, fade_out=0.8)
    sc.sfx("cloth", t_sit, gain_db=-14)
    sc.sfx("cloth", t_stand, gain_db=-13)
    sc.sfx("chime", t_cmd + 0.1, gain_db=-15)
    sc.sfx("whoosh", t_zhu + 0.05, gain_db=-15)
    sc.sfx("chime", t_moon + 0.2, gain_db=-14)
    sc.sfx("sparkle", t_star + 0.1, gain_db=-14)
    sc.sfx("night", t_feng + 0.8, dur=T - t_feng - 0.8, gain_db=-24, fade_in=2.0, fade_out=0.8)
    return sc
