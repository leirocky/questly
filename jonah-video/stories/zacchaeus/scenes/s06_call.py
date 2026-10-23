"""Scene 6 - Luke 19:5-6. Jesus comes along the road at the head of the crowd and stops right under the sycamore-fig;
he looks up at Zacchaeus with a warm smile and calls him by name; Zacchaeus nearly falls off the branch, then scrambles
down, overjoyed, and welcomes Jesus.

The same stage, tree and camera as the end of s05_tree (a plain 1 s fade: the first second here is identical to s05's
last second - same layers, seeds, refs, global-clock breathing / sway / clouds / particles, and the procession is one
shared function of s06's narration). The last second matches s07_grumble's first (END_* below).

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's beat();
nothing hard-coded to the take). Times are for the current take:
  0 .. 1.0      the s05 end frame: Zacchaeus peeking out of the leaves; Jesus walking towards the tree, Peter and John
                behind him, the townsfolk following, the people by the road watching
  1.0 .. 2.5    the camera glides left with Jesus; the people gathered at the tree step aside (they part, turn to the
                middle and welcome him)
  '停' 2.70     Jesus stops right under the sitting branch (stand); Zacchaeus's grin turns to surprise
  '抬' 4.07     Jesus looks up with a warm smile (look_up); Zacchaeus shrinks back on the branch, nervous; the twig
                swings back in front of the leaves
  '撒' 7.17     '撒该，快下来！' Jesus raises his hand to him (call_up, warm); the crowd gasps (they look up, hands to
                their cheeks, '!' marks pop); Zacchaeus sits bolt upright, astonished
  '今天' 8.98   the crowd turns to murmur to one another; '家' 10.42 a startled little bob
  '吓' 11.98    ('他吓了一跳。') Zacchaeus jumps so hard he nearly falls off backwards (wobble, rocking), a flurry of
                leaves, the crown shakes (whoosh); the crowd gasps again; the camera pushes in on him
  '耶稣认识我' 13.71  he points at himself; '他还要到我家去' 15.35 a hand on his heart; '家' 16.52 overjoyed
  '他高兴极了' 17.93  both arms up, bouncing on the branch (sparkle)
  '赶快' 19.27  he swings down to hang from the branch (climb_down); '爬' 19.70 slides down the trunk (slide_down, speed
                lines) and lands with a squash, arms up; a happy hop towards Jesus
  '欢欢喜喜' 20.72  a deep welcoming bow, hand on his heart; '接待' 22.04 'come!' - an open hand (host); Jesus smiles
                down at him and nods
  end           calm two-shot (CAM_END6), the crowd watching: s07's first second
"""
import math
import random

from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import beat
from stories.noah.scenes.s01_title import snap
from stories.zacchaeus.scenes.s05_tree import (
    CAM_HANDOFF, CK, CY, FOLLOWERS, H5, K, SP, TREE_CROWD, TWIG_PUSH, W5, XT, XU, YT, YU, ZREF, Z_FX, Z_ZAC, Fig, LeafFall, Track,
    add_ambient, add_right_crowd, add_twig, add_world, breath, bump, cam_path, dk, doc, env, f1, fk, jes_blink, jk,
    procession, squash, tree_crowd_layer, zac_blink, zac_svg, zk)

INK = "#4b3426"

# ---- the end state (s07_grumble starts from exactly this)
ZAC_END_X = 3700
ZAC_END = zk("host", 1, "happy")
JES_END = jk("smile", -1, None, "down")
PETER_END = dk("peter", "stand", -1, "happy")
JOHN_END = dk("john", "stand", -1, "happy")
FOLK_END = [fk(kind, v, "stand", -1, "surprised") for kind, v, *_ in FOLLOWERS]
CAM_END6 = Cam(3800, 716, 1500)
TREE_END = "watch"


def bang_svg(x, y, s=1.0):
    """A little comic '!' (anchor = its foot)."""
    b = (f'<path d="M{f1(x - 6 * s)},{f1(y - 52 * s)} Q{f1(x)},{f1(y - 60 * s)} {f1(x + 7 * s)},{f1(y - 52 * s)} '
         f'L{f1(x + 3 * s)},{f1(y - 16 * s)} L{f1(x - 3 * s)},{f1(y - 16 * s)} Z" fill="#fff3cf" stroke="{INK}" '
         f'stroke-width="{f1(3.2 * s)}" stroke-linejoin="round"/>'
         f'<circle cx="{f1(x)}" cy="{f1(y - 5 * s)}" r="{f1(5.5 * s)}" fill="#fff3cf" stroke="{INK}" '
         f'stroke-width="{f1(3 * s)}"/>')
    return S.g(b, filter="wobble-fine")


