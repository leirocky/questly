"""Scene 8 - Luke 19:8. The dinner in Zacchaeus's fine house: Zacchaeus stands up and makes his promise; the money chest
opens; two picture-book glosses explain '一半' and '四倍'. One continuous shot in the dining room (props.zacchaeus_house
interior at the golden hour), the same stage as s09_saved (a plain 1 s fade: the last second here is s09's first second
without the gloss card, so the card fades out in the dissolve while everything else holds still).

The table: John and Peter (the Storm film's disciples, 'sit'), Jesus (sit_table) and Zacchaeus at the right end of the
bench (sit_table, his feet dangle); the money chest stands against the back wall behind him.

Beats (syllable onsets measured in the voice clips with the Noah film's voice_marks helpers through the Lost Sheep film's
Beats; nothing is hard-coded to the take). Times are for the current take:
  0 .. 1.0      calm page (the paper dip from s07 lands here): the wide room, lamps flickering, golden light through the
                windows, everyone at the table, Zacchaeus beaming beside Jesus
  '在撒该家里' 0.95  the camera draws slowly in to the table
  '站' 2.84      Zacchaeus stands up (stand_speak, nervous: a sweat drop) and on '起来' hops down to the end of the table,
                facing Jesus; the disciples look up at him
  '对耶稣说'     he takes a breath, nervous
  '主啊' 5.55    promise (brave): a hand on his heart, the other raised; the camera eases toward him and Jesus
  '一半' 8.14    the money chest behind him opens (chest 0 -> 1 in 4 steps, golden shine, coins + sparkle); Peter is amazed
  '穷人'         Jesus nods
  '我以前' 9.99  stand_speak (determined): explaining
  '还他四倍' 12.9 promise again (determined) with a little bounce on '四'; the disciples are amazed
  '一半' 14.74   the camera eases back; a cream picture-book card pops up over the wall (pop)
  '十块' 16.12   ten gold coins drop onto the card in a row (coins)
  '五块' 17.28   they slide into two piles of five (p 0 -> .5 in 1/8 steps)
  '给穷人' 17.71  one pile moves into an alms bowl and a heart appears (p .5 -> 1; sparkle)
  '四倍' 19.08   the first card pops away and the second pops up
  '一块钱' 20.97  one coin and an arrow
  '四块钱' 22.32  four coins pop out one by one (p in 1/8 steps, a pop each)
  end           calm hold; the card fades out in the dissolve into s09

The stage, the set, the figure keys and the timing helpers are shared with s09_saved and s10_heart.
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
from stories.lost_sheep.scenes.s08_search import Beats, Track, blink_expr, env, flicker, gfx  # noqa: F401
from stories.noah.scenes.s01_title import snap

INK = S.INK

# ------------------------------------------------------------------ stage: the dining room (shared with s09)
W8, H8 = 2200, 1420
ROOM = (1100, 1000)                 # zacchaeus_house(view='interior') anchor at scale 1: the room fills the stage
RS = 1.0
FS = 1.12                           # people scale at the table
LIGHT_T = 0.5                       # golden hour through the windows
TY = 1150                           # the dining table's front edge (floor)
FY = TY - PR.DINING_TABLE_DEPTH * FS    # the guests' floor line behind it
SEAT_Y = FY - PR.DINING_BENCH_H * FS    # the bench seat (Zacchaeus sit_table anchor)
TABLE_X, TABLE_W = 868, 856
BENCH_W = 800
X_JOHN, X_PETER, X_JESUS, X_ZAC = 500, 760, 1015, 1258
X_ZSTAND = 1468                     # Zacchaeus standing at the right end of the table, in front of his chest
CHEST = PR.local_to_stage(ROOM[0], ROOM[1], RS, 1, *PR.ZAC_ROOM_CHEST)
LAMPS = [PR.local_to_stage(ROOM[0], ROOM[1], RS, 1, lx, -830) for lx in (-760, -260, 260, 760)]   # flame bases
WINDOWS = [PR.local_to_stage(ROOM[0], ROOM[1], RS, 1, wx, -300) for wx in (-560, 0, 560)]

CAM_WIDE = Cam(1100, 640, 2190)
CAM_TABLE = Cam(1112, 846, 1420)
CAM_PROMISE = Cam(1232, 842, 1270)
CAM_GLOSS = Cam(1110, 836, 1500)     # the end of s08 = the start of s09


def doc(body, defs=""):
    return S.svg_doc(body, defs, W8, H8)


def f1(v):
    return f"{v:.1f}"


# ------------------------------------------------------------------ motion helpers
def squash(t0, s, piv, depth=7.0):
    """Squash-dip whose bottom is at t0 (a pose cut hides there)."""
    return M.keys([(t0 - 0.14, {"dy": 0, "sy": 1}), (t0, {"dy": depth * s, "sy": 0.95}),
                   (t0 + 0.13, {"dy": -3 * s, "sy": 1.015}), (t0 + 0.28, {"dy": 0, "sy": 1})],
                  ["in", "out", "sine"], pivot=piv)


def bounce(t0, s, piv, height=14.0, dur=0.34):
    """A small happy bounce starting at t0."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf()
        v = u / dur
        return Tf(dy=-height * s * math.sin(math.pi * v), sy=1 + 0.02 * math.sin(math.pi * v), px=piv[0], py=piv[1])
    return m


