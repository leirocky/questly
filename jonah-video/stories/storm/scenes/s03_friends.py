"""Scene 3 - Mark 1:16-20, 3:13-19. A bright morning by the Sea of Galilee: Jesus walks along the beach with his
twelve friends while a number badge counts them 1..12; a picture-book 'porthole' opens from the four fishermen in the
line onto the lake, where they used to fish every day: Peter and Andrew in one boat, James and John in the other.
Each is named in turn (a little name ribbon pops up, he hops and smiles); John casts his round net, Peter hauls a net
full of flapping fish, fish leap round the boats. Then a picture-book map of the lake unfolds over the hills: fish
spots pop up on '哪里鱼多', wind lines rush down from the hills on '什么时候起风', and the four fishermen nod proudly.

Beats (syllable onsets measured in the voice clip with the Noah film's voice_marks helpers, so a re-generated voice
stays in sync; nothing is hard-coded to the take):
  0 .. 4.2     calm wide beach page: Jesus leads the twelve along the shore (planted-foot strides, footsteps),
               clouds drift, birds fly, the lake ripples
  '十二个'      the badge counts 1..12 left to right along the line (pop each; every counted friend gives a little
               hop); on '门徒' the badge bounces at 12 and a '门徒' ribbon unfurls (chime)
  end of line  the line stops (squash-dip pose cuts); Jesus turns back to his friends, smiling
  '当中'        the four fishermen at the front hop one after another (sparkles)
  '有好几个'    a round porthole opens from the four and grows over the page (ink ring, whoosh) onto the lake with
               the two fishing boats; the rowers row, the boats bob, gulls fly
  名字           '彼得' '安得烈' '雅各' '约翰': each fisherman's name ribbon pops up on his name, he hops / bounces with
               a smile (pop)
  '每天'        Peter starts hauling his net full of flapping fish on the stern deck (drips, rope creak)
  '撒网'        John swings and casts his round net: it flies open on '网' and lands on the water (splash)
  '捕鱼'        fish leap out of the water round the boats (small splashes); Peter's catch lands on his deck
  '他们最熟悉'   the camera eases back; a parchment map of the lake unfolds over the hills (cloth / whoosh)
  '哪里鱼多'    four fish spots pop up on the map, one per syllable (sparkle)
  '什么时候起风' three wind lines rush down from the hills on '时' '候' '起' (wind), a gust ruffles the water
  '他们都知道'   the four fishermen nod proudly one after another
  end          calm hold (page dip to s04)
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine import raster
from engine.motion import Cam, Tf
from engine.scene import BOIL_TOKEN, Scene
from stories.joseph.scenes.s03_coat import step_walk
from stories.noah.scenes.s01_title import char_times, cuts, snap, voice_marks

INK = P["ink"]
CREAM = "#fff6e3"

# ---- shared backdrop: the lake (sky, hills, lake), seen from the beach
LY, LS = 760, 0.5               # lake_galilee near shoreline and scale
YF = LY - 250 * LS              # far shoreline (the horizon line of the water)

# ---- shot A: the walk along the beach
KA = 0.62                       # everyone's scale on the beach
GY = 1010                       # ground line on the beach
J_END = 1700                    # Jesus' x when the line stops
GAPS = [0, 92] + [60] * 11      # Jesus, then Peter .. Judas behind him (stage px)

# ---- shot B: the two fishing boats
BP = (480, 960, 0.6, -1)        # Peter & Andrew's boat: x, waterline y, scale, facing (bow left)
BJ = (1640, 830, 0.52, 1)       # James & John's boat (farther away, bow right)
DECK_X, DECK_Y = -600, -172     # standing on the raised stern deck (local boat coords)

# ---- the map
MAP = (930, 362, 0.74)          # centre, scale


for _e in ("warm", "smile", "happy", "awed", "amazed", "kind", "calm", "neutral", "laugh"):
    if _e in C.EXPRS:
        C.EXPRS.setdefault(f"st_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def blink(expr):
    return f"st_blink_{expr}"


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def f1(v):
    return f"{v:.1f}"


# ================================================================== timing helpers (shared with s13 / s14)


class Beats:
    """Onset times measured in the voice clips: at(li, text, k) = onset of character k of ``text`` in line li."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.marks = [voice_marks(ctx, i) for i in range(len(ctx.lines))]

    def phrase(self, li, text):
        for m in self.marks[li]:
            if text in m[0] or m[0] in text:
                return m
        ln = self.ctx.lines[li]
        return (text, ln.start, ln.end, [(ln.start, ln.end)])

    def at(self, li, text, k=0):
        m = self.phrase(li, text)
        ct = char_times(m)
        j = (m[0].index(text) if text in m[0] else 0) + k
        return ct[min(max(j, 0), len(ct) - 1)]

    def end(self, li, text):
        return self.phrase(li, text)[2]


def clamp_cam(c, w=W, h=H):
    """Keep the camera viewport inside the painted stage."""
    cw = min(c.w, w, h * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2), w - cw / 2), min(max(c.y, ch / 2), h - ch / 2), cw, c.rot)


def cam_path(keys, curves, w=W, h=H):
    f = M.cam_keys([(t, clamp_cam(c, w, h)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), w, h)


def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def hop(t0, s, piv, height=26.0, dur=0.42):
    """A happy little hop starting at t0 (squash, lift, land)."""
    def m(t):
        u = t - t0
        if u < -0.1 or u > dur + 0.16:
            return Tf()
        if u < 0:
            k = (u + 0.1) / 0.1
            return Tf(dy=4 * s * k, sy=1 - 0.05 * k, px=piv[0], py=piv[1])
        if u < dur:
            v = u / dur
            return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.04 * math.sin(math.pi * v),
                      px=piv[0], py=piv[1])
        k = 1 - (u - dur) / 0.16
        return Tf(dy=3 * s * math.sin(math.pi * k), sy=1 - 0.035 * math.sin(math.pi * k), px=piv[0], py=piv[1])
    return m


