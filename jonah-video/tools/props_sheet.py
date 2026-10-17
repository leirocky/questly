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


SHEETS = {"fish": sheet_fish, "ship": sheet_ship, "items": sheet_items, "castor": sheet_castor,
          "plants": sheet_plants, "creatures": sheet_creatures, "buildings": sheet_buildings}


def main():
    names = sys.argv[1:] or list(SHEETS)
    try:
        for n in names:
            SHEETS[n]()
    finally:
        raster.close()


if __name__ == "__main__":
    main()
