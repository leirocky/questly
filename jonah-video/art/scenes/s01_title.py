"""Scene 1 — title page: a calm dawn sea, the great fish arching out of the water, a little ship far on
the horizon, gulls flying across, and the book title appearing with the narration.

v2: the approved v1 page (art/scenes_v1/s01_title.py) with its timing adapted to the v2 voice take
("圣经绘本：约拿的故事。", one utterance / one subtitle chunk, ~2.6 s, read more slowly than in v1).

Beats (all derived from ctx.duration and ctx.lines[0]; nothing hard-coded to the voice take):
  start        calm, readable frame (the film fades in from black over it): only the fish's back and dorsal fin
               above the swell (tail kept low and the water in front of the head nearly opaque, so no fin or eye
               reads ambiguously), the ship rocking on the horizon, a pair of gulls flying in above the ship, a far
               gull high on the left, sun rising
  ~1.0 s ..    the great fish arches up and forward out of the sea: nose up while rising, then the back curves
               over and the tail lifts clear at the top of the arc during "圣经绘本" (soft splash crest, a burst
               of spray that falls back, drops shed from the back), soft splash sfx
  line 0       "圣经绘本" -> the ribbon header unfurls just before the voice (chime); "约拿的故事" -> the five big
               title characters pop in one by one on their syllables. The syllables are located at build time
               in the line's voice clip (see syllable_onsets: the pause after 绘本 and the end of speech, with
               fixed ratios in between), so a regenerated voice take stays in sync; fallback: fractions of the
               line measured on the 2.44 s v2 take
  end          calm hold (~1.5 s): the fish hovers at the top of its arc, blinks and waves its tail, the gull pair
               glides on toward the sun and passes well above it (the lead gull glides there, wings level; their
               speed is derived from the scene length so they are still in view at the end), slow push-in; the sea
               ambience fades out across the closing dissolve

Edges: the camera starts slightly inside the stage (>= 26 px margin) because the full-width sea bands bob
sideways; the foreground crests only "swell" by scaling about their outer stage corner, so their cut edges
never move into view.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.paths import BUILD
from engine.scene import Scene

# ------------------------------------------------------------------ layout (stage px)
HORIZON = 700
SUN = (1720, 640)
SUN_R = 92
SHIP_X, SHIP_WL, SHIP_S = 360, 716, 0.17
MID_Y = 792                     # top of the mid-sea band
FISH_X, FISH_Y, FISH_S = 860, 860, 0.55
FISH_WL = 905                   # waterline the fish breaks through
NEAR_Y = 1052                   # top of the near-sea band

TITLE = "约拿的故事"
TITLE_Y, TITLE_SIZE, TITLE_STEP = 418, 200, 214
RIB_X, RIB_Y = W / 2, 150       # ribbon header centre
# Where each title syllable starts. Primary: measured in the voice clip at build time (syllable_onsets):
# t_a = end of the >= 0.25 s pause after 绘本 (the 约 onset), t_b = end of speech, and the five onsets at
# t_a + SYLLABLE_RATIO * (t_b - t_a); these ratios fit both the 2.574 s and the 2.44 s takes to ~0.03 s.
# Fallback (clip missing or unreadable): fractions of narration line 0, measured on the 2.44 s v2 take
# build/voice/lines/s01_title_00.wav: 约 1.415, 拿 1.56 (the n murmur), 的 1.81 (burst), 故 1.94 (burst),
# 事 2.125 (sh onset) s from the clip start; 圣经绘本 runs 0.04-1.06 s, then a 0.35 s pause.
SYLLABLE_RATIO = (0.0, 0.147, 0.401, 0.533, 0.721)
SYLLABLE_FRAC = (0.580, 0.639, 0.742, 0.795, 0.871)
SYLLABLE_L = 2.44               # length of the take SYLLABLE_FRAC was measured on (s)

GULL_BASE = (1056, 560)
GULL_S = 0.7
WINGS = (1.0, 0.5, 0.0, -0.5, -1.0)
FLAP_SEQ = (2, 1, 0, 1, 2, 3, 4, 3)     # starts from the glide pose (wing 0)
GULL_X0, GULL_Y, GULL_LAG = 480, 556, 0.5     # near pair: start x, path height, lag of the second gull (s)
GULL_X1 = 1840          # where the leading gull is at the end of the scene (still inside the final view)
# The pair's paths rise toward both ends (y = ymid - bend * ((x - W/2) / 1100)^2): they dip under the title in
# the middle and pass above the rising sun on the right. The lead gull bends more and glides (wings level) from
# the glide window before it reaches the sun, so neither its belly nor a down-stroke wing grazes the rim (>= 20 px
# clear). The trailing gull keeps the v1 bend (more would lift its up-stroke wing into 事) and only rises a little
# after it has passed the title (GULL_B_RISE: x0, x1, px), so it is ~29 px clear of the rim at the end too.
GULL_A_BEND, GULL_B_BEND = 160, 60
GULL_B_RISE = (1580, 1760, 25)

FISH_TAILS = tuple(float(v) for v in np.linspace(-0.75, 0.75, 13))   # 13 phases; closed eye on even ones
TAIL_PERIOD = 1.5

SKY_TOP, SKY_MAUVE, SKY_PEACH, SKY_GLOW = "#b7a6d4", "#dcb8cf", "#f4c6a6", "#fbe3b6"
CREAM = "#fff6e3"
DROP = "#f2fbff"                # water droplets


def doc(body, defs=""):
    return S.svg_doc(body, defs)


# ================================================================== sky & far planes


def sky():
    defs = (f'<linearGradient id="s1sky" gradientUnits="userSpaceOnUse" x1="0" y1="-20" x2="0" y2="{HORIZON + 10}">'
            f'<stop offset="0" stop-color="{SKY_TOP}"/><stop offset="0.32" stop-color="{SKY_MAUVE}"/>'
            f'<stop offset="0.64" stop-color="{SKY_PEACH}"/><stop offset="1" stop-color="{SKY_GLOW}"/>'
            f'</linearGradient>' +
            S.rad_grad("s1sunglow", [(0, "#fff4cf", 0.95), (0.3, "#ffe6ad", 0.6), (1, "#ffd9a0", 0)]) +
            S.rad_grad("s1tglow", [(0, "#fff3e2", 0.45), (0.6, "#fbe6dc", 0.18), (1, "#fbe6dc", 0)]))
    b = S.rect_bg("url(#s1sky)")
    # a calm, slightly lighter patch of sky behind the title
    b += f'<ellipse cx="{W / 2}" cy="300" rx="820" ry="300" fill="url(#s1tglow)"/>'
    b += f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="460" fill="url(#s1sunglow)"/>'
    return doc(b, defs)


def sun_rays():
    defs = S.rad_grad("s1ray", [(0, "#fff5dc", 1), (0.45, "#fff0d4", 0.55), (1, "#fff0d4", 0)])
    d = S.rays(SUN[0], SUN[1], SUN_R + 20, 360, n=18, width_deg=6.5)
    return doc(S.g(f'<path d="{d}" fill="url(#s1ray)"/>', filter="soft", opacity=0.75), defs)


def sun_disc():
    defs = S.rad_grad("s1sun", [(0, "#fff0b0"), (0.6, P["sun"]), (1, "#f7bd55")], cx=0.45, cy=0.42)
    b = f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="{SUN_R}" fill="url(#s1sun)" stroke="{P["ink"]}" stroke-width="3.5"/>'
    b += f'<circle cx="{SUN[0] - 28}" cy="{SUN[1] - 30}" r="22" fill="#fff6d0" opacity="0.6"/>'
    return doc(S.g(b, filter="wobble"), defs)


def streak(cx, cy, w, h, fill, seed=0):
    """Thin dawn cloud streak: a long rounded lozenge with a soft lower shade."""
    pts = [(cx - w / 2, cy + h * 0.25), (cx - w * 0.3, cy - h * 0.55), (cx, cy - h * 0.75),
           (cx + w * 0.32, cy - h * 0.5), (cx + w / 2, cy + h * 0.2), (cx + w * 0.2, cy + h * 0.55),
           (cx - w * 0.25, cy + h * 0.6)]
    d = S.smooth_path(pts)
    return (f'<path d="{d}" fill="{fill}" opacity="0.8"/>' +
            f'<path d="M{cx - w * 0.3:.0f},{cy - h * 0.25:.0f} Q{cx:.0f},{cy - h * 0.55:.0f} '
            f'{cx + w * 0.3:.0f},{cy - h * 0.3:.0f}" stroke="#fff1e4" stroke-width="{h * 0.22:.1f}" '
            f'fill="none" opacity="0.7" stroke-linecap="round"/>')


def far_planes():
    """Hazy far coast on the right and thin dawn streak clouds (static)."""
    hill_col = "#c9adc4"
    b = S.path(S.hill(1790, 2240, HORIZON + 4, 70, seed=4, bumps=2, bottom=HORIZON + 30), fill=hill_col, sw=2.5)
    b += S.path(S.hill(1930, 2260, HORIZON + 4, 112, seed=7, bumps=2, bottom=HORIZON + 30),
                fill=S.mix(hill_col, "#a98fb0", 0.35), sw=2.5)
    b = S.g(b, filter="wobble")
    st = (streak(470, 612, 320, 22, "#e8c3d2") + streak(690, 648, 180, 14, "#ecccd6") +
          streak(1560, 604, 300, 20, "#f0c8cc") + streak(1700, 628, 170, 12, "#f3d2d0") +
          streak(1960, 548, 240, 16, "#e8c3d2"))
    b += S.g(st, filter="s1wash")
    return doc(b, '<filter id="s1wash" x="-10%" y="-60%" width="120%" height="220%">'
                  '<feGaussianBlur stdDeviation="2.2"/></filter>')


def clouds():
    shade = "#e8bfc9"
    b = (S.cloud(330, 180, 440, 150, "#fdeee6", seed=1, sw=3.5, shade_fill=shade) +
         S.cloud(110, 345, 230, 82, "#fbe8e2", seed=5, sw=3, shade_fill=shade) +
         S.cloud(1870, 175, 420, 140, "#fdeee6", seed=3, sw=3.5, shade_fill=shade) +
         S.cloud(2040, 345, 210, 74, "#fbe8e2", seed=6, sw=3, shade_fill=shade))
    return doc(S.g(b, filter="wobble"))


# ================================================================== sea


def far_sea():
    defs = (f'<linearGradient id="s1far" gradientUnits="userSpaceOnUse" x1="0" y1="{HORIZON}" x2="0" y2="{MID_Y + 20}">'
            f'<stop offset="0" stop-color="{S.mix(P["sea_pale"], SKY_GLOW, 0.35)}"/>'
            f'<stop offset="1" stop-color="{S.mix(P["sea_light"], P["sea_pale"], 0.3)}"/></linearGradient>')
    b = S.path(S.wave_band(HORIZON, 3, 260, 0.3, bottom=H + 60), fill="url(#s1far)", sw=3)
    r = np.random.default_rng(4)
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(HORIZON + 16, MID_Y - 6)
        ln = r.uniform(30, 90) * (0.6 + (y - HORIZON) / 120)
        b += (f'<path d="M{x:.0f},{y:.0f} q{ln / 2:.0f},-4 {ln:.0f},0" stroke="{P["foam"]}" stroke-width="3" '
              f'fill="none" opacity="0.55" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"), defs)


def far_ship():
    """The little ship far on the horizon, hazed toward the sky, clipped at its waterline (sailing west)."""
    defs = ('<filter id="s1haze"><feColorMatrix type="matrix" values="0.74 0 0 0 0.25  0 0.74 0 0 0.2  '
            '0 0 0.74 0 0.19  0 0 0 1 0"/></filter>'
            f'<clipPath id="s1shipclip"><rect x="{SHIP_X - 400}" y="{SHIP_WL - 400}" width="800" height="401"/>'
            f'</clipPath>')
    b = S.g(S.g(PR.ship(SHIP_X, SHIP_WL, SHIP_S, -1, sail="full", lantern=False), extra='filter="url(#s1haze)"'),
            extra='clip-path="url(#s1shipclip)"')
    # a little foam where the hull meets the water
    b += (f'<path d="M{SHIP_X - 96},{SHIP_WL} q48,-4 96,-1 t96,1" stroke="{P["foam"]}" stroke-width="3.5" '
          f'fill="none" opacity="0.9" stroke-linecap="round"/>')
    return doc(b, defs)


def mid_sea():
    defs = (f'<linearGradient id="s1mid" gradientUnits="userSpaceOnUse" x1="0" y1="{MID_Y - 10}" x2="0" y2="{FISH_WL + 60}">'
            f'<stop offset="0" stop-color="{S.mix(P["sea_light"], SKY_PEACH, 0.12)}"/>'
            f'<stop offset="1" stop-color="{P["sea"]}"/></linearGradient>')
    b = S.path(S.wave_band(MID_Y, 7, 300, 1.0, bottom=FISH_WL + 160), fill="url(#s1mid)", sw=3.5)
    b += S.path(S.wave_line(MID_Y + 16, 5, 300, 1.4), stroke=False,
                extra=f'stroke="{P["foam"]}" stroke-width="4.5" fill="none" opacity="0.55" '
                      f'stroke-dasharray="120 160" stroke-linecap="round"')
    r = np.random.default_rng(8)
    for _ in range(18):
        x, y = r.uniform(0, W), r.uniform(MID_Y + 40, FISH_WL - 10)
        ln = r.uniform(50, 120)
        b += (f'<path d="M{x:.0f},{y:.0f} q{ln / 2:.0f},-6 {ln:.0f},0" stroke="{P["foam"]}" stroke-width="3.5" '
              f'fill="none" opacity="0.45" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"), defs)


def glitter_frames():
    """Sun path on the water: three shimmer variants of short gold strokes under the sun."""
    out = []
    for k in range(3):
        r = np.random.default_rng(20 + k)
        b = ""
        y = HORIZON + 8
        while y < NEAR_Y + 40:
            u = (y - HORIZON) / (NEAR_Y - HORIZON)
            spread = 40 + 170 * u
            for _ in range(2 if u < 0.4 else 3):
                x = SUN[0] + r.normal(0, spread * 0.5)
                ln = r.uniform(18, 50) * (0.6 + 1.2 * u)
                op = (0.9 - 0.55 * u) * r.uniform(0.5, 1)
                b += (f'<path d="M{x - ln / 2:.0f},{y:.0f} q{ln / 2:.0f},-{2 + 3 * u:.0f} {ln:.0f},0" '
                      f'stroke="#fff3c8" stroke-width="{3 + 4 * u:.1f}" fill="none" opacity="{op:.2f}" '
                      f'stroke-linecap="round"/>')
            y += 9 + 16 * u
        out.append(doc(S.g(b, filter="wobble-fine")))
    return out


def fish_front(top_op=0.6):
    """Sea band in front of the fish; its top is translucent (top_op) so the submerged body shows faintly."""
    defs = (f'<linearGradient id="s1ff" gradientUnits="userSpaceOnUse" x1="0" y1="{FISH_WL - 16}" x2="0" y2="{FISH_WL + 230}">'
            f'<stop offset="0" stop-color="{P["sea_light"]}" stop-opacity="{top_op}"/>'
            f'<stop offset="0.16" stop-color="{S.mix(P["sea_light"], P["sea"], 0.5)}" '
            f'stop-opacity="{max(0.9, top_op)}"/>'
            f'<stop offset="0.3" stop-color="{S.mix(P["sea_light"], P["sea"], 0.75)}"/>'
            f'<stop offset="0.6" stop-color="{P["sea"]}"/>'
            f'<stop offset="1" stop-color="{S.mix(P["sea"], P["sea_deep"], 0.6)}"/></linearGradient>')
    b = S.path(S.wave_band(FISH_WL, 10, 380, 1.3, bottom=H + 80), fill="url(#s1ff)", stroke=False)
    b += S.path(S.wave_line(FISH_WL, 10, 380, 1.3), sw=4)
    b += S.path(S.wave_line(FISH_WL + 20, 8, 380, 1.7), stroke=False,
                extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="0.6" '
                      f'stroke-dasharray="150 120" stroke-linecap="round"')
    r = np.random.default_rng(11)
    for _ in range(16):
        x, y = r.uniform(0, W), r.uniform(FISH_WL + 60, NEAR_Y - 10)
        ln = r.uniform(70, 150)
        b += (f'<path d="M{x:.0f},{y:.0f} q{ln / 2:.0f},-8 {ln:.0f},0" stroke="{P["foam"]}" stroke-width="4" '
              f'fill="none" opacity="0.4" stroke-linecap="round"/>')
    return doc(S.g(b, filter="wobble"), defs)


CREST_FRONT, CREST_REAR = 318, -296     # crest x offsets from FISH_X (where the body breaks the surface)


def _foam_blobs(blobs, sw=6.0):
    """Circles drawn twice (stroked, then fill only) so only the outer silhouette keeps an ink line."""
    c = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>' for x, y, r in blobs)
    return f'<g fill="{P["foam"]}" stroke="{P["ink"]}" stroke-width="{sw}">{c}</g><g fill="{P["foam"]}">{c}</g>'


def _water_crest(x, y, lean, h, w):
    """A soft mound of water peeling up and over toward `lean`, with a foam lip (spray: see drops_fx)."""
    def X(k):
        return x + lean * w * k
    water = S.mix(P["sea_light"], P["foam"], 0.25)
    d = (f"M{X(-0.8):.1f},{y + 6} C{X(-0.5):.1f},{y - h * 0.25:.1f} {X(-0.3):.1f},{y - h:.1f} {X(0.1):.1f},{y - h:.1f} "
         f"C{X(0.42):.1f},{y - h:.1f} {X(0.6):.1f},{y - h * 0.66:.1f} {X(0.5):.1f},{y - h * 0.46:.1f} "
         f"C{X(0.44):.1f},{y - h * 0.36:.1f} {X(0.56):.1f},{y - h * 0.2:.1f} {X(0.9):.1f},{y + 6} Z")
    b = S.path(d, fill=water, sw=3.2)
    b += (f'<path d="M{X(-0.45):.1f},{y} C{X(-0.3):.1f},{y - h * 0.45:.1f} {X(-0.1):.1f},{y - h * 0.7:.1f} '
          f'{X(0.15):.1f},{y - h * 0.72:.1f}" stroke="{P["sea"]}" stroke-width="5" fill="none" opacity="0.35" '
          f'stroke-linecap="round"/>')
    # foam lip along the crest top, ending in the curl (overlapping puffs -> one scalloped band)
    ctrl = [(-0.4, 0.78, 0.11), (-0.18, 0.97, 0.14), (0.08, 1.03, 0.16), (0.32, 0.94, 0.15), (0.5, 0.72, 0.13),
            (0.5, 0.5, 0.1)]
    lip = []
    for (k0, h0, r0), (k1, h1, r1) in zip(ctrl, ctrl[1:]):
        for j in range(3):
            u = j / 3
            lip.append((X(k0 + (k1 - k0) * u), y - h * (h0 + (h1 - h0) * u), h * (r0 + (r1 - r0) * u)))
    lip.append((X(ctrl[-1][0]), y - h * ctrl[-1][1], h * ctrl[-1][2]))
    b += _foam_blobs(lip, 5)
    return b


def splash_crest():
    """Soft splash crest where the fish breaks the surface: a peeling crest of water at the chest and at the
    tail, joined by lacy foam along the waterline."""
    y = FISH_WL + 2
    xf, xr = FISH_X + CREST_FRONT, FISH_X + CREST_REAR
    r = np.random.default_rng(5)
    lace = []
    x = xr - 40
    run_end = x + r.uniform(60, 140)
    while x < xf + 60:
        near = min(abs(x - xr), abs(x - xf))
        rad = 6 + 9 * math.exp(-(near / 80) ** 2) + r.uniform(-1.5, 2)
        lace.append((x, y + r.uniform(-3, 4), rad))
        x += rad * 1.1
        if x > run_end:                       # small gap between runs of foam
            x += r.uniform(14, 34)
            run_end = x + r.uniform(60, 150)
    b = (f'<ellipse cx="{(xr + xf) / 2:.0f}" cy="{y + 8}" rx="{(xf - xr) / 2 + 90:.0f}" ry="18" fill="{P["foam"]}" '
         f'opacity="0.35"/>')
    b += _water_crest(xr, y, -1, 70, 115)
    b += _water_crest(xf, y, 1, 84, 125)
    b += _foam_blobs(lace, 5)
    return doc(S.g(b, filter="wobble-fine"))


def ripples():
    """Two faint rings spreading on the water around the fish."""
    cx, cy = FISH_X - 10, FISH_WL + 16
    b = ""
    for rx, ry, sw, op in ((470, 40, 5, 0.75), (560, 52, 4, 0.5)):
        b += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{P["foam"]}" '
              f'stroke-width="{sw}" opacity="{op}" stroke-dasharray="{rx * 0.5:.0f} {rx * 0.12:.0f}"/>')
    return doc(S.g(b, filter="wobble"))


def near_sea():
    defs = (f'<linearGradient id="s1near" gradientUnits="userSpaceOnUse" x1="0" y1="{NEAR_Y - 20}" x2="0" y2="{H + 40}">'
            f'<stop offset="0" stop-color="{S.mix(P["sea"], P["sea_deep"], 0.45)}"/>'
            f'<stop offset="1" stop-color="{S.shade(P["sea_deep"], -0.1)}"/></linearGradient>')
    b = S.path(S.wave_band(NEAR_Y, 14, 440, 2.2, bottom=H + 90), fill="url(#s1near)", sw=4)
    b += S.path(S.wave_line(NEAR_Y + 18, 10, 440, 2.6, x0=600, x1=1600), stroke=False,
                extra=f'stroke="{P["foam"]}" stroke-width="6" fill="none" opacity="0.55" '
                      f'stroke-dasharray="180 140" stroke-linecap="round"')
    return doc(S.g(b, filter="wobble"), defs)


def curl_wave(x, y, s, flip, seed):
    """Big foreground curling wave crest, base at (x, y), curling toward +x (flip=-1 mirrors)."""
    def P_(px, py):
        return f"{x + flip * px * s:.1f},{y + py * s:.1f}"
    body = (f"M{P_(-120, 420)} L{P_(-120, -110)} C{P_(-40, -175)} {P_(120, -238)} {P_(250, -232)} "
            f"C{P_(350, -228)} {P_(420, -185)} {P_(418, -128)} C{P_(416, -82)} {P_(378, -58)} {P_(344, -72)} "
            f"C{P_(312, -86)} {P_(318, -124)} {P_(350, -122)} C{P_(330, -150)} {P_(270, -150)} {P_(250, -104)} "
            f"C{P_(232, -60)} {P_(300, 10)} {P_(470, 40)} C{P_(560, 55)} {P_(640, 90)} {P_(720, 150)} "
            f"L{P_(720, 420)} L{P_(-120, 420)} Z")
    deep, mid = S.mix(P["sea"], P["sea_deep"], 0.55), S.mix(P["sea_light"], P["sea"], 0.45)
    b = S.path(body, fill=deep, sw=4.5)
    # lighter inner face of the curl
    face = (f"M{P_(-120, -60)} C{P_(-30, -130)} {P_(120, -190)} {P_(240, -186)} "
            f"C{P_(300, -184)} {P_(330, -165)} {P_(320, -145)} C{P_(260, -160)} {P_(200, -120)} {P_(205, -70)} "
            f"C{P_(120, -90)} {P_(0, -40)} {P_(-120, -10)} Z")
    b += S.path(face, fill=mid, stroke=False, extra='opacity="0.75"')
    # foam lip on top of the crest
    lip = (f"M{P_(-60, -170)} C{P_(40, -230)} {P_(170, -262)} {P_(270, -252)} C{P_(380, -244)} {P_(440, -190)} "
           f"{P_(428, -130)} C{P_(410, -150)} {P_(392, -170)} {P_(372, -168)} C{P_(360, -190)} {P_(330, -196)} "
           f"{P_(312, -184)} C{P_(290, -214)} {P_(240, -214)} {P_(222, -200)} C{P_(190, -222)} {P_(130, -214)} "
           f"{P_(112, -198)} C{P_(70, -210)} {P_(10, -190)} {P_(-60, -170)} Z")
    b += S.path(lip, fill=P["foam"], sw=3.5)
    # spiral highlight inside the curl
    b += (f'<path d="M{P_(352, -100)} C{P_(370, -100)} {P_(388, -112)} {P_(384, -136)}" stroke="{P["foam"]}" '
          f'stroke-width="{5 * s:.1f}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # foam lines on the wave face
    for k, (a0, a1, yy) in enumerate(((-90, 120, -40), (-60, 200, 20), (60, 330, 70))):
        b += (f'<path d="M{P_(a0, yy)} Q{P_((a0 + a1) / 2, yy - 18)} {P_(a1, yy)}" stroke="{P["foam"]}" '
              f'stroke-width="{6 * s:.1f}" fill="none" opacity="0.5" stroke-linecap="round"/>')
    return b


def curl_spray(x, y, s, flip):
    """Spray drops off the curl tip of curl_wave(x, y, s, flip): light bluish-white with a thin, light outline
    and a highlight. On their own wc=0 layer — the watercolour pass greys such small shapes into pebbles."""
    b = ""
    for dx, dy, rr in ((470, -150, 10), (500, -110, 7), (455, -205, 7), (520, -170, 5)):
        cx_, cy_ = x + flip * dx * s, y + dy * s
        b += (f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{rr * s:.1f}" fill="{DROP}" stroke="{P["ink"]}" '
              f'stroke-opacity="0.45" stroke-width="{1.8 * s:.1f}"/>'
              f'<circle cx="{cx_ - rr * s * 0.38:.1f}" cy="{cy_ - rr * s * 0.4:.1f}" r="{max(1.2, rr * s * 0.25):.1f}" '
              f'fill="#fffffa" opacity="0.9"/>')
    return b


CURL_L, CURL_R = (-30, 1060, 0.9, 1), (2150, 1080, 0.8, -1)     # x, y, scale, flip


def crest_left():
    return doc(S.g(curl_wave(*CURL_L, 1), filter="wobble"))


def crest_right():
    return doc(S.g(curl_wave(*CURL_R, 2), filter="wobble"))


def crest_spray(curl):
    return doc(S.g(curl_spray(*curl), filter="wobble-fine"))


# ================================================================== title


def title_defs():
    return (S.lin_grad("s1tg", [(0, "#4a8fb0"), (0.55, "#2f6c8e"), (1, "#245a78")]) +
            '<filter id="s1tsh" x="-20%" y="-20%" width="140%" height="140%">'
            '<feGaussianBlur stdDeviation="7"/></filter>')


def title_char(ch, x, y):
    font = f'font-family="LXGW WenKai" font-weight="bold" font-size="{TITLE_SIZE}" text-anchor="middle"'
    b = (f'<text x="{x + 6}" y="{y + 10}" {font} fill="{P["ink"]}" opacity="0.28" filter="url(#s1tsh)" '
         f'stroke="{P["ink"]}" stroke-width="18" stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="{CREAM}" stroke="{CREAM}" stroke-width="22" '
          f'stroke-linejoin="round">{ch}</text>')
    b += (f'<text x="{x}" y="{y}" {font} fill="url(#s1tg)" stroke="{P["ink"]}" stroke-width="3.5" '
          f'stroke-linejoin="round">{ch}</text>')
    return doc(b, title_defs())


def ribbon():
    cx, cy, hw, h = RIB_X, RIB_Y, 330, 80
    band_col = S.mix(P["terracotta"], "#f0a07a", 0.35)
    tail_col, fold_col = S.shade(band_col, -0.16), S.shade(band_col, -0.38)
    b = ""
    for sd in (-1, 1):
        ex = cx + sd * hw
        top, bot = cy - h / 2 + 26, cy + h / 2 + 26
        pts = [(ex - sd * 30, top), (ex + sd * 95, top), (ex + sd * 66, (top + bot) / 2), (ex + sd * 95, bot),
               (ex - sd * 30, bot)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z", fill=tail_col, sw=3.5)
        fold = [(ex, cy + h / 2 + 6), (ex - sd * 30, bot), (ex - sd * 30, cy + h / 2 + 6)]
        b += S.path("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in fold) + " Z", fill=fold_col, sw=3)
    band = (f"M{cx - hw},{cy - h / 2 + 8} Q{cx},{cy - h / 2 - 12} {cx + hw},{cy - h / 2 + 8} "
            f"L{cx + hw},{cy + h / 2 + 6} Q{cx},{cy + h / 2 - 14} {cx - hw},{cy + h / 2 + 6} Z")
    b += S.path(band, fill=band_col, sw=3.5)
    b += (f'<path d="M{cx - hw + 18},{cy - h / 2 + 18} Q{cx},{cy - h / 2} {cx + hw - 18},{cy - h / 2 + 18}" '
          f'stroke="#f7c9a8" stroke-width="3" fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    b += (f'<path d="M{cx - hw + 18},{cy + h / 2 - 4} Q{cx},{cy + h / 2 - 22} {cx + hw - 18},{cy + h / 2 - 4}" '
          f'stroke="#f7c9a8" stroke-width="3" fill="none" opacity="0.8" stroke-dasharray="10 9"/>')
    body = S.g(b, filter="wobble-fine")
    body += (f'<text x="{cx}" y="{cy + 15}" font-family="LXGW WenKai" font-weight="bold" font-size="50" '
             f'fill="{CREAM}" text-anchor="middle" letter-spacing="3">圣经绘本 · 约拿书</text>')
    return doc(body)


# ================================================================== motion helpers


def hermite(keys):
    """Smooth curve through (t, value, slope) keys (cubic Hermite); clamps outside the key range."""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1]
        for (t0, v0, m0), (t1, v1, m1) in zip(keys, keys[1:]):
            if t <= t1:
                h = t1 - t0
                u = (t - t0) / h
                u2, u3 = u * u, u * u * u
                return ((2 * u3 - 3 * u2 + 1) * v0 + (u3 - 2 * u2 + u) * h * m0 + (-2 * u3 + 3 * u2) * v1 +
                        (u3 - u2) * h * m1)
        return keys[-1][1]
    return f


def fish_motion(T, t_rise0, t_rise1):
    """Back-only at the start, then an arc up AND forward out of the sea: nose up while rising, the back
    curving over (nose coming down) at the top, then a gentle hover. Each channel has its own smooth curve
    so the arc never stops and restarts at a key."""
    R = t_rise1 - t_rise0
    tm = t_rise0 + 0.45 * R
    dx = hermite([(0, 0, 5), (t_rise0, 5, 20), (t_rise0 + 0.5 * R, 75, 95), (t_rise1, 130, 45), (T, 175, 3)])
    dy = hermite([(0, 180, -2), (t_rise0, 176, -20), (tm, 82, -215), (t_rise1, -42, 0), (t_rise1 + 0.9, -30, 8),
                  (T, -24, 0)])
    rot = hermite([(0, -4, 0), (t_rise0, -4.5, -6), (t_rise0 + 0.55 * R, -18, -4), (t_rise1 + 0.1, -11, 9),
                   (t_rise1 + 1.0, -8, 1.5), (T, -7.5, 0)])
    key = lambda t: Tf(dx=dx(t), dy=dy(t), rot=rot(t), px=FISH_X, py=FISH_Y)
    wob = lambda t: Tf(rot=0.9 * math.sin(2 * math.pi * t / TAIL_PERIOD + 0.6))
    return M.combine(key, M.bob(5, 2.8, 0.1), wob)


def tail_value(t, t_rise0, t_rise1):
    """Tail bend -0.75..0.75 (+ = up). The upper lobe tip sits higher than the back, so before the rise the
    tail is held fully down (it stays under the surface while only the back and dorsal fin show); the beat
    widens in as the fish rises, and the tail is held up for ~0.5 s at the top of the arc so the lobe lifts
    clear of the water."""
    osc = math.sin(2 * math.pi * t / TAIL_PERIOD)
    ramp = M.progress(t, t_rise0, t_rise0 + 0.6, "sine")
    v = FISH_TAILS[0] * (1 - ramp) + FISH_TAILS[-1] * osc * ramp
    hold = M.progress(t, t_rise1 - 0.45, t_rise1 - 0.15, "sine") * (1 - M.progress(t, t_rise1 + 0.35, t_rise1 + 0.7,
                                                                                   "sine"))
    return v * (1 - hold) + FISH_TAILS[-1] * hold


def corner_swell(cx, cy, period, phase, ax, ay):
    """A foreground crest breathing like a swell: scaled about its outer stage corner (cx, cy), so the edges
    where the drawing is cut by the stage never move into view (unlike a sway or a bob)."""
    def m(t):
        a = 2 * math.pi * (t / period + phase)
        return Tf(sx=1 + ax * math.sin(a), sy=1 + ay * math.sin(a + 0.9), px=cx, py=cy)
    return m


def fish_point(tf, lx, ly):
    """Fish-local point (scale-1 coords, facing right) -> stage px under the layer transform tf."""
    x, y = FISH_X + lx * FISH_S, FISH_Y + ly * FISH_S
    a = math.radians(tf.rot)
    c, s = math.cos(a), math.sin(a)
    px, py = FISH_X, FISH_Y
    return px + tf.dx + c * (x - px) - s * (y - py), py + tf.dy + s * (x - px) + c * (y - py)


def gull_path(x0, vx, ymid, bend, scale, wob=0.0, phase=0.0, rise=None):
    """rise = (xa, xb, px): an extra smooth climb of px between x = xa and x = xb."""
    def pos(t):
        x = x0 + vx * t
        y = ymid - bend * ((x - W / 2) / 1100) ** 2 + wob * math.sin(1.9 * t + phase)
        if rise:
            u = min(1.0, max(0.0, (x - rise[0]) / (rise[1] - rise[0])))
            y -= rise[2] * u * u * (3 - 2 * u)
        return x, y

    def m(t):
        x, y = pos(t)
        x2, y2 = pos(t + 0.05)
        rot = math.degrees(math.atan2(y2 - y, x2 - x)) * 0.7
        return Tf(dx=x - GULL_BASE[0], dy=y - GULL_BASE[1], rot=rot, sx=scale, sy=scale,
                  px=GULL_BASE[0], py=GULL_BASE[1])
    return m


def flap(phase, beat=0.58, flap_for=1.4, glide_for=1.0, glide_from=None):
    """Wing flipbook index: a few whole wing beats, then a glide. FLAP_SEQ starts on the glide pose and the
    flapping lasts a whole number of beats, so both the start and the end of a flap run meet the glide pose
    without a jump. With glide_from = t, the bird glides from the start of the glide window that contains or
    precedes t to the end of the scene (it switches only at a window start, so there is no jump)."""
    step = beat / len(FLAP_SEQ)
    flap_for = max(1, round(flap_for / beat)) * beat
    cycle = flap_for + glide_for
    t_glide = math.inf
    if glide_from is not None:
        c = (glide_from + phase) % cycle
        t_glide = glide_from - (c - flap_for) if c >= flap_for else glide_from - c - glide_for

    def f(t):
        cyc = (t + phase) % cycle
        if cyc < flap_for and t < t_glide:
            return float(FLAP_SEQ[int(cyc / step) % len(FLAP_SEQ)])
        return 2.0          # glide (wing 0)
    return f


# ================================================================== voice timing


def _speech_span(path, floor_db=-40.0, min_pause=0.25):
    """(t_a, t_b, length) in s for a voice clip: t_a = end of its longest >= min_pause silence (here the
    pause after 绘本), t_b = end of speech; from a 5 ms RMS envelope (silence = floor_db below the peak).
    None if there is no such pause."""
    import soundfile as sf
    x, sr = sf.read(str(path), dtype="float32", always_2d=True)
    x = x.mean(axis=1)
    hop = max(1, int(0.005 * sr))
    n = len(x) // hop
    if n < 10:
        return None
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    idx = np.flatnonzero(20 * np.log10(rms / rms.max()) > floor_db)
    if len(idx) < 2:
        return None
    gaps = (np.diff(idx) - 1) * hop / sr
    j = int(np.argmax(gaps))
    if gaps[j] < min_pause:
        return None
    return idx[j + 1] * hop / sr, (idx[-1] + 1) * hop / sr, len(x) / sr


def syllable_onsets(ctx, L):
    """Onsets of 约 拿 的 故 事 in s from the start of line 0 (the clip is placed at the line start)."""
    path = BUILD / "voice" / "lines" / f"{ctx.id}_00.wav"
    try:
        span = _speech_span(path)
    except Exception as e:                              # missing / unreadable clip
        span, why = None, f"{type(e).__name__}: {e}"
    else:
        why = "no pause after 绘本 found"
    if span is not None:
        t_a, t_b, n = span
        if not (0.3 * n < t_a < 0.8 * n and 0.5 < t_b - t_a < 0.6 * n):
            span, why = None, f"implausible span {t_a:.2f}-{t_b:.2f} s in a {n:.2f} s clip"
    if span is not None:
        if abs(n - L) > 0.03:
            print(f"[{ctx.id}] warning: the voice clip is {n:.3f} s but line 0 in timeline.json is {L:.3f} s — "
                  f"timeline.json is out of date (python3 build.py voice); title pops follow the clip",
                  file=sys.stderr)
        return [t_a + r * (t_b - t_a) for r in SYLLABLE_RATIO]
    if abs(L - SYLLABLE_L) > 0.03:
        print(f"[{ctx.id}] warning: could not measure {path.name} ({why}) and line 0 is {L:.3f} s, not the "
              f"{SYLLABLE_L} s take SYLLABLE_FRAC was measured on — the title pops may be out of sync",
              file=sys.stderr)
    return [f * L for f in SYLLABLE_FRAC]


# ================================================================== effects


def drops_fx(fmot, t_rise0, t_rise1, T, seed=7):
    """Water drops: a burst of spray off both splash crests as the fish breaks the surface (thrown up and
    outward, falling back in), drops shed from the fish's back while it rises, then a few flicked off its
    tail. Light bluish-white with a thin light outline and a highlight; each drop grows in over 2 frames."""
    rng = np.random.default_rng(seed)
    # spawn only behind the gill line and throw them backward, so no drop ever crosses the face
    back = [(-560, -130), (-440, -205), (-300, -265), (-160, -300), (-20, -312), (110, -306)]
    parts = []
    for i in range(42):
        ts = rng.uniform(t_rise0 + 0.1, t_rise1 + 0.4)
        k = rng.uniform(0, len(back) - 1)
        i0 = int(k)
        u = k - i0
        lx = back[i0][0] + (back[i0 + 1][0] - back[i0][0]) * u
        ly = back[i0][1] + (back[i0 + 1][1] - back[i0][1]) * u
        x, y = fish_point(fmot(ts), lx, ly)
        parts.append((ts, x, y, rng.uniform(-130, 25), rng.uniform(-300, -80), rng.uniform(4.5, 9)))
    for i in range(16):
        ts = rng.uniform(t_rise1, T - 0.6)
        x, y = fish_point(fmot(ts), rng.uniform(-800, -700), rng.uniform(-300, -120))
        parts.append((ts, x, y, rng.uniform(-140, -30), rng.uniform(-220, -60), rng.uniform(4, 7)))
    # spray burst off the two crests (they follow the fish's forward travel)
    for side, off in ((1, CREST_FRONT), (-1, CREST_REAR)):
        for i in range(14):
            ts = rng.uniform(t_rise0 + 0.08, t_rise0 + 0.6)
            x = FISH_X + off + fmot(ts).dx + side * rng.uniform(-30, 70)
            y = FISH_WL - rng.uniform(25, 80)
            parts.append((ts, x, y, side * rng.uniform(30, 170), rng.uniform(-400, -170), rng.uniform(3.5, 7.5)))
    g = 1150.0
    fill, ink, hi = (242, 251, 255), (75, 52, 38), (255, 255, 250)
    grow = 2.0 / 30

    def fx(frame, t, view):
        live = []
        for ts, x0, y0, vx, vy, r in parts:
            a = t - ts
            if a <= 0:
                continue
            x, y = x0 + vx * a, y0 + vy * a + 0.5 * g * a * a
            if y > FISH_WL + 6:
                continue
            live.append((x, y, r, vy + g * a, min(1.0, a / grow)))
        if not live:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for x, y, r, vyy, k in live:
            ox, oy = view.to_out(x, y)
            rr = r * view.scale * (0.45 + 0.55 * k)
            st = min(1.8, 1 + abs(vyy) / 900)
            a = 0.35 + 0.65 * k
            d.ellipse([ox - rr, oy - rr * st, ox + rr, oy + rr], fill=(*fill, int(235 * a)),
                      outline=(*ink, int(110 * a)), width=2 if rr >= 6.5 else 1)
            hr = max(1.0, rr * 0.24)
            hx, hy = ox - rr * 0.38, oy - rr * st * 0.4
            d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(*hi, int(230 * a)))
        frame.alpha_composite(ov)
        return frame
    return fx


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    say = ctx.lines[0]
    L = say.end - say.start
    onsets = syllable_onsets(ctx, L)       # 约 拿 的 故 事, s from the line start
    # the fish surfaces just before the narration starts (after the film's fade-in, so the first second is
    # calm) and reaches the top of its arch during "圣经绘本"
    t_rise0 = max(1.0, say.start - 0.6)
    t_rise1 = t_rise0 + 1.5

    # ---- sky & far planes
    sc.add("sky", sky(), wc=0.6)
    sc.add("rays", sun_rays(), wc=0,
           motion=M.combine(M.keys([(0, {"dy": 24}), (T, {"dy": -14})], "sine"),
                            lambda t: Tf(rot=2.2 * t, px=SUN[0], py=SUN[1]),
                            M.pulse(0.75, 1.0, 3.2)))
    sc.add("sun", sun_disc(), motion=M.keys([(0, {"dy": 24}), (T, {"dy": -14})], "sine"))
    sc.add("far", far_planes(), wc=0.8)
    sc.add("clouds", clouds(), motion=M.drift(vx=8))
    sc.add("far_sea", far_sea(), wc=0.7)

    # a far, tiny gull high on the left (mostly gliding)
    gull_frames = [doc(PR.gull(GULL_BASE[0], GULL_BASE[1], GULL_S, 1, wing=w)) for w in WINGS]
    sc.add("gull_far", gull_frames, motion=gull_path(60, 40, 425, 0, 0.4, wob=7, phase=1.0),
           frame_at=flap(0.9, beat=0.62, flap_for=1.2, glide_for=1.6))

    # ---- ship far on the horizon, gently rocking, sailing west
    sc.add("ship", far_ship(), motion=M.combine(M.sway(2.0, 3.6, pivot=(SHIP_X, SHIP_WL)), M.bob(1.5, 3.6, 0.25),
                                                M.drift(vx=-5)))

    # ---- mid sea + sun path
    sea_m = lambda a, ax, ph: M.combine(M.bob(a, 3.2, ph), M.bob(ax, 5.0, ph, axis="x"))
    sc.add("mid_sea", mid_sea(), motion=sea_m(5, 12, 0.0))
    sc.add("glitter", glitter_frames(), wc=0, motion=M.bob(3, 3.2),
           frame_at=lambda t: (t * 2.2) % 3 if (t * 2.2) % 3 < 2 else 2.0)

    # ---- the great fish
    fmot = fish_motion(T, t_rise0, t_rise1)
    # 13 open-eye tail phases + 7 closed-eye ones (the even phases; a blink snaps to the nearest of them)
    fr = ([doc(PR.fish(FISH_X, FISH_Y, FISH_S, 1, eye="open", tail=tl)) for tl in FISH_TAILS] +
          [doc(PR.fish(FISH_X, FISH_Y, FISH_S, 1, eye="closed", tail=tl)) for tl in FISH_TAILS[::2]])
    n_t = len(FISH_TAILS)
    lo, hi = FISH_TAILS[0], FISH_TAILS[-1]
    blinks = [t_rise1 + 0.75, min(say.end + 0.55, T - 1.25)]     # the 2nd one before the closing dissolve

    def fish_frame(t):
        v = tail_value(t, t_rise0, t_rise1)
        f = int(round((v - lo) / (hi - lo) * (n_t - 1)))    # nearest tail phase (crossfades would ghost)
        if any(b <= t < b + 0.16 for b in blinks):
            f = n_t + int(round(f / 2))
        return float(f)
    sc.add("fish", fr, motion=fmot, frame_at=fish_frame, seed=11)

    # the water in front of the fish: nearly opaque at the top while only the back shows (no ghost of the
    # submerged eye), turning translucent as the fish rises so the body shows faintly through it
    sc.add("fish_front", [fish_front(0.95), fish_front(0.6)], motion=sea_m(6, -14, 0.3),
           frame_at=lambda t: M.progress(t, t_rise0 - 0.1, t_rise0 + 0.5, "sine"))

    def ripple_m(phase):
        def m(t):
            u = ((t - t_rise0) / 2.6 + phase) % 1.0
            on = M.progress(t, t_rise0 - 0.3, t_rise0 + 0.4, "sine")
            s = 0.7 + 0.5 * u
            return Tf(dx=fmot(t).dx, sx=s, sy=s, alpha=on * math.sin(math.pi * u) ** 0.8,
                      px=FISH_X - 10, py=FISH_WL + 16)
        return m
    rip = ripples()
    sc.add("ripple_a", rip, motion=ripple_m(0.0), wc=0.5)
    sc.add("ripple_b", rip, motion=ripple_m(0.5), wc=0.5)

    def crest_m(t):
        k = fmot(t)
        rise = M.progress(t, t_rise0, t_rise0 + 0.8, "out")
        settle = M.progress(t, t_rise0 + 0.8, t_rise1 + 1.2, "sine")
        sy = 0.4 + 0.8 * rise - 0.45 * settle + 0.05 * math.sin(t * 4.1)
        sx = 0.78 + 0.22 * rise
        return Tf(dx=k.dx, dy=4 * math.sin(2 * math.pi * t / 3.2 + 1.9), sx=sx, sy=sy,
                  px=FISH_X - 10, py=FISH_WL + 8)
    sc.add("crest", splash_crest(), motion=crest_m, boil=5)

    sc.add("near_sea", near_sea(), motion=sea_m(7, 18, 0.55))
    swell_l, swell_r = corner_swell(0, H, 3.6, 0.1, 0.018, 0.03), corner_swell(W, H, 3.9, 0.5, 0.016, 0.03)
    sc.add("crest_l", crest_left(), motion=swell_l)
    sc.add("crest_l_spray", crest_spray(CURL_L), motion=swell_l, wc=0)
    sc.add("crest_r", crest_right(), motion=swell_r)
    sc.add("crest_r_spray", crest_spray(CURL_R), motion=swell_r, wc=0)

    # ---- gulls flying across, dipping under the title
    # a pair in formation: gull_b trails gull_a by GULL_LAG s, a little higher and farther away; an unhurried
    # speed that keeps both in view until the end of the scene
    GULL_V = (GULL_X1 - GULL_X0) / T
    sc.add("gull_b", gull_frames, motion=gull_path(GULL_X0 - GULL_V * GULL_LAG, GULL_V, GULL_Y - 20, GULL_B_BEND,
                                                   0.8, wob=5, phase=1.3, rise=GULL_B_RISE), frame_at=flap(0.35))
    t_sun = (SUN[0] - SUN_R - 30 - GULL_X0) / GULL_V      # the lead gull nears the sun's left edge
    sc.add("gull_a", gull_frames, motion=gull_path(GULL_X0, GULL_V, GULL_Y, GULL_A_BEND, 1.0, wob=5),
           frame_at=flap(0.0, glide_from=t_sun))

    # ---- title: ribbon header with "圣经绘本", then the five characters on their syllables
    t_rib = say.start - 0.1              # the ribbon unfurls just before the voice

    def unfurl(t, t0=t_rib):
        if t < t0:
            return Tf(alpha=0)
        u = M.progress(t, t0, t0 + 0.6, "linear")
        return Tf(dy=2 * math.sin(2 * math.pi * t / 3.0 + 1.2), sx=0.2 + 0.8 * M.ease("back")(u),
                  sy=0.75 + 0.25 * M.ease("out")(u), alpha=M.progress(t, t0, t0 + 0.2, "sine"), px=RIB_X, py=RIB_Y)
    sc.add("ribbon", ribbon(), wc=0, motion=unfurl)
    x0 = W / 2 - TITLE_STEP * (len(TITLE) - 1) / 2
    for i, ch in enumerate(TITLE):
        x = x0 + i * TITLE_STEP
        t0 = say.start + onsets[i] - 0.06

        def pop(t, t0=t0, x=x, i=i):
            if t < t0:
                return Tf(alpha=0)
            a = min(1.0, (t - t0) / 0.12)
            u = min(1.0, (t - t0) / 0.42)
            s = 0.45 + 0.55 * M.ease("back")(u)
            dy = 30 * (1 - M.ease("out")(u)) + 2.5 * math.sin(2 * math.pi * (t / 2.6 + i * 0.16))
            return Tf(dy=dy, sx=s, sy=s, alpha=a, px=x, py=TITLE_Y - 70)
        sc.add(f"title_{i}", title_char(ch, x, TITLE_Y), wc=0, motion=pop)

    t_done = say.start + onsets[-1] + 0.4
    # starts slightly inside the stage: >= 26 px margin at the sides, 15 px top/bottom (the sea bands bob up
    # to 18 px sideways and 7 px vertically)
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W * 0.975)), (T, Cam(1046, 588, W * 0.9))], "sine")
    sc.fx = [
        FX.sparkles((1420, 712, 2000, 980), count=16, color=(255, 244, 210), size=(6, 14), period=1.8, drift=0,
                    seed=3),
        # light on the open water only: below the fish's waterline, so no glint ever sits on its body
        FX.sparkles((120, FISH_WL + 22, 1380, 1040), count=10, color=(250, 252, 240), size=(5, 11), period=2.2,
                    drift=0, seed=4),
        drops_fx(fmot, t_rise0, t_rise1, T),
        FX.sparkles((300, 230, 450, 440), count=3, t0=t_done, color=(255, 240, 190), size=(9, 17), period=2.0,
                    drift=0, seed=9),
        FX.sparkles((1660, 230, 1790, 420), count=3, t0=t_done, color=(255, 240, 190), size=(9, 17), period=2.0,
                    drift=0, seed=10),
    ]
    sc.subtitles = False  # the title is already on the page

    # the sea fades out across the closing dissolve (s02 is an inland village; its first words start there)
    sc.sfx("waves_calm", 0, dur=T + 0.3, gain_db=-10, fade_in=1.0, fade_out=1.3)
    sc.sfx("gull", 0.45, gain_db=-12, pan=-0.45)
    # a soft water rush as the fish breaks the surface (softened attack; splash_small is a 'crate plop')
    sc.sfx("splash", t_rise0 + 0.05, gain_db=-18, pan=-0.1, fade_in=0.15)
    # on the ribbon (which starts 0.1 s before the voice), so the chime's attack comes before "圣"
    sc.sfx("chime", t_rib, gain_db=-10)
    return sc
