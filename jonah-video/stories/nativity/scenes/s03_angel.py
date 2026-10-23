"""Scene 3 - Luke 1:26-38. Nazareth on a sunny morning: a little village of whitewashed cube houses climbing a
Galilean hillside among olive trees and cypresses; Mary walks home along the lane with a water jar on her shoulder and
goes in at her door. Inside, she sweeps the room; suddenly the room fills with warm heavenly light and the angel Gabriel
stands there, a tall gentle figure of light whose wings open; Mary jumps (the broom drops), the angel calms her and
gives God's message; Mary asks how this can be; the angel points up to God (light only); Mary bows and kneels: 'I am
the Lord's servant ... I am willing.'

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers through the Storm film's
Beats class, so a re-generated voice stays in sync; nothing is hard-coded to the take):
  0 .. 2.9     calm wide village page (the page-dip from s02 lands here): clouds drift, two birds cross the sky, the
               hens peck, the washing on the neighbour's roof flutters, smoke curls from a bread oven, a butterfly
               (rooster at the start, birdsong)
  '有一个小城'  Mary comes in from the left along the lane, the jar on her shoulder (planted-foot strides, footsteps);
  '善良的女孩'  the camera eases in after her
  '马利亚'      she stops by her door on '马' (squash) and smiles (blink), then steps in through the doorway and
               disappears behind the wall
  cut          (just before line 2) inside the house: Mary sweeps the woven mat (broom cycle, dust puffs)
  '亮起来了'    on '亮' the room fills with warm heavenly light (rays, motes; chime); she stops sweeping
  '一位天使'    on '天使' the angel appears in the light (fade + grow), his wings open in steps (whoosh, sparkle)
  '吓了一跳'    on '吓' Mary jumps back (startled, hop), the broom drops and clatters to the floor on '跳' (thud)
  '马利亚，不要怕' the angel lifts a calming hand (bless) on '马'; on '上帝很爱你' Mary relaxes (calm)
  '你要生'      the angel announces (proclaim); on '你要生' Mary lays a hand on her heart (listen_think)
  '耶稣'        a small warm burst of sparkles between them (sparkle)
  '他是上帝的儿子' wings_open with a gentle pulse of light
  line 4 (M)   Mary's question (question pose), the angel listens
  '这是上帝要做的事' bless; '在上帝' the angel raises his hand toward heaven, wings fully open, and a soft shaft of light
               pours down from above (light only, God is never drawn; chime)
  '我是上帝的使女' Mary bows her head, hands folded; '我愿意' she kneels, peaceful (sparkle); calm last frame for the page
               dip to s04.

Shared helpers for s04/s05 (same illustrator): village drawing (vhouse, olive, cypress, anemones, hen_svg, sky), the
blink expressions, planted-foot stepper, heart / pop helpers.
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
from stories.noah.scenes.s01_title import cuts, snap
from stories.storm.scenes.s03_friends import Beats, clamp_cam

INK = P["ink"]
CREAM = "#fff6e3"

# ---------------------------------------------------------------- blink expressions (closed-eye variants)
for _e in ("kind", "calm", "warm", "tender", "joyful", "happy", "awed", "peaceful", "weary", "worried", "sorry",
           "amazed", "thoughtful", "proclaim"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"n345b_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"n345b_{expr}"


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def f1(v):
    return f"{v:.1f}"


# ================================================================== motion helpers (shared with s04 / s05)


def stepper(times, step, s, lift=6.0, move=0.16):
    """Planted-foot walk: each drawing holds its anchor; at each cut time the anchor advances ``step`` px (a quick
    sine move of ``move`` s centred on the cut, with a little lift). Returns (dx(t), dy(t), n(t) = steps taken)."""
    ts = sorted(times)

    def dx(t):
        return sum(step * M.progress(t, tk - move * 0.45, tk + move * 0.55, "sine") for tk in ts)

    def dy(t):
        y = 0.0
        for tk in ts:
            if tk - move * 0.45 <= t <= tk + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - tk + move * 0.45) / move)
        return y

    def n(t):
        return sum(1 for tk in ts if t >= tk)
    return dx, dy, n


def dipm(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there); piv may be a function of t."""
    def m(t):
        u = t - t0
        if u < -0.14 or u > 0.3:
            return Tf()
        px, py = piv(t) if callable(piv) else piv
        if u < 0:
            k = M.ease("in")((u + 0.14) / 0.14)
            return Tf(dy=depth * s * k, sy=1 - 0.05 * k, px=px, py=py)
        if u < 0.13:
            k = M.ease("out")(u / 0.13)
            return Tf(dy=depth * s * (1 - k) - 3 * s * k, sy=0.95 + 0.065 * k, px=px, py=py)
        k = M.ease("sine")((u - 0.13) / 0.17)
        return Tf(dy=-3 * s * (1 - k), sy=1.015 - 0.015 * k, px=px, py=py)
    return m


def hopm(t0, s, piv, height=28.0, dur=0.4):
    """A little jump starting at t0 (crouch, lift, land)."""
    def m(t):
        u = t - t0
        if u < -0.1 or u > dur + 0.16:
            return Tf()
        px, py = piv(t) if callable(piv) else piv
        if u < 0:
            k = (u + 0.1) / 0.1
            return Tf(dy=4 * s * k, sy=1 - 0.05 * k, px=px, py=py)
        if u < dur:
            v = u / dur
            return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.04 * math.sin(math.pi * v), px=px, py=py)
        k = 1 - (u - dur) / 0.16
        return Tf(dy=3 * s * math.sin(math.pi * k), sy=1 - 0.035 * math.sin(math.pi * k), px=px, py=py)
    return m


def breathm(piv, period=2.8, amount=0.011, phase=0.0):
    def m(t):
        px, py = piv(t) if callable(piv) else piv
        v = math.sin(2 * math.pi * (t / period + phase))
        return Tf(sx=1 + 0.35 * amount * v, sy=1 + amount * v, px=px, py=py)
    return m


def gate(t0, t1):
    """Visible only for t0 <= t < t1 (hard cuts)."""
    return lambda t: Tf(alpha=1.0 if t0 <= t < t1 else 0.0)


def popm(t0, piv, dur=0.35, t_out=None, out_dur=0.25, wob=True):
    """Pop in at t0 (back-ease scale), optional pop out ending at t_out."""
    def m(t):
        if t < t0 or (t_out is not None and t > t_out):
            return Tf(alpha=0.0)
        u = min(1.0, (t - t0) / dur)
        k = 0.3 + 0.7 * M.ease("back")(u)
        a = min(1.0, (t - t0) / 0.1)
        if t_out is not None and t > t_out - out_dur:
            v = (t_out - t) / out_dur
            k *= 0.6 + 0.4 * v
            a *= v
        r = 5 * math.sin(2 * math.pi * (t - t0) / 2.2) if wob else 0.0
        return Tf(sx=k, sy=k, alpha=a, rot=r, dy=3 * math.sin(2 * math.pi * (t - t0) / 1.7), px=piv[0], py=piv[1])
    return m


def blinks_for(entries, times, blink_of):
    """Add 0.13 s blinks at the given times (where no cut is within 0.3 s) using blink_of[current frame]."""
    ents = sorted(entries)
    out = list(ents)
    for tb in times:
        tb = snap(tb)
        if any(abs(tb - tk) < 0.3 for tk, _ in out):
            continue
        cur = None
        for tk, i in ents:
            if tk <= tb:
                cur = i
        if cur is not None and cur in blink_of:
            out += [(tb, blink_of[cur]), (snap(tb + 0.13), cur)]
    return sorted(out)