def breath(piv, period=2.8, amount=0.011, phase=0.0):
    return lambda t: Tf(sx=1 + 0.4 * amount * math.sin(2 * math.pi * (t / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * (t / period + phase)), px=piv[0], py=piv[1])


def blink_entries(base_entries, times, base_of, blink_of):
    """Add 0.13 s blinks (frame indices from base_of / blink_of(current base)) at the given times where no other cut
    is within 0.3 s."""
    ents = list(base_entries)
    for tb in times:
        tb = snap(tb)
        if all(abs(tb - tk) > 0.3 for tk, _ in ents):
            cur = None
            for tk, i in sorted(ents):
                if tk <= tb:
                    cur = i
            if cur is not None and cur in blink_of:
                ents += [(tb, blink_of[cur]), (snap(tb + 0.13), cur)]
    return sorted(ents)


# ================================================================== figures


def disc(x, y, k, facing=1, v=0, pose="stand", expr=None, phase=0.0, wet=False, h=0.0, t=0.0, look=None,
         marks=True, net=True, oar=True, wind=0.0, shadow=False):
    """characters.disciples with an optional extra head tilt h (+ = bowed: a nod), torso lean t and look."""
    sh = C.ground_shadow(x, y, k, 120, 0.2) if shadow else ""
    if not h and not t and look is None:
        return sh + C.disciples(x, y, k, facing, variant=v, pose=pose, expr=expr, phase=phase, wet=wet, marks=marks,
                                net=net, oar=oar, wind=wind)
    vi = C._disciple_index(v)
    D, m = C._disciple_design(vi, C._clamp01(wind), wet)
    ps, _tip = C._disciple_pose(pose, phase)
    ps = dict(ps)
    ps["h"] = ps.get("h", 0) + h
    ps["t"] = ps.get("t", 0) + t
    if look is not None:
        ps["look"] = look
    fronts = []
    if pose == "row" and oar:
        fronts.append(C._oar_front(D, phase))
    elif pose == "haul_net" and net:
        fronts.append(C._net_haul_front(D, phase))
    elif pose == "cast_net" and net:
        fronts.append(C._net_cast_front(D, phase))
    D["front"] = C._hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, m, ps, e, C._fsign(facing), marks)
    return sh + C._wrap_out(inner, x, y, k, facing, f"disciple{vi}-{pose}-{h:.0f}-{t:.0f}")


def jes(x, y, k, facing=1, pose="stand", expr=None, h=0.0, t=0.0, look=None, shadow=False, **kw):
    """characters.jesus with an optional extra head tilt / lean."""
    sh = C.ground_shadow(x, y, k, 120, 0.2) if shadow else ""
    if not h and not t and look is None:
        return sh + C.jesus(x, y, k, facing, pose=pose, expr=expr, **kw)
    ps = dict(C._jesus_pose(pose, kw.get("phase", 0.0)))
    ps["h"] = ps.get("h", 0) + h
    ps["t"] = ps.get("t", 0) + t
    if look is not None:
        ps["look"] = look
    D = C._jesus_design(pose, C._clamp01(kw.get("glow", 0.0)), kw.get("cushion", True), C._clamp01(kw.get("wind", 0.0)),
                        kw.get("mantle", True))
    e = expr or ps["expr"]
    inner, _ = C._figure(D, C._JESUS_M, ps, e, C._fsign(facing), kw.get("marks", True))
    return sh + C._wrap_out(inner, x, y, k, facing, f"jesus-{pose}-{h:.0f}-{t:.0f}")


# ================================================================== labels


def ribbon_svg(x, y, text, size=46, col="#c0623f", gid="s3rib"):
    """A little picture-book name ribbon (cream banner with notched tails) centred on (x, y)."""
    n = len(text)
    w = size * (n * 1.02 + 1.3)
    h = size * 1.32
    x0, x1, y0, y1 = x - w / 2, x + w / 2, y - h / 2, y + h / 2
    tail = size * 0.62
    b = ""
    for sx in (-1, 1):                      # folded tails behind the band
        ex = x + sx * (w / 2 - size * 0.25)
        fx = x + sx * (w / 2 + tail)
        b += S.path(f"M{f1(ex)},{f1(y0 + h * 0.28)} L{f1(fx)},{f1(y0 + h * 0.28)} L{f1(fx - sx * size * 0.32)},"
                    f"{f1(y + h * 0.34)} L{f1(fx)},{f1(y1 + h * 0.36)} L{f1(ex)},{f1(y1 + h * 0.36)} Z",
                    fill=S.shade(col, -0.18), sw=3.2)
    b += S.path(f"M{f1(x0)},{f1(y0)} Q{f1(x)},{f1(y0 - size * 0.16)} {f1(x1)},{f1(y0)} L{f1(x1)},{f1(y1)} "
                f"Q{f1(x)},{f1(y1 - size * 0.16)} {f1(x0)},{f1(y1)} Z", fill=col, sw=3.6)
    b += S.path(f"M{f1(x0 + 8)},{f1(y0 + 7)} Q{f1(x)},{f1(y0 - size * 0.16 + 7)} {f1(x1 - 8)},{f1(y0 + 7)}",
                stroke=False, extra=f'stroke="{S.shade(col, 0.45)}" stroke-width="2.4" fill="none" '
                                    f'stroke-dasharray="7 6" stroke-linecap="round"')
    b = S.g(b, filter="wobble-fine")
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b += (f'<text x="{f1(x)}" y="{f1(y + size * 0.35)}" {font} fill="{CREAM}" stroke="{S.shade(col, -0.5)}" '
          f'stroke-width="5" stroke-linejoin="round" paint-order="stroke">{text}</text>')
    return b


def badge_svg(n, x, y, r=60, size=78):
    """The counting badge: a cream disc with a dashed lake-blue ring and a warm number."""
    if n <= 0:
        return doc("")
    defs = S.lin_grad("s3bg", [(0, "#ef8f4a"), (1, "#c4552c")])
    b = (f'<circle cx="{x + 4}" cy="{y + 7}" r="{r}" fill="{INK}" opacity="0.22" filter="url(#soft)"/>'
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffaf0" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="{x}" cy="{y}" r="{r - 11}" fill="none" stroke="#6fa8c0" stroke-width="4" '
         f'stroke-dasharray="9 7"/>')
    b = S.g(b, filter="wobble-fine")
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{size}" text-anchor="middle"'
    b += (f'<text x="{x}" y="{y + size * 0.36:.0f}" {font} fill="url(#s3bg)" stroke="{INK}" stroke-width="3" '
          f'paint-order="stroke">{n}</text>')
    return doc(b, defs)


def pop_motion(t0, piv, dur=0.4, out_t=None, out_dur=0.35, bob_amp=3.0, bob_per=2.2):
    """Pop in at t0 with an overshoot, float gently, optionally fade out at out_t."""
    def m(t):
        if t < t0:
            return Tf(alpha=0)
        u = min(1.0, (t - t0) / dur)
        k = 0.3 + 0.7 * M.ease("back")(u)
        a = min(1.0, (t - t0) / 0.1)
        if out_t is not None:
            a *= 1 - M.progress(t, out_t, out_t + out_dur, "sine")
        return Tf(sx=k, sy=k, alpha=a, dy=bob_amp * math.sin(2 * math.pi * (t - t0) / bob_per), px=piv[0], py=piv[1])
    return m


# ================================================================== backdrop drawings


def lake_back_svg():
    return doc(PR.lake_galilee(-20, W + 20, LY, LS, time="day", part="back", top=-60))


def clouds_svg(k):
    """Two small extra clouds that drift (the lake's own clouds stay put)."""
    b = (S.cloud(560 + 0 * k, 200, 220, 64, "#fbf6ec", seed=81, sw=3, shade_fill="#d8eaf0") +
         S.cloud(1500, 120, 180, 54, "#fbf6ec", seed=82, sw=2.8, shade_fill="#d8eaf0"))
    return doc(S.g(b, filter="wobble"))


def shore_svg():
    """Shot A: the near beach with the fishing village, and foreground grass / pebbles."""
    b = PR.lake_galilee(-20, W + 20, LY, LS, time="day", part="shore", village="left", bottom=H + 60)
    return doc(b)


