"""Scene 1 — title page: the ark resting on a green hill just after the rain, a soft rainbow behind it, animals
peeking out: two giraffes look out of the high window, an elephant stands in the open door waving its trunk, little
birds sit on the roof ridge, a monkey waves from the bow end of the roof, two rabbits wait by the ramp and two ducks
paddle in a puddle. Book title.

Beats (keyed to ctx.lines[0] '圣经绘本：挪亚方舟。'; the phrase / syllable onsets are measured in the voice clip at
build time (voice_marks), falling back to proportions of the subtitle chunk, so a re-generated voice stays in sync):
  start        calm frame (the film fades in over it): clouds drift, grass sways, the birds bob, two little birds fly
               across, the giraffes blink, the ducks paddle
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime)
  '挪亚方舟'    the four title characters pop in one by one on their syllables (pop); on '挪亚' the elephant raises
               its trunk (hard pose cut hidden by a squash dip), on '方舟' the monkey waves
  end          calm hold with a slow push-in. s02_rain opens with a plain cross-dissolve on this very page: it calls
               title_page(..., toff) so its first second is exactly this scene's last second.

The voice-timing helpers (voice_marks / mark / char_times) are shared by the other scenes of this illustrator
(s02_rain, s03_world, s14_end).
"""
import itertools
import math
import random
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
PUNCT = "，。？！：；、…,.?!:;"

ARK = (1060, 985, 0.46)          # grounded ark anchor (ground under the keel middle), scale
TITLE_Y, TITLE_SIZE, TITLE_STEP = 470, 170, 200
RIB_X, RIB_Y = W / 2, 262
RAINBOW = (1056, 1010, 0.9)
GIR_S = ARK[2]
ELE_S = ARK[2] * 0.9


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


# ================================================================== voice timing (shared helpers)

_SEG_CACHE = {}


def _clip_segments(path):
    """Speech segments (start, end) in seconds from the clip start (10 ms energy frames, gaps >= 50 ms)."""
    key = str(path)
    if key in _SEG_CACHE:
        return _SEG_CACHE[key]
    import soundfile as sf
    x, sr = sf.read(str(path), dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    hop = int(sr * 0.01)
    n = len(x) // hop
    e = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1))
    e = e / max(1e-6, e.max())
    on = e > 0.05
    segs, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            segs.append([s, i])
            s = None
    if s is not None:
        segs.append([s, n])
    merged = []
    for a, b in segs:
        if merged and a - merged[-1][1] < 5:
            merged[-1][1] = b
        elif b - a >= 3:
            merged.append([a, b])
    out = [(a * 0.01, b * 0.01) for a, b in merged]
    _SEG_CACHE[key] = out
    return out


def _split(text):
    out, cur = [], ""
    for ch in text:
        if ch in PUNCT:
            if cur:
                out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _proportional(t0, t1, phrases):
    n = sum(len(p) for p in phrases) + 0.5 * (len(phrases) - 1)
    out, acc = [], 0.0
    for p in phrases:
        a = t0 + (t1 - t0) * acc / n
        acc += len(p)
        b = t0 + (t1 - t0) * acc / n
        acc += 0.5
        out.append((a, b))
    return out


