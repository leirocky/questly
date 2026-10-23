"""Scene 15 - the closing page, back in the girl's bedroom at night (the room of s02): the wind still blows outside.
She sits up on her bed hugging her star pillow, the teddy at the foot of the bed; the picture on her wall - the
little boat on the evening lake - glows and becomes the end of the story: Jesus standing in the boat on the moonlit
lake with his friends. Then she prays, and calm comes into the room. End card '耶稣平静风浪 · 完' with a small heart.

Beats (phrase / syllable onsets measured in the voice clip with the Noah film's voice_marks helpers):
  start        calm frame (page dip from s14): the room, the curtains stirring in the wind, clouds racing past the
               moon, the girl on her bed looking up at the picture (blinks, breathing)
  '小朋友'      the picture glows softly and changes (sparkles, chime): Jesus in the boat on the moonlit lake, his
               friends around him in wonder; the camera glides toward the picture; she smiles up at it; the pause
               holds on the glowing picture
  '耶稣'        (line 1) the light round Jesus in the picture brightens (sparkle)
  '连风和海'    in the picture a few wind curls and little white-capped waves stir round the boat and Jesus lifts his
               hand; '都听耶稣的话' they shrink away: the lake turns mirror-smooth, the clouds part, the stars come out
               one by one, the moon's path shines on the water (chime)
  '下次你害怕的时候' the camera pulls back: a gust outside on '害怕' - the curtains billow, the branch thrashes - and she
               hugs her pillow, worried
  '记得耶稣就在你身边' the picture glows warmer; she looks up at it and smiles (sparkles drift round her)
  '你可以向他祷告' she sets the pillow down and kneels up on her bed, hands folded, eyes closed (squash-hop cut); the
               wind settles, the curtains hang still, a warm glow spreads from the window over the room
  line 3       '小朋友' she opens her eyes and smiles; '你害怕的时候' she sits back and snuggles her pillow, happy;
               '想对耶稣说什么呢' a little heart floats up from her toward the picture; the pause holds (breathing, twinkles)
  end          the end card '耶稣平静风浪 · 完' fades in with a little heart (chime); calm final frame for the film's
               fade-out
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam, Tf
from engine.scene import Scene
from stories.storm.scenes import s02_wind as R
from stories.storm.scenes.s01_title import (blink, boxed, char_times, compose, cuts, dip, heart_markup, snap,
                                            voice_marks, zoom_about)

INK = P["ink"]
KS = R.KID[2]
BX, BY = R.BED
SEAT = (262, BY + PR.BED_TOP * KS)          # the girl sitting / kneeling on the mattress, by the headboard
TEDDY = (BX + 175 * KS, BY + PR.BED_TOP * KS + 6)
KBOX = (int(SEAT[0] - 170), int(SEAT[1] - 380), int(SEAT[0] + 230), int(SEAT[1] + 30))
PILLOW_DOWN = (SEAT[0] + 200, SEAT[1] - 36)
END = (1056, 1000)
WIND15 = (0.95, 0.75, 0.55, 0.42, 0.32, 0.22)

# the picture's second state (full-stage coordinates, shown at R.GK0 in the frame)
P_HZ = 690
P_MOON = (1690, 230)
PB = (990, 935, 0.86)                       # boat waterline anchor and scale in the picture

C.EXPRS.setdefault("se_up", dict(C.EXPRS["kind"], look=(0.06, -0.11)))
C.EXPRS.setdefault("se_glad", dict(eyes="dot", brow=(-0.06, 0.02, -0.08), mouth="smile", look=(0.06, -0.12),
                                   blush=True))
for _e in ("se_up", "se_glad", "worried"):
    C.EXPRS.setdefault(f"st_blink_{_e}", dict(C.EXPRS[_e], eyes="closed"))


def doc(body, defs="", w=W, h=H):
    return S.svg_doc(body, defs, w, h)


def merge_docs(docs):
    """Flatten several svg_doc() documents into one (their user defs and bodies, the shared filters once)."""
    filt = S._filters()
    bodies, defs = "", ""
    for d in docs:
        i0 = d.index("<defs>") + 6
        i1 = d.index("</defs>")
        defs += d[i0:i1].replace(filt, "")
        bodies += d[i1 + 7:-6]
    return doc(bodies, defs)


# ================================================================== the picture: from the evening boat to the calm

def old_picture_svg():
    """s02's picture (the evening lake, Jesus asleep in the boat), flattened into one layer."""
    return merge_docs([R.g_sky_a_svg(), R.g_water_a_svg(), R.g_ripples_svg(0), R.g_boat_svg("calm", 0, "back"),
                       R.g_far_svg("calm"), R.g_jesus_svg(), R.g_near_svg("calm"), R.g_boat_svg("calm", 0, "front"),
                       R.g_strip_a_svg()])


