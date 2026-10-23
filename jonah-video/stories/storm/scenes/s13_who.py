"""Scene 13 - Mark 4:41. On the calm, moonlit lake the wet disciples look at Jesus, who sits quietly at the stern,
and at each other: amazed, then reverent (a few kneel), then whispering in pairs, '这到底是谁？连风和海都听他的话！'.
On line 3 they all turn to him; Jesus lifts his eyes and smiles at them in a soft warm glow; the boat drifts on
through the night and the sky slowly lightens to dawn - the lantern goes out, their clothes dry - so that the last
second is exactly s14's first (a plain cross-dissolve: same dawn lake, boat, crew, glow and camera).

Built on s14_arrive's shared geometry (stage, boat path, crew spots, layer seeds): the boat, the crew and Jesus are
drawn in s14's landed coordinates and moved with boat_motion(u) where u = t - (duration - 1) is s14's clock.

Beats (syllable onsets measured in the voice clip, see s03_friends.Beats):
  0 .. 1.6     calm moonlit page (after the page dip): stars twinkle, the moon's path shimmers, the lantern glows,
               the wet disciples stand looking at Jesus; he sits quietly at the stern
  '惊讶'        a ripple of amazement: one after another they lift their hands in wonder (squash-dip pose cuts)
  '敬畏'        three of them kneel before him
  '彼此说'      the others turn to each other in pairs; the camera has eased in on the crew
  M line       '这到底是谁？' one of each pair whispers, the other listens wide-eyed; on '连风和海' they swap
  '这一天'      everyone turns back to Jesus (staggered cuts); the kneelers rise on '门徒们'
  '耶稣'        Jesus looks up and smiles at them; a soft warm glow blooms round him (chime, sparkles); the camera
               draws back and the night lightens into dawn (moon and stars fade, the lantern goes out, the clothes and
               the boat dry), the boat drifting on toward the far shore
  last 1 s     identical to s14's first second (dissolve)
"""
import math

from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from art import props as PR
from stories.noah.scenes.s01_title import cuts, snap
from stories.storm.scenes.s03_friends import Beats, blink, disc, jes
from stories.storm.scenes import s14_arrive as A

MOON = (1500, 282)


def night_sky_svg(tw):
    return A.doc(PR.night_sky(-20, -60, A.WS + 20, A.YF2 + 8, moon=MOON, moon_r=50, stars=70, progress=1.0,
                              twinkle=tw, clouds=0.0, seed=13))


def night_hills_svg():
    return A.doc(PR.lake_galilee(-20, A.WS + 20, A.LY2, A.LS2, time="night", part="back", sky=False, boats=False,
                                 top=-60))


def night_water_svg(ph):
    return A.doc(PR.calm_lake(-20, A.WS + 20, A.YF2 + 2, phase=ph, moon_x=MOON[0], time="night", scale=0.62,
                              sparkle=0.8, seed=7, bottom=A.HS + 60, glow=1.0))


