"""Scene 9 — the dreams in prison (Genesis 40).

N '在监牢里，有两个人做了奇怪的梦。约瑟帮他们解梦，他说的都应验了。' / Y '能解梦的不是我，是上帝。'

s08's prison cell (same stage, drawings, positions and clocks): the scene opens on s08's last frame (plain 1 s
cross-dissolve) — Joseph standing in the warm golden window light, the king's cupbearer and baker dozing on the straw.

  line 0  '在监牢里，'                 calm; the camera eases over to frame Joseph and the two prisoners.
          '有两个人'                   the two prisoners wake up and stand (hop cuts); Joseph turns to them, kind.
          '做了奇怪的梦。'             they shrug, puzzled ('?'), and a dream bubble pops over each: the cupbearer's vine
                                       grows three branches, leaves, blossoms and ripe purple grapes; three birds land
                                       one by one on the baker's baskets of bread and peck.
          '约瑟帮他们解梦，'           Joseph explains with open hands; the two listen (amazed / thoughtful); the bubbles
                                       pop away.
          '他说的都应验了。'           a sunny picture bubble: the cupbearer back in the palace in his gold collar,
                                       smiling, handing Pharaoh his gold cup, with sparkles; in the cell he cheers (the
                                       baker's fate stays offscreen).
  line 1  '能解梦的不是我，'           Joseph puts his hand on his chest and shakes his head modestly.
          '是上帝。'                   he points up; the window light glows brighter and sparkles rise; the prisoners
                                       look up in wonder. Calm last frame (page-turn dip into s10).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes.s08_saul import Actor, pop_tf, pt, sparkle_dyn
from stories.joseph.scenes import s08_egypt as E
from stories.joseph.scenes.s08_egypt import (BAK_X, CAM_CELL2, CELL_BREATHE, CUP_X, GY, JC, KC, LOOK_UP_SOFT, SH, SW,
                                             doc, f1, jfig, jlib, person_sprite, prisoner_fig)

INK = P["ink"]
CAM9 = Cam(1736, 640, 1910)          # Joseph and both prisoners, room for the bubbles
CUP_B = (CUP_X - 130, 400, 450, 300)  # cupbearer's dream bubble: centre x, y, w, h
BAK_B = (BAK_X + 70, 372, 420, 300)  # baker's dream bubble
TRUE_B = (1800, 380, 720, 430)       # 'it came true' picture bubble


def _sky_inner(x, y, w, h, uid, warm=0.0):
    defs = S.lin_grad(uid, [(0, S.mix("#bfe2ea", "#f8dcae", warm)), (1, S.mix("#eef4dc", "#fbe9c6", warm))])
    out = f'<defs>{defs}</defs><rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="url(#{uid})"/>'
    return out


def cup_bubble_svg(grow):
    x, y, w, h = CUP_B
    inner = _sky_inner(x, y, w, h, "s9cs")
    inner += S.path(S.hill(x - w, x + w, y + 112, 30, seed=3, bumps=2, bottom=y + h), fill="#a9c76a", sw=3)
    inner += PR.grapevine(x - 10, y + 128, 0.86, grow=grow)
    return doc(PR.dream_bubble(x, y, w, h, tail=(CUP_X - 10, GY - 330 * KC), inner=inner, seed=4))


def bak_bubble_svg(birds):
    x, y, w, h = BAK_B
    inner = _sky_inner(x, y, w, h, "s9bs", 0.3)
    inner += S.path(S.hill(x - w, x + w, y + 112, 24, seed=6, bumps=2, bottom=y + h), fill="#d9c58d", sw=3)
    inner += PR.bread_baskets(x + 4, y + 120, 1.12, n=3, birds=birds)
    return doc(PR.dream_bubble(x, y, w, h, tail=(BAK_X + 10, GY - 330 * KC), inner=inner, seed=7))


def true_bubble_svg():
    """It came true: the cupbearer back in the palace, smiling, handing Pharaoh his gold cup."""
    x, y, w, h = TRUE_B
    defs = S.lin_grad("s9tb", [(0, "#f9e7bd"), (1, "#f3d79c")])
    inner = f'<defs>{defs}</defs><rect x="{x - w}" y="{y - h}" width="{2 * w}" height="{2 * h}" fill="url(#s9tb)"/>'
    inner += f'<rect x="{x - w}" y="{y + 140}" width="{2 * w}" height="{h}" fill="#d8b77e" stroke="{INK}" stroke-width="3"/>'
    s = 0.64
    inner += PR.egypt_column(x - 290, y + 144, 0.7) + PR.egypt_column(x + 295, y + 144, 0.7)
    inner += f'<path d="M{x - 380},{y - 150} L{x + 380},{y - 150}" stroke="#c9533f" stroke-width="10"/>'
    inner += f'<path d="M{x - 380},{y - 134} L{x + 380},{y - 134}" stroke="#3f6fa8" stroke-width="8"/>'
    inner += C.pharaoh(x + 120, y + 142, s, -1, pose="sit_throne", expr="happy")
    inner += C.egyptian(x - 80, y + 142, s * 1.02, 1, kind="cupbearer", pose="give", expr="happy")
    return doc(PR.dream_bubble(x, y, w, h, tail=(CUP_X - 20, GY - 345 * KC), inner=inner, seed=9))


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1 = ctx.lines[:2]
    T8, t_gold8 = E.s08_clock()
    toff = T8 - 1.0                     # s09 t = 0 is s08's t = T8 - 1 (the cross-dissolve)
    t_gold = t_gold8 - toff             # (negative: already glowing)

    # ---------------------------------------------------------------- beats
    t_wake = pt(ctx, 0, "有两个人") + 0.05          # the prisoners wake and stand
    t_turn = t_wake + 0.45                          # Joseph turns to them
    t_odd = pt(ctx, 0, "奇怪") - 0.15               # shrug + dream bubbles
    t_cupb, t_bakb = t_odd, t_odd + 0.3
    t_explain = pt(ctx, 0, "约瑟帮") + 0.02         # Joseph explains
    t_listen = pt(ctx, 0, "解梦") + 0.05
    t_bub_out = pt(ctx, 0, "他说的") - 0.3
    t_true = pt(ctx, 0, "他说的") + 0.05            # it came true
    t_cheer = pt(ctx, 0, "都应验") + 0.1            # the cupbearer cheers
    t_true_out = L1.start - 0.35
    t_bow = pt(ctx, 1, "能解梦") + 0.0              # hand on chest
    t_shake = pt(ctx, 1, "不是我") - 0.05           # shakes his head
    t_up = pt(ctx, 1, "是上帝") - 0.1               # points up
    t_bright = t_up + 0.1

    # ---------------------------------------------------------------- the cell (s08's layers)
    sc.add("cell_back", E.cell_back_svg(), wc=0.6)
    sc.add("cell_wall", E.cell_wall_svg(), wc=0.8)
    sc.add("cell_floor", E.cell_floor_svg(), wc=0.8)
    sc.add("gate", E.gate_svg(0.0), wc=0.4)

    def gold(t):
        return E.gold_env(t + toff, t_gold8)
    bright = lambda t: M.progress(t, t_bright, t_bright + 0.8, "sine")
    sc.add("beam", E.beam_svg(0.0, "s8b0"), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=E.beam_base_alpha(t + toff) * (1 - 0.6 * gold(t))))
    sc.add("beam_gold", E.beam_svg(1.0, "s8b1"), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=min(1.0, gold(t) * (0.88 + 0.12 * math.sin(2 * math.pi * (t + toff - t_gold8) / 2.6))
                                     + 0.25 * bright(t))))
    sc.add("jglow", E.glow_svg(JC + 10, GY - 180, 300, 290, "s8jg", a=0.85), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=E.gold_env(t + toff, t_gold8 + 0.3)
                               * (0.8 + 0.2 * math.sin(2 * math.pi * (t + toff - t_gold8) / 2.6))))
    sc.add("winglow", E.glow_svg(E.WIN_X, E.WIN_Y + 20, 330, 260, "s9wg", col="#ffe9a6", a=0.9), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=bright(t) * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.9))))

    # ---------------------------------------------------------------- the prisoners
    perfs = {}
    for name, kind, x, seed in (("cup", "cupbearer", CUP_X, 83), ("bak", "baker", BAK_X, 84)):
        sp = person_sprite(KC, seed=seed, shadow=200)
        d = dict(sit=prisoner_fig(sp, kind, "sit", "sleepy", marks=False))
        sp.shadow = (KC, 130)
        d.update(stand=prisoner_fig(sp, kind, "stand", "surprised", marks=False),
                 shrug=prisoner_fig(sp, kind, "shrug", "puzzled"),
                 listen=prisoner_fig(sp, kind, "stand", "amazed" if name == "cup" else "neutral", marks=False),
                 up=prisoner_fig(sp, kind, "amazed", "amazed", marks=False))
        if name == "cup":
            d["cheer"] = prisoner_fig(sp, kind, "cheer", "happy", marks=False)
            d["happy"] = prisoner_fig(sp, kind, "stand", "happy", marks=False)
        perfs[name] = (sp, d)
    # the sitting drawing keeps the wide shadow; standing drawings get the narrow one (added after the switch)
    sp, d = perfs["cup"]
    cup_sched = [(0, d["sit"], 0), (t_wake, d["stand"], 1.0), (t_odd, d["shrug"], 0.6), (t_listen, d["listen"], 0.5),
                 (t_cheer, d["cheer"], 1.0), (t_true_out, d["happy"], 0.4), (t_up + 0.35, d["up"], 0.7)]
    sp2, d2 = perfs["bak"]
    bak_sched = [(0, d2["sit"], 0), (t_wake + 0.22, d2["stand"], 1.0), (t_odd + 0.25, d2["shrug"], 0.6),
                 (t_listen + 0.2, d2["listen"], 0.5), (t_up + 0.5, d2["up"], 0.7)]
    for name, sched, x in (("cup", cup_sched, CUP_X), ("bak", bak_sched, BAK_X)):
        sp_, _ = perfs[name]
        amp, per, ph = CELL_BREATHE[name]
        sc.add_dynamic(name, Actor(sp_, sched, lambda t, x=x: (x, GY), breathe=amp, bper=per,
                                   phase=ph + toff / per))

    # ---------------------------------------------------------------- Joseph
    jsp = person_sprite(KC, seed=85)
    j_up0 = jfig(jsp, LOOK_UP_SOFT, "happy", KC, 1, label="lookup")
    j_stand = jlib(jsp, "stand", KC, 1, attire="slave", expr="kind")
    j_explain = jlib(jsp, "explain", KC, 1, attire="slave", expr="kind")
    j_talk = jlib(jsp, "talk", KC, 1, attire="slave", expr="happy")
    MODEST = C._P(h=6, legs=((6, 2), (-5, -2)), arms=(("fk", 10, 6), ("ik", "torso", 0.55, 0.74, 1)), expr="kind")
    j_modest = jfig(jsp, MODEST, "kind", KC, 1, label="modest")
    j_point = jlib(jsp, "point_up", KC, 1, attire="slave", expr="happy")
    jsched = [(0, j_up0, 0), (t_turn, j_stand, 0.6), (t_explain, j_explain, 0.6), (t_true + 0.2, j_talk, 0.4),
              (t_bow, j_modest, 0.5), (t_up, j_point, 0.9)]

    def shake(t):
        u = t - t_shake
        if 0 <= u <= 0.7:
            return 3.2 * math.sin(u * 2 * math.pi * 3.4) * (1 - u / 0.7)
        return 0.0
    amp, per, ph = CELL_BREATHE["jos"]
    sc.add_dynamic("joseph", Actor(jsp, jsched, lambda t: (JC, GY), breathe=amp, bper=per, phase=ph + toff / per,
                                   rot=shake))
    sc.add_dynamic("cell_sparkles", sparkle_dyn((JC - 260, GY - 520, JC + 260, GY - 60), count=16,
                                                t0=t_gold8 + 0.4 - toff, t1=1e9, color=(255, 236, 160), size=(8, 17),
                                                period=1.7, drift=-9, seed=31, tclock=toff))
    sc.add_dynamic("up_sparkles", sparkle_dyn((E.WIN_X - 220, E.WIN_Y - 60, E.WIN_X + 240, E.WIN_Y + 420), count=18,
                                              t0=t_bright, t1=1e9, color=(255, 240, 175), size=(9, 19), period=1.4,
                                              drift=-14, seed=37))

    # ---------------------------------------------------------------- dream bubbles
    cx, cy = CUP_B[0], CUP_B[1]
    vine = [cup_bubble_svg(g) for g in (0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.88, 1.0)]
    t_grow0 = t_cupb + 0.35

    def vine_fa(t):
        return float(min(7, max(0, int((t - t_grow0) / 0.2))))
    sc.add("cup_bubble", vine, wc=0.4, frame_at=vine_fa,
           motion=lambda t: pop_tf(t, t_cupb, t_bub_out, cx, cy + 100, dur_in=0.4))
    bx, by = BAK_B[0], BAK_B[1]
    birds = [bak_bubble_svg(b) for b in (0, 1, 2, 3)]
    t_bird0 = t_bakb + 0.4

    def bird_fa(t):
        return float(min(3, max(0, int((t - t_bird0) / 0.32) + 1))) if t >= t_bird0 else 0.0

    def bak_m(t):
        tf = pop_tf(t, t_bakb, t_bub_out + 0.08, bx, by + 100, dur_in=0.4)
        return tf
    sc.add("bak_bubble", birds, wc=0.4, frame_at=bird_fa, motion=bak_m)
    tx, ty = TRUE_B[0], TRUE_B[1]
    sc.add("true_bubble", true_bubble_svg(), wc=0.4,
           motion=lambda t: pop_tf(t, t_true, t_true_out, tx, ty + 120, dur_in=0.42))
    sc.add_dynamic("true_sparkles", sparkle_dyn((tx - 280, ty - 170, tx + 280, ty + 140), count=14, t0=t_true + 0.3,
                                                t1=t_true_out, color=(255, 240, 170), size=(9, 18), period=1.2,
                                                drift=-6, seed=41))

    # ---------------------------------------------------------------- camera
    sc.camera = M.cam_keys([(0.0, CAM_CELL2), (1.05, CAM_CELL2), (t_odd + 0.2, CAM9), (t_bow, CAM9),
                            (T, Cam(1700, 650, 1960))], "sine")
    sc.fx = [FX.vignette(lambda t: 0.42, color=(46, 32, 22)),
             FX.tint((255, 214, 120), lambda t: 0.13 * gold(t) + 0.05 * bright(t), mode="screen")]

    # ---------------------------------------------------------------- sound
    sc.sfx("drip", 0, dur=T, gain_db=-21, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_wake, gain_db=-14, pan=0.4)
    sc.sfx("cloth", t_wake + 0.22, gain_db=-16, pan=0.6)
    sc.sfx("cloth", t_turn, gain_db=-18, pan=0.0)
    sc.sfx("pop", t_cupb, gain_db=-11, pan=0.3)
    sc.sfx("pop", t_bakb, gain_db=-12, pan=0.6)
    sc.sfx("grow", t_grow0, gain_db=-16, pan=0.3)
    sc.sfx("birds", t_bird0 - 0.1, dur=1.6, gain_db=-20, fade_in=0.2, fade_out=0.5, pan=0.6)
    sc.sfx("cloth", t_explain, gain_db=-17)
    sc.sfx("pop", t_bub_out, gain_db=-16, pan=0.4)
    sc.sfx("pop", t_true, gain_db=-10, pan=0.2)
    sc.sfx("sparkle", t_true + 0.25, gain_db=-13, pan=0.2)
    sc.sfx("cheer", t_cheer, dur=1.2, gain_db=-26, fade_in=0.1, fade_out=0.5, pan=0.3)
    sc.sfx("pop", t_true_out, gain_db=-17, pan=0.2)
    sc.sfx("cloth", t_bow, gain_db=-18)
    sc.sfx("cloth", t_up, gain_db=-15)
    sc.sfx("chime", t_bright, gain_db=-9)
    sc.sfx("sparkle", t_bright + 0.4, gain_db=-13)
    return sc
