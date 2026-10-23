"""Scene 5 — Mark 4:30-32. Jesus tells the parable of the mustard seed. The scene opens on the shore of s04 (Jesus
on the stern of the moored boat, the crowd sitting on the sand); his story blooms out of his open hand as a framed
picture-book page in warm golden colours: a hand holding a tiny seed, the seed dropped into the garden soil, rain and
sun, a sprout that grows and grows into a big bushy tree with yellow flowers towering over the little vegetables,
songbirds flying in to build nests in its branches. Then the page closes back into Jesus' hand and the listeners nod
and smile; a little girl stands up and stretches her arms like the growing tree.

Beats (syllable onsets measured in the voice clip, proportional fallback):
  0 .. 0.9         calm medium shot of the shore (as at the end of s04): Jesus teaching, children in front
  '耶稣给大家讲'     the camera eases toward Jesus; he gestures with his open hand
  '小小种子'        a tiny golden twinkle on his palm (sparkle)
  '故事'           the story page opens in a widening circle from his hand (whoosh, chime)
  '芥菜种'          the page: an open hand holding a tiny seed; '最小' the golden ring round the seed pulses, the
                   second '最小' the camera leans in
  '种在地里'        the hand tips; on '种' the seed drops into the dug hole in the garden bed (pop), the hand
                   withdraws; a little rain cloud drifts over and rains (rain), the sun comes out
  '长啊长'          on each '长' (and '啊') the plant shoots up a stage: sprout, young plant, leafy bush (grow)
  '长大了，比所有的菜都大' it keeps growing on '长大了', '比', '都', '大' into a big bushy tree with yellow flowers, towering
                   over the cabbages, leeks and carrots; the camera pulls back to the whole page
  '小鸟'           four songbirds fly in and land in the branches; '枝子上' their nests build twig by twig,
                   '做窝' eggs appear in them (pop); the tree sways, the birds bob
  L2 '大家听了'     the page closes back into Jesus' hand; '点点头' the listeners nod twice; '笑了' everyone smiles
                   and a little girl in front stands up and stretches her arms up like the tree, swaying; calm hold
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import OUT_H, OUT_W
from engine.scene import Scene
from stories.storm.scenes import s04_shore as S4
from stories.noah.scenes.s01_title import cuts
from stories.storm.scenes.s04_shore import Actor, blink, doc, f1, snap, timer

INK = P["ink"]
SEAT = S4.SEAT
PALM = (SEAT[0] - 58 * S4.BK, SEAT[1] - 172 * S4.BK)     # Jesus' open hand in 'teach' (facing -1)

# ------------------------------------------------------------------ the story page geometry
HX, HY, HK = 1250, 620, 1.75         # the hand holding the seed (props.mustard_seed anchor = palm middle)
HSEED = (HX - 40 * HK, HY + 18 * HK)  # the seed on the palm
WRIST = (HX - 205 * HK, HY + 70 * HK)
PX, PY, PK = 1176, 942, 1.0          # the mustard plant: root on the garden bed
PSEED = (PX + 6 * PK, PY - 18 * PK)  # where the seed lies in the soil (growth 0)
GROWTH = (0.0, 0.1, 0.2, 0.3, 0.38, 0.45, 0.52, 0.6, 0.7, 0.8, 0.9, 1.0)
NESTS = [(PX + nx * PK, PY + ny * PK) for nx, ny in PR.MUSTARD_NESTS]
SKY = ("#f3cf9a", "#f9e2bb", "#fcefd6")
GREEN, GREEN_D, GREEN_L = "#86b45c", "#5f8f3e", "#b5d67a"


# ------------------------------------------------------------------ vegetables (the little garden)
def _veg(kind, x, y, s=1.0):
    """A little garden vegetable standing on the bed at (x, y) (bottom centre)."""
    st = f'stroke="{INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
    b = ""
    if kind == "cabbage":
        for i, (dx, dy, rx, ry, c) in enumerate(((-34, -26, 34, 24, GREEN_D), (34, -26, 34, 24, GREEN_D),
                                                 (0, -40, 44, 36, GREEN), (-18, -48, 24, 22, GREEN_L),
                                                 (20, -46, 22, 20, GREEN_L))):
            b += f'<ellipse cx="{dx}" cy="{dy}" rx="{rx}" ry="{ry}" fill="{c}" {st}/>'
        b += f'<path d="M0,-70 Q4,-46 0,-20 M-20,-40 Q-6,-34 0,-26 M20,-40 Q6,-34 0,-26" fill="none" {st} opacity="0.6"/>'
    elif kind == "lettuce":
        for i in range(7):
            a = -80 + i * 27
            b += (f'<path d="M0,-6 Q{f1(60 * math.sin(math.radians(a)) - 14)},{f1(-40 - 30 * math.cos(math.radians(a)))} '
                  f'{f1(70 * math.sin(math.radians(a)))},{f1(-20 - 46 * math.cos(math.radians(a)))} '
                  f'Q{f1(60 * math.sin(math.radians(a)) + 16)},{f1(-20 - 20 * math.cos(math.radians(a)))} 0,-6 Z" '
                  f'fill="{GREEN_L if i % 2 else "#a3cc66"}" {st}/>')
    elif kind == "leek":
        for i, a in enumerate((-18, -6, 8, 20)):
            b += (f'<path d="M-6,-30 Q{f1(a * 2)},{-90 - 10 * (i % 2)} {f1(a * 4.2)},{-150 + 12 * abs(a) / 10} '
                  f'Q{f1(a * 2 + 12)},-86 6,-30 Z" fill="{"#6f9f4c" if i % 2 else "#86b45c"}" {st}/>')
        b += f'<rect x="-11" y="-36" width="22" height="36" rx="8" fill="#f2ecd8" {st}/>'
    elif kind == "carrot":
        for a in (-30, -12, 6, 24):
            tx, ty = 70 * math.sin(math.radians(a)), -100 * math.cos(math.radians(a))
            b += f'<path d="M0,-12 Q{f1(tx * 0.4)},{f1(ty * 0.5)} {f1(tx)},{f1(ty)}" fill="none" {st}/>'
            for j in range(3):
                u = 0.45 + 0.2 * j
                cx, cy = tx * u, ty * u
                b += f'<ellipse cx="{f1(cx)}" cy="{f1(cy)}" rx="13" ry="6" fill="#7fae5a" transform="rotate({a - 60} {f1(cx)} {f1(cy)})" {st}/>'
        b += f'<path d="M-16,-2 Q0,-26 16,-2 Z" fill="#ef9a4a" {st}/>'
    elif kind == "onion":
        for a in (-16, -4, 10):
            b += (f'<path d="M-4,-40 Q{f1(a * 1.5)},-90 {f1(a * 3.4)},-128 Q{f1(a * 1.5 + 9)},-88 5,-40 Z" '
                  f'fill="#7fae5a" {st}/>')
        b += f'<path d="M-26,0 Q-30,-34 0,-46 Q30,-34 26,0 Z" fill="#e6c6d6" {st}/>'
    return f'<g transform="translate({f1(x)},{f1(y)}) scale({s})">{b}</g>'


GARDEN = (("lettuce", 300, 0.85), ("cabbage", 430, 0.9), ("carrot", 560, 0.85), ("leek", 680, 0.8),
          ("cabbage", 800, 0.8), ("onion", 900, 0.8), ("lettuce", 1450, 0.8), ("carrot", 1560, 0.85),
          ("cabbage", 1690, 0.9), ("leek", 1810, 0.85), ("onion", 1920, 0.8))


def page_bg_svg():
    """The warm golden story page: sky, soft hills, a far basalt house with a fig tree, meadow, the garden bed."""
    defs = (S.lin_grad("p5sky", [(0, SKY[0]), (0.55, SKY[1]), (1, SKY[2])]) +
            S.rad_grad("p5sun", [(0, "#fff4cf", 0.95), (0.35, "#fde3a0", 0.55), (1, "#fde3a0", 0)]) +
            S.lin_grad("p5mead", [(0, "#b8cc82"), (1, "#97b862")]) +
            S.lin_grad("p5soil", [(0, "#b0805a"), (1, "#8f6440")]))
    b = S.rect_bg("url(#p5sky)") + '<circle cx="1820" cy="200" r="520" fill="url(#p5sun)"/>'
    sh = "#f2d3a8"
    b += S.g(S.cloud(330, 210, 300, 90, "#fdf3e2", seed=51, sw=3.0, shade_fill=sh) +
             S.cloud(1050, 130, 220, 70, "#fdf3e2", seed=52, sw=2.6, shade_fill=sh), filter="wobble")
    b += S.g(S.path(S.hill(-100, W + 100, 700, 150, seed=53, bumps=4), fill="#d8c79c", sw=2.4) +
             S.path(S.hill(-100, W + 100, 760, 110, seed=54, bumps=5), fill="#c4c58c", sw=2.6), filter="wobble")
    trees = ""
    for x, y, k in ((150, 742, 0.3), (380, 738, 0.24), (1560, 744, 0.26), (2000, 740, 0.3)):
        trees += PR.olive_tree(x, y, k, seed=int(x))
    trees += PR.stone_house(640, 770, 0.28, variant=2, time="day")
    b += PR._haze(trees, "#ead9b0", 0.35, 0.4)
    mead = S.smooth_path([(-100, 840), (400, 812), (900, 806), (1400, 818), (1900, 806), (W + 100, 812)],
                         closed=False) + f" L{W + 100},{H + 60} L-100,{H + 60} Z"
    b += S.g(S.path(mead, fill="url(#p5mead)", sw=3), filter="wobble")
    # field strips on the far meadow
    for i in range(5):
        y = 836 + i * 14
        b += (f'<path d="M{-80 + i * 40},{y} Q{W / 2},{y - 8} {W + 80},{y + 4}" fill="none" stroke="#a9c272" '
              f'stroke-width="5" opacity="0.6"/>')
    # the garden bed
    bed = S.smooth_path([(170, 950), (500, 922), (1000, 916), (1500, 918), (1990, 930), (2040, 956)], closed=False)
    bed += " Q1100,1000 170,950 Z"
    b += S.g(S.path(bed, fill="url(#p5soil)", sw=3.6), filter="wobble")
    for i in range(3):
        y = 934 + i * 14
        b += (f'<path d="M{260 + i * 30},{y} Q1100,{y - 18} {1950 - i * 30},{y}" fill="none" stroke="#7a5236" '
              f'stroke-width="3" opacity="0.5"/>')
    b += f'<ellipse cx="{PX}" cy="{PY - 8}" rx="54" ry="14" fill="#6e4a30" stroke="{INK}" stroke-width="2.6"/>'
    # flowers and tufts in the meadow in front
    rng = random.Random(8)
    fl = ""
    for _ in range(26):
        x = rng.uniform(40, W - 40)
        y = rng.uniform(1000, 1170)
        c = rng.choice(("#f2c14e", "#f09a8a", "#fbf3e0", "#c9a0e0"))
        r = rng.uniform(6, 10)
        fl += (f'<path d="M{f1(x)},{f1(y + 18)} L{f1(x)},{f1(y)}" stroke="{GREEN_D}" stroke-width="3"/>'
               + "".join(f'<circle cx="{f1(x + r * math.cos(a))}" cy="{f1(y + r * math.sin(a))}" r="{f1(r * 0.62)}" '
                         f'fill="{c}" stroke="{INK}" stroke-width="1.8"/>' for a in np.linspace(0, 2 * math.pi, 6)[:5])
               + f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r * 0.45)}" fill="#e8a33c"/>')
    for x, y, s_, v in ((60, 1120, 1.0, 0), (2050, 1110, 1.0, 1), (1000, 1176, 0.8, 2), (520, 1160, 0.8, 1)):
        fl += PR.grass_tuft(x, y, s_, v)
    b += S.g(fl, filter="wobble-fine")
    return doc(b, defs)


def garden_svg():
    return doc(S.g("".join(_veg(k, x, 930 + 6 * math.sin(x / 300), s) for k, x, s in GARDEN), filter="wobble-fine"))


def sunrays_svg():
    return doc(S.path(S.rays(1820, 200, 120, 520, n=14, width_deg=8), fill="#fff1c4", stroke=False,
                      extra='opacity="0.55"'))


def sleeve_svg():
    """A sleeve reaching in from the lower left to the wrist (drawn over the hand prop's wrist edge), with a
    rolled cuff and a woven stripe."""
    st = f'stroke="{INK}" stroke-width="{f1(4 / HK)}" stroke-linejoin="round" stroke-linecap="round"'
    b = (f'<path d="M-980,250 Q-560,120 -196,14 L-180,118 Q-520,250 -900,420 Z" fill="#c9a86a" {st}/>'
         f'<path d="M-700,250 Q-460,150 -230,80" fill="none" stroke="#a88a52" stroke-width="{f1(3 / HK)}" '
         f'opacity="0.7"/>'
         f'<path d="M-232,6 Q-200,-4 -170,6 Q-150,62 -164,124 Q-196,134 -224,124 Q-246,62 -232,6 Z" fill="#d9bc80" {st}/>'
         f'<path d="M-214,8 Q-232,64 -210,126" fill="none" stroke="#3f7282" stroke-width="{f1(9 / HK)}"/>'
         f'<path d="M-188,12 Q-174,62 -184,120" fill="none" stroke="#b39360" stroke-width="{f1(2.4 / HK)}"/>')
    return f'<g transform="translate({f1(HX)},{f1(HY)}) scale({HK})" filter="url(#wobble-fine)">{b}</g>'


def hand_svg(sparkle=1.0, seed=True):
    b = PR.mustard_seed(HX, HY, HK, 1, sparkle=sparkle) + sleeve_svg()
    if not seed:   # the seed has gone: paint the palm over it
        sx, sy = HSEED
        skin = "#d9a37a"
        b += (f'<ellipse cx="{f1(sx)}" cy="{f1(sy)}" rx="{f1(8 * HK)}" ry="{f1(6.5 * HK)}" '
              f'fill="{S.mix(skin, S.shade(skin, -0.06), 0.5)}"/>')
    return b


def seed_svg():
    sx, sy = HSEED
    return doc(f'<ellipse cx="{f1(sx)}" cy="{f1(sy)}" rx="{f1(4.5 * HK)}" ry="{f1(3.6 * HK)}" fill="#4a2e1c" '
               f'stroke="{INK}" stroke-width="2"/><circle cx="{f1(sx - 2)}" cy="{f1(sy - 2)}" r="2.2" fill="#c9a06a"/>')


def raincloud_svg():
    return doc(S.g(S.cloud(PX, 455, 400, 120, "#d3d9e2", seed=57, sw=3.4, shade_fill="#aab6c6"), filter="wobble"))


def rain_svg(k):
    rng = random.Random(70 + k)
    b = ""
    for _ in range(40):
        x = rng.uniform(PX - 170, PX + 170)
        y = rng.uniform(520, 900)
        b += (f'<path d="M{f1(x)},{f1(y)} l-5,24" stroke="#7fa6cc" stroke-width="5" stroke-linecap="round"/>'
              f'<path d="M{f1(x)},{f1(y)} l-5,24" stroke="#d9ecf8" stroke-width="2" stroke-linecap="round"/>')
    for _ in range(5):                       # little splashes on the bed
        x = rng.uniform(PX - 150, PX + 150)
        y = PY - 6 + rng.uniform(-6, 6)
        b += f'<path d="M{f1(x - 9)},{f1(y)} q4,-9 9,-2 q5,-7 9,2" fill="none" stroke="#7fa6cc" stroke-width="3"/>'
    return doc(b)


def plant_svg(g):
    return doc(PR.mustard_plant(PX, PY, PK, growth=g))


def nest_svg(i, build=1.0, eggs=0):
    x, y = NESTS[i]
    return doc(PR.nest(x, y + 6, 0.75, 1 if i % 2 else -1, eggs=eggs, build=build))


def page_static_svg(final=False):
    """The whole page flattened (for the opening and closing iris)."""
    return page_bg_svg()


# ------------------------------------------------------------------ the page frame (output space)


def page_frame_image():
    """A deckled cream margin with a soft painted inner edge, a thin double ochre line and leafy corner sprigs."""
    w, h = OUT_W, OUT_H
    m = 38
    rng = np.random.default_rng(3)
    inner = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(inner)
    d.rounded_rectangle([m, m, w - m, h - m], radius=40, fill=255)
    for _ in range(520):                      # deckle the inner edge
        side = rng.integers(4)
        r = rng.uniform(3, 7)
        j = rng.uniform(-4, 4)
        if side == 0:
            x, y = rng.uniform(m, w - m), m + j
        elif side == 1:
            x, y = rng.uniform(m, w - m), h - m + j
        elif side == 2:
            x, y = m + j, rng.uniform(m, h - m)
        else:
            x, y = w - m + j, rng.uniform(m, h - m)
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(255 * (rng.random() < 0.5)))
    inner = inner.filter(ImageFilter.GaussianBlur(3))
    a_margin = 255 - np.asarray(inner, np.float32)
    shade = np.asarray(inner.filter(ImageFilter.GaussianBlur(22)), np.float32)
    pool = np.clip((255 - shade) / 255 * 1.6, 0, 1) * (np.asarray(inner, np.float32) / 255)
    img = np.zeros((h, w, 4), np.float32)
    paper = np.array((246, 238, 220), np.float32)
    warm = np.array((200, 150, 90), np.float32)
    img[..., :3] = paper
    img[..., 3] = a_margin
    # a soft warm pooled edge just inside the margin
    img[..., :3] = paper * (1 - pool[..., None] * 0.0) + 0
    edge = Image.fromarray(np.dstack([np.broadcast_to(warm, (h, w, 3)), pool * 120]).astype(np.uint8), "RGBA")
    out = Image.fromarray(img.astype(np.uint8), "RGBA")
    out = Image.alpha_composite(edge, out)
    d = ImageDraw.Draw(out)
    for k, wdt in ((54, 3), (62, 2)):
        d.rounded_rectangle([k, k, w - k, h - k], radius=34, outline=(196, 150, 84, 230), width=wdt)
    for cx, cy, sx, sy in ((80, 80, 1, 1), (w - 80, 80, -1, 1), (80, h - 80, 1, -1), (w - 80, h - 80, -1, -1)):
        for j, (ax, ay, ang) in enumerate(((30, 4, 20), (8, 30, 70), (22, 22, 45))):
            x, y = cx + sx * ax, cy + sy * ay
            leaf = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
            ld = ImageDraw.Draw(leaf)
            ld.ellipse([14, 22, 46, 38], fill=(134, 172, 88, 255), outline=(90, 70, 50, 255), width=2)
            leaf = leaf.rotate(-ang * sx * sy, resample=Image.BICUBIC)
            out.alpha_composite(leaf, (int(x - 30), int(y - 30)))
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(242, 193, 78, 255), outline=(110, 80, 50, 255), width=2)
    return out


def frame_fx(alpha_fn):
    img = page_frame_image()
    alpha = img.getchannel("A")

    def fx(frame, t, view):
        a = float(alpha_fn(t))
        if a <= 0.003:
            return frame
        if a >= 0.997:
            frame.alpha_composite(img)
            return frame
        im = img.copy()
        im.putalpha(alpha.point(lambda v, a=a: int(v * a)))
        frame.alpha_composite(im)
        return frame
    return fx


# ------------------------------------------------------------------ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    at = timer(ctx)
    rng = random.Random(5)
    t_jesus = at(0, "耶稣")
    t_tiny = at(0, "小小种子")
    t_story = at(0, "故事")
    t_mz = at(1, "芥菜种")
    t_min1 = at(1, "最小")
    t_min2 = at(1, "最小最小", 2)
    t_seedw = at(1, "的种子", 1)
    t_but = at(1, "可是")
    t_plant = at(1, "种在", 0)
    t_soil = at(1, "地里")
    t_it = at(1, "它会")
    t_g1 = at(1, "长啊长")
    t_g2 = at(1, "长啊长", 1)
    t_g3 = at(1, "长啊长", 2)
    t_g4 = at(1, "长大了")
    t_g5 = at(1, "比所有")
    t_veg = at(1, "所有的菜")
    t_g6 = at(1, "都大")
    t_g7 = at(1, "都大", 1)
    t_birds = at(1, "小鸟")
    t_on = at(1, "在它的")
    t_branch = at(1, "枝子")
    t_nest = at(1, "做窝")
    t_nest2 = at(1, "做窝", 1)
    t_heard = at(2, "大家听了")
    t_nod1 = at(2, "点点头")
    t_nod2 = at(2, "点点头", 1)
    t_smile = at(2, "笑了")

    t_open0, t_open1 = t_story - 0.02, t_story + 0.85        # the iris opening from Jesus' hand
    t_close0 = ctx.lines[1].end + 0.12
    t_close1 = min(t_heard - 0.05, t_close0 + 0.75)

    # ================================================================ the shore (s04's set)
    bm = S4.boat_motion((), g0=0.0)
    S4.add_shore(sc, T, rng, bm)
    sc.add("tufts", [S4.tufts_svg(k) for k in range(3)], z=40, frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.6) % 4]))
    jbd = lambda n: C.jesus(SEAT[0], SEAT[1], S4.BK, -1, pose=n.split("|")[0], expr=n.split("|")[1])
    jb = Actor("jesus_boat", jbd, SEAT, S4.BK, 12, seed=71, carrier=bm)
    jb.cut(0, "teach|smile")
    jb.cut(t_jesus - 0.1, "sit|warm")
    jb.cut(t_tiny - 0.12, "teach|smile")
    jb.cut(t_close1 + 0.2, "teach|smile", dip_=False)
    jb.cut(t_nod1 - 0.1, "sit|smile")
    jb.add_blinks({"sit|warm": f"sit|{blink('warm')}"}, T, rng)
    jb.mots += [M.breathe(0.01, 3.0, pivot=SEAT)]
    jb.build(sc)

    t_rise = snap(t_smile - 0.06)

    def crowd_extra(cid, a):
        x, y = a.piv
        seated = a.ents[0][1].startswith("sit")
        amp = 4.5 if seated else 2.5
        ph = rng.uniform(0, 0.08)
        a.mots.append(lambda t, x=x, y=y, ph=ph, amp=amp: Tf(rot=amp * (
            math.sin(math.pi * min(1.0, max(0.0, (t - t_nod1 - ph) / 0.2))) +
            math.sin(math.pi * min(1.0, max(0.0, (t - t_nod2 - ph) / 0.2)))), px=x, py=y))
        base = a.ents[0][1]
        pose = base.split("|")[0]
        if cid == "F4":       # the little girl who becomes a growing tree: up from the sand, arms up, swaying
            a.cut(t_rise, "cheer|happy", dip_=False)
            a.mots.append(lambda t: Tf(
                sy=1.0 if t < t_rise else 0.5 + 0.5 * M.ease("back")(min(1.0, (t - t_rise) / 0.55)),
                sx=1.0 if t < t_rise else 1.1 - 0.1 * min(1.0, (t - t_rise) / 0.55),
                rot=0.0 if t < t_rise + 0.55 else 5.0 * math.sin(2 * math.pi * (t - t_rise - 0.55) / 1.7),
                px=x, py=y))
            return
        a.cut(t_smile - 0.05 + rng.uniform(0, 0.3), f"{pose}|{'smile' if rng.random() < 0.6 else 'happy'}",
              depth=3)

    actors = S4.add_crowd(sc, T, {"press": -1.0}, rng, seated_from=0.0, extra=crowd_extra)
    for a in actors.values():
        a.build(sc)
    sc.fx.append(FX.sparkles((PALM[0] - 40, PALM[1] - 50, PALM[0] + 40, PALM[1] + 20), count=5, t0=t_tiny - 0.1,
                             t1=t_open1, size=(8, 15), period=0.9, drift=-6, seed=21))

    # ================================================================ the story page (z 60+)
    vis = lambda t: 1.0 if t_open1 <= t < t_close0 else 0.0
    gate = lambda m: (lambda t: Tf(alpha=0.0) if not vis(t) else m(t)) if m else (lambda t: Tf(alpha=vis(t)))

    def iris(t):
        cx, cy = PALM
        if t < t_open1:
            u = M.progress(t, t_open0, t_open1, "in")
        elif t < t_close0:
            u = 1.0
        else:
            u = 1 - M.progress(t, t_close0, t_close1, "out")
        return {"mode": "radial", "frac": max(0.001, 1.08 * u), "soft": 26, "cx": cx, "cy": cy}

    # the flattened page for the two iris transitions: opening (the hand with the seed), closing (the tree with nests)
    open_b = page_bg_svg().replace("</svg>", "")
    garden = S.g("".join(_veg(k, x, 930 + 6 * math.sin(x / 300), s) for k, x, s in GARDEN), filter="wobble-fine")
    rays_at = lambda t, a: S.path(S.rays(1820, 200, 120, 520, n=14, width_deg=8, rot=4 * t), fill="#fff1c4",
                                  stroke=False, extra=f'opacity="{0.55 * a:.3f}"')
    BIRDS = [("red", 0, -1), ("yellow", 1, 1), ("blue", 2, -1), ("green", 3, 1)]
    perch_pts = []
    for col, i, f in BIRDS:
        nx, ny = NESTS[i]
        perch_pts.append((nx - 66 * f, ny - 16))
    perched = "".join(PR.songbird(px, py, 0.62, f, pose="perch", color=col)
                      for (col, i, f), (px, py) in zip(BIRDS, perch_pts))
    nests_final = "".join(PR.nest(NESTS[i][0], NESTS[i][1] + 6, 0.75, 1 if i % 2 else -1, eggs=(2, 3, 2, 3)[i])
                          for i in range(4))
    sc.add("page_open", open_b + rays_at(t_open1, 0.75) + garden + f'<ellipse cx="{PX}" cy="{PY - 8}" rx="54" '
           f'ry="14" fill="#6e4a30"/>' + hand_svg(0.0) + "</svg>", z=90, reveal=iris,
           motion=lambda t: Tf(alpha=0.0 if t < t_open0 else 1 - M.progress(t, t_open1, t_open1 + 0.25, "linear")))
    sc.add("page_close", open_b + rays_at(t_close0, 1.0) + garden + PR.mustard_plant(PX, PY, PK, growth=1.0) +
           nests_final + perched + "</svg>", z=90, reveal=iris,
           motion=lambda t: Tf(alpha=M.progress(t, t_close0 - 0.25, t_close0, "linear") if t < t_close1 else 0.0))

    sc.add("page_bg", page_bg_svg(), z=60, motion=gate(None))
    sc.add("page_rays", sunrays_svg(), z=60.5, wc=0, motion=gate(lambda t: Tf(
        rot=4 * t, px=1820, py=200, alpha=0.75 + 0.25 * M.progress(t, t_it - 0.3, t_it + 0.6, "sine"))))
    sc.add("page_garden", garden_svg(), z=61, motion=gate(None))

    # the hand: sparkle pulses on '最小', tips on '可是', drops the seed on '种', withdraws
    hand_names = ["s0", "s1", "s2", "noseed"]
    hand_fr = [doc(hand_svg(0.0)), doc(hand_svg(0.5)), doc(hand_svg(1.0)), doc(hand_svg(0.0, seed=False))]
    t_drop = snap(t_plant)
    pulses = [t_min1, t_min2, t_seedw]

    def hand_fa(t):
        if t >= t_drop:
            return 3.0
        best = 0.0
        for tp in pulses:
            u = t - tp
            if 0 <= u < 0.7:
                best = max(best, (0, 1, 2, 2, 1, 1, 0)[min(6, int(u / 0.1))])
        return float(best)
    tip = lambda t: 14.0 * M.progress(t, t_but, t_drop - 0.05, "inout") * (1 - M.progress(t, t_drop + 0.3, t_drop + 0.8,
                                                                                         "sine"))
    t_away0, t_away1 = t_drop + 0.4, t_drop + 1.0

    def hand_m(t):
        a = M.progress(t, t_away0, t_away1, "in")
        return Tf(rot=tip(t), px=WRIST[0], py=WRIST[1], dx=-260 * a, dy=-560 * a,
                  alpha=1.0 - M.progress(t, t_away1 - 0.2, t_away1, "linear"))
    sc.add("page_hand", hand_fr, z=70, frame_at=hand_fa, motion=gate(hand_m), seed=91)

    # the falling seed: from the tipped palm into the hole in the bed
    def rot_pt(p, c, deg):
        r = math.radians(deg)
        x, y = p[0] - c[0], p[1] - c[1]
        return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))
    s0 = rot_pt(HSEED, WRIST, tip(t_drop))
    t_land = snap(t_drop + 0.5)

    def seed_m(t):
        if t < t_drop or t >= t_land:
            return Tf(alpha=0.0)
        u = (t - t_drop) / (t_land - t_drop)
        x = s0[0] + (PSEED[0] - s0[0]) * u
        y = s0[1] + (PSEED[1] - s0[1]) * u * u
        k = 1.5 - 0.9 * u
        return Tf(dx=x - HSEED[0], dy=y - HSEED[1], sx=k, sy=k, rot=300 * u, px=HSEED[0], py=HSEED[1])
    sc.add("page_seed", seed_svg(), z=69, motion=gate(seed_m), wc=0.4)

    # rain cloud and rain, then the sun
    t_rc0, t_rc1 = t_drop + 0.75, t_it + 0.55
    sc.add("page_cloud", raincloud_svg(), z=66, motion=gate(lambda t: Tf(
        dx=-560 * (1 - M.progress(t, t_rc0 - 0.6, t_rc0, "out")) + 640 * M.progress(t, t_rc1, t_rc1 + 1.1, "in"),
        alpha=M.progress(t, t_rc0 - 0.6, t_rc0 - 0.2, "linear") * (1 - M.progress(t, t_rc1 + 0.6, t_rc1 + 1.1,
                                                                                   "linear")))))
    sc.add("page_rain", [rain_svg(k) for k in range(3)], z=65, wc=0.3,
           frame_at=lambda t: float(int(t / 0.08) % 3),
           motion=gate(lambda t: Tf(alpha=M.progress(t, t_rc0, t_rc0 + 0.25, "linear") *
                                    (1 - M.progress(t, t_rc1 - 0.2, t_rc1 + 0.2, "linear")),
                                    dx=640 * M.progress(t, t_rc1, t_rc1 + 1.1, "in"))))

    # the plant: growth spurts keyed to the syllables (hard cuts through the in-between drawings + a springy stretch)
    spurts = [(t_land, 0), (t_g1, 2), (t_g2, 3), (t_g3, 7), (t_g4, 8), (t_g5, 9), (t_g6, 10), (t_g7, 11)]
    ents = [(0.0, 0)]
    prev = 0
    for ts, gi in spurts[1:]:
        ts = snap(ts - 0.04)
        for j, k in enumerate(range(prev + 1, gi + 1)):
            ents.append((snap(ts + 0.066 * j), k))
        prev = gi
    plant_fa = cuts(ents)
    spurt_ts = [snap(ts - 0.04) for ts, _ in spurts[1:]]

    def plant_m(t):
        if t < t_land:
            return Tf(alpha=0.0)
        s = 1.0
        for ts in spurt_ts:
            u = t - ts
            if 0 <= u < 0.45:
                s += 0.07 * math.sin(math.pi * u / 0.45) * (1 - u / 0.45)
        sw = 1.2 * math.sin(2 * math.pi * t / 3.4) * M.progress(t, t_g3, t_g3 + 1.0, "sine") * \
            (1 - M.progress(t, t_close0 - 0.9, t_close0 - 0.3, "sine"))
        return Tf(sx=2 - s, sy=s, rot=sw, px=PX, py=PY)
    sc.add("page_plant", [plant_svg(g) for g in GROWTH], z=64, frame_at=plant_fa, motion=gate(plant_m), seed=93)
    sc.add("page_hole", doc(f'<ellipse cx="{PX}" cy="{PY - 8}" rx="54" ry="14" fill="#6e4a30"/>'), z=63.5, wc=0,
           motion=gate(lambda t: Tf(alpha=1.0 - M.progress(t, t_land, t_land + 0.15, "linear"))))

    # nests (build twig by twig on '枝子', eggs on '做窝') and the birds
    for i in range(4):
        fr = [nest_svg(i, b) for b in (0.0, 0.3, 0.6, 1.0)] + [nest_svg(i, 1.0, e) for e in (1, 2, 3)]
        tb = t_branch + 0.12 * i
        eggs_n = (2, 3, 2, 3)[i]
        te = [t_nest + 0.08 * i, t_nest2 + 0.06 * i, t_nest2 + 0.3 + 0.06 * i]

        def nfa(t, tb=tb, te=te, eggs_n=eggs_n):
            if t < tb:
                return 0.0
            k = min(3, int((t - tb) / 0.12) + 1)
            if k < 3:
                return float(k)
            n = sum(1 for x in te if t >= x)
            return float(3 + min(n, eggs_n))
        sc.add(f"page_nest{i}", fr, z=68 + 0.01 * i, frame_at=nfa, seed=95 + i,
               motion=gate(lambda t, tb=tb, i=i: Tf(alpha=M.progress(t, tb, tb + 0.05, "linear"), rot=0.0)))
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for k, ((col, i, f), (lx, ly)) in enumerate(zip(BIRDS, perch_pts)):
        fly = [doc(PR.songbird(200, 200, 0.62, -f, wing=w, color=col)) for w in wings]
        sit = doc(PR.songbird(200, 200, 0.62, f, pose="perch", color=col))
        t0 = t_birds + 0.18 * k
        t_l = snap(t0 + 1.05 + 0.12 * k)
        sx0 = -160 if -f > 0 else W + 160
        sy0 = ly - 280 + 60 * k

        def bm_(t, t0=t0, t_l=t_l, sx0=sx0, sy0=sy0, lx=lx, ly=ly, k=k):
            if t < t0:
                return Tf(alpha=0.0)
            if t < t_l:
                u = (t - t0) / (t_l - t0)
                e = 1 - (1 - u) ** 2
                return Tf(dx=sx0 + (lx - sx0) * e - 200, dy=sy0 + (ly - sy0) * e - 90 * math.sin(math.pi * e) - 200)
            hop = 0.0
            for th in [x for x in (t_l + 0.9 + 0.2 * k, t_l + 1.9 + 0.3 * k) if x < t_close0 - 0.5]:
                if th <= t < th + 0.2:
                    hop = -10 * math.sin(math.pi * (t - th) / 0.2)
            return Tf(dx=lx - 200, dy=ly - 200 + hop)
        sc.add(f"page_bird{k}", fly + [sit], z=72 + 0.01 * k, wc=0.3, motion=gate(bm_),
               frame_at=lambda t, t_l=t_l, k=k: 8.0 if t >= t_l else float(int(t / 0.06 + 2 * k) % 8))

    sc.fx.append(FX.sparkles((PSEED[0] - 50, PSEED[1] - 260, PSEED[0] + 50, PSEED[1] - 10), count=7, t0=t_drop + 0.05,
                             t1=t_land + 0.5, size=(7, 13), period=0.5, drift=60, seed=34))
    sc.fx.append(FX.sparkles((HSEED[0] - 60, HSEED[1] - 60, HSEED[0] + 60, HSEED[1] + 40), count=6, t0=t_min1 - 0.1,
                             t1=t_but, size=(8, 16), period=0.8, drift=-8, seed=33))
    sc.fx.append(FX.sparkles((PX - 380, PY - 820, PX + 380, PY - 300), count=16, t0=t_g7 - 0.05, t1=t_g7 + 1.3,
                             size=(10, 20), period=0.7, drift=-14, seed=35))
    sc.fx.append(frame_fx(lambda t: M.progress(t, t_open1 - 0.3, t_open1 + 0.2, "sine") *
                          (1 - M.progress(t, t_close0 - 0.25, t_close0 + 0.05, "sine"))))

    # ================================================================ camera
    kids = Cam(880, 798, 1300)
    ck = [(0.0, Cam(930, 760, 1440), "sine"), (0.9, Cam(935, 756, 1430), "inout"),
          (t_tiny - 0.2, Cam(1120, 650, 1150), "sine"), (t_open0, Cam(1190, 630, 1060), "sine"),
          (t_open1, Cam(1200, 640, 1080), "inout"), (t_mz + 0.3, Cam(1180, 660, 1250), "sine"),
          (t_min2 - 0.15, Cam(1180, 662, 1260), "inout"), (t_min2 + 0.85, Cam(1160, 690, 1000), "sine"),
          (t_but - 0.1, Cam(1160, 695, 1000), "inout"), (t_it + 0.2, Cam(1170, 750, 1290), "inout"),
          (t_g3, Cam(1160, 720, 1500), "inout"),
          # step back with each growth spurt (长大了 / 比所有 / 都大) and hold between them: a pull-back while the
          # plant stands still would read as the plant shrinking
          (t_g4 - 0.05, Cam(1160, 720, 1500), "inout"), (t_g4 + 0.45, Cam(1145, 695, 1640), "inout"),
          (t_g5 - 0.05, Cam(1145, 695, 1640), "inout"), (t_g5 + 0.5, Cam(1105, 655, 1820), "inout"),
          (t_g6 - 0.05, Cam(1105, 655, 1820), "inout"),
          (t_g7 + 0.2, Cam(1056, 600, 2070), "sine"), (t_birds - 0.1, Cam(1056, 600, 2050), "inout"),
          (t_branch - 0.1, Cam(1190, 470, 1300), "sine"), (t_close0 - 0.3, Cam(1195, 480, 1260), "inout"),
          (t_close1, Cam(1150, 590, 1560), "sine"), (t_smile + 0.7, Cam(845, 818, 1180), "sine"),
          (T, Cam(840, 820, 1165), "sine")]
    sc.camera = M.cam_keys([(t, c) for t, c, _ in ck], [cv for _, _, cv in ck[:-1]])

    # ================================================================ sound
    sc.sfx("waves_calm", 0, dur=t_open1 + 0.4, gain_db=-16, fade_in=0.8, fade_out=0.8)
    sc.sfx("waves_calm", t_close0, dur=T - t_close0 + 0.3, gain_db=-16, fade_in=0.6, fade_out=1.0)
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-22, fade_in=0.8, fade_out=1.0)
    sc.sfx("sparkle", t_tiny, gain_db=-16)
    sc.sfx("whoosh", t_open0, gain_db=-17)
    sc.sfx("chime", t_open0 + 0.1, gain_db=-16)
    sc.sfx("sparkle", t_min1, gain_db=-17)
    sc.sfx("sparkle", t_min2, gain_db=-17)
    sc.sfx("pop", t_land, gain_db=-14)
    sc.sfx("rain", t_rc0, dur=t_rc1 - t_rc0 + 0.3, gain_db=-20, fade_in=0.3, fade_out=0.4)
    sc.sfx("grow", t_g1 - 0.1, gain_db=-15)
    sc.sfx("grow", t_g4 - 0.1, gain_db=-15)
    sc.sfx("sparkle", t_g7, gain_db=-15)
    sc.sfx("birds", t_birds, dur=t_close0 - t_birds + 0.4, gain_db=-15, fade_in=0.3, fade_out=0.6)
    for k, tn in enumerate((t_nest, t_nest2, t_nest2 + 0.3)):
        sc.sfx("pop", tn, gain_db=-18 - k, pan=0.1 * k)
    sc.sfx("whoosh", t_close0, gain_db=-19)
    sc.sfx("cloth", t_rise, gain_db=-17, pan=-0.3)
    return sc
