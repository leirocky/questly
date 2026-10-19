"""Scene 1 — title page: a friendly lion dozing beside the stone-ringed mouth of the lions' den at dawn, the big
round den stone rolled aside, Babylon far away in the golden haze, the sun rising, and the book title.

Beats (from ctx.lines[0], "圣经绘本：但以理和狮子坑。", one chunk):
  start        calm dawn frame (the film fades in over it): the lion lies by the den with sleepy half-closed eyes,
               its tail swishing lazily; two doves glide across the sky; the grass sways a little
  line 0       "圣经绘本" -> the ribbon header unfurls just before the voice (chime); "但以理和狮子坑" -> the seven
               title characters pop in one by one on their syllables (onsets measured in the approved take
               build/daniel/voice/lines/s01_title_00.wav and stored as fractions of the line, see SYL_FRAC)
               on "狮子" the lion wakes (a little perk-up hop): eyes open, then a happy smile
  end          calm hold: happy lion, one slow blink, slow push-in; ambience fades over the dissolve.
"""
import math

from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]
HORIZON = 730
SUN = (1770, 585)
SUN_R = 84
GROUND = 900                 # front edge of the far sand band / start of the foreground
DEN = (700, 1000, 1.1)       # den mouth anchor (view='outside')
STONE = (250, 990, 0.72)     # the den stone, rolled aside
LION = (1330, 1032, 0.95)    # lion lying beside the den, facing left
TITLE = "但以理和狮子坑"
TITLE_Y, TITLE_SIZE, TITLE_STEP = 420, 178, 196
RIB_X, RIB_Y = W / 2, 150
# Onsets of 但 以 理 和 狮 子 坑 in the approved 2.631 s take (s from the clip start: 1.13, 1.35, 1.54, 1.74 (h),
# 1.92 (sh), 2.13 (z), 2.31 (k)), as fractions of the line length so a slightly different take stays close.
SYL_FRAC = (0.429, 0.513, 0.585, 0.661, 0.730, 0.810, 0.878)
CREAM = "#fff6e3"
TAILS = (-0.6, -0.3, 0.0, 0.3, 0.6)


def doc(body, defs=""):
    return S.svg_doc(body, defs)


# ================================================================== drawings


def sky_svg():
    defs = (f'<linearGradient id="d1sky" gradientUnits="userSpaceOnUse" x1="0" y1="-20" x2="0" y2="{HORIZON + 40}">'
            f'<stop offset="0" stop-color="#b3a5d6"/><stop offset="0.35" stop-color="#dcb9d0"/>'
            f'<stop offset="0.7" stop-color="#f6c9a4"/><stop offset="1" stop-color="#fbe2b0"/></linearGradient>' +
            S.rad_grad("d1sunglow", [(0, "#fff4cf", 0.95), (0.3, "#ffe6ad", 0.6), (1, "#ffd9a0", 0)]) +
            S.rad_grad("d1tglow", [(0, "#fff3e2", 0.5), (0.6, "#fbe6dc", 0.2), (1, "#fbe6dc", 0)]))
    b = S.rect_bg("url(#d1sky)")
    b += f'<ellipse cx="{W / 2}" cy="320" rx="900" ry="300" fill="url(#d1tglow)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="480" fill="url(#d1sunglow)"/>'
    return doc(b, defs)


def sun_rays_svg():
    defs = S.rad_grad("d1ray", [(0, "#fff5dc", 1), (0.45, "#fff0d4", 0.55), (1, "#fff0d4", 0)])
    d = S.rays(SUN[0], SUN[1], SUN_R + 20, 380, n=18, width_deg=6.5)
    return doc(S.g(f'<path d="{d}" fill="url(#d1ray)"/>', filter="soft", opacity=0.75), defs)


def sun_svg():
    defs = S.rad_grad("d1sun", [(0, "#fff0b0"), (0.6, P["sun"]), (1, "#f7bd55")], cx=0.45, cy=0.42)
    b = f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="{SUN_R}" fill="url(#d1sun)" stroke="{INK}" stroke-width="3.5"/>'
    b += f'<circle cx="{SUN[0] - 26}" cy="{SUN[1] - 28}" r="20" fill="#fff6d0" opacity="0.6"/>'
    return doc(S.g(b, filter="wobble"), defs)


def clouds_svg():
    shade = "#e8bfc9"
    b = (S.cloud(300, 190, 430, 140, "#fdeee6", seed=31, sw=3.5, shade_fill=shade) +
         S.cloud(90, 360, 220, 78, "#fbe8e2", seed=32, sw=3, shade_fill=shade) +
         S.cloud(1880, 180, 420, 136, "#fdeee6", seed=33, sw=3.5, shade_fill=shade) +
         S.cloud(2050, 360, 200, 70, "#fbe8e2", seed=34, sw=3, shade_fill=shade))
    return doc(S.g(b, filter="wobble"))


