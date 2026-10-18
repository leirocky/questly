"""Scene 8 (v2) — the sailors row hard for the shore but cannot; they pray to the LORD (Jonah 1:13-14).

Wide storm shot in the v1 storm style (art/scenes_v1/s04_storm.py: storm sky and cloud banks, rounded foam-capped
waves, slanted rain, the ship with its torn striped sail, bow to the LEFT). A dark coastline with a little lit harbour
town lies far away on the left, ahead of the bow.

Line 0 (N) '水手们不忍心把约拿扔下去。' the crew stand around Jonah (by the mast, hand on his chest as in s07); two
        sailors hold up a palm and shake their heads: no, we won't. '他们拼命划桨，' a squash-and-hop cut: the four
        sailors grab long oars over the rail and row hard (an 8-drawing stroke cycle with a big body swing, a stroke
        every ~1.3 s, hands glued to the handle by a small continuous lean), blades dip with a splash in time with
        the 'oars' sound, the captain points at the shore on the horizon; '想让船回到岸边。' the camera pulls back to
        show the coast (it has widened before the first splash, which so stays above the subtitles); the coast slowly
        grows (the ship gains a little).
Line 1 (N) '但是，海浪越翻越高。' a huge dark wall of water rises between the ship and the shore, higher and higher,
        hiding the coast (lightning); its curl stays well ahead of the bow; frantic strokes (~1.05 s) from here;
        '他们怎么用力划桨，' sweating, tired faces; '都没有办法回到岸边。' in the last 0.4 s the wave rushes in and
        pitches onto the bow: a burst of foam, the bow rears up, the ship is shoved back to the right, the wave
        collapses into the sea and the shore reappears smaller, receding into the haze; the sailors lose their grip
        (scared): the wave wrenches the oars back in their locks, they bounce (always slanted), slip out through
        the locks and drop into the sea (small splashes).
Line 2 (N) '水手们只好向约拿的上帝耶和华祷告：' the sailors and the captain kneel (hard cuts hidden in a dip), hands
        pressed together, looking up; Jonah stands among them, hand on his chest; the camera moves in.
Line 3 (S) '耶和华啊，' the clouds part a little above the ship: a small clear pale-gold opening, the lids' inner
        edges lit warm, and four narrow golden shafts that pass between the kneeling heads and fade on the deck
        (God is never shown as a person); the sailors raise their arms; '求你不要因为这个人惩罚我们，' hands pressed
        together again, pleading, eyes to the sky; '也不要怪我们害了他。' heads bowed.
Line 4 (S) '因为这一切，' arms raised once more, eyes closed, mouths a small earnest 'o' (praying aloud - not relieved:
        the storm goes on until s09); '都是你照着自己的心意做的。' the light glows on; the scene ends on a calm, held
        frame (rain and rocking eased).
End frame (for s09): ship at SX0 + 262, no oars; kneeling, arms raised, eyes closed (expr 'sleepy'): sailor 0 at
        lx 274, sailor 1 at 132, Jonah standing at -4 (hand on chest), sailor 2 at -116, sailor 3 at -250, the
        captain at -362 (the stern lantern hangs behind his back); camera (1682, 670, 1600).

Every key time comes from the narration chunks (a phrase inside a chunk is placed by its character position).
Pose changes are hard cuts sold by a squash / hop (never crossfaded); each pose is held >= 0.5 s.

Technique notes
* Rowing: each rower has 8 drawings per stroke (custom poses through the rig of art/characters.py, with a public-pose
  fallback); between drawings the rower leans slightly about his feet so his drawn hand follows the path through the
  drawn hands, and the oar (inboard + outboard layers pivoting in the oarlock) is aimed through that hand. The blade
  is lifted by sliding the outboard part along its shaft, not by squashing it.
* The stroke times ARE the 'oars' sound: plan_oars() synthesises the two 'oars' cues exactly as audio/mix.py will
  (same seed / length / cycle) and reads where each blade dips in; the visual catches (and splashes) sit on them.
* Kneeling figures sit back on their heels (an upright kneel behind the rail would read as standing); they are drawn
  behind the rail, shields and stern lantern like everyone on deck (the oars are gone by then).
* The huge wave is drawn at its impact place, wholly inside the canvas, and only ever moved left of it, so no cut
  edge can show; its motion is planned by where the curl's lip should be.
* Stage 2640 x 1520; the camera never shows y > 1440 nor the outer 48 px at the sides, and every layer that touches a
  canvas edge only ever moves away from it (a rasterised layer is cut at the canvas edge).
"""
import bisect
from dataclasses import replace
import json
import math
import random
import zlib

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s04_storm as V
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import CACHE, SR
from engine.scene import Scene

W, H = 2640, 1520               # the camera never shows y > VIEW_BOTTOM (the margin below hides layer cut-offs)
VIEW_BOTTOM = 1440
INK = S.INK
HORIZON = 800

# ---------------------------------------------------------------- the ship (un-moved position)
SS = 0.92                     # ship + crew scale (as v1 s04)
SF = -1                       # bow to the LEFT (sailing west, as in s03-s06); the shore lies ahead of the bow
SX0, SY = 1360.0, 1130.0      # ship anchor = hull centre on the waterline
PIV = (SX0, SY + 40.0)        # pitch pivot

# crew along the deck (ship-local x: + toward the bow)
ROWERS = [("A", 0, 300.0), ("B", 1, 158.0), ("C", 2, -142.0), ("D", 3, -276.0)]
JON_LX = -4.0                 # Jonah in front of the mast
CAPT_LX = -418.0              # the captain on the raised stern deck
CAPT_KNEEL_LX = -362.0        # where he kneels to pray
OAR_DX = 104.0                # oarlock this far (local px) toward the stern from each rower's feet

# rowing stroke (rower-local px, scale 1, facing right = toward the stern)
HX_CATCH, HX_FIN = 100.0, 26.0     # near-hand x at the catch / finish
HY_DRIVE = -150.0                  # near-hand height while the blade pulls
T_CATCH, T_FIN = 22.0, -27.0       # torso tilt (a big swing: they row with all their strength)
FIN_LEAN = {"C": 0.4}              # C (next to Jonah's head-cloth flap) leans back less at the finish
N_ROW = 8                          # drawings per stroke
CYCLE_STEADY, CYCLE_FAST = 1.4, 1.05   # 'oars' sound cycles (s per stroke): hard rowing, then frantic
OAR_IN = 175.0                     # drawn inboard length (oarlock -> handle end) at sy = 1
OAR_OUT = 330.0                    # drawn outboard length (oarlock -> blade tip) at sy = 1
BLADE_L = 96.0
HANDLE_OVER = 34.0                 # handle end beyond the near hand
DEPTH_PULL, DEPTH_LIFT = 40.0, -24.0   # blade tip below the waterline (local px) in the pull / recovery

GRADE = V.GRADE_DEFS
PUNCT = "，。！？：；、,.!?:;"


def doc(body, defs=""):
    return S.svg_doc(body, defs, w=W, h=H)


def fm(v):
    return f"{v:.1f}"


def graded(markup):
    return V.graded(markup)


def hull_top(lx):
    return -165 - 75 * (abs(lx) / 480) ** 3.2


def ship_pt(lx, ly):
    return SX0 - lx * SS, SY + ly * SS


def deck_y(lx):
    return SY + hull_top(lx) * SS


def rail_y(lx):
    return SY + (hull_top(lx) - 54) * SS


def stage_x(lx):
    return SX0 - lx * SS


