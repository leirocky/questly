"""Scene 10 - Zacchaeus's changed heart (a light picture of his promise, Luke 19:8; nothing beyond it). The palm grove
and balsam gardens of Jericho in the golden evening (props.jericho_sky + palm_grove, time 'evening'). One calm shot:
the farmer works under the palms on the left, the widow stands by the path, children play in the grove on the right.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers through the Lost Sheep film's
Beats; nothing is hard-coded to the take). Times are for the current take:
  0 .. 0.3      calm page (the paper dip from s09 lands here): Zacchaeus at the left of the path, the grove at sunset
  0.3 .. ~3.1   '撒该心里好开心' 0.96: he walks happily along the path (planted-foot walk, a little lift in every
                step; no strut), his money pouch small and light now; on '开心' 2.33 a happy little skip
  '他' 3.27      he stops by the widow and holds out coins (give, tender); she cups her hands (receive)
  '钱' 4.46      the coin hops into her hands (coins); she thanks him with a little bow (thank)
                meanwhile the farmer turns from his palms and walks over (two planted steps)
  '因为' 5.57    Zacchaeus turns to the farmer and holds out four coins (pay_back) - he pays him back
  '耶稣' 6.24    the coins pass into the farmer's hands (coins); he beams (delighted)
  '爱' 6.69      a warm little heart rises over Zacchaeus (sparkle)
  '他也开始爱别人了' 7.44  the children wave and cheer; Zacchaeus turns and waves back; on '爱别人' 8.2 little hearts
                rise over the widow, the farmer and the children
  end           Zacchaeus laughs, everyone smiles in the golden light: a calm last frame for the page turn
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
from stories.lost_sheep.scenes.s08_search import Beats, Track, blink_expr, gfx
from stories.noah.scenes.s01_title import heart_markup, snap
from stories.zacchaeus.scenes.s08_promise import Fig, breath, f1

INK = S.INK
W10, H10 = 2112, 1188
YG = 1000                            # the near path, where the people stand
EVE = 1.0                            # props time: the golden evening
SUN = (1590, 610)
GS = 0.8                             # the grove's scale (the palms ~1.6 adults, the sky shows above them)
X_Z = 1082                           # Zacchaeus stops here
X_W = X_Z + 218                      # the widow (jericho_poor receive / give recipe)
X_F = X_Z - 160                      # the farmer when paid (pay_back recipe)
F_START = (673, YG - 38, 0.965)      # the farmer at work further back (3 planted steps of 86 * ~0.975 to X_F)
KIDS = [(1440, YG - 80, 0.88, 0), (1566, YG - 122, 0.84, 1), (1676, YG - 70, 0.89, 2)]
ZAC_FRAMES = ("walk_a", "walk_c", "walk_b", "walk_c")
ZAC_ADV = (22.8, 20.8, 47.2, 45.3)  # planted-foot advance INTO frame i of the cycle (scale 1), from zacchaeus_points
FARMER_STEP = 86.0                   # jericho_folk walk_a <-> walk_b
CAM0 = Cam(1000, 762, 1490)
CAM1 = Cam(1012, 776, 1430)

WARM = ('<filter id="z10warm" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="1.02 0 0 0 0.01  0 0.96 0 0 0  0 0 0.86 0 0  0 0 0 1 0"/></filter>'
        '<filter id="z10gold" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="1.04 0.02 0 0 0.035  0 1.0 0 0 0.012  0 0 0.8 0 0  0 0 0 1 0"/></filter>')


def golden(markup):
    """The backdrop graded toward the golden evening light (baked into the static layers)."""
    return f'<g filter="url(#z10gold)">{markup}</g>'


def doc(body, defs=""):
    return S.svg_doc(body, WARM + defs, W10, H10)


def warm(markup):
    return f'<g filter="url(#z10warm)">{markup}</g>'


# ------------------------------------------------------------------ backdrop
def sky_svg():
    b = PR.jericho_sky(0, 0, W10, YG - 300 * GS, time=EVE, sun=SUN, clouds=0.9, birds=0, seed=4)
    gid = "z10sun"
    b += (f'<defs>{S.rad_grad(gid, [(0, "#fff0c0", 0.7), (0.4, "#ffc878", 0.25), (1, "#ffb060", 0)])}</defs>'
          f'<ellipse cx="{SUN[0]}" cy="{SUN[1]}" rx="700" ry="420" fill="url(#{gid})"/>')
    return doc(golden(b))


def grove_svg(part, sway=0.0):
    return doc(golden(PR.palm_grove(-40, W10 + 40, YG, GS, time=EVE, part=part, seed=7, sway=sway)))


def front_bush_svg(x, y, k, seed, f=1):
    return doc(PR.balsam_bush(x, y, k, f, time=EVE, seed=seed))


def light_svg():
    """Low golden sunlight raking across the path from the right (a screen layer)."""
    gid = "z10rake"
    defs = S.lin_grad(gid, [(0, "#ffd890", 0), (0.55, "#ffd890", 0.22), (1, "#fff0c0", 0.42)], x1=0, y1=0, x2=1, y2=0)
    return doc(f'<path d="M0,{YG - 220} L{W10},{YG - 330} L{W10},{YG + 120} L0,{YG + 70} Z" fill="url(#{gid})" '
               f'filter="url(#blur-md)"/>', defs)


def sun_glow_svg():
    """The low sun's golden light flooding through the palms from the right (a screen layer above the grove)."""
    gid = "z10glow"
    defs = S.rad_grad(gid, [(0, "#fff2c4", 0.85), (0.3, "#ffd88a", 0.45), (0.7, "#ffb866", 0.12), (1, "#ffb866", 0)])
    return doc(f'<ellipse cx="{SUN[0]}" cy="{SUN[1]}" rx="820" ry="560" fill="url(#{gid})"/>', defs)


