"""Scene 9 - Luke 19:9-10. The same dinner as s08_promise (a plain 1 s fade: the first second here is s08's last second
- same stage, layers, seeds, keys, camera and global-clock motion - without the gloss card, which fades out in the
dissolve). Jesus smiles and speaks with joy; salvation is light only: a warm glow spreads from Jesus, soft golden light
fills the room, Zacchaeus's face shines. Then a small round picture-book inset: Zacchaeus peeking from the sycamore-fig
while Jesus comes and looks up for him, and - iris-opening inside the same circle - the shepherd of the Lost Sheep film
carrying the little lamb home under the moon.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers through the Lost Sheep film's
Beats; nothing is hard-coded to the take). Times are for the current take:
  0 .. 1.0      the s08 end frame (calm, no cuts): Zacchaeus standing at the end of the table, hopeful (tender)
  '笑' 1.38      Jesus smiles (sit_smile); a warm glow spreads out from him (sparkle)
  '今天' 3.42    Jesus speaks with joy, arms open (sit_speak_joy); the camera draws in to him and Zacchaeus
  '救' 4.13      soft golden light fills the room (light only: a warm wash, brighter window beams, slow sparkles; chime);
                Zacchaeus is overjoyed, his face shines (a glow round his head); the disciples are awed
  '上帝救了撒该' 7.96  Zacchaeus bows to Jesus, grateful, a hand on his heart
  '撒该也是' 9.75  he straightens, eyes closed, smiling (grateful); on '上帝家里的人' 10.57 a warm glow rings him and a
                heart rises over him (sparkle); the disciples smile
  '我来' 12.65   Jesus raises his hand (sit_bless) and the camera draws back to the whole table; '就是要找到' 13.45 he
                speaks to everyone with open arms
  '撒该想看看耶稣' 17.65  the inset pops up above the table (pop): Zacchaeus in the tree; on '看看' 18.36 he peeks out,
                Jesus walks along the road below (planted-foot steps) and stops under the tree
  '也在找撒该' 20.59  Jesus looks up; on '撒该' 21.65 Zacchaeus beams
  '就像牧羊人' 22.69  the picture iris-opens into the moonlit hills: the shepherd carries the little lamb home (carry walk,
                planted feet), a lit window waits on the far hill
  '小羊' 25.05   the lamb nuzzles his cheek, a little heart (bleat)
  end           he stands still with the lamb; everyone at the table smiles: a calm last frame for the page turn
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
from stories.lost_sheep.scenes.s08_search import Beats, env, gfx
from stories.noah.scenes.s01_title import heart_markup, snap
from stories.zacchaeus.scenes.s08_promise import (CAM_GLOSS, FS, FY, H8, INK, W8, X_JESUS, X_ZSTAND, add_chest_shine,
                                                  add_people, add_set, cam_path, disc_key, doc, f1,
                                                  jesus_key, nod, pop_in, stepped, zac_key)

INSET = (884, 548, 196)              # the round picture: centre, radius (stage px)
S_TREE = 0.46                        # the tree picture's scale
S_SHEP = 0.6                         # the shepherd picture's scale
CAM_Z1 = Cam(1240, 848, 1300)
CAM_Z2 = Cam(1288, 852, 1262)
CAM_ALL = Cam(1110, 806, 1660)

# planted-foot walks (scale-1 advances measured from body_points)
JESUS_STEP = 87.0                                    # walk_a <-> walk_b
CARRY_FRAMES = ("carry_a", "carry_c", "carry_b", "carry_c")
CARRY_ADV = (29.0, 26.0, 59.0, 56.0)                 # advance INTO frame i of the cycle (a, c, b, c)


def clip_defs(cid="z9clip"):
    cx, cy, r = INSET
    return f'<clipPath id="{cid}"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}"/></clipPath>'


def idoc(body, defs=""):
    """A layer clipped to the inset circle."""
    return doc(f'<g clip-path="url(#z9clip)">{body}</g>', clip_defs() + defs)


# ------------------------------------------------------------------ picture 1: the tree
def tree_anchor():
    cx, cy, r = INSET
    return cx - 84, cy + 150


def tree_bg_svg():
    cx, cy, r = INSET
    tx, ty = tree_anchor()
    b = PR.jericho_sky(cx - r - 10, cy - r - 10, cx + r + 10, ty + 4, time=0.0, sun=(cx + 120, cy - 120), clouds=0.6,
                       seed=9, scale=0.5)
    sand = "#e8c48a"
    b += f'<rect x="{f1(cx - r - 10)}" y="{f1(ty - 30)}" width="{f1(2 * r + 20)}" height="{f1(cy + r - ty + 40)}" fill="{sand}"/>'
    b += S.path(S.hill(cx - r - 20, cx + r + 20, ty - 26, 26, seed=3, bottom=ty + 10), fill="#d9b277", sw=2.4)
    b += PR.date_palm(cx + 150, ty - 24, 0.2, 1, height=0.9, time=0.0, seed=3)
    b += PR.date_palm(cx - 190, ty - 22, 0.17, -1, height=0.8, time=0.0, seed=5)
    b += (f'<path d="M{f1(cx - r - 10)},{f1(ty + 2)} Q{f1(cx)},{f1(ty - 8)} {f1(cx + r + 10)},{f1(ty + 4)} '
          f'L{f1(cx + r + 10)},{f1(ty + 46)} Q{f1(cx)},{f1(ty + 36)} {f1(cx - r - 10)},{f1(ty + 48)} Z" fill="#d6a868" '
          f'stroke="{INK}" stroke-width="2.4" opacity="0.9"/>')
    b += PR.sycomore(tx, ty, S_TREE, 1, part="back", seed=2)
    return idoc(b)


def tree_front_svg():
    tx, ty = tree_anchor()
    return idoc(PR.sycomore(tx, ty, S_TREE, 1, part="front", seed=2))


def tree_actors_svg(zpose, zexpr, jx, jpose):
    """Zacchaeus in the tree and Jesus on the road under it (jx = Jesus' anchor x; None = not in the picture)."""
    tx, ty = tree_anchor()
    pts = PR.sycomore_points(tx, ty, S_TREE, 1)
    b = C.zacchaeus(*pts["sit"], S_TREE, 1, pose=zpose, expr=zexpr)
    if jx is not None:
        ux, uy = pts["under"]
        b += C.ground_shadow(jx, uy, S_TREE, width=100, opacity=0.18)
        b += C.jesus(jx, uy, S_TREE, -1, pose=jpose)
    return idoc(b)


# ------------------------------------------------------------------ picture 2: the shepherd under the moon
def night_frame_svg(x, pose, nuzzle=0.0):
    """The moonlit hills with the shepherd carrying the lamb home at anchor x (one baked frame)."""
    cx, cy, r = INSET
    gid = "z9night"
    defs = S.lin_grad(gid, [(0, "#2c3a6c"), (0.55, "#53609a"), (1, "#8f8cb8")])
    gy = cy + 128
    b = f'<rect x="{f1(cx - r - 10)}" y="{f1(cy - r - 10)}" width="{f1(2 * r + 20)}" height="{f1(2 * r + 20)}" fill="url(#{gid})"/>'
    mx, my = cx - 92, cy - 104
    b += PR._ls_glow(mx, my, 120, 120, 0.55, "z9moon", "#fffbe6", "#c8cce8")
    b += PR._circ(mx, my, 30, "#f6efd2", 3)
    b += PR._circ(mx + 11, my - 6, 6, "#e9e0bf", 0) + PR._circ(mx - 8, my + 9, 4, "#e9e0bf", 0)
    for i, (sx, sy, sr) in enumerate(((0.22, -0.62, 7), (0.5, -0.35, 6), (-0.05, -0.78, 5), (0.7, -0.05, 5),
                                      (-0.62, 0.02, 4), (0.32, -0.12, 4))):
        b += PR._twinkle(cx + r * sx, cy + r * sy, sr, "#fff6d0")
    b += S.path(S.hill(cx - r - 30, cx + r + 30, gy - 40, 60, seed=11, bottom=cy + r + 20), fill="#4c6b6a", sw=3)
    hx, hy = cx + 146, gy - 70
    b += (f'<path d="M{f1(hx - 22)},{f1(hy)} L{f1(hx - 22)},{f1(hy - 26)} L{f1(hx)},{f1(hy - 44)} L{f1(hx + 22)},{f1(hy - 26)} '
          f'L{f1(hx + 22)},{f1(hy)} Z" fill="#3e4d63" stroke="{INK}" stroke-width="2.4"/>'
          f'<rect x="{f1(hx - 6)}" y="{f1(hy - 20)}" width="12" height="12" fill="#ffd27a" stroke="{INK}" stroke-width="1.8"/>')
    b += PR._ls_glow(hx, hy - 14, 40, 34, 0.7, "z9win", "#fff2c4", "#f6b450")
    b += S.path(S.hill(cx - r - 30, cx + r + 30, gy + 8, 22, seed=4, bottom=cy + r + 20), fill="#5f8a74", sw=3)
    for k in range(7):
        gx = cx - r + 40 + k * 56
        b += f'<path d="M{f1(gx)},{f1(gy + 30 + (k % 3) * 9)} l-5,-12 m5,12 l1,-15 m-1,15 l6,-11" stroke="#3f6656" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    # the shepherd with the little lamb on his shoulders (lamb drawn in parts so it can nuzzle)
    tint = '<g filter="url(#z9nt)">'
    lp = C.shepherd_points(x, gy, S_SHEP, 1, pose=pose, lamb=False)["lamb"]
    lamb_back = PR.little_lamb(lp[0], lp[1], 1.1 * S_SHEP, 1, pose="on_shoulders", eyes="happy", time=1.0, part="back")
    lamb_front = PR.little_lamb(lp[0], lp[1], 1.1 * S_SHEP, 1, pose="on_shoulders", eyes="happy" if nuzzle < 0.5 else "closed",
                                time=1.0, part="front")
    if nuzzle:
        lamb_front = f'<g transform="rotate({-9 * nuzzle:.1f} {f1(lp[0])} {f1(lp[1])})">{lamb_front}</g>'
    b += C.ground_shadow(x, gy, S_SHEP, width=120, opacity=0.25)
    b += tint + lamb_back + C.parable_shepherd(x, gy, S_SHEP, 1, pose=pose, expr="joyful", lamb=False, crook=True) + \
        lamb_front + "</g>"
    ndefs = ('<filter id="z9nt" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
             '<feColorMatrix type="matrix" values="0.86 0 0 0 0  0 0.88 0 0 0  0 0 0.98 0 0  0 0 0 1 0"/></filter>')
    return idoc(b, defs + ndefs)


def ring_back_svg():
    cx, cy, r = INSET
    return doc(f'<circle cx="{f1(cx + 8)}" cy="{f1(cy + 12)}" r="{f1(r + 18)}" fill="#6a3a22" opacity="0.22" filter="url(#soft)"/>'
               f'<g filter="url(#wobble-fine)"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 16)}" fill="#fbf1dc" '
               f'stroke="{INK}" stroke-width="4"/></g>')


def ring_front_svg():
    cx, cy, r = INSET
    return doc(f'<g filter="url(#wobble-fine)"><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="none" stroke="{INK}" '
               f'stroke-width="3.5"/><circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r + 9)}" fill="none" stroke="#e2c79a" '
               f'stroke-width="2.2" stroke-dasharray="7 6"/></g>')


# ------------------------------------------------------------------ light
def glow_svg(x, y, rx, ry, gid, c0="#fff2c8", c1="#ffcf7a", a0=0.85, a1=0.35):
    return doc(f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>',
               S.rad_grad(gid, [(0, c0, a0), (0.45, c1, a1), (1, c1, 0)]))


def build(ctx):
    sc = Scene(ctx, W=W8, H=H8)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(9)

    # ---- beats
    t_xiao = bt.at(0, "笑")
    t_jt = bt.at(1, "今天")
    t_jiu = bt.at(1, "救恩")
    t_l1_end = bt.end(1, "救恩到了这一家")
    t_sd = bt.at(2, "上帝救了撒该")
    t_sjiu = bt.at(2, "救了")
    t_sg = bt.at(2, "撒该也是")
    t_jia = bt.at(2, "上帝家里的人")
    t_ren = bt.at(2, "家里的人", 3)
    t_l2_end = bt.end(2, "撒该也是上帝家里的人")
    t_wl = bt.at(3, "我来")
    t_zd = bt.at(3, "就是要找到")
    t_l3_end = bt.end(3, "把他们救回来")
    t_zx = bt.at(4, "撒该想看看耶稣")
    t_kk = bt.at(4, "看看")
    t_yl = bt.at(4, "原来耶稣")
    t_ye = bt.at(4, "也在找")
    t_zhao = bt.at(4, "找撒该")
    t_sg2 = bt.at(4, "撒该", 0, occ=1)
    t_jx = bt.at(4, "就像牧羊人")
    t_my = bt.at(4, "牧羊人")
    t_xy = bt.at(4, "小羊")
    t_l4_end = bt.end(4, "去找走丢的小羊")

    # ---- the set (the chest open, as at the end of s08)
    gold = lambda t: M.progress(t, t_jiu - 0.1, t_l1_end + 0.6, "inout") * (1 - 0.35 * M.progress(t, t_l2_end, t_zx, "inout"))
    add_set(sc, g0, None, (1.0,), beam_boost=gold)
    add_chest_shine(sc, g0, -10.0, T)

    # ---- the people (the first second = s08's last second)
    k_rest = zac_key("stand_speak", -1, "tender")
    t_joy = snap(t_jiu + 0.05)
    t_bow = snap(t_sjiu - 0.1)
    t_grat = snap(t_sg - 0.08)
    t_lis = snap(t_l2_end + 0.5)
    t_eag = snap(t_zx - 0.1)
    zac_ents = [(0, k_rest, False), (t_joy, zac_key("stand_speak", -1, "overjoyed"), True),
                (t_bow, zac_key("bow", -1, "grateful"), True), (t_grat, zac_key("stand_speak", -1, "grateful"), True),
                (t_lis, zac_key("stand_speak", -1, "happy"), False), (t_eag, zac_key("stand_speak", -1, "eager"), False)]
    t_sm = snap(max(1.1, t_xiao - 0.05))
    t_sj = snap(t_jt - 0.1)
    t_bl = snap(t_wl - 0.08)
    t_ow = snap(t_zd - 0.06)
    jesus_ents = [(0, jesus_key("sit_table"), False), (t_sm, jesus_key("sit_smile"), True),
                  (t_sj, jesus_key("sit_speak_joy"), True), (snap(t_l1_end + 0.35), jesus_key("sit_smile"), True),
                  (t_bl, jesus_key("sit_bless", "kind"), True), (t_ow, jesus_key("sit_speak_joy", "call_warm"), True),
                  (snap(t_l3_end + 0.4), jesus_key("sit_table"), True), (snap(t_xy - 0.3), jesus_key("sit_smile"), False)]
    jmots = [nod(t_ren + 0.15, FS, (X_JESUS, FY))]
    peter_ents = [(0, disc_key("peter", "happy"), False), (t_jiu + 0.35, disc_key("peter", "amazed"), True),
                  (t_jia + 0.25, disc_key("peter", "joyful"), True), (t_wl + 0.3, disc_key("peter", "happy"), False),
                  (t_zx + 0.4, disc_key("peter", "joyful"), False)]
    john_ents = [(0, disc_key("john", "kind"), False), (t_jiu + 0.5, disc_key("john", "touched"), False),
                 (t_jia + 0.4, disc_key("john", "happy"), True), (t_wl + 0.45, disc_key("john", "kind"), False),
                 (t_zx + 0.6, disc_key("john", "happy"), False)]
    add_people(sc, g0, rng, zac_ents, jesus_ents, peter_ents, john_ents, T - 1.1, blink_from=1.3,
               jesus_mots=jmots)

    # ---- light only: the warm glow from Jesus, the golden room, Zacchaeus's face, the ring and the heart
    # one warm light: it spreads out from Jesus on '笑' and fills the whole room on '救恩'
    jx, jy = X_JESUS + 40, FY - 230 * FS

    def light_m(t):
        k = 0.3 + 0.17 * M.progress(t, t_sm, t_sm + 1.8, "out") + 0.53 * M.progress(t, t_jiu - 0.1, t_l1_end + 0.5, "inout")
        a = (0.62 * M.progress(t, t_sm, t_sm + 1.2, "sine") * (1 - 0.45 * gold(t)) + 0.36 * gold(t))
        return Tf(alpha=a * (0.92 + 0.08 * math.sin(2 * math.pi * (t + g0) / 3.7)), sx=k, sy=k, px=jx, py=jy)
    sc.add("warm_light", glow_svg(jx, jy, 1400, 1000, "z9light", "#fff2c8", "#ffd27e", 0.8, 0.32), z=2.8, wc=0,
           blend="screen", motion=light_m)
    sc.fx.append(gfx(FX.sparkles, g0, t0=t_jiu, t1=t_zx - 0.2, rect=(420, 380, 1880, 900), count=22,
                     color=(255, 236, 170), size=(7, 14), period=1.9, drift=-10, seed=91))
    zx, zy = X_ZSTAND - 8, FY - 252 * FS
    sc.add("zac_face", glow_svg(zx, zy, 170, 170, "z9zf", "#fff6d8", "#ffe09a", 0.9, 0.4), z=3.7, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.7 * env(t, t_joy, 1e9, 0.6) * (0.8 + 0.2 * math.sin(2 * math.pi * (t + g0) / 1.9))))
    t_rg = snap(t_jia + 0.1)
    rgx, rgy = X_ZSTAND - 6, FY - 150 * FS
    sc.add("zac_glow", glow_svg(rgx, rgy, 250, 300, "z9zg", "#fff4cc", "#ffd88a", 0.75, 0.35), z=3.5, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.8 * env(t, t_rg, t_zx + 0.4, 0.5, 1.2) * (0.85 + 0.15 * math.sin(2 * math.pi * (t + g0) / 1.6)),
                               sx=0.7 + 0.3 * M.progress(t, t_rg, t_rg + 0.9, "out"),
                               sy=0.7 + 0.3 * M.progress(t, t_rg, t_rg + 0.9, "out"), px=rgx, py=rgy))
    hx, hy = X_ZSTAND - 10, FY - 330 * FS
    t_ht = snap(t_ren - 0.05)

    def heart_m(t):
        if t < t_ht:
            return Tf(alpha=0.0)
        s = 0.4 + 0.6 * M.progress(t, t_ht, t_ht + 0.35, "back")
        a = M.progress(t, t_ht, t_ht + 0.15, "sine") * (1 - M.progress(t, t_ht + 1.6, t_ht + 2.3, "sine"))
        return Tf(dy=-70 * M.progress(t, t_ht, t_ht + 2.3, "out"), dx=5 * math.sin(2 * math.pi * (t - t_ht) / 1.2),
                  sx=s, sy=s, px=hx, py=hy, alpha=a)
    sc.add("zac_heart", doc(heart_markup(hx, hy, 30, fill="#ef8f9a")), z=12, wc=0, motion=heart_m)

    # ---- the inset
    cx, cy, r = INSET
    t_in = snap(t_zx - 0.06)
    pin = pop_in(t_in, (cx, cy), dur=0.36, s0=0.5)
    sc.add("ring_back", ring_back_svg(), z=30, motion=pin, seed=61)
    sc.add("tree_bg", tree_bg_svg(), z=30.2, motion=pin, seed=62)
    # actors: Zacchaeus sit_branch -> peek ('看看') -> beaming ('撒该'); Jesus walks in from the right and looks up
    tx, ty = tree_anchor()
    ux = PR.sycomore_points(tx, ty, S_TREE, 1)["under"][0]
    t_kk_c = snap(t_kk - 0.06)
    n_steps = 6
    t_w0 = t_in + 0.12
    t_stop = snap(min(t_yl - 0.05, t_w0 + 0.32 * n_steps + 0.05))
    per = (t_stop - t_w0) / n_steps
    step_t = [snap(t_w0 + per * i) for i in range(n_steps)]
    t_lu = snap(t_ye - 0.06)
    t_beam = snap(t_sg2 - 0.06)
    states = []                                       # (t, zpose, zexpr, jx, jpose)
    zp, ze = "sit_branch", "eager"
    ux_w = ux + 28.5 * S_TREE                        # the last walk anchor: stopping keeps the front foot planted
    states.append((0.0, zp, ze, ux_w + JESUS_STEP * S_TREE * n_steps, "walk_a"))
    for i, ts in enumerate(step_t):
        states.append((ts, None, None, ux_w + JESUS_STEP * S_TREE * (n_steps - 1 - i), "walk_b" if i % 2 == 0 else "walk_a"))
    states.append((t_stop, None, None, ux, "stand"))
    states.append((t_kk_c, "peek", "eager", None, None))
    states.append((t_lu, None, None, None, "look_up"))
    states.append((t_beam, "peek", "overjoyed", None, None))
    states.sort(key=lambda s_: s_[0])
    frames, idx, ents, cur = [], {}, [], [None, None, None, None]
    for ts, zp_, ze_, jx_, jp_ in states:
        if zp_ is not None:
            cur[0], cur[1] = zp_, ze_
        if jx_ is not None:
            cur[2] = jx_
        if jp_ is not None:
            cur[3] = jp_
        key = tuple(cur)
        if key not in idx:
            idx[key] = len(frames)
            frames.append(tree_actors_svg(*key))
        ents.append((ts, idx[key]))
    sc.add("tree_actors", frames, z=30.4, frame_at=stepped([e[0] for e in ents], [e[1] for e in ents]), motion=pin,
           seed=63)
    sc.add("tree_front", tree_front_svg(), z=30.6, motion=pin, seed=64)
    # picture 2: the shepherd carrying the lamb home, iris-opening inside the circle on '就像'
    t_r0 = snap(t_jx - 0.04)
    t_r1 = t_r0 + 0.65
    n_walk = 7
    t_s0 = t_r0 + 0.1
    t_s1 = snap(min(t_xy - 0.3, T - 1.8))
    wper = (t_s1 - t_s0) / n_walk
    x0 = cx - 150
    xs = [x0]
    for i in range(n_walk):
        xs.append(xs[-1] + CARRY_ADV[(i + 1) % 4] * S_SHEP)
    sh_frames, sh_ents = [], []
    sh_frames.append(night_frame_svg(xs[0], CARRY_FRAMES[0]))
    sh_ents.append((0.0, 0))
    for i in range(1, n_walk + 1):
        sh_frames.append(night_frame_svg(xs[i], CARRY_FRAMES[i % 4]))
        sh_ents.append((snap(t_s0 + wper * i), len(sh_frames) - 1))
    t_st = snap(t_s1 + 0.24)
    sh_frames.append(night_frame_svg(xs[-1], "carry_stand"))
    sh_ents.append((t_st, len(sh_frames) - 1))
    t_nz = snap(max(t_xy + 0.05, t_st + 0.12))
    sh_frames.append(night_frame_svg(xs[-1], "carry_stand", nuzzle=1.0))
    sh_ents.append((t_nz, len(sh_frames) - 1))
    sh_frames.append(night_frame_svg(xs[-1], "carry_stand", nuzzle=0.4))
    sh_ents.append((snap(min(t_nz + 0.55, T - 1.1)), len(sh_frames) - 1))

    def iris(t):
        # the crop is the circle's box, so frac ~.76 already covers the whole picture (radius + soft edge)
        f = 0.8 * M.progress(t, t_r0, t_r1, "sine") + (0.25 if t > t_r1 else 0.0)
        return {"mode": "radial", "frac": f, "soft": 26, "cx": cx, "cy": cy}
    sc.add("night", sh_frames, z=31.0, frame_at=stepped([e[0] for e in sh_ents], [e[1] for e in sh_ents]),
           reveal=iris, motion=lambda t: Tf(alpha=1.0 if t >= t_r0 - 0.01 else 0.0), seed=65)
    hx2, hy2 = xs[-1] + 40, cy + 128 - 330 * S_SHEP
    t_h2 = snap(t_nz + 0.1)

    def heart2(t):
        if t < t_h2:
            return Tf(alpha=0.0)
        s = 0.4 + 0.6 * M.progress(t, t_h2, t_h2 + 0.3, "back")
        a = M.progress(t, t_h2, t_h2 + 0.15, "sine") * (1 - M.progress(t, t_h2 + 1.1, t_h2 + 1.6, "sine"))
        return Tf(dy=-36 * M.progress(t, t_h2, t_h2 + 1.6, "out"), sx=s, sy=s, px=hx2, py=hy2, alpha=a)
    sc.add("lamb_heart", idoc(heart_markup(hx2, hy2, 14, fill="#ef8f9a")), z=31.2, wc=0, motion=heart2)
    sc.add("ring_front", ring_front_svg(), z=31.9, motion=pin, seed=66)
    sc.fx.append(gfx(FX.sparkles, g0, t0=t_r1, t1=T + 2, rect=(cx - 150, cy - 170, cx + 160, cy - 40), count=6,
                     color=(255, 246, 210), size=(5, 9), period=2.1, drift=0, seed=95))

    # ---- camera
    sc.camera = cam_path([(0.0, CAM_GLOSS), (t_sm, CAM_GLOSS), (t_jiu, CAM_Z1), (t_sg, CAM_Z1), (t_l2_end, CAM_Z2),
                          (t_wl, CAM_Z2), (t_zd + 0.9, CAM_ALL), (T, CAM_ALL)],
                         ["linear", "inout", "linear", "inout", "linear", "inout", "linear"])

    # ---- sound
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-28, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0, dur=T + 0.5, gain_db=-31, fade_in=0.8, fade_out=1.0)
    sc.sfx("sparkle", t_sm + 0.05, gain_db=-21, pan=-0.1)
    sc.sfx("chime", t_jiu, gain_db=-14)
    sc.sfx("cloth", t_bow, gain_db=-21, pan=0.4)
    sc.sfx("sparkle", t_ht, gain_db=-17, pan=0.4)
    sc.sfx("pop", t_in, gain_db=-19, pan=-0.2)
    sc.sfx("footsteps", step_t[0], dur=t_stop - step_t[0], gain_db=-30, pan=-0.1)
    sc.sfx("sparkle", t_r0, gain_db=-20, pan=-0.2)
    sc.sfx("night", t_r0, dur=T - t_r0 + 0.5, gain_db=-30, fade_in=0.6, fade_out=1.0)
    sc.sfx("sheep", t_nz, gain_db=-24, pan=-0.1, pitch=1.3)
    return sc
