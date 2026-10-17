"""Scene 5 — the lots (Jonah 1:6-12).

A tall dollhouse cut-away of the ship. The scene opens below deck in the warm, lantern-lit hold
(where scene 4 left Jonah asleep): the captain shakes Jonah awake and he scrambles up. The camera
then rises through the deck to the rainy deck above, where the sailors draw lots from a clay pot.
The last lot glows, jumps out of the pot and lands at Jonah's feet; every sailor turns and points
at him. Jonah, sorry and brave, confesses and points to the raging sea; the sailors exchange
worried looks. The storm goes on (a bit lighter): rain, big waves beyond the rail, one soft thunder.

Stage 2112 x 2440: deck world y 0..1190, cut section 1190..1262, hold 1262..2440.
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SH = 2440            # stage height
DECK_CUT = 1190      # near (cut) edge of the deck floor
HOLD_TOP = 1262      # top of the hold interior
RAIL_TOP = 800       # top of the far bulwark
DECK_BACK = 892      # where the deck floor meets the far bulwark
FLOOR = 2190         # hold floor line (back wall foot)

CAM_HOLD = Cam(1060, 1905, 1700)
CAM_DECK = Cam(1090, 640, 1840)
CAM_END = Cam(1110, 646, 1780)
MAST_X = 190

# deck characters (x, feet y, scale, facing at start)
CAPT = (360, 968, 1.0)
S0 = (570, 978, 0.95, 1)      # variant 1, front row
S1 = (757, 948, 0.95, 1)      # variant 0, back row, left of the pot
S2 = (1037, 948, 0.95, -1)    # variant 2, back row, right of the pot
S3 = (1240, 978, 0.95, -1)    # variant 3, front row
JON = (1515, 982, 1.0)
POT_X, POT_Y, POT_S = 897, 843, 1.3   # lots_jar anchor (bottom centre) on top of the crate
LOT_LAND = (1392, 974)
HOLD_LAMP = (1190, 1440)      # hook of the hanging lantern in the hold

# hold characters
HJ = (1090, 2160, 1.1)        # Jonah asleep on the straw pallet (hip anchor)
HC_X = HJ[0] - 237 * HJ[2]    # captain kneeling beside him (see characters.captain 'wake')


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=SH)


# ============================================================== small drawing helpers

def peaky_band(y0, amp, wl, phase=0.0, x0=-80, x1=W + 80, bottom=1060, sharp=1.7, step=None):
    """Storm-sea band whose top has pointed crests (crest where (x/wl+phase) % 1 == 0)."""
    step = step or wl / 10
    pts = []
    x = x0
    while x <= x1 + step:
        u = (x / wl + phase) % 1.0
        h = (0.5 + 0.5 * math.cos(2 * math.pi * u)) ** sharp
        pts.append((x, y0 - amp * h))
        x += step
    d = S.smooth_path(pts, closed=False)
    return d + f" L{S.fmt(pts[-1][0])},{bottom} L{S.fmt(pts[0][0])},{bottom} Z"


def crest_xs(wl, phase, x0=-80, x1=W + 80):
    k0 = math.floor(x0 / wl + phase) - 1
    out = []
    for k in range(k0, k0 + int((x1 - x0) / wl) + 4):
        x = (k - phase) * wl
        if x0 - wl < x < x1 + wl:
            out.append(x)
    return out


def foam_cap(x, y, w, seed=0, fill=None, opacity=1.0):
    """Little foam crown sitting on a wave crest (a few overlapping puffs + a curl)."""
    r = random.Random(seed)
    fill = fill or P["foam"]
    out = ""
    n = 4
    for i in range(n):
        u = (i + 0.5) / n
        cx = x - w / 2 + w * u + r.uniform(-5, 5)
        rad = w * (0.16 + 0.1 * math.sin(math.pi * u)) * r.uniform(0.85, 1.15)
        out += f'<circle cx="{S.fmt(cx)}" cy="{S.fmt(y + rad * 0.25)}" r="{S.fmt(rad)}" fill="{fill}"/>'
    out += (f'<path d="M{S.fmt(x - w * 0.55)},{S.fmt(y + w * 0.18)} q{S.fmt(w * 0.2)},{S.fmt(-w * 0.32)} '
            f'{S.fmt(w * 0.45)},{S.fmt(-w * 0.12)}" fill="none" stroke="{S.INK}" stroke-width="3" '
            f'stroke-linecap="round" opacity="0.55"/>')
    return f'<g opacity="{opacity}">{out}</g>'


def shield(cx, cy, r, col):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" {S.STROKE}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="#fff6e3" stroke-width="5" '
            f'opacity="0.75"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.25:.1f}" fill="{P["gold"]}" {S.STROKE_THIN}/>')


def plank_lines(x0, x1, ys, seed=0, color=None, joint_every=(160, 320), sw=2.5, opacity=0.55):
    """Horizontal plank seams with staggered butt joints."""
    r = random.Random(seed)
    color = color or S.INK
    out = ""
    for i, y in enumerate(ys):
        out += (f'<path d="M{x0},{y:.1f} L{x1},{y:.1f}" stroke="{color}" stroke-width="{sw}" '
                f'opacity="{opacity}" fill="none"/>')
        if i + 1 < len(ys):
            y2 = ys[i + 1]
            x = x0 + r.uniform(0, joint_every[1])
            while x < x1:
                out += (f'<path d="M{x:.1f},{y:.1f} L{x:.1f},{y2:.1f}" stroke="{color}" stroke-width="{sw}" '
                        f'opacity="{opacity * 0.8:.2f}"/>')
                out += (f'<circle cx="{x + 9:.1f}" cy="{(y + y2) / 2:.1f}" r="2.6" fill="{color}" '
                        f'opacity="{opacity * 0.8:.2f}"/>')
                x += r.uniform(*joint_every)
    return out


def straw_pallet(x0, x1, y):
    """Straw mattress on the hold floor; top surface at y."""
    body = (f'<path d="M{x0},{y + 6} Q{x0 - 8},{y - 10} {x0 + 20},{y - 14} L{x1 - 20},{y - 14} '
            f'Q{x1 + 8},{y - 10} {x1},{y + 6} L{x1 + 6},{y + 34} L{x0 - 6},{y + 34} Z" fill="#d9b66c" {S.STROKE}/>')
    r = random.Random(4)
    for i in range(26):
        xx = x0 + 20 + (x1 - x0 - 40) * i / 25 + r.uniform(-6, 6)
        body += (f'<path d="M{xx:.1f},{y - 6} l{r.uniform(-14, 14):.1f},{r.uniform(18, 30):.1f}" '
                 f'stroke="#a8823e" stroke-width="2.5" stroke-linecap="round" opacity="0.7"/>')
    body += (f'<path d="M{x0 + 4},{y + 12} L{x1 - 4},{y + 12}" stroke="#a8823e" stroke-width="3" '
             f'stroke-dasharray="14 10" opacity="0.7"/>')
    # folded teal blanket at the foot, cream pillow at the head
    body += (f'<path d="M{x1 - 120},{y - 10} q-6,-34 26,-38 l78,0 q24,4 18,38 z" fill="{P["jonah_sash"]}" '
             f'{S.STROKE}/><path d="M{x1 - 104},{y - 30} l84,0" stroke="#2c6a68" stroke-width="3" opacity="0.8"/>')
    return S.g(body, filter="wobble-fine")


def ladder(xt0, xt1, yt, xb0, xb1, yb, rungs=11):
    body = ""
    for (a, b) in ((xt0, xb0), (xt1, xb1)):
        body += (f'<path d="M{a - 11},{yt} L{a + 11},{yt} L{b + 12},{yb} L{b - 12},{yb} Z" '
                 f'fill="{P["wood_light"]}" {S.STROKE}/>')
    for i in range(1, rungs + 1):
        u = i / (rungs + 1)
        ya = yt + (yb - yt) * u
        xa = xt0 + (xb0 - xt0) * u
        xb = xt1 + (xb1 - xt1) * u
        body += (f'<rect x="{xa + 8:.1f}" y="{ya - 9:.1f}" width="{xb - xa - 16:.1f}" height="18" rx="6" '
                 f'fill="{P["wood"]}" {S.STROKE_THIN}/>')
    return S.g(body, filter="wobble-fine")


def bucket(x, y, s=1.0):
    w, h = 70 * s, 78 * s
    body = (f'<path d="M{x - w / 2},{y - h} L{x + w / 2},{y - h} L{x + w * 0.4},{y} L{x - w * 0.4},{y} Z" '
            f'fill="{P["wood_light"]}" {S.STROKE}/>'
            f'<ellipse cx="{x}" cy="{y - h}" rx="{w / 2}" ry="{10 * s}" fill="#5f7d8a" {S.STROKE}/>'
            f'<path d="M{x - w * 0.47},{y - h * 0.68} L{x + w * 0.47},{y - h * 0.68} M{x - w * 0.43},{y - h * 0.25} '
            f'L{x + w * 0.43},{y - h * 0.25}" stroke="#6d6a66" stroke-width="{6 * s}"/>'
            f'<path d="M{x - w / 2},{y - h} Q{x},{y - h - 60 * s} {x + w / 2},{y - h}" fill="none" '
            f'stroke="{S.INK}" stroke-width="{4 * s}"/>')
    return S.g(body, filter="wobble-fine")


# ============================================================== deck world

def rig_markup():
    """Mast, two shrouds and the yard with the furled sail (split between the sky and deck layers)."""
    mx = MAST_X
    mtop = (mx + 29, -700)
    b = ""
    for xr in (488, 702):
        b += f'<path d="M{mtop[0]},{mtop[1]} L{xr},{RAIL_TOP + 6}" stroke="{P["ink_soft"]}" stroke-width="5" fill="none"/>'
    b += f'<rect x="{mx}" y="-40" width="58" height="{972 + 40}" fill="url(#mast)" {S.STROKE}/>'
    for yy in (430, 690):
        b += f'<rect x="{mx - 6}" y="{yy}" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<rect x="{mx - 6}" y="452" width="70" height="16" rx="6" fill="#d8c08c" {S.STROKE_THIN}/>'
    b += f'<path d="M{mx - 28},972 Q{mx + 29},940 {mx + 86},972 Z" fill="{P["wood_dark"]}" {S.STROKE}/>'
    b += f'<path d="M{mx + 58},460 L{mx + 108},460" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linecap="round"/>'
    y0, y1 = 150, 196
    b += (f'<path d="M-40,{y0} L960,{y1}" stroke="{S.INK}" stroke-width="20" stroke-linecap="round"/>'
          f'<path d="M-40,{y0} L960,{y1}" stroke="{P["wood_light"]}" stroke-width="12" stroke-linecap="round"/>')
    n = 8
    for i in range(n):
        xa = -40 + i * 125
        ya = y0 + (y1 - y0) * (i / n) + 6
        col = P["sail"] if i % 2 == 0 else P["sail_stripe"]
        b += (f'<path d="M{xa},{ya} L{xa + 125},{ya + 6} Q{xa + 136},{ya + 36} {xa + 116},{ya + 46} '
              f'L{xa - 6},{ya + 40} Q{xa - 16},{ya + 22} {xa},{ya} Z" fill="{col}" {S.STROKE_THIN}/>')
    for xa in (150, 520, 860):
        ya = y0 + (y1 - y0) * ((xa + 40) / 1000)
        b += (f'<path d="M{xa},{ya - 4} Q{xa + 14},{ya + 26} {xa + 4},{ya + 56}" fill="none" stroke="#d8c08c" '
              f'stroke-width="8" stroke-linecap="round"/>')
    defs = S.lin_grad("mast", [(0, P["wood_dark"]), (0.4, P["wood_light"]), (1, P["wood"])], x1=0, y1=0, x2=1, y2=0)
    return b, defs


RIG_SPLIT = 430      # the deck layer carries the rig below this line (top edge of a rope band)


def rig_part(upper):
    body, defs = rig_markup()
    cid = "rigtop" if upper else "rigbot"
    y0, y1 = (-1000, RIG_SPLIT + 16) if upper else (RIG_SPLIT, 1300)
    clip = f'<clipPath id="{cid}"><rect x="-100" y="{y0}" width="{W + 200}" height="{y1 - y0}"/></clipPath>'
    return f'<g clip-path="url(#{cid})">{S.g(body, filter="wobble")}</g>', defs + clip


def sky_layer():
    defs = (S.lin_grad("dsky", [(0, "#36415a"), (0.42, "#4f5d77"), (0.77, "#7f8da2"), (1, "#9eaab8")]) +
            S.rad_grad("dbreak", [(0, "#f3e6c4", 0.6), (0.55, "#dcd0b6", 0.2), (1, "#d9cdb4", 0)]) +
            S.lin_grad("curtain", [(0, "#c9d3dc", 0.0), (0.3, "#c9d3dc", 0.22), (1, "#c9d3dc", 0.0)]))
    body = f'<rect x="-20" y="-20" width="{W + 40}" height="800" fill="url(#dsky)"/>'
    body += '<ellipse cx="1580" cy="330" rx="560" ry="190" fill="url(#dbreak)"/>'
    # soft, unlined storm masses high up
    soft = ""
    for (cx, cy, rx, ry, col) in [(250, 170, 520, 150, "#323c52"), (1000, 120, 640, 150, "#36415a"),
                                  (1850, 170, 520, 140, "#323c52"), (620, 300, 360, 80, "#465370")]:
        soft += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}"/>'
    body += S.g(soft, filter="blur-md")
    # distant rain curtains hanging under the clouds
    for (x0, x1) in [(180, 420), (930, 1150)]:
        body += S.g(f'<path d="M{x0},300 L{x1},300 L{x1 - 90},600 L{x0 - 90},600 Z" fill="url(#curtain)"/>',
                    filter="soft")
    bank = ""
    for i, (cx, cy, w, h, col) in enumerate([(120, 250, 560, 150, "#59667f"), (760, 210, 600, 140, "#55627b"),
                                              (1320, 245, 520, 130, "#5c6982"), (2010, 225, 560, 150, "#55627b")]):
        bank += S.cloud(cx, cy, w, h, col, seed=10 + i, sw=2.5)
    body += S.g(bank, filter="wobble")
    # far sea (static; the near swell and the big wave move in front of it)
    wl, ph = 190, 0.3
    sea = S.path(peaky_band(592, 16, wl, ph, bottom=780), fill="#5a7b8c", sw=3)
    for i, x in enumerate(crest_xs(wl, ph)):
        sea += foam_cap(x, 576, 34, seed=i, opacity=0.65)
    sea += S.path(peaky_band(606, 10, 150, 0.6, bottom=780), fill="#507285", stroke=False)
    body += S.g(sea, filter="wobble")
    rig, rdefs = rig_part(True)
    body += rig
    return doc(body, defs + rdefs)


def clouds_layer():
    c = ""
    for i, (cx, cy, w, h) in enumerate([(960, 370, 440, 105), (1520, 345, 400, 95), (2080, 365, 440, 105)]):
        c += S.cloud(cx, cy, w, h, "#6c7a91", seed=30 + i, sw=2.5)
    return doc(S.g(c, filter="wobble"))


def sea_mid_layer():
    wl, ph = 520, 0.15
    defs = S.lin_grad("smid", [(0, "#5b8a9b"), (0.45, "#3e687c"), (1, "#2c4d60")])
    body = S.path(peaky_band(690, 64, wl, ph, bottom=860, sharp=2.2), fill="url(#smid)", sw=4)
    for i, x in enumerate(crest_xs(wl, ph)):
        body += foam_cap(x, 630, 86, seed=20 + i)
        body += (f'<path d="M{x - 60:.1f},{660} q30,26 70,30 M{x + 30:.1f},{668} q26,18 64,16" fill="none" '
                 f'stroke="{P["foam"]}" stroke-width="5" stroke-linecap="round" opacity="0.6"/>')
    return doc(S.g(body, filter="wobble"), defs)


def big_wave_layer():
    """A huge breaking wave beyond the starboard rail (right), curling toward the ship."""
    defs = S.lin_grad("bigw", [(0, "#74a2b0"), (0.35, "#4a788b"), (1, "#2c4d60")])
    pts = [(1240, 860), (1380, 770), (1520, 630), (1640, 530), (1740, 470), (1840, 440), (1950, 448),
           (2060, 488), (2180, 548), (2280, 610)]
    d = S.smooth_path(pts, closed=False) + " L2280,860 L1240,860 Z"
    body = S.path(d, fill="url(#bigw)", sw=5)
    # inner darker trough line and light face streaks
    body += ('<path d="M1500,700 Q1620,640 1700,600" fill="none" stroke="#335a6c" stroke-width="10" '
             'stroke-linecap="round" opacity="0.6"/>')
    for (x, y) in [(1560, 660), (1660, 610), (1900, 560), (2020, 600), (1780, 650), (1460, 760)]:
        body += (f'<path d="M{x},{y} q34,26 92,30" fill="none" stroke="{P["foam"]}" stroke-width="6" '
                 f'stroke-linecap="round" opacity="0.5"/>')
    # foam crest riding along the top, ending in a curl at the left
    crest = S.smooth_path([(1690, 494), (1760, 462), (1850, 440), (1950, 446), (2060, 484), (2180, 544),
                           (2290, 606)], closed=False)
    curl = "M1700,494 C1660,498 1640,540 1664,562 C1688,582 1716,560 1704,542"
    body += f'<path d="{crest}" fill="none" stroke="{S.INK}" stroke-width="46" stroke-linecap="round"/>'
    body += f'<path d="{curl}" fill="none" stroke="{S.INK}" stroke-width="34" stroke-linecap="round"/>'
    body += f'<path d="{crest}" fill="none" stroke="{P["foam"]}" stroke-width="38" stroke-linecap="round"/>'
    body += f'<path d="{curl}" fill="none" stroke="{P["foam"]}" stroke-width="26" stroke-linecap="round"/>'
    body += foam_cap(1850, 430, 100, seed=52) + foam_cap(2040, 466, 110, seed=53)
    return doc(S.g(body, filter="wobble"), defs)


def splash_layer(cx, cy, seed, k=1.0):
    """Cartoon splash crown thrown up over the rail: tapered jets with droplet tips, a foam mound and
    loose drops. (cx, cy) = base of the burst (it sits on the rail top)."""
    r = random.Random(seed)
    foam, ink = P["foam"], S.INK
    body = ""
    n = 6
    for i in range(n):
        ang = math.radians(-160 + 140 * (i + 0.5) / n + r.uniform(-8, 8))
        ln = r.uniform(95, 165) * k
        w = r.uniform(20, 28) * k
        ca, sa = math.cos(ang), math.sin(ang)
        px_, py_ = -sa, ca
        tx, ty = cx + ln * ca, cy + ln * sa
        mx, my = cx + 0.55 * ln * ca, cy + 0.55 * ln * sa
        d = (f"M{cx + px_ * w:.1f},{cy + py_ * w:.1f} Q{mx + px_ * w * 0.45:.1f},{my + py_ * w * 0.45:.1f} "
             f"{tx:.1f},{ty:.1f} Q{mx - px_ * w * 0.45:.1f},{my - py_ * w * 0.45:.1f} "
             f"{cx - px_ * w:.1f},{cy - py_ * w:.1f} Z")
        body += f'<path d="{d}" fill="{foam}" stroke="{ink}" stroke-width="{3 * k:.1f}" stroke-linejoin="round"/>'
        dr = w * 0.42
        body += (f'<circle cx="{tx + ca * dr * 2.2:.1f}" cy="{ty + sa * dr * 2.2:.1f}" r="{dr:.1f}" fill="{foam}" '
                 f'stroke="{ink}" stroke-width="{2.5 * k:.1f}"/>')
    for i in range(9):
        ang = math.radians(r.uniform(-165, -15))
        dist = r.uniform(120, 210) * k
        rr = r.uniform(5, 10) * k
        body += (f'<circle cx="{cx + dist * math.cos(ang):.1f}" cy="{cy + dist * math.sin(ang):.1f}" r="{rr:.1f}" '
                 f'fill="{foam}" stroke="{ink}" stroke-width="{2 * k:.1f}"/>')
    ms = ""
    pts = [(cx + (i - 2) * 30 * k + r.uniform(-6, 6), cy - r.uniform(4, 18) * k, r.uniform(26, 36) * k) for i in range(5)]
    for x, y, rr in pts:
        ms += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr + 3 * k:.1f}" fill="{ink}"/>'
    for x, y, rr in pts:
        ms += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{foam}"/>'
    body += ms
    body += (f'<path d="M{cx - 50 * k:.1f},{cy - 26 * k:.1f} q20,-16 40,-6" fill="none" stroke="#b9d3da" '
             f'stroke-width="{5 * k:.1f}" stroke-linecap="round"/>')
    return doc(S.g(body, filter="wobble-fine"))


def deck_layer():
    """Mast, rigging, far bulwark with shields, deck planks, hatch and the cut-away section."""
    defs = (S.lin_grad("deckf", [(0, "#b98450"), (0.5, P["wood_light"]), (1, "#a96f42")]) +
            S.lin_grad("bulw", [(0, P["wood"]), (1, "#7e4e2e")]) +
            S.rad_grad("hatchglow", [(0, "#ffd68a", 0.95), (0.5, "#f2a95a", 0.55), (1, "#c9714a", 0)]))
    b = ""
    # --- far bulwark
    b += f'<rect x="-30" y="{RAIL_TOP + 14}" width="{W + 60}" height="{DECK_BACK - RAIL_TOP - 4}" fill="url(#bulw)" {S.STROKE}/>'
    b += plank_lines(-30, W + 30, [842, 868], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += f'<rect x="{x - 12}" y="{RAIL_TOP + 4}" width="24" height="{DECK_BACK - RAIL_TOP}" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    for xr in (488, 702):
        b += f'<circle cx="{xr}" cy="{RAIL_TOP + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += shield(x, 852, 33, cols[i % 4])
    b += (f'<path d="M-30,{RAIL_TOP} L{W + 30},{RAIL_TOP} L{W + 30},{RAIL_TOP + 18} L-30,{RAIL_TOP + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    # --- deck floor
    b += f'<rect x="-30" y="{DECK_BACK}" width="{W + 60}" height="{DECK_CUT - DECK_BACK + 4}" fill="url(#deckf)" {S.STROKE}/>'
    ys = [906, 924, 946, 972, 1003, 1039, 1080, 1126, 1176]
    b += plank_lines(-30, W + 30, ys, seed=7, opacity=0.45, joint_every=(260, 620))
    for (x, y, rx, ry) in [(660, 1062, 130, 16), (1250, 1112, 160, 18), (1880, 1150, 120, 14), (420, 1150, 90, 12)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9fb3bd" opacity="0.45"/>'
        b += f'<path d="M{x - rx * 0.5},{y - 3} l{rx * 0.5},0" stroke="#e8eef0" stroke-width="3" opacity="0.6"/>'
    # --- open hatch at the right (warm light from the hold below)
    hx0, hx1, hy0, hy1 = 1790, 2010, 978, 1040
    b += (f'<path d="M{hx0 + 10},{hy0 - 118} L{hx1 - 2},{hy0 - 132} L{hx1 + 4},{hy0 + 2} L{hx0 - 4},{hy0 + 2} Z" '
          f'fill="{P["wood"]}" {S.STROKE}/>')  # hatch lid propped up behind the opening
    b += plank_lines(hx0 + 4, hx1, [hy0 - 80, hy0 - 40], seed=11, opacity=0.45, joint_every=(400, 600))
    b += (f'<path d="M{hx0 + 30},{hy0 - 120} L{hx0 + 24},{hy0} M{hx1 - 30},{hy0 - 128} L{hx1 - 24},{hy0}" '
          f'stroke="#6d6a66" stroke-width="8"/>')
    b += (f'<path d="M{hx0},{hy0} L{hx1},{hy0} L{hx1 + 26},{hy1} L{hx0 - 26},{hy1} Z" fill="#3b2416" {S.STROKE}/>')
    b += f'<ellipse cx="{(hx0 + hx1) / 2}" cy="{hy1 - 10}" rx="150" ry="40" fill="url(#hatchglow)"/>'
    b += (f'<path d="M{hx0 - 8},{hy0 - 6} L{hx1 + 8},{hy0 - 6} L{hx1 + 38},{hy1 + 8} L{hx0 - 38},{hy1 + 8} Z" '
          f'fill="none" stroke="{P["wood_dark"]}" stroke-width="12" stroke-linejoin="round"/>')
    for xa, xb in ((hx0 + 50, hx0 + 58), (hx1 - 50, hx1 - 58)):
        b += (f'<path d="M{xa},{hy1} L{xb},{hy0 - 40}" stroke="{S.INK}" stroke-width="22" stroke-linecap="round"/>'
              f'<path d="M{xa},{hy1} L{xb},{hy0 - 40}" stroke="{P["wood_light"]}" stroke-width="14" stroke-linecap="round"/>')
    # --- the mast and the lower rigging (in front of the far rail)
    rig, rdefs = rig_part(False)
    b = S.g(b, filter="wobble") + rig
    cut = ""
    # --- the cut-away edge of the deck (dollhouse section), painted like the hull band
    cut += f'<rect x="-30" y="{DECK_CUT - 4}" width="{W + 60}" height="{HOLD_TOP - DECK_CUT + 8}" fill="{P["wood_dark"]}" {S.STROKE}/>'
    cut += f'<rect x="-30" y="{DECK_CUT + 8}" width="{W + 60}" height="26" fill="{P["jonah_sash"]}" {S.STROKE_THIN}/>'
    tri = ""
    for x in range(-20, W + 40, 64):
        tri += f'M{x},{DECK_CUT + 34} l26,0 l-13,18 z '
    cut += f'<path d="{tri}" fill="{P["terracotta"]}" {S.STROKE_THIN}/>'
    for x in range(60, W + 40, 330):
        cut += f'<rect x="{x}" y="{DECK_CUT + 40}" width="70" height="{HOLD_TOP - DECK_CUT - 34}" fill="#5e3820" {S.STROKE_THIN}/>'
    return doc(b + S.g(cut, filter="wobble"), defs + rdefs)


def deck_props_layer():
    """Crate under the lots pot (in front of the back-row sailors)."""
    cy = 958 - 48 * 1.25
    return doc(PR.crate(POT_X - 6, cy, 1.25))


def deck_foreground():
    return doc(PR.rope_coil(300, 1128, 1.5) + bucket(520, 1112, 1.1))


# ============================================================== hold

def fishing_net(x0, y0, x1, y1, seed=0):
    """A fishing net hung from two pegs, sagging, with cork floats along the top rope."""
    r = random.Random(seed)
    sag = 70
    top = f"M{x0},{y0} Q{(x0 + x1) / 2},{y0 + sag} {x1},{y0}"
    hem = [(x0 - 10, y0 + 30)]
    for i in range(1, 8):
        u = i / 8
        hem.append((x0 + (x1 - x0) * u, y1 + 26 * math.sin(math.pi * u) + r.uniform(-14, 14)))
    hem.append((x1 + 10, y0 + 30))
    d = top + " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in hem[::-1]) + " Z"
    body = f'<path d="{d}" fill="#b89a62" fill-opacity="0.35" {S.STROKE_THIN}/>'
    mesh = ""
    for i in range(-6, 14):
        xa = x0 + i * 34
        mesh += f'M{xa},{y0} l{(y1 - y0) * 0.55:.1f},{y1 - y0 + 40} M{xa + 120},{y0} l{-(y1 - y0) * 0.55:.1f},{y1 - y0 + 40} '
    cid = f"net{x0}{y0}"
    body += (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
             f'<path d="{mesh}" clip-path="url(#{cid})" stroke="#c9a76a" stroke-width="3" fill="none"/>'
             f'<path d="{mesh}" clip-path="url(#{cid})" stroke="{S.INK}" stroke-width="1.2" fill="none" opacity="0.5"/>')
    body += f'<path d="{top}" fill="none" stroke="#c9a76a" stroke-width="9" stroke-linecap="round"/>'
    for i in range(1, 6):
        u = i / 6
        x = x0 + (x1 - x0) * u
        y = y0 + sag * 2 * u * (1 - u) * 1.0
        body += f'<ellipse cx="{x:.1f}" cy="{y + 6:.1f}" rx="16" ry="11" fill="{P["gold"]}" {S.STROKE_THIN}/>'
    for x in (x0, x1):
        body += f'<circle cx="{x}" cy="{y0}" r="10" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    return S.g(body, filter="wobble-fine")


def shelf(x0, x1, y):
    body = (f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="18" fill="{P["wood_light"]}" {S.STROKE_THIN}/>'
            f'<path d="M{x0 + 20},{y + 18} l26,40 M{x1 - 20},{y + 18} l-26,40" stroke="{P["wood_dark"]}" '
            f'stroke-width="9" stroke-linecap="round"/>')
    # little pots and a bowl
    for (cx, w, h, col) in [(x0 + 45, 40, 56, P["terracotta"]), (x0 + 100, 34, 42, "#d8b56a"),
                            (x0 + 160, 52, 30, "#9a6a45")]:
        body += (f'<path d="M{cx - w / 2},{y} Q{cx - w / 2 - 6},{y - h * 0.6} {cx - w * 0.25},{y - h} '
                 f'L{cx + w * 0.25},{y - h} Q{cx + w / 2 + 6},{y - h * 0.6} {cx + w / 2},{y} Z" fill="{col}" {S.STROKE_THIN}/>')
    return S.g(body, filter="wobble-fine")


def hold_layer():
    defs = (S.lin_grad("hwall", [(0, "#5b3520"), (0.3, "#87532f"), (0.7, "#9a6238"), (1, "#6e4127")]) +
            S.lin_grad("hfloor", [(0, "#a8713f"), (1, "#7a4a2a")]) +
            S.rad_grad("hvig", [(0, "#2a160c", 0), (0.55, "#2a160c", 0.06), (1, "#2a160c", 0.72)]) +
            S.lin_grad("shaft", [(0, "#cfe0ea", 0.5), (1, "#cfe0ea", 0.0)]))
    b = f'<rect x="-30" y="{HOLD_TOP - 10}" width="{W + 60}" height="{FLOOR - HOLD_TOP + 20}" fill="url(#hwall)"/>'
    ys = [HOLD_TOP + 60 + 70 * i for i in range(14)]
    for i in range(0, len(ys) - 1, 2):
        b += f'<rect x="-30" y="{ys[i]}" width="{W + 60}" height="{ys[i + 1] - ys[i]}" fill="#3b2416" opacity="0.07"/>'
    b += plank_lines(-30, W + 30, ys, seed=21, opacity=0.38, joint_every=(520, 1100))
    # ribs
    for x in (170, 640, 1420, 2040):
        b += (f'<path d="M{x - 30},{HOLD_TOP} L{x + 30},{HOLD_TOP} L{x + 26},{FLOOR} L{x - 26},{FLOOR} Z" '
              f'fill="{P["wood_dark"]}" {S.STROKE}/>'
              f'<path d="M{x - 12},{HOLD_TOP + 20} L{x - 10},{FLOOR - 20}" stroke="{P["wood"]}" stroke-width="7" '
              f'opacity="0.8"/>')
    # ceiling (underside of the deck) and beam ends
    b += f'<rect x="-30" y="{HOLD_TOP - 6}" width="{W + 60}" height="46" fill="#4e2e1b" {S.STROKE}/>'
    for x in range(60, W + 40, 330):
        if 1700 < x < 2000:
            continue
        b += (f'<rect x="{x}" y="{HOLD_TOP}" width="72" height="84" rx="6" fill="{P["wood"]}" {S.STROKE}/>'
              f'<circle cx="{x + 36}" cy="{HOLD_TOP + 60}" r="7" fill="{P["wood_dark"]}"/>')
    # hatch opening in the ceiling with grey storm light falling in
    b += f'<rect x="1760" y="{HOLD_TOP - 8}" width="200" height="52" fill="#a9b8c4" {S.STROKE}/>'
    for i in range(7):
        x = 1775 + i * 27
        b += f'<path d="M{x},{HOLD_TOP - 4} l-6,40" stroke="#e6edf0" stroke-width="2.5" opacity="0.8"/>'
    b += S.g(f'<path d="M1760,{HOLD_TOP + 40} L1960,{HOLD_TOP + 40} L2090,{FLOOR + 30} L1610,{FLOOR + 30} Z" '
             f'fill="url(#shaft)"/>', filter="soft")
    # floor
    b += f'<rect x="-30" y="{FLOOR}" width="{W + 60}" height="{SH - FLOOR + 30}" fill="url(#hfloor)" {S.STROKE}/>'
    b += plank_lines(-30, W + 30, [FLOOR + 22, FLOOR + 52, FLOOR + 90, FLOOR + 136, FLOOR + 192], seed=23,
                     opacity=0.4, joint_every=(300, 700))
    b += f'<ellipse cx="1830" cy="{FLOOR + 70}" rx="190" ry="20" fill="#9fb3bd" opacity="0.35"/>'
    b = S.g(b, filter="wobble")
    b += fishing_net(260, 1500, 580, 1760, seed=3)
    b += shelf(1470, 1690, 1700)
    # cargo
    cargo = ""
    cargo += PR.crate(120, FLOOR - 48 * 1.6 + 6, 1.6) + PR.crate(150, FLOOR - 48 * 1.6 - 170, 1.45)
    cargo += PR.jar(300, FLOOR - 81 * 1.65 + 8, 1.65, rot=-4) + PR.jar(445, FLOOR - 81 * 1.5 + 10, 1.5, rot=5)
    cargo += PR.sack(590, FLOOR + 14, 1.35, seed=2)
    cargo += PR.crate(1530, FLOOR - 48 * 1.4 + 8, 1.4) + PR.sack(1440, FLOOR + 16, 1.2, seed=5)
    cargo += PR.rope_coil(2010, FLOOR + 40, 1.5)
    b += cargo
    b += ladder(1800, 1925, HOLD_TOP - 10, 1745, 1890, FLOOR + 30)
    b += straw_pallet(800, 1350, 2166)
    b += f'<rect x="-30" y="{HOLD_TOP - 10}" width="{W + 60}" height="{SH - HOLD_TOP + 40}" fill="url(#hvig)"/>'
    return doc(b, defs)


# ============================================================== animation helpers

def flip(sc, name, keyframes, z, motion=None, frame_at=None):
    """Flipbook layer from [(t, markup), ...] with hard pose switches at the given times."""
    times = [k[0] for k in keyframes]
    svgs = [doc(k[1]) for k in keyframes]

    def default_at(t):
        i = 0
        for j, tj in enumerate(times):
            if t >= tj:
                i = j
        return float(i)

    if len(svgs) == 1:
        sc.add(name, svgs[0], motion=motion, z=z)
    else:
        sc.add(name, svgs, motion=motion, z=z, frame_at=frame_at or default_at)
    return times


def alive(x, y, switches=(), phase=0.0, amp=0.011, period=3.1, extra=None):
    """Breathing (vertical stretch about the feet) + a squash 'pop' at every pose switch."""
    def m(t):
        sy = 1 + amp * math.sin(2 * math.pi * (t / period + phase))
        sx = 1.0
        for ts in switches:
            u = (t - ts) / 0.24
            if 0 <= u <= 1:
                bmp = math.sin(math.pi * u) * (1 - u)
                sy *= 1 - 0.09 * bmp
                sx *= 1 + 0.05 * bmp
        if extra:
            e = extra(t)
            return Tf(e.dx, e.dy, e.rot, sx, sy, e.alpha, x, y)
        return Tf(sx=sx, sy=sy, px=x, py=y)
    return m


def held_lot(fn, x, y, s, facing, **kw):
    """A plain lot stick in the hands of a figure: held up ('lift') or held out in both hands ('carry')."""
    far, near = C.hand_positions(fn, x, y, s, facing, **kw)
    if kw.get("pose") == "carry":
        hx, hy = (far[0] + near[0]) / 2, (far[1] + near[1]) / 2
        return PR.lot(hx, hy - 6 * s, 0.95 * s, rot=-12 * facing)
    hx, hy = far
    return PR.lot(hx + 3 * facing, hy - 16 * s, 0.95 * s, rot=-78 * facing)


# ============================================================== build

def build(ctx):
    T = ctx.duration
    L = ctx.lines
    sc = Scene(ctx, W=W, H=SH)

    def at(i, f):
        return L[i].start + f * (L[i].end - L[i].start)

    # ---------------------------------------------------------------- key times
    t_crouch = max(0.35, L[0].start - 0.12)       # captain crouches to wake Jonah
    t_shake0, t_shake1 = L[0].start, at(0, 0.25)
    t_situp = at(0, 0.25)                          # Jonah sits up, rubbing his eye
    t_cpoint = at(0, 0.33)                         # captain points to the ladder
    t_standup = at(0, 0.38)                        # Jonah jumps to his feet
    t_walk = t_standup + 0.24                      # ...and hurries to the ladder
    t_pan0 = at(0, 0.4)
    t_pan1 = t_pan0 + 1.0
    t_s1_reach, t_s1_lift = at(0, 0.62), at(0, 0.74)
    t_s2_reach, t_s2_lift = at(0, 0.80), at(0, 0.93)
    t_glow = L[1].start - 0.06                    # last lot glows in the pot
    t_rise = t_glow + 0.1
    t_fly = t_rise + 0.2
    t_land = L[1].start + 0.66                    # lands at Jonah's feet ("...落在了")
    t_point = [t_land + 0.12, t_land + 0.2, t_land + 0.28, t_land + 0.36]   # S3, S2, S1, S0
    t_cap_point = t_land + 0.42
    t_confess = L[2].start - 0.05
    t_listen = [L[2].start + 0.35 + 0.08 * k for k in range(4)]
    t_thunder = at(2, 0.3)
    t_sea = at(2, 0.5)                             # "把我抛进海里吧"
    t_scared = [t_sea + 0.35 + 0.09 * k for k in range(4)]
    t_cap_worry = t_sea + 0.45
    t_look = [at(2, 0.86), at(2, 0.9), at(2, 0.94), at(2, 0.98)]
    t_calm = L[3].start - 0.05                     # "海就会平静下来"
    t_back = [at(3, 0.4), at(3, 0.48)]
    t_cap_end = at(3, 0.55)

    # ---------------------------------------------------------------- deck world (back to front)
    sc.add("sky", sky_layer(), z=0, wc=0.7)
    sc.add("clouds", clouds_layer(), z=1, motion=M.drift(vx=16), wc=0.8)
    sc.add("big_wave", big_wave_layer(), z=3, motion=M.combine(
        M.bob(26, 3.4, 0.1), lambda t: Tf(dx=18 * math.sin(2 * math.pi * t / 6.8))))
    sc.add("sea_mid", sea_mid_layer(), z=4, motion=M.combine(M.bob(20, 3.4, 0.35), M.bob(46, 6.0, axis="x")))

    def splash_m(base, phase, period=3.4, dur=0.9):
        def m(t):
            u = ((t / period + phase) % 1.0) * period / dur
            if u >= 1 or t - u * dur > T - 2.0:     # no new bursts in the closing dissolve
                return Tf(alpha=0.0)
            s = 0.25 + 0.85 * M.ease("out")(min(1.0, u / 0.6))
            a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.5, 1.0, "sine"))
            return Tf(dy=50 * u * u, sx=s, sy=s, alpha=a, px=base[0], py=base[1])
        return m
    sc.add("splash_r", splash_layer(1930, RAIL_TOP + 14, 3), z=5, motion=splash_m((1930, RAIL_TOP + 14), 0.62),
           wc=0.3)
    sc.add("splash_m", splash_layer(1720, RAIL_TOP + 14, 7, k=0.75), z=5.1,
           motion=splash_m((1720, RAIL_TOP + 14), 0.512, period=4.1), wc=0.3)

    sc.add("deck", deck_layer(), z=10)
    sc.add("split", doc(""), z=10.5, motion=M.still())   # keeps deck and hold as separate (cheaper) items
    sc.add("hold", hold_layer(), z=11)

    # ---------------------------------------------------------------- hold animation
    hx_, hy_ = HOLD_LAMP
    lan_sway = M.sway(7, 2.6, pivot=(hx_, hy_))
    glow_defs = S.rad_grad("lg", [(0, "#ffcf86", 0.32), (0.45, "#ffbf6a", 0.12), (1, "#ffbf6a", 0)])
    sc.add("hold_glow", doc(f'<ellipse cx="{hx_}" cy="{hy_ + 100}" rx="640" ry="470" fill="url(#lg)"/>', glow_defs),
           z=12, motion=lan_sway, blend="add", wc=0)
    sc.add("hold_lantern", doc(f'<path d="M{hx_},{HOLD_TOP + 40} L{hx_},{hy_}" stroke="{S.INK}" stroke-width="4"/>' +
                               PR.lantern(hx_, hy_, 1.25)), z=13, motion=lan_sway)

    jx, jy, js = HJ
    shaking = lambda t: t_shake0 <= t <= t_shake1
    shake_c = lambda t: Tf(dx=(7 * math.sin(2 * math.pi * 4.6 * t) if shaking(t) else 0.0))
    shadow = C.ground_shadow(jx - 20, jy + 2, js, width=360, opacity=0.25)
    flip(sc, "hold_captain", [
        (0, C.captain(HC_X + 10, jy, js, 1, pose="worried")),
        (t_crouch, C.captain(HC_X, jy, js, 1, pose="wake")),
        (t_cpoint, C.captain(HC_X - 10, jy, js, 1, pose="point", expr="worried")),
    ], z=14, motion=alive(HC_X, jy, [t_crouch, t_cpoint], 0.3, extra=shake_c))

    jsx = jx + 60   # where he stands up
    hold_j = [
        (0, shadow + C.jonah(jx, jy, js, 1, pose="sleep")),
        (t_shake0, shadow + C.jonah(jx, jy, js, 1, pose="sleep", marks=False)),
        (t_situp, shadow + C.jonah(jx - 10, jy, js, 1, pose="wake")),
        (t_standup, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="stand", expr="surprised")),
        (t_walk, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="walk_a", expr="worried")),
        (t_walk, C.ground_shadow(jsx, jy + 2, js) + C.jonah(jsx, jy, js, 1, pose="walk_b", expr="worried")),
    ]

    def hold_j_at(t):
        if t >= t_walk:
            return 4.0 + (int((t - t_walk) / 0.2) % 2)
        return float(max(i for i, (tk, _) in enumerate(hold_j[:4]) if t >= tk))

    def hold_j_extra(t):
        if shaking(t):
            return Tf(dx=6 * math.sin(2 * math.pi * 4.6 * t - 0.5), rot=1.2 * math.sin(2 * math.pi * 4.6 * t - 0.5))
        if t >= t_walk:
            return Tf(dx=330 * (t - t_walk), dy=-6 * abs(math.sin(math.pi * (t - t_walk) / 0.2)))
        return Tf()
    flip(sc, "hold_jonah", hold_j, z=15, frame_at=hold_j_at,
         motion=alive(jx, jy, [t_situp, t_standup], 0.0, amp=0.008, extra=hold_j_extra))
    sc.add("hold_fg", doc(PR.sack(330, SH - 40, 1.9, seed=9) + PR.jar(1880, SH - 110, 1.75, rot=8)), z=16)

    # ---------------------------------------------------------------- deck characters
    lx_, ly_ = MAST_X + 100, 455
    sc.add("deck_lantern", doc(PR.lantern(lx_, ly_, 0.85)), z=20, motion=M.sway(9, 2.9, pivot=(lx_, ly_)))

    def sailor_frames(pos, variant, keys):
        x, y, s, _f0 = pos
        out = []
        for t, pose, facing, expr, lot_up in keys:
            mk = C.ground_shadow(x, y + 2, s) + C.sailor(x, y, s, facing, variant=variant, pose=pose, expr=expr)
            if lot_up:
                mk += held_lot(C.sailor, x, y, s, facing, variant=variant, pose=pose)
            out.append((t, mk))
        return out

    # back row: S1 and S2 flank the pot and take their turns drawing
    k1 = [(0, "stand", 1, "worried", False), (t_s1_reach, "point", 1, "worried", False),
          (t_s1_lift, "lift", 1, "worried", True), (t_point[2], "point", 1, "surprised", False),
          (t_listen[1], "stand", 1, "worried", False), (t_scared[1], "scared", 1, None, False),
          (t_look[1], "stand", -1, "worried", False), (t_back[0], "stand", 1, "worried", False)]
    flip(sc, "s1", sailor_frames(S1, 0, k1), z=21, motion=alive(S1[0], S1[1], [k[0] for k in k1[1:]], 0.2))
    k2 = [(0, "stand", -1, "worried", False), (t_s2_reach, "point", -1, "worried", False),
          (t_s2_lift, "lift", -1, "worried", True), (t_point[1], "point", 1, "surprised", False),
          (t_listen[2], "stand", 1, "worried", False), (t_scared[2], "scared", 1, None, False),
          (t_look[2], "stand", 1, "worried", False)]
    flip(sc, "s2", sailor_frames(S2, 2, k2), z=22, motion=alive(S2[0], S2[1], [k[0] for k in k2[1:]], 0.55))

    sc.add("crate", deck_props_layer(), z=23)
    t_j1 = t_s1_lift - 0.05
    t_j2 = t_s2_lift - 0.05
    flip(sc, "pot", [(0, PR.lots_jar(POT_X, POT_Y, POT_S, sticks=3)),
                     (t_j1, PR.lots_jar(POT_X, POT_Y, POT_S, sticks=2)),
                     (t_j2, PR.lots_jar(POT_X, POT_Y, POT_S, sticks=1)),
                     (t_glow + 0.08, PR.lots_jar(POT_X, POT_Y, POT_S, sticks=0))], z=24,
         motion=lambda t: Tf(rot=(2.5 * math.sin(2 * math.pi * 7 * t) * max(0, 1 - abs(t - t_glow) / 0.25)),
                             px=POT_X, py=POT_Y))

    k0 = [(0, "carry", 1, "worried", True), (t_point[3], "point", 1, "surprised", False),
          (t_listen[0], "stand", 1, "worried", False), (t_scared[0], "scared", 1, None, False),
          (t_look[0], "stand", 1, "worried", False)]
    flip(sc, "s0", sailor_frames(S0, 1, k0), z=25, motion=alive(S0[0], S0[1], [k[0] for k in k0[1:]], 0.8))
    k3 = [(0, "lift", -1, "worried", True), (t_point[0], "point", 1, "surprised", False),
          (t_listen[3], "stand", 1, "worried", False), (t_scared[3], "scared", 1, None, False),
          (t_look[3], "stand", -1, "worried", False), (t_back[1], "stand", 1, "worried", False)]
    flip(sc, "s3", sailor_frames(S3, 3, k3), z=26, motion=alive(S3[0], S3[1], [k[0] for k in k3[1:]], 0.4))

    cx, cy, cs = CAPT
    kc = [(0, "stand", "worried"), (t_cap_point, "point", "surprised"), (t_listen[0] + 0.15, "stand", "worried"),
          (t_cap_worry, "worried", None), (t_cap_end, "stand", "worried")]
    flip(sc, "captain", [(t, C.ground_shadow(cx, cy + 2, cs) + C.captain(cx, cy, cs, 1, pose=p, expr=e))
                         for t, p, e in kc], z=27, motion=alive(cx, cy, [k[0] for k in kc[1:]], 0.65))

    # Jonah on deck
    x, y, s = JON
    sh = C.ground_shadow(x, y + 2, s)
    kj = [(0, C.jonah(x, y, s, -1, pose="stand", expr="worried")),
          (t_land + 0.04, C.jonah(x, y, s, -1, pose="stand", expr="surprised")),
          (t_confess, C.jonah(x, y, s, -1, pose="confess", expr="sorry")),
          (t_sea, C.jonah(x, y, s, 1, pose="point", expr="neutral")),
          (t_calm + 0.5, C.jonah(x, y, s, -1, pose="confess", expr="peaceful"))]
    flip(sc, "jonah", [(t, sh + mk) for t, mk in kj], z=28, motion=alive(x, y, [k[0] for k in kj[1:]], 0.1))

    # warm golden light on Jonah when the lot falls on him (God's hand, never a figure)
    gdefs = (S.rad_grad("jg", [(0, "#ffe2a0", 0.5), (0.45, "#ffd27a", 0.24), (1, "#ffd27a", 0)]) +
             S.lin_grad("beam", [(0, "#fff0c0", 0.0), (0.2, "#ffeab0", 0.36), (0.85, "#ffdf96", 0.16),
                                 (1, "#ffe39a", 0.0)]))
    glow_env = M.keys([(t_land - 0.1, {"alpha": 0}), (t_land + 0.3, {"alpha": 1}), (t_confess + 0.6, {"alpha": 0.8}),
                       (t_sea, {"alpha": 0.0})], "sine")
    sc.add("beam", doc(S.g(f'<path d="M1560,60 L1860,60 L{x + 140},1000 L{x - 200},1000 Z" fill="url(#beam)"/>',
                           filter="blur-md"), gdefs),
           z=19, motion=glow_env, blend="add", wc=0)
    sc.add("jonah_glow", doc(f'<ellipse cx="{x}" cy="{y - 170}" rx="260" ry="330" fill="url(#jg)"/>', gdefs),
           z=27.5, motion=M.combine(glow_env, M.pulse(0.75, 1.0, 1.3)), blend="add", wc=0)

    # the flying marked lot (from the pot to Jonah's feet)
    lx0, ly0 = POT_X + 4, POT_Y - 78 * POT_S - 28
    lx1, ly1 = LOT_LAND

    def lot_pos(t):
        if t < t_rise:
            return lx0, ly0, -80.0
        if t < t_fly:
            u = M.progress(t, t_rise, t_fly, "out")
            return lx0, ly0 - 70 * u, -80.0 + 10 * u
        if t < t_land:
            u = (t - t_fly) / (t_land - t_fly)
            xx = M.lerp(lx0, lx1, u)
            yb = M.lerp(ly0 - 70, ly1, u)
            yy = yb - 340 * 4 * u * (1 - u)
            return xx, yy, -70 + 430 * M.ease("out")(u)
        b = (t - t_land) / 0.32
        hop = 22 * math.sin(math.pi * b) if b < 1 else 0.0
        return lx1, ly1 - hop, 360.0

    def lot_motion(delay=0.0, alpha=1.0):
        def m(t):
            tt_ = t - delay
            if t < t_glow:
                return Tf(alpha=0.0)
            if delay and not (t_fly < tt_ < t_land):
                return Tf(alpha=0.0)
            xx, yy, rr = lot_pos(tt_)
            a = alpha * min(1.0, (t - t_glow) / 0.12)
            pl = 1 + (0.1 * math.sin(2 * math.pi * t / 0.9) if t > t_land else 0)
            return Tf(dx=xx - lx0, dy=yy - ly0, rot=rr, sx=pl, sy=pl, alpha=a, px=lx0, py=ly0)
        return m
    lot_svg = doc(PR.lot(lx0, ly0, 1.5, marked=True))
    tdefs = S.rad_grad("tg", [(0, "#fff2c8", 0.9), (0.35, "#ffd77a", 0.6), (1, "#ffd36b", 0)])
    trail_svg = doc(f'<circle cx="{lx0}" cy="{ly0}" r="30" fill="url(#tg)"/>', tdefs)
    for k, (dl, al, sz) in enumerate([(0.04, 0.85, 1.0), (0.08, 0.65, 0.8), (0.12, 0.45, 0.62), (0.16, 0.3, 0.46)]):
        mk = lot_motion(dl, al)
        sc.add(f"lot_trail{k}", trail_svg, z=29 + 0.01 * k, blend="add", wc=0,
               motion=(lambda m_, z_: (lambda t: (lambda v: Tf(v.dx, v.dy, 0, z_, z_, v.alpha, v.px, v.py))(m_(t))))(mk, sz))
    sc.add("lot", lot_svg, z=29.2, motion=lot_motion(), wc=0.5)

    sc.add("deck_fg", deck_foreground(), z=30)

    # ---------------------------------------------------------------- camera
    hold_end = Cam(CAM_HOLD.x - 20, CAM_HOLD.y + 10, CAM_HOLD.w - 40)

    def cam_base(t):
        if t <= t_pan0:
            u = M.progress(t, 0, t_pan0, "sine")
            return Cam(M.lerp(CAM_HOLD.x, hold_end.x, u), M.lerp(CAM_HOLD.y, hold_end.y, u),
                       M.lerp(CAM_HOLD.w, hold_end.w, u))
        if t <= t_pan1:
            u = M.progress(t, t_pan0, t_pan1, "inout")
            return Cam(M.lerp(hold_end.x, CAM_DECK.x, u), M.lerp(hold_end.y, CAM_DECK.y, u),
                       M.lerp(hold_end.w, CAM_DECK.w, u))
        u = M.progress(t, t_pan1, T, "sine")
        return Cam(M.lerp(CAM_DECK.x, CAM_END.x, u), M.lerp(CAM_DECK.y, CAM_END.y, u),
                   M.lerp(CAM_DECK.w, CAM_END.w, u))

    def cam(t):
        c = cam_base(t)
        return Cam(c.x, c.y, c.w, 0.65 * math.sin(2 * math.pi * t / 4.3))
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    sc.fx = [
        rain_fx(),
        FX.lightning([t_thunder], dur=0.5, strength=0.22),
        FX.sparkles((lx1 - 120, y - 380, lx1 + 230, y - 10), count=26, t0=t_land - 0.05, t1=t_land + 2.6,
                    color=(255, 232, 160), size=(8, 18), period=1.3, drift=-20, seed=5),
        FX.motes((300, 1380, 1750, 2150), count=28, t1=t_pan1, color=(255, 228, 170), size=(3, 6), alpha=130),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_storm", 0, dur=T + 0.8, gain_db=-14, fade_in=0.8, fade_out=1.0)
    sc.sfx("storm_wind", 0, dur=T + 0.8, gain_db=-17, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("rain", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("ship_creak", 0, dur=t_pan1 + 0.5, gain_db=-15, fade_in=0.6, fade_out=0.8)
    sc.sfx("cloth", t_standup - 0.05, gain_db=-8)
    sc.sfx("footsteps_run", t_walk, dur=0.9, gain_db=-16, fade_out=0.4)
    sc.sfx("lots", t_s1_reach, gain_db=-7, pan=-0.25)
    sc.sfx("lots", t_s2_reach + 0.05, gain_db=-11, pan=-0.1)
    sc.sfx("whoosh", t_fly, gain_db=-15, pan=0.2)
    sc.sfx("sparkle", t_land - 0.1, gain_db=-7, pan=0.3)
    sc.sfx("thunder", t_thunder, gain_db=-13, pan=0.4)
    return sc


# ============================================================== rain (deck only)

def rain_fx(density=1.0, seed=8):
    """Slanted rain that only falls outdoors (above the deck's cut edge)."""
    import numpy as np
    from PIL import Image, ImageDraw
    from engine.paths import OUT_H, OUT_W

    n = int(360 * density)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = 1650 * rng.uniform(0.75, 1.25, n)
    ln = 44 * rng.uniform(0.6, 1.3, n)
    al = rng.uniform(70, 130, n).astype(int)
    a = math.radians(13)
    dx, dy = math.sin(a), math.cos(a)
    # splash ticks on the deck (stage coords)
    m = 40
    spx = rng.uniform(80, W - 80, m)
    spy = rng.uniform(DECK_BACK + 20, DECK_CUT - 20, m)
    sph = rng.uniform(0, 1, m)

    def fx(frame, t, view):
        _, ycut = view.to_out(1090, DECK_CUT)
        if ycut <= 0:
            return frame
        ylim = min(OUT_H, int(ycut))
        ov = Image.new("RGBA", (OUT_W, ylim), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0 + sp * t) % (OUT_H + 80) - 40
        x = (x0 - sp * t * dx / dy) % (OUT_W + 400) - 200
        for i in range(n):
            if y[i] > ylim:
                continue
            ye = min(y[i] + ln[i] * dy, ylim)
            xe = x[i] + (ye - y[i]) * dx / dy
            d.line([(x[i], y[i]), (xe, ye)], fill=(226, 234, 242, int(al[i])), width=2)
        for i in range(m):
            ph = (t * 2.2 + sph[i]) % 1.0
            if ph > 0.3:
                continue
            ox, oy = view.to_out(spx[i], spy[i])
            if oy > ylim - 2:
                continue
            r = (3 + 14 * ph / 0.3) * view.scale
            aa = int(150 * (1 - ph / 0.3))
            d.arc([ox - r, oy - r * 0.45, ox + r, oy + r * 0.45], 190, 350, fill=(232, 240, 245, aa), width=2)
        frame.alpha_composite(ov, (0, 0))
        return frame
    return fx
