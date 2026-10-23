"""Scene 1 - title page: a spring hillside in soft morning light (spring_sky / spring_hills, time 0): round clouds drift
across a wide blue sky, the sun glows top right, the parable shepherd leans on his crook on the left and watches his
big flock nibbling all over the hill; a little apart, bottom right, the little lamb (curl, tiny gold bell) has its
nose in a poppy, a yellow butterfly flutters over it. Book title on a lavender ribbon with coral lettering.

Beats (keyed to ctx.lines[0] '圣经绘本：迷失的羊。'; phrase / syllable onsets are measured in the voice clip with the
Noah film's voice_marks helpers, fallback: proportions of the subtitle chunk, so a re-generated voice stays in sync):
  start        calm frame (the film fades in over it): clouds drift, the flock nibbles, flowers and grass sway, the
               lamb sniffs its poppy (its tail wags, its bell swings), the butterfly flutters, the shepherd breathes
               and blinks
  ~0.8 s       a soft baa from the flock
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime)
  '迷失的羊'    the four title characters pop in one by one on their syllables (pop); on '羊' the little lamb lifts
               its head from the flower and smiles up at the butterfly (squash-dip hides the cut; its bell tinkles);
               the shepherd smiles a little wider
  end          calm hold with a slow push-in. s02_question (supermarket) follows with a plain 1 s cross-dissolve:
               the lamb sits about where the walking girl is in s02's first second, sky over the shop's window.

Shared with s02_question / s12_end (same illustrator): EX() custom expressions, lamb_body() (tail / bell life),
cloud_svg(), sway_flowers_svg(), heart_float().
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
from stories.nativity.scenes.s01_title import Fig, beat, breath, dip, doc, glow_svg, keyed, ribbon_svg  # noqa: F401
from stories.noah.scenes.s01_title import char_times, f1, heart_markup, snap, title_char_svg, voice_marks  # noqa: F401

INK = P["ink"]

HY, HS = 960, 0.9                      # spring_hills near ground line and scale
SKY_BOT = HY + 40
SUN = (1868, 168)
SHEP = (330, 1064, 1.0)                # the shepherd: ground point, scale
LAMB = (1496, 1096, 1.36)              # the little lamb: ground point, scale (facing right, away from the flock)
FLOCK_S = 0.8
RIB = (W / 2, 158)
TITLE_Y, TITLE_SIZE, TITLE_STEP = 418, 172, 206
TITLE_COLS = ("#ffcdb0", "#f4886b", "#d65b46")    # poppy-coral lettering
RIB_COL = "#8a70b4"                               # a lavender ribbon (new for this film)


# ================================================================== shared helpers

def EX(name, base, **over):
    """Register a custom expression (a copy of ``base`` with overrides) under a film-unique name; returns the name."""
    key = f"ls1_{name}"
    C.EXPRS.setdefault(key, dict(C.EXPRS[base], **over))
    return key


class _Patch:
    """Temporarily replace attributes of art.props while one drawing is built (markup is generated once at build)."""

    def __init__(self, **kw):
        self.kw, self.old = kw, {}

    def __enter__(self):
        for k, v in self.kw.items():
            self.old[k] = getattr(PR, k)
            setattr(PR, k, v)

    def __exit__(self, *a):
        for k, v in self.old.items():
            setattr(PR, k, v)


def _collar_swing(swing):
    """props._lamb_collar with the little bell swinging ``swing`` degrees on its ring (the ribbon stays put)."""
    def collar(nx, ny, k, rot, time):
        rib = PR._lt(PR.LAMB_RIBBON, time, 0.5)
        bell = PR._lt(PR.LAMB_BELL, time, 0.4)
        out = PR._p(f"M{f1(nx - 12 * k)},{f1(ny - 6 * k)} Q{f1(nx)},{f1(ny + 4 * k)} {f1(nx + 12 * k)},{f1(ny - 8 * k)}",
                    sw=5.5 * k + 2, stroke=INK)
        out += PR._p(f"M{f1(nx - 12 * k)},{f1(ny - 6 * k)} Q{f1(nx)},{f1(ny + 4 * k)} {f1(nx + 12 * k)},{f1(ny - 8 * k)}",
                     sw=5.5 * k, stroke=rib)
        b = PR._p(f"M{f1(nx - 5 * k)},{f1(ny + 6 * k)} Q{f1(nx - 5 * k)},{f1(ny - 1 * k)} {f1(nx)},{f1(ny - 1 * k)} "
                  f"Q{f1(nx + 5 * k)},{f1(ny - 1 * k)} {f1(nx + 5 * k)},{f1(ny + 6 * k)} Z", bell, 2.2)
        b += PR._circ(nx, ny + 7 * k, 1.8 * k, S.shade(bell, -0.45), 0) + PR._circ(nx - 1.8 * k, ny + 1.6 * k, 1.3 * k,
                                                                                 PR.HILITE, 0)
        out += f'<g transform="rotate({swing - rot:.2f} {f1(nx)} {f1(ny - 1 * k)})">{b}</g>'
        return f'<g transform="rotate({rot:.2f} {f1(nx)} {f1(ny)})">{out}</g>'
    return collar


def _cluster_wag(wag):
    """props._cluster that turns the lamb's two-puff tail (radii 7.5 / 5.5) ``wag`` degrees about its root."""
    orig = PR._cluster

    def cl(circles, fill, sw=4.0):
        if len(circles) == 2 and abs(circles[0][2] - 7.5) < 1e-6 and abs(circles[1][2] - 5.5) < 1e-6:
            (x0, y0, r0), (x1, y1, r1) = circles
            px, py = x0 + 7.0, y0 + 3.0
            a = math.radians(wag)
            rot = [(px + (x - px) * math.cos(a) - (y - py) * math.sin(a),
                    py + (x - px) * math.sin(a) + (y - py) * math.cos(a), r) for x, y, r in circles]
            return orig(rot, fill, sw)
        return orig(circles, fill, sw)
    return cl


