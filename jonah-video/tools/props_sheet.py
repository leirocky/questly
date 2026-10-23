"""Labelled contact sheets of every drawing in art/props.py.

Run from jonah-video/:
  python3 tools/props_sheet.py                 # all sheets
  python3 tools/props_sheet.py fish ship       # only some sheets
Writes build/preview/props_<sheet>.png (each <= 2400 px wide), rendered exactly like the film:
engine.raster (Chromium) + engine.watercolor + cream paper grain.

Overlays (not part of the art): a red cross marks each drawing's anchor (x, y); a faint dashed
grey figure is a 330 px adult at the same scale; dashed blue boxes show documented regions
(fish mouth box, ship cutaway interior / bed, castor shade, booth seat). Characters (Jonah, the king,
sailors) come from art/characters.py to check the props against them.
David film: python3 tools/props_sheet.py david_items david_creatures david_camp valley
Noah film: python3 tools/props_sheet.py noah_ark noah_animals noah_pairs noah_weather noah_items
Joseph film: python3 tools/props_sheet.py joseph_items joseph_animals joseph_egypt
Storm film: python3 tools/props_sheet.py storm_boat storm_lake storm_weather storm_items storm_story
Nativity film: python3 tools/props_sheet.py nativity_stable nativity_animals nativity_places nativity_sky nativity_journey
  nativity_items nativity_home
Environment (optional): PB_PREVIEW_DIR=<dir> writes the sheets there instead of build/preview; PB_RASTER_CACHE=<dir>
uses a separate raster cache (e.g. a scratch folder you delete afterwards).
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from art import characters as CH  # noqa: E402
from art import props as PR  # noqa: E402
from art import style as S  # noqa: E402
from art.style import P  # noqa: E402
from engine import raster, watercolor  # noqa: E402
from engine.paths import BUILD, FONT_BOLD  # noqa: E402
from engine.scene import BOIL_TOKEN  # noqa: E402

LABEL_H = 44
OUT = Path(os.environ.get("PB_PREVIEW_DIR") or BUILD / "preview")   # PB_PREVIEW_DIR: write sheets elsewhere
if os.environ.get("PB_RASTER_CACHE"):          # optional separate raster cache (e.g. a scratch dir you delete)
    raster._RASTER_DIR = Path(os.environ["PB_RASTER_CACHE"])
MAX_W = 2400


def person_ref(x, y, s=1.0):
    """Dashed silhouette of a 330 px adult standing at (x, y) — scale reference only."""
    d = (f"M{x - 40 * s},{y} L{x - 54 * s},{y - 70 * s} L{x - 44 * s},{y - 250 * s} Q{x},{y - 268 * s} "
         f"{x + 44 * s},{y - 250 * s} L{x + 54 * s},{y - 70 * s} L{x + 40 * s},{y} Z")
    return (f'<g opacity="0.55"><path d="{d}" fill="#bfae96" fill-opacity="0.35" stroke="#7a6a58" '
            f'stroke-width="2.5" stroke-dasharray="8 6"/>'
            f'<circle cx="{x}" cy="{y - 292 * s}" r="{36 * s}" fill="#bfae96" fill-opacity="0.35" stroke="#7a6a58" '
            f'stroke-width="2.5" stroke-dasharray="8 6"/></g>')


def lying_ref(x0, x1, y, s=1.0):
    """Dashed silhouette of a person lying down from x0 (head) to x1 (feet), back on y."""
    h = 96 * s
    return (f'<g opacity="0.55"><rect x="{min(x0, x1) + 60 * s}" y="{y - h}" width="{abs(x1 - x0) - 60 * s}" height="{h}" '
            f'rx="{40 * s}" fill="#bfae96" fill-opacity="0.35" stroke="#7a6a58" stroke-width="2.5" '
            f'stroke-dasharray="8 6"/><circle cx="{min(x0, x1) + 36 * s}" cy="{y - 40 * s}" r="{36 * s}" '
            f'fill="#bfae96" fill-opacity="0.35" stroke="#7a6a58" stroke-width="2.5" stroke-dasharray="8 6"/></g>')


def box(x0, y0, x1, y1, color="#3a7bd5"):
    return (f'<rect x="{min(x0, x1)}" y="{min(y0, y1)}" width="{abs(x1 - x0)}" height="{abs(y1 - y0)}" fill="none" '
            f'stroke="{color}" stroke-width="3" stroke-dasharray="12 8" opacity="0.8"/>')


class Cell:
    def __init__(self, label, art, w, anchors=(), overlay=""):
        """art(ox, oy) -> markup in sheet coords given the cell's top-left (ox, oy) below the label strip.
        anchors: list of (dx, dy) relative to (ox, oy); overlay(ox, oy) -> markup drawn without watercolour."""
        self.label, self.art, self.w, self.anchors, self.overlay = label, art, w, anchors, overlay


def render_sheet(name, title, rows):
    """rows: list of (height, [Cell, ...])."""
    W = max(sum(c.w for c in cells) for _, cells in rows)
    assert W <= MAX_W, (name, W)
    H = 70 + sum(h + LABEL_H for h, _ in rows)
    art, over, labels, marks, grid = [], [], [], [], []
    y = 70
    for h, cells in rows:
        x = 0
        for c in cells:
            ox, oy = x, y + LABEL_H
            cid = f"cell{len(labels)}"
            art.append(f'<clipPath id="{cid}"><rect x="{ox}" y="{oy}" width="{c.w}" height="{h}"/></clipPath>'
                       f'<g clip-path="url(#{cid})">{c.art(ox, oy)}</g>')
            if c.overlay:
                over.append(f'<g clip-path="url(#{cid})">{c.overlay(ox, oy)}</g>')
            labels.append((x + 12, y + 8, c.label))
            marks += [(ox + ax, oy + ay) for ax, ay in c.anchors]
            grid.append((x, y, x + c.w, y + LABEL_H + h))
            x += c.w
        y += h + LABEL_H

    def ras(body, defs=""):
        svg = S.svg_doc(body, defs=defs, w=W, h=H).replace(BOIL_TOKEN, "1")
        return raster.rasterize(svg, W, H)

    clip_defs = "".join(a[: a.index("</clipPath>") + 11] for a in art)
    art_im = watercolor.watercolor(ras("".join(art)), seed=5)
    over_im = ras("".join(over), clip_defs) if over else None
    sheet = Image.new("RGBA", (W, H), S.hex_rgb(P["paper"]) + (255,))
    sheet.alpha_composite(art_im)
    if over_im is not None:
        sheet.alpha_composite(over_im)
    rgb = sheet.convert("RGB")
    import numpy as np
    arr = watercolor.apply_paper(np.asarray(rgb), watercolor.paper_multiplier(W, H))
    rgb = Image.fromarray(arr)
    d = ImageDraw.Draw(rgb)
    f_title = ImageFont.truetype(str(FONT_BOLD), 40)
    f_lab = ImageFont.truetype(str(FONT_BOLD), 24)
    d.text((16, 14), title, fill=S.hex_rgb(P["ink"]), font=f_title)
    for x0, y0, x1, y1 in grid:
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(196, 180, 150), width=2)
    for x, yy, txt in labels:
        d.text((x, yy), txt, fill=S.hex_rgb(P["ink"]), font=f_lab)
    for mx, my in marks:
        d.line([mx - 11, my, mx + 11, my], fill=(214, 64, 52), width=3)
        d.line([mx, my - 11, mx, my + 11], fill=(214, 64, 52), width=3)
    out = OUT / f"props_{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    rgb.save(out)
    print(out, rgb.size)
    return out


# ------------------------------------------------------------------ sheets


def mouth_box(cx, cy, s, f, m):
    b = PR.fish_mouth_points(m)["box"]
    p0 = PR.local_to_stage(cx, cy, s, f, b[0], b[1])
    p1 = PR.local_to_stage(cx, cy, s, f, b[2], b[3])
    return box(p0[0], p0[1], p1[0], p1[1])


def swallow(cx, cy, s, f, m, dx=0.0, dy=0.0, js=0.8, eye="open"):
    """fish(part='back') -> Jonah clipped with in_fish_mouth -> fish(part='front')."""
    c = PR.fish_mouth_points(m)["center"]
    jx, jy = PR.local_to_stage(cx, cy, s, f, c[0] + dx, c[1] + 132 * js / 0.8 + dy)
    j = CH.jonah(jx, jy, js * s, -f, pose="float")
    return (PR.fish(cx, cy, s, f, mouth=m, eye=eye, part="back") + PR.in_fish_mouth(j, cx, cy, s, f, m) +
            PR.fish(cx, cy, s, f, mouth=m, eye=eye, part="front"))


def sheet_fish():
    s = 0.38

    def fcell(label, **kw):
        ax = 270 if kw.get("facing", 1) < 0 else 330
        m = kw.get("mouth", 0)
        ov = (lambda ox, oy: mouth_box(ox + ax, oy + 215, s, kw.get("facing", 1), m)) if m > 0.2 else ""
        return Cell(label, lambda ox, oy: PR.fish(ox + ax, oy + 215, s, **kw), 600, [(ax, 215)], ov)
    rows = [
        (420, [fcell(f"fish mouth={m} (blue: mouth box)", mouth=m) for m in (0, 0.33, 0.66, 1.0)]),
        (420, [fcell(f"eye='{e}'", eye=e, mouth=mo) for e, mo in
               (("open", 0.1), ("closed", 0.0), ("happy", 0.25), ("surprised", 0.5))]),
        (420, [fcell("tail=-1", tail=-1), fcell("tail=-0.5 blush=False", tail=-0.5, blush=False),
               fcell("tail=0.5 facing=-1", tail=0.5, facing=-1), fcell("tail=1 facing=-1 mouth=0.66", tail=1,
                                                                         facing=-1, mouth=0.66)]),
        (520, [Cell("part='back' + jonah 0.8 (in_fish_mouth) + part='front'",
                    lambda ox, oy: swallow(ox + 360, oy + 260, 0.5, 1, 1.0), 800, [(360, 260)],
                    lambda ox, oy: mouth_box(ox + 360, oy + 260, 0.5, 1, 1.0)),
               Cell("swallow: mouth=0.8, Jonah half in", lambda ox, oy: swallow(ox + 360, oy + 260, 0.5, 1, 0.8, dx=150,
                                                                              dy=-30),
                    800, [(360, 260)]),
               Cell("spit out, facing=-1: mouth=1, Jonah leaving", lambda ox, oy: swallow(ox + 440, oy + 260, 0.5, -1, 1.0,
                                                                                       dx=260, dy=-40, eye="happy"),
                    800, [(440, 260)])]),
        (720, [Cell("scale 0.75, mouth=1 vs a 330px adult (same scale)",
                    lambda ox, oy: PR.fish(ox + 560, oy + 340, 0.75, mouth=1.0) + person_ref(ox + 1110, oy + 600, 0.75),
                    1200, [(560, 340)], lambda ox, oy: mouth_box(ox + 560, oy + 340, 0.75, 1, 1.0)),
               Cell("scale 0.75 facing=-1 mouth=0.5 eye='happy' tail=0.6",
                    lambda ox, oy: PR.fish(ox + 640, oy + 340, 0.75, facing=-1, mouth=0.5, eye="happy", tail=0.6),
                    1200, [(640, 340)])]),
    ]
    return render_sheet("fish", "props.fish — the great fish (anchor = body centre)", rows)


def sheet_ship():
    s = 0.6
    gy = 600

    def scell(label, ref=True, **kw):
        def art(ox, oy):
            return PR.ship(ox + 400, oy + gy, s, **kw)
        ov = (lambda ox, oy: person_ref(ox + 470, oy + gy + PR.SHIP_DECK_Y * s, s)) if ref else ""
        return Cell(label, art, 800, [(400, gy)], ov)

    def cut_overlay(ox, oy, cx, cy, sc, f=1):
        x0, y0, x1, y1 = PR.SHIP_INTERIOR
        bx0, bx1, by = PR.SHIP_BED
        p0 = PR.local_to_stage(cx, cy, sc, f, x0, y0)
        p1 = PR.local_to_stage(cx, cy, sc, f, x1, y1)
        b0 = PR.local_to_stage(cx, cy, sc, f, bx0, by)
        b1 = PR.local_to_stage(cx, cy, sc, f, bx1, by)
        return box(p0[0], p0[1], p1[0], p1[1]) + box(b0[0], b0[1] - 4, b1[0], b1[1] + 4, "#2a9d6f")

    def sleeper(cx, cy, sc, f=1):
        jx, jy = PR.local_to_stage(cx, cy, sc, f, *PR.SHIP_SLEEP)
        return CH.jonah(jx, jy, sc, f, pose="sleep")

    def layered(ox, oy):
        cx, cy = ox + 400, oy + gy
        return (PR.ship(cx, cy, s, part="back") + CH.sailor(cx - 60, cy + PR.SHIP_DECK_Y * s, s, 1, 1, pose="scared") +
                CH.captain(cx + 150, cy + PR.SHIP_DECK_Y * s, s, -1) + PR.ship(cx, cy, s, part="front"))

    rows = [
        (720, [scell("sail='full' (person ref on deck)"), scell("sail='furled'", sail="furled"),
               scell("sail='torn' oars=True", sail="torn", oars=True)]),
        (720, [Cell("cutaway=True + jonah sleep at SHIP_SLEEP", lambda ox, oy: PR.ship(ox + 400, oy + gy, s, sail="furled",
                                                                                     cutaway=True) +
                    sleeper(ox + 400, oy + gy, s), 800, [(400, gy)],
                    lambda ox, oy: cut_overlay(ox, oy, ox + 400, oy + gy, s)),
               scell("facing=-1 lantern=False flag=False", facing=-1, lantern=False, flag=False),
               Cell("part='back' + crew on deck + part='front'", layered, 800, [(400, gy)])]),
        (700, [Cell("cutaway close-up, scale 1.5, facing=-1: jonah(*local_to_stage(..SHIP_SLEEP), facing=-1, "
                    "pose='sleep'); blue SHIP_INTERIOR, green SHIP_BED",
                    lambda ox, oy: PR.ship(ox + 1200, oy + 470, 1.5, -1, sail="furled", cutaway=True) +
                    sleeper(ox + 1200, oy + 470, 1.5, -1), 2400, [(1200, 470)],
                    lambda ox, oy: cut_overlay(ox, oy, ox + 1200, oy + 470, 1.5, -1))]),
    ]
    return render_sheet("ship", "props.ship — anchor = hull waterline centre; deck y = SHIP_DECK_Y", rows)


def sheet_items():
    def c(label, fn, w=400, ax=200, ay=260, ref=None, ov=None):
        o = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], 1.0)) if ref else (ov or "")
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], o)
    dx = PR.KING_ASH_DX

    def ashes(x, y, s=1.0, f=1):
        """ash_pile(part='back') -> king(sit_ashes, ashes=False) -> ash_pile(part='front')."""
        hx = x + dx * s * f
        return (PR.ash_pile(hx, y, s, smoke=True, facing=f, part="back") +
                CH.king(x, y, s, f, pose="sit_ashes", ashes=False) + PR.ash_pile(hx, y, s, facing=f, part="front"))
    rows = [
        (340, [c("crate (centre)", lambda x, y: PR.crate(x, y, 1.4), w=340, ax=170),
               c("jar / amphora (centre)", lambda x, y: PR.jar(x - 30, y, 1.4) + PR.jar(x + 100, y + 40, 0.8, rot=12,
                                                                                         color=P["sand_dark"]),
                 w=340, ax=170),
               c("sack (bottom)", lambda x, y: PR.sack(x, y + 50, 1.4) + PR.sack(x + 110, y + 50, 0.9, seed=3), w=340,
                 ax=150),
               c("lots_jar (bottom)", lambda x, y: PR.lots_jar(x, y + 50, 1.4), w=340, ax=170),
               c("lot / lot(marked=True)", lambda x, y: PR.lot(x - 70, y, 1.3, rot=-10) +
                 PR.lot(x + 70, y - 10, 1.3, rot=8, marked=True), w=340, ax=170, ay=200),
               c("lantern lit (top hook)", lambda x, y: PR.lantern(x, y, 1.4), w=340, ax=170, ay=60),
               c("lantern(lit=False)", lambda x, y: PR.lantern(x, y, 1.4, lit=False), w=340, ax=170, ay=60)]),
        (300, [c("rope_coil (bottom)", lambda x, y: PR.rope_coil(x, y, 1.5)),
               c("scroll (centre)", lambda x, y: PR.scroll(x, y, 1.5), ay=160),
               c("scroll(opened=True)", lambda x, y: PR.scroll(x, y, 1.4, opened=True), ay=160),
               c("ash_pile (bottom centre)", lambda x, y: PR.ash_pile(x, y, 1.3)),
               c("ash_pile(smoke=True)", lambda x, y: PR.ash_pile(x, y, 1.0, smoke=True)),
               c("lot rot=40, scale 2", lambda x, y: PR.lot(x, y, 2.0, rot=40, marked=True), ay=160)]),
        (460, [c("throne (anchor = seated king's anchor)", lambda x, y: PR.throne(x, y), w=480, ax=180, ay=420,
                 ref=(400, 420)),
               c("throne + king(sit_throne, throne=False)", lambda x, y: PR.throne(x, y) +
                 CH.king(x, y, 1.0, 1, pose="sit_throne", throne=False), w=480, ax=180, ay=420),
               c("throne facing=-1, king stands up", lambda x, y: PR.throne(x + 80, y, 1.0, -1) +
                 CH.king(x - 110, y, 1.0, 1, pose="remove_crown"), w=480, ax=220, ay=420),
               c("ash back + king(sit_ashes) + ash front", lambda x, y: ashes(x, y), w=480, ax=200, ay=420),
               c("same, facing=-1, scale 0.8", lambda x, y: ashes(x, y, 0.8, -1), w=480, ax=280, ay=420)]),
        (520, [c("booth (bottom) + 330px adult; blue = BOOTH_SEAT", lambda x, y: PR.booth(x, y), w=600, ax=280, ay=480,
                 ov=lambda ox, oy: person_ref(ox + 280, oy + 480) + box(ox + 280 + PR.BOOTH_SEAT[0],
                                                                        oy + 480 + PR.BOOTH_SEAT[1],
                                                                        ox + 280 + PR.BOOTH_SEAT[2],
                                                                        oy + 480 + PR.BOOTH_SEAT[3])),
               c("booth(shade=True) + jonah(pose='sit_sulk')", lambda x, y: PR.booth(x, y, shade=True) +
                 CH.jonah(x - 10, y, 1.0, 1, pose="sit_sulk"), w=600, ax=280, ay=480),
               c("booth facing=-1, scale 0.7, shade + jonah sit", lambda x, y: PR.booth(x, y, 0.7, facing=-1, shade=True) +
                 CH.jonah(x + 10, y, 0.7, -1, pose="sit"), w=600, ax=320, ay=480),
               c("booth + standing jonah (head above the eaves)", lambda x, y: PR.booth(x, y) +
                 CH.jonah(x + 40, y, 1.0, -1), w=600, ax=280, ay=480)]),
    ]
    return render_sheet("items", "props — small props (scaled up for viewing unless noted)", rows)


def sheet_castor():
    s = 0.62

    def cc(label, w=800, ax=280, **kw):
        def ov(ox, oy):
            return person_ref(ox + ax - 80, oy + 600, s)
        return Cell(label, lambda ox, oy: PR.castor_plant(ox + ax, oy + 600, s, **kw), w, [(ax, 600)], ov)

    def shade_ov(ox, oy, cx, cy, sc):
        x0, x1 = PR.CASTOR_SHADE
        return box(cx + x0 * sc, cy - 14, cx + x1 * sc, cy + 6, "#3a7bd5") + person_ref(cx + 260 * sc, cy, sc)

    def booth_combo(ox, oy, wither=0.0, pose="sit_sulk"):
        x, y = ox + 280, oy + 600
        return (PR.booth(x + PR.CASTOR_BOOTH_DX * s, y, s) +
                CH.jonah(x + (PR.CASTOR_BOOTH_DX - 10) * s, y, s, -1, pose=pose) +
                PR.castor_plant(x, y, s, wither=wither))
    rows = [
        (640, [cc(f"growth={g} (dashed: 330px adult)", growth=g) for g in (0.0, 0.25, 0.5)]),
        (640, [cc("growth=0.75", growth=0.75),
               Cell("growth=1 side=1: blue = CASTOR_SHADE ground strip", lambda ox, oy: PR.castor_plant(ox + 280, oy + 600, s),
                    800, [(280, 600)], lambda ox, oy: shade_ov(ox, oy, ox + 280, oy + 600, s)),
               cc("wither=0.25", wither=0.25)]),
        (640, [cc(f"wither={w}", wither=w) for w in (0.5, 0.75, 1.0)]),
        (520, [Cell(f"bite={b} (scale 2.2, with worm)",
                    lambda ox, oy, b=b: PR.castor_plant(ox + 260, oy + 480, 2.2, growth=1.0, bite=b) +
                    PR.worm(ox + 260 - PR.WORM_BITE_DX * 2.2, oy + 480, 2.2, chomp=b), 480, [(260, 480)])
               for b in (0.0, 0.25, 0.5, 0.75, 1.0)]),
        (420, [Cell(f"wither={w} beside Jonah (scale 0.45)",
                    lambda ox, oy, w=w: PR.castor_plant(ox + 170, oy + 400, 0.45, wither=w) +
                    CH.jonah(ox + 100, oy + 400, 0.45, 1), 480, [(170, 400)]) for w in (0.0, 0.25, 0.5, 0.75, 1.0)]),
        (420, [Cell("bite=1 at film scale 0.62 + worm (chomp=1)",
                    lambda ox, oy: PR.castor_plant(ox + 300, oy + 400, s, bite=1.0) +
                    PR.worm(ox + 300 - PR.WORM_BITE_DX * s, oy + 400, s, chomp=1.0), 800, [(300, 400)]),
               Cell("bite=0.5 at scale 1 + worm", lambda ox, oy: PR.castor_plant(ox + 300, oy + 400, 1.0, bite=0.5) +
                    PR.worm(ox + 300 - PR.WORM_BITE_DX, oy + 400, 1.0, chomp=0.5), 800, [(300, 400)]),
               Cell("bite=1 wither=1 side=-1 scale 0.62", lambda ox, oy: PR.castor_plant(ox + 500, oy + 400, s, bite=1.0,
                                                                                        wither=1.0, side=-1),
                    800, [(500, 400)])]),
        (640, [Cell("booth at x+CASTOR_BOOTH_DX*s (270) + jonah sit_sulk", booth_combo, 800, [(280, 600)]),
               Cell("same, wither=1, jonah sit_faint", lambda ox, oy: booth_combo(ox, oy, 1.0, "sit_faint"), 800,
                    [(280, 600)]),
               Cell("side=-1 growth=0.6 wither=0.3", lambda ox, oy: PR.castor_plant(ox + 560, oy + 600, s, growth=0.6,
                                                                                   wither=0.3, side=-1),
                    800, [(560, 600)])]),
    ]
    return render_sheet("castor", "props.castor_plant — anchor = root point; growth / wither / bite", rows)


def sheet_plants():
    def c(label, fn, w=400, ax=200, ay=460, anchors=None):
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, anchors or [(ax, ay)])
    rows = [
        (720, [c("palm_tree", lambda x, y: PR.palm_tree(x, y, 1.0), w=460, ax=230, ay=700),
               c("palm_tree lean=0.6 sway=1", lambda x, y: PR.palm_tree(x, y, 1.0, lean=0.6, sway=1), w=560, ax=220,
                 ay=700),
               c("olive_tree", lambda x, y: PR.olive_tree(x, y, 1.1), w=440, ax=220, ay=700),
               c("reeds variant 0 / variant 1 sway=1", lambda x, y: PR.reeds(x - 110, y, 1.4) +
                 PR.reeds(x + 70, y, 1.4, 1, sway=1), w=560, ax=240, ay=700, anchors=[(130, 700), (310, 700)]),
               c("bush variant=0 / 1", lambda x, y: PR.bush(x - 90, y, 0.85) + PR.bush(x + 90, y, 0.85, 1),
                 w=380, ax=190, ay=700, anchors=[(100, 700), (280, 700)])]),
        (300, [c("bush variant=2 (dry shrub)", lambda x, y: PR.bush(x, y, 1.2, 2), ay=260),
               c("bush variant=3", lambda x, y: PR.bush(x, y, 1.2, 3), ay=260),
               c("grass_tuft variant 0/1/2", lambda x, y: PR.grass_tuft(x - 110, y, 1.4) + PR.grass_tuft(x, y, 1.4, 1)
                 + PR.grass_tuft(x + 110, y, 1.4, 2), ay=260),
               c("grass_tuft sway=-1/0/1", lambda x, y: PR.grass_tuft(x - 110, y, 1.4, sway=-1) + PR.grass_tuft(x, y, 1.4)
                 + PR.grass_tuft(x + 110, y, 1.4, sway=1), ay=260),
               c("seaweed variant=3 (coral)", lambda x, y: PR.seaweed(x, y, 1.4, 3), ay=260),
               c("seaweed variant=1", lambda x, y: PR.seaweed(x, y, 1.2, 1), ay=260)]),
        (330, [c("seaweed variant=0 / sway=1", lambda x, y: PR.seaweed(x - 80, y, 1.0) + PR.seaweed(x + 80, y, 1.0, sway=1),
                 ay=310, anchors=[(120, 310), (280, 310)]),
               c("seaweed variant=2 / sway=-1", lambda x, y: PR.seaweed(x - 80, y, 1.0, 2) +
                 PR.seaweed(x + 80, y, 1.0, 2, sway=-1), ay=310, anchors=[(120, 310), (280, 310)]),
               c("bush 2 scale 0.6 + grass (desert edge)", lambda x, y: PR.bush(x - 60, y, 0.6, 2) +
                 PR.grass_tuft(x + 30, y, 0.8, 1) + PR.bush(x + 100, y, 0.5, 2), ay=310)]),
    ]
    return render_sheet("plants", "props — plants (anchor = base on the ground)", rows)


def sheet_creatures():
    def c(label, fn, w=400, ax=200, ay=200, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)
    rows = [
        (240, [c(f"worm chomp={k} (scale 3)", lambda x, y, k=k: PR.worm(x, y, 3.0, chomp=k), ay=200) for k in (0, 0.5, 1.0)] +
         [c("worm crawl=1, facing=-1", lambda x, y: PR.worm(x, y, 3.0, facing=-1, crawl=1.0), ay=200),
          c("worm scale 1 next to castor base", lambda x, y: PR.castor_plant(x + 50, y, 1.0, growth=1, bite=0.6) +
            PR.worm(x + 50 - PR.WORM_BITE_DX, y, 1.0, chomp=1), ay=210),
          c("small_fish colours", lambda x, y: "".join(PR.small_fish(x - 120 + (i % 4) * 80, y - 70 + (i // 4) * 80, 0.9,
                                                                     color=k) for i, k in enumerate(PR.FISH_COLORS)),
            ay=150)]),
        (300, [c(f"gull wing={k}", lambda x, y, k=k: PR.gull(x, y, 1.3, wing=k), ay=170) for k in (-1, -0.5, 0, 0.5, 1)] +
         [c("gull pose='stand' / facing=-1", lambda x, y: PR.gull(x - 80, y, 1.3, pose="stand") +
            PR.gull(x + 90, y, 1.3, facing=-1, wing=0.3), ay=170)]),
        (260, [c(f"dove wing={k}", lambda x, y, k=k: PR.dove(x, y, 1.3, wing=k), ay=150) for k in (-1, -0.5, 0, 0.5, 1)] +
         [c("dove pose='stand', small_fish tail", lambda x, y: PR.dove(x - 80, y, 1.4, pose="stand") +
            PR.small_fish(x + 90, y - 20, 1.3, tail=1, color="teal"), ay=170)]),
        (470, [c(k, lambda x, y, k=k: PR.animal(x, y, 1.0, kind=k), w=480, ax=170 if k == "camel" else 200, ay=440,
                 ref=(430, 440, 1.0)) for k in ("sheep", "goat", "cow", "donkey", "camel")]),
        (470, [c(f"{k} sackcloth=True", lambda x, y, k=k: PR.animal(x, y, 1.0, kind=k, sackcloth=True), w=480,
                 ax=170 if k == "camel" else 200, ay=440) for k in ("sheep", "goat", "cow", "donkey", "camel")]),
        (300, [c("animal facing=-1 (sheep, goat)", lambda x, y: PR.animal(x - 90, y, 0.9, -1) +
                 PR.animal(x + 130, y, 0.9, -1, "goat", True), w=600, ax=300, ay=280),
               c("cow + donkey facing=-1, scale 0.6", lambda x, y: PR.animal(x - 120, y, 0.6, -1, "cow") +
                 PR.animal(x + 120, y, 0.6, -1, "donkey", True), w=600, ax=300, ay=280),
               c("gulls at ship-scale 0.6 near a 0.6 adult", lambda x, y: PR.gull(x - 60, y - 160, 0.6, wing=0.7) +
                 PR.gull(x + 60, y - 120, 0.6, wing=-0.6), w=600, ax=300, ay=280, ref=(160, 280, 0.6))]),
    ]
    return render_sheet("creatures", "props — creatures (worm/animals: bottom centre; birds/fish: body centre)", rows)


def sheet_buildings():
    def c(label, fn, w=600, ax=300, ay=520, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)

    def sky(fn):
        return lambda x, y: f'<rect x="{x - 1300}" y="{y - 560}" width="2600" height="620" fill="{P["sky_warm"]}"/>' + fn(x, y)
    rows = [
        (560, [c(f"house variant={v}, scale 0.45", lambda x, y, v=v: PR.house(x, y, 0.45, v), w=480, ax=230,
                 ref=(450, 520, 0.45)) for v in range(4)] +
              [c("house 1 facing=-1 (+0.45 adult)", lambda x, y: PR.house(x, y, 0.45, 1, facing=-1), w=480, ax=250,
                 ref=(40, 520, 0.45))]),
        (700, [c("city_wall gate=(gx, 220) height=300", lambda x, y: PR.city_wall(x - 580, x + 580, y, 300,
                                                                                    gate=(x, 220)),
                 w=1200, ax=600, ay=660, ref=(160, 660, 1.0)),
               c("city_wall doors_open=0.5 / 1.0 (height 380, gate 200)", lambda x, y: PR.city_wall(x - 600, x - 20, y, 380,
                                                                                        gate=(x - 310, 200),
                                                                                        doors_open=0.5)
                 + PR.city_wall(x + 20, x + 600, y, 380, gate=(x + 310, 200), doors_open=1.0), w=1200, ax=600, ay=660,
                 ref=(1010, 660, 1.0))]),
        (560, [c("ziggurat scale 0.4 (+0.4 adult)", lambda x, y: PR.ziggurat(x, y, 0.4), w=800, ax=400, ay=520,
                 ref=(50, 520, 0.4)),
               c("nineveh_skyline scale 1 seed 0 (on sky_warm)", sky(lambda x, y: PR.nineveh_skyline(x - 780, x + 780, y, 1.0)),
                 w=1600, ax=800, ay=520)]),
        (420, [c("nineveh_skyline scale 0.5 haze 0.5 seed 3", sky(lambda x, y: PR.nineveh_skyline(x - 580, x + 580, y, 0.5,
                                                                                                   seed=3, haze=0.5)),
                 w=1200, ax=600, ay=300),
               c("nineveh_skyline scale 0.3 haze 0.7 seed 5", sky(lambda x, y: PR.nineveh_skyline(x - 580, x + 580, y, 0.3,
                                                                                                   seed=5, haze=0.7)),
                 w=1200, ax=600, ay=300)]),
        (440, [c("city_wall height=160 ink=0.6 (distant)", lambda x, y: PR.city_wall(x - 360, x + 360, y, 160,
                                                                                       gate=(x + 80, 90), ink=0.6),
                 w=800, ax=400, ay=380, ref=(60, 380, 0.5)),
               c("harbor_dock (deck level y) scale 1", lambda x, y: PR.harbor_dock(x - 260, x + 260, y), w=600, ax=300,
                 ay=120, ref=(160, 120, 1.0)),
               c("harbor_dock scale 0.6 (+0.6 adult)", lambda x, y: PR.harbor_dock(x - 260, x + 260, y, depth=150,
                                                                                    scale=0.6),
                 w=500, ax=250, ay=200, ref=(140, 200, 0.6)),
               c("signpost (base)", lambda x, y: PR.signpost(x, y, 1.0), w=500, ax=250, ay=400)]),
    ]
    return render_sheet("buildings", "props — buildings (anchor = ground line / bottom centre)", rows)


def sheet_lions():
    s = 0.75

    def c(label, fn, w=400, ax=190, ay=300):
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)])
    rows = [(330, [c(p, lambda x, y, p=p: PR.lion(x, y, s, pose=p)) for p in PR.LION_POSES]),
            (330, [c(f"sit mouth={m} eyes={e}", lambda x, y, m=m, e=e: PR.lion(x, y, s, pose="sit", mouth=m, eyes=e),
                     ax=180) for m, e in ((0.33, "open"), (0.66, "half"), (1.0, "closed"), (0, "happy"))] +
                   [c("facing=-1 tail=1", lambda x, y: PR.lion(x, y, s, -1, tail=1), ax=200),
                    c("walk_a tail=-1", lambda x, y: PR.lion(x, y, s, pose="walk_a", tail=-1))]),
            (300, [c("lioness " + p, lambda x, y, p=p: PR.lion(x, y, s, pose=p, variant=1), ay=270)
                   for p in PR.LION_POSES]),
            (470, [Cell("lion and people at scale 1 (lion, daniel, jonah)", lambda ox, oy: PR.lion(ox + 330, oy + 440, 1.0)
                        + CH.daniel(ox + 640, oy + 440, 1.0, -1) + CH.jonah(ox + 790, oy + 440), 900, [(330, 440)]),
                   Cell("lion 0.8 lie / daniel 0.8 sit_pray / lioness sleep / lion 0.6 sit mouth=1",
                        lambda ox, oy: PR.lion(ox + 130, oy + 440, 0.8, 1, pose="lie")
                        + CH.daniel(ox + 480, oy + 440, 0.8, 1, pose="sit_pray")
                        + PR.lion(ox + 840, oy + 440, 0.8, -1, pose="sleep", variant=1)
                        + PR.lion(ox + 650, oy + 340, 0.6, -1, pose="sit", mouth=1, eyes="closed"), 1100, [])])]
    return render_sheet("lions", "props — lion(): poses, mouth / eyes / tail, lioness (scale 0.75; red cross = anchor)",
                        rows)


def sheet_daniel():
    def den(ox, oy):
        s, ax, ay = 0.62, ox + 520, oy + 110
        fy = ay + PR.DEN_FLOOR_Y * s
        return (PR.lion_den(ax, ay, s, part="back", light=0.6) + PR.lion(ax - 230, fy, 0.6, 1, pose="lie")
                + PR.lion(ax + 260, fy, 0.6, -1, pose="sleep", variant=1) + CH.daniel(ax + 10, fy, s, 1, pose="sit_pray")
                + PR.lion_den(ax, ay, s, part="front") + CH.king(ax - 210, ay, s, 1, pose="call_out", attire="darius")
                + PR.den_stone(ax + 310, ay, s * 0.9, roll=40))

    def outside(ox, oy):
        s, ax, ay = 0.7, ox + 300, oy + 330
        return (f'<rect x="{ox}" y="{oy + 250}" width="760" height="320" fill="{P["sand"]}"/>'
                + PR.lion_den(ax, ay, s, view="outside", part="back")
                + PR.in_den_hole(CH.daniel(ax, ay + 140, s, 1, pose="hold_rope"), ax, ay, s)
                + PR.lion_den(ax, ay, s, view="outside", part="front") + PR.den_stone(ax + 300, ay + 60, s * 0.8, sealed=True))

    def win(op, d=False):
        def f(ox, oy):
            ax, ay = ox + 170, oy + 300
            o = PR.upstairs_window(ax, ay, 0.5, open=op, part="back", glow=0.7 if d else 0)
            if d:
                o += CH.daniel(ax, ay + PR.WINDOW_FLOOR_Y * 0.5, 0.5, -1, pose="kneel_pray")
            return o + PR.upstairs_window(ax, ay, 0.5, open=op, part="front")
        return f

    def c(label, fn, w, ax, ay, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)
    rows = [(580, [Cell("lion_den cutaway: back -> lions, Daniel -> front -> king; den_stone roll=40; light=0.6", den,
                        1100, []),
                   Cell("view='outside' + in_den_hole(daniel hold_rope); den_stone sealed=True", outside, 760, [])]),
            (420, [Cell(f"window open={op}" + (" + daniel" if d else ""), win(op, d), 340, [(170, 300)])
                   for op, d in ((0, False), (0.25, False), (0.5, False), (0.75, False), (1, True))] +
                  [Cell("interior=True", lambda ox, oy: f'<rect x="{ox + 40}" y="{oy + 40}" width="260" '
                        f'height="300" fill="{P["sky_day"]}"/>' + PR.upstairs_window(ox + 170, oy + 300, 0.5, interior=True),
                        340, [(170, 300)])]),
            (520, [c("persian_column 0.5", lambda x, y: PR.persian_column(x, y, 0.5), 300, 150, 500, (150, 500, 0.5)),
                   c("royal_seal x1.5", lambda x, y: PR.royal_seal(x, y, 1.5), 220, 110, 400),
                   c("impression x1.5", lambda x, y: PR.royal_seal(x, y, 1.5, "impression"), 220, 110, 240),
                   c("decree", lambda x, y: PR.decree(x, y), 260, 130, 300),
                   c("cushion / oil_lamp", lambda x, y: PR.cushion(x, y, 0.9) + PR.oil_lamp(x - 30, y - 300, 1.2)
                     + PR.oil_lamp(x + 60, y - 200, 1.2, lit=False), 300, 140, 500),
                   c("food_tray / lyre", lambda x, y: PR.food_tray(x, y) + PR.lyre(x, y - 200), 300, 150, 500),
                   c("couch + king sit_sad (0.7)", lambda x, y: PR.couch(x, y, 0.7) + CH.king(
                       x + 20 * 0.7, y - 85 * 0.7, 0.7, -1, pose="sit_sad", attire="darius", throne=False), 420, 210, 500)])]
    return render_sheet("daniel", "props — Daniel film: den, stone, window, palace things", rows)


def sheet_david_items():
    def c(label, fn, w=300, ax=150, ay=260, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)
    rows = [
        (300, [c(f"sling angle={a}", lambda x, y, a=a: PR.sling(x, y, 1.0, angle=a), 200, 100, 120) for a in (0, 60, 120, 180)]
         + [c("sling released=True angle=110", lambda x, y: PR.sling(x, y, 1.0, angle=110, released=True), 260, 60, 160),
            c("stone seeds 0-4 (x2)", lambda x, y: "".join(PR.stone(x - 100 + 50 * k, y, 2.0, seed=k) for k in range(5)), 300, 150, 200),
            c("five_stones n=5 / n=3 (x2)", lambda x, y: PR.five_stones(x, y - 90, 2.0) + PR.five_stones(x, y + 40, 2.0, n=3), 300, 150, 200),
            c("shepherd_bag stones=0 / 3", lambda x, y: PR.shepherd_bag(x - 70, y, 1.0) + PR.shepherd_bag(x + 70, y, 1.0, stones=3), 320, 160, 260)]),
        (420, [c("staff (+adult)", lambda x, y: PR.staff(x, y), 220, 90, 380, (170, 380, 1.0)),
               c("staff rot=-80 (lying)", lambda x, y: PR.staff(x, y, rot=-84), 340, 40, 380),
               c("bread_basket / handle=False", lambda x, y: PR.bread_basket(x - 80, y) + PR.bread_basket(x + 80, y, handle=False), 340, 170, 380),
               c("harp", lambda x, y: PR.harp(x, y, 1.2), 220, 110, 380),
               c("helmet_bronze crest / saul", lambda x, y: PR.helmet_bronze(x - 80, y) + PR.helmet_bronze(x + 90, y, crest=False, plume=P["royal_light"], circlet=True), 340, 170, 380),
               c("round_shield israel / philistine", lambda x, y: PR.round_shield(x - 60, y - 200) + PR.round_shield(x + 60, y - 200, kind="philistine")
                 + PR.tall_shield(x, y - 40, 0.55, rot=80), 300, 150, 380),
               c("camp_stool (+saul sit stool=False)", lambda x, y: PR.camp_stool(x, y) + CH.king(x, y, 1.0, pose="sit", attire="saul", stool=False), 280, 120, 380)]),
        (260, [c("spear soldier / goliath (scale .5)", lambda x, y: PR.spear(x, y - 140) + PR.spear(x, y - 60, 0.5, kind="goliath"), 520, 260, 200),
               c("sword", lambda x, y: PR.sword(x, y - 60), 300, 150, 200),
               c("day_counter n=7 filled=3.5 pop=.5", lambda x, y: PR.day_counter(x, y - 80, 1.0, n=7, filled=3.5, pop=0.5), 520, 260, 200),
               c("day_counter icons='sun' / 'moon'", lambda x, y: PR.day_counter(x, y - 140, 0.8, n=6, filled=4, icons="sun")
                 + PR.day_counter(x, y - 40, 0.8, n=6, filled=2, icons="moon"), 460, 230, 200)]),
    ]
    return render_sheet("david_items", "props — David film: sling, stones, bag, staff, basket, harp, armour, camp, counter", rows)


def sheet_david_creatures():
    def c(label, fn, w=400, ax=200, ay=330, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)
    rows = [
        (460, [c(f"bear {p}", lambda x, y, p=p: PR.bear(x, y, 0.8, pose=p), 400, 170, 420) for p in PR.BEAR_POSES[:4]]
         + [c("bear run_a / run_b (0.6)", lambda x, y: PR.bear(x - 60, y - 200, 0.6, pose="run_a") + PR.bear(x - 60, y, 0.6, pose="run_b"), 400, 170, 420)]),
        (260, [c(f"sheep v{v} {p}", lambda x, y, v=v, p=p: PR.sheep(x, y, 1.0, variant=v, pose=p), 300, 130, 220)
               for v, p in ((0, "stand"), (1, "graze"), (2, "walk_a"), (3, "bleat"), (0, "walk_b"))]
         + [c("lambs (lamb=True) + david 0.6", lambda x, y: PR.sheep(x - 90, y, 1.0, pose="stand", lamb=True, variant=0)
              + PR.sheep(x + 20, y, 1.0, -1, variant=1, pose="graze", lamb=True) + CH.david(x + 130, y, 0.6), 400, 200, 220)]),
    ]
    return render_sheet("david_creatures", "props — bear (scale 0.8) and sheep variants", rows)


def sheet_david_camp():
    def c(label, fn, w=600, ax=300, ay=430, ref=None):
        ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
        return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)
    rows = [(480, [c("tent side='israel' (+adult)", lambda x, y: PR.tent(x, y), 700, 330, 440, (640, 440, 1.0)),
                   c("tent side='philistine'", lambda x, y: PR.tent(x, y, side="philistine"), 560, 260, 440, (500, 440, 1.0)),
                   c("tent flag=False / facing=-1 (0.5)", lambda x, y: PR.tent(x - 120, y, 0.5, flag=False) + PR.tent(x + 130, y, 0.5, -1, side="philistine", flag=False), 520, 260, 440)]),
            (260, [Cell("brook(x0, x1, y, width=60) phase 0 / 0.5", lambda ox, oy: f'<rect x="{ox}" y="{oy}" width="1780" height="260" fill="{P["grass"]}"/>'
                        + PR.brook(ox + 40, ox + 860, oy + 120, 60) + PR.brook(ox + 920, ox + 1740, oy + 120, 60, phase=0.5), 1780, [])])]
    return render_sheet("david_camp", "props — tents, brook", rows)


def sheet_valley():
    W, Hh = 2200, 820

    def art(ox, oy):
        y = oy + 560
        sky = f'<rect x="{ox}" y="{oy}" width="{W}" height="{Hh}" fill="{P["sky_day"]}"/>'
        pts = PR.valley_points(ox + 40, ox + W - 40, y, 1.0)
        figs = (CH.soldier(pts["israel_camp"][0] + 260, PR.valley_ground(ox + 420, ox + 40, ox + W - 40, y), 0.4, 1, variant=1)
                + CH.goliath(pts["right_edge"][0] + 40, y + 60, 0.5, -1, pose="stride_a")
                + CH.david(pts["left_edge"][0] + 40, y + 60, 0.5, 1, pose="hold_sling", staff=True))
        return sky + PR.valley_elah(ox + 40, ox + W - 40, y, 1.0) + figs

    def ov(ox, oy):
        y = oy + 560
        pts = PR.valley_points(ox + 40, ox + W - 40, y, 1.0)
        return "".join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="9" fill="none" stroke="#3a7bd5" stroke-width="3"/>'
                       for px, py in pts.values())
    rows = [(Hh, [Cell("valley_elah(x0, x1, y, 1.0) + valley_points (blue rings); goliath 0.5 / david 0.5 on the floor", art, W,
                       [], ov)])]
    return render_sheet("valley", "props — valley_elah backdrop (Israel left, Philistines right)", rows)


# ------------------------------------------------------------------ Noah film (Genesis 6-9)
def _c(label, fn, w, ax, ay, ref=None):
    ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
    return Cell(label, lambda ox, oy: fn(ox + ax, oy + ay), w, [(ax, ay)], ov)


def sheet_noah_ark():
    def ark_cell(label, w=1180, k=0.55, ref=True, ax=560, ay=620, bg=None, **kw):
        def art(ox, oy):
            b = bg(ox, oy) if bg else ""
            return b + PR.ark(ox + ax, oy + ay, k, **kw)
        ov = (lambda ox, oy: person_ref(ox + ax + 640 * k, oy + ay, k)) if ref else ""
        return Cell(label, art, w, [(ax, ay)], ov)

    def sea(ox, oy):
        return PR.flood_sea(ox, ox + 1180, oy + 560, phase=0.2, bottom=oy + 680)

    def overlay(ox, oy):
        pts = PR.ark_points(ox + 560, oy + 620, 0.55)
        return (box(*pts["door_box"]) + box(*pts["window_box"], color="#d53a7b") +
                "".join(box(*b, color="#2a9d5c") for b in pts["windows"]) +
                f'<circle cx="{pts["window_stand"][0]:.0f}" cy="{pts["window_stand"][1]:.0f}" r="8" fill="#d53a7b"/>'
                f'<path d="M{pts["ramp_top"][0]:.0f},{pts["ramp_top"][1]:.0f} L{pts["ramp_bottom"][0]:.0f},{pts["ramp_bottom"][1]:.0f}" '
                f'stroke="#3a7bd5" stroke-width="3" stroke-dasharray="10 6"/>')
    rows = [
        (680, [ark_cell("ark() closed, ramp (+adult at 0.55)"),
               Cell("ark door='open' window='open' + ark_points (boxes) + in_ark_door / in_ark_window", lambda ox, oy:
                    PR.ark(ox + 560, oy + 620, 0.55, door=1, window=1)
                    + PR.in_ark_door(PR.animal_pair("zebra", ox + 760, PR.ark_ramp_y(ox + 760, ox + 560, oy + 620, 0.55), 0.55, -1, pose="walk_a"), ox + 560, oy + 620, 0.55)
                    + PR.in_ark_door(PR.ark_animal(ox + 640, oy + 620 - 170 * 0.55, 0.55, -1, kind="rabbit"), ox + 560, oy + 620, 0.55)
                    + PR.in_ark_window(CH.noah(*PR.ark_points(ox + 560, oy + 620, 0.55)["window_stand"], 0.55, 1, pose="release_dove"), ox + 560, oy + 620, 0.55)
                    + PR.dove(ox + 460, oy + 140, 0.55, 1, wing=0.5), 1180, [(560, 620)], overlay)]),
        (680, [ark_cell("floating=True wet=True on flood_sea (anchor = waterline)", bg=sea, floating=True, wet=True, ramp=False, ay=560, ref=False),
               ark_cell("door=0.5 glow=1 lamps=1 (God shuts the door)", door=0.5, glow=1.0, lamps=1.0)]),
        (500, [ark_cell(f"progress={p_}", w=590, k=0.28, ax=290, ay=440, ref=False, progress=p_) for p_ in (0.06, 0.15, 0.3, 0.45)]),
        (500, [ark_cell(f"progress={p_}", w=590, k=0.28, ax=290, ay=440, ref=False, progress=p_) for p_ in (0.6, 0.75, 0.9, 1.0)]),
    ]
    return render_sheet("noah_ark", "props — Noah: the ark (scale 0.55 / 0.28), building progress, door / window / floating", rows)


def sheet_noah_weather():
    def sky(ox, oy, w, h, c):
        return f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" fill="{c}"/>'
    rows = [
        (420, [Cell(f"rain intensity={it} phase=0", lambda ox, oy, it=it: sky(ox, oy, 470, 420, P["storm_sky"]) +
                    PR.rain(0.0, it, ox, oy, ox + 470, oy + 420, seed=1), 470, []) for it in (0.2, 0.5, 1.0)]
         + [Cell("dark_cloud seed 0 / light .6 + flash", lambda ox, oy: sky(ox, oy, 700, 420, P["storm_sky"]) +
                 PR.dark_cloud(ox + 220, oy + 150, 0.6) + PR.dark_cloud(ox + 480, oy + 290, 0.6, seed=2, light=0.6, flash=0.8), 700, [])]),
        (360, [Cell(f"flood_sea storm={st} phase={ph}", lambda ox, oy, st=st, ph=ph: sky(ox, oy, 700, 360, P["sky_day"] if st == 0 else P["storm_sky"]) +
                    PR.flood_sea(ox, ox + 700, oy + 120, phase=ph, bottom=oy + 360, storm=st), 700, [(0, 120)]) for st, ph in ((0, 0), (0, 0.5), (1, 0.25))]),
        (380, [_c(f"puddle splash={sp} ripple={rp}", lambda x, y, sp=sp, rp=rp: PR.puddle(x, y, 1.0, splash=sp, ripple=rp), 350, 175, 300)
               for sp, rp in ((0, 0), (0, 0.5), (0.3, 0.2), (0.6, 0.4), (1.0, 0.6))]
         + [_c("rain drops=True (drip)", lambda x, y: sky(x - 175, y - 300, 350, 380, P["sky_day"]) + PR.rain(0.3, 0.15, x - 175, y - 300, x + 175, y + 80, seed=2), 350, 175, 300)]),
        (560, [_c(f"rainbow progress={pr}", lambda x, y, pr=pr: sky(x - 300, y - 530, 600, 560, P["sky_day"]) + PR.rainbow(x, y, 0.55, progress=pr), 600, 300, 530)
               for pr in (0.2, 0.5, 0.75, 1.0)]),
        (640, [_c("ararat (scale 0.4) + ark 0.1 on ARARAT_LEDGE", lambda x, y: sky(x - 470, y - 640, 940, 640, P["sky_day"]) + PR.ararat(x, y, 0.4)
                  + PR.ark(x, y + PR.ARARAT_LEDGE[1] * 0.4, 0.1, wet=True, ramp=False), 940, 470, 620),
               _c("ararat green=1 snow / flood_sea covering", lambda x, y: sky(x - 470, y - 640, 940, 640, P["sky_day"]) + PR.ararat(x, y, 0.4, green=1.0)
                  + PR.flood_sea(x - 470, x + 470, y - 330, phase=0.3, bottom=y + 20), 940, 470, 620)]),
    ]
    return render_sheet("noah_weather", "props — Noah: rain, clouds, flood_sea, puddle, rainbow, Mount Ararat", rows)


def sheet_noah_items():
    rows = [
        (300, [_c("saw / hammer", lambda x, y: PR.saw(x - 60, y - 160) + PR.hammer(x - 40, y - 60), 300, 120, 260),
               _c("plank / timber_pile planks", lambda x, y: PR.plank(x, y - 200) + PR.timber_pile(x - 20, y, 0.9, kind="planks"), 360, 170, 260),
               _c("timber_pile mixed / logs", lambda x, y: PR.timber_pile(x - 80, y, 0.75) + PR.timber_pile(x + 110, y, 0.6, kind="logs"), 360, 160, 260),
               _c("sawhorse plank=True", lambda x, y: PR.sawhorse(x, y), 360, 170, 260),
               _c("nails box / loose", lambda x, y: PR.nails(x - 50, y) + PR.nails(x + 90, y, box=False), 300, 120, 260),
               _c("pitch_bucket", lambda x, y: PR.pitch_bucket(x, y), 220, 100, 260)]),
        (300, [_c(f"food_basket {k}", lambda x, y, k=k: PR.food_basket(x, y, kind=k), 230, 115, 260) for k in ("fruit", "grain", "veg", "bread")]
         + [_c("sack / jar (existing)", lambda x, y: PR.sack(x - 50, y) + PR.jar(x + 60, y - 82), 260, 120, 260),
            _c("hay bale / bundle / pile", lambda x, y: PR.hay(x - 150, y, 0.8) + PR.hay(x + 30, y - 120, 0.8, kind="bundle") + PR.hay(x + 100, y, 0.8, kind="pile"), 420, 220, 260)]),
        (360, [_c(f"altar fire={f} phase={ph}", lambda x, y, f=f, ph=ph: PR.altar(x, y, fire=f, phase=ph), 280, 140, 330) for f, ph in ((1, 0), (1, 0.33), (1, 0.66), (0, 0))]
         + [_c("olive_branch / olive_leaf (x2)", lambda x, y: PR.olive_branch(x - 120, y - 140, 1.4) + PR.olive_leaf(x - 60, y - 40, 2.0), 300, 150, 330),
            _c("dove leaf=True (x1.4)", lambda x, y: PR.dove(x, y - 200, 1.4, wing=0.5, leaf=True) + PR.dove(x, y - 60, 1.4, pose="stand", leaf=True), 280, 140, 330)]),
        (380, [_c("football_field (scale 0.7)", lambda x, y: PR.football_field(x, y, 0.7), 760, 380, 340),
               _c("football_field 0.42 vs ark (FOOTBALL_LEN x 1.37)", lambda x, y: PR.football_field(x, y, 0.42)
                  + PR.ark(x - 30, y - 140, 0.42 * 1.37 * PR.FOOTBALL_LEN / PR.ARK_LEN, ramp=False), 760, 380, 340)]),
    ]
    return render_sheet("noah_items", "props — Noah: tools, timber, food, altar, olive, football pitch", rows)


def sheet_noah_animals():
    def c(kind, pose, female=False, w=300, ax=150, ay=440, k=0.62, phase=0.0, ref=False):
        lab = f"{kind} {pose}" + (" female" if female else "") + (f" ph={phase}" if pose == "hop" else "")
        return _c(lab, lambda x, y: PR.ark_animal(x, y, k, kind=kind, pose=pose, female=female, phase=phase), w, ax, ay,
                  (w - 40, ay, k) if ref else None)
    rows = [
        (480, [c("elephant", p, f, w=330, ax=140) for p, f in (("stand", False), ("stand", True), ("walk_a", False), ("walk_b", False),
                                                              ("trunk_up", False), ("spray", True))]
         + [c("giraffe", "stand", False, w=260, ax=100, ref=True)]),
        (480, [c("giraffe", p, f, w=300, ax=110) for p, f in (("stand", True), ("walk_a", False), ("walk_b", False), ("bow", False))]
         + [c("elephant", "sleep", False, w=330, ax=150), c("elephant", "sleep", True, w=330, ax=150)]),
        (300, [c(kd, p, f, w=290, ax=130, ay=270) for kd in ("zebra", "horse", "deer") for p, f in (("stand", False), ("stand", True))]
         + []),
        (300, [c(kd, p, False, w=290, ax=130, ay=270) for kd in ("zebra", "horse", "deer") for p in ("walk_a", "walk_b")]),
        (220, [c("rabbit", "stand", f, w=170, ax=80, ay=190, k=1.0) for f in (False, True)]
         + [c("rabbit", "hop", False, w=200, ax=90, ay=190, k=1.0, phase=ph) for ph in (0, 0.25, 0.5, 0.75)]
         + [c("rabbit", "sleep", True, w=200, ax=90, ay=190, k=1.0)]
         + [c("turtle", p, f, w=220, ax=100, ay=190, k=1.0) for p, f in (("stand", False), ("walk_a", True), ("walk_b", False))]),
        (220, [c("duck", p, f, w=170, ax=70, ay=190, k=1.0) for p, f in (("stand", False), ("stand", True), ("walk_a", False), ("walk_b", True), ("swim", False))]
         + [c("monkey", p, f, w=170, ax=90, ay=200, k=0.9) for p, f in (("stand", False), ("stand", True), ("walk_a", False), ("walk_b", False), ("wave", True), ("sit", False))]),
        (260, [c("hippo", p, f, w=300, ax=120, ay=230, k=0.7) for p, f in (("stand", False), ("stand", True), ("walk_a", False), ("yawn", False))]
         + [c("fox", p, f, w=220, ax=115, ay=230, k=0.9) for p, f in (("stand", False), ("stand", True), ("walk_a", False), ("sit", False), ("sleep", True))]),
        (200, [_c(f"butterfly flap={fl}", lambda x, y, fl=fl, col=col: PR.butterfly(x, y - 80, 1.4, flap=fl, color=col), 170, 85, 180)
               for fl, col in ((0, "orange"), (0.25, "blue"), (0.5, "yellow"), (0.75, "pink"))]
         + [_c(f"songbird {col} wing={wg}", lambda x, y, col=col, wg=wg: PR.songbird(x, y - 90, 1.6, wing=wg, color=col), 200, 100, 180)
            for col, wg in (("blue", 1), ("red", 0), ("yellow", -1), ("green", 0.5))]
         + [_c("songbird perch / female", lambda x, y: PR.songbird(x - 40, y - 80, 1.6, pose="perch") + PR.songbird(x + 50, y - 80, 1.6, pose="perch", female=True), 230, 115, 180)]),
    ]
    return render_sheet("noah_animals", "props — Noah: ark_animal kinds x poses (female=True: bow + lashes, smaller)", rows)


def sheet_noah_pairs():
    def c(kind, pose="walk_a", w=400, ax=170, ay=380, k=0.5):
        return _c(f"{kind} {pose}", lambda x, y: PR.animal_pair(kind, x, y, k, pose=pose), w, ax, ay)
    kinds = list(PR.PAIR_KINDS)
    rows = []
    row = []
    for kd in kinds:
        big = kd in ("elephant", "giraffe", "camel", "hippo", "lion")
        row.append(c(kd, "walk_a" if kd not in ("rabbit",) else "hop", w=440 if big else 300, ax=170 if big else 120,
                     ay=380, k=0.5 if kd != "giraffe" else 0.45))
        if sum(cc.w for cc in row) > 1900:
            rows.append((420, row))
            row = []
    if row:
        rows.append((420, row))
    return render_sheet("noah_pairs", "props — Noah: animal_pair(kind, ...) two by two (scale 0.5; anchor = the near animal)", rows)


def sheet_joseph_items():
    def c(label, fn, w=300, ax=150, ay=330, ref=None):
        return _c(label, fn, w, ax, ay, (w - 40, ay, ref) if ref else None)
    rows = [
        (380, [c(f"held progress={pr:.2f}", lambda x, y, pr=pr: PR.coat_of_colours(x, y - 300, 1.0, progress=pr), 250, 125)
               for pr in (0, 1 / 6, 2 / 6, 4 / 6, 1.0)]
         + [c("held torn dirty", lambda x, y: PR.coat_of_colours(x, y - 300, 1.0, torn=True, dirty=True), 250, 125),
            c("lying", lambda x, y: PR.coat_of_colours(x, y, 1.0, state="lying"), 330, 165),
            c("lying torn dirty", lambda x, y: PR.coat_of_colours(x, y, 1.0, state="lying", torn=True, dirty=True), 330, 165)]),
        (300, [c("folded", lambda x, y: PR.coat_of_colours(x, y - 60, 1.0, state="folded"), 230, 115, 290),
               c("bundle torn dirty", lambda x, y: PR.coat_of_colours(x, y - 120, 1.0, state="bundle", torn=True, dirty=True), 260, 130, 290)]
         + [c(f"sheaf bow={b}", lambda x, y, b=b: PR.wheat_sheaf(x, y, 1.0, bow=b), 210, 90, 290) for b in (0, 0.5, 1.0)]
         + [c("sheaf glow=1", lambda x, y: PR.wheat_sheaf(x, y, 1.0, glow=1.0), 250, 125, 290),
            c("sheaf rise=.5", lambda x, y: PR.wheat_sheaf(x, y, 1.0, rise=0.5), 260, 150, 290),
            c("kind='bundle'", lambda x, y: PR.wheat_sheaf(x, y, 1.0, kind="bundle"), 280, 150, 290),
            c("ripe=0 (green)", lambda x, y: PR.wheat_sheaf(x, y, 1.0, ripe=0.0), 200, 100, 290)]),
        (240, [c(f"coins n={n} {k}", lambda x, y, n=n, k=k: PR.coins(x, y, 1.0, n=n, kind=k), 330, 165, 200)
               for n, k in ((20, "pile"), (20, "row"), (15, "stacks"), (5, "pouch"))]
         + [c("signet_ring", lambda x, y: PR.signet_ring(x, y - 60, 1.0), 170, 85, 200),
            c("gold_chain held / lying", lambda x, y: PR.gold_chain(x - 50, y - 190, 0.8) + PR.gold_chain(x + 60, y - 30, 0.8, state="lying"), 280, 140, 200),
            c("toy horse / ball", lambda x, y: PR.toy(x - 60, y, 1.0) + PR.toy(x + 80, y, 1.0, kind="ball"), 260, 120, 200)]),
        (330, [c(f"grapevine grow={g}", lambda x, y, g=g: PR.grapevine(x, y, 1.0, grow=g), 230, 115, 300)
               for g in (0.2, 0.45, 0.65, 0.85, 1.0)]
         + [c(f"bread_baskets birds={b}", lambda x, y, b=b: PR.bread_baskets(x, y - 30, 1.0, birds=b), 230, 115, 300) for b in (0, 3)]
         + [c("grain_sacks n=1 open / n=6", lambda x, y: PR.grain_sacks(x - 70, y, 0.9, n=1, open_=True) + PR.grain_sacks(x + 90, y, 0.6, n=6), 300, 150, 300)]),
    ]
    return render_sheet("joseph_items", "props — Joseph: coat, sheaves, coins, ring, chain, toy, dream vine and baskets, sacks", rows)


def sheet_joseph_animals():
    def c(label, fn, w=420, ax=170, ay=400, ref=False):
        return _c(label, fn, w, ax, ay, (w - 40, ay, 1.0) if ref else None)
    rows = [
        (420, [c(f"camel walk phase={ph}", lambda x, y, ph=ph: PR.camel(x, y, 1.0, pose="walk", phase=ph), 440, 160) for ph in (0, 0.25, 0.5, 0.75)]
         + [c("camel stand load=False", lambda x, y: PR.camel(x, y, 1.0, load=False, bridle=False), 440, 160)]),
        (320, [c(f"donkey walk phase={ph}", lambda x, y, ph=ph: PR.donkey(x, y, 1.0, pose="walk", phase=ph), 330, 130, 300) for ph in (0, 0.25, 0.5, 0.75)]
         + [c("donkey sacks=0", lambda x, y: PR.donkey(x, y, 1.0, sacks=0), 330, 130, 300), c("animal('donkey') (old)", lambda x, y: PR.animal(x, y, 1.0, kind="donkey"), 330, 130, 300)]),
        (300, [c(f"cow fat {p}", lambda x, y, p=p: PR.cow(x, y, 1.0, pose=p), 360, 160, 280) for p in ("stand", "walk_a", "walk_b", "graze")]
         + [c(f"cow thin {p}", lambda x, y, p=p: PR.cow(x, y, 1.0, kind="thin", pose=p, mouth=0.8 if p == "stand" else 0.0), 330, 140, 280) for p in ("stand", "walk_a")]),
        (420, [c(f"chariot wheel={w} phase={ph}", lambda x, y, w=w, ph=ph: PR.chariot(x, y, 0.62, wheel=w, phase=ph), 560, 90, 400) for w, ph in ((0, 0), (0.5, 0.5))]
         + [c("chariot back + ride (seated) + front", lambda x, y: PR.chariot(x, y, 0.62, part="back") + CH.joseph(
             *PR.local_to_stage(x, y, 0.62, 1, *PR.CHARIOT_SEAT), 0.62, attire="ruler", pose="ride") + PR.chariot(x, y, 0.62, part="front"), 560, 90, 400),
            c("cow thin graze", lambda x, y: PR.cow(x, y, 1.0, kind="thin", pose="graze"), 330, 140, 400)]),
    ]
    return render_sheet("joseph_animals", "props — Joseph: camel and donkey walk cycles, fat / thin cows, the chariot", rows)


def sheet_joseph_egypt():
    def c(label, fn, w=600, ax=300, ay=560, ref=None):
        return _c(label, fn, w, ax, ay, (w - 60, ay, ref) if ref else None)

    def sky(fn):
        return lambda x, y: f'<rect x="{x - 400}" y="{y - 600}" width="1200" height="620" fill="{P["sky_day"]}"/>' + fn(x, y)
    rows = [
        (600, [c("pyramids (n=3) scale 0.6 / haze=.6 behind", sky(lambda x, y: PR.pyramids(x + 120, y - 120, 0.45, haze=0.6) + PR.pyramids(x, y, 0.6)), 760, 380),
               c("egypt_house v0 (scale 0.7)", lambda x, y: PR.egypt_house(x, y, 0.7), 520, 260, 560, 0.7),
               c("egypt_house v1 villa (scale 0.55)", lambda x, y: PR.egypt_house(x, y, 0.55, variant=1), 560, 280, 560, 0.55),
               c("egypt_column", lambda x, y: PR.egypt_column(x, y, 1.0) + PR.palm_tree(x + 150, y, 0.9), 400, 120, 560, 1.0)]),
        (520, [c(f"granary fill={f}", lambda x, y, f=f: PR.granary(x, y, 0.55, fill=f), 520, 260, 480, 0.55) for f in (0, 0.35, 0.7, 1.0)]),
        (520, [c("egypt_throne + pharaoh(throne=False)", lambda x, y: PR.egypt_throne(x, y, 1.0) + CH.pharaoh(x, y, 1.0, pose="sit_throne", throne=False), 400, 180, 480),
               c("prison_window light=1", lambda x, y: PR.prison_window(x, y - 300, 0.9), 520, 260, 480),
               c("prison_bars open_=0 / .6", lambda x, y: PR.prison_bars(x - 110, y, 0.6) + PR.prison_bars(x + 130, y, 0.6, open_=0.6), 480, 240, 480, 0.6),
               c("pit outside (rope=.6) / cutaway", lambda x, y: PR.pit(x - 120, y - 300, 0.7, rope=0.6) + PR.pit(x + 220, y - 380, 0.45, view="cutaway", rope=0.8), 620, 300, 480)]),
        (340, [Cell("nile(x0, x1, y, width=150, phase) + papyrus + field(ripe) / field(dry=1)", lambda ox, oy: (
            PR.nile(ox + 20, ox + 1100, oy + 150, 150, 1.0, phase=0.3) + PR.field(ox + 1140, ox + 1640, oy + 160, 120)
            + PR.field(ox + 1680, ox + 2200, oy + 160, 120, dry=1.0)), 2220, [(20, 150)])]),
        (520, [Cell("dream_bubble(... inner=7 fat cows, tail toward a sleeper) | inner=sheaves bowing", lambda ox, oy: (
            CH.pharaoh(ox + 160, oy + 500, 0.6, pose="sleep") +
            PR.dream_bubble(ox + 560, oy + 230, 640, 380, tail=(ox + 180, oy + 420),
                            inner=PR.nile(ox + 200, ox + 900, oy + 380, 80, 0.6) + "".join(
                                PR.cow(ox + 330 + i * 110, oy + 330 + (i % 2) * 22, 0.42, pose="walk", phase=i * 0.3) for i in range(4))) +
            PR.dream_bubble(ox + 1500, oy + 250, 600, 400, tail=(ox + 1150, oy + 470), inner=
                            PR.field(ox + 1200, ox + 1800, oy + 380, 80) + PR.wheat_sheaf(ox + 1500, oy + 390, 0.8, glow=1.0) +
                            "".join(PR.wheat_sheaf(ox + 1500 + dx, oy + 400 + abs(dx) * 0.05, 0.6, -1 if dx > 0 else 1, bow=0.9)
                                    for dx in (-220, -130, 130, 220)))), 2220, [])]),
    ]
    return render_sheet("joseph_egypt", "props — Joseph: Egypt (pyramids, houses, column, granary fill, throne, prison, pit, Nile, fields, dream bubbles)", rows)


# ------------------------------------------------------------------ Storm film (Mark 4:35-41)
def _sky(ox, oy, w, h, col):
    return f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" fill="{col}"/>'


def _boat_marks(x, y, k, f=1):
    """Overlay: the documented boat points (blue = near floor / seats, green = far floor, red = Jesus, orange = cling /
    wake, purple = oarlocks)."""
    pts = PR.boat_points(x, y, k, f)
    out = ""
    for key, col in (("stand", "#3a7bd5"), ("seats", "#3a7bd5"), ("far_stand", "#2a9d5c"), ("far_seats", "#2a9d5c"),
                     ("oarlocks", "#8a3ad5")):
        for px, py in pts[key]:
            out += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="{col}" opacity="0.85"/>'
    for key, col in (("sleep", "#d53a3a"), ("stern_seat", "#d53a3a"), ("stern_cushion", "#d53a3a"), ("cling", "#e08a2a"),
                     ("wake", "#e08a2a"), ("mast_top", "#8a3ad5")):
        px, py = pts[key]
        out += f'<rect x="{px - 7:.0f}" y="{py - 7:.0f}" width="14" height="14" fill="{col}" opacity="0.85"/>'
    return out


def _storm_crew(x, y, k, f=1, mode="calm", phase=0.0):
    """Boat back + 13 people + boat front (see characters_storm_group for more)."""
    pts = PR.boat_points(x, y, k, f)
    storm = mode == "storm"
    out = PR.fishing_boat(x, y, k, f, part="back", sail="flapping" if storm else "full", phase=phase,
                          oars="out" if mode == "row" else "in", row=phase)
    for i, (px, py) in enumerate(pts["far_stand"]):
        out += CH.disciples(px, py, k, f if i % 2 else -f, variant=4 + i, pose="scared" if storm else "stand",
                            shake=0.25 * i, wet=storm)
    out += CH.jesus(*pts["sleep"], k, f, pose="sleep", glow=0.7 if storm else 0.0, marks=storm)
    if mode == "row":
        for (sx, sy), v in zip(pts["seats"], (1, 2)):
            out += CH.disciples(sx, sy, k, -f, variant=v, pose="row", phase=phase)
    for i, (px, py) in enumerate(pts["stand"]):
        if mode == "row" and i in (0, 2):
            continue
        v = (0, 3, 10, 11, 9, 2)[i]
        pose = ("bail", "bail", "pull_rope", "cling", "bail", "shout")[i] if storm else ("stand", "point")[i == 3]
        if pose == "cling":
            px, py = pts["cling"]
        out += CH.disciples(px, py, k, f if (pose == "cling" or i >= 3) else -f, variant=v, pose=pose,
                            phase=(phase + 0.3 * i) % 1, wet=storm, wind=1.0 if storm else 0.0)
    out += PR.fishing_boat(x, y, k, f, part="front", oars="out" if mode == "row" else "in", row=phase,
                           water=0.55 if storm else 0.0, wet=storm, lantern=storm)
    return out


def sheet_storm_boat():
    rows = [
        (640, [Cell("fishing_boat() sail=full (scale 0.55) + boat_points overlay + adult ref", lambda ox, oy: _sky(ox, oy, 1100, 640, P["sky_day"]) +
                    PR.fishing_boat(ox + 560, oy + 560, 0.55), 1100, [(560, 560)],
                    lambda ox, oy: _boat_marks(ox + 560, oy + 560, 0.55) + person_ref(ox + 860, oy + 560, 0.55)),
               Cell("sail=flapping phase .3, water=.6, wet, lantern, oars='none'", lambda ox, oy: _sky(ox, oy, 1100, 640, "#5a6c82") +
                    PR.fishing_boat(ox + 560, oy + 560, 0.55, sail="flapping", phase=0.3, water=0.6, wet=True, lantern=True,
                                    oars="none"), 1100, [(560, 560)])]),
        (640, [Cell("the crew rowing out (oars='out', row=.25; disciples row at 'seats', facing -1); Jesus asleep at 'sleep'",
                    lambda ox, oy: _sky(ox, oy, 1100, 640, "#e8b98a") + _storm_crew(ox + 560, oy + 560, 0.55, 1, "row", 0.25), 1100, [(560, 560)]),
               Cell("the crew in the storm: bail, cling at 'cling', pull_rope, scared; water .55", lambda ox, oy: _sky(ox, oy, 1100, 640, "#5a6c82") +
                    _storm_crew(ox + 560, oy + 560, 0.55, 1, "storm", 0.6), 1100, [(560, 560)])]),
        (500, [Cell(f"sail='{sl}' phase={ph} facing={fc}", lambda ox, oy, sl=sl, ph=ph, fc=fc: _sky(ox, oy, 733, 500, P["sky_day"]) +
                    PR.fishing_boat(ox + 366, oy + 440, 0.42, fc, sail=sl, phase=ph, oars="out" if sl == "furled" else "in", row=0.75),
                    733, [(366, 440)]) for sl, ph, fc in (("furled", 0, -1), ("flapping", 0.6, 1), ("none", 0, 1))]),
        (420, [Cell(f"water={w}", lambda ox, oy, w=w: _sky(ox, oy, 733, 420, "#5a6c82") + PR.fishing_boat(ox + 366, oy + 360, 0.42,
                    sail="none", water=w, wet=w > 0, oars="none", nets=False), 733, [(366, 360)]) for w in (0.2, 0.5, 0.9)]),
        (500, [Cell("boat_rock(crew, tilt=7, bob=10)", lambda ox, oy: _sky(ox, oy, 733, 500, P["sky_day"]) +
                    PR.boat_rock(_storm_crew(ox + 366, oy + 420, 0.42), ox + 366, oy + 420, 7, 10, 0.42), 733, [(366, 420)]),
               Cell("fishing_boat(tilt=-6) alone", lambda ox, oy: _sky(ox, oy, 733, 500, P["sky_day"]) +
                    PR.fishing_boat(ox + 366, oy + 420, 0.42, sail="full", tilt=-6), 733, [(366, 420)]),
               Cell("part='back' only / part='front' only", lambda ox, oy: _sky(ox, oy, 733, 500, P["sky_day"]) +
                    PR.fishing_boat(ox + 200, oy + 420, 0.24, part="back") + PR.fishing_boat(ox + 540, oy + 420, 0.24, part="front"),
                    733, [(200, 420), (540, 420)])]),
    ]
    return render_sheet("storm_boat", "props — Storm: the fishing boat (sails, oars, rowing, water inside, rocking, parts, boat_points)", rows)


def sheet_storm_lake():
    rows = [
        (560, [Cell(f"lake_galilee(time='{t}') scale 0.5 (anchor y = the near shoreline)", lambda ox, oy, t=t: PR.lake_galilee(
            ox, ox + 1100, oy + 380, 0.5, time=t, top=oy, bottom=oy + 560), 1100, [(0, 380)]) for t in ("day", "sunset")]),
        (560, [Cell("time='dawn' shore='far' village='right' (the arrival)", lambda ox, oy: PR.lake_galilee(
            ox, ox + 1100, oy + 380, 0.5, time="dawn", shore="far", village="right", top=oy, bottom=oy + 560), 1100, [(0, 380)]),
               Cell("time='night' village='right' + night_sky over it", lambda ox, oy: PR.lake_galilee(
                   ox, ox + 1100, oy + 380, 0.5, time="night", village="right", top=oy, bottom=oy + 560)
                   + PR.night_sky(ox, oy, ox + 1100, oy + 255, moon=(ox + 850, oy + 90), stars=40, progress=1.0), 1100, [(0, 380)])]),
        (560, [Cell("lake 'back' + boat + lake_band (hides the hull) + 'shore' + villager_crowd(sit_listen)", lambda ox, oy:
                    PR.lake_galilee(ox, ox + 1100, oy + 380, 0.5, time="day", part="back", top=oy, bottom=oy + 560)
                    + PR.fishing_boat(ox + 760, oy + 330, 0.3, sail="furled")
                    + CH.jesus(*PR.boat_points(ox + 760, oy + 330, 0.3)["stern_seat"], 0.3, -1, pose="teach")
                    + PR.fishing_boat(ox + 760, oy + 330, 0.3, part="front", sail="furled")
                    + PR.lake_band(ox, ox + 1100, oy + 330 - 4 * 0.3, oy + 385, "day", scale=0.5)
                    + PR.lake_galilee(ox, ox + 1100, oy + 380, 0.5, time="day", part="shore", village="left", top=oy, bottom=oy + 560)
                    + CH.villager_crowd(ox + 600, oy + 520, 0.42, -1, n=14, pose="sit_listen", width=900, rows=3), 1100, [(0, 380)]),
               Cell("sunset: the crowd going home, waving (villager walk / wave)", lambda ox, oy:
                    PR.lake_galilee(ox, ox + 1100, oy + 380, 0.5, time="sunset", top=oy, bottom=oy + 560)
                    + CH.villager_crowd(ox + 300, oy + 520, 0.42, -1, n=7, pose="walk_a", width=420, rows=2, seed=2)
                    + CH.villager_crowd(ox + 800, oy + 530, 0.42, 1, n=6, pose="wave", width=360, rows=2, seed=5), 1100, [(0, 380)])]),
    ]
    return render_sheet("storm_lake", "props — Storm: lake_galilee day / sunset / dawn (far shore) / night, parts, crowds", rows)


def sheet_storm_weather():
    rows = [
        (600, [Cell("storm_sky(rain=.6, lightning=.5) + storm_lake back / boat_rock(crew) / front (STORM_BOAT_DY)", lambda ox, oy:
                    PR.storm_sky(ox, oy, ox + 1100, oy + 600, phase=0.2, rain=0.6, lightning=0.5, scale=0.7)
                    + PR.storm_lake(ox, ox + 1100, oy + 330, phase=0.2, part="back", bottom=oy + 600, scale=0.6)
                    + PR.boat_rock(_storm_crew(ox + 560, oy + 330 + PR.STORM_BOAT_DY * 0.6, 0.42, 1, "storm", 0.4),
                                   ox + 560, oy + 330 + PR.STORM_BOAT_DY * 0.6, -6, 0, 0.42)
                    + PR.storm_lake(ox, ox + 1100, oy + 330, phase=0.2, part="front", bottom=oy + 600, scale=0.6), 1100, [(0, 330)]),
               Cell("the calm: night_sky(moon, clouds .4, stars) + calm_lake(moon_x) + the boat", lambda ox, oy:
                    PR.night_sky(ox, oy, ox + 1100, oy + 330, moon=(ox + 780, oy + 110), stars=50, progress=0.8, clouds=0.4)
                    + PR.calm_lake(ox, ox + 1100, oy + 330, moon_x=ox + 780, bottom=oy + 600, scale=0.7)
                    + _storm_crew(ox + 440, oy + 500, 0.4, 1, "calm"), 1100, [(0, 330)])]),
        (420, [Cell(f"storm_lake wave={wv} phase={ph}", lambda ox, oy, wv=wv, ph=ph: _sky(ox, oy, 550, 420, "#3e4c61")
                    + PR.storm_lake(ox, ox + 550, oy + 170, phase=ph, wave=wv, bottom=oy + 420, scale=0.55), 550, [(0, 170)])
               for wv, ph in ((1.0, 0.0), (1.0, 0.25), (0.5, 0.0), (0.1, 0.0))]),
        (420, [Cell(f"storm_sky phase={ph} density={dn}", lambda ox, oy, ph=ph, dn=dn, mo=mo: PR.storm_sky(
            ox, oy, ox + 550, oy + 420, phase=ph, density=dn, moon=mo, scale=0.6), 550, [])
               for ph, dn, mo in ((0.0, 1.0, None), (0.5, 1.0, None), (0.0, 0.4, (400, 120)), (0.0, 0.0, None))]),
        (420, [Cell("night_sky time='dusk' progress=.3", lambda ox, oy: PR.night_sky(ox, oy, ox + 550, oy + 420, stars=40, progress=0.3, time="dusk"), 550, []),
               Cell("night_sky progress=.6 twinkle=.5", lambda ox, oy: PR.night_sky(ox, oy, ox + 550, oy + 420, moon=(ox + 400, oy + 110), stars=50, progress=0.6, twinkle=0.5), 550, []),
               Cell("calm_lake time='dawn' (sun path)", lambda ox, oy: PR.calm_lake(ox, ox + 550, oy + 40, moon_x=ox + 275, time="dawn", bottom=oy + 420, scale=0.7), 550, [(0, 40)]),
               Cell("calm_lake night, glow=.4, phase .5", lambda ox, oy: PR.calm_lake(ox, ox + 550, oy + 40, moon_x=ox + 300, phase=0.5, glow=0.4, bottom=oy + 420, scale=0.7), 550, [(0, 40)])]),
    ]
    return render_sheet("storm_weather", "props — Storm: the storm (sky, lake, rocking boat) and the calm (night sky, moonlit lake)", rows)


def sheet_storm_items():
    def c(label, fn, w=300, ax=150, ay=330, ref=None):
        return _c(label, fn, w, ax, ay, (w - 40, ay, ref) if ref else None)
    night = "#2e3560"
    rows = [
        (300, [c(f"hanging_lantern swing={sw}", lambda x, y, sw=sw: _sky(x - 120, y - 280, 240, 300, night) + PR.hanging_lantern(x, y - 250, 1.5, swing=sw), 240, 120, 280)
               for sw in (-1, 0, 1)]
         + [c("unlit", lambda x, y: PR.hanging_lantern(x, y - 250, 1.5, lit=False), 140, 70, 280)]
         + [c(f"bail_bucket {k} tip={t}", lambda x, y, k=k, t=t: PR.bail_bucket(x - 40, y, 1.6, kind=k, tip=t), 250, 125, 280)
            for k, t in (("bucket", 0), ("bowl", 0), ("bucket", 1))]
         + [c("boat_cushion / pillow / rope_spiral", lambda x, y: PR.boat_cushion(x - 140, y, 1.0) + PR.pillow(x + 20, y - 60, 0.6) + PR.rope_spiral(x + 150, y), 460, 230, 280)]),
        (320, [c("fishing_net pile", lambda x, y: PR.fishing_net(x, y, 0.9), 260, 130, 300),
               c("fishing_net pole", lambda x, y: PR.fishing_net(x, y, 0.8, kind="pole"), 330, 165, 300),
               c("net_full phase 0 / .5", lambda x, y: PR.net_full(x - 90, y - 230, 1.0) + PR.net_full(x + 90, y - 230, 1.0, phase=0.5), 380, 190, 300),
               c("fishing_net cast spread .3 / 1", lambda x, y: PR.fishing_net(x - 150, y - 220, 0.6, kind="cast", spread=0.3) + PR.fishing_net(x + 120, y - 160, 0.6, kind="cast", spread=1.0), 520, 260, 300),
               c("lake_fish flap -1 / 0 / 1", lambda x, y: "".join(PR.lake_fish(x - 110 + 110 * i, y - 120 - 20 * i, 1.3, 1 if i % 2 else -1, flap=i - 1, rot=-20 + 20 * i) for i in range(3)), 380, 190, 300)]),
        (300, [c(f"small_boat variant={v}", lambda x, y, v=v: PR.small_boat(x, y - 60, 0.55, variant=v, lantern=v == 3), 300, 150, 280) for v in range(4)]
         + [c("sail='full' time='sunset'", lambda x, y: PR.small_boat(x, y - 60, 0.55, sail="full", time="sunset"), 300, 150, 280),
            c("stone_house variant 0 / 1 / 2 (0.3), time='night' lit", lambda x, y: "".join(PR.stone_house(x - 230 + 210 * i, y, 0.3, variant=i, time="night" if i == 2 else "day") for i in range(3)), 640, 320, 280)]),
        (620, [c(f"window_wind wind={w} rattle={r}", lambda x, y, w=w, r=r, n=n, gl=gl: _sky(x - 280, y - 600, 560, 620, "#d9c8ae")
                 + PR.window_wind(x, y - 90, 0.9, wind=w, phase=0.3, rattle=r, night=n, glow=gl), 560, 280, 600)
               for w, r, n, gl in ((1.0, 1.0, True, 0.0), (0.3, 0.0, True, 0.8))]
         + [c("bed + child sit_hug at BED_TOP", lambda x, y: PR.bed(x, y, 0.9) + CH.child(x - 40, y + PR.BED_TOP * 0.9, 0.9, pose="sit_hug", outfit="pyjamas"), 620, 310, 600),
            c("lake_map (scale .6), phase .3", lambda x, y: PR.lake_map(x, y - 260, 0.6, phase=0.3), 580, 290, 600)]),
    ]
    return render_sheet("storm_items", "props — Storm: lantern, buckets, cushion, pillow, rope, nets, fish, small boats, houses, window, bed, map", rows)


def sheet_storm_story():
    def c(label, fn, w=300, ax=150, ay=330, ref=None):
        return _c(label, fn, w, ax, ay, (w - 40, ay, ref) if ref else None)
    rows = [
        (330, [c(f"growth={g}", lambda x, y, g=g: PR.mustard_plant(x, y, 1.0, growth=g), 230, 115, 310)
               for g in (0.0, 0.1, 0.2, 0.3, 0.45)]
         + [c("mustard_seed (hand) sparkle=1", lambda x, y: PR.mustard_seed(x + 30, y - 150, 0.9), 360, 180, 310),
            c("nest build .3 / eggs 3 / chicks 3", lambda x, y: PR.nest(x - 150, y - 40, 1.2, build=0.3) + PR.nest(x, y - 40, 1.2, eggs=3) + PR.nest(x + 150, y - 40, 1.2, chicks=3), 500, 250, 310)]),
        (640, [c(f"growth={g} (scale 0.6)", lambda x, y, g=g: PR.mustard_plant(x, y, 0.6, growth=g), 430, 215, 610, 0.6)
               for g in (0.6, 0.8)]
         + [c("growth=1 + nests at MUSTARD_NESTS + songbirds", lambda x, y: PR.mustard_plant(x, y, 0.6, growth=1.0)
              + "".join(PR.nest(x + nx * 0.6, y + ny * 0.6, 0.5, chicks=2 if i % 2 else 0, eggs=0 if i % 2 else 2) for i, (nx, ny) in enumerate(PR.MUSTARD_NESTS))
              + PR.songbird(x - 200, y - 500, 0.6, 1, wing=0.5, color="yellow") + PR.songbird(x + 170, y - 420, 0.6, -1, pose="perch", color="red"), 600, 300, 610, 0.6),
            c("sway=1", lambda x, y: PR.mustard_plant(x, y, 0.45, growth=1.0, sway=1.0), 420, 210, 610)]),
    ]
    return render_sheet("storm_story", "props — Storm: the mustard seed (Mark 4:30-32): growth, the seed in a hand, nests", rows)


# ------------------------------------------------------------------ Nativity film
NIGHT = "#1c2c5c"


def _nat_c(label, fn, w=300, ax=150, ay=330, ref=None, bg=None, h=None):
    def art(ox, oy):
        b = f'<rect x="{ox}" y="{oy}" width="{w}" height="{h or 2000}" fill="{bg}"/>' if bg else ""
        return b + fn(ox + ax, oy + ay)
    ov = (lambda ox, oy: person_ref(ox + ref[0], oy + ref[1], ref[2])) if ref else ""
    return Cell(label, art, w, [(ax, ay)], ov)


def sheet_nativity_stable():
    def scene(ox, oy, k, lamp=1.0, time="night", baby=True, people=True):
        x, y = ox + 600, oy + 600
        s = PR.starry_sky(ox, oy, ox + 1200, oy + 640, density=0.8, seed=2) if hasattr(PR, "starry_sky") else ""
        s += PR.stable(x, y, k, part="back", lamp=lamp, time=time)
        pts = PR.stable_points(x, y, k)
        if people:
            s += PR.ox(*pts["ox"], k * 0.9, -1, pose="look")
            s += PR.donkey(*pts["donkey"], k * 0.9, 1, pose="lie_look", sacks=0)
            s += CH.joseph_carpenter(*pts["joseph"], k, 1, pose="watch")
            s += CH.mary(*pts["mary"], k, 1, pose="kneel")
        if baby:
            s += CH.baby_jesus(*pts["bed"], k, 1)
            s += PR.manger(*pts["manger"], k, part="front", time="day")
        s += PR.stable(x, y, k, part="front", lamp=lamp, time=time)
        return s
    rows = [
        (640, [Cell("stable (night, lamp=1) + ox look, donkey lie_look, Joseph watch, Mary kneel, baby in the manger (scale .5)",
                    lambda ox, oy: scene(ox, oy, 0.5), 1200, [(600, 600)]),
               Cell("stable time='day' lamp=.4, empty (manger=True)", lambda ox, oy: f'<rect x="{ox}" y="{oy}" width="1100" height="640" fill="#bfe0ea"/>'
                    + PR.stable(ox + 550, oy + 600, 0.5, time="day", lamp=0.4), 1100, [(550, 600)])]),
        (300, [_nat_c("manger", lambda x, y: PR.manger(x, y, 1.0), 280, 140, 280),
               _nat_c("manger + baby (back / baby / front)", lambda x, y: PR.manger(x, y, 1.0, part="back") + CH.baby_jesus(*PR.manger_points(x, y, 1.0)["bed"], 1.0)
                      + PR.manger(x, y, 1.0, part="front"), 280, 140, 280),
               _nat_c("manger glow=1, baby awake", lambda x, y: PR.manger(x, y, 1.0, part="back", glow=1.0) + CH.baby_jesus(*PR.manger_points(x, y, 1.0)["bed"], 1.0, state="awake")
                      + PR.manger(x, y, 1.0, part="front"), 280, 140, 280, bg=NIGHT),
               _nat_c("hay=False time='night'", lambda x, y: PR.manger(x, y, 1.0, hay=False, time="night"), 280, 140, 280)]
         + [_nat_c(f"gift {k} open={o} glow={g}", lambda x, y, k=k, o=o, g=g: PR.gift(x, y, 1.3, kind=k, open=o, glow=g), 180, 90, 280, bg=NIGHT if g else None)
            for k, o, g in (("gold", 0, 0), ("gold", 1, 1), ("frankincense", 0, 0), ("frankincense", 1, 1), ("myrrh", 0, 0), ("myrrh", 1, 1))]),
    ]
    return render_sheet("nativity_stable", "props — Nativity: the cave-stable (parts, people inside), the manger, the three treasures", rows)


def sheet_nativity_animals():
    rows = [
        (320, [_nat_c(f"ox {p}", lambda x, y, p=p: PR.ox(x, y, 0.9, pose=p), 300, 130, 300) for p in PR.OX_POSES if p != "walk"]),
        (330, [_nat_c(f"donkey {p}", lambda x, y, p=p: PR.donkey(x, y, 0.9, pose=p, sacks=0), 260, 120, 310) for p in PR.DONKEY_REST_POSES]
         + [_nat_c("donkey saddle='blue' bridle", lambda x, y: PR.donkey(x - 40, y, 0.9, saddle="blue", bridle=True), 320, 140, 310),
            _nat_c("Mary ride on donkey_points seat; Joseph lead", lambda x, y: PR.donkey(x - 120, y, 0.9, pose="walk_a", saddle="blue", bridle=True)
                   + CH.mary(*PR.donkey_points(x - 120, y, 0.9, pose="walk_a")["seat"], 0.9, pose="ride", pregnant=True)
                   + CH.joseph_carpenter(PR.donkey_points(x - 120, y, 0.9)["lead"][0] - CH.JOSEPH_LEAD_HAND[0] * 0.9, y, 0.9, pose="lead_a"), 620, 250, 310)]),
        (330, [_nat_c(f"sheep {p}", lambda x, y, p=p, v=v: PR.sheep(x, y, 1.0, variant=v, pose=p), 230, 110, 300) for v, p in ((0, "lie"), (1, "sleep"), (2, "look_up"))]
         + [_nat_c("lamb lie / look_up", lambda x, y: PR.sheep(x - 50, y, 1.0, pose="lie", lamb=True) + PR.sheep(x + 60, y, 1.0, pose="look_up", lamb=True), 260, 130, 300)]
         + [_nat_c(f"dog {p}", lambda x, y, p=p: PR.dog(x, y, 1.0, pose=p), 200, 90, 300) for p in PR.DOG_POSES[:4]]),
        (520, [_nat_c("camel saddle='red' + wise man ride at camel_points seat", lambda x, y: PR.camel(x, y, 0.8, saddle="red", load=False)
                      + CH.wise_men(*PR.camel_points(x, y, 0.8)["seat"], 0.8, variant=0, pose="ride"), 520, 220, 500),
               _nat_c("walk phase .25, saddle purple, Balthasar", lambda x, y: PR.camel(x, y, 0.8, pose="walk", phase=0.25, saddle="purple")
                      + CH.wise_men(*PR.camel_points(x, y, 0.8, pose="walk", phase=0.25)["seat"], 0.8, variant=2, pose="ride"), 520, 220, 500),
               _nat_c("saddle green, Caspar", lambda x, y: PR.camel(x, y, 0.8, saddle="green")
                      + CH.wise_men(*PR.camel_points(x, y, 0.8)["seat"], 0.8, variant=1, pose="ride"), 520, 220, 500)]),
    ]
    return render_sheet("nativity_animals", "props — Nativity: ox, donkey (rest poses, saddle, bridle, riders), resting sheep, the dog, camels with riders", rows)


def sheet_nativity_places():
    def naz_in(ox, oy):
        x, y = ox + 600, oy + 560
        s = PR.nazareth_house(x, y, 0.55, view="interior", light=0.8, light_x=300)
        s += CH.mary(x - 120, y, 0.55, pose="startled") + CH.angel(x + 160, y, 0.55, -1, pose="announce", glow=0.8)
        return s

    def fam_in(ox, oy):
        x, y = ox + 550, oy + 560
        s = PR.family_house(x, y, 0.55, view="interior", star_light=0.8)
        s += CH.mary(x + PR.FAMILY_SEAT[0] * 0.55 + 50 * 0.55, y, 0.55, pose="sit_hold")
        s += CH.joseph_carpenter(x - 330 * 0.55, y - 20 * 0.55, 0.52, pose="watch")
        s += CH.wise_men(x + 120, y, 0.55, -1, variant=0, pose="kneel_offer", gift_open=1.0, gift_glow=1.0)
        s += CH.wise_men(x + 270, y - 10, 0.53, -1, variant=1, pose="carry_gift")
        return s

    def inn_c(ox, oy):
        x, y = ox + 480, oy + 600
        s = f'<rect x="{ox}" y="{oy}" width="960" height="640" fill="{NIGHT}"/>' + PR.starry_sky(ox, oy, ox + 960, oy + 640, time="dusk", density=0.6)
        s += PR.inn(x, y, 0.62, part="back", time="dusk")
        s += CH.townsfolk(x, y - 6, 0.62, -1, kind="innkeeper", pose="shake_head", phase=0.25)
        s += PR.inn(x, y, 0.62, part="front", time="dusk")
        s += CH.joseph_carpenter(x + 230, y + 10, 0.62, -1, pose="knock", phase=0.5)
        s += CH.mary(x + 360, y + 14, 0.62, -1, pose="stand", pregnant=True, expr="tired")
        return s
    rows = [
        (640, [Cell("nazareth_house view='interior' light=.8 (Mary startled, angel announce)", naz_in, 1200, [(600, 560)]),
               Cell("nazareth_house exterior (day)", lambda ox, oy: f'<rect x="{ox}" y="{oy}" width="1000" height="640" fill="#bfe0ea"/>'
                    + PR.nazareth_house(ox + 520, oy + 600, 0.85) + CH.mary(ox + 820, oy + 610, 0.85, -1, pose="carry_jar_walk_a"), 1000, [(520, 600)])]),
        (640, [Cell("family_house interior, star_light=.8: Mary sit_hold on the bench, Joseph, wise men", fam_in, 1100, [(550, 560)]),
               Cell("family_house exterior (night) + the_star beam", lambda ox, oy: PR.starry_sky(ox, oy, ox + 560, oy + 640, density=0.8)
                    + PR.the_star(ox + 280, oy + 90, 0.45, beam=0.8, beam_to=(ox + 280, oy + 300)) + PR.family_house(ox + 280, oy + 620, 0.6, star_light=0.8), 560, [(280, 620)]),
               Cell("inn (dusk, full) + innkeeper shake_head, Joseph knock, Mary", inn_c, 700, [(480, 600)])]),
        (700, [Cell("bethlehem_town part='back' (dusk) + part='street' + townsfolk_crowd(walk) + crowd(squeeze)", lambda ox, oy: PR.starry_sky(ox, oy, ox + 2300, oy + 700, time="dusk", density=0.5)
                    + PR.bethlehem_town(ox, ox + 2300, oy + 300, 0.55, time="dusk", part="back")
                    + PR.bethlehem_town(ox, ox + 2300, oy + 520, 0.5, time="dusk", part="street")
                    + CH.townsfolk_crowd(ox + 700, oy + 640, 0.45, n=16, width=1300, rows=3, seed=1)
                    + CH.townsfolk_crowd(ox + 1750, oy + 650, 0.45, pose="squeeze", n=10, width=900, rows=2, seed=4), 2300, [(0, 520)])]),
    ]
    return render_sheet("nativity_places", "props — Nativity: Nazareth (inside / outside), the Bethlehem house (Matthew 2), the inn, the town and its busy street", rows)


def sheet_nativity_sky():
    def fields(ox, oy, glory=False):
        x0, x1, gy = ox, ox + 1150, oy + 520
        s = PR.starry_sky(ox, oy, x1, oy + 700, density=1.0, seed=3)
        s += PR.night_hills(x0, x1, gy, 0.6, part="back")
        if glory:
            s += PR.glory(ox + 640, gy + 40, 0.6, progress=1.0)
        s += PR.night_hills(x0, x1, gy, 0.6, part="front", fire=0.0 if glory else 1.0, phase=0.3, fire_x=ox + 430)
        for i, (dx, p, v) in enumerate(((330, "shield_eyes" if glory else "sit_warm", 0), (480, "shield_eyes" if glory else "sit", 1), (560, "kneel" if glory else "lean", 5),
                                        (250, "hold_lamb", 2))):
            s += CH.shepherds(ox + dx, gy + 60, 0.42, 1 if i < 3 else 1, variant=v, pose=p, expr="sleepy" if (not glory and p == "sit") else None)
        for i, dx in enumerate((700, 820, 900)):
            s += PR.sheep(ox + dx, gy + 70 + 10 * i, 0.4, -1, variant=i, pose="look_up" if glory else ("lie", "sleep", "lie")[i])
        s += PR.dog(ox + 160, gy + 70, 0.45, pose="look_up" if glory else "lie")
        if glory:
            s += CH.angel(ox + 700, gy - 20, 0.5, -1, pose="float", glow=1.0, lift=60)
        return s
    rows = [
        (700, [Cell("night_hills back/front (fire phase .3, fold) + shepherds by the fire, sheep lie / sleep, dog", lambda ox, oy: fields(ox, oy), 1150, [(0, 520)]),
               Cell("glory(...) round the group + angel float lift=60; shepherds shield_eyes, kneel; sheep look_up", lambda ox, oy: fields(ox, oy, True), 1150, [(640, 560)])]),
        (560, [Cell("starry_sky (milky way) + the_star intensity 1, pulse 0", lambda ox, oy: PR.starry_sky(ox, oy, ox + 760, oy + 560) + PR.the_star(ox + 380, oy + 220, 0.6), 760, [(380, 220)]),
               Cell("starry_sky time='dusk' + moon; the_star intensity .4", lambda ox, oy: PR.starry_sky(ox, oy, ox + 760, oy + 560, time="dusk", moon=(ox + 600, oy + 140)) + PR.the_star(ox + 300, oy + 200, 0.5, intensity=0.4), 760, [(300, 200)]),
               Cell("heaven_light progress .5 / 1 + angel_choir", lambda ox, oy: PR.starry_sky(ox, oy, ox + 760, oy + 560, seed=5) + PR.heaven_light(ox + 380, oy + 230, 0.45, progress=1.0)
                    + CH.angel_choir(ox + 60, ox + 700, oy + 380, n=9, scale=0.2, rows=2), 760, [(380, 230)])]),
        (300, [Cell(f"day_night_sky t={tt}", lambda ox, oy, tt=tt: PR.day_night_sky(ox, oy, ox + 380, oy + 300, t=tt, scale=0.5)
                    + f'<rect x="{ox}" y="{oy + 250}" width="380" height="50" fill="#7f9a5a"/>', 380, []) for tt in (0.0, 0.25, 0.45, 0.6, 0.75, 0.95)]),
    ]
    return render_sheet("nativity_sky", "props — Nativity: the fields at night, the glory of the Lord, the star, heaven's light and the choir, days passing", rows)


def sheet_nativity_journey():
    def road(ox, oy):
        x0, x1, y = ox, ox + 1150, oy + 300
        s = PR.day_night_sky(ox, oy, x1, oy + 400, t=0.3, scale=0.6) + PR.journey_road(x0, x1, y, 0.6)
        pts = PR.road_points(x0, x1, y, 0.6)
        px, py, k = pts[2]
        kk = 0.42 * k
        s += PR.donkey(px, py, kk, 1, pose="walk_a", saddle="blue", bridle=True)
        s += CH.mary(*PR.donkey_points(px, py, kk, pose="walk_a")["seat"], kk, pose="ride", pregnant=True)
        s += CH.joseph_carpenter(PR.donkey_points(px, py, kk)["lead"][0] - CH.JOSEPH_LEAD_HAND[0] * kk, py, kk, pose="lead_a")
        return s

    def dunes(ox, oy):
        s = PR.day_night_sky(ox, oy, ox + 1150, oy + 640, t=0.58, scale=0.6) + PR.the_star(ox + 900, oy + 110, 0.4)
        s += PR.desert_dunes(ox, ox + 1150, oy + 420, 0.6, time="dusk", oasis_x=ox + 300)
        for i, v in enumerate((0, 1, 2)):
            cx, cy = ox + 520 + i * 200, oy + 560 + 6 * i
            s += PR.camel(cx, cy, 0.36, pose="walk", phase=0.3 * i, saddle=("red", "green", "purple")[v], load=False)
            s += CH.wise_men(*PR.camel_points(cx, cy, 0.36, pose="walk", phase=0.3 * i)["seat"], 0.36, variant=v, pose="ride")
        return s

    def obs(ox, oy):
        x, y = ox + 560, oy + 520
        s = PR.starry_sky(ox, oy, ox + 1150, oy + 640, seed=8) + PR.the_star(ox + 900, oy + 120, 0.5, pulse=0.3)
        s += PR.observatory(x, y, 0.55, part="back")
        s += CH.wise_men(x - 120, y + 20, 0.55, 1, variant=0, pose="point_up") + CH.wise_men(x + 30, y + 24, 0.55, 1, variant=1, pose="study")
        s += CH.wise_men(x + 170, y + 18, 0.55, -1, variant=2, pose="look_up")
        s += PR.observatory(x, y, 0.55, part="front")
        return s
    rows = [
        (640, [Cell("journey_road + day_night_sky t=.3; Mary rides (pregnant), Joseph leads, at road_points()[2]", road, 1150, [(0, 300)]),
               Cell("desert_dunes (dusk, oasis) + camels walk with saddles + riders at camel_points seat; the star", dunes, 1150, [(0, 420)])]),
        (640, [Cell("observatory back / wise men point_up, study, look_up / front parapet; the star", obs, 1150, [(560, 520)]),
               Cell("oasis (scale .7) / astrolabe / star_chart", lambda ox, oy: f'<rect x="{ox}" y="{oy}" width="1150" height="640" fill="#f0d7a0"/>' + PR.oasis(ox + 330, oy + 420, 0.8)
                    + PR.astrolabe(ox + 780, oy + 260, 1.3) + PR.star_chart(ox + 960, oy + 500, 1.2, rot=-8), 1150, [(330, 420)])]),
    ]
    return render_sheet("nativity_journey", "props — Nativity: the long road (days passing), the desert journey of the wise men, the observatory in the East", rows)


def sheet_nativity_items():
    def c(label, fn, w=300, ax=150, ay=300, bg=None):
        return _nat_c(label, fn, w, ax, ay, bg=bg)
    rows = [
        (330, [c(f"campfire phase={ph}", lambda x, y, ph=ph: PR.campfire(x, y, 1.0, phase=ph), 260, 130, 300, NIGHT) for ph in (0.0, 0.33, 0.66)]
         + [c("sheepfold + sheep inside (back / sheep / front)", lambda x, y: PR.sheepfold(x, y - 40, 0.6, part="back") + PR.sheep(x - 40, y - 50, 0.4, pose="lie")
              + PR.sheep(x + 60, y - 40, 0.4, pose="sleep", variant=1) + PR.sheepfold(x, y - 40, 0.6, part="front"), 460, 230, 300),
            c("hanging_lamp lit 1 / 0", lambda x, y: PR.hanging_lamp(x - 60, y - 240, 1.3) + PR.hanging_lamp(x + 60, y - 240, 1.3, lit=0), 300, 150, 300, NIGHT),
            c("broom / water_jar", lambda x, y: PR.broom(x - 60, y, 1.0, rot=8) + PR.water_jar(x + 60, y, 1.4), 300, 150, 300)]),
        (330, [c("presents n=1..5", lambda x, y: PR.presents(x - 200, y, 0.9, n=2) + PR.presents(x + 100, y, 0.9, n=5, seed=3), 560, 280, 300),
               c("calendar circled 0 / .5 / 1", lambda x, y: PR.calendar(x - 270, y - 290, 0.75, circled=0) + PR.calendar(x, y - 290, 0.75, circled=0.5)
                 + PR.calendar(x + 270, y - 290, 0.75), 820, 410, 300)]
         + [c(f"figure {k}", lambda x, y, k=k: PR.nativity_figure(x, y, 1.1, kind=k), 140, 70, 300) for k in ("mary", "joseph", "baby", "angel")]),
        (330, [c(f"figure {k}", lambda x, y, k=k: PR.nativity_figure(x, y, 1.1, kind=k), 150, 75, 300) for k in ("shepherd", "magus", "sheep", "ox", "donkey", "star", "gift")]
         + [c("nativity_set (all) / figures=('star','baby','mary')", lambda x, y: PR.nativity_set(x - 230, y, 0.75) + PR.nativity_set(x + 230, y, 0.75, figures=("star", "baby", "mary")), 900, 450, 300)]),
    ]
    return render_sheet("nativity_items", "props — Nativity: campfire, sheepfold, lamp, broom, jar, presents, calendar, the little nativity set", rows)


def sheet_nativity_home():
    def room(ox, oy, end=False):
        x0, x1, y = ox, ox + 1150, oy + 560
        s = PR.living_room(x0, x1, y, 0.6, glow=0.8)
        s += PR.calendar(ox + 980, oy + 120, 0.6)
        s += PR.christmas_tree(ox + 620, y, 1.0, star=1.0 if end else 0.3, twinkle=0.3, ornaments=1.0 if end else 0.6)
        if end:
            s += PR.presents(ox + 820, y + 20, 0.6, n=3) + PR.nativity_set(ox + 420, y + 30, 0.42, glow=0.6)
            s += CH.child(ox + 250, y + 40, 1.0, pose="place", outfit="jumper", item="sheep")
        else:
            s += CH.child(ox + 470, y + 40, 1.0, pose="decorate", outfit="jumper")
        return s
    rows = [
        (640, [Cell("living_room + calendar + christmas_tree (star .3, ornaments .6) + child decorate (jumper)", lambda ox, oy: room(ox, oy), 1150, [(0, 560)]),
               Cell("the ending: tree star=1, presents, nativity_set glow .6, child place item='sheep'", lambda ox, oy: room(ox, oy, True), 1150, [(0, 560)])]),
        (520, [_nat_c(f"christmas_tree twinkle={tw} star={st}", lambda x, y, tw=tw, st=st, tp=tp, orn=orn: PR.christmas_tree(x, y, 1.0, twinkle=tw, star=st, top_star=tp, ornaments=orn), 380, 190, 490)
               for tw, st, tp, orn in ((0.0, 1.0, True, 1.0), (0.5, 0.0, True, 1.0), (0.25, 0.0, False, 0.3))]
         + [_nat_c("christmas_tree lights=0 presents=True", lambda x, y: PR.christmas_tree(x, y, 1.0, lights=0, presents=True), 520, 260, 490)]),
    ]
    return render_sheet("nativity_home", "props — Nativity: the living room, the Christmas tree, the child and the nativity set", rows)


SHEETS = {"fish": sheet_fish, "ship": sheet_ship, "items": sheet_items, "castor": sheet_castor,
          "plants": sheet_plants, "creatures": sheet_creatures, "buildings": sheet_buildings,
          "lions": sheet_lions, "daniel": sheet_daniel, "david_items": sheet_david_items,
          "david_creatures": sheet_david_creatures, "david_camp": sheet_david_camp, "valley": sheet_valley,
          "noah_ark": sheet_noah_ark, "noah_weather": sheet_noah_weather, "noah_items": sheet_noah_items,
          "noah_animals": sheet_noah_animals, "noah_pairs": sheet_noah_pairs,
          "joseph_items": sheet_joseph_items, "joseph_animals": sheet_joseph_animals, "joseph_egypt": sheet_joseph_egypt,
          "storm_boat": sheet_storm_boat, "storm_lake": sheet_storm_lake, "storm_weather": sheet_storm_weather,
          "storm_items": sheet_storm_items, "storm_story": sheet_storm_story,
          "nativity_stable": sheet_nativity_stable, "nativity_animals": sheet_nativity_animals,
          "nativity_places": sheet_nativity_places, "nativity_sky": sheet_nativity_sky, "nativity_journey": sheet_nativity_journey,
          "nativity_items": sheet_nativity_items, "nativity_home": sheet_nativity_home}


def main():
    names = sys.argv[1:] or list(SHEETS)
    try:
        for n in names:
            SHEETS[n]()
    finally:
        raster.close()


if __name__ == "__main__":
    main()
