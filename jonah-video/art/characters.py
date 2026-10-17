"""People library (docstring is regenerated below the code; see __doc__ at the end)."""
import hashlib
import math

from art.style import INK, P, fmt, mix, shade, smooth_path

# ======================================================================= constants
OW = 4.0                  # silhouette outline width (px at scale 1)
LW = 3.0                  # inner detail line width (faces, folds)
EYE = "#3a271b"           # pupils: deep umber, never black
HI = "#fffaf0"            # highlights: warm off-white, never pure white
SANDAL = "#8b5a35"
SANDAL_DARK = "#6b4127"
TONGUE = "#e08479"
GOLD = P["crown"]
GOLD_DARK = shade(P["crown"], -0.32)
DRIP = P["sea_light"]

# ======================================================================= vectors


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _mul(a, k):
    return (a[0] * k, a[1] * k)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _len(a):
    return math.hypot(a[0], a[1])


def _nrm(a):
    n = _len(a) or 1.0
    return (a[0] / n, a[1] / n)


def _rot(a, deg):
    """Rotate a vector; positive degrees turn clockwise on screen (y points down)."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (a[0] * c - a[1] * s, a[0] * s + a[1] * c)


def _dv(deg):
    """Limb angle -> unit direction. 0 = hanging down, 90 = forward, 180 = up, -90 = backward."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


def _ang(v):
    """Screen angle of a vector in degrees (0 = +x, 90 = down) for SVG rotate()."""
    return math.degrees(math.atan2(v[1], v[0]))


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _pt(p):
    return f"{fmt(p[0])},{fmt(p[1])}"


# ======================================================================= polygons


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _rounded(pts, r, k=5):
    """Convex polygon -> densely sampled polygon with rounded corners (stays convex)."""
    n = len(pts)
    out = []
    for i in range(n):
        a, v, b = pts[i - 1], pts[i], pts[(i + 1) % n]
        la, lb = _len(_sub(a, v)), _len(_sub(b, v))
        p1 = _lerp(v, a, min(r / la, 0.5) if la else 0)
        p2 = _lerp(v, b, min(r / lb, 0.5) if lb else 0)
        for j in range(k + 1):
            t = j / k
            q = _add(_add(_mul(p1, (1 - t) ** 2), _mul(v, 2 * t * (1 - t))), _mul(p2, t * t))
            out.append(q)
    return out


def _clip(poly, p0, n):
    """Keep the part of a convex polygon where (p - p0) . n >= 0 (Sutherland-Hodgman)."""
    out = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n), _dot(_sub(b, p0), n)
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            t = da / (da - db)
            out.append(_lerp(a, b, t))
    return out


def _band(poly, p0, n, d0, d1):
    """Part of a convex polygon between the lines (p - p0) . n = d0 and = d1."""
    c = _clip(poly, _add(p0, _mul(n, d0)), n)
    return _clip(c, _add(p0, _mul(n, d1)), _mul(n, -1)) if c else []


def _d(pts, closed=True):
    if not pts:
        return ""
    return "M" + " L".join(_pt(p) for p in pts) + (" Z" if closed else "")


# ======================================================================= svg helpers


def _st(w=OW, col=INK):
    return f'stroke="{col}" stroke-width="{fmt(w)}" stroke-linejoin="round" stroke-linecap="round"'


