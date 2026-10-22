"""Scene 1 — title page: teen Joseph in his bright coat of many colours stands on a sunny green hill with his sheep and
waves to us; far off on the next hill his ten brothers stand with the flocks by a little tent; a sheaf of golden wheat
leans in the bottom-left corner (the dream to come). Book title.

Beats (keyed to ctx.lines[0] '圣经绘本：约瑟和彩衣。'; phrase / syllable onsets are measured in the voice clip at build
time with the Noah film's voice_marks helpers (fallback: proportions of the subtitle chunk), so a new take stays in sync):
  start        calm sunny frame (the film fades in over it): clouds drift, grass sways, a butterfly flutters by the
               sheaf, a sheep bleats (sheep sfx), the lamb hops, two little birds fly across
  ~0.7 s       Joseph lifts his hand (hard pose cut hidden by a squash dip) and waves to us from then on
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime)
  '约瑟和彩衣'  the five title characters pop in one by one on their syllables (pop); on '约瑟' Joseph does a happy
               hop; on '彩衣' his coat twinkles with sparkles (sparkle) and the sheaf in the corner glows a little
  end          calm hold with a slow push-in. s02_question opens with a plain cross-dissolve on this very page: it
               calls title_page(..., toff), so its first second is exactly this scene's last second.

Shared with s02_question / s03_coat / s14_end of this illustrator: joseph_wave(), title helpers, timing helpers.
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
from engine.paths import load_story
from engine.scene import Scene
from stories.noah.scenes.s01_title import char_times, cuts, dip, f1, heart_markup, mark, snap, voice_marks  # noqa: F401

INK = P["ink"]
CREAM = "#fff6e3"
HORIZON = 700
SUN = (240, 190)
JOS = (1540, 986, 1.3)           # Joseph on the knoll, facing left (toward the title / the brothers)
SHEAF = (205, 1172, 1.12)
TITLE_Y, TITLE_SIZE, TITLE_STEP = 408, 172, 200
RIB_X, RIB_Y = W / 2, 150
# one coat colour per title character (deepened so the cream halo and ink keep them readable)
TITLE_COLS = (("#ef7a5e", "#d9503f", "#b23a2e"), ("#f3b843", "#e29a1f", "#c27a12"), ("#7fb862", "#5c9a45", "#467d35"),
              ("#6fa2e0", "#4a7fc6", "#3763a6"), ("#b08bd6", "#8d64bd", "#6f4a9e"))

for _e in ("happy", "proud", "kind", "cross", "jealous", "neutral", "sad", "amazed", "laugh", "sorry"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"j_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def blink_name(expr):
    return f"j_blink_{expr}"


# ================================================================== shared figure helpers


def joseph_wave(x, y, s, facing=1, phase=0.0, expr="happy", progress=1.0):
    """Teen Joseph in his coat waving (the library has no wave pose for Joseph: his own design and rig with a raised
    far arm whose forearm swings with ``phase``)."""
    D = C._joseph_design("shepherd", "colours", progress, True, True, "stand")
    fa = 154 + 15 * math.sin(2 * math.pi * phase)
    ps = C._P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 142, fa), ("fk", -8, -3)), hands=("open", "fist"),
              expr=expr)
    inner, _ = C._figure(D, C._JOSEPH_TEEN_M, ps, expr, C._fsign(facing), True)
    return C._wrap_out(inner, x, y, s, facing, f"joseph-wave-{phase:.3f}-{expr}")


def title_char_svg(ch, x, y, size, gid, cols):
    defs = (S.lin_grad(gid, [(0, cols[0]), (0.55, cols[1]), (1, cols[2])]) +
            '<filter id="j1tsh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/>'
            '</filter>')
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b = (f'<text x="{x + 6}" y="{y + 10}" {font} fill="{INK}" opacity="0.28" filter="url(#j1tsh)" '
         f'stroke="{INK}" stroke-width="18" stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="{CREAM}" stroke="{CREAM}" stroke-width="22" '
          f'stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="url(#{gid})" stroke="{INK}" stroke-width="3.5" '
          f'stroke-linejoin="round">{ch}</text>')
    return doc(b, defs)


def ribbon_svg(text, cx=RIB_X, cy=RIB_Y, hw=380, h=80, band_col="#c9714a", w=W, hh=H):
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
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#f6d3a8" stroke-width="3" '
              f'fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="46" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">{text}</text>')
    return doc(body, w=w, h=hh)


def flowers(rng, n, x0, x1, y0, y1, keep=None, rmul=1.0):
    fl = ""
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if keep is not None and not keep(x, y):
            continue
        col = rng.choice(["#f6d36b", "#fbf3e3", "#f2a6a0", "#c9b6e4"])
        r = rng.uniform(4.5, 8) * rmul
        fl += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.35)}" fill="#e7a23c"/>')
    return fl


# ================================================================== drawings


def sky_svg():
    defs = (S.lin_grad("j1sky", [(0, "#86c3dc"), (0.45, "#b4dbe6"), (0.8, "#dcecdc"), (1, "#f4ecd0")]) +
            S.rad_grad("j1sunglow", [(0, "#fff6d6", 0.95), (0.35, "#fff0c0", 0.5), (1, "#fff0c0", 0)]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 300}" fill="url(#j1sky)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="440" fill="url(#j1sunglow)"/>'
    return doc(b, defs)


def sun_svg():
    defs = (S.rad_grad("j1sun", [(0, "#fff3bf"), (0.6, P["sun"]), (1, "#f5bb4f")], cx=0.45, cy=0.42) +
            S.rad_grad("j1ray", [(0, "#fff7dc", 1), (0.5, "#fff2cf", 0.5), (1, "#fff2cf", 0)]))
    d = S.rays(SUN[0], SUN[1], 96, 300, n=16, width_deg=7)
    b = S.g(f'<path d="{d}" fill="url(#j1ray)"/>', filter="soft", opacity=0.8)
    b += S.g(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="76" fill="url(#j1sun)" stroke="{INK}" stroke-width="3.5"/>'
             f'<circle cx="{SUN[0] - 24}" cy="{SUN[1] - 26}" r="18" fill="#fff8dc" opacity="0.6"/>', filter="wobble")
    return doc(b, defs)


def clouds_svg():
    sh = "#d6e6ee"
    b = (S.cloud(620, 300, 300, 96, "#fbf6ec", seed=21, sw=3.5, shade_fill=sh) +
         S.cloud(1660, 240, 380, 118, "#fbf6ec", seed=22, sw=3.5, shade_fill=sh) +
         S.cloud(1180, 560, 210, 66, "#f8f3ea", seed=23, sw=2.8, shade_fill=sh) +
         S.cloud(2010, 470, 240, 78, "#f8f3ea", seed=24, sw=3, shade_fill=sh))
    return doc(S.g(b, filter="wobble"))


def far_svg():
    """Hazy far ridges, the brothers' hill with a little tent, the ten brothers and their flock (tiny, far off)."""
    b = S.path(S.hill(-200, W + 200, HORIZON + 10, 80, seed=31, bumps=4), fill="#c6d8c4", sw=2.2)
    b += S.path(S.hill(-200, W + 200, HORIZON + 70, 60, seed=32, bumps=5), fill="#b6cfa4", sw=2.4)
    trees = ""
    for x, y, s in ((1180, HORIZON + 50, 0.26), (1330, HORIZON + 58, 0.22), (1960, HORIZON + 50, 0.28)):
        trees += PR.olive_tree(x, y, s, seed=int(x))
    out = S.g(b, filter="wobble") + PR._haze(trees, "#c9d9c4", 0.45, 0.4)
    # the brothers' hill (left middle distance)
    pts = [(-150, 900), (60, 812), (300, 768), (560, 752), (820, 760), (1020, 792), (1180, 850), (1340, 960),
           (1460, 1080)]
    d = S.smooth_path(pts, closed=False) + f" L1460,{H + 60} L-150,{H + 60} Z"
    hill = S.path(d, fill="#a9c98a", sw=3)
    hill += ('<path d="M120,830 Q380,780 700,772" stroke="#c4dca6" stroke-width="10" fill="none" '
             'stroke-linecap="round" opacity="0.7"/>')
    out += S.g(hill, filter="wobble")
    items = PR.tent(905, 772, 0.3, -1, side="israel", flag=False)
    items += PR.olive_tree(150, 812, 0.4, seed=5)
    rng = random.Random(4)
    flock = ""
    for i in range(9):
        x = 250 + i * 70 + rng.uniform(-20, 20)
        y = 770 + rng.uniform(0, 22) + (12 if i % 2 else 0)
        flock += PR.sheep(x, y, 0.27, 1 if i % 3 else -1, i % 4, pose="graze" if i % 2 else "stand")
    group = C.brothers_group(560, 768, 0.25, 1, pose="stand")
    out += PR._haze(items + group + flock, "#cbdcc6", 0.28, 0.32)
    return doc(out)


