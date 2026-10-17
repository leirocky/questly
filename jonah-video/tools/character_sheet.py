"""Render labelled contact sheets of the people library (art/characters.py).

Every function / pose / expression is drawn on cream paper exactly as the film shows it
(SVG -> engine.raster.rasterize -> engine.watercolor.watercolor). A small cross marks each
figure's anchor point (x, y) and a faint line marks the ground.

  python3 tools/character_sheet.py            # all sheets
  python3 tools/character_sheet.py jonah      # only sheets whose name contains "jonah"
  python3 tools/character_sheet.py --bbox     # also print measured bounding boxes (scale 1)

Output: build/preview/characters_*.png (each <= 2400 px wide).
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
            defs += f'<clipPath id="{cid}"><rect x="{x0 + 4}" y="{y0 + 4}" width="{cell_w - 8}" height="{cell_h - LABEL_H - 6}"/></clipPath>'
            g = f'<g clip-path="url(#{cid})">{g}</g>'
        body += g
    svg = S.svg_doc(body, defs=defs, w=W, h=H).replace(BOIL_TOKEN, "1")
    fig = raster.rasterize(svg, W, H)
    fig = watercolor(fig, seed=11)
    paper = Image.new("RGBA", (W, H), S.hex_rgb(S.P["paper"]) + (255,))
    pd = ImageDraw.Draw(paper)
    for cx, cy, _ in anchors:
        pd.line([(cx - cell_w * 0.42, cy), (cx + cell_w * 0.42, cy)], fill=(214, 196, 160, 255), width=2)
    sheet = Image.alpha_composite(paper, fig)
    rgb = np.asarray(sheet.convert("RGB"))
    rgb = apply_paper(rgb, paper_multiplier(W, H))
    sheet = Image.fromarray(rgb)
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONT_REGULAR), 22)
    tfont = ImageFont.truetype(str(FONT_BOLD), 34)
    d.text((18, 14), title, fill=(75, 52, 38), font=tfont)
    bboxes = {}
    alpha = np.asarray(fig)[..., 3]
    for i, (cx, cy, label) in enumerate(anchors):
        x0 = int((i % cols) * cell_w)
        y0 = int(top + (i // cols) * cell_h)
        d.text((x0 + 10, y0 + cell_h - LABEL_H + 4), label, fill=(75, 52, 38), font=font)
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
                [(p, _j(p)) for p in jp], 6, 380, 450, 1.0, {}))
    ex = list(C.EXPRESSIONS)
    items = [(e, _j("stand", e)) for e in ex]
    items += [("wet=True", _j("stand", "sad", wet=True)), ("facing=-1 happy", _j("stand", "happy", -1)),
              ("float wet", _j("float", wet=True))]
    out.append(("jonah_expr", "Jonah — expressions (scale 1.5, upper body)", items, 8, 290, 330, 1.5,
                {"clip_cells": True, "ground_pad": -150}))
    items = [(p, _j(p)) for p in jp] + [(p + " -1", _j(p, facing=-1)) for p in jp]
    out.append(("jonah_small", "Jonah — readability check at scale 0.45 (top: facing=1, bottom: facing=-1)",
                items, 10, 190, 230, 0.45, {"ground_pad": 14}))
    items = []
    for v in range(4):
        for p in C.SAILOR_POSES:
            items.append((f"v{v} {p}", lambda x, y, s, v=v, p=p: C.sailor(x, y, s, 1, variant=v, pose=p)))
    out.append(("sailors", "Sailors — variants 0-3 x poses (scale 0.8)", items, 8, 290, 340, 0.8, {}))
    items = [(f"captain {p}", lambda x, y, s, p=p: C.captain(x, y, s, 1, pose=p)) for p in C.CAPTAIN_POSES]
    items += [(f"king {p}", lambda x, y, s, p=p: C.king(x, y, s, 1, pose=p)) for p in C.KING_POSES]
    items += [(f"sack {p}", lambda x, y, s, p=p: C.king(x, y, s, 1, pose=p, attire="sackcloth"))
              for p in C.KING_POSES]
    out.append(("captain_king", "Captain and King of Nineveh (scale 0.85)", items, 7, 330, 400, 0.85, {}))
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
    return out


def main():
    filt = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_bbox = "--bbox" in sys.argv
    allbb = {}
    for name, title, items, cols, cw, ch, sc, kw in sheets():
        if filt and not any(f in name for f in filt):
            continue
        path, bb = render_sheet(name, title, items, cols, cw, ch, sc, **kw)
        allbb[name] = bb
        print(path)
        if show_bbox:
            for k, v in bb.items():
                print(f"   {k:28s} {v}")
    (OUT / "characters_bbox.json").write_text(json.dumps(allbb, indent=1))
    raster.close()


if __name__ == "__main__":
    main()
