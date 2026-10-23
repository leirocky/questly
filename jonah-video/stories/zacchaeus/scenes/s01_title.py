"""Scene 1 - title page: the big sycamore-fig (桑树 = Ficus sycomorus) stands on the verge of a dusty road in Jericho, the
city of palms, under a hazy turquoise sky in warm golden afternoon light. The road winds in from the little town on the
horizon (sandstone houses among date palms, the striped cliffs of the Jordan valley behind) and passes right under the
tree's sitting branch. Zacchaeus is hidden in the leaves: he pushes them aside and peeks out with a big smile; a little
hoopoe hops along his branch. Book title on a palm-green ribbon with saffron-to-terracotta lettering.

Beats (keyed to ctx.lines[0] '圣经绘本：撒该爬上桑树。'; phrase / syllable onsets are measured in the voice clip with the
Noah film's voice_marks helpers (fallback: proportions of the subtitle chunk), so a re-generated voice stays in sync):
  start        calm frame (the film fades in over it): the leaves stir, palms sway, desert wisps and swifts drift, the
               hoopoe preens on the branch, dust motes float in the warm light; Zacchaeus is still hidden behind a
               clump of big leaves (his feet dangle below it, a sliver of his head-cloth peeks out)
  ~0.65 s      the clump quivers ...
  ~1.15 s      ... and he pushes it up and aside: Zacchaeus leans out ('peek', eager), looking down the road
               (cloth rustle + pop); his raised hand keeps holding the leaves aside
  '圣经绘本'    the ribbon header (story.SUBTITLE) unfurls just before the voice (chime); the hoopoe hops toward him
  '撒该'        on the first syllable he turns to us with a big smile (squash-dip hides the expression cut)
  '爬上桑树'    the six title characters pop in one by one on their syllables (pop); on '桑' the hoopoe hops once more
               and sings (a little note), on '树' Zacchaeus giggles (a happy wiggle)
  end          the finished title holds calmly (2.4 s tail) with a slow push-in. s02_question (the street festival)
               follows with a plain 1 s cross-dissolve: the tree and Zacchaeus sit on the right where the boy and his
               dad stand in s02's first second, the title block on the left where the parade float and bunting are; no
               sun disk is drawn here (the warm light comes from the upper left) so the festival's sun mascot never
               doubles with a sky sun.

Shared helpers for this illustrator's other scenes (s02_question, s11_end): EX (custom expressions), Patch (temporarily
replace art.props attributes while a drawing is built), hoopoe(), confetti fx, swift().
"""
import math
import random

from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import load_story
from engine.scene import Scene
from stories.nativity.scenes.s01_title import Fig, breath, dip, doc, glow_svg, hop, keyed, ribbon_svg  # noqa: F401
from stories.noah.scenes.s01_title import char_times, f1, snap, title_char_svg, voice_marks  # noqa: F401

INK = P["ink"]

TT = 0.22                               # Jericho time of day: warm afternoon turning golden
HZ = 768                                # horizon (the foot of the far hills)
TREE = (1708, 1058, 0.9, -1)            # the sycamore-fig: foot of the trunk, scale, facing (sitting branch to the left)
RIB = (676, 150)                        # ribbon centre
RIB_HW = 392
TITLE_X, TITLE_Y, TITLE_SIZE, TITLE_STEP = 676, 400, 138, 145
TITLE_COLS = ("#fff1c0", "#f5b444", "#cf6430")    # saffron to terracotta lettering
RIB_COL = "#3f7d56"                               # a date-palm green ribbon (new for this film)
GLOW = (60, -40)                                  # the warm light comes from beyond the upper-left corner


# ================================================================== shared helpers

def EX(name, base, **over):
    """Register a custom expression (a copy of ``base`` with overrides) under a film-unique name; returns the name."""
    key = f"zq1_{name}"
    C.EXPRS.setdefault(key, dict(C.EXPRS[base], **over))
    return key


class Patch:
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


def cam_inside(c, w=W, h=H):
    """True if the camera viewport lies inside the painted stage."""
    hw, hh = c.w / 2, c.w * 9 / 32
    return c.x - hw >= -0.01 and c.x + hw <= w + 0.01 and c.y - hh >= -0.01 and c.y + hh <= h + 0.01


def clamp_cam(c, w=W, h=H):
    """Keep the camera viewport inside the painted stage (no unpainted edges)."""
    cw = min(c.w, w, h * 16 / 9)
    hw, hh = cw / 2, cw * 9 / 32
    return Cam(min(max(c.x, hw), w - hw), min(max(c.y, hh), h - hh), cw, c.rot)


def safe_camera(keys, curve="sine", w=W, h=H):
    """M.cam_keys with every keyframe asserted inside the stage and every in-between frame clamped to it."""
    for tk, c in keys:
        assert cam_inside(c, w, h), f"camera key at {tk:.2f}s leaves the {w}x{h} stage: {c}"
    f = M.cam_keys(keys, curve)
    return lambda t: clamp_cam(f(t), w, h)