# ================================================================== village drawing (shared with s04)
SKY = ("#86c1e0", "#aed6e8", "#d4ebee", "#f2efdc", "#f8ecd2")
WASH = PR.WHITEWASH
OCHRE = "#e4c48a"
SAGE = "#a3b07c"
SAGE_DARK = "#7d8c58"
CYPRESS = "#4e6b42"


def sky_svg(w=W, h=H, sun=(1880, 130), key="n3"):
    defs = (S.lin_grad(f"{key}sky", [(0, SKY[0]), (0.3, SKY[1]), (0.55, SKY[2]), (0.8, SKY[3]), (1, SKY[4])]) +
            S.rad_grad(f"{key}sun", [(0, "#fffbe6", 0.95), (0.3, "#fff2c4", 0.5), (1, "#fff2c4", 0)]))
    b = f'<rect x="-20" y="-20" width="{w + 40}" height="{h + 40}" fill="url(#{key}sky)"/>'
    if sun:
        b += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="520" fill="url(#{key}sun)"/>'
        b += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="62" fill="#fff6d0" opacity="0.9"/>'
    return b, defs


def clouds_markup(spec):
    sh = "#d9e8ee"
    return S.g("".join(S.cloud(x, y, cw, ch, "#fbf7ee", seed=sd, sw=3.2, shade_fill=sh) for x, y, cw, ch, sd in spec),
               filter="wobble")


def olive(x, y, s=1.0, seed=0, col=SAGE, dark=SAGE_DARK):
    """A silvery-green olive tree: a gnarled twin trunk and a lumpy canopy (anchor = the foot of the trunk)."""
    r = random.Random(seed)
    tw = 16 * s
    trunk = (f"M{f1(x - tw)},{f1(y)} Q{f1(x - tw * 0.4)},{f1(y - 60 * s)} {f1(x - 24 * s)},{f1(y - 120 * s)} "
             f"L{f1(x - 8 * s)},{f1(y - 126 * s)} Q{f1(x + 2 * s)},{f1(y - 80 * s)} {f1(x + 6 * s)},{f1(y - 60 * s)} "
             f"Q{f1(x + 18 * s)},{f1(y - 96 * s)} {f1(x + 34 * s)},{f1(y - 128 * s)} L{f1(x + 46 * s)},{f1(y - 120 * s)} "
             f"Q{f1(x + 26 * s)},{f1(y - 70 * s)} {f1(x + tw)},{f1(y)} Z")
    b = S.path(trunk, fill="#8a6a4c", sw=3.2 * s)
    b += S.path(f"M{f1(x - 4 * s)},{f1(y - 20 * s)} Q{f1(x)},{f1(y - 50 * s)} {f1(x - 6 * s)},{f1(y - 80 * s)}", sw=2 * s)
    b += S.cloud(x + 6 * s, y - 175 * s, 250 * s * r.uniform(0.9, 1.1), 120 * s, fill=col, seed=seed, puffs=5,
                 sw=3.4 * s, shade_fill=dark)
    for i in range(9):
        lx = x + r.uniform(-100, 110) * s
        ly = y - r.uniform(150, 240) * s
        b += f'<ellipse cx="{f1(lx)}" cy="{f1(ly)}" rx="{f1(9 * s)}" ry="{f1(4 * s)}" fill="#cfd8b0" opacity="0.8"/>'
    return S.g(b, filter="wobble-fine")


def cypress(x, y, h=200, w=34, col=CYPRESS, sw=2.8):
    d = (f"M{f1(x)},{f1(y)} Q{f1(x - w * 0.75)},{f1(y - h * 0.35)} {f1(x - w * 0.18)},{f1(y - h * 0.8)} "
         f"Q{f1(x)},{f1(y - h * 1.02)} {f1(x + w * 0.18)},{f1(y - h * 0.8)} Q{f1(x + w * 0.75)},{f1(y - h * 0.35)} "
         f"{f1(x)},{f1(y)} Z")
    return S.path(d, fill=col, sw=sw) + S.path(f"M{f1(x)},{f1(y - h * 0.1)} L{f1(x + w * 0.05)},{f1(y - h * 0.75)}",
                                                sw=sw * 0.6, extra='opacity="0.5"')


def anemone(x, y, s=1.0, col="#d8463c"):
    b = ""
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        b += f'<circle cx="{f1(x + 7 * s * math.cos(a))}" cy="{f1(y + 7 * s * math.sin(a))}" r="{f1(6 * s)}" fill="{col}"/>'
    b += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(4 * s)}" fill="#3a2a3a"/>'
    return (S.path(f"M{f1(x)},{f1(y + 4 * s)} L{f1(x)},{f1(y + 22 * s)}", sw=2.2 * s, extra=f'stroke="#5f8a40"') + b)


def vhouse(x, base, w, h, col=WASH, door="#5f7f9a", win=1, stair=0, seed=0, s=1.0, awning=None, dome=False,
           shutters="#5f97a8"):
    """A small whitewashed cube house of Nazareth (anchor = bottom-left of the front wall)."""
    r = random.Random(seed)
    side = S.shade(col, -0.16)
    d = 0.22 * w
    b = ""
    if stair:                                     # an outside stair up the left side
        n = stair
        for i in range(n):
            sh = h / n
            b += S.path(f"M{f1(x - 0.30 * w + i * 0.06 * w)},{f1(base - i * sh)} h{f1(0.30 * w)} v{f1(-sh)} "
                        f"h{f1(-0.30 * w)} Z", fill=S.shade(col, -0.05), sw=2.6 * s)
    b += S.path(f"M{f1(x + w)},{f1(base)} L{f1(x + w + d)},{f1(base - d * 0.45)} L{f1(x + w + d)},"
                f"{f1(base - h - d * 0.45)} L{f1(x + w)},{f1(base - h)} Z", fill=side, sw=3 * s)
    b += S.path(f"M{f1(x)},{f1(base)} h{f1(w)} v{f1(-h)} h{f1(-w)} Z", fill=col, sw=3 * s)
    for i in range(3):                            # soft whitewash blotches
        bx, by = x + r.uniform(0.15, 0.85) * w, base - r.uniform(0.2, 0.8) * h
        b += f'<ellipse cx="{f1(bx)}" cy="{f1(by)}" rx="{f1(w * 0.16)}" ry="{f1(h * 0.08)}" fill="{S.shade(col, -0.07)}" opacity="0.5"/>'
    b += S.path(f"M{f1(x - 4 * s)},{f1(base - h)} L{f1(x + w + 4 * s)},{f1(base - h)} L{f1(x + w + d + 4 * s)},"
                f"{f1(base - h - d * 0.45)} L{f1(x + d - 4 * s)},{f1(base - h - d * 0.45)} Z", fill=S.shade(col, -0.22),
                sw=2.6 * s)
    b += S.path(f"M{f1(x - 4 * s)},{f1(base - h - 8 * s)} h{f1(w + 8 * s)} v{f1(10 * s)} h{f1(-w - 8 * s)} Z",
                fill=S.shade(col, 0.1), sw=2.4 * s)
    for i in range(max(2, int(w / (34 * s)))):
        b += f'<circle cx="{f1(x + (16 + i * 34) * s)}" cy="{f1(base - h + 9 * s)}" r="{f1(4 * s)}" fill="{PR.NAT_WOOD_DARK}"/>'
    if dome:
        b += S.path(f"M{f1(x + w * 0.25)},{f1(base - h - 8 * s)} Q{f1(x + w * 0.25)},{f1(base - h - w * 0.45)} "
                    f"{f1(x + w * 0.5)},{f1(base - h - w * 0.48)} Q{f1(x + w * 0.75)},{f1(base - h - w * 0.45)} "
                    f"{f1(x + w * 0.75)},{f1(base - h - 8 * s)} Z", fill=S.shade(col, 0.05), sw=2.6 * s)
    if door:
        dw, dh = min(0.28 * w, 46 * s), min(0.62 * h, 92 * s)
        dx = x + w * r.uniform(0.18, 0.42)
        b += S.path(f"M{f1(dx)},{f1(base)} L{f1(dx)},{f1(base - dh + dw * 0.4)} Q{f1(dx + dw / 2)},{f1(base - dh - dw * 0.2)} "
                    f"{f1(dx + dw)},{f1(base - dh + dw * 0.4)} L{f1(dx + dw)},{f1(base)} Z", fill=door, sw=2.6 * s)
        if awning:
            ax0, ax1, ay = dx - 14 * s, dx + dw + 14 * s, base - dh - 4 * s
            b += S.path(f"M{f1(ax0)},{f1(ay)} L{f1(ax1)},{f1(ay)} L{f1(ax1 + 8 * s)},{f1(ay + 22 * s)} "
                        f"L{f1(ax0 - 8 * s)},{f1(ay + 22 * s)} Z", fill=awning, sw=2.4 * s)
    for k in range(win):
        wx = x + w * (0.62 + 0.2 * k) if win > 1 else x + w * 0.7
        wy = base - h * 0.62
        ww_, wh_ = 18 * s, 22 * s
        b += S.path(f"M{f1(wx - ww_ / 2)},{f1(wy - wh_ / 2)} h{f1(ww_)} v{f1(wh_)} h{f1(-ww_)} Z", fill="#5a4436", sw=2.2 * s)
        if shutters:
            for sx in (-1, 1):
                b += S.path(f"M{f1(wx + sx * ww_ / 2)},{f1(wy - wh_ / 2)} l{f1(sx * 9 * s)},{f1(-2 * s)} "
                            f"v{f1(wh_ + 4 * s)} l{f1(-sx * 9 * s)},{f1(-2 * s)} Z", fill=shutters, sw=1.8 * s)
    return b


