"""placeholder"""
import math
import random

import numpy as np
from PIL import Image

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s15_city import WALK_A, WALK_N, keyed, sprite, walk_pose
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.daniel.scenes.s05_prays import Perf, clamp, fig, phrase_t

SW, SH = 2800, 1575
FY = 1300                      # floor line (feet)
K = 1.25                       # person scale in the tent
INK = P["ink"]


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=SW, h=SH)


def f1(v):
    return f"{v:.1f}"


# ================================================================== figures (custom rig poses)
def saul_fig(ps, expr=None, stool=False, front=None):
    D = C._saul_design("sit" if ps.get("lap") else "stand", False)
    if front is not None:
        D["front"] = front
    return lambda x, y, s, f: fig(D, C._SAUL_M, dict(ps), expr or ps["expr"], x, y, s, f, "saul-x")


def soldier_fig(v, ps, expr=None, spear=False, front=None):
    D, kind = C._soldier_design("israel", v)
    D["behind"] = C._shield_on_back(kind)
    if spear:
        D["front"] = C._spear_front(D)
    if front is not None:
        D["front"] = front
    return lambda x, y, s, f: fig(D, C._ADULT, dict(ps), expr or ps["expr"], x, y, s, f, f"sold{v}-x")


def david_fig(ps, expr=None, bag=True, front=None, mid="auto", behind=None, armor=False, hat=None, mail=False,
              metrics=None, curls=False):
    """David in a custom pose. hat: a custom head-top function (helmet stages); mail: Saul's mail coat (no sword);
    armor: mail coat + sword; curls: armour without the helmet (his own curls show)."""
    D = C._david_design(armor or mail, bag)
    if hat is not None:
        D["hat"] = ("custom", hat)
        D["hat_h"] = 1.2
    elif curls or (mail and not armor):
        D["hat"] = ("custom", C._david_head(False))
        D["hat_h"] = 0.30
    if mid == "auto":
        mid = (lambda st: C._sword_hang(st, drag=True)) if armor else (C._bag_mid if bag else None)
    D["behind"], D["mid"], D["front"] = behind, mid, front
    m = metrics or (C._metrics(C._BOY, 1.0, 1.22) if (armor or mail) else C._BOY)
    return lambda x, y, s, f: fig(D, m, dict(ps), expr or ps["expr"], x, y, s, f, "david-x")


def helmet_hat(k=0.0, tilt=7.0, curls=None):
    """David's head-top with Saul's too-big helmet. k = how far it is still lifted (0 = slid right down over the eyes
    like characters.david(armor=True); ~0.55 = pushed up so the eyes peek out; ~1 = sitting high on the curls)."""
    def hat(R):
        s = ""
        if curls if curls is not None else k > 0.3:
            s += C._curls_svg(R, C.DAVID_HAIR, cheeks=True)
        else:
            s += C._ell(-0.30 * R, 0.40 * R, 0.21 * R, 0.13 * R, P["cheek"], extra='opacity="0.38"')
            s += C._ell(0.68 * R, 0.42 * R, 0.16 * R, 0.12 * R, P["cheek"], extra='opacity="0.38"')
        s += (f'<g transform="translate({f1(-0.05 * R)},{f1((1.40 - 1.05 * k) * R)}) rotate({tilt:.1f})">'
              f'{C._bronze_helmet_svg(2.0 * R, C.BRONZE, plume=C.CREST_RED, circlet=True, guard=0.45)}</g>')
        return s
    return hat


# ================================================================== the tent (shared with s09)
WB = 1110                      # where the back wall meets the floor
CEIL = 300                     # bottom of the ceiling / top of the wall hangings
POLES = (700, 2330)
DOOR = (70, 560, 430)          # entrance opening in the back wall: x0, x1, top
LAMP = (1500, 600)             # hanging lamp (bowl centre)
LAMP_TOP = 250
TABLE = (2170, 2560, 1010)     # map table: x0, x1, top y (front edge)
RACK_X = 2700
BANNER = (2010, 430)           # royal banner on the wall (centre x, top)
CAM_MATCH = Cam(1328, 1003, 1550)   # s08's last second = s09's first second (the cross-dissolve)
STOOL_X = 1760                 # Saul's camp stool
DAVID_X = 1180                 # where David stands before the king
SAUL_END_X = 1400              # Saul after stepping up to bless David (s08 end, s09)
SOLA_X = 1990                  # soldier A (whispers; Saul's attendant)
SOLB_X = 800                   # soldier B (leads David in, then stands guard)
WALL = "#ecd8ae"
WALL_SH = S.shade("#ecd8ae", -0.16)
STRIPE = "#b8673f"
STRIPE2 = "#5f6f9a"
GOAT = "#6e5444"


def rect(x, y, w, h, fill, sw=4, rx=0, extra=""):
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" fill="{fill}" {st} {extra}/>'


def poly(pts, fill, sw=4, extra=""):
    d = "M" + " L".join(f"{f1(x)},{f1(y)}" for x, y in pts) + " Z"
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    return f'<path d="{d}" fill="{fill}" {st} {extra}/>'


def door_d():
    x0, x1, top = DOOR
    return (f"M{x0},{WB + 6} L{x0},{top + 120} C{x0 + 40},{top + 20} {x0 + 140},{top} {(x0 + x1) / 2},{top} "
            f"C{x1 - 140},{top} {x1 - 40},{top + 20} {x1},{top + 120} L{x1},{WB + 6} Z")


def outside_svg(wave=0.0):
    """Daylight seen through the entrance: sky, the far hill, two camp tents with banners, a soldier on guard."""
    x0, x1, top = DOOR
    defs = (S.lin_grad("s8sky", [(0, "#9fd0e4"), (0.6, "#d8ecdf"), (1, "#f6ecc9")]) +
            f'<clipPath id="s8door"><path d="{door_d()}"/></clipPath>')
    body = rect(x0 - 40, top - 40, x1 - x0 + 80, WB - top + 80, "url(#s8sky)", 0)
    body += S.g(S.cloud(330, 520, 230, 66, "#fdf6e8", seed=4, sw=3, shade_fill="#efe2d0"), filter="wobble")
    body += S.path(S.hill(-200, 900, 930, 160, seed=5, bumps=2, bottom=WB + 40), fill="#b9c99a", sw=3)
    body += S.path(S.hill(-100, 760, 1010, 70, seed=9, bumps=2, bottom=WB + 40), fill="#a6bd7a", sw=3)
    body += PR.tent(200, 1000, 0.42, 1, side="israel", wave=wave)
    body += PR.tent(470, 960, 0.3, -1, side="israel", wave=(wave + 0.5) % 1.0)
    body += f'<rect x="{x0 - 40}" y="{WB - 70}" width="{x1 - x0 + 80}" height="120" fill="#d8c08a"/>'
    return doc(f'<g clip-path="url(#s8door)">{body}</g>', defs)