def p_sky_svg(calm):
    sky = PR.night_sky(-20, -40, W + 20, P_HZ + 40, moon=P_MOON, moon_r=78, stars=48,
                       progress=1.0 if calm else 0.22, twinkle=0.3, clouds=0.0 if calm else 0.75, seed=5, scale=1.2)
    hills = PR.lake_galilee(-40, W + 40, P_HZ + 150, 0.6, time="night", shore=None, part="back", sky=False,
                            boats=False)
    return doc(sky + hills)


def p_lake_svg(calm):
    lake = PR.calm_lake(-20, W + 20, P_HZ, phase=0.3, moon_x=P_MOON[0], ripples=0.7 if calm else 1.6,
                        sparkle=1.0, seed=4, scale=1.3, glow=1.0 if calm else 0.35)
    return doc(lake)


def p_strip_svg(calm):
    """The same lake drawn again in front of the hull below the waterline (clipped to a band round the hull)."""
    bx, by, bs = PB
    lake = PR.calm_lake(-20, W + 20, P_HZ, phase=0.3, moon_x=P_MOON[0], ripples=0.7 if calm else 1.6,
                        sparkle=1.0, seed=4, scale=1.3, glow=1.0 if calm else 0.35)
    x0, x1 = bx - 720 * bs, bx + 720 * bs
    top = S.wave_line(by - 3, 2.6, 110, 0.4, x0=x0, x1=x1)
    d = top + f" L{x1},{by + 90 * bs} L{x0},{by + 90 * bs} Z"
    body = f'<clipPath id="sepc{int(calm)}"><path d="{d}"/></clipPath><g clip-path="url(#sepc{int(calm)})">{lake}</g>'
    body += (f'<path d="{S.wave_line(by - 1, 2.6, 110, 0.4, x0=bx - 680 * bs, x1=bx + 690 * bs)}" stroke="#dfe6f6" '
             f'stroke-width="4" fill="none" opacity="0.8"/>')
    return doc(body)


def p_pts():
    return PR.boat_points(PB[0], PB[1], PB[2], 1)


def p_boat_svg(part):
    bx, by, bs = PB
    return doc(PR.fishing_boat(bx, by, bs, 1, sail="furled", part=part, lantern=part == "front", swing=0.2))


def p_far_svg():
    p = p_pts()["far_stand"]
    s = PB[2]
    out = ""
    for v, i, pose, e in ((0, 2, "wonder", "amazed"), (2, 3, "stand", "awed"), (3, 4, "wonder", "awed"),
                          (6, 5, "stand", "awed")):
        x, y = p[i]
        out += C.disciples(x, y, s, -1, variant=v, pose=pose, expr=e)
    return doc(out)


def p_jesus_svg(pose, glow):
    x, y = p_pts()["stand"][0]
    kw = dict(wind=0.35) if pose == "stand_command" else {}
    return doc(C.jesus(x, y, PB[2], 1, pose=pose, expr="warm", glow=glow, **kw))


def p_near_svg():
    p = p_pts()["stand"]
    s = PB[2]
    out = ""
    x, y = p[3]
    out += C.disciples(x, y, s, -1, variant=1, pose="wonder", expr="amazed")
    x, y = p[4]
    out += C.disciples(x + 30 * s, y, s, -1, variant=7, pose="kneel", expr="awed")
    return doc(out)