def nod(t0, s, piv, depth=6.0, dur=0.42):
    """A gentle nod: the figure dips and tips forward a little (rotation about the seat / feet)."""
    def m(t):
        u = t - t0
        if u < 0 or u > dur:
            return Tf()
        k = math.sin(math.pi * u / dur)
        return Tf(dy=depth * s * k, rot=1.6 * k, px=piv[0], py=piv[1])
    return m


def breath(piv, g0, period=3.0, amount=0.011, phase=0.0):
    """Breathing on the film's global clock (g0 = ctx.start): identical in two scenes joined by a plain fade."""
    return lambda t: Tf(sx=1 + 0.35 * amount * math.sin(2 * math.pi * ((t + g0) / period + phase)),
                        sy=1 + amount * math.sin(2 * math.pi * ((t + g0) / period + phase)), px=piv[0], py=piv[1])


def pop_in(t0, piv, dur=0.32, t1=None, out=0.24, s0=0.55):
    """Pop in at t0 (scale with a back ease, quick fade in); pop out ending at t1."""
    def m(t):
        if t < t0 - 1e-6 or (t1 is not None and t > t1):
            return Tf(alpha=0.0)
        s = s0 + (1 - s0) * M.progress(t, t0, t0 + dur, "back")
        a = M.progress(t, t0, t0 + 0.12, "sine")
        if t1 is not None:
            u = M.progress(t, t1 - out, t1, "in")
            s *= 1 - 0.3 * u
            a *= 1 - u
        return Tf(sx=s, sy=s, px=piv[0], py=piv[1], alpha=a)
    return m


def clamp_cam(c, w=W8, h=H8):
    cw = min(c.w, w, h * 16 / 9)
    ch = cw * 9 / 16
    return Cam(min(max(c.x, cw / 2 + 1), w - cw / 2 - 1), min(max(c.y, ch / 2 + 1), h - ch / 2 - 1), cw, c.rot)


def cam_path(keys, curves, w=W8, h=H8):
    f = M.cam_keys([(t, clamp_cam(c, w, h)) for t, c in keys], curves)
    return lambda t: clamp_cam(f(t), w, h)


def stepped(times, values):
    """frame_at helper: value index that switches at each time (hard cuts)."""
    tv = sorted(zip(times, values))

    def fa(t):
        v = tv[0][1] if t >= tv[0][0] else values[0]
        cur = 0
        for tk, i in tv:
            if t >= tk:
                cur = i
        return float(cur)
    return fa


