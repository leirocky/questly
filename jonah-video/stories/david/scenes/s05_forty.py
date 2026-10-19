"""Scene 5 — forty days (1 Samuel 17:16): morning and evening Goliath comes out and shouts; nobody from Israel dares.

The valley of Elah stage of s03 (shared helpers from s03_valley). Goliath (small, same scale as the soldiers) comes
out from behind the right hill onto the valley floor and shouts toward Israel's hill; the sky changes between
morning and evening (smooth colour blends), the sun and a crescent moon swap; a picture-book day counter card
(props.day_counter, 4 rows of 10 sun/moon days) fills up to 40.

Beats (keyed to the narration chunks; positions inside a chunk are fractions measured on the current take):
  start        dawn: the sun rises over the far ridges, a rooster crows, Israel's soldiers stand on their hill
  line 0       "第二天早上，" morning light; Goliath's spear tip appears behind the right hill, he strides out
               (planted-foot strides, thud each step)
               "歌利亚又来喊。" -> he shouts (spear raised, sound arcs); the Israelites duck behind their shields
               "到了晚上，" -> the sky blends to evening, the sun sets, the moon rises, stars twinkle (crickets)
               "他又来喊。" -> he shouts again
  line 1       "早上喊，" -> morning again (the day counter card pops in, first sun fills)
               "晚上喊，" -> evening (first moon fills)
               "一连喊了四十天。" -> days fly by: the counter fills quickly while the sky swaps morning / evening
               at most ~2.7 times a second (smooth blends, no strobing); Goliath keeps shouting; on "四十天" the
               counter reaches 40 with a pop, sparkles and a chime
  line 2       morning; the card slides away and the camera pushes in on Israel's hill: the soldiers cower and
               tremble; one soldier peeks up over his shield, Goliath shouts, and he ducks back down with a squash
               (the comic beat: pop sfx) - "一个敢出来的都没有"
  end          calm hold on the trembling soldiers (page dip to s06)
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import cuts, snap, step_walk
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s03_valley as V

INK = P["ink"]
SW, SH, FS = V.SW, V.SH, V.FS
GOL_Y = 1190                      # Goliath's ground line on the valley floor (in front of the hills' feet)
GOL_X0, GOL_X1 = 2150, 1640       # behind the right hill -> his shouting spot
SUN = (1060, 360)                  # sun position at full morning
MOON = (2030, 300)                # moon position at full evening
CARD = (640, 420)                 # day counter card centre (stage px)
ROWS, PER_ROW, CARD_S = 4, 10, 0.5


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def in_chunk(line, phrase, frac):
    for c in line.chunks:
        if phrase in c.text:
            return c.start + frac * (c.end - c.start)
    raise KeyError(phrase)


def smooth(u):
    u = min(1.0, max(0.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


# ================================================================== drawings


def stars_svg():
    import random
    rng = random.Random(7)
    b = ""
    for _ in range(40):
        x, y = rng.uniform(0, SW), rng.uniform(30, 560)
        r = rng.uniform(3, 7)
        b += (f'<path d="M{x:.0f},{y - r * 2:.0f} L{x + r * 0.5:.0f},{y - r * 0.5:.0f} L{x + r * 2:.0f},{y:.0f} '
              f'L{x + r * 0.5:.0f},{y + r * 0.5:.0f} L{x:.0f},{y + r * 2:.0f} L{x - r * 0.5:.0f},{y + r * 0.5:.0f} '
              f'L{x - r * 2:.0f},{y:.0f} L{x - r * 0.5:.0f},{y - r * 0.5:.0f} Z" fill="#fff4cf" opacity="0.9"/>')
    return doc(b)


def sun_svg():
    x, y = SUN
    defs = (S.rad_grad("f5sun", [(0, "#fff3bf"), (0.6, P["sun"]), (1, "#f5bb4f")], cx=0.45, cy=0.42) +
            S.rad_grad("f5sg", [(0, "#fff6d6", 0.9), (0.35, "#fff0c0", 0.45), (1, "#fff0c0", 0)]))
    b = f'<circle cx="{x}" cy="{y}" r="330" fill="url(#f5sg)"/>'
    b += S.g(f'<circle cx="{x}" cy="{y}" r="74" fill="url(#f5sun)" stroke="{INK}" stroke-width="3.5"/>'
             f'<circle cx="{x - 22}" cy="{y - 24}" r="17" fill="#fff8dc" opacity="0.6"/>', filter="wobble")
    return doc(b, defs)


def moon_svg():
    x, y = MOON
    defs = S.rad_grad("f5mg", [(0, "#fdf3d0", 0.6), (0.4, "#f5e7c0", 0.25), (1, "#f5e7c0", 0)])
    d = (f"M{x + 10},{y - 66} A66,66 0 1 0 {x + 10},{y + 66} A52,58 0 1 1 {x + 10},{y - 66} Z")
    b = f'<circle cx="{x - 20}" cy="{y}" r="240" fill="url(#f5mg)"/>'
    b += S.g(f'<path d="{d}" fill="#fbefc4" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<circle cx="{x - 34}" cy="{y + 20}" r="7" fill="#efdca6"/><circle cx="{x - 44}" cy="{y - 18}" r="5" '
             f'fill="#efdca6"/>', filter="wobble")
    return doc(b, defs)


def eve_tint_svg():
    """Evening light for the land (multiply): transparent in the sky, warm violet over the hills."""
    defs = (f'<linearGradient id="f5et" gradientUnits="userSpaceOnUse" x1="0" y1="380" x2="0" y2="{SH}">'
            f'<stop offset="0" stop-color="#b6889e" stop-opacity="0"/>'
            f'<stop offset="0.25" stop-color="#b6889e" stop-opacity="0.75"/>'
            f'<stop offset="1" stop-color="#8a76a6" stop-opacity="0.9"/></linearGradient>')
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#f5et)"/>', defs)


def card_svg(filled):
    """The day-counter card: a cream page with 4 rows of 10 days, and the number of days."""
    cx, cy = CARD
    gap = 64
    row_w = ((PER_ROW - 1) * gap + 40) * CARD_S
    row_h = 128 * CARD_S
    w, h = row_w + 70, ROWS * row_h + 130
    x0, y0 = cx - w / 2, cy - h / 2
    b = (f'<rect x="{x0 + 8}" y="{y0 + 10}" width="{w}" height="{h}" rx="22" fill="{INK}" opacity="0.18"/>'
         f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="22" fill="#fbf2dc" stroke="{INK}" stroke-width="4"/>'
         f'<rect x="{x0 + 12}" y="{y0 + 12}" width="{w - 24}" height="{h - 24}" rx="14" fill="none" '
         f'stroke="#e2c58f" stroke-width="3" stroke-dasharray="10 8"/>')
    b = S.g(b, filter="wobble-fine")
    for r in range(ROWS):
        f = min(PER_ROW, max(0.0, filled - r * PER_ROW))
        b += PR.day_counter(cx, y0 + 112 + r * row_h, CARD_S, n=PER_ROW, filled=f, icons="pair", gap=gap)
    n = int(math.ceil(filled - 1e-6))
    col = "#c9572e" if n >= 40 else INK
    b += (f'<text x="{cx}" y="{y0 + 68}" font-family="LXGW WenKai" font-weight="bold" font-size="54" fill="{col}" '
          f'text-anchor="middle">第 {max(1, n)} 天</text>') if n > 0 else ""
    return doc(b)


def goliath_svg(pose):
    sh = C.ground_shadow(GOL_X0, GOL_Y + 2, FS * 1.6, 150, 0.22)
    return doc(sh + C.goliath(GOL_X0, GOL_Y, FS, -1, pose=pose))


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines

    # --- key times
    t_go = 0.45                                    # Goliath starts out from behind the hill
    t_sh1 = in_chunk(L0, "第二天早上", 0.77)        # "喊"
    t_eve1 = L0.at("到了晚上")
    t_sh2 = in_chunk(L0, "到了晚上", 0.66)          # "他又来喊"
    t_m2 = L1.start - 0.1                          # 早上喊
    t_e2 = in_chunk(L1, "早上喊", 0.31)             # 晚上喊
    t_run = in_chunk(L1, "早上喊", 0.54)            # 一连喊了
    t_40 = in_chunk(L1, "早上喊", 0.86)             # 四十天
    t_card = L1.start - 0.35
    t_card_out = L2.start - 0.2
    t_peek = in_chunk(L2, "可是", 0.5)
    t_shout3 = in_chunk(L2, "可是", 0.72)
    t_duck = t_shout3 + 0.18

    # evening amount e(t): 0 = morning, 1 = evening
    cyc0 = t_run
    period = 0.75
    n_cyc = max(1, round((t_40 - cyc0) / period))
    cyc1 = cyc0 + n_cyc * period

    def e_of(t):
        if t < t_eve1:
            return 0.0
        if t < t_m2 - 0.3:
            return smooth((t - t_eve1) / 0.9)
        if t < t_e2 - 0.25:
            return 1 - smooth((t - (t_m2 - 0.3)) / 0.6)
        if t < cyc0:
            return smooth((t - (t_e2 - 0.25)) / 0.55)
        if t < cyc1:
            return 0.5 + 0.5 * math.cos(2 * math.pi * (t - cyc0) / period)
        return 1 - smooth((t - cyc1) / 0.65)

    def fast(t):          # 0 for the slow day/night changes, 1 during the quick montage
        return smooth((t - cyc0 + 0.3) / 0.4) * (1 - smooth((t - cyc1) / 0.4))

    # --- sky
    sc.add("sky_dawn", V.sky_svg("dawn"), wc=0.6)
    sc.add("sky_day", V.sky_svg("morning"), wc=0.6,
           motion=lambda t: Tf(alpha=smooth((t - 0.2) / 2.2) if t < t_eve1 else 1.0))
    sc.add("sky_eve", V.sky_svg("evening"), wc=0.6, motion=lambda t: Tf(alpha=e_of(t)))
    sc.add("stars", stars_svg(), wc=0, motion=lambda t: Tf(alpha=max(0.0, e_of(t) - 0.35) / 0.65 *
                                                          (0.8 + 0.2 * math.sin(t * 3.1))))

    def sun_m(t):
        rise = 330 * (1 - smooth((t - 0.0) / 2.6))
        amp = 420 - 300 * fast(t)
        e = e_of(t)
        return Tf(dy=rise + amp * e, alpha=1 - fast(t) * e)
    sc.add("sun", sun_svg(), wc=0.3, motion=sun_m)

    def moon_m(t):
        e = e_of(t)
        amp = 380 - 260 * fast(t)
        return Tf(dy=amp * (1 - e), alpha=min(1.0, e * 1.6) if t > t_eve1 else 0.0)
    sc.add("moon", moon_svg(), wc=0.3, motion=moon_m)
    sc.add("clouds", V.clouds_svg(), motion=lambda t: Tf(dx=9 * t, alpha=1 - 0.75 * e_of(t)))
    sc.add("clouds_eve", V.clouds_svg("#f3c9c4", "#c99ab0"), motion=lambda t: Tf(dx=9 * t, alpha=0.75 * e_of(t)))
    sc.add("valley", V.valley_svg())

    # --- Goliath walks out from behind the right hill (drawn behind the hill layer's slope via clip: the hills
    # are part of valley_svg, so he is masked by a copy of the right hill drawn over him, see 'hill_mask')
    n_steps = 5
    step = (GOL_X0 - GOL_X1) / n_steps
    w_fa, w_dx, w_dy, t_walk_end = step_walk(t_go, n_steps, step, 0.36, FS * 2)
    gol_frames = [goliath_svg(p) for p in ("stride_a", "stride_b", "stand", "shout")]
    shouts = [(t_sh1, t_eve1 + 0.25), (t_sh2, t_m2 + 0.1), (t_m2 + 0.15, t_e2 - 0.1), (t_e2, cyc0),
              (cyc0, t_40 + 0.8), (t_shout3, T + 1)]

    def g_frame(t):
        f = w_fa(t)
        if f is not None:
            return f
        if t < t_walk_end:
            return 0.0
        for a, b in shouts:
            if snap(a) <= t < snap(b):
                return 3.0
        return 2.0

    def g_motion(t):
        x = GOL_X0 - w_dx(t)
        dy = w_dy(t)
        sy = 1.0
        # squash-dips hide the pose cuts; a bounce on every shout beat
        beats = [a for a, _ in shouts] + [b for _, b in shouts[:4]]
        beats += [cyc0 + k * period / 2 for k in range(1, int((t_40 + 0.8 - cyc0) / (period / 2)))]
        for tb in beats:
            u = t - snap(tb)
            if -0.1 <= u < 0.3:
                k = math.sin(math.pi * (u + 0.1) / 0.4)
                dy += 7 * FS * k
                sy *= 1 - 0.035 * k
        dy += 2 * math.sin(2 * math.pi * t / 2.4)
        return Tf(dx=x - GOL_X0, dy=dy, sy=sy, px=GOL_X0, py=GOL_Y)
    sc.add("goliath", gol_frames, frame_at=g_frame, motion=g_motion, seed=31)
    sc.add("hill_mask", hill_mask_svg(), wc=1.0)

    # --- the camps (tents with waving flags) and the soldiers
    sc.add("tents", [V.tents_svg(w) for w in (0.0, 0.33, 0.66)], frame_at=lambda t: float(int(t / 0.24) % 3))
    t_duckall = t_sh1 + 0.05
    peeker = 4                                  # the front soldier, nearest the valley
    for i, x in enumerate(V.ISR_MEN):
        y = V.ground(x) + 6
        frames = [V.soldier_svg(x, "israel", i, "stand", expr="worried")]
        frames += [V.soldier_svg(x, "israel", i, "cower", shake=k) for k in (0.0, 0.25, 0.5, 0.75)]
        if i == peeker:
            frames.append(V.soldier_svg(x, "israel", i, "cower", expr="surprised", shake=0.0))
        td = snap(t_duckall + 0.06 * i)

        def fa(t, td=td, i=i):
            if t < td:
                return 0.0
            if i == peeker and snap(t_peek + 0.15) <= t < snap(t_duck):
                return 5.0
            calm = i == peeker and t_peek - 0.1 <= t < t_duck
            if calm:
                return 1.0
            rate = 13 if (t_duck <= t < t_duck + 1.2 and i == peeker) else 9
            return 1.0 + float(int(t * rate + i) % 4)

        def mot(t, td=td, x=x, y=y, i=i):
            u = t - td
            dy, sy = 0.0, 1.0
            if 0 <= u < 0.3:
                k = math.sin(math.pi * u / 0.3)
                dy, sy = 8 * FS * k, 1 - 0.05 * k
            if i == peeker:
                # rises slowly to peek over the shield, then ducks back fast with a squash
                up = 30 * FS * smooth((t - t_peek) / 0.45) * (1 - M.progress(t, t_duck, t_duck + 0.12, "in"))
                dy -= up
                w = t - (t_duck + 0.12)
                if 0 <= w < 0.35:
                    k = math.sin(math.pi * w / 0.35)
                    dy += 9 * FS * k
                    sy *= 1 - 0.09 * k
            return Tf(dy=dy, sy=sy, px=x, py=y)
        sc.add(f"israel{i}", frames, frame_at=fa, motion=mot, seed=50 + i)
    for i, x in enumerate(V.PHI_MEN):
        y = V.ground(x) + 6
        frames = [V.soldier_svg(x, "philistine", i, "stand", expr="sneer"),
                  V.soldier_svg(x, "philistine", i, "cheer")]
        cheer = [(t_sh1 + 0.2 + 0.05 * i, t_sh1 + 1.0 + 0.05 * i), (t_40 + 0.1 + 0.05 * i, t_40 + 0.9 + 0.05 * i)]

        def fa(t, cheer=cheer):
            return 1.0 if any(snap(a) <= t < snap(b) for a, b in cheer) else 0.0
        sc.add(f"phil{i}", frames, frame_at=fa, seed=70 + i,
               motion=M.combine(M.breathe(0.015, 2.5, pivot=(x, y), phase=i * 0.19),
                                V.hop_m([snap(a) for a, _ in cheer], FS, 8, (x, y))))

    sc.add("eve_tint", eve_tint_svg(), wc=0, blend="multiply", motion=lambda t: Tf(alpha=0.55 * e_of(t)))
    sc.add("tufts", [V.tufts_svg(k) for k in range(3)], frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.55) % 4]))

    # --- the day counter card (81 states: 0, 0.5 ... 40 days)
    def fill(t):
        if t < t_m2 + 0.05:
            return 0.0
        if t < t_e2 + 0.05:
            return 0.5
        if t < cyc0 + 0.1:
            return 1.0
        u = M.progress(t, cyc0 + 0.1, t_40, lambda v: v ** 1.5)
        return round((1 + 39 * u) * 2) / 2
    sc.add("card", [card_svg(k / 2) for k in range(81)], wc=0.3, frame_at=lambda t: fill(t) * 2,
           motion=card_motion(t_card, t_40, t_card_out))

    # --- camera: wide on the valley; push in on Israel's hill for line 2
    sc.camera = M.cam_keys([
        (0.0, Cam(1480, 770, 2380)),
        (t_sh1, Cam(1470, 780, 2280)),
        (t_card_out, Cam(1420, 780, 2260)),
        (t_peek - 0.2, Cam(1010, 742, 1620)),
        (T, Cam(990, 745, 1590)),
    ], "sine")

    cx, cy = CARD
    sc.fx = [
        FX.sparkles((cx - 220, cy - 180, cx + 220, cy + 190), count=12, t0=t_40, t1=t_40 + 1.6,
                    color=(255, 238, 180), size=(9, 18), period=1.0, drift=-10, seed=41),
        FX.motes((0, 500, SW, 1300), count=18, color=(255, 246, 214), size=(2, 5), alpha=90, seed=42),
    ]

    # --- sound
    sc.sfx("rooster", 0.25, gain_db=-15, pan=-0.3)
    sc.sfx("birds", 0, dur=t_eve1 + 0.4, gain_db=-20, fade_in=0.6, fade_out=0.6)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("night", t_eve1 + 0.2, dur=t_m2 - t_eve1, gain_db=-19, fade_in=0.5, fade_out=0.5)
    for k in range(n_steps):
        sc.sfx("thud", snap(t_go + k * 0.36), gain_db=-15, pan=0.3)
    sc.sfx("whoosh", cyc0, gain_db=-20)
    sc.sfx("whoosh", cyc0 + 2 * period, gain_db=-21)
    sc.sfx("pop", t_card + 0.05, gain_db=-18)
    sc.sfx("chime", t_40, gain_db=-11)
    sc.sfx("sparkle", t_40 + 0.1, gain_db=-16)
    sc.sfx("pop", t_duck + 0.1, gain_db=-14, pan=-0.4)
    return sc


def card_motion(t_in, t_40, t_out):
    cx, cy = CARD

    def m(t):
        if t < t_in or t > t_out + 0.6:
            return Tf(alpha=0)
        u = M.progress(t, t_in, t_in + 0.45, "linear")
        s = 0.6 + 0.4 * M.ease("back")(u)
        w = t - t_40
        if 0 <= w < 0.45:
            s *= 1 + 0.08 * math.sin(math.pi * w / 0.45)
        v = M.progress(t, t_out, t_out + 0.55, "in")
        return Tf(dy=-260 * v + 3 * math.sin(2 * math.pi * t / 3.0), rot=-2.0 + 1.0 * math.sin(t * 0.8),
                  sx=s, sy=s, alpha=min(1.0, (t - t_in) / 0.15) * (1 - v), px=cx, py=cy)
    return m


def hill_mask_svg():
    """The right hill's inner slope drawn again over Goliath (so he walks out from behind it): the hills part of
    valley_elah, clipped to the region right of the valley mouth."""
    clip = f'<clipPath id="f5hm"><rect x="1650" y="0" width="{V.VX1 + 0.04 * (V.VX1 - V.VX0) - 45 - 1650:.0f}" height="{SH}"/></clipPath>'
    return doc(clip + S.g(PR.valley_elah(V.VX0, V.VX1, V.VY, V.VS, part="hills", camps=False),
                          extra='clip-path="url(#f5hm)"'))