def lamb_body(x, y, s, f, pose, ph, eyes="open", time=0.0, wag_amp=26.0, swing_amp=16.0, shadow=True):
    """The little lamb with a wagging tail and a swinging bell at loop phase ``ph`` (0..1: two wags, one swing)."""
    wag = wag_amp * math.sin(2 * math.pi * 2 * ph)
    swing = swing_amp * math.sin(2 * math.pi * ph + 0.6)
    with _Patch(_cluster=_cluster_wag(wag), _lamb_collar=_collar_swing(swing)):
        body = PR.little_lamb(x, y, s, f, pose=pose, phase=ph, eyes=eyes, time=time)
    if shadow:
        body = C.ground_shadow(x + 6 * s * f, y, s, 120, 0.2) + body
    return body


def cloud_svg(cx, cy, w, h, seed, time=0.0, sw=3.2):
    pal = PR._ls_pal(time)
    return doc(S.g(PR._ls_cloud(cx, cy, w, h, pal["cloud"], pal["cloud_sh"], pal["rim"], 0.0, seed, sw), filter="wobble"))


def sway_flowers_svg(items, sway, time=0.0, tufts=(), seed=0):
    """Big foreground wildflowers [(x, y, scale, kind)] at one sway value, plus grass tufts [(x, y, h)] leaning with it."""
    rng = random.Random(seed)
    b = ""
    pal = PR._ls_pal(time)
    gcol = S.mix(pal["near"], pal["dark"], 0.62)
    for tx, ty, th in tufts:
        lean = 7 * sway * rng.uniform(0.7, 1.2)
        d = ""
        for j, (dx, hk) in enumerate(((-12, 0.75), (-4, 1.0), (5, 0.9), (13, 0.7))):
            hh = th * hk
            d += (f"M{f1(tx + dx)},{f1(ty)} q{f1(lean * 0.4 + (j - 1.5) * 2)},{f1(-hh * 0.55)} "
                  f"{f1(lean + (j - 1.5) * 5)},{f1(-hh)} ")
        b += f'<path d="{d}" stroke="{gcol}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    for fx_, fy_, fs, kind in items:
        b += PR.wildflower(fx_, fy_, fs, kind, sway=sway * rng.uniform(0.6, 1.0), time=time)
    return doc(S.g(b, filter="wobble-fine"))


