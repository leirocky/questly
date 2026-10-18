"""Scene 14 — the closing page: Daniel keeps praying; so can we, and God is always with us.

One 2700 x 1560 stage at dusk in Babylon, no cuts: Daniel's two-storey mud-brick house on the right with his open
upstairs window (props.upstairs_window, lamp-lit, he kneels facing west toward Jerusalem, where the sun is setting),
a neighbour's house on the left with a shuttered upstairs window, the city and palms behind, and in the
picture-book corner (bottom right) the friendly lion from the title, lying on the street looking up.

  '但以理不管遇到什么事，'   wide dusk page; the camera pushes in slowly on Daniel praying at his window.
  '都一直向上帝祷告。'       he bows his head over his folded hands (squash), then lifts it again.
  '小朋友，遇到害怕的事情，' the camera glides left to the neighbour's window: the shutters swing open and a little
                             girl peeks out at the dark evening, a bit worried.
  '我们也可以像但以理一样，向上帝祷告。'  she kneels and folds her hands (squash) like Daniel; a lamp glows up in her
                             room; she becomes peaceful; the camera pulls back to show both windows.
  '不管在哪里，上帝都会听我们的祷告，'  God's warm golden light spreads from the sky over the town (light only),
                             stars come out and twinkle high in the sky, and little windows light up all over the city,
                             one group after another; the camera widens to the whole page.
  '和我们在一起。'           Daniel and the girl smile, the second dove hops over to the first on the roof, the lion
                             curls up to sleep (little z's); the end card '但以理和狮子坑 · 完' fades in high in the
                             sky with a small heart (chime). Everything comes to rest: a still final frame for the
                             film's fade-out.

Pose / face changes are hard cuts sold by squashes; the window shutters open in quantised steps; lights and the
sky are lighting crossfades. God is never drawn as a person.
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

SW, SH = 2700, 1560
INK = P["ink"]
HORIZON = 1000
GS_ = 1230                   # the street
WIN_D = (1700, 760, 1.0)     # Daniel's upstairs window (sill centre x, y, scale)
WIN_C = (860, 870, 0.75)     # the neighbour's window
CHS = 0.85                   # the neighbour's child
CHILD_FLOOR = 80             # her floor below the sill, in window units (kneeling)
CHILD_STAND = 120            # (standing)
LION = (2310, GS_ + 8, 0.66)
CARD_X, CARD_Y = 1300, 300

PUNCT = "，。；：？！、,.;:?!"

def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ============================================================================ timing helpers


def snap(t, fps=30):
    """Put a hard cut in the middle of a frame interval."""
    return (math.floor(t * fps) + 0.5) / fps


def cuts(entries):
    entries = sorted(entries, key=lambda e: e[0])

    def fa(t):
        v = entries[0][1]
        for tk, i in entries:
            if t >= tk:
                v = i
        return float(v)
    return fa


def with_blinks(entries, blink_of, times, dur=0.13, guard=0.35):
    """Add blinks (hard cuts to an eyes-closed copy of the held drawing) at ``times`` unless a cut is near."""
    entries = sorted(entries, key=lambda e: e[0])
    out = list(entries)
    for tb in times:
        tb = snap(tb)
        if any(abs(tb - tk) < guard or abs(tb + dur - tk) < guard for tk, _ in entries):
            continue
        cur = None
        for tk, i in entries:
            if tk <= tb:
                cur = i
        if cur is None or cur not in blink_of:
            continue
        out += [(tb, blink_of[cur]), (snap(tb + dur), cur)]
    return sorted(out, key=lambda e: e[0])


def when(ctx, phrase):
    """Start time of ``phrase``: its chunk start, or its character position inside the chunk."""
    for ln in ctx.lines:
        for ch in ln.chunks:
            if phrase in ch.text:
                k = ch.text.index(phrase)
                if k == 0:
                    return ch.start
                body = ch.text.rstrip(PUNCT)

                def w(s):
                    return sum(0.5 if c in PUNCT else 1.0 for c in s)
                return ch.start + (ch.end - ch.start) * w(ch.text[:k]) / max(1.0, w(body))
    raise KeyError(phrase)


def hop(t0, keys, pivot, curves="sine"):
    return M.keys([(t0 + dt, d) for dt, d in keys], curves, pivot=pivot)


def dip(t0, s, pivot, depth=9.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return hop(t0, [(-0.14, {"dy": 0, "sy": 1}), (0, {"dy": depth * s, "sy": 0.95}),
                    (0.13, {"dy": -3 * s, "sy": 1.015}), (0.28, {"dy": 0, "sy": 1})], pivot, ["in", "out", "sine"])


def happy_hop(t0, s, pivot, h=18.0):
    return hop(t0, [(-0.1, {"dy": 0, "sy": 1}), (0, {"dy": 5 * s, "sy": 0.94}), (0.17, {"dy": -h * s, "sy": 1.04}),
                    (0.34, {"dy": 0, "sy": 0.97}), (0.46, {"dy": 0, "sy": 1})], pivot,
               ["in", "out", "in", "sine"])


def step_walk(t0, n, step, period, s, move=0.12, lift=7.0):
    """Planted-foot walk with two stride drawings: each drawing holds its anchor still; as the next cuts in, the
    anchor advances one stride with a short ease and a little lift. Returns (frame_at -> 0/1 or None, dx, dy, t_end)."""
    cut_t = [snap(t0 + k * period) for k in range(n)]
    t_end = snap(t0 + n * period)

    def fa(t):
        if t < cut_t[0] or t >= t_end:
            return None
        k = min(n - 1, int((t - t0) / period))
        return float(k % 2)

    def dx(t):
        return sum(step * M.progress(t, ck - move * 0.45, ck + move * 0.55, "sine") for ck in cut_t)

    def dy(t):
        y = 0.0
        for ck in cut_t:
            if ck - move * 0.45 <= t <= ck + move * 0.55:
                y -= lift * s * math.sin(math.pi * (t - ck + move * 0.45) / move)
        return y
    return fa, dx, dy, t_end


def clamp_cam(c, margin=4):
    h = c.w * 9 / 16
    x = min(max(c.x, c.w / 2 + margin), SW - c.w / 2 - margin)
    y = min(max(c.y, h / 2 + margin), SH - h / 2 - margin)
    return Cam(x, y, c.w)


def cam_path(keys):
    """[(t, Cam)] eased moves; the viewport's bottom edge is interpolated so the clamp never kinks a move."""
    keys = [(t, clamp_cam(c)) for t, c in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a), (t1, b) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, "sine")
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
        return keys[-1][1]
    return cam


