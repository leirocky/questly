"""Scene 14 (v2) — God speaks to Jonah a second time; this time he obeys (Jonah 3:1-3a).

(work in progress)
"""
import hashlib
import math
import random

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

SW, SH = 3000, 1188

# ------------------------------------------------------------------ Jonah rig (damp robe, walking staff)
STAFF_DX = 84.0          # figure px in front of the anchor where the staff stands while he kneels / stands
STAFF_LEN = 384.0        # figure px, tip to knob
STAFF_W = 11.0
WOOD = "#9a6236"
WOOD_DARK = "#74462a"
WRAP = P["jonah_sash"]


def _damp_marks(st):
    """A few drops (two from the hem, one from the beard) - he is only 'still a bit wet'."""
    hemp, um, Hm = st["hemp"], st["um"], st["Hm"]
    floor = st["ground"] - 2 if st["mode"] != "air" else None

    def drop(p, k):
        y = p[1] if floor is None else min(p[1], floor - 1.15 * k)
        return C._drop(p[0], y, k)
    out = ""
    chain = [p for p in hemp if C._dot(C._sub(p, Hm), um) > -2]
    chain = sorted(chain, key=lambda p: C._dot(p, (-um[1], um[0])))
    if chain:
        for i, k in enumerate((0.3, 0.78)):
            p = chain[int(k * (len(chain) - 1))]
            out += drop(C._add(p, C._mul(um, 13 + 7 * i)), 5.0)
    chin = st["hw"](0.16, 1.32)
    out += drop((chin[0], chin[1] + 4), 4.6)
    return out


def _damp_patches(st):
    """Darker soaked patches along the hem, clipped to the hem band of the robe."""
    hemp, um, Hm, m = st["hemp"], st["um"], st["Hm"], st["m"]
    cid = "dmp" + hashlib.md5(C._d(hemp).encode()).hexdigest()[:10]
    col = S.shade(S.shade(P["jonah_robe"], -0.08), -0.2)
    inner = ""
    for k, (fx, r) in enumerate(((-0.55, 14), (0.1, 17), (0.65, 12))):
        c = C._add(C._sub(Hm, C._mul(um, 8 + 6 * (k % 2))), C._mul((-um[1], um[0]), fx * m["ww"]))
        inner += f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{r * 1.3:.1f}" ry="{r:.1f}" fill="{col}" opacity="0.5"/>'
    return (f'<clipPath id="{cid}"><path d="{C._d(hemp)}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>')


def _damp_design(front=None):
    """Jonah's design 'still a bit wet': the robe ~8 % darker with soaked patches at the hem and a few drops, the
    head-cloth already dry, and no seaweed any more."""
    D = C._jonah_design(wet=False)
    D["robe"] = D["sleeve"] = S.shade(P["jonah_robe"], -0.08)
    D["hem_col"] = S.shade(P["jonah_robe_dark"], -0.06)
    D["mid"] = _damp_patches
    D["front"] = (lambda st: front(st) + _damp_marks(st)) if front else _damp_marks
    return D


def _fist_centre(st, i=1):
    """Centre of hand i's fist (body coords), as characters._hand draws it."""
    Sx, E, W = st["arms"][i]
    d = C._nrm(C._sub(W, E))
    return C._add(W, C._mul(d, 0.45 * st["m"]["hr"]))


def _staff_markup(tip, through, length=STAFF_LEN, w=STAFF_W):
    """A wooden walking staff from ``tip`` along the line through ``through`` (body coords), knob at the top."""
    d = C._nrm(C._sub(through, tip))
    top = C._add(tip, C._mul(d, length))
    n = (-d[1], d[0])
    w0, w1 = w * 0.42, w * 0.55
    pts = [C._add(tip, C._mul(n, w0)), C._add(top, C._mul(n, w1)), C._sub(top, C._mul(n, w1)),
           C._sub(tip, C._mul(n, w0))]
    body = (f'<path d="M{C._pt(pts[0])} L{C._pt(pts[1])} L{C._pt(pts[2])} L{C._pt(pts[3])} Z" fill="{WOOD}" '
            f'stroke="{P["ink"]}" stroke-width="3.4" stroke-linejoin="round"/>')
    # grain line, a knot and the round knob at the top
    g0, g1 = C._add(tip, C._mul(d, 40)), C._add(tip, C._mul(d, length - 30))
    body += C._line(f"M{C._pt(C._add(g0, C._mul(n, 1.5)))} L{C._pt(C._add(g1, C._mul(n, 1.5)))}", w=1.6,
                    col=WOOD_DARK, extra='opacity="0.7"')
    kn = C._add(tip, C._mul(d, length * 0.62))
    body += f'<ellipse cx="{kn[0]:.1f}" cy="{kn[1]:.1f}" rx="3.2" ry="2.2" fill="{WOOD_DARK}"/>'
    kb = C._add(top, C._mul(d, 4))
    body += (f'<circle cx="{kb[0]:.1f}" cy="{kb[1]:.1f}" r="{w * 0.95:.1f}" fill="{S.shade(WOOD, 0.1)}" '
             f'stroke="{P["ink"]}" stroke-width="3.4"/>'
             f'<circle cx="{kb[0] - 3:.1f}" cy="{kb[1] - 3:.1f}" r="2.6" fill="#f0d2a8" opacity="0.8"/>')
    # a teal cloth wrap just under the knob (ties it to Jonah's sash colour)
    a, b = C._add(top, C._mul(d, -22)), C._add(top, C._mul(d, -40))
    body += (f'<path d="M{C._pt(a)} L{C._pt(b)}" stroke="{P["ink"]}" stroke-width="{w + 6.8:.1f}" '
             f'stroke-linecap="butt"/>'
             f'<path d="M{C._pt(a)} L{C._pt(b)}" stroke="{WRAP}" stroke-width="{w + 1.6:.1f}" stroke-linecap="butt"/>')
    return body