def voice_marks(ctx, li):
    """[(phrase text, start, end, [speech sub-segments])] for every punctuation-separated phrase of line ``li``, in
    seconds from the scene start. Chunk times are the anchors; inside a chunk the phrase boundaries are the pauses
    found in the voice clip (best match to the character-count estimate); fallback: proportional."""
    ln = ctx.lines[li]
    key = (ctx.id, li)
    if key in _SEG_CACHE:
        return _SEG_CACHE[key]
    try:
        segs = _clip_segments(BUILD / "voice" / "lines" / f"{ctx.id}_{li:02d}.wav")
        segs = [(ln.start + a, ln.start + b) for a, b in segs]
    except Exception as ex:                                  # missing clip: proportional timing
        print(f"[{ctx.id}] voice clip unreadable ({ex}); proportional timing", file=sys.stderr)
        segs = []
    chunks = ln.chunks or [ln]
    out = []
    for ci, ch in enumerate(chunks):
        phrases = _split(ch.text)
        lo = ch.start - 0.25
        hi = chunks[ci + 1].start - 0.1 if ci + 1 < len(chunks) else ch.end + 0.3
        mine = [s for s in segs if lo <= (s[0] + s[1]) / 2 <= hi]
        if not mine:
            for (a, b), p in zip(_proportional(ch.start, ch.end, phrases), phrases):
                out.append((p, a, b, [(a, b)]))
            continue
        s0, s1 = mine[0][0], mine[-1][1]
        if len(phrases) == 1:
            out.append((phrases[0], s0, s1, mine))
            continue
        est = _proportional(s0, s1, phrases)
        gaps = [(i, mine[i][1], mine[i + 1][0]) for i in range(len(mine) - 1)]
        k = len(phrases) - 1
        best = None
        if len(gaps) >= k:
            for combo in itertools.combinations(gaps, k):
                cost = 0.0
                for j, (_, ga, gb) in enumerate(combo):
                    cost += abs((ga + gb) / 2 - (est[j][1] + est[j + 1][0]) / 2) - 2.0 * min(gb - ga, 0.35)
                if best is None or cost < best[0]:
                    best = (cost, combo)
        if best is None:
            for (a, b), p in zip(est, phrases):
                out.append((p, a, b, [(a, b)]))
            continue
        cuts = [g[0] for g in best[1]]
        start_i = 0
        for j, p in enumerate(phrases):
            end_i = cuts[j] if j < k else len(mine) - 1
            sub = mine[start_i:end_i + 1]
            out.append((p, sub[0][0], sub[-1][1], sub))
            start_i = end_i + 1
    _SEG_CACHE[key] = out
    return out


def char_times(mark_entry):
    """Onset of every character of one phrase (speech time spread evenly over its sub-segments)."""
    text, a, b, subs = mark_entry
    total = sum(e - s for s, e in subs) or (b - a)
    out = []
    for i in range(len(text)):
        want = total * i / len(text)
        acc = 0.0
        for s, e in subs:
            if acc + (e - s) > want + 1e-6:
                out.append(s + want - acc)
                break
            acc += e - s
        else:
            out.append(b)
    return out


def mark(ctx, phrase, li=None, end=False):
    """Start (or end) time of ``phrase``: the measured phrase containing it, plus its character offset inside."""
    lines = [li] if li is not None else range(len(ctx.lines))
    for i in lines:
        for ent in voice_marks(ctx, i):
            if phrase in ent[0]:
                if end:
                    return ent[2]
                k = ent[0].index(phrase)
                return char_times(ent)[k] if k else ent[1]
    raise KeyError(phrase)


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    """[(t, frame index)] -> frame_at with hard cuts."""
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


def dip(t0, s, pivot, depth=9.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=pivot)


def heart_markup(x, y, r, fill="#e98a8a"):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.2)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.2)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} "
         f"{f1(x)},{f1(y + r * 0.9)} Z")
    return S.g(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{max(2.5, r * 0.15):.1f}" '
               f'stroke-linejoin="round"/><ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.3)}" '
               f'rx="{f1(r * 0.18)}" ry="{f1(r * 0.12)}" fill="#fbd0c4"/>', filter="wobble-fine")


def title_char_svg(ch, x, y, size, grad_id="n1tg", colors=("#ec8a45", "#d0632f", "#b04d26")):
    """One big picture-book title character: soft shadow, cream halo, warm gradient fill, ink outline."""
    defs = (S.lin_grad(grad_id, [(0, colors[0]), (0.55, colors[1]), (1, colors[2])]) +
            '<filter id="n1tsh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/>'
            '</filter>')
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b = (f'<text x="{x + 6}" y="{y + 10}" {font} fill="{INK}" opacity="0.28" filter="url(#n1tsh)" '
         f'stroke="{INK}" stroke-width="18" stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="{CREAM}" stroke="{CREAM}" stroke-width="22" '
          f'stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="url(#{grad_id})" stroke="{INK}" stroke-width="3.5" '
          f'stroke-linejoin="round">{ch}</text>')
    return doc(b, defs)