def long_shadow(x, y, k=1.0):
    """A long evening shadow stretching left, away from the low sun."""
    return (f'<ellipse cx="{f1(x - 95 * k)}" cy="{f1(y + 3 * k)}" rx="{f1(150 * k)}" ry="{f1(15 * k)}" fill="#5a3426" '
            f'opacity="0.2" filter="url(#soft)"/>')


def bird_svg(flap):
    k = 1.0
    if flap:
        d = "M-16,2 Q-8,-6 0,0 Q8,-6 16,2"
    else:
        d = "M-16,-8 Q-8,-2 0,0 Q8,-2 16,-8"
    return f'<path d="{d}" fill="none" stroke="#5a3a3a" stroke-width="{3.2 * k}" stroke-linecap="round" stroke-linejoin="round"/>'


# ------------------------------------------------------------------ people
def small_purse(x, y, s):
    """His money pouch, small and light now (drawn at the pouch's knot instead of the fat velvet one)."""
    col = C.ZAC_PURSE
    d = (f"M{f1(x - 4 * s)},{f1(y)} Q{f1(x - 13 * s)},{f1(y + 7 * s)} {f1(x - 10 * s)},{f1(y + 17 * s)} "
         f"Q{f1(x)},{f1(y + 24 * s)} {f1(x + 10 * s)},{f1(y + 17 * s)} Q{f1(x + 13 * s)},{f1(y + 7 * s)} {f1(x + 4 * s)},{f1(y)} Z")
    return (f'<g filter="url(#wobble-fine)"><path d="{d}" fill="{col}" stroke="{INK}" stroke-width="{3 * s:.1f}" '
            f'stroke-linejoin="round"/><path d="M{f1(x - 6 * s)},{f1(y + 2 * s)} L{f1(x + 6 * s)},{f1(y + 2 * s)}" '
            f'stroke="#e8b746" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>'
            f'<ellipse cx="{f1(x - 4 * s)}" cy="{f1(y + 11 * s)}" rx="{f1(2.4 * s)}" ry="{f1(3.6 * s)}" fill="#a07ab8" '
            f'opacity="0.8"/></g>')


