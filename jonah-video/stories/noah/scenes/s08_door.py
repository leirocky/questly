"""Scene 8 - 挪亚一家八口人，也走进了方舟。然后，上帝亲手把门关上了。 (Genesis 7:7, 13-16)

Starts exactly where s07 ends (plain 1 s cross-dissolve: same hilltop page, camera, light and the family standing
in their line on the ramp; every cyclic clock is shifted by s07's duration - 1 s so the dissolve matches).

  line 0  '挪亚一家八口人，也走进了方舟。'  the family walks up the ramp and in at the door with the last of the
          food, one after another (planted strides; they dim as they go into the hold). Noah, last, stops at the
          top of the ramp, turns round and waves goodbye to the green world, then goes in too. The camera eases
          a little closer to the door.
  line 1  '然后，上帝亲手把门关上了。'  on 上帝 a warm golden light gathers round the doorway (rim glow, halo,
          sparkles); on 把门 the big door swings shut all by itself (door 1 -> 0 in eighths, about a second) and
          closes on 关上了 with a soft thunk (a little dust, a tiny camera nudge). The glow fades.
  after   the first dark clouds have slid in over the sun; the light dims to a cool grey-blue; the camera eases
          back to show the closed ark under the gathering clouds. Calm last frame (page-turn dip to s09).
God is never drawn: only the golden light round the door.
"""
import math

from engine import fx as FX
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from art import props as PR
from art import style as S
from stories.noah.scenes import s07_animals as A
from stories.noah.scenes.s07_animals import (AX, DX0, DX1, DTOP, FAM_END, FAM_ORDER, GY, RTX, SC, SH, SILL, SW, Actor,
                                              Stepper, cam_at, cam_path, clamp, doc, family_sprites, lin_plan,
                                              noah_frames, person_spr, pt, snap, squash_dip)

STEP = 51.0          # stride (px) and period (s) of the family's walk
PER = 0.22


def door_glow_svg():
    x0, top, x1, sill = DX0, DTOP, DX1, SILL
    cx, cy = (x0 + x1) / 2, (top + sill) / 2
    defs = S.rad_grad("n8glow", [(0, "#fff3c6", 0.85), (0.45, "#ffe39a", 0.4), (1, "#ffe39a", 0)])
    rays = S.rays(cx, cy, 140, 330, 12, 6, rot=8)
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="260" ry="250" fill="url(#n8glow)"/>'
               f'<path d="{rays}" fill="#fff0b8" opacity="0.35" filter="url(#soft)"/>', defs)


def dark_clouds_svg(i):
    """Heavy slate clouds that slide in over the sky (two banks)."""
    if i == 0:
        body = (PR.dark_cloud(380, 330, 1.35, seed=3, light=0.35) + PR.dark_cloud(1150, 250, 1.2, seed=5, light=0.5) +
                PR.dark_cloud(1700, 420, 0.9, seed=8, light=0.45))
    else:
        body = (PR.dark_cloud(2450, 300, 1.35, seed=11, light=0.3) + PR.dark_cloud(3150, 380, 1.2, seed=13, light=0.45) +
                PR.dark_cloud(2000, 460, 0.85, seed=17, light=0.55))
    return doc(body)