def hen_svg(x, y, s=1.0, facing=1, peck=False, col="#f4ead8", seed=0):
    """A little round hen (anchor = ground between her feet); peck=True: head down to the ground."""
    f = facing
    comb, beak, leg = "#d8463c", "#f0b24a", "#e0a03c"
    b = ""
    for lx in (-6, 8):                                           # legs
        b += S.path(f"M{f1(x + lx * s)},{f1(y - 18 * s)} L{f1(x + lx * s)},{f1(y)} M{f1(x + (lx - 5) * s)},{f1(y)} "
                    f"L{f1(x + (lx + 6 * f) * s)},{f1(y)}", sw=2.4 * s, extra=f'stroke="{leg}"')
    body = (f"M{f1(x - 30 * s * f)},{f1(y - 40 * s)} Q{f1(x - 40 * s * f)},{f1(y - 64 * s)} {f1(x - 22 * s * f)},"
            f"{f1(y - 70 * s)} Q{f1(x - 10 * s * f)},{f1(y - 50 * s)} {f1(x + 4 * s * f)},{f1(y - 44 * s)} "
            f"Q{f1(x + 30 * s * f)},{f1(y - 46 * s)} {f1(x + 30 * s * f)},{f1(y - 28 * s)} Q{f1(x + 24 * s * f)},"
            f"{f1(y - 12 * s)} {f1(x)},{f1(y - 14 * s)} Q{f1(x - 26 * s * f)},{f1(y - 16 * s)} {f1(x - 30 * s * f)},{f1(y - 40 * s)} Z")
    b += S.path(body, fill=col, sw=3 * s)
    b += S.path(f"M{f1(x - 12 * s * f)},{f1(y - 34 * s)} Q{f1(x + 2 * s * f)},{f1(y - 24 * s)} {f1(x + 14 * s * f)},"
                f"{f1(y - 32 * s)}", sw=2.2 * s, extra=f'stroke="{S.shade(col, -0.35)}"')
    if peck:
        hx, hy = x + 36 * s * f, y - 14 * s
    else:
        hx, hy = x + 26 * s * f, y - 56 * s
    b += S.path(f"M{f1(x + 14 * s * f)},{f1(y - 38 * s)} L{f1(hx)},{f1(hy)}", sw=13 * s, extra=f'stroke="{INK}"')
    b += S.path(f"M{f1(x + 14 * s * f)},{f1(y - 38 * s)} L{f1(hx)},{f1(hy)}", sw=8 * s, extra=f'stroke="{col}"')
    b += f'<circle cx="{f1(hx)}" cy="{f1(hy)}" r="{f1(11 * s)}" fill="{col}" stroke="{INK}" stroke-width="{f1(2.6 * s)}"/>'
    b += S.path(f"M{f1(hx - 6 * s * f)},{f1(hy - 9 * s)} q{f1(3 * s * f)},{f1(-9 * s)} {f1(6 * s * f)},{f1(-2 * s)} "
                f"q{f1(3 * s * f)},{f1(-8 * s)} {f1(7 * s * f)},{f1(1 * s)}", fill=comb, sw=1.8 * s)
    b += S.path(f"M{f1(hx + 9 * s * f)},{f1(hy - 3 * s)} l{f1(9 * s * f)},{f1(3 * s)} l{f1(-9 * s * f)},{f1(3 * s)} Z",
                fill=beak, sw=1.6 * s)
    b += f'<ellipse cx="{f1(hx + 5 * s * f)}" cy="{f1(hy + 8 * s)}" rx="{f1(3 * s)}" ry="{f1(4.5 * s)}" fill="{comb}"/>'
    b += f'<circle cx="{f1(hx + 3 * s * f)}" cy="{f1(hy - 2 * s)}" r="{f1(2.2 * s)}" fill="{INK}"/>'
    return S.g(b, filter="wobble-fine")


def flyer_frames(color, s=0.42):
    return [doc(PR.songbird(200, 200, s, 1, wing=wv, color=color)) for wv in (1, .5, 0, -.5, -1, -.5, 0, .5)]


# ================================================================== s03 shot A: the village
HX, HY, HS = 1350, 880, 0.95        # Mary's house (nazareth_house exterior): anchor, scale
LANE_Y = 905                        # Mary walks along the lane in front of the house
DOOR_X1 = HX + PR.NAZARETH_DOOR[2] * HS     # right edge of the doorway (stage)
KM = 0.95                           # Mary's scale outside
MARY_STEP = 73                      # Mary walk_a <-> walk_b: the planted ankle moves 73 px (scale 1)


