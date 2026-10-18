"""Shared picture-book art style: palette, SVG document wrapper, filters, shape helpers.

Look: warm watercolour/gouache picture book. Soft rounded shapes, gentle
gradients, umber (not black) outlines with a hand-drawn wobble, cream paper.
Every layer is a complete <svg> sized to the stage (default 2112 x 1188).
Use ``svg_doc(body)`` so all layers share the same filters and defs.
"""
import math
import random

from engine.paths import STAGE_H, STAGE_W
from engine.scene import BOIL_TOKEN

W, H = STAGE_W, STAGE_H

# ------------------------------------------------------------------ palette
P = {
    # paper & ink
    "paper": "#f4ead5", "paper_dark": "#e6d6b4", "ink": "#4b3426", "ink_soft": "#7a5a40",
    # skies
    "sky_day": "#bfe2ea", "sky_day_top": "#8fcbe0", "sky_warm": "#f8dfb4", "sky_dawn": "#f6c7a0",
    "sky_dawn_top": "#c9b6d9", "sky_sunset": "#f3a873", "sky_sunset_top": "#b87fa5",
    "storm_sky": "#5b6b80", "storm_sky_top": "#2f3a4d", "storm_cloud": "#46536a", "storm_cloud_light": "#7d8aa0",
    "night": "#1f2b45", "night_light": "#3a4c6e",
    # sea
    "sea_deep": "#21587a", "sea": "#3a86a8", "sea_light": "#7fc1d0", "sea_pale": "#b9e0e3", "foam": "#f4f8f1",
    "storm_sea": "#2c4d60", "storm_sea_light": "#4f7a8c",
    "underwater": "#2b6f8f", "underwater_deep": "#163f5c",
    # land
    "sand": "#ebc98f", "sand_dark": "#c99b5d", "sand_light": "#f5e2b8",
    "grass": "#93b85c", "grass_dark": "#628d3e", "olive": "#7d9148", "earth": "#a8794c",
    "stone": "#dcbf92", "stone_dark": "#b8946a", "stone_light": "#efdcb8", "terracotta": "#c9714a",
    "wood": "#a0683e", "wood_dark": "#74462a", "wood_light": "#c58c5a", "sail": "#f2e6cc", "sail_stripe": "#c9714a",
    # light
    "gold": "#f2c14e", "glow": "#fff2c4", "sun": "#fbd46b", "sun_hot": "#f6a43c",
    # Jonah
    "jonah_robe": "#d9893c", "jonah_robe_dark": "#b06a2a", "jonah_sash": "#3b8b89",
    "headcloth": "#efe2c4", "headcloth_stripe": "#9b6b43",
    "skin": "#eab48c", "skin_shadow": "#d39570", "beard": "#6e4529", "cheek": "#f0998a",
    # fish
    "fish": "#4a87a8", "fish_light": "#9fd0d6", "fish_belly": "#e9efdc", "fish_dark": "#2e6280",
    "fish_spot": "#6fb0c4", "mouth_inside": "#9c3f4e",
    # Nineveh
    "royal": "#7b4f9d", "royal_light": "#a17cc0", "crown": "#e8b63c",
    "sackcloth": "#b59c74", "sackcloth_dark": "#8f7754", "ash": "#9a9188",
    # plants & creatures
    "leaf": "#6ea84b", "leaf_dark": "#457a32", "leaf_light": "#9ccc6a", "leaf_dry": "#b89b52",
    "leaf_dead": "#9a7a45", "worm": "#d99fb2", "worm_dark": "#b06f88",
}

INK = P["ink"]
STROKE = f'stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
STROKE_THIN = f'stroke="{INK}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"'
STROKE_THICK = f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'

# ------------------------------------------------------------------ document


def _filters():
    s = BOIL_TOKEN
    return f"""
<filter id="wobble" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="{s}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="wobble-fine" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{s}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="3.5" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="wobble-strong" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.009" numOctaves="3" seed="{s}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur-md" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
<filter id="blur-lg" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="wash" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.006 0.012" numOctaves="3" seed="7" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 0.75" result="m"/>
  <feComposite in="SourceGraphic" in2="m" operator="in" result="lit"/>
  <feBlend in="SourceGraphic" in2="lit" mode="multiply"/>
</filter>
"""


