"""Scene 4 (v2) — the storm (Jonah 1:4-5).

Adapted from the approved v1 storm (art/scenes_v1/s04_storm.py: same ship, stage, sea, clouds, bolts, crew
mechanics, hold painting and dive); everything is keyed to the narration chunks.

Line 0  '但是，人怎么能躲开上帝呢？' a calm, sunny sea: the ship sails west (left) with a full sail, a wake, gulls,
        the hazy coast of Joppa behind. '船开出去不久' the coast drifts away and the first dark clouds creep in.
        '上帝就让海上刮起了狂风' the storm rises: the storm clouds roll in, the sky darkens, a squall line of dark
        crested sea sweeps in from the east (right), curly gusts, rain, the gulls flee, the sailors start
        (hard pose cuts hidden by squash-and-hop) and, after '狂风', the first lightning bolt.
Line 1  '大浪一个接着一个打过来' three breakers rise and crash one after another (stern, bow, stern): each jolts
        the ship and staggers the crew (two of them crouch and brace); '船摇来摇去' the ship pitches about
        +-12 deg; '好像就要被打碎了' a flash, the sail tears, a wave bursts over the bow, the hull creaks, the
        camera shakes.
Line 2  '水手们都吓坏了' the camera pushes in on the four terrified sailors (variants 0-3). '每个人都向自己拜的神
        求救' one after another they pray with raised hands, each toward his own side, and a thought bubble with
        his own god's sign pops up (sun, little clay idol, moon, star). '他们把船上的货物扔进海里' they heave a jar,
        a jar, a sack, a jar, a crate and a sack overboard (spinning arcs, splashes); '想让船轻一些' the
        lightened ship bobs up in the water and the tired crew catch their breath.
Line 3  '这时候，约拿在哪里呢？' the camera looks down at the closed hull while the crew pray and panic above;
        '原来' the hull opens in cutaway (Jonah asleep below the panicking crew); during '下到船舱底下' the camera
        dives into the lantern-lit hold (v1 technique); '躺在那里' Jonah sleeps on the grain sacks, breathing
        with the snore, 'Z z z'; after '呼呼大睡' the picture dips to warm dark (s05 opens in the hold out of
        the dark, as in v1, so the two drawings of the hold never double up in the dissolve).

Stage 2400 x 1350 (v1). Everything aboard shares one ship transform ``ship_tf(t)``.
"""
import math
import random
from dataclasses import replace

import numpy as np

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s04_storm as V
from art.style import P
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

W, H = V.W, V.H
INK = S.INK
SS, SF, SX, SY, PIV, DECK = V.SS, V.SF, V.SX, V.SY, V.PIV, V.DECK
GRADE_DEFS = V.GRADE_DEFS
doc, graded, ship_pt, deck_y_at = V.doc, V.graded, V.ship_pt, V.deck_y_at
apply, compose, keyc = V.apply, V.compose, V.keyc
fm = V.fm

# crew on deck (bow on the left): A v0 and D v2 work the bow side, C v3 and B v1 the stern side
AX, DX, CX, BX = 980.0, 1140.0, 1335.0, 1495.0
GRAB, LIFT, FT = 0.85, 0.32, 0.22     # carry pose this long before a release, throw pose this long before, held after


def span(line, phrases, f0, f1):
    """(start, end) of the subtitle chunk containing one of ``phrases``; falls back to fractions of the line."""
    for ph in phrases:
        for c in line.chunks:
            if ph in c.text:
                return c.start, c.end
    d = line.end - line.start
    return line.start + f0 * d, line.start + f1 * d


# ================================================================= calm-weather drawings

def calm_sky_svg():
    defs = (S.lin_grad("csky", [(0, P["sky_day_top"]), (0.5, P["sky_day"]), (0.85, "#e2efe6"), (1, "#e8f1e6")])
            + S.rad_grad("csun", [(0, "#fff7d6", 0.95), (0.25, P["glow"], 0.6), (1, P["glow"], 0)]))
    b = S.rect_bg("url(#csky)", W, H)
    b += '<circle cx="1980" cy="250" r="360" fill="url(#csun)"/>'
    b += S.g(f'<circle cx="1980" cy="250" r="84" fill="{P["sun"]}" stroke="{INK}" stroke-width="4"/>'
             '<circle cx="1952" cy="222" r="36" fill="#fff4c8" opacity="0.65"/>', filter="wobble-fine")
    return b, defs


def calm_clouds_svg():
    sh = "#e8dece"
    b = (S.cloud(380, 230, 430, 130, seed=11, shade_fill=sh) + S.cloud(1130, 130, 380, 110, seed=12, shade_fill=sh)
         + S.cloud(700, 470, 280, 86, seed=13, shade_fill=sh) + S.cloud(1560, 400, 300, 92, seed=14, shade_fill=sh)
         + S.cloud(2330, 470, 400, 116, seed=15, shade_fill=sh))
    return S.g(b, filter="wobble")


