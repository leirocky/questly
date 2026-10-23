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
  Noah film (python3 tools/character_sheet.py noah): noah_poses, noah_actions (saw / hammer phases, carry items,
  options), noah_expr (close-ups), noah_family (wife, sons, daughters-in-law), noah_child (raincoat child) and
  noah_group (noah_family portrait and walking line, scale check with the ark and animal pairs).
  Joseph film (python3 tools/character_sheet.py joseph): joseph_poses, joseph_attires (coat progress, torn / None, slave,
  prisoner, ruler), joseph_expr (close-ups), joseph_brothers, joseph_jacob_pharaoh, joseph_egyptians (and traders),
  joseph_siblings (child(sibling=...)) and joseph_group (groups, hugs, the pit, the chariot, the caravan).
  Storm film (python3 tools/character_sheet.py storm): storm_jesus (poses and options), storm_expr (close-ups),
  storm_disciples (the twelve), storm_disciple_poses (poses and action phases), storm_villagers, storm_child (pyjamas)
  and storm_group (Jesus with the twelve, crowds, the crew in the fishing boat: teaching, rowing, the storm, waking him,
  the calm, scale checks).
  Nativity film (python3 tools/character_sheet.py nativity): nativity_mary (poses, pregnant, sweep), nativity_expr
  (close-ups), nativity_joseph, nativity_baby (baby_jesus, toddler_jesus), nativity_angel, nativity_shepherds,
  nativity_magi (wise men, gifts), nativity_townsfolk, nativity_child (child(outfit='jumper')) and nativity_group (scale
  line-up, the journey, the stable, the shepherds with the glory and the choir, the wise men's visit).
Environment (optional): PB_PREVIEW_DIR=<dir> writes the sheets there instead of build/preview; PB_RASTER_CACHE=<dir>
uses a separate raster cache (e.g. a scratch folder you delete afterwards).
"""
import json
import os
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

OUT = Path(os.environ.get("PB_PREVIEW_DIR") or BUILD / "preview")   # PB_PREVIEW_DIR: write sheets elsewhere
if os.environ.get("PB_RASTER_CACHE"):          # optional separate raster cache (e.g. a scratch dir you delete)
    raster._RASTER_DIR = Path(os.environ["PB_RASTER_CACHE"])
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
    out += noah_sheets()
    out += joseph_sheets()
    out += storm_sheets()
    out += nativity_sheets()
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


def noah_sheets():
    """Sheets for the Noah film (Genesis 6-9)."""
    out = []
    PR = C._prp()
    items = [("jonah (compare)", _j("stand"))]
    items += [(p, lambda x, y, s, p=p: C.noah(x, y, s, pose=p)) for p in C.NOAH_POSES]
    out.append(("noah_poses", "Noah — poses (scale 1; Jonah for comparison)", items, 7, 300, 430, 1.0, {"ground_pad": 26}))
    items = [(f"saw phase={ph}", lambda x, y, s, ph=ph: C.noah(x - 60 * s, y, s, pose="saw", phase=ph)) for ph in (0, 0.25, 0.5)]
    items += [(f"hammer phase={ph}", lambda x, y, s, ph=ph: C.noah(x - 40 * s, y, s, pose="hammer", phase=ph)) for ph in (0, 0.4, 0.7, 1.0)]
    items += [("saw sawhorse=False", lambda x, y, s: C.noah(x - 40 * s, y, s, pose="saw", sawhorse=False))]
    items += [(f"carry item={it}", lambda x, y, s, it=it: C.noah(x, y, s, pose="carry", item=it)) for it in C.CARRY_ITEMS]
    items += [("carry_walk_a sack", lambda x, y, s: C.noah(x, y, s, pose="carry_walk_a")),
              ("release_dove dove=True", lambda x, y, s: C.noah(x, y, s, pose="release_dove", dove=True)),
              ("wave phase=0.5 / facing -1", lambda x, y, s: C.noah(x, y, s, -1, pose="wave", phase=0.5)),
              ("marks=False scratch_head", lambda x, y, s: C.noah(x, y, s, pose="scratch_head", marks=False))]
    out.append(("noah_actions", "Noah — saw / hammer phases, carry items, options (scale 0.9)", items, 8, 290, 420, 0.9,
                {"ground_pad": 26}))
    exprs = ("kind", "happy", "puzzled", "determined", "amazed", "worried", "peaceful", "surprised")
    items = [(e, lambda x, y, s, e=e: C.noah(x, y, s, expr=e)) for e in exprs]
    items += [(f"wife {e}", lambda x, y, s, e=e: C.noah_wife(x, y + 10 * s, s, expr=e)) for e in ("kind", "amazed")]
    items += [(f"{n} {e}", lambda x, y, s, n=n, e=e: C.family_member(n, x, y + 14 * s, s, expr=e))
              for n, e in (("shem", "happy"), ("ham", "determined"), ("japheth", "laugh"), ("daughter_in_law0", "kind"),
                           ("daughter_in_law1", "happy"), ("daughter_in_law2", "amazed"))]
    out.append(("noah_expr", "Noah-film expressions (close-ups, scale 1.5)", items, 8, 290, 360, 1.5,
                {"clip_cells": True, "ground_pad": -190}))
    items = []
    for n in C.FAMILY[1:]:
        for p in ("stand", "walk_a", "talk", "carry", "cheer", "pray"):
            items.append((f"{n.replace('daughter_in_law', 'dil')} {p}",
                          lambda x, y, s, n=n, p=p: C.family_member(n, x, y, s, pose=p)))
    for n in ("shem", "ham", "japheth"):
        items.append((f"{n} saw", lambda x, y, s, n=n: C.family_member(n, x - 50 * s, y, s, pose="saw", phase=0.5)))
        items.append((f"{n} hammer", lambda x, y, s, n=n: C.family_member(n, x - 30 * s, y, s, pose="hammer", phase=1.0)))
    out.append(("noah_family", "Noah's family — wife, Shem, Ham, Japheth, daughters-in-law 0-2 (scale 0.75)", items, 12, 190,
                330, 0.75, {"ground_pad": 18}))
    items = [(p, lambda x, y, s, p=p: C.child(x, y, s, pose=p)) for p in C.CHILD_POSES]
    items += [("hood=True stand", lambda x, y, s: C.child(x, y, s, hood=True)),
              ("hood=True peek_window", lambda x, y, s: C.child(x, y, s, pose="peek_window", hood=True)),
              ("coat='#7fb6d6' splash", lambda x, y, s: C.child(x, y, s, pose="splash", coat="#7fb6d6") + PR.puddle(x, y + 4 * s, s, splash=0.4)),
              ("wave phase=.5 facing -1", lambda x, y, s: C.child(x, y, s, -1, pose="wave", phase=0.5)),
              ("adult citizen (compare)", lambda x, y, s: C.citizen(x, y, s, kind="child"))]
    out.append(("noah_child", "child() — raincoat and boots (scale 1.2)", items, 8, 250, 380, 1.2, {"ground_pad": 22}))
    return out


def noah_group():
    """The family portrait and walking line, and the scale check with the ark and the animals."""
    PR = C._prp()
    W, H = 2200, 64 + 520 + 430 + 640
    top = 64
    body = ""
    labels = []
    gy = top + 470
    body += C.noah_family(560, gy, 0.85, pose="stand") + C.noah_family(1660, gy, 0.85, pose="cheer")
    labels.append((20, top + 480, "noah_family(x, y, 0.85) pose='stand'  |  pose='cheer'  (x = Noah's anchor)"))
    gy2 = gy + 400
    body += C.noah_family(900, gy2, 0.6, pose="carry_walk_a") + C.noah_family(1240, gy2, 0.5, -1, pose="walk_b")
    labels.append((20, gy2 + 10, "carry_walk_a line (0.6, facing 1, Noah leads at x=900)  |  walk_b (0.5, facing -1, Noah at x=1240)"))
    gy3 = gy2 + 590
    sc = 0.55
    ax = 900
    body += PR.ark(ax, gy3, sc, door=1)
    rx = PR.ark_points(ax, gy3, sc)["ramp_bottom"][0]
    body += PR.animal_pair("giraffe", rx + 330, gy3, sc, -1, pose="walk_a")
    body += PR.animal_pair("elephant", rx + 120, gy3, sc, -1, pose="walk_b")
    body += PR.animal_pair("zebra", rx - 70, PR.ark_ramp_y(rx - 70, ax, gy3, sc), sc, -1, pose="walk_a")
    body += PR.animal_pair("rabbit", rx + 560, gy3, sc, -1, pose="hop", phase=0.25)
    body += C.noah(ax - 760 * sc, gy3, sc, 1, pose="point_up") + C.child(ax - 1050 * sc, gy3, sc, 1)
    body += PR.animal_pair("sheep", rx + 700, gy3, sc, -1, pose="walk_a")
    labels.append((20, gy3 + 10, "scale check at 0.55: ark(door=1), Noah, child, giraffe / elephant / zebra on the ramp / rabbit / sheep"))
    svg = S.svg_doc(f'<rect x="0" y="{gy3 - 640}" width="{W}" height="660" fill="#cfe3e4"/>' + body, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = watercolor(raster.rasterize(svg, W, H), seed=11)
    sheet, d = _finish(fig, W, H, "Noah film — family group, walking line, scale with the ark and animals")
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    for x0, y0, text in labels:
        d.text((x0, y0), text, fill=INK_RGB, font=font)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "characters_noah_group.png"
    sheet.save(path)
    return path


def joseph_sheets():
    """Sheets for the Joseph film (Genesis 37-50)."""
    out = []
    items = [("jonah (compare)", _j("stand"))]
    items += [(p, lambda x, y, s, p=p: C.joseph(x, y, s, pose=p)) for p in C.JOSEPH_POSES]
    out.append(("joseph_poses", "Joseph — teen shepherd in the coat of many colours: poses (scale 0.9)", items, 8, 270,
                420, 0.9, {"ground_pad": 24}))
    items = [(f"coat progress={pr:.2f}", lambda x, y, s, pr=pr: C.joseph(x, y, s, progress=pr, expr="proud"))
             for pr in (0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 1)]
    items += [("coat='torn' sad", lambda x, y, s: C.joseph(x, y, s, coat="torn", pose="sad")),
              ("coat=None walk_a", lambda x, y, s: C.joseph(x, y, s, coat=None, pose="walk_a")),
              ("torn call_up", lambda x, y, s: C.joseph(x, y, s, coat="torn", pose="call_up")),
              ("torn hold_rope", lambda x, y, s: C.joseph(x, y, s, coat="torn", pose="hold_rope"))]
    for att in ("slave", "prisoner", "ruler"):
        for p in ("stand", "walk_a", "talk", "point_up", "kneel_pray", "carry", "sad", "cry", "hug", "give", "comfort",
                  "ride", "ride_wave", "open_arms", "bow", "sit"):
            if att != "ruler" and p in ("ride", "ride_wave", "comfort"):
                continue
            if att == "ruler" and p in ("carry", "kneel_pray", "sit"):
                continue
            items.append((f"{att} {p}", lambda x, y, s, att=att, p=p: C.joseph(x, y, s, pose=p, attire=att)))
    items += [("ruler chain=False ring=False", lambda x, y, s: C.joseph(x, y, s, attire="ruler", chain=False, ring=False))]
    out.append(("joseph_attires", "Joseph — coat progress, torn / None, slave, prisoner, ruler (scale 0.8)", items, 10,
                220, 360, 0.8, {"ground_pad": 22}))
    exprs = ("happy", "proud", "worried", "sad", "crying", "tearful", "kind", "amazed", "determined", "peaceful")
    items = [(e, lambda x, y, s, e=e: C.joseph(x, y, s, expr=e)) for e in exprs]
    items += [(f"ruler {e}", lambda x, y, s, e=e: C.joseph(x, y + 10 * s, s, attire="ruler", expr=e))
              for e in ("kind", "crying", "tearful")]
    items += [(f"brother{v} {e}", lambda x, y, s, v=v, e=e: C.brothers(x, y + 26 * s, s, variant=v, expr=e))
              for v, e in ((1, "jealous"), (3, "angry"), (4, "sly"), (6, "scared"), (0, "ashamed"), (8, "crying"),
                           (2, "happy"))]
    items += [("jacob crying", lambda x, y, s: C.jacob(x, y + 8 * s, s, expr="crying")),
              ("jacob tearful", lambda x, y, s: C.jacob(x, y + 8 * s, s, expr="tearful")),
              ("pharaoh amazed", lambda x, y, s: C.pharaoh(x, y + 30 * s, s, expr="amazed")),
              ("pharaoh worried", lambda x, y, s: C.pharaoh(x, y + 30 * s, s, expr="worried"))]
    out.append(("joseph_expr", "Joseph-film expressions (close-ups, scale 1.4)", items, 8, 290, 370, 1.4,
                {"clip_cells": True, "ground_pad": -175}))
    items = [(f"{v} {C.BROTHER_NAMES[v]}", lambda x, y, s, v=v: C.brothers(x, y, s, variant=v)) for v in range(10)]
    items += [("benjamin", lambda x, y, s: C.brothers(x, y, s, variant="benjamin")),
              ("benjamin walk_a", lambda x, y, s: C.brothers(x, y, s, variant="benjamin", pose="walk_a"))]
    for i, p in enumerate(C.BROTHER_POSES):
        if p in ("stand",):
            continue
        items.append((f"v{i % 10} {p}", lambda x, y, s, i=i, p=p: C.brothers(x, y, s, variant=i % 10, pose=p)))
    out.append(("joseph_brothers", "The brothers — variants 0-9, Benjamin, poses (scale 0.75)", items, 10, 220, 340,
                0.75, {"ground_pad": 20}))
    items = [(f"jacob {p}", lambda x, y, s, p=p: C.jacob(x, y, s, pose=p)) for p in C.JACOB_POSES]
    items += [("jacob give progress=.5", lambda x, y, s: C.jacob(x, y, s, pose="give", progress=0.5)),
              ("jacob staff=False", lambda x, y, s: C.jacob(x, y, s, staff=False))]
    items += [(f"pharaoh {p}", lambda x, y, s, p=p: C.pharaoh(x, y, s, pose=p)) for p in C.PHARAOH_POSES]
    out.append(("joseph_jacob_pharaoh", "Jacob and Pharaoh (scale 0.8)", items, 8, 270, 380, 0.8, {"ground_pad": 22}))
    items = []
    for k in C.EGYPTIAN_KINDS:
        for p in ("stand", "walk_a", "bow", "shrug", "carry", "lead", "give"):
            if p == "give" and k not in ("potiphar", "cupbearer"):
                continue
            items.append((f"{k} {p}", lambda x, y, s, k=k, p=p: C.egyptian(x, y, s, kind=k, variant=1 if k == "wise" else 0,
                                                                            pose=p)))
    items += [(f"servant v{v}", lambda x, y, s, v=v: C.egyptian(x, y, s, kind="servant", variant=v)) for v in (1, 2, 3)]
    items += [(f"wise v{v}", lambda x, y, s, v=v: C.egyptian(x, y, s, kind="wise", variant=v)) for v in (0, 2)]
    items += [(f"woman v{v}", lambda x, y, s, v=v: C.egyptian(x, y, s, kind="woman", variant=v)) for v in (1, 2)]
    items += [("cupbearer prisoner", lambda x, y, s: C.egyptian(x, y, s, kind="cupbearer", prisoner=True, pose="shrug")),
              ("baker prisoner", lambda x, y, s: C.egyptian(x, y, s, kind="baker", prisoner=True, expr="worried")),
              ("cupbearer prisoner sit", lambda x, y, s: C.egyptian(x, y, s, kind="cupbearer", prisoner=True, pose="sit")),
              ("baker prisoner sad", lambda x, y, s: C.egyptian(x, y, s, kind="baker", prisoner=True, pose="sad"))]
    items += [(f"trader v{v} {p}", lambda x, y, s, v=v, p=p: C.trader(x, y, s, variant=v, pose=p))
              for v, p in ((0, "stand"), (1, "walk_a"), (2, "lead"), (0, "give"), (1, "count"), (2, "talk"))]
    out.append(("joseph_egyptians", "Egyptians (servant, guard, wise, Potiphar, woman, cupbearer, baker) and traders "
                "(scale 0.75)", items, 10, 220, 350, 0.75, {"ground_pad": 20}))
    items = [(f"{sb or 'raincoat'} {p}", lambda x, y, s, sb=sb, p=p: C.child(x, y, s, pose=p, sibling=sb))
             for sb in ("big", "little", None) for p in ("stand", "walk_a", "tug", "sulk", "sorry", "hug", "share")]
    items += [("big share toy=horse", lambda x, y, s: C.child(x, y, s, pose="share", sibling="big", toy="horse")),
              ("little tug toy=ball", lambda x, y, s: C.child(x, y, s, pose="tug", sibling="little", toy="ball")),
              ("little stand toy=horse", lambda x, y, s: C.child(x, y, s, sibling="little", toy="horse")),
              ("big cross", lambda x, y, s: C.child(x, y, s, sibling="big", expr="cross")),
              ("little crying", lambda x, y, s: C.child(x, y, s, sibling="little", expr="crying"))]
    out.append(("joseph_siblings", "Modern siblings: child(sibling='big' / 'little') and the new poses (scale 1.0)",
                items, 8, 250, 330, 1.0, {"ground_pad": 22}))
    return out


def joseph_group():
    """Compositions: the family, the brothers group, hugs, the pit, the chariot, the caravan (scale checks)."""
    PR = C._prp()
    W, H = 2300, 64 + 4 * 560
    top = 64
    body = ""
    labels = []
    gy = top + 470
    body += C.brothers_group(520, gy, 0.8, pose="cross_arms", expr="jealous")
    body += C.jacob(1180, gy, 0.8, pose="give", progress=1.0) + C.joseph(1400, gy, 0.8, -1, expr="amazed", progress=0.0, coat="colours")
    body += C.brothers(1620, gy, 0.8, variant="benjamin") + C.brothers_group(2050, gy, 0.55, pose="bow")
    labels.append((20, gy + 12, "brothers_group(cross_arms, jealous) | jacob give + joseph (coat progress 0) + Benjamin | brothers_group(bow) at 0.55"))
    gy2 = gy + 560
    body += C.hug_pair(250, gy2, 0.8)
    body += C.hug_pair(560, gy2, 0.8, a=(C.joseph, dict(attire="ruler", expr="tearful")), b=(C.brothers, dict(variant=3, expr="crying")))
    body += C.brothers(925, gy2, 0.8, -1, variant=0, pose="sad") + C.joseph(830, gy2, 0.8, attire="ruler", pose="comfort")
    body += C.child(1150, gy2, 1.0, pose="hug", sibling="big") + C.child(1225, gy2, 1.0, -1, pose="hug", sibling="little")
    body += C.child(1430, gy2, 1.0, pose="tug", sibling="big", toy="horse") + C.child(1600, gy2, 1.0, -1, pose="tug", sibling="little")
    body += C.child(1800, gy2, 1.0, pose="share", sibling="big", toy="ball") + C.child(1900, gy2, 1.0, -1, pose="stand", sibling="little")
    body += C.child(2120, gy2, 1.0, pose="sulk", sibling="big") + C.child(2230, gy2, 1.0, -1, pose="sorry", sibling="little")
    labels.append((20, gy2 + 12, "hug_pair() default (Joseph + Jacob) | with Judah | comfort | children hug / tug / share / sulk + sorry"))
    gy3 = gy2 + 560
    pk, rim = 0.6, gy3 - 330
    body += PR.pit(330, rim, pk, view="cutaway", rope=0.0) + C.joseph(330, rim + PR.PIT_DEPTH * pk, pk, coat="torn", pose="call_up")
    body += C.brothers(330 + 230 * pk, rim, pk, -1, variant=3, pose="point")
    body += PR.pit(900, gy3 - 60, 0.8, part="back") + PR.in_pit(C.joseph(900, gy3 - 60 + 300 * 0.8, 0.8, coat="torn", pose="call_up"), 900, gy3 - 60, 0.8) + PR.pit(900, gy3 - 60, 0.8, part="front")
    body += C.brothers(1060, gy3 - 60, 0.8, -1, variant=0, pose="pull")
    cx = 1600
    body += PR.chariot(cx, gy3, 0.8, part="back", wheel=0.3, phase=0.2)
    sx, sy = PR.local_to_stage(cx, gy3, 0.8, 1, *PR.CHARIOT_STAND)
    body += C.joseph(sx, sy, 0.8, attire="ruler", pose="ride_wave")
    body += PR.chariot(cx, gy3, 0.8, part="front", wheel=0.3)
    body += C.egyptian(2150, gy3, 0.8, -1, kind="servant", pose="bow")
    labels.append((20, gy3 + 12, "pit cutaway + Joseph call_up at PIT_FLOOR | pit outside (back, in_pit, front) | chariot back + Joseph ride_wave + front"))
    gy4 = gy3 + 560
    body += PR.camel(500, gy4, 0.7, pose="walk", phase=0.0) + C.trader(500 + PR.CAMEL_LEAD[0] * 0.7 + 30, gy4, 0.7, pose="lead")
    body += PR.camel(980, gy4, 0.7, pose="walk", phase=0.5, bridle=False)
    body += C.joseph(1180, gy4, 0.7, attire="slave", pose="walk_a", expr="sad") + C.brothers(1330, gy4, 0.7, -1, variant=3, pose="talk")
    body += C.trader(1450, gy4, 0.7, -1, pose="give") + PR.donkey(1750, gy4, 0.7, pose="walk", phase=0.25)
    body += C.pharaoh(2000, gy4, 0.7, pose="give_ring") + C.joseph(2130, gy4, 0.7, -1, attire="ruler", pose="bow", ring=False, chain=False)
    labels.append((20, gy4 + 12, "caravan: camel walk + trader lead (rope end CAMEL_LEAD) | slave Joseph, Judah, trader give | donkey | Pharaoh gives the ring"))
    svg = S.svg_doc(f'<rect x="0" y="{gy3 - 520}" width="{W}" height="540" fill="#e8d9b0"/>' + body, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = watercolor(raster.rasterize(svg, W, H), seed=11)
    sheet, d = _finish(fig, W, H, "Joseph film — groups, hugs, the pit, the chariot, the caravan (scale checks)")
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    for x0, y0, text in labels:
        d.text((x0, y0), text, fill=INK_RGB, font=font)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "characters_joseph_group.png"
    sheet.save(path)
    return path


def storm_sheets():
    """Sheets for the Storm film (Mark 4:35-41)."""
    out = []
    items = [("jonah (compare)", _j("stand"))]
    items += [(p, lambda x, y, s, p=p: C.jesus(x, y, s, pose=p)) for p in C.JESUS_POSES]
    items += [("glow=1", lambda x, y, s: C.jesus(x, y, s, glow=1.0)),
              ("sleep glow=.8", lambda x, y, s: C.jesus(x + 40 * s, y, s, pose="sleep", glow=0.8)),
              ("sleep marks=False", lambda x, y, s: C.jesus(x + 40 * s, y, s, pose="sleep", marks=False)),
              ("stand_command wind=1", lambda x, y, s: C.jesus(x, y, s, pose="stand_command", wind=1.0)),
              ("walk_a wind=.6", lambda x, y, s: C.jesus(x, y, s, pose="walk_a", wind=0.6)),
              ("wave phase=.5", lambda x, y, s: C.jesus(x, y, s, pose="wave", phase=0.5)),
              ("facing=-1 teach", lambda x, y, s: C.jesus(x, y, s, -1, pose="teach")),
              ("mantle=False", lambda x, y, s: C.jesus(x, y, s, mantle=False))]
    out.append(("storm_jesus", "Jesus — poses and options (scale 0.85; red cross = anchor)", items, 8, 270, 400, 0.85,
                {"ground_pad": 24}))
    items = [(e, lambda x, y, s, e=e: C.jesus(x, y, s, expr=e)) for e in C.JESUS_EXPRESSIONS]
    items += [(f"{n} {e}", lambda x, y, s, n=n, e=e: C.disciples(x, y + (C.body_points(C.jesus, 0, 0)["head"][1] -
                                                                         C.body_points(C.disciples, 0, 0, variant=n)["head"][1]) * s,
                                                                   s, variant=n, expr=e))
              for n, e in (("peter", "happy"), ("peter", "panicked"), ("andrew", "scared"), ("james", "amazed"),
                           ("john", "awed"), ("john", "tired"), ("peter", "ashamed"), ("james", "shout"))]
    out.append(("storm_expr", "Storm-film expressions (close-ups, scale 1.4): Jesus; Peter, Andrew, James, John",
                items, 9, 260, 360, 1.4, {"clip_cells": True, "ground_pad": -190}))
    items = [(f"{v} {C.DISCIPLE_NAMES[v]}", lambda x, y, s, v=v: C.disciples(x, y, s, variant=v)) for v in range(12)]
    items += [(f"'{n}' wet=True", lambda x, y, s, n=n: C.disciples(x, y, s, variant=n, wet=True, expr="tired"))
              for n in ("peter", "andrew", "james", "john")]
    out.append(("storm_disciples", "The twelve disciples (scale 0.8): 0-3 = 'peter', 'andrew', 'james', 'john' (the four "
                "fishermen); wet=True for after the storm", items, 8, 250, 360, 0.8, {"ground_pad": 22}))
    items = []
    for i, p in enumerate(C.DISCIPLE_POSES):
        items.append((f"v{i % 12} {p}", lambda x, y, s, i=i, p=p: C.disciples(x, y, s, variant=i % 12, pose=p, phase=0.3)))
    items += [(f"row phase={ph}", lambda x, y, s, ph=ph: C.disciples(x, y, s, variant=1, pose="row", phase=ph))
              for ph in (0, 0.25, 0.5, 0.75)]
    items += [(f"bail phase={ph}", lambda x, y, s, ph=ph: C.disciples(x, y, s, variant=2, pose="bail", phase=ph))
              for ph in (0, 0.35, 0.65, 0.8)]
    items += [("bail item='bowl'", lambda x, y, s: C.disciples(x, y, s, variant=5, pose="bail", phase=0.35, item="bowl"))]
    items += [(f"cast_net phase={ph}", lambda x, y, s, ph=ph: C.disciples(x, y, s, variant="peter", pose="cast_net", phase=ph))
              for ph in (0, 0.5, 0.9, 1.0)]
    items += [(f"haul_net phase={ph}", lambda x, y, s, ph=ph: C.disciples(x, y, s, variant="andrew", pose="haul_net", phase=ph))
              for ph in (0, 0.5)]
    items += [("scared shake=.25", lambda x, y, s: C.disciples(x, y, s, variant=9, pose="scared", shake=0.25)),
              ("cling wind=1", lambda x, y, s: C.disciples(x, y, s, variant=0, pose="cling", wind=1.0, shake=0.5)),
              ("wake_shake phase=.5", lambda x, y, s: C.disciples(x, y, s, variant=2, pose="wake_shake", phase=0.5))]
    out.append(("storm_disciple_poses", "Disciples — poses and action phases (scale 0.72)", items, 9, 240, 360, 0.72,
                {"ground_pad": 24}))
    items = []
    for k in C.VILLAGER_KINDS:
        for v in range(6):
            items.append((f"{k} {v}", lambda x, y, s, k=k, v=v: C.villager(x, y, s, kind=k, variant=v)))
    for p in C.VILLAGER_POSES:
        k = {"shoulders": "man", "carry": "woman", "carry_walk_a": "woman", "carry_walk_b": "man", "wave": "child",
             "sit_listen": "child", "kneel": "elder", "nod": "elder", "listen": "woman"}.get(p, "man")
        items.append((f"{k} {p}", lambda x, y, s, p=p, k=k: C.villager(x, y, s, kind=k, variant=2, pose=p)))
    out.append(("storm_villagers", "Galilean villagers — kinds x variants 0-5, poses (scale 0.7)", items, 12, 180, 340,
                0.7, {"ground_pad": 20}))
    items = [(f"pyjamas {p}", lambda x, y, s, p=p: C.child(x, y, s, pose=p, outfit="pyjamas"))
             for p in ("stand", "walk_a") + C.STORM_CHILD_POSES + ("peek_window", "wave")]
    items += [("pyjamas hug_pillow scared", lambda x, y, s: C.child(x, y, s, pose="hug_pillow", outfit="pyjamas", expr="scared")),
              ("pyjamas smile_up", lambda x, y, s: C.child(x, y, s, pose="smile_up", outfit="pyjamas")),
              ("pyjamas pillow=False", lambda x, y, s: C.child(x, y, s, pose="sit_hug", outfit="pyjamas", pillow=False)),
              ("raincoat pray", lambda x, y, s: C.child(x, y, s, pose="pray")),
              ("little hug_pillow", lambda x, y, s: C.child(x, y, s, pose="hug_pillow", sibling="little"))]
    out.append(("storm_child", "child(outfit='pyjamas') — the girl at home at night; the new poses (scale 1.1)", items, 8,
                240, 330, 1.1, {"ground_pad": 22}))
    return out


def storm_group():
    """Compositions: Jesus with the twelve, crowds, the crew in the fishing boat (teaching, rowing, the storm, waking him,
    the calm), the child's room."""
    PR = C._prp()
    W, H = 2300, 64 + 4 * 600
    top = 64
    body = ""
    labels = []
    gy = top + 500
    body += f'<rect x="0" y="{top}" width="{W}" height="600" fill="#e8d6ae"/>'
    body += C.disciples_group(800, gy, 0.62, pose="walk_a", n=12, gap=62)
    body += C.jesus(860, gy, 0.62, pose="walk_a")
    body += C.villager_crowd(1500, gy, 0.6, pose="sit_listen", n=12, width=700, rows=3)
    body += C.villager_crowd(2050, gy, 0.55, -1, pose="walk_a", n=6, width=380, rows=2, seed=3)
    labels.append((20, gy + 14, "jesus walk_a + disciples_group(walk_a, gap 62) | villager_crowd(sit_listen) | villager_crowd(walk_a): going home"))
    gy2 = gy + 600
    k = 0.42
    body += f'<rect x="0" y="{gy2 - 520}" width="{W}" height="600" fill="#f0c9a0"/>'
    body += PR.calm_lake(0, W, gy2 - 30, bottom=gy2 + 80, time="dawn", scale=0.6)

    def crew(bx, by, k, mode, phase=0.0):
        pts = PR.boat_points(bx, by, k)
        sail = {"teach": "furled", "row": "full", "storm": "flapping", "calm": "furled"}[mode]
        out = PR.fishing_boat(bx, by, k, part="back", sail=sail, phase=phase, oars="out" if mode == "row" else "in",
                              row=phase)
        far_pose = {"teach": "sit", "row": "stand", "storm": "scared", "calm": "wonder"}[mode]
        for i, (px, py) in enumerate(pts["far_stand"]):
            out += C.disciples(px, py, k, 1 if i % 2 else -1, variant=4 + i,
                               pose="whisper" if (mode == "calm" and i % 2) else far_pose, wet=mode in ("storm", "calm"),
                               phase=(phase + 0.2 * i) % 1, shake=0.25 * (i % 4))
        if mode == "teach":
            out += C.jesus(*pts["stern_seat"], k, -1, pose="teach")
        elif mode in ("row",):
            out += C.jesus(*pts["sleep"], k, 1, pose="sleep", marks=False)
        elif mode == "storm":
            out += C.jesus(*pts["sleep"], k, 1, pose="sleep", glow=0.8)
        else:
            out += C.jesus(pts["stand"][0][0] - 40 * k, pts["stand"][0][1], k, 1, pose="turn_kind", glow=0.3)
        if mode == "row":
            for (sx, sy), v in zip(pts["seats"], (1, 2)):
                out += C.disciples(sx, sy, k, -1, variant=v, pose="row", phase=phase)
        near = {"teach": [("stand", 0), ("sit", 3), ("stand", 10), ("point", 11), ("stand", 9), ("wave", 2)],
                "row": [None, ("stand", 3), None, ("point", 0), ("stand", 9), ("pull_rope", 11)],
                "storm": [("bail", 1), ("bail", 3), ("pull_rope", 10), ("cling", 0), ("bail", 9), ("shout", 2)],
                "calm": [None, ("wonder", 3), ("whisper", 10), ("wonder", 0), ("kneel", 9), ("whisper", 2)]}[mode]
        for i, ((px, py), spec) in enumerate(zip(pts["stand"], near)):
            if spec is None:
                continue
            pz, v = spec
            f = -1 if i < 3 else 1
            if pz == "cling":
                px, py, f = pts["cling"][0], pts["cling"][1], 1
            out += C.disciples(px, py, k, f, variant=v, pose=pz, phase=(phase + 0.3 * i) % 1, item="bowl" if i == 4 else "bucket",
                               wet=mode in ("storm", "calm"), wind=1.0 if mode == "storm" else 0.0)
        out += PR.fishing_boat(bx, by, k, part="front", oars="out" if mode == "row" else "in", row=phase,
                               water=0.55 if mode == "storm" else 0.0, wet=mode in ("storm", "calm"), lantern=mode != "teach")
        return out
    body += crew(380, gy2, k, "teach") + crew(1150, gy2, k, "row", 0.25) + crew(1920, gy2, k, "calm")
    labels.append((20, gy2 + 30, "in the boat (scale 0.42): Jesus teach on STERN_SEAT, crew | rowing (seats, oars out, phase .25), Jesus asleep | the calm: turn_kind, wonder, whisper, kneel"))
    gy3 = gy2 + 600
    body += PR.storm_sky(0, gy3 - 540, 1150, gy3 + 60, phase=0.3, rain=0.4, lightning=0.3, scale=0.6)
    body += PR.storm_lake(0, 1150, gy3 - 120, phase=0.3, part="back", bottom=gy3 + 60, scale=0.55)
    sb = (560, gy3 - 120 + PR.STORM_BOAT_DY * 0.55)
    body += PR.boat_rock(crew(sb[0], sb[1], 0.4, "storm", 0.4), sb[0], sb[1], -5, 0, 0.4)
    body += PR.storm_lake(0, 1150, gy3 - 120, phase=0.3, part="front", bottom=gy3 + 60, scale=0.55)
    # waking Jesus: two disciples at the stern (BOAT_WAKE) and Jesus waking / commanding
    k2 = 0.62
    bx, by = 1500, gy3 - 10
    body += f'<rect x="1150" y="{gy3 - 540}" width="1150" height="600" fill="#5a6c82"/>'
    pts = PR.boat_points(bx, by, k2)
    body += PR.fishing_boat(bx, by, k2, part="back", sail="none", oars="none")
    body += C.jesus(*pts["sleep"], k2, 1, pose="sleep", marks=False)
    body += C.disciples(*pts["wake"], k2, -1, variant="peter", pose="wake_shake", phase=0.5, wet=True)
    body += C.disciples(pts["wake"][0] + 120 * k2, pts["wake"][1], k2, -1, variant="john", pose="shout", wet=True)
    body += PR.fishing_boat(bx, by, k2, part="front", oars="none", wet=True, water=0.4)
    body += C.jesus(2190, gy3 - 20, 0.62, -1, pose="stand_command", wind=1.0, glow=0.6)
    labels.append((20, gy3 + 30, "the storm: storm_sky, storm_lake back / boat_rock(crew, -5 deg) / front | wake: disciples at BOAT_WAKE (wake_shake) | stand_command wind=1 glow .6"))
    gy4 = gy3 + 600
    body += f'<rect x="0" y="{gy4 - 540}" width="{W}" height="600" fill="#e9dcc4"/>'
    body += PR.window_wind(330, gy4 - 160, 0.62, wind=1.0, phase=0.2, rattle=0.8)
    body += C.child(250, gy4 - 10, 1.0, pose="hug_pillow", outfit="pyjamas", expr="scared")
    body += PR.bed(760, gy4, 0.85) + C.child(730, gy4 + PR.BED_TOP * 0.85, 0.85, pose="sit_pray", outfit="pyjamas")
    body += C.villager(1150, gy4, 0.8, kind="man", variant=2, pose="shoulders")
    body += C.villager(1300, gy4, 0.8, -1, kind="woman", variant=4, pose="wave")
    body += C.disciples(1500, gy4, 0.8, variant="peter", pose="haul_net", phase=0.2)
    body += C.disciples(1840, gy4, 0.8, variant="john", pose="cast_net", phase=1.0)
    body += C.jesus(2200, gy4, 0.8, -1, pose="point")
    labels.append((20, gy4 + 14, "window_wind + child hug_pillow | bed + child sit_pray at BED_TOP | villager shoulders, wave | Peter haul_net, John cast_net | Jesus point"))
    svg = S.svg_doc(body, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = watercolor(raster.rasterize(svg, W, H), seed=11)
    sheet, d = _finish(fig, W, H, "Storm film — Jesus and the twelve, crowds, the crew in the fishing boat, the child's room")
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    for x0, y0, text in labels:
        d.text((x0, y0), text, fill=INK_RGB, font=font)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "characters_storm_group.png"
    sheet.save(path)
    return path


def nativity_sheets():
    """Sheets for the Nativity film (Luke 1-2, Matthew 2)."""
    out = []
    items = [(p, lambda x, y, s, p=p: C.mary(x, y, s, pose=p)) for p in C.MARY_POSES if p not in ("walk",)]
    items += [(f"pregnant {p}", lambda x, y, s, p=p: C.mary(x, y, s, pose=p, pregnant=True))
              for p in ("stand", "walk_a", "walk_b", "sit", "ride", "startled")]
    items += [(f"sweep phase={ph}", lambda x, y, s, ph=ph: C.mary(x, y, s, pose="sweep", phase=ph)) for ph in (0.25, 0.75)]
    items += [("glow=.8", lambda x, y, s: C.mary(x, y, s, glow=0.8)), ("facing=-1 hold_baby", lambda x, y, s: C.mary(x, y, s, -1, pose="hold_baby"))]
    out.append(("nativity_mary", "Mary — poses, pregnant=True, sweep phases (scale 0.8; ride / sit anchors: see doc)", items, 9,
                250, 360, 0.8, {"ground_pad": 24}))
    items = [(e, lambda x, y, s, e=e: C.mary(x, y, s, expr=e)) for e in C.MARY_EXPRESSIONS]
    items += [(f"joseph {e}", lambda x, y, s, e=e: C.joseph_carpenter(x, y - 22 * s, s, expr=e)) for e in C.JOSEPH_CARPENTER_EXPRESSIONS]
    out.append(("nativity_expr", "Nativity expressions (close-ups, scale 1.4): Mary; Joseph", items, 10, 240, 330, 1.4,
                {"clip_cells": True, "ground_pad": -190}))
    items = [(p, lambda x, y, s, p=p: C.joseph_carpenter(x, y, s, pose=p)) for p in C.JOSEPH_CARPENTER_POSES if p not in ("walk", "lead")]
    items += [("staff=False", lambda x, y, s: C.joseph_carpenter(x, y, s, staff=False)),
              ("knock phase=.5", lambda x, y, s: C.joseph_carpenter(x, y, s, pose="knock", phase=0.5)),
              ("hold_lamp lamp=.4", lambda x, y, s: C.joseph_carpenter(x, y, s, pose="hold_lamp", lamp=0.4))]
    out.append(("nativity_joseph", "Joseph the carpenter — poses (scale 0.8)", items, 10, 230, 380, 0.8, {"ground_pad": 24}))
    items = [(f"baby {st}", lambda x, y, s, st=st: C.baby_jesus(x, y, s, state=st)) for st in C.BABY_STATES]
    items += [("baby glow=.8", lambda x, y, s: C.baby_jesus(x, y, s, glow=0.8)), ("baby hand=True facing=-1", lambda x, y, s: C.baby_jesus(x, y, s, -1, hand=True))]
    items += [(f"toddler {p}", lambda x, y, s, p=p: C.toddler_jesus(x, y, s, pose=p)) for p in C.TODDLER_POSES]
    items += [("toddler laugh", lambda x, y, s: C.toddler_jesus(x, y, s, pose="stand", expr="laugh"))]
    out.append(("nativity_baby", "baby_jesus states and toddler_jesus poses (scale 1.6)", items, 7, 300, 330, 1.6, {"ground_pad": 30}))
    items = [(p, lambda x, y, s, p=p: C.angel(x, y, s, pose=p)) for p in C.ANGEL_POSES]
    items += [(f"wings={w}", lambda x, y, s, w=w: C.angel(x, y, s, wings=w)) for w in (0.0, 0.5, 1.0)]
    items += [("float phase=.25", lambda x, y, s: C.angel(x, y, s, pose="float", phase=0.25)),
              ("glow=0", lambda x, y, s: C.angel(x, y, s, glow=0.0)), ("glow=1 announce -1", lambda x, y, s: C.angel(x, y, s, -1, pose="announce", glow=1.0))]
    items += [(f"variant {v} sing", lambda x, y, s, v=v: C.angel(x, y, s, pose="sing", variant=v)) for v in range(1, 6)]
    out.append(("nativity_angel", "angel — poses, wings, glow, variants (scale 0.6; float hovers ANGEL_FLOAT_LIFT above the anchor)",
                items, 8, 300, 420, 0.6, {"ground_pad": 30}))
    items = [(f"{v} stand", lambda x, y, s, v=v: C.shepherds(x, y, s, variant=v)) for v in range(6)]
    for i, p in enumerate(C.SHEPHERD_POSES):
        if p in ("stand", "walk", "run"):
            continue
        items.append((f"{i % 6} {p}", lambda x, y, s, i=i, p=p: C.shepherds(x, y, s, variant=i % 6, pose=p)))
    items += [("2 hold_lamb (boy)", lambda x, y, s: C.shepherds(x, y, s, variant=2, pose="hold_lamb")),
              ("1 sit sleepy", lambda x, y, s: C.shepherds(x, y, s, variant=1, pose="sit", expr="sleepy"))]
    out.append(("nativity_shepherds", "shepherds — variants 0-5 (2 = the boy, 1 = the old shepherd) and poses (scale 0.7)",
                items, 8, 250, 330, 0.7, {"ground_pad": 22}))
    items = []
    for v in range(3):
        for p in C.WISE_MEN_POSES:
            if p in ("walk",):
                continue
            items.append((f"{v} {p}", lambda x, y, s, v=v, p=p: C.wise_men(x, y, s, variant=v, pose=p)))
    items += [(f"{v} kneel_offer open=1 glow=1", lambda x, y, s, v=v: C.wise_men(x, y, s, variant=v, pose="kneel_offer", gift_open=1.0, gift_glow=1.0)) for v in range(3)]
    out.append(("nativity_magi", "wise_men — variants 0-2 x poses; gifts open and glow (scale 0.62)", items, 12, 200, 360, 0.62,
                {"ground_pad": 22}))
    items = []
    for k in C.TOWNSFOLK_KINDS:
        for v in range(3):
            items.append((f"{k} {v}", lambda x, y, s, k=k, v=v: C.townsfolk(x, y, s, kind=k, variant=v)))
    for p, k, it in (("carry_walk_a", "traveller", "bundle"), ("carry_walk_b", "traveller_woman", "bundle"), ("carry", "woman", "jar"),
                     ("carry_walk_a", "man", "pots"), ("carry", "traveller", "hen"), ("squeeze", "man", "bundle"), ("squeeze", "woman", "pots"),
                     ("look_around", "traveller", None), ("shake_head", "innkeeper", None), ("hold_lamp", "innkeeper", None),
                     ("point", "innkeeper", None), ("read", "herald", None), ("announce", "herald", None), ("talk", "woman", None),
                     ("wave", "child", None), ("listen", "elder", None), ("sit", "man", None), ("cheer", "child", None)):
        items.append((f"{k} {p} {it or ''}", lambda x, y, s, p=p, k=k, it=it: C.townsfolk(x, y, s, kind=k, variant=1, pose=p, item=it)))
    out.append(("nativity_townsfolk", "townsfolk — kinds x variants, travellers, the innkeeper, the herald, comic carriers (scale 0.6)",
                items, 12, 200, 300, 0.6, {"ground_pad": 20}))
    items = [(f"jumper {p}", lambda x, y, s, p=p: C.child(x, y, s, pose=p, outfit="jumper")) for p in ("stand", "walk_a") + C.NATIVITY_CHILD_POSES + ("smile_up", "point_up", "wave", "cheer", "pray")]
    items += [("decorate item='star'", lambda x, y, s: C.child(x, y, s, pose="decorate", outfit="jumper", item="star")),
              ("place item='sheep'", lambda x, y, s: C.child(x, y, s, pose="place", outfit="jumper", item="sheep")),
              ("raincoat decorate", lambda x, y, s: C.child(x, y, s, pose="decorate")),
              ("pyjamas place", lambda x, y, s: C.child(x, y, s, pose="place", outfit="pyjamas"))]
    out.append(("nativity_child", "child(outfit='jumper') — the boy at the Christmas tree; the new poses (scale 1.1)", items, 8, 240, 330,
                1.1, {"ground_pad": 22}))
    return out


def _panel(x0, y0, w, h, markup, key):
    """Clip one composition panel to its rectangle."""
    cid = f"natpanel{key}"
    return (f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{markup}</g>')


def nativity_group():
    """Compositions: the scale line-up, the journey, the stable, the shepherds and the angel, the wise men's visit."""
    PR = C._prp()
    W, H = 2300, 64 + 4 * 600
    top = 64
    body = ""
    labels = []
    gy = top + 540
    b = f'<rect x="0" y="{top}" width="{W}" height="600" fill="#e8d6ae"/>'
    xs = 80
    for fn, kw, w in ((C.mary, {}, 150), (C.mary, {"pregnant": True}, 150), (C.joseph_carpenter, {}, 180), (C.angel, {"glow": 0.4}, 260),
                      (C.shepherds, {"variant": 1}, 170), (C.shepherds, {"variant": 2, "pose": "hold_lamb"}, 140), (C.shepherds, {"variant": 3}, 170),
                      (C.wise_men, {"variant": 0}, 160), (C.wise_men, {"variant": 1}, 160), (C.wise_men, {"variant": 2}, 170),
                      (C.townsfolk, {"kind": "innkeeper"}, 170), (C.townsfolk, {"kind": "herald"}, 160), (C.child, {"outfit": "jumper"}, 120)):
        b += fn(xs, gy, 1.0, **kw)
        xs += w
    b += C.toddler_jesus(xs, gy, 1.0, pose="stand") + C.baby_jesus(xs + 100, gy, 1.0)
    body += _panel(0, top, W, 600, b, 1)
    labels.append((20, gy + 14, "scale 1, one ground line: Mary, Mary pregnant, Joseph, angel, shepherds (old, boy with lamb, sturdy), wise men 0-2, innkeeper, herald, the jumper boy, toddler, baby"))
    gy2 = gy + 600
    b = PR.day_night_sky(0, gy2 - 540, 1150, gy2 + 60, t=0.47, scale=0.6)
    b += PR.journey_road(0, 1150, gy2 - 260, 0.6, time="dusk")
    pts = PR.road_points(0, 1150, gy2 - 260, 0.6)
    px, py, kk = pts[1]
    kk *= 0.5
    b += PR.donkey(px, py, kk, 1, pose="walk_b", saddle="blue", bridle=True)
    b += C.mary(*PR.donkey_points(px, py, kk, pose="walk_b")["seat"], kk, pose="ride", pregnant=True, expr="tired")
    b += C.joseph_carpenter(PR.donkey_points(px, py, kk)["lead"][0] - C.JOSEPH_LEAD_HAND[0] * kk, py, kk, pose="lead_b")
    body += _panel(0, gy2 - 540, 1150, 600, b, 2)
    sx, sy = 1720, gy2 + 30
    b = PR.starry_sky(1150, gy2 - 540, W, gy2 + 60, density=0.6)
    b += PR.stable(sx, sy, 0.42, part="back")
    sp = PR.stable_points(sx, sy, 0.42)
    b += PR.ox(*sp["ox"], 0.42 * 0.9, -1, pose="lie_look") + PR.donkey(*sp["donkey"], 0.42 * 0.9, 1, pose="look", sacks=0)
    b += C.joseph_carpenter(*sp["joseph"], 0.42, 1, pose="hold_lamp")
    b += C.mary(sp["mary"][0] - 30, sp["mary"][1], 0.42, 1, pose="lay_baby")
    b += PR.manger(*sp["manger"], 0.42, part="front", time="day")
    b += PR.stable(sx, sy, 0.42, part="front")
    body += _panel(1150, gy2 - 540, 1150, 600, b, 3)
    labels.append((20, gy2 + 30, "the journey: journey_road, donkey walk + Mary ride (pregnant, tired) + Joseph lead | the stable: Mary lay_baby over the manger, Joseph hold_lamp, ox lie_look, donkey look"))
    gy3 = gy2 + 600
    b = PR.starry_sky(0, gy3 - 540, 1150, gy3 + 60, density=0.9, seed=4)
    b += PR.night_hills(0, 1150, gy3 - 60, 0.55, part="back", town=True)
    b += PR.glory(600, gy3, 0.5)
    b += PR.night_hills(0, 1150, gy3 - 60, 0.55, part="front", fire=0.0, fire_x=False, fold_x=980)
    for i, (dx, v, p) in enumerate(((380, 0, "shield_eyes"), (480, 1, "kneel"), (560, 5, "shield_eyes"), (290, 2, "hold_lamb"))):
        b += C.shepherds(dx, gy3 + 10, 0.5, 1, variant=v, pose=p)
    b += C.angel(740, gy3, 0.5, -1, pose="float", glow=1.0, lift=50)
    b += PR.sheep(850, gy3 + 20, 0.42, -1, pose="look_up") + PR.sheep(930, gy3 + 30, 0.42, -1, variant=2, pose="look_up")
    body += _panel(0, gy3 - 540, 1150, 600, b, 4)
    b = PR.starry_sky(1150, gy3 - 540, W, gy3 + 60, density=0.9, seed=6)
    b += PR.night_hills(1150, W, gy3 - 60, 0.55, part="back", town=False)
    b += PR.heaven_light(1720, gy3 - 330, 0.5, progress=0.8) + C.angel_choir(1250, 2200, gy3 - 200, n=10, scale=0.22, rows=2)
    b += PR.night_hills(1150, W, gy3 - 60, 0.55, part="front", fire=0.6, fire_x=1300, fold_x=False)
    b += C.shepherds(1500, gy3 + 10, 0.5, 1, variant=3, pose="kneel") + C.shepherds(1640, gy3 + 14, 0.5, 1, variant=0, pose="point_up")
    b += C.shepherds(1800, gy3 + 10, 0.5, -1, variant=4, pose="cheer") + PR.sheep(1950, gy3 + 30, 0.4, -1, pose="look_up", lamb=True)
    body += _panel(1150, gy3 - 540, 1150, 600, b, 5)
    labels.append((20, gy3 + 30, "the shepherds: glory round the group, angel float (lift 50) beside them, shield_eyes / kneel / hold_lamb, sheep look_up | heaven_light + angel_choir; kneel, point_up, cheer"))
    gy4 = gy3 + 600
    b = PR.family_house(560, gy4 - 30, 0.5, view="interior", star_light=0.7)
    b += C.mary(560 + (PR.FAMILY_SEAT[0] + 50) * 0.5, gy4 - 30, 0.5, pose="sit_hold")
    b += C.joseph_carpenter(330, gy4 - 40, 0.48, pose="watch")
    for i, (dx, v, p, o) in enumerate(((640, 0, "kneel_offer", 1.0), (760, 2, "bow", 0.0), (880, 1, "present", 0.6))):
        b += C.wise_men(dx, gy4 - 26 + 4 * i, 0.5, -1, variant=v, pose=p, gift_open=o, gift_glow=o)
    body += _panel(0, gy4 - 540, 1150, 600, b, 6)
    b = PR.starry_sky(1150, gy4 - 540, W, gy4 + 60, density=0.7, seed=9)
    b += PR.bethlehem_town(1150, W, gy4 - 200, 0.4, time="night", part="back")
    b += PR.the_star(1700, gy4 - 470, 0.4, beam=0.8, beam_to=(1700, gy4 - 300))
    b += PR.family_house(1700, gy4 - 20, 0.42, star_light=0.8)
    for i, v in enumerate((0, 1, 2)):
        cx = 1300 + i * 150
        b += PR.camel(cx, gy4 + 30, 0.3, pose="walk", phase=0.25 * i, saddle=("red", "green", "purple")[v], load=False)
        b += C.wise_men(*PR.camel_points(cx, gy4 + 30, 0.3, pose="walk", phase=0.25 * i)["seat"], 0.3, variant=v, pose="ride")
    body += _panel(1150, gy4 - 540, 1150, 600, b, 7)
    labels.append((20, gy4 + 30, "the visit (Matthew 2): family_house interior, Mary sit_hold on the bench, Joseph watch, wise men kneel_offer / bow / present (gifts open, glowing) | the star stops over the house; camels with riders"))
    svg = S.svg_doc(body, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = watercolor(raster.rasterize(svg, W, H), seed=11)
    sheet, d = _finish(fig, W, H, "Nativity film — scale line-up, the journey, the stable, the shepherds and the angels, the wise men's visit")
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    for x0, y0, text in labels:
        d.text((x0, y0), text, fill=INK_RGB, font=font)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "characters_nativity_group.png"
    sheet.save(path)
    return path


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
    for name in C.FAMILY:
        for p in C.NOAH_POSES:
            jobs.append((name, p, lambda x, y, p=p, name=name: C.family_member(name, x, y, pose=p)))
    for p in C.CHILD_POSES:
        jobs.append(("child", p, lambda x, y, p=p: C.child(x, y, pose=p)))
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
    if not filt or any(f in "noah_group" for f in filt):
        print(noah_group())
    if not filt or any(f in "joseph_group" for f in filt):
        print(joseph_group())
    if not filt or any(f in "storm_group" for f in filt):
        print(storm_group())
    if not filt or any(f in "nativity_group" for f in filt):
        print(nativity_group())
    raster.close()


if __name__ == "__main__":
    main()