def sstep(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def sub_at(line, phrase):
    """Time a phrase starts: its chunk's start plus its character position inside the chunk."""
    for c in line.chunks:
        if phrase in c.text:
            pre = c.text[:c.text.index(phrase)]
            n_pre = sum(1 for ch in pre if ch not in PUNCT)
            n_all = max(1, sum(1 for ch in c.text if ch not in PUNCT))
            return c.start + (c.end - c.start) * n_pre / n_all
    if phrase in line.text:
        return line.start + (line.end - line.start) * line.text.index(phrase) / max(1, len(line.text))
    raise KeyError(phrase)


def safe_at(line, phrases, default):
    for ph in phrases:
        try:
            return sub_at(line, ph)
        except (KeyError, AttributeError):
            continue
    return default


# ---------------------------------------------------------------- figures (custom poses through the rig)

def _design(kind, variant=0):
    if kind == "sailor":
        return C._sailor_design(variant), C._SAILOR_M
    if kind == "captain":
        return C._captain_design(), C._CAPTAIN_M
    return C._jonah_design(), C._ADULT


def person(kind, x, y, facing, ps, expr, variant=0, marks=True, scale=SS, fallback="stand"):
    """A library figure in a custom pose dict (the rig of art/characters.py). Falls back to a public pose if the
    rig's internals ever change."""
    try:
        D, m = _design(kind, variant)
        inner, _ = C._figure(D, m, dict(ps), expr, C._fsign(facing), marks)
        return C._wrap_out(inner, x, y, scale, facing, f"{kind}{variant}-s08")
    except Exception:
        if kind == "sailor":
            return C.sailor(x, y, scale, facing, variant=variant, pose=fallback, expr=expr, marks=marks)
        if kind == "captain":
            return C.captain(x, y, scale, facing, pose=fallback if fallback in C.CAPTAIN_POSES else "stand",
                             expr=expr, marks=marks)
        return C.jonah(x, y, scale, facing, pose=fallback, expr=expr, marks=marks)


def person_points(kind, x, y, facing, ps, expr, variant=0):
    try:
        return C.body_points(lambda x_, y_, s_, f_: person(kind, x_, y_, f_, ps, expr, variant, scale=s_),
                             x, y, SS, facing)
    except Exception:
        return None


def row_curve(psi, fin=1.0):
    """Near-hand target (rower-local, scale 1), torso tilt for stroke position psi (0 catch, .5 finish);
    ``fin`` scales the backward lean at the finish."""
    psi %= 1.0
    tf = T_FIN * fin
    if psi < 0.5:
        u = psi / 0.5
        e = 0.5 - 0.5 * math.cos(math.pi * u)
        return (HX_CATCH + (HX_FIN - HX_CATCH) * e, HY_DRIVE - 10 * math.sin(math.pi * u),
                T_CATCH + (tf - T_CATCH) * e)
    u = (psi - 0.5) / 0.5
    e = 0.5 - 0.5 * math.cos(math.pi * u)
    lift = sstep(u / 0.16) * (1 - sstep((u - 0.82) / 0.18))
    return HX_FIN + (HX_CATCH - HX_FIN) * e, HY_DRIVE + 14 * lift, tf + (T_CATCH - tf) * e


def blade_depth(psi):
    """Blade tip depth below the waterline (local px): in the water during the pull, lifted in the recovery."""
    psi %= 1.0
    if psi < 0.5:
        w = 1.0
    else:   # lifts out at the finish, dips in again just before the catch
        w = max(1 - sstep((psi - 0.5) / 0.07), sstep((psi - 0.955) / 0.045))
    return DEPTH_LIFT + (DEPTH_PULL - DEPTH_LIFT) * w


def row_pose(psi, rel_o, expr, fin=1.0):
    """Pose dict for stroke position psi; rel_o = oarlock in rower-local coords (to aim the far hand)."""
    hx, hy, tilt = row_curve(psi, fin)
    ux, uy = hx - rel_o[0], hy - rel_o[1]
    L = math.hypot(ux, uy) or 1.0
    fx, fy = hx + 24 * ux / L, hy + 24 * uy / L        # far hand further up the shaft (toward the handle end)
    drop = 24 - 6 * (T_CATCH - tilt) / (T_CATCH - T_FIN * fin)
    return C._P(t=tilt, h=-8, drop=drop, legs=(("ik", 64, 0), ("ik", -24, 1)),
                arms=(("ik", "abs", fx, fy, 1), ("ik", "abs", hx, hy, 1)), expr=expr)


POSE = C.POSES
# kneeling low, sitting back on the heels (an upright kneel hidden behind the rail would read as standing)
_LOW = dict(legs=((86, -100), (88, -100)), t=0)
KNEEL_PRESS = dict(POSE["kneel_pray"], expr="worried", look=(0.02, -0.06), **dict(_LOW, t=-3))   # eyes to the sky
KNEEL_UP = dict(POSE["kneel_pray"], arms=(("fk", 146, 164), ("fk", -140, -160)), hands=("open", "open"), h=-24,
                look=(0.02, -0.06), **_LOW)
KNEEL_BOW = dict(POSE["kneel_pray"], legs=_LOW["legs"], t=10, h=14)
REFUSE = dict(POSE["refuse"], arms=(("fk", 8, 3), ("fk", -46, -112)))
POINT_UP = dict(POSE["point"], arms=(("fk", 98, 102), ("fk", -8, -3)), h=-2)    # at the shore on the horizon
END_EXPR = "sleepy"     # last prayer: eyes closed, a small 'o' mouth (praying aloud, earnest - not relieved)
STAND = dict(POSE["stand"])
SCARED = dict(POSE["scared"])
POINT = dict(POSE["point"])
WORRIED = dict(POSE["worried"])


# ---------------------------------------------------------------- the oars sound -> stroke times

def oar_dips(scene_id, at, dur, cycle):
    """Times (s after the cue start) at which the 'oars' loop that audio/mix.py will synthesise for this cue (same
    seed, length and cycle) dips its blades in. Cached on disk; None if the sound library is unavailable."""
    try:       # the synth may still change: its source is part of the key
        import hashlib
        from audio import sfx as _sfx
        ver = hashlib.sha1(open(_sfx.__file__, "rb").read()).hexdigest()[:12]
    except Exception:
        ver = "?"
    key = f"{scene_id}:oars:{float(at)}:{float(dur):.4f}:{float(cycle)}:{ver}"
    path = CACHE / "s08_oars.json"
    try:
        cache = json.loads(path.read_text())
    except Exception:
        cache = {}
    if key in cache:
        return cache[key]
    res = None
    try:
        from audio import sfx
        seed = zlib.crc32(f"{scene_id}:oars:{float(at)}".encode()) & 0xFFFF
        n = int(round(float(dur) * SR))
        m = max(n, int(0.25 * SR))
        p = {"width": 1.0, **sfx.PARAMS.get("oars", {})}
        p["cycle"] = float(cycle)
        rec = []
        orig = sfx._place

        def hook(buf, x, i0, *a, **kw):
            rec.append(int(i0))
            return orig(buf, x, i0, *a, **kw)
        sfx._place = hook
        try:
            core = sfx._loop_core("oars", m, SR, seed, p)
        finally:
            sfx._place = orig
        xb = sfx._balance(core)
        rot = sfx._rotate_quiet(xb, SR)
        a = np.max(np.abs(xb), axis=1)
        from scipy import ndimage
        pair = np.maximum(a, np.roll(a, 1))
        env = ndimage.uniform_filter1d(a, max(1, int(0.03 * SR)), mode="wrap")
        i = int(np.argmin(pair + 0.05 * env))
        if np.allclose(np.roll(xb, -i, axis=0)[:2048], rot[:2048]):
            ts = sorted(((r - i) % m) / SR for r in rec)
            groups = []
            for t in ts:
                if groups and t - groups[-1][-1] < 0.08:
                    groups[-1].append(t)
                else:
                    groups.append([t])
            if len(groups) > 1 and groups[-1][-1] - groups[0][0] > m / SR - 0.08:   # a pair wrapped around
                groups[0] = groups.pop() + groups[0]
            res = sorted(min(g) if g[0] <= g[-1] else g[0] for g in groups)
    except Exception:
        res = None
    if res is not None:
        # parallel build workers share this file: merge with what is there now and replace it atomically
        try:
            import os
            import tempfile
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                cache = {**json.loads(path.read_text()), key: res}
            except Exception:
                cache[key] = res
            fd, tmp = tempfile.mkstemp(prefix=".s08_oars.", suffix=".tmp", dir=str(path.parent))
            try:
                with os.fdopen(fd, "w") as fh:
                    fh.write(json.dumps(cache))
                os.replace(tmp, path)
            except Exception:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
        except Exception:
            pass
    return res


def _cycle_for(dur, want, kmin=1):
    """The 'oars' loop holds a whole number of strokes: pass exactly dur / k so the period is the wanted one."""
    k = max(kmin, int(round(dur / want)))
    return round(dur / k, 4)


def plan_oars(scene_id, t_grab, t_switch, t_lose):
    """Pick the two 'oars' cues (hard strokes ~1.4 s apart, then frantic ones ~1.05 s apart from ``t_switch``) so
    the first dip comes ~0.85 s after the sailors grab the oars (the camera has pulled back by then, so the first
    splash sits above the subtitles), the tempo change has no double stroke and no stroke is cut by a cue's fade.
    Returns (cues, catches): cues [(at, dur, cycle)], catch times in scene seconds (the visual stroke follows
    exactly these dips)."""
    first_want = t_grab + 0.85
    best1 = None
    for k in range(44):        # (the loop is rotated to start quietly: its first dip comes 0.1-0.4 s after 'at')
        at = round(t_grab - 0.1 + 0.025 * k, 3)
        dur = round(t_switch + 0.12 - at, 3)
        cyc = _cycle_for(dur, CYCLE_STEADY)
        d = oar_dips(scene_id, at, dur, cyc)
        if d is None:
            break
        dips = sorted(at + x for x in d)
        first = dips[0]
        late = [x for x in dips if x > at + dur - 0.32]          # would be cut by the fade-out
        score = abs(first - first_want) + 3 * len(late) + (3 if first < t_grab + 0.45 else 0)
        if best1 is None or score < best1[0]:
            best1 = (score, at, dur, cyc, dips)
        if score < 0.06:
            break
    if best1 is None:          # no sound library: a plain metronome
        c1 = list(np.arange(first_want, t_switch - 0.1, CYCLE_STEADY))
        c2 = list(np.arange(c1[-1] + 1.2, t_lose - 0.25, CYCLE_FAST))
        return [], c1 + c2
    _, a1, d1, cy1, dips1 = best1
    keep1 = [x for x in dips1 if x < a1 + d1 - 0.32] or [first_want]
    best2 = None
    for k in range(32):
        at = round(t_switch - 0.2 + 0.025 * k, 3)
        dur = round(t_lose + 0.12 - at, 3)
        cyc = _cycle_for(dur, CYCLE_FAST, 2)
        d = oar_dips(scene_id, at, dur, cyc)
        if d is None:
            break
        dips = sorted(at + x for x in d)
        if not dips or dips[0] < at + 0.2:
            continue
        gap = dips[0] - keep1[-1]
        late = [x for x in dips if t_lose - 0.25 < x]
        score = abs(gap - 1.2) + (5 if gap < 0.95 else 0) + 3 * len(late)
        if best2 is None or score < best2[0]:
            best2 = (score, at, dur, cyc, dips)
        if score < 0.06:
            break
    if best2 is None:
        c2 = list(np.arange(keep1[-1] + 1.2, t_lose - 0.25, CYCLE_FAST))
        return [(a1, d1, cy1)], keep1 + c2
    _, a2, d2, cy2, dips2 = best2
    keep2 = [x for x in dips2 if x < t_lose - 0.25]
    return [(a1, d1, cy1), (a2, d2, cy2)], keep1 + keep2


# ---------------------------------------------------------------- scenery drawings

def sea_layer(f, fill, light, dark, wl, amp, seed, x0=-400, x1=W + 400, foam_size=1.0, sw=4.5, cap_amp=None,
              bottom=H + 120):
    """v1 s04 sea band (rounded foam caps, lace, dark troughs) with a configurable extent."""
    d, pts = V.band_path(f, x0, x1, 14, bottom)
    body = S.path(d, fill=fill, sw=sw)
    hl = S.smooth_path([(x, y + 14 + 0.12 * amp) for x, y in pts], closed=False)
    body += (f'<path d="{hl}" fill="none" stroke="{light}" stroke-width="{12 + 0.2 * amp:.1f}" opacity="0.4" '
             f'stroke-linecap="round"/>')
    r = random.Random(seed)
    for xc, yc in V.crests(f, x0, x1):
        y = yc + amp * 1.6 + r.uniform(10, 30)
        xa, xb = xc - wl * r.uniform(0.2, 0.32), xc + wl * r.uniform(0.15, 0.3)
        body += (f'<path d="M{fm(xa)},{fm(y)} Q{fm((xa + xb) / 2)},{fm(y - 16 - 0.15 * amp)} {fm(xb)},{fm(y + 8)}" '
                 f'fill="none" stroke="{dark}" stroke-width="6" opacity="0.35" stroke-linecap="round"/>')
    caps = ""
    for i, (xc, yc) in enumerate(V.crests(f, x0 + 30, x1 - 30)):
        a = cap_amp(xc) if cap_amp else amp
        caps += V.foam_cap(f, xc, wl, a, seed * 31 + i, foam_size * (0.75 + 0.25 * min(1.0, a / max(amp, 1))))
    return S.g(body, filter="wobble") + S.g(caps, filter="wobble-fine")


def sky_svg():
    defs = (S.lin_grad("s8sky", [(0, P["storm_sky_top"]), (0.42, P["storm_sky"]),
                                  (0.56, S.mix(P["storm_sky"], P["sea_pale"], 0.28)), (0.62, P["storm_sea_light"]),
                                  (1, S.shade(P["storm_sea"], -0.15))]))
    b = S.rect_bg("url(#s8sky)", W, H)
    b += S.g("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="0.5"/>'
                     for x, y, rx, ry, c in (
                         (380, 260, 600, 180, P["storm_cloud"]), (1350, 160, 720, 170, P["storm_sky_top"]),
                         (2250, 290, 620, 190, P["storm_cloud"]), (900, 560, 600, 110, P["storm_cloud_light"]),
                         (1950, 580, 560, 100, P["storm_cloud_light"]))), filter="blur-md")
    # rain curtains hanging from the clouds
    b += S.g("".join(f'<path d="M{x},380 L{x + 180},380 L{x + 70},790 L{x - 110},790 Z" fill="{P["storm_cloud"]}" '
                     f'opacity="0.28"/>' for x in (260, 1150, 2050, 2500)), filter="blur-md")
    # low clouds on the horizon
    far = ""
    for i, (x, y, w_, h_) in enumerate(((900, 700, 520, 110), (1500, 690, 560, 120), (2080, 705, 600, 120),
                                        (2560, 700, 420, 100))):
        far += V.storm_cloud(x, y, w_, h_, 120 + i, P["storm_cloud_light"],
                             S.mix(P["storm_cloud"], P["storm_sky"], 0.3), "#a9b4c4", sw=3)
    b += S.g(far, filter="wobble", opacity=0.92)
    return doc(b, defs)