def wall_svg():
    """Back wall hangings with the entrance cut out, the ceiling, valance, poles and the royal banner."""
    x0, x1, top = DOOR
    wall_d = f"M-40,{CEIL - 10} L{SW + 40},{CEIL - 10} L{SW + 40},{WB + 4} L-40,{WB + 4} Z " + door_d()
    defs = (f'<clipPath id="s8wall"><path d="{wall_d}" clip-rule="evenodd"/></clipPath>' +
            S.lin_grad("s8wsh", [(0, INK, 0.30), (0.25, INK, 0.0), (0.8, INK, 0.0), (1, INK, 0.16)]) +
            S.lin_grad("s8ceil", [(0, S.shade(GOAT, -0.25)), (1, S.shade(GOAT, 0.15))]) +
            S.rad_grad("s8lp", [(0, "#fff2c8", 0.55), (0.6, "#ffe6a8", 0.15), (1, "#ffe6a8", 0)]))
    inner = rect(-40, CEIL - 20, SW + 80, WB - CEIL + 40, WALL, 0)
    # woven panels: cream cloth with a seam band (terracotta + indigo pinstripes) every ~300 px, small diamonds
    x = -60
    i = 0
    while x < SW + 40:
        inner += rect(x, CEIL - 20, 30, WB - CEIL + 40, STRIPE, 0, extra='opacity="0.8"')
        inner += rect(x + 38, CEIL - 20, 7, WB - CEIL + 40, STRIPE2, 0, extra='opacity="0.6"')
        inner += rect(x - 15, CEIL - 20, 7, WB - CEIL + 40, STRIPE2, 0, extra='opacity="0.6"')
        if i % 2 == 0:
            inner += rect(x + 130, CEIL - 20, 60, WB - CEIL + 40, S.mix(WALL, STRIPE, 0.22), 0)
        for yy in range(CEIL + 150, WB - 160, 170):
            cx = x + 160 if i % 2 else x + 250
            inner += (f'<path d="M{cx},{yy - 12} l9,12 l-9,12 l-9,-12 Z" fill="{STRIPE}" opacity="0.55"/>')
        x += 300
        i += 1
    # soft fold lines and a band of woven zigzags low on the wall
    for fx_ in range(40, SW, 130):
        inner += (f'<path d="M{fx_},{CEIL} C{fx_ + 14},{CEIL + 300} {fx_ - 12},{WB - 300} {fx_ + 6},{WB}" fill="none" '
                  f'stroke="{WALL_SH}" stroke-width="5" opacity="0.45"/>')
    inner += rect(-40, WB - 120, SW + 80, 46, S.shade(STRIPE, -0.15), 0, extra='opacity="0.9"')
    zz = " ".join(f"L{xx},{WB - 97 + (12 if (xx // 30) % 2 else -12)}" for xx in range(-40, SW + 60, 30))
    inner += f'<path d="M-40,{WB - 97} {zz}" fill="none" stroke="{WALL}" stroke-width="5"/>'
    inner += f'<rect x="-40" y="{CEIL - 20}" width="{SW + 80}" height="{WB - CEIL + 40}" fill="url(#s8wsh)"/>'
    inner += f'<ellipse cx="{LAMP[0]}" cy="{LAMP[1] + 120}" rx="900" ry="520" fill="url(#s8lp)"/>'
    out = f'<g clip-path="url(#s8wall)">{inner}</g>'
    out += f'<path d="{wall_d}" fill="none" stroke="{INK}" stroke-width="5" fill-rule="evenodd"/>'
    # tied-back door flaps
    for side, xe in ((-1, x0), (1, x1)):
        xo = xe + side * 70
        d = (f"M{xe - side * 40},{top - 20} C{xe + side * 10},{top + 160} {xe - side * 10},{top + 330} {xe + side * 18},{top + 420} "
             f"C{xe - side * 6},{top + 520} {xe + side * 4},{WB - 120} {xe + side * 10},{WB + 8} L{xo + side * 36},{WB + 8} "
             f"C{xo + side * 30},{WB - 260} {xo + side * 20},{top + 440} {xo},{top + 420} C{xo + side * 30},{top + 300} "
             f"{xo + side * 40},{top + 120} {xo + side * 50},{top - 20} Z")
        out += f'<path d="{d}" fill="{S.shade(WALL, -0.06)}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        for k in (0.35, 0.7):
            xx = xe + side * 70 * k
            out += (f'<path d="M{xx},{top} C{xx + side * 10},{top + 200} {xx},{top + 380} {xx + side * 12},{top + 420}" '
                    f'fill="none" stroke="{STRIPE}" stroke-width="10" opacity="0.8"/>')
        out += f'<ellipse cx="{xe + side * 40}" cy="{top + 425}" rx="44" ry="16" fill="{P["wood_light"]}" stroke="{INK}" stroke-width="3.5"/>'
    # ceiling: the goat-hair roof seen from inside, sagging between the poles, with rope lashings
    cd = (f"M-40,-40 L{SW + 40},-40 L{SW + 40},{CEIL + 6} "
          + " ".join(f"Q{(a + b) / 2},{CEIL + 46} {a},{CEIL + 6}" for b, a in
                     zip([SW + 40, 2240, 1460, 700], [2240, 1460, 700, -40])) + " Z")
    out += f'<path d="{cd}" fill="url(#s8ceil)" stroke="{INK}" stroke-width="5"/>'
    for yy in range(30, CEIL, 46):
        out += (f'<path d="M-40,{yy} Q700,{yy + 26} 1460,{yy + 4} T{SW + 40},{yy + 8}" fill="none" '
                f'stroke="{S.shade(GOAT, 0.3)}" stroke-width="7" opacity="0.5"/>')
    # valance with tassels along the top of the wall
    val = f"M-40,{CEIL} L{SW + 40},{CEIL} L{SW + 40},{CEIL + 40} "
    for xx in range(SW + 40, -60, -80):
        val += f"Q{xx - 40},{CEIL + 86} {xx - 80},{CEIL + 40} "
    val += "Z"
    out += f'<path d="{val}" fill="{STRIPE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    out += f'<path d="M-40,{CEIL + 18} L{SW + 40},{CEIL + 18}" stroke="#e8c062" stroke-width="6"/>'
    for xx in range(-40, SW + 60, 80):
        out += (f'<path d="M{xx},{CEIL + 44} L{xx},{CEIL + 74}" stroke="{INK}" stroke-width="3"/>'
                f'<circle cx="{xx}" cy="{CEIL + 82}" r="9" fill="#e8c062" stroke="{INK}" stroke-width="3"/>')
    # poles
    for px in POLES:
        out += rect(px - 20, CEIL - 60, 40, WB - CEIL + 76, P["wood"], 4.5, 8)
        out += f'<path d="M{px - 6},{CEIL} L{px - 6},{WB}" stroke="{P["wood_light"]}" stroke-width="5" opacity="0.7"/>'
        for yy in (CEIL + 140, WB - 220):
            out += rect(px - 26, yy, 52, 26, P["wood_dark"], 3.5, 5)
            out += (f'<path d="M{px - 24},{yy + 8} L{px + 24},{yy + 4} M{px - 24},{yy + 18} L{px + 24},{yy + 14}" '
                    f'stroke="#c9a46a" stroke-width="3"/>')
    # the royal banner on the wall behind the king
    bx, by = BANNER
    bw, bh = 220, 380
    ban = rect(bx - bw / 2 - 30, by - 14, bw + 60, 22, P["wood"], 4, 6)
    ban += (f'<path d="M{bx - bw / 2},{by} L{bx + bw / 2},{by} L{bx + bw / 2},{by + bh} L{bx},{by + bh + 60} '
            f'L{bx - bw / 2},{by + bh} Z" fill="#3f6fa8" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    ban += rect(bx - bw / 2, by + 70, bw, 46, "#f2e6cc", 3.5)
    ban += f'<circle cx="{bx}" cy="{by + 210}" r="52" fill="#e8b63c" stroke="{INK}" stroke-width="4"/>'
    for j in range(12):
        a = j * math.pi / 6
        ban += (f'<path d="M{f1(bx + 62 * math.cos(a))},{f1(by + 210 + 62 * math.sin(a))} '
                f'L{f1(bx + 80 * math.cos(a))},{f1(by + 210 + 80 * math.sin(a))}" stroke="#e8b63c" stroke-width="7" '
                f'stroke-linecap="round"/>')
    ban += f'<circle cx="{bx}" cy="{by + 210}" r="24" fill="#f6dc8a"/>'
    for j in range(9):
        xx = bx - bw / 2 + 12 + j * (bw - 24) / 8
        yy = by + bh + 60 * (1 - abs(xx - bx) / (bw / 2))
        ban += f'<path d="M{f1(xx)},{f1(yy - 4)} l0,26" stroke="#e8c062" stroke-width="5" stroke-linecap="round"/>'
    out += ban
    return doc(S.g(out, filter="wobble"), defs)


def floor_svg():
    defs = (S.lin_grad("s8fl", [(0, "#b58d62"), (1, "#c9a274")]) +
            S.lin_grad("s8rug", [(0, "#a9473a"), (1, "#bd5643")]))
    out = f'<rect x="-40" y="{WB}" width="{SW + 80}" height="{SH - WB + 40}" fill="url(#s8fl)" stroke="{INK}" stroke-width="5"/>'
    rng = random.Random(8)
    for i in range(80):
        xx, yy = rng.uniform(0, SW), rng.uniform(WB + 20, SH)
        out += (f'<path d="M{xx:.0f},{yy:.0f} l{rng.uniform(30, 90):.0f},{rng.uniform(-3, 3):.0f}" '
                f'stroke="#d9b98c" stroke-width="3" opacity="0.6"/>')
    # the big rug (in perspective) under the king and David
    rb, rf = WB + 40, SH - 40
    pts = [(860, rb), (2330, rb), (2560, rf), (620, rf)]
    out += poly(pts, "url(#s8rug)", 5)
    inset = [(905, rb + 26), (2288, rb + 26), (2490, rf - 34), (690, rf - 34)]
    out += poly(inset, "none", 0, f'stroke="#e8b63c" stroke-width="10" stroke-linejoin="round"')
    inset2 = [(950, rb + 54), (2244, rb + 54), (2420, rf - 72), (760, rf - 72)]
    out += poly(inset2, "none", 0, f'stroke="#2f5d8a" stroke-width="6" stroke-linejoin="round"')
    for row, yy in enumerate((rb + 120, rb + 230, rb + 350)):
        u = (yy - rb) / (rf - rb)
        xl, xr = 950 - (950 - 760) * u, 2244 + (2420 - 2244) * u
        n = 9
        for j in range(n):
            cx = xl + 90 + (xr - xl - 180) * j / (n - 1)
            w, h = 34 + 14 * u, 16 + 10 * u
            out += (f'<path d="M{f1(cx - w)},{yy} L{f1(cx)},{f1(yy - h)} L{f1(cx + w)},{yy} L{f1(cx)},{f1(yy + h)} Z" '
                    f'fill="{"#e8b63c" if (j + row) % 2 else "#f2e6cc"}" opacity="0.85"/>')
    # fringe along the front edge
    for xx in range(630, 2560, 22):
        out += f'<path d="M{xx},{rf} l-3,22" stroke="#e8c062" stroke-width="4" stroke-linecap="round"/>'
    return doc(S.g(out, filter="wobble"), defs)


def table_svg(items="all"):
    """The low map table (Valley of Elah map). items: 'all' = Saul's spare armour lies beside the map (helmet,
    folded mail coat, sword), 'mail_sword', 'sword', 'none'."""
    x0, x1, ty = TABLE
    out = ""
    # legs
    for lx in (x0 + 30, x1 - 40):
        out += rect(lx - 12, ty + 10, 24, 150, P["wood_dark"], 4, 4)
    for lx in (x0 + 70, x1 - 10):
        out += rect(lx - 10, ty - 10, 20, 130, S.shade(P["wood_dark"], -0.15), 4, 4)
    out += poly([(x0 + 40, ty - 50), (x1 + 20, ty - 50), (x1, ty), (x0, ty)], P["wood_light"], 4.5)
    out += rect(x0, ty, x1 - x0, 26, P["wood"], 4.5, 4)
    # the map: parchment with two hills, the brook and little tents
    mx0, mx1 = x0 + 170, x0 + 330
    out += poly([(mx0 + 18, ty - 46), (mx1 + 22, ty - 46), (mx1 + 6, ty - 6), (mx0, ty - 6)], "#f3e2bb", 3.5)
    out += f'<path d="M{mx0 + 30},{ty - 14} Q{mx0 + 60},{ty - 44} {mx0 + 92},{ty - 16}" fill="#b9c99a" stroke="{INK}" stroke-width="2.5"/>'
    out += f'<path d="M{mx1 - 70},{ty - 14} Q{mx1 - 36},{ty - 44} {mx1 - 4},{ty - 16}" fill="#d8b98a" stroke="{INK}" stroke-width="2.5"/>'
    out += f'<path d="M{mx0 + 120},{ty - 42} C{mx0 + 100},{ty - 30} {mx0 + 140},{ty - 22} {mx0 + 118},{ty - 8}" fill="none" stroke="#5aa0c0" stroke-width="4"/>'
    for tx, col in ((mx0 + 50, "#7a5a40"), (mx0 + 72, "#7a5a40"), (mx1 - 46, "#c9714a"), (mx1 - 24, "#c9714a")):
        out += f'<path d="M{tx - 8},{ty - 22} L{tx},{ty - 34} L{tx + 8},{ty - 22} Z" fill="{col}"/>'
    for cx_, cy_ in ((mx0 + 22, ty - 40), (mx1 + 8, ty - 12)):
        out += f'<ellipse cx="{cx_}" cy="{cy_}" rx="9" ry="6" fill="#b9b2a6" stroke="{INK}" stroke-width="2.4"/>'
    # a cup
    out += (f'<path d="M{x1 - 70},{ty - 66} L{x1 - 40},{ty - 66} L{x1 - 46},{ty - 30} L{x1 - 64},{ty - 30} Z" '
            f'fill="#e8b63c" stroke="{INK}" stroke-width="3.5"/>')
    arm = armour_pile(ARM_PILE[0], ARM_PILE[1], items) if items != "none" else ""
    return doc(S.g(out, filter="wobble-fine") + arm)


ARM_PILE = (TABLE[0] + 80, TABLE[2] - 20)     # Saul's spare armour lies at the left end of the table


def armour_pile(cx, by, items="all", s=1.0):
    """Saul's armour as a little stack (bottom centre cx, by): folded mail coat, the sword on it, the helmet on top.
    items: 'all' | 'mail_sword' | 'sword'."""
    out = ""
    if items in ("all", "mail_sword"):
        out += mail_folded(cx, by - 22 * s, s)
    if items in ("all", "mail_sword", "sword"):
        out += PR.sword(cx + 4 * s, by - (50 if items != "sword" else 12) * s, 0.55 * s, rot=-3)
    if items == "all":
        out += PR.helmet_bronze(cx + 6 * s, by - 54 * s, 0.62 * s, -1, crest=False, plume=C.CREST_RED, circlet=True)
    return out


def mail_folded(cx, cy, s=1.0):
    """Saul's mail coat folded on the table (grey with rings)."""
    w, h = 120 * s, 44 * s
    out = (f'<path d="M{cx - w / 2},{cy + h / 2} L{cx - w / 2 + 10},{cy - h / 2} L{cx + w / 2 - 6},{cy - h / 2} '
           f'L{cx + w / 2},{cy + h / 2} Z" fill="{C.MAIL}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    for r_ in range(2):
        for j in range(6):
            out += (f'<circle cx="{f1(cx - w / 2 + 16 + j * (w - 30) / 5)}" cy="{f1(cy - h / 4 + r_ * h / 2)}" r="5" '
                    f'fill="none" stroke="{S.shade(C.MAIL, -0.3)}" stroke-width="2"/>')
    out += f'<path d="M{cx - w / 2 + 4},{cy} L{cx + w / 2 - 2},{cy}" stroke="{S.shade(C.MAIL, -0.25)}" stroke-width="2.5"/>'
    return S.g(out, filter="wobble-fine")


def rack_svg():
    """Saul's spear (upright in a wooden stand) and his round shield leaning against it, a water jar beside."""
    x = RACK_X
    out = ""
    out += rect(x - 70, WB + 4, 140, 26, P["wood_dark"], 4, 6)
    out += rect(x - 12, 760, 24, WB - 750, P["wood"], 4, 5)
    out += rect(x - 50, 800, 100, 18, P["wood"], 4, 5)
    sp = PR.spear(x + 2, WB - 228, 1.25, rot=-90, kind="soldier")
    out = S.g(out, filter="wobble-fine") + sp
    out += PR.round_shield(x - 40, WB - 64, 1.35, kind="israel", rot=-8)
    out += PR.jar(x + 120, WB - 40, 0.75)
    return doc(out)


def lamp_svg(lit=1.0):
    """Hanging bronze oil lamp on three chains (bowl centre LAMP), three little flames."""
    x, y = LAMP
    out = ""
    for dx in (-46, 0, 46):
        out += (f'<path d="M{x},{LAMP_TOP} L{x + dx},{y - 18}" stroke="{S.shade(C.BRONZE, -0.3)}" stroke-width="4" '
                f'stroke-dasharray="10 5"/>')
    out += f'<circle cx="{x}" cy="{LAMP_TOP}" r="10" fill="{C.BRONZE}" stroke="{INK}" stroke-width="3"/>'
    out += (f'<path d="M{x - 66},{y - 16} Q{x},{y - 30} {x + 66},{y - 16} Q{x + 50},{y + 34} {x},{y + 40} '
            f'Q{x - 50},{y + 34} {x - 66},{y - 16} Z" fill="{C.BRONZE}" stroke="{INK}" stroke-width="4"/>')
    out += f'<path d="M{x - 52},{y - 8} Q{x},{y - 18} {x + 52},{y - 8}" fill="none" stroke="{C.BRONZE_LIGHT}" stroke-width="4"/>'
    out += f'<path d="M{x - 6},{y + 40} L{x},{y + 62} L{x + 6},{y + 40}" fill="{C.BRONZE}" stroke="{INK}" stroke-width="3"/>'
    for dx in (-70, 0, 70):
        out += (f'<path d="M{x + dx * 0.95 - 10},{y - 16} Q{x + dx * 1.05},{y - 30} {x + dx * 1.05 + 10},{y - 16}" '
                f'fill="{C.BRONZE}" stroke="{INK}" stroke-width="3"/>')
    fl = ""
    for dx in (-70, 0, 70):
        fx_, fy_ = x + dx * 1.02, y - 26
        fl += (f'<path d="M{fx_},{fy_ - 34} C{fx_ + 12},{fy_ - 14} {fx_ + 10},{fy_} {fx_},{fy_} '
               f'C{fx_ - 10},{fy_} {fx_ - 12},{fy_ - 14} {fx_},{fy_ - 34} Z" fill="#ffc95a" stroke="{S.mix(P["sun_hot"], INK, 0.35)}" '
               f'stroke-width="2.5"/>')
        fl += f'<ellipse cx="{fx_}" cy="{fy_ - 8}" rx="4" ry="7" fill="#fff4cc"/>'
    return doc(S.g(out, filter="wobble-fine") + fl)


def lamp_glow_svg():
    x, y = LAMP
    defs = S.rad_grad("s8glow", [(0, "#ffe9b0", 0.75), (0.35, "#ffd98a", 0.32), (1, "#ffd98a", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y + 30}" rx="620" ry="540" fill="url(#s8glow)"/>', defs)


def doorlight_svg():
    """Daylight from the entrance spilling across the floor (screen)."""
    x0, x1, top = DOOR
    defs = S.lin_grad("s8dl", [(0, "#fff1c8", 0.55), (1, "#fff1c8", 0.0)], x1=0, y1=0, x2=1, y2=0.4)
    d = f"M{x0},{WB} L{x1},{WB} L{x1 + 900},{SH + 40} L{x0 + 120},{SH + 40} Z"
    return doc(f'<path d="{d}" fill="url(#s8dl)" filter="url(#blur-md)"/>', defs)


def fg_svg():
    """Foreground framing: a water jar and a rolled mat at the left, the tent's hanging edge and a guy rope at the
    right."""
    out = PR.jar(150, SH - 60, 1.35, rot=-4)
    out += S.g(rect(260, SH - 70, 260, 90, "#c9a46a", 4.5, 40) +
               f'<path d="M300,{SH - 66} L300,{SH + 10} M470,{SH - 66} L470,{SH + 10}" stroke="{STRIPE}" stroke-width="10"/>',
               filter="wobble-fine")
    d = (f"M{SW + 40},-40 L{SW - 210},-40 C{SW - 150},200 {SW - 200},420 {SW - 120},560 C{SW - 90},640 {SW - 60},700 "
         f"{SW - 40},780 L{SW + 40},800 Z")
    out += S.g(f'<path d="{d}" fill="{S.shade(GOAT, -0.1)}" stroke="{INK}" stroke-width="5"/>' +
               f'<path d="M{SW - 170},-40 C{SW - 120},200 {SW - 150},420 {SW - 90},560" fill="none" '
               f'stroke="{S.shade(GOAT, 0.3)}" stroke-width="8" opacity="0.6"/>', filter="wobble")
    return doc(out)



# ================================================================== timing helpers (shared with s09, s10)
_SEGS = {}


def voice_segs(ctx, i):
    """Voiced stretches [(start, end), ...] in scene seconds of narration line i (from its voice take), or None."""
    key = (ctx.id, i)
    if key in _SEGS:
        return _SEGS[key]
    out = None
    try:
        import soundfile as sf
        from engine.paths import BUILD
        line = ctx.lines[i]
        x, sr = sf.read(str(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav"), dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        if abs(len(x) / sr - (line.end - line.start)) < 0.3:
            hop = int(sr * 0.01)
            m = len(x) // hop
            e = np.sqrt((x[:m * hop].reshape(m, hop) ** 2).mean(axis=1)) + 1e-7
            db = np.convolve(20 * np.log10(e), np.ones(3) / 3, mode="same")
            db -= db.max()
            q = db < -30
            segs, j = [], 0
            while j < m:
                if not q[j]:
                    k = j
                    while k < m and not q[k]:
                        k += 1
                    if segs and j - segs[-1][1] < 8:
                        segs[-1][1] = k
                    else:
                        segs.append([j, k])
                    j = k
                else:
                    j += 1
            out = [(line.start + a * 0.01, line.start + b * 0.01) for a, b in segs if b - a >= 6]
    except Exception:
        out = None
    _SEGS[key] = out
    return out


def pt(ctx, i, phrase, snap=0.45):
    """When ``phrase`` of line i starts: its character-position estimate inside the subtitle chunk, snapped to the
    start of the nearest voiced stretch of the take (if one starts within ``snap`` s)."""
    line = ctx.lines[i]
    est = phrase_t(line, phrase, 0.0)
    segs = voice_segs(ctx, i)
    if segs:
        best = min(segs, key=lambda sg: abs(sg[0] - est))
        if abs(best[0] - est) <= snap:
            return best[0]
    return est


# ================================================================== image helpers
def paste(base, im, x, y):
    """alpha_composite im onto base with its top-left at (x, y) (may be partly outside)."""
    x, y = int(round(x)), int(round(y))
    w, h = im.size
    bw, bh = base.size
    x0, y0, x1, y1 = max(0, x), max(0, y), min(bw, x + w), min(bh, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    base.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


_ROT = {}


def rotated(im, deg, cx, cy):
    """im rotated by deg (clockwise, like SVG) about (cx, cy) in its own pixels (cached, 0.5 deg steps)."""
    deg = round(deg * 2) / 2
    if abs(deg) < 0.25:
        return im
    key = (id(im), deg, round(cx), round(cy))
    if key not in _ROT:
        if len(_ROT) > 300:
            _ROT.clear()
        _ROT[key] = im.rotate(-deg, resample=Image.BICUBIC, center=(cx, cy))
    return _ROT[key]


class Actor(Perf):
    """Perf (squash-and-hop pose schedule on a Sprite) plus an optional rotation about the anchor (rot(t), degrees)
    and an extra offset (off(t) -> (dx, dy)). toff shifts the breathing clock (so two scenes can match)."""

    def __init__(self, sp, sched, pos, walk=None, alpha=None, breathe=0.010, bper=3.0, phase=0.0, rot=None,
                 off=None, squash=None):
        super().__init__(sp, sched, pos, walk=walk, alpha=alpha, breathe=breathe, bper=bper, phase=phase)
        self.rot, self.off, self.squash = rot, off, squash

    def __call__(self, t):
        a = 1.0 if self.alpha is None else self.alpha(t)
        if a <= 0.002:
            return None
        x, y = self.pos(t)
        if self.off is not None:
            ox, oy = self.off(t)
            x, y = x + ox, y + oy
        hs, hd = self.hop(t)
        b = 1 + self.breathe * math.sin(2 * math.pi * (t / self.bper + self.phase))
        walking = self.walk is not None and self.walk(t) is not None
        sy = hs * (1.0 if walking else b)
        sx = 1 + 0.5 * (1 - hs)
        if self.squash is not None:
            qy = self.squash(t)
            sy *= qy
            sx *= 1 + 0.5 * (1 - qy)
        out = self.sp.place(self.frame(t), x, y, sx, sy, hd, a)
        if out is None:
            return None
        if self.rot is not None:
            r = self.rot(t)
            if abs(r) >= 0.25:
                im, (l, tp) = out
                out = rotated(im, r, x - l, y + hd - tp), (l, tp)
        return out


class WalkPath:
    """Planted-foot walking along a straight line: legs [(t0, x0, x1, rate drawings/s)], drawings [idx per walk
    drawing] for each leg (or one list for all), adv = stage px the anchor advances per drawing."""

    def __init__(self, legs, drawings, adv):
        self.legs, self.adv = legs, adv
        self.draw = drawings if isinstance(drawings[0], (list, tuple)) else [drawings] * len(legs)

    def n(self, i):
        t0, x0, x1, r = self.legs[i]
        return int(round(abs(x1 - x0) / self.adv))

    def end(self, i):
        return self.legs[i][0] + self.n(i) / self.legs[i][3]

    def frame(self, t):
        for i, (t0, x0, x1, r) in enumerate(self.legs):
            n = self.n(i)
            if t0 <= t < t0 + n / r:
                k = int((t - t0) * r + 1e-6)
                d = self.draw[i]
                return d[k % len(d)]
        return None

    def x(self, t):
        x = self.legs[0][1]
        for i, (t0, x0, x1, r) in enumerate(self.legs):
            if t < t0:
                return x
            n = self.n(i)
            k = min(n, int((t - t0) * r + 1e-6))
            x = x0 + (1 if x1 > x0 else -1) * k * self.adv
            if k >= n:
                x = x0 + (1 if x1 > x0 else -1) * n * self.adv
        return x


def walk_drawings(sp, mk, s, facing, A, lk=1.0, arm=None, label="w"):
    """2*WALK_N planted-foot walk drawings. mk(ps) -> fn(x, y, s, f); arm: fixed (far, near) arm spec + hands, e.g.
    (("fk", 26, 66), None) keeps the far arm still (None = swinging)."""
    idx = []
    for k in range(2 * WALK_N):
        ps = walk_pose(k, A=A, lk=lk)
        if arm is not None:
            arms = list(ps["arms"])
            hands = list(ps["hands"])
            for j in (0, 1):
                if arm[j] is not None:
                    arms[j] = arm[j][0]
                    hands[j] = arm[j][1]
            ps["arms"], ps["hands"] = tuple(arms), tuple(hands)
        idx.append(sp.add(mk(ps)(sp.ax, sp.ay, s, facing)))
    return idx


def walk_adv(A, s):
    return 2 * A / WALK_N * s


# ================================================================== little overlay drawings
def surprise_marks(x, y, s=1.0, facing=-1):
    """Three short 'double-take' lines fanning above a head and a little exclamation mark."""
    col = P["ink_soft"]
    out = ""
    for a in (-55, -90, -125):
        r = math.radians(a)
        x0, y0 = x + 70 * s * math.cos(r), y + 70 * s * math.sin(r)
        x1, y1 = x + 110 * s * math.cos(r), y + 110 * s * math.sin(r)
        out += f'<path d="M{f1(x0)},{f1(y0)} L{f1(x1)},{f1(y1)}" stroke="{col}" stroke-width="{6 * s}" stroke-linecap="round"/>'
    ex = x - facing * 120 * s
    out += (f'<path d="M{f1(ex - 10 * s)},{f1(y - 120 * s)} L{f1(ex + 10 * s)},{f1(y - 120 * s)} L{f1(ex + 4 * s)},{f1(y - 50 * s)} '
            f'L{f1(ex - 4 * s)},{f1(y - 50 * s)} Z" fill="#f2c14e" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>')
    out += f'<circle cx="{f1(ex)}" cy="{f1(y - 30 * s)}" r="{f1(9 * s)}" fill="#f2c14e" stroke="{INK}" stroke-width="{4 * s}"/>'
    return S.g(out, filter="wobble-fine")


def heart(cx, cy, w, fill="#ef8c95"):
    h = w * 0.9
    d = (f"M{f1(cx)},{f1(cy + h * 0.45)} C{f1(cx - w * 0.9)},{f1(cy - h * 0.1)} {f1(cx - w * 0.5)},{f1(cy - h * 0.75)} "
         f"{f1(cx)},{f1(cy - h * 0.3)} C{f1(cx + w * 0.5)},{f1(cy - h * 0.75)} {f1(cx + w * 0.9)},{f1(cy - h * 0.1)} "
         f"{f1(cx)},{f1(cy + h * 0.45)} Z")
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'


def rays_svg(ox, oy, tx, ty, spread, uid, n=6, wk=1.0, pool=(220, 60), w=SW, h=SH, length_k=1.0):
    """Soft golden rays from (ox, oy) toward (tx, ty) and a warm pool of light at the target (God's presence is only
    ever light)."""
    ang = math.degrees(math.atan2(ty - oy, tx - ox))
    dist = math.hypot(tx - ox, ty - oy) * length_k
    defs = (S.lin_grad(uid, [(0, "#fff1b8", 0.0), (0.3, "#ffe9a0", 0.55), (1, "#ffe39a", 0.10)], x1=0, y1=0, x2=1, y2=0)
            + S.rad_grad(uid + "p", [(0, "#fff3c6", 0.85), (0.5, "#ffe9a8", 0.35), (1, "#ffe9a8", 0)]))
    body = ""
    for i in range(n):
        a = ang + spread * (2 * i / (n - 1) - 1)
        ww = (26 + 12 * (i % 2)) * wk
        body += (f'<path d="M0,-8 L{f1(dist)},{-ww} L{f1(dist)},{ww} L0,8 Z" fill="url(#{uid})" '
                 f'transform="translate({ox},{oy}) rotate({a:.2f})"/>')
    body = f'<g filter="url(#soft)">{body}</g>'
    rx, ry = pool
    body += f'<ellipse cx="{tx}" cy="{ty}" rx="{rx}" ry="{ry}" fill="url(#{uid}p)"/>'
    return S.svg_doc(body, defs, w=w, h=h)


def pop_tf(t, t_in, t_out, px, py, dur_in=0.35, dur_out=0.22, bob=4.0):
    """Pop-in with overshoot at t_in, puff-and-vanish at t_out (a Tf about the pivot)."""
    if t < t_in or t > t_out + dur_out:
        return Tf(alpha=0.0)
    if t < t_out:
        u = t - t_in
        k = M.ease("back")(clamp(u / dur_in))
        return Tf(sx=max(0.01, k), sy=max(0.01, k), dy=-bob * math.sin(2 * math.pi * u / 2.2), px=px, py=py)
    u = (t - t_out) / dur_out
    return Tf(sx=1 + 0.15 * u, sy=1 + 0.15 * u, alpha=1 - u, px=px, py=py)


def pop_k(t, t_in, t_out, dur_in=0.35, dur_out=0.22):
    """(scale, alpha) of a pop-in / pop-out."""
    if t < t_in or t > t_out + dur_out:
        return 0.0, 0.0
    if t < t_out:
        return max(0.01, M.ease("back")(clamp((t - t_in) / dur_in))), 1.0
    u = (t - t_out) / dur_out
    return 1 + 0.15 * u, 1 - u


# ================================================================== the memory panel (line 3)
PX0, PY0 = 560, 290            # panel canvas top-left on the stage
PW, PH = 1180, 760             # panel canvas size
IR = (70, 76, 1030, 610)       # inner picture (local): x0, y0, x1, y1
IR_R = 70                      # its corner radius
MGY = 552                      # memory ground line (local y)
TAIL_TO = (DAVID_X - PX0 + 10, 1300 - 330 * K + 20 - PY0)   # toward David's head (local)


def _rr_d(x0, y0, x1, y1, r):
    return (f"M{x0 + r},{y0} L{x1 - r},{y0} Q{x1},{y0} {x1},{y0 + r} L{x1},{y1 - r} Q{x1},{y1} {x1 - r},{y1} "
            f"L{x0 + r},{y1} Q{x0},{y1} {x0},{y1 - r} L{x0},{y0 + r} Q{x0},{y0} {x0 + r},{y0} Z")


def panel_frame_svg():
    """The puffy cream thought-cloud around the picture, with three little puffs trailing toward David."""
    x0, y0, x1, y1 = IR
    fill = "#fff8ea"
    puffs = ""
    per = []
    n_top = 9
    for i in range(n_top + 1):
        u = i / n_top
        per.append((x0 + (x1 - x0) * u, y0 - 6))
        per.append((x0 + (x1 - x0) * u, y1 + 6))
    for i in range(1, 5):
        u = i / 5
        per.append((x0 - 6, y0 + (y1 - y0) * u))
        per.append((x1 + 6, y0 + (y1 - y0) * u))
    for i, (px, py) in enumerate(per):
        r = 46 + 8 * math.sin(i * 1.7)
        puffs += f'<circle cx="{f1(px)}" cy="{f1(py)}" r="{f1(r)}" ATTR/>'
    puffs += f'<rect x="{x0 - 20}" y="{y0 - 20}" width="{x1 - x0 + 40}" height="{y1 - y0 + 40}" rx="60" ATTR/>'
    body = puffs.replace("ATTR", f'fill="{fill}" stroke="{INK}" stroke-width="10"') + puffs.replace("ATTR", f'fill="{fill}"')
    tx, ty = TAIL_TO
    sx_, sy_ = (x0 + x1) / 2 + 40, y1 + 40
    for k, r_ in ((0.42, 24), (0.66, 16), (0.86, 10)):
        body += (f'<circle cx="{f1(sx_ + (tx - sx_) * k)}" cy="{f1(sy_ + (ty - sy_) * k)}" r="{r_}" fill="{fill}" '
                 f'stroke="{INK}" stroke-width="4.5"/>')
    return S.svg_doc(S.g(body, filter="wobble-fine"), w=PW, h=PH)


def panel_bg_svg():
    """The remembered hillside at Bethlehem: sunny sky, soft hills, an olive tree, flowers (clipped to the picture)."""
    x0, y0, x1, y1 = IR
    defs = (S.lin_grad("s8msky", [(0, "#a9d8e8"), (0.7, "#e6f1dc"), (1, "#f7efcf")]) +
            S.lin_grad("s8mgr", [(0, "#a8c868"), (1, "#7fa64e")]) +
            f'<clipPath id="s8mclip"><path d="{_rr_d(x0, y0, x1, y1, IR_R)}"/></clipPath>')
    b = f'<rect x="{x0 - 10}" y="{y0 - 10}" width="{x1 - x0 + 20}" height="{y1 - y0 + 20}" fill="url(#s8msky)"/>'
    b += f'<circle cx="{x1 - 140}" cy="{y0 + 90}" r="46" fill="#fbd46b" stroke="{S.mix(P["sun_hot"], INK, 0.3)}" stroke-width="4"/>'
    b += S.cloud(x0 + 200, y0 + 90, 170, 50, "#fdf6e8", seed=3, sw=3)
    b += S.path(S.hill(x0 - 60, x1 + 60, y0 + 330, 120, seed=11, bumps=2, bottom=y1 + 20), fill="#c2d69a", sw=3)
    b += S.path(S.hill(x0 - 80, x1 + 80, MGY - 40, 70, seed=4, bumps=3, bottom=y1 + 20), fill="url(#s8mgr)", sw=3.5)
    b += f'<rect x="{x0 - 10}" y="{MGY - 6}" width="{x1 - x0 + 20}" height="{y1 - MGY + 20}" fill="#8fb556"/>'
    out = S.g(b, filter="wobble")
    out += PR.olive_tree(x0 + 120, MGY - 36, 0.5, seed=2)
    for i, (gx, v) in enumerate(((x0 + 60, 2), (x0 + 360, 0), (x0 + 620, 2), (x1 - 40, 0), (x0 + 840, 2))):
        out += PR.grass_tuft(gx, MGY + 40 + 10 * (i % 2), 0.7, variant=v)
    rim = (f'<path d="{_rr_d(x0, y0, x1, y1, IR_R)}" fill="none" stroke="#e8c062" stroke-width="5" opacity="0.8"/>')
    return S.svg_doc(f'<g clip-path="url(#s8mclip)">{out}</g>', defs, w=PW, h=PH), rim


def panel_rim_svg():
    x0, y0, x1, y1 = IR
    d = _rr_d(x0, y0, x1, y1, IR_R)
    return S.svg_doc(S.g(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6"/>'
                         f'<path d="{_rr_d(x0 + 9, y0 + 9, x1 - 9, y1 - 9, IR_R - 8)}" fill="none" stroke="#e8c062" '
                         f'stroke-width="4" opacity="0.85"/>', filter="wobble-fine"), w=PW, h=PH)


def _rr_mask():
    x0, y0, x1, y1 = IR
    from PIL import ImageDraw
    m = Image.new("L", (PW * 2, PH * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([x0 * 2 + 4, y0 * 2 + 4, x1 * 2 - 4, y1 * 2 - 4], radius=IR_R * 2 - 4, fill=255)
    return m.resize((PW, PH), Image.LANCZOS)


class MemoryPanel:
    """Dynamic layer: the thought-cloud with the remembered hillside and its animated figures (actors in panel-local
    coordinates, clipped to the picture), popping in / out about the tail."""

    def __init__(self, t_in, t_out, actors):
        self.t_in, self.t_out, self.actors = t_in, t_out, actors
        bg, _ = panel_bg_svg()
        self.docs = [panel_frame_svg(), bg, panel_rim_svg()]
        self.imgs = None
        self.mask = None
        self._cache = {}

    def _load(self):
        if self.imgs is None:
            from engine import raster
            from engine import watercolor as WCm
            ims = []
            for i, d in enumerate(self.docs):
                im = raster.rasterize(d.replace(S.BOIL_TOKEN, "1"), PW, PH)
                if i < 2:
                    im = WCm.watercolor(im, seed=81 + i, strength=0.6)
                ims.append(im)
            self.imgs = ims
            self.mask = _rr_mask()
        return self.imgs

    def __call__(self, t):
        k, a = pop_k(t, self.t_in, self.t_out)
        if a <= 0.002:
            return None
        frame_im, bg, rim = self._load()
        content = bg.copy()
        for act in self.actors:
            r = act(t)
            if r is None:
                continue
            im, (x, y) = r
            paste(content, im, x, y)
        al = np.asarray(content.getchannel("A"), np.float32) * (np.asarray(self.mask, np.float32) / 255.0)
        content.putalpha(Image.fromarray(al.astype(np.uint8), "L"))
        out = frame_im.copy()
        out.alpha_composite(content)
        out.alpha_composite(rim)
        piv = TAIL_TO
        bobv = -4 * math.sin(2 * math.pi * (t - self.t_in) / 2.4)
        if abs(k - 1) > 0.004:
            nw, nh = max(2, int(PW * k)), max(2, int(PH * k))
            out = out.resize((nw, nh), Image.BILINEAR)
        else:
            k = 1.0
        if a < 0.998:
            arr = np.asarray(out).copy()
            arr[..., 3] = (arr[..., 3].astype(np.float32) * a).astype(np.uint8)
            out = Image.fromarray(arr, "RGBA")
        x = PX0 + piv[0] - piv[0] * k
        y = PY0 + piv[1] - piv[1] * k + bobv
        return out, (x, y)


# ================================================================== shared poses and sprites
_P = C._P
POSES = C.POSES
SIT = dict(POSES["king_sit_stool"])


def sit(**kw):
    d = dict(SIT)
    d.update(kw)
    return d


SAUL_SIT = {
    "worried": (sit(), "worried"),
    "listen": (sit(look=(-0.05, 0), h=-4), "worried"),
    "hear": (sit(look=(-0.05, 0), h=-6), "surprised"),
    "point": (sit(arms=(("ik", "knee", 0, 0.25, 1), ("fk", 84, 96)), hands=("fist", "point")), "neutral"),
    "look": (sit(h=-2), "neutral"),
    "surprise": (sit(t=-12, h=-8, arms=(("fk", -40, -20), ("fk", 50, 110)), hands=("open", "open")), "surprised"),
    "small": (sit(t=4, arms=(("ik", "knee", 0, 0.25, 1), ("fk", 48, 62)), hands=("fist", "palm")), "surprised"),
    "tall": (sit(t=-4, h=-10, arms=(("ik", "knee", 0, 0.25, 1), ("fk", 100, 135)), hands=("fist", "open"),
                 look=(0.02, -0.06)), "worried"),
    "big": (sit(t=-8, h=-10, arms=(("fk", -150, -172), ("fk", 104, 140)), hands=("open", "open")), "worried"),
    "wow": (sit(t=-6, h=-4), "surprised"),
    "up": (sit(t=-4, h=-14, look=(0.02, -0.08)), "surprised"),
    "kind": (sit(), "kind"),
}
D_ST = ("fk", 40, 76)          # David's near arm holding his staff (the crook stands in front of him)
DAVID_POSE = {
    "stand": (_P(arms=(("fk", 14, 8), D_ST)), "happy"),
    "puzzled": (_P(h=-4, arms=(("fk", 14, 8), D_ST)), "puzzled"),
    "talk": (_P(h=-4, arms=(("fk", 34, 86), D_ST), hands=("open", "fist")), "happy"),
    "brave": (_P(h=-6, legs=((8, 3), (-7, -3)), arms=(("fk", 120, 165), D_ST), hands=("fist", "fist")), "brave"),
    "point_up": (_P(h=-16, legs=((5, 2), (-5, -2)), arms=(("fk", 132, 162), D_ST), hands=("point", "fist"),
                    look=(0.03, -0.10)), "brave"),
    "lookup": (_P(h=-12, arms=(("fk", 14, 8), D_ST), look=(0.02, -0.08)), "happy"),
    "bless": (_P(h=-6, arms=(("fk", 14, 8), D_ST), look=(0.02, -0.06)), "peaceful"),
}


def david_sprite(seed=60):
    return sprite(460, 540, 230, 500, seed=seed)


def david_draw(sp, name, facing=1, expr=None):
    ps, e = DAVID_POSE[name]
    D = C._david_design(False, True)
    return sp.add(david_fig(ps, expr or e, front=C._staff_near(D))(sp.ax, sp.ay, K, facing))


def saul_sprite(seed=61):
    return sprite(700, 720, 350, 680, seed=seed)


def saul_draw(sp, name, facing=-1, expr=None):
    if name in SAUL_SIT:
        ps, e = SAUL_SIT[name]
        return sp.add(saul_fig(ps, expr or e)(sp.ax, sp.ay, K, facing))
    return sp.add(C.king(sp.ax, sp.ay, K, facing, pose=name, attire="saul", expr=expr, stool=False))


SAUL_BLESS = _P(h=-2, arms=(("fk", 12, 6), ("fk", 102, 126)), hands=("fist", "palm"), expr="kind")
SAUL_A = WALK_A * 1.1          # Saul's ankle travel (1.1 x an adult)
DAVID_A = WALK_A * 0.68        # David's (boy legs)
DAVID_LK = 0.68


def add_tent(sc, toff=0.0, table_items=None, saul_stool=True):
    """The tent behind the figures. toff shifts every cyclic motion's clock (s09 passes s08's duration - 1 s so the
    cross-dissolve between the two scenes matches). table_items(t) -> 'all' | 'mail_sword' | 'sword' | 'none'."""
    waves = [outside_svg(w) for w in (0.0, 0.33, 0.66)]
    sc.add("outside", waves, wc=0.6, frame_at=lambda t: float(int((t + toff) * 3) % 3))
    sc.add("wall", wall_svg(), wc=0.8)
    sc.add("lamp_glow", lamp_glow_svg(), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.82 + 0.1 * math.sin((t + toff) * 5.1) + 0.06 * math.sin((t + toff) * 13.3)))
    sc.add("lamp", lamp_svg(), wc=0.5, motion=M.sway(0.7, 4.6, pivot=(LAMP[0], LAMP_TOP), phase=toff / 4.6))
    sc.add("floor", floor_svg(), wc=0.8)
    sc.add("doorlight", doorlight_svg(), wc=0, blend="screen",
           motion=lambda t: Tf(alpha=0.9 + 0.1 * math.sin((t + toff) * 0.9)))
    if table_items is None:
        sc.add("table", table_svg("all"), wc=0.6)
    else:
        states = ["all", "mail_sword", "sword", "none"]
        sc.add("table", [table_svg(s_) for s_ in states], wc=0.6,
               frame_at=lambda t: float(states.index(table_items(t))))
    sc.add("rack", rack_svg(), wc=0.6)
    if saul_stool:
        sc.add("stool", doc(PR.camp_stool(STOOL_X, FY, K, -1)), wc=0.6)


def add_fg(sc, toff=0.0):
    sc.add("fg", fg_svg(), wc=0.7)


def shadow_layer(sc, name, x_fn, width=120, opacity=0.24, alpha=None, z=None):
    sc.add(name, doc(C.ground_shadow(0, FY, K, width=width, opacity=opacity)), wc=0,
           motion=lambda t: Tf(dx=x_fn(t), alpha=1.0 if alpha is None else alpha(t)), z=z)


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration
    L = ctx.lines

    # ------------------------------------------------------------ beats (all from the narration)
    t_tell = pt(ctx, 0, "有人把大卫")                  # soldier A whispers to Saul
    t_hear = phrase_t(L[0], "告诉了扫罗王", 0.3) + 0.1  # Saul's brows go up
    t_send = pt(ctx, 0, "扫罗王就叫人")                # Saul points to the entrance: bring him!
    t_sb = t_send + 0.15                              # soldier B leads David in
    t_dv = t_send + 0.3
    t_wang = pt(ctx, 1, "王啊")
    t_fear = pt(ctx, 1, "大家都不用害怕")
    t_fight = pt(ctx, 1, "我要去跟那个巨人打")
    t_ni = pt(ctx, 2, "你？")                          # the double-take
    t_child = phrase_t(L[2], "你还是个孩子啊", 0.1) + 0.05
    t_young = pt(ctx, 2, "他从年轻的时候")
    t_war = pt(ctx, 2, "就是打仗的勇士了")
    t_sheep = pt(ctx, 3, "我替爸爸放羊")
    t_lion = pt(ctx, 3, "有狮子来抓小羊")
    t_bear = pt(ctx, 3, "也有熊来抓小羊")
    t_chase = pt(ctx, 3, "我就去追")
    t_save = pt(ctx, 3, "把小羊从它们嘴里")
    t_god = pt(ctx, 4, "上帝救我")
    t_giant = pt(ctx, 4, "也一定会救我")
    t_ok = pt(ctx, 5, "好吧")
    t_go = pt(ctx, 5, "你去吧")
    t_bless = pt(ctx, 5, "愿上帝")
    p_in, p_out = t_sheep + 0.15, L[3].end + 0.35     # the memory panel

    # ------------------------------------------------------------ TENT (behind the figures)
    add_tent(sc)

    # light from above on David (God's help - light only)
    lx, ly = DAVID_X - 260, 260
    beam_a = lambda t: (M.progress(t, t_god - 0.05, t_god + 0.8, "sine") *
                        (1 - 0.55 * M.progress(t, t_giant + 1.5, t_giant + 3.5, "sine")) *
                        (1 - M.progress(t, t_ok - 0.3, t_ok + 0.8, "sine")) *
                        (0.88 + 0.12 * math.sin(2 * math.pi * (t - t_god) / 2.6)))
    sc.add("beam", rays_svg(lx, ly, DAVID_X + 10, FY - 30, 6, "s8b1", n=6, wk=1.7, pool=(240, 64)), wc=0,
           blend="screen", motion=lambda t: Tf(alpha=beam_a(t)))
    bless_a = lambda t: (M.progress(t, t_bless, t_bless + 1.2, "sine") * (0.85 + 0.15 * math.sin(2 * math.pi * t / 2.8)))
    gx = (DAVID_X + SAUL_END_X) / 2
    sc.add("bless_glow", S.svg_doc(f'<ellipse cx="{gx}" cy="{FY - 200}" rx="330" ry="300" fill="url(#s8bg)"/>',
                                   S.rad_grad("s8bg", [(0, "#fff0bc", 0.6), (0.6, "#ffe6a0", 0.2), (1, "#ffe6a0", 0)]),
                                   w=SW, h=SH), wc=0, blend="screen", motion=lambda t: Tf(alpha=bless_a(t)))

    # ------------------------------------------------------------ SOLDIER A (whispers, then stands by the table)
    spA = sprite(520, 620, 260, 590, seed=63)
    a_stand = spA.add(soldier_fig(1, dict(POSES["stand"]), "neutral")(spA.ax, spA.ay, K, -1))
    a_whisp = spA.add(soldier_fig(1, dict(POSES["whisper"], t=16, arms=(("fk", 8, 3), ("ik", "head", 1.3, 0.62, 1))),
                                  "neutral")(spA.ax, spA.ay, K, -1))
    a_happy = spA.add(soldier_fig(1, dict(POSES["stand"]), "happy")(spA.ax, spA.ay, K, -1))
    a_sched = [(0, a_stand, 0), (t_tell - 0.1, a_whisp, 0.6), (t_send - 0.35, a_stand, 0.5),
               (t_bless + 0.6, a_happy, 0.3)]
    shadow_layer(sc, "shA", lambda t: SOLA_X)
    sc.add_dynamic("soldierA", Actor(spA, a_sched, lambda t: (SOLA_X, FY), bper=3.4, phase=0.2))

    # ------------------------------------------------------------ KING SAUL
    spS = saul_sprite()
    S_ = {n: saul_draw(spS, n) for n in SAUL_SIT}
    s_stand = saul_draw(spS, "stand", expr="kind")
    s_talk = saul_draw(spS, "talk", expr="kind")
    s_bless = spS.add(saul_fig(SAUL_BLESS, "kind")(spS.ax, spS.ay, K, -1))
    sW = walk_drawings(spS, lambda ps: saul_fig(ps, "kind"), K, -1, SAUL_A, lk=1.1)
    s_adv = walk_adv(SAUL_A, K)
    t_sw = t_ok + 0.55
    s_walk = WalkPath([(t_sw, STOOL_X, SAUL_END_X, 24.0)], sW, s_adv)
    t_sarr = s_walk.end(0)
    s_sched = [(0, S_["worried"], 0), (t_tell + 0.15, S_["listen"], 0.4), (t_hear, S_["hear"], 0.4),
               (t_send, S_["point"], 0.8), (t_send + 1.7, S_["look"], 0.4), (t_fight + 0.4, S_["worried"], 0.4),
               (t_ni - 0.05, S_["look"], 0.3), (t_ni + 0.28, S_["surprise"], 1.5), (t_child, S_["small"], 0.7),
               (t_young, S_["tall"], 0.7), (t_war, S_["big"], 0.9), (L[2].end + 0.3, S_["worried"], 0.5),
               (t_lion + 0.5, S_["wow"], 0.4), (t_bear + 0.6, S_["worried"], 0.4), (t_save + 0.3, S_["wow"], 0.7),
               (t_god + 0.2, S_["up"], 0.6), (t_giant + 1.2, S_["kind"], 0.5),
               (t_ok, s_stand, 1.3), (t_sw - 0.1, sW[0], 0.2), (t_sarr, s_talk, 0.5), (t_bless, s_bless, 0.8)]
    s_pos = lambda t: (s_walk.x(t), FY)
    shadow_layer(sc, "shS", lambda t: s_walk.x(t), width=170)
    sc.add_dynamic("saul", Actor(spS, s_sched, s_pos, walk=s_walk.frame, bper=3.6, phase=0.5, breathe=0.008))
    sc.add("marks", doc(surprise_marks(STOOL_X - 10, FY - 360 * K, 1.0, -1)), wc=0,
           motion=lambda t: pop_tf(t, t_ni + 0.28, t_ni + 1.3, STOOL_X - 10, FY - 330 * K, dur_in=0.2))

    # ------------------------------------------------------------ SOLDIER B (leads David in, then on guard)
    spB = sprite(520, 680, 260, 640, seed=64)
    b_walk = walk_drawings(spB, lambda ps: soldier_fig(2, ps, "neutral", spear=True), K, 1, WALK_A,
                           arm=(None, (("fk", 48, 80), "fist")))
    b_stand = spB.add(C.soldier(spB.ax, spB.ay, K, 1, variant=2, pose="stand"))
    b_smile = spB.add(C.soldier(spB.ax, spB.ay, K, 1, variant=2, pose="stand", expr="happy"))
    b_path = WalkPath([(t_sb, 150, SOLB_X, 22.0)], b_walk, walk_adv(WALK_A, K))
    b_sched = [(0, b_stand, 0), (b_path.end(0), b_stand, 0.4), (t_save + 0.5, b_smile, 0.3)]
    shadow_layer(sc, "shB", lambda t: b_path.x(t), alpha=lambda t: 1.0 if t > t_sb else 0.0)
    sc.add_dynamic("soldierB", Actor(spB, b_sched, lambda t: (b_path.x(t), FY), walk=b_path.frame,
                                     alpha=lambda t: 1.0 if t > t_sb else 0.0, bper=3.2, phase=0.7))

    # ------------------------------------------------------------ DAVID
    spD = david_sprite()
    D_ = {n: david_draw(spD, n) for n in DAVID_POSE}
    d_brave2 = david_draw(spD, "brave")
    d_walk = walk_drawings(spD, lambda ps: david_fig(ps, "happy", front=C._staff_near(C._david_design(False, True))),
                           K, 1, DAVID_A, lk=DAVID_LK, arm=(None, (D_ST, "fist")))
    d_path = WalkPath([(t_dv, 40, DAVID_X, 30.0)], d_walk, walk_adv(DAVID_A, K))
    t_darr = d_path.end(0)
    d_sched = [(0, D_["stand"], 0), (t_darr, D_["stand"], 0.5), (t_wang, D_["talk"], 0.6),
               (t_fight, D_["brave"], 1.0), (t_fight + 1.6, d_brave2, 0.6),
               (t_ni + 0.3, D_["puzzled"], 0.5), (t_war + 0.9, D_["brave"], 0.5), (L[2].end + 0.4, D_["stand"], 0.3),
               (t_sheep, D_["talk"], 0.6), (t_chase, D_["brave"], 0.8), (t_save + 0.5, D_["talk"], 0.5),
               (t_god, D_["point_up"], 1.0), (t_giant, D_["brave"], 0.9), (L[4].end + 0.3, D_["stand"], 0.4),
               (t_ok + 0.1, D_["lookup"], 0.4), (t_bless + 0.1, D_["bless"], 0.4), (t_bless + 1.6, D_["stand"], 0.3)]
    shadow_layer(sc, "shD", lambda t: d_path.x(t), width=100, alpha=lambda t: 1.0 if t > t_dv else 0.0)
    sc.add_dynamic("david", Actor(spD, d_sched, lambda t: (d_path.x(t), FY), walk=d_path.frame,
                                  alpha=lambda t: 1.0 if t > t_dv else 0.0, bper=2.8, phase=0.1))

    add_fg(sc)

    # ------------------------------------------------------------ the memory panel
    sc.add_dynamic("memory", MemoryPanel(p_in, p_out, memory_actors(ctx, t_sheep, t_lion, t_bear, t_chase, t_save)))

    # ------------------------------------------------------------ CAMERA
    c_saul = Cam(1700, 1003, 1560)
    c_door = Cam(1240, 1003, 1800)
    c_two = Cam(1470, 1003, 1650)
    c_push = Cam(1560, 1012, 1500)
    c_mem = Cam(1390, 862, 1960)
    c_light = Cam(1420, 990, 1650)
    c_end = Cam(1330, 1003, 1560)
    sc.camera = M.cam_keys([
        (0.0, c_saul), (t_send - 0.5, Cam(1690, 1003, 1565)), (t_send + 1.7, c_door), (t_darr + 0.2, c_door),
        (t_darr + 2.2, c_two), (t_ni - 0.6, c_two), (t_ni + 0.6, c_push), (L[2].end - 0.6, c_push),
        (p_in + 0.2, c_mem), (p_out - 0.4, c_mem), (t_god + 1.6, c_light), (t_ok, c_light), (t_sarr + 0.6, c_end),
        (T - 1.0, CAM_MATCH), (T, CAM_MATCH)], "sine")

    # ------------------------------------------------------------ FX
    sc.fx = [
        FX.motes((300, 400, 2600, 1300), count=26, color=(255, 240, 200), size=(3, 6), alpha=90),
        FX.sparkles((DAVID_X - 220, 620, DAVID_X + 180, 1000), count=14, t0=t_god + 0.2, t1=t_ok + 0.4,
                    color=(255, 238, 170), size=(8, 16), period=1.5, drift=-12, seed=7),
        FX.sparkles((gx - 300, 560, gx + 260, 820), count=12, t0=t_bless + 0.3, t1=T - 1.05,
                    color=(255, 238, 170), size=(7, 14), period=1.7, drift=-8, seed=9),
        FX.vignette(lambda t: 0.28),
    ]

    # ------------------------------------------------------------ SOUND
    sc.sfx("crowd", 0, dur=T + 0.8, gain_db=-28, fade_in=0.8, fade_out=1.0, pan=-0.4)
    sc.sfx("wind_soft", 0, dur=T + 0.8, gain_db=-24, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_tell - 0.1, gain_db=-18, pan=0.4)
    sc.sfx("cloth", t_send, gain_db=-16, pan=0.3)
    sc.sfx("footsteps", t_sb, dur=t_darr - t_sb, gain_db=-13, fade_in=0.2, fade_out=0.3, pan=-0.4)
    sc.sfx("cloth", t_fight, gain_db=-16, pan=-0.1)
    sc.sfx("pop", t_ni + 0.28, gain_db=-10, pan=0.25)
    sc.sfx("cloth", t_war, gain_db=-16, pan=0.25)
    sc.sfx("pop", p_in, gain_db=-12, pan=-0.1)
    sc.sfx("sheep", p_in + 0.6, gain_db=-16, pan=-0.2)
    sc.sfx("sheep", t_lion + 1.1, gain_db=-13, pan=-0.3, pitch=1.25)
    sc.sfx("sheep", t_bear + 0.9, gain_db=-13, pan=0.1, pitch=1.3)
    sc.sfx("footsteps_run", t_chase, dur=1.8, gain_db=-16, fade_in=0.1, fade_out=0.3)
    sc.sfx("whoosh", t_chase + 0.5, gain_db=-16, pan=-0.4)
    sc.sfx("whoosh", t_save + 0.15, gain_db=-16, pan=0.2)
    sc.sfx("sparkle", t_save + 0.8, gain_db=-14)
    sc.sfx("sheep", t_save + 1.4, gain_db=-17, pitch=1.3)
    sc.sfx("pop", p_out, gain_db=-14)
    sc.sfx("chime", t_god + 0.05, gain_db=-9, pan=-0.2)
    sc.sfx("cloth", t_ok, gain_db=-14, pan=0.2)
    sc.sfx("footsteps", t_sw, dur=t_sarr - t_sw + 0.1, gain_db=-14, fade_in=0.1, fade_out=0.2, pan=0.1)
    sc.sfx("chime", t_bless + 0.1, gain_db=-12)
    return sc


# ================================================================== the memory figures (panel-local coordinates)
MD, ML, MB, MS, MLb = 0.76, 0.50, 0.56, 0.6, 0.66      # David, lion, bear, sheep, lamb scales in the memory


def _carry_lamb(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        cx = (W0[0] + W1[0]) / 2 + 4
        y = max(W0[1], W1[1]) + 26
        return PR.sheep(cx, y, 0.62, 1, lamb=True) + C._fist(W1, hr, D["skin"], 0, 2)
    return front


def memory_actors(ctx, t_sheep, t_lion, t_bear, t_chase, t_save):
    acts = []
    G = MGY

    # sheep and lambs
    spSh = sprite(300, 240, 150, 216, wc=0.6, seed=71)
    sh0g = spSh.add(PR.sheep(spSh.ax, spSh.ay, MS, -1, variant=0, pose="graze"))
    sh0b = spSh.add(PR.sheep(spSh.ax, spSh.ay, MS, -1, variant=0, pose="bleat"))
    sh1s = spSh.add(PR.sheep(spSh.ax, spSh.ay, MS, -1, variant=3, pose="stand"))
    sh1b = spSh.add(PR.sheep(spSh.ax, spSh.ay, MS, -1, variant=3, pose="bleat"))
    sh1g = spSh.add(PR.sheep(spSh.ax, spSh.ay, MS, -1, variant=3, pose="graze"))
    acts.append(Actor(spSh, [(0, sh0g, 0), (t_sheep + 0.6, sh0b, 0.3), (t_sheep + 1.6, sh0g, 0.3),
                             (t_lion + 1.0, sh0b, 1.4), (t_lion + 2.2, sh0g, 0.3), (t_save + 1.3, sh0b, 0.6),
                             (t_save + 2.4, sh0g, 0.3)], lambda t: (470, G), breathe=0.02, bper=2.2))
    acts.append(Actor(spSh, [(0, sh1s, 0), (t_sheep + 1.5, sh1g, 0.3), (t_bear + 0.8, sh1b, 1.4),
                             (t_bear + 2.0, sh1s, 0.3), (t_save + 1.7, sh1g, 0.3)],
                      lambda t: (720, G + 6), breathe=0.02, bper=2.5, phase=0.4))

    spLb = sprite(220, 190, 110, 170, wc=0.6, seed=72)
    lb_r = spLb.add(PR.sheep(spLb.ax, spLb.ay, MLb, 1, variant=0, lamb=True))
    lb_l = spLb.add(PR.sheep(spLb.ax, spLb.ay, MLb, -1, variant=0, lamb=True))
    lb2_l = spLb.add(PR.sheep(spLb.ax, spLb.ay, MLb, -1, variant=3, lamb=True))

    # lion: walks in from the left, crouches, takes lamb A by the scruff; drops it and runs off when David comes
    spLi = sprite(380, 300, 180, 270, wc=0.6, seed=73)
    li_w = [spLi.add(PR.lion(spLi.ax, spLi.ay, ML, 1, pose=p)) for p in ("walk_a", "walk_b")]
    li_hold = spLi.add(PR.lion(spLi.ax, spLi.ay, ML, 1, pose="stand", mouth=0.33))
    li_run = [spLi.add(PR.lion(spLi.ax, spLi.ay, ML, -1, pose=p, eyes="closed")) for p in ("walk_a", "walk_b")]
    LX = 200
    t_li0, t_li1 = t_lion, t_lion + 0.85
    t_grab = t_li1 + 0.35
    t_drop = t_chase + 0.5
    t_lr1 = t_drop + 0.9

    def li_x(t):
        if t < t_li1:
            return -140 + (LX + 140) * M.progress(t, t_li0, t_li1, "linear")
        if t < t_drop:
            return LX
        return LX - 420 * M.progress(t, t_drop, t_lr1, "in")

    def li_frame(t):
        if t_li0 <= t < t_li1:
            return li_w[int((t - t_li0) / 0.17) % 2]
        if t >= t_drop:
            return li_run[int((t - t_drop) / 0.13) % 2]
        return None

    acts.append(Actor(spLi, [(0, li_w[0], 0), (t_li1, li_hold, 0.6)], lambda t: (li_x(t), G - 2), walk=li_frame,
                      alpha=lambda t: 1.0 if t_li0 <= t <= t_lr1 else 0.0, breathe=0.015, bper=1.8,
                      squash=lambda t: 1 - 0.07 * M.progress(t, t_li1 - 0.1, t_grab - 0.1, "sine") *
                      (1 - M.progress(t, t_drop - 0.2, t_drop, "sine"))))
    mouth_l = (LX + 92, G - 100)

    # bear: from the right, takes lamb B; runs off when David snatches the lamb back
    spBe = sprite(380, 300, 190, 270, wc=0.6, seed=74)
    be_w = [spBe.add(PR.bear(spBe.ax, spBe.ay, MB, -1, pose=p)) for p in ("walk_a", "walk_b")]
    be_hold = spBe.add(PR.bear(spBe.ax, spBe.ay, MB, -1, pose="stand", mouth=0.45))
    be_run = [spBe.add(PR.bear(spBe.ax, spBe.ay, MB, 1, pose=p)) for p in ("run_a", "run_b")]
    BX = 900
    t_be0, t_be1 = t_bear, t_bear + 0.8
    t_bgrab = t_be1 + 0.35
    t_snatch = t_save + 0.15
    t_br1 = t_snatch + 1.0

    def be_x(t):
        if t < t_be1:
            return 1240 - (1240 - BX) * M.progress(t, t_be0, t_be1, "linear")
        if t < t_snatch:
            return BX
        return BX + 420 * M.progress(t, t_snatch, t_br1, "in")

    def be_frame(t):
        if t_be0 <= t < t_be1:
            return be_w[int((t - t_be0) / 0.2) % 2]
        if t >= t_snatch:
            return be_run[int((t - t_snatch) / 0.14) % 2]
        return None

    acts.append(Actor(spBe, [(0, be_w[0], 0), (t_be1, be_hold, 0.6)], lambda t: (be_x(t), G + 2), walk=be_frame,
                      alpha=lambda t: 1.0 if t_be0 <= t <= t_br1 else 0.0, breathe=0.015, bper=2.0, phase=0.3))
    mouth_b = (BX - 122, G - 66)

    # memory David: watches the sheep; surprised; runs to the lion, then to the bear; holds the lamb
    spMD = sprite(340, 300, 170, 276, wc=0.6, seed=75)
    md_stand = spMD.add(C.david(spMD.ax, spMD.ay, MD, 1, pose="stand", staff=True))
    md_surp = spMD.add(C.david(spMD.ax, spMD.ay, MD, -1, pose="stand", staff=True, expr="surprised"))
    md_surp_r = spMD.add(C.david(spMD.ax, spMD.ay, MD, 1, pose="stand", staff=True, expr="surprised"))
    md_run_l = [spMD.add(C.david(spMD.ax, spMD.ay, MD, -1, pose=p)) for p in ("run_a", "run_b")]
    md_run_r = [spMD.add(C.david(spMD.ax, spMD.ay, MD, 1, pose=p)) for p in ("run_a", "run_b")]
    D = C._david_design(False, True)
    D["mid"], D["front"] = C._bag_mid, _carry_lamb(D)
    ps = dict(POSES["dv_carry_basket"])
    md_hold = spMD.add(fig(D, C._BOY, ps, "happy", spMD.ax, spMD.ay, MD, -1, "md-lamb"))
    DX0, DXL, DXR = 600, LX + 150, BX - 175
    t_c0 = t_chase
    t_c1 = t_drop + 0.05
    t_c2 = t_c1 + 0.12
    t_c3 = t_snatch

    def md_x(t):
        if t < t_c0:
            return DX0
        if t < t_c1:
            return DX0 + (DXL - DX0) * M.progress(t, t_c0, t_c1, "linear")
        if t < t_c2:
            return DXL
        if t < t_c3:
            return DXL + (DXR - DXL) * M.progress(t, t_c2, t_c3, "linear")
        return DXR

    def md_frame(t):
        if t_c0 <= t < t_c1:
            return md_run_l[int((t - t_c0) / 0.13) % 2]
        if t_c2 <= t < t_c3:
            return md_run_r[int((t - t_c2) / 0.13) % 2]
        return None

    acts.append(Actor(spMD, [(0, md_stand, 0), (t_lion + 0.9, md_surp, 0.8), (t_bear + 0.8, md_surp_r, 0.8),
                             (t_c0, md_run_l[0], 0.4), (t_c1, md_surp, 0.4), (t_c3, md_hold, 1.0)],
                      lambda t: (md_x(t), G + 10), walk=md_frame, breathe=0.015, bper=2.2))

    # lamb A: by the lion's paws -> held in its mouth -> dropped, then trots to David
    t_la1 = t_drop + 1.2

    def la_pos(t):
        if t < t_grab:
            return 345, G + 12
        if t < t_drop:
            u = M.progress(t, t_grab, t_grab + 0.25, "out")
            return M.lerp(345, mouth_l[0] + 8, u), M.lerp(G + 12, mouth_l[1] + 48, u)
        u = M.progress(t, t_drop, t_drop + 0.25, "in")
        x = mouth_l[0] + 8
        y = M.lerp(mouth_l[1] + 48, G + 12, u)
        if t > t_drop + 0.5:
            x = M.lerp(x, DXR - 110, M.progress(t, t_drop + 0.5, t_la1 + 0.6, "sine"))
            y -= 8 * abs(math.sin(math.pi * (t - t_drop - 0.5) / 0.22))
        return x, y

    def la_rot(t):
        if t_grab <= t < t_drop:
            return 8 * math.sin(2 * math.pi * (t - t_grab) / 1.1)
        return 0.0

    acts.append(Actor(spLb, [(0, lb_r, 0), (t_drop + 0.4, lb_r, 0.5)], la_pos, rot=la_rot, breathe=0.02, bper=1.6))

    # lamb B: held by the bear, then in David's arms (it is drawn with him)
    def lb_pos(t):
        if t < t_bgrab:
            return 790, G + 14
        u = M.progress(t, t_bgrab, t_bgrab + 0.25, "out")
        return M.lerp(790, mouth_b[0] - 6, u), M.lerp(G + 14, mouth_b[1] + 46, u)

    acts.append(Actor(spLb, [(0, lb2_l, 0)], lb_pos, alpha=lambda t: 1.0 if t < t_c3 else 0.0,
                      rot=lambda t: -8 * math.sin(2 * math.pi * (t - t_bgrab) / 1.2) if t >= t_bgrab else 0.0,
                      breathe=0.02, bper=1.7, phase=0.5))

    # hearts over David and his lamb
    spH = sprite(220, 160, 110, 150, wc=0.3, seed=76)
    hh = spH.add(S.g(heart(70, 70, 40) + heart(140, 50, 30, "#f4a3a8") + heart(100, 120, 24), filter="wobble-fine"))
    acts.append(lambda t: (lambda k: None if k[1] <= 0.01 else spH.place(hh, DXR - 10, G - 150 * MD / 0.62 - 40 -
                                                                      10 * math.sin(2 * math.pi * t / 1.8),
                                                                      k[0], k[0], 0, k[1]))(
        pop_k(t, t_snatch + 0.5, t_save + 3.4 if t_save + 3.4 < 1e9 else 1e9)))
    return acts