def zac_key(pose, f=1, expr=None, phase=0.0, coins=True):
    return ("zac", pose, f, expr, round(phase, 3), coins)


def zac_draw(key):
    _, pose, f, expr, phase, coins = key
    x, y = X_Z, YG
    lift = 5 if pose == "walk_c" else 0
    b = long_shadow(x, y) + C.ground_shadow(x, y, 1.0, width=110, opacity=0.2)
    fig = C.zacchaeus(x, y - lift, 1.0, f, pose=pose, expr=expr, phase=phase, purse=False, coins=coins)
    px, py = C.zacchaeus_points(x, y - lift, 1.0, f, pose=pose, phase=phase)["purse"]
    return b + warm(fig + small_purse(px, py, 1.0))


def widow_key(pose, expr=None, phase=0.0):
    return ("widow", pose, expr, round(phase, 3))


def widow_draw(key):
    _, pose, expr, phase = key
    return long_shadow(X_W, YG) + C.ground_shadow(X_W, YG, 1.0, width=100, opacity=0.2) + \
        warm(C.jericho_poor(X_W, YG, 1.0, -1, kind="widow", pose=pose, expr=expr, phase=phase))


def farmer_key(pose, f=1, expr=None, phase=0.0, coins=True):
    return ("farmer", pose, f, expr, round(phase, 3), coins)


def farmer_draw(key):
    _, pose, f, expr, phase, coins = key
    item = None if pose == "receive" else "hoe"
    return long_shadow(X_F, YG) + C.ground_shadow(X_F, YG, 1.0, width=110, opacity=0.2) + \
        warm(C.jericho_folk(X_F, YG, 1.0, f, kind="farmer", pose=pose, expr=expr, phase=phase, item=item, coins=coins))


def kid_key(i, pose="smile", expr=None, phase=0.0):
    return ("kid", i, pose, expr, round(phase, 3))


def kid_draw(key):
    _, i, pose, expr, phase = key
    x, y, k, v = KIDS[i]
    return long_shadow(x, y, k * 0.8) + C.ground_shadow(x, y, k, width=80, opacity=0.18) + \
        warm(C.jericho_folk(x, y, k, -1, kind="child", variant=v, pose=pose, expr=expr, phase=phase))


def closed(key):
    """Closed-eye variant for blinks (None when the eyes are already shut or the pose is moving)."""
    if key is None:
        return None
    who = key[0]
    if who == "zac":
        _, pose, f, expr, phase, coins = key
        if pose.startswith("walk") or expr in (None, "overjoyed", "laugh", "grateful") or pose == "laugh":
            return None
        return zac_key(pose, f, blink_expr(expr), phase, coins)
    if who == "widow":
        _, pose, expr, phase = key
        if pose == "thank":
            return None
        return widow_key(pose, blink_expr(expr or ("kind" if pose == "stand" else "touched")), phase)
    if who == "farmer":
        _, pose, f, expr, phase, coins = key
        if pose.startswith("walk"):
            return None
        return farmer_key(pose, f, blink_expr(expr or "kind"), phase, coins)
    if who == "kid":
        _, i, pose, expr, phase = key
        if pose in ("wave", "cheer"):
            return None
        return kid_key(i, pose, blink_expr(expr or "happy"), phase)
    return None


def float_heart(t0, x, y, r, rise=80, dur=1.8):
    def m(t):
        if t < t0:
            return Tf(alpha=0.0)
        s = 0.4 + 0.6 * M.progress(t, t0, t0 + 0.32, "back")
        a = M.progress(t, t0, t0 + 0.15, "sine") * (1 - M.progress(t, t0 + dur * 0.65, t0 + dur, "sine"))
        return Tf(dy=-rise * M.progress(t, t0, t0 + dur, "out"), dx=5 * math.sin(2 * math.pi * (t - t0) / 1.3),
                  sx=s, sy=s, px=x, py=y, alpha=a)
    return m