def build(ctx):
    sc = Scene(ctx, W=A.WS, H=A.HS)
    T = ctx.duration
    B = Beats(ctx)
    toff = -(T - 1.0)
    U = lambda t: t + toff                                       # noqa: E731  s14's clock
    bm = A.boat_motion(U)
    bx = lambda t: A.boat_x(U(t))                                # noqa: E731

    t_jingya = B.at(0, "惊讶")
    t_jingwei = B.at(0, "敬畏", 1)
    t_bici = B.at(0, "彼此说")
    t_lian = B.at(1, "连风和海")
    t_l3 = ctx.lines[2].start
    t_mentu = B.at(2, "门徒们才知道")
    t_jesus = B.at(2, "耶稣不只是")
    t_x = T - 1.0                                                # the dissolve starts here (u = 0)
    t_dawn0, t_dawn1 = snap(t_jesus - 0.4), snap(t_x - 0.35)
    t_dry0, t_dry1 = snap(t_jesus + 0.4), snap(t_x - 0.45)
    night_a = lambda t: Tf(alpha=1 - M.progress(t, t_dawn0, t_dawn1, "sine"))   # noqa: E731

    # ------------------------------------------------------------ backdrop: dawn underneath, night on top
    A.add_dawn_backdrop(sc, toff=toff, z0=0.0)
    tw = [night_sky_svg(p) for p in (0.0, 0.33, 0.66)]
    sc.add("n_sky", tw + [tw[0]], z=1.0, wc=0.8, seed=1301, frame_at=lambda t: (t / 1.1) % 3.0, motion=night_a)
    sc.add("n_hills", night_hills_svg(), z=1.1, wc=0.8, seed=1302, motion=night_a)
    wv = [night_water_svg(p) for p in (0.0, 0.33, 0.66)]
    sc.add("n_water", wv + [wv[0]], z=1.2, wc=0.9, seed=1303, frame_at=lambda t: (t / 1.3) % 3.0, motion=night_a)
    sc.fx.append(FX.vignette(lambda t: 0.45 * (1 - M.progress(t, t_dawn0, t_dawn1 - 0.5, "sine")), color=(18, 22, 48)))

    # ------------------------------------------------------------ the boat (wet at night, dry by dawn)
    dry = lambda t: M.progress(t, t_dry0, t_dry1, "sine")       # noqa: E731
    sc.add("boat_back", [A.boat_back_svg(True), A.boat_back_svg(False)], z=2, seed=A.SEED["boat_back"],
           frame_at=dry, motion=bm)
    sc.add("furled", A.furled_svg(), z=2.1, motion=bm, seed=A.SEED["furled"])
    sc.add("boat_front", [A.boat_front_svg(True), A.boat_front_svg(False)], z=6, seed=A.SEED["boat_front"],
           frame_at=dry, motion=bm)
    t_lamp0, t_lamp1 = snap(t_jesus + 0.7), snap(t_x - 0.6)
    sc.add("lantern", [A.lantern_svg(True), A.lantern_svg(False)], z=6.1, seed=A.SEED["lantern"],
           frame_at=lambda t: M.progress(t, t_lamp0, t_lamp1, "sine"), motion=bm)
    sc.add("band", A.band_svg("dawn"), z=6.5, wc=0.9, wc_edge=0.0, seed=A.SEED["water"])
    sc.add("n_band", A.band_svg("night"), z=6.52, wc=0.9, wc_edge=0.0, seed=1303, motion=night_a)
    sc.add("wline", A.waterline_svg(), z=6.6, wc=0, seed=A.SEED["wline"], motion=bm)

    # ------------------------------------------------------------ the crew
    members = A.crew_members()
    order = sorted(members, key=lambda m: -m[2])               # s14's plan order (z and breathing phase)
    idx_of = {m[0]: i for i, m in enumerate(order)}
    kneel = {6: 0, 7: 1, 8: 2}                                  # Matthew, Thomas, James son of Alphaeus
    pairs = {9: (3, 1), 3: (9, -1), 1: (0, 1), 0: (1, -1), 10: (11, 1), 11: (10, -1), 4: (2, 1), 2: (4, -1)}
    leader = {9, 1, 10, 4}                                      # whispers first
    wonder_order = [0, 3, 1, 2, 9, 4, 11, 10, 5]
    t_won = {v: snap(t_jingya - 0.15 + 0.07 * i) for i, v in enumerate(wonder_order)}
    t_kn = {v: snap(t_jingwei - 0.1 + 0.12 * k) for v, k in kneel.items()}
    t_pair = {v: snap(t_bici - 0.05 + 0.06 * (i % 4)) for i, v in enumerate(sorted(pairs))}
    t_swap = {v: snap(t_lian - 0.08 + 0.05 * (i % 4)) for i, v in enumerate(sorted(pairs))}
    t_back = {v: snap(t_l3 + 0.02 + 0.06 * (idx_of[v] % 6)) for v, *_ in members}
    t_rise = {v: snap(t_mentu + 0.05 + 0.15 * k) for v, k in kneel.items()}

    for v, row, lx, ly in members:
        idx = idx_of[v]
        x, y = A.lp(lx, ly)
        kk = A.K * (0.97 if ly < 0 else 1.0)
        F = {}
        F["stand"] = A.doc(disc(x, y, kk, -1, v, "stand", "awed", wet=True))
        F["stand_b"] = A.doc(disc(x, y, kk, -1, v, "stand", blink("awed"), wet=True))
        F["wonder"] = A.doc(disc(x, y, kk, -1, v, "wonder", "amazed", wet=True))
        if v in kneel:
            F["kneel"] = A.doc(disc(x, y, kk, -1, v, "kneel", "awed", wet=True))
        if v in pairs:
            f = pairs[v][1]
            F["whisper"] = A.doc(disc(x, y, kk, f, v, "whisper", "awed", wet=True))
            F["listen"] = A.doc(disc(x, y, kk, f, v, "wonder", "amazed", wet=True))
        F["dry"] = A.crew_start_svg(v, lx, ly, wet=False)       # = s14's first frame of this disciple
        names = list(F)
        # the wet 'stand' must sit right before 'dry' for the drying cross-fade (same pose, only the cloth dries)
        names.remove("stand")
        names.remove("dry")
        names += ["stand", "dry"]
        I = {n: i for i, n in enumerate(names)}
        frames = [F[n] for n in names]
        ents = [(-1, I["stand"])]
        dips = []
        if v in t_won and v not in pairs:
            ents.append((t_won[v], I["wonder"]))
            dips.append(t_won[v])
        if v in pairs:
            if v in t_won:
                ents.append((t_won[v], I["wonder"]))
                dips.append(t_won[v])
            first, second = ("whisper", "listen") if v in leader else ("listen", "whisper")
            ents += [(t_pair[v], I[first]), (t_swap[v], I[second])]
            dips += [t_pair[v], t_swap[v]]
            ents.append((t_back[v], I["stand"]))
            dips.append(t_back[v])
        elif v in kneel:
            ents.append((t_kn[v], I["kneel"]))
            dips.append(t_kn[v])
            ents.append((t_rise[v], I["stand"]))
            dips.append(t_rise[v])
        else:                                                    # Bartholomew, right behind Jesus: wonder, then rest
            ents.append((snap(t_bici + 0.2), I["stand"]))
            ents.append((snap(t_lian + 0.1), I["wonder"]))
            ents.append((t_back[v], I["stand"]))
            dips += [snap(t_bici + 0.2), snap(t_lian + 0.1), t_back[v]]
        # blinks while standing (never inside the dissolve)
        for tb in (0.6 + 0.23 * (idx % 5), t_l3 + 1.2 + 0.19 * (idx % 4), t_jesus + 0.6 + 0.15 * (idx % 5)):
            tb = snap(tb)
            if tb < t_dry0 - 0.2 and all(abs(tb - tk) > 0.35 for tk, _ in ents):
                cur = [i for tk, i in sorted(ents) if tk <= tb][-1]
                if cur == I["stand"]:
                    ents += [(tb, I["stand_b"]), (snap(tb + 0.13), I["stand"])]
        ents.sort()
        base = cuts(ents)
        i_stand, i_dry = float(I["stand"]), float(I["dry"])

        def fa(t, base=base, i_stand=i_stand, i_dry=i_dry):
            if t >= t_dry0:
                return i_stand + dry(t)
            return base(t)
        piv = (x, y)
        per, ph = 2.6 + 0.15 * (idx % 4), 0.13 * idx
        mots = [bm] + [A.squash_at(d, kk, lambda t, piv=piv: piv, 6) for d in dips]
        mots.append(lambda t, per=per, ph=ph, piv=piv: Tf(sy=1 + 0.011 * math.sin(2 * math.pi * (U(t) / per + ph)),
                                                         px=piv[0], py=piv[1]))
        z = (3.0 if row == "far" else 5.0) + 0.01 * idx
        sc.add(f"crew{v}", frames, frame_at=fa, z=z, seed=A.crew_seed(v), motion=M.combine(*mots))

    # ------------------------------------------------------------ Jesus at the stern
    js = A.lp(*A.JESUS_SIT)
    jfr = [A.jesus_sit_svg("warm"),                                    # 0 = s14's first frame
           A.doc(jes(js[0], js[1], A.K, 1, "sit", "smile")),          # 1
           A.doc(jes(js[0], js[1], A.K, 1, "sit", blink("warm"))),    # 2
           A.doc(jes(js[0], js[1], A.K, 1, "sit", "calm"))]           # 3 quiet, eyes lowered
    t_up = snap(t_l3 + 0.5)
    t_smile = snap(t_jesus - 0.05)
    t_warm = snap(min(t_x - 0.7, t_smile + 1.9))
    jents = [(-1, 3), (t_up, 0), (snap(t_up + 1.1), 2), (snap(t_up + 1.23), 0), (t_smile, 1), (t_warm, 0)]
    sc.add("jesus", jfr, frame_at=cuts(sorted(jents)), z=4.0, seed=A.SEED["jesus"],
           motion=M.combine(bm, A.squash_at(t_up, A.K, lambda t: js, 4), A.squash_at(t_smile, A.K, lambda t: js, 4),
                            lambda t: Tf(sy=1 + 0.011 * math.sin(2 * math.pi * (U(t) / 3.0)), px=js[0], py=js[1])))
    sc.add("jglow", A.jglow_svg(), z=3.9, wc=0, seed=A.SEED["jglow"], blend="screen",
           motion=M.combine(bm, lambda t: Tf(alpha=M.progress(t, t_smile - 0.1, t_smile + 0.9, "sine") *
                                             A.jglow_alpha(U(t)))))

    class _Shift:
        """FX sparkles round Jesus that ride with the drifting boat."""

        def __init__(self, inner):
            self.inner = inner

        def __call__(self, frame, t, view):
            dx = bx(t) - A.X_LAND
            v0 = view.to_out

            class V:
                scale = view.scale

                @staticmethod
                def to_out(x, y):
                    return v0(x + dx, y)
            return self.inner(frame, t, V)
    gx, gy = A.lp(A.JESUS_SIT[0] + 20, A.JESUS_SIT[1] - 170)
    sc.fx.append(_Shift(FX.sparkles((gx - 120, gy - 140, gx + 120, gy + 90), count=8, t0=t_smile, t1=t_x - 0.15,
                                    size=(8, 15), period=1.2, drift=-10, seed=131)))

    # ------------------------------------------------------------ camera: wide -> in on the crew -> back to s14's
    def cam(t):
        b = bx(t)
        wide = Cam(b + 60, 600, 1720)
        close = Cam(b + 90, 762, 1120)
        jes_c = Cam(b - 110, 760, 980)
        k1 = M.progress(t, 0.45, t_jingya - 0.1, "inout")
        c = Cam(M.lerp(wide.x, close.x, k1), M.lerp(wide.y, close.y, k1), M.lerp(wide.w, close.w, k1))
        k2 = M.progress(t, t_l3 - 0.2, t_jesus - 0.1, "inout")
        c = Cam(M.lerp(c.x, jes_c.x, k2), M.lerp(c.y, jes_c.y, k2), M.lerp(c.w, jes_c.w, k2))
        f = A.follow_cam(U(t))
        k3 = M.progress(t, t_smile + 0.6, t_x, "inout")
        c = Cam(M.lerp(c.x, f.x, k3), M.lerp(c.y, f.y, k3), M.lerp(c.w, f.w, k3))
        return A.clamp_cam(c)
    sc.camera = cam

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-17, fade_in=0.8, fade_out=1.2)
    sc.sfx("night", 0, dur=t_dawn1, gain_db=-26, fade_in=0.8, fade_out=2.0)
    sc.sfx("cloth", t_jingya, gain_db=-18, pan=0.1)
    sc.sfx("cloth", t_jingwei, gain_db=-17, pan=-0.2)
    sc.sfx("cloth", t_bici + 0.1, gain_db=-19, pan=0.2)
    sc.sfx("chime", t_smile, gain_db=-14, pan=-0.2)
    sc.sfx("sparkle", t_smile + 0.3, gain_db=-18, pan=-0.2)
    sc.sfx("birds", t_dawn1 - 1.6, dur=T - t_dawn1 + 1.9, gain_db=-26, fade_in=1.5, fade_out=1.0)
    return sc