def stepped(n, per, ph=0.0, blend=0.08):
    """frame_at for a looping flipbook of n drawings plus a repeat of drawing 0 at the end (n + 1 frames): each drawing
    holds, then blends into the next over ``blend`` seconds only (no long double-exposed crossfades)."""
    step = per / n
    k = min(1.0, blend / step)

    def fa(t):
        u = ((t / per + ph) % 1.0) * n
        i = math.floor(u)
        fr = u - i
        return i + (0.0 if fr < 1 - k else (fr - (1 - k)) / k)
    return fa


def tree_pts():
    return PR.sycomore_points(*TREE)


def branch_top(lx):
    """Stage point on top of the sitting branch at local x ``lx`` (the tree's own limb geometry)."""
    tx, ty, ts, tf = TREE
    ly = PR._syco_branch_top(PR._SYCO_L2, PR._SYCO_L2_W, lx)
    return PR.local_to_stage(tx, ty, ts, tf, lx, ly)


HOOPOE = ("#eaa46c", "#d98852", "#3a3030", "#f6ecd8")     # cinnamon body, its shade, black, cream bars


def _hoopoe(pose="perch", crest=0.0, beak=0.0, look=0.0, key="a"):
    """A little hoopoe of the Jordan valley (local, anchor = its feet on the perch, facing right, ~80 px long at scale 1):
    a cinnamon body, a crest of black-tipped feathers, a long thin down-curved beak, black-and-cream barred wing and tail.
    pose 'perch' | 'crouch' (about to hop) | 'hop' (in the air, wing up) | 'preen' (head down to the wing); crest 0
    (folded back) .. 1 (fanned up); beak 0..1 opens it (singing); look tilts the head (deg)."""
    body, body_dk, blk, wht = HOOPOE
    st = f'stroke="{INK}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"'
    leg = 'fill="none" stroke="#6a5a5a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    out = ""
    by = -24 + {"perch": 0, "crouch": 6, "hop": -3, "preen": 2}[pose]
    if pose != "hop":
        for lx in (-4, 6):
            out += f'<path d="M{lx},{by + 10} L{lx + 2},{by + (17 if pose == "crouch" else 16)} L{lx},0 M{lx - 4},0 L{lx + 6},0" {leg}/>'
    else:
        out += f'<path d="M-2,{by + 12} q-6,6 -11,4 M6,{by + 12} q-4,7 -10,6" {leg}/>'
    tu = {"perch": 0, "crouch": -7, "hop": 7, "preen": -2}[pose]
    out += f'<path d="M-16,{by - 2} L-46,{by + 2 + tu} L-45,{by + 12 + tu} L-15,{by + 8} Z" fill="{blk}" {st}/>'
    out += f'<path d="M-35,{f1(by + 1 + tu * 0.7)} L-36,{f1(by + 10.5 + tu * 0.7)}" stroke="{wht}" stroke-width="5"/>'
    out += f'<ellipse cx="0" cy="{by}" rx="21" ry="14.5" fill="{body}" {st} transform="rotate(-12 0 {by})"/>'
    out += f'<path d="M-4,{by + 6} Q6,{by + 15} 16,{by + 3}" fill="none" stroke="{body_dk}" stroke-width="2.4" opacity="0.6"/>'
    hx, hy = (10, by - 10) if pose == "preen" else (15, by - 15)
    c = max(0.0, min(1.0, crest))
    hd = ""
    for k in range(5):
        a = math.radians((-176 + 8 * k) + ((-166 + 30 * k) - (-176 + 8 * k)) * c)
        L = (14 + 3 * (2 - abs(k - 2))) * (0.85 + 0.4 * c)
        bx, by_ = hx - 2 + 3 * math.cos(a), hy - 5 + 3 * math.sin(a)
        ex, ey = bx + L * math.cos(a), by_ + L * math.sin(a)
        nx, ny = -math.sin(a) * 3.6, math.cos(a) * 3.6
        d = (f"M{f1(bx + nx)},{f1(by_ + ny)} Q{f1((bx + ex) / 2 + nx * 1.5)},{f1((by_ + ey) / 2 + ny * 1.5)} {f1(ex)},{f1(ey)} "
             f"Q{f1((bx + ex) / 2 - nx * 1.5)},{f1((by_ + ey) / 2 - ny * 1.5)} {f1(bx - nx)},{f1(by_ - ny)} Z")
        hd += f'<path d="{d}" fill="{body}" stroke="{INK}" stroke-width="2"/>'
        hd += f'<circle cx="{f1(bx + (L - 3) * math.cos(a))}" cy="{f1(by_ + (L - 3) * math.sin(a))}" r="2.2" fill="{blk}"/>'
    hd += (f'<path d="M{hx + 8},{hy - 1} Q{hx + 22},{hy + 1} {hx + 32},{hy + 9} Q{hx + 21},{hy + 4} {hx + 8},{hy + 3} Z" '
           f'fill="{blk}" {st}/>')
    if beak > 0.05:
        o = 6 * beak
        hd += (f'<path d="M{hx + 8},{hy + 3} Q{hx + 19},{f1(hy + 5 + o)} {hx + 27},{f1(hy + 12 + o)}" fill="none" '
               f'stroke="{blk}" stroke-width="3" stroke-linecap="round"/>')
    hd += f'<circle cx="{hx}" cy="{hy}" r="11.5" fill="{body}" {st}/>'
    hd += (f'<circle cx="{hx + 3.5}" cy="{hy - 2}" r="2.8" fill="#2e2630"/><circle cx="{hx + 4.4}" cy="{hy - 3}" r="1" '
           f'fill="#fffaf0"/><ellipse cx="{hx + 2}" cy="{hy + 5}" rx="3.4" ry="2" fill="#f0887a" opacity="0.75"/>')
    out += f'<g transform="rotate({look + (36 if pose == "preen" else 0):.1f} {hx - 5} {hy + 7})">{hd}</g>'
    if pose == "hop":
        wing = f"M-8,{by - 6} Q-6,{by - 34} 14,{by - 40} Q12,{by - 20} 8,{by - 4} Z"
        bars = "".join(f'<path d="M{-6 + 6 * j},{by - 8 - 8 * j} L{5 + 5 * j},{by - 15 - 8 * j}" stroke="{wht}" stroke-width="4"/>'
                       for j in range(3))
    else:
        wing = f"M-22,{by - 2} Q-4,{by - 14} 12,{by - 4} Q0,{by + 7} -22,{by + 6} Z"
        bars = "".join(f'<path d="M{-13 + 8 * j},{by - 10} L{-16 + 8 * j},{by + 8}" stroke="{wht}" stroke-width="3.6"/>'
                       for j in range(3))
    cid = f"zq1hpw_{key}_{pose}"
    out += (f'<clipPath id="{cid}"><path d="{wing}"/></clipPath><path d="{wing}" fill="{blk}"/>'
            f'<g clip-path="url(#{cid})">{bars}</g><path d="{wing}" fill="none" {st}/>')
    return out


