"""Scene 5 - John 6:8-9. On the golden hillside above the lake Jesus asks the disciples how many loaves they have; they
search the standing crowd (shading their eyes, peering into baskets, people opening empty hands); Andrew, Peter's
brother, comes back leading a small boy with his little lunch basket. Andrew lifts the open basket: five barley
loaves and two small fish (a picture-book count pops them one by one), looks at the huge crowd and doubts. The basket
goes back to the boy (a gloss card: one little basket = one boy's full tummy); the boy looks up at Jesus and gives
him his lunch with both hands; Jesus bends and takes it, smiling; the boy beams.

One wide stage (the lake_hillside world at the golden hour, time 0.55, the same place as s03-s08); the neighbours
are page-turn dips, so only calm first / last frames are needed. lake_hillside is drawn with trees=False: the trees
(TREES5) stand in gaps between the crowd clusters on their own layers, and trees and clusters are depth-sorted (z from
their ground y), so no group is ever painted over a tree in front of it.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks through the Nativity film's
beat(); nothing hard-coded to the take). Times are for the current take:
  0 .. 0.9      Jesus with Peter, Andrew, James, John and Philip on the grass, the crowd standing on the slope
  '你们' 0.95    Jesus turns to them and asks (ask, gentle_question); the disciples listen, worried
  '去' 2.36      'go and see': he points up the slope to the crowd; '看' / '看' the disciples nod one after another;
                '吧' Andrew, James, John and Philip turn toward the crowd, Peter stays with Jesus
  ~3.85         hard cut (phrase boundary) to the crowd further along the slope
  '找' x4 4.94 / 5.40 / 5.92 / 6.39   James shades his eyes and looks one way, then the other, on every 找; John
                bends over a family's empty basket, then shakes his head; a man shows Philip his empty hands, Philip
                shakes his head; Andrew searches near a small boy with a basket
  '这时候' 6.77  Andrew turns and sees the boy; the boy looks up at him; Andrew lays a hand on his back
  '彼' 7.20 ..   Andrew leads the boy across the slope to Jesus (planted-foot walk, the boy's basket swinging); the
                camera travels with them
  ~11.3         Andrew stops; the boy takes one more shy step and stands before Jesus, hugging his basket
  '这里有个小孩子' 13.33  Andrew presents him (open hand); '小孩子' the boy turns to Andrew and holds up his open basket
  ~14.6         Andrew lifts it out of his hands (the basket travels on its own layer between the hands, no pop);
                '带着' he holds it up: five loaves, two fish; '可是' his face turns doubtful
  '五个大麦饼'   one loaf pops up into the air on each syllable (1-5), '两' / '小' the two fish (1, 2)
  '这么多人'     the camera glances over the huge crowd on the hillside (out 17.42-18.92, back 19.15-20.65, each a
                gentle 1.5 s sine move)
  '这一点点'     once the camera is back (20.55) the counted loaves and fish arc down into Andrew's basket one by one
                and drop in at the rim (a soft pop); Andrew doubtful
  after the line Andrew hands the basket back down to the boy; the boy turns to Jesus holding it
  '五个饼'       a gloss card: the little open basket ... '只够' = one boy patting his full tummy
  '可是' 26.65   the boy looks up at Jesus; just before '交给' (28.58) he lifts the basket with both hands; Jesus
                bends kindly (smile_boy)
  ~29.05        on '交给了' the basket passes into Jesus's hands (chime 29.32, clear of the scene's end); the boy folds
                his hands and smiles
  end           calm: Jesus holding the basket, smiling down at the boy; Andrew and Peter watching
"""
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.nativity.scenes.s01_title import beat
from stories.noah.scenes.s01_title import snap

INK = S.P["ink"]

# ================================================================== the place (shared with s08_baskets)
W5, H5 = 3400, 1250
YF = 1000                                  # the hillside's front line (lake_hillside y)
LSEED = 5                                  # lake_hillside seed (the same slope, trees, rocks in s05 and s08)
ROCK_X = 380                               # the teaching rock, left of the meeting place
PTS = PR.lake_hillside_points(0, W5, YF, 1.0, rock_x=ROCK_X, seed=LSEED)
LAKE_Y, FAR_Y = PTS["lake_y"], PTS["far_y"]
DEPTH = PTS["depth"]
K = 0.95                                   # the main people
YG = 1052                                  # their ground line
TIME5 = 0.55                               # the golden hour
SUN5 = (2980, 300)

# the meeting: Jesus, the boy in front of him (the offer: BOY_OFFER contact), Andrew behind the boy
XJ = 700
XB = XJ + 150 * K                          # the boy (facing Jesus) - jesus 'smile_boy' contact
XA = XB + 155 * K                          # Andrew: far enough that his raised basket clears the boy's head
XP = XJ - 175 * K                          # Peter stays beside Jesus

# z order
Z_SKY, Z_SUN, Z_CLOUD, Z_BACK, Z_GLINT, Z_MID, Z_FAR = 0, 0.5, 1, 2, 2.4, 3, 4
Z_CROWD, Z_HERO, Z_PEOPLE, Z_FRONT_PEOPLE, Z_PROP, Z_FX, Z_GLOSS, Z_FG = 5, 6, 7, 7.5, 8, 9, 10, 11


def doc(body, defs="", w=W5, h=H5):
    return S.svg_doc(body, defs, w, h)


def f1(v):
    return f"{v:.1f}"


def clamp01(v):
    return 0.0 if v < 0 else 1.0 if v > 1 else v


def env(t, t0, t1, fin=0.4, fout=0.4):
    """0 -> 1 -> 0 envelope."""
    if t1 >= 1e8:
        return M.progress(t, t0, t0 + fin, "sine")
    return M.progress(t, t0, t0 + fin, "sine") * (1 - M.progress(t, t1 - fout, t1, "sine"))