def village_back_svg():
    sky, defs = sky_svg()
    b = sky
    # far Galilean hills
    far = S.path(S.hill(-200, W + 200, 560, 110, seed=31, bumps=4), fill="#c3c8b8", sw=2.4)
    far += S.path(S.hill(-200, W + 200, 630, 80, seed=32, bumps=5), fill="#b4c09e", sw=2.6)
    far += "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#98a77e" opacity="0.7"/>'
                   for x, y in ((180, 600), (230, 606), (900, 590), (960, 598), (1500, 612), (1560, 606),
                                (1610, 616), (1900, 618)))
    b += S.g(far, filter="wobble")
    # the village hill (rising to the left) with terraces
    hill = [(-120, 330), (200, 322), (520, 392), (820, 470), (1120, 575), (1420, 690), (1800, 760), (2240, 790)]
    hd = S.smooth_path(hill, closed=False) + f" L2240,{H + 40} L-120,{H + 40} Z"
    defs += S.lin_grad("n3hill", [(0, "#cfc896"), (0.45, "#bdbb80"), (1, "#a8ae6c")])
    hb = S.path(hd, fill="url(#n3hill)", sw=3.4)
    b += S.g(hb, filter="wobble")
    rng = random.Random(5)
    cols = [WASH, "#efe3c8", "#f4ecdc", "#e9d9b8", "#efe6d2", "#f0dcc0"]
    doors = ["#5f7f9a", "#7a5a40", "#4f8f8a", "#9a6a42", "#5f7f9a", "#b8603e"]

    def base(x, r):
        return 722 - 0.2 * (1150 - x) - 62 * r
    # crest: olive trees along the top of the hill
    crest = ""
    for i, x in enumerate(range(-40, 900, 120)):
        yy = base(x, 3.75) + 8
        crest += olive(x + rng.uniform(-20, 20), yy, 0.34 + 0.04 * (i % 2), 60 + i, col="#a9b585", dark="#8a9864")
    b += crest
    hs = ""
    for r in (3, 2, 1, 0):
        k = 0.9 - 0.11 * r
        xx = -60 + rng.uniform(0, 60) * k
        x_end = 1160 - 150 * r
        # a terrace wall under the row
        tw = ""
        for x in range(-60, int(x_end) + 80, 40):
            tw += (f'<ellipse cx="{x}" cy="{f1(base(x, r) + 6)}" rx="{f1(22 * k)}" ry="{f1(9 * k)}" fill="#ddd0ae" '
                   f'stroke="{S.shade("#ddd0ae", -0.4)}" stroke-width="{f1(1.8 * k)}"/>')
        hs += tw
        i = 0
        while xx < x_end:
            w = rng.uniform(96, 146) * k
            h = rng.uniform(66, 100) * k
            y0 = base(xx + w / 2, r) + rng.uniform(-4, 4)
            if rng.random() < 0.22 and i > 0:                     # an olive tree in a gap
                hs += olive(xx + 40 * k, y0, 0.42 * k + 0.08, int(xx) + r)
                xx += 100 * k
                i += 1
                continue
            hs += vhouse(xx, y0, w, h, rng.choice(cols), door=rng.choice(doors), win=rng.choice((1, 1, 2)),
                         stair=4 if (i + r) % 4 == 1 else 0, seed=int(xx) + 7 * r, s=k, dome=rng.random() < 0.07,
                         awning=rng.choice((None, None, "#c9714a", "#5f97a8")))
            if rng.random() < 0.3:
                hs += cypress(xx + w + 18 * k, y0 + 2, rng.uniform(110, 160) * k, 26 * k, sw=2.2)
                xx += 26 * k
            xx += w + rng.uniform(26, 56) * k
            i += 1
    b += S.g(hs, filter="wobble-fine")
    # olive trees and cypresses at the foot of the village
    b += olive(1120, 660, 0.5, 12) + olive(1250, 700, 0.55, 13) + olive(40, 770, 0.55, 11)
    b += S.g(cypress(1190, 712, 180, 32) + cypress(1222, 716, 150, 28), filter="wobble-fine")
    return doc(b, defs)


def oven_svg():
    """A clay bread oven (tabun) beside the neighbour's house."""
    x, y = 1880, 905
    b = S.path(f"M{x - 70},{y} Q{x - 70},{y - 86} {x},{y - 92} Q{x + 70},{y - 86} {x + 70},{y} Z", fill="#c98a5a", sw=3.4)
    b += S.path(f"M{x - 28},{y} L{x - 28},{y - 34} Q{x},{y - 52} {x + 28},{y - 34} L{x + 28},{y} Z", fill="#5a3a2a", sw=3)
    b += f'<ellipse cx="{x}" cy="{y - 18}" rx="18" ry="10" fill="#f6a43c" opacity="0.8"/>'
    b += S.path(f"M{x - 16},{y - 92} h32 v-10 h-32 Z", fill="#b8794a", sw=2.6)
    return S.g(b, filter="wobble-fine")


def village_near_svg():
    """Mary's house, the neighbour's house with its washing line, the lane and the near ground."""
    b = ""
    # neighbour's house on the right (cut by the page edge)
    b += S.g(vhouse(1800, 880, 380, 300, "#efe3c8", door="#4f8f8a", win=2, seed=77, s=1.4, awning="#c9714a"),
             filter="wobble-fine")
    # Mary's house
    b += PR.nazareth_house(HX, HY, HS, 1, view="exterior", time="day")
    # the lane and the near ground
    defs = S.lin_grad("n3lane", [(0, "#ecd3a0"), (1, "#d9b47a")])
    defs += S.lin_grad("n3gnd", [(0, "#b7b46e"), (1, "#97a058")])
    gd = (f"M-60,{H + 40} L-60,930 Q400,948 900,936 Q1400,924 2200,930 L2200,{H + 40} Z")
    b += S.g(S.path(gd, fill="url(#n3gnd)", sw=0), filter="wobble")
    lane = "M-60,880 Q500,868 1000,878 Q1500,886 2200,880 L2200,950 Q1400,960 900,966 Q400,972 -60,958 Z"
    b += S.g(S.path(lane, fill="url(#n3lane)", sw=3.4), filter="wobble")
    rng = random.Random(9)
    peb = ""
    for i in range(26):
        x = rng.uniform(-40, 2150)
        y = rng.uniform(890, 955)
        peb += f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(5, 11))}" ry="{f1(rng.uniform(3, 6))}" fill="#c9a272" opacity="0.8"/>'
    b += peb
    b += oven_svg()
    return doc(b, defs)


def front_svg():
    """Foreground: the big olive tree on the left, a low stone wall, grass, red anemones."""
    b = ""
    stones = ""
    for i in range(9):
        x = -40 + i * 62
        stones += (f'<ellipse cx="{x}" cy="{1010 - (i % 2) * 6}" rx="40" ry="24" fill="{S.mix("#d8c39a", "#bba57c", (i % 3) / 2)}" '
                   f'stroke="{INK}" stroke-width="3.2"/>')
        stones += (f'<ellipse cx="{x + 30}" cy="{975 - (i % 2) * 4}" rx="34" ry="20" fill="{S.mix("#e2cfa8", "#c9b38a", (i % 2))}" '
                   f'stroke="{INK}" stroke-width="3"/>')
    b += S.g(stones, filter="wobble-fine")
    b += olive(250, 1040, 1.25, 21)
    rng = random.Random(4)
    fl = ""
    for i in range(30):
        x = rng.uniform(520, 2100)
        y = rng.uniform(985, 1170)
        fl += anemone(x, y, rng.uniform(0.8, 1.2), rng.choice(("#d8463c", "#e86a5a", "#f2f0e2", "#c9a6e0")))
    b += S.g(fl, filter="wobble-fine")
    for x, y, s_, v in ((620, 1000, 0.8, 0), (1000, 1010, 0.7, 2), (1500, 1000, 0.8, 1), (1960, 1010, 0.9, 0),
                        (2080, 990, 0.7, 2)):
        b += PR.grass_tuft(x, y, s_, variant=v)
    return doc(b)


