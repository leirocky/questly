"""Scene 2 - the opening question, at a picnic in a sunny city park: a sky-blue gingham blanket on the lawn, the skyline of
pale buildings beyond plane trees, a poplar and a pink cherry, the curving path with its bench, the pond with two ducks and
the little yellow climbing frame; a red kite dances on its string, soft clouds drift, swallows sail past, a yellow
butterfly visits the blanket. On the blanket: the little school girl (child outfit 'school') with her coral lunchbox and
her friend (outfit 'school_friend'), who has brought nothing.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity
film's Tm class; fallback: the subtitle chunks):
  start        calm, wide frame (1 s cross-dissolve from the title page: the park's skyline sits where the far hills and
               lake were, the lawn where the slope was, and the girl sits where the boy stood, her lunchbox where his
               basket was): the two children sit on the blanket; the kite sways, clouds drift
  '小朋友'      the girl looks round at us with a smile (a little bounce); the camera eases in
  '把'          she lifts the lid (open_lunchbox, 5 drawings) ...
  '好吃的'      ... and it is open: the sandwich, strawberries and carrot sticks (pop, sparkle); her friend leans to look
  '的'          he has nothing: no_lunch, empty hands in his lap, looking at her box
  '分给'        she takes one sandwich half out of the box and turns to him (look_at_friend, concerned); he looks down at his
               empty hands. The 0.8 s pause holds on her looking at her friend.
  '有一个小男孩' she looks down at the half in her hands and hesitates (hesitate); a small thought bubble rises from her
               (two dots, then the bubble, pop): a boy with his tiny basket on a green hillside by the lake
  '一点点'      in the bubble the boy lifts his little basket to show it (five small loaves, two small fish; sparkle)
  '可是'        the bubble shrinks away; her face brightens - she has decided (a little bounce)
  '耶稣'        she scoots in and holds the half out to her friend (share_half); he looks up, surprised ...
               ... scoots in, reaches out (receive_share) and takes it (the half passes from her hand into his, pop;
               the shared poses' hands do not meet at CHILD_SHARE_GAP, so both lean in for the hand-over); they sit back
               and she takes the other half out of her box for herself
  '好多'        they both eat (yum), munching
  '吃饱了'      they both beam (smile); little hearts float up between them (chime)
  end          calm warm frame for the page turn into s03 (breathing, blinks, the kite, the clouds)

Drawn on a 1.5x stage (3168 x 1782) so the close shots stay crisp: every drawing is made in the 2112 x 1188 design
coordinates of the title page and scaled up by K inside its layer; motions, pivots, fx and the camera use stage px (x K).

Shared with s09_end: park_body() (the park without its baked kite, lamp post and clouds, with an evening option), the
kite, clouds, daisies, girl() / friend() builders (lunchbox states and the sandwich in hand handled here, see girl()), the
seated wave (friend_wave), the thought-bubble pop.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.loaves.scenes.s01_title import CAM_END, EX, swallow
from stories.nativity.scenes.s01_title import Fig, breath, dip, hop, keyed
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import f1, heart_markup, snap
from stories.zacchaeus.scenes.s01_title import safe_camera

INK = P["ink"]

K = 1.5                             # stage up-scale for crisp close shots
SW, SH = 3168, 1782                 # the stage (2112 x 1188 design units x K)
PY, PS = 1040, 1.3                  # city_park: the blanket line, scale (design units)
PX0, PX1 = -200, 2312               # city_park x range
KS = 1.75                           # the children
BLK_Y = 1040                        # the blanket's near edge
SEAT = BLK_Y - 60 * KS              # the children's seats (anchors)
GX = 1090                           # the girl (facing right)
FX_ = GX + C.CHILD_SHARE_GAP * KS   # her friend (facing left)
BLK_X = (GX + FX_) / 2
BLK_W = 400
LEAN_DX, LEAN_ROT = 40, 7           # the lean-in for the hand-over (design px, degrees)
KITE = (1690, 440)                  # where our own kite flies (the baked one is removed)
KITE_HAND = (2170, 880)             # the string runs down to here (off behind the trees)


def doc2(body, defs=""):
    """A layer document on the K stage with the body drawn in design units."""
    return S.svg_doc(f'<g transform="scale({K})">{body}</g>', defs, SW, SH)


def raw2(body, defs=""):
    """A layer document on the K stage with the body already in stage px."""
    return S.svg_doc(body, defs, SW, SH)


def kp(x, y):
    """Design point -> stage point."""
    return x * K, y * K


def kcam(x, y, w):
    return Cam(x * K, y * K, w * K)


def kbody(markup):
    """Figure markup (design units) for a Fig layer on the K stage."""
    return f'<g transform="scale({K})">{markup}</g>'


# ================================================================== the park

def park_body(part="back", evening=False, seed=0):
    """city_park (design units) without its baked kite, lamp post and clouds (we animate our own kite and clouds);
    evening=True swaps the cyan sky and the lawn gradients for golden-evening colours."""
    s = PS
    kx = PX0 + (PX1 - PX0) * 0.78
    kite_m = f"M{PR._f(kx)},"
    o_p, o_rect, o_cl, o_lg = PR._p, PR._rect, PR._cluster, S.lin_grad

    def p_(d, fill="none", sw=4.0, stroke=INK, extra=""):
        if str(d).startswith(kite_m) or fill == "#fbf1c8":          # the kite, the lamp head
            return ""
        return o_p(d, fill, sw, stroke, extra)

    def rect_(x, y, w, h, fill, sw=4.0, rx=0, stroke=INK, extra=""):
        if fill == "#4a5a62":                                        # the lamp post
            return ""
        return o_rect(x, y, w, h, fill, sw, rx, stroke, extra)

    def cl_(circles, fill, sw=4.0):
        if fill == "#fbfbf6":                                        # the baked clouds
            return ""
        return o_cl(circles, fill, sw)

    def lg_(id_, stops, x1=0, y1=0, x2=0, y2=1):
        if evening and id_.startswith("pr-lfpark"):
            stops = [(0, "#86a2cc"), (0.4, "#d6c2b2"), (0.7, "#f6ce98"), (1, "#fde4b4")]
        elif evening and id_.startswith("pr-lflawn"):
            stops = [(0, "#a6cc70"), (1, "#68a252")]
        return o_lg(id_, stops, x1, y1, x2, y2)
    PR._p, PR._rect, PR._cluster, S.lin_grad = p_, rect_, cl_, lg_
    try:
        return PR.city_park(PX0, PX1, PY, s, part=part, seed=seed)
    finally:
        PR._p, PR._rect, PR._cluster, S.lin_grad = o_p, o_rect, o_cl, o_lg


def blanket_body(part):
    out = ""
    if part == "back":
        out += (f'<ellipse cx="{f1(BLK_X)}" cy="{f1(BLK_Y - 70 * KS)}" rx="{f1(BLK_W / 2 * KS + 40)}" ry="{f1(90 * KS)}" '
                f'fill="#3a7a3a" opacity="0.16" filter="url(#soft)"/>')
    return out + PR.picnic_blanket(BLK_X, BLK_Y, KS, 1, width=BLK_W, part=part)


def kite_body(tail=0, col="#e8503c"):
    """Our own kite on its string: a red diamond with a yellow cross and a bow-tied tail (tail 0..2 wiggles)."""
    kx, ky = KITE
    hx, hy = KITE_HAND
    out = (f'<path d="M{f1(kx)},{f1(ky + 52)} Q{f1(kx + (hx - kx) * 0.3 + 70)},{f1(ky + (hy - ky) * 0.25)} {f1(hx)},{f1(hy)}" '
           f'fill="none" stroke="{INK}" stroke-width="2" opacity="0.5"/>')
    pts = [(kx, ky + 52)]
    for j in range(1, 6):
        pts.append((kx - 10 * j + 9 * math.sin(j * 1.3 + tail * 2.1), ky + 52 + 24 * j))
    out += f'<path d="{S.smooth_path(pts, closed=False)}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    for j, (bx, by) in enumerate(pts[1:5]):
        c = ("#f6cf55", "#5aa0d8", "#f6cf55", "#5aa0d8")[j]
        out += (f'<path d="M{f1(bx - 9)},{f1(by - 6)} L{f1(bx + 9)},{f1(by + 6)} L{f1(bx + 9)},{f1(by - 6)} L{f1(bx - 9)},{f1(by + 6)} Z" '
                f'fill="{c}" stroke="{INK}" stroke-width="2"/>')
    out += (f'<path d="M{f1(kx)},{f1(ky - 46)} L{f1(kx + 34)},{f1(ky)} L{f1(kx)},{f1(ky + 52)} L{f1(kx - 34)},{f1(ky)} Z" '
            f'fill="{col}" stroke="{INK}" stroke-width="3"/>')
    out += (f'<path d="M{f1(kx)},{f1(ky - 46)} L{f1(kx)},{f1(ky + 52)} M{f1(kx - 34)},{f1(ky)} L{f1(kx + 34)},{f1(ky)}" '
            f'stroke="#f6cf55" stroke-width="3"/>')
    out += f'<ellipse cx="{f1(kx - 10)}" cy="{f1(ky - 16)}" rx="7" ry="11" fill="#fbe0d0" opacity="0.55"/>'
    return S.g(out, filter="wobble-fine")


def puff_cloud(cx, cy, k, fill="#fbfbf6", sw=2.6):
    """A puffy park cloud with an ink outline (the park's own cloud style)."""
    return PR._cluster([(cx - 60 * k, cy, 40 * k), (cx, cy - 22 * k, 54 * k), (cx + 62 * k, cy, 42 * k), (cx, cy + 10 * k, 46 * k)],
                       fill, sw * k)


PCLOUDS = [  # cx, cy, scale, drift px/s (design units)
    (380, 150, 1.25, 4.0),
    (1180, 96, 1.05, 5.2),
    (1700, 236, 0.9, 3.4),
    (60, 330, 0.75, 4.6),
]


def daisies_body(k, n=4, evening=False):
    """Swaying daisy clumps and grass tufts in the near corners (k = sway drawing 0..n-1)."""
    sway = -1 + 2 * k / (n - 1)
    rng = random.Random(31)
    g1, g2 = ("#3f8a42", "#5aa84a") if not evening else ("#4f8a3e", "#6a9e48")
    out = ""
    for cx, cy, kk in ((90, 1150, 1.5), (300, 1176, 1.2), (1840, 1168, 1.3), (2040, 1140, 1.6), (560, 1180, 1.0), (1620, 1186, 1.0)):
        for j in range(8):
            bx = cx + rng.uniform(-50, 50) * kk
            h_ = rng.uniform(34, 60) * kk
            lean = (rng.uniform(-6, 6) + 11 * sway) * kk
            out += (f'<path d="M{f1(bx - 4 * kk)},{f1(cy + 4)} Q{f1(bx + lean * 0.4)},{f1(cy - h_ * 0.6)} {f1(bx + lean)},{f1(cy - h_)} '
                    f'Q{f1(bx + lean * 0.3 + 3 * kk)},{f1(cy - h_ * 0.5)} {f1(bx + 4 * kk)},{f1(cy + 4)} Z" fill="{g1 if j % 2 else g2}" '
                    f'stroke="{INK}" stroke-width="{f1(1.6 * kk)}"/>')
        for j in range(4):
            fx = cx + rng.uniform(-44, 44) * kk
            fy = cy - rng.uniform(26, 52) * kk
            lx = fx + 9 * sway * kk
            out += (f'<path d="M{f1(fx)},{f1(cy + 4)} Q{f1(fx + 3 * sway * kk)},{f1((fy + cy) / 2)} {f1(lx)},{f1(fy)}" fill="none" '
                    f'stroke="{g2}" stroke-width="{f1(2.6 * kk)}"/>')
            for a in range(7):
                r = math.radians(360 * a / 7)
                px_, py_ = lx + 8 * kk * math.cos(r), fy + 8 * kk * math.sin(r)
                out += (f'<ellipse cx="{f1(px_)}" cy="{f1(py_)}" rx="{f1(5.6 * kk)}" ry="{f1(3.6 * kk)}" fill="#fbf6ea" stroke="{INK}" '
                        f'stroke-width="{f1(1.2 * kk)}" transform="rotate({f1(360 * a / 7)} {f1(px_)} {f1(py_)})"/>')
            out += f'<circle cx="{f1(lx)}" cy="{f1(fy)}" r="{f1(4.6 * kk)}" fill="#f6cf55" stroke="{INK}" stroke-width="{f1(1.2 * kk)}"/>'
    return S.g(out, filter="wobble-fine")


def add_park(sc, evening=False, sun=None, shadows=True):
    """The park set shared with s09: the park, our drifting clouds, the kite, two swallows, the blanket (back / front),
    the children's shadows, the near daisies, a yellow butterfly. Returns nothing; z: park 0..1, blanket 5 / 7, front 7.5+."""
    cloud_fill = "#fbfbf6" if not evening else "#fde8d0"
    sc.add("park", doc2(park_body("back", evening)), z=0, wc=0.7)
    if sun is not None:
        sx, sy, rr = sun
        sc.add("sun", doc2(f'<circle cx="{f1(sx)}" cy="{f1(sy)}" r="{f1(rr)}" fill="#ffd98a" stroke="#e8a250" stroke-width="3" '
                           f'opacity="0.95"/>'), z=0.05, wc=0.2)
    for i, (cx, cy, k, v) in enumerate(PCLOUDS):
        sc.add(f"pcloud{i}", doc2(S.g(puff_cloud(cx, cy, k, cloud_fill), filter="wobble")), z=0.2 + 0.01 * i, wc=0.4,
               motion=lambda t, v=v, i=i: Tf(dx=v * K * t, dy=1.5 * math.sin(2 * math.pi * (t / 7.0 + 0.3 * i))))
    kfr = [doc2(kite_body(k, "#e8503c")) for k in range(3)]
    khx, khy = kp(*KITE_HAND)
    sc.add("kite", kfr, z=0.5, seed=57, wc=0.3, frame_at=lambda t: float(int(t * 5) % 3),
           motion=lambda t: Tf(rot=2.4 * math.sin(2 * math.pi * t / 3.1) + 0.9 * math.sin(2 * math.pi * t / 1.3), px=khx, py=khy))
    for i, (x0, y0, off, v, k, ph, per) in enumerate(((600, 300, -700, 66, 0.8, 0.0, 0.34), (600, 350, -860, 72, 0.65, 0.4, 0.3))):
        frames = [doc2(swallow(x0, y0, k, w)) for w in (0, 1)]

        def flap(t, ph=ph, per=per):
            u = t / per + ph
            return float(int(u * 2) % 2) if u % 4 < 2.2 else 0.0
        sc.add(f"swallow{i}", frames, z=0.6 + 0.01 * i, wc=0, seed=60 + i, frame_at=flap,
               motion=lambda t, v=v, ph=ph, off=off: Tf(dx=(off + v * t) * K, dy=14 * math.sin(2 * math.pi * (t / 3.0 + ph))))
    sc.add("blanket_back", doc2(blanket_body("back")), z=5, wc=0.6)
    if shadows:
        sc.add("kid_shadows", doc2(kid_shadow(GX, evening=evening) + kid_shadow(FX_, evening=evening)), z=5.1, wc=0)
    sc.add("blanket_front", doc2(blanket_body("front")), z=7, wc=0.6)
    sc.add("park_front", doc2(park_body("front", evening)), z=7.5, wc=0.7)
    sc.add("daisies", [doc2(daisies_body(k, evening=evening)) for k in range(4)], z=7.6, seed=81,
           frame_at=lambda t: 3 * (0.5 + 0.5 * math.sin(2 * math.pi * (t / 3.2 + 0.1))))

    def bpos(t):
        return ((1700 + 190 * math.sin(2 * math.pi * t / 9.0 + 1.0) + 26 * math.sin(2 * math.pi * t / 1.6)) * K,
                (610 - 50 * math.sin(2 * math.pi * t / 6.5) + 14 * math.sin(2 * math.pi * t / 0.9)) * K)
    b0 = bpos(0.0)
    bfr = [raw2(PR.butterfly(b0[0], b0[1], 0.55 * K, flap=k / 4, color="yellow")) for k in range(4)]
    sc.add("butterfly", bfr, z=4.9, seed=83, wc=0.3, frame_at=lambda t: float(int(t * 14) % 4),
           motion=lambda t: Tf(dx=bpos(t)[0] - b0[0], dy=bpos(t)[1] - b0[1], rot=8 * math.sin(2 * math.pi * t / 1.1),
                               px=b0[0], py=b0[1]))


# ================================================================== the children

def _blank(*a, **kw):
    return ""


def girl(pose, expr=None, phase=0.0, box=None, hand=True):
    """The school girl on the blanket (design units; anchor = her seat, facing right). box overrides the lunchbox state the
    pose would draw: 'closed' | 'open' | 'half' | 'fruit' (both sandwich halves gone, the strawberries and carrots left) -
    the shared child() draws 'open' (two halves in the box) while she already holds one half in look_at_friend /
    hesitate, and 'half' while she eats her own half; hand=False hides the sandwich half in her hand (after she has
    handed it over)."""
    o_lb, o_sh = PR._lunchbox, PR._sandwich_half

    def lb(state="closed", lid=None, k=1.0):
        st = box or state
        saved = PR._sandwich_half
        PR._sandwich_half = _blank if st == "fruit" else o_sh
        try:
            return o_lb("half" if st == "fruit" else st, lid, k)
        finally:
            PR._sandwich_half = saved
    PR._lunchbox = lb
    if not hand:
        PR._sandwich_half = _blank
    try:
        return C.child(GX, SEAT, KS, 1, pose=pose, expr=expr, outfit="school", phase=phase)
    finally:
        PR._lunchbox, PR._sandwich_half = o_lb, o_sh


def friend(pose, expr=None, phase=0.0, hand=True):
    """Her friend on the blanket (design units; anchor = his seat, facing left); hand=False hides the half he would hold
    (reaching for it before he has it). pose 'wave_sit': a seated wave (phase swings the hand)."""
    if pose == "wave_sit":
        return friend_wave(phase, expr or "happy")
    o_sh = PR._sandwich_half
    if not hand:
        PR._sandwich_half = _blank
    try:
        return C.child(FX_, SEAT, KS, -1, pose=pose, expr=expr, outfit="school_friend", phase=phase)
    finally:
        PR._sandwich_half = o_sh


def friend_wave(phase, expr):
    """The friend sitting on the blanket and waving to us with his far hand, his half-eaten sandwich in the near hand on his
    knee: a seated pose built with the shared rig (the standing 'wave' would stand him up)."""
    f = 150 + 22 * math.sin(2 * math.pi * phase)
    ps = C._P(t=-4, h=-6, arms=(("fk", 140, f), ("ik", "knee", 0, 0.25, 1)), hands=("open", "fist"), expr=expr,
              look=(-0.05, 0.0), **C._LFC_SEAT)
    D, m = C._school_design("school_friend")
    D["front"] = C._hooks(D.get("front"), C._lfc_items(D, "school_friend", "eat", 0.0, None))
    inner, _ = C._figure(D, m, ps, expr, C._fsign(-1), True)
    return C._wrap_out(inner, FX_, SEAT, KS, -1, f"lf2-friend-wave-{phase:.2f}")


def kid_shadow(x, s=KS, evening=False):
    if evening:                       # the low evening sun on the left: a long soft shadow to the right
        return (f'<ellipse cx="{f1(x + 120 * s)}" cy="{f1(SEAT + 8)}" rx="{f1(150 * s)}" ry="{f1(20 * s)}" fill="#5a4a3a" '
                f'opacity="0.2" filter="url(#soft)"/>')
    return C.ground_shadow(x + 10, SEAT + 6, s, 150, 0.18, color="#3a6a3a")


# ================================================================== the thought bubble

BUB = (820, 480, 150)                # the thought bubble: centre, radius (design units)
BUB_DOTS = [(1032, 648, 10), (984, 620, 15)]   # from the girl's head up to the bubble


def bubble_body(boy_pose="stand_basket", boy_expr="happy"):
    """A round thought bubble: a little green hillside by the lake under an afternoon sky, a boy holding his tiny basket."""
    cx, cy, rr = BUB
    r = 168                                          # the vignette is laid out at this radius and scaled to rr
    cid, gid = "lf2bub", "lf2bsky"
    pl = PR._lf_pal(0.25)
    defs = (S.lin_grad(gid, [(0, pl["sky"][0]), (0.55, pl["sky"][1]), (1, pl["sky"][3])]) +
            f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}"/></clipPath>')
    gy = cy + r * 0.66
    inner = f'<rect x="{f1(cx - r)}" y="{f1(cy - r)}" width="{f1(2 * r)}" height="{f1(2 * r)}" fill="url(#{gid})"/>'
    inner += PR._lf_cloud(cx - 64, cy - 100, 130, 38, pl, 3, 0.5)
    inner += PR._p(S.hill(cx - r - 20, cx + r + 20, cy - 2, 34, seed=3, bottom=cy + 40), pl["far"][1], 2.4)
    inner += f'<rect x="{f1(cx - r)}" y="{f1(cy + 2)}" width="{f1(2 * r)}" height="60" fill="{pl["lake"][1]}"/>'
    inner += PR._p(S.hill(cx - r - 20, cx + r + 20, gy - 40, 40, seed=5, bottom=cy + r + 20), pl["grass"][0], 3)
    inner += PR._p(S.hill(cx - r - 20, cx + r + 20, gy + 14, 16, seed=8, bottom=cy + r + 20), pl["grass"][1], 3)
    for j, (fx, fy) in enumerate(((cx - 104, gy + 4), (cx + 98, gy + 12), (cx - 66, gy + 40), (cx + 56, gy + 44))):
        inner += PR.galilee_flower(fx, fy, 0.75, ("anemone", "daisy")[j % 2], time=0.25)
    bxo = cx - 18
    inner += C.ground_shadow(bxo + 4, gy + 26, 0.74, 120, 0.2, color="#1f5a3a")
    inner += C.the_boy(bxo, gy + 26, 0.74, 1, pose=boy_pose, expr=boy_expr, basket="open")
    b = (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 14)}" fill="#fbf6ea" stroke="{INK}" stroke-width="4"/>'
         f'<g clip-path="url(#{cid})">{inner}</g>'
         f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="none" stroke="{INK}" stroke-width="3"/>')
    q = rr / r
    return (f'<g transform="translate({f1(cx)},{f1(cy)}) scale({q:.4f}) translate({f1(-cx)},{f1(-cy)})">'
            f'<g filter="url(#wobble-fine)">{b}</g></g>'), defs


