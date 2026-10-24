"""Scene 1 - title page: a grassy emerald hillside above the Sea of Galilee in warm late-afternoon light (time 0.32). The
boy who will bring his lunch stands on the slope with his little round basket open in his hands - five round barley loaves
and two small dried fish peeking out - smiling. Two big honey wicker baskets of bread sit on the grass beside him (the
twelve baskets to come), red anemones and yellow crown daisies nod in the breeze, a butterfly flits round the baskets,
swallows sail across, soft lit clouds drift, the lake glints below and the disciples' boat drifts far out on the water.
Book title on a lake-teal ribbon (new for this film) with lettering in the colours of a barley loaf.

Beats (keyed to ctx.lines[0] '圣经绘本：五饼二鱼。'; phrase / syllable onsets measured in the voice clip with the Noah
film's voice_marks helpers through the Nativity film's Tm class, fallback: the subtitle chunk, so a re-generated voice
stays in sync):
  start        calm frame (the film fades in over it): the boy looks down into his basket, smiling; clouds, swallows, the
               boat, the butterfly, grass and flowers, glints on the lake, warm motes
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime); the boy looks up at us
  '五饼二鱼'    the four title characters pop in one by one on their syllables (pop); on '五' the boy lifts his open basket
               forward to show the five loaves and two fish (a little hop hides the pose cut; sparkle on the basket);
               on '鱼' he giggles (a happy wiggle)
  end          he lowers the basket again and smiles at us; the finished title holds calmly through the 2.8 s tail with a
               slow push-in, no pose change in the last 1.2 s. s02_question (the park picnic) follows with a plain 1 s
               cross-dissolve composed against this last frame (same camera): the lake-and-hills horizon meets the
               park's skyline at the same height, the green slope meets the lawn, the boy stands just left of where the
               school girl sits with her lunchbox (no faces overlap: the boy of then beside the children of now) and the
               big baskets sit where the two children's picnic will be; the title block dissolves into sky and trees.

Shared with this illustrator's other scenes (s02_question, s09_end): EX (custom expressions), swallow(), CAM_END (the
dissolve's camera).
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
from stories.nativity.scenes.s01_title import Fig, Twinkle, breath, dip, doc, glow_svg, hop, keyed, ribbon_svg  # noqa: F401
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import f1, snap, title_char_svg  # noqa: F401
from stories.zacchaeus.scenes.s01_title import Patch, safe_camera

INK = P["ink"]

TT = 0.25                               # time of day: warm late afternoon, on the way to the golden hour
HY = 1000                               # lake_hillside front line
HX0, HX1 = -70, W + 70
LAKE_Y = 600                            # where the slope meets the lake (the far shore 150 higher)
BOY = (872, 1032, 1.95, -1)            # the boy: feet, scale, facing (toward the title)
BASKETS = [(1268, 966, 1.36, 1.0, 3), (1500, 1004, 1.46, 0.75, 7)]   # x, y, scale, fill, seed (big wicker baskets)
RIB = (690, 146)
RIB_HW = 430
TITLE_X, TITLE_Y, TITLE_SIZE, TITLE_STEP = 690, 412, 172, 198
TITLE_COLS = ("#fff3c8", "#f2c060", "#cf8233")    # barley-loaf gold lettering
RIB_COL = "#2b7f88"                               # a lake-teal ribbon (new for this film)
SUN = (1880, 196)
CAM_START = Cam(W / 2, H / 2, W * 0.985)
CAM_END = Cam(W / 2 + 30, H / 2 + 12, W * 0.94)    # s02_question's first frame is composed against this view


# ================================================================== shared helpers

def EX(name, base, **over):
    """Register a custom expression (a copy of ``base`` with overrides) under a film-unique name; returns the name."""
    key = f"lf1_{name}"
    C.EXPRS.setdefault(key, dict(C.EXPRS[base], **over))
    return key


def swallow(x, y, k=1.0, wing=0, col="#3d4a66", belly="#f4e6d0"):
    """A swallow gliding across the sky (local drawing at x, y): dark blue back, cream belly, long forked tail; wing 0 up,
    1 down."""
    u = -16 if wing == 0 else 9
    st = f'stroke="{INK}" stroke-width="{f1(2.2 * k)}" stroke-linejoin="round" stroke-linecap="round"'
    body = (f'<path d="M{f1(x - 30 * k)},{f1(y + u * k)} Q{f1(x - 12 * k)},{f1(y - 7 * k)} {f1(x)},{f1(y)} '
            f'Q{f1(x + 12 * k)},{f1(y - 7 * k)} {f1(x + 30 * k)},{f1(y + u * k)} Q{f1(x + 12 * k)},{f1(y + 1 * k)} '
            f'{f1(x)},{f1(y + 5 * k)} Q{f1(x - 12 * k)},{f1(y + 1 * k)} {f1(x - 30 * k)},{f1(y + u * k)} Z" fill="{col}" {st}/>')
    body += (f'<path d="M{f1(x - 4 * k)},{f1(y + 3 * k)} L{f1(x - 12 * k)},{f1(y + 20 * k)} L{f1(x - 3 * k)},{f1(y + 12 * k)} '
             f'L{f1(x + 4 * k)},{f1(y + 21 * k)} L{f1(x + 3 * k)},{f1(y + 3 * k)} Z" fill="{col}" {st}/>')
    body += f'<ellipse cx="{f1(x)}" cy="{f1(y + 2 * k)}" rx="{f1(5 * k)}" ry="{f1(6.5 * k)}" fill="{belly}" {st}/>'
    body += f'<circle cx="{f1(x)}" cy="{f1(y - 5 * k)}" r="{f1(4.6 * k)}" fill="{col}" {st}/>'
    return body


def cloud_svg(cx, cy, w, h, pal, seed, rim=0.5):
    """One soft lit cumulus bank (the hillside film's clouds, no ink) on its own layer."""
    return doc(S.g(PR._lf_cloud(cx, cy, w, h, pal, seed, rim_k=rim), filter="wobble"))


def flower_clump(cx, cy, k, sway, seed, n=5, kinds=("anemone", "daisy", "anemone", "white", "daisy"), time=TT):
    """A little clump of Galilee flowers and grass blades (stage px) leaning with the breeze (sway -1..1)."""
    rng = random.Random(seed)
    pal = PR._lf_pal(time)
    out = ""
    for j in range(7):
        bx = cx + rng.uniform(-40, 40) * k
        h_ = rng.uniform(30, 52) * k
        lean = (rng.uniform(-6, 6) + 10 * sway) * k
        out += (f'<path d="M{f1(bx - 4 * k)},{f1(cy + 2)} Q{f1(bx + lean * 0.4)},{f1(cy - h_ * 0.6)} {f1(bx + lean)},{f1(cy - h_)} '
                f'Q{f1(bx + lean * 0.3 + 3 * k)},{f1(cy - h_ * 0.5)} {f1(bx + 4 * k)},{f1(cy + 2)} Z" '
                f'fill="{pal["grass"][2] if j % 2 else pal["grass_dk"]}" stroke="{INK}" stroke-width="{f1(1.6 * k)}"/>')
    for j in range(n):
        fx = cx + rng.uniform(-34, 34) * k
        fy = cy + rng.uniform(-4, 6) * k
        out += PR.galilee_flower(fx, fy, k * rng.uniform(0.85, 1.1), kinds[j % len(kinds)], sway=sway * rng.uniform(0.7, 1.2),
                                 time=time)
    return out


# ================================================================== drawings

def pal():
    return PR._lf_pal(TT)


def sky_svg():
    return doc(PR.galilee_sky(-40, -40, W + 40, LAKE_Y + 350, time=TT, sun=SUN, clouds=0.0, scale=1.0, seed=2))


CLOUDS = [  # cx, cy, w, h, seed, drift px/s
    (250, 92, 430, 128, 1, 3.4),
    (1180, 62, 360, 104, 2, 4.4),
    (1560, 236, 300, 86, 3, 2.6),
    (120, 300, 300, 84, 4, 5.0),
    (840, 268, 250, 70, 5, 3.0),
]


PATH_DX = -770                          # the footpath down to the shore runs left of the boy (not behind him)


def _path_shifted(orig):
    def pts(*a, **kw):
        out = dict(orig(*a, **kw))
        out["path"] = [(x + PATH_DX, y) for x, y in out["path"]]
        return out
    return pts


def hill_svg(part):
    kw = dict(time=TT, seed=4, lake_y=LAKE_Y, rock_x=330, boat=None, flowers=1.0)
    with Patch(lake_hillside_points=_path_shifted(PR.lake_hillside_points)):
        body = PR.lake_hillside(HX0, HX1, HY, 1.0, part=part, **kw)
    return doc(body)


def boat_svg():
    pts = PR.lake_hillside_points(HX0, HX1, HY, 1.0, lake_y=LAKE_Y, seed=4)
    return doc(PR.far_boat(BOAT_X, pts["lake_y"] - 52, 0.1, 1, sail="full", crew=True, time=TT))


BOAT_X = 560


def baskets_svg():
    out = ""
    for x, y, s, fl, sd in BASKETS:
        out += C.ground_shadow(x + 10, y + 2, s, 170, 0.2, color="#1f5a3a")
        out += PR.wicker_basket(x, y, s, 1, fill=fl, food="mixed", time=TT, seed=sd)
    return doc(out)


NSW = 4                                  # sway drawings of the flowers


def flowers_svg(k):
    sway = -1 + 2 * k / (NSW - 1)
    out = ""
    for i, (cx, cy, kk, sd) in enumerate(((1040, 1050, 1.3, 11), (1385, 1000, 1.0, 12), (1640, 1040, 1.3, 13), (1900, 1056, 1.5, 14),
                                         (700, 990, 1.0, 15), (420, 1020, 1.2, 16), (140, 940, 1.1, 17), (1150, 1070, 1.2, 18),
                                         (1800, 880, 0.9, 19))):
        out += flower_clump(cx, cy, kk, sway * (0.8 + 0.1 * (i % 3)), sd)
    return doc(S.g(out, filter="wobble-fine"))


def boy_body(pose, expr, basket="open"):
    x, y, s, f = BOY
    return C.the_boy(x, y, s, f, pose=pose, expr=expr, basket=basket)


def sunwash_svg():
    sx, sy = SUN
    return glow_svg(sx, sy + 80, 1250, 900, "lf1sun", "#fff3cf", "#ffdf9a", 0.5, 0.18)


SWALLOWS = [  # drawn at x, y; enter offset px, speed px/s, size, phase, flap period
    (300, 330, -420, 62, 0.9, 0.0, 0.36),
    (300, 380, -560, 70, 0.75, 0.5, 0.32),
    (1500, 110, 0, -44, 0.7, 0.2, 0.44),
]


# ================================================================== build

def title_onsets(ctx):
    tm = Tm(ctx)
    t_rib = tm.at(0, "圣经") - 0.12
    ons = [tm.at(0, ch) for ch in load_story().TITLE]
    return t_rib, ons


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    t_rib, onsets = title_onsets(ctx)
    t_wu, t_yu = onsets[0], onsets[-1]
    t_done = t_yu + 0.45
    PL = pal()

    # ---------------- sky, clouds, swallows
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    for i, (cx, cy, cw, ch_, sd, v) in enumerate(CLOUDS):
        sc.add(f"cloud{i}", cloud_svg(cx, cy, cw, ch_, PL, sd, 0.5 + 0.1 * i), z=0.2 + 0.01 * i, wc=0.4,
               motion=lambda t, v=v, i=i: Tf(dx=v * t, dy=1.5 * math.sin(2 * math.pi * (t / 7.0 + 0.3 * i))))
    for i, (x0, y0, off, v, k, ph, per) in enumerate(SWALLOWS):
        frames = [doc(swallow(x0, y0, k * 1.1, w)) for w in (0, 1)]

        def flap(t, ph=ph, per=per):
            u = t / per + ph
            return float(int(u * 2) % 2) if u % 4 < 2.2 else 0.0           # a few beats, then a glide
        sc.add(f"swallow{i}", frames, z=0.5 + 0.01 * i, wc=0, seed=60 + i, frame_at=flap,
               motion=lambda t, v=v, ph=ph, off=off: Tf(dx=off + v * t, dy=16 * math.sin(2 * math.pi * (t / 3.2 + ph))))

    # ---------------- the lake, the far hills, the boat, the slope
    sc.add("hill_back", hill_svg("back"), z=1, wc=0.7)
    sc.add("boat", boat_svg(), z=1.1, wc=0.3,
           motion=lambda t: Tf(dx=7.0 * t, dy=1.2 * math.sin(2 * math.pi * t / 2.6), rot=0.8 * math.sin(2 * math.pi * t / 3.1),
                               px=BOAT_X, py=LAKE_Y - 52))
    sc.add("hill_mid", hill_svg("mid"), z=2, wc=0.75)
    sc.add("baskets", baskets_svg(), z=3, wc=0.8)
    sc.add("flowers", [flowers_svg(k) for k in range(NSW)], z=3.2, seed=21,
           frame_at=lambda t: (NSW - 1) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.4 + 0.15))))

    # ---------------- the boy
    bx, by, bs, bf = BOY
    sc.add("boy_shadow", doc(C.ground_shadow(bx + 4, by + 2, bs, 120, 0.24, color="#1f5a3a")), z=3.4, wc=0)
    into = EX("into_basket", "happy", look=(0.03, 0.09))
    into_blink = EX("into_blink", "happy", eyes="closed")
    at_us = EX("boy_at_us", "delighted", look=(-0.06, 0.0))
    show = EX("boy_show", "overjoyed", look=(-0.05, 0.02))
    grin = EX("boy_grin", "happy", look=(-0.06, 0.0), blush=True)
    grin_blink = EX("boy_grin_blink", "happy", eyes="closed", blush=True)

    t_up = snap(t_rib + 0.08)                     # looks up at us as the ribbon opens
    t_show = snap(t_wu - 0.08)                    # lifts the basket forward to show it
    t_down = snap(max(t_done + 0.55, t_yu + 0.9))  # lowers it again, smiling at us
    tb0 = snap(0.85)
    boy = Fig(ctx, "boy", (bx, by), z=3.5, seed=41)
    boy.at(0, boy_body("stand_basket", into))
    boy.at(tb0, boy_body("stand_basket", into_blink)).at(snap(tb0 + 0.13), boy_body("stand_basket", into))
    boy.at(t_up, boy_body("stand_basket", at_us))
    boy.at(t_show, boy_body("offer_up", show))
    boy.at(t_down, boy_body("stand_basket", grin))
    tb1 = snap(t_down + 0.75)
    if tb1 + 0.3 < T - 1.2:
        boy.at(tb1, boy_body("stand_basket", grin_blink)).at(snap(tb1 + 0.13), boy_body("stand_basket", grin))
    giggle = keyed([(t_yu + 0.02, 0.0), (t_yu + 0.16, 1.0), (t_yu + 0.7, 1.0), (t_yu + 0.9, 0.0)], "sine")
    boy.move(hop(t_show, [(-0.12, {"dy": 0, "sy": 1}), (0, {"dy": 7, "sy": 0.95}), (0.13, {"dy": -16, "sy": 1.03}),
                          (0.34, {"dy": 0, "sy": 1})], ["in", "out", "sine"]),
             dip(t_up, 5.0, 0.965), dip(t_down, 6.0, 0.96),
             lambda t: Tf(rot=2.2 * math.sin(2 * math.pi * (t - t_yu) / 0.3) * giggle(t)),
             lambda t: Tf(rot=1.0 * math.sin(2 * math.pi * (t / 3.3 + 0.2))),
             breath(ctx, 0.011, 2.9))
    boy.add(sc)

    # ---------------- the butterfly round the baskets
    def bfly_pos(t):
        u = t / 6.6
        return (1380 + 130 * math.sin(2 * math.pi * u * 0.9 + 0.4) + 30 * math.sin(2 * math.pi * t / 1.7),
                740 - 40 * math.sin(2 * math.pi * u * 1.3) + 14 * math.sin(2 * math.pi * t / 0.9))
    NB = 4
    b0 = bfly_pos(0.0)
    bfr = [doc(PR.butterfly(b0[0], b0[1], 0.62, flap=k / NB, color="orange")) for k in range(NB)]

    def bfly(t):
        x, y = bfly_pos(t)
        return Tf(dx=x - b0[0], dy=y - b0[1], rot=8 * math.sin(2 * math.pi * t / 1.1), px=b0[0], py=b0[1])
    sc.add("butterfly", bfr, z=3.6, seed=51, wc=0.3, frame_at=lambda t: float(int(t * 14) % NB), motion=bfly)

    sc.add("hill_front", hill_svg("front"), z=4, wc=0.8)

    # ---------------- warm light
    sc.add("sunwash", sunwash_svg(), z=4.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.7 + 0.1 * math.sin(2 * math.pi * t / 5.0)))

    # ---------------- title lettering
    story = load_story()
    rx, ry = RIB

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=rx, py=ry)
    sc.add("ribbon", ribbon_svg(story.SUBTITLE, rx, ry, hw=RIB_HW, band_col=RIB_COL, size=42), z=10, motion=unfurl, wc=0)
    title = story.TITLE
    x0 = TITLE_X - TITLE_STEP * (len(title) - 1) / 2
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
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 54)
        sc.add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, grad_id=f"lf1tg{i}", colors=TITLE_COLS),
               z=10.1 + i * 0.01, motion=pop, wc=0)

    # ---------------- camera: a slow push-in
    sc.camera = safe_camera([(0, CAM_START), (T, CAM_END)], "sine")

    # ---------------- sparkle / light / glints
    ox, oy = bx + C.BOY_OFFER[0] * bs * bf, by + C.BOY_OFFER[1] * bs
    sc.fx.append(FX.sparkles((ox - 70, oy - 90, ox + 70, oy - 10), count=6, t0=t_show + 0.1, t1=t_down + 0.2,
                             color=(255, 240, 200), size=(8, 14), period=1.1, drift=-10, seed=7))
    sc.fx.append(FX.sparkles((330, 260, 1060, 450), count=7, t0=t_done, color=(255, 238, 196), size=(9, 16),
                             period=2.0, drift=0, seed=9))
    rng = random.Random(5)
    glints = []
    while len(glints) < 16:
        gx, gy = rng.uniform(40, W - 40), rng.uniform(LAKE_Y - 132, LAKE_Y - 18)
        if 700 < gx < 1040 and gy > LAKE_Y - 70:                 # behind the boy's curls
            continue
        glints.append((gx, gy, rng.uniform(5, 9)))
    sc.fx.append(Twinkle(glints, seed=11, base=0.5, color=(255, 246, 214), period=(1.2, 2.6)))
    sc.fx.append(FX.motes((100, 300, W - 100, 1100), count=16, color=(255, 246, 214), seed=13, alpha=80))
    sc.subtitles = False

    # ---------------- sound
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-24, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-29, fade_in=1.0, fade_out=1.3)
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-33, fade_in=1.0, fade_out=1.3)
    sc.sfx("chime", t_rib, gain_db=-10)
    for t in onsets:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("cloth", t_show - 0.06, gain_db=-22, pan=0.3)
    sc.sfx("sparkle", t_show + 0.12, gain_db=-19, pan=0.3)
    sc.sfx("sparkle", t_done, gain_db=-17)
    return sc
