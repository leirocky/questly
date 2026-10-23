"""Scene 7 - Luke 19:7. Jesus and Zacchaeus walk off together towards his house, Zacchaeus beaming; the crowd frowns,
folds its arms and mutters; but Jesus goes with him all the same, a kind hand on his shoulder, and Zacchaeus opens his
gate.

Two shots on the shared s05/s06 stage, joined by a hard cut on a phrase boundary (the same two people in both):
  A  the sycamore-fig (the first second is s06's last second: a plain 1 s fade - same layers, seeds, refs, keys and
     global-clock motion); Zacchaeus leads Jesus off to the left past the people at the tree and along the street
  B  Zacchaeus's fine house further down the street (props.zacchaeus_house exterior), a few grumblers by the road

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's beat();
nothing hard-coded to the take). Times are for the current take:
  0 .. 1.0      s06's end: Zacchaeus 'come!' (host) beside Jesus under the tree, the crowd watching
  '大家看见了' 0.95  he turns, waves 'this way!' towards his house and trots off, beaming; Jesus walks with him, Peter
                and John follow; the people at the tree turn to watch them go ('看' 1.38)
  '都不高兴' 2.26  frowns and folded arms all along the road (the townsfolk lining the street too)
  '小声说' 3.38  they lean together and mutter in pairs
  '哼' 5.07     a huff: two of them point after Zacchaeus (grumpy puffs)
  '大家都说' 9.02  hard cut to his house: the two walk in along the street, a few grumblers by the road muttering
  '坏' 11.12    Zacchaeus stops and glances back at the grumblers, his smile gone; they fold their arms and turn away;
                Jesus stops beside him; '可是耶稣' 12.09 he bows his head (lonely) and Jesus looks down at him kindly
  '愿' 13.54    Jesus puts a kind hand on his shoulder; Zacchaeus looks up at him, touched
  '到他家里去' 13.92  overjoyed, he turns to his gate and pushes it open: warm light spills out (chime); 'come in!'
  end           calm last frame (page turn into s08): the open gate, Zacchaeus inviting Jesus in, Jesus smiling
"""
import math
import random

from art import characters as C
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.loader import context
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import beat
from stories.noah.scenes.s01_title import snap
from stories.zacchaeus.scenes.s05_tree import (
    CK, CY, FOLLOWERS, H5, HOUSE_X, HOUSE_Y, K, STRIDE, TREE_CROWD, W5, YT, YU, ZREF, Z_FARCROWD, Z_FX, Z_ZAC, Fig,
    Track, add_ambient, add_right_crowd, add_twig, add_world, breath, cam_path, dk, doc, f1, fk, folk_svg, jes_blink, jk,
    procession, tree_crowd_layer, zac_blink, zac_svg, zk)
from stories.zacchaeus.scenes.s06_call import (CAM_END6, FOLK_END, JES_END, JOHN_END, PETER_END, TREE_END, ZAC_END,
                                               ZAC_END_X)

INK = "#4b3426"
ZAC_ADV = (22.8, 20.8, 47.2, 45.3)        # planted-foot advance (scale 1) into walk_a, walk_c (after a), walk_b, walk_c
ZAC_CYCLE = ("walk_a", "walk_c", "walk_b", "walk_c")
YB = 935                                  # shot B: the walking line in front of his house
GATE_X = HOUSE_X                          # the carved double gate (props.ZAC_GATE: +-118 local)
DOORS = (0.0, 0.25, 0.5, 0.75, 1.0)
GRUMBLERS_B = [   # shot B: a few grumblers by the road (kind, variant, x)
    ("man", 5, 1392), ("woman", 4, 1478), ("man", 0, 1590), ("elder", 3, 1668),
]


