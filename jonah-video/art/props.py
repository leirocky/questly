"""Creatures, vehicles, plants, buildings and props for the Jonah picture-book video.

Every public drawing function returns SVG markup — one ``<g filter="url(#wobble-fine)">…</g>``, no ``<svg>``
wrapper — to be placed inside ``art.style.svg_doc(...)``. Shapes use the ``art.style.P`` palette, umber ink
outlines (``art.style.INK``) of 3-5 px at scale 1 with round joins; never pure black or pure white.

Conventions (read these first)
------------------------------
* Signature style ``fn(x, y, scale=1.0, facing=1, **options)``. ``(x, y)`` is the ANCHOR in stage px (listed
  for each function). ``facing=1`` faces / moves right, ``facing=-1`` mirrors around the anchor's x.
* ``scale`` multiplies everything, including ink width (a 0.5-scale drawing has ~2 px lines, as distant
  things should). Scale 1 is "person scale": an adult (Jonah, art/characters.py) is ~330 px tall.
* Bounding boxes below are MEASURED at scale 1, facing=1, as (left, top, right, bottom) px relative to the
  anchor (rendered alpha incl. wobble). For facing=-1 use (-right, top, -left, bottom); multiply by scale.
* Local -> stage: ``local_to_stage(x, y, scale, facing, lx, ly)`` converts a documented local point (e.g. the
  ship bed, the fish mouth) to stage px for a drawing placed at (x, y, scale, facing).
* clipPath / mask / gradient ids are derived from the parameters, so many copies may share one document.
* Animate by rendering several frames (flipbook) with different option values, or by moving the layer
  with engine.motion; options marked "0..1" are continuous and look good at intermediate values.
* Compositions whose coordinates are absolute (city_wall, nineveh_skyline, harbor_dock) take x0/x1/y in
  stage px and have no scale/facing.

1. THE GREAT FISH
-----------------
fish(x, y, scale=1.0, facing=1, mouth=0.0, eye='open', tail=0.0, blush=True)
    Anchor: centre of the round body (about the level of the top of the pectoral fin).
    A huge friendly blue fish, ~1390 px long at scale 1 (tail tip -792 .. snout +599): blue body
    P['fish'], darker back P['fish_dark'], light belly/lower jaw P['fish_belly'], light spots
    P['fish_spot'], scale arcs, gill line, dorsal / anal / pectoral fins, vertical forked tail fin,
    one big kind eye with highlights, rosy cheek, gentle smile.
    BBox: mouth=0 (-792, -462, 599, 357); mouth=1 (-792, -462, 566, 386);
          tail=+-1 widens left to -880 and bottom to 418.
    Options:
      mouth 0..1  jaw opens; lower jaw swings down 55 deg and the throat stretches like a pouch, snout
                  lifts 19 deg; dark-red inside P['mouth_inside'] with a pink tongue. Smooth at every value
                  (check 0, .33, .66, 1). At 1 the gape is ~395 px — big enough to swallow a 330 px person.
      eye         'open' | 'closed' (sleepy curve with lashes) | 'happy' (^ arc) | 'surprised' (big eye,
                  small pupil, raised brow).
      tail -1..1  tail fin bends around the peduncle (+1 = up, -1 = down, 22 deg); the pectoral fin
                  counter-flaps. Cycle it (e.g. sin) for swimming.
      blush       rosy cheek on/off.
fish_mouth_points(mouth=0.0) -> {'corner', 'upper', 'lower', 'center'}
    Local key points of the mouth: corner (hinge) (272, 42); lip tips at mouth=0 (588, 16)/(596, 28);
    at mouth=1 upper (562, -85), lower (469, 299), center (443, 87). Put Jonah at 'center' when swallowed /
    spat out; the eye is at about (380, -115).

2. THE SHIP
-----------
ship(x, y, scale=1.0, facing=1, sail='full', cutaway=False, lantern=True, oars=False, part='all', flag=True)
    Anchor: hull centre on the WATERLINE (y=0). Ancient Phoenician-style merchant ship, bow on the facing
    side: curved planked hull (P['wood'] tones) with a teal / terracotta painted band, raised bow post,
    curling stern post, rail with a row of round painted shields, one mast, yard and square striped sail
    P['sail'] / P['sail_stripe'], stays and sheets, a pennant, a big steering oar at the stern.
    BBox: (-603, -943, 524, 126) — oars=True extends the bottom to 157. The hull below the waterline
    (y 0..+98) is drawn: cover it with your sea layer.
    Geometry (local, facing right): deck / feet of people standing on board SHIP_DECK_Y = -165 (valid
    for |x| < 300); rail top ~-220; mast x=-10 from -170 to -930; yard y~-850 spanning x -318..298;
    sail foot ~-500..-550 (just above the head of an adult standing on deck); stern curl x -520..-420,
    y -440..-175; bow knob (488, -358); stern lantern hook (-428, -372).
    Options:
      sail     'full' (billowing, striped) | 'furled' (rolled under the yard, tied) | 'torn' (ragged
               edges, a hole, a flapping loose strip, yard tilted - for the storm).
      cutaway  True shows the hull in dollhouse cross-section with a warm lantern-lit hold: amphorae and
               a sack (stern side), a straw mattress with pillow and folded teal blanket, a crate and
               sack (bow side), a hanging lantern at x=-160 (bottom at y~-14), ribs and deck beams.
               SHIP_INTERIOR = (-360, -146, 360, 34): the hold rectangle (x0, top, x1, bottom; bottom
               corners rounded, floor surface y~18). Its lower part is BELOW the waterline: draw the
               sea in front only below y~+40 (or translucent) for cutaway shots.
               SHIP_BED = (-130, 240, -4): mattress x0, x1 and its top surface y. Lay sleeping Jonah on
               it head at the pillow end (x~-100), feet toward x~230; ~140 px of headroom.
      lantern  a small lit lantern hanging from the stern post (glow off in cutaway).
      oars     a row of 7 oars dipping into the water.
      part     'all' | 'back' | 'front'. 'back' = flag, stays, mast, sail, sheets, hull, posts and the
               cutaway hold; 'front' = rail with shields, steering oar, oars, stern lantern. Draw
               ship(part='back') -> characters standing on deck (feet at SHIP_DECK_Y) -> ship(part='front')
               so the rail hides their shins.
      flag     the pennant on the masthead.

3. PROPS
--------
crate(x, y, scale=1.0, rot=0)
    Anchor: centre. Planked wooden box with a diagonal brace, top and side faces. BBox (-53, -59, 68, 48).
jar(x, y, scale=1.0, rot=0, color=None)
    Anchor: centre. Terracotta amphora with two handles, cream band, wavy line; color overrides the clay.
    BBox (-44, -86, 42, 81).
sack(x, y, scale=1.0, rot=0, color=None, seed=0)
    Anchor: bottom centre. Lumpy burlap sack tied with rope, with a patch; seed varies the lumps.
    BBox (-60, -122, 57, 4).
lots_jar(x, y, scale=1.0, sticks=5)
    Anchor: bottom centre. Clay pot the lots are drawn from, with wooden lot sticks poking out (sticks=0
    for an empty pot). BBox (-50, -152, 49, 3); pot rim at y~-78.
lot(x, y, scale=1.0, rot=0, marked=False)
    Anchor: centre. A small flat wooden lot stick 76 x 22. marked=True adds a glowing orange-gold mark with
    a soft golden halo (the lot that falls on Jonah). BBox (-41, -14, 39, 13); marked halo (-70, -51, 69, 50).
lantern(x, y, scale=1.0, lit=True)
    Anchor: the top hook ring (hang it from a beam). Oil lantern 58 x 137 (bottom tip y~135); lit adds a
    warm flame and a ~100 px glow halo. BBox unlit (-29, -2, 29, 136); lit incl. halo (-101, -13, 99, 187).
rope_coil(x, y, scale=1.0)
    Anchor: bottom centre. Three-loop coil of rope with a loose end to the right. BBox (-58, -65, 90, 5).
scroll(x, y, scale=1.0, rot=0, opened=False)
    Anchor: centre. Closed: rolled parchment with a red tie, BBox (-76, -23, 74, 45). opened=True:
    parchment between two wooden rollers with lines of writing, BBox (-100, -78, 99, 77).
booth(x, y, scale=1.0, facing=1)
    Anchor: bottom centre (ground). Jonah's little shelter (Jonah 4:5): four stick posts, an A-frame of
    crossed sticks, a striped cloth roof draped over it with side flaps, a shade cloth hanging at the back,
    leafy branches on top. BBox (-288, -542, 286, 11). Eaves y~-350, apex y~-530, front posts at x=-200 and
    192. BOOTH_SEAT = (-140, -250, 132, 0): the open space under the roof (x0, top, x1, ground) where a seated
    Jonah fits (draw him after the booth). A standing adult's head touches the eaves.
throne(x, y, scale=1.0)
    Anchor: bottom centre (floor). Royal Assyrian throne, front view: tall purple back with gold rosettes,
    gold armrests and lion-paw legs, lavender cushion, footstool. BBox (-169, -442, 167, 2). Seat cushion top
    y~-196 (a sitting king's hips at about (0, -190)), armrests y~-236, footstool top y~-40.
ash_pile(x, y, scale=1.0, smoke=False)
    Anchor: bottom centre. Low grey mound of ashes with charcoal bits (the king sits in ashes, Jonah 3:6).
    BBox (-142, -69, 141, 2); smoke=True adds soft wisps up to y~-220.

4. PLANTS
---------
castor_plant(x, y, scale=1.0, growth=1.0, wither=0.0, bite=0.0, side=1, seed=0)
    Anchor: root point on the ground (centre of a small soil mound). The castor-oil plant (蓖麻, Ricinus
    communis): thick reddish-green stem (P['leaf_dark'] + terracotta) with nodes, very large peltate
    palm-shaped leaves with 7-9 pointed lobes and pale veins (P['leaf']), a side branch, spiky red seed
    clusters at the top. side=+1 leans / spreads the canopy to the right (+x), side=-1 to the left.
    Stem height castor_height(growth) = 30 + 470 * growth**1.5 (g 0: 30, .25: 89, .5: 196, .75: 335, 1: 500).
    BBox (side=1): growth 0 (-49, -44, 47, 11) sprout with two seed-leaves; .25 (-53, -120, 51, 11);
          .5 (-112, -267, 107, 12) about waist high; .75 (-161, -431, 255, 13);
          1 (-214, -622, 509, 13) taller than a standing man; growth=1 wither=1 (-119, -530, 479, 13).
    Shade: at growth=1 the leaves form a canopy between y~-620 and -330 spanning x -210..510, densest over
    CASTOR_SHADE = (-180, 400) (ground x-range of the shade for a high sun; mirror for side=-1). Put the
    booth centre at x + 270*scale*side so the canopy arches over its roof (see props_castor.png).
    Options (all continuous, check 0/.25/.5/.75/1):
      growth 0..1  sprout -> waist-high bush -> tall plant; leaves are born one by one and unfold, the
                   branch grows from .4 to .85, seed clusters appear after .68, seed-leaves vanish by .37.
      wither 0..1  leaves turn yellow-brown (P['leaf_dry'] at .55) then dead brown (P['leaf_dead']), get
                   brown spots, curl and shrink, petioles droop until leaves hang; the stem bends over.
      bite 0..1    a scalloped notch eaten into the stem near the ground (y~-16) on the side opposite the
                   canopy, with pale pith and crumbs. For the worm: worm(x - WORM_BITE_DX*scale*side, y,
                   scale, facing=side, chomp=...) puts its mouth in the notch (WORM_BITE_DX = 52).
      seed         varies leaf spin.
palm_tree(x, y, scale=1.0, lean=0.0, sway=0.0, dates=True)
    Anchor: base of the trunk. Date palm ~605 px tall: ringed trunk, crown of feathery fronds, date
    clusters. lean -1..1 moves the crown +-150 px sideways (crown at (150*lean, -430)); sway -1..1 swings the
    fronds for wind. BBox lean 0 (-221, -604, 220, 5); lean 1 (-71, -604, 370, 6).
olive_tree(x, y, scale=1.0, seed=0)
    Anchor: base of the trunk. Gnarled grey trunk, rounded silver-green canopy, small dark olives.
    BBox (-177, -371, 177, 2).
bush(x, y, scale=1.0, variant=0)
    Anchor: base centre. variant 0 green, 1 green with pink flowers, 2 dry grey-olive desert shrub with
    twigs, 3 dark green with red berries. BBox (-99, -112, 104, 19); variant 2 (-90, -95, 94, 19).
grass_tuft(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base centre. variant 0 green, 1 dry yellow, 2 green with red / yellow wild flowers. sway -1..1
    bends the blades. BBox (-40, -58, 36, 1); variant 2 up to y -93.
seaweed(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base on the sea floor. variant 0 olive kelp ribbons (-47, -248, 40, 3); 1 pink bubbly weed
    (-83, -128, 79, 6); 2 teal sea-grass (-71, -186, 76, 1); 3 orange branching coral (-117, -155, 107, 11).
    sway -1..1 bends the tips (animate with a sine for currents).
reeds(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base centre. Clump of reed blades with three brown cattails. BBox (-66, -289, 79, 4).

5. CREATURES
------------
worm(x, y, scale=1.0, facing=1, chomp=0.0, crawl=0.0)
    Anchor: bottom centre (on the ground). Small cute pink caterpillar-like worm with green spots,
    antennae, a big dot eye and rosy cheek; head on the facing side. Body ~62 px long.
    BBox (-35, -45, 44, 2). Mouth at local (40, -11). chomp 0..1 opens the mouth (two tiny teeth);
    crawl 0..1 arches the middle of the body like an inchworm.
gull(x, y, scale=1.0, facing=1, wing=0.0, pose='fly')
    Anchor: body centre. Cream seagull with grey wings, dark wing tips, yellow beak. pose 'fly' | 'stand'
    (wings folded, orange legs, feet at y~+40). wing -1..1 is the flap position (+1 wings up, 0 swept back
    / glide, -1 down-stroke); cycle it for flight. BBox fly wing 0 (-105, -59, 65, 19); wing 1
    (-75, -119, 65, 19); wing -1 (-75, -28, 65, 45); stand (-65, -36, 60, 40).
dove(x, y, scale=1.0, facing=1, wing=0.0, pose='fly')
    Anchor: body centre. Cream-white dove with lavender wings, pink beak; same options as gull, smaller.
    BBox fly (-85, -50, 46, 17); wing 1 (-58, -98, 46, 17); stand (-49, -34, 42, 37).
small_fish(x, y, scale=1.0, facing=1, color='orange', tail=0.0)
    Anchor: centre. Little striped round fish with a big eye. color: a FISH_COLORS name ('orange', 'yellow',
    'pink', 'teal', 'purple', 'blue', 'red') or any hex. tail -1..1 bends the tail. BBox (-59, -28, 39, 24).
animal(x, y, scale=1.0, facing=1, kind='sheep', sackcloth=False)
    Anchor: bottom centre (hooves on the ground). Cute rounded picture-book animals, head on the facing side:
      'sheep'  fluffy cream wool, tan face          BBox (-95, -147, 119, 1)
      'goat'   cream with brown patches, horns, beard (-79, -214, 109, 1)
      'cow'    cream with brown patches, pink muzzle (-133, -214, 185, 2)
      'donkey' grey, long ears, dark mane           (-107, -295, 165, 1)
      'camel'  tan dromedary, one hump, long neck    (-116, -321, 227, 2)
    sackcloth=True drapes a burlap blanket with a patch and a rope tie over the back (Jonah 3:8).

6. BUILDINGS
------------
house(x, y, scale=1.0, variant=0, facing=1)
    Anchor: bottom centre of the front wall (ground). Flat-roofed mud-brick house at person scale (doors
    ~330 px tall), front face + a 3/4 side face on the facing side, roof beam ends, small dark windows,
    exposed bricks. Variants: 0 one storey, pot on the roof (-325, -652, 385, 12), roof y~-510;
    1 two storeys with an outside stair and a teal awning (-431, -889, 330, 19), roof y~-845;
    2 wide, striped door awning, rooftop shade, pots (-394, -733, 451, 12), roof y~-524;
    3 palm-frond roof shade, laundry line, bush (-305, -794, 455, 15), roof y~-594.
    For background streets use scale 0.2-0.5.
city_wall(x0, x1, y, height=260, gate=None, doors_open=0.0, towers=True, seed=0)
    Anchor: ground line y, from x0 to x1 (absolute stage px, no scale). Thick Assyrian mud-brick wall with
    stepped crenellations, brick courses, base band and projecting towers every ~420*k px (k = height/260;
    every detail scales with k). Wall top y-height, merlons to y-height-34k, towers to y-height-90k.
    gate=(gx, width) adds an arched gate centred at gx: flanking towers 120k wide reaching y-1.45*height-34k,
    blue glazed rosette bands, arched opening from y up to y - 0.62*height - width/2 with tall studded
    wooden doors; doors_open 0..1 swings them open showing the passage and the bright far side.
    A 330 px adult walks through comfortably with height >= 520 and width >= 220. BBox ~ (x0-3, top, x1+2, y+3).
ziggurat(x, y, scale=1.0)
    Anchor: bottom centre. Stepped temple tower: three tiers with buttress lines, a central stair and a
    small shrine with a glazed rosette band on top. Drawn at person scale (huge): BBox (-771, -1199, 770, 3);
    use scale 0.2-0.5 in backgrounds.
nineveh_skyline(x0, x1, y, scale=1.0, seed=0, haze=0.35, tint=None)
    Anchor: ground line y from x0 to x1 (absolute). Dense distant panorama for far backgrounds: one or two
    ziggurats, rows of flat-roofed houses with tiny windows, date palms and a crenellated city wall with
    towers in front. Colours are mixed toward tint (default P['sky_warm']) by haze 0..1 (distance).
    Height ~350*scale (ziggurat tops), wall 110*scale. BBox ~ (x0-35, y-350*scale, x1+75, y+2).
harbor_dock(x0, x1, y, depth=250, bollards=True)
    Anchor: y = the plank walking surface (feet of people on the pier), from x0 to x1 (absolute). Wooden
    pier: planks, front beam, posts every 150 px going down to y+depth (dark and wet lower half, put the
    sea in front), cross braces, bollards with rope. BBox ~ (x0-3, y-49, x1+2, y+depth+3).
signpost(x, y, scale=1.0, left_text='尼尼微', right_text='他施')
    Anchor: foot of the post (ground). Wooden post with two arrow boards painted in LXGW WenKai: the upper
    board points left (left_text, centred y=-276), the lower board points right (right_text, centred
    y=-196); each board is 50*len(text)+70 px long. Pass '' to omit a board. Text is never mirrored.
    BBox with the defaults (-248, -342, 197, 9).

Helpers / constants
-------------------
local_to_stage(x, y, scale, facing, lx, ly); castor_height(growth); fish_mouth_points(mouth);
SHIP_DECK_Y, SHIP_INTERIOR, SHIP_BED, BOOTH_SEAT, CASTOR_SHADE, WORM_BITE_DX, FISH_COLORS.
Contact sheets of everything: ``python3 tools/props_sheet.py`` -> build/preview/props_*.png.
"""
import hashlib
import math
import random
import re

from art import style as S
from art.style import INK, P

# ====================================================================== helpers
EYE_WHITE = "#fbf6ea"
PUPIL = "#2e2630"
HILITE = "#fffaf0"
CREAM = "#f7efdc"

SHIP_DECK_Y = -165
SHIP_INTERIOR = (-360, -146, 360, 34)
SHIP_BED = (-130, 240, -4)
SHIP_SLEEP = (48, -2)
SHIP_HOLD_LANTERN = (200, -140)
BOOTH_SEAT = (-140, -250, 132, 0)
CASTOR_SHADE = (-180, 400)
CASTOR_BOOTH_DX = 270
WORM_BITE_DX = 52


def _f(v):
    return f"{v:.1f}"


def _clamp(v, a=0.0, b=1.0):
    return max(a, min(b, float(v)))


def _lerp(a, b, t):
    return a + (b - a) * t


def _lerp2(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _smooth(t):
    t = _clamp(t)
    return t * t * (3 - 2 * t)


def _uid(prefix, *parts):
    return f"pr-{prefix}-{hashlib.md5(repr(parts).encode()).hexdigest()[:10]}"


def _st(sw=4.0, color=INK):
    return f'stroke="{color}" stroke-width="{_f(sw)}" stroke-linejoin="round" stroke-linecap="round"'


def _p(d, fill="none", sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<path d="{d}" fill="{fill}" {s} {extra}/>'


def _sm(pts, closed=True, tension=1.0):
    return S.smooth_path(pts, closed, tension)


def _poly(pts, closed=True):
    d = "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in pts)
    return d + (" Z" if closed else "")


def _ell(cx, cy, rx, ry, fill, sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<ellipse cx="{_f(cx)}" cy="{_f(cy)}" rx="{_f(rx)}" ry="{_f(ry)}" fill="{fill}" {s} {extra}/>'


def _circ(cx, cy, r, fill, sw=4.0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" fill="{fill}" {s} {extra}/>'


def _rect(x, y, w, h, fill, sw=4.0, rx=0, stroke=INK, extra=""):
    s = _st(sw, stroke) if sw else ""
    return (f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(rx)}" '
            f'fill="{fill}" {s} {extra}/>')


def _line(x1, y1, x2, y2, sw=4.0, color=INK, extra=""):
    return f'<path d="M{_f(x1)},{_f(y1)} L{_f(x2)},{_f(y2)}" fill="none" {_st(sw, color)} {extra}/>'


def _tube(d, width, fill, sw=4.0, extra=""):
    """A rounded 'tube' along path data d: ink stroke underneath, coloured stroke on top."""
    return (f'<path d="{d}" fill="none" {_st(width + 2 * sw, INK)} {extra}/>'
            f'<path d="{d}" fill="none" {_st(width, fill)} {extra}/>')


def _rot(px, py, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))


def _g(body, tr=None, extra=""):
    t = f' transform="{tr}"' if tr else ""
    return f"<g{t} {extra}>{body}</g>"


def _upscale(body, k):
    """Scale geometry by k while keeping ink line widths unchanged (outlines stay 3-5 px)."""
    body = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) / k:.2f}"', body)
    return f'<g transform="scale({k})">{body}</g>'


def _clip(cid, d, body):
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{body}</g>'


def _place(body, x, y, scale=1.0, facing=1, rot=0.0, filt="wobble-fine"):
    """Put local markup (anchor at 0,0, facing right, scale 1) onto the stage."""
    sx = scale * (-1 if facing < 0 else 1)
    tr = f"translate({_f(x)},{_f(y)})"
    if rot:
        tr += f" rotate({rot:.2f})"
    tr += f" scale({sx:.4f},{scale:.4f})"
    inner = f'<g transform="{tr}">{body}</g>'
    return f'<g filter="url(#{filt})">{inner}</g>' if filt else inner


