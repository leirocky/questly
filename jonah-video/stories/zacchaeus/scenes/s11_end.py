"""Scene 11 - the closing page: the boy of the street festival (s02) at home in the evening with his dad (parent
kind='dad', variant=1). They sit on the mustard sofa in the sage-blue living room - the window shows the city at dusk
with lit windows and a crescent moon, the floor lamp glows, the bookshelf is full of picture books, and on the right
the front door with its little window and red knot ('如果耶稣今天到你家来'). Dad holds the picture book open at
Zacchaeus in the sycamore-fig. God is never drawn: love is warm light.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame (page dip from s10): dad reads, the boy leans in to the book; the lamp breathes, the city
               lights twinkle in the window
  '耶稣知道撒该的名字' the camera eases in; on '撒该' the boy points at Zacchaeus in the tree on the page and a soft glow
               comes on the page (sparkle)
  '你的名字'    on '你' the boy looks up at dad, delighted; dad smiles back at him
  '耶稣都爱你'   a warm light rises round the boy; on '爱' a heart pops up over him (chime)
  '他也想住进你的心里' dad puts his arm round him and leans his cheek on his cap (a custom seated hug; the book rests on
               dad's lap), the boy snuggles in, eyes closed; on '心' the light swells and a second heart floats up
  '小朋友'      they sit up again
  '到你家来'    the camera has opened out to the front door; the boy turns and glances at it (a soft warm light
               glows in its little window) ...
  '你想对他说什么呢' ... then looks at us, thinking (eyes up), and smiles at us after the question, holding that face
               through the 2 s answer pause; ~1.8 s after the question the end card '撒该爬上桑树 · 完' fades in with a
               heart (chime), fully visible ~2 s before the film's 1.6 s fade-out; calm, alive final frame (breathing,
               blinks, the lamp, the twinkling city).
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
from stories.nativity.scenes.s01_title import Fig, Twinkle, beat, breath, dip, hop, keyed, snap
from stories.noah.scenes.s01_title import f1, heart_markup
from stories.zacchaeus.scenes.s01_title import EX

INK = P["ink"]

W, H = 2640, 1485                    # a larger stage (x1.25) so the close shots of the sofa stay crisp
RS = 1.25                            # room and people scale
FLR = 1290                           # the floor line (evening_room y)
WALL_Y = FLR - 40 * RS
SX = 1320                            # the sofa (the middle of the room)
DX = SX - 60 * RS                    # dad (anchor = the floor), facing right
BX, BY = SX + 88 * RS, FLR - PR.SOFA_SEAT * RS      # the boy (anchor = the seat), facing left
DOOR_X = W * 0.86
WIN_X = W * 0.2
LAMP_X = W * 0.36
END = (1366, 770)                    # the end card: on the wall between the family picture and their heads


def doc(body, defs=""):
    return S.svg_doc(body, defs, W, H)


def glow_svg(cx, cy, rx, ry, gid, c0="#fff4d0", c1="#ffd986", a0=0.9, a1=0.38):
    defs = S.rad_grad(gid, [(0, c0, a0), (0.45, c1, a1), (1, c1, 0)])
    return doc(f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>', defs)


def heart_float(sc, name, x0, y0, r, t0, dx=0.0, rise_px=220, life=2.4, z=9.5):
    """A little heart that pops in at t0 and floats up, fading (on this scene's larger stage)."""
    def m(t):
        if t < t0 or t > t0 + life:
            return Tf(alpha=0.0)
        u = (t - t0) / life
        s_ = M.ease("back")(min(1.0, (t - t0) / 0.35))
        a = min(1.0, (t - t0) / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine"))
        return Tf(dx=dx * u + 9 * math.sin(2 * math.pi * (t - t0) / 1.3), dy=-rise_px * M.ease("out")(u),
                  sx=s_, sy=s_, alpha=a, px=x0, py=y0)
    sc.add(name, doc(heart_markup(x0, y0, r)), z=z, wc=0, motion=m)


# ================================================================== people

BOOK = (80, -94, 0.8, -3)            # the picture book on dad's lap (dad-local bottom middle at scale 1, size, tilt)


def book_stage(lx=0.0, ly=0.0):
    """Stage point of a point given relative to the book's bottom middle (book-local px at its own size)."""
    bx, by, bs, br = BOOK
    a = math.radians(br)
    x, y = lx * bs, ly * bs
    return DX + (bx + x * math.cos(a) - y * math.sin(a)) * RS, FLR + (by + x * math.sin(a) + y * math.cos(a)) * RS


def _book_front(D, hands=2):
    """The open picture book (Zacchaeus in the sycamore-fig on the left page) held up on dad's lap: both hands at its
    bottom corners (reading), or only the near hand (while his far arm hugs the boy)."""
    bx, by, bs, br = BOOK

    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        G = st["ground"]
        s = f'<g transform="translate({f1(bx)},{f1(by + G)}) rotate({br}) scale({bs})">{PR._picture_book(1.0)}</g>'
        if hands == 2:
            s += C._hand(W0, (0.2, -1.0), "open", D["skin"], hr)
        return s + C._hand(W1, (-0.2, -1.0), "open", D["skin"], hr)
    return front


def _dad_custom(ps, expr, hands, key):
    D, m = C._fdad_design(ps["feet"])
    D["front"] = C._hooks(D.get("front"), _book_front(D, hands))
    inner, _ = C._figure(D, m, ps, expr, C._fsign(1), True)
    return C._wrap_out(inner, DX, FLR, RS, 1, f"zq11-dad-{key}")


def _near_grip():
    bx, by, bs, br = BOOK
    return bx - 75 * bs + 6, by - 2


def dad(pose, expr="kind"):
    """Dad on the sofa (anchor = the floor, facing right): 'read' holds the picture book up on his lap for the boy;
    'hug' leans in with his cheek on the boy's cap, the far arm round the boy's back, the book still on his lap under his
    near hand."""
    bx, by, bs, br = BOOK
    ng = _near_grip()
    if pose == "read":
        ps = C._P(t=5, h=18, arms=(("ik", "abs", bx + 75 * bs - 4, by - 4, 1), ("ik", "abs", ng[0], ng[1], 1)),
                  hands=("open", "open"), expr=expr, **C._SEAT)
        return _dad_custom(ps, expr, 2, "read")
    if pose == "hug":
        sh = C.body_points(C.child, BX, BY, RS, -1, pose="sit_read", outfit="tracksuit")["shoulders"]
        fx, fy = (sh[0][0] - DX) / RS, (sh[0][1] - FLR) / RS
        ps = C._P(t=12, h=24, arms=(("ik", "abs", fx + 8, fy + 2, 1), ("ik", "abs", ng[0], ng[1], 1)),
                  hands=("open", "open"), expr=expr, **C._SEAT)
        return _dad_custom(ps, expr, 1, "hug")
    raise ValueError(pose)


PAGE_PIC = (-22, -44)                 # the picture on the left page (book-local): Zacchaeus in the tree


def boy(pose, expr=None, facing=-1):
    """The boy on the sofa (anchor = the seat, facing left toward dad); 'point' leans in and puts a finger on Zacchaeus
    in the book (an IK reach to the picture)."""
    if pose == "point":
        D, m = C._tracksuit_design()
        tx, ty = book_stage(*PAGE_PIC)
        lx, ly = (BX - tx) / RS, (ty - BY) / RS
        e = expr or "delighted"
        ps = C._P(t=7, h=14, legs=((80, 6), (74, 2)), arms=(("ik", "body", 30, 2, 1), ("ik", "abs", lx, ly, 1)),
                  hands=("open", "point"), expr=e, look=(0.04, 0.09), **C._ZC_SEAT)
        inner, _ = C._figure(D, m, ps, e, C._fsign(-1), True)
        sx, sy = C._seat_point(m)
        return C._wrap_out(C._reanchor(inner, sx, sy), BX, BY, RS, -1, "zq11-boy-point")
    return C.child(BX, BY, RS, facing, pose=pose, expr=expr, outfit="tracksuit")


def book_point():
    return book_stage(0, -46)


# ================================================================== drawings

def room_svg():
    return doc(PR.evening_room(-40, W + 40, FLR, RS, glow=0.75, seed=3, door_x=DOOR_X, window_x=WIN_X))


def sofa_svg(part):
    out = ""
    if part == "back":
        out += (f'<ellipse cx="{SX}" cy="{FLR + 4}" rx="{f1(300 * RS)}" ry="{f1(22 * RS)}" fill="#6a4a30" opacity="0.28" '
                f'filter="url(#soft)"/>')
    return doc(out + PR.sofa(SX, FLR, RS, part=part))


def lamp_glow_svg():
    return glow_svg(LAMP_X, WALL_Y - 560 * RS, 620, 560, "zq11lamp", "#fff3cc", "#ffd27a", 0.55, 0.2)


def page_glow_svg():
    px, py = book_stage(*PAGE_PIC)
    return glow_svg(px, py, 150, 120, "zq11page", "#fff6d8", "#ffe39a", 0.85, 0.36)


def boy_glow_svg():
    return glow_svg(BX - 10, BY - 110 * RS, 360, 330, "zq11boy", "#fff1cc", "#ffd890", 0.6, 0.24)


def door_light_svg():
    """A soft warm light in the front door's little window (lit while the closing question is asked)."""
    dw_y = WALL_Y - 560 * RS + 60 * RS
    return glow_svg(DOOR_X, dw_y + 35 * RS, 120 * RS, 100 * RS, "zq11door", "#fff4d0", "#ffd98a", 0.85, 0.3)


def warm_svg():
    """Evening warmth: a gentle golden multiply lightest round the sofa and the lamp, deeper at the edges."""
    cx, cy = (SX + LAMP_X) / 2, FLR - 260
    gid = "zq11warm"
    defs = (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f1(cx)}" cy="{f1(cy)}" r="1700">'
            f'<stop offset="0" stop-color="#fffdf6"/><stop offset="0.4" stop-color="#fbf0dc"/>'
            f'<stop offset="0.75" stop-color="#e9d2b8"/><stop offset="1" stop-color="#cdb4a6"/></radialGradient>')
    return doc(f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#{gid})"/>', defs)


def end_card_svg():
    x, y = END
    defs = S.rad_grad("zq11card", [(0, "#fff3d6", 0.92), (0.6, "#ffe9c0", 0.45), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 30}" rx="430" ry="118" fill="url(#zq11card)"/>' +
           S.text(x, y, "撒该爬上桑树 · 完", size=78, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


def window_lights():
    """Points of the lit windows in the city seen through the window (for twinkles)."""
    rng = random.Random(17)
    ww, wh = 420 * RS, 560 * RS
    wtop = WALL_Y - 300 * RS - wh
    pts = []
    for _ in range(9):
        pts.append((WIN_X + rng.uniform(-0.42, 0.42) * ww, wtop + wh * rng.uniform(0.55, 0.93), rng.uniform(5, 8)))
    for _ in range(3):
        pts.append((WIN_X + rng.uniform(-0.4, 0.1) * ww, wtop + wh * rng.uniform(0.06, 0.3), rng.uniform(4, 6)))
    return pts


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_jesus = beat(ctx, 0, "耶稣知道")
    t_zac = beat(ctx, 0, "撒该")
    t_also = beat(ctx, 0, "也知道")
    t_you = beat(ctx, 0, "你的名字")
    t_l0 = L[0].end
    t_nomatter = beat(ctx, 1, "不管")
    t_loves = beat(ctx, 1, "耶稣都爱你")
    t_ai = beat(ctx, 1, "爱你")
    t_wants = beat(ctx, 1, "他也想")
    t_heart = beat(ctx, 1, "心里")
    t_l1 = L[1].end
    t_kid = beat(ctx, 2, "小朋友")
    t_if = beat(ctx, 2, "如果")
    t_home = beat(ctx, 2, "到你家来")
    t_say = beat(ctx, 2, "你想对他")
    t_what = beat(ctx, 2, "说什么")
    t_end = L[2].end

    # ---------------------------------------------------------------- expressions
    at_book = EX("b_book", "happy", look=(0.05, 0.08))
    book_blink = EX("b_book_blink", "happy", eyes="closed")
    up_dad = EX("b_up_dad", "delighted", look=(0.06, -0.10))
    snug = EX("b_snug", "grateful")
    think = EX("b_think", "neutral", look=(-0.07, -0.11), brow=(-0.06, 0.02, -0.07))
    us_smile = EX("b_us_smile", "happy", look=(-0.05, 0.0))
    us_blink = EX("b_us_blink", "happy", eyes="closed")
    to_door = EX("b_door", "eager", look=(0.07, -0.03))
    d_book = EX("d_book", "kind", look=(0.04, 0.08))
    d_book_blink = EX("d_book_blink", "kind", eyes="closed")
    d_boy = EX("d_boy", "happy", look=(0.06, 0.08))
    d_boy_kind = EX("d_boy_kind", "kind", look=(0.06, 0.08))
    d_boy_blink = EX("d_boy_blink", "kind", eyes="closed")

    # ---------------------------------------------------------------- the boy
    c_point = snap(t_zac - 0.12)
    c_lookup = snap(t_you - 0.08)
    c_read2 = snap(t_nomatter + 0.9)
    c_snug = snap(t_wants + 0.06)
    c_unsnug = snap(t_kid - 0.05)
    c_door = snap(t_home - 0.04)
    c_back = snap(t_say - 0.12)
    c_think = snap(t_what - 0.05)
    c_smile = snap(t_end + 0.35)

    bfig = Fig(ctx, "boy", (BX, BY), z=5, seed=91)
    bfig.at(0, boy("sit_read", at_book))
    bfig.at(snap(1.25), boy("sit_read", book_blink)).at(snap(1.38), boy("sit_read", at_book))
    bfig.at(c_point, boy("point", "delighted"))
    bfig.at(c_lookup, boy("sit_read", up_dad))
    bfig.at(c_read2, boy("sit_read", at_book))
    bfig.at(snap(t_loves + 0.55), boy("sit_read", EX("b_warm", "delighted", look=(-0.02, -0.04))))
    bfig.at(c_snug, boy("sit_read", snug))
    bfig.at(c_unsnug, boy("sit_read", EX("b_after", "happy", look=(0.04, -0.06))))
    bfig.at(c_door, boy("sit_read", to_door, facing=1))
    bfig.at(c_back, boy("sit_read", EX("b_ponder_us", "neutral", look=(-0.05, -0.02), brow=(-0.07, 0.02, -0.09))))
    bfig.at(c_think, boy("sit_read", think))
    bfig.at(c_smile, boy("sit_read", us_smile))
    for tb in (snap(c_smile + 1.25), snap(c_smile + 3.3)):
        if tb + 0.3 < T:
            bfig.at(tb, boy("sit_read", us_blink)).at(snap(tb + 0.14), boy("sit_read", us_smile))

    snug_on = keyed([(c_snug - 0.05, 0.0), (c_snug + 0.35, 1.0), (c_unsnug - 0.3, 1.0), (c_unsnug + 0.05, 0.0)], "sine")
    think_tilt = keyed([(c_think, 0.0), (c_think + 0.4, 1.0), (c_smile - 0.2, 1.0), (c_smile + 0.1, 0.0)], "sine")
    bfig.move(lambda t: Tf(rot=-5.5 * snug_on(t) + 2.5 * think_tilt(t), dx=-10 * snug_on(t)),
              dip(c_point, 3), dip(c_lookup, 4), dip(c_read2, 3), dip(c_snug, 3), dip(c_unsnug, 3), dip(c_door, 4),
              dip(c_back, 4), dip(c_think, 2), dip(c_smile, 3),
              hop(c_lookup + 0.05, [(0, {"dy": 0}), (0.12, {"dy": -7}), (0.28, {"dy": 0})], ["out", "in"]),
              breath(ctx, 0.012, 2.7))
    bfig.add(sc)

    # ---------------------------------------------------------------- dad
    c_dsmile = snap(c_point + 0.3)
    c_dboy = snap(c_lookup + 0.1)
    c_dbook = snap(c_read2 + 0.2)
    c_hug = snap(c_snug - 0.04)
    c_unhug = snap(c_unsnug + 0.02)
    dfig = Fig(ctx, "dad", (DX, FLR), z=4.8, seed=93)
    dfig.at(0, dad("read", d_book))
    dfig.at(snap(2.0), dad("read", d_book_blink)).at(snap(2.14), dad("read", d_book))
    dfig.at(c_dsmile, dad("read", EX("d_book_smile", "happy", look=(0.04, 0.08))))
    dfig.at(c_dboy, dad("read", d_boy))
    dfig.at(c_dbook, dad("read", d_book))
    dfig.at(snap(t_loves + 0.3), dad("read", d_boy_kind))
    dfig.at(c_hug, dad("hug", "peaceful"))
    dfig.at(c_unhug, dad("read", d_boy))
    dfig.at(snap(c_back + 0.3), dad("read", d_boy_kind))
    for tb in (snap(c_smile + 2.2), snap(c_smile + 4.2)):
        if tb + 0.3 < T:
            dfig.at(tb, dad("read", d_boy_blink)).at(snap(tb + 0.14), dad("read", d_boy_kind))
    hug_rock = keyed([(c_hug + 0.3, 0.0), (c_hug + 0.7, 1.0), (c_unhug - 0.35, 1.0), (c_unhug - 0.05, 0.0)], "sine")
    dfig.move(dip(c_dboy, 3), dip(c_hug, 4), dip(c_unhug, 4),
              lambda t: Tf(rot=1.2 * math.sin(2 * math.pi * (t - c_hug) / 1.8) * hug_rock(t)),
              breath(ctx, 0.008, 3.3, 0.4))
    dfig.add(sc)

    # ---------------------------------------------------------------- the room
    sc.add("room", room_svg(), z=0, wc=0.8)
    sc.add("sofa_back", sofa_svg("back"), z=1, wc=0.8)
    sc.add("sofa_front", sofa_svg("front"), z=6, wc=0.8)
    sc.add("warm", warm_svg(), z=7, wc=0, blend="multiply")
    sc.add("lamp_glow", lamp_glow_svg(), z=7.2, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.75 + 0.12 * math.sin(2 * math.pi * t / 4.4) + 0.05 * math.sin(2 * math.pi * t / 1.7)))

    # ---------------------------------------------------------------- the light of the story
    page = keyed([(c_point - 0.05, 0.0), (c_point + 0.6, 1.0), (c_lookup + 0.8, 0.75), (c_read2, 0.55), (t_l1, 0.4),
                  (t_end, 0.35)], "sine")
    sc.add("page_glow", page_glow_svg(), z=7.4, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=page(t) * (0.88 + 0.12 * math.sin(2 * math.pi * t / 1.9))))
    warm_boy = keyed([(t_loves - 0.1, 0.0), (t_ai + 0.3, 0.85), (c_snug + 0.2, 0.7), (t_heart + 0.3, 1.0),
                      (t_l1 + 0.6, 0.6), (c_door, 0.35), (c_smile, 0.45)], "sine")
    sc.add("boy_glow", boy_glow_svg(), z=7.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=warm_boy(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.6))))
    door = keyed([(c_door - 0.3, 0.0), (c_door + 0.5, 1.0), (c_back + 0.5, 0.75), (T, 0.7)], "sine")
    sc.add("door_light", door_light_svg(), z=7.6, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=door(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.3))))

    # ---------------------------------------------------------------- hearts
    hx, hy = BX - 20, BY - 220 * RS
    heart_float(sc, "heart0", hx, hy, 30, snap(t_ai + 0.02), dx=-18, rise_px=210)
    heart_float(sc, "heart1", hx - 70, hy + 10, 26, snap(t_heart + 0.02), dx=-14, rise_px=200)
    heart_float(sc, "heart2", hx - 20, hy + 40, 18, snap(t_heart + 0.32), dx=20, rise_px=170)

    # ---------------------------------------------------------------- end card
    ex, ey = END
    t_card = snap(t_end + 1.8)          # the script leaves the child 2 s to answer: the card comes late in it
    sc.add("endcard", end_card_svg(), z=20, wc=0, motion=M.keys(
        [(t_card, {"alpha": 0, "s": 0.95, "dy": 16}), (t_card + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    th = t_card + 0.45
    sc.add("endheart", doc(heart_markup(ex, ey + 62, 26)), z=20.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(ex, ey + 62)))

    # ---------------------------------------------------------------- sparkles, twinkles
    bpx, bpy = book_point()
    sc.fx.append(FX.sparkles((bpx - 75, bpy - 45, bpx + 5, bpy + 35), count=5, t0=c_point + 0.1, t1=c_lookup + 1.2,
                             color=(255, 240, 196), size=(7, 12), period=1.3, drift=-3, seed=31))
    sc.fx.append(FX.sparkles((BX - 280, BY - 430 * RS, BX + 120, BY - 255 * RS), count=7, t0=t_ai, t1=t_l1 + 0.8,
                             color=(255, 238, 190), size=(8, 14), period=1.5, drift=-12, seed=33))
    sc.fx.append(FX.sparkles((ex - 420, ey - 120, ex + 420, ey + 40), count=6, t0=t_card + 0.4, size=(9, 16), period=2.0,
                             drift=0, seed=35))
    sc.fx.append(Twinkle(window_lights(), seed=37, base=0.45, color=(255, 226, 150), period=(1.4, 3.0)))
    sc.fx.append(FX.motes((700, 500, 2300, 1300), count=12, color=(255, 240, 210), seed=39, alpha=60))

    # ---------------------------------------------------------------- camera
    c0 = Cam(1360, 830, 2300)                     # the living room: window, lamp, sofa, bookshelf, front door
    c1 = Cam(1386, 1036, 1120)                    # the book, the boy's finger, their faces
    c2 = Cam(1372, 1010, 1360)                    # the two of them on the sofa
    c3 = Cam(1378, 1016, 1200)                    # the hug
    c4 = Cam(1760, 930, 1780)                     # opened out to the front door
    c5 = Cam(1700, 950, 1560)                     # the boy, dad and the door; the end card on the wall above them
    c6 = Cam(1700, 952, 1536)
    cq = Cam(1420, 1012, 1250)                    # the boy's face while he thinks and smiles at us
    sc.camera = M.cam_keys([(0, c0), (t_friend + 0.3, c0), (t_zac + 0.3, c1), (t_l0 + 0.2, c1), (t_nomatter + 0.9, c2),
                            (t_wants - 0.3, c2), (t_wants + 0.6, c3), (t_kid - 0.2, c3), (t_home - 0.1, c4),
                            (t_say - 0.1, c4), (t_end + 0.1, cq), (t_end + 0.7, cq), (t_end + 2.2, c5), (T, c6)], "sine")

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=T, gain_db=-30, fade_in=0.8, fade_out=1.6)
    sc.sfx("sparkle", c_point + 0.1, gain_db=-17)
    sc.sfx("pop", c_lookup + 0.05, gain_db=-23)
    sc.sfx("chime", t_ai + 0.05, gain_db=-14)
    sc.sfx("cloth", c_hug, gain_db=-22)
    sc.sfx("sparkle", t_heart + 0.1, gain_db=-17)
    sc.sfx("cloth", c_door, gain_db=-24)
    sc.sfx("chime", t_card + 0.1, gain_db=-12)
    return sc