def zac_walk(fig, t0, x0, x1, y, f, expr, per):
    """Planted-foot trot of Zacchaeus from x0 to x1 starting at t0 (cycle a, c, b, c; the anchor advances on every
    cut). Returns the time of the last cut."""
    i = 0
    x = x0
    tk = t0
    while True:
        fr = ZAC_CYCLE[i % 4]
        adv = ZAC_ADV[i % 4] * K * (0.6 if i == 0 else 1.0)
        if abs(x1 - x) < adv * 0.5:
            break
        tk = snap(t0 + i * per)
        fig.cut(tk, zk(fr, f, expr), dip=False)
        x += f * adv
        fig.track.to(tk - 0.05, tk + 0.07, x, y)
        i += 1
    return tk


def walk2(fig, t0, x0, x1, y, keyf, stride, per, first=0):
    """Planted-foot walk with two stride drawings from x0 to x1 starting at t0. Returns the time of the last cut."""
    f = 1 if x1 > x0 else -1
    n = max(1, int(round(abs(x1 - x0) / stride)))
    st = abs(x1 - x0) / n
    tk = t0
    for i in range(n):
        tk = snap(t0 + i * per)
        fig.cut(tk, keyf(("walk_a", "walk_b")[(i + first) % 2]), dip=False)
        fig.track.to(tk - 0.06, tk + 0.08, x0 + f * st * (i + 1), y)
    return tk


def huff_svg(x, y, s=1.0):
    """A grumpy little puff ('hmph!') beside a head: a cloud with three short strokes."""
    b = ""
    for dx, dy, r in ((0, 0, 13), (15, -5, 11), (27, 3, 9), (11, 9, 9)):
        b += (f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s)}" fill="#f1e6d2" stroke="{INK}" '
              f'stroke-width="{f1(2.6 * s)}"/>')
    for dx, dy, r in ((0, 0, 13), (15, -5, 11), (27, 3, 9), (11, 9, 9)):
        b += f'<circle cx="{f1(x + dx * s)}" cy="{f1(y + dy * s)}" r="{f1(r * s - 1.4)}" fill="#f1e6d2"/>'
    for k in range(3):
        a = math.radians(-150 + 30 * k)
        b += (f'<path d="M{f1(x - 16 * s + 8 * math.cos(a) * s)},{f1(y - 4 * s + 8 * math.sin(a) * s)} '
              f'l{f1(10 * math.cos(a) * s)},{f1(10 * math.sin(a) * s)}" stroke="{INK}" stroke-width="{f1(2.6 * s)}" '
              f'stroke-linecap="round"/>')
    return S.g(b, filter="wobble-fine")


def puff_motion(t0, piv, dur=1.1):
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf(alpha=0.0)
        s = 0.4 + 0.6 * M.progress(t, t0, t0 + 0.2, "back")
        a = M.progress(t, t0, t0 + 0.08, "sine") * (1 - M.progress(t, t0 + dur * 0.6, t0 + dur, "sine"))
        return Tf(sx=s, sy=s, px=piv[0], py=piv[1], alpha=a, dx=10 * u, dy=-14 * u)
    return m


def grumblers_b_markup(state, phase=0.0):
    out = ""
    rng = random.Random(3)
    for i, (kind, v, x) in enumerate(GRUMBLERS_B):
        dy = rng.uniform(-4, 4)
        if state == "mutter":
            pose, f, mod = ("mutter", "mutter", "arms_folded", "frown")[i], (1, -1, -1, -1)[i], None
        elif state == "point":
            pose, f, mod = ("point", "mutter", "arms_folded", "point")[i], (-1, -1, -1, -1)[i], None
        elif state == "glare":
            pose, f, mod = ("arms_folded", "arms_folded", "frown", "arms_folded")[i], (1, -1, 1, -1)[i], None
        else:
            raise ValueError(state)
        expr = "grumble" if pose in ("point", "frown") else None
        out += folk_svg(x, CY + dy, CK, fk(kind, v, pose, f, expr, phase, mod))
    return out


