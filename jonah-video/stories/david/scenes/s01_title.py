"""Scene 1 — title page: a sunny Bethlehem hillside; David sits in the grass with his sheep, his sling held up in
one hand; a lamb hops about; far across the valley a huge bronze helmet with a red crest peeks over the opposite
hill and glints in the sun (Goliath only hinted). Book title.

Beats (from ctx.lines[0], "圣经绘本：大卫和歌利亚。", one chunk; nothing hard-coded to the take):
  start        calm sunny frame (the film fades in over it): clouds drift, grass sways, the lamb hops, a sheep
               bleats (sheep sfx), the helmet glints softly
  line 0       "圣经绘本" -> the ribbon header (story.SUBTITLE) unfurls just before the voice (chime);
               "大卫和歌利亚" -> the six title characters pop in one by one on their syllables (onsets measured in
               the voice clip at build time, see syllable_onsets; fallback fractions of the line);
               on "大卫" David bounces happily; on "歌利亚" the far helmet rises a little and flashes a big glint
  end          calm hold, slow push-in. s02_afraid opens with a plain cross-dissolve on this very page:
               it calls title_page(..., toff) with the time offset between the two scenes, so its first second
               is exactly this scene's last second.
"""
import math
import sys

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD, load_story
from engine.scene import Scene

INK = P["ink"]
CREAM = "#fff6e3"
HORIZON = 640
SUN = (250, 215)
SUN_R = 78
DAVID = (560, 948, 1.25)          # sitting anchor (seat on the ground), facing right toward the helmet
HELMET = (1740, 668, 1.3)        # bottom centre of the far helmet (its lower part is hidden by the far hill)
TITLE_Y, TITLE_SIZE, TITLE_STEP = 410, 176, 196
RIB_X, RIB_Y = W / 2, 150
# Onsets of 大 卫 和 歌 利 亚 in the 2.694 s take (1.39, 1.56, 1.70, 1.93, 2.11, 2.40 s from the clip start):
# primary = measured in the clip at build time as t_a + RATIO * (t_b - t_a) (t_a = end of the pause after 绘本,
# t_b = end of speech); fallback = fractions of the line length.
SYL_RATIO = (0.0, 0.133, 0.242, 0.422, 0.563, 0.789)
SYL_FRAC = (0.516, 0.579, 0.631, 0.716, 0.783, 0.891)
SYL_L = 2.694


def doc(body, defs=""):
    return S.svg_doc(body, defs)


# ================================================================== voice timing