def hoopoe(x, y, s=1.0, f=1, pose="perch", crest=0.0, beak=0.0, look=0.0):
    sx = s * (1 if f >= 0 else -1)
    return (f'<g transform="translate({f1(x)},{f1(y)}) scale({sx:.4f},{s:.4f})" filter="url(#wobble-fine)">'
            f'{_hoopoe(pose, crest, beak, look)}</g>')


def note_markup(x, y, k=1.0, col="#3f7d56"):
    """A little music note (the hoopoe's song)."""
    return S.g(f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(7 * k)}" ry="{f1(5.5 * k)}" fill="{col}" stroke="{INK}" '
               f'stroke-width="2" transform="rotate(-20 {f1(x)} {f1(y)})"/>'
               f'<path d="M{f1(x + 6 * k)},{f1(y - 1 * k)} L{f1(x + 6 * k)},{f1(y - 26 * k)} Q{f1(x + 14 * k)},{f1(y - 20 * k)} '
               f'{f1(x + 16 * k)},{f1(y - 12 * k)}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>',
               filter="wobble-fine")


def swift(x, y, k=1.0, wing=0, col="#6a6a7a"):
    """A little swift gliding high in the sky (wing 0 up, 1 down)."""
    u = -9 if wing == 0 else 4
    return (f'<path d="M{f1(x - 20 * k)},{f1(y + u * k)} Q{f1(x - 8 * k)},{f1(y - 4 * k)} {f1(x)},{f1(y)} '
            f'Q{f1(x + 8 * k)},{f1(y - 4 * k)} {f1(x + 20 * k)},{f1(y + u * k)}" fill="none" stroke="{col}" '
            f'stroke-width="{f1(3.2 * k)}" stroke-linecap="round" stroke-linejoin="round"/>')