def build(ctx):
    sc = Scene(ctx, W=W10, H=H10)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(10)

    # ---- beats
    t_kx = bt.at(0, "开心")
    t_ta = bt.at(0, "他不再")
    t_qian = bt.at(0, "钱")
    t_yw = bt.at(1, "因为")
    t_ys = bt.at(1, "耶稣")
    t_ai = bt.at(1, "爱他")
    t_ty = bt.at(1, "他也开始")
    t_ai2 = bt.at(1, "爱别人")
    t_end = bt.end(1, "他也开始爱别人了")

    # ---- backdrop
    sc.add("sky", sky_svg(), z=0, seed=3)
    sc.add("grove_back", grove_svg("back"), z=1, seed=5)
    # the palms stir in the evening breeze: three sway frames, cross-faded only between neighbours (small steps)
    sway = lambda t: 1.0 + math.sin(2 * math.pi * (t + 0.4) / 4.6)
    sc.add("grove_mid", [grove_svg("mid", -0.3), grove_svg("mid", 0.0), grove_svg("mid", 0.3)], z=2, seed=7,
           frame_at=sway)
    sc.add("sun_glow", sun_glow_svg(), z=2.6, wc=0, blend="screen", seed=10,
           motion=lambda t: Tf(alpha=0.62 + 0.06 * math.sin(2 * math.pi * t / 6.1)))
    sc.add("rake", light_svg(), z=2.5, wc=0, blend="screen", seed=9,
           motion=lambda t: Tf(alpha=0.85 + 0.15 * math.sin(2 * math.pi * t / 5.3)))
    for i, (bx, by, bk, bs, bf) in enumerate(((250, 1182, 1.45, 51, 1), (1790, 1190, 1.55, 52, -1))):
        sc.add(f"bush{i}", front_bush_svg(bx, by, bk, bs, bf), z=8, seed=11 + i,
               motion=M.sway(1.2, 3.8 + 0.7 * i, (bx, by), phase=0.3 * i))
    # birds: three swifts crossing the evening sky
    for i, (y0, vx, t0, sc_k) in enumerate(((330, 150, -1.0, 1.0), (260, 175, 1.5, 0.8), (410, 135, 4.0, 0.9))):
        bx0 = 300 + 200 * i
        frames = [doc(f'<g transform="translate({bx0},{y0}) scale({sc_k})">{bird_svg(fl)}</g>') for fl in (0, 1)]

        def bm(t, vx=vx, t0=t0, i=i):
            u = t - t0
            return Tf(dx=vx * u, dy=14 * math.sin(u * 1.7 + i), alpha=1.0 if u >= 0 else 0.0)
        sc.add(f"bird{i}", frames, z=0.5, wc=0, seed=13 + i, motion=bm,
               frame_at=lambda t, i=i: float(int((t + 0.07 * i) * 7) % 2))

    # ---- Zacchaeus: walks in, gives to the widow, pays the farmer back, waves to the children, laughs
    # he stands beaming, then walks a, c, b, c, a, c, b, c (planted feet: stand -> walk_a keeps the front foot, the
    # last walk_c -> give too) and stops by the widow
    n_walk = 8
    adv = [ZAC_ADV[i % 4] for i in range(1, n_walk)]
    x_stand = X_Z - (-22.0 + sum(adv) - 5.3)
    t_w1 = snap(t_ta - 0.3)
    t_w0 = snap(max(1.15, t_w1 - 0.24 * (n_walk - 1)))
    dt = (t_w1 - t_w0) / (n_walk - 1)
    zt = Track(X_Z, YG)
    zt.to(0, 0, x_stand, YG)
    z = Fig("zac", zac_draw, (X_Z, YG), 6.0, s=1.0, seed=41, track=zt, docf=doc)
    z.cut(0, zac_key("stand", 1, "happy"))
    x = x_stand - 22.0
    walk_ts = []
    for i in range(n_walk):
        tk = snap(t_w0 + dt * i)
        walk_ts.append(tk)
        z.cut(tk, zac_key(ZAC_FRAMES[i % 4], 1, "happy"), dip=False)
        if i:
            x += adv[i - 1]
        zt.to(tk, tk, x, YG)
    zt.to(snap(t_ta - 0.05), snap(t_ta - 0.05), X_Z, YG)
    t_skip = snap(t_kx)
    t_give = snap(max(t_ta - 0.05, walk_ts[-1] + 0.2))
    z.mots.append(M.keys([(0.85, {"dy": 0}), (1.0, {"dy": -10}), (1.16, {"dy": 0})], ["out", "in"]))
    z.cut(t_give, zac_key("give", 1, "tender", 0.0), depth=6)
    t_hop0 = snap(t_qian - 0.55)
    hop_ts = [snap(t_hop0 + (t_qian - t_hop0) * k / 5) for k in range(1, 6)]
    for k, tk in enumerate(hop_ts):
        z.cut(tk, zac_key("give", 1, "tender", (k + 1) / 5), dip=False)
    t_pay = snap(t_yw - 0.05)
    z.cut(t_pay, zac_key("pay_back", -1, "tender"), depth=7)
    t_hand = snap(t_ys)
    z.cut(t_hand, zac_key("pay_back", -1, "happy", coins=False), dip=False)
    t_wave = snap(t_ty + 0.3)
    t_laugh = snap(min(t_end + 0.2, T - 1.2))
    n_wv = int((t_laugh - t_wave) / 0.16)
    for k in range(n_wv):
        z.cut(t_wave + 0.16 * k, zac_key("wave", 1, "happy", (k % 4) / 4), dip=(k == 0))
    z.cut(t_laugh, zac_key("laugh", 1, "laugh"), depth=6)
    z.blinks(closed, 0.5, T - 1.1, rng)
    z.mots += [breath((X_Z, YG), g0, 2.8, 0.010),
               M.keys([(t_skip - 0.05, {"dy": 0}), (t_skip + 0.12, {"dy": -16}), (t_skip + 0.3, {"dy": 0})],
                      ["out", "in"])]
    z.build(sc)

    # ---- the widow
    w = Fig("widow", widow_draw, (X_W, YG), 5.5, s=1.0, seed=43, docf=doc)
    w.cut(0, widow_key("stand", "kind"))
    t_recv = snap(t_give + 0.18)
    w.cut(t_recv, widow_key("receive", "touched", 0.0), depth=5)
    w.cut(hop_ts[-1], widow_key("receive", "delighted", 1.0), dip=False)
    t_thank = snap(t_qian + 0.45)
    w.cut(t_thank, widow_key("thank", "grateful"), depth=6)
    t_wsm = snap(t_ty + 0.2)
    w.cut(t_wsm, widow_key("stand", "happy"), depth=4)
    w.blinks(closed, 0.6, T - 1.1, rng)
    w.mots.append(breath((X_W, YG), g0, 3.2, 0.010, 0.4))
    w.build(sc)

    # ---- the farmer: at work under the palms, turns, walks over, is paid back
    ft = Track(X_F, YG)
    fx0, fy0, fk0 = F_START
    ft.to(0, 0, fx0, fy0, fk0)
    f = Fig("farmer", farmer_draw, (X_F, YG), 4.5, s=1.0, seed=45, track=ft, docf=doc)
    f.cut(0, farmer_key("stand", -1, "kind"))
    t_turn = snap(t_qian + 0.06)
    f.cut(t_turn, farmer_key("walk_a", 1, "happy"), depth=4)
    x_arr = X_F + 3.0                                           # walk_b front foot (near, +20) stays planted into 'receive'
    steps = [(snap(t_turn + 0.26), "walk_b", 1 / 3), (snap(t_turn + 0.52), "walk_a", 2 / 3), (snap(t_turn + 0.78), "walk_b", 1.0)]
    for tk, fr, u in steps:
        f.cut(tk, farmer_key(fr, 1, "happy"), dip=False)
        ft.to(tk, tk, fx0 + (x_arr - fx0) * u, fy0 + (YG - fy0) * u, fk0 + (1 - fk0) * u)
    t_frecv = snap(max(t_pay + 0.1, steps[-1][0] + 0.25))
    ft.to(t_frecv, t_frecv, X_F, YG, 1.0)
    f.cut(t_frecv, farmer_key("receive", 1, "surprised", 0.0, coins=False), depth=5)
    f.cut(t_hand, farmer_key("receive", 1, "delighted", 1.0), dip=False)
    f.blinks(closed, 0.6, T - 1.1, rng)
    f.mots.append(breath((X_F, YG), g0, 3.0, 0.010, 0.2))
    f.build(sc)

    # ---- the children: playing quietly, then waving and cheering
    t_kw = snap(t_ty + 0.05)
    for i in range(3):
        kx, ky, kk, v = KIDS[i]
        kf = Fig(f"kid{i}", kid_draw, (kx, ky), 3.2 + 0.1 * i, s=kk, seed=51 + i, docf=doc)
        kf.cut(0, kid_key(i, "smile", "happy"))
        if i == 1:
            kf.cut(t_kw + 0.1, kid_key(i, "cheer", "laugh"), depth=8)
        else:
            n = int((t_laugh - t_kw) / 0.15)
            for k in range(n):
                kf.cut(t_kw + 0.07 * i + 0.15 * k, kid_key(i, "wave", None, ((k + i) % 4) / 4), dip=(k == 0))
        kf.cut(t_laugh + 0.06 * i, kid_key(i, "smile", "happy"), depth=5)     # still for the page turn
        kf.blinks(closed, 0.4, t_kw - 0.3, rng)
        kf.mots += [breath((kx, ky), g0, 2.4 + 0.2 * i, 0.012, 0.3 * i)]
        if i == 1:
            kf.mots.append(M.keys([(t_kw + 0.1, {"dy": 0}), (t_kw + 0.3, {"dy": -14}), (t_kw + 0.5, {"dy": 0}),
                                   (t_kw + 0.7, {"dy": -10}), (t_kw + 0.9, {"dy": 0})], ["out", "in", "out", "in"]))
        kf.build(sc)

    # ---- hearts: over Zacchaeus on '爱他', over the others on '爱别人'
    hz = (X_Z - 10, YG - 330)
    sc.add("heart_z", doc(heart_markup(*hz, 26, fill="#ef8f9a")), z=9, wc=0, motion=float_heart(snap(t_ai), *hz, 26))
    others = [(X_W - 6, YG - 360, 18), (X_F + 8, YG - 395, 18), (1590, YG - 330, 15)]
    for i, (hx, hy, hr) in enumerate(others):
        th = snap(t_ai2 + 0.2 * i)
        sc.add(f"heart{i}", doc(heart_markup(hx, hy, hr, fill="#f2a0a6")), z=9, wc=0,
               motion=float_heart(th, hx, hy, hr, rise=60, dur=1.6))

    # ---- light and air
    sc.fx.append(gfx(FX.motes, g0, rect=(250, 360, 1850, 1080), count=24, color=(255, 226, 150), size=(2.5, 5.5),
                     seed=101, alpha=140))
    sc.fx.append(FX.vignette(lambda t: 0.32, color=(80, 40, 30)))

    # ---- camera: a slow, gentle drift
    sc.camera = M.cam_keys([(0.0, CAM0), (T, CAM1)], "sine")

    # ---- sound
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-25, fade_in=0.8, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-27, fade_in=0.8, fade_out=1.0)
    sc.sfx("footsteps", walk_ts[0], dur=walk_ts[-1] - walk_ts[0] + 0.15, gain_db=-23, pan=-0.3)
    sc.sfx("coins", hop_ts[-1] - 0.05, gain_db=-15, pan=0.2)
    sc.sfx("footsteps", t_turn, dur=0.8, gain_db=-26, pan=-0.4)
    sc.sfx("coins", t_hand - 0.04, gain_db=-14, pan=-0.2)
    sc.sfx("sparkle", t_ai, gain_db=-18)
    sc.sfx("sparkle", t_ai2 + 0.15, gain_db=-20, pan=0.3)
    return sc
