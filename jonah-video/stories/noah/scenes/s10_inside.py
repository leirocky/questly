"""Scene 10 — inside the ark (Genesis 8:1).

'方舟里面，挪亚一家和动物们，都平平安安的。' / '外面风很大，雨很大。可是上帝一直记得挪亚，也记得方舟里的每一只动物。'

A cosy dollhouse cutaway of the ark at night (one 2112 x 1188 stage): the gable roof at the top with the dark
storm sky and rain above it (drops splash on the shingles), the upper deck with lamplight, a porthole with rain,
a bird perch where the birds sleep with their heads tucked in, Noah's tools on the wall, and the family standing
at a long supper table; through a hatch in the floor the sleeping giraffe's head pokes up from the lower deck,
where the elephants sleep with their trunks curled, the rabbits and the foxes are snuggled, two monkeys doze on a
hippo's back and the turtles sleep in the straw. The whole ark rocks very gently on the water.

  line 0  '方舟里面，'          calm, everyone safe; the lanterns sway softly.
          '挪亚一家和动物们，'  the family laughs together at the table (laugh, small dips), the hippo yawns.
          '都平平安安的。'      calm, breathing.
  line 1  '外面风很大，雨很大。'  the rain outside gets heavier, wind streaks whoosh through the sky, the lanterns swing
                                a little more, the ark rolls a touch more.
          '可是上帝一直记得挪亚，' a soft golden glow spreads from the roof over everyone; the family fold their hands
                                and lift their faces (pray).
          '也记得方舟里的每一只动物。' each sleeping animal gets its own tiny sparkle, one after another.
  calm warm last frame (dip to black into s11).
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s11_belly import phrase_t
from art.scenes.s17_king import cuts, dip, hop, snap
from art.style import P, W, H
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

INK = P["ink"]
K = 0.72                     # everybody's scale
RIDGE = (1056, 58)           # roof ridge (outer)
EAVE_Y = 236                 # outer roof line at x = -40 / W + 40
ROOF_T = 40                  # roof thickness
UF_BACK, UF_FRONT, UF_BEAM = 650, 722, 760     # upper floor: back edge, front edge, bottom of the cut beam
LF_BACK, LF_FRONT = 912, 995                   # lower floor
UY = 700                     # upper-deck feet (front row)
LY = 968                     # lower-deck feet
GIR = (830, LY)              # giraffe
HATCH = (700, 1012)          # the giraffe well: an opening in the upper floor, x0, x1
PORT_U = (210, 420, 66)      # upper porthole cx, cy, r
PORT_L = (1590, 836, 40)     # lower porthole
PORT_R = (1985, 400, 52)     # porthole by the table
GX = 1600                    # family group centre
TABLE = (1262, 1872, 612)    # table x0, x1, top surface y
LAMP_U = (1600, 262)         # upper lantern hook
LAMP_L = (1015, UF_BEAM)     # lower lantern hook
PERCH = (330, 770, 452)      # bird perch x0, x1, y


def doc(body, defs=""):
    return S.svg_doc(body, defs)


def f1(v):
    return f"{v:.1f}"


def roof_y(x, inner=False):
    """y of the roof's outer line (or the ceiling line under it) at x."""
    x0 = -40
    u = abs(x - RIDGE[0]) / (RIDGE[0] - x0)
    y = RIDGE[1] + (EAVE_Y - RIDGE[1]) * u
    return y + (ROOF_T if inner else 0)


def gtime(ctx):
    return lambda t: ctx.start + t


# ============================================================================ backdrops


def sky_svg():
    defs = S.lin_grad("s10sky", [(0, "#1f2940"), (0.6, "#2e3a55"), (1, "#3c4a66")])
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="{EAVE_Y + 80}" fill="url(#s10sky)"/>'
    for i, (cx, cy, w, h) in enumerate(((240, 70, 520, 120), (900, 30, 600, 110), (1700, 80, 640, 130),
                                        (2050, 40, 420, 100))):
        body += S.g(S.cloud(cx, cy, w, h, fill="#46536c", seed=20 + i, puffs=6, sw=2.5, shade_fill="#3a4660"),
                    opacity=0.9)
    return doc(S.g(body, filter="wobble"), defs)