def wash_line_svg(k):
    """Washing on a line on the neighbour's roof: 3 flutter phases."""
    x0, x1, y = 1840, 2150, 405
    b = S.path(f"M{x0},{y + 60} L{x0},{y - 6} M{x1},{y + 60} L{x1},{y - 6}", sw=6)
    b += S.path(f"M{x0},{y} Q{(x0 + x1) / 2},{y + 26} {x1},{y}", sw=2.4)
    cols = ("#c9714a", "#5f97a8", "#f2e6cc", "#e9c35c")
    for i, c in enumerate(cols):
        u = (i + 0.7) / (len(cols) + 0.4)
        cx = x0 + (x1 - x0) * u
        cy = y + 26 * 4 * u * (1 - u)
        cw, ch = 46, 58 + 8 * (i % 2)
        sk = 10 * math.sin(2 * math.pi * (k / 3 + i * 0.27))
        d = (f"M{f1(cx - cw / 2)},{f1(cy)} L{f1(cx + cw / 2)},{f1(cy)} L{f1(cx + cw / 2 + sk)},{f1(cy + ch)} "
             f"Q{f1(cx + sk)},{f1(cy + ch - 8)} {f1(cx - cw / 2 + sk)},{f1(cy + ch)} Z")
        b += S.path(d, fill=c, sw=2.6)
        b += f'<circle cx="{f1(cx - cw / 2 + 6)}" cy="{f1(cy)}" r="3" fill="{PR.NAT_WOOD}"/>'
    return doc(S.g(b, filter="wobble-fine"))


def smoke_svg():
    b = ""
    for i, (dx, dy, r) in enumerate(((0, 0, 16), (8, -26, 20), (-4, -56, 24))):
        b += f'<circle cx="{1880 + dx}" cy="{790 + dy}" r="{r}" fill="#efe9e0" stroke="{S.shade("#c9c0b4", -0.2)}" stroke-width="2.4"/>'
    return doc(S.g(b, filter="wobble-fine"))


def door_occluder_svg():
    """The front wall right of the doorway, drawn over Mary as she steps inside (clipped copy of the house)."""
    x1 = DOOR_X1
    cid = "n3occ"
    house = PR.nazareth_house(HX, HY, HS, 1, view="exterior", time="day")
    return doc(f'<clipPath id="{cid}"><rect x="{f1(x1)}" y="0" width="{f1(W - x1)}" height="{HY + 4}"/></clipPath>'
               f'<g clip-path="url(#{cid})">{house}</g>')


# ================================================================== s03 shot B: the room
IX, IY, IS = 1056, 900, 1.1         # nazareth_house interior anchor, scale
MX = 726                            # Mary sweeping
AX, AY = 1672, 905                  # the angel (in front of the corner broom)
LIGHT_LX = (AX - IX) / IS           # light_x (local)
KI = 1.1                            # people's scale inside


def room_extras(light):
    """Things added to Mary's room: a rolled sleeping mat leaning in the corner (over the house's own broom: Mary
    sweeps with that one), a woven hanging on the wall, a bunch of drying herbs."""
    b = ""
    # rolled reed mat in the corner
    cx, cy, ln, wd, rot = 1749, 586, 346, 88, 11.2
    mat = (f'<g transform="rotate({rot} {cx} {cy})">'
           f'<rect x="{cx - wd / 2}" y="{cy - ln / 2}" width="{wd}" height="{ln}" rx="18" fill="#dcc28a" stroke="{INK}" stroke-width="3.6"/>')
    for k, (yy, col) in enumerate(((-120, "#b8473c"), (-100, "#3f62a2"), (60, "#b8473c"), (80, "#3f62a2"))):
        mat += f'<rect x="{cx - wd / 2 + 2}" y="{cy + yy}" width="{wd - 4}" height="9" fill="{col}" opacity="0.85"/>'
    for yy in (-60, 0, 120):
        mat += f'<path d="M{cx - wd / 2 + 6},{cy + yy} q{wd / 2 - 6},10 {wd - 12},0" fill="none" stroke="#b89a5a" stroke-width="2.2"/>'
    mat += (f'<ellipse cx="{cx}" cy="{cy - ln / 2 + 6}" rx="{wd / 2}" ry="14" fill="#e8d4a4" stroke="{INK}" stroke-width="3.2"/>'
            f'<path d="M{cx},{cy - ln / 2 + 6} m-4,0 a4,3 0 1 1 8,0 a10,7 0 1 1 -20,0 a18,11 0 1 1 34,0" fill="none" '
            f'stroke="#a8884a" stroke-width="2"/>')
    mat += (f'<path d="M{cx - wd / 2},{cy - 20} q{wd / 2},14 {wd},0" fill="none" stroke="{PR.NAT_WOOD_DARK}" stroke-width="5"/>'
            f'<path d="M{cx + wd / 2 - 6},{cy - 16} q10,26 2,48" fill="none" stroke="{PR.NAT_WOOD_DARK}" stroke-width="4"/>')
    if light > 0:
        mat += (f'<rect x="{cx - wd / 2}" y="{cy - ln / 2}" width="{wd}" height="{ln}" rx="18" fill="{PR.LAMP_GLOW}" '
                f'opacity="{0.38 * light:.2f}"/>')
    mat += '</g>'
    b += mat
    # a woven hanging on the wall
    hx0, hx1, hy0, hy1 = 250, 440, 262, 560
    hang = f'<rect x="{hx0 - 16}" y="{hy0 - 12}" width="{hx1 - hx0 + 32}" height="14" rx="6" fill="{PR.NAT_WOOD}" stroke="{INK}" stroke-width="3"/>'
    hang += f'<path d="M{hx0},{hy0} L{hx1},{hy0} L{hx1 + 4},{hy1} L{hx0 - 4},{hy1} Z" fill="#c9714a" stroke="{INK}" stroke-width="3.4"/>'
    for k, (yy, col, hh) in enumerate(((300, "#e9c35c", 16), (336, "#3f62a2", 22), (380, "#f2e6cc", 12), (420, "#3f62a2", 22),
                                       (466, "#e9c35c", 16), (510, "#7a3a3a", 14))):
        hang += f'<rect x="{hx0 - 2}" y="{yy}" width="{hx1 - hx0 + 4}" height="{hh}" fill="{col}"/>'
    for i in range(5):
        xx = hx0 + 20 + i * 38
        hang += f'<path d="M{xx},{hy0 + 52} l14,14 l-14,14 l-14,-14 Z" fill="#f2e6cc" stroke="{S.shade("#c9714a", -0.3)}" stroke-width="2"/>'
    for i in range(10):
        xx = hx0 + 6 + i * (hx1 - hx0 - 12) / 9
        hang += f'<path d="M{xx:.1f},{hy1} l{(i % 3) - 1},26" stroke="#e9c35c" stroke-width="4" stroke-linecap="round"/>'
    hang += f'<path d="M{hx0},{hy0} L{hx1},{hy0} L{hx1 + 4},{hy1} L{hx0 - 4},{hy1} Z" fill="none" stroke="{INK}" stroke-width="3.4"/>'
    if light > 0:
        hang += f'<rect x="{hx0 - 6}" y="{hy0}" width="{hx1 - hx0 + 12}" height="{hy1 - hy0 + 26}" fill="{PR.LAMP_GLOW}" opacity="{0.22 * light:.2f}"/>'
    b += hang
    # drying herbs on a peg
    px, py = 1236, 238
    herbs = f'<circle cx="{px}" cy="{py}" r="7" fill="{PR.NAT_WOOD_DARK}" stroke="{INK}" stroke-width="2.4"/>'
    for k in range(6):
        a = -30 + 12 * k
        ex, ey = px + 90 * math.sin(math.radians(a)), py + 100 * math.cos(math.radians(a))
        herbs += f'<path d="M{px},{py + 6} Q{(px + ex) / 2 + 4},{(py + ey) / 2} {ex:.1f},{ey:.1f}" fill="none" stroke="#6f7f48" stroke-width="3"/>'
        for j in range(3):
            u = 0.45 + 0.2 * j
            lx, ly = px + (ex - px) * u, py + (ey - py) * u
            herbs += f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="9" ry="4" fill="#8a9a58" transform="rotate({a + 60} {lx:.1f} {ly:.1f})"/>'
    herbs += f'<path d="M{px - 12},{py + 14} h24" stroke="#b8473c" stroke-width="5"/>'
    b += herbs
    return S.g(b, filter="wobble-fine")