def tufts_svg(k):
    sw = (-0.5, 0.0, 0.5)[k]
    out = ""
    for x, y, s, v in ((60, 1196, 1.0, 2), (420, 1190, 0.8, 0), (900, 1200, 0.9, 1), (1380, 1196, 0.8, 2),
                       (1860, 1192, 1.0, 0), (2080, 1186, 0.9, 1), (250, 1110, 0.5, 1), (1990, 1100, 0.5, 2)):
        out += PR.grass_tuft(x, y, s, variant=v, sway=sw)
    return doc(out)


def water_svg():
    """Shot B: the open lake from the far shoreline down (a calm day lake with ripples)."""
    return doc(PR.calm_lake(-20, W + 20, YF + 2, time="day", scale=0.6, sparkle=0.5, seed=5, bottom=H + 60))


def band_svg(bx, by, k, phase=0.0):
    """The same lake clipped to a strip in front of a hull (hides the keel and the oar blades below the waterline)."""
    x0, x1 = bx - 800 * k, bx + 800 * k
    top = S.wave_line(by - 3 * k, 2.5 * k, 110 * k, 2 * math.pi * phase, x0=x0, x1=x1)
    d = top + f" L{f1(x1)},{f1(by + 90 * k)} L{f1(x0)},{f1(by + 90 * k)} Z"
    cid = f"s3band{int(bx)}{int(phase * 100)}"
    lake = PR.calm_lake(-20, W + 20, YF + 2, time="day", scale=0.6, sparkle=0.0, seed=5, bottom=H + 60, ripples=1.0)
    hi = (f'<path d="{S.wave_line(by - 3 * k, 2.5 * k, 110 * k, 2 * math.pi * phase, x0=bx - 700 * k, x1=bx + 700 * k)}" '
          f'fill="none" stroke="#eef8f4" stroke-width="{3.4 * k / 0.6:.1f}" opacity="0.75" stroke-linecap="round"/>')
    return doc(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{lake}</g>' +
               S.g(hi, filter="wobble"))


def boat_part(b, part, row=None, wet=False, lantern=False):
    """One of the shot-B boats: back (furled sail, stern deck free for a fisherman) or front (+ one rower's oar)."""
    bx, by, k, f = b
    if part == "back":
        return PR.fishing_boat(bx, by, k, f, sail="furled", part="back", oars="none", cushion=False, wet=wet)
    out = PR.fishing_boat(bx, by, k, f, sail="furled", part="front", oars="none", nets=True, wet=wet, lantern=lantern)
    if row is not None:                           # the outboard part of the rower's oar (seat 1)
        sx, sy = PR.BOAT_SEATS[1]
        o = PR._oar_svg(row, (0.0, 0.0), part="out")
        out += PR._place(f'<g transform="translate({sx},{sy}) scale(-1,1)">{o}</g>', bx, by, k, f)
    return out


def boat_pt(b, lx, ly):
    bx, by, k, f = b
    return (bx + lx * k * f, by + ly * k)


def net_water_svg(x, y, k):
    """John's cast net lying on the water: a flat ring of cork floats with mesh, a few bubbles."""
    rx, ry = 150 * k, 26 * k
    d = (f"M{f1(x - rx)},{f1(y)} Q{f1(x - rx)},{f1(y - ry)} {f1(x)},{f1(y - ry)} Q{f1(x + rx)},{f1(y - ry)} "
         f"{f1(x + rx)},{f1(y)} Q{f1(x + rx)},{f1(y + ry)} {f1(x)},{f1(y + ry)} Q{f1(x - rx)},{f1(y + ry)} "
         f"{f1(x - rx)},{f1(y)} Z")
    b = f'<path d="{d}" fill="{S.mix(PR.NET, "#7fb4cc", 0.45)}" fill-opacity="0.55"/>'
    b += PR._net_mesh(d, "s3netw", 10 * k / 0.5, col=S.shade(PR.NET, -0.2), sw=1.4)
    b += f'<path d="{d}" fill="none" stroke="{S.shade(PR.NET, -0.35)}" stroke-width="2.4"/>'
    for i in range(12):
        a = 2 * math.pi * i / 12
        b += (f'<ellipse cx="{f1(x + rx * math.cos(a))}" cy="{f1(y + ry * math.sin(a))}" rx="{f1(9 * k)}" '
              f'ry="{f1(6 * k)}" fill="{PR.NET_FLOAT}" stroke="{INK}" stroke-width="2.2"/>')
    b += (f'<path d="{S.wave_line(y + ry + 8 * k, 2, 50, 0, x0=x - rx * 1.2, x1=x + rx * 1.2)}" fill="none" '
          f'stroke="#eef8f4" stroke-width="3" opacity="0.7"/>')
    return doc(S.g(b, filter="wobble-fine"))


def splash_svg(x, y, k, seed=0):
    """A small splash: a flat ripple ring and a crown of drops (scaled / faded by its motion)."""
    rng = random.Random(seed)
    b = (f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(70 * k)}" ry="{f1(14 * k)}" fill="none" stroke="#f4f8f1" '
         f'stroke-width="5" opacity="0.9"/>'
         f'<ellipse cx="{f1(x)}" cy="{f1(y)}" rx="{f1(44 * k)}" ry="{f1(8 * k)}" fill="none" stroke="#f4f8f1" '
         f'stroke-width="3.5" opacity="0.8"/>')
    for i in range(7):
        a = math.pi * (0.15 + 0.7 * i / 6)
        r = rng.uniform(40, 70) * k
        dx, dy = r * math.cos(a), -r * math.sin(a) * 1.2
        b += (f'<ellipse cx="{f1(x - dx)}" cy="{f1(y + dy)}" rx="{f1(7 * k)}" ry="{f1(10 * k)}" fill="#f4f8f1" '
              f'stroke="{S.shade("#7fb4cc", -0.3)}" stroke-width="2"/>')
    return doc(S.g(b, filter="wobble-fine"))


def drips_svg(x, y, k, ph):
    """Water dripping from Peter's hauled net (falling drops; ph 0..1 loops)."""
    b = ""
    for i in range(5):
        u = (ph + i / 5) % 1.0
        dx = (-50 + 25 * i) * k
        yy = y + 90 * k * u
        b += (f'<path d="M{f1(x + dx)},{f1(yy - 9 * k)} Q{f1(x + dx + 6 * k)},{f1(yy + 3 * k)} {f1(x + dx)},'
              f'{f1(yy + 6 * k)} Q{f1(x + dx - 6 * k)},{f1(yy + 3 * k)} {f1(x + dx)},{f1(yy - 9 * k)} Z" '
              f'fill="#cfe8ee" stroke="{S.shade("#7fb4cc", -0.35)}" stroke-width="1.8" opacity="{1 - u * 0.6:.2f}"/>')
    return doc(b)


# ================================================================== the map