# ------------------------------------------------------------------ the figure: a flipbook with hard cuts
class Fig:
    """One figure on its own flipbook layer. States are hashable keys drawn by ``draw(key)`` (markup at absolute stage
    coordinates, reference anchor ``ref``); ``cut`` switches state with a hard cut (hidden in a squash dip unless
    dip=False). ``track`` (Track) moves the drawing; ``mots`` adds extra motions (breathing, nods)."""

    def __init__(self, name, draw, ref, z, s=FS, seed=0, wc=1.0, track=None, docf=None):
        self.name, self.draw, self.ref, self.z, self.s, self.seed, self.wc = name, draw, ref, z, s, seed, wc
        self.ents, self.dips, self.mots = [], [], []
        self.track = track or Track(*ref)
        self.alpha = None
        self.docf = docf or doc

    def cut(self, t, key, dip=True, depth=7.0):
        t = snap(t) if t > 0 else 0.0
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

    def blinks(self, closed, t_from, t_to, rng, every=(2.3, 4.0)):
        """closed(key) -> the closed-eye key (or None); no blink within 0.35 s of another cut."""
        t = t_from + rng.uniform(0.3, 1.4)
        cut_ts = [tk for tk, _ in self.ents if tk > 0]
        while t < t_to - 0.3:
            cur = self.key_at(t)
            ck = closed(cur) if cur is not None else None
            if ck is not None and all(abs(t - tk) > 0.35 for tk in cut_ts):
                self.ents += [(snap(t), ck), (snap(t + 0.13), cur)]
            t += rng.uniform(*every)
        return self

    def motion(self):
        px, py = self.ref
        tr = self.track

        def base(t):
            x, y, k, _ = tr(t)
            return Tf(dx=x - px, dy=y - py, sx=k, sy=k, px=px, py=py)
        mots = [base] + [squash(td, self.s, self.ref, depth) for td, depth in self.dips] + self.mots
        if self.alpha is not None:
            al = self.alpha
            mots.append(lambda t: Tf(alpha=al(t)))
        return M.combine(*mots)

    def build(self, sc):
        ents = sorted(self.ents, key=lambda e: e[0])
        names = []
        for _, n in ents:
            if n not in names:
                names.append(n)
        frames = [self.docf(self.draw(n)) for n in names]
        index = {n: i for i, n in enumerate(names)}

        def fa(t):
            cur = ents[0][1]
            for tk, n in ents:
                if t >= tk:
                    cur = n
            return float(index[cur])
        sc.add(self.name, frames if len(frames) > 1 else frames[0], frame_at=fa if len(frames) > 1 else None,
               z=self.z, seed=self.seed, wc=self.wc, motion=self.motion())
        return self


# ------------------------------------------------------------------ the people at the table
def zac_key(pose, f=-1, expr=None, phase=0.0, purse=True):
    return ("zac", pose, f, expr, round(phase, 3), purse)


def zac_anchor(pose):
    return (X_ZAC, SEAT_Y) if pose == "sit_table" else (X_ZSTAND, FY)


def zac_draw(key):
    _, pose, f, expr, phase, purse = key
    x, y = zac_anchor(pose)
    return C.zacchaeus(x, y, FS, f, pose=pose, expr=expr, phase=phase, purse=purse)


def jesus_key(pose="sit_table", expr=None):
    return ("jesus", pose, expr)


def jesus_draw(key):
    _, pose, expr = key
    return C.jesus(X_JESUS, FY, FS, 1, pose=pose, expr=expr)


def disc_key(v, expr="kind"):
    return ("disc", v, expr)


def disc_draw(key):
    _, v, expr = key
    x = X_PETER if v == "peter" else X_JOHN
    return C.disciples(x, FY, FS, 1, variant=v, pose="sit", expr=expr)


NATURAL = {"sit_table": {"zac": "happy", "jesus": "warm"}, "sit_smile": {"jesus": "smile"}, "sit_bless": {"jesus": "kind"},
           "sit_speak_joy": {"jesus": "speak_joy"}, "stand_speak": {"zac": "nervous"}, "promise": {"zac": "brave"}}


