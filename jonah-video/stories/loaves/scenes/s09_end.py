"""Scene 9 - the closing page: the park of the opening (s02) in golden evening light - a honey sky over the pale skyline,
long soft shadows from the low sun on the left, peach clouds drifting, the kite still dancing - and the school girl and
her friend on the blue gingham blanket, eating the lunch they shared. A round picture-book corner opens above the girl
(a cream-framed vignette on the golden hillside by the lake) to show the story again. God is never drawn: love is warm
light.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity
film's Tm class; fallback: the subtitle chunks):
  start        calm frame (page dip from s08): both children munch their sandwich halves; the kite, clouds, butterfly
  '小朋友'      the girl looks round at us with a smile
  '五个饼'      the round picture-book corner pops open above her; five round barley loaves pop onto a little cloth, one
               per beat of '五个饼', and the two fish on '两条鱼' (soft pops); both children look up at the picture
  '只有一点点'  the girl tilts her head, pondering: only a little
  '在耶稣手里'  a warm light shines down into the picture from above (light only) and the loaves glow a little
  '变成好多好多' the loaves and fish melt away and the picture fills with twelve full baskets, popping in row by row
               (5 + 4 + 3, count them), sparkle on '多'; the children beam
  '耶稣看见'    the picture turns over like a card: Jesus handing a piece of bread to a mother with her baby, a child
               beside her and families eating on the grass behind them
  '就疼爱'      she takes the bread from his hand (the piece passes from his hand into hers); a little heart floats up in
               the picture on '爱'; on '照顾他们' Jesus smiles
  '耶稣也知道'  the picture shrinks away; the camera comes in to the two children, a warm light rises round them; she
               smiles at her friend and he smiles back
  '他也会照顾你' they both beam; a heart floats up over them on '照顾你' (chime)
  '小朋友'      both look at us
  '你有什么'    she thinks, eyes up, her sandwich in both hands ...
  after it     ... and smiles at us through the full 2 s answer pause; her friend waves to us; 2.0 s after the question the
               end card '五饼二鱼 · 完' fades in over the sky (0.5 s) with a little heart (chime), fully visible ~1.6 s
               before the film's 1.6 s fade-out; calm, alive final frame (breathing, blinks, the kite, the drifting
               clouds, motes)

Drawn on the same 1.5x stage as s02 (design coordinates of the title page, scaled by K inside each layer).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Tf
from engine.scene import Scene
from stories.loaves.scenes.s01_title import EX
from stories.loaves.scenes.s02_question import (BLK_X, FX_, GX, K, SEAT, SH, SW, add_park, doc2, friend, girl, heart_float2,
                                                kbody, kcam, kp, ksparkles, raw2)
from stories.nativity.scenes.s01_title import Fig, breath, dip, hop, keyed
from stories.nativity.scenes.s07_shepherds import Tm
from stories.noah.scenes.s01_title import f1, heart_markup, snap
from stories.zacchaeus.scenes.s01_title import safe_camera

INK = P["ink"]

INS = (782, 556, 205)               # the picture-book corner: centre, radius (design units)
END = (BLK_X, 468)                  # the end card (design units): over the sky, above the children
LT = 0.5                            # the hillside's time of day inside the picture (the golden hour)


# ================================================================== the picture-book corner

def _clip(body, key):
    cx, cy, r = INS
    cid = f"lf9clip{key}"
    return f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}"/></clipPath><g clip-path="url(#{cid})">{body}</g>'


def inset_bg_body():
    """The vignette's background: the golden hillside above the lake (the story's own world), in a cream frame."""
    cx, cy, r = INS
    sky = PR.galilee_sky(cx - r - 20, cy - r - 20, cx + r + 20, cy + r * 0.5, time=LT, sun=(cx + r * 0.52, cy - r * 0.22),
                         clouds=0.7, scale=0.4, seed=5)
    hill = PR.lake_hillside(cx - r - 70, cx + r + 70, cy + r * 0.80, 0.4, time=LT, part="all", seed=6, rock=False,
                            boat=cx - r * 0.45, flowers=0.7)
    body = (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 18)}" fill="#fbf3e2" stroke="{INK}" stroke-width="4.5"/>'
            + _clip(sky + hill, "bg") +
            f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 7)}" fill="none" stroke="#e8b866" stroke-width="3" opacity="0.9"/>'
            f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="none" stroke="{INK}" stroke-width="3.2"/>')
    for a in (-128, -52):                                      # two little leaf sprigs on the frame (a book-corner touch)
        x = cx + (r + 12) * math.cos(math.radians(a))
        y = cy + (r + 12) * math.sin(math.radians(a))
        for j, d in enumerate((-30, 0, 30)):
            ang = a + 90 + d
            lx, ly = x + 16 * math.cos(math.radians(ang)), y + 16 * math.sin(math.radians(ang))
            body += (f'<ellipse cx="{f1(lx)}" cy="{f1(ly)}" rx="12" ry="6" fill="{("#7cb85a", "#5a9e4a")[j % 2]}" stroke="{INK}" '
                     f'stroke-width="2.2" transform="rotate({f1(ang)} {f1(lx)} {f1(ly)})"/>')
        body += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="6" fill="{PR.ANEMONE}" stroke="{INK}" stroke-width="2"/>'
    return S.g(body, filter="wobble-fine")


def cloth_body():
    cx, cy, r = INS
    x, y = cx, cy + 128
    out = (f'<ellipse cx="{f1(x + 6)}" cy="{f1(y + 10)}" rx="160" ry="44" fill="#2a5a30" opacity="0.18" filter="url(#soft)"/>'
           f'<path d="{S.blob(x, y, 156, 50, 0.06, 10, seed=3)}" fill="{PR.LF_CLOTH}" stroke="{INK}" stroke-width="3"/>')
    for dy in (-22, 18):
        out += (f'<path d="M{f1(x - 140)},{f1(y + dy)} Q{f1(x)},{f1(y + dy + 6)} {f1(x + 140)},{f1(y + dy)}" fill="none" '
                f'stroke="{PR.LF_CLOTH_STRIPE}" stroke-width="5" opacity="0.8"/>')
    return _clip(S.g(out, filter="wobble-fine"), "cloth")


def _loaf_spots():
    cx, cy, r = INS
    loaves = [(cx - 74, cy + 104), (cx, cy + 98), (cx + 74, cy + 104), (cx - 38, cy + 132), (cx + 40, cy + 134)]
    fish = [(cx - 48, cy + 166, 1), (cx + 52, cy + 164, -1)]
    return loaves, fish


def loaf_body(i):
    (x, y) = _loaf_spots()[0][i]
    return _clip(PR.barley_loaf(x, y, 1.4, 1 if i % 2 else -1, "whole", rot=(-6, 4, 8, -4, 5)[i], time=LT, seed=i), f"loaf{i}")


def fish_body(i):
    (x, y, f) = _loaf_spots()[1][i]
    return _clip(PR.dried_fish(x, y, 1.35, f, "whole", rot=(-5, 6)[i], time=LT), f"fish{i}")


def _basket_spots():
    """Twelve full baskets as a little pyramid: 5 at the back, 4 in the middle, 3 in front (anchor = bottom centre, scale)."""
    cx, cy, r = INS
    out = []
    for n, y, s, gap in ((5, cy + 30, 0.42, 80), (4, cy + 92, 0.46, 86), (3, cy + 156, 0.5, 86)):
        for j in range(n):
            out.append((cx + (j - (n - 1) / 2) * gap, y, s))
    return out


def basket_body(i):
    x, y, s = _basket_spots()[i]
    return _clip(C.ground_shadow(x + 4, y + 2, s, 160, 0.18, color="#2a5a30") +
                 PR.wicker_basket(x, y, s, 1, fill=1.0, food="mixed", time=LT, seed=i), f"bsk{i}")


def light_body():
    """Warm light shining down into the picture from above (God is never drawn)."""
    cx, cy, r = INS
    gid = "lf9inlight"
    defs = S.rad_grad(gid, [(0, "#fff6d6", 0.95), (0.5, "#ffe7a8", 0.45), (1, "#ffe7a8", 0)], cx=0.5, cy=0.0, r=0.9)
    cone = "lf9cone"
    defs += S.lin_grad(cone, [(0, "#fff6d6", 0.75), (0.55, "#fff0c0", 0.25), (1, "#fff0c0", 0)])
    body = f'<rect x="{f1(cx - r)}" y="{f1(cy - r)}" width="{f1(2 * r)}" height="{f1(2 * r)}" fill="url(#{gid})"/>'
    for j, (a, w) in enumerate(((-0.55, 0.18), (-0.2, 0.22), (0.18, 0.2), (0.5, 0.16))):      # soft beams fanning down
        x0, x1 = cx + a * r * 0.5, cx + a * r * 1.2
        body += (f'<path d="M{f1(x0 - w * 30)},{f1(cy - r)} L{f1(x0 + w * 30)},{f1(cy - r)} L{f1(x1 + w * 120)},{f1(cy + r * 0.7)} '
                 f'L{f1(x1 - w * 120)},{f1(cy + r * 0.7)} Z" fill="url(#{cone})" opacity="0.7"/>')
    return _clip(body, "light"), defs


# the story inside the picture: Jesus hands bread to a mother with her baby
JX, JY, JS = INS[0] - 62, INS[1] + 180, 0.6       # Jesus (facing right)
MX, MY = INS[0] + 44, INS[1] + 172                # the mother (facing left)
KX, KY = INS[0] + 128, INS[1] + 154               # her child beside her


def story_body(stage, j_expr=None, m_expr=None):
    """stage 0: Jesus holds a piece of bread out, the mother reaches for it; 1: she has it (his near hand empty, the
    rest of the loaf still in his far hand)."""
    cx, cy, r = INS
    out = ""
    for (x, y, k, f, kind, v) in ((cx - 142, cy + 96, 0.4, 1, "man", 4), (cx + 158, cy + 90, 0.38, -1, "woman", 9),
                                  (cx - 70, cy + 70, 0.32, 1, "child", 3)):
        out += C.galilee_folk(x, y, k, f, kind=kind, variant=v, pose="sit_eat")
    out += C.ground_shadow(KX + 2, KY + 2, 0.58, 110, 0.18, color="#2a5a30")
    out += C.galilee_folk(KX, KY, 0.58, -1, kind="child", variant=7, pose="stand", expr=EX("e_in_child", "happy", look=(0.05, -0.06)))
    out += C.ground_shadow(MX + 2, MY + 2, JS, 130, 0.2, color="#2a5a30")
    out += C.galilee_folk(MX, MY, JS, -1, kind="mother", variant=2, pose="receive", food="bread" if stage else False,
                          expr=m_expr or ("delighted" if stage else "eager"))
    out += C.ground_shadow(JX + 2, JY + 2, JS, 140, 0.2, color="#2a5a30")
    o_loaf = PR._barley_loaf
    if stage:
        PR._barley_loaf = lambda state="whole", *a, **kw: "" if state == "piece" else o_loaf(state, *a, **kw)
    try:
        out += C.jesus(JX, JY, JS, 1, pose="give_bread", expr=j_expr)
    finally:
        PR._barley_loaf = o_loaf
    return _clip(out, f"story{stage}{j_expr}")


# ================================================================== the light and the card

def warm_body():
    """Golden evening: a gentle warm multiply, lightest round the children, deeper amber-rose toward the edges."""
    gid = "lf9warm"
    defs = (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f1(BLK_X - 80)}" cy="{f1(SEAT - 160)}" r="1500">'
            f'<stop offset="0" stop-color="#fffaf0"/><stop offset="0.35" stop-color="#fdf0d8"/>'
            f'<stop offset="0.7" stop-color="#f4d8b4"/><stop offset="1" stop-color="#e2b8a4"/></radialGradient>')
    return f'<rect x="-20" y="-20" width="2160" height="1230" fill="url(#{gid})"/>', defs


def low_sun_body():
    gid = "lf9lowsun"
    defs = S.rad_grad(gid, [(0, "#fff0c0", 0.85), (0.4, "#ffd890", 0.4), (1, "#ffc878", 0)])
    return f'<ellipse cx="120" cy="600" rx="1200" ry="620" fill="url(#{gid})"/>', defs


def kids_glow_body():
    gid = "lf9kids"
    defs = S.rad_grad(gid, [(0, "#fff3cc", 0.75), (0.45, "#ffdc96", 0.3), (1, "#ffdc96", 0)])
    return f'<ellipse cx="{f1(BLK_X)}" cy="{f1(SEAT - 150)}" rx="560" ry="420" fill="url(#{gid})"/>', defs


def end_card_body():
    x, y = END
    defs = S.rad_grad("lf9card", [(0, "#fff3d6", 0.92), (0.6, "#ffe9c0", 0.45), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{f1(x)}" cy="{f1(y - 30)}" rx="420" ry="116" fill="url(#lf9card)"/>' +
           S.text(x, y, "五饼二鱼 · 完", size=78, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return out, defs


# ================================================================== motion helpers

def compose(outer, own, q):
    """outer(t) then own(t) about the stage point q: the transform own(t) (a scale about q plus a translation, alpha)
    applied inside the outer transform (the picture's pop / flip / shrink). Both are Tf functions; own's pivot is q."""
    def m(t):
        a, b = outer(t), own(t)
        ox, oy = a.px, a.py
        dx = ox + a.dx + a.sx * (q[0] + b.dx - ox) - q[0]
        dy = oy + a.dy + a.sy * (q[1] + b.dy - oy) - q[1]
        return Tf(dx=dx, dy=dy, sx=a.sx * b.sx, sy=a.sy * b.sy, alpha=a.alpha * b.alpha, px=q[0], py=q[1])
    return m


def pop_own(t0, t1=1e9, dur=0.32, out=0.25, drop=0.0):
    """Own-motion of a little thing in the picture: pops in at t0 (back ease, optional drop from above), shrinks away
    over ``out`` s ending at t1."""
    def m(t):
        if t < t0 or t > t1:
            return Tf(alpha=0.0, sx=0.001, sy=0.001)
        k = M.ease("back")(min(1.0, (t - t0) / dur)) * (1 - M.progress(t, t1 - out, t1, "in") if t1 < 1e8 else 1.0)
        a = min(1.0, (t - t0) / 0.08) * ((1 - M.progress(t, t1 - out * 0.6, t1, "sine")) if t1 < 1e8 else 1.0)
        return Tf(sx=max(0.001, k), sy=max(0.001, k), alpha=a, dy=-drop * (1 - M.ease("out")(min(1.0, (t - t0) / dur))))
    return m


# ================================================================== build

def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines
    tm = Tm(ctx)

    t_kid = tm.at(0, "小朋友")
    t_five = [tm.at(0, "五个饼", k) for k in range(3)]
    t_two = [tm.at(0, "两条鱼", k) for k in range(3)]
    t_little = tm.at(0, "只有一点点")
    t_hand = tm.at(0, "在耶稣手里")
    t_bian = tm.at(0, "变成")
    t_duo = tm.at(0, "好多好多", 3)
    t_l1 = tm.at(1, "耶稣看见")
    t_love = tm.at(1, "疼爱")
    t_ai = tm.at(1, "疼爱", 1)
    t_care = tm.at(1, "照顾他们")
    t_knows = tm.at(1, "耶稣也知道")
    t_he = tm.at(1, "他也会照顾你")
    t_you = tm.at(1, "照顾你", 2)
    t_kid3 = tm.at(2, "小朋友")
    t_what = tm.at(2, "你有什么")
    t_end = L[2].end

    # ---------------------------------------------------------------- the picture-book corner: timing and motion
    cx, cy, r = INS
    P_ = kp(cx, cy)
    t_in = snap(t_five[0] - 0.16)
    t_flip = snap(t_l1 + 0.03)
    t_close = snap(t_knows - 0.02)
    t_gone = t_close + 0.4

    def inset_m(t):
        if t < t_in or t > t_gone:
            return Tf(alpha=0.0, sx=0.001, sy=0.001, px=P_[0], py=P_[1])
        k = M.ease("back")(min(1.0, (t - t_in) / 0.45)) * (1 - M.progress(t, t_close, t_gone, "in"))
        a = min(1.0, (t - t_in) / 0.12) * (1 - M.progress(t, t_gone - 0.15, t_gone, "sine"))
        u = (t - (t_flip - 0.22)) / 0.44
        fx = abs(math.cos(math.pi * u)) if 0 <= u <= 1 else 1.0
        return Tf(sx=max(0.001, k * max(0.02, fx)), sy=max(0.001, k), alpha=a, px=P_[0], py=P_[1],
                  dy=3 * math.sin(2 * math.pi * t / 3.0))

    def own_vis(t0, t1):
        return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)

    sc.add("inset_bg", doc2(inset_bg_body()), z=9.0, wc=0.4, motion=inset_m)
    t_fill = snap(t_bian - 0.04)
    loaves, fish = _loaf_spots()
    sc.add("cloth", doc2(cloth_body()), z=9.1, wc=0.3, motion=compose(inset_m, pop_own(t_in + 0.1, t_fill + 0.3, 0.3, 0.3), kp(cx, cy + 128)))
    loaf_t = [snap(t_five[0] + (t_five[2] + 0.12 - t_five[0]) * i / 4) for i in range(5)]
    for i, (x, y) in enumerate(loaves):
        sc.add(f"loaf{i}", doc2(loaf_body(i)), z=9.2 + 0.01 * i, wc=0.3,
               motion=compose(inset_m, M.combine(pop_own(loaf_t[i], t_fill + 0.06 * i + 0.22, drop=18),
                                                 lambda t, i=i: Tf(dy=-7 * M.progress(t, t_hand, t_hand + 0.8, "sine") *
                                                                   (1 + 0.3 * math.sin(2 * math.pi * (t / 1.6 + 0.2 * i))))),
                              kp(x, y)))
    fish_t = [snap(t_two[0] + 0.02), snap(t_two[1] + 0.02)]
    for i, (x, y, f) in enumerate(fish):
        sc.add(f"fish{i}", doc2(fish_body(i)), z=9.26 + 0.01 * i, wc=0.3,
               motion=compose(inset_m, M.combine(pop_own(fish_t[i], t_fill + 0.3 + 0.06 * i, drop=14),
                                                 lambda t: Tf(dy=-6 * M.progress(t, t_hand, t_hand + 0.8, "sine"))),
                              kp(x, y)))
    lb, ldefs = light_body()
    t_glow = snap(t_hand + 0.1)
    sc.add("inset_light", doc2(lb, ldefs), z=9.3, wc=0, blend="screen",
           motion=compose(inset_m, lambda t: Tf(alpha=M.progress(t, t_glow, t_glow + 0.7, "sine") * (1 - M.progress(t, t_flip - 0.25, t_flip, "sine"))
                                               * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.8))), kp(cx, cy)))
    spots = _basket_spots()
    bsk_t = [snap(t_fill + 0.12 + (t_duo - 0.1 - t_fill - 0.12) * i / 11) for i in range(12)]
    for i, (x, y, s) in enumerate(spots):
        sc.add(f"basket{i}", doc2(basket_body(i)), z=9.4 + 0.01 * i, wc=0.3,
               motion=compose(inset_m, M.combine(pop_own(bsk_t[i], dur=0.28, drop=10), own_vis(0, t_flip)), kp(x, y)))
    # the story frame (after the flip): Jesus hands bread to the mother; a heart
    c_hand = snap(t_love - 0.1)
    c_jsmile = snap(t_care + 0.04)
    sfr = [doc2(story_body(0)), doc2(story_body(1)), doc2(story_body(1, j_expr="smile"))]

    def story_fa(t):
        return 0.0 if t < c_hand else (1.0 if t < c_jsmile else 2.0)
    sc.add("story", sfr, z=9.6, wc=0.3, seed=95, frame_at=story_fa, motion=compose(inset_m, own_vis(t_flip, 1e9), P_))
    hx, hy = MX - 20, MY - 230
    sc.add("inset_heart", doc2(_clip(heart_markup(hx, hy, 17), "heart")), z=9.7, wc=0,
           motion=compose(inset_m, M.combine(pop_own(snap(t_ai), dur=0.35),
                                             lambda t: Tf(dy=-28 * M.progress(t, t_ai, t_ai + 1.6, "out") +
                                                          3 * math.sin(2 * math.pi * t / 1.3))), kp(hx, hy)))

    # ---------------------------------------------------------------- expressions
    g_us = EX("e_g_us", "happy", look=(-0.07, 0.0), blush=True)
    g_us_blink = EX("e_g_us_blink", "happy", eyes="closed", blush=True)
    g_up = EX("e_g_up", "delighted", look=(-0.09, -0.10))
    g_ponder = EX("e_g_ponder", "ponder", look=(-0.05, -0.05))
    g_wow = EX("e_g_wow", "overjoyed")
    g_watch = EX("e_g_watch", "kind", look=(-0.09, -0.10))
    g_watch_blink = EX("e_g_watch_blink", "kind", eyes="closed")
    g_friend = EX("e_g_friend", "happy", look=(0.04, 0.0), blush=True)
    g_think = EX("e_g_think", "ponder", look=(-0.06, -0.12))
    f_up = EX("e_f_up", "delighted", look=(0.08, -0.10))
    f_watch = EX("e_f_watch", "kind", look=(0.08, -0.10))
    f_girl = EX("e_f_girl", "happy", look=(0.04, 0.0), blush=True)
    f_us = EX("e_f_us", "happy", look=(-0.07, 0.0), blush=True)
    f_blink = EX("e_f_blink", "happy", eyes="closed", blush=True)

    # ---------------------------------------------------------------- the girl
    c_us = snap(t_kid + 0.02)
    c_up = snap(t_in + 0.2)
    c_ponder = snap(t_little + 0.02)
    c_awe = snap(t_hand + 0.1)
    c_wow = snap(t_duo - 0.4)
    c_watch = snap(t_flip + 0.25)
    c_friend = snap(t_close + 0.1)
    c_joy = snap(t_he + 0.04)
    c_us3 = snap(t_kid3 + 0.02)
    c_think = snap(t_what - 0.04)
    c_smile3 = snap(t_end + 0.32)

    gfig = Fig(ctx, "girl", kp(GX, SEAT), z=6.5, seed=71)

    def G(*a, **kw):
        return kbody(girl(*a, **kw))

    def G_think(expr):
        o_sh = PR._sandwich_half                          # her half is already bitten (as in 'smile' / 'eat')
        PR._sandwich_half = lambda bite=0.0, k=1.0: o_sh(0.6, k)
        try:
            return kbody(girl("hesitate", expr, box="fruit"))
        finally:
            PR._sandwich_half = o_sh
    gfig.at(0, G("eat", box="fruit"))
    gfig.at(c_us, G("smile", g_us, box="fruit"))
    gfig.at(c_up, G("smile", g_up, box="fruit"))
    gfig.at(c_ponder, G("smile", g_ponder, box="fruit"))
    gfig.at(c_awe, G("smile", EX("e_g_awe", "awed", look=(-0.07, -0.10)), box="fruit"))
    gfig.at(c_wow, G("smile", g_wow, box="fruit"))
    gfig.at(c_watch, G("smile", g_watch, box="fruit"))
    tb = snap(c_watch + 1.6)
    gfig.at(tb, G("smile", g_watch_blink, box="fruit")).at(snap(tb + 0.13), G("smile", g_watch, box="fruit"))
    gfig.at(c_friend, G("smile", g_friend, box="fruit"))
    gfig.at(c_joy, G("smile", box="fruit"))
    gfig.at(c_us3, G("smile", g_us, box="fruit"))
    gfig.at(c_think, G_think(g_think))
    gfig.at(c_smile3, G("smile", g_us, box="fruit"))
    for tb in (snap(c_smile3 + 1.5), snap(c_smile3 + 3.4)):
        if tb + 0.3 < T:
            gfig.at(tb, G("smile", g_us_blink, box="fruit")).at(snap(tb + 0.14), G("smile", g_us, box="fruit"))
    munch = keyed([(0.0, 1.0), (c_us - 0.25, 1.0), (c_us - 0.05, 0.0)], "sine")
    # she leans back a little to look up at the picture
    look_up = keyed([(c_up - 0.1, 0.0), (c_up + 0.3, 1.0), (c_friend - 0.3, 1.0), (c_friend + 0.1, 0.0)], "sine")
    tilt = keyed([(c_ponder, 0.0), (c_ponder + 0.4, 1.0), (c_awe - 0.2, 1.0), (c_awe + 0.1, 0.0),
                  (c_think, 0.0), (c_think + 0.4, 1.0), (c_smile3 - 0.2, 1.0), (c_smile3 + 0.1, 0.0)], "sine")
    gfig.move(dip(c_us, 4), dip(c_up, 3), dip(c_ponder, 3), dip(c_awe, 3), dip(c_wow, 4), dip(c_watch, 2), dip(c_friend, 3),
              dip(c_joy, 4), dip(c_us3, 3), dip(c_think, 3), dip(c_smile3, 4),
              hop(c_wow + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              hop(c_joy + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * t / 0.42) * munch(t), rot=-2.5 * tilt(t) - 3.0 * look_up(t)),
              breath(ctx, 0.011, 2.7))
    gfig.add(sc)

    # ---------------------------------------------------------------- the friend
    d_up = snap(c_up + 0.14)
    d_wow = snap(c_wow + 0.1)
    d_watch = snap(c_watch + 0.2)
    d_bite = snap(t_love - 0.3)
    d_bite_end = snap(t_care + 0.3)
    d_girl = snap(c_friend + 0.25)
    d_joy = snap(c_joy + 0.1)
    d_us3 = snap(c_us3 + 0.12)
    d_wave = snap(t_end + 0.6)
    d_wave_end = snap(d_wave + 1.92)

    ffig = Fig(ctx, "friend", kp(FX_, SEAT), z=6.4, seed=73)

    def F(*a, **kw):
        return kbody(friend(*a, **kw))
    ffig.at(0, F("eat"))
    ffig.at(d_up, F("smile", f_up))
    ffig.at(d_wow, F("smile"))
    ffig.at(d_watch, F("smile", f_watch))
    ffig.at(d_bite, F("eat"))
    ffig.at(d_bite_end, F("smile", f_watch))
    ffig.at(d_girl, F("smile", f_girl))
    ffig.at(d_joy, F("smile"))
    ffig.at(d_us3, F("smile", f_us))
    waves = [F("wave_sit", "overjoyed", phase=k / 4) for k in range(4)]
    ffig.cycle(d_wave, waves, step=3)
    ffig.at(d_wave_end, F("smile", f_us))
    for tb in (snap(d_wave_end + 1.1), snap(d_wave_end + 2.6)):
        if tb + 0.3 < T - 0.2:
            ffig.at(tb, F("smile", f_blink)).at(snap(tb + 0.14), F("smile", f_us))
    fmunch = keyed([(0.0, 1.0), (d_up - 0.25, 1.0), (d_up - 0.05, 0.0), (d_bite + 0.1, 0.0), (d_bite + 0.25, 1.0),
                    (d_bite_end - 0.25, 1.0), (d_bite_end - 0.05, 0.0)], "sine")
    f_look = keyed([(d_up - 0.1, 0.0), (d_up + 0.3, 1.0), (d_bite - 0.1, 1.0), (d_bite + 0.2, 0.0), (d_bite_end - 0.1, 0.0),
                    (d_bite_end + 0.2, 1.0), (d_girl - 0.3, 1.0), (d_girl + 0.1, 0.0)], "sine")
    ffig.move(dip(d_up, 3), dip(d_wow, 4), dip(d_watch, 2), dip(d_bite, 3), dip(d_bite_end, 3), dip(d_girl, 3), dip(d_joy, 4),
              dip(d_us3, 3), dip(d_wave, 3), dip(d_wave_end, 3),
              hop(d_wow + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              hop(d_joy + 0.05, [(0, {"dy": 0}), (0.13, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"]),
              lambda t: Tf(sy=1 + 0.02 * math.sin(2 * math.pi * t / 0.46) * fmunch(t), rot=3.0 * f_look(t)),
              breath(ctx, 0.011, 3.0, 0.4))
    ffig.add(sc)

    # ---------------------------------------------------------------- the park at golden evening, the light
    add_park(sc, evening=True)
    sc.add("low_sun", doc2(*low_sun_body()), z=0.08, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.8 + 0.08 * math.sin(2 * math.pi * t / 6.0)))
    sc.add("warm", doc2(*warm_body()), z=7.9, wc=0, blend="multiply")
    kg = keyed([(0, 0.08), (t_close, 0.08), (t_close + 1.2, 0.4), (t_you, 0.42), (t_you + 0.4, 0.55), (t_kid3 + 0.4, 0.38),
                (t_end, 0.32), (T, 0.35)], "sine")
    sc.add("kids_glow", doc2(*kids_glow_body()), z=8.0, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=kg(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.6))))

    # ---------------------------------------------------------------- hearts, card, sparkles
    hx0, hy0 = BLK_X, SEAT - 300
    heart_float2(sc, "heart0", hx0 - 10, hy0, 30, snap(t_you + 0.02), dx=-14, rise_px=170)
    heart_float2(sc, "heart1", hx0 + 60, hy0 + 30, 22, snap(t_you + 0.32), dx=16, rise_px=150)
    ex, ey = END
    t_card = snap(t_end + 2.0)          # after the child's full 2 s answer pause
    cb, cdefs = end_card_body()
    sc.add("endcard", doc2(cb, cdefs), z=20, wc=0, motion=M.keys(
        [(t_card, {"alpha": 0, "s": 0.95, "dy": 16 * K}), (t_card + 0.5, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=kp(ex, ey - 50)))
    th = t_card + 0.45
    hcx, hcy = kp(ex, ey + 62)
    sc.add("endheart", raw2(heart_markup(hcx, hcy, 26 * K)), z=20.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hcx, hcy)))
    sc.fx.append(ksparkles((cx - 160, cy - 30, cx + 160, cy + 160), count=9, t0=t_duo - 0.05, t1=t_flip - 0.2,
                           color=(255, 240, 196), size=(8, 15), period=1.2, drift=-10, seed=41))
    sc.fx.append(ksparkles((cx - 120, cy - 170, cx + 120, cy + 40), count=6, t0=t_glow + 0.2, t1=t_bian,
                           color=(255, 246, 214), size=(6, 11), period=1.5, drift=12, seed=43))
    sc.fx.append(ksparkles((ex - 400, ey - 110, ex + 400, ey + 30), count=6, t0=t_card + 0.4, size=(9, 16), period=2.0,
                           drift=0, seed=45))
    sc.fx.append(ksparkles((BLK_X - 360, SEAT - 420, BLK_X + 360, SEAT - 200), count=6, t0=t_you, t1=t_kid3 + 1.0,
                           color=(255, 238, 190), size=(8, 14), period=1.5, drift=-12, seed=47))
    sc.fx.append(FX.motes((300 * K, 300 * K, 2000 * K, 1100 * K), count=16, color=(255, 236, 196), size=(4, 9), seed=49, alpha=90))

    # ---------------------------------------------------------------- camera (design units, x K)
    c0 = kcam(BLK_X, 772, 1240)                        # the two children at their picnic
    ci = kcam(1150, 692, 1500)                         # the picture-book corner above the girl, both children
    ck = kcam(BLK_X, 792, 1100)                        # the two children, close
    ce = kcam(BLK_X, 730, 1300)                        # the children and the end card above them
    ce2 = kcam(BLK_X, 726, 1280)
    sc.camera = safe_camera([(0, c0), (0.7, c0), (t_in + 0.1, ci), (t_close, ci), (t_close + 1.8, ck),
                            (t_end + 0.3, ck), (t_card + 0.5, ce), (T, ce2)], "sine", SW, SH)

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T, gain_db=-30, fade_in=0.8, fade_out=1.6)
    sc.sfx("wind_soft", 0, dur=T, gain_db=-32, fade_in=0.8, fade_out=1.6)
    sc.sfx("pop", t_in, gain_db=-20, pan=-0.3)
    for t in loaf_t + fish_t:
        sc.sfx("pop", t, gain_db=-26, pan=-0.3)
    sc.sfx("chime", t_glow, gain_db=-16, pan=-0.3)
    for t in bsk_t[::3]:
        sc.sfx("pop", t, gain_db=-27, pan=-0.3)
    sc.sfx("sparkle", t_duo, gain_db=-16, pan=-0.3)
    sc.sfx("whoosh", t_flip - 0.2, gain_db=-24, pan=-0.3)
    sc.sfx("sparkle", t_ai, gain_db=-21, pan=-0.3)
    sc.sfx("chime", t_you + 0.05, gain_db=-14)
    sc.sfx("chime", t_card + 0.1, gain_db=-12)
    return sc