# ================================================================== drawings

def sky_svg():
    defs = (S.lin_grad("n1sky", [(0, "#8cc7e0"), (0.45, "#b9dfe8"), (0.78, "#e2efe0"), (1, "#f6eed4")]) +
            S.rad_grad("n1sun", [(0, "#fff7d8", 0.95), (0.4, "#fff0c4", 0.45), (1, "#fff0c4", 0)]))
    b = S.rect_bg("url(#n1sky)")
    b += '<circle cx="230" cy="120" r="520" fill="url(#n1sun)"/>'
    return doc(b, defs)


def rainbow_svg():
    x, y, s = RAINBOW
    return doc(S.g(PR.rainbow(x, y, s), opacity=0.82))


def clouds_svg():
    sh = "#d3e3ec"
    b = (S.cloud(380, 250, 300, 92, "#fbf6ec", seed=31, sw=3.5, shade_fill=sh) +
         S.cloud(1700, 190, 340, 104, "#fbf6ec", seed=32, sw=3.5, shade_fill=sh) +
         S.cloud(1180, 120, 180, 56, "#f8f3ea", seed=33, sw=2.8, shade_fill=sh) +
         S.cloud(-80, 520, 260, 80, "#f8f3ea", seed=34, sw=3, shade_fill=sh) +
         S.cloud(2160, 560, 300, 86, "#f8f3ea", seed=35, sw=3, shade_fill=sh))
    # the last grey rain cloud drifting away at the right edge
    b += S.cloud(2120, 330, 420, 130, "#b9c3d1", seed=36, sw=3.5, shade_fill="#9aa6b8")
    return doc(S.g(b, filter="wobble"))


def far_svg():
    b = S.path(S.hill(-200, W + 200, 860, 120, seed=11, bumps=4), fill="#b9cfd4", sw=2.2)
    b += S.path(S.hill(-200, W + 200, 930, 90, seed=12, bumps=5), fill="#a8c79d", sw=2.6)
    trees = ""
    for x, y, s in ((210, 905, 0.3), (370, 918, 0.26), (1830, 902, 0.3), (1980, 915, 0.26)):
        trees += PR.olive_tree(x, y, s, seed=int(x))
    return doc(S.g(b, filter="wobble") + PR._haze(trees, "#c4d9c4", 0.4, 0.4))


HILL_PTS = [(-140, 1075), (200, 1045), (520, 1000), (760, 986), (1060, 985), (1400, 986), (1640, 994),
            (1900, 1032), (2260, 1075)]


def hill_svg():
    d = S.smooth_path(HILL_PTS, closed=False) + f" L2260,{H + 60} L-140,{H + 60} Z"
    defs = S.lin_grad("n1hill", [(0, "#a8cc66"), (0.5, "#93b85c"), (1, "#7fa64d")])
    b = S.path(d, fill="url(#n1hill)", sw=4)
    for x, y, rx in ((400, 1090, 220), (1100, 1060, 260), (1750, 1100, 200)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.14:.0f}" fill="#b9d878" opacity="0.6"/>'
    rng = random.Random(7)
    fl = ""
    for _ in range(60):
        x = rng.uniform(-40, W + 40)
        y = rng.uniform(1010, 1180)
        if 600 < x < 1560 and y < 1030:
            continue
        col = rng.choice(["#f6d36b", "#fbf3e3", "#f2a6a0", "#c9b6e4"])
        r = rng.uniform(5, 8)
        fl += (f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
               f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.35)}" fill="#e7a23c"/>')
    bushes = PR.bush(240, 1050, 0.7, variant=1) + PR.bush(1930, 1048, 0.75, variant=3)
    return doc(S.g(b, filter="wobble") + bushes + S.g(fl, filter="wobble-fine"), defs)