def closed_key(key):
    """The closed-eye variant of a figure key (for blinks); None when the eyes are already closed."""
    if key is None:
        return None
    who = key[0]
    if who == "zac":
        _, pose, f, expr, phase, purse = key
        e = expr or NATURAL.get(pose, {}).get("zac", "happy")
        if e in ("grateful", "overjoyed", "speak_joy", "laugh"):
            return None
        return zac_key(pose, f, blink_expr(e), phase, purse)
    if who == "jesus":
        _, pose, expr = key
        e = expr or NATURAL.get(pose, {}).get("jesus", "warm")
        if e in ("smile", "speak_joy", "peaceful"):
            return None
        return jesus_key(pose, blink_expr(e))
    if who == "disc":
        _, v, expr = key
        if expr in ("happy", "joyful", "peaceful"):
            return None
        return disc_key(v, blink_expr(expr))
    return None


# ------------------------------------------------------------------ the set
def room_svg(chest=0.0):
    return doc(PR.zacchaeus_house(ROOM[0], ROOM[1], RS, 1, view="interior", time=LIGHT_T, lamp=1.0, chest=chest,
                                  part="back"))


def lamp_glow_svg(x, y, k=1.0):
    gid = f"z8lamp{int(x)}"
    defs = S.rad_grad(gid, [(0, "#fff3c8", 0.85), (0.35, "#ffd27a", 0.38), (1, "#ffc060", 0)])
    return doc(f'<ellipse cx="{f1(x)}" cy="{f1(y - 6)}" rx="{f1(230 * k)}" ry="{f1(210 * k)}" fill="url(#{gid})"/>', defs)


def flame_svg(x, y, i):
    """A little lamp flame (redrawn over the lamp bowl so it can flicker)."""
    h = (30, 34, 28)[i % 3]
    lean = (-3, 2, 4)[i % 3]
    d = f"M{f1(x - 8)},{f1(y)} Q{f1(x - 9)},{f1(y - h * 0.5)} {f1(x + lean)},{f1(y - h)} Q{f1(x + 9)},{f1(y - h * 0.5)} {f1(x + 8)},{f1(y)} Z"
    di = f"M{f1(x - 4)},{f1(y)} Q{f1(x - 4)},{f1(y - h * 0.35)} {f1(x + lean * 0.6)},{f1(y - h * 0.62)} Q{f1(x + 4)},{f1(y - h * 0.35)} {f1(x + 4)},{f1(y)} Z"
    return f'<path d="{d}" fill="#f6a43c" stroke="{INK}" stroke-width="2"/><path d="{di}" fill="#fff0b8"/>'


def beams_svg():
    """Slanting golden-hour sunbeams from the three windows across the floor (a screen layer)."""
    gid = "z8beam"
    defs = S.lin_grad(gid, [(0, "#fff0c0", 0.55), (0.6, "#ffd890", 0.22), (1, "#ffd890", 0)], x1=0, y1=0, x2=0.35, y2=1)
    b = ""
    for wx, wy in WINDOWS:
        b += (f'<path d="M{f1(wx - 100)},{f1(wy - 380)} L{f1(wx + 100)},{f1(wy - 380)} L{f1(wx + 420)},{f1(wy + 640)} '
              f'L{f1(wx + 40)},{f1(wy + 640)} Z" fill="url(#{gid})"/>')
    return doc(f'<g filter="url(#blur-md)">{b}</g>', defs)


def table_svg():
    return doc(PR.dining_table(TABLE_X, TY, FS, width=TABLE_W, seed=4))


def bench_svg():
    return doc(PR.dining_bench(TABLE_X, FY, FS, width=BENCH_W))


def front_svg():
    return doc(PR.zacchaeus_house(ROOM[0], ROOM[1], RS, 1, view="interior", time=LIGHT_T, part="front"))


def steam_svg(x, y, i):
    d = (f"M{f1(x)},{f1(y)} c{-10 - 3 * i},-14 {10 + 2 * i},-26 0,-42 c-10,-14 8,-26 0,-40")
    return doc(f'<path d="{d}" fill="none" stroke="#fffaf0" stroke-width="5" stroke-linecap="round" opacity="0.75" '
               f'filter="url(#soft)"/>')


def pillars_in_view(cam):
    """The room's front pillars stand at the stage's left and right edges; skip their layer when it is out of view."""
    return cam.x - cam.w / 2 < 165 or cam.x + cam.w / 2 > W8 - 165