def pop_hold(t0, piv, hold=0.9, out=0.3):
    def m(t):
        if t < t0 or t > t0 + hold + out:
            return Tf(alpha=0.0)
        s = 0.3 + 0.7 * M.progress(t, t0, t0 + 0.22, "back")
        a = M.progress(t, t0, t0 + 0.08, "sine") * (1 - M.progress(t, t0 + hold, t0 + hold + out, "sine"))
        return Tf(sx=s, sy=s, px=piv[0], py=piv[1], alpha=a, dy=-6 * M.progress(t, t0, t0 + hold + out, "out"))
    return m


def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(6)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731

    # ---- beats
    t_ting = b(0, "停")
    t_tai = b(0, "抬")
    t_sa = b(1, "撒")
    t_jt = b(1, "今天")
    t_l1e = ctx.lines[1].end
    t_xia = b(2, "吓")
    t_l2e = ctx.lines[2].end
    t_rs = b(3, "耶稣认识我")
    t_hy = b(3, "他还要")
    t_jia = b(3, "家")
    t_gx = b(4, "他高兴极了")
    t_gk = b(4, "赶快")
    t_pa = b(4, "爬")
    t_hh = b(4, "欢欢喜喜")
    t_jd = b(4, "接待")
    t_l4e = ctx.lines[4].end

    # ---- the world (the crown shakes when he nearly falls)
    shake = lambda t: 5.0 * math.sin((t - t_xia) * 38) * env(t, t_xia - 0.05, t_xia + 0.9, 0.06, 0.6)  # noqa: E731
    add_world(sc, g0, leaf_shake=shake)
    add_right_crowd(sc, g0)
    step_t = [1.0 + 0.25 * k for k in range(6)]
    tree_crowd_layer(sc, g0, [(0, "closed")] + [(step_t[k - 1], f"step{k}") for k in range(1, 6)] +
                     [(step_t[5], "open"), (t_sa + 0.04, "gasp"), (t_jt + 0.35, "murmur"), (t_l1e + 0.3, "watch"),
                      (t_xia - 0.02, "gasp"), (t_l2e + 0.45, TREE_END)])

    # ---- the procession (shared with s05) and what happens after the stop
    figs, t_stop = procession(sc, g0, ctx)
    jf = figs["jesus"]
    t_up = snap(t_tai - 0.06)
    jf.cut(t_up, jk("look_up", -1), depth=5)
    t_call = snap(t_sa - 0.1)
    jf.cut(t_call, jk("call_up", -1), depth=6)
    jf.cut(snap(t_l1e + 0.2), jk("look_up", -1, "smile"), depth=5)
    t_down = snap(t_pa + 0.15)
    jf.cut(t_down, jk("stand", -1, "smile", "down"), depth=4)
    t_bow = snap(t_hh + 0.05)
    jf.cut(snap(t_bow + 0.2), JES_END, depth=5)
    jf.mots.append(squash(snap(t_jd + 0.12), K, jf.ref, 5.0))           # a little nod on '接待'
    jf.blinks(jes_blink, 3.2, T - 1.3, rng, avoid=[(t_call - 0.3, t_l1e + 0.3)])
    for name, gasp_pose in (("peter", "wonder"), ("john", "point")):
        df = figs[name]
        v = name
        df.cut(snap(t_sa + 0.15 + (0.1 if name == "john" else 0)), dk(v, gasp_pose, -1, "amazed"), depth=5)
        df.cut(snap(t_l1e + 0.5), dk(v, "stand", -1, "happy"), depth=4)
        df.cut(snap(t_xia + 0.08), dk(v, "wonder", -1, "amazed"), depth=4)
        df.cut(snap(t_l2e + 0.7 + (0.15 if name == "john" else 0)), PETER_END if name == "peter" else JOHN_END, depth=4)
    for j, (kind, v, *_rest) in enumerate(FOLLOWERS):
        ff = figs[f"folk{j}"]
        mod = ("up_hands", "up", "up_point", "up_hands", "up")[j]
        ff.cut(snap(t_sa + 0.06 + 0.05 * j), fk(kind, v, "look" if mod == "up" else "stand", -1, "surprised", 0.0, mod), depth=5)
        ff.cut(snap(t_jt + 0.4 + 0.07 * j), fk(kind, v, "mutter", (1, -1, -1, 1, -1)[j], "surprised"), depth=4)
        ff.cut(snap(t_l1e + 0.35 + 0.05 * j), fk(kind, v, "look", -1, "surprised", 0.0, "up"), depth=4)
        ff.cut(snap(t_xia + 0.02 * j), fk(kind, v, "stand", -1, "surprised", 0.0, "up_hands" if j % 2 == 0 else "up"), depth=4)
        ff.cut(snap(t_l2e + 0.6 + 0.08 * j), FOLK_END[j], depth=4)
    for f_ in figs.values():
        f_.build(sc)

    # ---- Zacchaeus
    sx, sy = SP["sit"]
    zac = Fig("zac", lambda key, i=0: zac_svg(ZREF[0], ZREF[1], K, key), ZREF, Z_ZAC, g0, seed=181)
    zac.track = Track(sx, sy)
    zac.cut(0, zk("peek", 1, "eager"))
    zac.cut(snap(t_ting + 0.02), zk("peek", 1, "surprised"), dip=False)
    t_hide = snap(t_tai + 0.3)
    zac.cut(t_hide, zk("sit_branch", 1, "nervous", mod="sit_down"), depth=6)
    t_named = snap(t_sa + 0.02)
    zac.cut(t_named, zk("sit_branch", 1, "surprised", mod="sit_up"), depth=5)
    zac.mots.append(bump(t_named + 0.02, K, ZREF, 10, 0.22))
    zac.mots.append(bump(b(1, "家") - 0.04, K, ZREF, 6, 0.18))            # '...你家里' - a startled little bob
    # '吓': nearly falls off backwards
    t_wob = snap(t_xia - 0.06)
    zac.cut(t_wob, zk("wobble", 1, "surprised"), dip=False)
    zac.mots.append(bump(t_wob, K, ZREF, 18, 0.3))

    def rock(t):
        u = t - t_wob
        if u < 0 or u > 1.1:
            return Tf()
        return Tf(rot=-11 * math.sin(2 * math.pi * u / 0.5) * math.exp(-u / 0.45))
    zac.mots.append(rock)
    t_grab = snap(max(t_wob + 0.9, t_l2e - 0.1))
    zac.cut(t_grab, zk("sit_branch", 1, "surprised"), depth=6)
    zac.cut(snap(t_rs - 0.05), zk("sit_branch", 1, "surprised", mod="self"), depth=5)
    zac.cut(snap(t_hy - 0.05), zk("sit_branch", 1, "surprised", mod="heart"), depth=5)
    zac.cut(snap(t_jia - 0.1), zk("sit_branch", 1, "overjoyed", mod="heart"), dip=False)
    zac.mots.append(bump(t_jia - 0.08, K, ZREF, 6, 0.2))
    t_ch = snap(t_gx - 0.05)
    zac.cut(t_ch, zk("sit_branch", 1, "overjoyed", mod="sit_cheer"), depth=5)
    for k_ in range(3):
        zac.mots.append(bump(t_ch + 0.12 + 0.36 * k_, K, ZREF, 10, 0.3))
    # '赶快爬下来': hang from the branch, slide down the trunk, land, hop to Jesus
    gx, gy = PR.local_to_stage(XT, YT, K, 1, -22, -458)
    t_hang = snap(t_gk + 0.02)
    zac.cut(t_hang, zk("climb_down", 1, "overjoyed"), dip=False)
    zac.track.to(t_hang, t_hang + 0.22, gx, gy, curve="out")
    slide = SP["slide"]
    t_sl = snap(max(t_pa - 0.05, t_hang + 0.36))
    zac.cut(t_sl, zk("slide_down", 1, "overjoyed"), dip=False)
    zac.track.to(t_sl - 0.001, t_sl, slide[0][0] + 26, slide[0][1])
    zac.track.along(t_sl + 0.01, t_sl + 0.48, slide, lambda u: u * u * (1.6 - 0.6 * u))
    t_land = snap(t_sl + 0.5)
    zac.cut(t_land, zk("cheer", 1, "overjoyed"), depth=11)           # lands with a squash, arms up
    t_hop = snap(max(t_land + 0.3, t_hh - 0.36))
    t_hop1 = snap(t_hop + 0.36)
    zac.track.to(t_hop + 0.02, t_hop1, ZAC_END_X, YT, lift=34 * K)
    t_bw = snap(t_hop1 + 0.02)
    zac.cut(t_bw, zk("bow", 1, "grateful"), depth=8)
    t_host = snap(t_jd - 0.06)
    zac.cut(t_host, ZAC_END, depth=6)
    zac.blinks(zac_blink, 1.4, T - 1.3, rng, avoid=[(t_wob - 0.3, t_grab + 0.3), (t_hang - 0.4, t_bw + 0.3)])
    zac.mots.append(breath(ZREF, g0, 2.6, 0.012))
    zac.build(sc)

    # the twig: pushed aside (as at the end of s05) until he shrinks back, then hangs free
    add_twig(sc, g0, lambda t: -TWIG_PUSH * (1 - M.progress(t, t_hide - 0.05, t_hide + 0.35, "inout"))
             + 4 * math.sin(math.pi * min(1.0, max(0.0, (t - t_hide - 0.35) / 0.5))) * (t > t_hide + 0.35))

    # leaves: the flurry on '吓', a few when he swings down and slides
    sc.fx.append(LeafFall([(t_wob, sx + 10, sy - 120, 9, 120), (t_wob + 0.15, sx + 150, sy - 210, 5, 130),
                           (t_hang + 0.05, gx + 20, gy - 40, 3, 60), (t_sl + 0.1, XT - 60, YT - 260, 2, 40)], seed=13))
    # the gasp: '!' over a few heads
    heads = [(TREE_CROWD[i]["x1"], CY - 352 * CK) for i in (2, 3, 5)]
    heads += [(XU + FOLLOWERS[j][2] + 6, FOLLOWERS[j][4] - 352 * K * 0.97) for j in (0, 1, 3)]
    heads += [(XU + 168 + 8, YU - 6 - 352 * K)]
    for i, (hx, hy) in enumerate(heads):
        t0 = t_sa + 0.06 + 0.05 * (i % 4)
        sc.add(f"bang{i}", doc(bang_svg(hx, hy, 0.95)), z=Z_FX, wc=0, motion=pop_hold(t0, (hx, hy), 0.85))
    for i, (hx, hy) in enumerate(heads[:4]):
        t0 = t_xia + 0.04 + 0.05 * i
        sc.add(f"bangb{i}", doc(bang_svg(hx + 8, hy, 0.9)), z=Z_FX, wc=0, motion=pop_hold(t0, (hx, hy), 0.7))
    # joy: a few sparkles round him on '他高兴极了'
    sc.fx.append(FX.sparkles((sx - 130, sy - 230, sx + 150, sy + 20), count=12, t0=t_ch, t1=t_hang + 0.2, color=(255, 236, 160),
                             size=(7, 13), period=1.0, drift=-14, seed=61))

    add_ambient(sc, g0)

    # ---- camera
    c_two = Cam(3830, 655, 1660)
    c_up = Cam(3820, 612, 1560)
    c_z = Cam(3812, 548, 1270)
    c_down = Cam(3770, 700, 1620)
    sc.camera = cam_path([(0.0, CAM_HANDOFF), (1.0, CAM_HANDOFF), (3.0, c_two), (t_tai - 0.3, c_two), (t_tai + 0.9, c_up),
                          (t_l1e + 0.1, c_up), (t_xia + 0.25, c_z), (t_gx + 0.1, c_z), (t_gk + 0.3, c_down),
                          (t_bw + 0.25, c_down), (min(T - 1.25, t_l4e + 0.2), CAM_END6), (T, CAM_END6)],
                         ["linear", "inout", "linear", "inout", "linear", "inout", "linear", "inout", "linear", "inout",
                          "linear"])

    # ---- sound
    sc.sfx("crowd", 0, dur=T + 0.5, gain_db=-18, fade_in=0.6, fade_out=1.0, pan=0.3)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-23, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("footsteps", 0, dur=t_stop + 0.2, gain_db=-21, fade_in=0.4, fade_out=0.3, pan=0.3)
    sc.sfx("cloth", step_t[0] + 0.1, gain_db=-20, pan=0.3)
    sc.sfx("cloth", t_hide, gain_db=-18)
    sc.sfx("crowd", t_sa + 0.1, dur=1.6, gain_db=-12, fade_in=0.1, fade_out=1.0, pan=0.2)
    sc.sfx("pop", t_sa + 0.08, gain_db=-17)
    sc.sfx("whoosh", t_wob - 0.05, gain_db=-10)
    sc.sfx("cloth", t_wob + 0.05, gain_db=-14)
    sc.sfx("crowd", t_xia + 0.05, dur=1.2, gain_db=-14, fade_in=0.1, fade_out=0.8, pan=0.2)
    sc.sfx("sparkle", t_ch + 0.05, gain_db=-14)
    sc.sfx("cloth", t_hang, gain_db=-15)
    sc.sfx("whoosh", t_sl, gain_db=-15)
    sc.sfx("thud", t_land, gain_db=-12)
    sc.sfx("pop", t_bw, gain_db=-17)
    sc.sfx("chime", t_host + 0.05, gain_db=-16)
    return sc