def _tube(pts, w, col, ow=OW):
    """Outlined round-capped tube along a polyline (limbs, sleeves, ropes)."""
    d = _d(pts, closed=False)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{fmt(w + 2 * ow)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{fmt(w)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _union(polys, fill, ow=OW):
    """Several overlapping shapes drawn with one outer ink outline (no inner seams)."""
    ds = [_d(p) for p in polys if p]
    return ("".join(f'<path d="{d}" fill="{fill}" {_st(2 * ow)}/>' for d in ds) +
            "".join(f'<path d="{d}" fill="{fill}"/>' for d in ds))


def _poly(pts, fill, sw=LW, extra=""):
    if not pts or len(pts) < 3:
        return ""
    st = _st(sw) if sw else ""
    return f'<path d="{_d(pts)}" fill="{fill}" {st} {extra}/>'


def _clip_id(*parts):
    return "cp" + hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


def _ell(cx, cy, rx, ry, fill, sw=None, extra=""):
    st = _st(sw) if sw else ""
    return f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="{fill}" {st} {extra}/>'


def _line(d, w=LW, col=INK, extra=""):
    return f'<path d="{d}" fill="none" {_st(w, col)} {extra}/>'


def _drop(x, y, s, fill=DRIP):
    """Small water drop (tip up)."""
    return (f'<path d="M{fmt(x)},{fmt(y - 1.7 * s)} Q{fmt(x + 1.15 * s)},{fmt(y + 0.1 * s)} {fmt(x)},{fmt(y + s)} '
            f'Q{fmt(x - 1.15 * s)},{fmt(y + 0.1 * s)} {fmt(x)},{fmt(y - 1.7 * s)} Z" fill="{fill}" {_st(2.2)}/>')


# ======================================================================= metrics

_ADULT = dict(R=44, T=100, neck=46, ua=50, fa=46, th=60, sh=58, aw=22, lw=17, hr=11, fl=30,
              sw=25, hw=13, ww=31, shw=37, flare=22, sdrop=14, seat=20, ank=12)
_CHILD = dict(R=40, T=62, neck=40, ua=33, fa=30, th=38, sh=36, aw=17, lw=14, hr=9.5, fl=22,
              sw=19, hw=10, ww=24, shw=28, flare=12, sdrop=10, seat=15, ank=10)


def _metrics(base, k=1.0, wide=1.0, **over):
    m = {key: v * k for key, v in base.items()}
    for key in ("sw", "ww", "shw", "hw"):
        m[key] *= wide
    m.update(over)
    return m


# ======================================================================= expressions

EXPRS = {
    #            eyes      brow (inner, outer, lift)   mouth          extras
    "neutral":   dict(eyes="dot", brow=(0.0, 0.0, 0.0), mouth="smile"),
    "happy":     dict(eyes="dot", brow=(-0.03, 0.02, -0.06), mouth="grin"),
    "sad":       dict(eyes="dot", brow=(-0.10, 0.05, 0.0), mouth="frown", look=(0, 0.05)),
    "scared":    dict(eyes="big", brow=(-0.11, 0.03, -0.08), mouth="scared", sweat=True),
    "angry":     dict(eyes="dot", brow=(0.11, -0.05, 0.03), mouth="grumpy"),
    "surprised": dict(eyes="big", brow=(-0.03, -0.03, -0.12), mouth="o"),
    "sleepy":    dict(eyes="closed", brow=(0.0, 0.02, 0.04), mouth="small_o"),
    "peaceful":  dict(eyes="closed", brow=(-0.03, 0.02, 0.0), mouth="smile"),
    "dizzy":     dict(eyes="spiral", brow=(-0.07, 0.03, -0.04), mouth="wave"),
    "shout":     dict(eyes="dot", brow=(0.07, -0.04, -0.03), mouth="shout"),
    "sorry":     dict(eyes="down", brow=(-0.10, 0.05, 0.03), mouth="wobble", blush=True),
    "worried":   dict(eyes="dot", brow=(-0.09, 0.04, -0.02), mouth="flat"),
    "tired":     dict(eyes="lid", brow=(-0.06, 0.04, 0.04), mouth="small_open", sweat=True),
}
EXPRESSIONS = tuple(EXPRS)


def _face(R, skin, expr, look=(0, 0), brow_col=INK):
    """Eyes, brows, nose, cheeks, mouth in head-frame coordinates (3/4 view facing +x)."""
    E = EXPRS.get(expr, EXPRS["neutral"])
    lx = look[0] + E.get("look", (0, 0))[0]
    ly = look[1] + E.get("look", (0, 0))[1]
    s = ""
    ck = mix(skin, P["cheek"], 0.8)
    big = 1.35 if E.get("blush") else 1.0
    s += _ell(-0.30 * R, 0.36 * R, 0.16 * R * big, 0.10 * R * big, ck, extra='opacity="0.85"')
    s += _ell(0.67 * R, 0.38 * R, 0.12 * R * big, 0.09 * R * big, ck, extra='opacity="0.85"')
    eyes = [(-0.10 * R, 0.04 * R), (0.40 * R, 0.04 * R)]
    kind = E["eyes"]
    for ex, ey in eyes:
        if kind in ("dot", "big", "down"):
            k = 1.2 if kind == "big" else (0.9 if kind == "down" else 1.0)
            cx, cy = ex + lx * R, ey + ly * R + (0.07 * R if kind == "down" else 0)
            rx, ry = 0.118 * R * k, 0.15 * R * k
            s += _ell(cx, cy, rx, ry, EYE)
            s += f'<circle cx="{fmt(cx - 0.35 * rx)}" cy="{fmt(cy - 0.38 * ry)}" r="{fmt(0.36 * rx)}" fill="{HI}"/>'
            if kind == "down":
                s += _line(f"M{fmt(cx - 1.5 * rx)},{fmt(cy - 0.6 * ry)} Q{fmt(cx)},{fmt(cy - 1.3 * ry)} "
                           f"{fmt(cx + 1.5 * rx)},{fmt(cy - 0.6 * ry)}", w=2.6)
        elif kind == "lid":
            cx, cy = ex + lx * R, ey + ly * R + 0.02 * R
            rx, ry = 0.118 * R, 0.15 * R
            s += (f'<path d="M{fmt(cx - rx)},{fmt(cy - 0.1 * ry)} A{fmt(rx)},{fmt(ry)} 0 0 0 {fmt(cx + rx)},'
                  f'{fmt(cy - 0.1 * ry)} Z" fill="{EYE}"/>')
            s += _line(f"M{fmt(cx - 1.45 * rx)},{fmt(cy - 0.05 * ry)} L{fmt(cx + 1.45 * rx)},{fmt(cy - 0.2 * ry)}",
                       w=3.0)
        elif kind == "closed":
            s += _line(f"M{fmt(ex - 0.13 * R)},{fmt(ey)} Q{fmt(ex)},{fmt(ey + 0.12 * R)} {fmt(ex + 0.13 * R)},{fmt(ey)}",
                       w=3.4)
        elif kind == "spiral":
            pts = []
            for i in range(22):
                a = i * 0.62
                rr = 0.02 * R + 0.0058 * R * i
                pts.append((ex + rr * math.cos(a), ey + rr * math.sin(a)))
            s += _line(smooth_path(pts, closed=False), w=2.4)
    bi, bo, bl = E["brow"]
    for i, (ex, ey) in enumerate(eyes):
        if i == 0:
            xo, xi = ex - 0.14 * R, ex + 0.09 * R
        else:
            xi, xo = ex - 0.09 * R, ex + 0.14 * R
        yb = -0.24 * R + bl * R
        yi, yo = yb + bi * R, yb + bo * R
        cx, cy = (xi + xo) / 2, (yi + yo) / 2 - 0.05 * R
        s += _line(f"M{fmt(xo)},{fmt(yo)} Q{fmt(cx)},{fmt(cy)} {fmt(xi)},{fmt(yi)}", w=3.4, col=brow_col)
    # nose: small rounded bump on the far cheek
    s += _ell(0.70 * R, 0.21 * R, 0.10 * R, 0.085 * R, shade(skin, -0.10))
    s += _line(f"M{fmt(0.61 * R)},{fmt(0.27 * R)} Q{fmt(0.72 * R)},{fmt(0.35 * R)} {fmt(0.81 * R)},{fmt(0.22 * R)}", w=2.6)
    s += _mouth(R, E["mouth"])
    if E.get("sweat"):
        s += _drop(0.98 * R, -0.42 * R, 0.09 * R)
    return s


def _mouth(R, kind, mx=None, my=None):
    mx = 0.18 * R if mx is None else mx
    my = 0.55 * R if my is None else my
    MI = P["mouth_inside"]

    def P_(x, y):
        return f"{fmt(mx + x * R)},{fmt(my + y * R)}"

    if kind == "smile":
        return _line(f"M{P_(-0.15, -0.02)} Q{P_(0, 0.13)} {P_(0.15, -0.02)}", w=3.2)
    if kind == "grin":
        return (f'<path d="M{P_(-0.19, -0.05)} Q{P_(0, 0.36)} {P_(0.19, -0.05)} Q{P_(0, 0.0)} {P_(-0.19, -0.05)} Z" '
                f'fill="{MI}" {_st(2.8)}/>'
                f'<path d="M{P_(-0.08, 0.14)} Q{P_(0, 0.08)} {P_(0.09, 0.14)} Q{P_(0, 0.20)} {P_(-0.08, 0.14)} Z" '
                f'fill="{TONGUE}"/>')
    if kind == "frown":
        return _line(f"M{P_(-0.14, 0.06)} Q{P_(0, -0.07)} {P_(0.14, 0.06)}", w=3.2)
    if kind == "grumpy":
        return _line(f"M{P_(-0.15, 0.05)} Q{P_(-0.05, -0.04)} {P_(0.02, -0.01)} T{P_(0.15, 0.06)}", w=3.4)
    if kind == "scared":
        return (f'<path d="M{P_(-0.12, 0.02)} Q{P_(-0.06, -0.06)} {P_(0, 0.0)} Q{P_(0.06, -0.06)} {P_(0.12, 0.02)} '
                f'Q{P_(0.1, 0.2)} {P_(0, 0.2)} Q{P_(-0.1, 0.2)} {P_(-0.12, 0.02)} Z" fill="{MI}" {_st(2.8)}/>')
    if kind == "o":
        return _ell(mx, my + 0.06 * R, 0.09 * R, 0.13 * R, MI, sw=2.8)
    if kind == "small_o":
        return _ell(mx, my + 0.03 * R, 0.05 * R, 0.065 * R, MI, sw=2.6)
    if kind == "small_open":
        return _ell(mx, my + 0.03 * R, 0.08 * R, 0.05 * R, MI, sw=2.6)
    if kind == "wave":
        return _line(f"M{P_(-0.17, 0.03)} Q{P_(-0.11, -0.05)} {P_(-0.05, 0.03)} T{P_(0.07, 0.03)} T{P_(0.17, 0.03)}",
                     w=3.0)
    if kind == "shout":
        return (_ell(mx, my + 0.08 * R, 0.17 * R, 0.19 * R, MI, sw=2.8) +
                _ell(mx + 0.01 * R, my + 0.19 * R, 0.10 * R, 0.06 * R, TONGUE))
    if kind == "wobble":
        return _line(f"M{P_(-0.12, 0.05)} Q{P_(-0.06, -0.02)} {P_(0, 0.02)} T{P_(0.12, 0.04)}", w=3.0)
    if kind == "flat":
        return _line(f"M{P_(-0.12, 0.03)} Q{P_(-0.04, -0.01)} {P_(0.02, 0.02)} T{P_(0.13, 0.01)}", w=3.0)
    return ""


# ======================================================================= head parts (head frame)


def _ear(R, skin):
    return (_ell(-0.84 * R, 0.12 * R, 0.17 * R, 0.22 * R, skin, sw=3.2) +
            _line(f"M{fmt(-0.80 * R)},{fmt(0.02 * R)} Q{fmt(-0.92 * R)},{fmt(0.12 * R)} {fmt(-0.80 * R)},{fmt(0.24 * R)}",
                  w=2.4))


def _polar(R, deg, k=1.0):
    a = math.radians(deg)
    return (R * k * math.cos(a), R * k * math.sin(a))


def _hair_cap(R, col, style="short", front=-28, back=165, line=-0.42):
    """Hair covering the top/back of the head. Angles in screen degrees (-90 = top, 180 = back)."""
    outer = []
    n = 16
    for i in range(n + 1):
        deg = front - (front - (back - 360)) * i / n
        k = 1.07
        if style == "curly":
            k = 1.03 + (0.08 if i % 2 else 0.0)
        outer.append(_polar(R, deg, k))
    inner = [_polar(R, back, 0.9), _polar(R, back - 25, 0.92), (-0.55 * R, line * R - 0.05 * R),
             (0.05 * R, line * R - 0.10 * R), (0.55 * R, line * R)]
    pts = outer + inner
    return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'


def _beard(R, col, kind):
    if kind is None:
        return ""
    if kind == "short":      # Jonah: short beard along the jaw, open below the mouth
        pts = [(-0.84 * R, 0.10 * R), (-0.86 * R, 0.55 * R), (-0.46 * R, 0.98 * R), (0.16 * R, 1.10 * R),
               (0.62 * R, 0.94 * R), (0.88 * R, 0.52 * R), (0.70 * R, 0.62 * R), (0.20 * R, 0.76 * R),
               (-0.28 * R, 0.66 * R), (-0.62 * R, 0.32 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
    if kind == "stubble":
        pts = [(-0.80 * R, 0.30 * R), (-0.72 * R, 0.70 * R), (-0.30 * R, 0.98 * R), (0.18 * R, 1.04 * R),
               (0.64 * R, 0.86 * R), (0.84 * R, 0.55 * R), (0.66 * R, 0.66 * R), (0.20 * R, 0.78 * R),
               (-0.30 * R, 0.70 * R), (-0.62 * R, 0.45 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.0)}/>'
    if kind in ("full", "white"):  # captain / elder: big rounded beard + moustache
        pts = [(-0.86 * R, 0.0), (-0.92 * R, 0.62 * R), (-0.55 * R, 1.22 * R), (0.10 * R, 1.42 * R),
               (0.68 * R, 1.18 * R), (0.92 * R, 0.55 * R), (0.70 * R, 0.62 * R), (0.20 * R, 0.80 * R),
               (-0.30 * R, 0.68 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.18)
        s += _line(f"M{fmt(-0.25 * R)},{fmt(0.95 * R)} q{fmt(0.05 * R)},{fmt(0.18 * R)} {fmt(0.02 * R)},{fmt(0.30 * R)}",
                   w=2.2, col=dark)
        s += _line(f"M{fmt(0.35 * R)},{fmt(0.95 * R)} q{fmt(0.02 * R)},{fmt(0.16 * R)} {fmt(-0.04 * R)},{fmt(0.28 * R)}",
                   w=2.2, col=dark)
        return s
    if kind in ("assyrian", "assyrian_short"):
        L = 1.52 if kind == "assyrian" else 1.30
        pts = [(-0.86 * R, -0.05 * R), (-0.88 * R, 0.55 * R), (-0.62 * R, (L - 0.05) * R), (-0.20 * R, L * R),
               (0.12 * R, (L + 0.06) * R), (0.46 * R, L * R), (0.74 * R, (L - 0.12) * R), (0.92 * R, 0.55 * R),
               (0.70 * R, 0.62 * R), (0.20 * R, 0.78 * R), (-0.30 * R, 0.68 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        curl = mix(col, "#c9b29a", 0.55)
        rows = 3 if kind == "assyrian" else 2
        for r_ in range(rows):
            yy = (0.92 + r_ * 0.22) * R
            x0, x1 = (-0.62 + 0.06 * r_) * R, (0.70 - 0.04 * r_) * R
            n = 5
            w = (x1 - x0) / n
            d = f"M{fmt(x0)},{fmt(yy)}"
            for i in range(n):
                d += f" q{fmt(w / 2)},{fmt(0.13 * R)} {fmt(w)},0"
            s += f'<path d="{d}" fill="none" {_st(2.2, curl)}/>'
        return s
    return ""


def _moustache(R, col, kind):
    if kind not in ("full", "white", "assyrian", "assyrian_short"):
        return ""
    mx, my = 0.18 * R, 0.47 * R
    return (f'<path d="M{fmt(mx - 0.26 * R)},{fmt(my + 0.10 * R)} Q{fmt(mx - 0.16 * R)},{fmt(my - 0.06 * R)} '
            f'{fmt(mx)},{fmt(my + 0.0)} Q{fmt(mx + 0.16 * R)},{fmt(my - 0.06 * R)} {fmt(mx + 0.26 * R)},{fmt(my + 0.10 * R)} '
            f'Q{fmt(mx + 0.12 * R)},{fmt(my + 0.06 * R)} {fmt(mx)},{fmt(my + 0.07 * R)} '
            f'Q{fmt(mx - 0.12 * R)},{fmt(my + 0.06 * R)} {fmt(mx - 0.26 * R)},{fmt(my + 0.10 * R)} Z" '
            f'fill="{col}" {_st(2.6)}/>')


# ---------------------------------------------------------------- headwear (head frame)


def _cloth_cap(R, col, edge=None):
    """Head-cloth / veil covering top and back of head; front edge across the forehead."""
    pts = [(0.94 * R, -0.30 * R), (0.80 * R, -0.78 * R), (0.25 * R, -1.10 * R), (-0.45 * R, -1.04 * R),
           (-0.98 * R, -0.62 * R), (-1.14 * R, 0.05 * R), (-1.10 * R, 0.62 * R), (-0.80 * R, 0.72 * R),
           (-0.64 * R, 0.30 * R), (-0.60 * R, -0.18 * R), (-0.20 * R, -0.40 * R), (0.45 * R, -0.42 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.6)}/>'
    s += _line(f"M{fmt(-0.30 * R)},{fmt(-0.88 * R)} Q{fmt(-0.78 * R)},{fmt(-0.45 * R)} {fmt(-0.86 * R)},{fmt(0.40 * R)}",
               w=2.2, col=shade(col, -0.22))
    if edge:
        s += _tube(smooth_path_pts([(0.97 * R, -0.33 * R), (0.45 * R, -0.50 * R), (-0.18 * R, -0.46 * R),
                                    (-0.62 * R, -0.18 * R), (-0.70 * R, 0.25 * R)]), 0.15 * R, edge, ow=2.4)
    return s


def smooth_path_pts(pts, steps=6):
    """Catmull-Rom sampled points (open curve) for tubes."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        for j in range(steps):
            t = j / steps
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def _headband(R, col, tails=True):
    s = ""
    if tails:
        s += _tube([(-0.92 * R, -0.25 * R), (-1.25 * R, 0.10 * R), (-1.32 * R, 0.42 * R)], 0.10 * R, col, ow=2.4)
        s += _tube([(-0.92 * R, -0.25 * R), (-1.10 * R, 0.25 * R), (-1.08 * R, 0.55 * R)], 0.10 * R, col, ow=2.4)
    s += _tube(smooth_path_pts([(0.98 * R, -0.36 * R), (0.45 * R, -0.54 * R), (-0.25 * R, -0.52 * R),
                                (-0.92 * R, -0.25 * R)]), 0.15 * R, col, ow=2.6)
    return s


def _knit_cap(R, col):
    dome = [(0.92 * R, -0.36 * R), (0.80 * R, -0.85 * R), (0.20 * R, -1.20 * R), (-0.55 * R, -1.10 * R),
            (-1.0 * R, -0.55 * R), (-1.02 * R, -0.20 * R)]
    s = f'<path d="{smooth_path(dome + [(0.0, -0.45 * R)])}" fill="{col}" {_st(3.4)}/>'
    s += _tube(smooth_path_pts([(0.98 * R, -0.36 * R), (0.40 * R, -0.52 * R), (-0.35 * R, -0.48 * R),
                                (-1.02 * R, -0.18 * R)]), 0.20 * R, shade(col, -0.15), ow=2.6)
    for x in (-0.45, -0.05, 0.35):
        s += _line(f"M{fmt(x * R)},{fmt(-0.66 * R)} Q{fmt((x + 0.06) * R)},{fmt(-0.92 * R)} {fmt((x + 0.02) * R)},"
                   f"{fmt(-1.08 * R)}", w=2.0, col=shade(col, -0.25))
    s += f'<circle cx="{fmt(-0.05 * R)}" cy="{fmt(-1.22 * R)}" r="{fmt(0.13 * R)}" fill="{shade(col, 0.2)}" {_st(2.6)}/>'
    return s


def _red_cap(R, col):
    """Captain's soft cap with the tip flopping forward."""
    pts = [(0.96 * R, -0.34 * R), (0.95 * R, -0.80 * R), (1.25 * R, -1.02 * R), (1.18 * R, -1.30 * R),
           (0.55 * R, -1.42 * R), (-0.30 * R, -1.25 * R), (-0.95 * R, -0.72 * R), (-1.04 * R, -0.22 * R),
           (0.0, -0.52 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(0.10 * R)},{fmt(-1.25 * R)} Q{fmt(0.70 * R)},{fmt(-1.20 * R)} {fmt(1.0 * R)},{fmt(-0.92 * R)}",
               w=2.2, col=shade(col, -0.3))
    s += _tube(smooth_path_pts([(1.0 * R, -0.36 * R), (0.40 * R, -0.54 * R), (-0.35 * R, -0.50 * R),
                                (-1.04 * R, -0.18 * R)]), 0.18 * R, shade(col, -0.18), ow=2.6)
    return s


def _crown(R, col=GOLD, x0=0.0, y0=0.0, k=1.0):
    """Tall Assyrian crown (truncated cone with small top spike). Base centre at (x0, y0)."""
    def q(x, y):
        return f"{fmt(x0 + x * R * k)},{fmt(y0 + y * R * k)}"
    dark = GOLD_DARK
    s = (f'<path d="M{q(-0.72, 0.02)} L{q(-0.62, -1.15)} Q{q(0.05, -1.30)} {q(0.72, -1.15)} L{q(0.82, 0.02)} '
         f'Q{q(0.05, 0.20)} {q(-0.72, 0.02)} Z" fill="{col}" {_st(3.4)}/>')
    s += (f'<path d="M{q(-0.62, -1.15)} Q{q(0.05, -1.00)} {q(0.72, -1.15)} Q{q(0.05, -1.30)} {q(-0.62, -1.15)} Z" '
          f'fill="{shade(col, 0.18)}" {_st(2.6)}/>')
    s += f'<path d="M{q(-0.10, -1.18)} L{q(0.06, -1.62)} L{q(0.22, -1.18)} Z" fill="{col}" {_st(2.8)}/>'
    for yy in (-0.32, -0.80):
        s += _line(f"M{q(-0.70, yy)} Q{q(0.05, yy + 0.16)} {q(0.80, yy)}", w=2.4, col=dark)
    for xx in (-0.40, 0.05, 0.50):
        s += f'<circle cx="{fmt(x0 + xx * R * k)}" cy="{fmt(y0 - 0.52 * R * k + (0.05 if xx == 0.05 else 0) * R * k)}" ' \
             f'r="{fmt(0.09 * R * k)}" fill="{P["royal_light"]}" {_st(2.0)}/>'
    return s


def _wrap(R, col, stripe=None):
    """Simple wrapped cap (townspeople / elders)."""
    pts = [(0.94 * R, -0.34 * R), (0.75 * R, -0.95 * R), (0.0, -1.18 * R), (-0.80 * R, -0.95 * R),
           (-1.04 * R, -0.30 * R), (-0.5 * R, -0.50 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    for yy in (-0.62, -0.86):
        s += _line(f"M{fmt(-0.95 * R)},{fmt((yy + 0.28) * R)} Q{fmt(0.0)},{fmt((yy - 0.22) * R)} {fmt(0.88 * R)},"
                   f"{fmt(yy * R)}", w=2.2, col=shade(col, -0.22))
    s += _tube(smooth_path_pts([(0.98 * R, -0.36 * R), (0.40 * R, -0.52 * R), (-0.35 * R, -0.48 * R),
                                (-1.04 * R, -0.22 * R)]), 0.14 * R, stripe or shade(col, -0.15), ow=2.4)
    return s


# ======================================================================= hands & feet


def _hand(W, d, style, skin, hr):
    """Hand at wrist W, forearm direction d (unit)."""
    if style == "none":
        return ""
    pp = _rot(d, -90)
    st = _st(3.2)
    if style == "fist":
        c = _add(W, _mul(d, 0.45 * hr))
        return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'
    if style in ("open", "cup"):
        c = _add(W, _mul(d, 0.75 * hr))
        a = _ang(d)
        th = _add(_add(W, _mul(d, 0.45 * hr)), _mul(pp, 0.85 * hr))
        return (f'<ellipse cx="{fmt(th[0])}" cy="{fmt(th[1])}" rx="{fmt(0.42 * hr)}" ry="{fmt(0.32 * hr)}" '
                f'transform="rotate({fmt(a - 30)} {fmt(th[0])} {fmt(th[1])})" fill="{skin}" {st}/>'
                f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(1.22 * hr)}" ry="{fmt(0.88 * hr)}" '
                f'transform="rotate({fmt(a)} {fmt(c[0])} {fmt(c[1])})" fill="{skin}" {st}/>')
    if style == "palm":           # open palm facing out, fingers up
        c = _add(W, (0, -0.7 * hr))
        s = (f'<ellipse cx="{fmt(c[0] - 0.85 * hr)}" cy="{fmt(c[1] + 0.25 * hr)}" rx="{fmt(0.42 * hr)}" '
             f'ry="{fmt(0.30 * hr)}" transform="rotate(-35 {fmt(c[0] - 0.85 * hr)} {fmt(c[1] + 0.25 * hr)})" '
             f'fill="{skin}" {st}/>')
        s += _ell(c[0], c[1], 0.95 * hr, 1.25 * hr, skin, sw=3.2)
        for dx in (-0.32, 0.0, 0.32):
            s += _line(f"M{fmt(c[0] + dx * hr)},{fmt(c[1] - 1.18 * hr)} l0,{fmt(0.55 * hr)}", w=2.0)
        return s
    if style == "point":
        c = _add(W, _mul(d, 0.45 * hr))
        tip = _add(W, _mul(d, 2.2 * hr))
        base = _add(W, _mul(d, 0.9 * hr))
        return (_tube([base, tip], 0.62 * hr, skin, ow=3.0) +
                f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>')
    if style == "pray":           # two palms pressed together, fingertips up
        c = W
        return (f'<path d="M{fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Q{fmt(c[0] + 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} '
                f'{fmt(c[0] + 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} L{fmt(c[0] - 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} '
                f'Q{fmt(c[0] - 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} {fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Z" '
                f'fill="{skin}" {st}/>' +
                _line(f"M{fmt(c[0])},{fmt(c[1] - 1.7 * hr)} L{fmt(c[0])},{fmt(c[1] + 0.5 * hr)}", w=2.0))
    c = _add(W, _mul(d, 0.45 * hr))
    return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'


def _foot(A, ang, skin, fl, sandal=SANDAL, bare=False):
    """Foot at ankle A pointing along screen angle ``ang`` (0 = +x). Returns (svg, sole points)."""
    def q(x, y):
        v = _rot((x, y), ang)
        return (A[0] + v[0], A[1] + v[1])
    foot = [q(-0.30 * fl, -0.15 * fl), q(-0.34 * fl, 0.20 * fl), q(0.15 * fl, 0.30 * fl), q(0.85 * fl, 0.30 * fl),
            q(0.95 * fl, 0.12 * fl), q(0.60 * fl, -0.08 * fl), q(0.05 * fl, -0.26 * fl)]
    s = ""
    if not bare:
        sole = [q(-0.40 * fl, 0.24 * fl), q(1.00 * fl, 0.24 * fl), q(1.02 * fl, 0.40 * fl), q(-0.40 * fl, 0.40 * fl)]
        s += f'<path d="{smooth_path(sole)}" fill="{sandal}" {_st(3.0)}/>'
    s += f'<path d="{smooth_path(foot)}" fill="{skin}" {_st(3.0)}/>'
    if not bare:
        s += _tube([q(0.30 * fl, -0.12 * fl), q(0.40 * fl, 0.24 * fl)], 0.12 * fl, sandal, ow=1.8)
    soles = [q(-0.40 * fl, 0.40 * fl), q(1.0 * fl, 0.40 * fl), q(0.3 * fl, 0.40 * fl)]
    return s, soles


# ======================================================================= poses


def _P(**kw):
    base = dict(t=0, h=0, legs=((3, 1), (-3, -1)), arms=(("fk", 8, 3), ("fk", -8, -3)),
                hands=("fist", "fist"), seat=False, anchor="pelvis", hem=None, flare=0,
                far_front=False, near_back=False, tail=None, flip=False, spin=0, marks=(),
                expr="neutral", look=(0, 0), feet=(None, None), far_over_head=False, fan_arm=1)
    base.update(kw)
    return base


POSES = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -24, -14), ("fk", 26, 46))),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 48), ("fk", -24, -14))),
    "run_a": _P(t=14, legs=((66, 16), (-30, -96)), arms=(("fk", -62, -12), ("fk", 64, 104)),
                hands=("fist", "fist"), hem=0.66, tail=-102, flare=-4),
    "run_b": _P(t=14, legs=((-30, -96), (66, 16)), arms=(("fk", 64, 112), ("fk", -58, -14)),
                hands=("fist", "fist"), hem=0.66, tail=-102, flare=-4),
    "sleep": _P(t=-88, h=13, legs=((100, 80), (94, 86)),
                arms=(("ik", "headw", 0.30, 0.92, 1), ("ik", "headw", 0.05, 0.95, 1)),
                hands=("open", "open"), anchor="center", far_front=True, near_back=True, tail=-62,
                expr="sleepy", feet=(-75, -80), hem=0.95),
    "kneel_pray": _P(t=-4, h=-16, legs=((4, -88), (0, -92)),
                     arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)),
                     hands=("none", "pray"), expr="peaceful", feet=(100, 100), hem=0.97),
    "sit": _P(t=-3, seat=True, legs=(("sit", 32), ("sit", 26)),
              arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), hands=("fist", "fist"), hem=0.97),
    "sit_sulk": _P(t=-2, h=10, seat=True, legs=(("sit", 30), ("sit", 22)),
                   arms=(("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
                   far_front=True, hands=("fist", "fist"), expr="angry", hem=0.97),
    "sit_faint": _P(t=-16, h=24, seat=True, legs=((86, 74), (80, 66)),
                    arms=(("ik", "headw", 1.55, 0.05, 1), ("fk", -40, -14)), hands=("open", "open"),
                    marks=("fan",), fan_arm=0, expr="tired", hem=0.97),
    "sit_happy": _P(t=-6, h=-6, seat=True, legs=((84, 76), (92, 82)),
                    arms=(("fk", 118, 145), ("fk", -112, -140)), hands=("open", "open"), expr="happy", hem=0.97),
    "preach": _P(t=-3, h=-6, legs=((8, 3), (-7, -3)),
                 arms=(("fk", 152, 168), ("fk", 30, 74)), hands=("open", "open"), expr="shout"),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 84, 88), ("fk", -8, -3)), hands=("point", "fist")),
    "arms_up": _P(h=-6, arms=(("fk", 150, 168), ("fk", -150, -168)), hands=("open", "open"), expr="happy"),
    "fall": _P(spin=28, legs=((44, 12), (-24, -64)), arms=(("fk", 128, 150), ("fk", -140, -165)),
               hands=("open", "open"), anchor="center", tail=175, expr="scared", flare=8),
    "float": _P(t=2, h=-6, legs=((18, -8), (-14, 14)), arms=(("fk", 96, 108), ("fk", -96, -108)),
                hands=("open", "open"), anchor="center", tail=165, expr="scared", flare=14),
    "refuse": _P(flip=True, t=-4, h=8, legs=((14, 4), (-10, -14)),
                 arms=(("fk", 8, 3), ("fk", -112, -168)), hands=("fist", "palm"), marks=("shake",),
                 expr="angry", tail=-30),
    "confess": _P(t=6, h=18, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
                  expr="sorry"),
    "listen": _P(h=-14, arms=(("fk", 14, 8), ("ik", "head", -1.12, 0.12, -1)), hands=("fist", "cup"),
                 near_back=False, look=(0.02, -0.06)),
    "wake": _P(t=2, h=-4, seat=True, legs=((88, 78), (84, 72)),
               arms=(("fk", 148, 172), ("ik", "head", -0.14, 0.10, -1)), hands=("open", "fist"),
               expr="sleepy"),
    # ---- generic poses used by the other characters
    "scared": _P(t=-4, legs=((10, 2), (-8, -4)),
                 arms=(("ik", "headw", 1.15, 0.45, 1), ("ik", "headw", -1.15, 0.45, -1)),
                 hands=("open", "open"), expr="scared"),
    "throw": _P(t=-10, h=-8, legs=((16, 4), (-14, -6)), arms=(("fk", 150, 166), ("fk", 162, 172)),
                hands=("open", "open"), expr="worried", near_back=True),
    "carry": _P(t=14, legs=((26, -6), (-16, -30)), arms=(("fk", 40, 80), ("fk", 52, 88)),
                hands=("fist", "fist"), expr="worried"),
    "pray": _P(t=-6, h=-20, arms=(("fk", 158, 172), ("fk", -158, -172)), hands=("open", "open"),
               expr="scared", look=(0.02, -0.06)),
    "pull": _P(t=-20, legs=((30, 18), (-12, -4)), arms=(("fk", 76, 82), ("fk", 70, 78)),
               hands=("fist", "fist"), expr="angry"),
    "lift": _P(t=-4, h=-14, legs=((12, 2), (-10, -2)), arms=(("fk", 160, 176), ("fk", 172, 184)),
               hands=("open", "open"), expr="worried", near_back=True),
    "wake_other": _P(t=26, h=-10, legs=((14, 6), (-12, -6)), arms=(("fk", 24, 18), ("fk", 50, 30)),
                     hands=("fist", "open"), expr="worried"),
    "worried": _P(t=-2, arms=(("ik", "head", 0.80, -0.78, 1), ("ik", "head", -0.80, -0.75, -1)),
                  hands=("open", "open"), expr="worried", far_over_head=True),
    "sit_throne": _P(t=-2, legs=((86, 4), (82, 2)), arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)),
                     hands=("fist", "fist"), anchor="pelvis", hem=0.97),
    "sit_ashes": _P(t=6, h=24, seat=True, legs=(("sit", 30), ("sit", 24)),
                    arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), hands=("fist", "fist"),
                    expr="sad", hem=0.97),
    "remove_crown": _P(t=-2, h=8, arms=(("ik", "torso", 1.55, 0.58, 1), ("ik", "torso", 1.15, 0.60, 1)),
                       hands=("fist", "fist"), expr="sorry"),
    "walk": None,          # alias -> walk_a (filled below)
    "sad": _P(t=6, h=24, arms=(("fk", 6, 2), ("fk", -6, -2)), expr="sad"),
    "cheer": _P(h=-8, legs=((10, 4), (-8, -2)), arms=(("fk", 145, 165), ("fk", -150, -170)),
                hands=("open", "open"), expr="happy"),
    "listen_chin": _P(h=-6, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
                      expr="worried"),
}
POSES["walk"] = POSES["walk_a"]


