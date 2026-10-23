"""Scene 12 - the closing page: the copper-haired girl of s02 at bedtime in her cosy lilac bedroom (cloud pyjamas),
sitting up in bed hugging the soft toy lamb from the supermarket. The full moon looks in at the window, the little moon
night light glows on its table, and on the wall hangs a framed picture-book page: the shepherd carrying the little lamb
home under the moon. God is never drawn: his love is shown as warm light from the picture.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame (page dip from s11): she hugs her lamb, eyes closed, smiling; the night light breathes, stars
               twinkle in the window
  '小朋友'      she opens her eyes and looks up at the picture
  '上帝就像这个牧羊人' the camera eases up to the picture on the wall, which glows softly (chime, sparkles)
  '你，'        back to the girl hugging her lamb ...
  '宝贝小羊'    ... she squeezes it, beaming (a heart pops up)
  '不管你走多远' the camera opens out to show the picture and the girl together; the picture glows warmly
  '上帝都会来找你' a soft beam of warm light reaches down from the picture to the girl (sparkle), she looks up into it
  '如果你做错了事' she looks at us kindly; '也不要怕' a small reassuring nod
  '你可以对上帝说' she sets the lamb on the quilt beside her and folds her hands; '对不起，我想回到你身边' eyes
               closed, a peaceful prayer face in a warm glow (the light swells gently)
  '小朋友，如果你是那只小羊' she opens her eyes, takes her lamb again and hugs it
  '被找到的时候' she looks at it fondly
  '你想对牧羊人说什么呢' she looks at us, thinking (eyes up), then smiles at us and holds that face through the 2 s
               pause; late in the pause (>= 1.5 s after the question) the end card '迷失的羊 · 完' fades in with a heart
               (chime); calm final frame for the film's fade-out.
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
from engine.scene import Scene
from stories.lost_sheep.scenes.s01_title import EX, heart_float
from stories.lost_sheep.scenes.s02_question import TOY_K, girl
from stories.nativity.scenes.s01_title import Fig, Twinkle, beat, breath, dip, doc, glow_svg, hop, keyed, snap
from stories.noah.scenes.s01_title import f1, heart_markup

INK = P["ink"]

FLR = 1150                                  # the bedroom floor line (cosy_bedroom y)
RS = 1.0                                    # room scale
WALL_Y = FLR - 40 * RS                      # where the wall meets the floor
WIN_X = 520                                 # the window
BED = (1150, 1166, 1.45, -1)                # kid_bed anchor, scale, facing (headboard on the right)
GS = BED[2]                                 # the girl's scale
SIT_DX = -112                               # she sits up near her pillow (local bed x; the recipe's 40 is mid-bed)
GIRL = (BED[0] + SIT_DX * GS * BED[3], BED[1] + PR.KID_BED_TOP * GS)
PIC = (1000, 296, 1.32)                     # the framed story picture: nail, scale
PIC_W, PIC_H = 290, 220
PIC_C = (PIC[0], PIC[1] + (54 + PIC_H / 2) * PIC[2])          # centre of the picture
NL = (1800, FLR + 6, 1.45)                  # the moon night light on its table
NL_C = (NL[0], NL[1] - 100 * NL[2])         # the lamp's centre
END = (1472, 612)                           # the end card (inside the final close shot)


# ================================================================== drawings

def room_svg():
    out = PR.cosy_bedroom(-40, W + 40, FLR, RS, glow=0.0, seed=5, window_x=WIN_X, frame_x=-9000, light_x=-9000)
    x, y, s = NL
    out += C.ground_shadow(x, y, s, 130, 0.2)
    out += PR.nightlight(x, y, s, glow=0.0)
    return doc(out)


def nightlight_lit_svg():
    x, y, s = NL
    return doc(PR.nightlight(x, y, s, glow=1.0))


def story_picture():
    """The picture-book page in the frame: the shepherd carrying the little lamb home under the moon, on the spring hills
    at night (this film's own designs, drawn small)."""
    w, h = PIC_W, PIC_H
    k = 0.3
    out = PR.spring_sky(-4, -4, w + 4, h + 4, time=1.0, moon=(w * 0.78, h * 0.25), clouds=0.35, stars=1.0, scale=k, seed=3)
    out += PR.spring_hills(-30, w + 30, h * 0.80, k, time=1.0, part="back", seed=4)
    out += PR.spring_hills(-30, w + 30, h * 0.80, k, time=1.0, part="mid", stream=False, seed=4)
    out += PR.spring_hills(-30, w + 30, h * 0.80, k, time=1.0, part="front", stream=False, flowers=0.6, seed=4)
    sx, sy, ss = w * 0.44, h * 0.92, 0.5
    out += C.ground_shadow(sx, sy, ss, 140, 0.25)
    out += C.parable_shepherd(sx, sy, ss, 1, pose="carry_b", lamb_eyes="happy", expr="joyful")
    out += (f'<ellipse cx="{f1(sx)}" cy="{f1(sy - 150)}" rx="90" ry="120" fill="#fff2c8" opacity="0.16" '
            f'filter="url(#soft)"/>')
    return out


def picture_svg():
    x, y, s = PIC
    return doc(PR.picture_frame(x, y, s, w=PIC_W, h=PIC_H, inner=story_picture(), color="#c9925a"))


def pic_glow_svg():
    cx, cy = PIC_C
    return glow_svg(cx, cy, 470, 400, "ls12pg", "#fff0c8", "#ffcf72", 0.8, 0.34)


def pic_inner_light_svg():
    """A warm light over the picture itself (clipped to the picture)."""
    x, y, s = PIC
    x0, y0 = x - PIC_W / 2 * s, y + 54 * s
    gid = "ls12pil"
    defs = S.rad_grad(gid, [(0, "#ffe8b0", 0.55), (0.6, "#ffd88a", 0.22), (1, "#ffd88a", 0.0)])
    return doc(f'<rect x="{f1(x0)}" y="{f1(y0)}" width="{f1(PIC_W * s)}" height="{f1(PIC_H * s)}" fill="url(#{gid})"/>', defs)


def beam_svg():
    """A soft ribbon of warm light from the picture down to the girl."""
    cx, cy = PIC_C
    gx, gy = GIRL[0] - 10, GIRL[1] - 90 * GS
    gid = "ls12beam"
    defs = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f1(cx)}" y1="{f1(cy)}" x2="{f1(gx)}" '
            f'y2="{f1(gy)}"><stop offset="0" stop-color="#fff0c4" stop-opacity="0.8"/>'
            f'<stop offset="0.65" stop-color="#ffdc94" stop-opacity="0.42"/>'
            f'<stop offset="1" stop-color="#ffd88a" stop-opacity="0.2"/></linearGradient>')
    dx, dy = gx - cx, gy - cy
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    w0, w1 = 120, 230
    pts = [(cx + nx * w0, cy + ny * w0), (gx + nx * w1, gy + ny * w1), (gx - nx * w1, gy - ny * w1),
           (cx - nx * w0, cy - ny * w0)]
    d = "M" + " L".join(f"{f1(a)},{f1(b)}" for a, b in pts) + " Z"
    body = f'<path d="{d}" fill="url(#{gid})" filter="url(#blur-md)"/>'
    return doc(body, defs)