def p_wind_svg():
    """Wind curls in the air and little white-capped waves round the boat (they shrink away on '都听耶稣的话')."""
    bx, by, bs = PB
    out = ""
    for cx, cy, L in ((bx - 760, by - 600, 320), (bx + 560, by - 700, 360), (bx - 420, by - 820, 280),
                      (bx + 830, by - 420, 280), (bx - 920, by - 300, 260)):
        out += (f'<path d="M{cx - L / 2},{cy} q{L * 0.3},-26 {L * 0.62},0 q{L * 0.22},22 {L * 0.3},-8 '
                f'q14,-34 -22,-36 q-26,0 -18,26" stroke="#eef2fa" stroke-width="10" fill="none" stroke-linecap="round" '
                f'opacity="0.9"/>')
    caps = ""
    for cx, cy, w in ((bx - 880, by + 30, 100), (bx - 560, by + 140, 120), (bx + 720, by + 40, 110),
                      (bx + 960, by + 160, 120), (bx + 200, by + 200, 120), (bx - 1040, by + 180, 100),
                      (bx + 1060, by - 20, 80), (bx - 250, by + 110, 90), (bx + 470, by + 130, 90)):
        caps += (f'<path d="M{cx - w},{cy} Q{cx - w * 0.3},{cy - w * 0.55} {cx + w * 0.1},{cy - w * 0.35} '
                 f'Q{cx + w * 0.4},{cy - w * 0.2} {cx + w * 0.25},{cy - w * 0.02} Q{cx + w * 0.6},{cy} {cx + w},{cy} Z" '
                 f'fill="#5a6aa0" stroke="#2c3560" stroke-width="5"/>'
                 f'<path d="M{cx - w * 0.3},{cy - w * 0.45} Q{cx + w * 0.1},{cy - w * 0.6} {cx + w * 0.28},{cy - w * 0.12}" '
                 f'stroke="#f0f4fa" stroke-width="10" fill="none" stroke-linecap="round"/>')
    return doc(S.g(caps + out, filter="wobble-fine"))


def p_dim_svg():
    return doc(f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 20}" fill="#262a52"/>')


# ================================================================== the girl

def kid_svg(pose, expr, pillow=True):
    x, y = SEAT
    return boxed(C.child(x, y, KS, 1, pose=pose, expr=expr, outfit="pyjamas", pillow=pillow), KBOX)


def kid_shadow_svg():
    return boxed(C.ground_shadow(SEAT[0] + 20, SEAT[1] + 4, KS, 150, 0.22), KBOX)


def pillow_down_svg():
    x, y = PILLOW_DOWN
    return doc(PR.pillow(x, y, KS * 0.62, rot=-8))