# ======================================================================= the rig


def _ik(S, T, L1, L2, bend):
    d = _sub(T, S)
    dist = _len(d)
    dn = _nrm(d) if dist > 1e-6 else (0.0, 1.0)
    dist = max(min(dist, (L1 + L2) * 0.999), abs(L1 - L2) + 1.0)
    a = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
    hh = math.sqrt(max(L1 * L1 - a * a, 0.0))
    perp = (-dn[1], dn[0])
    E = _add(_add(S, _mul(dn, a)), _mul(perp, hh * bend))
    W = _add(S, _mul(dn, dist))
    return E, W


def _leg_point(H, K, A, th, d):
    """Point at distance d along the leg polyline hip->knee->ankle, plus local direction."""
    if d <= th:
        dirv = _nrm(_sub(K, H))
        return _add(H, _mul(dirv, d)), dirv, True
    dirv = _nrm(_sub(A, K))
    return _add(K, _mul(dirv, d - th)), dirv, False


def _figure(D, m, pose, expr, opts=None):
    """Build a person. Returns (inner svg in local coords, matrix tuple, extents).

    D: design dict, m: metrics dict, pose: pose dict (POSES entry, possibly modified).
    """
    opts = opts or {}
    ps = pose
    t, h = ps["t"], ps["h"]
    u = _rot((0, -1), t)
    f = _rot((1, 0), t)

    def tp(fx, uy):
        return (f[0] * fx + u[0] * uy, f[1] * fx + u[1] * uy)

    R = m["R"]
    pel = (0.0, 0.0)
    ext = []   # (x, y, r) for bbox / grounding

    # ---------------- legs
    hips = [tp(m["hw"], -4), tp(-m["hw"], -4)]
    legs = []
    for i, spec in enumerate(ps["legs"]):
        if spec[0] == "sit":
            a2 = spec[1]
            hy = hips[i][1]
            c = (m["seat"] - m["ank"] - hy - m["sh"] * math.cos(math.radians(a2))) / m["th"]
            a1 = math.degrees(math.acos(max(-1.0, min(1.0, c))))
        else:
            a1, a2 = spec
        H = hips[i]
        K = _add(H, _mul(_dv(a1), m["th"]))
        A = _add(K, _mul(_dv(a2), m["sh"]))
        legs.append((H, K, A, a1, a2))
        ext += [(K[0], K[1], m["lw"] / 2 + OW)]

    # ---------------- head
    N = tp(0, m["T"])
    ha = t + h
    Hc = _add(N, _rot((2.0, -m["neck"]), ha))

    def hw(hx, hy):
        v = _rot((hx * R, hy * R), ha)
        return (Hc[0] + v[0], Hc[1] + v[1])

    ext.append((Hc[0], Hc[1], R + OW))
    top = hw(0, -1.0 - D.get("hat_h", 0.08))
    ext.append((top[0], top[1], 2))

    # ---------------- arms
    L1, L2 = m["ua"], m["fa"]
    S = [tp(m["sw"], m["T"] - m["sdrop"]), tp(-m["sw"], m["T"] - m["sdrop"])]
    arms = []
    for i, spec in enumerate(ps["arms"]):
        if spec[0] == "fk":
            E = _add(S[i], _mul(_dv(spec[1]), L1))
            W = _add(E, _mul(_dv(spec[2]), L2))
        else:
            kind, x, y, bend = spec[1], spec[2], spec[3], spec[4]
            if kind == "torso":
                T_ = tp(x * m["sw"], y * m["T"])
            elif kind == "head":
                T_ = hw(x, y)
            elif kind == "headw":
                T_ = (Hc[0] + x * R, Hc[1] + y * R)
            elif kind == "knee":
                K = legs[int(x)][1]
                T_ = (K[0], K[1] - y * R)
            else:
                T_ = _add(S[i], (x * (L1 + L2), y * (L1 + L2)))
            E, W = _ik(S[i], T_, L1, L2, bend)
        arms.append((S[i], E, W))
        ext += [(E[0], E[1], m["aw"] / 2 + OW), (W[0], W[1], m["hr"] + OW)]

    # ---------------- robe hulls
    hem_frac = D["hem"] if ps["hem"] is None else min(D["hem"], ps["hem"])
    hem_d = hem_frac * (m["th"] + m["sh"])
    flare = m["flare"] * D.get("flare_k", 1.0) + ps["flare"]
    skirt_pts = [tp(m["ww"] + 1, 2), tp(-m["ww"] - 1, 2), tp(m["ww"] - 4, -10), tp(-m["ww"] + 4, -10)]
    if ps["seat"]:
        skirt_pts += [tp(m["ww"] * 0.8, -m["seat"]), tp(-m["ww"] * 0.9, -m["seat"])]
    hem_pts, hem_dirs = [], []
    for (H, K, A, a1, a2) in legs:
        Q, dq, on_thigh = _leg_point(H, K, A, m["th"], hem_d)
        nq = (-dq[1], dq[0])
        wq = m["lw"] / 2 + flare
        skirt_pts += [_add(Q, _mul(nq, wq)), _sub(Q, _mul(nq, wq))]
        if not on_thigh:
            dk = _nrm(_sub(K, H))
            nk = (-dk[1], dk[0])
            wk = m["lw"] / 2 + 9
            skirt_pts += [_add(K, _mul(nk, wk)), _sub(K, _mul(nk, wk))]
        hem_pts.append(Q)
        hem_dirs.append(dq)
    skirt = _rounded(_hull(skirt_pts), 14)
    bodice = _rounded(_hull([tp(m["shw"], m["T"] - 16), tp(-m["shw"], m["T"] - 16),
                             tp(m["shw"] - 13, m["T"] + 1), tp(-m["shw"] + 13, m["T"] + 1), tp(0, m["T"] + 3),
                             tp(m["ww"], -2), tp(-m["ww"], -2)]), 13)
    robe_polys = [bodice, skirt]
    for poly in robe_polys:
        ext += [(x, y, OW) for x, y in poly]
    Hm = _mul(_add(hem_pts[0], hem_pts[1]), 0.5)
    um = _nrm(_add(hem_dirs[0], hem_dirs[1]))

    # ---------------- feet
    feet_svg = []
    for i, (H, K, A, a1, a2) in enumerate(legs):
        fa = ps["feet"][i]
        if fa is None:
            fa = _ang(_rot(_dv(a2), -90))
        sv, soles = _foot(A, fa, D["leg"], m["fl"], D.get("sandal", SANDAL), bare=D.get("bare", False))
        feet_svg.append(sv)
        ext += [(x, y, 0) for x, y in soles]
        ext.append((A[0], A[1], m["lw"] / 2 + OW))

    # ---------------- transform & grounding
    flip = -1 if ps["flip"] else 1
    spin = ps["spin"]

    def xf(p):
        q = (p[0] * flip, p[1])
        return _rot(q, spin)

    tx = [(xf((x, y)), r) for x, y, r in ext]
    gy = max(p[1] + r for p, r in tx)
    minx = min(p[0] - r for p, r in tx)
    maxx = max(p[0] + r for p, r in tx)
    if ps["anchor"] == "center":
        ax = (minx + maxx) / 2
    else:
        ax = 0.0
    ground_body = None  # body-space ground y (valid when spin == 0)
    if spin == 0:
        ground_body = gy

    # ======================== draw
    st = {"pel": pel, "u": u, "f": f, "tp": tp, "legs": legs, "arms": arms, "Hc": Hc, "hw": hw, "ha": ha,
          "S": S, "N": N, "m": m, "ground": ground_body, "robe": robe_polys, "Hm": Hm, "um": um}
    out = []
    # props behind everything
    if D.get("behind"):
        out.append(D["behind"](st))
    # back layer: cloth tails, long hair, veils
    out.append(_back_layer(D, st, ps))

    def arm_svg(i):
        Sx, E, W = arms[i]
        skin = D["skin"]
        s = ""
        sl = D.get("sleeve_len", 1.0)
        if sl < 1.0:
            s += _tube([Sx, E, W], m["aw"] * 0.82, skin)
            mid = _lerp(Sx, E, min(1.0, sl * 2)) if sl <= 0.5 else _lerp(E, W, (sl - 0.5) * 2)
            pts = [Sx, mid] if sl <= 0.5 else [Sx, E, mid]
            s += _tube(pts, m["aw"], D["sleeve"])
        else:
            s += _tube([Sx, E, W], m["aw"], D["sleeve"])
            if D.get("cuff"):
                dw = _nrm(_sub(W, E))
                c0 = _sub(W, _mul(dw, 8))
                s += (f'<path d="M{_pt(c0)} L{_pt(W)}" stroke="{D["cuff"]}" stroke-width="{fmt(m["aw"])}" '
                      f'stroke-linecap="butt"/>')
                s += _line(f"M{_pt(_add(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))} "
                           f"L{_pt(_sub(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))}", w=2.2)
        dw = _nrm(_sub(W, E))
        s += _hand(W, dw, ps["hands"][i], skin, m["hr"])
        return s

    if not ps["far_front"] and not ps["far_over_head"]:
        out.append(arm_svg(0))
    for i in (0, 1):
        H, K, A, a1, a2 = legs[i]
        out.append(_tube([H, K, A], m["lw"], D["leg"]))
        out.append(feet_svg[i])
    # robe
    out.append(_robe(D, st, ps))
    if ps["far_front"]:
        out.append(arm_svg(0))
    if D.get("mid"):
        out.append(D["mid"](st))
    if ps["near_back"]:
        out.append(arm_svg(1))
    out.append(_head_svg(D, st, ps, expr))
    if ps["far_over_head"]:
        out.append(arm_svg(0))
    if not ps["near_back"]:
        out.append(arm_svg(1))
    if D.get("front"):
        out.append(D["front"](st))
    out.append(_marks(D, st, ps, expr))
    body = "".join(out)
    tf = f"translate({fmt(-ax)},{fmt(-gy)})"
    if spin:
        tf += f" rotate({fmt(spin)})"
    if flip < 0:
        tf += " scale(-1,1)"
    bbox = (minx - ax, min(p[1] - r for p, r in tx) - gy, maxx - ax, 0.0)
    return f'<g transform="{tf}">{body}</g>', bbox


