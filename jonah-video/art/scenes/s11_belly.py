"""Scene 11 — inside the great fish (Jonah 1:17-2:2).

Adapted from the approved v1 belly (art/scenes_v1/s07_belly.py, first half): the same soft tube of crooked rib
arches, wet plum/teal walls, lumpy floor, pool with little fishes, swallowed kelp, jar and shells.

Story beats (all keyed to the narration chunks, never to fixed times):
  L0 '大鱼的肚子里又黑又湿。'   the scene opens very dark; the glowing nubs on the walls light up one by one and
                                 show the wet belly; drops fall from the kelp and the ceiling into the puddles.
                                 Jonah lies curled up on the floor, wet, eyes closed.
     '可是别怕，约拿还活着！'    he stirs on '别怕' and pops up to sit on '约拿还活着', eyes wide (surprised: he is
                                 alive!), then blinks into a relieved smile with a little wiggle (face visible).
  L1 '…过了三天三夜。'          he sits hugging his knees, sad and soaked; a soft glow opens at the top of the
                                 belly and three suns and three moons pop up one by one (day, night, day, ...),
                                 each sun warming and each moon cooling the light a little. He stays wet.
     '他在那里，向上帝祷告：'   the full row of days holds through '他在那里'; on '向上帝祷告' he gathers himself
                                 (squash) and pops up onto his knees with folded hands — a hard pose cut sold by a
                                 clear squash-hop-land, on v1's spot. He is still soaked (seaweed on his
                                 head-cloth): he is still inside the fish. The row drifts away.
  L2 '我遇到危险，向你求救，你就回答了我。'   earnest prayer (worried face, gentle rocking); a small warm ember
                                 glows at his hands, a few single sparkles drift up from them on '向你求救', and on
                                 '你就回答了我' a faint warm glow blooms around him.
  L3 '我从很深很深的地方呼喊，'  golden sparkles rise from him up through the dark (his prayer rising).
     '你就听见了我的声音。'     God hears: a soft golden beam comes down from above, the glow grows, the walls
                                 near him warm up, and Jonah opens his eyes and lifts his face, hopeful.
                                 Then the warm light washes down over him from head to knees and leaves him dry
                                 (seaweed and drops gone, cream head-cloth, as in s12): a soft top-down wipe of the
                                 dry figure over the identical wet one, led by a band of warm light.
                                 The glow is deliberately capped at about half of s12's finale
                                 ('救恩属于耶和华', glow fullest) so the story's light keeps building there.
The last second is a calm hold (Jonah kneeling in the glow) that dissolves into s12.
Ground shadows sit on their own still layers, so hops and wiggles never lift a contact shadow off the floor.

God is never drawn: only warm light, a beam and sparkles.
Note: engine blend="screen" saturates (cv2.add clips before the subtract), so glows here use "add"/"normal".
"""
import math
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes_v1 import s07_belly as V
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene

JX, JY, JS = V.JX, V.JY, V.JS          # Jonah's anchor and scale (same spot as v1 / s12)
GX, GY = V.GX, V.GY                    # centre of God's warm glow (Jonah's chest when kneeling)
TOP = (V.TOP[0], V.TOP[1] + 10)        # the round "days" glow at the top
PX, PY, PRX, PRY = V.PX, V.PY, V.PRX, V.PRY
NEAR_I = V.NEAR_I

_PUNCT = "，。！？：；、…—“”‘’（）,.!?:; "


def phrase_t(line, phrase, where=0.0, fallback=None):
    """Estimated time of ``phrase`` (where=0 its start, 1 its end) inside the subtitle chunk that contains it:
    the chunk's start plus its duration scaled by the share of characters spoken before it (punctuation counts
    as a short pause). Checked against the recorded voice: within ~0.05 s for these lines."""
    for c in line.chunks:
        if phrase in c.text:
            txt = c.text.rstrip(_PUNCT)

            def w(s):
                return sum(0.8 if ch in _PUNCT else 1.0 for ch in s)
            i = txt.index(phrase) + int(round(where * len(phrase)))
            return c.start + (c.end - c.start) * w(txt[:i]) / max(1e-6, w(txt))
    if fallback is not None:
        return line.start + (line.end - line.start) * fallback
    raise KeyError(f"{phrase!r} not in {line.text!r}")


def masked_doc(inner_doc, cx, cy, r, stops, tag):
    """Wrap a full SVG document in a soft radial mask centred at (cx, cy)."""
    defs = (f'<radialGradient id="mg{tag}" gradientUnits="userSpaceOnUse" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}">'
            + "".join(f'<stop offset="{o}" stop-color="#ffffff" stop-opacity="{a}"/>' for o, a in stops)
            + f'</radialGradient><mask id="mk{tag}" maskUnits="userSpaceOnUse" x="-50" y="-50" width="{W + 100}" '
              f'height="{H + 100}"><rect x="-50" y="-50" width="{W + 100}" height="{H + 100}" fill="url(#mg{tag})"/>'
              f'</mask>')
    return S.svg_doc(f'<g mask="url(#mk{tag})">{inner_doc}</g>', defs=defs)