def loop_idx(t, g0, period, n):
    """Index of an idle loop of n drawings, period s each, counted in whole film frames on the global clock."""
    g = int(round((t + g0) * 30))
    return int(g // (period * 30)) % n


# ================================================================== camera
def cam_inside(c, w=W5, h=H5):
    hw, hh = c.w / 2, c.w * 9 / 32
    return c.x - hw >= -0.01 and c.x + hw <= w + 0.01 and c.y - hh >= -0.01 and c.y + hh <= h + 0.01


def clamp_cam(c, w=W5, h=H5):
    cw = min(c.w, w - 2, (h - 2) * 16 / 9)
    hw, hh = cw / 2, cw * 9 / 32
    return Cam(min(max(c.x, hw + 0.5), w - hw - 0.5), min(max(c.y, hh + 0.5), h - hh - 0.5), cw, c.rot)


def zoom_cam(keys, curves="sine", w=W5, h=H5):
    """Camera keys (t, Cam) with every key clamped inside the stage; zooms run at an even rate in log-width with the
    centre moving in step (the Nativity film's zoom_path), every in-between frame clamped. A key may be the string
    'cut' between two keys at the same time: a hard cut."""
    ks = [(t, clamp_cam(c, w, h)) for t, c in sorted(keys, key=lambda k_: k_[0])]
    cv = curves if isinstance(curves, (list, tuple)) else [curves] * max(1, len(ks) - 1)

    def cam(t):
        if t <= ks[0][0]:
            return ks[0][1]
        if t >= ks[-1][0]:
            return ks[-1][1]
        for i in range(len(ks) - 1):
            (t0, a), (t1, b) = ks[i], ks[i + 1]
            if t0 <= t < t1 or (i == len(ks) - 2 and t <= t1):
                u = M.progress(t, t0, t1, cv[min(i, len(cv) - 1)])
                if abs(b.w - a.w) > 1:
                    ww = math.exp(M.lerp(math.log(a.w), math.log(b.w), u))
                    v = (ww - a.w) / (b.w - a.w)
                else:
                    ww, v = M.lerp(a.w, b.w, u), u
                return clamp_cam(Cam(M.lerp(a.x, b.x, v), M.lerp(a.y, b.y, v), ww), w, h)
        return ks[-1][1]
    return cam


def cut_cam(shots):
    """shots: [(t_start, cam_fn)] - hard cuts between camera functions."""
    shots = sorted(shots, key=lambda s_: s_[0])

    def cam(t):
        f = shots[0][1]
        for t0, fn in shots:
            if t >= t0:
                f = fn
        return f(t)
    return cam


# ================================================================== motion helpers
class Track:
    """Anchor position over time: holds, eased moves, hop arcs. pos(t) -> (x, y)."""

    def __init__(self, x, y):
        self.moves = []
        self.cur = (x, y)
        self.x0, self.y0 = x, y

    def to(self, t0, t1, x, y, lift=0.0, curve="sine"):
        self.moves.append((t0, t1, self.cur, (x, y), lift, curve))
        self.cur = (x, y)
        return self

    def jump(self, t, x, y):
        return self.to(t, t, x, y)

    def __call__(self, t):
        x, y = self.x0, self.y0
        for t0, t1, a, b, lift, curve in self.moves:
            if t < t0:
                break
            if t >= t1:
                x, y = b
                continue
            u = M.progress(t, t0, t1, curve)
            v = (t - t0) / max(1e-6, t1 - t0)
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - lift * math.sin(math.pi * v)
        return x, y


def squash(t0, s, piv, depth=8.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def bump(t0, s, piv, height=14.0, dur=0.26):
    """A little hop / bob up whose take-off is at t0."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf()
        v = u / dur
        return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.02 * math.sin(math.pi * v), px=piv[0], py=piv[1])
    return m


def nod(t0, s, piv, deg=4.0, dur=0.42):
    """A small forward nod of the whole figure (rotation about the feet)."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf()
        return Tf(rot=deg * math.sin(math.pi * u / dur), sy=1 - 0.012 * math.sin(math.pi * u / dur), px=piv[0], py=piv[1])
    return m


def breath(piv, g0, period=3.0, amount=0.011, phase=0.0):
    """Breathing on the film's global clock."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def pop_in(t0, piv, dur=0.3, t1=None, out=0.3, s0=0.3, rise=0.0):
    """Scale-pop in at t0 (back ease) and shrink-fade out ending at t1."""
    def m(t):
        if t < t0 or (t1 is not None and t > t1):
            return Tf(alpha=0.0)
        u = M.progress(t, t0, t0 + dur, "back")
        a = M.progress(t, t0, t0 + dur * 0.5, "sine")
        s = s0 + (1 - s0) * u
        if t1 is not None:
            o = M.progress(t, t1 - out, t1, "inout")
            a *= 1 - o
            s *= 1 - 0.5 * o
        return Tf(alpha=a, sx=s, sy=s, dy=-rise * M.progress(t, t0, t0 + 1.5, "out"), px=piv[0], py=piv[1])
    return m


def blink_expr(e):
    """A closed-eye variant of expression e (registered once in characters.EXPRS)."""
    name = f"lf5_blink_{e}"
    if name not in C.EXPRS and e in C.EXPRS:
        C.EXPRS[name] = dict(C.EXPRS[e], eyes="closed")
    return name


# ================================================================== people (keys -> markup with small overrides)
def _apply(ps, mod):
    ps = dict(ps)
    if not mod:
        return ps
    for k_, v in dict(mod).items():
        if k_ in ("h", "t", "drop"):
            ps[k_] = ps.get(k_, 0) + v
        else:
            ps[k_] = v
    return ps


def _mods(mod):
    return tuple(sorted(mod.items())) if isinstance(mod, dict) else mod


def jk(pose, f=1, expr=None, item=None, mod=None, glow=0.0, phase=0.0):
    return ("J", pose, f, expr, item, _mods(mod), round(glow, 3), round(phase, 3))


def dk(variant, pose, f=-1, expr=None, phase=0.0, basket=True, mod=None, fill=None, food="bread"):
    return ("D", variant, pose, f, expr, round(phase, 3), basket, _mods(mod), fill, food)


def bk(pose, f=-1, expr=None, phase=0.0, basket=None, mod=None):
    return ("B", pose, f, expr, round(phase, 3), basket, _mods(mod))


def fk(kind, variant, pose, f=1, expr=None, phase=0.0, food=None):
    return ("F", kind, variant, pose, f, expr, round(phase, 3), food)


def jesus_svg(x, y, k, key):
    _, pose, f, expr, item, mod, glow, phase = key
    if not mod:
        return C.jesus(x, y, k, f, pose=pose, expr=expr, item=item, glow=glow, phase=phase) if pose in C.JESUS_LOAVES_POSES \
            else C.jesus(x, y, k, f, pose=pose, expr=expr, glow=glow, phase=phase)
    if pose in C.JESUS_LOAVES_POSES:
        ps = C._jesus_lf_pose(pose, phase)
        D = C._jesus_design(pose, clamp01(glow), True, 0.0, True)
        if pose in ("look_up_bless", "break_bread", "give_bread", "smile_boy"):
            D["front"] = C._hooks(D["front"], C._jesus_lf_items(pose, phase, item, True))
    elif pose in C.JESUS_LOST_SHEEP_POSES:
        ps = dict(C._JZ_LS[pose])
        D = C._jesus_design(pose, clamp01(glow), True, 0.0, True)
    else:
        ps = dict(C._jesus_pose(pose, phase))
        D = C._jesus_design(pose, clamp01(glow), True, 0.0, True)
    ps = _apply(ps, mod)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, C._JESUS_M, ps, e, C._fsign(f), True)
    return C._wrap_out(inner, x, y, k, f, f"lf5-jesus-{pose}")


def disc_svg(x, y, k, key):
    _, v, pose, f, expr, phase, basket, mod, fill, food = key
    if not mod:
        if pose in C.DISCIPLE_LOAVES_POSES:
            return C.disciples(x, y, k, f, variant=v, pose=pose, expr=expr, phase=phase, basket=basket, fill=fill, food=food)
        return C.disciples(x, y, k, f, variant=v, pose=pose, expr=expr, phase=phase)
    vi = C._disciple_index(4 if v == "philip" else v)
    D, m = C._disciple_design(vi, 0.0, False)
    if pose in C.DISCIPLE_LOAVES_POSES:
        ps, key_ = C._disciple_lf_pose(pose, phase)
        D["front"] = C._hooks(C._disciple_lf_items(D, key_, phase, fill, food, basket))
    else:
        ps, _tip = C._disciple_pose(pose, phase)
        key_ = pose
    ps = _apply(ps, mod)
    e = expr or ps["expr"]
    inner, _ = C._figure(D, m, ps, e, C._fsign(f), True)
    return C._wrap_out(inner, x, y, k, f, f"lf5-disciple{vi}-{key_}")


def boy_svg(x, y, k, key):
    _, pose, f, expr, phase, basket, mod = key
    if not mod:
        return C.the_boy(x, y, k, f, pose=pose, expr=expr, phase=phase, basket=basket)
    ph = phase % 1.0
    key_ = ("walk_a" if ph < 0.5 else "walk_b") if pose == "walk" else pose
    ps = _apply(C._BZ[key_], mod)
    b = C._BOY_DEFAULT_BASKET.get(key_) if basket is None else basket
    D = C._boy_design()
    D["front"] = C._hooks(C._boy_items(D, key_, phase, b))
    e = expr or ps["expr"]
    inner, _ = C._figure(D, C._BOY_M, ps, e, C._fsign(f), True)
    return C._wrap_out(inner, x, y, k, f, f"lf5-boy-{key_}")


def folk_svg(x, y, k, key):
    _, kind, v, pose, f, expr, phase, food = key
    return C.galilee_folk(x, y, k, f, kind=kind, variant=v, pose=pose, expr=expr, phase=phase, food=food)


def draw_key(key, x, y, k):
    return {"J": jesus_svg, "D": disc_svg, "B": boy_svg, "F": folk_svg}[key[0]](x, y, k, key)


def natural_expr(key):
    """The expression a key draws (its own, or the pose's natural one)."""
    kind = key[0]
    if kind == "J":
        _, pose, f, expr, item, mod, glow, phase = key
        if expr:
            return expr
        if pose in C.JESUS_LOAVES_POSES:
            return C._jesus_lf_pose(pose, phase)["expr"]
        if pose in C.JESUS_LOST_SHEEP_POSES:
            return C._JZ_LS[pose]["expr"]
        return C._jesus_pose(pose, phase)["expr"]
    if kind == "D":
        _, v, pose, f, expr, phase, basket, mod, fill, food = key
        if expr:
            return expr
        if pose in C.DISCIPLE_LOAVES_POSES:
            return C._disciple_lf_pose(pose, phase)[0]["expr"]
        return C._disciple_pose(pose, phase)[0]["expr"]
    if kind == "B":
        _, pose, f, expr, phase, basket, mod = key
        if expr:
            return expr
        ph = phase % 1.0
        key_ = ("walk_a" if ph < 0.5 else "walk_b") if pose == "walk" else pose
        return "yum" if key_ == "pat_tummy" else C._BZ[key_]["expr"]
    if kind == "F":
        _, kd, v, pose, f, expr, phase, food = key
        return expr or C._gl_pose(kd, pose, phase)[0]["expr"]
    return None


def blink_key(key):
    """The same drawing with closed eyes (None when the expression already has closed / arc eyes)."""
    if key is None:
        return None
    e = natural_expr(key)
    if e is None or C.EXPRS.get(e, {}).get("eyes") in ("closed", "arc", "happy_arc"):
        return None
    be = blink_expr(e)
    kind = key[0]
    if kind == "J":
        return key[:3] + (be,) + key[4:]
    if kind == "D":
        return key[:4] + (be,) + key[5:]
    if kind == "B":
        return key[:3] + (be,) + key[4:]
    if kind == "F":
        return key[:5] + (be,) + key[6:]
    return None


class Fig:
    """One figure on its own flipbook layer: hard cuts between keys (hidden in a squash dip unless dip=False), a Track
    that moves the drawing, idle loops on the global clock (loops[key] = (n, period): draw(key, i)), blinks."""

    def __init__(self, name, ref, z, g0, k=K, seed=0, loops=None, draw=None, wc=1.0, w=W5, h=H5, shadow=None):
        self.name, self.ref, self.z, self.g0, self.k, self.seed, self.wc = name, ref, z, g0, k, seed, wc
        self.loops = loops or {}
        self.ents, self.dips, self.mots = [], [], []
        self.track = Track(*ref)
        self.alpha = None
        self.w, self.h = w, h
        self.draw = draw or (lambda key, i=0: draw_key(key, ref[0], ref[1], k))
        self.shadow = shadow                    # width of a soft contact shadow drawn under the figure (own layer)

    def cut(self, t, key, dip=True, depth=7.0):
        t = snap(t) if t > 0 else -1e4
        self.ents = [e for e in self.ents if e[0] != t]
        self.ents.append((t, key))
        if dip and t > 0:
            self.dips.append((t, depth))
        return self

    def key_at(self, t):
        cur = None
        for tk, n in sorted(self.ents, key=lambda e: e[0]):
            if tk <= t:
                cur = n
        return cur

    def blinks(self, t_from, t_to, rng, every=(2.4, 4.2), avoid=()):
        t = t_from + rng.uniform(0.3, 1.2)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.25:
            cur = self.key_at(t)
            bk_ = blink_key(cur)
            if bk_ and all(abs(t - tk) > 0.35 for tk in cut_ts) and not any(a - 0.2 <= t <= b for a, b in avoid):
                self.ents += [(snap(t), bk_), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def motion(self):
        px, py = self.ref
        tr = self.track

        def base(t):
            x, y = tr(t)
            return Tf(dx=x - px, dy=y - py, px=px, py=py)
        mots = [base] + [squash(td, self.k, self.ref, depth) for td, depth in self.dips] + self.mots
        al = self.alpha
        if al is not None:
            mots.append(lambda t: Tf(alpha=al(t)))
        return M.combine(*mots)

    def build(self, sc):
        ents = sorted(self.ents, key=lambda e: e[0])
        names = []
        for _, n in ents:
            if n not in names:
                names.append(n)
        frames, index = [], {}
        for n in names:
            nl, _ = self.loops.get(n, (1, 1.0))
            for i in range(nl):
                index[(n, i)] = len(frames)
                frames.append(doc(self.draw(n, i) if n in self.loops else self.draw(n), w=self.w, h=self.h))
        g0, loops = self.g0, self.loops

        def fa(t):
            cur = ents[0][1]
            for tk, n in ents:
                if t >= tk:
                    cur = n
            if cur in loops:
                nl, per = loops[cur]
                return float(index[(cur, loop_idx(t, g0, per, nl))])
            return float(index[(cur, 0)])
        if self.shadow:
            px, py = self.ref
            tr = self.track
            sh = doc(C.ground_shadow(px, py, self.k, self.shadow, 0.2), w=self.w, h=self.h)
            al = self.alpha
            sc.add(self.name + "_sh", sh, z=self.z - 0.01, wc=0,
                   motion=lambda t: Tf(dx=tr(t)[0] - px, dy=tr(t)[1] - py, alpha=al(t) if al else 1.0))
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=self.wc, motion=self.motion())
        return self


def walk_steps(t0, t1, x0, x1):
    """Planted-foot walk from x0 (t0) to x1 (t1): [(t_cut, x_after)] one step per cut, the steps evenly spaced."""
    n = max(1, round(abs(x1 - x0) / (68 * K)))
    per = (t1 - t0) / n
    return [(t0 + per * (i + 0.5), x0 + (x1 - x0) * (i + 1) / n) for i in range(n)], per


# ================================================================== the basket passing between hands
def held_basket(fn, x, y, k, f, dy, rot, bk_scale, **kw):
    """Where fn(x, y, k, f, **kw) holds the boy's basket: the hook draws it at the hands' midpoint + dy (local units),
    rotated rot, scaled bk_scale. Returns (x, y, k, f, atx, aty, rot, bk_scale) - the same transform chain as the
    figure, so the basket drawn alone matches it exactly (wobble included)."""
    (x0, y0), (x1, y1) = C.hand_positions(fn, x, y, k, f, **kw)
    sx = k * (1 if f >= 0 else -1)
    atx = ((x0 + x1) / 2 - x) / sx
    aty = ((y0 + y1) / 2 - y) / k + dy
    return (x, y, k, f, atx, aty, rot, bk_scale)


def held_centre(h):
    x, y, k, f, atx, aty, rot, bks = h
    return x + atx * k * (1 if f >= 0 else -1), y + aty * k


def basket_markup(state, h, handle=False):
    x, y, k, f, atx, aty, rot, bks = h
    sx = k * (1 if f >= 0 else -1)
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({sx:.5g},{k:.5g})"><g filter="url(#wobble-fine)">'
            f'<g transform="translate({atx:.1f},{aty:.1f}) rotate({rot:.1f}) scale({bks:.3f})">'
            f'{PR._boy_basket(state, handle=handle)}</g></g></g>')


def add_pass(sc, name, state, a, b, t0, t1, z, lift=12.0, state_b=None):
    """The basket travelling from holder a to holder b (held_basket tuples) between t0 and t1 (eased), drawn on its own
    layer only while it travels (the figures hold it before / after). When the two holders face different ways the
    drawing switches to b's (mirrored) version half way. state_b: the state in b's hands (e.g. the cloth folded back)."""
    ca, cb = held_centre(a), held_centre(b)
    ka, kb = a[2] * a[7], b[2] * b[7]
    ra = a[6] * (1 if a[3] >= 0 else -1)
    rb = b[6] * (1 if b[3] >= 0 else -1)
    flip = (a[3] >= 0) != (b[3] >= 0) or (state_b and state_b != state)
    svg_a = doc(basket_markup(state, a))
    svg_b = doc(basket_markup(state_b or state, b))

    def mot(t, which):
        if t < t0 or t >= t1:
            return Tf(alpha=0.0)
        u = M.progress(t, t0, t1, "inout")
        if flip and ((u < 0.5) != (which == 0)):
            return Tf(alpha=0.0)
        cx, cy = M.lerp(ca[0], cb[0], u), M.lerp(ca[1], cb[1], u) - lift * math.sin(math.pi * u)
        kk = M.lerp(ka, kb, u)
        rr = M.lerp(ra, rb, u)
        if which == 0:
            return Tf(dx=cx - ca[0], dy=cy - ca[1], sx=kk / ka, sy=kk / ka, rot=rr - ra, px=ca[0], py=ca[1])
        return Tf(dx=cx - cb[0], dy=cy - cb[1], sx=kk / kb, sy=kk / kb, rot=rr - rb, px=cb[0], py=cb[1])
    sc.add(name + "_a", svg_a, z=z, motion=lambda t: mot(t, 0))
    if flip:
        sc.add(name + "_b", svg_b, z=z, motion=lambda t: mot(t, 1))


# ================================================================== timing
def syl(ctx, li, phrase, occ=0):
    """Onsets of every character of the occ-th occurrence of phrase in line li (voice-measured; fallback: spread over
    the subtitle chunk that contains it)."""
    from stories.noah.scenes.s01_title import char_times, voice_marks
    n = 0
    try:
        for ent in voice_marks(ctx, li):
            pos = ent[0].find(phrase)
            while pos >= 0:
                if n == occ:
                    ct = char_times(ent)
                    return [ct[min(pos + j, len(ct) - 1)] for j in range(len(phrase))]
                n += 1
                pos = ent[0].find(phrase, pos + 1)
    except Exception:                                    # noqa: BLE001
        pass
    ln = ctx.lines[li]
    for c in ln.chunks:
        if phrase in c.text:
            i = c.text.index(phrase)
            step = (c.end - c.start) / max(1, len(c.text))
            return [c.start + step * (i + j) for j in range(len(phrase))]
    return [ln.start + 0.2 * j for j in range(len(phrase))]


# ================================================================== the world
def sky_svg(time, sun=SUN5):
    return doc(PR.galilee_sky(0, 0, W5, FAR_Y + 140, time=time, sun=sun, clouds=0, birds=0, seed=LSEED, scale=1.0))


CLOUDS = [  # cx, cy, w, h, seed, drift px/s
    (380, 150, 470, 130, 3, 5.0), (1250, 95, 560, 150, 8, 3.5), (2050, 205, 420, 115, 12, 4.5),
    (2750, 120, 520, 140, 17, 3.0), (3300, 230, 380, 105, 21, 5.5)]


def add_clouds(sc, time, g0, z=Z_CLOUD):
    pal = PR._lf_pal(time)
    for i, (cx, cy, w, h, seed, v) in enumerate(CLOUDS):
        body = PR._lf_cloud(cx, cy, w, h, pal, seed, rim_k=0.4 + 0.6 * PR._lf_t(time))
        sc.add(f"cloud{i}", doc(f'<g opacity="0.92">{body}</g>'), z=z + 0.01 * i, wc=0.8,
               motion=lambda t, v=v: Tf(dx=v * (t + g0 - 100.0)))


def hill_svg(time, part, **kw):
    """lake_hillside without its own trees (trees=False): the trees are drawn on their own layers, depth-sorted with
    the crowd, so no seated or standing group is ever painted over a tree that stands in front of it."""
    return doc(PR.lake_hillside(0, W5, YF, 1.0, time=time, part=part, seed=LSEED, rock_x=ROCK_X, bottom=H5 + 30,
                                boat=None, trees=False, **kw))


# the hillside trees (x, depth fraction, kind, seed), placed in the gaps between the people of each scene; only left of
# the hill's shoulder (x < 0.66 W), so they stand at the same depth y in every convention
TREES5 = [(600, 0.72, "oak", 7), (2190, 0.60, "olive", 9)]


def tree_at(x, d):
    y, k = DEPTH(d)
    return x, y, k


def tree_svg(x, d, kind, seed, time):
    tx, ty, k = tree_at(x, d)
    return doc(f'<g filter="url(#wobble)">{PR._lf_tree(tx, ty, k, time, seed, kind)}</g>')


def depth_z(z0, y):
    """A z inside the crowd band for something standing on the ground at stage y (farther = lower)."""
    return z0 + 0.5 * (y / H5)


def boat_svg(time, x=2560):
    return doc(PR.far_boat(x, LAKE_Y - 16, 0.13, -1, sail="furled", crew=False, time=time))


def glints_svg(time, which):
    """Little sun glints on the lake (two alternating sets), only on the open water left of the hill's shoulder."""
    rng = random.Random(40 + which)
    pal = PR._lf_pal(time)
    col = pal["glit"]
    out = ""
    for _ in range(26):
        x = rng.uniform(60, W5 * 0.70)
        y = rng.uniform(FAR_Y + 30, LAKE_Y - 12)
        w = rng.uniform(10, 26) * (0.6 + 0.6 * (y - FAR_Y) / (LAKE_Y - FAR_Y))
        out += f'<path d="M{f1(x - w)},{f1(y)} Q{f1(x)},{f1(y - 3)} {f1(x + w)},{f1(y)}" stroke="{col}" stroke-width="3" ' \
               f'stroke-linecap="round" fill="none" opacity="0.85"/>'
    return doc(out)


def add_glints(sc, time, g0, z=Z_GLINT):
    for w_ in (0, 1):
        sc.add(f"glint{w_}", glints_svg(time, w_), z=z + 0.01 * w_, wc=0,
               motion=lambda t, w_=w_: Tf(alpha=0.15 + 0.85 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t + g0) / 2.6 + 0.5 * w_)))))