# ---------------------------------------------------------------- robe


def _robe(D, st, ps):
    m, tp, u, f = st["m"], st["tp"], st["u"], st["f"]
    bodice, skirt = st["robe"]
    polys = [bodice, skirt]
    col = D["robe"]
    s = ""
    if D.get("fringe"):
        # fringe: dashed strip just below the hem edge (drawn first, the robe covers its top)
        chain = [p for p in skirt if _dot(_sub(p, st["Hm"]), st["um"]) > -3]
        if len(chain) > 2:
            chain = sorted(chain, key=lambda p: _dot(_sub(p, st["Hm"]), (-st["um"][1], st["um"][0])))
            off = [_add(p, _mul(st["um"], 4)) for p in chain]
            s += (f'<path d="{_d(off, closed=False)}" fill="none" stroke="{D["fringe"]}" stroke-width="10" '
                  f'stroke-dasharray="2.6 3.2"/>')
    s += _union(polys, col)
    cid = _clip_id("robe", *[_d(p) for p in polys])
    clip = f'<clipPath id="{cid}">' + "".join(f'<path d="{_d(p)}"/>' for p in polys) + "</clipPath>"
    inner = ""
    # stripes (sailor tunics): bands perpendicular to the torso axis
    if D.get("stripes"):
        sc, sp, sw_ = D["stripes"]
        k = -8
        while k * sp < m["T"] + 30:
            d0 = k * sp
            for poly in polys:
                b = _band(poly, st["pel"], u, d0, d0 + sw_)
                inner += _poly(b, sc, sw=0)
            k += 1
    # coat (captain): back part of the robe in coat colour, front strip shows the tunic
    if D.get("coat"):
        cut = D.get("coat_cut", 0.30) * m["ww"]
        for poly in polys:
            c = _clip(poly, _add(st["pel"], _mul(f, cut)), _mul(f, -1))
            inner += _poly(c, D["coat"], sw=0)
    # folds
    fold = shade(D.get("coat") or col, -0.16)
    for x0, x1 in ((-0.45, -0.62), (0.35, 0.50)):
        a = tp(x0 * m["ww"], -14)
        b = _add(st["Hm"], _mul(f, x1 * m["ww"]))
        b = _sub(b, _mul(st["um"], 16))
        mid = _add(_lerp(a, b, 0.5), _mul(f, 3))
        inner += _line(f"M{_pt(a)} Q{_pt(mid)} {_pt(b)}", w=2.4, col=fold, extra='opacity="0.8"')
    # hem band
    hem = D.get("hem_col")
    if hem:
        hb = _clip(skirt, _sub(st["Hm"], _mul(st["um"], D.get("hem_w", 13))), st["um"])
        if D.get("coat"):
            inner += _poly(hb, D.get("coat_hem", hem), sw=0)
        else:
            inner += _poly(hb, hem, sw=0)
        inner += _line(_d(_band_edge(skirt, st["Hm"], st["um"], -D.get("hem_w", 13)), closed=False), w=2.6)
    # texture (sackcloth)
    if D.get("texture") == "sack":
        tcol = P["sackcloth_dark"]
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        d = ""
        yy = y0
        while yy < y1:
            d += f"M{fmt(x0)},{fmt(yy)} L{fmt(x1)},{fmt(yy + 3)} "
            yy += 9
        xx = x0
        while xx < x1:
            d += f"M{fmt(xx)},{fmt(y0)} L{fmt(xx + 4)},{fmt(y1)} "
            xx += 11
        inner += f'<path d="{d}" fill="none" stroke="{tcol}" stroke-width="1.6" opacity="0.45"/>'
        # patch
        pc = tp(-0.35 * m["ww"], 0.45 * m["T"])
        inner += (f'<rect x="{fmt(pc[0] - 9)}" y="{fmt(pc[1] - 8)}" width="18" height="16" rx="3" '
                  f'fill="{shade(P["sackcloth"], -0.08)}" stroke="{tcol}" stroke-width="2" stroke-dasharray="3 3"/>')
    # shawl: diagonal band from the near shoulder to the far hip
    if D.get("shawl"):
        n = _nrm(_add(_mul(u, 0.80), _mul(f, 0.60)))
        p0 = tp(-0.1 * m["ww"], 0.55 * m["T"])
        for poly in polys:
            b = _band(poly, p0, n, -13, 13)
            inner += _poly(b, D["shawl"], sw=2.6)
        if D.get("shawl_trim"):
            for poly in polys:
                for off in (-9, 9):
                    b = _band(poly, p0, n, off - 1.5, off + 1.5)
                    inner += _poly(b, D["shawl_trim"], sw=0)
    if D.get("collar"):
        c0, c1, c2 = tp(-m["shw"] * 0.55, m["T"] - 2), tp(m["shw"] * 0.55, m["T"] - 2), tp(0, m["T"] - 22)
        inner += _line(f"M{_pt(c0)} Q{_pt(c2)} {_pt(c1)}", w=7, col=D["collar"])
        inner += _line(f"M{_pt(c0)} Q{_pt(c2)} {_pt(c1)}", w=1.8, col=GOLD_DARK)
    if D.get("neck_v"):
        a, b, c = tp(-11, m["T"] + 1), tp(12, m["T"] + 1), tp(1, m["T"] - 20)
        inner += _poly([a, c, b], D["neck_v"], sw=2.6)
    # belt / sash
    if D.get("sash"):
        for poly in polys:
            b = _band(poly, st["pel"], u, -6, 11)
            inner += _poly(b, D["sash"], sw=2.8)
        if D.get("sash_tail", True):
            k0 = tp(0.45 * m["ww"], 2)
            k1 = _add(tp(0.55 * m["ww"], -26), _mul(f, 2))
            k2 = _add(tp(0.35 * m["ww"], -34), _mul(f, 0))
            inner += _tube([k0, k1], 7, D["sash"], ow=2.6) + _tube([k0, k2], 7, D["sash"], ow=2.6)
            inner += f'<circle cx="{fmt(k0[0])}" cy="{fmt(k0[1])}" r="6.5" fill="{D["sash"]}" {_st(2.6)}/>'
    if D.get("rope_belt"):
        rc = D["rope_belt"]
        for poly in polys:
            b = _band(poly, st["pel"], u, -3, 6)
            inner += _poly(b, rc, sw=2.4)
        for poly in polys:
            b = _band(poly, st["pel"], u, -3, 6)
            if len(b) > 2:
                xs = sorted(b, key=lambda p: _dot(p, f))
                a, z = xs[0], xs[-1]
                for i in range(1, 7):
                    q = _lerp(a, z, i / 7)
                    inner += _line(f"M{_pt(_add(q, _mul(u, 4)))} L{_pt(_sub(_add(q, _mul(f, 4)), _mul(u, 3)))}",
                                   w=1.6, col=shade(rc, -0.35))
        k0 = tp(0.40 * m["ww"], 1)
        inner += _tube([k0, tp(0.48 * m["ww"], -30)], 4.5, rc, ow=2.2)
        inner += _tube([k0, tp(0.28 * m["ww"], -26)], 4.5, rc, ow=2.2)
    if D.get("ash"):
        for fx, uy, r in ((-0.4, 0.3, 9), (0.5, 0.75, 7), (0.1, -0.9, 10)):
            c = tp(fx * m["ww"], uy * m["T"] * (0.6 if uy < 0 else 1))
            inner += _ell(c[0], c[1], r * 1.3, r, P["ash"], extra='opacity="0.55"')
    s += clip + f'<g clip-path="url(#{cid})">{inner}</g>'
    return s


