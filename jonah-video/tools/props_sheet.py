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
"""
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
    out = BUILD / "preview" / f"props_{name}.png"
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
            _c(f"hay bale / bundle / pile", lambda x, y: PR.hay(x - 150, y, 0.8) + PR.hay(x + 30, y - 120, 0.8, kind="bundle") + PR.hay(x + 100, y, 0.8, kind="pile"), 420, 220, 260)]),
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


SHEETS = {"fish": sheet_fish, "ship": sheet_ship, "items": sheet_items, "castor": sheet_castor,
          "plants": sheet_plants, "creatures": sheet_creatures, "buildings": sheet_buildings,
          "lions": sheet_lions, "daniel": sheet_daniel, "david_items": sheet_david_items,
          "david_creatures": sheet_david_creatures, "david_camp": sheet_david_camp, "valley": sheet_valley,
          "noah_ark": sheet_noah_ark, "noah_weather": sheet_noah_weather, "noah_items": sheet_noah_items,
          "noah_animals": sheet_noah_animals, "noah_pairs": sheet_noah_pairs}


def main():
    names = sys.argv[1:] or list(SHEETS)
    try:
        for n in names:
            SHEETS[n]()
    finally:
        raster.close()


if __name__ == "__main__":
    main()
