"""Scene 3 — the jealous officials search Daniel's work and find nothing wrong (Daniel 6:4-5).

Same hall and stage as s02 (stories/daniel/scenes/s02_daniel.py: identical layers, seeds and figure placings), so
the scene opens on s02's last frame: the king with his open hand, Daniel bowing, the two other overseers.

  start        s02's final framing; the king lowers his hand (happy) and Daniel goes back to reading his scroll
  line 0  "可是，别的官员心里很不高兴。"  the two overseers frown (cuts on dips) under little grumble clouds
          "他们嫉妒但以理，想找他的错处。"  they turn and walk off behind the big column (planted-foot strides; the
                                        camera follows) and peek around it at Daniel and whisper; two more officials
                                        are already at the records table
  line 1  "他们找啊找，"                  the two walk on to the table; all four read through scrolls, scrolls fly out
                                        of the basket (whoosh)
          "可是一点错处也找不到，"        a puzzled "?" pops over each head
          "因为但以理又忠心，又诚实。"    the camera pulls back to Daniel, who finishes his scroll and smiles; a warm
                                        glow behind him; the four officials hang their heads
  line 2  (O) "我们找不到他的错。"       the camera returns to the officials (speaking arcs)
          "除非，在他敬拜上帝的事上想办法！"  the leader rubs his hands, a thought bubble shows Daniel kneeling in
                                        prayer; the others whisper and rub their hands too (sly, never scary)
  end     calm hold on the four scheming officials by the records table (s04 opens on this framing).
"""
import math

from art import characters as C
from art import props as PR
from art import style as S
from art.scenes.s17_king import arcs_markup, dip, grumble_markup, nod, question_markup, snap
from art.style import P
from engine import fx as FX
from engine import motion as M
from engine.motion import Tf
from engine.scene import Scene
from stories.daniel.scenes.s02_daniel import (
    FLOOR_Y, KING_OFFER, KS, OVS_END, OVS_S, SH, SW, THRONE_HX, THRONE_Y, actor, add_hall,
    basket_markup, bcam, cam_path, chunk, dan, doc, hx, king_fig, king_ib, off, records_table_markup, scene_offset)

INK = P["ink"]
DX, AX, BX = OVS_END                      # Daniel, overseer A (variant 0), overseer B (variant 2): hall x
A_PEEK, B_PEEK = 1540, 1690               # behind the front column (hall x 1400)
A_X, B_X, C_X, D_X = 1920, 2100, 2290, 2480   # around the records table at the end (s04 starts here)
BASKET = (2620, 1250)
OS = OVS_S


def thought_markup(cx, cy, tx, ty):
    """A cloud thought bubble at (cx, cy) with trailing puffs toward (tx, ty), showing Daniel kneeling in prayer
    at his open window (a tiny picture, warm light)."""
    out = S.cloud(cx, cy, 330, 190, "#fffaf0", seed=77, puffs=6, sw=4, shade_fill="#efe4cc")
    for k, r in ((0.45, 22), (0.7, 15), (0.88, 10)):
        x, y = cx + (tx - cx) * k, cy + 70 + (ty - cy - 70) * k
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fffaf0" stroke="{INK}" stroke-width="3.5"/>'
    # the little window: a wooden frame with open teal shutters and warm light inside
    wx, wy = cx + 6, cy + 70
    out += (f'<rect x="{wx - 70}" y="{wy - 150}" width="140" height="150" fill="#f6dc9a" stroke="{INK}" '
            f'stroke-width="3.5"/><rect x="{wx - 100}" y="{wy - 150}" width="30" height="150" fill="#3b8b89" '
            f'stroke="{INK}" stroke-width="3"/><rect x="{wx + 70}" y="{wy - 150}" width="30" height="150" '
            f'fill="#3b8b89" stroke="{INK}" stroke-width="3"/><rect x="{wx - 84}" y="{wy - 4}" width="168" height="14" '
            f'fill="{P["wood"]}" stroke="{INK}" stroke-width="3"/>')
    out = S.g(out, filter="wobble-fine")
    out += C.daniel(wx + 18, wy + 2, 0.42, -1, pose="kneel_pray")
    return out


def glow_svg(x, y):
    defs = S.rad_grad("d3glow", [(0, "#fff3cc", 1.0), (0.45, "#ffe9ae", 0.6), (1, "#ffe7a8", 0)])
    return doc(f'<ellipse cx="{x}" cy="{y}" rx="300" ry="360" fill="url(#d3glow)"/>', defs)


