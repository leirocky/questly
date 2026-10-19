"""Scene 13 — victory (1 Samuel 17:51-52).

"非利士人一看，他们最厉害的勇士倒下了，吓得转身就逃。 以色列人欢呼起来。大家都知道：是上帝帮助了大卫！"

The shared valley (s04_giant.py). Opens on s12's last frame (same camera, poses and clock: a plain dissolve):
Goliath lying face down with his bump and stars, his spear on the grass, David at a safe distance.
  line 0  "非利士人一看，" the camera draws back toward the Philistine hill: the soldiers stare and point;
          "他们最厉害的勇士倒下了，" the shield-bearer drops the champion's great shield (it topples onto the grass);
          "吓得转身就逃。" they all turn and run away over their hill (planted-foot run cycles, a comic scramble), a
          bronze helmet bounces and rolls down the slope, the shield-bearer dashes off behind the big tent.
  line 1  "以色列人欢呼起来。" the camera swings back across the valley: Israel's soldiers cheer and jump, banners are
          raised and wave, King Saul is amazed and then throws up his arms; "大家都知道：是上帝帮助了大卫！" David
          folds his hands and looks up to heaven, thankful, as warm golden light falls on him (God only as light).
          Calm last frame for the page turn.
"""
import math

from art import characters as C
from art import props as PR
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s04_giant as V
from stories.david.scenes import s12_sling as B
from stories.david.scenes.s04_giant import (GY, K, KH, SH, SW, XB, XD, XD2, XG2, Z, Actor, Sprite, add_hill_actors,
                                            add_valley, clamp, david_sprite, hill_cast, light_motion,
                                            light_svg, phrase_t, run_pose, saul_sprite, scene_clock, shadow_sprite)


def runner(sp, side, v, s, facing=1, A=62):
    D, kind = C._soldier_design(side, v)
    D["behind"] = C._shield_on_back(kind)
    return [sp.add(V._out(dict(D), C._ADULT, run_pose(k, A, 1.0, lean=18), "scared", sp.ax, sp.ay, s, facing, "run"))
            for k in range(2 * V.RUN_N)]


def run_fn(t0, x0, step, dt):
    """Running from x0 at t0, one stride per dt s: (drawing k or None, x)."""
    def f(t):
        if t < t0:
            return None, x0
        k = int((t - t0) / dt * V.RUN_N)
        return k % (2 * V.RUN_N), x0 + step * k / V.RUN_N
    return f


