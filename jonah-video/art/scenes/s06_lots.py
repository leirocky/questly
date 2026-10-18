"""Scene 6 (v2) — the lots (Jonah 1:7-10).

Line 0 (N)  水手们彼此商量说：
Line 1 (S)  来，我们来抽签，看看是哪个人惹来了这场大风暴！
Line 2 (N)  他们就抽签。结果，抽中的正是约拿！水手们赶紧问他：
Line 3 (S)  请你告诉我们，你是做什么的？你从哪里来？你是哪国人？
Line 4 (J)  我是希伯来人。我敬拜耶和华，天上的上帝。大海和陆地，都是他造的。
Line 5 (N)  耶和华，就是上帝的名字。约拿还告诉他们，他正在逃跑，想要躲开耶和华。水手们听了，更加害怕了，说：
Line 6 (S)  你怎么能做这样的事呢？

On deck in the storm — the approved v1 deck of s05_lots (same far bulwark with shields, mast, torn striped sail,
open hatch, big curling wave beyond the starboard rail, tilting horizon, rain), reused layer by layer.

Line 0: the captain and the four sailors (variants 0-3) huddle round a crate, talking with raised open palms and
hands at their chins (all at chest / face height, clear of the lots jar: nobody touches it before S3 suggests drawing
lots); Jonah stands apart by the open hatch he has just climbed out of, worried.
Line 1: the ginger-bearded sailor (S3, the sailors' voice in this scene) grabs the clay lots jar, lifts it (one
in-between, one squash-hop) high on his open palm ('来，我们来抽签') and rattles it, sets it back (mirrored in-between);
'看看' he draws a plain stick and looks at it held upright before his eyes; the red-headband sailor (S1) draws next
('是哪个人'), then hops upstage-right and walks (planted feet) along the back row behind Jonah to the hatch side;
the sailor behind the crate (S0) draws ('惹来了'); lightning at '大风暴'.
Line 2: S3 beckons; once S1 is past him, Jonah walks over (planted feet) and draws ('他们就抽签'), looks at his stick,
'结果，' looks closer; '抽中的正是约拿！' the stick's mark glows gold, he holds it up, warm light breaks through the
clouds onto him (God is only light; a soft low rumble, only a few sparkles: grave, not a prize), the sailors start
back, drop their plain sticks and point; he steps back into the light. '水手们赶紧问他' they crowd in.
Line 3: S3 asks, gesturing (open hand, pointing, open palm); the others nod in turn.
Line 4: Jonah answers humbly: hand on chest ('我是希伯来人'), eyes closed ('我敬拜耶和华'), arm straight up to heaven
('天上的上帝' — the light brightens, the sailors look up), a paper turn to sweep an open palm up at the towering sea
('大海' — a wave bursts over the rail), a turn back to point out to the far coast ('和陆地' — green hills, a sandy
shore, trees and a tiny white town, lit by a warm glint through '都是他造的'), both arms open ('都是他造的').
Line 5: '耶和华，就是上帝的名字' the light glows and twinkles, the sailors look up in awe; then Jonah bows his head and
tells them he is running away — a thought bubble shows a little Jonah running away from the golden light; '更加害怕了'
thunder, and the sailors gasp and hop back, hands at their heads (the captain clutches his cap); the far land fades
into the rain.
Line 6: S3 spreads his arms '你怎么能做这样的事呢？'; Jonah stands sorry with his head bowed — the calm, held final
frame, which is exactly s07's opening frame (same marks, poses, camera, plain coast, dropped lots).

Every pose change is a hard cut sold by a small squash-and-hop (no crossfades between poses); moves are hops or
planted-foot walks; every main pose is held >= 0.5 s whatever the voice take (min-hold rules on the derived times);
all key times come from the narration (sub-phrases timed from the punctuation pauses in the voice takes — ignored if
a take's length does not match the timeline — with a proportional fallback).

Stage 2112 x 1240 (the v1 deck world; v1 layers are re-hosted on this canvas).
"""
import math
import re

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s05_lots as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene

W, H = V.W, 1240
INK = S.INK
FR = 1 / 30

# ---- where things are (v1 deck: mast 820..878, hatch centre 1790, wave beyond the starboard rail)
X_C, Y_CRATE, CRATE_S = 1232, 992, 1.15          # the crate the lots jar stands on (ground line of its foot)
CRATE_A = (X_C, Y_CRATE - 46 * CRATE_S)          # crate anchor (centre)
JAR = (X_C + 9 * CRATE_S, CRATE_A[1] - 48 * CRATE_S)   # lots jar on the crate (bottom centre)
MOUTH = (JAR[0], JAR[1] - 78)
JY = 1000                                         # Jonah's ground line
J_START = 1652                                    # Jonah by the open hatch
J_END = 1592                                      # Jonah in the light after the lot falls on him
FRONT_Y = 1014
CAPT_S = 1.02
SWAY_PIVOT = V.SWAY_PIVOT


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=H)


def rehost(svg):
    """A v1 layer (drawn on the 2112 x 2120 v1 canvas) on this scene's 2112 x 1240 canvas."""
    a = f'height="{V.SH}" viewBox="0 0 {W} {V.SH}"'
    assert a in svg
    return svg.replace(a, f'height="{H}" viewBox="0 0 {W} {H}"', 1)


# ============================================================== narration timing (as in v2 s05)

PUNCT = "，。！？：；、,.!?:;"


def _subphrases(text):
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in PUNCT:
            out.append(cur)
            cur = ""
    if cur.strip():
        out.append(cur)
    return out


def _nchar(s):
    return max(1, sum(1 for ch in s if ch not in PUNCT and not ch.isspace()))


