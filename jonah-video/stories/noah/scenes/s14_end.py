"""Scene 14 — the closing page: a child (the listener, not Noah) after a rain shower, splashing in a puddle, sees a
rainbow and smiles; far away under the rainbow the ark and tiny animals rest on a green hill; God keeps his word
and remembers you; "which animal do you like best?" - a parade of animal pairs pops up; end card.

Beats (phrase onsets measured in the voice clip, see s01_title.voice_marks):
  start        calm frame, close on the child standing in a puddle (ripples), wet sparkles, clouds leaving
  '小朋友'      she jumps and lands in the puddle - splash!   '下次下完雨' a second, bigger splash
  '看见彩虹'    she looks up (smile_up), the camera lifts and widens, the rainbow sweeps in across the sky over the
               far hill where the little ark rests with its animals
  '想一想'      she points up at the rainbow
  line 1       '上帝说过的话，一定会做到' the rainbow brightens with twinkles; '上帝一直记得你' a warm glow grows
               round the child (hands clasped, smiling); '就像他记得挪亚一样' the far ark glows softly too
  line 2       '对了' she waves to us; '方舟里那么多动物' the animal pairs pop up one pair at a time on the
               meadow (pop + sparkle); '你最喜欢哪一种呢' a big bouncing '?' bubble; she cheers; the pause holds
               on the parade (breathing, hops, blinks)
  end          the '?' bubble pops away and the end card '挪亚方舟 · 完' fades in with a little heart (chime);
               calm final frame for the film's fade-out
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, cuts, dip, f1, heart_markup, snap, voice_marks

INK = P["ink"]
KID = (400, 1040, 1.45)
PUD = (410, 1046, 1.25)
RB = (1056, 830, 0.85)
ARK = (1056, 708, 0.13)
PARADE_Y, PARADE_S = 968, 0.55
# pair bboxes facing left at scale 1 (measured): pack them left to right after the child
PAIR_BOX = {"elephant": (-422, 225), "rabbit": (-110, 64), "turtle": (-181, 94), "duck": (-130, 67),
            "giraffe": (-308, 145), "lion": (-319, 181), "zebra": (-283, 145)}


def _pack(kinds, x0=505, gap=14):
    out, x = [], x0
    for k in kinds:
        l, r = PAIR_BOX[k]
        out.append((k, x - l * PARADE_S))
        x += (r - l) * PARADE_S + gap
    return out


PARADE = _pack(["elephant", "rabbit", "turtle", "duck", "giraffe", "lion", "zebra"])
END = (1056, 420)
QM = (1730, 540)


def doc(body, defs=""):
    return S.svg_doc(body, defs)


for _e in ("happy", "amazed"):
    C.EXPRS.setdefault(f"n14_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


# ================================================================== backdrop

def sky_svg():
    defs = (S.lin_grad("n14sky", [(0, "#88c3e0"), (0.5, "#b8deea"), (0.85, "#e3f0e4"), (1, "#f4eed6")]) +
            S.rad_grad("n14sun", [(0, "#fff7d6", 0.95), (0.4, "#fff0c2", 0.45), (1, "#fff0c2", 0)]))
    b = S.rect_bg("url(#n14sky)") + '<circle cx="1960" cy="90" r="460" fill="url(#n14sun)"/>'
    return doc(b, defs)


def clouds_svg():
    sh = "#d3e3ec"
    b = (S.cloud(300, 170, 300, 90, "#fbf6ec", seed=51, sw=3.5, shade_fill=sh) +
         S.cloud(1660, 120, 280, 84, "#fbf6ec", seed=52, sw=3.2, shade_fill=sh))
    b += S.cloud(-60, 380, 420, 130, "#b9c3d1", seed=54, sw=3.5, shade_fill="#9aa6b8")
    b += S.cloud(2180, 420, 380, 120, "#c3ccd8", seed=55, sw=3.5, shade_fill="#a4afbe")
    return doc(S.g(b, filter="wobble"))


def rainbow_svg():
    x, y, s = RB
    return doc(S.g(PR.rainbow(x, y, s), opacity=0.85))


def far_svg():
    b = S.path(S.hill(-200, W + 200, 800, 110, seed=61, bumps=5), fill="#b8d0c8", sw=2.2)
    trees = ""
    for x, y, s in ((230, 790, 0.28), (420, 800, 0.24), (1700, 792, 0.28), (1880, 800, 0.24)):
        trees += PR.olive_tree(x, y, s, seed=int(x))
    # the ark's hill under the rainbow
    d = S.smooth_path([(560, 860), (760, 780), (940, 722), (1056, 708), (1180, 716), (1360, 770), (1560, 860)],
                      closed=False) + " L1560,900 L560,900 Z"
    hill = S.path(d, fill="#9cc477", sw=3)
    hill += (f'<path d="M700,820 Q860,760 1000,734" stroke="#b6d68c" stroke-width="12" fill="none" '
             f'stroke-linecap="round" opacity="0.7"/>')
    deco = (PR.olive_tree(760, 800, 0.22, seed=3) + PR.bush(1300, 760, 0.3, variant=1) +
            PR.bush(880, 770, 0.26, variant=0) + PR.olive_tree(1420, 812, 0.2, seed=8))
    x, y, s = ARK
    ark = PR.ark(x, y, s, 1, door=1.0, window=1.0)
    tiny = (PR.animal_pair("elephant", x - 200, y + 18, s, 1) + PR.animal_pair("giraffe", x + 190, y + 12, s, -1) +
            PR.animal_pair("zebra", x + 290, y + 34, s, -1) + PR.animal_pair("sheep", x - 300, y + 40, s, 1))
    return doc(S.g(b, filter="wobble") + PR._haze(trees, "#cfe0d4", 0.4, 0.4) + S.g(hill, filter="wobble") +
               PR._haze(deco, "#d8e6dc", 0.2, 0.25) + PR._haze(ark + tiny, "#d8e6dc", 0.12, 0.2))


def meadow_svg():
    defs = S.lin_grad("n14m", [(0, "#a6cc66"), (1, "#80a84f")])
    d = S.smooth_path([(-100, 850), (400, 860), (900, 880), (1400, 872), (1900, 858), (W + 100, 864)], closed=False)
    b = S.path(d + f" L{W + 100},{H + 60} L-100,{H + 60} Z", fill="url(#n14m)", sw=3.5)
    rng = random.Random(14)
    fl = ""
    for _ in range(70):
        x, y = rng.uniform(-40, W + 40), rng.uniform(930, 1180)
        col = rng.choice(["#f6d36b", "#fbf3e3", "#f2a6a0", "#c9b6e4"])
        r = rng.uniform(4, 8) * (0.6 + (y - 900) / 400)
        fl += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.35)}" fill="#e7a23c"/>')
    for x, y, rx in ((1500, 1010, 260), (900, 1080, 220), (1900, 1100, 200)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.14:.0f}" fill="#bad879" opacity="0.6"/>'
    extra = (PR.puddle(1560, 1050, 0.9, width=260, sky="#b8deea") + PR.bush(2010, 905, 0.75, variant=1) +
             PR.bush(120, 900, 0.7, variant=3))
    return doc(S.g(b, filter="wobble") + S.g(fl, filter="wobble-fine") + extra, defs)


def puddle_svg(ripple=0.0, splash=0.0):
    x, y, s = PUD
    return doc(PR.puddle(x, y, s, width=300, ripple=ripple, splash=splash, sky="#b8deea"))


def kid_svg(pose, expr=None):
    x, y, s = KID
    sh = C.ground_shadow(x, y + 2, s, 90, 0.18) if pose != "jump" else ""
    return doc(sh + C.child(x, y, s, 1, pose=pose, expr=expr))


def kid_glow_svg():
    x, y, s = KID
    defs = S.rad_grad("n14kg", [(0, "#fff0c0", 0.85), (0.45, "#ffe3a0", 0.4), (1, "#ffe3a0", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y - 150 * s}" rx="330" ry="330" fill="url(#n14kg)"/>', defs)


def ark_glow_svg():
    x, y, s = ARK
    defs = S.rad_grad("n14ag", [(0, "#fff0c0", 0.9), (0.5, "#ffe3a0", 0.35), (1, "#ffe3a0", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y - 70}" rx="260" ry="170" fill="url(#n14ag)"/>', defs)


FG = [(20, 1192, 1.3, 2), (260, 1190, 1.0, 0), (700, 1196, 1.1, 2), (1100, 1192, 0.9, 0), (1480, 1194, 1.2, 2),
      (1820, 1190, 1.0, 0), (2100, 1196, 1.3, 1), (620, 1090, 0.7, 0), (1300, 1080, 0.6, 2)]


def fg_svg(k):
    out = ""
    for x, y, s, v in FG:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.45 * math.sin(k * 2.1 + x * 0.013))
    return doc(out)


def pair_svg(kind, x, pose="stand", phase=0.0):
    s = PARADE_S
    return doc(C.ground_shadow(x - 20, PARADE_Y + 2, s, 360 if kind in ("elephant", "giraffe", "lion", "zebra")
                               else 200, 0.18) + PR.animal_pair(kind, x, PARADE_Y, s, -1, pose=pose, phase=phase))


def qm_svg():
    x, y = QM
    b = (f'<circle cx="{x}" cy="{y}" r="74" fill="#fffaf0" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{x - 70}" cy="{y + 74}" r="14" fill="#fffaf0" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="{x - 98}" cy="{y + 104}" r="8" fill="#fffaf0" stroke="{INK}" stroke-width="3.5"/>')
    b = S.g(b, filter="wobble-fine")
    b += S.text(x, y + 40, "？", size=118, fill="#e2763d",
                extra=f'stroke="{INK}" stroke-width="4" paint-order="stroke"')
    return doc(b)


def end_card_svg():
    x, y = END
    defs = S.rad_grad("n14card", [(0, "#fff3d6", 0.75), (0.6, "#ffe9c0", 0.3), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 40}" rx="620" ry="170" fill="url(#n14card)"/>' +
           S.text(x, y, "挪亚方舟 · 完", size=124, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


# ================================================================== build

def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    m0, m1, m2 = (voice_marks(ctx, i) for i in range(3))

    def ph(m, i, default):
        return m[i][1] if len(m) > i else default
    L0, L1, L2 = ctx.lines[:3]
    t_kid = ph(m0, 0, L0.start)
    t_rain = ph(m0, 1, t_kid + 1.0)
    t_bow = ph(m0, 2, t_rain + 1.1)
    t_think = ph(m0, 3, t_bow + 1.7)
    t_word = ph(m1, 0, L1.start)
    t_keep = ph(m1, 1, t_word + 1.5)
    t_you = ph(m1, 2, t_keep + 1.4)
    t_noah = ph(m1, 3, t_you + 1.6)
    t_oh = ph(m2, 0, L2.start)
    t_ark = ph(m2, 1, t_oh + 0.7)
    t_which = ph(m2, 2, t_ark + 1.8)
    t_end = max(L2.end + 0.15, T - 1.25)
    t_still = T - 0.5

    # ---- child timeline: two jumps into the puddle, look up, point, smile, wave, cheer
    j1 = snap(t_kid + 0.08)
    j2 = snap(t_rain + 0.1)
    JUMP = 0.36
    land = [snap(j1 + JUMP), snap(j2 + JUMP)]
    t_up = snap(t_bow + 0.05)
    t_pt = snap(t_think + 0.05)
    t_smile = snap(t_word + 0.1)
    t_wave = snap(t_oh + 0.02)
    t_cheer = snap(t_which + 0.3)
    t_calm = snap(min(t_cheer + 1.3, t_end - 0.4))
    names = ["stand", "jump", "splash", "smile_up", "point_up", "smile_up_h", "wave", "cheer", "stand_h",
             "blink_happy", "blink_amazed"]
    kfr = [kid_svg("stand", "happy"), kid_svg("jump", "laugh"), kid_svg("splash", "laugh"),
           kid_svg("smile_up", "amazed"), kid_svg("point_up", "amazed"), kid_svg("smile_up", "happy"),
           kid_svg("wave", "happy"), kid_svg("cheer", "laugh"), kid_svg("stand", "happy"),
           kid_svg("smile_up", "n14_blink_happy"), kid_svg("point_up", "n14_blink_amazed")]
    N = {n: i for i, n in enumerate(names)}
    kents = [(0, N["stand"]), (j1, N["jump"]), (land[0], N["splash"]), (snap(land[0] + 0.45), N["stand"]),
             (j2, N["jump"]), (land[1], N["splash"]), (snap(land[1] + 0.5), N["stand"]), (t_up, N["smile_up"]),
             (t_pt, N["point_up"]), (t_smile, N["smile_up_h"]), (t_wave, N["wave"]), (t_cheer, N["cheer"]),
             (t_calm, N["stand_h"])]
    for tb, base, bl in ((t_word - 0.9, "point_up", "blink_amazed"), (t_you + 0.9, "smile_up_h", "blink_happy"),
                         (t_noah + 1.0, "smile_up_h", "blink_happy")):
        tb = snap(tb)
        if all(abs(tb - tk) > 0.35 for tk, _ in kents):
            kents += [(tb, N[bl]), (snap(tb + 0.13), N[base])]
    kents.sort()
    kx, ky, ks = KID

    def jump_arc(t):
        dy = 0.0
        for j, l in zip((j1, j2), land):
            if j <= t < l:
                u = (t - j) / (l - j)
                dy = -95 * ks * math.sin(math.pi * u) * (1.0 if j == j1 else 1.25)
        return Tf(dy=dy)
    pose_cuts = [tk for tk, _ in kents if tk > 0]
    land_dips = [dip(l, ks, (kx, ky), 14) for l in land]
    other_dips = [dip(tc, ks, (kx, ky), 7) for tc in (t_up, t_pt, t_smile, t_wave, t_cheer, t_calm)]

    def wave_rock(t):
        if t_wave + 0.2 < t < t_cheer - 0.1:
            return Tf(rot=2.2 * math.sin(2 * math.pi * (t - t_wave) / 0.6), px=kx, py=ky)
        return Tf()
    still = lambda t: 1.0 - M.progress(t, t_still - 0.6, t_still, "sine")  # noqa: E731
    sc.add("kid_glow", kid_glow_svg(), z=7.9, wc=0, blend="screen",
           motion=M.combine(lambda t: Tf(alpha=M.progress(t, t_word - 0.2, t_word + 1.2, "sine") *
                                         (0.55 + 0.45 * M.progress(t, t_you, t_you + 0.8, "sine")) *
                                         (1 - 0.5 * M.progress(t, t_oh, t_ark + 0.6, "sine")) *
                                         (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.2))),
                            M.breathe(0.04, 2.2, pivot=(kx, ky - 150 * ks))))
    sc.add("puddle", [puddle_svg(ripple=k / 4) for k in range(4)] +
           [puddle_svg(ripple=0.0, splash=k / 8) for k in range(1, 9)], z=8,
           frame_at=lambda t: puddle_frame(t), wc=0.5)

    def puddle_frame(t):
        for l in land:
            u = t - l
            if 0 <= u < 0.64:
                return 4.0 + min(7, int(u / 0.08))
        return float(int(t / 0.3) % 4)
    sc.add("kid", kfr, z=9, frame_at=cuts(kents),
           motion=M.combine(jump_arc, *land_dips, *other_dips, wave_rock,
                            lambda t: Tf(sx=1 + 0.012 * math.sin(2 * math.pi * t / 2.6) * still(t),
                                         sy=1 + 0.012 * math.sin(2 * math.pi * t / 2.6) * still(t), px=kx, py=ky)),
           seed=91)

    # ---- backdrop
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg(), z=0.5, motion=lambda t: Tf(dx=8 * t))
    t_bow1 = t_bow + 1.6

    def bow_reveal(t):
        return {"mode": "left", "frac": M.progress(t, t_bow - 0.1, t_bow1, "inout"), "soft": 260}
    sc.add("rainbow", rainbow_svg(), z=1, wc=0.35, reveal=bow_reveal,
           motion=lambda t: Tf(alpha=0.85 + 0.15 * M.progress(t, t_keep - 0.3, t_keep + 0.6, "sine") *
                               (1 - 0.6 * M.progress(t, t_you, t_you + 1.5, "sine"))))
    sc.add("far", far_svg(), z=2)
    sc.add("ark_glow", ark_glow_svg(), z=2.1, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, t_noah, t_noah + 0.9, "sine") *
                               (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.0)) *
                               (1 - 0.6 * M.progress(t, t_ark, t_ark + 1.0, "sine"))))
    sc.add("meadow", meadow_svg(), z=3)

    # ---- the parade of pairs (pop up one at a time on '方舟里那么多动物 ... 你最喜欢哪一种呢')
    n = len(PARADE)
    span0, span1 = t_ark + 0.05, max(t_which + 0.8, t_ark + 2.4)
    pops = [snap(span0 + (span1 - span0) * i / (n - 1)) for i in range(n)]
    for i, (kind, x) in enumerate(PARADE):
        tp = pops[i]
        fr = [pair_svg(kind, x)]
        if kind == "rabbit":
            fr += [pair_svg(kind, x, "hop", p) for p in (0, .25, .5, .75)]
        piv = (x, PARADE_Y)
        hops = [tp + 1.6 + 1.7 * k + 0.23 * i for k in range(4)]

        def pmot(t, tp=tp, piv=piv, i=i, hops=hops, kind=kind):
            if t < tp:
                return Tf(alpha=0)
            u = min(1.0, (t - tp) / 0.42)
            s = 0.2 + 0.8 * M.ease("back")(u)
            a = min(1.0, (t - tp) / 0.1)
            dy = 0.0
            if kind != "rabbit":
                for th in hops:
                    w = t - th
                    if 0 <= w < 0.34 and th < t_still - 0.4:
                        dy -= 12 * math.sin(math.pi * w / 0.34)
            br = 1 + 0.012 * math.sin(2 * math.pi * (t / 2.5 + i * 0.21)) * still(t)
            return Tf(dy=dy, sx=s * br, sy=s * (2 - br), alpha=a, px=piv[0], py=piv[1])
        kw = {}
        if kind == "rabbit":
            def rfa(t, hops=hops):
                for th in hops:
                    w = t - th
                    if 0 <= w < 0.4 and th < t_still - 0.4:
                        return 1.0 + float(min(3, int(w / 0.1)))
                return 0.0
            kw["frame_at"] = rfa
        sc.add(f"pair{i}", fr, z=4 + i * 0.01, motion=pmot, seed=60 + i, **kw)
        sc.fx.append(FX.sparkles((x - 90, PARADE_Y - 260, x + 70, PARADE_Y - 80), count=4, t0=tp, t1=tp + 0.9,
                                 size=(10, 18), period=0.9, drift=-30, seed=70 + i))

    sc.add("fg", [fg_svg(k) for k in range(3)], z=10,
           frame_at=lambda t: float((0, 1, 2, 1)[int(min(t, t_still) / 0.55) % 4]))

    # ---- '?' bubble, end card and heart
    t_q = snap(t_which + 0.15)
    t_q_out = t_end - 0.1

    def qm_m(t):
        if t < t_q:
            return Tf(alpha=0)
        u = min(1.0, (t - t_q) / 0.4)
        s = 0.3 + 0.7 * M.ease("back")(u)
        out = M.progress(t, t_q_out, t_q_out + 0.3, "in")
        return Tf(sx=s * (1 - 0.6 * out), sy=s * (1 - 0.6 * out), rot=6 * math.sin(2 * math.pi * (t - t_q) / 1.4),
                  dy=-6 * abs(math.sin(math.pi * (t - t_q) / 0.7)), alpha=1 - out, px=QM[0], py=QM[1] + 40)
    sc.add("qm", qm_svg(), z=11, motion=qm_m, wc=0)
    ex, ey = END
    sc.add("endcard", end_card_svg(), z=12, wc=0, motion=M.keys(
        [(t_end, {"alpha": 0, "s": 0.95, "dy": 16}), (t_end + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    hx, hy = ex, ey + 78
    th = t_end + 0.45
    sc.add("heart", S.svg_doc(heart_markup(hx, hy, 30)), z=12.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))

    # ---- sparkles: wet grass, the rainbow's promise, the child's glow
    sc.fx.append(FX.sparkles((80, 960, 2050, 1150), count=8, t0=0, t1=t_bow1, color=(255, 252, 230), size=(7, 13),
                             period=1.8, drift=0, seed=81))
    sc.fx.append(FX.sparkles((450, 100, 1700, 520), count=12, t0=t_keep - 0.2, t1=t_you + 1.0, size=(9, 17),
                             period=1.4, drift=0, seed=83))
    sc.fx.append(FX.sparkles((kx - 230, ky - 420, kx + 230, ky - 60), count=9, t0=t_you, t1=t_ark + 0.4,
                             size=(8, 15), period=1.5, drift=-14, seed=85))
    sc.fx.append(FX.sparkles((ex - 420, ey - 120, ex + 420, ey + 40), count=6, t0=t_end + 0.4, size=(9, 16),
                             period=2.0, drift=0, seed=87))

    # ---- camera: close on the splashing child, then lift and widen to the rainbow page
    c0 = Cam(720, 760, 1380)
    cw = Cam(W / 2, H / 2 + 4, W * 0.985)
    sc.camera = M.cam_keys([(0, c0), (t_rain + 0.4, Cam(730, 755, 1420)), (t_bow + 2.2, cw),
                            (T, Cam(W / 2, H / 2 + 8, W * 0.95))], ["sine", "sine", "sine"])

    # ---- sound
    sc.sfx("birds", 0, dur=T, gain_db=-17, fade_in=0.8, fade_out=1.5)
    sc.sfx("drip", 0, dur=t_bow + 1.0, gain_db=-24, fade_in=0.8, fade_out=1.0)
    for l, g in zip(land, (-11, -9)):
        sc.sfx("splash_small", l - 0.02, gain_db=g, pan=-0.5)
    sc.sfx("chime", t_bow + 0.1, gain_db=-12)
    sc.sfx("sparkle", t_keep, gain_db=-15)
    sc.sfx("sparkle", t_you + 0.2, gain_db=-16, pan=-0.4)
    for i, tp in enumerate(pops):
        sc.sfx("pop", tp, gain_db=-14, pan=-0.6 + 1.2 * i / (n - 1))
    sc.sfx("pop", t_q, gain_db=-12, pan=0.4)
    sc.sfx("chime", t_end + 0.1, gain_db=-12)
    return sc