def banner_svg(x, y, wave, s=0.5):
    body = PR._flag_pole(0, -420, 0, "#3f6f9e", "#efe2c4", "banner", wave)
    return V.doc(f'<g filter="url(#wobble-fine)" transform="translate({x},{y}) scale({s * 1.25})">{body}</g>')


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[:2]
    toff = scene_clock(ctx.id)
    add_valley(sc, toff)
    c0 = L0.chunks

    # ---------------------------------------------------------------- beats
    t_see = (c0[0].start if c0 else L0.start) + 0.15
    t_drop = (c0[1].start if len(c0) > 1 else L0.start + 1.5) + 0.45
    t_flee = (c0[2].start if len(c0) > 2 else L0.start + 3.8) - 0.1
    t_cheer = L1.start + 0.05
    t_amaze = t_cheer + 0.1
    t_arms = t_cheer + 1.1
    t_pray = (L1.chunks[1].start if len(L1.chunks) > 1 else L1.start + 2.0) + 0.1
    t_light = phrase_t(L1, "是上帝", 0.5) - 0.15

    # ---------------------------------------------------------------- what s12 left on the grass
    fsp = V.person_sprite(1050 * K, 1000 * K, 260 * K, 40, seed=32)
    f_lying = fsp.add(C.goliath(fsp.ax, fsp.ay, K, -1, pose="lying", bump=True))
    sc.add_dynamic("goliath_fall", Actor(fsp, [(0, f_lying, 0)], lambda t: (XG2, GY), breathe=0.006, bper=3.3,
                                         toff=toff), z=Z["goliath"])
    hand = C.body_points(C.goliath, XG2, GY, K, -1, pose="stand")["hands"][1]
    sb = (hand[0], GY - 16)
    L_sp = C.GOLIATH_SPEAR_LEN * K
    sc.add("spear", V.doc(PR.spear(sb[0] + L_sp / 2, sb[1], K, 0, kind="goliath")), z=Z["bearer_back"] - 0.2, wc=0.5)
    sx_ = XD + 70 * K
    sc.add("staff", V.doc(PR.staff(sx_, GY - 4, K, 1)), z=Z["david"] - 0.1, wc=0.5,
           motion=lambda t: Tf(rot=-84, px=sx_, py=GY - 4))
    hp = C.goliath_head_point(XG2, GY, K, -1, "stand")
    ssp = Sprite(80, 70, 40, 52, wc=0.3, seed=7)
    ssp.add(PR.stone(40, 52, 1.2, seed=2))
    sc.add_dynamic("stone", Actor(ssp, [(0, 0, 0)], lambda t: (hp[0] + 140, GY - 8), breathe=0), z=Z["prop"] + 2)
    for i, pts in enumerate([[(1150, 1985, 14), (1190, 1992, 10)], [(2700, 2010, 15), (2740, 2016, 11)],
                             [(1900, 2050, 16), (1940, 2056, 10), (1870, 2060, 8)]]):
        sc.add(f"pebbles{i}", V.pebbles_svg(pts, 60 + i), z=Z["prop"] + 0.1 * i, wc=0.4)

    # ---------------------------------------------------------------- David
    dsp = david_sprite()
    dv = lambda **kw: dsp.add(C.david(dsp.ax, dsp.ay, K, 1, **kw))       # noqa: E731
    di = dict(surp=dv(pose="stand", expr="surprised"), happy=dv(pose="stand", expr="happy"), pray=dv(pose="pray"))
    sc.add_dynamic("david", Actor(dsp, [(0, di["surp"], 0), (t_cheer + 0.4, di["happy"], 0.6), (t_pray, di["pray"], 0.8)],
                                  lambda t: (XD2, GY), breathe=0.012, bper=2.6, toff=toff), z=Z["david"])

    # ---------------------------------------------------------------- the shield-bearer drops the shield and runs
    bsp = V.bearer_sprite()
    b_sc = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand", expr="scared"))
    b_no = bsp.add(C.soldier(bsp.ax, bsp.ay, K, -1, side="philistine", variant=0, pose="stand", spear=False,
                             expr="scared"))
    BR = runner(bsp, "philistine", 0, K, 1, A=70)
    b_run = run_fn(t_flee + 0.15, XB, 2 * 70 * K, 0.3)
    sc.add_dynamic("bearer", Actor(bsp, [(0, b_sc, 0), (t_drop, b_no, 0.8)], lambda t: (b_run(t)[1], GY),
                                   walk=lambda t: None if b_run(t)[0] is None else BR[b_run(t)[0]], breathe=0.012,
                                   bper=2.9, phase=0.3, toff=toff, alpha=lambda t: 1.0 if b_run(t)[1] < 4100 else 0.0),
                   z=Z["bearer_back"])
    shx, shy = XB - 59.5 * K, GY - 149 * K
    sb_x, sb_y = shx, GY - 6

    def shield_m(t):
        u = clamp((t - t_drop) / 0.7)
        r = -84 * M.ease("bounce")(u) if t >= t_drop else 0.0
        return Tf(rot=r, px=sb_x, py=sb_y, alpha=1.0 if t >= t_drop else 0.0)
    sc.add("big_shield", V.doc(PR.tall_shield(shx, shy, 0.69 * K)), z=Z["bearer_back"] + 0.1, wc=0.5, motion=shield_m)

    # ---------------------------------------------------------------- the Philistines flee over their hill
    acts = []
    phi = hill_cast("philistine", dict(scared=("stand", "scared"), point=("point", "scared")), seed0=80)
    for j, (x, y, sp, d) in enumerate(phi):
        v = V.PHIL_MEN[j][1]
        R = runner(sp, "philistine", v, KH, 1)
        f = run_fn(t_flee + 0.11 * (j % 6) + 0.05 * j, x, 2 * 62 * KH, 0.26 + 0.02 * (j % 3))
        dy = y - V.ground(x)
        sched = [(0, d["scared"], 0)]
        if j % 2 == 0:
            sched.append((t_see + 0.08 * j, d["point"], 0.6))

        def pos(t, f=f, dy=dy):
            xx = f(t)[1]
            return xx, V.ground(xx) + dy

        def lift(t, f=f, j=j):
            k = f(t)[0]
            return 0.0 if k is None else -6 * abs(math.sin(math.pi * (k % V.RUN_N) / V.RUN_N))
        acts.append(Actor(sp, sched, pos, walk=lambda t, f=f, R=R: None if f(t)[0] is None else R[f(t)[0]],
                          breathe=0.012, bper=2.7 + 0.2 * j, phase=0.17 * j, toff=toff, lift=lift,
                          alpha=lambda t, f=f: 1.0 if f(t)[1] < SW + 160 else 0.0))
    # a bronze helmet bounces off and rolls down the slope (behind the meadow's rise)
    hsp = Sprite(110, 110, 55, 80, wc=0.4, seed=12)
    hsp.add(PR.helmet_bronze(55, 80, 0.55, -1, crest=False))
    hx0 = 2900
    t_h = t_flee + 0.35

    def helm_pos(t):
        u = clamp((t - t_h) / 2.4)
        x = hx0 - 760 * (1 - (1 - u) ** 1.4)
        y = V.ground(x) + 2 - 50 * abs(math.sin(math.pi * u * 4)) * (1 - u)
        if t < t_h + 0.3:
            v = clamp((t - t_h) / 0.3)
            y -= 60 * math.sin(math.pi * v)
        return x, y
    acts.append(Actor(hsp, [(0, 0, 0)], helm_pos, rot=lambda t: -max(0.0, t - t_h) * 260 % 360, breathe=0,
                      alpha=lambda t: 0.0 if t < t_h else 1 - M.progress(t, t_h + 1.9, t_h + 2.3, "sine")))
    # Israel cheers
    isr = hill_cast("israel", dict(surp=("stand", "surprised"), cheer=("cheer", "happy")), seed0=60)
    for j, (x, y, sp, d) in enumerate(isr):
        tc = t_cheer + 0.06 * j

        def jump(t, tc=tc, j=j):
            u = t - tc - 0.2
            return -16 * abs(math.sin(math.pi * u / (0.42 + 0.03 * (j % 4)))) if u > 0 else 0.0
        acts.append(Actor(sp, [(0, d["surp"], 0), (tc, d["cheer"], 0.9)], lambda t, x=x, y=y: (x, y), breathe=0.012,
                          bper=2.6 + 0.2 * j, phase=0.13 * j, toff=toff, lift=jump))
    ssp2, sd = saul_sprite(dict(surp=("stand", "surprised"), arms=("arms_up", "happy")))
    acts.append(Actor(ssp2, [(0, sd["surp"], 0), (t_amaze, sd["surp"], 0.7), (t_arms, sd["arms"], 0.9)],
                      lambda t: (V.SAUL_X, V.ground(V.SAUL_X) + 6), breathe=0.012, bper=3.1, toff=toff,
                      lift=lambda t: -12 * abs(math.sin(math.pi * (t - t_arms - 0.25) / 0.5)) if t > t_arms + 0.25
                      else 0.0))
    add_hill_actors(sc, acts)
    for i, bx in enumerate((320, 560, 790)):
        by = V.ground(bx) + 2
        frames = [banner_svg(bx, by, w) for w in (0.0, 0.25, 0.5, 0.75)]

        def bm(t, i=i, bx=bx, by=by):
            u = clamp((t - t_cheer - 0.15 * i) / 0.35)
            return Tf(dy=160 * (1 - M.ease("back")(u)), alpha=clamp(u * 3), rot=6 * math.sin(2 * math.pi * t / 1.3 + i),
                      px=bx, py=by + 120)
        sc.add(f"banner{i}", frames, z=Z["hill_men"] - 0.05, wc=0.5, motion=bm,
               frame_at=lambda t, i=i: 1.5 + 1.5 * math.sin(2 * math.pi * (t * 1.4 + 0.3 * i)))

    # ---------------------------------------------------------------- shadows
    shp = shadow_sprite()

    def shadows(t):
        from PIL import Image
        parts = [shp.place(2, XD2, GY, 1, 1, 0, 1.0), shp.place(3, XG2, GY, 1, 1, 0, 1.0)]
        bx_ = clamp_x = min(b_run(t)[1], 4300)
        _ = clamp_x
        parts.append(shp.place(1, bx_, GY, 1, 1, 0, 1.0))
        x0 = int(min(p[0] for _, p in parts))
        x1 = int(max(p[0] + im.size[0] for im, p in parts)) + 2
        y0 = int(min(p[1] for _, p in parts))
        can = Image.new("RGBA", (x1 - x0, 130), (0, 0, 0, 0))
        for im, (px, py) in parts:
            can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
        return can, (x0, y0)
    sc.add_dynamic("shadows", shadows, z=Z["shadow"])

    # ---------------------------------------------------------------- God's light on David
    lx = XD2 + 10
    sc.add("light", light_svg(lx, 0, GY + 20, 140, 260, "s13l"), z=Z["fx"] - 2, wc=0, blend="screen",
           motion=light_motion([(t_light - 0.2, T + 5)], peak=0.65))

    # ---------------------------------------------------------------- camera
    start = B.END_CAM
    phil = Cam(2470, 1160, 2650)
    wide = Cam(1950, 1110, 3500)
    endc = Cam(1265, 1190, 2500)
    keys = [(0, start), (t_see - 0.1, start), (t_drop + 0.4, phil), (t_flee + 1.4, phil), (t_cheer + 0.2, wide),
            (t_pray - 0.2, Cam(1500, 1220, 2900)), (t_light + 1.2, endc), (T, Cam(1230, 1210, 2420))]
    sc.camera = M.cam_keys(keys, "sine")

    # ---------------------------------------------------------------- fx
    sc.fx = [FX.sparkles((lx - 260, GY - 640, lx + 260, GY - 120), count=20, t0=t_light, t1=T + 5, size=(9, 20),
                         drift=-14, seed=13),
             FX.sparkles((60, 520, 1150, 900), count=14, t0=t_cheer + 0.2, t1=T + 5, color=(255, 230, 160),
                         size=(8, 16), drift=-20, seed=17),
             V.valley_motes(toff)]

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("crowd", 0, dur=t_flee + 1.0, gain_db=-20, fade_in=0.6, fade_out=0.8, pan=0.5)
    sc.sfx("thud", t_drop + 0.3, gain_db=-12, pan=0.3)
    sc.sfx("footsteps_run", t_flee + 0.1, dur=3.2, gain_db=-14, pan=0.6, fade_out=1.2)
    sc.sfx("hammer", t_h + 0.3, gain_db=-20, pan=0.5)
    sc.sfx("cheer", t_cheer - 0.1, dur=T - t_cheer + 0.2, gain_db=-12, pan=-0.4, fade_in=0.3, fade_out=0.8)
    sc.sfx("horn", t_cheer + 0.4, gain_db=-17, pan=-0.6)
    sc.sfx("chime", t_light, gain_db=-10)
    sc.sfx("sparkle", t_light + 0.4, gain_db=-15)
    V.preload()
    return sc
