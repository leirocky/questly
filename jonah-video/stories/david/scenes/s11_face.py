"""Scene 11 — face to face (1 Samuel 17:41-47).

"歌利亚看见大卫走过来，哈哈大笑。 (歌利亚) 你拿着棍子来找我，把我当成狗吗？过来，我要把你喂给天上的鸟！
(大卫) 你来打我，靠的是刀和枪。我来打你，靠的是万军之耶和华的名！
(大卫) 今天，我要让全世界的人都知道，以色列有一位上帝！打仗的输赢，全在乎上帝！"

The shared valley of s04 (stories/david/scenes/s04_giant.py): Goliath and his shield-bearer stand on the right of
the meadow where s04 left them; both armies watch from their hills.
  line 0  wide: the little shepherd boy (staff, bag) walks in from the left (planted-foot walk); "哈哈大笑" — the
          giant throws his head back and laughs ('ha ha'), the Philistines on their hill laugh along.
  line 1  (Goliath) reverse shot on the giant: "你拿着棍子来找我，把我当成狗吗？" he leans and points down at the boy;
          "过来，我要把你喂给天上的鸟！" spear up, he shouts — the camera tilts up to a few little doves circling in
          the sky (cute, not menacing).
  line 2  (David) on David: he answers bravely ("你来打我，靠的是刀和枪。"), then "万军之耶和华的名" — he points up to
          heaven and a soft golden light falls on him from above (God only as light).
  line 3  (David) a wide two-shot with both armies on their hills ("全世界的人都知道" — the Israelites lean and point);
          "以色列有一位上帝！" he points up again into the light; "打仗的输赢，全在乎上帝！" he lowers his hand and stands
          firm.  The camera settles on the calm two-shot s12 starts from (same camera, same poses; the shared clock
          continues across the dissolve).
"""
import math

from art import characters as C
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s04_giant as V
from stories.david.scenes.s04_giant import (GY, K, SH, SW, XB, XD, XG, Z, Actor, Birds, add_hill_actors, add_valley,
                                            david_rig, david_sprite, david_walk_ps, dove_sprite, hill_cast,
                                            light_motion, light_svg, phrase_t, saul_sprite, scene_clock,
                                            shadow_sprite, steps_walk)

END_CAM = Cam(1900, 1300, 2900)      # the calm two-shot shared with s12's first frame