def map_base_svg():
    x, y, s = MAP
    sh = (f'<rect x="{x - 440 * s + 12}" y="{y - 320 * s + 16}" width="{880 * s}" height="{650 * s}" rx="30" '
          f'fill="{INK}" opacity="0.22" filter="url(#soft)"/>')
    title = ribbon_svg(x, y - 322 * s, "加利利湖", 40, "#4f8aa8")
    return doc(sh + PR.lake_map(x, y, s, fish=False, wind=0.0, boat=False, labels=False) + title)


def map_spot_svg(i, wig):
    x, y, s = MAP
    fx, fy = ((-60, -110), (70, -40), (-80, 90), (90, 130))[i]
    w = math.sin(2 * math.pi * wig + i)
    body = (f'<circle cx="{fx}" cy="{fy}" r="32" fill="#bfe0ea" fill-opacity="0.55" stroke="#4f8aa8" '
            f'stroke-width="3" stroke-dasharray="7 6"/>'
            f'<g transform="translate({fx},{fy}) rotate({8 * w:.1f})">{PR._lake_fish(w, 0.5)}</g>')
    return doc(PR._place(body, x, y, s, 1))


def map_wind_svg(i, ph):
    x, y, s = MAP
    wx, wy, a = ((260, -150, 200), (290, 60, 190), (-290, -100, -20))[i]
    sx = 1 if a > 90 else -1
    off = 10 * math.sin(2 * math.pi * ph + i)
    body = (S.path(f"M{wx},{f1(wy + off)} q{-sx * 50},-14 {-sx * 100},0 q{-sx * 24},6 {-sx * 14},-20", stroke=False,
                   extra='stroke="#5f7fa6" stroke-width="5" stroke-linecap="round" fill="none"') +
            S.path(f"M{wx + sx * 10},{f1(wy + 26 + off)} q{-sx * 40},-10 {-sx * 80},0", stroke=False,
                   extra='stroke="#5f7fa6" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.8"') +
            S.path(f"M{wx - sx * 4},{f1(wy - 22 + off)} q{-sx * 26},-6 {-sx * 52},0", stroke=False,
                   extra='stroke="#5f7fa6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.7"'))
    return doc(PR._place(body, x, y, s, 1))


def map_boat_svg():
    x, y, s = MAP
    return doc(PR._place(PR._place(PR._small_boat(1, "full", False, "day"), 0, 10, 0.16, 1, filt=None), x, y, s, 1))


# ================================================================== iris (porthole) helpers


def layer_bbox(svgs):
    """Union alpha bbox of the rasterised frames (the compositor crops a layer to exactly this)."""
    bb = None
    for s in svgs:
        im = raster.rasterize(s.replace(BOIL_TOKEN, "1"), W, H)
        b = im.getchannel("A").getbbox()
        if b:
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    return bb


def iris_reveal(bb, cx, cy, radius, t0, t1, soft=34):
    """Radial reveal of one layer whose crop box is bb, so that every layer shares the same circle radius(t)."""
    x0, y0, x1, y1 = bb
    maxd = max(math.hypot(px - cx, py - cy) for px in (x0, x1) for py in (y0, y1)) or 1.0

    def rv(t):
        if t >= t1:
            return {"mode": "up", "frac": 1.0}
        return {"mode": "radial", "frac": max(0.0, radius(t)) / maxd, "soft": soft, "cx": cx, "cy": cy}
    return rv


