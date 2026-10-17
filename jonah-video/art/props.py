"""DOCSTRING_PLACEHOLDER"""
import hashlib
import math
import random

from art import style as S
from art.style import INK, P

# ====================================================================== helpers
EYE_WHITE = "#fbf6ea"
PUPIL = "#2e2630"
HILITE = "#fffaf0"
CREAM = "#f7efdc"

SHIP_DECK_Y = -165
SHIP_INTERIOR = (-360, -146, 360, 34)
SHIP_BED = (-130, 240, -4)


def _f(v):
    return f"{v:.1f}"


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, float(v)))


def _lerp(a, b, t):
    return a + (b - a) * t


def _lerp2(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _smooth(t):
    t = _clamp(t)
    return t * t * (3 - 2 * t)


def _uid(prefix, *parts):
    return f"pr-{prefix}-{hashlib.md5(repr(parts).encode()).hexdigest()[:10]}"


def _st(sw=4.0, color=INK):
    return f'stroke="{color}" stroke-width="{_f(sw)}" stroke-linejoin="round" stroke-linecap="round"'


def _p(d, fill="none", sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<path d="{d}" fill="{fill}" {s} {extra}/>'


def _sm(pts, closed=True, tension=1.0):
    return S.smooth_path(pts, closed, tension)


def _poly(pts, closed=True):
    d = "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in pts)
    return d + (" Z" if closed else "")


def _ell(cx, cy, rx, ry, fill, sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<ellipse cx="{_f(cx)}" cy="{_f(cy)}" rx="{_f(rx)}" ry="{_f(ry)}" fill="{fill}" {s} {extra}/>'


def _circ(cx, cy, r, fill, sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" fill="{fill}" {s} {extra}/>'


def _rect(x, y, w, h, fill, sw=4.0, rx=0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return (f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(rx)}" '
            f'fill="{fill}" {s} {extra}/>')


def _line(x1, y1, x2, y2, sw=4.0, color=INK, extra=""):
    return f'<path d="M{_f(x1)},{_f(y1)} L{_f(x2)},{_f(y2)}" fill="none" {_st(sw, color)} {extra}/>'


def _tube(d, width, fill, sw=4.0, extra=""):
    """A rounded 'tube' along path data d: ink stroke underneath, coloured stroke on top."""
    return (f'<path d="{d}" fill="none" {_st(width + 2 * sw, INK)} {extra}/>'
            f'<path d="{d}" fill="none" {_st(width, fill)} {extra}/>')


def _rot(px, py, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))


def _g(body, tr=None, extra=""):
    t = f' transform="{tr}"' if tr else ""
    return f"<g{t} {extra}>{body}</g>"


def _clip(cid, d, body):
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{body}</g>'


def _place(body, x, y, scale=1.0, facing=1, rot=0.0, filt="wobble-fine"):
    """Put local markup (anchor at 0,0, facing right, scale 1) onto the stage."""
    sx = scale * (-1 if facing < 0 else 1)
    tr = f"translate({_f(x)},{_f(y)})"
    if rot:
        tr += f" rotate({rot:.2f})"
    tr += f" scale({sx:.4f},{scale:.4f})"
    inner = f'<g transform="{tr}">{body}</g>'
    return f'<g filter="url(#{filt})">{inner}</g>' if filt else inner


def local_to_stage(x, y, scale, facing, lx, ly):
    """Convert a point (lx, ly) given in a drawing's local scale-1 coordinates (relative to its
    anchor, facing right) to stage pixels for a drawing placed at (x, y, scale, facing)."""
    return (x + lx * scale * (-1 if facing < 0 else 1), y + ly * scale)


def _eye(cx, cy, r, kind="open", look=(0.35, 0.15), sw=4.0):
    """Big friendly eye. kind: open | closed | happy | surprised."""
    if kind == "closed":
        d = f"M{_f(cx - r)},{_f(cy)} Q{_f(cx)},{_f(cy + r * 0.85)} {_f(cx + r)},{_f(cy)}"
        out = _p(d, sw=sw * 1.25)
        for k in (-0.6, 0.0, 0.6):
            bx, by = cx + k * r * 0.95, cy + r * 0.38 * (1 - k * k * 0.6)
            out += _line(bx, by, bx + k * r * 0.25, by + r * 0.32, sw=sw * 0.8)
        return out
    if kind == "happy":
        d = f"M{_f(cx - r)},{_f(cy + r * 0.3)} Q{_f(cx)},{_f(cy - r * 0.95)} {_f(cx + r)},{_f(cy + r * 0.3)}"
        return _p(d, sw=sw * 1.3)
    if kind == "surprised":
        rr = r * 1.12
        out = _ell(cx, cy, rr * 0.95, rr * 1.08, EYE_WHITE, sw)
        out += _circ(cx + look[0] * r * 0.1, cy, r * 0.36, PUPIL, 0)
        out += _circ(cx + look[0] * r * 0.1 - r * 0.12, cy - r * 0.13, r * 0.12, HILITE, 0)
        return out
    out = _ell(cx, cy, r * 0.95, r * 1.05, EYE_WHITE, sw)
    ix, iy = cx + look[0] * r * 0.32, cy + look[1] * r * 0.3
    out += _circ(ix, iy, r * 0.62, PUPIL, 0)
    out += _circ(ix - r * 0.2, iy - r * 0.24, r * 0.22, HILITE, 0)
    out += _circ(ix + r * 0.22, iy + r * 0.2, r * 0.09, HILITE, 0)
    return out


def _dot_eye(cx, cy, r, kind="open"):
    """Small picture-book dot eye with a highlight (for little creatures and animals)."""
    if kind == "closed":
        return _p(f"M{_f(cx - r * 1.2)},{_f(cy)} Q{_f(cx)},{_f(cy + r * 1.1)} {_f(cx + r * 1.2)},{_f(cy)}",
                  sw=max(2.5, r * 0.55))
    if kind == "happy":
        return _p(f"M{_f(cx - r * 1.2)},{_f(cy + r * 0.4)} Q{_f(cx)},{_f(cy - r * 1.1)} "
                  f"{_f(cx + r * 1.2)},{_f(cy + r * 0.4)}", sw=max(2.5, r * 0.55))
    return _circ(cx, cy, r, PUPIL, 0) + _circ(cx - r * 0.3, cy - r * 0.35, r * 0.36, HILITE, 0)


def _blush(cx, cy, rx, ry, op=0.55):
    return _ell(cx, cy, rx, ry, P["cheek"], 0, extra=f'opacity="{op}"')


# ====================================================================== 1. the great fish


def _fish(mouth=0.0, eye="open", tail=0.0, blush=True):
    m = _clamp(mouth)
    tl = _clamp(tail, -1, 1)
    H = (272.0, 42.0)
    lift, drop = -19.0 * m, 55.0 * m

    def up(p, w):
        return _rot(p[0], p[1], H[0], H[1], lift * w)

    def dn(p, w=1.0):
        return _rot(p[0], p[1], H[0], H[1], drop * w)

    lipU = [up((345, 48), .3), up((430, 53), .6), up((518, 43), .85), up((588, 16), 1)]
    U = lipU[-1]
    fore = [up((580, -62), .75), up((522, -160), .4), up((420, -244), .12), (268, -294), (80, -315)]
    back = [(-120, -297), (-300, -229), (-432, -133), (-506, -58)]
    belly = [(-514, 0), (-506, 58), (-432, 140), (-292, 232), (-110, 292), (60, 306)]
    T = (178, 297)
    body_line = [H] + lipU + fore + back + belly + [T]
    d_body_open = _sm(body_line, closed=False)
    d_body = d_body_open + " Z"

    lipL_rest = [(345, 42), (430, 47), (518, 37), (584, 13)]
    lipL = [dn(p) for p in lipL_rest]
    tipL = dn((596, 28))
    # the floor of the mouth stretches like a pouch: rest -> open targets (not a rigid rotation)
    pouch = [((590, 92), (452, 336)), ((550, 162), (404, 370)), ((470, 236), (336, 384)), ((372, 284), (264, 360)),
             ((265, 303), (210, 322))]
    chin = [_lerp2(a, b, m) for a, b in pouch]
    jaw_line = [H] + lipL + [tipL] + chin + [T]
    d_jaw_open = _sm(jaw_line, closed=False)
    d_jaw = d_jaw_open + " L205,175 L238,95 Z"

    body_col, dark, light, belly_col = P["fish"], P["fish_dark"], P["fish_light"], P["fish_belly"]
    fin_col = S.mix(body_col, light, 0.45)
    out = ""

    # ---- tail fin (behind body), bends around the peduncle
    tail_pts = [(-430, -58), (-560, -150), (-672, -270), (-760, -330), (-788, -268), (-752, -130),
                (-690, 0), (-752, 130), (-788, 268), (-760, 330), (-672, 270), (-560, 150), (-430, 58)]
    td = _sm(tail_pts, closed=False) + " L-400,0 Z"
    rays = ""
    for a in (-62, -44, -26, -9, 9, 26, 44, 62):
        ex, ey = -470 - 250 * math.cos(math.radians(a)), 285 * math.sin(math.radians(a))
        rays += _line(-500, ey * 0.12, ex, ey, sw=3.5, color=dark, extra='opacity="0.45"')
    out += _g(_p(td, fin_col, 0) + _clip(_uid("fisht", 0), td, rays) + _p(td, sw=4.5), f"rotate({22 * tl:.2f} -470 0)")

    # ---- dorsal and anal fins (behind body)
    dors = [(-235, -262), (-196, -372), (-80, -452), (55, -446), (150, -372), (196, -292), (110, -260)]
    out += _p(_sm(dors, closed=False) + " Z", fin_col, 4.5)
    for i in range(6):
        bx = -200 + i * 66
        out += _line(bx, -300, bx + 6 + i * 4, -400 + abs(i - 2.5) * 18, sw=3.5, color=dark,
                     extra='opacity="0.45"')
    anal = [(-170, 285), (-245, 342), (-330, 352), (-372, 300), (-300, 240)]
    out += _p(_sm(anal, closed=False) + " Z", fin_col, 4.5)

    # ---- inside of the mouth
    if m > 0.004:
        lu = [H] + lipU
        ll = [H] + lipL + [tipL]
        mid = _lerp2(U, tipL, 0.5)
        ctrl = _lerp2(mid, H, 0.36)
        d_in = (_poly(lu, closed=False) + f" Q{_f(ctrl[0])},{_f(ctrl[1])} {_f(tipL[0])},{_f(tipL[1])} "
                + " ".join(f"L{_f(px)},{_f(py)}" for px, py in reversed(ll[:-1])) + " Z")
        cid = _uid("fishm", m)
        inner = _p(d_in, P["mouth_inside"], 0)
        bis = _rot(H[0] + 120, H[1], H[0], H[1], (lift + drop) / 2)
        inner += _ell(bis[0] - 35, bis[1], 40 + 55 * m, 26 + 70 * m, S.shade(P["mouth_inside"], -0.45), 0,
                      extra='filter="url(#soft)"')
        tongue = [(330, 44), (360, 8), (430, -6), (505, 6), (545, 36)]
        tongue = [dn(p) for p in tongue]
        inner += _p(_sm(tongue, closed=False) + " Z", "#e48a8c", 3.5)
        tm1, tm2 = dn((375, 22)), dn((480, 18))
        inner += _p(f"M{_f(tm1[0])},{_f(tm1[1])} Q{_f((tm1[0] + tm2[0]) / 2)},{_f((tm1[1] + tm2[1]) / 2 + 8)} "
                    f"{_f(tm2[0])},{_f(tm2[1])}", sw=3, stroke=S.shade("#e48a8c", -0.3))
        out += _clip(cid, d_in, inner)
        out += _p(f"M{_f(U[0])},{_f(U[1])} Q{_f(ctrl[0])},{_f(ctrl[1])} {_f(tipL[0])},{_f(tipL[1])}", sw=3.5,
                  extra='opacity="0.8"')

    # ---- lower jaw
    jid = _uid("fishj", m)
    band = [H] + lipL + [tipL] + [dn((566, 74)), dn((470, 94)), dn((360, 88)), (290, 84)]
    jaw_detail = _p(_sm(band, closed=True), S.mix(body_col, light, 0.15), 0)
    out += _p(d_jaw, belly_col, 0) + _clip(jid, d_jaw, jaw_detail) + _p(d_jaw_open, sw=4.5)

    # ---- body with clipped shading
    bid = _uid("fishb", m)
    belly_shape = [(-540, 30), (-420, 110), (-260, 160), (-60, 185), (110, 172), (212, 122), (252, 80),
                   (278, 62), (330, 330), (-560, 330)]
    shade = _p(_sm(belly_shape, closed=True), belly_col, 0)
    shade += _p(_sm([(140, 168), (-60, 186), (-260, 162), (-420, 112)], closed=False), sw=3.5,
                stroke=S.shade(belly_col, -0.15), extra='opacity="0.7"')
    back_shape = [(-540, -40), (-330, -170), (-80, -238), (200, -236), (420, -190), (520, -130), (520, -420),
                  (-540, -420)]
    shade += _p(_sm(back_shape, closed=True), dark, 0, extra='filter="url(#soft)" opacity="0.75"')
    shade += _ell(40, -150, 230, 38, light, 0, extra='filter="url(#soft)" opacity="0.38" transform="rotate(-6 40 -150)"')
    # scale arcs
    for row, yy in enumerate((-175, -100, -25, 50)):
        for k in range(8):
            xx = -400 + k * 66 + (33 if row % 2 else 0)
            if xx > 130 - abs(yy) * 0.15:
                continue
            op = 0.32 if yy < 40 else 0.22
            shade += _p(f"M{_f(xx)},{_f(yy - 30)} Q{_f(xx - 34)},{_f(yy)} {_f(xx)},{_f(yy + 30)}", sw=3.5,
                        stroke=dark, extra=f'opacity="{op}"')
    for sx, sy, sr in ((-60, -232, 22), (40, -262, 15), (-185, -205, 18), (125, -222, 13), (-300, -150, 14),
                       (-105, -165, 11), (225, -250, 12), (-385, -92, 10), (-235, -118, 9), (300, -205, 9)):
        shade += _circ(sx, sy, sr, P["fish_spot"], 0, extra='opacity="0.95"')
    out += _p(d_body, body_col, 0) + _clip(bid, d_body, shade) + _p(d_body_open, sw=4.5)

    # ---- gill, pectoral fin
    out += _p("M236,-205 Q160,-30 222,168", sw=4.5)
    out += _p("M205,-150 Q150,-30 196,110", sw=3, stroke=dark, extra='opacity="0.4"')
    pb = (182, 104)
    fan = [(196, 70), (120, 60), (40, 92), (6, 140), (24, 176), (70, 182), (120, 160), (176, 136)]
    fan_rays = ""
    for e in ((45, 98), (25, 140), (55, 172), (110, 160)):
        fan_rays += _line(170, 104, e[0] + 10, e[1] - 4, sw=3, color=dark, extra='opacity="0.5"')
    out += _g(_p(_sm(fan, closed=True), fin_col, 4.5) + fan_rays, f"rotate({-10 * tl:.2f} {pb[0]} {pb[1]})")

    # ---- face
    ec = up((385, -110), 0.32)
    if eye == "surprised":
        out += _p(f"M{_f(ec[0] - 60)},{_f(ec[1] - 112)} Q{_f(ec[0])},{_f(ec[1] - 150)} {_f(ec[0] + 58)},{_f(ec[1] - 108)}",
                  sw=5)
    out += _eye(ec[0], ec[1], 64, eye, look=(0.55, 0.1), sw=4.5)
    if blush:
        out += _blush(ec[0] + 30, ec[1] + 100, 48, 24, 0.8)
    if m < 0.5:
        a = 1 - m * 2
        out += _p(f"M{_f(H[0] + 8)},{_f(H[1] - 20)} Q{_f(H[0] - 14)},{_f(H[1] - 2)} {_f(H[0] + 4)},{_f(H[1] + 14)}",
                  sw=4.5, extra=f'opacity="{a:.2f}"')
    return out


def fish(x, y, scale=1.0, facing=1, mouth=0.0, eye="open", tail=0.0, blush=True):
    return _place(_fish(mouth, eye, tail, blush), x, y, scale, facing)


# ====================================================================== 2. the ship


def _hull_top(x):
    return -165 - 75 * (abs(x) / 480) ** 3.2


def _hull_bot(x):
    return 96 - 250 * (abs(x) / 490) ** 3.5


def _sail_pt(u, v, kind):
    """Point on the square sail surface (u: 0 stern edge .. 1 bow edge, v: 0 yard .. 1 foot)."""
    if kind == "torn":
        xl = -300 - 18 * math.sin(math.pi * v)
        xr = 280 + 22 * math.sin(math.pi * v)
        yb = -585 + 30 * math.sin(math.pi * u)
    else:
        xl = -300 - 30 * math.sin(math.pi * v)
        xr = 280 + 52 * math.sin(math.pi * v) ** 0.8
        yb = -548 + 46 * math.sin(math.pi * u)
    return (_lerp(xl, xr, u), _lerp(-842, yb, v))


def _sail(kind, sid):
    out = ""
    yard = "M-318,-848 Q-10,-866 298,-848"
    if kind == "furled":
        pts = []
        for i in range(13):
            u = i / 12
            pts.append((_lerp(-292, 272, u), -840 + 46 + 12 * math.sin(i * 1.9) - 10 * (u * (1 - u) < 0.03)))
        roll = [(-300, -846), (272, -846)] + list(reversed(pts))
        out += _p(_sm([(-296, -846)] + [(p[0], p[1] - 2) for p in pts[1:-1]] + [(276, -846)], closed=True),
                  P["sail"], 4)
        for i in range(1, 12, 2):
            u = i / 12
            xx = _lerp(-292, 272, u)
            out += _p(f"M{_f(xx - 14)},{_f(-842)} Q{_f(xx)},{_f(-822)} {_f(xx + 12)},{_f(-842)}", sw=2.5,
                      stroke=S.shade(P["sail"], -0.35))
        for xx in (-210, -60, 90, 220):
            out += _rect(xx - 7, -852, 14, 46, P["wood_light"], 3, rx=5)
        del roll
        out = _tube(yard, 14, P["wood"]) + out
        return out
    # surface outline
    n = 14
    left = [_sail_pt(0, i / n, kind) for i in range(n + 1)]
    bottom = [_sail_pt(i / n, 1, kind) for i in range(n + 1)]
    right = [_sail_pt(1, 1 - i / n, kind) for i in range(n + 1)]
    top = [_sail_pt(1 - i / n, 0, kind) for i in range(n + 1)]
    if kind == "torn":
        rng = random.Random(4)
        tb = [0, 26, -8, 38, 4, 18, -14, 44, 10, 30, -6, 52, 0, 22, 0]
        bottom = [(px + rng.uniform(-8, 8), py + tb[i]) for i, (px, py) in enumerate(bottom)]
        tr_ = [0, -40, 6, -18, 16, -52, 0, -10, 14, -34, -4, -22, 8, 0, 0]
        right = [(px + tr_[i], py) for i, (px, py) in enumerate(right)]
        outline = _poly(left[:-1] + bottom + right[1:] + top[1:-1])
    else:
        outline = _sm(left[:-1] + bottom + right[1:] + top[1:-1], closed=True, tension=0.6)
    hole = ""
    if kind == "torn":
        hc = _sail_pt(0.62, 0.48, kind)
        hp = [(hc[0] - 50, hc[1] - 6), (hc[0] - 22, hc[1] - 30), (hc[0] - 4, hc[1] - 12), (hc[0] + 30, hc[1] - 40),
              (hc[0] + 40, hc[1] - 8), (hc[0] + 22, hc[1] + 4), (hc[0] + 30, hc[1] + 30), (hc[0] - 2, hc[1] + 22),
              (hc[0] - 30, hc[1] + 34)]
        hole = " " + _poly(hp)
    stripes = ""
    for u0, u1 in ((1 / 7, 2 / 7), (3 / 7, 4 / 7), (5 / 7, 6 / 7)):
        a = [_sail_pt(u0, i / n, kind) for i in range(n + 1)]
        b = [_sail_pt(u1, 1 - i / n, kind) for i in range(n + 1)]
        a[-1] = (a[-1][0], a[-1][1] + 60)
        b[0] = (b[0][0], b[0][1] + 60)
        stripes += _p(_poly(a + b), P["sail_stripe"], 0)
    shade = _p(_poly([_sail_pt(0, i / n, kind) for i in range(n + 1)] +
                     [_sail_pt(0.28, 1 - i / n, kind) for i in range(n + 1)]),
               S.shade(P["sail"], -0.25), 0, extra='filter="url(#soft)" opacity="0.55"')
    shade += _p(_poly([_sail_pt(0.62, i / n, kind) for i in range(n + 1)] +
                      [_sail_pt(0.9, 1 - i / n, kind) for i in range(n + 1)]),
                HILITE, 0, extra='filter="url(#soft)" opacity="0.2"')
    seams = ""
    for v in (0.33, 0.66):
        pts = [_sail_pt(i / n, v, kind) for i in range(n + 1)]
        seams += _p(_sm(pts, closed=False), sw=2.5, stroke=S.shade(P["sail"], -0.4), extra='opacity="0.6"')
    body = _p(outline + hole, P["sail"], 0, extra='fill-rule="evenodd"')
    inner = stripes + shade + seams
    out += body + f'<clipPath id="{sid}"><path d="{outline + hole}" clip-rule="evenodd"/></clipPath>'
    out += f'<g clip-path="url(#{sid})">{inner}</g>'
    out += _p(outline + hole, sw=4.5, extra='fill-rule="evenodd"')
    if kind == "torn":
        bc = _sail_pt(0.93, 0.93, kind)
        flap = [(bc[0] - 60, bc[1] - 10), (bc[0] - 10, bc[1] - 30), (bc[0] + 60, bc[1] - 6), (bc[0] + 120, bc[1] + 20),
                (bc[0] + 150, bc[1] + 8), (bc[0] + 128, bc[1] + 46), (bc[0] + 92, bc[1] + 40), (bc[0] + 70, bc[1] + 64),
                (bc[0] + 30, bc[1] + 42), (bc[0] - 30, bc[1] + 40)]
        out += _p(_poly(flap), S.shade(P["sail"], -0.1), 4)
        out += _p(_poly([(bc[0] + 4, bc[1] - 22), (bc[0] + 44, bc[1] - 10), (bc[0] + 38, bc[1] + 44), (bc[0] + 4, bc[1] + 42)]),
                  P["sail_stripe"], 0, extra='opacity="0.9"')
    out = _tube(yard, 14, P["wood"]) + out
    for xx in (-200, -60, 80, 210):
        tp = _sail_pt((xx + 300) / 580, 0, kind)
        out += _circ(tp[0], tp[1] + 2, 6, P["wood_light"], 3)
    return out


def _amphora(rot=0.0, col=None, s=1.0):
    col = col or P["terracotta"]
    body = [(0, -70), (22, -64), (38, -40), (40, -5), (30, 34), (12, 62), (0, 74), (-12, 62), (-30, 34), (-40, -5),
            (-38, -40), (-22, -64)]
    out = _p("M-13,-66 Q-36,-62 -32,-36", sw=11, stroke=INK) + _p("M-13,-66 Q-36,-62 -32,-36", sw=5, stroke=col)
    out += _p("M13,-66 Q36,-62 32,-36", sw=11, stroke=INK) + _p("M13,-66 Q36,-62 32,-36", sw=5, stroke=col)
    out += _p(_sm(body, closed=True), col, 4)
    out += _rect(-15, -84, 30, 20, col, 4, rx=4)
    out += _ell(0, -84, 17, 5, S.shade(col, -0.3), 3)
    out += _p("M-37,-18 Q0,-8 37,-18", sw=7, stroke=CREAM, extra='opacity="0.85"')
    out += _p("M-39,4 Q-26,10 -13,4 Q0,-2 13,4 Q26,10 39,4", sw=3, stroke=S.shade(col, -0.35))
    out += _ell(-16, -30, 7, 18, HILITE, 0, extra='opacity="0.35"')
    return _g(out, f"rotate({rot:.1f}) scale({s})")


def _sack(s=1.0, col=None, seed=0):
    col = col or P["sackcloth"]
    r = random.Random(seed)
    j = lambda v: v + r.uniform(-4, 4)  # noqa: E731
    pts = [(j(-24), -84), (j(-44), -64), (j(-54), -30), (j(-50), -4), (0, 2), (j(50), -4), (j(54), -30), (j(44), -64),
           (j(24), -84)]
    out = _p(_sm(pts, closed=False) + " L14,-90 L-14,-90 Z", col, 4)
    out += _p("M-26,-94 Q-34,-118 -16,-114 Q-6,-126 2,-112 Q14,-124 22,-110 Q36,-114 26,-94 Z", col, 4)
    out += _p("M-24,-90 Q0,-82 24,-90", sw=7, stroke=P["wood_light"]) + _p("M-24,-90 Q0,-82 24,-90", sw=2.5)
    for k in range(-2, 3):
        out += _p(f"M{k * 18},-70 Q{k * 20 + 3},-40 {k * 19},-8", sw=2.5, stroke=S.shade(col, -0.25),
                  extra='opacity="0.5"')
    out += _ell(14, -40, 13, 11, S.shade(col, 0.25), 2.5, extra='opacity="0.9"')
    return _g(out, f"scale({s})")


def _crate(s=1.0):
    out = _p("M-50,-40 L-34,-56 L66,-56 L50,-40 Z", P["wood_light"], 4)
    out += _p("M50,-40 L66,-56 L66,30 L50,46 Z", P["wood_dark"], 4)
    out += _rect(-50, -40, 100, 86, P["wood"], 4, rx=3)
    for yy in (-12, 17):
        out += _line(-46, yy, 46, yy, sw=3, color=P["wood_dark"])
    out += _rect(-50, -40, 100, 86, "none", 4, rx=3)
    out += _p("M-42,38 L42,-32", sw=13, stroke=INK) + _p("M-42,38 L42,-32", sw=6, stroke=P["wood_light"])
    for cx, cy in ((-42, -32), (42, -32), (-42, 38), (42, 38)):
        out += _circ(cx, cy, 3, INK, 0)
    return _g(out, f"scale({s})")


def _lantern_body(lit=True, glow=True, gid="lg"):
    """Hanging lantern, hook at (0,0), about 54 x 132."""
    out = ""
    if lit and glow:
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.85), (0.4, P["gold"], 0.35), (1, P["gold"], 0)])}</defs>'
                f'<circle cx="0" cy="88" r="120" fill="url(#{gid})"/>')
    out += _circ(0, 8, 8, "none", 3.5)
    out += _line(0, 16, 0, 34, sw=3.5)
    out += _p("M-24,52 Q-24,32 0,30 Q24,32 24,52 Z", P["wood_dark"], 4)
    win = P["glow"] if lit else S.mix(P["sand"], P["ink"], 0.3)
    out += _rect(-22, 52, 44, 60, win, 4, rx=6)
    if lit:
        out += _ell(0, 90, 9, 14, P["sun_hot"], 0) + _ell(0, 93, 5, 8, P["glow"], 0)
    out += _line(-8, 54, -8, 110, sw=3, color=P["wood_dark"]) + _line(8, 54, 8, 110, sw=3, color=P["wood_dark"])
    out += _rect(-27, 110, 54, 12, P["wood_dark"], 4, rx=4)
    out += _p("M-12,122 L0,134 L12,122", P["wood_dark"], 3.5)
    return out


