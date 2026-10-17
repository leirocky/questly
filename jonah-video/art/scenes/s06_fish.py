"""Scene 6 — Jonah is thrown into the sea, the storm stops at once, and the great fish swallows him.

Jonah 1:15-17. Tall stage (2112 x 2376): the top half is the sea surface with the ship (storm -> calm),
the bottom half is the underwater world. The camera tilts from the ship down below the waterline.

  line 0  sailors heave Jonah over the bow, he flies in an arc and splashes into the sea; at once the rain
          stops, the clouds part, the sky turns blue, the waves flatten and a golden sunbeam falls on the sea.
  line 1  camera tilts underwater: Jonah sinks with bubbles; the great fish glides in from the left.
  line 2  the fish opens its mouth wide, lunges and gulps Jonah; it wiggles happily, a burst of bubbles.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf, lerp, progress
from engine.scene import Scene

W, H = 2112, 2376
HORIZON = 690          # far horizon line
WL = 880               # near waterline (cross-section cut)
FLOOR = 2215           # top of the sandy sea floor

SX, SS = 770, 0.8      # ship anchor x (on WL) and scale
DECK = WL + PR.SHIP_DECK_Y * SS
CREW_X = [SX + 20 * SS, SX + 130 * SS, SX + 240 * SS]
CAPT_X = SX - 235 * SS

JS = 0.8               # Jonah scale (above and below water)
JAIR_ROT = 10                                  # the 'fall' pose tipped a little toward the bow
JAIR_C = (CREW_X[1] + 4, DECK - 317 * SS - 126)  # centre of the lifted Jonah (robe resting on the hands)
JAIR = (JAIR_C[0] - 1 * JS, JAIR_C[1] + 164 * JS)  # 'fall' anchor (bottom-centre) before the turn
SPLASH = (1592, WL)

FX0, FY0, FSC = 760, 1660, 0.9                 # the great fish: anchor and scale (before motion)
JB = (1470, 1690)                              # underwater Jonah: base bbox centre
JB_ANCHOR = (JB[0] - 1 * JS, JB[1] + 165 * JS)


def doc(body, defs=""):
    return S.svg_doc(body, defs=defs, w=W, h=H)


# ============================================================================ static painting


def background():
    """Clear sky, calm far sea and the whole underwater world (one flattened static layer)."""
    defs = (
        S.lin_grad("s6sky", [(0, "#7dbfdc"), (0.5, "#a9d9e6"), (0.85, "#d4ece6"), (1, "#e8f2e2")]) +
        S.rad_grad("s6sun", [(0, "#fff6d6", 0.95), (0.3, "#fff0c0", 0.6), (1, "#ffe9b0", 0)]) +
        S.lin_grad("s6far", [(0, "#c3e3e2"), (0.35, P["sea_light"]), (1, "#4f9cb8")]) +
        S.lin_grad("s6uw", [(0, "#4f9cb8"), (0.12, "#3e8dab"), (0.4, "#2f7898"), (0.75, "#276686"),
                            (1, "#1f5776")]) +
        S.lin_grad("s6sand", [(0, S.mix(P["sand"], "#5e9fb0", 0.38)), (1, S.mix(P["sand_dark"], "#2c6683", 0.55))]) +
        S.lin_grad("s6haze", [(0, "#3a86a8", 0), (1, "#2f7898", 0.55)])
    )
    b = ""
    # sky + sun
    b += f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 40}" fill="url(#s6sky)"/>'
    b += '<circle cx="1700" cy="215" r="360" fill="url(#s6sun)"/>'
    b += S.g(f'<circle cx="1700" cy="215" r="88" fill="{P["sun"]}" stroke="{S.shade(P["sun_hot"], -0.1)}" '
             f'stroke-width="4"/>', filter="wobble")
    # distant hazy headland on the left horizon
    b += S.g(S.path(S.hill(-80, 520, HORIZON + 4, 70, seed=4, bottom=HORIZON + 10, bumps=2),
                    fill=S.mix(P["sea_light"], "#c9d9cf", 0.5), sw=2.5), filter="wobble", opacity=0.85)
    # far sea surface (perspective band)
    b += f'<rect x="-20" y="{HORIZON}" width="{W + 40}" height="{WL - HORIZON + 2}" fill="url(#s6far)"/>'
    b += S.g(S.path(f"M-20,{HORIZON} L{W + 20},{HORIZON}", sw=3), filter="wobble", opacity=0.6)
    hl = ""
    for i, (x, y, w) in enumerate([(160, 720, 150), (520, 742, 210), (980, 712, 130), (1350, 735, 190),
                                    (1780, 718, 160), (300, 790, 260), (1150, 800, 240), (1900, 780, 200),
                                    (700, 840, 280), (1600, 850, 260)]):
        hl += S.path(S.wave_line(y, 3 + i % 3, w / 1.5, i, x0=x, x1=x + w), stroke=False,
                     extra=f'stroke="{P["foam"]}" stroke-width="{3 + (y - 700) / 60:.1f}" fill="none" opacity="0.7"')
    b += S.g(hl, filter="wobble")
    # underwater body
    b += f'<rect x="-20" y="{WL}" width="{W + 40}" height="{H - WL + 20}" fill="url(#s6uw)"/>'
    # rippling light under the surface
    rip = ""
    for i in range(7):
        y = WL + 45 + i * 34
        rip += S.path(S.wave_line(y, 6, 170 + 20 * i, i * 1.3, x0=-40 + (i % 2) * 90, x1=W + 40), stroke=False,
                      extra=f'stroke="#cdeeed" stroke-width="{5 - i * 0.5:.1f}" fill="none" '
                            f'opacity="{0.32 - i * 0.035:.2f}" stroke-dasharray="{90 + 15 * i} {60 + 25 * i}"')
    b += S.g(rip, filter="wobble")
    # far reefs (hazy, light) on both sides
    far_rock = S.mix("#2f7898", "#9fd0d6", 0.3)
    b += S.g(
        S.path(S.smooth_path([(-60, H + 40), (-40, 1700), (60, 1590), (190, 1560), (300, 1630), (380, 1760),
                              (470, 1900), (560, 2080), (640, H + 40)], closed=True), fill=far_rock, sw=3) +
        S.path(S.smooth_path([(1640, H + 40), (1700, 2000), (1780, 1820), (1860, 1650), (1960, 1560),
                              (2080, 1530), (2180, 1560), (2190, H + 40)], closed=True), fill=far_rock, sw=3),
        filter="wobble", opacity=0.9)
    tex = ""
    crev = S.mix("#2f7898", "#1f5776", 0.5)
    for pts in ([(60, 1650), (120, 1700), (110, 1790)], [(230, 1640), (260, 1720), (330, 1760)],
                [(80, 1900), (170, 1950), (190, 2050)], [(330, 1880), (380, 1960), (440, 2000)],
                [(1980, 1620), (1940, 1700), (1960, 1790)], [(2090, 1600), (2060, 1700), (2100, 1760)],
                [(1820, 1900), (1880, 1960), (1870, 2060)], [(2020, 1850), (1990, 1930)]):
        tex += S.path(S.smooth_path(pts, closed=False), stroke=False,
                      extra=f'stroke="{crev}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.55"')
    for cx, cy, rx, ry in ((150, 1600, 110, 26), (2040, 1575, 120, 26), (310, 1680, 60, 16), (1880, 1700, 70, 18)):
        tex += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#a9d8d8" opacity="0.32"/>'
    for cx, cy, r in ((200, 1820, 22), (90, 2000, 16), (1950, 1880, 20), (2070, 2040, 14), (420, 2120, 12)):
        tex += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.3}" ry="{r}" fill="{crev}" opacity="0.6"/>'
    b += S.g(tex, filter="wobble")
    back_weed = (PR.seaweed(150, 1600, 0.75, 0) + PR.seaweed(260, 1615, 0.6, 2) + PR.seaweed(1990, 1545, 0.8, 0) +
                 PR.seaweed(1900, 1640, 0.6, 3) + PR.seaweed(450, 1860, 0.55, 1) + PR.seaweed(1760, 1830, 0.6, 2))
    b += S.g(back_weed, opacity=0.75)
    # far kelp-forest silhouettes in the blue distance
    kelp = ""
    for i, (x, h, lean) in enumerate([(560, 520, 30), (640, 380, -20), (760, 460, 25), (1460, 420, -25),
                                      (1560, 560, 20), (1650, 400, -15), (980, 300, 15), (1250, 340, -20)]):
        y0 = FLOOR + 40
        pts = [(x + lean * math.sin(k / 5 * math.pi * 1.3) * (k / 5), y0 - h * k / 5) for k in range(6)]
        kelp += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="#3d86a0" stroke-width="{22 - i % 3 * 4}" fill="none" stroke-linecap="round" '
                             f'opacity="0.55"')
        for k in range(1, 5):
            px, py = pts[k]
            side = 1 if k % 2 else -1
            kelp += (f'<ellipse cx="{px + side * 22:.0f}" cy="{py:.0f}" rx="26" ry="10" fill="#3d86a0" '
                     f'opacity="0.55" transform="rotate({side * -30} {px + side * 22:.0f} {py:.0f})"/>')
    b += S.g(kelp, filter="wobble")
    # haze over the far reefs
    b += f'<rect x="-20" y="1450" width="{W + 40}" height="{H - 1450 + 20}" fill="url(#s6haze)"/>'
    # near reef rocks
    rock = S.mix("#2a6f8c", P["stone_dark"], 0.25)
    b += S.g(
        S.path(S.smooth_path([(-60, H + 40), (-50, 2010), (40, 1930), (170, 1900), (290, 1960), (360, 2080),
                              (420, H + 40)], closed=True), fill=rock, sw=4) +
        S.path(S.smooth_path([(1780, H + 40), (1830, 2060), (1930, 1960), (2060, 1925), (2180, 1960),
                              (2190, H + 40)], closed=True), fill=rock, sw=4), filter="wobble")
    rtex = ""
    for pts in ([(60, 1990), (110, 2040), (100, 2110)], [(250, 1960), (290, 2030)], [(1900, 2020), (1950, 2090)],
                [(2070, 1975), (2040, 2050), (2080, 2120)]):
        rtex += S.path(S.smooth_path(pts, closed=False), stroke=False,
                       extra=f'stroke="{S.shade(rock, -0.25)}" stroke-width="6" fill="none" stroke-linecap="round" '
                             f'opacity="0.6"')
    rtex += '<ellipse cx="160" cy="1918" rx="90" ry="14" fill="#9fd0d6" opacity="0.3"/>'
    rtex += '<ellipse cx="2040" cy="1940" rx="90" ry="14" fill="#9fd0d6" opacity="0.3"/>'
    b += S.g(rtex, filter="wobble")
    b += _anemone(300, 1958, 1.0, "#e9877f") + _anemone(1990, 1932, 0.9, "#f0a65a") + _anemone(120, 1925, 0.7, "#d98bc0")
    b += PR.seaweed(1860, 2010, 0.7, 1) + PR.seaweed(380, 2070, 0.6, 3)
    # sandy floor
    b += S.g(S.path(S.hill(-80, W + 80, FLOOR + 40, 60, seed=11, bottom=H + 40, bumps=4), fill="url(#s6sand)", sw=4),
             filter="wobble")
    det = ""
    for i, (x, y, r) in enumerate([(520, 2262, 16), (560, 2270, 10), (980, 2250, 13), (1210, 2268, 18),
                                    (1250, 2262, 9), (1530, 2245, 12), (850, 2300, 9), (1700, 2290, 14)]):
        det += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4}" ry="{r}" fill="{S.mix(P["stone"], "#5e9fb0", 0.35)}" ' \
               f'stroke="{P["ink"]}" stroke-width="3"/>'
    # shells and a starfish
    det += _starfish(1080, 2286, 30, "#e7926f") + _starfish(640, 2300, 22, "#f0b45c", rot=20)
    det += _shell(1400, 2290, 22) + _shell(760, 2262, 16)
    b += S.g(det, filter="wobble-fine")
    b += PR.seaweed(1000, 2240, 0.55, 2) + PR.seaweed(1460, 2236, 0.6, 1)
    return doc(b, defs)


def _starfish(cx, cy, r, col, rot=0):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + 36 * i)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.62))
    d = S.smooth_path(pts, closed=True, tension=0.55)
    dots = "".join(f'<circle cx="{cx + r * 0.5 * math.cos(math.radians(rot - 90 + 72 * i)):.1f}" '
                   f'cy="{cy + r * 0.5 * 0.62 * math.sin(math.radians(rot - 90 + 72 * i)):.1f}" r="2.5" '
                   f'fill="{S.shade(col, 0.5)}"/>' for i in range(5))
    return S.path(d, fill=col, sw=3) + dots


def _anemone(x, y, s, col):
    """Little sea anemone sitting on a rock: a squat body with a crown of rounded tentacles."""
    tips = ""
    for i in range(9):
        a = math.radians(-160 + 140 * i / 8)
        tx, ty = x + math.cos(a) * 46 * s, y - 40 * s + math.sin(a) * 40 * s
        tips += (f'<path d="M{x + math.cos(a) * 16 * s:.1f},{y - 36 * s:.1f} Q{(x + tx) / 2:.1f},{ty - 8 * s:.1f} '
                 f'{tx:.1f},{ty:.1f}" stroke="{P["ink"]}" stroke-width="{13 * s + 4:.1f}" fill="none" '
                 f'stroke-linecap="round"/>'
                 f'<path d="M{x + math.cos(a) * 16 * s:.1f},{y - 36 * s:.1f} Q{(x + tx) / 2:.1f},{ty - 8 * s:.1f} '
                 f'{tx:.1f},{ty:.1f}" stroke="{S.shade(col, 0.25)}" stroke-width="{13 * s:.1f}" fill="none" '
                 f'stroke-linecap="round"/>')
    body = (f'<path d="M{x - 26 * s:.1f},{y:.1f} Q{x - 30 * s:.1f},{y - 40 * s:.1f} {x:.1f},{y - 42 * s:.1f} '
            f'Q{x + 30 * s:.1f},{y - 40 * s:.1f} {x + 26 * s:.1f},{y:.1f} Z" fill="{col}" stroke="{P["ink"]}" '
            f'stroke-width="3.5"/>')
    return S.g(tips + body, filter="wobble-fine")


def _shell(cx, cy, r):
    d = f"M{cx - r},{cy} Q{cx - r},{cy - r * 1.3} {cx},{cy - r * 1.2} Q{cx + r},{cy - r * 1.3} {cx + r},{cy} Z"
    ribs = "".join(S.path(f"M{cx},{cy} L{cx + r * 0.85 * math.cos(math.radians(a)):.1f},"
                          f"{cy - r * 1.05 * math.sin(math.radians(a)):.1f}", sw=2)
                   for a in (35, 65, 90, 115, 145))
    return S.path(d, fill="#f3d6c4", sw=3) + ribs


def light_shafts():
    defs = S.lin_grad("s6shaft", [(0, "#f4fbe6", 0.05), (0.12, "#f4fbe6", 0.4), (0.55, "#d8f3ec", 0.16),
                                  (1, "#d8f3ec", 0)])
    b = ""
    for x, w, lean, ln in [(1180, 90, -170, 1150), (1380, 140, -200, 1300), (1640, 70, -160, 1050),
                           (1820, 120, -230, 1250), (930, 60, -120, 900), (2000, 80, -260, 1100)]:
        y0 = WL + 8
        b += (f'<path d="M{x},{y0} L{x + w},{y0} L{x + w + lean},{y0 + ln} L{x + lean - w * 0.6},{y0 + ln} Z" '
              f'fill="url(#s6shaft)"/>')
    return doc(S.g(b, filter="soft"), defs)


def clouds_clear():
    b = (S.cloud(330, 250, 420, 130, "#fbf6ec", seed=3, sw=3, shade_fill="#d8e6ea") +
         S.cloud(980, 150, 300, 95, "#fbf6ec", seed=5, sw=3, shade_fill="#d8e6ea") +
         S.cloud(1300, 360, 260, 80, "#fbf6ec", seed=8, sw=3, shade_fill="#d8e6ea") +
         S.cloud(2030, 420, 300, 90, "#fbf6ec", seed=9, sw=3, shade_fill="#d8e6ea"))
    return doc(S.g(b, filter="wobble"))


def sunbeams():
    defs = S.lin_grad("s6beam", [(0, "#fff6d2", 0.6), (0.6, "#fff3c8", 0.25), (1, "#fff3c8", 0)], x1=1, y1=0, x2=0, y2=1)
    d = ""
    for ang, wd in [(102, 7), (113, 5), (124, 8), (136, 6), (148, 9), (160, 5)]:
        a0, a1 = math.radians(ang - wd / 2), math.radians(ang + wd / 2)
        cx, cy, r0, r1 = 1700, 215, 120, 1500
        d += (f"M{cx + r0 * math.cos(a0):.1f},{cy + r0 * math.sin(a0):.1f} L{cx + r1 * math.cos(a0):.1f},"
              f"{cy + r1 * math.sin(a0):.1f} L{cx + r1 * math.cos(a1):.1f},{cy + r1 * math.sin(a1):.1f} "
              f"L{cx + r0 * math.cos(a1):.1f},{cy + r0 * math.sin(a1):.1f} Z ")
    clip = f'<clipPath id="s6abovewl"><rect x="0" y="0" width="{W}" height="{WL + 10}"/></clipPath>'
    return doc('<g clip-path="url(#s6abovewl)">' + S.g(S.path(d, fill="url(#s6beam)", stroke=False), filter="soft") +
               '<circle cx="1700" cy="215" r="200" fill="#fff6d6" opacity="0.5" filter="url(#blur-md)"/></g>',
               defs + clip)


def storm_overlay():
    """Storm sky + rough far sea; fades away when the sea calms."""
    defs = (S.lin_grad("s6ssky", [(0, P["storm_sky_top"]), (0.7, P["storm_sky"]), (1, "#74839a")]) +
            S.lin_grad("s6ssea", [(0, "#3f6275"), (1, P["storm_sea"])]))
    b = f'<rect x="-20" y="-20" width="{W + 40}" height="{HORIZON + 40}" fill="url(#s6ssky)"/>'
    b += S.g(S.path(S.wave_band(HORIZON + 4, 9, 110, 0.5, bottom=WL + 60, jitter=4, seed=2), fill="url(#s6ssea)",
                    sw=3), filter="wobble")
    caps = ""
    for i, (x, y) in enumerate([(120, 730), (420, 760), (700, 722), (1000, 790), (1320, 740), (1560, 800),
                                (1850, 735), (2020, 790), (260, 830), (1240, 845), (1780, 850), (600, 810)]):
        w = 60 + (y - 700) * 0.9
        caps += S.path(f"M{x},{y} q{w * 0.3:.0f},-{w * 0.22:.0f} {w * 0.6:.0f},-4 q{w * 0.2:.0f},6 {w * 0.4:.0f},-2",
                       stroke=False, extra=f'stroke="#dfe8ea" stroke-width="{4 + (y - 700) / 40:.1f}" fill="none" '
                                           f'opacity="0.8"')
    b += S.g(caps, filter="wobble")
    return doc(b, defs)


def storm_bank(side):
    dark, mid, light = P["storm_sky_top"], P["storm_cloud"], P["storm_cloud_light"]
    if side < 0:
        b = (S.cloud(380, 70, 900, 250, mid, seed=21, sw=4, puffs=6, shade_fill=dark) +
             S.cloud(1000, 60, 640, 220, mid, seed=22, sw=4, puffs=5, shade_fill=dark) +
             S.cloud(260, 320, 760, 250, light, seed=31, sw=4, puffs=6, shade_fill=mid) +
             S.cloud(830, 250, 620, 210, mid, seed=32, sw=4, puffs=5, shade_fill=dark))
    else:
        b = (S.cloud(1500, 50, 760, 240, mid, seed=23, sw=4, puffs=6, shade_fill=dark) +
             S.cloud(2000, 90, 600, 230, mid, seed=24, sw=4, puffs=5, shade_fill=dark) +
             S.cloud(1430, 270, 660, 220, mid, seed=33, sw=4, puffs=5, shade_fill=dark) +
             S.cloud(1920, 340, 720, 250, light, seed=34, sw=4, puffs=6, shade_fill=mid))
    return doc(S.g(b, filter="wobble"))


def near_waves(storm):
    """Translucent wave band at the waterline (the 'front' water over the ship's hull)."""
    if storm:
        amp, lam, ph, top = 30, 360, 0.4, WL - 6
        # murky storm water: nearly opaque down past the bottom of the surface shot, then fades out
        defs = S.lin_grad("s6nst", [(0, P["storm_sea_light"], 1), (0.15, P["storm_sea"], 0.97),
                                    (0.55, S.shade(P["storm_sea"], -0.08), 0.93), (0.8, P["storm_sea"], 0.8),
                                    (1, P["storm_sea"], 0)])
        fill, bottom = "url(#s6nst)", WL + 420
    else:
        amp, lam, ph, top = 7, 300, 1.0, WL
        defs = S.lin_grad("s6ncl", [(0, P["sea_light"], 0.8), (0.25, "#4f9cb8", 0.45), (1, "#4f9cb8", 0)])
        fill, bottom = "url(#s6ncl)", WL + 260
    band = S.wave_band(top, amp, lam, ph, x0=-60, x1=W + 60, bottom=bottom, jitter=3 if storm else 0, seed=3)
    b = S.path(band, fill=fill, stroke=False)
    b += S.path(S.wave_line(top, amp, lam, ph, x0=-60, x1=W + 60), sw=4.5 if storm else 4)
    if storm:
        caps = ""
        k0 = -1
        while True:
            x = lam * (k0 - 0.25 - ph / (2 * math.pi))
            k0 += 1
            if x > W + 100:
                break
            if x < -150:
                continue
            y = top - amp
            caps += S.path(f"M{x - 95:.0f},{y + 22:.0f} Q{x - 40:.0f},{y - 30:.0f} {x + 30:.0f},{y - 22:.0f} "
                           f"Q{x + 70:.0f},{y - 12:.0f} {x + 58:.0f},{y + 12:.0f} Q{x + 30:.0f},{y - 4:.0f} "
                           f"{x + 10:.0f},{y + 14:.0f} Q{x - 30:.0f},{y + 2:.0f} {x - 95:.0f},{y + 22:.0f} Z",
                           fill=P["foam"], sw=3.5)
            for j in range(3):
                caps += f'<circle cx="{x + 40 + j * 22:.0f}" cy="{y - 42 - j * 12:.0f}" r="{7 - j * 1.5:.1f}" ' \
                        f'fill="{P["foam"]}" stroke="{P["ink"]}" stroke-width="2.5"/>'
        b += caps
    else:
        b += S.path(S.wave_line(top + 16, amp * 0.8, lam, ph + 0.4, x0=-60, x1=W + 60), stroke=False,
                    extra=f'stroke="{P["foam"]}" stroke-width="5" fill="none" opacity="0.55" '
                          f'stroke-dasharray="160 90"')
    return doc(S.g(b, filter="wobble"), defs)


def splash_crown():
    x, y = SPLASH
    b = f'<ellipse cx="{x}" cy="{y + 6}" rx="200" ry="30" fill="{P["foam"]}" stroke="{P["ink"]}" stroke-width="4"/>'
    b += f'<ellipse cx="{x}" cy="{y + 2}" rx="120" ry="14" fill="{P["sea_light"]}" opacity="0.7"/>'
    petals = ""
    for i, a in enumerate((-66, -46, -26, -8, 8, 26, 46, 66)):
        h = 300 - abs(a) * 2.0 + (26 if i % 2 else 0)
        ang = math.radians(a)
        tx, ty = x + math.sin(ang) * h * 0.95, y - math.cos(ang) * h
        bx0, bx1 = x + a * 2.2 - 30, x + a * 2.2 + 30
        petals += (f'<path d="M{bx0:.0f},{y + 4} Q{(bx0 + tx) / 2 - 18:.0f},{(y + ty) / 2:.0f} {tx:.0f},{ty:.0f} '
                   f'Q{(bx1 + tx) / 2 + 18:.0f},{(y + ty) / 2:.0f} {bx1:.0f},{y + 4} Z" fill="{P["foam"]}" '
                   f'stroke="{P["ink"]}" stroke-width="4" stroke-linejoin="round"/>')
        petals += (f'<path d="M{(bx0 + bx1) / 2:.0f},{y} Q{(bx0 + tx) / 2 + 4:.0f},{(y + ty) / 2 + 10:.0f} '
                   f'{tx:.0f},{ty + 22:.0f}" stroke="{P["sea_light"]}" stroke-width="7" fill="none" opacity="0.8"/>')
        petals += (f'<circle cx="{tx + math.sin(ang) * 30:.0f}" cy="{ty - 34:.0f}" r="{12 - abs(a) / 12:.1f}" '
                   f'fill="{P["foam"]}" stroke="{P["ink"]}" stroke-width="3"/>')
    b = petals + b
    return doc(S.g(b, filter="wobble-fine"))


def splash_drops():
    x, y = SPLASH
    b = ""
    rng = np.random.default_rng(6)
    for i in range(16):
        a = math.radians(-80 + 160 * i / 15 + rng.uniform(-5, 5))
        r = rng.uniform(170, 300)
        dx, dy = math.sin(a) * r * 1.2, -math.cos(a) * r
        s = rng.uniform(8, 16)
        b += (f'<path d="M{x + dx:.0f},{y + dy - s * 1.6:.0f} Q{x + dx + s:.0f},{y + dy:.0f} {x + dx:.0f},{y + dy + s:.0f} '
              f'Q{x + dx - s:.0f},{y + dy:.0f} {x + dx:.0f},{y + dy - s * 1.6:.0f} Z" fill="{P["foam"]}" '
              f'stroke="{P["ink"]}" stroke-width="3" transform="rotate({math.degrees(a):.0f} {x + dx:.0f} {y + dy:.0f})"/>')
    return doc(S.g(b, filter="wobble-fine"))


def ripples():
    x, y = SPLASH
    b = ""
    for i, (rx, ry) in enumerate([(230, 30), (330, 44), (440, 58)]):
        b += f'<ellipse cx="{x}" cy="{y + 4 + i * 4}" rx="{rx}" ry="{ry}" fill="none" stroke="{P["foam"]}" ' \
             f'stroke-width="{7 - i * 1.5}" opacity="{0.85 - i * 0.2:.2f}"/>'
    return doc(S.g(b, filter="wobble"))


# ============================================================================ animated characters


def crew(after):
    """Captain at the stern + three sailors on deck (lifting Jonah, or praying in awe once the sea is calm)."""
    b = C.captain(CAPT_X, DECK, SS, 1, pose="stand" if after else "worried", expr="surprised" if after else None)
    poses = [("pray", "surprised"), ("pray", "surprised"), ("point", "surprised")] if after else \
        [("lift", None)] * 3
    for i, (x, (pose, ex)) in enumerate(zip(CREW_X, poses)):
        b += C.sailor(x, DECK, SS, 1, variant=[0, 1, 2][i], pose=pose, expr=ex)
    return doc(b)


def fish_frames():
    """(mouth, eye, tail) for every flipbook frame of the great fish."""
    tails = [-0.75, -0.38, 0.0, 0.38, 0.75]
    fr = [(0.0, "open", tl) for tl in tails]                         # 0-4   swim
    fr += [(m / 10, "open", 0.0) for m in range(1, 11)]               # 5-14  opening
    fr += [(0.7, "happy", 0.0), (0.4, "happy", 0.0), (0.15, "happy", 0.0)]  # 15-17 snapping shut
    fr += [(0.0, "happy", tl) for tl in tails]                        # 18-22 happy swim
    return fr


WAG = [0, 1, 2, 3, 4, 3, 2, 1]


# ============================================================================ effects


def bubble_fx(sources, seed=3):
    """All bubbles in one fx. sources: list of (emitter(t)->(x, y), t0, t1, rate, rise, size, spread, alpha)."""
    rng = np.random.default_rng(seed)
    parts = []
    for src, t0, t1, rate, rise, size, spread, alpha in sources:
        n = max(1, int((t1 - t0) * rate))
        ts = t0 + (np.arange(n) + rng.uniform(0, 1, n)) / rate
        for i in range(n):
            ex, ey = src(ts[i])
            parts.append((ts[i], ex + rng.uniform(-spread, spread), ey + rng.uniform(-spread, spread) * 0.5,
                          rng.uniform(*size), rise * rng.uniform(0.7, 1.3), rng.uniform(0, 6.3), alpha))
    arr = np.array(parts, np.float64)

    def fx(frame, t, view):
        live = arr[(arr[:, 0] <= t) & (arr[:, 0] > t - 6)]
        if not len(live):
            return frame
        pts = []
        for ts, x, y, r, sp, ph, al in live:
            age = t - ts
            yy = y - sp * age - 30 * age * age
            if yy < WL + 18:
                continue
            xx = x + 10 * math.sin(age * 4.5 + ph) * min(1, age * 2)
            fade = min(1.0, age / 0.12, (yy - WL - 18) / 60)
            ox, oy = view.to_out(xx, yy)
            rr = r * view.scale * (0.55 + 0.45 * min(1.0, age / 0.4))
            if -40 < ox < frame.size[0] + 40 and -40 < oy < frame.size[1] + 40:
                pts.append((ox, oy, rr, int(al * fade)))
        if not pts:
            return frame
        x0 = int(max(0, min(p[0] - p[2] for p in pts) - 4))
        y0 = int(max(0, min(p[1] - p[2] for p in pts) - 4))
        x1 = int(min(frame.size[0], max(p[0] + p[2] for p in pts) + 4))
        y1 = int(min(frame.size[1], max(p[1] + p[2] for p in pts) + 4))
        if x1 <= x0 or y1 <= y0:
            return frame
        ov = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for ox, oy, r, a in pts:
            ox, oy = ox - x0, oy - y0
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(215, 240, 245, a // 5),
                      outline=(236, 250, 250, a), width=max(2, int(r / 5)))
            d.ellipse([ox - r * 0.5, oy - r * 0.6, ox - r * 0.12, oy - r * 0.22], fill=(255, 255, 250, a))
        frame.alpha_composite(ov, dest=(x0, y0))
        return frame
    return fx


# ============================================================================ build


def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    L0, L1, L2 = ctx.lines[0], ctx.lines[1], ctx.lines[2]

    # ---- timing (all from the narration)
    t_heave0 = L0.start + 0.25          # sailors dip...
    t_launch = L0.start + 0.95          # ...and heave Jonah over the bow
    t_impact = L0.start + 1.7           # "...抛进海里" -> splash
    t_calm0 = L0.end - 1.5              # "海立刻平静了"
    t_calm1 = L0.end - 0.45
    t_tilt0, t_tilt1 = L0.end + 0.0, L1.start + 1.05
    t_fish0, t_fish1 = L1.start + 0.3, L1.end + 0.2
    t_see = t_fish1 - 0.55              # Jonah turns to look at the fish
    t_open0, t_open1 = L2.start - 0.15, L2.start + 0.5
    t_surge0, t_surge1 = L2.start + 0.8, L2.start + 1.08
    t_close0, t_close1 = t_surge1, t_surge1 + 0.17
    t_gulp = t_close0 + 0.07

    def storm(t):          # 1 = full storm, 0 = calm
        return 1 - progress(t, t_calm0, t_calm1, "inout")

    # ---- ship rocking: amplitude decays when the sea calms
    def ship_tf(t):
        a = 0.18 + 0.82 * storm(t)
        return Tf(dx=8 * a * math.sin(2 * math.pi * t / 3.1), dy=12 * a * math.sin(2 * math.pi * t / 2.2 + 0.6),
                  rot=4.2 * a * math.sin(2 * math.pi * t / 2.6), px=SX, py=WL)

    heave = M.keys([(t_heave0, {"dy": 0}), (t_heave0 + 0.3, {"dy": 14}), (t_launch, {"dy": -34}),
                    (t_launch + 0.35, {"dy": 0})], ["inout", "out", "inout"])

    # ---------------------------------------------------------------- layers (back to front)
    sc.add("background", background(), z=0, wc=0.8)
    # light shafts and fair-weather clouds are static: they flatten into the background (hidden by the storm)
    sc.add("shafts", light_shafts(), z=1, wc=0)
    sc.add("clouds", clouds_clear(), z=2)
    sc.add("sunbeams", sunbeams(), z=3, wc=0,
           motion=lambda t: Tf(alpha=progress(t, t_calm0 + 0.2, t_calm1 + 0.3, "sine") *
                               (0.8 + 0.2 * math.sin(2 * math.pi * t / 2.7))))
    # gulls return once the sky clears
    gull_frames = [doc(PR.gull(1880, 470, 0.55, -1, wing=w) + PR.gull(2010, 540, 0.45, -1, wing=-w * 0.8))
                   for w in (1.0, 0.0, -1.0, 0.0)]
    sc.add("gulls", gull_frames, z=4,
           motion=M.combine(M.drift(vx=-95, vy=-8, t0=t_calm0 + 0.5), M.visible(t_calm0 + 0.5, fade=0.5)),
           frame_at=lambda t: float(int(t * 7) % 4))
    sc.add("storm", storm_overlay(), z=5, motion=lambda t: Tf(alpha=storm(t)))
    for side in (-1, 1):
        sc.add(f"storm_bank{side}", storm_bank(side), z=6,
               motion=lambda t, s=side: Tf(dx=s * 1250 * progress(t, t_calm0 - 0.1, t_calm1, "sine") +
                                           s * 8 * math.sin(t * 1.3),
                                           alpha=1 - progress(t, t_calm0 + 0.15, t_calm1 - 0.15, "sine")))

    # little fish in the lower right: they dart away when the great fish arrives
    school_a = [doc(PR.small_fish(1330, 1850, 0.7, 1, "yellow", tail=tl) +
                    PR.small_fish(1250, 1905, 0.6, 1, "orange", tail=-tl) +
                    PR.small_fish(1400, 1930, 0.65, 1, "yellow", tail=-tl) +
                    PR.small_fish(1180, 1840, 0.55, 1, "orange", tail=tl)) for tl in (0.7, -0.7)]
    sc.add("school_a", school_a, z=7,
           motion=M.combine(lambda t: Tf(dx=35 * t + 900 * progress(t, t_fish1 - 0.9, t_fish1 + 0.9, "in"),
                                         dy=-60 * progress(t, t_fish1 - 0.9, t_fish1 + 0.9, "in")),
                            M.bob(10, 1.7)),
           frame_at=lambda t: float(int(t * (6 if t < t_fish1 - 0.9 else 12)) % 2))

    # ship + crew + lifted Jonah
    sc.add("ship_back", doc(PR.ship(SX, WL, SS, 1, sail="furled", part="back")), z=10, motion=ship_tf)
    sc.add("crew", [crew(False), crew(True)], z=11,
           motion=M.combine(ship_tf, lambda t: Tf(dy=0.45 * heave(t).dy)),
           frame_at=lambda t: progress(t, t_calm0 + 0.15, t_calm0 + 0.4, "sine"))
    sc.add("ship_front", doc(PR.ship(SX, WL, SS, 1, sail="furled", part="front")), z=12, motion=ship_tf)

    # Jonah's flight: rides the ship until launch, then a ballistic arc with a tumble into the sea
    st_l = ship_tf(t_launch)
    th = math.radians(st_l.rot)
    rx, ry = JAIR_C[0] - SX, JAIR_C[1] - WL
    p0 = (SX + rx * math.cos(th) - ry * math.sin(th) + st_l.dx,
          WL + rx * math.sin(th) + ry * math.cos(th) + st_l.dy + heave(t_launch).dy)
    p1 = (SPLASH[0], SPLASH[1] - 6)

    def jonah_air(t):
        if t < t_launch:
            s = ship_tf(t)
            return Tf(dx=s.dx, dy=s.dy + heave(t).dy, rot=s.rot, px=SX, py=WL)
        u = min(1.0, (t - t_launch) / (t_impact - t_launch))
        x = lerp(p0[0], p1[0], u)
        y = lerp(p0[1], p1[1], u) - 4 * 250 * u * (1 - u)
        rot = st_l.rot + 62 * progress(u, 0.15, 1.0, "inout")
        a = 1 - progress(t, t_impact - 0.04, t_impact + 0.06, "linear")
        return Tf(dx=x - JAIR_C[0], dy=y - JAIR_C[1], rot=rot, alpha=a, px=JAIR_C[0], py=JAIR_C[1])

    sc.add("jonah_air", doc(S.g(C.jonah(JAIR[0], JAIR[1], JS, 1, pose="fall"),
                                transform=f"rotate({JAIR_ROT} {JAIR_C[0]:.1f} {JAIR_C[1]:.1f})")),
           z=13, motion=jonah_air)

    # waves at the waterline: storm crests flatten into a gentle swell
    def wave_m(storm_layer):
        def m(t):
            a = storm(t)
            amp = a if storm_layer else (0.35 + 0.65 * a)
            return Tf(dx=(46 if storm_layer else 30) * amp * math.sin(2 * math.pi * t / 2.9),
                      dy=(16 if storm_layer else 5) * amp * math.sin(2 * math.pi * t / 1.7 + 0.8),
                      alpha=a if storm_layer else 1 - 0.85 * a)
        return m

    sc.add("waves_calm", near_waves(False), z=20, motion=wave_m(False))
    sc.add("waves_storm", near_waves(True), z=21, motion=wave_m(True))

    # splash
    px_, py_ = SPLASH[0], SPLASH[1] + 10
    sc.add("ripples", ripples(), z=22, motion=M.keys(
        [(t_impact + 0.15, {"sx": 0.3, "sy": 0.3, "alpha": 0}), (t_impact + 0.35, {"alpha": 0.9}),
         (t_impact + 1.6, {"sx": 1.15, "sy": 1.15, "alpha": 0})], ["out", "out"], pivot=(px_, py_)))
    sc.add("splash", splash_crown(), z=23, motion=M.keys(
        [(t_impact - 0.04, {"sx": 0.6, "sy": 0.15, "alpha": 0}), (t_impact + 0.02, {"alpha": 1}),
         (t_impact + 0.2, {"sx": 1.0, "sy": 1.0}), (t_impact + 0.75, {"sx": 1.15, "sy": 0.55, "alpha": 0.8}),
         (t_impact + 1.05, {"sx": 1.2, "sy": 0.3, "alpha": 0})], ["out", "out", "in", "linear"], pivot=(px_, py_)))
    sc.add("drops", splash_drops(), z=24, motion=M.keys(
        [(t_impact, {"s": 0.25, "alpha": 0, "dy": 0}), (t_impact + 0.06, {"alpha": 1}),
         (t_impact + 0.5, {"s": 1.05, "dy": -10}), (t_impact + 0.95, {"s": 1.25, "dy": 70, "alpha": 0})],
        ["out", "linear", "in"], pivot=(px_, py_)))

    # ---- underwater: the great fish (back part) -> Jonah -> fish (front part: lower jaw, fin)
    frames = fish_frames()

    def fish_idx(t):
        if t < t_fish1 - 0.35:       # glides in contentedly (happy eye)...
            return 18.0 + WAG[int(t * 1.8 * 8) % 8]
        if t < t_open0:              # ...then spots Jonah (open eye)
            return float(WAG[int(t * 1.6 * 8) % 8])
        if t < t_close0:
            return 5 + min(9, int(10 * progress(t, t_open0, t_open1, "out")))
        if t < t_close1:
            return 15 + min(2, int(3 * (t - t_close0) / (t_close1 - t_close0)))
        k = 2.8 if t < t_close1 + 1.0 else 1.6
        return 18 + WAG[int(t * k * 8) % 8]

    def fish_m(t):
        u = progress(t, t_fish0, t_fish1, "out")
        x = lerp(-1750, 0, u) + 40 * progress(t, t_fish1, t_surge0, "sine")
        x += 200 * progress(t, t_surge0, t_surge1, "out") + 80 * progress(t, t_close1, T, "sine")
        y = 70 * (1 - u) + 10 * math.sin(2 * math.pi * t / 2.3)
        rot = 2.0 * math.sin(2 * math.pi * t / 1.6) * (0.4 + 0.6 * (1 - progress(t, t_fish1, t_fish1 + 0.4)))
        rot -= 3.0 * (progress(t, t_surge0, t_surge0 + 0.15) - progress(t, t_close0, t_close1 + 0.1))
        sx = sy = 1.0
        if t > t_close1:
            w = math.exp(-(t - t_close1) / 0.6)
            rot += 5.5 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1))
            sy += 0.04 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1) + 1.2)
            sx -= 0.02 * w * math.sin(2 * math.pi * 2.4 * (t - t_close1) + 1.2)
            y += -14 * w * abs(math.sin(2 * math.pi * 1.2 * (t - t_close1)))
        return Tf(dx=x, dy=y, rot=rot, sx=sx, sy=sy, px=FX0, py=FY0)

    sc.add("fish_back", [doc(PR.fish(FX0, FY0, FSC, 1, mouth=m, eye=e, tail=tl, part="back"))
                         for m, e, tl in frames], z=30, motion=fish_m, frame_at=fish_idx)

    # Jonah underwater
    def jonah_path(t):
        # plunges out of the surface shot (so his face never hides behind the subtitles)...
        if t < t_impact + 0.9:
            u = progress(t, t_impact + 0.05, t_impact + 0.9, "out")
            cx, cy = lerp(SPLASH[0], 1575, u), lerp(WL + 150, WL + 460, u)
            rot = lerp(35, 6, u)
        else:                # ...and keeps sinking slowly until the fish comes
            u = progress(t, t_impact + 0.9, t_surge0, "sine")
            cx, cy = lerp(1575, JB[0], u), lerp(WL + 460, JB[1], u)
            rot = 6 * (1 - u)
        cx += 16 * math.sin(2 * math.pi * t / 2.6) * progress(t, t_impact + 0.4, t_impact + 1.2)
        rot += 5 * math.sin(2 * math.pi * t / 2.1 + 0.5)
        s = 1.0
        if t > t_surge0:     # sucked into the mouth
            f = fish_m(t_surge1)
            tx, ty = FX0 + f.dx + 300 * FSC, FY0 + f.dy + 70 * FSC
            v = progress(t, t_surge0, t_surge1 + 0.05, "in")
            cx, cy = lerp(cx, tx, v), lerp(cy, ty, v)
            rot -= 25 * v
            s = 1 - 0.32 * v
        a = progress(t, t_impact + 0.05, t_impact + 0.2, "linear") * \
            (1 - progress(t, t_close0 - 0.12, t_close0, "linear"))
        return cx, cy, rot, s, a

    def jonah_uw(t):
        cx, cy, rot, s, a = jonah_path(t)
        return Tf(dx=cx - JB[0], dy=cy - JB[1], rot=rot, sx=s, sy=s, alpha=a, px=JB[0], py=JB[1])

    uw_defs = ('<filter id="s6uwt"><feColorMatrix type="matrix" values="0.86 0.04 0.04 0 0  0.02 0.92 0.06 0 0.02  '
               '0.02 0.06 0.9 0 0.05  0 0 0 1 0"/></filter>')
    sc.add("jonah_uw", [doc(f'<g filter="url(#s6uwt)">{C.jonah(*JB_ANCHOR, JS, 1, pose="float")}</g>', uw_defs),
                        doc(f'<g filter="url(#s6uwt)">{C.jonah(*JB_ANCHOR, JS, -1, pose="float", expr="surprised")}'
                            f'</g>', uw_defs)],
           z=31, motion=jonah_uw, frame_at=lambda t: progress(t, t_see, t_see + 0.15, "linear"))
    sc.add("fish_front", [doc(PR.fish(FX0, FY0, FSC, 1, mouth=m, eye=e, tail=tl, part="front"))
                          for m, e, tl in frames], z=32, motion=fish_m, frame_at=fish_idx)

    # little fish near the floor + swaying foreground weeds
    school_b = [doc(PR.small_fish(1560, 2080, 0.55, 1, "pink", tail=tl) +
                    PR.small_fish(1480, 2130, 0.5, 1, "teal", tail=-tl) +
                    PR.small_fish(1430, 2060, 0.45, 1, "purple", tail=tl)) for tl in (0.7, -0.7)]
    sc.add("school_b", school_b, z=33, motion=M.combine(M.drift(vx=55), M.bob(8, 2.1, 0.3)),
           frame_at=lambda t: float(int(t * 5) % 2))
    # (two narrow layers instead of one full-width one: much cheaper to composite)
    weeds_l = [doc(PR.seaweed(70, H + 10, 1.5, 0, sway=s) + PR.seaweed(200, H + 10, 1.1, 2, sway=-s) +
                   PR.seaweed(330, H + 6, 0.9, 3, sway=s * 0.5)) for s in (-1.0, -0.5, 0.0, 0.5, 1.0)]
    weeds_r = [doc(PR.seaweed(1890, H + 10, 1.0, 1, sway=-s) + PR.seaweed(2020, H + 10, 1.45, 0, sway=s) +
                   PR.seaweed(1750, H + 10, 0.85, 3, sway=-s * 0.5)) for s in (-1.0, -0.5, 0.0, 0.5, 1.0)]
    sc.add("weeds_l", weeds_l, z=34, frame_at=lambda t: 2 + 2 * math.sin(2 * math.pi * t / 3.4))
    sc.add("weeds_r", weeds_r, z=35, frame_at=lambda t: 2 + 2 * math.sin(2 * math.pi * t / 3.1 + 1.0))

    # ---- camera: storm sway at the surface, then tilt below the waterline
    cam = M.cam_keys([(0, Cam(1056, 612, 1980)), (t_tilt0, Cam(1056, 612, 1980)),
                      (t_tilt1, Cam(1070, 1772, 2050)), (T, Cam(1100, 1760, 1990))], ["linear", "inout", "sine"])

    def camera(t):
        c = cam(t)
        a = storm(t)
        return Cam(c.x + 6 * a * math.sin(2 * math.pi * t / 3.3), c.y + 7 * a * math.sin(2 * math.pi * t / 2.4),
                   c.w, 0.45 * a * math.sin(2 * math.pi * t / 2.9))
    sc.camera = camera

    # ---- effects
    def jonah_mouth(t):
        cx, cy, rot, s, a = jonah_path(t)
        return cx + 40 * JS, cy - 120 * JS * s

    def fish_snout(t):
        f = fish_m(t)
        return FX0 + f.dx + 640 * FSC, FY0 + f.dy + 10 * FSC

    sc.fx = [
        FX.rain(t0=-1, t1=t_calm0 + 0.45, density=0.85, angle=16, alpha=105),
        FX.motes((0, WL + 60, W, H), count=40, t0=t_calm1, color=(214, 242, 236), size=(3, 6), alpha=80),
        # God's providence: a few warm glints in the light as the great fish arrives
        FX.sparkles((640, 1250, 1560, 1520), count=12, t0=t_fish0 + 0.3, t1=t_open0 + 0.3,
                    color=(255, 238, 180), size=(7, 14), period=1.4, drift=-8, seed=61),
        bubble_fx([
            (lambda t: (SPLASH[0], WL + 110), t_impact + 0.03, t_impact + 0.4, 70, 170, (6, 20), 80, 220),
            (jonah_mouth, t_impact + 0.3, t_surge0, 4.0, 120, (5, 13), 14, 200),
            (fish_snout, t_close0 + 0.02, t_close1 + 0.3, 45, 200, (7, 22), 30, 225),
            (fish_snout, t_close1 + 1.0, T, 2.2, 110, (5, 11), 8, 170),
        ]),
    ]

    # ---- sound
    sc.sfx("storm_wind", 0, dur=t_calm1 + 0.2, gain_db=-14, fade_in=0.8, fade_out=1.4)
    sc.sfx("rain", 0, dur=t_calm0 + 0.8, gain_db=-16, fade_in=0.8, fade_out=0.9)
    sc.sfx("waves_storm", 0, dur=t_calm1 + 0.3, gain_db=-12, fade_in=0.8, fade_out=1.5)
    sc.sfx("ship_creak", 0, dur=t_calm1, gain_db=-18, fade_in=0.8, fade_out=1.0)
    sc.sfx("thunder", 0.15, gain_db=-16, pan=-0.3)
    sc.sfx("cloth", t_launch - 0.1, gain_db=-12, pan=-0.2)
    sc.sfx("whoosh", t_launch + 0.05, gain_db=-11, pan=0.2)
    sc.sfx("splash", t_impact - 0.02, gain_db=-6, pan=0.35)
    sc.sfx("bubbles", t_impact + 0.05, dur=1.2, gain_db=-14, pan=0.3, fade_out=0.5)
    sc.sfx("waves_calm", t_calm0 - 0.2, dur=t_tilt1 - t_calm0 + 0.6, gain_db=-12, fade_in=0.9, fade_out=1.0)
    sc.sfx("chime", t_calm0 + 0.35, gain_db=-15)
    sc.sfx("gull", t_calm1 + 0.1, gain_db=-17, pan=0.5)
    sc.sfx("underwater", t_tilt0, dur=T - t_tilt0 + 0.8, gain_db=-12, fade_in=1.0, fade_out=0.8)
    sc.sfx("bubbles", t_tilt0 + 0.4, dur=t_surge0 - t_tilt0 - 0.2, gain_db=-17, pan=0.25, fade_in=0.4, fade_out=0.4)
    sc.sfx("whoosh", t_fish0 + 0.15, gain_db=-10, pan=-0.5)
    sc.sfx("gulp", t_gulp - 0.04, gain_db=-7)
    sc.sfx("bubbles", t_close1, dur=1.0, gain_db=-12, fade_out=0.5)
    return sc