def calm_horizon_svg():
    """The hazy coast of Joppa (east, right) and the calm far sea, which also floods the lower frame."""
    haze = "#d3e6e2"
    defs = S.lin_grad("cfar", [(0, P["sea_light"]), (0.12, S.mix(P["sea_light"], P["sea"], 0.5)),
                               (0.5, P["sea"]), (1, S.mix(P["sea"], P["sea_deep"], 0.6))])
    b = ""
    hills = S.hill(1620, 2700, 706, 92, seed=3, bottom=760, bumps=3)
    b += S.path(hills, fill=S.mix(P["olive"], haze, 0.6), sw=2.5)
    r = random.Random(4)
    town = ""
    for i in range(13):
        x = 1870 + i * 40 + r.uniform(-6, 6)
        w_ = r.uniform(30, 46)
        h_ = r.uniform(24, 58) + 26 * math.sin(math.pi * i / 12)
        col = S.mix(r.choice((P["stone"], P["stone_light"], P["sand"])), haze, 0.45)
        town += (f'<rect x="{fm(x)}" y="{fm(704 - h_)}" width="{fm(w_)}" height="{fm(h_ + 6)}" fill="{col}" '
                 f'stroke="{S.mix(INK, haze, 0.45)}" stroke-width="2.5"/>')
        for k in range(int(h_ // 22)):
            town += (f'<rect x="{fm(x + w_ * 0.35)}" y="{fm(704 - h_ + 8 + 20 * k)}" width="6" height="8" '
                     f'fill="{S.mix(INK, haze, 0.5)}"/>')
    town += (f'<rect x="2410" y="600" width="26" height="104" fill="{S.mix(P["stone_light"], haze, 0.4)}" '
             f'stroke="{S.mix(INK, haze, 0.45)}" stroke-width="2.5"/>'
             f'<path d="M2404,602 L2423,580 L2442,602 Z" fill="{S.mix(P["terracotta"], haze, 0.45)}" '
             f'stroke="{S.mix(INK, haze, 0.45)}" stroke-width="2.5"/>')
    for x in (1840, 2380):
        town += (f'<path d="M{x},704 Q{x + 4},670 {x + 2},646" fill="none" stroke="{S.mix(P["wood"], haze, 0.5)}" '
                 f'stroke-width="5"/>' + S.path(S.blob(x + 2, 640, 26, 12, 0.2, 8, seed=x), fill=S.mix(P["leaf"], haze, 0.5),
                                                sw=2))
    b += S.g(town, filter="wobble-fine")
    f = V.wave_fn(706, 4, 170, 0.3, p=1.5, lean=0.2)
    d, pts = V.band_path(f, -500, W + 500, step=20)
    b += S.path(d, fill="url(#cfar)", sw=2.5)
    b += (f'<path d="{S.smooth_path([(x, y + 9) for x, y in pts], closed=False)}" fill="none" stroke="{P["sea_pale"]}" '
          f'stroke-width="6" opacity="0.6"/>')
    r = random.Random(9)
    gl = ""
    for k in range(7):
        y = 716 + 7 * k
        for _ in range(2):
            x = 1980 + r.uniform(-14 - 7 * k, 14 + 7 * k)
            gl += (f'<path d="M{fm(x - 9 - 2 * k)},{fm(y)} L{fm(x + 9 + 2 * k)},{fm(y)}" stroke="#fff6d8" stroke-width="3" '
                   f'opacity="0.85" stroke-linecap="round"/>')
    for _ in range(26):
        x, y = r.uniform(-400, W + 400), r.uniform(730, 820)
        gl += (f'<path d="M{fm(x)},{fm(y)} q{fm(14)},-5 {fm(28)},0" fill="none" stroke="#f6faf2" stroke-width="3" '
               f'opacity="0.7" stroke-linecap="round"/>')
    b += gl
    return S.g(b, filter="wobble"), defs


def calm_bg_svg():
    """Sunny sky, sun, clouds, the coast of Joppa and the calm far sea, flattened into one layer."""
    sky, d1 = calm_sky_svg()
    hor, d2 = calm_horizon_svg()
    return doc(sky + calm_clouds_svg() + hor, d1 + d2)


def calm_sea_svg(f, fill, light, dark, wl, amp, seed, x0=-160, x1=W + 160, glints=14, sw=4.0, glitter=None):
    """Gentle sunny sea band: light rim, little cream wave curls on the crests, soft glints."""
    d, pts = V.band_path(f, x0, x1)
    body = S.path(d, fill=fill, sw=sw)
    hl = S.smooth_path([(x, y + 9 + 0.3 * amp) for x, y in pts], closed=False)
    body += (f'<path d="{hl}" fill="none" stroke="{light}" stroke-width="{9 + 0.3 * amp:.1f}" opacity="0.55" '
             f'stroke-linecap="round"/>')
    r = random.Random(seed)
    curls = ""
    for xc, yc in V.crests(f, x0, x1):
        xa, xb = xc - wl * 0.16, xc + wl * 0.12
        cd = (f"M{fm(xa)},{fm(f(xa) + 4)} Q{fm(xc - wl * 0.02)},{fm(yc - 9)} {fm(xb)},{fm(f(xb) + 2)} "
              f"q{fm(-6)},{fm(-9)} {fm(-16)},{fm(-6)}")
        curls += f'<path d="{cd}" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
        curls += f'<path d="{cd}" fill="none" stroke="{P["foam"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        y = yc + amp * 1.8 + r.uniform(18, 36)
        xa, xb = xc - wl * r.uniform(0.18, 0.28), xc + wl * r.uniform(0.12, 0.25)
        body += (f'<path d="M{fm(xa)},{fm(y)} Q{fm((xa + xb) / 2)},{fm(y - 9)} {fm(xb)},{fm(y + 4)}" fill="none" '
                 f'stroke="{dark}" stroke-width="5" opacity="0.3" stroke-linecap="round"/>')
    ymax = max(y for _, y in pts)
    for _ in range(glints):
        x = r.uniform(x0 + 60, x1 - 60)
        y = f(x) + r.uniform(40, 150)
        if y < ymax + 400:
            body += (f'<path d="M{fm(x)},{fm(y)} q14,-5 30,0" fill="none" stroke="#f6faf2" stroke-width="3.5" '
                     f'opacity="0.65" stroke-linecap="round"/>')
    if glitter:   # sunlight sparkling on the water below the sun: a widening column of short bright dashes
        gx_, gy0, gy1 = glitter
        for k in range(16):
            v = k / 15
            y = gy0 + (gy1 - gy0) * v
            half = 40 + 150 * v
            for _ in range(2):
                x = gx_ + r.uniform(-half, half)
                L = r.uniform(18, 46) * (0.6 + 0.6 * v)
                body += (f'<path d="M{fm(x - L / 2)},{fm(y)} L{fm(x + L / 2)},{fm(y)}" stroke="#fff6d8" '
                         f'stroke-width="{3 + 2 * v:.1f}" opacity="0.85" stroke-linecap="round"/>')
    return S.g(body, filter="wobble") + S.g(curls, filter="wobble-fine")


def wake_svg():
    """Calm sailing: foam trailing from the stern (right) and a little bow wave (left), on the waterline."""
    sx_, sy_ = ship_pt(-470, 6)
    bx_, by_ = ship_pt(505, 4)
    out = ""
    for k, (dy, L, op) in enumerate(((2, 760, 0.95), (20, 600, 0.8), (-12, 520, 0.7))):
        pts = [(sx_ - 20 + L * u, sy_ + dy + 20 * u * (1 if k != 2 else -0.5) + 4 * math.sin(9 * u + k))
               for u in np.linspace(0, 1, 9)]
        dd = S.smooth_path(pts, closed=False)
        out += (f'<path d="{dd}" fill="none" stroke="{P["foam"]}" stroke-width="{7 - 1.5 * k:.1f}" '
                f'stroke-dasharray="{50 - 8 * k} {22 + 6 * k}" opacity="{op}" stroke-linecap="round"/>')
    circ = [(sx_ - 10 + 26 * i, sy_ + 4 + 3 * math.sin(i), 13 - 1.6 * i) for i in range(6)]
    circ += [(bx_ + 14 - 26 * i, by_ + 2 - 4 * (i == 2), 15 - 2 * i) for i in range(5)]
    out += V.puffs(circ, P["foam"], 3.0, cid="wakefoam")
    for i in range(4):
        out += (f'<circle cx="{fm(bx_ - 30 - 22 * i)}" cy="{fm(by_ - 26 - 10 * (i % 2))}" r="{5 - 0.6 * i:.1f}" '
                f'fill="{P["foam"]}" stroke="{INK}" stroke-width="2"/>')
    return doc(S.g(out, filter="wobble-fine"))


# ================================================================= storm drawings (new in v2)

def breaker_svg(x, y, s, facing, seed):
    """A big picture-book breaker rising out of the sea, its foamy lip curling over toward ``facing``.
    Anchor (x, y) = base centre on the sea surface; ~820 x 520 px at s=1 (crest ~330 px above the anchor)."""
    r = random.Random(seed)
    gid = f"brg{seed}"
    defs = S.lin_grad(gid, [(0, S.mix(P["storm_sea_light"], P["sea_light"], 0.45)), (0.35, P["storm_sea_light"]),
                            (1, P["storm_sea"])])
    back = [(-460, 110), (-360, 56), (-260, -14), (-160, -104), (-70, -192), (10, -262), (85, -308), (165, -326)]
    lip = [(240, -318), (302, -288), (342, -240), (352, -190), (338, -150)]
    under = [(316, -160), (306, -196), (282, -222), (248, -232), (216, -220), (196, -192)]
    face = [(188, -150), (194, -96), (220, -36), (276, 30), (360, 110)]
    pts = back + lip
    d = S.smooth_path(pts, closed=False) + " " + S.smooth_path([pts[-1]] + under + face, closed=False).replace("M", "L", 1)
    d += " L360,190 L-460,190 Z"
    out = f'<path d="{d}" fill="url(#{gid})" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    sh = S.smooth_path([(200, -196), (192, -150), (198, -96), (222, -40), (262, 4)], closed=False)
    out += (f'<path d="{sh}" fill="none" stroke="{S.shade(P["storm_sea"], -0.35)}" stroke-width="20" opacity="0.45" '
            f'stroke-linecap="round" transform="translate(16,0)"/>')
    gl = S.smooth_path([(150, -250), (120, -180), (118, -110), (146, -40), (196, 20)], closed=False)
    out += (f'<path d="{gl}" fill="none" stroke="{P["sea_pale"]}" stroke-width="26" opacity="0.3" '
            f'stroke-linecap="round"/>')
    for k in range(5):
        u = 0.12 + 0.17 * k
        px_, py_ = -360 + 445 * u, 56 - 364 * u
        off = r.uniform(55, 100)
        cx_, cy_ = px_ + 0.55 * off, py_ + off
        out += (f'<path d="M{fm(cx_ - 48)},{fm(cy_ + 40)} Q{fm(cx_)},{fm(cy_ - 6)} {fm(cx_ + 46)},{fm(cy_ - 38)}" '
                f'fill="none" stroke="{S.shade(P["storm_sea"], -0.3)}" stroke-width="6" opacity="0.4" '
                f'stroke-linecap="round"/>')
    for k, off in enumerate((52, 118)):
        pp = [(-360 + 445 * u + 0.6 * off, 56 - 364 * u + off + 6 * math.sin(14 * u + k))
              for u in np.linspace(0.04, 0.82, 8)]
        out += (f'<path d="{S.smooth_path(pp, closed=False)}" fill="none" stroke="{P["foam"]}" stroke-width="5" '
                f'stroke-dasharray="28 16" stroke-linecap="round" opacity="{0.6 - 0.18 * k:.2f}"/>')
    # foam cap: dense overlapping puffs along the crest and over the lip, claws dripping from the tip
    allp = back[3:] + lip
    seg = []
    for a, b in zip(allp, allp[1:]):
        for u in np.linspace(0, 1, 6, endpoint=False):
            seg.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
    seg.append(allp[-1])
    cps = []
    for i, (x_, y_) in enumerate(seg):
        u = i / (len(seg) - 1)
        rad = (10 + 22 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.8) * r.uniform(0.88, 1.1)
        cps.append((x_ + 2, y_ + 0.25 * rad, rad))
    tx, ty = lip[-1]
    for dx_, dy_, rr in ((-6, 16, 15), (-14, 34, 11), (-20, 50, 8), (14, 14, 12), (22, 30, 9), (28, 44, 6),
                         (-30, 8, 12), (-40, 22, 8)):
        cps.append((tx + dx_, ty + dy_, rr))
    out += V.puffs(cps, P["foam"], 3.5, shade=(P["sea_pale"], (150, -280, 170, 34), 0.65), cid=f"brf{seed}")
    for _ in range(9):
        cx_, cy_ = r.uniform(-40, 380), r.uniform(-410, -350)
        out += (f'<circle cx="{fm(cx_)}" cy="{fm(cy_)}" r="{r.uniform(5, 9.5):.1f}" fill="{P["foam"]}" '
                f'stroke="{INK}" stroke-width="2.5"/>')
    g_ = f'<g transform="translate({fm(x)},{fm(y)}) scale({fm(facing * s)},{fm(s)})">{out}</g>'
    return doc(S.g(g_, filter="wobble-fine"), defs)


def creak_svg(seed):
    """Comic stress strokes radiating from the straining hull (bow, stern, under the keel)."""
    r = random.Random(seed)
    ink, cream = "", ""
    for lx, ly, ang in ((525, -215, 205), (470, -70, 160), (-555, -175, -25), (-495, -65, 20)):
        x, y = ship_pt(lx, ly)
        for k in (-1, 0, 1):
            a = math.radians(ang + 28 * k + r.uniform(-5, 5))
            r0, r1 = 16 + r.uniform(0, 6), 88 + r.uniform(-8, 10) - 22 * abs(k)
            seg = (f"M{fm(x + r0 * math.cos(a))},{fm(y + r0 * math.sin(a))} "
                   f"L{fm(x + r1 * math.cos(a))},{fm(y + r1 * math.sin(a))}")
            ink += f'<path d="{seg}" fill="none" stroke="{INK}" stroke-width="17" stroke-linecap="round"/>'
            cream += f'<path d="{seg}" fill="none" stroke="#f3efe2" stroke-width="9" stroke-linecap="round"/>'
    return doc(S.g(ink + cream, filter="wobble-fine"))


def _crescent(cx, cy, R):
    """Crescent moon path: circle R minus a circle shifted up-right."""
    d2, R2 = (0.48 * R, -0.22 * R), 0.86 * R
    dist = math.hypot(*d2)
    a = (R * R - R2 * R2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(0.0, R * R - a * a))
    ux, uy = d2[0] / dist, d2[1] / dist
    mx, my = a * ux, a * uy
    p1 = (cx + mx - h * uy, cy + my + h * ux)
    p2 = (cx + mx + h * uy, cy + my - h * ux)
    return (f"M{fm(p1[0])},{fm(p1[1])} A{fm(R)},{fm(R)} 0 1 1 {fm(p2[0])},{fm(p2[1])} "
            f"A{fm(R2)},{fm(R2)} 0 0 0 {fm(p1[0])},{fm(p1[1])} Z")


def god_sign(kind, cx, cy, s):
    """The sign of a sailor's own god in his prayer bubble (gentle, simple): sun, idol, moon or star."""
    if kind == "sun":
        rays = ""
        for k in range(10):
            a = math.radians(36 * k)
            p = [(cx + 30 * s * math.cos(a - 0.2), cy + 30 * s * math.sin(a - 0.2)),
                 (cx + 46 * s * math.cos(a), cy + 46 * s * math.sin(a)),
                 (cx + 30 * s * math.cos(a + 0.2), cy + 30 * s * math.sin(a + 0.2))]
            rays += "M" + " L".join(f"{fm(x)},{fm(y)}" for x, y in p) + " Z "
        return (S.path(rays, fill=P["sun_hot"], sw=3)
                + f'<circle cx="{fm(cx)}" cy="{fm(cy)}" r="{fm(29 * s)}" fill="{P["sun"]}" stroke="{INK}" stroke-width="3.5"/>'
                + f'<circle cx="{fm(cx - 9 * s)}" cy="{fm(cy - 9 * s)}" r="{fm(10 * s)}" fill="#fff4c8" opacity="0.7"/>')
    if kind == "moon":
        return (S.path(_crescent(cx - 4 * s, cy, 38 * s), fill="#f4e3a0", sw=3.5)
                + f'<circle cx="{fm(cx - 22 * s)}" cy="{fm(cy - 6 * s)}" r="{fm(4 * s)}" fill="#e2c97c"/>')
    if kind == "star":
        pts = []
        for k in range(10):
            a = math.radians(-90 + 36 * k)
            rr = (44 if k % 2 == 0 else 19) * s
            pts.append((cx + rr * math.cos(a), cy + 4 * s + rr * math.sin(a)))
        dd = "M" + " L".join(f"{fm(x)},{fm(y)}" for x, y in pts) + " Z"
        return S.path(dd, fill=P["gold"], sw=3.5, extra='stroke-linejoin="round"')
    # a little clay household idol on a block
    clay, dark = "#c98a5c", "#a96d45"
    out = (f'<rect x="{fm(cx - 22 * s)}" y="{fm(cy + 26 * s)}" width="{fm(44 * s)}" height="{fm(14 * s)}" rx="{fm(3 * s)}" '
           f'fill="{dark}" stroke="{INK}" stroke-width="3"/>')
    body = (f"M{fm(cx - 15 * s)},{fm(cy + 27 * s)} Q{fm(cx - 19 * s)},{fm(cy - 2 * s)} {fm(cx - 9 * s)},{fm(cy - 12 * s)} "
            f"L{fm(cx + 9 * s)},{fm(cy - 12 * s)} Q{fm(cx + 19 * s)},{fm(cy - 2 * s)} {fm(cx + 15 * s)},{fm(cy + 27 * s)} Z")
    out += S.path(body, fill=clay, sw=3)
    out += (f'<path d="M{fm(cx - 10 * s)},{fm(cy + 4 * s)} Q{fm(cx)},{fm(cy + 10 * s)} {fm(cx + 10 * s)},{fm(cy + 4 * s)}" '
            f'fill="none" stroke="{INK}" stroke-width="2.5"/>')
    out += f'<circle cx="{fm(cx)}" cy="{fm(cy - 24 * s)}" r="{fm(14 * s)}" fill="{clay}" stroke="{INK}" stroke-width="3"/>'
    out += (f'<path d="M{fm(cx - 14 * s)},{fm(cy - 30 * s)} Q{fm(cx)},{fm(cy - 46 * s)} {fm(cx + 14 * s)},{fm(cy - 30 * s)}" '
            f'fill="{dark}" stroke="{INK}" stroke-width="2.5"/>')
    for ex in (-5, 5):
        out += f'<circle cx="{fm(cx + ex * s)}" cy="{fm(cy - 24 * s)}" r="{fm(2.2 * s)}" fill="{INK}"/>'
    return out


def bubble_svg(cx, cy, r, tail, kind, seed):
    """Thought / prayer bubble (soft cloud with an ink rim, two trailing dots toward the head) holding a sign."""
    rr = random.Random(seed)
    circ = [(cx, cy, 0.74 * r)]
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.3
        circ.append((cx + 0.72 * r * math.cos(a), cy + 0.5 * r * math.sin(a), 0.4 * r * rr.uniform(0.9, 1.1)))
    out = ""
    for u, k in ((0.5, 0.15), (0.76, 0.095)):
        x, y = cx + (tail[0] - cx) * u, cy + (tail[1] - cy) * u
        out += (f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(k * r)}" fill="#fbf4e2" stroke="{INK}" '
                f'stroke-width="3.5"/>')
    out += V.puffs(circ, "#fbf4e2", 4.0, shade=("#e9dcc0", (cx, cy + 0.42 * r, 0.9 * r, 0.25 * r), 0.6),
                   cid=f"bub{seed}")
    out += god_sign(kind, cx, cy - 2, r / 70)
    return doc(S.g(out, filter="wobble-fine"))


def rain_fx(k_fn, density=1.0, angle=-15, length=42, speed=1750, color=(222, 232, 242), alpha=80, width=2,
            seed=5, hole=None):
    """v1's trailing rain streaks, but with a density envelope k_fn(t) in 0..1: as the storm builds more drops
    fall (and they get a little brighter). hole(t, view) -> polygon kept free of rain (the open hold)."""
    from PIL import Image, ImageDraw

    from engine.paths import OUT_H, OUT_W
    n = int(420 * density)
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, OUT_W + 400, n)
    y0 = rng.uniform(0, OUT_H, n)
    sp = speed * rng.uniform(0.75, 1.25, n)
    ln = length * rng.uniform(0.6, 1.3, n)
    al = rng.uniform(0.55, 1.0, n)
    a = math.radians(angle)
    dx, dy = math.sin(a), math.cos(a)

    def fx(frame, t, view):
        k = float(k_fn(t))
        m = int(n * k)
        if m <= 0:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = (y0[:m] + sp[:m] * t) % (OUT_H + 80) - 40
        x = (x0[:m] + sp[:m] * t * dx / dy) % (OUT_W + 400) - 200
        aa = alpha * (0.75 + 0.25 * k)
        for i in range(m):
            d.line([(x[i], y[i]), (x[i] - ln[i] * dx, y[i] - ln[i] * dy)], fill=(*color, int(aa * al[i])), width=width)
        poly = hole(t, view) if hole else None
        if poly:
            d.polygon(poly, fill=(0, 0, 0, 0))
        frame.alpha_composite(ov)
        return frame
    return fx