def build(ctx):
    sc = Scene(ctx, W=SW, H=SH)
    L0, L1, L2 = ctx.lines
    t_off = scene_offset(ctx.id)
    c_jeal = chunk(L0, "嫉妒")
    c_find = chunk(L1, "找啊找")
    c_faith = chunk(L1, "忠心")
    c_cant = chunk(L2, "找不到他的错")
    c_unless = chunk(L2, "除非")

    add_hall(sc, z0=3, t_off=t_off)
    sc.add("table", doc(records_table_markup()), z=6.6, seed=130)
    sc.add("basket", doc(basket_markup(hx(BASKET[0]), BASKET[1], 0.9)), z=7.6, seed=131)

    # ---------------- the king (s02's last drawing, then he lowers his hand, happy)
    kp = (hx(THRONE_HX), THRONE_Y)
    t_settle = 1.15
    sc.add("king", [doc(king_ib(KING_OFFER, "happy")), doc(king_fig("sit_throne", "happy"))], z=5, seed=120,
           frame_at=lambda t: 0.0 if t < snap(t_settle) else 1.0,
           motion=M.combine(dip(snap(t_settle), KS, kp, 4), M.breathe(0.008, 3.2, pivot=kp, phase=0.3 + t_off / 3.2)))

    # ---------------- Daniel: bowing (s02) -> reading diligently -> finishes and smiles
    x = hx(DX)
    dp = (x, FLOOR_Y)
    t_read = 1.3
    t_done = c_faith.start + 0.25
    t_read2 = c_faith.end + 0.9
    dfr = [dan(x, FLOOR_Y, "bow", -1, s=OS), dan(x, FLOOR_Y, "read", -1, s=OS),
           dan(x, FLOOR_Y, "stand", -1, "happy", s=OS)]

    def read_sway(t):
        if t_read + 0.3 < t < t_done or t > t_read2 + 0.3:
            return Tf(rot=1.0 * math.sin(2 * math.pi * (t - t_read) / 2.4))
        return Tf()
    actor(sc, "daniel", 7.2, [None, None] + dfr, dp, OS, seed=121,
          base=[(0, 2), (snap(t_read), 3), (snap(t_done), 4), (snap(t_read2), 3)],
          bumps=[dip(snap(t_read), OS, dp), dip(snap(t_done), OS, dp), nod(t_done + 0.25, dp, -3, 0.6),
                 dip(snap(t_read2), OS, dp), M.with_pivot(read_sway, dp)],
          breathe=(0.01, 3.0, t_off / 3.0))
    sc.add("dglow", glow_svg(x, FLOOR_Y - 190), z=7.1, wc=0, blend="screen",
           motion=M.keys([(t_done - 0.1, {"alpha": 0}), (t_done + 0.6, {"alpha": 1}), (c_faith.end + 0.4, {"alpha": 1}),
                          (c_faith.end + 1.2, {"alpha": 0})], "sine"))

    # ---------------- the two jealous overseers (A: crimson, B: rust)
    t_frown = (L0.start + 0.7, L0.start + 0.85)
    t_turn = (c_jeal.start + 0.05, c_jeal.start + 0.15)
    t_scheme = c_unless.start + 0.1
    sad_t = c_faith.start + 0.9
    walk2 = (c_find.start + 0.1, c_find.start + 0.2)
    marks = []
    leaders = {}
    for who, (v, sx_, peek_x, end_x, z) in enumerate(((0, AX, A_PEEK, A_X, 7.3), (2, BX, B_PEEK, B_X, 7.4))):
        x = hx(sx_)
        ap = (x, FLOOR_Y)
        n1 = max(2, round((peek_x - sx_) / (87 * OS)))
        n2 = max(2, round((end_x - peek_x) / (87 * OS)))
        t1 = t_turn[who] + 0.2
        t1e = snap(t1 + n1 * 0.27)
        t2 = walk2[who]
        t2e = snap(t2 + n2 * 0.27)
        lead = who == 0
        fr = [off(x, FLOOR_Y, v, "walk_a", 1, s=OS), off(x, FLOOR_Y, v, "walk_b", 1, s=OS),
              off(x, FLOOR_Y, v, "stand", -1, s=OS), off(x, FLOOR_Y, v, "stand", -1, "angry", s=OS),
              off(x, FLOOR_Y, v, "stand", 1, "angry", s=OS),
              off(x, FLOOR_Y, v, "peek" if lead else "whisper", -1, s=OS),
              off(x, FLOOR_Y, v, "read", 1 if lead else -1, s=OS),
              off(x, FLOOR_Y, v, "sad", 1 if lead else -1, s=OS),
              off(x, FLOOR_Y, v, "scheme" if lead else "whisper", 1 if lead else -1, s=OS)]
        t_peek = t1e + 0.12
        t_rd = t2e + 0.12
        t_sad = sad_t + 0.15 * who
        t_sch = t_scheme + (0 if lead else 0.6)
        base = [(0, 2), (snap(t_frown[who]), 3), (snap(t_turn[who]), 4), (snap(t_peek), 5), (snap(t_rd), 6),
                (snap(t_sad), 7), (snap(t_sch), 8)]
        actor(sc, "ovA" if lead else "ovB", z, fr, ap, OS, seed=122 + who, base=base,
              walks=[(t1, n1, (peek_x - sx_) / n1), (t2, n2, (end_x - peek_x) / n2)],
              bumps=[dip(snap(t_frown[who]), OS, ap, 6), dip(snap(t_turn[who]), OS, ap, 5),
                     dip(snap(t_peek), OS, ap, 7), dip(snap(t_rd), OS, ap), dip(snap(t_sad), OS, ap, 6),
                     dip(snap(t_sch), OS, ap)],
              breathe=(0.01, 3.0, 0.3 * (who + 1) + t_off / 3.0))
        head = C.body_points(C.official, hx(sx_), FLOOR_Y, OS, -1, variant=v, pose="stand")["head"]
        # grumble cloud over the head while they frown (follows nothing: they stand still then)
        gx, gy = head[0], head[1] - 175
        sc.add(f"grumble{who}", [doc(grumble_markup(gx, gy, 0.8, seed=k + 3 * who)) for k in range(3)], z=9.6,
               wc=0, frame_at=lambda t: float(int(t * 6) % 3),
               motion=M.keys([(t_frown[who] + 0.1, {"alpha": 0, "s": 0.7}), (t_frown[who] + 0.35, {"alpha": 1, "s": 1}),
                              (t_turn[who] - 0.25, {"alpha": 1}), (t_turn[who] + 0.05, {"alpha": 0})],
                             "sine", pivot=(gx, gy)))
        marks.append((hx(end_x), head[1] - 120, t_rd))
        leaders[who] = hx(end_x)

    # ---------------- two more officials, already at the records table (C: green turban, D: mustard turban)
    for name, v, x_, fac, z, ph in (("ovC", 1, C_X, 1, 7.25, 0.15), ("ovD", 3, D_X, -1, 7.45, 0.55)):
        x = hx(x_)
        ap = (x, FLOOR_Y)
        fr = [off(x, FLOOR_Y, v, "read", fac, s=OS), off(x, FLOOR_Y, v, "sad", fac, s=OS),
              off(x, FLOOR_Y, v, "scheme" if v == 1 else "whisper", fac, s=OS)]
        t_sad = sad_t + (0.3 if v == 1 else 0.45)
        t_sch = t_scheme + (1.2 if v == 1 else 1.5)

        def look(t, ph=ph, t_sad=t_sad):
            return Tf(rot=1.2 * math.sin(2 * math.pi * (t / 2.1 + ph))) if t < t_sad else Tf()
        actor(sc, name, z, [None, None] + fr, ap, OS, base=[(0, 2), (snap(t_sad), 3), (snap(t_sch), 4)],
              bumps=[M.with_pivot(look, ap), dip(snap(t_sad), OS, ap, 6), dip(snap(t_sch), OS, ap)],
              breathe=(0.01, 3.0, ph + t_off / 3.0), seed=126 if v == 1 else 127)
        marks.append((x, FLOOR_Y - 400 * OS - 10, None))

    # ---------------- scrolls tossed out of the basket while they search
    bx, by = hx(BASKET[0]), BASKET[1] - 150
    for i, (t0, vx, rot) in enumerate(((c_find.start + 0.8, -260, -340), (c_find.start + 1.7, 180, 300),
                                       (c_find.start + 2.5, -120, -260))):
        def toss(t, t0=t0, vx=vx, rot=rot):
            u = t - t0
            if u < 0 or u > 1.1:
                return Tf(alpha=0)
            return Tf(dx=vx * u, dy=-620 * u + 900 * u * u, rot=rot * u, alpha=min(1, u / 0.06, (1.1 - u) / 0.2),
                      px=bx, py=by)
        sc.add(f"toss{i}", doc(PR.scroll(bx, by, 0.55, opened=i == 1)), z=9.7, motion=toss)
        sc.sfx("whoosh", t0, gain_db=-18, pan=0.3)

    # ---------------- "?" over every head ("一点错处也找不到")
    t_q = c_find.start + 0.55 * (c_find.end - c_find.start)
    order = sorted(marks, key=lambda m: m[0])
    for i, (mx, my, _) in enumerate(order):
        t0 = t_q + 0.18 * i
        sc.add(f"q{i}", doc(question_markup(mx, my, 0.9)), z=9.8, wc=0,
               motion=M.keys([(t0, {"alpha": 0, "s": 0.5}), (t0 + 0.2, {"alpha": 1, "s": 1.08}),
                              (t0 + 0.35, {"s": 1.0}), (c_faith.start + 0.5, {"alpha": 1}),
                              (c_faith.start + 0.9, {"alpha": 0})], ["out", "sine", "sine", "sine"], pivot=(mx, my)))
        sc.sfx("pop", t0, gain_db=-19, pan=0.15 * (i - 1.5))

    # ---------------- speaking arcs and the thought bubble
    ax_ = leaders[0]
    ahead = C.body_points(C.official, ax_, FLOOR_Y, OS, 1, variant=0, pose="stand")["head"]
    sc.add("arcs", [doc(arcs_markup(ahead[0] + 46 * OS, ahead[1] + 26 * OS, 1, k, OS)) for k in (1, 2, 3)], z=9.8,
           wc=0, frame_at=lambda t: float(int(t * 7) % 3),
           motion=M.keys([(L2.start, {"alpha": 0}), (L2.start + 0.12, {"alpha": 1}), (c_cant.end - 0.1, {"alpha": 1}),
                          (c_cant.end + 0.05, {"alpha": 0}), (c_unless.start, {"alpha": 0}),
                          (c_unless.start + 0.12, {"alpha": 1}), (L2.end - 0.15, {"alpha": 0})], "sine"))
    bub = (ax_ + 120, 600)
    t_bub = c_unless.start + 0.55
    sc.add("bubble", doc(thought_markup(bub[0], bub[1], ahead[0] + 30, ahead[1] - 90)), z=9.9, wc=0.5,
           motion=M.keys([(t_bub, {"alpha": 0, "s": 0.6}), (t_bub + 0.3, {"alpha": 1, "s": 1.05}),
                          (t_bub + 0.5, {"s": 1.0}), (L2.end + 0.1, {"alpha": 1}), (L2.end + 0.6, {"alpha": 0})],
                         ["out", "sine", "sine", "sine"], pivot=(bub[0], bub[1] + 60)))

    # ---------------- camera (s02's last framing first)
    sc.camera = cam_path([
        (0.0, bcam(hx(780), 1900), 0),
        (c_jeal.start + 0.1, bcam(hx(780), 1900), 0),
        (c_jeal.start + 2.6, bcam(hx(1650), 1900), 0),
        (c_find.start + 0.1, bcam(hx(1650), 1900), 0),
        (c_find.start + 1.9, bcam(hx(2050), 1900), 0),
        (c_faith.start - 0.1, bcam(hx(2050), 1900), 0),
        (c_faith.start + 2.0, bcam(hx(1620), 2420), 0),
        (L2.start - 0.4, bcam(hx(1620), 2420), 0),
        (L2.start + 1.8, bcam(hx(2050), 1900), 0),
    ])
    sc.fx = [FX.sparkles((hx(DX) - 170, 690, hx(DX) + 170, 850), count=8, t0=t_done + 0.2, t1=c_faith.end + 1.0,
                         color=(255, 240, 190), size=(8, 15), period=1.7, drift=-8, seed=31),
             FX.motes((hx(950), 520, hx(2900), 1250), count=40, t0=0, color=(255, 246, 214), size=(2, 5), alpha=110,
                      seed=22)]

    # ---------------- sound
    sc.sfx("cloth", t_settle - 0.05, gain_db=-17)
    sc.sfx("cloth", t_read - 0.05, gain_db=-15)
    sc.sfx("footsteps", t_turn[0] + 0.2, dur=1.9, gain_db=-14, fade_in=0.05, fade_out=0.25, rate=1 / 0.27)
    sc.sfx("cloth", t_turn[0] + 2.0, gain_db=-16)
    sc.sfx("footsteps", walk2[0], dur=2.0, gain_db=-14, fade_in=0.05, fade_out=0.25, rate=1 / 0.27)
    sc.sfx("cloth", walk2[0] + 2.0, gain_db=-14)
    sc.sfx("sparkle", t_done + 0.1, gain_db=-17)
    sc.sfx("cloth", t_scheme, gain_db=-15)
    sc.sfx("pop", t_bub, gain_db=-16)
    return sc