def far_sea_svg():
    """Sea from the horizon down (static): a light band with small far waves."""
    defs = S.lin_grad("s8seab", [(0, S.mix(P["storm_sea_light"], P["storm_sky"], 0.25)), (0.25, P["storm_sea_light"]),
                                 (1, S.shade(P["storm_sea"], -0.2))])
    b = f'<rect x="-20" y="{HORIZON}" width="{W + 40}" height="{H - HORIZON + 40}" fill="url(#s8seab)"/>'
    b += S.g(S.path(f"M-20,{HORIZON} L{W + 20},{HORIZON}", sw=3), filter="wobble", opacity=0.55)
    f_far = V.wave_fn(HORIZON + 14, 12, 230, 0.4, p=1.6, lean=0.25)
    b += sea_layer(f_far, S.mix(P["storm_sea_light"], P["storm_sky"], 0.2), P["sea_pale"], P["storm_sea"], 230, 12, 1,
                   x0=-80, x1=W + 80, foam_size=0.45, sw=3)
    return doc(b, defs)


def coast_svg():
    """The shore far ahead of the bow: a headland that rises out of the sea and ends in a cliff (two bands of dark
    hills), a little harbour town with warm windows, a watchtower and palms, surf at its foot, softened by rain
    haze. Bounded on both sides (it shrinks and slides as the ship is pushed back). Sits on the horizon."""
    y0 = HORIZON + 2
    back = S.mix(P["storm_cloud_light"], P["storm_sky"], 0.45)
    mid = S.mix(P["storm_cloud"], "#4b5d58", 0.55)
    near = S.mix("#3e4f4a", P["storm_sea"], 0.25)
    b = ""
    b += S.path(S.smooth_path([(40, y0), (110, y0 - 90), (190, y0 - 150), (320, y0 - 150), (430, y0 - 190),
                               (560, y0 - 160), (690, y0 - 120), (790, y0 - 70), (870, y0 - 20), (890, y0)],
                              closed=True, tension=0.8), fill=back, sw=2.5)
    b += S.path(S.smooth_path([(70, y0), (130, y0 - 60), (200, y0 - 104), (290, y0 - 104), (390, y0 - 126),
                               (510, y0 - 112), (610, y0 - 92), (690, y0 - 84), (730, y0 - 40), (770, y0)],
                              closed=True, tension=0.7), fill=mid, sw=3)
    town = ""
    r = random.Random(8)
    houses = [(280, 102, 34, 24), (316, 108, 28, 20), (352, 116, 38, 26), (392, 120, 30, 22), (426, 114, 36, 24),
              (466, 106, 30, 20), (502, 100, 40, 26), (544, 96, 28, 18), (578, 90, 32, 22)]
    wall = S.mix(P["stone"], P["storm_cloud_light"], 0.55)
    for x, top, w_, h_ in houses:
        town += (f'<rect x="{x}" y="{fm(y0 - top)}" width="{w_}" height="{h_ + 30}" '
                 f'fill="{S.shade(wall, -0.12 * r.random())}" stroke="{INK}" stroke-width="2.2"/>')
        town += f'<rect x="{x - 2}" y="{fm(y0 - top - 4)}" width="{w_ + 4}" height="5" fill="{S.shade(wall, -0.3)}"/>'
        if r.random() < 0.8:
            wx = x + r.uniform(6, w_ - 12)
            wy = y0 - top + r.uniform(6, h_ - 6)
            town += f'<rect x="{fm(wx)}" y="{fm(wy)}" width="6" height="7" fill="#ffd27a"/>'
    tx = 630
    town += (f'<rect x="{tx}" y="{y0 - 160}" width="30" height="120" fill="{S.shade(wall, -0.1)}" stroke="{INK}" '
             f'stroke-width="2.4"/>')
    town += "".join(f'<rect x="{tx - 3 + 9 * k}" y="{y0 - 168}" width="6" height="9" fill="{S.shade(wall, -0.1)}" '
                    f'stroke="{INK}" stroke-width="1.6"/>' for k in range(4))
    town += f'<rect x="{tx + 11}" y="{y0 - 140}" width="8" height="11" fill="#ffd27a"/>'
    for px, ph in ((250, 70), (600, 60), (715, 52)):
        base = y0 - 82 if px < 630 else y0 - 70
        town += (f'<path d="M{px},{base} Q{px + 6},{base - ph * 0.6} {px + 2},{base - ph}" fill="none" stroke="{INK}" '
                 f'stroke-width="4"/>')
        for a in (-150, -110, -60, -20, 20):
            ra = math.radians(a)
            ex, ey = px + 2 + 26 * math.cos(ra), base - ph + 10 + 16 * math.sin(ra) + 10
            town += (f'<path d="M{px + 2},{base - ph} Q{fm((px + ex) / 2)},{fm(base - ph - 10)} {fm(ex)},{fm(ey)}" '
                     f'fill="none" stroke="{S.mix(P["leaf_dark"], P["storm_cloud"], 0.4)}" stroke-width="6" '
                     f'stroke-linecap="round"/>')
    b += town
    b += S.path(S.smooth_path([(100, y0 + 4), (150, y0 - 40), (230, y0 - 74), (310, y0 - 60), (450, y0 - 80),
                               (600, y0 - 66), (730, y0 - 62), (820, y0 - 58), (842, y0 - 30), (856, y0 + 4)],
                              closed=True, tension=0.6), fill=near, sw=3.2)
    b += (f'<path d="M770,{y0 - 50} L830,{y0 - 44} M740,{y0 - 30} L820,{y0 - 22}" stroke="{S.shade(near, -0.3)}" '
          f'stroke-width="3" opacity="0.6"/>')
    for x in range(110, 880, 64):
        b += f'<ellipse cx="{x}" cy="{y0 + 2}" rx="30" ry="6" fill="{P["foam"]}" stroke="{INK}" stroke-width="1.8"/>'
    defs = S.rad_grad("s8haze", [(0, S.mix(P["storm_sky"], P["sea_pale"], 0.3), 0.3),
                                 (0.7, S.mix(P["storm_sky"], P["sea_pale"], 0.3), 0.22),
                                 (1, S.mix(P["storm_sky"], P["sea_pale"], 0.3), 0.0)])
    b = S.g(b, filter="wobble")
    b += f'<ellipse cx="470" cy="{y0 - 60}" rx="520" ry="220" fill="url(#s8haze)"/>'
    return doc(b, defs)


WAVE_LIP = (330.0, -490.0)      # the curl's leading tip, relative to the wave anchor (unscaled)
WAVE_SPIRAL = (262.0, -462.0)   # centre of the foam spiral in the curl


def big_wave_svg(cx, base):
    """The huge wave that rises between the ship and the shore: a tall, steep, dark wall of water (darker than the
    sea around it, so it reads as a rising wall) with a light translucent band under the crest, a curl over toward
    the ship (right), foam puffs along the top and a small foam spiral in the curl. Anchor = (cx, base); drawn
    with its back foot at x = cx - 570, so with cx >= 580 it lies wholly inside the canvas (no cut edge can show
    whatever its motion)."""
    hgt = 640
    wall = S.mix(S.shade(P["storm_sea"], -0.2), "#1f3d4c", 0.25)
    mid = S.shade(P["storm_sea"], -0.04)
    lite = S.mix(P["sea_light"], P["storm_sea_light"], 0.5)
    pts = [(cx - 570, base + 90), (cx - 450, base + 18), (cx - 345, base - 150), (cx - 215, base - 420),
           (cx - 80, base - 585), (cx + 60, base - hgt), (cx + 195, base - 626), (cx + 292, base - 566),
           (cx + WAVE_LIP[0], base + WAVE_LIP[1]), (cx + 302, base - 428), (cx + 256, base - 408),
           (cx + 236, base - 300), (cx + 280, base - 140), (cx + 410, base + 60)]
    d = S.smooth_path(pts, closed=True, tension=0.85)
    defs = S.lin_grad("s8bw", [(0, lite), (0.2, mid), (0.55, wall), (1, S.shade(wall, -0.15))],
                      x1=0, y1=0, x2=0, y2=1)
    b = S.path(d, fill="url(#s8bw)", sw=5)
    # hollow under the curl (darkest), a pale rim of light just under the crest, streaks on the back
    b += S.path(S.smooth_path([(cx + 298, base - 470), (cx + 244, base - 420), (cx + 226, base - 300),
                               (cx + 264, base - 160), (cx + 330, base - 80), (cx + 292, base - 260),
                               (cx + 302, base - 400)], closed=True, tension=0.8), fill=S.shade(wall, -0.25),
                stroke=False, extra='opacity="0.8"')
    rim = [(cx - 300, base - 300), (cx - 190, base - 455), (cx - 60, base - 565), (cx + 70, base - 605),
           (cx + 190, base - 590), (cx + 268, base - 540)]
    b += (f'<path d="{S.smooth_path(rim, closed=False)}" fill="none" stroke="{P["sea_pale"]}" stroke-width="22" '
          f'stroke-linecap="round" opacity="0.35"/>')
    for k, (xa, ya, xb, yb) in enumerate(((cx - 420, base - 100, cx - 260, base - 300),
                                         (cx - 300, base - 250, cx - 140, base - 460),
                                         (cx - 200, base - 140, cx - 40, base - 330),
                                         (cx - 90, base - 300, cx + 70, base - 480),
                                         (cx - 40, base - 110, cx + 120, base - 260))):
        b += (f'<path d="M{xa},{ya} Q{(xa + xb) / 2 + 30},{(ya + yb) / 2 + 20} {xb},{yb}" fill="none" '
              f'stroke="{P["sea_pale"]}" stroke-width="7" stroke-linecap="round" opacity="0.4"/>')
    b += (f'<path d="M{cx - 400},{base - 60} Q{cx - 300},{base - 120} {cx - 140},{base - 80} T{cx + 250},{base - 60}" '
          f'fill="none" stroke="{P["foam"]}" stroke-width="6" stroke-dasharray="40 22" opacity="0.45"/>')
    body = S.g(b, filter="wobble")
    # foam along the crest and a small spiral in the curl
    circ = []
    for k in range(14):
        u = k / 13
        x = cx - 200 + 500 * u
        y = (base - 560 + 70 * (1 - u) ** 2 - 90 * math.sin(math.pi * min(1, u * 1.15))
             + (60 * (u - 0.75) / 0.25 if u > 0.75 else 0))
        circ.append((x, y + 18, 24 + 16 * math.sin(math.pi * u)))
    foam = V.puffs(circ, P["foam"], 4.0, shade=(P["sea_pale"], (cx + 60, base - 560, 260, 40), 0.8), cid="s8bwf")
    sp = []
    for k in range(24):
        a = math.radians(-60 + 26 * k)
        rr = 50 * (1 - k / 30)
        sp.append((cx + WAVE_SPIRAL[0] + rr * math.cos(a), base + WAVE_SPIRAL[1] + rr * math.sin(a)))
    foam += (f'<path d="{S.smooth_path(sp, closed=False)}" fill="none" stroke="{INK}" stroke-width="25" '
             f'stroke-linecap="round"/>'
             f'<path d="{S.smooth_path(sp, closed=False)}" fill="none" stroke="{P["foam"]}" stroke-width="18" '
             f'stroke-linecap="round"/>')
    r = random.Random(4)
    for k in range(9):
        x = cx - 180 + r.uniform(0, 480)
        y = base - 640 - r.uniform(20, 90)
        foam += (f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(r.uniform(5, 10))}" fill="{P["foam"]}" stroke="{INK}" '
                 f'stroke-width="2.5"/>')
    return doc(body + S.g(foam, filter="wobble-fine"), defs)