def _speech_span(path):
    import soundfile as sf
    x, sr = sf.read(str(path), dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    hop = int(sr * 0.01)
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    e = e / max(1e-6, e.max())
    on = e > 0.06
    n = len(x) / sr
    idx = np.nonzero(on)[0]
    if len(idx) == 0:
        return None
    t_b = (idx[-1] + 1) * 0.01
    # longest silent run in the middle part of the clip = the pause after 绘本
    best, run, start = (0, 0), 0, 0
    for i in range(int(0.15 * len(e)), int(0.75 * len(e))):
        if not on[i]:
            if run == 0:
                start = i
            run += 1
            if run > best[0]:
                best = (run, start + run)
        else:
            run = 0
    if best[0] < 20:
        return None
    return best[1] * 0.01, t_b, n


def syllable_onsets(ctx):
    """Onsets of the six title characters, in seconds from the scene start."""
    ln = ctx.lines[0]
    L = ln.end - ln.start
    path = BUILD / "voice" / "lines" / f"{ctx.id}_00.wav"
    span = None
    try:
        span = _speech_span(path)
    except Exception as e:                              # missing / unreadable clip
        print(f"[{ctx.id}] could not read {path.name}: {e}", file=sys.stderr)
    if span is not None:
        t_a, t_b, n = span
        if 0.3 * n < t_a < 0.8 * n and 0.6 < t_b - t_a < 0.65 * n:
            return [ln.start + t_a + r * (t_b - t_a) for r in SYL_RATIO]
    print(f"[{ctx.id}] title syllables: using fractions of line 0", file=sys.stderr)
    return [ln.start + f * L for f in SYL_FRAC]


# ================================================================== drawings


def sky_svg():
    defs = (S.lin_grad("t1sky", [(0, "#86c3dc"), (0.45, "#b4dbe6"), (0.8, "#dcecdc"), (1, "#f4ecd0")]) +
            S.rad_grad("t1sunglow", [(0, "#fff6d6", 0.95), (0.35, "#fff0c0", 0.5), (1, "#fff0c0", 0)]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 260}" fill="url(#t1sky)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="430" fill="url(#t1sunglow)"/>'
    return doc(b, defs)


def sun_svg():
    defs = (S.rad_grad("t1sun", [(0, "#fff3bf"), (0.6, P["sun"]), (1, "#f5bb4f")], cx=0.45, cy=0.42) +
            S.rad_grad("t1ray", [(0, "#fff7dc", 1), (0.5, "#fff2cf", 0.5), (1, "#fff2cf", 0)]))
    d = S.rays(SUN[0], SUN[1], SUN_R + 18, 300, n=16, width_deg=7)
    b = S.g(f'<path d="{d}" fill="url(#t1ray)"/>', filter="soft", opacity=0.8)
    b += S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="{SUN_R}" fill="url(#t1sun)" stroke="{INK}" stroke-width="3.5"/>'
             f'<circle cx="{SUN[0] - 24}" cy="{SUN[1] - 26}" r="18" fill="#fff8dc" opacity="0.6"/>', filter="wobble")
    return doc(b, defs)


def clouds_svg():
    sh = "#d6e6ee"
    b = (S.cloud(640, 300, 330, 104, "#fbf6ec", seed=11, sw=3.5, shade_fill=sh) +
         S.cloud(1560, 250, 380, 120, "#fbf6ec", seed=12, sw=3.5, shade_fill=sh) +
         S.cloud(2030, 420, 240, 80, "#f8f3ea", seed=13, sw=3, shade_fill=sh) +
         S.cloud(-60, 470, 260, 84, "#f8f3ea", seed=14, sw=3, shade_fill=sh) +
         S.cloud(1060, 520, 200, 64, "#f6f1e8", seed=15, sw=2.5, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def far_svg():
    """Hazy far ridges and the valley floor between the hills."""
    b = S.path(S.hill(-200, W + 200, HORIZON + 20, 70, seed=21, bumps=4), fill="#c9d9c4", sw=2.2)
    b += S.path(S.hill(-200, W + 200, HORIZON + 80, 50, seed=22, bumps=5), fill="#b9d0a8", sw=2.5)
    trees = ""
    for x, y, s in ((760, HORIZON + 66, 0.3), (960, HORIZON + 70, 0.26), (1180, HORIZON + 62, 0.28)):
        trees += PR.olive_tree(x, y, s, seed=int(x))
    return doc(S.g(b, filter="wobble") + PR._haze(trees, "#c9d9c4", 0.45, 0.4))


def far_hill_svg():
    """The opposite hill (across the valley) the helmet peeks over, with a far tent and bushes."""
    pts = [(1180, 900), (1330, 760), (1500, 668), (1680, 628), (1850, 630), (2010, 660), (2180, 700), (2300, 760)]
    d = S.smooth_path(pts, closed=False) + f" L2300,{H + 60} L1180,{H + 60} Z"
    defs = S.lin_grad("t1fh", [(0, "#a9c98a"), (1, "#93b672")])
    b = S.path(d, fill="url(#t1fh)", sw=3)
    b += (f'<path d="M1420,720 Q1560,672 1700,660" stroke="#c4dca6" stroke-width="10" fill="none" '
          f'stroke-linecap="round" opacity="0.7"/>')
    items = PR.bush(1440, 735, 0.45, variant=1) + PR.bush(2060, 690, 0.4, variant=0)
    items += PR.olive_tree(1985, 668, 0.42, seed=4)
    return doc(S.g(b, filter="wobble") + PR._haze(items, "#c4d8bc", 0.25, 0.25), defs)


def valley_svg():
    """Valley floor in the middle distance with the little brook."""
    defs = (S.lin_grad("t1vf", [(0, "#c2d8a6", 0), (0.25, "#bcd59b"), (1, "#a9c784")]) +
            S.lin_grad("t1br", [(0, "#a9d3dc"), (1, "#5e9fbe")]))
    b = f'<ellipse cx="1020" cy="860" rx="420" ry="200" fill="url(#t1vf)" filter="url(#soft)"/>'
    d = "M1000,705 C1030,725 990,745 1020,768 C1060,795 1130,815 1110,850 C1090,885 1150,915 1230,950"
    brook = (f'<path d="{d}" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.55"/>'
             f'<path d="{d}" stroke="url(#t1br)" stroke-width="14" fill="none" stroke-linecap="round"/>'
             f'<path d="{d}" stroke="#e2f3f3" stroke-width="3" fill="none" stroke-dasharray="12 26" '
             f'stroke-linecap="round"/>')
    return doc(b + S.g(brook, filter="wobble-fine"), defs)


def helmet_svg():
    x, y, s = HELMET
    hel = PR.helmet_bronze(x, y, s, -1, crest=True)
    # the tip of the great spear peeking up beside it
    sx, top = x + 100 * s, y - 175 * s
    spear = (f'<path d="M{sx},{y + 10} L{sx + 5},{top}" stroke="{INK}" stroke-width="{12 * s + 8:.0f}" '
             f'stroke-linecap="round"/><path d="M{sx},{y + 10} L{sx + 5},{top}" stroke="#a0683e" '
             f'stroke-width="{12 * s:.0f}" stroke-linecap="round"/>'
             f'<path d="M{sx + 5},{top - 62 * s} L{sx + 5 + 14 * s},{top - 8 * s} L{sx + 5},{top + 4} '
             f'L{sx + 5 - 14 * s},{top - 8 * s} Z" fill="#b9bfc4" stroke="{INK}" stroke-width="3.5" '
             f'stroke-linejoin="round"/>')
    return doc(PR._haze(S.g(spear, filter="wobble-fine") + hel, "#d9e6e0", 0.12, 0.2))


def near_hill_svg():
    """David's hill: the big sunny foreground slope, with flowers and stones."""
    pts = [(-120, 820), (120, 800), (420, 840), (760, 880), (1060, 925), (1360, 955), (1700, 1010), (2000, 1080),
           (2260, 1160)]
    d = S.smooth_path(pts, closed=False) + f" L2260,{H + 60} L-120,{H + 60} Z"
    defs = S.lin_grad("t1nh", [(0, "#a6c962"), (0.5, "#93b85c"), (1, "#7fa64d")])
    b = S.path(d, fill="url(#t1nh)", sw=4)
    for x, y, rx in ((300, 1010, 200), (980, 1040, 160), (1500, 1110, 220), (160, 1130, 140)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.16:.0f}" fill="#b5d36f" opacity="0.6"/>'
    for x, y, r in ((1240, 1010, 13), (110, 960, 10), (1650, 1070, 11), (820, 1100, 9)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5}" ry="{r}" fill="#d8ccb6" stroke="{INK}" stroke-width="2.5"/>'
    flowers = ""
    import random
    rng = random.Random(5)
    for _ in range(46):
        x = rng.uniform(-60, 1900)
        y = rng.uniform(870, 1170)
        if y < 840 + (x + 120) * 0.12:
            continue
        col = rng.choice(["#f6d36b", "#fbf3e3", "#f2a6a0", "#c9b6e4"])
        r = rng.uniform(5, 8)
        flowers += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
                    f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 0.35:.1f}" fill="#e7a23c"/>')
    tree = PR.olive_tree(170, 830, 0.95, seed=2)
    return doc(tree + S.g(b, filter="wobble") + S.g(flowers, filter="wobble-fine"), defs)


def tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((40, 1180, 1.2, 2), (330, 1150, 0.9, 0), (760, 1175, 1.0, 2), (1180, 1185, 1.0, 0),
                       (1560, 1180, 1.1, 2), (1960, 1188, 1.1, 1), (1430, 1060, 0.7, 0), (880, 1010, 0.65, 2),
                       (60, 900, 0.7, 0), (1820, 1080, 0.8, 0)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


def david_sit(x, y, s=1.0, facing=1, expr="happy"):
    """David sitting in the grass, legs out, arms open, the sling hanging from his raised hand (the library has
    no plain sitting pose for David: his design on the 'sit_happy' rig, with the 'hold_sling' sling)."""
    ps = dict(C.POSES["sit_happy"])
    ps["expr"] = expr
    D = C._david_design(False, True)
    D["behind"], D["mid"], D["front"] = None, C._bag_mid, C._sling_front(D, "hold")
    inner, _ = C._figure(D, C._BOY, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"david-sit-{expr}")


def ribbon_svg(text):
    cx, cy, hw, h = RIB_X, RIB_Y, 360, 80
    band_col = "#4f86bf"
    tail_col, fold_col = S.shade(band_col, -0.16), S.shade(band_col, -0.38)
    b = ""
    for sd in (-1, 1):
        ex = cx + sd * hw
        top, bot = cy - h / 2 + 26, cy + h / 2 + 26
        pts = [(ex - sd * 30, top), (ex + sd * 95, top), (ex + sd * 66, (top + bot) / 2), (ex + sd * 95, bot),
               (ex - sd * 30, bot)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z", fill=tail_col, sw=3.5)
        fold = [(ex, cy + h / 2 + 6), (ex - sd * 30, bot), (ex - sd * 30, cy + h / 2 + 6)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in fold) + " Z", fill=fold_col, sw=3)
    band = (f"M{cx - hw},{cy - h / 2 + 8} Q{cx},{cy - h / 2 - 12} {cx + hw},{cy - h / 2 + 8} "
            f"L{cx + hw},{cy + h / 2 + 6} Q{cx},{cy + h / 2 - 14} {cx - hw},{cy + h / 2 + 6} Z")
    b += S.path(band, fill=band_col, sw=3.5)
    for yy, q in ((cy - h / 2 + 18, cy - h / 2), (cy + h / 2 - 4, cy + h / 2 - 22)):
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#a9c8e8" stroke-width="3" '
              f'fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="48" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">{text}</text>')
    return doc(body)


def title_defs():
    return (S.lin_grad("t1tg", [(0, "#ec8a45"), (0.55, "#d0632f"), (1, "#b04d26")]) +
            '<filter id="t1tsh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/>'
            '</filter>')


def title_char(ch, x, y):
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{TITLE_SIZE}" text-anchor="middle"'
    b = (f'<text x="{x + 6}" y="{y + 10}" {font} fill="{INK}" opacity="0.28" filter="url(#t1tsh)" '
         f'stroke="{INK}" stroke-width="18" stroke-linejoin="round">{ch}</text>')
    b += f'<text x="{x}" y="{y}" {font} fill="{CREAM}" stroke="{CREAM}" stroke-width="22" stroke-linejoin="round">{ch}</text>'
    b += (f'<text x="{x}" y="{y}" {font} fill="url(#t1tg)" stroke="{INK}" stroke-width="3.5" '
          f'stroke-linejoin="round">{ch}</text>')
    return doc(b, title_defs())


# ================================================================== the page (shared with s02)


def _shift(fn, toff):
    if fn is None:
        return None
    return lambda t: fn(t + toff)


def title_page(sc, ctx, toff=0.0, gate=None, title_gate=None):
    """Add the whole title page to ``sc``. Times inside are this scene's (s01) times; ``toff`` is added to the
    host scene's clock (s02 passes the offset between the two scene starts). ``gate(t_host)`` -> 0/1 alpha
    multiplier for every layer (s02 hides the page once it is covered); ``title_gate`` multiplies the title
    lettering only. Returns (camera(t_host), fx list, info dict)."""
    T = ctx.duration
    say = ctx.lines[0]
    onsets = syllable_onsets(ctx)
    t_rib = say.start - 0.1
    t_david = onsets[0]
    t_glint = onsets[3]
    names = []

    def add(name, svg, motion=None, title=False, **kw):
        g1 = gate
        g2 = title_gate if title else None
        m0 = motion

        def mot(th):
            tf = m0(th + toff) if m0 is not None else Tf()
            a = tf.alpha * (g1(th) if g1 else 1.0) * (g2(th) if g2 else 1.0)
            return Tf(tf.dx, tf.dy, tf.rot, tf.sx, tf.sy, a, tf.px, tf.py)
        need = m0 is not None or g1 is not None or g2 is not None
        fa = kw.pop("frame_at", None)
        sc.add(f"t1_{name}", svg, motion=mot if need else None,
               frame_at=_shift(fa, toff), **kw)
        names.append(name)

    add("sky", sky_svg(), wc=0.6)
    add("sun", sun_svg(), motion=lambda t: Tf(rot=1.5 * t, px=SUN[0], py=SUN[1]))
    add("clouds", clouds_svg(), motion=M.drift(vx=9))
    add("far", far_svg())
    add("valley", valley_svg())
    # the helmet: a slow breathing bob, and a little rise on "歌利亚" as if the giant stood up a bit taller
    hx, hy, hs = HELMET
    add("helmet", helmet_svg(), seed=5,
        motion=M.combine(M.keys([(0, {"dy": 8}), (t_glint - 0.3, {"dy": 6}), (t_glint + 0.25, {"dy": -16}),
                                 (T + 6, {"dy": -12})], ["sine", "out", "sine"]),
                         lambda t: Tf(dy=3 * math.sin(2 * math.pi * t / 2.6), rot=1.2 * math.sin(2 * math.pi * t / 4.0),
                                      px=hx, py=hy)))
    add("far_hill", far_hill_svg())
    add("near_hill", near_hill_svg())

    # sheep: a grazing ewe behind David, a standing ewe on the right that bleats once, a far one on the slope
    def sheep_layer(name, x, y, s, f, variant, poses, fa=None, mot=None):
        frames = [doc(C.ground_shadow(x, y + 2, s, 190, 0.18) + PR.sheep(x, y, s, f, variant, pose=p)) for p in poses]
        add(name, frames if len(frames) > 1 else frames[0], frame_at=fa, motion=mot, seed=len(names) * 3)

    sheep_layer("sheep_far", 1300, 975, 0.62, -1, 2, ["graze"], mot=M.breathe(0.012, 3.1, pivot=(1300, 975)))
    switches = [k * 6.0 + d for k in range(4) for d in (2.6, 4.4)]

    def dips(t, pv=(300, 905)):
        dy, sy = 0.0, 1.0
        for ts in switches:
            u = t - ts
            if -0.12 <= u < 0.2:
                k = math.sin(math.pi * (u + 0.12) / 0.32)
                dy += 4 * k
                sy *= 1 - 0.035 * k
        return Tf(dy=dy, sy=sy, px=pv[0], py=pv[1])
    sheep_layer("sheep_back", 300, 905, 0.9, 1, 0, ["graze", "stand"],
                fa=lambda t: 1.0 if 2.6 <= (t % 6.0) < 4.4 else 0.0,
                mot=M.combine(dips, M.breathe(0.012, 2.7, pivot=(300, 905), phase=0.3)))
    t_bleat = 0.55
    sheep_layer("sheep_right", 905, 1010, 1.0, -1, 3, ["stand", "bleat"],
                fa=lambda t: 1.0 if t_bleat <= t < t_bleat + 1.0 else 0.0,
                mot=M.combine(M.breathe(0.012, 2.9, pivot=(905, 1010)),
                              M.keys([(t_bleat - 0.12, {"dy": 0, "sy": 1}), (t_bleat, {"dy": 4, "sy": 0.96}),
                                      (t_bleat + 0.16, {"dy": -4, "sy": 1.02}), (t_bleat + 0.32, {"dy": 0, "sy": 1}),
                                      (t_bleat + 0.88, {"dy": 0, "sy": 1}), (t_bleat + 1.0, {"dy": 4, "sy": 0.965}),
                                      (t_bleat + 1.2, {"dy": 0, "sy": 1})],
                                     ["in", "out", "sine", "sine", "in", "out"], pivot=(905, 1010))))

    # David (blinks now and then; bounces on "大卫")
    dx_, dy_, ds = DAVID
    dfr = [doc(C.ground_shadow(dx_ + 10 * ds, dy_ + 3, ds, 230, 0.2) + david_sit(dx_, dy_, ds, 1, e))
           for e in ("happy", "peaceful")]

    def blink(t):
        for tb in (1.15, 3.6, 5.3, 7.5):
            if tb <= t < tb + 0.14:
                return 1.0
        return 0.0
    piv = (dx_, dy_)
    add("david", dfr, frame_at=blink, seed=11,
        motion=M.combine(M.breathe(0.012, 2.6, pivot=piv),
                         M.keys([(t_david - 0.1, {"dy": 0, "sy": 1}), (t_david, {"dy": 5, "sy": 0.96}),
                                 (t_david + 0.17, {"dy": -16, "sy": 1.03}), (t_david + 0.36, {"dy": 0, "sy": 0.98}),
                                 (t_david + 0.5, {"dy": 0, "sy": 1})], ["in", "out", "in", "sine"], pivot=piv)))

    # the lamb hops about in front of David
    lx, ly, ls = 1085, 1048, 0.95
    lamb = doc(PR.sheep(lx, ly, ls, -1, 1, lamb=True))
    lsh = doc(C.ground_shadow(lx, ly + 2, ls, 130, 0.2))
    period, t_first = 1.5, 0.3

    def hop_y(t):
        if t < t_first:
            return 0.0, 1.0
        u = ((t - t_first) % period) / 0.5
        if u >= 1:
            return 0.0, 1.0
        return -46 * math.sin(math.pi * u), 1.0 + 0.04 * math.sin(math.pi * u)

    def lamb_m(t):
        y, s = hop_y(t)
        u = ((t - t_first) % period)
        squash = 0.94 if (t >= t_first and (u < 0.06 or 0.5 <= u < 0.58)) else 1.0
        return Tf(dy=y, sy=s * squash, sx=1 / (s * squash) ** 0.5, rot=-4 * math.sin(math.pi * min(1, u / 0.5)) if
                  t >= t_first else 0, px=lx, py=ly)

    def lsh_m(t):
        y, _ = hop_y(t)
        k = 1 + y / 160
        return Tf(sx=k, sy=k, alpha=0.6 + 0.4 * k, px=lx, py=ly)
    add("lamb_shadow", lsh, motion=lsh_m, wc=0)
    add("lamb", lamb, motion=lamb_m, seed=17)
    add("tufts", [tufts_svg(k) for k in range(3)], frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.5) % 4]))

    # ---- title lettering
    story = load_story()

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=RIB_X, py=RIB_Y)
    add("ribbon", ribbon_svg(story.SUBTITLE), motion=unfurl, title=True, wc=0)
    title = story.TITLE
    x0 = W / 2 - TITLE_STEP * (len(title) - 1) / 2
    for i, ch in enumerate(title):
        x = x0 + i * TITLE_STEP
        t0 = onsets[min(i, len(onsets) - 1)] - 0.06

        def pop(t, t0=t0, x=x, i=i):
            if t < t0:
                return Tf(alpha=0)
            a = min(1.0, (t - t0) / 0.12)
            u = min(1.0, (t - t0) / 0.42)
            s = 0.45 + 0.55 * M.ease("back")(u)
            dy = 30 * (1 - M.ease("out")(u)) + 2.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.16))
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 65)
        add(f"title_{i}", title_char(ch, x, TITLE_Y), motion=pop, title=True, wc=0)

    cam0 = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 - 12, H / 2 + 18, W * 0.93))], "sine")
    cam = lambda th: cam0(th + toff)                                          # noqa: E731

    t_done = onsets[-1] + 0.4

    def gated(f):
        def fx(frame, th, view):
            if gate is not None and gate(th) <= 0:
                return frame
            return f(frame, th + toff, view)
        return fx
    fxs = [
        gated(FX.sparkles((hx - 40, hy - 70, hx + 30, hy - 40), count=2, color=(255, 246, 214), size=(10, 18),
                          period=2.2, drift=0, seed=4)),
        gated(FX.sparkles((hx - 60, hy - 95, hx - 10, hy - 55), count=1, t0=t_glint, t1=t_glint + 1.3,
                          color=(255, 248, 220), size=(30, 42), period=1.3, drift=0, seed=6)),
        gated(FX.sparkles((300, 260, 520, 380), count=3, t0=t_done, color=(255, 240, 190), size=(9, 16),
                          period=2.0, drift=0, seed=9)),
        gated(FX.sparkles((1620, 260, 1840, 380), count=3, t0=t_done, color=(255, 240, 190), size=(9, 16),
                          period=2.0, drift=0, seed=10)),
        gated(FX.motes((0, 600, W, 1100), count=20, color=(255, 246, 214), size=(2, 5), alpha=110, seed=12)),
    ]
    info = dict(t_rib=t_rib, t_glint=t_glint, t_bleat=t_bleat, onsets=onsets, names=names)
    return cam, fxs, info


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    cam, fxs, info = title_page(sc, ctx)
    sc.camera = cam
    sc.fx = fxs
    sc.subtitles = False
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-16, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-22, fade_in=1.0, fade_out=1.3)
    sc.sfx("sheep", info["t_bleat"], gain_db=-15, pan=-0.1)
    sc.sfx("chime", info["t_rib"], gain_db=-10)
    sc.sfx("sparkle", info["t_glint"], gain_db=-16, pan=0.6)
    return sc
