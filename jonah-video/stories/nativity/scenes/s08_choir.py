"""Scene 8 - Luke 2:13-14. The heavenly host. It opens on the very picture s07 ends with (a plain 1 s fade: same tall
stage, camera, figures, poses and vision bubble, and every loop on the film's global clock), then the night sky above
the fields opens in a great golden light and it fills with angels of light singing and praising God; the shepherds
kneel and gaze up, the boy sets his lamb down and looks up with it, the sheep and the dog look up.

Beats (syllable onsets measured in the voice clip, see s07_shepherds.Tm; nothing hard-coded to the take):
  0 .. 1.0     identical to s07's last second (the vision bubble above the angel's hand, the glory round the group)
  '忽然'        the vision shrinks back into the angel's hand; high above, the sky begins to open in golden light
               (heaven_light, chime) and the camera tilts up and widens to show sky and field together
  '好多好多天使' three groups of singing angels appear one after another in the opened sky, on '好多', '好多' and
               '天使' (sparkles); the young shepherd points up, the others kneel and look up, the boy puts his lamb
               down and looks up with it, the dog and the sheep look up (a bleat)
  '一起赞美上帝' the angel by the shepherds rises and sings with them; little golden notes float up from the host;
               soft rays turn slowly in the opened sky
  line 2 (A)   the host sings (wings flutter, gentle bobbing); '荣耀' a shower of sparkles round the host; '平安'
               another, and the light pulses warmly; the young shepherd kneels too
  line 3       '天上，要赞美上帝' the camera tilts up to the singing host (the light brightens); '地上' it tilts back
               down to the shepherds, and on '平安' a soft peaceful light spreads over the hills and the little town
               (its windows glow)
  end          a calm hold (page dip to s09)
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s07_shepherds import (ANGEL, ANGEL_LOOP, DOG0, FINAL, GLORY, GY, H7, HUDDLE, K, LIFT,
                                                    SEED, SHEEP_IN, SHEEP_OUT, SHEP, SK, STURDY_REST, TOWN, W7,
                                                    YOUNG_WATCH, Fig, Tm, add_bubble, add_crook, add_fields,
                                                    angel_bob, angel_draw, blink, breath, cam_path, doc7, dog_draw,
                                                    env, f1, gsparkles, sheep_in_draw, sheep_markup, sheep_out_draw,
                                                    shep_draw, zorder)
from stories.noah.scenes.s01_title import snap

INK = P["ink"]
HEAVEN = (1056, 400)                 # the centre of the opening in the sky
HEAVEN_P = (0.12, 0.3, 0.52, 0.76, 1.0)
CAM0 = Cam(1130, 1200, 1800)         # = s07's last camera
# the host: three groups (x0, x1, front-row y, n, scale, rows, seed)
GROUPS = [(650, 1470, 900, 5, 0.5, 2, 3), (120, 640, 960, 4, 0.42, 2, 5), (1470, 1990, 960, 4, 0.42, 2, 7)]
CHOIR_PH = 6


def heaven_svg(p):
    """heaven_light, its lowest ring clouds fading out above the far ridge (a soft mask)."""
    defs = (S.lin_grad("hvm", [(0, "#ffffff"), (0.82, "#ffffff"), (1, "#000000")], 0, 0, 0, 1) +
            '<mask id="hvmask" maskUnits="userSpaceOnUse" x="0" y="0" width="2112" height="1800">'
            '<rect x="-20" y="-20" width="2152" height="1110" fill="url(#hvm)"/></mask>')
    return doc7(f'<g mask="url(#hvmask)">{PR.heaven_light(HEAVEN[0], HEAVEN[1], 1.0, progress=p, width=1800, seed=2)}'
                f'</g>', defs)


def choir_svg(gi, k):
    x0, x1, y, n, s, rows, seed = GROUPS[gi]
    return doc7(C.angel_choir(x0, x1, y, n=n, phase=k / CHOIR_PH, scale=s, rows=rows, seed=seed, glow=0.6))


def note_svg(x, y, s, kind=0):
    """A little golden music note."""
    col, edge = "#f6d27a", "#b8862e"
    if kind == 0:
        d = (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(11 * s)}" ry="{f1(8 * s)}" transform="rotate(-20 {f1(x)} '
             f'{f1(y)})" fill="{col}" stroke="{edge}" stroke-width="2.4"/>'
             f'<path d="M{f1(x + 9 * s)},{f1(y - 3 * s)} L{f1(x + 9 * s)},{f1(y - 40 * s)} Q{f1(x + 22 * s)},'
             f'{f1(y - 30 * s)} {f1(x + 24 * s)},{f1(y - 18 * s)}" fill="none" stroke="{edge}" stroke-width="3.2" '
             f'stroke-linecap="round"/>')
    else:
        d = ""
        for dx in (0, 26):
            d += (f'<ellipse cx="{f1(x + dx * s)}" cy="{f1(y)}" rx="{f1(10 * s)}" ry="{f1(7 * s)}" '
                  f'transform="rotate(-20 {f1(x + dx * s)} {f1(y)})" fill="{col}" stroke="{edge}" stroke-width="2.4"/>')
            d += (f'<path d="M{f1(x + (dx + 8) * s)},{f1(y - 3 * s)} L{f1(x + (dx + 8) * s)},{f1(y - 36 * s)}" '
                  f'stroke="{edge}" stroke-width="3" stroke-linecap="round"/>')
        d += (f'<path d="M{f1(x + 8 * s)},{f1(y - 36 * s)} L{f1(x + 34 * s)},{f1(y - 40 * s)}" stroke="{edge}" '
              f'stroke-width="6" stroke-linecap="round"/>')
    glow = f'<circle cx="{f1(x + 8 * s)}" cy="{f1(y - 14 * s)}" r="{f1(30 * s)}" fill="#fff2c4" opacity="0.35"/>'
    return doc7(glow + d)


def peace_svg():
    """Screen layer: a soft rose-gold light lying over the hills and the little town."""
    gid = "peace"
    defs = S.rad_grad(gid, [(0, "#ffe6b8", 0.75), (0.55, "#f8d0a8", 0.4), (1, "#f8d0a8", 0)])
    return doc7(f'<ellipse cx="{f1(TOWN[0] + 520)}" cy="{f1(GY - 240)}" rx="1250" ry="250" fill="url(#{gid})"/>', defs)


def build(ctx):
    sc = Scene(ctx, W=W7, H=H7)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    rng = random.Random(8)

    t_hu = tm.at(0, "忽然")
    t_hao1 = tm.at(0, "好多")
    t_hao2 = tm.at(0, "好多", 2)
    t_ts = tm.at(0, "天使")
    t_zm = tm.at(0, "一起赞美")
    t_sing = ctx.lines[1].start
    t_ry = tm.at(1, "荣耀")
    t_pa = tm.at(1, "平安")
    t_sing_end = ctx.lines[1].end
    t_jss = tm.at(2, "就是说")
    t_tian = tm.at(2, "天上")
    t_zmsd = tm.at(2, "要赞美")
    t_di = tm.at(2, "地上")
    t_pa2 = tm.at(2, "平安")
    t_last = ctx.lines[2].end
    T0 = max(1.02, t_hu)            # nothing changes before the fade from s07 is over

    # ---- the sky opens: heaven_light behind the host (in front of the stars, behind the hills)
    t_h0, t_h1 = T0 + 0.05, T0 + 2.0
    open_k = lambda t: M.progress(t, t_h0, t_h1, "inout")

    # ---- the fields (as s07 ends: the glory and its light on the field are full; they soften as the sky opens)
    add_fields(sc, g0, glory_on=lambda t: 1 - 0.22 * open_k(t), field_on=lambda t: 1 - 0.3 * open_k(t))

    def heaven_fa(t):
        v = 0.12 + 0.88 * open_k(t)
        for i in range(len(HEAVEN_P) - 1):
            if HEAVEN_P[i] <= v <= HEAVEN_P[i + 1]:
                return i + (v - HEAVEN_P[i]) / (HEAVEN_P[i + 1] - HEAVEN_P[i])
        return len(HEAVEN_P) - 1.0
    bright = lambda t: (0.9 + 0.1 * math.sin(2 * math.pi * (t + g0) / 3.1) + 0.12 * env(t, t_ry - 0.1, t_ry + 1.4, 0.3, 1.0)
                        + 0.12 * env(t, t_pa - 0.1, t_pa + 1.4, 0.3, 1.0) + 0.1 * env(t, t_tian, t_di, 0.6, 0.8))
    sc.add("heaven", [heaven_svg(p) for p in HEAVEN_P], z=0.7, wc=0.5, frame_at=heaven_fa,
           motion=lambda t: Tf(alpha=min(1.0, open_k(t) * 6) * min(1.0, bright(t)) if t >= t_h0 else 0.0))

    # slowly turning soft rays in the opened sky, and twinkles in its light
    rays_svg = doc7(f'<path d="{S.rays(HEAVEN[0], HEAVEN[1], 120, 1150, n=16, width_deg=3.2)}" fill="#fff6d8" '
                    f'opacity="0.5" filter="url(#soft)"/>')
    sc.add("heaven_rays", rays_svg, z=0.75, wc=0, blend="screen", motion=lambda t: Tf(
        rot=2.2 * (t + g0) % 360, px=HEAVEN[0], py=HEAVEN[1],
        alpha=open_k(t) * 0.55 * (0.85 + 0.15 * math.sin(2 * math.pi * (t + g0) / 3.7))))
    sc.fx.append(gsparkles((HEAVEN[0] - 520, HEAVEN[1] - 300, HEAVEN[0] + 520, HEAVEN[1] + 260), g0, t0=t_h1 - 0.5,
                           count=26, color=(255, 252, 236), size=(8, 16), period=1.8, drift=0, seed=77))

    # ---- the host: three groups appear on '好多', '好多', '天使'; wings flutter and they bob gently
    appear_t = [t_hao1 - 0.05, t_hao2 - 0.05, t_ts - 0.05]
    for gi in range(3):
        x0, x1, y, n, s, rows, seed = GROUPS[gi]
        cx, cy = (x0 + x1) / 2, y - 120
        ta = appear_t[gi]
        per = 3.0 + 0.4 * gi

        def m(t, ta=ta, cx=cx, cy=cy, per=per, gi=gi):
            if t < ta:
                return Tf(alpha=0.0)
            u = M.progress(t, ta, ta + 0.7, "out")
            sk = 0.85 + 0.15 * u
            return Tf(alpha=M.progress(t, ta, ta + 0.5, "sine"), sx=sk, sy=sk, px=cx, py=cy,
                      dy=30 * (1 - u) + 7 * math.sin(2 * math.pi * ((t + g0) / per + 0.3 * gi)))
        sc.add(f"choir{gi}", [choir_svg(gi, k) for k in range(CHOIR_PH)], z=0.8 + 0.01 * gi, wc=0.8, seed=150 + gi,
               frame_at=lambda t, gi=gi: float(int((t + g0) / 0.2 + 2 * gi) % CHOIR_PH), motion=m)
        sc.fx.append(gsparkles((x0 - 40, y - 330, x1 + 40, y + 20), g0, t0=ta, t1=ta + 1.6, count=14,
                               color=(255, 244, 200), size=(9, 17), period=1.0, drift=-20, seed=60 + gi))
    # sparkle showers on '荣耀' and '平安', and over the host while they sing
    for k, tt in enumerate((t_ry, t_pa)):
        sc.fx.append(gsparkles((120, 380, 1990, 980), g0, t0=tt - 0.1, t1=tt + 2.0, count=40, color=(255, 240, 190),
                               size=(9, 20), period=1.1, drift=-24, seed=70 + k))
    sc.fx.append(gsparkles((100, 220, 2010, 1000), g0, t0=t_zm, count=24, color=(255, 248, 220), size=(6, 12),
                           period=2.1, drift=-8, seed=75))

    # little golden notes floating up from the host while they sing
    nrng = random.Random(9)
    for i in range(9):
        gx0, gx1, gy = GROUPS[i % 3][0], GROUPS[i % 3][1], GROUPS[i % 3][2]
        x = nrng.uniform(gx0 + 40, gx1 - 40)
        y = gy - nrng.uniform(140, 260)
        per = nrng.uniform(2.4, 3.2)
        ph = nrng.random()
        svg = note_svg(x, y, nrng.uniform(1.3, 1.7), i % 2)

        def nm(t, x=x, y=y, per=per, ph=ph):
            if t < t_zm:
                return Tf(alpha=0.0)
            u = ((t + g0) / per + ph) % 1.0
            a = math.sin(math.pi * u) * env(t, t_zm, t_sing_end + 1.2, 0.6, 1.0)
            return Tf(dx=18 * math.sin(2 * math.pi * u), dy=-120 * u, alpha=a, rot=10 * math.sin(2 * math.pi * u * 1.5),
                      px=x, py=y)
        sc.add(f"note{i}", svg, z=0.9 + 0.001 * i, wc=0, motion=nm)

    # ---- the peaceful light over the hills and the town ('地上…平安')
    peace = lambda t: M.progress(t, t_pa2 - 0.2, t_pa2 + 1.8, "inout")
    sc.add("peace", peace_svg(), z=1.06, wc=0, blend="screen", motion=lambda t: Tf(
        alpha=0.7 * peace(t) * (0.92 + 0.08 * math.sin(2 * math.pi * (t + g0) / 3.3))))
    sc.add("town_peace", doc7(f'<defs>{S.rad_grad("tpc", [(0, "#ffe8a8", 0.9), (1, "#ffe8a8", 0)])}</defs>'
                              f'<ellipse cx="{f1(TOWN[0])}" cy="{f1(TOWN[1] - 70)}" rx="260" ry="120" '
                              f'fill="url(#tpc)"/>'), z=1.07, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=peace(t) * (0.8 + 0.2 * math.sin(2 * math.pi * (t + g0) / 2.1))))
    sc.fx.append(gsparkles((TOWN[0] - 260, TOWN[1] - 240, TOWN[0] + 900, GY - 60), g0, t0=t_pa2, count=18,
                           color=(255, 236, 196), size=(6, 12), period=1.7, drift=6, seed=78))

    # ---- the sheep and the dog look up at the sky
    for i, (x, y, f, v, pose) in enumerate(SHEEP_IN):
        a = Fig(f"sheep_in{i}", sheep_in_draw(i), (x, y), SK, 4 + y / 10000, g0, seed=80 + i)
        a.cut(0, FINAL["sheep_in"])
        a.mots.append(breath((x, y), g0, 2.6 + 0.3 * i, 0.02, 0.3 * i))
        a.build(sc)
    for i, (x, y, f, v, pose) in enumerate(SHEEP_OUT):
        hx, hy = HUDDLE[i]
        a = Fig(f"sheep_out{i}", sheep_out_draw(i), (x, y), SK, zorder(max(y, hy)), g0, seed=90 + i)
        a.cut(0, FINAL["sheep_out"])
        if i in (1, 3):
            a.cut(t_ts + 0.3 + 0.3 * i, "look_up|h|1", depth=4)
        a.mots.append(breath((x, y), g0, 2.4 + 0.2 * i, 0.02, 0.5 * i))
        a.build(sc)
    dg = Fig("dog", dog_draw, DOG0, SK, zorder(DOG0[1]), g0, seed=SEED["dog"])
    dg.cut(0, FINAL["dog"])
    dg.cut(t_hao2 + 0.3, "look_up|open", depth=4)
    dg.mots.append(breath(DOG0, g0, 2.2, 0.02))
    dg.build(sc)

    # ---- the shepherds kneel and look up
    def fig(key):
        piv = SHEP[key][1:]
        return Fig(key, shep_draw(key), piv, K, zorder(piv[1]), g0, seed=SEED[key])

    old = fig("old")
    old.cut(0, FINAL["old"])
    old.add_blinks({FINAL["old"]: "kneel|" + blink("awed") + "|1|a|"}, 1.3, T, rng)
    old.mots.append(breath(SHEP["old"][1:], g0, 3.4, 0.014, 0.1))
    old.build(sc)

    bd = fig("beard")
    bd.cut(0, FINAL["beard"])
    bd.cut(t_hao2 + 0.15, "kneel|awed|1|a|", depth=8)
    bd.add_blinks({FINAL["beard"]: "stand|" + blink("awed") + "|1|a|",
                   "kneel|awed|1|a|": "kneel|" + blink("awed") + "|1|a|"}, 1.3, T, rng)
    bd.mots.append(breath(SHEP["beard"][1:], g0, 3.0, 0.012, 0.4))
    bd.build(sc)

    # the boy sets his lamb down beside him and looks up with it
    xb, yb = SHEP["boy"][1:]
    by = fig("boy")
    by.cut(0, FINAL["boy"])
    t_set = t_ts + 0.25
    by.cut(t_set, "look_up|amazed|1|a|", depth=8)
    by.cut(t_sing + 0.4, "look_up|happy|1|a|", dip=False)
    by.add_blinks({"look_up|amazed|1|a|": "look_up|" + blink("amazed") + "|1|a|",
                   "look_up|happy|1|a|": "look_up|" + blink("happy") + "|1|a|"}, t_set + 0.4, T, rng)
    by.mots.append(breath((xb, yb), g0, 2.6, 0.014, 0.7))
    by.build(sc)
    lx, ly = xb + 70, yb + 12
    lamb = Fig("lamb_up", lambda n: sheep_markup(lx, ly, -1, 3, n, lamb=True), (lx, ly), SK, zorder(ly), g0,
               seed=SEED["lamb"])
    lamb.cut(0, "stand")
    lamb.cut(t_set + 0.6, "look_up", depth=4)
    lamb.mots += [lambda t: Tf(alpha=1.0 if t >= snap(t_set) else 0.0), breath((lx, ly), g0, 2.0, 0.025)]
    lamb.build(sc)

    # the young shepherd points up at the host, later kneels too
    yn = Fig("young", shep_draw("young"), YOUNG_WATCH, K, zorder(YOUNG_WATCH[1] + 12), g0, seed=SEED["young"])
    yn.cut(0, FINAL["young"])
    yn.cut(t_hao1 + 0.1, "point_up|amazed|1|w|", depth=7)
    yn.cut(t_zm + 0.2, "kneel|awed|1|w|", depth=8)
    yn.add_blinks({"kneel|awed|1|w|": "kneel|" + blink("awed") + "|1|w|"}, t_zm + 0.6, T, rng)
    yn.mots.append(breath(YOUNG_WATCH, g0, 3.2, 0.012, 0.2))
    yn.build(sc)
    add_crook(sc)

    st = Fig("sturdy", shep_draw("sturdy"), STURDY_REST, K, zorder(STURDY_REST[1]), g0, seed=SEED["sturdy"])
    st.cut(0, FINAL["sturdy"])
    st.cut(t_ts + 0.5, "kneel|joyful|1|r|", dip=False)
    st.cut(t_last + 0.2, "kneel|awed|1|r|", dip=False)
    st.add_blinks({FINAL["sturdy"]: "kneel|" + blink("awed") + "|1|r|"}, 1.3, T, rng)
    st.mots.append(breath(STURDY_REST, g0, 3.1, 0.012, 0.6))
    st.build(sc)

    # ---- the angel by the shepherds: the vision goes back into its hand, then it rises and sings with the host
    ax, ay = ANGEL
    an = Fig("angel", angel_draw, (ax, ay - LIFT), K, zorder(ay) + 0.001, g0, seed=SEED["angel"],
             loops={s: ANGEL_LOOP for s in (FINAL["angel"], "sing|sing", "wings_open|joyful")})
    an.cut(0, FINAL["angel"])
    an.cut(t_hao2 + 0.4, "wings_open|joyful", depth=5)
    an.cut(t_zm - 0.05, "sing|sing", depth=5)
    rise = lambda t: Tf(dy=-60 * M.progress(t, t_zm - 0.2, t_zm + 2.2, "inout"))
    an.mots += [angel_bob(g0), rise]
    an.build(sc)
    sc.add("angel_shadow", doc7(C.ground_shadow(ax, ay, K, 170, 0.25, color="#fff3c0")), z=zorder(ay) - 0.01, wc=0,
           motion=lambda t: Tf(alpha=1 - 0.4 * M.progress(t, t_zm - 0.2, t_zm + 2.2, "inout")))
    add_bubble(sc, g0, -100.0, t_out=T0 + 0.02)

    # ---- the glory sparkles round the group continue from s07
    sc.fx.append(gsparkles((GLORY[0] - 700, GLORY[1] - 900, GLORY[0] + 700, GLORY[1] - 60), g0, count=26,
                           color=(255, 246, 214), size=(7, 14), period=1.9, drift=0, seed=41))

    # ---- camera: s07's framing, up and wide to the opening sky, up to the host on '天上', down on '地上'
    wide = Cam(1056, 1090, 2112)
    sc.camera = cam_path([
        (0.0, CAM0), (T0 + 0.1, CAM0), (t_ts + 0.9, wide), (t_jss - 0.6, Cam(1056, 1080, 2100)),
        (t_tian + 0.75, Cam(1056, 566, 1840)), (t_di - 0.7, Cam(1056, 560, 1840)), (t_di + 2.0, Cam(980, 1200, 1840)),
        (T, Cam(990, 1205, 1820))],
        ["linear", "sine", "sine", "sine", "linear", "sine", "sine"])

    # ---- sound
    sc.sfx("night", 0, dur=T + 0.5, gain_db=-19, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0, dur=T + 0.5, gain_db=-21, fade_in=0.8, fade_out=1.0, pan=-0.15)
    sc.sfx("chime", T0 + 0.05, gain_db=-11)
    sc.sfx("grow", T0 + 0.1, gain_db=-16)
    for k, ta in enumerate(appear_t):
        sc.sfx("sparkle", ta, gain_db=-15 - k, pan=(0.0, -0.5, 0.5)[k])
    sc.sfx("sheep", t_ts + 0.9, gain_db=-21, pan=0.55)
    sc.sfx("cloth", t_hao2 + 0.15, gain_db=-21, pan=-0.3)
    sc.sfx("cloth", t_zm + 0.2, gain_db=-21, pan=0.2)
    sc.sfx("sparkle", t_ry, gain_db=-15)
    sc.sfx("chime", t_pa, gain_db=-17)
    sc.sfx("sparkle", t_tian, gain_db=-18)
    sc.sfx("chime", t_pa2, gain_db=-17, pan=-0.4)
    return sc
