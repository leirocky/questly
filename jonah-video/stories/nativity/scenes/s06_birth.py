"""Scene 6 - Luke 2:7: night in the cave-stable of Bethlehem (the same stable() as s05, default look and lamp). Baby
Jesus is born: Mary holds the newborn, Joseph lifts his little clay lamp, a soft warm glow shines on the baby; Mary sits
on a small straw bundle (hidden behind her skirt when she stands) and wraps him in cloth bands, then lays him gently in the manger on the fresh hay; a little picture
shows what a manger is (the ox and the donkey munching hay from one); the baby falls asleep; outside, the stars of
Bethlehem twinkle.

One tall stage (3400 x 1913) with the stable at scale 1 (people 330 px): the camera starts wide on the stable on its hill
under the stars, glides in close for the birth and glides back out to the stars at the end.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm wide frame (page dip from s05): the stable on its hill under the deep-blue sky, warm lamplight in the
               doorway; inside, Mary holds the newborn, Joseph with his lamp, the ox and the donkey resting; stars twinkle
  '他们在伯利恒的时候' the far stars breathe; the camera begins to glide in
  '小耶稣出生了' a soft warm glow blooms on the baby in Mary's arms (chime); Joseph's face lights up; the ox and the
               donkey turn their heads to look
  '用布把他包起来' Mary sits down on the straw bundle and wraps him in the cloth (wrap pose; cloth rustle); Joseph leans on
               his staff and watches tenderly
  '轻轻地放在马槽里' she rises, turns to the manger and lays him down gently on the fresh hay (lay_baby, a slow
               lowering); on '马槽' he lies in the manger (a little glow pulse), she straightens and smiles down at him;
               he opens his eyes
  '马槽，就是给牛和驴吃草的槽子' a round picture pops up beside them: a manger full of hay, the ox munching from one end
               ('牛') and the donkey from the other ('驴') (crunch); it pops away after the line
  '小耶稣睡着了' the baby's eyes close (the glow softens and warms); Mary smiles down; Joseph kneels; the ox and the
               donkey close their eyes too
  '睡着了'…'闪'  the camera glides back out (~3.1 s, from 'sleep' to just after the first 闪, even log-zoom about
               the stable, peak ~1.4 %/frame) to the stable on its hill under the stars
  '一闪一闪亮晶晶' the stars flare exactly on 闪 (left sky), 闪 (right sky), 晶 (over the hill), 晶 (all) (sparkles)
  end          calm wide hold for the page dip into s07 (another illustrator)
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
from stories.nativity.scenes.s01_title import (Fig, Twinkle, beat, breath, char_times, dip, f1, flicker, keyed, snap,
                                               voice_marks)

INK = S.P["ink"]
SW, SH = 3400, 1913
STAB = (1700, 1430, 1.0)
HILL_Y, HILL_S = 1560, 1.5
PTS = PR.stable_points(*STAB)
BED = PTS["bed"]                               # (1740, 1276)
MGR = PTS["manger"]                            # (1740, 1400)
MARY = (MGR[0] + C.MARY_LAY_DX, MGR[1] - 12)   # (1852, 1388): lay_baby facing -1 puts the baby on the bed
JOS = (1418, 1416)
OX = (2210, 1372)
DONKEY = (1235, 1372)
ANIMAL_S = 0.9
INSET = (2300, 1002, 198)                       # the 'what is a manger' picture: centre, radius


def doc(body, defs=""):
    return S.svg_doc(body, defs, SW, SH)


def glow_svg(cx, cy, rx, ry, gid, c0="#fff4d0", c1="#ffd986", a0=0.9, a1=0.38):
    defs = S.rad_grad(gid, [(0, c0, a0), (0.45, c1, a1), (1, c1, 0)])
    return doc(f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="{f1(rx)}" ry="{f1(ry)}" fill="url(#{gid})"/>', defs)


# ================================================================== drawings

def sky_svg():
    return doc(PR.starry_sky(-40, -40, SW + 40, 1500, density=1.0, twinkle=0.2, milky_way=True, seed=61, scale=1.3))


def hills_svg():
    return doc(PR.night_hills(-80, SW + 80, HILL_Y, HILL_S, part="back", fire_x=False, fold_x=False, town=True, seed=9))


def field_svg():
    return doc(PR.night_hills(-80, SW + 80, HILL_Y, HILL_S, part="front", fire_x=False, fold_x=False, town=True, seed=9,
                              bottom=SH + 60))


def tufts_svg():
    x, y, s = STAB
    rng = random.Random(4)
    b = ""
    for i in range(70):
        tx = x - 980 + i * 28 + rng.uniform(-8, 8)
        if 1060 < tx < 2340 and i % 3:
            continue
        ty = y + 34 + rng.uniform(-6, 14)
        h = rng.uniform(18, 34)
        b += (f'<path d="M{f1(tx - 10)},{f1(ty)} l5,{f1(-h)} l5,{f1(h * 0.8)} l5,{f1(-h * 1.1)} l5,{f1(h)}" '
              f'stroke="#2f4a3a" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return doc(S.g(b, filter="wobble-fine"))


def spill_svg():
    x, y, s = STAB
    return doc(PR._warm_glow(x, y + 60, 760, 90, 0.8, "n6spill", "#ffe9b0", "#ffc860"))


def stable_svg(part):
    return doc(PR.stable(*STAB, part=part, lamp=1.0, time="night"))


def manger_front_svg():
    return doc(PR.manger(*MGR, STAB[2], part="front", time="day"))


def bale_svg():
    """Mary's seat: a small tied bundle of straw, no wider than her skirt, so it hides behind her when she stands
    and only shows under her when she sits (no box round her feet)."""
    x, y = MARY[0] + 2, MARY[1]
    w, h = 60, 62
    hay, dk = "#e3b955", "#b8892e"
    o = (f'<path d="M{x - w / 2},{y} L{x - w / 2},{y - h} Q{x},{y - h - 8} {x + w / 2},{y - h} L{x + w / 2},{y} Z" '
         f'fill="{hay}" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>')
    for i in range(7):
        xx = x - w / 2 + 6 + i * (w - 12) / 6
        o += f'<path d="M{f1(xx)},{y - 4} L{f1(xx + 2)},{y - h + 6}" stroke="{dk}" stroke-width="2" opacity="0.6"/>'
    o += f'<path d="M{x - w / 2},{y - h * 0.5} Q{x},{y - h * 0.5 + 5} {x + w / 2},{y - h * 0.5}" stroke="#7a5230" stroke-width="4" fill="none"/>'
    return doc(S.g(o, filter="wobble-fine"))


# wall stones of stable() (seed 0) that would sit round Mary's head like a ring in the close-up: painted out
HALO_STONES = (2, 5, 21, 45)
STABLE_SEED = 401


def wall_patch_svg():
    """The cave's back wall exactly as stable() paints it (same lit gradient, same stones in the same places, same
    wobble), minus the HALO_STONES, clipped to just round those stones. Laid over the stable on the same watercolour
    seed (and no edge pooling), it paints those rings out without a seam."""
    x0, top, x1, _ = PR.STABLE_OPENING
    op = (f"M{x0},0 L{x0},{top + 230} Q{x0 + 20},{top + 30} {x0 + 260},{top} L{x1 - 260},{top} "
          f"Q{x1 - 20},{top + 30} {x1},{top + 230} L{x1},0 Z")
    k = 1.0
    wall_lit = S.mix("#6a4a34", "#e8b46a", 0.75 * k)
    body = (f'<defs>{S.rad_grad("n6wall", [(0, wall_lit), (0.55, S.mix("#4a3428", "#b07a48", 0.6 * k)), (1, "#2e2420")], 0.43, 0.42, 0.62)}</defs>'
            f'<path d="{op}" fill="url(#n6wall)"/>')
    rng2 = random.Random(0 + 9)
    holes = ""
    for i in range(46):
        sx_, sy_ = rng2.uniform(x0, x1), rng2.uniform(top + 40, PR.STABLE_BACK_Y - 20)
        rx_, ry_ = rng2.uniform(40, 90), rng2.uniform(24, 46)
        if i in HALO_STONES:
            holes += f'<ellipse cx="{f1(sx_)}" cy="{f1(sy_)}" rx="{f1(rx_ + 14)}" ry="{f1(ry_ + 14)}"/>'
            continue
        body += PR._ell(sx_, sy_, rx_, ry_, "none", 3, stroke="#3a2c24", extra='opacity="0.28"')
        body += PR._p(f"M{f1(sx_ - rx_ * 0.5)},{f1(sy_ - ry_ * 0.4)} Q{f1(sx_)},{f1(sy_ - ry_ * 0.9)} "
                      f"{f1(sx_ + rx_ * 0.4)},{f1(sy_ - ry_ * 0.5)}", sw=3, stroke="#f2c47a", extra=f'opacity="{0.25 * k:.2f}"')
    clip = f'<clipPath id="n6holes">{holes}</clipPath><g clip-path="url(#n6holes)">{body}</g>'
    return doc(PR._place(clip, *STAB))


def mary_body(pose, facing=1, expr=None, baby=True):
    x, y = MARY
    return C.mary(x, y, STAB[2], facing, pose=pose, expr=expr, baby=baby)


def joseph_body(pose, expr=None):
    x, y = JOS
    return C.joseph_carpenter(x, y, STAB[2], 1, pose=pose, expr=expr)


def ox_body(pose, eyes="open"):
    x, y = OX
    return PR.ox(x, y, STAB[2] * ANIMAL_S, -1, pose=pose, eyes=eyes)


def donkey_body(pose, eyes="open"):
    x, y = DONKEY
    return PR.donkey(x, y, STAB[2] * ANIMAL_S, 1, pose=pose, sacks=0, eyes=eyes)


def baby_body(state):
    return C.baby_jesus(*BED, STAB[2], 1, state=state, hand=(state == "awake"))


def shadow(x, y, w):
    return (f'<ellipse cx="{f1(x)}" cy="{f1(y + 3)}" rx="{f1(w / 2)}" ry="13" fill="#4a3020" opacity="0.3" '
            f'filter="url(#soft)"/>')


def lamp_glow_svg():
    lx, ly = PTS["lamp"]
    return glow_svg(lx, ly + 40, 420, 330, "n6lamp", "#fff1c6", "#ffcf70", 0.65, 0.28)


def jlamp_glow_svg():
    x, y = JOS
    return glow_svg(x + 111, y - 236, 260, 220, "n6jlamp", "#fff1c6", "#ffcf70", 0.75, 0.3)


HOLD_C = (MARY[0] + 40, MARY[1] - 168)        # the baby in Mary's arms (hold_baby, facing 1)


def baby_glow_svg():
    return glow_svg(HOLD_C[0], HOLD_C[1], 170, 140, "n6baby", "#fffbea", "#ffe7a0", 0.9, 0.4)


# ---- the little round picture: what a manger is
def inset_body(k):
    cx, cy, r = INSET
    fy = cy + 118                                  # the floor line inside the picture
    gid = "n6inbg"
    defs = (S.rad_grad(gid, [(0, "#f8dca0"), (0.6, "#dcaa6a"), (1, "#9a6a40")], cx=0.5, cy=0.38, r=0.7) +
            f'<clipPath id="n6inclip"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
    inner = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#{gid})"/>'
    for i in range(7):                             # the rough stones of the wall
        sx_, sy_ = cx - 170 + i * 56 + (i % 2) * 18, cy - 120 + (i % 3) * 52
        inner += (f'<ellipse cx="{sx_}" cy="{sy_}" rx="34" ry="20" fill="none" stroke="#7a5236" stroke-width="2.6" '
                  f'opacity="0.35"/>')
    inner += (f'<path d="M{cx - r},{fy - 6} Q{cx},{fy - 16} {cx + r},{fy - 6} L{cx + r},{cy + r} L{cx - r},{cy + r} Z" '
              f'fill="#e8c46c" stroke="{INK}" stroke-width="3"/>')
    inner += PR._straw_bits(cx - r, cx + r, fy, cy + r - 10, 30, 5)
    # munching: each animal's head dips in turn (a small rotation about its legs), ox and donkey out of phase
    oa = (0, 3.0, 0.6, -1.2)[k % 4]
    da = (0, 3.0, 0.6, -1.2)[(k + 2) % 4]
    ox_x, ox_y, dk_x, dk_y = cx + 190, fy + 2, cx - 180, fy + 2
    inner += PR.hanging_lamp(cx - 70, cy - r - 4, 0.9, 1.0)
    inner += PR.manger(cx, fy + 8, 0.78, 1, hay=True, part="back", time="day")
    inner += (f'<g transform="rotate({-oa} {ox_x + 50} {ox_y})">'
              f'{PR.ox(ox_x, ox_y, 0.72, -1, pose="look")}{_wisp(ox_x - 172, ox_y - 74, k)}</g>')
    inner += (f'<g transform="rotate({da} {dk_x - 40} {dk_y})">'
              f'{PR.donkey(dk_x, dk_y, 0.72, 1, pose="look", sacks=0)}{_wisp(dk_x + 136, dk_y - 66, k + 2)}</g>')
    inner += PR.manger(cx, fy + 8, 0.78, 1, hay=True, part="front", time="day")
    body = f'<g clip-path="url(#n6inclip)">{inner}</g>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" stroke="#fff4dc" stroke-width="14"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="none" stroke="{INK}" stroke-width="4"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="3"/>'
    return S.g(body, filter="wobble-fine"), defs


def _wisp(x, y, k):
    """A few straws sticking out of a munching mouth (they wiggle with k)."""
    a = (0, 6, 0, -6)[k % 4]
    return (f'<g transform="rotate({a} {x} {y})"><path d="M{x - 12},{y + 4} L{x + 14},{y - 8} M{x - 10},{y + 8} '
            f'L{x + 16},{y + 2} M{x - 8},{y} L{x + 10},{y - 16}" stroke="#d9a63e" stroke-width="3.2" '
            f'stroke-linecap="round"/></g>')


def inset_svg(k):
    body, defs = inset_body(k)
    return doc(body, defs)


def inset_shadow_svg():
    cx, cy, r = INSET
    return doc(f'<circle cx="{cx + 8}" cy="{cy + 12}" r="{r + 16}" fill="#2a1a10" opacity="0.35" filter="url(#soft)"/>')


# ================================================================== the sky for the twinkles

_MASS = [(-960, 40), (-980, -380), (-900, -700), (-700, -900), (-380, -1000), (0, -1030), (420, -990), (760, -860),
         (940, -620), (990, -300), (970, 40)]


def _inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def sky_points(n=40, seed=3):
    x0, y0, s = STAB
    poly = [(x0 + lx * 1.12 * s, y0 - 450 * s + (ly + 450) * 1.12 * s) for lx, ly in _MASS]
    blobs = [(x0 + 570 * s, y0 - 1150 * s, 230), (x0 - 560 * s, y0 - 930 * s, 170), (x0 - 180 * s, y0 - 1040 * s, 140),
             (x0 + 300 * s, y0 - 1010 * s, 160), (x0 + 780 * s, y0 - 820 * s, 160), (x0 - 860 * s, y0 - 640 * s, 150)]

    def avoid(x, y):
        if y > 930 or _inside(poly, x, y):
            return True
        return any((x - bx) ** 2 + (y - by) ** 2 < br ** 2 for bx, by, br in blobs)
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        x, y = rng.uniform(60, SW - 60), rng.uniform(40, 920)
        if avoid(x, y) or any((x - a) ** 2 + (y - b) ** 2 < 110 ** 2 for a, b, _ in out):
            continue
        out.append((x, y, rng.uniform(11, 19)))
    return out


# ================================================================== camera


def zoom_path(keys, curves):
    """Camera keyframes where every zoom happens about a fixed point of the picture, at an even rate in log-width
    (a plain linear width runs fastest at the close end): w = exp(lerp(ln w0, ln w1, u)), and the centre moves in
    step with w, so the picture never swims and the zoom speed peaks gently."""
    ks = sorted(keys, key=lambda k: k[0])

    def cam(t):
        if t <= ks[0][0]:
            return ks[0][1]
        if t >= ks[-1][0]:
            return ks[-1][1]
        for i in range(len(ks) - 1):
            (t0, a), (t1, b) = ks[i], ks[i + 1]
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, curves[min(i, len(curves) - 1)])
                if abs(b.w - a.w) > 1:
                    w = math.exp(M.lerp(math.log(a.w), math.log(b.w), u))
                    v = (w - a.w) / (b.w - a.w)
                else:
                    w, v = M.lerp(a.w, b.w, u), u
                return Cam(M.lerp(a.x, b.x, v), M.lerp(a.y, b.y, v), w)
        return ks[-1][1]
    return cam


# ================================================================== build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines

    t_born = beat(ctx, 0, "出生了")
    t_small = beat(ctx, 0, "小耶稣")
    t_wrap = beat(ctx, 1, "用布")
    t_gently = beat(ctx, 1, "轻轻地")
    t_in = beat(ctx, 1, "槽里")
    t_gloss = L[1].chunks[2].start if len(L[1].chunks) > 2 else beat(ctx, 1, "马槽，")
    t_ox = beat(ctx, 1, "牛")
    t_dk = beat(ctx, 1, "驴")
    t_l2end = L[1].end
    t_sleep = beat(ctx, 2, "睡着")
    t_sky = beat(ctx, 2, "天上")
    flare_ts = []
    for ent in voice_marks(ctx, 2):
        if "闪" in ent[0]:
            ct = char_times(ent)
            flare_ts = [ct[i] for i, ch in enumerate(ent[0]) if ch in "闪晶"]
    if len(flare_ts) < 4:                               # fallback: spread over the chunk
        c = L[2].chunks[-1]
        flare_ts = [c.start + (c.end - c.start) * u for u in (0.45, 0.6, 0.78, 0.9)]
    flare_ts = flare_ts[:4]

    # ---------------- cuts
    c_sit = snap(t_wrap - 0.1)                    # Mary sits down on the bale and wraps him
    c_jwatch = snap(t_wrap + 0.35)                # Joseph leans on his staff
    c_lay = snap(t_gently - 0.12)                 # she rises, turns and lays him down
    c_in = snap(t_in + 0.08)                      # he lies in the manger
    c_up = snap(c_in + 0.55)                      # she straightens up and smiles down
    c_awake = snap(c_in + 0.9)                    # he opens his eyes
    c_asleep = snap(t_sleep + 0.05)               # his eyes close
    c_kneel = snap(t_sleep + 0.35)                # Joseph kneels
    c_olook = snap(t_born + 0.4)
    c_dlook = snap(t_born + 0.7)

    # ---------------- background
    sc.add("sky", sky_svg(), z=0, wc=0.55)
    sc.add("hills", hills_svg(), z=0.5, wc=0.8)
    sc.add("field", field_svg(), z=1, wc=0.8)
    sc.add("stable", stable_svg("back"), z=2, wc=0.9, seed=STABLE_SEED)
    sc.add("wallpatch", wall_patch_svg(), z=2.01, wc=0.9, wc_edge=0.0, seed=STABLE_SEED)

    # ---------------- the animals
    dk = Fig(ctx, "donkey", DONKEY, 3.0, seed=101)
    dk.at(0, donkey_body("lie")).at(c_dlook, donkey_body("lie_look")).at(snap(c_asleep + 0.6), donkey_body("lie_look", "closed"))
    dk.move(dip(c_dlook, 4, 0.97), breath(ctx, 0.012, 3.6, 0.2)).add(sc)
    ox = Fig(ctx, "ox", OX, 3.1, seed=103)
    ox.at(0, ox_body("lie")).at(c_olook, ox_body("lie_look")).at(snap(c_asleep + 0.4), ox_body("lie_look", "closed"))
    ox.move(dip(c_olook, 4, 0.97), breath(ctx, 0.012, 3.9, 0.5)).add(sc)

    # ---------------- Mary, the bale, the baby, Joseph
    sc.add("bale", bale_svg(), z=3.2, seed=105)
    mary = Fig(ctx, "mary", MARY, 3.3, seed=107)
    mary.at(0, mary_body("hold_baby", 1, "tender"))
    mary.at(c_sit, mary_body("wrap", 1, "tender"))
    mary.at(c_lay, mary_body("lay_baby", -1, "tender"))
    mary.at(c_in, mary_body("lay_baby", -1, "tender", baby=False))
    mary.at(c_up, mary_body("smile_down", -1, "tender"))
    lower = keyed([(c_lay, -16.0), (c_in - 0.05, 0.0)], "sine")
    mary.move(dip(c_sit, 8), dip(c_lay, 6), dip(c_up, 5), breath(ctx, 0.008, 3.3),
              lambda t: Tf(dy=lower(t) if c_lay <= t < c_in else 0.0, rot=(0.25 * lower(t)) if c_lay <= t < c_in else 0.0))
    mary.add(sc)

    baby = Fig(ctx, "baby", BED, 3.5, seed=109)
    baby.at(0, "")
    baby.at(c_in, baby_body("in_manger")).at(c_awake, baby_body("awake")).at(c_asleep, baby_body("in_manger"))
    baby.move(breath(ctx, 0.02, 1.6))
    baby.add(sc)
    sc.add("manger_front", manger_front_svg(), z=3.6, seed=111)

    jos = Fig(ctx, "joseph", JOS, 3.4, seed=113)
    jos.at(0, joseph_body("hold_lamp", "tender"))
    jos.at(snap(t_born + 0.2), joseph_body("hold_lamp", "joyful"))
    jos.at(c_jwatch, joseph_body("watch", "tender"))
    jos.at(c_kneel, joseph_body("kneel", "tender"))
    jos.move(dip(snap(t_born + 0.2), 4), dip(c_jwatch, 6), dip(c_kneel, 9), breath(ctx, 0.008, 3.7, 0.4))
    jos.add(sc)
    sc.add("jlamp", jlamp_glow_svg(), z=3.45, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(0.55 + 0.4 * flicker(t, 0.3)) * (1 - M.progress(t, c_jwatch - 0.02, c_jwatch, "linear"))))

    # ---------------- the front of the stable, lamplight
    sc.add("stable_front", stable_svg("front"), z=4, wc=0.9)
    sc.add("tufts", tufts_svg(), z=4.05, wc=0.5)
    sc.add("spill", spill_svg(), z=1.5, wc=0, blend="screen", motion=lambda t: Tf(alpha=0.6 + 0.3 * flicker(t)))
    sc.add("lampglow", lamp_glow_svg(), z=4.1, wc=0, blend="screen", motion=lambda t: Tf(alpha=0.4 + 0.4 * flicker(t, 0.6)))

    # ---------------- the glow on the baby: follows him (arms, lap, manger)
    hold_c = HOLD_C
    lap_c = (MARY[0] + 64, MARY[1] - 112)
    bed_c = (BED[0], BED[1] - 30)
    glow_lvl = keyed([(t_born - 0.1, 0.0), (t_born + 0.7, 1.0), (t_born + 1.6, 0.72), (c_in - 0.1, 0.72),
                      (c_in + 0.15, 1.0), (c_in + 0.9, 0.75), (c_asleep - 0.1, 0.75), (c_asleep + 0.8, 0.95)], "sine")

    def glow_m(t):
        if t < c_sit:
            p = hold_c
        elif t < c_lay:
            p = lap_c
        else:
            p = bed_c
        a = glow_lvl(t) * (0.9 + 0.1 * math.sin(2 * math.pi * t / 2.4))
        return Tf(dx=p[0] - hold_c[0], dy=p[1] - hold_c[1], alpha=a)
    sc.add("babyglow", baby_glow_svg(), z=4.2, wc=0, blend="screen", motion=glow_m)

    # ---------------- the little picture: what a manger is
    cx, cy, r = INSET
    t_pop = snap(t_gloss + 0.05)
    t_away = snap(max(t_l2end + 0.25, t_dk + 0.9))

    def inset_m(t):
        if t < t_pop or t > t_away + 0.3:
            return Tf(alpha=0.0)
        u = M.progress(t, t_pop, t_pop + 0.45, "back")
        s_ = 0.25 + 0.75 * u
        a = min(1.0, (t - t_pop) / 0.12)
        if t > t_away:
            v = (t - t_away) / 0.3
            s_ *= 1 - 0.4 * v
            a *= 1 - v
        return Tf(sx=s_, sy=s_, alpha=a, dy=3 * math.sin(2 * math.pi * t / 2.6), px=cx, py=cy)

    def munch_fa(t):
        if t < t_ox:
            return 0.0
        return float(int((t - t_ox) / 0.13) % 4)
    sc.add("inset_shadow", inset_shadow_svg(), z=5, wc=0, motion=inset_m)
    sc.add("inset", [inset_svg(k) for k in range(4)], z=5.1, wc=0.5, motion=inset_m, frame_at=munch_fa, seed=115)

    # ---------------- camera: wide -> close for the birth -> wide to the stars
    c_wide0 = Cam(1700, 945, 3290)
    c_wide1 = Cam(1712, 955, 3200)
    c_close = Cam(1785, 1222, 1380)
    c_close2 = Cam(1815, 1180, 1440)
    c_end = Cam(1700, 948, 3280)
    t_push0 = max(1.2, t_small - 1.6)
    t_push1 = t_born + 1.0
    t_back0 = t_sleep - 0.1                       # the pull-out starts as he falls asleep ...
    t_back1 = flare_ts[0] + 0.4                   # ... and settles just after the first 闪 (~3.1 s)
    sc.camera = zoom_path([(0, c_wide0), (t_push0, c_wide1), (t_push1, c_close), (c_lay, c_close),
                           (t_gloss - 0.15, c_close2), (t_back0, c_close2), (t_back1, c_end), (T, Cam(1700, 950, 3296))],
                          ["sine", "sine", "sine", "sine", "sine", "sine", "sine"])

    # ---------------- stars: soft twinkles all the time, flares on 闪 闪 晶 晶
    stars = sky_points(42)
    left = {i for i, (x, y, r_) in enumerate(stars) if x < 1000}
    right = {i for i, (x, y, r_) in enumerate(stars) if x > 2400}
    top = {i for i, (x, y, r_) in enumerate(stars) if 1000 <= x <= 2400}
    flares = [(flare_ts[0], 1.5, left), (flare_ts[1], 1.5, right), (flare_ts[2], 1.5, top), (flare_ts[3], 1.2, None)]

    def sky_alpha(t):
        w = sc.camera(t).w
        return M.progress(w, 2200, 3000, "sine")
    sc.fx.append(Twinkle(stars, flares=flares, alpha_fn=sky_alpha, seed=7))
    sc.fx.append(FX.motes((1100, 820, 2330, 1420), count=22, color=(255, 236, 190), seed=17, alpha=110))
    sc.fx.append(FX.sparkles((bed_c[0] - 110, bed_c[1] - 90, bed_c[0] + 110, bed_c[1] + 30), count=5, t0=t_born + 0.3,
                             t1=c_sit, size=(8, 14), period=1.5, drift=-6, seed=19))
    sc.fx.append(FX.sparkles((bed_c[0] - 130, bed_c[1] - 80, bed_c[0] + 60, bed_c[1] + 20), count=6, t0=c_in,
                             size=(8, 14), period=1.7, drift=-6, seed=21))

    # ---------------- sound
    sc.sfx("night", 0, dur=T, gain_db=-22, fade_in=0.8, fade_out=0.8)
    sc.sfx("fire", 0, dur=T, gain_db=-32, fade_in=0.8, fade_out=0.8)
    sc.sfx("chime", t_born + 0.05, gain_db=-12)
    sc.sfx("cloth", c_sit + 0.1, gain_db=-14)
    sc.sfx("cloth", c_sit + 0.9, gain_db=-17)
    sc.sfx("sparkle", c_in + 0.05, gain_db=-16)
    sc.sfx("pop", t_pop, gain_db=-17, pan=0.5)
    sc.sfx("crunch", t_ox, gain_db=-16, pan=0.5)
    sc.sfx("pop", t_away, gain_db=-20, pan=0.5)
    sc.sfx("sparkle", c_asleep + 0.1, gain_db=-20)
    for i, tf in enumerate(flare_ts):
        sc.sfx("sparkle", tf - 0.03, gain_db=-14 - (i == 3) * 2, pan=(-0.6, 0.6, 0.0, 0.0)[i])
    return sc