def local_to_stage(x, y, scale, facing, lx, ly):
    """Convert a point (lx, ly) given in a drawing's local scale-1 coordinates (relative to its
    anchor, facing right) to stage pixels for a drawing placed at (x, y, scale, facing)."""
    return (x + lx * scale * (-1 if facing < 0 else 1), y + ly * scale)


def _eye(cx, cy, r, kind="open", look=(0.35, 0.15), sw=4.0):
    """Big friendly eye. kind: open | closed | happy | surprised."""
    if kind == "closed":
        d = f"M{_f(cx - r)},{_f(cy)} Q{_f(cx)},{_f(cy + r * 0.85)} {_f(cx + r)},{_f(cy)}"
        out = _p(d, sw=sw * 1.25)
        for k in (-0.6, 0.0, 0.6):
            bx, by = cx + k * r * 0.95, cy + r * 0.38 * (1 - k * k * 0.6)
            out += _line(bx, by, bx + k * r * 0.25, by + r * 0.32, sw=sw * 0.8)
        return out
    if kind == "happy":
        d = f"M{_f(cx - r)},{_f(cy + r * 0.3)} Q{_f(cx)},{_f(cy - r * 0.95)} {_f(cx + r)},{_f(cy + r * 0.3)}"
        return _p(d, sw=sw * 1.3)
    if kind == "surprised":
        rr = r * 1.12
        out = _ell(cx, cy, rr * 0.95, rr * 1.08, EYE_WHITE, sw)
        out += _circ(cx + look[0] * r * 0.1, cy, r * 0.36, PUPIL, 0)
        out += _circ(cx + look[0] * r * 0.1 - r * 0.12, cy - r * 0.13, r * 0.12, HILITE, 0)
        return out
    out = _ell(cx, cy, r * 0.95, r * 1.05, EYE_WHITE, sw)
    ix, iy = cx + look[0] * r * 0.32, cy + look[1] * r * 0.3
    out += _circ(ix, iy, r * 0.62, PUPIL, 0)
    out += _circ(ix - r * 0.2, iy - r * 0.24, r * 0.22, HILITE, 0)
    out += _circ(ix + r * 0.22, iy + r * 0.2, r * 0.09, HILITE, 0)
    return out


def _dot_eye(cx, cy, r, kind="open"):
    """Small picture-book dot eye with a highlight (for little creatures and animals)."""
    if kind == "closed":
        return _p(f"M{_f(cx - r * 1.2)},{_f(cy)} Q{_f(cx)},{_f(cy + r * 1.1)} {_f(cx + r * 1.2)},{_f(cy)}",
                  sw=max(2.5, r * 0.55))
    if kind == "happy":
        return _p(f"M{_f(cx - r * 1.2)},{_f(cy + r * 0.4)} Q{_f(cx)},{_f(cy - r * 1.1)} "
                  f"{_f(cx + r * 1.2)},{_f(cy + r * 0.4)}", sw=max(2.5, r * 0.55))
    return _circ(cx, cy, r, PUPIL, 0) + _circ(cx - r * 0.3, cy - r * 0.35, r * 0.36, HILITE, 0)


def _blush(cx, cy, rx, ry, op=0.55):
    return _ell(cx, cy, rx, ry, P["cheek"], 0, extra=f'opacity="{op}"')


# ====================================================================== 1. the great fish

_FISH_LIP_U = [(272, 42), (345, 48), (430, 53), (518, 43), (588, 16)]      # closed mouth, corner -> tip
_FISH_LIP_L = [(272, 42), (345, 42), (430, 47), (518, 37), (596, 28)]
# wide-open targets (mouth=1): a rounded throat at the back, bowed lips, protruding rounded lip tips
_FISH_OPEN_U = [(214, 70), (216, 0), (236, -62), (284, -118), (352, -158), (430, -180), (500, -184), (556, -164)]
_FISH_OPEN_L = [(214, 70), (216, 138), (238, 202), (284, 254), (346, 290), (414, 310), (476, 314), (522, 296)]
_FISH_FORE = [((590, -40), (584, -192)), ((556, -122), (564, -238)), ((500, -200), (500, -284)),
              ((418, -252), (420, -312)), ((268, -296), (268, -326)), ((80, -315), (80, -322))]
_FISH_POUCH = [((598, 62), (524, 336)), ((570, 150), (486, 372)), ((486, 232), (410, 400)), ((380, 284), (322, 410)),
               ((268, 304), (238, 378)), ((205, 302), (196, 336))]
_FISH_US = (0.0, 0.07, 0.17, 0.3, 0.45, 0.6, 0.75, 0.88, 1.0)
_FISH_T = (178.0, 297.0)      # throat point where the lower jaw meets the belly


def _along(poly, u):
    """Point at fraction u (by arc length) along a polyline."""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:])]
    s = _clamp(u) * sum(segs)
    for i, ln in enumerate(segs):
        if s <= ln or i == len(segs) - 1:
            return _lerp2(poly[i], poly[i + 1], 0 if ln == 0 else min(1.0, s / ln))
        s -= ln
    return poly[-1]


def _fish_geom(mouth=0.0):
    """All mouth-dependent fish geometry (local coords, facing right)."""
    m = _clamp(mouth)
    e = m * m * (3 - 2 * m) * 0.35 + m * 0.65          # gentle ease, still moving at both ends
    up = [_lerp2(_along(_FISH_LIP_U, u), _along(_FISH_OPEN_U, u), e) for u in _FISH_US]
    lo = [_lerp2(_along(_FISH_LIP_L, u), _along(_FISH_OPEN_L, u), e) for u in _FISH_US]
    C, U, L = up[0], up[-1], lo[-1]
    fore = [_lerp2(a, b, e) for a, b in _FISH_FORE]
    chin = [_lerp2(a, b, e) for a, b in _FISH_POUCH]
    eye = _lerp2((380, -118), (340, -222), e)
    # the opening between the lip tips bows slightly inward, so the lips read as protruding
    mid = _lerp2(_lerp2(U, L, 0.5), C, 0.08 * e)
    front = [_lerp2(U, mid, 0.5), mid, _lerp2(mid, L, 0.5)] if m > 0.004 else []
    cavity = up + front + list(reversed(lo))[:-1]
    return dict(m=m, e=e, C=C, up=up, lo=lo, U=U, L=L, fore=fore, chin=chin, eye=eye, front=front,
                cavity=cavity)


def _fish_cavity_d(G):
    """Closed path of the dark mouth opening: spline lip edges joined by the (slightly bowed) front."""
    d_up = _sm(G["up"], closed=False)
    d_lo = _sm(list(reversed(G["lo"])), closed=False)
    if not G["front"]:
        return d_up + " Z"
    mid = G["front"][1]
    U, L = G["U"], G["L"]
    ctrl = (2 * mid[0] - (U[0] + L[0]) / 2, 2 * mid[1] - (U[1] + L[1]) / 2)
    return d_up + f" Q{_f(ctrl[0])},{_f(ctrl[1])} " + d_lo[1:] + " Z"


def _fish(mouth=0.0, eye="open", tail=0.0, blush=True, part="all"):
    G = _fish_geom(mouth)
    m = G["m"]
    tl = _clamp(tail, -1, 1)
    C, U, L = G["C"], G["U"], G["L"]
    body_col, dark, light, belly_col = P["fish"], P["fish_dark"], P["fish_light"], P["fish_belly"]
    fin_col = S.mix(body_col, light, 0.45)
    inside = P["mouth_inside"]
    back, front = "", ""

    # ---- outlines
    back_pts = [(-120, -297), (-300, -229), (-432, -133), (-506, -58)]
    belly = [(-514, 0), (-506, 58), (-432, 140), (-292, 232), (-110, 292), (60, 306)]
    body_line = G["up"] + G["fore"] + back_pts + belly + [_FISH_T]
    d_body_open = _sm(body_line, closed=False)
    d_body = d_body_open + " Z"
    jaw_line = G["lo"] + G["chin"] + [_FISH_T]
    d_jaw_open = _sm(jaw_line, closed=False)
    d_jaw = d_jaw_open + f" L{_f(_FISH_T[0] - 6)},{_f(_FISH_T[1] - 20)} L{_f(C[0] - 6)},{_f(C[1] + 6)} Z"

    # ---- tail fin (behind body), bends around the peduncle
    tail_pts = [(-430, -58), (-560, -150), (-672, -270), (-760, -330), (-788, -268), (-752, -130),
                (-690, 0), (-752, 130), (-788, 268), (-760, 330), (-672, 270), (-560, 150), (-430, 58)]
    td = _sm(tail_pts, closed=False) + " L-400,0 Z"
    rays = ""
    for a in (-62, -44, -26, -9, 9, 26, 44, 62):
        ex, ey = -470 - 250 * math.cos(math.radians(a)), 285 * math.sin(math.radians(a))
        rays += _line(-500, ey * 0.12, ex, ey, sw=3.5, color=dark, extra='opacity="0.45"')
    back += _g(_p(td, fin_col, 0) + _clip(_uid("fisht", 0), td, rays) + _p(td, sw=4.5), f"rotate({22 * tl:.2f} -470 0)")

    # ---- dorsal and anal fins (behind body)
    dors = [(-235, -262), (-196, -372), (-80, -452), (55, -446), (150, -372), (196, -292), (110, -260)]
    back += _p(_sm(dors, closed=False) + " Z", fin_col, 4.5)
    for i in range(6):
        bx = -200 + i * 66
        back += _line(bx, -300, bx + 6 + i * 4, -400 + abs(i - 2.5) * 18, sw=3.5, color=dark, extra='opacity="0.45"')
    anal = [(-170, 285), (-245, 342), (-330, 352), (-372, 300), (-300, 240)]
    back += _p(_sm(anal, closed=False) + " Z", fin_col, 4.5)

    # ---- inside of the mouth (dark throat, gums, tongue)
    d_cav = _fish_cavity_d(G)
    if m > 0.004:
        cid = _uid("fishm", round(m, 4))
        inner = _p(d_cav, inside, 0)
        deep = S.shade(inside, -0.5)
        thr = _lerp2(C, _lerp2(U, L, 0.5), 0.22)
        inner += _ell(thr[0], thr[1], 30 + 95 * m, 26 + 120 * m, deep, 0, extra='filter="url(#soft)" opacity="0.9"')
        gum = S.shade(inside, 0.25)
        inner += _p(_sm(G["up"], closed=False), sw=6 + 16 * m, stroke=gum, extra='opacity="0.55"')
        # tongue resting on the floor of the mouth (its lower half is hidden under the jaw by the clip)
        lo = G["lo"]
        top, bot = [], []
        for u in (0.1, 0.22, 0.36, 0.5, 0.64, 0.78, 0.9):
            p = _along(lo, u)
            q = _along(lo, min(1.0, u + 0.02))
            dx, dy = q[0] - p[0], q[1] - p[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = dy / ln, -dx / ln          # toward the inside of the mouth
            hgt = (10 + 62 * m) * math.sin(math.pi * (u - 0.04) / 0.92) ** 0.8
            top.append((p[0] + nx * hgt, p[1] + ny * hgt))
            bot.append((p[0] - nx * 30, p[1] - ny * 30))
        tc = "#e48a8c"
        inner += _p(_sm(top + list(reversed(bot)), closed=True, tension=0.8), tc, 3.5)
        groove = [_lerp2(top[i], _along(lo, u), 0.42) for i, u in ((1, 0.22), (2, 0.36), (3, 0.5), (4, 0.64), (5, 0.78))]
        inner += _p(_sm(groove, closed=False), sw=3, stroke=S.shade(tc, -0.3), extra='opacity="0.8"')
        inner += _ell(top[3][0] - 6, top[3][1] + 16, 22 + 18 * m, 7 + 5 * m, S.shade(tc, 0.35), 0,
                      extra=f'opacity="0.6" transform="rotate({_f(math.degrees(math.atan2(top[4][1] - top[2][1], top[4][0] - top[2][0])))} {_f(top[3][0] - 6)} {_f(top[3][1] + 16)})"')
        back += _clip(cid, d_cav, inner)

    # ---- body with clipped shading
    bid = _uid("fishb", round(m, 4))
    belly_shape = [(-540, 30), (-420, 110), (-260, 160), (-60, 185), (110, 172), (212, 122), (252, 80),
                   (278, 62), (330, 330), (-560, 330)]
    shade = _p(_sm(belly_shape, closed=True), belly_col, 0)
    shade += _p(_sm([(140, 168), (-60, 186), (-260, 162), (-420, 112)], closed=False), sw=3.5,
                stroke=S.shade(belly_col, -0.15), extra='opacity="0.7"')
    back_shape = [(-540, -40), (-330, -170), (-80, -238), (200, -236), (420, -190), (520, -130), (520, -420),
                  (-540, -420)]
    shade += _p(_sm(back_shape, closed=True), dark, 0, extra='filter="url(#soft)" opacity="0.75"')
    shade += _ell(40, -150, 230, 38, light, 0, extra='filter="url(#soft)" opacity="0.38" transform="rotate(-6 40 -150)"')
    for row, yy in enumerate((-175, -100, -25, 50)):
        for k in range(8):
            xx = -400 + k * 66 + (33 if row % 2 else 0)
            if xx > 130 - abs(yy) * 0.15:
                continue
            op = 0.32 if yy < 40 else 0.22
            shade += _p(f"M{_f(xx)},{_f(yy - 30)} Q{_f(xx - 34)},{_f(yy)} {_f(xx)},{_f(yy + 30)}", sw=3.5,
                        stroke=dark, extra=f'opacity="{op}"')
    for sx, sy, sr in ((-60, -232, 22), (40, -262, 15), (-185, -205, 18), (125, -222, 13), (-300, -150, 14),
                       (-105, -165, 11), (225, -250, 12), (-385, -92, 10), (-235, -118, 9), (300, -205, 9)):
        shade += _circ(sx, sy, sr, P["fish_spot"], 0, extra='opacity="0.95"')
    body_fill = _p(d_body, body_col, 0) + _clip(bid, d_body, shade)
    back += body_fill + _p(d_body_open, sw=4.5)

    # ---- face (on the head, always above the mouth)
    ec = G["eye"]
    face = ""
    if eye == "surprised":
        face += _p(f"M{_f(ec[0] - 60)},{_f(ec[1] - 112)} Q{_f(ec[0])},{_f(ec[1] - 150)} {_f(ec[0] + 58)},{_f(ec[1] - 108)}",
                   sw=5)
    face += _eye(ec[0], ec[1], 64, eye, look=(0.55, 0.1), sw=4.5)
    if blush:
        bl = _lerp2((ec[0] + 34, ec[1] + 98), (ec[0] - 78, ec[1] + 62), G["e"])
        face += _blush(bl[0], bl[1], 48, 24, 0.8)
    back += face

    # ---- FRONT: lower jaw + pouch, gill, pectoral fin, upper-lip rim and the ink over the mouth
    jid = _uid("fishj", round(m, 4))
    lo = G["lo"]
    band = []
    for i, p in enumerate(lo):
        q0, q1 = lo[max(0, i - 1)], lo[min(len(lo) - 1, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        band.append((p[0] - dy / ln * 34, p[1] + dx / ln * 34))   # 34 px into the jaw
    jaw_detail = _p(_sm(lo + list(reversed(band)), closed=True, tension=0.8), S.mix(body_col, light, 0.15), 0)
    jaw_detail += _p(_sm(band, closed=False), sw=3, stroke=S.shade(belly_col, -0.12), extra='opacity="0.6"')
    front += _p(d_jaw, belly_col, 0) + _clip(jid, d_jaw, jaw_detail)
    # upper-lip rim: the body (with its shading) re-drawn in a band along the upper lip, so anything placed
    # between part='back' and part='front' slips under the lip
    mid_ = _uid("fishrim", round(m, 4))
    d_up = _sm(G["up"], closed=False)
    front += (f'<mask id="{mid_}" maskUnits="userSpaceOnUse" x="-1200" y="-1200" width="2400" height="2400">'
              f'<path d="{d_up}" fill="none" stroke="#ffffff" stroke-width="{_f(26 + 12 * m)}" stroke-linecap="round"/>'
              f'</mask><g mask="url(#{mid_})">{body_fill}</g>')
    front += _p(d_jaw_open, sw=4.5) + _p(d_up, sw=4.5)
    # gill line (slides back as the mouth opens) and pectoral fin
    e = G["e"]
    front += _p(f"M{_f(236 - 8 * e)},-205 Q{_f(160 - 40 * e)},-30 {_f(222 - 50 * e)},168", sw=4.5)
    front += _p(f"M{_f(205 - 8 * e)},-150 Q{_f(150 - 40 * e)},-30 {_f(196 - 46 * e)},110", sw=3, stroke=dark,
                extra='opacity="0.4"')
    pb = (182, 104)
    fan = [(196, 70), (120, 60), (40, 92), (6, 140), (24, 176), (70, 182), (120, 160), (176, 136)]
    fan_rays = ""
    for q in ((45, 98), (25, 140), (55, 172), (110, 160)):
        fan_rays += _line(170, 104, q[0] + 10, q[1] - 4, sw=3, color=dark, extra='opacity="0.5"')
    front += _g(_p(_sm(fan, closed=True), fin_col, 4.5) + fan_rays,
                f"translate({_f(-30 * e)},{_f(10 * e)}) rotate({-10 * tl:.2f} {pb[0]} {pb[1]})")
    if m < 0.5:  # little smile crease at the corner of the mouth
        a = 1 - m * 2
        front += _p(f"M{_f(C[0] + 8)},{_f(C[1] - 20)} Q{_f(C[0] - 14)},{_f(C[1] - 2)} {_f(C[0] + 4)},{_f(C[1] + 14)}",
                    sw=4.5, extra=f'opacity="{a:.2f}"')
    if part == "back":
        return back
    if part == "front":
        return front
    return back + front


def fish_mouth_points(mouth=0.0):
    """Local (scale 1, facing right) key points of the fish mouth for a given mouth value:
    {'corner', 'upper', 'lower', 'center', 'box'} — corner = back of the mouth, upper/lower = lip tips,
    center = middle of the dark opening (aim swallowed things here), box = largest axis-aligned rectangle
    (x0, y0, x1, y1) inside the dark opening. Convert points with local_to_stage()."""
    G = _fish_geom(mouth)
    box = _fish_mouth_box(round(G["m"], 3))
    c = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2) if box[2] > box[0] else _lerp2(_lerp2(G["U"], G["L"], 0.5),
                                                                                         G["C"], 0.3)
    return {"corner": G["C"], "upper": G["U"], "lower": G["L"], "center": c, "box": box}


_BOX_CACHE = {}


def _fish_mouth_box(m):
    """Largest axis-aligned rectangle inside the cavity polygon (8 px grid, 6 px margin)."""
    if m in _BOX_CACHE:
        return _BOX_CACHE[m]
    G = _fish_geom(m)
    poly = []
    cav = G["cavity"]
    for i in range(len(cav)):
        for k in range(4):
            poly.append(_lerp2(cav[i], cav[(i + 1) % len(cav)], k / 4))
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    step, mg = 8.0, 6.0
    x0, y0 = min(xs), min(ys)
    nx, ny = int((max(xs) - x0) / step) + 1, int((max(ys) - y0) / step) + 1
    if nx < 2 or ny < 2:
        _BOX_CACHE[m] = (G["C"][0], G["C"][1], G["C"][0], G["C"][1])
        return _BOX_CACHE[m]

    def inside(px, py):
        c = False
        n = len(poly)
        for i in range(n):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % n]
            if (ay > py) != (by > py) and px < ax + (py - ay) * (bx - ax) / (by - ay):
                c = not c
        return c
    grid = [[inside(x0 + i * step, y0 + j * step) for i in range(nx)] for j in range(ny)]
    best, hts = (0, None), [0] * nx
    for j in range(ny):
        for i in range(nx):
            hts[i] = hts[i] + 1 if grid[j][i] else 0
        stack = []
        for i in range(nx + 1):
            h = hts[i] if i < nx else 0
            start = i
            while stack and stack[-1][1] >= h:
                si, sh_ = stack.pop()
                area = sh_ * (i - si)
                if area > best[0]:
                    best = (area, (si, j - sh_ + 1, i - 1, j))
                start = si
            stack.append((start, h))
    if best[1] is None:
        r = (G["C"][0], G["C"][1], G["C"][0], G["C"][1])
    else:
        i0, j0, i1, j1 = best[1]
        r = (x0 + i0 * step + mg, y0 + j0 * step + mg, x0 + i1 * step - mg, y0 + j1 * step - mg)
    r = tuple(round(v) for v in r)
    _BOX_CACHE[m] = r
    return r


def fish_mouth_path(mouth=1.0, x=0.0, y=0.0, scale=1.0, facing=1, reach=1600.0):
    """Clip path data (stage px for a fish drawn at x, y, scale, facing) of everything a swallowed / spat-out
    figure may show through: the dark mouth opening plus the open water in front of the lips (the half-plane
    beyond the line from the upper to the lower lip tip, `reach` px deep). The head, cheeks and jaws are
    outside it. Use with in_fish_mouth() or your own <clipPath>."""
    G = _fish_geom(mouth)
    U, L = G["U"], G["L"]
    dx, dy = L[0] - U[0], L[1] - U[1]
    ln = math.hypot(dx, dy)
    if ln < 1e-3:
        dx, dy, ln = 8.0, 12.0, math.hypot(8.0, 12.0)
    c = (dx / ln, dy / ln)                 # along the opening, top -> bottom
    n = (c[1], -c[0])                      # forward, out of the mouth
    R = reach
    far = [(U[0] - c[0] * R, U[1] - c[1] * R), (U[0] - c[0] * R + n[0] * R, U[1] - c[1] * R + n[1] * R),
           (L[0] + c[0] * R + n[0] * R, L[1] + c[1] * R + n[1] * R), (L[0] + c[0] * R, L[1] + c[1] * R)]
    pts = []
    for seg in (G["up"], far, list(reversed(G["lo"]))):
        pts += seg
    sx = scale * (-1 if facing < 0 else 1)
    return _poly([(x + px * sx, y + py * scale) for px, py in pts])


def in_fish_mouth(markup, x, y, scale=1.0, facing=1, mouth=1.0):
    """Wrap figure markup in a clip so it only shows inside the fish's mouth / in front of it. Draw
    fish(..., part='back') -> in_fish_mouth(jonah(...), same x, y, scale, facing, mouth) -> fish(..., part='front')."""
    cid = _uid("inmouth", round(x, 2), round(y, 2), scale, facing, round(_clamp(mouth), 4))
    return (f'<clipPath id="{cid}"><path d="{fish_mouth_path(mouth, x, y, scale, facing)}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{markup}</g>')


def fish(x, y, scale=1.0, facing=1, mouth=0.0, eye="open", tail=0.0, blush=True, part="all"):
    return _place(_fish(mouth, eye, tail, blush, part), x, y, scale, facing)



# ====================================================================== 2. the ship


def _hull_top(x):
    return -165 - 75 * (abs(x) / 480) ** 3.2


def _hull_bot(x):
    return 96 - 250 * (abs(x) / 490) ** 3.5


def _sail_pt(u, v, kind):
    """Point on the square sail surface (u: 0 stern edge .. 1 bow edge, v: 0 yard .. 1 foot)."""
    if kind == "torn":
        xl = -300 - 18 * math.sin(math.pi * v)
        xr = 280 + 22 * math.sin(math.pi * v)
        yb = -585 + 30 * math.sin(math.pi * u)
    else:
        xl = -300 - 46 * math.sin(math.pi * v) ** 0.9
        xr = 280 + 74 * math.sin(math.pi * v) ** 0.8
        yb = -548 + 74 * math.sin(math.pi * u) ** 0.9
    return (_lerp(xl, xr, u), _lerp(-842, yb, v))


def _sail(kind, sid):
    out = ""
    yard = "M-318,-848 Q-10,-866 298,-848"
    if kind == "furled":
        pts = []
        for i in range(13):
            u = i / 12
            pts.append((_lerp(-292, 272, u), -840 + 46 + 12 * math.sin(i * 1.9) - 10 * (u * (1 - u) < 0.03)))
        out += _p(_sm([(-296, -846)] + [(p[0], p[1] - 2) for p in pts[1:-1]] + [(276, -846)], closed=True),
                  P["sail"], 4)
        for i in range(1, 12, 2):
            u = i / 12
            xx = _lerp(-292, 272, u)
            out += _p(f"M{_f(xx - 14)},{_f(-842)} Q{_f(xx)},{_f(-822)} {_f(xx + 12)},{_f(-842)}", sw=2.5,
                      stroke=S.shade(P["sail"], -0.35))
        for xx in (-210, -60, 90, 220):
            out += _rect(xx - 7, -852, 14, 46, P["wood_light"], 3, rx=5)
        out = _tube(yard, 14, P["wood"]) + out
        return out
    # surface outline
    n = 14
    left = [_sail_pt(0, i / n, kind) for i in range(n + 1)]
    bottom = [_sail_pt(i / n, 1, kind) for i in range(n + 1)]
    right = [_sail_pt(1, 1 - i / n, kind) for i in range(n + 1)]
    top = [_sail_pt(1 - i / n, 0, kind) for i in range(n + 1)]
    if kind == "torn":
        rng = random.Random(4)
        tb = [0, 26, -8, 38, 4, 18, -14, 44, 10, 30, -6, 52, 0, 22, 0]
        bottom = [(px + rng.uniform(-8, 8), py + tb[i]) for i, (px, py) in enumerate(bottom)]
        tr_ = [0, -40, 6, -18, 16, -52, 0, -10, 14, -34, -4, -22, 8, 0, 0]
        right = [(px + tr_[i], py) for i, (px, py) in enumerate(right)]
        outline = _poly(left[:-1] + bottom + right[1:] + top[1:-1])
    else:
        outline = _sm(left[:-1] + bottom + right[1:] + top[1:-1], closed=True, tension=0.6)
    hole = ""
    if kind == "torn":
        hc = _sail_pt(0.62, 0.48, kind)
        hp = [(hc[0] - 50, hc[1] - 6), (hc[0] - 22, hc[1] - 30), (hc[0] - 4, hc[1] - 12), (hc[0] + 30, hc[1] - 40),
              (hc[0] + 40, hc[1] - 8), (hc[0] + 22, hc[1] + 4), (hc[0] + 30, hc[1] + 30), (hc[0] - 2, hc[1] + 22),
              (hc[0] - 30, hc[1] + 34)]
        hole = " " + _poly(hp)
    stripes = ""
    for u0, u1 in ((1 / 7, 2 / 7), (3 / 7, 4 / 7), (5 / 7, 6 / 7)):
        a = [_sail_pt(u0, i / n, kind) for i in range(n + 1)]
        b = [_sail_pt(u1, 1 - i / n, kind) for i in range(n + 1)]
        a[-1] = (a[-1][0], a[-1][1] + 60)
        b[0] = (b[0][0], b[0][1] + 60)
        stripes += _p(_poly(a + b), P["sail_stripe"], 0)
    shade = _p(_poly([_sail_pt(0, i / n, kind) for i in range(n + 1)] +
                     [_sail_pt(0.28, 1 - i / n, kind) for i in range(n + 1)]),
               S.shade(P["sail"], -0.25), 0, extra='filter="url(#soft)" opacity="0.55"')
    shade += _p(_poly([_sail_pt(0.62, i / n, kind) for i in range(n + 1)] +
                      [_sail_pt(0.9, 1 - i / n, kind) for i in range(n + 1)]),
                HILITE, 0, extra='filter="url(#soft)" opacity="0.2"')
    if kind == "full":   # wind-filled belly: shadow under the curve of the foot, a soft light band above
        belly = [_sail_pt(i / n, 0.68 + 0.1 * math.sin(math.pi * i / n), kind) for i in range(n + 1)]
        foot = [_sail_pt(1 - i / n, 1.05, kind) for i in range(n + 1)]
        shade += _p(_sm(belly, closed=False, tension=0.8) + " L" + _poly(foot)[1:], S.shade(P["sail"], -0.3), 0,
                    extra='filter="url(#soft)" opacity="0.45"')
        lit = [_sail_pt(i / n, 0.3 + 0.12 * math.sin(math.pi * i / n), kind) for i in range(n + 1)]
        lit2 = [_sail_pt(1 - i / n, 0.46 + 0.14 * math.sin(math.pi * i / n), kind) for i in range(n + 1)]
        shade += _p(_poly(lit + lit2), HILITE, 0, extra='filter="url(#soft)" opacity="0.35"')
        shade += _p(_sm([_sail_pt(i / n, 0.62 + 0.12 * math.sin(math.pi * i / n), kind) for i in range(1, n)],
                        closed=False), sw=3, stroke=S.shade(P["sail"], -0.4), extra='opacity="0.35"')
    seams = ""
    for v in (0.33, 0.66):
        pts = [_sail_pt(i / n, v, kind) for i in range(n + 1)]
        seams += _p(_sm(pts, closed=False), sw=2.5, stroke=S.shade(P["sail"], -0.4), extra='opacity="0.6"')
    body = _p(outline + hole, P["sail"], 0, extra='fill-rule="evenodd"')
    inner = stripes + shade + seams
    out += body + f'<clipPath id="{sid}"><path d="{outline + hole}" clip-rule="evenodd"/></clipPath>'
    out += f'<g clip-path="url(#{sid})">{inner}</g>'
    out += _p(outline + hole, sw=4.5, extra='fill-rule="evenodd"')
    if kind == "torn":
        bc = _sail_pt(0.93, 0.93, kind)
        flap = [(bc[0] - 60, bc[1] - 10), (bc[0] - 10, bc[1] - 30), (bc[0] + 60, bc[1] - 6), (bc[0] + 120, bc[1] + 20),
                (bc[0] + 150, bc[1] + 8), (bc[0] + 128, bc[1] + 46), (bc[0] + 92, bc[1] + 40), (bc[0] + 70, bc[1] + 64),
                (bc[0] + 30, bc[1] + 42), (bc[0] - 30, bc[1] + 40)]
        out += _p(_poly(flap), S.shade(P["sail"], -0.1), 4)
        out += _p(_poly([(bc[0] + 4, bc[1] - 22), (bc[0] + 44, bc[1] - 10), (bc[0] + 38, bc[1] + 44), (bc[0] + 4, bc[1] + 42)]),
                  P["sail_stripe"], 0, extra='opacity="0.9"')
    out = _tube(yard, 14, P["wood"]) + out
    for xx in (-200, -60, 80, 210):
        tp = _sail_pt((xx + 300) / 580, 0, kind)
        out += _circ(tp[0], tp[1] + 2, 6, P["wood_light"], 3)
    return out


def _amphora(rot=0.0, col=None, s=1.0):
    col = col or P["terracotta"]
    body = [(0, -70), (22, -64), (38, -40), (40, -5), (30, 34), (12, 62), (0, 74), (-12, 62), (-30, 34), (-40, -5),
            (-38, -40), (-22, -64)]
    out = ""
    for sx in (-1, 1):      # loop handles standing out beside the neck, joining the shoulders
        hd = f"M{sx * 13},-72 C{sx * 46},-78 {sx * 58},-56 {sx * 36},-40"
        out += _p(hd, sw=13, stroke=INK) + _p(hd, sw=6, stroke=col)
    out += _p(_sm(body, closed=True), col, 4)
    out += _rect(-15, -84, 30, 20, col, 4, rx=4)
    out += _ell(0, -84, 17, 5, S.shade(col, -0.3), 3)
    out += _p("M-37,-18 Q0,-8 37,-18", sw=7, stroke=CREAM, extra='opacity="0.85"')
    out += _p("M-39,4 Q-26,10 -13,4 Q0,-2 13,4 Q26,10 39,4", sw=3, stroke=S.shade(col, -0.35))
    out += _ell(-16, -30, 7, 18, HILITE, 0, extra='opacity="0.35"')
    return _g(out, f"rotate({rot:.1f}) scale({s})")


def _sack(s=1.0, col=None, seed=0):
    col = col or P["sackcloth"]
    r = random.Random(seed)
    j = lambda v: v + r.uniform(-4, 4)  # noqa: E731
    pts = [(j(-24), -84), (j(-44), -64), (j(-54), -30), (j(-50), -4), (0, 2), (j(50), -4), (j(54), -30), (j(44), -64),
           (j(24), -84)]
    out = _p(_sm(pts, closed=False) + " L14,-90 L-14,-90 Z", col, 4)
    out += _p("M-26,-94 Q-34,-118 -16,-114 Q-6,-126 2,-112 Q14,-124 22,-110 Q36,-114 26,-94 Z", col, 4)
    out += _p("M-24,-90 Q0,-82 24,-90", sw=7, stroke=P["wood_light"]) + _p("M-24,-90 Q0,-82 24,-90", sw=2.5)
    for k in range(-2, 3):
        out += _p(f"M{k * 18},-70 Q{k * 20 + 3},-40 {k * 19},-8", sw=2.5, stroke=S.shade(col, -0.25),
                  extra='opacity="0.5"')
    out += _ell(14, -40, 13, 11, S.shade(col, 0.25), 2.5, extra='opacity="0.9"')
    return _g(out, f"scale({s})")


def _crate(s=1.0):
    out = _p("M-50,-40 L-34,-56 L66,-56 L50,-40 Z", P["wood_light"], 4)
    out += _p("M50,-40 L66,-56 L66,30 L50,46 Z", P["wood_dark"], 4)
    out += _rect(-50, -40, 100, 86, P["wood"], 4, rx=3)
    for yy in (-12, 17):
        out += _line(-46, yy, 46, yy, sw=3, color=P["wood_dark"])
    out += _rect(-50, -40, 100, 86, "none", 4, rx=3)
    out += _p("M-42,38 L42,-32", sw=13, stroke=INK) + _p("M-42,38 L42,-32", sw=6, stroke=P["wood_light"])
    for cx, cy in ((-42, -32), (42, -32), (-42, 38), (42, 38)):
        out += _circ(cx, cy, 3, INK, 0)
    return _g(out, f"scale({s})")


def _lantern_body(lit=True, glow=True, gid="lg"):
    """Hanging lantern, hook at (0,0), about 54 x 132."""
    out = ""
    if lit and glow:
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.85), (0.4, P["gold"], 0.35), (1, P["gold"], 0)])}</defs>'
                f'<circle cx="0" cy="88" r="120" fill="url(#{gid})"/>')
    out += _circ(0, 8, 8, "none", 3.5)
    out += _line(0, 16, 0, 34, sw=3.5)
    out += _p("M-24,52 Q-24,32 0,30 Q24,32 24,52 Z", P["wood_dark"], 4)
    win = P["glow"] if lit else S.mix(P["sand"], P["ink"], 0.3)
    out += _rect(-22, 52, 44, 60, win, 4, rx=6)
    if lit:
        out += _ell(0, 90, 9, 14, P["sun_hot"], 0) + _ell(0, 93, 5, 8, P["glow"], 0)
    out += _line(-8, 54, -8, 110, sw=3, color=P["wood_dark"]) + _line(8, 54, 8, 110, sw=3, color=P["wood_dark"])
    out += _rect(-27, 110, 54, 12, P["wood_dark"], 4, rx=4)
    out += _p("M-12,122 L0,134 L12,122", P["wood_dark"], 3.5)
    return out