def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(7)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731

    # ---- beats
    t_dj = b(0, "大家看见了")
    t_kan = b(0, "看")
    t_bgx = b(0, "都不高兴")
    t_xsh = b(0, "小声说")
    t_heng = b(1, "哼")
    t_l1e = ctx.lines[1].end
    t_l2 = ctx.lines[2].start
    t_huai = b(2, "坏")
    t_ks = b(2, "可是耶稣")
    t_hs = b(2, "还是愿意")
    t_dao = b(2, "到他家里去")
    t_cut = snap(t_l2 - 0.08)                    # the hard cut to his house (a phrase boundary)

    # ---- the house gate opens on '到他家里去'
    t_jia = b(2, "家里")
    t_push = snap(t_jia + 0.36)
    door_t = [t_push + 0.06 + 0.1 * k for k in range(len(DOORS))]

    def door_fa(t):
        k = 0
        for i, td in enumerate(door_t):
            if t >= td:
                k = i
        return float(k)
    add_world(sc, g0, house_door=(DOORS, door_fa))
    add_right_crowd(sc, g0)
    add_twig(sc, g0, lambda t: 0.0)

    # the people at the tree: watching, frowning, muttering, huffing
    tree_crowd_layer(sc, g0, [(0, TREE_END), (t_kan + 0.05, "see"), (t_bgx + 0.02, "frown"), (t_xsh + 0.05, "mutter"),
                              (t_heng - 0.04, "hmph"), (t_heng + 1.5, "mutter"), (t_l1e + 0.2, "glare")])
    # the townsfolk lining the street: watching, then grumbling
    line_frames = [doc(C.jericho_crowd(2290, CY, CK, 1, n=11, pose="line", rows=1, width=1250, seed=1, phase=p))
                   for p in (0.0, 0.5)]
    grum_frames = [doc(C.jericho_crowd(2290, CY, CK, 1, n=11, pose="grumble", rows=1, width=1250, seed=1, phase=p))
                   for p in (0.0, 0.5)]
    sc.add("c_line", line_frames + grum_frames, z=Z_FARCROWD, seed=151,
           frame_at=lambda t: float((2 if t >= t_bgx + 0.1 else 0) + int(math.floor((t + g0) / 0.5)) % 2))
    # shot B: grumblers by the road near his house
    gb_ents = [(0, "mutter"), (snap(t_huai - 0.5), "point"), (snap(t_huai + 0.25), "glare"), (snap(t_dao), "mutter")]
    gstates = ["mutter", "point", "glare"]
    sc.add("c_grumb", [doc(grumblers_b_markup(s_)) for s_ in gstates], z=Z_FARCROWD, seed=173,
           frame_at=lambda t: float(gstates.index([s_ for tk, s_ in gb_ents if t >= tk or tk == 0][-1])))

    # ---- the procession figures from s06 (same refs, seeds and motions), starting in s06's end keys
    c6 = context("s06_call")
    figs, _ = procession(sc, g0, c6)
    jf = figs["jesus"]
    jf.cut(0, JES_END)
    figs["peter"].cut(0, PETER_END)
    figs["john"].cut(0, JOHN_END)
    for j in range(len(FOLLOWERS)):
        figs[f"folk{j}"].cut(0, FOLK_END[j])

    # ---- Zacchaeus
    zac = Fig("zac", lambda key, i=0: zac_svg(ZREF[0], ZREF[1], K, key), ZREF, Z_ZAC, g0, seed=181)
    zac.track = Track(ZAC_END_X, YT)
    zac.cut(0, ZAC_END)
    # '大家看见了': 'this way!' and off he trots, beaming
    t_turn = snap(max(1.17, t_dj + 0.12))
    zac.cut(t_turn, zk("host", -1, "overjoyed"), depth=6)
    per_z = 0.155
    t_w0 = snap(t_turn + 0.55)
    zac_walk(zac, t_w0, ZAC_END_X, 2350, YT, -1, "overjoyed", per_z)
    # shot B: he trots in towards his gate ...
    XZ_B0, XZ_STOP = 1300, 932
    t_b_stop = snap(t_huai - 0.06)
    per_b = max(0.12, min(0.19, (t_b_stop - t_cut) / max(1, round((XZ_B0 - XZ_STOP) / (sum(ZAC_ADV) / 4 * K)))))
    zac.ents = [e for e in zac.ents if e[0] < t_cut]
    zac.track.moves = [mv for mv in zac.track.moves if mv[1] < t_cut - 0.01]
    zac.track.cur = zac.track(t_cut - 0.01)
    zac.track.to(t_cut - 0.002, t_cut, XZ_B0, YB)
    zac_walk(zac, t_cut, XZ_B0, XZ_STOP, YB, -1, "happy", per_b)
    # ... '坏': stops and glances back at the grumblers, his smile gone
    zac.cut(t_b_stop, zk("stand", 1, "sad", mod="glance"), depth=6)
    zac.track.to(t_b_stop - 0.05, t_b_stop + 0.1, XZ_STOP, YB)
    t_lonely = snap(t_ks - 0.04)
    zac.cut(t_lonely, zk("lonely", 1, "lonely"), depth=5)
    # '愿': Jesus's hand on his shoulder; he looks up at him, touched
    t_hand = snap(t_hs - 0.05)
    zac.cut(snap(t_hand + 0.2), zk("stand", 1, "grateful", mod="up_to"), depth=5)
    # '到他家里去': overjoyed, he turns to his gate and pushes it open, then 'come in!'
    t_go = snap(t_jia - 0.12)
    zac.cut(t_go, zk("stand", -1, "overjoyed"), depth=6)
    x_push = GATE_X + 112
    zac_walk(zac, snap(t_go + 0.1), XZ_STOP, x_push, YB, -1, "overjoyed", max(0.08, (t_push - t_go - 0.16) / 5))
    zac.cut(t_push, zk("stand", -1, "happy", mod="push"), depth=5)
    zac.track.to(t_push - 0.06, t_push + 0.05, x_push, YB)
    t_host = snap(door_t[-1] + 0.2)
    zac.cut(t_host, zk("host", 1, "overjoyed"), depth=6)
    zac.blinks(zac_blink, 1.5, T - 0.4, rng, avoid=[(0, 1.3), (t_cut - 0.3, t_b_stop + 0.2), (t_go - 0.3, t_host + 0.3)])
    zac.mots.append(breath(ZREF, g0, 2.6, 0.012))
    zac.build(sc)

    # ---- Jesus: walks with him, then stops beside him at the gate
    per_j = 0.4
    XJ0 = jf.track(0.0)[0]
    t_j0 = snap(t_turn + 0.62)
    walk2(jf, t_j0, XJ0, 2560, YU, lambda fr: jk(fr, -1, "warm"), STRIDE["jesus"] * K, per_j)
    XJ_B0, XJ_STOP = XZ_B0 + 178, XZ_STOP + 92
    jf.ents = [e for e in jf.ents if e[0] < t_cut]
    jf.track.moves = [mv for mv in jf.track.moves if mv[1] < t_cut - 0.01]
    jf.track.cur = jf.track(t_cut - 0.01)
    jf.track.to(t_cut - 0.002, t_cut, XJ_B0, YB)
    t_js = snap(t_huai + 0.25)
    n_j = max(2, int(round((XJ_B0 - XJ_STOP) / (STRIDE["jesus"] * K))))
    walk2(jf, t_cut, XJ_B0, XJ_STOP, YB, lambda fr: jk(fr, -1, "warm"),
          STRIDE["jesus"] * K, max(0.3, min(0.45, (t_js - t_cut) / n_j)))
    jf.cut(t_js, jk("stand", -1, "warm"), depth=4)
    jf.cut(snap(t_ks + 0.1), jk("stand", -1, "kind", "down"), depth=5)
    # the hand on his shoulder (the near hand on the top of Zacchaeus's front shoulder)
    zsh = C.body_points(C.zacchaeus, XZ_STOP, YB, K, 1, pose="stand")["shoulders"][0]
    lx, ly = (zsh[0] + 5 * K - XJ_STOP) * -1 / K, (zsh[1] + 11 * K - YB) / K
    hand = ((("ik", "abs", lx, ly, 1), ("fk", -8, -3)), ("open", "fist"))
    jf.cut(t_hand, jk("stand", -1, "warm", "down", arms=hand), depth=4)
    t_jg = snap(t_go + 0.3)
    jf.cut(snap(t_go + 0.12), jk("stand", -1, "warm"), depth=4)
    walk2(jf, t_jg, XJ_STOP, XJ_STOP - 0.55 * STRIDE["jesus"] * K, YB, lambda fr: jk(fr, -1, "warm"), STRIDE["jesus"] * K, 0.36)
    jf.cut(snap(t_jg + 0.4), jk("smile", -1, None, "down"), depth=4)
    jf.cut(snap(t_host + 0.15), jk("smile", -1, None), depth=4)
    jf.blinks(jes_blink, 1.6, T - 0.4, rng, avoid=[(0, 1.3), (t_cut - 0.3, t_js + 0.2), (t_hand - 0.3, t_hand + 0.6)])
    # the disciples follow at a distance (out of the picture by the cut)
    for name, v, dt, per in (("peter", "peter", 1.4, 0.38), ("john", "john", 1.75, 0.4)):
        df = figs[name]
        x0 = df.track(0.0)[0]
        walk2(df, snap(t_j0 + dt), x0, 2700, df.ref[1], lambda fr, v=v: dk(v, fr, -1, "happy"), STRIDE["disc"] * K, per)
        df.ents = [e for e in df.ents if e[0] < t_cut]
        df.alpha = lambda t: 1.0 if t < t_cut else 0.0
    # the townsfolk who came with Jesus: watch, frown, mutter
    for j, (kind, v, *_r) in enumerate(FOLLOWERS):
        ff = figs[f"folk{j}"]
        ff.cut(snap(t_kan + 0.05 + 0.04 * j), fk(kind, v, "look", -1, "surprised"), depth=4)
        ff.cut(snap(t_bgx + 0.05 * j), fk(kind, v, ("arms_folded", "frown", "frown", "arms_folded", "frown")[j], -1,
                                           "grumble" if j % 2 == 0 else None), depth=4)
        ff.cut(snap(t_xsh + 0.05 * j), fk(kind, v, "mutter", (1, -1, 1, 1, -1)[j]), depth=4)
        ff.alpha = lambda t: 1.0 if t < t_cut else 0.0
    for f_ in figs.values():
        f_.build(sc)

    # ---- the huffs on '哼'
    for i, (hx, hy) in enumerate(((TREE_CROWD[1]["x1"] - 52, CY - 372 * CK), (TREE_CROWD[0]["x1"] - 48, CY - 352 * CK),
                                  (TREE_CROWD[5]["x1"] - 52, CY - 372 * CK))):
        t0 = t_heng + 0.02 + 0.12 * i
        sc.add(f"huff{i}", doc(huff_svg(hx, hy, 1.0)), z=Z_FX, wc=0, motion=puff_motion(t0, (hx, hy)))
    # shot B: a huff from the grumblers on '坏人'
    for i, (kind, v, x) in enumerate(GRUMBLERS_B[:2]):
        hx, hy = x - 52, CY - 372 * CK
        sc.add(f"huffb{i}", doc(huff_svg(hx, hy, 1.0)), z=Z_FX, wc=0, motion=puff_motion(t_huai - 0.4 + 0.15 * i, (hx, hy)))

    # ---- the warm light from the open gate
    gx, gy = GATE_X, HOUSE_Y - 150 * K
    gid = "zq7gate"
    defs = S.rad_grad(gid, [(0, "#ffe7a6", 1.0), (0.35, "#ffcf6e", 0.7), (0.7, "#f6b04e", 0.22), (1, "#f6b04e", 0)])
    gw, gtop = 100 * K, HOUSE_Y - 312 * K
    gdefs = S.lin_grad("zq7gin", [(0, "#ffefbd"), (0.55, "#ffd77e"), (1, "#f2ac4c")])
    gate_in = (f'<path d="M{f1(gx - gw)},{f1(HOUSE_Y)} L{f1(gx - gw)},{f1(gtop + gw)} A{f1(gw)},{f1(gw)} 0 0 1 '
               f'{f1(gx + gw)},{f1(gtop + gw)} L{f1(gx + gw)},{f1(HOUSE_Y)} Z" fill="url(#zq7gin)"/>')
    spill = (f'<path d="M{f1(gx - gw)},{f1(HOUSE_Y)} L{f1(gx + gw)},{f1(HOUSE_Y)} L{f1(gx + gw * 2.3)},{f1(HOUSE_Y + 70)} '
             f'L{f1(gx - gw * 2.1)},{f1(HOUSE_Y + 70)} Z" fill="#ffd98a" opacity="0.55"/>')
    sc.add("gate_light", doc(gate_in, gdefs), z=Z_FARCROWD - 0.06, wc=0.3,
           motion=lambda t: Tf(alpha=0.85 * M.progress(t, door_t[1], door_t[-1] + 0.25, "sine")))
    sc.add("gate_spill", doc(S.g(spill, filter="soft")), z=Z_FARCROWD - 0.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, door_t[1], door_t[-1] + 0.4, "sine")))
    sc.add("gate_glow", doc(f'<ellipse cx="{f1(gx)}" cy="{f1(gy + 40)}" rx="300" ry="270" fill="url(#{gid})"/>', defs),
           z=Z_FARCROWD - 0.04, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.6 * M.progress(t, door_t[1], door_t[-1] + 0.4, "sine")
                               * (0.92 + 0.08 * math.sin(2 * math.pi * (t + g0) / 2.3))))
    sc.fx.append(FX.motes((gx - 200, gy - 160, gx + 260, gy + 200), count=12, t0=door_t[2], t1=T + 1, color=(255, 236, 170),
                          size=(3, 6), seed=29, alpha=170))

    add_ambient(sc, g0)

    # ---- camera: A follows them along the street; B (hard cut) at his house
    c_a3 = Cam(2860, 684, 1880)
    c_b0 = Cam(1010, 676, 1640)
    c_b1 = Cam(905, 672, 1540)
    c_b2 = Cam(880, 662, 1500)
    camA = cam_path([(0.0, CAM_END6), (1.0, CAM_END6), (t_cut, c_a3)], ["linear", "sine"])
    camB = cam_path([(t_cut, c_b0), (t_huai + 0.3, c_b1), (t_dao, c_b1), (min(T - 1.0, t_host + 0.3), c_b2), (T, c_b2)],
                    ["inout", "linear", "inout", "linear"])
    sc.camera = lambda t: camA(t) if t < t_cut else camB(t)

    # ---- sound
    sc.sfx("crowd", 0, dur=t_cut + 0.3, gain_db=-16, fade_in=0.6, fade_out=0.25, pan=0.3)
    sc.sfx("crowd", t_cut, dur=T - t_cut + 0.5, gain_db=-22, fade_in=0.15, fade_out=1.0, pan=0.5)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0, pan=-0.3)
    sc.sfx("footsteps", t_w0, dur=t_cut - t_w0, gain_db=-21, fade_in=0.2, fade_out=0.25)
    sc.sfx("footsteps", t_cut, dur=t_b_stop - t_cut + 0.1, gain_db=-20, fade_in=0.05, fade_out=0.2)
    sc.sfx("cloth", t_turn, gain_db=-18)
    sc.sfx("cloth", t_lonely, gain_db=-20)
    sc.sfx("cloth", t_hand, gain_db=-19)
    sc.sfx("footsteps", t_go + 0.08, dur=t_push - t_go, gain_db=-20)
    sc.sfx("cloth", t_push + 0.02, gain_db=-17)
    sc.sfx("chime", door_t[2], gain_db=-14)
    return sc