def lut_tint(color, alpha_fn, mode="multiply"):
    """FX.tint for 'multiply' / 'screen' with the same per-channel maths, done as one uint8 lookup table
    (cv2.LUT) instead of float arrays over the whole frame — several times cheaper."""
    col = np.array(color, np.float64) / 255.0
    v = np.arange(256, dtype=np.float64) / 255.0

    def fx(frame, t, view):
        a = float(alpha_fn(t))
        if a <= 0.003:
            return frame
        lut = np.empty((1, 256, 4), np.uint8)
        for c in range(3):
            f = v * (1 - a + a * col[c]) if mode == "multiply" else 1 - (1 - v) * (1 - a * col[c])
            lut[0, :, c] = (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
        lut[0, :, 3] = np.arange(256, dtype=np.uint8)
        return Image.fromarray(cv2.LUT(np.asarray(frame), lut), "RGBA")
    return fx


def hand_sparkles(x, y, cues, dur=1.7, rise=170, size=12, color=(255, 232, 160), face=None):
    """A few single sparkles that leave (x, y) — Jonah's folded hands — and drift up, one per cue
    (start time, sideways drift px). They fade out over his face (v1's face mask)."""
    mask = V._face_mask(face)

    def fx(frame, t, view):
        live = [(t0, sdx) for t0, sdx in cues if t0 <= t < t0 + dur]
        if not live:
            return frame
        ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i, (t0, sdx) in enumerate(live):
            u = (t - t0) / dur
            xx = x + sdx * u + 7 * math.sin(2 * math.pi * u * 1.3 + i)
            yy = y - rise * M.ease("out")(u)
            tw = 0.7 + 0.3 * math.sin((t - t0) * 9 + i)
            env = min(1.0, u / 0.12, (1 - u) / 0.45) * mask(xx, yy)
            a = int(240 * env * tw)
            if a <= 4:
                continue
            ox, oy = view.to_out(xx, yy)
            V._star(d, ox, oy, size * view.scale * (0.55 + 0.45 * tw) * (1 - 0.3 * u), color, a)
        frame.alpha_composite(ov)
        return frame
    return fx


def swap(t_on, t_off):
    """Hard on/off switch of a pose layer (no crossfade between different poses)."""
    return lambda t: Tf(alpha=1.0 if t_on <= t < t_off else 0.0)


def glow_cluster(centres):
    """Little glowing nubs on the walls (bioluminescence), from v1."""
    out = ""
    pts = []
    for (gi, u, ang, sc_) in centres:
        cx, cy = V._wall_pt(gi, u, math.radians(ang))
        for (ox, oy, r) in ((0, 0, 15), (25, -9, 11), (-21, 9, 10), (6, 21, 8)):
            pts.append((cx + ox * sc_, cy + oy * sc_, r * sc_))
    for x, y, r in pts:
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="#6fd8cc" opacity="0.22" filter="url(#soft)"/>'
    for x, y, r in pts:
        out += S.g(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#9fe6da" stroke="{S.mix(P["ink"], "#2a5a66", 0.4)}" '
                   f'stroke-width="2.6"/><circle cx="{x - r * 0.32:.1f}" cy="{y - r * 0.32:.1f}" r="{r * 0.3:.1f}" '
                   f'fill="#f2fff8"/>', filter="wobble-fine")
    c = pts[0]
    return S.svg_doc(out), (c[0], c[1])


# ----------------------------------------------------------------- build
def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    L0, L1, L2, L3 = (ctx.line(i) for i in range(4))

    # ---------------------------------------------------------- key times (from the narration chunks)
    t_dark = L0.start                                   # '大鱼的肚子里又黑又湿'
    t_wet = phrase_t(L0, "又湿")                         # a drop falls on 'wet'
    t_fear = L0.at("别怕")                               # '可是别怕' — Jonah stirs
    t_alive = phrase_t(L0, "约拿还活着")                  # ... and sits up, eyes wide: he is alive!
    t_glad = t_alive + 0.8                              # blink-cut to a relieved smile (+ little wiggle)
    t_sit = L1.start - 0.25                             # settles into a sad sit before the days start
    t_guo = phrase_t(L1, "过了三天三夜")                  # '过了三天三夜'
    t_ye = phrase_t(L1, "三夜", where=0.5)               # the last moon lands on '夜'
    t_pray = phrase_t(L1, "向上帝祷告")                   # kneels to pray
    t_qiu = phrase_t(L2, "向你求救")                      # '向你求救' — single sparkles leave his hands
    t_answer = phrase_t(L2, "你就回答")                   # '你就回答了我' — faint glow blooms
    t_deep = L3.start                                   # '我从很深很深的地方呼喊' — sparkles rise
    t_heard = L3.at("你就听见")                           # '你就听见了我的声音' — God hears
    n = 6                                               # 3 suns + 3 moons, one by one, the last on '夜'
    t_pop0 = t_guo - 0.6
    step = (t_ye - t_pop0) / (n - 1)
    pops = [t_pop0 + step * i for i in range(n)]

    # ---------------------------------------------------------- the belly (cool), and a warm patch around Jonah
    sc.add("belly_cool", V.belly_svg(V.COOL, "c", "#1a1430", 1.0), seed=11)

    warm = masked_doc(V.belly_svg(V.WARM, "w", "#2a1420", 0.65), GX + 40, GY + 40, 900,
                      [(0, 1), (0.35, 0.85), (0.7, 0.3), (1, 0)], "w")
    # glow caps: s11 only *begins* the warm light (God hears); s12's finale ('救恩属于耶和华') is the fullest
    sc.add("belly_warm", warm, seed=11, wc_edge=0.0, motion=M.keys(
        [(t_answer - 0.2, {"alpha": 0}), (t_answer + 1.6, {"alpha": 0.18}), (t_heard - 0.1, {"alpha": 0.21}),
         (t_heard + 1.6, {"alpha": 0.45})], ["sine", "linear", "inout"]))

    # wet glints on the walls twinkle softly ('又湿'); they fade a little as the warm light comes.
    # Each glint is its own tiny layer (same twinkle per set): one layer per scattered set would warp a
    # near-full-stage bounding box every frame.
    glint_sets = []
    for gset in range(3):
        rr = random.Random(900 + gset)
        body = []
        for _ in range(7):
            gi = rr.choice((NEAR_I - 3, NEAR_I - 2, NEAR_I - 1, NEAR_I - 1, NEAR_I - 1))
            u = rr.uniform(0.25, 0.75)
            ang = rr.choice((rr.uniform(188, 352), rr.uniform(188, 352), rr.uniform(-25, 25), rr.uniform(155, 200)))
            a0 = math.radians(ang)
            p0 = V._wall_pt(gi, u, a0)
            p1 = V._wall_pt(gi, u, a0 + math.radians(rr.uniform(3, 6)))
            kk = V.KS[gi] + (V.KS[gi + 1] - V.KS[gi]) * u
            body.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" stroke="#bfe4e4" '
                        f'stroke-width="{9 * kk:.1f}" stroke-linecap="round" opacity="0.35" filter="url(#soft)"/>'
                        f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" stroke="#eafcfa" '
                        f'stroke-width="{3 * kk:.1f}" stroke-linecap="round" opacity="0.8"/>'
                        f'<circle cx="{(p0[0] + p1[0]) / 2:.1f}" cy="{(p0[1] + p1[1]) / 2:.1f}" '
                        f'r="{4.5 * kk:.1f}" fill="#f4fffc"/>')
        glint_sets.append(body)
    glint_fade = M.keys([(t_answer, {"alpha": 1.0}), (t_heard + 1.2, {"alpha": 0.75})], "sine")
    for gset, body in enumerate(glint_sets):
        per = (2.3, 2.9, 3.4)[gset]

        def gl(t, per=per, ph=gset / 3.0):
            v = 0.5 + 0.5 * math.sin(2 * math.pi * (t / per + ph))
            return Tf(alpha=0.12 + 0.88 * v ** 3)
        gm = M.combine(gl, glint_fade)
        for gk, one in enumerate(body):
            sc.add(f"glints{gset}_{gk}", S.svg_doc(one), wc=0, motion=gm)

    # glowing nubs: dim in the dark, they light up one by one on '大鱼的肚子里又黑' and pulse softly;
    # they dim a little when God's light comes. (The last cluster sits lower on the right wall than v1's, so it
    # stays clear of the last moon of the 'days' row instead of showing through the crescent's hollow.)
    clusters = [[(NEAR_I - 1, 0.2, 195, 0.95)], [(NEAR_I, 0.45, 236, 1.2)], [(NEAR_I - 1, 0.5, 318, 0.9)],
                [(NEAR_I - 1, 0.55, 12, 0.8)], [(NEAR_I - 2, 0.45, 345, 0.7)]]
    for j, cl in enumerate(clusters):
        doc, (cx, cy) = glow_cluster(cl)
        ton = t_dark + 0.15 + 0.42 * j
        sc.add(f"nubs{j}", doc, wc=0.3, motion=M.combine(
            M.keys([(ton, {"alpha": 0.2, "s": 0.85}), (ton + 0.35, {"alpha": 1.0, "s": 1.06}),
                    (ton + 0.6, {"s": 1.0}), (t_heard, {"alpha": 1.0}), (t_heard + 1.2, {"alpha": 0.75})],
                   ["out", "inout", "linear", "sine"], pivot=(cx, cy)),
            M.pulse(0.65, 1.0, 2.6 + 0.35 * j, 0.21 * j)))

    # ---------------------------------------------------------- God's light behind Jonah
    halo = S.svg_doc(
        f'<circle cx="{GX}" cy="{GY}" r="640" fill="url(#halo)"/>',
        defs=S.rad_grad("halo", [(0, "#ffe6a6", 0.55), (0.22, "#fbd38a", 0.4), (0.52, "#f2ad5c", 0.2),
                                 (1, "#e8913f", 0)]))
    glow_keys = M.keys([(t_answer - 0.2, {"alpha": 0, "s": 0.3}),
                        (t_answer + 1.4, {"alpha": 0.22, "s": 0.5}), (t_heard - 0.2, {"alpha": 0.27, "s": 0.58}),
                        (t_heard + 1.4, {"alpha": 0.5, "s": 0.8})],
                       ["out", "linear", "inout"], pivot=(GX, GY))
    sc.add("halo", halo, wc=0, motion=M.combine(glow_keys, M.breathe(0.03, 2.8, pivot=(GX, GY))))

    # the first warmth: a small, readable ember at his folded hands while he cries out (a point of light, not a
    # bloom), widening into a soft glow around him on '你就回答了我' (additive dark gold, so it stays warm over
    # the purple instead of turning grey)
    hands = C.hand_positions(C.jonah, JX, JY, JS, 1, pose="kneel_pray")[1]
    ember = S.svg_doc(f'<circle cx="{GX:.0f}" cy="{GY + 20:.0f}" r="460" fill="url(#emb)"/>',
                      defs=S.rad_grad("emb", [(0, "#8a6224", 1), (0.22, "#6e4a18", 0.9), (0.55, "#3a2410", 0.45),
                                              (1, "#000000", 0)]))
    hdx, hdy = hands[0] - GX, hands[1] - GY - 20
    sc.add("ember", ember, wc=0, blend="add", motion=M.combine(
        M.keys([(L2.start + 0.2, {"alpha": 0, "s": 0.2, "dx": hdx, "dy": hdy}),
                (L2.start + 1.5, {"alpha": 0.8, "s": 0.27}),
                (t_answer - 0.2, {"alpha": 0.85, "s": 0.3}),
                (t_answer + 1.5, {"alpha": 0.75, "s": 0.62, "dx": 0, "dy": 0}),
                (t_heard + 1.4, {"alpha": 0.6, "s": 0.85})],
               ["sine", "linear", "inout", "inout"], pivot=(GX, GY + 20)),
        M.breathe(0.035, 2.8, pivot=(GX, GY + 20), phase=0.2)))

    rays = S.svg_doc(S.path(S.rays(GX, GY, 200, 760, n=14, width_deg=4.5), fill="url(#rayg)", stroke=False,
                            extra='filter="url(#blur-md)"'),
                     defs=f'<radialGradient id="rayg" gradientUnits="userSpaceOnUse" cx="{GX}" cy="{GY}" r="760">'
                          f'<stop offset="0.2" stop-color="#6e4c22"/><stop offset="1" stop-color="#6e4c22" '
                          f'stop-opacity="0"/></radialGradient>')
    sc.add("rays", rays, wc=0, blend="add", motion=M.combine(
        M.keys([(t_heard - 0.2, {"alpha": 0, "s": 0.75}), (t_heard + 1.4, {"alpha": 0.3, "s": 0.88})], "out",
               pivot=(GX, GY)),
        lambda t: Tf(rot=2.0 * t, px=GX, py=GY)))

    # a faint cool rim of light behind Jonah so he reads in the dark (follows him from lying to sitting)
    rim = S.svg_doc(f'<ellipse cx="{JX - 20}" cy="{JY - 230}" rx="215" ry="240" fill="url(#rim)"/>',
                    defs=S.rad_grad("rim", [(0, "#22404a"), (0.6, "#0e1c22"), (1, "#000000")]))
    sc.add("rim", rim, wc=0, blend="add", motion=M.keys(
        [(0, {"alpha": 0.0, "dx": 160, "dy": 130, "sx": 1.5, "sy": 0.62}),
         (t_fear - 0.3, {"alpha": 0.0}), (t_fear + 0.6, {"alpha": 0.8}),
         (t_alive - 0.05, {"dx": 160, "dy": 130, "sx": 1.5, "sy": 0.62}),
         (t_alive + 0.35, {"alpha": 1.0, "dx": 0, "dy": 0, "sx": 1.0, "sy": 1.0}),
         (t_answer - 0.2, {"alpha": 1.0}), (t_answer + 1.6, {"alpha": 0.35})], "sine",
        pivot=(JX - 20, JY - 30)))

    # soft golden beam from the top down onto Jonah (God hears him) — behind him, lighting the space
    beam_body = ""
    for wk in (1.0, 0.72, 0.46, 0.24):
        bx0, bx1 = TOP[0] - 10, GX - 15
        beam_body += (f'<path d="M{bx0 - 80 * wk:.0f},{TOP[1] - 160} L{bx0 + 80 * wk:.0f},{TOP[1] - 160} '
                      f'L{bx1 + 260 * wk:.0f},{JY + 10} L{bx1 - 260 * wk:.0f},{JY + 10} Z" fill="url(#beam)"/>')
    beam = S.svg_doc(S.g(beam_body, filter="blur-lg"),
                     defs=S.lin_grad("beam", [(0, "#4a3a20", 0.0), (0.15, "#4a3a20", 1), (0.75, "#3e2a14", 0.8),
                                              (1, "#3e2a14", 0.0)]))
    sc.add("beam", beam, wc=0, blend="add", motion=M.combine(
        M.keys([(t_heard - 0.3, {"alpha": 0}), (t_heard + 1.3, {"alpha": 0.45})], "sine"), M.pulse(0.85, 1.0, 3.1)))

    gold_top = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] - 30}" rx="420" ry="190" fill="url(#gt)"/>',
        defs=S.rad_grad("gt", [(0, "#9a7a40", 1), (0.45, "#7a5a28", 0.6), (1, "#6a4a20", 0)]))
    sc.add("gold_top", gold_top, wc=0, blend="add", motion=M.combine(
        M.keys([(t_deep + 0.8, {"alpha": 0}), (t_heard, {"alpha": 0.2}), (t_heard + 1.0, {"alpha": 0.5})],
               "sine"),
        M.breathe(0.04, 2.6, pivot=TOP)))

    # ---------------------------------------------------------- Jonah
    # lies curled up (wet) -> pops up to sit, eyes wide (alive!) -> blinks into a relieved smile -> sits hugging
    # his knees, sad -> kneels and prays. Pose changes are hard cuts sold by a squash / hop; expression changes
    # are hard cuts like a blink (never crossfades); poses are held >= 1.5 s.
    # the sleeper lies with his head (on the left) right under the spot where his head will be when he sits up,
    # so the cut reads as "he sits up" rather than a jump.
    # Contact shadows are separate still layers under the figures, so hops never lift them off the floor.
    SLX = JX + 215
    sleep_sh = C.ground_shadow(SLX - 70, JY, 1.0, width=470, opacity=0.42)
    shadow = C.ground_shadow(JX + 10, JY, 1.0, width=320, opacity=0.4)
    sc.add("shadow_sleep", S.svg_doc(sleep_sh), motion=swap(-1, t_alive))
    sc.add("shadow", S.svg_doc(shadow), motion=swap(t_alive, 1e9))

    sleep = S.svg_doc(C.jonah(SLX, JY, JS, 1, pose="sleep", wet=True, marks=False))

    def breath_lying(t):
        u = math.sin(2 * math.pi * t / 3.3)
        return Tf(sy=1 + 0.018 * u, sx=1 - 0.004 * u, px=SLX - 60, py=JY)
    stir = M.keys([(t_fear + 0.15, {"rot": 0, "dy": 0}), (t_fear + 0.32, {"rot": 1.6, "dy": -5}),
                   (t_fear + 0.55, {"rot": 0, "dy": 0}), (t_alive - 0.42, {"rot": 0, "dy": 0}),
                   (t_alive - 0.24, {"rot": 1.4, "dy": -4}), (t_alive - 0.08, {"rot": 0, "sy": 0.94, "dy": 4})],
                  ["sine", "sine", "linear", "sine", "inout"], pivot=(SLX, JY))
    sc.add("jonah_sleep", sleep, motion=M.combine(swap(-1, t_alive), stir, breath_lying))

    # sitting (wet the whole time, hands on his knees): surprised -> happy -> sad. One flipbook, hard cuts.
    # Pivot on the ground between seat and heels, so the squash keeps both on the floor and the wiggle (<= 1.2
    # deg) moves them by only ~1.5 px.
    SPV = (JX + 65, JY)
    wg = max(0.4, min(0.85, t_sit - 0.12 - t_glad))     # the wiggle fits between the smile and the sad cut
    sit =[S.svg_doc(C.jonah(JX, JY, JS, 1, pose="sit", expr=e, wet=True)) for e in ("surprised", "happy", "sad")]
    sit_m = M.keys([(t_alive, {"sy": 0.9, "sx": 1.05, "dy": 8}), (t_alive + 0.14, {"sy": 1.05, "sx": 0.98, "dy": -16}),
                    (t_alive + 0.36, {"sy": 1.0, "sx": 1.0, "dy": 0}),
                    # blink into a smile, then a happy little wiggle (he is alive!)
                    (t_glad + 0.05, {"rot": 0}), (t_glad + 0.35 * wg, {"rot": -1.2}),
                    (t_glad + 0.68 * wg, {"rot": 1.0}), (t_glad + wg, {"rot": 0}),
                    # a little sigh as he settles in for the long wait
                    (t_sit, {"sy": 0.96, "dy": 0}), (t_sit + 0.35, {"sy": 1.0}),
                    # he gathers himself (anticipation squash) before popping up onto his knees
                    (t_pray - 0.3, {"sy": 1.0, "sx": 1.0, "dy": 0}), (t_pray, {"sy": 0.88, "sx": 1.05, "dy": 5})],
                   ["out", "inout", "linear", "sine", "sine", "sine", "inout", "back", "linear", "inout"], pivot=SPV)
    sc.add("jonah_sit", sit, frame_at=lambda t: 0.0 if t < t_glad else (1.0 if t < t_sit else 2.0),
           motion=M.combine(swap(t_alive, t_pray), sit_m, M.breathe(0.012, 3.4, pivot=SPV)))

    # three days later he kneels to pray, still soaked (he is still inside the fish): the same wet costume as the
    # sitting pose, so the cut only changes the pose — sold by a clear squash -> hop -> land. Worried while he
    # cries out -> peaceful when God answers -> eyes open, hopeful, when God hears him (expression swaps are
    # hard cuts, like a blink). Only then does God's warm light wash down over him and leave him dry (as in s12):
    # the dry figure (same pose, expression and motion) is revealed top-down over the wet one, never crossfaded.
    exprs = ("worried", "peaceful", "happy")
    kneel = [S.svg_doc(C.jonah(JX, JY, JS, 1, pose="kneel_pray", expr=e)) for e in exprs]
    kneel_wet = [S.svg_doc(C.jonah(JX, JY, JS, 1, pose="kneel_pray", expr=e, wet=True)) for e in exprs]
    # Both kneel layers carry one extra, never-shown frame: two dots at the corners of BOX, so the two layers get
    # the same crop box (with room above and below the figure for the soft wipe edge) and the wipe lines up.
    BOX = (JX - 125 * JS, JY - 345 * JS, JX + 85 * JS, JY + 62 * JS)
    box_frame = S.svg_doc("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{P["foam"]}"/>'
                                  for x, y in ((BOX[0], BOX[1]), (BOX[2], BOX[3]))))
    t_e1, t_e2 = t_answer + 0.25, t_heard + 0.45
    lift0, lift1 = t_heard + 0.2, t_heard + 1.0

    def rock(t):
        a = M.progress(t, L2.start - 0.3, L2.start + 0.6, "sine") * (1 - 0.6 * M.progress(t, lift0, lift1, "sine"))
        return Tf(rot=1.1 * a * math.sin(2 * math.pi * (t - L2.start) / 3.4))
    # the cut lands on a deep squash (keeps the head close to the gathered sitting head; held ~2 frames so it is
    # always on screen), then he springs up (stretch + hop), lands on his knees (small squash) and settles
    kneel_m = M.keys([(t_pray, {"sy": 0.8, "sx": 1.08, "dy": 4}), (t_pray + 0.06, {"sy": 0.8, "sx": 1.08, "dy": 4}),
                      (t_pray + 0.2, {"sy": 1.05, "sx": 0.97, "dy": -18}),
                      (t_pray + 0.36, {"sy": 0.94, "sx": 1.04, "dy": 2}),
                      (t_pray + 0.56, {"sy": 1.0, "sx": 1.0, "dy": 0}),
                      (lift0, {"rot": 0, "dy": 0}), (lift1, {"rot": -2.0, "dy": 0})],
                     ["linear", "out", "in", "inout", "linear", "out"], pivot=(JX, JY))
    kneel_motion = M.combine(kneel_m, M.with_pivot(rock, (JX, JY)), M.breathe(0.01, 3.0, pivot=(JX, JY), phase=0.3))
    kneel_frame = lambda t: 0.0 if t < t_e1 else (1.0 if t < t_e2 else 2.0)  # noqa: E731

    # the drying wipe (stage y, in the figures' own frame): the dry figure's soft edge runs from above the head-cloth
    # to below the knees; the wet figure is erased LAG px behind it, so the figure is never see-through
    W_SOFT, LAG = 90.0, 104.0
    w_y0 = JY - 305 * JS - W_SOFT / 2 - 4              # edge above the (wet) head-cloth
    w_y1 = JY + 20 * JS + W_SOFT / 2 + 4               # edge below the knees / toes (and drops)
    crop_t, crop_h = BOX[1] - 3, BOX[3] - BOX[1] + 6   # the shared crop box (dots of r=2, anti-aliased)
    t_w0, t_w1 = t_heard + 0.3, t_heard + 2.0          # while '你就听见了我的声音' and the beam comes down

    def wipe_y(t):
        return w_y0 + (w_y1 + LAG - w_y0) * M.progress(t, t_w0, t_w1, "sine")

    def dry_reveal(t):
        y = wipe_y(t)
        return dict(mode="down", frac=1.0 if y >= w_y1 else (y - crop_t) / crop_h, soft=W_SOFT)

    def wet_reveal(t):
        y = wipe_y(t) - LAG
        return dict(mode="up", frac=1.0 if y <= w_y0 else 1 - (y - crop_t) / crop_h, soft=W_SOFT)
    sc.add("jonah_kneel", kneel + [box_frame], frame_at=kneel_frame, reveal=dry_reveal,
           motion=M.combine(swap(t_w0, 1e9), kneel_motion))
    kneel_layer = sc.layers[-1]

    # ---------------------------------------------------------- swallowed things on the floor (v1)
    stuff = PR.seaweed(1425, 868, 0.42, variant=2)
    stuff += PR.jar(1500, 862, 0.5, rot=78)
    stuff += V.shell(1580, 882, 0.8)
    stuff += V.starfish(705, 975, 30, rot=12)
    stuff += V.shell(1180, 1010, 0.9, "#e7c2d8")
    sc.add("floor_things", S.svg_doc(V.dimmed(stuff, 0.9)))

    for j, (x, y, s_, var, sw, deg, per, ph) in enumerate((
            (1860, 1075, 1.3, 0, 0.2, 2.4, 4.6, 0.0), (2010, 1095, 1.05, 2, -0.15, 3.0, 3.9, 0.35),
            (1710, 1090, 0.9, 1, 0.1, 2.0, 5.3, 0.6))):
        sc.add(f"weed{j}", S.svg_doc(V.dimmed(PR.seaweed(x, y, s_, variant=var, sway=sw), 0.72)),
               motion=M.sway(deg, per, (x, y), ph))

    # the pool with little fishes (v1)
    pool = f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="url(#pool)" {S.STROKE_THIN}/>'
    sc.add("pool", S.svg_doc(V.dimmed(S.g(pool, filter="wobble"), 0.8),
                             defs=S.rad_grad("pool", [(0, "#3f8c96"), (0.7, "#2a5f70"), (1, "#22465a")])))
    fishes = [("pink", 330, 986, 75, 19.0, 0.8), ("yellow", 440, 1010, 80, 20.0, 0.85),
              ("orange", 215, 1032, 80, 17.0, 0.5)]
    for i, (col, xc, yc, A, per, ph) in enumerate(fishes):
        frames = [S.svg_doc(V.dimmed(PR.small_fish(xc, yc, 0.85, fac, col, tail=tl), 0.84))
                  for fac in (1, -1) for tl in (-0.7, 0.7)]

        def fish_frame(t, per=per, ph=ph):
            right = math.cos(2 * math.pi * (t / per + ph)) >= 0
            return float((0 if right else 2) + int(t / 0.3 + ph * 3) % 2)

        def fish_motion(t, A=A, per=per, ph=ph):
            return Tf(dx=A * math.sin(2 * math.pi * (t / per + ph)), dy=4 * math.sin(2 * math.pi * (t / 2.2 + ph)))
        sc.add(f"fish{i}", frames, frame_at=fish_frame, motion=fish_motion)
    surf = (f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX - 4}" ry="{PRY - 3}" fill="#6fb3bd" opacity="0.36"/>'
            + S.path(f"M{PX - 220},{PY - 30} q40,-10 80,0 t80,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.7"')
            + S.path(f"M{PX + 40},{PY + 24} q35,-9 70,0 t70,0", stroke=False,
                     extra=f'stroke="{P["sea_pale"]}" stroke-width="4" fill="none" opacity="0.55"'))
    sc.add("pool_surface", S.svg_doc(surf), wc=0.4, motion=M.bob(3, 3.0, axis="x"))

    # ---------------------------------------------------------- hanging kelp and drips
    hx1, hx2 = 300.0, 1850.0
    hy1, hy2 = V._rib_top_y(NEAR_I, hx1), V._rib_top_y(NEAR_I, hx2)
    len1 = 300.0
    hang_l = (V.kelp_strand(hx1 - 30, hy1, 230, 34, "#5e7d3c", seed=1, curl=-1) +
              V.kelp_strand(hx1, hy1 + 4, len1, 40, P["olive"], seed=2) +
              V.kelp_strand(hx1 + 36, hy1 - 4, 170, 30, "#4f7a52", seed=3))
    SW_DEG, SW_PER = 2.0, 5.2

    def sway_l(t):
        return SW_DEG * math.sin(2 * math.pi * t / SW_PER)
    sc.add("hang_l", S.svg_doc(V.dimmed(S.g(hang_l, filter="wobble-fine"), 0.78)),
           motion=M.sway(SW_DEG, SW_PER, (hx1, hy1)))
    hang_r = (V.kelp_strand(hx2 - 24, hy2, 250, 36, P["olive"], seed=4) +
              V.kelp_strand(hx2 + 20, hy2 + 2, 190, 30, "#5e7d3c", seed=5, curl=-1))
    sc.add("hang_r", S.svg_doc(V.dimmed(S.g(hang_r, filter="wobble-fine"), 0.74)),
           motion=M.sway(-1.8, 4.4, (hx2, hy2), 0.3))

    # drips from the middle kelp strand's tip into the pool
    tipx, tipy = V.kelp_tip(hx1, hy1 + 4, len1, seed=2)
    DS = 1.2
    DX, DY0 = tipx, tipy + 8
    DTOP = DY0 - 16 * DS
    # only while the narrator talks about the wet belly (L0) — none under Jonah's prayer, where the soft drip
    # ambience carries the wetness
    kelp_drips = (t_dark + 0.5, t_alive + 1.4)
    fall = 0.5
    sfx_plips = []

    def drop_motion(t):
        for td in kelp_drips:
            if td - 0.6 <= t < td:
                s = 0.3 + 0.7 * M.progress(t, td - 0.6, td, "out")
                th = sway_l(t)
                qx, qy = V._rot_pt(DX, DTOP, hx1, hy1, th)
                return Tf(dx=qx - DX, dy=qy - DTOP, rot=th, sx=s, sy=s, alpha=1.0, px=DX, py=DTOP)
            if td <= t < td + fall:
                u = (t - td) / fall
                qx, qy = V._rot_pt(DX, DTOP, hx1, hy1, sway_l(td))
                oy = qy - DTOP
                return Tf(dx=qx - DX, dy=oy + (PY - 4 - DY0 - oy) * u * u, alpha=1.0)
        return Tf(alpha=0.0)
    sc.add("drop", S.svg_doc(V.drop_shape(DX, DY0, DS)), wc=0, motion=drop_motion)
    sfx_plips += [(td + fall, -0.45) for td in kelp_drips]

    def ripple_motion(times, cx, cy, delay, lx_fn=None, big=2.6):
        def m(t):
            for ti0 in times:
                ti = ti0 + delay
                if ti <= t < ti + 1.2:
                    u = (t - ti) / 1.2
                    s = 0.4 + big * M.ease("out")(u)
                    lx = lx_fn(ti0) if lx_fn else 0.0
                    return Tf(dx=lx, sx=s, sy=s, alpha=0.9 * (1 - u), px=cx, py=cy)
            return Tf(alpha=0.0)
        return m
    ring = S.svg_doc(f'<ellipse cx="{DX:.1f}" cy="{PY - 4}" rx="26" ry="7" fill="none" stroke="{P["sea_pale"]}" '
                     f'stroke-width="3.5"/>')
    lands = [td + fall for td in kelp_drips]
    lx_k = lambda tl: V._rot_pt(DX, DTOP, hx1, hy1, sway_l(tl - fall))[0] - DX  # noqa: E731
    sc.add("ripple_a", ring, wc=0, motion=ripple_motion(lands, DX, PY - 4, 0.0, lx_k))
    sc.add("ripple_b", ring, wc=0, motion=ripple_motion(lands, DX, PY - 4, 0.28, lx_k))

    # drips from the ceiling (the inner edge of a rib) into the shiny puddles on the floor: one on '又湿'
    ceil = [  # (x, top y, puddle y, times)
        (1330.0, 205.0, 818.0, (t_wet - 0.35, t_sit + 0.25)),
        (1215.0, 192.0, 906.0, (t_alive + 0.3,)),
    ]
    for k, (cx, cy0, py, times) in enumerate(ceil):
        fall_c = math.sqrt((py - cy0) / 900.0) * 0.62

        def cdrop(t, cx=cx, cy0=cy0, py=py, times=times, fall_c=fall_c):
            for td in times:
                if td - 0.7 <= t < td:            # swells on the rib
                    s = 0.25 + 0.75 * M.progress(t, td - 0.7, td, "out")
                    return Tf(sx=s, sy=s, alpha=1.0, px=cx, py=cy0 - 12)
                if td <= t < td + fall_c:
                    u = (t - td) / fall_c
                    return Tf(dy=(py - 8 - cy0) * u * u, sy=1 + 0.25 * u, alpha=1.0, px=cx, py=cy0)
            return Tf(alpha=0.0)
        sc.add(f"cdrop{k}", S.svg_doc(V.drop_shape(cx, cy0, 1.0)), wc=0, motion=cdrop)
        cl = [td + fall_c for td in times]
        cring = S.svg_doc(f'<ellipse cx="{cx:.1f}" cy="{py:.1f}" rx="20" ry="5" fill="none" stroke="{P["sea_pale"]}" '
                          f'stroke-width="3"/>')
        sc.add(f"cring{k}a", cring, wc=0, motion=ripple_motion(cl, cx, py, 0.0, big=2.2))
        sc.add(f"cring{k}b", cring, wc=0, motion=ripple_motion(cl, cx, py, 0.25, big=2.2))
        sfx_plips += [(x, 0.25 if cx > 1250 else 0.15) for x in cl]

    # ---------------------------------------------------------- three days and three nights
    # A round glow opens at the top while the narrator says '约拿在大鱼的肚子里'; then a sun, a moon, a sun ...
    # pop up one by one, the last moon landing on '夜'. The full row holds through '他在那里' (~1.7 s for small
    # viewers to take in 'three days and three nights') and drifts away as he begins to pray.
    fade0, fade1 = t_pray + 0.2, t_pray + 1.2
    top_glow = S.svg_doc(
        f'<ellipse cx="{TOP[0]}" cy="{TOP[1] + 4}" rx="560" ry="135" fill="url(#tg)"/>',
        defs=S.rad_grad("tg", [(0, "#fff4d8", 0.5), (0.6, "#f6e2c0", 0.3), (1, "#f0d8b0", 0)]))
    sc.add("days_glow", top_glow, wc=0, motion=M.keys(
        [(L1.start + 0.4, {"alpha": 0}), (t_pop0 - 0.15, {"alpha": 1}), (fade0, {"alpha": 1}),
         (fade1 + 0.2, {"alpha": 0})], "sine"))
    SPC = 168
    for i in range(n):
        x = TOP[0] + (i - (n - 1) / 2) * SPC
        y = TOP[1] + ((i - (n - 1) / 2) / ((n - 1) / 2)) ** 2 * 24
        icon = V.sun_icon(x, y, 42) if i % 2 == 0 else V.moon_icon(x, y, 44)
        disc_col = "#ffe7a0" if i % 2 == 0 else "#cfe0f2"
        disc = f'<circle cx="{x}" cy="{y}" r="82" fill="url(#d{i})"/>'
        ti = pops[i]
        sc.add(f"day{i}", S.svg_doc(disc + icon, defs=S.rad_grad(f"d{i}", [(0, disc_col, 0.9), (0.6, disc_col, 0.45),
                                                                          (1, disc_col, 0)])),
               wc=0.3, motion=M.combine(
                   M.keys([(ti, {"alpha": 0, "s": 0.2}), (ti + 0.15, {"alpha": 1}), (ti + 0.42, {"s": 1.0}),
                           (fade0 + 0.05 * i, {"alpha": 1, "dy": 0}),
                           (fade1 + 0.05 * i, {"alpha": 0, "dy": -30})],
                          ["sine", "back", "linear", "sine"], pivot=(x, y)),
                   M.bob(3, 2.4, i * 0.17)))

    # each sun warms the light a little and each moon cools it (day, night, day, ...)
    def day_tint(warm_):
        def a(t):
            v = 0.0
            for i, ti in enumerate(pops):
                if (i % 2 == 0) == warm_ and ti <= t < ti + 1.3:
                    u = (t - ti) / 1.3                       # quick swell (~0.2 s), slow ebb
                    v = max(v, min(1.0, u / 0.15) * (1 - u) ** 1.5)
            return v
        return a
    tint_warm = lut_tint((255, 214, 150), lambda t: 0.09 * day_tint(True)(t), mode="screen")
    tint_cool = lut_tint((150, 160, 215), lambda t: 0.16 * day_tint(False)(t), mode="multiply")

    # ---------------------------------------------------------- camera: one slow, continuous push-in towards Jonah
    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2, W)), (T, Cam(935, 600, W * 0.8))], "sine")

    # ---------------------------------------------------------- particles (kept off Jonah's face)
    head = C.body_points(C.jonah, JX, JY, JS, 1, pose="kneel_pray")["head"]
    face = (head[0] - 8, head[1] - 2, 112, 118)

    def prayer_level(t):
        return (0.12 * M.progress(t, t_answer - 0.2, t_answer + 1.2, "sine") +
                0.55 * M.progress(t, t_deep, t_deep + 2.2, "sine") +
                0.33 * M.progress(t, t_heard, t_heard + 1.0, "sine"))

    def opening_dark(t):           # the belly is darker at first; the nubs light it up ('又黑')
        return 0.42 * (1 - M.progress(t, t_dark - 0.2, t_dark + 2.2, "sine"))

    sc.fx = [
        FX.tint((14, 10, 24), opening_dark),
        tint_warm, tint_cool,
        FX.motes((0, 100, W, 950), count=18, color=(160, 205, 200), size=(3, 6), alpha=55, seed=5),
        # '向你求救': three single sparkles leave his folded hands (drifting away from his face)
        hand_sparkles(hands[0] + 6, hands[1] - 6, [(t_qiu - 0.05, 40), (t_qiu + 0.4, 85), (t_qiu + 0.85, 20)],
                      face=face),
        V.rising_sparkles(GX + 10, JY - 20, 150, 230, 40, prayer_level, face=face),
        V.twinkles((GX - 330, GY - 330, GX + 330, GY + 180), count=18, t0=t_heard + 0.2,
                   color=(255, 240, 190), size=(8, 18), drift=-8, seed=17, face=face),
    ]

    # ---------------------------------------------------------- Jonah kneeling, wet (until the light dries him)
    # Added last with an explicit z just under the dry kneeling layer (and its watercolour seed, so the paper
    # texture matches across the wipe): adding it in place would shift every later layer's default seed.
    sc.add("jonah_kneel_wet", kneel_wet + [box_frame], frame_at=kneel_frame, reveal=wet_reveal,
           z=kneel_layer.z - 0.5, seed=kneel_layer.seed, motion=M.combine(swap(t_pray, t_w1), kneel_motion))
    # ... and the soft band of warm light that leads the wipe down over him (it is the light that dries him)
    BLX, BLY = JX - 22, w_y0
    band = S.svg_doc(f'<ellipse cx="{BLX:.0f}" cy="{BLY:.0f}" rx="215" ry="62" fill="url(#dryl)"/>',
                     defs=S.rad_grad("dryl", [(0, "#7a5a2c", 1), (0.5, "#6a4a22", 0.55), (1, "#4a3418", 0)]))

    def band_m(t):
        y = wipe_y(t) - 0.25 * W_SOFT
        u = min(1.0, max(0.0, (y - w_y0) / (w_y1 - w_y0)))
        return Tf(dy=y - BLY, alpha=0.5 * math.sin(math.pi * u) ** 0.8 if t_w0 < t < t_w1 else 0.0)
    sc.add("dry_light", band, wc=0, blend="add", z=kneel_layer.z + 0.5, seed=kneel_layer.seed, motion=band_m)

    # ---------------------------------------------------------- sound
    sc.sfx("underwater", 0, dur=T + 0.1, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("heartbeat", 0, dur=T + 0.1, gain_db=-12, fade_in=0.8, fade_out=0.9)
    sc.sfx("drip", 0, dur=T + 0.1, gain_db=-19, fade_in=0.8, fade_out=0.9, density=0.6)
    for tl, pan in sfx_plips:                      # quiet, so they don't sound like the day / night icon pops
        sc.sfx("pop", tl, gain_db=-24, pan=pan)
    sc.sfx("cloth", t_alive - 0.05, gain_db=-15)
    sc.sfx("cloth", t_sit - 0.05, gain_db=-20)
    sc.sfx("cloth", t_pray - 0.05, gain_db=-16)
    for i, ti in enumerate(pops):
        sc.sfx("pop", ti, gain_db=-17, pan=(i - 2.5) * 0.12)
    sc.sfx("chime", t_answer, gain_db=-11)
    sc.sfx("sparkle", t_heard, gain_db=-9)
    return sc