def front_corner_svg(time, side):
    """The big grass blades / flowers / stones of lake_hillside part 'front', one corner at a time (they sway)."""
    full = PR.lake_hillside(0, W5, YF, 1.0, time=time, part="front", seed=LSEED, bottom=H5 + 30)
    x0 = 0 if side == 0 else W5 - 560
    cid = f"lf5front{side}"
    return doc(f'<clipPath id="{cid}"><rect x="{x0}" y="0" width="560" height="{H5}"/></clipPath>'
               f'<g clip-path="url(#{cid})">{full}</g>')


def add_front(sc, time, g0, z=Z_FG):
    for side in (0, 1):
        px = 200 if side == 0 else W5 - 200
        sc.add(f"front{side}", front_corner_svg(time, side), z=z + 0.01 * side,
               motion=lambda t, px=px, side=side: Tf(rot=0.9 * math.sin(2 * math.pi * ((t + g0) / 3.4 + 0.3 * side)),
                                                       px=px, py=H5 + 40))


# the standing crowd on the slope (s05): clusters of families chatting, waiting
CROWD5 = [  # x, depth, n, width, rows, seed, pose
    (230, 0.87, 7, 330, 2, 11, "stand"), (860, 0.88, 8, 380, 2, 12, "listen"), (1480, 0.86, 9, 420, 2, 13, "stand"),
    (2040, 0.87, 9, 400, 2, 14, "stand"), (2600, 0.85, 10, 460, 2, 15, "point"), (3170, 0.84, 9, 420, 2, 16, "stand"),
    (1690, 0.64, 8, 360, 2, 22, "stand"), (2470, 0.63, 10, 440, 2, 23, "listen"), (2980, 0.65, 9, 400, 2, 25, "stand"),
    (3330, 0.60, 6, 260, 2, 24, "stand"),
    (2660, 0.42, 8, 360, 2, 33, "stand"), (3200, 0.40, 7, 320, 2, 34, "listen"),
    (1390, 0.57, 6, 260, 2, 41, "stand"), (110, 0.62, 5, 220, 2, 42, "listen"),
    (1960, 0.74, 8, 360, 2, 43, "stand"), (2820, 0.75, 9, 400, 2, 44, "listen"), (2430, 0.50, 8, 340, 2, 45, "stand"),
    (1830, 0.50, 7, 320, 2, 46, "point"),
    (3320, 0.24, 4, 200, 1, 31, "stand")]


