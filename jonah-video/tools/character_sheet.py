"""Render labelled contact sheets of the people library (art/characters.py).

Every function / pose / expression is drawn on cream paper exactly as the film shows it
(SVG -> engine.raster.rasterize -> engine.watercolor.watercolor). A small red cross marks each
figure's anchor point (x, y) and a faint line marks the ground (not drawn on the clipped close-up
sheet, whose anchors fall outside their cells).

  python3 tools/character_sheet.py            # all sheets
  python3 tools/character_sheet.py jonah      # only sheets whose name contains "jonah"
  python3 tools/character_sheet.py --bbox     # measure every figure alone at scale 1 -> characters_bbox.json

Output: build/preview/characters_*.png (each <= 2400 px wide):
  jonah_poses, jonah_expr (close-ups), jonah_small (scale 0.45 readability, both facings + expressions),
  sailors, captain_king, citizens, citizens_poses, compositions (figures used together on backgrounds);
  Daniel film: daniel_poses, daniel_expr, daniel_officials, daniel_darius, daniel_guards
  (python3 tools/character_sheet.py daniel).
  David film (python3 tools/character_sheet.py david): david_poses, david_items (staff / basket / bag / sling
  phases), david_expr (close-ups), david_armor, goliath (poses, fall progress, lying), goliath_expr, soldiers_israel,
  soldiers_philistine, david_saul (king attire='saul', Eliab, Jesse, shield-bearer) and david_scale (boy / adult /
  giant on one ground line).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from art import characters as C  # noqa: E402
from art import style as S  # noqa: E402
from engine import raster  # noqa: E402
from engine.paths import BUILD, FONT_BOLD, FONT_REGULAR  # noqa: E402
from engine.scene import BOIL_TOKEN  # noqa: E402
from engine.watercolor import apply_paper, paper_multiplier, watercolor  # noqa: E402

OUT = BUILD / "preview"
LABEL_H = 34
INK_RGB = (75, 52, 38)


def _finish(fig, W, H, title, under=None):
    """Composite a rasterised, watercoloured figure layer on paper; returns (PIL RGB sheet, draw)."""
    paper = Image.new("RGBA", (W, H), S.hex_rgb(S.P["paper"]) + (255,))
    if under is not None:
        paper = Image.alpha_composite(paper, under)
    sheet = Image.alpha_composite(paper, fig)
    rgb = apply_paper(np.asarray(sheet.convert("RGB")), paper_multiplier(W, H))
    sheet = Image.fromarray(rgb)
    d = ImageDraw.Draw(sheet)
    d.text((18, 14), title, fill=INK_RGB, font=ImageFont.truetype(str(FONT_BOLD), 34))
    return sheet, d


def render_sheet(name, title, items, cols, cell_w, cell_h, scale, ground_pad=26, clip_cells=False):
    """items: list of (label, fn) where fn(x, y, scale) -> SVG <g> markup."""
    rows = (len(items) + cols - 1) // cols
    top = 64
    W, H = cols * cell_w, top + rows * cell_h
    body = ""
    defs = ""
    anchors = []
    for i, (label, fn) in enumerate(items):
        cx = (i % cols) * cell_w + cell_w / 2
        cy = top + (i // cols) * cell_h + cell_h - LABEL_H - ground_pad
        anchors.append((cx, cy, label))
        g = fn(cx, cy, scale)
        if clip_cells:
            cid = f"cell{i}"
            x0 = (i % cols) * cell_w
            y0 = top + (i // cols) * cell_h
            defs += (f'<clipPath id="{cid}"><rect x="{x0 + 4}" y="{y0 + 4}" width="{cell_w - 8}" '
                     f'height="{cell_h - LABEL_H - 6}"/></clipPath>')
            g = f'<g clip-path="url(#{cid})">{g}</g>'
        body += g
    svg = S.svg_doc(body, defs=defs, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = watercolor(raster.rasterize(svg, W, H), seed=11)
    ground = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not clip_cells:            # anchors of clipped close-ups lie outside their cells: no overlays
        gd = ImageDraw.Draw(ground)
        for cx, cy, lab in anchors:
            if not lab:           # blank padding cell
                continue
            gd.line([(cx - cell_w * 0.42, cy), (cx + cell_w * 0.42, cy)], fill=(214, 196, 160, 255), width=2)
    sheet, d = _finish(fig, W, H, title, under=ground)
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    bboxes = {}
    alpha = np.asarray(fig)[..., 3]
    for i, (cx, cy, label) in enumerate(anchors):
        x0 = int((i % cols) * cell_w)
        y0 = int(top + (i // cols) * cell_h)
        d.text((x0 + 10, y0 + cell_h - LABEL_H + 4), label, fill=INK_RGB, font=font)
        if not clip_cells and label:
            d.line([(cx - 7, cy), (cx + 7, cy)], fill=(200, 40, 40), width=2)
            d.line([(cx, cy - 7), (cx, cy + 7)], fill=(200, 40, 40), width=2)
        d.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h - 1], outline=(222, 206, 176))
        a = alpha[y0:y0 + cell_h - LABEL_H, x0:x0 + cell_w]
        ys, xs = np.nonzero(a > 40)
        if len(xs):
            bboxes[label] = [round((x0 + xs.min() - cx) / scale), round((y0 + ys.min() - cy) / scale),
                             round((x0 + xs.max() - cx) / scale), round((y0 + ys.max() - cy) / scale)]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"characters_{name}.png"
    sheet.save(path)
    return path, bboxes


def _j(pose, expr=None, facing=1, wet=False):
    return lambda x, y, s: C.jonah(x, y, s, facing, pose=pose, expr=expr, wet=wet)


def sheets():
    out = []
    jp = list(C.JONAH_POSES)
    out.append(("jonah_poses", "Jonah — poses (scale 1, facing=1; red cross = anchor)",
                [(p, _j(p)) for p in jp], 6, 380, 470, 1.0, {"ground_pad": 52}))
    items = [(e, _j("stand", e)) for e in C.EXPRESSIONS]
    items += [("wet=True stand", _j("stand", "sad", wet=True)), ("wet float", _j("float", wet=True)),
              ("wet kneel_pray", _j("kneel_pray", wet=True)), ("facing=-1 happy", _j("stand", "happy", -1)),
              ("facing=-1 scared", _j("stand", "scared", -1)), ("listen", _j("listen")),
              ("sit_faint (tired)", _j("sit_faint"))]
    out.append(("jonah_expr", "Jonah — expressions and wet=True (scale 1.5, upper body)", items, 8, 290, 360, 1.5,
                {"clip_cells": True, "ground_pad": -185}))
    cols = 11

    def pad(group):               # keep every group on whole rows so the title's row numbers stay true
        return group + [("", lambda x, y, s: "")] * (-len(group) % cols)
    items = pad([(p, _j(p)) for p in jp]) + pad([(p + " -1", _j(p, facing=-1)) for p in jp])
    items += pad([(e, _j("stand", e)) for e in C.EXPRESSIONS] + [("wet", _j("stand", wet=True))])
    out.append(("jonah_small", ("Jonah — readability at scale 0.45 (rows 1-2 facing=1, rows 3-4 facing=-1, "
                                "rows 5-6 expressions)"), items, cols, 190, 230, 0.45, {"ground_pad": 14}))
    items = []
    for v in range(4):
        for p in C.SAILOR_POSES:
            items.append((f"v{v} {p}", lambda x, y, s, v=v, p=p: C.sailor(x, y, s, 1, variant=v, pose=p)))
    out.append(("sailors", "Sailors — variants 0-3 x poses (scale 0.8)", items, 8, 290, 340, 0.8, {}))
    items = [(f"captain {p}", lambda x, y, s, p=p: C.captain(x, y, s, 1, pose=p)) for p in C.CAPTAIN_POSES]
    items += [(f"king {p}", lambda x, y, s, p=p: C.king(x, y, s, 1, pose=p, attire="royal"))
              for p in C.KING_POSES if p != "sit_ashes"]
    items += [("king throne=False", lambda x, y, s: C.king(x, y, s, 1, pose="sit_throne", throne=False))]
    items += [(f"sack {p}", lambda x, y, s, p=p: C.king(x, y, s, 1, pose=p, attire="sackcloth"))
              for p in C.KING_POSES]
    out.append(("captain_king", "Captain and King of Nineveh (scale 0.85; 'sack' = attire='sackcloth')", items,
                7, 330, 400, 0.85, {}))
    items = []
    for k in C.CITIZEN_KINDS:
        for v in range(4):
            items.append((f"{k} v{v}", lambda x, y, s, k=k, v=v: C.citizen(x, y, s, 1, kind=k, variant=v)))
    out.append(("citizens", "Citizens — kinds x variants (stand, scale 0.8)", items, 8, 280, 330, 0.8, {}))
    items = []
    poses = ["walk", "listen", "kneel_pray", "point", "sad", "cheer"]
    for k in C.CITIZEN_KINDS:
        for i, p in enumerate(poses):
            items.append((f"{k} {p}", lambda x, y, s, k=k, p=p, i=i: C.citizen(x, y, s, 1, kind=k, variant=i % 4,
                                                                             pose=p)))
    for i, k in enumerate(C.CITIZEN_KINDS):
        for p in ("stand", "kneel_pray"):
            items.append((f"{k} sack {p}", lambda x, y, s, k=k, p=p, i=i: C.citizen(
                x, y, s, 1, kind=k, variant=i, pose=p, attire="sackcloth")))
    out.append(("citizens_poses", "Citizens — poses and sackcloth (scale 0.8)", items, 8, 280, 330, 0.8, {}))
    # ---- Daniel film
    items = [("jonah (compare)", _j("stand"))]
    items += [(p, lambda x, y, s, p=p: C.daniel(x, y, s, pose=p)) for p in C.DANIEL_POSES]
    out.append(("daniel_poses", "Daniel — poses (scale 1; Jonah for comparison)", items, 7, 290, 470, 1.0,
                {"ground_pad": 30}))
    items = [(e, lambda x, y, s, e=e: C.daniel(x, y, s, expr=e)) for e in C.EXPRESSIONS]
    items += [(f"official v{v} {e}", lambda x, y, s, v=v, e=e: C.official(x, y, s, variant=v, expr=e))
              for v in range(4) for e in ("sly", "smug")]
    out.append(("daniel_expr", "Daniel expressions; officials sly / smug (scale 1.5, upper body)", items, 8, 290,
                380, 1.5, {"clip_cells": True, "ground_pad": -200}))
    items = [(f"v{v} {p}", lambda x, y, s, v=v, p=p: C.official(x, y, s, variant=v, pose=p))
             for v in range(4) for p in C.OFFICIAL_POSES]
    out.append(("daniel_officials", "Officials — variants 0-3 x poses (scale 0.8)", items, 10, 230, 360, 0.8,
                {"ground_pad": 20}))
    items = [("nineveh king (compare)", lambda x, y, s: C.king(x, y, s))]
    items += [(p, lambda x, y, s, p=p: C.king(x, y, s, pose=p, attire="darius")) for p in C.KING_POSES
              if p != "sit_ashes"]
    out.append(("daniel_darius", "King Darius — king(attire='darius') poses (scale 0.85)", items, 9, 250, 420, 0.85,
                {"ground_pad": 20}))
    items = [(f"v{v} {p}", lambda x, y, s, v=v, p=p: C.guard(x, y, s, variant=v, pose=p))
             for v in range(4) for p in C.GUARD_POSES]
    out.append(("daniel_guards", "Palace guards — variants 0-3 x poses (scale 0.8)", items, 10, 230, 400, 0.8,
                {"ground_pad": 20}))
    out += david_sheets()
    return out


def david_sheets():
    """Sheets for the David film (1 Samuel 17)."""
    out = []
    items = [("jonah (compare)", _j("stand"))]
    items += [(p, lambda x, y, s, p=p: C.david(x, y, s, pose=p)) for p in C.DAVID_POSES]
    out.append(("david_poses", "David — poses (scale 1; Jonah for comparison; bag=True default)", items, 9, 260, 380,
                1.0, {"ground_pad": 24}))
    items = [(f"staff {p}", lambda x, y, s, p=p: C.david(x, y, s, pose=p, staff=True)) for p in ("stand", "walk_a", "walk_b")]
    items += [(f"basket {p}", lambda x, y, s, p=p: C.david(x, y, s, pose=p, basket=True)) for p in ("stand", "walk_a", "walk_b")]
    items += [("hold_sling staff=True", lambda x, y, s: C.david(x, y, s, pose="hold_sling", staff=True)),
              ("bag=False stand", lambda x, y, s: C.david(x, y, s, bag=False)),
              ("facing=-1 point_up", lambda x, y, s: C.david(x, y, s, -1, pose="point_up"))]
    items += [(f"sling_spin phase={ph}", lambda x, y, s, ph=ph: C.david(x, y, s, pose="sling_spin", phase=ph))
              for ph in (0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875)]
    items += [("hold_sling stone=False", lambda x, y, s: C.david(x, y, s, pose="hold_sling", stone=False))]
    out.append(("david_items", "David — staff / basket / sling options (scale 1)", items, 9, 260, 400, 1.0,
                {"ground_pad": 24}))
    items = [(e, lambda x, y, s, e=e: C.david(x, y, s, expr=e)) for e in
             ("happy", "brave", "puzzled", "worried", "laugh", "surprised", "scared", "peaceful")]
    items += [(f"goliath {e}", lambda x, y, s, e=e: C.goliath(x, y, s * 0.42, expr=e, spear=False)) for e in
              ("angry", "sneer", "laugh", "surprised", "roar", "dizzy")]
    items += [(f"saul {e}", lambda x, y, s, e=e: C.king(x - 10 * s, y + 70 * s, s * 0.82, attire="saul", expr=e)) for e in
              ("worried", "surprised", "kind")]
    items += [(f"eliab {e}", lambda x, y, s, e=e: C.eliab(x, y, s * 0.92, expr=e)) for e in ("cross", "neutral")]
    items += [(f"jesse {e}", lambda x, y, s, e=e: C.jesse(x, y, s, expr=e)) for e in ("happy", "neutral")]
    out.append(("david_expr", "David-film expressions (close-ups; Goliath at 0.42 x, Saul 0.82 x)", items, 8, 270, 330,
                1.5, {"clip_cells": True, "ground_pad": -150}))
    items = [(p, lambda x, y, s, p=p: C.david(x, y, s, pose=p, armor=True)) for p in
             ("stand", "walk_a", "walk_b", "armor_wobble", "talk")]
    items += [(f"{e}", lambda x, y, s, e=e: C.david(x, y, s, pose="stand", armor=True, expr=e)) for e in
              ("puzzled", "laugh")]
    out.append(("david_armor", "David in Saul's armour — armor=True (scale 1)", items, 7, 300, 400, 1.0,
                {"ground_pad": 24}))
    items = [(p, lambda x, y, s, p=p: C.goliath(x, y, s, pose=p)) for p in
             ("stand", "stride_a", "stride_b", "shout", "laugh", "mock_point")]
    items += [(f"fall progress={k}", lambda x, y, s, k=k: C.goliath(x - 120 * s, y, s, pose="fall", progress=k))
              for k in (0.0, 0.25, 0.5, 0.75, 1.0)]
    items += [("lying bump=True", lambda x, y, s: C.goliath(x - 200 * s, y, s, pose="lying", bump=True)),
              ("lying", lambda x, y, s: C.goliath(x - 200 * s, y, s, pose="lying"))]
    out.append(("goliath", "Goliath — poses, fall progress (pivot at the feet), lying (scale 0.5)", items, 7, 340, 470,
                0.5, {"ground_pad": 20}))
    for side in ("israel", "philistine"):
        items = []
        for v in range(4):
            for p in C.SOLDIER_POSES:
                items.append((f"v{v} {p}", lambda x, y, s, v=v, p=p, sd=side: C.soldier(x, y, s, side=sd, variant=v,
                                                                                     pose=p)))
        out.append((f"soldiers_{side}", f"soldier(side='{side}') — variants 0-3 x poses (scale 0.7)", items, 8, 250,
                    330, 0.7, {"ground_pad": 16}))
    items = [(f"saul {p}", lambda x, y, s, p=p: C.king(x, y, s, pose=p, attire="saul")) for p in
             ("stand", "sit", "talk", "bless", "walk_a", "sit_throne")]
    items += [("saul sit stool=False", lambda x, y, s: C.king(x, y, s, pose="sit", attire="saul", stool=False))]
    items += [(f"eliab {p}", lambda x, y, s, p=p: C.eliab(x, y, s, pose=p)) for p in C.ELIAB_POSES]
    items += [(f"jesse {p}", lambda x, y, s, p=p: C.jesse(x, y, s, pose=p)) for p in C.JESSE_POSES]
    items += [(f"shield_bearer {p}", lambda x, y, s, p=p: C.shield_bearer(x, y, s, pose=p)) for p in
              C.SHIELD_BEARER_POSES]
    out.append(("david_saul", "King Saul (attire='saul'), Eliab, Jesse, shield-bearer (scale 0.8)", items, 8, 260, 400,
                0.8, {"ground_pad": 20}))
    items = [("david", lambda x, y, s: C.david(x, y, s)), ("jonah", _j("stand")),
             ("eliab", lambda x, y, s: C.eliab(x, y, s)), ("saul", lambda x, y, s: C.king(x, y, s, attire="saul")),
             ("goliath", lambda x, y, s: C.goliath(x, y, s)),
             ("shield_bearer", lambda x, y, s: C.shield_bearer(x, y, s, pose="stand")),
             ("david sling_release", lambda x, y, s: C.david(x, y, s, pose="sling_release"))]
    out.append(("david_scale", "Scale check at scale 0.6: boy ~240, adult ~330, giant ~640 px at scale 1", items, 7,
                330, 520, 0.6, {"ground_pad": 20}))
    return out


# ---------------------------------------------------------------- compositions


def _panel_bg(x0, y0, w, h, sky, ground, gy):
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{gy - y0}" fill="{sky}"/>'
            f'<rect x="{x0}" y="{gy}" width="{w}" height="{y0 + h - gy}" fill="{ground}"/>')


def compositions():
    """Figures used together, on scene-like colours: checks contact points, scale and readability."""
    pw, ph, top = 1100, 560, 64
    W, H = 2 * pw, top + 2 * ph
    bg, fg, labels = "", "", []
    P = S.P
    # (1) the captain wakes Jonah asleep in the hold: hand placed with body_points
    x0, y0 = 0, top
    gy = y0 + 470
    bg += _panel_bg(x0, y0, pw, ph, "#6d5440", P["wood_dark"], gy)
    sc = 0.9
    jx = x0 + 640
    shoulder = C.body_points(C.jonah, jx, gy, sc, 1, pose="sleep")["shoulders"][0]
    hand0 = C.body_points(C.captain, 0, gy, sc, 1, pose="wake")["hands"][0]
    cx = shoulder[0] - hand0[0]
    fg += C.ground_shadow(cx, gy, sc, 150) + C.captain(cx, gy, sc, 1, pose="wake")
    fg += C.ground_shadow(jx, gy, sc, 330) + C.jonah(jx, gy, sc, 1, pose="sleep", marks=False)
    labels.append((x0, y0, f"captain(pose='wake') at x = jonah_x {cx - jx:+.0f} (= {(cx - jx) / sc:+.0f}*scale)"))
    # (2) sailors lift Jonah up to throw him overboard (Jonah 1:15), then he tumbles toward the sea
    x0, y0 = pw, top
    gy = y0 + 470
    bg += _panel_bg(x0, y0, pw, ph, P["storm_sky"], P["wood"], gy)
    sc = 0.8
    xs = [x0 + 300, x0 + 420, x0 + 540]
    hands = [C.hand_positions(C.sailor, x, gy, sc, 1, variant=i, pose="lift") for i, x in enumerate(xs)]
    top_y = min(min(h[0][1], h[1][1]) for h in hands)
    jx = xs[1] + 20 * sc                       # the carried body spans -181..+141 around its anchor
    fg += C.jonah(jx, top_y + 6 * sc, sc, 1, pose="carried")   # behind the sailors: their hands hold him
    for i, x in enumerate(xs):
        fg += C.sailor(x, gy, sc, 1, variant=i, pose="lift")
    fg += C.jonah(x0 + 900, y0 + 330, 0.7, 1, pose="fall")
    labels.append((x0, y0, "3 x sailor(pose='lift') under jonah(pose='carried') at the hand line; jonah(pose='fall')"))
    # (3) Jonah preaches to a crowd in Nineveh at scale 0.5: Jonah must stand out
    x0, y0 = 0, top + ph
    gy = y0 + 480
    bg += _panel_bg(x0, y0, pw, ph, P["sky_warm"], P["sand"], gy)
    sc = 0.5
    crowd = [("man", 1, "listen"), ("woman", 0, "stand"), ("elder", 1, "listen"), ("child", 2, "cheer"),
             ("man", 3, "stand"), ("woman", 1, "listen"), ("man", 0, "sad"), ("child", 1, "stand"),
             ("elder", 2, "sad"), ("man", 2, "listen")]
    fg += C.jonah(x0 + 170, gy - 20, sc, 1, pose="preach")
    for i, (k, v, p) in enumerate(crowd):
        fg += C.citizen(x0 + 330 + i * 72, gy - (i % 2) * 26, sc, -1, kind=k, variant=v, pose=p)
    labels.append((x0, y0, "jonah(pose='preach') beside citizens at scale 0.5 (facing=-1)"))
    # (4) wet Jonah on the sea and on the sand
    x0, y0 = pw, top + ph
    gy = y0 + 480
    bg += (f'<rect x="{x0}" y="{y0}" width="{pw // 2}" height="{ph}" fill="{P["underwater"]}"/>'
           f'<rect x="{x0 + pw // 2}" y="{y0}" width="{pw // 2}" height="{gy - y0}" fill="{P["sky_day"]}"/>'
           f'<rect x="{x0 + pw // 2}" y="{gy}" width="{pw // 2}" height="{y0 + ph - gy}" fill="{P["sand"]}"/>')
    fg += C.jonah(x0 + 270, gy - 30, 0.85, 1, pose="float", wet=True)
    fg += C.jonah(x0 + 700, gy, 0.85, 1, pose="stand", wet=True)
    fg += C.jonah(x0 + 920, gy, 0.85, -1, pose="kneel_pray", wet=True)
    labels.append((x0, y0, "wet=True underwater (float) and on the sand (stand, kneel_pray)"))
    svg_bg = S.svg_doc(bg, w=W, h=H).replace(BOIL_TOKEN, "1")
    svg_fg = S.svg_doc(fg, w=W, h=H).replace(BOIL_TOKEN, "1")
    under = watercolor(raster.rasterize(svg_bg, W, H), seed=3)
    fig = watercolor(raster.rasterize(svg_fg, W, H), seed=11)
    sheet, d = _finish(fig, W, H, "Compositions — figures used together", under=under)
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    for x0, y0, text in labels:
        d.rectangle([x0, y0, x0 + pw - 1, y0 + ph - 1], outline=(222, 206, 176), width=2)
        d.rectangle([x0 + 6, y0 + ph - 36, x0 + pw - 6, y0 + ph - 6], fill=(244, 234, 213))
        d.text((x0 + 12, y0 + ph - 34), text, fill=INK_RGB, font=font)
    path = OUT / "characters_compositions.png"
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(path)
    return path


def measure():
    """Render every figure alone at scale 1 and return {function: {pose: [l, t, r, b]}} (union over variants)."""
    jobs = []
    for p in C.JONAH_POSES:
        jobs.append(("jonah", p, lambda x, y, p=p: C.jonah(x, y, pose=p)))
    for v in range(4):
        for p in C.SAILOR_POSES:
            jobs.append(("sailor", p, lambda x, y, p=p, v=v: C.sailor(x, y, variant=v, pose=p)))
    for p in C.CAPTAIN_POSES:
        jobs.append(("captain", p, lambda x, y, p=p: C.captain(x, y, pose=p)))
    for att in C.KING_ATTIRES:
        for p in C.KING_POSES:
            if att == "royal" and p == "sit_ashes":
                continue
            try:
                C.king(0, 0, pose=p, attire=att)
            except ValueError:
                continue
            jobs.append((f"king/{att}", p, lambda x, y, p=p, att=att: C.king(x, y, pose=p, attire=att)))
    for p in C.KING_EXTRA_POSES:
        for att in C.KING_ATTIRES:
            jobs.append((f"king/{att}", p, lambda x, y, p=p, att=att: C.king(x, y, pose=p, attire=att)))
    jobs.append(("king/royal", "sit_throne throne=False", lambda x, y: C.king(x, y, pose="sit_throne", throne=False)))
    jobs.append(("king/sackcloth", "sit_ashes ashes=False", lambda x, y: C.king(x, y, pose="sit_ashes", ashes=False)))
    for p in C.DANIEL_POSES:
        jobs.append(("daniel", p, lambda x, y, p=p: C.daniel(x, y, pose=p)))
    for p in C.DAVID_POSES:
        jobs.append(("david", p, lambda x, y, p=p: C.david(x, y, pose=p)))
        jobs.append(("david armor=True", p, lambda x, y, p=p: C.david(x, y, pose=p, armor=True)))
    for p in C.GOLIATH_POSES:
        jobs.append(("goliath (at scale 0.5)", p, lambda x, y, p=p: C.goliath(x, y, 0.5, pose=p, bump=True)))
    for sd in C.SOLDIER_SIDES:
        for v in range(4):
            for p in C.SOLDIER_POSES:
                jobs.append((f"soldier/{sd}", p, lambda x, y, p=p, v=v, sd=sd: C.soldier(x, y, side=sd, variant=v, pose=p)))
    for p in C.SHIELD_BEARER_POSES:
        jobs.append(("shield_bearer", p, lambda x, y, p=p: C.shield_bearer(x, y, pose=p)))
    for p in C.ELIAB_POSES:
        jobs.append(("eliab", p, lambda x, y, p=p: C.eliab(x, y, pose=p)))
    for p in C.JESSE_POSES:
        jobs.append(("jesse", p, lambda x, y, p=p: C.jesse(x, y, pose=p)))
    for v in range(4):
        for p in C.OFFICIAL_POSES:
            jobs.append(("official", p, lambda x, y, p=p, v=v: C.official(x, y, variant=v, pose=p)))
        for p in C.GUARD_POSES:
            jobs.append(("guard", p, lambda x, y, p=p, v=v: C.guard(x, y, variant=v, pose=p)))
    for k in C.CITIZEN_KINDS:
        for v in range(4):
            for p in C.CITIZEN_POSES:
                for att in C.CITIZEN_ATTIRES:
                    jobs.append((f"citizen/{k}", p, lambda x, y, p=p, k=k, v=v, att=att: C.citizen(
                        x, y, kind=k, variant=v, pose=p, attire=att)))
    res = {}
    for who, pose, fn in jobs:
        svg = S.svg_doc(fn(450, 620), w=900, h=700).replace(BOIL_TOKEN, "1")
        a = np.asarray(raster.rasterize(svg, 900, 700))[..., 3]
        ys, xs = np.nonzero(a > 40)
        bb = [int(xs.min()) - 450, int(ys.min()) - 620, int(xs.max()) - 450, int(ys.max()) - 620]
        if not len(xs):
            continue
        old = res.setdefault(who, {}).get(pose)
        if old:
            bb = [min(old[0], bb[0]), min(old[1], bb[1]), max(old[2], bb[2]), max(old[3], bb[3])]
        res[who][pose] = bb
    return res


def main():
    filt = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--bbox" in sys.argv:
        res = measure()
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "characters_bbox.json").write_text(json.dumps(res, indent=1))
        for who, poses in res.items():
            print(who)
            for p, bb in poses.items():
                print(f"   {p:24s} {tuple(bb)}")
        raster.close()
        return
    for name, title, items, cols, cw, ch, sc, kw in sheets():
        if filt and not any(f in name for f in filt):
            continue
        path, _ = render_sheet(name, title, items, cols, cw, ch, sc, **kw)
        print(path)
    if not filt or any(f in "compositions" for f in filt):
        print(compositions())
    raster.close()


if __name__ == "__main__":
    main()
