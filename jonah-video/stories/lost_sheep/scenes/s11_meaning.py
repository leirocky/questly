"""Scene 11 - Luke 15:7, Matthew 18:14. Back at the meal in the evening light. It opens on Jesus with his story page
still open above him (the shepherd carrying his lamb home under the moon); the camera draws back over the courtyard
while the page folds up and settles back into Jesus' hands (mirroring s04). Jesus speaks of the joy in heaven: gentle golden light
and sparkles pour down over the courtyard (light only) and the guests' faces light up. He sits down and offers bread to
the tax collector, and a round picture above them shows the shepherd hugging his found lamb: the same love. Warm light
spreads over everyone, a little heart over each guest; the Pharisees soften and think.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Nativity film's
Tm class, chunk fallback; nothing is hard-coded to the take):
  0 .. 0.9      calm (the page-dip lands here): the evening courtyard, Jesus standing with the open story page glowing
                above him (the shepherd with the lamb on his shoulders, lantern, moon), the guests listening; every
                face sits well above the subtitle band
  '讲完故事'     the camera draws gently back to the whole courtyard (faces only ever move up, away from the
                subtitle) while the page folds up above Jesus (unfold 1 -> 0) ...
  '耶稣说'       ... and floats down into his open hands, where it vanishes in a twinkle
  Z '一个做错事的人' Jesus speaks to everyone (tell)
  '回到'         he opens his arms wide (come back home)
  '天上'         soft golden rays and sparkles pour down from the sky over the courtyard (chime); the guests look up,
                their faces light up one after another (touched)
  '欢欢喜喜'     joy: Jesus' welcome, the guests beam and raise their cups (cheery), sparkles dance (sparkle)
  '耶稣和这些人' Jesus sits down beside the tax collector (hop) and holds out a piece of bread to him ...
  '吃饭'         ... the tax collector takes it, touched
  '牧羊人'       a round picture pops up above the two of them (pop): the shepherd kneeling, hugging his found lamb;
                the Pharisees glance at each other
  '小羊'         a little heart pops over the lamb in the picture and one over the tax collector (the same love)
  '在上帝眼里'   the picture melts away; a warm glow spreads out from Jesus over the whole table
  '每一个人'     a little heart pops over each guest, one on each syllable (每 一 个 人 都 是), each one touched
  '宝贝'         the glow is at its warmest
  '上帝一个也'   the light reaches the Pharisees (a few sparkles): the elder thinks, hand on the chin; on '失去' he
                and the tall one soften (hand on the heart, eyes down), the stout one ponders - thoughtful, not
                converted, not mocked
  end          calm warm tableau for the page-turn into s12
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.lost_sheep.scenes.s03_meal import (H3, INK, K, SEATS, SEAT_Y, STAND_Y, TY, W3, add_air, add_flyers,
                                                add_front, add_gate_overlay, add_set, add_sparrows, cam_seq,
                                                coin_stack_svg, doc3, f1, sunlight_svg)
from stories.lost_sheep.scenes.s04_story import (GY_P, PHT, PW, book_motion, hands_mid, page_frames, page_glow_svg,
                                                 seated_actors, unfold_at)
from stories.nativity.scenes.s07_shepherds import Tm, env

BUBBLE = (1838, 476, 142)            # the round picture above Jesus and the tax collector: centre, radius


def page_inner_night(phase=0.0):
    """The end of Jesus' story in page coordinates: the shepherd carrying the found lamb home over the moonlit hills,
    his lantern glowing, the flock waiting on the hillside."""
    s = 0.55
    gy = GY_P
    sx = 90
    pts = PR.spring_hills_points(0, PW, gy, s, stream_x=sx)
    b = PR.spring_sky(0, 0, PW, PHT, time=1.0, moon=(160, 98), clouds=0.6, scale=s, seed=6)
    b += PR.spring_hills(0, PW, gy, s, time=1.0, part="back", stream_x=sx, flowers=0.6)
    b += PR.spring_hills(0, PW, gy, s, time=1.0, part="mid", stream_x=sx, flowers=0.6)
    b += PR.flock(470, 840, gy - 140 * s, gy + 24, n=18, scale=s * 0.8, time=1.0, top=pts["mid_top"], phase=phase,
                  seed=5)
    b += PR.spring_hills(0, PW, gy, s, time=1.0, part="front", stream_x=sx, flowers=0.6)
    b += PR.lantern_light(330, gy - 40, s, radius=200, k=0.8)
    b += C.parable_shepherd(350, gy + 44, s, 1, pose="carry_a", lamb_eyes="happy", lantern=True, glow=1.0)
    return b


def bubble_svg():
    """A round picture-book vignette: the shepherd kneeling on the moonlit hill, hugging the lamb he found."""
    cx, cy, r = BUBBLE
    cid = "ls11bub"
    gid = "ls11bsky"
    defs = (S.lin_grad(gid, [(0, "#3d4f86"), (0.6, "#6f7fb4"), (1, "#a8a6c8")]) +
            f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}"/></clipPath>')
    s = 0.62
    gy = cy + r * 0.62
    inner = f'<rect x="{f1(cx - r)}" y="{f1(cy - r)}" width="{f1(2 * r)}" height="{f1(2 * r)}" fill="url(#{gid})"/>'
    inner += PR._circ(cx - r * 0.5, cy - r * 0.5, 22, "#f4eccf", 3) + PR._ls_glow(cx - r * 0.5, cy - r * 0.5, 70, 70, 0.5,
                                                                                    "ls11moon", "#fffbe6", "#d8dcf0")
    for i, (x_, y_) in enumerate(((0.3, -0.6), (0.6, -0.3), (-0.1, -0.75), (0.15, -0.35))):
        inner += PR._twinkle(cx + r * x_, cy + r * y_, 6 + 2 * (i % 2), "#fff6d0")
    inner += PR._p(S.hill(cx - r - 20, cx + r + 20, gy + 10, 46, seed=4, bottom=cy + r + 20), "#5d7a6e", 3)
    inner += PR._p(S.hill(cx - r - 20, cx + r + 20, gy + 40, 20, seed=7, bottom=cy + r + 20), "#6e8f78", 3)
    inner += PR.lantern_light(cx + 40, gy - 40, s, radius=150, k=0.9)
    inner += C.parable_shepherd(cx + 10, gy + 18, s, 1, pose="kneel_hug", lantern=True, glow=1.0, lamb_eyes="closed")
    b = (f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 16)}" fill="#fbf1dc" stroke="{INK}" stroke-width="4"/>'
         f'<g clip-path="url(#{cid})">{inner}</g>'
         f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="none" stroke="{INK}" stroke-width="3.5"/>')
    return doc3(f'<g filter="url(#wobble-fine)">{b}</g>', defs)


def bubble_dot_svg(x, y, r):
    return doc3(f'<g filter="url(#wobble-fine)"><circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fbf1dc" '
                f'stroke="{INK}" stroke-width="3.5"/></g>')


def heart_svg(x, y, r, fill="#ef8d8d"):
    d = (f"M{f1(x)},{f1(y + r * 0.9)} C{f1(x - r * 1.5)},{f1(y - r * 0.1)} {f1(x - r * 0.9)},{f1(y - r * 1.2)} "
         f"{f1(x)},{f1(y - r * 0.45)} C{f1(x + r * 0.9)},{f1(y - r * 1.2)} {f1(x + r * 1.5)},{f1(y - r * 0.1)} "
         f"{f1(x)},{f1(y + r * 0.9)} Z")
    return doc3(f'<g filter="url(#wobble-fine)"><path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="3.2" '
                f'stroke-linejoin="round"/><ellipse cx="{f1(x - r * 0.45)}" cy="{f1(y - r * 0.3)}" rx="{f1(r * 0.2)}" '
                f'ry="{f1(r * 0.13)}" fill="#fbd6cc"/></g>')


def rays_svg():
    """Heaven's joy as light only: soft golden rays from high above the courtyard."""
    gid = "ls11ray"
    defs = S.rad_grad(gid, [(0, "#fff7d8", 0.85), (0.5, "#ffe6a6", 0.3), (1, "#ffe6a6", 0)])
    b = f'<ellipse cx="1760" cy="-80" rx="1500" ry="820" fill="url(#{gid})"/>'
    b += S.path(S.rays(1760, -260, 120, 1500, n=11, width_deg=5.5, rot=36), fill="#fff3cc", stroke=False,
                extra='opacity="0.5" filter="url(#blur-md)"')
    return doc3(b, defs)