def interior_svg():
    """Walls, ceiling, floors, beams, stall posts, porthole openings (painted night outside) — static."""
    defs = (S.lin_grad("s10wall", [(0, "#7a4f31"), (0.5, "#a06b42"), (1, "#b47a4a")]) +
            S.lin_grad("s10wall2", [(0, "#6e4a30"), (1, "#8f6040")]) +
            S.lin_grad("s10floor", [(0, "#a8784a"), (1, "#c08a56")]) +
            S.lin_grad("s10floor2", [(0, "#8d6440"), (1, "#a57548")]) +
            S.lin_grad("s10port", [(0, "#1e2a42"), (1, "#36486a")]) +
            S.lin_grad("s10hull", [(0, "#6a4228"), (1, "#4e3020")]))
    b = ""
    # upper deck back wall (under the roof)
    ceil = f"M-40,{f1(roof_y(-40, True))} L{RIDGE[0]},{RIDGE[1] + ROOF_T} L{W + 40},{f1(roof_y(W + 40, True))} " \
           f"L{W + 40},{UF_BACK} L-40,{UF_BACK} Z"
    b += f'<path d="{ceil}" fill="url(#s10wall)"/>'
    # vertical wall boards
    for x in range(-30, W + 40, 64):
        y0 = roof_y(x, True)
        b += f'<path d="M{x},{f1(y0)} L{x},{UF_BACK}" stroke="#7d5232" stroke-width="3" opacity="0.7"/>'
        if (x // 64) % 3 == 0:
            yy = UF_BACK - 90 - (x * 7) % 140
            b += f'<circle cx="{x + 32}" cy="{yy}" r="3" fill="#6a4228"/>'
    # rafters under the roof (sloping beams) and a cross tie beam
    for x in range(40, W, 210):
        yt = roof_y(x, True)
        b += (f'<path d="M{x - 14},{f1(yt - 4)} L{x + 14},{f1(yt - 4)} L{x + 14},{f1(yt + 46)} L{x - 14},{f1(yt + 46)} Z" '
              f'fill="#6a4228" {S.STROKE_THIN}/>')
    b += S.path(f"M-40,{f1(roof_y(-40, True))} L{RIDGE[0]},{RIDGE[1] + ROOF_T} L{W + 40},{f1(roof_y(W + 40, True))}",
                sw=4)
    tie = 268
    b += f'<rect x="-40" y="{tie}" width="{W + 80}" height="26" fill="#7a4c2c" {S.STROKE}/>'
    for x in range(120, W, 300):
        b += f'<circle cx="{x}" cy="{tie + 13}" r="4" fill="#4e3020"/>'
    # upright posts of the upper deck (frame)
    for x in (70, 1170, 2050):
        b += f'<rect x="{x - 18}" y="{tie + 26}" width="36" height="{UF_BACK - tie - 26}" fill="#87573a" {S.STROKE}/>'
    # portholes (painted night outside; the rain goes on top)
    for cx, cy, r in (PORT_U, PORT_L, PORT_R):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#s10port)"/>'
        b += f'<circle cx="{cx - r * 0.3}" cy="{cy + r * 0.45}" r="{r * 0.5}" fill="#2a3a58" opacity="0.6"/>'
    # upper floor: surface with receding boards, with the giraffe's well cut out of it
    h0, h1 = HATCH
    for xa, xb in ((-40, h0), (h1, W + 40)):
        b += f'<path d="M{xa},{UF_BACK} L{xb},{UF_BACK} L{xb},{UF_FRONT} L{xa},{UF_FRONT} Z" fill="url(#s10floor)"/>'
        for x in range(xa + 30, xb, 90):
            b += f'<path d="M{x},{UF_BACK} L{x + (x - W / 2) * 0.12:.1f},{UF_FRONT}" stroke="#94643c" stroke-width="2.5"/>'
        b += f'<path d="M{xa},{UF_BACK + 30} L{xb},{UF_BACK + 30}" stroke="#94643c" stroke-width="2" opacity="0.6"/>'
    # through the well: the lower deck's back wall runs up to the upper floor line
    b += f'<rect x="{h0}" y="{UF_BACK}" width="{h1 - h0}" height="{UF_BEAM - UF_BACK + 2}" fill="#7a5034"/>'
    for x in range(h0 + 20, h1, 58):
        b += f'<path d="M{x},{UF_BACK} L{x},{UF_BEAM}" stroke="#5e3e28" stroke-width="3" opacity="0.7"/>'
    # lower deck back wall
    b += f'<rect x="-40" y="{UF_BEAM}" width="{W + 80}" height="{LF_BACK - UF_BEAM}" fill="url(#s10wall2)"/>'
    for x in range(-20, W + 40, 58):
        b += f'<path d="M{x},{UF_BEAM} L{x},{LF_BACK}" stroke="#5e3e28" stroke-width="3" opacity="0.7"/>'
    # stall posts and low partitions (seen edge-on)
    for x in (640, 1060, 1335, 1640):
        b += f'<rect x="{x - 14}" y="{UF_BEAM}" width="28" height="{LF_BACK - UF_BEAM + 30}" fill="#7a4c2c" {S.STROKE}/>'
        b += (f'<path d="M{x - 60},{LF_BACK - 70} L{x + 60},{LF_BACK - 70}" stroke="{INK}" stroke-width="16" '
              f'stroke-linecap="round"/><path d="M{x - 60},{LF_BACK - 70} L{x + 60},{LF_BACK - 70}" stroke="#a06b42" '
              f'stroke-width="9" stroke-linecap="round"/>')
    # lower floor (straw-covered)
    b += f'<path d="M-40,{LF_BACK} L{W + 40},{LF_BACK} L{W + 40},{LF_FRONT} L-40,{LF_FRONT} Z" fill="url(#s10floor2)"/>'
    rng = random.Random(5)
    straw = ""
    for _ in range(260):
        x = rng.uniform(-30, W + 30)
        y = rng.uniform(LF_BACK + 6, LF_FRONT - 4)
        a = rng.uniform(-0.6, 0.6)
        ln = rng.uniform(14, 30)
        straw += f'<path d="M{f1(x)},{f1(y)} l{f1(ln * math.cos(a))},{f1(ln * math.sin(a))}"/>'
    b += f'<g stroke="#e2c070" stroke-width="3" stroke-linecap="round" opacity="0.75">{straw}</g>'
    # hull below the lower floor (cut face)
    b += f'<rect x="-40" y="{LF_FRONT}" width="{W + 80}" height="{H - LF_FRONT + 40}" fill="url(#s10hull)"/>'
    for y in (LF_FRONT + 40, LF_FRONT + 90, LF_FRONT + 140):
        b += f'<path d="M-40,{y} L{W + 40},{y}" stroke="#3e2618" stroke-width="3"/>'
    b += S.path(f"M-40,{LF_FRONT} L{W + 40},{LF_FRONT}", sw=5)
    b += S.path(f"M-40,{LF_BACK} L{W + 40},{LF_BACK}", sw=3.5)
    b += S.path(f"M-40,{UF_BACK} L{W + 40},{UF_BACK}", sw=3.5)
    return doc(S.g(b, filter="wobble"), defs)


def beam_svg():
    """The upper floor's cut beam face (drawn IN FRONT of the giraffe so its neck goes through the hatch)."""
    h0, h1 = HATCH
    b = ""
    for xa, xb in ((-40, h0), (h1, W + 40)):
        b += f'<rect x="{xa}" y="{UF_FRONT}" width="{xb - xa}" height="{UF_BEAM - UF_FRONT}" fill="#6e4429"/>'
        for x in range(30, W, 170):
            if xa < x and x + 40 < xb:
                b += f'<rect x="{x}" y="{UF_FRONT + 7}" width="40" height="{UF_BEAM - UF_FRONT - 14}" rx="6" ' \
                     f'fill="#86573a" {S.STROKE_THIN}/>'
        b += S.path(f"M{xa},{UF_FRONT} L{xb},{UF_FRONT} L{xb},{UF_BEAM} L{xa},{UF_BEAM}", sw=4.5)
    # the well's cut floor edges
    for x in (h0, h1):
        b += f'<path d="M{x},{UF_BACK} L{x},{UF_FRONT}" stroke="{INK}" stroke-width="4"/>'
    return doc(S.g(b, filter="wobble"))


def roof_svg():
    """The roof's cut edge (shingles) over everything."""
    x0, x1 = -40, W + 40
    outer = f"M{x0},{EAVE_Y} L{RIDGE[0]},{RIDGE[1]} L{x1},{EAVE_Y}"
    inner = f"L{x1},{EAVE_Y + ROOF_T} L{RIDGE[0]},{RIDGE[1] + ROOF_T} L{x0},{EAVE_Y + ROOF_T} Z"
    b = f'<path d="{outer} {inner}" fill="#8e4a30" {S.STROKE}/>'
    # shingle ticks
    for x in range(-20, W + 40, 46):
        y = roof_y(x)
        b += f'<path d="M{x},{f1(y + 4)} L{x - 6},{f1(y + ROOF_T - 6)}" stroke="#6e3420" stroke-width="3"/>'
    b += f'<path d="M{x0},{EAVE_Y + 14} L{RIDGE[0]},{RIDGE[1] + 14} L{x1},{EAVE_Y + 14}" fill="none" ' \
         f'stroke="#a85c3c" stroke-width="5"/>'
    return doc(S.g(b, filter="wobble"))


def sky_rain_svg(phase, heavy):
    """Rain above the roof (clipped to the sky) + little splashes on the shingles."""
    clip = f"M-40,-40 L{W + 40},-40 L{W + 40},{EAVE_Y} L{RIDGE[0]},{RIDGE[1]} L-40,{EAVE_Y} Z"
    rain = PR.rain(phase, 1.05 if heavy else 0.62, -40, -20, W + 40, EAVE_Y + 10, angle=16 if heavy else 9,
                   seed=3)
    b = f'<clipPath id="s10rc"><path d="{clip}"/></clipPath><g clip-path="url(#s10rc)">{rain}</g>'
    rng = random.Random(int(phase * 100) + (7 if heavy else 0))
    spl = ""
    for _ in range(26 if heavy else 15):
        x = rng.uniform(-20, W + 20)
        y = roof_y(x) - 2
        k = rng.uniform(0.7, 1.2)
        spl += (f'<path d="M{f1(x - 12 * k)},{f1(y - 4 * k)} l{f1(-6 * k)},{f1(-9 * k)} M{f1(x)},{f1(y - 6 * k)} '
                f'l0,{f1(-12 * k)} M{f1(x + 12 * k)},{f1(y - 4 * k)} l{f1(6 * k)},{f1(-9 * k)}"/>')
    b += f'<g stroke="#c9d6e6" stroke-width="3" stroke-linecap="round" opacity="0.85">{spl}</g>'
    return doc(b)


def port_rain_svg(port, phase, heavy, tag):
    cx, cy, r = port
    rain = PR.rain(phase, 1.1 if heavy else 0.7, cx - r, cy - r, cx + r, cy + r, angle=18 if heavy else 10,
                   seed=11 + cx % 7, scale=0.7)
    b = (f'<clipPath id="s10p{tag}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
         f'<g clip-path="url(#s10p{tag})">{rain}</g>')
    return doc(b)


def port_frames_svg():
    b = ""
    for cx, cy, r in (PORT_U, PORT_L, PORT_R):
        b += (f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="#c4904c" stroke-width="18"/>'
              f'<circle cx="{cx}" cy="{cy}" r="{r + 18}" fill="none" {S.STROKE}/>'
              f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" {S.STROKE}/>'
              f'<path d="M{cx - r * 0.55},{cy - r * 0.5} q{r * 0.2},{-r * 0.25} {r * 0.5},{-r * 0.3}" fill="none" '
              f'stroke="#fffaf0" stroke-width="4" stroke-linecap="round" opacity="0.5"/>')
        for a in range(0, 360, 60):
            ra = math.radians(a + 30)
            b += f'<circle cx="{f1(cx + (r + 9) * math.cos(ra))}" cy="{f1(cy + (r + 9) * math.sin(ra))}" r="3.5" fill="#6a4228"/>'
    return doc(S.g(b, filter="wobble-fine"))


def wall_dress_svg():
    """Things on the upper-deck walls and floor: tools on pegs, shelves of jars, sacks, the perch ropes."""
    b = ""
    # shelf with jars near the right porthole
    b += f'<rect x="1880" y="520" width="170" height="16" fill="#8a5a35" {S.STROKE_THIN}/>'
    for i, x in enumerate((1905, 1960, 2015)):
        b += PR.jar(x, 485, 0.38, color=["#c9714a", "#b8865a", "#c98a4a"][i])
    # Noah's tools hanging on pegs
    b += f'<circle cx="1230" cy="360" r="6" fill="#5a3a24"/><circle cx="1300" cy="380" r="6" fill="#5a3a24"/>'
    b += PR.saw(1232, 366, 0.55, 1, rot=78)
    b += PR.hammer(1300, 386, 0.6, 1, rot=88)
    # food stores on the floor at the left
    b += PR.sack(420, UY + 2, 0.55, seed=1) + PR.sack(488, UY + 6, 0.5, seed=3)
    b += PR.hay(575, UY + 4, 0.5, kind="bale") + PR.food_basket(1090, UY + 6, 0.5, kind="veg")
    b += PR.jar(355, UY - 40, 0.42)
    # the perch: a pole hanging from the tie beam on two ropes
    x0, x1, y = PERCH
    for x in (x0 + 30, x1 - 30):
        b += f'<path d="M{x},294 L{x},{y}" stroke="{INK}" stroke-width="7"/><path d="M{x},294 L{x},{y}" ' \
             f'stroke="#c9a46a" stroke-width="3.5" stroke-dasharray="7 5"/>'
    b += f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="16" rx="8" fill="#9a6a40" {S.STROKE}/>'
    return doc(S.g(b, filter="wobble-fine"))


def sleep_bird(x, y, s, f, body, wing, breast, beak="#e89a6a"):
    """A little bird asleep on a perch, head tucked in, eye closed. (x, y) = feet on the perch."""
    def X(dx):
        return f1(x + f * dx * s)

    def Y(dy):
        return f1(y + dy * s)
    sw = f'stroke="{INK}" stroke-width="{f1(3.2 * s)}" stroke-linejoin="round" stroke-linecap="round"'
    g = (f'<path d="M{X(-22)},{Y(-26)} L{X(-50)},{Y(-14)} L{X(-46)},{Y(-30)} Z" fill="{wing}" {sw}/>'
         f'<ellipse cx="{X(0)}" cy="{Y(-26)}" rx="{f1(30 * s)}" ry="{f1(23 * s)}" fill="{body}" {sw}/>'
         f'<ellipse cx="{X(6)}" cy="{Y(-18)}" rx="{f1(17 * s)}" ry="{f1(12 * s)}" fill="{breast}"/>'
         f'<path d="M{X(-20)},{Y(-34)} Q{X(0)},{Y(-48)} {X(14)},{Y(-30)} Q{X(0)},{Y(-14)} {X(-18)},{Y(-20)} Z" '
         f'fill="{wing}" {sw}/>'
         f'<circle cx="{X(20)}" cy="{Y(-42)}" r="{f1(14 * s)}" fill="{body}" {sw}/>'
         f'<path d="M{X(14)},{Y(-44)} q{f1(f * 5 * s)},{f1(4 * s)} {f1(f * 10 * s)},0" fill="none" {sw}/>'
         f'<path d="M{X(32)},{Y(-40)} L{X(41)},{Y(-36)} L{X(32)},{Y(-33)} Z" fill="{beak}" '
         f'stroke="{INK}" stroke-width="{f1(2 * s)}" stroke-linejoin="round"/>'
         f'<circle cx="{X(24)}" cy="{Y(-35)}" r="{f1(3.5 * s)}" fill="{P["cheek"]}" opacity="0.7"/>'
         f'<path d="M{X(-6)},{Y(-4)} l0,{f1(5 * s)} M{X(6)},{Y(-4)} l0,{f1(5 * s)}" stroke="#d28a5a" '
         f'stroke-width="{f1(3 * s)}" stroke-linecap="round"/>')
    return g


BIRDS = [  # x on the perch, scale, facing, body, wing, breast
    (380, 1.0, 1, "#f6efe4", "#c9bede", "#f3d2cf"),      # doves
    (438, 0.95, -1, "#f6efe4", "#c9bede", "#f3d2cf"),
    (530, 0.72, 1, "#6f9fd6", "#4f7fb8", "#f2dca6"),     # bluebirds
    (578, 0.7, -1, "#7aa8da", "#5a86bc", "#f2dca6"),
    (668, 0.72, 1, "#d9584a", "#b14438", "#f2c79a"),     # robins
    (716, 0.7, -1, "#e0705a", "#ba5040", "#f2c79a"),
]


def birds_svg():
    b = "".join(sleep_bird(x, PERCH[2] + 2, s, f, *cols) for x, s, f, *cols in BIRDS)
    return doc(S.g(b, filter="wobble-fine"))


def table_svg():
    x0, x1, ty = TABLE
    b = ""
    for lx in (x0 + 50, x1 - 50):
        b += f'<path d="M{lx - 12},{ty + 30} L{lx - 22},{UY + 26} L{lx + 22},{UY + 26} L{lx + 12},{ty + 30} Z" ' \
             f'fill="#7a4c2c" {S.STROKE}/>'
    b += (f'<path d="M{x0},{ty} L{x1},{ty} L{x1 + 6},{ty + 30} L{x0 - 6},{ty + 30} Z" fill="#9a6440" {S.STROKE}/>'
          f'<path d="M{x0 + 8},{ty + 3} L{x1 - 8},{ty + 3}" stroke="#b97d4e" stroke-width="5"/>')
    # cloth runner
    b += (f'<path d="M{x0 + 120},{ty - 1} L{x1 - 120},{ty - 1} L{x1 - 116},{ty + 44} L{x1 - 150},{ty + 36} '
          f'L{x0 + 150},{ty + 36} L{x0 + 116},{ty + 44} Z" fill="#e9dcc0" {S.STROKE_THIN}/>')
    b += (f'<path d="M{x0 + 4},{ty + 28} L{x1 - 4},{ty + 28} L{x1 - 14},{UY + 14} Q{(x0 + x1) / 2},{UY + 24} {x0 + 14},{UY + 14} Z" '
          f'fill="#e3d2b0" {S.STROKE}/>')
    for k in range(1, 9):
        xx = x0 + (x1 - x0) * k / 9
        b += f'<path d="M{f1(xx)},{ty + 34} q-6,40 2,{UY - ty - 14}" fill="none" stroke="#c9b48c" stroke-width="3"/>'
    b += f'<path d="M{x0 + 10},{UY - 6} L{x1 - 10},{UY - 6}" stroke="#c9714a" stroke-width="7" stroke-dasharray="18 12"/>'
    b += f'<path d="M{x0 + 130},{ty + 20} L{x1 - 130},{ty + 20}" stroke="#c9714a" stroke-width="4" stroke-dasharray="14 10"/>'
    b += PR.bread_basket(1470, ty + 4, 0.48, handle=False)
    b += PR.food_basket(1730, ty + 4, 0.44, kind="fruit")
    b += PR.jar(1335, ty - 34, 0.4)
    for cx in (1380, 1590, 1655, 1810):   # cups
        b += (f'<path d="M{cx - 13},{ty - 30} L{cx + 13},{ty - 30} L{cx + 9},{ty} L{cx - 9},{ty} Z" fill="#c9714a" '
              f'{S.STROKE_THIN}/><ellipse cx="{cx}" cy="{ty - 30}" rx="13" ry="4" fill="#8a3e2a"/>')
    b += (f'<ellipse cx="1540" cy="{ty - 4}" rx="40" ry="9" fill="#e9dcc0" {S.STROKE_THIN}/>'
          f'<ellipse cx="1532" cy="{ty - 14}" rx="22" ry="11" fill="#d9a35a" {S.STROKE_THIN}/>')
    return doc(S.g(b, filter="wobble-fine"))


# ============================================================================ helpers


def stars_fx(cues, color=(255, 236, 170), life=None):
    """Single sparkles: cues = [(x, y, t0, size)] in stage px; each pops in, twinkles and settles to a glint
    (or, with ``life`` seconds, fades out completely)."""
    def fx(frame, t, view):
        live = [(x, y, t0, s) for x, y, t0, s in cues if t >= t0]
        if not live:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for x, y, t0, s in live:
            u = t - t0
            k = min(1.0, u / 0.18)
            env = k * (1.0 if u < 0.6 else 0.35 + 0.65 * math.exp(-(u - 0.6) / 0.5))
            if life is not None:
                env *= 1 - M.progress(u, life - 0.5, life, "sine")
                if env <= 0.003:
                    continue
            tw = 0.75 + 0.25 * math.sin(2 * math.pi * (u / 0.9) + x)
            ox, oy = view.to_out(x, y - 10 * min(u, 2.0))
            r = s * view.scale * (0.6 + 0.6 * k) * tw * (1.3 if u < 0.35 else 1.0)
            a = int(240 * env * tw)
            w, gl = r * 0.2, r * 0.6
            d.ellipse([ox - gl, oy - gl, ox + gl, oy + gl], fill=(*color, a // 4))
            d.polygon([(ox, oy - r), (ox + w, oy - w), (ox + r, oy), (ox + w, oy + w), (ox, oy + r),
                       (ox - w, oy + w), (ox - r, oy), (ox - w, oy - w)], fill=(*color, a))
        frame.alpha_composite(ov)
        return frame
    return fx


def breathe_at(pivot, amount=0.012, period=3.2, phase=0.0):
    return M.breathe(amount, period, pivot=pivot, phase=phase)


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1 = ctx.line(0), ctx.line(1)
    g = gtime(ctx)

    t_family = phrase_t(L0, "挪亚一家")
    t_animals = phrase_t(L0, "动物们")
    t_wind = L1.at("外面风很大")
    t_rem = L1.at("上帝一直记得挪亚")
    t_each = L1.at("每一只动物")
    t_each_end = L1.chunks[-1].end if L1.chunks else L1.end

    # rain strength: gentle -> heavy on '外面风很大，雨很大' -> eases a little when God's glow comes
    def heavy(t):
        return M.progress(t, t_wind - 0.3, t_wind + 0.5, "sine") * (1 - 0.6 * M.progress(t, t_rem + 0.5, t_rem + 2.5))

    # ---------------------------------------------------------------- sky + rain above the roof
    sc.add("sky", sky_svg(), seed=3)
    NPH = 6
    rain_l = [sky_rain_svg(i / NPH, False) for i in range(NPH)]
    rain_h = [sky_rain_svg(i / NPH, True) for i in range(NPH)]
    ph = lambda t: float(int(t / 0.07) % NPH)                       # noqa: E731
    sc.add("rain_l", rain_l, frame_at=ph, wc=0.3, motion=lambda t: Tf(alpha=1 - heavy(t)))
    sc.add("rain_h", rain_h, frame_at=ph, wc=0.3, motion=lambda t: Tf(alpha=heavy(t)))
    # wind streaks across the sky on '外面风很大'
    wind = ""
    for i, (x, y, ln) in enumerate(((260, 120, 360), (820, 70, 420), (1350, 150, 380), (1780, 95, 330))):
        wind += (f'<path d="M{x},{y} q{ln * 0.35},-26 {ln * 0.7},0 t{ln * 0.3},-6 q36,-10 26,-36 q-14,-16 -30,4" '
                 f'fill="none" stroke="#c9d6e6" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
    sc.add("wind", doc(wind), wc=0, motion=M.keys(
        [(t_wind - 0.2, {"dx": -260, "alpha": 0}), (t_wind + 0.4, {"alpha": 1}), (t_wind + 1.8, {"alpha": 0.9}),
         (t_wind + 2.6, {"dx": 420, "alpha": 0})], "linear"))

    # ---------------------------------------------------------------- the interior
    sc.add("interior", interior_svg(), seed=5)
    for i, port in enumerate((PORT_U, PORT_L, PORT_R)):
        fl = [port_rain_svg(port, k / 4, False, f"{i}l{k}") for k in range(4)]
        fh = [port_rain_svg(port, k / 4, True, f"{i}h{k}") for k in range(4)]
        pf = lambda t, i=i: float(int(t / 0.08 + i) % 4)             # noqa: E731
        sc.add(f"prain_l{i}", fl, frame_at=pf, wc=0, motion=lambda t: Tf(alpha=1 - heavy(t)))
        sc.add(f"prain_h{i}", fh, frame_at=pf, wc=0, motion=lambda t: Tf(alpha=heavy(t)))
    sc.add("port_frames", port_frames_svg(), seed=9)
    sc.add("wall_dress", wall_dress_svg(), seed=11)

    # ---------------------------------------------------------------- birds asleep on the perch (gentle bob)
    perch_sway = lambda t: Tf(rot=0.5 * math.sin(2 * math.pi * g(t) / 4.6), px=(PERCH[0] + PERCH[1]) / 2, py=294)  # noqa
    sc.add("birds", birds_svg(), motion=M.combine(perch_sway, breathe_at(((PERCH[0] + PERCH[1]) / 2, PERCH[2]),
                                                                         0.01, 2.6)))

    # ---------------------------------------------------------------- lower deck animals (behind the beam face)
    def animal(name, kind, x, y, f=1, pose="stand", female=False, eyes="closed", per=3.2, ph_=0.0, amount=0.014,
               shadow=200):
        body = C.ground_shadow(x, y + 2, K, shadow, 0.22) + PR.ark_animal(x, y, K, f, kind, pose, female, eyes)
        sc.add(name, doc(body), motion=breathe_at((x, y), amount, per, ph_))

    animal("ele_f", "elephant", 425, LY - 18, 1, "sleep", True, per=3.8, ph_=0.4, shadow=380)
    animal("ele_m", "elephant", 300, LY + 8, 1, "sleep", per=4.1, shadow=420)
    sc.add("hay_l", doc(PR.hay(1010, LY + 12, 0.6, kind="pile")))
    animal("turtle_f", "turtle", 690, LY - 2, -1, female=True, per=3.0, ph_=0.3, shadow=120)
    animal("turtle_m", "turtle", 600, LY + 14, 1, per=3.3, shadow=130)
    animal("rabbit_f", "rabbit", 1236, LY + 4, -1, "sleep", True, per=2.2, ph_=0.5, shadow=150)
    animal("rabbit_m", "rabbit", 1112, LY + 10, 1, "sleep", per=2.4, shadow=150)
    animal("fox_f", "fox", 1540, LY - 2, -1, "sleep", True, per=2.9, ph_=0.2, shadow=220)
    animal("fox_m", "fox", 1400, LY + 10, 1, "sleep", per=3.1, shadow=230)
    animal("hippo_f", "hippo", 1985, LY - 14, -1, female=True, per=3.6, ph_=0.6, shadow=320)
    # the hippo (with two monkeys asleep on his back) yawns on '动物们'
    hx, hy = 1745, LY + 10
    t_yawn = snap(t_animals + 0.15)
    t_yawn_end = snap(t_yawn + 1.25)
    hippo = [doc(C.ground_shadow(hx, hy + 2, K, 330, 0.22) + PR.ark_animal(hx, hy, K, 1, "hippo", "stand", eyes="closed")),
             doc(C.ground_shadow(hx, hy + 2, K, 330, 0.22) + PR.ark_animal(hx, hy, K, 1, "hippo", "yawn"))]
    sc.add("hippo_m", hippo, frame_at=cuts([(0, 0), (t_yawn, 1), (t_yawn_end, 0)]),
           motion=M.combine(breathe_at((hx, hy), 0.014, 3.4), dip(t_yawn, K, (hx, hy), 5),
                            dip(t_yawn_end, K, (hx, hy), 4),
                            hop(t_yawn, [(0, {"rot": 0}), (0.5, {"rot": -1.2}), (1.2, {"rot": 0})], (hx - 120, hy))))
    mk = 0.66 * K / K
    monk = (PR.ark_animal(hx - 30, hy - 112, K * mk, 1, "monkey", "sit", eyes="closed") +
            PR.ark_animal(hx + 40, hy - 116, K * mk * 0.95, -1, "monkey", "sit", female=True, eyes="closed"))
    sc.add("monkeys", doc(monk), motion=M.combine(
        breathe_at((hx, hy - 112), 0.016, 2.7, 0.3),
        hop(t_yawn, [(0, {"rot": 0}), (0.5, {"rot": -1.2}), (1.2, {"rot": 0})], (hx - 120, hy))))

    # the giraffe: body below, neck up through the hatch (the beam face is drawn in front of it)
    gx, gy = GIR
    sc.add("giraffe", doc(C.ground_shadow(gx, gy + 2, K, 220, 0.22) + PR.ark_animal(gx, gy, K, 1, "giraffe", "stand",
                                                                                    eyes="closed")),
           motion=M.combine(breathe_at((gx, gy), 0.008, 3.9, 0.2),
                            lambda t: Tf(rot=0.8 * math.sin(2 * math.pi * g(t) / 5.3), px=gx + 60, py=gy - 280)))
    sc.add("beam", beam_svg(), seed=13)

    # ---------------------------------------------------------------- lower lantern (hangs from the beam)
    def lantern_layer(name, hook, amp_fn, per, ph_=0.0, s=0.62):
        lx, ly = hook
        sc.add(name, doc(f'<path d="M{lx},{ly - 4} L{lx},{ly + 2}" stroke="{INK}" stroke-width="4"/>' +
                         PR.lantern(lx, ly, s, lit=True)), wc=0.5,
               motion=lambda t: Tf(rot=amp_fn(t) * math.sin(2 * math.pi * (g(t) / per + ph_)), px=lx, py=ly))

    swing = lambda base: (lambda t: base * (1 + 1.6 * heavy(t)))      # noqa: E731
    lantern_layer("lantern_l", LAMP_L, swing(3.0), 3.1, 0.3)

    # ---------------------------------------------------------------- the family at the table (upper deck)
    s_back = K * 0.97
    yb = UY - 30
    fam = [  # name, x, y, scale, facing, base pose/expr
        ("daughter_in_law1", GX - 245, yb, s_back, 1, dict(pose="stand", expr="happy")),
        ("shem", GX - 122, yb, s_back, 1, dict(pose="talk", expr="happy")),
        ("ham", GX, yb, s_back, -1, dict(pose="stand", expr="happy")),
        ("japheth", GX + 122, yb, s_back, -1, dict(pose="talk", expr="happy")),
        ("daughter_in_law0", GX - 184, UY, K, 1, dict(pose="stand", expr="happy")),
        ("noah_wife", GX - 61, UY, K, 1, dict(pose="carry", item="basket")),
        ("noah", GX + 61, UY, K, -1, dict(pose="talk", expr="happy")),
        ("daughter_in_law2", GX + 184, UY, K, -1, dict(pose="stand", expr="happy")),
    ]
    for i, (name, x, y, s, f, base) in enumerate(fam):
        laugh = dict(base, expr="laugh")
        if name == "noah_wife":
            laugh = dict(pose="carry", item="basket", expr="laugh")
        if name in ("noah", "ham"):
            laugh = dict(base, pose="talk" if name == "noah" else "stand", expr="laugh")
        pray = dict(pose="pray")

        def fm(**kw):
            kw = dict(kw)
            nm = name
            if nm.startswith("daughter_in_law"):
                return C.daughter_in_law(x, y, s, f, variant=int(nm[-1]), **kw)
            return C.family_member(nm, x, y, s, f, **kw)
        frames = [doc(fm(**base)), doc(fm(**laugh)), doc(fm(**pray))]
        tl = snap(t_family + 0.1 + 0.06 * (i % 4))
        tl_end = snap(tl + 1.5 + 0.1 * (i % 3))
        tp = snap(t_rem + 0.25 + 0.07 * ((i * 3) % 8))
        piv = (x, y)
        sc.add(f"fam_{name}", frames, frame_at=cuts([(0, 0), (tl, 1), (tl_end, 0), (tp, 2)]),
               motion=M.combine(dip(tl, s, piv, 6), dip(tl_end, s, piv, 4), dip(tp, s, piv, 7),
                                hop(tl + 0.3, [(0, {"dy": 0}), (0.18, {"dy": -6 * s}), (0.36, {"dy": 0}),
                                               (0.54, {"dy": -4 * s}), (0.72, {"dy": 0})], piv),
                                breathe_at(piv, 0.01, 2.8 + 0.23 * i, 0.13 * i)))
    sc.add("table", table_svg(), seed=17)

    # upper lantern over the table (in front of the family's heads? no: above them, hung from the tie beam)
    lantern_layer("lantern_u", LAMP_U, swing(2.4), 2.7)

    # ---------------------------------------------------------------- the roof edge over the interior
    sc.add("roof", roof_svg(), seed=19)

    # ---------------------------------------------------------------- warm light
    lg = S.rad_grad("s10lg", [(0, "#7a4a14", 1), (0.4, "#4e2c0c", 0.55), (1, "#000000", 0)])
    for i, (x, y, r) in enumerate(((LAMP_U[0], LAMP_U[1] + 90, 520), (LAMP_L[0], LAMP_L[1] + 90, 430))):
        sc.add(f"lampglow{i}", doc(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#s10lg)"/>', lg), wc=0,
               blend="add", motion=M.combine(M.pulse(0.8, 1.0, 0.9 + 0.17 * i, 0.3 * i)))
    # God remembers: a soft golden glow spreads from the roof over everyone
    gc = (RIDGE[0], 330)
    gg = S.rad_grad("s10gg", [(0, "#ffe7a0", 0.85), (0.45, "#f7cf78", 0.45), (1, "#f2c14e", 0)])
    sc.add("god_glow", doc(f'<ellipse cx="{gc[0]}" cy="{gc[1]}" rx="1250" ry="820" fill="url(#s10gg)"/>', gg), wc=0,
           blend="screen",
           motion=M.combine(M.keys([(t_rem - 0.1, {"s": 0.18, "alpha": 0}), (t_rem + 0.5, {"alpha": 0.5}),
                                    (t_rem + 1.9, {"s": 1.0, "alpha": 0.4})], ["out", "sine"], pivot=gc),
                            lambda t: Tf(alpha=0.9 + 0.1 * math.sin(2 * math.pi * t / 2.6))))
    rays = S.path(S.rays(gc[0], 60, 60, 900, n=14, width_deg=6, rot=8), fill="#fff0c0", stroke=False)
    sc.add("god_rays", doc(S.g(rays, filter="blur-md"), ""), wc=0, blend="screen",
           motion=M.combine(M.keys([(t_rem, {"alpha": 0}), (t_rem + 1.2, {"alpha": 0.14})], "sine"),
                            lambda t: Tf(rot=1.5 * math.sin(2 * math.pi * t / 9), px=gc[0], py=60)))

    # each sleeping animal gets its own tiny sparkle, one after another
    spots = [(460, 812), (585, 845), (952, 468), (1145, 905), (1265, 905), (1430, 890), (1545, 895),
             (1725, 820), (1810, 860), (1975, 860), (650, 930), (410, 420), (600, 425), (700, 425), (450, 860)]
    order = [0, 14, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 1]
    span = max(1.2, t_each_end - t_each - 0.2)
    cues = []
    for k, j in enumerate(order):
        x, y = spots[j]
        cues.append((x, y, t_each + 0.05 + span * k / len(order), 15 + 4 * (k % 3)))
    sc.fx = [stars_fx(cues)]

    # ---------------------------------------------------------------- camera: the ark rolls gently on the water
    def roll(t):
        return (0.35 + 0.45 * heavy(t)) * math.sin(2 * math.pi * g(t) / 5.2)
    base = M.cam_keys([(0, Cam(1056, 600, 1960)), (t_family, Cam(1056, 600, 1960)), (t_wind, Cam(1060, 598, 1930)),
                       (T, Cam(1090, 594, 1880))], "sine")

    def cam(t):
        c = base(t)
        return Cam(c.x, c.y + 4 * math.sin(2 * math.pi * g(t) / 5.2 + 1.2), c.w, roll(t))
    sc.camera = cam

    # ---------------------------------------------------------------- sound
    sc.sfx("rain", 0, dur=T + 0.1, gain_db=-17, fade_in=0.8, fade_out=0.9)
    sc.sfx("ship_creak", 0, dur=T + 0.1, gain_db=-22, fade_in=0.8, fade_out=0.9)
    sc.sfx("snore", 0.3, dur=t_wind - 0.3, gain_db=-24, fade_in=0.6, fade_out=0.6, pan=-0.3)
    sc.sfx("crowd", t_family, dur=1.8, gain_db=-24, fade_in=0.2, fade_out=0.6, pan=0.5)
    sc.sfx("storm_wind", t_wind - 0.3, dur=3.4, gain_db=-17, fade_in=0.4, fade_out=1.2)
    sc.sfx("rain", t_wind - 0.3, dur=3.6, gain_db=-15, fade_in=0.4, fade_out=1.4)
    sc.sfx("chime", t_rem + 0.05, gain_db=-11)
    sc.sfx("sparkle", t_each + 0.1, gain_db=-15)
    sc.sfx("sparkle", t_each + span * 0.55, gain_db=-17, pan=0.3)
    sc.sfx("snore", t_each_end, dur=T - t_each_end, gain_db=-26, fade_in=0.5, fade_out=0.8, pan=-0.3)
    return sc
