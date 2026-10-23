"""Scene 2 - the opening question, in a bright supermarket (big window with trees and sky, shelves of colourful
boxes and bottles, a fruit stand): the copper-haired girl in mint dungarees walks behind her mum, who pushes a full
trolley along the aisle. On the bottom shelf, among the toys, sits a soft toy lamb.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers; fallback:
the subtitle chunks):
  start        calm, wide frame (1 s cross-dissolve from the title page): mum pushes the trolley to the left
               (planted-foot strides), the girl trots behind her
  '小朋友'      the toy lamb twinkles; the girl stops, turns back to it and clasps her hands - a toy lamb! (sparkle)
  '你有没有走丢过' she gazes at it, rocking happily on her toes; mum walks on and disappears round the end of the
               aisle (behind the near shelf on the left), the trolley first
  '找不到爸爸妈妈' she turns to show mum - and looks up: mum is gone (surprised); then 'lost': hand at the mouth, one
               shining tear, looking this way and that (pose flips sold by small dips); the camera eases in
  '心里是不是好着急' worried, still looking round (a little tremble), the camera a little closer; the 0.8 s pause holds
               her looking for mum
  '今天'        mum hurries back round the corner (running), the girl sees her (surprised -> happy)
  '耶稣要讲一个故事' mum kneels and they hug (hug_pair: mum kneel_hug, girl relieved_hug), rocking gently; hearts
  '故事里'      mum stands up smiling; the girl turns to the shelf
  '也有一个走丢的小家伙' she reaches for the toy lamb, lifts it off the shelf and hugs it (eyes closed, smiling);
               on '小家伙' she turns to mum with it, beaming (a heart). Calm last frame for the page turn into s03.

Shared with s12_end (same illustrator): girl() (child outfit='dungarees' / 'cloud_pyjamas' + custom poses), the toy
lamb size TOY_K.
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.lost_sheep.scenes.s01_title import EX, heart_float
from stories.nativity.scenes.s01_title import Fig, beat, breath, dip, doc, hop, keyed, snap
from stories.nativity.scenes.s03_angel import stepper
from stories.noah.scenes.s01_title import f1

INK = P["ink"]

SM_Y, SM_S = 1000, 1.0                   # supermarket floor line and scale (the shop is drawn a little smaller)
FY = 1020                                # the people's ground line
PS = 1.15                                # people scale
GX = 1090                                # where the girl stops (in front of the toy shelf)
TOY_K = 0.56                             # the toy lamb's size in her arms (relative to her scale; characters uses 0.56)
TOY = (1206, 848)                        # the toy lamb on the bottom shelf (its middle)
MKX = GX - C.PARENT_HUG_GAP * PS         # mum kneels here (facing right) for the hug
X0 = -40                                 # supermarket x0
X1 = W + 40

# ================================================================== the girl and mum (custom poses)

_G_POSES = {
    "admire": C._P(h=-4, legs=((5, 2), (-5, -2)), arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)),
                   hands=("none", "pray"), look=(0.06, -0.03), expr="touched"),
    "reach": C._P(t=12, h=-2, legs=((10, 4), (-6, -2)), arms=(("ik", "abs", 94, -150, 1), ("ik", "abs", 82, -142, 1)),
                  hands=("open", "open"), look=(0.07, 0.0), expr="touched"),
    "lift": C._P(t=4, h=-4, legs=((6, 2), (-5, -2)), arms=(("ik", "abs", 54, -128, 1), ("ik", "abs", 44, -120, 1)),
                 hands=("open", "open"), look=(0.05, 0.0), expr="cheery"),
}


def _toy_in_hands(D, k=TOY_K, hug=0.3, rot=-8):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        c = ((W0[0] + W1[0]) / 2 + 4, (W0[1] + W1[1]) / 2 + 2)
        s = f'<g transform="translate({f1(c[0])},{f1(c[1])}) rotate({rot}) scale({k})">{PR._toy_lamb(hug=hug)}</g>'
        return s + C._hand(W0, (0.3, 1.0), "open", D["skin"], hr) + C._hand(W1, (0.4, 1.0), "open", D["skin"], hr)
    return front


def girl(x, y, pose="stand", expr=None, facing=1, s=PS, outfit="dungarees", phase=0.0, toy=None, marks=True):
    """The copper-haired girl (characters.child outfit 'dungarees' / 'cloud_pyjamas') plus this scene's own poses:
    'admire' (hands clasped at the chest, gazing), 'reach' (both hands out to the shelf), 'lift' (holding the toy lamb
    in front of her)."""
    if pose in _G_POSES:
        ps = dict(_G_POSES[pose])
        if outfit == "cloud_pyjamas":
            D, m = C._cloud_pyjama_design(), C._metrics(C._CHILD, 1.0, 0.96)
        else:
            D, m = C._dungaree_design(), C._metrics(C._CHILD, 1.0, 0.98)
        fronts = [D.get("front")]
        if pose == "lift":
            fronts.append(_toy_in_hands(D))
        e = expr or ps["expr"]
        if e == "teary":
            fronts.append(C._teardrop_front)
        D["front"] = C._hooks(*fronts)
        inner, _ = C._figure(D, m, ps, e, C._fsign(facing), marks)
        return C._wrap_out(inner, x, y, s, facing, f"ls-girl-{outfit}-{pose}")
    return C.child(x, y, s, facing, pose=pose, expr=expr, outfit=outfit, phase=phase, toy=toy, marks=marks)


def girl_fn(x, y, s, f, **kw):
    return girl(x, y, s=s, facing=f, **kw)


def mum(x, y, pose="stand", expr=None, facing=1, s=PS, phase=0.0):
    """characters.parent(kind='mum') plus 'push_walk_a' / 'push_walk_b': pushing the trolley while walking."""
    if pose in ("push_walk_a", "push_walk_b"):
        ps = dict(C._PAZ["push"])
        ps["legs"] = C._PAZ["walk_a" if pose.endswith("a") else "walk_b"]["legs"]
        ps["t"] = 7
        D, m = C._parent_design("mum", ps["feet"])
        inner, _ = C._figure(D, m, ps, expr or "kind", C._fsign(facing), True)
        return C._wrap_out(inner, x, y, s, facing, f"ls-mum-{pose}")
    return C.parent(x, y, s, facing, kind="mum", pose=pose, expr=expr, phase=phase)


def mum_fn(x, y, s, f, **kw):
    return mum(x, y, s=s, facing=f, **kw)


def shadow(x, y=FY, w=120, s=PS, a=0.2):
    return C.ground_shadow(x, y, s, w, a, color="#6a5a48")


# ================================================================== drawings

def market_svg():
    """The supermarket (back) with a toy corner on the first shelf's bottom row (the toy lamb's place, a ball, a wooden
    horse, letter blocks, a little bunting)."""
    out = PR.supermarket(X0, X1, SM_Y, SM_S, part="back", seed=3)
    s = SM_S
    sy = SM_Y - 590 * s + 3 * 120 * s                 # the bottom row of shelf 1
    plank = sy + 104 * s
    cx0, cx1 = 1112, 1448
    toys = f'<rect x="{cx0}" y="{f1(sy - 4)}" width="{cx1 - cx0}" height="{f1(plank - sy + 3)}" fill="#e9e2d4"/>'
    toys += (f'<rect x="{cx0 + 6}" y="{f1(sy + 2)}" width="{cx1 - cx0 - 12}" height="{f1(plank - sy - 4)}" rx="6" '
             f'fill="#d9ecf2" stroke="{INK}" stroke-width="2.2"/>')
    bunt = ""
    for i in range(9):
        bx = cx0 + 22 + i * 35
        col = ("#e8573f", "#f2c43c", "#7cc4a2", "#8fc4ec", "#b7a8de")[i % 5]
        bunt += (f'<path d="M{bx},{f1(sy + 8)} l24,0 l-12,18 Z" fill="{col}" stroke="{INK}" stroke-width="2" '
                 f'stroke-linejoin="round"/>')
    toys += (f'<path d="M{cx0 + 12},{f1(sy + 8)} Q{(cx0 + cx1) / 2},{f1(sy + 14)} {cx1 - 12},{f1(sy + 8)}" stroke="{INK}" '
             f'stroke-width="2" fill="none"/>' + bunt)
    by = plank
    for j, (bx, col, lab) in enumerate(((1384, "#e8573f", "A"), (1414, "#7cc4a2", "B"), (1399, "#f2c43c", "C"))):
        yy = by - 29 - (29 if j == 2 else 0)
        toys += (f'<rect x="{bx}" y="{f1(yy)}" width="28" height="28" rx="4" fill="{col}" stroke="{INK}" stroke-width="2.4"/>'
                 f'<text x="{bx + 14}" y="{f1(yy + 21)}" font-family="LXGW WenKai" font-weight="bold" font-size="19" '
                 f'fill="#fffaf0" text-anchor="middle">{lab}</text>')
    toys += PR.toy(1282, by, 0.55, 1, kind="ball")
    toys += PR.toy(1344, by, 0.42, -1, kind="horse")
    toys += (f'<rect x="{TOY[0] - 30}" y="{f1(plank + 1)}" width="60" height="10" rx="2" fill="#fffaf0" stroke="{INK}" '
             f'stroke-width="1.6"/>')
    out += S.g(toys, filter="wobble-fine")
    return doc(out)


BALLOON = (1452, 700)


def balloon_svg():
    """A coral balloon tied to the toy corner (it bobs)."""
    x, y = BALLOON
    s = SM_S
    plank = SM_Y - 590 * s + 3 * 120 * s + 104 * s
    b = (f'<path d="M{x - 14},{plank - 2} Q{x + 10},{(plank + y) / 2 + 30} {x},{y + 46}" stroke="{INK}" stroke-width="2" '
         f'fill="none"/>')
    b += (f'<ellipse cx="{x}" cy="{y}" rx="36" ry="43" fill="#ee7a68" stroke="{INK}" stroke-width="3.2"/>'
          f'<path d="M{x - 7},{y + 42} L{x + 7},{y + 42} L{x},{y + 52} Z" fill="#ee7a68" stroke="{INK}" stroke-width="2.4" '
          f'stroke-linejoin="round"/><ellipse cx="{x - 12}" cy="{y - 16}" rx="7" ry="12" fill="#fffaf0" opacity="0.7"/>')
    return doc(S.g(b, filter="wobble-fine"))


FRONT_X0, FRONT_S = 20, 1.45            # the near shelf end on the left (bigger: it is close to us) - mum goes round it


def market_front_svg():
    return doc(PR.supermarket(FRONT_X0, X1, SM_Y, FRONT_S, part="front", seed=3))


def floor_light_svg():
    """Daylight from the big window lying on the shiny floor, and a few soft gloss streaks."""
    b = ""
    for cx, w in ((300, 300), (650, 280)):
        b += (f'<path d="M{cx - w / 2},{SM_Y - 96} L{cx + w / 2},{SM_Y - 96} L{cx + w / 2 + 160},{SM_Y + 60} '
              f'L{cx - w / 2 + 100},{SM_Y + 60} Z" fill="#fffbea" opacity="0.32" filter="url(#blur-md)"/>')
    for x, y, w in ((980, 1060, 260), (1500, 1080, 300), (1900, 1050, 220)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="12" fill="#fffdf4" opacity="0.35" filter="url(#soft)"/>'
    return doc(b)


def floor_shade_svg():
    """A soft shadow along the foot of the shelves and the fruit stand."""
    b = ""
    for x0, x1 in ((170, 870), (985, 1525), (1575, 2115)):
        b += (f'<rect x="{x0}" y="{SM_Y - 104}" width="{x1 - x0}" height="26" rx="13" fill="#7a6a58" opacity="0.18" '
              f'filter="url(#soft)"/>')
    return doc(b)


def shelf_toy_svg():
    x, y = TOY
    return doc(f'<ellipse cx="{x + 4}" cy="{y + 25}" rx="34" ry="5" fill="#6a5a48" opacity="0.25" filter="url(#soft)"/>'
               + PR.toy_lamb(x, y, TOY_K * PS, -1, rot=0))


def trolley_svg(x):
    return doc(shadow(x, FY, 230) + PR.trolley(x, FY, PS, -1, full=True))


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_lost = beat(ctx, 0, "你有没有")
    t_find = beat(ctx, 0, "找不到")
    t_heart = beat(ctx, 0, "心里")
    t_ji = beat(ctx, 0, "着急")
    t_l0 = L[0].end
    t_today = beat(ctx, 1, "今天")
    t_jesus = beat(ctx, 1, "耶稣")
    t_story = beat(ctx, 1, "故事里")
    t_also = beat(ctx, 1, "也有")
    t_little = beat(ctx, 1, "小家伙")
    t_end = L[1].end

    # ---------------------------------------------------------------- expressions
    look_back = EX("look_back", "happy", look=(-0.06, -0.02))
    tell = EX("tell", "happy", look=(0.05, -0.05))
    gone = EX("gone", "surprised", look=(0.04, -0.07))
    see_mum = EX("see_mum", "surprised", look=(0.06, -0.02))
    blink_touched = EX("blink_touched", "touched", eyes="closed")
    hug_smile = EX("hug_smile", "cheery")
    mum_smile = EX("mum_smile", "happy", look=(0.05, 0.06))

    # ---------------------------------------------------------------- the girl
    ga = C.body_points(girl_fn, 0, 0, 1, 1, pose="walk_a")["feet"]
    gb = C.body_points(girl_fn, 0, 0, 1, 1, pose="walk_b")["feet"]
    g_step = (ga[0][0] - gb[0][0]) * PS                      # planted-foot advance per drawing (stage px)
    n_g = 4
    g_cuts = [snap(0.18 + 0.29 * k) for k in range(n_g)]
    gdx, gdy, _ = stepper(g_cuts, g_step, PS, lift=4, move=0.2)
    g_x0 = GX + n_g * g_step                                   # she starts to the right, walking left

    c_stop = snap(g_cuts[-1] + 0.3)                          # stops (looking back over her shoulder)
    c_admire = snap(max(t_friend + 0.42, c_stop + 0.3))       # turns back: a toy lamb!
    c_blink = snap(t_lost + 0.5)
    c_turn = snap(t_find - 0.12)                             # turns to tell mum...
    c_gone = snap(t_find + 0.32)                             # ...mum is gone
    c_lost = snap(t_find + 0.86)
    flips = [c_lost]
    while flips[-1] + 0.7 < t_today - 0.25:
        flips.append(snap(flips[-1] + 0.7))
    if len(flips) % 2 == 0:                                  # end looking left (toward the corner mum went round)
        flips.pop()
    c_see = snap(t_today + 0.08)                             # sees mum running back
    c_hug = snap(t_jesus - 0.12)
    c_release = snap(t_story - 0.25)
    c_toshelf = snap(t_story + 0.25)
    c_reach = snap(t_also - 0.05)
    c_take = snap(t_also + 0.42)
    c_hugtoy = snap(c_take + 0.42)
    c_beam = snap(t_little - 0.1)
    c_blinkend = snap(min(T - 0.6, t_end + 0.55))

    gfig = Fig(ctx, "girl", (GX, FY), z=5, seed=71)
    sh = shadow(GX, FY, 110)
    walk_fr = [sh + girl(GX, FY, "walk_a", "happy", -1), sh + girl(GX, FY, "walk_b", "happy", -1)]
    gfig.at(0, walk_fr[0])
    for k, tc in enumerate(g_cuts):
        gfig.at(tc, walk_fr[(k + 1) % 2])
    gfig.at(c_stop, sh + girl(GX, FY, "stand", look_back, -1))
    gfig.at(c_admire, sh + girl(GX, FY, "admire", "touched", 1))
    gfig.at(c_blink, sh + girl(GX, FY, "admire", blink_touched, 1)).at(snap(c_blink + 0.14),
                                                                      sh + girl(GX, FY, "admire", "touched", 1))
    gfig.at(c_turn, sh + girl(GX, FY, "stand", tell, -1))
    gfig.at(c_gone, sh + girl(GX, FY, "stand", gone, -1))
    for i, tf_ in enumerate(flips):
        gfig.at(tf_, sh + girl(GX, FY, "lost", "teary", -1, phase=0.0 if i % 2 == 0 else 0.6))
    gfig.at(c_see, sh + girl(GX, FY, "stand", see_mum, -1))
    gfig.at(c_hug, sh + girl(GX, FY, "relieved_hug", "relieved", -1))
    gfig.at(c_release, sh + girl(GX, FY, "stand", "cheery", -1))
    gfig.at(c_toshelf, sh + girl(GX, FY, "admire", "touched", 1))
    gfig.at(c_reach, sh + girl(GX, FY, "reach", "touched", 1))
    gfig.at(c_take, sh + girl(GX, FY, "lift", "cheery", 1))
    gfig.at(c_hugtoy, sh + girl(GX, FY, "hug_toy", "peaceful", 1))
    gfig.at(c_beam, sh + girl(GX, FY, "hug_toy", hug_smile, -1))
    gfig.at(c_blinkend, sh + girl(GX, FY, "hug_toy", "peaceful", -1)).at(snap(c_blinkend + 0.16),
                                                                       sh + girl(GX, FY, "hug_toy", hug_smile, -1))

    rock_on = keyed([(c_admire + 0.3, 0.0), (c_admire + 0.7, 1.0), (c_turn - 0.3, 1.0), (c_turn - 0.05, 0.0)], "sine")
    tremble = keyed([(t_heart - 0.1, 0.0), (t_heart + 0.2, 1.0), (t_today - 0.4, 1.0), (t_today - 0.1, 0.0)], "sine")
    hug_rock = keyed([(c_hug + 0.25, 0.0), (c_hug + 0.6, 1.0), (c_release - 0.35, 1.0), (c_release - 0.05, 0.0)], "sine")
    HUG_PIV = ((GX + MKX) / 2, FY)

    # the girl's own walk offset: frames are drawn at GX; she starts at g_x0 and steps left
    def g_walk(t):
        if t >= c_stop:
            return Tf()
        return Tf(dx=(g_x0 - GX) - gdx(t), dy=gdy(t))

    def g_sway(t):
        return Tf(rot=2.2 * math.sin(2 * math.pi * (t - c_admire) / 1.3) * rock_on(t),
                  dx=1.6 * math.sin(2 * math.pi * t * 7.0) * tremble(t))

    def rock_about(foot):
        """The hug's gentle rock about the pair's contact point, for a layer whose pivot is ``foot``."""
        hx_, hy_ = HUG_PIV[0] - foot[0], HUG_PIV[1] - foot[1]

        def m(t):
            a = 1.4 * math.sin(2 * math.pi * (t - c_hug) / 1.7) * hug_rock(t)
            r = math.radians(a)
            return Tf(rot=a, dx=hx_ - (hx_ * math.cos(r) - hy_ * math.sin(r)),
                      dy=hy_ - (hx_ * math.sin(r) + hy_ * math.cos(r)))
        return m

    gfig.move(g_walk, g_sway,
              dip(c_stop, 4), dip(c_admire, 6), dip(c_turn, 4), dip(c_gone, 6, 0.94), *[dip(tf_, 4) for tf_ in flips],
              dip(c_see, 5), dip(c_hug, 6), dip(c_release, 4), dip(c_toshelf, 4), dip(c_reach, 4), dip(c_take, 5),
              dip(c_hugtoy, 5), dip(c_beam, 6), breath(ctx, 0.009, 2.8))
    hop_a = hop(c_admire, [(0, {"dy": 0}), (0.14, {"dy": -12}), (0.3, {"dy": 0})], ["out", "in"])
    hop_b = hop(c_beam + 0.12, [(0, {"dy": 0}), (0.14, {"dy": -10}), (0.3, {"dy": 0})], ["out", "in"])
    gfig.move(hop_a, hop_b, rock_about((GX, FY)))
    gfig.add(sc)

    # ---------------------------------------------------------------- mum
    pa = C.body_points(mum_fn, 0, 0, 1, 1, pose="push_walk_a")["feet"]
    pb = C.body_points(mum_fn, 0, 0, 1, 1, pose="push_walk_b")["feet"]
    m_step = (pa[0][0] - pb[0][0]) * PS                     # planted-foot advance per drawing (stage px)
    m_x0 = GX - 300                                          # at t=0 (walking left, ahead of the girl)
    m_exit = 100.0                                           # hidden behind the near shelf end from here
    n_m = int(math.ceil((m_x0 - m_exit) / m_step))
    m_cuts = [snap(0.1 + 0.33 * k) for k in range(n_m)]
    mdx, mdy, _ = stepper(m_cuts, m_step, PS, lift=3, move=0.24)
    m_gone = m_cuts[-1] + 0.2

    # running back in from the corner
    r_step = 160.0
    r_x0 = 150.0                                             # behind the near shelf end
    r_end = MKX - 84                                         # the last stride lands short; she slides into the kneel
    n_r = int(math.ceil((r_end - r_x0) / r_step))
    r_step = (r_end - r_x0) / n_r
    r_per = 5 / 30.0
    r_arrive = c_hug
    r_cuts = [snap(r_arrive - r_per * (n_r - k)) for k in range(n_r)]
    r_t0 = r_cuts[0] - r_per
    w = 1 / 30.0

    def r_x(t):
        v = r_x0
        for tk in r_cuts:
            v += r_step * min(1.0, max(0.0, (t - (tk - w)) / (2 * w)))
        return v

    def r_b(t):
        for tk in r_cuts:
            if tk - w <= t <= tk + w:
                return -10 * PS * math.sin(math.pi * (t - tk + w) / (2 * w))
        return 0.0

    def m_x(t):
        if t < m_gone + 0.5:
            return m_x0 - mdx(t)
        if t < r_t0:
            return r_x0
        return r_x(t)

    c_mstand = snap(c_release + 0.08)
    c_mblink = snap(c_toshelf + 0.9)
    mfig = Fig(ctx, "mum", (MKX, FY), z=6, seed=81)
    msh = shadow(MKX, FY, 140)
    pw = [msh + mum(MKX, FY, "push_walk_a", "kind", -1), msh + mum(MKX, FY, "push_walk_b", "kind", -1)]
    mfig.at(0, pw[0])
    for k, tc in enumerate(m_cuts):
        mfig.at(tc, pw[(k + 1) % 2])
    run = [msh + mum(MKX, FY, "run_a", "worried", 1), msh + mum(MKX, FY, "run_b", "worried", 1)]
    mfig.at(r_t0 - 0.05, run[0])
    for k, tc in enumerate(r_cuts):
        mfig.at(tc, run[(k + 1) % 2])
    mfig.at(c_hug, msh + mum(MKX, FY, "kneel_hug", "relieved", 1))
    mfig.at(c_mstand, msh + mum(MKX, FY, "smile", mum_smile, 1))
    mfig.at(c_mblink, msh + mum(MKX, FY, "smile", EX("mum_blink", "happy", eyes="closed"), 1))
    mfig.at(snap(c_mblink + 0.14), msh + mum(MKX, FY, "smile", mum_smile, 1))
    m_alpha = lambda t: 0.0 if (m_gone + 0.4 < t < r_t0 - 0.06) else 1.0          # noqa: E731

    def m_move(t):
        if t < m_gone + 0.5:
            return Tf(dx=m_x(t) - MKX, dy=mdy(t), alpha=m_alpha(t))
        slide = (MKX - r_end) * M.progress(t, c_hug - 0.12, c_hug + 0.08, "out")
        if t < c_hug + 0.08:
            return Tf(dx=m_x(t) - MKX + slide, dy=r_b(t), alpha=m_alpha(t))
        return Tf()
    mfig.move(m_move, dip(c_hug, 9, 0.93), dip(c_mstand, 6), breath(ctx, 0.008, 3.2, 0.4), rock_about((MKX, FY)))
    mfig.add(sc)

    # ---------------------------------------------------------------- the trolley (ahead of mum)
    t_ref = MKX - 210 * PS
    sc.add("trolley", trolley_svg(t_ref), z=4, seed=83,
           motion=lambda t: Tf(dx=m_x(t) - MKX, alpha=1.0 if t < m_gone + 0.4 else 0.0))

    # ---------------------------------------------------------------- the shop, the toy on the shelf
    sc.add("market", market_svg(), z=0, wc=0.7)
    sc.add("shelf_toy", shelf_toy_svg(), z=0.6, seed=85,
           motion=lambda t: Tf(alpha=1.0 if t < c_take else 0.0,
                               dy=-3 * M.progress(t, c_reach + 0.15, c_take, "sine")))
    sc.add("balloon", balloon_svg(), z=0.7, seed=87,
           motion=lambda t: Tf(dy=5 * math.sin(2 * math.pi * t / 2.6), rot=2.5 * math.sin(2 * math.pi * (t / 3.4 + 0.2)),
                               px=BALLOON[0] - 14, py=SM_Y - 126))
    sc.add("market_front", market_front_svg(), z=8, wc=0.7)
    sc.add("light", doc(f'<ellipse cx="560" cy="300" rx="760" ry="520" fill="#fffbe8" opacity="0.38" filter="url(#blur-lg)"/>'),
           z=0.4, wc=0, blend="screen", motion=lambda t: Tf(alpha=0.8 + 0.2 * math.sin(2 * math.pi * t / 6.0)))
    sc.add("floor_light", floor_light_svg(), z=0.45, wc=0, blend="screen")
    sc.add("floor_shade", floor_shade_svg(), z=0.42, wc=0)

    # ---------------------------------------------------------------- hearts and sparkles
    hx, hy = (GX + MKX) / 2, FY - 300 * PS
    heart_float(sc, "hug_heart0", hx, hy, 30, c_hug + 0.35, dx=-20, rise_px=200)
    heart_float(sc, "hug_heart1", hx + 50, hy + 30, 20, c_hug + 0.6, dx=25, rise_px=180)
    heart_float(sc, "hug_heart2", hx - 40, hy + 10, 18, c_hug + 0.9, dx=-30, rise_px=170)
    gtop = (GX + 30, FY - 250 * PS)
    heart_float(sc, "toy_heart", gtop[0], gtop[1], 26, c_beam + 0.12, dx=-15, rise_px=170, life=1.8)
    tx, ty = TOY
    sc.fx.append(FX.sparkles((tx - 70, ty - 70, tx + 70, ty + 30), count=5, t0=t_friend - 0.1, t1=t_friend + 1.6,
                             size=(9, 16), period=1.0, drift=-8, seed=21))
    sc.fx.append(FX.sparkles((GX - 60, FY - 330 * PS, GX + 120, FY - 150 * PS), count=5, t0=c_hugtoy, t1=c_hugtoy + 1.8,
                             size=(8, 14), period=1.2, drift=-14, seed=23))

    # ---------------------------------------------------------------- camera
    c0 = Cam(1010, 616, 1960)
    c_toy = Cam(1130, 716, 1520)
    c1 = Cam(1080, 742, 1400)
    c2 = Cam(1086, 772, 1250)
    c3 = Cam(1000, 742, 1520)
    c4 = Cam(1046, 760, 1300)
    c5 = Cam(1052, 772, 1180)
    sc.camera = M.cam_keys([(0, c0), (m_gone - 0.3, c0), (c_turn - 0.1, c_toy), (c_lost + 0.6, c1), (t_ji, c2),
                            (t_l0 + 0.3, c2), (r_t0 + 0.4, c3), (c_hug + 0.6, c4), (c_take, c4), (t_end + 0.2, c5),
                            (T, Cam(c5.x + 4, c5.y + 2, c5.w - 26))], "sine")

    # ---------------------------------------------------------------- sound
    sc.sfx("crowd", 0, dur=T, gain_db=-30, fade_in=0.9, fade_out=1.2, density=0.6)
    sc.sfx("footsteps", m_cuts[0] - 0.05, dur=m_cuts[-1] - m_cuts[0] + 0.3, gain_db=-22, fade_in=0.05, fade_out=0.4,
           pan=-0.3, rate=1 / 0.33)
    sc.sfx("footsteps", g_cuts[0] - 0.05, dur=g_cuts[-1] - g_cuts[0] + 0.25, gain_db=-24, fade_in=0.05, fade_out=0.2,
           rate=1 / 0.29)
    sc.sfx("sparkle", t_friend - 0.05, gain_db=-17, pan=0.2)
    sc.sfx("pop", c_gone, gain_db=-22)
    sc.sfx("footsteps_run", r_t0, dur=c_hug - r_t0 + 0.05, gain_db=-17, fade_in=0.1, fade_out=0.15, pan=-0.4)
    sc.sfx("cloth", c_hug, gain_db=-15)
    sc.sfx("pop", c_hug + 0.35, gain_db=-20)
    sc.sfx("cloth", c_take, gain_db=-20, pan=0.2)
    sc.sfx("sparkle", c_hugtoy, gain_db=-17)
    sc.sfx("pop", c_beam + 0.12, gain_db=-20)
    return sc