def add_set(sc, g0, chest_fa=None, chest_vals=(0.0,), beam_boost=None):
    """The room (a chest flipbook if chest_fa), the bench, the lamps' flicker, the sunbeams (beam_boost(t) 0..1
    brightens them) and the motes."""
    if chest_fa is None or len(chest_vals) == 1:
        sc.add("room", room_svg(chest_vals[0]), z=0, seed=3)
    else:
        sc.add("room", [room_svg(c) for c in chest_vals], z=0, frame_at=chest_fa, seed=3)
    def beam_a(t):
        a = 0.75 + 0.18 * math.sin(2 * math.pi * (t + g0) / 7.3)
        b = 0.75 * beam_boost(t) if beam_boost else 0.0
        return Tf(alpha=a * (1 - b) + b)
    sc.add("beams", beams_svg(), z=0.5, wc=0, blend="screen", seed=5, motion=beam_a)
    for i, (lx, ly) in enumerate(LAMPS):
        fl = flicker(g0, 0.85, 0.15, seed=1.7 * i)
        sc.add(f"lampglow{i}", lamp_glow_svg(lx, ly), z=0.6, wc=0, blend="screen", seed=11 + i,
               motion=lambda t, fl=fl: Tf(alpha=0.36 * fl(t)))
        fl2 = flicker(g0, 1.0, 0.12, seed=0.9 + 1.3 * i)
        sc.add(f"flame{i}", doc(flame_svg(lx, ly, i)), z=0.7, wc=0.4, seed=17 + i,
               motion=lambda t, fl2=fl2, lx=lx, ly=ly: Tf(sx=0.92 + 0.1 * fl2(t), sy=0.85 + 0.2 * fl2(t), px=lx, py=ly))
    sc.add("bench", bench_svg(), z=1, seed=23)
    sc.add("table", table_svg(), z=8, seed=29)
    sc.add("front", front_svg(), z=9, seed=37,
           motion=lambda t: Tf(alpha=1.0 if pillars_in_view(sc.camera(t)) else 0.0))
    # steam from the bread
    bx = TABLE_X + (-0.22 * TABLE_W / 2) * FS
    by = TY - (PR.DINING_TABLE_H + 22) * FS
    for i in range(2):
        per = 2.6
        ph = i * 0.5

        def stm(t, ph=ph, per=per, bx=bx, by=by):
            u = ((t + g0) / per + ph) % 1.0
            return Tf(dy=-70 * u, dx=6 * math.sin(2 * math.pi * u), sx=0.8 + 0.4 * u, sy=0.8 + 0.4 * u, px=bx,
                      py=by, alpha=0.7 * math.sin(math.pi * u))
        sc.add(f"steam{i}", steam_svg(bx - 14 + 28 * i, by, i), z=8.5, wc=0, motion=stm, seed=41 + i)
    sc.fx.append(gfx(FX.motes, g0, rect=(300, 300, 1950, 1150), count=26, color=(255, 236, 190), size=(2.5, 5.5),
                     seed=81, alpha=120))
    sc.fx.append(FX.vignette(lambda t: 0.3, color=(70, 36, 22)))


def add_chest_shine(sc, g0, t_on, T):
    """The open chest's golden shine (from t_on) and twinkles; global-clock pulses, so s09 continues them."""
    cx_, cy_ = CHEST
    sc.fx.append(gfx(FX.sparkles, g0, t0=t_on, t1=T + 2, rect=(cx_ - 120, cy_ - 330, cx_ + 120, cy_ - 170),
                     count=8, color=(255, 238, 170), size=(7, 13), period=1.7, drift=0, seed=83))
    gid = "z8chestglow"
    sc.add("chest_glow", doc(f'<ellipse cx="{f1(cx_)}" cy="{f1(cy_ - 200)}" rx="260" ry="200" fill="url(#{gid})"/>',
                             S.rad_grad(gid, [(0, "#fff2c0", 0.8), (0.5, "#ffd070", 0.3), (1, "#ffd070", 0)])),
           z=2.5, wc=0, blend="screen", seed=47,
           motion=lambda t: Tf(alpha=env(t, t_on - 0.15, 1e9, 0.5) * (0.85 + 0.15 * math.sin(2 * math.pi * (t + g0) / 2.1))))