def svg_doc(body, defs="", w=W, h=H):
    """Wrap SVG body markup into a full document with the shared filters."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"<defs>{_filters()}{defs}</defs>{body}</svg>")


def g(body, transform=None, filter=None, opacity=None, extra=""):
    attrs = ""
    if transform:
        attrs += f' transform="{transform}"'
    if filter:
        attrs += f' filter="url(#{filter})"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    return f"<g{attrs} {extra}>{body}</g>"


# ------------------------------------------------------------------ colour


def hex_rgb(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(r, g_, b):
    return "#%02x%02x%02x" % (int(max(0, min(255, r))), int(max(0, min(255, g_))), int(max(0, min(255, b))))


def mix(c1, c2, t):
    a, b = hex_rgb(c1), hex_rgb(c2)
    return rgb_hex(*(a[i] + (b[i] - a[i]) * t for i in range(3)))


def shade(c, k):
    """k < 0 darkens toward ink, k > 0 lightens toward paper."""
    return mix(c, P["ink"] if k < 0 else "#fffaf0", abs(k))


# ------------------------------------------------------------------ gradients


def lin_grad(id_, stops, x1=0, y1=0, x2=0, y2=1):
    """stops: list of (offset 0..1, colour[, opacity])."""
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a[0] if a else 1}"/>' for o, c, *a in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad_grad(id_, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a[0] if a else 1}"/>' for o, c, *a in stops)
    f = (f' fx="{fx}"' if fx is not None else "") + (f' fy="{fy}"' if fy is not None else "")
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>'


# ------------------------------------------------------------------ paths


def fmt(v):
    return f"{v:.1f}"


def smooth_path(pts, closed=True, tension=1.0):
    """Catmull-Rom spline through points -> SVG path data (cubic Béziers)."""
    n = len(pts)
    if n < 2:
        return ""
    d = f"M{fmt(pts[0][0])},{fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d += f" C{fmt(c1[0])},{fmt(c1[1])} {fmt(c2[0])},{fmt(c2[1])} {fmt(p2[0])},{fmt(p2[1])}"
    return d + (" Z" if closed else "")


def blob(cx, cy, rx, ry, wobble=0.1, n=10, seed=0, rot=0.0):
    """Organic closed shape around an ellipse (path data)."""
    r = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + math.radians(rot)
        k = 1 + r.uniform(-wobble, wobble)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return smooth_path(pts)


def wave_band(y, amp, wavelength, phase=0.0, x0=-60, x1=W + 60, bottom=H + 60, step=None, jitter=0.0, seed=0):
    """Filled body of water whose top edge is a soft wave (path data)."""
    r = random.Random(seed)
    step = step or wavelength / 4
    pts = []
    x = x0
    while x <= x1 + step:
        yy = y + amp * math.sin(2 * math.pi * (x / wavelength) + phase) + r.uniform(-jitter, jitter)
        pts.append((x, yy))
        x += step
    d = smooth_path(pts, closed=False)
    return d + f" L{fmt(pts[-1][0])},{fmt(bottom)} L{fmt(pts[0][0])},{fmt(bottom)} Z"


def wave_line(y, amp, wavelength, phase=0.0, x0=-60, x1=W + 60, step=None):
    """Open wavy line (for foam / crest highlights)."""
    step = step or wavelength / 4
    pts = []
    x = x0
    while x <= x1 + step:
        pts.append((x, y + amp * math.sin(2 * math.pi * (x / wavelength) + phase)))
        x += step
    return smooth_path(pts, closed=False)


def cloud(cx, cy, w, h, fill="#fbf3e6", seed=0, puffs=5, sw=4, shade_fill=None):
    """Puffy picture-book cloud (SVG markup): overlapping circles with one outer outline.

    Drawn twice — stroked circles first, then fill-only circles on top — so only the
    outer silhouette keeps its ink line. Optional ``shade_fill`` adds a soft underside.
    """
    r = random.Random(seed)
    circles = []
    for i in range(puffs):
        u = (i + 0.5) / puffs
        rad = h * (0.42 + 0.35 * math.sin(math.pi * u)) * r.uniform(0.85, 1.12)
        x = cx - w / 2 + w * u + r.uniform(-w * 0.03, w * 0.03)
        y = cy + h * 0.18 - rad * 0.55 + r.uniform(-h * 0.06, h * 0.06)
        circles.append((x, y, rad))
    base = (cx, cy + h * 0.2, w * 0.52, h * 0.32)
    def shapes(attrs):
        out = f'<ellipse cx="{fmt(base[0])}" cy="{fmt(base[1])}" rx="{fmt(base[2])}" ry="{fmt(base[3])}" {attrs}/>'
        for x, y, rad in circles:
            out += f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(rad)}" {attrs}/>'
        return out
    body = shapes(f'fill="{fill}" stroke="{INK}" stroke-width="{sw * 2}"') + shapes(f'fill="{fill}"')
    if shade_fill:
        body += (f'<ellipse cx="{fmt(base[0])}" cy="{fmt(base[1] + base[3] * 0.25)}" rx="{fmt(base[2] * 0.9)}" '
                 f'ry="{fmt(base[3] * 0.55)}" fill="{shade_fill}" opacity="0.55"/>')
    return body


def hill(x0, x1, y, peak, seed=0, bottom=H + 60, bumps=3):
    """Rolling hill silhouette from x0 to x1 with a top around y-peak (path data)."""
    r = random.Random(seed)
    pts = [(x0, y)]
    for i in range(1, bumps * 2):
        u = i / (bumps * 2)
        pts.append((x0 + (x1 - x0) * u, y - peak * math.sin(math.pi * u) * r.uniform(0.75, 1.1)))
    pts.append((x1, y))
    d = smooth_path(pts, closed=False)
    return d + f" L{fmt(x1)},{fmt(bottom)} L{fmt(x0)},{fmt(bottom)} Z"


def rays(cx, cy, r0, r1, n=12, width_deg=7, rot=0.0):
    """Wedge-shaped light rays from a centre (path data, fill it with a glow colour)."""
    d = ""
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        wa = math.radians(width_deg / 2)
        p = [(cx + r0 * math.cos(a - wa / 3), cy + r0 * math.sin(a - wa / 3)),
             (cx + r1 * math.cos(a - wa), cy + r1 * math.sin(a - wa)),
             (cx + r1 * math.cos(a + wa), cy + r1 * math.sin(a + wa)),
             (cx + r0 * math.cos(a + wa / 3), cy + r0 * math.sin(a + wa / 3))]
        d += "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in p) + " Z "
    return d


def path(d, fill="none", stroke=True, sw=4, extra=""):
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}" {st} {extra}/>'


def rect_bg(fill, w=W, h=H):
    return f'<rect x="-20" y="-20" width="{w + 40}" height="{h + 40}" fill="{fill}"/>'


def text(x, y, s, size=96, fill=None, weight="bold", anchor="middle", extra=""):
    fill = fill or P["ink"]
    return (f'<text x="{x}" y="{y}" font-family="LXGW WenKai" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')
