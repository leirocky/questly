"""Scene 12 — the sling (1 Samuel 17:48-49).

"歌利亚朝大卫走过来。大卫不但没有跑，反而朝着歌利亚跑过去！ 他从口袋里拿出一块石头，放在机弦上，转啊转，转啊转……
嗖！石头飞了出去，正好打中歌利亚的额头。 咚！巨人扑倒在地上，再也起不来了。"

The shared valley (s04_giant.py). Opens on s11's last frame (same camera, poses and clock: a plain dissolve).
  line 0  "歌利亚朝大卫走过来。" the giant strides at the boy, two heavy planted-foot strides (thud, dust, a jolt),
          passing in front of his shield-bearer.  "大卫不但没有跑，" David lays down his staff and stands firm;
          "反而朝着歌利亚跑过去！" he runs at the giant (planted-foot run, dust at his heels) and stops short.
  line 1  "他从口袋里拿出一块石头，" he reaches into his shepherd's bag and holds up a smooth stone (twinkle);
          "放在机弦上，" he loads the sling; "转啊转，转啊转……" the sling whirls round his raised hand, 8 drawings per
          turn, two turns a second, the camera leaning in.
  line 2  "嗖！" he lets fly (sling_release) and the stone flies across the valley on a gentle arc with a whoosh
          trail, the camera following it; "正好打中歌利亚的额头。" — boing: a cartoon impact burst, a pink bump,
          three stars circle his head; he wobbles, dizzy (the stone drops behind him).
  line 3  "咚！" the giant topples forward, pivoting at his toes (fall progress eased in and quantised), and lands face
          down on "咚" — a big dust cloud, the ground shakes, pebbles hop; "再也起不来了。" he lies still, dizzy, with
          stars, while the dust settles.  Calm last frame (s13 starts on it).
"""
import math

from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s04_giant as V
from stories.david.scenes import s11_face as A
from stories.david.scenes.s04_giant import (GY, K, SH, SW, XB, XD, XD2, XG, XG2, Z, Actor, Dust, Sprite, add_hill_actors,
                                            add_valley, clamp, david_rig, david_sprite, f1, giant_sprite,
                                            goliath_rig, goliath_walk_ps, hill_cast, phrase_t, puff_sprite,
                                            run_pose, saul_sprite, scene_clock, shadow_sprite, steps_walk, twinkle)

END_CAM = Cam(1880, 1420, 2350)              # s13 starts here
RUN_A = (XD2 - XD) / (4 * 2 * K)             # four running strides from XD to XD2
FALL_Q = (0.0, 0.1, 0.25, 0.45, 0.7, 1.0)

REACH = C._P(h=10, arms=(("fk", 14, 8), ("fk", -40, -12)), hands=("fist", "fist"), expr="brave", look=(-0.03, 0.06))
SHOW = C._P(h=-6, arms=(("fk", 14, 8), ("fk", 74, 128)), hands=("fist", "fist"), expr="happy", look=(0.03, -0.05))


def stone_in_hand(st):
    W = st["arms"][1][2]
    return PR.stone(W[0] + 4, W[1] + 2, 1.0, seed=2)


def star_svg(r=22):
    pts = []
    for j in range(10):
        rr = r if j % 2 == 0 else r * 0.42
        a = -math.pi / 2 + j * math.pi / 5
        pts.append((r + 6 + rr * math.cos(a), r + 6 + rr * math.sin(a)))
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="#f2c14e" stroke="{V.INK}" stroke-width="3.2" stroke-linejoin="round"/>'


class StarRing:
    """Three cartoon stars circling a head: centre(t) -> (x, y) or None."""

    def __init__(self, centre, rx=80, ry=24, period=1.1):
        self.c, self.rx, self.ry, self.per = centre, rx, ry, period
        self.sp = Sprite(84, 84, 38, 38, wc=0.3, seed=5)
        self.sp.add(star_svg(32))

    def __call__(self, t):
        c = self.c(t)
        if c is None:
            return None
        ims = []
        for k in range(3):
            a = 2 * math.pi * (t / self.per + k / 3)
            s = 0.8 + 0.25 * math.sin(a)
            r = self.sp.place(0, c[0] + self.rx * math.cos(a), c[1] + self.ry * math.sin(a), s, s, 0, 1.0)
            ims.append(r)
        x0 = int(min(p[0] for _, p in ims))
        y0 = int(min(p[1] for _, p in ims))
        can = Image.new("RGBA", (int(2 * self.rx + 130), int(2 * self.ry + 130)), (0, 0, 0, 0))
        for im, (px, py) in ims:
            can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
        return can, (x0, y0)