def city_svg():
    """Babylon far away in the dawn haze, the sun rising behind it."""
    tint = "#f3cfb4"
    far = PR.nineveh_skyline(-80, W + 80, HORIZON + 30, 0.55, seed=6, haze=0.62, tint=tint)
    return doc(far)


def land_svg():
    """Sand bands: hazy dunes with palms, then the warm foreground ground around the den."""
    defs = (S.lin_grad("d1mid", [(0, "#e9c99a"), (1, "#dcb47c")]) +
            S.lin_grad("d1fg", [(0, "#e2bd84"), (0.5, "#d9ad72"), (1, "#c99a5f")]))
    b = S.path(S.hill(-140, W + 140, HORIZON + 44, 22, seed=3, bumps=5, bottom=H + 60), fill="#e5c7a1", sw=2.5)
    palms = ""
    for x, s, lean in ((180, 0.36, 0.1), (300, 0.3, -0.1), (1240, 0.32, 0.12), (2000, 0.36, -0.1)):
        palms += PR.palm_tree(x, HORIZON + 62, s, lean=lean)
    for x, y, s, v in ((520, 830, 0.42, 0), (760, 805, 0.32, 2), (1560, 818, 0.4, 0), (1880, 840, 0.46, 3),
                       (1330, 795, 0.3, 2)):
        palms += PR.bush(x, y, s, variant=v)
    b = S.g(b, filter="wobble") + PR._haze(palms, "#f3cfb4", 0.45, 0.25)
    fg = S.path(S.hill(-120, W + 120, GROUND, 40, seed=8, bumps=4, bottom=H + 80), fill="url(#d1fg)", sw=4)
    # soft grassy patches and pebbles
    for x, y, rx in ((120, 1050, 170), (1010, 940, 140), (1830, 1080, 220), (1520, 930, 120)):
        fg += (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.22:.0f}" fill="{P["grass"]}" opacity="0.55"/>')
    for x, y, r in ((420, 1110, 12), (1110, 1120, 9), (1730, 980, 10), (1960, 940, 8), (560, 930, 7)):
        fg += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4}" ry="{r}" fill="#cdbfae" stroke="{INK}" stroke-width="2.5"/>'
    return doc(b + S.g(fg, filter="wobble"), defs)


def den_svg(part):
    x, y, s = DEN
    out = PR.lion_den(x, y, s, part=part, view="outside")
    if part == "back":
        out = PR.den_stone(*STONE, roll=-30) + out
    return doc(out)