def heart_float(sc, name, x0, y0, r, t0, dx=0.0, rise_px=220, life=2.4, z=9.5):
    """A little heart that pops in at t0 and floats up, fading."""
    def m(t):
        if t < t0 or t > t0 + life:
            return Tf(alpha=0.0)
        u = (t - t0) / life
        s_ = M.ease("back")(min(1.0, (t - t0) / 0.35))
        a = min(1.0, (t - t0) / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine"))
        return Tf(dx=dx * u + 9 * math.sin(2 * math.pi * (t - t0) / 1.3), dy=-rise_px * M.ease("out")(u),
                  sx=s_, sy=s_, alpha=a, px=x0, py=y0)
    sc.add(name, doc(heart_markup(x0, y0, r)), z=z, wc=0, motion=m)


# ================================================================== drawings

def sky_svg():
    return doc(PR.spring_sky(-30, -30, W + 30, SKY_BOT, time=0.0, sun=SUN, clouds=0.0, scale=HS, seed=4))


CLOUDS = [  # cx, cy, w, h, seed, drift px/s (the title sits in front of the middle ones)
    (250, 300, 330, 150, 11, 5.0),
    (1340, 560, 300, 128, 12, 4.0),
    (760, 590, 250, 104, 13, 6.0),
    (1660, 352, 280, 120, 14, 3.4),
    (-60, 610, 220, 92, 15, 6.5),
]


def hills_svg(part):
    return doc(PR.spring_hills(-80, W + 80, HY, HS, time=0.0, part=part, stream_x=60, seed=6))


def hill_pts():
    return PR.spring_hills_points(-80, W + 80, HY, HS, stream_x=60, seed=6)


def stream_shimmer_svg(k, n=4):
    """Light glints on the stream (frame k of a loop of n): short pale arcs that come and go."""
    rng = random.Random(17)
    pal = PR._ls_pal(0.0)
    b = ""
    for x, y, hw in hill_pts()["stream"][2:12]:
        for j in range(3):
            u = rng.uniform(-0.55, 0.55)
            ph = rng.random()
            a = 0.5 + 0.5 * math.cos(2 * math.pi * (k / n + ph))
            L = 0.35 * hw
            yy = y + rng.uniform(-4, 10)
            b += (f'<path d="M{f1(x + u * hw - L / 2)},{f1(yy)} q{f1(L / 2)},{f1(-3)} {f1(L)},0" stroke="{pal["water_hi"]}" '
                  f'stroke-width="{f1(2 + hw / 30)}" fill="none" stroke-linecap="round" opacity="{0.85 * a:.2f}"/>')
    return doc(b)


def flock_svg(ph):
    """The flock on the mid hill (behind the meadow's edge)."""
    sx, sy, ss = SHEP
    gaps = [(sx + 40, sy - 60, 230)]
    body = PR.flock(470, W + 60, HY - 150, HY - 30, n=90, scale=FLOCK_S, k_far=0.34, seed=21, phase=ph, time=0.0,
                    top=hill_pts()["mid_top"], gaps=gaps)
    return doc(body)


def near_flock_svg(ph):
    """A few of the hundred grazing on the near meadow, in front of the hill's edge (the lamb keeps apart)."""
    sx, sy, ss = SHEP
    lx, ly, ls = LAMB
    gaps = [(sx + 30, sy - 40, 260), (lx + 40, ly - 30, 330)]
    body = PR.flock(520, 1640, HY - 24, HY + 40, n=15, scale=0.86, k_far=0.78, seed=27, phase=ph, time=0.0, gaps=gaps,
                    poses=("graze", "graze", "graze", "stand", "graze", "look_up", "graze", "lie"))
    return doc(body)


def shepherd_body(expr):
    x, y, s = SHEP
    return C.ground_shadow(x + 4, y, s, 150, 0.2) + C.parable_shepherd(x, y, s, 1, pose="stand", expr=expr)


FRONT_L = [(70, 1150, 1.5, "poppy"), (150, 1176, 1.75, "buttercup"), (235, 1160, 1.35, "daisy"),
           (36, 1104, 1.1, "buttercup"), (300, 1186, 1.6, "poppy")]
FRONT_R = [(1820, 1168, 1.55, "buttercup"), (1930, 1150, 1.4, "daisy"), (2040, 1180, 1.8, "poppy"),
           (1990, 1110, 1.15, "clover"), (2090, 1124, 1.3, "buttercup")]
TUFTS_L = [(10, 1188, 60), (110, 1192, 52), (200, 1196, 66), (340, 1196, 48), (420, 1198, 40)]
TUFTS_R = [(1760, 1196, 46), (1870, 1194, 62), (1980, 1196, 54), (2080, 1192, 66)]
NSW = 5


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    if len(marks) == 1:                       # fallback: the title is the last 4 characters
        ch = ch[-4:]
    return t_rib, ch


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_done = onsets[-1] + 0.45
    t_up = snap(onsets[-1] + 0.02)                  # '羊': the lamb looks up

    # ---------------- sky, sun, clouds
    sc.add("sky", sky_svg(), z=0, wc=0.55)
    for i, (cx, cy, cw, ch_, sd, v) in enumerate(CLOUDS):
        sc.add(f"cloud{i}", cloud_svg(cx, cy, cw, ch_, sd), z=0.5 + 0.01 * i, wc=0.7,
               motion=lambda t, v=v, i=i: Tf(dx=v * t, dy=2.5 * math.sin(2 * math.pi * (t / 7.0 + 0.3 * i))))

    # ---------------- hills, flock, meadow
    sc.add("hills_back", hills_svg("back"), z=1, wc=0.8)
    sc.add("hills_mid", hills_svg("mid"), z=1.5, wc=0.8)
    sc.add("flock", [flock_svg(k / 4) for k in range(4)], z=2, seed=31, frame_at=lambda t: float(int(t / 0.42) % 4))
    sc.add("meadow", hills_svg("front"), z=3, wc=0.8)
    sc.add("shimmer", [stream_shimmer_svg(k) for k in range(4)] + [stream_shimmer_svg(0)], z=3.2, wc=0, seed=35,
           frame_at=lambda t: (t / 0.5) % 4)
    sc.add("near_flock", [near_flock_svg(k / 4 + 0.13) for k in range(4)], z=3.5, seed=33,
           frame_at=lambda t: float(int(t / 0.5 + 1) % 4))
    sc.add("sunwash", glow_svg(SUN[0] - 60, SUN[1] + 40, 1100, 760, "ls1sun", "#fff6da", "#ffe9b0", 0.42, 0.14), z=3.8,
           wc=0, blend="screen", motion=lambda t: Tf(alpha=0.85 + 0.15 * math.sin(2 * math.pi * t / 5.0)))

    # ---------------- the shepherd (breathes, blinks, smiles wider on the title)
    warm, blink, happy = "warm", EX("blink_warm", "warm", eyes="closed"), "happy"
    sx, sy, ss = SHEP
    shep = Fig(ctx, "shepherd", (sx, sy), z=4, seed=41)
    blink_h = EX("blink_happy", "happy", eyes="closed")
    shep.at(0, shepherd_body(warm))
    shep.at(snap(1.25), shepherd_body(blink)).at(snap(1.38), shepherd_body(warm))
    shep.at(snap(onsets[0] + 0.1), shepherd_body(happy))
    shep.at(snap(4.3), shepherd_body(blink_h)).at(snap(4.43), shepherd_body(happy))
    shep.move(breath(ctx, 0.008, 3.4))
    shep.add(sc)

    # ---------------- the little lamb: nose in a poppy, then looks up at the butterfly on '羊'
    lx, ly, ls = LAMB
    lamb = Fig(ctx, "lamb", (lx, ly), z=5, seed=51)
    sniff = [lamb_body(lx, ly, ls, 1, "sniff_flower", k / 8, wag_amp=34) for k in range(8)]
    look = [lamb_body(lx, ly, ls, 1, "stand", k / 8, eyes="happy", wag_amp=32) for k in range(8)]
    lamb.cycle(0, sniff, step=3)
    lamb.cycle(t_up, look, step=3, offset=2)
    lamb.move(dip(t_up, 5.0, 0.95), breath(ctx, 0.012, 2.6, 0.2))
    lamb.add(sc)

    # ---------------- the butterfly over the lamb (a lazy loop; flaps fast while it flies)
    bx0, by0 = lx + 262, ly - 142
    flaps = [doc(PR.spring_butterfly(bx0, by0, 0.8, flap=fl, color="yellow")) for fl in (0.0, 0.2, 0.42, 0.2)]

    def fly(t):
        a = 2 * math.pi * t / 4.6
        return Tf(dx=95 * math.sin(a) + 18 * math.sin(3.1 * a), dy=-34 * math.sin(2 * a) + 10 * math.sin(5.3 * t),
                  rot=8 * math.cos(a), px=bx0, py=by0)
    sc.add("butterfly", flaps, z=5.5, wc=0.3, motion=fly, frame_at=lambda t: float(int(t / 0.06) % 4))

    # ---------------- foreground flowers and tufts sway in the breeze
    for side, items, tufts in ((0, FRONT_L, TUFTS_L), (1, FRONT_R, TUFTS_R)):
        frames = [sway_flowers_svg(items, -1 + 2 * k / (NSW - 1), tufts=tufts, seed=60 + side) for k in range(NSW)]
        sc.add(f"front{side}", frames, z=6 + 0.1 * side, wc=0.6, seed=61 + side,
               frame_at=lambda t, side=side: (NSW - 1) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.3 + 0.27 * side))))

    # ---------------- title lettering
    story = load_story()
    rx, ry = RIB

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=rx, py=ry)
    sc.add("ribbon", ribbon_svg(story.SUBTITLE, rx, ry, band_col=RIB_COL), z=10, motion=unfurl, wc=0)
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
        sc.add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, grad_id=f"ls1tg{i}", colors=TITLE_COLS),
               z=10.1 + i * 0.01, motion=pop, wc=0)

    # ---------------- camera: a slow push-in toward the lamb's side
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.985)), (T, Cam(W / 2 + 30, H / 2 + 6, W * 0.935))], "sine")

    # ---------------- sparkle / light
    sc.fx.append(FX.sparkles((540, 250, 1580, 470), count=7, t0=t_done, color=(255, 236, 196), size=(9, 16),
                             period=2.0, drift=0, seed=9))
    sc.fx.append(FX.sparkles((lx - 40, ly - 190, lx + 160, ly - 60), count=4, t0=t_up, t1=t_up + 1.6,
                             color=(255, 238, 170), size=(7, 12), period=1.1, drift=-10, seed=12))
    sc.fx.append(FX.motes((200, 300, W - 200, 1000), count=14, color=(255, 250, 225), seed=13, alpha=70))
    sc.subtitles = False

    # ---------------- sound
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-24, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-30, fade_in=1.0, fade_out=1.3)
    sc.sfx("sheep", 0.8, gain_db=-25, pan=0.3)
    sc.sfx("chime", t_rib, gain_db=-10)
    for t in onsets:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", t_up + 0.02, gain_db=-21, pan=0.45)
    sc.sfx("sparkle", t_done, gain_db=-18)
    return sc