def _voice_gaps(path, expect=None):
    """Silent stretches (>= 70 ms) inside a voice take: [(start, end)] in seconds, or [] if unreadable — or if the
    take's length differs from the timeline's (``expect``) by more than 0.1 s: then the take on disk is not the one
    the timeline was laid out from (voices being re-generated), and its pauses would be misplaced."""
    try:
        import soundfile as sf
        x, sr = sf.read(str(path), dtype="float32")
    except Exception:
        return []
    if expect is not None and abs(len(x) / sr - expect) > 0.1:
        return []
    if x.ndim == 2:
        x = x.mean(axis=1)
    hop = sr // 100
    nb = len(x) // hop
    if nb < 10:
        return []
    e = np.sqrt((x[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1))
    sil = e < 0.02 * e.max()
    gaps, i = [], 0
    while i < nb:
        if sil[i]:
            j = i
            while j < nb and sil[j]:
                j += 1
            if j - i >= 7 and i > 0 and j < nb:
                gaps.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return gaps


class Phrases:
    """Every punctuation-delimited piece of every line, timed: subtitle chunks first, then the pauses in the voice
    take inside a chunk (the pause nearest to a proportional estimate), then the estimate itself."""

    def __init__(self, ctx):
        self.items = []          # (text, start, end, line index)
        self.gaps = []
        for i, ln in enumerate(ctx.lines):
            gaps = [(ln.start + a, ln.start + b)
                    for a, b in _voice_gaps(BUILD / "voice" / "lines" / f"{ctx.id}_{i:02d}.wav", ln.end - ln.start)]
            self.gaps += gaps
            spans = [(c.text, c.start, c.end) for c in (ln.chunks or [])] or [(ln.text, ln.start, ln.end)]
            for text, c0, c1 in spans:
                subs = _subphrases(text)
                n = [_nchar(s) for s in subs]
                tot, acc, bounds, used = sum(n), 0, [], set()
                for k in range(len(subs) - 1):
                    acc += n[k]
                    est = c0 + (c1 - c0) * acc / tot
                    best = None
                    for gi, (a, b) in enumerate(gaps):
                        if gi in used or not (c0 + 0.15 < a and b < c1 - 0.1):
                            continue
                        if bounds and a <= bounds[-1][1]:
                            continue
                        d = abs((a + b) / 2 - est)
                        if d < 0.7 and (best is None or d < best[0]):
                            best = (d, gi, a, b)
                    if best:
                        used.add(best[1])
                        bounds.append((best[2], best[3]))
                    else:
                        bounds.append((est - 0.05, est + 0.05))
                s = c0
                for k, sub in enumerate(subs):
                    e = bounds[k][0] if k < len(bounds) else c1
                    self.items.append((sub, s, e, i))
                    if k < len(bounds):
                        s = bounds[k][1]

    def find(self, key, line=None):
        for it in self.items:
            if key in it[0] and (line is None or it[3] == line):
                return it
        return None

    def start(self, key, default, line=None):
        it = self.find(key, line)
        return it[1] if it else default

    def end(self, key, default):
        it = self.find(key)
        return it[2] if it else default

    def inner(self, key, sub, default):
        """Time at which ``sub`` starts inside the piece containing ``key`` (snapped to a nearby voice pause; the
        pause at the piece's own start — the lead-in before its first word — is never taken)."""
        it = self.find(key)
        if not it or sub not in it[0]:
            return default
        text, s, e, _ = it
        est = s + (e - s) * _nchar(text[:text.index(sub)]) / _nchar(text)
        best = None
        for a, b in self.gaps:
            if s + 0.2 < a and b < e and abs(b - est) < 0.35 and (best is None or abs(b - est) < abs(best - est)):
                best = b
        return best if best is not None else est


# ============================================================== people

_P = C._P
STAND = C.POSES["stand"]
POSE = {
    # sailors / captain
    "lean": _P(t=16, h=8, arms=(("fk", 40, 95), ("fk", -4, 12)), hands=("open", "fist"), expr="worried"),
    "talk": _P(t=10, h=0, arms=(("fk", 70, 120), ("fk", 6, 20)), hands=("open", "fist"), expr="worried"),
    "chin": _P(t=8, h=4, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
               expr="worried"),
    "nod_lean": _P(t=16, h=22, arms=(("fk", 40, 95), ("fk", -4, 12)), hands=("open", "fist"), expr="worried"),
    # huddle (line 0): talking with raised open palms and hands at the chin, at chest / face height and on their
    # own side of the crate — nobody's hand goes near the lots jar before S3 suggests drawing lots
    "h_talk": _P(t=6, h=2, arms=(("fk", 8, 3), ("fk", 34, 142)), hands=("fist", "open"), expr="worried"),
    "h_talk_nod": _P(t=6, h=18, arms=(("fk", 8, 3), ("fk", 34, 142)), hands=("fist", "open"), expr="worried"),
    "h_both": _P(t=4, h=0, arms=(("fk", 26, 128), ("fk", 22, 138)), hands=("open", "open"), expr="worried"),
    "chin_nod": _P(t=8, h=18, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
                   expr="worried"),
    # the jar shown round on a raised palm (high, so the sailor behind the crate keeps his face)
    "show_jar": _P(t=-6, h=-10, arms=(("fk", 150, 166), ("fk", 40, 100)), hands=("open", "open"), expr="call",
                   look=(0.04, -0.08)),
    "lift_in": _P(t=4, arms=(("fk", 104, 126), ("fk", 40, 96)), hands=("open", "open"), expr="worried"),
    "reach": _P(t=6, legs=((5, 2), (-5, -2)), arms=(("fk", 84, 92), ("fk", -8, -3)), hands=("fist", "fist"),
                expr="worried"),
    "reach_down": _P(t=18, h=10, arms=(("ik", "abs", 82, -170, 1), ("fk", -6, -2)), hands=("fist", "fist"),
                     expr="worried"),
    # looking at a drawn stick: fist up in front of the chin, the stick upright before the eyes (see held_up)
    "look_stick": _P(t=2, h=14, arms=(("ik", "headw", 1.4, 1.15, 1), ("fk", -8, -3)), hands=("fist", "fist"),
                     expr="worried", look=(0.08, 0.06)),
    "relief": _P(t=-2, h=-4, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="neutral"),
    "beckon": _P(t=-2, arms=(("fk", 60, 140), ("fk", -8, -3)), hands=("open", "fist"), expr="neutral"),
    "palm": _P(t=4, h=-2, arms=(("fk", 72, 96), ("fk", -8, -3)), hands=("open", "fist"), expr="worried"),
    "palm_up": _P(t=0, h=-6, arms=(("fk", 96, 128), ("fk", -8, -3)), hands=("open", "fist"), expr="worried"),
    "dismay": _P(t=-4, h=-4, arms=(("fk", 62, 112), ("fk", -58, -10)), hands=("open", "open"), expr="scared"),
    "lookup": _P(t=-3, h=-26, arms=(("fk", 14, 8), ("fk", -8, -3)), look=(0.04, -0.16), expr="worried"),
    "nod": _P(h=18, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="worried"),
    "stand": STAND,
    "point": C.POSES["point"],
    "scared": C.POSES["scared"],
    "worried": C.POSES["worried"],
    "walk_a": C.POSES["walk_a"],
    "walk_b": C.POSES["walk_b"],
    # Jonah
    "j_reach": _P(t=4, legs=((5, 2), (-5, -2)), arms=(("fk", 80, 88), ("fk", -8, -3)), hands=("fist", "fist")),
    "j_look": _P(t=3, h=12, arms=(("ik", "headw", 1.5, 1.2, 1), ("fk", -8, -3)), hands=("fist", "fist"),
                 look=(0.08, 0.06)),
    "j_look2": _P(t=8, h=20, arms=(("ik", "headw", 1.2, 0.95, 1), ("fk", -8, -3)), hands=("fist", "fist"),
                  look=(0.05, 0.1)),
    "j_raise": _P(t=-3, h=-6, legs=((8, 3), (-7, -3)), arms=(("fk", 152, 168), ("fk", 30, 74)),
                  hands=("fist", "open")),
    "j_chest": _P(t=4, h=8, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "fist")),
    "j_heaven": _P(t=-5, h=-22, arms=(("fk", 166, 172), ("fk", -6, -2)), hands=("open", "fist"),
                   look=(0.02, -0.14)),
    # drawn facing RIGHT (a paper turn toward the rail): an open palm swept up and out at the towering sea
    "j_sea": _P(t=-3, h=-10, legs=((8, 3), (-7, -3)), arms=(("fk", 136, 146), ("fk", -6, -2)),
                hands=("open", "fist"), look=(0.05, -0.08)),
    "j_land": _P(t=-2, h=-8, arms=(("fk", 118, 122), ("fk", -6, -2)), hands=("point", "fist"),
                 look=(0.0, -0.05)),
    "j_all": _P(t=-2, h=-6, arms=(("fk", 118, 138), ("fk", -78, -70)), hands=("open", "fist")),
    "j_stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "j_down": _P(h=14, arms=(("fk", 14, 8), ("fk", -8, -3))),
    "confess": C.POSES["confess"],
}


def figure(who, x, y, s, facing, pose, expr=None, variant=0, marks=True):
    """(markup, points) of a person in a POSE entry (or a pose record). points: hands [far, near], shoulders,
    head, all in stage px."""
    ps = dict(POSE[pose]) if isinstance(pose, str) else dict(pose)
    if who == "jonah":
        D, m = C._jonah_design(), C._ADULT
    elif who == "captain":
        D, m = C._captain_design(), C._CAPTAIN_M
    else:
        D, m = C._sailor_design(variant), C._SAILOR_M
    inner, _ = C._figure(D, m, ps, expr or ps["expr"], C._fsign(facing), marks)
    L = dict(C._LAST)
    sx = s * (1 if facing >= 0 else -1)

    def st(p):
        return (x + p[0] * sx, y + p[1] * s)
    pts = {"hands": [st(p) for p in L["hands"]], "shoulders": [st(p) for p in L["shoulders"]],
           "head": st(L["head"])}
    label = f"{who}{variant}-{pose if isinstance(pose, str) else 'custom'}"
    return C._wrap_out(inner, x, y, s, facing, label), pts


def lot_svg(x, y, s, rot, marked=False):
    """A lot stick; the marked one keeps its gold mark but loses the built-in halo (the glow is its own layer)."""
    m = PR.lot(x, y, s, rot=rot, marked=marked)
    if marked:
        m = re.sub(r'<ellipse cx="0" cy="0" rx="78" ry="56"[^>]*/>', "", m)
    return m


def stick_in(pts, hand=0, s=1.0, marked=False, out=26):
    """A lot held in a fist, sticking out of it along the shoulder -> hand direction. Returns (markup, centre)."""
    hx, hy = pts["hands"][hand]
    sx_, sy_ = pts["shoulders"][hand]
    d = math.atan2(hy - sy_, hx - sx_)
    cx, cy = hx + out * s * math.cos(d), hy + out * s * math.sin(d)
    return lot_svg(cx, cy, s, math.degrees(d), marked), (cx, cy)


# ============================================================== animation helpers

# Planted-foot walk (the technique of v1 s05 / v2 s05_captain): WALK_N drawings per step, two steps per cycle.
# Drawing k (phase k / WALK_N, 0..2): the planted leg (far leg in the first step, near leg in the second) sweeps its
# ankle from +A to -A figure px (forward = +) while the other leg swings from -A to +A with a bent knee; drawing 0 is
# the contact with the far foot forward. The anchor advances 2 A / WALK_N * scale stage px per drawing, so the
# planted sole stays on the same plank for the whole step (measured: within 1 px per drawing). Legs are forward
# kinematics with the stance leg nearly straight, so long robes hang as in walk_a / walk_b (IK legs with a lowered
# pelvis made the robes bunch up like a crouch).
WALK_N = 3
WALK_A = {"sailor": 46, "jonah": 44, "captain": 50}
WALK_LEG = {"sailor": 116.0, "jonah": 116.0, "captain": 125.5}   # ~ thigh + shin, a touch short of straight


def walk_pose(k, who, n=WALK_N):
    A, leg = WALK_A[who], WALK_LEG[who]
    ph = (k % (2 * n)) / n
    step, u = divmod(ph, 1.0)
    ap = math.degrees(math.asin(A * (1 - 2 * u) / leg))
    plant = (ap + 3, ap - 3)
    xs = -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u))
    as_ = math.degrees(math.asin(xs / leg)) + 10 * math.sin(math.pi * u)
    swing = (as_, as_ - 42 * math.sin(math.pi * u) - 6)
    sw = 30 * math.cos(math.pi * ph)            # arms swing against the legs
    return C._P(t=5, h=-4, legs=(plant, swing) if step == 0 else (swing, plant),
                arms=(("fk", -sw, -sw + 14), ("fk", sw, sw + 14)))


def apply_tf(tf, p, pivot):
    """Where stage point p goes under a layer transform tf (pivot = the layer's default pivot)."""
    px = tf.px if tf.px is not None else pivot[0]
    py = tf.py if tf.py is not None else pivot[1]
    x, y = (p[0] - px) * tf.sx, (p[1] - py) * tf.sy
    a = math.radians(tf.rot)
    return (px + tf.dx + x * math.cos(a) - y * math.sin(a), py + tf.dy + x * math.sin(a) + y * math.cos(a))


def keyed(keys_, curve="sine"):
    keys_ = sorted(keys_)

    def f(t):
        if t <= keys_[0][0]:
            return keys_[0][1]
        for (t0, a), (t1, b) in zip(keys_, keys_[1:]):
            if t <= t1:
                return M.lerp(a, b, M.progress(t, t0, t1, curve))
        return keys_[-1][1]
    return f