def warm_glow_svg():
    gid = "ls11warm"
    defs = S.rad_grad(gid, [(0, "#ffd99a", 0.6), (0.55, "#ffc878", 0.2), (1, "#ffc878", 0)])
    return doc3(f'<ellipse cx="{SEATS["jesus"]}" cy="760" rx="1200" ry="520" fill="url(#{gid})"/>', defs)


def table_lamps_svg(k):
    """Two little clay lamps lit on the table (k flickers the glow)."""
    b = ""
    for x in (1240, 2010):
        b += PR._g(PR._oil_lamp(True, f"ls11tl{x}{k}"), f"translate({x},{f1(TY - 78 * K - 18)}) scale({0.55 * K:.3f})")
        b += PR._ls_glow(x + 20, TY - 78 * K - 60, 150, 110, 0.55 + 0.15 * k, f"ls11tlg{x}{k}")
    return doc3(f'<g filter="url(#wobble-fine)">{b}</g>')


def build(ctx):
    sc = Scene(ctx, W=W3, H=H3)
    T = ctx.duration
    g0 = ctx.start
    tm = Tm(ctx)
    at = tm.at
    rng = random.Random(110)

    t_jwgs = at(0, "讲完")
    t_shuo = at(0, "耶稣说")
    t_z0 = at(1, "一个做错")
    t_huidao = at(1, "回到")
    t_tian = at(1, "天上")
    t_huan = at(1, "欢欢")
    t_qing = at(1, "庆祝")
    t_l2 = at(2, "耶稣和")
    t_zhexie = at(2, "这些人")
    t_chifan = at(2, "吃饭")
    t_muyang = at(2, "牧羊人")
    t_zhao = at(2, "去找")
    t_xiaoy = at(2, "小羊")
    t_l3 = at(3, "在上帝")
    t_mei = [at(3, "每一个人都是", k) for k in range(6)]
    t_bao = at(3, "宝贝")
    t_sd = at(3, "上帝一个")
    t_shiqu = at(3, "失去")
    t_end3 = ctx.lines[3].end

    add_set(sc, g0, "evening")
    add_gate_overlay(sc, "evening")
    add_front(sc, g0, "evening")
    add_sparrows(sc, g0)
    add_flyers(sc, g0, n=1)
    sc.add("sun", sunlight_svg("evening"), z=95, blend="screen", wc=0)
    sc.add("coins", coin_stack_svg(0, 1.0), z=61, seed=301)
    sc.add("lamps", [table_lamps_svg(k) for k in (0, 1)], z=62,
           frame_at=lambda t: 0.5 + 0.45 * math.sin(2 * math.pi * (t + g0) / 0.9) * math.sin(2 * math.pi * (t + g0) / 2.3))
    sc.fx.append(FX.tint((255, 200, 160), lambda t: 0.07, mode="multiply"))
    add_air(sc, g0, "evening")

    sto = STAND_Y - SEAT_Y
    start = {
        "jesus": ("open_hands", "warm", -1, 0, 0, sto),
        "tax0": ("listen", "kind", -1, 0, 0, 0), "tax1": ("listen", "kind", 1, 0, 0, 0),
        "tax2": ("listen", "kind", 1, 0, 0, 0), "woman": ("listen", "kind", 1, 0, 0, 0),
        "young": ("listen", "kind", 1, 0, 0, 0), "labourer": ("listen", "kind", 1, 0, 0, 0),
        "ph0": ("arms_folded", "ponder", -1, 0, 0, 0), "ph2": ("think", "ponder", -1, 0, 0, 0),
        "ph1": ("arms_folded", "stern", -1, 0, 0, 0),
    }
    acts = seated_actors(g0, start)
    jes = acts["jesus"]
    # ---------------------------------------------------------------- the page folds back into his hands
    t_f0, t_f1 = t_jwgs + 0.35, t_jwgs + 1.25            # unfold 1 -> 0 at the top
    t_d0, t_d1 = t_f1 - 0.05, t_shuo + 0.3                # floats down into the hands
    t_gone = t_d1 + 0.35
    jes.cut(t_d1 + 0.05, ("open_hands", "smile", -1, 0, 0, sto), depth=3)
    jes.cut(t_z0, ("tell", "smile", -1, 0, 0, sto))
    jes.cut(t_huidao, ("welcome", "smile", -1, 0, 0, sto))
    jes.cut(t_tian + 0.2, ("look_kind", "kind", 1, 0, 0, sto))
    jes.cut(t_huan, ("welcome", "laugh", 1, 0, 0, sto))
    jes.cut(t_qing + 0.5, ("tell", "smile", -1, 0, 0, sto))
    # '耶稣和这些人一起吃饭'
    jes.cut(t_l2 + 0.1, ("sit_look_kind", "kind", 1, 0, 0, 0), depth=10)
    jes.cut(t_zhexie, ("sit_offer", "warm", 1, 0, 0, 0))
    jes.cut(t_chifan + 0.35, ("sit_look_kind", "warm", 1, 0, 0, 0))
    jes.cut(t_mei[0] - 0.1, ("sit_welcome", "smile", -1, 0, 0, 0))
    jes.cut(t_sd + 0.1, ("sit_look_kind", "warm", 1, 0, 0, 0))
    jes.blinks(0.5, T - 1.0, rng)

    hands = hands_mid("open_hands", -1)
    inner = page_inner_night(0.0)
    sc.add("page_glow", page_glow_svg(), z=80, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=0.8 * (1 - M.progress(t, t_f0, t_f1, "sine"))))
    sc.add("book", page_frames(inner), z=81, frame_at=unfold_at(t_f0, t_f1, reverse=True),
           motion=book_motion(hands, 0, 0, 0, g0, fold=(t_d0, t_d1)))
    sc.fx.append(FX.sparkles((hands[0] - 70, hands[1] - 90, hands[0] + 70, hands[1] + 10), count=8, t0=t_d1 - 0.1,
                             t1=t_gone + 0.5, color=(255, 236, 170), size=(7, 14), period=1.0, drift=-24, seed=111))

    # ---------------------------------------------------------------- the guests
    order = ["labourer", "young", "woman", "tax2", "tax1", "tax0"]
    for i, who in enumerate(order):
        a = acts[who]
        f = -1 if who == "tax0" else 1
        tl = t_tian + 0.25 + 0.16 * i
        a.cut(tl, ("smile", "surprised", f, 0, 0, 0))
        a.cut(tl + 0.75, ("warm", "touched", f, 0, 0, 0))
        if who in ("young", "tax1", "labourer"):
            a.cut(t_huan + 0.2 + 0.1 * i, ("toast", "cheery", f, 0, 0, 0))
        elif who == "woman":
            a.cut(t_huan + 0.3, ("laugh", "laugh", f, 0, 0, 0))
        elif who == "tax2":
            a.cut(t_huan + 0.45, ("smile", "cheery", f, 0, 0, 0))
        if who == "tax0":
            a.cut(t_l2 + 0.2, ("listen", "kind", -1, 0, 0, 0))
            a.cut(t_chifan, ("sit_eat", "happy", -1, 0, 0, 0, (("item", "bread"),)))
            a.cut(t_xiaoy, ("warm", "touched", -1, 0, 0, 0))
        else:
            a.cut(t_l2 + 0.3 + 0.12 * i, ("smile" if i % 2 else "sit_eat", "happy", f, 0, 0, 0))
        a.cut(t_mei[i], ("warm", "touched", f, 0, 0, 0), depth=5)
        a.cut(t_sd + 0.5 + 0.1 * i, ("smile", "happy", f, 0, 0, 0))
        a.blinks(0.5, T - 1.0, rng)
    # ---------------------------------------------------------------- the Pharisees soften
    p0, p1, p2 = acts["ph0"], acts["ph1"], acts["ph2"]
    p0.cut(t_tian + 0.6, ("stand", "ponder", -1, 0, 0, 0))
    p2.cut(t_tian + 0.8, ("stand", "ponder", -1, 0, 0, 0))
    p0.cut(t_qing, ("arms_folded", "ponder", -1, 0, 0, 0))
    p1.cut(t_huan + 0.4, ("think", "ponder", -1, 0, 0, 0))
    p0.cut(t_muyang, ("look_at_each_other", "ponder", 1, 0, 0, 0))
    p2.cut(t_muyang + 0.2, ("look_at_each_other", "ponder", -1, 0, 0, 0))
    p0.cut(t_sd, ("think", "ponder", -1, 0, 0, 0))
    p0.cut(t_shiqu - 0.25, ("soften", "softened", -1, 0, 0, 0))
    p2.cut(t_shiqu, ("soften", "softened", -1, 0, 0, 0))
    p1.cut(t_shiqu + 0.3, ("stand", "ponder", -1, 0, 0, 0))
    for a in (p0, p1, p2):
        a.blinks(0.5, T - 1.0, rng)
    for a in acts.values():
        a.build(sc)

    # ---------------------------------------------------------------- heaven's joy: light only
    sc.add("rays", rays_svg(), z=93, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=env(t, t_tian - 0.1, t_l2 + 1.6, 0.9, 1.4) *
                               (0.85 + 0.15 * math.sin(2 * math.pi * (t + g0) / 3.1))))
    sc.fx.append(FX.sparkles((900, 40, 2800, 760), count=34, t0=t_tian, t1=t_l2 + 1.2, color=(255, 240, 190),
                             size=(7, 15), period=1.8, drift=26, seed=112))
    sc.fx.append(FX.sparkles((1000, 120, 2600, 620), count=18, t0=t_huan, t1=t_l2 + 0.8, color=(255, 250, 220),
                             size=(9, 18), period=1.1, drift=-14, seed=113))

    # ---------------------------------------------------------------- the round picture: the shepherd and the lamb
    bx, by, br = BUBBLE
    t_b0, t_b1 = t_muyang - 0.05, t_l3 + 0.5
    pop = lambda t0, piv: (lambda t: Tf(sx=max(0.001, M.progress(t, t0, t0 + 0.4, "back")),
                                        sy=max(0.001, M.progress(t, t0, t0 + 0.4, "back")), px=piv[0], py=piv[1],
                                        alpha=1 - M.progress(t, t_b1 - 0.5, t_b1, "sine")))
    dots = [(1812, 664, 8), (1822, 640, 12)]
    for i, (x, y, r) in enumerate(dots):
        sc.add(f"bub_dot{i}", bubble_dot_svg(x, y, r), z=84, motion=pop(t_b0 - 0.25 + 0.1 * i, (x, y)))
    sc.add("bubble", bubble_svg(), z=84.5, motion=M.combine(
        pop(t_b0, (bx, by + br)), lambda t: Tf(dy=4 * math.sin(2 * math.pi * (t + g0) / 2.8))))
    lamb_h = (bx - 40, by - 34)
    tax_h = C.body_points(C.tax_collector, SEATS["tax0"], SEAT_Y, K, -1, variant=0, pose="warm")["head"]
    for nm, (x, y), r, t0 in (("heart_lamb", lamb_h, 16, t_xiaoy), ("heart_tax", (tax_h[0] + 6, tax_h[1] - 78), 20,
                                                                    t_xiaoy + 0.12)):
        sc.add(nm, heart_svg(x, y, r), z=85,
               motion=lambda t, t0=t0, x=x, y=y: Tf(sx=max(0.001, M.progress(t, t0, t0 + 0.35, "back")),
                                                    sy=max(0.001, M.progress(t, t0, t0 + 0.35, "back")), px=x, py=y,
                                                    dy=-10 * M.progress(t, t0, t0 + 1.6),
                                                    alpha=1 - M.progress(t, t_b1 - 0.6, t_b1 - 0.1, "sine")))
    sc.fx.append(FX.sparkles((bx - br, by - br, bx + br, by + br), count=10, t0=t_b0 + 0.2, t1=t_b1, color=(255, 246, 210),
                             size=(6, 12), period=1.5, drift=-5, seed=114))

    # ---------------------------------------------------------------- every one a treasure: the warmth spreads
    sc.add("warm", warm_glow_svg(), z=92, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=0.55 * M.progress(t, t_l3, t_bao + 0.3, "sine") *
                               (1 - 0.35 * M.progress(t, t_bao + 0.6, T, "sine")),
                               sx=0.35 + 1.0 * M.progress(t, t_l3, t_bao + 0.4, "out"),
                               sy=0.35 + 1.0 * M.progress(t, t_l3, t_bao + 0.4, "out"), px=SEATS["jesus"], py=760))
    for i, who in enumerate(order):
        x = SEATS[who]
        f = -1 if who == "tax0" else 1
        head = C.body_points(C.tax_collector if who.startswith("tax") else C.sinner, x, SEAT_Y, K, f,
                             **({"variant": int(who[3])} if who.startswith("tax") else
                                {"kind": {"woman": "woman", "young": "young_man", "labourer": "labourer"}[who]}),
                             pose="warm")["head"]
        hx, hy = head[0] + 4 * f, head[1] - 80
        t0 = t_mei[i]
        sc.add(f"heart{i}", heart_svg(hx, hy, 17), z=86,
               motion=lambda t, t0=t0, hx=hx, hy=hy: Tf(
                   sx=max(0.001, M.progress(t, t0, t0 + 0.35, "back")), sy=max(0.001, M.progress(t, t0, t0 + 0.35, "back")),
                   px=hx, py=hy, dy=-26 * M.progress(t, t0, t0 + 2.4, "out"),
                   alpha=env(t, t0, t0 + 2.6, 0.05, 0.8)))
        sc.sfx("pop", t0, gain_db=-22, pan=-0.5 + 0.18 * i)
    # the light reaches the Pharisees
    sc.fx.append(FX.sparkles((2300, 520, 2800, 760), count=8, t0=t_sd + 0.2, t1=T + 1, color=(255, 236, 190),
                             size=(6, 11), period=1.9, drift=-6, seed=115))

    # ---------------------------------------------------------------- camera
    c_out = Cam(1820, 594, 2112)
    c_talk = Cam(1700, 720, 1640)
    c_sky = Cam(1760, 594, 2112)
    c_offer = Cam(1840, 694, 1340)
    c_all = Cam(1450, 740, 1350)
    c_soft = Cam(2050, 745, 1440)
    c_open = Cam(1790, 500, 1700)           # Jesus, the open page and the guests' faces above the subtitle band
    sc.camera = cam_seq([
        (0.0, c_open), (0.6, c_open), (t_shuo + 0.45, c_out), (t_shuo + 0.6, c_out), (t_z0 + 0.9, c_talk),
        (t_tian - 0.3, c_talk), (t_tian + 1.3, c_sky), (t_qing + 0.2, c_sky), (t_zhexie + 0.4, c_offer),
        (t_l3 - 0.2, c_offer), (t_mei[0] + 0.4, c_all), (t_sd - 0.1, c_all), (t_shiqu + 0.6, c_soft), (T, c_soft)])

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=T, gain_db=-28, fade_in=1.0, fade_out=1.0)
    sc.sfx("crowd", t_jwgs, dur=T - t_jwgs, gain_db=-31, fade_in=1.2, fade_out=1.0)
    sc.sfx("cloth", t_f0 + 0.1, gain_db=-19)
    sc.sfx("sparkle", t_d1, gain_db=-20)
    sc.sfx("chime", t_tian, gain_db=-15)
    sc.sfx("sparkle", t_huan + 0.1, gain_db=-18)
    sc.sfx("cloth", t_l2 + 0.1, gain_db=-23)
    sc.sfx("pop", t_b0, gain_db=-18)
    sc.sfx("sheep", t_xiaoy + 0.1, gain_db=-23, pan=0.3)
    sc.sfx("chime", t_l3 + 0.2, gain_db=-20)
    sc.sfx("sparkle", t_shiqu - 0.2, gain_db=-21, pan=0.5)
    return sc