def _band_edge(poly, p0, n, d):
    """Points along the chord (p - p0) . n = d of a convex polygon (2 points)."""
    pts = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n) - d, _dot(_sub(b, p0), n) - d
        if (da >= 0) != (db >= 0):
            pts.append(_lerp(a, b, da / (da - db)))
    return pts[:2]


# ---------------------------------------------------------------- head assembly


def _back_layer(D, st, ps):
    """Things hanging behind the body: head-cloth tail, veil drape, long Assyrian hair."""
    R, hw, Hc, ha = st["m"]["R"], st["hw"], st["Hc"], st["ha"]
    s = ""
    tail = D.get("tail")
    if tail:
        col, stripe = tail
        if D.get("wet"):
            col = shade(col, -0.08)
        A0 = hw(-0.78, 0.32)
        ang = ps["tail"] if ps["tail"] is not None else (-14 + 0.4 * ha)
        dirv = _dv(ang)
        nv = (-dirv[1], dirv[0])
        L, w0, w1 = 1.25 * R, 0.36 * R, 0.46 * R

        def q(a, b):
            return _add(_add(A0, _mul(dirv, a)), _mul(nv, b))
        pts = [q(-0.1 * R, -w0), q(-0.1 * R, w0), q(L * 0.6, w1 * 0.95), q(L, w1), q(L + 0.06 * R, 0),
               q(L, -w1), q(L * 0.6, -w1 * 0.95)]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
        if stripe:
            for a0 in (0.58, 0.76):
                quad = [q(L * a0, -w1 * 0.97), q(L * a0, w1 * 0.97), q(L * (a0 + 0.09), w1 * 0.99),
                        q(L * (a0 + 0.09), -w1 * 0.99)]
                s += _poly(quad, stripe, sw=2.2)
    if D.get("veil"):
        col = D["veil"]
        A0 = hw(-0.70, 0.10)
        A1 = hw(0.15, 0.25)
        bot = (A0[0] - 0.15 * R, A0[1] + 2.0 * R)
        pts = [hw(-0.95, -0.5), A0, (A0[0] - 0.55 * R, A0[1] + 1.0 * R), bot, (bot[0] + 0.9 * R, bot[1] - 0.2 * R),
               A1]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    if D.get("long_hair"):
        col = D["long_hair"]
        pts = [hw(-0.95, -0.3), hw(-1.20, 0.5), hw(-1.12, 1.25), hw(-0.40, 1.42), hw(0.05, 1.0), hw(-0.3, 0.2)]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
        curl = shade(col, 0.35)
        for (hx, hy) in ((-1.0, 0.75), (-0.75, 1.05), (-1.05, 1.15), (-0.45, 1.25), (-0.80, 0.45)):
            c = hw(hx, hy)
            s += (f'<path d="M{fmt(c[0] - 0.07 * R)},{fmt(c[1])} a{fmt(0.07 * R)},{fmt(0.07 * R)} 0 1 1 '
                  f'{fmt(0.10 * R)},{fmt(0.05 * R)}" fill="none" {_st(2.0, curl)}/>')
    if D.get("ponytail"):
        col = D["ponytail"]
        c = hw(-1.08, -0.15)
        s += _ell(c[0], c[1], 0.30 * R, 0.36 * R, col, sw=3.2)
    return s