class Track:
    """One person on their own flipbook layer.

    moves: (t0, t1, (x, y, s) from, (x, y, s) to, kind 'hop' | 'walk'); keys: (t, pose, facing, expr, props, pop).
    Every key is drawn at the person's home at its time (the destination of a move in progress), the layer motion
    carries it from the move's start; pose switches are hard cuts sold by a squash-and-hop ('pop')."""

    def __init__(self, name, who, start, z, variant=0, phase=0.0, amp=0.011):
        self.name, self.who, self.start, self.z = name, who, start, z
        self.variant, self.phase, self.amp = variant, phase, amp
        self.moves, self.keys = [], []
        self.turns = []
        self.jiggle = None

    def move(self, t0, t1, to, kind="hop"):
        frm = self.rest(t0)
        to = (to[0], to[1], to[2] if len(to) > 2 else frm[2])
        self.moves.append((t0, t1, frm, to, kind))
        self.moves.sort(key=lambda m: m[0])
        return self

    def rest(self, t):
        p = self.start
        for (t0, t1, a, b, k) in self.moves:
            if t0 <= t:
                p = b
        return p

    def pos(self, t):
        for (t0, t1, a, b, k) in self.moves:
            if t0 <= t < t1:
                if isinstance(k, tuple):          # planted steps: the anchor jumps one stride share per drawing
                    u = math.floor((t - t0) / (t1 - t0) * k[1] + 1e-6) / k[1]
                elif k == "walk":
                    u = (t - t0) / (t1 - t0)
                else:
                    u = M.progress(t, t0, t1, "sine")
                return tuple(M.lerp(a[i], b[i], u) for i in range(3))
        return self.rest(t)

    def key(self, t, pose, facing, expr=None, props=None, pop=True, marks=True):
        x, y, s = self.rest(t + 1e-6)
        mk, pts = figure(self.who, x, y, s, facing, pose, expr, self.variant, marks)
        sh = C.ground_shadow(x, y + 2, s, width=120 if self.who != "captain" else 136)
        extra = ""
        if props:
            for fn in props:
                extra += fn(pts, s, facing)
        self.keys.append((t, sh + mk + extra, (x, y, s), pop, pts, facing))
        self.keys.sort(key=lambda k: k[0])
        return pts

    def walk(self, t0, to, facing, expr=None, props=None, dt=0.1, pose_after="stand"):
        """Planted-foot walk to ``to`` starting at t0 (walk_pose drawings, ``dt`` s each; the number of drawings
        follows the distance, so the planted sole never slides). Ends on ``pose_after`` (a squash-hop). Returns
        the arrival time."""
        frm = self.rest(t0)
        s = 0.5 * (frm[2] + (to[2] if len(to) > 2 else frm[2]))
        A = WALK_A[self.who]
        m = max(2, round(abs(to[0] - frm[0]) / (2 * A * s / WALK_N)))
        t1 = t0 + m * dt
        self.move(t0, t1, to, ("steps", m))
        for k in range(m):
            self.key(t0 + k * dt, walk_pose(k, self.who), facing, expr, props, pop=False)
        if pose_after:
            self.key(t1, pose_after, facing, expr, props, pop=True)
        return t1

    def idx(self, t):
        i = 0
        for j, k in enumerate(self.keys):
            if t >= k[0]:
                i = j
        return i

    def pts_at(self, t):
        return self.keys[self.idx(t)][4]

    def motion(self):
        switches = [k[0] for k in self.keys if k[3]]

        def m(t):
            i = self.idx(t)
            hx, hy, hs = self.keys[i][2]
            x, y, s = self.pos(t)
            k = s / hs
            dy = y - hy
            for (t0, t1, a, b, kind) in self.moves:
                if t0 <= t < t1:
                    if kind == "hop":
                        dist = math.hypot(b[0] - a[0], b[1] - a[1])
                        dy -= min(26.0, 6 + 0.12 * dist) * math.sin(math.pi * (t - t0) / (t1 - t0))
                    elif kind == "walk":
                        dy -= 5 * abs(math.sin(math.pi * (t - t0) / 0.15))
            sy = 1 + self.amp * math.sin(2 * math.pi * (t / 3.1 + self.phase))
            sx = 1.0
            for ts in switches:
                u = (t - ts) / 0.24
                if 0 <= u <= 1:
                    bmp = math.sin(math.pi * u) * (1 - u)
                    sy *= 1 - 0.08 * bmp
                    sx *= 1 + 0.045 * bmp
                    dy -= 7 * math.sin(math.pi * min(1.0, u * 1.6)) * (u < 0.62)
            rot = 0.0
            if self.jiggle:
                jd = self.jiggle(t)
                dy += jd[0]
                rot += jd[1]
            for ts in self.turns:      # paper cut-out turn around a facing flip
                v = abs(t - ts) / 0.09
                if v < 1:
                    sx *= 1 - 0.7 * (1 - v)
            return Tf(x - hx, dy, rot, sx * k, sy * k, 1.0, hx, hy)
        return m

    def add_to(self, sc, seed=None):
        """One layer per stretch of keys drawn near the same spot (each with a small box; the compositor warps a
        layer's whole box every frame), shown only while its keys are current."""
        segs, cur = [], []
        for k in self.keys:
            if cur and abs(k[2][0] - cur[0][2][0]) + abs(k[2][1] - cur[0][2][1]) > 70:
                segs.append(cur)
                cur = []
            cur.append(k)
        segs.append(cur)
        mot = self.motion()
        for si, seg in enumerate(segs):
            uniq, idx_of = [], []
            for k in seg:
                if k[1] not in uniq:
                    uniq.append(k[1])
                idx_of.append(uniq.index(k[1]))
            times = [k[0] for k in seg]
            t_on = times[0] if si > 0 else -1e9
            t_off = segs[si + 1][0][0] if si + 1 < len(segs) else 1e9

            def at(t, times=times, idx_of=idx_of):
                i = 0
                for j, tk in enumerate(times):
                    if t >= tk:
                        i = j
                return float(idx_of[i])

            def m(t, t_on=t_on, t_off=t_off):
                return mot(t) if t_on <= t < t_off else Tf(alpha=0.0)
            svgs = [doc(b) for b in uniq]
            sc.add(f"{self.name}_{si}", svgs if len(svgs) > 1 else svgs[0], z=self.z + 0.001 * si, motion=m,
                   frame_at=at if len(svgs) > 1 else None, seed=seed)


def held(hand=1, marked=False, s_mul=1.0, out=26):
    """Prop function: a lot in the far (0) or near (1) fist."""
    def f(pts, s, facing):
        return stick_in(pts, hand, s * s_mul, marked, out)[0]
    return f


def held_up(hand=0, lean=0.3, out=30):
    """Prop function: a plain lot held upright in a fist (leaning a little forward), to look at it."""
    def f(pts, s, facing):
        hx, hy = pts["hands"][hand]
        d = math.atan2(-1.0, lean * facing)
        return lot_svg(hx + out * s * math.cos(d), hy + out * s * math.sin(d), s, math.degrees(d))
    return f


def jar_on_palm(pts, s, facing, rot=0.0):
    """The lots jar (6 sticks) standing on S3's raised open far hand, as he shows it round; ``rot`` rocks it about
    its foot on the palm (the rattle), with little shake marks."""
    hx, hy = pts["hands"][0]
    bx, by = hx + 2 * facing, hy - 7
    out = PR.lots_jar(bx, by, 1.0, sticks=6)
    if rot:
        out = f'<g transform="rotate({rot:.1f} {bx:.1f} {by:.1f})">{out}</g>'
        for sgn in (-1, 1):
            x0 = bx + sgn * 66
            out += (f'<path d="M{x0:.0f},{by - 120:.0f} q{sgn * 12:.0f},14 0,28 M{x0 + sgn * 16:.0f},{by - 112:.0f} '
                    f'q{sgn * 10:.0f},10 0,20" fill="none" stroke="{P["ink_soft"]}" stroke-width="4" '
                    f'stroke-linecap="round"/>')
    return out


def jar_rattle(rot):
    return lambda pts, s, facing: jar_on_palm(pts, s, facing, rot)


# ============================================================== world extras