def haze_filter(fid, amount, time):
    """An SVG filter that mixes the colours toward the evening haze (distant people)."""
    r, g_, b_ = S.hex_rgb(PR._lf_pal(time)["haze"])
    a = 1 - amount
    return (f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%"><feColorMatrix type="matrix" values="'
            f'{a:.3f} 0 0 0 {amount * r / 255:.3f}  0 {a:.3f} 0 0 {amount * g_ / 255:.3f}  0 0 {a:.3f} 0 {amount * b_ / 255:.3f}  '
            f'0 0 0 1 0"/></filter>')


def fg_strip_svg(time, x0, x1, y0, y1, seed, dens=1.0):
    """A strip of long grass tufts and Galilee flowers in front of the people's feet (framing the bottom edge)."""
    pal = PR._lf_pal(time)
    g = pal["grass"]
    out = PR._lf_grass(x0, x1, y0, y1, int(26 * dens * (x1 - x0) / 1000), seed, (pal["grass_dk"], g[2]), 1.25, 0.8, 1.3)
    out += PR._lf_flowers(x0, x1, y0 + 10, y1, 1.6 * dens, seed + 1, time, 1.2)
    return doc(f'<g filter="url(#wobble)">{out}</g>')


def add_fg_strip(sc, time, g0, x0=0, x1=W5, y0=1088, y1=1170, z=Z_FG - 0.5):
    for j in range(2):
        sc.add(f"fgstrip{j}", fg_strip_svg(time, x0, x1, y0, y1, 600 + 7 * j, 0.6), z=z + 0.01 * j,
               motion=lambda t, j=j: Tf(dx=2.2 * math.sin(2 * math.pi * ((t + g0) / 2.9 + 0.5 * j)), px=0, py=y1))


