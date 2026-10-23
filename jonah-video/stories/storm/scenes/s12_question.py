"""Scene 12 - the gentle question (Mark 4:40): 耶稣转过身来，温柔地问门徒： /
Z 你们为什么这样害怕呢？你们还没有信心吗？

The shared boat world of s08_storm, on the silver calm (opens on s11's last frame: plain cross-dissolve); a
page-turn dip leads to s13 (another illustrator), so it ends on a calm, readable frame.

Beats (voice-measured phrase marks of the take):
  start          the calm, wide (= s11's end): moon and stars, the moon's path on the still lake, Jesus standing on
                 the stern deck looking out over the water, the wet disciples in wonder.
  '耶稣转过身来'  the camera moves in close and intimate; Jesus turns round to his friends (turn_kind: both hands
                 open, head tilted, a soft warm light round him).
  '温柔地问门徒'  the disciples lower their hands and look up at him, awed.
  Z '你们为什么这样害怕呢？' Jesus asks gently (a small nod on each phrase); the disciples glance at each other,
                 a little ashamed (Thomas and Peter turn to each other, Andrew looks down); James pulls off his
                 soaked kerchief and wrings it out (drips).
  '你们还没有信心吗？' they hang their heads a little; Jesus' face softens into a kind smile.
  end            calm hold.
"""
import math

from art import characters as C
from art import props as PR
from engine.motion import Cam
from engine.scene import Scene

from .s08_storm import (BP, CALM_BOB, CALM_TILT, CREW, DECK_X, DECK_Y, K, SH, SW, Actor, Rock, Twinkle, add_boat,
                        add_calm_lake, add_moon, add_night, add_sail, beat, breath, cam_path, dip,
                        disciple, foot_of, hop, jesus_body, snap, voice_marks)
from .s10_wake import add_glow
from .s11_calm import CAM_END as S11_CAM_END
from .s11_calm import GLOW_CALM, STAND_GLOW, add_night_clouds, calm_body