def _rope_coil(s=1.0, col=None):
    col = col or S.mix(P["sackcloth"], P["sand"], 0.4)
    dark = S.shade(col, -0.35)
    out = ""
    for ry, rx, cy in ((15, 56, -15), (15, 50, -33), (14, 42, -49)):
        out += _ell(0, cy, rx, ry, col, 4)
        out += _ell(0, cy - 3, rx - 13, ry - 7, S.shade(col, -0.15), 3)
        for k in range(9):
            a = math.pi * (0.1 + 0.8 * k / 8)
            px, py = rx * math.cos(a), cy + ry * math.sin(a)
            out += _line(px - 4, py - 6, px + 4, py + 4, sw=2.5, color=dark, extra='opacity="0.7"')
    out += _p("M30,-52 Q58,-64 62,-40 Q66,-14 84,-6", sw=13, stroke=INK) + _p("M30,-52 Q58,-64 62,-40 Q66,-14 84,-6",
                                                                             sw=6, stroke=col)
    return _g(out, f"scale({s})")


def _ship(sail="full", cutaway=False, lantern=True, oars=False, part="all", flag=True, rig=4.0):
    back, front = "", ""
    wood, wd, wl = P["wood"], P["wood_dark"], P["wood_light"]
    # ---- rigging behind the sail
    mast_top = (-10, -930)
    stay_c = S.shade(INK, 0.15)
    back += _line(mast_top[0], mast_top[1] + 10, 505, -352, sw=rig, color=stay_c)
    back += _line(mast_top[0], mast_top[1] + 10, -478, -420, sw=rig, color=stay_c)
    # pennant
    if flag:
        fl = "M-10,-922 Q30,-948 70,-930 Q100,-918 128,-934 Q104,-906 72,-912 Q36,-918 -10,-900 Z"
        back += _p(fl, P["sail_stripe"], 4)
    back += _tube("M-10,-170 L-10,-930", 18, wood)
    back += _ell(-10, -930, 18, 9, wd, 4)
    tilt = -6 if sail == "torn" else 0
    sid = _uid("sail", sail)
    back += _g(_sail(sail, sid), f"rotate({tilt} -10 -850)")
    # sheets
    if sail != "furled":
        bl, br = _sail_pt(0, 1, sail), _sail_pt(1, 1, sail)
        if sail == "torn":
            bl = _rot(bl[0], bl[1], -10, -850, tilt)
            br = _rot(br[0], br[1], -10, -850, tilt)
        back += _line(bl[0], bl[1], -360, -200, sw=rig, color=stay_c)
        back += _line(br[0], br[1], 380, -205, sw=rig, color=stay_c)
    # ---- hull
    xs = [-480 + i * 20 for i in range(49)]
    top = [(x, _hull_top(x)) for x in xs]
    hull_pts = top + [(503, -196), (494, -136), (466, -72), (418, -14), (340, 40), (200, 80), (0, 96), (-200, 82),
                      (-350, 42), (-430, -14), (-478, -80), (-500, -146), (-505, -204)]
    hull_d = _sm(hull_pts, closed=True, tension=0.5)
    hid = _uid("hull", 1)
    hull_in = _rect(-520, -10, 1040, 140, S.mix(wd, P["sea_deep"], 0.15), 0)
    hull_in += _p(_poly([(x, _hull_top(x) + 2) for x in xs] + [(x, _hull_top(x) + 32) for x in reversed(xs)]),
                  wl, 0)
    hull_in += _p(_poly([(x, _hull_top(x) + 44) for x in xs] + [(x, _hull_top(x) + 64) for x in reversed(xs)]),
                  P["jonah_sash"], 0)
    tri = ""
    for x in range(-440, 460, 44):
        yy = _hull_top(x) + 44
        tri += _poly([(x - 12, yy), (x + 12, yy), (x, yy + 18)]) + " "
    hull_in += _p(tri, P["sail_stripe"], 0)
    for t in (0.26, 0.44, 0.62, 0.8):
        pts = [(x, _lerp(_hull_top(x) + 64, _hull_bot(x), t)) for x in xs]
        hull_in += _p(_sm(pts, closed=False), sw=3, stroke=wd, extra='opacity="0.75"')
    hull_in += _p(_sm([(x, _hull_top(x) + 32) for x in xs], closed=False), sw=3, stroke=wd)
    hull_in += _p(_sm([(x, _hull_top(x) + 64) for x in xs], closed=False), sw=3, stroke=S.shade(P["jonah_sash"], -0.4))
    rng = random.Random(3)
    for _ in range(26):
        x = rng.uniform(-430, 430)
        t = rng.choice((0.35, 0.53, 0.71))
        y0 = _lerp(_hull_top(x) + 64, _hull_bot(x), t)
        hull_in += _circ(x, y0, 2.6, wd, 0, extra='opacity="0.8"')
    hull_in += _ell(-60, -60, 360, 30, HILITE, 0, extra='filter="url(#soft)" opacity="0.18"')
    hull = _p(hull_d, wood, 0) + _clip(hid, hull_d, hull_in) + _p(hull_d, sw=4.5)
    # posts
    bow = "M474,-222 Q500,-262 508,-306 Q512,-340 490,-356"
    stern = ("M-474,-222 Q-504,-268 -512,-330 Q-520,-392 -478,-420 Q-436,-438 -418,-400 Q-404,-366 -436,-356 "
             "Q-462,-350 -458,-376")
    posts = _tube(bow, 22, wood) + _circ(488, -358, 14, wl, 4)
    posts += _tube(stern, 24, wood)
    posts += _p("M-498,-300 Q-500,-370 -470,-404", sw=4, stroke=wl, extra='opacity="0.8"')
    if cutaway:
        back += hull + _ship_interior(lantern) + posts
    else:
        back += hull + posts
    # ---- rail and shields (in front of standing people)
    rail = ""
    for x in range(-400, 440, 40):
        yt = _hull_top(x)
        rail += _line(x, yt, x, yt - 52, sw=5, color=INK) + _line(x, yt, x, yt - 52, sw=2, color=wl)
    rail += _tube(_sm([(x, _hull_top(x) - 54) for x in range(-410, 450, 40)], closed=False), 8, wl, 3.5)
    cols = (P["terracotta"], P["sail"], P["jonah_sash"], P["gold"])
    for i, x in enumerate(range(-330, 360, 66)):
        cy = _hull_top(x) - 30
        c = cols[i % 4]
        rail += _circ(x, cy, 27, c, 4)
        rail += _circ(x, cy, 17, "none", 2.5, stroke=S.shade(c, -0.3))
        rail += _circ(x, cy, 6, S.shade(c, -0.25), 3)
    front += rail
    # steering oar (stern, near side)
    so = "M-372,-262 L-548,72"
    front += _tube(so, 13, wl)
    front += _p("M-520,10 Q-530,-12 -548,-6 L-600,106 Q-590,128 -566,122 Z", wl, 4)
    front += _rect(-394, -284, 52, 16, wd, 4, rx=6, extra="transform='rotate(-25 -372 -276)'")
    if oars:
        for x in range(-280, 320, 85):
            y0 = _hull_top(x) + 64
            d = f"M{x},{y0} L{x - 110},{y0 + 210}"
            front += _circ(x, y0, 9, wd, 3.5)
            front += _tube(d, 9, wl, 3.5)
            front += _p(f"M{x - 96},{y0 + 176} L{x - 132},{y0 + 250} Q{x - 124},{y0 + 262} {x - 110},{y0 + 254} "
                        f"L{x - 88},{y0 + 182} Z", wl, 3.5)
    if lantern and not cutaway:
        front += _g(_lantern_body(True, True, _uid("shiplan", 0)), "translate(-428,-372) scale(0.85)")
    elif lantern and cutaway:
        front += _g(_lantern_body(True, False, _uid("shiplan", 1)), "translate(-428,-372) scale(0.85)")
    if part == "back":
        return back
    if part == "front":
        return front
    return back + front


