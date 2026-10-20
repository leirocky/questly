"""Scene 13 — the rainbow, God's promise (Genesis 8:21-9:17).

Starts exactly where s12 ends (same world, camera END_CAM and cast; a plain dissolve; idle motion runs on the film's
global clock): the family kneeling round the little altar fire, the animals resting on the meadow, the birds on the
ark's roof, the turtles still crawling down the ramp.

  line 0  G '我要和你们立约：'  God's warm light grows from the upper left, soft white clouds gather in the sky and
          a golden glow falls on the family.
          '我再也不会用大水毁灭大地了。'  the light breathes gently with the words, golden motes drift down.
  line 1  '上帝把一道彩虹放在云彩里。'  the family open their eyes and look up (amazed); the camera draws back to
          the whole sky; a soft glow where the rainbow will be.
          '红、橙、黄、绿、青、蓝、紫，'  the rainbow appears band by band, one per colour word (8 key renders,
          each band fades in with a little sparkle that runs along it from foot to foot).
          '好漂亮啊！'  the family stand up and cheer, Noah points up; the elephant trumpets, the monkeys wave, the
          rabbits hop, the birds take off from the roof and fly through the arc.
  line 2  G '每次看见彩虹，我就会记得我的应许。'  a gentle golden shimmer glides along the rainbow; the family fold
          their hands and look up, thankful; the birds settle on the roof again. Calm last frame (page dip to s14).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.loader import context
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes import s12_out as O
from stories.noah.scenes.s10_inside import stars_fx

INK = P["ink"]
KS = O.KS
RB = (1390, 975, 0.82)          # rainbow centre x, base y, scale
RB_R, RB_BAND = 900, 30
COLORS = "红橙黄绿青蓝紫"


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def band_sweeps_fx(cues, color=(255, 246, 214)):
    """A bright sparkle that runs along rainbow band k from the left foot over the top to the right foot."""
    from PIL import Image, ImageDraw
    rx, ry, s = RB

    def fx(frame, t, view):
        live = [(k, t0) for k, t0 in cues if t0 <= t <= t0 + 0.75]
        if not live:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for k, t0 in live:
            u = clamp((t - t0) / 0.6)
            fade = 1 - clamp((t - t0 - 0.6) / 0.15)
            rr = (RB_R - k * RB_BAND) * s
            for j in range(6):           # the head and a short glittering tail
                uj = u - j * 0.025
                if uj < 0.12 or uj > 0.88:
                    continue
                a = math.pi * (1 - uj)
                x, y = rx + rr * math.cos(a), ry - rr * math.sin(a)
                ox, oy = view.to_out(x, y)
                r = (16 - 2.2 * j) * view.scale
                al = int(235 * fade * (1 - j / 6))
                w = r * 0.22
                d.ellipse([ox - r * 0.6, oy - r * 0.6, ox + r * 0.6, oy + r * 0.6], fill=(*color, al // 4))
                d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                           (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, al))
        frame.alpha_composite(ov)
        return frame
    return fx


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]
    g = O.gtime(ctx)
    ctx12 = context("s12_out")
    O.set_turtle_starts(ctx12)

    # ---------------------------------------------------------------- beats
    t_god = L0.start
    t_look = snap(L1.start + 0.15)
    t_bands = [phrase_t(L1, c) for c in COLORS]
    t_pretty = phrase_t(L1, "好漂亮啊")
    t_prom = L2.start
    t_calm = snap(L2.start + 0.2)

    # ---------------------------------------------------------------- the world (as s12 left it) + the rainbow
    def light_alpha(t):
        up = M.progress(t, t_god - 0.3, t_god + 1.6, "sine")
        down = M.progress(t, L0.end, L0.end + 2.0, "sine")
        up2 = M.progress(t, t_prom - 0.3, t_prom + 1.2, "sine")
        return 0.4 * up * (1 - 0.6 * down) + 0.18 * up2
    O.add_world(sc, g, light_alpha)
    rbf = [doc(PR.rainbow(RB[0], RB[1], RB[2], progress=k / 7, radius=RB_R, band=RB_BAND)) for k in range(8)]

    def rb_fa(t):
        n = sum(1 for tb in t_bands if t >= tb)
        if n == 0:
            return 0.0
        tb = t_bands[n - 1]
        return (n - 1) + clamp((t - tb) / 0.22)
    sc.add("rainbow", rbf, frame_at=rb_fa, z=3.5, wc=0.35,
           motion=lambda t: Tf(alpha=0.94 + 0.06 * math.sin(2 * math.pi * g(t) / 2.2) * M.progress(t, t_prom, t_prom + 1)))
    # a soft glow where the rainbow will be, before the colours come
    pg = S.rad_grad("s13pg", [(0, "#fff6d8", 0.0), (0.82, "#fff2c4", 0.55), (0.9, "#fff2c4", 0.3), (1, "#fff2c4", 0)])
    sc.add("preglow", doc(f'<ellipse cx="{RB[0]}" cy="{RB[1]}" rx="{RB_R * RB[2] * 1.12}" ry="{RB_R * RB[2] * 1.12}" '
                          f'fill="url(#s13pg)"/>', pg), z=3.4, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.8 * M.progress(t, t_look, t_bands[0], "sine") *
                               (1 - M.progress(t, t_bands[0], t_bands[-1] + 0.8))))
    # a golden shimmer gliding along the arc during the promise (rotates about the rainbow's centre)
    rr = RB_R * RB[2]
    arc = (f'<path d="M{RB[0] - rr},{RB[1]} A{rr},{rr} 0 0 1 {RB[0] - rr * math.cos(0.5)},{RB[1] - rr * math.sin(0.5)}" '
           f'fill="none" stroke="#fff6dc" stroke-width="{RB_BAND * RB[2] * 5}" stroke-linecap="round" '
           f'filter="url(#blur-md)"/>')
    sweep_t = [t_prom + 0.2, t_prom + 2.2]

    def shim(t):
        for ts in sweep_t:
            if ts <= t <= ts + 1.8:
                u = (t - ts) / 1.8
                return Tf(rot=180 * u - 10, px=RB[0], py=RB[1], alpha=0.7 * math.sin(math.pi * u))
        return Tf(alpha=0.0)
    sc.add("shimmer", doc(arc), z=3.55, wc=0, blend="screen", motion=shim)
    # soft clouds gather round the rainbow's feet and in the sky ('放在云彩里')
    def cloud_layer(name, spots, z, seed0):
        cl = "".join(S.cloud(x, y, w_, h_, fill="#fffaf0", seed=seed0 + i, puffs=6, sw=3, shade_fill="#f1e6d2")
                     for i, (x, y, w_, h_) in enumerate(spots))
        sc.add(name, doc(S.g(cl, filter="wobble")), z=z, motion=lambda t: Tf(
            dx=-30 + 6 * t, dy=12 * (1 - M.progress(t, t_god, t_god + 3.0, "sine")),
            alpha=M.progress(t, t_god + 0.3, t_god + 3.0, "sine")))
    cloud_layer("soft_clouds", ((1000, 200, 320, 84), (1700, 230, 340, 88)), 2.7, 90)       # behind the bow
    cloud_layer("feet_cloud_r", ((2050, 700, 380, 110),), 3.6, 94)                        # round its feet
    cloud_layer("feet_cloud_l", ((760, 330, 260, 76),), 3.61, 95)
    O.add_ground(sc, g)
    sc.add("ark", O.ark_svg(1.0, 1.0, 0.0), seed=11)

    # ---------------------------------------------------------------- the animals (resting as s12 left them)
    def animal(name, kind, female, extra=(), shadow=200, react=None):
        xr, yr, fr = O.REST[name]
        draw = O.animal_draw(kind, xr, yr, female, shadow=shadow)
        keys = [("stand", fr)] + list(extra)
        frames = [doc(draw(k, f)) for k, f in keys]
        sched = react or [(0, 0)]
        mot = [O.g_breathe(g, (xr, yr), 0.012, 3.0, 0.0)]
        mot += [dip(ts, KS, (xr, yr), 6) for ts, _ in sched if ts > 0]
        sc.add(name, frames, frame_at=cuts(sched), motion=M.combine(*mot), z=20 + yr / 100, wc=0.8)

    animal("elephant_m", "elephant", False, [("trunk_up", -1)], 380,
           react=[(0, 0), (snap(t_pretty + 0.05), 1), (snap(t_prom + 0.4), 0)])
    animal("elephant_f", "elephant", True, [("trunk_up", -1)], 360,
           react=[(0, 0), (snap(t_pretty + 0.35), 1), (snap(t_prom + 0.8), 0)])
    for nm, kind, fem, sh in (("giraffe_m", "giraffe", False, 260), ("giraffe_f", "giraffe", True, 250),
                              ("zebra_m", "zebra", False, 260), ("zebra_f", "zebra", True, 260),
                              ("horse_m", "horse", False, 260), ("horse_f", "horse", True, 260)):
        animal(nm, kind, fem, shadow=sh)
    for k, nm in enumerate(("monkey_m", "monkey_f")):
        animal(nm, "monkey", k == 1, [("wave", -1)], 110,
               react=[(0, 0), (snap(t_pretty + 0.15 + 0.2 * k), 1), (snap(t_prom + 0.2 + 0.3 * k), 0)])
    # the rabbits hop in place for joy
    for k, nm in enumerate(("rabbit_m", "rabbit_f")):
        xr, yr, fr = O.REST[nm]
        draw = O.animal_draw("rabbit", xr, yr, k == 1, shadow=120)
        frames = [doc(draw("stand", fr))] + [doc(draw(f"hop{p}", fr)) for p in (0.0, 0.25, 0.5, 0.75)]
        th0 = snap(t_pretty + 0.1 + 0.15 * k)
        th1 = th0 + 4 * 0.32

        def rfa(t, th0=th0, th1=th1):
            if th0 <= t < th1:
                return 1.0 + int((t - th0) / 0.08) % 4
            return 0.0
        sc.add(nm, frames, frame_at=rfa, z=20 + yr / 100, wc=0.8,
               motion=M.combine(O.g_breathe(g, (xr, yr), 0.012, 3.0, 0.0)))

    # ---------------------------------------------------------------- the family: kneeling -> look up -> stand and
    # cheer -> fold their hands, thankful
    react = {"noah": "point_up:amazed", "noah_wife": "cheer", "shem": "cheer", "daughter_in_law0": "stand:amazed",
             "ham": "cheer", "daughter_in_law1": "cheer", "japheth": "stand:amazed", "daughter_in_law2": "cheer"}
    for k, nm in enumerate(O.FAMILY_ORDER):
        xr, yr, fr = O.REST[nm]
        draw = O.fam_draw(nm, xr, yr)
        keys = ["kneel_pray", "kneel_pray:amazed", react[nm], "pray"]
        frames = [doc(draw(kk, fr)) for kk in keys]
        tl = snap(t_look + 0.06 * k)
        tu = snap(t_pretty + 0.04 + 0.06 * k)
        tp = snap(t_calm + 0.08 * k)
        sched = [(0, 0), (tl, 1), (tu, 2), (tp, 3)]
        sc.add(nm, frames, frame_at=cuts(sched), z=40 + yr / 100, wc=0.8, motion=M.combine(
            O.g_breathe(g, (xr, yr), 0.012, 2.6 + 0.2 * k, 0.13 * k),
            dip(tl, KS, (xr, yr), 4), dip(tu, KS, (xr, yr), 8), dip(tp, KS, (xr, yr), 6),
            hop(tu + 0.3, [(0, {"dy": 0}), (0.16, {"dy": -9 * KS}), (0.32, {"dy": 0}), (0.5, {"dy": -6 * KS}),
                           (0.66, {"dy": 0})], (xr, yr))))

    # ---------------------------------------------------------------- the altar fire, turtles, occluder (as s12)
    ax_, ay_, _ = O.ALTAR
    sc.add("altar", O.altar_frames(), frame_at=O.flicker_fa(g), z=40 + ay_ / 100 - 0.005, wc=0.7)
    fg = S.rad_grad("s12fg", [(0, "#ffd890", 0.9), (0.4, "#f6b860", 0.4), (1, "#f2c14e", 0)])
    sc.add("fire_glow", doc(f'<ellipse cx="{ax_}" cy="{ay_ - 90}" rx="430" ry="330" fill="url(#s12fg)"/>', fg), wc=0,
           blend="screen", z=60, motion=lambda t: Tf(alpha=min(1.0, (0.75 + 0.25 * M.progress(t, t_god, t_god + 1.5, "sine") *
                                                    (1 - 0.6 * M.progress(t, L0.end, L0.end + 1.5)) +
                                                    0.15 * M.progress(t, t_prom, t_prom + 1.2, "sine")) *
                                                   (0.88 + 0.12 * math.sin(2 * math.pi * g(t) / 0.7)))))
    O.turtle_layers(sc, g)
    sc.add("occluder", O.occluder_svg(1.0), z=55, seed=11, wc_edge=0.0)
    # ---------------------------------------------------------------- birds: on the roof, then through the arc, back
    for i, (px, col) in enumerate(O.BIRD_PERCH):
        ey = O.RIDGE_Y - 30 * O.BIRD_S
        t0 = snap(t_pretty - 0.2 + 0.2 * i)
        t1 = t_prom + 2.4 + 0.35 * i
        cx_, cy_ = RB[0], RB[1]
        r_out = (RB_R + 120) * RB[2] - 40 * i
        r_in = (RB_R - 300) * RB[2] + 30 * i

        def pos(t, t0=t0, t1=t1, px=px, ey=ey, i=i, r_out=r_out, r_in=r_in):
            u = clamp((t - t0) / (t1 - t0))
            # up from the roof, an S through the arc (outside it, then under it), and home to the ridge
            a = math.pi * (0.95 - 0.8 * u) if i % 2 == 0 else math.pi * (0.1 + 0.8 * u)
            r = r_out + (r_in - r_out) * (0.5 - 0.5 * math.cos(2 * math.pi * u))
            x, y = cx_ + r * math.cos(a), cy_ - r * math.sin(a)
            w_a = 1 - M.progress(u, 0, 0.18)
            w_b = M.progress(u, 0.8, 1.0)
            x = x * (1 - w_a) + px * w_a
            y = y * (1 - w_a) + ey * w_a
            x = x * (1 - w_b) + px * w_b
            y = y * (1 - w_b) + ey * w_b
            return x, y
        fl_ = {f: O.bird_frames(col, 300, 300, O.BIRD_S, f) for f in (-1, 1)}
        for f in (-1, 1):
            def bm(t, f=f, pos=pos, t0=t0, t1=t1):
                if t < t0 or t >= t1:
                    return Tf(alpha=0.0)
                x, y = pos(t)
                x2, _ = pos(t + 0.04)
                if (1 if x2 >= x else -1) != f:
                    return Tf(alpha=0.0)
                return Tf(dx=x - 300, dy=y - 300)
            sc.add(f"bird{i}_{'l' if f < 0 else 'r'}", fl_[f], z=70, wc=0.3, motion=bm,
                   frame_at=lambda t, t0=t0: float((0, 1, 2, 3, 4, 3, 2, 1)[int((t - t0) / 0.06) % 8]))
        sc.add(f"bird{i}_perch", O.perched_bird(col, px), z=70, wc=0.3, motion=M.combine(
            lambda t, t0=t0, t1=t1: Tf(alpha=0.0 if t0 <= t < t1 else 1.0),
            lambda t, px=px, i=i: Tf(rot=4 * max(0.0, math.sin(2 * math.pi * (g(t) / 2.3 + 0.27 * i))) ** 4,
                                     px=px, py=O.RIDGE_Y)))

    tuf = [O.tufts_svg(p) for p in (0.0, 0.25, 0.5, 0.75)]
    sc.add("tufts", tuf, z=90, frame_at=lambda t: float(round(1.5 + 1.5 * math.sin(2 * math.pi * g(t) / 2.8))))

    # ---------------------------------------------------------------- fx
    sc.fx = [O.g_fx(FX.motes((0, 200, W, 900), count=24, color=(255, 240, 200), size=(3, 6), seed=17, alpha=110), g),
             FX.sparkles((150, 80, 1500, 700), count=18, t0=t_god + 0.4, t1=L0.end + 1.0, size=(7, 15), drift=14,
                         seed=41),
             band_sweeps_fx([(k, tb) for k, tb in enumerate(t_bands)]),
             stars_fx([(RB[0] + (RB_R - k * RB_BAND) * RB[2] * math.cos(math.pi * (0.5 + 0.3 * ((k % 3) - 1))),
                        RB[1] - (RB_R - k * RB_BAND) * RB[2] * math.sin(math.pi * (0.5 + 0.3 * ((k % 3) - 1))),
                        tb + 0.45, 14) for k, tb in enumerate(t_bands)], life=1.6),
             FX.sparkles((300, 120, 1900, 700), count=16, t0=t_prom, t1=T + 2, size=(6, 13), drift=-6, seed=43,
                         period=2.2)]

    # ---------------------------------------------------------------- camera: from s12's framing back to the whole sky
    keys = [(0, O.END_CAM), (t_look - 0.3, O.END_CAM), (t_bands[0] - 0.15, Cam(1080, 600, 2080)),
            (t_prom, Cam(1076, 598, 2090)), (T, Cam(1100, 604, 2000))]
    sc.camera = M.cam_keys(keys, "sine")
    O.fix_seeds(sc)

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T + 0.1, gain_db=-22, fade_in=0.8, fade_out=0.9)
    sc.sfx("wind_soft", 0, dur=T + 0.1, gain_db=-24, fade_in=0.8, fade_out=0.9)
    sc.sfx("fire", 0, dur=T + 0.1, gain_db=-20, fade_in=0.8, fade_out=0.9)
    sc.sfx("chime", t_god + 0.05, gain_db=-12)
    for k, tb in enumerate(t_bands):
        sc.sfx("sparkle", tb, gain_db=-16 - (k % 2), pan=-0.6 + 0.2 * k)
    sc.sfx("chime", t_pretty, gain_db=-13)
    sc.sfx("cheer", t_pretty + 0.05, dur=2.6, gain_db=-15, fade_out=1.0)
    sc.sfx("horn", t_pretty + 0.1, gain_db=-22, pan=0.4)
    sc.sfx("chime", t_prom + 0.2, gain_db=-13)
    return sc