# ================================================================= build

def build(ctx):
    sc = Scene(ctx, W=W, H=H)
    T = ctx.duration
    l0, l1, l2, l3 = ctx.lines[:4]

    # --------------------------------------------------- timing (all from the narration chunks)
    c_sail = span(l0, ["开出去", "不久"], 0.38, 0.58)
    c_wind = span(l0, ["狂风", "刮起"], 0.58, 1.0)
    c_waves = span(l1, ["一个接着一个", "大浪"], 0.0, 0.67)
    c_break = span(l1, ["打碎", "好像"], 0.68, 1.0)
    c_scare = span(l2, ["吓坏"], 0.0, 0.19)
    c_pray = span(l2, ["求救", "自己"], 0.2, 0.5)
    c_throw = span(l2, ["扔进海里", "货物"], 0.51, 0.8)
    c_light = span(l2, ["轻一些", "想让"], 0.8, 1.0)
    c_where = span(l3, ["在哪里", "这时候"], 0.0, 0.3)
    c_below = span(l3, ["船舱底下", "原来"], 0.31, 0.84)
    c_sleep = span(l3, ["呼呼大睡", "大睡"], 0.85, 1.0)

    T_WIND = c_wind[0]                               # the storm rises
    T_REACT = T_WIND + 1.1                           # the crew notice it (hard cuts) as the light changes
    WIPE = (T_WIND + 0.3, T_WIND + 2.45)             # squall line sweeps in from the east (right)
    S1 = l0.end + 0.15                               # first bolt, after '狂风'
    wv = c_waves[1] - c_waves[0]
    HITS = [(c_waves[0] + 0.12 * wv + 0.3, "stern", 1.0), (c_waves[0] + 0.38 * wv, "bow", 1.05),
            (c_waves[0] + 0.62 * wv, "stern", 1.2)]  # breakers: (crash time, side, size)
    S2 = c_break[0] + 0.02                           # '好像就要被打碎了': flash, the sail tears, bow crash
    T_TEAR = S2 + 0.03
    T_CRASH = S2 + 0.12
    S3 = c_scare[0] + 0.1                            # '吓坏了'
    S4 = l2.end + 0.3
    STRIKES = [(S1, 0.36), (S2, 0.45), (S3, 0.3), (S4, 0.24)]
    pr0 = c_pray[0]
    T_PRAY = {"A": pr0 + 0.12, "D": pr0 + 0.42, "C": pr0 + 0.72, "B": pr0 + 1.02}
    r0 = c_throw[0] + 0.75
    REL = {"A1": r0, "B1": r0 + 0.45, "D1": r0 + 0.9, "C1": r0 + 1.35, "A2": r0 + 1.95, "B2": r0 + 2.4}
    T_LIGHT = max(REL["B2"] + 0.5, c_light[0] + 0.3)  # the lightened ship bobs up
    T_L3 = l3.start - 0.25                            # crew back to praying / panicking
    T_CUT = (c_below[0] + 0.05, c_below[0] + 0.55)   # '原来': the hull opens
    T_DIVE0 = T_CUT[1] + 1.1                         # dive during '下到船舱底下'
    T_DIVE1 = T_DIVE0 + 1.45
    T_REV = (T_DIVE0 + 0.4, T_DIVE0 + 0.95)
    T_IN = T_REV[1]
    T_HATCH = [T_IN + 0.45, max(T_IN + 1.4, c_sleep[0] + 0.25)]
    T_BLACK = (max(T_DIVE1 + 0.6, T - 1.45), T - 0.95)   # dark as the 1.0 s dissolve into s05 begins

    # --------------------------------------------------- ship motion
    grade = lambda t: M.progress(t, T_REACT - 0.9, T_REACT + 0.9, "sine")       # noqa: E731  calm -> storm light
    wipe = lambda t: M.progress(t, *WIPE, "inout")                              # noqa: E731
    pitch_amp = keyc([(0, 1.3), (T_WIND, 1.5), (T_WIND + 1.6, 4.5), (l0.end, 8.0), (l1.start + 0.2, 9.0),
                      (c_waves[0] + 0.7 * wv, 12.0), (l1.end, 11.0), (l2.start + 0.9, 6.0), (c_throw[0], 5.5),
                      (T_CUT[0], 5.0), (T_DIVE1, 3.2), (T, 2.8)])
    bob_amp = keyc([(0, 5), (T_WIND, 6), (l0.end, 22), (l1.start, 27), (l1.end, 30), (l2.start + 0.9, 16),
                    (T_CUT[0], 14), (T_DIVE1, 8), (T, 7)])
    freq = keyc([(0, 1 / 4.0), (T_WIND, 1 / 3.7), (l0.end, 1 / 2.6), (l1.start, 1 / 2.25), (l1.end, 1 / 2.25),
                 (l2.start + 0.9, 1 / 2.9), (T_CUT[0], 1 / 3.4), (T, 1 / 3.8)])
    phase = V.integrate(freq, -1.0, T + 1.0)
    sea_amp = keyc([(0, 0.5), (T_WIND, 0.55), (l0.end, 1.0), (l1.end, 1.15), (l2.start + 0.5, 0.9), (T, 0.85)])
    lift = keyc([(T_LIGHT, 0.0), (T_LIGHT + 0.55, -26.0), (T_LIGHT + 1.2, -17.0)], ["out", "sine"])
    JOLT = {"stern": -1, "bow": 1}

    def jolts(t):
        v = 0.0
        for th, side, sz in HITS:
            if t >= th:
                v += JOLT[side] * 3.6 * sz * math.exp(-(t - th) / 0.45) * math.sin(7.5 * (t - th))
        if t >= T_CRASH:
            v -= 3.0 * math.exp(-(t - T_CRASH) / 0.4) * math.sin(8 * (t - T_CRASH))
        return v

    def ship_tf(t):
        ph = 2 * math.pi * phase(t)
        rot = pitch_amp(t) * math.sin(ph) + jolts(t)
        dy = bob_amp(t) * math.sin(ph - 1.3) + lift(t)
        dx = 0.35 * bob_amp(t) * math.sin(0.5 * ph + 0.4)
        return Tf(dx, dy, rot, 1, 1, 1, PIV[0], PIV[1])

    def on_ship(local):
        return lambda t: compose(ship_tf(t), local(t))

    def wave_motion(by, sx_, k_ph, k_sw=0.0, lag=0.0, drop=None):
        def m(t):
            a = sea_amp(t)
            ph = 2 * math.pi * phase(t - lag)
            return Tf(dx=sx_ * a * math.sin(0.5 * ph + k_sw),
                      dy=by * a * math.sin(ph + k_ph) + (drop(t) if drop else 0.0))
        return m

    calm_vis = lambda t: 1 - M.progress(t, WIPE[1] - 0.2, WIPE[1] + 0.25, "sine")   # noqa: E731

    def calm_motion(by, sx_, per, ph0):
        def m(t):
            u = 2 * math.pi * (t / per + ph0)
            return Tf(dx=sx_ * math.sin(0.5 * u), dy=by * math.sin(u), alpha=calm_vis(t))
        return m

    storm_reveal = lambda t: {"mode": "right", "frac": wipe(t), "soft": 340}           # noqa: E731
    calm_reveal = lambda t: {"mode": "left", "frac": min(1.0, 1.04 - wipe(t)), "soft": 340}   # noqa: E731

    # --------------------------------------------------- sky: storm (beneath), calm (fades away)
    sky_defs = (S.lin_grad("sky", [(0, P["storm_sky_top"]), (0.5, P["storm_sky"]),
                                   (0.8, S.mix(P["storm_sky"], P["sea_pale"], 0.3)), (1, P["storm_sea_light"])])
                + S.lin_grad("seab", [(0, S.mix(P["storm_sea_light"], P["storm_sky"], 0.3)), (0.3, P["storm_sea_light"]),
                                      (1, S.shade(P["storm_sea"], -0.2))]))
    sky = S.rect_bg("url(#sky)", W, H)
    sky += S.g("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="0.5"/>' for x, y, rx, ry, c in (
        (400, 250, 560, 170, P["storm_cloud"]), (1300, 170, 680, 160, P["storm_sky_top"]),
        (2050, 290, 560, 180, P["storm_cloud"]), (900, 480, 560, 100, P["storm_cloud_light"]),
        (1800, 500, 520, 100, P["storm_cloud_light"]))), filter="blur-md")
    sky += S.g("".join(f'<path d="M{x},340 L{x + 170},340 L{x + 60},720 L{x - 110},720 Z" fill="{P["storm_cloud"]}" '
                       f'opacity="0.3"/>' for x in (240, 1060, 1960)), filter="blur-md")
    sea_base = f'<rect x="-20" y="668" width="{W + 40}" height="{H}" fill="url(#seab)"/>'
    f_far = V.wave_fn(705, 15, 250, 0.4, p=1.6, lean=0.25)
    far_sea = V.sea_layer(f_far, S.mix(P["storm_sea_light"], P["storm_sky"], 0.22), P["sea_pale"], P["storm_sea"],
                          250, 15, 1, foam_size=0.5, sw=3, x1=W + 80)
    far = ""
    for i, (x, y, w_, h_) in enumerate(((250, 615, 440, 105), (760, 585, 540, 125), (1350, 620, 480, 100),
                                        (1900, 590, 580, 125), (2330, 620, 400, 95))):
        far += V.storm_cloud(x, y, w_, h_, 20 + i, P["storm_cloud_light"],
                             S.mix(P["storm_cloud"], P["storm_sky"], 0.3), "#a9b4c4", sw=3)
    sc.add("sky", doc(sky + sea_base + S.g(far, filter="wobble") + far_sea, sky_defs), wc=0.7,
           motion=lambda t: Tf(alpha=float(t >= T_WIND - 0.1)))      # hidden under the opaque calm sky

    sky_fade = lambda t: 1 - M.progress(t, T_WIND - 0.1, l0.end - 0.3, "sine")        # noqa: E731
    sc.add("calm_bg", calm_bg_svg(), wc=0.7,
           motion=lambda t: Tf(dx=9 * t + 18 * M.progress(t, c_sail[0], c_sail[1] + 1.0, "sine"), alpha=sky_fade(t)))

    # gulls glide around the mast in the sun and flee as the wind rises
    gull_frames = lambda gx_, gy_, s_: [doc(PR.gull(gx_, gy_, s_, -1, wing=w)) for w in (1, 0.5, 0, -0.5, -1)]  # noqa
    cyc = [0, 1, 2, 3, 4, 3, 2, 1]
    for i, (gx_, gy_, s_, path_, flap0, ph0) in enumerate((
            (640, 330, 0.85, [(0, (0, 0)), (T_WIND + 0.2, (-150, -18)), (T_WIND + 1.9, (-1000, -420))], 1.8, 0.0),
            (1720, 300, 0.72, [(0, (0, 0)), (T_WIND + 0.4, (-120, 10)), (T_WIND + 2.2, (-700, -520))], 3.1, 0.4))):
        def gm(t, path_=path_, ph0=ph0, i=i):
            (t0, a), (t1, b), (t2, c) = path_
            if t <= t1:
                u = M.progress(t, t0, t1, "linear")
                x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
                y += 16 * math.sin(2 * math.pi * (t / 3.4 + ph0))
                x += 22 * math.sin(2 * math.pi * (t / 6.8 + ph0))
            else:
                u = M.progress(t, t1, t2, "in")
                x0_ = b[0] + 22 * math.sin(2 * math.pi * (t1 / 6.8 + ph0))
                y0_ = b[1] + 16 * math.sin(2 * math.pi * (t1 / 3.4 + ph0))
                x, y = x0_ + (c[0] - x0_) * u, y0_ + (c[1] - y0_) * u
            return Tf(x, y, -6 * M.progress(t, t1, t1 + 0.5) + 3 * math.sin(t * 1.3 + i), 1, 1,
                      1 - M.progress(t, t2 - 0.3, t2, "sine"), gx_, gy_)

        def gf(t, flap0=flap0, t1=path_[1][0]):
            if t > t1:                                      # hard flapping into the wind
                return float(cyc[int((t - t1) * 16) % 8])
            ph = (t - flap0) % 4.2                          # a few flaps, then a long glide
            return float(cyc[int(ph * 10) % 8]) if ph < 1.2 else 2.0
        sc.add(f"gull{i}", gull_frames(gx_, gy_, s_), wc=0.4, motion=gm, frame_at=gf)

    # --------------------------------------------------- storm clouds roll in, bolts behind them
    CL = ((160, 160, 720, 270), (650, 100, 780, 250), (420, 370, 840, 240), (1060, 270, 620, 200))
    CR = ((2240, 150, 780, 280), (1750, 95, 720, 240), (1960, 370, 840, 230), (1390, 230, 580, 190))
    t_in = l0.end + 0.25
    m_left = M.combine(M.keys([(0, {"dx": -1330, "dy": -80}), (c_sail[0] + 0.3, {"dx": -1300, "dy": -78}),
                               (T_WIND + 0.4, {"dx": -1000, "dy": -50}), (t_in, {"dx": 0, "dy": 0})],
                              ["linear", "in", "out"]),
                       M.drift(vx=6), M.bob(6, 5.0))
    m_right = M.combine(M.keys([(0, {"dx": 1300, "dy": -70}), (c_sail[0] + 0.3, {"dx": 1270, "dy": -68}),
                                (T_WIND + 0.5, {"dx": 960, "dy": -44}), (t_in + 0.3, {"dx": 0, "dy": 0})],
                               ["linear", "in", "out"]),
                        M.drift(vx=-5), M.bob(7, 4.4, 0.3))
    bolt_spec = [(m_left, CL[3], -0.3, 700, -1), (m_right, CR[2], 0.05, 770, -1), (m_left, CL[2], 0.25, 760, -1),
                 (m_right, CR[0], -0.28, 650, 1)]
    bolts = []
    for (ts, _), (mm, (cx, cy, cw, ch), fr, y1, sway) in zip(STRIKES, bolt_spec):
        mv = mm(ts)
        bolts.append((cx + fr * cw + mv.dx, cy + 0.5 * ch - 50 + mv.dy, y1, sway))
    for i, ((ts, _), (bx, by0, by1, sway)) in enumerate(zip(STRIKES, bolts)):
        sc.add(f"bolt{i}", doc(V.bolt_svg(bx, by0, by1, seed=7 + i, sway=sway), V.BOLT_DEFS), wc=0,
               motion=(lambda ts_: lambda t: Tf(alpha=V.bolt_alpha(t - ts_)))(ts))
    cl, cr = P["storm_cloud"], S.mix(P["storm_cloud"], P["storm_cloud_light"], 0.3)
    under, rim = S.mix(P["storm_sky_top"], INK, 0.25), "#9aa6ba"
    left = "".join(V.storm_cloud(x, y, w_, h_, 40 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CL))
    right = "".join(V.storm_cloud(x, y, w_, h_, 60 + i, (cl, cr)[i % 2], under, rim) for i, (x, y, w_, h_) in enumerate(CR))
    sc.add("clouds_left", doc(S.g(left, filter="wobble")), wc=0.9, motion=m_left)
    sc.add("clouds_right", doc(S.g(right, filter="wobble")), wc=0.9, motion=m_right)

    gusts = [(T_WIND + 0.15, 1550, 330, 520), (T_WIND + 0.75, 700, 470, 480), (T_WIND + 1.35, 1950, 470, 440),
             (T_WIND + 1.85, 1100, 250, 640), (T_WIND + 2.35, 520, 300, 520), (l1.start + 0.25, 450, 330, 460),
             (l1.start + 0.85, 1750, 400, 520), (c_break[0] + 0.4, 1350, 260, 560), (l2.start + 0.6, 600, 420, 460),
             (c_throw[0] - 0.4, 1900, 330, 480), (c_where[0] + 0.3, 700, 380, 520)]
    for i, (tg, gx_, gy_, gl) in enumerate(gusts):
        sc.add(f"gust{i}", doc(S.g(V.wind_svg(gx_, gy_, gl, seed=30 + i), filter="wobble-fine")), wc=0,
               motion=(lambda tg_: M.combine(
                   M.keys([(tg_, {"dx": 260, "alpha": 0}), (tg_ + 0.25, {"alpha": 0.95}), (tg_ + 0.95, {"alpha": 0.95}),
                           (tg_ + 1.3, {"dx": -380, "alpha": 0})], "linear"),
                   lambda t: Tf(dy=10 * math.sin(4 * t))))(tg))

    # --------------------------------------------------- sea behind the ship: calm, then the storm sweeps in
    f_cmid = V.wave_fn(852, 10, 420, 0.8, p=1.6, lean=0.2)
    sc.add("calm_mid", doc(calm_sea_svg(f_cmid, S.mix(P["sea"], P["sea_light"], 0.35), P["sea_pale"], P["sea_deep"],
                                        420, 10, 21, glitter=(2010, 880, 975))),
           wc=0.9, motion=calm_motion(4, 10, 3.9, 0.1), reveal=calm_reveal)
    f_mid = V.wave_fn(850, 52, 580, 1.3, p=2.2)
    sc.add("sea_mid", doc(V.sea_layer(f_mid, S.mix(P["storm_sea_light"], P["storm_sea"], 0.3), P["sea_light"],
                                      P["storm_sea"], 580, 52, 2, foam_size=0.85)),
           wc=1.0, reveal=storm_reveal,
           motion=M.combine(wave_motion(18, 34, -0.4, 0.5, lag=0.25), lambda t: Tf(alpha=float(t >= WIPE[0]))))

    # --------------------------------------------------- the ship (back), crew, cargo, ship (front)
    ox0, oy0, ox1, oy1 = V.opening_rect()
    coil_x = ship_pt(-36, -165)[0]

    def ship_back(sail, cut, storm=True):
        base = (PR.ship(SX, SY, SS, SF, sail=sail, cutaway=cut, part="back", flag=False)
                + PR.rope_coil(coil_x, DECK + 2, SS * 0.85))
        out = graded(base) if storm else base
        if cut:   # the lantern-lit hold stays warm
            out += (f'<clipPath id="holdwarm"><rect x="{ox0 + 9:.1f}" y="{oy0 + 9:.1f}" width="{ox1 - ox0 - 18:.1f}" '
                    f'height="{oy1 - oy0 - 14:.1f}" rx="30"/></clipPath><g clip-path="url(#holdwarm)">{base}</g>')
        return doc(out, GRADE_DEFS)
    cutf = lambda t: M.progress(t, *T_CUT, "sine")                          # noqa: E731
    sc.add("ship_back", [ship_back("full", False, False), ship_back("full", False), ship_back("torn", False),
                         ship_back("torn", True)],
           motion=ship_tf, frame_at=lambda t: grade(t) + float(t >= T_TEAR) + cutf(t))

    for nm, stormy, fps, vis in (("pennant_calm", False, 4, lambda t: 1 - grade(t)), ("pennant", True, 9, grade)):
        flags = []
        for ph in (0.0, 1.6, 3.2):
            pts = [ship_pt(*q) for q in V.pennant_pts(ph)]
            mk = S.g(S.path(S.smooth_path(pts, closed=True, tension=0.6), fill=P["sail_stripe"], sw=3.5),
                     filter="wobble-fine")
            flags.append(doc(graded(mk) if stormy else mk, GRADE_DEFS))
        sc.add(nm, flags, frame_at=(lambda fps_: lambda t: float(int(t * fps_) % 3))(fps),
               motion=(lambda vis_: lambda t: replace(ship_tf(t), alpha=vis_(t)))(vis))

    # scraps of sail torn off at the flash, flying away downwind (left) in tumbling arcs
    st_tear = ship_tf(T_TEAR)
    for i, (lx, ly, dxe, peak, drop, spin, dur, s) in enumerate((
            (292, -790, -520, 70, 60, -420, 0.75, 1.7), (300, -690, -430, 30, 150, 380, 0.65, 1.35),
            (318, -610, -600, 55, 110, -300, 0.8, 1.5))):
        x0_, y0_ = apply(st_tear, *ship_pt(lx, ly))

        def scrap_m(t, x0_=x0_, y0_=y0_, dxe=dxe, peak=peak, drop=drop, spin=spin, dur=dur, i=i):
            if t < T_TEAR or t > T_TEAR + dur:
                return Tf(alpha=0.0, px=x0_, py=y0_)
            u = (t - T_TEAR) / dur
            xo = dxe * (1 - (1 - u) ** 2)
            yo = -4 * peak * u * (1 - u) + drop * u * u
            return Tf(xo, yo, spin * u, 0.55 + 0.45 * abs(math.cos(9 * u + i)), 1.0,
                      1 - M.progress(u, 0.6, 1.0, "sine"), x0_, y0_)
        sc.add(f"scrap{i}", doc(graded(S.g(V.scrap_svg(x0_, y0_, 90 + i, s), filter="wobble-fine")), GRADE_DEFS),
               wc=0.5, motion=scrap_m)

    # snore cue -> Jonah's breathing (chest highest at the end of each inhale of the actual sound)
    snore_at = round(T_CUT[0] + 0.25, 3)
    peaks = []
    for k in range(8):   # choose a variation whose inhale falls inside the hold, before the scene's dissolve
        at_k = round(snore_at + 0.07 * k, 3)
        pk = V.snore_inhale_peaks(ctx.id, at_k, round(T + 0.6 - at_k, 3))
        if not pk or any(T_IN + 0.15 <= p <= T_BLACK[0] for p in pk):
            snore_at, peaks = at_k, pk
            break
    else:
        peaks = V.snore_inhale_peaks(ctx.id, snore_at, round(T + 0.6 - snore_at, 3))
    snore_dur = round(T + 0.6 - snore_at, 3)
    breath = V.breath_curve(peaks)

    # sleeping Jonah inside the cutaway hold (small; the hold painting takes over during the dive)
    jx_c, jy_c = ship_pt(*PR.SHIP_SLEEP)
    sc.add("jonah_cut", doc(C.jonah(jx_c, jy_c, SS, -1, pose="sleep", marks=False)),
           motion=on_ship(lambda t: Tf(0, 0, 0, 1 + 0.006 * breath(t), 1 + 0.024 * breath(t),
                                       cutf(t) * (1 - M.progress(t, T_REV[0] + 0.02, T_REV[0] + 0.18, "sine")),
                                       jx_c, jy_c)))

    hcx, hcy = jx_c + 136 * SS, jy_c - 79 * SS          # cutaway Jonah's head (facing -1)
    for i in range(3):
        zc = doc(S.text(hcx + 34, hcy - 34, "Z", size=40, fill="#fff3d6",
                        extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))

        def zcm(t, i=i):
            per_ = 1.5
            t0 = T_CUT[1] + 0.1 + 0.5 * i
            if t < t0:
                return Tf(alpha=0.0, px=hcx + 34, py=hcy - 44)
            u = ((t - t0) % per_) / per_
            a = (min(1.0, u / 0.15) * (1 - M.progress(u, 0.55, 1.0, "sine"))
                 * (1 - M.progress(t, T_REV[0] - 0.2, T_REV[0] + 0.1, "sine")))
            s_ = 0.55 + 0.6 * u
            return Tf(10 + 34 * u, -8 - 46 * u, -10 + 18 * u, s_, s_, a, hcx + 34, hcy - 44)
        sc.add(f"zc{i}", zc, wc=0, motion=on_ship(zcm))

    # ---- crew choreography: (time, pose, expr, facing, storm-graded, hop?) per sailor
    def throws_ev(names, facing, after):
        ev = []
        for k, nm in enumerate(names):
            tr = REL[nm]
            ev += [(tr - GRAB, "carry", None, facing, True, k == 0), (tr - LIFT, "throw", None, facing, True, False),
                   (tr + FT, "carry", None, facing, True, False)]
        ev.append((REL[names[-1]] + 0.62, "stand", "tired", facing, True, True))
        return ev

    h1 = HITS[0][0]
    EV = {
        "A": [(0, "point", "happy", -1, False, False), (T_REACT, "point", "surprised", -1, True, True),
              (S1 + 0.05, "scared", None, -1, True, True), (h1 - 0.12, "carry", "worried", -1, True, True),
              (S2 + 0.05, "scared", None, -1, True, True), (T_PRAY["A"], "pray", None, -1, True, True)]
             + throws_ev(["A1", "A2"], -1, None) + [(T_L3, "scared", None, -1, True, True)],
        "D": [(0, "stand", "happy", 1, False, False), (T_REACT + 0.12, "stand", "worried", -1, True, True),
              (S1 + 0.1, "scared", None, -1, True, True), (T_PRAY["D"], "pray", None, -1, True, True)]
             + throws_ev(["D1"], -1, None) + [(T_L3 + 0.1, "pray", None, -1, True, True)],
        "C": [(0, "stand", "neutral", -1, False, False), (T_REACT + 0.06, "stand", "worried", 1, True, True),
              (S1 + 0.12, "scared", None, 1, True, True), (T_PRAY["C"], "pray", None, 1, True, True)]
             + throws_ev(["C1"], 1, None) + [(T_L3 + 0.05, "pray", None, 1, True, True)],
        "B": [(0, "stand", "happy", -1, False, False), (T_REACT + 0.18, "stand", "worried", 1, True, True),
              (S1 + 0.08, "scared", None, 1, True, True), (h1 - 0.08, "carry", "worried", 1, True, True),
              (S2 + 0.08, "scared", None, 1, True, True), (T_PRAY["B"], "pray", None, 1, True, True)]
             + throws_ev(["B1", "B2"], 1, None) + [(T_L3 - 0.05, "scared", None, 1, True, True)],
    }
    CREW = {"A": (AX, 0, -1, ["A1", "A2"]), "D": (DX, 2, -1, ["D1"]), "C": (CX, 3, 1, ["C1"]),
            "B": (BX, 1, 1, ["B1", "B2"])}

    def heave_keys(throws):
        """Forward lean (deg, + = toward the sea) and vertical squash for a sailor's throws."""
        lk, lc, sk, scv = [(0.0, 0.0)], [], [(0.0, 1.0)], []
        for tr in throws:
            lk += [(tr - LIFT, 0.0), (tr - 0.08, -8.0), (tr + 0.06, 12.0), (tr + 0.5, 0.0)]
            lc += ["linear", "sine", "out", "back"]
            tg = tr - GRAB
            sk += [(tg - 0.001, 1.0), (tg, 0.95), (tg + 0.26, 1.0)]
            scv += ["linear", "linear", "out"]
        return keyc(lk, lc), keyc(sk, scv)

    def hop_fn(cuts):
        """Squash-and-hop that sells a hard pose cut: anticipation squash, cut, a little hop, settle."""
        def f(t):
            dy, sy = 0.0, 1.0
            for tc in cuts:
                if tc - 0.09 <= t < tc:
                    sy *= 1 - 0.06 * M.progress(t, tc - 0.09, tc, "sine")
                elif tc <= t < tc + 0.32:
                    u = (t - tc) / 0.32
                    dy -= 12 * math.sin(math.pi * min(1.0, u * 1.25))
                    sy *= 1 + 0.045 * math.sin(math.pi * u) - 0.06 * (1 - u) ** 3
            return dy, sy
        return f

    hit_dir = {"stern": -1, "bow": 1}

    def stagger(t, seed):
        v = 0.0
        for th, side, sz in HITS:
            if t >= th:
                v += hit_dir[side] * 4.5 * sz * math.exp(-(t - th) / 0.35) * math.sin(10 * (t - th) + 0.2 * seed)
        if t >= T_CRASH:
            v += 4.0 * math.exp(-(t - T_CRASH) / 0.35) * math.sin(10 * (t - T_CRASH) + 0.2 * seed)
        return v

    actors, layers_z = {}, {}

    def make_actor(key):
        x, var, tf_face, names = CREW[key]
        ev = sorted(EV[key], key=lambda e: e[0])
        lean, squash = heave_keys([REL[n] for n in names])
        hop = hop_fn([e[0] for e in ev[1:] if e[5]])
        grab0 = REL[names[0]] - GRAB
        last = REL[names[-1]]
        seed = ord(key)
        tamp = keyc([(S1, 0.0), (S1 + 0.25, 2.0), (c_scare[0], 2.0), (c_scare[0] + 0.25, 3.2),
                     (T_PRAY[key], 3.2), (T_PRAY[key] + 0.35, 1.1), (grab0 - 0.1, 1.1), (grab0, 0.0),
                     (last + 0.62, 0.0), (last + 0.9, 0.6), (T_L3, 0.6), (T_L3 + 0.3, 2.0)], "linear")
        pray_iv = []
        for i, e in enumerate(ev):
            if e[1] == "pray":
                pray_iv.append((e[0], ev[i + 1][0] if i + 1 < len(ev) else 1e9))

        def m(t):
            a = tamp(t)
            ddx, ddy = a * math.sin(t * 47 + seed), 0.4 * a * math.sin(t * 31 + seed)
            hdy, hsy = hop(t)
            sy = squash(t) * hsy * (1 + 0.006 * math.sin(2 * math.pi * t / 3.1 + seed))
            rot = tf_face * lean(t) + stagger(t, seed)
            for p0, p1 in pray_iv:          # praying: a slow imploring sway
                if p0 <= t < p1:
                    rot += 1.6 * M.progress(t, p0, p0 + 0.5, "sine") * math.sin(2 * math.pi * (t - p0) / 2.3 + seed)
            return Tf(ddx, ddy + hdy, rot, 1 + 0.5 * (1 - sy), sy, 1.0, x, DECK)
        actors[key] = m

        frames, keys_, idx = [], {}, []
        for e in ev:
            k = e[1:5]
            if k not in keys_:
                keys_[k] = len(frames)
                mk = C.sailor(x, DECK, SS, e[3], variant=var, pose=e[1], expr=e[2])
                frames.append(doc(graded(mk) if e[4] else mk, GRADE_DEFS))
            idx.append(keys_[k])
        times = [e[0] for e in ev[1:]]
        return frames, (lambda t: float(idx[sum(t >= ts for ts in times)]))

    def carry_over(sx, facing, variant):
        hc = C.hand_positions(C.sailor, sx, DECK, SS, facing, variant=variant, pose="carry")
        ht = C.hand_positions(C.sailor, sx, DECK, SS, facing, variant=variant, pose="throw")
        return (((hc[0][0] + hc[1][0]) / 2, (hc[0][1] + hc[1][1]) / 2 - 6),
                ((ht[0][0] + ht[1][0]) / 2, (ht[0][1] + ht[1][1]) / 2))

    z_crew = len(sc.layers) + len(sc.dynamics)
    for key in ("C", "D", "A", "B"):
        frames, fa = make_actor(key)
        sc.add(f"sailor_{key}", frames, motion=on_ship(actors[key]), frame_at=fa)

    # the sea surface in front of the ship (for splash timing): near-wave function + its motion
    gx = lambda x: min(1.0, abs(x - SX) / 950) ** 1.4                        # noqa: E731
    f_near = V.wave_fn(lambda x: 1004 - 75 * gx(x), lambda x: 16 + 100 * gx(x), 600, 0.75, p=2.0, lean=0.3)
    near_drop = lambda t: 115 * M.progress(t, T_CUT[0] - 0.1, T_CUT[1] + 0.15, "inout")   # noqa: E731
    near_m = wave_motion(22, 46, 0.3, 2.0, lag=0.1, drop=near_drop)

    def surface(x, t):
        m = near_m(t)
        return f_near(x - m.dx) + m.dy

    # cargo: rests on deck -> grabbed (carry) -> overhead (throw) -> released in a spinning arc -> splash
    splashes = []

    def cargo(name, svg, rest, carry, over, t_rel, land, spin, half_h, act, fly=0.72, peak=170, z=None):
        t_grab, t_up = t_rel - GRAB, t_rel - LIFT
        top = (over[0], over[1] - half_h + 12)

        def local_pos(t):
            if t < t_grab:
                return rest
            if t < t_up:
                u = M.progress(t, t_grab, t_grab + 0.12, "out")
                return (rest[0] + (carry[0] - rest[0]) * u, rest[1] + (carry[1] - rest[1]) * u)
            return top

        def held(t):
            p = local_pos(t)
            inner = Tf(p[0] - rest[0], p[1] - rest[1], 0, 1, 1, 1, rest[0], rest[1])
            if t >= t_grab:
                inner = compose(act(t), inner)
            return compose(ship_tf(t), inner)

        rel_tf = held(t_rel)
        sx_, sy_ = apply(rel_tf, *rest)
        rot0 = rel_tf.rot

        def make_path(lx):
            return lambda u: (sx_ + (lx - sx_) * u, sy_ + (land[1] - sy_) * u - 4 * peak * u * (1 - u))

        def hit(pth):
            for i in range(60, 200):
                tt = t_rel + fly * i / 160
                x, y = pth(i / 160)
                if y >= surface(x, tt):
                    return tt, y
            return t_rel + fly, 9e9

        best = None
        for lx in np.arange(land[0] - 110, land[0] + 111, 20):
            tt, y = hit(make_path(lx))
            score = y + 0.5 * abs(lx - land[0])
            if best is None or score < best[0]:
                best = (score, lx, tt)
        _, lx_best, t_hit = best
        path = make_path(lx_best)
        hx_, _ = path((t_hit - t_rel) / fly)

        def m(t):
            if t < t_rel:
                return held(t)
            u = (t - t_rel) / fly
            if t > t_hit + 0.35:
                return Tf(alpha=0.0, px=rest[0], py=rest[1])
            x, y = path(u)
            return Tf(x - rest[0], y - rest[1], rot0 + spin * u, 1, 1, 1, rest[0], rest[1])
        sc.add(name, [doc(svg), doc(graded(svg), GRADE_DEFS)], motion=m, z=z, frame_at=grade)
        splashes.append((t_hit, hx_, surface(hx_, t_hit) + 10, name))

    A_carry, A_over = carry_over(AX, -1, 0)
    D_carry, D_over = carry_over(DX, -1, 2)
    C_carry, C_over = carry_over(CX, 1, 3)
    B_carry, B_over = carry_over(BX, 1, 1)
    a_cr = (AX + 45, deck_y_at(AX + 45) - 37)
    a_jar = (AX + 112, deck_y_at(AX + 112) - 51)
    d_sack = (DX + 44, deck_y_at(DX + 44) + 2)
    c_jar = (C_carry[0] - 8, deck_y_at(C_carry[0] - 8) - 50)
    b_jar = (B_carry[0], deck_y_at(B_carry[0]) - 53)
    b_sack = (BX - 52, deck_y_at(BX - 52) + 2)
    cargo("cargo_A2", PR.crate(*a_cr, 0.78), a_cr, A_carry, A_over, REL["A2"], (560, 1130), -320, 40, actors["A"],
          z=z_crew - 0.6)
    cargo("cargo_A1", PR.jar(*a_jar, 0.62), a_jar, A_carry, A_over, REL["A1"], (660, 1120), -400, 52, actors["A"],
          z=z_crew - 0.5)
    cargo("cargo_D1", PR.sack(*d_sack, 0.6, seed=9), d_sack, (D_carry[0], D_carry[1] + 32), (D_over[0], D_over[1] + 40),
          REL["D1"], (470, 1110), -280, 40, actors["D"], peak=310, fly=0.85, z=z_crew - 0.4)
    cargo("cargo_C1", PR.jar(*c_jar, 0.6, color=S.mix(P["terracotta"], P["sand"], 0.15)), c_jar, C_carry, C_over,
          REL["C1"], (2010, 1110), 360, 52, actors["C"], peak=310, fly=0.85, z=z_crew - 0.3)
    cargo("cargo_B1", PR.jar(*b_jar, 0.66, color=S.mix(P["terracotta"], P["sand"], 0.35)), b_jar, B_carry, B_over,
          REL["B1"], (1860, 1120), 380, 55, actors["B"])
    cargo("cargo_B2", PR.sack(*b_sack, 0.62, seed=6), b_sack, (B_carry[0], B_carry[1] + 32),
          (B_over[0], B_over[1] + 40), REL["B2"], (1960, 1130), 300, 40, actors["B"])

    # front of the ship; its stern lantern stays warm
    lan = PR.lantern(*ship_pt(-428, -372), 0.85 * SS)
    front = PR.ship(SX, SY, SS, SF, sail="torn", part="front", lantern=False)
    sc.add("ship_front", [doc(front + lan), doc(graded(front) + lan, GRADE_DEFS)], motion=ship_tf, frame_at=grade)

    # the hull strains: stress marks flicker around it while it '好像就要被打碎了'
    t_cr = (T_CRASH + 0.1, c_break[1] - 0.1)
    sc.add("creak", [creak_svg(1), creak_svg(2)], wc=0, frame_at=lambda t: float(int(t * 9) % 2),
           motion=lambda t: replace(ship_tf(t), alpha=M.progress(t, t_cr[0], t_cr[0] + 0.15)
                                    * (1 - M.progress(t, t_cr[1] - 0.3, t_cr[1], "sine"))
                                    * (0.75 + 0.25 * math.sin(t * 23))))

    # prayer bubbles: each sailor's own god's sign (sun, little idol, moon, star)
    BUB = {"A": ("sun", -70, -175, 72), "D": ("idol", -30, -215, 70), "C": ("moon", 40, -205, 70),
           "B": ("star", 70, -172, 72)}
    for key, (kind, ox, oy, rad) in BUB.items():
        x, var, _, names = CREW[key]
        f_ = next(e[3] for e in EV[key] if e[1] == "pray")
        head = C.body_points(C.sailor, x, DECK, SS, f_, variant=var, pose="pray")["head"]
        cx_, cy_ = head[0] + ox, head[1] + oy
        tail = (head[0] + 0.25 * ox, head[1] - 60)
        tb, te = T_PRAY[key] + 0.22, REL[names[0]] - GRAB - 0.05

        def bm(t, tb=tb, te=te, cx_=cx_, cy_=cy_, ph=ord(key)):
            if t < tb or t > te:
                return Tf(alpha=0.0, px=cx_, py=cy_)
            k = M.progress(t, tb, tb + 0.38, "back")
            s = 0.3 + 0.7 * k
            a = min(1.0, (t - tb) / 0.1) * (1 - M.progress(t, te - 0.32, te, "sine"))
            return Tf(3 * math.sin(t * 1.9 + ph), -5 * math.sin(2 * math.pi * (t - tb) / 2.2), 0, s, s, a, cx_, cy_ + 30)
        sc.add(f"bubble_{key}", bubble_svg(cx_, cy_, rad, tail, kind, ord(key)), wc=0.4, motion=on_ship(bm))

    # --------------------------------------------------- sea in front of the ship: calm (+ wake), then storm
    f_cnear = V.wave_fn(985, 8, 470, 0.3, p=1.6, lean=0.25)
    sc.add("calm_near", doc(calm_sea_svg(f_cnear, S.mix(P["sea"], P["sea_deep"], 0.15), P["sea_light"],
                                         P["sea_deep"], 470, 8, 22)),
           wc=0.9, motion=calm_motion(4, 14, 3.6, 0.35), reveal=calm_reveal)
    sc.add("wake", wake_svg(), wc=0.5, boil=4,
           motion=lambda t: Tf(dx=0.3 * ship_tf(t).dx, dy=0.7 * ship_tf(t).dy,
                               alpha=1 - M.progress(t, WIPE[0] + 0.4, WIPE[0] + 1.2, "sine")))

    # breakers: '大浪一个接着一个打过来' — they rise beside the stern / bow, curl in and crash
    for i, (th, side, sz) in enumerate(HITS):
        face = -1 if side == "stern" else 1
        st_h = ship_tf(th)
        tip = apply(st_h, *ship_pt(-405, -225)) if side == "stern" else apply(st_h, *ship_pt(390, -235))
        surge = 70.0
        bx_ = tip[0] - face * (345 * sz + surge)
        by_ = tip[1] + 175 * sz
        base_y = max(by_, 975.0)
        by_ = base_y

        def brm(t, th=th, face=face, bx_=bx_, by_=by_):
            if t < th - 0.85 or t > th + 0.7:
                return Tf(alpha=0.0, px=bx_, py=by_ + 60)
            rise = M.progress(t, th - 0.85, th - 0.1, "out")
            c = M.progress(t, th, th + 0.55, "in")
            sy = (0.12 + 0.88 * rise) * (1 - 0.62 * c)
            sx = 0.75 + 0.25 * rise
            dx = face * (surge * M.progress(t, th - 0.85, th, "inout") + 90 * c)
            a = M.progress(t, th - 0.85, th - 0.68) * (1 - M.progress(t, th + 0.12, th + 0.6, "sine"))
            return Tf(dx, 8 * math.sin(4 * t), face * 7 * c, sx, sy, a, bx_, by_ + 60)
        sc.add(f"breaker{i}", breaker_svg(bx_, by_, sz, face, 70 + i), wc=0.8, motion=brm)

    sc.add("sea_near", doc(V.sea_layer(f_near, P["storm_sea"], P["storm_sea_light"], S.shade(P["storm_sea"], -0.3),
                                       600, 70, 3, foam_size=1.0, cap_amp=lambda x: 16 + 100 * gx(x))),
           wc=1.0, reveal=storm_reveal, motion=M.combine(near_m, lambda t: Tf(alpha=float(t >= WIPE[0]))))

    for i, (ts, x, y, _) in enumerate(splashes):
        sc.add(f"splash{i}", doc(V.burst(x, y, 0.75, seed=i, lean=(-12 if x < SX else 12))), wc=0.5,
               motion=(lambda ts_, x_, y_: M.keys([(ts_ - 0.01, {"sy": 0.1, "sx": 0.5, "alpha": 0}),
                                                   (ts_, {"alpha": 1}),
                                                   (ts_ + 0.2, {"sy": 1.0, "sx": 1.0}),
                                                   (ts_ + 0.45, {"sy": 0.92, "sx": 1.08, "alpha": 0.95}),
                                                   (ts_ + 0.85, {"sy": 0.3, "sx": 1.2, "alpha": 0})],
                                                  ["linear", "out", "sine", "in"], pivot=(x_, y_ + 10)))(ts, x, y))

    # breaker crashes: spray bursting over the stern / bow, fanning away from the crew
    for i, (th, side, sz) in enumerate(HITS):
        st_h = ship_tf(th)
        px_, py_ = apply(st_h, *ship_pt(-500, -185)) if side == "stern" else apply(st_h, *ship_pt(505, -190))
        lean = 40 if side == "stern" else -40
        sc.add(f"hitspray{i}", doc(V.burst(px_, py_, 1.05 * sz, seed=40 + i, n=6, spread=46, height=150, lean=lean)),
               wc=0.5,
               motion=(lambda th_, x_, y_: M.keys([(th_ - 0.01, {"sy": 0.15, "sx": 0.6, "alpha": 0}), (th_, {"alpha": 1}),
                                                   (th_ + 0.25, {"sy": 1.0, "sx": 1.0}),
                                                   (th_ + 0.65, {"sy": 0.95, "sx": 1.1, "alpha": 0.95}),
                                                   (th_ + 1.1, {"sy": 0.3, "sx": 1.2, "alpha": 0})],
                                                  ["linear", "out", "sine", "in"], pivot=(x_, y_ + 10)))(th, px_, py_))

    # a big wave bursting over the bow as the ship nearly breaks
    bx, by = ship_pt(455, -60)
    sc.add("bow_crash", doc(V.burst(bx - 40, by + 40, 1.7, seed=12, n=6, spread=48, height=150, lean=-32)), wc=0.5,
           motion=M.keys([(T_CRASH - 0.01, {"sy": 0.15, "sx": 0.6, "alpha": 0}), (T_CRASH, {"alpha": 1}),
                          (T_CRASH + 0.28, {"sy": 1.0, "sx": 1.0}),
                          (T_CRASH + 0.75, {"sy": 0.95, "sx": 1.1, "alpha": 0.95}),
                          (T_CRASH + 1.3, {"sy": 0.3, "sx": 1.2, "alpha": 0})],
                         ["linear", "out", "sine", "in"], pivot=(bx - 40, by + 50)))

    f_cfg = V.wave_fn(1266, 12, 520, 0.7, p=1.6, lean=0.25)
    sc.add("calm_fg", doc(calm_sea_svg(f_cfg, S.mix(P["sea_deep"], P["sea"], 0.35), P["sea_light"], P["sea_deep"],
                                       520, 12, 23, glints=8)),
           wc=0.9, motion=M.combine(calm_motion(5, 18, 3.3, 0.6),
                                    lambda t: Tf(alpha=1 - M.progress(t, WIPE[0] + 0.5, WIPE[1] - 0.2, "sine"))))
    f_fg = V.wave_fn(1262, 36, 540, 0.7, p=1.8, lean=0.3)
    sc.add("sea_fg", doc(V.sea_layer(f_fg, S.shade(P["storm_sea"], -0.18), P["storm_sea_light"],
                                     S.shade(P["storm_sea"], -0.45), 540, 36, 4, foam_size=0.8)),
           wc=1.0,
           motion=M.combine(wave_motion(12, 30, 1.6, 3.0, lag=-0.15, drop=lambda t: 1.4 * near_drop(t)),
                            lambda t: Tf(alpha=M.progress(t, WIPE[0] + 0.5, WIPE[1] - 0.2, "sine"))))

    # --------------------------------------------------- the dive: the outside darkens around the hull opening
    dim_d = (f"M-20,-20 H{W + 20} V{H + 20} H-20 Z "
             f"M{ox0 + 10:.1f},{oy0 + 10:.1f} H{ox1 - 10:.1f} V{oy1 - 12:.1f} H{ox0 + 10:.1f} Z")
    dim_a = lambda t: (0.74 * M.progress(t, T_DIVE0 + 0.1, T_REV[0] + 0.08, "sine")      # noqa: E731
                       + 0.24 * M.progress(t, T_REV[0] + 0.08, T_REV[0] + 0.24, "sine"))
    sc.add("dim", doc(f'<path d="{dim_d}" fill="#24150d" fill-rule="evenodd" filter="url(#blur-md)"/>'), wc=0,
           motion=lambda t: replace(ship_tf(t), alpha=dim_a(t)))

    # --------------------------------------------------- the hold painting, attached to the ship at scale K
    K, Q0, J_PAINT = V.K, V.Q0, V.J_PAINT
    H0 = (jx_c - K * (J_PAINT[0] - Q0[0]), jy_c - K * (J_PAINT[1] - Q0[1]))
    place = Tf(H0[0] - Q0[0], H0[1] - Q0[1], 0, K, K, 1, Q0[0], Q0[1])

    def to_paint(x, y):
        return Q0[0] + (x - H0[0]) / K, Q0[1] + (y - H0[1]) / K

    def in_hold(local=None):
        def m(t):
            base = compose(ship_tf(t), place)
            return compose(base, local(t)) if local else base
        return m

    jx, jy = J_PAINT
    rc = (jx + 130, jy - 120)
    px0, py0 = to_paint(ox0, oy0)
    px1, py1 = to_paint(ox1, oy1)
    full_a = lambda t: M.progress(t, T_REV[0] + 0.28, T_REV[1] - 0.03, "sine")        # noqa: E731
    stages = [((14, 14, 10), 0.0, 0.15), ((-190, -150, 50), 0.08, 0.25), ((-520, -400, 120), 0.17, 0.36)]
    t_off = [T_REV[0] + 0.26, T_REV[0] + 0.37, T_REV[1]]
    for i, ((ix, iy, fe), a0, a1) in enumerate(stages):
        sc.add(f"hold_r{i}", V.hold_svg(clip=(px0 + ix, py0 + iy, px1 - ix, py1 - iy, fe)), wc=1.0, seed=101,
               motion=in_hold(lambda t, a0=a0, a1=a1, off=t_off[i]: Tf(
                   alpha=M.progress(t, T_REV[0] + a0, T_REV[0] + a1, "sine") * (t < off),
                   px=Q0[0], py=Q0[1])))
    sc.add("hold", V.hold_svg(), wc=1.0, seed=101, motion=in_hold(lambda t: Tf(alpha=full_a(t), px=Q0[0], py=Q0[1])))

    fade_in = lambda t: M.progress(t, T_REV[0] + 0.02, T_REV[0] + 0.18, "sine")       # noqa: E731
    sc.add("jonah", doc(C.jonah(jx, jy, V.JS, -1, pose="sleep", marks=False)),
           motion=in_hold(lambda t: Tf(0, 0, 0, 1 + 0.006 * breath(t), 1 + 0.024 * breath(t), fade_in(t), jx, jy)))

    lhx, lhy = V.LANTERN_HOOK
    swing = lambda t: 8 * math.sin(2 * math.pi * t / 3.1 + 0.6) - 0.6 * ship_tf(t).rot     # noqa: E731
    glow = f'<ellipse cx="{lhx + 60}" cy="{lhy + 400}" rx="600" ry="520" fill="url(#lg2)"/>'
    sc.add("lamp_glow", doc(glow, S.rad_grad("lg2", [(0, "#ffd890", 0.5), (0.35, "#ffc870", 0.22), (1, "#ffc060", 0)])),
           wc=0, blend="add",
           motion=in_hold(lambda t: Tf(0, 0, swing(t), 1, 1,
                                       full_a(t) * (0.85 + 0.1 * math.sin(t * 7.3) + 0.05 * math.sin(t * 12.1)),
                                       lhx, lhy)))
    sc.add("lantern", doc(f'<line x1="{lhx}" y1="{lhy - 10}" x2="{lhx}" y2="{lhy + 44}" stroke="{INK}" stroke-width="5"/>'
                          + PR.lantern(lhx, lhy + 34, 1.5)),
           motion=in_hold(lambda t: Tf(0, 0, swing(t), 1, 1, full_a(t), lhx, lhy)))

    # Z z z drifting up from the sleeper's head; one Z rises right on '呼呼大睡'
    head = (jx + 240, jy - 140)
    per = 2.25
    t_z0 = c_sleep[0] - 0.1
    while t_z0 - per / 3 >= T_REV[0] + 0.2:
        t_z0 -= per / 3
    for i, delay in enumerate((0.0, per / 3, 2 * per / 3)):
        zsvg = doc(S.text(head[0] + 50, head[1] - 50, "Z", size=84, fill="#fff3d6",
                          extra=f'stroke="{INK}" stroke-width="8" paint-order="stroke"'))

        def zm(t, delay=delay):
            if t < t_z0 + delay:
                return Tf(alpha=0.0, px=head[0], py=head[1])
            u = ((t - t_z0 - delay) % per) / per
            a = min(1.0, u / 0.15) * (1 - M.progress(u, 0.6, 1.0, "sine")) * full_a(t)
            s = 0.45 + 0.75 * u
            return Tf(70 + 190 * u + 26 * math.sin(u * 6.0), -30 - 330 * u, -12 + 22 * u, s, s, a,
                      head[0] + 50, head[1] - 70)
        sc.add(f"z{i}", zsvg, wc=0, motion=in_hold(zm))

    # drips from the hatch, rain boiling in the hatch and cold flickers through it (the storm still rages above)
    hx0 = V.HATCH[0]
    drop = (f'<path d="M{hx0 + 150},312 Q{hx0 + 162},336 {hx0 + 150},344 Q{hx0 + 138},336 {hx0 + 150},312 Z" '
            f'fill="{P["sea_pale"]}" stroke="{INK}" stroke-width="3"/>')
    for i in range(2):
        def dm(t, i=i):
            per_ = 1.3
            if t < T_REV[0]:
                return Tf(alpha=0.0, px=hx0 + 150, py=320)
            u = ((t + i * 0.65) % per_) / per_
            return Tf(0, 790 * u * u, 0, 1, 1, min(1.0, u / 0.1) * (1 - M.progress(u, 0.85, 1.0)) * full_a(t),
                      hx0 + 150, 320)
        sc.add(f"drip{i}", doc(drop), wc=0, motion=in_hold(dm))
    sc.add("hatch_rain", [V.hatch_rain_svg(s) for s in (1, 2, 3)], wc=0,
           motion=in_hold(lambda t: Tf(alpha=full_a(t), px=Q0[0], py=Q0[1])), frame_at=lambda t: float(int(t * 11) % 3))
    HX, HY = V.HATCH, V.HATCH_Y
    flash = (f'<path d="M{HX[0] + 20},296 L{HX[1] - 20},296 L{HX[1] + 200},1110 L{HX[0] + 20},1110 Z" '
             f'fill="#9fb6e0" opacity="0.45" filter="url(#blur-lg)"/>'
             f'<ellipse cx="{(HX[0] + HX[1]) / 2}" cy="{(HY[0] + HY[1]) / 2}" rx="260" ry="150" '
             f'fill="#c8d6f0" opacity="0.8" filter="url(#blur-md)"/>')
    sc.add("hatch_flash", doc(flash), wc=0, blend="add",
           motion=in_hold(lambda t: Tf(alpha=max(0.65 * V.flick(t - T_HATCH[0]), 0.42 * V.flick(t - T_HATCH[1])),
                                       px=Q0[0], py=Q0[1])))

    bloom = f'<circle cx="{rc[0]}" cy="{rc[1]}" r="1150" fill="url(#bl)"/>'
    sc.add("bloom", doc(bloom, S.rad_grad("bl", [(0, "#ffd890", 0.17), (0.45, "#f6b860", 0.1), (1, "#f0a050", 0)])),
           wc=0, blend="add",
           motion=in_hold(lambda t: Tf(alpha=M.progress(t, T_REV[0] - 0.1, T_REV[0] + 0.4, "sine")
                                       * (1 - M.progress(t, T_REV[0] + 0.45, T_REV[1] + 0.35, "sine")),
                                       px=Q0[0], py=Q0[1])))

    # --------------------------------------------------- camera
    CAM_CONTRAST = Cam(1225, 795, 1350)   # crew panicking on deck above, Jonah asleep in the open hold below
    cam_ext = M.cam_keys([
        (0, Cam(1215, 690, 2170)), (T_WIND, Cam(1212, 686, 2140)), (l0.end + 0.3, Cam(1208, 680, 2120)),
        (l1.end, Cam(1210, 678, 2110)), (c_scare[0] - 0.1, Cam(1212, 676, 2100)),
        (c_scare[0] + 1.4, Cam(1232, 632, 1480)),           # '水手们都吓坏了': close on the crew
        (c_pray[0] + 1.6, Cam(1238, 604, 1450)),            # a little higher for the prayer bubbles
        (c_throw[0] - 0.15, Cam(1236, 610, 1470)),
        (c_throw[0] + 1.15, Cam(1225, 682, 1800)),          # wider for the splashes
        (l2.end + 0.2, Cam(1225, 690, 1840)), (c_where[0] + 0.1, Cam(1225, 690, 1840)),
        (c_where[0] + 2.0, Cam(1228, 768, 1500)),           # '约拿在哪里呢？' look down at the hull
        (T_CUT[0], Cam(1228, 772, 1490)), (T_DIVE0 + 0.4, CAM_CONTRAST)],
        ["inout"] * 9 + ["sine", "inout", "sine", "inout"])
    cam_ext = M.cam_shake(cam_ext, amp=15, t0=c_break[0] - 0.02, t1=l1.end + 0.1, freq=7.5, seed=3)
    for i, (th, _, sz) in enumerate(HITS):
        cam_ext = M.cam_shake(cam_ext, amp=7 * sz, t0=th - 0.02, t1=th + 0.6, freq=9, seed=11 + i)
    cam_ext = M.cam_shake(cam_ext, amp=5, t0=S1, t1=S1 + 0.7, freq=9, seed=5)
    cam_ext = M.cam_shake(cam_ext, amp=6, t0=S3, t1=S3 + 0.7, freq=9, seed=8)

    def camera(t):
        u = M.progress(t, T_DIVE0, T_DIVE1, "inout")
        if u <= 0:
            return cam_ext(t)
        st = ship_tf(t)
        hx, hy = apply(compose(st, place), *V.V0)
        ce = cam_ext(t)
        w_end = V.VIEW_W_INT * K * (1 - 0.04 * M.progress(t, T_DIVE1, T, "sine"))
        w = math.exp(math.log(ce.w) + (math.log(w_end) - math.log(ce.w)) * u)   # even-feeling zoom
        return Cam(ce.x + (hx - ce.x) * u, ce.y + (hy - ce.y) * u, w, ce.rot + (0.7 * st.rot - ce.rot) * u)
    sc.camera = camera

    # cull the outside world once the hold covers the frame (render time)
    def view_in_painting(t, margin=72):
        cam = camera(t)
        tf = compose(ship_tf(t), place)
        hw, hh = cam.w / 2, cam.w * 9 / 32
        cr_, sr_ = math.cos(math.radians(cam.rot)), math.sin(math.radians(cam.rot))
        r = math.radians(tf.rot)
        for ax, ay in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
            x, y = cam.x + cr_ * ax - sr_ * ay, cam.y + sr_ * ax + cr_ * ay
            ox_, oy_ = apply(tf, tf.px, tf.py)
            dx_, dy_ = x - ox_, y - oy_
            qx = tf.px + (math.cos(r) * dx_ + math.sin(r) * dy_) / K
            qy = tf.py + (-math.sin(r) * dx_ + math.cos(r) * dy_) / K
            if not (margin <= qx <= W - margin and margin <= qy <= H - margin):
                return False
        return True

    t_cull = T + 1
    for t in np.arange(T_IN, T + 0.001, 1 / 30):
        if all(view_in_painting(tt) for tt in np.arange(t, T + 0.001, 1 / 30)):
            t_cull = float(t)
            break
    inside = {"bloom", "hold_r0", "hold_r1", "hold_r2", "hold", "jonah", "lamp_glow", "lantern", "hatch_flash",
              "hatch_rain", "z0", "z1", "z2", "drip0", "drip1"}
    t_hidden = T_REV[0] + 0.26
    for lay in sc.layers:
        if lay.name in inside or lay.motion is None:
            continue

        def culled(t, m0=lay.motion, tc=(t_cull if lay.name == "dim" else min(t_cull, t_hidden))):
            return Tf(alpha=0.0) if t > tc else m0(t)
        lay.motion = culled
    # calm-weather layers: gone once the storm has swept in
    for lay in sc.layers:
        if lay.name in ("calm_bg", "calm_mid", "calm_near", "calm_fg", "wake",
                        "pennant_calm", "gull0", "gull1"):
            def gone(t, m0=lay.motion, tg=l0.end + 0.6):
                return Tf(alpha=0.0) if t > tg else m0(t)
            lay.motion = gone

    # --------------------------------------------------- effects
    def hold_region(t):
        st = compose(ship_tf(t), place)
        x0, y0 = apply(st, 750, 330)
        x1, y1 = apply(st, 1650, 1000)
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    def rain_hole(t, view):
        if t < T_CUT[0] + 0.2:
            return None
        st = ship_tf(t)
        return [view.to_out(*apply(st, x, y)) for x, y in ((ox0, oy0), (ox1, oy0), (ox1, oy1), (ox0, oy1))]

    rain_k = keyc([(T_WIND + 1.0, 0.0), (T_WIND + 1.6, 0.4), (l0.end - 0.3, 0.45), (l0.end + 0.5, 1.0),
                   (T_REV[0] - 0.25, 1.0), (T_REV[0] + 0.35, 0.0)], "sine")
    sc.fx = [rain_fx(rain_k, density=0.95, angle=-16, seed=5, hole=rain_hole),
             V.flash_fx(STRIKES), V.motes_fx(hold_region, 24, T_IN - 0.3), V.dip_fx(*T_BLACK)]
    sc.meta = dict(STRIKES=STRIKES, HITS=HITS, REL=REL, T_PRAY=T_PRAY, splashes=[s[:3] for s in splashes],
                   T_CUT=T_CUT, T_DIVE0=T_DIVE0, T_DIVE1=T_DIVE1, T_REV=T_REV, T_IN=T_IN, T_HATCH=T_HATCH,
                   T_CRASH=T_CRASH, T_TEAR=T_TEAR, T_LIGHT=T_LIGHT, T_REACT=T_REACT, WIPE=WIPE, T_BLACK=T_BLACK,
                   t_cull=t_cull, snore=(snore_at, snore_dur, peaks), ship_tf=ship_tf, camera=camera, bolts=bolts,
                   t_z0=t_z0)

    # --------------------------------------------------- sound
    sc.sfx("waves_calm", 0, dur=T_WIND + 2.2, gain_db=-12, fade_in=0.8, fade_out=1.6)
    sc.sfx("wind_soft", 0, dur=T_WIND + 1.2, gain_db=-17, fade_in=0.8, fade_out=1.2)
    sc.sfx("gull", 1.1, gain_db=-15, pan=-0.4)
    sc.sfx("gull", 3.4, gain_db=-17, pan=0.45)
    sc.sfx("gull", T_WIND + 0.5, gain_db=-14, pan=-0.2)
    out_end = T_IN + 0.4
    t_in_amb = T_REV[0] - 0.3
    for name, g_out, g_in, t0, fi in (("storm_wind", -9, -17, T_WIND - 0.4, 2.0), ("waves_storm", -9, -15, T_WIND, 2.0),
                                      ("rain", -10, -17, T_WIND + 1.0, 1.0)):
        sc.sfx(name, t0, dur=out_end - t0, gain_db=g_out, fade_in=fi, fade_out=1.2)
        sc.sfx(name, t_in_amb, dur=T + 0.6 - t_in_amb, gain_db=g_in, fade_in=1.0, fade_out=0.8)
    sc.sfx("drip", T_REV[0], dur=T + 0.6 - T_REV[0], gain_db=-16, fade_in=0.6, fade_out=0.8)
    sc.sfx("ship_creak", 0, dur=T + 0.6, gain_db=-13, fade_in=0.8, fade_out=0.8)
    sc.sfx("ship_creak", l1.start - 0.1, dur=l1.end - l1.start + 0.8, gain_db=-7, fade_in=0.3, fade_out=0.5)
    for (ts, _), (bx_, *_r) in zip(STRIKES, bolts):
        sc.sfx("thunder", ts, gain_db=-6 if ts < S4 else -9, pan=max(-0.6, min(0.6, (bx_ - 1200) / 1300)))
    sc.sfx("thunder", T_HATCH[0], gain_db=-14, pan=0.3)
    sc.sfx("thunder", T_HATCH[1], gain_db=-17, pan=0.3)
    for th, side, sz in HITS:
        sc.sfx("splash", th, gain_db=-8, pan=0.45 if side == "stern" else -0.45)
    sc.sfx("cloth", T_TEAR, gain_db=-12, pan=-0.3)
    sc.sfx("splash", T_CRASH + 0.05, gain_db=-7, pan=-0.4)
    for ts, x, _, _ in splashes:
        sc.sfx("splash_small", ts, gain_db=-7, pan=max(-0.8, min(0.8, (x - 1200) / 1100)))
    for nm, tr in REL.items():
        sc.sfx("whoosh", tr, gain_db=-15, pan=-0.3 if nm[0] in "AD" else 0.3)
    sc.sfx("snore", snore_at, dur=snore_dur, gain_db=-8, fade_in=0.5, fade_out=0.6)
    return sc