def _ship_interior(lantern=True):
    x0, y0, x1, y1 = SHIP_INTERIOR
    wd, wood, wl = P["wood_dark"], P["wood"], P["wood_light"]
    d = (f"M{x0},{y0} L{x1},{y0} L{x1},-20 Q{x1 - 8},{y1} {x1 - 110},{y1} L{x0 + 110},{y1} "
         f"Q{x0 + 8},{y1} {x0},-20 Z")
    wall = S.mix(wd, wood, 0.25)
    inner = _rect(x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20, wall, 0)
    for yy in range(y0 + 26, y1, 28):
        inner += _line(x0, yy, x1, yy, sw=3, color=S.shade(wd, -0.25), extra='opacity="0.6"')
    for xx in range(x0 + 60, x1, 120):
        inner += _p(f"M{xx - 10},{y0} Q{xx + 8},{(y0 + y1) / 2} {xx - 6},{y1}", sw=20, stroke=INK)
        inner += _p(f"M{xx - 10},{y0} Q{xx + 8},{(y0 + y1) / 2} {xx - 6},{y1}", sw=13, stroke=S.mix(wood, wd, 0.3))
    # deck beams
    inner += _rect(x0 - 10, y0 - 4, x1 - x0 + 20, 20, S.shade(wd, -0.15), 0)
    for xx in range(x0 + 30, x1, 90):
        inner += _rect(xx - 10, y0 + 6, 20, 16, wood, 3, rx=2)
    # floor
    inner += _rect(x0, y1 - 16, x1 - x0, 30, wl, 3.5)
    for xx in range(x0 + 40, x1, 70):
        inner += _line(xx, y1 - 14, xx - 6, y1 + 10, sw=2.5, color=wd, extra='opacity="0.6"')
    # warm glow
    gid = _uid("holdglow", 0)
    lx_ = SHIP_HOLD_LANTERN[0]
    inner += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.8), (0.5, P["gold"], 0.3), (1, P["gold"], 0)])}</defs>'
              f'<ellipse cx="{lx_ - 140}" cy="-70" rx="420" ry="220" fill="url(#{gid})"/>')
    # bed: straw mat, folded blanket, pillow
    bx0, bx1, by = SHIP_BED
    inner += _rect(bx0 - 6, by + 12, bx1 - bx0 + 12, y1 - 16 - by - 12, P["wood"], 3.5, rx=3)
    inner += _p(f"M{bx0},{by + 14} Q{bx0 - 4},{by} {bx0 + 14},{by - 2} L{bx1 - 14},{by - 2} Q{bx1 + 4},{by} {bx1},{by + 14} Z",
                S.mix(P["sackcloth"], P["sand"], 0.5), 3.5)
    for xx in range(bx0 + 20, bx1, 26):
        inner += _line(xx, by + 1, xx - 2, by + 12, sw=2, color=P["sackcloth_dark"], extra='opacity="0.6"')
    inner += _p(f"M{bx0 + 6},{by + 2} Q{bx0 - 4},{by - 30} {bx0 + 30},{by - 34} Q{bx0 + 70},{by - 38} "
                f"{bx0 + 76},{by - 12} Q{bx0 + 76},{by + 4} {bx0 + 50},{by + 4} Z", P["headcloth"], 3.5)
    inner += _p(f"M{bx1 - 70},{by + 2} Q{bx1 - 78},{by - 24} {bx1 - 50},{by - 26} L{bx1 - 6},{by - 22} "
                f"Q{bx1 + 6},{by - 8} {bx1 - 4},{by + 2} Z", P["jonah_sash"], 3.5)
    inner += _line(bx1 - 62, by - 14, bx1 - 10, by - 12, sw=2.5, color=S.shade(P["jonah_sash"], -0.4))
    # cargo
    fl = y1 - 16
    inner += _g(_amphora(-8), f"translate(-318,{fl - 64}) scale(0.9)")
    inner += _g(_amphora(6, S.mix(P["terracotta"], P["sand"], 0.35)), f"translate(-254,{fl - 64}) scale(0.85)")
    inner += _g(_sack(0.8, seed=2), f"translate(-190,{fl})")
    inner += _g(_crate(0.85), f"translate(300,{fl - 39})")
    inner += _g(_sack(0.72, seed=5), f"translate(296,{fl - 74})")
    if lantern:   # hangs toward the bow, clear of a sleeper's head on the pillow
        lx_, ly_ = SHIP_HOLD_LANTERN
        inner += _line(lx_, y0 + 12, lx_, ly_ + 4, sw=3)
        inner += _g(_lantern_body(True, False), f"translate({lx_},{ly_}) scale(0.48)")
    cid = _uid("hold", 0)
    out = _clip(cid, d, inner)
    out += _p(d, sw=22) + _p(d, sw=12, stroke=wl)
    return out


def ship(x, y, scale=1.0, facing=1, sail="full", cutaway=False, lantern=True, oars=False, part="all", flag=True):
    rig = max(4.0, 2.6 / max(scale, 0.05))      # stays / sheets never thinner than ~2.6 px on screen
    return _place(_ship(sail, cutaway, lantern, oars, part, flag, rig), x, y, scale, facing)


# ====================================================================== 3. props


def crate(x, y, scale=1.0, rot=0):
    return _place(_crate(), x, y, scale, 1, rot)


def jar(x, y, scale=1.0, rot=0, color=None):
    return _place(_g(_amphora(0, color), "translate(0,6)"), x, y, scale, 1, rot)


def sack(x, y, scale=1.0, rot=0, color=None, seed=0):
    return _place(_sack(1.0, color, seed), x, y, scale, 1, rot)


def _lots_jar(sticks=5):
    col = S.mix(P["terracotta"], P["sand_dark"], 0.35)
    out = ""
    rng = random.Random(7)
    for i in range(sticks):
        a = -18 + 36 * i / max(1, sticks - 1) + rng.uniform(-4, 4)
        ln = rng.uniform(56, 74)
        tip = _rot(0, -78 - ln, 0, -60, a)
        out += _tube(f"M0,-56 L{_f(tip[0])},{_f(tip[1])}", 9, P["wood_light"], 3)
    body = [(-26, -78), (-40, -62), (-48, -34), (-42, -10), (-26, 0), (26, 0), (42, -10), (48, -34), (40, -62),
            (26, -78)]
    out += _p(_sm(body, closed=False) + " Z", col, 4)
    out += _ell(0, -78, 30, 9, S.shade(col, -0.45), 4)
    out += _p("M-46,-40 Q0,-28 46,-40", sw=6, stroke=CREAM, extra='opacity="0.85"')
    out += _p("M-44,-22 L-34,-30 L-24,-22 L-14,-30 L-4,-22 L6,-30 L16,-22 L26,-30 L36,-22", sw=2.5,
              stroke=S.shade(col, -0.4))
    out += _ell(-24, -50, 6, 14, HILITE, 0, extra='opacity="0.35"')
    return out


def lots_jar(x, y, scale=1.0, sticks=5):
    return _place(_lots_jar(sticks), x, y, scale)


def _lot(marked=False, gid="lot"):
    out = ""
    if marked:
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.95), (0.45, P["gold"], 0.5), (1, P["gold"], 0)])}</defs>'
                f'<ellipse cx="0" cy="0" rx="78" ry="56" fill="url(#{gid})"/>')
    out += _rect(-38, -11, 76, 22, P["wood_light"], 4, rx=10)
    out += _p("M-26,-2 Q-6,-6 10,0 Q22,4 30,0", sw=2.5, stroke=P["wood"])
    out += _line(-30, 5, -12, 5, sw=2.5, color=P["wood"], extra='opacity="0.7"')
    if marked:
        out += _circ(8, 0, 8, P["sun_hot"], 3)
        out += _circ(8, 0, 3.5, P["glow"], 0)
    return out


def lot(x, y, scale=1.0, rot=0, marked=False):
    return _place(_lot(marked, _uid("lot", marked)), x, y, scale, 1, rot)


def lantern(x, y, scale=1.0, lit=True):
    return _place(_lantern_body(lit, lit, _uid("lan", lit)), x, y, scale)


def rope_coil(x, y, scale=1.0):
    return _place(_rope_coil(), x, y, scale)


def _scroll(opened=False):
    parch, roll = "#efdfb8", "#e2cb98"
    out = ""
    if not opened:
        out += _rect(-64, -18, 128, 36, parch, 4, rx=16)
        out += _ell(-64, 0, 9, 18, roll, 4) + _p("M-64,-8 Q-58,0 -64,8", sw=2.5)
        out += _ell(64, 0, 9, 18, roll, 4)
        out += _p("M58,-8 Q64,-12 66,0 Q64,10 58,8", sw=2.5)
        out += _rect(-6, -21, 16, 42, P["sail_stripe"], 3.5, rx=3)
        out += _p("M2,20 Q-6,36 -14,42 M2,20 Q10,36 18,40", sw=6, stroke=INK) + \
            _p("M2,20 Q-6,36 -14,42 M2,20 Q10,36 18,40", sw=3, stroke=P["sail_stripe"])
        out += _ell(-50, -6, 26, 4, HILITE, 0, extra='opacity="0.5"')
        return out
    out += _p("M-80,-52 L80,-52 Q86,0 80,52 L-80,52 Q-74,0 -80,-52 Z", parch, 4)
    for i, yy in enumerate((-30, -14, 2, 18, 34)):
        x0, x1 = -60, 60 - (i % 2) * 22
        d = f"M{x0},{yy}"
        xx = x0
        while xx < x1:
            d += " q5,-5 10,0 q5,5 10,0"
            xx += 20
        out += _p(d, sw=2.5, stroke=P["ink_soft"], extra='opacity="0.8"')
    for sx in (-86, 86):
        out += _rect(sx - 11, -62, 22, 124, roll, 4, rx=10)
        out += _rect(sx - 4, -76, 8, 16, P["wood"], 3, rx=3) + _rect(sx - 4, 60, 8, 16, P["wood"], 3, rx=3)
        out += _line(sx - 4, -50, sx - 4, 50, sw=2.5, color=S.shade(roll, -0.25))
    return out


def scroll(x, y, scale=1.0, rot=0, opened=False):
    return _place(_scroll(opened), x, y, scale, 1, rot)


def _stick(pts, w, col, sw=3.5, knots=()):
    """A rough wooden stick along a polyline (slightly uneven) with optional knots."""
    out = _tube(_poly(pts, closed=False), w, col, sw)
    for t in knots:
        i = min(len(pts) - 2, int(t * (len(pts) - 1)))
        q = _lerp2(pts[i], pts[i + 1], t * (len(pts) - 1) - i)
        out += _ell(q[0], q[1], w * 0.45, w * 0.3, S.shade(col, -0.3), 0)
    return out


def _lashing(x, y, k=1.0, col=None):
    col = col or S.mix(P["sackcloth"], P["sand"], 0.3)
    out = ""
    for j in (-1, 0, 1):
        d = f"M{_f(x - 9 * k)},{_f(y + j * 6 * k - 4 * k)} L{_f(x + 9 * k)},{_f(y + j * 6 * k + 4 * k)}"
        out += _p(d, sw=6.5 * k, stroke=INK) + _p(d, sw=3 * k, stroke=col)
    return out


def _booth():
    """Jonah's little shelter (Jonah 4:5): rough sticks lashed into an A-frame, a thin cloth thrown over it."""
    wood, wd = P["wood"], P["wood_dark"]
    cloth = S.mix(P["headcloth"], P["sand"], 0.3)
    under = S.shade(cloth, -0.32)
    out = ""
    # back posts (farther: base higher, thinner, darker)
    out += _stick([(-112, -16), (-115, -150), (-110, -268)], 9, S.shade(wd, 0.05), 3)
    out += _stick([(184, -18), (187, -140), (182, -272)], 9, S.shade(wd, 0.05), 3)
    # shady inside of the cloth roof
    out += _p("M-196,-252 Q-100,-300 0,-366 Q100,-302 196,-256 L184,-262 L-110,-260 Z", under, 0)
    out += _p("M-150,-262 L182,-266", sw=8, stroke=S.shade(under, -0.25), extra='opacity="0.6"')
    # front posts: uneven sticks, the tops poke up past the tie bar
    out += _stick([(-158, 2), (-162, -120), (-156, -200), (-160, -292)], 13, wood, 3.5, knots=(0.45,))
    out += _stick([(146, 2), (150, -110), (146, -205), (152, -284)], 13, wood, 3.5, knots=(0.62,))
    out += _stick([(-196, -256), (-40, -260), (194, -254)], 9, S.shade(wood, -0.1), 3)
    for bx, by in ((-158, 0), (146, 0)):
        out += _ell(bx - 14, by - 2, 15, 7, P["stone"], 3) + _ell(bx + 14, by - 1, 11, 6, P["stone_dark"], 3)
    # the cloth: a thin sheet over the rafters, sagging between them, ragged hems hanging at the sides
    top = [(-212, -230), (-150, -276), (-80, -322), (0, -376), (80, -324), (152, -280), (214, -236)]
    hem = [(222, -214), (210, -198), (200, -214), (188, -202), (176, -226), (90, -284), (0, -346),
           (-88, -286), (-170, -232), (-182, -206), (-194, -220), (-206, -200), (-218, -214)]
    cd = _sm(top, closed=False, tension=0.8) + " " + " ".join(f"L{_f(x)},{_f(y)}" for x, y in hem) + " Z"
    stripe = _p(_sm([(-216, -222), (-150, -264), (-76, -310), (0, -360), (76, -312), (152, -268), (218, -226)],
                    closed=False, tension=0.8), sw=6, stroke=P["sail_stripe"], extra='opacity="0.85"')
    out += _p(cd, cloth, 0) + _clip(_uid("boothc", 0), cd, stripe) + _p(cd, sw=4)
    for x0, y0, x1, y1 in ((-120, -262, -112, -236), (120, -270, 128, -240), (-40, -334, -46, -312)):
        out += _line(x0, y0, x1, y1, sw=2.5, color=S.shade(cloth, -0.35), extra='opacity="0.55"')
    # rafters crossing at the apex, ends sticking out above the cloth
    out += _stick([(-176, -228), (-80, -300), (30, -400)], 10, wd, 3.5)
    out += _stick([(174, -232), (84, -298), (-26, -394)], 10, wd, 3.5)
    out += _lashing(0, -372) + _lashing(-158, -262, 0.85) + _lashing(148, -260, 0.85)
    # a few leafy branches laid on the cloth
    for sx, sy, ang in ((-150, -270, -36), (24, -372, 32)):
        out += _g(_p("M0,0 Q60,-6 128,-2", sw=4, stroke=P["leaf_dark"]) +
                  "".join(_ell(16 + 24 * i, -5 - (i % 2) * 8, 14, 6, P["leaf"] if i % 2 else P["leaf_dark"], 2.5,
                               extra=f'transform="rotate({-30 + 60 * (i % 2)} {16 + 24 * i} {-5 - (i % 2) * 8})"')
                          for i in range(5)), f"translate({sx},{sy}) rotate({ang})")
    return out


def booth(x, y, scale=1.0, facing=1):
    return _place(_booth(), x, y, scale, facing)


_KING_PROPS = {}


def _king_prop(kind):
    """The king's own throne / ash heap exactly as art/characters.king draws them behind a seated king.
    Returns (markup in the king's anchor coordinates, facing right, info dict). One library calls the
    other, so the empty throne and the occupied one can never drift apart."""
    if kind in _KING_PROPS:
        return _KING_PROPS[kind]
    from art import characters as CH   # local import: characters does not import props
    pose, attire = ("sit_throne", "royal") if kind == "throne" else ("sit_ashes", "sackcloth")
    D = CH._king_design(attire, pose, True, True)
    real, cap = D["behind"], {}

    def grab(st):
        cap.update(svg=real(st), G=st["ground"] or 0.0, pel=st["pel"], th=st["m"]["th"])
        return ""
    D["behind"] = grab
    ps = dict(CH.POSES[pose])
    CH._figure(D, CH._KING_M, ps, ps["expr"], 1)
    body = f'<g transform="translate(0,{_f(-cap["G"])})">{cap["svg"]}</g>'
    info = {"cx": cap["pel"][0] + 0.35 * cap["th"]}
    _KING_PROPS[kind] = (body, info)
    return _KING_PROPS[kind]


def throne(x, y, scale=1.0, facing=1):
    return _place(_king_prop("throne")[0], x, y, scale, facing)


def _ash_smoke():
    """Two thin, soft curls of grey rising from the heap."""
    c = S.shade(P["ash"], 0.3)
    out = ""
    for x0, h, ph, op in ((-30, 170, 0.0, 0.55), (22, 130, 1.8, 0.45)):
        pts = [(x0 + 16 * math.sin(ph + k * 1.4) * (k / 6), -24 - h * k / 6) for k in range(7)]
        d = _sm(pts, closed=False)
        out += _p(d, sw=9, stroke=c, extra=f'opacity="{op * 0.6:.2f}" filter="url(#soft)"')
        out += _p(d, sw=3.2, stroke=c, extra=f'opacity="{op:.2f}"')
    return out


def ash_pile(x, y, scale=1.0, smoke=False, facing=1):
    body, info = _king_prop("ashes")
    heap = f'<g transform="translate({_f(-info["cx"])},0)">{body}</g>'
    return _place((_ash_smoke() if smoke else "") + heap, x, y, scale, facing)


# x offset (scale 1, facing right) from king(pose='sit_ashes')'s anchor to the centre of his ash heap
KING_ASH_DX = round(_king_prop("ashes")[1]["cx"], 1)


# ====================================================================== 4. plants


def _palmate(cx, cy, r, lobes, spin, tilt, hang, fill, vein, wither=0.0, seed=0, sw=4.0):
    """Peltate palm-shaped leaf (castor) attached at (cx, cy). Geometry is transformed in python so the ink
    stays even. As it withers the lobes fold down around the petiole tip like a closing umbrella, so a
    dead leaf hangs as a limp brown 'hand' below its stalk."""
    rng = random.Random(seed)
    w = _clamp(wither)
    fold = _smooth(w * 1.15)
    comp = 1 - 0.72 * fold                      # lobe fan compresses toward 'down'
    spin_e = math.radians(spin * (1 - fold))
    tilt_e = tilt + (0.95 - tilt) * fold         # a hanging leaf is seen face-on
    hang_e = math.radians(hang * (1 - fold))
    ca, sa = math.cos(hang_e), math.sin(hang_e)

    def tf(px, py):
        qx, qy = px * math.cos(spin_e) - py * math.sin(spin_e), px * math.sin(spin_e) + py * math.cos(spin_e)
        qy *= tilt_e
        return (cx + qx * ca - qy * sa, cy + qx * sa + qy * ca)

    n = lobes
    hw = math.pi / n * comp
    rs = r * (0.34 + 0.08 * w)
    d = ""
    tips = []
    for i in range(n):
        rel = 2 * math.pi * (i - (n - 1) / 2) / n
        a = math.pi / 2 + rel * comp + rng.uniform(-0.04, 0.04)
        lob = _lerp(0.72 - 0.28 * math.cos(rel), 0.9 - 0.12 * abs(rel) / math.pi, fold)
        rt = r * lob * (1 - 0.12 * w) * rng.uniform(0.93, 1.05)
        bw = hw * (0.82 - 0.2 * w)
        s0 = (rs * math.cos(a - hw), rs * math.sin(a - hw))
        s1 = (rs * math.cos(a + hw), rs * math.sin(a + hw))
        c0 = (rt * 0.86 * math.cos(a - bw), rt * 0.86 * math.sin(a - bw))
        c1 = (rt * 0.86 * math.cos(a + bw), rt * 0.86 * math.sin(a + bw))
        curl = -w * 0.18 * rng.uniform(0.5, 1.2) * (1 if rel >= 0 else -1)   # tips curl in toward the middle
        t = (rt * math.cos(a + curl), rt * math.sin(a + curl))
        tips.append((a, rt))
        P0, C0, T, C1, P1 = tf(*s0), tf(*c0), tf(*t), tf(*c1), tf(*s1)
        if i == 0:
            d += f"M{_f(P0[0])},{_f(P0[1])}"
        d += (f" Q{_f(C0[0])},{_f(C0[1])} {_f(T[0])},{_f(T[1])}"
              f" Q{_f(C1[0])},{_f(C1[1])} {_f(P1[0])},{_f(P1[1])}")
    if fold > 0.02:     # folded: the top of the leaf gathers at the stalk tip
        hub = tf(0, -rs * 0.25)
        d += f" L{_f(hub[0])},{_f(hub[1])}"
    d += " Z"
    under = f'<path d="{d}" fill="{S.shade(fill, -0.3)}" transform="translate({_f(2 - 2 * fold)},{_f(5 + 3 * tilt_e)})"/>'
    vein_c = S.mix(vein, S.shade(fill, -0.28), w)
    inner = ""
    c = tf(0, 0)
    for a, rt in tips:
        e = tf(rt * 0.78 * math.cos(a), rt * 0.78 * math.sin(a))
        inner += _line(c[0], c[1], e[0], e[1], sw=sw * 0.7, color=vein_c, extra='opacity="0.85"')
    if w > 0.2:
        spot = S.shade(P["leaf_dead"], -0.25)
        for k in range(int(3 + 6 * w)):
            a, rt = tips[rng.randrange(n)]
            rr = rng.uniform(0.35, 0.8) * rt
            spt = tf(rr * math.cos(a), rr * math.sin(a))
            inner += _ell(spt[0], spt[1], 4 + 6 * w, 3 + 3 * w, spot, 0, extra=f'opacity="{0.3 + 0.45 * w:.2f}"')
    cid = _uid("leaf", round(cx, 1), round(cy, 1), round(r, 1), seed, round(w, 3))
    out = under + _p(d, fill, 0) + _clip(cid, d, inner) + _p(d, sw=sw)
    out += _circ(c[0], c[1], 3 + r * 0.03, vein_c, 0)
    return out


def _leaf_col(w, base=None):
    base = base or P["leaf"]
    if w <= 0.55:
        return S.mix(base, P["leaf_dry"], w / 0.55)
    return S.mix(P["leaf_dry"], P["leaf_dead"], (w - 0.55) / 0.45)


def castor_height(growth):
    """Stem height in px (scale 1) of castor_plant at a growth value."""
    return 30 + 470 * _clamp(growth) ** 2.2


