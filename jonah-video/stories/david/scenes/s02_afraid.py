"""Scene 2 — the opening question: "have you ever been afraid?" A cosy bedroom vignette (a little girl in bed,
thunder at the window, then the lamp goes out), then a page of Israelite soldiers trembling behind their shields
as the huge shadow of a giant slides over them.

Beats (all keyed to the narration chunks; positions inside a chunk are fractions of that chunk, measured on the
current take, so a regenerated voice stays close):
  0 .. 1.0     s01's title page, continued exactly (title_page(..., toff) from s01_title: the plain cross-dissolve
               between the two scenes blends identical pictures); the title lettering then fades
  line 0       "小朋友，你有没有害怕过什么？" -> a round page-iris opens on a cosy night bedroom: the girl sits up
               in bed with her toy lamb, the oil lamp glowing, rain at the window; she glances at the window
               "比如打雷，" -> lightning flashes in the window (thunder sfx), she squeaks and dives under the quilt,
               which trembles
               "比如黑黑的房间？" -> the lamp goes out (a little smoke curl), the room turns night-blue; on "黑黑" she
               peeks out over the quilt edge, only her wide eyes and fingers showing - a little scared but cute
  line 1       a second iris opens on Israel's camp: rows of soldiers with spears ("今天的故事里，有一大群人，")
               "都怕得不得了。" -> one after another they duck behind their shields (squash dips), trembling
               "他们怕的，是一个巨人！" -> on "是一个巨人" a huge giant-shaped shadow (helmet crest, spear) slides in
               from the right over the whole crowd with two heavy footfalls (thud sfx, tiny camera nudges); the
               soldiers jolt; the light dims
  end          calm hold: the soldiers trembling under the shadow (page dip to s03)
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import cuts, snap
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.loader import context, load_timeline
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.david.scenes import s01_title as T1

INK = P["ink"]

# ---------------------------------------------------------------- bedroom layout (stage px)
FLOOR_Y = 935
WIN = (1480, 1880, 175, 640)          # window opening x0, x1, top (arch apex), sill
KID = (790, 935, 1.55)                # the girl (citizen child, variant 1): anchor hidden behind the quilt
QUILT_EDGE = 772                      # top edge of the quilt in front of her
DIVE_DY = 270                         # fully under the quilt
PEEK_DY = 102                         # eyes and hair just above the quilt edge
LAMP = (395, 708, 1.7)                # oil lamp on the bedside table
IRIS1 = (900, 600)
# ---------------------------------------------------------------- soldiers page
CAMP_GROUND = 760
IRIS2 = (900, 640)


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def in_chunk(line, phrase, frac):
    for c in line.chunks:
        if phrase in c.text:
            return c.start + frac * (c.end - c.start)
    raise KeyError(phrase)


# ================================================================== bedroom drawings


def room_svg():
    defs = (S.lin_grad("a2wall", [(0, "#efd2ad"), (1, "#f5e0c0")]) +
            S.lin_grad("a2floor", [(0, "#b98455"), (1, "#a06f45")]) +
            S.lin_grad("a2night", [(0, "#27355a"), (0.6, "#3c4d78"), (1, "#56658c")]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{FLOOR_Y + 30}" fill="url(#a2wall)"/>'
    # wallpaper: soft stripes with little stars and moons
    for x in range(-40, W + 60, 120):
        b += f'<rect x="{x}" y="-20" width="44" height="{FLOOR_Y + 20}" fill="#e9c79f" opacity="0.45"/>'
    for i, x in enumerate(range(20, W, 120)):
        for j, y in enumerate(range(60 + (i % 2) * 70, FLOOR_Y - 60, 140)):
            if (i + j) % 2:
                b += (f'<path d="M{x},{y - 11} L{x + 4},{y - 3} L{x + 12},{y} L{x + 4},{y + 3} L{x},{y + 11} '
                      f'L{x - 4},{y + 3} L{x - 12},{y} L{x - 4},{y - 3} Z" fill="#f7e3b8" opacity="0.9"/>')
            else:
                b += f'<circle cx="{x}" cy="{y}" r="5" fill="#dcb88c" opacity="0.7"/>'
    b = S.g(b, filter="wobble")
    # floor and skirting
    fl = f'<rect x="-20" y="{FLOOR_Y}" width="{W + 40}" height="{H - FLOOR_Y + 30}" fill="url(#a2floor)"/>'
    for y in range(FLOOR_Y + 40, H + 40, 52):
        fl += f'<path d="M-20,{y} L{W + 20},{y + 6}" stroke="#8a5a36" stroke-width="3" opacity="0.6"/>'
    fl += (f'<rect x="-20" y="{FLOOR_Y - 26}" width="{W + 40}" height="30" fill="{P["wood"]}" stroke="{INK}" '
           f'stroke-width="4"/>')
    # rug
    fl += (f'<ellipse cx="1180" cy="{FLOOR_Y + 120}" rx="520" ry="70" fill="#c9714a" stroke="{INK}" stroke-width="4"/>'
           f'<ellipse cx="1180" cy="{FLOOR_Y + 120}" rx="440" ry="48" fill="none" stroke="#f2c14e" stroke-width="6" '
           f'stroke-dasharray="18 14"/>')
    b += S.g(fl, filter="wobble")
    # window: night sky, far hills, rain clouds
    x0, x1, top, sill = WIN
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    shape = f"M{x0},{sill} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{sill} Z"
    win = f'<path d="{shape}" fill="url(#a2night)"/>'
    win += S.path(S.hill(x0 - 40, x1 + 40, sill - 20, 60, seed=4, bumps=2, bottom=sill + 10), fill="#2b3a52", sw=2.5)
    win += S.cloud(cx - 60, top + 120, 300, 90, "#5d6b8a", seed=3, sw=3)
    win += S.cloud(cx + 120, top + 200, 220, 70, "#53617f", seed=5, sw=3)
    clip = f'<clipPath id="a2win"><path d="{shape}"/></clipPath>'
    b += S.g(S.g(win, extra='clip-path="url(#a2win)"'), filter="wobble")
    b += window_frame_svg()
    # picture of a sheep on the wall, a shelf with toys
    pic = (f'<rect x="900" y="250" width="230" height="180" rx="10" fill="#c9e0c0" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="900" y="250" width="230" height="180" rx="10" fill="none" stroke="{P["wood"]}" '
           f'stroke-width="3" transform="translate(0,0)"/>'
           f'<circle cx="1060" cy="300" r="22" fill="{P["sun"]}" stroke="{INK}" stroke-width="2.5"/>'
           f'<path d="M900,385 Q1000,340 1130,380 L1130,430 L900,430 Z" fill="#93b85c"/>')
    pic += PR.sheep(1005, 410, 0.45, 1, 0)
    b += S.g(pic, filter="wobble-fine")
    shelf = (f'<rect x="240" y="300" width="300" height="22" rx="5" fill="{P["wood_light"]}" stroke="{INK}" '
             f'stroke-width="4"/><path d="M270,322 L290,350 M510,322 L490,350" stroke="{INK}" stroke-width="5"/>')
    shelf += PR.jar(300, 300, 0.45, color="#7fa6c9") + PR.five_stones(400, 300, 0.7) + PR.jar(480, 300, 0.35)
    b += S.g(shelf, filter="wobble-fine")
    # headboard and pillows (behind the girl)
    hb = (f'<path d="M560,{FLOOR_Y + 5} L560,560 Q560,500 620,500 L700,500 Q760,500 760,560 L760,{FLOOR_Y + 5} Z" '
          f'fill="{P["wood"]}" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M590,560 Q600,530 630,530 L690,530 Q730,530 730,565 L730,700 L590,700 Z" '
          f'fill="{P["wood_light"]}" stroke="{INK}" stroke-width="3" opacity="0.8"/>'
          f'<circle cx="660" cy="590" r="16" fill="{P["gold"]}" stroke="{INK}" stroke-width="3"/>')
    hb += S.path(S.blob(745, 690, 120, 75, 0.06, 9, seed=3), fill="#fbf1de", sw=4)
    hb += S.path(S.blob(790, 715, 95, 56, 0.06, 9, seed=4), fill="#f3e2f0", sw=4)
    b += S.g(hb, filter="wobble-fine")
    return doc(b, defs + clip)


def window_frame_svg():
    x0, x1, top, sill = WIN
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    wood, wl = P["wood"], P["wood_light"]
    b = (f'<path d="M{x0},{sill} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{sill}" fill="none" '
         f'stroke="{INK}" stroke-width="34"/>'
         f'<path d="M{x0},{sill} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{sill}" fill="none" '
         f'stroke="{wl}" stroke-width="26"/>'
         f'<path d="M{cx},{top} L{cx},{sill} M{x0},{top + r + 40} L{x1},{top + r + 40}" stroke="{INK}" '
         f'stroke-width="16"/><path d="M{cx},{top} L{cx},{sill} M{x0},{top + r + 40} L{x1},{top + r + 40}" '
         f'stroke="{wl}" stroke-width="9"/>'
         f'<rect x="{x0 - 50}" y="{sill - 6}" width="{x1 - x0 + 100}" height="34" rx="6" fill="{wood}" '
         f'stroke="{INK}" stroke-width="4"/>')
    # curtains tied back on both sides
    for sd, xe in ((-1, x0), (1, x1)):
        xo = xe + sd * 80
        d = (f"M{xe - sd * 40},{top - 60} L{xo + sd * 20},{top - 60} C{xo + sd * 10},{top + 160} {xo - sd * 30},"
             f"{top + 260} {xo},{sill - 100} C{xo + sd * 20},{sill} {xo + sd * 10},{sill + 120} {xo},{sill + 200} "
             f"L{xe - sd * 10},{sill + 200} C{xe + sd * 30},{sill + 60} {xe + sd * 40},{sill - 60} {xe + sd * 20},"
             f"{sill - 110} C{xe - sd * 20},{top + 200} {xe - sd * 40},{top + 60} {xe - sd * 40},{top - 60} Z")
        b += S.path(d, fill="#8fb3c9", sw=4)
        b += (f'<path d="M{xe - sd * 5},{top} C{xe + sd * 10},{top + 200} {xe + sd * 30},{sill - 160} '
              f'{xe + sd * 40},{sill - 110}" stroke="#6f95ad" stroke-width="5" fill="none"/>')
        b += S.path(S.blob(xo - sd * 10, sill - 100, 30, 14, 0.1, 8, seed=7), fill="#e6b85a", sw=3)
    b += (f'<rect x="{x0 - 130}" y="{top - 78}" width="{x1 - x0 + 260}" height="20" rx="10" fill="{P["wood_dark"]}" '
          f'stroke="{INK}" stroke-width="4"/>')
    b += PR.jar(x1 - 40, sill - 6, 0.38, color="#c9714a")
    b += f'<path d="M{x1 - 48},{sill - 46} q-14,-40 6,-62 M{x1 - 38},{sill - 48} q16,-30 2,-58" stroke="{P["leaf_dark"]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return S.g(b, filter="wobble-fine")


def rain_svg(k):
    import random
    rng = random.Random(30 + k)
    x0, x1, top, sill = WIN
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    shape = f"M{x0},{sill} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{sill} Z"
    b = ""
    for _ in range(46):
        x = rng.uniform(x0 - 40, x1)
        y = rng.uniform(top, sill)
        b += f'<path d="M{x:.0f},{y:.0f} l12,34" stroke="#b8c8e6" stroke-width="3" stroke-linecap="round" opacity="0.75"/>'
    return doc(f'<clipPath id="a2rc{k}"><path d="{shape}"/></clipPath>' + S.g(b, extra=f'clip-path="url(#a2rc{k})"'))


def flash_svg():
    x0, x1, top, sill = WIN
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    shape = f"M{x0},{sill} L{x0},{top + r} A{r},{r} 0 0 1 {x1},{top + r} L{x1},{sill} Z"
    bolt = (f"M{cx + 40},{top + 40} L{cx - 10},{top + 190} L{cx + 30},{top + 190} L{cx - 40},{top + 360} "
            f"L{cx + 70},{top + 160} L{cx + 25},{top + 160} L{cx + 80},{top + 40} Z")
    defs = S.rad_grad("a2fl", [(0, "#f4f6ff", 1), (0.6, "#d9e2ff", 0.9), (1, "#b8c6f0", 0.7)])
    b = f'<path d="{shape}" fill="url(#a2fl)"/>'
    b += f'<path d="{bolt}" fill="#fff6c8" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    b = S.g(b, extra='clip-path="url(#a2fc)"')
    b += window_frame_svg()
    return doc(f'<clipPath id="a2fc"><path d="{shape}"/></clipPath>' + b, defs)


def lamp_glow_svg():
    x, y, s = LAMP
    defs = S.rad_grad("a2lg", [(0, "#fff0c0", 0.85), (0.35, "#ffdf9a", 0.45), (1, "#ffd890", 0)])
    return doc(f'<circle cx="{x + 30}" cy="{y - 60}" r="620" fill="url(#a2lg)"/>', defs)


def lamp_svg(lit):
    x, y, s = LAMP
    table = (f'<rect x="{x - 150}" y="{y}" width="300" height="26" rx="6" fill="{P["wood_light"]}" stroke="{INK}" '
             f'stroke-width="4"/><rect x="{x - 130}" y="{y + 26}" width="260" height="{FLOOR_Y + 10 - y - 26}" '
             f'fill="{P["wood"]}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="{x - 100}" y="{y + 60}" width="200" height="70" rx="6" fill="{P["wood_light"]}" '
             f'stroke="{INK}" stroke-width="3"/><circle cx="{x}" cy="{y + 95}" r="8" fill="{P["gold"]}" '
             f'stroke="{INK}" stroke-width="2.5"/>')
    b = S.g(table, filter="wobble-fine") + PR.oil_lamp(x, y + 2, s, lit=lit)
    if not lit:
        b += (f'<path d="M{x + 72 * s},{y - 30 * s} q-14,-24 4,-44 q16,-18 0,-40" stroke="#b9b2c4" stroke-width="6" '
              f'fill="none" stroke-linecap="round" opacity="0.8"/>')
    return doc(b)


def kid_svg(expr, marks=True):
    x, y, s = KID
    return doc(C.citizen(x, y, s, -1, kind="child", variant=1, expr=expr, marks=marks))


def quilt_svg():
    """Mattress, patchwork quilt (covering the girl from the waist down) and the bed frame, plus the floor in
    front of the bed (so whatever sinks behind the quilt is hidden)."""
    defs = S.lin_grad("a2q", [(0, "#f2b8a8"), (1, "#e49a8a")])
    b = f'<rect x="-20" y="{FLOOR_Y + 2}" width="{W + 40}" height="{H - FLOOR_Y + 30}" fill="#a87650"/>'
    for y in range(FLOOR_Y + 40, H + 40, 52):
        b += f'<path d="M-20,{y} L{W + 20},{y + 6}" stroke="#8a5a36" stroke-width="3" opacity="0.6"/>'
    b += (f'<ellipse cx="1180" cy="{FLOOR_Y + 120}" rx="520" ry="70" fill="#c9714a" stroke="{INK}" stroke-width="4"/>'
          f'<ellipse cx="1180" cy="{FLOOR_Y + 120}" rx="440" ry="48" fill="none" stroke="#f2c14e" stroke-width="6" '
          f'stroke-dasharray="18 14"/>')
    b = S.g(b, filter="wobble")
    # bed frame
    fr = (f'<rect x="580" y="830" width="880" height="80" rx="10" fill="{P["wood"]}" stroke="{INK}" stroke-width="5"/>'
          f'<rect x="600" y="905" width="40" height="{FLOOR_Y + 22 - 905}" fill="{P["wood_dark"]}" stroke="{INK}" '
          f'stroke-width="4"/><rect x="1400" y="905" width="40" height="{FLOOR_Y + 22 - 905}" '
          f'fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="4"/>'
          f'<path d="M1440,{FLOOR_Y + 5} L1440,700 Q1440,660 1480,660 L1500,660 Q1530,660 1530,700 L1530,'
          f'{FLOOR_Y + 5} Z" fill="{P["wood"]}" stroke="{INK}" stroke-width="5"/>')
    # quilt: top edge at the girl, a bump over her knees, draping over the side
    q = (f"M600,{QUILT_EDGE + 8} C650,{QUILT_EDGE - 6} 760,{QUILT_EDGE - 10} 870,{QUILT_EDGE} "
         f"C960,{QUILT_EDGE + 8} 1010,{QUILT_EDGE - 40} 1080,{QUILT_EDGE - 42} C1150,{QUILT_EDGE - 44} 1190,"
         f"{QUILT_EDGE + 2} 1260,{QUILT_EDGE + 4} C1340,{QUILT_EDGE + 6} 1420,{QUILT_EDGE + 8} 1450,{QUILT_EDGE + 20} "
         f"L1462,{FLOOR_Y + 8} C1300,{FLOOR_Y + 14} 800,{FLOOR_Y + 14} 588,{FLOOR_Y + 8} Z")
    quilt = f'<path d="{q}" fill="url(#a2q)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    patch = ""
    cols = ["#f6d36b", "#9cc3d6", "#bfd88e", "#f7e8cf"]
    k = 0
    for xx in range(640, 1440, 110):
        for yy in (QUILT_EDGE + 40, QUILT_EDGE + 95, QUILT_EDGE + 150):
            patch += (f'<rect x="{xx}" y="{yy}" width="70" height="38" rx="8" fill="{cols[k % 4]}" opacity="0.85" '
                      f'stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>')
            k += 1
    quilt += f'<clipPath id="a2qc"><path d="{q}"/></clipPath>' + S.g(patch, extra='clip-path="url(#a2qc)"')
    quilt += (f'<path d="M600,{QUILT_EDGE + 8} C650,{QUILT_EDGE - 6} 760,{QUILT_EDGE - 10} 870,{QUILT_EDGE}" '
              f'stroke="#fbf1de" stroke-width="14" fill="none" stroke-linecap="round"/>'
              f'<path d="M600,{QUILT_EDGE + 8} C650,{QUILT_EDGE - 6} 760,{QUILT_EDGE - 10} 870,{QUILT_EDGE}" '
              f'stroke="{INK}" stroke-width="3" fill="none" opacity="0.5" transform="translate(0,9)"/>')
    body = b + S.g(fr, filter="wobble-fine") + S.g(quilt, filter="wobble-fine")
    body += PR.sheep(1260, QUILT_EDGE + 8, 0.62, -1, 0, lamb=True)
    return doc(body, defs)


def fingers_svg():
    b = ""
    for x in (742, 838):
        for i in range(3):
            fx = x + (i - 1) * 15
            b += (f'<ellipse cx="{fx}" cy="{QUILT_EDGE + 2 + abs(i - 1) * 2}" rx="9" ry="13" fill="#b07a55" '
                  f'stroke="{INK}" stroke-width="3"/>')
    return doc(S.g(b, filter="wobble-fine"))


def dark_svg():
    defs = (S.rad_grad("a2dk", [(0, "#a8b2d0"), (0.5, "#7c87ad"), (1, "#5a6390")], cx=0.78, cy=0.32, r=0.75) +
            S.rad_grad("a2dk2", [(0, "#b4bcd8", 0.9), (1, "#b4bcd8", 0)]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#a2dk)"/>'
    b += f'<ellipse cx="800" cy="760" rx="260" ry="180" fill="url(#a2dk2)"/>'
    return doc(b, defs)


# ================================================================== soldiers page


def camp_sky_svg():
    defs = S.lin_grad("a2cs", [(0, "#9fbfd2"), (0.6, "#cfdcd6"), (1, "#ecdfc0")])
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#a2cs)"/>'
    b += S.g(S.cloud(420, 200, 360, 110, "#f6f1e6", seed=41, sw=3.5, shade_fill="#d3dde0") +
             S.cloud(1500, 150, 300, 96, "#f6f1e6", seed=42, sw=3.5, shade_fill="#d3dde0") +
             S.cloud(1980, 300, 240, 80, "#f3eee4", seed=43, sw=3, shade_fill="#d3dde0"), filter="wobble")
    return doc(b, defs)


def camp_land_svg():
    defs = S.lin_grad("a2cg", [(0, "#a8c66e"), (1, "#86a956")])
    far = S.path(S.hill(-200, W + 200, 570, 60, seed=12, bumps=3), fill="#c3d3b2", sw=2.5)
    tents = ""
    for x, s in ((260, 0.42), (620, 0.36), (1010, 0.4), (1420, 0.34)):
        tents += PR.tent(x, 606 - (0 if s > 0.38 else 6), s, 1, side="israel")
    pts = [(-120, 615), (300, 605), (800, 618), (1300, 630), (1700, 650), (2000, 680), (2240, 720)]
    d = S.smooth_path(pts, closed=False) + f" L2240,{H + 60} L-120,{H + 60} Z"
    land = S.path(d, fill="url(#a2cg)", sw=4)
    for x, y, rx in ((400, 900, 260), (1300, 980, 300), (1900, 880, 200)):
        land += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.15:.0f}" fill="#b6d27c" opacity="0.55"/>'
    return doc(S.g(far, filter="wobble") + PR._haze(tents, "#cfdcd6", 0.3, 0.3) + S.g(land, filter="wobble") +
               PR.olive_tree(1900, 690, 0.85, seed=3) + PR.bush(120, 650, 0.6, 0), defs)


# rows of soldiers: (x, ground y, scale, variant)
SOLDIERS = [
    (330, 712, 0.8, 2), (640, 716, 0.8, 0), (950, 720, 0.8, 3), (1260, 724, 0.8, 1), (1570, 728, 0.8, 2),
    (480, 842, 0.95, 1), (800, 848, 0.95, 3), (1120, 854, 0.95, 0), (1440, 860, 0.95, 2),
    (330, 985, 1.1, 0), (690, 990, 1.1, 2), (1050, 995, 1.1, 1), (1410, 1000, 1.1, 3),
]


def soldier_frames(x, y, s, v):
    sh = C.ground_shadow(x, y + 2, s, 140, 0.2)
    fr = [doc(sh + C.soldier(x, y, s, 1, side="israel", variant=v, pose="stand", expr="worried"))]
    for k in (0.0, 0.25, 0.5, 0.75):
        fr.append(doc(sh + C.soldier(x, y, s, 1, side="israel", variant=v, pose="cower", shake=k)))
    return fr


def shadow_svg():
    """The giant's shadow: a soft blue-grey silhouette (multiply layer) - crested helmet, bearded profile, broad
    shoulders, a fist thrust forward and the great spear raised. Drawn in local units around the neck base."""
    defs = ('<filter id="a2sil" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="11"/>'
            '</filter>')
    ox, oy, k = 1320, 615, 1.0
    parts = [
        "M-300,1000 L-280,130 Q-262,0 -120,-24 L140,-24 Q282,0 304,130 L330,1000 Z",          # torso
        "M-62,-90 L62,-90 L62,10 L-62,10 Z",                                                 # neck
        "M-150,-190 A140,140 0 1 1 130,-190 A140,140 0 1 1 -150,-190 Z",                    # head
        "M-150,-176 Q-215,-40 -80,0 Q20,-10 70,-60 L40,-150 Z",                              # beard
        "M-176,-212 L-176,-184 L172,-184 L172,-212 Z",                                       # brim
        "M-168,-198 A168,150 0 0 1 168,-198 Z",                                              # helmet dome
        "M-150,-260 C-160,-470 180,-500 215,-300 C230,-230 200,-150 175,-120 L150,-250 Z",  # crest
        "M-205,40 L-540,-80 L-500,-170 L-175,-60 Z",                                         # front arm
        "M180,30 L250,-420 L345,-405 L292,60 Z",                                             # raised arm
        "M262,1000 L282,-1160 L328,-1158 L318,1000 Z",                                       # spear shaft
        "M305,-1300 L345,-1170 L305,-1130 L262,-1170 Z",                                     # spear head
    ]
    body = "".join(f'<path d="{d}"/>' for d in parts)
    body += '<circle cx="-540" cy="-120" r="72"/><circle cx="300" cy="-440" r="66"/>'      # fists
    return doc(f'<g filter="url(#a2sil)" opacity="0.58"><g transform="translate({ox},{oy}) scale({k})" '
               f'fill="#55587e">{body}</g></g>', defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1 = ctx.lines[0], ctx.lines[1]

    # --- the title page from s01, continued (identical picture across the cross-dissolve)
    tl = load_timeline()
    c01 = context("s01_title", tl)
    starts = {s["id"]: s["start"] for s in tl["scenes"]}
    toff = starts[ctx.id] - starts["s01_title"]
    t_iris1 = 1.3
    t_iris1_end = t_iris1 + 1.15
    page_gate = lambda t: 1.0 if t < t_iris1_end + 0.05 else 0.0           # noqa: E731
    title_gate = lambda t: 1.0 - M.progress(t, 1.0, 1.45, "sine")          # noqa: E731
    cam_title, fx_title, _ = T1.title_page(sc, c01, toff, gate=page_gate, title_gate=title_gate)

    # --- bedroom timing
    t_glance = L0.start + 1.6
    t_thunder = in_chunk(L0, "比如打雷", 0.25)
    t_dark = in_chunk(L0, "比如打雷", 0.513)
    t_peek = in_chunk(L0, "比如打雷", 0.69)
    t_iris2 = max(L0.end + 0.2, L1.start - 0.75)
    t_iris2_end = t_iris2 + 0.85

    def iris(t0, t1, c):
        def rv(t):
            if t >= t1:
                return {"mode": "up", "frac": 1.0}
            return {"mode": "radial", "frac": M.progress(t, t0, t1, "sine") * 1.02, "soft": 90, "cx": c[0],
                    "cy": c[1]}
        return rv
    rv1 = iris(t_iris1, t_iris1_end, IRIS1)
    room_gate = lambda t: Tf(alpha=1.0 if (t_iris1 <= t < t_iris2_end + 0.05) else 0.0)   # noqa: E731

    sc.add("room", room_svg(), motion=room_gate, reveal=rv1)
    sc.add("rain", [rain_svg(k) for k in range(3)], motion=room_gate, reveal=rv1, wc=0.3,
           frame_at=lambda t: float(int(t / 0.09) % 3))

    def flash_env(t):
        u = t - t_thunder
        if u < 0 or u > 0.9:
            return 0.0
        return max(math.exp(-((u - 0.03) / 0.04) ** 2), 0.8 * math.exp(-((u - 0.2) / 0.06) ** 2),
                   0.35 * math.exp(-u / 0.35))
    sc.add("flash", flash_svg(), wc=0.3, motion=lambda t: Tf(alpha=min(1.0, flash_env(t) * 1.2)))
    lamp_on = lambda t: t < t_dark + 0.05                                  # noqa: E731
    sc.add("lamp_glow", lamp_glow_svg(), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=room_gate(t).alpha * (0.85 + 0.08 * math.sin(t * 7.3) + 0.05 * math.sin(t * 13))
                               * (1 - M.progress(t, t_dark + 0.03, t_dark + 0.25, "out"))))

    # the girl: neutral -> worried glance -> scared (dive) -> hidden -> peek (scared eyes, blink)
    kx, ky, ks = KID
    kid_fr = [kid_svg("neutral"), kid_svg("worried"), kid_svg("scared", marks=False), kid_svg("sleepy", marks=False)]
    t_blink = t_peek + 0.95
    kid_fa = cuts([(0, 0), (snap(t_glance), 1), (snap(t_thunder - 0.02), 2), (snap(t_blink), 3),
                   (snap(t_blink + 0.14), 2)])
    piv = (kx, QUILT_EDGE)

    def kid_m(t):
        if t < t_thunder:
            # breathing; a small turn-dip at the glance
            dip = 6 * math.sin(math.pi * min(1, max(0, (t - t_glance + 0.1) / 0.3)))
            return Tf(dy=dip + 3 * math.sin(2 * math.pi * t / 2.6), alpha=room_gate(t).alpha)
        jump = -18 * math.sin(math.pi * min(1, max(0, (t - t_thunder) / 0.16)))
        down = DIVE_DY * M.progress(t, t_thunder + 0.14, t_thunder + 0.42, "in")
        up = (DIVE_DY - PEEK_DY) * M.progress(t, t_peek, t_peek + 0.55, "sine")
        dy = jump + down - up
        if t > t_peek + 0.55:
            dy += 3 * math.sin(2 * math.pi * (t - t_peek) / 0.9)
        return Tf(dy=dy, alpha=room_gate(t).alpha, rot=(1.5 * math.sin(2 * math.pi * (t - t_peek) / 2.2)
                                                         if t > t_peek + 0.55 else 0), px=piv[0], py=piv[1])
    sc.add("kid", kid_fr, frame_at=kid_fa, motion=kid_m, reveal=rv1, seed=21)

    def quilt_m(t):
        a = room_gate(t).alpha
        if t_thunder + 0.4 < t < t_peek + 0.2:
            k = min(1, (t - t_thunder - 0.4) / 0.15, (t_peek + 0.2 - t) / 0.2)
            return Tf(dy=-2.5 * k * abs(math.sin(t * 31)), sy=1 + 0.006 * k * math.sin(t * 29),
                      alpha=a, px=820, py=900)
        return Tf(alpha=a)
    sc.add("quilt", quilt_svg(), motion=quilt_m, reveal=rv1, seed=23)
    sc.add("fingers", fingers_svg(),
           motion=lambda t: Tf(dy=30 * (1 - M.progress(t, t_peek + 0.25, t_peek + 0.6, "out")) +
                               (2 * math.sin(2 * math.pi * (t - t_peek) / 0.9) if t > t_peek + 0.6 else 0),
                               alpha=room_gate(t).alpha * M.progress(t, t_peek + 0.25, t_peek + 0.4, "linear")))
    sc.add("lamp", [lamp_svg(True), lamp_svg(False)], motion=room_gate, reveal=rv1,
           frame_at=lambda t: 0.0 if lamp_on(t) else 1.0)
    sc.add("dark", dark_svg(), wc=0, blend="multiply",
           motion=lambda t: Tf(alpha=room_gate(t).alpha * 0.95 * M.progress(t, t_dark + 0.03, t_dark + 0.4, "sine")))

    # --- soldiers page
    t_afraid = L1.at("都怕得不得了")
    t_sh0 = in_chunk(L1, "是一个巨人", 0.56)
    t_sh1 = t_sh0 + 0.7
    rv2 = iris(t_iris2, t_iris2_end, IRIS2)
    page2 = lambda t: Tf(alpha=1.0 if t >= t_iris2 else 0.0)              # noqa: E731
    sc.add("camp_sky", camp_sky_svg(), motion=page2, reveal=rv2, wc=0.6)
    sc.add("camp_land", camp_land_svg(), motion=page2, reveal=rv2)
    for i, (x, y, s, v) in enumerate(SOLDIERS):
        td = snap(t_afraid + 0.1 + 0.07 * ((i * 5) % len(SOLDIERS)))
        tj = t_sh1 + 0.04 * (i % 4)
        ph = (i * 0.37) % 1

        def fa(t, td=td, ph=ph):
            if t < td:
                return 0.0
            rate = 11 if t < t_sh0 else 15
            return 1.0 + float(int(t * rate + ph * 4) % 4)

        def mot(t, td=td, tj=tj, x=x, y=y, s=s, i=i):
            a = page2(t).alpha
            if t < td:
                return Tf(dy=2 * s * math.sin(2 * math.pi * (t / 2.8 + i * 0.13)), alpha=a)
            u = t - td
            dy = 0.0
            sy = 1.0
            if u < 0.3:
                dy = 10 * s * math.sin(math.pi * u / 0.3)
                sy = 1 - 0.05 * math.sin(math.pi * u / 0.3)
            w = t - tj
            if 0 <= w < 0.32:
                dy -= 22 * s * math.sin(math.pi * w / 0.32)
            return Tf(dy=dy, sy=sy, alpha=a, px=x, py=y)
        sc.add(f"soldier{i}", soldier_frames(x, y, s, v), frame_at=fa, motion=mot, reveal=rv2, seed=40 + i)

    def shadow_m(t):
        if t < t_sh0 - 0.05:
            return Tf(alpha=0)
        u1 = M.progress(t, t_sh0, t_sh0 + 0.32, "out")
        u2 = M.progress(t, t_sh0 + 0.38, t_sh1, "out")
        dx = 1500 * (1 - 0.55 * u1 - 0.45 * u2)
        return Tf(dx=dx + 6 * math.sin(2 * math.pi * (t - t_sh1) / 3.0), dy=4 * math.sin(2 * math.pi * t / 2.4),
                  alpha=1.0)
    sc.add("shadow", shadow_svg(), wc=0, blend="multiply", motion=shadow_m)

    # --- camera: s01's slow push continues on the title page and the bedroom; a gentle drift on the camp page
    c_end = cam_title(1.0)
    cam_room = M.cam_keys([(1.0, c_end), (t_thunder, Cam(1030, 640, 1760)), (t_peek + 0.7, Cam(885, 700, 1330)),
                           (t_iris2, Cam(880, 702, 1310))], ["sine", "sine", "sine"])
    cam_camp = M.cam_keys([(t_iris2, Cam(880, 702, 1310)), (t_afraid, Cam(950, 660, 1780)),
                           (t_sh0, Cam(960, 655, 1840)), (T, Cam(975, 650, 1880))], ["sine", "sine", "sine"])

    def cam(t):
        if t <= 1.0:
            return cam_title(t)
        c = cam_room(t) if t < t_iris2 else cam_camp(t)
        # bump on the two footfalls of the shadow
        for tb in (t_sh0 + 0.3, t_sh1):
            u = t - tb
            if 0 <= u < 0.35:
                k = math.exp(-u / 0.09) * math.sin(u * 60)
                c = Cam(c.x, c.y + 5 * k, c.w, c.rot)
        return c
    sc.camera = cam

    sc.fx = fx_title + [
        FX.lightning([t_thunder], dur=0.5, strength=0.45),
        FX.tint((40, 44, 80), lambda t: 0.16 * M.progress(t, t_sh0 + 0.1, t_sh1 + 0.3, "sine"), mode="multiply"),
    ]

    # --- sound
    sc.sfx("rain", t_iris1, dur=t_iris2_end - t_iris1 + 0.4, gain_db=-15, fade_in=0.8, fade_out=0.8)
    sc.sfx("thunder", t_thunder - 0.03, gain_db=-7)
    sc.sfx("cloth", t_thunder + 0.15, gain_db=-14)
    sc.sfx("pop", t_dark + 0.03, gain_db=-20)
    sc.sfx("cloth", t_peek + 0.05, gain_db=-18)
    sc.sfx("wind_soft", t_iris2, dur=T - t_iris2 + 0.3, gain_db=-20, fade_in=0.8, fade_out=1.0)
    sc.sfx("heartbeat", t_afraid, dur=T - t_afraid + 0.2, gain_db=-17, fade_in=0.6, fade_out=1.0)
    sc.sfx("thud", t_sh0 + 0.3, gain_db=-7)
    sc.sfx("thud", t_sh1, gain_db=-5)
    return sc