def _head_svg(D, st, ps, expr):
    R, Hc, ha = st["m"]["R"], st["Hc"], st["ha"]
    skin = D["skin"]
    s = ""
    hair = D.get("hair")
    hat = D.get("hat")
    if D.get("ears", True):
        s += _ear(R, skin)
    s += _ell(0, 0, R, R * 0.97, skin, sw=OW)
    if hair:
        s += _hair_cap(R, hair, D.get("hair_style", "short"))
        if D.get("ears", True):
            s += _ear(R, skin)
    if D.get("ponytail"):
        s += _tube([(-0.60 * R, -0.55 * R), (-1.0 * R, -0.28 * R)], 0.16 * R, D.get("ribbon", P["terracotta"]),
                   ow=2.4)
    s += _face(R, skin, expr, ps["look"])
    if D.get("beard"):
        kind, bcol = D["beard"]
        s += _beard(R, bcol, kind)
        s += _mouth(R, EXPRS.get(expr, EXPRS["neutral"])["mouth"])
        s += _moustache(R, bcol, kind)
    if D.get("ash"):
        s += _ell(-0.30 * R, -0.62 * R, 0.25 * R, 0.13 * R, P["ash"], extra='opacity="0.6"')
        s += _ell(0.62 * R, 0.12 * R, 0.12 * R, 0.08 * R, P["ash"], extra='opacity="0.5"')
    if hat:
        kind = hat[0]
        if kind == "headcloth":
            col = hat[1]
            if D.get("wet"):
                col = shade(col, -0.08)
            s += _cloth_cap(R, col, edge=hat[2])
        elif kind == "veil":
            s += _cloth_cap(R, hat[1], edge=hat[2])
        elif kind == "headband":
            s += _headband(R, hat[1])
        elif kind == "knit":
            s += _knit_cap(R, hat[1])
        elif kind == "redcap":
            s += _red_cap(R, hat[1])
        elif kind == "crown":
            s += _crown(R, x0=0.05 * R, y0=-0.55 * R)
        elif kind == "wrap":
            s += _wrap(R, hat[1], hat[2] if len(hat) > 2 else None)
    if D.get("seaweed"):
        sw_ = smooth_path_pts([(0.35 * R, -1.08 * R), (-0.15 * R, -1.18 * R), (-0.62 * R, -0.95 * R),
                               (-1.0 * R, -0.55 * R), (-1.18 * R, -0.05 * R), (-1.05 * R, 0.45 * R)])
        s += _tube(sw_, 0.13 * R, P["leaf"], ow=2.4)
        for (hx, hy, a) in ((-0.30, -1.12, -60), (-0.92, -0.62, -120), (-1.16, 0.15, 160)):
            s += (f'<ellipse cx="{fmt(hx * R)}" cy="{fmt(hy * R)}" rx="{fmt(0.16 * R)}" ry="{fmt(0.07 * R)}" '
                  f'transform="rotate({a} {fmt(hx * R)} {fmt(hy * R)})" fill="{P["leaf_dark"]}" {_st(2.0)}/>')
    if D.get("wet"):
        for (hx, hy, k) in ((0.95, -0.15, 0.08), (-1.05, 0.75, 0.07)):
            s += _drop(hx * R, hy * R, k * R)
    return f'<g transform="translate({_pt(Hc)}) rotate({fmt(ha)})">{s}</g>'