def goliath_drawings(sp):
    a = lambda **kw: sp.add(C.goliath(sp.ax, sp.ay, K, -1, **kw))     # noqa: E731
    return dict(stand=a(pose="stand"), laugh=a(pose="laugh"), mock=a(pose="mock_point"),
                shout=a(pose="shout", expr="roar"), angry=a(pose="stand", expr="angry"))


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]
    toff = scene_clock(ctx.id)
    add_valley(sc, toff)

    # ---------------------------------------------------------------- beats
    t_laugh = phrase_t(L0, "哈哈大笑", 0.7) - 0.1
    t_mock = L1.start - 0.1
    t_shout = (L1.chunks[1].start if len(L1.chunks) > 1 else L1.start + 4.4) - 0.1
    t_birds = phrase_t(L1, "天上的鸟", 0.75) - 0.6
    t_gstand = L1.end + 0.3
    t_talk = L2.start - 0.1
    t_up = phrase_t(L2, "万军之", 0.6) - 0.1
    t_down = L2.end + 0.1
    t_talk2 = L3.start - 0.05
    t_world = phrase_t(L3, "全世界", 0.15)
    t_up2 = (L3.chunks[1].start if len(L3.chunks) > 1 else L3.start + 5.0) - 0.1
    t_firm = (L3.chunks[2].start if len(L3.chunks) > 2 else L3.start + 8.2) - 0.05
    t_end = L3.end + 0.1
    t_angry = t_up2 + 0.4

    # ---------------------------------------------------------------- David walks in
    n = 10
    ff = [0.6 + 0.42 * i for i in range(n + 1)]
    x0 = XD - n * V.STEP_D
    d_walk, d_px = steps_walk(ff, x0, V.STEP_D, 1)
    dsp = david_sprite()
    DW = [dsp.add(david_rig(david_walk_ps(k), "brave", dsp.ax, dsp.ay, staff=True)) for k in range(2 * V.WALK_N)]
    di = dict(stand=dsp.add(C.david(dsp.ax, dsp.ay, K, 1, pose="stand", staff=True, expr="brave")),
              talk=dsp.add(david_rig(V.TALK_STAFF, "brave", dsp.ax, dsp.ay, staff_far=True)),
              up=dsp.add(david_rig(V.POINT_STAFF, "brave", dsp.ax, dsp.ay, staff=True)),
              look=dsp.add(C.david(dsp.ax, dsp.ay, K, 1, pose="stand", staff=True, expr="puzzled")))
    d_sched = [(0, DW[0], 0), (ff[-1], di["stand"], 0.5), (t_mock + 0.6, di["look"], 0.0),
               (t_gstand - 0.2, di["stand"], 0.0), (t_talk, di["talk"], 0.7), (t_up, di["up"], 0.9),
               (t_down, di["stand"], 0.6), (t_talk2, di["talk"], 0.7), (t_up2, di["up"], 0.9),
               (t_firm, di["talk"], 0.6), (t_end, di["stand"], 0.6)]
    sc.add_dynamic("david", Actor(dsp, d_sched, lambda t: (d_px(t), GY), walk=d_walk, breathe=0.012, bper=2.6,
                                  toff=toff), z=Z["david"])

    # ---------------------------------------------------------------- Goliath and his shield-bearer
    gsp = V.giant_sprite()
    gi = goliath_drawings(gsp)
    g_sched = [(0, gi["stand"], 0), (t_laugh, gi["laugh"], 0.8), (t_mock, gi["mock"], 0.7),
               (t_shout, gi["shout"], 1.0), (t_gstand, gi["stand"], 0.6), (t_angry, gi["angry"], 0.0)]
    sc.add_dynamic("goliath", Actor(gsp, g_sched, lambda t: (XG, GY), breathe=0.008, bper=3.6, toff=toff),
                   z=Z["goliath"])
    bsp = V.bearer_sprite()
    b_st = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand"))
    b_sm = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand", expr="laugh"))
    sc.add_dynamic("bearer", Actor(bsp, [(0, b_st, 0), (t_laugh + 0.2, b_sm, 0.4), (t_shout + 1.5, b_st, 0.0)],
                                   lambda t: (XB, GY), breathe=0.012, bper=2.9, phase=0.3, toff=toff),
                   z=Z["bearer_back"])
    shp = shadow_sprite()
    sc.add_dynamic("shadows", lambda t: _shadows(shp, d_px(t)), z=Z["shadow"])

    # ---------------------------------------------------------------- the armies watch
    acts = []
    isr = hill_cast("israel", dict(worry=("stand", "worried"), stand=("stand", None), point=("point", "surprised"),
                                   hope=("stand", "happy")), seed0=60)
    for j, (x, y, sp, d) in enumerate(isr):
        sched = [(0, d["worry"], 0), (t_up + 0.5 + 0.1 * j, d["stand"], 0.0)]
        if j % 3 == 1:
            sched += [(t_world + 0.3 + 0.15 * j, d["point"], 0.6), (t_firm + 0.4 + 0.1 * j, d["hope"], 0.5)]
        else:
            sched += [(t_up2 + 0.4 + 0.1 * j, d["hope"], 0.5 if j % 2 else 0.0)]
        acts.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), breathe=0.012, bper=2.6 + 0.2 * j, phase=0.13 * j,
                          toff=toff))
    ssp, sd = saul_sprite(dict(worry=("stand", "worried"), surp=("stand", "surprised"), kind=("talk", "kind")))
    acts.append(Actor(ssp, [(0, sd["worry"], 0), (t_up2 + 0.3, sd["surp"], 0.6), (t_end - 0.5, sd["kind"], 0.5)],
                      lambda t: (V.SAUL_X, V.ground(V.SAUL_X) + 6), breathe=0.012, bper=3.1, toff=toff))
    phi = hill_cast("philistine", dict(stand=("stand", None), laugh=("cheer", "laugh"), surp=("stand", "surprised")),
                    seed0=80)
    for j, (x, y, sp, d) in enumerate(phi):
        sched = [(0, d["stand"], 0), (t_laugh + 0.3 + 0.12 * j, d["laugh"], 0.7), (t_gstand + 0.2 + 0.1 * j,
                                                                                    d["stand"], 0.4)]
        if j % 2 == 0:
            sched += [(t_up2 + 0.5 + 0.12 * j, d["surp"], 0.4), (t_end + 0.2 + 0.1 * j, d["stand"], 0.0)]

        def jig(t, j=j):
            u = t - (t_laugh + 0.3 + 0.12 * j)
            return -10 * abs(math.sin(math.pi * u / 0.4)) if 0.15 < u < t_gstand - t_laugh - 0.3 else 0.0
        acts.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), breathe=0.012, bper=2.7 + 0.2 * j, phase=0.17 * j,
                          toff=toff, lift=jig))
    add_hill_actors(sc, acts)

    # ---------------------------------------------------------------- birds in the sky, God's light
    sc.add_dynamic("birds", Birds(dove_sprite(), 4, 2420, 610, 420, 120, t_birds, t_talk + 0.6, period=4.6),
                   z=Z["hills"] + 0.6)
    lx = XD + 10
    sc.add("light", light_svg(lx, 0, GY + 20, 120, 230, "s11l"), z=Z["fx"] - 2, wc=0, blend="screen",
           motion=light_motion([(t_up - 0.1, t_down + 0.6), (t_up2 - 0.1, t_firm + 1.0)]))

    # ---------------------------------------------------------------- camera
    wide = Cam(1950, 1110, 3500)
    walk = Cam(1880, 1230, 3000)
    gol = Cam(2650, 1400, 2000)
    sky = Cam(2560, 1150, 2300)
    dav = Cam(1120, 1540, 1520)
    davup = Cam(1110, 1460, 1640)
    two = Cam(1900, 1150, 3300)
    keys = [(0, wide), (L0.start + 0.3, wide), (t_laugh + 0.2, walk), (t_mock - 0.1, walk), (t_mock + 1.2, gol),
            (t_shout, gol), (t_birds + 1.1, sky), (L1.end + 0.1, sky), (t_talk + 0.3, dav), (t_up - 0.2, dav),
            (t_up + 0.9, davup), (L2.end + 0.1, davup), (t_talk2 + 1.2, two), (t_up2 - 0.6, two),
            (t_up2 + 0.7, davup), (t_firm + 0.2, davup), (t_end + 0.6, END_CAM), (T, END_CAM)]
    sc.camera = M.cam_keys(keys, "sine")

    # ---------------------------------------------------------------- fx
    sc.fx = [FX.sparkles((lx - 200, GY - 520, lx + 200, GY - 120), count=16, t0=t_up + 0.2, t1=t_down + 0.5,
                         size=(8, 18), drift=-14, seed=5),
             FX.sparkles((lx - 200, GY - 520, lx + 200, GY - 120), count=16, t0=t_up2 + 0.2, t1=t_firm + 0.8,
                         size=(8, 18), drift=-14, seed=6),
             FX.motes((0, 300, SW, 1800), count=26, color=(255, 246, 214), size=(3, 6), alpha=80)]

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("crowd", 0, dur=T, gain_db=-25, fade_in=0.8, fade_out=0.8)
    sc.sfx("footsteps", ff[0], dur=ff[-1] - ff[0], gain_db=-19, pan=-0.5)
    sc.sfx("cheer", t_laugh + 0.3, dur=2.6, gain_db=-22, pan=0.6, fade_in=0.3, fade_out=0.8)
    sc.sfx("cloth", t_mock, gain_db=-15, pan=0.4)
    sc.sfx("cloth", t_shout, gain_db=-14, pan=0.4)
    sc.sfx("birds", t_birds, dur=t_talk + 0.6 - t_birds, gain_db=-16, pan=0.2, fade_in=0.5, fade_out=0.6)
    for tt in (t_up, t_up2):
        sc.sfx("chime", tt + 0.1, gain_db=-11)
        sc.sfx("sparkle", tt + 0.3, gain_db=-16)
    sc.sfx("cloth", t_talk, gain_db=-16, pan=-0.4)
    V.preload()
    return sc


def _shadows(shp, dx):
    from PIL import Image
    parts = [shp.place(0, XG, GY, 1, 1, 0, 1.0), shp.place(1, XB, GY, 1, 1, 0, 1.0), shp.place(2, dx, GY, 1, 1, 0, 1.0)]
    x0 = int(min(p[0] for _, p in parts))
    x1 = int(max(p[0] + im.size[0] for im, p in parts)) + 2
    y0 = int(min(p[1] for _, p in parts))
    can = Image.new("RGBA", (x1 - x0, 130), (0, 0, 0, 0))
    for im, (px, py) in parts:
        can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
    return can, (x0, y0)