def wring_body(name, k, facing=1):
    """A disciple wringing out his soaked kerchief (head bare, the twisted cloth between his fists, drips falling);
    k = 0..2 twist phase. Built on the characters rig (a custom pose of the disciples' own design)."""
    v, lx, row = CREW[name]
    x, y = foot_of(name)
    D, m = C._disciple_design(v, 0.0, True)
    cloth = {0: "#c0623f", 1: "#4f9a94", 2: "#ece0c4", 6: "#efe2c4", 10: "#a8bb8a"}.get(v, "#ece0c4")
    cloth = PR.S.shade(cloth, -0.18)
    if D.get("hat") and D["hat"][0] == "custom":
        D["hat"] = None
        D.pop("hat_h", None)
        D.pop("ears", None)
    tw = (0, 1, 2)[k % 3]
    fa = (78 + 4 * tw, -276 - 6 * tw)            # far fist (twisting up)
    na = (42 - 3 * tw, -258 + 5 * tw)            # near fist (twisting down)

    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        dx, dy = W0[0] - W1[0], W0[1] - W1[1]
        n = max(1.0, math.hypot(dx, dy))
        ux, uy = dx / n, dy / n
        a = (W1[0] - ux * 26, W1[1] - uy * 26)
        b = (W0[0] + ux * 26, W0[1] + uy * 26)
        s = (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" fill="none" stroke="{PR.INK}" '
             f'stroke-width="22" stroke-linecap="round"/>'
             f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" fill="none" stroke="{cloth}" '
             f'stroke-width="15" stroke-linecap="round"/>')
        for j in range(5):                       # the twist
            u = (j + 0.5 + 0.33 * tw) / 5
            px, py = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            s += (f'<path d="M{px - uy * 7 - ux * 4:.1f},{py + ux * 7 - uy * 4:.1f} L{px + uy * 7 + ux * 4:.1f},'
                  f'{py - ux * 7 + uy * 4:.1f}" stroke="{PR.S.shade(cloth, -0.35)}" stroke-width="2.6" '
                  f'stroke-linecap="round"/>')
        mx, my = (W0[0] + W1[0]) / 2, (W0[1] + W1[1]) / 2 + 14
        for j, (ddx, ddy) in enumerate(((-6, 18), (4, 46), (-2, 78))):
            yy = my + ddy + 10 * ((tw + j) % 3)
            s += (f'<path d="{PR._raindrop_d(mx + ddx, yy, 6)}" fill="{PR.STORM_WATER[3]}" stroke="{PR.INK}" '
                  f'stroke-width="2"/>')
        return s + C._fist(W1, hr, D["skin"]) + C._fist(W0, hr, D["skin"])
    D["front"] = C._hooks(front)
    ps = C._P(t=6, h=14, legs=((8, 3), (-7, -3)), arms=(("ik", "abs", fa[0], fa[1], 1), ("ik", "abs", na[0], na[1], 1)),
              hands=("fist", "fist"), expr="ashamed", look=(0.02, 0.05))
    inner, _ = C._figure(D, m, ps, "ashamed", C._fsign(facing), True)
    return C._wrap_out(inner, x, y, K, facing, f"disciple{v}-wring")


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    T = ctx.duration

    t_turn = beat(ctx, 0, "转过身")
    t_gentle = beat(ctx, 0, "温柔")
    t_ask = beat(ctx, 0, "问门徒")
    t_q1 = beat(ctx, 1, "你们为什么")
    t_afraid = beat(ctx, 1, "害怕")
    t_q2 = beat(ctx, 1, "你们还没有")
    t_faith = beat(ctx, 1, "信心")
    t_end = ctx.lines[1].end
    t_spin = snap(t_turn + 0.12)

    # ---------------- camera: from the wide calm in close and intimate
    C11b = S11_CAM_END
    C12 = Cam(1400, 930, 1480)
    sc.camera = cam_path([(0, C11b), (t_turn - 0.25, C11b), (t_ask + 0.2, C12), (T, C12)])

    rock = Rock(ctx, lambda t: CALM_TILT, lambda t: CALM_BOB)

    # ---------------- the calm night (= s11's end)
    add_night(sc, ctx, progress=lambda t: 1.0)
    add_moon(sc, halo=lambda t: 1.0, disc=lambda t: 1.0, hills=lambda t: 1.0)
    add_night_clouds(sc, ctx, lambda t: 0.85, lambda t: 1.0)
    sc.fx.append(Twinkle(ctx, lambda t: 1.0))
    add_calm_lake(sc, ctx, glow=1.0, name="calm_moon", z=4.1)
    add_boat(sc, ctx, rock, lambda t: 1.0, [0.8], lambda t: 0.0, slosh=lambda t: False, lantern_amp=lambda t: 1.5)
    add_sail(sc, ctx, rock, [(0, "furled", 0)])

    # ---------------- Jesus turns round to his friends and asks them gently
    up = Actor(ctx, "jesus_up", (DECK_X, DECK_Y), rock, z=12.0)
    up.at(0, jesus_body("stand", expr="kind", facing=-1))
    up.at(t_spin, jesus_body("turn_kind", facing=1))
    up.at(snap(t_end + 0.05), jesus_body("turn_kind", expr="kind", facing=1))
    nods = []
    for ent in voice_marks(ctx, 1):          # a small nod on each phrase of the question
        nods.append(hop(ent[1], [(0, {"dy": 0, "rot": 0}), (0.18, {"dy": 3 * K, "rot": 1.2}), (0.5, {"dy": 0, "rot": 0})],
                        ["sine", "sine"]))
    up.move(dip(t_spin, 7.0), dip(snap(t_end + 0.05), 3.0), breath(ctx, 0.008, 3.4, 0.2), *nods)
    up.add(sc)
    add_glow(sc, ctx, rock, "glow_stand", STAND_GLOW, lambda t: GLOW_CALM)

    # ---------------- the disciples: awed, then a little ashamed
    look_t = {"andrew": 0.0, "james": 0.1, "philip": 0.18, "thomas": 0.26, "peter": 0.34, "matthew": 0.42,
              "john": 0.5, "bartholomew": 0.58}
    ashamed = {   # name: (pose, facing, expr, delay after 害怕)
        "andrew": ("stand", -1, "ashamed", 0.0), "thomas": ("stand", 1, "ashamed", 0.12),
        "peter": ("stand", -1, "ashamed", 0.2), "john": ("stand", -1, "ashamed", 0.3),
        "philip": ("stand", -1, "ashamed", 0.36), "matthew": ("stand", 1, "ashamed", 0.44),
        "bartholomew": ("stand", -1, "ashamed", 0.5), "thaddaeus": ("stand", -1, "ashamed", 0.58),
    }
    for k, name in enumerate(CREW):
        foot = BP["cling"] if name == "peter" else foot_of(name)
        a = Actor(ctx, name, foot, rock)
        a.at(0, calm_body(name))
        cuts = []
        if name in look_t:
            tl = snap(t_ask + look_t[name])
            a.at(tl, disciple(name, "stand", expr="awed", wet=True, facing=-1))
            cuts.append(tl)
        if name in ashamed:
            pose, fc, ex, dl = ashamed[name]
            ta = snap(t_afraid + dl)
            a.at(ta, disciple(name, pose, expr=ex, wet=True, facing=fc))
            cuts.append(ta)
            if name in ("thomas", "matthew"):
                tb = snap(t_faith + 0.1 + 0.1 * (name == "matthew"))
                a.at(tb, disciple(name, "stand", expr="ashamed", wet=True, facing=-1))
                cuts.append(tb)
        if name == "james":                  # pulls off his soaked kerchief and wrings it out
            tw = snap(t_q1 + 0.35)
            a.cycle(tw, [wring_body(name, i) for i in range(3)], step=5)
            cuts.append(tw)
        for tc in cuts:
            a.move(dip(tc, 6.0))
        a.move(breath(ctx, 0.007, 3.0 + 0.2 * k, k * 0.13))
        a.add(sc)

    # ---------------- sound
    sc.sfx("waves_calm", 0.0, dur=T, gain_db=-20, fade_in=0.8, fade_out=0.8)
    sc.sfx("night", 0.0, dur=T, gain_db=-24, fade_in=0.8, fade_out=0.8)
    sc.sfx("cloth", t_spin, gain_db=-14)
    sc.sfx("drip", snap(t_q1 + 0.45), dur=t_end - t_q1, gain_db=-20, fade_in=0.3, fade_out=0.6, pan=0.15)
    sc.sfx("sparkle", t_end + 0.1, gain_db=-18)
    return sc