def _grip(st, tip):
    """Front hook: the staff through the near fist, then the fist again on top so the fingers close round it."""
    c = _fist_centre(st)
    hr = st["m"]["hr"]
    return (_staff_markup(tip, c) +
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{hr:.1f}" fill="{P["skin"]}" stroke="{P["ink"]}" '
            f'stroke-width="3.2"/>'
            + C._line(f"M{c[0] - 0.55 * hr:.1f},{c[1] - 0.15 * hr:.1f} q{0.5 * hr:.1f},{0.35 * hr:.1f} "
                      f"{1.05 * hr:.1f},0", w=1.8))


def jonah_fig(x, y, s, ps, expr=None, facing=1, marks=True, staff=None, label="j"):
    """Damp Jonah in pose dict ``ps``. staff=(tip_x, lift) in figure px (x forward of the anchor, lift above the
    ground) draws the walking staff held in the near hand."""
    ps = dict(C.POSES[ps]) if isinstance(ps, str) else dict(ps)
    e = expr or ps["expr"]
    front = None
    if staff is not None:
        tx, lift = staff
        front = lambda st: _grip(st, (tx, st["ground"] - lift))   # noqa: E731
    inner, _ = C._figure(_damp_design(front), C._ADULT, ps, e, C._fsign(facing), marks)
    return C._wrap_out(inner, x, y, s, facing, label)


def _jfn(x, y, scale=1.0, facing=1, ps=None, expr=None, marks=True, staff=None):
    return jonah_fig(x, y, scale, ps, expr, facing, marks, staff)


def staff_alone(x, y, s):
    """The staff standing planted in the ground at stage (x, y) (while Jonah kneels beside it)."""
    body = _staff_markup((0.0, 0.0), (0.0, -10.0)) + \
        f'<ellipse cx="0" cy="2" rx="20" ry="4" fill="{P["ink"]}" opacity="0.18"/>'
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><g filter="url(#wobble-fine)">{body}</g></g>'


# poses ------------------------------------------------------------------------------------------
_KNEEL = C.POSES["kneel_pray"]
KNEEL_UP = dict(_KNEEL, look=(0.03, -0.08))                        # eyes open, looking up into the light
KNEEL_LISTEN = dict(_KNEEL, h=-18, look=(0.03, -0.08), marks=("sound",),
                    arms=(("ik", "torso", 0.9, 0.42, 1), ("ik", "head", -0.66, 0.16, -1)),
                    hands=("open", "cup"))
KNEEL_CHEST = dict(_KNEEL, h=-8, look=(0.02, -0.05),
                   arms=(("ik", "torso", 0.9, 0.42, 1), ("ik", "torso", 0.55, 0.74, 1)),
                   hands=("open", "open"))
KNEEL_NOD = dict(KNEEL_CHEST, h=14, look=(0.0, 0.04))
KNEEL_CITY = dict(KNEEL_CHEST, h=-2, look=(0.08, -0.01))           # hand on chest, looking far east (right)
KNEEL_VISOR = dict(_KNEEL, h=-4, look=(0.08, -0.02),
                   arms=(("ik", "torso", 0.9, 0.42, 1), ("ik", "headw", 0.62, -0.5, 1)), hands=("open", "open"))
RISE = C._P(t=4, h=-8, drop=70, legs=(("ik", 60, 1), (0, -92)),
            arms=(("fk", 30, 40), ("ik", "abs", STAFF_DX - 6, -205, 1)),
            hands=("open", "fist"), feet=(None, 100))
STAND_STAFF = C._P(arms=(("fk", 14, 8), ("ik", "abs", STAFF_DX - 6, -168, 1)), hands=("fist", "fist"))


def walk_staff_pose(k, A=40.0, N=5, swing=34, lift=20, drop=10):
    """Planted-foot walk drawing k (N drawings per step, two steps per cycle, the s02 rig) holding the staff in the
    near hand. The staff tip is planted together with the FAR foot (step 0) and moves back with it, so it never
    slides on the road; during step 1 it swings forward through the air. Returns (pose, (tip_x, tip_lift))."""
    ph = (k % (2 * N)) / N
    step, u = divmod(ph, 1.0)
    plant = ("ik", A * (1 - 2 * u), 1)
    swing_leg = ("ik", -A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 1, lift * math.sin(math.pi * u))
    sw = swing * math.cos(math.pi * ph)
    c = STAFF_DX - A
    if step == 0:
        tip = (c + A * (1 - 2 * u), 0.0)
    else:
        tip = (c - A + 2 * A * (0.5 - 0.5 * math.cos(math.pi * u)), 16 * math.sin(math.pi * u))
    hx = STAFF_DX - 26 + 22 * math.cos(math.pi * ph)
    ps = C._P(t=4, h=-3, legs=(plant, swing_leg) if step == 0 else (swing_leg, plant),
              arms=(("fk", -sw, -sw + 16), ("ik", "abs", hx, -166 + 4 * math.sin(math.pi * ph), 1)),
              hands=("fist", "fist"), drop=drop + 0.4 * drop * math.cos(2 * math.pi * u))
    return ps, tip