def crowd_cluster_svg(x, d, n, width, rows, seed, pose, time=TIME5):
    y, k = DEPTH(d)
    y -= PTS["shoulder"](x / W5) * d ** 1.4
    fid = f"lfhz{seed}"
    body = C.galilee_crowd(x, y, k, 1, n=n, pose=pose, width=width, rows=rows, seed=seed, gap=60)
    return doc(f'<g filter="url(#{fid})">{body}</g>', defs=haze_filter(fid, 0.30 * d, time))


def swallow_svg(x, y, s, up):
    w = -14 if up else 6
    d = (f"M{f1(x - 22 * s)},{f1(y + w * s)} Q{f1(x - 9 * s)},{f1(y - 4 * s + w * 0.3 * s)} {f1(x)},{f1(y)} "
         f"Q{f1(x + 9 * s)},{f1(y - 4 * s + w * 0.3 * s)} {f1(x + 22 * s)},{f1(y + w * s)}")
    return doc(f'<path d="{d}" stroke="#5a4a5a" stroke-width="{f1(3.2 * s)}" fill="none" stroke-linecap="round" '
               f'stroke-linejoin="round"/>')


def add_swallows(sc, g0, z=Z_CLOUD + 0.5, birds=((300, 230, 1.0, 62, 0.0), (900, 170, 0.8, 48, 0.4),
                                                  (2200, 260, 0.9, -55, 0.2))):
    """Swallows gliding and flapping across the sky (x0, y0, size, speed px/s, phase) on the global clock."""
    for i, (x0, y0, s, v, ph) in enumerate(birds):
        frames = [swallow_svg(x0, y0, s, True), swallow_svg(x0, y0, s, False)]

        def fa(t, ph=ph):
            u = ((t + g0) / 0.36 + ph) % 1.0
            return 0.0 if u < 0.5 else 1.0

        def mot(t, v=v, ph=ph, x0=x0):
            g = t + g0
            dx = (v * g) % (W5 + 600) - (x0 + 300) if v > 0 else -((-v * g) % (W5 + 600)) + (W5 + 300 - x0)
            return Tf(dx=dx, dy=18 * math.sin(g * 0.9 + 6 * ph))
        sc.add(f"swallow{i}", frames, frame_at=fa, z=z + 0.01 * i, wc=0, motion=mot)


def light_svg(time, sun=SUN5, strength=0.24):
    """A soft warm glow from the low sun over the whole picture (people included): the golden hour."""
    pal = PR._lf_pal(time)
    col = pal["sun_halo"]
    gid = "lf5light"
    return doc(f'<rect x="-20" y="-20" width="{W5 + 40}" height="{H5 + 40}" fill="url(#{gid})"/>',
               defs=S.rad_grad(gid, [(0, col, strength), (0.45, col, strength * 0.45), (1, col, 0)],
                               cx=sun[0] / W5, cy=sun[1] / H5, r=0.75))


def add_world5(sc, g0, time=TIME5):
    sc.add("sky", sky_svg(time), z=Z_SKY)
    add_clouds(sc, time, g0)
    add_swallows(sc, g0)
    sc.add("hill_back", hill_svg(time, "back"), z=Z_BACK)
    add_glints(sc, time, g0)
    sc.add("boat", boat_svg(time), z=Z_GLINT + 0.1,
           motion=lambda t: Tf(dy=2.5 * math.sin((t + g0) * 1.7), rot=0.6 * math.sin((t + g0) * 1.3), px=2560, py=LAKE_Y - 16))
    sc.add("hill_mid", hill_svg(time, "mid"), z=Z_MID)
    add_front(sc, time, g0)
    add_fg_strip(sc, time, g0)
    sc.add("light", light_svg(time), z=Z_FG + 0.5, wc=0)


# ================================================================== the glosses
CARD_PATH = ("M-286,-138 Q-290,-152 -272,-154 L272,-154 Q290,-152 286,-138 L280,138 Q278,152 262,154 L-262,154 "
             "Q-280,152 -282,138 Z")


def card_svg(cx, cy, k):
    art = PR._p(CARD_PATH, "#fbf3e0", 4.0)
    art += PR._p("M-266,-134 L266,-134 L262,134 L-262,134 Z", "none", 2.0, stroke="#e2c79a", extra='stroke-dasharray="7 6"')
    shadow = (f'<g transform="translate({f1(cx + 10)},{f1(cy + 14)}) scale({k:.4f})"><path d="{CARD_PATH}" '
              f'fill="#7a4a2c" opacity="0.18" filter="url(#soft)"/></g>')
    return doc(shadow + PR._place(art, cx, cy, k))