KNOLL = [(-150, 1060), (200, 1040), (560, 1028), (900, 1020), (1200, 996), (1420, 980), (1560, 978), (1760, 986),
         (2000, 1004), (2280, 1030)]


def near_svg():
    d = S.smooth_path(KNOLL, closed=False) + f" L2280,{H + 60} L-150,{H + 60} Z"
    defs = S.lin_grad("j1nh", [(0, "#a8cc66"), (0.5, "#93b85c"), (1, "#7fa64d")])
    b = S.path(d, fill="url(#j1nh)", sw=4)
    for x, y, rx in ((420, 1100, 230), (1100, 1080, 200), (1640, 1100, 240), (2000, 1140, 160)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.15:.0f}" fill="#b6d470" opacity="0.6"/>'
    for x, y, r in ((960, 1060, 11), (1760, 1050, 12), (640, 1120, 9)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5}" ry="{r}" fill="#d8ccb6" stroke="{INK}" stroke-width="2.5"/>'
    rng = random.Random(9)
    fl = flowers(rng, 70, -40, W + 40, 1000, 1180, keep=lambda x, y: y > 1012 + (0 if x < 1300 else 0))
    bushes = PR.bush(2040, 1012, 0.7, variant=1) + PR.bush(820, 1032, 0.45, variant=0)
    return doc(S.g(b, filter="wobble") + bushes + S.g(fl, filter="wobble-fine"), defs)


def tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((40, 1186, 1.2, 2), (420, 1170, 0.9, 0), (760, 1190, 1.0, 2), (1120, 1186, 1.0, 0),
                       (1500, 1188, 1.1, 2), (1900, 1186, 1.1, 1), (2090, 1150, 0.9, 0), (980, 1100, 0.7, 2),
                       (1300, 1110, 0.7, 0), (600, 1080, 0.6, 2)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


def sheaf_svg(glow=0.0):
    x, y, s = SHEAF
    out = C.ground_shadow(x, y - 2, s, 170, 0.2)
    out += PR.wheat_sheaf(x + 120, y + 8, s * 0.8, -1, bow=0.0, rise=0.0, kind="bundle", seed=3)
    out += PR.wheat_sheaf(x, y, s, 1, glow=glow, seed=1)
    return doc(out)


def joseph_svg(phase=None, blink=False):
    x, y, s = JOS
    expr = blink_name("happy") if blink else "happy"
    sh = C.ground_shadow(x + 6, y + 2, s, 150, 0.2)
    if phase is None:
        return doc(sh + C.joseph(x, y, s, -1, pose="stand", expr=expr))
    return doc(sh + joseph_wave(x, y, s, -1, phase, expr))


def flyer_svg(color, wing):
    return doc(PR.songbird(200, 200, 0.5, 1, wing=wing, color=color))


def butterfly_svg(flap):
    return doc(PR.butterfly(0, 0, 0.9, flap=flap, color="orange"))


# ================================================================== the page (shared with s02)


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    n = len(load_story().TITLE)
    if len(marks) == 1:                       # fallback: the title is the last characters
        ch = ch[-n:]
    return t_rib, ch[:n]


def title_page(sc, ctx, toff=0.0, gate=None, title_gate=None):
    """Add the whole title page to ``sc``. Times inside are s01's; ``toff`` is added to the host scene's clock
    (s02 passes the offset between the two scene starts). ``gate(t_host)`` multiplies every layer's alpha (s02 hides
    the page once covered); ``title_gate`` multiplies the lettering only. Returns (camera(t_host), fx, info)."""
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_hop = snap(onsets[0] + 0.02)
    t_coat = onsets[3] if len(onsets) > 3 else onsets[-1]
    t_up = snap(0.7)

    def add(name, svg, motion=None, title=False, **kw):
        m0 = motion
        g1 = gate
        g2 = title_gate if title else None

        def mot(th):
            tf = m0(th + toff) if m0 is not None else Tf()
            a = tf.alpha * (g1(th) if g1 else 1.0) * (g2(th) if g2 else 1.0)
            return Tf(tf.dx, tf.dy, tf.rot, tf.sx, tf.sy, a, tf.px, tf.py)
        need = m0 is not None or g1 is not None or g2 is not None
        fa = kw.pop("frame_at", None)
        sc.add(f"j1_{name}", svg, motion=mot if need else None,
               frame_at=(lambda th, fa=fa: fa(th + toff)) if fa else None, **kw)

    add("sky", sky_svg(), wc=0.6)
    add("sun", sun_svg(), motion=lambda t: Tf(rot=1.5 * t, px=SUN[0], py=SUN[1]))
    add("clouds", clouds_svg(), motion=M.drift(vx=8))
    add("far", far_svg())

    # two little birds flying across the sky (wing cycle)
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (col, y0, vx, ph) in enumerate((("blue", 300, 92, 0.0), ("yellow", 360, 80, 0.4))):
        def fly(t, y0=y0, vx=vx, ph=ph, i=i):
            x = -300 + 380 * i + vx * t
            return Tf(dx=x, dy=y0 - 200 + 26 * math.sin(2 * math.pi * (t / 2.2 + ph)))
        add(f"flyer{i}", [flyer_svg(col, w) for w in wings], motion=fly, wc=0.3,
            frame_at=lambda t, ph=ph: float(int(t / 0.07 + ph * 8) % 8))

    add("near", near_svg())

    # sheep: a grazing ewe left of Joseph (lifts its head now and then), a ewe on the right that bleats, the lamb hops
    def sheep_layer(name, x, y, s, f, variant, poses, fa=None, mot=None, seed=0):
        frames = [doc(C.ground_shadow(x, y + 2, s, 190, 0.18) + PR.sheep(x, y, s, f, variant, pose=p)) for p in poses]
        add(name, frames if len(frames) > 1 else frames[0], frame_at=fa, motion=mot, seed=seed)

    switches = [k * 5.0 + d for k in range(4) for d in (1.9, 3.6)]

    def dips(t, pv=(1170, 1036)):
        dy, sy = 0.0, 1.0
        for ts in switches:
            u = t - ts
            if -0.12 <= u < 0.2:
                k = math.sin(math.pi * (u + 0.12) / 0.32)
                dy += 4 * k
                sy *= 1 - 0.035 * k
        return Tf(dy=dy, sy=sy, px=pv[0], py=pv[1])
    sheep_layer("sheep_left", 1170, 1036, 0.95, 1, 0, ["graze", "stand"],
                fa=lambda t: 1.0 if 1.9 <= (t % 5.0) < 3.6 else 0.0,
                mot=M.combine(dips, M.breathe(0.012, 2.7, pivot=(1170, 1036), phase=0.3)), seed=41)
    t_bleat = 0.5
    sheep_layer("sheep_right", 1880, 1048, 0.92, -1, 3, ["stand", "bleat"],
                fa=lambda t: 1.0 if t_bleat <= t < t_bleat + 1.0 else 0.0,
                mot=M.combine(M.breathe(0.012, 2.9, pivot=(1880, 1048)),
                              M.keys([(t_bleat - 0.12, {"dy": 0, "sy": 1}), (t_bleat, {"dy": 4, "sy": 0.96}),
                                      (t_bleat + 0.16, {"dy": -4, "sy": 1.02}), (t_bleat + 0.32, {"dy": 0, "sy": 1}),
                                      (t_bleat + 0.88, {"dy": 0, "sy": 1}), (t_bleat + 1.0, {"dy": 4, "sy": 0.965}),
                                      (t_bleat + 1.2, {"dy": 0, "sy": 1})],
                                     ["in", "out", "sine", "sine", "in", "out"], pivot=(1880, 1048))), seed=43)

    # Joseph: stands, lifts his hand at ~0.7 s and waves; a happy hop on '约瑟'; blinks
    jx, jy, js = JOS
    frames = [joseph_svg(), joseph_svg(blink=True)]
    phases = (0.0, 0.25, 0.5, 0.75)
    frames += [joseph_svg(p) for p in phases] + [joseph_svg(p, True) for p in phases]
    blinks = [1.6, 3.4, 5.2, 6.9]

    def jfa(t):
        bl = any(tb <= t < tb + 0.14 for tb in blinks)
        if t < t_up:
            return 1.0 if bl else 0.0
        k = int((t - t_up) / 0.15) % 4
        return float(2 + k + (4 if bl else 0))
    jpiv = (jx, jy)
    add("joseph", frames, frame_at=jfa, seed=11,
        motion=M.combine(M.breathe(0.012, 2.6, pivot=jpiv), dip(t_up, js, jpiv, 7),
                         M.keys([(t_hop - 0.12, {"dy": 0, "sy": 1}), (t_hop, {"dy": 6, "sy": 0.96}),
                                 (t_hop + 0.18, {"dy": -26, "sy": 1.03}), (t_hop + 0.38, {"dy": 0, "sy": 0.97}),
                                 (t_hop + 0.52, {"dy": 0, "sy": 1})], ["in", "out", "in", "sine"], pivot=jpiv)))

    # the lamb hops about between the ewe and Joseph
    lx, ly, ls = 1345, 1068, 0.92
    lamb = doc(PR.sheep(lx, ly, ls, 1, 1, lamb=True))
    lsh = doc(C.ground_shadow(lx, ly + 2, ls, 130, 0.2))
    period, t_first = 1.6, 0.35

    def hop_y(t):
        if t < t_first:
            return 0.0, 1.0
        u = ((t - t_first) % period) / 0.5
        if u >= 1:
            return 0.0, 1.0
        return -42 * math.sin(math.pi * u), 1.0 + 0.04 * math.sin(math.pi * u)

    def lamb_m(t):
        y, s = hop_y(t)
        u = ((t - t_first) % period)
        squash = 0.94 if (t >= t_first and (u < 0.06 or 0.5 <= u < 0.58)) else 1.0
        return Tf(dy=y, sy=s * squash, sx=1 / (s * squash) ** 0.5, rot=4 * math.sin(math.pi * min(1, u / 0.5)) if
                  t >= t_first else 0, px=lx, py=ly)

    def lsh_m(t):
        y, _ = hop_y(t)
        k = 1 + y / 160
        return Tf(sx=k, sy=k, alpha=0.6 + 0.4 * k, px=lx, py=ly)
    add("lamb_shadow", lsh, motion=lsh_m, wc=0)
    add("lamb", lamb, motion=lamb_m, seed=17)

    # the sheaf in the corner: a gentle sway, a little golden glow on '彩衣'
    sx_, sy_, ss = SHEAF
    add("sheaf", [sheaf_svg(0.0), sheaf_svg(0.6)], seed=23,
        frame_at=lambda t: 0.6 * M.progress(t, t_coat, t_coat + 0.6, "sine"),
        motion=M.sway(1.2, 3.4, pivot=(sx_, sy_)))
    # a butterfly fluttering around the sheaf
    bfr = [butterfly_svg(f) for f in (0.0, 0.5, 1.0, 0.5)]

    def bfly(t):
        x = 420 + 110 * math.sin(2 * math.pi * t / 6.5) + 30 * math.sin(2 * math.pi * t / 2.1)
        y = 900 + 40 * math.sin(2 * math.pi * t / 3.3 + 1.0) + 14 * math.sin(2 * math.pi * t / 0.9)
        return Tf(dx=x, dy=y, rot=8 * math.sin(2 * math.pi * t / 1.7))
    add("butterfly", bfr, motion=bfly, wc=0.3, frame_at=lambda t: float(int(t / 0.06) % 4))
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
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 60)
        add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, f"j1tg{i}", TITLE_COLS[i % len(TITLE_COLS)]),
            motion=pop, title=True, wc=0)

    cam0 = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 + 10, H / 2 + 14, W * 0.93))], "sine")
    cam = lambda th: cam0(th + toff)                                          # noqa: E731
    t_done = onsets[-1] + 0.45

    def gated(f):
        def fx(frame, th, view):
            if gate is not None and gate(th) <= 0:
                return frame
            return f(frame, th + toff, view)
        return fx
    fxs = [
        gated(FX.sparkles((300, 1030, 1900, 1150), count=7, color=(255, 250, 225), size=(7, 13), period=1.9,
                          drift=0, seed=4)),
        gated(FX.sparkles((jx - 110, jy - 330, jx + 90, jy - 30), count=7, t0=t_coat - 0.05, t1=t_coat + 2.2,
                          color=(255, 244, 200), size=(10, 18), period=1.1, drift=-10, seed=6)),
        gated(FX.sparkles((560, 300, 1560, 470), count=6, t0=t_done, color=(255, 240, 190), size=(9, 16),
                          period=2.0, drift=0, seed=9)),
    ]
    info = dict(t_rib=t_rib, onsets=onsets, t_done=t_done, t_hop=t_hop, t_coat=t_coat, t_bleat=t_bleat, t_up=t_up)
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
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-23, fade_in=1.0, fade_out=1.3)
    sc.sfx("sheep", info["t_bleat"], gain_db=-15, pan=0.6)
    sc.sfx("chime", info["t_rib"], gain_db=-10)
    for t in info["onsets"]:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", info["t_coat"], gain_db=-15, pan=0.4)
    return sc