def tufts_svg(k):
    """Grass and flower tufts in the foreground (3 sway drawings)."""
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((60, 1170, 1.2, 2), (330, 1100, 0.9, 0), (980, 1060, 0.85, 2), (1150, 1150, 1.0, 0),
                       (1710, 1150, 1.1, 2), (2050, 1120, 1.0, 1), (1960, 990, 0.7, 0), (470, 985, 0.7, 2)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


def lion_frames():
    x, y, s = LION
    fr = []
    for eyes in ("half", "open", "happy", "closed"):
        for tl in TAILS:
            fr.append(doc(PR.lion(x, y, s, -1, pose="lie", eyes=eyes, tail=tl)))
    return fr


def lion_shadow_svg():
    x, y, s = LION
    defs = S.rad_grad("d1lsh", [(0, INK, 0.28), (1, INK, 0)])
    return doc(f'<ellipse cx="{x}" cy="{y + 4}" rx="{300 * s:.0f}" ry="{34 * s:.0f}" fill="url(#d1lsh)"/>', defs)


def title_defs():
    return (S.lin_grad("d1tg", [(0, "#4a7fc0"), (0.55, "#2f5f9e"), (1, "#244c82")]) +
            '<filter id="d1tsh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/>'
            '</filter>')


def title_char(ch, x, y):
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{TITLE_SIZE}" text-anchor="middle"'
    b = (f'<text x="{x + 6}" y="{y + 10}" {font} fill="{INK}" opacity="0.28" filter="url(#d1tsh)" '
         f'stroke="{INK}" stroke-width="18" stroke-linejoin="round">{ch}</text>')
    b += f'<text x="{x}" y="{y}" {font} fill="{CREAM}" stroke="{CREAM}" stroke-width="22" stroke-linejoin="round">{ch}</text>'
    b += (f'<text x="{x}" y="{y}" {font} fill="url(#d1tg)" stroke="{INK}" stroke-width="3.5" '
          f'stroke-linejoin="round">{ch}</text>')
    return doc(b, title_defs())


def ribbon_svg():
    cx, cy, hw, h = RIB_X, RIB_Y, 340, 80
    band_col = S.mix(P["terracotta"], "#f0a07a", 0.35)
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
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#f7c9a8" stroke-width="3" '
              f'fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="50" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">圣经绘本 · 但以理书</text>')
    return doc(body)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    say = ctx.lines[0]
    L = say.end - say.start
    onsets = [say.start + f * L for f in SYL_FRAC]
    t_wake = onsets[4] - 0.05            # "狮"
    t_smile = onsets[6] + 0.35
    t_blink = min(say.end + 0.5, T - 1.3)

    sc.add("sky", sky_svg(), wc=0.6)
    sc.add("rays", sun_rays_svg(), wc=0,
           motion=M.combine(M.keys([(0, {"dy": 20}), (T, {"dy": -12})], "sine"),
                            lambda t: Tf(rot=2.0 * t, px=SUN[0], py=SUN[1]), M.pulse(0.75, 1.0, 3.2)))
    sc.add("sun", sun_svg(), motion=M.keys([(0, {"dy": 20}), (T, {"dy": -12})], "sine"))
    sc.add("clouds", clouds_svg(), motion=M.drift(vx=7))
    sc.add("city", city_svg(), wc=0.8)
    sc.add("land", land_svg())
    for i, (y, t0, sp, s) in enumerate(((520, 0.0, 150, 0.5), (640, -0.9, 140, 0.42))):
        ref = (1000, 600)
        frames = [doc(PR.dove(ref[0], ref[1], s, -1, wing=w)) for w in (1.0, 0.4, -0.5, -1.0, -0.4, 0.3)]

        def path(t, y=y, t0=t0, sp=sp, i=i):
            x = 1500 - sp * (t - t0) - 70 * i
            return Tf(dx=x - ref[0], dy=y - ref[1] - 18 * math.sin(1.7 * t + i) - 8 * t)
        sc.add(f"dove{i}", frames, wc=0.6, motion=path,
               frame_at=lambda t, i=i: float(int(t * 10 + 3 * i) % 6) if (t + i) % 2.6 < 1.5 else 0.0)
    sc.add("den_back", den_svg("back"))
    sc.add("lion_shadow", lion_shadow_svg(), wc=0)

    # the lion: half-closed sleepy eyes and a lazy tail swish; it perks up on "狮子" and smiles
    lx, ly, ls = LION
    n = len(TAILS)
    seq = (0, 1, 2, 3, 4, 3, 2, 1)

    def lion_frame(t):
        tail = seq[int(t / 0.22) % len(seq)]
        if t < t_wake:
            eyes = 0
        elif t < t_smile:
            eyes = 1
        elif t_blink <= t < t_blink + 0.16:
            eyes = 3
        else:
            eyes = 2
        return float(eyes * n + tail)
    piv = (lx, ly)
    sc.add("lion", lion_frames(), frame_at=lion_frame, seed=7,
           motion=M.combine(
               M.keys([(t_wake - 0.12, {"dy": 0, "sy": 1}), (t_wake, {"dy": 4, "sy": 0.97}),
                       (t_wake + 0.16, {"dy": -12, "sy": 1.03}), (t_wake + 0.36, {"dy": 0, "sy": 1})],
                      ["in", "out", "sine"], pivot=piv),
               M.breathe(0.012, 2.8, pivot=piv)))
    sc.add("den_front", den_svg("front"))
    sc.add("tufts", [tufts_svg(k) for k in range(3)],
           frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.5) % 4]))

    # ---- title
    t_rib = say.start - 0.1

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=RIB_X, py=RIB_Y)
    sc.add("ribbon", ribbon_svg(), wc=0, motion=unfurl)
    x0 = W / 2 - TITLE_STEP * (len(TITLE) - 1) / 2
    for i, ch in enumerate(TITLE):
        x = x0 + i * TITLE_STEP
        t0 = onsets[i] - 0.06

        def pop(t, t0=t0, x=x, i=i):
            if t < t0:
                return Tf(alpha=0)
            a = min(1.0, (t - t0) / 0.12)
            u = min(1.0, (t - t0) / 0.42)
            s = 0.45 + 0.55 * M.ease("back")(u)
            dy = 30 * (1 - M.ease("out")(u)) + 2.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.16))
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 65)
        sc.add(f"title_{i}", title_char(ch, x, TITLE_Y), wc=0, motion=pop)

    t_done = onsets[-1] + 0.4
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 - 20, H / 2 + 22, W * 0.915))], "sine")
    sc.fx = [
        FX.sparkles((1500, 380, 2060, 520), count=10, color=(255, 244, 210), size=(6, 14), period=1.8, drift=0,
                    seed=3),
        FX.sparkles((150, 250, 330, 470), count=3, t0=t_done, color=(255, 240, 190), size=(9, 17), period=2.0,
                    drift=0, seed=9),
        FX.sparkles((1780, 250, 1960, 470), count=3, t0=t_done, color=(255, 240, 190), size=(9, 17), period=2.0,
                    drift=0, seed=10),
        FX.motes((0, 500, W, 1000), count=24, color=(255, 240, 205), size=(2, 5), alpha=120, seed=12),
    ]
    sc.subtitles = False

    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-16, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-21, fade_in=1.0, fade_out=1.3)
    sc.sfx("chime", t_rib, gain_db=-10)
    sc.sfx("pop", t_wake + 0.02, gain_db=-20)
    return sc