def ark_svg():
    x, y, s = ARK
    shadow = f'<ellipse cx="{x + 40}" cy="{y + 4}" rx="{460}" ry="22" fill="{INK}" opacity="0.16" filter="url(#soft)"/>'
    return doc(shadow + PR.ark(x, y, s, 1, door=1.0, window=1.0))


def ark_pts():
    x, y, s = ARK
    return PR.ark_points(x, y, s, 1)


def giraffes_svg(blink=False, look=0):
    """Two giraffes looking out of the high window (clipped to the opening)."""
    x, y, s = ARK
    wb = ark_pts()["window_box"]
    wx0, wy0, wx1, wy1 = wb
    ga = PR.ark_animal(wx0 - 52, wy1 + 232 + look, GIR_S, 1, kind="giraffe", eyes="closed" if blink else "open")
    gb = PR.ark_animal(wx1 + 48, wy1 + 224, GIR_S, -1, kind="giraffe", female=True)
    return doc(PR.in_ark_window(gb + ga, x, y, s, 1))


def elephant_svg(pose):
    x, y, s = ARK
    p = ark_pts()
    sill = p["door_box"][3]
    ex = p["door_box"][2] - 80
    ele = PR.ark_animal(ex, sill, ELE_S, 1, kind="elephant", pose=pose)
    return doc(PR.in_ark_door(ele, x, y, s, 1))


RIDGE_Y = None


def bird_svg(i, kind, x, color=None, flap=False):
    ry = ark_pts()["roof_mid"][1]
    if kind == "dove":
        s = 0.5
        b = PR.dove(x, ry - 38 * s, s, 1 if i % 2 else -1, pose="stand")
    else:
        s = 0.55
        if flap:
            b = PR.songbird(x, ry - 32 * s - 6, s, 1 if i % 2 else -1, wing=flap, pose="fly", color=color)
        else:
            b = PR.songbird(x, ry - 32 * s, s, 1 if i % 2 else -1, pose="perch", color=color)
    return doc(b)


BIRDS = [(0, "song", 845, "blue"), (1, "dove", 965, None), (2, "song", 1150, "red"), (3, "song", 1255, "yellow")]


def monkey_svg(pose):
    p = ark_pts()
    return doc(PR.ark_animal(MONKEY[0], MONKEY[1], ARK[2], 1, kind="monkey", pose=pose))


RAB = (1650, 1003)
MONKEY = (1440, 690)
DUCKS = (430, 1052)


def rabbits_svg(phase=None):
    x, y = RAB
    s = ARK[2]
    sh = C.ground_shadow(x + 20, y + 2, s, 220, 0.18)
    if phase is None:
        return doc(sh + PR.animal_pair("rabbit", x, y, s, -1, pose="stand"))
    return doc(sh + PR.animal_pair("rabbit", x, y, s, -1, pose="hop", phase=phase))


def puddle_svg(k):
    x, y = DUCKS
    return doc(PR.puddle(x + 10, y - 6, 1.05, width=300, ripple=k / 4, sky="#b9dfe8"))


def ducks_svg(k):
    x, y = DUCKS
    s = ARK[2] * 1.1
    dx = 6 * math.sin(2 * math.pi * k / 4)
    return doc(PR.ark_animal(x - 50 + dx, y - 4, s, 1, kind="duck", pose="swim") +
               PR.ark_animal(x + 70 - dx, y - 10, s * 0.94, -1, kind="duck", pose="swim", female=True))


FG = [(30, 1190, 1.2, 2), (300, 1170, 0.9, 0), (720, 1185, 1.0, 2), (1060, 1192, 0.9, 0), (1420, 1182, 1.1, 2),
      (1780, 1176, 0.9, 0), (2080, 1190, 1.2, 1), (560, 1105, 0.6, 0), (1560, 1095, 0.6, 2)]


def tufts_svg(k):
    out = ""
    for x, y, s, v in FG:
        out += PR.grass_tuft(x, y, s, variant=v, sway=0.45 * math.sin(k * 2.1 + x * 0.013))
    return doc(out)