# blink drawings (eyes-closed copies of the expressions that blink); setdefault keeps the shared table intact
for _e in ("happy", "neutral", "worried", "surprised", "call"):
    C.EXPRS.setdefault(f"d11_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))

C.EXPRS.setdefault("d14_smile", dict(C.EXPRS["peaceful"], mouth="grin"))



def trap(a=0.3):
    """Ease with a trapezoid velocity profile (sine ramps over the first and last ``a``, cruise between)."""
    def f(u):
        if u <= 0:
            return 0.0
        if u >= 1:
            return 1.0
        if u < a:
            s = u / 2 - a / (2 * math.pi) * math.sin(math.pi * u / a)
        elif u <= 1 - a:
            s = a / 2 + (u - a)
        else:
            w = 1 - u
            s = (1 - a) - (w / 2 - a / (2 * math.pi) * math.sin(math.pi * w / a))
        return s / (1 - a)
    return f


def cam_path2(keys):
    """[(t, Cam[, curve])]: eased moves (bottom edge interpolated, clamped to the stage)."""
    keys = [(k[0], clamp_cam(k[1]), k[2] if len(k) > 2 else "sine") for k in sorted(keys, key=lambda k: k[0])]

    def bottom(c):
        return c.y + c.w * 9 / 32

    def cam(t):
        if t <= keys[0][0]:
            return keys[0][1]
        if t >= keys[-1][0]:
            return keys[-1][1]
        for (t0, a, cv), (t1, b, _) in zip(keys, keys[1:]):
            if t0 <= t <= t1:
                u = M.progress(t, t0, t1, cv)
                w = M.lerp(a.w, b.w, u)
                yb = M.lerp(bottom(a), bottom(b), u)
                return clamp_cam(Cam(M.lerp(a.x, b.x, u), yb - w * 9 / 32, w))
        return keys[-1][1]
    return cam


# ============================================================================ drawings


def sky_svg():
    defs = S.lin_grad("sky14", [(0, "#36406e"), (0.33, "#6d5f93"), (0.62, "#c98a99"), (0.82, "#f0ad83"),
                                (1, "#f8cf92")])
    defs += S.rad_grad("sun14", [(0, "#fff0c4", 0.95), (0.3, "#fbd38e", 0.55), (1, "#f6b47e", 0)])
    body = (f'<rect x="-20" y="-20" width="{SW + 40}" height="{HORIZON + 60}" fill="url(#sky14)"/>'
            f'<circle cx="160" cy="{HORIZON + 10}" r="520" fill="url(#sun14)"/>'
            f'<circle cx="160" cy="{HORIZON + 30}" r="70" fill="#fbc56b" stroke="#e9925a" stroke-width="5" '
            f'filter="url(#wobble)"/>')
    return doc(body, defs)


def clouds_svg():
    out = ""
    for cx, cy, w, h, sd in ((520, 520, 420, 90, 1), (1150, 380, 300, 70, 2), (1900, 470, 380, 84, 3),
                             (2500, 330, 280, 64, 4), (850, 640, 260, 54, 5), (2250, 640, 240, 52, 6)):
        out += S.cloud(cx, cy, w, h, fill="#f3b7a0", seed=sd, sw=3, shade_fill="#b9839f")
    return doc(S.g(out, filter="wobble"))


def stars_svg():
    rng = random.Random(14)
    out = ""
    for _ in range(46):
        x, y = rng.uniform(0, SW), rng.uniform(20, 470)
        if CARD_X - 760 < x < CARD_X + 760 and CARD_Y - 190 < y < CARD_Y + 140:
            continue
        r = rng.uniform(2.5, 5.5)
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="#fff6d8"/>'
    # the evening star
    x, y = 2350, 210
    out += (f'<path d="M{x},{y - 26} L{x + 6},{y - 6} L{x + 26},{y} L{x + 6},{y + 6} L{x},{y + 26} L{x - 6},{y + 6} '
            f'L{x - 26},{y} L{x - 6},{y - 6} Z" fill="#fff3c8" stroke="{P["ink_soft"]}" stroke-width="2"/>')
    return doc(out)


def city_svg():
    """Babylon at dusk behind the two houses."""
    out = PR.nineveh_skyline(-60, SW + 60, HORIZON + 40, 0.75, seed=31, haze=0.45, tint="#c9a3b4")
    out += PR.palm_tree(1230, HORIZON + 120, 0.55, lean=0.1)
    out += PR.palm_tree(2420, HORIZON + 110, 0.5, lean=-0.15)
    return doc(out)


# little lit windows spread over the far city: 4 groups light up one after another ("不管在哪里")
CITY_LIGHTS = [[(70, 1010), (2290, 990), (1225, 985)],
               [(250, 960), (2420, 1030), (2620, 1000)],
               [(150, 1080), (2540, 950), (1240, 1070)],
               [(290, 1040), (2350, 1080), (2660, 1090)]]


def city_lights_svg(group):
    out = ""
    for x, y in CITY_LIGHTS[group]:
        out += (f'<circle cx="{x}" cy="{y}" r="26" fill="#ffd98c" opacity="0.35" filter="url(#soft)"/>'
                f'<rect x="{x - 9}" y="{y - 12}" width="18" height="24" rx="4" fill="#ffe3a0" stroke="{INK}" '
                f'stroke-width="2.5"/>')
    return doc(out)


def wall_brick(x0, x1, y0, y1, col, seed):
    rng = random.Random(seed)
    out = ""
    for _ in range(int((x1 - x0) * (y1 - y0) / 26000)):
        x, y = rng.uniform(x0 + 20, x1 - 70), rng.uniform(y0 + 20, y1 - 30)
        out += (f'<rect x="{f1(x)}" y="{f1(y)}" width="46" height="20" rx="3" fill="none" '
                f'stroke="{S.shade(col, -0.25)}" stroke-width="2.5" opacity="0.7"/>')
    return out


def houses_svg():
    """Daniel's two-storey house (right) and the neighbour's house (left), the street, a palm and plants."""
    out = ""
    col_d = "#cfa688"
    col_n = "#c49b84"
    # street
    defs = S.lin_grad("street14", [(0, "#c9a57c"), (1, "#b08b66")])
    out += S.path(f"M-20,{GS_} L{SW + 20},{GS_} L{SW + 20},{SH + 20} L-20,{SH + 20} Z", "url(#street14)", sw=4)
    rng = random.Random(2)
    for _ in range(50):
        x, y = rng.uniform(0, SW), rng.uniform(GS_ + 20, SH - 10)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(14, 28))}" ry="{f1(rng.uniform(5, 9))}" '
                f'fill="#bf9a72" stroke="{S.shade("#bf9a72", -0.25)}" stroke-width="2" opacity="0.8"/>')
    # neighbour's house (left)
    nx0, nx1, ntop = 330, 1170, 610
    out += S.path(f"M{nx0},{ntop} L{nx1},{ntop} L{nx1},{GS_} L{nx0},{GS_} Z", col_n, sw=4.5)
    out += wall_brick(nx0, nx1, ntop, GS_, col_n, 5)
    out += S.path(f"M{nx0 - 20},{ntop - 34} L{nx1 + 20},{ntop - 34} L{nx1 + 20},{ntop} L{nx0 - 20},{ntop} Z",
                  S.shade(col_n, -0.12), sw=4)
    for x in range(nx0 + 10, nx1, 70):
        out += f'<circle cx="{x}" cy="{ntop - 17}" r="9" fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="2.5"/>'
    out += (f'<path d="M{nx0 + 140},{GS_} L{nx0 + 140},{GS_ - 250} Q{nx0 + 215},{GS_ - 320} {nx0 + 290},{GS_ - 250} '
            f'L{nx0 + 290},{GS_} Z" fill="#7a5640" stroke="{INK}" stroke-width="4"/>')
    out += PR.jar(nx0 + 380, GS_ - 50, 0.55) + PR.bush(nx1 - 120, GS_ - 4, 0.5, variant=1)
    # Daniel's house (right): two storeys with an outside stair
    dx0, dx1, dtop = 1290, 2190, 420
    out += S.path(f"M{dx0},{dtop} L{dx1},{dtop} L{dx1},{GS_} L{dx0},{GS_} Z", col_d, sw=4.5)
    out += wall_brick(dx0, dx1, dtop, GS_, col_d, 9)
    out += S.path(f"M{dx0 - 20},{dtop - 36} L{dx1 + 20},{dtop - 36} L{dx1 + 20},{dtop} L{dx0 - 20},{dtop} Z",
                  S.shade(col_d, -0.12), sw=4)
    for x in range(dx0 + 10, dx1, 70):
        out += f'<circle cx="{x}" cy="{dtop - 18}" r="9" fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="2.5"/>'
    out += S.path(f"M{dx0},{GS_ - 330} L{dx1},{GS_ - 330}", sw=3, extra=f'stroke="{S.shade(col_d, -0.22)}"')
    # ground-floor door with a little lamp-lit glow under it
    out += (f'<path d="M{dx0 + 90},{GS_} L{dx0 + 90},{GS_ - 250} Q{dx0 + 165},{GS_ - 320} {dx0 + 240},{GS_ - 250} '
            f'L{dx0 + 240},{GS_} Z" fill="#6f4e3a" stroke="{INK}" stroke-width="4"/>')
    # outside stair up the right side
    for k in range(7):
        x = dx1 - 40 - 0 * k
        y = GS_ - 46 * (k + 1)
        out += (f'<rect x="{dx1 - 250 + 34 * k}" y="{y}" width="{250 - 34 * k}" height="46" fill="{S.shade(col_d, 0.06)}" '
                f'stroke="{INK}" stroke-width="3.5"/>')
        del x
    out += PR.jar(dx0 - 40, GS_ - 48, 0.55)
    out += PR.oil_lamp(dx0 + 280, GS_ - 4, 0.8, lit=True)
    for x, v in ((90, 2), (640, 0), (1250, 2), (1880, 1), (2600, 0), (1040, 1)):
        out += PR.grass_tuft(x, GS_ + 6, 0.7, variant=v)
    # a vine climbing beside Daniel's window
    vx = WIN_D[0] + 170
    out += S.path(f"M{vx},{GS_ - 330} C{vx + 30},{GS_ - 420} {vx - 20},{GS_ - 520} {vx + 10},{GS_ - 640}", sw=5,
                  extra=f'stroke="{P["leaf_dark"]}"')
    rng2 = random.Random(8)
    for k in range(9):
        yy = GS_ - 340 - k * 34
        xx = vx + 12 * math.sin(k * 1.3) + rng2.uniform(-6, 6)
        out += (f'<ellipse cx="{f1(xx + (14 if k % 2 else -14))}" cy="{f1(yy)}" rx="16" ry="10" fill="{P["leaf"]}" '
                f'stroke="{INK}" stroke-width="2.5" transform="rotate({30 if k % 2 else -30} {f1(xx)} {f1(yy)})"/>')
    out += PR.bush(dx0 + 330, GS_ - 4, 0.45, variant=3)
    # potted flowers on the sill line of the neighbour, a washing line between the roofs
    out += S.path(f"M{nx1 + 10},{ntop + 40} Q{(nx1 + dx0) / 2},{ntop + 90} {dx0 - 10},{ntop - 10}", sw=3)
    for k, x in enumerate((1195, 1235, 1270)):
        y = ntop + 60 + (k - 1) * -12
        col = ("#e6b45a", "#5f9a92", "#f0998a")[k]
        out += (f'<path d="M{x - 14},{y} L{x + 14},{y} L{x + 18},{y + 40} L{x - 18},{y + 40} Z" fill="{col}" '
                f'stroke="{INK}" stroke-width="2.5"/>')
    return doc(out, defs)