def deck_floor_layer():
    """v1 s05's deck_layer without the rig (far bulwark with shields, deck planks, puddles, the open hatch and the
    cut edge): the mast and sail are their own layer, so neither item's box covers the whole frame."""
    defs = (S.lin_grad("deckf", [(0, "#b98450"), (0.5, P["wood_light"]), (1, "#a96f42")]) +
            S.lin_grad("bulw", [(0, P["wood"]), (1, "#7e4e2e")]))
    RT, DB, DC, HT = V.RAIL_TOP, V.DECK_BACK, V.DECK_CUT, V.HOLD_TOP
    b = ""
    b += f'<rect x="-30" y="{RT + 14}" width="{W + 60}" height="{DB - RT - 4}" fill="url(#bulw)" {S.STROKE}/>'
    b += V.plank_lines(-30, W + 30, [842, 868], seed=3, opacity=0.4, joint_every=(500, 900))
    for x in range(40, W + 80, 300):
        b += f'<rect x="{x - 12}" y="{RT + 4}" width="24" height="{DB - RT}" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    for xr in (V.MAST_X + 29 - 330, V.MAST_X + 29 + 330):
        b += f'<circle cx="{xr}" cy="{RT + 8}" r="9" fill="{P["wood_dark"]}" {S.STROKE_THIN}/>'
    cols = [P["jonah_sash"], P["terracotta"], "#efe2c4", P["gold"]]
    for i, x in enumerate(range(110, W + 60, 150)):
        b += V.shield(x, 852, 33, cols[i % 4])
    b += (f'<path d="M-30,{RT} L{W + 30},{RT} L{W + 30},{RT + 18} L-30,{RT + 18} Z" '
          f'fill="{P["wood_light"]}" {S.STROKE}/>')
    b += f'<rect x="-30" y="{DB}" width="{W + 60}" height="{DC - DB + 4}" fill="url(#deckf)" {S.STROKE}/>'
    ys = [906, 924, 946, 972, 1003, 1039, 1080, 1126, 1176]
    b += V.plank_lines(-30, W + 30, ys, seed=7, opacity=0.45, joint_every=(260, 620))
    for (x, y, rx, ry) in [(660, 1062, 130, 16), (1180, 1112, 160, 18), (1600, 1150, 120, 14), (420, 1150, 90, 12)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#9fb3bd" opacity="0.45"/>'
        b += f'<path d="M{x - rx * 0.5},{y - 3} l{rx * 0.5},0" stroke="#e8eef0" stroke-width="3" opacity="0.6"/>'
    hm, hdefs = V.hatch_markup()
    b += hm
    cut = f'<rect x="-30" y="{DC - 4}" width="{W + 60}" height="{HT - DC + 8}" fill="{P["wood_dark"]}" {S.STROKE}/>'
    cut += f'<rect x="-30" y="{DC + 8}" width="{W + 60}" height="26" fill="{P["jonah_sash"]}" {S.STROKE_THIN}/>'
    return doc(S.g(b, filter="wobble") + S.g(cut, filter="wobble"), defs + hdefs)


def rig_layer():
    """v1's mast, shrouds and torn striped sail (V.rig_markup), on its own."""
    rig, rdefs = V.rig_markup()
    return doc(rig, rdefs)


def clipped(svg, y0, y1, cid):
    """Crop a layer document to the band y0..y1 (the compositor warps a layer's whole box every frame, so parts
    that are always hidden behind nearer layers should not be in it)."""
    i = svg.index("</defs>")
    clip = f'<clipPath id="{cid}"><rect x="-200" y="{y0}" width="{W + 400}" height="{y1 - y0}"/></clipPath>'
    j = svg.rindex("</svg>")
    return svg[:i] + clip + "</defs>" + f'<g clip-path="url(#{cid})">' + svg[i + 7:j] + "</g></svg>"


def sky_clouds_layer():
    """v1's storm sky with its low cloud bank merged in (one item; they drift together)."""
    sky = rehost(V.sky_layer())
    clouds = rehost(V.clouds_layer())
    body = clouds[clouds.index("</defs>") + 7:clouds.rindex("</svg>")]
    # sea_far covers the sky below ~y 620 even at the strongest tilt
    return clipped(sky[:sky.rindex("</svg>")] + body + "</svg>", -40, 668, "skyclip")

def coast_layer():
    """A faint far coast on the horizon between the sail and the big wave (Jonah points to it: '陆地')."""
    d = S.hill(960, 1500, 606, 96, seed=4, bottom=650, bumps=3)
    d2 = S.hill(1120, 1430, 606, 62, seed=9, bottom=650, bumps=2)
    body = S.path(d, fill="#93a09a", sw=3, extra='opacity="0.95"')
    body += S.path(d2, fill="#7f9288", sw=2.5)
    for x, y in ((1060, 560), (1300, 548), (1380, 572)):          # a few tiny trees on the far shore
        body += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="13" fill="#6f8478" stroke="{INK}" stroke-width="2"/>'
    return doc(S.g(body, filter="wobble"))


def land_layer():
    """Land colours and features over the faint coast (registered with coast_layer): warm green hills, a sandy
    shore, round trees and a palm with trunks, a tiny white town — so '陆地' reads as land, not as another swell.
    Its own layer so it can fade back to the plain coast that s07 opens on."""
    d = S.hill(960, 1500, 606, 96, seed=4, bottom=650, bumps=3)
    d2 = S.hill(1120, 1430, 606, 62, seed=9, bottom=650, bumps=2)
    body = S.path(d, fill="#a3b47c", sw=3)
    body += S.path(d2, fill="#8fa66c", sw=2.5)
    # soft fields on the slopes
    for (x, y, rx, ry, c) in ((1030, 590, 50, 9, "#b9c487"), (1350, 596, 46, 8, "#c3c98f"), (1160, 584, 38, 7, "#9bb070")):
        body += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="0.8"/>'
    # sandy shore along the water line
    body += (f'<path d="M944,612 Q1000,598 1080,600 Q1200,594 1320,599 Q1440,596 1516,610 L1516,622 L944,622 Z" '
             f'fill="#e6d29e" stroke="{INK}" stroke-width="2"/>')
    trees = ""
    for x, y, r in ((1060, 560, 11), (1300, 548, 10), (1380, 572, 10), (1012, 586, 8)):
        trees += (f'<path d="M{x},{y + r + 13} L{x},{y + 2}" stroke="#7a5638" stroke-width="3.2" '
                  f'stroke-linecap="round"/>')
        trees += f'<circle cx="{x}" cy="{y}" r="{r + 1}" fill="#5f8048" stroke="{INK}" stroke-width="2"/>'
        trees += f'<circle cx="{x - r * 0.35:.1f}" cy="{y - r * 0.35:.1f}" r="{r * 0.35:.1f}" fill="#7d9b5c"/>'
    # a palm on the shore
    px_, py_ = 1452, 604
    trees += (f'<path d="M{px_},{py_} Q{px_ + 6},{py_ - 18} {px_ + 2},{py_ - 36}" fill="none" stroke="#7a5638" '
              f'stroke-width="3.4" stroke-linecap="round"/>')
    for ang in (-160, -125, -90, -55, -20):
        a = math.radians(ang)
        ex, ey = px_ + 2 + 17 * math.cos(a), py_ - 36 + 17 * math.sin(a) + 6
        trees += (f'<path d="M{px_ + 2},{py_ - 36} Q{(px_ + 2 + ex) / 2:.1f},{py_ - 44 + 2 * math.sin(a):.1f} '
                  f'{ex:.1f},{ey:.1f}" fill="none" stroke="#4f7040" stroke-width="4" stroke-linecap="round"/>')
    # a tiny white town on the front hill (flat roofs, dark doorways)
    town = ""
    for x, y, w, h in ((1222, 572, 15, 11), (1238, 566, 13, 15), (1253, 574, 16, 10), (1270, 569, 12, 13),
                       (1284, 576, 14, 9)):
        town += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f2e7cd" stroke="{INK}" stroke-width="1.6"/>'
        town += f'<rect x="{x + w * 0.4:.1f}" y="{y + h * 0.45:.1f}" width="3" height="{h * 0.5:.1f}" fill="#8a6a50"/>'
    return doc(S.g(body, filter="wobble") + S.g(trees + town, filter="wobble-fine"))


def bubble_layer(cx, cy, tail):
    """Thought bubble: a cloud with a soft green-gold landscape inside and warm light on its right."""
    rx, ry = 214, 128
    defs = (S.rad_grad("bglow", [(0, "#ffe9a8", 0.95), (0.4, "#ffd27a", 0.55), (1, "#ffd27a", 0)]) +
            f'<clipPath id="bclip"><ellipse cx="{cx}" cy="{cy}" rx="{rx - 16}" ry="{ry - 14}"/></clipPath>')
    puffs = []
    n = 13
    for i in range(n):
        a = 2 * math.pi * i / n
        puffs.append((cx + rx * math.cos(a), cy + ry * math.sin(a), 46 if i % 2 else 38))
    out = ""
    for x, y, r in puffs:
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 4}" fill="{INK}"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 4}" ry="{ry + 4}" fill="{INK}"/>'
    for x, y, r in puffs:
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fbf3e2"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fbf3e2"/>'
    inner = f'<rect x="{cx - rx}" y="{cy - ry}" width="{2 * rx}" height="{2 * ry}" fill="#f6ead0"/>'
    inner += f'<ellipse cx="{cx + 175}" cy="{cy - 40}" rx="170" ry="150" fill="url(#bglow)"/>'
    inner += S.path(S.rays(cx + 190, cy - 50, 30, 190, n=10, width_deg=9, rot=4), fill="#ffd77e", stroke=False,
                    extra='opacity="0.55"')
    inner += S.path(S.hill(cx - rx - 20, cx + rx + 20, cy + 70, 24, seed=3, bottom=cy + ry + 20, bumps=3),
                    fill="#cfd9a0", sw=3)
    inner += f'<path d="M{cx - 200},{cy + 88} Q{cx},{cy + 70} {cx + 200},{cy + 86}" stroke="#b8a46a" ' \
             f'stroke-width="5" fill="none" stroke-dasharray="14 12" opacity="0.6"/>'
    out += f'<g clip-path="url(#bclip)">{inner}</g>'
    # trailing thought dots down to Jonah's head
    (tx, ty) = tail
    for k, r in ((0.25, 26), (0.55, 18), (0.82, 12)):
        x = M.lerp(cx + 120, tx, k)
        y = M.lerp(cy + ry, ty, k)
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fbf3e2" {S.STROKE}/>'
    return doc(S.g(out, filter="wobble-fine"), defs)


# ============================================================== build