def overcast_svg():
    defs = S.lin_grad("n8oc", [(0, "#7f8da3"), (0.5, "#a3adbb"), (0.75, "#c3c6c4"), (1, "#cfcfc4")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="1180" fill="url(#n8oc)"/>', defs)


def dust_ring_svg():
    """A soft puff of dust along the closed door's edges (the thunk)."""
    out = ""
    for k, (x, y) in enumerate(((DX0 - 6, SILL - 20), (DX1 + 6, SILL - 24), (DX0 + 30, SILL + 4), (DX1 - 30, SILL + 4),
                                (DX0 - 4, DTOP + 60), (DX1 + 4, DTOP + 70))):
        out += A.dust_markup(x, y, 44, seed=40 + k, col="#e9dcc0")
    return doc(S.g(out, opacity=0.7))


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[:2]
    T7 = context("s07_animals", load_timeline()).duration
    toff = T7 - 1.0                       # s08 t=0 is s07's t = T7 - 1 (the 1 s dissolve)

    t_walk = snap(max(1.12, pt(ctx, 0, "挪亚") + 0.1))
    t_god = pt(ctx, 1, "上帝")
    t_door = pt(ctx, 1, "把门")
    t_shut = pt(ctx, 1, "关上了")
    t_close = max(t_door + 0.85, t_shut + 0.35)     # the door meets its frame

    # ---------------- camera: s07's last framing, a little closer for the door, then back for the clouds
    BOT = SH - 2
    C0 = cam_at(1640, 1760, BOT - 10)
    C1 = cam_at(1560, 1560, BOT - 40)
    C2 = cam_at(1450, 1480, BOT - 60)
    C3 = cam_at(1560, 2060, BOT - 30)
    base_cam = cam_path([(0, C0), (1.2, C0), (3.6, C1), (t_god, C1), (t_door + 0.2, C2), (t_close + 0.35, C2),
                         (T - 0.45, C3), (T, C3)])

    def camera(t):
        c = base_cam(t)
        u = t - t_close
        dy = 4.0 * math.exp(-u / 0.06) * math.sin(2 * math.pi * u / 0.12) if 0 <= u < 0.3 else 0.0
        return Cam(c.x, c.y + dy, c.w)
    sc.camera = camera

    # ---------------- backdrop (s07's, with the ark as a door flipbook)
    A.add_backdrop(sc, toff, ark=False)
    dim = lambda t: M.progress(t, 3.4, T - 0.5, "sine")                       # noqa: E731
    sc.add("overcast", overcast_svg(), z=0.35, wc=0.5, motion=lambda t: Tf(alpha=0.85 * dim(t)))
    sc.add("dark_clouds0", dark_clouds_svg(0), z=0.4, wc=0.7,
           motion=lambda t: Tf(dx=-900 * (1 - M.progress(t, 3.0, T - 0.3, "out")) - 4 * t,
                               alpha=M.progress(t, 3.0, 4.6, "sine")))
    sc.add("dark_clouds1", dark_clouds_svg(1), z=0.45, wc=0.7,
           motion=lambda t: Tf(dx=1000 * (1 - M.progress(t, 3.4, T - 0.2, "out")) + 3 * t,
                               alpha=M.progress(t, 3.4, 5.0, "sine")))
    glows = [0.0, 0.35, 0.7, 1.0]
    doors = [1.0, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0]
    frames = [A.ark_svg(door=1.0, glow=g) for g in glows]                    # 0..3
    frames += [A.ark_svg(door=d, glow=1.0) for d in doors[1:]]               # 4..11
    frames += [A.ark_svg(door=0.0, glow=g) for g in (0.6, 0.25, 0.0)]        # 12..14
    t_g0 = t_god - 0.1
    t_d0 = t_close - 0.9

    def ark_frame(t):
        if t < t_d0:
            return 3.0 * M.progress(t, t_g0, t_g0 + 0.9, "sine")
        if t < t_close:
            u = M.progress(t, t_d0, t_close, lambda v: v * (0.35 + 0.65 * v))
            return float(3 + min(8, int(u * 8 + 0.5)))
        return 11 + 3.0 * M.progress(t, t_close + 0.4, t_close + 1.6, "sine")
    sc.add("ark", frames, z=3, frame_at=ark_frame, seed=A.ARK_SEED)
    sc.add("door_glow", door_glow_svg(), z=3.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.9 * M.progress(t, t_g0, t_g0 + 0.9, "sine") *
                               (1 - M.progress(t, t_close + 0.3, t_close + 1.6, "sine")),
                               sx=1 + 0.03 * math.sin(t * 3), sy=1 + 0.03 * math.sin(t * 3),
                               px=(DX0 + DX1) / 2, py=(DTOP + SILL) / 2))
    sc.fx.append(FX.sparkles((DX0 - 90, DTOP - 80, DX1 + 90, SILL + 10), count=18, t0=t_g0 + 0.2,
                             t1=t_close + 1.3, size=(7, 15), drift=-10, seed=81))
    sc.add("door_dust", dust_ring_svg(), z=44, wc=0.3,
           motion=M.keys([(t_close - 0.02, {"alpha": 0, "s": 0.85}), (t_close + 0.05, {"alpha": 0.95, "s": 0.95}),
                          (t_close + 0.25, {"alpha": 0.7, "s": 1.06, "dy": -6}),
                          (t_close + 0.65, {"alpha": 0, "s": 1.14, "dy": -14})], ["out", "sine", "in"],
                         pivot=((DX0 + DX1) / 2, SILL)))
    A.add_foreground(sc, toff)
    A.add_butterflies(sc, toff=toff, alpha=lambda t: 1 - M.progress(t, 3.5, 5.5, "sine"))

    # ---------------- the family walks in
    door_clip = A.make_door_clip()
    fam = family_sprites()
    x_in = DX0 - 150
    z0 = 18.0
    last_cut = {}
    for k, nm in enumerate(FAM_ORDER[:-1]):
        sp, idx = fam[nm]
        x0 = FAM_END[nm]
        n = int(math.ceil((x0 - x_in) / STEP))
        cts = [t_walk + j * PER for j in range(n)]
        st = Stepper(lambda t, x0=x0: x0, 0, T, STEP, cut_times=cts, mf=0.6, max_move=0.15)
        st.pos = [x0 - STEP * (j + 1) for j in range(n)]
        st.hold = PER * 1.4
        last_cut[nm] = cts[-1]
        act = Actor(sp, st.x, lambda t, i=idx["carry"]: i, stepper=st,
                    walk=(idx["carry_walk_a"], idx["carry_walk_b"]), span=26 * SC, bounce=6 * SC, clip=door_clip,
                    kshift=k % 2, breathe=(0.010, 2.9, 0.21 * k + toff / 2.9),
                    alpha=lambda t, e=cts[-1]: 1.0 if t < e + 0.4 else 0.0)
        sc.add_dynamic(f"fam_{nm}", act, z=z0 - 0.1 * k)

    # ---------------- Noah: up to the top of the ramp, turn, wave goodbye, in
    sp = person_spr(60)
    fr = noah_frames(sp)
    nx0 = FAM_END["noah"]
    x_top = RTX + 8
    n1 = int(round((nx0 - x_top) / STEP))
    c1 = [t_walk + j * PER for j in range(n1)]
    t_arrive = c1[-1] + PER
    t_turn = snap(t_arrive + 0.05)
    t_wave_end = snap(min(t_turn + 1.05, t_door - 1.7))
    t_back = t_wave_end
    t_go = snap(t_back + 0.2)
    n2 = int(math.ceil((x_top - x_in) / STEP))
    c2 = [t_go + j * PER for j in range(n2)]
    st = Stepper(lambda t: nx0, 0, T, STEP, cut_times=c1 + c2, mf=0.6, max_move=0.15)
    st.pos = [nx0 - (nx0 - x_top) * (j + 1) / n1 for j in range(n1)] + [x_top - STEP * (j + 1) for j in range(n2)]
    st.hold = PER * 1.4

    def nbase(t):
        if t < t_turn:
            return fr["stand_l"]
        if t < t_wave_end:
            return fr[f"wave{int((t - t_turn) * 8) % 4}"]
        return fr["stand_l"]
    nact = Actor(sp, st.x, nbase, stepper=st, walk=(fr["walk_a"], fr["walk_b"]), span=26 * SC, bounce=6 * SC,
                 clip=door_clip, kshift=1, breathe=(0.011, 3.1, 0.1 + toff / 3.1),
                 bumps=[squash_dip(t_turn, 0.045, 0.28), squash_dip(t_back, 0.04, 0.26)],
                 alpha=lambda t: 1.0 if t < c2[-1] + 0.4 else 0.0)
    sc.add_dynamic("noah", nact, z=z0 + 1)

    # ---------------- light: the sun hides, the day turns grey-blue
    sc.fx.append(FX.tint((150, 162, 196), lambda t: 0.5 * dim(t), mode="multiply"))
    sc.fx.append(FX.tint((255, 226, 160), lambda t: 0.10 * M.progress(t, t_g0, t_g0 + 0.8, "sine") *
                         (1 - M.progress(t, t_close + 0.2, t_close + 1.5, "sine")), mode="screen"))

    # ---------------- sound
    sc.sfx("birds", 0.0, dur=4.6, gain_db=-21, fade_in=0.6, fade_out=1.4)
    sc.sfx("wind_soft", 0.0, dur=T, gain_db=-22, fade_in=0.6, fade_out=1.0)
    sc.sfx("footsteps", t_walk, dur=c2[-1] - t_walk + 0.2, gain_db=-19, fade_out=0.4)
    sc.sfx("chime", t_god + 0.05, gain_db=-12)
    sc.sfx("ship_creak", t_d0 + 0.05, dur=t_close - t_d0, gain_db=-16, fade_in=0.1, fade_out=0.15)
    sc.sfx("thud", t_close, gain_db=-6, duck_db=-3)
    sc.sfx("sparkle", t_close + 0.25, gain_db=-17)
    sc.sfx("storm_wind", 5.0, dur=T - 5.0, gain_db=-24, fade_in=2.0, fade_out=0.8)
    return sc