def god_light_svg():
    """God's presence: a warm golden light from the sky, soft rays over the town (never a figure)."""
    cx, cy = 1250, -120
    defs = S.rad_grad("gl14", [(0, "#fff0c0", 0.85), (0.5, "#ffe0a0", 0.35), (1, "#ffe0a0", 0)])
    body = (f'<ellipse cx="{cx}" cy="{cy + 200}" rx="1300" ry="700" fill="url(#gl14)"/>'
            f'<path d="{S.rays(cx, cy, 160, 1500, 11, 5, rot=40)}" fill="#fff0c4" opacity="0.4" filter="url(#soft)"/>')
    return doc(body, defs)


def in_window(markup, x, y, s, key):
    """Clip a figure to the window opening (so only what shows through the window is drawn)."""
    x0, top, x1, sill = PR.WINDOW_OPENING
    cid = f"win{key}"
    return (f'<clipPath id="{cid}"><rect x="{f1(x + x0 * s)}" y="{f1(y + top * s - 40)}" width="{f1((x1 - x0) * s)}" '
            f'height="{f1((sill - top) * s + 40 + 4)}"/></clipPath><g clip-path="url(#{cid})">{markup}</g>')


def window_glow_svg(x, y, s):
    defs = S.rad_grad(f"wg{int(x)}", [(0, "#ffdf9a", 0.7), (0.5, "#ffd38a", 0.25), (1, "#ffd38a", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y - 130 * s}" rx="{320 * s}" ry="{260 * s}" fill="url(#wg{int(x)})"/>', defs)


def card_svg():
    out = (f'<ellipse cx="{CARD_X}" cy="{CARD_Y - 40}" rx="760" ry="200" fill="url(#cardg)"/>' +
           S.text(CARD_X, CARD_Y, "但以理和狮子坑 · 完", size=132, fill="#fff3d6",
                  extra=f'stroke="{P["ink"]}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    defs = S.rad_grad("cardg", [(0, "#ffe9bb", 0.4), (0.6, "#ffd9a8", 0.14), (1, "#ffd9a8", 0)])
    return doc(out, defs)


def heart_svg(x, y, r):
    d = (f"M{x},{y + r * 0.9} C{x - r * 1.5},{y - r * 0.1} {x - r * 0.9},{y - r * 1.2} {x},{y - r * 0.45} "
         f"C{x + r * 0.9},{y - r * 1.2} {x + r * 1.5},{y - r * 0.1} {x},{y + r * 0.9} Z")
    return doc(S.g(f'<path d="{d}" fill="#e98a8a" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                   f'<ellipse cx="{x - r * 0.45}" cy="{y - r * 0.3}" rx="{r * 0.18}" ry="{r * 0.12}" fill="#fbd0c4"/>',
                   filter="wobble-fine"))


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    t_always = snap(L0.at("都一直") + 0.05)            # "都一直向上帝祷告": he bows his head in prayer
    t_up_again = snap(L0.end + 0.2)
    t_shut = L1.start + 0.35                          # the neighbour child's shutters open
    t_child = snap(t_shut + 0.5)                      # a worried child peeks out
    t_pray_c = snap(L1.at("我们也可以") + 0.1)          # "我们也可以像但以理一样": the child kneels and prays
    t_lamp = t_pray_c + 0.3                           # the child's lamp glows
    t_peace = snap(L1.at("我们也可以") + 1.6)
    t_god = L2.start                                  # "不管在哪里": light from heaven, city windows light up
    t_with = snap(L2.at("和我们在一起") + 0.05)          # "和我们在一起": warm glow, the lion settles to sleep
    t_card = L2.at("和我们在一起") + 0.6
    t_still = min(T - 1.4, L2.end + 0.2)              # everything comes to rest (the film fades out)

    # ---- camera ----
    CW = Cam(1330, 860, 2560)
    CDN = Cam(1660, 740, 1320)
    CCH = Cam(920, 830, 1420)
    CBO = Cam(1290, 800, 1900)
    CEND = Cam(1350, 830, 2500)
    sc.camera = cam_path2([(0, CW), (L0.start + 0.2, CW), (L0.end - 0.5, CDN), (L0.end - 0.1, CDN),
                           (t_pray_c - 0.15, CCH, trap(0.3)), (t_peace, CCH), (t_god - 0.1, CBO),
                           (t_with + 0.4, CEND), (T, CEND)])
    still = lambda t: 1.0 - M.progress(t, t_still - 0.6, t_still, "sine")      # noqa: E731  motion fades to rest

    # ---- sky ----
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("stars", stars_svg(), z=0.3, wc=0.2, motion=lambda t: Tf(alpha=M.progress(t, 3.0, t_god + 1.5, "sine")))
    sc.add("clouds", clouds_svg(), z=0.5, wc=0.6,
           motion=lambda t: Tf(dx=-7 * (min(t, t_still) - 0.0)))
    sc.add("god_light", god_light_svg(), z=0.7, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.9 * M.progress(t, t_god - 0.2, t_god + 1.6, "sine") *
                               (1 - 0.35 * M.progress(t, t_with + 0.6, t_still, "sine"))))
    sc.add("city", city_svg(), z=1)
    for gi in range(4):
        tg = t_god + 0.6 + 0.75 * gi
        sc.add(f"city_lights{gi}", city_lights_svg(gi), z=1.1, wc=0.3,
               motion=lambda t, tg=tg: Tf(alpha=M.progress(t, tg, tg + 0.5, "sine")))
    sc.add("houses", houses_svg(), z=2)

    # ---- the two upstairs windows ----
    wx, wy, ws = WIN_D
    cx_, cy_, cs = WIN_C
    sc.add("glow_d", window_glow_svg(wx, wy, ws), z=2.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.75 + 0.15 * math.sin(2 * math.pi * t / 2.7) * still(t)))
    sc.add("glow_c", window_glow_svg(cx_, cy_, cs), z=2.05, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.8 * M.progress(t, t_lamp, t_lamp + 0.8, "sine")))
    sc.add("win_d_back", doc(PR.upstairs_window(wx, wy, ws, 1.0, part="back", wall=False, glow=1.0)), z=2.1)
    sc.add("win_c_back", [doc(PR.upstairs_window(cx_, cy_, cs, 1.0, part="back", wall=False, glow=g))
                          for g in (0.0, 0.5, 1.0)], z=2.1,
           frame_at=lambda t: 2 * M.progress(t, t_lamp, t_lamp + 0.8, "sine"))
    # Daniel at his window, praying toward Jerusalem (west, the sunset side)
    fy = wy + PR.WINDOW_FLOOR_Y * ws
    dfr = [doc(in_window(C.daniel(wx + 8, fy, ws, -1, pose=p, expr=e), wx, wy, ws, "d"))
           for p, e in (("kneel_pray", None), ("kneel_bow", None), ("kneel_pray", "d14_smile"))]
    sc.add("daniel", dfr, z=2.2, frame_at=cuts([(0, 0), (t_always, 1), (t_up_again, 0), (snap(t_with + 0.2), 2)]),
           motion=M.combine(lambda t: Tf(sx=1 + 0.008 * math.sin(2 * math.pi * t / 3.2) * still(t),
                                         sy=1 + 0.008 * math.sin(2 * math.pi * t / 3.2) * still(t), px=wx, py=fy),
                            dip(t_always, ws, (wx, fy), 5), dip(t_up_again, ws, (wx, fy), 4)))
    # the neighbour's child: peeks out worried, then kneels and prays, at peace
    cfy = cy_ + CHILD_FLOOR * cs
    kid = lambda pose, expr=None, y=cfy: doc(in_window(C.citizen(cx_ + 4, y, CHS, -1, kind="child",  # noqa: E731
                                                                 variant=1, pose=pose, expr=expr), cx_, cy_, cs, "c"))
    cfr = [kid("stand", "worried", cy_ + CHILD_STAND * cs), kid("stand", "d11_blink_worried", cy_ + CHILD_STAND * cs),
           kid("kneel_pray", "worried"), kid("kneel_pray"), kid("kneel_pray", "d14_smile")]
    sc.add("child", cfr, z=2.2, frame_at=cuts(with_blinks([(0, 0), (t_pray_c, 2), (t_peace, 3), (snap(t_with + 0.35), 4)],
                                                         {0: 1}, [t_child + 0.9])),
           motion=M.combine(lambda t: Tf(alpha=0.0 if t < t_child else 1.0),
                            hop(t_child, [(0, {"dy": 40}), (0.25, {"dy": -4}), (0.4, {"dy": 0})], (cx_, cfy)),
                            dip(t_pray_c, CHS, (cx_, cfy), 6),
                            lambda t: Tf(sy=1 + 0.01 * math.sin(2 * math.pi * t / 2.9) * still(t), px=cx_, py=cfy)))
    sc.add("win_d_front", doc(PR.upstairs_window(wx, wy, ws, 1.0, part="front", wall=False)), z=2.3)
    opens = (0.0, 0.25, 0.5, 0.75, 1.0)
    sc.add("win_c_front", [doc(PR.upstairs_window(cx_, cy_, cs, o, part="front", wall=False)) for o in opens], z=2.3,
           frame_at=lambda t: float(min(4, max(0, int((t - t_shut) / 0.09) + 1))) if t >= t_shut else 0.0)

    # ---- doves on Daniel's roof: the second one hops up beside the first at the end ----
    roof = 384
    sc.add("dove_a", [doc(PR.dove(1560, roof - 36, 0.5, 1, pose="stand"))], z=2.4,
           motion=lambda t: Tf(dy=-3 * abs(math.sin(2 * math.pi * t / 2.2)) * still(t)))
    t_dv = snap(t_with + 0.3)
    sc.add("dove_b", doc(PR.dove(1760, roof - 36, 0.5, -1, pose="stand")), z=2.4, motion=M.combine(
        M.keys([(t_dv, {"dx": 0}), (t_dv + 0.45, {"dx": -120})], "inout"),
        hop(t_dv, [(0, {"dy": 0}), (0.22, {"dy": -40}), (0.45, {"dy": 0})], (1760, roof))))

    # ---- the friendly lion in the picture-book corner ----
    lx, ly, ls = LION
    lfr = [doc(C.ground_shadow(lx, ly, ls, 420) + PR.lion(lx, ly, ls, -1, pose="lie", eyes=e, tail=tl))
           for e in ("open", "closed") for tl in (-0.5, 0.0, 0.5)]
    lfr += [doc(C.ground_shadow(lx, ly, ls, 420) + PR.lion(lx, ly, ls, -1, pose="sleep", tail=0.3))]
    t_sleep = t_with + 0.5

    def lion_fa(t):
        if t >= t_sleep:
            return 6.0
        swish = 1 + round(math.sin(2 * math.pi * t / 2.4))
        blink = 1 if any(tb <= t < tb + 0.14 for tb in (2.2, 6.4, 10.1, 13.9)) else 0
        return float(blink * 3 + swish)
    sc.add("lion", lfr, z=3, frame_at=lion_fa, motion=M.combine(
        lambda t: Tf(sx=1 + 0.012 * math.sin(2 * math.pi * t / 3.4) * still(t),
                     sy=1 + 0.012 * math.sin(2 * math.pi * t / 3.4) * still(t), px=lx, py=ly),
        dip(t_sleep, ls, (lx, ly), 6)))
    sc.add("lion_z", [doc(f'<text x="{lx - 200 * ls + k * 4}" y="{ly - 230 * ls - k * 6}" font-family="LXGW WenKai" '
                          f'font-size="{40 + 6 * k}" fill="{P["ink_soft"]}">z</text>') for k in range(3)], z=3.1, wc=0,
           frame_at=lambda t: float(int(t * 2.5) % 3),
           motion=lambda t: Tf(alpha=M.progress(t, t_sleep + 0.4, t_sleep + 0.9) * still(t)))

    # ---- sparkles high in the sky while God's light shines (never on faces) ----
    sc.fx.append(FX.sparkles((300, 80, 2500, 430), count=22, t0=t_god + 0.2, t1=t_still, color=(255, 236, 170),
                             size=(8, 18), drift=6, seed=41))
    sc.fx.append(FX.vignette(lambda t: 0.35))

    # ---- end card ----
    sc.add("card", card_svg(), z=6, wc=0, motion=M.keys(
        [(t_card, {"alpha": 0, "s": 0.95, "dy": 16}), (t_card + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(CARD_X, CARD_Y - 50)))
    hx, hy = CARD_X, CARD_Y + 70
    th = t_card + 0.5
    sc.add("heart", heart_svg(hx, hy, 30), z=6.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))

    # ---- sound ----
    sc.sfx("night", 0.0, dur=T, gain_db=-17, fade_in=0.8, fade_out=1.5)
    sc.sfx("cloth", t_shut, gain_db=-14, pan=-0.3)
    sc.sfx("chime", t_god + 0.1, gain_db=-12)
    sc.sfx("sparkle", t_with + 0.1, gain_db=-16)
    sc.sfx("chime", t_card + 0.1, gain_db=-14)
    return sc