def gap_svg(gx, gy):
    """The clear sky behind the cloud lids, seen when they part: a small pale-gold opening with a bright heart,
    kept compact so it reads as a break in the clouds (the lids frame it), not a hazy moon."""
    defs = (S.rad_grad("s8gap", [(0, "#fff7de", 1.0), (0.4, "#fdeab8", 0.95), (0.7, "#f7d995", 0.55),
                                 (0.88, "#f2cc80", 0.18), (1, "#f0c878", 0.0)])
            + S.rad_grad("s8gapw", [(0, "#f6d796", 0.32), (0.6, "#f0c880", 0.12), (1, "#f0c070", 0.0)]))
    return doc(f'<ellipse cx="{gx}" cy="{gy}" rx="520" ry="300" fill="url(#s8gapw)"/>'
               f'<ellipse cx="{gx + 10}" cy="{gy + 4}" rx="300" ry="190" fill="url(#s8gap)"/>', defs)


def lid_glow_svg(cloud, focus, mid):
    """A warm rim of light behind a cloud lit from behind: the same cloud in gold, a little larger, blurred, and
    only on the side facing the light (masked by a radial falloff around ``focus``, the break in layer coords)."""
    fx, fy = focus
    defs = (f'<radialGradient id="{mid}g" gradientUnits="userSpaceOnUse" cx="{fm(fx)}" cy="{fm(fy)}" r="430">'
            '<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.55" stop-color="#fff" '
            'stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{mid}"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#{mid}g)"/></mask>')
    return doc(f'<g mask="url(#{mid})"><g filter="url(#soft)" opacity="0.95">{cloud}</g></g>', defs)


def rays_svg(src, targets, pool):
    """Narrow golden shafts from the cloud break down onto the deck and the crew: each a thin wedge (soft edge,
    blur ~6) with a brighter narrow core, fading in just below the break and out where it lands; plus a faint
    warm pool on the deck."""
    defs = ('<filter id="s8rb" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>'
            '<filter id="s8rc" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5"/>'
            '</filter>')
    sx, sy = src
    shafts, cores = "", ""
    for i, (tx, ty, w) in enumerate(targets):
        L = math.hypot(tx - sx, ty - sy)
        nx, ny = -(ty - sy) / L, (tx - sx) / L         # unit normal
        for kind, ww, col, stops in (
                ("s", w, "#ffe3a0", ((0, 0), (0.1, 0.42), (0.5, 0.28), (0.8, 0.12), (1, 0))),
                ("c", w * 0.3, "#fff4d2", ((0, 0), (0.12, 0.62), (0.5, 0.36), (0.8, 0.12), (1, 0)))):
            gid = f"s8r{kind}{i}"
            defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{fm(sx)}" y1="{fm(sy)}" '
                     f'x2="{fm(tx)}" y2="{fm(ty)}">'
                     + "".join(f'<stop offset="{o}" stop-color="{col}" stop-opacity="{a}"/>' for o, a in stops)
                     + '</linearGradient>')
            w0 = ww * 0.12
            p = [(sx + nx * w0, sy + ny * w0), (tx + nx * ww / 2, ty + ny * ww / 2),
                 (tx - nx * ww / 2, ty - ny * ww / 2), (sx - nx * w0, sy - ny * w0)]
            d = '<path d="M' + " L".join(f"{fm(x)},{fm(y)}" for x, y in p) + f' Z" fill="url(#{gid})"/>'
            if kind == "s":
                shafts += d
            else:
                cores += d
    b = f'<g filter="url(#s8rb)">{shafts}</g><g filter="url(#s8rc)">{cores}</g>'
    px, py, prx, pry = pool
    b += (f'<ellipse cx="{fm(px)}" cy="{fm(py)}" rx="{prx}" ry="{pry}" fill="#ffe2a0" opacity="0.1" '
          f'filter="url(#blur-lg)"/>')
    return doc(b, defs)


def oar_svg(ox, oy, part, wet=0.0):
    """One oar drawn vertically through its oarlock (ox, oy): part 'in' = handle side (up), 'out' = blade side."""
    s = SS
    wl, wood, wd = P["wood_light"], P["wood"], P["wood_dark"]
    sw = 3.6
    if part == "in":
        top = oy - OAR_IN * s
        b = (f'<path d="M{fm(ox)},{fm(oy + 4)} L{fm(ox)},{fm(top + 10 * s)}" stroke="{INK}" '
             f'stroke-width="{fm(15 * s + 2 * sw)}" stroke-linecap="round"/>'
             f'<path d="M{fm(ox)},{fm(oy + 4)} L{fm(ox)},{fm(top + 10 * s)}" stroke="{wl}" stroke-width="{fm(15 * s)}" '
             f'stroke-linecap="round"/>'
             f'<path d="M{fm(ox - 3 * s)},{fm(oy - 10)} L{fm(ox - 3 * s)},{fm(top + 22 * s)}" stroke="{S.shade(wl, 0.35)}" '
             f'stroke-width="{fm(3.5 * s)}" opacity="0.7" stroke-linecap="round"/>'
             # leather sleeve where it rests in the lock
             f'<rect x="{fm(ox - 11 * s)}" y="{fm(oy - 22 * s)}" width="{fm(22 * s)}" height="{fm(26 * s)}" rx="4" '
             f'fill="{S.mix(wd, P["sackcloth_dark"], 0.4)}" stroke="{INK}" stroke-width="{sw}"/>')
        return doc(S.g(graded(b), filter="wobble-fine"), GRADE)
    tip = oy + OAR_OUT * s
    bt = tip - BLADE_L * s
    bw = 17 * s
    blade = (f"M{fm(ox - 7 * s)},{fm(bt - 20 * s)} C{fm(ox - bw)},{fm(bt)} {fm(ox - bw)},{fm(bt + 20 * s)} "
             f"{fm(ox - bw)},{fm(tip - 14 * s)} Q{fm(ox - bw)},{fm(tip)} {fm(ox)},{fm(tip)} "
             f"Q{fm(ox + bw)},{fm(tip)} {fm(ox + bw)},{fm(tip - 14 * s)} C{fm(ox + bw)},{fm(bt + 20 * s)} "
             f"{fm(ox + bw)},{fm(bt)} {fm(ox + 7 * s)},{fm(bt - 20 * s)} Z")
    b = (f'<path d="M{fm(ox)},{fm(oy - 4)} L{fm(ox)},{fm(bt)}" stroke="{INK}" stroke-width="{fm(14 * s + 2 * sw)}" '
         f'stroke-linecap="round"/>'
         f'<path d="M{fm(ox)},{fm(oy - 4)} L{fm(ox)},{fm(bt)}" stroke="{wl}" stroke-width="{fm(14 * s)}" '
         f'stroke-linecap="round"/>'
         f'<path d="{blade}" fill="{S.mix(wood, wd, 0.25)}" stroke="{INK}" stroke-width="{sw}"/>'
         f'<path d="M{fm(ox)},{fm(bt - 10 * s)} L{fm(ox)},{fm(tip - 10 * s)}" stroke="{S.shade(wd, -0.2)}" '
         f'stroke-width="{fm(3 * s)}" opacity="0.6"/>'
         f'<path d="M{fm(ox - 3 * s)},{fm(oy + 8)} L{fm(ox - 3 * s)},{fm(bt - 16 * s)}" stroke="{S.shade(wl, 0.35)}" '
         f'stroke-width="{fm(3.5 * s)}" opacity="0.7" stroke-linecap="round"/>'
         # wet, darker lower blade
         f'<path d="M{fm(ox - bw + 2)},{fm(tip - 44 * s)} L{fm(ox + bw - 2)},{fm(tip - 44 * s)} '
         f'L{fm(ox + bw - 2)},{fm(tip - 12 * s)} Q{fm(ox)},{fm(tip - 2)} {fm(ox - bw + 2)},{fm(tip - 12 * s)} Z" '
         f'fill="{S.shade(wd, -0.15)}" opacity="0.45"/>')
    return doc(S.g(graded(b), filter="wobble-fine"), GRADE)


def splash_svg(x, y, seed):
    return doc(S.g(V.burst(x, y, 0.32, seed=seed, n=5, spread=55, height=120, lean=18), filter="wobble-fine"))


def crew_doc(markup):
    """A figure on its own stage-sized layer, in the cool storm light."""
    return doc(graded(markup), GRADE)


# ---------------------------------------------------------------- motion helpers

def track(entries):
    """[(t, index), ...] -> frame_at with hard cuts (never a crossfade between two drawings)."""
    entries = sorted(entries)
    ts = [e[0] for e in entries]

    def fa(t):
        k = bisect.bisect_right(ts, t) - 1
        return float(entries[max(0, k)][1])
    return fa


def hop_tf(t, events, pivot):
    """Additive squash / hop bumps: events [(t0, kind, s)]; kind 'dip' (crouch -> swap at the bottom -> spring),
    'hop' (a small jump), 'flinch' (jolt back). Returns Tf about the pivot."""
    dx = dy = 0.0
    sy = 1.0
    for t0, kind, k in events:
        u = t - t0
        if kind == "dip":
            if -0.14 <= u <= 0.3:
                if u < 0:
                    a = M.progress(u, -0.14, 0, "in")
                    dy += 8 * k * a
                    sy *= 1 - 0.05 * a
                else:
                    a = 1 - M.progress(u, 0, 0.3, "out")
                    dy += (8 * a - 10 * math.sin(math.pi * min(1, u / 0.3)) * 0.4) * k
                    sy *= 1 - 0.05 * a + 0.02 * math.sin(math.pi * min(1, u / 0.3))
        elif kind == "hop":
            if -0.1 <= u <= 0.36:
                if u < 0:
                    a = M.progress(u, -0.1, 0, "in")
                    sy *= 1 - 0.05 * a
                    dy += 4 * k * a
                else:
                    dy -= 22 * k * math.sin(math.pi * min(1, u / 0.36))
                    sy *= 1 + 0.03 * math.sin(math.pi * min(1, u / 0.18)) * (u < 0.18)
        elif kind == "flinch":
            if 0 <= u <= 0.6:
                a = math.sin(math.pi * min(1, u / 0.6)) * math.exp(-u * 2)
                dx -= 14 * k * a
                dy -= 10 * k * a
    return Tf(dx, dy, 0, 1.0 + (1 - sy) * 0.5, sy, 1.0, pivot[0], pivot[1])


# ---------------------------------------------------------------- build