def _rope_coil(s=1.0, col=None):
    col = col or S.mix(P["sackcloth"], P["sand"], 0.4)
    dark = S.shade(col, -0.35)
    out = ""
    for i, (ry, rx, cy) in enumerate(((15, 56, -15), (15, 50, -33), (14, 42, -49))):
        out += _ell(0, cy, rx, ry, col, 4)
        out += _ell(0, cy - 3, rx - 13, ry - 7, S.shade(col, -0.15), 3)
        for k in range(9):
            a = math.pi * (0.1 + 0.8 * k / 8)
            px, py = rx * math.cos(a), cy + ry * math.sin(a)
            out += _line(px - 4, py - 6, px + 4, py + 4, sw=2.5, color=dark, extra='opacity="0.7"')
    out += _p("M30,-52 Q58,-64 62,-40 Q66,-14 84,-6", sw=13, stroke=INK) + _p("M30,-52 Q58,-64 62,-40 Q66,-14 84,-6",
                                                                             sw=6, stroke=col)
    return _g(out, f"scale({s})")


def _ship(sail="full", cutaway=False, lantern=True, oars=False, part="all", flag=True):
    back, front = "", ""
    wood, wd, wl = P["wood"], P["wood_dark"], P["wood_light"]
    # ---- rigging behind the sail
    mast_top = (-10, -930)
    stay_c = S.shade(INK, 0.15)
    back += _line(mast_top[0], mast_top[1] + 10, 505, -352, sw=3, color=stay_c)
    back += _line(mast_top[0], mast_top[1] + 10, -478, -420, sw=3, color=stay_c)
    # pennant
    if flag:
        fl = "M-10,-922 Q30,-948 70,-930 Q100,-918 128,-934 Q104,-906 72,-912 Q36,-918 -10,-900 Z"
        back += _p(fl, P["sail_stripe"], 4)
    back += _tube("M-10,-170 L-10,-930", 18, wood)
    back += _ell(-10, -930, 18, 9, wd, 4)
    tilt = -6 if sail == "torn" else 0
    sid = _uid("sail", sail)
    back += _g(_sail(sail, sid), f"rotate({tilt} -10 -850)")
    # sheets
    if sail != "furled":
        bl, br = _sail_pt(0, 1, sail), _sail_pt(1, 1, sail)
        if sail == "torn":
            bl = _rot(bl[0], bl[1], -10, -850, tilt)
            br = _rot(br[0], br[1], -10, -850, tilt)
        back += _line(bl[0], bl[1], -360, -200, sw=3, color=stay_c)
        back += _line(br[0], br[1], 380, -205, sw=3, color=stay_c)
    # ---- hull
    xs = [-480 + i * 20 for i in range(49)]
    top = [(x, _hull_top(x)) for x in xs]
    hull_pts = top + [(503, -196), (494, -136), (466, -72), (418, -14), (340, 40), (200, 80), (0, 96), (-200, 82),
                      (-350, 42), (-430, -14), (-478, -80), (-500, -146), (-505, -204)]
    hull_d = _poly(top) + " " + _sm(hull_pts[len(top) - 1:] + [top[0]], closed=False)[0:]
    hull_d = _sm(hull_pts, closed=True, tension=0.5)
    hid = _uid("hull", 1)
    hull_in = _rect(-520, -10, 1040, 140, S.mix(wd, P["sea_deep"], 0.15), 0)
    hull_in += _p(_poly([(x, _hull_top(x) + 2) for x in xs] + [(x, _hull_top(x) + 32) for x in reversed(xs)]),
                  wl, 0)
    hull_in += _p(_poly([(x, _hull_top(x) + 44) for x in xs] + [(x, _hull_top(x) + 64) for x in reversed(xs)]),
                  P["jonah_sash"], 0)
    tri = ""
    for x in range(-440, 460, 44):
        yy = _hull_top(x) + 44
        tri += _poly([(x - 12, yy), (x + 12, yy), (x, yy + 18)]) + " "
    hull_in += _p(tri, P["sail_stripe"], 0)
    for t in (0.26, 0.44, 0.62, 0.8):
        pts = [(x, _lerp(_hull_top(x) + 64, _hull_bot(x), t)) for x in xs]
        hull_in += _p(_sm(pts, closed=False), sw=3, stroke=wd, extra='opacity="0.75"')
    hull_in += _p(_sm([(x, _hull_top(x) + 32) for x in xs], closed=False), sw=3, stroke=wd)
    hull_in += _p(_sm([(x, _hull_top(x) + 64) for x in xs], closed=False), sw=3, stroke=S.shade(P["jonah_sash"], -0.4))
    rng = random.Random(3)
    for _ in range(26):
        x = rng.uniform(-430, 430)
        t = rng.choice((0.35, 0.53, 0.71))
        y0 = _lerp(_hull_top(x) + 64, _hull_bot(x), t)
        hull_in += _circ(x, y0, 2.6, wd, 0, extra='opacity="0.8"')
    hull_in += _ell(-60, -60, 360, 30, HILITE, 0, extra='filter="url(#soft)" opacity="0.18"')
    hull = _p(hull_d, wood, 0) + _clip(hid, hull_d, hull_in) + _p(hull_d, sw=4.5)
    # posts
    bow = "M474,-222 Q500,-262 508,-306 Q512,-340 490,-356"
    stern = ("M-474,-222 Q-504,-268 -512,-330 Q-520,-392 -478,-420 Q-436,-438 -418,-400 Q-404,-366 -436,-356 "
             "Q-462,-350 -458,-376")
    posts = _tube(bow, 22, wood) + _circ(488, -358, 14, wl, 4)
    posts += _tube(stern, 24, wood)
    posts += _p("M-498,-300 Q-500,-370 -470,-404", sw=4, stroke=wl, extra='opacity="0.8"')
    if cutaway:
        back += hull + _ship_interior(lantern) + posts
    else:
        back += hull + posts
    # ---- rail and shields (in front of standing people)
    rail = ""
    for x in range(-400, 440, 40):
        yt = _hull_top(x)
        rail += _line(x, yt, x, yt - 52, sw=5, color=INK) + _line(x, yt, x, yt - 52, sw=2, color=wl)
    rail += _tube(_sm([(x, _hull_top(x) - 54) for x in range(-410, 450, 40)], closed=False), 8, wl, 3.5)
    cols = (P["terracotta"], P["sail"], P["jonah_sash"], P["gold"])
    for i, x in enumerate(range(-330, 360, 66)):
        cy = _hull_top(x) - 30
        c = cols[i % 4]
        rail += _circ(x, cy, 27, c, 4)
        rail += _circ(x, cy, 17, "none", 2.5, stroke=S.shade(c, -0.3))
        rail += _circ(x, cy, 6, S.shade(c, -0.25), 3)
    front += rail
    # steering oar (stern, near side)
    so = "M-372,-262 L-548,72"
    front += _tube(so, 13, wl)
    front += _p("M-520,10 Q-530,-12 -548,-6 L-600,106 Q-590,128 -566,122 Z", wl, 4)
    front += _rect(-394, -284, 52, 16, wd, 4, rx=6, extra="transform='rotate(-25 -372 -276)'")
    if oars:
        for x in range(-280, 320, 85):
            y0 = _hull_top(x) + 64
            d = f"M{x},{y0} L{x - 110},{y0 + 210}"
            front += _circ(x, y0, 9, wd, 3.5)
            front += _tube(d, 9, wl, 3.5)
            front += _p(f"M{x - 96},{y0 + 176} L{x - 132},{y0 + 250} Q{x - 124},{y0 + 262} {x - 110},{y0 + 254} "
                        f"L{x - 88},{y0 + 182} Z", wl, 3.5)
    if lantern and not cutaway:
        front += _g(_lantern_body(True, True, _uid("shiplan", 0)), "translate(-428,-372) scale(0.85)")
    elif lantern and cutaway:
        front += _g(_lantern_body(True, False, _uid("shiplan", 1)), "translate(-428,-372) scale(0.85)")
    if part == "back":
        return back
    if part == "front":
        return front
    return back + front


