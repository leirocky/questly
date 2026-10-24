"""Scene 8 - John 6:12-14. Dusk on the same hillside (time 0.8 -> 1): everyone has eaten their fill - children pat full
tummies, a father leans back laughing; Jesus tells the disciples to gather the leftover pieces so that nothing is
wasted; the disciples stoop over their baskets and pick up the pieces on every 收, the baskets filling .25 -> 1; cut to
twelve full baskets in one long row with the twelve standing behind them - a picture-book count pops 1 .. 12 over the
baskets; a gloss card: the boy's one little basket (5 loaves) against twelve big full baskets; amazement (the
disciples' hands at their cheeks, the boy's eyes wide, his family jumping up); the people cheer and point to Jesus;
the boy looks at the full baskets and smiles.

The lake_hillside world of s05 (same stage, seed, rock and slope), now at dusk; the crowd sits in its colourful groups
(galilee_groups on lake_hillside_points()['groups']). The neighbours are page-turn dips: calm first / last frames.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's
beat(); nothing hard-coded to the take). Times are for the current take:
  0 .. 0.9      the boy's family on the grass in the dusk light (the baby asleep), the groups behind
  '每个人' 0.94  the children pat their full tummies (sit_pat_tummy loops), the father leans back laughing, the boy
                pats his tummy; '饱饱' a contented sigh (bob)
  ~3.05         hard cut (phrase boundary) to Jesus with Peter, Andrew and John, holding their empty baskets
  '把剩下' 5.47  Jesus speaks, an open hand toward the leftover pieces lying on the grass; '收起来' the three nod;
                '浪费' they turn to go
  ~9.95         hard cut to the far side of the slope: Andrew, John, James and Philip stooping over their baskets
  '门徒们'       a first piece each; every '收' (x5) a piece picked from the grass (the pile shrinks) and dropped into
                the basket, which fills .25 -> .5 -> .75 -> 1
  ~14.05        hard cut: twelve full baskets in a row, the twelve standing proudly behind them, Jesus on the left,
                the boy on the right
  '装满了十二个篮子'  a count bubble pops over each basket in turn, 1 .. 12, each basket giving a little hop
  '比' 16.33     a gloss card: the boy's little basket with five loaves ('5') ... '还多得多' twelve big baskets ('12')
  '大家都好惊讶'  the twelve put their hands to their cheeks, the boy's eyes go wide, his parents jump up amazed
  '大家都说' 25.98  the camera pulls back over the hillside: the groups cheer (arms up), the twelve wave; '耶稣一定'
                the boy's father and three people further up point to Jesus, his mother cheers; a soft warm glow
                round Jesus (light only)
  '小男孩' 29.88  the boy steps over to the end of the row (the camera pushes in slowly): '看' he looks at the full
                baskets, eyes wide; '笑' he smiles
  end           calm: the boy smiling at the full baskets in the dusk glow
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
from stories.loaves.scenes.s05_boy import (
    CLOUDS, FAR_Y, H5, K, LAKE_Y, LSEED, PTS, ROCK_X, W5, YF, YG, Fig, arrow_svg, beat, bk, breath, bump, card_svg,
    cut_cam, dk, doc, f1, fk, haze_filter, jk, nod, pop_in, snap, squash, syl, zoom_cam)

INK = S.P["ink"]
T0, T1 = 0.8, 1.0                          # dusk: time of day at the start / end of the scene
TIMES = (0.8, 0.9, 1.0)                     # backdrop drawings, cross-faded
SUN8 = (3050, 360)

XJ8 = 560                                  # Jesus (beside the teaching rock)
ROW = (1180, 1086, 0.55)                   # the twelve baskets: centre x, ground y, scale (one long row)
GAP = 150
XBOY = 1790                                # the boy, just right of the row
FAMILY = [  # kind, variant, x, y, pose, facing - the boy's family (his mother from s05)
    ("mother", 7, 1965, 1046, "sit", -1), ("child", 13, 2070, 1064, "sit_pat_tummy", -1),
    ("child", 8, 2160, 1050, "sit_pat_tummy", -1), ("man", 7, 2265, 1060, "sit_laugh", -1)]
GATHER = [  # variant, x, y - the four gathering on the far side
    ("andrew", 2440, 1004), ("john", 2700, 1020), ("james", 2960, 1000), ("philip", 3215, 1016)]
DROP_GROUPS = ((724, 890), (1781, 890), (2942, 890), (1170, 774))    # left out: the heroes need the front of the slope

Z_SKY, Z_BG, Z_GLINT, Z_GROUPS, Z_PIECES, Z_ROW_PEOPLE, Z_ROW, Z_PEOPLE, Z_NUM, Z_GLOSS, Z_FG, Z_TINT = (
    0, 1, 1.5, 3, 4, 5, 5.5, 7, 9, 10, 11, 12)


def tod_of(T):
    return lambda t: T0 + (T1 - T0) * M.progress(t, 0.0, T, "linear")


def frame_of_time(tod):
    """Fractional backdrop drawing index for the time of day (the TIMES drawings cross-fade)."""
    def fa(t):
        v = (tod(t) - TIMES[0]) / (TIMES[1] - TIMES[0])
        return min(max(v, 0.0), len(TIMES) - 1.0)
    return fa


# ================================================================== the world at dusk
def bg_svg(time):
    """Sky, sun, the far shore and lake, the slope (one drawing per time of day)."""
    body = PR.galilee_sky(0, 0, W5, FAR_Y + 140, time=time, sun=SUN8, clouds=0, birds=0, seed=LSEED, scale=1.0)
    body += PR.lake_hillside(0, W5, YF, 1.0, time=time, part="back", seed=LSEED, rock_x=ROCK_X, bottom=H5 + 30)
    body += PR.far_boat(2560, LAKE_Y - 16, 0.13, -1, sail="furled", crew=False, time=time)
    body += PR.lake_hillside(0, W5, YF, 1.0, time=time, part="mid", seed=LSEED, rock_x=ROCK_X, bottom=H5 + 30)
    return doc(body)


def clouds8_svg(time, i):
    cx, cy, w, h, seed, v = CLOUDS[i]
    pal = PR._lf_pal(time)
    return doc(f'<g opacity="0.9">{PR._lf_cloud(cx, cy - 20, w, h, pal, seed, rim_k=1.0)}</g>')


def glints8_svg(time, which):
    rng = random.Random(80 + which)
    col = PR._lf_pal(time)["glit"]
    out = ""
    for _ in range(30):
        x = rng.uniform(60, W5 * 0.70)
        y = rng.uniform(FAR_Y + 30, LAKE_Y - 12)
        w = rng.uniform(10, 28) * (0.6 + 0.6 * (y - FAR_Y) / (LAKE_Y - FAR_Y))
        out += (f'<path d="M{f1(x - w)},{f1(y)} Q{f1(x)},{f1(y - 3)} {f1(x + w)},{f1(y)}" stroke="{col}" stroke-width="3" '
                f'stroke-linecap="round" fill="none" opacity="0.9"/>')
    return doc(out)


def front8_svg(time, side):
    full = PR.lake_hillside(0, W5, YF, 1.0, time=time, part="front", seed=LSEED, bottom=H5 + 30)
    x0 = 0 if side == 0 else W5 - 560
    cid = f"lf8front{side}"
    return doc(f'<clipPath id="{cid}"><rect x="{x0}" y="0" width="560" height="{H5}"/></clipPath>'
               f'<g clip-path="url(#{cid})">{full}</g>')


def fg8_svg(time, seed):
    pal = PR._lf_pal(time)
    g = pal["grass"]
    out = PR._lf_grass(0, W5, 1100, 1180, int(26 * 0.6 * W5 / 1000), seed, (pal["grass_dk"], g[2]), 1.25, 0.8, 1.3)
    out += PR._lf_flowers(0, W5, 1110, 1180, 1.0, seed + 1, time, 1.2)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def groups_rows():
    rows = {}
    for (x, y, k) in PTS["groups"]:
        if any(abs(x - dx) < 5 and abs(y - dy) < 5 for dx, dy in DROP_GROUPS):
            continue
        rows.setdefault(round(y), []).append((x, y, k))
    return [rows[y] for y in sorted(rows)]


def groups_svg(groups, pose, time, seed):
    y = groups[0][1]
    d = (YF - y) / (YF - LAKE_Y)
    fid = f"lf8hz{seed}"
    body = C.galilee_groups(0, W5, 0, 0, 1.0, groups=groups, pose=pose, seed=seed, focus=XJ8, per_group=(12, 7))
    return doc(f'<g filter="url(#{fid})">{body}</g>', defs=haze_filter(fid, 0.22 * d, time))


def tint_svg(strength=1.0):
    """The rose-violet dusk over the whole picture (multiplied): it deepens as the sun sets."""
    gid = "lf8tint"
    return doc(f'<rect x="-20" y="-20" width="{W5 + 40}" height="{H5 + 40}" fill="url(#{gid})"/>',
               defs=S.lin_grad(gid, [(0, "#b49ac4"), (0.55, "#e8b8b0"), (1, "#d8a8b4")]))


def glow8_svg(time):
    pal = PR._lf_pal(time)
    gid = "lf8glow"
    return doc(f'<rect x="-20" y="-20" width="{W5 + 40}" height="{H5 + 40}" fill="url(#{gid})"/>',
               defs=S.rad_grad(gid, [(0, pal["sun_halo"], 0.30), (0.4, pal["sun_halo"], 0.12), (1, pal["sun_halo"], 0)],
                               cx=SUN8[0] / W5, cy=SUN8[1] / H5, r=0.8))


def add_world8(sc, g0, tod, T):
    fa = frame_of_time(tod)
    sc.add("bg", [bg_svg(tm) for tm in TIMES], z=Z_BG, frame_at=fa)
    for i in range(len(CLOUDS)):
        v = CLOUDS[i][5]
        sc.add(f"cloud{i}", [clouds8_svg(tm, i) for tm in TIMES], z=Z_BG + 0.1 + 0.01 * i, wc=0.8, frame_at=fa,
               motion=lambda t, v=v: Tf(dx=v * (t + g0 - 180.0)))
    for w_ in (0, 1):
        sc.add(f"glint{w_}", glints8_svg(0.9, w_), z=Z_GLINT + 0.01 * w_, wc=0,
               motion=lambda t, w_=w_: Tf(alpha=0.15 + 0.85 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t + g0) / 2.6 + 0.5 * w_)))))
    for side in (0, 1):
        px = 200 if side == 0 else W5 - 200
        sc.add(f"front{side}", front8_svg(0.9, side), z=Z_FG + 0.01 * side,
               motion=lambda t, px=px, side=side: Tf(rot=0.9 * math.sin(2 * math.pi * ((t + g0) / 3.4 + 0.3 * side)),
                                                       px=px, py=H5 + 40))
    for j in range(2):
        sc.add(f"fg{j}", fg8_svg(0.9, 620 + 7 * j), z=Z_FG - 0.5 + 0.01 * j,
               motion=lambda t, j=j: Tf(dx=2.2 * math.sin(2 * math.pi * ((t + g0) / 2.9 + 0.5 * j))))
    sc.add("glow", glow8_svg(0.9), z=Z_TINT - 0.5, wc=0)
    sc.add("tint", tint_svg(), z=Z_TINT, wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=0.10 + 0.14 * (tod(t) - T0) / (T1 - T0)))


# ================================================================== the gathering (a deeper stoop than 'gather')
BASKET_AT = (150, -2)                      # the basket on the grass, local (anchor = his feet), scale .52
MOUTH = (132, -78)                         # the near hand over the basket mouth
PICKS = [(84, -12), (104, -6), (66, -8), (114, -16), (92, -2), (72, -18)]     # pieces on the grass (local)
PIECE_STYLE = [(20, 0), (-35, 3), (62, 5), (6, 7), (-18, 9), (44, 11)]          # their rotation and drawing seed


def gather_fn(x, y, scale=1.0, facing=1, variant="john", e=1.0, target=PICKS[0], fill=0.0, holding=False,
              piece=PIECE_STYLE[0]):
    """A disciple stooping over his basket on the grass: e = 0 the near hand down on the piece at target, 1 over the
    basket mouth; holding draws a piece in that hand; fill the basket. (characters.disciples 'gather' never brings the
    hand down to the grass, so the hand reach and the stoop are deeper here.)"""
    vi = C._disciple_index(4 if variant == "philip" else variant)
    D, m = C._disciple_design(vi, 0.0, False)
    hx = M.lerp(target[0], MOUTH[0], e)
    hy = M.lerp(target[1], MOUTH[1], e) - 18 * math.sin(math.pi * e)
    ps = C._P(t=56 - 8 * e, h=-6 + 4 * (1 - e), drop=46, legs=(("ik", 44, 1), ("ik", -34, 1)),
              arms=(("ik", "abs", 116, -66, 1), ("ik", "abs", hx, hy, 1)), hands=("fist", "fist"), expr="happy",
              look=(0.04, 0.07), reach=1.12)

    def front(st):
        PR_ = C._prp()
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        G = st["ground"]
        s = C._lf_held(st, PR_._wicker_basket(fill, "mixed", time=0.9, seed=9), (BASKET_AT[0], G + BASKET_AT[1]), 0, 0.52)
        s += C._fist(W0, hr, D["skin"])
        if holding:
            s += C._lf_held(st, PR_._barley_loaf("piece", 0.9, seed=piece[1]), (W1[0] + 6, W1[1] + 6), piece[0], 1.1)
        s += C._fist(W1, hr, D["skin"])
        return s
    D["front"] = C._hooks(front)
    inner, _ = C._figure(D, m, ps, "happy", C._fsign(facing), True)
    return C._wrap_out(inner, x, y, scale, facing, f"lf8-gather{vi}")


def piece_at_hand(x, y, k, variant, target, piece):
    """The piece lying on the grass exactly where the hand will hold it at e = 0 (the same transform chain)."""
    (_, _), (hx, hy) = C.hand_positions(gather_fn, x, y, k, 1, variant=variant, e=0.0, target=target, holding=True)
    lx, ly = (hx - x) / k, (hy - y) / k
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5g},{k:.5g})"><g filter="url(#wobble-fine)">'
            f'<g transform="translate({lx + 6:.1f},{ly + 6:.1f}) rotate({piece[0]}) scale(1.1)">'
            f'{PR._barley_loaf("piece", 0.9, seed=piece[1])}</g>'
            f'<ellipse cx="{lx + 8:.1f}" cy="{ly + 16:.1f}" rx="11" ry="3" fill="#2a3048" opacity="0.18"/></g></g>')


# ================================================================== the count and the gloss
def row_basket_xs(x, scale, n=12, gap=GAP):
    return [x + (j - (n - 1) / 2) * gap * scale for j in range(n)]


def row_svg(x, y, s, time, fill=1.0, only=None):
    """The twelve baskets in one long row (props.baskets_row rows=1), or only the basket of index only (its own
    layer: it hops when it is counted)."""
    if only is None:
        return doc(PR.baskets_row(x, y, s, n=12, fill=fill, gap=GAP, rows=1, time=time, seed=0))
    px = row_basket_xs(x, s)[only]
    return doc(PR.wicker_basket(px, y, s, 1 if only % 2 else -1, fill=fill, time=time, seed=3 * only))


def number_svg(x, y, n, k=0.62, color="#e8705a"):
    return doc(PR.count_bubble(x, y, n, k, pop=1.0, color=color))


def label_svg(x, y, txt, size=46, col="#8a4a2a"):
    return doc(f'<text x="{f1(x)}" y="{f1(y)}" font-family="LXGW WenKai" font-weight="bold" font-size="{size}" fill="{col}" '
               f'text-anchor="middle">{txt}</text>')


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(8)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731
    L = ctx.lines
    tod = tod_of(T)

    # ---------------------------------------------------------------- beats
    t_bao = syl(ctx, 0, "饱饱")
    t_ys = b(0, "耶稣对门徒说")
    t_ba = b(1, "把剩下")
    t_shou_l1 = b(1, "收起来")
    t_lf = b(1, "浪费")
    t_l1e = L[1].end
    t_mt = b(2, "门徒们")
    t_shou = [b(2, "收", k) for k in range(5)]
    t_zm = b(2, "装满了")
    t_count = syl(ctx, 2, "装满了十二个篮子")
    t_bi = b(2, "比原来")
    t_wb = b(2, "五个饼")
    t_hd = b(2, "还多得多")
    t_jy = b(3, "大家都好惊讶")
    t_djs = b(4, "大家都说")
    t_ys4 = b(4, "耶稣一定")
    t_xnh = b(4, "小男孩")
    t_kan = b(4, "看着")
    t_xiao = b(4, "笑了")
    t_cut1 = snap(t_ys - 0.12)                     # S1 -> S2 (the family -> Jesus)
    t_cut2 = snap((t_l1e + L[2].start) / 2)        # S2 -> S3 (the gathering)
    t_cut3 = snap(t_zm - 0.13)                     # S3 -> S4 (the twelve baskets)

    def during(a, z=1e9):
        return lambda t: 1.0 if a <= t < z else 0.0

    # ---------------------------------------------------------------- the world and the seated crowd
    add_world8(sc, g0, tod, T)
    t_cheer = snap(t_djs + 0.1)
    for r, grp in enumerate(groups_rows()):
        y = grp[0][1]
        piv = (W5 / 2, y)
        frames = [groups_svg(grp, "sit_pat_tummy", 0.9, 40 + r), groups_svg(grp, "cheer", 0.9, 40 + r)]
        sc.add(f"groups{r}", frames, z=Z_GROUPS + 0.01 * r, seed=500 + r,
               frame_at=lambda t: 0.0 if t < t_cheer else 1.0,
               motion=M.combine(breath(piv, g0, 3.4 + 0.3 * r, 0.004, 0.2 * r), bump(t_cheer + 0.02 * r, 1.0, piv, 5, 0.3)))

    # leftover pieces on the grass (S1 / S2: gathered before the baskets are shown)
    left_pieces = [(1110, 1076, 5, 1), (1300, 1058, 6, 2), (1480, 1088, 5, 3), (1640, 1050, 4, 4), (1250, 1110, 4, 5),
                   (2560, 1080, 5, 6), (2830, 1096, 4, 7), (3080, 1082, 5, 8), (3330, 1094, 4, 9)]
    sc.add("pieces_near", doc("".join(PR.bread_pieces(x, y, 1.25, n=n, spread=110, time=0.9, seed=s)
                                      for x, y, n, s in left_pieces[:5])),
           z=Z_PIECES, motion=lambda t: Tf(alpha=1.0 if t < t_cut3 else 0.0))
    sc.add("pieces_far", doc("".join(PR.bread_pieces(x, y, 0.95, n=n, spread=120, time=0.9, seed=s)
                                     for x, y, n, s in left_pieces[5:])), z=Z_PIECES)

    # ---------------------------------------------------------------- the boy's family (S1, then beside the baskets)
    fam = []
    for i, (kind, v, x, y, pose, f) in enumerate(FAMILY):
        loops = {}
        if pose == "sit_pat_tummy":
            key = fk(kind, v, pose, f, "yum")
            loops[key] = (4, 0.15)
        ff = Fig(f"fam{i}", (x, y), Z_PEOPLE - 0.3 + 0.01 * i, g0, k=K * 0.97, seed=60 + i, shadow=150, loops=loops,
                 draw=lambda key, j=0, x=x, y=y: C.galilee_folk(x, y, K * 0.97, key[4], kind=key[1], variant=key[2],
                                                                 pose=key[3], expr=key[5], phase=j / 4 if key[3] in (
                                                                     "sit_pat_tummy", "pat_tummy", "wave") else key[6],
                                                                 food=key[7]))
        e0 = {"sit": "kind", "sit_pat_tummy": "yum", "sit_laugh": "laugh"}[pose]
        ff.cut(0, fk(kind, v, pose, f, e0))
        ff.mots.append(breath((x, y), g0, 2.8 + 0.3 * i, 0.012, 0.25 * i))
        fam.append(ff)
    fam[3].mots.append(bump(t_bao[0], K, FAMILY[3][2:4], 6, 0.4))
    # amazed: the parents jump up; then cheering and pointing to Jesus
    t_amaze = snap(t_jy + 0.1)
    fam[0].cut(t_amaze + 0.12, fk("mother", 7, "amazed", -1, "amazed"), depth=9)
    fam[0].mots.append(bump(t_amaze + 0.14, K, FAMILY[0][2:4], 16, 0.32))
    fam[3].cut(t_amaze, fk("man", 7, "amazed", -1, "amazed"), depth=9)
    fam[3].mots.append(bump(t_amaze + 0.02, K, FAMILY[3][2:4], 18, 0.32))
    fam[1].cut(t_amaze + 0.2, fk("child", 13, "sit_laugh", -1, "surprised"), depth=6)
    fam[2].cut(t_amaze + 0.26, fk("child", 8, "sit_laugh", -1, "surprised"), depth=6)
    fam[3].cut(t_ys4 - 0.05, fk("man", 7, "point", -1, "joyful"), depth=6)
    fam[0].cut(t_ys4 + 0.05, fk("mother", 7, "cheer", -1, "joyful"), depth=6)
    fam[1].cut(t_cheer + 0.1, fk("child", 13, "sit_laugh", -1, "laugh"), depth=5)
    fam[2].cut(t_cheer + 0.15, fk("child", 8, "sit_laugh", -1, "laugh"), depth=5)
    fam[3].cut(snap(t_xnh - 0.2), fk("man", 7, "stand", -1, "happy"), depth=5)
    fam[0].cut(snap(t_xnh - 0.1), fk("mother", 7, "stand", -1, "happy"), depth=5)

    # three people further up who jump up amazed and then point to Jesus
    for i, (kind, v, x, y, p0, p2) in enumerate((("man", 9, 2085, 905, "sit_laugh", "point"),
                                                  ("woman", 16, 2205, 916, "sit_pat_tummy", "cheer"),
                                                  ("elder", 5, 2322, 900, "sit", "point"))):
        k_ = K * 0.86
        loops = {fk(kind, v, "sit_pat_tummy", -1, "yum"): (4, 0.17)} if p0 == "sit_pat_tummy" else {}
        pfig = Fig(f"praise{i}", (x, y), Z_GROUPS + 0.5 + 0.01 * i, g0, k=k_, seed=90 + i, shadow=130, loops=loops,
                   draw=lambda key, j=0, x=x, y=y, k_=k_: C.galilee_folk(
                       x, y, k_, key[4], kind=key[1], variant=key[2], pose=key[3], expr=key[5],
                       phase=j / 4 if key[3] == "sit_pat_tummy" else key[6], food=key[7]))
        pfig.cut(0, fk(kind, v, p0, -1, {"sit_laugh": "laugh", "sit_pat_tummy": "yum", "sit": "kind"}[p0]))
        pfig.cut(t_amaze + 0.18 + 0.07 * i, fk(kind, v, "amazed", -1, "amazed"), depth=7)
        pfig.mots.append(bump(t_amaze + 0.2 + 0.07 * i, k_, (x, y), 14, 0.3))
        pfig.cut(t_ys4 + 0.05 * i, fk(kind, v, p2, -1, "joyful"), depth=6)
        pfig.cut(snap(t_xnh - 0.15 + 0.06 * i), fk(kind, v, "stand", -1, "happy"), depth=5)
        pfig.mots.append(breath((x, y), g0, 3.0 + 0.2 * i, 0.010, 0.4 * i))
        pfig.alpha = lambda t: 1.0 if t >= t_cut3 else 0.0
        fam.append(pfig)

    # ---------------------------------------------------------------- the boy
    bf = Fig("boy", (XBOY, YG + 4), Z_PEOPLE, g0, seed=101, shadow=90,
             loops={bk("pat_tummy", -1, "yum"): (4, 0.15)},
             draw=lambda key, j=0: C.the_boy(XBOY, YG + 4, K, key[2], pose=key[1], expr=key[3],
                                             phase=j / 4 if key[1] == "pat_tummy" else key[4], basket=key[5]))
    bf.cut(0, bk("pat_tummy", -1, "yum"))
    bf.mots.append(bump(t_bao[1], K, (XBOY, YG), 6, 0.4))
    bf.cut(snap(t_cut3), bk("smile", -1, "happy"), dip=False)
    bf.cut(snap(t_count[3] - 0.05), bk("watch", -1, "awed"), depth=5)
    bf.cut(t_amaze + 0.05, bk("eyes_wide", -1), depth=7)
    bf.cut(snap(t_cheer + 0.2), bk("cheer", -1, "overjoyed"), depth=6)
    # '小男孩看着满满的篮子': he steps over to the full baskets and looks at them
    t_w0 = snap(t_xnh - 0.05)
    xb1 = ROW[0] + 5.5 * GAP * ROW[2] + 92
    yb1 = ROW[1] + 22
    bf.cut(t_w0, bk("walk_a", -1, "happy"), dip=False)
    bf.track.to(t_w0 - 0.05, t_w0 + 0.1, (XBOY + xb1) / 2, (YG + 4 + yb1) / 2)
    bf.cut(snap(t_w0 + 0.3), bk("walk_b", -1, "happy"), dip=False)
    bf.track.to(t_w0 + 0.25, t_w0 + 0.4, xb1, yb1)
    bf.cut(snap(max(t_kan - 0.05, t_w0 + 0.55)), bk("eyes_wide", -1, "awed"), depth=6)
    bf.cut(snap(t_xiao - 0.06), bk("smile", -1, "smile"), depth=6)
    bf.mots.append(bump(t_xiao, K, (XBOY, YG), 8, 0.3))
    bf.mots.append(breath((XBOY, YG), g0, 2.6, 0.012, 0.3))
    bf.alpha = lambda t: 0.0 if t_cut1 <= t < t_cut3 else 1.0

    # ---------------------------------------------------------------- Jesus (S2 and from S4 on)
    jf = Fig("jesus", (XJ8, YG), Z_PEOPLE + 0.1, g0, seed=11, shadow=120)
    jf.cut(0, jk("stand", 1, "warm"))
    jf.cut(snap(t_ba - 0.08), jk("tell", 1, "warm"), depth=6)
    jf.mots.append(nod(t_lf + 0.05, K, (XJ8, YG), 3))
    jf.cut(snap(t_l1e + 0.2), jk("stand", 1, "smile"), depth=4)
    jf.cut(snap(t_jy + 0.3), jk("look_kind", 1, "smile"), depth=4)
    jf.cut(snap(t_ys4 + 0.3), jk("stand", 1, "smile"), depth=4)
    jf.cut(snap(t_xnh + 0.1), jk("look_kind", 1, "kind"), depth=5)
    jf.mots.append(breath((XJ8, YG), g0, 3.2, 0.010))
    jf.alpha = lambda t: 1.0 if (t_cut1 <= t < t_cut2) or t >= t_cut3 else 0.0

    # Peter, Andrew and John with their empty baskets (S2)
    s2 = []
    for i, (v, x, y) in enumerate((("peter", 728, YG + 10), ("andrew", 862, YG - 26), ("john", 996, YG + 6))):
        df = Fig(f"s2_{v}", (x, y), Z_PEOPLE - 0.2 + 0.01 * (i % 2), g0, seed=30 + i, shadow=110)
        df.cut(0, dk(v, "carry_basket", -1, "happy", fill=0.0))
        df.mots.append(nod(t_shou_l1 + 0.05 + 0.08 * i, K, (x, y), 4))
        df.cut(snap(t_lf + 0.1 + 0.1 * i), dk(v, "carry_basket", 1, "happy", fill=0.0), depth=6)
        df.mots.append(breath((x, y), g0, 3.0 + 0.2 * i, 0.010, 0.3 * i))
        df.alpha = during(t_cut1, t_cut2)
        s2.append(df)

    # ---------------------------------------------------------------- the gathering (S3)
    picks_t = [t_mt + 0.15] + list(t_shou)
    fills_after = [0.0, 0.25, 0.5, 0.75, 1.0, 1.0]
    for gi, (v, gx, gy) in enumerate(GATHER):
        off = (0.0, 0.05, -0.04, 0.08)[gi]
        times = [snap(tp + off) for tp in picks_t]

        def gkey(e, k, fill, holding):
            return (round(e, 3), k if (e < 0.01 or holding) else -1, fill, holding)

        ents = [(-1e4, gkey(1.0, -1, 0.0, False))]
        pile_cuts = [(-1e4, 0)]
        fill = 0.0
        for k, ts in enumerate(times):
            seq = [(-0.24, 1.0, False), (-0.16, 0.66, False), (-0.08, 0.33, False), (0.0, 0.0, True), (0.08, 0.33, True),
                   (0.16, 0.66, True), (0.24, 1.0, True)]
            for dt, e, hold in seq:
                ents.append((snap(ts + dt), gkey(e, k, fill, hold)))
            pile_cuts.append((snap(ts), k + 1))
            fill = fills_after[k]
            ents.append((snap(ts + 0.32), gkey(1.0, -1, fill, False)))
        frames, index = [], {}
        for _, key in ents:
            if key not in index:
                e, k, fl, hold = key
                index[key] = len(frames)
                tgt = PICKS[k] if (k >= 0 and e < 0.01) else PICKS[0]
                frames.append(doc(gather_fn(gx, gy, K, 1, variant=v, e=e, target=tgt, fill=fl, holding=hold,
                                            piece=PIECE_STYLE[k] if k >= 0 else PIECE_STYLE[0])))
        ents_s = sorted(ents, key=lambda e_: e_[0])

        def fa(t, ents_s=ents_s, index=index):
            cur = ents_s[0][1]
            for tk, key in ents_s:
                if t >= tk:
                    cur = key
            return float(index[cur])
        sc.add(f"gather{gi}", frames, z=Z_PEOPLE - 0.1 + 0.01 * gi, frame_at=fa, seed=700 + gi,
               motion=M.combine(breath((gx, gy), g0, 2.7 + 0.2 * gi, 0.008, 0.3 * gi),
                                lambda t: Tf(alpha=1.0 if t_cut2 <= t < t_cut3 else 0.0)))
        sc.add(f"gather{gi}_sh", doc(C.ground_shadow(gx + 50 * K, gy, K, 200, 0.2)), z=Z_PEOPLE - 0.12, wc=0,
               motion=lambda t: Tf(alpha=1.0 if t_cut2 <= t < t_cut3 else 0.0))
        # the pile of pieces he picks from (one gone on every pick)
        pile = [piece_at_hand(gx, gy, K, v, PICKS[k], PIECE_STYLE[k]) for k in range(len(times))]
        pframes = [doc("".join(pile[j:])) for j in range(len(times) + 1)]

        def pfa(t, pile_cuts=pile_cuts):
            cur = 0
            for tk, j in pile_cuts:
                if t >= tk:
                    cur = j
            return float(cur)
        sc.add(f"pile{gi}", pframes, z=Z_PEOPLE - 0.11 + 0.01 * gi, frame_at=pfa, seed=720 + gi,
               motion=lambda t: Tf(alpha=1.0 if t_cut2 <= t < t_cut3 else 0.0))

    # ---------------------------------------------------------------- S4: the twelve baskets and the twelve
    rx, ry, rs = ROW
    xs = row_basket_xs(rx, rs)
    t_c = [snap(tt) for tt in (t_count[0] + (t_count[-1] + 0.12 - t_count[0]) * j / 11 for j in range(12))]
    for j in range(12):
        piv = (xs[j], ry)
        sc.add(f"basket{j}", row_svg(rx, ry, rs, 0.9, only=j), z=Z_ROW + 0.001 * j,
               motion=M.combine(lambda t: Tf(alpha=1.0 if t >= t_cut3 else 0.0), bump(t_c[j], 1.0, piv, 12, 0.24)))
        top = ry - 166 * rs - 40
        sc.add(f"num{j}", number_svg(xs[j], top, j + 1, 0.6), z=Z_NUM, wc=0,
               motion=pop_in(t_c[j], (xs[j], top), dur=0.26, t1=snap(t_bi + 0.1), s0=0.3))
        sc.sfx("pop", t_c[j] + 0.01, gain_db=-17 - (j % 3), pan=-0.4 + 0.07 * j)
    # the twelve standing behind (two staggered lines)
    back = [(800 + 160 * i, 978, (2, 5, 7, 9, 11, 3)[i]) for i in range(6)]
    front = [(882 + 150 * i, 1014, (0, 1, 4, 6, 8, 10)[i]) for i in range(6)]

    def twelve(pose_of, expr):
        out = ""
        for x, y, v in back + front:
            f = 1 if x < rx else -1
            out += C.disciples(x, y, K * 0.97, f, variant=v, pose=pose_of(v), expr=expr)
        return out
    tw_frames = [doc(twelve(lambda v: "stand", "happy")), doc(twelve(lambda v: "amazed", "amazed")),
                 doc(twelve(lambda v: "wave" if v % 3 == 0 else "stand", "joyful"))]
    t_tw1 = snap(t_amaze + 0.06)
    t_tw2 = snap(t_cheer + 0.25)
    t_tw3 = snap(t_xnh - 0.25)
    piv12 = (rx, 1000)
    sc.add("twelve", tw_frames, z=Z_ROW_PEOPLE, seed=800,
           frame_at=lambda t: 0.0 if t < t_tw1 or t >= t_tw3 else (1.0 if t < t_tw2 else 2.0),
           motion=M.combine(lambda t: Tf(alpha=1.0 if t >= t_cut3 else 0.0), breath(piv12, g0, 3.1, 0.006),
                            squash(t_tw1, K, piv12, 7), squash(t_tw2, K, piv12, 6), squash(t_tw3, K, piv12, 5)))

    # ---------------------------------------------------------------- S5: the gloss - one little basket, twelve big ones
    GX, GY, GK = 1170, 440, 1.12
    t_g0 = snap(t_bi - 0.05)
    t_g1 = snap(t_jy - 0.15)
    sc.add("card", card_svg(GX, GY, GK), z=Z_GLOSS, motion=pop_in(t_g0, (GX, GY), t1=t_g1))
    lx = GX - 192 * GK
    sc.add("card_small", doc(PR.lunch_basket(lx, GY + 40 * GK, 0.78 * GK, 1, state="open", time=0.6)), z=Z_GLOSS + 0.1,
           motion=pop_in(snap(t_wb - 0.05), (lx, GY), dur=0.3, t1=t_g1, s0=0.4))
    sc.add("card_5", label_svg(lx, GY + 104 * GK, "5", 48 * GK), z=Z_GLOSS + 0.2, wc=0,
           motion=pop_in(snap(t_wb + 0.15), (lx, GY + 88 * GK), dur=0.25, t1=t_g1))
    sc.add("card_arrow", arrow_svg(GX - 110 * GK, GY - 4 * GK, 0.8 * GK), z=Z_GLOSS + 0.1,
           motion=pop_in(snap(t_hd - 0.25), (GX - 110 * GK, GY), dur=0.25, t1=t_g1))
    bxr = GX + 98 * GK
    sc.add("card_big", doc(PR.baskets_row(bxr, GY + 58 * GK, 0.35 * GK, n=12, fill=1.0, gap=150, rows=2, time=0.6)),
           z=Z_GLOSS + 0.1, motion=pop_in(snap(t_hd - 0.05), (bxr, GY), dur=0.32, t1=t_g1, s0=0.3))
    sc.add("card_12", label_svg(bxr, GY + 104 * GK, "12", 48 * GK), z=Z_GLOSS + 0.2, wc=0,
           motion=pop_in(snap(t_hd + 0.2), (bxr, GY + 88 * GK), dur=0.25, t1=t_g1))
    sc.fx.append(FX.sparkles((bxr - 160, GY - 90, bxr + 160, GY + 60), count=8, t0=t_hd, t1=t_g1, color=(255, 236, 170),
                             size=(6, 11), period=1.0, drift=-6, seed=81))

    # a soft warm glow round Jesus while the people say he is sent by God (light only, no halo)
    gid = "lf8jglow"
    sc.add("jglow", doc(f'<ellipse cx="{XJ8}" cy="{YG - 175 * K}" rx="{190 * K:.0f}" ry="{240 * K:.0f}" fill="url(#{gid})"/>',
                        defs=S.rad_grad(gid, [(0, "#fff2c4", 0.75), (0.6, "#ffe0a0", 0.3), (1, "#ffe0a0", 0)])),
           z=Z_PEOPLE + 0.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.9 * M.progress(t, t_ys4 - 0.1, t_ys4 + 0.8, "sine") *
                               (1 - M.progress(t, t_xnh + 0.2, t_xnh + 1.2, "sine"))))

    # ---------------------------------------------------------------- build the figures
    for ff in fam:
        ff.blinks(0.5, T - 0.4, rng)
    bf.blinks(0.5, T - 0.4, rng)
    jf.blinks(t_cut1 + 0.3, T - 0.4, rng)
    for ff in fam + [bf, jf] + s2:
        ff.build(sc)

    # ---------------------------------------------------------------- ambience
    sc.fx.append(FX.motes((0, 300, W5, 1150), count=22, color=(255, 214, 190), size=(2, 5), seed=18, alpha=100))
    sc.fx.append(FX.sparkles((rx - 520, ry - 160, rx + 520, ry - 40), count=10, t0=t_cut3 + 0.3, t1=T,
                             color=(255, 230, 170), size=(6, 11), period=1.4, drift=-5, seed=83))

    # ---------------------------------------------------------------- camera
    c1a, c1b = Cam(2040, 792, 1400), Cam(2020, 798, 1350)
    camS1 = zoom_cam([(0, c1a), (1.0, c1a), (t_cut1, c1b)], ["linear", "sine"])
    c2a, c2b = Cam(930, 742, 1460), Cam(900, 748, 1400)
    camS2 = zoom_cam([(t_cut1, c2a), (t_l1e, c2b)], "sine")
    c3a, c3b = Cam(2720, 790, 1460), Cam(2700, 794, 1420)
    camS3 = zoom_cam([(t_cut2, c3a), (t_cut3, c3b)], "sine")
    c4 = Cam(1160, 770, 1620)
    c5 = Cam(1160, 728, 1700)
    c6 = Cam(1480, 750, 1660)
    c7 = Cam(1250, 625, 2222)
    c8 = Cam(1660, 880, 1040)
    camS4 = zoom_cam([(t_cut3, c4), (t_bi - 0.3, c4), (t_bi + 0.5, c5), (t_jy - 0.3, c5), (t_jy + 0.7, c6),
                      (t_djs - 0.2, c6), (t_djs + 1.0, c7), (t_xnh - 0.6, c7), (t_xnh + 1.9, c8), (T, c8)],
                     ["linear", "sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear"])
    sc.camera = cut_cam([(0, camS1), (t_cut1, camS2), (t_cut2, camS3), (t_cut3, camS4)])

    # ---------------------------------------------------------------- sound
    sc.sfx("night", 0, dur=T + 0.5, gain_db=-28, fade_in=1.0, fade_out=1.0)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-27, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", 0, dur=T + 0.5, gain_db=-23, fade_in=0.8, fade_out=1.0, pan=0.2)
    sc.sfx("birds", 0, dur=t_cut2, gain_db=-28, fade_in=0.8, fade_out=1.0, pan=-0.3)
    sc.sfx("cloth", t_ba - 0.05, gain_db=-22)
    sc.sfx("cloth", t_lf + 0.1, gain_db=-21)
    for k, tp in enumerate(picks_t):
        sc.sfx("crunch", tp + 0.22, dur=0.5, gain_db=-24, fade_out=0.2, pan=0.2)
    sc.sfx("sparkle", t_count[-1] + 0.1, gain_db=-16)
    sc.sfx("pop", t_g0, gain_db=-19, pan=-0.2)
    sc.sfx("pop", t_wb, gain_db=-20, pan=-0.3)
    sc.sfx("pop", t_hd, gain_db=-18, pan=0.1)
    sc.sfx("crowd", t_jy, dur=2.2, gain_db=-15, fade_in=0.15, fade_out=1.2, pan=0.2)
    sc.sfx("cheer", t_cheer - 0.05, dur=t_xnh - t_cheer + 0.8, gain_db=-14, fade_in=0.3, fade_out=1.0)
    sc.sfx("chime", t_xiao - 0.02, gain_db=-17)
    return sc