def interior_svg(light):
    return doc(PR.nazareth_house(IX, IY, IS, 1, view="interior", time="day", light=light, light_x=LIGHT_LX) +
               room_extras(light))


def angel_glow_svg():
    defs = S.rad_grad("n3ag", [(0, "#fffbea", 0.85), (0.4, "#fff3c8", 0.45), (1, "#fff0c0", 0)])
    return doc(f'<ellipse cx="{AX}" cy="{AY - 210 * KI}" rx="{360 * KI}" ry="{330 * KI}" fill="url(#n3ag)"/>', defs)


def rays_svg():
    cx, cy = AX, IY - 480 * IS
    defs = S.rad_grad("n3rg", [(0, "#fff8dc", 0.9), (0.5, "#fff0c0", 0.35), (1, "#fff0c0", 0)])
    b = f'<path d="{S.rays(cx, cy, 120, 1500, n=14, width_deg=5, rot=3)}" fill="#fff4cc" opacity="0.32"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="420" fill="url(#n3rg)"/>'
    return doc(b, defs)


def beam_svg():
    """A soft shaft of light pouring down from above (God's power: light only)."""
    defs = S.lin_grad("n3beam", [(0, "#fffbe8", 0.95), (0.6, "#fff0c0", 0.45), (1, "#fff0c0", 0)])
    x = AX - 40
    b = f'<path d="M{x - 150},-40 L{x + 150},-40 L{x + 420},{IY + 60} L{x - 420},{IY + 60} Z" fill="url(#n3beam)"/>'
    return doc(b, defs)


def broom_line(phase, x, y, s):
    """Stage points (top, bristle tip) of Mary's broom in the sweep pose (characters._broom_line)."""
    sn = math.sin(2 * math.pi * phase)
    T = (24 + 10 * sn, -214)
    B = (150 + 38 * sn, -6)
    return (x + T[0] * s, y + T[1] * s), (x + B[0] * s, y + B[1] * s)


