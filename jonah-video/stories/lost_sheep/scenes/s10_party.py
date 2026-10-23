"""Scene 10 - Luke 15:6. Home in the shepherd's village at night: he knocks on his neighbours' doors with the lamb on his
shoulders, the doors open onto warm light, everybody comes out with lamps and lanterns; then (a hard cut at the
phrase boundary) the party in the little square: festival string lanterns, a table of food, three musicians (lyre,
tambourine, flute), neighbours dancing and clapping round the shepherd with the lamb in the middle, nuzzling him.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers through s08's Beats; nothing
hard-coded to the take). Times are for the current take:
  0 .. 0.9      calm page (the page-dip from s09 lands here): the lantern-lit street, the shepherd with the lamb on his
                shoulders between the houses; lanterns flicker, stars twinkle, clouds drift
  '回到家' 1.00  he walks to the first door (planted-foot walk, the lamb on his shoulders)
  '牧羊人' 1.94  he knocks (knock, two knocks, wooden knocks)
  '朋友' 2.73   the door opens onto warm light: his friend stands in the doorway with a little clay lamp; the shepherd
                hops back happily
  '邻居' 3.48   the next door opens: a neighbour comes out holding up a lantern and steps over
  '都请来' 4.02  a child (with a lantern) and an old man (with his stick) come along the street
  '和我一起高兴吧' 5.59 (H) he cheers, arms up (cheer, the lamb on his shoulders)
  '我丢的那只羊' 7.31 he lifts the lamb up to show it (lift); '找到了' 8.79 everybody cheers (sparkles, a happy crowd)
  '大家都好开心' 10.24  cut to the party: string lanterns, the table, the musicians playing (little notes), neighbours
                dancing and clapping; the shepherd dances with the lamb on his shoulders
  '一起唱歌' 12.14  some sing (arms open), the shepherd sings with the lamb nuzzling his cheek (a heart)
  '一起庆祝' 13.33  arms up all round (cheer)
  end           calm-ish: everyone claps gently, the lamb nuzzles the shepherd (a heart), the lanterns sway
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
    CARRY_FRAMES, NIGHT, SH, SW, Beats, Fig, ShoulderLamb, Track, blink_expr, breath, cam_path, cloud_markup, doc, f1,
    flicker, gfx, moon_markup, shep_key, snap, walk_x)
from stories.lost_sheep.scenes.s09_found import float_up, heart_markup

INK = "#4b3426"
S10 = 0.8                       # people scale
HSC = 0.86                      # village_house scale
GYV = 1000                      # the house fronts' base line (village_house anchor y)
TINTV = (0.86, 0.88, 0.96)      # a lighter night tint: the village is lantern-lit
MOON10 = (2470, 330)

# houses along the street: x, variant
XD, XE = 230, 1250              # the party square between D and E (part 2)
XA, XB, XC = 1730, 2270, 2810   # the doors he knocks at (part 1)
HOUSES = [(XD, 1), (XE, 3), (XA, 0), (XB, 2), (XC, 3)]


def tintv(markup):
    r, g_, b = TINTV
    return (f'<defs><filter id="ntintv" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'<feColorMatrix type="matrix" values="{r} 0 0 0 0  0 {g_} 0 0 0  0 0 {b} 0 0  0 0 0 1 0"/></filter></defs>'
            f'<g filter="url(#ntintv)">{markup}</g>')


def shadow(x, y, s, w=150, op=0.24):
    return C.ground_shadow(x, y, s, w, op, color="#2a2a40")


# ------------------------------------------------------------------ backdrop
def sky_svg():
    return doc(PR.spring_sky(-10, -10, SW + 10, GYV - 250, time=NIGHT, moon=None, clouds=0, stars=1.0, seed=51))


def village_back_svg():
    return doc(PR.shepherd_village(-60, SW + 60, GYV - 10, 1.0, time=NIGHT, part="back", seed=7))


def street_svg():
    pal = PR._ls_pal(NIGHT)
    ground = S.mix(PR._lt("#d8bf94", NIGHT, 0.8), pal["near"], 0.15)
    gid = "s10street"
    defs = S.lin_grad(gid, [(0, S.shade(ground, 0.05)), (1, S.shade(ground, -0.2))])
    b = f'<rect x="-20" y="{GYV - 26}" width="{SW + 40}" height="{SH - GYV + 60}" fill="url(#{gid})"/>'
    rng = random.Random(4)
    d = ""
    for i in range(110):
        px, py = rng.uniform(0, SW), rng.uniform(GYV + 10, SH - 10)
        d += f"M{f1(px)},{f1(py)} l{f1(rng.uniform(8, 20))},0 "
    b += f'<path d="{d}" stroke="{S.shade(ground, -0.32)}" stroke-width="2.6" opacity="0.5" stroke-linecap="round"/>'
    for i in range(26):
        px, py = rng.uniform(0, SW), rng.uniform(GYV + 60, SH - 20)
        r = rng.uniform(7, 15)
        b += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r * 1.4)}" ry="{f1(r * 0.75)}" fill="{S.shade(ground, -0.12)}" '
              f'stroke="{INK}" stroke-width="2.4"/>')
    return doc(S.g(b, filter="wobble"), defs)


def house_svg(x, variant, door):
    return doc(PR.village_house(x, GYV, HSC, 1, variant=variant, door=door, lit=1.0, time=NIGHT, seed=3))


def glow_pool_svg(x, y, rx, ry, k=0.6, key="p"):
    gid = f"s10pool{key}"
    defs = S.rad_grad(gid, [(0, "#ffd890", 0.75 * k), (0.45, "#f6a43c", 0.28 * k), (1, "#f6a43c", 0)])
    return doc(f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>', defs)


# ------------------------------------------------------------------ people
def person(name, draw, ref, z, g0, seed, track=None, loops=None):
    return Fig(name, draw, ref, z, g0, seed=seed, loops=loops, track=track)


def nb_draw(ref, kind, variant, item=None, s=S10, wsh=130):
    """Draw function for a neighbour Fig: key = (pose, facing, expr, phase, item)."""
    x, y = ref

    def d(key, k=None):
        pose, f, expr, phase, it = key
        if k is not None:
            phase = k / 4.0 if pose in ("clap", "wave") else (0.25 if k % 2 == 0 else 0.75)
        return shadow(x, y, s, wsh) + tintv(C.neighbour(x, y, s, f, kind=kind, variant=variant, pose=pose, expr=expr,
                                                         phase=phase, item=it))
    return d


def mus_draw(ref, instrument, variant, s=S10):
    x, y = ref

    def d(key, k=None):
        pose, f, expr, phase = key
        if k is not None:
            phase = k / 4.0
        return shadow(x, y, s, 130) + tintv(C.musician(x, y, s, f, instrument=instrument, variant=variant, pose=pose,
                                                        expr=expr, phase=phase))
    return d


def nkey(pose, f=1, expr=None, phase=0.0, item=None):
    return (pose, f, expr, round(phase, 3), item)


def walk_nb(fig, tr, t0, t1, x0, x1, y, keyf, step=84 * S10, period=0.26):
    """Neighbour planted-foot walk: walk_a / walk_b flip on each cut, the anchor advancing one step."""
    f = 1 if x1 >= x0 else -1
    n = max(2, int(round(abs(x1 - x0) / step)))
    per = (t1 - t0) / n if t1 > t0 else period
    x = x0
    for i in range(n):
        tk = snap(t0 + i * per)
        fig.cut(tk, keyf("walk_a" if i % 2 == 0 else "walk_b"), dip=False)
        x = x0 + (x1 - x0) * (i + 1) / n
        tr.to(tk - 0.04, tk + 0.08, x, y, None)
    return snap(t0 + n * per)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(10)

    t_hdj = bt.at(0, "回到家")
    t_my = bt.at(0, "牧羊人")
    t_py = bt.at(0, "朋友")
    t_lj = bt.at(0, "邻居")
    t_dqd = bt.at(0, "都请来")
    t_l0_end = bt.end(0, "牧羊人把朋友和邻居都请来")
    t_gx = bt.at(1, "和我一起高兴吧")
    t_wd = bt.at(1, "我丢的那只羊")
    t_zdl = bt.at(1, "找到了")
    t_zdl_end = bt.end(1, "找到了")
    t_dj = bt.at(2, "大家都好开心")
    t_cg = bt.at(2, "一起唱歌")
    t_qz = bt.at(2, "一起庆祝")
    t_qz_end = bt.end(2, "一起庆祝")
    t_cut = snap((t_zdl_end + t_dj) / 2 - 0.05)
    g1 = lambda t: 1.0 if t < t_cut else 0.0           # part 1 (the doors)
    g2 = lambda t: 1.0 if t >= t_cut else 0.0          # part 2 (the party)

    # ---------------------------------------------------------------- backdrop (shared by both parts)
    sc.add("sky", sky_svg(), z=0, seed=601)
    sc.add("moonglow", doc(moon_markup(*MOON10, 70, glow=1.0, disc=False)), z=0.1, wc=0)
    sc.add("moon", doc(moon_markup(*MOON10, 70, glow=0.0, disc=True)), z=0.12, seed=603)
    tw_rng = random.Random(5)
    for j in range(3):
        b = ""
        for _ in range(8):
            x, y, r = tw_rng.uniform(0, SW), tw_rng.uniform(0, GYV - 480), tw_rng.uniform(6, 11)
            w = r * 0.22
            pts = [(x, y - r), (x + w, y - w), (x + r, y), (x + w, y + w), (x, y + r), (x - w, y + w), (x - r, y), (x - w, y - w)]
            b += f'<path d="M{" L".join(f"{f1(a)},{f1(c)}" for a, c in pts)} Z" fill="#fbf6e2"/>'
        sc.add(f"twinkle{j}", doc(b), z=0.05 + 0.001 * j, wc=0,
               motion=lambda t, j=j: Tf(alpha=0.25 + 0.75 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t + g0) / (2.3 + 0.6 * j) + j / 3)))))
    for i, (cx, cy, w, v) in enumerate(((420, 210, 300, 5.0), (1250, 140, 260, 3.5), (2050, 230, 280, 4.5),
                                        (2850, 160, 240, 4.0))):
        sc.add(f"cloud{i}", doc(cloud_markup(cx, cy, w, seed=71 + 2 * i)), z=0.2, seed=605 + i,
               motion=lambda t, v=v: Tf(dx=v * (t + g0 - 180.0)))
    sc.add("village_back", village_back_svg(), z=1, seed=611)
    sc.add("street", street_svg(), z=1.5, seed=613)
    # the houses; doors A and B open (5-frame flipbooks)
    t_dA = snap(t_py - 0.08)
    t_dB = snap(t_lj - 0.08)
    doors = (0.0, 0.25, 0.5, 0.75, 1.0)
    for x, v in HOUSES:
        if x in (XA, XB):
            t_d = t_dA if x == XA else t_dB
            sc.add(f"house{x}", [house_svg(x, v, d) for d in doors], z=2 + x / 10000, seed=620 + v,
                   frame_at=lambda t, t_d=t_d: float(min(4, max(0, int((t - t_d) / 0.07) + 1))) if t >= t_d else 0.0)
            sc.add(f"doorpool{x}", glow_pool_svg(x, GYV + 50, 260, 80, 1.0, key=str(x)), z=2.5, wc=0, blend="screen",
                   motion=lambda t, t_d=t_d: Tf(alpha=M.progress(t, t_d, t_d + 0.5, "sine") * flicker(g0, 0.92, 0.08, x)(t)))
        else:
            sc.add(f"house{x}", house_svg(x, v, 0.0), z=2 + x / 10000, seed=620 + v)
        # every house's lantern by the door makes a soft pool on the street
        lx = x - 100 * HSC
        sc.add(f"lpool{x}", glow_pool_svg(lx, GYV + 30, 200, 60, 0.7, key=f"l{x}"), z=2.4, wc=0, blend="screen",
               motion=lambda t, x=x: Tf(alpha=flicker(g0, 0.9, 0.1, x * 0.01)(t)))

    # ---------------------------------------------------------------- part 1: knocking at the doors
    z1 = 10.0
    y_sh = GYV + 6 * S10
    x_knock = XA + 160 * S10
    x_start = x_knock + 210
    tr = Track(x_start, y_sh)
    ref1 = (x_knock, y_sh)

    def sh_draw(key):
        pose, f, expr, phase, lamb, eyes, crook, marks, lantern = key
        m = C.parable_shepherd(ref1[0], ref1[1], S10, f, pose=pose, expr=expr, phase=phase, crook=crook, lantern=lantern,
                               glow=0.6, lamb=lamb, lamb_eyes=eyes, marks=marks)
        return shadow(ref1[0], ref1[1], S10, 170) + tintv(m)
    sh = Fig("shep1", sh_draw, ref1, z1 + 3, g0, seed=641, track=tr,
             loops={shep_key("knock", -1, "happy", 0.0, lantern=True): (4, 0.085)})
    base_sh_draw = sh.draw
    sh.draw = lambda key, k=None: base_sh_draw(key if k is None else key[:3] + (k / 4.0,) + key[4:])
    key_cs = shep_key("carry_stand", -1, "joyful", eyes="happy")
    sh.cut(0, key_cs)
    t_w0 = snap(max(0.85, t_hdj - 0.3))
    t_arr = walk_x(sh, tr, t_w0, t_my - 0.3, x_start, x_knock,
                   lambda fr: shep_key(fr, -1, "joyful", eyes="happy"), y=y_sh, start=2, frames=CARRY_FRAMES, s=S10)
    sh.cut(t_my - 0.12, shep_key("carry_stand", -1, "happy", eyes="happy"), dip=False)
    key_knock = shep_key("knock", -1, "happy", 0.0)
    t_kn = snap(t_my + 0.02)
    sh.cut(t_kn, key_knock, depth=4)
    t_kn_end = snap(t_kn + 0.68)
    sh.cut(t_kn_end, shep_key("knock", -1, "happy", 0.0, marks=False), dip=False)
    # from here his lantern stays where the knock pose set it down (a separate little lantern on the street)
    lx_g, ly_g = x_knock + 92 * S10, y_sh - 68 * S10
    # the door opens: a happy little hop back
    t_hop = snap(t_dA + 0.22)
    sh.cut(t_hop, shep_key("carry_stand", -1, "joyful", eyes="happy", lantern=False), depth=8)
    tr.to(t_hop, t_hop + 0.34, x_knock + 95, y_sh + 8, None, lift=22, curve="linear")
    t_ch = snap(t_gx - 0.1)
    sh.cut(t_ch, shep_key("cheer", 1, "joyful", lamb=True, eyes="happy", lantern=False), depth=8)
    t_show = snap(t_wd - 0.1)
    sh.cut(t_show, shep_key("lift", 1, "joyful", 1.0, lantern=False), depth=8)
    sh.cut(t_zdl + 0.1, shep_key("lift", 1, "laugh", 1.0, lantern=False), dip=False)
    sh.blinks({key_cs: shep_key("carry_stand", -1, blink_expr("joyful"), eyes="happy")}, 0.2, t_w0, rng)
    sh.mots.append(breath(ref1, g0, 3.0, 0.012))
    sh.alpha = g1
    sh.build(sc)
    sc.add("lantern_down", doc(tintv(PR.ls_lantern(lx_g, ly_g, 0.9 * S10, lit=1.0, glow=True))), z=z1 + 2.9, seed=645,
           motion=lambda t: Tf(alpha=(1.0 if t >= t_hop else 0.0) * g1(t)))
    sc.add("lantern_pool", glow_pool_svg(lx_g, y_sh + 10, 230, 60, 0.8, key="ld"), z=2.6, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(1.0 if t >= t_kn else 0.0) * g1(t) * flicker(g0, 0.9, 0.1, 1.7)(t)))

    # friend A in the doorway (a lamp), friend B with a lantern, then a child and an old man
    yA = GYV + 2
    nA = person("nA", nb_draw((XA, yA), "man", 0), (XA, yA), z1 + 1, g0, 651)
    nA.cut(0, nkey("open_door", 1, "surprised", item="lamp"))
    nA.cut(t_dA + 0.55, nkey("open_door", 1, "happy", item="lamp"), dip=False)
    nA.cut(t_gx + 0.4, nkey("laugh", 1, None, item="lamp"), depth=5)
    nA.cut(t_zdl - 0.02, nkey("cheer", 1, "joyful"), depth=7)
    nA.mots.append(breath((XA, yA), g0, 2.8, 0.012, 0.3))
    nA.alpha = lambda t: M.progress(t, t_dA + 0.04, t_dA + 0.3, "sine") * g1(t)
    nA.build(sc)

    yB = GYV + 2
    xB2, yB2 = XB - 190, GYV + 70
    trB = Track(XB, yB)
    nB = person("nB", nb_draw((XB, yB), "woman", 1), (XB, yB), z1 + 2, g0, 653, track=trB)
    nB.cut(0, nkey("open_door", -1, "surprised", item="lantern"))
    t_out = snap(t_dB + 0.5)
    walk_nb(nB, trB, t_out, t_out + 0.52, XB, xB2, yB2, lambda fr: nkey(fr, -1, "happy", item="lantern"))
    nB.cut(t_out + 0.55, nkey("hold_lantern", -1, "happy"), depth=4)
    nB.cut(t_zdl - 0.02, nkey("cheer", -1, "joyful"), depth=7)
    nB.mots.append(breath((XB, yB), g0, 2.6, 0.012, 0.6))
    nB.alpha = lambda t: M.progress(t, t_dB + 0.04, t_dB + 0.3, "sine") * g1(t)
    nB.build(sc)

    yK = GYV + 104
    trK = Track(SW + 120, yK)
    nK = person("nK", nb_draw((XB + 150, yK), "child", 0, wsh=100), (XB + 150, yK), z1 + 5, g0, 655, track=trK)
    nK.cut(0, nkey("walk_a", -1, "happy", item="lantern"))
    t_k0 = snap(t_dqd - 0.35)
    walk_nb(nK, trK, t_k0, t_k0 + 1.25, SW + 120, XB + 150, yK, lambda fr: nkey(fr, -1, "happy", item="lantern"),
            step=50 * S10 * 1.6)
    nK.cut(t_k0 + 1.3, nkey("hold_lantern", -1, "happy"), depth=4)
    nK.cut(t_zdl - 0.02, nkey("cheer", -1, "joyful"), depth=6)
    nK.mots.append(breath((XB + 150, yK), g0, 2.2, 0.015, 0.2))
    nK.alpha = g1
    nK.build(sc)

    yE = GYV + 60
    xE2 = XB + 330
    trE = Track(SW + 160, yE)
    nE = person("nE", nb_draw((xE2, yE), "elder", 0), (xE2, yE), z1 + 2.5, g0, 657, track=trE)
    nE.cut(0, nkey("walk_a", -1, "happy"))
    t_e0 = snap(t_dqd - 0.1)
    walk_nb(nE, trE, t_e0, t_e0 + 1.5, SW + 160, xE2, yE, lambda fr: nkey(fr, -1, "happy"))
    nE.cut(t_e0 + 1.55, nkey("stand", -1, "happy"), depth=4)
    nE.cut(t_zdl - 0.02, nkey("clap", -1, "joyful"), depth=5)
    nE.loops = {nkey("clap", -1, "joyful"): (4, 0.11)}
    nE.mots.append(breath((xE2, yE), g0, 3.2, 0.012, 0.8))
    nE.alpha = g1
    nE.build(sc)

    # '找到了': sparkles over everyone
    sp1 = gfx(FX.sparkles, g0, t0=t_zdl - 0.05, t1=t_cut + 0.1, rect=(XA - 100, GYV - 520, XB + 400, GYV - 160), count=22,
              color=(255, 232, 170), size=(8, 15), period=1.1, drift=-20, seed=81)
    sc.fx.append(lambda frame, t, view: sp1(frame, t, view) if t < t_cut else frame)

    # ---------------------------------------------------------------- part 2: the party in the square
    z2 = 20.0
    # festival string lanterns (4-frame sway) and the party table
    strings = [(XD + 150, GYV - 330, XE - 120, GYV - 345, 7, 70), (XD - 260, GYV - 420, XD + 160, GYV - 330, 4, 40),
               (XE - 120, GYV - 345, XE + 300, GYV - 430, 4, 40)]
    sl_frames = [doc("".join(PR.string_lanterns(a, b, c, d, n=n, sag=sg, glow=1.0, phase=k / 4, scale=1.0)
                             for a, b, c, d, n, sg in strings)) for k in range(4)]
    sc.add("strings", sl_frames, z=z2 + 0.5, seed=661, frame_at=lambda t: float(int((t + g0) / 0.32) % 4),
           motion=lambda t: Tf(alpha=g2(t)))
    sc.add("strings_pool", glow_pool_svg((XD + XE) / 2, GYV + 70, 720, 150, 0.9, key="sq"), z=z2 + 0.6, wc=0,
           blend="screen", motion=lambda t: Tf(alpha=g2(t) * flicker(g0, 0.9, 0.08, 3.3)(t)))
    xT, yT = XE + 200, GYV + 22
    sc.add("table", doc(tintv(PR.party_table(xT, yT, S10 * 1.05, 1, width=480)) + shadow(xT, yT, S10, 560, 0.2)),
           z=z2 + 1, seed=663, motion=lambda t: Tf(alpha=g2(t)))

    def loop_fig(name, draw, ref, z, seed, key, n=4, per=0.12, track=None):
        f = person(name, draw, ref, z, g0, seed, track=track, loops={key: (n, per)})
        f.cut(0, key)
        return f

    # the musicians on the left
    m_lyre = loop_fig("m_lyre", mus_draw((330, GYV + 30), "lyre", 0), (330, GYV + 30), z2 + 2, 671,
                      ("play", 1, None, 0.0), per=0.12)
    m_tamb = loop_fig("m_tamb", mus_draw((150, GYV + 110), "tambourine", 1), (150, GYV + 110), z2 + 4, 673,
                      ("play", 1, None, 0.0), per=0.11)
    m_flute = loop_fig("m_flute", mus_draw((470, GYV + 115), "flute", 2), (470, GYV + 115), z2 + 3.5, 675,
                       ("play", 1, None, 0.0), per=0.13)
    for f in (m_lyre, m_tamb, m_flute):
        f.mots.append(breath(f.ref, g0, 2.4, 0.014))
        f.alpha = g2
        f.build(sc)

    # neighbours round the shepherd
    def party_nb(name, kind, variant, ref, z, seed, plan, item=None, wsh=130):
        """plan: [(t, pose, facing, expr)] - loops for clap / dance."""
        fig = person(name, nb_draw(ref, kind, variant, wsh=wsh), ref, z, g0, seed)
        loops = {}
        for i, (tk, pose, f, expr) in enumerate(plan):
            key = nkey(pose, f, expr, item=item if pose not in ("cheer", "clap", "dance", "sing") else None)
            if pose in ("clap", "dance"):
                loops[key] = (4 if pose == "clap" else 2, 0.12 if pose == "clap" else 0.3)
            fig.cut(tk, key, dip=i > 0, depth=5)
        fig.loops = loops
        fig.mots.append(breath(ref, g0, 2.7, 0.012, seed * 0.1))
        fig.alpha = g2
        fig.build(sc)
        return fig

    cz = lambda y: z2 + 2 + (y - GYV) / 100
    t_c2 = t_cut
    party_nb("p_man", "man", 0, (660, GYV + 20), cz(GYV + 20), 681,
             [(t_c2, "clap", 1, "joyful"), (t_cg - 0.05, "sing", 1, None), (t_qz - 0.05, "cheer", 1, "joyful"),
              (t_qz_end + 0.25, "clap", 1, "joyful")])
    party_nb("p_wom", "woman", 1, (1110, GYV + 30), cz(GYV + 30), 683,
             [(t_c2, "dance", -1, "joyful"), (t_cg - 0.02, "sing", -1, None), (t_qz - 0.02, "cheer", -1, "joyful"),
              (t_qz_end + 0.3, "clap", -1, "joyful")])
    party_nb("p_kid", "child", 0, (1140, GYV + 118), cz(GYV + 118), 685,
             [(t_c2, "dance", -1, "joyful"), (t_qz - 0.04, "cheer", -1, "joyful"), (t_qz_end + 0.35, "dance", -1, "joyful")],
             wsh=100)
    party_nb("p_eld", "elder", 0, (1300, GYV + 100), cz(GYV + 100), 687,
             [(t_c2, "clap", -1, "joyful"), (t_cg + 0.1, "sing", -1, None), (t_qz, "cheer", -1, "joyful"),
              (t_qz_end + 0.3, "clap", -1, "joyful")])
    party_nb("p_wom2", "woman", 4, (640, GYV + 140), cz(GYV + 140), 689,
             [(t_c2, "dance", 1, "joyful"), (t_qz - 0.03, "cheer", 1, "joyful"), (t_qz_end + 0.3, "clap", 1, "joyful")])

    # the shepherd in the middle with the lamb on his shoulders, in a warm glow
    ref2 = (870, GYV + 80)
    gid = "s10mid"
    defs = S.rad_grad(gid, [(0, "#fff0c4", 0.7), (0.4, "#ffd27a", 0.3), (1, "#f6a43c", 0)])
    sc.add("mid_glow", doc(f'<ellipse cx="{ref2[0]}" cy="{ref2[1] - 150}" rx="330" ry="300" fill="url(#{gid})"/>', defs),
           z=cz(ref2[1]) - 0.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=g2(t) * (0.55 + 0.1 * math.sin(2 * math.pi * (t + g0) / 1.9))))
    ff2 = gfx(FX.motes, g0, rect=(0, GYV - 500, 1700, GYV + 100), count=18, color=(255, 226, 150), size=(3, 6),
              seed=83, alpha=140)
    sc.fx.append(lambda frame, t, view: ff2(frame, t, view) if t >= t_cut else frame)
    tr2 = Track(*ref2)

    def sh2_draw(key):
        pose, f, expr, phase, lamb, eyes, crook, marks, lantern = key
        m = C.parable_shepherd(ref2[0], ref2[1], S10, f, pose=pose, expr=expr, phase=phase, crook=crook, lantern=lantern,
                               glow=0.6, lamb=lamb, lamb_eyes=eyes, marks=marks)
        return shadow(ref2[0], ref2[1], S10, 170) + tintv(m)
    key_dance = shep_key("dance", 1, "joyful", 0.0, lamb=True, eyes="happy", lantern=False)
    sh2 = Fig("shep2", sh2_draw, ref2, cz(ref2[1]), g0, seed=691, track=tr2, loops={key_dance: (2, 0.3)})
    base2 = sh2.draw
    sh2.draw = lambda key, k=None: base2(key if k is None else key[:3] + (0.25 + 0.5 * (k % 2),) + key[4:])
    sh2.cut(0, key_dance)
    key_sing = shep_key("carry_stand", 1, "cheery", lamb=False, eyes="happy", lantern=False)
    sh2.cut(t_cg - 0.08, key_sing, depth=6)
    sh2.cut(t_qz - 0.06, shep_key("cheer", 1, "joyful", lamb=True, eyes="happy", lantern=False), depth=7)
    key_end = shep_key("carry_stand", 1, "warm", lamb=False, eyes="happy", lantern=False)
    t_settle = snap(t_qz_end + 0.25)
    sh2.cut(t_settle, key_end, depth=6)
    sh2.blinks({key_end: shep_key("carry_stand", 1, blink_expr("warm"), lamb=False, eyes="happy", lantern=False)},
               t_settle + 0.3, T - 0.2, rng)
    sh2.mots.append(breath(ref2, g0, 3.0, 0.012))
    sh2.alpha = g2
    t_nz = [t_cg + 0.35, t_cg + 1.0, t_settle + 0.35, t_settle + 1.2]
    sl = ShoulderLamb(sh2, S10, g0, cz(ref2[1]) + 0.01, 693, nuzzle_t=t_nz, tint=tintv, name="lamb_front2")
    sl.finish(sc)
    for i, tn in enumerate(t_nz[1::2]):
        h_t = tn + 0.15
        hx, hy = sl.head_point(h_t)
        sc.add(f"heart{i}", doc(heart_markup(hx, hy, 16)), z=cz(ref2[1]) + 0.02, wc=0,
               motion=float_up(h_t, (hx, hy), 1.5, 120))

    # ---------------------------------------------------------------- camera
    cam1a = Cam(XA + 370, 720, 1640)
    cam1b = Cam(XA + 470, 730, 1600)
    cam2a = Cam(830, 745, 1680)
    cam2b = Cam(850, 760, 1560)
    c1 = cam_path([(0.0, cam1a), (t_hdj - 0.3, cam1a), (t_my + 0.3, Cam(XA + 330, 725, 1580)),
                   (t_dqd + 0.4, cam1b), (t_cut, Cam(XA + 450, 720, 1640))], ["linear", "sine", "inout", "sine"])
    c2 = cam_path([(t_cut, cam2a), (T, cam2b)], ["sine"])
    sc.camera = lambda t: c1(t) if t < t_cut else c2(t)

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=t_cut + 0.6, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("footsteps", t_w0, dur=t_arr - t_w0 + 0.2, gain_db=-22, pan=0.3)
    sc.sfx("hammer", t_kn, dur=0.75, gain_db=-14, pan=-0.1, fade_out=0.15)
    sc.sfx("cloth", t_dA, gain_db=-17, pan=-0.2)
    sc.sfx("cloth", t_dB, gain_db=-18, pan=0.3)
    sc.sfx("footsteps", t_k0, dur=1.6, gain_db=-23, pan=0.6)
    sc.sfx("cheer", t_zdl - 0.1, dur=T - t_zdl + 0.6, gain_db=-17, fade_in=0.5, fade_out=1.0)
    sc.sfx("sparkle", t_zdl, gain_db=-16, pan=0.1)
    return sc