def add_people(sc, g0, rng, zac_ents, jesus_ents, peter_ents, john_ents, t_end, blink_from=0.0, zac_track=None,
               zac_mots=(), jesus_mots=(), peter_mots=(), john_mots=()):
    """The four at the table as Fig layers; *_ents = [(t, key, dip)] cuts. Returns the figs."""
    figs = {}
    spec = [("john", disc_draw, (X_JOHN, FY), 3.0, john_ents, john_mots, 0.0),
            ("peter", disc_draw, (X_PETER, FY), 3.2, peter_ents, peter_mots, 0.21),
            ("jesus", jesus_draw, (X_JESUS, FY), 3.4, jesus_ents, jesus_mots, 0.43),
            ("zac", zac_draw, (X_ZSTAND, FY), 3.6, zac_ents, zac_mots, 0.67)]
    for name, draw, ref, z, ents, mots, ph in spec:
        fg = Fig(name, draw, ref, z, seed=31 + int(z * 10), track=zac_track if name == "zac" else None)
        for tk, key, dip in ents:
            fg.cut(tk, key, dip=dip)
        fg.blinks(closed_key, blink_from, t_end, rng)
        piv = (ref[0], FY - 60 * FS)
        fg.mots += [breath(piv, g0, 2.9 + 0.3 * ph, 0.010, ph)] + list(mots)
        fg.build(sc)
        figs[name] = fg
    return figs


# ------------------------------------------------------------------ the glosses
CARD_PATH = ("M-286,-138 Q-290,-152 -272,-154 L272,-154 Q290,-152 286,-138 L280,138 Q278,152 262,154 L-262,154 "
             "Q-280,152 -282,138 Z")


def heading_svg(cx, cy, k, txt):
    """The card's heading ('一半' / '四倍'), LXGW WenKai on a text layer (wc=0)."""
    return doc(f'<text x="{f1(cx)}" y="{f1(cy - 82 * k)}" font-family="LXGW WenKai" font-weight="bold" '
               f'font-size="{f1(50 * k)}" fill="#8a4a2a" text-anchor="middle">{txt}</text>')


def card_svg(cx, cy, k):
    """The cream card of props.coins_gloss (the same paths), drawn alone so the coins can arrive on their own."""
    art = PR._p(CARD_PATH, "#fbf3e0", 4.0)
    art += PR._p("M-266,-134 L266,-134 L262,134 L-262,134 Z", "none", 2.0, stroke="#e2c79a",
                 extra='stroke-dasharray="7 6"')
    shadow = (f'<g transform="translate({f1(cx + 10)},{f1(cy + 14)}) scale({k:.4f})"><path d="{CARD_PATH}" '
              f'fill="#7a4a2c" opacity="0.18" filter="url(#soft)"/></g>')
    return doc(shadow + PR._place(art, cx, cy, k))


def gloss_svg(cx, cy, k, kind, p):
    return doc(PR.coins_gloss(cx, cy, k, kind=kind, progress=p, card=False, labels=True))