def build(ctx):
    T = ctx.duration
    L = ctx.lines
    PH = Phrases(ctx)
    sc = Scene(ctx, W=W, H=H)

    def ph(key, default, line=None):
        return PH.start(key, default, line)

    # ---------------------------------------------------------------- key times (all from the narration)
    def after(t, prev, gap=0.55):
        """t, but no earlier than ``gap`` after prev: every pose is held long enough to read whatever the voice
        take (a short pause or a re-timed take can bring two phrase times very close)."""
        return max(t, prev + gap)

    t_l0, t_l0e = L[0].start, L[0].end
    t_up = t_l0e + 0.12                                   # the huddle breaks up
    t_lai = after(ph("来，", L[1].start), t_up, 0.6)        # '来，' S3 takes the jar
    t_draw_ph = after(ph("看看", L[1].start + 1.3), t_lai, 1.0)    # '看看…' the sailors draw
    t_who = after(PH.inner("看看是哪个人", "是哪个人", t_draw_ph + 0.8), t_draw_ph, 0.25)
    t_rela = after(PH.inner("看看是哪个人", "惹来了", t_who + 0.9), t_who, 0.6)
    t_storm = after(PH.inner("这场大风暴", "大风暴", L[1].end - 0.6), t_rela, 0.5)   # lightning
    t_they = ph("他们就抽签", L[2].start)
    t_result = after(ph("结果", t_they + 1.4), t_they, 0.9)
    t_glow = after(ph("抽中的正是约拿", t_result + 0.8), t_result, 0.6)
    t_ask = after(ph("水手们赶紧问他", L[2].chunks[-1].start if L[2].chunks else t_glow + 2), t_glow, 1.6)
    t_q0 = ph("请你告诉我们", L[3].start)
    t_q1 = after(ph("你是做什么的", t_q0 + 1.1), t_q0)
    t_q2 = after(ph("你从哪里来", t_q1 + 1.0), t_q1)
    t_q3 = after(ph("你是哪国人", t_q2 + 1.2), t_q2)
    t_hebrew = ph("我是希伯来人", L[4].start)
    t_worship = after(ph("我敬拜耶和华", t_hebrew + 1.4), t_hebrew, 0.6)
    t_heaven = after(ph("天上的上帝", t_worship + 1.7), t_worship, 0.6)
    t_sea = after(ph("大海和陆地", t_heaven + 1.1), t_heaven, 0.6)
    t_land = after(PH.inner("大海和陆地", "和陆地", t_sea + 0.6), t_sea, 0.6)
    t_made = after(ph("都是他造的", t_land + 0.7), t_land, 0.6)
    t_name = ph("耶和华，", L[5].start, line=5)
    t_name2 = after(ph("就是上帝的名字", t_name + 1.1), t_name, 0.5)
    t_told = after(ph("约拿还告诉他们", t_name2 + 1.6), t_name2, 0.8)
    t_flee = after(ph("他正在逃跑", t_told + 1.8), t_told, 0.8)
    t_hide = after(ph("想要躲开耶和华", t_flee + 1.3), t_flee, 0.6)
    t_heard = after(ph("水手们听了", t_hide + 2.2), t_hide, 0.6)
    t_afraid = after(ph("更加害怕了", t_heard + 1.5), t_heard, 0.6)
    t_how = after(L[6].start, t_afraid, 0.9)

    # ---------------------------------------------------------------- outboard world (rocks against the ship)
    # sky + cloud bank drift slowly (dx >= 0 keeps the sky's right edge outside the view)
    sc.add("sky", sky_clouds_layer(), z=0, wc=0.7,
           motion=lambda t: Tf(dx=22 + 22 * math.sin(2 * math.pi * t / 40 - 1.2)))
    sc.add("coast", coast_layer(), z=0.4, motion=V.tilted(), wc=0.8)
    # its land colours and features; they fade into the rain as the storm grows at '更加害怕了', so the scene ends on
    # the plain hazy coast that s07 opens on (and lets vanish)
    land_a = keyed([(0, 1.0), (t_heard, 1.0), (t_afraid + 1.2, 0.0)])
    sc.add("land", land_layer(), z=0.42, wc=0.8, motion=V.tilted(lambda t: Tf(alpha=land_a(t))))
    # a warm glint touches the far land as Jonah names it ('和陆地') and stays through '都是他造的'
    cg = S.rad_grad("cglint", [(0, "#ffe2a0", 0.75), (0.5, "#ffd27a", 0.3), (1, "#ffd27a", 0)])
    land_env = keyed([(t_land - 0.05, 0.0), (t_land + 0.4, 1.0), (L[4].end + 0.3, 0.9), (t_name + 0.5, 0.0)])
    sc.add("coast_glint", doc('<ellipse cx="1240" cy="560" rx="300" ry="70" fill="url(#cglint)"/>', cg), z=0.45,
           wc=0, blend="add", motion=V.tilted(lambda t: Tf(alpha=land_env(t))))
    sc.add("sea_far", rehost(V.sea_far_layer()), z=0.5, motion=V.tilted(), wc=0.9)

    # golden light from the cloud break (God is never drawn, only light): when the lot falls on Jonah, at
    # '天上的上帝' and at '耶和华，就是上帝的名字'
    beam_env = keyed([(0, 0.0), (t_glow - 0.06, 0.0), (t_glow + 0.55, 1.0), (t_ask, 0.8), (t_q0 + 0.6, 0.5),
                      (t_heaven - 0.1, 0.5), (t_heaven + 0.6, 0.85), (t_sea + 0.4, 0.6), (t_name - 0.1, 0.6),
                      (t_name + 0.8, 1.0), (t_name2 + 1.2, 0.95), (t_told + 0.8, 0.45), (t_heard, 0.35),
                      (t_afraid + 0.4, 0.22), (T, 0.22)])
    bdefs = (S.rad_grad("brk", [(0, "#ffd77e", 0.85), (0.45, "#ffbf55", 0.42), (1, "#ffbf55", 0)]))
    rays = "".join(S.rays(1650, 290, 60, 470, n=26, width_deg=5, rot=8).split(" Z ")[i] + " Z "
                   for i in range(26) if 1 <= i <= 12)          # only the rays that fall toward the deck
    brk = (S.g('<ellipse cx="1650" cy="300" rx="400" ry="180" fill="url(#brk)"/>', filter="soft") +
           S.g(S.path(rays, fill="#ffd27a", stroke=False, extra='opacity="0.4"'), filter="blur-md") +
           S.g('<ellipse cx="1650" cy="318" rx="250" ry="70" fill="#ffe2a0" opacity="0.5"/>', filter="blur-md"))
    sc.add("break_glow", doc(brk, bdefs), z=1.5, wc=0,
           motion=lambda t: Tf(alpha=beam_env(t) * (0.92 + 0.08 * math.sin(2 * math.pi * t / 2.3))))

    sc.add("big_wave", clipped(rehost(V.big_wave_layer()), -40, 836, "bwclip"), z=3, motion=V.tilted(M.combine(
        M.bob(26, 3.4, 0.1), lambda t: Tf(dx=18 * math.sin(2 * math.pi * t / 6.8)))))
    sc.add("sea_mid", clipped(rehost(V.sea_mid_layer()), -40, 836, "smclip"), z=4,
           motion=V.tilted(M.combine(M.bob(20, 3.4, 0.35), M.bob(46, 6.0, axis="x"))))

    # ambient splashes over the rail, away from faces and key moments
    splashes = [(2.0, 2010, 0.7, 3), (t_who + 0.4, 1990, 0.62, 7), (t_q2 + 0.2, 2020, 0.7, 5),
                (t_sea + 0.1, 1975, 0.95, 17),        # the sea answers Jonah's sweep toward it ('大海')
                (t_told + 0.6, 1980, 0.66, 11), (t_afraid + 0.25, 2000, 0.85, 13)]

    def splash_m(base, t0, dur=0.95):
        def m(t):
            u = (t - t0) / dur
            if not (0 <= u < 1):
                return Tf(alpha=0.0)
            s = 0.25 + 0.85 * M.ease("out")(min(1.0, u / 0.6))
            a = min(1.0, u / 0.12) * (1 - M.progress(u, 0.5, 1.0, "sine"))
            return Tf(dy=50 * u * u, sx=s, sy=s, alpha=a, px=base[0], py=base[1])
        return V.tilted(m)
    for i, (ts, sx_, k, seed) in enumerate(splashes):
        base = (sx_, V.RAIL_TOP + 14)
        sc.add(f"splash{i}", rehost(V.splash_layer(base[0], base[1], seed, k)), z=5 + 0.1 * i,
               motion=splash_m(base, ts), wc=0.3)
        sc.sfx("splash_small", ts, gain_db=-17, pan=0.75)

    # ---------------------------------------------------------------- ship
    sc.add("deck", deck_floor_layer(), z=10)
    sc.add("rig", rig_layer(), z=10.45)
    hg_defs = S.rad_grad("hg", [(0, "#ffcf86", 0.75), (0.5, "#f6a956", 0.28), (1, "#f2a95a", 0)])
    sc.add("hatch_glow", doc(f'<ellipse cx="{V.HX}" cy="{V.HATCH_F[2] - 30}" rx="190" ry="120" fill="url(#hg)"/>',
                             hg_defs), z=10.4, blend="add", wc=0, motion=M.pulse(0.7, 1.0, 1.7))
    sc.add("deck_props", rehost(V.deck_props_layer()), z=11)
    mlx, mly = V.MAST_X + 29 + 47, 610
    sc.add("deck_lantern", doc(PR.lantern(mlx, mly, 0.8)), z=11.5, motion=M.sway(9, 2.9, pivot=(mlx, mly)))

    # warm light on Jonah's spot: a gold wash in the beam + highlights (normal blend keeps it gold over the blue)
    jxe = J_END
    wdefs = (S.lin_grad("beamw", [(0, "#ffbf55", 0.5), (0.35, "#ffcb6a", 0.32), (0.8, "#ffd98a", 0.12),
                                   (1, "#ffd98a", 0.0)]) +
             S.lin_grad("beamh", [(0, "#fff0c0", 0.0), (0.25, "#ffe7a8", 0.3), (0.85, "#ffe29a", 0.1),
                                  (1, "#ffe39a", 0.0)]) +
             S.rad_grad("jg", [(0, "#ffe2a0", 0.55), (0.45, "#ffd27a", 0.25), (1, "#ffd27a", 0)]) +
             S.rad_grad("pool", [(0, "#ffc85e", 0.5), (1, "#ffc85e", 0)]) +
             S.rad_grad("lotg", [(0, "#fff2c4", 0.95), (0.35, "#ffd27a", 0.6), (1, "#ffbf55", 0)]))
    sc.add("beam_wash", doc(S.g(f'<path d="M1500,250 L1800,250 L{jxe + 230},1010 L{jxe - 240},1010 Z" '
                                f'fill="url(#beamw)"/>', filter="blur-md") +
                            S.g(f'<path d="M1580,260 L1720,260 L{jxe + 110},990 L{jxe - 120},990 Z" '
                                f'fill="url(#beamh)"/>', filter="blur-md") +
                            f'<ellipse cx="{jxe}" cy="{JY + 4}" rx="230" ry="46" fill="url(#pool)"/>', wdefs),
           z=19, wc=0, motion=lambda t: Tf(alpha=beam_env(t)))

    # ---------------------------------------------------------------- the crate and the lots jar
    sc.add("crate", doc(C.ground_shadow(X_C + 8, Y_CRATE - 2, 1.0, width=170, opacity=0.2) +
                        PR.crate(CRATE_A[0], CRATE_A[1], CRATE_S)), z=21)

    # ---------------------------------------------------------------- people
    S3 = Track("s3", "sailor", (0, FRONT_Y, 1.0), z=24, variant=3, phase=0.4)
    # left slot: S3's 'reach' hand at the jar mouth
    _, p = figure("sailor", 0, FRONT_Y, 1.0, 1, "reach", variant=3)
    S3.start = (MOUTH[0] - 14 - p["hands"][0][0], FRONT_Y, 1.0)
    S0 = Track("s0", "sailor", (0, 952, 0.9), z=20.5, variant=1, phase=0.8)
    _, p = figure("sailor", 0, 952, 0.9, 1, "reach_down", variant=1)
    S0.start = (MOUTH[0] + 4 - p["hands"][0][0], 952, 0.9)
    S1 = Track("s1", "sailor", (0, 1008, 0.96), z=23, variant=0, phase=0.2)
    _, p = figure("sailor", 0, 1008, 0.96, -1, "reach", variant=0)
    S1.start = (MOUTH[0] + 14 - p["hands"][0][0], 1008, 0.96)
    S2 = Track("s2", "sailor", (1042, 930, 0.86), z=20, variant=2, phase=0.55)
    CP = Track("captain", "captain", (972, 1018, CAPT_S), z=22, phase=0.65)
    JN = Track("jonah", "jonah", (J_START, JY, 1.0), z=25, phase=0.1, amp=0.009)
    _, p = figure("jonah", 0, JY, 1.0, -1, "j_reach")
    J_SLOT = MOUTH[0] + 16 - p["hands"][0][0]

    # ---- line 0: the huddle (heads together, talking with raised palms, hands at chins, nodding); Jonah apart by
    # the hatch. Keys follow line 0's length; nothing changes in the opening dissolve, and nobody's hand goes near the
    # jar until S3 suggests drawing lots.
    def hud(f):
        return min(max(1.05, t_l0 + f * (t_l0e - t_l0)), t_up - 0.5)
    CP.key(0, "lean", 1)
    CP.key(hud(0.3), "talk", 1)
    CP.key(hud(0.72), "lean", 1)
    S2.key(0, "lean", 1)
    S2.key(hud(0.5), "nod_lean", 1, pop=False)
    S2.key(hud(0.68), "lean", 1, pop=False)
    S3.key(0, "h_talk", 1)
    S3.key(hud(0.45), "chin", 1)
    S0.key(0, "chin", 1)
    S0.key(hud(0.22), "chin_nod", 1, pop=False)
    S0.key(hud(0.4), "chin", 1, pop=False)
    S1.key(0, "chin", -1)
    S1.key(hud(0.35), "h_talk", -1)
    S1.key(hud(0.58), "h_talk_nod", -1, pop=False)
    S1.key(hud(0.76), "h_talk", -1, pop=False)
    JN.key(0, "j_stand", -1, "worried")
    JN.key(hud(0.6), "j_down", -1, "sorry", pop=False)

    # end of the huddle: they straighten up; S3 has an idea and reaches for the jar (below)
    CP.key(t_up + 0.1, "stand", 1, "worried")
    S2.key(t_up + 0.22, "stand", 1, "worried")
    S0.key(t_up + 0.16, "stand", 1, "worried")
    S1.key(t_up + 0.04, "stand", -1, "worried")
    JN.key(t_up + 0.3, "j_stand", -1, "worried")

    # ---- line 1: S3 takes the jar, shows it round on his palm and shakes it, sets it back and draws first
    t_grab = max(t_up - 0.06, t_lai - 0.6)    # hand on the jar (anticipation, in the pause)
    t_show = t_lai + 0.02                     # '来，' up on his raised palm, shaking it ('我们来抽签')
    t_setdown = after(t_draw_ph - 0.15, t_show, 0.9)   # back on the crate
    t_shake0, t_shake1 = t_show + 0.25, t_setdown - 0.13
    S3.key(t_grab, "reach", 1, "surprised")
    S3.key(t_show - 0.11, "lift_in", 1, "worried", props=[jar_on_palm], pop=False)   # in-between (no pop)
    S3.key(t_show, "show_jar", 1, "call", props=[jar_on_palm])
    k, tk = 0, t_shake0
    while tk < t_shake1 - 0.05:                # the rattle: two drawings, 3 frames each
        S3.key(tk, "show_jar", 1, "call", props=[jar_rattle(6 if k % 2 == 0 else -6)], pop=False)
        k, tk = k + 1, tk + 0.1
    S3.key(t_shake1, "lift_in", 1, "worried", props=[jar_on_palm], pop=False)       # down again (in-between)
    S3.key(t_setdown, "reach", 1, "worried")
    t_s3_pull = after(t_draw_ph + 0.3, t_setdown, 0.45)     # '看看' pulls a stick and looks at it
    t_s3_relief = after(t_who + 0.15, t_s3_pull, 0.6)
    S3.key(t_s3_pull, "look_stick", 1, "worried", props=[held_up(0)])
    S3.key(t_s3_relief, "relief", 1, "neutral", props=[held(1)])
    S3.key(t_s3_relief + 0.75, "stand", 1, "worried", props=[held(1)], pop=False)

    def s3_jiggle(t):
        if t_shake0 <= t <= t_shake1:
            k = min(1.0, (t - t_shake0) / 0.1, (t_shake1 - t) / 0.1)
            return (-3.0 * k * abs(math.sin(2 * math.pi * 5.5 * (t - t_shake0))), 0.0)
        return (0.0, 0.0)
    S3.jiggle = s3_jiggle

    # S1 (right of the crate) draws next ('是哪个人'), then makes room for Jonah before he is called: one hop
    # upstage-right (the turn hidden in the hop), a planted walk along the back row behind Jonah to the hatch
    # side, a paper turn back to face the crew — all done before Jonah sets off, so nobody crosses his draw
    t_s1_reach = after(t_who + 0.05, t_s3_pull, 0.2)
    t_s1_pull = t_s1_reach + 0.45
    t_s1_relief = after(t_rela - 0.05, t_s1_pull, 0.6)
    S1.key(t_s1_reach, "reach", -1, "worried")
    S1.key(t_s1_pull, "look_stick", -1, "worried", props=[held_up(0)])
    S1.key(t_s1_relief, "relief", -1, "neutral", props=[held(1)])
    t_s1_hop = t_s1_relief + 0.5
    S1.move(t_s1_hop, t_s1_hop + 0.3, (1532, 928, 0.86))
    S1.key(t_s1_hop, "stand", 1, "worried", props=[held(1)])
    t_s1_arr = S1.walk(t_s1_hop + 0.36, (1806, 928, 0.86), 1, "worried", props=[held(1)], pose_after=None)
    S1.turns.append(t_s1_arr)
    S1.key(t_s1_arr, "stand", -1, "worried", props=[held(1)])

    # S0 (behind the crate) draws last of the crew ('惹来了')
    t_s0_reach = after(t_rela + 0.02, t_s1_pull, 0.2)
    t_s0_pull = t_s0_reach + 0.45
    t_s0_relief = after(t_storm + 0.12, t_s0_pull, 0.6)
    S0.key(t_s0_reach, "reach_down", 1, "worried")
    S0.key(t_s0_pull, "look_stick", 1, "worried", props=[held_up(0)])
    S0.key(t_s0_relief, "relief", 1, "neutral", props=[held(1)])
    S0.key(t_s0_relief + 0.8, "stand", 1, "worried", props=[held(1)], pop=False)

    # S3 beckons Jonah over ('你来'); Jonah walks to the jar once S1 is past him
    t_beckon = after(t_storm + 0.25, t_s3_relief + 0.75, 0.5)
    S3.key(t_beckon, "beckon", 1, "neutral", props=[held(1)])
    JN.key(t_draw_ph + 0.65, "j_down", -1, "sorry", pop=False)       # he knows whose lot it will be
    t_jstand = after(t_storm - 0.25, t_draw_ph + 0.65, 0.6)
    JN.key(t_jstand, "j_stand", -1, "worried")
    t_jw0 = max(t_beckon + 0.3, t_s1_arr - 0.3, t_jstand + 0.6)
    t_jw1 = JN.walk(t_jw0, (J_SLOT, JY, 1.0), -1, "worried", dt=0.11, pose_after=None)
    S3.key(after(t_they + 0.1, t_jw1, 0.0), "stand", 1, "worried", props=[held(1)])

    # ---- line 2: Jonah draws the last-but-one stick; '结果，' he looks closer; '抽中的正是约拿！' it glows
    t_j_reach = t_jw1
    t_j_pull = after(t_they + 0.62, t_j_reach, 0.45)
    t_j_look2 = after(t_result, t_j_pull, 0.6)
    JN.key(t_j_reach, "j_reach", -1, "worried")
    JN.key(t_j_pull, "j_look", -1, "worried", props=[held_up(0)])
    JN.key(t_j_look2, "j_look2", -1, "worried", props=[held_up(0, lean=0.2)], pop=False)
    JN.key(t_glow, "j_raise", -1, "surprised", props=[held(0, marked=True, s_mul=1.1, out=30)])
    # two startled little hops back into the light
    t_jback0 = t_glow + 0.8
    mid = (J_SLOT + J_END) / 2
    JN.move(t_jback0, t_jback0 + 0.3, (mid, JY, 1.0))
    JN.move(t_jback0 + 0.42, t_jback0 + 0.72, (J_END, JY, 1.0))
    for tk in (t_jback0, t_jback0 + 0.42):
        JN.key(tk, "j_raise", -1, "surprised", props=[held(0, marked=True, s_mul=1.1, out=30)], pop=False)
    JN.key(t_ask + 0.25, "j_stand", -1, "worried", props=[held(1, marked=True)])

    # the sailors start back, drop their plain sticks, point
    t_r = [t_glow + 0.28, t_glow + 0.36, t_glow + 0.44, t_glow + 0.5, t_glow + 0.58]
    S3.key(t_r[0], "scared", 1, "surprised")
    S3.key(t_r[0] + 0.62, "point", 1, "surprised")
    S1.key(t_r[1], "scared", -1, "surprised")
    S1.key(t_r[1] + 0.75, "point", -1, "surprised")
    S0.key(t_r[2], "scared", 1, "surprised")
    S2.key(t_r[3], "scared", 1, "surprised")
    CP.key(t_r[4], "worried", 1, "surprised")
    # (S0's stick falls just behind the crate he stands behind: out of sight here and in s07, which opens on this)
    dropped = [(t_r[0], S3, (58, 30)), (t_r[1], S1, (-60, 22)), (t_r[2], S0, (44, 6))]

    # '水手们赶紧问他' — they crowd round Jonah (planted walks / hops)
    S3.walk(t_ask + 0.05, (1362, FRONT_Y, 1.0), 1, "worried")
    CP.walk(t_ask + 0.2, (1112, 1018, CAPT_S), 1, "worried")
    S2.walk(t_ask + 0.35, (1292, 930, 0.86), 1, "worried")
    S0.move(t_ask + 0.3, t_ask + 0.62, (S0.start[0] + 34, 952, 0.9))
    S0.key(t_ask + 0.3, "stand", 1, "worried")
    S1.key(t_ask + 0.45, "chin", -1, "worried")       # stays by the hatch, clear of Jonah's sweep to the sea

    # ---- line 3: S3 asks (gestures on each question), the others nod in turn
    S3.key(t_q0, "palm", 1, "worried")
    S3.key(t_q1, "point", 1, "worried")
    S3.key(t_q2, "palm_up", 1, "worried")
    S3.key(t_q3, "palm", 1, "worried")
    S3.key(L[3].end + 0.25, "stand", 1, "worried")
    for tr, (t0, pose_a, pose_b, f) in ((S1, (t_q1 + 0.15, "chin_nod", "chin", -1)),
                                        (S0, (t_q2 + 0.1, "nod", "stand", 1)),
                                        (CP, (t_q3 + 0.05, "nod", "stand", 1)),
                                        (S2, (t_q1 + 0.55, "nod", "stand", 1))):
        tr.key(t0, pose_a, f, "worried", pop=False)
        tr.key(t0 + 0.4, pose_b, f, "worried", pop=False)
    S1.key(L[3].end + 0.3, "stand", -1, "worried")
    JN.key(t_q2 + 0.1, "j_down", -1, "sorry", props=[held(1, marked=True)], pop=False)
    JN.key(t_q3 + 0.35, "j_stand", -1, "worried", props=[held(1, marked=True)], pop=False)

    # ---- line 4: Jonah answers humbly: hand on chest, eyes closed, arm straight up to heaven (the light above him),
    # a paper turn to sweep an open palm out at the towering sea ('大海', a wave bursts over the rail), a turn back
    # to point out to the far coast ('和陆地'), both arms open ('都是他造的')
    lot_near = held(1, marked=True)
    JN.key(t_hebrew, "j_chest", -1, "neutral", props=[lot_near])
    JN.key(t_worship, "j_chest", -1, "peaceful", props=[lot_near], pop=False)
    JN.key(t_heaven, "j_heaven", -1, "neutral", props=[lot_near])
    JN.turns.append(t_sea)
    JN.key(t_sea, "j_sea", 1, "neutral", props=[lot_near])
    JN.turns.append(t_land)
    JN.key(t_land, "j_land", -1, "neutral", props=[lot_near])
    JN.key(t_made, "j_all", -1, "peaceful", props=[lot_near])
    JN.key(L[4].end + 0.45, "j_stand", -1, "neutral", props=[lot_near])
    # the sailors look up with him at '天上的上帝', back down at '大海'
    for tr, dt, f in ((S1, 0.18, -1), (S0, 0.3, 1), (S2, 0.4, 1), (CP, 0.5, 1), (S3, 0.25, 1)):
        tr.key(t_heaven + dt, "lookup", f, "worried", pop=False)
        tr.key(max(t_sea + dt * 0.5, t_heaven + dt + 0.55), "stand", f, "worried", pop=False)

    # ---- line 5: '耶和华，就是上帝的名字' — awe at the light; then the confession and the thought bubble
    for tr, dt in ((S2, 0.2), (CP, 0.35), (S0, 0.45), (S1, 0.6), (S3, 0.75)):
        f = -1 if tr is S1 else 1
        tr.key(t_name + dt, "lookup", f, "surprised", pop=False)
        tr.key(max(t_told + dt * 0.4, t_name + dt + 0.6), "stand", f, "worried", pop=False)
    JN.key(t_name + 0.1, "j_chest", -1, "peaceful", props=[lot_near])
    JN.key(t_told, "confess", -1, "sorry", props=[lot_near])
    # as he tells them he is running away, they grow uneasy
    S3.key(t_flee + 0.2, "stand", 1, "surprised", pop=False)
    S1.key(t_flee + 0.45, "stand", -1, "scared", pop=False)
    CP.key(t_hide + 0.3, "stand", 1, "scared", pop=False)
    S0.key(t_hide + 0.5, "stand", 1, "scared", pop=False)
    S2.key(t_heard + 0.1, "stand", 1, "scared", pop=False)
    S3.key(t_heard + 0.2, "stand", 1, "scared", pop=False)
    # '更加害怕了' — gasp and hop back. These are s07's opening marks and poses (art/scenes/s07_confess.py CAPT, SV0-3,
    # JON): keep them in step with that file.
    back = [(S3, 0.0, (1290, FRONT_Y, 1.0), "scared"), (S1, 0.08, (1834, 928, 0.86), "scared"),
            (CP, 0.14, (1046, 1018, CAPT_S), "worried"), (S0, 0.2, (S0.start[0] - 10, 952, 0.9), "scared"),
            (S2, 0.26, (1246, 930, 0.86), "scared")]
    for tr, dt, to, pose in back:
        t0 = t_afraid + dt
        tr.move(t0, t0 + 0.34, to)
        tr.key(t0, pose, -1 if tr is S1 else 1, "scared")
    # line 6: '你怎么能做这样的事呢？'
    S3.key(t_how, "dismay", 1, "scared")

    # ---- the lot's own glow (follows Jonah's hand; added below Jonah's layer as 'add')
    LG0 = (400, 400)
    lot_glow = doc(f'<ellipse cx="{LG0[0]}" cy="{LG0[1]}" rx="120" ry="100" fill="url(#lotg)"/>', wdefs)

    # ---------------------------------------------------------------- jar on the crate (sticks: 6 5 4 3 2)
    jar_keys = [(tk, 6 - i) for i, tk in enumerate(sorted([0, t_s3_pull, t_s0_pull, t_s1_pull, t_j_pull]))]
    jar_frames = [doc(PR.lots_jar(JAR[0], JAR[1], 1.0, sticks=n)) for _, n in jar_keys]

    def jar_at(t):
        i = 0
        for j, (tk, _) in enumerate(jar_keys):
            if t >= tk:
                i = j
        return float(i)

    def jar_m(t):
        a = 0.0 if t_show - 0.11 <= t < t_setdown else 1.0
        jig = sum(3.0 * math.sin(2 * math.pi * 7 * (t - tj)) * max(0.0, 1 - abs(t - tj) / 0.25)
                  for tj in (t_setdown, t_s3_pull, t_s0_pull, t_s1_pull, t_j_pull))
        return Tf(rot=jig, alpha=a, px=JAR[0], py=JAR[1])
    sc.add("jar", jar_frames, z=21.2, frame_at=jar_at, motion=jar_m)

    # plain sticks dropped on the deck at the reveal
    for i, (td, tr, off) in enumerate(dropped):
        x, y, s = tr.rest(td)
        sc.add(f"dropped{i}", doc(lot_svg(x + off[0], y + off[1], 0.85 * s, 12 - 25 * i)), z=19.5 + 0.01 * i,
               motion=lambda t, td=td: Tf(alpha=1.0 if t >= td else 0.0))

    for tr, seed in ((S2, 201), (S0, 202), (CP, 203), (S1, 204), (S3, 205), (JN, 206)):
        tr.add_to(sc, seed)

    jm = JN.motion()

    def lot_pos(t):
        k = JN.keys[JN.idx(t)]
        pts = k[4]
        if t < t_glow:
            return None
        hand = 0 if t < t_ask + 0.25 else 1          # raised in the far fist, then in the near hand
        _, c = stick_in(pts, hand, 1.1 if hand == 0 else 1.0, True, 30 if hand == 0 else 26)
        home = k[2]
        return apply_tf(jm(t), c, (home[0], home[1]))

    lot_env = keyed([(t_glow - 0.02, 0.0), (t_glow + 0.15, 1.0), (t_ask + 0.3, 0.85), (t_q0 + 1.0, 0.55),
                     (T, 0.45)])

    def lot_glow_m(t):
        p = lot_pos(t)
        if p is None:
            return Tf(alpha=0.0)
        a = lot_env(t) * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.1))
        s = 1.0 + 0.3 * math.exp(-max(0.0, t - t_glow) / 0.35)
        return Tf(dx=p[0] - LG0[0], dy=p[1] - LG0[1], sx=s, sy=s, alpha=a, px=LG0[0], py=LG0[1])
    sc.add("lot_glow", lot_glow, z=25.3, wc=0, blend="add", motion=lot_glow_m)

    # warm glow round Jonah while he stands in the light
    def jglow_m(t):
        x, y, s = JN.pos(t)
        return Tf(dx=x - J_END, alpha=beam_env(t) * (0.8 + 0.2 * math.sin(2 * math.pi * t / 1.3)))
    sc.add("jonah_glow", doc(f'<ellipse cx="{J_END}" cy="{JY - 200}" rx="210" ry="270" fill="url(#jg)"/>', wdefs),
           z=24.9, wc=0, blend="add", motion=jglow_m)

    # ---------------------------------------------------------------- thought bubble: running from God's light
    head = (J_END - 10, JY - 330)
    BC = (1352, 478)
    t_b0, t_b1 = t_told + 0.35, t_heard - 0.05
    bub_env = lambda t: M.progress(t, t_b0, t_b0 + 0.35, "back") * (1 - M.progress(t, t_b1 - 0.25, t_b1, "in"))  # noqa

    def bub_m(t):
        k = bub_env(t)
        if k <= 0.003:
            return Tf(alpha=0.0)
        return Tf(sx=0.3 + 0.7 * k, sy=0.3 + 0.7 * k, alpha=min(1.0, k * 1.4), px=head[0] - 60, py=head[1] + 10)
    sc.add("bubble", bubble_layer(BC[0], BC[1], (head[0] - 40, head[1])), z=26, wc=0.5, motion=bub_m)
    tiny = [doc(C.jonah(BC[0], BC[1] + 92, 0.34, -1, pose=p_, expr="worried")) for p_ in ("run_a", "run_b")]
    tiny.append(doc(C.jonah(BC[0], BC[1] + 92, 0.34, 1, pose="stand", expr="worried")))

    def tiny_at(t):
        if t < t_flee:
            return 2.0
        return float(int((t - t_flee) / 0.2) % 2)

    def tiny_m(t):
        b = bub_m(t)
        if b.alpha <= 0.003:
            return Tf(alpha=0.0)
        u = M.progress(t, t_flee, t_b1 - 0.2, "linear")
        x = 150 - 300 * u
        y = -5 * abs(math.sin(math.pi * (t - t_flee) / 0.2)) if t >= t_flee else 0.0
        # follow the bubble's own pop: carry the tiny figure's feet through the bubble's transform
        foot = (BC[0], BC[1] + 92)
        q = apply_tf(b, (foot[0] + x, foot[1] + y), (0, 0))
        return Tf(dx=q[0] - foot[0], dy=q[1] - foot[1], sx=b.sx, sy=b.sy, alpha=b.alpha, px=foot[0], py=foot[1])
    sc.add("tiny_jonah", tiny, z=26.1, frame_at=tiny_at, motion=tiny_m, wc=0.6)

    sc.add("deck_fg", rehost(V.deck_foreground()), z=30)

    # ---------------------------------------------------------------- camera
    keys = [
        (0.0, Cam(1262, 650, 1620)),
        (t_lai - 1.1, Cam(1262, 662, 1590)),
        (t_show + 0.2, Cam(1250, 690, 1420)),
        (t_draw_ph + 0.4, Cam(1276, 700, 1400)),
        (t_storm, Cam(1292, 700, 1390)),
        (t_they + 0.3, Cam(1360, 700, 1400)),
        (t_glow - 0.05, Cam(1366, 706, 1340)),
        (t_glow + 1.4, Cam(1362, 650, 1480)),
        (t_q0, Cam(1396, 690, 1400)),
        (L[3].end, Cam(1398, 690, 1390)),
        (t_heaven - 0.4, Cam(1440, 672, 1300)),
        (t_name - 0.3, Cam(1450, 668, 1280)),
        (t_name2 + 0.6, Cam(1426, 640, 1340)),
        (t_told + 0.3, Cam(1400, 650, 1400)),
        (t_heard, Cam(1398, 656, 1400)),
        (t_afraid + 0.6, Cam(1374, 662, 1460)),
        (T, Cam(1372, 664, 1450)),
    ]
    cam_base = M.cam_keys(keys, "sine")

    def cam(t):
        c = cam_base(t)
        hw, hh = c.w / 2 + 8, c.w * 9 / 32 + 8          # keep the view (and its slight roll) on the painting
        x = min(max(c.x, hw), W - hw)
        y = min(max(c.y, hh), V.DECK_CUT - hh)
        return Cam(x, y, c.w, 0.25 * math.sin(2 * math.pi * t / 5.4 + 2.2))
    sc.camera = cam

    # ---------------------------------------------------------------- fx
    sc.fx = [
        V.rain_fx(),
        FX.lightning([t_storm, t_afraid - 0.12], dur=0.5, strength=0.24),
        FX.sparkles((J_END - 150, JY - 420, J_END + 150, JY - 120), count=6, t0=t_glow - 0.05, t1=t_ask + 0.8,
                    color=(255, 226, 140), size=(7, 14), period=1.4, drift=-14, seed=5),
        FX.sparkles((1420, 160, 1900, 460), count=20, t0=t_name - 0.1, t1=t_told + 0.6,
                    color=(255, 232, 160), size=(7, 16), period=1.6, drift=-6, seed=8),
    ]

    # ---------------------------------------------------------------- sound
    sc.sfx("waves_storm", 0, dur=T + 0.8, gain_db=-15, fade_in=0.8, fade_out=1.0)
    sc.sfx("storm_wind", 0, dur=T + 0.8, gain_db=-18, fade_in=0.8, fade_out=1.0, pan=-0.2)
    sc.sfx("rain", 0, dur=T + 0.8, gain_db=-16, fade_in=0.8, fade_out=1.0)
    sc.sfx("ship_creak", 0, dur=T + 0.8, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("lots", t_show, gain_db=-12, pan=-0.1)
    for tt in (t_s3_pull, t_s0_pull, t_s1_pull):
        sc.sfx("lots", tt - 0.08, gain_db=-14, pan=0.0)
    sc.sfx("footsteps", t_s1_hop + 0.36, dur=t_s1_arr - t_s1_hop - 0.3, gain_db=-19, pan=0.55, fade_out=0.15)
    sc.sfx("footsteps", t_jw0, dur=t_jw1 - t_jw0 + 0.1, gain_db=-17, pan=0.4, fade_out=0.15)
    sc.sfx("lots", t_j_pull - 0.08, gain_db=-12, pan=0.15)
    # the lot falls on Jonah: a soft, low far rumble (the crack faded out) — grave, not a prize
    sc.sfx("thunder", t_glow - 0.1, dur=2.4, gain_db=-18, pan=0.3, fade_in=0.45, fade_out=1.0)
    sc.sfx("footsteps", t_ask + 0.05, dur=1.0, gain_db=-17, pan=0.0, fade_out=0.2)
    sc.sfx("chime", t_name + 0.05, gain_db=-12, pan=0.35)
    sc.sfx("pop", t_b0, gain_db=-14, pan=0.1)
    sc.sfx("pop", t_b1 - 0.2, gain_db=-16, pan=0.1)
    sc.sfx("thunder", t_storm, dur=2.6, gain_db=-15, pan=0.3, fade_out=1.2)
    sc.sfx("thunder", t_afraid - 0.15, dur=2.0, gain_db=-16, pan=0.2, fade_out=0.9)   # starts in the pause before
    sc.sfx("cloth", t_afraid + 0.05, gain_db=-12, pan=-0.1)

    # key times, for reviewers (seconds from scene start)
    sc.events = {
        "huddle talk/nods": t_l0 + 0.3, "huddle breaks up": t_up, "S3 takes the jar ('来，')": t_show,
        "jar rattle": (t_shake0, t_shake1), "S3 draws ('看看')": t_s3_pull,
        "S1 draws ('是哪个人')": t_s1_pull, "S0 draws ('惹来了')": t_s0_pull, "lightning ('大风暴')": t_storm,
        "S1 hops up and walks behind Jonah": (t_s1_hop, t_s1_arr), "S3 beckons": t_beckon,
        "Jonah looks closer ('结果，')": t_j_look2,
        "Jonah walks to the jar": (t_jw0, t_jw1), "Jonah draws ('他们就抽签')": t_j_pull,
        "lot glows + light ('抽中的正是约拿')": t_glow, "sailors start back": t_r[0],
        "Jonah hops into the light": t_jback0, "crowd in ('水手们赶紧问他')": t_ask, "S3 asks": (t_q0, t_q1, t_q2, t_q3),
        "Jonah: chest": t_hebrew, "eyes closed ('我敬拜')": t_worship, "arm to heaven ('天上的上帝')": t_heaven,
        "sea ('大海')": t_sea, "land ('和陆地')": t_land, "arms open ('都是他造的')": t_made,
        "light + awe ('耶和华，')": t_name, "confess + bubble": (t_told, t_b0), "tiny Jonah runs ('他正在逃跑')": t_flee,
        "bubble out": t_b1, "scared faces ('水手们听了')": t_heard, "gasp, hop back, thunder ('更加害怕了')": t_afraid,
        "S3 dismay ('你怎么能…')": t_how,
    }
    return sc