def burst_svg(x, y, r=70):
    pts = []
    for j in range(16):
        rr = r if j % 2 == 0 else r * 0.5
        a = j * math.pi / 8 + 0.2
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d = "M" + " L".join(f"{f1(px)},{f1(py)}" for px, py in pts) + " Z"
    return V.doc(f'<g filter="url(#wobble-fine)"><path d="{d}" fill="#fff1b8" stroke="{V.INK}" stroke-width="5" '
                 f'stroke-linejoin="round"/><circle cx="{x}" cy="{y}" r="{r * 0.28}" fill="#ffd36a"/></g>')


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2, L3 = ctx.lines[:4]
    toff = scene_clock(ctx.id)
    add_valley(sc, toff)

    # ---------------------------------------------------------------- beats
    c0 = L0.chunks
    t_g0 = max(L0.start + 0.15, 1.15)          # still for the whole dissolve from s11
    g_ff = [t_g0, t_g0 + 0.95, t_g0 + 1.9]
    t_firm = (c0[1].start if len(c0) > 1 else L0.start + 2.4) + 0.05
    t_run = (c0[2].start if len(c0) > 2 else L0.start + 4.0) + 0.1
    d_ff = [t_run + 0.36 * i for i in range(5)]
    t_reach = L1.start + 0.05
    t_show = phrase_t(L1, "拿出", 0.2) + 0.35
    t_load = phrase_t(L1, "放在", 0.5)
    t_spin = (L1.chunks[1].start if len(L1.chunks) > 1 else L1.start + 4.0) - 0.05
    t_rel = L2.start + 0.02
    t_hit = (L2.chunks[1].start if len(L2.chunks) > 1 else L2.start + 2.2) - 0.03
    t_land = L3.start + 0.04
    t_fall0 = t_land - 0.85
    t_hold = t_rel + 0.9

    # ---------------------------------------------------------------- Goliath: two strides, the hit, the fall
    g_walk, g_px = steps_walk(g_ff, XG, V.STEP_G, -1)
    gsp = giant_sprite()
    GW = [gsp.add(goliath_rig(goliath_walk_ps(k), "angry", gsp.ax, gsp.ay, items="stride_a"))
          for k in range(2 * V.WALK_N)]
    a = lambda **kw: gsp.add(C.goliath(gsp.ax, gsp.ay, K, -1, **kw))     # noqa: E731
    gi = dict(angry=a(pose="stand", expr="angry"), surp=a(pose="stand", expr="surprised"),
              dizzy=a(pose="stand", expr="dizzy", bump=True))
    g_sched = [(0, gi["angry"], 0), (g_ff[0], GW[0], 0.5), (g_ff[-1], gi["angry"], 0.8),
               (t_hit - 0.45, gi["surp"], 0.0), (t_hit, gi["dizzy"], 0.0)]

    def g_rot(t):
        if t < t_hit:
            return 0.0
        u = t - t_hit
        jolt = 4.5 * math.exp(-u * 5) * math.cos(u * 18)          # the head snaps back (rotate away from David)
        wob = 2.6 * math.sin(2 * math.pi * u / 0.9) * M.progress(t, t_hit + 0.2, t_hit + 0.8)
        return jolt + wob

    def g_lift(t):
        d = 0.0
        for f in g_ff[1:]:
            u = t - f
            if 0 <= u < 0.3:
                d = max(d, 8 * math.sin(math.pi * u / 0.3))
        return d
    stand_act = Actor(gsp, g_sched, lambda t: (g_px(t), GY), walk=g_walk, rot=g_rot, breathe=0.008, bper=3.6,
                      toff=toff, lift=g_lift, alpha=lambda t: 1.0 if t < t_fall0 else 0.0)
    sc.add_dynamic("goliath", stand_act, z=Z["goliath"])
    fsp = V.person_sprite(1050 * K, 1000 * K, 260 * K, 40, seed=32)
    FI = [fsp.add(C.goliath(fsp.ax, fsp.ay, K, -1, pose="fall", progress=p_, bump=True, expr="dizzy"))
          for p_ in FALL_Q]
    f_lying = fsp.add(C.goliath(fsp.ax, fsp.ay, K, -1, pose="lying", bump=True))

    def fall_frame(t):
        if t >= t_land:
            return f_lying
        u = clamp((t - t_fall0) / (t_land - t_fall0)) ** 2.2
        k = min(range(len(FALL_Q)), key=lambda i: abs(FALL_Q[i] - u))
        if u > 0.0 and k == 0:
            k = 1 if u > 0.04 else 0
        return FI[k]
    sc.add_dynamic("goliath_fall", Actor(fsp, [(0, f_lying, 0), (t_land, f_lying, 0.5)], lambda t: (XG2, GY),
                                         walk=lambda t: fall_frame(t) if t < t_land else None, breathe=0.006,
                                         bper=3.3, toff=toff, alpha=lambda t: 1.0 if t >= t_fall0 else 0.0),
                   z=Z["goliath"])

    # his huge spear falls from his hand and topples backward onto the grass
    hand = C.body_points(C.goliath, XG2, GY, K, -1, pose="stand")["hands"][1]
    sb = (hand[0], GY - 16)
    L_sp = V.C.GOLIATH_SPEAR_LEN * K
    sc.add("spear", V.doc(PR.spear(sb[0] + L_sp / 2, sb[1], K * 1.0, 0, kind="goliath")), z=Z["bearer_back"] - 0.2,
           wc=0.5, motion=lambda t: Tf(alpha=0.0) if t < t_fall0 else Tf(
               rot=-86 + 86 * M.ease("bounce")(clamp((t - t_fall0 - 0.05) / 0.9)), px=sb[0], py=sb[1]))
    head_up = V.C.goliath_head_point(XG2, GY, K, -1, "stand")
    hc = C.body_points(C.goliath, XG2, GY, K, -1, pose="stand")["head"]
    sc.add_dynamic("stars", StarRing(lambda t: (hc[0] + 20 - 6 * g_rot(t), hc[1] - 150) if t_hit + 0.15 <= t < t_fall0
                                     else None, rx=120, ry=30), z=Z["goliath"] + 0.3)
    sc.add("burst", burst_svg(head_up[0], head_up[1]), z=Z["goliath"] + 0.35, wc=0.2,
           motion=lambda t: Tf(alpha=0.0) if not (t_hit <= t < t_hit + 0.32) else
           Tf(sx=0.5 + 1.2 * (t - t_hit) / 0.32, sy=0.5 + 1.2 * (t - t_hit) / 0.32, px=head_up[0], py=head_up[1],
              alpha=1 - ((t - t_hit) / 0.32) ** 2))

    # ---------------------------------------------------------------- the shield-bearer
    bsp = V.bearer_sprite()
    b_st = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand"))
    b_w = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand", expr="worried"))
    b_s = bsp.add(C.shield_bearer(bsp.ax, bsp.ay, K, -1, pose="stand", expr="scared"))
    sc.add_dynamic("bearer", Actor(bsp, [(0, b_st, 0), (t_hit + 0.3, b_w, 0.5), (t_land + 0.1, b_s, 1.0)],
                                   lambda t: (XB, GY), breathe=0.012, bper=2.9, phase=0.3, toff=toff),
                   z=Z["bearer_back"])

    # ---------------------------------------------------------------- David
    d_walk, d_px = steps_walk(d_ff, XD, 2 * RUN_A * K, 1, n_draw=V.RUN_N)
    dsp = david_sprite()
    DR = [dsp.add(david_rig(run_pose(k, RUN_A, V.DAVID_LK), "brave", dsp.ax, dsp.ay)) for k in range(2 * V.RUN_N)]
    b = lambda **kw: dsp.add(C.david(dsp.ax, dsp.ay, K, 1, **kw))       # noqa: E731
    SPIN = [b(pose="sling_spin", phase=k / 8) for k in range(8)]
    di = dict(staff=b(pose="stand", staff=True, expr="brave"), firm=b(pose="stand", expr="brave"),
              reach=dsp.add(david_rig(REACH, "brave", dsp.ax, dsp.ay)),
              show=dsp.add(david_rig(SHOW, "happy", dsp.ax, dsp.ay, front=stone_in_hand)),
              load=b(pose="hold_sling"), rel=b(pose="sling_release"), empty=b(pose="hold_sling", stone=False),
              surp=b(pose="stand", expr="surprised"))
    d_sched = [(0, di["staff"], 0), (t_firm, di["firm"], 0.6), (d_ff[-1], di["firm"], 0.7), (t_reach, di["reach"], 0.5),
               (t_show, di["show"], 0.8), (t_load, di["load"], 0.6), (t_rel, di["rel"], 0.9),
               (t_hold, di["empty"], 0.4), (t_land + 0.12, di["surp"], 1.0)]

    def d_draw(t):
        k = d_walk(t)
        if k is not None:
            return DR[k]
        if t_spin <= t < t_rel:
            return SPIN[int((t - t_spin) * 16) % 8]
        return None
    sc.add_dynamic("david", Actor(dsp, d_sched, lambda t: (d_px(t), GY), walk=d_draw, breathe=0.012, bper=2.6,
                                  toff=toff), z=Z["david"])
    # the staff he lays down
    sx_ = XD + 70 * K
    staff_svg = V.doc(PR.staff(sx_, GY - 4, K, 1))

    def staff_m(t):
        u = M.progress(t, t_firm - 0.05, t_firm + 0.4, "in")
        r = -84 * u + (3 * math.sin(math.pi * clamp((t - t_firm - 0.4) / 0.2)) if t > t_firm + 0.4 else 0)
        return Tf(rot=r, px=sx_, py=GY - 4, alpha=1.0 if t >= t_firm - 0.05 else 0.0)
    sc.add("staff", staff_svg, z=Z["david"] - 0.1, wc=0.5, motion=staff_m)

    # ---------------------------------------------------------------- the stone's flight
    p0 = C.body_points(C.david, XD2, GY, K, 1, pose="sling_release")["hands"][0]
    p1 = head_up
    ctrl = ((p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - 170)

    def stone_at(t):
        u = clamp((t - t_rel) / (t_hit - t_rel))
        u = 0.15 * u + 0.85 * (1 - (1 - u) ** 1.3)
        x = (1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * ctrl[0] + u * u * p1[0]
        y = (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * ctrl[1] + u * u * p1[1]
        return x, y

    def stone_drop(t):          # it drops off his forehead behind him
        u = clamp((t - t_hit) / 0.75)
        x = p1[0] + 110 * u
        y = p1[1] + (GY - 8 - p1[1]) * u * u - 90 * math.sin(math.pi * u) * (1 - u)
        if t > t_hit + 0.75:
            v = clamp((t - t_hit - 0.75) / 0.3)
            x, y = p1[0] + 110 + 30 * v, GY - 8 - 30 * math.sin(math.pi * v)
        return x, y
    ssp = Sprite(80, 70, 40, 52, wc=0.3, seed=7)
    ssp.add(PR.stone(40, 52, 1.2, seed=2))
    sc.add_dynamic("stone", Actor(ssp, [(0, 0, 0)], lambda t: stone_at(t) if t < t_hit else stone_drop(t),
                                  rot=lambda t: (t - t_rel) * 720 if t < t_hit + 1.05 else 0.0, breathe=0,
                                  alpha=lambda t: 1.0 if t >= t_rel else 0.0), z=Z["prop"] + 2)

    def trail(frame, t, view):
        if not (t_rel <= t <= t_hit + 0.05):
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        n = 14
        for i in range(n):
            ta = t - 0.42 * (i + 1) / n
            tb = t - 0.42 * i / n
            if tb < t_rel:
                break
            ta = max(ta, t_rel)
            (xa, ya), (xb, yb) = view.to_out(*stone_at(ta)), view.to_out(*stone_at(tb))
            k = 1 - i / n
            d.line([(xa, ya + 6), (xb, yb + 6)], fill=(255, 246, 215, int(235 * k)), width=max(3, int(34 * k)))
        for j, off in enumerate((-22, 0, 22)):
            ta = t - 0.5
            if ta < t_rel:
                continue
            (xa, ya), (xb, yb) = view.to_out(*stone_at(ta)), view.to_out(*stone_at(t - 0.18))
            d.line([(xa, ya + off + 6), (xb, yb + off + 6)], fill=(110, 80, 55, 170), width=4)
        frame.alpha_composite(ov)
        return frame

    # ---------------------------------------------------------------- dust and shadows
    pev = []
    for i, f in enumerate(g_ff[1:]):
        pev.append((f, XG - V.STEP_G * (i + 1) - V.GOLIATH_A * K, GY + 8, 0.7, -1))
    for i, f in enumerate(d_ff[1:]):
        pev.append((f, XD + 2 * RUN_A * K * (i + 1) + RUN_A * K, GY + 6, 0.32, -1))
    pev.append((d_ff[-1] + 0.05, XD2 + 40, GY + 8, 0.45, 1))
    lie_l, lie_r = XG2 - 874, XG2 - 60
    for j in range(5):
        x = lie_l + (lie_r - lie_l) * (j + 0.5) / 5
        pev.append((t_land + 0.02 * j, x, GY + 14, 1.3 - 0.1 * abs(j - 2), -1 if j < 2 else 1))
    pev.append((t_land + 0.1, lie_l - 40, GY + 10, 1.0, -1))
    pev.append((t_land + 0.1, lie_r + 60, GY + 10, 0.9, 1))
    sc.add_dynamic("dust", Dust(puff_sprite(3), pev, dur=1.6), z=Z["goliath"] + 0.5)
    shp = shadow_sprite()

    def shadows(t):
        parts = [shp.place(1, XB, GY, 1, 1, 0, 1.0), shp.place(2, d_px(t), GY, 1, 1, 0, 1.0)]
        if t < t_fall0:
            parts.append(shp.place(0, g_px(t), GY, 1, 1, 0, 1.0))
        else:
            u = clamp((t - t_fall0) / (t_land - t_fall0))
            parts.append(shp.place(3, XG2, GY, 1, 1, 0, 0.3 + 0.7 * u))
        x0 = int(min(p[0] for _, p in parts))
        x1 = int(max(p[0] + im.size[0] for im, p in parts)) + 2
        y0 = int(min(p[1] for _, p in parts))
        can = Image.new("RGBA", (x1 - x0, 130), (0, 0, 0, 0))
        for im, (px, py) in parts:
            can.alpha_composite(im, (int(round(px - x0)), int(round(py - y0))))
        return can, (x0, y0)
    sc.add_dynamic("shadows", shadows, z=Z["shadow"])

    # pebbles hop when he lands
    def hop(amp, dl):
        def m(t):
            d = 0.0
            for b_, a_ in ((t_land, 1.0), (g_ff[1], 0.35), (g_ff[2], 0.35)):
                u = t - b_ - dl
                if 0 <= u < 0.5:
                    d = min(d, -amp * a_ * abs(math.sin(2 * math.pi * u / 0.5)) * (1 - u / 0.5))
            return Tf(dy=d)
        return m
    for i, pts in enumerate([[(1150, 1985, 14), (1190, 1992, 10)], [(2700, 2010, 15), (2740, 2016, 11)],
                             [(1900, 2050, 16), (1940, 2056, 10), (1870, 2060, 8)]]):
        sc.add(f"pebbles{i}", V.pebbles_svg(pts, 60 + i), z=Z["prop"] + 0.1 * i, wc=0.4, motion=hop(30, 0.02 * i))

    # ---------------------------------------------------------------- the armies hold their breath
    acts = []
    isr = hill_cast("israel", dict(hope=("stand", "happy"), worry=("stand", "worried"),
                                   surp=("stand", "surprised")), seed0=60)
    for j, (x, y, sp, d) in enumerate(isr):
        sched = [(0, d["hope"], 0), (g_ff[1] + 0.1 * j, d["worry"], 0.0),
                 (t_hit + 0.2 + 0.07 * j, d["surp"], 0.6)]
        acts.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), breathe=0.012, bper=2.6 + 0.2 * j, phase=0.13 * j,
                          toff=toff))
    ssp2, sd = saul_sprite(dict(kind=("talk", "kind"), worry=("stand", "worried"), surp=("stand", "surprised")))
    acts.append(Actor(ssp2, [(0, sd["kind"], 0), (g_ff[1], sd["worry"], 0.0), (t_hit + 0.3, sd["surp"], 0.6)],
                      lambda t: (V.SAUL_X, V.ground(V.SAUL_X) + 6), breathe=0.012, bper=3.1, toff=toff))
    phi = hill_cast("philistine", dict(stand=("stand", None), happy=("stand", "smug"), surp=("stand", "surprised"),
                                       scared=("stand", "scared")), seed0=80)
    for j, (x, y, sp, d) in enumerate(phi):
        sched = [(0, d["stand"], 0), (g_ff[0] + 0.1 * j, d["happy"], 0.0), (t_hit + 0.2 + 0.07 * j, d["surp"], 0.6),
                 (t_land + 0.3 + 0.08 * j, d["scared"], 0.8)]
        acts.append(Actor(sp, sched, lambda t, x=x, y=y: (x, y), breathe=0.012, bper=2.7 + 0.2 * j, phase=0.17 * j,
                          toff=toff))
    add_hill_actors(sc, acts)

    # ---------------------------------------------------------------- camera
    start = A.END_CAM
    keys = [(0, start), (t_g0, start), (g_ff[-1], Cam(1860, 1340, 2750)), (t_firm - 0.1, Cam(1860, 1340, 2750)),
            (t_firm + 1.0, Cam(1420, 1480, 2050)), (t_run + 0.1, Cam(1420, 1480, 2050)),
            (d_ff[-1] + 0.4, Cam(1640, 1470, 2200)), (t_reach - 0.3, Cam(1640, 1470, 2200)),
            (t_show + 0.2, Cam(1560, 1590, 1500)), (t_spin, Cam(1560, 1590, 1500)), (t_rel - 0.1, Cam(1560, 1560, 1420)),
            (t_rel + 0.25, Cam(1720, 1500, 1650)), (t_hit - 0.1, Cam(2330, 1330, 1550)),
            (t_fall0 - 0.6, Cam(2340, 1340, 1620)), (t_land + 0.3, Cam(1920, 1400, 2400)), (T - 1.4, END_CAM),
            (T, END_CAM)]
    cam = M.cam_keys(keys, "sine")
    for f in g_ff[1:]:
        cam = M.cam_shake(cam, amp=8, t0=f, t1=f + 0.32, freq=15, seed=4)
    cam = M.cam_shake(cam, amp=5, t0=t_hit, t1=t_hit + 0.3, freq=18, seed=8)
    cam = M.cam_shake(cam, amp=24, t0=t_land, t1=t_land + 0.75, freq=14, seed=9)
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    hand = C.body_points(V.C.david, XD2, GY, K, 1, pose="hold_sling")["head"]
    sc.fx = [twinkle([(t_show + 0.3, XD2 + 70 * K, GY - 240 * K, 50)]), trail,
             V.valley_motes(toff)]
    _ = hand

    # ---------------------------------------------------------------- sound
    sc.sfx("wind_soft", 0, dur=T, gain_db=-18, fade_in=0.8, fade_out=0.8)
    sc.sfx("crowd", 0, dur=T, gain_db=-26, fade_in=0.8, fade_out=0.8)
    for f in g_ff[1:]:
        sc.sfx("thud", f, gain_db=-8, pan=0.3)
    sc.sfx("thud", t_firm + 0.4, gain_db=-20, pan=-0.3)
    sc.sfx("footsteps_run", d_ff[0], dur=d_ff[-1] - d_ff[0] + 0.1, gain_db=-14, pan=-0.2)
    sc.sfx("cloth", t_reach, gain_db=-15)
    sc.sfx("sparkle", t_show + 0.3, gain_db=-16)
    sc.sfx("cloth", t_load, gain_db=-15)
    for k in range(int((t_rel - t_spin) * 2)):
        sc.sfx("whoosh", t_spin + 0.5 * k, gain_db=-20 + k, pan=-0.2)
    sc.sfx("whoosh", t_rel, gain_db=-6, duck_db=-3)
    sc.sfx("pop", t_hit, gain_db=-5, duck_db=-3)
    sc.sfx("thud", t_hit + 0.01, gain_db=-12)
    sc.sfx("sparkle", t_hit + 0.15, gain_db=-14)
    sc.sfx("thud", t_land, gain_db=-1, duck_db=-2)
    sc.sfx("thunder", t_land, gain_db=-16)
    sc.sfx("crowd", t_hit + 0.3, dur=2.0, gain_db=-20, fade_in=0.2, fade_out=0.8)
    V.preload()
    return sc
