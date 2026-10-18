"""Scene 13 — King Darius writes to all the peoples; his words go out to every land (Daniel 6:25-28).

One wide 5500 x 1300 stage seen as a picture-book panorama, plus a closing 'page' that dissolves in on top:
  A (left)   the king's audience portico (cedar beams, a blue glazed frieze of friendly lions, purple curtains,
             Persian bull-capital columns, a red runner): the king on his throne with the sealed letter, Daniel
             beside him, two messengers holding rolled letters;
  B (middle) the lands: snowy mountains, hills, a tent camp with camels, a city, a river with a little boat
             (a messenger on deck) and a road where another messenger walks with his letter;
  C (right)  another people's town: a wall with an open gate, the letter posted on a board, a herald reading it
             aloud, townspeople reading and listening.
  D (page)   afterwards: a golden afternoon on the palace garden terrace.

  '后来，大利乌王写信给…'  the king (sit_sign) presses his seal onto the letter (squash, twinkle, pop); Daniel
                         bows; '全国各地的人' the two messengers turn and stride out of the open portico, a herald's
                         horn sounds, and the camera glides out with them into the lands.
  K line                 '你们都要敬畏但以理的上帝！' over the lands: the boat sails, the far messenger walks on;
                         '他是永远活着的上帝。' the camera travels on to the town (a horn there); '他会拯救人，他救了
                         但以理，' the herald points to the letter and reads, the people nod; '脱离狮子的口。' they
                         cheer (one man kneels to pray).
  (page turn)            the closing page dissolves in: '从那以后，但以理一直平平安安，' Daniel reads a scroll on
                         the terrace with the king smiling beside him, doves fly over the garden; '做事都很顺利。'
                         he turns and explains to the king, who nods happily; a child waves. Slow push-in, calm end.

Pose and face changes are hard cuts sold by squashes / hops; walking uses planted-foot strides. The page dissolve
is a whole-picture crossfade (a page turn), never two poses of one figure.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 5500, 1300
INK = P["ink"]
GA = 1080                    # portico floor (region A)
GB = 1010                    # the road out in the lands (region B)
GC = 1040                    # the town square (region C)
TX = 620                     # the throne
KS = 1.0
GS = 0.95                    # messengers
CS = 0.85                    # townspeople
PORT_X1 = 1760               # where the portico opens onto the lands
COLS = (90, 1080, 1620)
MSG = ((1, 1200), (3, 1360))
TOWN_X0 = 3750
DECREE = (4380, 720)
PAGE = (3460, 5520, 100, SH + 20)   # the closing page's painted area (x0, x1, y0, y1)

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



# ============================================================================ drawings


def sky_svg():
    defs = S.lin_grad("sky13", [(0, "#86c0dc"), (0.6, "#c2e0e8"), (1, "#f3e7c4")])
    return doc(f'<rect x="-20" y="-20" width="{SW + 40}" height="{SH + 40}" fill="url(#sky13)"/>', defs)


CLOUDS = [(2100, 160, 360, 100, 1), (2900, 110, 300, 84, 2), (3600, 190, 380, 104, 3), (4400, 120, 320, 90, 4),
          (5200, 200, 300, 86, 5), (2500, 330, 200, 56, 6), (4000, 340, 220, 60, 7), (1500, 80, 260, 70, 8)]


def clouds_svg():
    out = "".join(S.cloud(cx, cy, w, h, fill="#fdf6ea", seed=sd, sw=3, shade_fill="#dfe6ea")
                  for cx, cy, w, h, sd in CLOUDS)
    return doc(S.g(out, filter="wobble"))


def lands_svg():
    """Far mountains, hills, towns of many peoples, the river and the road (behind the portico on the left)."""
    out = ""
    defs = S.lin_grad("hillnear13", [(0, "#b7c47c"), (1, "#9fb466")])
    # far blue mountains with snow caps
    for x0, x1, top, sd, col in ((1500, 3300, 430, 2, "#a9b8cc"), (2900, 4600, 470, 5, "#b3c0d0"),
                                 (4200, 5600, 440, 8, "#a9b8cc")):
        out += S.path(S.hill(x0, x1, 760, 760 - top, seed=sd, bottom=900, bumps=3), col, sw=3)
    for cx, cy in ((2380, 470), (3700, 520), (4950, 470)):
        out += (f'<path d="M{cx - 70},{cy + 60} L{cx},{cy - 6} L{cx + 70},{cy + 60} Q{cx + 30},{cy + 40} {cx + 10},'
                f'{cy + 62} Q{cx - 20},{cy + 40} {cx - 70},{cy + 60} Z" fill="#eef0f2" stroke="{INK}" stroke-width="3"/>')
    # mid hills
    out += S.path(S.hill(1400, 3900, 830, 130, seed=3, bottom=SH + 20, bumps=4), "#c4cd8e", sw=3.5)
    out += S.path(S.hill(3300, 5600, 840, 110, seed=6, bottom=SH + 20, bumps=4), "#bfcb88", sw=3.5)
    # towns of different peoples on the hills
    out += PR.nineveh_skyline(3150, 3650, 770, 0.33, seed=12, haze=0.3, tint="#e3ead4")        # a city
    for k, x in enumerate((2240, 2310, 2390, 2460)):                                           # a tent camp
        col = ("#d9a26a", "#c9714a", "#e6c890", "#b98f5c")[k]
        y = 812 + (k % 2) * 8
        out += (f'<path d="M{x - 38},{y} L{x},{y - 52} L{x + 38},{y} Z" fill="{col}" stroke="{INK}" '
                f'stroke-width="3" stroke-linejoin="round"/><path d="M{x},{y - 52} L{x},{y} M{x - 8},{y} '
                f'L{x},{y - 22} L{x + 8},{y}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    out += PR.animal(2560, 830, 0.22, -1, kind="camel") + PR.animal(2620, 836, 0.2, 1, kind="camel")
    for k, x in enumerate((4950, 5010, 5080, 5150, 5230)):                                     # a hill village
        out += PR.house(x, 790 + (k % 2) * 10, 0.13, variant=k % 4)
    # the river winding across the middle distance
    river = (f"M{2550},{SH + 30} C{2620},{1020} {2760},{930} {2980},{905} C{3200},{885} {3500},{880} {3800},{872} "
             f"L{3800},{895} C{3500},{905} {3220},{915} {3020},{935} C{2840},{955} {2730},{1040} {2700},{SH + 30} Z")
    out += S.path(river, P["sea_light"], sw=3)
    out += S.path(f"M{2700},{1100} C{2760},{1000} {2850},{950} {3000},{925}", sw=2.5,
                  extra=f'stroke="{P["foam"]}" opacity="0.8"')
    # the near meadow strip under everything right of the portico
    out += S.path(S.wave_line(1000, 8, 900, 0.5, 1500, SW + 40) + f" L{SW + 40},{SH + 30} L1500,{SH + 30} Z",
                  "url(#hillnear13)", sw=3.5)
    # the road out of the palace into the lands
    road = (f"M1700,{SH + 30} C1900,{GA + 20} 2200,{GB + 10} 2600,{GB} C2900,{GB - 6} 3200,{GB + 4} 3500,{GB + 30} "
            f"C3700,{GB + 50} 3800,{SH} 3850,{SH + 30} L4050,{SH + 30} C3990,{SH - 30} 3900,{GB + 60} 3650,{GB + 10} "
            f"C3350,{GB - 40} 3000,{GB - 50} 2600,{GB - 46} C2250,{GB - 40} 2000,{GB - 10} 1850,{SH + 30} Z")
    out += S.path(road, P["sand_light"], sw=3)
    rng = random.Random(7)
    for _ in range(80):
        x = rng.uniform(1600, SW)
        y = rng.uniform(1010, SH - 10)
        out += (f'<path d="M{f1(x)},{f1(y)} q4,-12 8,0" fill="none" stroke="{S.shade(P["grass_dark"], -0.1)}" '
                f'stroke-width="2.5" opacity="0.5"/>')
    for x, y, s, lean in ((2050, 1020, 0.55, 0.15), (3420, 1000, 0.5, -0.1), (3000, 870, 0.25, 0.0),
                          (2700, 860, 0.22, 0.1)):
        out += PR.palm_tree(x, y, s, lean=lean)
    for x, y, v in ((2250, 1150, 2), (2900, 1170, 0), (3300, 1140, 1), (2500, 1200, 2)):
        out += PR.grass_tuft(x, y, 0.7, variant=v)
    out += PR.bush(3150, 1120, 0.45, variant=1)
    return doc(out, defs)


def portico_svg():
    """King Darius's audience portico: cedar beams, a cream wall with a blue glazed frieze of friendly lions and
    rosettes, purple curtains behind the throne, a tiled floor with a red runner; open at the right to the lands."""
    out = ""
    x1 = PORT_X1
    defs = S.lin_grad("wall13", [(0, "#f1dfbb"), (1, "#e6cc9c")])
    defs += S.lin_grad("floor13", [(0, "#d9b98a"), (1, "#c49e6c")])
    # back wall up to the open end
    out += S.path(f"M-20,150 L{x1},150 L{x1},{GA} L-20,{GA} Z", "url(#wall13)", sw=0)
    # glazed frieze band with rosettes and little walking lions
    out += S.path(f"M-20,660 L{x1},660 L{x1},770 L-20,770 Z", "#3f6fa8", sw=4)
    for x in range(30, x1 - 40, 70):
        out += f'<circle cx="{x}" cy="690" r="14" fill="#f2d27a" stroke="{INK}" stroke-width="2.5"/>'
        out += f'<circle cx="{x}" cy="690" r="5" fill="#c9714a"/>'
    for k, x in enumerate(range(140, x1 - 120, 360)):
        out += PR.lion(x, 762, 0.17, 1, pose="walk_a" if k % 2 else "walk_b", eyes="happy")
    out += S.path(f"M-20,{GA - 130} L{x1},{GA - 130}", sw=3, extra=f'stroke="{S.shade("#e6cc9c", -0.2)}"')
    # cedar ceiling beams
    out += S.path(f"M-20,-20 L{x1 + 40},-20 L{x1 + 40},150 L-20,150 Z", P["wood"], sw=4)
    for x in range(-10, x1 + 40, 120):
        out += (f'<rect x="{x}" y="120" width="70" height="44" rx="6" fill="{P["wood_dark"]}" stroke="{INK}" '
                f'stroke-width="3"/>')
    out += S.path(f"M-20,40 L{x1 + 40},40", sw=3, extra=f'stroke="{P["wood_dark"]}"')
    # purple curtains tied back behind the throne
    for cx, side in ((TX - 230, -1), (TX + 230, 1)):
        d = (f"M{cx - 120 * side},150 L{cx + 60 * side},150 Q{cx + 30 * side},420 {cx - 20 * side},560 "
             f"Q{cx - 50 * side},800 {cx - 60 * side},{GA} L{cx - 160 * side},{GA} Q{cx - 140 * side},600 "
             f"{cx - 120 * side},150 Z")
        out += S.path(d, P["royal"], sw=4)
        out += S.path(f"M{cx - 20 * side},560 Q{cx + 10 * side},575 {cx - 6 * side},600", sw=6,
                      extra=f'stroke="{P["gold"]}"')
        for k in range(3):
            xx = cx - (20 + 35 * k) * side
            out += S.path(f"M{xx},200 Q{xx - 10 * side},520 {xx - 30 * side},{GA - 10}", sw=2.5,
                          extra=f'stroke="{S.shade(P["royal"], -0.25)}" opacity="0.7"')
    # floor
    out += S.path(f"M-20,{GA} L{x1 + 60},{GA} L{x1 + 140},{SH + 30} L-20,{SH + 30} Z", "url(#floor13)", sw=4)
    for k, y in enumerate(range(GA + 40, SH + 30, 60)):
        out += S.path(f"M-20,{y} L{x1 + 60 + (y - GA) * 0.4},{y}", sw=2.5,
                      extra=f'stroke="{S.shade("#c49e6c", -0.18)}" opacity="0.7"')
    # red runner from the throne toward the open end
    out += S.path(f"M{TX - 60},{GA + 6} L{x1 + 60},{GA + 6} L{x1 + 110},{GA + 120} L{TX - 120},{GA + 120} Z",
                  "#b5523b", sw=3.5)
    out += S.path(f"M{TX - 85},{GA + 30} L{x1 + 75},{GA + 30} M{TX - 105},{GA + 96} L{x1 + 98},{GA + 96}", sw=3,
                  extra=f'stroke="{P["gold"]}"')
    # the wall's cut end (a thick pier) where the portico opens onto the lands
    out += S.path(f"M{x1 - 40},150 L{x1 + 40},150 L{x1 + 40},{GA} L{x1 - 40},{GA} Z", "#e2c591", sw=4)
    out += S.path(f"M{x1 - 40},660 L{x1 + 40},660 L{x1 + 40},770 L{x1 - 40},770 Z", "#3f6fa8", sw=3)
    return doc(out, defs)


def columns_svg():
    out = ""
    for x in COLS:
        out += PR.persian_column(x, GA + 20, 0.5, height=1340)
    return doc(out)


def town_svg():
    """Another land's town: houses and a ziggurat behind a wall; the king's letter posted on the wall."""
    out = ""
    out += PR.nineveh_skyline(TOWN_X0 - 50, SW + 60, 930, 0.55, seed=21, haze=0.18, tint="#ece6d2")
    out += PR.city_wall(TOWN_X0, SW + 40, 1000, height=300, gate=(TOWN_X0 + 260, 230), doors_open=1.0, seed=3)
    # a festive cloth banner and a notice board on the wall for the decree
    bx, by = DECREE
    out += (f'<rect x="{bx - 150}" y="{by - 170}" width="300" height="350" rx="10" fill="{P["wood"]}" '
            f'stroke="{INK}" stroke-width="4"/>')
    out += PR.decree(bx, by, 1.15)
    for k, x in enumerate(range(TOWN_X0 + 480, SW, 160)):
        col = ("#c9714a", "#3f6fa8", "#e6b45a", "#6f8a45")[k % 4]
        out += f'<path d="M{x},700 L{x + 60},700 L{x + 30},745 Z" fill="{col}" stroke="{INK}" stroke-width="2.5"/>'
    out += S.path(f"M{TOWN_X0 + 470},700 Q{(TOWN_X0 + SW) / 2},716 {SW + 20},700", sw=3)
    # the square's paving
    out += S.path(f"M{TOWN_X0 - 80},{GC - 70} L{SW + 40},{GC - 70} L{SW + 40},{SH + 30} L{TOWN_X0 - 260},{SH + 30} Z",
                  "#e6d2a6", sw=4)
    rng = random.Random(3)
    for _ in range(60):
        x = rng.uniform(TOWN_X0 - 100, SW)
        y = rng.uniform(GC - 50, SH - 10)
        out += (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(rng.uniform(16, 30))}" ry="{f1(rng.uniform(6, 10))}" '
                f'fill="#d8c08f" stroke="{S.shade("#d8c08f", -0.25)}" stroke-width="2" opacity="0.8"/>')
    out += PR.palm_tree(TOWN_X0 + 40, GC - 60, 0.65, lean=0.12)
    out += PR.palm_tree(SW - 70, GC - 50, 0.6, lean=-0.15)
    return doc(out)


def page_d_svg():
    """Afterwards: a golden afternoon on the palace garden terrace (the closing 'page' of this scene)."""
    x0, x1, y0, y1 = PAGE
    out = ""
    defs = S.lin_grad("skyd", [(0, "#9cc6dc"), (0.55, "#f3dcb0"), (1, "#f8e4b8")])
    defs += S.lin_grad("terr", [(0, "#e2c48f"), (1, "#cfa974")])
    out += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#skyd)"/>'
    for cx, cy, w, h, sd in ((x0 + 900, y0 + 160, 300, 84, 31), (x0 + 1600, y0 + 110, 260, 76, 32),
                             (x0 + 1250, y0 + 290, 180, 52, 33)):
        out += S.cloud(cx, cy, w, h, fill="#fff3df", seed=sd, sw=3, shade_fill="#f2d6b0")
    # distant Babylon and the river behind the garden
    out += PR.nineveh_skyline(x0 + 600, x1 + 60, y0 + 700, 0.45, seed=40, haze=0.45, tint="#f3dcb0")
    out += S.path(f"M{x0},{y0 + 700} L{x1},{y0 + 700} L{x1},{y0 + 760} L{x0},{y0 + 760} Z", P["sea_light"], sw=3)
    # garden: hedges, flowers, palms
    out += S.path(S.wave_line(y0 + 742, 10, 260, 0, x0 - 20, x1 + 20) + f" L{x1 + 20},{y0 + 830} L{x0 - 20},{y0 + 830} Z",
                  P["leaf"], sw=3.5)
    rng = random.Random(9)
    for _ in range(40):
        x = rng.uniform(x0 + 500, x1)
        y = rng.uniform(y0 + 752, y0 + 812)
        col = rng.choice(("#f0998a", "#f2c14e", "#fff1d0", "#c9714a"))
        out += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="7" fill="{col}" stroke="{INK}" stroke-width="2"/>'
    out += PR.palm_tree(x0 + 1700, y0 + 820, 0.62, lean=-0.1)
    out += PR.palm_tree(x0 + 1960, y0 + 830, 0.5, lean=0.15)
    # the palace on the left: wall, frieze, two columns and a cedar beam
    out += S.path(f"M{x0 - 20},{y0 - 20} L{x0 + 520},{y0 - 20} L{x0 + 520},{y0 + 860} L{x0 - 20},{y0 + 860} Z",
                  "#efdcb6", sw=4)
    out += S.path(f"M{x0 - 20},{y0 + 520} L{x0 + 520},{y0 + 520} L{x0 + 520},{y0 + 610} L{x0 - 20},{y0 + 610} Z",
                  "#3f6fa8", sw=3.5)
    for x in range(int(x0) + 20, int(x0) + 520, 64):
        out += f'<circle cx="{x}" cy="{y0 + 565}" r="13" fill="#f2d27a" stroke="{INK}" stroke-width="2.5"/>'
    # an arched window with a lattice above the frieze
    out += S.path(f"M{x0 + 170},{y0 + 470} L{x0 + 170},{y0 + 300} Q{x0 + 270},{y0 + 170} {x0 + 370},{y0 + 300} "
                  f"L{x0 + 370},{y0 + 470} Z", "#8c6a50", sw=4)
    for k in range(1, 4):
        xx = x0 + 170 + 50 * k
        out += S.path(f"M{xx},{y0 + 250} L{xx},{y0 + 470}", sw=3)
    for yy in (y0 + 340, y0 + 405):
        out += S.path(f"M{x0 + 170},{yy} L{x0 + 370},{yy}", sw=3)
    out += S.path(f"M{x0 + 520},{y0 + 40} L{x1 + 20},{y0 + 40} L{x1 + 20},{y0 + 100} L{x0 + 520},{y0 + 100} Z",
                  P["wood"], sw=4)
    # terrace floor
    out += S.path(f"M{x0 - 20},{y0 + 820} L{x1 + 20},{y0 + 820} L{x1 + 20},{y1 + 20} L{x0 - 20},{y1 + 20} Z",
                  "url(#terr)", sw=4)
    for y in range(int(y0) + 870, int(y1) + 20, 60):
        out += S.path(f"M{x0 - 20},{y} L{x1 + 20},{y}", sw=2.5, extra=f'stroke="{S.shade("#cfa974", -0.18)}" opacity="0.7"')
    # a low balustrade between terrace and garden
    out += S.path(f"M{x0 + 520},{y0 + 800} L{x1 + 20},{y0 + 800} L{x1 + 20},{y0 + 826} L{x0 + 520},{y0 + 826} Z",
                  "#e9d4ac", sw=3.5)
    return doc(out, defs)


def page_d_front_svg():
    x0, x1, y0, y1 = PAGE
    out = ""
    for x in (x0 + 470, x1 - 140):
        out += PR.persian_column(x, y0 + 826, 0.42, height=1050)
    out += PR.bush(x0 + 640, y0 + 830, 0.5, variant=1) + PR.bush(x1 - 330, y0 + 830, 0.45, variant=3)
    # a striped rug, potted flowers and a little stack of scrolls on the terrace
    out += S.path(f"M{x0 + 700},{y0 + 925} L{x0 + 1260},{y0 + 925} L{x0 + 1310},{y0 + 1000} L{x0 + 650},{y0 + 1000} Z",
                  "#b5523b", sw=3.5)
    out += S.path(f"M{x0 + 692},{y0 + 940} L{x0 + 1270},{y0 + 940} M{x0 + 664},{y0 + 984} L{x0 + 1298},{y0 + 984}",
                  sw=3, extra=f'stroke="{P["gold"]}"')
    for px_, py_ in ((x0 + 560, y0 + 930), (x1 - 180, y0 + 935)):
        out += PR.bush(px_, py_ - 90, 0.38, variant=1) + PR.jar(px_, py_ - 40, 0.6)
    for k in range(3):
        out += PR.scroll(x0 + 610 + 18 * k, y0 + 975 - 26 * k, 0.45, rot=-6 + 6 * k)
    return doc(out)


def sparkle_burst(x, y, s=1.0):
    """A little golden twinkle (the seal pressed onto the letter)."""
    out = ""
    for k in range(8):
        a = math.radians(45 * k)
        r0, r1 = (14 if k % 2 else 10) * s, (40 if k % 2 else 28) * s
        out += (f'<path d="M{f1(x + r0 * math.cos(a))},{f1(y + r0 * math.sin(a))} L{f1(x + r1 * math.cos(a))},'
                f'{f1(y + r1 * math.sin(a))}" stroke="#f2c14e" stroke-width="{5 * s:.1f}" stroke-linecap="round"/>')
    return S.g(out, filter="wobble-fine")


def scroll_in_hand(fn, x, y, s, f, **kw):
    far = C.hand_positions(fn, x, y, s, f, **kw)[0]
    return PR.scroll(far[0] + 10 * f * s, far[1] + 4 * s, 0.42 * s, rot=-70 * f)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[:3]

    # ---- key times ----
    t_write = snap(L0.start + 0.4)                       # the king writes / seals ("写信")
    t_seal = snap(when(ctx, "写信") + 0.3)
    t_go = snap(when(ctx, "全国各地") - 0.1)              # the messengers turn and set off
    WALK_P = 0.3
    t_horn = t_go + 0.2
    t_panB0, t_panB1 = L0.end - 0.4, L1.start + 2.6
    t_panC0, t_panC1 = L1.at("他是永远") + 1.6, L1.at("他会拯救人") + 2.2
    t_nod = snap(L1.at("他会拯救人") + 2.4)                # people nod as they read
    t_cheer = snap(L1.at("脱离") + 0.1)                   # "脱离狮子的口": cheers
    t_page0, t_page1 = L1.end + 0.25, L2.start + 0.1      # page turn to the palace garden
    t_read = snap(L2.start + 0.2)
    t_turn = snap(L2.at("做事") + 0.05)                   # "做事都很顺利": Daniel turns and talks to the king
    t_kn = snap(t_turn + 0.6)

    # ---- camera ----
    CA = Cam(960, 760, 1680)
    CB = Cam(2850, 690, 2100)
    CC = Cam(4500, 700, 2000)
    CD = Cam(4470, 795, 1500)
    sc.camera = cam_path([(0, CA), (t_panB0, CA), (t_panB1, CB), (t_panC0, CB), (t_panC1, CC), (t_page1, CC),
                          (T, CD)])

    # ---- backdrop ----
    sc.add("sky", sky_svg(), z=0, wc=0.5)
    sc.add("clouds", clouds_svg(), z=0.5, wc=0.6, motion=M.drift(vx=-8))
    sc.add("lands", lands_svg(), z=1)
    # the river boat with a tiny messenger on deck, sailing on
    bx, by, bs = 2900, 917, 0.16
    deck = PR.local_to_stage(bx, by, bs, 1, 40, PR.SHIP_DECK_Y)
    boat = PR.ship(bx, by, bs, 1, part="back") + C.guard(deck[0], deck[1], bs * 0.95, 1, variant=2, spear=True) + \
        PR.ship(bx, by, bs, 1, part="front")
    river_clip = (f'<clipPath id="bclip"><path d="M0,0 L{SW},0 L{SW},{by + 4} L0,{by + 4} Z"/></clipPath>')
    sc.add("boat", doc(f'<g clip-path="url(#bclip)">{boat}</g>', river_clip), z=1.2,
           motion=M.combine(M.drift(vx=16), M.sway(1.5, 3.0, pivot=(bx, by))))
    sc.add("town", town_svg(), z=1.5)
    sc.add("portico", portico_svg(), z=2)

    # ---- region A: the king seals the letter, Daniel beside him, the messengers set off ----
    sc.add("throne", doc(PR.throne(TX, GA, KS, 1)), z=2.1)
    K = lambda expr=None: doc(C.king(TX, GA, KS, 1, pose="sit_sign", attire="darius", throne=False, expr=expr))  # noqa
    kfr = [K("happy"), K("call"), K("d11_blink_happy")]
    sc.add("king", kfr, z=2.2, frame_at=cuts(with_blinks([(0, 0), (t_seal, 1), (snap(t_go + 0.6), 0)], {0: 2},
                                                         [1.2, 4.6])),
           motion=M.combine(M.breathe(0.01, 3.2, pivot=(TX, GA)), dip(t_seal, KS, (TX, GA), 7)))
    seal_pt = C.hand_positions(C.king, TX, GA, KS, 1, pose="sit_sign", attire="darius", throne=False)[1]
    sc.add("seal_pop", doc(sparkle_burst(seal_pt[0] + 30, seal_pt[1] - 10, 1.0)), z=2.25, wc=0,
           motion=hop(t_seal, [(-0.02, {"alpha": 0, "s": 0.5}), (0.08, {"alpha": 1, "s": 1}),
                               (0.6, {"alpha": 0, "s": 1.3})], (seal_pt[0] + 30, seal_pt[1] - 10), ["out", "sine"]))
    DX_ = TX + 330
    dfr = [doc(C.ground_shadow(DX_, GA, 1.0, 130) + C.daniel(DX_, GA, 1.0, -1, pose=p, expr=e))
           for p, e in (("stand", "happy"), ("stand", "d11_blink_happy"), ("bow", "peaceful"))]
    sc.add("daniel_a", dfr, z=2.3, frame_at=cuts(with_blinks([(0, 0), (snap(t_seal + 0.1), 2), (snap(t_seal + 1.2), 0)],
                                                             {0: 1}, [2.1, 4.9])),
           motion=M.combine(M.breathe(0.01, 3.0, pivot=(DX_, GA)), dip(snap(t_seal + 0.1), 1.0, (DX_, GA), 6),
                            dip(snap(t_seal + 1.2), 1.0, (DX_, GA), 5)))
    for i, (v, x) in enumerate(MSG):
        n = 22 - 2 * i
        fa_w, dxw, dyw, t_end = step_walk(t_go + 0.25 + 0.12 * i, n, 85 * GS, WALK_P, GS)
        fr = [doc(C.ground_shadow(x, GA, GS, 120) + C.guard(x, GA, GS, -1, variant=v) +
                  scroll_in_hand(C.guard, x, GA, GS, -1, variant=v, pose="stand")),
              doc(C.ground_shadow(x, GA, GS, 120) + C.guard(x, GA, GS, 1, variant=v) +
                  scroll_in_hand(C.guard, x, GA, GS, 1, variant=v, pose="stand"))]
        for p in ("walk_a", "walk_b"):
            fr.append(doc(C.ground_shadow(x, GA, GS, 120) + C.guard(x, GA, GS, 1, variant=v, pose=p) +
                          scroll_in_hand(C.guard, x, GA, GS, 1, variant=v, pose=p)))
        fr.append(doc(C.ground_shadow(x, GA, GS, 120) + C.guard(x, GA, GS, -1, variant=v, expr="d11_blink_neutral") +
                      scroll_in_hand(C.guard, x, GA, GS, -1, variant=v, pose="stand")))
        t_turn_m = snap(t_go + 0.1 * i)
        base = cuts(with_blinks([(0, 0), (t_turn_m, 1)], {0: 4}, [1.7 + i, 3.3 + i * 0.4]))

        def fa(t, base=base, fa_w=fa_w):
            w = fa_w(t)
            return base(t) if w is None else 2.0 + w
        sc.add(f"messenger{i}", fr, z=2.4 + 0.01 * i, frame_at=fa, motion=M.combine(
            lambda t, dxw=dxw, dyw=dyw: Tf(dx=dxw(t), dy=dyw(t)),
            M.breathe(0.012, 2.8, pivot=(x, GA), phase=0.4 * i), dip(t_turn_m, GS, (x, GA), 6),
            lambda t: Tf(alpha=1 - M.progress(t, t_panC1, t_panC1 + 0.1))))
    sc.add("columns", columns_svg(), z=2.6)

    # ---- region B: a messenger on the road far out in the lands ----
    rv, rx, ry, rs = 1, 2380, GB - 22, 0.62
    n = 34
    fa_w, dxw, dyw, _ = step_walk(0.3, n, 85 * rs, 0.36, rs)
    rfr = [doc(C.ground_shadow(rx, ry, rs, 120) + C.guard(rx, ry, rs, 1, variant=rv, pose=p) +
               scroll_in_hand(C.guard, rx, ry, rs, 1, variant=rv, pose=p)) for p in ("walk_a", "walk_b")]
    sc.add("road_msg", rfr, z=1.3, frame_at=lambda t: fa_w(t) or 0.0,
           motion=lambda t: Tf(dx=dxw(t), dy=dyw(t) - 0.035 * dxw(t), alpha=0.0 if t > t_page1 + 0.2 else 1.0))

    # ---- region C: people of another land read the letter on the town wall ----
    bxd, byd = DECREE
    hx = bxd - 250
    herald = [doc(C.ground_shadow(hx, GC, CS, 120) + C.citizen(hx, GC, CS, 1, kind="man", variant=2, pose=p, expr=e))
              for p, e in (("point", "call"), ("stand", "happy"), ("cheer", "happy"), ("point", "d11_blink_call"))]
    sc.add("herald", herald, z=2.7, frame_at=cuts(with_blinks([(0, 0), (t_cheer, 2), (snap(t_cheer + 1.5), 1)], {0: 3},
                                                             [12.6, 14.3])),
           motion=M.combine(M.breathe(0.012, 2.6, pivot=(hx, GC)), happy_hop(t_cheer, CS, (hx, GC), 14),
                            lambda t: Tf(rot=1.6 * math.sin(2 * math.pi * t / 1.9) * (1 - M.progress(t, t_cheer - 0.4, t_cheer)),
                                         px=hx, py=GC),
                            lambda t: Tf(alpha=0.0 if t > t_page1 + 0.2 else 1.0)))
    crowd = [("elder", 0, bxd + 220, GC + 10, "listen", None, "stand"),
             ("child", 1, bxd + 340, GC + 40, "point", None, "cheer"),
             ("woman", 2, bxd + 460, GC, "listen", None, "cheer"),
             ("man", 3, bxd + 590, GC + 14, "listen", None, "kneel_pray"),
             ("child", 0, bxd + 700, GC + 46, "stand", "happy", "cheer"),
             ("woman", 1, bxd + 820, GC + 6, "stand", "happy", "cheer"),
             ("man", 0, bxd - 520, GC + 30, "listen", None, "cheer")]
    for i, (kind, v, x, y, p0, e0, p1) in enumerate(crowd):
        f = -1 if x > bxd else 1
        s = CS
        fr = [doc(C.ground_shadow(x, y, s, 110) + C.citizen(x, y, s, f, kind=kind, variant=v, pose=p0, expr=e0)),
              doc(C.ground_shadow(x, y, s, 110) + C.citizen(x, y, s, f, kind=kind, variant=v, pose="stand", expr="happy")),
              doc(C.ground_shadow(x, y, s, 110) + C.citizen(x, y, s, f, kind=kind, variant=v, pose=p1,
                                                              expr="happy" if p1 != "kneel_pray" else None)),
              doc(C.ground_shadow(x, y, s, 110) + C.citizen(x, y, s, f, kind=kind, variant=v, pose="stand",
                                                              expr="d11_blink_happy"))]
        tn = snap(t_nod + 0.13 * i)
        tc = snap(t_cheer + 0.1 * (i % 4))
        cc = with_blinks([(0, 0), (tn, 1), (tc, 2)], {1: 3}, [11.0 + 0.3 * i, 14.6 - 0.2 * i])
        pv = (x, y)
        sc.add(f"reader{i}", fr, z=2.75 + 0.01 * i, frame_at=cuts(cc), motion=M.combine(
            M.breathe(0.012, 2.6 + 0.15 * i, pivot=pv, phase=0.3 * i), dip(tn, s, pv, 5),
            hop(tn + 0.3, [(0, {"rot": 0}), (0.2, {"rot": 3 * f}), (0.45, {"rot": 0})], pv),
            happy_hop(tc, s, pv, 16) if p1 != "kneel_pray" else dip(tc, s, pv, 8),
            hop(tc + 0.55, [(0, {"dy": 0}), (0.17, {"dy": -10 * s}), (0.34, {"dy": 0})], pv) if p1 == "cheer" else None,
            lambda t: Tf(alpha=0.0 if t > t_page1 + 0.2 else 1.0)))

    # ---- page D: afterwards, Daniel serves happily at the palace (a page-turn dissolve) ----
    page_in = lambda t: Tf(alpha=M.progress(t, t_page0, t_page1, "sine"))     # noqa: E731
    sc.add("page_d", page_d_svg(), z=5, motion=page_in)
    x0, x1, y0, y1 = PAGE
    gd = y0 + 1000
    dvx, kvx = x0 + 1080, x0 + 820
    wings = (1.0, 0.5, 0.0, -0.5, -1.0)
    cyc = (0, 1, 2, 3, 4, 3, 2, 1)
    for i, (xa, ya, xb, yb, ta, tb, s) in enumerate(((x1 - 300, y0 + 240, x0 + 900, y0 + 170, t_page0, T + 1, 0.45),
                                                     (x1 - 120, y0 + 330, x0 + 1100, y0 + 270, t_page0 + 1.5, T + 2, 0.4))):
        fr = [doc(PR.dove(xa, ya, s, -1, wing=w)) for w in wings]

        def mv(t, xa=xa, ya=ya, xb=xb, yb=yb, ta=ta, tb=tb, i=i):
            u = (t - ta) / (tb - ta)
            if u <= 0 or u >= 1:
                return Tf(alpha=0.0)
            return Tf(dx=(xb - xa) * u, dy=(yb - ya) * u + 10 * math.sin(2 * math.pi * t / 1.7 + i),
                      alpha=page_in(t).alpha)
        sc.add(f"dove{i}", fr, z=5.05, frame_at=lambda t, i=i: float(cyc[int(t * 9 + i * 3) % 8]), motion=mv,
               seed=880 + i)
    kd = [doc(C.ground_shadow(kvx, gd, 1.0, 130) + C.king(kvx, gd, 1.0, 1, pose="stand", attire="darius", expr=e))
          for e in ("happy", "d11_blink_happy")]
    sc.add("king_d", kd, z=5.2, frame_at=cuts(with_blinks([(0, 0)], {0: 1}, [19.3, 21.9, 23.6])),
           motion=M.combine(page_in, M.breathe(0.01, 3.1, pivot=(kvx, gd)),
                            hop(t_kn, [(0, {"rot": 0}), (0.2, {"rot": 3}), (0.45, {"rot": -1}), (0.7, {"rot": 0})],
                                (kvx, gd))))
    dd = [doc(C.ground_shadow(dvx, gd, 1.0, 130) + C.daniel(dvx, gd, 1.0, f, pose=p, expr=e))
          for p, e, f in (("read", "happy", 1), ("read", "d11_blink_happy", 1), ("explain", "happy", -1),
                          ("explain", "d11_blink_happy", -1))]
    sc.add("daniel_d", dd, z=5.3, frame_at=cuts(with_blinks([(0, 0), (t_turn, 2)], {0: 1, 2: 3}, [19.9, 22.6])),
           motion=M.combine(page_in, M.breathe(0.01, 3.0, pivot=(dvx, gd)), dip(t_turn, 1.0, (dvx, gd), 6)))
    # a helper brings a basket of fruit; a child waves
    cx_, cy_ = x0 + 1500, gd - 30
    sc.add("helpers", [doc(C.ground_shadow(cx_, cy_, 0.85, 110) + C.citizen(cx_, cy_, 0.85, -1, kind="woman", variant=1,
                                                                          pose=p) +
                           C.ground_shadow(cx_ + 130, cy_ + 20, 0.85, 90) +
                           C.citizen(cx_ + 130, cy_ + 20, 0.85, -1, kind="child", variant=1, pose=q))
                       for p, q in (("stand", "stand"), ("stand", "cheer"))], z=5.15,
           frame_at=cuts([(0, 0), (snap(t_turn + 0.8), 1)]),
           motion=M.combine(page_in, M.breathe(0.012, 2.7, pivot=(cx_, cy_)),
                            happy_hop(snap(t_turn + 0.8), 0.85, (cx_ + 130, cy_ + 20), 10)))
    sc.add("page_d_front", page_d_front_svg(), z=5.4, motion=page_in)

    # ---- sound ----
    sc.sfx("birds", 0.0, dur=T, gain_db=-17, fade_in=0.8, fade_out=0.8)
    sc.sfx("pop", t_seal, gain_db=-9)
    sc.sfx("sparkle", t_seal + 0.05, gain_db=-16)
    sc.sfx("horn", t_horn, gain_db=-10, pan=0.2)
    sc.sfx("footsteps", t_go + 0.25, dur=4.2, gain_db=-14, pan=0.2, fade_out=1.0)
    sc.sfx("wind_soft", t_panB0, dur=t_page0 - t_panB0 + 0.5, gain_db=-18, fade_in=1.0, fade_out=1.0)
    sc.sfx("waves_calm", t_panB0 + 1.0, dur=5.0, gain_db=-21, fade_in=1.2, fade_out=1.5)
    sc.sfx("horn", t_panC1 - 0.6, gain_db=-14, pan=0.4)
    sc.sfx("crowd", t_panC0, dur=t_page0 - t_panC0 + 0.6, gain_db=-17, fade_in=1.0, fade_out=0.8)
    sc.sfx("cheer", t_cheer, dur=t_page1 - t_cheer + 0.4, gain_db=-13, fade_in=0.2, fade_out=0.9)
    return sc