def flyer_svg(color, wing):
    return doc(PR.songbird(0 + 200, 200, 0.5, 1, wing=wing, color=color))


def ribbon_svg(text):
    cx, cy, hw, h = RIB_X, RIB_Y, 330, 78
    band_col = "#3f8f8c"
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
        b += (f'<path d="M{cx - hw + 18},{yy} Q{cx},{q} {cx + hw - 18},{yy}" stroke="#9fd0c8" stroke-width="3" '
              f'fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="46" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">{text}</text>')
    return doc(body)


# ================================================================== the page (shared with s02)


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    if len(marks) == 1:                       # fallback: the title is the last 4 characters
        ch = ch[-4:]
    return t_rib, ch


def title_page(sc, ctx, toff=0.0, gate=None, title_gate=None):
    """Add the whole title page to ``sc``. Times inside are s01's; ``toff`` is added to the host scene's clock
    (s02 passes the offset between the two scene starts). ``gate(t_host)`` multiplies every layer's alpha (s02
    hides the page once covered); ``title_gate`` multiplies the lettering only. Returns (camera(t_host), fx, info)."""
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_trunk = snap(onsets[0] + 0.05)
    t_monkey = snap(onsets[2] + 0.05)

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
        sc.add(f"n1_{name}", svg, motion=mot if need else None,
               frame_at=(lambda th, fa=fa: fa(th + toff)) if fa else None, **kw)

    add("sky", sky_svg(), wc=0.6)
    add("rainbow", rainbow_svg(), wc=0.35)
    add("clouds", clouds_svg(), motion=M.drift(vx=7))
    add("far", far_svg())

    # two little birds flying across the sky (wing cycle)
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (col, y0, vx, ph) in enumerate((("blue", 330, 95, 0.0), ("yellow", 395, 82, 0.4))):
        def fly(t, y0=y0, vx=vx, ph=ph, i=i):
            x = -260 + 420 * i + vx * t
            return Tf(dx=x, dy=y0 - 200 + 28 * math.sin(2 * math.pi * (t / 2.2 + ph)))
        add(f"flyer{i}", [flyer_svg(col, w) for w in wings], motion=fly, wc=0.3,
            frame_at=lambda t, ph=ph: float(int(t / 0.07 + ph * 8) % 8))

    add("hill", hill_svg())
    add("ark", ark_svg())

    # giraffes in the window: a blink now and then, the near one lifts its head a little
    gfr = [giraffes_svg(), giraffes_svg(blink=True), giraffes_svg(look=-8)]
    gents = [(0, 0)]
    for tb in (0.9, 2.7, 4.6, 6.4, 8.2):
        gents += [(snap(tb), 1), (snap(tb + 0.14), 0)]
    gents += [(snap(3.05), 2), (snap(3.05 + 1.3), 0)]
    gents = sorted(gents)
    add("giraffes", gfr, frame_at=cuts(gents), seed=13)

    # the elephant in the door: trunk up on '挪亚', down again, up again later
    p = ark_pts()
    sill = p["door_box"][3]
    epiv = (p["door_box"][2] - 80, sill)
    efr = [elephant_svg("stand"), elephant_svg("trunk_up")]
    e_cuts = [t_trunk, snap(t_trunk + 1.15), snap(t_trunk + 2.3), snap(t_trunk + 3.4)]
    add("elephant", efr, frame_at=cuts([(0, 0), (e_cuts[0], 1), (e_cuts[1], 0), (e_cuts[2], 1), (e_cuts[3], 0)]),
        motion=M.combine(*[dip(tc, ELE_S, epiv, 9) for tc in e_cuts],
                         M.breathe(0.008, 2.6, pivot=epiv)), seed=17)

    # birds on the roof ridge: little bobs and hops; the red one flutters up once
    ry = p["roof_mid"][1]
    for i, kind, x, col in BIRDS:
        fr = [bird_svg(i, kind, x, col)]
        flutter = kind == "song" and i == 2
        if flutter:
            fr += [bird_svg(i, kind, x, col, flap=w) for w in (1.0, -0.8)]
        hops = [0.6 + i * 1.3 + k * 4.1 for k in range(3)]
        tf0 = snap(2.0)

        def bmot(t, x=x, hops=hops, i=i, flutter=flutter, tf0=tf0):
            dy = 0.0
            for th in hops:
                u = t - th
                if 0 <= u < 0.32 and not (flutter and tf0 - 0.4 < th < tf0 + 1.0):
                    dy -= 16 * math.sin(math.pi * u / 0.32)
            dy += 1.5 * math.sin(2 * math.pi * (t / 1.3 + i * 0.27))
            u = t - tf0
            if flutter and 0 <= u < 0.7:
                dy -= 40 * math.sin(math.pi * u / 0.7)
            return Tf(dy=dy, px=x, py=ry)
        kw = {}
        if flutter:
            kw["frame_at"] = lambda t, tf0=tf0: (1.0 + float(int((t - tf0) / 0.07) % 2)) if tf0 <= t < tf0 + 0.7 \
                else 0.0
        add(f"bird{i}", fr, motion=bmot, seed=20 + i, wc=0.6, **kw)

    # the monkey on the bow end of the roof: waves on '方舟' and again later
    mpiv = MONKEY
    mfr = [monkey_svg("sit"), monkey_svg("wave")]
    mc = [t_monkey, snap(t_monkey + 1.6)]
    add("monkey", mfr, frame_at=cuts([(0, 0), (mc[0], 1), (mc[1], 0)]),
        motion=M.combine(dip(mc[0], ARK[2], mpiv, 8), dip(mc[1], ARK[2], mpiv, 8),
                         lambda t: Tf(rot=6 * math.sin(2 * math.pi * (t - mc[0]) / 0.7) if mc[0] + 0.2 < t < mc[1] - 0.1
                                      else 0.0, px=mpiv[0], py=mpiv[1])), seed=29)

    # rabbits by the ramp: one little hop in place now and then
    rfr = [rabbits_svg()] + [rabbits_svg(ph) for ph in (0, .25, .5, .75)]
    hop_t = [1.3, 4.7]

    def rab_fa(t):
        for th in hop_t:
            u = t - th
            if 0 <= u < 0.4:
                return 1.0 + float(min(3, int(u / 0.1)))
        return 0.0
    add("rabbits", rfr, frame_at=rab_fa, seed=31)

    # ducks paddling in a puddle
    add("puddle", [puddle_svg(k) for k in range(4)], frame_at=lambda t: float(int(t / 0.25) % 4), wc=0.5)
    add("ducks", [ducks_svg(k) for k in range(4)], frame_at=lambda t: float(int(t / 0.3) % 4), seed=33)
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
        add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE), motion=pop, title=True, wc=0)

    cam0 = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 - 10, H / 2 + 12, W * 0.93))], "sine")
    cam = lambda th: cam0(th + toff)                                          # noqa: E731
    t_done = onsets[-1] + 0.45

    def gated(f):
        def fx(frame, th, view):
            if gate is not None and gate(th) <= 0:
                return frame
            return f(frame, th + toff, view)
        return fx
    fxs = [
        gated(FX.sparkles((420, 1010, 1700, 1150), count=7, color=(255, 250, 225), size=(7, 13), period=1.9,
                          drift=0, seed=4)),
        gated(FX.sparkles((560, 330, 1560, 520), count=6, t0=t_done, color=(255, 240, 190), size=(9, 16),
                          period=2.0, drift=0, seed=9)),
    ]
    info = dict(t_rib=t_rib, onsets=onsets, t_done=t_done, t_trunk=t_trunk)
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
    sc.sfx("drip", 0, dur=T + 0.3, gain_db=-26, fade_in=1.0, fade_out=1.3)
    sc.sfx("chime", info["t_rib"], gain_db=-10)
    for t in info["onsets"]:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", info["t_done"], gain_db=-17)
    return sc