def arrow_svg(cx, cy, k):
    a = (f'<path d="M{f1(cx - 40 * k)},{f1(cy)} L{f1(cx + 38 * k)},{f1(cy)} M{f1(cx + 14 * k)},{f1(cy - 20 * k)} '
         f'L{f1(cx + 40 * k)},{f1(cy)} L{f1(cx + 14 * k)},{f1(cy + 20 * k)}" stroke="#c8643c" stroke-width="{f1(9 * k)}" '
         f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    return doc(S.g(a, filter="wobble-fine"))


def number_svg(x, y, n, k=0.62, color="#e8705a"):
    return doc(PR.count_bubble(x, y, n, k, pop=1.0, color=color))


def boy_card_svg(cx, cy, k, phase):
    """The right half of the gloss card: the boy patting his full tummy (small)."""
    return doc(C.the_boy(cx, cy, k, -1, pose="pat_tummy", phase=phase))


# ================================================================== build
def build(ctx):
    sc = Scene(ctx, W=W5, H=H5)
    T = ctx.duration
    g0 = ctx.start
    rng = random.Random(5)
    b = lambda li, ph, k=0: beat(ctx, li, ph, k)                    # noqa: E731
    L = ctx.lines

    # ---------------------------------------------------------------- beats
    t_ni, t_qu, t_ba = b(0, "你们"), b(0, "去"), b(0, "吧")
    t_kan = syl(ctx, 0, "看看")
    t_zhao = [b(1, "找", k) for k in range(4)]
    t_zsh = b(1, "这时候")
    t_bi = b(1, "彼")
    t_l1e = L[1].end
    t_zl, t_xh = b(2, "这里"), b(2, "小孩子")
    t_dz = b(2, "带着")
    t_loaf = syl(ctx, 2, "五个大麦饼")
    t_fishes = syl(ctx, 2, "两条小鱼")
    t_fish = [t_fishes[0], t_fishes[2]]
    t_zmd = b(2, "这么多人")
    t_ydd = b(2, "这一点点")
    t_dd = syl(ctx, 2, "点点")
    t_gou = b(2, "够")
    t_l2e = L[2].end
    t_wg = b(3, "五个饼")
    t_zg = b(3, "只够")
    t_ks3 = b(3, "可是")
    t_jg = b(3, "交给")
    t_ys = b(3, "耶稣")
    t_cut = snap(L[0].end + 0.42)                               # shot A -> shot B (hard cut between the lines)

    # ---------------------------------------------------------------- the world + the crowd
    add_world5(sc, g0)
    for i, c in enumerate(CROWD5):                     # depth-sorted: a farther cluster never covers a nearer one
        y, k = DEPTH(c[1])
        y -= PTS["shoulder"](c[0] / W5) * c[1] ** 1.4
        piv = (c[0], y)
        sc.add(f"crowd{i}", crowd_cluster_svg(*c), z=depth_z(Z_CROWD, y), seed=300 + i,
               motion=breath(piv, g0, 3.3 + 0.21 * (i % 5), 0.006, 0.17 * i))
    for j, (x, d, kind, seed) in enumerate(TREES5):
        tx, ty, k = tree_at(x, d)
        sc.add(f"tree{j}", tree_svg(x, d, kind, seed, TIME5), z=depth_z(Z_CROWD, ty) - 1e-4, seed=330 + j,
               motion=lambda t, j=j, tx=tx, ty=ty: Tf(rot=0.5 * math.sin(2 * math.pi * ((t + g0) / 4.1 + 0.37 * j)),
                                                      px=tx, py=ty))

    # ---------------------------------------------------------------- Jesus
    jf = Fig("jesus", (XJ, YG), Z_PEOPLE, g0, seed=11, shadow=120)
    jf.cut(0, jk("stand", 1, "warm"))
    jf.cut(t_ni + 0.04, jk("ask", 1))
    jf.cut(t_qu - 0.08, jk("tell", 1, "smile"), depth=6)
    jf.cut(t_cut - 0.25, jk("stand", 1, "warm"), dip=False)
    jf.mots.append(breath((XJ, YG), g0, 3.2, 0.010))

    # ---------------------------------------------------------------- the disciples in shot A
    A_POS = {"peter": (945, YG + 10), "andrew": (1080, YG - 40), "james": (1195, YG + 14), "john": (1325, YG - 46),
             "philip": (1445, YG + 4)}
    pf = Fig("peter", A_POS["peter"], Z_PEOPLE - 0.1, g0, seed=21, shadow=110)
    pf.cut(0, dk("peter", "talk", -1, "concerned"))
    pf.mots.append(nod(t_kan[0] + 0.02, K, A_POS["peter"], 4))
    pf.cut(t_ba + 0.15, dk("peter", "stand", -1, "happy"), depth=5)
    # after the cut Peter waits beside Jesus (on his left)
    pf.track.jump(t_cut, XP, YG - 10)
    pf.cut(t_cut, dk("peter", "stand", 1, "happy"), dip=False)

    # ---------------------------------------------------------------- shot B: the search (positions)
    BOY0 = (1880, YG - 4)
    AND0 = (2075, YG + 6)
    JAM0 = (2430, YG - 14)
    JOH0 = (2720, YG + 2)
    WOM0 = (2865, YG - 6)
    BAS0 = (2798, YG - 2)
    PHI0 = (3020, YG - 8)
    MAN0 = (3190, YG - 4)
    MUM0 = (1745, YG - 62)

    # James: worried in A, nods, turns to go; in B he shades his eyes on every 找
    jaf = Fig("james", A_POS["james"], Z_PEOPLE - 0.12, g0, seed=31, shadow=110)
    jaf.cut(0, dk("james", "stand", -1, "worried"))
    jaf.mots.append(nod(t_kan[1] + 0.02, K, A_POS["james"], 4))
    jaf.cut(t_ba + 0.05, dk("james", "stand", 1, "happy"), depth=6)
    jaf.track.jump(t_cut, *JAM0)
    jaf.cut(t_cut, dk("james", "stand", 1, "thoughtful"), dip=False)
    for j, tz in enumerate(t_zhao):
        jaf.cut(tz - 0.06, dk("james", "search", 1, phase=0.0 if j % 2 == 0 else 0.6), depth=5)
    jaf.cut(t_zhao[3] + 0.9, dk("james", "stand", -1, "thoughtful"), depth=5)

    # John: bends over a family's empty basket, then shakes his head
    jof = Fig("john", A_POS["john"], Z_PEOPLE - 0.35, g0, seed=41, shadow=110,
              loops={dk("john", "shake_head", 1): (4, 0.12)},
              draw=lambda key, i=0: draw_key(key[:5] + (i / 4,) + key[6:] if key[2] == "shake_head" else key,
                                             A_POS["john"][0], A_POS["john"][1], K))
    jof.cut(0, dk("john", "worried", -1))
    jof.mots.append(nod(t_kan[1] + 0.1, K, A_POS["john"], 4))
    jof.cut(t_ba + 0.12, dk("john", "stand", 1, "happy"), depth=6)
    jof.track.jump(t_cut, *JOH0)
    jof.cut(t_cut, dk("john", "talk", 1, "thoughtful"), dip=False)
    jof.cut(t_zhao[0] - 0.08, dk("john", "talk", 1, "thoughtful", mod={"t": 22, "h": 18, "look": (0.03, 0.09)}), depth=6)
    jof.cut(t_zhao[2] - 0.06, dk("john", "shake_head", 1), depth=5)
    jof.cut(t_zhao[3] + 0.55, dk("john", "search", 1, phase=0.6), depth=5)

    # Philip: asks a man, who opens his empty hands; Philip shakes his head
    phf = Fig("philip", A_POS["philip"], Z_PEOPLE - 0.15, g0, seed=51, shadow=110,
              loops={dk("philip", "shake_head", 1): (4, 0.12)},
              draw=lambda key, i=0: draw_key(key[:5] + (i / 4,) + key[6:] if key[2] == "shake_head" else key,
                                             A_POS["philip"][0], A_POS["philip"][1], K))
    phf.cut(0, dk("philip", "worried", -1))
    phf.mots.append(nod(t_kan[1] + 0.18, K, A_POS["philip"], 4))
    phf.cut(t_ba + 0.2, dk("philip", "stand", 1, "happy"), depth=6)
    phf.track.jump(t_cut, *PHI0)
    phf.cut(t_cut, dk("philip", "talk", 1, "concerned"), dip=False)
    phf.cut(t_zhao[3] - 0.05, dk("philip", "shake_head", 1), depth=5)
    phf.cut(t_zhao[3] + 0.75, dk("philip", "worried", 1), depth=4)

    manf = Fig("man", MAN0, Z_HERO, g0, k=K * 0.97, seed=61, shadow=110)
    manf.cut(0, fk("man", 9, "stand", -1, "kind"))
    manf.cut(t_zhao[1] - 0.05, fk("man", 9, "receive", -1, "worried", food=False), depth=5)
    manf.cut(t_zhao[3] + 0.8, fk("man", 9, "stand", -1, "kind"), depth=4)
    manf.mots.append(breath(MAN0, g0, 3.1, 0.010, 0.2))

    womf = Fig("woman", WOM0, Z_HERO, g0, k=K * 0.97, seed=71, shadow=150)
    womf.cut(0, fk("woman", 15, "sit", -1, "kind"))
    womf.mots.append(breath(WOM0, g0, 2.9, 0.010, 0.5))
    sc.add("basket_empty", doc(PR.lunch_basket(*BAS0, 0.95 * K, 1, state="empty", time=TIME5)), z=Z_HERO + 0.05)

    mumf = Fig("mum", MUM0, Z_HERO - 0.5, g0, k=K * 0.95, seed=81, shadow=110,
               loops={fk("mother", 7, "wave", 1, "happy"): (3, 0.18)},
               draw=lambda key, i=0: draw_key(key[:6] + (i / 3,) + key[7:] if key[3] == "wave" else key,
                                              MUM0[0], MUM0[1], K * 0.95))
    mumf.cut(0, fk("mother", 7, "stand", 1, "kind"))
    mumf.mots.append(breath(MUM0, g0, 3.0, 0.010, 0.1))

    # ---------------------------------------------------------------- Andrew and the boy
    af = Fig("andrew", A_POS["andrew"], Z_PEOPLE - 0.3, g0, seed=91, shadow=110)
    bf = Fig("boy", BOY0, Z_PEOPLE - 0.4, g0, seed=101, shadow=90)
    af.cut(0, dk("andrew", "worried", -1))
    af.mots.append(nod(t_kan[0] + 0.12, K, A_POS["andrew"], 4))
    af.cut(t_ba + 0.0, dk("andrew", "stand", 1, "happy"), depth=6)
    af.track.jump(t_cut, *AND0)
    af.cut(t_cut, dk("andrew", "search", 1, phase=0.0), dip=False)
    for j, tz in enumerate(t_zhao):
        af.cut(tz + 0.1, dk("andrew", "search", 1, phase=0.0 if j % 2 == 0 else 0.6), depth=5)
    # '这时候': he sees the boy, turns and steps to him
    t_see = snap(t_zsh - 0.02)
    af.cut(t_see, dk("andrew", "stand", -1, "happy"), depth=6)
    af.mots.append(bump(t_see + 0.05, K, AND0, 8, 0.24))
    lead_x0 = BOY0[0] + C.DISCIPLE_LEAD_BOY[0] * K
    t_st = snap(t_see + 0.32)
    af.cut(t_st, dk("andrew", "walk_a", -1, "happy"), dip=False)
    af.track.to(t_st - 0.05, t_st + 0.08, lead_x0, AND0[1])
    t_hand = snap(max(t_st + 0.3, t_bi + 0.05))
    af.cut(t_hand, dk("andrew", "lead_boy", -1), dip=False)
    bf.cut(0, bk("stand_basket", 1, "happy"))
    bf.cut(snap(t_see + 0.12), bk("look_up", 1), depth=5)
    bf.cut(t_hand, bk("stand_basket", -1, "happy"), depth=5)
    bf.track.jump(t_hand, BOY0[0], AND0[1] + C.DISCIPLE_LEAD_BOY[1] * K)
    mumf.cut(t_hand + 0.25, fk("mother", 7, "wave", 1, "happy"), depth=4)
    mumf.cut(t_hand + 2.2, fk("mother", 7, "stand", 1, "happy"), depth=4)

    # the walk to Jesus
    t_w0 = snap(t_hand + 0.32)
    t_w1 = snap(min(t_l1e - 0.55, t_w0 + 4.4))
    steps, per = walk_steps(t_w0, t_w1, lead_x0, XA)
    ya = AND0[1]
    yb = AND0[1] + C.DISCIPLE_LEAD_BOY[1] * K
    for i, (tc, xa) in enumerate(steps):
        tc = snap(tc)
        fr = "a" if i % 2 == 0 else "b"
        af.cut(tc, dk("andrew", f"lead_boy_walk_{fr}", -1), dip=False)
        bf.cut(tc, bk(f"walk_{fr}", -1, "happy"), dip=False)
        af.track.to(tc - 0.06, tc + 0.07, xa, ya)
        bf.track.to(tc - 0.06, tc + 0.07, xa - C.DISCIPLE_LEAD_BOY[0] * K, yb)
    t_stop = snap(t_w1 + per * 0.5)
    af.cut(t_stop, dk("andrew", "lead_boy", -1), dip=False)
    bf.cut(t_stop, bk("shy", -1), dip=False)
    af.track.to(t_stop - 0.05, t_stop + 0.1, XA, YG)
    bf.track.to(t_stop - 0.05, t_stop + 0.1, XA - C.DISCIPLE_LEAD_BOY[0] * K, YG + C.DISCIPLE_LEAD_BOY[1] * K)
    # the boy's one more shy step to stand before Jesus; Andrew's hand lets go
    t_step = snap(t_stop + 0.38)
    bf.cut(t_step, bk("walk_a", -1, "shy"), dip=False)
    bf.track.to(t_step - 0.05, t_step + 0.1, XB, YG)
    af.cut(t_step, dk("andrew", "talk", -1, "kind"), depth=4)
    bf.cut(snap(t_step + 0.34), bk("shy", -1), dip=False)

    # Jesus watches them come, then looks down kindly at the boy
    jf.cut(snap(t_stop - 0.3), jk("look_kind", 1, "smile"), depth=5)

    # '这里有个小孩子': Andrew presents him (a nod, then looking down at him)
    af.mots.append(nod(t_zl + 0.05, K, (XA, YG), 3))
    af.cut(t_xh - 0.1, dk("andrew", "talk", -1, "kind", mod={"h": 12, "look": (0.02, 0.07)}), depth=4)
    # ... the boy turns to Andrew and holds up his basket; Andrew lifts it and opens it
    t_turn = snap(t_xh + 0.08)
    bf.cut(t_turn, bk("offer_up", 1, "hopeful", basket="open"), depth=6)
    t_p0 = snap(t_turn + 0.42)
    t_p1 = snap(t_p0 + 0.22)
    hb_boy = held_basket(C.the_boy, XB, YG, K, 1, -4, -4, 0.62, pose="offer_up")
    hb_and = held_basket(C.disciples, XA, YG, K, -1, -2, -6, 0.74, variant="andrew", pose="show_lunch")
    bf.cut(t_p0, bk("offer_up", 1, "hopeful", basket=False), dip=False)
    af.cut(t_p0, dk("andrew", "show_lunch", -1, "kind", basket=False), dip=False)
    add_pass(sc, "pass1", "open", hb_boy, hb_and, t_p0, t_p1, Z_PROP)
    af.cut(t_p1, dk("andrew", "show_lunch", -1, "happy"), dip=False)
    bf.cut(snap(t_p1 + 0.12), bk("watch", 1, "hopeful"), depth=5)
    af.mots.append(bump(t_dz - 0.05, K, (XA, YG), 7, 0.3))
    af.cut(snap(b(2, "可是") - 0.05), dk("andrew", "show_lunch", -1, "doubtful"), depth=4)
    af.mots.append(bump(t_gou - 0.05, K, (XA, YG), 5, 0.3))

    # after the line: the basket goes back down to the boy
    t_r0 = snap(t_l2e + 0.25)
    bf.cut(t_r0 - 0.2, bk("offer_up", 1, "hopeful", basket=False), depth=5)
    t_r1 = snap(t_r0 + 0.24)
    af.cut(t_r0, dk("andrew", "show_lunch", -1, "kind", basket=False), dip=False)
    add_pass(sc, "pass2", "open", hb_and, hb_boy, t_r0, t_r1, Z_PROP)
    bf.cut(t_r1, bk("offer_up", 1, "happy", basket="open"), dip=False)
    af.cut(snap(t_r1 + 0.25), dk("andrew", "stand", -1, "happy"), depth=4)
    t_turn2 = snap(max(t_r1 + 0.45, t_wg + 0.1))
    bf.cut(t_turn2, bk("stand_basket", -1, "happy", basket="open"), depth=6)

    # '可是': he looks up at Jesus; '交给': he lifts the basket; Jesus bends and takes it
    bf.cut(t_ks3 - 0.05, bk("look_up", -1, "hopeful", basket="open"), depth=5)
    # (the hand-over sits on '交给了', half a second before '耶稣', so the chime is clear of the scene's end)
    t_off = snap(t_jg - 0.3)
    bf.cut(t_off, bk("offer_up", -1, "hopeful", basket="open"), depth=6)
    jf.cut(snap(t_off + 0.1), jk("smile_boy", 1), depth=5)
    t_q0 = snap(max(t_off + 0.5, t_ys - 0.5))
    t_q1 = snap(t_q0 + 0.22)
    hb_boy2 = held_basket(C.the_boy, XB, YG, K, -1, -4, -4, 0.62, pose="offer_up")
    hb_jes = held_basket(C.jesus, XJ, YG, K, 1, -4, 0, 0.72, pose="smile_boy")
    bf.cut(t_q0, bk("offer_up", -1, "hopeful", basket=False), dip=False)
    add_pass(sc, "pass3", "open", hb_boy2, hb_jes, t_q0, t_q1, Z_PROP, lift=6)
    jf.cut(t_q1, jk("smile_boy", 1, item="basket"), dip=False)
    t_back = snap(t_q1 + 0.3)
    bf.cut(t_back, bk("smile", -1), depth=6)
    bf.track.to(t_back + 0.02, t_back + 0.32, XB + 28 * K, YG, lift=12 * K)

    # Peter: kind, a little awed at the end
    pf.cut(snap(t_jg + 0.25), dk("peter", "stand", 1, "awed"), dip=False)

    # blinks and breathing
    for fig_, t_from in ((jf, 0.4), (pf, 0.4), (af, t_stop + 0.6), (bf, t_stop + 0.6)):
        fig_.blinks(t_from, T - 0.4, rng)
    for fig_, ref in ((pf, A_POS["peter"]), (af, A_POS["andrew"])):
        fig_.mots.append(breath(ref, g0, 3.0 + rng.uniform(0, 0.4), 0.010, rng.random()))
    bf.mots.append(breath(BOY0, g0, 2.6, 0.012, 0.3))
    for fig_ in (jf, pf, jaf, jof, phf, manf, womf, mumf, af, bf):
        fig_.build(sc)

    # ---------------------------------------------------------------- the count: five loaves, two fish
    bx, by = held_centre(hb_and)
    CCX, CCY = bx + 10, 528
    loaf_xy = [(CCX - 176 + 88 * i, 454 + 8 * abs(i - 2)) for i in range(5)]
    fish_xy = [(CCX - 70, 566), (CCX + 70, 566)]
    # the glance at the crowd: out and back, each move 1.5 s (sine), around '这么多人'
    t_out0 = snap(max(t_fishes[2] + 0.35, t_zmd - 1.0))
    t_out1 = t_out0 + 1.5
    t_back0 = snap(max(t_out1 + 0.2, t_ydd - 0.85))
    t_back1 = t_back0 + 1.5
    t_shrink = snap(max(t_dd[0] - 0.05, t_back1 - 0.1))      # the counted loaves go home once the camera is back
    t_gone = t_shrink + 0.75

    def gather(t0, x, y, i, fly=True):
        """Pop in at t0; on '这一点点' shrink and fly back into Andrew's basket (numbers just fade)."""
        base = pop_in(t0, (x, y), dur=0.3, s0=0.2)

        def m(t):
            v = base(t)
            if t < t_shrink:
                return v
            if not fly:
                return Tf(alpha=v.alpha * (1 - M.progress(t, t_shrink, t_shrink + 0.18, "sine")), sx=v.sx, sy=v.sy,
                          px=x, py=y)
            # an arc down into the basket, shrinking to the size of the loaves inside it; it drops in at the rim
            a0 = t_shrink + 0.06 * i
            u = M.progress(t, a0, a0 + 0.4, "inout")
            land = M.progress(t, a0 + 0.4, a0 + 0.5, "in")
            tx_, ty_ = bx + (i - 3) * 5, by - 8 * K
            k_ = 1 - 0.7 * u
            return Tf(dx=(tx_ - x) * u, dy=(ty_ - y) * u - 50 * math.sin(math.pi * u) + 10 * land,
                      sx=v.sx * k_, sy=v.sy * k_, alpha=v.alpha * (1 - land), px=x, py=y)
        return m
    t_cloud = snap(t_loaf[0] - 0.22)
    cloud_m = pop_in(t_cloud, (CCX, CCY + 120), dur=0.32, s0=0.35)

    def cloud_mot(t):
        v = cloud_m(t)
        if t < t_shrink + 0.1:
            return v
        u = M.progress(t, t_shrink + 0.1, t_shrink + 0.45, "inout")
        return Tf(sx=v.sx * (1 - 0.35 * u), sy=v.sy * (1 - 0.35 * u), alpha=v.alpha * (1 - u), px=CCX, py=CCY + 60)
    sc.add("cnt_cloud", doc(S.g(S.cloud(CCX, CCY + 12, 470, 165, fill="#fbf4e2", seed=7, puffs=6, sw=3.2),
                                    filter="wobble-fine", opacity=0.95)),
           z=Z_GLOSS - 0.2, motion=cloud_mot)
    for i, ((x, y), tp) in enumerate(zip(loaf_xy, t_loaf)):
        tp = snap(tp - 0.04)
        sc.add(f"cnt_loaf{i}", doc(PR.barley_loaf(x, y, 1.55, 1, "whole", rot=(-8, 4, -3, 7, -5)[i], time=TIME5, seed=i)),
               z=Z_GLOSS, motion=gather(tp, x, y, i))
        sc.add(f"cnt_n{i}", number_svg(x, y + 52, i + 1, 0.52), z=Z_GLOSS + 0.1, wc=0,
               motion=gather(tp + 0.06, x, y + 52, i, False))
        sc.sfx("pop", tp + 0.02, gain_db=-15 - (i % 2), pan=-0.1 + 0.05 * i)
    for i, ((x, y), tp) in enumerate(zip(fish_xy, t_fish)):
        tp = snap(tp - 0.04)
        sc.add(f"cnt_fish{i}", doc(PR.dried_fish(x, y, 1.45, 1 if i else -1, "whole", rot=(-6, 6)[i], time=TIME5)),
               z=Z_GLOSS, motion=gather(tp, x, y, i + 5))
        sc.add(f"cnt_fn{i}", number_svg(x, y + 46, i + 1, 0.52, "#4f86b8"), z=Z_GLOSS + 0.1, wc=0,
               motion=gather(tp + 0.06, x, y + 46, i + 5, False))
        sc.sfx("pop", tp + 0.02, gain_db=-14, pan=0.05 * i)
    sc.fx.append(FX.sparkles((CCX - 300, 380, CCX + 300, 680), count=10, t0=t_loaf[0], t1=t_gone + 0.2,
                             color=(255, 236, 170), size=(6, 12), period=1.1, drift=-8, seed=55))

    # ---------------------------------------------------------------- the gloss: one little basket = one boy's tummy
    GX, GY, GK = 1010, 425, 0.78
    t_c0 = snap(t_wg - 0.08)
    t_c1 = snap(t_ks3 - 0.25)
    sc.add("card", card_svg(GX, GY, GK), z=Z_GLOSS + 1, motion=pop_in(t_c0, (GX, GY), t1=t_c1))
    sc.add("card_basket", doc(PR.lunch_basket(GX - 150 * GK, GY + 72 * GK, 1.9 * GK, 1, state="open", time=TIME5)),
           z=Z_GLOSS + 1.1, motion=pop_in(t_c0 + 0.12, (GX - 150 * GK, GY), dur=0.3, t1=t_c1, s0=0.4))
    t_eq = snap(t_zg - 0.06)
    sc.add("card_eq", arrow_svg(GX + 2, GY - 6, GK), z=Z_GLOSS + 1.1, motion=pop_in(t_eq, (GX, GY), dur=0.25, t1=t_c1))
    boy_frames = [boy_card_svg(GX + 160 * GK, GY + 128 * GK, 0.86 * GK, ph) for ph in (0.0, 0.25, 0.5, 0.75)]
    sc.add("card_boy", boy_frames, z=Z_GLOSS + 1.1, frame_at=lambda t: float(int((t + g0) / 0.16) % 4),
           motion=pop_in(t_eq + 0.15, (GX + 160 * GK, GY + 30 * GK), dur=0.3, t1=t_c1, s0=0.4))

    # ---------------------------------------------------------------- ambience
    sc.fx.append(FX.motes((0, 200, W5, 1100), count=26, color=(255, 236, 190), size=(2, 5), seed=15, alpha=110))

    # ---------------------------------------------------------------- camera
    c_a0 = Cam(965, 690, 1420)
    c_a1 = Cam(950, 698, 1370)
    camA = zoom_cam([(0, c_a0), (1.0, c_a0), (t_cut, c_a1)], ["linear", "sine"])
    c_b0 = Cam(2465, 690, 1760)
    c_b1 = Cam(2400, 692, 1740)
    c_walk = Cam(2080, 700, 1760)
    c_mid = Cam(1480, 702, 1600)
    c_two = Cam(935, 705, 1440)
    c_show = Cam(925, 680, 1350)
    c_wide = Cam(1520, 625, 2222)
    c_show2 = Cam(915, 690, 1370)
    c_gloss = Cam(900, 650, 1480)
    c_offer = Cam(840, 725, 1250)
    camB = zoom_cam([(t_cut, c_b0), (t_zsh - 0.1, c_b1), (t_w0 + 0.2, c_walk), (t_w0 + 0.55 * (t_w1 - t_w0), c_mid),
                     (t_stop + 0.5, c_two), (t_zl, c_two), (t_dz + 0.2, c_show), (t_out0, c_show),
                     (t_out1, c_wide), (t_back0, c_wide), (t_back1, c_show2), (max(t_l2e + 0.1, t_back1 + 0.2), c_show2),
                     (t_wg + 0.6, c_gloss), (t_ks3 - 0.1, c_gloss), (t_jg + 0.2, c_offer), (T, c_offer)],
                    ["sine", "sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear", "sine", "linear",
                     "sine", "linear", "sine", "linear"])
    sc.camera = cut_cam([(0, camA), (t_cut, camB)])

    # ---------------------------------------------------------------- sound
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-24, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("wind_soft", 0, dur=T + 0.5, gain_db=-26, fade_in=0.8, fade_out=1.0)
    sc.sfx("crowd", 0, dur=T + 0.5, gain_db=-22, fade_in=0.8, fade_out=1.0, pan=0.25)
    sc.sfx("crowd", t_cut, dur=t_w0 - t_cut + 0.6, gain_db=-18, fade_in=0.1, fade_out=0.8, pan=0.3)
    sc.sfx("cloth", t_ni - 0.1, gain_db=-22)
    sc.sfx("cloth", t_qu - 0.05, gain_db=-21)
    sc.sfx("footsteps", t_ba + 0.1, dur=0.8, gain_db=-24, fade_out=0.3, pan=0.3)
    sc.sfx("footsteps", t_w0 - 0.1, dur=t_stop - t_w0 + 0.3, gain_db=-20, fade_in=0.2, fade_out=0.3, pan=0.1)
    sc.sfx("cloth", t_p0, gain_db=-18)
    sc.sfx("cloth", t_p1, gain_db=-15)
    sc.sfx("whoosh", t_shrink + 0.05, gain_db=-21)
    sc.sfx("pop", t_shrink + 0.48, gain_db=-21)                          # they drop into the basket
    sc.sfx("cloth", t_r0, gain_db=-19)
    sc.sfx("pop", t_c0, gain_db=-19, pan=-0.3)
    sc.sfx("pop", t_eq + 0.15, gain_db=-19, pan=-0.3)
    sc.sfx("cloth", t_off, gain_db=-18)
    sc.sfx("chime", t_q1, gain_db=-17)
    return sc