class Confetti:
    """Paper confetti fluttering down through the frame (output space, deterministic in t): little rectangles that tumble
    (their width breathes as they spin) and sway as they fall. alpha_fn(t) scales them."""

    def __init__(self, n=46, cols=PR.FESTIVAL_COLS, speed=(60, 120), size=(9, 15), seed=3, alpha_fn=None, box=(0, 0, 1, 0.8)):
        rng = random.Random(seed)
        self.parts = [(rng.uniform(box[0], box[2]), rng.uniform(0, 1), rng.uniform(*speed), rng.uniform(*size),
                       rng.uniform(0, 6.28), rng.uniform(1.5, 3.2), rng.uniform(18, 46), S.hex_rgb(cols[i % len(cols)]))
                      for i in range(n)]
        self.box = box
        self.alpha_fn = alpha_fn or (lambda t: 1.0)

    def __call__(self, frame, t, view):
        a0 = self.alpha_fn(t)
        if a0 <= 0.01:
            return frame
        Wd, Hd = frame.size
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        span = (self.box[3] - self.box[1]) * Hd + 60
        for x, y0, v, sz, ph, spin, sway, col in self.parts:
            yy = self.box[1] * Hd - 30 + (y0 * span + v * t) % span
            xx = x * Wd + sway * math.sin(t * 0.9 + ph)
            ang = t * spin + ph
            w = sz * (0.25 + 0.75 * abs(math.cos(ang * 1.3)))
            h = sz * 0.62
            ca, sa = math.cos(ang), math.sin(ang)
            pts = [(xx + ca * dx - sa * dy, yy + sa * dx + ca * dy) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2),
                                                                                 (w / 2, h / 2), (-w / 2, h / 2))]
            fade = min(1.0, (yy - self.box[1] * Hd + 30) / 60, (self.box[3] * Hd + 30 - yy) / 80)
            if fade <= 0:
                continue
            d.polygon(pts, fill=(*col, int(235 * a0 * fade)))
        frame.alpha_composite(ov)
        return frame


# ================================================================== drawings

def sky_svg():
    return doc(PR.jericho_sky(-40, -40, W + 40, HZ + 40, time=TT, sun=None, clouds=0.0, scale=0.9, seed=3))


WISPS = [  # cx, cy, w, h, seed, drift px/s
    (300, 92, 380, 34, 11, 4.0),
    (1040, 58, 300, 28, 12, 5.0),
    (1460, 150, 420, 36, 13, 3.2),
    (-120, 236, 260, 26, 14, 5.6),
    (820, 560, 300, 24, 15, 3.8),
]


def wisp_svg(cx, cy, w, h, seed):
    pal = PR._jr_pal(TT)
    return doc(S.g(PR._jr_wisp(cx, cy, w, h, pal["cloud"], pal["cloud_sh"], seed), filter="wobble"))


ROAD_C = [(612, HZ - 14), (560, HZ + 26), (520, HZ + 76), (566, HZ + 130), (760, HZ + 192), (1036, HZ + 262),
          (1240, HZ + 340), (1372, HZ + 440), (1450, HZ + 560)]
ROAD_W = [14, 26, 44, 80, 150, 250, 380, 540, 700]