def _castor(growth=1.0, wither=0.0, bite=0.0, side=1, seed=0):
    g, w, b = _clamp(growth), _clamp(wither), _clamp(bite)
    sd = 1 if side >= 0 else -1
    Hs = castor_height(g)
    rng = random.Random(seed)

    def stem_pt(f):
        x = sd * (0.16 * Hs * f * f + w * 0.2 * Hs * f ** 3)
        y = -Hs * f + w * 0.1 * Hs * f ** 3
        return (x, y)

    def normal(f):
        a, c = stem_pt(max(0, f - 0.02)), stem_pt(min(1, f + 0.02))
        dx, dy = c[0] - a[0], c[1] - a[1]
        L = math.hypot(dx, dy) or 1
        return (-dy / L, dx / L)

    base_w = 5 + 12 * g

    def hw(f):
        return base_w * (1 - 0.55 * f)

    brown = S.shade(P["leaf_dead"], -0.18)
    stem_c = S.mix(S.mix("#a65b49", P["leaf_dark"], 0.18), brown, w)       # castor stems are reddish
    pet_c = S.mix(S.mix("#b8604c", P["leaf_dark"], 0.12), brown, w)
    vein_c = S.mix(P["leaf_light"], "#d9b3a0", 0.25)

    # branch
    bg = _smooth((g - 0.4) / 0.45)
    b0 = stem_pt(0.6)
    bend = (b0[0] + sd * 0.62 * Hs * bg, b0[1] - 0.18 * Hs * bg + w * 0.22 * Hs * bg)
    bmid = (b0[0] + sd * 0.32 * Hs * bg, b0[1] - 0.2 * Hs * bg + w * 0.06 * Hs * bg)

    def branch_pt(f):
        u = 1 - f
        return (u * u * b0[0] + 2 * u * f * bmid[0] + f * f * bend[0], u * u * b0[1] + 2 * u * f * bmid[1] + f * f * bend[1])

    # leaf table: (on, f, petiole dx, dy [x Hs], radius, birth, back, tilt)
    table = [("s", .26, -.24, -.02, 80, .05, False, .8), ("s", .38, .26, -.06, 92, .12, True, .75),
             ("s", .50, -.30, -.08, 110, .22, False, .7), ("s", .68, -.26, -.10, 130, .36, True, .55),
             ("b", .35, .00, -.16, 130, .48, True, .45), ("b", .85, .04, .04, 120, .74, True, .5),
             ("b", .65, .04, -.14, 150, .56, False, .42), ("b", 1.0, .10, -.08, 160, .64, False, .42),
             ("s", .88, .14, -.14, 150, .50, False, .45), ("s", 1.0, -.10, -.10, 130, 0.0, False, .55)]
    back_l, front_l = "", ""
    for i, (on, f, pdx, pdy, r, birth, back, tilt) in enumerate(table):
        if on == "b" and bg <= 0.01:
            continue
        if birth == 0.0:
            k = 0.22 + 0.78 * _smooth(g / 0.55)
        else:
            k = _smooth((g - birth) / 0.3)
        if k <= 0.01:
            continue
        a = stem_pt(f) if on == "s" else branch_pt(f)
        Hk = Hs if on == "s" else max(Hs, 200)
        vx, vy = sd * pdx * Hk * (0.4 + 0.6 * k), pdy * Hk * (0.4 + 0.6 * k)
        # wither: petioles droop toward hanging
        ang = math.atan2(vy, vx)
        L = math.hypot(vx, vy)
        down = math.pi / 2
        ang = ang + (down - ang if abs(down - ang) <= math.pi else (down - ang) - math.copysign(2 * math.pi, down - ang)) * 0.62 * _smooth(w)
        L *= 1 - 0.25 * w
        c = (a[0] + L * math.cos(ang), a[1] + L * math.sin(ang))
        mid = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - L * 0.18 * (1 - w))
        rr = r * k * (1 - 0.15 * w) * (0.45 + 0.55 * g)
        lobes = 7 if r < 100 else 9
        spin = rng.uniform(-12, 12)
        hang = 0.0
        tl = tilt
        lc = _leaf_col(w, S.mix(P["leaf"], P["leaf_dark"], 0.3) if back else P["leaf"])
        pet = _p(f"M{_f(a[0])},{_f(a[1])} Q{_f(mid[0])},{_f(mid[1])} {_f(c[0])},{_f(c[1])}",
                 sw=4 + 3.5 * k + 2 * g, stroke=INK) + \
            _p(f"M{_f(a[0])},{_f(a[1])} Q{_f(mid[0])},{_f(mid[1])} {_f(c[0])},{_f(c[1])}",
               sw=max(1.5, 3.5 * k + 2 * g - 2), stroke=pet_c)
        leaf = _palmate(c[0], c[1], rr, lobes, spin, tl, hang, lc, vein_c, w, seed * 31 + i, sw=3.2 + 1.3 * k)
        if back:
            back_l += pet + leaf
        else:
            front_l += pet + leaf
    # stem polygon
    N = 14
    left, right = [], []
    for j in range(N + 1):
        f = j / N
        p = stem_pt(f)
        nx, ny = normal(f)
        h = hw(f)
        left.append((p[0] + nx * h, p[1] + ny * h))
        right.append((p[0] - nx * h, p[1] - ny * h))
    tip = stem_pt(1.0)
    stem_d = _sm(left + [(tip[0], tip[1] - hw(1) * 0.8)] + list(reversed(right)), closed=True, tension=0.8)
    stem = _p(stem_d, stem_c, 0)
    hl = [(p[0] + nx * h * 0.4, p[1] + ny * h * 0.4) for p, (nx, ny), h in
          ((stem_pt(j / N), normal(j / N), hw(j / N)) for j in range(1, N))]
    stem += _p(_sm(hl, closed=False), sw=max(2, base_w * 0.3), stroke=S.shade(stem_c, 0.3), extra='opacity="0.7"')
    for f in (0.3, 0.42, 0.56, 0.6, 0.74, 0.92):
        if f * Hs > 20:
            p = stem_pt(f)
            nx, ny = normal(f)
            h = hw(f) * 1.1
            stem += _line(p[0] + nx * h, p[1] + ny * h, p[0] - nx * h, p[1] - ny * h, sw=2.5,
                          color=S.shade(stem_c, -0.3))
    stem += _p(stem_d, sw=3.5 + g)
    # bite notch: one concave scallop with little tooth nicks, pale pith along the cut
    if b > 0.01:
        fb = min(16.0, Hs * 0.45) / Hs
        p = stem_pt(fb)
        nx, ny = normal(fb)
        e = (p[0] - sd * abs(nx) * hw(fb) * 1.05, p[1])
        rb = hw(fb) * (0.3 + 0.85 * b)
        ry = rb * 1.15
        nicks = [(e[0] + sd * rb * math.cos(t_), e[1] + ry * math.sin(t_)) for t_ in (-0.8, 0.0, 0.8)]
        mid_ = _uid("bite", g, b, sd)
        holes = _ell(e[0], e[1], rb, ry, "black", 0) + "".join(_circ(qx, qy, 2.2 + 1.2 * b, "black", 0)
                                                                for qx, qy in nicks)
        stem = (f'<mask id="{mid_}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">'
                f'<rect x="-2000" y="-2000" width="4000" height="4000" fill="white"/>{holes}</mask>'
                f'<g mask="url(#{mid_})">{stem}</g>')
        cid = _uid("bitec", g, b, sd)
        rims = _ell(e[0], e[1], rb + 3.5, ry + 3.5, "none", 6, stroke="#e6e2ad") + _ell(e[0], e[1], rb, ry, "none", 3)
        stem += _g(_clip(cid, stem_d, rims), extra=f'mask="url(#{mid_})"')
        for k in range(int(1 + 4 * b)):
            stem += _circ(e[0] - sd * rng.uniform(6, 26), rng.uniform(-5, -1.5), rng.uniform(1.8, 3.0), "#d8dca2", 1.4)
    # branch
    branch = ""
    if bg > 0.01:
        bpts = [branch_pt(j / 8) for j in range(9)]
        bw_ = 3 + 6 * bg
        branch = _tube(_sm(bpts, closed=False), bw_, stem_c, 3.5)
    # cotyledons
    cot = ""
    kc = 1 - _smooth((g - 0.12) / 0.25)
    if kc > 0.01:
        fc = min(1.0, 26 / Hs)
        p = stem_pt(fc)
        for s_ in (-1, 1):
            cx_, cy_ = p[0] + s_ * 16 * kc, p[1] - 6 * kc
            cot += _ell(cx_, cy_, 17 * kc, 8 * kc, _leaf_col(w, P["leaf_light"]), 3,
                        extra=f'transform="rotate({s_ * -22} {_f(cx_)} {_f(cy_)})"')
    # seeds (spiky red clusters)
    seeds = ""
    ks = _smooth((g - 0.68) / 0.3)
    if ks > 0.01:
        t0 = stem_pt(1.0)
        sc_col = S.mix("#c8473f", "#8a5a3a", w)
        top = (t0[0] + sd * 10 * ks, t0[1] - 66 * ks)
        seeds += _tube(f"M{_f(t0[0])},{_f(t0[1])} Q{_f(t0[0])},{_f(t0[1] - 40 * ks)} {_f(top[0])},{_f(top[1])}",
                       4, pet_c, 3)
        for j, (dx, dy) in enumerate(((-12, -20), (12, -30), (-8, -44), (10, -54), (0, -66), (-16, -58))):
            cx_, cy_ = t0[0] + (dx + sd * 6) * ks, t0[1] + dy * ks
            rr = 9 * ks
            spikes = ""
            for q in range(10):
                a = q * math.pi / 5
                spikes += f"M{_f(cx_ + rr * math.cos(a))},{_f(cy_ + rr * math.sin(a))} l{_f(5 * ks * math.cos(a))},{_f(5 * ks * math.sin(a))} "
            seeds += _p(spikes, sw=2.2, stroke=S.shade(sc_col, -0.3))
            seeds += _circ(cx_, cy_, rr, sc_col, 2.8) + _circ(cx_ - rr * 0.3, cy_ - rr * 0.3, rr * 0.25, "#f2a99a", 0)
    mound = _ell(0, 0, 46 + 14 * g, 9 + 2 * g, P["earth"], 3.5) + _ell(-10, -3, 20, 4, S.shade(P["earth"], 0.25), 0)
    return mound + back_l + branch + stem + cot + front_l + seeds


def castor_plant(x, y, scale=1.0, growth=1.0, wither=0.0, bite=0.0, side=1, seed=0):
    return _place(_castor(growth, wither, bite, side, seed), x, y, scale)


def _frond(base, ang, length, droop, width, col, seed=0):
    """Date-palm frond: a tapered, arching feather with a soft comb of rounded leaflet tips."""
    a = math.radians(ang)
    end = (base[0] + math.cos(a) * length, base[1] + math.sin(a) * length + droop)
    ctrl = (base[0] + math.cos(a) * length * 0.6, base[1] + math.sin(a) * length * 0.6 - droop * 0.25)

    def at(t):
        u = 1 - t
        return (u * u * base[0] + 2 * u * t * ctrl[0] + t * t * end[0], u * u * base[1] + 2 * u * t * ctrl[1] + t * t * end[1])

    N = 40
    L, R, frame = [], [], []
    for i in range(N + 1):
        t = i / N
        p, q = at(max(0, t - 0.01)), at(min(1, t + 0.01))
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy) or 1
        tx, ty = dx / ln, dy / ln
        nx, ny = -ty, tx
        wv = 0.82 * width * math.sin(math.pi * min(1.0, t * 1.04)) ** 0.7
        comb = 0.72 + 0.28 * abs(math.sin(math.pi * t * 9.5))     # soft rounded leaflet tips
        c = at(t)
        sh = wv * 0.35                                           # leaflets sweep toward the tip
        L.append((c[0] + nx * wv * comb + tx * sh, c[1] + ny * wv * comb + ty * sh))
        R.append((c[0] - nx * wv * comb + tx * sh, c[1] - ny * wv * comb + ty * sh))
        frame.append((c, (nx, ny), (tx, ty), wv))
    d = _sm(L + list(reversed(R)), closed=True, tension=0.8)
    inner = ""
    dark = S.shade(col, -0.3)
    for i in range(3, N - 2, 3):
        c, (nx, ny), (tx, ty), wv = frame[i]
        for sgn in (1, -1):
            e = (c[0] + sgn * nx * wv * 0.85 + tx * wv * 0.45, c[1] + sgn * ny * wv * 0.85 + ty * wv * 0.45)
            inner += _line(c[0], c[1], e[0], e[1], sw=2.2, color=dark, extra='opacity="0.45"')
    out = _p(d, col, 0) + _clip(_uid("frond", round(base[0], 1), round(base[1], 1), ang, length, col), d, inner)
    out += _p(d, sw=3.2)
    out += _p(f"M{_f(base[0])},{_f(base[1])} Q{_f(ctrl[0])},{_f(ctrl[1])} {_f(end[0])},{_f(end[1])}", sw=3,
              stroke=S.shade(col, -0.38))
    return out


def _palm(lean=0.0, sway=0.0, dates=True):
    top = (lean * 150, -430)
    ctrl = (lean * 10, -230)

    def at(t):
        u = 1 - t
        return (2 * u * t * ctrl[0] + t * t * top[0], 2 * u * t * ctrl[1] + t * t * top[1])

    L, R = [], []
    for i in range(13):
        t = i / 12
        p, q = at(max(0, t - 0.01)), at(min(1, t + 0.01))
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        h = 24 - 9 * t + (8 if i == 0 else 0)
        c = at(t)
        L.append((c[0] + nx * h, c[1] + ny * h))
        R.append((c[0] - nx * h, c[1] - ny * h))
    trunk_c = "#a8825a"
    out = ""
    sw_ = sway * 9
    for ang, ln, dr in ((-150, 200, 70), (-110, 190, 40), (-70, 195, 40), (-30, 200, 70)):
        out += _frond(top, ang + sw_, ln, dr, 30, S.mix(P["leaf_dark"], P["olive"], 0.3))
    trunk_d = _sm(L + list(reversed(R)), closed=True, tension=0.7)
    out += _p(trunk_d, trunk_c, 0)
    chev = ""
    for i in range(1, 17):
        t = i / 17
        c = at(t)
        p, q = at(t - 0.01), at(t + 0.01)
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        h = 24 - 9 * t
        chev += (f"M{_f(c[0] + nx * h)},{_f(c[1] + ny * h)} Q{_f(c[0] + dx / ln * 9)},{_f(c[1] + dy / ln * 9)} "
                 f"{_f(c[0] - nx * h)},{_f(c[1] - ny * h)} ")
    out += _clip(_uid("palm", lean), trunk_d, _p(chev, sw=3, stroke=S.shade(trunk_c, -0.35)) +
                 _p(_sm([(c[0] + 8, c[1]) for c in (at(i / 10) for i in range(11))], closed=False), sw=8,
                    stroke=S.shade(trunk_c, 0.25), extra='opacity="0.5"'))
    out += _p(trunk_d, sw=4)
    if dates:
        for dx_, s_ in ((-24, 1), (26, -1)):
            cx_, cy_ = top[0] + dx_, top[1] + 30
            out += _p(f"M{_f(top[0] + dx_ * 0.4)},{_f(top[1] + 6)} Q{_f(cx_)},{_f(cy_ - 20)} {_f(cx_)},{_f(cy_)}",
                      sw=3, stroke=P["wood"])
            for j, (ox, oy) in enumerate(((0, 0), (-9, 8), (9, 8), (-5, 18), (6, 19), (-12, 20), (12, 21), (0, 28))):
                out += _ell(cx_ + ox, cy_ + oy, 6, 8, "#d68a3c" if j % 3 else "#a85a2c", 2.5)
    for ang, ln, dr in ((-175, 220, 120), (-135, 210, 55), (-92, 180, 10), (-50, 210, 55), (-5, 220, 120),
                        (155, 160, 70), (25, 160, 70)):
        out += _frond(top, ang + sw_ * (1.4 if abs(ang) > 90 else 1), ln, dr, 34, P["leaf"])
    out += _circ(top[0], top[1] + 4, 14, S.shade(trunk_c, -0.2), 3.5)
    return out


def palm_tree(x, y, scale=1.0, lean=0.0, sway=0.0, dates=True):
    return _place(_palm(lean, sway, dates), x, y, scale)


def _cluster(circles, fill, sw=4.0):
    a = "".join(_circ(cx, cy, r, fill, sw * 2) for cx, cy, r in circles)
    b = "".join(_circ(cx, cy, r, fill, 0) for cx, cy, r in circles)
    return a + b


def _olive(seed=0):
    rng = random.Random(seed)
    bark = "#8f7e68"
    out = ""
    out += _p("M-34,0 Q-20,-40 -28,-90 Q-40,-140 -80,-190 L-64,-198 Q-24,-150 -10,-112 Q0,-160 10,-200 L26,-196 "
              "Q16,-140 18,-100 Q40,-150 84,-180 L92,-166 Q48,-130 34,-70 Q30,-30 40,0 Z", bark, 4)
    out += _p("M-18,-10 Q-8,-60 -14,-100 M14,-20 Q10,-60 22,-96", sw=3, stroke=S.shade(bark, -0.35))
    out += _ell(-6, -60, 7, 10, S.shade(bark, -0.45), 2.5)
    blobs = [(-110, -230, 62), (-60, -270, 70), (10, -290, 76), (80, -268, 66), (120, -225, 54), (40, -220, 64),
             (-40, -215, 60), (-130, -190, 40), (130, -185, 38)]
    out += _cluster(blobs, P["olive"], 4)
    for cx, cy, r in ((-60, -230, 50), (50, -235, 52), (110, -205, 30), (-120, -200, 28)):
        out += _circ(cx, cy + 16, r, S.shade(P["olive"], -0.18), 0, extra='opacity="0.6" filter="url(#soft)"')
    silver = "#c3c99a"
    for _ in range(46):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 1) ** 0.6
        px, py = 0 + 125 * rr * math.cos(a), -248 + 60 * rr * math.sin(a)
        rot = rng.uniform(-50, 50)
        out += _ell(px, py, 9, 3.2, silver if rng.random() < 0.65 else S.shade(P["olive"], -0.3), 0,
                    extra=f'transform="rotate({rot:.0f} {_f(px)} {_f(py)})" opacity="0.9"')
    for _ in range(9):
        px, py = rng.uniform(-110, 110), rng.uniform(-280, -200)
        out += _ell(px, py, 5, 6.5, "#5c4a63", 2)
    return out


def olive_tree(x, y, scale=1.0, seed=0):
    return _place(_olive(seed), x, y, scale)


def _bush(variant=0):
    v = variant % 4
    rng = random.Random(11 + v)
    if v == 2:  # dry desert shrub: a fan of bare forked twigs with a few small grey-green tufts
        twig = S.shade(P["wood"], -0.15)
        tuft = S.mix(P["olive"], P["stone"], 0.45)
        out, tips = "", []

        def br(x0, y0, ang, ln, depth, wdt):
            nonlocal out
            a_ = math.radians(ang)
            x1, y1 = x0 + math.cos(a_) * ln, y0 + math.sin(a_) * ln
            mx_, my_ = (x0 + x1) / 2 + rng.uniform(-5, 5), (y0 + y1) / 2 + rng.uniform(-4, 4)
            out += _tube(f"M{_f(x0)},{_f(y0)} Q{_f(mx_)},{_f(my_)} {_f(x1)},{_f(y1)}", wdt, twig, 2.6)
            if depth < 2:
                br(x1, y1, ang - rng.uniform(18, 32), ln * 0.66, depth + 1, wdt * 0.7)
                br(x1, y1, ang + rng.uniform(16, 30), ln * 0.62, depth + 1, wdt * 0.7)
            else:
                tips.append((x1, y1))
        for ang in (-150, -122, -98, -76, -52, -28):
            br(rng.uniform(-8, 8), 0, ang + rng.uniform(-6, 6), rng.uniform(34, 46), 0, 6.5)
        for i, (tx, ty) in enumerate(tips):
            if i % 2 == 1:
                continue
            blobs = [(tx + rng.uniform(-5, 5), ty + rng.uniform(-4, 4), rng.uniform(6, 9)) for _ in range(3)]
            out += _cluster(blobs, tuft if i % 2 else S.shade(tuft, -0.12), 2.6)
        out += _ell(0, -2, 44, 6, S.shade(P["sand_dark"], -0.1), 0, extra='opacity="0.35"')
        return out
    base = {0: P["leaf"], 1: S.mix(P["leaf"], P["olive"], 0.4), 3: P["leaf_dark"]}[v]
    circles = [(-58, -34, 36), (-20, -62, 46), (30, -60, 44), (66, -32, 34), (4, -30, 44)]
    out = _cluster(circles, base, 4)
    out += _ell(0, -14, 70, 14, S.shade(base, -0.25), 0, extra='opacity="0.5" filter="url(#soft)"')
    for _ in range(14):
        px, py = rng.uniform(-70, 70), rng.uniform(-90, -24)
        out += _p(f"M{_f(px - 6)},{_f(py + 3)} Q{_f(px)},{_f(py - 6)} {_f(px + 6)},{_f(py + 3)}", sw=2.5,
                  stroke=S.shade(base, 0.35), extra='opacity="0.8"')
    if v == 1:
        for _ in range(9):
            px, py = rng.uniform(-70, 70), rng.uniform(-92, -24)
            for k in range(5):
                a = k * 2 * math.pi / 5
                out += _circ(px + 5 * math.cos(a), py + 5 * math.sin(a), 4.2, "#f3b8c4", 1.8)
            out += _circ(px, py, 3, P["gold"], 0)
    if v == 3:
        for _ in range(12):
            px, py = rng.uniform(-68, 68), rng.uniform(-90, -22)
            out += _circ(px, py, 5.5, "#c8473f", 2.5) + _circ(px - 1.6, py - 1.6, 1.6, "#f6c6b6", 0)
    return out


def bush(x, y, scale=1.0, variant=0):
    return _place(_bush(variant), x, y, scale)


def _blades(n, spread, hmin, hmax, cols, seed, sway=0.0, wmin=5, wmax=8, sw=2.8):
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        u = (i + 0.5) / n
        bx = (u - 0.5) * spread + rng.uniform(-4, 4)
        h = rng.uniform(hmin, hmax) * (0.75 + 0.25 * math.sin(math.pi * u))
        lean = (u - 0.5) * h * 0.7 + rng.uniform(-8, 8) + sway * h * 0.35
        wd = rng.uniform(wmin, wmax)
        tip = (bx + lean, -h)
        out += _p(f"M{_f(bx - wd)},0 Q{_f(bx - wd * 0.3 + lean * 0.3)},{_f(-h * 0.55)} {_f(tip[0])},{_f(tip[1])} "
                  f"Q{_f(bx + wd * 0.5 + lean * 0.45)},{_f(-h * 0.5)} {_f(bx + wd)},0 Z", cols[i % len(cols)], sw)
    return out


def _grass(variant=0, sway=0.0):
    v = variant % 3
    if v == 1:
        return _blades(9, 70, 34, 66, [P["leaf_dry"], P["sand_dark"], S.mix(P["leaf_dry"], P["sand"], 0.5)], 21, sway)
    out = _blades(9, 70, 36, 70, [P["grass"], P["grass_dark"], S.mix(P["grass"], P["leaf_light"], 0.5)], 20 + v, sway)
    if v == 2:
        for fx, fh, c in ((-18, 74, "#d9544d"), (16, 62, "#e9b949"), (30, 80, "#d9544d")):
            tx = fx + sway * fh * 0.35
            out += _p(f"M{fx},0 Q{fx + 2},{-fh * 0.5} {_f(tx)},{-fh}", sw=3, stroke=P["grass_dark"])
            for k in range(5):
                a = k * 2 * math.pi / 5 - math.pi / 2
                out += _ell(tx + 6 * math.cos(a), -fh + 6 * math.sin(a), 6, 6, c, 2)
            out += _circ(tx, -fh, 3.5, INK, 0)
    return out


def grass_tuft(x, y, scale=1.0, variant=0, sway=0.0):
    return _place(_grass(variant, sway), x, y, scale)


def _ribbon(base, h, amp, waves, width, col, sway, phase=0.0, n=22):
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        y = -h * t
        x = base + amp * math.sin(waves * 2 * math.pi * t + phase) * t ** 0.6 + sway * h * 0.3 * t * t
        wv = width * (0.55 + 0.45 * math.sin(math.pi * min(1.0, t * 1.3 + 0.1))) * (1 - 0.85 * t ** 3)
        L.append((x - wv, y))
        R.append((x + wv, y))
    return _p(_sm(L + [(L[-1][0] + 0, -h - width * 0.4)] + list(reversed(R)), closed=True, tension=0.8), col, 3.5)