def dot_body(x, y, r):
    return (f'<g filter="url(#wobble-fine)"><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fbf6ea" stroke="{INK}" '
            f'stroke-width="3.2"/></g>')


def pop_in(t0, t1, piv, dur=0.35):
    """Scale pop at t0 (back ease) about the stage point piv, shrink away over 0.3 s ending at t1."""
    def m(t):
        if t < t0 or t > t1:
            return Tf(alpha=0.0, sx=0.001, sy=0.001, px=piv[0], py=piv[1])
        k = M.ease("back")(min(1.0, (t - t0) / dur)) * (1 - M.progress(t, t1 - 0.3, t1, "in"))
        a = min(1.0, (t - t0) / 0.1) * (1 - M.progress(t, t1 - 0.2, t1, "sine"))
        return Tf(sx=max(0.001, k), sy=max(0.001, k), alpha=a, px=piv[0], py=piv[1])
    return m


def heart_float2(sc, name, x0, y0, r, t0, dx=0.0, rise_px=200, life=2.4, z=9.5, fill="#ef8a8a"):
    """A little heart (design point x0, y0, radius r) that pops in at t0 and floats up, fading."""
    X, Y = kp(x0, y0)

    def m(t):
        if t < t0 or t > t0 + life:
            return Tf(alpha=0.0)
        u = (t - t0) / life
        s_ = max(0.001, M.ease("back")(min(1.0, (t - t0) / 0.35)))
        a = min(1.0, (t - t0) / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine"))
        return Tf(dx=(dx * u + 8 * math.sin(2 * math.pi * (t - t0) / 1.3)) * K, dy=-rise_px * K * M.ease("out")(u),
                  sx=s_, sy=s_, alpha=a, px=X, py=Y)
    sc.add(name, raw2(heart_markup(X, Y, r * K, fill=fill)), z=z, wc=0, motion=m)


def ksparkles(rect, **kw):
    x0, y0, x1, y1 = rect
    if "size" in kw:
        kw["size"] = (kw["size"][0] * K, kw["size"][1] * K)
    return FX.sparkles((x0 * K, y0 * K, x1 * K, y1 * K), **kw)


# ================================================================== build

def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    tm = Tm(ctx)

    t_kid = tm.at(0, "小朋友")
    t_ba = tm.at(0, "把")
    t_de = tm.at(0, "的")
    t_fen = tm.at(0, "分给")
    t_l0 = L[0].end
    t_boy = tm.at(1, "有一个小男孩")
    t_dian = tm.at(1, "一点点饭")
    t_but = tm.at(1, "可是")
    t_jesus = tm.at(1, "耶稣")
    t_many = tm.at(1, "好多好多")
    t_full = tm.at(1, "吃饱了")

    # ---------------------------------------------------------------- expressions
    g_front = EX("q_g_front", "happy", look=(0.0, 0.02))
    g_us = EX("q_g_us", "delighted", look=(-0.08, 0.0))
    g_us_blink = EX("q_g_us_blink", "happy", eyes="closed", blush=True)
    g_box = EX("q_g_box", "happy", look=(0.0, 0.0))
    g_decide = EX("q_g_decide", "delighted", look=(0.04, -0.02))
    g_friend = EX("q_g_friend", "happy", look=(0.02, 0.0))
    g_smile_blink = EX("q_g_smile_blink", "smile")
    f_happy = EX("q_f_happy", "happy", look=(0.03, 0.0))
    f_blink = EX("q_f_blink", "happy", eyes="closed")
    f_box = EX("q_f_box", "awed", look=(0.05, 0.08))
    f_wish = EX("q_f_wish", "sad", look=(0.05, -0.02))
    f_surp = EX("q_f_surp", "surprised", look=(0.04, -0.03))

    # ---------------------------------------------------------------- the girl
    c_us = snap(t_kid + 0.02)
    c_open = snap(t_ba - 0.12)
    open_cuts = [snap(c_open + 0.1 * i) for i in range(5)]
    c_take = snap(t_fen - 0.06)
    c_hes = snap(t_boy - 0.04)
    c_decide = snap(t_but + 0.04)
    c_share = snap(t_jesus + 0.02)
    c_give = snap(c_share + 1.15)
    c_own = snap(c_give + 0.5)
    c_eat = snap(max(t_many + 0.02, c_own + 0.5))
    c_smile = snap(t_full + 0.04)

    gfoot = kp(GX, SEAT)
    gfig = Fig(ctx, "girl", gfoot, z=6.5, seed=71)

    def G(*a, **kw):
        return kbody(girl(*a, **kw))
    gfig.at(0, G("sit_picnic", g_front))
    gfig.at(c_us, G("sit_picnic", g_us))
    tb = snap(c_us + 0.75)
    if tb + 0.3 < c_open:
        gfig.at(tb, G("sit_picnic", g_us_blink)).at(snap(tb + 0.13), G("sit_picnic", g_us))
    for i, tc in enumerate(open_cuts):
        gfig.at(tc, G("open_lunchbox", g_box, phase=i / 4))
    gfig.at(c_take, G("look_at_friend", box="half"))
    gfig.at(c_hes, G("hesitate", box="half"))
    gfig.at(c_decide, G("hesitate", g_decide, box="half"))
    gfig.at(c_share, G("share_half"))
    gfig.at(c_give, G("share_half", hand=False))
    gfig.at(c_own, G("look_at_friend", g_friend, box="fruit"))
    gfig.at(c_eat, G("eat", box="fruit"))
    gfig.at(c_smile, G("smile", box="fruit"))
    for tb in (snap(c_smile + 1.0), snap(c_smile + 2.2)):
        if tb + 0.3 < T - 0.2:
            gfig.at(tb, G("smile", g_smile_blink, box="fruit")).at(snap(tb + 0.14), G("smile", box="fruit"))
    munch = keyed([(c_eat + 0.15, 0.0), (c_eat + 0.3, 1.0), (c_smile - 0.25, 1.0), (c_smile - 0.05, 0.0)], "sine")
    # the shared poses leave a gap between the hands at this distance: she scoots and leans in to hold the half out,
    # he scoots and leans in to take it (the half passes from her hand into his at c_give), then both sit back
    g_lean = keyed([(c_share - 0.06, 0.0), (c_share + 0.3, 1.0), (c_own - 0.06, 1.0), (c_own + 0.3, 0.0)], "sine")
    gfig.move(dip(c_us, 4), dip(open_cuts[0], 3), dip(c_take, 4), dip(c_hes, 4), dip(c_decide, 3), dip(c_share, 4),
              dip(c_give, 2), dip(c_own, 3), dip(c_eat, 4), dip(c_smile, 4),
              hop(c_us + 0.02, [(0, {"dy": 0}), (0.12, {"dy": -9}), (0.28, {"dy": 0})], ["out", "in"]),
              hop(c_decide + 0.04, [(0, {"dy": 0}), (0.12, {"dy": -8}), (0.28, {"dy": 0})], ["out", "in"]),
              hop(c_smile + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * (t - c_eat) / 0.42) * munch(t)),
              lambda t: Tf(dx=LEAN_DX * K * g_lean(t), rot=LEAN_ROT * g_lean(t)),
              breath(ctx, 0.011, 2.7))
    gfig.add(sc)

    # ---------------------------------------------------------------- the friend
    d_box = snap(open_cuts[2] + 0.05)
    d_none = snap(t_de + 0.12)
    d_down = snap(c_take + 0.5)
    d_surp = snap(c_share + 0.12)
    d_reach = snap(c_share + 0.62)
    d_eat = snap(c_eat + 0.12)
    d_smile = snap(c_smile + 0.1)

    ffig = Fig(ctx, "friend", kp(FX_, SEAT), z=6.4, seed=73)

    def F(*a, **kw):
        return kbody(friend(*a, **kw))
    ffig.at(0, F("sit_picnic", f_happy))
    tfb = snap(1.6)
    ffig.at(tfb, F("sit_picnic", f_blink)).at(snap(tfb + 0.13), F("sit_picnic", f_happy))
    ffig.at(d_box, F("sit_picnic", f_box))
    ffig.at(d_none, F("no_lunch", f_wish))
    ffig.at(d_down, F("no_lunch"))
    ffig.at(d_surp, F("no_lunch", f_surp))
    ffig.at(d_reach, F("receive_share", hand=False))
    ffig.at(c_give, F("receive_share"))
    ffig.at(d_eat, F("eat"))
    ffig.at(d_smile, F("smile"))
    tb = snap(d_smile + 1.6)
    if tb + 0.3 < T - 0.2:
        ffig.at(tb, F("smile", f_blink)).at(snap(tb + 0.14), F("smile"))
    fmunch = keyed([(d_eat + 0.15, 0.0), (d_eat + 0.3, 1.0), (d_smile - 0.25, 1.0), (d_smile - 0.05, 0.0)], "sine")
    f_lean = keyed([(d_reach - 0.06, 0.0), (d_reach + 0.3, 1.0), (c_give + 0.25, 1.0), (c_give + 0.6, 0.0)], "sine")
    ffig.move(dip(d_box, 3), dip(d_none, 4), dip(d_down, 3), dip(d_surp, 3), dip(d_reach, 3), dip(c_give, 2), dip(d_eat, 4),
              dip(d_smile, 4),
              hop(d_surp + 0.02, [(0, {"dy": 0}), (0.1, {"dy": -7}), (0.24, {"dy": 0})], ["out", "in"]),
              hop(d_smile + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * (t - d_eat) / 0.46) * fmunch(t)),
              lambda t: Tf(dx=-LEAN_DX * K * f_lean(t), rot=-LEAN_ROT * f_lean(t)),
              breath(ctx, 0.011, 3.0, 0.4))
    ffig.add(sc)
    sc.add("girl_shadow", doc2(kid_shadow(GX)), z=5.1, wc=0, motion=lambda t: Tf(dx=LEAN_DX * K * g_lean(t)))
    sc.add("friend_shadow", doc2(kid_shadow(FX_)), z=5.1, wc=0, motion=lambda t: Tf(dx=-LEAN_DX * K * f_lean(t)))

    # ---------------------------------------------------------------- the park, the blanket, the light
    add_park(sc, shadows=False)
    sc.add("sunwash", raw2(f'<ellipse cx="{300 * K}" cy="{80 * K}" rx="{1300 * K}" ry="{800 * K}" fill="url(#lf2sun)"/>',
                           S.rad_grad("lf2sun", [(0, "#fffbe6", 0.45), (0.45, "#fff2c4", 0.15), (1, "#fff2c4", 0)])),
           z=8, wc=0, blend="screen")

    # ---------------------------------------------------------------- the thought bubble
    bx, by, br = BUB
    t_b0 = snap(c_hes + 0.12)
    t_b1 = snap(c_decide + 0.3)
    for i, (x, y, r) in enumerate(BUB_DOTS):
        sc.add(f"bub_dot{i}", doc2(dot_body(x, y, r)), z=9.0, wc=0,
               motion=pop_in(t_b0 + 0.12 * i, t_b1 - 0.1 * (1 - i), kp(x, y), 0.25))
    c_bshow = snap(t_dian - 0.04)
    bfrm = [doc2(*bubble_body("stand_basket", EX("q_b_boy", "happy", look=(-0.05, 0.0)))),
            doc2(*bubble_body("offer_up", EX("q_b_boy_show", "delighted", look=(-0.04, 0.02))))]
    sc.add("bubble", bfrm, z=9.1, wc=0, seed=85, frame_at=lambda t: 1.0 if t >= c_bshow else 0.0,
           motion=M.combine(pop_in(t_b0 + 0.3, t_b1, kp(bx + 70, by + br), 0.4),
                            lambda t: Tf(dy=4 * math.sin(2 * math.pi * t / 2.6)),
                            hop(c_bshow, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 3, "sy": 0.97}), (0.14, {"dy": -7, "sy": 1.02}),
                                          (0.3, {"dy": 0, "sy": 1})], ["in", "out", "sine"])))

    # ---------------------------------------------------------------- hearts and sparkles
    lbx, lby = GX + C.CHILD_LUNCHBOX[0] * KS, SEAT + C.CHILD_LUNCHBOX[1] * KS
    sc.fx.append(ksparkles((lbx - 70, lby - 110, lbx + 70, lby - 30), count=6, t0=open_cuts[-1], t1=open_cuts[-1] + 1.3,
                           color=(255, 244, 200), size=(8, 14), period=1.0, drift=-12, seed=21))
    sc.fx.append(ksparkles((bx - 5, by - 10, bx + 70, by + 60), count=5, t0=c_bshow + 0.05, t1=t_b1 - 0.3,
                           color=(255, 240, 196), size=(6, 11), period=1.0, drift=-8, seed=23))
    hx, hy = BLK_X, SEAT - 300
    heart_float2(sc, "heart0", hx - 20, hy, 26, snap(c_smile + 0.12), dx=-16, rise_px=170)
    heart_float2(sc, "heart1", hx + 50, hy + 30, 20, snap(c_smile + 0.42), dx=18, rise_px=150)
    heart_float2(sc, "heart2", hx - 70, hy + 40, 16, snap(c_smile + 0.75), dx=-10, rise_px=130)

    # ---------------------------------------------------------------- camera (design units, x K)
    c0 = kcam(CAM_END.x, CAM_END.y, CAM_END.w)         # the title page's last view (the dissolve)
    cm = kcam(1210, 730, 1450)                         # easing in while she opens her lunchbox
    c1 = kcam(BLK_X, 780, 1130)                        # the two children on the blanket
    c2 = kcam(1110, 684, 1400)                         # the girl and her thought bubble
    c3 = kcam(BLK_X, 800, 990)                         # the share
    c4 = kcam(BLK_X, 794, 1040)
    sc.camera = safe_camera([(0, c0), (0.9, c0), (c_open - 0.1, cm), (t_l0 - 0.2, c1), (t_l0 + 0.4, c1), (t_b0 + 0.6, c2),
                            (c_decide, c2), (c_share + 0.6, c3), (c_smile + 0.4, c3), (T, c4)], "sine", SW, SH)

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T, gain_db=-27, fade_in=0.9, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T, gain_db=-31, fade_in=0.9, fade_out=1.0)
    sc.sfx("cloth", open_cuts[0] - 0.04, gain_db=-22, pan=-0.1)
    sc.sfx("pop", open_cuts[-1], gain_db=-20, pan=-0.1)
    sc.sfx("sparkle", open_cuts[-1] + 0.05, gain_db=-19, pan=-0.1)
    sc.sfx("pop", t_b0 + 0.3, gain_db=-21, pan=-0.3)
    sc.sfx("sparkle", c_bshow + 0.05, gain_db=-20, pan=-0.3)
    sc.sfx("pop", t_b1 - 0.3, gain_db=-24, pan=-0.3)
    sc.sfx("cloth", c_share - 0.04, gain_db=-22)
    sc.sfx("pop", c_give, gain_db=-23, pan=0.15)
    sc.sfx("crunch", c_eat + 0.2, gain_db=-24)
    sc.sfx("chime", c_smile + 0.1, gain_db=-14)
    return sc