def road_markup():
    """The dusty packed-earth road winding from the town on the horizon and passing under the sitting branch: ruts,
    pebbles, dry tufts on the verges."""
    pal = PR._jr_pal(TT)
    n = len(ROAD_C)
    left, right = [], []
    for i, (x, y) in enumerate(ROAD_C):
        q0, q1 = ROAD_C[max(0, i - 1)], ROAD_C[min(n - 1, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = ROAD_W[i] / 2
        k = 0.35 + 0.65 * min(1.0, i / 4)
        left.append((x + nx * w, y + ny * w * k))
        right.append((x - nx * w, y - ny * w * k))
    d = S.smooth_path(left + list(reversed(right)), closed=True, tension=0.8)
    out = f'<path d="{d}" fill="{pal["sand_lt"]}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
    rng = random.Random(6)
    for side in (-0.26, 0.22):
        pts = [((l[0] + r[0]) / 2 + (l[0] - r[0]) * side, (l[1] + r[1]) / 2 + (l[1] - r[1]) * side) for l, r in zip(left, right)]
        out += (f'<path d="{S.smooth_path(pts[2:], closed=False)}" fill="none" stroke="{pal["sand_dk"]}" stroke-width="5" '
                f'opacity="0.45" stroke-linecap="round"/>')
    for i in range(46):
        u = rng.uniform(0.15, 1.0)
        j = min(n - 2, int(u * (n - 1)))
        fr = u * (n - 1) - j
        lx = left[j][0] + (left[j + 1][0] - left[j][0]) * fr
        ly = left[j][1] + (left[j + 1][1] - left[j][1]) * fr
        rx = right[j][0] + (right[j + 1][0] - right[j][0]) * fr
        ry = right[j][1] + (right[j + 1][1] - right[j][1]) * fr
        v = rng.uniform(0.08, 0.92)
        px, py = lx + (rx - lx) * v, ly + (ry - ly) * v
        if py > H + 20:
            continue
        r = (2 + 7 * u) * rng.uniform(0.7, 1.2)
        out += (f'<ellipse cx="{f1(px)}" cy="{f1(py)}" rx="{f1(r)}" ry="{f1(r * 0.62)}" fill="{pal["sand_dk"]}" '
                f'stroke="{INK}" stroke-width="{f1(0.8 + 0.9 * u)}" opacity="0.8"/>')
    for i in range(30):
        x = rng.uniform(-40, W + 40)
        y = rng.uniform(HZ + 40, H + 20)
        k = 0.5 + 0.9 * (y - HZ) / (H - HZ)
        out += PR._jr_tuft(x, y, k, TT, i)
    return S.g(out, filter="wobble")


def far_svg():
    """The far hills of the Jordan valley with the striped cliffs (left), the sand plain, the road, and Jericho on the
    horizon: little sandstone houses among date palms where the road begins."""
    out = PR._jr_far(-60, W + 60, HZ, 0.74, TT, seed=1, cliffs=True)
    pal = PR._jr_pal(TT)
    out += (f'<path d="M-60,{HZ - 24} L{W + 60},{HZ - 24} L{W + 60},{H + 60} L-60,{H + 60} Z" fill="{pal["sand"]}" '
            f'stroke="none"/>')
    out += road_markup()
    town = ""
    rng = random.Random(4)
    for i, (x, sc, ht) in enumerate(((236, 0.2, 0.8), (318, 0.25, 1.0), (430, 0.21, 0.9), (548, 0.26, 1.0), (700, 0.23, 0.95),
                                     (790, 0.19, 0.8), (902, 0.22, 0.9), (1000, 0.17, 0.75), (150, 0.17, 0.7))):
        town += PR._place(PR._jr_palm(ht, rng.uniform(-0.12, 0.12), 0.0, False, TT, 40 + i, far=True), x, HZ - 14, sc, 1,
                          filt=None)
    for i, (x, sc, v) in enumerate(((372, 0.19, 1), (472, 0.17, 0), (590, 0.2, 3), (660, 0.16, 2), (276, 0.15, 2),
                                    (744, 0.17, 1), (842, 0.14, 3))):
        town += PR.jericho_house(x, HZ - 10 + rng.uniform(-3, 3), sc, 1 if i % 2 else -1, variant=v, time=TT, awning=False,
                                 seed=i)
    out += S.g(town, filter="wobble-fine")
    out += f'<rect x="-60" y="{HZ - 64}" width="{W + 120}" height="50" fill="{pal["haze"]}" opacity="0.22"/>'
    return doc(out)


MID_PALMS = [  # x, y, scale, facing, height, lean, seed (two behind the tree on the right, three left of the road)
    (1930, 842, 0.46, -1, 1.0, -0.12, 51),
    (2080, 884, 0.54, 1, 0.95, 0.1, 52),
    (1046, 806, 0.29, 1, 0.9, 0.06, 53),
    (96, 950, 0.42, 1, 0.95, 0.14, 54),
    (250, 884, 0.3, -1, 0.85, -0.08, 55),
]
NPS = 5


def palms_svg(k):
    sway = 0.5 * (-1 + 2 * k / (NPS - 1))
    out = ""
    for i, (x, y, s, f, ht, ln, sd) in enumerate(MID_PALMS):
        out += C.ground_shadow(x + 10, y, s, 240, 0.16, color="#a07a4a")
        out += PR.date_palm(x, y, s, f, height=ht, lean=ln, sway=sway * (0.6 + 0.12 * i), time=TT, seed=sd)
    return doc(out)


NTS = 5


def tree_svg(part, k=1):
    tx, ty, ts, tf = TREE
    sway = (0.25 if part == "back" else 0.45) * (-1 + 2 * k / (NTS - 1))
    out = ""
    if part == "back":
        out += (f'<ellipse cx="{f1(tx - 60)}" cy="{f1(ty + 6)}" rx="{f1(420 * ts)}" ry="{f1(34 * ts)}" fill="#8a6a3a" '
                f'opacity="0.24" filter="url(#soft)"/>')
    out += PR.sycomore(tx, ty, ts, tf, part=part, sway=sway, time=TT, seed=2)
    return doc(out)


ZS = TREE[2]


def zac_body(pose, expr):
    sx, sy = tree_pts()["sit"]
    return C.zacchaeus(sx, sy, ZS, TREE[3], pose=pose, expr=expr)


def clump_root():
    """Where the twig of the hiding leaf clump grows out of the sitting branch (left of Zacchaeus)."""
    sx, sy = tree_pts()["sit"]
    return sx - 128 * ZS, sy + 4 * ZS


CLUMP_SWING = -78          # degrees: he pushes the clump up and aside (it stays held there by his hand)


def clump_svg():
    """A dense clump of big heart-shaped sycamore-fig leaves on one twig: at first it hides Zacchaeus (only his dangling
    feet show below it); he pushes it up and aside to peek out."""
    pal = PR._jr_pal(TT)
    fx, fy = clump_root()
    rng = random.Random(9)
    cols = (pal["leaf_lt"], pal["leaf"], pal["leaf_lt"], S.mix(pal["leaf"], pal["leaf_dk"], 0.4))
    out = ""
    cx, cy = fx + 100 * ZS, fy - 84 * ZS
    for i in range(26):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0.0, 0.85)
        lx, ly = cx + 74 * ZS * rr * math.cos(a), cy + 66 * ZS * rr * math.sin(a)
        out += PR._syco_leaf(lx, ly, rng.uniform(26, 33) * ZS, rng.uniform(-60, 60), cols[i % 4])
    for ang, ln, n, size in ((-82, 168, 6, 32), (-60, 186, 6, 34), (-38, 180, 6, 33), (-16, 150, 5, 31), (-70, 120, 4, 30),
                             (-28, 118, 4, 30), (-4, 150, 5, 31)):
        out += PR._leaf_spray(fx, fy, ang, ln * ZS, n, cols, rng, 0.0, size=size * ZS)
    return doc(S.g(out, filter="wobble-fine"))


def glow_light_svg():
    gx, gy = GLOW
    return glow_svg(gx, gy, 1350, 900, "zq1sun", "#fff3cf", "#ffdf9a", 0.62, 0.2)


def front_svg(k):
    """Dry desert tufts and a few stones framing the near corners (they stir in the breeze)."""
    pal = PR._jr_pal(TT)
    sway = -1 + 2 * k / 3
    rng = random.Random(21)
    out = ""
    for bx, by, bw, bh, col in ((-40, H + 6, 300, 110, pal["sand_dk"]), (W + 30, H + 14, 320, 120, pal["sand_dk"])):
        out += S.cloud(bx, by, bw, bh, fill=S.mix(col, pal["sand"], 0.35), seed=int(bx) + 3, puffs=4, sw=3.2,
                       shade_fill=S.shade(col, -0.12))
    for x0, x1 in ((-30, 420), (1720, W + 30)):
        for i in range(12):
            tx = rng.uniform(x0, x1)
            ty = H + 4 - rng.uniform(0, 60)
            hh = rng.uniform(26, 46)
            lean = 6 * sway * rng.uniform(0.6, 1.2)
            d = ""
            for j, dx in enumerate((-12, -4, 5, 13)):
                d += (f"M{f1(tx + dx)},{f1(ty)} q{f1(lean * 0.4 + (j - 1.5) * 3)},{f1(-hh * 0.6)} "
                      f"{f1(lean + (j - 1.5) * 6)},{f1(-hh * (0.8 + 0.1 * (j % 2)))} ")
            out += (f'<path d="{d}" stroke="{S.mix(pal["leaf"], pal["sand_dk"], 0.45)}" stroke-width="4" fill="none" '
                    f'stroke-linecap="round"/>')
    for sx_, sy_, r in ((180, 1150, 26), (232, 1166, 16), (1880, 1160, 24), (1934, 1172, 15)):
        out += (f'<ellipse cx="{sx_}" cy="{sy_}" rx="{r}" ry="{f1(r * 0.62)}" fill="{pal["stone"]}" stroke="{INK}" '
                f'stroke-width="3"/><ellipse cx="{sx_ - r * 0.3}" cy="{sy_ - r * 0.25}" rx="{r * 0.4}" ry="{r * 0.2}" '
                f'fill="#fff3d6" opacity="0.5"/>')
    return doc(S.g(out, filter="wobble-fine"))


SWIFTS = [  # start x, y, speed px/s, size, phase, flap period
    (-80, 250, 68, 1.0, 0.0, 0.42),
    (-200, 300, 74, 0.8, 0.4, 0.36),
    (1240, 112, -46, 0.75, 0.2, 0.5),
]
BIRD_S = 0.92
BIRD_X = (604, 560, 516)                 # the hoopoe's three perches along the sitting branch (local tree x)


# ================================================================== build


def title_times(ctx):
    marks = voice_marks(ctx, 0)
    t_rib = marks[0][1] - 0.12
    title_m = marks[-1] if len(marks) > 1 else marks[0]
    ch = char_times(title_m)
    if len(marks) == 1:                       # fallback: the title is the last 6 characters
        ch = ch[-6:]
    return t_rib, ch


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    t_rib, onsets = title_times(ctx)
    t_zac = onsets[0]                                     # '撒'
    t_sang = onsets[min(4, len(onsets) - 1)]               # '桑'
    t_shu = onsets[-1]                                     # '树'
    t_done = t_shu + 0.45
    t_peek = snap(1.15)                                    # he pushes the leaves aside and peeks out
    t_us = snap(t_zac - 0.04)                              # turns to us with a big smile

    # ---------------- sky, wisps, swifts
    sc.add("sky", sky_svg(), z=0, wc=0.55)
    for i, (cx, cy, cw, ch_, sd, v) in enumerate(WISPS):
        sc.add(f"wisp{i}", wisp_svg(cx, cy, cw, ch_, sd), z=0.3 + 0.01 * i, wc=0.5,
               motion=lambda t, v=v, i=i: Tf(dx=v * t, dy=1.5 * math.sin(2 * math.pi * (t / 8.0 + 0.3 * i))))
    for i, (x0, y0, v, k, ph, per) in enumerate(SWIFTS):
        frames = [doc(swift(x0, y0, k * 1.2, w)) for w in (0, 1)]

        def flap(t, ph=ph, per=per):
            u = t / per + ph
            return float(int(u * 2) % 2) if u % 4 < 1.6 else 0.0          # a few flaps, then a glide
        sc.add(f"swift{i}", frames, z=0.6 + 0.01 * i, wc=0, seed=70 + i, frame_at=flap,
               motion=lambda t, v=v, ph=ph: Tf(dx=v * t, dy=14 * math.sin(2 * math.pi * (t / 3.4 + ph))))

    # ---------------- the far hills, the town, the road, the palms
    sc.add("far", far_svg(), z=1, wc=0.75)
    sc.add("palms", [palms_svg(k) for k in range(NPS)], z=2, seed=31,
           frame_at=lambda t: (NPS - 1) * (0.5 + 0.5 * math.sin(2 * math.pi * t / 4.1)))

    # ---------------- the sycamore-fig, Zacchaeus, the leaf clump, the hoopoe
    sc.add("tree", [tree_svg("back", k) for k in range(NTS)], z=3, seed=33,
           frame_at=lambda t: (NTS - 1) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.6 + 0.1))))

    peek_blink = EX("peek_blink", "eager", eyes="closed")
    at_us = EX("at_us_joy", "overjoyed", look=(-0.05, 0.0))
    grin_us = EX("grin_us", "delighted", look=(-0.05, 0.01))
    grin_blink = EX("grin_blink", "happy", eyes="closed", blush=True)
    sx, sy = tree_pts()["sit"]
    zac = Fig(ctx, "zac", (sx, sy), z=3.5, seed=41)
    zac.at(0, zac_body("sit_branch", "eager"))
    zac.at(t_peek, zac_body("peek", "eager"))
    zac.at(snap(t_peek + 1.0), zac_body("peek", peek_blink)).at(snap(t_peek + 1.13), zac_body("peek", "eager"))
    zac.at(t_us, zac_body("peek", at_us))
    zac.at(snap(t_shu + 0.6), zac_body("peek", grin_us))
    tb = snap(max(t_shu + 1.5, T - 1.75))
    zac.at(tb, zac_body("peek", grin_blink)).at(snap(tb + 0.14), zac_body("peek", grin_us))
    giggle = keyed([(t_shu + 0.05, 0.0), (t_shu + 0.2, 1.0), (t_shu + 0.75, 1.0), (t_shu + 0.95, 0.0)], "sine")
    zac.move(hop(t_peek, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 6, "sy": 0.95}), (0.12, {"dy": -12, "sy": 1.03}),
                          (0.32, {"dy": 0, "sy": 1})], ["in", "out", "sine"]),
             dip(t_us, 5.0, 0.96),
             lambda t: Tf(rot=2.4 * math.sin(2 * math.pi * (t - t_shu) / 0.32) * giggle(t)),
             lambda t: Tf(rot=1.3 * math.sin(2 * math.pi * (t / 2.9 + 0.2)) * M.progress(t, t_peek + 0.4, t_peek + 1.2, "sine")),
             breath(ctx, 0.01, 3.1))
    zac.add(sc)

    rx_, ry_ = clump_root()

    def clump(t):
        q = keyed([(0.6, 0.0), (0.68, 1.0), (0.92, 1.0), (1.0, 0.0)], "sine")(t)
        swing = M.progress(t, t_peek - 0.06, t_peek + 0.34, "back")
        settle = 1.8 * math.sin(2 * math.pi * (t - t_peek) / 2.4) * M.progress(t, t_peek + 0.3, t_peek + 1.0, "sine")
        return Tf(rot=3.0 * math.sin(2 * math.pi * t / 0.12) * q + CLUMP_SWING * swing + settle, px=rx_, py=ry_)
    sc.add("clump", clump_svg(), z=3.6, seed=43, motion=clump)

    # the hoopoe hops along the sitting branch toward him and sings
    perch = [branch_top(lx) for lx in BIRD_X]
    bfig = Fig(ctx, "bird", perch[0], z=3.7, seed=45)
    t_h1 = snap(t_rib + 0.3)
    t_h2 = snap(t_sang - 0.06)
    t_sing = snap(t_sang + 0.42)

    def bird(pose, crest=0.0, beak=0.0, look=0.0):
        x, y = perch[0]
        return hoopoe(x, y, BIRD_S, 1, pose, crest, beak, look)
    bfig.at(0, bird("preen"))
    bfig.at(snap(0.5), bird("perch", look=-8)).at(snap(0.9), bird("preen")).at(snap(1.3), bird("perch", crest=0.4, look=6))
    for th in (t_h1, t_h2):
        bfig.at(snap(th - 0.12), bird("crouch", 0.3)).at(th, bird("hop", 0.6)).at(snap(th + 0.3), bird("crouch", 0.3))
        bfig.at(snap(th + 0.42), bird("perch", 0.2, look=10))
    bfig.at(t_sing, bird("perch", 1.0, 1.0, -14)).at(snap(t_sing + 0.2), bird("perch", 0.9, 0.2, -10))
    bfig.at(snap(t_sing + 0.4), bird("perch", 1.0, 1.0, -16)).at(snap(t_sing + 0.64), bird("perch", 0.5, look=4))
    bfig.at(snap(t_sing + 1.6), bird("preen", 0.2))
    if t_sing + 2.3 < T - 1.2:                              # no pose change during the dissolve into s02
        bfig.at(snap(t_sing + 2.3), bird("perch", 0.3, look=8))

    def bird_path(t):
        x, y = perch[0]
        dx = dy = 0.0
        for th, a, b in ((t_h1, perch[0], perch[1]), (t_h2, perch[1], perch[2])):
            if t >= th:
                u = M.progress(t, th, th + 0.3, "sine")
                dx = (a[0] - x) + (b[0] - a[0]) * u
                dy = (a[1] - y) + (b[1] - a[1]) * u - 30 * math.sin(math.pi * min(1.0, (t - th) / 0.3))
        return Tf(dx=dx, dy=dy)
    bfig.move(bird_path)
    bfig.add(sc, wc=0.4)
    nx, ny = perch[2][0] + 22, perch[2][1] - 86
    for j, (dt, ox) in enumerate(((0.0, 0), (0.4, -22))):
        t0 = t_sing + dt
        sc.add(f"note{j}", doc(note_markup(nx + ox, ny, 1.0, col="#d98852")), z=3.75, wc=0,
               motion=lambda t, t0=t0: Tf(alpha=M.progress(t, t0, t0 + 0.12) * (1 - M.progress(t, t0 + 0.7, t0 + 1.1)),
                                          dy=-40 * M.progress(t, t0, t0 + 1.1, "out"),
                                          dx=-8 * math.sin(2 * math.pi * (t - t0) / 0.9)))

    sc.add("tree_front", [tree_svg("front", k) for k in range(NTS)], z=4, seed=35,
           frame_at=lambda t: (NTS - 1) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.6 + 0.35))))

    # ---------------- warm light, foreground
    sc.add("sunwash", glow_light_svg(), z=4.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.8 + 0.12 * math.sin(2 * math.pi * t / 5.0)))
    sc.add("front", [front_svg(k) for k in range(4)], z=5, seed=37, wc=0.7,
           frame_at=lambda t: 3 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.3 + 0.2))))

    # ---------------- title lettering
    story = load_story()
    rx, ry = RIB

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=rx, py=ry)
    sc.add("ribbon", ribbon_svg(story.SUBTITLE, rx, ry, hw=RIB_HW, band_col=RIB_COL), z=10, motion=unfurl, wc=0)
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
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 52)
        sc.add(f"title_{i}", title_char_svg(ch, x, TITLE_Y, TITLE_SIZE, grad_id=f"zq1tg{i}", colors=TITLE_COLS),
               z=10.1 + i * 0.01, motion=pop, wc=0)

    # ---------------- camera: a slow push-in toward the tree
    sc.camera = safe_camera([(0, Cam(W / 2, H / 2, W * 0.985)), (T, CAM_END)], "sine")

    # ---------------- sparkle / light
    sc.fx.append(FX.sparkles((300, 270, 1080, 460), count=7, t0=t_done, color=(255, 238, 196), size=(9, 16),
                             period=2.0, drift=0, seed=9))
    sc.fx.append(FX.motes((100, 200, W - 100, 1000), count=16, color=(255, 246, 214), seed=13, alpha=80))
    sc.subtitles = False

    # ---------------- sound
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-24, fade_in=1.0, fade_out=1.3)
    sc.sfx("wind_soft", 0, dur=T + 0.3, gain_db=-29, fade_in=1.0, fade_out=1.3)
    sc.sfx("cloth", t_peek - 0.08, gain_db=-19, pan=0.45)
    sc.sfx("pop", t_peek + 0.06, gain_db=-22, pan=0.45)
    sc.sfx("chime", t_rib, gain_db=-10)
    for t in onsets:
        sc.sfx("pop", t - 0.04, gain_db=-21)
    sc.sfx("sparkle", t_done, gain_db=-17)
    return sc


CAM_END = Cam(W / 2 + 34, H / 2 + 8, W * 0.935)        # s02_question's first frame is composed against this view