def night_svg():
    """Night in the room: a soft blue-violet multiply, lightest round the girl and the night light, so the warm lights
    read."""
    cx, cy = (GIRL[0] + NL_C[0]) / 2, GIRL[1] - 40
    gid = "ls12night"
    defs = (f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f1(cx)}" cy="{f1(cy)}" r="1350">'
            f'<stop offset="0" stop-color="#fbf8ff"/><stop offset="0.3" stop-color="#ece6f6"/>'
            f'<stop offset="0.65" stop-color="#c3b8e0"/><stop offset="1" stop-color="#a296cc"/></radialGradient>')
    return doc(f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#{gid})"/>', defs)


def girl_glow_svg():
    gx, gy = GIRL
    return glow_svg(gx, gy - 90 * GS, 330, 300, "ls12gg", "#fff1cc", "#ffd890", 0.6, 0.22)


def bed_svg(part):
    x, y, s, f = BED
    return doc(PR.kid_bed(x, y, s, f, part=part))


def bed_shadow_svg():
    x, y, s, f = BED
    return doc(f'<ellipse cx="{x}" cy="{y + 6}" rx="{f1(330 * s)}" ry="{f1(26 * s)}" fill="#4a3a5a" opacity="0.25" '
               f'filter="url(#soft)"/>')


TOY_SIDE = (GIRL[0] - 112 * GS, BED[1] - 172 * GS)   # the toy lamb sitting on the quilt beside her while she prays


def toy_side_svg():
    x, y = TOY_SIDE
    return doc(PR.toy_lamb(x, y, TOY_K * GS * 1.05, -1, rot=6))


def nightlight_glow_svg():
    lx, ly = NL_C
    return glow_svg(lx, ly, 520, 460, "ls12nl", "#fff4d6", "#ffd27a", 0.6, 0.22)


def end_card_svg():
    x, y = END
    defs = S.rad_grad("ls12card", [(0, "#fff3d6", 0.92), (0.6, "#ffe9c0", 0.45), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 30}" rx="360" ry="112" fill="url(#ls12card)"/>' +
           S.text(x, y, "迷失的羊 · 完", size=74, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L = ctx.lines

    t_friend = beat(ctx, 0, "小朋友")
    t_god = beat(ctx, 0, "上帝")
    t_shep = beat(ctx, 0, "牧羊人")
    t_you = beat(ctx, 0, "你")
    t_treasure = beat(ctx, 0, "宝贝")
    t_l0 = L[0].end
    t_far = beat(ctx, 1, "不管")
    t_come = beat(ctx, 1, "上帝都会")
    t_find = beat(ctx, 1, "找你")
    t_l1 = L[1].end
    t_wrong = beat(ctx, 2, "如果")
    t_say = beat(ctx, 2, "你可以")
    t_sorry = beat(ctx, 2, "对不起")
    t_back = beat(ctx, 2, "我想")
    t_l2 = L[2].end
    t_kid = beat(ctx, 3, "小朋友")
    t_found = beat(ctx, 3, "被找到")
    t_what = beat(ctx, 3, "你想")
    t_q = beat(ctx, 3, "说什么")
    t_end = L[3].end

    # ---------------------------------------------------------------- expressions
    up_pic = EX("up_pic", "touched", look=(0.07, -0.13))
    up_light = EX("up_light", "touched", look=(0.06, -0.10))
    fond = EX("fond", "happy", look=(0.06, 0.08))
    at_us = EX("at_us", "kind", look=(-0.04, 0.0))
    at_us_smile = EX("at_us_smile", "happy", look=(-0.04, 0.0))
    blink_smile = EX("blink_smile", "happy", eyes="closed")
    think = EX("think", "neutral", look=(-0.07, -0.11), brow=(-0.06, 0.02, -0.07))
    beam_face = EX("beam_face", "cheery")

    # ---------------------------------------------------------------- the girl
    gx, gy = GIRL
    c_open = snap(t_friend + 0.1)                     # opens her eyes, looks up at the picture
    c_back = snap(t_you - 0.08)                        # back to her lamb
    c_squeeze = snap(t_treasure - 0.05)
    c_lookup = snap(t_come - 0.1)                      # looks up into the light
    c_us = snap(t_wrong + 0.05)                        # looks at us kindly
    c_nod = beat(ctx, 2, "不要")
    c_set = snap(t_say + 0.1)                          # sets the lamb down
    c_pray = snap(c_set + 0.5)                         # folds her hands
    c_take = snap(t_kid + 0.15)                        # takes her lamb again
    c_fond = snap(t_found - 0.05)
    c_us2 = snap(t_what - 0.1)
    c_think = snap(t_q - 0.25)
    c_smile = snap(t_end + 0.3)
    c_blinks = [snap(t_end + 1.35)]

    def body(pose, expr):
        return girl(gx, gy, pose, expr, -1, GS, outfit="cloud_pyjamas")

    gfig = Fig(ctx, "girl", (gx, gy), z=5, seed=91)
    gfig.at(0, body("sit_hug_toy", "peaceful"))
    gfig.at(c_open, body("sit_hug_toy", up_pic))
    gfig.at(c_back, body("sit_hug_toy", fond))
    gfig.at(c_squeeze, body("sit_hug_toy", beam_face))
    gfig.at(snap(t_l0 + 0.3), body("sit_hug_toy", "peaceful"))
    gfig.at(snap(t_far + 0.2), body("sit_hug_toy", fond))
    gfig.at(c_lookup, body("sit_hug_toy", up_light))
    gfig.at(c_us, body("sit_hug_toy", at_us))
    gfig.at(snap(c_nod + 0.4), body("sit_hug_toy", at_us_smile))
    gfig.at(c_set, body("sit_pray", EX("pray_open", "kind", look=(0.02, -0.04))))     # the lamb on the quilt
    gfig.at(c_pray, body("sit_pray", "peaceful"))
    gfig.at(c_take, body("sit_hug_toy", "happy"))
    gfig.at(c_fond, body("sit_hug_toy", fond))
    gfig.at(c_us2, body("sit_hug_toy", at_us))
    gfig.at(c_think, body("sit_hug_toy", think))
    gfig.at(c_smile, body("sit_hug_toy", at_us_smile))
    for tb in c_blinks:
        if tb + 0.3 < T:
            gfig.at(tb, body("sit_hug_toy", blink_smile)).at(snap(tb + 0.15), body("sit_hug_toy", at_us_smile))
    nod = hop(c_nod, [(0, {"rot": 0}), (0.16, {"rot": -2.5}), (0.42, {"rot": 0})], ["sine", "sine"])
    squeeze = hop(c_squeeze, [(0, {"sy": 1.0}), (0.12, {"sy": 0.97}), (0.3, {"sy": 1.02}), (0.5, {"sy": 1.0})],
                  ["out", "out", "sine"])
    sway_on = keyed([(c_fond, 0.0), (c_fond + 0.4, 1.0), (c_us2 - 0.3, 1.0), (c_us2, 0.0)], "sine")
    sway = lambda t: Tf(rot=1.6 * math.sin(2 * math.pi * (t - c_fond) / 1.9) * sway_on(t))      # noqa: E731
    gfig.move(dip(c_open, 3), dip(c_back, 3), dip(c_lookup, 3), dip(c_us, 3), dip(c_set, 4), dip(c_pray, 4),
              dip(c_take, 4), dip(c_us2, 3), dip(c_think, 2), dip(c_smile, 3), nod, squeeze, sway,
              breath(ctx, 0.01, 3.4))
    gfig.add(sc)

    # ---------------------------------------------------------------- the room
    sc.add("room", room_svg(), z=0, wc=0.8)
    sc.add("nl_lit", nightlight_lit_svg(), z=0.3, seed=97)
    sc.add("night", night_svg(), z=7.8, wc=0, blend="multiply")
    sc.add("nl_glow", nightlight_glow_svg(), z=8.0, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.6 + 0.2 * math.sin(2 * math.pi * t / 4.2)))
    sc.add("picture", picture_svg(), z=1, wc=0.6)
    sc.add("bed_shadow", bed_shadow_svg(), z=2, wc=0)
    sc.add("bed_back", bed_svg("back"), z=3, wc=0.8)
    sc.add("bed_front", bed_svg("front"), z=7, wc=0.8)
    sc.add("toy_side", toy_side_svg(), z=7.5, seed=95, motion=lambda t: Tf(alpha=1.0 if c_set <= t < c_take else 0.0))

    # ---------------------------------------------------------------- the picture's light
    soft = keyed([(t_god - 0.2, 0.0), (t_shep + 0.2, 0.55), (t_far, 0.45), (t_come, 1.0), (t_l1 + 0.6, 0.75),
                  (t_sorry - 0.3, 0.75), (t_back + 0.4, 1.0), (t_l2 + 0.8, 0.6)], "sine")
    sc.add("pic_glow", pic_glow_svg(), z=8.1, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=soft(t) * (0.88 + 0.12 * math.sin(2 * math.pi * t / 2.6))))
    sc.add("pic_light", pic_inner_light_svg(), z=8.2, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.6 * soft(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.1))))
    beam = keyed([(t_come - 0.15, 0.0), (t_find + 0.2, 1.0), (t_l1 + 0.8, 0.8), (t_say, 0.55), (t_back + 0.3, 0.85),
                  (t_l2 + 0.8, 0.35), (t_found, 0.25)], "sine")
    sc.add("beam", beam_svg(), z=8.3, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=beam(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 3.1))))
    warm = keyed([(t_come, 0.0), (t_find + 0.3, 0.7), (t_l1 + 0.8, 0.5), (c_pray, 0.6), (t_back + 0.4, 1.0),
                  (t_l2 + 0.8, 0.6), (t_end, 0.55)], "sine")
    sc.add("girl_glow", girl_glow_svg(), z=8.4, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=warm(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.8))))

    # ---------------------------------------------------------------- hearts
    hx, hy = gx - 40, gy - 190 * GS
    heart_float(sc, "heart0", hx, hy, 28, c_squeeze + 0.1, dx=-20, rise_px=190)
    heart_float(sc, "heart1", hx + 46, hy + 26, 18, c_squeeze + 0.35, dx=20, rise_px=160)
    heart_float(sc, "heart2", hx - 10, hy, 22, c_take + 0.25, dx=-15, rise_px=170)

    # ---------------------------------------------------------------- end card
    ex, ey = END
    t_card = snap(t_end + 1.8)          # the script leaves the child 2 s to answer: the card comes late in it
    sc.add("endcard", end_card_svg(), z=20, wc=0, motion=M.keys(
        [(t_card, {"alpha": 0, "s": 0.95, "dy": 16}), (t_card + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    th = t_card + 0.45
    sc.add("endheart", doc(heart_markup(ex, ey + 58, 24)), z=20.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(ex, ey + 58)))

    # ---------------------------------------------------------------- sparkles, stars
    pcx, pcy = PIC_C
    sc.fx.append(FX.sparkles((pcx - 230, pcy - 190, pcx + 230, pcy + 190), count=8, t0=t_god, t1=t_l2 + 1.0,
                             color=(255, 240, 196), size=(8, 15), period=1.7, drift=-6, seed=31))
    sc.fx.append(FX.sparkles((gx - 220, gy - 300 * GS, gx + 160, gy - 60 * GS), count=7, t0=t_come + 0.2, t1=t_l2 + 0.6,
                             color=(255, 238, 190), size=(8, 14), period=1.5, drift=-12, seed=33))
    sc.fx.append(FX.sparkles((ex - 380, ey - 120, ex + 380, ey + 40), count=6, t0=t_card + 0.4, size=(9, 16), period=2.0,
                             drift=0, seed=35))
    rng = random.Random(7)
    wx0, wx1 = WIN_X - 165 * RS, WIN_X + 165 * RS
    stars = [(rng.uniform(wx0, wx1), rng.uniform(WALL_Y - 880 * RS, WALL_Y - 560 * RS), rng.uniform(5, 9)) for _ in range(7)]
    sc.fx.append(Twinkle(stars, seed=37, base=0.5))
    sc.fx.append(FX.motes((500, 200, 1800, 1000), count=14, color=(255, 240, 210), seed=39, alpha=70))

    # ---------------------------------------------------------------- camera
    c0 = Cam(1160, 720, 1600)                         # the room: window, picture, the girl in bed
    c_pic = Cam(PIC_C[0] - 10, PIC_C[1] - 18, 860)    # the picture (the girl just below the frame)
    c_girl = Cam(gx - 20, gy - 150, 1000)             # the girl and her lamb
    c_both = Cam(1150, 660, 1320)                     # the picture and the girl together
    c_pray_ = Cam(gx - 40, gy - 160, 1060)
    c_q = Cam(1310, 792, 1000)                        # her face and the lamb; the end card comes in its top
    c_fin = Cam(1312, 792, 972)
    sc.camera = M.cam_keys([(0, c0), (t_god - 0.2, c0), (t_shep + 0.5, c_pic), (t_you - 0.35, c_pic),
                            (t_treasure + 0.4, c_girl), (t_far - 0.2, c_girl), (t_come + 0.6, c_both),
                            (t_l1 + 0.6, c_both), (t_say + 0.4, c_pray_), (t_l2 + 0.4, c_pray_), (t_found, c_q),
                            (t_end, c_q), (T, c_fin)], "sine")

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=T, gain_db=-26, fade_in=0.8, fade_out=1.5)
    sc.sfx("chime", t_god + 0.1, gain_db=-13)
    sc.sfx("pop", c_squeeze + 0.1, gain_db=-20)
    sc.sfx("sparkle", t_come + 0.1, gain_db=-15)
    sc.sfx("cloth", c_set, gain_db=-22)
    sc.sfx("sparkle", t_back + 0.2, gain_db=-19)
    sc.sfx("cloth", c_take, gain_db=-22)
    sc.sfx("pop", c_take + 0.25, gain_db=-22)
    sc.sfx("chime", t_card + 0.1, gain_db=-12)
    return sc