def warm_glow_svg(cx, cy, rx, ry, gid, col="#ffd99a", op=0.6):
    defs = S.rad_grad(gid, [(0, col, op), (0.55, col, op * 0.35), (1, col, 0)])
    return doc(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>', defs)


def heart_svg(x, y, r):
    return doc(heart_markup(x, y, r))


def end_card_svg():
    x, y = END
    defs = S.rad_grad("se_card", [(0, "#fff3d6", 0.85), (0.6, "#ffe9c0", 0.35), (1, "#ffe9c0", 0)])
    out = (f'<ellipse cx="{x}" cy="{y - 40}" rx="620" ry="165" fill="url(#se_card)"/>' +
           S.text(x, y, "耶稣平静风浪 · 完", size=104, fill="#fff3d6",
                  extra=f'stroke="{INK}" stroke-width="11" paint-order="stroke" stroke-linejoin="round"'))
    return doc(out, defs)


# ================================================================== build


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    m = [voice_marks(ctx, i) for i in range(4)]
    L = ctx.lines

    def ph(li, i, text, a, b):
        mm = m[li]
        return mm[i] if len(mm) > i and mm[i][0] == text else (text, a, b, [(a, b)])
    p_kid0 = ph(0, 0, "小朋友", L[0].start, L[0].start + 0.6)
    p_he = ph(1, 0, "他就是耶稣", L[1].start, L[1].chunks[0].start + 1.0)
    p_wind = ph(1, 2, "连风和海", L[1].chunks[-1].start, L[1].chunks[-1].start + 0.9)
    p_obey = ph(1, 3, "都听耶稣的话", L[1].chunks[-1].start + 1.2, L[1].end)
    p_fear = ph(2, 0, "下次你害怕的时候", L[2].start, L[2].chunks[0].end)
    p_near = ph(2, 1, "记得耶稣就在你身边", L[2].chunks[1].start, L[2].chunks[1].end)
    p_pray = ph(2, 2, "你可以向他祷告", L[2].chunks[-1].start, L[2].end)
    p_kid3 = ph(3, 0, "小朋友", L[3].start, L[3].start + 0.6)
    p_when = ph(3, 1, "你害怕的时候", L[3].chunks[0].start + 0.9, L[3].chunks[0].end)
    p_say = ph(3, 2, "想对耶稣说什么呢", L[3].chunks[-1].start, L[3].end)
    t_glow = p_kid0[1]
    t_jesus = char_times(p_he)[3]                                  # '耶'
    t_wind = p_wind[1]
    t_obey = p_obey[1]
    t_fear = p_fear[1]
    t_gust = char_times(p_fear)[3]                                 # '害'
    t_near = p_near[1]
    t_with = char_times(p_near)[2]                                 # '耶稣'
    t_pray = snap(p_pray[1] + 0.05)
    t_open = snap(p_kid3[1] + 0.05)
    t_snug = snap(p_when[1] + 0.05)
    t_say = p_say[1]
    t_end = max(L[3].end + 0.15, T - 1.3)
    t_calm0, t_calm1 = t_pray, t_pray + 2.2

    # ---- the wind outside: still blowing, a gust on '害怕', settling after the prayer
    def base(t):
        return 0.55 - 0.36 * M.progress(t, t_calm0, t_calm1, "sine")
    wind = R.Wind(base, [(t_gust, 0.95, 0.15, 0.7)], T)
    calm = lambda t: M.progress(t, t_calm0 + 0.2, t_calm1 + 0.3, "sine")    # noqa: E731

    Z = 100
    R.add_outside(sc, wind, Z)
    body, defs = R.room_svg("s15")
    sc.add("se_room", doc(body, defs), z=Z + 1)

    # window front: wind levels x phases, a second identical flipbook with the warm glow fading in on top
    nl = len(WIND15)

    def win_fa(t):
        p = int(t / 0.09) % R.WPH
        return float(p * nl + wind.level(t, WIND15))
    sc.add("se_window", R.window_frames(WIND15, (0.0,)), z=Z + 2, frame_at=win_fa, seed=61, wc=0.8)
    sc.add("se_window_glow", R.window_frames(WIND15, (1.0,)), z=Z + 2.05, frame_at=win_fa, seed=61, wc=0.8,
           motion=lambda t: Tf(alpha=calm(t)))
    sc.add("se_winlight", warm_glow_svg(R.WIN[0], R.WIN[1] - 160, 560, 460, "se_wl", col="#ffcf86", op=0.45),
           z=Z + 2.1, blend="screen", wc=0, motion=lambda t: Tf(alpha=0.5 * calm(t)))

    # ---- the picture on the wall: s02's evening boat, then (on '小朋友') the end of the story
    def kfix(t):
        return zoom_about(R.GK0, R.ZOOM_P)

    def with_alpha(a, inner=None):
        def mm(t):
            z = kfix(t)
            tf = compose(z, inner(t)) if inner else z
            return Tf(tf.dx, tf.dy, tf.rot, tf.sx, tf.sy, tf.alpha * a(t), tf.px, tf.py)
        return mm
    t_sw0, t_sw1 = t_glow + 0.15, t_glow + 0.95
    new_a = lambda t: M.progress(t, t_sw0, t_sw1, "sine")                    # noqa: E731
    ZP = 150
    sc.add("se_old_pic", old_picture_svg(), z=ZP, motion=with_alpha(lambda t: 1.0 if t < t_sw1 + 0.02 else 0.0),
           wc=0.6)
    t_clear0, t_clear1 = t_obey - 0.05, t_obey + 1.0
    clear = lambda t: M.progress(t, t_clear0, t_clear1, "sine")              # noqa: E731
    sc.add("se_p_sky", [p_sky_svg(False), p_sky_svg(True)], z=ZP + 0.1, motion=with_alpha(new_a),
           frame_at=clear, wc=0.6)
    sc.add("se_p_lake", [p_lake_svg(False), p_lake_svg(True)], z=ZP + 0.2, motion=with_alpha(new_a),
           frame_at=clear, wc=0.6)

    def pbob(t):
        return Tf(dy=4 * math.sin(2 * math.pi * t / 4.0), rot=0.6 * math.sin(2 * math.pi * t / 4.0 + 0.5),
                  px=PB[0], py=PB[1])
    sc.add("se_p_bback", p_boat_svg("back"), z=ZP + 0.3, motion=with_alpha(new_a, pbob), seed=71)
    sc.add("se_p_far", p_far_svg(), z=ZP + 0.31, motion=with_alpha(new_a, pbob), seed=73)
    # Jesus: standing (soft glow) -> brighter on '耶稣' -> lifts his hand on '连风和海' -> lowers it after the calm
    jfr = [p_jesus_svg("stand", 0.3), p_jesus_svg("stand", 0.6), p_jesus_svg("stand_command", 0.6),
           p_jesus_svg("stand", 1.0)]
    t_hand = snap(t_wind + 0.05)
    t_hand_dn = snap(t_clear1 + 0.5)

    def jfa(t):
        if t < t_hand:
            return M.progress(t, t_jesus - 0.1, t_jesus + 0.4, "sine")
        if t < t_hand_dn:
            return 2.0
        return 3.0
    sc.add("se_p_jesus", jfr, z=ZP + 0.32, frame_at=jfa, seed=75,
           motion=with_alpha(new_a, lambda t: compose(pbob(t), dip(t_hand, PB[2], p_pts()["stand"][0], 6)(t))
                             if abs(t - t_hand) < 0.4 else pbob(t)))
    sc.add("se_p_near", p_near_svg(), z=ZP + 0.33, motion=with_alpha(new_a, pbob), seed=77)
    sc.add("se_p_bfront", p_boat_svg("front"), z=ZP + 0.34, motion=with_alpha(new_a, pbob), seed=79)
    sc.add("se_p_strip", [p_strip_svg(False), p_strip_svg(True)], z=ZP + 0.35, motion=with_alpha(new_a),
           frame_at=clear, wc=0.6)

    def wind_m(t):
        a = M.progress(t, t_wind - 0.1, t_wind + 0.35, "sine") * (1 - M.progress(t, t_obey + 0.1, t_obey + 0.9, "in"))
        k = 1 - 0.5 * M.progress(t, t_obey + 0.05, t_obey + 0.9, "in")
        sway = 6 * math.sin(2 * math.pi * t / 0.9)
        inner = Tf(dx=sway, sx=k, sy=k, alpha=a, px=PB[0], py=PB[1] - 150)
        z = kfix(t)
        return compose(z, inner)
    sc.add("se_p_wind", p_wind_svg(), z=ZP + 0.36, motion=wind_m, wc=0.3)
    sc.add("se_p_dim", p_dim_svg(), z=ZP + 0.5, wc=0,
           motion=with_alpha(lambda t: 0.34 * (1 - M.progress(t, t_glow - 0.1, t_glow + 0.6, "sine"))))
    t_mid = (t_sw0 + t_sw1) / 2
    sc.add("se_p_flash", doc(f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 20}" fill="#fff0c8"/>'), z=ZP + 0.55,
           wc=0, motion=with_alpha(lambda t: 0.6 * math.exp(-((t - t_mid) / 0.22) ** 2)))
    sc.add("se_border", R.frame_border_svg(), z=ZP + 0.6, seed=91)

    def fglow(t):
        a = 0.7 * M.progress(t, t_glow - 0.1, t_glow + 0.6, "sine")
        a += 0.3 * math.exp(-((t - t_jesus - 0.3) / 0.5) ** 2) + 0.3 * math.exp(-((t - t_obey - 0.6) / 0.6) ** 2)
        a += 0.3 * M.progress(t, t_with - 0.2, t_with + 0.6, "sine")
        return Tf(alpha=min(1.0, a * (0.9 + 0.1 * math.sin(t * 3.1))))
    sc.add("se_fglow", R.frame_glow_svg(), z=ZP - 1, blend="screen", wc=0, motion=fglow)

    # ---- the girl on her bed
    kx, ky = SEAT
    kfr = {
        "up": kid_svg("sit_hug", "se_up"), "up_b": kid_svg("sit_hug", blink("se_up")),
        "glad": kid_svg("sit_hug", "se_glad"), "glad_b": kid_svg("sit_hug", blink("se_glad")),
        "worry": kid_svg("sit_hug", "worried"), "worry_b": kid_svg("sit_hug", blink("worried")),
        "pray": kid_svg("kneel_pray", "peaceful"),
        "pray_open": kid_svg("kneel_pray", "se_glad"),
        "snug": kid_svg("sit_hug", "smile"),
        "snug_o": kid_svg("sit_hug", "se_glad"), "snug_o_b": kid_svg("sit_hug", blink("se_glad")),
    }
    names = list(kfr)
    KI = {k: i for i, k in enumerate(names)}
    t_glad = snap(t_glow + 0.5)
    t_worry = snap(t_gust + 0.02)
    t_glad2 = snap(t_with)
    t_snug_o = snap(t_say + 0.6)
    ents = [(0, KI["up"]), (t_glad, KI["glad"]), (t_worry, KI["worry"]), (t_glad2, KI["glad"]),
            (t_pray, KI["pray"]), (t_open, KI["pray_open"]), (t_snug, KI["snug"]), (t_snug_o, KI["snug_o"])]
    for tb, b in ((0.5, "up"), (2.6, "glad"), (4.3, "glad"), (6.6, "glad"), (9.4, "glad"), (12.1, "worry"),
                  (14.0, "glad"), (t_snug_o + 0.8, "snug_o"), (t_snug_o + 2.4, "snug_o")):
        tb = snap(tb)
        if tb < T - 0.2 and all(abs(tb - tk) > 0.35 for tk, _ in ents):
            ents += [(tb, KI[b + "_b"]), (snap(tb + 0.13), KI[b])]
    ents = sorted(ents)
    feet = (kx, ky)

    def hug_tight(t):
        k = math.exp(-max(0.0, t - t_worry) / 0.6) * (t >= t_worry - 0.05) * (t < t_glad2)
        return Tf(sx=1 + 0.03 * k, sy=1 - 0.035 * k, px=kx, py=ky)

    def hops(t):
        dy = 0.0
        for tk, hgt in ((t_pray, 24), (t_snug, 16)):
            u = t - tk
            if 0 <= u < 0.34:
                dy -= hgt * math.sin(math.pi * u / 0.34)
        return Tf(dy=dy)

    def happy_bob(t):
        u = t - t_snug
        if u < 0.4:
            return Tf()
        return Tf(rot=1.6 * math.sin(2 * math.pi * u / 2.2), px=kx, py=ky)
    kid_m = M.combine(hug_tight, hops, happy_bob, dip(t_glad, KS, feet, 4), dip(t_worry, KS, feet, 6),
                      dip(t_glad2, KS, feet, 4), dip(t_pray, KS, feet, 8), dip(t_open, KS, feet, 4),
                      dip(t_snug, KS, feet, 7), M.breathe(0.012, 2.8, pivot=feet))
    sc.add("se_kid_sh", kid_shadow_svg(), z=Z + 2.9)
    sc.add("se_kid", [kfr[k] for k in names], z=Z + 3, frame_at=cuts(ents), motion=kid_m, seed=81)
    sc.add("se_pillow", pillow_down_svg(), z=Z + 2.95, seed=83,
           motion=lambda t: Tf(alpha=1.0 if t_pray <= t < t_snug else 0.0))
    sc.add("se_kidglow", warm_glow_svg(kx + 20, ky - 160, 330, 300, "se_kg"), z=Z + 2.8, blend="screen", wc=0,
           motion=lambda t: Tf(alpha=0.6 * M.progress(t, t_with - 0.2, t_with + 0.8, "sine")
                               * (0.85 + 0.15 * math.sin(t * 2.2))))

    # a little heart floating up from her toward the picture on '想对耶稣说什么呢'
    hx0, hy0 = kx + 60, ky - 300
    th0 = t_say + 0.3

    def heart_m(t):
        u = t - th0
        if u < 0:
            return Tf(alpha=0)
        a = min(1.0, u / 0.25) * (1 - M.progress(u, 1.9, 2.6, "sine"))
        s = 0.4 + 0.6 * M.ease("back")(min(1.0, u / 0.4))
        return Tf(dx=120 * M.ease("out")(min(1.0, u / 2.4)) + 10 * math.sin(u * 4), dy=-150 * M.ease("out")(min(1.0, u / 2.4)),
                  sx=s, sy=s, alpha=a, px=hx0, py=hy0)
    sc.add("se_heart_up", heart_svg(hx0, hy0, 24), z=Z + 4, motion=heart_m, wc=0)

    # ---- end card and heart
    ex, ey = END
    sc.add("se_endcard", end_card_svg(), z=Z + 10, wc=0, motion=M.keys(
        [(t_end, {"alpha": 0, "s": 0.95, "dy": 16}), (t_end + 0.6, {"alpha": 1, "s": 1.0, "dy": 0})], "out",
        pivot=(ex, ey - 50)))
    hx, hy = ex, ey + 74
    th = t_end + 0.45
    sc.add("se_endheart", heart_svg(hx, hy, 30), z=Z + 10.1, wc=0, motion=M.keys(
        [(th, {"alpha": 0, "s": 0.2}), (th + 0.12, {"alpha": 1}), (th + 0.45, {"s": 1.0})], "back", pivot=(hx, hy)))

    # ---- light: the night's cool tint gives way to a warm glow; twinkles in the picture and round her
    fx0, fy0, fx1, fy1 = R.FX0, R.FY0, R.FX0 + R.FRW, R.FY0 + R.FRH
    sc.fx = [
        FX.tint((150, 160, 215), lambda t: 0.16 - 0.11 * calm(t), mode="multiply"),
        FX.tint((255, 214, 160), lambda t: 0.10 * calm(t), mode="screen"),
        FX.sparkles((fx0 - 20, fy0 - 20, fx1 + 20, fy1 + 20), count=10, t0=t_glow - 0.05, t1=t_sw1 + 1.2,
                    size=(9, 17), period=1.2, drift=-10, seed=93),
        FX.sparkles((fx0 + 20, fy0 + 10, fx1 - 20, fy0 + R.FRH * 0.55), count=12, t0=t_obey + 0.2, size=(5, 10),
                    period=1.6, drift=0, seed=95, color=(255, 248, 220)),
        FX.sparkles((kx - 180, ky - 360, kx + 220, ky - 40), count=8, t0=t_with, t1=t_pray + 1.5, size=(8, 15),
                    period=1.5, drift=-12, seed=97),
        FX.sparkles((ex - 420, ey - 120, ex + 420, ey + 40), count=6, t0=t_end + 0.4, size=(9, 16), period=2.0,
                    drift=0, seed=99),
    ]

    # ---- camera: the room -> toward the glowing picture -> back for the gust -> toward her prayer -> wide end
    c_wide = Cam(1030, 588, 1990)
    c_pic = Cam(745, 478, 1470)
    c_pic2 = Cam(760, 455, 1380)
    c_room = Cam(1056, 594, 2010)
    c_pray = Cam(872, 570, 1720)
    c_end = Cam(985, 612, 1880)
    sc.camera = M.cam_keys([(0, c_wide), (t_glow + 0.1, Cam(1010, 584, 1960)), (t_glow + 2.3, c_pic),
                            (t_obey - 0.3, c_pic2), (t_fear - 0.55, c_pic2), (t_fear + 1.15, c_room),
                            (t_near + 0.3, Cam(1000, 590, 1900)), (t_pray + 1.0, c_pray), (p_kid3[1], c_pray),
                            (min(t_end - 0.2, p_kid3[1] + 2.6), c_end), (T, Cam(985, 614, 1850))],
                           ["sine"] * 10)

    # ---- sound
    sc.sfx("wind_soft", 0, dur=t_calm1 + 0.5, gain_db=-20, fade_in=0.8, fade_out=1.5)
    sc.sfx("storm_wind", t_gust - 0.3, dur=1.8, gain_db=-19, fade_in=0.2, fade_out=0.9, pan=0.4)
    sc.sfx("whoosh", t_gust - 0.05, gain_db=-14, pan=0.4)
    sc.sfx("night", t_calm0, dur=T - t_calm0 + 0.3, gain_db=-23, fade_in=1.5, fade_out=1.0)
    sc.sfx("sparkle", t_glow + 0.1, gain_db=-15, pan=-0.3)
    sc.sfx("chime", t_glow + 0.25, gain_db=-14)
    sc.sfx("sparkle", t_jesus, gain_db=-18, pan=-0.3)
    sc.sfx("chime", t_obey + 0.2, gain_db=-14)
    sc.sfx("sparkle", t_with, gain_db=-17)
    sc.sfx("cloth", t_pray - 0.05, gain_db=-18)
    sc.sfx("cloth", t_snug - 0.05, gain_db=-19)
    sc.sfx("pop", th0 + 0.05, gain_db=-17)
    sc.sfx("chime", t_end + 0.1, gain_db=-12)
    return sc