def _seaweed(variant=0, sway=0.0):
    v = variant % 4
    if v == 0:
        out = ""
        for b, h, ph, c in ((-22, 200, 0.0, S.shade(P["olive"], -0.1)), (18, 240, 1.7, P["olive"]),
                            (-2, 170, 3.1, S.mix(P["olive"], P["leaf"], 0.5))):
            out += _ribbon(b, h, 18, 1.6, 13, c, sway, ph)
        return out
    if v == 1:
        col = "#d77a8a"
        out = ""
        rng = random.Random(41)
        for i in range(5):
            a = -90 + (i - 2) * 22
            ln = rng.uniform(90, 140)
            ex = math.cos(math.radians(a)) * ln + sway * ln * 0.3
            ey = math.sin(math.radians(a)) * ln
            out += _tube(f"M0,0 Q{_f(ex * 0.3)},{_f(ey * 0.6)} {_f(ex)},{_f(ey)}", 7, col, 3)
            for k in (0.45, 0.7, 0.95):
                out += _circ(ex * k + rng.uniform(-6, 6), ey * k, rng.uniform(9, 14), S.mix(col, P["sun"], 0.15 * k), 3)
        return out
    if v == 2:
        return _blades(9, 70, 120, 210, [P["sea_light"], S.mix(P["leaf"], P["sea"], 0.5), P["leaf_light"]], 33,
                       sway, 8, 12)
    col = "#f0915a"
    out = ""

    def branch(x0, y0, ang, ln, depth):
        nonlocal out
        a = math.radians(ang)
        x1, y1 = x0 + math.cos(a) * ln + sway * ln * 0.2, y0 + math.sin(a) * ln
        out += _tube(f"M{_f(x0)},{_f(y0)} L{_f(x1)},{_f(y1)}", 15 - depth * 3.5, col, 3.2)
        if depth < 2:
            branch(x1, y1, ang - 34, ln * 0.78, depth + 1)
            branch(x1, y1, ang + 30, ln * 0.72, depth + 1)
        else:
            out += _circ(x1, y1, 6, S.mix(col, P["sun"], 0.5), 2.5)

    branch(-8, 0, -112, 62, 0)
    branch(8, 0, -70, 66, 0)
    branch(0, 0, -92, 54, 1)
    return out


def seaweed(x, y, scale=1.0, variant=0, sway=0.0):
    return _place(_seaweed(variant, sway), x, y, scale)


def _reeds(variant=0, sway=0.0):
    rng = random.Random(51 + variant)
    out = _blades(8, 80, 140, 220, [S.mix(P["grass"], P["olive"], 0.5), P["grass_dark"]], 52 + variant, sway, 4, 6)
    for i, (bx, h) in enumerate(((-26, 230), (6, 262), (34, 214))):
        tx = bx + sway * h * 0.3 + rng.uniform(-6, 6)
        out += _tube(f"M{bx},0 Q{bx + 2},{-h * 0.5} {_f(tx)},{-h}", 4, S.mix(P["grass_dark"], P["olive"], 0.5), 2.8)
        out += _rect(tx - 8, -h - 6, 16, 46, "#8a5a36", 3.2, rx=8)
        out += _line(tx, -h - 6, tx + sway * 6, -h - 26, sw=3)
    return out


def reeds(x, y, scale=1.0, variant=0, sway=0.0):
    return _place(_reeds(variant, sway), x, y, scale)


# ====================================================================== 5. creatures


def _worm(chomp=0.0, crawl=0.0):
    c = _clamp(chomp)
    k = _clamp(crawl)
    body, dark = P["worm"], P["worm_dark"]
    green = P["leaf_light"]
    segs = []
    for i in range(5):
        u = i / 4
        x = -24 + 42 * u - k * 6 * math.sin(math.pi * u)
        r = 7.5 + 2.2 * math.sin(math.pi * (0.25 + 0.6 * u))
        y = -r - k * 13 * math.sin(math.pi * u) ** 1.5
        segs.append((x, y, r))
    out = ""
    for x, yy, r in segs:    # little prolegs tucked under every segment (they lift with the arch)
        out += _ell(x - 2.5, yy + r * 0.82, 2.8, 2.6, dark, 2)
        out += _ell(x + 2.5, yy + r * 0.86, 2.8, 2.6, dark, 2)
    for i, (x, yy, r) in enumerate(segs):
        out += _circ(x, yy, r, body if i % 2 else S.shade(body, 0.12), 3)
    for x, yy, r in segs:
        out += _circ(x - 1, yy - r * 0.55, r * 0.3, green, 1.6)
    hx, hy = segs[-1][0] + 12, segs[-1][1] - 5
    out += _p(f"M{_f(hx - 4)},{_f(hy - 10)} Q{_f(hx - 8)},{_f(hy - 22)} {_f(hx - 14)},{_f(hy - 24)}", sw=2.4)
    out += _p(f"M{_f(hx + 3)},{_f(hy - 11)} Q{_f(hx + 4)},{_f(hy - 24)} {_f(hx + 10)},{_f(hy - 27)}", sw=2.4)
    out += _circ(hx - 14, hy - 24, 3.4, green, 2) + _circ(hx + 10, hy - 27, 3.4, green, 2)
    out += _circ(hx, hy, 12.5, S.shade(body, 0.08), 3)
    out += _dot_eye(hx + 3, hy - 3.5, 2.8)
    out += _blush(hx + 2, hy + 4, 3.6, 2.2, 0.8)
    mx, my = hx + 7.5, hy + 4.5
    if c < 0.08:
        out += _p(f"M{_f(mx - 3)},{_f(my - 1)} Q{_f(mx + 1)},{_f(my + 2.5)} {_f(mx + 4)},{_f(my - 1.5)}", sw=2)
    else:   # round 'O' mouth, up to ~40% of the head height, with one row of tiny teeth
        rx, ry = 2.2 + 2.6 * c, 1.8 + 3.4 * c
        md = (f"M{_f(mx - rx)},{_f(my)} A{_f(rx)},{_f(ry)} 0 1 0 {_f(mx + rx)},{_f(my)} "
              f"A{_f(rx)},{_f(ry)} 0 1 0 {_f(mx - rx)},{_f(my)} Z")
        teeth = _rect(mx - rx, my - ry, 2 * rx, ry * 0.42, CREAM, 0)
        teeth += _line(mx, my - ry, mx, my - ry * 0.55, sw=0.9, color=S.shade(CREAM, -0.3))
        out += _p(md, P["mouth_inside"], 0) + _clip(_uid("wormm", round(c, 3)), md, teeth) + _p(md, sw=2)
    return out


def worm(x, y, scale=1.0, facing=1, chomp=0.0, crawl=0.0):
    return _place(_worm(chomp, crawl), x, y, scale, facing)


def _wing(sh, elev, side, length, col, tip_col=None, round_=False, chord=44.0):
    """Flying bird wing seen from the side and a little above. elev = elevation in degrees (+ up), side = +1
    near wing / -1 far wing. The wing is a 3D direction projected to the screen, so a level (gliding) wing
    is foreshortened into a short broad arc and an up / down wing shows its full curved length."""
    ph = math.radians(elev)
    vx = -0.26 - 0.06 * (side < 0)
    vy = -math.sin(ph) - 0.34 * side * math.cos(ph)     # seen from a little below: near wing rides over the back
    V = (vx * length, vy * length)
    vl = math.hypot(*V) or 1.0
    n = (-V[1] / vl, V[0] / vl)
    if n[0] < 0 or (abs(n[0]) < 0.2 and n[1] > 0):
        n = (-n[0], -n[1])                      # bow toward the front / top: a curved leading edge
    arc = 0.13 * vl
    N = 40

    def ctr(t):
        return (sh[0] + V[0] * t + n[0] * arc * math.sin(math.pi * t * 0.9),
                sh[1] + V[1] * t + n[1] * arc * math.sin(math.pi * t * 0.9))
    lead, trail = [], []
    for i in range(N + 1):
        t = i / N
        c = ctr(t)
        ch = chord * (1 - t) ** 0.55 + 9
        th = ch * 0.42 * max(0.0, 1 - abs(V[1]) / (0.55 * vl))   # pointing at the viewer: show the broad side
        lead.append((c[0] + ch * 0.36 + n[0] * th, c[1] - ch * 0.08 + n[1] * th))
        dep = 0.0
        if t > 0.42:        # rounded feather tips (scallops with small notches between them)
            dep = (7 if round_ else 6) * abs(math.sin(math.pi * (t - 0.42) / 0.145))
        trail.append((c[0] - ch * 0.64 - dep * 0.8 - n[0] * th, c[1] + ch * 0.08 + dep * 0.6 - n[1] * th))
    tip = ctr(1.04)
    pts = lead + [(tip[0] + V[0] / vl * 6, tip[1] + V[1] / vl * 6)] + list(reversed(trail))
    d = _sm(pts, closed=True, tension=0.75)
    out = _p(d, col, 0)
    inner = ""
    if tip_col:
        a = [ctr(0.66)]
        cut = [(ctr(0.66)[0] + chord * 0.8, ctr(0.66)[1]), (ctr(0.66)[0] - chord * 1.2, ctr(0.66)[1])]
        far_ = [(tip[0] + V[0] / vl * 60 - chord, tip[1] + V[1] / vl * 60), (tip[0] + V[0] / vl * 60 + chord, tip[1] + V[1] / vl * 60)]
        inner += _p(_poly([cut[0], cut[1], far_[0], far_[1]]), tip_col, 0)
    for k in (0.42, 0.62):          # two soft feather lines
        p0, p1 = ctr(k * 0.4), ctr(k + 0.25)
        inner += _p(f"M{_f(p0[0] - chord * 0.3)},{_f(p0[1] + 4)} Q{_f(p1[0] - chord * 0.35)},{_f(p1[1])} "
                    f"{_f(p1[0] - chord * 0.1)},{_f(p1[1] + 2)}", sw=2.4, stroke=S.shade(col, -0.25), extra='opacity="0.6"')
    out += _clip(_uid("wing", round(elev, 2), side, length, col), d, inner)
    return out + _p(d, sw=3.5)


def _bird(kind="gull", wing=0.0, pose="fly"):
    wv = _clamp(wing, -1, 1)
    if kind == "dove":
        bodyc, wingc, tipc, beak, feet = "#f6f0e4", "#d9d1e2", "#a99cbc", "#e7a08f", "#e58f8f"
        L, hr, wl = 0.82, 17, 118
    else:
        bodyc, wingc, tipc, beak, feet = "#f7f2e7", "#b9c4cb", "#5f6a74", "#f2b84b", "#f09a4a"
        L, hr, wl = 1.0, 16, 132
    out = ""
    body = [(-62 * L, 4), (-30 * L, -14), (10 * L, -18), (34 * L, -10), (40 * L, 6), (20 * L, 20), (-20 * L, 18),
            (-58 * L, 12)]
    tail = [(-50 * L, 0), (-84 * L, -6), (-90 * L, 6), (-84 * L, 14), (-50 * L, 12)]
    head = (42 * L, -16)
    if pose == "stand":
        body = [(-48 * L, -8), (-22 * L, -24), (12 * L, -24), (32 * L, -12), (34 * L, 6), (16 * L, 22), (-16 * L, 22),
                (-44 * L, 6)]
        tail = [(-40 * L, -4), (-74 * L, 8), (-76 * L, 18), (-66 * L, 22), (-36 * L, 12)]
        head = (36 * L, -26)
        for lx in (-6, 8):
            out += _line(lx, 18, lx + 2, 46, sw=6.5, color=INK) + _line(lx, 18, lx + 2, 46, sw=2.8, color=feet)
            out += _p(f"M{lx - 8},48 L{lx + 2},44 L{lx + 14},48 Z", feet, 2.5)
    sh = (-4 * L, -12 if pose == "fly" else -14)
    if pose == "fly":
        elev = 72 * wv if wv >= 0 else 52 * wv
        elev = elev + 14 * (1 - abs(wv))          # level glide keeps a slight upward dihedral
        out += _wing((sh[0] + 4, sh[1] - 6), elev + 4, -1, wl * 0.95, S.shade(wingc, -0.15),
                     S.shade(tipc, -0.1) if kind == "gull" else None, kind == "dove", 40 * L)
    out += _p(_sm(tail, closed=True, tension=0.6), S.mix(bodyc, wingc, 0.4) if kind == "dove" else bodyc, 3.5)
    if kind == "gull":
        out += _clip(_uid("gtail", pose), _sm(tail, closed=True, tension=0.6),
                     _rect(-100 * L, -20, 22 * L, 50, tipc, 0))
        out += _p(_sm(tail, closed=True, tension=0.6), sw=3.5)
    out += _p(_sm(body, closed=True), bodyc, 3.8)
    out += _circ(head[0], head[1], hr, bodyc, 3.8)
    bx = head[0] + hr - 3
    if kind == "dove":
        out += _p(f"M{_f(bx)},{_f(head[1] - 2)} L{_f(bx + 12)},{_f(head[1] + 3)} L{_f(bx)},{_f(head[1] + 6)} Z", beak, 2.8)
    else:
        out += _p(f"M{_f(bx)},{_f(head[1] - 4)} L{_f(bx + 24)},{_f(head[1] + 1)} Q{_f(bx + 22)},{_f(head[1] + 8)} "
                  f"{_f(bx)},{_f(head[1] + 6)} Z", beak, 2.8)
        out += _circ(bx + 17, head[1] + 4, 2.2, "#d9544d", 0)
    out += _dot_eye(head[0] + 5, head[1] - 4, 3.6)
    out += _blush(head[0] + 4, head[1] + 6, 5, 3, 0.55)
    if pose == "fly":
        out += _wing(sh, elev, 1, wl, wingc, tipc if kind == "gull" else None, kind == "dove", 44 * L)
    else:
        fw = [(-16 * L, -16), (20 * L, -16), (26 * L, -2), (0, 10), (-40 * L, 10), (-62 * L, 4)]
        out += _p(_sm(fw, closed=True, tension=0.7), wingc, 3.5)
        out += _clip(_uid("fw", kind), _sm(fw, closed=True, tension=0.7), _rect(-70 * L, -30, 34 * L, 50, tipc, 0))
        out += _p(_sm(fw, closed=True, tension=0.7), sw=3.5)
        out += _p(f"M{-10 * L},-6 Q{6 * L},-2 {14 * L},-8 M{-24 * L},2 Q{-6 * L},6 {6 * L},2", sw=2.5,
                  stroke=S.shade(wingc, -0.3))
    if pose == "fly":
        for lx in (-36, -28):
            out += _p(f"M{lx * L},{16} L{(lx - 16) * L},{22}", sw=5, stroke=INK) + _p(
                f"M{lx * L},{16} L{(lx - 16) * L},{22}", sw=2, stroke=feet)
    return out


def gull(x, y, scale=1.0, facing=1, wing=0.0, pose="fly"):
    return _place(_bird("gull", wing, pose), x, y, scale * 0.82, facing)


def dove(x, y, scale=1.0, facing=1, wing=0.0, pose="fly"):
    return _place(_bird("dove", wing, pose), x, y, scale * 0.75, facing)


FISH_COLORS = {"orange": "#f0a04b", "yellow": "#f2cf5b", "pink": "#e98f9f", "teal": "#5fb3a8",
               "purple": "#9d86c6", "blue": "#7fb6d6", "red": "#e06a55"}


def _small_fish(color="orange", tail=0.0):
    col = FISH_COLORS.get(color, color)
    dark, light = S.shade(col, -0.3), S.shade(col, 0.45)
    out = ""
    out += _g(_p(_sm([(-26, -4), (-50, -22), (-56, -12), (-50, 0), (-56, 12), (-50, 22), (-26, 4)], closed=True), col, 3.2),
              f"rotate({18 * _clamp(tail, -1, 1):.1f} -28 0)")
    out += _p("M-14,-18 Q-2,-34 14,-20 Z", dark, 3)
    out += _p("M-6,16 Q2,28 10,18 Z", dark, 3)
    body = [(-30, 0), (-18, -18), (10, -22), (32, -10), (38, 2), (28, 15), (4, 22), (-20, 16)]
    bd = _sm(body, closed=True)
    out += _p(bd, col, 0)
    out += _clip(_uid("sf", col), bd, _p("M-20,-30 Q-26,0 -16,30 L-6,30 Q-16,0 -10,-30 Z M2,-30 Q-4,0 6,30 L14,30 Q4,0 10,-30 Z",
                                         light, 0, extra='opacity="0.75"') +
                 _ell(6, 18, 34, 9, light, 0, extra='opacity="0.6"'))
    out += _p(bd, sw=3.2)
    out += _eye(20, -5, 9, "open", look=(0.6, 0.0), sw=2.5)
    out += _p("M31,8 Q34,11 37,8", sw=2.2)
    out += _blush(24, 8, 5, 3, 0.7)
    return out


def small_fish(x, y, scale=1.0, facing=1, color="orange", tail=0.0):
    return _place(_small_fish(color, tail), x, y, scale, facing)


def _leg(x, top, bottom, w, col, hoof=None, knee=None):
    hoof = hoof or S.shade(col, -0.55)
    out = _p(f"M{_f(x - w / 2)},{_f(top)} L{_f(x - w / 2 + 1)},{_f(bottom - 4)} Q{_f(x)},{_f(bottom + 1)} "
             f"{_f(x + w / 2 - 1)},{_f(bottom - 4)} L{_f(x + w / 2)},{_f(top)} Z", col, 3.5)
    out += _p(f"M{_f(x - w / 2 - 1)},{_f(bottom - 10)} L{_f(x + w / 2 + 1)},{_f(bottom - 10)} L{_f(x + w / 2 + 1)},{_f(bottom)} "
              f"L{_f(x - w / 2 - 1)},{_f(bottom)} Z", hoof, 3)
    if knee:
        out += _ell(x, knee, w * 0.62, w * 0.5, col, 3)
    return out