def mary_svg(x, y, s, pose, expr=None, phase=0.0, facing=1, marks=True, pregnant=False, shadow=True):
    sh = C.ground_shadow(x, y, s, 110, 0.18) if shadow and pose not in ("ride",) else ""
    return doc(sh + C.mary(x, y, s, facing, pose=pose, expr=expr, phase=phase, marks=marks, pregnant=pregnant))


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    B = Beats(ctx)
    L = ctx.lines

    # ---------------------------------------------------------------- beats
    t_cheng = B.at(0, "有一个小城")
    t_ma0 = B.at(0, "名叫马利亚", 2)
    t_cut = snap(L[1].start - 0.3)                   # cut inside, just before '有一天'
    t_liang = B.at(1, "房间里忽然亮起来了", 5)
    t_tianshi = B.at(1, "一位天使", 2)
    t_xia = B.at(1, "马利亚吓了一跳", 3)
    t_tiao = B.at(1, "马利亚吓了一跳", 6)
    t_a_ma = L[2].start
    t_shangdi = B.at(2, "上帝很爱你")
    t_nisheng = B.at(2, "你要生一个儿子")
    t_yesu = B.at(2, "给他起名叫耶稣", 5)
    t_erzi = B.at(2, "他是上帝的儿子")
    t_q = L[3].start
    t_zhe = L[4].start
    t_zai = B.at(4, "在上帝")
    t_wo = L[5].start
    t_yuan = B.at(5, "我愿意")

    # ================================================================ SHOT B: the room (below shot A in z)
    sc.add("i_room", interior_svg(0.0), z=1, wc=0.9)
    t_l0, t_l1 = snap(t_liang - 0.15), snap(t_liang + 0.85)
    lfr = [interior_svg(1.0)]
    sc.add("i_light", lfr, z=1.1, wc=0.9,
           motion=lambda t: Tf(alpha=M.progress(t, t_l0, t_l1, "sine") *
                               (0.93 + 0.07 * math.sin(2 * math.pi * t / 3.1)) if t >= t_cut else 0.0))
    sc.add("i_rays", rays_svg(), z=1.2, wc=0, blend="screen",
           motion=lambda t: Tf(rot=3 * math.sin(2 * math.pi * t / 11.0), px=AX, py=IY - 480 * IS,
                               alpha=(M.progress(t, t_l0 + 0.3, t_l1 + 0.4, "sine") *
                                      (0.75 + 0.25 * math.sin(2 * math.pi * t / 2.6)) +
                                      0.35 * math.exp(-((t - t_erzi - 0.5) / 0.6) ** 2)) if t >= t_cut else 0.0))
    t_b0 = snap(t_zai - 0.05)
    sc.add("i_beam", beam_svg(), z=1.25, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=(M.progress(t, t_b0, t_b0 + 0.7, "sine") * (1 - 0.55 * M.progress(t, t_b0 + 2.4,
                                                                                                    t_b0 + 4.0, "sine")) *
                                      (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.9))) if t >= t_cut else 0.0))

    # ---- the angel
    t_app = snap(t_tianshi - 0.1)
    t_bless = snap(t_a_ma - 0.05)
    t_ann = snap(t_shangdi - 0.05)
    t_wo1 = snap(t_erzi - 0.05)
    t_listen = snap(t_q - 0.2)
    t_bless2 = snap(t_zhe - 0.05)
    t_up = snap(t_zai - 0.05)
    t_stand2 = snap(t_wo - 0.1)
    apose = [("stand", "warm", 0.05), ("stand", "warm", 0.25), ("stand", "warm", 0.45), ("stand", "warm", 0.65),
             ("bless", "warm", None), ("announce", "proclaim", None), ("wings_open", "proclaim", None),
             ("stand", "warm", 0.6), ("bless", "warm", 0.75), ("announce", "joyful", 1.0), ("stand", "joyful", 0.6)]
    NPH = 4
    afr = []
    for pose, ex, wg in apose:
        for k in range(NPH):
            afr.append(doc(C.ground_shadow(AX, AY, KI, 150, 0.12) +
                           C.angel(AX, AY, KI, -1, pose=pose, expr=ex, wings=wg, phase=k / NPH, glow=1.0)))
    open_steps = [snap(t_app + 0.08 * i) for i in range(4)]
    a_ents = [(0, 0)] + [(open_steps[i], i) for i in range(4)] + [(t_bless, 4), (t_ann, 5), (t_wo1, 6), (t_listen, 7),
                                                                   (t_bless2, 8), (t_up, 9), (t_stand2, 10)]
    a_base = cuts(a_ents)

    def a_fa(t):
        p = int(a_base(t))
        k = 0 if t < open_steps[-1] + 0.2 else int((t - t_app) / 0.19) % NPH
        return float(p * NPH + k)
    apiv = (AX, AY)
    sc.add("angel_glow", angel_glow_svg(), z=1.9, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, t_app - 0.1, t_app + 0.5, "sine") *
                               (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.3)), sx=1 + 0.03 * math.sin(2 * math.pi * t / 2.3),
                               sy=1 + 0.03 * math.sin(2 * math.pi * t / 2.3), px=AX, py=AY - 210 * KI))
    sc.add("angel", afr, z=2.0, frame_at=a_fa, seed=301,
           motion=M.combine(
               lambda t: Tf(alpha=M.progress(t, t_app, t_app + 0.55, "sine"),
                            sx=0.9 + 0.1 * M.progress(t, t_app, t_app + 0.6, "out"),
                            sy=0.9 + 0.1 * M.progress(t, t_app, t_app + 0.6, "out"),
                            dy=-6 * math.sin(2 * math.pi * t / 3.4), px=AX, py=AY),
               *[dipm(tc, KI, apiv, 6) for tc in (t_bless, t_ann, t_wo1, t_listen, t_bless2, t_up, t_stand2)],
               breathm(apiv, 3.2, 0.008)))

    # ---- Mary in the room
    sw_ph = [i / 6 for i in range(6)]
    mfr = [mary_svg(MX, IY, KI, "sweep", "kind", ph) for ph in sw_ph]               # 0-5 sweep cycle
    mfr += [mary_svg(MX, IY, KI, "sweep", "awed", 0.25, marks=False),             # 6 stopped, looking
            mary_svg(MX - 24, IY, KI, "startled", "startled"),                     # 7
            mary_svg(MX - 24, IY, KI, "stand", "calm"),                            # 8
            mary_svg(MX - 24, IY, KI, "listen_think", "thoughtful"),               # 9
            mary_svg(MX - 24, IY, KI, "question", "question"),                     # 10
            mary_svg(MX - 24, IY, KI, "stand", "awed"),                            # 11
            mary_svg(MX - 24, IY, KI, "bow", "calm"),                              # 12
            mary_svg(MX - 24, IY, KI, "kneel", "peaceful"),                        # 13
            mary_svg(MX - 24, IY, KI, "stand", blink("calm")),                     # 14
            mary_svg(MX - 24, IY, KI, "listen_think", blink("thoughtful")),        # 15
            mary_svg(MX - 24, IY, KI, "stand", "kind")]                            # 16
    t_stop = snap(t_liang + 0.05)
    t_jump = snap(t_xia)
    t_relax = snap(t_shangdi + 0.05)
    t_heart = snap(t_nisheng + 0.1)
    t_ask = snap(t_q - 0.05)
    t_awe = snap(t_zai + 0.15)
    t_bow = snap(t_wo + 0.05)
    t_kneel = snap(t_yuan - 0.05)
    m_ents = [(0, 6), (t_stop, 6), (t_jump, 7), (t_relax, 8), (t_heart, 9), (t_ask, 10), (snap(t_zhe + 0.3), 16),
              (t_awe, 11), (t_bow, 12), (t_kneel, 13)]
    m_ents = blinks_for(m_ents, [t_relax + 0.45, t_heart + 1.6, t_nisheng + 3.4, t_zhe + 1.2], {8: 14, 9: 15})
    m_base = cuts(m_ents)

    def m_fa(t):
        if t < t_stop:
            return float(int((t - t_cut) / 0.12) % 6)
        return m_base(t)
    mpiv = (MX, IY)
    sc.add("mary_in", mfr, z=2.2, frame_at=m_fa, seed=302,
           motion=M.combine(gate(t_cut, 1e9), hopm(t_jump, KI, (MX - 24, IY), 30, 0.36),
                            *[dipm(tc, KI, mpiv, 7) for tc in (t_relax, t_heart, t_ask, t_awe, t_bow, t_kneel)],
                            breathm(mpiv, 2.9, 0.01)))

    # ---- the broom drops when she jumps
    (bt, bb) = broom_line(0.25, MX, IY, KI)
    rot0 = math.degrees(math.atan2(bt[0] - bb[0], bb[1] - bt[1]))
    t_land = snap(max(t_tiao, t_jump + 0.42))
    sc.add("broom_fall", doc(PR.broom(bb[0], bb[1] + 4, KI * 0.97, rot=0.0)), z=2.3, seed=303,
           motion=lambda t: (Tf(alpha=0.0) if t < t_jump else
                             Tf(rot=rot0 + (-84 - rot0) * M.ease("in")(M.progress(t, t_jump, t_land, "linear")) +
                                (4 * math.sin(math.pi * min(1.0, (t - t_land) / 0.25)) if t > t_land else 0.0),
                                dx=60 * M.progress(t, t_jump, t_land, "out"), dy=34 * M.progress(t, t_jump, t_land, "in"),
                                px=bb[0], py=bb[1] + 4)))
    # tiny dust puff where it lands
    puff = doc(S.g("".join(f'<ellipse cx="{f1(bb[0] + 60 - 200 * KI + 30 * i)}" cy="{f1(IY + 30 - 6 * (i % 2))}" rx="{18 + 4 * (i % 2)}" '
                           f'ry="9" fill="#efe2c4" stroke="#c9b48e" stroke-width="2"/>' for i in range(4)), filter="wobble-fine"))
    sc.add("broom_puff", puff, z=2.31, wc=0,
           motion=lambda t: Tf(alpha=(max(0.0, 1 - (t - t_land) / 0.7) if t >= t_land else 0.0),
                               sx=1 + 0.4 * M.progress(t, t_land, t_land + 0.7), px=bb[0] + 60 - 155 * KI, py=IY + 30))

    # ---- sparkles, motes
    sc.fx.append(FX.sparkles((AX - 330, AY - 560, AX + 300, AY - 40), count=16, t0=t_app, color=(255, 244, 196),
                             size=(9, 18), period=1.7, drift=-6, seed=31))
    sc.fx.append(FX.motes((IX - 900, IY - 760, IX + 950, IY - 60), count=34, t0=t_l0, color=(255, 246, 214),
                          size=(3, 7), seed=33, alpha=130))
    t_ys = snap(t_yesu - 0.05)
    sc.fx.append(FX.sparkles((1060, 430, 1420, 700), count=12, t0=t_ys, t1=t_ys + 2.4, color=(255, 232, 160),
                             size=(10, 20), period=1.1, drift=-14, seed=35))
    sc.fx.append(FX.sparkles((MX - 140, IY - 420, MX + 160, IY - 120), count=8, t0=snap(t_yuan + 0.1), color=(255, 240, 190),
                             size=(8, 15), period=1.6, drift=-8, seed=37))
    sc.fx.append(FX.sparkles((AX - 260, 60, AX + 200, AY - 360), count=10, t0=t_b0 + 0.2, t1=t_b0 + 3.6, color=(255, 250, 225),
                             size=(8, 16), period=1.4, drift=18, seed=39))

    # ================================================================ SHOT A: the village (above shot B, gated)
    gA = gate(-1, t_cut)

    def addA(name, svg, motion=None, z=5.0, **kw):
        sc.add(name, svg, z=z, motion=M.combine(gA, motion) if motion else gA, **kw)

    addA("v_back", village_back_svg(), z=5.0, wc=0.9)
    addA("v_clouds", doc(clouds_markup([(420, 200, 330, 96, 41), (1250, 120, 260, 80, 42), (1700, 300, 200, 64, 43)])),
         z=5.05, motion=M.drift(vx=9))
    for i, (col, y0, vx, ph, t0) in enumerate((("brown", 260, 92, 0.0, 0.2), ("blue", 330, 80, 0.45, 1.6))):
        def fly(t, y0=y0, vx=vx, ph=ph, t0=t0, i=i):
            x = -240 + vx * (t - t0)
            return Tf(dx=x - 200, dy=y0 - 200 + 22 * math.sin(2 * math.pi * (t / 2.1 + ph)))
        addA(f"v_bird{i}", flyer_frames(col), z=5.06 + 0.01 * i, motion=fly, wc=0.3,
             frame_at=lambda t, ph=ph: float(int(t / 0.07 + ph * 8) % 8))
    addA("v_near", village_near_svg(), z=5.1, wc=0.9)
    addA("v_wash", [wash_line_svg(k) for k in range(3)], z=5.12,
         frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.32) % 4]))
    for i in range(3):
        def smoke(t, i=i):
            u = ((t / 2.6) + i / 3) % 1.0
            return Tf(dy=-90 * u, dx=14 * math.sin(2 * math.pi * u) + 10 * u, sx=0.7 + 0.8 * u, sy=0.7 + 0.8 * u,
                      alpha=0.85 * math.sin(math.pi * u), px=1880, py=790)
        addA(f"v_smoke{i}", smoke_svg(), z=5.13 + 0.001 * i, motion=smoke, wc=0)
    # hens pecking by the lane
    for i, (hx, hy, f, col, s_) in enumerate(((760, 935, 1, "#f4ead8", 0.95), (860, 950, -1, "#c9874a", 0.9),
                                              (1600, 940, -1, "#f4ead8", 0.85))):
        fr = [doc(C.ground_shadow(hx, hy, s_, 70, 0.15) + hen_svg(hx, hy, s_, f, False, col)),
              doc(C.ground_shadow(hx, hy, s_, 70, 0.15) + hen_svg(hx, hy, s_, f, True, col))]
        rng = random.Random(40 + i)
        pecks = []
        tt = 0.3 + 0.4 * i
        while tt < t_cut:
            pecks += [(snap(tt), 1), (snap(tt + 0.22), 0)]
            if rng.random() < 0.5:
                pecks += [(snap(tt + 0.36), 1), (snap(tt + 0.56), 0)]
            tt += rng.uniform(1.1, 2.0)
        addA(f"v_hen{i}", fr, z=5.21 + 0.01 * i, frame_at=cuts([(0, 0)] + pecks), seed=310 + i,
             motion=lambda t, hx=hx, hy=hy, i=i: Tf(dx=6 * math.sin(2 * math.pi * (t / 5.0 + i * 0.3)), px=hx, py=hy))
    # a butterfly over the flowers
    bfr = [doc(PR.butterfly(0 + 200, 200, 0.42, flap=fl, color="yellow" if "yellow" in getattr(PR, "BUTTERFLY_COLORS", {})
                            else "orange")) for fl in (0.0, 0.33, 0.66)]
    addA("v_fly", bfr, z=5.3, wc=0.3, frame_at=lambda t: float(int(t / 0.06) % 3),
         motion=lambda t: Tf(dx=1500 + 160 * math.sin(t / 1.9) - 200, dy=1020 + 50 * math.sin(t / 0.7) - 60 * math.cos(t / 2.3) - 200))

    # ---- Mary walks home with her water jar (frames drawn at her stopping spot X_STOP, moved by dx)
    X_STOP = 1155
    n_walk = 15
    step = MARY_STEP * KM                        # carry_jar_walk_a <-> _b: the planted foot stays put
    x_start = X_STOP - n_walk * step
    t_w0 = snap(t_cheng + 0.65)
    t_arrive0 = snap(t_ma0 - 0.2)
    per = (t_arrive0 - t_w0) / (n_walk - 1)
    walk_cuts = [snap(t_w0 + per * i) for i in range(n_walk)]
    t_arrive = walk_cuts[-1]
    t_stopm = snap(t_arrive + per)
    t_in0 = snap(max(t_ma0 + 0.55, t_stopm + 0.5))
    in_cuts = [t_in0, snap(t_in0 + 0.3), snap(t_in0 + 0.6)]
    dxw, dyw, nw = stepper(walk_cuts, step, KM, lift=6)
    dxi, dyi, ni = stepper(in_cuts, step, KM, lift=6)
    rise = lambda t: -25 * M.progress(t, in_cuts[0] - 0.08, in_cuts[0] + 0.1, "sine")   # noqa: E731  up onto the sill
    xm = lambda t: x_start + dxw(t) + dxi(t)                                               # noqa: E731
    afr_m = [mary_svg(X_STOP, LANE_Y, KM, "carry_jar_walk_a", "kind"),
             mary_svg(X_STOP, LANE_Y, KM, "carry_jar_walk_b", "kind"),
             mary_svg(X_STOP, LANE_Y, KM, "carry_jar", "happy"),
             mary_svg(X_STOP, LANE_Y, KM, "carry_jar", blink("happy"))]
    t_bl = snap(t_ma0 + 0.15)

    def mA_fa(t):
        if t < t_stopm:
            return float(nw(t) % 2)
        if t < in_cuts[0]:
            return 3.0 if t_bl <= t < t_bl + 0.14 else 2.0
        return float((ni(t) + 1) % 2)
    mApiv = lambda t: (xm(t), LANE_Y + rise(t))      # noqa: E731
    addA("mary_out", afr_m, z=5.2, frame_at=mA_fa, seed=320,
         motion=M.combine(lambda t: Tf(dx=xm(t) - X_STOP, dy=dyw(t) + dyi(t) + rise(t)), dipm(t_stopm, KM, mApiv, 6),
                          breathm(mApiv, 2.7, 0.01)))
    addA("v_occ", door_occluder_svg(), z=5.25, wc=0.9)
    addA("v_front", front_svg(), z=5.4, wc=0.9)

    # ================================================================ camera
    camA = M.cam_keys([(0, Cam(1150, 606, 1800)), (t_w0 + 1.2, Cam(1130, 612, 1760)),
                       (t_stopm + 0.2, Cam(1130, 640, 1620)), (t_cut, Cam(1190, 652, 1500))],
                      ["sine", "inout", "sine"])
    t_c1 = snap(t_l0 - 0.1)
    camB = M.cam_keys([(t_cut, Cam(870, 650, 1540)), (t_c1, Cam(885, 645, 1515)), (t_c1 + 1.9, Cam(1200, 660, 1600)),
                       (t_a_ma, Cam(1200, 660, 1600)), (L[2].end, Cam(1250, 650, 1560)),
                       (t_q + 0.2, Cam(1250, 650, 1560)), (L[3].end, Cam(1150, 668, 1560)),
                       (t_zhe, Cam(1150, 668, 1560)), (t_zai + 1.0, Cam(1220, 620, 1680)),
                       (t_wo, Cam(1220, 620, 1680)), (T, Cam(1160, 676, 1500))],
                      ["sine"] * 11)

    def cam(t):
        return clamp_cam(camA(t) if t < t_cut else camB(t))
    sc.camera = cam

    # ================================================================ sound
    sc.sfx("birds", 0, dur=t_cut + 0.4, gain_db=-16, fade_in=1.0, fade_out=0.5)
    sc.sfx("wind_soft", 0, dur=t_cut + 0.4, gain_db=-25, fade_in=1.0, fade_out=0.5)
    sc.sfx("rooster", 0.5, gain_db=-16, pan=0.3)
    sc.sfx("footsteps", t_w0 - 0.05, dur=t_arrive - t_w0 + 0.4, gain_db=-19, pan=-0.2, fade_in=0.3)
    sc.sfx("footsteps", in_cuts[0] - 0.05, dur=0.8, gain_db=-20, pan=0.2)
    sc.sfx("wind_soft", t_cut, dur=T - t_cut + 0.3, gain_db=-30, fade_in=0.4, fade_out=1.2)
    sc.sfx("cloth", t_cut + 0.15, gain_db=-22)
    sc.sfx("chime", t_l0, gain_db=-11)
    sc.sfx("sparkle", t_app, gain_db=-13)
    sc.sfx("whoosh", open_steps[1], gain_db=-17)
    sc.sfx("cloth", t_jump, gain_db=-15)
    sc.sfx("thud", t_land, gain_db=-13, pan=-0.2)
    sc.sfx("sparkle", t_ys, gain_db=-14)
    sc.sfx("chime", t_b0, gain_db=-12)
    sc.sfx("sparkle", t_yuan + 0.1, gain_db=-17)
    return sc