def build(ctx):
    sc = Scene(ctx, W=W8, H=H8)
    T = ctx.duration
    g0 = ctx.start
    bt = Beats(ctx)
    rng = random.Random(8)

    # ---- beats
    t_zai = bt.at(0, "在撒该家里")
    t_zhan = bt.at(0, "站")
    t_qi = bt.at(0, "起")
    t_dui = bt.at(0, "对耶稣说")
    t_l0_end = bt.end(0, "对耶稣说")
    t_zhu = bt.at(1, "主啊")
    t_qian1 = bt.at(1, "钱")
    t_yi1 = bt.at(1, "一半")
    t_ban1 = bt.at(1, "半")
    t_qiong1 = bt.at(1, "穷人")
    t_yiqian = bt.at(1, "我以前")
    t_huan = bt.at(1, "还他")
    t_si1 = bt.at(1, "四倍")
    t_l1_end = bt.end(1, "我就还他四倍")
    t_yb = bt.at(2, "一半")
    t_shi = bt.at(2, "十块")
    t_wu = bt.at(2, "五块")
    t_gei = bt.at(2, "给穷人")
    t_ren = bt.at(2, "人")
    t_l2_end = bt.end(2, "分五块给穷人")
    t_sb = bt.at(3, "四倍")
    t_yk = bt.at(3, "一块钱")
    t_sk = bt.at(3, "四块钱")
    t_l3_end = bt.end(3, "要还四块钱")

    # ---- the room: the chest opens on '一半'
    chest_vals = (0.0, 0.25, 0.5, 0.75, 1.0)
    t_ch = snap(t_yi1)
    ch_times = [0.0] + [snap(t_ch + 0.1 * i) for i in range(4)]
    add_set(sc, g0, stepped(ch_times, range(5)), chest_vals)
    add_chest_shine(sc, g0, t_ch + 0.3, T)

    # ---- Zacchaeus
    zt = Track(X_ZSTAND, FY)
    t_up = snap(t_zhan - 0.04)
    zt.to(t_up, t_up, X_ZAC + 24, FY)                          # standing up behind the bench ...
    t_h0 = snap(max(t_qi + 0.05, t_up + 0.3))
    zt.to(t_h0, t_h0 + 0.36, X_ZSTAND, FY, lift=34)            # ... and hopping down to the end of the table
    k_sit = zac_key("sit_table", -1, "happy")
    k_nerv = zac_key("stand_speak", -1, "nervous")
    k_prom = zac_key("promise", -1, "brave")
    k_expl = zac_key("stand_speak", -1, "determined")
    k_prom2 = zac_key("promise", -1, "determined")
    k_rest = zac_key("stand_speak", -1, "tender")
    t_prom2 = snap(t_huan - 0.2)
    t_rest = snap(t_l1_end + 0.45)
    zac_ents = [(0, k_sit, False), (t_up, k_nerv, True), (snap(t_zhu - 0.12), k_prom, True),
                (snap(t_yiqian - 0.1), k_expl, True), (t_prom2, k_prom2, True), (t_rest, k_rest, True)]
    zmots = [bounce(snap(t_si1 - 0.05), FS, (X_ZSTAND, FY), 12),
             bounce(t_zai + 0.35, FS, (X_ZSTAND, FY), 9, 0.3),          # beaming in his seat: Jesus is at his table
             # a nervous breath before '主啊'
             M.keys([(t_l0_end + 0.15, {"sy": 1.0}), (t_l0_end + 0.55, {"sy": 1.025}), (t_zhu - 0.3, {"sy": 1.0})],
                    "sine", pivot=(X_ZSTAND, FY))]

    # ---- Jesus: warm, listening; a nod at '穷人' and at '四倍'
    jesus_ents = [(0, jesus_key("sit_table"), False)]
    jmots = [nod(t_qiong1 + 0.1, FS, (X_JESUS, FY - 70 * FS)), nod(t_l1_end + 0.1, FS, (X_JESUS, FY - 70 * FS))]

    # ---- the disciples
    peter_ents = [(0, disc_key("peter", "happy"), False), (t_zhan + 0.25, disc_key("peter", "kind"), False),
                  (t_ban1 + 0.1, disc_key("peter", "amazed"), True), (t_qiong1 + 0.6, disc_key("peter", "happy"), False),
                  (t_si1 + 0.1, disc_key("peter", "amazed"), True), (t_l1_end + 0.8, disc_key("peter", "happy"), False)]
    john_ents = [(0, disc_key("john", "happy"), False), (t_zhan + 0.35, disc_key("john", "kind"), False),
                 (t_ban1 + 0.25, disc_key("john", "awed"), False), (t_qiong1 + 0.8, disc_key("john", "happy"), False),
                 (t_si1 + 0.2, disc_key("john", "amazed"), True), (t_l1_end + 1.0, disc_key("john", "kind"), False)]
    add_people(sc, g0, rng, zac_ents, jesus_ents, peter_ents, john_ents, T - 1.1, zac_track=zt, zac_mots=zmots,
               jesus_mots=jmots)

    # ---- the glosses (cards float over the wall above the table)
    GX, GY, GK = 900, 622, 0.95
    t_c1 = snap(t_yb - 0.05)
    t_c1_out = snap(t_sb - 0.12)
    sc.add("card1", card_svg(GX, GY, GK), z=20, motion=pop_in(t_c1, (GX, GY), t1=t_c1_out))
    sc.add("head1", heading_svg(GX, GY, GK, "一半"), z=20.2, wc=0, motion=pop_in(t_c1, (GX, GY), t1=t_c1_out))
    half_p = [i / 8 for i in range(9)]
    t_coins = snap(t_shi - 0.04)
    split_t = [snap(t_wu + 0.08 * i) for i in range(1, 5)]
    move_t = [snap(t_gei + 0.12 * i) for i in range(4)]
    half_times = [0.0] + split_t + move_t
    sc.add("gloss1", [gloss_svg(GX, GY, GK, "half", p) for p in half_p], z=20.5, wc=0.5,
           frame_at=stepped(half_times, range(9)), motion=pop_in(t_coins, (GX, GY + 10), dur=0.26, t1=t_c1_out, s0=0.75))
    t_c2 = snap(t_sb + 0.02)
    sc.add("card2", card_svg(GX, GY, GK), z=21, motion=pop_in(t_c2, (GX, GY)))
    sc.add("head2", heading_svg(GX, GY, GK, "四倍"), z=21.2, wc=0, motion=pop_in(t_c2, (GX, GY)))
    t_one = snap(t_yk - 0.04)
    pops = [snap(t_sk + 0.24 * k) for k in range(4)]
    four_times = [0.0]
    for tp in pops:
        four_times += [tp, snap(tp + 0.1)]
    sc.add("gloss2", [gloss_svg(GX, GY, GK, "fourfold", p) for p in half_p], z=21.5, wc=0.5,
           frame_at=stepped(four_times, range(9)), motion=pop_in(t_one, (GX - 190 * GK, GY), dur=0.26, s0=0.5))

    # ---- camera
    t_cam_in = t_zai
    sc.camera = cam_path([(0.0, CAM_WIDE), (t_cam_in, CAM_WIDE), (t_dui + 0.2, CAM_TABLE), (t_zhu - 0.2, CAM_TABLE),
                          (t_yiqian, CAM_PROMISE), (t_l1_end + 0.2, CAM_PROMISE), (t_yb + 0.1, CAM_GLOSS),
                          (T, CAM_GLOSS)],
                         ["linear", "inout", "linear", "inout", "linear", "inout", "linear"])

    # ---- sound
    sc.sfx("birds", 0, dur=T + 0.5, gain_db=-28, fade_in=0.8, fade_out=1.0)
    sc.sfx("fire", 0, dur=T + 0.5, gain_db=-31, fade_in=0.8, fade_out=1.0)
    sc.sfx("cloth", t_up, gain_db=-20, pan=0.3)
    sc.sfx("thud", t_h0 + 0.36, gain_db=-24, pan=0.35)
    sc.sfx("coins", t_ch + 0.05, gain_db=-15, pan=0.45)
    sc.sfx("sparkle", t_ch + 0.25, gain_db=-17, pan=0.45)
    sc.sfx("pop", t_c1, gain_db=-19, pan=-0.3)
    sc.sfx("coins", t_coins, gain_db=-17, pan=-0.3)
    sc.sfx("coins", split_t[0], gain_db=-19, pan=-0.3)
    sc.sfx("coins", move_t[1], gain_db=-20, pan=-0.2)
    sc.sfx("sparkle", move_t[3], gain_db=-18, pan=-0.2)
    sc.sfx("pop", t_c2, gain_db=-19, pan=-0.3)
    sc.sfx("coins", t_one, gain_db=-19, pan=-0.4)
    for i, tp in enumerate(pops):
        sc.sfx("pop", tp, gain_db=-17, pan=-0.3 + 0.1 * i)
    return sc