def iris_ring(cx, cy, radius, t0, t1):
    """The porthole's rim drawn in output space: a cream band with ink edges, growing with radius(t)."""
    from PIL import Image, ImageDraw

    def fx(frame, t, view):
        if not (t0 <= t <= t1):
            return frame
        r = radius(t)
        if r <= 2:
            return frame
        ox, oy = view.to_out(cx, cy)
        R = r * view.scale
        a = 1.0 - M.progress(t, t1 - 0.25, t1, "sine")
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        bw = min(max(6, 15 * view.scale), R * 0.2)
        if R < 12:
            return frame
        d.ellipse([ox - R - bw, oy - R - bw, ox + R + bw, oy + R + bw], outline=(75, 52, 38, int(220 * a)),
                  width=max(2, int(4 * view.scale)))
        d.ellipse([ox - R - bw + 3, oy - R - bw + 3, ox + R + bw - 3, oy + R + bw - 3],
                  outline=(255, 246, 227, int(235 * a)), width=max(2, int(bw * 1.6)))
        d.ellipse([ox - R + bw * 0.6, oy - R + bw * 0.6, ox + R - bw * 0.6, oy + R - bw * 0.6],
                  outline=(75, 52, 38, int(170 * a)), width=max(2, int(3 * view.scale)))
        frame.alpha_composite(ov)
        return frame
    return fx


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    B = Beats(ctx)

    # ------------------------------------------------------------ beats
    t_twelve = B.at(0, "十二")
    t_mentu = B.at(0, "门徒")
    t_dang = B.at(1, "当中")
    t_you = B.at(1, "有好几个")
    t_da = B.at(1, "打鱼")
    t_names = [B.at(1, "彼得"), B.at(1, "安得烈"), B.at(1, "雅各和约翰"), B.at(1, "约翰")]
    t_meitian = B.at(1, "每天")
    t_sa = B.at(1, "撒网")
    t_bu = B.at(1, "捕鱼")
    t_yu = B.at(1, "捕鱼", 1)
    t_l2 = ctx.lines[2].start
    t_hu = B.at(2, "这个湖")
    t_spots = [B.at(2, "哪里鱼多", k) for k in range(4)]
    t_wind = [B.at(2, "什么时候起风", k) for k in (2, 3, 4)]
    t_zhidao = B.at(2, "他们都知道")
    t_stop = 4.2

    # ------------------------------------------------------------ backdrop (shared by both shots)
    sc.add("lake_back", lake_back_svg(), z=0, wc=0.8)
    sc.add("clouds", clouds_svg(0), z=1, motion=M.drift(vx=9))
    wings = (1, .5, 0, -.5, -1, -.5, 0, .5)
    for i, (col, y0, vx, ph_, t0) in enumerate((("blue", 230, 70, 0.0, 0.0), ("yellow", 300, 62, 0.4, 0.3),
                                                ("blue", 190, -66, 0.2, 9.0))):
        def fly(t, y0=y0, vx=vx, ph_=ph_, t0=t0, i=i):
            x = (-200 + 260 * i if vx > 0 else W + 200) + vx * (t - t0)
            return Tf(dx=x - 200, dy=y0 - 200 + 20 * math.sin(2 * math.pi * (t / 2.3 + ph_)),
                      alpha=1.0 if t >= t0 else 0.0)
        sc.add(f"bird{i}", [doc(PR.songbird(200, 200, 0.36, 1 if vx > 0 else -1, wing=w, color=col)) for w in wings],
               z=2 + 0.01 * i, motion=fly, wc=0.3, frame_at=lambda t, ph_=ph_: float(int(t / 0.07 + ph_ * 8) % 8))

    # ------------------------------------------------------------ shot A: the walk
    t_iris0 = snap(t_you + 0.1)
    t_iris1 = snap(max(t_da + 0.3, t_iris0 + 0.95))
    a_alpha = lambda t: Tf(alpha=0.0 if t > t_iris1 + 0.05 else 1.0)        # noqa: E731
    sc.add("shore", shore_svg(), z=3, motion=a_alpha)
    sc.add("tufts", [tufts_svg(k) for k in range(3)], z=30,
           frame_at=lambda t: float((0, 1, 2, 1)[int(t / 0.5) % 4]),
           motion=a_alpha)

    period, n_steps, t_w0 = 0.3, 15, -0.3
    wfa, wdx, wdy, t_wend = step_walk(t_w0, n_steps, 44, period, KA)
    t_stop = t_wend
    xs_end, acc = [], J_END
    for gap in GAPS:
        acc -= gap
        xs_end.append(acc)
    # walker order: 0 = Jesus, 1..12 = Peter .. Judas
    count_order = list(range(12, 0, -1))          # counted left to right: Judas first, Peter last
    pop0, pop1 = t_twelve - 0.06, max(t_mentu + 0.15, t_twelve + 1.7)
    pop_t = {w: snap(pop0 + (pop1 - pop0) * i / 11) for i, w in enumerate(count_order)}
    t_four = [snap(t_dang + 0.02 + 0.12 * i) for i in range(4)]

    for wi in range(13):
        x_end = xs_end[wi]
        x0 = x_end - wdx(1e9)
        parity = wi % 2
        gy = GY + 8 if wi % 2 == 0 else GY - 16          # two loose rows: the line reads as a friendly group
        k = KA if wi % 2 == 0 else KA * 0.97
        if wi == 0:
            fr = [jes(x0, gy, k, 1, "walk_a", shadow=True), jes(x0, gy, k, 1, "walk_b", shadow=True),
                  jes(x_end, gy, k, 1, "stand", "warm", shadow=True),
                  jes(x_end, gy, k, -1, "stand", "warm", shadow=True),
                  jes(x_end, gy, k, -1, "stand", blink("warm"), shadow=True)]
            ents = [(-1, 0), (t_stop, 3)]
            ents = blink_entries(ents, [t_stop + 1.1, t_stop + 2.6], None, {3: 4})
        else:
            v = wi - 1
            fr = [disc(x0, gy, k, 1, v, "walk_a", shadow=True), disc(x0, gy, k, 1, v, "walk_b", shadow=True),
                  disc(x_end, gy, k, 1, v, "stand", "happy", shadow=True),
                  disc(x_end, gy, k, 1, v, "stand", blink("happy"), shadow=True),
                  disc(x_end, gy, k, 1, v, "stand", "smile" if v < 4 else "happy", shadow=True)]
            ents = [(-1, 0), (t_stop, 2)]
            if v < 4:
                ents.append((t_four[v], 4))
            ents = blink_entries(ents, [t_stop + 0.7 + 0.37 * (v % 5)], None, {2: 3})
        base_fa = cuts(ents)

        def fa(t, base_fa=base_fa, parity=parity):
            w = wfa(t)
            if w is not None:
                return float(int(w) ^ parity)
            return base_fa(t)

        def walk_m(t):
            # the walk frames are drawn at the start x, the stand frames at the end x
            return Tf(dx=wdx(t), dy=wdy(t)) if t < t_stop else Tf()

        piv = (x_end, gy)
        mots = [walk_m, squash(t_stop, k, piv, 6), a_alpha,
                lambda t, wi=wi, gy=gy: Tf(sy=1 + 0.011 * math.sin(2 * math.pi * (t / (2.6 + 0.13 * (wi % 4)) + 0.17 * wi)),
                                           px=x_end, py=gy)]
        if wi > 0:
            mots.append(hop(pop_t[wi], k, piv, 16, 0.3))
            if wi - 1 < 4:
                mots.append(hop(t_four[wi - 1], k, piv, 30, 0.4))
        sc.add(f"walker{wi}", [doc(x) for x in fr], frame_at=fa, z=(10.5 if wi % 2 == 0 else 10) + 0.01 * (13 - wi),
               seed=200 + 7 * wi, motion=M.combine(*mots))

    # ------------------------------------------------------------ camera (defined here: the badge rides with it)
    camB = Cam(1056, 682, 1800)
    camW = Cam(W / 2, 600, 1950)
    cam = cam_path([
        (0, Cam(700, 794, 1400)), (t_stop, Cam(1290, 790, 1420)), (t_iris0 + 0.1, Cam(1430, 780, 1320)),
        (t_iris1 + 0.15, Cam(1250, 720, 1600)), (t_names[0] - 0.2, camB), (t_meitian, camB),
        (t_bu + 0.2, Cam(1060, 690, 1760)), (t_yu + 0.45, Cam(1060, 690, 1760)), (t_hu - 0.15, camW),
        (T, Cam(W / 2, 604, 1930))],
        ["sine", "inout", "inout", "inout", "sine", "sine", "sine", "inout", "sine"])
    sc.camera = cam

    # badge + '门徒' ribbon (they ride with the camera, above the line)
    bx_, by_ = W / 2, 300
    t_badge_out = t_iris0 - 0.1

    def cam_lock(t):
        c = cam(t)
        return Tf(dx=c.x - bx_, dy=c.y - c.w * 9 / 32 + 150 - by_)

    def count(t):
        return sum(1 for tp in pop_t.values() if t >= tp)

    def badge_m(t):
        t_first = min(pop_t.values())
        if t < t_first:
            return Tf(alpha=0)
        a = min(1.0, (t - t_first) / 0.12) * (1 - M.progress(t, t_badge_out, t_badge_out + 0.35, "sine"))
        s = 1.0
        for tp in pop_t.values():
            u = t - tp
            if 0 <= u < 0.16:
                s = max(s, 1 + 0.16 * math.sin(math.pi * u / 0.16))
        u = t - (pop1 + 0.05)
        if 0 <= u < 0.4:
            s = max(s, 1 + 0.3 * math.sin(math.pi * u / 0.4))
        return Tf(sx=s, sy=s, alpha=a, dy=3 * math.sin(2 * math.pi * t / 2.6), px=bx_, py=by_)
    sc.add("badge", [badge_svg(n, bx_, by_) for n in range(13)], z=60, wc=0, frame_at=lambda t: float(count(t)),
           motion=M.combine(badge_m, cam_lock))
    t_rib = snap(t_mentu - 0.05)
    sc.add("rib_mentu", doc(ribbon_svg(bx_, by_ + 112, "门徒", 44, "#4f8aa8")), z=60.1, wc=0,
           motion=M.combine(pop_motion(t_rib, (bx_, by_ + 112), out_t=t_badge_out, bob_amp=2.5), cam_lock))
    cb = cam(pop1)
    sbx, sby = cb.x, cb.y - cb.w * 9 / 32 + 150
    sc.fx.append(FX.sparkles((sbx - 120, sby - 90, sbx + 120, sby + 160), count=7, t0=pop1, t1=pop1 + 1.2,
                             size=(9, 18), period=1.0, drift=-14, seed=31))
    fx_ = J_END - 95 - 96
    sc.fx.append(FX.sparkles((fx_ - 170, GY - 300 * KA, fx_ + 170, GY - 120 * KA), count=9, t0=t_four[0] - 0.05,
                             t1=t_iris1, size=(9, 17), period=0.8, drift=-16, seed=33))

    # ------------------------------------------------------------ shot B: the fishing boats (revealed by the iris)
    icx, icy = J_END - 95 - 96, GY - 130
    iris_r = lambda t: 1850 * M.progress(t, t_iris0, t_iris1, "inout")      # noqa: E731
    b_layers = []

    def add_b(name, svg, z, **kw):
        frames = svg if isinstance(svg, (list, tuple)) else [svg]
        mot = kw.pop("motion", None)
        vis = lambda t: Tf(alpha=0.0 if t < t_iris0 else 1.0)              # noqa: E731
        sc.add(name, list(frames) if len(frames) > 1 else frames[0], z=z,
               motion=M.combine(vis, mot) if mot else vis, **kw)
        b_layers.append((sc.layers[-1], frames))

    add_b("water", water_svg(), 40, seed=401, wc=0.9)
    sc.fx.append(FX.sparkles((60, 1010, W - 60, H - 30), count=10, t0=t_iris1, color=(255, 252, 235),
                             size=(6, 13), period=2.2, drift=0, seed=41))
    sc.fx.append(FX.sparkles((60, YF + 14, W - 60, YF + 70), count=8, t0=t_iris1, color=(255, 252, 235),
                             size=(5, 10), period=2.4, drift=0, seed=42))

    def boat_motion(b, per, ph, amp=3.0, deg=0.8):
        bx, by, k, f = b

        def m(t):
            u = 2 * math.pi * (t / per + ph)
            return Tf(dy=amp * math.sin(u), rot=deg * math.sin(u + 0.9), px=bx, py=by)
        return m

    # rowing: 8 phases at 0.2 s (a calm stroke), pausing on the rower's name and while nodding
    row_ph = [i / 8 for i in range(8)]
    names_x = []

    # ---------------- James & John's boat (far)
    mJ = boat_motion(BJ, 3.4, 0.3)
    add_b("boatJ_back", doc(boat_part(BJ, "back")), 41, motion=mJ)
    jx, jy = boat_pt(BJ, DECK_X, DECK_Y)
    kJ = BJ[2]
    # John: ready (net gathered), name hop, cast phases, stand watching, nods
    cast_ph = (0.0, 0.2, 0.4, 0.55, 0.7, 0.85, 0.93, 1.0)
    jn_fr = [disc(jx, jy, kJ, -1, "john", "cast_net", "happy", phase=0.0),
             disc(jx, jy, kJ, -1, "john", "cast_net", "smile", phase=0.0),
             disc(jx, jy, kJ, -1, "john", "cast_net", blink("happy"), phase=0.0)]
    JC0 = len(jn_fr)
    jn_fr += [disc(jx, jy, kJ, -1, "john", "cast_net", "happy", phase=p) for p in cast_ph]
    JS = len(jn_fr)
    jn_fr += [disc(jx, jy, kJ, -1, "john", "stand", "happy"), disc(jx, jy, kJ, -1, "john", "stand", blink("happy")),
              disc(jx, jy, kJ, -1, "john", "stand", "smile", h=16), disc(jx, jy, kJ, -1, "john", "stand", "smile")]
    t_cast0 = snap(t_sa - 0.62)
    cast_dt = [0.16, 0.13, 0.11, 0.09, 0.08, 0.08, 0.12]
    cast_t = [t_cast0]
    for d_ in cast_dt:
        cast_t.append(snap(cast_t[-1] + d_))
    t_land = snap(cast_t[-1] + 0.3)
    jn_ents = [(-1, 0), (snap(t_names[3] - 0.04), 1), (snap(t_names[3] + 1.0), 0)]
    jn_ents += [(tc, JC0 + i) for i, tc in enumerate(cast_t)]
    jn_ents.append((t_land, JS))
    t_nods = [snap(t_zhidao + 0.02 + 0.13 * i) for i in range(4)]
    nod_seq = lambda tn: [(tn, JS + 2), (snap(tn + 0.27), JS + 3), (snap(tn + 0.55), JS + 2),   # noqa: E731
                          (snap(tn + 0.82), JS + 3)]
    jn_ents += nod_seq(t_nods[1])
    jn_ents = blink_entries(jn_ents, [7.2, 11.4, t_land + 1.6, t_l2 + 2.2], None, {0: 2, JS: JS + 1})
    jpiv = (jx, jy)
    add_b("john", [doc(x) for x in jn_fr], 43, frame_at=cuts(jn_ents), seed=431,
          motion=M.combine(mJ, hop(t_names[3], kJ, jpiv, 30), squash(t_land, kJ, jpiv, 6), breath(jpiv, 2.5)))
    names_x.append(("约翰", jx, jy - 345 * kJ - 30, t_names[3], "#77a063"))
    # James rowing at seat 1 (faces the stern = John)
    sjx, sjy = boat_pt(BJ, *PR.BOAT_SEATS[1])
    ja_fr = [disc(sjx, sjy, kJ, -1, "james", "row", "happy", phase=p) for p in row_ph]
    ja_fr += [disc(sjx, sjy, kJ, -1, "james", "row", "smile", phase=0.25),
              disc(sjx, sjy, kJ, -1, "james", "row", "smile", phase=0.25, h=14)]
    names_x.append(("雅各", sjx + 30, sjy - 300 * kJ - 30, t_names[2], "#8b4a5c"))

    def rower_fa(t_name, t_nod, nodk, row_off):
        def fa(t):
            if t_name - 0.05 <= t < t_name + 1.05:
                return 8.0
            if t_nod <= t < t_nod + 1.1:
                k = int((t - t_nod) / 0.27)
                return 9.0 if k % 2 == 0 else 8.0
            if t < t_iris1 + 0.2:
                return 2.0
            return float(int((t - t_iris1) / 0.2 + row_off) % 8)
        return fa
    ja_fa = rower_fa(t_names[2], t_nods[3], 9, 3)
    add_b("james", [doc(x) for x in ja_fr], 42.5, frame_at=ja_fa, seed=425,
          motion=M.combine(mJ, hop(t_names[2], kJ, (sjx, sjy), 12, 0.36)))
    add_b("boatJ_front", [doc(boat_part(BJ, "front", row=p)) for p in row_ph] + [doc(boat_part(BJ, "front", row=0.25))],
          44, frame_at=lambda t: ja_fa(t) if ja_fa(t) < 8 else 2.0, motion=mJ, seed=441)
    add_b("bandJ", band_svg(BJ[0], BJ[1], kJ), 45, seed=401, wc=0.9, wc_edge=0.0)

    # ---------------- Peter & Andrew's boat (near)
    mP = boat_motion(BP, 3.0, 0.0, 3.4, 0.9)
    add_b("boatP_back", doc(boat_part(BP, "back")), 50, motion=mP)
    kP = BP[2]
    px_, py_ = boat_pt(BP, DECK_X, DECK_Y)
    px2 = boat_pt(BP, DECK_X + 60, DECK_Y)[0]           # after the catch he steps back a little
    haul_ph = [i / 8 for i in range(8)]
    pe_fr = [disc(px_, py_, kP, 1, "peter", "stand", "happy"), disc(px_, py_, kP, 1, "peter", "stand", "smile"),
             disc(px_, py_, kP, 1, "peter", "stand", blink("happy"))]
    PH0 = len(pe_fr)
    pe_fr += [disc(px_, py_, kP, 1, "peter", "haul_net", "laugh", phase=p) for p in haul_ph]
    PS = len(pe_fr)
    pe_fr += [disc(px2, py_, kP, 1, "peter", "stand", "happy"), disc(px2, py_, kP, 1, "peter", "stand", blink("happy")),
              disc(px2, py_, kP, 1, "peter", "stand", "smile", h=16), disc(px2, py_, kP, 1, "peter", "stand", "smile")]
    t_haul0 = snap(t_meitian - 0.05)
    t_catch = snap(max(t_yu + 0.55, t_land + 0.3))
    pe_ents = [(-1, 0), (snap(t_names[0] - 0.04), 1), (snap(t_names[0] + 1.0), 0), (t_catch, PS)]

    def pe_haul(t):
        if t_haul0 <= t < t_catch:
            return float(PH0 + int((t - t_haul0) / 0.085) % 8)
        return None
    pe_ents += [(tn, i - JS + PS) for tn, i in nod_seq(t_nods[0])]
    pe_ents = blink_entries(pe_ents, [8.9, t_catch + 1.3, t_l2 + 3.0], None, {0: 2, PS: PS + 1})
    pe_base = cuts(pe_ents)
    ppiv = (px_, py_)
    add_b("peter", [doc(x) for x in pe_fr], 52, frame_at=lambda t: pe_haul(t) if pe_haul(t) is not None else pe_base(t), seed=521,
          motion=M.combine(mP, hop(t_names[0], kP, ppiv, 30), squash(t_haul0, kP, ppiv, 6),
                           squash(t_catch, kP, ppiv, 7), breath(ppiv, 2.7, phase=0.3)))
    names_x.append(("彼得", px_ + 10, py_ - 345 * kP - 34, t_names[0], "#3f7282"))
    # the catch on the deck after hauling (a net bag of flapping fish)
    cx_, cy_ = boat_pt(BP, -700, -172 - 150)
    catch_fr = [doc(PR.net_full(cx_, cy_, kP * 0.95, -1, phase=p)) for p in (0.0, 0.33, 0.66)]
    add_b("catch", catch_fr, 51.5, frame_at=lambda t: float(int(t / 0.14) % 3),
          motion=M.combine(mP, lambda t: Tf(alpha=1.0 if t >= t_catch else 0.0)))
    # drips under the hauled net
    bag_x = px_ + (190 + 20) * kP
    bag_y = py_ + 30 * kP
    add_b("drips", [drips_svg(bag_x, bag_y, kP, p) for p in (0.0, 0.25, 0.5, 0.75)], 52.5,
          frame_at=lambda t: float(int(t / 0.09) % 4), wc=0.3,
          motion=M.combine(mP, lambda t: Tf(alpha=1.0 if t_haul0 + 0.3 <= t < t_catch else 0.0)))
    # Andrew rowing at seat 1 (faces the stern = Peter)
    sax, say = boat_pt(BP, *PR.BOAT_SEATS[1])
    an_fr = [disc(sax, say, kP, 1, "andrew", "row", "happy", phase=p) for p in row_ph]
    an_fr += [disc(sax, say, kP, 1, "andrew", "row", "smile", phase=0.25),
              disc(sax, say, kP, 1, "andrew", "row", "smile", phase=0.25, h=14)]
    an_fa = rower_fa(t_names[1], t_nods[2], 9, 0)
    add_b("andrew", [doc(x) for x in an_fr], 51, frame_at=an_fa, seed=511,
          motion=M.combine(mP, hop(t_names[1], kP, (sax, say), 12, 0.36)))
    names_x.append(("安得烈", sax - 10, say - 300 * kP - 34, t_names[1], "#c9a86a"))
    add_b("boatP_front", [doc(boat_part(BP, "front", row=p)) for p in row_ph], 53,
          frame_at=lambda t: an_fa(t) if an_fa(t) < 8 else 2.0, motion=mP, seed=531)
    add_b("bandP", band_svg(BP[0], BP[1], kP, 0.3), 54, seed=401, wc=0.9, wc_edge=0.0)

    # iris: every shot-B layer reveals with the same circle
    for layer, frames in b_layers:
        bb = layer_bbox([f for f in layer.frames])
        if bb:
            layer.reveal = iris_reveal(bb, icx, icy, iris_r, t_iris0, t_iris1)
    sc.fx.append(iris_ring(icx, icy, iris_r, t_iris0, t_iris1 + 0.02))

    # ---------------- John's net on the water, splashes, leaping fish
    lx, ly = jx - 300 * kJ, BJ[1] + 22
    sc.add("net_water", net_water_svg(lx, ly, kJ), z=46, wc=0.6,
           motion=M.combine(lambda t: Tf(alpha=M.progress(t, t_land - 0.04, t_land + 0.12, "sine")),
                            M.bob(1.5, 2.6, 0.2)))

    def splash_m(t0, piv, dur=0.7):
        def m(t):
            u = (t - t0) / dur
            if u < 0 or u > 1:
                return Tf(alpha=0)
            return Tf(sx=0.5 + 0.9 * u, sy=0.5 + 0.9 * u, alpha=1 - u * u, px=piv[0], py=piv[1])
        return m
    sc.add("splash_net", splash_svg(lx, ly, kJ * 1.4, 3), z=46.5, wc=0, motion=splash_m(t_land - 0.02, (lx, ly)))
    # leaping fish: (start x, water y, distance, height, t0, dur, facing, scale)
    fishes = [(bag_x - 40, BP[1] + 18, -150, 150, snap(t_bu - 0.05), 0.85, -1, 0.75),
              (lx + 90, BJ[1] + 30, 140, 120, snap(t_yu + 0.1), 0.8, 1, 0.62),
              (bag_x + 140, BP[1] + 24, 130, 130, snap(t_yu + 0.75), 0.8, 1, 0.7),
              (1180, 1010, -120, 110, snap(t_l2 + 0.6), 0.8, -1, 0.75)]
    for i, (fx0, fy0, dist, hgt, ft0, fdur, ff, fk) in enumerate(fishes):
        fr = [doc(PR.lake_fish(300, 300, fk, ff, flap=fl)) for fl in (-0.8, 0.0, 0.8)]

        def fish_m(t, fx0=fx0, fy0=fy0, dist=dist, hgt=hgt, ft0=ft0, fdur=fdur, ff=ff):
            u = (t - ft0) / fdur
            if u < 0 or u > 1:
                return Tf(alpha=0)
            x = fx0 + dist * u
            y = fy0 - hgt * 4 * u * (1 - u)
            ang = math.degrees(math.atan2(-hgt * 4 * (1 - 2 * u), dist)) * (1 if ff > 0 else -1)
            if ff < 0:
                ang = -math.degrees(math.atan2(-hgt * 4 * (1 - 2 * u), -dist))
            return Tf(dx=x - 300, dy=y - 300, rot=ang, px=300, py=300)
        sc.add(f"fish{i}", fr, z=55 + 0.1 * i, frame_at=lambda t, i=i: float(int(t / 0.07 + i) % 3), motion=fish_m,
               wc=0.5)
        sc.add(f"fsplash{i}a", splash_svg(fx0, fy0, 0.42, 10 + i), z=55.05 + 0.1 * i, wc=0,
               motion=splash_m(ft0 - 0.03, (fx0, fy0), 0.55))
        sc.add(f"fsplash{i}b", splash_svg(fx0 + dist, fy0, 0.42, 20 + i), z=55.05 + 0.1 * i, wc=0,
               motion=splash_m(ft0 + fdur - 0.04, (fx0 + dist, fy0), 0.6))

    # ---------------- name ribbons
    t_rib_out = t_l2 - 0.2
    for k, (text, rx, ry, tn, col) in enumerate(names_x):
        sc.add(f"name{k}", doc(ribbon_svg(rx, ry, text, 40, col)), z=70 + 0.1 * k, wc=0,
               motion=pop_motion(snap(tn - 0.06), (rx, ry), out_t=t_rib_out + 0.08 * k, bob_amp=2.5,
                                 bob_per=2.0 + 0.2 * k))
        sc.fx.append(FX.sparkles((rx - 110, ry - 60, rx + 110, ry + 50), count=5, t0=tn - 0.05, t1=tn + 0.9,
                                 size=(8, 15), period=0.8, drift=-12, seed=60 + k))

    # ------------------------------------------------------------ the map
    mx, my, ms = MAP
    t_map = snap(t_hu - 0.12)

    def map_m(t):
        if t < t_map:
            return Tf(alpha=0)
        u = min(1.0, (t - t_map) / 0.6)
        k = 0.15 + 0.85 * M.ease("back")(u)
        return Tf(sx=k, sy=k, rot=-7 * (1 - M.ease("out")(u)), alpha=min(1.0, (t - t_map) / 0.15),
                  dy=-30 * (1 - M.ease("out")(u)), px=mx, py=my)
    float_m = lambda t: Tf(dy=3 * math.sin(2 * math.pi * (t - t_map) / 3.1))     # noqa: E731
    sc.add("map", map_base_svg(), z=80, wc=0.7, motion=M.combine(map_m, float_m))
    sc.add("map_boat", map_boat_svg(), z=80.5, wc=0.4,
           motion=M.combine(map_m, float_m, lambda t: Tf(dx=26 * ms * math.sin(2 * math.pi * (t - t_map) / 5.0),
                                                       rot=2 * math.sin(2 * math.pi * t / 1.7))))
    for i, ts in enumerate(t_spots):
        sx_, sy_ = mx + ((-60, 70, -80, 90)[i]) * ms, my + ((-110, -40, 90, 130)[i]) * ms
        fr = [map_spot_svg(i, w) for w in (0.0, 0.25, 0.5, 0.75)]
        sc.add(f"spot{i}", fr, z=81 + 0.1 * i, wc=0.4, frame_at=lambda t, i=i: float(int(t / 0.16 + i) % 4),
               motion=M.combine(pop_motion(snap(ts - 0.04), (sx_, sy_), 0.35, bob_amp=0), float_m))
        sc.fx.append(FX.sparkles((sx_ - 50, sy_ - 50, sx_ + 50, sy_ + 40), count=4, t0=ts - 0.04, t1=ts + 0.8,
                                 size=(7, 13), period=0.7, drift=-10, seed=70 + i))
    for i, tw in enumerate(t_wind):
        fr = [map_wind_svg(i, p) for p in (0.0, 0.33, 0.66)]
        sx_dir = ("right", "right", "left")[i]
        t0w = snap(tw - 0.06)

        def wind_rv(t, t0w=t0w, sx_dir=sx_dir):
            f = M.progress(t, t0w, t0w + 0.4, "out")
            return {"mode": sx_dir, "frac": f, "soft": 18}
        sc.add(f"wind{i}", fr, z=82 + 0.1 * i, wc=0, frame_at=lambda t, i=i: float(int(t / 0.22 + i) % 3),
               reveal=wind_rv, motion=M.combine(lambda t, t0w=t0w: Tf(alpha=1.0 if t >= t0w else 0.0), float_m))

    # ------------------------------------------------------------ sound
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-17, fade_in=0.8, fade_out=1.2)
    sc.sfx("birds", 0, dur=T + 0.3, gain_db=-20, fade_in=0.8, fade_out=1.2)
    sc.sfx("footsteps", 0, dur=t_stop + 0.1, gain_db=-16, pan=0.2, fade_in=0.4)
    for w, tp in pop_t.items():
        sc.sfx("pop", tp, gain_db=-17, pan=-0.6 + 1.2 * (12 - w) / 12)
    sc.sfx("chime", pop1, gain_db=-15)
    for i, tf_ in enumerate(t_four):
        sc.sfx("pop", tf_, gain_db=-18, pan=0.4)
    sc.sfx("sparkle", t_four[0], gain_db=-17, pan=0.4)
    sc.sfx("whoosh", t_iris0, gain_db=-12)
    sc.sfx("oars", t_iris1, dur=T - t_iris1 + 0.3, gain_db=-21, fade_in=0.6, fade_out=1.0)
    for k, (_, rx, _, tn, _) in enumerate(names_x):
        sc.sfx("pop", tn, gain_db=-14, pan=-0.8 + 1.6 * rx / W)
    sc.sfx("cloth", t_haul0, gain_db=-16, pan=-0.2)
    sc.sfx("whoosh", cast_t[3], gain_db=-14, pan=0.3)
    sc.sfx("splash", t_land - 0.02, gain_db=-11, pan=0.2)
    for i, (fx0, _, dist, _, ft0, fdur, _, _) in enumerate(fishes):
        sc.sfx("splash_small", ft0, gain_db=-15, pan=-0.8 + 1.6 * fx0 / W)
        sc.sfx("splash_small", ft0 + fdur, gain_db=-16, pan=-0.8 + 1.6 * (fx0 + dist) / W)
    sc.sfx("thud", t_catch, gain_db=-14, pan=-0.3)
    sc.sfx("cloth", t_map, gain_db=-12)
    sc.sfx("whoosh", t_map + 0.05, gain_db=-16)
    for i, ts in enumerate(t_spots):
        sc.sfx("pop", ts, gain_db=-15, pan=-0.2 + 0.15 * i)
    sc.sfx("sparkle", t_spots[0], gain_db=-18)
    sc.sfx("wind_soft", t_wind[0] - 0.1, dur=1.8, gain_db=-12, fade_in=0.2, fade_out=0.8)
    sc.sfx("chime", t_zhidao + 0.1, gain_db=-17)
    return sc