def _marks(D, st, ps, expr):
    R, Hc = st["m"]["R"], st["Hc"]
    s = ""
    mk = ps["marks"]
    mcol = st["m"].get("mark_col", P["ink_soft"])
    if "shake" in mk:
        for sgn in (-1, 1):
            for k in (0, 1):
                cx = Hc[0] + sgn * (R * (1.30 + 0.25 * k))
                s += _line(f"M{fmt(cx)},{fmt(Hc[1] - 0.45 * R)} Q{fmt(cx + sgn * 0.14 * R)},{fmt(Hc[1])} "
                           f"{fmt(cx)},{fmt(Hc[1] + 0.45 * R)}", w=3.2, col=mcol)
    if "fan" in mk:
        W = st["arms"][ps["fan_arm"]][2]
        for k in range(3):
            r = 0.45 * R + k * 0.2 * R
            s += _line(f"M{fmt(W[0] + r * 0.9)},{fmt(W[1] - r * 0.5)} Q{fmt(W[0] + r * 1.15)},{fmt(W[1])} "
                       f"{fmt(W[0] + r * 0.9)},{fmt(W[1] + r * 0.5)}", w=2.6, col=mcol)
    if D.get("wet"):
        bodice, skirt = st["robe"]
        chain = [p for p in skirt if _dot(_sub(p, st["Hm"]), st["um"]) > -2]
        chain = sorted(chain, key=lambda p: p[0])
        if chain:
            for i, k in enumerate((0.1, 0.45, 0.85)):
                p = chain[int(k * (len(chain) - 1))]
                s += _drop(p[0], p[1] + 14 + 9 * (i % 2), 5.5)
        for (Sx, E, W) in st["arms"]:
            s += _drop(W[0], W[1] + 24, 4.5)
    return s


# ======================================================================= public API

def _wrap_out(inner, x, y, scale, facing, label):
    sx = scale * (1 if facing >= 0 else -1)
    return (f'<g transform="translate({fmt(x)},{fmt(y)}) scale({fmt(sx)},{fmt(scale)})" data-who="{label}">'
            f'<g filter="url(#wobble-fine)">{inner}</g></g>')


def _resolve_pose(pose, allowed, who):
    if pose not in allowed:
        raise ValueError(f"{who}: unknown pose {pose!r}; choose from {sorted(allowed)}")
    return dict(POSES[pose])


JONAH_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "sleep", "kneel_pray", "sit", "sit_sulk",
               "sit_faint", "sit_happy", "preach", "point", "arms_up", "fall", "float", "refuse", "confess",
               "listen", "wake")


def _jonah_design(wet=False):
    robe = P["jonah_robe"]
    if wet:
        robe = shade(robe, -0.10)
    return dict(robe=robe, sleeve=robe, hem_col=P["jonah_robe_dark"], cuff=P["jonah_robe_dark"],
                sash=P["jonah_sash"], skin=P["skin"], leg=P["skin"], hem=0.90,
                hat=("headcloth", P["headcloth"], P["headcloth_stripe"]),
                tail=(P["headcloth"], P["headcloth_stripe"]), ears=False,
                beard=("short", P["beard"]), neck_v=P["headcloth"], wet=wet, seaweed=wet)


def jonah(x, y, scale=1.0, facing=1, pose="stand", expr=None, wet=False):
    ps = _resolve_pose(pose, JONAH_POSES, "jonah")
    e = expr or ps["expr"]
    inner, _ = _figure(_jonah_design(wet), _ADULT, ps, e)
    return _wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")


# ---------------------------------------------------------------- sailors
SAILOR_POSES = ("stand", "scared", "throw", "carry", "pray", "point", "pull", "lift")
_SAILORS = [
    dict(stripe=("#4a78a8", P["headcloth"]), skin="#eab48c", hair="#4a2f1f", hair_style="curly",
         hat=("headband", "#c0533a"), beard=None),
    dict(stripe=("#c0533a", P["headcloth"]), skin="#b9805a", hair="#2f2420", hair_style="short",
         hat=("knit", "#3f6f9e"), beard=("stubble", "#2f2420")),
    dict(stripe=(P["jonah_sash"], P["headcloth"]), skin="#8d5a3b", hair="#2a201b", hair_style="curly",
         hat=("headband", "#e0a23c"), beard=None),
    dict(stripe=("#d9a03c", "#8a5a36"), skin="#f0c6a2", hair="#a0582e", hair_style="short",
         hat=("knit", P["grass_dark"]), beard=("full", "#a0582e")),
]


def _sailor_design(variant):
    v = _SAILORS[variant % 4]
    base, stripe = v["stripe"][1], v["stripe"][0]
    return dict(robe=base, sleeve=stripe, hem_col=stripe, stripes=(stripe, 22, 10), skin=v["skin"],
                leg=v["skin"], hem=0.50, sleeve_len=0.45, rope_belt="#b98a52", hair=v["hair"],
                hair_style=v["hair_style"], hat=v["hat"], beard=v["beard"], flare_k=0.6, hem_w=9)


_SAILOR_M = dict(_ADULT, lw=20.0)


def sailor(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None):
    ps = _resolve_pose(pose, SAILOR_POSES, "sailor")
    e = expr or ps["expr"]
    inner, _ = _figure(_sailor_design(variant), _SAILOR_M, ps, e)
    return _wrap_out(inner, x, y, scale, facing, f"sailor{variant}-{pose}")


# ---------------------------------------------------------------- captain
CAPTAIN_POSES = ("stand", "wake", "point", "worried")
_CAPTAIN_M = _metrics(_ADULT, 1.08, 1.18)


def _captain_design():
    return dict(robe="#efe2c4", sleeve="#3f6f9e", coat="#3f6f9e", coat_hem="#2f5680", hem_col="#2f5680",
                cuff="#2f5680", stripes=("#c0533a", 30, 6), skin="#dba27c", leg="#dba27c", hem=0.86,
                rope_belt="#8b5a35", hair="#b8b2a8", hair_style="short", hat=("redcap", "#c0533a"),
                beard=("full", "#c9c3b8"), coat_cut=0.30)


def captain(x, y, scale=1.0, facing=1, pose="stand", expr=None):
    ps = _resolve_pose("wake_other" if pose == "wake" else pose,
                       CAPTAIN_POSES[:1] + ("wake_other",) + CAPTAIN_POSES[2:], "captain")
    e = expr or ps["expr"]
    inner, _ = _figure(_captain_design(), _CAPTAIN_M, ps, e)
    return _wrap_out(inner, x, y, scale, facing, f"captain-{pose}")


# ---------------------------------------------------------------- king
KING_POSES = ("stand", "sit_throne", "sit_ashes", "kneel_pray", "remove_crown")
_KING_M = _metrics(_ADULT, 1.04, 1.08)
KING_HAIR = "#2f2622"