def _ship_interior(lantern=True):
    x0, y0, x1, y1 = SHIP_INTERIOR
    wd, wood, wl = P["wood_dark"], P["wood"], P["wood_light"]
    pts = [(x0, y0), (x1, y0), (x1, -4), (x1 - 28, 30), (x1 - 90, y1), (x0 + 90, y1), (x0 + 28, 30), (x0, -4)]
    d = _poly(pts)
    d = (f"M{x0},{y0} L{x1},{y0} L{x1},-20 Q{x1 - 8},{y1} {x1 - 110},{y1} L{x0 + 110},{y1} "
         f"Q{x0 + 8},{y1} {x0},-20 Z")
    wall = S.mix(wd, wood, 0.25)
    inner = _rect(x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20, wall, 0)
    for yy in range(y0 + 26, y1, 28):
        inner += _line(x0, yy, x1, yy, sw=3, color=S.shade(wd, -0.25), extra='opacity="0.6"')
    for xx in range(x0 + 60, x1, 120):
        inner += _p(f"M{xx - 10},{y0} Q{xx + 8},{(y0 + y1) / 2} {xx - 6},{y1}", sw=20, stroke=INK)
        inner += _p(f"M{xx - 10},{y0} Q{xx + 8},{(y0 + y1) / 2} {xx - 6},{y1}", sw=13, stroke=S.mix(wood, wd, 0.3))
    # deck beams
    inner += _rect(x0 - 10, y0 - 4, x1 - x0 + 20, 20, S.shade(wd, -0.15), 0)
    for xx in range(x0 + 30, x1, 90):
        inner += _rect(xx - 10, y0 + 6, 20, 16, wood, 3, rx=2)
    # floor
    inner += _rect(x0, y1 - 16, x1 - x0, 30, wl, 3.5)
    for xx in range(x0 + 40, x1, 70):
        inner += _line(xx, y1 - 14, xx - 6, y1 + 10, sw=2.5, color=wd, extra='opacity="0.6"')
    # warm glow
    gid = _uid("holdglow", 0)
    inner += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.8), (0.5, P["gold"], 0.3), (1, P["gold"], 0)])}</defs>'
              f'<ellipse cx="-160" cy="-60" rx="380" ry="210" fill="url(#{gid})"/>')
    # bed: straw mat, folded blanket, pillow
    bx0, bx1, by = SHIP_BED
    inner += _rect(bx0 - 6, by + 12, bx1 - bx0 + 12, y1 - 16 - by - 12, P["wood"], 3.5, rx=3)
    inner += _p(f"M{bx0},{by + 14} Q{bx0 - 4},{by} {bx0 + 14},{by - 2} L{bx1 - 14},{by - 2} Q{bx1 + 4},{by} {bx1},{by + 14} Z",
                S.mix(P["sackcloth"], P["sand"], 0.5), 3.5)
    for xx in range(bx0 + 20, bx1, 26):
        inner += _line(xx, by + 1, xx - 2, by + 12, sw=2, color=P["sackcloth_dark"], extra='opacity="0.6"')
    inner += _p(f"M{bx0 + 6},{by + 2} Q{bx0 - 4},{by - 30} {bx0 + 30},{by - 34} Q{bx0 + 70},{by - 38} "
                f"{bx0 + 76},{by - 12} Q{bx0 + 76},{by + 4} {bx0 + 50},{by + 4} Z", P["headcloth"], 3.5)
    inner += _p(f"M{bx1 - 70},{by + 2} Q{bx1 - 78},{by - 24} {bx1 - 50},{by - 26} L{bx1 - 6},{by - 22} "
                f"Q{bx1 + 6},{by - 8} {bx1 - 4},{by + 2} Z", P["jonah_sash"], 3.5)
    inner += _line(bx1 - 62, by - 14, bx1 - 10, by - 12, sw=2.5, color=S.shade(P["jonah_sash"], -0.4))
    # cargo
    fl = y1 - 16
    inner += _g(_amphora(-8), f"translate(-318,{fl - 64}) scale(0.9)")
    inner += _g(_amphora(6, S.mix(P["terracotta"], P["sand"], 0.35)), f"translate(-254,{fl - 64}) scale(0.85)")
    inner += _g(_sack(0.8, seed=2), f"translate(-190,{fl})")
    inner += _g(_crate(0.85), f"translate(300,{fl - 39})")
    inner += _g(_sack(0.72, seed=5), f"translate(296,{fl - 74})")
    if lantern:
        inner += _line(-160, y0 + 14, -160, y0 + 30, sw=3)
        inner += _g(_lantern_body(True, False), f"translate(-160,{y0 + 26}) scale(0.8)")
    cid = _uid("hold", 0)
    out = _clip(cid, d, inner)
    out += _p(d, sw=22) + _p(d, sw=12, stroke=wl)
    out += _p(d, sw=3, stroke=S.shade(wl, 0.3), extra='opacity="0.0"')
    return out


def ship(x, y, scale=1.0, facing=1, sail="full", cutaway=False, lantern=True, oars=False, part="all", flag=True):
    return _place(_ship(sail, cutaway, lantern, oars, part, flag), x, y, scale, facing)
