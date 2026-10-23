"""Scene 9 - Luke 15:5. Found! The same rocky slope at night as the end of s08_search (a plain 1 s cross-dissolve: the
first second here is identical to s08's last second - same stage, layers, seeds, camera and global-clock motion).

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers through s08's Beats; nothing
hard-coded to the take). Times are for the current take:
  0 .. 1.0      the s08 end frame: the shepherd stands with his lantern raised high (look_around, determined), the
                cloud half over the moon, the rock at the right edge; the lamb is tucked behind the rock, out of view
  '忽然' 1.01   he freezes (eyes wide)
  '他听见了' 1.82 he cups his ear toward the rock (listen 1.72, the lantern raised; the crook tilts to rest against his
                shoulder in 0.3 s)
  '咩' 2.96 / 3.46  a little bleat bubble floats up from behind the big rock on each 咩 (a soft bleat after them)
  '在一块大石头后面' 4.52  he takes the crook back in hand (4.48, 0.3 s) and hurries to the rock (planted-foot walk), the
                camera pans right and finds the lamb on its far side, curled in the rock's shadow
  '小羊冷得发抖' 6.54  he raises the lantern over it (look_around): the warm light falls on the lamb, trembling
                (scared, a 4-phase jitter with tremble ticks), the shadow lifts
  '找到了' 8.38  a warm burst of lantern light round them (sparkle); his face lights up, the lamb looks up; at 8.68 he
                lets his crook tilt over to lean on the big rock (0.42 s) and takes two steps to the lamb
  '牧羊人一点也没生气' 9.78  he kneels and hugs it, soft and kind (kneel_hug 9.65, tender; the lamb nuzzles, a heart);
                as he goes down he sets the lantern on the ground behind him (0.4 s)
  '欢欢喜喜地' 12.43  he stands up holding the lamb (lift 0 -> 1 from 12.32 to 13.76: from his chest up beside his head);
                at 13.88 it swings up over his head in an arc (0.34 s, whoosh) and on '扛在' 14.22 lands across his
                shoulders (carry_stand, the lamb's eyes happy); meanwhile the cloud slides away and the moon shines out
  14.85         he turns round, stoops and picks up his lantern (15.22, 0.4 s, it rises into his hand), then takes his
                crook from the rock onto his shoulder (15.78, 0.46 s) - exactly how he carries them in s10
  '找到你了' 16.25 (H) he walks off home to the left (16.38) with the lamb on his shoulders, the lamb nuzzling his cheek
                (its head rubs, a heart); '我们回家吧' 17.55
  end           he stops under the bright moon, the lamb nuzzles him: a calm last frame for the page turn into s10
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.lost_sheep.scenes.s08_search import (
    CARRY_FRAMES, CLOUD_V, COVER_X, CROOK_L0, FS, LAMB_HIDE, LIGHT_UP, MOON_C, RGY, RX, SH, SHADE_A, SLOPE_CAM0,
    SLOPE_END_KEY, SW, WGY, X_END, X_LOOK, Beats, Fig, ShoulderLamb, Slope, Track, add_slope_shepherd_extras, add_tufts,
    blink_expr, breath, cam_path, crook_local, doc, env, f1, gfx, lamb_markup, rock_shadow_svg, shep_key, slope_crook,
    slope_lantern, slope_shepherd, snap, tinted, walk_x)

INK = "#4b3426"
X_KNEEL = LAMB_HIDE[0] - 92 * FS          # parable_shepherd(kneel_hug) draws the lamb at +92 (scale 1) in front
Y_KNEEL = LAMB_HIDE[1] + 2 * FS


def bleat_markup(x, y, r=38):
    """A little cream bleat bubble with '咩' and two sound ticks (anchor = its centre)."""
    b = (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fbf4e2" stroke="{INK}" stroke-width="3.4"/>'
         f'<path d="M{f1(x - r * 0.35)},{f1(y + r * 0.85)} l{f1(-r * 0.25)},{f1(r * 0.5)} l{f1(r * 0.55)},{f1(-r * 0.3)} Z" '
         f'fill="#fbf4e2" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
         f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r - 3)}" fill="#fbf4e2"/>'
         f'<text x="{f1(x)}" y="{f1(y + r * 0.36)}" font-family="LXGW WenKai" font-weight="bold" font-size="{f1(r * 1.05)}" '
         f'text-anchor="middle" fill="#7a5a40">咩</text>')
    for k in (1, 2):
        rr = r + 10 * k
        b += (f'<path d="M{f1(x + rr * 0.72)},{f1(y - rr * 0.62)} A{f1(rr)},{f1(rr)} 0 0 1 {f1(x + rr * 0.9)},{f1(y + rr * 0.1)}" '
              f'fill="none" stroke="#f6f1de" stroke-width="4" stroke-linecap="round" opacity="{0.9 - 0.3 * k:.2f}"/>')
    return S.g(b, filter="wobble-fine")


def heart_markup(x, y, r, fill="#ef8f9a"):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.2)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.2)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} "
         f"{f1(x)},{f1(y + r * 0.9)} Z")
    return S.g(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{max(2.5, r * 0.15):.1f}" '
               f'stroke-linejoin="round"/><ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.3)}" '
               f'rx="{f1(r * 0.18)}" ry="{f1(r * 0.12)}" fill="#fbd0c4"/>', filter="wobble-fine")


def float_up(t0, piv, dur=1.4, rise=120, drift=0.0, pop=0.3):
    """Pop in at t0, float up and fade (a bubble or a heart)."""
    def m(t):
        if t < t0 or t > t0 + dur:
            return Tf(alpha=0.0)
        u = (t - t0) / dur
        s = 0.4 + 0.6 * M.progress(t, t0, t0 + pop, "back")
        a = M.progress(t, t0, t0 + 0.2, "sine") * (1 - M.progress(t, t0 + dur * 0.6, t0 + dur, "sine"))
        return Tf(dx=drift * u + 6 * math.sin(2 * math.pi * u * 1.5), dy=-rise * M.progress(t, t0, t0 + dur, "out"),
                  sx=s, sy=s, px=piv[0], py=piv[1], alpha=a)
    return m


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(9)

    # ---- beats
    t_hr = bt.at(0, "忽然")
    t_tj = bt.at(0, "他听见了")
    t_m1 = bt.at(0, "咩")
    t_m2 = bt.at(0, "咩", 3)
    t_m_end = bt.end(0, "咩")
    t_zai = bt.at(1, "在一块大石头后面")
    t_hm = bt.at(1, "后面")
    t_xy = bt.at(1, "小羊冷得发抖")
    t_fd = bt.at(1, "发抖")
    t_zdl = bt.at(1, "找到了")
    t_my = bt.at(2, "牧羊人一点也没生气")
    t_sq_end = bt.end(2, "牧羊人一点也没生气")
    t_hh = bt.at(2, "欢欢喜喜")
    t_kang = bt.at(2, "扛在")
    t_jb = bt.at(2, "肩膀")
    t_kang_end = bt.end(2, "他欢欢喜喜地把小羊扛在肩膀上")
    t_zdn = bt.at(3, "找到你了")
    t_hj = bt.at(3, "我们回家吧")
    t_hj_end = bt.end(3, "我们回家吧")

    # ---- the slope: the cloud over the moon (as at the end of s08) slides away when he lifts the lamb
    t_unc0 = t_hh + 0.1
    uncover = lambda t: M.progress(t, t_unc0, t_unc0 + 2.6, "inout")
    cover = lambda t: 1.0
    dark = lambda t: 1.0
    bright = lambda t: M.progress(t, t_unc0 + 0.5, t_unc0 + 2.8, "inout")

    def cloud_x(t):
        drift = COVER_X + CLOUD_V * (t - 1.0)                 # s08: COVER_X + CLOUD_V * (t - T08)
        return drift - 640 * uncover(t)
    slope = Slope(sc, g0, cover, dark, bright=bright, cloud_x=cloud_x)

    # ---- the lamb (tucked against the rock's far side; out of view at first)
    lamb = Fig("lamb", lambda key: lamb_markup(*key) if key[0] != "none" else "", LAMB_HIDE, 20.0, g0, seed=531,
               loops={("scared", 0.0, "open"): (4, 0.075)})
    lamb.draw = (lambda key, k=None: "" if key[0] == "none" else
                 lamb_markup(key[0], (k or 0) * 0.25 if key[0] == "scared" else key[1], key[2]))
    lamb.cut(0, ("hide", 0.0, "open"))
    lamb.cut(t_m1 - 0.05, ("bleat", 0.3, "open"), dip=False)
    lamb.cut(t_m1 + 0.35, ("hide", 0.0, "open"), dip=False)
    lamb.cut(t_m2 - 0.05, ("bleat", 0.6, "open"), dip=False)
    lamb.cut(t_m2 + 0.35, ("scared", 0.0, "open"), dip=False)
    lamb.cut(t_zdl + 0.05, ("stand", 0.0, "big"), depth=5)
    t_kneel = snap(t_my - 0.12)
    lamb.cut(t_kneel, ("none", 0.0, "open"), dip=False)
    lamb.mots.append(breath(LAMB_HIDE, g0, 2.2, 0.02))
    lamb.build(sc)
    # the rock's shadow over the lamb lifts as the lantern comes near
    shade_a = lambda t: SHADE_A * (1 - 0.85 * M.progress(t, t_hm - 0.2, t_xy + 0.3, "inout"))
    sc.add("sl_rock_shade", rock_shadow_svg(), z=20.5, wc=0, blend="multiply", motion=lambda t: Tf(alpha=shade_a(t)))

    # ---- the shepherd (drawn at s08's reference anchor so the opening second matches pixel for pixel)
    tr = Track(X_END, WGY)
    sh = slope_shepherd(sc, g0, tr)
    sh.cut(0, SLOPE_END_KEY)
    sh.cut(max(t_hr + 0.02, 1.17), shep_key("look_around", 1, "surprised", 0.0), depth=4)
    t_lis = snap(t_tj - 0.1)
    key_lis = shep_key("listen", 1, "worried")
    sh.cut(t_lis, key_lis, depth=6)
    # to the rock
    x_look2 = RX + 60
    t_w0 = snap(t_zai - 0.05)
    t_w1 = t_hm + 0.45
    walk_x(sh, tr, t_w0, t_w1, X_END, x_look2, lambda fr: shep_key(fr, 1, "worried"), y=WGY, start=2)
    t_peer = snap(t_w1 + 0.2)
    sh.cut(t_peer, shep_key("look_around", 1, "worried", 0.0), depth=6)
    # '找到了': his face lights up; he leans his crook on the big rock, two steps to the lamb, and kneels (the lantern
    # is set down behind him as he goes down)
    sh.cut(t_zdl - 0.02, shep_key("look_around", 1, "relieved", 0.0), depth=4)
    t_rel = snap(t_zdl + 0.3)
    x_step = X_KNEEL - 40
    t_s0 = snap(max(t_zdl + 0.78, t_rel + 0.45))
    walk_x(sh, tr, t_s0, t_kneel - 0.18, x_look2, x_step, lambda fr: shep_key(fr, 1, "happy"), y=WGY, start=0)
    tr.to(t_kneel - 0.1, t_kneel + 0.12, X_KNEEL, Y_KNEEL, None)
    key_hug = shep_key("kneel_hug", 1, "tender")
    sh.cut(t_kneel, key_hug, depth=10)
    # '欢欢喜喜': up with the lamb (lift 0 -> 1), it swings over onto his shoulders on '扛在'
    t_up = snap(t_hh - 0.12)
    tr.to(t_up - 0.06, t_up + 0.1, X_KNEEL - 20, WGY, None)
    n_lift = 8
    t_l0, t_l1 = t_up + 0.25, max(t_up + 1.35, t_kang - 0.5)
    sh.cut(t_up, shep_key("lift", 1, "joyful", 0.0), depth=10)
    for i in range(1, n_lift + 1):
        sh.cut(t_l0 + (t_l1 - t_l0) * i / n_lift, shep_key("lift", 1, "joyful", i / n_lift), dip=False)
    t_on = max(snap(t_kang - 0.05), snap(t_l1 + 0.42))
    t_sw = snap(t_on - 0.34)                          # the swing: the lamb leaves his raised hands ...
    key_sw = shep_key("lift", 1, "joyful", 1.0, lamb=False)
    sh.cut(t_sw, key_sw, depth=4)
    key_cs = shep_key("carry_stand", 1, "joyful", lamb=False)
    sh.cut(t_on, key_cs, depth=9)                     # ... and lands across his shoulders
    # he turns round, stoops for his lantern, takes his crook from the rock - then home
    t_tn = snap(t_on + 0.62)
    key_cs2 = shep_key("carry_stand", -1, "joyful", lamb=False)
    sh.cut(t_tn, key_cs2, depth=6)
    t_pl = snap(t_tn + 0.36)                          # lantern pick-up (a stoop), into his hand at t_pl + 0.4
    sh.dips.append((snap(t_pl + 0.12), 14.0))
    sh.dips.append((snap(t_pl + 0.4), 6.0))
    t_pc = snap(t_pl + 0.56)                          # crook from the rock to his shoulder
    t_turn = snap(max(t_zdn + 0.04, t_pc + 0.6))
    x_home = X_KNEEL - 470
    t_stop = min(T - 1.0, t_hj_end + 0.5)
    walk_x(sh, tr, t_turn, t_stop - 0.22, X_KNEEL - 20, x_home, lambda fr: shep_key(fr, -1, "joyful", lamb=False),
           y=WGY, start=2, frames=CARRY_FRAMES)
    key_end = shep_key("carry_stand", -1, "joyful", lamb=False)
    sh.cut(t_stop, key_end, depth=4)
    # blinks (none in the first 1.3 s: the dissolve from s08 must match)
    sh.blinks({SLOPE_END_KEY: shep_key("look_around", 1, blink_expr("determined"), 0.0),
               key_lis: shep_key("listen", 1, blink_expr("worried")),
               key_hug: shep_key("kneel_hug", 1, blink_expr("tender")),
               key_end: shep_key("carry_stand", -1, blink_expr("joyful"), lamb=False)}, 1.3, T - 0.2, rng)
    sh.mots.append(breath((X_LOOK, WGY), g0, 3.0, 0.012))

    # ---- his crook and lantern (no prop ever pops; see s08 Prop)
    lean = ("key", lambda key: crook_local(key, "lean")[:2])
    near = ("key", lambda key: crook_local(key, "near")[:2])
    crk = slope_crook(sh, g0, curl=1)
    crk.at(0, "fig")
    crk.at(t_lis, lean, dur=0.3, layer="back")               # cupping his ear: the crook rests against his shoulder
    crk.at(t_w0, near, dur=0.3, layer="back", lift=6)        # walking on: back into his hand
    crk.at(t_w0 + 0.3, "fig")
    # leaning on the big rock: it tilts over from his hand (foot where his hand held it)
    rf = (x_look2 + (crook_local(shep_key("look_around", 1, "relieved", 0.0), "near")[0][0]) * FS, WGY - 4 * FS)
    rl = CROOK_L0 * FS
    rt = (rf[0] - math.sin(math.radians(24)) * rl, rf[1] - math.cos(math.radians(24)) * rl)
    crk.at(t_rel, ("stage", (rf, rt)), dur=0.42, layer="back")
    crk.at(t_pc, lean, dur=0.46, layer="back", lift=14)      # picked up: over his shoulder for the way home
    lan = slope_lantern(sh, g0)
    lan.at(0, "fig")
    gl = (X_KNEEL - 92 * FS, Y_KNEEL - 58 * FS)              # set down behind him as he kneels
    lan.at(t_kneel, ("stage", (gl[0], gl[1], 1.0)), dur=0.4, layer="back", lift=10)
    lan.at(t_pl, "fig", dur=0.4, layer="front", lift=8)      # and picked up again
    crk.apply(sh)
    lan.apply(sh)

    # the lamb on his shoulders as separate parts: it nuzzles his cheek (little pulses) with a heart now and then
    t_nz = [t_on + 0.3, t_pc + 0.6, t_hj + 0.2, t_stop + 0.25]
    sl = ShoulderLamb(sh, FS, g0, 30.5, 561, nuzzle_t=t_nz)
    sl.finish(sc)
    crk.build(sc)
    lan.build(sc)
    add_slope_shepherd_extras(sc, sh, g0, lan, extra=lambda t: 1 + LIGHT_UP * (1 - M.progress(t, t_zai, t_zai + 1.5, "sine"))
                              + 0.22 * env(t, t_zdl - 0.1, t_kneel + 0.6, 0.25, 0.9))
    for i, tn in enumerate(t_nz[1:]):
        h_t = tn + 0.2
        hx, hy = sl.head_point(h_t)
        p0 = sh.point(h_t, (X_LOOK, WGY))
        follow = lambda t, p0=p0: (lambda p: Tf(dx=p[0] - p0[0], dy=p[1] - p0[1]))(sh.point(t, (X_LOOK, WGY), ground=True))
        sc.add(f"heart{i}", doc(heart_markup(hx, hy, 17)), z=31.0, wc=0,
               motion=M.combine(float_up(h_t, (hx, hy), 1.4, 110), follow))

    # the swing: the lamb (held) flies from his raised hands up and over onto his shoulders
    bp = C.body_points(C.parable_shepherd, X_LOOK, WGY, FS, 1, pose="lift", phase=1.0, lamb=False)
    (w0x, w0y), (w1x, w1y) = bp["hands"]
    c0 = ((w0x + w1x) / 2 + 4 * FS, (w0y + w1y) / 2 + 4 * FS)        # where parable_shepherd draws the held lamb
    ca = sl.anchor(key_cs)
    c1 = (ca[0] + 8 * 1.1 * FS, ca[1] - 26 * 1.1 * FS)              # the middle of the lamb draped on his shoulders
    held = doc(tinted(PR.little_lamb(c0[0], c0[1], FS, 1, pose="held", eyes="open")))

    def swing(t):
        if not (t_sw <= t < t_on):
            return Tf(alpha=0.0)
        u = M.progress(t, t_sw, t_on, "inout")
        a = sh.full_point(t, c0)
        b = sh.full_point(t, c1)
        x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - 46 * FS * math.sin(math.pi * u)
        k = 1 + 0.1 * u
        return Tf(dx=x - c0[0], dy=y - c0[1], rot=-18 * math.sin(math.pi * u), sx=k, sy=k, px=c0[0], py=c0[1])
    sc.add("lamb_swing", held, z=29.95, seed=571, motion=swing)   # behind his raised arms, like the held lamb

    # the heart over the hug
    hx, hy = LAMB_HIDE[0] + 10, LAMB_HIDE[1] - 160 * FS
    sc.add("heart_hug", doc(heart_markup(hx, hy, 20)), z=31.0, wc=0, motion=float_up(t_kneel + 0.9, (hx, hy), 1.6, 120))

    # ---- the bleats from behind the rock
    for i, tm in enumerate((t_m1, t_m2)):
        bx, by = RX - 10 + 40 * i, RGY - 70
        sc.add(f"bleat{i}", doc(bleat_markup(bx, by)), z=18.9, wc=0,
               motion=float_up(tm - 0.05, (bx, by), 1.5, 290 + 20 * i, drift=-50 - 20 * i, pop=0.25))

    # ---- '找到了': a warm burst of lantern light
    bx, by = (X_KNEEL + LAMB_HIDE[0]) / 2 - 60, WGY - 150
    gid = "s9burst"
    defs = S.rad_grad(gid, [(0, "#fff4cf", 0.95), (0.3, "#ffd88a", 0.55), (0.7, "#f6b450", 0.15), (1, "#f6b450", 0)])
    sc.add("burst", doc(f'<ellipse cx="{f1(bx)}" cy="{f1(by)}" rx="520" ry="440" fill="url(#{gid})"/>', defs), z=39.5,
           wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.5 * env(t, t_zdl - 0.05, t_kneel + 1.2, 0.2, 1.4),
                               sx=0.5 + 0.6 * M.progress(t, t_zdl - 0.05, t_zdl + 0.7, "out"),
                               sy=0.5 + 0.6 * M.progress(t, t_zdl - 0.05, t_zdl + 0.7, "out"), px=bx, py=by))
    sc.fx.append(gfx(FX.sparkles, g0, t0=t_zdl, t1=t_kneel + 1.4, rect=(bx - 380, by - 300, bx + 380, by + 120),
                     count=16, color=(255, 232, 170), size=(7, 14), period=1.3, drift=-18, seed=91))
    # the moon shining out: a few silver twinkles round it
    mx, my = MOON_C
    sc.fx.append(gfx(FX.sparkles, g0, t0=t_unc0 + 1.2, t1=T + 2, rect=(mx - 420, my - 260, mx + 420, my + 200),
                     count=10, color=(236, 240, 255), size=(6, 11), period=2.2, drift=0, seed=93))
    sc.fx.append(gfx(FX.motes, g0, rect=(200, RGY - 260, SW - 200, SH - 120), count=16, color=(255, 222, 140),
                     size=(3, 6), seed=71, alpha=150))

    slope.add_front(z_rock=19.0, z_bush_back=25.0, z_bush_front=35.0)
    add_tufts(sc, "sl_tufts_near", g0, (-40, SH - 70, SW + 40, SH - 10), 30, 63, 36.0)

    # ---- camera
    cam_find = Cam(RX - 60, 770, 1480)
    cam_hug = Cam(RX + 40, 790, 1340)
    cam_moon = Cam(RX - 120, 690, 1720)
    cam_end = Cam(x_home + 150, 735, 1520)
    sc.camera = cam_path([(0.0, SLOPE_CAM0), (1.0, SLOPE_CAM0), (t_zai - 0.1, SLOPE_CAM0), (t_xy + 0.2, cam_find),
                          (t_zdl, cam_find), (t_kneel + 0.6, cam_hug), (t_up + 0.3, cam_hug), (t_kang_end, cam_moon),
                          (t_zdn, cam_moon), (t_stop + 0.4, cam_end), (T, cam_end)],
                         ["linear", "linear", "inout", "linear", "sine", "linear", "inout", "linear", "inout", "linear"])

    # ---- sound
    sc.sfx("night", 0, dur=T + 0.5, gain_db=-17, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("sheep", t_m_end + 0.1, gain_db=-17, pan=0.6, pitch=1.25)
    sc.sfx("footsteps", t_w0, dur=t_w1 - t_w0, gain_db=-21, pan=0.2)
    sc.sfx("sparkle", t_zdl, gain_db=-14, pan=0.3)
    sc.sfx("footsteps", t_s0, dur=t_kneel - t_s0, gain_db=-22, pan=0.3)
    sc.sfx("cloth", t_kneel - 0.05, gain_db=-17, pan=0.3)
    sc.sfx("sheep", t_kneel + 0.9, gain_db=-21, pan=0.3, pitch=1.3)
    sc.sfx("cloth", t_rel + 0.1, gain_db=-23, pan=0.2)
    sc.sfx("thud", t_rel + 0.4, gain_db=-26, pan=0.1)
    sc.sfx("thud", t_kneel + 0.38, gain_db=-27, pan=0.2)
    sc.sfx("cloth", t_up, gain_db=-18, pan=0.3)
    sc.sfx("whoosh", t_sw, gain_db=-22, pan=0.2)
    sc.sfx("cloth", t_on, gain_db=-18, pan=0.2)
    sc.sfx("cloth", t_pl + 0.05, gain_db=-21, pan=0.1)
    sc.sfx("cloth", t_pc + 0.1, gain_db=-21, pan=0.0)
    sc.sfx("sparkle", t_unc0 + 0.9, gain_db=-19, pan=-0.2)
    sc.sfx("footsteps", t_turn, dur=t_stop - t_turn, gain_db=-22, pan=0.0)
    return sc