def _throne(st):
    """High-backed wooden throne with gold trim, drawn behind a seated figure."""
    m, pel, legs = st["m"], st["pel"], st["legs"]
    g = st["ground"] or 0
    K = legs[1][1]
    seat_y = pel[1] + m["seat"] * 0.75
    xb0, xb1 = pel[0] - m["ww"] - 34, pel[0] - m["ww"] + 18
    top = st["N"][1] - 60
    wood, wd = P["wood"], P["wood_dark"]
    cush = P["royal_light"]
    xm = (xb0 + xb1) / 2
    x_front = K[0] + 4
    s = ""
    # back legs + front legs with gold paw feet
    for xx in (xb0 + 10, x_front - 10):
        s += f'<rect x="{fmt(xx - 8)}" y="{fmt(seat_y)}" width="16" height="{fmt(g - seat_y - 8)}" rx="4" fill="{wd}" {_st(3.2)}/>'
        s += _ell(xx + 4, g - 7, 13, 7, GOLD, sw=2.8)
    s += (f'<rect x="{fmt(xb0 + 14)}" y="{fmt(seat_y + (g - seat_y) * 0.55)}" width="{fmt(x_front - xb0 - 30)}" '
          f'height="9" rx="3" fill="{wd}" {_st(2.6)}/>')
    # backrest
    s += (f'<path d="M{fmt(xb0)},{fmt(seat_y)} L{fmt(xb0)},{fmt(top + 26)} Q{fmt(xm)},{fmt(top - 16)} '
          f'{fmt(xb1)},{fmt(top + 26)} L{fmt(xb1)},{fmt(seat_y)} Z" fill="{wood}" {_st(OW)}/>')
    s += (f'<path d="M{fmt(xb0 + 10)},{fmt(seat_y - 14)} L{fmt(xb0 + 10)},{fmt(top + 32)} Q{fmt(xm)},'
          f'{fmt(top + 4)} {fmt(xb1 - 10)},{fmt(top + 32)} L{fmt(xb1 - 10)},{fmt(seat_y - 14)} Z" '
          f'fill="{cush}" {_st(2.6)}/>')
    for k in range(3):
        yy = top + 46 + k * 34
        if yy < seat_y - 20:
            s += f'<circle cx="{fmt(xm)}" cy="{fmt(yy)}" r="5" fill="{GOLD}" {_st(2.0)}/>'
    for xx in (xb0, xb1):
        s += f'<circle cx="{fmt(xx)}" cy="{fmt(top + 24)}" r="9" fill="{GOLD}" {_st(2.8)}/>'
    s += f'<circle cx="{fmt(xm)}" cy="{fmt(top - 16)}" r="11" fill="{GOLD}" {_st(2.8)}/>'
    # seat slab with gold edge + cushion
    s += (f'<rect x="{fmt(xb0 - 8)}" y="{fmt(seat_y - 6)}" width="{fmt(x_front - xb0 + 16)}" height="20" rx="7" '
          f'fill="{wood}" {_st(OW)}/>')
    s += _line(f"M{fmt(xb0 + 2)},{fmt(seat_y + 4)} L{fmt(x_front - 2)},{fmt(seat_y + 4)}", w=3, col=GOLD)
    return s


def _ash_heap(st):
    pel, g = st["pel"], st["ground"] or 0
    m = st["m"]
    w = 2.2 * m["th"] + 70
    cx = pel[0] + 0.35 * m["th"]
    d = (f"M{fmt(cx - w / 2)},{fmt(g)} Q{fmt(cx - w / 3)},{fmt(g - 26)} {fmt(cx - w / 8)},{fmt(g - 20)} "
         f"Q{fmt(cx)},{fmt(g - 34)} {fmt(cx + w / 6)},{fmt(g - 22)} Q{fmt(cx + w / 2.6)},{fmt(g - 24)} "
         f"{fmt(cx + w / 2)},{fmt(g)} Z")
    s = f'<path d="{d}" fill="{P["ash"]}" {_st(OW)}/>'
    for dx, dy in ((-0.3, -9), (0.05, -14), (0.32, -8), (-0.12, -6)):
        s += _ell(cx + dx * w, g + dy, 7, 3.5, shade(P["ash"], -0.2), extra='opacity="0.7"')
    return s


def _king_design(attire, pose, throne, ashes):
    sack = attire == "sackcloth"
    D = dict(skin="#d9a27a", leg="#d9a27a", hem=0.95, ears=False, long_hair=KING_HAIR, hair=KING_HAIR,
             hair_style="curly", beard=("assyrian", KING_HAIR), sandal=GOLD_DARK)
    if sack:
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], sandal=None, bare=True)
    else:
        D.update(robe=P["royal"], sleeve=P["royal"], hem_col=GOLD, fringe=GOLD, shawl=P["royal_light"],
                 shawl_trim=GOLD, cuff=GOLD, sash=GOLD, sash_tail=False, collar=GOLD, hem_w=11)
        if pose != "remove_crown":
            D.update(hat=("crown",), hat_h=1.75)
    if pose == "sit_throne" and throne:
        D["behind"] = _throne
    if pose == "sit_ashes" and ashes:
        D["behind"] = _ash_heap
    if pose == "remove_crown":
        def held(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            R = st["m"]["R"]
            c = _lerp(W0, W1, 0.5)
            s = f'<g transform="translate({_pt(c)}) rotate(-6)">{_crown(R, x0=0, y0=0.62 * R, k=0.8)}</g>'
            for W in (W0, W1):
                s += f'<circle cx="{fmt(W[0])}" cy="{fmt(W[1] + 4)}" r="{fmt(st["m"]["hr"])}" fill="{D["skin"]}" {_st(3.2)}/>'
            return s
        D["front"] = held
    return D


def king(x, y, scale=1.0, facing=1, pose="stand", attire="royal", expr=None, throne=True, ashes=True):
    ps = _resolve_pose(pose, KING_POSES, "king")
    if pose == "sit_throne":
        ps["anchor"] = "pelvis"
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose == "stand":
        e = "sad"
    D = _king_design(attire, pose, throne, ashes)
    if pose == "remove_crown":
        ps["arms"] = (("ik", "torso", 2.30, 0.50, 1), ("ik", "torso", 0.75, 0.50, 1))
    inner, _ = _figure(D, _KING_M, ps, e)
    return _wrap_out(inner, x, y, scale, facing, f"king-{pose}")


# ---------------------------------------------------------------- citizens
CITIZEN_POSES = ("stand", "walk", "walk_a", "walk_b", "listen", "kneel_pray", "point", "sad", "cheer")
CITIZEN_KINDS = ("man", "woman", "child", "elder")
_CIT_COL = [
    dict(robe="#d9b98a", trim=P["terracotta"], skin="#e2a77e", hair="#4a2f1f"),
    dict(robe=P["terracotta"], trim="#e8d3a8", skin="#c68a62", hair="#2f2420"),
    dict(robe=P["olive"], trim="#e0b25a", skin="#a46b47", hair="#2a201b"),
    dict(robe="#4b5a8f", trim="#e8d3a8", skin="#eab48c", hair="#5a3a24"),
]


def _citizen_design(kind, variant, attire):
    c = _CIT_COL[variant % 4]
    robe = c["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.22), skin=c["skin"], leg=c["skin"], hem=0.90,
             cuff=shade(robe, -0.22))
    if kind == "man":
        D.update(hair=c["hair"], hair_style="curly", beard=("assyrian_short", c["hair"]), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25), hat=("wrap", c["trim"], shade(c["trim"], -0.2))
                 if variant % 2 else None, long_hair=None if variant % 2 else c["hair"])
    elif kind == "woman":
        D.update(hair=c["hair"], hair_style="short", hat=("veil", c["trim"], shade(robe, -0.1)),
                 veil=c["trim"], ears=False, sash=shade(c["trim"], -0.15), sash_tail=True)
    elif kind == "child":
        girl = variant % 2 == 1
        D.update(hair=c["hair"], hair_style="short" if girl else "curly", hem=0.56, flare_k=0.9,
                 rope_belt=c["trim"], sleeve_len=0.55)
        if girl:
            D.update(ponytail=c["hair"], ribbon=c["trim"])
    elif kind == "elder":
        D.update(hair="#e4ddd0", hair_style="short", beard=("white", "#ece6da"), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25))
        if variant % 2:
            D.update(hat=("wrap", "#e8d3a8", c["trim"]))
    if attire == "sackcloth":
        for key in ("shawl", "shawl_trim", "sash", "hat"):
            D.pop(key, None)
        if kind == "woman":
            D.update(hat=("veil", P["sackcloth"], None), veil=P["sackcloth"])
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], bare=True)
    return D


def _cane(st):
    W = st["arms"][1][2]
    g = st["ground"] or 0
    return (_tube([(W[0] + 2, W[1] - 10), (W[0] + 8, g - 2)], 6, P["wood"], ow=2.6) +
            _tube([(W[0] + 2, W[1] - 10), (W[0] - 8, W[1] - 16)], 6, P["wood"], ow=2.6))


def citizen(x, y, scale=1.0, facing=1, kind="man", variant=0, pose="stand", attire="normal", expr=None):
    if kind not in CITIZEN_KINDS:
        raise ValueError(f"citizen: unknown kind {kind!r}")
    pose_key = "listen_chin" if pose == "listen" else pose
    ps = _resolve_pose(pose_key, CITIZEN_POSES + ("listen_chin",), "citizen")
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose in ("stand", "walk", "walk_a", "walk_b"):
        e = "sad"
    D = _citizen_design(kind, variant, attire)
    m = _ADULT
    if kind == "child":
        m = _CHILD
    elif kind == "woman":
        m = _metrics(_ADULT, 0.96, 0.92)
    elif kind == "elder":
        m = _metrics(_ADULT, 0.97, 1.0)
        if pose in ("stand", "walk", "walk_a", "walk_b", "sad", "listen"):
            ps["t"] = ps["t"] + 8
            if pose != "listen":
                ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
                D["front"] = _cane
    inner, _ = _figure(D, m, ps, e)
    return _wrap_out(inner, x, y, scale, facing, f"{kind}{variant}-{pose}")