def _qleg(hip, foot_x, w0, w1, col, hind=False, far=False, ground=0.0, hoof="hoof", knob=0.0, bend=1.0):
    """Tapered animal leg from the hip/shoulder point to a hoof on the ground at foot_x. Hind legs bend back at
    the hock, front legs bow slightly forward at the knee. far=True: the other side of the animal (darker,
    a little higher). hoof: 'hoof' | 'cloven' | 'pad' (camel). knob>0 adds a knobbly knee."""
    if far:
        col = S.shade(col, -0.2)
        ground -= 5
    hx, hy = hip
    L = ground - hy
    hh = max(9.0, w1 * 0.95) if hoof != "pad" else max(8.0, w1 * 0.6)
    fet = (foot_x, ground - hh + 2)
    if hind:
        knee = (_lerp(hx, foot_x, 0.45) - 0.13 * L * bend, hy + 0.56 * L)
    else:
        knee = (_lerp(hx, foot_x, 0.55) + 0.04 * L * bend, hy + 0.5 * L)
    top = (hx + (hx - knee[0]) * 0.15, hy - 0.12 * L)
    path = [top, hip, knee, fet]
    N = 16
    pts = []
    for i in range(N + 1):            # sample a Catmull-Rom curve through the joints
        t = i / N * 3
        k = min(2, int(t))
        u = t - k
        p0, p1, p2, p3 = path[max(0, k - 1)], path[k], path[k + 1], path[min(3, k + 2)]
        pts.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u * u +
                                (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u ** 3) for j in (0, 1)))
    left, right = [], []
    for i, p in enumerate(pts):
        q0, q1 = pts[max(0, i - 1)], pts[min(N, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        t = i / N
        wv = _lerp(w0, w1, min(1.0, t * 1.15) ** 0.75) / 2
        wv += knob * w1 * 0.5 * math.exp(-((t - 0.62) / 0.07) ** 2)
        left.append((p[0] + nx * wv, p[1] + ny * wv))
        right.append((p[0] - nx * wv, p[1] - ny * wv))
    out = _p(_sm(left + list(reversed(right)), closed=True, tension=0.7), col, 3.5)
    hc = S.shade(col, -0.5) if hoof != "pad" else S.shade(col, -0.12)
    fx, gy = foot_x, ground
    if hoof == "pad":
        out += _p(f"M{_f(fx - w1 * 0.6)},{_f(gy - hh)} Q{_f(fx - w1 * 1.25)},{_f(gy + 1)} {_f(fx - w1 * 0.2)},{_f(gy)} "
                  f"L{_f(fx + w1 * 0.9)},{_f(gy)} Q{_f(fx + w1 * 1.45)},{_f(gy - 1)} {_f(fx + w1 * 0.6)},{_f(gy - hh)} Z",
                  hc, 3.2)
    else:
        hw0, hw1 = w1 * 0.55, w1 * 0.68
        out += _p(f"M{_f(fx - hw0)},{_f(gy - hh)} L{_f(fx + hw0)},{_f(gy - hh)} Q{_f(fx + hw1 + 2)},{_f(gy - hh * 0.4)} "
                  f"{_f(fx + hw1)},{_f(gy)} L{_f(fx - hw1)},{_f(gy)} Q{_f(fx - hw1 - 2)},{_f(gy - hh * 0.4)} Z", hc, 3.2)
        if hoof == "cloven":
            out += _line(fx + 1, gy - hh * 0.5, fx + 1, gy - 1, sw=2.2, color=S.shade(hc, 0.35))
    return out


def _body(pts, fill, patches="", belly=None, uid="body"):
    d = _sm(pts, closed=True)
    inner = patches
    if belly:
        inner += belly
    return _p(d, fill, 0) + (_clip(_uid(uid, len(pts), pts[0]), d, inner) if inner else "") + _p(d, sw=4)


def _sackcloth(x0, x1, ytop, ybot, sag=14, seed=0):
    rng = random.Random(seed)
    col, dark = P["sackcloth"], P["sackcloth_dark"]
    mid = (x0 + x1) / 2
    top = [(x0, ytop + sag), (mid - (x1 - x0) * 0.25, ytop + 2), (mid, ytop), (mid + (x1 - x0) * 0.25, ytop + 2),
           (x1, ytop + sag)]
    bot = []
    n = 9
    for i in range(n + 1):
        u = i / n
        bot.append((_lerp(x1 + 4, x0 - 4, u), ybot + (8 if i % 2 else 0) + rng.uniform(-3, 3)))
    d = _sm(top, closed=False) + " " + " ".join(f"L{_f(px)},{_f(py)}" for px, py in bot) + " Z"
    inner = ""
    for xx in range(int(x0) - 10, int(x1) + 10, 9):
        inner += _line(xx, ytop - 10, xx + 4, ybot + 12, sw=1.6, color=dark, extra='opacity="0.35"')
    for yy in range(int(ytop), int(ybot) + 10, 9):
        inner += _line(x0 - 10, yy, x1 + 10, yy + 2, sw=1.6, color=dark, extra='opacity="0.3"')
    px, py = mid + (x1 - x0) * 0.18, (ytop + ybot) / 2
    inner += _rect(px - 10, py - 8, 20, 16, S.shade(col, 0.2), 2, extra=f'transform="rotate(8 {_f(px)} {_f(py)})"')
    inner += _p(f"M{_f(px - 9)},{_f(py - 6)} l4,0 m4,0 l4,0 m4,0 l3,0", sw=1.8, stroke=dark)
    out = _p(d, col, 0) + _clip(_uid("sackc", x0, x1, ytop, ybot), d, inner) + _p(d, sw=3.5)
    out += _p(f"M{_f(mid - 2)},{_f(ytop + 2)} Q{_f(mid + 4)},{_f((ytop + ybot) / 2)} {_f(mid)},{_f(ybot + 4)}", sw=6,
              stroke=INK) + _p(f"M{_f(mid - 2)},{_f(ytop + 2)} Q{_f(mid + 4)},{_f((ytop + ybot) / 2)} {_f(mid)},{_f(ybot + 4)}",
                               sw=3, stroke=P["wood_light"])
    return out


def _animal(kind="sheep", sackcloth=False):
    out = ""
    if kind == "sheep":
        wool, face, leg = "#f6efe0", "#dcb89c", "#6b5040"
        for lx in (-28, 44):
            out += _leg(lx, -46, 0, 13, S.shade(leg, -0.15))
        circles = [(-74, -84, 16)]
        for i in range(12):
            a = 2 * math.pi * i / 12
            circles.append((70 * math.cos(a) * 0.95, -80 + 38 * math.sin(a), 24))
        circles.append((0, -80, 52))
        for lx in (-46, 24):
            out += _leg(lx, -46, 0, 14, leg)
        out += _cluster(circles, wool, 3.8)
        for cx, cy in ((-30, -96), (10, -104), (-10, -72), (30, -78), (-46, -70)):
            out += _p(f"M{cx - 8},{cy} q4,-7 8,0 q4,7 8,0", sw=2.4, stroke=S.shade(wool, -0.2))
        if sackcloth:
            out += _sackcloth(-56, 50, -126, -60, 18, 1)
        out += _ell(54, -110, 17, 8, face, 3.4, extra='transform="rotate(-24 54 -110)"')
        out += _ell(76, -96, 25, 31, face, 3.8, extra='transform="rotate(22 76 -96)"')
        out += _ell(104, -112, 16, 7, S.shade(face, -0.08), 3.4, extra='transform="rotate(28 104 -112)"')
        out += _cluster([(62, -124, 12), (74, -128, 13), (86, -122, 11)], wool, 3.2)
        out += _dot_eye(84, -100, 4.2) + _blush(88, -88, 6, 3.6)
        out += _p("M91,-80 Q95,-76 99,-80", sw=2.6)
        return out
    if kind == "goat":
        coat, patch, horn = "#ece0c8", "#a8784e", "#a8957d"
        out += _qleg((-40, -96), -44, 24, 11, coat, hind=True, far=True, hoof="cloven", bend=0.6)
        out += _qleg((52, -96), 60, 22, 11, coat, far=True, hoof="cloven", bend=0.4)
        out += _qleg((-58, -94), -62, 26, 12, coat, hind=True, hoof="cloven", bend=0.6)
        out += _qleg((38, -94), 44, 24, 12, coat, hoof="cloven", bend=0.4)
        out += _p("M-80,-124 Q-98,-146 -86,-156 Q-74,-144 -70,-124 Z", coat, 3.4)          # perky tail
        bd = [(-86, -108), (-76, -136), (-40, -148), (0, -144), (40, -148), (68, -142), (86, -118), (80, -92),
              (50, -76), (0, -70), (-50, -74), (-82, -88)]
        belly = _p(_sm([(-70, -84), (0, -90), (70, -86), (70, -50), (-70, -50)]), S.shade(coat, 0.25), 0)
        out += _body(bd, coat, _ell(-36, -124, 30, 20, patch, 0) + _ell(26, -82, 22, 11, patch, 0), belly, "goat")
        if sackcloth:
            out += _sackcloth(-60, 48, -146, -88, 12, 2)
        out += _p("M50,-136 Q62,-172 82,-186 L104,-166 Q84,-146 80,-106 Z", coat, 3.8)    # neck
        out += _tube("M80,-198 Q72,-226 54,-232 Q42,-234 42,-222", 9, horn, 3.2)
        out += _tube("M92,-200 Q90,-230 74,-242 Q62,-246 60,-234", 9, S.shade(horn, 0.15), 3.2)
        out += _ell(68, -186, 17, 7, coat, 3.2, extra='transform="rotate(26 68 -186)"')
        out += _p(_sm([(78, -202), (100, -202), (116, -182), (120, -160), (110, -148), (92, -152), (80, -172)]), coat, 3.8)
        out += _ell(90, -192, 9, 7, patch, 0, extra='opacity="0.8"')
        out += _p("M106,-150 Q110,-132 102,-124 Q96,-136 96,-150 Z", S.shade(coat, -0.15), 3)      # beard
        out += _dot_eye(98, -182, 4) + _blush(104, -168, 5, 3)
        out += _p("M112,-156 Q115,-153 118,-156", sw=2.4)
        return out
    if kind == "cow":
        coat, patch, muzzle = "#f3ead8", "#9b6542", "#f0b2b0"
        out += _qleg((-70, -100), -74, 38, 21, coat, hind=True, far=True, hoof="cloven", bend=0.5)
        out += _qleg((74, -100), 84, 36, 20, coat, far=True, hoof="cloven", bend=0.3)
        out += _qleg((-90, -98), -94, 40, 22, coat, hind=True, hoof="cloven", bend=0.5)
        out += _qleg((56, -98), 62, 38, 22, coat, hoof="cloven", bend=0.3)
        out += _p("M-118,-152 Q-136,-112 -130,-78", sw=7, stroke=INK) + _p("M-118,-152 Q-136,-112 -130,-78", sw=3,
                                                                           stroke=coat)
        out += _p("M-130,-86 Q-142,-68 -130,-60 Q-118,-68 -130,-86 Z", patch, 3)
        bd = [(-124, -124), (-114, -164), (-70, -182), (-10, -178), (50, -184), (100, -174), (126, -144),
              (120, -104), (84, -82), (20, -70), (-50, -74), (-100, -90)]
        belly = _p(_sm([(-110, -94), (0, -100), (110, -100), (110, -50), (-110, -50)]), S.shade(coat, 0.3), 0)
        pt = _ell(-62, -148, 42, 28, patch, 0) + _ell(46, -118, 32, 26, patch, 0) + _ell(-104, -104, 18, 16, patch, 0)
        out += _body(bd, coat, pt, belly, "cow")
        out += _ell(-22, -72, 14, 7, muzzle, 3)                                              # little udder
        if sackcloth:
            out += _sackcloth(-88, 74, -186, -104, 18, 3)
        out += _tube("M118,-190 Q104,-206 110,-218", 8, "#efe2c0", 3) + _tube("M160,-192 Q174,-206 168,-218", 8,
                                                                              "#efe2c0", 3)
        out += _ell(104, -174, 19, 9, coat, 3.4, extra='transform="rotate(-20 104 -174)"')
        out += _ell(174, -176, 19, 9, coat, 3.4, extra='transform="rotate(20 174 -176)"')
        out += _p(_sm([(114, -188), (160, -190), (170, -154), (160, -126), (120, -126), (108, -154)]), coat, 4)
        out += _ell(140, -178, 15, 10, patch, 0, extra='opacity="0.9"')
        out += _ell(140, -122, 30, 19, muzzle, 3.8)
        out += _ell(130, -122, 3.4, 4, S.shade(muzzle, -0.5), 0) + _ell(150, -122, 3.4, 4, S.shade(muzzle, -0.5), 0)
        out += _dot_eye(127, -158, 4.6) + _dot_eye(153, -158, 4.6)
        out += _blush(118, -142, 6, 3.5) + _blush(162, -142, 6, 3.5)
        return out
    if kind == "donkey":
        coat, light, dark = "#aaa39b", "#e2d9cb", "#5e554e"
        out += _qleg((-58, -118), -62, 30, 13, coat, hind=True, far=True, bend=0.6)
        out += _qleg((64, -118), 74, 28, 13, coat, far=True, bend=0.4)
        out += _qleg((-74, -116), -78, 32, 14, coat, hind=True, bend=0.6)
        out += _qleg((50, -116), 54, 30, 14, coat, bend=0.4)
        out += _p("M-96,-166 Q-110,-126 -106,-96", sw=7, stroke=INK) + _p("M-96,-166 Q-110,-126 -106,-96", sw=3,
                                                                          stroke=coat)
        out += _p("M-106,-106 Q-118,-86 -106,-76 Q-94,-86 -106,-106 Z", dark, 3)
        bd = [(-102, -146), (-88, -178), (-40, -188), (10, -182), (60, -190), (92, -172), (102, -142), (88, -112),
              (40, -98), (-20, -96), (-76, -106)]
        belly = _p(_sm([(-90, -118), (0, -118), (95, -122), (95, -80), (-90, -80)]), light, 0)
        out += _body(bd, coat, "", belly, "donk")
        if sackcloth:
            out += _sackcloth(-72, 62, -192, -118, 16, 4)
        out += _p("M58,-180 Q80,-220 102,-240 L134,-214 Q106,-182 96,-132 Z", coat, 4)          # neck
        out += _p("M66,-186 Q86,-224 106,-246", sw=12, stroke=INK) + _p("M66,-186 Q86,-224 106,-246", sw=6, stroke=dark)
        for ex, rot in ((110, -16), (126, 12)):
            out += _ell(ex, -268, 10, 34, coat, 3.6, extra=f'transform="rotate({rot} {ex} -240)"')
            out += _ell(ex, -278, 4.5, 18, "#d7b2a8", 0, extra=f'transform="rotate({rot} {ex} -240)"')
            out += _p(f"M{ex - 9},-292 Q{ex},-308 {ex + 9},-292 Z", dark, 2.5, extra=f'transform="rotate({rot} {ex} -240)"')
        out += _ell(128, -214, 26, 30, coat, 4)
        out += _ell(142, -186, 26, 19, light, 3.8, extra='transform="rotate(20 142 -186)"')
        out += _circ(148, -186, 2.6, INK, 0) + _circ(158, -182, 2.6, INK, 0)
        out += _dot_eye(136, -220, 4.4) + _blush(142, -204, 6, 3.5)
        out += _p("M144,-174 Q150,-170 156,-174", sw=2.5)
        return out
    if kind == "camel":
        coat, dark = "#d9ad72", "#b48650"
        out += _qleg((-80, -222), -84, 46, 16, coat, hind=True, far=True, hoof="pad", knob=1.6, bend=0.55)
        out += _qleg((92, -222), 100, 42, 16, coat, far=True, hoof="pad", knob=1.6, bend=0.35)
        out += _qleg((-100, -220), -104, 48, 17, coat, hind=True, hoof="pad", knob=1.6, bend=0.55)
        out += _qleg((74, -220), 80, 44, 17, coat, hoof="pad", knob=1.6, bend=0.35)
        out += _p("M-130,-268 Q-146,-232 -140,-200", sw=7, stroke=INK) + _p("M-130,-268 Q-146,-232 -140,-200", sw=3,
                                                                            stroke=coat)
        out += _ell(-140, -194, 6, 11, dark, 3)
        # long curved neck: forward and down from the chest, then up to the head
        out += _p(_sm([(96, -296), (146, -280), (184, -270), (210, -296), (220, -342), (228, -388), (256, -396),
                       (254, -362), (244, -314), (230, -262), (200, -228), (150, -222), (110, -232)]), coat, 4)
        bd = [(-136, -248), (-130, -282), (-104, -300), (-72, -310), (-54, -336), (-34, -382), (-4, -404), (26, -390),
              (48, -350), (64, -316), (92, -306), (124, -292), (136, -262), (120, -228), (60, -208), (-20, -200),
              (-92, -206), (-128, -224)]
        belly = _p(_sm([(-120, -232), (0, -228), (130, -236), (130, -180), (-120, -180)]), S.shade(coat, 0.18), 0)
        shine = _p("M-50,-344 Q-26,-388 12,-392", sw=6, stroke=S.shade(coat, 0.3), extra='opacity="0.8"')
        shine += _p("M-60,-318 Q-4,-300 56,-318", sw=3, stroke=dark, extra='opacity="0.35"')
        out += _body(bd, coat, shine, belly, "camel")
        if sackcloth:
            out += _sackcloth(-74, 64, -402, -246, 104, 5)
        # head
        out += _ell(234, -406, 8, 12, coat, 3.2, extra='transform="rotate(-20 234 -406)"')
        out += _p(_sm([(220, -410), (258, -416), (284, -402), (292, -380), (278, -368), (248, -372), (224, -384)]),
                  coat, 4)
        out += _p("M278,-372 Q292,-364 294,-378", sw=2.5)
        out += _p("M248,-400 Q255,-404 262,-400", sw=3) + _p("M248,-400 Q255,-395 262,-400 Z", PUPIL, 0)
        out += _p("M250,-403 l-3,-5 M255,-404 l0,-6 M260,-403 l3,-5", sw=2)
        out += _blush(264, -386, 6, 3.6)
        return out
    raise ValueError(f"unknown animal kind {kind!r}")


def animal(x, y, scale=1.0, facing=1, kind="sheep", sackcloth=False):
    return _place(_animal(kind, sackcloth), x, y, scale, facing)


# ====================================================================== 6. buildings

_WALL = {"stone": P["stone"], "sand": P["sand"], "terra": S.mix(P["sand"], P["terracotta"], 0.3)}


def _box3d(x0, x1, y0, y1, col, depth=34, sw=4.0):
    """Front face + right side face + roof top, slight 3/4 view. y0 bottom (ground), y1 top."""
    dx, dy = depth, -depth * 0.55
    side = _poly([(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)])
    roof = _poly([(x0, y1), (x0 + dx, y1 + dy), (x1 + dx, y1 + dy), (x1, y1)])
    front = _sm([(x0, y0), (x0 - 1, (y0 + y1) / 2), (x0, y1), ((x0 + x1) / 2, y1 - 1), (x1, y1), (x1 + 1, (y0 + y1) / 2),
                 (x1, y0)], closed=True, tension=0.3)
    return (_p(side, S.shade(col, -0.22), sw) + _p(roof, S.shade(col, 0.22), sw) + _p(front, col, sw))


def _window(cx, top, w=28, h=38, col=None):
    col = col or "#5b4232"
    return (_p(f"M{_f(cx - w / 2)},{_f(top + h)} L{_f(cx - w / 2)},{_f(top + w / 2)} Q{_f(cx - w / 2)},{_f(top)} {_f(cx)},{_f(top)} "
               f"Q{_f(cx + w / 2)},{_f(top)} {_f(cx + w / 2)},{_f(top + w / 2)} L{_f(cx + w / 2)},{_f(top + h)} Z", col, 3.5)
            + _rect(cx - w / 2 - 6, top + h - 2, w + 12, 8, P["wood"], 3, rx=2))


def _door(cx, w=70, h=150, col=None):
    col = col or P["wood"]
    out = _p(f"M{_f(cx - w / 2)},0 L{_f(cx - w / 2)},{_f(-h + w / 2)} Q{_f(cx - w / 2)},{_f(-h)} {_f(cx)},{_f(-h)} "
             f"Q{_f(cx + w / 2)},{_f(-h)} {_f(cx + w / 2)},{_f(-h + w / 2)} L{_f(cx + w / 2)},0 Z", col, 4)
    for k in (-1, 1):
        out += _line(cx + k * w / 6, -h + 12, cx + k * w / 6, -4, sw=2.5, color=S.shade(col, -0.35))
    out += _circ(cx + w / 2 - 12, -h * 0.45, 4, P["crown"], 2.2)
    return out


def _bricks(x0, x1, y0, y1, col, seed, n=6):
    rng = random.Random(seed)
    out = ""
    for _ in range(n):
        bx, by = rng.uniform(x0, x1 - 40), rng.uniform(y1 + 10, y0 - 30)
        for r_ in range(rng.randint(2, 3)):
            for c in range(rng.randint(1, 3)):
                out += _rect(bx + c * 26 + (13 if r_ % 2 else 0), by + r_ * 13, 24, 11, "none", 2,
                             stroke=S.shade(col, -0.3), extra='opacity="0.6"')
    return out


def _house(variant=0):
    v = variant % 4
    out = ""
    if v == 0:
        w, h, col = 280, 232, _WALL["stone"]
        x0, x1 = -w / 2, w / 2
        out += _box3d(x0, x1, 0, -h, col)
        out += _p(f"M{x0 - 6},{-h} L{x1 + 6},{-h} L{x1 + 6},{-h + 16} L{x0 - 6},{-h + 16} Z", S.shade(col, 0.12), 3.5)
        for bx in range(int(x0) + 26, int(x1), 46):
            out += _circ(bx, -h + 30, 6, P["wood_dark"], 2.5)
        out += _bricks(x0 + 10, x1 - 10, 0, -h, col, 1)
        out += _door(-40, 72, 150) + _window(70, -170)
        out += _g(_amphora(0, P["terracotta"]), f"translate({x1 - 30},{-h - 30}) scale(0.38)")
        out += _ell(0, -6, w * 0.45, 5, S.shade(col, -0.18), 0, extra='opacity="0.5"')
    elif v == 1:
        w, h, col = 230, 384, _WALL["sand"]
        x0, x1 = -w / 2, w / 2
        out += _box3d(x0, x1, 0, -h, col)
        out += _p(f"M{x0 - 6},{-h} L{x1 + 6},{-h} L{x1 + 6},{-h + 16} L{x0 - 6},{-h + 16} Z", S.shade(col, 0.12), 3.5)
        out += _line(x0 + 4, -196, x1 - 4, -196, sw=3, color=S.shade(col, -0.25))
        for bx in range(int(x0) + 24, int(x1), 44):
            out += _circ(bx, -h + 30, 5.5, P["wood_dark"], 2.5)
            out += _circ(bx, -184, 5.5, P["wood_dark"], 2.5)
        out += _bricks(x0 + 10, x1 - 10, 0, -h, col, 2, 5)
        out += _door(40, 68, 146) + _window(-50, -150) + _window(-30, -320, 30, 40) + _window(50, -320, 30, 40)
        # awning over upper window
        out += _p("M-10,-338 L90,-338 L100,-306 L-20,-306 Z", P["jonah_sash"], 3.5)
        for k in range(4):
            out += _p(f"M{-14 + k * 30},-306 q15,14 30,0", P["jonah_sash"], 3)
        # external stair on the left
        st = [(x0, 0)]
        for k in range(7):
            st += [(x0 - 70 + k * 10, -k * 28), (x0 - 70 + k * 10, -(k + 1) * 28)]
        stair = _poly([(x0 - 80, 0)] + st[1:] + [(x0, -196), (x0, 0)])
        out += _p(stair, S.shade(col, -0.1), 3.5)
    elif v == 2:
        w, h, col = 340, 238, _WALL["terra"]
        x0, x1 = -w / 2, w / 2
        # rooftop shelter behind parapet
        for px in (x1 - 120, x1 - 20):
            out += _tube(f"M{px},{-h - 10} L{px},{-h - 92}", 6, P["wood"], 3)
        out += _p(f"M{x1 - 134},{-h - 92} L{x1 - 6},{-h - 92} L{x1 + 2},{-h - 70} L{x1 - 142},{-h - 70} Z",
                  P["sail"], 3.5)
        out += _line(x1 - 138, -h - 80, x1 - 2, -h - 80, sw=5, color=P["sail_stripe"])
        out += _box3d(x0, x1, 0, -h, col)
        out += _p(f"M{x0 - 6},{-h} L{x1 + 6},{-h} L{x1 + 6},{-h + 18} L{x0 - 6},{-h + 18} Z", S.shade(col, 0.12), 3.5)
        out += _bricks(x0 + 10, x1 - 10, 0, -h, col, 3, 5)
        out += _door(-70, 74, 152)
        # striped awning over door
        out += _p("M-122,-176 L-18,-176 L-4,-140 L-136,-140 Z", P["sail"], 3.5)
        for k in range(3):
            out += _p(f"M{-112 + k * 36},-176 L{-96 + k * 36},-176 L{-88 + k * 38},-140 L{-106 + k * 38},-140 Z",
                      P["sail_stripe"], 0)
        out += _p("M-122,-176 L-18,-176 L-4,-140 L-136,-140 Z", sw=3.5)
        for px in (-130, -10):
            out += _line(px, -140, px, 0, sw=4, color=P["wood_dark"])
        out += _window(60, -172) + _window(120, -172)
        for px in (40, 76):
            out += _g(_lots_jar(0), f"translate({px},0) scale(0.45)")
    else:
        w, h, col = 262, 270, S.mix(_WALL["stone"], P["sand_light"], 0.4)
        x0, x1 = -w / 2, w / 2
        out += _box3d(x0, x1, 0, -h, col)
        out += _p(f"M{x0 - 6},{-h} L{x1 + 6},{-h} L{x1 + 6},{-h + 16} L{x0 - 6},{-h + 16} Z", S.shade(col, 0.12), 3.5)
        # palm-frond lean-to on the roof
        out += _frond((x0 + 30, -h - 60), -8, 140, 22, 22, P["leaf_dark"])
        out += _frond((x0 + 30, -h - 52), 4, 150, 26, 22, P["leaf"])
        out += _tube(f"M{x0 + 34},{-h} L{x0 + 34},{-h - 60}", 5, P["wood"], 3)
        out += _tube(f"M{x0 + 150},{-h} L{x0 + 150},{-h - 50}", 5, P["wood"], 3)
        out += _bricks(x0 + 10, x1 - 10, 0, -h, col, 4, 4)
        out += _p("M-30,0 L-30,-110 Q-30,-160 20,-160 Q70,-160 70,-110 L70,0 Z", P["wood"], 4)
        out += _p("M20,-160 L20,0", sw=2.5, stroke=P["wood_dark"])
        out += _window(-80, -200, 26, 34)
        # laundry line
        out += _p(f"M{x0 + 10},-{h - 40} Q{0},-{h - 58} {x1 - 10},-{h - 40}", sw=2.2, stroke=P["ink_soft"])
        for px, c in ((-80, P["jonah_sash"]), (-30, P["sail_stripe"]), (40, P["headcloth"])):
            out += _p(f"M{px - 14},{-h + 50} L{px + 14},{-h + 51} L{px + 12},{-h + 84} L{px - 12},{-h + 82} Z", c, 3)
        out += _g(_bush(0), f"translate({x1 + 30},0) scale(0.45)")
    return out


HOUSE_K = 2.2


def house(x, y, scale=1.0, variant=0, facing=1):
    return _place(_upscale(_house(variant), HOUSE_K), x, y, scale, facing)


def _merlons(x0, x1, ytop, col, mw=40, gap=16, mh=34, sw=4.0):
    out = ""
    n = max(1, int((x1 - x0 + gap) // (mw + gap)))
    span = n * mw + (n - 1) * gap
    sx = x0 + (x1 - x0 - span) / 2
    s3 = mw / 5
    for i in range(n):
        a = sx + i * (mw + gap)
        pts = [(a, ytop), (a, ytop - mh * 0.4), (a + s3, ytop - mh * 0.4), (a + s3, ytop - mh * 0.75),
               (a + 2 * s3, ytop - mh * 0.75), (a + 2 * s3, ytop - mh), (a + 3 * s3, ytop - mh),
               (a + 3 * s3, ytop - mh * 0.75), (a + 4 * s3, ytop - mh * 0.75), (a + 4 * s3, ytop - mh * 0.4),
               (a + mw, ytop - mh * 0.4), (a + mw, ytop)]
        out += _p(_poly(pts), col, sw)
    return out


def _rosette_band(x0, x1, yc, h=26):
    out = _rect(x0, yc - h / 2, x1 - x0, h, "#4f86b0", 3.5)
    k = h / 26
    n = max(1, int((x1 - x0) // (34 * k)))
    for i in range(n):
        cx = x0 + (i + 0.5) * (x1 - x0) / n
        for j in range(6):
            a = j * math.pi / 3
            out += _circ(cx + 5 * k * math.cos(a), yc + 5 * k * math.sin(a), 3.6 * k, "#f4e3b0", 0)
        out += _circ(cx, yc, 3 * k, P["crown"], 0)
    return out


def _brick_rows(a, b, top, y, k, color):
    out = ""
    for yy in range(int(top + 26 * k), int(y - 20 * k), max(8, int(26 * k))):
        out += _line(a + 3, yy, b - 3, yy, sw=1.8, color=color, extra='opacity="0.35"')
    return out


def _city_wall(x0, x1, y, height=260, gate=None, doors_open=0.0, towers=True, seed=0):
    col = P["sand"]
    dark = S.shade(col, -0.2)
    k = height / 260.0
    rng = random.Random(seed)
    out = ""
    top = y - height
    gx, gw = (gate if gate else (None, 0))
    gl, gr = (gx - gw / 2 - 120 * k, gx + gw / 2 + 120 * k) if gate else (None, None)
    segs = [(x0, x1)] if not gate else [(x0, gl), (gr, x1)]
    for a, b in segs:
        if b - a < 60 * k:      # too short for a wall piece: the gate tower is the end of the wall
            continue
        out += _merlons(a, b, top, col, 40 * k, 16 * k, 34 * k)
        out += _rect(a, top, b - a, height, col, 4)
        inner = _rect(a + 2, y - 26 * k, b - a - 4, 24 * k, S.shade(col, -0.12), 0)
        inner += _brick_rows(a, b, top, y, k, dark)
        for _ in range(int((b - a) / (140 * k)) + 1):
            bx = rng.uniform(a + 10, max(a + 11, b - 70 * k))
            by = rng.uniform(top + 30 * k, y - 60 * k)
            for r_ in range(2):
                for c in range(2 + r_):
                    inner += _rect(bx + (c * 28 + 14 * r_) * k, by + r_ * 13 * k, 26 * k, 12 * k, "none", 2, stroke=dark,
                                   extra='opacity="0.55"')
        out += _clip(_uid("wallseg", a, b, y, height, seed), _poly([(a, top), (b, top), (b, y), (a, y)]), inner)
        out += _rect(a, top, b - a, height, "none", 4)
        if towers:
            n = int((b - a) // (420 * k))
            for i in range(n):     # towers keep >= ~80k of plain wall to each end
                tx = a + (i + 0.5) * (b - a) / n
                tx = min(max(tx, a + 130 * k), b - 146 * k)
                out += _tower(tx, y, 96 * k, height + 56 * k, col, k)
    if gate:
        th = height * 1.45
        mid_top = y - height * 1.12
        out += _merlons(gl + 100 * k, gr - 100 * k, mid_top, col, 40 * k, 16 * k, 34 * k)
        out += _rect(gl + 100 * k, mid_top, gr - gl - 200 * k, y - mid_top, col, 4)
        out += _brick_rows(gl + 100 * k, gr - 100 * k, mid_top, y, k, dark)
        spring = y - height * 0.62
        r = gw / 2
        arch = f"M{gx - r},{y} L{gx - r},{spring} A{r},{r} 0 0 1 {gx + r},{spring} L{gx + r},{y} Z"
        o = _clamp(doors_open)
        out += _p(arch, "#4a3426", 0)
        if o > 0.01:
            r2 = r * 0.55
            out += _p(f"M{gx - r2},{y} L{gx - r2},{spring + 30 * k} A{r2},{r2} 0 0 1 {gx + r2},{spring + 30 * k} "
                      f"L{gx + r2},{y} Z", S.mix(P["sand_light"], P["sky_warm"], 0.4), 0,
                      extra=f'opacity="{min(1, o * 1.5):.2f}"')
        for side in (-1, 1):
            leaf_w = r * (1 - 0.82 * o)
            hx = gx + side * r
            xa, xb = sorted((hx, hx - side * leaf_w))
            leaf_ = _rect(xa, spring - r, xb - xa, y - spring + r, P["wood"], 0)
            for j in range(1, 4):
                px = xa + (xb - xa) * j / 4
                leaf_ += _line(px, spring - r, px, y, sw=2.5, color=P["wood_dark"])
            for yy in (spring - r * 0.3, (spring + y) / 2, y - 40 * k):
                leaf_ += _rect(xa, yy - 6 * k, xb - xa, 12 * k, S.shade(P["wood_dark"], -0.1), 0)
                for j in range(3):
                    leaf_ += _circ(xa + (xb - xa) * (j + 0.5) / 3, yy, 3.2 * k, P["crown"], 0)
            cid = _uid("gate", gx, gw, side, round(o, 3), y, height)
            out += _clip(cid, arch, leaf_ + _rect(xa, spring - r, xb - xa, y - spring + r, "none", 3.5))
        arch_o = f"M{gx - r},{y} L{gx - r},{spring} A{r},{r} 0 0 1 {gx + r},{spring} L{gx + r},{y}"
        out += f'<path d="{arch_o}" fill="none" stroke="{INK}" stroke-width="{30 * k:.1f}" stroke-linejoin="round"/>'
        out += (f'<path d="{arch_o}" fill="none" stroke="{S.shade(col, -0.1)}" stroke-width="{30 * k - 8:.1f}" '
                f'stroke-linejoin="round"/>')
        for j in range(9):
            a = math.pi * (j + 0.5) / 9
            out += _line(gx - (r + 4) * math.cos(a), spring - (r + 4) * math.sin(a), gx - (r + 15 * k) * math.cos(a),
                         spring - (r + 15 * k) * math.sin(a), sw=2.5, color=dark)
        out += _p(f"M{gx - r},{y} L{gx - r},{spring} A{r},{r} 0 0 1 {gx + r},{spring} L{gx + r},{y}", sw=4)
        out += _rosette_band(gl + 110 * k, gr - 110 * k, mid_top + 34 * k, 24 * k)
        out += _tower(gl + 60 * k, y, 120 * k, th, col, k, band=True)
        out += _tower(gr - 60 * k, y, 120 * k, th, col, k, band=True)
    return out


def _tower(cx, y, w, h, col, k=1.0, band=False):
    x0, x1 = cx - w / 2, cx + w / 2
    top = y - h
    out = _merlons(x0 - 6 * k, x1 + 6 * k, top, col, 40 * k, 16 * k, 34 * k)
    out += _p(_poly([(x1, y), (x1 + 16 * k, y - 8 * k), (x1 + 16 * k, top - 8 * k), (x1, top)]), S.shade(col, -0.22), 4)
    out += _rect(x0, top, w, h, S.shade(col, 0.06), 4)
    out += _rect(x0 + 2, y - 26 * k, w - 4, 24 * k, S.shade(col, -0.12), 0)
    out += _brick_rows(x0, x1, top, y, k, S.shade(col, -0.2))
    out += _rect(cx - 6 * k, top + 40 * k, 12 * k, 34 * k, "#4a3426", 3, rx=6 * k)
    if h > 260 * k:
        out += _rect(cx - 6 * k, top + 120 * k, 12 * k, 34 * k, "#4a3426", 3, rx=6 * k)
    if band:
        out += _rosette_band(x0 + 6 * k, x1 - 6 * k, top + 22 * k, 22 * k)
    out += _rect(x0, top, w, h, "none", 4)
    return out


def _ink(body, k):
    """Multiply every stroke width in markup by k (thinner / heavier ink without changing geometry)."""
    if abs(k - 1) < 1e-3:
        return body
    body = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) * k:.2f}"', body)
    return re.sub(r"stroke-width='([0-9.]+)'", lambda m: f"stroke-width='{float(m.group(1)) * k:.2f}'", body)


def city_wall(x0, x1, y, height=260, gate=None, doors_open=0.0, towers=True, seed=0, ink=1.0):
    return _place(_ink(_city_wall(x0, x1, y, height, gate, doors_open, towers, seed), ink), 0, 0, 1.0)


def _ziggurat():
    tiers = [(640, 150, P["sand"]), (470, 120, S.mix(P["sand"], P["stone"], 0.5)), (310, 104, P["stone"])]
    out = ""
    y = 0
    for i, (w, h, col) in enumerate(tiers):
        x0, x1 = -w / 2, w / 2
        inset = 14
        face = _poly([(x0, y), (x0 + inset, y - h), (x1 - inset, y - h), (x1, y)])
        out += _p(face, col, 4.2)
        for k in range(1, 12):
            px = _lerp(x0 + 20, x1 - 20, k / 12)
            out += _line(px, y - 6, px + (inset if px < 0 else -inset) * 0.5, y - h + 8, sw=2.5,
                         color=S.shade(col, -0.2), extra='opacity="0.55"')
        out += _rect(x0 + inset - 4, y - h - 10, w - 2 * inset + 8, 12, S.shade(col, 0.15), 3.5)
        y -= h
    # shrine
    sw_, sh_ = 150, 92
    out += _rect(-sw_ / 2, y - sh_ - 10, sw_, sh_, P["stone_light"], 4)
    out += _rosette_band(-sw_ / 2 + 4, sw_ / 2 - 4, y - sh_ + 6, 18)
    out += _p(f"M-22,{y - 10} L-22,{y - 52} Q0,{y - 74} 22,{y - 52} L22,{y - 10} Z", "#4a3426", 3.5)
    out += _merlons(-sw_ / 2 - 4, sw_ / 2 + 4, y - sh_ - 10, P["stone_light"], 22, 8, 22, 3.5)
    # central stair
    out += _p("M-60,0 L-34,-374 L34,-374 L60,0 Z", S.shade(P["stone"], 0.12), 4)
    for k in range(1, 26):
        yy = -k * 15
        hw_ = _lerp(60, 34, k / 25)
        out += _line(-hw_, yy, hw_, yy, sw=2.2, color=S.shade(P["stone"], -0.3))
    return out


ZIGGURAT_K = 2.4


def ziggurat(x, y, scale=1.0):
    return _place(_upscale(_ziggurat(), ZIGGURAT_K), x, y, scale)


def _haze(markup, tint, k_fill, k_ink, sw_mul=1.0):
    """Push every colour in markup toward tint (aerial perspective): fills by k_fill, the umber ink by k_ink;
    stroke widths are multiplied by sw_mul."""
    ink = INK.lower()

    def col(m):
        attr, c = m.group(1), m.group(2)
        k = k_ink if (attr == "stroke" and c.lower() == ink) else k_fill
        return f'{attr}="{S.mix(c, tint, _clamp(k))}"'
    return _ink(re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6})"', col, markup), sw_mul)


def _sky_house(xx, ground, w, h, c, s, rng, parapet=False):
    out = _rect(xx, ground - h, w, h, c, 2.8)
    out += _rect(xx - 3 * s, ground - h - 6 * s, w + 6 * s, 8 * s, S.shade(c, 0.15), 2.4)
    for _ in range(rng.randint(1, 3)):
        wx = xx + rng.uniform(8 * s, max(9 * s, w - 18 * s))
        wy = ground - h + rng.uniform(16 * s, max(17 * s, h - 50 * s))
        out += _rect(wx, wy, 9 * s, 13 * s, "#5b4232", 0, rx=3 * s)
    if parapet:
        out += _merlons(xx, xx + w, ground - h - 6 * s, c, 16 * s, 6 * s, 12 * s, 2.4)
    return out


def _palace(s):
    """A wide Assyrian palace block with two towers and a glazed band (local, bottom centre at 0,0)."""
    col, lt = P["stone"], P["stone_light"]
    out = ""
    for tx in (-150, 150):
        out += _merlons(tx - 44, tx + 44, -250, lt, 20, 8, 18, 3)
        out += _rect(tx - 40, -250, 80, 250, lt, 3.5)
        out += _rect(tx - 7, -210, 14, 30, "#5b4232", 0, rx=7)
    out += _merlons(-112, 112, -190, col, 22, 9, 20, 3)
    out += _rect(-112, -190, 224, 190, col, 3.5)
    out += _rosette_band(-108, 108, -160, 22)
    out += _p("M-34,0 L-34,-70 A34,34 0 0 1 34,-70 L34,0 Z", "#5b4232", 3)
    for wx in (-80, 70):
        out += _rect(wx, -120, 12, 24, "#5b4232", 0, rx=6)
    return _g(out, f"scale({s:.3f})")


def _skyline(x0, x1, y, scale=1.0, seed=0, haze=0.35, tint=None):
    rng = random.Random(seed)
    tint = tint or P["sky_warm"]
    s = scale
    swm = min(1.0, 0.45 + 0.55 * s)

    def hz(markup, extra):
        k = _clamp(haze + extra)
        return _haze(markup, tint, k, 0.5 * k + 0.1 * extra, swm)
    layers = []
    # far landmarks: a ziggurat and (on wide panoramas) a palace or a smaller second ziggurat
    lm = ""
    zx = x0 + (x1 - x0) * rng.uniform(0.22, 0.38)
    lm += _g(_ziggurat(), f"translate({_f(zx)},{_f(y - 105 * s)}) scale({0.8 * s:.3f})")
    if x1 - x0 > 900 * s:
        px = x0 + (x1 - x0) * rng.uniform(0.66, 0.8)
        if rng.random() < 0.65:
            lm += _g(_palace(1.0), f"translate({_f(px)},{_f(y - 105 * s)}) scale({1.2 * s:.3f})")
        else:
            lm += _g(_ziggurat(), f"translate({_f(px)},{_f(y - 105 * s)}) scale({0.55 * s:.3f})")
    layers.append(hz(lm, 0.24))
    # two or three staggered rows of flat roofs climbing the city mound, farthest first
    for r, (hmin, hmax, ex, off) in enumerate(((150, 230, 0.17, 0), (110, 175, 0.11, 0.45), (70, 130, 0.05, 0.2))):
        row = ""
        xx = x0 - 30 - off * 90 * s
        while xx < x1:
            w = rng.uniform(58, 125) * s
            h = rng.uniform(hmin, hmax) * s
            c = rng.choice((P["sand"], P["stone"], P["sand_light"], _WALL["terra"]))
            row += _sky_house(xx, y - 40 * s * (2 - r) / 2, w, h, c, s, rng, rng.random() < 0.22)
            xx += w * rng.uniform(0.72, 1.0)
        layers.append(hz(row, ex))
        if r == 0:   # tall towers and palms rise between the back rows
            tw_ = ""
            for _ in range(int((x1 - x0) / (420 * s)) + 1):
                tx = rng.uniform(x0 + 40 * s, x1 - 40 * s)
                th = rng.uniform(250, 320) * s
                tw = rng.uniform(34, 48) * s
                tw_ += _merlons(tx - tw / 2 - 3 * s, tx + tw / 2 + 3 * s, y - th, P["stone_light"], 12 * s, 5 * s,
                                12 * s, 2.4)
                tw_ += _rect(tx - tw / 2, y - th, tw, th, P["stone_light"], 2.6)
                tw_ += _rect(tx - 4 * s, y - th + 20 * s, 8 * s, 16 * s, "#5b4232", 0, rx=4 * s)
            layers.append(hz(tw_, 0.14))
            palms = ""
            for _ in range(int((x1 - x0) / (240 * s)) + 1):
                px = rng.uniform(x0, x1)
                palms += _g(_palm(rng.uniform(-0.3, 0.3), 0, False),
                            f"translate({_f(px)},{_f(y - 50 * s)}) scale({0.3 * s * rng.uniform(0.85, 1.1):.3f})")
            layers.append(hz(palms, 0.1))
    # city wall with towers in front
    wh = 110 * s
    wc = P["sand"]
    wall = _merlons(x0, x1, y - wh, wc, 22 * s, 9 * s, 18 * s, 2.8)
    wall += _rect(x0, y - wh, x1 - x0, wh, wc, 3)
    for yy in range(int(y - wh + 16 * s), int(y), max(6, int(16 * s))):
        wall += _line(x0 + 3, yy, x1 - 3, yy, sw=1.4, color=S.shade(wc, -0.2), extra='opacity="0.35"')
    tx = x0 + rng.uniform(40, 160) * s
    while tx < x1 - 30 * s:
        tw = 54 * s
        wall += _merlons(tx - tw / 2, tx + tw / 2, y - wh - 34 * s, S.shade(wc, 0.05), 14 * s, 6 * s, 14 * s, 2.6)
        wall += _rect(tx - tw / 2, y - wh - 34 * s, tw, wh + 34 * s, S.shade(wc, 0.05), 3)
        wall += _rect(tx - 4 * s, y - wh - 14 * s, 8 * s, 20 * s, "#4a3426", 0, rx=4 * s)
        tx += rng.uniform(220, 320) * s
    layers.append(hz(wall, -0.08))
    return "".join(layers)


def nineveh_skyline(x0, x1, y, scale=1.0, seed=0, haze=0.35, tint=None):
    return _place(_skyline(x0, x1, y, scale, seed, haze, tint), 0, 0, 1.0)


def _dock(x0, x1, y, depth=250, bollards=True):
    wood, wd, wl = P["wood"], P["wood_dark"], P["wood_light"]
    out = ""
    posts = []
    px = x0 + 40
    while px <= x1 - 30:
        posts.append(px)
        px += 150
    for a, b in zip(posts, posts[1:]):
        out += _tube(f"M{a},{y + 56} L{b},{y + depth * 0.7}", 9, wd, 3.2)
        out += _tube(f"M{b},{y + 56} L{a},{y + depth * 0.7}", 9, wd, 3.2)
    for p_ in posts:
        out += _rect(p_ - 15, y + 16, 30, depth - 16, S.shade(wood, -0.1), 4, rx=6)
        out += _rect(p_ - 13, y + depth * 0.55, 26, depth * 0.45 - 3, S.mix(wd, P["sea_deep"], 0.25), 0, rx=4,
                     extra='opacity="0.8"')
        out += _line(p_ - 6, y + 56, p_ - 6, y + depth - 20, sw=2.5, color=wd, extra='opacity="0.6"')
    out += _rect(x0, y, x1 - x0, 18, wl, 4, rx=4)
    out += _rect(x0, y + 16, x1 - x0, 32, wood, 4, rx=3)
    xx = x0 + 60
    while xx < x1:
        out += _line(xx, y + 2, xx, y + 16, sw=2.5, color=wd)
        xx += 60
    xx = x0 + 30
    while xx < x1:
        out += _circ(xx, y + 32, 3, wd, 0)
        xx += 75
    if bollards:
        for p_ in posts[1::2]:
            out += _rect(p_ - 14, y - 42, 28, 44, S.shade(wood, -0.1), 4, rx=8)
            out += _ell(p_, y - 42, 14, 5, wl, 3)
            for k in range(3):
                out += _line(p_ - 15, y - 28 + k * 9, p_ + 15, y - 24 + k * 9, sw=4, color=INK)
                out += _line(p_ - 15, y - 28 + k * 9, p_ + 15, y - 24 + k * 9, sw=2, color=P["sackcloth"])
    return out


def harbor_dock(x0, x1, y, depth=250, bollards=True, scale=1.0):
    s = max(0.05, scale)
    body = _dock(0, (x1 - x0) / s, 0, depth / s, bollards)
    return _place(body, x0, y, s, 1)


def _signpost(left_text="他施", right_text="尼尼微"):
    out = ""
    out += _p("M-12,0 L-12,-322 L0,-340 L12,-322 L12,0 Z", P["wood"], 4)
    out += _line(-3, -310, -3, -20, sw=2.5, color=P["wood_dark"], extra='opacity="0.6"')
    boards = []
    if left_text:
        tw = 50 * len(left_text) + 40
        boards.append((-1, -276, tw, left_text, S.mix(P["wood_light"], P["sand"], 0.3)))
    if right_text:
        tw = 50 * len(right_text) + 40
        boards.append((1, -196, tw, right_text, P["wood_light"]))
    for d, yc, tw, txt, col in boards:
        hh = 30
        if d < 0:
            pts = [(26, yc - hh), (-26 - tw, yc - hh), (-26 - tw - 30, yc), (-26 - tw, yc + hh), (26, yc + hh)]
            tx = -26 - tw / 2 - 6
        else:
            pts = [(-26, yc - hh), (26 + tw, yc - hh), (26 + tw + 30, yc), (26 + tw, yc + hh), (-26, yc + hh)]
            tx = 26 + tw / 2 + 6
        out += _p(_poly(pts), col, 4)
        out += _line(pts[0][0] + d * 8, yc + hh - 9, pts[1][0] - d * 6, yc + hh - 9, sw=2.2, color=P["wood"],
                     extra='opacity="0.7"')
        out += _circ(d * -8, yc, 4, P["wood_dark"], 0)
        out += S.text(_f(tx), _f(yc + 16), txt, size=44, fill=S.shade(INK, 0.05), weight="bold")
    out += _ell(-18, -2, 18, 8, P["stone"], 3) + _ell(16, 0, 14, 7, P["stone_dark"], 3)
    out += _g(_grass(0), "translate(28,0) scale(0.6)")
    return out


def signpost(x, y, scale=1.0, left_text="他施", right_text="尼尼微"):
    return _place(_signpost(left_text, right_text), x, y, scale)