def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L = ctx.lines
    l0, l1, l2, l3 = L[0], L[1], L[2], L[3]
    l4 = L[4] if len(L) > 4 else None

    # --------------------------------------------------- key times (from the narration)
    t_no = safe_at(l0, ["不忍心"], l0.start)                         # 'no, we won't throw him in'
    t_row = safe_at(l0, ["他们拼命划桨", "拼命划桨"], l0.start + 0.45 * (l0.end - l0.start))
    t_shore = safe_at(l0, ["想让船回到岸边", "回到岸边"], t_row + 1.6)
    t_wave = safe_at(l1, ["海浪越翻越高", "海浪"], l1.start)
    t_hard = safe_at(l1, ["他们怎么用力划桨", "怎么用力"], l1.start + 0.33 * (l1.end - l1.start))
    t_fail = safe_at(l1, ["都没有办法", "没有办法"], l1.start + 0.6 * (l1.end - l1.start))
    t_pray = l2.start
    t_lord = l3.start                                                 # '耶和华啊'
    t_plead = safe_at(l3, ["求你不要", "惩罚我们"], l3.start + 0.35 * (l3.end - l3.start))
    t_blame = safe_at(l3, ["也不要怪我们", "害了他"], l3.start + 0.75 * (l3.end - l3.start))
    t_all = l4.start if l4 else l3.end + 0.6                          # '因为这一切'
    T_GRAB = t_row + 0.04
    T_HIT = t_fail + 0.12           # the huge wave slams into the bow
    T_LOSE = T_HIT + 0.38           # the sailors lose the oars
    T_SHOVE1 = T_HIT + 1.7

    oar_cues, catches = plan_oars(ctx.id, T_GRAB, t_hard - 0.75, T_LOSE)   # frantic as the wave rises
    catches = [c for c in catches if T_GRAB + 0.25 < c < T_LOSE - 0.15]
    # the drive (blade in the water) lasts like the sound's pull: ~0.63 s (compressed for fast strokes)
    periods = [b - a for a, b in zip(catches, catches[1:])]
    periods.append(periods[-1] if periods else CYCLE_STEADY)

    def drive_len(k):
        per = periods[min(k, len(periods) - 1)]
        return 0.63 * min(1.0, per / 1.4)

    def psi_at(t):
        """Continuous stroke position: 0 at each catch, 0.5 at the end of the pull."""
        if not catches or t < T_GRAB:
            return 0.62
        k = bisect.bisect_right(catches, t) - 1
        if k < 0:      # reaching forward for the first catch
            return 0.62 + 0.38 * M.progress(t, T_GRAB + 0.12, catches[0], "linear")
        c0 = catches[k]
        c1 = catches[k + 1] if k + 1 < len(catches) else c0 + periods[-1]
        dd = drive_len(k)
        if t - c0 < dd:
            return 0.5 * (t - c0) / dd
        return 0.5 + 0.5 * min(1.0, (t - c0 - dd) / max(0.2, c1 - c0 - dd))

    # --------------------------------------------------- the ship's motion
    ship_x = V.keyc([(0, SX0), (T_GRAB + 0.5, SX0), (t_hard, SX0 - 58), (T_HIT - 0.05, SX0 - 44),
                     (T_HIT + 0.25, SX0 - 20), (T_SHOVE1, SX0 + 236), (T, SX0 + 262)],
                    ["linear", "inout", "sine", "in", "out", "sine"])
    pitch_amp = V.keyc([(0, 3.2), (T_GRAB, 4.2), (t_wave, 5.5), (T_HIT - 0.3, 7.0), (T_SHOVE1 + 0.6, 5.0),
                        (t_pray + 1.0, 3.4), (t_lord, 2.8), (T, 2.2)])
    bob_amp = V.keyc([(0, 10), (t_wave, 16), (T_HIT - 0.3, 22), (T_SHOVE1 + 0.6, 16), (t_pray + 1.0, 11), (T, 8)])
    freq = V.keyc([(0, 1 / 3.4), (t_wave, 1 / 2.8), (T_HIT, 1 / 2.4), (T_SHOVE1 + 1, 1 / 3.0), (t_lord, 1 / 3.6),
                   (T, 1 / 3.9)])
    phase = V.integrate(freq, -1.0, T + 1.0)
    sea_amp = V.keyc([(0, 0.55), (t_wave, 0.8), (T_HIT - 0.2, 1.15), (T_SHOVE1 + 0.5, 1.0), (t_pray + 1.5, 0.75),
                      (T, 0.6)])

    def impact(t):
        """Bow rears up (+ rot lifts the bow, which is on the left) and the hull rises when the wave hits."""
        u = t - T_HIT
        if u < -0.05 or u > 3.0:
            return 0.0, 0.0
        up = M.progress(u, -0.05, 0.42, "out") * (1 - M.progress(u, 0.42, 1.5, "inout"))
        rock = -3.5 * math.sin(math.pi * M.progress(u, 1.1, 2.6, "linear")) * (u > 1.1)
        return 10.5 * up + rock, -46 * up

    def ship_tf(t):
        ph = 2 * math.pi * phase(t)
        rot = pitch_amp(t) * math.sin(ph)
        dy = bob_amp(t) * math.sin(ph - 1.3)
        ir, idy = impact(t)
        return Tf(ship_x(t) - SX0 + 0.3 * bob_amp(t) * math.sin(0.5 * ph + 0.4), dy + idy, rot + ir, 1, 1, 1,
                  PIV[0], PIV[1])

    def on_ship(local):
        return lambda t: V.compose(ship_tf(t), local(t))

    def wave_motion(by, sx_, k_ph, k_sw=0.0, lag=0.0, follow=0.0, extra=None):
        def m(t):
            a = sea_amp(t)
            ph = 2 * math.pi * phase(t - lag)
            ex = extra(t) if extra else 0.0
            return Tf(dx=sx_ * a * math.sin(0.5 * ph + k_sw) + follow * (ship_x(t) - SX0),
                      dy=by * a * math.sin(ph + k_ph) + ex)
        return m

    # --------------------------------------------------- sky, cloud gap, clouds, lightning
    sc.add("sky", sky_svg(), wc=0.7, motion=lambda t: Tf())
    GX, GY = 2040.0, 350.0
    gap_open = lambda t: M.progress(t, t_lord - 0.2, t_lord + 2.4, "inout")          # noqa: E731
    sc.add("gap", gap_svg(GX, GY), wc=0, motion=lambda t: Tf(alpha=gap_open(t) * (0.9 + 0.1 * math.sin(t * 1.3))))

    cl, cr = P["storm_cloud"], S.mix(P["storm_cloud"], P["storm_cloud_light"], 0.3)
    under, rim = S.mix(P["storm_sky_top"], INK, 0.25), "#9aa6ba"
    CL = ((180, 170, 760, 270), (720, 110, 780, 240), (430, 390, 820, 230), (1080, 300, 640, 200))
    CR = ((2520, 150, 760, 270), (2560, 560, 700, 200))
    left = "".join(V.storm_cloud(x, y, w_, h_, 40 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CL))
    right = "".join(V.storm_cloud(x, y, w_, h_, 60 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CR))
    # (each bank touches one canvas side: it only ever drifts away from that side, so its cut edge never shows)
    sc.add("clouds_left", doc(S.g(left, filter="wobble")), wc=0.9,
           motion=M.combine(M.drift(vx=-5), M.bob(6, 5.0),
                            lambda t: Tf(dx=-40 * M.progress(t, t_wave, T_HIT, "inout"))))
    sc.add("clouds_right", doc(S.g(right, filter="wobble")), wc=0.9,
           motion=M.combine(M.drift(vx=4), M.bob(7, 4.4, 0.3)))
    # the two lids over the gap: they part on '耶和华啊'; as they part their edges catch the light (a warm rim
    # glows behind each lid and its own colours warm up - a colour change of the same drawing, not a new pose)
    cl_w, cr_w = S.mix(cl, "#c8b08a", 0.3), S.mix(cr, "#d2bc94", 0.3)
    under_w, rim_w, gold = S.mix(under, "#7a6656", 0.35), "#ffe2a0", "#ffd98c"
    LIDS = (("lid_left", (GX - 210, GY + 10, 620, 230, 81), cr, cr_w, (210, 20),
             M.combine(M.bob(5, 4.8, 0.2), lambda t: Tf(dx=-210 * gap_open(t), dy=-20 * gap_open(t)))),
            ("lid_right", (GX + 230, GY - 20, 640, 240, 82), cl, cl_w, (-220, 30),
             M.combine(M.bob(6, 5.3, 0.6), lambda t: Tf(dx=220 * gap_open(t), dy=-30 * gap_open(t)))))
    for name, (x_, y_, w_, h_, seed), fill, fill_w, (ox_, oy_), m in LIDS:
        glow = V.storm_cloud(x_, y_, w_, h_, seed, gold, gold, gold, sw=0)
        sc.add(f"{name}_glow", lid_glow_svg(f'<g transform="translate({x_},{y_}) scale(1.07) translate({-x_},{-y_})">'
                                            f'{glow}</g>', (GX + 10 + ox_, GY + oy_), f"m{name}"), wc=0,
               motion=(lambda m_: lambda t: replace(m_(t), alpha=0.9 * gap_open(t)))(m))
        cool = doc(S.g(V.storm_cloud(x_, y_, w_, h_, seed, fill, under, rim), filter="wobble"))
        warm = doc(S.g(V.storm_cloud(x_, y_, w_, h_, seed, fill_w, under_w, rim_w), filter="wobble"))
        sc.add(name, [cool, warm], wc=0.9, motion=m, frame_at=lambda t: gap_open(t))
    lid_c = V.storm_cloud(GX + 10, GY + 40, 460, 190, 83, cl, under, rim)
    # the light shining through right at the break (screen: it lifts the lids' inner edges softly)
    glow_defs = S.rad_grad("s8gt", [(0, "#ffe7b0", 0.45), (0.45, "#f8d898", 0.2), (1, "#f0c880", 0.0)])
    sc.add("gap_through", doc(f'<ellipse cx="{GX + 10}" cy="{GY}" rx="360" ry="220" fill="url(#s8gt)"/>', glow_defs),
           wc=0, blend="screen",
           motion=lambda t: Tf(alpha=M.progress(t, t_lord + 0.1, t_lord + 2.8, "sine") * (0.9 + 0.1 * math.sin(t * 1.3))))
    sc.add("lid_mid", doc(S.g(lid_c, filter="wobble")), wc=0.9,
           motion=M.combine(M.bob(5, 4.1, 0.1), lambda t: Tf(dy=150 * gap_open(t), sx=1 - 0.25 * gap_open(t),
                                                            sy=1 - 0.25 * gap_open(t), alpha=1 - gap_open(t),
                                                            px=GX, py=GY + 40)))

    STRIKES = [(t_wave + 0.3, 0.34, (520, 330, 720)), (T_HIT - 0.06, 0.42, (1980, 300, 660))]
    for i, (ts, _, (bx, by0, by1)) in enumerate(STRIKES):
        sc.add(f"bolt{i}", doc(V.bolt_svg(bx, by0, by1, seed=17 + i, sway=-1 if i else 1, w0=30), V.BOLT_DEFS), wc=0,
               motion=(lambda ts_: lambda t: Tf(alpha=V.bolt_alpha(t - ts_)))(ts))

    # --------------------------------------------------- the shore (grows a little while they row, then recedes)
    def coast_m(t):
        near = 0.08 * M.progress(t, T_GRAB + 0.5, t_hard, "inout")
        far = M.progress(t, T_HIT + 0.1, T_SHOVE1 + 0.9, "inout")
        k = (1 + near) * (1 - 0.4 * far)
        return Tf(dx=-150 * far + 20 * near / 0.08, dy=0, sx=k, sy=k, alpha=1 - 0.3 * far, px=480, py=HORIZON)
    sc.add("coast", coast_svg(), wc=0.8, motion=coast_m)
    sc.add("far_sea", far_sea_svg(), wc=0.7, motion=lambda t: Tf())

    # --------------------------------------------------- the huge wave
    # Drawn at its impact place (wholly inside the canvas) and moved LEFT of it while it rises, so no cut edge can
    # ever show. The motion is planned by where the curl's lip should be: it rises between the ship and the shore
    # with the lip >= ~200 px ahead of the bow post (and clear of the sail's loose flap), and only in the last
    # 0.4 s before T_HIT does it rush in and pitch forward onto the bow; then it collapses into the sea fast.
    BW_X, BW_B = 590.0, 1110.0
    bow_knob = V.apply(ship_tf(T_HIT), *ship_pt(488, -358))
    LIP_EARLY, LIP_PRE, LIP_HIT = 470.0, 640.0, bow_knob[0] + 14.0

    def bigwave_m(t):
        rise = M.progress(t, t_wave - 0.5, t_hard + 0.4, "sine")
        grow2 = M.progress(t, t_hard, T_HIT - 0.45, "inout")
        slam = M.progress(t, T_HIT - 0.4, T_HIT, "in")
        follow = M.progress(t, T_HIT, T_HIT + 0.6, "out")
        sink = M.progress(t, T_HIT + 0.05, T_HIT + 1.15, "inout")
        sy = 0.38 + 0.54 * rise + 0.38 * grow2
        sx = 0.9 + 0.1 * rise + 0.12 * grow2
        rot = 3 * grow2 + 6 * slam + 3 * follow
        lip = (LIP_EARLY + (LIP_PRE - LIP_EARLY) * (0.5 * rise + 0.5 * grow2) + (LIP_HIT - LIP_PRE) * slam
               + 60 * follow)
        x0, _ = V.apply(Tf(0, 0, rot, sx, sy, 1, BW_X, BW_B), BW_X + WAVE_LIP[0], BW_B + WAVE_LIP[1])
        dy = 250 * (1 - rise) + 100 * slam + 950 * sink + 14 * math.sin(2 * math.pi * t / 3.1)
        alpha = 1 - M.progress(t, T_HIT + 0.75, T_HIT + 1.1, "linear")
        return Tf(lip - x0, dy, rot, sx, sy, alpha, BW_X, BW_B)
    sc.add("big_wave", big_wave_svg(BW_X, BW_B), wc=1.0, motion=bigwave_m)

    # --------------------------------------------------- sea behind the ship
    f_mid = V.wave_fn(SY - 62, 40, 560, 1.3, p=2.2)
    sc.add("sea_mid", doc(sea_layer(f_mid, S.mix(P["storm_sea_light"], P["storm_sea"], 0.3), P["sea_light"],
                                    P["storm_sea"], 560, 40, 2, foam_size=0.8)),
           wc=1.0, motion=wave_motion(14, 30, -0.4, 0.5, lag=0.25))

    # --------------------------------------------------- ship (back)
    deck_mid = deck_y(0)
    sc.add("ship_back", doc(graded(PR.ship(SX0, SY, SS, SF, sail="torn", part="back", flag=False)
                                   + PR.rope_coil(*ship_pt(-60, hull_top(-60)), SS * 0.85)), GRADE),
           motion=ship_tf)
    z_ship_back = sc.layers[-1].z
    flags = []
    for ph in (0.0, 1.6, 3.2):
        pts = [ship_pt(*q) for q in V.pennant_pts(ph)]
        flags.append(doc(graded(S.g(S.path(S.smooth_path(pts, closed=True, tension=0.6), fill=P["sail_stripe"],
                                           sw=3.5), filter="wobble-fine")), GRADE))
    sc.add("pennant", flags, motion=ship_tf, frame_at=lambda t: float(int(t * 6) % 3))

    # --------------------------------------------------- crew: times of every pose change
    T_KNEEL = {"A": t_pray + 0.35, "B": t_pray + 0.55, "C": t_pray + 0.45, "D": t_pray + 0.7, "capt": t_pray + 0.9}
    T_UP = {"A": t_lord + 0.15, "B": t_lord + 0.3, "C": t_lord + 0.22, "D": t_lord + 0.4, "capt": t_lord + 0.5}
    T_PRESS = {"A": t_plead + 0.05, "B": t_plead + 0.2, "C": t_plead + 0.12, "D": t_plead + 0.28,
               "capt": t_plead + 0.35}
    T_BOW = {"A": t_blame + 0.05, "B": t_blame + 0.18, "C": t_blame + 0.1, "D": t_blame + 0.25, "capt": t_blame + 0.3}
    T_UP2 = {"A": t_all + 0.1, "B": t_all + 0.26, "C": t_all + 0.18, "D": t_all + 0.34, "capt": t_all + 0.42}
    T_REFUSE = {"B": t_no + 0.35, "C": t_no + 0.75}
    T_SCARED = {"A": T_LOSE, "B": T_LOSE + 0.06, "C": T_LOSE + 0.03, "D": T_LOSE + 0.1}
    t_fast_set = next((c for c in catches if c >= t_hard - 0.05), T_LOSE)   # tired faces from this catch on

    z_crew = len(sc.layers) + 1.0
    z_crew0 = z_crew
    # kneeling drawings: hands pressed (looking up) -> arms raised -> pressed -> heads bowed -> arms raised, eyes shut
    KNEEL_SEQ = ((KNEEL_PRESS, "worried"), (KNEEL_UP, "worried"), (KNEEL_PRESS, "worried"), (KNEEL_BOW, "sorry"),
                 (KNEEL_UP, END_EXPR))
    kneel_layers = []          # added later, between Jonah and the ship's front (rail, shields, lantern)
    oar_specs = []

    for name, variant, lx in ROWERS:
        X, Yd = stage_x(lx), deck_y(lx)
        olx = lx - OAR_DX
        O = (stage_x(olx), rail_y(olx))
        rel_o = ((O[0] - X) / SS, (O[1] - Yd) / SS)
        toward_jonah = 1 if lx > JON_LX else -1
        expr1, expr2 = "worried", "tired"
        frames, hands = [], []
        # 0 standing (looking at Jonah), 1 refusing (B, C) / same, 2..9 rowing, 10..17 rowing (tired), 18 scared
        frames.append(crew_doc(person("sailor", X, Yd, toward_jonah, STAND, "sad", variant)))
        hands.append(None)
        frames.append(crew_doc(person("sailor", X, Yd, toward_jonah, REFUSE if name in T_REFUSE else STAND,
                                      "sad" if name in T_REFUSE else "worried", variant, fallback="stand")))
        hands.append(None)
        for e in (expr1, expr2):
            for j in range(N_ROW):
                ps = row_pose(j / N_ROW, rel_o, e, FIN_LEAN.get(name, 1.0))
                frames.append(crew_doc(person("sailor", X, Yd, 1, ps, e, variant, fallback="pull")))
                bp = person_points("sailor", X, Yd, 1, ps, e, variant)
                hands.append(bp["hands"][1] if bp else (X + 60 * SS, Yd - 155 * SS))
        frames.append(crew_doc(person("sailor", X, Yd, 1, SCARED, "scared", variant, fallback="scared")))
        hands.append(None)
        sched = [(0, 0)]
        if name in T_REFUSE:
            sched.append((T_REFUSE[name], 1))
        t_sc = T_SCARED[name]

        def frame_idx(t, sched=sched, t_sc=t_sc):
            if t < T_GRAB:
                return track(sched)(t)
            if t >= t_sc:
                return 18.0
            j = int(round(psi_at(t) * N_ROW)) % N_ROW
            return float(2 + j + (N_ROW if t >= t_fast_set else 0))

        hop_ev = [(T_GRAB, "hop", 1.0), (t_sc, "flinch", 1.0), (T_KNEEL[name], "dip", 0.8)]
        if name in T_REFUSE:
            hop_ev.append((T_REFUSE[name], "dip", 0.6))
        F = (X, Yd)

        def rower_tf(t, F=F, hands=hands, frame_idx=frame_idx, hop_ev=hop_ev, t_sc=t_sc, name=name):
            """Body motion about the feet: on the oar the rower rocks so the drawn hand meets the continuous stroke
            path (between drawings); a hop on grabbing the oar, a flinch when the wave hits; before / after rowing
            a gentle sway. Alpha 0 once he kneels (the kneeling drawing takes over)."""
            idx = int(frame_idx(t))
            rot = 0.0
            if 2 <= idx < 18:
                hk = hands[idx]
                # the hand follows the path through the DRAWN hands of neighbouring drawings, so the lean that
                # glues it there between drawings stays small
                q = (psi_at(t) % 1.0) * N_ROW
                j0 = int(q) % N_ROW
                fq = q - int(q)
                base = 2 if idx < 2 + N_ROW else 2 + N_ROW
                h0, h1 = hands[base + j0], hands[base + (j0 + 1) % N_ROW]
                want = (h0[0] + (h1[0] - h0[0]) * fq, h0[1] + (h1[1] - h0[1]) * fq)
                rot = math.degrees(math.atan2(want[1] - F[1], want[0] - F[0])
                                   - math.atan2(hk[1] - F[1], hk[0] - F[0]))
            else:
                rot = 1.2 * math.sin(2 * math.pi * t / 3.3 + len(name))
                if idx == 18:
                    rot += 2.0 * math.sin(t * 31 + len(name)) * (1 - M.progress(t, t_sc, t_sc + 1.4))
            h = hop_tf(t, hop_ev, F)
            a = 0.0 if t >= T_KNEEL[name] else 1.0
            return Tf(h.dx, h.dy, rot, h.sx, h.sy, a, F[0], F[1])

        sc.add(f"rower_{name}", frames, z=z_crew, motion=on_ship(rower_tf), frame_at=frame_idx)
        z_crew += 0.01
        oar_specs.append(dict(name=name, F=F, O=O, hands=hands, frame_idx=frame_idx, rower_tf=rower_tf, lx=lx,
                              variant=variant, t_sc=t_sc))

        # kneeling drawings (behind the rail like everyone on deck: the oars are gone by then)
        kx = X + (26 if lx > 0 else -26) * SS
        kf = 1 if lx > 0 else -1
        kyd = deck_y(lx + (-26 if lx > 0 else 26))
        kd = [crew_doc(person("sailor", kx, kyd, kf, ps, e, variant, fallback="pray")) for ps, e in KNEEL_SEQ]
        kneel_layers.append((name, kd, (kx, kyd)))

    # Jonah by the mast: hand on chest (as s07 ends) -> watches, worried -> the wave (surprised) -> sorry among the
    # kneeling crew
    JX, JY = stage_x(JON_LX), deck_y(JON_LX)
    jon_frames = [crew_doc(person("jonah", JX, JY, -1, dict(POSE["confess"]), "sorry", fallback="confess")),
                  crew_doc(person("jonah", JX, JY, -1, STAND, "worried")),
                  crew_doc(person("jonah", JX, JY, -1, dict(POSE["stand"], h=-10), "surprised")),
                  crew_doc(person("jonah", JX, JY, -1, dict(POSE["confess"]), "sorry", fallback="confess"))]
    j_sched = [(0, 0), (T_GRAB + 0.3, 1), (t_wave + 0.15, 2), (t_pray + 0.15, 3)]
    j_hops = [(T_GRAB + 0.3, "dip", 0.5), (t_wave + 0.15, "hop", 0.4), (T_HIT + 0.02, "flinch", 0.8),
              (t_pray + 0.15, "dip", 0.5)]
    # (between B and C: C, leaning back at the finish, passes in front of Jonah's head-cloth flap, not behind it)
    sc.add("jonah", jon_frames, z=z_crew0 + 0.015, frame_at=track(j_sched),
           motion=on_ship(lambda t: V.compose(hop_tf(t, j_hops, (JX, JY)),
                                              Tf(0, 0, 0.8 * math.sin(2 * math.pi * t / 3.6), 1,
                                                 1 + 0.008 * math.sin(2 * math.pi * t / 3.6 + 1), 1, JX, JY))))
    z_crew += 0.01

    # the captain on the stern deck: sad -> points at the shore -> hands on his head -> kneels
    CX, CY = stage_x(CAPT_LX), deck_y(CAPT_LX)
    cap_frames = [crew_doc(person("captain", CX, CY, -1, STAND, "sad")),
                  crew_doc(person("captain", CX, CY, -1, POINT_UP, "worried", fallback="point")),
                  crew_doc(person("captain", CX, CY, -1, WORRIED, "worried", fallback="worried")),
                  crew_doc(person("captain", CX, CY, -1, WORRIED, "scared", fallback="worried"))]
    c_sched = [(0, 0), (T_GRAB + 0.12, 1), (t_wave + 0.3, 2), (T_HIT + 0.05, 3)]
    c_hops = [(T_GRAB + 0.12, "hop", 0.6), (t_wave + 0.3, "dip", 0.6), (T_HIT + 0.05, "flinch", 1.0)]
    c_hops.append((T_KNEEL["capt"], "dip", 0.8))

    def capt_m(t):
        h = hop_tf(t, c_hops, (CX, CY))
        return Tf(h.dx, h.dy, 0.9 * math.sin(2 * math.pi * t / 3.9 + 2), h.sx, h.sy,
                  0.0 if t >= T_KNEEL["capt"] else 1.0, CX, CY)
    sc.add("captain", cap_frames, z=z_crew - 0.5, frame_at=track(c_sched), motion=on_ship(capt_m))
    # (he kneels a little toward the mast, so the stern lantern hangs behind his back, not over his face)
    ckx, cky = stage_x(CAPT_KNEEL_LX), deck_y(CAPT_KNEEL_LX)
    ckd = [crew_doc(person("captain", ckx, cky, -1, ps, e, fallback="stand")) for ps, e in KNEEL_SEQ]
    kneel_layers.append(("capt", ckd, (ckx, cky)))

    # --------------------------------------------------- ship (front): rail, shields, steering oar, oarlocks, lantern
    locks = ""
    for spec in oar_specs:
        ox, oy = spec["O"]
        locks += (f'<rect x="{fm(ox - 5 * SS)}" y="{fm(oy - 26 * SS)}" width="{fm(10 * SS)}" height="{fm(30 * SS)}" '
                  f'rx="3" fill="{P["wood_dark"]}" stroke="{INK}" stroke-width="3"/>')
    lan = PR.lantern(*ship_pt(-428, -372), 0.85 * SS)
    z_front = z_crew + 0.5
    sc.add("ship_front", doc(graded(PR.ship(SX0, SY, SS, SF, sail="torn", part="front", lantern=False)
                                    + S.g(locks, filter="wobble-fine")) + lan, GRADE), z=z_front,
           motion=ship_tf)

    # --------------------------------------------------- the oars
    def out_geom(O, a_deg, depth):
        """Outboard sy (projection of a blade dipped DEPTH_PULL deep at this angle) and the slide along the shaft
        (stage px, + = up toward the handle) that lifts the tip to ``depth``."""
        ca = max(0.35, math.cos(math.radians(a_deg)))
        s_out = (SY + DEPTH_PULL * SS - O[1]) / (OAR_OUT * SS * ca)
        s_out = min(1.18, max(0.7, s_out))
        tip = O[1] + OAR_OUT * SS * s_out * ca
        lift = (tip - (SY + depth * SS)) / ca
        return s_out, lift

    def lose_state(spec, u):
        """After the sailors let go (u s after): the wave wrenches the blade back toward the stern, the oar bounces
        (always clearly slanted, never swinging up through vertical), then it slips out through its lock and drops
        into the sea. Returns (angle, visible inboard length (local px), blade depth, slide (stage px, along the
        shaft toward the blade), alpha)."""
        k = spec["k"]
        a0 = spec.get("a_lose", -30.0)
        rest = -38.0 - 3 * (k % 2)
        a = V.keyc([(0, a0), (0.2, -60 + 3 * k), (0.52, -27 - 2 * k), (0.85, -45), (1.25, rest)], "sine")(u)
        depth = 30.0 - 80 * math.sin(math.pi * min(1.0, u / 0.6)) * math.exp(-u / 1.4)
        inl = 120.0 + 30 * math.exp(-u / 0.6)
        v = max(0.0, u - spec["u_slip"]) / 0.9
        slide = spec["slide_end"] * v * v
        alpha = 0.0 if slide > spec["slide_end"] else 1.0
        return a, inl, depth, slide, alpha

    def oar_state(spec, t):
        """(angle deg, inboard sy, outboard sy, lift along the shaft, slide along the shaft, alpha) of an oar in
        un-moved ship coordinates."""
        O = spec["O"]
        idx = int(spec["frame_idx"](t))
        if t < T_GRAB or (t >= spec["t_sc"]):
            slide, alpha = 0.0, 1.0
            if t < T_GRAB:       # resting in its lock before rowing
                a, depth, inl = -34.0, 30.0, 120.0
            else:
                a, inl, depth, slide, alpha = lose_state(spec, t - spec["t_sc"])
            a += 1.8 * math.sin(2 * math.pi * t / 2.7 + spec["lx"] / 90)
            s_in = inl / OAR_IN
            s_out, lift = out_geom(O, a, depth)
            return a, s_in, s_out, lift, slide, alpha
        hk = spec["hands"][idx] if spec["hands"][idx] else (O[0] - 40, O[1] - 100)
        hx, hy = V.apply(spec["rower_tf"](t), *hk)
        a = math.degrees(math.atan2(hx - O[0], O[1] - hy))
        dist = math.hypot(hx - O[0], hy - O[1])
        s_in = (dist + HANDLE_OVER * SS) / (OAR_IN * SS)
        s_out, lift = out_geom(O, a, blade_depth(psi_at(t)))
        return a, s_in, s_out, lift, 0.0, 1.0

    for k, spec in enumerate(oar_specs):
        spec["k"] = k
        spec["u_slip"] = 0.6 + 0.16 * (0, 2, 1, 3)[k]
        st = oar_state(spec, spec["t_sc"] - 0.01)
        spec["a_lose"] = st[0]
        # slide far enough that the handle end ends up under the sea (near the hull the sea is calm: ~SY + 14)
        ar = math.radians(-38.0)
        spec["slide_end"] = 150 * SS + (SY + 60 - spec["O"][1]) / math.cos(ar)
        # when the handle end passes the waterline: a small splash there
        d_w = 120 * SS + (SY - spec["O"][1]) / math.cos(ar)
        u_w = spec["u_slip"] + 0.9 * math.sqrt(min(1.0, d_w / spec["slide_end"]))
        spec["t_drop"] = spec["t_sc"] + u_w
        spec["drop_x"] = spec["O"][0] + (SY - spec["O"][1]) * math.tan(-ar)

    z_oar = z_crew + 1.0
    for i, spec in enumerate(oar_specs):
        ox, oy = spec["O"]

        def m_in(t, spec=spec, ox=ox, oy=oy):
            a, s_in, _, _, sl, al = oar_state(spec, t)
            ar = math.radians(a)
            return Tf(-sl * math.sin(ar), sl * math.cos(ar), a, 1, s_in, al, ox, oy)

        def m_out(t, spec=spec, ox=ox, oy=oy):
            a, _, s_out, lift, sl, al = oar_state(spec, t)
            ar = math.radians(a)
            return Tf((lift - sl) * math.sin(ar), -(lift - sl) * math.cos(ar), a, 1, s_out, al, ox, oy)
        sc.add(f"oar_out_{spec['name']}", oar_svg(ox, oy, "out"), z=z_oar + 0.01 * i, motion=on_ship(m_out), wc=0.6)
        sc.add(f"oar_in_{spec['name']}", oar_svg(ox, oy, "in"), z=z_oar + 0.05 + 0.01 * i, motion=on_ship(m_in),
               wc=0.6)
        # the near fist over the handle
        fr = []
        for k in range(len(spec["hands"])):
            hp = spec["hands"][k]
            if hp is None:
                fr.append(doc(""))
            else:
                r_ = C._ADULT["hr"] * SS
                skin = C._SAILORS[spec["variant"]]["skin"] if hasattr(C, "_SAILORS") else P["skin"]
                fr.append(doc(S.g(graded(f'<circle cx="{fm(hp[0])}" cy="{fm(hp[1])}" r="{fm(r_)}" fill="{skin}" '
                                         f'stroke="{INK}" stroke-width="{fm(3.2 * SS)}"/>'), filter="wobble-fine"),
                              GRADE))
        sc.add(f"fist_{spec['name']}", fr, z=z_oar + 0.1 + 0.01 * i, motion=on_ship(spec["rower_tf"]),
               frame_at=spec["frame_idx"])

    # kneeling crew: in front of Jonah, behind the rail, the shields and the stern lantern
    z_k = z_front - 0.3
    for name, kd, (kx, kyd) in kneel_layers:
        tk = T_KNEEL[name]
        kn_sched = [(0, 0), (T_UP[name], 1), (T_PRESS[name], 2), (T_BOW[name], 3), (T_UP2[name], 4)]
        ev = [(tk, "dip", 0.8)] + [(T_UP[name], "hop", 0.25), (T_PRESS[name], "dip", 0.4), (T_BOW[name], "dip", 0.3),
                                   (T_UP2[name], "hop", 0.25)]

        def kn_m(t, tk=tk, ev=ev, kx=kx, kyd=kyd, name=name):
            h = hop_tf(t, ev, (kx, kyd))
            br = 1 + 0.01 * math.sin(2 * math.pi * t / 3.2 + len(name))
            return Tf(h.dx, h.dy, 0.6 * math.sin(2 * math.pi * t / 4.1 + len(name)), h.sx, h.sy * br,
                      1.0 if t >= tk else 0.0, kx, kyd)
        sc.add(f"kneel_{name}", kd, z=z_k, motion=on_ship(kn_m), frame_at=track(kn_sched))
        z_k += 0.01
    z_kn = z_oar + 0.5         # (the sea in front of the ship and the effects stack above this)

    # --------------------------------------------------- sea in front of the ship
    def gx(x):     # calm pocket around the ship (between its start and end positions)
        return min(1.0, abs(x - (SX0 + 140)) / 1000) ** 1.4
    f_near = V.wave_fn(lambda x: SY + 14 - 70 * gx(x), lambda x: 16 + 95 * gx(x), 600, 0.75, p=2.0, lean=0.3)
    surge_up = lambda t: -60 * math.sin(math.pi * M.progress(t, T_HIT - 0.1, T_HIT + 1.4, "linear"))  # noqa: E731
    near_m = wave_motion(18, 40, 0.3, 2.0, lag=0.1, extra=surge_up)
    sc.add("sea_near", doc(sea_layer(f_near, P["storm_sea"], P["storm_sea_light"], S.shade(P["storm_sea"], -0.3),
                                     600, 70, 3, foam_size=1.0, cap_amp=lambda x: 16 + 95 * gx(x))),
           z=z_kn + 1, wc=1.0, motion=near_m)

    # splashes where the blades bite (one per oar, re-triggered at every catch)
    z_sp = z_kn + 1.5
    for i, spec in enumerate(oar_specs):
        ox, oy = spec["O"]
        hx, hy, _ = row_curve(0.0)
        # blade tip at the catch (un-moved ship)
        F = spec["F"]
        hpos = (F[0] + hx * SS, F[1] + hy * SS)
        a = math.atan2(hpos[0] - ox, oy - hpos[1])
        tip_y = SY + DEPTH_PULL * SS
        tip_x = ox - (tip_y - oy) * math.tan(a)
        sx_, sy_ = tip_x, SY - 6

        def sp_m(t, sx_=sx_, sy_=sy_, spec=spec):
            u_d = t - spec["t_drop"]
            if 0 <= u_d <= 0.75:        # the lost oar drops into the sea
                u, dx = u_d, spec["drop_x"] - sx_
            else:
                if not catches or t < catches[0] - 0.05 or t >= spec["t_sc"] + 0.6:
                    return Tf(alpha=0.0, px=sx_, py=sy_)
                k = bisect.bisect_right(catches, t + 0.02) - 1
                u, dx = t - catches[k] + 0.02, 0.0
                if u > 0.75:
                    return Tf(alpha=0.0, px=sx_, py=sy_)
            grow = M.progress(u, 0, 0.16, "out")
            a_ = (1 - M.progress(u, 0.35, 0.75, "sine"))
            inner = Tf(dx, 0, 0, 0.6 + 0.5 * grow, 0.2 + 0.8 * grow - 0.3 * M.progress(u, 0.4, 0.75), a_ * 0.95,
                       sx_, sy_ + 10)
            return V.compose(ship_tf(t), inner)
        sc.add(f"oar_splash_{spec['name']}", splash_svg(sx_, sy_, 300 + i), z=z_sp + 0.01 * i, wc=0.5, motion=sp_m)

    # the wave's crash over the bow: it bursts up, then collapses down onto its foamy base and sinks into the
    # waves (never fading as a translucent ghost over the hull)
    bow_hit = V.apply(ship_tf(T_HIT), *ship_pt(470, -80))
    bx, by = bow_hit
    # (it fans up and a little back over the bow, its tongues ending below the faces of the nearest rowers)
    sc.add("bow_crash", doc(V.burst(bx - 60, by + 40, 2.0, seed=12, n=7, spread=44, height=170, lean=-4)), wc=0.5,
           z=z_kn + 0.9,
           motion=M.keys([(T_HIT - 0.01, {"sy": 0.15, "sx": 0.6, "alpha": 0}), (T_HIT, {"alpha": 1}),
                          (T_HIT + 0.3, {"sy": 1.0, "sx": 1.0, "dx": 20}),
                          (T_HIT + 0.8, {"sy": 0.95, "sx": 1.08, "dx": 60}),
                          (T_HIT + 1.3, {"sy": 0.3, "sx": 1.12, "dx": 85, "dy": 70}),
                          (T_HIT + 1.55, {"sy": 0.1, "sx": 1.12, "dx": 95, "dy": 130, "alpha": 0})],
                         ["linear", "out", "sine", "in", "in"], pivot=(bx - 60, by + 50)))

    f_fg = V.wave_fn(VIEW_BOTTOM - 60, 34, 540, 0.7, p=1.8, lean=0.3)
    sc.add("sea_fg", doc(sea_layer(f_fg, S.shade(P["storm_sea"], -0.18), P["storm_sea_light"],
                                   S.shade(P["storm_sea"], -0.45), 540, 34, 4, foam_size=0.8)),
           z=z_sp + 1, wc=1.0, motion=wave_motion(12, 30, 1.6, 3.0, lag=-0.15, extra=lambda t: 1.2 * surge_up(t)))

    # golden shafts from the break, landing on the deck among the kneeling crew (end place of the ship)
    ray_a = lambda t: M.progress(t, t_lord + 0.4, t_lord + 2.8, "inout") * (0.9 + 0.1 * math.sin(t * 1.1))  # noqa
    # Each shaft passes BETWEEN two kneeling heads (at head height, end place of the ship) and fades out on the
    # deck, so it lights the crew without washing out a face.
    ex = SX0 + 262 - SX0            # the ship's end offset
    ray_src = (GX + 10, GY + 60)
    head_y = deck_y(0) - 225
    ray_targets = []
    for lx_a, lx_b, w in ((274, 132, 78), (132, -4, 74), (-4, -116, 76), (-116, -250, 70)):   # kneeling places
        gx_ = (stage_x(lx_a) + stage_x(lx_b)) / 2 + ex           # the gap between the two heads
        k = (deck_y(0) - 10 - ray_src[1]) / (head_y - ray_src[1])
        ray_targets.append((ray_src[0] + (gx_ - ray_src[0]) * k, deck_y(0) - 10, w))
    sc.add("rays", rays_svg(ray_src, ray_targets, (SX0 + 262, deck_mid - 60, 380, 120)),
           z=z_sp + 2, wc=0, blend="screen",
           motion=lambda t: Tf(alpha=ray_a(t)))

    # gusts while the wave rises: in the open sky right of / above the sail, and behind the ship (never across
    # the sail, where they would read as rips)
    gusts = [(t_wave - 0.1, 2150, 300, 520), (t_wave + 0.6, 2060, 610, 460), (t_hard + 0.2, 2250, 440, 460),
             (t_fail - 0.3, 1960, 205, 520)]
    for i, (tg, gx_, gy_, gl) in enumerate(gusts):
        sc.add(f"gust{i}", doc(S.g(V.wind_svg(gx_, gy_, gl, seed=30 + i), filter="wobble-fine")), wc=0,
               z=z_ship_back - 0.3 + 0.01 * i,
               motion=(lambda tg_: M.combine(
                   M.keys([(tg_, {"dx": 260, "alpha": 0}), (tg_ + 0.25, {"alpha": 0.9}), (tg_ + 0.95, {"alpha": 0.9}),
                           (tg_ + 1.3, {"dx": -380, "alpha": 0})], "linear"),
                   lambda t: Tf(dy=10 * math.sin(4 * t))))(tg))

    # --------------------------------------------------- camera
    sx_end = SX0 + 262
    cam_base = M.cam_keys([
        (0.0, Cam(1430, 760, 1700)), (T_GRAB - 0.6, Cam(1420, 760, 1690)),
        (t_shore + 1.2, Cam(1250, 740, 2300)), (t_wave, Cam(1240, 735, 2340)),
        (t_fail - 0.2, Cam(1260, 715, 2420)), (T_SHOVE1 + 0.2, Cam(1420, 720, 2400)),
        (T_SHOVE1 + 0.9, Cam(1440, 720, 2380)), (t_lord - 0.4, Cam(sx_end + 40, 700, 1700)),
        (t_lord + 2.6, Cam(sx_end + 70, 660, 1680)), (T, Cam(sx_end + 60, 670, 1600))],
        ["sine", "sine", "sine", "inout", "inout", "sine", "inout", "inout", "sine"])
    cam = M.cam_shake(cam_base, amp=14, t0=T_HIT - 0.05, t1=T_HIT + 1.3, freq=7.5, seed=3)
    cam = M.cam_shake(cam, amp=5, t0=STRIKES[0][0], t1=STRIKES[0][0] + 0.6, freq=9, seed=5)

    def camera(t):
        """Keyed camera, clamped inside the painting with margins (layers that sway sideways / bob never show
        their cut edges)."""
        c = cam(t)
        w = min(c.w, W - 100, (VIEW_BOTTOM - 24) * 16 / 9)
        hw, hh = w / 2, w * 9 / 32
        return Cam(min(max(c.x, hw + 48), W - hw - 48), min(max(c.y, hh + 14), VIEW_BOTTOM - hh - 8), w, 0.0)
    sc.camera = camera

    # --------------------------------------------------- effects
    sc.fx = [V.rain_fx(0.0, t_lord + 1.5, density=0.85, angle=-16),
             V.rain_fx(t_lord + 0.3, T + 1.0, density=0.45, angle=-12, alpha=60, seed=9),
             V.flash_fx([(ts, st) for ts, st, _ in STRIKES]),
             FX.sparkles((GX - 560, GY + 160, GX + 120, deck_mid - 140), count=14, t0=t_lord + 1.2, t1=T + 2,
                         period=2.2, drift=-6, seed=21)]
    sc.meta = dict(catches=catches, oar_cues=oar_cues, T_HIT=T_HIT, T_LOSE=T_LOSE, t_fast_set=t_fast_set)

    # --------------------------------------------------- sound
    sc.sfx("storm_wind", 0, dur=T + 0.6, gain_db=-11, fade_in=0.8, fade_out=1.0)
    sc.sfx("waves_storm", 0, dur=T + 0.6, gain_db=-11, fade_in=0.8, fade_out=1.0)
    sc.sfx("rain", 0, dur=t_lord + 1.5, gain_db=-12, fade_in=0.8, fade_out=1.5)
    sc.sfx("rain", t_lord + 0.3, dur=T + 0.3 - t_lord, gain_db=-17, fade_in=1.2, fade_out=1.0)
    sc.sfx("ship_creak", 0, dur=T + 0.6, gain_db=-13, fade_in=0.8, fade_out=0.8)
    sc.sfx("ship_creak", T_HIT - 0.2, dur=2.6, gain_db=-7, fade_in=0.1, fade_out=0.8)
    for at, dur, cyc in oar_cues:
        sc.sfx("oars", at, dur=dur, gain_db=-5, fade_in=0.05, fade_out=0.25, cycle=cyc)
    for ts, _, (bx_, _, _) in STRIKES:
        sc.sfx("thunder", ts, gain_db=-7, pan=max(-0.6, min(0.6, (bx_ - 1320) / 1300)))
    sc.sfx("whoosh", T_HIT - 0.45, gain_db=-10, pan=-0.4)
    sc.sfx("splash", T_HIT, gain_db=-5, pan=-0.3)
    for k, spec in enumerate(oar_specs):          # the lost oars drop into the sea
        if k % 2 == 0:
            sc.sfx("splash_small", spec["t_drop"] - 0.03, gain_db=-14, pan=max(-0.6, min(0.6, (spec["drop_x"] - 1320) / 1300)))
    sc.sfx("chime", t_lord + 0.3, gain_db=-15, pan=0.3)
    sc.sfx("sparkle", t_all + 0.2, gain_db=-18, pan=0.3)
    return sc
